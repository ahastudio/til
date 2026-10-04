# DeepSeek Harness 데스크톱: 웹 UI를 Electron으로 감싼 맥·윈도우용 에이전트 앱

<https://www.deepseek.com/en/harness/>

HN 토론: <https://news.ycombinator.com/item?id=49929489> (405점, 216개 댓글)

GN 토론: <https://news.hada.io/topic?id=34656>

## 소개

DeepSeek Harness(`dsh`)는 DeepSeek AI가 만든 오픈소스 에이전트 하네스이고,
이번에 macOS와 Windows용 데스크톱 앱이 나왔다.
제품 페이지는 이제 전 세계 대상 공개 프리뷰(public preview)이자 오픈소스라고
소개하며, 일상 업무와 코딩과 직접 만드는 하네스를 모두 여기서 시작하라고 권한다.
설치 파일은 Apple silicon용 macOS(macOS 13 이상)와 64비트 Windows용 두 가지이고,
다운로드 페이지는 백그라운드 작업, 로컬 파일 편집,
길고 복잡한 작업 처리를 내세운다.
라이선스는 MIT이고 저장소 언어는 TypeScript이며,
2026년 10월 4일 기준 GitHub 스타는 약 24만 3천 개다.

하네스 자체와 그 바탕인 Cordis의 “모든 것이 플러그인” 설계는 8월 개발자
프리뷰 때 이 저장소의 `ai-tool/deepseek-harness.md`에 정리했다.
이 문서는 그 위에 새로 얹힌 데스크톱 앱만 다룬다.
나는 앱을 설치해 실행하지 않았다.
아래 내용은 제품 페이지, 다운로드 페이지,
저장소의 `apps/desktop/README.md`와 릴리스 노트, HN 토론에서 확인한 것이다.

제품 페이지가 보여 주는 앱의 일은 다섯 갈래다.
파일 정리와 데이터 분석과 문서·슬라이드 작성 같은 일상 업무,
저장소 탐색과 버그 수정과 테스트 실행 같은 코딩, 사실 확인과
출처 인용을 하는 리서치, 스크립트 실행과 일괄 처리를 맡는 백그라운드 작업,
그리고 플러그인 추가와 제작이다.
Word, Excel, PDF, HTML, 코드 파일을 앱 안에서 바로 미리 보고 대화로 고치며,
코드 변경은 줄 단위 diff로 검토한다.

## 동작 방식

### 웹 앱 전체를 감싼 Electron 셸

데스크톱 README의 첫 설명은 이 앱이 dsh 웹 애플리케이션 전체를 감싼
Electron 셸이라는 것이다.
Electron의 RunAsNode 자식 프로세스가 공용 프로필 러너를 띄우고,
창은 패키지된 웹 진입점 `dsh-app://app/`을 바로 불러온다.
HTTP 요청은 인증된 웹 호스트로 전달되고 WebSocket 스트림도 같은 호스트에 붙는다.
즉 데스크톱 앱과 `npx @deepseek-ai/dsh web`으로 띄우는 웹 UI는 같은 제품이고,
차이는 설치와 수명 관리 쪽에 있다.

웹 UI는 기본으로 `http://127.0.0.1:3080`에서 뜨지만,
데스크톱은 운영체제가 정해 주는 포트를 쓴다.
그래서 웹의 3080 포트나 예약된 포트와 부딪히지 않는다.
10월 3일 릴리스 노트(v0.2.1-alpha.1)는 이 기본값이 Windows의 예약 포트 범위
때문에 앱이 뜨지 않던 문제를 피하려는 것이라고 적었다.

### 창을 닫아도 작업은 계속된다

macOS의 닫기 버튼이나 ⌘W,
Windows의 ×나 Alt+F4로 메인 창을 닫으면 앱은 끝나지 않고 창만 숨는다.
페이지와 호스트는 계속 돌고,
다시 열면 세션과 작성 중인 초안과 스크롤 위치가 그대로다.
Windows는 처음 숨길 때 한 번 확인을 받고, 실행 내내 트레이 아이콘을 둔다.
macOS는 메뉴 막대 아이콘 없이 Dock 아이콘이나 두 번째 실행으로 창을 되살린다.

실제로 끝내는 동작(⌘Q, 메뉴,
트레이의 종료)은 먼저 호스트에 무엇이 끊기는지 묻는다.
실행 중인 에이전트와 서브에이전트, 승인 대기, 대기열의 메시지, 돌고 있는 작업,
예약된 알림이 있으면 종료 확인 창이 뜬다.
예약 작업은 앱이 닫혀 있는 동안 실행되지 않고,
알림도 이번 실행에서 불러온 세션에서만 울린다.
README는 데스크톱이 예약 작업을 기본으로 켜 두지 않는다고 밝힌다.

### 플러그인과 Creator 모드

제품 페이지의 공식 플러그인 목록에는 Agent teams, Auto approval review,
Scheduled tasks, Voice input이 실험 기능으로 올라 있고, Terminal, Agent loop,
Subagents가 함께 있다.
Creator 모드에서는 대화로 플러그인을 만들어 설치한다.
제품 페이지의 예시는 뽀모도로 타이머 플러그인을 써 달라는 요청에서 시작한다.
에이전트는 플러그인 개발 스킬을 읽고,
항상 위에 떠 있는 창이 필요하다고 판단한 뒤,
`package.json`과 638줄짜리 `client.js`를 쓰고,
`plugin_manager`로 설치하고 동작을 확인했으며, 여기까지 5분 24초가 걸렸다.
README에 따르면 Creator와 웹 플러그인 관리자는 데스크톱에 들어 있는 pnpm을
쓰므로 PATH에 pnpm이 없어도 된다.

HN에서 Kuyawa는 macOS 앱을 깔아 보니 설정과 작업 공간이 그대로 넘어왔고,
단축키로 글자 크기를 바꾸는 기능이 없어 dsh에게 플러그인을 만들어 달라고
했더니 한 번에 만들어 줬다고 적었다.[^Kuyawa]
같은 댓글에 붙은 답글에서 sroerick은 그 스레드 분위기가 홍보성 댓글처럼
느껴진다고 했다.[^sroerick]

### 개발자 도구와 관측성

제품 페이지는 실행 추적과 런타임 정보를 볼 수 있는 개발자 도구를 따로 소개한다.
턴마다 시스템 프롬프트, 사용자 메시지, 컨텍스트, 도구 호출과 그 입력·결과,
소요 시간이 펼쳐진다.
데스크톱 README에 따르면 패키지된 빌드에서도 F12나 Command+Option+I(Windows는
Ctrl+Shift+I)로 DevTools를 열 수 있다.

HN에서 cjbprime은 다른 하네스와 비교해 가장 눈에 띈 점으로 모든 프롬프트와
응답과 도구 호출을 그대로 볼 수 있는 관측성을 꼽았다.[^cjbprime]
logicchains는 컨텍스트를 덧붙이기만 하는(append-only) 설계라 다른 하네스에서
자주 터지는 캐시 무효화 버그가 원천적으로 생기지 않는다고 했다.[^logicchains]
wg0은 서브에이전트가 작업 도중 부모에게 메시지를 보내고 부모도 도중에
서브에이전트의 방향을 바꿀 수 있는 양방향 통신을 장점으로 들었다.[^wg0]

## 설치하기

설치 경로는 세 가지다.
제품 페이지의 설치 파일, npm으로 띄우는 웹 UI, 소스 빌드다.

```bash
# 1. 데스크톱 앱: 제품 페이지의 설치 파일
#    macOS (Apple silicon, macOS 13 이상)
curl -LO https://download.deepseek.com/desktop/dsh-latest-macos-arm64.dmg
#    Windows (64비트)
curl -LO https://download.deepseek.com/desktop/dsh-latest-windows-x64.exe

# 2. 웹 UI: Node.js만 있으면 된다. 기본 주소는 http://127.0.0.1:3080
npx @deepseek-ai/dsh web

# 3. 소스에서 빌드
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

웹 UI 빠른 시작 문서의 첫 순서는 모델 설정이다.
Settings → Models에서 DeepSeek API 키를 넣으면 서버를 다시 띄우지
않아도 바로 쓸 수 있다.
그다음 작업 공간(workspace)을 고르기 전까지는 입력창이 열리지 않는다.
HN에서 BrentOzar는 설정의 Models 화면에 지원 모델 목록이 길게 있고, 이름과 base
URL과 프로토콜과 API 키를 넣는 커스텀 모델 탭도 있다고 설명했다.[^BrentOzar]
JamesMcMinn은 로컬에서 돌리는 Qwen 모델에 붙여 잘 쓰고 있다고
적었다.[^JamesMcMinn]

### 터미널 명령 설치

데스크톱 앱에는 `dsh` 명령도 함께 들어 있다.
9월 29일 릴리스 노트(v0.2.0-rc.2)부터 Node나 pnpm을 따로 깔지 않아도 메뉴의
Manage dsh Command… 항목으로 명령을 설치할 수 있다.
macOS에서는 `/usr/local/bin/dsh`를 만들고,
Windows에서는 현재 사용자의 PATH에 등록한다.
설치 후 새 터미널에서 확인한다.

```bash
dsh --version
```

데스크톱은 `$DSH_HOME/profiles/desktop` 프로필을 소유하고,
README는 일반 CLI가 이 프로필을 부팅하지 못한다고 적는다.
데스크톱이 설치한 명령은 앱이 꺼져 있을 때도 이 프로필의 플러그인을 관리할 수
있지만, npm으로 설치한 `dsh`는 이 프로필을 건드리지 못한다.

## 텔레메트리

데스크톱과 웹은 수집 정책이 다르다.
저장소의 제품 텔레메트리 문서는 데스크톱 분석 소비자가 상호작용 이벤트와 컴팩션
이벤트를 골라 보내고, 가능하면 로그인 신원을 붙인다고 설명한다.
같은 문서에 일반 웹 클라이언트는 제품 이벤트를 수집하지 않는다고 적혀 있다.
데스크톱 README도 첫 문단에서 데스크톱 분석이 제품 수집 정책과 앱 설정을
따르고 웹 사용은 제외된다고 밝힌다.

HN 토론의 첫 댓글이 바로 이 차이를 짚었다.
wren6991은 데스크톱 빌드가 텔레메트리를 기본으로 켜는 것 같고, `dsh web`은
사용자가 명시적으로 보낸 피드백에만 텔레메트리가 붙는다고 적었다.[^wren6991]
그는 처음 실행하기 전에 `$DSH_HOME/cordis.patch.yml`(기본은 `~/.dsh`)에
다음을 넣으라고 했다.

```yaml
- id: desktop-product-telemetry
  disabled: true
- id: product-analytics
  disabled: true
- id: session-log-deepseek
  config:
    enabled: false
```

이 설정은 HN 댓글이 제시한 방법이고,
나는 플러그인 id를 저장소에서 하나씩 대조하지 않았다.
rootsudo는 이 댓글을 첫 명령을 실행한 뒤에야 봐서 무엇이 이미 나갔는지
모르겠다고 했고, 설정 화면에도 항목이 있지만 웹 포털에서 먼저 정한 값과 동기화
후에도 맞지 않는다고 적었다.[^rootsudo]

## 트레이드오프

### Electron으로 얻는 것과 잃는 것

웹 앱 전체를 Electron으로 감싸는 선택 덕분에 웹과 데스크톱은 같은 UI,
같은 플러그인, 같은 호스트를 공유한다.
웹에서 쓰던 설정과 작업 공간이 그대로 넘어왔다는 Kuyawa의
경험도 이 구조에서 나온다.
대신 데스크톱만의 이점은 설치, 창 수명, 트레이, 터미널 명령,
마이크 권한 같은 운영체제 연동에 머문다.

HN에서 rayiner는 README의 Electron 셸 문장을 인용하며 이렇게 단순한
UI라면 AI가 네이티브 프런트엔드를 쉽게 써 줄 텐데 모든 하네스가 Electron이라고
꼬집었다.[^rayiner]
searealist는 반대로 모델이 HTML과 JS를 출력으로 만들고,
하네스를 고치는 플러그인을 생성하고, 웹 페이지를 탭 패널로 여는 일에
TypeScript와 V8이 잘 맞아서 다들 이 모델로 수렴했다고 설명했다.[^searealist]
dsh의 Creator 모드가 브라우저에서 바로 도는 `client.js` 플러그인을 쓰는 걸
보면, 이 수렴은 취향이 아니라 플러그인 구조의 요구에 가깝다는 것이 내 해석이다.

### 모든 것이 플러그인이면 수정 비용도 플러그인 단위다

wren6991은 같은 댓글에서 “모든 것이 플러그인”의 문제를 짚었다.
핵심 기능까지 플러그인이면, 기존 동작을 조금 바꾸고 싶을 때 그 핵심 플러그인에
대한 패치를 계속 직접 유지해야 한다는 것이다.[^wren6991]
anticensor는 코어가 잘 정의된 확장 지점을 제공하므로 핵심 플러그인을 패치할
필요가 없다고 반박했다.[^anticensor]

redox99는 제3자 플러그인은 악성일 수도, 관리가 끊길 수도, 품질이 낮을 수도 있어
깔고 싶지 않고, 잘 다듬어진 기본 기능이 낫다고 했다.[^redox99]
Maxatar는 플러그인 구조는 기본 기능의 품질과 무관한 설계 성질일
뿐이라고 답했다.[^Maxatar]
설치 측면에서 보면 이 논쟁의 결론은 단순하다.
데스크톱 앱은 플러그인 설치 장벽을 없앴으므로,
제3자 플러그인을 검토 없이 들일 위험도 같이 커졌다.

### 하네스는 커질 것인가 줄어들 것인가

StrauXX는 모델이 좋아질수록 하네스는 바닐라 Pi 수준이나 그 이하로 줄어들 것이라
이런 정교한 하네스의 미래는 밝지 않다고 봤다.[^StrauXX]
surgical_fire는 하네스가 LLM에게는 언어에 대한 IDE만큼 중요하다고
답했다.[^surgical_fire]
dsh 데스크톱은 분명 후자에 건 제품이다.
예약 작업, 개발자 도구, 파일 미리 보기,
에이전트 팀처럼 모델 바깥의 기능을 계속 늘리고 있기 때문이다.

## 함정

### 개발자 프리뷰 경고는 그대로다

제품 페이지는 공개 프리뷰라고 부르지만, 저장소 README는 여전히 개발자 프리뷰이며
호환성을 깨는 변경이 있을 것이라고 대문자로 경고한다.
`SAFETY.md`는 보안 감사를 받지 않은 실험 소프트웨어이고,
모델이 만든 코드와 명령을 실행하며,
샌드박스와 승인 창이 격리를 보장하지 않는다고 적는다.
권장 사항은 최소 권한, 일회용 가상 머신이나 컨테이너, 접근 가능한 파일의 백업,
플러그인과 명령의 사전 검토다.
데스크톱 앱이 설치를 쉽게 만들었다고 이 경고가 약해지지는 않는다.

### 비공식 배포처

throwa356262는 이번 업데이트가 설치를 쉽게 하려는 것이라고 보면서,
그동안 공식 설치 패키지가 없던 틈에 정체불명의 제3자가 수정본을 만들어 검색
결과에서 DeepSeek보다 위에 오르도록 SEO를 해 왔다고 경고했다.[^throwa356262]
설치 파일은 제품 페이지에 걸린 `download.deepseek.com`
주소에서만 받는 편이 안전하다.

### 업데이트 속도

릴리스 노트를 보면 9월 22일부터 10월 3일 사이에만 alpha와 rc가 여러 번 나왔고,
일부 변경은 기존 설정을 바꾼다.
예를 들어 v0.2.0-rc.2는 서드파티 모델 목록을 갱신하면서 일부 옛 모델 id를
지웠고, 저장된 선택을 다시 골라야 할 수 있다고 적었다.
같은 시기 v0.2.1-alpha.1은 Claude Code Mods 호환 계층을 실험으로 넣었는데,
노트는 이것이 실제 호환성을 주려는 것이 아니라 그 API가 dsh 플러그인의
부분집합임을 확인하려는 단계라고 밝힌다.
쓰는 쪽에서는 업데이트 후 모델 선택과 플러그인 동작을 다시 확인해야 한다.

## 체크리스트

- 설치 파일을 `download.deepseek.com`에서 받았는가?
- 첫 실행 전에 텔레메트리 설정을 확인했는가?
- 에이전트가 접근할 작업 공간에 백업이 있는가?
- 제3자 플러그인의 코드를 설치 전에 읽었는가?
- 창을 닫아도 작업이 계속 돈다는 점을 알고 있는가?
- 터미널에서 쓰는 `dsh`가 데스크톱이 설치한 명령인지 npm 명령인지 구분했는가?

---

[^Kuyawa]: <https://news.ycombinator.com/item?id=49929518>

[^sroerick]: <https://news.ycombinator.com/item?id=49930294>

[^cjbprime]: <https://news.ycombinator.com/item?id=49930007>

[^logicchains]: <https://news.ycombinator.com/item?id=49930716>

[^wg0]: <https://news.ycombinator.com/item?id=49930609>

[^BrentOzar]: <https://news.ycombinator.com/item?id=49934457>

[^JamesMcMinn]: <https://news.ycombinator.com/item?id=49930997>

[^wren6991]: <https://news.ycombinator.com/item?id=49933838>

[^rootsudo]: <https://news.ycombinator.com/item?id=49934494>

[^rayiner]: <https://news.ycombinator.com/item?id=49933469>

[^searealist]: <https://news.ycombinator.com/item?id=49941686>

[^anticensor]: <https://news.ycombinator.com/item?id=49947637>

[^redox99]: <https://news.ycombinator.com/item?id=49932585>

[^Maxatar]: <https://news.ycombinator.com/item?id=49936480>

[^StrauXX]: <https://news.ycombinator.com/item?id=49930395>

[^surgical_fire]: <https://news.ycombinator.com/item?id=49931311>

[^throwa356262]: <https://news.ycombinator.com/item?id=49930499>
