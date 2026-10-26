# Steal My Bitcoin: 알려진 PHP 취약점이 있는 서버에서 비트코인 키를 가져가는 도전

<https://stealmybitcoin.com/>

Show HN: [Steal My Bitcoin](https://news.ycombinator.com/item?id=50224916) (504점, 309개 댓글)

GN 토론: <https://news.hada.io/topic?id=35941>

## 소개

Steal My Bitcoin은 의도적으로 취약하게 둔 서버에 비트코인 키를 숨겨 놓고, 그
키를 가져가는 첫 사람이 이기는 보안 도전이다.
페이지는 서버 어딘가에 약 500달러 상당의 비트코인 키가 있고,
PHP 사용자 계정이 `print-flag`라는 실행 파일을 통해 그 키에 접근할 수 있다고
설명한다.
서버의 PHP 버전은 PHP2SHELL 취약점들이 공개되기 전의 것으로 골랐다고 한다.
먼저 지갑을 비우는 사람이 상금을 가져가며, 돈이 필요 없다면 GiveWell 같은 곳에
기부하라는 문장이 붙어 있다.

페이지 맨 위에는 성공한 해킹 없이 흐른 시간이 시 단위로 표시된다.
시계의 시작은 2026년 10월 24일 20시 30분(UTC)이다.
이 시계는 방문자의 시계가 아니라 지갑 거래 내역으로 멈춘다.
화면의 스크립트는 지갑 주소의 거래 내역을 mempool.space API에서 거슬러 읽어,
잔액이 10달러 아래로 내려간 거래를 찾고 그 거래가 들어간 블록 시각을 종료
시각으로 쓴다.
페이지에는 지갑 주소와 잔액, 새로고침 버튼도 있다.

HN에 올린 사람은 cloudlandsdev다.
도전이 올라온 때는 PHP 코어의 치명적 취약점에 대한 보안 패치가 나오고 며칠 지난
시점이고,
Wiz가 PHP2Shell로 이름 붙여 공개한 그 취약점이 이 도전의 배경이다.
cloudlandsdev는 HN 답글에서 이 도전의 목표를 길모퉁이에 500달러를 놓고
가져가세요라는 팻말을 세워 얼마나 오래 남는지 보는 것이라고 설명했다.
누군가 같은 모퉁이에 자기 돈을 보태는 것은 그 사람의 몫이라고도
했다.[^cloudlandsdev-goal]

## 이용 규칙

별도 약관 페이지가 참여 범위를 정한다.

- 이 도전은 무작위 추첨이 아니라 기술을 겨루는 것이고, 결제는 필요 없다.
- 시험해도 되는 대상은 웹 애플리케이션과 PHP 컨테이너 안에서 `print-flag`를
실행하는 일까지다.
- 호스트, SSH, Docker, Nginx, 다른 사람, 제3자 서비스는 공격하면 안 된다.
- 컨테이너 탈출, 서비스 거부, 자원 고갈, 지속 접근, 방해 행위는 금지된다.
- 키를 찾아도 다른 사람이 먼저 지갑을 비울 수 있으며, 지급이나 대체는 보장되지
않는다.
- 자기 돈을 지갑에 보내지 말고, 격리된 환경에서 시험하며, 비밀번호나 개인정보를
제출하지 말라고 한다.
- 모든 트래픽은 기록되고, 도전은 언제든 중단되거나 바뀔 수 있다.

## 비평

### 이 도전은 주장을 반증할 수 없다

HN에서 hau는 이 도전이 사소한 익스플로잇이 존재한다는 주장을 반증 가능하게
만든다고 했다.[^hau]
akerl_는 이것이 익스플로잇의 존재를 반증할 수 없고,
이 서버에 익스플로잇이 쓰였는지만 보여 줄 수 있다고 바로잡았다.[^akerl_]
muvlon은 거기서 더 나아가, 서버가 거짓말을 할 수 있으므로 그것조차 보일 수
없다고 했다.[^muvlon]
tylergetsay는 코인이 옮겨지면 블록체인은 거짓말을 하지 않는다고 맞섰고,
akerl_는 키가 서버에 실제로 있다는 가정이 있어야 성립한다고
답했다.[^akerl_-chain]

결과는 비대칭이다.
누군가 지갑을 비우면 취약한 구성이 있다는 사실이 확인된다.
아무도 비우지 않은 시간은 훨씬 적은 것을 알려 준다.

### 키가 실제로 서버에 있다는 증거가 없다

Stevvo는 키가 서버에 있다는 증명이 없으므로 공격할 이유가 없다고 했다.[^Stevvo]
echoangle는 가능성이 0이 아니므로 기대값에 확률을 곱해 따져야 하고, 첫 사람이 될
기대값을 약 300달러로 추정했다.[^echoangle]
orlp는 더 날카로운 가능성을 짚었다.
키가 서버에 없어도 운영자는 여러 시도가 기록된 로그와 돈을 모두 가진다는
것이다.[^orlp]
zoeysmithe도 모든 트래픽이 기록되므로 500달러로 새로운 변형까지 얻을 수 있는
영리한 구조라고 했다.[^zoeysmithe]

paxy는 같은 논리를 뒤집었다.
자신이 이 사이트를 뚫었지만 키를 찾지 못했다고 쓰고, 증거는 도전을 올린 사람이
낸 만큼이라고 했다.[^paxy]
Gigachad는 셸을 얻었다면 서버를 내리거나 화면을 바꿔 보이면 된다고
답했다.[^Gigachad]
이 응수는 성공의 증명은 쉽지만 실패의 증명은 어렵다는 같은 비대칭을 다른 쪽에서
보여 준다.

### 서버가 먼저 쓰러졌다

nayuki는 글이 올라온 직후 서버가 과부하라며 페이지 문구를 옮겨 적었다.[^nayuki]
glerk는 누구도 비트코인에 닿기 전에 서버가 서비스 거부를 당한 것 같다고
했다.[^glerk]
vikramkr도 서버가 한동안 내려가 있어서, 사이트가 안전한 것인지 익스플로잇을 가진
사람이 쓰기 전에
서비스 거부로 쓰러진 것인지 알 수 없다고 했다.[^vikramkr]
cloudlandsdev는 접속량이 예상 밖이었고, 서버를 키울 때마다 늘어난 자원이 곧
소진된다고 밝혔다.
해결 사례를 블로그에 쓰기 위한 기록은 디스크 용량이 부족해 가능한 만큼만
남기겠다고도 했다.[^cloudlandsdev-update]
그렇다면 모든 트래픽이 기록된다는 페이지의 문구는 실제로는 일부만 기록된다는
뜻이어서,
로그로 새 익스플로잇을 얻는다는 우려도 그만큼 줄어든다.
서버가 응답하지 못한 시간도 해킹이 없었던 시간으로 세어진다.
페이지 시계는 서버가 응답했는지와 상관없이 흐르기 때문이다.

## 인사이트

### 미청구 시간은 구성 하나에 대한 증거일 뿐이다

이 도전이 알리고 싶은 것은 AI로 서버를 대규모로 뚫는다는 서사의 가격이다.
fwlr는 그 서사에 가격 정보를 넣는다고 했고,
500달러가 아니라 1만 5천 달러쯤이라면 서사가 완전히 다르게 보일 것이라고
했다.[^fwlr]
ls612는 이를 가격 신호로 읽었다.
운영자는 돈을 잃을 각오를 하고, 인터넷에 연결된 PHP 서버를 자동으로 뚫는 무리가
아직 없음을 보이려 한다는 것이다.[^ls612]
technion은 한 시간이 지나도 열려 있다는 사실이 천 개의 에이전트가 사이트를
장악한다는 이야기를 끝낸다고 봤다.[^technion]

그러나 이 서버는 알려진 취약 버전을 쓰되 구성은 운영자가 고른 것이다.
oefrha는 이 서버가 보통보다 덜 취약한 설정과 강한 감시를 갖췄을 가능성이 크다고
했다.[^oefrha]
jerrythegerbil은 이 서버가 악용 가능하더라도 GitHub에서 찾은 범용 공개 코드로는
안 되고,
애플리케이션 구성에 맞춰 고쳐야 한다고 했다.[^jerrythegerbil]
msm_도 모든 서버를 한 번에 뚫는 익스플로잇은 아직 없고, 대상마다 시간이 든다고
했다.[^msm_]
athrowaway3z는 악용되지 않은 서버는 악용되지 않는 구성이 존재한다는 뜻일
뿐이라고 정리했다.[^athrowaway3z]
그러므로 미청구 시간이 알려 주는 것은 이 구성이 아직 안 뚫렸다는 사실이다.
인터넷의 PHP 서버 일반에 대한 결론으로 확장하려면 구성의 대표성이 필요한데, 그
근거는 도전에 없다.

### 상금이 늘어나면 가격 신호는 시장이 된다

xmcp123은 글이 올라온 지 얼마 안 되어 누군가 지갑에 돈을 더해 상금이 1,004달러가
되었다고 적었다.[^xmcp123]
johanyc는 잔액이 0.02500416 BTC, 약 2,018달러라고 적었다.[^johanyc]
상금이 운영자의 500달러에서 방문자의 기부로 커지면 가격은 더 이상 한 사람의
판단이 아니다.
많은 사람이 보태는 상금은 이 구성을 뚫는 일의 값을 시장이 정하게 만든다.

그러나 약관은 자기 돈을 지갑에 보내지 말라고 한다.
보태진 돈도 같은 지갑에 있으므로, 도전에 성공한 사람이 가져가고 돌려받을 길은
없기 때문이다.
상금을 더한 사람이 얻는 것은 도전자가 늘어난다는 기대뿐이다.

### 공개 도전은 기록을 만들고, 그 기록은 방어자와 공격자 중 누구에게도 쓸 수 있다

zoeysmithe는 모든 트래픽이 기록된다는 문구를 두고,
500달러로 새로운 익스플로잇이나 변형을 얻는 사업 모델이라고
꼬집었다.[^zoeysmithe]
A1kmm은 이 점을 구체화했다.
익스플로잇이 백엔드와 주고받는 대화를 통해 서버가 사용자에 맞춰 보내는
페이로드를 볼 수 있지만, 백엔드의 실제 코드는 볼 수 없다.[^A1kmm]
cortesoft는 반대 방향에서 의도를 읽었다.
이 실험은 AI 토큰으로 누구나 익스플로잇을 만들고 인터넷을 뒤질 수 있다는 주장에
맞서는 것이므로,
익스플로잇이 그렇게 쉽다면 그 가치도 낮아야 한다는 것이다.[^cortesoft]

wavemode와 gbingles는 이 취약점이 제로데이가 아니라고 했다.
패치가 나왔고 소스가 공개되어 있어서 감춰 둘 이유가 줄었다는
것이다.[^wavemode][^gbingles]
기록이 방어자에게 유용한지 공격자에게 유용한지는 익스플로잇이 이미 알려졌는지에
달려 있다.
알려지지 않았다면 기록은 운영자가 얻는 정보이고, 알려졌다면 새로 얻는 것이 거의
없다.

### 이 글을 읽는 방법

이 도전은 증명이 아니라 관측을 하나 만드는 장치다.
기록할 수 있는 것은 이 구성이 이 시간 동안 뚫렸는지 여부이고,
그 결과를 일반 주장으로 올리려면 구성이 대표적인지, 시도가 충분했는지, 서버가
시도를 받을 수 있었는지를 따로 확인해야 한다.

이 도전의 결과가 무엇을 말하는지는 두 관찰로 가릴 수 있다.
첫째, 지갑이 비워졌을 때 공개되는 설명에서 사용한 익스플로잇이 범용 공개
코드인지, 이 구성에 맞춰 고친 것인지 보는 것이다.
범용 코드로 뚫렸다면 PHP 서버 일반의 위험이 크다는 근거가 되고,
구성에 맞춰 고쳐야 했다면 서사와 반대로 대규모 자동화가 어렵다는 근거가 된다.
둘째, 시간이 지나도 지갑이 그대로라면 같은 구성에서 서버가 응답한 시간과 방문
수를 함께 기록하는 것이다.
시도가 많았는데도 비워지지 않았다면 미청구 시간이 의미를 얻고,
시도가 적었다면 그 시간은 아무것도 알려 주지 않는다.

---

[^hau]: <https://news.ycombinator.com/item?id=50225251>

[^akerl_]: <https://news.ycombinator.com/item?id=50225334>

[^muvlon]: <https://news.ycombinator.com/item?id=50225391>

[^akerl_-chain]: <https://news.ycombinator.com/item?id=50225761>

[^Stevvo]: <https://news.ycombinator.com/item?id=50225481>

[^echoangle]: <https://news.ycombinator.com/item?id=50225902>

[^orlp]: <https://news.ycombinator.com/item?id=50226697>

[^zoeysmithe]: <https://news.ycombinator.com/item?id=50225515>

[^cloudlandsdev-goal]: <https://news.ycombinator.com/item?id=50230070>

[^cloudlandsdev-update]: <https://news.ycombinator.com/item?id=50229699>

[^vikramkr]: <https://news.ycombinator.com/item?id=50229058>

[^paxy]: <https://news.ycombinator.com/item?id=50227364>

[^Gigachad]: <https://news.ycombinator.com/item?id=50227405>

[^nayuki]: <https://news.ycombinator.com/item?id=50225315>

[^glerk]: <https://news.ycombinator.com/item?id=50227784>

[^fwlr]: <https://news.ycombinator.com/item?id=50225617>

[^ls612]: <https://news.ycombinator.com/item?id=50226033>

[^technion]: <https://news.ycombinator.com/item?id=50225703>

[^oefrha]: <https://news.ycombinator.com/item?id=50228025>

[^jerrythegerbil]: <https://news.ycombinator.com/item?id=50225383>

[^msm_]: <https://news.ycombinator.com/item?id=50225576>

[^athrowaway3z]: <https://news.ycombinator.com/item?id=50228891>

[^xmcp123]: <https://news.ycombinator.com/item?id=50225975>

[^johanyc]: <https://news.ycombinator.com/item?id=50226826>

[^A1kmm]: <https://news.ycombinator.com/item?id=50227882>

[^cortesoft]: <https://news.ycombinator.com/item?id=50226322>

[^wavemode]: <https://news.ycombinator.com/item?id=50228609>

[^gbingles]: <https://news.ycombinator.com/item?id=50226286>
