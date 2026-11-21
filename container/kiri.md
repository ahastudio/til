# Kiri: Rust로 만든 컨테이너 런타임

<https://runkiri.com/>

<https://github.com/libracoder/kiri>

HN 토론: <https://news.ycombinator.com/item?id=50504077> (95점, 36개 댓글)

GN 토론: <https://news.hada.io/topic?id=37496>

## 소개

Kiri는 Mac, Windows, Linux에서 Docker Desktop을 대신한다고 소개하는 컨테이너 런타임이다.
홈페이지는 현재 베타이고 버전 0.2.2이며 Mac용(Apple silicon, macOS 14 이상)을 내려받을 수 있다고 한다.
Rust로 쓰였다고 밝히고, docker CLI와 Compose와 Docker API가 지금처럼 동작한다고 한다.
이 문서는 홈페이지 전문과 HN 스레드, 저장소 README를 읽었다.
저장소의 `ROADMAP.md`, `RELEASES.md`, `SECURITY.md`, `docs/features.md`, `docs/development.md`, 리눅스와 윈도우 벤치마크 기록(`bench/`)도 읽었다.
Kiri를 설치하거나 벤치마크를 재현하지는 않았고 소스 코드는 읽지 않았다.
홈페이지의 일부 그래프에는 “측정한 값이 곧 이 표본을 대체한다”는 문구가 있어, 모든 막대가 실측은 아니다.

저장소는 GitHub의 libracoder/kiri이고 홈페이지 필드가 `https://runkiri.com`이다.
GitHub API로 2026년 11월 21일에 읽은 값은 다음과 같다.
Apache-2.0 라이선스, Rust, 별 11,709개, 포크 546개, 열린 이슈와 PR 189개이다.
저장소는 2026년 11월 2일에 만들어졌고 마지막 푸시는 11월 20일이며 최신 릴리스는
11월 19일의 v0.2.2이다.
첫 릴리스 v0.1.14가 저장소를 만든 날 나왔고, API가 돌려준 릴리스는 v0.2.2까지 모두 7개이다.
언어별 코드량은 Rust가 약 4.7MB로 가장 크고, HTML과 JavaScript가 그다음이다.
기여자는 35명으로 집계되고, 가장 많은 한 사람(libracoder)이 158건을 차지한다.
README는 이름이 이그보어 단어로 작다는 뜻이라고 밝히고, GeekNews 글은 이 도구를
무료 ngrok 대안을 내장한 경량 Docker Desktop 대체재로 소개한다.

## 주장과 구성

홈페이지가 내세우는 핵심은 이렇다.

- 속도: `docker run`이 Kiri에서 22ms, Docker Desktop에서 178ms, Colima에서 152ms, OrbStack에서 279ms이며, 모든 엔진을 CPU 2개와 메모리 8GB로 제한했다고 한다. 비교 세 가지는 같은 docker CLI와 Docker 기본 브리지 네트워크를 쓰고, Apple Silicon Mac 한 대의 전체 실행에서 나온 중앙값이다. 도커 API로는 컨테이너 전체 수명주기가 3.1ms라고 하며, 22ms의 대부분은 docker CLI가 시작되는 시간이라고 밝힌다.
- 구조: macOS에서는 Apple의 Virtualization.framework로 사용자 지정 커널과 작은 Rust init(PID 1)이 있는 리눅스 VM을 하나 띄우고, 호스트와 게스트는 vsock으로 통신한다. VM 안의 Kiri 데몬이 각 컨테이너를 `clone3`로 만든다. Linux에서는 VM 없이 자기 커널에서 같은 데몬이 돌고, Windows에서는 WSL2 안에서 돈다. 콜드 부팅이 112ms(일반 커널 810ms), vsock 왕복이 31마이크로초라고 한다.
- 기존 도구와의 차이: OrbStack과 Docker Desktop은 컨테이너 시작이 프로그램 다섯 개와 각자의 소켓을 거치고 실행 중인 컨테이너마다 shim 프로세스가 상주하는 반면, Kiri는 데몬 하나가 커널을 직접 부르고 컨테이너마다 남는 프로세스가 없다고 한다. OrbStack의 shim이 컨테이너 143개에서 1.13GB를 쓴다는 수치를 든다.
- 기능: Compose와 이미지 검색과 당겨 받기(amd64는 Rosetta), BuildKit 빌드와 이미지 취약점 검사, `kiri k8s start`로 약 20초에 k3s 클러스터(kind도 가능), `kiri machine create`로 리눅스 머신, `kiri share`로 `runkiri.cloud`의 공개 링크, `.kiri.local` 이름과 자체 인증 기관의 HTTPS, 쓰지 않는 메모리 반환과 1분 유휴 뒤 VM 수면(데몬 약 15MB, 깨우는 데 0.15초), OrbStack과 Docker Desktop에서의 이전이 있다.
- 앱: Mac에서는 AppKit과 시스템 WebKit, Windows에서는 Win32와 WebView2로 만든 네이티브 앱이라 Electron이 아니라고 한다. 창은 15개 언어를 지원한다.
- 공유 링크의 경고: 공유 링크를 처음 방문하면 Kiri의 경고 페이지가 먼저 떠서 링크가 은행으로 위장하지 못하게 한다고 한다.
- 저장소 README의 수치: README는 알파인 이미지로 `true`를 실행하고 지우는 일을 30회 반복한 중앙값을 든다. Docker Engine API 기준 Kiri 2.55ms, Docker Desktop 213ms, OrbStack 380ms이고 docker CLI 기준 Kiri 14.2ms, Docker Desktop 243ms, OrbStack 442ms이다. Docker Desktop보다 약 80배 빠르다고 쓰고, 방법과 모든 수치는 저장소의 `bench/results.json`에 있다고 한다.
- README의 그 밖의 서술: 데몬이 약 15MB이고 VM이 60초 유휴 뒤 잠들며 깨는 데 0.15초가 걸린다고 쓴다. 게스트 커널은 약 10MB의 사용자 지정 커널이고 PID 1은 약 900KB의 Rust 에이전트이며, runc, shim, dockerd 없이 `clone3`로 컨테이너를 시작한다고 한다.
- 로드맵: 0.3.0에서 Tailscale과 Cloudflare Tunnel을 통한 공유, 0.4.0에서 Coolify 지원을 예고한다.
- 리눅스와 윈도우 측정: 저장소의 `bench/` 기록은 리눅스에서 Kiri가 `run --rm alpine true`를 188ms에 마쳐 Docker Engine(697ms), Podman(1105ms), nerdctl(631ms), Colima(635ms), Docker Desktop(714ms)보다 빠르다고 적는다. 바인드 마운트 1GB 쓰기는 1467MB/s 대 Docker Engine 819MB/s이고, 읽기는 3851MB/s 대 1307MB/s이다. 윈도우에서는 `docker run`이 78ms 대 Docker Desktop 491ms이다. 이 측정은 모두 WSL 2 안의 우분투(리눅스)와 윈도우 11 한 대에서 한 번의 세션으로 얻은 값이라고 기록이 밝힌다.
- 개발 문서가 적는 구조: `docs/development.md`는 게스트 안의 PID 1이 약 900KB의 정적 Rust 바이너리이고, 컨테이너를 `clone3` 한 번으로 새 네임스페이스와 cgroup에 만든다고 적는다. 그 뒤 overlayfs, `pivot_root`, 권한 집합(capabilities)과 seccomp 필터를 설정하고, 네트워크는 손으로 쓴 rtnetlink와 nf_tables 메시지로 설정한다. runc도 shim도 dockerd도 없다고 한다. 커널은 allnoconfig에서 만든 10MB짜리이고 패치가 네 개 붙는다.
- 릴리스 방식: `RELEASES.md`는 릴리스를 비공개 저장소의 빌드 워크플로가 만든다고 밝힌다. 서명 키가 있어 공개 CI에 둘 수 없다는 이유이다. 비공개 저장소는 공개 저장소의 태그를 읽기 전용 키로 받아 빌드한다. 맥 앱은 Developer ID로 서명되고 공증을 거치며, 윈도우 설치 파일은 Authenticode 서명을 준비 중이라 현재는 서명되지 않았다고 한다. 빌드는 바이트 단위로 재현되지 않는다고 한다.
- 로드맵 문서의 현재 항목: 0.2.3은 윈도우의 WSL 재시작 수정 잔여분과 네트워크 주소 선택이다. 0.4.0의 Coolify 지원을 막는 항목으로 레이어 60개 이상 이미지의 시작 실패, `--pid host`, Traefik의 포트 탐지가 적혀 있다. 로드맵은 계획이 날짜가 아니라 버전에 묶여 있다고 밝힌다.
- 라이선스: 코드는 Apache-2.0이고 게스트 커널은 Linux(GPL-2.0)이며, “Kiri” 이름과 로고는 라이선스에 포함되지 않아 포크는 다른 이름과 로고로 해야 한다고 한다.

## 분석

### 중심 주장은 컨테이너 시작 경로를 줄이면 빨라진다는 것이다

설명이 구체적인 부분은 경로이다. 다섯 개 프로그램을 거치는 구조를 데몬 하나와 vsock 한 채널로 줄였다는 서술이다.
이 설명은 홈페이지가 주장하는 구조이고, HN의 한 댓글은 이 구조를 문서(`docs.runkiri.com/features`)에서 읽고 의문을 달았다. 컨테이너 스케줄링을 맡는 데몬이 VM과 직접 일하고 게스트 에이전트가 사실상 init인데, 그러면 Kiri가 자체 컨테이너 런타임을 전부 구현한 것이냐 containerd 같은 것을 쓰느냐는 질문이다.[^i_v]
같은 의문을 다른 댓글도 냈다. 8배 주장을 가능하게 하는 구조상의 결정이 무엇이냐는 질문이다.[^gempir]
저장소의 `docs/development.md`가 이 질문에 답한다.
게스트의 PID 1인 Rust 에이전트가 `clone3` 한 번으로 컨테이너를 만들고, 네트워크는 커널 메시지를 직접 보내 설정하며, runc와 shim과 dockerd가 없다고 적는다.
즉 저장소 문서는 containerd 같은 기존 구성 요소를 쓰지 않고 컨테이너 런타임을 자체 구현했다고 밝히는 셈이다.
이 문서는 소스 코드를 읽지 않아 문서의 서술이 코드와 맞는지는 확인하지 못했다.
자체 구현은 시작 경로를 줄이는 대신 runc가 오래 다듬어 온 호환성과 격리 동작을 Kiri가 직접 책임진다는 뜻이다. 이는 이 문서의 해석이다.

### 8배의 의미는 시작 시간이다

한 댓글은 “8배 빠르다”가 컨테이너가 빨리 도는 것인지 도구가 빠른 것인지 물었고,[^cholindo]
답글은 컨테이너 시작 시간을 재는 것이라고 설명하며, 며칠에 한 번 하는 일에서 200ms는 체감되지 않고 메모리 절약도 컨테이너 100개 넘게에서의 수치라고 했다.[^tpetry]
OrbStack의 장점인 빠른 바인드 마운트는 비교되지 않았다는 지적도 있다.[^tpetry]
홈페이지는 이 비교가 컨테이너 시작과 메모리 상주량이라고 스스로 밝히고, 바인드 마운트나 빌드 속도는 수치로 제시하지 않는다.

## 비평

### 비교 대상과 방법

한 댓글은 대부분의 도커 이후 컨테이너 기술이 도커보다 빠르다며 Podman, systemd-nspawn, incus 같은 기준과 macOS에서는 Apple containers와 OrbStack과 Colima와 비교해야 한다고 했다.[^d3xt3r]
다른 댓글은 Podman과 비교했느냐고 물었고, 답글은 홈페이지의 “Podman 대안” 페이지를 가리켰으며 다시 그 페이지에 Podman의 시간이 없으니 Podman보다 빠르다고 결론 낼 수 없다고 했다.[^forty][^hn_throw2025][^abc42]
한 댓글은 홈페이지의 벤치마크 명령 `docker run --rm alpine true`가 캐시된 이미지의 데운 시작을 재는 것이어서 실제로 사람들이 체감하는 콜드 스타트와 다르다고 했고, 코드를 들여다보니 정리를 응답 뒤로 미루는 동작 등 우려되는 점이 있다고 썼다.[^binsquare]
이 문서는 벤치마크를 재현하지 못했고 그 기본 실행 조건을 확인하지 못했다.
macOS에서 Colima(vz)보다 빠르냐고 물은 댓글도 있었는데,[^user-error] 홈페이지는 Colima의 `docker run`을 152ms로 적는다. 이 비교는 홈페이지가 제시한 것이다.

### 용어에 대한 혼란

한 댓글은 “컨테이너 엔진”과 “컨테이너 런타임”과 “컨테이너 관리자”가 가리키는 대상이 도구마다 달라 혼란스럽다며 헤드라인의 용어를 문제 삼았다.[^5g_activated]
다른 댓글은 도커와 Podman에도 이미 런타임 개념이 있어 헤드라인이 혼란스럽다고 했다.[^sureglymop]
홈페이지는 “데스크톱 앱과 데몬”이라는 의미로 “런타임”을 쓰는 것으로 보인다. 이 문서는 이 용어 사용을 정리하지 않는다.

### AI로 만든 코드라는 의심은 근거가 엇갈린다

스레드에서 가장 큰 가지는 이 프로젝트가 AI가 만든 저질 결과물이 아니냐는 논쟁이었다.
한 댓글은 또 하나의 컨테이너 런타임처럼 보인다며 슬롭이 아니라고 설득해 달라고 했고,[^newjazz]
한 답글은 코드베이스를 보니 많이 AI로 만든 것 같지 않거나 흔적을 많이 지웠다며 슬롭이 아니라고 했다.[^webstrand]
다른 답글은 약 2주 만에 20만 줄이 생겼고 코드에 줄표(em dash)가 가득하다며 AI로 만들지 않았다면 일부러 그렇게 보이게 한 것이라고 했고,[^wavemode]
기여자가 실제 사람인지 모르겠다는 댓글,[^quaffcode-kiri]
홈페이지를 “화려한 애니메이션으로 읽기를 막는 슬롭”이라고 한 댓글도 있었다.[^dimpalo]
한 댓글은 Kiri의 문서가 VM 하나가 아니라 컨테이너마다 (마이크로)VM이라고 틀리게 적었다고 지적하며 사실상 OrbStack 복제라고 했다.[^jbverschoor]
이 모든 것은 인상이고 이 문서는 소스 코드를 읽지 않아 판단하지 못한다. 20만 줄이라는 규모를 읽지 않고 신뢰하기 어렵다는 우려도 스레드에 있었다.[^classified]
이 우려에는 이런 문제가 LLM 이전에도 십 년 넘게 있었다는 답글,[^vmg] 이제는 코드를 생성해 주는 도구가 있어 그 마찰이 사라졌다는 재답글,[^classified-2] 토큰이 충분하면 LLM이 모든 줄을 읽어 준다는 반론이 붙었다.[^brabel]
저장소 API 기준 기여자는 35명이고 한 사람이 158건을 차지한다. 이 수치는 사람이 쓴 코드인지 아닌지와는 무관한 정보이다.
만든 사람(libracoder)은 스레드에서 기여자가 실제 사람이라고 답했고,[^libracoder-contrib] OrbStack보다 빠르고 성능이 낫다고 답했다.[^libracoder-orbstack]
두 답글 모두 근거를 덧붙이지 않았다.
저장소는 GitHub API 기준 별 11,709개를 가졌고 이 수치는 기여자의 실재 여부와 별개의 정보이다.

### 홈페이지와 README의 수치가 다르다

홈페이지는 8배, README는 약 80배라고 쓴다.
두 수치의 측정 대상이 다르다.
홈페이지의 22ms 대 178ms는 `docker run --rm alpine true`를 docker CLI로 실행한
시간이다.
README의 2.55ms 대 213ms는 같은 일을 Docker Engine API로 한 시간이다.
홈페이지는 22ms의 대부분이 docker CLI가 시작되는 시간이라고 스스로 밝힌다.
README의 같은 표에서 CLI 기준은 14.2ms 대 243ms로 약 17배이다.
이는 이 문서의 계산이며, 세 수치는 측정 방식에 따라 8배에서 80배까지 달라지는
같은 비교의 다른 표현이다.

언어 수도 다르다.
홈페이지는 창이 15개 언어를 지원한다고 쓰고 README는 38개 언어를 쓴다.
저장소의 `crates/kiri/src/ui/lang` 폴더에는 번역 JSON 파일이 37개 있다.
README의 38개는 여기에 영어를 더한 수로 보이고, 이는 이 문서의 추정이다.
홈페이지는 언어 이름을 열다섯 개 나열한다. 홈페이지 쪽이 갱신되지 않았을 가능성이 있지만 확인하지는 못했다.

### 리눅스 비교에는 조건과 약점이 함께 적혀 있다

`bench/ubuntu-2026-10-26.md`는 이 비교를 베어메탈이 아니라 WSL 2 위의 우분투에서 했다고 밝힌다.
같은 기록은 Kiri가 지는 항목도 적는다.
게시된 포트(published port)를 통한 iperf3 처리량이 Kiri 10.3Gbit/s, Docker Engine 100.7Gbit/s로 Kiri가 열 배 낮았다.
Kiri가 포트 중계를 사용자 공간에서 하기 때문이라고 설명한다.
호스트에서 컨테이너로 보내는 표준 입력은 에이전트가 대기 입력을 4MiB로 제한해 나머지를 버려서, 200MB를 보냈는데 1.2MB만 도착했고 그 칸은 “유효하지 않음”으로 표시되었다.
같은 날 두 수정을 브랜치에서 시험한 결과도 이어 붙어 있다.
수정 뒤 입력은 200MB/s로 전부 도착했고 포트 처리량은 약 56~58Gbit/s로 올랐다. 다만 `run`은 188ms에서 214~230ms로, 바인드 마운트 쓰기는 1467MB/s에서 883~970MB/s로 느려졌고, 기록은 이를 하루치 소음 범위로 해석한다.
README의 리눅스 표는 수정 전 값(10.3Gbit/s)을 싣고 있어, 같은 저장소 안에서도 수정 전후 값이 갈린다.
또 같은 기록은 이 WSL 배포판에서 docker CLI 자체의 기동이 185~190ms라서 `docker` 기준 수치는 대부분 CLI의 시간이라고 밝힌다.
윈도우 기록도 같은 입력 제한 때문에 “호스트에서 컨테이너로” 칸을 비교할 수 없다고 적는다.
측정과 한계를 저장소가 스스로 적는 것은 장점이다. 다만 홈페이지의 “8배”에는 이런 단서가 따라붙지 않는다.

### 문서가 스스로 적은 미완성 항목

`docs/features.md`와 `ROADMAP.md`에는 사용자가 부딪힐 항목이 적혀 있다.
레이어가 60개 이상인 이미지는 시작에 실패한다(로드맵의 #253).
BuildKit의 `--add-host name:host-gateway`는 실패하고, 내장 빌더가 생길 때까지 주소를 직접 쓰라고 한다.
윈도우에서는 TCP를 쓰지 않는다. WSL의 localhost 중계가 반닫기(half-close)를 떨어뜨려 `docker run`이 출력을 잃기 때문이라고 한다.
Mac에서는 잠자기 동안 USB 장치가 컨테이너에서 빠진다.
리눅스에서 `kiri` 그룹 구성원은 `docker` 그룹처럼 root와 같은 권한을 갖는다고 문서가 밝힌다.
홈페이지의 “Docker Desktop을 대신한다”는 표현에 비하면 이 목록은 현재 단계가 베타라는 말의 구체적 내용이다.

### 배포 방식에서 읽는 신뢰 문제

Kiri는 특권 컨테이너와 로컬 인증 기관을 다루고 스스로 업데이트하는 프로그램이다.
`SECURITY.md`는 그래서 보안 보고가 매우 중요하다고 쓴다.
`RELEASES.md`에 따르면 릴리스 파일은 공개 저장소가 아니라 비공개 저장소의 빌드가 만든다.
저장소 소스를 직접 빌드할 수는 있지만 결과물이 바이트 단위로 같지 않아, 배포 파일이 공개 소스에서 나왔다는 것을 사용자가 비트 단위로 검증할 수는 없다.
윈도우 설치 파일은 서명되지 않아 SmartScreen 경고가 뜬다고 문서가 밝힌다.
맥은 서명과 공증이, 리눅스는 `SHA256SUMS-linux`가 검증 수단이다.
같은 문서는 VS Code나 Chrome도 같은 방식이라고 비교한다. 이는 문서의 주장이고, 이 문서는 그 비교를 따로 확인하지 않았다.
HN 스레드에는 20만 줄을 누가 읽어 악성 코드가 없는지 확인하느냐는 우려가 있었다.[^classified]
이 비공개 빌드 경로는 소스를 읽은 사람에게도 배포 파일이 그 소스에서 나왔는지를 따로 확인해야 하는 단계를 남긴다. 이는 이 문서의 해석이다.

### 네이티브라는 표현

홈페이지는 맥과 윈도우의 창을 AppKit, 시스템 WebKit, Win32, WebView2로 만든 네이티브 앱이라 하고 Electron이 아니라고 한다.
한 댓글은 웹 앱이 아니라면서 웹뷰를 쓰는 것은 네이티브가 아니라고 반박했다.[^pjmlp]
어느 정의를 택하느냐의 문제이고, 이 문서는 소스 코드를 읽지 않아 창의 어느 부분이 웹뷰인지 확인하지 못했다.

### 이름에 대한 농담

“Kiri”는 페르시아어와 프랑스의 치즈 브랜드, 이그보어 등 여러 뜻으로 읽힌다는 댓글이 이어졌고, 제품의 성격과는 무관하다.[^ksajadi][^wiether]

## 인사이트

### 성능 주장을 읽는 법

Kiri의 수치는 한 Mac에서 한 번 전체 실행한 중앙값이고, 측정 대상은 `docker run`의 시작이다.
사용자에게 필요한 것은 시작 시간 외에 바인드 마운트 속도, 이미지 빌드, 네트워크, 메모리의 평소 상주량, 안정성이다.
이 중 홈페이지가 수치로 보이는 것은 시작과 상주 메모리뿐이다.
비교 대상을 고를 때는 본인의 작업(컨테이너를 얼마나 자주 띄우는지, 마운트를 얼마나 쓰는지)에 맞는 항목부터 보는 것이 맞다. 이는 이 문서의 제안이다.

### 베타 도구를 쓸 때의 점검 항목

0.2.2 베타이므로 이미지와 볼륨을 옮기기 전에 기존 환경을 보존하고, 공유 링크(`kiri share`)로 내보내는 컨테이너에는 민감한 데이터를 두지 않으며, 코드와 문서가 어긋나는 부분(VM 구조에 대한 지적)이 해소되는지 지켜본다.
홈페이지가 공유 링크의 경고 페이지를 설명하지만 접근 제어나 인증의 세부는 이 문서가 확인하지 못했다.

### 확인할 관찰

이 도구를 평가할 관찰은 세 가지이다.
콜드 스타트와 바인드 마운트와 빌드에서의 독립 벤치마크,
컨테이너 런타임을 자체 구현했는지와 보안 모델(격리 수준)에 대한 설명,
저장소의 코드와 문서가 서로 맞는지와 기여자 구성이다.
추가로 리눅스 포트 처리량과 입력 제한 수정이 병합되어 릴리스에 들어갔는지와, 윈도우 설치 파일에 서명이 붙었는지도 볼 만하다.
모두 이 문서가 확인하지 못했다.

---

[^i_v]: <https://news.ycombinator.com/item?id=50504902>

[^cholindo]: <https://news.ycombinator.com/item?id=50504621>

[^tpetry]: <https://news.ycombinator.com/item?id=50506015>

[^d3xt3r]: <https://news.ycombinator.com/item?id=50504660>

[^forty]: <https://news.ycombinator.com/item?id=50505046>

[^hn_throw2025]: <https://news.ycombinator.com/item?id=50505365>

[^abc42]: <https://news.ycombinator.com/item?id=50505932>

[^binsquare]: <https://news.ycombinator.com/item?id=50506627>

[^5g_activated]: <https://news.ycombinator.com/item?id=50505540>

[^sureglymop]: <https://news.ycombinator.com/item?id=50504982>

[^newjazz]: <https://news.ycombinator.com/item?id=50504155>

[^webstrand]: <https://news.ycombinator.com/item?id=50504221>

[^wavemode]: <https://news.ycombinator.com/item?id=50504736>

[^quaffcode-kiri]: <https://news.ycombinator.com/item?id=50504238>

[^dimpalo]: <https://news.ycombinator.com/item?id=50506102>

[^jbverschoor]: <https://news.ycombinator.com/item?id=50504231>

[^classified]: <https://news.ycombinator.com/item?id=50505114>

[^ksajadi]: <https://news.ycombinator.com/item?id=50504154>

[^wiether]: <https://news.ycombinator.com/item?id=50505387>

[^libracoder-contrib]: <https://news.ycombinator.com/item?id=50520298>

[^libracoder-orbstack]: <https://news.ycombinator.com/item?id=50520316>

[^gempir]: <https://news.ycombinator.com/item?id=50506007>

[^user-error]: <https://news.ycombinator.com/item?id=50504273>

[^vmg]: <https://news.ycombinator.com/item?id=50505196>

[^classified-2]: <https://news.ycombinator.com/item?id=50508775>

[^brabel]: <https://news.ycombinator.com/item?id=50505231>

[^pjmlp]: <https://news.ycombinator.com/item?id=50511067>
