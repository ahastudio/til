# 비둘기가 실어 나른 RFC 1149 패킷 한 장이 크리스티 경매에 나왔다

<https://onlineonly.christies.com/s/fine-printed-books-manuscripts-science/carrier-pigeon-internet-protocol-150/325216>

HN 토론: <https://news.ycombinator.com/item?id=49932911> (84점, 16개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/wqqkws/actual_rfc1149_packet_being_auctioned> (51점, 10개 댓글)

GN 토론: <https://news.hada.io/topic?id=34692>

## 소개

크리스티(Christie's)의 온라인 경매에
“Carrier Pigeon Internet Protocol, April 2001”이라는 이름의 출품물이 올라왔다.
경매 페이지 주소의 슬러그는 `fine-printed-books-manuscripts-science`이고
출품 번호는 150이다.
출품물은 2001년 노르웨이 Bergen Linux User Group(BLUG)이 RFC 1149를 실제로
구현할 때 비둘기 다리에 묶어 보낸 IP/ICMP “ping” 패킷 인쇄물 한 장이다.
이 문서는 경매 페이지의 목록 설명과 페이지에 함께 실린 경매
데이터만을 근거로 한다.
경매 페이지 밖의 BLUG 실험 기록이나 RFC 원문은 따로 읽지 않았다.

## 출품물

크리스티의 설명은 출품물을
`[WAITZMAN, David and the BERGEN LINUX USER GROUP.]`로 표기한다.
실물은 41 x 210 mm 크기의 작은 종이 두루마리다.
비둘기 다리에 묶여 있을 때 생긴 말린 주름이 남아 있고, 액자에 넣은 상태다.
액자 뒤판 뒷면에는 “Property of David Waitzman”이라는 문구와 서명이 있다.

크리스티는 이것을 Carrier Pigeon Internet Protocol의 첫 번째이자 가장 유명한
구현에서 살아남은 패킷이라고 소개한다.
실험 중 실제로 비둘기를 타고 이동한 물리적 인터넷 데이터그램이라는 것이다.
이 패킷은 실험 이듬해 RFC 1149의 원저자인 Waitzman에게 전달되었다.
크리스티는 BLUG가 패킷을 물리적인 액자(frame)에 담아 보낸 것이 IP 패킷이
코드화된 프레임 안에 실려 전송되는 것과 잘 맞아떨어진다고 덧붙인다.

## RFC 1149와 BLUG의 구현

미국 네트워크 엔지니어 David Waitzman은 1990년 만우절에 RFC 1149,
“A Standard for the Transmission of IP Datagrams on Avian Carriers”를 썼다.
비둘기로 인터넷 패킷을 전송하는 방법을 무표정한 기술 문체로 서술한 문서다.
농담으로 쓰였지만 인터넷 민간전승 가운데 가장 잘 알려진 것이 되었고,
30년이 넘게 지난 지금도 널리 인용된다고 크리스티는 적었다.

2001년 4월 28일 BLUG 회원들이 이 프로토콜을 실제 규모로 구현했다.
프린터, 스캐너, 경주용 비둘기를 써서 IP 패킷을 하나씩 16진수 문자열로 인쇄하고,
그 종이를 비둘기 다리에 묶어 약 3마일 떨어진 두 비둘기장 사이로 보냈다.
보낸 패킷은 9개였고 성공적으로 돌아온 응답은 4개였다.

크리스티는 이 구현을 인터넷의 “artful hack” 전통을 보여 주는
전형적인 사례로 소개한다.
초기 인터넷 공동체의 장난기, 기술적 재간, 협업 정신을 담고 있다는 설명이다.

## 경매 정보

다음 값은 2026년 10월 4일 05시 11분(UTC)에 받은 페이지 데이터에서 읽었다.

| 항목             | 값                     |
| ---------------- | ---------------------- |
| 추정가           | USD 2,000 - USD 3,000  |
| 현재 입찰가      | USD 2,600 (14 Bids)    |
| 입찰 시작        | 2026-10-01 14:00 (UTC) |
| 이 출품물의 마감 | 2026-10-13 16:29 (UTC) |
| 출품 번호        | 150                    |

현재 입찰가는 경매가 진행되는 동안 계속 바뀐다.
추정가에는 구매자 수수료와 세금이 포함되지 않는다고 페이지의 안내문은 적고 있다.

## 비평

### 2001년을 “초기 인터넷”으로 부르는 것은 설명의 틀이다

크리스티의 마지막 문단은 이 실험이 초기 인터넷 공동체의 정신을 담았다고 말한다.
HN의 sublinear는 2001년을 “초기 인터넷 공동체”로 부르는 데
의문을 던졌다.[^sublinear]
그 무렵 이미 쇼핑몰이 전자상거래의 영향을 받고 있었다는 것이다.
dn3500은 2001년의 인터넷이 이미 19살이었고, 상업 트래픽이 제한 없이 허용된
1995년의 NSF 백본 종료를 초기 인터넷의 끝으로 본다고 답했다.[^dn3500]
반면 goodmythical은 미국 인구의 3분의 1 정도가 2001년 이후에 태어났으니
그 시기를 역사적으로 부르는 것도 무리가 없다고 보았다.[^goodmythical]

이 논쟁에서 읽어야 할 것은 연대의 정답이 아니라 경매 설명문의 역할이다.
“초기 인터넷”이라는 틀은 출품물을 역사 유물로 위치시키는 데 쓰인다.
1990년의 RFC와 2001년의 실험을 한 문단 안에 묶으면 11년의 간격이 흐려진다.
경매 설명문이 판매를 위해 쓰인 글이라는 점을 감안하고 읽어야
한다는 것이 내 해석이다.

### 가치는 종이가 아니라 출처 기록에 있다

HN의 noisy_boy는 액자 속 패킷은 누구든 직접 입력해 인쇄할 수 있는데
왜 1천 달러가 넘느냐고 물었다.[^noisy_boy]
flufluflufluffy는 이것이 실제로 비둘기가 나른 바로 그 종이이고 RFC 1149 저자의
서명이 있는 인터넷 역사의 기념물이라고 답했다.[^flufluflufluffy]
Lobste.rs의 SamRW는 갖고 싶다면서도,
사진을 찍어 인쇄하면 같은 효과일지 모른다고 농담했다.[^SamRW]

이 문답은 출품물의 가치가 내용이 아니라 출처 기록(provenance)에서
나온다는 점을 드러낸다.
16진수 문자열은 복제할 수 있지만,
비둘기 다리에 묶였던 주름과 Waitzman의 서명은 복제할 수 없다.
다만 경매 페이지가 보여 주는 근거는 크리스티의 설명, 주름,
뒤판의 문구와 서명뿐이다.
이 종이가 9개 패킷 가운데 어느 것인지,
왕복에 성공한 4개에 속하는지는 페이지에 나와 있지 않다.

## 인사이트

### 농담 표준은 실행되는 순간 유물이 된다

RFC 1149 자체는 텍스트이고, 텍스트는 무한히 복제된다.
경매에 나올 수 있는 것은 그 텍스트를 누군가 실제로 실행했을 때 남은
물리적 부산물뿐이다.
Lobste.rs의 zie는 비둘기 조련사와 함께 직접 RFC 1149 패킷을 만들어 보는 것이
더 재미있겠다며,
QoS를 다룬 RFC 2549와 IPv6를 다룬 RFC 6214도 있다고 적었다.[^zie]
HN의 geerlingguy는 2023년 3TB 재실험을 위해 묶어 두었던 SanDisk USB 스틱을 계속
보관해야겠다고 농담했다.[^geerlingguy]

이 두 댓글은 표준이 같아도 구현마다 다른 유물이 남는다는 점을 보여 준다.
농담 RFC의 문화적 가치는 문서보다 그것을 끝까지 실행한 사람들에게서
생긴다는 것이 내 해석이다.
HN의 podunkPDX가 이메일 서명을 “Sent via RFC1149”로 바꿔 둔 것처럼,
실행이 아닌 인용으로 이어지는 경로도 있다.[^podunkPDX]

### 사람이 만든 농담이 사람을 끌어들인다

Lobste.rs의 Two9A는 IP over Avian Carrier나 Hypertext Coffeepot Control 같은
기술이 웹 뒤에 있는 장난기와 인간미를 상기시킨다고 적었다.[^Two9A]
에이전트가 에이전트와 “대화하는” 시대에 인터넷은 사람이 쓰고 사람에게 이롭도록
만들어졌다는 점을 잊지 말아야 한다는 것이다.

같은 스레드에서 gspr은 2001년 베르겐에 살던 15살 리눅스 입문자였다고
밝혔다.[^gspr-lobsters]
주변에 관심사를 나눌 사람이 없어 고립감을 느끼던 중, 아마도 Slashdot에서 같은
도시의 사람들이 RFC 1149를 구현했다는 소식을 보았다고 한다.
비둘기를 날린 장소가 자주 걷던 산책로 근처였고, 그 순간 세상이 가깝게 느껴졌으며
자신도 언젠가 그런 사람이 될 수 있겠다고 생각했다는 것이다.
너무 수줍어 연락은 하지 못했지만 그 일이 자기 삶을 만드는 데
도움이 되었다고 적었다.

크리스티의 설명이 말하는 “협업 정신”보다 이 댓글이 실험의 효과를 더
구체적으로 보여 준다.
쓸모없는 실험이 남긴 가장 큰 결과는 패킷 전송률이 아니라,
그것을 본 누군가가 이 분야에 들어올 수 있다고 느끼게 만든 일이다.

### 판매 가격이 유물의 무게를 정하지는 않는다

HN의 gspr은 이런 가보를 몇천 달러에 파는 것이 이상하게 느껴진다며 판매자가
괜찮은지 물었다.[^gspr]
Lobste.rs의 WilhelmVonWeiner도 살아 있는 동안 고작 몇천 달러에 팔기에는
너무 특별한 물건이라고 보았다.[^WilhelmVonWeiner]
dgl은 남의 사정을 넘겨짚지 말라며, 직접 판매를 주선하면 물건을 원하는 조건으로,
좋은 사람 손에 넘길 수 있다고 답했다.[^dgl]
dsr은 Waitzman이 그날 아침 이메일에서
“인터넷 억만장자를 알면 입찰하라고 해 달라”고 썼다고 전했다.[^dsr]

추정가 2천에서 3천 달러는 이 물건의 문화적 무게에 비하면 작아 보인다.
하지만 농담 RFC 유물에는 비교할 수 있는 거래 기록이 거의 없으니, 이 경매의
낙찰가가 앞으로 같은 종류의 물건에 대한 첫 기준점이 될 가능성이 있다.
이것은 경매 데이터가 아니라 내 추정이다.

---

[^sublinear]: <https://news.ycombinator.com/item?id=49937679>

[^dn3500]: <https://news.ycombinator.com/item?id=49938912>

[^goodmythical]: <https://news.ycombinator.com/item?id=49947768>

[^noisy_boy]: <https://news.ycombinator.com/item?id=49940018>

[^flufluflufluffy]: <https://news.ycombinator.com/item?id=49940181>

[^SamRW]: <https://lobste.rs/s/wqqkws/actual_rfc1149_packet_being_auctioned#c_eccypq>

[^zie]: <https://lobste.rs/s/wqqkws/actual_rfc1149_packet_being_auctioned#c_gxz4rh>

[^geerlingguy]: <https://news.ycombinator.com/item?id=49941115>

[^podunkPDX]: <https://news.ycombinator.com/item?id=49940627>

[^Two9A]: <https://lobste.rs/s/wqqkws/actual_rfc1149_packet_being_auctioned#c_0ptcxr>

[^gspr-lobsters]: <https://lobste.rs/s/wqqkws/actual_rfc1149_packet_being_auctioned#c_ez1uik>

[^gspr]: <https://news.ycombinator.com/item?id=49942922>

[^WilhelmVonWeiner]: <https://lobste.rs/s/wqqkws/actual_rfc1149_packet_being_auctioned#c_2k9yqw>

[^dgl]: <https://lobste.rs/s/wqqkws/actual_rfc1149_packet_being_auctioned#c_djdpog>

[^dsr]: <https://lobste.rs/s/wqqkws/actual_rfc1149_packet_being_auctioned#c_fwre16>
