# Modern Web Guidance: 코딩 에이전트를 2019년식 JavaScript에서 웹 표준 기능으로 돌려놓는 스킬 모음

<https://developer.chrome.com/docs/modern-web-guidance>

<https://github.com/GoogleChrome/modern-web-guidance>

Show HN: [Get your coding agent off ~2019 JavaScript, onto modern web primitives](https://news.ycombinator.com/item?id=50443812) (420점, 139개 댓글)

GN 토론: <https://news.hada.io/topic?id=36964>

## 소개

Modern Web Guidance는 웹 플랫폼의 전문 지식, 모범 사례, 브라우저 호환성 데이터를
코딩 에이전트에 직접 넣어 주는 스킬 모음이다.
README는 에이전트가 학습 데이터에 많은 레거시 코드 탓에 오래된 패턴을 기본으로
선택하고, 지금은 브라우저가 기본 제공하는 기능으로 할 일을 부풀린 JavaScript로
작성한다고 문제를 진단한다.
모델이 어떤 API가 있다는 것을 알아도, 실무에 맞는 현대적 구현 패턴의 밀도가
부족하다는 것이다.
Google Chrome, Microsoft Edge, Mozilla Firefox, MDN 팀이 웹 개발 커뮤니티와 함께
관리한다고 밝힌다.

GitHub API로 확인한 2026년 11월 11일 기준 별은 4,672개, 포크는 150개이고
저장소는 2026년 3월 23일에 만들어졌다.
코드는 Apache-2.0, `guides/` 아래 문서 내용은 CC-BY 4.0 라이선스다.
소스 저장소는 별도의 `modern-web-guidance-src`다.

### 사용 방법

`npx modern-web-guidance@latest install`이 대화형 설치 마법사를 실행한다.
설치 없이도 CLI를 쓸 수 있다.

```shell
npx modern-web-guidance@latest search "animate a dialog modal backdrop"
npx modern-web-guidance@latest retrieve "animate-to-from-top-layer"
npx modern-web-guidance@latest legacy-scan .
```

`search`는 관련 가이드를 찾고, `retrieve`는 ID로 가이드를 가져오며,
`legacy-scan`은 코드베이스에서 레거시 패턴을 찾는다.
스킬 팩은 `modern-web-guidance`와 `chrome-extensions` 두 가지이고, README는
각각의 토큰 규모를 약 205개와 약 175개로 적는다.

### 담긴 내용

가이드는 최근 몇 년간의 웹 플랫폼 새 기능부터 최신 기능까지 다루며, 토큰 효율을
위해 설계되었다고 한다.
모델이 이미 아는 평범한 내용은 평가를 거쳐 걷어 낸다.
README의 접이식 목록은 250개의 웹 기능과 203개의 실제 개발자 사용 사례를 든다.

| 분야         | 예                                                                 |
| ------------ | ------------------------------------------------------------------ |
| 사용자 경험  | View Transitions, 진입·퇴장 애니메이션, 시차 스크롤                |
| CSS 레이아웃 | 컨테이너 쿼리, `subgrid`, `oklch` 같은 색 공간, 텍스트 줄바꿈 조절 |
| 성능         | 즉시 사전 로딩, INP 진단, `scheduler.yield`                        |
| 폼과 UI      | Anchor Positioning, Popover API, `:user-invalid` 검증              |
| 접근성       | 스크린 리더와 키보드 조작성                                        |
| 내장 AI      | 번역, 요약, 언어 감지 같은 로컬 모델 API                           |

### 평가

README는 가이드가 효과가 있다는 근거로 평가 체계를 내세운다.
전문가가 쓴 가이드와 데모에서 실제 웹 앱 위의 과제, 정답 풀이, Playwright
채점기를 만들고, 채점기가 정답 풀이에는 100% 통과하고 수정하지 않은 기본 앱에는
100% 실패하도록 보정한다.
이어 코딩 에이전트를 가이드 있는 모드와 없는 모드로 돌려 통과율을 비교한다.
“여지”(100%에서 가이드 없는 통과율을 뺀 값)와 “상승분”(가이드 있는 통과율에서
없는 통과율을 뺀 값)이 핵심 지표이고, 모델이 이미 잘하는 곳의 조언은 줄이는 데
쓴다.
11월 8일 최근 결과는 다음과 같다.

| 에이전트(모델)                   | 과제/검증 수 | 가이드 없음 → 있음 |
| -------------------------------- | ------------ | ------------------ |
| antigravity_cli (gemini-4-argon) | 214 / 1673   | 58% → 94% (+36pp)  |
| codex_cli (gpt-6.1-sol)          | 215 / 1795   | 54% → 82% (+28pp)  |
| claude_code (opus-5-5)           | 215 / 1801   | 57% → 88% (+31pp)  |

개발자 프롬프트는 API 이름을 말하지 않고(예: “이미지 로딩을 빠르게”) 에이전트가
가이드를 스스로 찾아 쓰는지 본다.
README는 개인 프롬프트는 수집하지 않지만 설치 수, 호출한 에이전트 이름, 가이드
조회 ID, 에이전트가 만든 검색어를 익명으로 수집한다고 밝히며
`DISABLE_TELEMETRY=1`로 끌 수 있다고 안내한다.

저장소가 홈페이지로 등록한 주소는 developer.chrome.com이다.
2026년 11월 26일에 사이트 첫 화면을 열어 본문을 끝까지 읽었다.
사이트의 설명은 제작자의 주장이다.
아래 소절은 그 첫 화면이 싣는 내용 가운데 위 README와 겹치지 않는 부분이다.

### 공식 사이트가 내세우는 것

첫 화면은 설치 경로를 네 가지로 안내한다.
권장 경로는 `npx modern-web-guidance@latest install`이고,
Vercel의 Agent Skills(`npx skills add`), Claude Code와 Copilot CLI의
플러그인 마켓플레이스, Antigravity CLI(`agy plugin install`)가 이어진다.

| 설치 경로       | 사이트가 적은 명령                                        |
| --------------- | --------------------------------------------------------- |
| npx skills      | `npx skills add GoogleChrome/modern-web-guidance`         |
| Claude Code     | `claude plugin marketplace add`와 `claude plugin install` |
| Copilot CLI     | `/plugin marketplace add`와 `/plugin install`             |
| Antigravity CLI | `agy plugin install <저장소 주소>`                        |

사이트는 가이드가 200개 넘는 전문가 검수 스킬이고,
Chrome 전문가가 CSS, Web UI, HTML, JavaScript, Core Web Vitals, 접근성, 보안,
Web AI에 걸쳐 썼다고 소개한다.
공개 평가 대시보드 항목에는 가이드 없는 최신 모델이 약 51%, 가이드가 있으면
91%를 통과한다고 적혀 있다.
같은 목록에 Baseline 데이터와 프로젝트의 브라우저 목표로
점진적 향상, `@supports` 질의, 폴리필을 자동 생성한다는 항목,
로컬 벡터 검색 인덱스를 다룬 글,
개발자가 만들면서 현대 HTML, CSS, Web API를 배우게 하는 학습 모드 글이 있다.

Chrome DevTools for agents와 묶어 “만들고 검증하는 고리”를 닫는다는 점도
앞세운다.
에이전트가 실시간 Lighthouse 감사, 사용자 흐름 재현, 메모리 누수 분석,
살아 있는 브라우저 세션 디버깅을 하게 하고 그 뒤에 현대 웹 수정을 적용한다는
설명이다.

사이트는 실무 사례 카드도 네 건 싣는다.
카드에 적힌 문장만 읽었고, 각 사례의 본문은 열어 보지 않았다.

| 조직                         | 카드가 적은 내용                                                                                     |
| ---------------------------- | ---------------------------------------------------------------------------------------------------- |
| Policybazaar와 Pensionbazaar | 새 페이지 처리 기간과 UI 버그를 90% 넘게 줄이고, 수동 Core Web Vitals 감사 노력을 92% 줄임           |
| MetaMask                     | 세 줄짜리 조언형 PR 리뷰 봇을 약 480개 PR에 돌려 접근성과 시맨틱 HTML 수정 43건, 중간 처리 시간 15분 |
| WeTV                         | CI/CD에 넣어 반복되는 CLS 회귀의 90%를 자동 진단하고 수정                                            |
| note inc.                    | 자사 디자인 시스템 규칙과 함께 써서 현대 웹 준수율 61%에서 94%, LCP 우선순위 28% 향상                |

사이트는 그 밖에 시작용 프롬프트 예(아코디언 애니메이션, CSS Anchor Positioning
탭 막대, 컨테이너 쿼리 카드, `<dialog>`와 Popover API로의 이전, passkey 로그인,
CSP 초안, 호버 사전 로딩, INP와 LCP 개선), 입문 코드랩,
기여 안내, Google Chat이 DevTools for agents로 메모리 누수 30여 건을 고쳤다는
글도 연결한다.

## 분석

### 핵심 접근은 학습 데이터의 시차를 검색 가능한 지침으로 메우는 것이다

문제의 원인은 모델의 능력이 아니라 학습 데이터에 있는 레거시 코드의 비중이라고
README는 본다.
해법은 모델을 다시 학습하지 않고, 작업 시점에 CLI가 가이드를 에이전트의
컨텍스트로 넣어 주는 것이다.
HN에서 paulirish는 유지보수성이 다음 과제라고 하며, 에이전트가 1천 줄짜리 해법을
계속 쌓으면 코드베이스가 이해 가능한 범위를 빠르게 벗어나므로 `ResizeObserver`와
`setTimeout`을 쓰는 60줄 대신 CSS 한 줄을 택하겠다고 말했다.[^paulirish-1]
halflife는 현대 기능 두 줄로 바꿀 수 있는 코드가 뒤섞인 풀 리퀘스트를 많이
리뷰해 직접 비슷한 도구를 반쯤 만들었다고 썼다.[^halflife]
두 사례는 같은 문제의식이다.
에이전트가 만든 코드의 양을 줄이는 것이 이 도구의 가치다.

### 배포 방식에 대한 제안이 도구의 정체를 드러낸다

simonw는 npm 패키지 외에 GitHub Pages로 스킬의 마크다운 색인을 공개하라고
제안했다.
에이전트가 HTTP 요청만 할 수 있으면 설치 없이 색인을 읽고 가장 관련 있는 문서로
이동할 수 있기 때문이다.[^simonw]
이에 kinlan은 developer.chrome.com에 가이드 문서가 있다고 알리고 더 분명히 할 수
있다고 답했다.[^kinlan]
이 대화는 이 도구의 본체가 CLI가 아니라 가이드 문서 모음이며, CLI는 그것을
에이전트 컨텍스트에 효율적으로 전달하는 통로임을 보여 준다.

## 비평

### 가장 큰 쟁점은 Chrome에 치우친 기능을 권하는가이다

surround는 스킬이 에이전트에게 쓰라고 안내하는 기능 중 Chrome에서는 안정적이지만
Firefox와 Safari에서는 지원되지 않는 것이 CSS `@function`, `calc-size()`,
`interpolate-size`, `corner-shape` 등 매우 많다는 목록을 올렸다.
같은 글에서 그는 스킬이 Chrome 자체가 지원하지 않는 기능도 열한 개쯤 권하고,
프로젝트가 호환성을 고려하는 것으로 보인다고 공정하게 덧붙였다.[^surround]
Cthulhu_는 몇 개를 MDN에서 찾아보니 모두 실험적 기능이라며 에이전트가 이를 쓰지
않게 프롬프트하기를 바라고, 도구가 이를 권하는 것이 실망스럽다고
했다.[^Cthulhu_]
advisedwang은 Chrome이 이미 표준 세계에서 힘이 너무 센데 모든 LLM이 Chrome 팀의
지침을 따르게 되는 것이 걱정이라고 썼다.[^advisedwang]
이에 philipwalton은 Mozilla Firefox와 Microsoft Edge도 기여자인 크로스 브라우저
이니셔티브라고 답했고,[^philipwalton-1] 0o777은 이 프로젝트가 Chrome, Firefox,
Edge, Safari가 모두 지원하는 모범 사례만 권한다는 Baseline 프로젝트에 근거한다고
설명했다.[^0o777]
다만 Baseline 정책이 어떻게 적용되는지는 philipwalton의 다음 답이 더 정확하다.
스킬은 해당 기능으로 흔한 사례를 푸는 법을 문서화하고, Baseline에서 널리 지원이
되지 않는 API에는 브라우저 지원 표를 주며, 사이트의 지원 요구에 따라 에이전트가
쓸지 결정하게 한다는 것이다.
대부분은 크로스 브라우저 대체 구현도 적혀 있다고 한다.[^philipwalton-2]
이는 개발자가 하는 선택이지만, 이 선택이 에이전트의 판단에 맡겨진다는 점이 정책
위험이다.
onion2k는 점진적 향상(progressive enhancement)이면 괜찮다고 했지만,[^onion2k]
codepoet80은 호환 코드를 원한다며 호환성을 떨어뜨리는 도구를 왜 쓰느냐고
물었다.[^codepoet80]

### 평가 결과의 의미는 제한적이다

README의 상승분은 인상적이지만 몇 가지 단서가 있다.
평가는 이 프로젝트가 직접 만든 과제와 채점기로 이루어지고, 과제 설계자가
가이드를 쓴 쪽과 같다.
측정 대상은 가이드를 따랐는지이며, 그 코드가 실제 브라우저와 사용자에게 더
나은지는 다른 문제다.
Playwright 검증이 접근성 상태와 계산된 스타일을 확인한다고 하지만, 크로스
브라우저 동작은 이 지표로 알 수 없다.
sublinear는 “현대 웹 기본 기능”이 곧 최선의 방식은 아니며 브라우저별 구현의
함정을 다듬는 데 보통 10년이 걸린다고 하며, 완성도를 원하면 기기와 브라우저
조합의 수동 테스트를 피할 수 없다고 썼다.[^sublinear]
reedlaw는 자신의 코드를 `legacy-scan`에 돌렸더니 문제가 두 개만 나왔다고
했고,[^reedlaw] paulirish는 스캔이 명확히 감지되는 레거시 패턴만 겨냥하고 오탐을
피하도록 조율되어서 전체 가이드의 약 20%만 겹치며, 한 달 안에 50%쯤으로 늘릴
계획이라고 답했다.[^paulirish-2]
이는 도구 쪽이 밝힌 현재 한계다.

### “모범 사례” 자체가 의미를 잃었다는 반론

phyzix5761은 AI 시대에 모범 사례는 거의 죽었고, 곧 AI가 만든 코드를 아무도 읽지
않을 것이라고 썼다.[^phyzix5761]
natorion은 좋은 사용자 경험으로 이어지면 모범 사례는 죽지 않았고, 초점이 개발자
편의에서 줄어들 뿐이라고 반박했다.[^natorion]
paulirish는 모범 사례가 코드뿐 아니라 품질 있는 UX, 키보드 조작성, 레이아웃 이동
방지를 보장하는 것이라고 했다.[^paulirish-3]
이 논쟁은 도구의 효과가 아니라 코드 읽기의 미래에 대한 전망이므로 이 도구가
판가름하지는 못한다.

### 사이트의 수치와 README의 수치

사이트의 91% 대 약 51%와 README의 11월 8일 표(가이드 없음 54~58%,
있음 82~94%)는 같은 평가를 다른 시점과 집계로 보여 주는 것으로 읽히지만,
이 문서는 둘이 같은 실행에서 나왔는지 확인하지 못했다.
사이트는 모델 이름이나 과제 수를 첫 화면에서 밝히지 않는다.
어느 수치가 어떤 모델, 어떤 과제 집합, 언제의 값인지는 공개 대시보드를 열어
대조해야 한다.

### 사례는 제작자가 고른 것이다

파트너 사례 네 건은 모두 도구를 쓴 조직이 얻은 개선을 보여 준다.
사이트가 사례를 고른 기준이나 효과가 없었던 사례의 비율은 첫 화면에 없다.
수치의 기준도 각 카드마다 다르다.
MetaMask는 PR 480개에 43건의 수정이라는 건수이고,
Policybazaar는 감사 노력의 비율이다.
또한 여러 사례가 Modern Web Guidance와 DevTools for agents를 함께 썼다고 하므로
어느 효과가 가이드에서 나왔는지는 카드만으로 가를 수 없다.

## 인사이트

### 에이전트의 기본값을 바꾸는 가장 싼 길은 도구 설명이 아니라 지침이다

모델을 고치는 것은 도구 제작자가 할 수 없고, 에이전트 하네스의 기본값도 건드리기
어렵다.
이 프로젝트는 그 사이에서 에이전트가 검색하는 문서를 바꾸는 방식으로 기본 선택을
옮긴다.
평가에서 모델이 이미 아는 지식은 가지치기한다는 설계는, 지침이 컨텍스트를
낭비하지 않게 하려는 장치다.
SoftTalker가 인용 문장을 “세상에”라고 평했듯 평가 인프라에 크게 투자한 것이
놀라울 수는 있지만,[^SoftTalker] 이 투자가 없으면 지침은 평균적인 조언을
늘어놓는 것에 그친다.
cyanydeez는 모든 가이드를 주입하면 모델이 이 관행들의 평균을 따라
쓸모없어진다며, 한 단계에서 에이전트에게 가이드를 따라 훑으라고 시키는 방식이
낫다고 보았다.[^cyanydeez]
이 의견은 지침의 양과 시점이 효과를 좌우한다는 가설이며 검증되지 않았다.

### 표준을 정하는 쪽이 에이전트의 선호도 정한다

에이전트가 쓰는 웹 기능의 선택이 소수 조직의 가이드에 의존하게 되면, 새 기능의
채택 속도와 범위가 그 가이드의 편집 판단에 영향을 받는다.
Arubis는 Firefox에서 사이트를 열 때 다른 브라우저로 바꿔야 하는 일이 “몇 주에 한
번”에서 “주에 여러 번”으로 늘었고, 대부분 AI가 함께 쓴 것으로 보이는 사이트라고
했다.[^Arubis]
이는 한 사용자의 관찰이고 원인이 이 도구인지는 확인된 것이 아니다.
그래도 이 도구가 널리 쓰일 때 호환성 정책이 에이전트 출력에 얼마나 반영되는지는
추적할 가치가 있는 지표다.

### 가이드와 검증을 한 묶음으로 내놓는 구성

사이트는 가이드를 단독 도구가 아니라 DevTools for agents와 이어진 고리로
보여 준다.
지침으로 기본 선택을 옮기고, 브라우저에서 실제로 돌려 확인하는 단계가 따로
있다는 것이다.
이 문서가 읽은 바로는 이 구성은 위 비평에서 본 호환성 걱정을
검증 단계가 받는 구조다.
다만 사이트는 크로스 브라우저 확인을 검증 단계에 포함하는지 첫 화면에서
말하지 않으므로, 실제로 Chrome 밖의 브라우저까지 확인하는지는 문서를 열어
봐야 안다.

### 결론을 바꿀 관찰

- 가이드 있는 에이전트가 만든 코드를 Chrome, Firefox, Safari에서 모두 돌려 본
  독립된 측정이 나와 호환성 문제가 늘지 않는다면, Chrome 편향 우려는 약해진다.
- 평가가 이 프로젝트 밖의 과제로 재현되어 상승분이 비슷하게 나온다면, README의
  수치가 더 믿을 만해진다.
- 반대로 가이드가 권한 기능 때문에 비지원 브라우저에서 깨지는 사례가 쌓이면,
  에이전트에 판단을 맡기는 현재 방식의 위험이 확인된다.

---

[^paulirish-1]: <https://news.ycombinator.com/item?id=50444384>

[^halflife]: <https://news.ycombinator.com/item?id=50444390>

[^simonw]: <https://news.ycombinator.com/item?id=50444594>

[^kinlan]: <https://news.ycombinator.com/item?id=50444904>

[^surround]: <https://news.ycombinator.com/item?id=50446132>

[^Cthulhu_]: <https://news.ycombinator.com/item?id=50451814>

[^advisedwang]: <https://news.ycombinator.com/item?id=50444758>

[^philipwalton-1]: <https://news.ycombinator.com/item?id=50444860>

[^0o777]: <https://news.ycombinator.com/item?id=50444960>

[^philipwalton-2]: <https://news.ycombinator.com/item?id=50446275>

[^onion2k]: <https://news.ycombinator.com/item?id=50450807>

[^codepoet80]: <https://news.ycombinator.com/item?id=50446852>

[^sublinear]: <https://news.ycombinator.com/item?id=50444717>

[^reedlaw]: <https://news.ycombinator.com/item?id=50445033>

[^paulirish-2]: <https://news.ycombinator.com/item?id=50445195>

[^phyzix5761]: <https://news.ycombinator.com/item?id=50444183>

[^natorion]: <https://news.ycombinator.com/item?id=50444260>

[^paulirish-3]: <https://news.ycombinator.com/item?id=50444384>

[^SoftTalker]: <https://news.ycombinator.com/item?id=50447679>

[^cyanydeez]: <https://news.ycombinator.com/item?id=50444534>

[^Arubis]: <https://news.ycombinator.com/item?id=50454562>
