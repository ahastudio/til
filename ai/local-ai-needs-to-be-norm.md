# 로컬 AI가 표준이 되어야 한다

원문: <https://unix.foo/posts/local-ai-needs-to-be-norm/>

HN 토론: <https://news.ycombinator.com/item?id=48085821> (783점, 357개 댓글)

## 요약

Brutalist Report iOS 앱 개발자가 쓴 글로, 개발자들이 단순한 데이터 변환 작업에 OpenAI·Anthropic 같은 클라우드 AI를 의존하는 관행을 비판한다.
기기에 이미 있는 데이터를 처리하는 데 외부 서버가 필요 없다는 주장이며, Apple FoundationModels API로 로컬 요약 기능을 구현한 실제 사례를 제시한다.

## 분석

### 클라우드 AI 의존의 문제

저자는 사용자 콘텐츠를 제3자 AI에 스트리밍하는 순간 제품의 성질이 바뀐다고 지적한다.

- 네트워크 의존성: 서버 장애나 결제 문제가 곧 기능 장애로 이어진다.
- 프라이버시: 방대한 정책 문서가 필요한 데이터 흐름을 만들어낸다.
- 비용: API 호출당 과금은 사용자가 늘수록 선형으로 증가한다.

### 로컬 AI가 충분한 영역

요약, 분류, 추출, 재작성, 정규화 같은 작업은 셰익스피어를 쓰거나 양자역학을 설명하는 모델이 필요 없다.
기기에 이미 존재하는 정보를 변환하는 작업이라면 로컬 모델이 충분하다.

### Apple FoundationModels API

```swift
import FoundationModels
let session = LanguageModelSession()
let response = try await session.respond(...)
```

타입 안전 구조화 출력을 사용하면 JSON 파싱 추측 없이 결과를 받을 수 있다.

```swift
@Generable
struct ArticleIntel {
  @Guide(description: "...") var tldr: String
  @Guide(description: "...") var bullets: [String]
}
```

Brutalist Report는 이 방식으로 서버 왕복, 프롬프트 로깅, 데이터 보관 정책 없이 기사 요약을 구현했다.

## 비평

저자의 주장은 설득력이 있지만 적용 범위에 한계가 있다.
로컬 모델은 단순 변환에는 충분하지만 최신 지식이 필요한 작업이나 멀티모달 추론에서 클라우드 모델과 격차가 크다.
Apple FoundationModels는 Apple 생태계에서만 동작하므로 크로스플랫폼 앱에는 대안이 없다.
로컬 AI 실행에 필요한 기기 성능도 아직 불균등하다.

adamtaylor_13[^adamtaylor_13]은 "Opus 수준 성능이 로컬에서 실용적인 속도로 동작하게 될 때 함께하겠다"며 현실적인 선을 그었다.
현재로서는 버지니아 서버팜이 자신의 실제 요구를 충족시키는 유일한 선택지라는 것이다.
QuadrupleA[^QuadrupleA]도 8GB 모델이 자동으로 다운로드되고 VRAM 부족으로 크래시가 나는 시나리오를 우려했다.
기기 이질성 문제는 로컬 AI 배포의 현실적 장벽으로 남아 있다.

## 인사이트

"AI는 어디에나"가 목표가 아니라 "유용한 소프트웨어"가 목표라는 저자의 결론은 간결하다.
클라우드 AI 의존이 기능처럼 보이지만 실제로는 분산 시스템 복잡도를 도입하는 것이라는 관점은 개발자가 설계 시 자주 놓치는 지점이다.
로컬과 클라우드를 구분하는 기준은 모델 성능이 아니라 데이터가 이미 기기에 있는가 여부다.

pronik[^pronik]은 기술 진화의 방향성을 구체적으로 그렸다.
대규모 데이터센터 → H100 몇 장짜리 서버 → MacBook Pro 128GB VRAM으로의 흐름이 이미 진행 중이며, 1년 내에 "원격 대형 모델로 계획, 로컬 느리지만 인간보다 빠른 모델로 실행"하는 패턴이 기업 표준이 될 것으로 예측했다.

Guillaume86[^Guillaume86]은 "프라이버시 AI"와 "로컬 AI" 논의를 분리해야 한다고 제안했다.
대형 LLM은 대규모 서버에서 실행하는 것이 현실적으로 합리적이지만, 그 서버를 반드시 민간 기업이 운영해야 한다는 의미는 아니라는 지적이다.
자체 호스팅 추론 인프라와 오픈소스 모델을 조합하는 경로가 클라우드 의존 없이 프라이버시를 확보하는 현실적 대안이 될 수 있다.

TheJCDenton[^TheJCDenton]은 수십 년 전 오픈소스에 대한 주류 반응과 현재 로컬 AI에 대한 인식을 겹쳐봤다.
코딩에서 Anthropic과 OpenAI에 대한 의존도가 "미쳐있다"고 표현하며, 예고 없이 중단될 수 있는 외부 인프라에 핵심 개발 워크플로우를 위탁하는 구조의 위험성을 지적했다.

---

[^adamtaylor_13]: <https://news.ycombinator.com/item?id=48090332>
[^QuadrupleA]: <https://news.ycombinator.com/item?id=48091091>
[^pronik]: <https://news.ycombinator.com/item?id=48088051>
[^Guillaume86]: <https://news.ycombinator.com/item?id=48088433>
[^TheJCDenton]: <https://news.ycombinator.com/item?id=48087467>
