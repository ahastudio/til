# Max·Team 월간 API 크레딧: 구독에 붙은 API 잔액과 그 경계

원문: [Monthly API credits for Max and Team plans | Claude Help Center](https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-and-team-plans)

HN 토론: <https://news.ycombinator.com/item?id=49997205> (11점, 0개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=49997654> (4점, 6개 댓글)

## 소개

Claude Max와 Team 구독에 매달 Claude Platform에서 쓸 API 크레딧이 붙는다.
Claude Help Center의 이 도움말은 2026년 10월 7일에 갱신되었고,
누가 받을 수 있는지, 어떻게 받는지, 어디에 쓰이는지,
다 쓰면 어떻게 되는지를 정리한다.
같은 날 나온 Claude Haiku 5.5 발표문은 이 크레딧을
사용자가 API를 호출하는 도구, 앱, 에이전트를 실험해 보게 하려는 것이라고
소개했다.

이 크레딧이 약속하는 것은 Console 조직 하나에 매달 들어오는 잔액이다.
약속하지 않는 것도 분명하다.
구독의 사용 한도를 늘려 주지 않고, 대화형 Claude Code에는 쓰이지 않으며,
이월되지 않는다.
Free, Pro, Enterprise 플랜은 대상이 아니다.

이 문서는 도움말의 규칙을 정리하고,
그 규칙이 실제 사용에서 어떤 결정을 요구하는지,
그리고 같은 날 관련 안내문이 어떻게 바뀌었는지를 다룬다.

## 동작 방식

### 플랜별 금액

| 플랜                                   | 월간 크레딧                         |
| -------------------------------------- | ----------------------------------- |
| Max 5x                                 | $100                                |
| Max 20x                                | $200                                |
| Team (Standard 좌석)                   | 좌석당 $20                          |
| Team (Premium 좌석)                    | 좌석당 $100                         |
| 할인 Team 플랜 (Nonprofit, Scientists) | Standard $20, Premium $100 (좌석당) |

Team은 모든 좌석의 크레딧을 하나의 월간 잔액으로 합치며, 상한은 $500이다.
도움말의 예에서 Standard 3석과 Premium 2석인 팀은 매달 $260을 받고,
Premium 1석을 더하면 다음 주기부터 $360이 된다.
합계는 크레딧이 들어오는 시점의 좌석 수로 매번 다시 계산된다.

Claude 요금 페이지와 대조하면 Team의 좌석당 크레딧은
연간 결제 기준 좌석 요금과 같은 금액이다.
Standard 좌석은 연간 결제 시 월 $20, Premium 좌석은 월 $100이다.
Max도 요금 페이지에 월 $100부터라고 적혀 있어, Max 5x의 크레딧은 구독료와 같다.

### 쓰이는 곳과 쓰이지 않는 곳

크레딧은 Claude Platform의 모든 모델에 쓸 수 있다.
도움말이 꼽는 사용처는 다음과 같다.

- Claude API(Messages API와 Message Batches API)
- Claude Console의 Playground
- Claude Managed Agents
- Claude Agent SDK

다음에는 쓰이지 않는다.

- 터미널, IDE, 데스크톱, 웹의 대화형 Claude Code
- Claude, Claude Code, Claude Cowork의 추가 사용량(extra usage)
- Amazon Bedrock, Google Cloud Vertex AI, Microsoft Foundry의 Claude

경계가 가장 미묘한 것은 `claude -p`다.
연결한 Console 조직의 API 키로 직접 실행하면 Agent SDK 사용으로 과금되므로
크레딧이 쓰인다.
같은 `claude -p`라도 Claude 플랜으로 로그인한 상태라면
플랜의 사용 한도에서 빠지고 크레딧은 쓰이지 않는다.
Claude Code GitHub Action, IDE 확장, Claude 데스크톱 앱이 시작한 실행은
`-p`를 쓰더라도 Claude Code 사용으로 집계되어 크레딧 대상이 아니다.
즉 어떤 명령을 쓰느냐가 아니라 어떤 자격 증명으로, 무엇이 실행하느냐가 기준이다.

### 주기와 차감 순서

- 플랜 결제가 처리된 직후 결제 주기마다 새로 들어온다.
  연간 플랜도 크레딧은 매달 들어온다.
- 이월되지 않는다.
  쓰지 않은 크레딧은 결제 주기가 끝나면 사라진다.
- 구매한 크레딧보다 먼저 쓰인다.
- 연결한 조직에서 API 키를 가진 모든 사람이 같은 잔액을 쓴다.
- Claude, Claude Code, Claude Cowork의 사용 한도와는 무관하다.
- Console의 Settings > Billing에서 금액과 만료일을 볼 수 있다.

차감 순서는 구매 크레딧의 약관과 맞물린다.
Anthropic의 Supplemental Credit Terms에 따르면 구매한 Usage Credits는
발급일로부터 1년 뒤에 만료되고, 환불되지 않으며, 계정을 닫으면 함께 사라진다.
월간 크레딧이 먼저 쓰이므로, 한 달 안에 사라질 돈을 먼저 쓰고
1년짜리 잔액은 아껴 두는 순서다.

### 다 쓰면

- 조직에 구매한 크레딧이나 자동 충전(auto-reload)이 있으면 그쪽에서 이어서 쓴다.
- 다른 크레딧이 없으면 다음 달 크레딧이 들어올 때까지 API 요청이 멈춘다.
  사용량이 Claude 플랜 요금에 청구되는 일은 없다.
- Anthropic 영업팀을 통해 청구서로 결제하는 조직은 초과분이 평소대로 청구된다.

크레딧을 받는 데 Console에 카드를 등록할 필요는 없다.
카드가 없는 조직에서는 크레딧이 곧 지출 상한이고,
자동 충전을 켠 조직에서는 크레딧이 첫 구간일 뿐 상한이 아니다.

### 플랜이 바뀌면

- 해지, 대상이 아닌 플랜으로 내려감, 환불: 새 크레딧이 끊긴다.
  이미 받은 크레딧은 만료 전까지 쓸 수 있다.
- Max 5x에서 Max 20x로 올림: 남은 기간만큼 비례한 크레딧을 바로 받고,
  다음 주기부터 매달 $200을 받는다.
- Max에서 Team으로 옮김: Max의 연결이 끝난다.
  Team 플랜이 7일 동안 유지된 뒤 Team Owner나 Primary Owner가 다시 청구할 수 있다.

## 받는 방법

자격 조건은 네 가지다.
구독이 활성 상태여야 하고, 대상 플랜을 7일 이상 유지해야 하며,
iOS나 Android에서 구독했더라도 청구는 웹 브라우저의 claude.ai에서 해야 한다.
Console에 결제 수단을 등록할 필요는 없다.

역할도 양쪽에서 맞아야 한다.

| 위치         | 필요한 역할                                     |
| ------------ | ----------------------------------------------- |
| Claude 플랜  | Max는 구독자 본인, Team은 Primary Owner나 Owner |
| Console 조직 | Owner, Admin, Billing 중 하나                   |

청구 절차는 다음과 같다.

1. claude.ai에서 Max 구독자는 Settings > Billing,
   Team Owner나 Primary Owner는 Organization settings > Billing으로 간다.
2. API credits 항목에서 Link organization을 고른다.
3. 크레딧을 받을 Console 조직을 고르거나 새로 만든다.
4. Supplemental Credit Terms를 확인하고 Link organization을 누른다.

연결은 한 조직에만 할 수 있고,
한 Console 조직도 한 플랜에서만 크레딧을 받을 수 있다.
연결한 조직은 사용자가 직접 바꿀 수 없고 지원팀에 요청해야 한다.
도움말은 claude.ai와 같은 이메일로 Console에 로그인하라고 권하고,
연결 중 오류가 나면 몇 시간 뒤 다시 시도하라고 적는다.

Team에서는 소유자 한 명이 팀 전체의 크레딧을 한 번에 청구한다.
연결한 조직의 API 키를 가진 사람은 누구나 이 잔액을 쓸 수 있으므로,
프로젝트나 팀원별로 제한하려면 Console에서 워크스페이스 지출 한도를 걸어야 한다.

## 트레이드오프

### 연결할 조직을 고르는 일은 사실상 되돌릴 수 없다

연결할 Console 조직은 한 번 고르면 사용자가 바꿀 수 없다.
그래서 이미 쓰고 있는 회사 조직에 연결할지,
크레딧 전용 조직을 새로 만들지를 먼저 정해야 한다.

기존 조직에 연결하면 크레딧이 구매 크레딧보다 먼저 차감되므로
실제 운영 트래픽이 매달 첫 $100이나 $200을 자동으로 소진한다.
청구서의 금액은 줄지만, 실험에 쓰라는 돈이 실험에 쓰이지 않는다.
반대로 전용 조직을 만들면 실험과 운영이 깔끔하게 나뉘지만,
API 키, 워크스페이스, 지출 한도 같은 설정을 하나 더 관리해야 한다.

개인 Max 구독자가 회사 Console 조직에 연결하는 경우는 더 조심해야 한다.
Console 조직에서 Owner, Admin, Billing 역할이면 연결할 수 있으므로
기술적으로는 가능하지만,
연결을 바꾸려면 지원팀을 거쳐야 하고 한 조직은 한 플랜에서만 크레딧을 받는다.
퇴사나 팀 이동처럼 사람과 조직의 관계가 바뀌는 상황을 도움말은 다루지 않는다.

### 공유 잔액은 키 관리의 문제를 키운다

연결한 조직의 API 키를 가진 모든 사람이 같은 잔액에서 쓴다.
Team에서는 이것이 의도된 설계이지만,
키 하나가 새어 나가면 팀 전체의 그달 크레딧이 한꺼번에 사라질 수 있다.
카드가 없는 조직이라면 피해는 그 달의 잔액에서 멈추지만,
자동 충전을 켠 조직이라면 크레딧이 바닥난 뒤에도 결제 수단에서 계속 빠져나간다.

워크스페이스 지출 한도는 이 문제를 나누는 도구이지
없애는 도구는 아니다.
한도를 프로젝트별로 걸면 한 곳의 사고가 다른 곳으로 번지지 않지만,
한도가 걸린 워크스페이스 안에서는 여전히 잔액을 공유한다.

### 구독 한도와 API 크레딧 중 어느 쪽으로 돌릴지 정해야 한다

`claude -p`와 Agent SDK는 이제 두 가지 방식으로 돌릴 수 있다.
Claude 플랜으로 로그인하면 구독의 사용 한도를 쓰고,
연결한 조직의 API 키로 실행하면 API 크레딧을 쓴다.
같은 스크립트라도 환경에 어느 자격 증명이 잡혀 있느냐에 따라 청구처가 달라진다.

구독 한도는 대화형 Claude Code와 공유되므로,
배치 작업을 구독으로 돌리면 낮에 쓸 대화형 한도가 줄어든다.
API 크레딧으로 돌리면 대화형 한도는 지켜지지만,
월 $100이나 $200이라는 금액 상한이 생기고 모델별 API 단가가 그대로 적용된다.
HN에서 0gs는 구독 한도로 도는 오케스트레이터가 API 에이전트 여러 개를 띄우는
구성을 예로 들며, 이 크레딧이 이미 쓰던 절약 방식을 더 장려하는
공짜 돈 같다고 했다.[^0gs]

어느 모델로 돌리느냐가 이 계산을 크게 바꾼다.
Haiku 5.5는 프롬프트 10만 토큰 이하에서 입력 100만 토큰당 $0.10이므로
$100이면 입력 10억 토큰이고,
입력 100만 토큰당 $2인 Sonnet 5.5로는 5천만 토큰이다.
이 환산은 이 문서의 계산이며 출력 토큰과 캐시 비용은 빼고 셈한 값이다.

같은 금액이라도 두 쪽의 값어치는 다르다는 지적도 나왔다.
vmg12가 이 크레딧은 API 토큰이라 어떤 하네스로든 사업을 만들 수 있다고 하자,
tekacs는 그 토큰이 같은 금액의 구독 사용량보다
훨씬 값어치가 낮다고 답했다.[^tekacs]
usef-는 $20 구독이 API 가격으로 환산해
$500어치가 넘는 토큰을 준다고 주장했다.[^usef-]
이 배율은 댓글의 주장일 뿐 이 문서가 확인한 값은 아니다.
그러나 방향이 맞다면, 구독 한도로 돌릴 수 있는 일을 크레딧으로 옮기는 것은
같은 일을 더 비싼 단가로 치르는 선택이 된다.
크레딧은 구독 한도로는 할 수 없는 일,
즉 자기 앱의 사용자에게 응답하는 일이나
다른 하네스에서 키로 부르는 일에 쓸 때 값을 한다.

## 함정

### 크레딧이 보이지 않는다고 대상이 아닌 것은 아니다

도움말은 크레딧을 며칠에 걸쳐 순차 배포한다고 적는다.
대상 플랜을 7일 유지해야 제안이 나타나므로,
새로 가입했거나 Max에서 Team으로 옮긴 사용자는 한동안 보지 못한다.
HN에서도 출시 당일 ChickadeeBandit이
API 크레딧 항목이 보이지 않는다고 물었다.[^ChickadeeBandit]
7일이 지났는데도 보이지 않으면 플랜과 역할을 확인하고,
그래도 안 되면 지원팀에 문의하라는 것이 도움말의 안내다.

### `ANTHROPIC_API_KEY`가 청구처를 바꾼다

Claude Code 도움말에 따르면 `ANTHROPIC_API_KEY` 환경 변수가 설정되어 있으면
Claude Code는 구독 대신 그 API 키로 인증하고 API 요금으로 청구한다.
연결한 조직의 키를 셸에 넣어 두고 `claude -p`를 돌리면 의도대로 크레딧이 쓰인다.
그러나 같은 셸에서 대화형 Claude Code를 열면
대화형 사용은 크레딧 대상이 아니라고 도움말이 적고 있으므로,
그 사용량은 크레딧이 아닌 다른 경로로 청구될 것으로 보인다.
도움말은 이 경우 어느 잔액에서 빠지는지를 적지 않았고,
이 문서는 그 동작을 직접 확인하지 않았다.
배치용 키는 그 작업에만 주입하고 셸 전역에 두지 않는 편이 안전하다.

### 자동 충전을 켜 두면 크레딧은 상한이 아니다

도움말은 크레딧이 떨어지면 요청이 멈춘다고 하지만,
그것은 조직에 다른 크레딧도 자동 충전도 없을 때의 이야기다.
기존 회사 조직에 연결했고 그 조직이 자동 충전을 쓰고 있다면,
크레딧을 다 쓴 순간 아무 경고 없이 유료 사용으로 넘어간다.
“공짜 $100” 안에서만 실험하려면 자동 충전이 꺼진 조직에 연결해야 한다.

### Bedrock, Vertex AI, Foundry를 쓰는 팀에는 쓸모가 줄어든다

크레딧은 Claude Platform 안에서만 쓰인다.
회사의 운영 트래픽이 Amazon Bedrock이나 Google Cloud Vertex AI를 거친다면,
크레딧으로 만든 실험은 운영 경로와 다른 엔드포인트, 다른 모델 식별자,
다른 기능 지원 범위에서 돌아간다.
실험에서 확인한 동작을 운영 경로에서 다시 확인해야 한다.

### 크레딧은 팔거나 넘길 수 없다

Topfi는 이 $200을 API로 마음대로 쓰고 되팔 수도 있느냐고 물으며,
약관은 합리적으로 보인다고 Supplemental Credit Terms를 링크했다.[^Topfi]
그 약관에는 크레딧을 다른 사람이나 단체에 넘기거나 팔 수 없고,
크레딧이 연결된 계정의 보유자만 쓸 수 있다고 적혀 있다.
크레딧으로 만든 앱이 자기 사용자에게 응답하는 데 쓰는 것과,
크레딧이 든 조직이나 키를 남에게 넘기는 것은 다른 일이다.
앞의 경우가 어디까지 허용되는지는 도움말도 약관도 따로 다루지 않으므로,
크레딧을 상용 서비스의 원가로 계산하기 전에 이용 약관 전체를 확인해야 한다.
이 구분은 이 문서의 해석이다.

### Team 크레딧은 좌석이 늘어도 $500에서 멈춘다

풀 상한이 $500이므로 Premium 5석이나 Standard 25석이면 상한에 닿는다.
도움말의 범위 안에서 계산하면, Standard 좌석만 100석인 팀도 매달 $500을 받아
좌석당으로는 $5가 된다.
작은 팀에는 좌석 요금만큼의 크레딧이지만,
큰 팀에서는 팀 전체가 쓰는 공용 실험 예산 정도로 보는 것이 맞다.

## 비평

### 같은 날 두 번 바뀐 안내문이 경계를 흐렸다

이 크레딧은 6월에 철회된 변경의 그림자 안에서 발표되었다.
Agent SDK 도움말에는 6월 15일 자로,
Agent SDK, `claude -p`, 서드파티 앱 사용에 대해 예고했던 변경을 멈추고
당분간 구독 한도에서 계속 빠진다는 안내가 붙어 있었다.
nullishdomain이 인용한 10월 6일 보관본에는 그 변경과 함께 주기로 했던
월간 크레딧도 제공하지 않는다는 문장이 있었다.[^nullishdomain]

10월 7일 Agent SDK 도움말의 첫 갱신 문구는 HN 글 본문에 그대로 남아 있다.
6월에 발표한 Agent SDK 월간 크레딧은 더는 제공하지 않으며,
Max와 Team의 월간 API 크레딧을 Console 조직에 받아
그 조직의 API 키로 쓰라는 내용이었다.
이 문구는 구독으로 Agent SDK를 쓰는 길이 막혔다는 뜻으로 읽혔다.
thepasch는 6월에 반발로 물러섰던 변경을
모델 출시와 함께 몰래 들여온 것이라고 했고,[^thepasch]
Paseo로 Claude Code를 돌리던 InsideOutSanta는
일이 훨씬 복잡해졌다고 했다.[^InsideOutSanta]
nr378은 해당 페이지가 내려갔다며 구독으로 Agent SDK를 쓰는 길을
곧 끊으려는 신호라고 보았다.[^nr378]

같은 시각 실제 동작은 바뀌지 않았다.
eli는 Agent SDK를 직접 시험해 보니 아직 아무것도 바뀌지 않았다며,
요금 방식이 바뀐다는 해석은 추측이라고 반박했다.[^eli]
ziga도 `claude -p`가 아직 이 API 크레딧에서 빠지지 않는다고 적으면서,
다음 차례로 그렇게 될 것 같다고 덧붙였다.[^ziga]
문서가 먼저 바뀌고 동작은 그대로였던 셈이라,
사용자들은 문서와 동작 중 어느 쪽을 믿어야 할지 알 수 없었다.

몇 시간 뒤 문구는 다시 바뀌었다.
cjav_dev는 API 크레딧을 `claude -p`에 어떻게 쓰는지 분명히 하도록
문서를 고쳤다고 답했고,[^cjav_dev]
luketaylor는 오해를 부른 문구를 사과하며,
Agent SDK를 여전히 구독으로 쓸 수 있다고 고쳤다고 적었다.[^luketaylor]
nullishdomain도 구독 한도로 계속 쓸 수 있다는 문장이
새로 들어갔다고 확인했다.[^nullishdomain-2]
eli도 구독 청구를 확인해 주던 예전 안내가 다시 나타났다고 적었다.[^eli-2]
지금 Agent SDK 도움말에는 10월 7일 자와 6월 15일 자 안내 두 문단만 남아 있고,
Agent SDK, `claude -p`, 서드파티 앱을 구독 한도로 계속 쓸 수 있다고 적는다.

문구는 바로잡혔지만, 이 도움말만 읽어서는 그 경계를 알 수 없다는 문제는 남는다.
6월의 Agent SDK 크레딧과 같은 것이냐는 질문에 도움말은 아니라고만 답하고
그 크레딧은 제공되지 않는다고 적는다.
그런데 6월의 크레딧이 무엇을 대가로 주기로 했던 것인지,
즉 구독에서 Agent SDK 사용을 떼어 내는 변경이 지금 어떤 상태인지는
이 도움말이 아니라 다른 도움말을 찾아 읽어야 알 수 있다.
그 다른 도움말도 아직 “당분간”이라는 6월의 표현을 지우지 않았다.
luketaylor는 이번 변경으로 없어지는 것이
아무것도 없다고 답했지만,[^luketaylor-2]
winwang은 지금은 그렇다는 것일 뿐이라며,
선의로 보이는 혜택이 사실은 재배분이라면 나중의 축소를
여전히 기준보다 많다는 말로 설명할 수 있게 된다고 했다.[^winwang]
Tadpole9181은 SDK와 `-p`에 맞춰 작업 흐름을 막 고쳤는데
다시 처음부터 해야 한다며,
제발 방침을 정해 달라고 했다.[^Tadpole9181]

### 크레딧은 경계를 넓혔지만 구독을 다른 하네스에서 쓰게 해 주지는 않는다

크레딧을 반긴 반응 가운데 일부는
이것을 구독을 다른 도구에서 쓸 수 있게 된 것으로 받아들였다.
HN에서 그렇게 읽은 댓글에 neucoas는 다른 하네스에서 Claude 모델을 쓰는 것은
원래 API로는 늘 가능했고 구독으로만 안 됐을 뿐이라고 정리했다.[^neucoas]
이제 opencode나 Pi에서 쓸 $100어치 API 토큰을 받게 된 것이니 나아지기는 했지만,
구독 자체를 Pi에서 문제없이 쓰게 해 주는 OpenAI와 같지는 않다는 것이다.

Topfi는 두 회사의 방식을 다르게 정리했다.[^Topfi]
OpenAI가 발표한 Sign in with OpenAI는
서비스 사용자가 자기 구독 토큰을 들고 오는 방식이라
사용자에게는 쌀 수 있지만 서비스를 만드는 쪽은 모델을 바꾸기 어렵다.
Anthropic의 크레딧은 개발자가 할당량을 자기 사용자에게 마음대로 쓰고,
다 쓰면 다른 모델로 넘어갈 수 있어 개발자 쪽의 종속이 덜하다는 것이다.
같은 문제, 즉 구독자의 토큰을 다른 도구로 내보내는 문제를
한쪽은 사용자 쪽에서, 다른 쪽은 개발자 쪽에서 푼 셈이다.
notatoad는 도구와 앱과 에이전트를 실험하게 하려는 것이라는 발표문의 설명을 두고,
그냥 개발자가 API 위에서 만들게 하려는 무료 체험이라고 했다.[^notatoad]

도움말의 규칙도 이 해석과 맞는다.
크레딧은 구독의 사용 한도를 바꾸지 않고, 대화형 Claude Code에는 쓰이지 않으며,
구독 한도가 끝난 뒤의 추가 사용량에도 쓰이지 않는다.
구독과 API는 여전히 별개의 상품이고,
크레딧은 그 사이에 매달 일정 금액만큼의 다리를 놓은 것이다.
theGeatZhopa가 Max 플랜과 API 크레딧을 함께 쓰면서 플랜의 토큰은 그대로 둘 수
있느냐고 물은 것도
이 경계가 처음에 얼마나 헷갈렸는지를 보여 준다.[^theGeatZhopa]
도움말에 따르면 답은 그렇다는 것이다.
API 크레딧은 플랜의 사용 한도와 무관하게 따로 차감된다.

## 확인하기

크레딧이 들어왔는지는 Console의 Settings > Billing에서 금액과 만료일로 확인한다.
연결한 조직의 API 키로 요청이 실제로 나가는지는 짧은 요청 하나로 확인할 수 있다.

```bash
# LINKED_ORG_KEY: 연결한 Console 조직에서 만든 API 키.
# ANTHROPIC_API_KEY로 셸 전역에 export하면 대화형 Claude Code의 청구처까지 바뀐다.
curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $LINKED_ORG_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-haiku-5-5",
    "max_tokens": 64,
    "messages": [{"role": "user", "content": "ping"}]
  }'
```

요청을 보낸 뒤 Console의 사용량 화면과 잔액이 함께 움직이는지 본다.
`claude -p`를 크레딧으로 돌리려는 경우에도
같은 방식으로 키를 그 명령에만 넘기고,
Claude 플랜으로 로그인된 상태에서 돌리면 크레딧이 아니라 구독 한도에서 빠진다는
점을 기억한다.

## 체크리스트

- 대상 플랜(Max 5x, Max 20x, Team)을 7일 이상 유지했는가?
- Claude 플랜과 Console 조직 양쪽에서 필요한 역할을 갖고 있는가?
- 연결할 조직이 실험 전용인지 운영 조직인지 정했는가?
- 연결할 조직의 자동 충전 설정을 확인했는가?
- Team이라면 워크스페이스 지출 한도를 걸었는가?
- 크레딧용 API 키를 셸 전역이 아니라 해당 작업에만 넘기는가?
- 운영 트래픽이 Bedrock, Vertex AI, Foundry라면 실험 결과를 그 경로에서 다시 확인할 계획이 있는가?
- 매달 결제 주기가 끝나기 전에 남은 잔액과 만료일을 확인하는가?

## 기억할 원칙

### 청구처는 명령이 아니라 자격 증명이 정한다

이 도움말에서 가장 오래 남을 규칙은 `claude -p`에 대한 답이다.
같은 명령이 API 키로 실행되면 크레딧을,
플랜 로그인으로 실행되면 구독 한도를 쓰고,
GitHub Action이나 IDE가 실행하면 둘 다 아닌 Claude Code 사용이 된다.
무엇이 어디에 청구되는지 알려면 명령을 볼 것이 아니라
그 실행에 어떤 자격 증명이 잡혀 있는지를 봐야 한다.

### 매달 사라지는 돈은 지출 순서를 바꾼다

이월되지 않는 크레딧이 구매 크레딧보다 먼저 쓰인다는 규칙은
사용자에게 유리하지만,
운영 조직에 연결하면 그 돈은 의도와 달리 운영 트래픽이 먼저 가져간다.
공짜 잔액이 어떤 일에 쓰이게 할지는 어느 조직에 연결하느냐로 정해지고,
그 선택은 직접 되돌릴 수 없다.

---

[^0gs]: <https://news.ycombinator.com/item?id=49996696>

[^ChickadeeBandit]: <https://news.ycombinator.com/item?id=49998693>

[^nullishdomain]: <https://news.ycombinator.com/item?id=49998209>

[^thepasch]: <https://news.ycombinator.com/item?id=49996942>

[^InsideOutSanta]: <https://news.ycombinator.com/item?id=49997034>

[^nr378]: <https://news.ycombinator.com/item?id=49999227>

[^cjav_dev]: <https://news.ycombinator.com/item?id=49999509>

[^luketaylor]: <https://news.ycombinator.com/item?id=49999718>

[^nullishdomain-2]: <https://news.ycombinator.com/item?id=49999753>

[^Tadpole9181]: <https://news.ycombinator.com/item?id=49998983>

[^neucoas]: <https://news.ycombinator.com/item?id=49998441>

[^theGeatZhopa]: <https://news.ycombinator.com/item?id=49998482>

[^tekacs]: <https://news.ycombinator.com/item?id=49998422>

[^usef-]: <https://news.ycombinator.com/item?id=49998368>

[^Topfi]: <https://news.ycombinator.com/item?id=49997354>

[^eli]: <https://news.ycombinator.com/item?id=49998104>

[^ziga]: <https://news.ycombinator.com/item?id=49998069>

[^eli-2]: <https://news.ycombinator.com/item?id=50000752>

[^winwang]: <https://news.ycombinator.com/item?id=49999340>

[^notatoad]: <https://news.ycombinator.com/item?id=50001452>

[^luketaylor-2]: <https://news.ycombinator.com/item?id=49999240>
