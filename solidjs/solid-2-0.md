# Solid 2.0 정식 출시

원문: [Solid 2.0 - The Long Hold](https://www.solidjs.com/blog/solid-2-0-the-long-hold/)

HN 토론: <https://news.ycombinator.com/item?id=50536387> (282점, 82개 댓글)

GN 토론: <https://news.hada.io/topic?id=37376>

## 요약

SolidJS 창시자 Ryan Carniato가 2026년 11월 16일 올린 릴리스 글이다.
프레임워크를 직접 써 보거나 마이그레이션 가이드, API 문서, 릴리스 노트는 열지 않았다.
수치와 평가는 모두 Solid 팀의 주장이다.

Solid 1.0 이후 5년 만에 2.0이 정식(stable)이 되었다는 발표이다.
글은 1.0이 내건 내기, 곧 세밀한 반응성(fine-grained reactivity)인 시그널(signal)이 UI의 올바른 토대라는 입장이 이제 Angular, Svelte의 runes, Vue Vapor, TC39 제안으로 퍼졌다고 말한다.

주요 변경은 다음과 같다.

- 비동기를 그래프 안으로: 계산이 Promise나 async iterator를 돌려주면 하위 계산이 알아서 이해한다. `<Loading>`과 `isPending`을 쓰고, 경쟁 상태(race condition)를 자동으로 다루며, 추측으로 갱신한 상태는 서버가 진실의 기준이 되도록 자동으로 되돌린다고 한다.
- 서버 함수의 코어 편입: SolidStart가 2022년 초에 소개한 서버 함수가 코어로 들어왔다. Request/Response 기반 RPC와 Server Sent Events 기반 지속 연결(`live`)을 지원한다. 반응형 Server Components는 몇 주 안에 발표한다고 예고한다.
- 에이전트를 위한 진단: 개발 빌드가 반응성 실수를 안정된 코드, 소스 위치, 해결책과 함께 보고하고 에이전트용 수리 안내 파일 경로도 내준다. 폭포수(waterfall) 요청, 잘못된 effect 루프, 넓은 팬아웃 같은 문제도 감지한다고 한다. Chrome Performance Tracks와 Sentry 플러그인에 연동되고, 컴파일을 이용하는 실험적 문법 ReactiveScript와 TSRX를 지원한다.
- 하나의 프레임워크: 메타프레임워크 SolidStart를 은퇴시켰다. 필요한 기본 요소를 코어나 프레임워크 중립 Vite 플러그인이 제공하기 때문이라고 한다. TanStack Query와 Router를 일급 수준으로 평가한다.
- 표면적 축소: `createResource`, `batch`, `startTransition`, `on`, `produce`, `createComputed`, `createMutable`을 없앴다.
- 개발 과정: 2024년 말 본격 착수, 2025년 2월 로드맵 발표, 3월 베타, 8월 릴리스 후보(API 동결)이고, 이후 14주 동안 후보 23개를 내며 풀 리퀘스트 971개를 병합하고 이슈 753개를 닫았다. 정식 기준은 일반 앱 코드에서 회귀가 없고 어디서도 충돌이나 멈춤이 없는 상태가 일주일 이어지는 것이었다고 한다.
- 후원 기관으로 Sentry, Netlify, Google Chrome, JetBrains, Anomaly, Cursor, Code Rabbit, Anthropic, Tembo 등을 든다.

글 제목의 Long Hold는 2.0의 진단 경고 이름이라고 밝힌다. `isPending`으로 보여 준 보류(hold)가 마지막 입력 뒤 충분히 오래 지속될 때 뜨는 경고이다.

## 분석

### 중심 주장은 구조적 제약이 에이전트 시대의 강점이라는 것이다

글은 반응형 프레임워크의 제약이 한때 개발 경험의 결함으로 여겨졌지만 이제 최대 강점이라고 말한다.
이유는 구성상 제약을 둔 시스템이 유지할 코드와 경우의 수가 적고,
세밀한 그래프가 무엇을 어디서 읽었고 무엇이 갱신될지 정확히 알기 때문에 실수를 조용히 넘기지 않고 보고할 수 있다는 것이다.
모델이 이 프레임워크를 많이 봤다는 것은 학습 데이터에 관한 말일 뿐이고, 중요한 질문은 에이전트가 틀렸을 때 무슨 일이 일어나느냐라고 한다.
이는 글의 서술을 이 문서가 압축한 것이다.

### 두 가지 전략이 같은 방향이다

API를 줄이는 것(이스케이프 해치 제거)과 진단을 늘리는 것(안정 코드와 수리 안내)은 모두 잘못 쓸 여지를 줄이는 쪽이다.
HN에서 한 사용자는 이 대목의 진단 기능이 사람이 직접 쓸 때도 도움이 될 것이라며 에이전트에 한정된 이야기가 아니라고 짚었고,[^wk_end]
다른 사용자는 AI와 일하며 처음으로 어른처럼 개발하게 됐다는 친구의 말을 전하며 같은 모범 사례가 에이전트에서는 어겼을 때의 대가가 더 크다고 했다.[^lemming]
Rust가 에이전트와 잘 맞는 이유도 좋은 오류 메시지와 엄격한 타입이라는 의견이 나왔다.[^novacrazy]
이 해석은 글이 아니라 댓글의 것이다.

### 프레임워크 자체가 필요한가를 묻는 질문이 따라붙었다

한 사용자는 에이전트용으로 만들었다는 말이 프레임워크를 버리는 쪽을 뜻해야 한다고 했다.
프레임워크는 큰 팀의 지식 격차를 메우는 추상화였는데 이제 그 일을 에이전트가 하기 때문이라는 논리이다.[^ale]
이에 대해 LLM이 반응형 프레임워크를 쓸 때 직접 짠 JS보다 더 유지보수하기 좋은 코드를 낸다는 반박이 달렸다.[^rafram]
필자는 ReactiveScript를 만들고 있다고 답했다.
Solid의 제약을 컴파일되는 언어로 옮겨, 비동기 버그를 컴파일 오류로 만들고 에이전트가 나쁜 코드를 쓸 수 없게 한다는 Rust식 접근이다.
아직 진행 중이지만 초기 결과가 유망하다고 했다.[^ryansolid_rs]

## 비평

### 가장 눈에 띄는 비용 서술이 빠져 있다

HN에서 한 사용자가 간단한 카운터 컴포넌트 번들을 재 보니 Solid 1.9.18에서는 4.8 KiB(brotli), 2.0.0에서는 20.3 KiB로 크게 늘었다고 했다.[^altano]
글은 표면적이 줄었다고 말하지만 번들 크기는 언급하지 않는다.
다만 글이 낸 장점(적은 API)과 번들 크기의 변화는 같은 주장이 아니므로 따로 확인해야 한다.

### 마이그레이션 비용과 생태계 준비도

에이전트 시대에 적은 표면적이 이점이라는 주장은 기존 앱의 마이그레이션 비용을 말해 주지 않는다.
제거된 API가 일곱 개이고, 한 사용자는 RC 단계에서 1.0에서 2.0으로 옮긴 경험을 글로 남겼다.[^flamewolf]
생태계는 TanStack Query, Router, Start가 2.0 사전 배포 브랜치로 지금 설치할 수 있고 다른 라이브러리는 열린 풀 리퀘스트 상태라고 필자가 답했다.[^ryansolid_lib]
한 사용자는 TanStack의 Solid 2 어댑터가 나오면 걸림돌이 없어진다고 했다.[^prajaybasu]
컴포넌트 라이브러리가 많지 않다는 지적에는 Kobalte, Ark UI 등이 있다는 반박이 있었다.[^maxloh][^pwmglenn]

### 문서의 품질과 설명의 불투명성에 대한 지적

HN에서 한 사용자는 릴리스 글에 없는 `broadcast`를 문서에서 찾아보니 이해하기 어려운 문장이 이어졌다고 했다.[^ricardobeat]
이 반응은 서버 함수의 새 기능이 설명보다 먼저 발표된다는 인상을 준다.

### 진단 기능의 효과는 사례가 없다

글은 에이전트가 틀렸을 때 프레임워크가 알려 준다고 주장하지만 실제 에이전트의 오류가 진단으로 얼마나 줄었는지는 보이지 않는다.
후보 기간 동안 에이전트가 스케줄러의 구석을 일부러 파헤쳐 버그를 찾아냈다는 서술이 있을 뿐이다.
진단이 에이전트의 수정 성공률을 높인다는 측정은 글에 없다.

### 외부 반응

HN 스레드는 282점 82개 댓글이다.
한 사용자는 Svelte를 골랐다가 올해 Solid로 옮겼다고 했다. TS/TSX를 별도 도구 없이 쓰고 싶었다는 이유이다.[^pier25]
다른 사용자는 더 이상 프레임워크 논쟁을 하지 않게 됐다며 어셈블리 명령어를 따지는 것과 같다고 했는데,[^bottlepalm] 이는 개인의 관점이다.
한 사용자는 Solid 2의 범용 렌더러로 watchOS 네이티브 UI를 만들어 저장소를 공개했다고 전했고,[^extremeracer] 범용 렌더러가 React와의 차별점이었다는 반응이 이어졌다.[^dalmo3]
Lobste.rs에서는 `solidjs.com` 도메인이 올라온 적이 없다.
GeekNews에는 같은 글의 토픽이 있으나 댓글이 하나이고, 그것도 HN 댓글을 다시 모은 GN⁺ 계정의 요약이라 GeekNews 이용자의 반응은 없다.

## 인사이트

### 가져갈 것은 에이전트 시대의 프레임워크 평가 기준이 오류 보고의 질이라는 관찰이다

모델이 이 프레임워크를 얼마나 봤는지보다, 잘못 썼을 때 안정된 코드와 위치와 해결책을 돌려주는지가 기준이 된다는 주장은 프레임워크 선택 말고도 쓸 수 있다.
자기 팀의 라이브러리나 내부 도구에도 오류 메시지가 에이전트가 고칠 수 있는 형태인지를 점검할 수 있다. 이는 이 문서의 적용이다.

### 업그레이드 전에 번들 크기와 의존 라이브러리의 준비도를 잰다

글의 장점은 표면적과 기능이지만 HN에서 나온 번들 크기 증가 보고와 라이브러리 준비 상황이 실제 도입의 변수이다.
자기 앱의 대표 화면으로 1.x와 2.0의 번들 크기를 재고, 쓰는 라이브러리의 2.0 지원 상태를 확인한 뒤 옮기는 순서가 안전하다.

### 확인할 관찰

이 글의 주장을 가를 관찰은 세 가지이다.
독립적으로 잰 번들 크기와 런타임 성능이 1.x 대비 어떤지,
에이전트가 만든 Solid 2.0 코드에서 진단 기능이 실제로 오류를 줄이는지,
ReactiveScript와 반응형 Server Components가 약속대로 나오는지이다.

---

[^wk_end]: <https://news.ycombinator.com/item?id=50537697>

[^lemming]: <https://news.ycombinator.com/item?id=50538644>

[^novacrazy]: <https://news.ycombinator.com/item?id=50538149>

[^ale]: <https://news.ycombinator.com/item?id=50536923>

[^rafram]: <https://news.ycombinator.com/item?id=50537093>

[^ryansolid_rs]: <https://news.ycombinator.com/item?id=50538206>

[^altano]: <https://news.ycombinator.com/item?id=50542354>

[^flamewolf]: <https://news.ycombinator.com/item?id=50541816>

[^ryansolid_lib]: <https://news.ycombinator.com/item?id=50539832>

[^prajaybasu]: <https://news.ycombinator.com/item?id=50538561>

[^maxloh]: <https://news.ycombinator.com/item?id=50536877>

[^pwmglenn]: <https://news.ycombinator.com/item?id=50537180>

[^ricardobeat]: <https://news.ycombinator.com/item?id=50539250>

[^pier25]: <https://news.ycombinator.com/item?id=50537344>

[^bottlepalm]: <https://news.ycombinator.com/item?id=50537913>

[^extremeracer]: <https://news.ycombinator.com/item?id=50540684>

[^dalmo3]: <https://news.ycombinator.com/item?id=50541284>
