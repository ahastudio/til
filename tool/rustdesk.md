# RustDesk: 서버까지 직접 운영하는 오픈소스 원격 데스크톱

<https://rustdesk.com/>

<https://github.com/rustdesk/rustdesk>

HN 토론: <https://news.ycombinator.com/item?id=31456007> (421점, 102개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=44283911> (42점, 11개 댓글)

GN 토론: <https://news.hada.io/topic?id=6621>

## 소개

RustDesk는 원격 접속과 원격 지원을 위한 오픈소스 소프트웨어다.
홈페이지는 TeamViewer, AnyDesk, Splashtop에서 넘어와 자체 호스팅 서버로 쓰라고
권하며, 스스로를 빠른 오픈소스 원격 접속·지원 소프트웨어라고 소개한다.
GitHub 저장소의 설명은 자체 호스팅을 위해 설계된 TeamViewer 대안이다.
홈페이지 상단에는 rustdesk.com이 유일한 공식 도메인이니 다른 도메인에서 내려받지
말라는 경고가 붙어 있다.

클라이언트는 Rust로 작성되었고 라이선스는 AGPL-3.0이다.
저장소는 2020년 9월 28일에 만들어졌고,
2026년 10월 5일 기준 스타 125,149개, 포크 19,432개다.
최신 릴리스는 9월 30일의 1.5.0이다.
서버 프로그램은 별도 저장소 `rustdesk-server`에 있고 역시 Rust와
AGPL-3.0이며 스타는 10,504개다.
운영사는 싱가포르의 Purslane Tech Pte. Ltd.로 표기되어 있다.

홈페이지가 내세우는 규모는 클라이언트 다운로드 3천만 회 이상,
Docker 다운로드 1천만 회 이상, 활성 기기 1천만 대 이상,
커뮤니티 회원 5만 명 이상, 지원 언어 50개 이상이다.
홈페이지의 스타 수는 113K+로 적혀 있어 GitHub API의 현재 값보다 낮다.
자체 호스팅 사용자 1,000명 이상을 대상으로 한 설문에서는 IT 지원 37%,
원격 근무 29%, IT 관리 25%, 산업용과 기타 9%로 쓰임새가 나뉜다.

클라이언트는 Windows, macOS, Linux, Android를 지원한다.
Linux는 F-Droid와 Flathub로도 배포되고, 데스크톱 UI는 Flutter로 만든다.
README에 따르면 예전 Sciter UI는 지원 중단(deprecated) 상태다.

## 동작 방식

### ID 서버와 중계 서버

자체 호스팅 문서에 따르면 서버는 두 실행 파일로 나뉜다.

| 프로그램 | 역할                      | 포트                                                             |
| -------- | ------------------------- | ---------------------------------------------------------------- |
| `hbbs`   | ID(랑데부, 시그널링) 서버 | TCP 21115, 21116, 21118(WebSocket), 21114(Pro의 HTTP), UDP 21116 |
| `hbbr`   | 중계(relay) 서버          | TCP 21117, 21119(WebSocket)                                      |

RustDesk가 켜진 기기는 ID 서버에 계속 신호를 보내 현재 IP와 포트를 알린다.
기기 A가 기기 B에 접속하려 하면 A가 ID 서버에 B와 연결해 달라고 요청한다.
ID 서버는 홀 펀칭(hole punching)으로 A와 B를 직접 잇고,
실패하면 A와 B는 중계 서버를 거쳐 통신한다.
문서는 대부분의 경우 홀 펀칭이 성공해서 중계 서버는 쓰이지 않는다고 적는다.

이 구조 덕분에 사용자는 방화벽에 포트를 열지 않고도 접속할 수 있다.
2022년 HN 스레드에서도 VNC처럼 방화벽을 만질 필요가 없는 랑데부 구조가 첫
장점으로 꼽혔다[^jeroenhd].
README는 RustDesk가 제공하는 공개 서버를 쓰거나, 서버를 직접 세우거나,
랑데부·중계 서버를 직접 작성할 수 있다고 적는다.

### 코드 구조

README의 파일 구조 설명을 보면 화면 캡처는 `libs/scrap`, 키보드와 마우스 제어는
`libs/enigo`, 파일 복사·붙여넣기는 `libs/clipboard`가 맡는다.
`libs/hbb_common`은 비디오 코덱, 설정,
TCP/UDP 래퍼처럼 서버와 공유하는 코드를 담고, `src/rendezvous_mediator.rs`가
서버와 통신하며 직접 연결이나 중계 연결을 기다린다.
빌드에는 vcpkg로 설치하는 `libvpx`, `libyuv`, `opus`, `aom`이 필요하다.

VNC와 무엇이 다르냐는 질문에, pizza234는 VNC 계열이 주로 프레임버퍼 갱신을
보내는 반면 RustDesk는 현대 비디오 코덱과 시간 방향 압축으로 화면 변화를 훨씬
효율적으로 인코딩한다고 설명했다[^pizza234].

### Wayland 무인 접속

Linux 원격 데스크톱에서 오래 문제였던 것이 Wayland다.
2022년 HN 스레드에서는 Wayland에서 실행하면 GDM 설정을 고쳐 X11로 되돌리는
버튼을 띄운다는 지적이 가장 먼저 올라왔다[^proto_lambda].
같은 시기 GeekNews에서도 bbulbum이 그 버튼을 눌러 보니 Wayland를 끄는
버튼이었다며, 데스크톱 설정을 마음대로 바꾸지 말라고 적었다[^gn-bbulbum].
2025년 스레드에서도 Wayland에서는 접속할 때마다 원격 기기에서 승인해야 해서
원격의 의미가 없다는 불만이 나왔다[^sciencesama].

RustDesk는 2026년 8월 14일 블로그에서 Wayland에서 원격
기기 쪽 승인 없이 접속하는 진짜 무인 접속(unattended access)을 다중 모니터까지
지원한다고 발표했다.
처음 설정을 마치면 재부팅 뒤 로그인 화면에서도 접속할 수 있다.
다만 지금은 x86_64 Debian·Ubuntu 계열용 별도 미리보기 빌드이고,
안정화되면 Fedora와 Arch Linux로 넓힌 뒤 정식 릴리스에 넣을 계획이다.
글은 AnyDesk가 Linux로 들어오는 세션에 Xorg를 요구하고 TeamViewer는 Wayland
지원을 실험적이라고 설명한다며 경쟁 제품과 비교한다.
이 발표의 HN 스레드는 346점, 댓글 162개를 모았다.
superkuh는 이 기능이 DRM/KMS 프레임버퍼 캡처 라이브러리 `libdrmtap`에 기대며, 그
저장소가 스스로를 LLM으로 작성한 라이브러리라고 소개한다고 지적했다[^superkuh].

## 자체 호스팅

### 설치

홈페이지가 보여 주는 설치는 Docker를 깔고,
compose 파일을 받고, 띄우는 세 단계다.

```bash
bash <(wget -qO- https://get.docker.com)
wget rustdesk.com/oss.yml -O compose.yml    # Server Pro는 pro.yml
sudo docker compose up -d
```

OSS 설치 문서는 Docker를 권장하는 이유로 재현, 업그레이드, 서버 이전,
롤백이 쉽다는 점을 든다.
그 밖에 systemd 서비스를 만드는 커뮤니티 설치 스크립트와 Debian 패키지가 있다.
서버를 띄운 뒤 클라이언트에는 ID 서버 주소와 서버 공개 키를 넣고,
Server Pro라면 API 서버 주소도 넣는다.

### 서버 사양과 포트

문서는 하드웨어 요구가 매우 낮아 가장 작은 클라우드 서버나 라즈베리
파이로도 충분하다고 적는다.
비용을 정하는 것은 중계 트래픽이다.
홀 펀칭이 실패해 중계를 쓰면 연결 하나에 해상도와 화면 변화에 따라 초당 30KB에서
3MB(1920×1080)가 들고, 사무 작업이라면 초당 100KB 안팎이다.

최소로 필요한 포트는 TCP 21115~21117과 UDP 21116이다.
21118과 21119는 웹 클라이언트용 WebSocket 포트이고 HTTPS로 쓰려면
리버스 프록시가 필요하다.
Server Pro는 SSL 프록시가 없으면 API용으로 TCP 21114를,
프록시가 있으면 443을 연다.

```bash
ufw allow 21114:21119/tcp
ufw allow 21116/udp
sudo ufw enable
```

### OSS와 Pro

| 구분     | Server OSS                          | Server Pro                                                     |
| -------- | ----------------------------------- | -------------------------------------------------------------- |
| 대상     | 무료 자체 호스팅을 원하는 개인과 팀 | 중앙 관리가 필요한 회사                                        |
| 구성     | `hbbs`, `hbbr`, 수동 설정           | 웹 콘솔, API, OIDC, LDAP, 2FA, 기기 관리, 접근 제어, 다중 중계 |
| 지원     | Discord 커뮤니티                    | 이메일                                                         |
| 라이선스 | AGPL-3.0 소스                       | 유료 라이선스 키                                               |

가격 페이지는 이것이 SaaS 구독이 아니라 자체 호스팅 솔루션의
가격이라고 먼저 밝힌다.

| 요금제        | 연간 결제 기준 월 요금 | 포함                                                                                            |
| ------------- | ---------------------- | ----------------------------------------------------------------------------------------------- |
| Free          | $0                     | 오픈소스, 온라인 상태 표시, 커뮤니티 지원                                                       |
| Individual    | $11.88                 | 로그인 사용자 1명, 관리 기기 20대, 동시 연결 무제한, 2FA, 웹 콘솔, 주소록, 감사 로그, 접근 제어 |
| Basic         | $23.88                 | 사용자 10명, 기기 100대, OIDC(SSO), LDAP, 그룹 간 접근, 맞춤 클라이언트 생성기                  |
| Customized    | $23.88부터             | 사용자 1명당 $1.20, 기기 1대당 $0.12 추가                                                       |
| Customized V2 | $23.88부터             | 동시 연결 수 제한, 동시 연결 1개당 $24 추가                                                     |

결제는 연간만 있고 자동 갱신은 하지 않으며,
만료 14일 전에 갱신 안내 메일이 온다.
비영리나 교육 기관 할인은 아직 없고 무료 플랜을 쓰라고 권한다.
Server Pro에 통합된 웹 클라이언트는 사용자 수 × 10 + 기기 수가 400 이상인
플랜에서만 쓸 수 있다.
맞춤 클라이언트는 이름, 아이콘, 로고를 바꿔 자기 브랜드로 배포하는 기능이고,
설정 항목은 90개가 넘는다고 홈페이지는 적는다.

### 규모

7월 9일 블로그 글은 7월 7일 12코어, 32GB 메모리의 공개 서버 한 대에서 온라인
엔드포인트 200만 개 이상을 기록했다고 밝힌다.
글은 이 수치의 범위를 스스로 좁힌다.
온라인 엔드포인트는 그 순간 온라인으로
보고된 기기 수이지 동시 원격 제어 세션 수가 아니며,
외부 감사를 받은 벤치마크도 Server Pro 보장도 아닌 내부 관찰이라는 것이다.
Server Pro는 데이터베이스 쓰기,
감사 기록, 콘솔 조회, 정책 처리가 더해지므로 접속 변동, 동시 직접·중계 세션 수,
기록 보존 기간을 넣은 부하 테스트로 직접 확인하라고 권한다.
고가용성과 부하 분산은 기본 제공이 아니라 설계해야 하는 부분이라고도 적는다.

## 트레이드오프

### 자체 호스팅해도 인터넷과 완전히 끊을 수는 없다

자체 호스팅의 첫 이유는 데이터 통제다.
그러나 Server Pro는 완전한 오프라인이나 망 분리(air-gapped)
환경을 지원하지 않는다.
6월 28일 블로그 글에 따르면 Pro 라이선스는 활성화할 때와 운영하는 동안 계속
rustdesk.com에 443 포트로 연결해 검증해야 한다.
검사는 대략 하루에 한 번이고, 실패하면 성공하거나 약 7일이 지날 때까지 다시
시도하며, 그 뒤에는 라이선스 검증이 멈춘다.
맞춤 클라이언트를 생성하는 과정도 외부 연결을 기대한다.

글은 이 요구가 라이선스 때문이지 세션을 중개하기 위한 것이 아니며,
ID와 중계 서비스는 계속 자체 호스팅 상태라고 강조한다.
프록시를 지원하므로 rustdesk.com으로 가는 HTTPS 경로 하나만 열고
나머지를 막을 수 있다.
반대로 말하면 데이터 경로는 내 것이지만 기능의 존속은 판매사
서버에 묶여 있다는 뜻이다.
라이선스가 필요 없는 OSS 서버는 이 제약과 따로 다룬다고 글은 적는다.

### OSS 서버는 인증이 없다

ranger_danger는 서버를 자체 호스팅하면 인증 없이 열어 두는 수밖에 없어 누구나 그
서버로 스트림을 중계할 수 있고, 그래서 결국 VPN 뒤에 두게 되어 성능과 지연이
나빠진다고 지적했다[^ranger_danger].
이 경우 원격 지원 도구의 장점인 쉬운 접속이 사라진다.
Server Pro는 웹 콘솔, 사용자 인증, 접근 제어를 더하지만 유료다.
자체 호스팅의 비용을 서버 비용만으로 보면 이 부분을 놓친다.

Tailscale 같은 메시 VPN으로 서버 없이 쓰는 방법도 자주 나온다.
theturtletalks는 양쪽 기기에 Tailscale을 깔면 서버 없이 할당된 IP를 원격 ID 칸에
넣어 접속할 수 있다고 적었다[^theturtletalks].
jsisto는 그렇게 Tailscale을 쓸 거라면 왜 RDP를 쓰지 않느냐고 되물었다[^jsisto].
VPN 위에서 직접 연결을 쓰면 RustDesk의 랑데부 구조라는 장점이 빠지므로,
남는 이점은 코덱 성능과 여러 운영체제를 같은 도구로 다룬다는 점이다.

### 공개 서버는 공짜지만 통제권이 없다

설치 없이 바로 쓰는 공개 ID·중계 서버는 편하지만,
운영사가 정책을 바꾸면 그대로 따라야 한다.
2022년 GeekNews에서 guesswhat이 한국 서버가 있는 것이 신기하다고 적었을 만큼,
공개 서버는 지역별로 나뉘어 있다[^gn-guesswhat].
2026년 1월 HN에 올라온 글에 따르면 RustDesk는 봇넷 대응으로
공개 중계 서버에 같은 도시 안에서만 연결되도록 하는 제한을 예고 없이 걸었고,
해외에서 집 서버에 접속하던 사용자들이 막혔다[^gordian-mind].
게시자는 원래 공격이 수락 버튼을 눌러야 하는 자동 연결 요청이었고 비밀번호
인증을 쓰던 사용자는 처음부터 취약하지 않았다고 적었다.
이 사건은 GitHub 토론을 인용한 게시자의 설명이며,
나는 그 토론을 직접 확인하지 않았다.

## 함정

### WebSocket 포트는 IP를 위조당할 수 있다

OSS 설치 문서는 경고를 하나 둔다.
웹 클라이언트용 WebSocket 포트 21118,
21119를 열면 `hbbs`와 `hbbr`은 리버스 프록시 뒤의 실제 IP를 알기 위해
`X-Real-IP`와 `X-Forwarded-For` 헤더를 그대로 믿는다.
이 헤더는 검증하지 않으므로, 두 포트에 직접 닿을 수 있는 사람은 헤더를 위조해 IP
기반 속도 제한과 차단을 피하고 로그의 IP를 조작할 수 있다.
웹 클라이언트를 쓴다면 헤더를 직접 설정하는 리버스 프록시만 두 포트에 닿도록
방화벽을 걸고, 쓰지 않는다면 두 포트를 닫아 두라고 문서는 권한다.

### 콘솔에 모르는 기기가 나타난다

6월 30일 블로그 글은 Server Pro 콘솔에 낯선 기기가 등록되는 현상을 다룬다.
일부 백신과 EDR 제품은 처음 보는 바이너리를 클라우드 샌드박스에서 실행하고, 서버
설정이 들어간 맞춤 클라이언트가 그 안에서 ID 서버에 닿으면 잠깐 등록될 수 있다.
그러나 글은 클라우드 IP나 이상한 하드웨어 이름만으로 이 설명을
믿지 말라고 경고한다.
설정 유출, 무단 등록, 노출된 토큰도 같은 증상을 만들기 때문이다.

막는 방법은 두 가지다.
기기 목록이 거의 고정되어 있다면 웹 콘솔에서 새 기기 등록을 끈다.
계속 기기를 늘린다면 새 기기에 배포 토큰을 요구하고,
설치 과정에서 다음처럼 토큰을 넘긴다.

```bash
rustdesk --deploy --token <api_token>
```

글은 이 플래그가 릴리스마다 바뀔 수 있으니 Server Pro 문서에서 현재 문법을
확인하라고 덧붙인다.

### 맞춤 클라이언트 배포 경로가 곧 보안 경계다

맞춤 클라이언트에는 ID 서버 주소와 키가 들어 있다.
누구든 그 바이너리를 얻으면 서버에 기기를 등록할 수 있으므로,
배포 링크와 토큰을 비밀처럼 다뤄야 한다.
위의 샌드박스 사례도 결국 이 경로에서 생긴다.

### 사기범도 같은 도구를 쓴다

홈페이지가 공식 도메인을 따로 경고하는 이유는 원격 지원 도구가 기술 지원 사기의
단골 도구이기 때문이다.
2022년 스레드에서 benbristow는 사기범이 자기 서버를 세워 RustDesk를 쓰기
시작하면 서버 호스팅 업체에 IP를 신고하는 것 말고는 막을 방법이 없을 것이라고
내다봤다[^benbristow].
README의 첫 경고도 무단 접속과 사생활 침해 같은 오용을 지지하지
않는다는 면책 문구다.

## 비평

### 신뢰는 코드 공개만으로 생기지 않는다

RustDesk에 대한 HN 반응은 성능 칭찬과 신뢰 의심이 늘 함께 나온다.
2022년에는 README의 보안 걱정 없이(with no concerns about security)라는 문구가
조롱을 받았다[^rmbyrro].
Erlangen은 저자의 중국어 원문이 보안을 걱정하지 않아도 된다는 뜻이며 기계 번역
문제로 보인다고 설명했다[^Erlangen].
같은 스레드에서 pizza234는 뮤텍스 없이 `static mut`를 쓰는 코드를 들어 Rust를
쓰는 의미를 없애는 코드라고 비판했다[^pizza234-2022].

같은 의심은 Lobste.rs에서 더 구체적으로 나왔다.
2023년 11월 Tailscale과 함께 RustDesk를 쓰는 글에 달린 가장 높은
점수의 댓글에서, CobaltCause는 `rustdesk-server` 소스를 읽어 보니 많은 기능이
`sh`를 띄워 셸 코드를 실행하는 방식으로 구현되어 있다며 RustDesk가 무섭다고
적었다[^CobaltCause].
invlpg는 `/proc/self/sessionid`를 Rust에서 바로 읽지 않고 `cat`을 셸로 실행해
읽는 코드를 예로 들었다[^invlpg].
5d22b는 셸 호출은 강한 코드 냄새 정도지만,
멀티스레드 비동기 코드에서 동기화 없이 `static mut`에 접근하는 것은 그 자체로
정의되지 않은 동작(undefined behavior)이라고 짚었다[^5d22b].
dpc_pw는 이 `unsafe` 사용이 심각해 보인다며 업스트림에 이슈로 보고했다[^dpc_pw].
steinuil은 이런 코드가 Rust에 익숙하지 않은 개발자들이
시간 압박 속에서 제품을 내야 하는 팀의 강한 신호로 보인다고 했다[^steinuil].
2022년 HN에서 지적된 `static mut` 문제가 1년 넘게 같은 형태로 다시 나온 셈이다.

2024년 2월에는 Windows 클라이언트가 중국어 관리 정보를 가진 루트 인증서를 신뢰
저장소에 설치한다는 문제가 HN에 올라왔다.
게시자 lobito14가 옮긴 GitHub 답변에 따르면, 인증서가 왜 루트 저장소에
있는지, 왜 유효기간이 10년이고 SHA-1만 쓰는지에 대해 RustDesk는 자신들도 이 분야
전문가가 아니라 모르겠고 아마 테스트 인증서 때문일 것이라고 답했다[^lobito14].
cpach는 루트 인증서를 설치하는 것은 그 주체가 내 기기의 모든 TLS 연결을 몰래
가로챌 수 있게 하는 일이라며 이 앱을 피하라고 했다[^cpach].
ComputerGuru는 커널 드라이버 서명에는 Microsoft의 교차 서명이 필요하므로 루트에
인증서를 넣는 것만으로는 드라이버 서명 문제가 풀리지 않는다며 RustDesk의 설명이
맞지 않는다고 지적했다[^ComputerGuru].

2026년 Wayland 스레드에서는 GitHub 이슈와 토론이 지워진다는 불만이 나왔다.
yencabulator는 비밀번호 요구 사항에 관한 토론과 앞서 인용된 암호화 이슈가 모두
삭제되었다며 아주 나쁜 모습이라고 적었다[^yencabulator].
2025년에는 Server Pro가 AGPL 서버 코드 위에 만들어졌는데 소스를
배포하지 않는다는 의혹이 이슈로 제기되었고[^majorchord],
제기자는 작성자가 이슈를 통째로 지웠다고 주장했다[^majorchord-deleted].
이 의혹은 한쪽의 주장이고 법적 판단을 거친 것은 아니다.

이 이력이 말하는 것은 RustDesk가 악성이라는 뜻이 아니다.
원격 접속 도구는 사용자 기기 전체를 넘겨받는 소프트웨어이므로,
소스 공개만큼이나 의문에 대한 대응 방식이 신뢰를 결정한다는 뜻이다.
홈페이지는 데이터 통제와 규정 준수를 앞세우지만,
루트 인증서나 이슈 삭제 같은 질문에 대한 답은 홈페이지 어디에도 없다.

### 암호화 논쟁은 문서가 부족해서 반복된다

Wayland 스레드의 첫 댓글은 RustDesk가 자체 호스팅에서 암호화 연결을 지원하지
않는다는 주장이었다[^inktype].
곧바로 여러 반박이 붙었다.
wolrah는 자체 호스팅 서버를 써도 연결은 완전히 암호화되며, 지원하지 않는 것은
서버를 전혀 거치지 않는 기기 간 직접 연결의 암호화라고 정정했다[^wolrah].
wooben은 이 제한이 기본으로 꺼져 있는 로컬 네트워크의 직접 IP 접속에만
해당한다고 덧붙였다[^wooben].

이 논쟁이 2022년부터 반복된다는 점이 문제다.
2022년 스레드에서도 Snuupy는 암호화 같은 기능을 라이선스 뒤에
잠근다고 의심했다[^Snuupy].
어떤 경로가 암호화되고 어떤 경로가 아닌지를 홈페이지와 자체 호스팅 문서가 한눈에
보여 준다면 이런 오해는 줄어든다.
원격 접속 제품에서 암호화 범위는 기능 목록의 한 줄이 아니라 첫
화면에 있어야 할 계약이다.

### 비교 마케팅이 운영 비용을 가린다

홈페이지는 SaaS의 불안정한 성능, 불투명함,
불확실한 데이터 보안을 문제로 들고 자체 호스팅을 해답으로 제시한다.
그러나 위에서 본 것처럼 자체 호스팅에는 인증 없는 OSS 서버, WebSocket 헤더 위조,
맞춤 클라이언트 유출, 라이선스 서버 의존이라는 운영 과제가 따라온다.
블로그에는 이런 함정을 다룬 글이 꽤 있지만 홈페이지는 세 단계 설치로
준비 끝이라고만 말한다.
TeamViewer 비용을 줄이려는 팀이라면 라이선스 비용과 함께 이 운영 책임을
비교표에 넣어야 한다.

## 인사이트

### 원격 지원 시장의 균열은 가격보다 신뢰에서 났다

HN 댓글에서 사람들이 RustDesk로 옮긴 이유는 대개 기존 제품에 대한 실망이다.
vablings는 TeamViewer가 망가진 뒤 AnyDesk가 그 자리를 먹었고 그것도 망가져서
이제 RustDesk가 왔다고 정리했다[^vablings].
xupybd는 TeamViewer가 결제를 잘못 처리하고 말없이 환불한 뒤 소송하겠다는 편지를
보내서 떠났다고 적었다[^xupybd].
2Gkashmiri는 AnyDesk의 광고가 늘어나서 RustDesk로 옮겼다고 했다[^2Gkashmiri].

흥미로운 점은 사용자들이 RustDesk를 신뢰해서 옮긴 것이 아니라 기존 제품을
신뢰하지 않게 되어 옮겼다는 것이다.
그래서 RustDesk의 신뢰 의심은 이 흐름을 막지 못했다.
이 구조는 오픈소스 대안이 상용 제품의 실수로 시장을 얻는 전형적인 경로이고,
그만큼 대안 쪽의 실수에도 같은 속도로 사용자를 잃을 수 있다는 뜻이다.

### 오픈코어 원격 접속은 인증을 유료 경계로 쓴다

OSS 서버에는 사용자 인증과 웹 콘솔이 없고, Pro에는 있다.
원격 접속 도구에서 인증은 부가 기능이 아니라 서버를 인터넷에 내놓을 수
있느냐를 가르는 조건이다.
그래서 이 경계는 OSS 사용자를 VPN 뒤로 밀어 넣고, 회사 사용자를 Pro로 이끈다.
오픈코어 사업에서 흔히 SSO를 유료 기능으로 두는 것과 같은 설계이지만,
원격 접속에서는 그 경계가 보안 자체와 겹친다는 점이 다르다.
AGPL 서버 위에 비공개 Pro를 올렸다는 의혹이 제기된 것도 이 경계가 그만큼 사업의
중심에 있기 때문으로 읽힌다.

### 자체 호스팅의 정의가 바뀌고 있다

Server Pro의 라이선스 검증 구조는 자체 호스팅이 무엇을 뜻하는지 다시 묻게 한다.
세션 데이터는 내 서버를 지나지만, 7일 동안 rustdesk.com에 닿지
못하면 관리 기능이 멈춘다.
이런 구조는 데이터 주권과 기능 주권을 분리한다.
규제 산업이 원하는 것은 대개 앞쪽이고, 망 분리 환경이 원하는 것은 둘 다다.
자체 호스팅 제품을 고를 때는 데이터가 어디를 지나는지뿐 아니라,
판매사 서버가 사라지면 무엇이 멈추는지를 함께 물어야 한다.

### Wayland 지원은 Linux 데스크톱의 원격 접속 비용을 보여 준다

Wayland는 보안을 위해 애플리케이션이 화면을 읽고 입력을 넣는 것을 막는다.
그 결과 원격 접속 도구는 DRM/KMS 캡처와 `uinput` 같은 특권 경로로 내려가야 한다.
jchw는 로그인 화면까지 다루려면 대개 DRM/KMS
캡처와 `uinput` 장치 에뮬레이션을 쓰며,
루트까지는 아니어도 일반 사용자에게 없는 권한이 필요하다고 설명했다[^jchw].
결국 Wayland에서 무인 접속을 얻는다는 것은 Wayland가 막으려던 권한을 원격 접속
데몬에 다시 주는 일이다.
RustDesk가 이 기능을 미리보기 빌드로 따로 낸 것은 기술적 난도만큼이나 이 권한
문제의 무게 때문일 것이다.

---

[^jeroenhd]: <https://news.ycombinator.com/item?id=31456443>

[^pizza234]: <https://news.ycombinator.com/item?id=49302466>

[^proto_lambda]: <https://news.ycombinator.com/item?id=31456522>

[^sciencesama]: <https://news.ycombinator.com/item?id=44284998>

[^superkuh]: <https://news.ycombinator.com/item?id=49306867>

[^ranger_danger]: <https://news.ycombinator.com/item?id=49311330>

[^theturtletalks]: <https://news.ycombinator.com/item?id=44284758>

[^jsisto]: <https://news.ycombinator.com/item?id=44286099>

[^gordian-mind]: <https://news.ycombinator.com/item?id=46840656>

[^benbristow]: <https://news.ycombinator.com/item?id=31456452>

[^rmbyrro]: <https://news.ycombinator.com/item?id=31456645>

[^Erlangen]: <https://news.ycombinator.com/item?id=31457771>

[^pizza234-2022]: <https://news.ycombinator.com/item?id=31457238>

[^lobito14]: <https://news.ycombinator.com/item?id=39296372>

[^cpach]: <https://news.ycombinator.com/item?id=39260241>

[^ComputerGuru]: <https://news.ycombinator.com/item?id=39266403>

[^yencabulator]: <https://news.ycombinator.com/item?id=49332852>

[^majorchord]: <https://news.ycombinator.com/item?id=45385537>

[^majorchord-deleted]: <https://news.ycombinator.com/item?id=45387890>

[^inktype]: <https://news.ycombinator.com/item?id=49302135>

[^wolrah]: <https://news.ycombinator.com/item?id=49310586>

[^wooben]: <https://news.ycombinator.com/item?id=49302667>

[^Snuupy]: <https://news.ycombinator.com/item?id=31457047>

[^vablings]: <https://news.ycombinator.com/item?id=49301884>

[^xupybd]: <https://news.ycombinator.com/item?id=44285128>

[^2Gkashmiri]: <https://news.ycombinator.com/item?id=31456712>

[^jchw]: <https://news.ycombinator.com/item?id=49304012>

[^CobaltCause]: <https://lobste.rs/s/njfvjb/rustdesk_with_tailscale_on_arch_linux#c_5dyag0>

[^invlpg]: <https://lobste.rs/s/njfvjb/rustdesk_with_tailscale_on_arch_linux#c_2gkvdv>

[^5d22b]: <https://lobste.rs/s/njfvjb/rustdesk_with_tailscale_on_arch_linux#c_i4x9gc>

[^dpc_pw]: <https://lobste.rs/s/njfvjb/rustdesk_with_tailscale_on_arch_linux#c_hlgvkq>

[^steinuil]: <https://lobste.rs/s/njfvjb/rustdesk_with_tailscale_on_arch_linux#c_czn8li>

[^gn-bbulbum]: <https://news.hada.io/topic?id=6621#cid10155>

[^gn-guesswhat]: <https://news.hada.io/topic?id=6621#cid10147>
