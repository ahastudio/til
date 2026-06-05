# Angular v22 발표

원문: <https://blog.angular.dev/announcing-angular-v22-c52bb83a4664>

HN 토론: <https://news.ycombinator.com/item?id=48386463> (132점, 79개 댓글)

## 요약

Angular v22는 Signal Forms, Angular Aria, 비동기 반응성 API 안정화와 함께 AI 에이전트 통합, 라우터 개선, 핵심 API 개선을 포함한다.
공식 릴리스는 2026년 6월 5일이다.

Signal Forms가 프로덕션 준비 완료 상태에 진입했다.
반응형 폼(Reactive Forms)의 타입 안전성, 템플릿 기반 폼(template-driven forms)의 선언적 편의성, 시그널(signals)의 반응성을 결합했다.
Angular Material과 Angular Aria를 완전 지원한다.

Angular Aria는 웹 접근성 패턴 12가지를 지원하는 안정적인 UI 지시문 세트다.
Signal Forms와 완전 통합되며 테스트 하네스도 제공된다.

`resource`와 `httpResource` API가 안정화됐다.
비동기 시그널 처리를 선언적으로 다룰 수 있게 해주며,
HTTP 데이터 패칭에 직관적인 멘탈 모델을 제공한다.

AI 에이전트 통합이 강화됐다.
Model Context Protocol(MCP) 서버가 안정화되어 개발 서버 제어, 빌드 결과 모니터링, 자가 치유 루프가 가능해졌다.
Angular Agent Skills는 Angular 개발의 모범 사례를 AI 에이전트에게 제공하는 지침 묶음이다.
Google AI Studio와 Gemini Canvas에서 직접 Angular 앱을 생성하고 브라우저에서 개발할 수 있다.

라우터와 핵심 API도 개선됐다.
Navigation API 통합으로 네이티브 브라우저 스크롤 동작을 활용하고,
`@Service` 데코레이터로 `@Injectable({ providedIn: 'root' })` 대체가 가능해졌다.
`injectAsync`로 비동기 의존성 주입과 서비스 코드 분할이 가능하다.
TypeScript 6를 완전 지원한다.

OnPush 변경 감지(change detection) 전략이 새 앱의 기본값으로 변경됐다.
Webpack 지원이 중단되며 TSGo 기반 앱 빌더로 전환된다.
`@boundary` 에러 처리가 Q3 2026 개발자 미리보기로 예고됐다.

## 분석

### Signal 기반 API로의 전환 완성

Angular는 v16에서 시그널을 실험적 기능으로 도입했고, v22에서 Signal Forms가 안정화됐다.
이것은 3년에 걸친 반응성 모델 전환의 완성에 가깝다.

Zone.js 기반의 변경 감지는 “무엇이 변했는지 알 수 없으니 전체를 확인한다”는 암묵적 계약이었다.
시그널은 “이 값이 변하면 이 컴포넌트만 업데이트한다”는 명시적 반응성이다.
OnPush가 기본값이 된 것은 이 전환의 논리적 귀결이다.
시그널을 쓰는 코드에서 Zone.js 기반 전체 트리 재검사는 불필요하다.

Signal Forms는 이 전환의 핵심 테스트였다.
폼 상태는 복잡하다 — 유효성 검사, 비동기 검사, 중첩 컨트롤, 배열 필드가 얽혀 있다.
이 복잡성을 시그널로 모델링하는 것이 가능하다는 것을 v22가 증명했다.

HN에서 "Signal Forms와 resource API가 실험적 단계였을 때부터 기다려왔다.
시그널 방식으로 넘어간 뒤로는 돌아갈 수가 없고, 폼에서 RxJS를 써야 했던 것이 큰 고통이었다"는 반응이 있었다.[^majora2007]
RxJS 의존성이 Signal Forms 도입의 가장 강력한 동기 중 하나였음을 실무 개발자의 목소리가 확인해준다.

### AI 에이전트 통합의 방향

Angular v22가 MCP, Agent Skills, WebMCP, AI 플랫폼 통합을 한 번에 포함시킨 것은
Angular 팀의 전략적 결정을 드러낸다.

프레임워크가 AI 에이전트의 “이해 대상”이 되어야 한다는 것이다.
`angular-developer` 스킬은 AI가 구식 패턴 대신 Signal Forms, OnPush 같은 현대적 API를 사용하도록 안내한다.
이것은 문서화의 새로운 형태다.
개발자를 위한 마크다운 문서 대신, AI 에이전트를 위한 구조화된 컨텍스트다.

[GeekNews 댓글](https://news.hada.io/topic?id=30162)에서 “요즘 Angular는 쓰기 즐거운 수준이라는 걸 인정하게 됨”이라는 반응이 있었다.
Signal Forms와 시그널 덕분에 상태 관리가 크게 개선되었다는 평가도 나왔다.
과거 Angular의 복잡성에 대한 피로감이 v22에서 해소되고 있다는 신호다.

### `@Service` 데코레이터의 의미

`@Injectable({ providedIn: 'root' })` 대신 `@Service()`로 쓸 수 있게 된 것은 작은 변화지만 방향을 보여준다.
Angular는 명시성(explicitness)을 중시하는 프레임워크였다.
모든 설정이 드러나야 한다는 철학이 초기의 복잡한 설정 코드를 낳았다.

이 변화는 “명시적이되 장황하지 않아야 한다”는 방향으로의 이동이다.
의도는 명확하지만 구현 세부 사항은 숨기는 것이다.
React의 Hooks가 클래스 컴포넌트의 장황함을 줄인 것과 같은 방향이다.

## 비평

### 강점: 일관된 진화 방향

v22의 변화들은 단편적이지 않다.
시그널로의 전환, AI 통합 강화, 의존성 주입 단순화, 템플릿 표현력 향상이 모두 “더 현대적이고 더 간결한 Angular”라는 방향으로 수렴한다.
3년 전의 Angular와 비교하면 같은 프레임워크라고 부르기 어려울 정도의 변화다.

### 약점: 마이그레이션 부담 명시 부족

새 앱의 기본값 변경(OnPush), Webpack 중단, API 이름 변경은 기존 코드베이스에 영향을 준다.
릴리스 노트는 새 기능에 집중하고 마이그레이션 부담을 충분히 다루지 않는다.
수백만 줄의 기존 Angular 코드를 운영하는 팀에게 “쓰기 즐거운 Angular”는 마이그레이션 후의 이야기다.

### 보완할 시각: 번들 크기와 성능

Signal 기반 변경 감지와 OnPush 기본값이 실제 앱 성능에 미치는 영향을 수치로 제시하지 않는다.
“번들 크기 영향 없음”이라는 언급이 Navigation API에만 있고 전체적인 성능 이야기가 빠져 있다.
Angular의 오랜 약점이 번들 크기였던 만큼, v22에서의 변화가 이 문제를 어떻게 다루는지가 중요하다.

## 인사이트

### 프레임워크가 AI 에이전트를 위한 인터페이스를 만든다

Angular v22에서 Agent Skills와 MCP 통합이 핵심 기능으로 포함된 것은 프레임워크 설계의 새로운 레이어를 보여준다.

전통적으로 프레임워크는 두 가지 인터페이스를 설계했다.
개발자 경험(DX) — 코드를 얼마나 쉽게 쓸 수 있는가.
런타임 성능 — 사용자에게 얼마나 빠르게 동작하는가.

AI 에이전트 시대에 세 번째 인터페이스가 추가된다.
AI 이해 가능성(AI comprehensibility) — AI 에이전트가 이 프레임워크의 코드를 얼마나 잘 생성하고 수정할 수 있는가.

`angular-developer` 스킬은 이 세 번째 인터페이스의 첫 번째 구현이다.
AI가 Angular 코드를 생성할 때 구식 패턴을 쓰지 않도록 하는 구조화된 컨텍스트다.
이 인터페이스를 잘 만든 프레임워크가 AI 에이전트 개발 시대의 승자가 될 수 있다.

HN의 한 댓글은 이 변화를 다른 각도에서 정확히 포착했다.
"이제 싸움은 어느 프레임워크가 기술적으로 더 좋은가가 아니라 에이전트가 어느 프레임워크에 더 능숙한가의 문제가 됐다"는 시각은[^hmokiguess] Angular Agent Skills가 겨냥하는 경쟁의 본질을 직접 가리킨다.

### 시그널로의 전환이 프레임워크 선택을 바꾸는 방식

React의 훅(Hooks), Vue의 Composition API, Solid의 시그널, Angular의 시그널.
주요 프론트엔드 프레임워크들이 선언적 반응성 모델로 수렴하고 있다.

이 수렴이 역설적인 결과를 만든다.
프레임워크 간 차이가 줄어들수록, 선택의 기준이 기술 특성에서 생태계와 조직 맥락으로 이동한다.
“어느 것이 기술적으로 더 좋은가”보다 “어느 것을 우리 팀이 잘 쓸 수 있는가”가 중요해진다.

Angular가 “Django처럼 필요한 게 다 포함돼 있는 프레임워크”라는 인식은 이 맥락에서 강점이다.[^TheChaplain]
라우팅, 폼, HTTP 클라이언트, 의존성 주입, 접근성 프리미티브까지 내장된 것은
선택의 복잡성을 줄이고 팀의 일관성을 유지하게 해준다.

Signal Forms의 안정화는 이 포지션을 강화한다.
React는 서드파티 폼 라이브러리(React Hook Form, Formik)가 표준화된 반면,
Angular는 프레임워크 내장 솔루션으로 수렴한다.
규모 있는 조직에서 이 차이는 작지 않다.

---

[^majora2007]: <https://news.ycombinator.com/item?id=48388888>
[^hmokiguess]: <https://news.ycombinator.com/item?id=48391194>
[^TheChaplain]: <https://news.ycombinator.com/item?id=48387462>
