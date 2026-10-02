# Pi Durable: 크래시에서 살아남아 이어 가는 에이전트 하네스를 만드는 법

원문: [Pi Durable | Earendil](https://earendil.com/posts/pi-durable/)

HN 토론: <https://news.ycombinator.com/item?id=49925969> (298점, 37개 댓글)

GN 토론: <https://news.hada.io/topic?id=34641>

## 소개

Pi Durable은 Earendil이 Pi 1.0과 함께 2026년 10월 1일에 내놓은 실험 패키지다.
오래 돌고(long-running) 내구성이 있으며(durable) 고칠 수 있는(malleable)
에이전트를 어디서든 돌리기 위한 것이라고 한다.
Pi 코딩 에이전트는 사용자의 (원격) 기계에서 터미널 안에서 한 사람이 몰며,
프로세스가 죽으면 사람이 무슨 일이 있었는지 보고 계속하라고 시킨다.
Pi Durable은 이를 대체하지 않고,
어디서든 돌고 여러 표면에서 닿을 수 있으며 끝없이 긴 대화를 지원하고
내부와 외부의 치명적 실패에서 살아남으며 여러 사람이 같은 에이전트를 몰 수 있는
하네스, 곧 코딩 에이전트를 포함한 모든 에이전트 응용을 만드는 프레임워크다.
`pi-ai` 같은 코드와 최소주의와 가변성이라는 원칙을 Pi와 공유하고,
여기서 배운 것이 검증되면 Pi 코딩 에이전트로 돌아간다는 것이 글의 설명이다.

계약의 경계를 먼저 적는다.
패키지 README는 대화, 모델 차례, 도구 호출,
사용자 상태가 무엇을 보여 주기 전에 저장소에 커밋되며, 프로세스가 차례 도중에
죽으면 저장소를 다시 열었을 때 멈춘 곳에서 일을 이어 간다고 약속한다.
README 맨 위에는 릴리스 사이에 API가 예고 없이 바뀐다는 “실험적” 경고가
있고(npm 1.0.0, MIT, Node 22.19 이상), 한 시점에 한 프로세스만 저장소를 소유하며
프로세스 간 잠금이 없다.
소스 전체(테스트 제외)는 약 15,000줄로 GPT 토큰으로 약 15만,
Claude 토큰으로 약 25만이며, 이는 최악의 경우이고 저장소 백엔드만 3,000줄이라
에이전트가 보통 건너뛸 수 있다고 한다.

## 동작 방식

### 하네스는 저장소와 그 위에서 대화를 돌리는 기계다

하네스는 저장소에 더해 하나 이상의 LLM 대화를 병렬로 돌리는 데 필요한 기계, 곧
모델이 부르는 도구와 도구가 도는 실행 환경을 제공하는 것이다.
대화(conversation)는 에이전트와 사용자의 상호작용을 기록한 transcript이고,
에이전트는 LLM에 사고 수준 같은 설정과 부를 수 있는 도구를 더한 것이다.
도구는 실행 환경(노트북, 원격 VM, 메모리 내 샌드박스)을 통해 일하고,
하네스가 돌리는 모든 것(모델 호출부터 도구 실행까지)은 작업(task)이다.

용어는 README가 더 정확하게 정리한다.
항목(entry)은 transcript의 불변 레코드(사용자 메시지, 모델 응답, 도구 결과,
시스템 프롬프트 변경, 리셋)이고, 커밋(commit)은 항목과 문서와 작업을 한꺼번에
쓰는 원자적 쓰기이며, 문서(document)는 transcript 옆에 저장되고 같은 커밋으로
바뀌는 타입 있는 JSON 상태다.
입력 하나가 답이 되는 과정은 `submit(input)`이 사용자 항목을 만들고,
생성 작업이 모델을 불러 `assistant` 항목을 쓰며,
도구 호출마다 도구 작업이 돌고 결과가 돌아와,
마지막 생성 작업이 답을 쓰면 제출(submission)이 끝나는 순서다.

### 모든 단계는 체크포인트를 저장하는 작업이다

크래시 복구의 핵심은 한 문장이다.
실행의 모든 단계는 작업이고 작업은 다음으로 넘어가기 전에 체크포인트를 저장한다.
프로세스가 죽으면 새 프로세스가 같은 저장소를 열어 끝나지 않은 작업을 찾고 각
작업을 마지막 체크포인트부터 이어 간다.

복구 규칙은 요소마다 다르다.
끊긴 모델 요청은 다시 보내고 부분 응답은 transcript에 중단됨으로 남는다.
끊긴 도구 호출은 안전하면(`replay: "safe"`) 다시 실행하고,
그렇지 않으면 모델에게 호출이 중단됐다고 알린다.
대기 중이던 메시지는 그대로 대기하고,
`requestId`가 같은 제출은 원래 제출을 돌려준다.

### 작업과 대화는 하나의 소유 트리를 이룬다

작업은 자식 작업을 소유할 수 있고(`ownership: { kind: "task", taskId }`), 소유한
작업이 끝나기를 기다리는 `waiting` 상태로 커밋하면 그동안 코드가 돌지 않는다.
중단은 아래에서 위로 일어나 부모를 중단하면 소유한 것부터 먼저 중단되고 각
작업이 자기 효과를 먼저 되돌린다.
하위 에이전트도 같은 패턴이어서,
하위 에이전트는 그것을 시작한 도구 호출이 소유한 대화이고
그래서 크래시에서도 살아남고 비용을 따로 세며 UI가 호출 아래에 보여 줄 수 있다.

작업은 기본이 포그라운드(현재 일의 일부)이고 Esc로 대화를
중단하면 함께 중단된다.
백그라운드 작업은 대화에 속하지만 현재 일에 속하지 않아 대화가
한가해지고 일반 중단은 이를 건드리지 않으며,
다음 날 울리는 알림이나 차례를 넘어 살아남을 하위 에이전트에 맞는다.

## 구현하기

### 가장 작은 예: 체크포인트 이후 크래시에서 이어 가는 작업

글의 약속을 모델 없이 확인할 수 있게 줄인 실험이다.
두 단계짜리 작업을 만들고 첫 프로세스에서 첫 단계의 체크포인트를 커밋한 직후
죽인 뒤, 두 번째 프로세스가 저장소를 열어 이어 가는지 본다.
Node.js 22.19 이상에서 아래 순서로 설치하고 실행한다.

```bash
npm install @earendil-works/pi-durable @earendil-works/pi-ai @earendil-works/chord
node demo.mjs first   # 체크포인트 직후 프로세스가 죽는다
node demo.mjs second  # 같은 저장소를 열어 이어 간다
```

```javascript
// demo.mjs
import fs from "node:fs";
import { BACKGROUND_CONTEXT as context } from "@earendil-works/chord/context";
import { createModels } from "@earendil-works/pi-ai/models";
import { createRegistry, defineExtension, defineTask, Harness } from "@earendil-works/pi-durable";
import { openNodeSqliteStorage } from "@earendil-works/pi-durable/storage/sqlite/node";

const mode = process.argv[2]; // "first" 또는 "second"
const log = (m) => { fs.appendFileSync("run.log", `${mode}: ${m}\n`); console.log(`${mode}: ${m}`); };

const Job = defineTask({
  name: "demo.job",
  version: 1,
  initial: () => ({ phase: "one" }),
  phases: {
    one: async (task, runtime, ctx) => {
      log("phase one runs");
      // 체크포인트: 이 커밋이 저장돼야 다음 프로세스가 phase two부터 시작한다
      await runtime.commit(() => ({ status: "running", checkpoint: { phase: "two" } }), ctx);
      if (mode === "first") { log("crashing after the checkpoint"); process.exit(1); }
    },
    two: async (task, runtime, ctx) => {
      log("phase two runs");
      await runtime.commit(() => ({ status: "terminal", outcome: { status: "completed", result: "done" } }), ctx);
    },
  },
  abort: (_t, runtime, ctx) => runtime.commit(() => ({ status: "terminal", outcome: { status: "aborted" } }), ctx),
});

const registry = createRegistry();
registry.install(defineExtension({ name: "demo", tasks: [Job] }));

const harness = await Harness.open(
  await openNodeSqliteStorage("./demo.sqlite"),
  { models: createModels(), registry },
  context,
);
const root = await harness.root(context);
if (mode === "first") {
  await root.commit((tx) => tx.createTask(Job, {}, { ownership: { kind: "conversation" } }), context);
}
harness.resume(); // 마지막 프로세스가 끝내지 못한 작업을 이어 간다
await new Promise((r) => setTimeout(r, 1500));
await harness.close(context);
```

필자가 이 스크립트를 로컬에서 실행한 결과는 다음과 같다.
첫 프로세스는 `phase one runs`를 찍고 체크포인트를 커밋한 뒤 죽었고, 두 번째
프로세스는 `phase two runs`만 찍었다.
같은 스크립트에서 죽는 위치를 체크포인트 커밋 앞으로 옮기면 두 번째 프로세스가
`phase one runs`와 `phase two runs`를 모두 찍었다.
단계 안의 코드는 체크포인트 전에 죽으면 다시 실행되므로,
단계 안의 부수 효과는 이미 일어났을 수 있다는 가정이 필요하다.

### 도구와 부수 효과는 재실행 가능 여부를 선언한다

조회처럼 다시 해도 안전한 도구는 `replay: "safe"`로 선언하고,
배포처럼 반복하면 안 되는 도구는 선언하지 않는다.
선언하지 않은 도구가 크래시로 끊기면 하네스는 호출을 반복하지 않고 모델에게
중단됐다고, 지금까지 저장된 출력과 함께 알린다.
돈이 오가는 단계는 멱등 키를 쓰는 것이 글의 예이며, 결제 작업은
`payment-${task.id}` 같은 키로 은행을 부르고 중단 처리기에서 같은 키로 환불한다.

훅(hook)이 결정을 내릴 때는 메모(memo)에 저장한다.
훅은 크래시 뒤에 다시 실행될 수 있어서,
승인 질문을 한 번 하고 그 답을 작업에 붙은 작은 값(첫 쓰기가 이기는)으로 남기면
재시작 후 같은 질문을 되풀이하지 않는다.
여러 확장이 같은 훅에 걸리면 선택된 순서대로 사슬로 실행되고,
`beforeTool`에서는 첫 차단이 사슬을 멈추며 훅이 예외를 던지면 호출이 차단된다.

### 상태, 압축, 갱신, 다중 접속

애플리케이션 상태(할 일 목록, 계획, 티켓)는 문서에 둔다.
문서는 transcript와 같은 원자적 커밋으로 바뀌므로 transcript와 어긋나지 않고,
문서마다 포크가 무엇으로 시작할지(부모의 포크 시점 값, 현재 값, 새 값)를 정한다.
압축은 대화가 계속되는 동안 백그라운드 작업으로 돌고,
요약은 다음 차례 경계에 들어가며 오래된 메시지는 저장소에 남는다.
확장을 같은 이름으로 다시 설치하면 한 번에
교체되어 이미 도는 도구 호출은 시작한 코드로 끝나고 다음 호출이 새 코드를 쓰며,
대화는 이름만 저장하므로 재시작 뒤에도 새 프로세스가 설치한 것을 쓴다.
여러 클라이언트는 현재 보기를 먼저 받고 이후에는 변화만 받으며,
누구나 실행 중인 대화를 `whenBusy: "steer"`로 몰거나 후속을 큐에 넣을 수 있다.

## 값 정하기

| 결정                    | 시작값                                           | 근거                                                                                  |
| ----------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------- |
| 저장소                  | 개발은 `MemoryStorage`, 운영은 SQLite            | 메모리는 아무것도 보존하지 않고 SQLite는 프로세스 크래시에서 커밋이 살아남는다        |
| SQLite 내구성           | 기본(WAL, `synchronous = NORMAL`)                | 전원이나 호스트 장애에서는 가장 최근 커밋을 잃을 수 있다고 README가 밝힌다            |
| JSONL fsync             | 잃으면 안 되면 `{ fsync: true }`                 | 각 커밋 표시 앞에서 디스크로 플러시한다                                               |
| 압축 `reserveTokens`    | 16384                                            | 컨텍스트 창에서 이만큼을 남긴 지점을 넘으면 다음 요청이 요약을 기다린다(글의 예시 값) |
| 압축 `backgroundTokens` | 32768                                            | 그 지점보다 이만큼 앞서 백그라운드 요약을 시작한다(글의 예시 값)                      |
| 도구 `replay`           | 읽기 전용만 `"safe"`                             | 배포, 결제, 메시지 전송은 반복하면 안 되므로 기본 비활성이 안전하다                   |
| 작업의 소유             | 현재 일이면 포그라운드, 차례를 넘으면 백그라운드 | Esc 중단이 닿는 범위를 정한다                                                         |
| 포크 문서               | 대화 상태는 `asOf`                               | 포크가 포크 시점 부모의 값으로 시작한다                                               |

압축 두 값은 글이 보여 준 예시이지 권장값이 아니다.
컨텍스트 창 크기, 평균 응답 길이,
요약에 걸리는 시간에 따라 달라지므로 자기 모델에서 측정해 정해야 한다.
측정할 것은 요약이 끝나기 전에 다음 요청이 한계를 넘어 대기하는 비율과
압축 직후 응답 품질이다.

## 트레이드오프

### 체크포인트는 재실행을 없애지 않고 줄인다

복구의 보장은 마지막 체크포인트부터다.
위 실험처럼 체크포인트 앞에서 죽으면 같은 단계가 다시 돈다.
그래서 부수 효과가 있는 단계는 단계를 잘게 나눠 체크포인트를 부수 효과 직후에
두거나, 부수 효과 자체를 멱등으로 만들어야 한다.
체크포인트를 많이 두면 복구가 정밀해지지만 커밋 비용이 늘어나고,
적게 두면 단계가 길어져 재실행의 손실이 커진다.

### 정확히 한 번은 제출 수준의 약속이다

글은 `requestId`가 제출을 정확히 한 번으로 만든다고 쓴다.
HN의 lostmsu는 ID만으로 정확히 한 번 의미론을 보장할 수 없다며 거짓 가정 위의
버그처럼 들린다고 했다.[^lostmsu]
README가 정의하는 범위는 같은 `requestId`의 재제출이 기존 제출을 돌려준다는
것으로, 이것은 중복 제출의 방지이지 도구가 외부 세계에서 일으킨 효과의
정확히 한 번이 아니다.
외부 효과는 위의 `replay` 선언과 멱등 키가 맡는다.
이 구분이 글의 문장에서는 흐려져 있다.

### 상태를 JSON 문서에 가둔 대가는 외부 저장소와의 동기화다

vmg12는 내구성 있는 애플리케이션 상태가 JSON 문서로만 제한되는 점이 아쉽고,
외부 저장소를 대화 상태와 동기화하도록 아웃박스 패턴이 통합돼 있으면
좋겠다고 했다.[^vmg12]
badlogic은 작업으로 이미 가능하다며 항목을 커밋하면서 같은 커밋에서 백그라운드
작업을 만들어 Postgres에 멱등 키로 올리는 코드를 보였다.[^badlogic-outbox]
문서 저장 API의 설계에 대해 필자들은 리듀서 방식으로 숨길 수 있느냐는 물음에
많은 것을 시도했고 어느 시점에서 복잡도가 과해졌으며(automerge 프록시 시스템의
절반까지 들어간 적이 있다) 지금의 선을 그었다고 답했다.[^the_mitsuhiko-doc]
이 API는 저장소 I/O처럼 보이지만 Immer의 draft에 더 가깝고,
JSON 패치는 워크로드의 데이터를 메모리와 성능 한도 안에서 다룰 수 없어서 다른
인코딩을 썼다고도 했다.[^badlogic-doc]

### 샌드박스는 내장하지 않고 가져다 쓴다

zmmmmm은 이런 도구가 샌드박싱을 일급 시민으로 다루지 않는 점이 아쉽다며,
에이전트가 실행되는 샌드박스를 선언적으로 정하고 신뢰할 수 없을 때 컨텍스트를
오염됨으로 표시하는 기능을 원한다고 했다.[^zmmmmm]
NitpickLawyer는 도구가 샌드박스에 무관한 편이 낫고 통합하는
사람이 고르는 것이 맞다고 했고,[^NitpickLawyer] jlkuester7은 완전히 플러그인으로
바꿀 수 있는 하네스의 샌드박스 계층을 믿기 어려워 OS 수준 샌드박스로 Pi를
감싼다고 했다.[^jlkuester7]
antonok은 Earendil의 Gondolin이 하네스 전체가 아니라 도구 호출만 일회용 최소
VM에서 실행해 폭발 반경이 완전히 격리된다고 했다.[^antonok]
실행 환경 인터페이스가 작아 원격 환경을 붙이기 쉽다는 것이 글의 접근이지만,
신뢰 경계의 책임은 통합하는 쪽에 있다.

### 대화는 트리가 아니라 포크다

lemming은 Durable이 원래 Pi의 분기하는 대화 트리를 지원하지 않고 조상 정보를
가진 포크만 지원한다며 이유를 물었다.[^lemming]
CGamesPlay는 일관성 때문일 것이라며 포크와 트리 이동은 개념상 같은 연산이고,
달라진 점은 `/resume`이 모든 대화 되감기를 보여 주고 `/tree`
구현이 어려워진 것이며 Durable은 이를 제공하지 않아 빈틈은 구현자의 몫이라고
정리했다.[^CGamesPlay]

## 함정

- 체크포인트 이전의 부수 효과를 정확히 한 번이라고 믿는다. 위 실험처럼 같은 단계가 다시 돈다.
- 모든 도구를 `replay: "safe"`로 표시한다. 반복하면 안 되는 호출(배포, 결제)은 선언하지 말고 중단 알림을 모델이 처리하게 한다.
- 훅의 결정을 저장하지 않는다. 훅은 크래시 뒤에 다시 돌 수 있어서 메모 없이 사람에게 승인을 묻는 훅은 재시작마다 같은 질문을 되풀이한다.
- 여러 프로세스가 같은 저장소를 연다. 한 시점에 한 프로세스만 저장소를 소유하고 프로세스 간 잠금이 없다.
- SQLite 기본값이 전원 장애까지 막는다고 믿는다. 가장 최근 커밋은 호스트 장애에서 잃을 수 있다.
- 실험적 API를 운영 계약처럼 쓴다. README는 릴리스 사이에 예고 없이 바뀐다고 경고한다.
- 소스를 통째로 에이전트에게 읽힌다. 전체가 약 15만에서 25만 토큰이며 저장소 백엔드 3,000줄은 대개 건너뛸 수 있다. 토큰 수 차이(GPT 대 Claude)에 놀란 ireadmevs에게 roywiggins는 토크나이저 변경이 일부 원인이라고 답했다.[^ireadmevs][^roywiggins]

## 확인하기

위 `demo.mjs`로 두 가지를 직접 확인한다.
첫째, 체크포인트 커밋 뒤에서 죽이면 `run.log`에 `phase one`이 한 번,
`phase two`가 한 번 찍힌다.
둘째, 죽는 줄을 체크포인트 커밋 앞으로 옮기면 `phase one`이 두 번 찍힌다.
다음으로 README가 가리키는 저장소의 예제로 도구 재실행과 하위
에이전트의 복구를 살펴본다.
필자는 이 노트에서 작업 단계의 체크포인트 재개만 확인했고, 모델 호출과 도구
재실행과 휴가 계획 데모는 모델 키가 필요해 직접 실행하지 못했다.

```bash
# Pi 저장소에서 두 데모를 돌리는 명령(글이 안내한 것, 필자는 실행하지 않았다)
npm install && npm run build
node packages/coding-agent/src/experimental/durable/main.ts
node packages/coding-agent/src/experimental/vacation/main.ts
```

## 체크리스트

- 부수 효과가 있는 단계가 체크포인트 직후이거나 멱등 키를 쓰는가?
- 도구마다 `replay: "safe"` 여부를 읽기 전용인지로 판단했는가?
- 사람에게 묻는 훅의 답을 메모에 저장하는가?
- 저장소를 한 프로세스만 여는가?
- 전원 장애에서 마지막 커밋 손실을 허용할 수 있는가, 아니면 JSONL `fsync`가 필요한가?
- 압축 두 값을 자기 모델의 컨텍스트 창에서 측정해 정했는가?
- 샌드박스와 신뢰 경계를 하네스 밖에서 정했는가?
- 외부 저장소와의 동기화를 백그라운드 작업과 멱등 키로 설계했는가?

## 기억할 원칙

### 내구성은 재실행을 안전하게 만드는 일이다

복구는 크래시를 없애는 것이 아니라 크래시 뒤에 같은 일이 다시 돌아도
문제가 없게 만드는 것이다.
체크포인트의 위치, 도구의 재실행 선언, 훅의 메모,
외부 호출의 멱등 키가 모두 같은 목적이다.
내구성 있는 하네스를 쓸 때 가장 먼저 물을 것은 이 단계가 두 번 돌면
무슨 일이 생기느냐다.

### 에이전트가 오래 도는 이유는 사람이 자리를 비우기 때문이다

lukebuehler는 내구성 있는 하네스를 만드는 이유를 세 가지로 요약했다.
무인으로 오래 돌리고 복구와 모니터링을 구현하기 쉽고,
하네스를 계산에서 분리하면 안전과 확장 이득이 있으며,
여러 사람이 함께하기 쉽다는 것이다.[^lukebuehler]
phainopepla2의 무한히 도는 에이전트가 무엇에 쓰이느냐는
물음에는 plaguuuuuu가 퇴근할 때까지 일이 끝나지 않았거나 노트북이 죽는 흔한
경우를 들었고,[^plaguuuuuu] rubslopes는 프로젝트를 감시하다 메시지를 보내면 같은
대화에서 처리를 요청하는 cron 작업을 들었다.[^rubslopes]
무인과 장시간이 목적이라면 크래시 복구는 부가 기능이 아니라 기본 요구다.

---

[^lostmsu]: <https://news.ycombinator.com/item?id=49929597>

[^vmg12]: <https://news.ycombinator.com/item?id=49927339>

[^badlogic-outbox]: <https://news.ycombinator.com/item?id=49927546>

[^the_mitsuhiko-doc]: <https://news.ycombinator.com/item?id=49927163>

[^badlogic-doc]: <https://news.ycombinator.com/item?id=49927329>

[^zmmmmm]: <https://news.ycombinator.com/item?id=49929069>

[^NitpickLawyer]: <https://news.ycombinator.com/item?id=49930131>

[^jlkuester7]: <https://news.ycombinator.com/item?id=49929161>

[^antonok]: <https://news.ycombinator.com/item?id=49929996>

[^lemming]: <https://news.ycombinator.com/item?id=49928702>

[^CGamesPlay]: <https://news.ycombinator.com/item?id=49929774>

[^ireadmevs]: <https://news.ycombinator.com/item?id=49927056>

[^roywiggins]: <https://news.ycombinator.com/item?id=49928273>

[^lukebuehler]: <https://news.ycombinator.com/item?id=49927001>

[^plaguuuuuu]: <https://news.ycombinator.com/item?id=49929504>

[^rubslopes]: <https://news.ycombinator.com/item?id=49928279>
