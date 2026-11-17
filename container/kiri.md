# Kiri: Rust로 만든 컨테이너 런타임

<https://runkiri.com/>

HN 토론: <https://news.ycombinator.com/item?id=50504077> (65점, 31개 댓글)

## 소개

Kiri는 Mac, Windows, Linux에서 Docker Desktop을 대신한다고 소개하는 컨테이너 런타임이다.
홈페이지는 현재 베타이고 버전 0.2.1이며 Mac용(Apple silicon, macOS 14 이상)을 내려받을 수 있다고 한다.
Rust로 쓰였다고 밝히고, docker CLI와 Compose와 Docker API가 지금처럼 동작한다고 한다.
이 문서는 홈페이지 전문과 HN 스레드를 읽었다.
Kiri를 설치하거나 벤치마크를 재현하지는 않았다.
홈페이지의 일부 그래프에는 “측정한 값이 곧 이 표본을 대체한다”는 문구가 있어, 모든 막대가 실측은 아니다.

## 주장과 구성

홈페이지가 내세우는 핵심은 이렇다.

- 속도: `docker run`이 Kiri에서 22ms, Docker Desktop에서 178ms, Colima에서 152ms, OrbStack에서 279ms이며, 모든 엔진을 CPU 2개와 메모리 8GB로 제한했다고 한다. 비교 세 가지는 같은 docker CLI와 Docker 기본 브리지 네트워크를 쓰고, Apple Silicon Mac 한 대의 전체 실행에서 나온 중앙값이다. 도커 API로는 컨테이너 전체 수명주기가 3.1ms라고 하며, 22ms의 대부분은 docker CLI가 시작되는 시간이라고 밝힌다.
- 구조: macOS에서는 Apple의 Virtualization.framework로 사용자 지정 커널과 작은 Rust init(PID 1)이 있는 리눅스 VM을 하나 띄우고, 호스트와 게스트는 vsock으로 통신한다. VM 안의 Kiri 데몬이 각 컨테이너를 `clone3`로 만든다. Linux에서는 VM 없이 자기 커널에서 같은 데몬이 돌고, Windows에서는 WSL2 안에서 돈다. 콜드 부팅이 112ms(일반 커널 810ms), vsock 왕복이 31마이크로초라고 한다.
- 기존 도구와의 차이: OrbStack과 Docker Desktop은 컨테이너 시작이 프로그램 다섯 개와 각자의 소켓을 거치고 실행 중인 컨테이너마다 shim 프로세스가 상주하는 반면, Kiri는 데몬 하나가 커널을 직접 부르고 컨테이너마다 남는 프로세스가 없다고 한다. OrbStack의 shim이 컨테이너 143개에서 1.13GB를 쓴다는 수치를 든다.
- 기능: Compose와 이미지 검색과 당겨 받기(amd64는 Rosetta), BuildKit 빌드와 이미지 취약점 검사, `kiri k8s start`로 약 20초에 k3s 클러스터(kind도 가능), `kiri machine create`로 리눅스 머신, `kiri share`로 `runkiri.cloud`의 공개 링크, `.kiri.local` 이름과 자체 인증 기관의 HTTPS, 쓰지 않는 메모리 반환과 1분 유휴 뒤 VM 수면(데몬 약 15MB, 깨우는 데 0.15초), OrbStack과 Docker Desktop에서의 이전이 있다.
- 앱: Mac에서는 AppKit과 시스템 WebKit, Windows에서는 Win32와 WebView2로 만든 네이티브 앱이라 Electron이 아니라고 한다. 창은 15개 언어를 지원한다.
- 공유 링크의 경고: 공유 링크를 처음 방문하면 Kiri의 경고 페이지가 먼저 떠서 링크가 은행으로 위장하지 못하게 한다고 한다.

## 분석

### 중심 주장은 컨테이너 시작 경로를 줄이면 빨라진다는 것이다

설명이 구체적인 부분은 경로이다. 다섯 개 프로그램을 거치는 구조를 데몬 하나와 vsock 한 채널로 줄였다는 서술이다.
이 설명은 홈페이지가 주장하는 구조이고, HN의 한 댓글은 이 구조를 문서(`docs.runkiri.com/features`)에서 읽고 의문을 달았다. 컨테이너 스케줄링을 맡는 데몬이 VM과 직접 일하고 게스트 에이전트가 사실상 init인데, 그러면 Kiri가 자체 컨테이너 런타임을 전부 구현한 것이냐 containerd 같은 것을 쓰느냐는 질문이다.[^i_v]
이 문서는 문서 페이지를 열지 못해 답을 확인하지 못했다.

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
이 모든 것은 인상이고 이 문서는 저장소를 열어 보지 않아 판단하지 못한다. 20만 줄이라는 규모를 읽지 않고 신뢰하기 어렵다는 우려도 스레드에 있었다.[^classified]

### 이름에 대한 농담

“Kiri”는 페르시아어와 프랑스의 치즈 브랜드, 이그보어 등 여러 뜻으로 읽힌다는 댓글이 이어졌고, 제품의 성격과는 무관하다.[^ksajadi][^wiether]

## 인사이트

### 성능 주장을 읽는 법

Kiri의 수치는 한 Mac에서 한 번 전체 실행한 중앙값이고, 측정 대상은 `docker run`의 시작이다.
사용자에게 필요한 것은 시작 시간 외에 바인드 마운트 속도, 이미지 빌드, 네트워크, 메모리의 평소 상주량, 안정성이다.
이 중 홈페이지가 수치로 보이는 것은 시작과 상주 메모리뿐이다.
비교 대상을 고를 때는 본인의 작업(컨테이너를 얼마나 자주 띄우는지, 마운트를 얼마나 쓰는지)에 맞는 항목부터 보는 것이 맞다. 이는 이 문서의 제안이다.

### 베타 도구를 쓸 때의 점검 항목

0.2.1 베타이므로 이미지와 볼륨을 옮기기 전에 기존 환경을 보존하고, 공유 링크(`kiri share`)로 내보내는 컨테이너에는 민감한 데이터를 두지 않으며, 코드와 문서가 어긋나는 부분(VM 구조에 대한 지적)이 해소되는지 지켜본다.
홈페이지가 공유 링크의 경고 페이지를 설명하지만 접근 제어나 인증의 세부는 이 문서가 확인하지 못했다.

### 확인할 관찰

이 도구를 평가할 관찰은 세 가지이다.
콜드 스타트와 바인드 마운트와 빌드에서의 독립 벤치마크,
컨테이너 런타임을 자체 구현했는지와 보안 모델(격리 수준)에 대한 설명,
저장소의 코드와 문서가 서로 맞는지와 기여자 구성이다.
셋 모두 이 문서가 확인하지 못했다.

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
