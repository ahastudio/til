# Ladybird 알파 공개

원문: [Ladybird is now in alpha](https://ladybird.org/posts/alpha/)

HN 토론: <https://news.ycombinator.com/item?id=50614249> (2159점, 524개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/h6webg/ladybird_is_now_alpha>

GN 토론: <https://news.hada.io/topic?id=37724>

## 요약

Andreas Kling이 2026년 11월 23일에 올린 짧은 공지이다.
Ladybird가 알파 단계에 들어갔고 macOS와 Linux용으로 내려받을 수 있다고 한다.
이 문서는 공지의 전문을 읽고 썼으며, 분량이 짧아 공지가 말한 내용은 아래가 전부이다.

- 정체: 새 엔진을 가진 브라우저이다.
  엔진은 처음부터 직접 만들었고 포크가 아니며, 주변의 브라우저 껍데기는 소박하지만 작동한다고 한다.
- 한계: 일부 사이트는 작동하지 않고 가끔 충돌한다.
  브라우저 안에서 깨진 사이트를 신고할 수 있고, 충돌 뒤에는 보고서를 읽고 보낼지 정할 수 있다.
- 보안: 보안 연구자들이 공격해 주기를 바란다고 하며, 지금은 보안을 약속하지 않는다고 밝힌다.
  뚫었다면 방법을 알려 달라고 한다.
- 배포 방식: 알파는 롤링 채널이며 자동 업데이트가 정기적으로 나온다.
  지금까지는 개선을 보려면 소스에서 직접 빌드해야 했다.
- 웹 개발자: 자기 사이트를 Ladybird에서 시험해 깨지는 곳을 알려 달라고 한다.
  자동 시험용 WebDriver와 Firefox DevTools 프로토콜을 지원한다.

## 분석

### 공지가 약속하는 것과 약속하지 않는 것

공지가 확실히 말하는 변화는 두 가지이다.
소스를 빌드하지 않고 내려받아 쓸 수 있게 되었다는 것과 그 뒤 자동으로 업데이트된다는 것이다.
반대로 호환성의 정도나 성능에 대한 수치, 지원 일정은 공지에 없다.
GeekNews의 요약은 웹 표준 테스트(WPT)에서 Safari Technology Preview를 앞질렀고 JavaScript JIT를 넣었다고 적지만,
이 문서가 읽은 공지 본문에서는 그 문장을 찾지 못했다.
그래서 이 문서는 그 수치를 사실로 쓰지 않는다.

### 보안 문구의 성격

“보안을 약속하지 않는다”는 문장은 알파 소프트웨어에 흔한 면책이면서 동시에 연구자를 향한 초대이다.
공지가 요구하는 것은 취약점을 공개 전에 알려 달라는 한 가지이며, 포상이나 절차는 쓰여 있지 않다.

## 비평

### 써 본 사람들의 첫 반응

HN의 freakynit은 이미 Firefox로 열어 둔 사이트를 포함해 많은 사이트를 시험했고
전부 제대로 그려졌으며 스크롤이 조금 끊기는 것이 유일한 문제라고 했다.[^freakynit]
kamranjon은 탭 여러 개를 열고도 메모리가 53MB 정도라고 했다.[^kamranjon]
FinnKuhn은 패스키로 로그인하는 사이트에서는 작동하지 않아 실제 사용에 제약이 된다고 했다.[^FinnKuhn]
Lobste.rs의 smoores는 Ladybird로 댓글을 쓰고 있다고 하면서 일부 글꼴이 맞지 않는다고 했고,[^smoores]
classichasclass는 Mac에서는 알파치고 상당히 다듬어졌다고 답했다.[^classichasclass]
GeekNews의 edunga1은 문제 없이 탐색되지만 매직 마우스와 트랙패드의 앞으로/뒤로 제스처가 동작하지 않는다고 했다.[^edunga1]
모두 개인의 사용 경험이며 이 문서가 직접 시험한 것은 아니다.

### 보안 주의

HN의 jtumbot은 알파 동안 어떤 주의가 필요한지 물었고,
hollerith는 안전하지 않은 브라우저는 그 운영체제 전체를 위험하게 만든다고 답했다.[^hollerith]
npteljes는 지금처럼 알려지지 않은 틈새 단계에서는 실제 위험이 크지 않고
샌드박스, 별도 VM, 오래된 노트북 같은 격리를 권했다.[^npteljes]
pessimizer는 Ladybird를 노리는 공격자는 거의 없고 평소 쓰는 브라우저가 오히려 더 위험하다고 보았다.[^pessimizer]
GeekNews의 geek12356은 연구자에게 공격을 부탁하는 공지를 책임 떠넘기기로 읽었다.[^geek12356]
공지는 이 요청이 새 브라우저의 일반적인 과정이라는 입장이다.

### 왜 또 하나의 브라우저인가

sashank_1509는 Mozilla나 Chrome을 떠날 이유가 없고 시간 낭비라고 했고,[^sashank_1509]
pure-orange는 비 Chromium 브라우저가 늘어나는 이점을 보지 못하느냐고 되물었다.[^pure-orange]
x-complexity는 구현이 하나 늘 때마다 Chromium이 사양을 좌우하는 힘이 줄어든다고 했다.[^x-complexity]
worldsavior의 Chromium 포크 제안에는 wavemode가 포크를 유지하려면 구글 직원 수백 명이 하는 일을 따라가야 한다고 답했다.[^wavemode]

### 개발 방식과 프로젝트를 둘러싼 논쟁

kvuj는 sqlite와 Skia 같은 검증된 라이브러리를 쓰면서 개선이 빨라졌지만 초기의 해커 정신이 그립다고 했다.[^kvuj]
diath는 LLM을 쓰는 개발이 진행 속도를 올렸다고 보았고,[^diath]
moralestapia는 브라우저를 처음부터 만드는 일이 AI 시대에는 불가능할 만큼 어렵지 않다고 했다.[^moralestapia]
youngtaff와 KingMob은 프로젝트 주도자의 정치적 견해와 과거 행동 때문에 쓰지 않겠다고 했다.[^youngtaff][^KingMob]
이 논쟁은 공지와 직접 관련이 없고 이 문서는 사실 여부를 확인하지 못했다.

### Servo와의 차이

Lobste.rs의 aCaB이 Servo와 비교를 묻자 op는 Servo는 임베딩을 염두에 두고 설계되었고
Ladybird는 통과하는 WPT 시험이 훨씬 많다고 답했다.[^aCaB][^op-lobsters]
moltonel은 Servo는 엔진이고 껍데기는 일부러 최소로 두는 반면 Ladybird는 전통적인 브라우저에 가깝다고 보탰다.[^moltonel]
op의 WPT 서술은 댓글의 설명이며 이 문서는 수치를 확인하지 못했다.

### Rust 전환

siwatanejo가 Rust 이식의 진행을 묻자 nicoburns는 C/C++/Rust 코드만 세면 절반 정도가 Rust이고
외부 기여는 더 받지 않는다고 답했다.[^nicoburns]
이 문서는 저장소의 언어 비율을 확인하지 못했다.

## 인사이트

### 글에서 가져갈 것

이 공지의 요점은 새 기능이 아니라 배포 단계의 변화이다.
소스 빌드 없이 쓸 수 있고 자동 업데이트가 있는 알파가 된 것이다.
쓰는 사람에게 현실적인 선택은 주 브라우저를 바꾸는 것이 아니라
격리된 환경에서 자신이 쓰는 사이트가 되는지 시험해 보고 깨지는 곳을 신고하는 것이다.
웹 개발자라면 WebDriver를 이용한 자동 시험에 Ladybird를 추가해 볼 수 있다.

### 확인할 관찰

1. WPT 통과율 같은 호환성 수치가 공식 문서로 공개되는지.
2. 패스키, 제스처, 글꼴 같은 댓글에 나온 문제가 얼마나 빨리 고쳐지는지.
3. 보안 제보 절차와 취약점 보고가 공개되는지.
4. 자동 업데이트가 안정적으로 유지되는지.

위 넷 모두 이 문서가 확인하지 못했다.

---

[^freakynit]: <https://news.ycombinator.com/item?id=50615429>

[^kamranjon]: <https://news.ycombinator.com/item?id=50617209>

[^FinnKuhn]: <https://news.ycombinator.com/item?id=50625653>

[^smoores]: <https://lobste.rs/s/h6webg/ladybird_is_now_alpha#c_2udxnm>

[^classichasclass]: <https://lobste.rs/s/h6webg/ladybird_is_now_alpha#c_55vjis>

[^edunga1]: <https://news.hada.io/topic?id=37724#cid70488>

[^hollerith]: <https://news.ycombinator.com/item?id=50614699>

[^npteljes]: <https://news.ycombinator.com/item?id=50616200>

[^pessimizer]: <https://news.ycombinator.com/item?id=50618960>

[^geek12356]: <https://news.hada.io/topic?id=37724#cid70481>

[^sashank_1509]: <https://news.ycombinator.com/item?id=50614742>

[^pure-orange]: <https://news.ycombinator.com/item?id=50614794>

[^x-complexity]: <https://news.ycombinator.com/item?id=50624131>

[^wavemode]: <https://news.ycombinator.com/item?id=50616022>

[^kvuj]: <https://news.ycombinator.com/item?id=50614419>

[^diath]: <https://news.ycombinator.com/item?id=50615206>

[^moralestapia]: <https://news.ycombinator.com/item?id=50619638>

[^youngtaff]: <https://news.ycombinator.com/item?id=50615248>

[^KingMob]: <https://news.ycombinator.com/item?id=50625099>

[^aCaB]: <https://lobste.rs/s/h6webg/ladybird_is_now_alpha#c_vqiwsq>

[^op-lobsters]: <https://lobste.rs/s/h6webg/ladybird_is_now_alpha#c_5bkzy6>

[^moltonel]: <https://lobste.rs/s/h6webg/ladybird_is_now_alpha#c_afbxtd>

[^nicoburns]: <https://news.ycombinator.com/item?id=50615497>
