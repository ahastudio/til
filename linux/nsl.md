# nsl: 리눅스 위에서 WSL처럼 쓰는 systemd-nspawn 개발 머신

<https://frostyard.github.io/nsl/>

<https://github.com/frostyard/nsl>

HN 토론: <https://news.ycombinator.com/item?id=49894351> (161점, 101개 댓글)

GN 토론: <https://news.hada.io/topic?id=34557>

## 소개

nsl은 NSpawn Subsystem for Linux의 줄임말이다.
README는 이 도구를 원자적(atomic) 리눅스를 위한 WSL 방식의 리눅스 머신이라고 소개하고, 호스트는 원자적으로 두고 어떤 배포판에서든 일하라는 문장을 내세운다.
원자적 리눅스 호스트는 기본 시스템을 읽기 전용으로 두고 통째로 교체하므로, 프로젝트 의존성을 `apt install`하거나 다른 배포판용 툴체인을 시험할 자리가 따로 필요하다.
nsl은 그 자리로 WSL처럼 패키지와 서비스와 파일을 세션 사이에 유지하는 영구 머신을 준다.

HN에 직접 소개한 작성자 bketelsen이 만들었고, 저장소는 2026년 9월 26일 생성된 Go 프로젝트이며 MIT 라이선스다.
아직 정식 릴리스가 없는 사전 릴리스 단계로, 문서는 v0.4.0이 현재 설계의 첫 릴리스이고 v0.3.0 이전은 폐기된 프로토타입이라고 밝힌다.
저장소의 릴리스는 9월 28일 v0.5.0부터 9월 30일 v0.7.0까지 사흘 사이에 다섯 번 나왔을 만큼 빠르게 움직이고 있다.
검증된 호스트는 x86-64의 Snow Linux 13, systemd 261.2, QEMU 10.0.13, virtiofsd 1.13.2, GNOME Wayland다.

```bash
nsl create debian --distro debian:13   # 서명된 이미지를 검증해 캐시한다, 첫 머신이 기본 머신이 된다
nsl                                    # 지금 디렉터리에서 그 머신의 로그인 셸을 연다
nsl run make test                      # 명령 하나를 실행하고 종료 코드를 호스트로 돌려준다
```

머신이 주는 것은 다음과 같다.

| 기능        | 내용                                                                                                |
| ----------- | --------------------------------------------------------------------------------------------------- |
| 셸과 명령   | 프로젝트 디렉터리에서 기본 머신의 셸을 열거나 `nsl run`으로 명령 하나를 실행한다                    |
| 파일과 계정 | 호스트의 `$HOME`, `/run/media/USER`, `/mnt`가 `/mnt/host`에 보이고, 같은 사용자명과 UID, GID를 쓴다 |
| 포트와 창   | 머신의 서버를 호스트 `127.0.0.1`의 같은 포트로 열고, Wayland 앱은 Waypipe로 데스크톱에 창을 띄운다  |
| 배포판      | Debian 13, Ubuntu 26.04 LTS, Fedora 44, CentOS Stream 10, Arch, openSUSE Tumbleweed와 Leap 16.0     |
| 편집기      | `nsl ssh-config`가 VS Code 같은 SSH 클라이언트에 머신별 호스트 별칭을 준다                          |
| 격리        | `--isolated` 머신은 자기 VM에서 호스트 파일, 데스크톱, 호스트 동작 없이 돈다                        |
| 백업과 이동 | 멈춘 머신을 아카이브로 내보내고 다른 호스트에서 가져올 수 있다                                      |

이미지는 매주 다시 빌드되고, nsl은 사용 전에 서명된 Frostyard 배포 워크플로에서 왔는지 검증하며 이 검증을 끄는 스위치는 없다.

## 동작 방식

### 공유 VM 하나 안에 nspawn 컨테이너 여러 개

일반 머신은 공유 VM 하나 안에서 systemd-nspawn 컨테이너로 돈다.
VM은 서명된 nsl VM 이미지를 systemd-vmspawn과 QEMU/KVM으로 부팅하며, 호스트에서는 `nsl-UID-vm-ID.service`라는 사용자 유닛으로 실행되므로 별도 호스트 데몬이 없다.
VM은 디스크 두 개를 쓴다.
루트는 캐시된 VM 이미지 위의 qcow2 오버레이로 사용자 상태를 담지 않아 `nsl update`나 `nsl recover`가 다음 시작 때 통째로 바꿀 수 있고, 데이터 디스크는 btrfs가 든 qcow2 이미지로 모든 머신과 VM 자신의 상태를 담는다.

VM은 처음 필요할 때 켜지고 쉬면 꺼진다.
기본으로 호스트 메모리의 절반과 모든 CPU를 쓸 수 있고, 머신들이 VM 자원을 나눠 쓰므로 머신을 더해도 VM 하나만큼의 메모리를 따로 잡지 않는다.
실행에 root가 필요 없고, 기존의 `kvm` 그룹 멤버십으로 `/dev/kvm`과 `/dev/vhost-vsock`을 비특권 사용자 네임스페이스 안에서 열어 vmspawn에 넘긴다.

각 머신은 데이터 디스크의 btrfs 서브볼륨이며, 서명된 머신 이미지에서 만들어지고 systemd-nspawn으로 실행된다.
머신은 VM의 커널, 네트워크 네임스페이스, 리졸버를 쓰고, 공유 VM에서는 호스트 파일이 있는 `/mnt/host`를 바인드한다.
이미지가 캐시된 뒤에는 네트워크 없이 머신을 만들 수 있다.

### CLI와 에이전트

CLI는 vsock 위의 SSH로 VM에 닿고, VM의 sshd는 nsl의 키만 받아 nsl 에이전트만 실행한다.
CLI는 무엇을 하기 전에 VM의 ID, 사용자의 UID와 GID, 역할, 이미지의 프로토콜과 아키텍처를 확인한다.
에이전트는 각 명령을 머신 안의 일시적 systemd 유닛과 PAM 로그인 세션으로 실행하고, 인자를 그대로 넘기며, 종료 코드를 돌려준다.
신호 N으로 죽은 명령은 128+N을 돌려준다.

호스트 통합은 다음과 같이 이뤄진다.

| 기능        | 방식                                                                    |
| ----------- | ----------------------------------------------------------------------- |
| `/mnt/host` | 사용자 권한으로 도는 virtiofs 공유                                      |
| 포트        | VM마다 하나인 포워더 유닛이 1초마다 에이전트를 확인한다                 |
| 창          | 머신마다 하나인 데스크톱 유닛이 호스트와 머신 사이에서 Waypipe를 돌린다 |
| 링크와 파일 | 머신마다 하나인 브로커에 `nsl-open`이 Varlink로 닿는다                  |
| 편집기      | `nsl _ssh NAME`이 에이전트를 통해 머신 안에서 `sshd -i`를 실행한다      |

### 유휴 정지

유휴 판단은 VM이 하므로 호스트에는 백그라운드 프로세스가 없다.
nsl 세션도 창도 최근 요청도 없는 머신은 `idle_timeout` 뒤에 멈추고, VM은 마지막 머신이 멈추고 마지막 요청이 끝난 지 60초 뒤에 꺼진다.
VM이 꺼지는 중에 들어온 명령은 VM이 멈추기를 기다렸다가 다시 켠다.

## 사용하기

### 설치와 호스트 확인

nsl은 사용자로 도는 단일 바이너리이며, KVM이 있는 x86-64 리눅스 호스트가 필요하다.
필요한 것은 systemd-vmspawn과 사용자 systemd 관리자, KVM이 되는 QEMU, Secure Boot 없는 UEFI 펌웨어와 QEMU 펌웨어 설명자, `/usr/libexec/virtiofsd`, OpenSSH와 `systemd-ssh-proxy`, `kvm` 그룹 멤버십, 비특권 사용자 네임스페이스다.
Waypipe는 선택이다.

```bash
# 최신 릴리스 받기(버전은 릴리스 페이지에서 확인한다)
version=0.5.1
base=https://github.com/frostyard/nsl/releases/download/v$version
curl -LO "$base/nsl_${version}_linux_amd64.tar.gz" -LO "$base/checksums.txt"

# 체크섬과 GitHub 빌드 출처를 확인한다
sha256sum --ignore-missing -c checksums.txt
gh attestation verify "nsl_${version}_linux_amd64.tar.gz" --repo frostyard/nsl

# PATH에 설치하고 호스트를 점검한다
tar -xzf "nsl_${version}_linux_amd64.tar.gz" nsl
install -m 0755 nsl ~/.local/bin/nsl
nsl doctor
```

설치 문서의 예시 버전은 0.5.1이지만, 2026년 9월 30일 기준 최신 릴리스는 v0.7.0이다.
Homebrew 캐스크(`brew install --cask frostyard/tap/nsl`)는 다음 정식 릴리스부터 쓸 수 있다고 적혀 있다.
`nsl doctor`는 도구와 펌웨어마다 OK 또는 MISSING을 출력하고, `kvm` 멤버십이 없으면 관리자가 실행할 `usermod` 명령을 보여 주며, 멤버십을 더한 뒤 다시 로그인하지 않아도 된다.

### 믿지 못하는 소프트웨어는 격리 머신에

```bash
nsl create sandbox --distro fedora:44 --isolated
nsl -m sandbox
nsl run -m sandbox --cd /home/you uname -a   # 격리 머신은 호스트 경로가 없어 --cd가 필요하다
```

격리 머신은 자기 VM에서 돌며 호스트 파일, Wayland 창, `nsl-open`이 없고 포트만 호스트 루프백에 닿는다.
기본 자원은 2GiB와 CPU 2개이고, 머신을 지우면 VM과 디스크도 지워진다.
등급은 만들거나 가져올 때 정하며, 나중에 바꾸려면 내보낸 뒤 다른 이름으로 가져와야 한다.

## 신뢰 모델

### 일반 머신은 당신으로서 신뢰된다

문서는 일반 머신이 사용자의 권한으로 홈을 읽고 쓸 수 있다고 분명히 한다.
여기에는 셸 시작 파일, SSH 키, 토큰, nsl 자신의 상태가 포함된다.
VM은 머신의 커널, 패키지, 서비스, 루트를 호스트 시스템과 떼어 놓지만, 파일 공유는 WSL처럼 동작해 패키지를 호스트 밖에 둔다고 공유한 파일이 보호되지는 않는다.

일반 머신이 할 수 없는 것도 적혀 있다.
호스트에서 root가 될 수 없고, 호스트의 `/usr`, `/etc`, `/tmp`, 장치를 볼 수 없으며, D-Bus, SSH 에이전트, GPU, 디스플레이 같은 호스트 소켓에 닿지 못하고, 호스트에서 임의 명령을 실행할 수 없다.
유일한 호스트 동작은 링크나 공유 파일을 기본 처리기로 여는 것이다.
공유 VM 안의 머신들은 서로 닿을 수 있어, 한 머신의 root는 사실상 VM의 root다.

### 읽기 전용 등급이 없는 이유

문서는 읽기 전용 홈도 키와 자격 증명을 드러내고, 쓰기 가능한 홈은 셸 시작 파일을 바꿔 나중에 사용자로 코드를 실행할 수 있게 한다고 설명한다.
기능을 하나씩 끄는 것으로는 어느 문제도 풀리지 않으므로, 선택지는 믿는 머신에 파일을 공유하거나 공유 없는 격리 머신을 쓰는 두 가지뿐이다.
이 설명은 보안 설계에서 드문 정직함이다.
반쯤 안전한 중간 단계를 만들어 사용자가 안전하다고 착각하게 하는 대신, 경계를 두 개로만 두고 각각이 무엇을 막지 않는지 적는다.

## 트레이드오프

### 왜 리눅스 위에서 굳이 VM을 쓰는가

HN에서 0x457은 WSL2가 VM을 쓰는 것은 리눅스 커널이 필요하기 때문인데, 이미 리눅스 위라면 왜 systemd-nspawn만 쓰지 않느냐고 물었다[^0x457].
작성자 bketelsen은 그것이 취향이라면 nspawn.org가 딱 맞다고 답했고[^bketelsen-nspawn], pkulak은 훨씬 나은 격리와 다른 커널을 쓸 수 있다는 점이 이유일 것이라고 추측하며, 이제는 중간 수준의 LLM도 LXC나 Docker나 nspawn을 탈출할 수 있을 것이라고 덧붙였다[^pkulak].

VM 한 겹의 대가는 분명하다.
호스트 파일 편집이 머신 안에서 inotify 이벤트를 만들지 않으므로 파일 감시가 필요한 프로젝트는 게스트 홈에 두어야 하고, 성능 차이도 있다.
ocean2는 컨테이너 안의 컴파일과 호스트의 컴파일 성능 차이를 쟀느냐고 물었지만 답은 없었다[^ocean2].
얻는 것은 호스트 커널과 머신 사이의 경계, 그리고 머신 안에서 무엇을 해도 호스트 패키지가 바뀌지 않는다는 보장이다.

### distrobox와 toolbx와의 차이는 홈 공유 방식이다

HN에서 가장 많이 나온 질문은 distrobox나 toolbx와 무엇이 다르냐는 것이었다.
bketelsen은 distrobox가 기본으로 `$HOME`을 컨테이너의 `$HOME`에 마운트하지만, WSL과 nsl은 그렇지 않으며 그것이 자기 선호라고 답했다[^bketelsen-distrobox].
그래서 기본 PATH를 바꾸거나 dotfiles를 고치는 도구를 설치해도 호스트에 영향이 없다는 것이다.
그는 toolbx, distrobox, Flatpak, Snap이 대부분 `$HOME`의 오버레이로 가장 잘 동작하도록 설계되었고, nsl은 호스트와 제한적으로 통합되는 반려 VM을 주므로 원격 컴퓨터나 VM을 쓰는 것과 비교하는 편이 맞다고 했다[^bketelsen-pet].

다만 이 차이는 생각보다 미묘하다.
머신의 홈은 호스트 홈과 다르지만, 호스트 홈은 `/mnt/host` 아래에서 읽고 쓸 수 있다.
dotfiles가 섞이지 않는다는 것은 편의의 차이이지, 신뢰 모델이 말하듯 보안의 차이는 아니다.

## 함정

### 유휴 정지는 서비스를 보지 않는다

머신은 nsl 명령, 편집기 세션, 창이 없으면 `idle_timeout` 뒤에 멈추는데, 그 안의 서비스가 바쁘게 돌고 있어도 멈춘다.
개발 서버나 데이터베이스를 띄워 두고 브라우저로만 접근하는 사용 방식에서는 갑자기 서비스가 사라질 수 있다.
그런 머신에는 `idle_timeout = 0`을 설정해야 한다.

### 포트와 창에는 조건이 붙는다

포워딩되는 포트는 호스트의 `127.0.0.1`에만 바인드되고, 한 포트는 한 번에 한 머신만 쓴다.
서버는 1024번 이상의 포트에서 들어야 하고, 5353과 5355는 쓸 수 없다.
창은 Wayland 전용이라 X11 전용 앱은 창을 열지 못한다.

### 아카이브와 디스크

내보낸 아카이브는 암호화되지 않으며 자격 증명을 담을 수 있고, 체크섬은 손상을 잡을 뿐 변조를 잡지 못한다.
데이터 디스크는 늘어나기만 하고 줄일 수 없다.
가져오기에는 같은 UID와 GID가 필요하다.

## 비평

### WSL의 사용감을 원하면서 WSL과 다른 신뢰를 기대하게 만든다

nsl의 장점은 HN에서 여러 사람이 말한 WSL의 사용감이다.
rao-v는 데스크톱 안에서 다른 머신을 깔끔하게 쓰는 것이 얼마나 좋은지 의외로 잘 알려져 있지 않다고 했고[^rao-v], tonymet은 에이전트와 함께 쓸 때 일회용 VM을 깔끔한 터미널 통합으로 쉽게 쓸 수 있어 이제 Darwin보다 WSL을 선호한다고 썼다[^tonymet].
ilvez는 이 도구라면 Claude가 시스템 쪽 의존성을 마음대로 설치하게 둘 수 있다며 바로 써 보겠다고 했다[^ilvez].

그런데 마지막 사용 방식이 신뢰 모델과 정면으로 부딪친다.
일반 머신은 홈을 읽고 쓸 수 있으므로, 에이전트가 그 안에서 마음대로 움직이면 SSH 키와 토큰과 셸 시작 파일에도 닿는다.
naman_307은 VM 층이 주로 호스트 위생을 위한 것인지, 의존성이나 에이전트가 쓴 코드 같은 믿지 못할 것을 돌릴 때의 실제 보안 경계인지 물었다[^naman_307].
문서의 답은 분명하지만, 홈페이지와 HN의 분위기는 VM이라는 단어 때문에 사용자가 그 경계를 실제보다 두껍게 여기게 만든다.
에이전트 실험에는 `--isolated`가 기본이어야 한다는 점을 홈페이지 첫 화면에서 더 크게 말할 필요가 있다.

### 검증된 환경이 사실상 한 배포판이다

검증된 호스트는 Snow Linux 13 하나이고, 그 배포판도 같은 Frostyard가 만든다.
HN의 lproven은 Snow Linux를 처음 들어 본다고 했고, bketelsen은 Frostyard의 원자적 이미지가 이제 모두 하나의 mkosi 저장소에서 빌드된다고 답했다[^bketelsen-snow].
systemd 261.2와 특정 QEMU, virtiofsd 버전에 기대는 도구라면, 일반 배포판의 오래된 패키지에서는 `nsl doctor`가 MISSING을 많이 낼 가능성이 높다.
원자적 호스트를 위한 도구라는 소개는 맞지만, 그 원자적 호스트가 지금은 거의 한 곳이라는 점은 사용 전에 알아야 한다.

## 체크리스트

- 호스트가 x86-64이고 `kvm` 그룹 멤버십과 `/dev/vhost-vsock` 접근이 있는가?
- `nsl doctor`가 모든 VM 필수 항목에서 OK를 출력하는가?
- 믿지 못하는 코드나 에이전트를 돌리는 머신을 `--isolated`로 만들었는가?
- 서비스를 상시 띄우는 머신에 `idle_timeout = 0`을 설정했는가?
- 파일 감시가 필요한 프로젝트를 `/mnt/host`가 아니라 게스트 홈에 두었는가?
- 내보낸 아카이브를 자격 증명이 든 파일처럼 다루고 있는가?

## 기억할 원칙

### 경계를 두 개로만 두고 각각이 막지 않는 것을 적는다

nsl의 신뢰 모델이 가장 배울 만한 부분은 읽기 전용 등급을 만들지 않은 이유다.
기능을 하나씩 끄는 중간 단계는 사용자에게 안전하다는 느낌을 주지만, 홈을 읽을 수 있으면 키가 새고 홈을 쓸 수 있으면 나중에 코드가 실행된다.
그래서 nsl은 믿는 머신과 격리 머신 두 가지만 두고, 각 등급이 무엇을 할 수 있고 무엇을 할 수 없는지 목록으로 적는다.

이 원칙은 에이전트 샌드박스 설계에도 그대로 적용된다.
허용 목록을 잘게 쪼갤수록 사용자는 어디까지 안전한지 판단하기 어려워진다.
경계의 수를 줄이고, 각 경계가 막지 않는 것을 먼저 적는 편이 사용자가 올바른 등급을 고르게 만든다.

---

[^0x457]: <https://news.ycombinator.com/item?id=49896511>

[^bketelsen-nspawn]: <https://news.ycombinator.com/item?id=49896607>

[^pkulak]: <https://news.ycombinator.com/item?id=49896861>

[^ocean2]: <https://news.ycombinator.com/item?id=49904738>

[^bketelsen-distrobox]: <https://news.ycombinator.com/item?id=49896422>

[^bketelsen-pet]: <https://news.ycombinator.com/item?id=49904018>

[^rao-v]: <https://news.ycombinator.com/item?id=49896132>

[^tonymet]: <https://news.ycombinator.com/item?id=49904278>

[^ilvez]: <https://news.ycombinator.com/item?id=49904688>

[^naman_307]: <https://news.ycombinator.com/item?id=49900759>

[^bketelsen-snow]: <https://news.ycombinator.com/item?id=49908441>
