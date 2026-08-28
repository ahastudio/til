# Tailcat: 계정도 제어 서버도 없이 두 머신을 잇는 netcat

<https://tailscale.com/tailcat>

<https://github.com/tailscale/tailcat>

HN 토론: <https://news.ycombinator.com/item?id=49452990> (640점, 120개 댓글)

## 소개

Tailcat은 Tailscale의 오픈소스 데이터 플레인 조각들을 엮어
두 머신 사이에 암호화된 점대점 연결을 만드는 도구다.
문서의 표현으로는 “Tailscale의 오픈소스 조각들을 리믹스해
netcat처럼 동작하되, Tailscale의 데이터 플레인 위에서,
Tailscale의 제어 플레인 없이” 작동한다.
결정적 차이는 사용자가 Tailscale 계정도, 관리자 권한도 필요 없다는 점이다.
라우팅 테이블이나 DNS를 건드리지 않고 root도 요구하지 않는
유저스페이스 라이브러리이자 CLI다.
Go로 작성되었고 BSD 3-Clause 라이선스이며 별 1,580개를 받았다.

## 작동 방식

Tailcat은 네 가지 Tailscale 구성 요소를 유저스페이스에서 조합한다.
WireGuard(Curve25519 기반)의 유저스페이스 구현이 모든 터널 트래픽을 암호화하고,
DERP 릴레이가 NAT 통과의 랑데부 지점이자 직접 연결이 실패할 때의
대체 경로 역할을 한다.
Magicsock은 직접 UDP 연결과 DERP 릴레이를 다중화하며
STUN 기반 엔드포인트 발견과 UDP 홀펀칭으로 NAT를 뚫고,
gVisor의 netstack이 유저스페이스 TCP/IP 스택으로서
OS 수준 네트워크 설정 없이 TCP 연결을 주고받게 한다.

연결은 `tcXYZ...` 형태의 짧은 토큰으로 시작한다.
이 토큰은 base64로 인코딩된 CBOR 데이터로,
서버의 WireGuard 공개키 32바이트와
DERP 정보(지역 ID 또는 전체 서버 메타데이터)를 담는다.
보통 토큰은 약 50바이트이며,
DERP 정보를 통째로 넣은 자기완결형 토큰은 더 길지만
클라이언트가 릴레이 정보를 따로 조회할 왕복을 없앤다.
연결 흐름은 서버가 키쌍을 만들고 DERP에 접속해 토큰을 출력하면,
클라이언트가 토큰에서 공개키와 DERP 지역을 뽑아
DERP를 통해 “Meow” 핑을 보내고 서버가 “Meowed”로 답하며 시작된다.
이후 표준 WireGuard 핸드셰이크가 처음에는 DERP를 거쳐 진행되고,
양쪽이 disco call-me-maybe 메시지로 UDP 엔드포인트를 교환해
가능하면 직접 P2P 경로로 승격시킨다.

## 사용법

가장 단순한 사용은 두 머신 사이의 파이프다.
서버에서 `tailcat`을 실행하면 토큰을 출력하며 대기하고,
클라이언트에서 `echo hello | tailcat <토큰>`을 실행하면
서버가 `hello`를 받는다.
`--serve=8080,8443`으로 로컬 TCP 포트를 노출하고,
클라이언트는 `tailcat <토큰> 8080`으로 그 포트에 접속한다.
`--serve=no-auth-ssh`는 인증 없는 SSH 서버를 띄우고
`tailcat ssh <토큰>`으로 붙는다.
그 밖에 `tailcat ping --until-direct`로 직접 연결이 될 때까지 핑을 보내고,
`tailcat socks`로 SOCKS5 프록시를, `--serve=exit-node`로 exit 노드를 제공한다.

키는 기본적으로 일회성이다.
서버 실행마다 메모리에 새 키를 만들고 프로세스가 끝나면 토큰이 무효가 되어,
일회성 공유에 안전한 기본값이 된다.
`tailcat genkey`로 지속 키를 만들면 이후 실행에서 자동으로 재사용되고,
`--allow=nodekey:...`로 특정 클라이언트 공개키만 허용할 수 있다.
토큰을 DNS TXT 레코드로 공개하면
`tailcat ssh my-server.example.com`처럼 이름으로 접속할 수 있어
토큰을 외우지 않아도 된다.
Go 라이브러리로도 제공되어 `tailcat.Server`와 `tailcat.NewClient`로
직접 서버와 클라이언트를 짤 수 있다.

## 분석

### 이것이 파는 것은 Tailscale의 데이터 플레인이지 Tailscale이 아니다

이 프로젝트에서 가장 많은 혼란을 부른 지점이 이름이다.
HN에서 spockz는 전송이 WireGuard이고 제어 플레인이 새 구조라면
이게 도대체 얼마나 Tailscale이냐고 물었고[^spockz],
larnon도 이미 Tailscale을 쓰는데 이게 무엇을 더해 주는지 모르겠다고 했다[^larnon].
이 혼란은 Tailscale이라는 제품이 실제로 두 부분,
곧 데이터 플레인과 제어 플레인으로 나뉜다는 사실을 드러낸다.

Tailcat이 가져온 것은 데이터 플레인,
곧 WireGuard·DERP·Magicsock·netstack이라는 연결의 기계다.
버린 것은 제어 플레인,
곧 계정, 신원 관리, ACL, 코디네이션 서버다.
tptacek이 가장 명료하게 요약했다.
이것은 파일 전송에 국한된 Magic Wormhole을
일반적 연결로 확장한 것이라는 것이다[^tptacek].
그러면 larnon의 물음에 대한 답도 분명해진다.
Tailscale은 지속적 신원 기반 사설망을 주고,
Tailcat은 계정 없이 토큰 하나로 여는 일회성 연결을 준다.
같은 데이터 플레인을 공유하지만 겨누는 사용 사례가 다르다.

### 제어 플레인을 토큰으로 대체한 것이 핵심 설계다

Tailscale의 제어 플레인이 하던 일은
누가 누구에게 연결할 수 있는지를 중앙에서 관리하는 것이었다.
Tailcat은 이 중앙 조정을 없애고 그 역할을 토큰에 담는다.
토큰이 서버 공개키와 릴레이 정보를 자기 안에 지니므로,
연결에 필요한 모든 신원 교환이 대역 외에서 토큰 전달만으로 끝난다.
중앙 서버가 관찰하거나 통제할 지점이 사라지는 것이다.

이 설계가 낳는 성질이 흥미롭다.
토큰을 아는 사람만 연결할 수 있으므로 토큰이 곧 접근 권한이 되고,
일회성 키가 기본이라 토큰의 수명이 프로세스 수명과 같아진다.
이것은 신원을 지속적으로 관리하는 Tailscale의 모델과 정반대다.
Tailscale이 “누구인가”를 관리한다면,
Tailcat은 “이 토큰을 가졌는가”만 묻는다.
DNS TXT에 토큰을 올려 이름으로 접속하게 하는 기능은
이 토큰 기반 신원을 사람이 읽을 수 있는 주소로 끌어올린 것으로,
제어 플레인 없이도 안정적 주소를 흉내 낼 수 있게 한다.

### NAT 뒤의 두 머신을 잇는 오래된 문제의 최신 답이다

Tailcat이 푸는 근본 문제는 NAT 뒤에 있는 두 머신을
어떻게 직접 연결하느냐다.
HN에서 pbohun은 100% IPv6에 CGNAT이 없다면 애초에 필요 없을 도구지만,
현실에서는 이것이 차선책이라며
사소한 P2P가 가능해지면 얼마나 많은 혁신이 일어날지
사람들이 과소평가한다고 적었다[^pbohun].
cpuguy83도 Tailscale의 NAT 통과 블로그를 읽고 비슷한 걸 만들려다
기존 대안 때문에 접었다고 회고했다[^cpuguy83].

이 맥락이 Tailcat의 위치를 정한다.
홀펀칭과 DERP 폴백은 Tailscale이 수년간 다듬은 NAT 통과 기술이며,
Tailcat은 그 검증된 데이터 플레인을 계정 장벽 없이 개방한다.
GeekNews에서 @neo가 Iroh, dumbpipe, pai-sho 같은 유사 프로젝트를 언급하고[^neo],
HN에서 megamorf가 Iroh를 든 것은[^megamorf]
이 문제 공간에 이미 여러 답이 있음을 보여 준다.
Tailcat의 차별점은 새로운 기술이 아니라
가장 실전에서 검증된 데이터 플레인을 가장 낮은 진입 장벽으로 제공한다는 데 있다.

## 비평

### 릴레이 의존이 “제어 플레인 없음”이라는 약속을 흐린다

Tailcat은 제어 플레인이 없다고 내세우지만,
DERP 릴레이라는 제3자 인프라에 기댄다.
HN에서 1vuio0pswjnm7은 이 지점을 정확히 짚어,
피어가 제3자 랑데부·릴레이 서버를 쓰고 싶지 않을 수 있는데
정작 Tailscale은 자체 DERP 서버 운영을 권장하지 않으며
대부분의 사용자가 그럴 필요도 없다고 안내한다고 인용했다[^1vuio0pswjnm7].
그러면 기본 설정에서 Tailcat 사용자는
Tailscale이 운영하는 공개 DERP를 거치게 된다.

이 의존은 “탈중앙”이라는 인상과 충돌한다.
제어 플레인을 없앴다고 해도,
NAT를 뚫지 못하는 연결은 DERP를 데이터 경로로 계속 쓰므로
Tailscale의 인프라가 여전히 트래픽의 길목에 있다.
DERP는 내용을 볼 수 없도록 암호화되지만,
연결의 존재와 메타데이터는 릴레이를 지난다.
게다가 문서 스스로 밝히듯 공개 DERP는 속도 제한이 있고
가동 시간 보장이 없다.
그러면 이 도구의 “계정도 서버도 없이”라는 약속은
자체 DERP를 운영할 때만 온전하며,
그것은 대부분의 사용자가 하지 않을 일이다.
탈중앙의 외형과 중앙 릴레이 의존의 실질 사이에 간극이 있다.

### 이미 있던 방법들과의 차별점이 얇다

여러 참가자가 이것이 새롭지 않다고 지적했다.
petcat은 몇 년째 SSH 포워딩과 nginx 리버스 프록시로
같은 일을 손수 해 왔다고 적었고[^petcat],
archietect는 최근 출시된 bitbang-cli의 직접 경쟁자로 보인다고 했으며[^archietect],
Schlagbohrer는 10~15년 전 Tor의 어니언 주소로
집 서비스를 안전하게 노출하던 방식을 떠올렸다[^Schlagbohrer].
Magic Wormhole, Iroh, dumbpipe까지 더하면
이 문제 공간은 이미 붐빈다.

이 붐빔이 Tailcat의 실질적 기여를 묻게 만든다.
데이터 플레인의 품질이 앞선다는 것은 강점이지만,
사용자 대부분에게는 SSH 터널이나 Wormhole로 충분하다.
cpuguy83이 비슷한 걸 만들려다 대안 때문에 접은 것도 같은 이유다.
그러면 Tailcat의 가치는 기술의 새로움이 아니라
Tailscale이라는 이름이 주는 신뢰와 완성도에 있는데,
그 신뢰가 정작 이름의 혼란(제어 플레인 없는 Tailscale이 Tailscale인가)으로
반쯤 상쇄된다.
가장 좋은 데이터 플레인이라는 강점과
이미 흔한 문제라는 약점이 팽팽하다.

### 엔드포인트 인증과 공유의 부재가 실사용을 제한한다

토큰 기반 접근은 단순하지만 거칠다.
HN에서 gsallesl은 두 가지 핵심 기능이 빠졌다고 짚었다.
엔드포인트에서의 선택적 애플리케이션 사용자 인증과
계정 간 접근 공유다[^gsallesl].
토큰을 가진 사람이면 누구나 연결되고,
그 접근을 세분화하거나 여러 사람과 안전하게 나눌 방법이 없다.

이 한계는 Tailcat이 개인용 일회성 도구에 머무는 이유를 설명한다.
`--allow`로 클라이언트 공개키를 제한할 수는 있지만,
그것은 팀 단위의 권한 관리와 거리가 멀다.
제어 플레인을 없앤 대가가 여기서 드러난다.
중앙 신원 관리가 사라지면 세밀한 권한과 공유도 함께 사라진다.
gsallesl의 팀이 이런 기능을 처음부터 다시 구현했다는 것은,
Tailcat이 비운 자리가 실무에서는 다시 채워져야 하는 자리임을 보여 준다.
그러면 Tailcat은 완성된 해법이 아니라
데이터 플레인이라는 재료이며,
진짜 제품은 그 위에 인증과 공유를 얹은 무언가다.

## 인사이트

### 이 도구의 진짜 폭로는 Tailscale의 가치가 제어 플레인에 있다는 것이다

Tailcat을 둘러싼 “이게 얼마나 Tailscale이냐”는 반복된 혼란은
사소한 명명 문제가 아니라 깊은 것을 드러낸다.
데이터 플레인만 떼어 내 무료로 개방했더니
사용자들이 그것을 Tailscale로 인식하지 못했다는 사실은,
Tailscale이라는 제품의 실제 가치가
WireGuard 터널이 아니라 그 위의 제어 플레인,
곧 신원, ACL, 조정, 관리 경험에 있었음을 역설적으로 증명한다.

이 폭로는 오픈코어 사업 모델의 논리를 그대로 보여 준다.
Tailscale이 데이터 플레인을 오픈소스로 개방할 수 있는 것은
그것이 팔리는 물건이 아니기 때문이다.
진짜 상품인 제어 플레인은 여전히 닫혀 있다.
Tailcat은 그 개방된 절반을 극한까지 활용한 데모이면서,
동시에 나머지 절반이 왜 상품인지를 증언한다.
larnon이 “이게 Tailscale에 뭘 더해 주냐”고 물었을 때,
정답은 “아무것도, 오히려 뺀다”이다.
그리고 그 뺀 것이 바로 사람들이 Tailscale에 돈을 내는 이유다.

### 사소한 P2P의 개방은 Tor가 놓친 자리를 채운다

Schlagbohrer가 떠올린 Tor 어니언 서비스는
10~15년 전 집의 서비스를 안전하게 노출하는 표준 방법이었다.
그러나 Tor는 익명성에 최적화되어 느리고 복잡했으며,
지금은 관련 소식조차 드물다.
Tailcat이 여는 자리는 정확히 Tor가 잘 채우지 못한 곳이다.
익명성이 아니라 연결성,
느린 다중 홉이 아니라 직접 P2P를 원하는 사용 사례다.

이 대비가 P2P 도구의 세대 교체를 보여 준다.
Tor는 감시 회피를 위해 성능을 희생했지만,
Tailcat과 그 형제들(Iroh, Wormhole)은 성능을 위해 익명성을 포기한다.
pbohun이 말한 “사소한 P2P가 가능해지면 일어날 혁신”은
바로 이 성능 우선 P2P의 대중화를 가리킨다.
bradfitz가 소개한 Minecraft 모드처럼[^bradfitz],
연결이 토큰 하나로 사소해지면
사람들은 그 위에 예상 못 한 것들을 짓기 시작한다.
NAT 통과가 라이브러리 호출로 떨어지는 순간,
집의 두 기기를 잇는 일이 특별한 설정에서 기본 도구로 바뀐다.

### 데이터 플레인의 개방은 실험을 폭발시키지만 인프라 부담을 남긴다

Tailcat의 가장 큰 2차 효과는 실험의 폭발이다.
계정과 설정이라는 장벽이 사라지면
사람들이 즉흥적으로 무언가를 연결해 본다.
bradfitz의 동료가 하루 만에 Minecraft 모드를 만든 것,
@neo가 그 데모를 공유한 것,
aseipp가 Iroh로 짜던 것을 Tailcat으로 다시 설계하겠다고 한 것이
모두 이 낮은 진입 장벽이 부르는 즉흥의 사례다.
토큰 하나로 연결이 시작되면 실험의 비용이 거의 0이 된다.

그러나 이 실험의 폭발에는 숨은 청구서가 있다.
그 모든 즉흥적 연결이 기본적으로 Tailscale의 공개 DERP를 거친다는 것이다.
개방이 사용을 늘릴수록 릴레이 부하가 늘고,
그 부담은 인프라를 운영하는 한 회사에 집중된다.
이것은 앞서 다룬 무료 인프라의 공공재 딜레마와 같은 구조다.
Tailscale이 데이터 플레인을 개방한 것은 관대함이자 마케팅이지만,
그 개방이 성공할수록 공개 DERP의 비용은 오른다.
그러면 Tailcat의 지속 가능성은
사용자가 자체 DERP를 얼마나 운영하는가에 달려 있는데,
문서 스스로 그것을 권하지 않는다는 데 긴장이 있다.
개방의 이상과 중앙 릴레이의 현실이 여기서 다시 만난다.

---

[^spockz]: <https://news.ycombinator.com/item?id=49456173>
[^larnon]: <https://news.ycombinator.com/item?id=49465425>
[^tptacek]: <https://news.ycombinator.com/item?id=49454214>
[^pbohun]: <https://news.ycombinator.com/item?id=49455132>
[^cpuguy83]: <https://news.ycombinator.com/item?id=49453165>
[^neo]: <https://news.hada.io/topic?id=32920#cid64219>
[^megamorf]: <https://news.ycombinator.com/item?id=49454070>
[^1vuio0pswjnm7]: <https://news.ycombinator.com/item?id=49466638>
[^petcat]: <https://news.ycombinator.com/item?id=49453540>
[^archietect]: <https://news.ycombinator.com/item?id=49453841>
[^Schlagbohrer]: <https://news.ycombinator.com/item?id=49461589>
[^gsallesl]: <https://news.ycombinator.com/item?id=49463085>
[^bradfitz]: <https://news.ycombinator.com/item?id=49455269>
