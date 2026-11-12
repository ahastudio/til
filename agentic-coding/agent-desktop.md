# agent-desktop: 스크린샷 대신 접근성 트리로 데스크톱 앱을 조작하는 에이전트용 CLI

<https://github.com/vercel-labs/agent-desktop>

Show HN: [Agent-desktop – Native desktop automation CLI for AI agents](https://news.ycombinator.com/item?id=47982708) (99점, 44개 댓글)

GN 토론: <https://news.hada.io/topic?id=36967>

## 소개

agent-desktop은 AI 에이전트가 macOS, Windows, Linux의 데스크톱 앱을 보고
조작하게 하는 CLI이자 C 라이브러리다.
README는 이 도구가 스크린샷이나 픽셀 매칭 없이 운영체제의 접근성
트리(accessibility tree)를 읽어 JSON으로 돌려주고, 에이전트가 조작할 수 있는
요소마다 참조(ref)를 붙인다고 설명한다.
에이전트는 참조에 클릭이나 입력을 한 뒤 UI를 다시 읽어 결과를 확인하고 이를
반복한다.
이 반복은 에이전트 쪽에 있고 agent-desktop 안에는 모델이 없다.

저장소는 Vercel Labs 소속이고 Rust로 쓰였으며 Apache-2.0 라이선스다.
GitHub API로 확인한 2026년 11월 11일 기준 별은 21,939개, 포크는 1,633개이고
저장소는 2026년 2월 19일에 만들어졌다.
HN의 Show HN 글이 올라온 2026년 5월에는 저장소가 개인 계정 lahfir 아래에 있었고,
지금 그 주소는 vercel-labs 저장소로 영구 이동(301)된다.

### 사용 흐름

설치는 `npm install -g agent-desktop`이고 Homebrew도 지원한다.
`agent-desktop status`로 플랫폼과 권한을 확인하고, macOS에서는 `permissions
--guide`가 접근성 권한 부여를 안내한다.

```bash
agent-desktop snapshot --app Finder -i
agent-desktop click @s8f3k2p9:e8
agent-desktop snapshot --app Finder -i
```

모든 명령은 JSON 봉투 하나를 출력한다.
README가 밝힌 규칙은 다음과 같다.

| 규칙                 | 내용                                                              |
| -------------------- | ----------------------------------------------------------------- |
| 참조는 스냅샷에 종속 | `@e8`만 쓰면 거부되고, UI가 바뀌면 `STALE_REF`가 나와 다시 읽는다 |
| 창이 여럿            | `AMBIGUOUS_TARGET`이 나오고 `--window-id`로 지정한다              |
| 복잡한 앱            | `--skeleton`으로 지도를 먼저 만든 뒤 한 영역만 파고든다           |
| 기본은 헤드리스      | 접근성 API로 포인터를 움직이거나 포커스를 가져가지 않고 조작한다  |
| 비밀 입력            | `--stdin`으로 넘겨 프로세스 인자에 남지 않게 한다                 |

### 구조와 에이전트 연동

CLI와 C 라이브러리는 같은 코어를 쓰고, 코어는 `PlatformAdapter` 트레이트로만
운영체제에 닿는다.
각 바이너리는 한 운영체제용으로 빌드되어 macOS의 AX API, Windows의 UI
Automation, Linux의 AT-SPI를 쓴다.
`agent-desktop mcp`는 모든 명령을 MCP 도구로 노출하고, `skills get desktop`
명령으로 버전에 맞는 사용 지침을 내려받을 수 있다.
README는 61개 명령 이름 중 57개가 실제로 동작하며, 키와 마우스를 누른 채
유지하는 네 개는 이를 풀어 주는 데몬이 생길 때까지 실행을 거부한다고 밝힌다.
지원 환경은 macOS 13 이상, Windows 10 1809 이상, Ubuntu 24.04 이상이다.

## 분석

### 핵심 선택은 “화면을 보지 않고 구조를 읽는다”이다

기존의 컴퓨터 조작 도구는 스크린샷을 모델에 보여 주고 좌표를 고르게 한다.
agent-desktop은 접근성 트리가 이미 UI의 구조화된 설명이라는 점을 이용한다.
HN 사용자 TheFragenTaken은 도구들이 구조화된 데이터인 접근성 트리가 아니라
픽셀로 동작하는 것이 늘 이상했고, 이런 진전이 반갑다고 썼다.[^TheFragenTaken]
이 선택의 이점은 README의 설계에 그대로 드러난다.
조작 대상이 참조로 식별되므로 좌표 오차가 없고, 포인터와 포커스를 건드리지 않는
헤드리스 조작이 기본이며, 실패가 `STALE_REF` 같은 코드로 구분된다.

### 모델을 넣지 않은 설계가 연동 범위를 넓힌다

agent-desktop에는 모델이 없고 관찰과 조작만 제공한다.
그 덕에 CLI, MCP 서버, C 라이브러리, 에이전트용 skill 어느 쪽으로든 붙는다.
이는 어떤 에이전트 하네스(harness)와도 함께 쓸 수 있다는 뜻이다.
같은 접근을 택한 프로젝트가 여럿이라는 증언도 있다.
HN의 _crowecawcaw는 거의 같은 도구를 같은 이름으로 만들었고 다른 유사 프로젝트도
봤다고 하며, 플랫폼마다 달라서 크로스 플랫폼 접근성 라이브러리가 없었기에 직접
라이브러리를 만들었다고 썼다.[^_crowecawcaw]
접근성 트리 방식이 한 팀의 아이디어가 아니라 여러 곳이 비슷하게 도달한
방향이라는 정황이다.

## 비평

### 접근성 트리가 닿지 않는 화면이 있다

README는 이 한계를 직접 다루지 않는다.
HN의 tidbeck는 접근성 트리가 겹친 뷰나 뷰포트 밖의 지연 로딩에서 한계가 있다고
짚었고,[^tidbeck] MattRogish는 macOS 앱이 이 API를 쓸 의무가 없어서 화면
스크래핑 같은 대안이 항상 필요하다고 하며, Zoom 데스크톱 앱의 회의 창이 거의
커스텀 컨트롤이라 이름조차 없는 경우가 많다는 예를 들었다.[^MattRogish]
DeathArrow는 Zig의 Capy, Rust의 egui, C++의 Dear ImGui처럼 하드웨어에 직접
그리는 GUI 라이브러리로 만든 앱에서도 되면 좋겠다고 했다.[^DeathArrow]
이 한계는 사용자의 경험이고 앱마다 다르다.
그러나 “스크린샷 없이 된다”는 약속이 접근성 정보를 제대로 내보내는 앱에만
성립한다는 뜻이다.

GeekNews 사용자 junoverse는 직접 써 보니 아직 지원하는 앱이 많지 않고, 워드나
엑셀도 안 되며, 인식이 잘 안 되는 부분과 갑자기 포커스를 가져가는 문제가 있어서
더 기다려 보려 한다고 썼다.[^junoverse]
이는 한 사용자의 경험이라 어떤 버전과 앱에서 겪었는지 알 수 없다.
다만 README가 헤드리스를 기본으로 내세우는 것과 포커스를 가져가는 증상은 맞지
않으므로, 쓴 환경이나 `--headed` 여부를 확인해 볼 만하다.

### 플랫폼 지원의 서술이 시점에 따라 달랐다

2026년 5월 HN 글에서 lahfir는 반복해서 macOS가 정식(GA)이고 Windows와 Linux는
로드맵에 있다고 답했다.[^lahfir]
이에 앞서 jstanley는 작성자의 첫 댓글이 크로스 플랫폼이라고 암시하지만 README
그림은 Mac만 된다고 한다고 지적했다.[^jstanley]
지금 README는 세 플랫폼을 표로 지원한다고 쓴다.
따라서 이 글의 플랫폼 서술은 README의 현재 주장이고, 플랫폼별 완성도는 이 문서가
확인하지 못했다.
README도 각 플랫폼 문서에 헤드리스로 되는 것, `--headed`가 필요한 것, 거부하는
것이 따로 적혀 있다고만 밝힌다.
Linux에 대해서는 접근성 지원이 일관되지 않다는 우려가 있었다.
Arainach는 컴포지터, 창 관리자, UI 프레임워크, 앱마다 지원 수준이 제각각이라
접근성에 기대 Linux 시스템을 쓸 수는 없다고 썼다.[^Arainach]

### 보안 경계가 README의 경고 한 줄에 머문다

README는 스냅샷, 클립보드, 스크린샷, 명령 출력, 디버그 산출물에 비공개 데스크톱
내용이 담길 수 있으니 공개 로그나 업로드에 넣지 말라고 한 줄 경고한다.
이 도구는 에이전트에게 데스크톱 전체의 읽기와 조작 권한을 주는 것이므로, 어떤
앱을 조작하게 할지 범위를 제한하는 방법이 핵심이다.
README의 `sandbox` 명령군과 `--session`, `--trace` 옵션이 이 쪽에 해당하는
것으로 보이지만 이 문서는 그 동작을 확인하지 않았다.
HN의 dorianzheng는 boxlite 같은 로컬 마이크로 VM 안에서 돌릴 수 있는지
물었다.[^dorianzheng]

## 인사이트

### 컴퓨터 조작의 병목은 모델이 아니라 앱이 내보내는 구조다

스크린샷 방식은 어떤 앱이든 되지만 모델이 픽셀을 해석해야 하고, 접근성 방식은
정확하지만 앱이 구조를 내보내야 한다.
두 방식은 대체재라기보다 폴백 관계로 보인다.
MattRogish가 말한 Zoom의 경우처럼 구조가 있는 창은 트리로, 없는 창은 이미지로
처리하는 혼합 설계가 현실적이다.
이는 이 문서의 추론이며, README는 이미지 폴백을 내세우지 않는다.

### 접근성 품질이 에이전트 호환성이 된다

앱이 접근성 정보를 잘 채울수록 에이전트가 조작하기 쉬워진다.
접근성 개선이 지금까지는 일부 사용자를 위한 일로 취급되었다면, 에이전트가 쓰는
입력이 되면서 앱 개발자가 이를 챙길 이유가 늘어난다.
이 효과가 실제로 나타나는지는 이 글만으로 알 수 없다.
접근성 레이블이 부족한 앱이 에이전트에서도 같은 이유로 실패하는지를 앱별로
비교해 봐야 한다.

### 결론을 바꿀 관찰

- Windows와 Linux에서 macOS와 같은 수준의 조작 성공률이 앱별 표로 공개되면,
  현재의 플랫폼 지원에 대한 유보가 줄어든다.
- 일반 업무 앱(오피스 문서 편집기, 메신저, 화상 회의)에서 접근성 트리만으로
  대부분의 작업이 끝난다는 결과가 나오면, 접근성 트리가 닿지 않는 화면이 많다는
  우려는 약해진다.
- 반대로 조작 가능한 요소가 비어 있는 앱이 흔하다는 측정이 나오면, 스크린샷
  폴백이 필수라는 쪽의 해석이 힘을 얻는다.

---

[^TheFragenTaken]: <https://news.ycombinator.com/item?id=47984412>

[^_crowecawcaw]: <https://news.ycombinator.com/item?id=47988024>

[^tidbeck]: <https://news.ycombinator.com/item?id=47984524>

[^MattRogish]: <https://news.ycombinator.com/item?id=47992922>

[^DeathArrow]: <https://news.ycombinator.com/item?id=47986184>

[^junoverse]: <https://news.hada.io/topic?id=36967#cid69602>

[^lahfir]: <https://news.ycombinator.com/item?id=48019304>

[^jstanley]: <https://news.ycombinator.com/item?id=47983478>

[^Arainach]: <https://news.ycombinator.com/item?id=47984214>

[^dorianzheng]: <https://news.ycombinator.com/item?id=48038630>
