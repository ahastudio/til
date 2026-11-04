# 프라이버시를 지키는 TV를 고르는 답은 제품이 아니라 TV를 네트워크에서 떼어 내고 화면으로만 쓰는 것이다

Ask HN: [Ask HN: Which TV do you recommend for privacy?](https://news.ycombinator.com/item?id=50328896)

## 요약

질문자는 몇 년간 TV 없이 지냈고, 프라이버시를 존중하는 TV를 원한다고 쓴다.
조건은 60~80인치, 4K, 60Hz 이상이며 프리미엄 가격은 감수한다.
Apple TV가 TV에 내장된 앱보다 낫다고 들었는데, TV를 Apple TV의 디스플레이로만
쓰고 싶고
Apple TV와 더 잘 맞는 TV가 있는지 묻는다.

스레드에서 가장 많이 반복된 답은 제품 추천이 아니라 방법이다.
TV를 인터넷에 연결하지 않고, 내장 앱을 쓰지 않으며, HDMI로 믿을 수 있는 기기를
연결한다는 것이다.
epwr는 조사해 보니 어느 TV 브랜드도 프라이버시 면에서 나은 곳이 없었다며
LG TV를 Wi-Fi에 연결하지 않고 Apple TV로 본다고 쓴다.
HDMI CEC를 지원하는지 확인하라는 조언을 붙인다.[^epwr]

기기 쪽 선택지는 여러 갈래로 갈렸다.
realityfactchex는 TV를 열어 무선 모듈을 메인보드에서 분리하고,
내장 앱을 쓰지 말고 이더넷을 꽂지 말고, 믿는 기기를 HDMI로 연결하라고
한다.[^realityfactchex]
kitestramuort와 lrvick는 중고 Intel NUC에 Kodi나 Linux를 올려 쓴다고
한다.[^kitestramuort][^lrvick]
mullingitover는 Apple TV를 쓰지 말고 15년째 Mac Mini를 TV에 연결해 쓴다고
한다.[^mullingitover]
디지털 사이니지(digital signage)나 상업용 모니터는 스마트 기능이 없는 대안으로
여러 번 나온다.
pyrophane와 mlsu는 프로젝터를 권했다.[^pyrophane][^mlsu]

한편 LG를 사서 루팅(rooting)하자는 의견도 가장 많은 답글을 받았다.
MegaDeKay는 LG OLED를 사서 루팅하고 Glasshouse로 텔레메트리를 끄라고 하며,
LG가 최근 취약점을 막아 2026-10-10 이후 펌웨어는 피해야 한다고 쓴다.[^MegaDeKay]

## 분석

### 답의 구조는 연결을 끊는 것에서 시작해 얼마나 더 갈지로 갈린다

거의 모든 답이 TV를 네트워크에 연결하지 않는다는 데서 시작한다.
차이는 그 위에 무엇을 더하느냐다.
가장 가벼운 쪽은 연결하지 않고 외부 기기를 쓰는 것이고,
무선 모듈을 물리적으로 떼는 것(realityfactchex, drnick1), 라우터에서 TV의
트래픽을 막는 것(thinkingkong)이 이어진다.[^thinkingkong]
가장 무거운 쪽은 TV의 펌웨어를 직접 바꾸는 루팅이다.
이 해석은 스레드의 답변을 이 문서가 정리한 것이다.

### 믿을 대상이 TV 제조사에서 HDMI 기기로 옮겨 간다

realityfactchex는 TV를 디스플레이로만 두고 HDMI 쪽 기기를 내가 믿는 상자로
정한다고 설명한다.[^realityfactchex]
kempbellt는 이때 신뢰의 문제가 Apple을 얼마나 믿느냐로 옮겨 간다고
쓴다.[^kempbellt]
drnick1은 Samsung, LG, Google을 Apple이나 Amazon으로 바꾸면 프라이버시 쪽으로는
나아진 것이 없다고 한다.[^drnick1]
이는 질문자의 Apple TV 전제에 대한 직접적인 반론이다.

### 연결하지 않는 것만으로 충분한지를 두고 가장 큰 논쟁이 났다

pier25는 왜 무선 모듈까지 떼느냐고 묻는다.
sudonem은 연결하지 않아도 TV가 공개 네트워크를 계속 찾고 주변 기기에 응답을
요구한다고 답하고,
MiscCompFacts는 비밀번호 없는 공개 접속점에는 TV가 허락 없이 붙는다고 들었다고
한다.[^sudonem][^MiscCompFacts]
kazinator는 Wi-Fi 비밀번호를 주지 않는 것으로 부족한 이유를 묻고,
꺼 둔 TV가 몰래 다시 연결되면 공유기에서 막거나 비밀번호를 바꾸면 되지 않느냐고
한다.[^kazinator]
이 문서는 TV가 공개 네트워크에 허락 없이 접속한다는 주장을 확인하지 못했고,
댓글들의 주장으로만 적는다.

## 비평

### 스레드의 주장 대부분은 개인 경험이고 검증이 없다

공개 접속점에 붙는다는 주장, 몰래 데이터를 쌓았다가 내보낸다는 주장(eecc)은 근거
링크가 없다.[^eecc]
LG의 어떤 펌웨어 날짜 이후 루팅이 막혔다는 주장도 한 사람의 서술이다.
이 문서는 이들 가운데 어느 것도 TV 쪽에서 확인하지 못했다.
연결하지 않으면 된다는 합의가 강한 것은 위험을 줄이는 방법으로서 값이 싸기
때문이지, 위험이 측정되었기 때문은 아니다.

### 연결하지 않는 방법이 막히는 사례가 있다

mrandish는 Vizio TV가 몇 번 켜질 때까지 오프라인이면 Wi-Fi 설정 절차로 강제로
이끌고,
공장 초기화 외에는 이 카운터가 지워지지 않는다고 쓴다.
설정 절차는 리모컨으로 세 번 눌러 넘길 수 있지만 약 열 번 켤 때마다 반복되고,
외부 HDMI 입력은 켜진 뒤 수동으로 다시 골라야 한다고도 한다.[^mrandish]
bscphil은 비싼 TV를 사고 나서 홈 화면에 사전 설치된 광고나 연결 요구가 뜨는 것이
견딜 수 없을 것 같다고 한다.[^bscphil]
연결하지 않는 전략은 제조사가 그 경우를 막지 않는다는 가정 위에 있다.

### 루팅과 설치형 방법은 보증과 안전성의 비용이 있다

andrewla는 루팅이 과하다며 인터넷에 연결하지 않고 HDMI1로 부팅시키고 Hotel
Mode로 고정하면 된다고 반박한다.[^andrewla]
goobatrooba는 루팅 절차가 웹사이트에 IP와 취약한 TV 버전을 알려 주는 것이라
봇넷(botnet)에 초대하는 것이 아니냐고 묻고,
serf는 취약점을 이용하려고 비싼 장비를 사는 것은 나쁜 생각이고 제조사에 돈을
주는 것이라고 쓴다.[^goobatrooba][^serf]
이 문서는 Glasshouse나 루팅 가이드를 열어 보지 않았으므로 그 절차의 안전성은
판단하지 못한다.

### 구매 질문에 대한 답이 되었는지는 불분명하다

질문자는 어떤 TV를 고르느냐고 물었고, 많은 답이 어느 TV든 상관없다고 답한다.
그러나 같은 스레드에서 Vizio 사례나 LG의 반복되는 언급은 브랜드와 모델에 따라
연결하지 않는 조건의 감당 비용이 다르다는 것을 보여 준다.
디지털 사이니지를 추천한 의견들은 모델명을 들었지만,
Barbing이 제시한 Samsung QB55C-N은 1,050달러 55인치 상업용 모니터이고 TV로서의
단점이 있는지 묻는다.[^Barbing]

## 인사이트

### 선택 기준은 브랜드가 아니라 연결을 끊었을 때 유지되는 기능이다

스레드가 보여 주는 실제 구매 기준은 세 가지다.
HDMI CEC가 되는지, 무선 없이도 리모컨이 동작하는지, 연결 없이도 설정 화면에
갇히지 않는지.
epwr는 LG에 Apple TV를 쓰면 게임 콘솔로 입력을 바꿀 때 Apple TV가 TV 입력을
제어하지 못해 불편하다고 쓴다.[^epwr]
kempbellt는 무선을 완전히 없애면 BLE(저전력 블루투스) 리모컨이 안 되는 부작용이
있다고 쓴다.[^kempbellt]
이 조건들은 사기 전에 해당 모델의 사용자 후기에서 확인할 항목이다.
이것은 이 문서의 구매 제안이다.

### 스레드가 놓친 질문은 HDMI 기기의 프라이버시다

질문자의 전제인 Apple TV 자체의 신뢰에 대한 반응은 갈렸고,
gargs는 Apple TV가 더 프라이버시 친화적일 수 있어도 그 위에 설치하는 스트리밍
앱까지 믿을 이유는 없다고 쓴다.[^gargs]
TV를 디스플레이로 두면 프라이버시 문제는 TV 제조사에서 HDMI 기기와 그 위의
앱으로 옮겨 가는 것이지 사라지는 것이 아니다.

### 이 방법을 확인하는 관찰

TV를 설치하고 한 주 동안 공유기의 DNS 질의 기록에서 그 TV의 MAC 주소로 나가는
요청을 본다.
연결하지 않은 상태에서 요청이 없고(와이파이를 끈 경우) 공개 접속점에 붙지
않는다면 스레드의 우려는 해당 모델에서는 해당하지 않는다.
요청이 있다면 무선 모듈 분리나 상업용 모니터 같은 더 강한 방법의 이유가 된다.

---

[^epwr]: <https://news.ycombinator.com/item?id=50329201>

[^realityfactchex]: <https://news.ycombinator.com/item?id=50330810>

[^kitestramuort]: <https://news.ycombinator.com/item?id=50334611>

[^lrvick]: <https://news.ycombinator.com/item?id=50329648>

[^mullingitover]: <https://news.ycombinator.com/item?id=50329658>

[^pyrophane]: <https://news.ycombinator.com/item?id=50329491>

[^mlsu]: <https://news.ycombinator.com/item?id=50333461>

[^MegaDeKay]: <https://news.ycombinator.com/item?id=50332515>

[^thinkingkong]: <https://news.ycombinator.com/item?id=50329595>

[^kempbellt]: <https://news.ycombinator.com/item?id=50331572>

[^drnick1]: <https://news.ycombinator.com/item?id=50330815>

[^sudonem]: <https://news.ycombinator.com/item?id=50331080>

[^MiscCompFacts]: <https://news.ycombinator.com/item?id=50331082>

[^kazinator]: <https://news.ycombinator.com/item?id=50331520>

[^eecc]: <https://news.ycombinator.com/item?id=50337511>

[^mrandish]: <https://news.ycombinator.com/item?id=50331474>

[^bscphil]: <https://news.ycombinator.com/item?id=50331305>

[^andrewla]: <https://news.ycombinator.com/item?id=50337330>

[^goobatrooba]: <https://news.ycombinator.com/item?id=50334431>

[^serf]: <https://news.ycombinator.com/item?id=50333406>

[^Barbing]: <https://news.ycombinator.com/item?id=50332351>

[^gargs]: <https://news.ycombinator.com/item?id=50334540>
