# Procexp-Mac는 Sysinternals Process Explorer를 macOS로 옮긴 Microsoft 저장소이고, 첫 반응은 기능보다 모양과 라이선스에 쏠렸다

<https://github.com/microsoft/Procexp-Mac>

HN 토론: <https://news.ycombinator.com/item?id=50433216> (235점, 78개 댓글)

GN 토론: <https://news.hada.io/topic?id=36980>

## 소개

Procexp-Mac는 Windows의 Sysinternals Process Explorer를 macOS용 앱으로 만든 Microsoft의 GitHub 저장소이다.
Swift로 쓰였고 2026년 7월 6일에 만들어졌다.
2026년 11월 읽은 값으로 별 944개, 포크 29개, 열린 이슈 11개이고, 저장소 메타데이터에 라이선스 항목이 없다.
2026년 11월 5일에 `ProcExp 1.0.0` 릴리스가 올라와 있다.
이 문서는 저장소 README 전문과 GitHub API 값, HN 스레드를 읽었다.
앱을 설치하거나 실행해 보지는 않았다.

## 기능

README가 설명하는 기능은 다음과 같다.

- 프로세스 트리를 실시간으로 보여 주고, 아래쪽 창에서 선택한 프로세스의 상세를 본다.
- 속성 창에는 TCP/IP 탭과, 코드 서명과 VirusTotal 조회를 묶은 Security 탭이 있다.
- System Information 창에서 시스템 전체 그래프를 본다.
- macOS 메뉴 막대에 File, Options, View, Process, Find, Window, Help 명령이 있다.

macOS가 공개 API로 열지 않는 값은 지어내지 않고 빈칸으로 둔다고 README가 밝힌다.
같은 사용자의 프로세스가 아니면 일부 세부 정보는 권한 있는 도우미(privileged helper)가 켜져 있을 때만 보인다.

## 구조와 설치

프로세스 표본 추출은 `libproc`과 `sysctl`을 쓰는 권한 없는 경로로 하고, 소켓 열거와 GPU 사용률, 코드 서명과 SHA-256과 Keychain과 VirusTotal, launchd 자동 시작 감지가 각각 별도 Swift 모듈로 나뉜다.
권한이 필요한 부분은 루트로 도는 데몬이 맡고, 앱은 `SMAppService`와 XPC로 이 데몬을 등록하고 호출한다.
시스템 설정의 로그인 항목에서 사용자가 승인해야 켜진다.
등록이 거부되면 앱은 권한 없는 모드로 계속 돈다고 한다.

빌드는 xcodegen으로 프로젝트를 만든 뒤 스크립트로 한다.
개발용 번들 식별자와 공식 번들 식별자가 따로 있고, 개발용 설치는 서명용 임시 키체인을 만들어 쓴다.
공식 배포는 Developer ID 서명과 공증 절차를 거친다.

## 분석

### 중심 주장은 Windows의 관찰 도구를 macOS의 공개 API 한계 안에서 옮긴다는 것이다

이 프로젝트의 선택은 두 가지로 읽힌다.
하나는 Windows 사용자에게 익숙한 화면(프로세스 트리, 아래쪽 상세, 탭 속성)을 그대로 가져온 것이다.
다른 하나는 macOS가 허용하지 않는 값을 추측으로 채우지 않는 것이다.
HN의 한 댓글은 Process Explorer가 소켓과 파일 핸들과 라이브러리와 스레드까지 보여 주는 관찰 능력 때문에 값지다며, 공급자에 대한 편견 때문에 지나치지 말라고 했다.[^tonymet]
README의 한계 문구를 보면 macOS 쪽에서는 그 관찰 폭이 줄어들 수밖에 없다.
이 문서는 줄어든 폭이 실제로 어느 정도인지 앱을 돌려 확인하지 못했다.

### 권한 있는 도우미는 가치와 위험이 같은 곳에 있다

다른 사용자와 시스템 프로세스를 보려면 루트 데몬이 필요하다.
관찰 도구가 루트 권한을 얻는 구조이므로, 이 데몬의 XPC 경계가 어떻게 닫혀 있는지가 도구 신뢰의 핵심이다.
README는 도우미 구조를 `Helper/README.md`에 둔다고 안내하고, 이 문서는 그 파일을 열어 보지 않았다.

## 비평

### 도우미를 설치한 뒤 목록이 비었다는 보고가 둘 있다

한 사용자는 도우미를 설치하자 프로세스 트리가 비었다고 했고,[^jherskovic]
다른 사용자는 앱이 처음에는 프로세스를 많이 나열했지만 세 주요 열이 비어 있었고, 도우미를 설치하고 로그인 항목에서 승인한 뒤에는 모든 창이 재시작 뒤에도 비었다고 하며 아직 깊은 알파 같다고 평했다.[^rekabis]
또 다른 사용자는 CPU 정렬이 동작하지 않고, Processes 열을 눌러도 트리 보기와 평면 보기가 바뀌지 않는다고 적었다.[^mannycalavera42]
셋 모두 개인 보고이고 재현 조건(macOS 버전, 설치 경로)이 적혀 있지 않다.
다만 README가 도우미 등록의 여러 실패 경로(재설치 때 승인 기억이 지워짐, 임시 서명 거부)를 직접 적고 있어서, 이 부분이 마찰이 큰 영역이라는 점과는 맞는다.

### 라이선스 파일이 없고, 기여자에 Copilot이 있다

저장소에는 LICENSE 파일이 없고 7월 9일에 정책 봇이 연 1번 이슈가 열려 있다.[^mzs]
한 댓글은 Copilot이 기여자로 나열되어 있어 사람이 코드를 라이선스할 권리가 있는지 의심스럽다고 했다.[^runset]
이는 법적 판단이 아니라 댓글의 추측이고, 이 문서는 기여자 목록을 확인하지 못했다.
라이선스가 없으면 코드를 읽을 수는 있어도 재사용 조건이 정해지지 않는다는 점은 사실이다.

### 반응의 상당수가 모양에 관한 것이었다

스레드의 짧은 댓글 다수는 화면이 Mac답지 않다는 평이었다.
한 사용자는 Windows 판의 직접 이식이라 당연하고 개발자 도구라면 괜찮다고 했고,[^gwbas1c]
다른 사용자는 아이콘 도구 막대와 어긋난 표 머리글과 색 선택이 Microsoft다운 모습이라고 했다.[^ricardobeat]
한 댓글은 기능 목록이 LLM이 만든 문장 같다고 비꼬았는데, 메뉴 막대 명령까지 늘어놓은 README 문장을 가리킨 것이다.[^tlhunter]
미적 평가는 도구의 관찰 능력과 별개이고, 이 문서는 어느 쪽도 직접 확인하지 못했다.

### 기존 대안과의 비교가 비어 있다

스레드는 Objective-See의 TaskExplorer와 비교를 물었고,[^jollyllama]
Dave Plummer의 TMOG를 대안으로 들었다.[^gilgoomesh]
Activity Monitor는 프로세스 트리 단위로 메모리를 합산하지 못한다는 불만이 있었고, 한 사용자는 그 자리를 채우는 메모리 탭 대체품을 직접 만들었다고 소개했다.[^tomaskafka]
이 저장소 README는 이 도구들과의 비교를 하지 않는다.

## 인사이트

### 도입 전 점검은 세 가지다

이 앱을 쓰기 전에 확인할 것은 이렇다.
도우미를 설치해도 되는 기기인가(루트 데몬이 상주한다),
라이선스가 없는 코드를 회사 환경에 들여도 되는가,
macOS 버전에서 목록이 비는 보고가 재현되는가이다.
셋 다 이 문서가 확인하지 못했다.

### 리눅스에도 같은 요구가 있다는 신호가 있다

스레드에서 두 사용자는 리눅스용으로 비슷한 도구를 Rust와 `/proc`, systemd, netlink로 만들고 있다고 소개했다.[^kburman][^hparadiz]
한 답글은 systemd 의존이 init이 다른 배포판에서 쓸모를 제한한다고 지적했다.[^pschastain]
Process Explorer류의 수요가 Windows 밖에서도 크다는 것을 보여 주는 정황이다.

### 확인할 관찰

이 프로젝트의 방향을 가를 관찰은 세 가지이다.
LICENSE 이슈가 닫히는지,
도우미 설치 뒤 목록이 비는 문제가 고쳐지는지,
릴리스가 1.0.0 이후에도 이어지는지이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^tonymet]: <https://news.ycombinator.com/item?id=50444845>

[^jherskovic]: <https://news.ycombinator.com/item?id=50444424>

[^rekabis]: <https://news.ycombinator.com/item?id=50435752>

[^mannycalavera42]: <https://news.ycombinator.com/item?id=50444912>

[^mzs]: <https://news.ycombinator.com/item?id=50445406>

[^runset]: <https://news.ycombinator.com/item?id=50447430>

[^gwbas1c]: <https://news.ycombinator.com/item?id=50445657>

[^ricardobeat]: <https://news.ycombinator.com/item?id=50448936>

[^tlhunter]: <https://news.ycombinator.com/item?id=50448700>

[^jollyllama]: <https://news.ycombinator.com/item?id=50444771>

[^gilgoomesh]: <https://news.ycombinator.com/item?id=50449075>

[^tomaskafka]: <https://news.ycombinator.com/item?id=50447946>

[^kburman]: <https://news.ycombinator.com/item?id=50444341>

[^hparadiz]: <https://news.ycombinator.com/item?id=50445202>

[^pschastain]: <https://news.ycombinator.com/item?id=50449139>
