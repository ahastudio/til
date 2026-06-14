# apple/container — Apple Silicon Mac의 네이티브 리눅스 컨테이너

<https://github.com/apple/container>

HN 토론: <https://news.ycombinator.com/item?id=44229348> (769점, 409개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/h0pge0/container_tool_for_creating_and_running>

Apple이 공개한 `container`는 Apple Silicon Mac에서 리눅스 컨테이너를 경량 VM으로 실행하는 Swift 기반 유틸리티다.
OCI 호환 컨테이너 이미지를 사용하며, Apple Silicon Mac과 macOS 26 이상을 요구한다.
2024년 6월 첫 공개 이후 정확히 1년 만인 2025년 6월 9일에 1.0.0 버전이 릴리스됐다.

## 소개

`container`는 macOS의 Virtualization 프레임워크를 활용해 컨테이너마다 독립된 경량 VM을 생성한다.
공유 커널 방식이 아닌 컨테이너당 VM 격리를 제공하므로 보안 경계가 명확하다.
GitHub에서 36.7k 스타, 1k 포크를 기록하며 빠르게 주목받았다.

각 VM은 macOS 위에서 동작하는 경량 init 시스템을 통해 기동된다.
Lobste.rs의 wezm[^wezm]은 이 init 시스템이 Swift로 작성된 Linux 바이너리이며,
musl을 통해 완전히 정적 링크된다는 점을 짚었다.
Swift 코드가 Linux 사용자 공간 바이너리로 빌드된다는 사실 자체가 흥미롭다.

저장소에 `.claude/` 디렉토리가 포함되어 있어 Claude Code를 통한 AI 기여를 공식적으로 장려하고 있다.
Apple이 오픈소스 프로젝트에 AI 협업 도구를 직접 포함시킨 점이 눈길을 끈다.

## Container Machine

1.0.0의 핵심 신기능은 Container Machine이다.
Container Machine은 호스트와 긴밀하게 통합된 장수명(long-lived) 리눅스 환경을 제공한다.
일반 컨테이너가 단발성 프로세스 실행에 최적화된 것과 달리,
Container Machine은 개발 환경으로서 지속적으로 사용하는 리눅스 VM처럼 동작한다.
호스트 디렉토리 마운트, 네트워크 통합 등 macOS와의 밀접한 연동이 특징이다.

## 주요 기능

1.0.0에서 추가되거나 개선된 기능은 다음과 같다.

- **TOML 설정 파일**: `UserDefaults` 기반 설정을 대체하는 파일 시스템 기반 설정 체계
- **구조화된 출력**: 컨테이너, 이미지, 네트워크, 볼륨에 대한 JSON/YAML/TOML 포맷 지원
- **`--stop-signal` 옵션**: 컨테이너 실행 시 종료 신호 지정 가능
- **`container cp` 명령어**: 호스트와 컨테이너 간 파일 전송
- **네트워크 개선**: XPC 연결을 리스(lease)로 활용해 IP 주소 누수 문제 수정

### 호환성 변경 사항

- `container system property` 서브커맨드 제거
- JSON/YAML/TOML 출력 구조 재편
- 애플리케이션 버전 0 XPC API 지원 중단

## 분석

`container`는 Docker Desktop 없이 Apple Silicon에서 네이티브로 리눅스 컨테이너를 실행하려는 수요를 정확히 겨냥한다.
GeekNews 커뮤니티에서는 기존 Lima, Colima와 비교하며 교체 가치가 있는지 의문을 제기하는 목소리가 있었다.
차별점은 Apple이 직접 만든 1st-party 도구라는 점과 컨테이너당 VM 격리 모델이다.

OrbStack 개발자는 자사의 Rust 스택이 동적 메모리 관리를 제공하는 반면 Container Machine에는 없다고 지적했다.
성능 측면에서도 Podman, Colima, OrbStack($96/year)과 비교하는 논의가 이어졌다.

Lobste.rs의 dgl[^dgl]은 커널 구성 측면에서 주목할 만한 사실을 지적했다.
Apple이 커스텀 커널을 사용하지 않고 업스트림 Linux(현재 6.14.9)를 그대로 사용한다는 점,
그리고 구조적으로 Kata Containers와 유사하다는 점이다.
WSL1이 시스템 콜 호환 레이어 방식을 포기한 것도 같은 맥락으로 언급됐다.
masklinn[^masklinn]은 WSL1의 실패 원인이 시스템 콜 복잡도보다
Windows와 Unix의 파일시스템 시맨틱 차이에 있다고 분석했다.
대소문자 구분, 심볼릭 링크 처리 등 근본적인 의미론적 불일치 때문에
가상화 없이 완전한 호환성을 달성하는 것은 사실상 불가능하다는 시각이다.
호스트 볼륨 I/O 성능이 Lima처럼 저하되는지를 묻는 질문도 있었는데, 이는 macOS 기반 컨테이너 도구의 공통 약점이다.

기본 CPU와 RAM 할당값이 너무 보수적이라는 비판도 있었다.
초기 설정만으로 실용적인 개발 환경을 구성하기 어렵다면 채택 장벽이 높아진다.

HN에서 spockz[^spockz]는 이 프로젝트가 Firecracker 스타일의 경량 커널과 Apple Virtualization 프레임워크의 혼합처럼 보인다고 설명했다.
자체 커널을 갖추면서도 Firecracker 커널도 선택 가능한 구조에 대해 어떤 이점이 있는지 — 더 작은 풋프린트인지, Apple Silicon 특성을 활용하는지 — 를 질문했으며, 실제 성능 수치가 부족하다는 아쉬움을 드러냈다.

### 팀 개발 환경에서의 현실적 한계

paxys[^paxys]는 컨테이너마다 독립 VM과 독립 IP를 부여하는 모델이 macOS에서는 깔끔하지만,
Linux나 Windows에는 동등한 구현이 없다는 점을 지적했다.
팀원 중 한 명이라도 Mac이 아닌 환경을 사용한다면 로컬 개발 모델 자체가 성립하지 않으므로,
Docker Compose를 대체하는 용도로는 현실적으로 어렵다는 결론이다.
이에 대해 dontdoxxme는 포드(pod) 개념만 없을 뿐 Kubernetes와의 대응 관계는 성립하며,
나중에 포드 지원을 추가하면 Compose 유사 설정도 가능하다고 반론했다.

### 동적 메모리 관리 현황

현재 각 VM은 할당된 RAM을 macOS에 돌려주는 동적 메모리 회수 기능이 없다.
dontdoxxme[^dontdoxxme-mem]는 공식 기술 문서를 인용하며 아직 미구현 상태임을 확인했다.
컨테이너를 여러 개 띄울수록 메모리 압박이 커지는 구조적 약점이다.

## 비평

Lobste.rs의 ianloic[^ianloic]은 "언제부터 'container'가 'Linux VM 실행'을 의미하게 됐냐"고 직접적으로 물었다.
Apple이 macOS 컨테이너화를 드디어 제공한다고 기대했다가 실망했다는 반응이다.
sknebel[^sknebel]은 대부분의 개발자가 Linux 컨테이너만 접해봤기 때문에 그것이 사실상 표준으로 굳었다고 반박했지만,
"native macOS 컨테이너도 있으면 좋겠다"고 덧붙였다.
Microsoft의 Windows 컨테이너, FreeBSD의 OCI 컨테이너가 이미 존재하는 상황에서,
Apple만 자사 OS 네이티브 컨테이너를 제공하지 않는다는 지적은 유효하다.

$HOME 노출에 대한 보안 우려는 짚고 넘어갈 필요가 있다.
호스트 홈 디렉토리를 컨테이너나 VM에 마운트하는 편의 기능은 격리 보안의 근본 목적과 충돌한다.
컨테이너당 VM 모델로 커널 격리를 제공하면서도 파일 시스템 경계를 느슨하게 허용한다면 격리의 의미가 퇴색된다.

Container Machine이 제공하는 “호스트 통합”의 범위와 기본값이 구체적으로 문서화되어 있지 않으면,
사용자는 자신도 모르게 넓은 공격 면적을 열어두게 된다.

Docker Desktop 대체재로서의 가능성은 있지만, 1.0.0은 아직 생태계 도구 지원이나 성능 데이터가 부족하다.
Lima/Colima나 OrbStack에 익숙한 사용자가 이전하려면 명확한 성능 비교 자료가 먼저 필요하다.

### 중첩 가상화 지원 부재

sitole[^sitole]은 VM 안에서 다시 VM을 띄우는 중첩 가상화(nested virtualization)가 가능한지 물었다.
Apple 문서에 따르면 이 기능은 M3 이상 칩에서만 지원되며(`VZGenericPlatformConfiguration.isNestedVirtualizationSupported`),
`container` CLI에는 이를 활성화하는 플래그가 보이지 않는다.
KVM을 게스트 VM 내에서 실행하고 싶은 개발자에게는 여전히 장벽이 존재한다.

## 인사이트

Apple이 직접 1st-party 컨테이너 도구를 내놓은 것은 개발자 도구 생태계에 대한 플랫폼 차원의 의지 표명이다.
Container Machine 개념은 단순한 컨테이너 실행을 넘어, 개발 환경 전체를 VM으로 격리하는 방향이다.
이는 Dev Container나 GitHub Codespaces의 로컬 오프라인 버전에 가깝다.

TOML 기반 설정 체계로의 전환은 장기적으로 버전 관리와 팀 공유에 유리하다.
`UserDefaults`에 묶인 설정은 재현성이 낮고 자동화하기 어렵기 때문이다.

AI 기여 도구를 저장소에 직접 포함시킨 것은 오픈소스 협업 방식의 변화를 암시한다.
Apple이 커뮤니티 기여를 AI 도구와 함께 공식화하는 방향은 앞으로 다른 대형 오픈소스 프로젝트에도 영향을 줄 수 있다.

### 오픈소스 협업 태도의 변화

HN의 pxc[^pxc]는 저장소 README에 "기여를 환영하고 장려한다"는 문구가 포함된 점을 Apple로서는 매우 이례적이라고 평가했다.
WebKit은 KHTML의 적대적 포크에서 출발했고, Darwin은 필요에 따라 코드를 공개하는 방식이었다는 점에서,
이번 프로젝트가 진정한 커뮤니티 협업의 선례가 될 수 있다는 기대를 표명했다.
holycrapwhodat[^holycrapwhodat]은 이를 반박하며, WebKit은 2005년부터 이미 공개 버그 트래커와 패치 리뷰를 갖춘 정식 오픈소스 프로젝트였고
Swift도 2015년부터 그러했다고 지적했다.
2025년의 이 프로젝트는 Apple 오픈소스 역사의 연장선이지 출발점이 아니라는 시각이다.

### Linux의 사실상 표준 지위

sho_hn[^sho_hn]은 이제 두 주요 데스크톱 OS(Windows의 WSL, macOS의 `container`)가 모두 리눅스 VM을 공식 지원한다는 사실에서
"Linux가 이겼다"는 역설적 결론을 도출했다.
리눅스 자체가 데스크톱을 정복한 것이 아니라, 리눅스 syscall API가 사실상 가장 광범위한 애플리케이션 인터페이스가 됐다는 의미다.

### Apple 클라우드 진출의 포석

jbverschoor[^jbverschoor]는 이 프로젝트를 Xcode Cloud와 연결해 해석했다.
Amazon과의 대규모 클라우드 계약 종료 시점과 맞물려, Apple이 자사 하드웨어 — 특히 Apple Silicon — 에서 실행되는
컨테이너 기반 클라우드 호스팅 서비스를 준비하는 포석일 수 있다는 시각이다.
개발자가 컨테이너를 빌드하고 Apple 인프라에 바로 배포하는 수직 통합 시나리오다.

---

[^spockz]: <https://news.ycombinator.com/item?id=44232063>
[^paxys]: <https://news.ycombinator.com/item?id=44230893>
[^dontdoxxme-mem]: <https://news.ycombinator.com/item?id=44233808>
[^sitole]: <https://news.ycombinator.com/item?id=44231308>
[^pxc]: <https://news.ycombinator.com/item?id=44231055>
[^holycrapwhodat]: <https://news.ycombinator.com/item?id=44231894>
[^sho_hn]: <https://news.ycombinator.com/item?id=44230671>
[^jbverschoor]: <https://news.ycombinator.com/item?id=44230109>
[^wezm]: <https://lobste.rs/s/h0pge0/container_tool_for_creating_and_running#bicwzd>
[^dgl]: <https://lobste.rs/s/h0pge0/container_tool_for_creating_and_running#rh6top>
[^masklinn]: <https://lobste.rs/s/h0pge0/container_tool_for_creating_and_running#antpp6>
[^ianloic]: <https://lobste.rs/s/h0pge0/container_tool_for_creating_and_running#kyvc6w>
[^sknebel]: <https://lobste.rs/s/h0pge0/container_tool_for_creating_and_running#kwrq4j>
