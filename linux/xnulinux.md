# xnulinux

<https://github.com/AFK-surf/xnulinux>

HN 토론: <https://news.ycombinator.com/item?id=50607261> (253점, 106개 댓글)

GN 토론: <https://news.hada.io/topic?id=37700>

## 소개

xnulinux는 macOS의 커널을 Linux 안에 올려 macOS 사용자 공간을 Linux 위에서 돌리는 프로젝트이다.
macOS의 오픈 소스 커널 XNU를 Apple이 공개한 소스에서 빌드해
수정하지 않은 arm64 Linux 커널 안에 적재 가능한 커널 모듈(`xnu.ko`)로 실행한다.
함께 올라온 XNU는 CPU와 MMU를 직접 다루고, macOS 프로세스가 Linux 프로세스와
같은 CPU에서 하이퍼바이저 없이 나란히 돈다.
Linux는 작은 인터페이스 모듈(`fki.ko`)로 메모리, 타이머, 파일, 네트워크, GPU를 XNU에 빌려 준다.
README는 기본 Ubuntu 커널에서 `insmod xnu.ko`를 하면
Apple 설치 프로그램이 만든 macOS 27 시스템 디스크가 로그인 창, WindowServer, Dock, Finder,
Safari와 Chrome이 있는 바탕 화면까지 부팅한다고 한다.

API의 라이선스 항목은 NOASSERTION이고, README는 라이선스가 경로별로 갈린다고 설명한다.
저장소의 homepage 항목은 비어 있고 별도의 프로젝트 사이트는 확인하지 못했다.
이 문서는 README를 근거로 쓴다.

## 아키텍처

README의 그림은 두 층이다.
위쪽에서 macOS 프로세스(launchd, WindowServer, Safari 등)와 Linux 프로세스(systemd, sshd 등)가
나란히 돌고, 아래에서 XNU와 `xnu.ko`(APSL 측), FKI라는 외래 커널 인터페이스,
`fki.ko`(GPL 측), 배포판 기본 Linux 커널이 겹친다.

- CPU: 호스팅된 CPU 각각이 Linux CPU에 고정된 Linux 커널 스레드이다.
  XNU는 호출이 호스트로 나갈 때(유휴, 입출력, 타이머)까지 그 위에서 돌고,
  Linux가 자기 예외 벡터를 유지하며 `fki.ko`가 XNU 코드의 오류와 예외를
  XNU의 처리기로 전달한다.
- 메모리: XNU는 Linux에서 물리적으로 연속된 한 덩어리(CMA)를 받아 자기 pmap으로 관리한다.
- 장치: 디스크(Linux 쪽 파일), 화면(Linux가 읽는 프레임버퍼), 키보드와 포인터,
  이더넷, 키스토어, GPU 다리를 커널 확장(kext)으로 제공한다.
- GPU: 호스팅된 macOS의 Metal은 Vulkan 위에서 돌고 Linux 호스트의 GPU에 DRM 다리를 거쳐
  Mesa의 Venus 드라이버로 닿는다. GPU가 없으면 CPU의 Mesa lavapipe로 대체한다.

## 사용법

필요한 것은 PAC가 있는 arm64 Linux 호스트(VM 안의 Apple Silicon M1 이상, GPU는 krunkit 또는 tart),
4K 페이지, 16GB RAM(그중 8GB는 호스팅 커널 전용)이다.
시스템 디스크와 GPU 부분을 만들 Xcode가 있는 Mac이 필요하고,
사용자가 가진 macOS 27 설치(Apple Virtualization VM 디스크)를 쓴다.
README는 이 저장소에 Apple 바이너리가 없으며 Apple이 배포하는 kext, 시스템 디스크, 신뢰 캐시는
사용자의 설치에서 가져온다고 밝힌다.

빌드와 실행은 스크립트 순서로 안내된다.
XNU 빌드(`scripts/vm-xnu-build.sh`), 패치 적용과 커널 컬렉션 링크(`scripts/vm-xnu-rebuild.sh`),
Mac에서 시스템 디스크 만들기(`scripts/mk-macvm-disk.sh`),
모듈 빌드와 부팅(`scripts/xnulinux-boot.sh`), systemd 서비스 설치(`scripts/install-service.sh`),
선택적 GPU 빌드이다.

## 라이선스 및 상태

README가 밝힌 상태는 다음과 같다.

- Apple Silicon Mac의 arm64 Linux VM(krunkit)에서 호스팅 CPU 1~6개로 동작한다.
- macOS 27.2.1이 자동 로그인으로 31~48초에 바탕 화면에 도달한다.
  같은 Mac의 Apple Virtualization macOS VM은 49초이다.
- 30분 스트레스 시험(Safari, Notes, 계산기 등 40회)을 패닉과 충돌 보고서 없이 마쳤다.
- GPU 다리가 호스트 GPU를 호스팅 앱에 주고 기본으로 켜진다.
- 임시방편으로 남은 것: OS cryptex를 시스템 볼륨에 합쳤고, AMFI를 패치하고 SIP를 완화했으며,
  메모리 접근이 네이티브 VM보다 느리다(4K 페이지와 16K 페이지의 차이).

Linux 쪽과 XNU 쪽은 라이선스로 분리되어 FKI에서만 만나고,
모든 소스 파일에 SPDX 식별자가 있다고 한다.

## 분석

### 접근의 새로움

이 프로젝트는 가상화(하이퍼바이저)가 아니라 커널 공존이다.
두 커널이 같은 CPU를 나누어 쓰고, Linux가 장치를 빌려 준다.
README의 성능 수치는 부팅 시간뿐이며 응용 프로그램 성능은 비교하지 않는다.
가능한 이유는 HN의 relistan이 짚은 것처럼 XNU 커널이 오픈 소스이기 때문이다.[^relistan]
Aurornis는 이 프로젝트가 빌려 온 오픈 소스의 비중이 크다며 README의 해당 문장을 인용했다.[^Aurornis]

### 제약

valleyer는 이 프로젝트가 실제 macOS 커널을 거의 그대로 메모리에 올려 공동 커널로 쓰므로
원래 커널이 돌지 않는 하드웨어에서는 작동하지 않을 것이라고 했다.[^valleyer]
matthewfcarlson은 PAC 시스템이 필요해서 현재 Apple Silicon뿐이고
x86_64로 넓히면 훨씬 많은 하드웨어가 열린다고 했다.[^matthewfcarlson]
README의 요구 사항과 일치한다.

## 비평

### 목적

probablyStimmed는 왜 하는지 물었고,[^probablyStimmed]
runtime_terror는 macOS의 미감을 좋아하는 사람이 있기 때문이라고 답했으며,[^runtime_terror]
asveikau는 Linux 호스트에서 Mac이나 iOS 소프트웨어를 만들고 시험하는 교차 개발이 좋은 이유라고 했다.[^asveikau]
README는 목적을 따로 설명하지 않는다.
hn_submit는 Xcode로 iOS 앱을 만들 수 있느냐고 물었고 bigfatkitten은 어차피 Apple 하드웨어가 필요하다고 답했다.[^bigfatkitten]

### 법적 위험

natas는 Apple이 좋아하지 않을 것이라고 했고,[^natas]
sneak은 Apple이 자기 하드웨어에서 사람들이 하는 일에는 대체로 무관심했으며
처음 보기에는 사용권 계약(EULA)을 어기지 않을 것 같고 문제가 되면 패치된 AMFI 파일의 배포 정도라고 했다.[^sneak]
flomo는 공개한 소스에 기반하고 Apple이 Hackintosh 애호가는 건드리지 않고 재판매자만 건드렸다고 했다.[^flomo]
이는 모두 댓글의 추측이다. README는 Apple 바이너리를 포함하지 않는다는 점만 밝히고

### 보호 기술의 미래

pcwalton은 다음 단계가 하드웨어에만 키가 있는 암호화된 OS일 것이라고 걱정했고,
CodeArtisan은 Nintendo가 그렇게 했지만 키가 복구되었다고 답했으며,[^pcwalton][^CodeArtisan]
saagarjha는 콘솔에서는 이미 쓰이지만 디버깅이 불가능해져 다른 시스템에서는 어렵다고 했다.[^saagarjha]
이 논의는 이 프로젝트의 범위를 넘어선 전망이다.

### 만든 방식에 대한 반응

zakisaad는 4~5년 전에 이것을 보았다면 말문이 막혔을 것이며
이런 프로젝트가 일반화된 것이 놀랍다고 했다.[^zakisaad]

## 인사이트

### 가져갈 것

OS를 가상 머신이 아니라 커널 모듈로 공존시킬 수 있다는 사실 자체가 가장 큰 정보이다.
오픈 소스 커널과 안정된 인터페이스 경계(FKI)가 이를 가능하게 한다.
실제로 쓰기에는 README가 말하는 임시방편(AMFI 패치, SIP 완화)과
macOS 27을 직접 설치해야 하는 조건이 남아 있다.

### 확인할 관찰

1. 임시방편이 정식 해법으로 바뀌는지.
2. 응용 프로그램 수준에서 네이티브 VM과의 성능 차이가 얼마인지.
3. Apple이 이 프로젝트에 어떻게 대응하는지.
4. x86_64나 다른 하드웨어로 확장되는지.

---

[^relistan]: <https://news.ycombinator.com/item?id=50608664>

[^Aurornis]: <https://news.ycombinator.com/item?id=50608083>

[^valleyer]: <https://news.ycombinator.com/item?id=50608005>

[^matthewfcarlson]: <https://news.ycombinator.com/item?id=50607771>

[^probablyStimmed]: <https://news.ycombinator.com/item?id=50607575>

[^runtime_terror]: <https://news.ycombinator.com/item?id=50607589>

[^asveikau]: <https://news.ycombinator.com/item?id=50607612>

[^bigfatkitten]: <https://news.ycombinator.com/item?id=50607881>

[^natas]: <https://news.ycombinator.com/item?id=50607555>

[^sneak]: <https://news.ycombinator.com/item?id=50607690>

[^flomo]: <https://news.ycombinator.com/item?id=50607644>

[^pcwalton]: <https://news.ycombinator.com/item?id=50607734>

[^CodeArtisan]: <https://news.ycombinator.com/item?id=50608123>

[^saagarjha]: <https://news.ycombinator.com/item?id=50608046>

[^zakisaad]: <https://news.ycombinator.com/item?id=50607693>
