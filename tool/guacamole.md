# Apache Guacamole: 브라우저 하나로 VNC, RDP, SSH에 접속하는 원격 데스크톱 게이트웨이

<https://guacamole.apache.org/>

<https://github.com/apache/guacamole-server>

<https://github.com/apache/guacamole-client>

HN 토론: <https://news.ycombinator.com/item?id=15389727> (1096점, 216개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=29442643> (503점, 116개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=39867702> (215점, 50개 댓글)

GN 토론: <https://news.hada.io/topic?id=5495>

## 소개

Apache Guacamole은 클라이언트 없는(clientless) 원격 데스크톱 게이트웨이다.
홈페이지는 VNC, RDP, SSH 같은 표준 프로토콜을 지원하며, 플러그인이나 클라이언트
소프트웨어가 필요 없어서 클라이언트 없는 게이트웨이라고 부른다고 설명한다.
서버에 Guacamole을 설치하면 데스크톱에 접속하는 데 필요한 것은 HTML5를
지원하는 웹 브라우저뿐이다.

Apache Software Foundation 프로젝트이고 라이선스는 Apache License 2.0이다.
홈페이지는 Guacamole이 앞으로도 언제나 자유 오픈소스 소프트웨어로 남을 것이며,
자기 개발 환경에 접속하려고 Guacamole을 쓰는 개발자 커뮤니티가
유지보수한다고 적는다.
지원은 공개 메일링 리스트로 받고, 전담 상용 지원은 제3자 회사들이 제공한다.

현재 릴리스는 2025년 6월 22일의 1.6.0이다.
릴리스 노트는 렌더링 성능 개선, Docker 지원 개선, 대소문자 구분 설정,
연결 일괄 가져오기, Duo v4 지원을 꼽는다.
그 전의 1.5.5는 2024년 4월 5일에 나왔으므로 정식 릴리스 사이의
간격이 1년을 넘는다.
GitHub에서 C로 작성된 `guacamole-server`는 스타 3,997개,
Java로 작성된 `guacamole-client`는 스타 1,723개이고, 두 저장소 모두 2026년
9월까지 커밋이 이어지고 있다.

## 동작 방식

### 세 층으로 나뉜 구조

매뉴얼의 아키텍처 장은 Guacamole을 세 부분으로 나눈다.

| 구성 요소             | 언어       | 하는 일                                              |
| --------------------- | ---------- | ---------------------------------------------------- |
| JavaScript 클라이언트 | JavaScript | 브라우저에서 화면을 그리고 입력을 보낸다             |
| 웹 애플리케이션       | Java       | 인증과 웹 인터페이스, 클라이언트와 `guacd` 사이 중계 |
| `guacd`               | C          | 실제 원격 데스크톱 프로토콜로 접속하는 프록시 데몬   |

사용자가 서버에 접속하면 브라우저는 JavaScript로 된 클라이언트를 내려받는다.
이 클라이언트는 Guacamole 프로토콜로 서버에 다시 연결한다.
웹 애플리케이션은 그 프로토콜을 읽어 `guacd`에 넘기고, `guacd`가 사용자를
대신해 원격 데스크톱 서버에 접속한다.

핵심은 웹 애플리케이션이 어떤 원격 데스크톱 프로토콜도 모른다는 점이다.
VNC나 RDP를 이해하는 것은 `guacd`가 동적으로 불러오는 클라이언트
플러그인뿐이고, 웹 애플리케이션은 인증과 인터페이스만 맡는다.
매뉴얼은 이 덕분에 클라이언트와 웹 애플리케이션 모두 실제로 어떤 프로토콜이
쓰이는지 알 필요가 없다고 설명한다.
웹 애플리케이션을 Java로 만든 것도 선택일 뿐이고,
Guacamole은 API로 쓰이도록 설계되었으니 다른 언어로 만들어도 된다고 권한다.

### Guacamole 프로토콜

Guacamole 프로토콜은 원격 화면 렌더링과 이벤트 전달을 위한
텍스트 기반 프로토콜이다.
매뉴얼은 이것을 기존 원격 데스크톱 프로토콜들의 상위 집합이라고 부른다.
새 프로토콜을 지원하려면 그 프로토콜과 Guacamole 프로토콜 사이를 번역하는 중간
층을 쓰면 되고, 이는 화면을 로컬이 아니라 원격에 그리는 네이티브 클라이언트를
만드는 일과 같다고 설명한다.
그 번역 층이 `guacd`이고,
`guacd`와 모든 클라이언트 플러그인은 공통 라이브러리 `libguac`를 쓴다.

프로젝트의 시작은 RealMint라는 JavaScript 텔넷 클라이언트였다.
RealMint는 terminal의 철자를 바꾼 이름이고, PHP로 쓴 롱 폴링 터널을 썼다.
이후 HTML5 canvas가 Firefox와
Chrome에 들어오자 VNC를 XML로 번역하는 JavaScript VNC 클라이언트를 만들었고,
이것이 SourceForge에 HTML5 VNC 클라이언트 Guacamole로 등록되었다.
당시에는 WebSocket을 믿을 수 없어서 HTTP 기반 터널을 만들었는데, 이 터널은
WebSocket을 쓸 수 없을 때를 위해 지금도 남아 있다.
그 뒤 여러 프로토콜을 담는 더 빠른 텍스트 프로토콜과 `guacd`,
`libguac`로 구조를 다시 짜면서 지금의 게이트웨이가 되었다.

## 설치하기

### Docker로 띄우기

매뉴얼이 권하는 Docker 배포는 컨테이너 세 개로 이루어진다.

- `guacamole/guacd`: `guacamole-server` 릴리스로 빌드한 `guacd`이며 VNC, RDP, SSH, 텔넷, Kubernetes를 지원한다.
- `guacamole/guacamole`: Tomcat 9.x 위의 웹 애플리케이션이며 WebSocket을 지원하고, `guacd`, MySQL, PostgreSQL, LDAP 연결 설정을 환경 변수에서 읽는다.
- `mysql` 또는 `postgresql`: 인증과 연결 설정을 저장하는 데이터베이스다.

매뉴얼은 이렇게 나눈 덕분에 업그레이드할 때 데이터를 유지해야 하는 컨테이너는
데이터베이스 하나뿐이라고 설명한다.
`guacd` 이미지에는 SSH와 텔넷용 글꼴,
FreeRDP 플러그인 위치처럼 직접 빌드할 때 흔히 틀리는 부분이 이미 들어 있다.

```bash
docker network create guac-net
# guacd는 기본 포트 4822로 듣지만, 이 네트워크 안에서만 닿는다
docker run --network=guac-net --name some-guacd -d guacamole/guacd
```

Guacamole 컨테이너와 함께 쓸 때는 `guacd`의 포트를 바깥에 열 필요가 없다.
`-p 4822:4822`로 포트를 열면 Docker 밖의 Tomcat도 `guacd`에 붙을 수 있지만,
매뉴얼은 따로 경고한다.
`guacd`는 아무 인증도 하지 않는 수동 프록시이므로, 신뢰할 수 없는 네트워크에서
격리하지 않으면 공격자가 다른 시스템으로 넘어가는 발판으로 쓸 수 있다.

### 설치가 어렵다는 평

HN에서는 설치에 대한 불만이 꾸준히 나왔다.
_8j50은 Docker로도 배포가 쉽지 않았고 Tomcat을 설정해야 했다고 적었다[^_8j50].
skanga는 Docker를 쓰지 않는 사용자를 위한 설치 절차가 터무니없다며
개선을 요구했다[^skanga].
moontear는 직접 구성하는 것보다 Docker 컨테이너가 훨씬 쉽다고 했다[^moontear].
Docker 이미지가 1.6.0에서도 개선 항목에 오른 것은 이 마찰을 프로젝트도 알고
있다는 뜻으로 읽힌다.

## 쓰임새

### 인증을 앞에 둔 접속 관문

HN 사용자들이 가장 많이 꼽은 쓰임새는 원격 데스크톱 앞에 웹
인증을 두는 관문이다.
NovemberWhiskey는 Windows 운영 서버 접속에 Guacamole을 도입했는데, 회사 SSO와
권한 모델을 웹 애플리케이션에 넣어 접근을 통제하면서 서비스 계정의 자격 증명을
사람들에게 알려 주지 않아도 된다는 점이 좋다고 했다[^NovemberWhiskey].
ldoughty는 Guacamole이 회사가 통제하는 중간자 역할을 하므로,
서버 쪽 계정이 허술해도 Guacamole을 거쳐야만 닿는다면 Guacamole만 인터넷에
노출하면 된다고 설명했다[^ldoughty].
buybackoff는 RDP를 인터넷에 그대로 여는 것이 불안해서 쓰며,
HTTPS 쪽이 NGINX 같은 보안 층을 더하기 쉽다고 했다[^buybackoff].

GeekNews에서 randomparty는 회사에서 쓰는 장점으로 세션 공유를 꼽았다.
RDP도 VNC처럼 화면을 같이 볼 수 있고 터미널도 마찬가지이며, 원격 접속 중의 작업
기록을 영상이나 텍스트로 남길 수 있다는 것이다[^gn-randomparty].

1.x 릴리스 노트에는 이 쓰임새를 받치는 기능이 쌓여 있다.
1.2.0의 SAML 2.0과 TOTP 개선, 1.3.0의 CAS와 OpenID 사용자 그룹,
1.5.0의 녹화 재생, 키 볼트, 여러 LDAP·AD 서버 지원이 그 예다.
FAQ는 기존 애플리케이션에 인증이 있으니 Guacamole의 인증을 끄고 싶다는 질문에,
대문자로 절대 끄지 말라고 답한다.
이미 다른 곳에서 인증했더라도 사용자마다 인증 상태를 확인하는 것만이 안전하며,
올바른 방법은 각 사용자를 검증하는 Guacamole 확장을 쓰는 것이라고 설명한다.

### 교육과 실습 환경

교육 용도도 자주 나온다.
ldoughty는 학생에게 Kali Linux
박스와 취약점을 일부러 넣은 서버를 주는 실습에서 Guacamole을 관문으로 쓰므로,
취약한 대상이 외부로 노출될 걱정을 하지 않는다고 했다[^ldoughty-2].
adamretter는 교육 과정에서 Ubuntu LXDE 가상 머신 10대에 RDP로 접속하게 했는데
대체로 잘 동작했지만 Microsoft 원격 데스크톱 클라이언트만큼 매끄럽지는 않았다고
적었다[^adamretter].
jstrieb은 GitHub Actions 워크플로를 원격 데스크톱으로 열어 다른 운영체제의 GUI
앱을 시험하는 데 썼다고 소개했다[^jstrieb].

개인 용도도 있다.
GeekNews의 joyfui는 NAS에 설치해 가끔 잘 쓰고 있고,
가장 잘 쓴 때는 군대에 있을 때였다고 적었다[^gn-joyfui].

### 상용 제품을 대체하는 경우

sparcpile은 OpenText가 Exceed OnDemand 지원을 끝내고 후속 제품 FastX에 너무 비싼
값을 매기자 Guacamole로 옮겼다고 했다[^sparcpile].
데모를 받으려면 내부 아키텍처를 먼저 알려 달라고 요구받았다는 경험도 덧붙였다.

## 함정

### 브라우저가 단축키를 먼저 가져간다

linuxandrew는 SSH와 RDP를 모두 Guacamole로 쓰면서,
bash에서 단어를 지우려고 `Ctrl+W`를 누르는 습관
때문에 Firefox 탭이 닫히는 일이 가장 짜증스러웠다고 적었다[^linuxandrew].
FAQ도 키보드 단축키가 원격 데스크톱이 아니라 브라우저나 운영체제에 먼저
잡히는 문제를 따로 다룬다.
클립보드도 비슷하다.
FAQ에 따르면 Guacamole은 W3C Clipboard API를 쓰려고
하지만 브라우저마다 지원이 달라서, Chrome 66과 Edge 79 이후는 읽기와 쓰기를,
Firefox 63 이후는 쓰기만 지원한다.

### VNC 연결은 느리다

GeekNews의 platanus는 RDP는 모르겠지만 VNC로 쓸 때 실사용성은 0에 가깝다며,
SSH도 지원하니 간단한 작업용 게이트웨이로는 좋아 보였다고
평가했다[^gn-platanus].
NotionSSH를 만든 mirseo도 Guacamole을 써 봤지만 VNC 특성상 느려서 지연
때문에 영향을 많이 받았다고 답했다[^gn-mirseo].
내 해석으로는 VNC의 화면 갱신 방식에 브라우저 렌더링이 한 겹 더 얹히는 탓이므로,
그래픽 작업이 많다면 RDP 연결을 먼저 고려하는 편이 낫다.

### 화면 크기는 프로토콜이 정한다

RDP는 처음 접속할 때만 화면 크기를 정할 수 있으므로 브라우저 창 크기를 바꿔도
따라오지 않고 다시 접속해야 한다.
VNC는 화면 크기를 VNC 서버가 정하므로 클라이언트가 바꿀 수 없다.
이것은 Guacamole의 한계라기보다 밑에 깔린 프로토콜의 성질이지만,
브라우저에서 쓰는 사람은 Guacamole 탓으로 느끼기 쉽다.

### iframe에 넣으면 키보드가 깨진다

FAQ는 Guacamole을 `<iframe>`으로 다른 페이지에 넣는 방식을 권하지 않는다.
포커스를 한 번 잃으면 iframe 안을 클릭해도 키보드 포커스가 돌아오지
않을 수 있기 때문이다.
대신 JavaScript API인 `guacamole-common-js`로 페이지에 직접 넣거나,
Java API인 `guacamole-common`으로 자기 웹 애플리케이션을 만들라고 권한다.
데이터베이스나 XML을 스크립트로 직접 고쳐 연동하려는 시도에도, 확장 API
`guacamole-ext`로 기존 시스템에서 데이터를 가져오는 확장을 쓰라고 답한다.

### X11, NX, X2Go는 지원하지 않는다

FAQ는 SSH의 X11 포워딩, NX, X2Go 지원 요청에 모두 아니라고 답한다.
X11 서버를 구현하는 일이 너무 복잡하고, NXv3은 X11을 압축하는 방법이며,
NXv4는 공개 문서가 없는 독점 프로토콜이기 때문이다.
대신 Guacamole 프로토콜을 쓰는 X.Org 그래픽 드라이버를 개발 중이라고 밝힌다.

## 비평

### 보안 관문 자체가 공격면이다

Guacamole을 쓰는 가장 큰 이유는 원격 데스크톱 앞에 관문을 두는 것이다.
그런데 보안 공지를 보면 그 관문이 여러 번 코드 실행 취약점을 가졌다.
1.6.0에서 고친 CVE-2024-35164는 1.5.5 이하의 터미널 에뮬레이터가 SSH 같은 텍스트
프로토콜로 받은 콘솔 코드를 제대로 검증하지 않아, 텍스트 연결에 접근할 수 있는
악의적인 사용자가 `guacd` 권한으로 임의 코드를 실행할 수 있었던 문제다.
1.5.4의 CVE-2023-43826은 악성 VNC 서버가 보낸 값으로 정수 오버플로와 메모리
손상을 일으킬 수 있었고, 1.5.2의 CVE-2023-30576은 RDP 오디오 입력 버퍼의 해제 후
사용(use-after-free) 문제였다.
1.4.0의 CVE-2021-43999는 SAML 응답을 제대로 검증하지 않아 다른 사용자로
행세할 수 있었던 인증 우회다.

이 목록이 말하는 것은 Guacamole이 특별히 허술하다는 것이 아니다.
여러 프로토콜을 C로 번역하는 프록시는 각 프로토콜의 공격면을 모두 한곳에 모은다.
관문을 두면 원격 데스크톱 서버를 직접 노출하지 않아도 되지만,
관문의 `guacd`가 뚫리면 그 뒤의 모든 서버로 가는 길이 열린다.
홈페이지는 이 거래를 언급하지 않으므로,
운영자는 보안 공지를 직접 구독하고 업데이트를 미루지 말아야 한다.

### 오래된 웹 기반이 남아 있다

보안 페이지에는 AngularJS에 대한 별도 항목이 있다.
Guacamole 1.x는 호환성을 위해 지원이 끝난 AngularJS를 계속 쓰며,
2.0.0부터 Angular로 옮길 계획이라고 밝힌다.
페이지는 AngularJS에 보고된 CVE를 하나씩 나열하며 Guacamole이 해당 기능을 쓰지
않아 영향이 없다고 설명한다.
설명 자체는 성실하지만, 사용자가 보안 감사에서 지원 종료된 프레임워크를 매번
해명해야 한다는 부담은 남는다.
2.0.0의 일정은 페이지에 나와 있지 않다.

### 클라이언트가 없다는 말은 절반만 맞다

charcircuit은 플러그인이나 클라이언트
소프트웨어가 필요 없다면서 웹 브라우저만 있으면 된다고 하는 것은 말이 안 된다며,
클라이언트가 없다는 표현을 꼬집었다[^charcircuit].
브라우저가 곧 클라이언트이고, 그 브라우저의 키보드 처리, 클립보드 권한,
포커스 정책이 사용 경험을 좌우한다.
앞의 함정 대부분이 이 지점에서 나온다.
설치할 것이 없다는 장점은 분명하지만, 그 대가로 브라우저라는 범용 클라이언트의
제약을 그대로 받는다.

### Java 서버가 무겁다는 불만

rcarmo는 여러 연결을 동시에 열면 프록시가 크게 부풀어서 Java 백엔드가 필요 없는
대안을 찾고 있다고 했다[^rcarmo].
jakestl은 Java 클라이언트가 하는 일이 필요 없어서 일부를 Go로 옮긴 적이
있다고 답했다[^jakestl].
PenguinCoder는 Guacamole을 오래 썼지만 KasmWeb으로 바꿨고 훨씬 매끄러우며 Java도
없다고 했다[^PenguinCoder].
Teleport의 benarent는 Windows와 RDP 지원 요청이 많아서 Go와 Rust로 자체 RDP
클라이언트를 만들어 프로토콜과 인증을 더 통제하게 되었다고 소개했다[^benarent].
아키텍처가 웹 애플리케이션을 갈아 끼울 수 있게 설계되었다는 점은 이런 불만에
대한 답이 될 수 있지만, 실제로 갈아 끼우는 비용은 사용자가 진다.

## 인사이트

### 프로토콜 번역 계층은 원격 접속의 표준 인터페이스가 된다

Guacamole의 설계에서 가장 오래 남을 부분은 웹 애플리케이션이 원격 데스크톱
프로토콜을 모른다는 결정이다.
VNC, RDP, SSH, 텔넷, Kubernetes가 모두 하나의 화면·입력 프로토콜로 번역되므로,
위쪽에서는 인증, 녹화, 권한, 공유를 프로토콜과 상관없이 한 번만 구현하면 된다.
이 구조는 데이터베이스 드라이버나 컨테이너 런타임 인터페이스처럼 아래의 다양성을
위의 단일 인터페이스로 묶는 익숙한 패턴이다.
그래서 Guacamole은 완성된 제품이면서 동시에 다른 제품이 그 위에
올라가는 부품으로도 쓰인다.
`linuxserver`의 Calibre Docker 이미지가 Guacamole을
쓴다는 HN 댓글[^zaptheimpaler]처럼, 데스크톱 앱을 브라우저로 내보내야 하는 많은
프로젝트가 이 계층을 그대로 빌려 쓴다.

### 제로 트러스트 이전의 제로 트러스트

NovemberWhiskey와 ldoughty가 설명한 쓰임새는 지금 말하는 제로 트러스트
접근(ZTNA)과 같은 모양이다.
네트워크 위치가 아니라 사용자 인증으로 접근을 정하고,
서버는 관문 뒤에 숨기고, 접속은 기록한다.
Guacamole은 이 개념이 유행하기 전부터 오픈소스로 그것을 제공해 왔다.
반대로 상용 ZTNA 제품이 RDP와 SSH를 브라우저로 여는 기능을 내놓으면서,
Guacamole의 독자적인 자리는 직접 운영하고 싶은 조직으로 좁아지고 있다.
그 조직에게 Guacamole이 주는 값은 기능보다 통제권이다.

### 느린 릴리스 주기는 관문 소프트웨어에서 비용이 커진다

1.5.5에서 1.6.0까지 1년 2개월이 걸렸고, 그 사이 CVE-2024-35164는
1.5.5 이하에 남아 있었다.
일반 애플리케이션이라면 릴리스 간격이 긴 것은 안정성의 신호일 수 있지만, 모든
원격 접속이 지나가는 관문에서는 패치를 기다리는 시간이 그대로 노출 시간이 된다.
Apache 프로젝트의 릴리스 절차와 자원봉사 중심의 유지보수가 이 속도를 정한다.
Guacamole을 운영하는 조직이 상용 지원 회사를 쓰거나,
소스에서 보안 패치를 직접 빌드할 준비를 해 두는 이유가 여기에 있다.

---

[^_8j50]: <https://news.ycombinator.com/item?id=29445694>

[^skanga]: <https://news.ycombinator.com/item?id=29445413>

[^moontear]: <https://news.ycombinator.com/item?id=29443181>

[^NovemberWhiskey]: <https://news.ycombinator.com/item?id=29443539>

[^ldoughty]: <https://news.ycombinator.com/item?id=29444941>

[^buybackoff]: <https://news.ycombinator.com/item?id=29444536>

[^ldoughty-2]: <https://news.ycombinator.com/item?id=29444273>

[^adamretter]: <https://news.ycombinator.com/item?id=39869669>

[^jstrieb]: <https://news.ycombinator.com/item?id=29444235>

[^sparcpile]: <https://news.ycombinator.com/item?id=39870168>

[^linuxandrew]: <https://news.ycombinator.com/item?id=39869207>

[^charcircuit]: <https://news.ycombinator.com/item?id=29445793>

[^rcarmo]: <https://news.ycombinator.com/item?id=39869246>

[^jakestl]: <https://news.ycombinator.com/item?id=39869443>

[^PenguinCoder]: <https://news.ycombinator.com/item?id=39870647>

[^benarent]: <https://news.ycombinator.com/item?id=39871265>

[^zaptheimpaler]: <https://news.ycombinator.com/item?id=29446595>

[^gn-randomparty]: <https://news.hada.io/topic?id=5495#cid8190>

[^gn-joyfui]: <https://news.hada.io/topic?id=5495#cid7801>

[^gn-platanus]: <https://news.hada.io/topic?id=5495#cid7812>

[^gn-mirseo]: <https://news.hada.io/topic?id=23014#cid44557>
