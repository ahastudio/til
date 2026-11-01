# Tangled의 연합 코드 포지: 이슈와 풀 리퀘스트를 저장소로 옮긴 개편

원문: [The federated code forge · The Tangled Blog](https://tangled.org/blog/forge/)

HN 토론: <https://news.ycombinator.com/item?id=50305573> (307점, 89개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/ukj8mm/federated_code_forge> (37점, 22개 댓글)

## 요약

Tangled가 2026년 10월 30일에 올린 대규모 개편 발표 글이다.
Tangled는 AT Protocol 위에 만든 Git 협업 플랫폼이다.
글은 지난 20년 동안 코드 포지(forge)가 프로젝트가 사는 곳이었지만,
편의를 주는 대가로 중앙화를 요구했다고 말한다.
이어서 운영 시간과 기능과 코드 관리를 남에게 맡기는 중앙화 포지가
무너지고 있다고 진단한다.

글이 내놓는 대안은 연표 한 줄이다.
2005년의 메일과 Git, 2009년의 GitHub와 Git, 2025년의 AT Protocol과 Git이다.
Git으로 코드를 옮기고 이메일이라는 열린 프로토콜로 논의하는 방식은 오래 버텼지만
사용자 경험이 나빴다는 것이다.
Tangled는 열린 프로토콜의 지속성과 제대로 된 포지의 편의를 함께 주겠다고 하며,
스스로를 첫 번째 진정한 연합(federated) 코드 포지라고 부른다.
Git 호스팅이나 CI 실행기처럼 원하는 부분만, 또는 API 서버와 UI까지 전부 직접
운영해도 다른 사람들과 협업할 수 있다는 설명이다.

제품 소식은 다섯 갈래다.
먼저 Svelte로 다시 만든 UI와 글꼴 교체(Inter에서 Timeless Sans)가 있다.
다음으로 Go 모놀리스였던 appview를 쪼갰다.
AT Protocol 색인과 캐시, 프로토콜 밖의 데이터, 화면 그리기를 한 서버가 맡고
SQLite 하나를 스웨덴의 중간 규모 서버 한 대에서 돌리던 구조를, 에지에 배포한
Svelte 프런트엔드와 Rust로 쓴 읽기 전용 색인 서비스 bobbin으로 바꿨다.
bobbin은 디스크 없이 메모리만 쓰고 11개가 넘는 지역에 배포되었다고 한다.

그다음은 데이터 모델이다.
레코드 형식(lexicon)은 sh.tangled.*에서 org.tangled.*로 바뀌었고,
Rust로 다시 쓴 knot2가 사용자 정의 Git 서버와 SSH 서버를 한 바이너리에 담는다.
이슈, 풀 리퀘스트, 댓글, 반응, 라벨은 이제 knot에, 코드 바로 옆에 저장된다.
이 저장 단위는 협업 객체(COB)로, 저장소 안의 Git 객체 사슬일 뿐이다.
knot이 사용자의 말을 바꿔 쓰지 못하도록, 사용자가 레코드를 만들거나 고칠 때마다
웹 앱이 사용자의 PDS에 증명(attestation) 레코드를 따로 쓴다.

나머지는 조직 계정과 스택형 풀 리퀘스트다.
조직은 자체 DID와 핸들을 가진 AT Protocol 계정이며 비밀번호 없는 위임 계정이다.
스택형 풀 리퀘스트는 Jujutsu가 아닌 평범한 Git 사용자에게도 열렸고,
버전 사이의 차이(interdiff)를 볼 수 있다.
글은 앞으로 몇 주에 걸쳐 비공개 저장소, CLI, 여러 언어의 SDK, 에이전트용
스킬이 나온다고 예고한다.

## 분석

### 이 글의 주장은 포지의 위기가 아니라 프로토콜의 선택이다

글은 중앙화 포지의 문제를 운영 시간, 기능, 관리자의 태도라는 세 가지로 요약한다.
모두 남의 결정에 기대는 문제다.
해법으로 내세우는 것은 더 나은 포지가 아니라 열린 프로토콜이다.
연표가 이 논리를 압축한다.
메일에서 GitHub로 갈 때 사람들은 프로토콜을 서비스로 바꿨고,
Tangled는 서비스를 다시 프로토콜로 되돌리려 한다.

이 전제에서 보면 Tangled가 파는 것은 기능이 아니라 이탈할 수 있는 권리다.
글은 자체 호스팅을 부분 단위로 설명한다.
Git 호스팅만, CI 실행기만, 또는 API 서버와 UI까지 고를 수 있다.
다만 첫 번째 진정한 연합 포지라는 말은 Tangled의 자기 평가다.
무엇을 연합이라 부르는지에 따라 달라지는 주장이다.

### 구조 개편은 읽기와 쓰기를 가른다

개편 전 appview는 한 대의 서버에 모든 일을 몰아 둔 구조였다.
글은 이것이 사용자가 스웨덴에서 50~100밀리초 거리일 때만 괜찮았고,
대부분의 사용자는 그렇지 않았다고 직접 적는다.
새 구조는 읽기와 쓰기를 가른다.
bobbin은 AT Protocol 데이터만 다루는 읽기 전용 색인이고,
나머지 기능은 다른 서비스가 맡는다.

이 분리 덕에 읽기는 전 세계에 복제할 수 있다.
HN에서 nerdypepper는 appview가 이제 완전히 메모리에서 돌고 상태가 없어서
네트워크의 상태를 매번 처음부터 다시 만든다고 설명했다.[^nerdypepper-indexer]
쓰기는 저장소가 있는 knot에 머문다.

### 이슈와 풀 리퀘스트를 저장소로 옮긴 결정이 연합의 실체다

가장 큰 설계 변화는 데이터가 사는 곳이다.
이슈와 풀 리퀘스트와 댓글이 사용자 계정이 아니라 저장소를 따라간다.
글은 프로젝트의 이슈와 풀 리퀘스트도 코드만큼 그 프로젝트의 일부이므로 호스팅
위치와 상관없이 함께 있어야 한다고 이유를 밝힌다.
저장소를 옮기면 논의도 따라 옮겨지므로 이식성이 최대가 된다는 것이다.

HN에서 icy는 Tangled 공동 창업자라고 소개하며, 이제 저장소가 이슈와 풀 리퀘스트를
소유한다고 확인했다.
Git 객체로 저장소 안에 저장하고 AT Protocol의 MST로 투영하기 때문에 knot이
PDS와 닮게 된다고 설명했다.[^icy-cob]
이 구조의 약점도 글이 알고 있다.
knot이 사용자의 이름으로 글을 쓸 수 있다면 말을 바꿔 넣을 수도 있다.
그래서 사용자 PDS에 증명 레코드를 따로 써서 knot과 사용자가 서로를 검증하게
했다.

### 커뮤니티의 첫 질문은 낯선 기여자와 비공개였다

HN에서 kstrauser는 자기 Forgejo로 프로젝트를 옮겼지만 낯선 사람이 가입 없이
풀 리퀘스트를 열기 어려워 아쉽다고 하면서, Tangled에서는 낯선 기여자가 무엇을
해야 하느냐고 물었다.[^kstrauser]
nerdypepper는 AT Protocol 계정만 있으면 되고, 곧 저장소별 기여 정책을
선언할 수 있을 것이라고 답했다.[^nerdypepper-policy]
icy는 이 계정이 마지막으로 필요한 계정이며 이식할 수 있다고 덧붙였다.[^icy-account]

비공개 저장소에 대한 질문도 이어졌다.
jon-wood는 Tangled의 데이터 모델이 AT Protocol 위에 있고 이 프로토콜은 올린 것이
모두 공개라고 가정하므로 지금은 비공개 저장소가 어렵다고 설명했다.[^jon-wood]
nerdypepper는 AT Protocol의 spaces 알파와 비슷하게 동작하는 시연이 이미 있고
몇 주 안에 보여 주겠다고 답했다.[^nerdypepper-private]

Lobste.rs에서도 첫 반응은 같았다.
minimax는 개인정보 모델이 전혀 없는 포지는 끌리지 않는다고 했고,[^minimax]
uncenter는 글 끝에 비공개 저장소가 예고되어 있다고 짚었다.[^uncenter]
mariusor는 연합하는 부분이 변경 요청과 리뷰와 댓글 같은 사회적 상호작용에
그치기를 바란다고 했다.[^mariusor]
frontsideair는 코드가 있는 knot은 직접 또는 Tangled가 운영하고 상호작용은
AT Protocol에 저장되며, 정보가 샐 수는 있어도 대안보다는 낫다고 이해했다.[^frontsideair]
이는 댓글 작성자의 이해이고, 글은 이슈와 풀 리퀘스트가 이제 knot에 저장된다고
말한다.

## 비평

### 첫 번째 진정한 연합 포지라는 말은 정의에 달려 있다

글의 가장 센 문장은 첫 번째 진정한 연합 포지라는 주장이다.
HN의 질문이 이 주장의 경계를 드러냈다.
vaylian은 ForgeFed에 대한 입장을 물었고,[^vaylian]
ar-nelson은 Forgejo의 ActivityPub 연합 기능이 한참 정체 상태라고 짚으면서
AT Protocol이 구현하기 더 쉽다고 했다.[^ar-nelson]
rapnie는 ForgeFed를 구현하는 프로젝트가 여럿 있다고 목록을 들었다.[^rapnie]
Tangled가 처음이라는 말은 연합을 무엇으로 정의하느냐에 달린 말이다.

더 날카로운 반론은 max-privatevoid에게서 나왔다.
이 프로토콜은 AppView가 네트워크 전체를 소비해야 하고 중계기(relay)에 메시지 전달을
맡겨야 하므로 중앙화로 기울어 있다는 것이다.[^max-privatevoid]
글 자체가 이 주장에 힘을 싣는다.
개편 전의 구조 설명이 스웨덴의 한 서버에 모든 것을 둔 앱이었다고 인정하기
때문이다.
icy는 맞섰다.
AppView는 org.tangled.*만 받아 오는 색인이고,
ActivityPub은 신원이 인스턴스에 묶여 있어서 이 용도에 맞지 않는다는 것이다.[^icy-appview]
jauntywundrkind는 중계기가 작은 서버로도 돌 수 있다고 보탰다.[^jauntywundrkind]
Lobste.rs에서 pointlessone은 ForgeFed를 더 좋아하지만 깊이 따져 본 판단은 아니라는
단서를 달았고,[^pointlessone]
diktomat은 ActivityPub이 처음부터 기본적인 것을 잘못 잡았고 AT Protocol은 많은 것을
제대로 잡았다고 보았다.[^diktomat]
논쟁은 결론 없이 끝났고, 글은 이 쟁점을 다루지 않는다.

### 자체 호스팅이 쉬워졌다는 말은 범위가 좁다

글은 Tangled 전체를 쉽게 자체 호스팅할 수 있다고 말한다.
그러나 HN에서 드러난 빈틈이 있다.
jon-wood의 말대로 지금은 자체 호스팅에서 비공개 저장소를 지원하지 않는다.[^jon-wood]
HexDecOctBin은 knot이 SSH만 지원해서 Cloudflare 뒤에 두기 어렵다고 지적했고,[^hexdecoctbin]
nerdypepper는 HTTPS 푸시가 이미 있지만 문서화되지 않았다고 답했다.[^nerdypepper-https]
사용성의 흠도 있었다.
paaloeye는 댓글란에 댓글 버튼이 없어 사람들이 풀 리퀘스트를 모르고 닫을 수 있다고
지적했다.[^paaloeye]

Lobste.rs에서 arialdo는 UI와 색인과 knot을 Tailscale 안에 두고 tailnet에서만 보이는
완전한 비공개 포지로 운영할 수 있는지 물었다.[^arialdo]
이 질문에는 답이 달리지 않았다.
이는 출시 직후의 사소한 흠으로 볼 수도 있다.
그러나 자체 호스팅이 쉽다는 주장은 이런 흠이 있는 상태에서의 주장이라는 점은
알아 둘 만하다.
글이 예고한 비공개 저장소가 오면 이 목록은 줄어들 것이다.

### 새 용어가 한꺼번에 쏟아져 읽는 사람을 가린다

글은 appview, firehose, knot, spindle, bobbin, lexicon, PDS, DID, COB 같은 말을
풀이 없이 이어서 쓴다.
Lobste.rs에서 zetashift는 Svelte와 Nix와 AT Protocol처럼 좋아하는 것이 겹치는데도
이 용어들을 이어 붙이면 무슨 뜻인지 모르겠다고 털어놓았다.[^zetashift]
diktomat은 knot이 저장소 서버, spindle이 CI 서버, bobbin이 CDN에 가까운 것이라고
풀어 주었다.[^diktomat-terms]

이 용어들은 Tangled의 자체 이름이고, 글의 독자는 이미 AT Protocol에 익숙한
사람으로 전제되어 있다.
연합이라는 약속은 처음 오는 사람이 이해하고 들어올 수 있어야 의미가 커진다.
한 문장짜리 용어 풀이가 글에 있었다면 이 비용을 줄일 수 있었다.

### 이 글은 사업 모델에 침묵한다

글은 열린 프로토콜과 개발자의 주도권에 건 선택이 앞으로 10년을 버티게 해 줄
것이라고 말한다.
그러나 이 서비스가 어떻게 유지될지는 말하지 않는다.
HN에서 rapnie는 자체 호스팅을 고려하는 입장에서 사업 모델이 궁금하다고 물었고,[^rapnie-business]
paaloeye는 GitHub와 경쟁하기 쉽지 않다고 했다.[^paaloeye-business]
ivanjermakov는 Tangled가 380만 유로를 조달했다는 기사 링크를 올렸다.[^ivanjermakov]
이는 댓글이 가리킨 기사이고 글에는 없는 내용이다.
10년을 약속하는 글이라면 이 서비스의 존속 조건도 함께 밝히는 편이 설득력이 컸을
것이다.

## 인사이트

### 저장소가 논의를 소유하면 포지는 색인으로 줄어든다

이슈와 풀 리퀘스트가 저장소 안에 살면 포지가 가진 것은 데이터가 아니라 화면과
색인이다.
글의 연표가 말하듯 Git은 코드를 분산시켰지만 논의는 메일에서 GitHub로 중앙에
모이게 했다.
이 설계는 논의까지 분산시킨다.
그러면 포지 사이의 경쟁은 데이터를 가진 쪽이 아니라 데이터를 더 잘 보여 주는
쪽의 경쟁이 된다.
이는 필자의 해석이다.

여기서 새 문제가 생긴다.
데이터가 저장소를 따라가면 의존성의 가용성이 저장소를 가진 서버에 달린다.
HN에서 stryan은 Neovim 플러그인이 Tangled에 있었는데 그 knot이 내려가 있어서
새 기계 설정이 막혔다고 했다.[^stryan]
nerdypepper는 Tangled가 모든 Git 저장소의 미러를 두고 있으며 knot이 내려가면
이를 제공하고, 해시를 확인하는 방식은 Go의 패키지 프록시와 같다고 답했다.[^nerdypepper-mirror]
이식성이 커진 만큼 어디서 가져올지와 어떤 해시를 믿을지를 의존하는 쪽이 정해야
한다.

### 권한이 없는 프로토콜 위에 비공개를 얹으면 파편화가 따른다

verdverm은 AT Protocol의 권한 원시 요소가 처음부터 들어 있었어야 하고,
spaces는 핵심 인가 블록을 빼먹어서 사용자 영역에서 구현해야 하므로 방식이 갈릴
것이라고 했다.[^verdverm]
Tangled의 비공개 저장소 계획은 정확히 그 위에 있다.
nerdypepper가 spaces 알파와 비슷하지만 spaces의 안정화를 기다리지 않는 시연이라고
말한 것은, 표준을 기다리지 않고 먼저 가겠다는 선택이다.[^nerdypepper-private]

이 선택은 속도와 호환성을 맞바꾼다.
먼저 가면 사용자가 빨리 쓰지만, 나중에 표준이 나오면 Tangled의 방식과 달라질 수
있다.
그때 비공개 저장소를 쓰던 사용자는 다시 옮겨야 할지 모른다.
이는 필자의 추론이다.

Lobste.rs에서 pksunkara는 spaces 제안이 이 문제를 해결하지 않느냐고 물었다.[^pksunkara]
Tangled 쪽으로 보이는 op는 spaces가 해결하고 이미 구현이 여럿 있으며,
Tangled도 비공개 저장소에 매우 비슷한 방식을 만들었고 사양이 안정되면 그에 맞춰
올리겠다고 답했다.[^op-lobsters]
그 답대로라면 위의 위험은 사양이 나온 뒤 옮겨 가는 비용으로 한정된다.

### 손쉬운 변형과 안정된 스키마 사이에서 스키마를 고정했다

글은 에이전트 덕에 맞춤형 소프트웨어를 만드는 일이 쉬워졌고,
해킹하기 쉽게 설계한 소프트웨어에서는 특히 그렇다고 말한다.
Cloudflare Workers 위의 knot, 다른 CI를 잇는 spindle, 자체 API 서버로 만든 포지가
그 예다.
이런 변형이 늘수록 서로 호환되는 기준이 중요해진다.

그래서 이번 개편이 레코드 형식을 안정화한 것이 의미 있다.
nerdypepper는 형식을 안정화했으므로 자체 호스팅하는 사람이 깨지는 업그레이드를
요구받지 않을 것이라고 했다.[^nerdypepper-indexer]
Lobste.rs에서 tuxes는 GitHub에서 LLM 에이전트에게 모든 저장소를 읽고 풀 리퀘스트를
올릴 수 있지만 커밋과 병합은 못 하게 하는 인증 모델을 만들기 어려워서, 직접
비공개 포지를 세우는 것을 생각했다고 했다.[^tuxes]
에이전트에게 맞춘 권한 모델이 필요한 사람에게 해킹하기 쉬운 포지는 실제 동기가
된다.
변형의 자유와 호환의 안정을 함께 얻으려면 바뀌지 않는 것을 먼저 정해야 한다.
Tangled는 그 기준을 데이터 형식에 두었다.
이 정리는 필자의 해석이다.

---

[^nerdypepper-indexer]: <https://news.ycombinator.com/item?id=50307404>

[^icy-cob]: <https://news.ycombinator.com/item?id=50307665>

[^kstrauser]: <https://news.ycombinator.com/item?id=50306295>

[^nerdypepper-policy]: <https://news.ycombinator.com/item?id=50306367>

[^icy-account]: <https://news.ycombinator.com/item?id=50306446>

[^jon-wood]: <https://news.ycombinator.com/item?id=50306906>

[^nerdypepper-private]: <https://news.ycombinator.com/item?id=50307062>

[^vaylian]: <https://news.ycombinator.com/item?id=50308840>

[^ar-nelson]: <https://news.ycombinator.com/item?id=50309531>

[^rapnie]: <https://news.ycombinator.com/item?id=50309100>

[^max-privatevoid]: <https://news.ycombinator.com/item?id=50307499>

[^icy-appview]: <https://news.ycombinator.com/item?id=50308751>

[^jauntywundrkind]: <https://news.ycombinator.com/item?id=50308861>

[^hexdecoctbin]: <https://news.ycombinator.com/item?id=50311849>

[^nerdypepper-https]: <https://news.ycombinator.com/item?id=50307193>

[^paaloeye]: <https://news.ycombinator.com/item?id=50307561>

[^rapnie-business]: <https://news.ycombinator.com/item?id=50309244>

[^paaloeye-business]: <https://news.ycombinator.com/item?id=50308279>

[^ivanjermakov]: <https://news.ycombinator.com/item?id=50307812>

[^stryan]: <https://news.ycombinator.com/item?id=50306735>

[^nerdypepper-mirror]: <https://news.ycombinator.com/item?id=50306854>

[^verdverm]: <https://news.ycombinator.com/item?id=50308121>

[^minimax]: <https://lobste.rs/s/ukj8mm/federated_code_forge#c_kxofko>

[^uncenter]: <https://lobste.rs/s/ukj8mm/federated_code_forge#c_zyxfey>

[^mariusor]: <https://lobste.rs/s/ukj8mm/federated_code_forge#c_w54hex>

[^frontsideair]: <https://lobste.rs/s/ukj8mm/federated_code_forge#c_sgykvx>

[^pointlessone]: <https://lobste.rs/s/ukj8mm/federated_code_forge#c_wv7nse>

[^diktomat]: <https://lobste.rs/s/ukj8mm/federated_code_forge#c_zrdwpx>

[^arialdo]: <https://lobste.rs/s/ukj8mm/federated_code_forge#c_3zbeeq>

[^zetashift]: <https://lobste.rs/s/ukj8mm/federated_code_forge#c_ziegse>

[^diktomat-terms]: <https://lobste.rs/s/ukj8mm/federated_code_forge#c_yyfjld>

[^pksunkara]: <https://lobste.rs/s/ukj8mm/federated_code_forge#c_zb6xty>

[^op-lobsters]: <https://lobste.rs/s/ukj8mm/federated_code_forge#c_tohzf1>

[^tuxes]: <https://lobste.rs/s/ukj8mm/federated_code_forge#c_dy6glz>
