# Colima — macOS와 Linux를 위한 경량 컨테이너 런타임

> Container runtimes on macOS (and Linux) with minimal setup.

<https://colima.run/>

<https://github.com/abiosoft/colima>

HN 토론: <https://news.ycombinator.com/item?id=35983349> (132점, 55개 댓글)

## 소개

Colima는 macOS와 Linux에서 최소 설정으로 컨테이너 런타임을 실행하는 오픈소스 도구다.
이름은 “Containers on Lima”의 약자로,
Linux Machines(Lima) 위에 컨테이너 워크로드를 얹는 구조를 그대로 드러낸다.
Intel 및 Apple Silicon Mac과 Linux에서 동작하고,
Docker, Containerd, Incus 세 가지 런타임을 선택할 수 있으며,
선택적으로 Kubernetes를 함께 띄울 수 있다.

설치는 Homebrew(`brew install colima`), MacPorts, Nix, Mise 등 여러 패키지 매니저를 통해 가능하다.
실행은 `colima start` 한 줄로 끝나고,
필요하면 `colima start --edit`로 설정 파일을 직접 수정한다.
기본 사양은 CPU 2개, 메모리 2GB, 디스크 100GB이며,
`--cpu`, `--memory`, `--disk`, `--runtime` 같은 플래그로 즉시 조정한다.

런타임별로 클라이언트가 분리된다.
Docker 런타임은 별도로 `brew install docker`로 CLI를 깔아야 하고,
Containerd는 `nerdctl`을 사용하며 `colima nerdctl install`로 PATH에 등록한다.
Kubernetes는 `--kubernetes` 플래그로 활성화하고 `kubectl`로 접근한다.
Incus는 v0.7.0부터 추가되어 컨테이너와 VM을 모두 다루지만,
VM 기능은 Apple Silicon M3 이상에서만 지원된다.

v0.10.0부터는 Apple Silicon과 macOS 13+ 환경에서 GPU 가속 컨테이너를 지원한다.
이때는 `krunkit` VM 타입을 선택하고,
Docker Model Runner(기본) 또는 Ramalama 백엔드로 모델을 실행한다.
`colima model run gemma3` 같은 명령으로 Docker AI Registry, HuggingFace, Ollama 레지스트리의 모델을 곧바로 돌릴 수 있다.

라이선스는 MIT이고,
커뮤니티는 GitHub Discussions와 CNCF Slack의 `#colima` 채널을 사용한다.
GitHub Sponsors, Buy Me a Coffee, Patreon으로 후원을 받는 개인 주도 프로젝트다.

## 분석

### Docker Desktop 유료화의 빈자리를 메운 위치 선정

Colima의 존재 이유는 기술적 혁신이 아니라 시장 공백이다.
Docker Desktop이 2021년 8월부터 일정 규모 이상의 기업에 유료 라이선스를 요구하면서,
“맥에서 컨테이너를 어떻게 띄울 것인가”라는 질문은 다시 열린 문제가 되었다.
Colima는 그 시점에 등장해
“가장 단순한 대안”이라는 자리를 빠르게 차지했다.

Colima 자체는 새 가상화 기술을 만들지 않는다.
Lima가 만든 macOS용 Linux VM 위에 Docker/Containerd/Incus 런타임을 끼워 넣고,
포트 포워딩과 볼륨 마운트를 자동화하는 얇은 래퍼다.
즉 Colima의 경쟁력은 코드의 양이 아니라
“무엇을 안 만들지”에 대한 결정이다.
VM은 Lima에, 런타임은 Docker/Containerd에 맡기고,
자신은 사용자 경험만 책임진다.

이런 설계는 Docker Desktop의 정반대 지점에 선다.
Docker Desktop은 VM, GUI, Kubernetes, 확장 시스템까지 한 묶음으로 제공하는 통합 제품이지만,
Colima는 CLI 한 줄로 환경을 띄우고 끄는 일에만 집중한다.
“덜 갖춘 제품”이 “더 갖춘 제품”의 자리를 침식하는 전형적인 다운마켓 진입이다.

### 런타임 다중화는 표준화보다 정치적 결정에 가깝다

Colima가 Docker, Containerd, Incus를 동시에 지원하는 것은 기술적 호기심처럼 보이지만,
실제로는 컨테이너 생태계의 분열 상태에 대한 베팅이다.
Docker가 표준이던 시절에는 런타임 선택지가 의미가 없었다.
하지만 Kubernetes가 dockershim을 제거하고 containerd를 1급 시민으로 채택한 이후,
“내 로컬 환경의 런타임”과 “프로덕션의 런타임”이 갈라지는 사례가 늘었다.

Colima는 이 갈라짐을 받아들이고 양쪽 모두를 같은 CLI로 띄울 수 있게 한다.
`--runtime containerd`를 켜면 `nerdctl`로 작업하고,
Kubernetes 모드에서는 `k8s.io` 네임스페이스를 자동으로 다룬다.
이건 단순한 옵션이 아니라
“개발자가 프로덕션 런타임을 로컬에서도 그대로 쓸 수 있게 한다”는 입장 표명이다.

Incus까지 끌어들인 것은 더 흥미롭다.
Incus는 컨테이너와 VM을 모두 다루는 LXD 포크인데,
m3 이상 Apple Silicon에서만 VM이 동작한다는 단서가 붙는다.
이 제약은 Colima가 단순히 “되는 것은 다 지원한다”가 아니라,
하드웨어 발전 곡선에 맞춰 기능을 풀어내는 단계적 전략을 따른다는 신호다.

### krunkit과 모델 러너의 결합은 새로운 카테고리 진입이다

`colima model run gemma3` 같은 명령은 표면적으로는 편의 기능이지만,
구조적으로는 Colima가 “컨테이너 도구”에서 “로컬 AI 워크로드 매니저”로 영역을 넓히는 출발점이다.
GPU 가속을 위해서는 일반 Lima의 QEMU 기반 VM이 아니라
`krunkit`이라는 별도 VM 타입을 골라야 한다.
즉 AI 워크로드는 컨테이너 워크로드와 다른 가상화 스택을 요구한다는 사실을 인정한 것이다.

이 결합이 의미하는 바는 두 가지다.
첫째, Colima는 Docker Model Runner와 Ramalama 같은 외부 도구를
자신의 런타임 추상화 안에 흡수해 사용자에게 단일 명령으로 노출한다.
이는 과거 `docker run`이 cgroup, namespace, overlayfs 같은 기술을 묶어 보여줬던 방식과 같다.

둘째, 이 방향은 OrbStack과 Docker Desktop이 모두 진입하려는 영역과 정면으로 겹친다.
“로컬에서 LLM을 어떻게 띄울 것인가”는 곧 컨테이너 도구의 차기 전선이 되었고,
Colima는 무료 오픈소스 진영에서 그 자리를 선점하려 한다.

### “최소 설정”이라는 표어는 책임 분산을 미덕으로 포장한다

README가 반복해서 강조하는 “minimal setup”은 사용자 경험의 단순함만이 아니라,
프로젝트의 책임 범위를 좁히는 선언이기도 하다.
VM은 Lima 책임, 런타임은 Docker/containerd 책임, 모델 실행은 Model Runner 책임이다.
Colima는 이들을 묶는 얇은 결합 층만 책임진다.

이 구조는 빠른 기능 추가를 가능하게 한다.
Incus, krunkit, Model Runner 같은 신기능이
Colima 본체의 변경 없이 옵션 플래그로 흡수되는 패턴은 이런 책임 분산의 결과다.
반면 같은 구조는 디버깅의 책임도 분산시킨다.
어디서 문제가 났는지 사용자가 직접 가르고 들어가야 하는 상황은
“minimal setup”이라는 표어가 가리는 비용이다.

## 비평

### “minimal setup”은 정상 동작 경로에만 적용된다

README와 사이트가 반복하는 단순함은
모든 컴포넌트가 의도대로 동작할 때의 이야기다.
Lima의 VM 부팅, Docker/containerd 데몬의 기동, 포트 포워딩, 볼륨 마운트가 한 번에 맞물려야
`colima start` 한 줄의 약속이 성립한다.
하지만 이 체인이 한 곳에서 끊어지면 사용자는 곧바로
Lima 로그, QEMU/krunkit 옵션, gRPC 소켓 권한, macOS 파일시스템 매핑 같은 층위로 내려가야 한다.

이 구조는 “구성 요소가 다 외부 프로젝트”라는 설계의 필연적 부작용이다.
Colima는 자기 영역의 코드를 늘리는 대신,
경계에서 발생하는 오류를 추적할 책임을 사용자에게 넘긴다.
GitHub Issues에 반복적으로 등장하는 마운트 권한, 네트워크, krunkit 호환성 이슈는
이 비용이 실제로 청구되고 있다는 증거다.

HN 토론에서도 같은 패턴이 확인된다.
한 사용자는 Podman과 Colima 모두 "적당히 복잡한" Docker Compose 파일을 돌리지 못해
하루를 통째로 디버깅에 쓰고 결국 Docker Desktop으로 돌아갔다고 보고했다[^tootie].
다른 사용자는 Colima를 도입하긴 했지만,
sshfs 캐시 지연 때문에 현재 작업 디렉터리를 마운트한 컨테이너에서 파일을 생성하는 단위 테스트가
간헐적으로 실패해 테스트 코드 쪽을 "파일이 나타날 때까지 기다리는" 방식으로 고쳐야 했다고 적었다[^segfaltnh].
또 다른 사용자는 시계 표류(clock drift) 이슈[^JonMR]까지 지적했다.
모두 "정상 경로의 단순함"이라는 약속 바깥에서 발생하는 비용이고,
README는 이 비용을 명시하지 않는다.

문제는 README가 이 비용을 명시하지 않는다는 점이다.
“sensible defaults”라는 표현은 정상 경로의 매끄러움만 강조하고,
실패 경로에서의 학습 곡선은 침묵 속에 둔다.
오픈소스 프로젝트의 documentation에서 흔한 누락이지만,
Docker Desktop을 떠나는 사용자에게 가장 필요한 정보가 빠진 셈이다.

### Apple Silicon 차별과 “교차 플랫폼”의 모순

README는 Intel과 Apple Silicon, Linux를 모두 지원한다고 광고하지만,
정작 가장 흥미로운 기능들은 Apple Silicon에 묶여 있다.
GPU 가속은 Apple Silicon + macOS 13+에서만,
Incus VM은 M3 이상에서만 동작한다.
“여러 플랫폼에서 같은 경험”이라는 인상과 실제 기능 매트릭스 사이에는 분명한 간격이 있다.

이 간격은 Lima와 krunkit 같은 의존성의 한계를 그대로 물려받은 결과지만,
Colima의 마케팅은 그 사실을 잘 드러내지 않는다.
사용자는 문서 상단의 호환성 목록을 보고 도입했다가
하단의 세부 조건에서 막히는 패턴을 반복한다.

진짜 문제는 이 패턴이 시간이 갈수록 더 심해진다는 것이다.
M 시리즈 칩이 세대마다 가상화 기능을 다르게 노출하기 때문에,
“Apple Silicon”이라는 단일 라벨로 묶기 어려운 분기가 코드에 누적된다.
Colima가 이 분기를 사용자에게 충분히 노출하지 않으면,
“지원한다”는 표현은 점점 약속이 아니라 마케팅이 된다.

### 개인 주도 프로젝트라는 거버넌스 위험

Colima는 CNCF Slack 채널을 가지고 있지만 CNCF 프로젝트가 아니다.
거버넌스는 사실상 단일 메인테이너에 의존하고,
재정 모델은 GitHub Sponsors, Buy Me a Coffee, Patreon이다.
다시 말해 기업 환경에서 Docker Desktop을 대체하기에는
조직 차원의 위험 평가를 통과하기 어려운 구조다.

이 위험은 단순한 “버스 팩터”의 문제만이 아니다.
Docker Desktop이 만약 라이선스 정책을 다시 한 번 강화하거나,
Apple이 가상화 API를 갑작스럽게 바꿔
Lima/krunkit이 영향을 받을 때,
대응 속도와 자원이 단일 메인테이너의 사정에 종속된다.
기업 사용자가 Colima로 옮길수록 이 종속의 비용은 커진다.

OrbStack이 유료 모델로 빠르게 자원을 모으고,
Apple이 자체 `container` 도구를 내놓는 환경에서,
Colima가 “무료 오픈소스 + 개인 주도”라는 조합을 얼마나 더 유지할 수 있느냐는
도구의 기능 로드맵보다 먼저 답해야 할 질문이다.

HN 토론에서도 이 점이 직접적으로 거론된다.
한 댓글은 “단일 메인테이너에 의존하지 않고 SUSE의 지원을 받는다”는 이유로
Rancher Desktop을 고수하겠다고 밝혔다[^traceroute66].
“컨테이너 런타임을 디버깅하는 데 시간을 쓰고 싶지 않다”는 한 줄은
개인 사용자보다 조직 사용자가 Colima에 대해 가지는 가장 큰 망설임을 정확히 요약한다.
AWS가 후원하는 Finch[^JustinGarrison]가 비슷한 스택을 들고 나오는 것도
같은 시장 신호다.
“누가 이 도구의 뒤를 받치고 있는가”가 기능 비교표만큼 중요한 항목이 되었다.

### “Docker 호환”이라는 약속의 점진적 균열

Colima의 약속 중 가장 강한 것은
“`colima start` 후에는 평소처럼 `docker` 명령을 쓸 수 있다”는 것이다.
이 약속은 Docker Engine API가 안정적이라는 가정 위에 서 있다.
하지만 Docker Desktop은 BuildKit, Compose v2, Docker Init, Docker AI 같은 기능을
CLI와 GUI에 점점 더 깊이 통합하고 있고,
이 중 일부는 클라이언트 측 통합에 의존한다.

Colima가 가져오는 것은 데몬과 소켓 수준의 호환성이지,
Docker Desktop이 제공하는 GUI 흐름과 데스크톱 통합이 아니다.
시간이 갈수록 “docker 명령은 똑같이 동작한다”는 표현이 다루는 표면적은 좁아진다.
사용자는 “Docker는 되는데 Docker Desktop만의 기능은 안 된다”는 상태를 반복적으로 마주한다.

이 균열은 Colima가 직접 해결할 수 없다.
Docker가 데스크톱 제품을 강화할수록 호환성의 의미가 변하기 때문이다.
“Docker Desktop 대체”라는 포지셔닝을 유지하려면
Colima는 자기 영역을 넘어 클라이언트 측 도구까지 손대야 하는데,
이는 “minimal” 철학과 정면으로 충돌한다.

## 인사이트

### Docker Desktop의 라이선스 변경은 컨테이너 도구의 토대를 영구히 바꿨다

Colima의 사용자 증가는 단일 정책 변경이 만든 시장 구조 변화의 직접적 결과다.
2021년 이전에는 “맥에서 컨테이너 = Docker Desktop”이 사실상 정의였다.
정책 변경 이후 그 정의가 깨지면서,
Colima, Podman Desktop, OrbStack, 최근의 Apple `container`까지
서로 다른 철학을 가진 도구들이 같은 자리를 두고 경쟁하는 시장이 만들어졌다.

이 변화는 되돌릴 수 없다.
한 번 분열된 시장은
Docker가 라이선스를 다시 무료로 풀어도 단일 표준으로 복귀하지 않는다.
사용자는 이미 대안의 존재를 학습했고,
조직은 한 회사의 정책 변경에 다시 노출되는 것을 피하려 한다.
컨테이너 도구는 운영체제처럼 “한 번 정한 표준”의 시대를 지나
패키지 매니저처럼 “환경마다 다른 선택”의 시대로 넘어가는 중이다.

이 흐름은 Colima에 유리하면서 동시에 위험하다.
유리한 점은 “표준이 없는 시장”이 작은 도구의 진입을 허락한다는 것이고,
위험한 점은 같은 이유로 OrbStack, Podman, Apple `container` 같은 경쟁자가 끊임없이 등장한다는 것이다.
시장 분열에서 살아남는 도구는 “기능이 가장 많은 도구”가 아니라
“가장 좁은 영역을 가장 깊이 정의한 도구”다.

### “VM 위 컨테이너”는 macOS에서 영구적 우회로가 되었다

Colima의 구조 — Lima로 Linux VM을 띄우고 그 안에서 컨테이너를 돌리는 — 는
임시 해결책처럼 보이지만 실은 macOS 컨테이너의 기본 형태가 되었다.
Apple이 자체 `container` 도구를 내놓아도 본질은 같다.
가벼운 VM을 띄워 그 안에서 컨테이너 워크로드를 돌리는 구조다.

이 사실은 Linux 호스트의 컨테이너와 macOS 호스트의 컨테이너가
영원히 다른 성능 곡선을 그릴 것이라는 의미다.
파일시스템 마운트는 두 OS 사이의 번역을 거치고,
네트워크는 VM 경계를 한 번 더 통과하며,
CPU/메모리는 호스트 OS와 게스트 OS가 나눠 갖는다.
“Mac에서도 같은 컨테이너가 돈다”는 약속은 기능 호환의 약속이지 성능 동일성의 약속이 아니다.

이 구조적 차이는 도구 선택의 기준을 바꾼다.
“어떤 도구가 가장 빠른가”보다 “어떤 도구가 VM 경계의 비용을 가장 잘 숨기는가”가 더 중요한 질문이 된다.
OrbStack이 유료 정책을 내세울 수 있었던 것도,
“비슷한 구조에서 더 빠른 경계 처리”라는 단일 축에 자원을 집중했기 때문이다.
Colima의 다음 라운드 경쟁력도 이 축에서 결정된다.
HN 토론에서 OrbStack이 더 나았다는 짧은 보고[^crobibero]가 반복적으로 등장하는 것도
이 경계 처리의 체감 차이가 도구 선택의 결정 변수가 되었음을 보여준다.

같은 토론에서 한 사용자가 “macOS에 네이티브 컨테이너를 가능하게 할 원시 기능이 있느냐”고 물은 것[^fulafel]은
이 구조의 깊이를 드러낸다.
질문 자체가 가설법으로 던져진다는 사실은,
실제로는 그런 원시 기능이 없거나 있어도 충분치 않다는 합의를 반영한다.
Apple이 자체 `container` 도구를 내놓아도 이 한계는 그대로다.
다른 사용자가 “Docker를 쓰려면 그냥 Linux를 써라”고 정리한 한 줄[^28304283409234]은
이 모든 우회로의 본질을 가장 짧게 요약한다.
macOS 컨테이너는 영원히 “Linux를 시뮬레이션하는 비용”을 지불하는 구조이고,
그 비용을 누구에게도 영원히 사라지게 할 수는 없다.

### 로컬 AI 워크로드는 컨테이너 도구의 두 번째 정체성을 강제한다

`colima model run gemma3`은 표면적으로는 편의 기능이지만,
구조적으로는 컨테이너 도구가 “로컬 추론 환경 매니저”라는 두 번째 정체성을 받아들이는 신호다.
GPU 가속, 모델 레지스트리, 양자화 형식 같은 개념은
원래 컨테이너 도구가 다루던 영역이 아니다.
하지만 사용자가 “Mac에서 로컬로 LLM을 돌린다”는 일을
컨테이너 워크로드와 분리해서 다루지 않기 때문에,
도구가 그 경계를 흡수할 수밖에 없다.

이 흡수는 컨테이너 도구의 추상화를 새로 정의하라는 압력으로 돌아온다.
지금까지 컨테이너는 “프로세스를 격리하는 단위”였지만,
모델 러너가 들어오면 “GPU를 공유하는 단위”, “모델 캐시를 공유하는 단위” 같은 새로운 추상이 필요해진다.
Colima의 `--vm-type krunkit` 옵션이 이런 압력의 첫 표면화다.

이 추상의 재정의에서 누가 표준을 잡느냐가 다음 5년의 게임 규칙을 결정한다.
Docker는 Model Runner를 자기 클라이언트에 묶고,
Ollama는 자체 런타임으로 따로 가고,
Colima는 둘 다 옵션으로 흡수하는 중립 위치를 선택했다.
중립이 유지될지, 결국 한쪽에 줄을 서야 할지는
모델 배포 포맷이 OCI 이미지처럼 표준화되느냐에 달려 있다.

### “얇은 래퍼” 전략은 기능이 늘수록 비용이 가속한다

Colima의 핵심 설계는 자기 코드를 최소화하고 외부 프로젝트를 조립하는 것이다.
초기에는 이 전략이 압도적으로 유리하다.
적은 인력으로 빠르게 기능을 추가할 수 있고,
유지보수 부담이 외부 프로젝트로 분산된다.

하지만 조립하는 부품의 수가 늘수록 비용 곡선이 꺾인다.
Lima의 업데이트, Docker의 API 변경, krunkit의 호환성, Incus의 거버넌스 변화,
각각의 외부 변화가 Colima의 회귀를 만들 수 있다.
“통합 테스트의 표면적”은 부품 수의 곱셈으로 증가하고,
단일 메인테이너가 이 표면적을 모두 감당하기는 어렵다.

이 비용 곡선은 OrbStack이 유료 모델로 자원을 모은 이유이기도 하다.
“얇은 래퍼”는 진입 단계의 전략이지 성장 단계의 전략이 아니다.
Colima가 무료 오픈소스 + 개인 주도 모델을 유지하면서 부품을 계속 늘리려면,
어느 시점에 “지원 부품의 수”를 줄이거나 거버넌스를 확장하는 선택을 해야 한다.
이 선택을 미루면 도구는 “지원한다고 적혀 있지만 실제로는 깨지는 조합”이 늘어나는 길로 들어선다.
오픈소스 인프라 도구가 사용자 신뢰를 잃는 가장 흔한 경로다.

---

[^tootie]: <https://news.ycombinator.com/item?id=35987774>
[^segfaltnh]: <https://news.ycombinator.com/item?id=35986191>
[^JonMR]: <https://news.ycombinator.com/item?id=35985873>
[^traceroute66]: <https://news.ycombinator.com/item?id=35985346>
[^JustinGarrison]: <https://news.ycombinator.com/item?id=35989126>
[^crobibero]: <https://news.ycombinator.com/item?id=35983999>
[^fulafel]: <https://news.ycombinator.com/item?id=35990373>
[^28304283409234]: <https://news.ycombinator.com/item?id=35988647>
