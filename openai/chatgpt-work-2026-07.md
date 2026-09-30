# ChatGPT Work 출시: Codex가 ChatGPT가 되고 ChatGPT가 Classic이 된 날

원문: [ChatGPT is now a partner for your most ambitious work | OpenAI](https://openai.com/index/chatgpt-for-your-most-ambitious-work/)

HN 토론: <https://news.ycombinator.com/item?id=48849059> (353점, 190개 댓글)

GN 토론: <https://news.hada.io/topic?id=31281>

## 요약

OpenAI가 2026년 7월 9일 ChatGPT Work를 발표했다.
ChatGPT Work는 앱과 파일을 오가며 행동하고, 필요하면 몇 시간씩 한 프로젝트에 붙어 있으며, 목표를 완성된 결과물로 바꾸는 ChatGPT 안의 에이전트라고 소개된다.
여러 앱과 작업 흐름에서 정보를 모아 시트, 슬라이드, 문서, 웹 앱 같은 완성물을 만들고, 복잡한 프로젝트를 작은 단계로 나눠 스스로 끝낸다는 것이다.

발표의 근거는 Codex다.
Codex 기술이 내장되어 ChatGPT가 질문에 답하는 것을 넘어 실제 일을 하게 되었다고 말한다.
Codex를 매주 쓰는 사람은 500만 명이 넘고, 원래 개발자용 코딩 에이전트였지만 100만 명 넘게 소프트웨어 개발 밖의 일에 쓰고 있다는 숫자가 제시된다.
ChatGPT Work는 같은 날 출시된 GPT-5.6으로 돌아가고, OpenAI는 이 모델이 여러 단계의 작업을 추론하고 템플릿과 참고 파일을 따르는 결과물을 만드는 데서 최첨단이라고 쓴다.
OpenAI 내부에서는 재무와 영업을 포함한 거의 100%의 팀이 ChatGPT Work와 Codex를 쓰고 있으며, 영업에서는 몇 주 걸리던 개념 증명을 24시간 안에, 재무에서는 월말 결산과 예측을 며칠에서 몇 시간으로 줄였다고 한다.

기능 묶음은 넷이다.
플러그인은 Slack, Microsoft Teams, Google Drive, SharePoint, 이메일, 캘린더, CRM, 프로젝트 관리 도구를 연결하고, 프롬프트에 따라 알아서 참조하거나 `@`와 앱 이름으로 직접 부를 수 있으며, 새 통합 플러그인 디렉터리로 한곳에 모인다.
Sites는 공개 베타로, 작업과 아이디어를 대화형 사이트나 웹 앱으로 바꿔 팀이나 URL로 공유하게 한다.
Scheduled Tasks는 한 번, 일정에 따라, 이벤트가 생길 때, 또는 변화를 감시하며 행동한다.
데스크톱에서는 내장 브라우저가 웹의 정보와 도구와 온라인 파일을 가져오고, Computer Use가 사용자의 컴퓨터에서 클릭하고 입력하고 파일을 옮기며 배경에서 작업한다.

발표에는 제품 구조의 큰 변화가 함께 들어 있다.
그날부터 Codex 앱이 새 ChatGPT 데스크톱 앱으로 합쳐졌다.
Codex 앱을 쓰던 사람은 평소처럼 업데이트하면 새 ChatGPT 데스크톱 앱이 되고, 기존 ChatGPT 데스크톱 앱은 ChatGPT Classic으로 이름이 바뀐다.
개발자는 앱을 열 때 Codex 화면을 기본으로 하고 앱 아이콘을 Codex 로고로 고를 수 있다.
Chrome 확장 프로그램은 Chrome 사이드바에서 ChatGPT를 쓰게 바뀌고, OpenAI는 Atlas에서 배운 것을 바탕으로 한다며 독립 Atlas 브라우저를 단계적으로 종료하겠다고 밝혔다.

조직용 통제도 있다.
Enterprise와 Edu 관리자는 누가 접근하는지, 어떤 회사 맥락을 쓸 수 있는지, 어떤 도구에 연결하고 어떤 행동을 할 수 있는지를 관리하고, Compliance API로 ChatGPT Work의 대화와 행동을 대규모로 볼 수 있다.
Auto-review는 가장 발전된 모델로 연결된 도구와 API가 관련된 중요한 행동을 실행 전에 검토해 민감한 정보의 무단 공유를 막는다.
ChatGPT Work는 웹과 모바일에서 Pro, Enterprise, Edu부터 배포되고 며칠 안에 Plus와 Business로 넓어지며, 새 데스크톱 앱은 Free를 포함한 모든 요금제에서 Chat, Work, Codex를 쓸 수 있다.
사용량은 일반 채팅과 다르게 작업량에 따라 달라지고 Codex와 같은 사용량 구조를 따르며, 관리자는 작업 공간 기본값, 그룹 한도, 개인별 예외로 지출을 통제할 수 있다.

## 분석

### 발표의 실체는 기능이 아니라 제품의 재배치다

기능만 보면 이 발표는 이미 있던 것들의 묶음이다.
HN에서 wahnfrieden은 능력은 몇 달 전에 나왔고, 이것은 ChatGPT 앱을 은퇴시키고 일반 사용자를 위한 Codex로 바꾸는 일일 뿐이라고 적었다.[^wahnfrieden]
paxys도 이름을 바꾸고 코딩 밖의 일로 넓힌 것이라고 요약했다.[^paxys]

실제로 가장 큰 변화는 어떤 앱이 ChatGPT라는 이름을 갖느냐였다.
simonw는 macOS Codex 데스크톱 앱에서 업그레이드를 누르자 ChatGPT라는 새 이름으로 다시 실행되었고, 기존 ChatGPT 앱은 ChatGPT Classic이 되었다고 보고했다.[^simonw]
ChatGPT라는 브랜드가 대화형 챗봇에서 에이전트 작업 도구로 옮겨 간 것이다.

이 재배치는 OpenAI가 무엇을 주력으로 보는지 보여 준다.
사람들이 AI를 처음 만난 채팅 화면은 Classic이 되었고, 코딩 에이전트에서 자란 작업 도구가 그 이름을 이어받았다.
hobofan은 OpenAI가 LLM의 주 인터페이스로 채팅을 개척했고 평범한 사용자에게 가장 강한 브랜드와 방어력이 거기에 있는데, 동시에 여러 방식으로 채팅에서 벗어나려 한다는 점이 흥미롭다고 적었다.[^hobofan]

### 코딩 에이전트의 하네스가 지식 노동의 하네스가 된다

발표의 논리는 Codex에서 출발한다.
코딩 에이전트로 시작했지만 100만 명 넘게 코딩 밖의 일에 쓰고 있다는 숫자는, 같은 하네스가 코드가 아닌 일에도 통한다는 증거로 제시된다.
그래서 ChatGPT Work는 새 에이전트라기보다 Codex의 하네스에 사무 작업용 플러그인과 결과물 형식을 붙인 것에 가깝다.

HN 사용자들도 이것을 확인했다.
smoe는 Work와 Codex를 전환해도 로컬·원격, 브랜치, 워크트리 컨트롤이 사라지고 오피스 도구 플러그인이 보이는 정도의 차이만 있다며, 아마 배경의 시스템 프롬프트가 바뀌는 것 같다고 추측했다.[^smoe]
neil_s는 Work와 Codex 사이의 전환이 같은 하네스를 쓰면서 기술적 출력의 장황함만 조금 바꾸는 것 같다고 적었다.[^neil_s]
aniviacat은 Plus 사용자로서 Chat 탭에서는 최대 추론 강도가 High인데 Work 탭에서는 Extra High와 Max까지 고를 수 있다는 차이를 찾아냈다.[^aniviacat]

이것은 에이전트 제품의 공통 흐름이다.
Anthropic의 Cowork도 Claude Code의 에이전트 방식을 지식 노동에 옮긴 것이라고 스스로 설명한다.
코딩은 에이전트가 가장 먼저 쓸모를 증명한 영역이었고, 그 하네스가 파일과 도구를 다루는 일반적인 방식으로 굳어지고 있다.

### 조직 통제가 발표의 한 축을 차지한다

발표의 뒷부분은 개인 사용자가 아니라 관리자에게 말한다.
누가 무엇에 접근하는지, 어떤 행동을 할 수 있는지, 대화와 행동을 어떻게 감사하는지, 지출을 어떻게 나누는지다.
관리자가 작업 공간 기본값과 그룹 한도와 개인별 예외를 두고, 추가 크레딧 요청을 프로젝트 설명과 근거와 함께 검토한다는 대목은 거의 조달 절차 설명처럼 읽힌다.

이 비중은 ChatGPT Work가 누구에게 팔리는지 보여 준다.
사용량이 작업량에 따라 달라지고 Codex와 같은 구조를 따른다는 것은, 무제한에 가까운 채팅과 달리 이 제품이 쓰는 만큼 비용이 드는 도구라는 뜻이다.
그 비용을 통제할 수단이 있어야 기업이 대규모로 들일 수 있다.

## 비평

### 통합이 사용자에게 준 것은 단순함이 아니라 혼란이었다

HN 스레드의 첫 댓글이 이 출시의 성격을 가장 잘 요약한다.
postalcoder는 설치했더니 매우 혼란스럽다며, 컴퓨터에서 Codex 앱이 사라지고 ChatGPT가 Codex가 되었는데 그렇다면 ChatGPT는 어디로 갔고 가볍게 대화하려면 어디로 가야 하느냐고 물었다.[^postalcoder]
그리고 ChatGPT Work와 ChatGPT Codex를 전환해도 아무것도 바뀌지 않는다고 덧붙였다.

GMoromisato는 이것을 UI의 본래 역할로 설명했다.[^GMoromisato]
UI는 사용자가 뒤에서 무슨 일이 일어나는지 멘탈 모델을 세우게 도와야 하는데, 기존 세션에서 Work와 Codex를 바꿔도 아무 일도 일어나지 않는 것처럼 보이면 사용자는 그 전환이 무엇을 하는지 알 수 없다는 것이다.
발표가 Work와 Codex의 차이를 기능 목록으로 설명하는 동안, 실제 앱은 그 차이를 사용자가 볼 수 있게 보여 주지 않았다.

기존 사용자가 잃은 것도 많았다.
todfox는 프로그래밍 프로젝트가 아닌 대화가 작고 검색도 안 되는 팝업 창으로 밀려났다고 적었고,[^todfox] quinncom은 새 앱에 음성 모드, 심층 리서치, 명시적 검색 토글, 회의 요약 녹음, 맞춤형 GPT가 없고 예전 대화는 숨겨져 있다고 목록을 만들었다.[^quinncom]
발표의 모든 요금제에서 Chat, Work, Codex를 쓸 수 있다는 문장은 사실이지만, Chat이 그 앱에서 어떤 대우를 받는지는 말하지 않는다.

### 내부 채택률은 증거가 되기 어렵다

발표는 OpenAI 내부의 거의 100% 팀이 ChatGPT Work와 Codex를 쓴다고 강조한다.
miltonlost는 내부 채택률 그래프가 우습다며, KPI와 업무 요구 사항이 곡선을 크게 비틀었을 것이라고 적었다.[^miltonlost]
자기 회사 제품을 쓰라는 압력이 있는 조직의 채택률은 제품의 가치보다 조직의 정책을 보여 준다.

영업과 재무의 사례도 같은 한계를 가진다.
몇 주 걸리던 개념 증명을 24시간에, 며칠 걸리던 결산을 몇 시간에 했다는 것은 인상적이지만, 그것을 해낸 사람들은 이 도구를 만든 회사의 직원들이다.
그들은 도구의 한계를 누구보다 잘 알고, 문제가 생기면 만든 사람에게 바로 물어볼 수 있다.
일반 기업의 재무팀이 같은 결과를 얻을 수 있는지는 이 사례로 알 수 없다.

sbarre는 억지스럽지만 그럴듯한 시나리오로 서비스의 쓸모를 과장하는 일이 AI 회사 마케팅의 핵심 업무가 된 것이 섬뜩하다고 적었다.[^sbarre]
이 발표의 사례들이 과장이라는 증거는 없다.
하지만 증거로서의 무게는 발표가 기대하는 것보다 가볍다.

### 두 달 뒤 경쟁사는 반대 방향으로 갔다

발표 당일 tekacs는 Anthropic이 바로 전날 웹 인터페이스에 Chat과 Cowork를 나눴는데 볼 때마다 혼란스럽고, 이제 ChatGPT 데스크톱 앱도 Work와 Code로 나뉘었다고 적었다.[^tekacs]
z11i는 채팅, 작업, 코딩 사이에 인지적 차이가 있어서는 안 되며, 두 회사가 제품을 이렇게 나누는 것이 이상하다고 했다.[^z11i]
그의 제안은 프로젝트만 두고, 각 대화가 순수한 채팅이든 도구 사용이든 코딩이든 될 수 있게 하라는 것이었다.

두 달 뒤인 9월 16일, Anthropic은 정확히 그 방향으로 갔다.
Cowork와 채팅을 하나의 Claude로 합치고, 작업이 어디에 속하는지 사용자가 고를 필요가 없게 했다(`claude/cowork.md`).
OpenAI는 이름을 합치면서 모드를 남겼고, Anthropic은 이름을 남긴 채 모드를 없앴다.

이 대비는 ChatGPT Work의 설계를 다시 보게 한다.
OpenAI는 Codex를 ChatGPT로 만들면서도 Chat, Work, Codex를 사용자가 고르는 세 개의 모드로 남겼다.
그 모드의 차이가 사용자에게 보이지 않는다면, 모드를 남긴 이유는 사용자가 아니라 과금과 조직 통제 쪽에 있을 가능성이 크다.
사용량 구조가 다른 두 제품을 한 앱에 넣으려면, 어느 쪽 사용량을 쓰는지 가를 경계가 필요하기 때문이다.

## 인사이트

### 이름을 옮기는 것은 사용자를 옮기는 가장 거친 방법이다

OpenAI는 ChatGPT라는 이름을 Codex 앱에 넘기고, 기존 앱을 Classic으로 바꿨다.
btheconqueror가 뉴 코크와 코카콜라 클래식을 떠올린 것은 우연이 아니다.[^btheconqueror]
새 제품에 원래 이름을 주고 옛 제품에 클래식을 붙이는 것은, 사용자가 원하든 원하지 않든 새 제품으로 옮기겠다는 선언이다.

이 방법의 장점은 속도다.
업데이트 한 번으로 수백만 명이 새 앱을 쓰게 된다.
단점은 사용자가 스스로 옮겨 가지 않았다는 것이다.
michelb는 회사 사람들이 다음 날 업데이트하고 나서 대화와 프로젝트와 GPT가 모두 사라졌다고 생각하게 될 것이라고 걱정했다.[^michelb]

그래서 이런 전환에서 가장 비싼 비용은 기술이 아니라 신뢰다.
사용자는 다음 업데이트에서 또 무엇이 옮겨질지 걱정하게 되고, tencentshill이 다른 제공자로 옮기기 쉬워서 다행이라고 쓴 것처럼 이탈 비용을 다시 계산한다.[^tencentshill]
제품을 합치는 회사는 합친 뒤의 모양만큼, 사용자가 그 과정을 어떻게 겪는지를 설계해야 한다.

### 에이전트 제품의 모드는 과금 경계를 드러낸다

Chat은 사실상 무제한이고 Work는 Codex의 사용량을 쓴다.
같은 앱 안에서 두 모드를 가르는 가장 분명한 차이는 기능이 아니라 요금 구조다.
aniviacat이 발견한 추론 강도 차이도, 더 비싼 추론을 어느 모드에서 허용할지의 경계로 읽을 수 있다.

Cowork 통합 발표 HN 스레드에서 Sn0wCoder는 ChatGPT의 Chat은 여전히 무제한이고 Work는 Codex 토큰을 쓰니 통합되지 않기를 바란다고 적었다.[^Sn0wCoder]
이것은 모드가 사용자에게 무엇을 뜻하는지 정확히 보여 준다.
사용자에게 모드는 작업의 종류가 아니라 어느 주머니에서 돈이 나가느냐다.

모드를 없애면 이 경계는 모델이 대신 그어야 한다.
Anthropic이 모드를 없앴을 때 사용량이 어떻게 계산되는지가 가장 먼저 질문으로 나온 것도 그 때문이다.
에이전트 제품이 하나의 화면으로 수렴할수록, 사용자에게 보이지 않던 과금 경계를 어떻게 다시 보여 줄지가 제품 설계의 핵심 문제가 될 것이다.

### 호스팅된 에이전트가 기업의 기본 형태가 되어 간다

lukebuehler는 이런 반쯤 코딩하는 호스팅 에이전트가 기업의 미래라고 봤다.[^lukebuehler]
Claude Tag, Claude Cowork, 그리고 OpenAI의 Work가 모두 공유 인프라에서 오래 도는 에이전트라는 같은 패턴이고, 사용자 기기의 에이전트는 자리가 있지만 많은 작업 흐름에서 너무 다루기 어렵다는 것이다.

발표의 조직 통제 절이 이 방향을 뒷받침한다.
웹에서는 관리자가 클라우드 환경의 브라우저 사용과 네트워크 접근을 설정하고, 데스크톱에서는 Codex의 기업 거버넌스 모델을 가져온다.
클라우드에서 도는 에이전트는 관리자가 한곳에서 통제하고 감사할 수 있지만, 사용자 기기에서 도는 에이전트는 기기마다 정책을 밀어 넣어야 한다.

그래서 기업 시장에서 에이전트의 무게 중심은 점점 클라우드 쪽으로 옮겨 갈 것이다.
사용자 기기의 파일과 앱에 닿는 능력은 계속 중요하지만, 그 능력은 클라우드 에이전트가 필요할 때 빌려 쓰는 도구가 되고, 기본 실행 환경은 관리자가 통제하는 공유 인프라가 된다.
두 달 뒤 OpenAI가 DevDay에서 Dots와 클라우드 Codex를 전면에 내세운 것(`openai/devday-2026.md`)은 이 흐름의 다음 단계로 읽힌다.

---

[^wahnfrieden]: <https://news.ycombinator.com/item?id=48849624>

[^paxys]: <https://news.ycombinator.com/item?id=48849622>

[^simonw]: <https://news.ycombinator.com/item?id=48850620>

[^hobofan]: <https://news.ycombinator.com/item?id=48852555>

[^smoe]: <https://news.ycombinator.com/item?id=48850038>

[^neil_s]: <https://news.ycombinator.com/item?id=48850679>

[^aniviacat]: <https://news.ycombinator.com/item?id=48857401>

[^postalcoder]: <https://news.ycombinator.com/item?id=48849778>

[^GMoromisato]: <https://news.ycombinator.com/item?id=48852828>

[^todfox]: <https://news.ycombinator.com/item?id=48850888>

[^quinncom]: <https://news.ycombinator.com/item?id=48853060>

[^miltonlost]: <https://news.ycombinator.com/item?id=48850707>

[^sbarre]: <https://news.ycombinator.com/item?id=48851206>

[^tekacs]: <https://news.ycombinator.com/item?id=48849568>

[^z11i]: <https://news.ycombinator.com/item?id=48869908>

[^btheconqueror]: <https://news.ycombinator.com/item?id=48851279>

[^michelb]: <https://news.ycombinator.com/item?id=48850219>

[^tencentshill]: <https://news.ycombinator.com/item?id=48851937>

[^lukebuehler]: <https://news.ycombinator.com/item?id=48850254>

[^Sn0wCoder]: <https://news.ycombinator.com/item?id=49730310>
