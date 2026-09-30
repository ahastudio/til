# Next.js에서 겹치는 낙관적 업데이트 조율하기: useActionState로 줄 세우고 useOptimistic으로 먼저 보여 주기

원문: [Coordinating Optimistic Updates in Next.js | Aurora Scharff](https://aurorascharff.no/posts/coordinating-optimistic-updates-in-nextjs/)

## 소개

Aurora Scharff가 2026년 8월 13일 자기 블로그에 쓴 글이다.
저자는 Next.js로 SPA 같은 경험을 만드는 예제 앱(Next Beats, Drop, Flow, Huddle)을 연재해 왔고,
이 글에서는 그 가운데 Huddle과 Flow에서 쓴 패턴, 곧 사용자의 쓰기 작업이 겹칠 때 낙관적 업데이트를 조율하는 방법을 다룬다.

겹치는 쓰기는 웹에서 흔한 문제이며 프레임워크마다 다르게 다룬다.
React Router는 중단된 요청과 오래된 재검증을 취소하고, Solid Router는 대기 중인 제출을 추적한다.
React에서는 `useActionState`와 `useOptimistic`을 조합한다는 것이 글의 출발점이다.

글이 약속하는 것은 세 가지다.
여러 변경이 빠르게 이어져도 서버에는 사용자가 만든 순서대로 저장되고, 화면에는 저장을 기다리지 않고 즉시 반영되며, 저장이 실패하면 역연산 없이 마지막으로 확정된 상태로 돌아간다.
확정된 데이터는 계속 Server Component가 소유하고, 클라이언트 상태는 상호작용을 조율할 만큼만 더한다는 것이 저자가 이 패턴을 좋아하는 이유다.

예제는 두 개다.
Slack 비슷한 팀 채팅 앱 Huddle의 채널 사이드바는 한 컴포넌트 안에서 패턴을 완성하고,
캘린더 앱 Flow의 일정 보드는 같은 패턴을 컴포넌트 트리 전체로 넓힌다.

## 동작 방식

### 먼저 무엇이 깨지는가

Huddle의 사이드바에서 채널을 끌어 다른 그룹으로 옮기면 전체 레이아웃을 저장하는 Server Function을 부른다.
가장 단순한 구현은 현재 레이아웃에서 다음 레이아웃을 계산해 Transition 안에서 저장하는 것이다.

Next.js는 현재 Server Action을 한 번에 하나씩 보내고 기다리므로 요청끼리 경쟁하지는 않는다.
문제는 다른 곳에 있다.
다음 레이아웃은 저장이 대기열에 들어가기 전에 계산된다.
첫 저장이 끝나기 전에 사용자가 두 번째 변경을 하면, 두 번째 레이아웃은 두 변경이 모두 반영되기 전의 레이아웃에서 계산된다.
요청은 순서대로 쓰이지만 나중 요청이 마지막에 도착하면서 앞의 변경을 지운다.
전형적인 갱신 손실(lost update)이다.

저장 중에 컨트롤을 막으면 해결되지만 드래그와 편집이 느리게 느껴진다.
저자는 사이드바를 계속 조작 가능하게 두고, 나중 변경이 앞 저장의 결과 위에 쌓이게 만드는 쪽을 택한다.

### useActionState가 대기열이 된다

`useActionState`는 Action의 결과를 상태로 저장하고, 디스패처로 들어온 호출을 줄 세운다.
여러 변경을 디스패치하면 React는 한 콜백이 끝나기를 기다렸다가 그 결과를 다음 콜백의 이전 상태로 넘긴다.
그래서 콜백 안에서 저장을 기다리고, 저장된 결과를 반환하면 다음 변경은 그 결과 위에서 계산된다.
`isPending`은 대기열의 모든 저장이 끝날 때까지 참이다.

이렇게 하려면 저장 함수가 “완성된 다음 레이아웃”이 아니라 “이전 레이아웃과 무엇이 바뀌었는지”를 받아야 한다.
저자는 레이아웃 갱신을 리듀서로 뽑아내고, 변경을 `move`, `addGroup`, `renameGroup`, `deleteGroup`, `moveGroup` 같은 `LayoutChange` 값으로 표현한다.
Server Function은 이전 레이아웃과 변경을 받아 리듀서로 다음 레이아웃을 계산하고, 저장한 뒤 반환한다.

### useOptimistic이 화면을 앞서 보여 준다

대기열만으로는 저장이 끝나야 화면이 바뀐다.
`useOptimistic`은 확정 상태를 첫 인자로 받고, 추가된 낙관적 값을 갱신 함수로 적용한 결과를 Action이 대기 중인 동안 보여 준다.
확정 상태가 그사이 바뀌면 React는 갱신 함수를 새 확정 상태 위에 다시 적용한다.

Huddle에서 확정 상태는 `useActionState`의 레이아웃이고, 낙관적 값은 `LayoutChange`다.
이미 있는 리듀서가 정확히 이 두 값을 받으므로 그대로 갱신 함수로 넘긴다.
그래서 같은 리듀서가 서버에서는 저장할 레이아웃을, 클라이언트에서는 보여 줄 레이아웃을 계산한다.

### 실패하면 확정 상태로 돌아간다

`useActionState` 콜백 안에서 저장이 실패하면 토스트를 띄우고 이전 상태를 그대로 반환한다.
Action이 끝나면 React는 낙관적 상태를 버리고 확정 상태를 렌더링하는데, 실패했으므로 확정 상태는 마지막으로 성공한 저장의 결과다.
사이드바는 역방향 `LayoutChange` 없이 원래 자리로 돌아간다.

### 시간 순서로 보기

사용자가 채널 A를 그룹 X로 옮기고, 첫 저장이 끝나기 전에 채널 B를 그룹 Y로 옮긴다고 하자.

```text
t0  확정 상태 S0, 화면 S0
t1  move(A→X): addOptimistic + dispatch
    화면 = reducer(S0, A→X)                  저장 1 시작(이전 상태 S0)
t2  move(B→Y): addOptimistic + dispatch
    화면 = reducer(reducer(S0, A→X), B→Y)    저장 2는 대기열에서 기다린다
t3  저장 1 완료 → 확정 상태 S1 = reducer(S0, A→X)
    화면 = reducer(S1, B→Y)                  (남은 낙관적 변경을 새 확정 상태 위에 다시 적용)
                                             저장 2 시작(이전 상태 S1)
t4  저장 2 완료 → 확정 상태 S2 = reducer(S1, B→Y)
    Transition 종료, 낙관적 상태 폐기, 화면 S2
```

저장 2가 실패했다면 t4에서 확정 상태는 S1로 남고, 화면은 B만 원래 자리로 돌아간 S1이 된다.
A의 이동은 이미 저장되었으므로 유지된다.

### 트리 전체로 넓히기

Flow의 캘린더에서는 주간 보드, 월간 보드, 헤더의 새 일정 버튼이 모두 같은 낙관적 상태를 읽거나 써야 하고, 그 사이에 Server Component가 끼어 있다.
props로 넘기려면 중간의 Server Component를 모두 Client Component로 바꿔야 하므로, 저자는 헤더와 선택된 뷰를 감싸는 Context 프로바이더를 둔다.

어려운 점은 낙관적 상태의 기준 상태다.
일정 리듀서는 이미 목록에 있는 일정을 옮기고 늘이고 지우므로 기준이 일정 목록이어야 하는데,
일정은 프로바이더 아래의 `CalendarWeek`와 `CalendarMonth`에서 따로 가져오고 두 뷰의 범위도 다르다.
그래서 저자는 일정 대신 변경 목록을 낙관적 상태로 둔다.
변경 목록은 빈 배열에서 시작해 덧붙기만 하므로 서버 데이터 없이 프로바이더가 가질 수 있고,
각 보드는 자기가 받은 서버 일정 위에 그 목록을 차례로 재생한다.

Flow에서는 이전 저장의 결과가 다음 변경에 필요 없으므로 Action 상태를 `void`로 둔다.
일정 하나는 행 하나를 따로 갱신하므로, Huddle처럼 전체를 다시 계산해 저장할 필요가 없기 때문이다.
대신 서버 함수는 오류나 갱신된 행을 반환하고, 오류가 있으면 콜백이 토스트를 띄운다.
실패한 쓰기는 서버 일정을 바꾸지 않으므로 Transition이 끝나면 일정이 원래 자리로 돌아간다.

## 구현하기

### 공유 리듀서

서버와 클라이언트가 같이 쓰는 순수 함수다.
원문의 채널 레이아웃 리듀서에서 `move`와 `addGroup`만 남겼다.

```typescript
// lib/layout-reducer.ts
export type Channel = { id: string; name: string };
export type LayoutGroup = { name: string; channels: Channel[] };

export type LayoutChange =
  | { type: "move"; channelId: string; toGroup: string; toIndex: number }
  | { type: "addGroup"; name: string };

// 입력을 바꾸지 않는다. 같은 입력에는 서버와 클라이언트에서 같은 결과를 낸다.
export function layoutReducer(groups: LayoutGroup[], change: LayoutChange): LayoutGroup[] {
  switch (change.type) {
    case "move": {
      const moved = groups.flatMap(g => g.channels).find(c => c.id === change.channelId);
      const next = groups.map(g => ({
        ...g,
        channels: g.channels.filter(c => c.id !== change.channelId),
      }));
      const target = next.find(g => g.name === change.toGroup);
      // 대상이 없으면 조용히 무시한다. 앞선 변경이 실패했을 때 여기로 온다(함정 참고).
      if (!moved || !target) return groups;
      const index = Math.max(0, Math.min(change.toIndex, target.channels.length));
      target.channels.splice(index, 0, moved);
      return next;
    }
    case "addGroup": {
      if (groups.some(g => g.name === change.name)) return groups;
      return [...groups, { name: change.name, channels: [] }];
    }
  }
}
```

### Server Function

실험용으로 메모리 저장소를 쓰고, 지연과 실패를 흉내 낸다.
실제 앱이라면 이 자리에서 트랜잭션으로 쓰고 캐시를 무효화한다.

```typescript
// app/actions.ts
"use server";

import { layoutReducer, type LayoutChange, type LayoutGroup } from "@/lib/layout-reducer";

let saved: LayoutGroup[] = [
  { name: "Starred", channels: [] },
  { name: "Channels", channels: [{ id: "a", name: "general" }, { id: "b", name: "random" }] },
];

export async function getLayout() {
  return saved;
}

export async function saveLayout(previous: LayoutGroup[], change: LayoutChange) {
  await new Promise(r => setTimeout(r, 1500));            // 네트워크와 DB 지연
  if (change.type === "addGroup" && change.name.startsWith("fail")) {
    throw new Error("save failed");                       // 실패 경로 확인용
  }
  // 클라이언트가 보낸 previous가 아니라 서버의 saved를 기준으로 계산한다(트레이드오프 참고).
  saved = layoutReducer(saved, change);
  return saved;
}
```

### 클라이언트 컴포넌트

원문의 `ChannelNav`와 같은 구조다.
`useActionState`가 대기열과 확정 상태를, `useOptimistic`이 화면 상태를 맡는다.

```tsx
// app/channel-nav.tsx
"use client";

import { startTransition, useActionState, useOptimistic } from "react";
import { layoutReducer, type LayoutChange, type LayoutGroup } from "@/lib/layout-reducer";
import { saveLayout } from "./actions";

export function ChannelNav({ initialGroups }: { initialGroups: LayoutGroup[] }) {
  const [groups, dispatch, isPending] = useActionState(
    async (previous: LayoutGroup[], change: LayoutChange) => {
      try {
        return await saveLayout(previous, change);
      } catch {
        alert("Could not save layout.");   // 실제 앱에서는 토스트
        return previous;                   // 확정 상태를 그대로 두면 역연산 없이 되돌아간다
      }
    },
    initialGroups,
  );
  // 같은 리듀서를 갱신 함수로 쓴다. 확정 상태가 바뀌면 남은 변경이 그 위에 다시 적용된다.
  const [optimisticGroups, addOptimistic] = useOptimistic(groups, layoutReducer);

  function runChange(change: LayoutChange) {
    // 이벤트 핸들러에서 부르므로 Transition을 직접 연다. <form action>이면 자동이다.
    startTransition(() => {
      addOptimistic(change);
      dispatch(change);
    });
  }

  return (
    <nav aria-label="Channels" aria-busy={isPending}>
      {optimisticGroups.map(group => (
        <section key={group.name}>
          <h3>{group.name}</h3>
          {group.channels.map(channel => (
            <div key={channel.id}>
              #{channel.name}{" "}
              <button onClick={() => runChange({ type: "move", channelId: channel.id, toGroup: "Starred", toIndex: 0 })}>
                star
              </button>
            </div>
          ))}
        </section>
      ))}
      <button onClick={() => runChange({ type: "addGroup", name: `group-${Date.now() % 1000}` })}>add group</button>
      <button onClick={() => runChange({ type: "addGroup", name: "fail-group" })}>add failing group</button>
    </nav>
  );
}
```

```tsx
// app/page.tsx
import { getLayout } from "./actions";
import { ChannelNav } from "./channel-nav";

export default async function Page() {
  const groups = await getLayout();
  return <ChannelNav initialGroups={groups} />;
}
```

### 트리 전체로 넓힐 때의 프로바이더

Flow 방식으로 넓히려면 낙관적 상태를 데이터가 아니라 변경 목록으로 두고, 상태와 디스패치를 다른 Context로 나눈다.
디스패치만 쓰는 컴포넌트가 변경 목록이 바뀔 때마다 다시 렌더링되지 않게 하려는 것으로, React 공식 문서의 리듀서와 Context 확장 가이드를 따른 구성이다.

```tsx
// app/events-provider.tsx
"use client";

import { createContext, startTransition, useActionState, useContext, useOptimistic, type ReactNode } from "react";
import { saveEventChange, type EventChange } from "./event-actions";   // { error?: string } 를 반환하는 Server Function
import { eventReducer, type CalendarEvent } from "@/lib/event-reducer"; // 일정 목록 × 변경 → 일정 목록

const StateContext = createContext<{ isPending: boolean; pendingChanges: EventChange[] } | null>(null);
const DispatchContext = createContext<((change: EventChange) => void) | null>(null);

export function EventsProvider({ children }: { children: ReactNode }) {
  const [, dispatch, isPending] = useActionState(async (_: void, change: EventChange) => {
    const result = await saveEventChange(change);
    if (result.error) alert(result.error);   // 서버 일정은 그대로이므로 끝나면 제자리로 돌아간다
  }, undefined);

  // 기준 상태가 빈 배열이라 서버 데이터가 없어도 된다. 덧붙기만 한다.
  const [pendingChanges, addChange] = useOptimistic<EventChange[], EventChange>(
    [],
    (changes, change) => [...changes, change],
  );

  function mutate(change: EventChange) {
    startTransition(() => {
      addChange(change);
      dispatch(change);
    });
  }

  return (
    <StateContext.Provider value={{ isPending, pendingChanges }}>
      <DispatchContext.Provider value={mutate}>{children}</DispatchContext.Provider>
    </StateContext.Provider>
  );
}

// 각 보드는 자기가 받은 서버 일정 위에 대기 중인 변경을 재생한다.
export function useOptimisticEvents(events: CalendarEvent[]) {
  const state = useContext(StateContext);
  if (!state) throw new Error("useOptimisticEvents must be used within EventsProvider");
  return state.pendingChanges.reduce(eventReducer, events);
}

export function useEventsDispatch() {
  const mutate = useContext(DispatchContext);
  if (!mutate) throw new Error("useEventsDispatch must be used within EventsProvider");
  return mutate;
}
```

## 트레이드오프

### 대기열은 순서를 주는 대신 지연을 쌓는다

`useActionState`의 대기열은 변경을 하나씩 처리하므로 순서가 보장된다.
대신 각 변경은 앞의 왕복이 끝나야 시작된다.
사용자가 1초에 다섯 번 드래그하고 저장 한 번이 300ms라면, 마지막 변경은 1.5초 뒤에야 서버에 도달한다.
화면은 낙관적 상태로 즉시 바뀌므로 사용자는 느끼지 못하지만, 그동안 탭을 닫으면 뒤쪽 변경은 사라진다.

이 지연을 줄이는 명백한 방법, 곧 대기열의 변경을 묶어 한 번에 보내는 것은 이 패턴 안에서는 쉽지 않다.
`useActionState`는 호출마다 콜백을 한 번씩 부르므로, 묶으려면 대기열 밖에서 디바운스하거나 콜백 안에서 직접 버퍼를 관리해야 한다.
그러면 “변경 하나당 저장 하나”라는 단순한 실패 의미가 흐려진다.
Huddle처럼 레이아웃 전체를 저장하는 경우에는 매 변경마다 모든 그룹과 채널을 다시 쓰므로, 변경이 잦을수록 쓰기 비용도 선형으로 는다.

### 이전 상태를 클라이언트가 들고 있다

Huddle의 설계에서 다음 레이아웃은 `useActionState`가 들고 있는 이전 레이아웃에서 계산된다.
이 이전 레이아웃은 처음에 서버에서 받은 `initialGroups`로 시작하고, 이후로는 저장 결과로만 바뀐다.
`useActionState`는 초기값을 처음 한 번만 쓰므로, 다른 탭이나 다른 기기에서 레이아웃이 바뀌어 서버 컴포넌트가 새 props를 내려보내도 이 상태는 따라가지 않는다.

그 상태에서 변경을 저장하면, 클라이언트가 보낸 오래된 이전 레이아웃에 변경을 적용한 결과가 서버의 최신 레이아웃을 덮어쓴다.
원문의 코드처럼 서버 함수가 클라이언트가 넘긴 `groups`를 기준으로 계산하면 이 문제가 그대로 드러난다.
위 구현에서 서버가 넘겨받은 값이 아니라 저장된 값을 기준으로 계산하게 한 것은 그 때문이다.
대신 그렇게 하면 클라이언트의 확정 상태와 서버의 계산 기준이 달라질 수 있으므로, 서버는 계산한 결과를 반드시 반환해 클라이언트 상태를 맞춰야 한다.
원문의 `key={userId}`는 사용자가 바뀔 때만 상태를 초기화하므로 이 경우를 막지 못한다.

Flow의 설계는 이 문제를 비켜 간다.
확정 데이터는 늘 Server Component가 내려보내는 일정이고, 클라이언트는 변경 목록만 들고 있기 때문이다.
그래서 여러 곳에서 동시에 바뀔 수 있는 데이터라면 Huddle보다 Flow 방식이 안전하다.
대신 서버 함수는 변경 하나를 독립적으로 적용할 수 있어야 하고, 이전 저장의 결과에 의존하는 변경은 표현하기 어렵다.

### 되돌리기가 공짜인 대신 부분 실패가 보이지 않는다

실패하면 확정 상태로 돌아간다는 설계는 역연산을 짤 필요가 없어서 우아하다.
하지만 Action이 대기열의 마지막 변경까지 끝나야 낙관적 상태가 폐기되므로, 중간 변경이 실패해도 화면은 끝까지 낙관적 상태를 보여 준다.
실패는 토스트로만 알리고, 화면은 모든 저장이 끝난 뒤에 한꺼번에 확정 상태로 돌아간다.

그 사이에 사용자는 실패한 변경 위에 다음 변경을 쌓을 수 있다.
새 그룹을 만들고 채널을 그 그룹으로 옮겼는데 그룹 생성이 실패했다면, 서버는 없는 그룹으로 채널을 옮기라는 요청을 받는다.
리듀서가 대상 그룹이 없다며 조용히 무시하면 채널 이동도 사라지는데, 사용자는 그룹 생성 실패 토스트 하나만 본다.
의존 관계가 있는 변경을 다룬다면, 실패한 변경에 의존하는 뒤 변경도 실패로 알리거나 앞 변경이 실패했을 때 대기열의 나머지를 버리는 규칙이 필요하다.

### 클라이언트 데이터 라이브러리와의 경계

저자는 Huddle의 메시지처럼 데이터가 스스로 바뀌는 경우, 곧 읽는 동안 새 메시지가 도착하는 경우에는 TanStack Query나 SWR을 쓴다고 밝힌다.
SWR 버전에서는 서버에서 메시지를 불러 캐시에 미리 넣고, 클라이언트 훅이 같은 키로 이어받아 10초마다 폴링한다.
대신 Next.js 캐시와 SWR 캐시라는 두 캐시를 맞춰야 하므로, 변경마다 서버 함수에서 Next.js 캐시를 무효화하고 브라우저에서 해당 SWR 키도 갱신해야 한다.
채널 레이아웃처럼 사용자가 드래그할 때만 바뀌는 데이터에는 두 훅으로 충분하다는 것이 저자의 기준이다.

## 함정

### Next.js의 직렬 실행에 기대고 있다

글 전체가 Next.js가 Server Action을 한 번에 하나씩 보낸다는 현재 동작 위에 서 있다.
`useActionState` 자체도 콜백을 순서대로 부르므로 이 패턴 안에서는 괜찮지만,
같은 화면의 다른 곳에서 `useTransition` 안에 직접 `fetch`나 다른 비동기 작업을 넣으면 그 작업들은 순서가 보장되지 않는다.
React 문서가 Transition 안의 상태 갱신이 순서 없이 끝날 수 있다고 경고하는 부분이다.
한 데이터에 대한 쓰기는 모두 같은 `useActionState` 디스패처를 거치게 해야 한다.

### 캐시 무효화를 빠뜨리면 되돌아갔다가 다시 온다

Action이 끝나면 낙관적 상태가 폐기되고 확정 상태가 렌더링된다.
Flow처럼 확정 상태가 Server Component의 데이터라면, 서버 함수 안에서 캐시를 무효화해야 같은 Transition 안에서 새 데이터가 도착한다.
무효화가 빠지면 일정이 낙관적 위치에서 옛 위치로 돌아갔다가, 나중에 새로고침하면 다시 새 위치로 가는 깜빡임이 생긴다.
원문 코드가 매번 “캐시를 무효화한다”는 주석을 남겨 둔 곳이 바로 이 자리다.

### 생성한 항목의 임시 식별자

낙관적으로 만든 일정은 서버가 실제 식별자를 주기 전까지 클라이언트가 만든 식별자를 쓴다.
원문의 Flow 리듀서에서 `move`는 `id`로, `delete`와 `resize`와 `update`는 `sourceId`로 일정을 찾는다.
막 만든 일정을 저장이 끝나기 전에 옮기면, 서버는 아직 모르는 식별자로 된 이동 요청을 받는다.
생성 요청이 대기열의 앞에 있으므로 순서는 맞지만, 서버가 클라이언트의 임시 식별자를 받아들이거나 생성 결과의 식별자로 뒤 변경을 바꿔 주는 장치가 필요하다.

### 서버와 클라이언트의 리듀서가 어긋난다

Huddle 방식은 같은 리듀서가 서버에서는 저장할 값을, 클라이언트에서는 보여 줄 값을 계산한다는 데 기댄다.
배포 중에 옛 클라이언트와 새 서버가 섞이면 두 리듀서의 결과가 달라지고, Action이 끝나는 순간 화면이 낙관적 결과에서 서버 결과로 튀는 모습이 보인다.
리듀서는 결정론적이어야 하고, 시각이나 난수나 환경에 따라 결과가 달라지면 안 된다.

### `isPending`은 대기열 전체에 대해 하나다

`isPending`은 대기열의 모든 저장이 끝날 때까지 참이다.
전역 저장 표시로는 적당하지만, 변경마다 “저장 중” 표시를 달려고 쓰면 첫 변경은 이미 저장됐는데도 계속 저장 중으로 보인다.
항목별 상태가 필요하면 변경 목록에서 해당 항목에 대한 대기 중인 변경이 있는지로 판단해야 한다.

## 확인하기

위의 구현을 새 Next.js 앱에 넣고 다음 순서로 확인한다.

```bash
npx create-next-app@latest optimistic-demo --ts --app --no-tailwind --no-eslint
cd optimistic-demo
mkdir -p lib
# lib/layout-reducer.ts, app/actions.ts, app/channel-nav.tsx, app/page.tsx 를 위 코드로 만든다
npm run dev
```

첫째, 순서와 갱신 손실을 확인한다.
`general` 옆의 star를 누르고 1.5초 안에 `random` 옆의 star를 누른다.
두 채널이 즉시 Starred로 올라가고, 3초 뒤 새로고침해도 둘 다 Starred에 있어야 한다.
`useActionState` 대신 현재 화면 상태로 다음 레이아웃을 계산해 `saveLayout`을 직접 부르도록 바꾸면, 새로고침 뒤 하나만 남는 것을 볼 수 있다.

둘째, 되돌리기를 확인한다.
add failing group을 누르면 그룹이 즉시 나타났다가, 1.5초 뒤 실패 알림과 함께 사라져야 한다.

셋째, 부분 실패를 확인한다.
add failing group을 누르고 바로 add group을 누른다.
두 그룹이 모두 나타났다가, 3초 뒤에는 실패한 그룹만 사라지고 나머지는 남아야 한다.
그 사이 실패 알림이 떴는데도 두 그룹이 계속 보이는 구간이 있다는 점도 함께 확인한다.

## 체크리스트

- 같은 데이터에 대한 모든 쓰기가 하나의 `useActionState` 디스패처를 거치는가?
- 다음 상태를 현재 화면 상태가 아니라 대기열이 넘겨주는 이전 상태에서 계산하는가?
- `addOptimistic`과 `dispatch`를 같은 `startTransition` 안에서 부르는가?
- 낙관적 갱신 함수와 서버 계산이 같은 결정론적 리듀서를 쓰는가?
- 실패 시 콜백이 이전 상태를 반환하거나 서버 데이터가 바뀌지 않은 채로 남는가?
- 서버 함수 안에서 캐시를 무효화하는가?
- 다른 탭이나 사용자가 같은 데이터를 바꿀 수 있다면 서버가 최신 저장값을 기준으로 계산하는가?
- 실패한 변경에 의존하는 뒤 변경을 어떻게 알릴지 정했는가?
- 트리 전체에서 쓴다면 낙관적 상태를 데이터가 아니라 변경 목록으로 두었는가?
- 상태 Context와 디스패치 Context를 나누었는가?
- 데이터가 사용자 조작 없이도 바뀐다면 클라이언트 데이터 라이브러리를 검토했는가?

## 기억할 원칙

### 상태가 아니라 변경을 보내라

이 패턴의 핵심은 “다음 상태”가 아니라 “무엇이 바뀌었는지”를 다루는 것이다.
완성된 다음 상태를 보내면 그 상태를 계산한 시점의 전제가 함께 실려 가고, 그 전제가 낡으면 앞의 변경을 지운다.
변경을 보내면 그 변경이 적용될 기준 상태를 받는 쪽이 정할 수 있다.

Huddle과 Flow의 차이도 여기서 나온다.
Huddle은 변경과 함께 기준 상태를 클라이언트가 넘겨 서버가 그 위에 계산하고, Flow는 변경만 넘겨 서버가 자기 데이터 위에 적용한다.
기준 상태를 누가 쥐느냐가 동시성의 안전성을 정한다.
데이터베이스가 전체 행을 덮어쓰는 대신 `UPDATE ... SET x = x + 1`을 쓰는 것과 같은 원리다.

### 확정 상태는 한 곳에만 두고 낙관적 상태는 버릴 것으로 다뤄라

저자가 이 패턴을 좋아하는 이유로 든 것은 Server Component가 계속 데이터를 소유한다는 점이다.
낙관적 상태는 Action이 끝나면 버려지는 일시적 투영일 뿐이고, 확정 상태는 서버에서 온 값 하나뿐이다.
그래서 실패하면 버리기만 하면 되고, 역연산도 동기화 로직도 필요 없다.

이 원칙이 깨지는 순간은 클라이언트가 확정 상태의 사본을 오래 들고 있을 때다.
Huddle의 `useActionState` 상태가 그 사본이며, 다른 곳에서 데이터가 바뀌면 그 사본이 진실과 어긋난다.
낙관적 업데이트를 설계할 때 먼저 물어야 할 것은 화면을 어떻게 빨리 바꿀지가 아니라, 확정 상태가 어디에 몇 개 있는지다.
