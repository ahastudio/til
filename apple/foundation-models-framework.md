# Apple Foundation Models framework는 온디바이스 모델과 Claude, Gemini 같은 서버 모델을 하나의 Swift API로 묶으려 한다

<https://developer.apple.com/foundation-models-framework/>

HN 토론: <https://news.ycombinator.com/item?id=50474361> (267점, 35개 댓글)

GN 토론: <https://news.hada.io/topic?id=37098>

## 소개

Foundation Models framework는 앱에 대규모 언어 모델을 넣기 위한 Apple의 네이티브 Swift API이다.
Apple 개발자 사이트의 이 안내 페이지는 이것을 어떤 대규모 언어 모델이든 앱에서 쓰는 가장 좋은 방법이라고 소개한다.
기기 안과 Private Cloud Compute(PCC)의 Apple Foundation Models에 바로 접근할 수 있고, 가이드 생성(guided generation)과 도구 호출과 이미지 이해와 Dynamic Profiles가 내장되어 있다고 한다.
페이지에 적힌 내용은 모두 Apple의 설명이며, 이 문서가 API를 써 보거나 성능을 측정한 것은 아니다.

## 페이지가 말하는 것

### 모델 지원

프레임워크는 Apple Intelligence의 핵심인 기기 내 파운데이션 모델에 직접 접근하게 한다.
이 모델은 똑똑하고 개인적이며 인터넷 없이도 돌아간다고 설명한다.
더 복잡한 작업에는 더 큰 모델이 필요하다는 점을 인정하면서, 이제 프레임워크가 Claude와 Gemini 같은 서버 모델까지 같은 Swift API로 확장되고 도구 호출과 가이드 생성도 그대로 지원된다고 한다.
어떤 모델 제공자든 언어 모델 프로토콜을 따르는 Swift 패키지를 만들 수 있다.
지원하는 서드파티 모델로 Core AI 언어 모델, MLX 언어 모델, Claude, Gemini가 나열된다.

### Private Cloud Compute

App Store 소규모 사업자 프로그램에 등록되어 있고 첫 App Store 다운로드가 200만 건 미만인 개발자는 PCC에서 도는 Apple Foundation Models를 클라우드 API 비용 없이 쓸 수 있다고 한다.
페이지는 이것이 최전선 수준의 지능을 사용자 데이터가 Apple이나 누구에게도 저장되거나 접근되지 않는 개인정보 보호와 함께 준다고 주장한다.

### 새 기능

- 이미지 이해: 이미지를 프롬프트에 붙일 수 있고 Vision 프레임워크가 통합되어 OCR이나 바코드 읽기를 기기 안에서 쓴다.
- Dynamic Profiles: 세션의 모델, 도구, 지시를 즉석에서 갱신하는 선언형 API이다. 프로필마다 모델과 온도와 추론 수준과 도구 묶음을 정하고 한 세션 안에서 바꾸며, 대화 기록은 프로필을 바꿔도 공유된다. 에이전트나 스킬 같은 상위 추상을 만드는 재료라고 한다.
- Evaluations 프레임워크: 프롬프트를 시험하고 동적 조건에서 기능이 맞게 동작하는지 검증한다. 모델을 바꾸거나 Dynamic Profile을 조정할 때 출시 전 신뢰를 준다고 한다.
- `fm` 명령줄 도구: macOS 27에 들어가며 앱 코드를 쓰지 않고 스크립트와 모델 워크플로를 자동화한다.
- 오픈소스: 맞춤 스킬, 컨텍스트 관리 도우미, 선택한 호스팅 모델에 붙는 Chat Completions 클라이언트를 담은 유틸리티 패키지와 Python SDK가 있다.
- 요구 사항: Apple Foundation Models의 금지된 사용을 정한 허용 사용 요건이 있고, EU AI 법 53조 1항 (b)에 따라 AFM 3 Cloud를 자기 AI 시스템에 통합하려는 제공자에게 정보와 문서를 제공한다고 밝힌다.

## 분석

### 중심 주장은 모델 제공자 위의 추상층을 Apple이 맡겠다는 것이다

페이지의 가장 큰 변화는 프레임워크가 기기 내 모델에 한정되지 않고 서버 모델까지 같은 API로 묶는다는 점이다.
이것은 모델 제공자가 아니라 모델과 앱 사이의 인터페이스를 Apple이 쥐겠다는 선택이다.
언어 모델 프로토콜을 공개해 제공자가 Swift 패키지를 만들 수 있게 한 것도 같은 방향이다.
HN의 한 댓글은 이 상황을 이렇게 평했다. 경쟁하는 AI 제공자들 위에 Apple이 통합 추상화를 제공하는 지점에 이르렀고, 어딘가에서 개발자가 제공자별 기능 가운데 어느 것이 추상화를 먼저 깨뜨리는지 이미 알아보고 있을 것이라는 것이다.[^swtcyber]
추상화의 이득은 제공자를 바꾸는 비용을 낮추는 것이고, 대가는 가장 작은 공통 기능에 맞춰진다는 점이다.

### 무료 PCC는 소규모 개발자를 겨냥한 유인책이다

PCC를 소규모 사업자에게 비용 없이 여는 조건은 앱이 아직 작을 때의 진입 비용을 없애는 장치이다.
HN의 한 댓글은 이를 그대로 인용하며 확인했고, 답글은 조직 개발자 계정이 있어야 PCC 권한을 받을 수 있다고 한 사용자의 경험을 전했다.[^btown][^nseggs]
다른 답글은 일일 한도가 명시되지 않은 무료 토큰이라는 표현이 많은 부담을 진다고 지적했다.[^swtcyber2]
페이지는 별표로 조건을 단서 달고 있어서 한도는 페이지만으로는 알 수 없다.

### 에이전트 구조를 프레임워크에 내장하려는 흐름이다

Dynamic Profiles와 Evaluations는 앱이 에이전트가 되어 가는 것을 가정한 설계이다.
세션 하나에서 모델과 도구와 지시를 바꾸고, 그 변경이 프롬프트의 품질을 해치지 않는지 평가하는 틀을 함께 준다.
이는 이 저장소의 다른 글들이 다룬 다중 모델 전환(Antigravity의 Orchestrator)과 같은 문제를 Apple 방식으로 푼 것이다.

## 비평

### 온디바이스 모델의 품질에 대한 증거가 페이지에 없다

페이지는 온디바이스 모델이 유용하다고 말하지만 성능 수치나 비교가 없다.
HN의 한 댓글은 같은 크기의 다른 모델, 곧 Gemma 4 E4B나 Qwen 3.5 4B와 비교한 벤치마크나 사용 시험을 본 적이 없다고 했다.[^cnj]
사용 경험은 엇갈린다.
한 사용자는 터미널에서 오류 수정과 명령 제안에 쓰는데 M1 8GB에서도 놀랄 만큼 쓸 만하다고 했고,[^albertgoeswoof]
다른 사용자는 SwiftUI 앱의 문법 검토에 시험했더니 쓸 수 없어서 Sonnet으로 돌아갔다고 했다.[^lukisk]
한 사용자는 가장 간단한 코딩으로 FizzBuzz를 빠르게 냈다고 했지만 코딩 하네스에서 좋을지는 모른다고 했고,[^jonwood]
더 강한 PCC 모델도 웹 기반 횡스크롤 플랫포머 코딩 과제에서 고전했다는 시험도 있었다.[^bobertdowney]
이 보고들은 개인 경험이고 같은 조건의 비교가 아니다.

### 안전 장치가 강하다는 불만이 있다

한 댓글은 모델의 안전 제한이 일상 사용에 꽤 공격적인 것 같다고 물었고,[^jshier]
macOS 27의 `fm` 명령은 두꺼운 가드레일이 있다고 다른 사용자가 전했다.[^gardaani]
가드레일의 범위는 페이지에 없다.
허용 사용 요건 문서가 금지 용도를 정한다고만 안내한다.

### 공급자 목록의 빈자리가 눈에 띈다

한 댓글은 지원 서버 모델의 명시 목록에 Claude와 Gemini가 있고 ChatGPT가 없는 점을 지적하며 법적 분쟁 때문이 아니냐고 비꼬았다.[^einsteinx2]
이는 추측이다.
페이지는 Claude, Gemini와 함께 “and more”라고 쓰고 지원 목록을 따로 둔다.

### HN이 새로움을 묻는 질문이 먼저였다

스레드는 이 페이지가 왜 첫 화면에 올랐는지를 묻는 댓글로 시작했고, 답글은 작년에 발표되어 이미 논의되었다고 알렸다.[^imagetic]
이 페이지는 모델 지원과 Dynamic Profiles와 `fm` 도구가 새로 들어간 갱신된 판이다.

## 인사이트

### 앱 개발자의 선택지는 세 층의 모델로 정리된다

페이지의 구조에서 앱 개발자의 선택지를 세 층으로 읽을 수 있다.
기기 안의 작은 모델(오프라인과 개인정보에 유리하고 능력에 한계), PCC의 더 큰 Apple 모델(개인정보 보호를 내세우고 소규모 사업자에게 무료 조건), 서드파티 서버 모델(능력이 크고 제공자의 데이터 처리 정책을 따름)이다.
이 세 층을 같은 API로 오가게 한다는 것이 이 프레임워크의 가치이고, 작업마다 어느 층에 보낼지를 정하는 일이 개발자의 몫으로 남는다.
Dynamic Profiles는 그 선택을 세션 안에서 바꾸는 수단이다.

### 인증과 키 관리가 서버 모델 연동의 실제 병목이다

HN의 한 댓글은 Claude가 몇 달 전부터 App Attest를 지원한다는 점을 짚으며, iOS 앱에서 LLM을 직접 부르려면 Firebase가 가장 실용적인 방법이었는데 Anthropic이 이것을 더 알리지 않는 것이 놀랍다고 했다.[^mcemilg]
답글은 App Attest가 요청이 추출된 키가 아니라 실제 앱에서 왔음을 믿게 해 주는 견고한 해법으로 보인다고 평했다.[^jonwood2]
이 대화는 서버 모델을 앱에서 쓸 때의 어려움이 모델 호출 자체가 아니라 앱 안에 키를 두지 않고 요청의 출처를 증명하는 데 있다는 것을 보여 준다.

### 확인할 관찰

이 프레임워크의 실제 가치를 가를 관찰은 세 가지이다.
무료 PCC의 일일 한도와 조건이 공개되는지,
온디바이스 모델과 같은 크기 모델의 독립 비교가 나오는지,
서드파티 제공자의 Swift 패키지가 얼마나 늘어나는지이다.

---

[^swtcyber]: <https://news.ycombinator.com/item?id=50478742>

[^btown]: <https://news.ycombinator.com/item?id=50476748>

[^nseggs]: <https://news.ycombinator.com/item?id=50477303>

[^swtcyber2]: <https://news.ycombinator.com/item?id=50478754>

[^cnj]: <https://news.ycombinator.com/item?id=50480442>

[^albertgoeswoof]: <https://news.ycombinator.com/item?id=50474967>

[^lukisk]: <https://news.ycombinator.com/item?id=50485861>

[^jonwood]: <https://news.ycombinator.com/item?id=50481391>

[^bobertdowney]: <https://news.ycombinator.com/item?id=50476479>

[^jshier]: <https://news.ycombinator.com/item?id=50475020>

[^gardaani]: <https://news.ycombinator.com/item?id=50479074>

[^einsteinx2]: <https://news.ycombinator.com/item?id=50481160>

[^imagetic]: <https://news.ycombinator.com/item?id=50474701>

[^mcemilg]: <https://news.ycombinator.com/item?id=50475592>

[^jonwood2]: <https://news.ycombinator.com/item?id=50481381>
