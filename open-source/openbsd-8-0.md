# OpenBSD 8.0은 64 vCPU 가상 머신과 arm64 최대 절전을 얻었고, 출시일에 정오표 네 건이 붙었다

원문: [OpenBSD 8.0](https://www.openbsd.org/80.html)

HN 토론: <https://news.ycombinator.com/item?id=50160494> (467점, 154개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/sqdhu7/openbsd_8_0> (96점, 11개 댓글)

GN 토론: <https://news.hada.io/topic?id=35692>

## 소개

OpenBSD 8.0은 2026년 10월 20일에 나온 61번째 릴리스다.
릴리스 페이지는 변경 사항을 플랫폼, 커널, 가상화,
그래픽과 드라이버, 사용자 영역, 설치와 패키지 도구,
보안, 네트워크 스택, 서비스, 외부 구성요소, 포트와 패키지 순으로 나열한다.
페이지는 스스로를 부분 목록이라고 부르며
전체 목록은 7.9에서 8.0 사이의 변경 로그를 보라고 한다.

이 문서는 그 목록을 읽고
업그레이드하는 사람이 알아야 할 것 위주로 간추린 것이다.
항목마다 수백 개가 되는 개별 버그 수정은 옮기지 않았다.
수치와 이름은 릴리스 페이지와 거기서
링크한 업그레이드 안내, 정오표에서 가져왔다.
페이지에 실린 그래픽은 열어 보지 않았다.

## 주요 변화

### 플랫폼과 커널

amd64 커널의 가상 주소 공간이 4G에서 512G로 커졌고,
직접 매핑(direct map)이 무작위 위치에 놓이며,
AES CPU 명령으로 스왑 암호화가 빨라졌다.
같은 스왑 암호화 가속이 arm64에도 들어갔다.
arm64는 최대 절전(hibernate)을 지원하게 되었고 bounce buffer를 구현했다.
riscv64는 CPU 확장을 감지해 `elf_aux_info(3)`로 사용자 영역에 알리고,
`V` 벡터 확장과 RISC-V 고급 인터럽트 아키텍처(imsic,
aplic 드라이버), Sstc 타이머 확장을 지원한다.
sparc64는 LLVM 도구 모음으로 넘어갔다.
loongson은 Clang 22에서 동작하지 않아 지원이 끝났다.

커널에는 `getexecpath(3)`가 새로 들어갔다.
프로그램이 자기 실행 경로의 사본을 얻는 함수이고,
뒤에 나올 데몬들의 `execv(3)` 절대 경로 사용과 이어진다.

### 가상화

vmm과 vmd는 게스트 한 대에 최대 64개의 가상 CPU를 줄 수 있는 다중 프로세서
지원을 얻었다.
게스트 소유권을 파일로 관리하도록 설계를 바꿨고,
x2apic 모드와 MSI, MSI-X virtio 인터럽트, 체크섬 오프로드가 들어갔다.
악의적으로 깨진 `elf(5)` 파일로 vmd가 범위를 넘어 읽던 문제도 막았다.

### 노트북과 그래픽

최대 절전과 일시 중단이 눈에 띄게 늘었다.
무선 드라이버 `qwz(4)`와 UART 드라이버 `qcuart(4)`의 절전 복귀,
Samsung Galaxy Book4 Edge와 HONOR MagicBook Art 14에서
`ufshci(4)`가 일시 중단을 견디도록 한 수정이 그렇다.
덮개를 닫아도 `machdep.lidaction=0`이면 일시 중단된 노트북을 깨우지 않는다.
`drm(4)`은 Linux 6.18.53 기준으로 갱신되고
Intel Arc A-Series(DG2/Alchemist) 지원이 들어갔으며,
늘어난 커널 주소 공간 덕에 4GB가 넘는 VRAM을 매핑할 수 있다.
무선 드라이버 `qwx(4)`와 `qwz(4)`는 802.11n과 40MHz 폭을 지원하게 되었다.

### 서비스 데몬

`httpd(8)`는 사용자 지정 HTTP 헤더를 지원한다.
`relayd(8)`는 필터 규칙에 Lua 패턴을 쓸 수 있고 CA 분리 엔진에 ECDSA를 지원한다.
`acme-client(1)`는 대체 이름에 와일드카드를 허용하고
외부 계정 바인딩(EAB)을 지원한다.
RPKI-To-Router 프로토콜 데몬 `rtrd(8)`와 `rtrctl(8)`이 새로 들어왔다.
`tmux(1)`에는 `new-pane` 명령과 모달 창(`new-pane -O`),
창 제목 변경 키가 생겼다.

### 외부 구성요소

OpenSSH는 10.6이고,
실험적인 복합 양자내성 서명 방식 `mldsa44-ed25519`를 `ssh(1)`에 넣었다.
`ssh(1)`는 ed25519 구현을 supercop에서 libsodium으로 바꾸었다.
LibreSSL은 4.4.0이고
libtls가 TLSv1.3의 기본 선호 그룹으로 `X25519MLKEM768`을 쓴다.
기본 시스템의 컴파일러는 LLVM/Clang 22.1.6(패치 포함)이고,
GCC 4.2.1과 3.3.6, Binutils 2.17, GDB 6.3도 패치된 채 여전히 들어 있다.

## 업그레이드하기

업그레이드 안내문은 한 릴리스에서 바로 다음 릴리스로만 지원한다고 분명히 한다.
`/usr` 파티션이 1.1G 이상이어야 하고,
원격에 있는 중요한 기계는 같은 환경의 로컬 기계에서
먼저 시험해 보라고 권한다.[^upgrade]
가장 쉬운 방법은 `sysupgrade(8)`이고, 끝난 뒤에 `sysmerge`,
낡은 파일 제거, `pkg_add -u` 순서로 진행한다.[^upgrade]

```sh
# 7.9에서 8.0으로 무인 업그레이드 (루트 권한)
sysupgrade
# 재부팅 후 설정 파일 병합
sysmerge
# 패키지 갱신
pkg_add -u
```

업그레이드 안내문이 따로 짚은 호환성 영향은 다섯 가지다.[^upgrade]

| 대상          | 변경                                                                          |
| ------------- | ----------------------------------------------------------------------------- |
| bgpd          | `announce as-4byte` 기본값이 `yes`에서 `enforce`로 바뀌어 4바이트 AS를 강제함 |
| firefox       | AI 기능을 기본으로 끄는 정책 파일이 추가됨. 설정의 AI Controls에서 켤 수 있음 |
| kea           | 2.4.2에서 3.2로 올라 설정을 새로 써야 하고 데이터가 `/var/db/kea`로 이동함    |
| libmaxminddb  | 낡은 GeoLite 데이터베이스 번들 제거. DB-IP 패키지로 대체 가능                 |
| stalwart-mail | 0.16으로 올라 전체 덤프와 복원이 필요함                                       |

릴리스 페이지의 변경 목록에서도 설정에 영향을 주는 것이 몇 가지 보인다.
`httpd.conf(5)`와 `relayd.conf(5)`의 기본 TLS 암호 집합이 `compat`,
`HIGH:!aNULL`에서 `secure`로 바뀌었다.
`pkg_add(1)`의 기본 검색 경로에서 현재 디렉터리가 빠졌다.
`sshd_config(5)`에서 `DisableForwarding=yes`가 `PermitTunnel=yes`보다 우선한다.
libcrypto에서는 `SSL_OP_LEGACY_SERVER_CONNECT`가 기본 옵션에서 빠졌다.
이름만으로 영향을 알 수 없는 변경도 있으므로
업그레이드 전에 변경 로그를 한 번 훑는 편이 안전하다.

## 보안 변경의 성격

릴리스 페이지의 보안 절은 길다.
개별 취약점에 대한 설명은 거의 없고, 대부분이 범위 검사와 정수 오버플로,
해제 후 사용, 커널 스택 내용 노출 같은
짧은 문장이다.
크게 다섯 갈래로 나뉜다.

- 설치 도구: `fw_update(8)`는 내려받는 파일 크기에
한도를 두고 서명 검사를 엄격하게 하며,
  `syspatch(8)`는 악성 스크립트에 대비해 강화되었다.
- 프로세스 분리와 실행 경로: 여러 데몬이 `execv(3)`에 절대 경로를 쓰고,
  `smtpd(8)`는 권한 분리 통신으로 보내기 전에 사용자 정보를 지운다.
- 샌드박스: `unveil(2)`이 `man(1)`과
`makewhatis(8)`의 읽기와 쓰기 접근을 제한하고,
  `pledge(2)`의 소켓 옵션 검사가 엄격해졌다.
- 프로토콜 파서: `httpd(8)`가 RFC 9112에 맞춰 CL.TE 요청 구분을 거부하고,
`httpd(8)`와 `relayd(8)`는 `obs-fold`를 거부한다.
- 번들 소프트웨어: libexpat, libXfont, Perl과 NSD의 취약점 수정을 가져왔다.

흥미로운 한 줄이 있다.
`smtpd(8)`의 코드를 고쳐 LLM 스캐너가 내는
거짓 버그 보고를 피하도록 했다는 항목이다.
코드가 틀려서가 아니라 스캐너가 틀리게 읽어서 고친 것이라고 이 문서는 읽는다.

## 비평

### 릴리스 당일 정오표 네 건은 보안 절 옆에 놓고 읽어야 한다

정오표 페이지에는 출시일 하루에 네 건이 올라 있다.
`ppp(4)`의 off-by-one이 범위를 벗어난 쓰기를 일으킬 수 있고,
`nsd(8)` 4.15.3의 보안 수정을 가져왔으며,
IPsec에서 AES-GMAC를 쓰면
커널 힙 오버플로를 원격으로 일으킬 수 있고(AES-NI가 있는 amd64와
암호 보조 프로세서가 있는 octeon에만 해당하며 AES-GCM은 해당 없음),
`video(4)`의 여러 버그가 해제 후 사용과
커널 메모리 손상을 일으킬 수 있다.[^errata]
Lobste.rs의 fazalmajid는 벌써 정오표가 네 건이라고 지적했고,
elobdog와 voutilad는 코드 동결 이후에 발견된 문제들이라 어쩔 수 없다고
답했다.[^fazalmajid][^elobdog][^voutilad]

릴리스 페이지가 `ipsec(4)`의 AES GMAC 암호를 개선했다고
적은 것과 정오표 세 번째 항목은 같은 영역이다.
이 문서는 그 둘이 같은 원인이라고 말하지 않는다.
다만 새 릴리스의 변경이 많은 영역에서
하루 만에 원격 커널 문제가 나온 것은 사실이고,
변경이 많은 영역일수록 동결 이후에 발견되는 것도 많으리라는 예상과 맞아떨어진다.
이는 이 문서의 해석이다.

### 릴리스 페이지 자체에 아직 비어 있는 곳이 있다

이 문서를 쓴 시점의 페이지는 패키지 개수 표에서
arm과 powerpc의 값이 XXX로 남아 있다.
다른 구조의 수치는 채워져 있는 것으로 보아 아직 채우지 못한 자리표시자로 보인다.
HN의 MycroftJones는 변경 로그를 읽다가 만우절인지 확인해야 했고
이것이 진짜 릴리스인지 의심했다고 썼다.[^MycroftJones]
이 댓글이 무엇을 보고 그렇게 느꼈는지는 적혀 있지 않아서 판단할 근거가 없다.

### 업그레이드가 순조롭다는 칭찬은 OpenBSD만의 장점이 아니다

HN에서는
7.6부터 모든 릴리스를 `sysupgrade`로 따라온 노트북이
8.0에서도 잘 돈다는 사례가 줄을 이었다.[^idatum]
volkadav는 배스천 호스트를 10분 만에 7.9에서 8.0으로 올렸다고 했다.[^volkadav]
반면 stackghost는 이것이 기본 요건이며
Debian이 1999년부터 해 온 일이라고 했고,[^stackghost]
prmoustache도 지난 20여 년 동안 어느 OS든 릴리스 사이 업그레이드가 안전했다고
덧붙였다.[^prmoustache]
이 문서의 읽기로는 OpenBSD가 눈에 띄는 것은 업그레이드가 되느냐가 아니라
그 방법이 설명서 한 장이고 한 릴리스씩만 지원한다고 한정하는 단순함에 있다.

### 출시 페이지의 크레디트 한 줄이 논의의 일부를 가져갔다

페이지 맨 위에는 8.0의 노래와 그림의 제작자가 적혀 있다.
그림은 yvaneht nioj와 clanker의 것이라고 되어 있다.
HN의 jan_m_savage는 슬롭이 바이러스처럼 퍼져 사람이 만든 믿을
만한 자료를 걸러 내기 어려워질 것이라고 썼다.[^jan_m_savage]
Lobste.rs에서는 운영자 pushcx가 AI 사용 여부를 논한 데서
시작해 순수성 시험이 된 스레드를
공개적인 비난으로 번지기 전에 삭제했다고 밝혔다.[^pushcx]
삭제된 댓글의 내용은 볼 수 없어서
무엇이 AI 사용으로 지목되었는지 확인할 수 없다.
이 문서는 그림을 열어 보지 않았다.

## 인사이트

### 여러 데몬에 같은 종류의 수정이 한꺼번에 들어갔다

릴리스 페이지의 보안 항목은 길고 비슷하다.
범위 검사 추가, 크기 검증, 정수 오버플로 방지,
초기화되지 않은 변수 제거, 커널 스택 노출 수정이다.
`bgpd`, `rpki-client`, `smtpd`, `httpd`, `relayd`, `isakmpd`,
`ospfd`처럼 서로 다른 데몬에서 같은 종류가 한 릴리스에 모였다.

페이지는 왜 이렇게 되었는지 말하지 않는다.
이 문서가 확인한 AI 관련 문장은 하나다.
`smtpd(8)`의 코드를 고쳐 LLM 스캐너가 내는
거짓 버그 보고를 피하도록 했다는 항목이다.
이 문장은 자동 도구가 유지보수자의 일에 끼어들고 있다는 사실을 보여 준다.
코드가 틀려서가 아니라 도구가 틀리게 읽어서 코드를 고친 것이기 때문이다.

그렇다고 나머지 수정이 스캐너에서 나왔다고 말할 수는 없다.
어느 수정이 어디서 나왔는지는 이 페이지로 알 수 없고,
그 비율을 이 문서는 추정하지 않는다.
다만 한꺼번에 몰린 같은 종류의 수정과 하루
만에 붙은 정오표 네 건은 함께 보아 둘 만하다.
릴리스 직전에 고칠 것이 많았다면 동결 뒤에 남는 것도 많을 수 있기 때문이다.

### 번호는 신호가 아니고 안내문이 신호다

HN의 gucci-on-fleek은 7.9에서 8.0으로의 변화가 더 큰 갱신인지,
아니면 9 다음이라서 번호가 올라간 것인지 물었다.[^gucci-on-fleek]
릴리스 페이지는 번호의 의미를 설명하지 않는다.
페이지에서 보이는 것은 아키텍처 하나가 빠졌고(loongson),
bgpd의 4바이트 AS 기본값처럼 하나씩 따로 보아야 하는 변경이 있다는 점이다.
호환성에 영향을 주는 것은 번호가 아니라
업그레이드 안내문의 설정 변경 절에 적혀 있다.

이 문서의 해석으로는 번호가 약속이 아니라 이름이므로
업그레이드할 때 번호의 크기를 믿으면 안 된다.
안내문이 한 릴리스에서 바로 다음 릴리스로만 올리게 하는 것도 같은 맥락이다.
경로를 한 단계로 한정하면 호환성 변경을 릴리스마다 안내문 한 장에 담을 수 있다.
번호를 신호로 쓰는 프로젝트에서는
큰 숫자가 큰 변화를 뜻하지만 여기서는 그렇지 않다.

### 툴체인과 아키텍처 지원은 함께 움직인다

기본 시스템에는 GCC 4.2.1과 3.3.6, Binutils 2.17,
GDB 6.3이 패치된 채 아직 들어 있다.
HN의 RetroTechie는 이 이유를 설명한 2021년 글을 찾아 링크했다.[^RetroTechie]
같은 릴리스에서 loongson은 Clang 22에서 동작하지 않아 지원이 끝났고
sparc64는 LLVM으로 넘어갔다.

이 문서는 어느 아키텍처가 어느 컴파일러를 쓰는지는 확인하지 않았다.
페이지가 밝힌 사실만 놓고 보면 새 컴파일러에서
빌드되지 않는 아키텍처는 정리 대상이 되고,
빌드되는 아키텍처는 전환한다.
HN의 SoftTalker는 OpenBSD가 살아남은 하드웨어가 거의 없거나 Clang이
지원하지 않는 아키텍처를 조금씩 없애 가고 있다고 했다.[^SoftTalker]
이 문서의 해석으로는 OpenBSD가 지원하는 아키텍처의
범위가 컴파일러가 지원하는 범위에 묶여 있다.
그래도 설치 안내를 싣는 아키텍처가 지금도 13개라서 줄어드는 속도는 느리다.

---

[^upgrade]: OpenBSD, [OpenBSD Upgrade Guide: 7.9 to 8.0](https://www.openbsd.org/faq/upgrade80.html), 2026-10-20

[^errata]: OpenBSD, [OpenBSD 8.0 Errata](https://www.openbsd.org/errata80.html), 2026-10-20

[^fazalmajid]: <https://lobste.rs/s/sqdhu7/openbsd_8_0#c_78fbuh>

[^elobdog]: <https://lobste.rs/s/sqdhu7/openbsd_8_0#c_jgigj4>

[^voutilad]: <https://lobste.rs/s/sqdhu7/openbsd_8_0#c_gxm2cs>

[^MycroftJones]: <https://news.ycombinator.com/item?id=50161489>

[^idatum]: <https://news.ycombinator.com/item?id=50161517>

[^volkadav]: <https://news.ycombinator.com/item?id=50166559>

[^stackghost]: <https://news.ycombinator.com/item?id=50162803>

[^prmoustache]: <https://news.ycombinator.com/item?id=50162059>

[^gucci-on-fleek]: <https://news.ycombinator.com/item?id=50161399>

[^RetroTechie]: <https://news.ycombinator.com/item?id=50170826>

[^SoftTalker]: <https://news.ycombinator.com/item?id=50169937>

[^jan_m_savage]: <https://news.ycombinator.com/item?id=50161516>

[^pushcx]: <https://lobste.rs/s/sqdhu7/openbsd_8_0#c_aez5r1>
