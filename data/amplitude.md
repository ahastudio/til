# Amplitude: 제품 분석을 AI 에이전트와 한 루프로 묶겠다는 플랫폼의 두 얼굴

<https://amplitude.com/>

<https://amplitude.com/digital-analytics-platform>

## 소개

Amplitude는 제품 분석(product analytics)에서 출발해
세션 리플레이, 실험, 피처 플래그, 인앱 안내,
데이터 활성화까지 한 플랫폼에 묶은 SaaS다.
회사 소개 페이지는 2012년 Y Combinator(W12)에서 시작했고,
직원 700명 이상,
고객 5,200곳 이상(포춘 100대 기업 30곳 포함)이라고 적는다.[^company]
홈페이지의 첫 문장은 분석에서
피드백과 코드까지 AI를 제품을 만드는 모든 단계에 넣어
스스로 개선되는 제품(self-improving products)을 만든다는 것이다.

이 문서는 같은 회사의 두 페이지를 함께 읽는다.
하나는 2026년 현재의 홈페이지이고,
다른 하나는 페이지 메타데이터상 2023년 12월에 처음 공개되어
2026년 5월 2일에 마지막으로 수정된 digital-analytics-platform 페이지다.
두 페이지는 같은 회사를 소개하지만 내세우는 중심이 다르다.
홈페이지는 에이전트와 MCP와 자기 개선 루프를 앞세우고,
플랫폼 페이지는 디지털 분석 플랫폼으로서의 포괄성과 투자 대비 효과를 앞세운다.
이 차이를 읽는 것이 이 문서의 한 축이고,
나머지 한 축은 두 페이지가 인용한 숫자를
뒷받침하는 페이지를 직접 열어 확인한 결과다.

## 제품 구성

홈페이지의 메뉴는 플랫폼을 네 묶음으로 나눈다.

| 묶음     | 포함된 것                                                                                        |
| -------- | ------------------------------------------------------------------------------------------------ |
| AI       | Agents, Headless Amplitude, Agent Analytics, Amplitude MCP, AI Feedback                          |
| Insights | Product Analytics, Marketing Analytics, Session Replay, Heatmaps                                 |
| Action   | Guides and Surveys, Feature Experimentation, Web Experimentation, Feature Management, Activation |
| Data     | Data Governance, Integrations, Security & Privacy                                                |

여기서 두 종류의 에이전트를 구분해야 한다.
Global Agent와 특화 에이전트는 Amplitude 안에서 일하는 AI 분석가다.
이벤트 분류, 차트, 대시보드, 실험, 플래그,
거버넌스 메타데이터로 제품에 대한 의미 모델을 만들고,
질문에 답하고 차트와 대시보드와 PRD 초안을 만들고
데이터 정리를 제안한다.[^agent-page]
반면
Agent Analytics는 고객이 자기 제품에 넣은
AI 에이전트의 사용을 분석하는 제품이다.
요금표에서도 월간 에이전트 세션과 트레이스 분석,
평가기 같은 항목으로 따로 정의되어 있다.[^pricing]
이름이 비슷해서 홈페이지만 읽으면 쉽게 섞인다.

## 홈페이지가 말하는 것

### 에이전트가 가장 앞에 선다

홈페이지의 대표 문구는 Amplitude가 시장에서
가장 성능이 높은 분석 에이전트라는 것이다.
근거로는 Global Agent가 고객 4,900곳 이상에서
고객 문제의 76%를 평균적으로 해결하고,
일부는 85%를 넘으며 평균 해결률이 매달 1%포인트씩 오른다는 설명이 붙는다.
사용 통계로는 사용자 중 41.7%가 AI로 상호작용하고, 주간 AI 상호작용이 134만 건,
주간 활성 AI 사용자가 2만 9,200명, 주간 MCP 도구 호출이 121만 건이라고 적는다.

MCP와 헤드리스 쪽 페이지는 같은 방향을 더 밀어붙인다.
Headless Amplitude는 Amplitude의 제품 맥락을 Claude,
Cursor 같은 도구와 에이전트로 가져가는 것이고,
MCP 주간 활성 사용자가 1만 6천 명 이상이라고 한다.
페이지는 활성화율이 떨어지면
에이전트가 원인을 찾아 수정 PR까지 여는 시나리오를 보여 주고,
결정적 명령이 필요한 반복 작업을 위한 `amp` CLI도 소개한다.[^headless]
설치도 그 방향에 맞춰 두었다.
홈페이지는 AI 편집기에 붙여 넣으라고
SDK 설치 명령(`npm install @amplitude/analytics-browser`)을 바로 제시한다.

### 실험과 플래그와 리플레이도 같은 이야기에 묶인다

실험 페이지는 순차 검정, T 검정, 다중 슬롯머신 알고리즘(multi-armed bandit),
CUPED, 상호 배제 그룹, 홀드아웃을
내장했다고 적고, 분석 차트와 세션 리플레이에서
실험을 바로 시작할 수 있다고 한다.[^experiment]
피처 관리 페이지는 클라이언트와 서버 플래그,
로컬과 원격 평가, 롤백과 자동 생성 대시보드를 말한다.[^fm]
세션 리플레이 페이지는 기본 텍스트 마스킹과 개인정보 API 연동,
AI 요약, 실험과 안내용 리플레이를 말한다.[^replay]
이 세 페이지의 공통 서사는 같은 데이터 모델과 사용자 식별과 코호트로
분석에서 실험으로, 리플레이로, 안내로 한 번에 넘어간다는 것이다.

### 자기 개선 루프의 증거로 내부 사례를 든다

홈페이지가 추천 자료로 올린 Speedrunning Software
글은 Amplitude 자신의 이야기다.
6개월 만에 PR을 3배로 늘렸고 PR 주기를 5.2시간에서 44분으로 줄였다고 한다.
글은 PR이 허영 지표가 될 수 있다는 점을 스스로 인정하면서도
PR 하나하나가 실험이라서 고객 가치의 선행 지표라고 주장한다.[^speedrun]
고객 이야기로는 전환 27% 증가, 온보딩 개선으로 활성화 40% 증가,
개인화 콘텐츠로 구독자 40% 증가 세 편의 제목을 보여 준다.

## digital-analytics-platform 페이지

### 이 페이지가 하는 말

이 페이지는 제목에서
스스로를 1위로 평가받은 디지털 분석 플랫폼(#1
Rated Digital Analytics Platform)이라 부르고
본문에서는 AI 우선 디지털 분석 플랫폼이라고 소개한다.
세 가지 약속을 한다.
모두가 AI로 통찰을 얻게 하고, 고객 여정 전체를 이해하게 하며,
통찰을 얻는 같은 곳에서 개인화된 경험으로 바로 연결하게 한다는 것이다.
플랫폼 구성은 AI 에이전트와 Act, Decide, Sense 네 묶음이다.
Act는 개인화와 실험과 인앱 소통, Decide는 정량과 정성 통찰,
Sense는 거버넌스된 고객 데이터 수집이다.

요금제는 네 칸의 카드로 보여 준다.
무료는 입문용, 둘째는 작은 팀을 위한 분석과 플래그와 활성화와 세션 리플레이,
셋째는 자동화된 통찰과 실험과 오디언스, 넷째는 고급 맞춤과 자동화와 통제다.
증거로는 Forrester의 총경제효과(Total Economic Impact) 연구를 앞세운다.
Amplitude가 의뢰한 이 연구에서 합성 조직이 투자 대비 수익률 217%,
회수 기간 6개월 미만,
3년간 매출 효과 534만 달러와 운영 효율과 비용 절감 260만 달러를 얻었다고 한다.
고객 사례는 MySwimPro(실험 10배, 사용자당 평균 매출 70% 증가),
TicketSwap(판매 퍼널 완료율 15% 증가),
Rocket Money(연 1,000만 달러 매출 추가 기대) 세 곳이다.
애널리스트 평가로는 Forrester Wave: Digital Analytics Solutions 2025년 3분기의
리더이자 고객 선호 기업(Customer Favorite)이고
21개 기준에서 5점 만점이라고 한다.

### 홈페이지와 겹치는 곳과 갈리는 곳

| 항목        | 홈페이지                                              | digital-analytics-platform 페이지                                |
| ----------- | ----------------------------------------------------- | ---------------------------------------------------------------- |
| 중심 서사   | 에이전트와 MCP로 스스로 개선되는 제품                 | 모든 단계를 잇는 AI 우선 디지털 분석 플랫폼                      |
| 구성 어휘   | AI, Insights, Action, Data                            | AI Agents, Act, Decide, Sense                                    |
| AI의 위치   | 성능 수치(해결률 76%)와 사용 통계                     | 세 약속 중 하나와 AI Agents 묶음. 요금제 카드에는 AI 항목이 없다 |
| 가격 서술   | 무료 월 200만 이벤트를 업계에서 가장 후한 무료로 소개 | 카드 네 칸. 무료는 입문용이라고만 소개                           |
| 증거의 종류 | 사용 통계, 자사 내부 사례, 고객 이야기 제목           | 의뢰 연구(합성 조직), 고객 사례 세 편, 애널리스트 평가           |
| 증거의 시점 | 최근 통계와 2025년 평가                               | 2023~2024년 고객 사례와 2024년 연구                              |
| 겹치는 증거 | Forrester Wave 2025년 3분기                           | 같은 Forrester Wave와 요금제 안내                                |

두 페이지는 같은 제품을 다른 청중에게 말한다.
홈페이지는 AI 도구를 쓰는 개발자와 제품 담당자를,
플랫폼 페이지는 분석 플랫폼을 비교하며
구매를 검토하는 사람을 겨냥하는 것으로 읽힌다.
이는 이 문서의 해석이다.

### 이 페이지의 숫자를 근거 페이지에서 확인한 결과

| 주장                               | 근거 페이지가 말하는 것                                                         | 판정                                  |
| ---------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------- |
| 투자 수익률 217%, 회수 6개월 미만  | Amplitude 의뢰 연구이고 인터뷰한 고객들의 합성 조직 기준                        | 맞지만 한 합성 조직의 모형이다        |
| 3년 매출 효과 534만 달러           | 블로그는 구성 항목을 180만, 210만, 130만 달러로 합쳐 520만 달러 이상이라고 적음 | 반올림 차이 안에서 일치한다           |
| 운영 효율과 절감 260만 달러        | 87만 3,700, 15만 1,400, 160만 달러를 더하면 약 262만 달러                       | 일치한다                              |
| MySwimPro 실험 10배, ARPU 70% 증가 | 분기당 A/B 테스트가 2건에서 19건으로. 70%는 실험 한 건의 결과                   | 맞는 숫자를 압축해 한 문장으로 합쳤다 |
| TicketSwap 퍼널 완료율 15% 증가    | 오디언스를 광고와 CRM으로 동기화해 돌아오게 한 결과로 15% 증가                  | 일치한다                              |
| Rocket Money 연 1,000만 달러 기대  | 블로그도 예측된 값이라고 적음                                                   | 예측임을 페이지가 기대라고 적어 일치  |
| Forrester 리더, 21개 기준 5점      | Forrester 면책 문구가 붙어 있고 Amplitude 자신이 우리에게는이라고 해석          | 평가는 사실이나 해석은 판매자의 것    |

MySwimPro 사례는 따로 짚을 만하다.
원 블로그에 따르면 실험을 도입하기 전 분기에 2건, 그다음 분기에 5건,
도입 뒤 분기에 19건의 A/B 테스트를 돌려 약 10배라고 했다.
70% 증가는 두 달 동안 돌린 가격과 수익화 실험 세
건이 각각 70%, 53%, 39% 올린 가운데 가장 큰 값이고,
저자는 모든 테스트가 통계적 유의성에 이르기를 기다리지 않았다고 직접 밝히며
테스트의 75%는 실패한다고도 적었다.[^myswimpro]
플랫폼 페이지는 이를 실험을 10배 늘려 ARPU 70%를 높였다고 한 문장에 압축했다.
TicketSwap 글은 2022년까지 Mixpanel을 쓰다가 갈아탔고
두 달 구현 뒤 여섯 달 병행 운영했다고 적는다.[^ticketswap]
Rocket Money 글은 1,000만 달러가 예측된 값이라고 적는다.[^rocketmoney]
세 사례의 게시일은 2023년 8월, 2023년 12월, 2024년 1월이고
연구는 2024년 12월에 나왔다.
2026년에 수정된 페이지가 2~3년 전 증거에 기대고 있다.

### 요금제 카드는 현재 요금표와 어긋난다

플랫폼 페이지의 둘째 카드는 세션 리플레이를 작은 팀용 플랜의 기능으로 소개한다.
현재 요금표는 무료 플랜에도 월 1만 건의 세션 리플레이를 넣고,
AI 에이전트와 MCP를 모든 플랜에 넣는다.[^pricing]
플랫폼 페이지의 카드에는 AI 항목이 없고 리플레이가 무료에 없다.
셋째 카드는 A/B 또는 다변량 테스트를 성장 단계에 둔다.
요금표는 웹 실험의 A/B/n을 무료에도 넣지만
실험 결과 보기는 무료와 Plus에 포함하지 않는다고 적는다.[^pricing]
페이지가 마지막으로 수정된 5월 이후 요금표가
바뀌었거나 두 페이지가 따로 관리되는 것으로 보이며,
어느 쪽인지는 이 문서가 확인하지 못했다.

## 가격과 사용

### 요금제의 구조

현재 요금표는 네 단계다.[^pricing]

| 단계       | 가격                | 핵심 한도와 내용                                                         |
| ---------- | ------------------- | ------------------------------------------------------------------------ |
| Free       | 무료, 신용카드 없음 | 월 200만 이벤트, 세션 리플레이 월 1만 건, 실험 1개, 데이터 보관 1년      |
| Plus       | 0달러부터           | 첫 200만 이벤트 무료, 최대 7,000만 이벤트, 코호트 20개, 히트맵, 보관 2년 |
| Growth     | 맞춤, 이벤트 기반   | 고급 행동 탐색, SSO와 프로젝트 권한, 월 2만 건 리플레이, 보관 무제한     |
| Enterprise | 맞춤, 이벤트 기반   | 프로젝트 무제한, 데이터 접근 통제, RBAC, 월 5만 건 리플레이, 전담 지원   |

모든 플랜이 무제한 좌석과 무제한 피처 플래그를 갖는다.
사용량 단위는 이벤트이고 사용자 단위가 아니다.
요금표는 MTU를 월간 추적 사용자로 정의하되 무료 플랜을 이벤트로 잰다고 설명한다.
Growth와 Enterprise에서
더 필요한 기능은 플랫폼 플랜에 대한 비율로 값이 매겨지는 추가 상품으로 산다.
이 모든 값이 문서에는 금액으로 나오지 않는다.
Plus는 0달러부터이고 Growth와 Enterprise는 문의해야 하며,
Annual Plus Plan 표의 이벤트 구간별 가격은 내가 읽은 텍스트에 없었다.
직원이 20명 미만이고
투자금이 1,000만 달러 미만인 스타트업은 Growth를 1년 무료로 받는다.

### 무료 플랜의 실제 한도

실험은 동시에 하나만 돌릴 수 있고
Growth 이상에서도 둘이며 더 쓰려면 추가 상품이다.
세션 리플레이는 월 1만 건이고 보관은 한 달이다.
Agent Analytics는 월간 에이전트 세션이 5,000건이고
에이전트 세션 대화 보관이 14일이다.
데이터 접근은 1년이다.
알림과 예측과 전환 동인 같은 기능은 상위 단계에 있다.
홈페이지의 업계에서
가장 후한 무료 플랜이라는 말은 이벤트 한도에 대해서는 사실일 수 있으나,
이 문서가 비교 대상의 요금제를 조사하지 않았으므로 확인하지 못했다.

### 에이전트와 보안

에이전트 페이지는 OpenAI, Google, Anthropic의 모델을 OpenAI,
Google Vertex, AWS Bedrock로 제공받아 쓰고
오케스트레이션과 기억과 세션 저장은 자체 백엔드로 만들었다고 밝힌다.
고객 데이터로 모델을 학습하지 않으며
각 에이전트는 고객별로 분리된 기억을 쌓는다고 한다.[^agent-page]
보안 페이지는 EU 데이터 센터가 프랑크푸르트에 있고
EU에 있는 조직의 AI 기능 처리가 EU 밖으로 나가지 않는다고 하며,
HIPAA 고객에게는 BAA를 맺고 AI 하위 처리자와도 BAA를 맺었다고 한다.
ISO 27001과 SOC 2 Type II 인증이라는 문장은 해당 페이지에서
AWS 데이터 센터를 설명하는 대목에 들어 있다.
Amplitude 자체의 인증 현황은 Customer Trust Portal로 안내되며
이 문서가 열어 보지 않았다.[^security]

## 인수와 통합

Amplitude는 2026년 5월 5일 Statsig의 브랜드와 고객을 넘겨받고
현재 Statsig 플랫폼을 클라우드와 데이터 웨어하우스에서
유지하고 발전시키며 더 통합된 로드맵을 만들겠다고 밝혔다.
원래의 Statsig 팀은 OpenAI에 있고 전환기에 협력한다.[^partnership]
저장소의 `feature-flag/statsig.md`가 이 인수를 Statsig 쪽에서 다룬다.
HN의 dantihanyi는 OpenAI가 Statsig를 2025년 9월에 11억
달러에 샀다는 보도를 링크했다.[^dantihanyi]

내가 읽은 Amplitude의 마케팅 페이지에는 Statsig가 한 군데도 없다.
홈페이지, 요금표, 에이전트와 헤드리스와 실험과 피처 관리와 세션 리플레이 페이지,
LaunchDarkly 비교 페이지, 플랫폼 페이지 어디에도 이름이 나오지 않았고,
언급은 파트너십 블로그 글에만 있었다.
Amplitude의 실험 제품이 자체 Experiment라는 점을 생각하면
두 제품의 통합 로드맵과 마케팅 구성이 아직 만나지 않았다는 신호로 읽힌다.
이는 마케팅 페이지가 인수 발표 뒤 갱신되었는지에 대한 추정이 아니라
읽은 시점의 사실에 대한 서술이다.

## 비평

### 숫자의 분모가 페이지마다 다르다

고객 수가 페이지마다 다르다.
제품 분석 페이지는 4,500곳 이상,
홈페이지의 에이전트 통계는 4,900곳 이상,
회사 소개 페이지는 5,200곳 이상이라고 적는다.[^analytics-page][^company]
각각 다른 분모(분석 고객, 에이전트 사용 고객,
전체 고객)일 수 있으나 페이지는 구분하지 않는다.

더 큰 문제는 홈페이지의 대표 수치다.
고객 문제의 76%를 해결한다고 하는데 문제와 해결의 정의가 없다.
시스템이 답을 냈다는 뜻인지 사용자가 해결되었다고
확인했다는 뜻인지, 어떤 표본인지 알 수 없다.
시장에서 가장 성능이 높은 분석 에이전트라는 주장도 비교 대상과 벤치마크가 없다.
주간 MCP 도구 호출 121만 건을 MCP 주간 활성 사용자 1만 6천 명으로 나누면
사용자당 약 76건이다.
이 나눗셈은 이 문서의 계산이고,
활성 사용자의 정의가 달라 비교 가능한 값인지는 알 수 없다.

### 사례의 증거는 오래되었고 합성이거나 한 건이다

플랫폼 페이지의 217%는 Amplitude가 의뢰한 연구에서
인터뷰 고객을 합친 가상의 조직이 얻은 값이다.[^tei]
실제 고객 한 곳이 217%를 얻었다는 뜻이 아니다.
MySwimPro의 70%는 한 건의 가격 실험 결과이고
저자도 유의성을 기다리지 않았다고 했다.
세 사례가 모두 2023~2024년의 것이라는 점도 앞서 보았다.
이 증거는 제품이 효과가 있었던 가능성을 보여 줄 뿐
2026년의 AI 중심 제품이 그만한 효과를 내는지는 말하지 않는다.
Forrester Wave는 2025년 7월 평가이고 평가 기관의 면책 문구가 붙은 채
Amplitude의 해석인 우리에게는이라는 말과 함께 소개된다.[^wave]

### 무료가 넉넉하다는 주장과 한도가 같이 있다

무료 플랜은 월 200만 이벤트에 무제한 좌석이라는 점에서 후하다.
그러나 실험이 한 번에 하나이고 결과 보기가 포함되지 않으며
리플레이 보관은 한 달이고 데이터 접근은 1년이다.
Growth 단계에서도 동시 실험이 둘이다.
Plus 소개는 이벤트가 늘어도
초과 요금과 갱신 때의 갑작스러운 인상 없이 쓰게 하겠다고 약속한다.

이 약속은 과거의 불만을 향한 것으로 읽힌다.
2023년 HN에서 Amplitude의 감원 소식에 붙은 댓글들은 제품은 좋지만
무료가 후하다가 어느 순간 급격히 비싸진다고 지적했다.[^feeble]
다른 댓글은 MTU 대신 이벤트 단위 가격이 있었으면 좋겠다고 했다.[^redsquare]
지금의 요금표는 이벤트 단위로 바뀌었지만 Growth 이상은 맞춤 견적이고
추가 상품은 플랫폼 요금의 비율이어서 금액이 공개되지 않는다.
급격한 인상이 사라졌는지는 가격표만으로는 알 수 없다.

### 경쟁사 비교는 자기 서술이다

LaunchDarkly 비교 페이지는 상대가 분석 연동이 필요하고
시각 편집기가 없으며 개발자 전용이고
리플레이와 안내와 설문이 없다고 적는다.[^launchdarkly]
이는 Amplitude가 쓴 상대의 약점 목록이어서 검증된 비교가 아니다.
실험 페이지가 내세우는 Forrester의 유일한 리더라는 평가는 2024년 3분기 자료다.
페이지의 HTML 제목은 Pendo 대안이라고 되어 있어 템플릿을 재사용한 흔적이 보이며
이 문서는 이를 사소한 부주의로만 기록한다.

### 플랫폼 페이지에는 구매 판단에 필요한 것이 빠져 있다

이 페이지는 스타트업부터 포춘 500대 기업까지 맞는 요금제가 있다고 말하지만
요금제 카드에는 금액도 이벤트 한도도 없다.
카드에 적힌 것은 기능 이름 네 개씩이고, 한도는 요금표 페이지를 봐야 알 수 있다.
같은 카드가 요금표와 어긋나는 곳이 있다는 점은 앞서 보았다.
플랫폼의 경계에 대한 서술도 없다.
어느 데이터는 Amplitude 안에 쌓이고 어느 데이터는 웨어하우스에 남는지,
무엇이 추가 상품이고 무엇이 기본인지,
동시 실험이 몇 개까지인지가 이 페이지에 없다.
Sense라는 묶음은 어디서든 신뢰할 수 있는 데이터를 가져온다고 하지만
수집 방식과 정합성을 어떻게 보장하는지는 말하지 않는다.
홈페이지의 에이전트와 Statsig도 이 페이지에는 나오지 않는다.
결과적으로 이 페이지는 비교 구매 단계의 첫 인상을 위한 글이고,
판단에 필요한 사실은 다른 페이지로 넘긴다.

### 에이전트가 실제로 하는 일의 범위가 불분명하다

에이전트 페이지는 에이전트가 사용자를 대신해 Amplitude 안에서 행동한다고 하지만
승인 절차의 구체적인 범위는 적지 않는다.
특화 에이전트가 제안을 사용자가 승인하면 실행한다는 서술은 있다.[^agent-page]
헤드리스 페이지의 시나리오는 에이전트가 PR을 열고
플래그를 켜고 롤백까지 하는 흐름을 보여 주는데,
이는 데모 화면의 연출이다.
그 시나리오의 활성화율 증가 예측치(18%)도 연출된 숫자이며
어떤 고객의 결과도 아니다.[^headless]

## 인사이트

### 에이전트가 코드를 더 빨리 만들수록 병목은 측정으로 옮겨 간다

Amplitude의 인수 발표문은 AI가 소프트웨어를 만드는 장벽을 낮췄지만
출시 전에 평가하고, 출시 뒤에 효과를 추적하고,
무엇을 되돌릴지 알고, 그 신호를 다음 제작으로 되돌리는 일은
여전히 병목이라고 쓴다.[^partnership]
Speedrunning Software 글도 만드는 일이 싸진 시대에는 무엇을
만들지 아는 것이 새 게임이라는 같은 논리를 편다.[^speedrun]
이 논리는 분석 회사에게 유리한 진단이다.
코드의 양이 늘수록 측정과 실험과 롤백의 수요가 늘기 때문이다.

그러나 이 진단은 맞는 면이 있다.
개별 변경이 늘면 사람이 변경마다 효과를 판단할 수 없고,
플래그와 지표가 안전판이 된다.
다만 그 안전판의 가치는 측정의 질에 달려 있고,
앞서 본 대로 사례들이 보여 주는 것은 소규모 팀의 몇 건짜리 실험이다.
수백 건의 에이전트 변경을 통계적으로 판단하는
문제는 이 페이지들이 아직 다루지 않았다.

### 화면 없는 제품에서는 좌석이 아니라 데이터와 권한 계층이 제품이 된다

모든 플랜이 무제한 좌석이고 MCP가 모든 플랜에서 되며
과금 단위가 이벤트라는 구조는 한 방향을 가리킨다.
사용자가 사람만이 아니라 에이전트가 되면 좌석 수는 의미를 잃고
수집한 이벤트와 그것을 읽는 질의가 가치의 단위가 된다.
Headless라는 이름이 그 선언이다. 화면은 선택 사항이고 데이터 계층이 제품이다.

이 전환에는 두 가지 이차 효과가 있다.
첫째, 질의는 에이전트 때문에 늘지만 과금은 수집에서 일어나므로
읽기 비용이 늘어날수록 공급자의 수익 구조가 눌린다.
요금표의 FAQ는 AI 에이전트를 무제한이라고 하면서 모든 플랜에 넣는데,
그 비용을 이벤트 과금 안에서 어떻게 감당하는지는 페이지가 설명하지 않는다.
이는 이 문서의 추정이다.
둘째, 에이전트 페이지가 말하는 고객별로 분리되어 쌓이는 에이전트 기억은
분류 체계와 함께 이탈 비용을 키운다.
기억은 이식되지 않으므로,
가격표에는 나오지 않지만 전환의 실제 비용이 될 수 있다.

### 마케팅 페이지의 증거는 의뢰, 사례, 텔레메트리의 순서로 읽어야 한다

이 두 페이지는 서로 다른 증거를 섞어 쓴다.
의뢰한 연구는 합성 조직의 모형이고,
고객 사례는 고객이 고른 성공담이고,
자체 사용 통계는 제품의 활동량이지 가치의 증거가 아니다.
활동량(주간 AI 상호작용 134만 건)은 쓰였다는
사실이지 도움이 되었다는 사실이 아니다.
증거의 강도는 모형, 선택된 사례,
활동량 순으로 약하다기보다 각각 다른 질문에 답한다.
모형은 구매 근거가 되고, 사례는 가능성을 보이며, 활동량은 도입 속도를 보여 준다.

도입을 검토하는 팀은 이 구분을 따라 자기 질문을 정해야 한다.
자기 규모에서 실험이 몇 건 가능한지(요금표의 동시 실험 한도),
에이전트가 무엇을 승인 없이 실행하는지,
이벤트 규모가 늘 때 견적이 어떻게 변하는지,
그리고 기존 데이터와 에이전트 기억을 어떻게 옮길지를 계약 전에 묻는 것이 순서다.

---

[^company]: Amplitude, [Make every release smarter than the last.](https://amplitude.com/company)

[^agent-page]: Amplitude, [Amplitude AI Agents - Agentic AI Data Analytics](https://amplitude.com/global-agent), 2026-04-20

[^pricing]: Amplitude, [Amplitude Pricing](https://amplitude.com/pricing)

[^headless]: Amplitude, [Headless Amplitude: Product Analytics in Your AI Tools](https://amplitude.com/headless)

[^experiment]: Amplitude, [Amplitude Feature Experimentation: A/B testing & Product Experimentation Platform](https://amplitude.com/amplitude-experiment)

[^fm]: Amplitude, [Feature Management powered by customer insights | Amplitude](https://amplitude.com/feature-management)

[^replay]: Amplitude, [Session Replay and Experience Analytics](https://amplitude.com/session-replay)

[^speedrun]: Amplitude, [Speedrunning Software — Amplitude EPD × AI](https://amplitude.com/3x)

[^myswimpro]: Amplitude, [MySwimPro increased experiments by 10X, boosting ARPU by 70%](https://amplitude.com/blog/myswimpro-experiment-growth), 2023-08-10

[^ticketswap]: Amplitude, [From frustration to success: Pursuing growth and optimizing buy and sell funnels with Amplitude](https://amplitude.com/blog/ticketswap-amplitude-growth-optimization), 2023-12-19

[^rocketmoney]: Amplitude, [Building trust, increasing revenue, and optimizing customer journeys at Rocket Money](https://amplitude.com/blog/rocket-money-revenue-customer-journeys), 2024-01-09

[^tei]: Amplitude, [What’s the ROI of Amplitude?](https://amplitude.com/resources/forrester-tei-report), 2024-12-02

[^wave]: Amplitude, [The Forrester Wave™: Digital Analytics Solutions, Q3 2025](https://amplitude.com/resources/forrester-wave-digital-analytics-solutions), 2025-07-29

[^security]: Amplitude, [Trust, Security and Privacy](https://amplitude.com/security-and-privacy)

[^analytics-page]: Amplitude, [Product and Web Analytics Tool](https://amplitude.com/amplitude-analytics)

[^launchdarkly]: Amplitude, [Amplitude vs. LaunchDarkly](https://amplitude.com/compare/launchdarkly)

[^partnership]: Amplitude, [Amplitude and Statsig partnership](https://amplitude.com/blog/amplitude-and-statsig-partnership), 2026-05-05

[^dantihanyi]: <https://news.ycombinator.com/item?id=48029407>

[^feeble]: <https://news.ycombinator.com/item?id=35465785>

[^redsquare]: <https://news.ycombinator.com/item?id=35467821>
