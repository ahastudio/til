# Google Workspace MCP 의무화

원문: [Google Will Make AI Agents Use Its Workspace MCP Servers. The Gmail One Can't Send Email](https://techstackups.com/articles/google-workspace-ai-agents-mcp/)

HN 토론: <https://news.ycombinator.com/item?id=50653477> (420점, 330개 댓글)

GN 토론: <https://news.hada.io/topic?id=37919>

## 요약

Tech Stackups가 정리한 글이다.
2026년 11월 24일 Google은 Workspace용 MCP 서버 여덟 개를 정식 출시하고,
API 약관에 새 조항을 추가했다.
2027년 2월 1일부터 AI 에이전트이거나 AI 에이전트가 구동하는 도구는 Gmail,
Drive, Calendar 등 Workspace에 이 MCP 서버를 통해서만 접근해야 한다.
글은 Gmail 서버가 검색, 스레드 읽기, 초안 작성, 라벨 정리는 하지만 전송, 답장,
전달, 초안 수정은 할 수 없다고 쓴다.
이 도구들은 파트너 접근이 필요하며 일반 제공이 아니라는 것이 Google 할당량
페이지의 설명이라고 한다.

글이 정리한 규칙과 제한은 다음과 같다.

| 항목           | 내용                                                                                 |
| -------------- | ------------------------------------------------------------------------------------ |
| 적용 대상      | AI 에이전트, AI 하네스, AI 모델을 쓰는 서비스가 구동하는 Workspace 접근 도구         |
| 적용 시점      | 2027년 2월 1일                                                                       |
| 직접 REST 호출 | 에이전트는 유료 등급과 무관하게 Standard 등급 할당량에 묶이고 약관 위반이 됨         |
| 비 AI 앱       | 야간 백업, CRM 동기화, 결정적 스크립트는 영향 없음                                   |
| 데이터 규칙    | 사용자가 승인한 작업에만 처리, 연동 해제 시 삭제, 임베딩 등 기술 정보 보관 30일 상한 |
| 금지           | 학습, 미세 조정, 평가, 증류, Workspace 경쟁 제품 개발                                |
| 할당량         | 프로젝트당 제품별 하루 5,000건, Gmail 검색과 초안 목록은 건당 10으로 계산            |
| 유료 등급      | 2027년 4월 1일부터 Gmail, Calendar, Drive 과금, MCP는 첫 요청부터 과금               |

서버별 범위도 다르다.
Docs, Slides, Tasks는 REST와 거의 같고,
Gmail과 Drive는 훨씬 얇다.
Drive는 이동, 이름 변경, 공유, 휴지통이 빠져 있다.
글은 Anthropic의 Google Workspace 커넥터가 전송, 답장, 전달, Drive 파일 이동을
광고한다는 점을 들어 대형 AI 업체의 에이전트는 승인된 경로로 메일을 보내고
독립 개발자의 에이전트는 초안만 남길 수 있다고 지적한다.

Google의 논거는 Cloud 블로그에서 가져온다.
유효한 OAuth 토큰이 사용자 의도를 뜻하던 시대와 달리 에이전트가 기계 속도로
행동하므로 정책 검사, 데이터 경계, 사람의 확인이 요청 경로에 있어야 한다는
것이다.
글은 여기에 실질이 있다고 인정하면서도,
같은 설계가 어떤 에이전트가 무엇을 하고 어떤 데이터를 보관하며
Google 제품과 경쟁할 수 있는지를 Google이 통제하게 만든다고 쓴다.
글은 Slack이 2025년 5월 비슷한 길을 갔다고 비교한다.

글은 대상별 대응도 제시한다.
에이전트 제품을 만드는 팀은 에이전트로 표시한 OAuth 클라이언트를 만들고
빠진 기능은 파트너 신청을 서두르라고 한다.
개인용은 오픈소스 서버가 REST로 계속 돌아가지만 약관 밖이 된다고 한다.
관리자는 Admin console의 API 컨트롤에서 에이전트 행동 범주를 막거나 승인할 수
있고,
저장된 승인은 사용자가 보거나 취소할 수 없으며 90일 뒤 만료된다고 한다.

## 분석

### 안전 논거와 사업 논거가 겹치는 지점

Google이 내세운 이유는 프롬프트 인젝션이다.
글도 받은 메일의 지시로 송장 열 건을 전달하는 위험이 문서화되어 있다고 인정한다.
그러나 전송 도구가 파트너 전용이라는 결정은 보안만으로 설명되지 않는다.
HN의 perdy는 MCP에 이미 서버가 호출을 멈추고 사용자에게 확인을 묻는 엘리시테이션
기능이 있으니 전송 도구를 거기에 걸 수 있다고 하며,
파트너 전용은 사업 결정으로 보인다고 썼다.[^perdy]
aleksiy123은 확인이 클라이언트 쪽에서 이뤄져 자동 승인을 막을 수 없다고
되받았다.[^aleksiy123]

### 자기선언이라는 분류

에이전트인지 여부는 OAuth 클라이언트의 체크박스 자기선언에서 시작한다.
글은 Google이 선언하지 않은 에이전트의 REST 호출을 어떻게 탐지할지 밝히지
않았다고 쓴다.
선언하지 않은 사용자가 처벌받을지 감지될지는 시행 방식에 달려 있다.

## 비평

### 우회 가능성

HN에서 가장 많은 공감을 받은 반응은 이 제한이 효과가 없을 것이라는 것이다.
Schnitz는 에이전트가 브라우저를 조작해 메일을 보내게 될 뿐이며 더 번거롭고
낭비가 크다고 썼다.[^Schnitz]
coffeefirst와 Zak은 Gmail이 SMTP를 지원한다고 짚었고,
macNchz는 위험은 계정이 정지되는 것이라고 답했다.[^coffeefirst][^Zak][^macNchz]
skeledrew는 사람과 에이전트가 함께 쓰는 사용자 지정 앱을 만들면 구별이 어렵다고
했고, thih9는 자동화된 행동은 감지될 수 있다고 이의를
제기했다.[^skeledrew][^thih9]
우회 가능성이 높을수록 이 정책의 효과는 선의의 개발자를 막는 데 쏠린다.

### 스팸 우려

remus는 에이전트가 현실감 있는 메일을 대량으로 만들어 스팸을 늘릴 수 있어서
제한했을 가능성을 들었다.[^remus]
rwmj는 Google이 지금까지 스팸에 크게 신경 쓰지 않았다고 비꼬았다.[^rwmj]
글 자체는 이 이유를 다루지 않는다.

### 글에서 빠진 내용

alexdobrenko는 글이 놓친 점으로 Gmail 서버가 초안은 만들 수 있다고
했다.[^alexdobrenko]
글도 본문에서 초안 작성은 가능하다고 이미 쓰고 있어,
이 지적은 글의 내용과 겹친다.
knollimar는 초안은 텍스트를 출력하는 것과 다르지 않다고 답했다.[^knollimar]

### 글의 출처와 최신성

HN의 imrehg는 이 사이트의 모든 글에 AI 에이전트 작가 Al Smith의 바이라인이 붙고
사람 편집자가 검토한다는 점을 짚었다.[^imrehg]
페이지 메타데이터에도 저자가 Ritza의 AI 에이전트 작가로 표시되어 있다.
사이트 운영자 ritzaco는 이를 좋아하지 않지만 에이전트가 여러 글을 읽어 묶는
요약형 콘텐츠에 강하고 제출 전에 본인이 읽는다고 답했다.[^ritzaco]
따라서 수치와 약관 인용은 사람이 검토한 AI 작성 글의 서술이다.
bugthe0ry는 어제까지 없던 전송 기능이 지금은 Gmail API 문서에 지원된다고
적혀 있다고 썼다.[^bugthe0ry]
글이 쓴 “Gmail 서버가 전송을 못 한다”는 시간이 지나 바뀔 수 있다.

### 영향을 받는 프로젝트

rclone 개발자 nickcw는 rclone이 Drive와 Photos용 내장 client_id를 쓰는데,
Scaled 요금제로 가려면 Google의 비용 추정기 기준 월 13만 달러가 든다고 썼다.
그렇지 않으면 할당량의 약 400배를 쓰고 있어 내장 client_id 사용자는 사실상 쓸 수
없는 수준으로 제한될 것이라고 한다.[^nickcw]
lmeyerov는 자기 데이터를 어떻게 쓸지 제한하는 것이 어떻게 합법이냐고 물었고,
WarmWash는 무료 서비스에서는 사용자가 상품이라고 답했다.[^lmeyerov][^WarmWash]

## 인사이트

### 플랫폼 의존을 줄이는 선택

k9294는 Google 인프라를 벗어나고 싶다며 대안을 물었고,[^k9294]
Fastmail의 nmjenkins는 자사의 MCP 서버가 파트너 전용 도구 없이 모두에게 열려
있고 JMAP API로 더 강력한 연결도 가능하다고 답했다.[^nmjenkins]
michaelanckaert는 사용자당 300GB 한도가 걸림돌이라고 했다.[^michaelanckaert]
spawrks는 메일 독점이 스팸을 막아 온 한편 에이전트의 발신은 제한한다는 딜레마를
물었고, ivanmontillam은 유료 소규모 사업자로 옮기라고
답했다.[^spawrks][^ivanmontillam]
이 정책이 현실이 되면 팀은 에이전트가 필요로 하는 연산이 공개된 도구 목록에
있는지부터 점검해야 한다.

---

[^imrehg]: <https://news.ycombinator.com/item?id=50654136>

[^ritzaco]: <https://news.ycombinator.com/item?id=50654233>

[^bugthe0ry]: <https://news.ycombinator.com/item?id=50663581>

[^nickcw]: <https://news.ycombinator.com/item?id=50658725>

[^lmeyerov]: <https://news.ycombinator.com/item?id=50659303>

[^WarmWash]: <https://news.ycombinator.com/item?id=50659516>

[^perdy]: <https://news.ycombinator.com/item?id=50654225>

[^aleksiy123]: <https://news.ycombinator.com/item?id=50659081>

[^Schnitz]: <https://news.ycombinator.com/item?id=50658840>

[^coffeefirst]: <https://news.ycombinator.com/item?id=50659865>

[^Zak]: <https://news.ycombinator.com/item?id=50654102>

[^macNchz]: <https://news.ycombinator.com/item?id=50654590>

[^skeledrew]: <https://news.ycombinator.com/item?id=50654452>

[^thih9]: <https://news.ycombinator.com/item?id=50654538>

[^remus]: <https://news.ycombinator.com/item?id=50654099>

[^rwmj]: <https://news.ycombinator.com/item?id=50654442>

[^alexdobrenko]: <https://news.ycombinator.com/item?id=50654443>

[^knollimar]: <https://news.ycombinator.com/item?id=50660815>

[^k9294]: <https://news.ycombinator.com/item?id=50654039>

[^nmjenkins]: <https://news.ycombinator.com/item?id=50654101>

[^michaelanckaert]: <https://news.ycombinator.com/item?id=50654416>

[^spawrks]: <https://news.ycombinator.com/item?id=50656512>

[^ivanmontillam]: <https://news.ycombinator.com/item?id=50658589>
