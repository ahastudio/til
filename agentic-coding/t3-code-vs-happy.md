# T3 Code와 Happy 비교

Happy와 T3 Code를 비교한다.
이 저장소에 이미 정리한 [Happy 문서](../happy-coder/architecture.md)와
[T3 Code 문서](t3-code.md)를 바탕으로,
두 도구의 공식 문서와 저장소에서 읽은 차이를 출발점, 비전, 로드맵, 철학, 구조,
에이전트와 모델, 권한, 원격 접속, 팀 사용, 데이터 전송 순서로 놓는다.

## 소개

T3 Code와 Happy는 둘 다 컴퓨터에 설치된 코딩 에이전트를 구독 플랜 그대로 쓰면서
데스크톱과 폰에서 조종하게 해 주는 MIT 라이선스 오픈소스 앱이다.
T3 Code는 사용자가 이미 로그인한 에이전트를 한 인터페이스에서 조종하는
제어판이고, 토큰을 되팔지 않는다고 README가 밝힌다.[^t3-readme]
Happy는 README가 Claude, Codex, Grok을 한 앱에서 조율하고 구독을 재사용한다고
소개하며,[^happy-readme] 홈페이지는 사용자와 팀과 에이전트를 위한 한 곳이라는 팀
앱으로 내세운다.[^happy-home]
여기서 팀은 사람과 에이전트가 함께 일하는 팀이다.[^happy-multiplayer]

GitHub API로 2026년 11월 20일에 읽은 저장소 정보는 다음과 같다.
열린 이슈 수는 GitHub가 열린 풀 리퀘스트를 포함해 센 값이다.

| 항목        | T3 Code                | Happy (`slopus/happy`)       |
| ----------- | ---------------------- | ---------------------------- |
| 라이선스    | MIT                    | MIT                          |
| 주 언어     | TypeScript             | Swift (모바일 앱 저장소)     |
| 별과 포크   | 별 66,941, 포크 11,637 | 별 24,718, 포크 2,127        |
| 열린 이슈   | 3,596                  | 1,131                        |
| 저장소 생성 | 2026년 2월 8일         | 2025년 7월 18일              |
| 마지막 푸시 | 2026년 11월 20일       | 2026년 11월 20일             |
| 홈페이지    | `https://t3.codes`     | `https://happy.engineering/` |

Happy는 저장소가 여러 개로 나뉘어 있다.
`slopus/happy`는 모바일 앱(iOS, Android, 웹)과 원래 CLI와 릴레이 서버를 담고,
데스크톱 앱은 `slopus/happy-desktop`, 에이전트 런타임은 `slopus/happy-agent`에
있다고 README가 안내한다.[^happy-readme]
`happy-desktop`은 2026년 7월에, `happy-agent`도 같은 달에 만들어졌고 별은 각각
114개와 40개이다.
이 문서가 비교하는 Happy는 이 데스크톱 앱과 런타임, 모바일 앱의 묶음이다.

## 출발점과 변화

### Happy는 모바일 클라이언트에서 사람과 에이전트의 팀 앱으로 옮겨 왔다

Happy가 공개된 것은 2025년 8월 14일의 Show HN이다.
글을 쓴 ex3ndr는 모델이 좋아져서 더는 붙어서 지켜볼 필요가 없다는 생각에서
시작했고, 네 명이 주말에 만들었다고 적었다.[^show-hn]
`happy-coder`를 설치해 `claude` 대신 `happy`를 실행하는 방식이었다.[^show-hn]
목표는 세 가지였다.
책상에서 쓰던 흐름을 깨지 않을 것, 암호화 키를 폰에서 만들어 서버가 내용을 볼 수
없게 할 것, 11Labs 실시간 SDK로 말로 조종하게 할 것이다.[^show-hn]
앱과 채팅은 무료이고 나중에 음성 추론에 요금을 받을 수 있다고도 썼다.[^show-hn]

이 저장소의 기존 노트도 이 시기의 Happy를 설명한다.
[아키텍처 노트](../happy-coder/architecture.md)는 Expo 클라이언트와 Claude Code,
Codex CLI를 감싸는 래퍼, 암호화된 릴레이 서버로 이루어진 구조를 적는다.
[새 세션 노트](../happy-coder/start-new-session.md)는 2025년 9월의 1.5.0에서
폰에서 새 세션을 시작하게 되었다고 적는다.

2026년 1월에는 다른 모습도 보인다.
Ask HN에서 한 사용자가 Happy가 안정적으로 돌아가지 않고 버려진 것 같다고
썼고,[^ask-hn] 기여자 marxism은 한동안 어려운 시기를 겪었지만 새 핵심 기여자가
들어와 이슈 약 100개를 정리하고 단일 실행 파일로 자체 호스팅하게 하는 릴리스를
낼 예정이라고 답했다.[^marxism]
이 시기가 지나 2026년 7월에 `happy-agent`와 `happy-desktop` 저장소가 만들어졌다.
변경 기록에 따르면 데스크톱 앱의 첫 핵심 릴리스(v0.0.20, 2026년 7월 29일)는
프로젝트, 에이전트 대화, 모델과 추론 강도 조절, 파일, 변경 내용, 터미널을 담은
macOS 앱이었다.[^happy-changelog]
10월에는 에이전트를 업데이트해도 실행 중인 턴이 이어지게 하는 기능(v0.0.95)과
사이드바를 스스로 정리하는 줄기세포(stem cells) 베타(v0.0.102)가
나왔다.[^happy-changelog]

옮겨 가기 안내는 구조의 변화를 그림으로 보여 준다.
이전에는 터미널의 `happy`가 폰과 Happy 서버를 거쳐 암호화된 대화를 저장했다.
지금은 사용자의 컴퓨터마다 Happy Agent가 돌고, 폰이 각 Happy Agent에 따로
붙으며, 릴레이는 트래픽만 전달하고 저장하지 않는다.[^happy-migrate]

여기서 말하는 팀은 에이전트만의 팀이 아니라 사람과 에이전트가 함께 일하는
팀이다.
팀의 구성원은 사람이고, 각자 자기 이름으로 로그인해 같은 작업과 봇과 피드와 공유
목록을 본다.[^happy-multiplayer]
에이전트는 그 구성원이 시킨 작업을 하거나, 봇으로서 이름과 폴더와 규칙집을
가지고 팀의 상시 업무를 맡는 식으로 팀에 참여한다.[^happy-bots]
비전 문서는 동료 대부분이 이제 에이전트라는 가정에서 출발하므로 에이전트도 팀의
일원처럼 다루지만, 로그인하고 결정을 내리고 권한을 쥐는 쪽은
사람이다.[^happy-vision]
이 구분은 문서의 서술을 읽어 이 문서가 정리한 것이다.

### T3 Code는 처음부터 제어판이었고 표면을 넓혀 왔다

T3 Code의 저장소는 2026년 2월 8일에 만들어졌고, 첫 릴리스(v0.0.0-alpha.3)는 3월
2일이다.
2026년 11월 20일까지 야간 빌드를 포함해 릴리스가 855개 올라왔고 최신 안정판은
v0.1.11이다.
릴리스 수는 GitHub API가 알려 준 값이다.
`AGENTS.md`는 T3 Code를 코딩 에이전트를 위한 최소한의 GUI로 소개하고, Claude
Desktop, Codex App, Cursor Glass, Conductor 같은 앱의 구독
지참(bring-your-own-subscription) 오픈소스 대안이라고 부른다.[^t3-agents-md]
README는 이 도구들에서 영감을 받았지만 어느 것도 기준에 못 미쳐 직접 만들었다고
쓴다.[^t3-readme]

시작이 제어판이었다는 점은 지금도 이어진다.
문서 목차에는 스레드와 권한 모드, 터미널 기록, 소스 컨트롤, 음성 입력, 비밀 값,
기기, 게스트 링크, 외부 에이전트용 MCP 같은 항목이 있다.[^t3-docs]
목차의 제목만 읽었으므로 각 기능의 깊이는 확인하지 못했다.
제공자 목록은 Claude Code와 Codex에서 시작해 Cursor, Grok Build, Antigravity,
Kiro, Pi, Muse Code, fx와 ACP 에이전트까지 늘었다.[^t3-readme]
기능은 늘었지만 에이전트의 루프를 건드리지 않고 그 위의 화면과 연결을 키운다는
방향은 바뀌지 않았다.
이는 두 자료를 대조한 이 문서의 정리이다.

## 비전

### Happy가 그리는 곳은 회사 전체를 담는 한 앱이다

Happy의 비전 문서는 한 회사가 하나의 앱 위에서 돌아갈 수 있어야 하고 그것을
공개된 곳에서 만들겠다고 쓴다.[^happy-vision]
문서가 내세우는 방향은 다음과 같다.
- 사람을 행복하게 한다. 다듬어진 UX, 오픈소스, 모든 제공자의 모델, 종속 없음.
- 회사 전체를 위한 한 앱. 작업, 봇, 피드, 목록, 문서, 달력은 지금 있고 메시지와
통화는 다음이다.
- 하나의 주 에이전트. 많은 에이전트를 돌려도 사용자에게 말을 거는 것은 하나이고,
그것이 알림을 모아 꼭 필요할 때만 방해한다.
- 채팅의 변화. 쌓이기만 하는 로그 대신 사이드바와 채팅이 에이전트가 만든
산출물이 된다.
- 덜 만지고 더 이해하기. 설정과 이름 짓기 같은 잡무는 에이전트가 맡고 사람은
이해에 집중한다.
- 폰이 먼저. 폰에서 승인하는 것은 이미 흔하고 폰에서 일하는 것이 다음이다.
- 하나의 하네스. 모든 에이전트 아래에 Happy Agent를 두고 제공자별 프롬프트와
도구는 그대로 쓴다.
- 권한은 에이전트에 속한다. 지금은 에이전트와 말하는 사람이 그 권한을 쥐는데
에이전트 자신의 것이어야 한다는 생각이다.[^happy-vision]

돈에 대해서는 지금은 수익에 집중하지 않는다고 쓴다.
현재 유료인 것은 모바일 앱의 음성뿐이고, 나중에는 호스팅 업체의 추천 코드나 자체
호스팅과 추가 기능을 생각한다고 한다.[^happy-vision]
같은 글은 Meta가 내부 시범 도입을 문의해 왔다고 적는데, 이 문서는 그 서술을
확인하지 못했다.[^happy-vision]
저자는 Steve Korshakov와 Kirill Dubovitskiy 두 사람이고 GitHub 기여자들이
돕는다고 팀 소개에 있다.[^happy-team]
비전 문서의 아직 나오지 않은 항목(직접 메시지, 통화, 클릭 한 번으로 빌리는
컴퓨트)은 문서가 직접 아직 출시되지 않았다고 밝힌다.[^happy-vision]

### Happy는 하네스 위에 일의 단위를 올렸다

방향은 이미 문서의 기능으로 나타난다.
- 작업(task)은 이름과 소유자와 대화를 가진 일의 단위이다. 팀원의 새 작업이 내
사이드바 맨 위에 나타나고 열면 실시간으로 따라 읽을 수 있다.[^happy-tasks]
- 봇은 하나의 일과 하나의 열쇠와 하나의 규칙집을 가진다. 이름과 폴더와 이어지는
대화를 갖고 일정에 따라 일한다.[^happy-bots]
- 피드는 에이전트가 만든 보고서와 화면과 영상 같은 산출물이 하루 단위로 모이는
한 줄기이다.[^happy-feed]
- 컴퓨터는 사용자와 팀이 가진 기계이다. 임대 가상 머신 대신 이미 가진 컴퓨터에서
에이전트를 돌리는 쪽을 택한다.[^happy-computers]
- 첫 봇인 Chief of Staff는 모델 계정 추가, 프로젝트 가져오기, 폰 연결, 서버 배포
같은 설정을 말로 대신한다.[^happy-chief]
- 에이전트는 창을 닫거나 재시작해도 이어지고, 하위 에이전트는 다른 모델로 일을
맡을 수 있으며 서로 메시지를 보내고 기다림과 예약 메시지를
가진다.[^happy-agents]

팀이 이 도구로 Happy 자체를 만든다는 서술도 있다.
두 사람과 봇들이 일하고, 피드에는 2026년 10월에서 11월 중순 사이 에이전트가 올린
게시물이 약 400개라는 수치가 나온다.[^happy-feed]
이는 만든 쪽의 사용 사례이며 이 문서가 확인하지 못했다.

### T3 Code가 지키려는 것은 빠르고 열린 제어판이다

`AGENTS.md`는 절대 타협하지 않을 것 네 가지를 든다.
핵심에서 열려 있을 것, 성능에서 타협하지 않을 것, 원격으로 쓸 수 있을 것, 여러
화면(웹, 데스크톱, 모바일)을 지원할 것이다.[^t3-agents-md]
열림은 로드맵과 생각을 공유하고 많은 사용자가 포크해서 쓴다는 설명이고, 성능은
웹소켓으로 보내는 데이터 양과 CSS 애니메이션이 만드는 GPU 부하 같은 퇴행을
정기적으로 점검한다는 설명이다.[^t3-agents-md]
README는 방향이 틀어지면 누구든 포크해서 원하는 도구를 만들 수 있게 하겠다고
쓴다.[^t3-readme]

Theo의 글이 같은 문서에 실려 있다.
야심 찬 아이디어와 단순한 시스템을 좋아하고, 이미 있는 복잡함을 지키려 하지 말고
그럴듯해 보인다는 이유로 장치를 들이지도 말며, 올바른 동작이 놀랍지 않게 되는
가장 작은 모델을 위해 싸우라는 내용이다.[^t3-agents-md]
범위가 커지는 것(scope creep)을 막으라고도 쓴다.[^t3-agents-md]
기여 정책도 같은 방향이다. 리뷰 여력이 제한적이라 작고 집중된 수정이 병합될
가능성이 가장 높고 기능은 먼저 승인된 논의가 있어야 한다.[^t3-readme]
`AGENTS.md`는 대부분의 기여가 T3 Code 자체에서, 종종 원격으로 조종되어
나온다고도 밝힌다.[^t3-agents-md]

홈페이지는 이 도구를 코딩 에이전트의 오픈소스 제어 평면이라고 부르고 50만 명
이상이 쓴다고 내세운다.[^t3-home]
이 수치는 만든 쪽의 서술이며 근거나 집계 방식을 이 문서가 확인하지 못했다.

## 로드맵

비전이 가려는 곳이라면 로드맵은 그곳에 닿는 순서이다.
두 도구는 로드맵을 다루는 방식부터 다르다.
Happy는 사이트와 저장소에 로드맵과 계획서를 공개하고, T3 Code는 로드맵 문서를
따로 두지 않고 기여 정책으로 방향을 드러낸다.

### Happy 사이트가 아직 없다고 밝힌 것

Happy 문서는 곳곳에 아직 만들지 않은 것을 적어 두었다.
이 목록이 사실상 가장 가까운 로드맵이다.
- 직접 메시지(사람끼리, 사람과 봇 사이)와 통화, 클릭 한 번으로 빌리는 컴퓨트.
비전 문서가 출시되지 않았다고 직접 밝힌다.[^happy-vision]
- Happy Cloud와 함께 오는 권한 체계. 역할이 담긴 초대, 맞춤 역할, 비공개 보관함,
읽을 수는 없지만 쓸 수는 있는 비밀 값, 감사 기록이다.[^happy-perm]
- Happy Cloud와 함께 오는 컴퓨터 추가. 명령 한 번으로 컴퓨터를 팀에 붙이고, 그
컴퓨터는 바깥으로 연결을 걸기만 하고 들어오는 연결은 받지
않는다.[^happy-computers]
- 팀 서버의 빠진 것. 초대와 제거 버튼, 구성원별 제공자 계정, 구성원별 권한이다.
지금은 구성원 제거 기능이 없고 서버를 멈추면 모두가 한꺼번에
끊긴다.[^happy-teamserver]
- 실행 중인 제공자 세션의 포크와, 이름으로 원격 컴퓨터를 추가하는
경험이다.[^happy-how]

사이트의 변경 기록은 이 목록이 짧은 주기로 줄고 있음을 보여 준다.
2026년 7월의 첫 핵심 릴리스 뒤 10월에만 업데이트 중 턴 유지, 줄기세포 베타, 새
모델 추가가 이어졌다.[^happy-changelog]

### Happy 저장소의 로드맵 문서

`slopus/happy`에는 `docs/roadmap.md`가 있고 마지막 수정은 2026년 4월
13일이다.[^happy-roadmap]
항목은 다음과 같이 묶여 있다.
- 바로 다음: 자신들이 매일 쓰는 개발 도구로 삼기, 기여 지침(버그, UI 손질, 새
기능, 리팩터, 핵심 리팩터 순서), 변경 소식을 이미지와 영상으로
알리기.[^happy-roadmap]
- 기본 요건(table stakes): Conductor를 따라잡기. 세션 안의 파일 미리보기와 편집,
더 나은 diff 보기, 세션 포크, 묶음 배포가 들어 있다.[^happy-roadmap]
- 작업 공간과 체크아웃: 여러 컴퓨터에 걸친 작업 공간 개념과 데몬이 관리하는
체크아웃. 암호화 첨부와 내장 터미널은 어려운 항목으로 따로 적혀
있다.[^happy-roadmap]
- 기반 정비: 세션 수명 관리 버그 수정, 정기 실행 에이전트, 벤더 SDK
최신화.[^happy-roadmap]
- 바이럴: 여러 에이전트를 여러 컴퓨터에 뿌리는 다중 에이전트 배치, 에이전트가
에이전트를 부리는 구조, 반복 가능한 에이전트 파이프라인(소프트웨어 공장), 말로
에이전트를 부리는 음성.[^happy-roadmap]
- 그 밖: 사용자와 직접 이야기하기, 성장(게시물 반자동화), UI를 말로 바꾸는 자기
맞춤, 푸시 알림 라우팅, Linear와 GitHub 연동.[^happy-roadmap]

이 문서는 날짜가 4월이고 이후 일부는 이미 나왔다.
데스크톱의 첫 핵심 릴리스가 파일, 변경 내용, 터미널을 담은
앱이었고,[^happy-changelog] 하위 에이전트와 예약 메시지가 문서에
있으며,[^happy-agents] 음성도 나왔다.[^happy-voice]
이 대응은 두 자료를 대조한 이 문서의 해석이다.
반대로 세션 포크는 지금도 사이트에서 아직 없는 것으로 남아 있다.[^happy-how]
같은 저장소의 `docs/experimental/roadmap.md`는 Expo 앱 시절의 로드맵이고 이제는
옛 문서라고 스스로 밝힌다.[^happy-roadmap-old]

### Happy 마스터 플랜이 말하는 현재 방향

두 저장소(`happy-desktop`, `happy-agent`)는 `master-plans/` 폴더에 계획서를
둔다.
계획서는 사람이 불러 준 제품 의도이고, 코드가 계획서와 어긋나면 틀린 것은
코드라는 원칙을 앞머리에 적는다.[^happy-plans-desktop]
계획서는 할 일 목록이 아니라 도착지의 설명이며 번호는 우선순위가 아니라고
한다.[^happy-plans-desktop]
데스크톱 쪽 계획서의 주제는 다음과 같다.
- 원격 Happy Agent: 다른 컴퓨터의 에이전트가 같은 프로젝트와 화면과 코드 경로로
쓰이고, SSH 방식은 버린다.[^happy-plan-remote]
- 여러 Happy Agent: 네트워크가 끊겨도 마운트된 앱은 사라지지 않고, 한 에이전트의
실패가 다른 에이전트의 작업을 끊지 않는다.[^happy-plan-multi]
- 인라인 산출물: 에이전트가 채팅 안에 UI를 그리고, 하드코딩하는 컴포넌트는
최소로 둔다.[^happy-plan-artifacts]
- 채팅 화면: 기록은 사람이 움직이기 전까지 가만히 있고 스크롤 위치는 읽는 사람의
것이다.[^happy-plan-chat]
- 슬롯: 에이전트가 앱의 정해진 자리(입력창 위 줄, 프로젝트 제목 등)에 내용을
꽂는다.[^happy-plan-slots]
- 앱 내 브라우저: 로그인할 수 있는 진짜 브라우저이고 비밀번호를 저장하거나 다른
브라우저의 로그인을 가져오지 않는다.[^happy-plan-browser]
- Windows: 어떤 콘솔 창도 화면에 보이면 안 된다.[^happy-plan-windows]

에이전트 쪽 계획서의 주제는 다음과 같다.
계획서는 런타임을 Rig라고도 부르며 이 문서는 Happy Agent와 같은 대상으로 읽었다.
- 제공자 프로토콜: 제공자마다가 아니라 프로토콜마다 구현을 하나만
둔다.[^happy-plan-providers]
- 받은편지함: 에이전트가 사람에게 묻거나 양식을 채우게 하는 하나의 지속되는
곳.[^happy-plan-inbox]
- 죽지 않는 에이전트: 하위 에이전트도 후속 메시지를 받아 이어 가야 한다.
계획서는 지금 코드가 이 원칙에서 후퇴했다고 스스로 적는다.[^happy-plan-agents]
- 예약: 모든 모델에 대기와 시각까지 대기, 일반 에이전트에 예약 메시지를
준다.[^happy-plan-schedule]
- 계정 라우팅: 같은 제공자의 여러 계정을 모델이 아니라 런타임이 알아서 나눠
쓴다.[^happy-plan-accounts]
- 워크렛(worklet): TypeScript로 쓰는 상시 백그라운드 연산이고 도구를 선언해 모든
에이전트가 부른다. 이전의 플러그인 계획은 이것으로
대체되었다.[^happy-plan-worklets][^happy-plan-plugins]
- P2P 네트워킹: 주 컴퓨터에 보조 컴퓨터를 붙이는 일이 전송 신원을 손으로
설정하는 일이 아니라 합류처럼 느껴지게 한다.[^happy-plan-p2p]
- 폴더와 문서: 프로젝트와 worktree 대신 항목이 순서대로 놓인 폴더를 두고 채팅
중심의 Notion처럼 만든다. 구현 방법은 아직 분명하지 않다고 계획서가
적는다.[^happy-plan-folders]
- 샌드박스 환경: Happy의 자체 감독 프로세스(macOS의 Seatbelt, 리눅스의
네임스페이스)를 샌드박스 구현으로 계속 쓴다.[^happy-plan-sandbox]

이 주제들 가운데 여럿은 이미 공개 문서에 기능으로 나와 있다.
받은편지함과 죽지 않는 에이전트, 예약이 그렇고,[^happy-agents] 여러 계정을 돌려
쓰는 설정도 그렇다.[^happy-models]
계획서가 도착지이고 코드는 그에 가까워지는 중이라는 뜻으로 읽힌다.
어느 항목이 어디까지 구현되었는지는 이 문서가 코드로 확인하지 못했다.

### T3 Code의 방향은 로드맵이 아니라 기여 정책에 있다

`AGENTS.md`는 로드맵을 공유한다고 쓰지만,[^t3-agents-md] 이 문서는 저장소에서
로드맵 문서를 찾지 못했고 홈페이지의 로드맵 주소도 열리지 않았다.
확인한 것은 `CONTRIBUTING.md`가 방향을 아주 분명하게 적는다는 점이다.
- 작은 팀이 분명한 비전을 가지고 만들며, 외부 사람의 새 기능 PR에는 관심이
없다고 쓴다. 보증된(vouched) 기여자만 작은 기능 PR을 열 수 있고 동시에 세
개까지이다.[^t3-contributing]
- 병목은 창의성이나 토큰이 아니라 리뷰 여력이라고 쓰고, 기여하러 오는 사람이
너무 많으니 기여하지 말라는 조언까지 한다.[^t3-contributing]
- 자동으로 닫겠다고 밝힌 것은 새 기능, UI 개편, 새 제공자, 구조 개편(확장,
플러그인, 새 연결 방식), 새 소스 컨트롤, 다른 인증 방식, 추가 플랫폼
지원이다.[^t3-contributing]
- 기여할 이유는 버그 수정이고, 기능 요청은 Ideas 토론에 올리라고
한다.[^t3-contributing]

Ideas 토론은 사용자의 요청이 쌓이는 곳이다.
내려받은 토론 100건은 모두 이 범주였고, 제목에는 Steer와 Queue 후속 모드, 계획
모드 설정, 계획과 구현 단계에서 다른 모델이나 하네스를 고르는 기능 같은 요청이
보인다.[^t3-ideas]
토론이 로드맵으로 이어지는지는 문서에 없다.
이 문서는 변경 기록이나 계획서도 찾지 못했고, 릴리스가 855개라는 점으로 속도만
확인했다.

### 두 로드맵을 겹쳐 읽기

두 도구가 같은 곳으로 가는 부분이 있다.
둘 다 원격, 여러 화면, 여러 제공자를 핵심으로 삼는다.
Happy 계획서의 원격과 여러 Happy Agent, P2P 네트워킹은 T3 Code가 이미 가진 T3
Connect와 여러 환경 연결과 겹친다.[^happy-plan-p2p][^t3-remote]

갈라지는 부분이 더 눈에 띈다.
Happy는 확장의 문을 연다.
슬롯으로 에이전트가 앱의 자리에 내용을 꽂고, 워크렛으로 상시 연산을 붙이고,
인라인 산출물로 에이전트가 UI를 그리게
한다.[^happy-plan-slots][^happy-plan-worklets][^happy-plan-artifacts]
T3 Code는 확장과 플러그인 같은 구조 개편을 외부 기여로 받지 않겠다고 못
박는다.[^t3-contributing]
한쪽은 에이전트와 사용자가 앱을 늘려 가는 구조를, 다른 쪽은 소수 팀이 작게
유지하는 구조를 로드맵의 중심에 둔다.
이는 두 문서를 대조한 이 문서의 해석이다.

또 하나는 투명성이다.
Happy는 로드맵과 계획서와 아직 없는 목록까지 공개하지만, 그 문서들에는 날짜가
지났거나 후퇴를 스스로 적은 대목이 섞여
있다.[^happy-plan-agents][^happy-roadmap]
T3 Code는 로드맵을 공개하지 않는 대신 하지 않을 일의 목록을 공개한다.
로드맵을 보고 도구를 고르려는 사람에게 Happy는 어디로 갈지를, T3 Code는 어디로
가지 않을지를 알려 주는 셈이다.

## 철학

| 질문               | T3 Code                                 | Happy                                               |
| ------------------ | --------------------------------------- | --------------------------------------------------- |
| 스스로를 부르는 말 | 코딩 에이전트의 제어 평면, 최소한의 GUI | 모든 에이전트 아래의 하나의 하네스, 팀을 위한 한 앱 |
| 에이전트 루프      | 각 벤더의 것을 그대로 실행              | 자체 런타임이 벤더의 프롬프트와 도구로 실행         |
| 지키려는 가치      | 열림, 성능, 원격, 여러 화면             | 사람을 행복하게, 오픈소스, 모든 모델, 종속 없음     |
| 그리는 사용자      | 구독을 가진 개발자, 포크해 쓰는 사람    | 팀과 에이전트가 함께 일하는 회사                    |
| 권한               | 환경은 신뢰하고 접속 권한을 좁히는 방식 | 에이전트의 것, 샌드박스와 검토가 기본               |
| 범위               | 작게 유지, 기능은 승인된 논의 뒤        | 넓게 확장, 작업과 봇과 피드와 문서와 달력           |
| 수익               | 아무것도 팔지 않는다고 밝힘             | 지금은 집중하지 않음, 음성만 유료                   |

아래 해석은 위 표에 쓴 서술을 두 도구의 문서에서 읽어 이 문서가 대조한 것이다.

### 에이전트 루프를 누가 쥐는가

가장 큰 갈림길은 에이전트의 루프가 어디에 있느냐이다.
T3 Code는 벤더의 에이전트 프로그램을 서버가 감싸 띄우고,[^t3-agents-md] 제공자별
동작은 어댑터 뒤에 두어 정규화된 명령과 이벤트로 다룬다.[^t3-overview]
벤더가 새 기능을 내면 그 에이전트를 지원하는 한 사용자가 곧바로 쓸 수 있다는
점이 장점이다.
대가는 제공자마다 다른 차이를 화면이 그대로 떠안는다는 것이다.
권한 문서에는 Auto가 제공자마다 다르게 동작하고 모드가 없는 제공자도 있다고 적혀
있다.[^t3-perm]
GN의 click은 에이전트마다 T3 Code가 따로 지원을 만들어야 하는 방식이 아쉽다고
썼다.[^click]

Happy는 루프까지 하네스가 쥔다.
Claude에는 Claude Code의 프롬프트와 도구, GPT에는 Codex의 것을 그대로 쓰면서
권한과 샌드박스와 기록은 공통으로 둔다.[^happy-how]
모델을 바꿔도 같은 기록이 이어지고 하위 에이전트가 서로 다른 제공자를 쓸 수 있는
것은 이 구조 덕분이다.[^happy-models]
대가는 Happy가 각 벤더의 동작을 따라가는 일을 스스로 맡는다는 것이다.
벤더의 에이전트를 직접 돌리는 방식은 Happy에서 베타이다.[^happy-vs-t3]

### 권한은 누구에게 속하는가

T3 Code의 보안 문서는 서버가 샌드박스가 아니며 에이전트와 터미널이 서버 사용자의
권한으로 일부러 돈다고 밝힌다.[^t3-security]
그래서 안전은 누가 세션을 얻느냐에서 시작하고, 세션을 얻은 뒤 무엇을 할 수
있느냐는 사용자가 정하는 권한 모드가 맡는다.[^t3-security]
새 스레드의 기본값이 Full access인 것도 이 신뢰 모델과 맞는다.[^t3-perm]

Happy는 권한이 에이전트에 속해야 한다고 쓴다.
지금은 에이전트에게 말을 거는 사람이 그 권한을 쥐는데, 이를 바꾸려는 첫걸음으로
운영체제 샌드박스와 별도 에이전트의 검토를 기본에 두었다고
한다.[^happy-vision][^happy-perm]
문서는 아직 답이 아니라 시작이라고 스스로 쓴다.
팀 서버에서는 지금 모든 구성원이 같은 권한을 가진다.[^happy-perm]

두 철학의 차이는 신뢰의 단위이다.
T3 Code는 사용자와 그 컴퓨터를 신뢰하고 접속자를 좁힌다.
Happy는 컴퓨터 안의 에이전트마저 가두고 그 안에서 허용된 일을 정한다.
어느 쪽이 실제로 더 안전한지는 이 문서가 확인하지 못했다.

### 단순함과 포괄성

Theo의 글은 가장 작은 모델과 범위를 막는 것을 강조하고 기능은 승인된 논의를
거치게 한다.[^t3-agents-md][^t3-readme]
Happy의 비전은 한 회사가 필요한 것을 한 앱에 모으겠다고 하며 메시지와 통화를
다음 목표로 든다.[^happy-vision]
이 둘은 같은 선택의 양쪽 끝이다.
작게 두면 빨라지고 기여를 받기 쉽지만 팀의 협업은 다른 도구의 몫이 된다.
넓게 두면 도구 사이를 오가는 수고가 줄지만 범위가 커져 완성도를 지키기 어렵다.
이는 이 문서의 해석이며, 어느 쪽이 맞다는 증거는 아직 어느 문서에도 없다.

### 사람과 에이전트의 관계

T3 Code에서 사람은 에이전트를 조종하는 쪽이고, 앱은 그 조종을 빠르고 어디서나
가능하게 만든다.
Happy에서는 에이전트가 팀의 구성원처럼 다뤄진다.
봇에게 이름과 얼굴과 폴더가 있고,[^happy-bots] 에이전트가 결정이 필요할 때
이름을 지목해 묻고,[^happy-multiplayer] 하나의 주 에이전트만 사용자에게 말을
건다는 구상이다.[^happy-vision]
Happy의 비전 문서는 동료 대부분이 이제 에이전트라는 가정에서
출발한다.[^happy-vision]

### 옛 Happy와 T3 Code, 그리고 지금의 Happy

T3 Code가 옛 Happy에 가깝다는 관찰은 에이전트 루프의 위치에서 맞다.
둘 다 벤더가 만든 에이전트를 건드리지 않고 그 위의 창이 되려 했고, Happy 쪽 비교
글도 T3 Code가 각 벤더의 에이전트를 그대로 쓴다고 서술한다.[^happy-vs-t3]
옛 Happy는 CLI 래퍼와 폰 앱과 암호화 릴레이였고, 목표는 책상에서 쓰던 흐름을
깨지 않으며 폰으로 이어 가는 것이었다.[^show-hn]

다른 점도 분명하다.
T3 Code는 CLI 래퍼가 아니라 서버 하나에 데스크톱과 웹과 폰 클라이언트를 붙이는
구조이다.[^t3-overview]
스레드마다 worktree를 만들고 풀 리퀘스트까지 이어지는 Git 통합은 옛 Happy에 없던
것이다.[^t3-readme]
[옛 Happy 노트](../happy-coder/best-practices.md)는 Happy가 Git worktree를 직접
관리하지 않는다고 적는다.
그래서 T3 Code는 옛 Happy를 키운 것이 아니라 같은 자리에서 다른 쪽으로 넓어진
도구에 가깝다.

지금의 Happy는 거대한 하네스라는 표현이 어울린다.
에이전트 루프, 도구, 샌드박스, 세션 저장소를 런타임이 가지고 그 위에 작업과 봇과
피드를 올린다.[^happy-how][^happy-tasks]
ADE(에이전트 개발 환경)라는 이름은 Happy의 문서에서 보지 못했다.
Happy 데스크톱의 첫 릴리스가 이미 프로젝트와 파일과 변경 내용과 터미널을
담았고,[^happy-changelog] T3 Code의 문서 목차에도 스레드 관리와 터미널 기록과
소스 컨트롤이 함께 있다.[^t3-docs]
그래서 개발 화면을 한곳에 모았다는 점에서는 둘 다 ADE의 면모가 있고, 차이는 그
위에서 어디로 넓히느냐에 있다.
T3 Code는 개발자 한 사람의 에이전트 세션을 빠르고 열린 화면으로 만드는 쪽이고,
Happy는 팀의 일과 에이전트 운영 전체를 담는 쪽이다.
이는 이 문서의 해석이다.

## 한눈에 비교

각 항목의 근거는 아래 절의 각주에 있다.

| 항목                  | T3 Code                                 | Happy                                           |
| --------------------- | --------------------------------------- | ----------------------------------------------- |
| 중심 개념             | 에이전트 제어판                         | 에이전트 하네스와 사람·에이전트 팀 앱           |
| 에이전트 실행         | 각 벤더의 에이전트를 그대로 실행        | 자체 에이전트 루프가 기본, 벤더 에이전트는 베타 |
| 지원 에이전트         | Claude, Codex, Cursor, Grok, 그 밖 다수 | Claude, Codex, Grok, Gemini, ACP 에이전트       |
| 새 세션 기본 권한     | Full access                             | Auto (샌드박스와 검토)                          |
| 샌드박스              | 환경 자체는 샌드박스가 아님             | 운영체제 샌드박스가 기본                        |
| 클라이언트            | 데스크톱, 웹, iOS, Android              | 데스크톱, iOS, Android                          |
| 원격 경로             | T3 Connect, 사설망, Tailscale 등        | 릴레이(종단간 암호화) 또는 직접 연결            |
| 팀 서버와 개인 로그인 | 없음 (Happy 쪽 서술)                    | 있음, 역할 구분은 아직 없음                     |
| 제품 분석             | 기본 켜짐, 끌 수 있음 (PostHog)         | 설정에서 끌 수 있음 (PostHog)                   |

## 구조

### T3 Code는 서버 하나에 여러 클라이언트를 붙인다

T3 Code는 실행을 작업 공간을 가진 환경이 맡고 웹과 데스크톱과 모바일
클라이언트는 인증된 RPC로 조종한다고 아키텍처 문서가 쓴다.[^t3-overview]
에이전트 프로세스와 터미널과 Git과 프로젝트 파일은 서버의 것이고, 원격
클라이언트가 자기 파일 시스템이나 인증 정보로 그것을 대신해서는 안 된다고
한다.[^t3-overview]
원격 접근 문서는 그 컴퓨터가 계속 켜져 있고 닿을 수 있어야 한다고 첫머리에서
밝힌다.[^t3-remote]
서버와 보안 구조는 [T3 Code 문서](t3-code.md)에 정리했으므로 여기서는 반복하지
않는다.

### Happy는 데몬이 에이전트 루프까지 가진다

Happy의 런타임인 Happy Agent는 사용자 컴퓨터에서 도는 헤드리스
데몬이다.[^happy-how]
데몬이 에이전트 루프와 도구와 샌드박스, 모든 세션의 SQLite 데이터베이스를
가진다.[^happy-how]
데스크톱 앱은 이 데몬에 비공개 로컬 소켓으로 붙고, 앱을 닫아도 세션은 계속 돌며
데몬을 다시 시작하면 디스크에서 이어진다.[^happy-how]
폰은 암호화된 릴레이나 직접 연결로 같은 세션에 붙고, 어느 클라이언트의 메시지든
같은 세션과 대기열과 권한 경계로 들어가므로 원격 모드가 따로 없다고
한다.[^happy-how]

### 이 저장소의 Happy 노트는 이전 구조를 설명한다

[아키텍처 노트](../happy-coder/architecture.md)는 Happy를 Expo 클라이언트와
Claude Code, Codex CLI를 감싸는 래퍼로 설명한다.
현재 README는 같은 저장소의 CLI를 원래 CLI라고 부르고, 다중 모델 세션과 팀에는
데스크톱 앱으로 옮기라고 안내한다.[^happy-readme]
모바일 앱도 iOS는 Swift, Android는 Kotlin 네이티브 패키지로 적혀
있다.[^happy-readme]
그래서 `happy-coder/` 폴더의 문서 다섯 개는 CLI 래퍼 시절의 설명이고 이 문서가
다루는 현재 모습과 다르다.

## 에이전트와 모델

T3 Code가 지원하는 에이전트는 Claude Code, Codex, Cursor, OpenCode, Grok Build,
Antigravity, Kiro, Pi, Muse Code, fx와 ACP(Agent Client Protocol)
에이전트이다.[^t3-readme]
스레드 안에서 제공자를 바꾸면 이전 제공자의 스레드를 다시 이어 가되 그동안
일어난 일의 요약을 넣는 것이 기본 설계이고, 이어 가지 못하면 전체 요약으로 새
제공자 스레드를 만든다.[^t3-switch]

Happy는 Claude, Codex, Grok을 지원하고 Gemini는 Antigravity를 통해, OpenCode와
ACP 에이전트는 각자의 로그인으로 베타로 지원한다.[^happy-models]
모델을 바꾸면 기록이 유지되고, 제공자별 불투명 데이터(추론과 응답 항목)는 받은
그대로 저장해 돌려준다.[^happy-models]
하위 에이전트는 각자 모델과 추론 강도를 고르며 상속하지 않고, 한 작업에서 계획,
구현, 검토를 서로 다른 제공자에게 맡길 수 있다.[^happy-models]
같은 제공자의 계정을 여럿 등록해 `happy.toml`에서 자동으로 돌려 쓰는 설정도
있다.[^happy-models]

## 권한과 샌드박스

T3 Code의 새 스레드 기본 권한은 Full access이고, Supervised, Auto-accept edits,
Auto, Full access 네 모드를 스레드마다 고른다.[^t3-perm]
Auto는 제공자의 자동 검토에 맡기며, 그런 검토가 없는 OpenCode 같은 제공자는 묻는
쪽으로 돌아간다.[^t3-perm]
관리자는 관리 정책으로 기기에서 쓸 수 있는 모드의 상한을 정할 수 있다.[^t3-perm]

Happy의 새 세션 기본값은 Auto이다.[^happy-perm]
모든 에이전트가 운영체제 샌드박스 안에서 돌고(macOS는 Seatbelt, 리눅스는 자체
감독 프로세스의 네임스페이스와 seccomp), 쓰기는 작업 디렉터리와 임시 디렉터리에
한정되며 네트워크는 허용한 도메인만 관리형 프록시로 나간다.[^happy-perm]
경계를 넘는 행동 하나는 별도의 읽기 전용 에이전트가 사용자의 말에 비추어
허용하거나 거부하고, 파일 내용이나 웹 페이지의 문구는 허가로 치지
않는다.[^happy-perm]
Happy 문서가 스스로 적은 한계도 있다.
셸은 자격 증명 폴더를 뺀 컴퓨터의 나머지를 읽을 수 있고,[^happy-perm] MCP 서버는
샌드박스 밖에서 돌아 Auto에서는 모든 MCP 호출이 검토 대상이다.[^happy-perm]

두 도구는 기본값에서 반대편에 있다.
T3 Code는 편의를 위해 제한 없는 모드에서 시작하고, Happy는 샌드박스와 자동
검토를 켠 채 시작한다.
이 정리는 각 도구가 문서에서 밝힌 기본값을 나란히 놓은 것이며, 어느 쪽이 실제로
더 안전한지는 이 문서가 시험하지 못했다.

## 원격 접속과 모바일

T3 Connect는 공유기 포워딩 없이 다른 기기에서 호스트에 닿는 경로이고, 호스트에서
로그인해 켠다.[^t3-remote]
기본값에서는 같은 T3 Connect 계정에 로그인된 모든 기기가 연결된 컴퓨터를 열 수
있고, 새 기기 승인 옵션을 켜야 승인 절차가 생긴다.[^t3-remote]
사설망이나 Tailscale 같은 직접 경로로 한정할 수도 있다.
브라우저용 웹 클라이언트(`app.t3.codes`)와 iOS, Android 앱이 있다.[^t3-readme]

Happy는 폰에서 QR로 한 번 짝지으면 세션이 폰에 나타난다.[^happy-mobile]
폰이 계정의 기본 키를 쥐고, 내용은 한 기기에서 암호화되어 다른 기기에서 풀리며
릴레이는 불투명한 데이터만 저장하고 전달한다.[^happy-mobile]
릴레이 없이 컴퓨터에 직접 연결하는 선택지도 있다.[^happy-mobile]
폰에서는 메시지와 암호화된 이미지 보내기, 권한 요청과 질문 응답, 모델과 권한
모드 바꾸기, 디렉터리에서 새 세션 시작, 파일과 Git 변경 읽기를 할 수
있다.[^happy-mobile]
Happy 문서는 앱을 만드는 쪽이 폰을 먼저 설계한다고 쓴다.[^happy-mobile]

T3 Code에는 웹 클라이언트가 있다는 점이 눈에 띄고, Happy에는 릴레이가 암호문만
본다는 암호화 설계가 설명되어 있다는 점이 눈에 띈다.
T3 Code 쪽 중계의 신뢰 가정은 [T3 Code 문서](t3-code.md)에 정리되어 있다.

## 팀 사용

Happy는 팀 앱을 전면에 두며, 팀은 각자 로그인하는 사람 구성원과 그들이 부리는
에이전트와 봇을 함께 가리킨다.[^happy-multiplayer]
팀 서버를 한 컴퓨터에 두고 구성원이 각자 로그인하며 같은 작업과 봇과 피드와
목록과 문서와 달력을 보는 구조를 멀티플레이어 문서가
설명한다.[^happy-multiplayer]
같은 서버를 Happy 쪽 비교 문서는 구성원별 로그인과 같은 샌드박스와 검토 규칙
아래에서 쓰는 것으로 소개하면서, 팀 설정이 여러 단계이고 구성원 제거 기능이 아직
없으며 구성원의 작업이 서버의 계정으로 돈다고 스스로 밝힌다.[^happy-vs-t3]
권한 문서도 지금은 팀 서버의 모든 사람이 같은 권한을 가져서 서로 믿는 사람들끼리
쓰도록 만들었고, 역할과 감사 기록은 Happy Cloud와 함께 온다고 쓴다.[^happy-perm]

T3 Code는 팀 서버와 구성원별 로그인이 없고, 대신 스레드 하나를 보여 주는 게스트
링크가 베타로 있다.
게스트 링크는 계정 없이 브라우저에서 스레드를 따라가고, 게스트가 보낸 메시지는
사용자가 보내거나 버릴 때까지 기다린다.[^t3-guest]
이 링크는 T3 Connect가 필요하고 호스트가 켜져 있어야 한다.[^t3-guest]

## 데이터가 나가는 곳

T3 Code의 서버가 제품 분석 전송과 거부 설정과 식별을 맡는다.[^t3-analytics]
식별자는 해시한 Codex 워크스페이스, 없으면 Claude 기기 ID, 없으면 설치의 익명
ID이다.[^t3-analytics]
끄는 범위와 기본값은 [T3 Code 문서](t3-code.md)에 정리되어 있다.

Happy는 앱에서 PostHog로 가는 제품 분석이 무작위 설치 ID에 묶이고, 기능 사용과
모델과 운영체제와 앱 버전을 담으며, 메시지와 코드와 파일은 담지 않는다고
쓴다.[^happy-how]
PostHog는 요청마다 IP 주소도 본다고 같은 문서가 밝히고, 설정의 개인정보 항목에서
끌 수 있다.[^happy-how]
모델 요청은 선택한 제공자에게 사용자의 자격 증명으로 직접 가고, 앱에 호스팅된
계정이나 프로젝트 사본은 없다고 한다.[^happy-how]

## 써 본 사람들의 반응

T3 Code에서는 UX를 장점으로 꼽는 목소리가 가장 많다.
HN의 viraptor는 PR 미리보기와 git push 같은 흔한 일이 빨라지고 worktree를
네임스페이스와 함께 기본으로 만들어 주는 점이 좋다고 했다.[^viraptor]
joshka는 개발자에게 필요한 UX가 Claude와 Codex의 공식 앱보다 훨씬 강하고 이슈
트래커가 블랙홀 같지 않다고 하면서, 자신은 OpenAI에서 Codex 쪽 일을 한 편향이
있다고 스스로 밝혔다.[^joshka]
다른 시선도 있다.
hyperultra는 에이전트 메타 하네스에 T3라는 이름을 붙여 쓰게 만드는 것이 강력한
브랜딩이라고 평했고,[^hyperultra] awaseem은 Superset과 어떻게 다르냐고 물었지만
답이 달리지 않았다.[^awaseem]
GN의 3ae3ae는 같은 목적에는 paseo가 더 마음에 들었다고 했고,[^3ae3ae] click은
에이전트마다 지원을 따로 만들어야 하는 개발 방식이 아쉬워 쓰지 않는다고
했다.[^click]

Happy의 반응은 시기에 따라 갈린다.
2025년 8월 Show HN에서 becomevocal은 설치해서 외출 중에 쓰고 있으며 잘
동작한다고 했다.[^becomevocal]
2026년 1월 Ask HN에서는 안정적으로 동작하지 않아 버려진 것 같다는 글이
올라왔다.[^ask-hn]
같은 스레드에서 기여자가 새 핵심 기여자 합류와 정리 계획으로 답했다.[^marxism]
이 문서는 Happy의 최근 사용 후기를 따로 찾아 읽지 못했다.

## 선택 기준

| 원하는 것                                    | 가까운 쪽 | 근거                                                |
| -------------------------------------------- | --------- | --------------------------------------------------- |
| 브라우저에서 내 컴퓨터에 접속                | T3 Code   | 웹 클라이언트가 있다                                |
| Cursor, Pi, Muse Code를 직접 연동            | T3 Code   | 지원 에이전트 목록에 있다                           |
| 작고 빠른 화면, 열린 포크                    | T3 Code   | 성능과 열림을 지키려는 것으로 내세운다              |
| 모든 모델에 같은 샌드박스와 권한 모델        | Happy     | 공통 샌드박스와 권한을 문서가 밝힌다                |
| 새 세션부터 샌드박스와 자동 검토             | Happy     | 기본값이 Auto이다                                   |
| 한 서버에서 구성원이 각자 로그인하는 팀 사용 | Happy     | 팀 서버가 있다. 역할 구분과 구성원 제거는 아직 없다 |
| 에이전트에게 일정과 봇을 맡기는 운영         | Happy     | 봇, 예약 메시지, 피드가 있다                        |
| 릴레이가 암호문만 본다는 설계 설명           | Happy     | 암호화 방식이 문서에 있다                           |
| 공개된 로드맵과 계획서를 따라가기            | Happy     | 저장소에 로드맵과 마스터 플랜이 공개되어 있다       |
| 소수 팀이 작게 유지하는 방향에 맡기기        | T3 Code   | 외부 신규 기능 PR을 받지 않는다고 밝힌다            |

이 표는 두 도구의 문서에서 읽은 차이를 선택 상황에 옮긴 이 문서의 정리이다.
둘 다 사용해 본 경험이 아니라 문서와 소스 서술에 근거한다.

## 비평

### 방향과 로드맵은 만든 쪽의 서술에서 읽은 것이다

Happy의 비전은 아직 나오지 않은 계획을 많이 담고 있어 이미 쓸 수 있는 기능과
구분해서 읽어야 한다.[^happy-vision]
계획서는 스스로 도착지의 설명이지 코드의 현재 기록이 아니라고
밝히고,[^happy-plans-desktop] 저장소 로드맵 문서는 2026년 4월이 마지막
수정이어서 일부가 이미 지난 내용이다.[^happy-roadmap]
계획서 항목이 실제로 출시되었는지는 이 문서가 변경 기록과 공개 문서로만 대조했고
코드를 열어 확인하지 못했다.
T3 Code의 철학도 `AGENTS.md`와 README, 홈페이지, 즉 만든 쪽이 쓴 글에서
읽었다.[^t3-agents-md]
50만 명이라는 사용자 수와 Happy의 400개 게시물 같은 수치는 두 쪽 모두 집계
방식이 밝혀져 있지 않다.
이 문서의 철학 절은 그런 서술을 읽어 대조한 해석이며, 실제로 어떻게 쓰이는지는
확인하지 못했다.

### 가장 많이 쓴 비교 자료는 한쪽 만든 이의 글이다

Happy 사이트에는 `Happy vs T3 Code` 비교 문서가 있고, T3 Code에 대한 사실을
2026년 10월 27일에 소스와 문서에서 확인했다고 밝힌다.[^happy-vs-t3]
이 문서는 그 글이 서술한 사실 가운데 새 스레드의 기본 권한(Full access)과 Auto의
방식을 T3 Code 쪽 문서로 다시 확인했다.[^t3-perm]
나머지(팀 서버 없음, 전환 시 문맥 전달 방식의 수치 등)는 Happy 쪽 서술이며 이
문서가 확인하지 못했다.
같은 글에는 T3 Code가 더 나은 점(웹 클라이언트, 편집 가능한 대기 메시지, 앱 개발
도구, 게스트 링크)도 적혀 있다.[^happy-vs-t3]

### 평점과 별 수는 선택의 근거가 못 된다

Happy README는 App Store 평점 4.9와 Google Play 평점 5.0을
내세운다.[^happy-readme]
T3 Code의 별은 66,941개이고 Happy는 24,718개이지만, 별은 저장소의 나이와 관심을
보여 줄 뿐 품질을 가리지 않는다.
두 수치와 평점 모두 이 문서가 확인한 사용 경험이 아니다.

### 두 도구 모두 빠르게 바뀌고 있다

T3 Code는 야간 빌드를 포함해 855개의 릴리스가 올라왔고, Happy는 변경 기록에서
2026년 10월에만 세 건의 릴리스가 보인다.[^happy-changelog]
이 문서의 서술은 2026년 11월 20일의 한 시점이다.
특히 Happy는 하네스와 팀 기능이 아직 만들어지는 중이라고 스스로 밝히므로, 몇 달
뒤에는 구조도 철학의 우선순위도 달라질 수 있다.

### 이 문서는 어느 쪽도 실행하지 않았다

두 도구를 설치하거나 실행하지 않았다.
Happy의 샌드박스가 설명대로 경계를 지키는지, T3 Code의 권한 모드가 제공자마다
어떻게 동작하는지는 확인하지 못했다.
Happy는 저장소가 나뉘어 있어 `happy-agent`와 `happy-desktop`의 코드는 읽지
않았고 사이트와 README, 문서만 읽었다.
T3 Code의 서버 구조와 보안 모델은 앞서 [T3 Code 문서](t3-code.md)에서 소스를
읽어 정리한 것에 기댔다.

---

[^t3-readme]: GitHub pingdotgg/t3code, [T3 Code README](https://github.com/pingdotgg/t3code/blob/main/README.md), 2026-11-20 열람

[^t3-agents-md]: GitHub pingdotgg/t3code, [AGENTS.md](https://github.com/pingdotgg/t3code/blob/main/AGENTS.md), 2026-11-20 열람

[^t3-docs]: GitHub pingdotgg/t3code, [T3 Code docs](https://github.com/pingdotgg/t3code/blob/main/docs/README.md), 2026-11-20 열람

[^t3-overview]: GitHub pingdotgg/t3code, [Architecture](https://github.com/pingdotgg/t3code/blob/main/docs/internals/overview.md), 2026-11-20 열람

[^t3-home]: T3 Code, [T3 Code | The open-source control plane for coding agents](https://t3.codes/), 2026-11-20 열람

[^t3-remote]: GitHub pingdotgg/t3code, [Remote access](https://github.com/pingdotgg/t3code/blob/main/docs/user/remote-access.md), 2026-11-20 열람

[^t3-switch]: GitHub pingdotgg/t3code, [Provider Switching And Context Handoff](https://github.com/pingdotgg/t3code/blob/main/docs/orchestration-v2/provider-switching-and-context.md), 2026-11-20 열람

[^t3-perm]: GitHub pingdotgg/t3code, [Permission modes](https://github.com/pingdotgg/t3code/blob/main/docs/user/permission-modes.md), 2026-11-20 열람

[^t3-security]: GitHub pingdotgg/t3code, [Security](https://github.com/pingdotgg/t3code/blob/main/SECURITY.md), 2026-11-20 열람

[^t3-guest]: GitHub pingdotgg/t3code, [Guest links](https://github.com/pingdotgg/t3code/blob/main/docs/user/guest-links.md), 2026-11-20 열람

[^t3-analytics]: GitHub pingdotgg/t3code, [Product analytics](https://github.com/pingdotgg/t3code/blob/main/docs/internals/product-analytics.md), 2026-11-20 열람

[^happy-readme]: GitHub slopus/happy, [Happy Engineering README](https://github.com/slopus/happy/blob/main/README.md), 2026-11-20 열람

[^happy-home]: Happy Engineering, [Happy — Open-Source Team App for Claude Code, Codex, Grok, Gemini](https://happy.engineering/), 2026-11-20 열람

[^happy-vision]: Happy 문서, [Vision](https://happy.engineering/vision/), 2026-11-20 열람

[^happy-team]: Happy 문서, [Team](https://happy.engineering/team/), 2026-11-20 열람

[^happy-changelog]: Happy 문서, [Changelog](https://happy.engineering/changelog/), 2026-11-20 열람

[^happy-migrate]: Happy 문서, [Move from the Happy CLI to Happy Agent](https://happy.engineering/migrate/), 2026-11-20 열람

[^happy-tasks]: Happy 문서, [Tasks](https://happy.engineering/tasks/), 2026-11-20 열람

[^happy-bots]: Happy 문서, [Bots](https://happy.engineering/bots/), 2026-11-20 열람

[^happy-feed]: Happy 문서, [The feed](https://happy.engineering/feed/), 2026-11-20 열람

[^happy-computers]: Happy 문서, [Computers](https://happy.engineering/computers/), 2026-11-20 열람

[^happy-chief]: Happy 문서, [Chief of Staff](https://happy.engineering/chief-of-staff/), 2026-11-20 열람

[^happy-agents]: Happy 문서, [Agents That Never Die](https://happy.engineering/agents/), 2026-11-20 열람

[^happy-multiplayer]: Happy 문서, [Multiplayer](https://happy.engineering/multiplayer/), 2026-11-20 열람

[^happy-how]: Happy 문서, [How It Works](https://happy.engineering/how-it-works/), 2026-11-20 열람

[^happy-models]: Happy 문서, [Models & Subscriptions](https://happy.engineering/models/), 2026-11-20 열람

[^happy-perm]: Happy 문서, [Permissions & Sandbox](https://happy.engineering/permissions/), 2026-11-20 열람

[^happy-mobile]: Happy 문서, [Mobile Access](https://happy.engineering/mobile/), 2026-11-20 열람

[^happy-vs-t3]: Happy 문서, [Happy vs T3 Code](https://happy.engineering/t3-code/), 2026-11-20 열람

[^happy-roadmap]: GitHub slopus/happy, [Happy Roadmap](https://github.com/slopus/happy/blob/main/docs/roadmap.md), 2026-11-20 열람

[^happy-roadmap-old]: GitHub slopus/happy, [Roadmap](https://github.com/slopus/happy/blob/main/docs/experimental/roadmap.md), 2026-11-20 열람

[^happy-plans-desktop]: GitHub slopus/happy-desktop, [How master plans work](https://github.com/slopus/happy-desktop/blob/main/master-plans/00-master-plan.md), 2026-11-20 열람

[^happy-plan-remote]: GitHub slopus/happy-desktop, [Remote Happy Agent](https://github.com/slopus/happy-desktop/blob/main/master-plans/01-remote-happy-agent.md), 2026-11-20 열람

[^happy-plan-multi]: GitHub slopus/happy-desktop, [Multiple Happy Agents](https://github.com/slopus/happy-desktop/blob/main/master-plans/05-multiple-happy-agents.md), 2026-11-20 열람

[^happy-plan-artifacts]: GitHub slopus/happy-desktop, [Inline artifacts](https://github.com/slopus/happy-desktop/blob/main/master-plans/08-inline-artifacts.md), 2026-11-20 열람

[^happy-plan-chat]: GitHub slopus/happy-desktop, [Chat surface](https://github.com/slopus/happy-desktop/blob/main/master-plans/09-chat-surface.md), 2026-11-20 열람

[^happy-plan-slots]: GitHub slopus/happy-desktop, [Slots](https://github.com/slopus/happy-desktop/blob/main/master-plans/04-slots.md), 2026-11-20 열람

[^happy-plan-browser]: GitHub slopus/happy-desktop, [In-app browser](https://github.com/slopus/happy-desktop/blob/main/master-plans/11-in-app-browser.md), 2026-11-20 열람

[^happy-plan-windows]: GitHub slopus/happy-desktop, [Windows](https://github.com/slopus/happy-desktop/blob/main/master-plans/12-windows.md), 2026-11-20 열람

[^happy-plan-providers]: GitHub slopus/happy-agent, [Master plan 5: provider protocols](https://github.com/slopus/happy-agent/blob/main/master-plans/05-providers.md), 2026-11-20 열람

[^happy-plan-inbox]: GitHub slopus/happy-agent, [Master plan 6: Inbox](https://github.com/slopus/happy-agent/blob/main/master-plans/06-inbox.md), 2026-11-20 열람

[^happy-plan-agents]: GitHub slopus/happy-agent, [Master plan 7: Agents](https://github.com/slopus/happy-agent/blob/main/master-plans/07-agents.md), 2026-11-20 열람

[^happy-plan-schedule]: GitHub slopus/happy-agent, [Master plan 10: Scheduling](https://github.com/slopus/happy-agent/blob/main/master-plans/10-scheduling.md), 2026-11-20 열람

[^happy-plan-accounts]: GitHub slopus/happy-agent, [Master plan 11: account routing](https://github.com/slopus/happy-agent/blob/main/master-plans/11-account-routing.md), 2026-11-20 열람

[^happy-plan-worklets]: GitHub slopus/happy-agent, [Master plan 17: Worklets](https://github.com/slopus/happy-agent/blob/main/master-plans/17-worklets.md), 2026-11-20 열람

[^happy-plan-plugins]: GitHub slopus/happy-agent, [Master plan 13: Plugins](https://github.com/slopus/happy-agent/blob/main/master-plans/13-plugins.md), 2026-11-20 열람

[^happy-plan-p2p]: GitHub slopus/happy-agent, [Master plan 15: P2P networking](https://github.com/slopus/happy-agent/blob/main/master-plans/15-p2p-networking.md), 2026-11-20 열람

[^happy-plan-folders]: GitHub slopus/happy-agent, [Master plan 18: folders and documents](https://github.com/slopus/happy-agent/blob/main/master-plans/18-folders-and-documents.md), 2026-11-20 열람

[^happy-plan-sandbox]: GitHub slopus/happy-agent, [Master plan 8: sandbox environments](https://github.com/slopus/happy-agent/blob/main/master-plans/08-sandbox-environments.md), 2026-11-20 열람

[^happy-teamserver]: Happy 문서, [Run a Happy Team Server](https://happy.engineering/guides/team-server/), 2026-11-20 열람

[^happy-voice]: Happy 문서, [Talk to Your Agents: Voice with ElevenLabs](https://happy.engineering/voice/), 2026-11-20 열람

[^t3-contributing]: GitHub pingdotgg/t3code, [Contributing](https://github.com/pingdotgg/t3code/blob/main/CONTRIBUTING.md), 2026-11-20 열람

[^t3-ideas]: GitHub pingdotgg/t3code, [Ideas discussions](https://github.com/pingdotgg/t3code/discussions/categories/ideas), 2026-11-20 열람

[^show-hn]: Hacker News, [Show HN: Happy Coder – End-to-End Encrypted Mobile Client for Claude Code](https://news.ycombinator.com/item?id=44904039), 2025-08-14

[^ask-hn]: Hacker News, [Ask HN: How do you AI code from your phone?](https://news.ycombinator.com/item?id=46742298), 2026-01-24

[^marxism]: <https://news.ycombinator.com/item?id=46757485>

[^becomevocal]: <https://news.ycombinator.com/item?id=44912638>

[^viraptor]: <https://news.ycombinator.com/item?id=50176139>

[^joshka]: <https://news.ycombinator.com/item?id=50179892>

[^hyperultra]: <https://news.ycombinator.com/item?id=50066029>

[^awaseem]: <https://news.ycombinator.com/item?id=47294778>

[^3ae3ae]: <https://news.hada.io/topic?id=35612#cid68000>

[^click]: <https://news.hada.io/topic?id=35612#cid67992>
