# N100 미니 PC 한 대로 서비스 28개를 돌리는 셀프호스팅

원문: [What I Self-Host | Clever Blog Title](https://viceconsole.fyi/blog/2026/10/10/what-i-self-host/)

HN 토론: <https://news.ycombinator.com/item?id=50091061> (2점, 0개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/j4tlzg/what_i_self_host> (57점, 38개 댓글)

GN 토론: <https://news.hada.io/topic?id=35376>

## 요약

viceconsole.fyi의 저자는 대학 시절 침대 밑 리눅스 컴퓨터로 웹사이트를 돌리고,
MythTV와 XBMC(지금의 Kodi)를 오래 운영한 사람이다.
인도에서 몇 년 사는 동안 Netflix, Disney Plus(Hotstar),
Spotify를 싸게 썼지만, 인도를 떠난 뒤에는 서구 가격을 낼 생각이 없었다.
더 큰 이유는 아들에게 쏟아지는 “recommended for you”와
“up next” 같은 참여 유도 장치였다.
서비스마다 자동 재생을 끄고 클라이언트 변경을 추적하는 일이 너무 번거로워,
저자는 스트리밍 구독을 끊고 Jellyfin으로 옮겼다.
그 뒤 1년 반 동안 Jellyfin이 다른 서비스로 가는 문이 되었고,
저자는 불필요한 재디자인과 약관 변경 메일에서
벗어난 “반가운 안정감”을 얻었다고 쓴다.

저자에게는 몇 가지 원칙이 있다.
첫째, 라우터의 VPN 서버를 제외하면 어떤 서비스도 공용 인터넷에 직접 노출하지 않는다.
AI 보조 해킹이 늘어난 지금은 더더욱 현명하지 않다고 본다.
ISP가 IPv4에 CGNAT를 쓰기 때문에 VPN은 IPv6로만 접근할 수 있고,
그래서 IPv6를 거의 주지 않는 공용 Wi-Fi에서는
VPN이 잘 붙지 않는다는 단점도 감수한다.
둘째, 가능하면 네이티브로 실행하고 의존성이 복잡한 서비스만 컨테이너로 돌린다.
단일 Go 바이너리는 환영하지만,
MySQL과 Redis와 컨테이너 세 개를 더 요구하는
Docker compose 파일만 제공하는 서비스라면 대안부터 찾는다.
셋째, Docker는 더 쓰지 않는다.
원칙이라기보다 별도의 서비스 관리 체계를 하나 더 다루는 데 지쳤기 때문이고,
이미 쓰고 있는 systemd와 Podman의 통합이 훌륭하다는 이유다.

하드웨어는 Beelink S12 Pro 미니 PC 한 대다.
Intel N100, 16GB RAM,
512GB SSD 구성을 램 가격 폭등(“rampocalypse”) 전에 180유로에 샀고,
같은 Amazon 상품은 지금 359유로다.
미디어 저장용으로 6TB 하드 디스크를 붙였다.
이 글은 저자가 Hacker News에 남긴 셀프호스팅 목록 댓글에
“16GB로 이걸 다 어떻게 돌리느냐”는 질문이 달린 데서 출발했다.

본문은 서비스 목록을 알파벳순으로 소개하고,
각각이 네이티브인지 Podman인지 적는다.
Actual Budget(가계부), Audiobookshelf, Automatic Ripping Machine(DVD 리핑),
Backrest(Restic 백업 UI), Beszel, Caddy(리버스 프록시와 LetsEncrypt 인증서),
Cockpit, Forgejo, FreshRSS, Frigate(IP 카메라 8대의 NVR), Gonic, Gotify,
Home Assistant, Homepage, Immich, Jellyfin, MPD, PocketBase, Readeck, Samba,
slskd, Snapcast, Syncthing, Transmission,
Uptime Kuma, Vaultwarden, Vikunja, Yubal이다.
선택 기준은 일관된다.
Vikunja를 고른 이유는 두 명이 쓸 서비스에 PostgreSQL이나 MySQL을
띄우고 싶지 않아서이고, SQLite를 기본으로 쓰기 때문이다.
자원을 아끼는 장치도 곳곳에 있다.
미디어는 1080p보다 720p를 선호하고,
카메라는 지원 해상도보다 낮게 돌리며 Frigate는
저해상도 RTSP 서브스트림으로 움직임을 감지한다.

반대로 하지 않는 것도 적는다.
Sonarr, Radarr 같은 *arr 스택은 자원을 많이 먹고 자주 깨질 것 같아 피한다.
Collabora Online은 공유 네트워크 드라이브와
로컬 LibreOffice가 있으니 필요 없다고 본다.
Firefly III는
데이터 가져오기 전용 컨테이너까지 필요한 복잡한 구성이라 Actual Budget으로 갔다.
Dawarich는 컨테이너를 “최소” 네 개 요구해서,
Music Assistant는 모든 것을 “소유”하려 들어서 접었다.
이메일은 주고받지 못할 위험을 감수할 수 없어 직접 호스팅하지 않는다.
결론은 네이티브 17개, Podman 11개,
모두 systemd가 관리하며 htop 기준 메모리 약 7.5GB, CPU 30~40%라는 숫자다.
저자는 AI 수요로 하드웨어가 비싸진 지금,
단순함과 효율을 우선하는 셀프호스팅 프로젝트가
계속 나오기를 바란다며 글을 맺는다.

## 분석

### 셀프호스팅의 동기는 비용보다 통제권이다

글의 출발점은 구독료지만, 실제 논지는 돈이 아니다.
저자가 Jellyfin에서 얻었다고 꼽는 것은 자동 재생이 없고,
추천이 보이지 않고, 쓰레기 같은 목록을 스크롤하지 않아도 된다는 점이다.
업그레이드도 릴리스 노트를 읽고 언제 할지 스스로 정한다.
즉 저자가 되찾으려는 것은 변경의 주도권이다.

이 점은 서비스 하나하나의 도입 사연에서도 반복된다.
Immich는 Google이 유료 저장 공간을 계속 권하는 데 지쳐서,
Vikunja는 Trello의 며칠짜리 장애 뒤에,
Vaultwarden은 LastPass의 침해 사고 때문에 들였다.
각각은 클라우드 서비스가 사용자의 동의 없이 상태를 바꾼 사건에 대한 반응이다.
셀프호스팅을 “싸게 쓰기”로 읽으면 이 글의 절반을 놓친다.

### 자원 효율은 하드웨어가 아니라 선택에서 나온다

16GB에 28개라는 숫자는 하드웨어 자랑처럼 보이지만,
글이 실제로 보여 주는 것은 선택의 누적이다.
의존성이 많은 서비스를 배제하고, SQLite 기반을 고르고,
720p와 저해상도 서브스트림으로 처리량을 줄였다.
이 기준을 지키면 서비스 수가 늘어도 메모리는 대부분 비어 있다.

저자가 Docker compose 하나로 여러 컨테이너를 요구하는
프로젝트를 피하는 이유도 결국 같은 축 위에 있다.
컨테이너 수는 메모리뿐 아니라 운영자의 머릿속 부담이기도 하다.
어떤 컨테이너에는 `curl`이 없고, 어떤 컨테이너는 busybox라 인자가 다르며,
가상 네트워크와 포트 매핑을 따로 기억해야 한다.
저자가 네이티브 실행을 고르는 근거는 성능보다 이 인지 부하를 줄이는 데 있다.

### 노출하지 않는다는 원칙이 아키텍처 전체를 결정한다

공용 인터넷에 서비스를 내놓지 않는다는 규칙은
단순해 보이지만 많은 결정을 끌고 다닌다.
Caddy와 개인 도메인은 외부 공개용이 아니라 LAN 안에서
HTTPS와 서브도메인을 쓰기 위한 것이다.
Vaultwarden 동기화는 LAN에 있을 때 자동으로 되고,
밖에서는 VPN을 켜고 수동으로 맞춘다.
Audiobookshelf 대신 바깥에서 팟캐스트를 들을 수단도 VPN 연결 여부에 달려 있다.

이 원칙의 대가는 접근성이다.
CGNAT 환경에서 IPv6로만 VPN을 열었기 때문에 공용 Wi-Fi에서는 거의 쓸 수 없고,
휴대폰 데이터로 바꿔야 한다.
저자는 이 불편을 “내 용도에는 괜찮다”는 판단으로 받아들였고,
그 판단이 가족 단위 사용을 전제로 한다는 점은 비평에서 다시 볼 대목이다.

## 비평

### 28개 서비스는 한 대의 단일 장애점 위에 있다

저자는 Home Assistant를 다루며 서버 장애가 집의 기능을
해치지 않게 할 “현실적인 방법”을 고민해야 한다고 스스로 적는다.
그러나 글 전체에서 이 문제는 그 한 문장 이상으로 다뤄지지 않는다.
비밀번호 관리자, 사진 원본, 가계부, 카메라 녹화,
홈 자동화가 모두 N100 한 대와 6TB 디스크 하나에 모여 있다.
Backrest와 Syncthing으로 백업은 하지만, 백업은 복구 시간을 보장하지 않는다.

이 구조에서 하드웨어 고장은 단순한 다운타임이 아니다.
아내가 비밀번호를 열지 못하고, 마당 조명 자동화가 멈추고, 카메라 녹화가 끊긴다.
클라우드의 변덕에서 벗어나려던 선택이 가정의 핵심 기능을
한 장비의 수명에 묶는 결과가 된 셈이다.
글이 “28개도 돌아간다”는 용량의 문제에 답했다면,
“28개가 동시에 멈추면 어떻게 하느냐”는 내구성의 문제는 남겨 두었다.

### 감시 장치가 감시 대상과 같은 장비에 있다

Uptime Kuma는 아내가 “X가 안 된다”고 말하는 일을 줄이려고 들였다.
그런데 Uptime Kuma와 알림을 보내는 Gotify가
감시 대상 서비스와 같은 미니 PC에서 돈다.
디스크가 가득 차거나 전원이 나가면 감시 장치도 함께 죽고, 알림은 오지 않는다.

Lobste.rs에서 가장 점수가 높은 축의 논의가 정확히 이 지점이었다.
markerz는 서비스를 일부러든 실수로든 자주 내리는데 디스크가 차거나
전원이 끊기면 어떻게 되느냐며, 모니터링만큼은 셀프호스팅하지 않는다고 썼다.[^markerz]
ggpsv는 모니터링 도구를 다른 지역,
다른 공급자의 작은 VPS에서 따로 돌리면
앞의 상황을 모두 잡을 수 있다고 답했다.[^ggpsv]
tuxes는 셀프호스팅한 Uptime Kuma가 healthchecks.io 같은 외부 데드맨 스위치를
주기적으로 찌르게 하면,
감시 장치 자체가 죽었을 때도 알림을 받는다는 흔한 패턴을 소개했다.[^tuxes]
strugee는 자기 단체와 자원봉사자가 서로의 Uptime Kuma를 한쪽으로만
감시하고 있었다며,
1차 시스템이 충분히 안정적이면
이중화 장치는 몇 달씩 아무도 모르게
고장 나 있을 수 있다는 점을 이 토론에서 깨달았다고 적었다.[^strugee]
반면 noirscape는 매시간 도는 cron 작업이 성공할 때마다 Uptime Kuma에
POST를 보내고,
90분 동안 신호가 없으면 알림을 받는 식으로
같은 장비 안의 조용한 실패를
잡는 데는 셀프호스팅 Uptime Kuma가 쓸모 있다고 짚었다.[^noirscape]
즉 같은 장비의 Uptime Kuma는 서비스 단위 장애를 잡는 도구이지
장비 단위 장애를 잡는 도구가 아니며, 저자의 글은 이 경계를 구분하지 않는다.

### 노출하지 않는다는 원칙은 가족 공유에서 시험대에 오른다

저자는 Immich에서 가족과 앨범을 공유하는 해법을 찾았다고 한 문장으로만 쓴다.
하지만 서비스를 외부에 노출하지 않는다는 원칙과
집 밖의 가족에게 사진을 보여 주는 일은 정면으로 부딪힌다.
Hacker News에서 bschwindHN은 바로 이 부분을 물었다.
저자의 원래 댓글에 달린 답글에서 그는 자신도 인터넷에 서비스를 노출하지 않는
비슷한 구성을 꾸리고 있다며,
LAN 밖 가족과 Immich 앨범을 어떻게 공유하는지 물었다.[^bschwindHN]
글에서 가장 어려운 문제가 가장 짧게 처리된 셈이다.

VPN 쪽도 같은 긴장을 보인다.
저자는 Hacker News 답글에서 WireGuard를 먼저 설정했지만 통신사 필터링 때문에
휴대폰 데이터 연결에서는 동작하지 않아 OpenVPN도
함께 운영한다고 설명했다.[^viceconsole-vpn]
기술에 익숙한 운영자는 이런 우회를 감수하지만,
가족 구성원은 “VPN을 켜고 Wi-Fi를 끄라”는 지시를 매번 따르기 어렵다.
노출하지 않는 원칙의 비용은 운영자가 아니라
같은 서비스를 쓰는 다른 가족에게 더 크게 돌아간다.

### 단순함의 기준은 운영자 개인의 숙련도에 기대고 있다

저자는 *arr 스택을 자원을 많이 먹고 자주 깨지는 엉망이라고 단정하지만,
직접 써 본 경험이 아니라 설정 방법을 읽은 인상에 근거한다.
반대로 Snapcast는 설정이 복잡하다고 인정하면서도 잘 동작하니 남겨 두었다.
즉 “단순함”은 객관적 기준이라기보다
저자가 이미 익숙한 도구와 낯선 도구를 가르는 말로도 쓰인다.

“네이티브가 더 낫다”는 주장도 마찬가지다.
17개 서비스를 네이티브로 운영하려면 각 서비스의 업그레이드 경로,
사용자 계정, 파일 권한을 운영자가 직접 관리해야 한다.
저자에게는 systemd와 Podman quadlet이 하나의 관리 체계로 보이지만,
그 통일감은 리눅스 서버를 20년 넘게 다룬 사람에게 주어지는 것이다.
이 글을 처음 셀프호스팅을 시작하는 독자가 그대로 따라 하면
단순함보다 관리 표면이 먼저 늘어날 가능성이 크다.

## 인사이트

### 셀프호스팅의 진짜 비용은 다른 사람이 쓰기 시작할 때 생긴다

이 글의 서비스 목록은 대부분 아내와 아이들 때문에 생겼다.
Vaultwarden은 아내의 LastPass 때문에, Uptime Kuma는 아내의 “X가 안 된다” 때문에,
Gonic 두 인스턴스는 아이용과 어른용 음악을 나누려고 들였다.
혼자 쓰는 셀프호스팅은 취미지만,
가족이 쓰기 시작하면 그것은 작은 운영 조직이 된다.

이때 운영자는 고객 지원, 장애 대응, 접근 권한 관리를 모두 떠안는다.
글에 등장하는 모니터링, 알림, 대시보드 같은 도구들은 이 역할 변화의 흔적이다.
셀프호스팅 규모를 가늠할 때는 서비스 수나 메모리보다
“나 말고 몇 명이 이것에 기대는가”를 먼저 세는 편이 현실적이다.

### 메모리 가격이 오르면 소프트웨어의 단순함이 다시 가치가 된다

저자는 같은 미니 PC가 1년 사이 180유로에서 359유로가 되었다고 적는다.
하드웨어가 싸던 시절에는 컨테이너 다섯 개를
요구하는 서비스도 큰 문제가 아니었다.
그러나 램과 저장 장치가 다시 비싸지면,
SQLite 하나와 단일 바이너리로 끝나는 프로젝트가 경쟁력을 얻는다.

이는 2000년대 초 저사양 VPS 시절 lighttpd나 SQLite가 각광받던 흐름과 닮았다.
자원이 귀할 때 소프트웨어는 가벼워지는 쪽으로 선택받는다.
Lobste.rs의 hackguy는 기업이 폐기한 중고 장비를 권하며, i5-9500T와 32GB DDR4를 갖춘 Lenovo M720q를 배송비 포함 270유로에 샀다고 썼다.[^hackguy]
하드웨어 쪽 대안은 중고 시장이고,
소프트웨어 쪽 대안은 저자가 바라는 효율 우선 프로젝트다.

### 자립을 원하면 결국 다른 사람과의 연결이 필요하다

셀프호스팅은 기업 의존을 줄이는 선택이지만,
감시와 백업은 본질적으로 다른 장소를 요구한다.
Lobste.rs의 technomancy는 셀프호스터끼리 서로의 백업과 모니터링을 맡아 주는 상호 교환을 오래 구상해 왔다고 썼다.[^technomancy]
bjeanes는 친구와 각자의 NAS에 상대 전용 사용자와 공유 폴더를 두고,
둘 사이를 전용 ZeroTier 네트워크로 연결해
실제로 이렇게 하고 있다고 답했다.[^bjeanes]
B2가 싸니 6TB 이상이 아니면 경제적으로 맞지 않는다는 atmosx의 반론에,
technomancy는 돈이 아니라 상호 부조와
호혜의 원칙이라고 응수했다.[^technomancy-aid]

이 토론은 셀프호스팅의 다음 단계를 보여 준다.
클라우드 기업에서 벗어난 개인이 다시 마주하는 문제는 지리적 분산이고,
그 해법은 기업이 아니라 신뢰하는 개인 간의 네트워크다.
1990년대 BBS와 미러 서버 문화가 그랬듯,
자립적인 인프라는 결국 작은 공동체 단위로 묶일 때 내구성을 얻는다.

### VPN 계층은 셀프호스팅에서 가장 버리기 어려운 외부 의존이다

저자는 라우터에서 WireGuard와 OpenVPN을
직접 운영하며 Tailscale을 언급하지 않는다.
Lobste.rs의 baetylboy는 자신의 셀프호스팅 구성이 MagicDNS와 서비스 이름 덕분에 Tailscale에 깊이 얽혀 있다며, 이 글에 언급조차 없는 것이 놀랍다고 썼다.[^baetylboy]
msangi는 반대로 Tailscale에서 순수 WireGuard로 옮겼다며,
Tailscale에서 대체하기 어려운 것은 NAT 통과뿐이었고 IPv6 노출과
VPS 중계로 해결했지만 더 많은 고민과 설정이 필요했다고 적었다.[^msangi]

저자의 CGNAT와 IPv6 전용 VPN 문제는 정확히 이 NAT 통과의 비용이다.
Tailscale을 쓰면 공용 Wi-Fi 문제는 대부분 사라지지만,
그 대신 셀프호스팅 전체가 한 기업의 조정 서버에 기대게 된다.
결국 셀프호스팅은 모든 의존을 없애는 일이 아니라
어떤 의존을 남길지 고르는 일이며,
접근 계층은 그 선택이 가장 날카롭게 드러나는 곳이다.

### 컨테이너를 줄이는 것은 성능보다 안정성의 문제다

저자는 Docker를 떠난 이유를 별도 관리 체계의 피로라고만 설명한다.
Lobste.rs의 alexozer는 NAS에 컨테이너 없이 systemd 서비스만 쓰는 정책을 들인 뒤 안정성이 크게 좋아졌고, 매일 밤 자동 재부팅으로 일시적 상태 문제도 정리한다고 썼다.[^alexozer]
Hacker News에서 저자는 서비스의 절반가량은 네이티브로,
나머지는 systemd quadlet 형태의 Podman으로 돌리며
메모리 문제는 겪어 보지 않았다고 답했다.[^viceconsole-mem]
같은 스레드에서 koyote는 비슷한 수의 서비스를 16GB NUC의 Proxmox LXC로 돌려도
메모리 사용량이 대개 절반 아래라며,
메모리를 크게 먹는 것은 Unifi 네트워크 컨트롤러 같은
독점 소프트웨어라고 지적했다.[^koyote]

이 반응들을 모으면 16GB가 넉넉한 이유는
컨테이너냐 네이티브냐보다 어떤 소프트웨어를 고르느냐에 있다.
네이티브 실행의 실질적 이점은 메모리 절약보다
상태가 한 곳에서 관리되어 장애 원인을 추적하기 쉽다는 데 있다.
셀프호스팅 규모가 커질수록 성능을 최적화한 구성보다
장애가 났을 때 무엇을 봐야 하는지 분명한 구성이 오래간다.

---

[^markerz]: <https://lobste.rs/s/j4tlzg/what_i_self_host#c_cp3qn5>

[^ggpsv]: <https://lobste.rs/s/j4tlzg/what_i_self_host#c_5eh8dc>

[^tuxes]: <https://lobste.rs/s/j4tlzg/what_i_self_host#c_qoxd27>

[^strugee]: <https://lobste.rs/s/j4tlzg/what_i_self_host#c_xb8q3x>

[^noirscape]: <https://lobste.rs/s/j4tlzg/what_i_self_host#c_bsnohb>

[^bschwindHN]: <https://news.ycombinator.com/item?id=50097778>

[^viceconsole-vpn]: <https://news.ycombinator.com/item?id=50017194>

[^hackguy]: <https://lobste.rs/s/j4tlzg/what_i_self_host#c_eotmzv>

[^technomancy]: <https://lobste.rs/s/j4tlzg/what_i_self_host#c_b9pe8g>

[^bjeanes]: <https://lobste.rs/s/j4tlzg/what_i_self_host#c_j17n8f>

[^technomancy-aid]: <https://lobste.rs/s/j4tlzg/what_i_self_host#c_kupq0o>

[^baetylboy]: <https://lobste.rs/s/j4tlzg/what_i_self_host#c_2xittw>

[^msangi]: <https://lobste.rs/s/j4tlzg/what_i_self_host#c_lnaesh>

[^alexozer]: <https://lobste.rs/s/j4tlzg/what_i_self_host#c_ayza74>

[^viceconsole-mem]: <https://news.ycombinator.com/item?id=50017170>

[^koyote]: <https://news.ycombinator.com/item?id=50015869>
