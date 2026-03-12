# Page Agent

- 원문: <https://github.com/alibaba/page-agent>
- 사이트: <https://alibaba.github.io/page-agent/>

## 요약

웹페이지 안에서 동작하는 GUI 자동화 에이전트다.
브라우저 확장, Python, 헤드리스 브라우저 없이
순수 클라이언트 사이드 JavaScript만으로 DOM을 제어한다.

스크린샷 기반 멀티모달 접근 대신 텍스트 기반 DOM 파싱을
사용하므로, 일반 텍스트 LLM만으로도 동작한다.

자연어 명령 하나로 클릭, 입력, 스크롤 등 웹 인터랙션을
수행한다.

## 아키텍처

```
사용자 명령 → PageAgentCore (ReAct 루프)
                ├── LLM (OpenAI 호환 API)
                ├── PageController (DOM 추출/액션)
                │   ├── dom/ (트리 구축, 인덱싱)
                │   ├── mask/ (시각적 오버레이)
                │   └── actions (클릭, 입력, 스크롤)
                └── UI (Human-in-the-loop 피드백)
```

모노레포 7개 패키지로 구성된다:

| 패키지            | 역할                          |
|-------------------|-------------------------------|
| core              | ReAct 루프, 프롬프트, 도구    |
| page-controller   | DOM 추출, 인덱싱, 액션 실행   |
| llms              | OpenAI 호환 LLM 클라이언트    |
| ui                | 사용자 인터페이스 컴포넌트    |
| extension         | Chrome 확장 (멀티탭 지원)     |
| page-agent        | 통합 패키지 (npm 배포)        |
| website           | 문서 사이트                   |

## 핵심 메커니즘

### ReAct 루프

`PageAgentCore`는 최대 40스텝의 ReAct 루프를 실행한다.

```
while (스텝 < 40 && !done) {
  1. Observe: DOM 상태 + 페이지 URL + 뷰포트 정보 수집
  2. Think: LLM에 시스템 프롬프트 + 히스토리 + 현재 상태 전달
  3. Act: LLM이 선택한 도구(MacroTool) 실행
  4. 결과를 히스토리에 누적
}
```

LLM은 매 스텝마다 반드시 하나의 MacroTool을 호출해야 한다.
MacroTool에는 reflection 필드(평가, 메모리, 다음 목표)와
액션 선택이 포함된다.

잔여 스텝이 5, 2일 때 경고를 발생시켜 LLM이 작업을
수렴하도록 유도한다.

### DOM 텍스트 변환

`PageController`가 DOM을 평탄화(flat tree)한 뒤,
인터랙티브 요소에 `[0]`, `[1]` 같은 숫자 인덱스를 부여한다.

```html
<div>
  <h1>로그인</h1>
  [0] <input placeholder="이메일" />
  [1] <input type="password" placeholder="비밀번호" />
  [2] <button>로그인</button>
</div>
```

이 텍스트 표현이 LLM 컨텍스트로 전달된다.
`aria-label`, `role`, `title` 등 시맨틱 속성만 선별 포함하고,
중복 속성값은 필터링한다.

`selectorMap`으로 인덱스 → DOM 엘리먼트 매핑을 유지하므로,
LLM이 인덱스만 지정하면 실제 엘리먼트를 정확히 조작한다.

### 도구 목록

| 도구                       | 기능                          |
|----------------------------|-------------------------------|
| `click_element_by_index`   | 인덱스로 요소 클릭           |
| `input_text`               | 입력 필드에 텍스트 입력      |
| `select_dropdown_option`   | 드롭다운 옵션 선택           |
| `scroll`                   | 수직 스크롤                  |
| `scroll_horizontally`      | 수평 스크롤                  |
| `execute_javascript`       | 임의 JS 실행                 |
| `wait`                     | 지정 시간 대기               |
| `done`                     | 작업 완료 선언               |
| `ask_user`                 | 사용자에게 질문              |

## 설치 및 사용

```bash
npm install page-agent
```

```javascript
import { PageAgent } from 'page-agent'

const agent = new PageAgent({
  model: 'qwen3.5-plus',
  baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
  apiKey: 'YOUR_API_KEY',
  language: 'ko-KR',
})

await agent.execute('로그인 버튼을 클릭하세요')
```

CDN으로 즉시 테스트도 가능하다:

```html
<script src="https://cdn.jsdelivr.net/npm/page-agent@1.5.6/dist/iife/page-agent.demo.js"></script>
```

## 활용 사례 추정

### 1) SaaS 제품에 AI 코파일럿 탑재

기존 웹 앱의 백엔드를 건드리지 않고,
프론트엔드에 `page-agent`를 삽입하는 것만으로
자연어 기반 조작 기능을 추가할 수 있다.

ERP, CRM처럼 폼이 복잡하고 워크플로우가 긴 시스템에서
"신규 고객 등록하고 3개월 무료 플랜 적용해줘" 같은
명령 한 줄이 수십 번의 클릭을 대체한다.

### 2) 레거시 시스템 자연어 래퍼

API가 없거나 빈약한 내부 시스템에 대해,
UI 자동화 계층을 씌워 자연어 인터페이스로 전환한다.
RPA보다 가볍고, 배포가 스크립트 주입 하나로 끝난다.

### 3) 접근성(Accessibility) 즉시 강화

스크린 리더나 음성 명령으로 조작하기 어려운 웹 앱에
page-agent를 올리면, 자연어가 곧 접근성 레이어가 된다.
별도 접근성 개선 작업 없이 즉시 효과를 볼 수 있다.

### 4) QA 테스트 자동화

테스트 시나리오를 자연어로 작성하고
page-agent가 실제 DOM에서 실행한다.
셀렉터 기반 E2E 테스트와 달리 UI 변경에 덜 취약하다.

### 5) 사용자 온보딩 가이드

"프로필 사진을 변경하세요"라는 안내를 텍스트 대신
에이전트가 직접 시연하거나 사용자를 단계별로 이끈다.
인터랙티브 튜토리얼의 구현 비용이 극적으로 줄어든다.

## 인사이트

### 1) 스크린샷 없는 GUI 에이전트가 실용적 선택이다

GPT-4o, Claude 같은 멀티모달 LLM에 스크린샷을 보내는
방식은 직관적이지만 비용과 지연이 크다.
1장의 스크린샷이 수천 토큰을 소비하고,
매 스텝마다 캡처-전송-분석 오버헤드가 누적된다.

Page Agent는 DOM을 텍스트로 변환해 일반 LLM으로
충분히 동작하게 만든다.
이것은 browser-use에서 검증된 접근이고,
Page Agent는 이를 클라이언트 사이드에 이식했다.

"보는 것"이 아니라 "읽는 것"으로 웹을 이해하는 방식이,
현재 시점에서는 비용 대비 효과가 더 높다.

### 2) 클라이언트 사이드 실행은 인프라 부담을 제거한다

Playwright, Puppeteer, Selenium 기반 자동화는
서버에서 브라우저를 띄워야 한다.
인프라 비용, 세션 관리, 스케일링이 뒤따른다.

Page Agent는 사용자의 브라우저 안에서 직접 실행되므로
서버가 필요 없다. LLM API 호출만 외부 의존이다.

이것은 배포 모델의 근본적 차이다.
npm 패키지 하나 또는 CDN 스크립트 한 줄이면 끝이다.

### 3) MacroTool 패턴이 에이전트 루프의 구조적 문제를 해결한다

LLM에게 여러 도구를 자유롭게 호출하게 하면,
도구 선택의 순서와 조합이 폭발적으로 늘어난다.

Page Agent는 모든 도구를 하나의 MacroTool로 감싸고,
매 스텝마다 반드시 reflection(평가 + 메모리 + 목표)과
함께 정확히 하나의 액션을 선택하게 강제한다.

이 제약이 LLM의 추론을 구조화한다.
자유도를 줄여서 정확도를 올리는 전략이다.

### 4) Human-in-the-loop이 프로덕션 배포의 전제 조건이다

`ask_user` 도구와 시각적 UI 피드백은 단순한 부가 기능이
아니다. GUI 자동화 에이전트가 실수하면 실제 데이터가
변경된다.

Page Agent가 매 액션을 시각적으로 보여주고,
불확실할 때 사용자에게 물어보는 설계는,
"자동화의 정확성"과 "실수의 비가역성" 사이의 균형점이다.

프로덕션에서 GUI 에이전트를 쓰려면
이 균형이 반드시 필요하다.

### 5) 인덱스 기반 요소 참조는 LLM에 최적화된 추상화다

CSS 셀렉터(`div.form > button:nth-child(3)`)는
LLM이 생성하기 어렵고 DOM 변경에 취약하다.
XPath는 더 복잡하다.

`[0]`, `[1]` 같은 정수 인덱스는 LLM이 실수할 여지가
거의 없다. 목록에서 번호를 고르는 것은 언어 모델이
가장 잘하는 작업 중 하나다.

agent-browser의 `@e1` 참조와 같은 맥락이지만,
Page Agent는 이를 DOM 텍스트 표현 안에 인라인으로
삽입해서 별도 매핑 단계 없이 시각적으로 명확하게 만든다.

### 6) browser-use의 클라이언트 사이드 포크가 새로운 카테고리를 만든다

Page Agent는 browser-use에서 DOM 처리와 프롬프트를
가져왔다고 명시한다. 하지만 실행 환경이 완전히 다르다.

browser-use: 서버 → 헤드리스 브라우저 → 웹 페이지
Page Agent: 웹 페이지 내부 → 같은 DOM 직접 조작

같은 알고리즘이 다른 실행 컨텍스트에 놓이면서,
"외부에서 조종하는 자동화"가 아니라
"내부에서 보조하는 코파일럿"이 된다.

이것은 단순한 포팅이 아니라 제품 카테고리의 전환이다.

## 관련 문서

- [agent-browser](agent-browser.md) - Vercel의 에이전트 브라우저 CLI.
  서버 사이드 Playwright 기반으로, Page Agent와 정반대 배포 모델.
