# Ledger 하드웨어 지갑에 숨겨진 LTE 스파이 칩이 확인되었다

원문: [Ledger confirms spy chip implant behind wallet crypto thefts](https://www.bleepingcomputer.com/news/security/ledger-confirms-hardware-wallet-spy-implant-behind-crypto-thefts/)

HN 토론: <https://news.ycombinator.com/item?id=50054092> (785점, 495개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/cwota8/ledger_confirms_spy_chip_implant_behind> (35점, 11개 댓글)

GN 토론: <https://news.hada.io/topic?id=35311>

## 요약

BleepingComputer의 Bill Toulas가 2026년 10월 12일 보도한 기사다.
Ledger는 동남아시아 판매업체 CryptoBilis를 통해 유통된 일부 기기에
하드웨어 임플란트가 들어 있었고,
이것이 사용자의 암호화폐 지갑을 털었다고 확인했다.
CryptoBilis는 말레이시아에 본사를 두고
동남아 전역에서 하드웨어 지갑을 파는 대형 판매업체다.
연구자들은 9월 16일부터 Ledger 기기 안의 임플란트를 공개해 왔고,
변조된 기기는 정품의 거의 절반 가격에 팔렸다고 한다.

경과는 짧다.
Ledger는 10월 9일 자금 손실 신고에 대한 조사를
시작하며 CryptoBilis에 판매와 배송 중단을 요청했고,
다음 날 피해 사용자 기기 하나에서 승인되지 않은 하드웨어 임플란트를 확인했다.
이후 예기치 않은 자금 유출 신고가 모두 CryptoBilis가 판 기기와 연결되며,
영향 규모는 “제한적”이라고 밝혔다.
Ledger는 이 판매업체에서 산 기기를 아직 설정하지 않았다면 설정하지 말고,
이미 설정했다면 새 시드로 만든 새 Ledger 서명 기기로 자산을 옮기라고 권했다.

임플란트의 구조는 외부 연구자들이 밝혔다.
Mt. Gox 전 CEO이자 현재 Karpeles Lab Inc.를 이끄는 Mark Karpelès는
화면 뒤에 숨긴 새 임플란트 사진을 공개하며,
손으로 납땜한 이전 버전에서 “상당히 진화했다”고 했다.
그에 따르면 임플란트는 기기의 화면 출력과
버튼 입력을 가로채 시드 문구를 알아내고,
eSIM을 이용한 LTE 연결로 공격자에게 보냈다.
암호화폐 연구 스튜디오 Tibane Labs는 임플란트 변종 두 개를 구했는데,
하나는 Amazon Japan의 “중국 판매자, 말레이시아 발송” 상품이었고
다른 하나는 Yahoo! 옥션 재팬에서 산 것이었다.

첫 번째 변종은 원래 배터리를 더 작은 것으로 바꿔 공간을 만들었고,
그 배터리가 임플란트와 지갑에 함께 전원을 댔다.
배터리와 안테나 밑에는
ST STM32G431KBU6(Arm Cortex-M4, 128KB 플래시) 마이크로컨트롤러가,
그 옆에는 2×2mm의 8핀 eSIM과 차폐된 LTE 모듈이 있었다.
두 번째 변종은 MCU와 eSIM의 부품 번호를 긁어 지웠고,
원래 배터리를 그대로 쓰며 OLED 화면 아래 폼 패딩 자리에 들어갔다.
두 경우 모두 결정적인 단서는 안테나 선이었다.
연구자들은 이 임플란트가 손으로 만든 일회성 장치가 아니라
기판 업체에 주문한 설계된 플렉스 PCB라고 경고했다.

Ledger는 비공인 판매업체에서 사지 말라고 권하고,
공인 판매업체에는 공식 경로로만 제품을 받고
반품 제품을 재입고하지 말라고 당부했다.
Ledger의 정품 확인(Genuine Check)은 원래의 보안 요소(Secure Element)가 그대로면
추가된 임플란트를 탐지할 수 없다고 회사 스스로 밝힌다.
다른 판매업체에서 변조 기기가 나왔다는 징후는 아직 없지만,
판매업체 망에 대한 신뢰가 무너져 그 망을 해체하라는 목소리가 커졌다.

## 분석

### 공격자는 보안 요소를 깨지 않고 그 바깥을 노렸다

하드웨어 지갑의 보안 모델은 개인 키를 보안 요소 안에 가두는 데 있다.
이 공격은 그 칩을 한 번도 건드리지 않았다.
시드 문구는 처음 설정할 때 화면에 표시되고 사용자가 버튼으로 확인하므로,
화면과 버튼 사이의 신호만 엿보면 된다.
보안 요소가 아무리 단단해도 사람이 읽고 입력하는 경로는 보호 범위 밖이었다.

HN의 megous는 보안 요소를 해킹하는 대신 화면으로 가는 출력을 엿보는 기법이 감탄스럽다고 했고,[^megous]
userbinator는 같은 기법이 원래 컴퓨터 연결 기능이
없는 저울이나 디지털 마이크로미터의 표시를
읽는 데 흔히 쓰인다고 덧붙였다.[^userbinator]
새로운 기술이 아니라, 오래된 계측 기법을 가장 값비싼 표적에 적용한 것이다.
Lobste.rs의 jbe_도 화면에 시드가 표시될 때 엿볼 수 있다면 보안 요소를 뚫을 필요가 없다며
상당히 정교한 공급망 공격이라고 평했고,
어떤 분석 글에 따르면 Ledger가 3월부터 이를 알고 있었다고 덧붙였다.[^jbe_]
이 주장은 기사에서 확인되지 않는다.

역설적으로 화면은 하드웨어 지갑의 핵심 장점이다.
Lobste.rs의 krtab은 Yubikey와 달리 하드웨어 지갑은 서명할 거래를 기기 자체 화면에 보여 주므로,
감염된 컴퓨터가 한 거래를 보여 주고 다른 거래를
서명하게 하는 공격을 막는다고 설명했다.[^krtab]
Irene은 그 장점이 공격 면을 크게 늘리는 대가로 온다고 답했다.[^Irene]
이번 공격은 바로 그 화면을 통로로 썼다.

### 정품 확인은 무엇을 보증하고 무엇을 보증하지 않는가

Ledger의 Genuine Check는 보안 요소가 진짜인지를 확인한다.
이번 임플란트는 보안 요소를 그대로 둔 채 옆에 붙었으므로 이 확인을 통과한다.
사용자는 “정품 확인 통과”를 기기 전체가 안전하다는 뜻으로 읽기 쉽지만,
실제 보증 범위는 칩 하나다.
회사가 이 한계를 스스로 밝힌 것은 정직하지만,
그 말은 곧 사용자가 기기 안을 직접 열어 보지 않는
한 변조를 알 방법이 거의 없다는 뜻이기도 하다.

HN의 csomar는 최근 90일 안에 바로 이 판매업체에서 산 Stax를 칼로 열어 보니 임플란트가 있었다고 썼다.
YouTube 영상을 보지 않았다면 원래 Ledger 하드웨어의 일부로
여겼을 만큼 잘 만들어졌다고 했다.[^csomar]
변조가 정교할수록 사용자의 육안 검사는 무력해진다.

### 공급망 공격의 경제학이 바뀌었다

맞춤 플렉스 PCB, 소형 LTE 모듈, eSIM을 갖춘 임플란트는 싸지 않다.
HN의 Neywiny는 처음에는 하드웨어 임플란트가 너무 비싸서 실제로 할 리 없다고 생각했지만,
수천만 달러를 훔칠 수 있다면 전용 칩을 만들어도 남는다고 적었다.[^Neywiny]
TacticalCoder는 “이론적”이거나 “편집증 환자의 상상”으로
불리던 공격이 실제로 일어났다고 정리했고,[^TacticalCoder]
nostrademons는 돈이 걸리면 상상할 수 있는 모든 공격이
시도된다며 이를 금전적 동기의 힘으로 설명했다.[^nostrademons]
하드웨어 지갑은 “여기에 돈이 있다”고 알리는 장치이므로,
공격 비용이 아무리 커도 표적 하나당 기대 수익이 그보다 크다.

## 비평

### 기사는 피해 규모와 기기 모델을 흐린 채 남긴다

기사는 Ledger가 영향 규모를 “제한적”이라고
했다는 말만 전하고 숫자를 주지 않는다.
변조된 기기 모델도 Ledger는 밝히지 않았고,
기사 본문은 Karpelès의 사진을 근거로 Ledger X와 Ledger Nano X를 섞어 부른다.
HN에서는 9,200만 달러, 1억 달러 같은 피해액이 오갔지만 기사에는 근거가 없다.[^Neywiny][^chinathrow]
csomar의 증언대로 Stax에서도 나왔다면 피해 모델은 더 넓다.[^csomar]
독자가 자기 기기가 위험한지 판단하는 데 필요한 정보는 아직 공개되지 않았다.

### “공인 판매처에서만 사라”는 권고의 전제가 흔들린다

Ledger의 첫 권고는 비공인 판매업체를 피하라는 것이다.
그런데 CryptoBilis는 동남아의 대형 판매업체였고,
HN의 cowlevel은 독일의 대형 가전 매장 MediaMarkt도 변조 기기를 진열대에서 팔았다고 주장했다.[^cowlevel]
mikeryan은 평판 좋은 판매업체(CryptoBilis)가
인수된 뒤 판매망에서 지갑이 변조된 것으로 이해한다며,
이것은 Ledger의 잘못이 아니라 문자 그대로의 공급망 문제라고 반박했다.[^mikeryan]
두 주장 모두 기사로는 확인되지 않지만,
어느 쪽이든 사용자가 판매처의 진위를 가려낼 수단은 많지 않다.
Ledger가 판매업체에 반품 재입고를 하지 말라고 당부한 것은,
판매망 내부에서도 변조가 일어날 수 있음을 인정한 것으로 읽힌다.

### 하드웨어 지갑이 자기 보관의 답이라는 전제

HN의 ArtTimeInvestor는 부품 공급망, 제조사 직원, 제조사의 실수, 배송, 사용자의 실수까지
잘못될 수 있는 것을 나열하면 하드웨어 지갑은
자기 보관의 해법이 아니라고 했다.[^ArtTimeInvestor]
akoboldfrying는 같은 위협 분석이 은행 앱을 쓰는
노트북과 휴대폰에도 적용된다고 반박했다.[^akoboldfrying]
redox99는 왜 사람들이 전용 하드웨어를
범용 하드웨어보다 안전하다고 여기는지 모르겠다며,
하드웨어 지갑은 기성 Intel이나 AMD CPU보다 훨씬 백도어가
심어지기 쉽다고 했다.[^redox99]
jmyeet은 전용 기기가 이론적으로 공격 면이 작다는
장점이 있다며 이는 트레이드오프라고 답했다.[^jmyeet]
기사는 이 논쟁에 들어가지 않지만,
이번 사건은 “전용 기기라서 안전하다”는 믿음이
기기의 공급망 신뢰에 기대고 있었음을 드러낸다.
Lobste.rs의 flockofbirbs는 복사할 수 없다는 패스키도 비슷한 방식으로 복사될 수 있다며
이 공격이 최근의 패스키 논쟁과 맞물린다고 봤다.[^flockofbirbs]

## 인사이트

### 신뢰의 단위가 칩에서 경로로 바뀐다

보안 요소가 완벽해도 기기가 사용자 손에 오기까지의 경로가 깨지면 소용없다.
반도체 공급망 보안에서 오래 다뤄 온 문제가
수십만 원짜리 소비자 기기 하나에서 그대로 재현되었다.
앞으로 하드웨어 지갑 제조사는 칩의 진위만이 아니라
배송 상자, 봉인, 무게, 내부 사진 같은 “경로의 증거”를 사용자에게 줘야 한다.
HN의 jacquesm이 기기가 들어 있을 때와 없을 때의 무게를 공개했어야 한다고 한 것도 같은 방향이다.[^jacquesm]

### 변조 방지와 검사 가능성은 서로 부딪힌다

jacquesm은 하드웨어 키에 빈 공간을 남기지 말고
전체를 에폭시로 채우라고 했고,[^jacquesm]
olalonde도 에폭시 포팅이나 열면 보드를
태우는 능동 변조 대응을 제안했다.[^olalonde]
swinglock은 그것이 변조 비용을 높이지만
1억 달러의 보상 앞에서는 충분히 비싸지 않고,
동시에 사용자가 내부를 검사하는 것을
사실상 불가능하게 만든다고 지적했다.[^swinglock]
csomar처럼 칼로 열어 임플란트를 찾는 일이
가능했던 것은 기기가 열 수 있게 만들어졌기 때문이다.
기기를 단단히 봉인할수록 공격은 어려워지지만,
공격이 성공했을 때 사용자가 알아챌 길도 사라진다.

### 여러 공급자로 나누는 것이 단일 기기를 믿는 것보다 낫다

HN의 Freeaqingme는 서로 다른 제조사의 하드웨어 지갑 여러 개로 다중 서명 지갑을 만드는 것이
자기 보관의 최선이라고 봤다.[^Freeaqingme]
thinkmassive는 m-of-n 구성이 보안과 중복을 함께 준다며,
2-of-3이면 키 하나를, 3-of-5면 둘을 잃어도 된다고 설명했다.[^thinkmassive]
이번 공격은 한 판매업체의 한 제조사 기기를 노렸다.
서로 다른 경로로 온 여러 기기가 동시에 변조될 확률은 훨씬 낮으므로,
다중 서명은 공급망 공격에 대한 가장 현실적인 완화책이다.
대가는 복잡성이고, 그 복잡성이 사용자의 실수를 부른다는 점이 남는다.

---

[^megous]: <https://news.ycombinator.com/item?id=50069899>

[^userbinator]: <https://news.ycombinator.com/item?id=50081913>

[^csomar]: <https://news.ycombinator.com/item?id=50078739>

[^Neywiny]: <https://news.ycombinator.com/item?id=50054525>

[^TacticalCoder]: <https://news.ycombinator.com/item?id=50046048>

[^nostrademons]: <https://news.ycombinator.com/item?id=50078030>

[^chinathrow]: <https://news.ycombinator.com/item?id=50070813>

[^cowlevel]: <https://news.ycombinator.com/item?id=50069828>

[^mikeryan]: <https://news.ycombinator.com/item?id=50070479>

[^ArtTimeInvestor]: <https://news.ycombinator.com/item?id=50054330>

[^akoboldfrying]: <https://news.ycombinator.com/item?id=50054508>

[^redox99]: <https://news.ycombinator.com/item?id=50079849>

[^jmyeet]: <https://news.ycombinator.com/item?id=50082289>

[^jacquesm]: <https://news.ycombinator.com/item?id=50069374>

[^olalonde]: <https://news.ycombinator.com/item?id=50064240>

[^swinglock]: <https://news.ycombinator.com/item?id=50078473>

[^Freeaqingme]: <https://news.ycombinator.com/item?id=50054640>

[^thinkmassive]: <https://news.ycombinator.com/item?id=50070518>

[^jbe_]: <https://lobste.rs/s/cwota8/ledger_confirms_spy_chip_implant_behind#c_2yrobv>

[^krtab]: <https://lobste.rs/s/cwota8/ledger_confirms_spy_chip_implant_behind#c_vhd2be>

[^Irene]: <https://lobste.rs/s/cwota8/ledger_confirms_spy_chip_implant_behind#c_8jlt8i>

[^flockofbirbs]: <https://lobste.rs/s/cwota8/ledger_confirms_spy_chip_implant_behind#c_5wom6x>
