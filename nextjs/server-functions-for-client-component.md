# Next.js: Client Component 통신을 Server Functions로 처리하기

## 개요

Next.js App Router에서 Client Component가 서버와 통신할 때
API Route를 따로 만들지 않고 Server Functions만으로 처리하는 패턴이다.
`'use server'` 지시어를 붙인 함수를 Client Component에서 직접 호출할 수 있어
타입 안전성을 유지하면서 보일러플레이트를 대폭 줄인다.

## 핵심 개념

### Server Action vs Server Function

- **Server Function**: `'use server'`가 붙은 모든 비동기 함수 (상위 개념).
  React가 2024년 9월부터 공식화한 용어다.
- **Server Action**: Server Functions 중 `action` prop 또는
  `startTransition`으로 호출되는 서브셋.

React가 먼저 이 둘을 구분했고, Next.js는 그 용어 체계를 따른다.
Next.js 문서는 아직 “Server Actions” 중심으로 서술되어 있지만,
React 공식 문서(`react.dev`)는 Server Functions를 상위 개념으로 정의한다.

## 설정

Next.js 15 이상은 별도 설정 없이 사용 가능하다.

`next.config.ts`:

```ts
// 추가 설정 불필요 — App Router에서 기본 지원
```

## 기본 사용법

### 1. Server Functions 파일 만들기

`app/actions.ts`:

```ts
'use server';

export async function getItems() {
  // DB 조회, 외부 API 호출 등 서버 전용 로직
  return [{ id: 1, name: 'Item A' }, { id: 2, name: 'Item B' }];
}

export async function createItem(name: string) {
  // DB 저장 등
  return { id: 3, name };
}

export async function deleteItem(id: number) {
  // DB 삭제 등
}
```

### 2. Client Component에서 호출

`app/items-client.tsx`:

```tsx
'use client';

import { useState, useEffect } from 'react';
import { getItems, createItem, deleteItem } from './actions';

export default function ItemsClient() {
  const [items, setItems] = useState<{ id: number; name: string }[]>([]);

  useEffect(() => {
    getItems().then(setItems);
  }, []);

  async function handleCreate() {
    const newItem = await createItem('New Item');
    setItems((prev) => [...prev, newItem]);
  }

  async function handleDelete(id: number) {
    await deleteItem(id);
    setItems((prev) => prev.filter((item) => item.id !== id));
  }

  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>
          {item.name}
          <button onClick={() => handleDelete(item.id)}>삭제</button>
        </li>
      ))}
      <button onClick={handleCreate}>추가</button>
    </ul>
  );
}
```

### 3. Server Component에서 초기 데이터 주입 (권장)

데이터 패칭은 Server Component에서 처리하고,
변경(mutation)만 Server Functions에 맡기는 방식이 더 깔끔하다.

`app/items-page.tsx` (Server Component):

```tsx
import { getItems } from './actions';
import ItemsClient from './items-client';

export default async function ItemsPage() {
  const initialItems = await getItems();
  return <ItemsClient initialItems={initialItems} />;
}
```

`app/items-client.tsx`:

```tsx
'use client';

import { useState } from 'react';
import { createItem, deleteItem } from './actions';

type Item = { id: number; name: string };

export default function ItemsClient({ initialItems }: { initialItems: Item[] }) {
  const [items, setItems] = useState(initialItems);
  // ... 이하 동일
}
```

## 에러 처리

```ts
'use server';

export async function createItem(name: string) {
  try {
    // 처리 로직
    return { ok: true, data: { id: 3, name } };
  } catch (e) {
    return { ok: false, error: '저장에 실패했습니다.' };
  }
}
```

```tsx
'use client';

async function handleCreate() {
  const result = await createItem('New Item');
  if (!result.ok) {
    alert(result.error);
    return;
  }
  setItems((prev) => [...prev, result.data]);
}
```

## 주의사항

- Server Functions 파일에는 `'use server'`를 파일 최상단에 선언한다.
- 인자와 반환값은 직렬화 가능한 타입이어야 한다 (함수, 클래스 인스턴스 불가).
- 민감한 로직이 서버에서만 실행되므로 클라이언트에 노출되지 않는다.
- 내부적으로 HTTP POST 요청으로 변환되므로 네트워크 탭에서 확인할 수 있다.

## 분석

### API Route와의 비교

| 항목         | API Route                  | Server Functions          |
| ------------ | -------------------------- | ------------------------- |
| 파일 위치    | `app/api/*/route.ts`       | 아무 `.ts` 파일           |
| 호출 방법    | `fetch('/api/...')`        | 함수 직접 호출            |
| 타입 안전성  | 수동 타입 정의 필요        | 자동 (TypeScript 추론)    |
| 보일러플레이트 | Request/Response 파싱 필요 | 없음                      |
| 외부 공개    | URL로 직접 접근 가능       | 빌드 타임 내부 참조       |

Server Functions는 외부에 공개할 필요 없는 내부 통신에 적합하고,
API Route는 외부 클라이언트(모바일 앱, 서드파티)가 소비해야 할 때 유리하다.

### 아키텍처 관점

모든 Client Component 통신을 Server Functions로 통일하면
“서버 로직이 어디에 있는가”가 명확해진다.
API Route가 흩어져 있을 때 생기는 “이 데이터는 어느 엔드포인트에서 오는가”
같은 탐색 비용이 사라진다.

## 비평

### 장점

함수 호출 시그니처가 곧 API 계약이기 때문에,
API 스펙을 별도로 관리하지 않아도 타입스크립트 컴파일러가 일관성을 보장한다.
소규모 팀이나 풀스택 Next.js 앱에서 개발 속도를 크게 높일 수 있다.

### 단점과 한계

직렬화 제약으로 인해 Date, Map, Set 같은 타입은 그대로 전달할 수 없어
변환 레이어가 필요하다.
또한 네트워크 요청이 암묵적으로 발생하므로,
요청 횟수나 캐싱 전략에 주의하지 않으면 성능 문제가 생길 수 있다.
외부 파트너가 API를 소비해야 하는 경우에는 API Route와 병행해야 한다.

## 인사이트

### “API Route 없는 풀스택”의 의미

Server Functions 패턴이 의미하는 바는 단순히 코드 절감이 아니다.
클라이언트-서버 경계를 “URL”이 아닌 “함수 호출”로 표현한다는 설계 철학의 변화다.
URL은 외부 계약(external contract)이고 함수는 내부 계약(internal contract)이다.
외부에 공개할 필요 없는 통신에 URL을 붙이는 것은 과잉 설계였다는 성찰에서 나온 방향이다.

### 경계의 점진적 이동

React Server Components가 “렌더링 경계”를 컴포넌트 단위로 옮겼다면,
Server Functions는 “통신 경계”를 함수 단위로 옮기고 있다.
두 흐름이 합쳐지면 Next.js 앱에서 개발자가 인식해야 할
클라이언트/서버 경계의 총량이 줄어들고,
대신 컴파일러와 프레임워크가 그 경계를 관리하게 된다.
이는 네트워크를 “신경 써야 할 인프라”에서 “투명한 구현 세부사항”으로
추상화하는 장기 방향의 일부다.
