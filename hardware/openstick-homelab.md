# 10달러 OpenStick 홈랩: 메모리 450MB 안에 모니터링과 AI 에이전트까지 올리기

원문: [What I run on my $10 USD OpenStick homelab | Bosscher](https://blog.bosscher.ch/posts/openstick/)

HN 토론: <https://news.ycombinator.com/item?id=50406670> (696점, 125개 댓글)

GN 토론: <https://news.hada.io/topic?id=36776>

## 소개

Laurens Bosscher가 2026년 11월 7일에 쓴 글이다.
배송비를 포함해 10달러를 주고 충동적으로 산 OpenStick에서 지금 돌리는 소프트웨어를
소개한다.
OpenStick은 4G 모뎀이 달린 작은 USB 동글 형태의 장치로,
글쓴이가 적은 사양은 다음과 같다.

- 메모리 512MB(실제 사용 가능한 양은 약 450MB)
- 1GHz ARM Cortex-A53 코어 4개
- eMMC 플래시 4GB
- 150Mbit/s Wi-Fi, 4G 모뎀, GPS
- 방열판 없이 소음이 없는 수동 냉각, 프로그래밍할 수 있는 LED 하나

설치 과정은 번거롭지만 한 번 올리면 Debian이 돌아가고,
systemd와 Podman으로 컨테이너를 쓸 수 있어서 소음 없고 전력이 적게 드는 홈
서버가 된다고 한다.
글쓴이는 이것이 자체 호스팅을 시작하기에 좋은 장치라고 주장하고,
HN에서도 요즘 메모리가 비싸서 다른 사람들에게 시작점이 될 것 같다고 썼다.[^author]
이 문서는 장치와 소프트웨어를 직접 실행해 보지 않았고, 글에 적힌 구성과 수치를
정리했다.

## 올려 둔 소프트웨어

글이 소개하는 소프트웨어와 글쓴이가 적은 메모리 사용량은 다음과 같다.
수치는 글쓴이의 보고이며 이 문서가 측정한 값이 아니다.

| 소프트웨어          | 메모리    | 하는 일                                                          |
| ------------------- | --------- | ---------------------------------------------------------------- |
| CastSponsorSkip     | 5~10MB    | Google Cast 기기에 연결해 유튜브의 스폰서 구간을 건너뛴다        |
| AdGuard Home (포크) | 40MB      | DNS 수준 광고와 악성 도메인 차단, 큰 차단 목록을 효율적으로 처리 |
| Zeroclaw            | 64MB      | AI 에이전트 하니스, Telegram 등 30개 채널 지원                   |
| Cloudflare Tunnel   | 8~20MB    | 포트를 열지 않고 서비스를 인터넷에 노출한다                      |
| Beszel              | 20MB      | CPU와 메모리 그래프와 경보                                       |
| Dozzle              | 글에 없음 | Podman 컨테이너 로그를 보는 화면                                 |
| Gatus               | 10MB      | 웹 서버와 데이터베이스 같은 서비스의 상태 감시                   |
| Fusion              | 22MB      | RSS 리더                                                         |
| Shiori              | 10~20MB   | 북마크 관리와 페이지 자동 보관                                   |
| Diun                | 9MB       | 컨테이너 업데이트를 Telegram으로 알린다                          |

AdGuard Home은 글쓴이가 큰 차단 목록을 효율적으로 처리하도록 고친 포크를 쓴다.
공식 버전은 작은(20만 항목) 차단 목록이면 40MB로 충분하다고 글이 적는다.
글쓴이는 차단 목록을 몇 개 추가한 뒤 질의의 60%가 차단된다고 쓴다.

Zeroclaw를 쓰는 이유도 메모리다.
글쓴이는 쿠버네티스 클러스터에서 OpenClaw를 돌렸지만 1GB 넘게 쓰고
업데이트마다 깨졌으며 기능이 바뀌어 기존 작업 흐름이 깨졌다고 한다.
Zeroclaw는 유휴 시 약 3MB RSS를 쓰고 필요한 기능을 덮는다고 평가한다.
Picoclaw와 Nullclaw도 살펴봤지만 문서와 커뮤니티가 가장 활발해 보여 Zeroclaw를
골랐다고 한다.
Beszel과 Dozzle은 기능이 겹치므로 10~20MB를 아껴야 하면 하나를 버리겠다고 쓴다.

## 비평

### 루트 셸을 에이전트에 주는 판단은 설명보다 위험하다

글쓴이는 Zeroclaw에 OpenStick 접근만 허용했고, 사실상 루트 셸이지만 영향 범위가
제한되어 있으니 받아들일 만하다고 쓴다.
HN에서 mk_stjames는 이 문장이 이해되지 않는다고 했다.
이 장치는 항상 켜져 있고 네트워크에 접근하며 로그를 모두 읽는데,
LLM에게 셸을 주는 것이 곧 그 접근을 주는 것 아니냐는 지적이다.[^mk-stjames]
영향 범위가 이 장치로 한정된다는 가정은 이 장치가 같은 네트워크의 다른 기기를
볼 수 있는 한 성립하지 않을 수 있다.
글은 이 장치의 네트워크 경계, 에이전트가 쓸 수 있는 명령, 사람이 승인하는 단계를
설명하지 않는다.
글쓴이는 HN에서 Zeroclaw의 기본 보안 설정이 매우 제한적이고 모두 푸는
YOLO 모드가 있으니 문서를 읽고 맞는 것만 켜라고 답했다.[^author-zeroclaw]
이는 설정 가능성이지 현재 설정이 어떤지에 대한 설명은 아니다.

### 터널은 편리하지만 신뢰를 중개자에게 넘긴다

글쓴이는 Cloudflare Tunnel로 포트를 열지 않고 서비스를 노출하면서
NSA가 모든 것을 읽을 수 있을지도 모르지만 홈랩에서는 받아들일 만한 거래라고
쓴다.
HN에서 hikemu는 NSA가 볼 수 있다는 것은 받아들일 수 없는 거래라고 반박했고,
글쓴이는 동의하지만 완전히 감사할 수 있는 스택은 매우 어렵고 어느 정도의 타협은
불가피하며 Cloudflare는 많이 타협한다고 답했다.[^hikemu][^author-trade]
이 장치에서 노출하는 서비스가 RSS와 북마크라면 노출되는 정보는 취향과 기록이다.
그런데 같은 장치에 루트 셸을 가진 에이전트와 로그와 모니터링이 함께 있다.
무엇이 터널 뒤에 있는지에 따라 위험의 크기가 크게 다르며, 글은 터널로 노출되는
서비스 목록을 밝히지 않는다.

### 자동 업데이트와 알림 사이에서 공급망 위험이 갈린다

글쓴이는 Diun으로 컨테이너 업데이트가 생기면 Telegram으로 알림을 받는다.
HN에서 suprjami는 Podman 자동 업데이트로 새 이미지를 받아 컨테이너를 재시작하게
하며 거의 모든 자체 호스팅 환경이 자동으로 업데이트된다고 썼다.
이에 peddling-brink는 공급망 침해는 어떻게 하느냐고 되물었다.[^suprjami][^peddling-brink]
알림만 받고 사람이 올리는 쪽은 느리지만 침해된 이미지가 자동으로 실행되는 일을
막는다.
글은 이 선택의 이유를 말하지 않는다.
글쓴이가 자기 AdGuard 포크를 바이너리로 올린 점도 공급망 문제의 일부다.
글쓴이는 믿지 말고 공식 버전을 쓰라는 안내를 달고 있고,
HN에서 rustyhancock이 소스를 달라고 하자 글쓴이는 저장소 링크를
올렸다.[^rustyhancock][^author-fork]
이는 좋은 대응이다.

### 장치를 구하기가 글보다 어렵다

글은 장치를 구하는 방법과 설치 절차를 자세히 말하지 않는다.
HN에서 dataflow가 어디서 사는지 묻자 글쓴이는 AliExpress에서 샀으며
판매자가 정확한 SoC를 표기하지 않는 경우가 많아 도박에 가깝지만
최악의 경우 예비 4G 동글이 생기는 정도라고 답했다.[^dataflow][^author-buy]
글의 10달러는 글쓴이가 낸 가격이며, 같은 이름으로 팔리는 변형이 판매자마다
다를 수 있다는 뜻이기도 하다.
설치가 번거롭다는 글의 한 줄은 이 글을 따라 하려는 사람에게 가장 큰 미지수다.

## 도입 전에 따져볼 것

- 필요한 서비스의 합이 450MB 안에 들어오는가. 표의 값을 더하면 Dozzle을 제외하고 약 190~215MB이며, 컨테이너 런타임과 운영체제의 몫은 별도다.
- 에이전트에게 줄 권한과 장치의 네트워크 위치를 먼저 정한다. 같은 네트워크의 다른 기기를 볼 수 있다면 영향 범위는 이 장치만이 아니다.
- 터널 뒤에 놓을 서비스를 적어 둔다. 모니터링 화면과 로그를 노출하지 않는 것이 안전하다.
- 업데이트는 알림과 자동 적용 중 무엇으로 할지 정한다. 자동 적용은 편하지만 공급망 침해를 그대로 받는다.
- 백업은 글쓴이가 HN에서 밝힌 방식, 곧 restic으로 매일 밤 Backblaze에 올리는 것을 참고할 수 있다. NixOS로 전체를 선언하려 했지만 하드웨어가 빠듯해 접었다고 한다.[^author-backup]
- 이만한 장치를 구하기 어렵다면 Raspberry Pi 같은 대안과 비교한다. HN에서 jon-wood는 이것이 Debian이 도는 ARM 장치일 뿐이라 다른 Debian 장치가 돌리는 것은 다 돌릴 수 있다고 썼다.[^jon-wood]

---

[^author]: <https://news.ycombinator.com/item?id=50406671>

[^mk-stjames]: <https://news.ycombinator.com/item?id=50408551>

[^author-zeroclaw]: <https://news.ycombinator.com/item?id=50407407>

[^hikemu]: <https://news.ycombinator.com/item?id=50407437>

[^author-trade]: <https://news.ycombinator.com/item?id=50408503>

[^suprjami]: <https://news.ycombinator.com/item?id=50408000>

[^peddling-brink]: <https://news.ycombinator.com/item?id=50408063>

[^rustyhancock]: <https://news.ycombinator.com/item?id=50407132>

[^dataflow]: <https://news.ycombinator.com/item?id=50407221>

[^author-buy]: <https://news.ycombinator.com/item?id=50407293>

[^author-backup]: <https://news.ycombinator.com/item?id=50407303>

[^jon-wood]: <https://news.ycombinator.com/item?id=50414669>

[^author-fork]: <https://news.ycombinator.com/item?id=50407216>
