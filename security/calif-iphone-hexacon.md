# Calif가 Hexacon에서 iPhone 18 Pro 공격 시연 영상 4개를 공개했다

원문: [iPhone - Calif Newsletter](https://blog.calif.io/p/iphone)

HN 토론: <https://news.ycombinator.com/item?id=50211474> (750점, 510개 댓글)

GN 토론: <https://news.hada.io/topic?id=35877>


## 요약

보안 회사 Calif의 뉴스레터에 2026년 10월 16일에 올라온 짧은 글이다.
본문은 “오늘 우리는 해킹하려던 것을 해킹했다. iPhone이다”라는 문장으로 시작하고,
파리 Hexacon에서 같은 날 공개한 시연 영상 시리즈를 소개하며 모든 것은 때가 되면
공개하겠다고 한다.
이 글에는 기술 설명이 없고 영상 네 개가 전부다.
영상 제목과 길이는 다음과 같다.

| 번호 | 영상 제목                               | 길이 |
| ---- | --------------------------------------- | ---- |
| 1    | Signal 1-click exploit on iPhone 18 Pro | 33초 |
| 2    | iMessage 1-click on iPhone 18 Pro       | 20초 |
| 3    | Can you iPhone do this?                 | 91초 |
| 4    | iPhone 18 Pro Persistent Jailbreak      | 43초 |

글의 소제목은 각각 Signal에서의 1클릭, 모두가 쓰는 iMessage에서는 어떠냐는 물음,
당신의 iPhone이 이런 것을 할 수 있느냐, 그리고 APT가 Apple Persistent Threat의
약자라는 농담이다.
이 문서는 영상을 보지 못했고 제목과 길이만 확인했으며, 글 본문에는 이를 보충하는
설명이 없다.
HN 댓글에서 영상 내용을 본 사람들이 전한 바로는 메시지로 보낸 PDF를 열면 코드가
실행되는 사슬 두 개(iMessage와 Signal)와 휴대폰을 탈취하는 앱, 그리고 재부팅
뒤에도 살아남는 지속성이 보인다고 한다.
이 문서는 그 서술을 댓글의 요약으로만 전하며, 공격이 어떻게 작동하는지는 다루지
않는다.

## 분석

### 글의 중심 주장: 최신 하드웨어에서 공개 전 시연으로 능력을 증명한다

글의 정보량은 모델이 기기를 해킹했다는 사실 자체다.
어떤 취약점이고 어떤 버전에서 통하며 어떤 조건(1클릭)이 필요한지는 글에 없다.
Calif는 모든 것을 때가 되면 공개하겠다고 하고, 시연 영상의 제목만이 대상(iPhone
18 Pro)과 방식(1클릭, 지속적 탈옥)을 말한다.
이 구조는 학회 발표와 함께 공개하는 시연이 취약점의 존재를 알리는 신호로 쓰이는
전형적인 방식이다.

### 시연 형식의 정보 격차가 토론을 만들었다

영상이 보여 주는 것은 결과(기기가 탈취된 상태)이고 원인은 공개되지 않았다.
이 격차 때문에 HN에서는 무엇을 시연한 것인지부터 설명을 요구하는 질문이 나왔다.
nsxwolf는 영상들이 실제로 무엇을 보여 주느냐고 물었고, ks2048은 왜 영상 대신
말로 하지 않느냐고, 악성 PDF가 열리면 무엇에 접근하는지, 어느 iOS 버전과
기기인지 물었다.[^nsxwolf][^ks2048]
jeroenhd는 iMessage와 Signal에서 PDF를 통한 코드 실행 사슬 두 개, 휴대폰을
루팅하는 앱, 그리고 재부팅 뒤에도 남는 악성코드라는 요약을 달았고, 지속성은
메모리에만 있는 공격보다 어렵다고 덧붙였다.[^jeroenhd-summary]
이 서술은 영상을 본 사람의 해석이며 이 문서가 확인한 것이 아니다.

## 비평

### 책임 있는 공개를 둘러싼 공방이 가장 큰 쟁점이다

eyalitki는 아직 패치되지 않은 취약점을 시연하는 가치가 무엇이냐고 물었고, 책임
있는 공개 절차를 무시한다고 비판했다.[^eyalitki]
Calif 측으로 보이는 cryptbe는 이 체인에 쓰인 버그 대부분을 Apple에 공개했고
나머지도 공개할 것이라고 답했다.[^cryptbe]
creata는 시연이 방법을 거의 드러내지 않았으며 첫 단계가 PDF라는 것과 몇 가지
단서 외에는 공개된 것이 없으므로 무책임한지 의문이라고 했다.[^creata]
cryptbe의 답이 Calif의 공식 입장인지, 이 글의 작성자와 같은 사람인지 이 문서는
확인하지 못했다.
핵심 사실(Apple에 얼마나 공개했는지, 패치 상태)은 스레드의 주장이며 독립적으로
확인되지 않았다.

### 영상만으로는 검증할 수 없다

suralind는 이것이 실제인지 모르겠지만 실제라면 이번 주가 믿기 어렵다고
했다.[^suralind]
공개 영상은 기기 화면의 시연이며 재현물이나 기술 보고서가 없다.
글이 때가 되면 공개하겠다고 한 것은 검증을 미룬 것이고, 그때까지의 판단은 회사의
신뢰도에 기댄다.
jeroenhd가 이 요약을 단 근거도 영상 관찰이다.

### 지속 탈옥의 의미는 영상 설명만으로 가려지지 않는다

drum55는 영상이 사용자 영역 공격이지 부트롬이 아니라는 것을 시사하고
업데이트하지 말라고 안내하는 것이 공격 표면을 확인해 준다고 추정했다.[^drum55]
aseipp는 보안 부팅과 업그레이드 체인을 깨려면 SecureROM 공격과 Secure Enclave
침해가 필요하므로 업데이트로 고쳐질 것이 거의 확실하고, 인터넷의 보도가 이
영상의 공격을 untethered로 서술하는 것은 매우 드문 일이라고 했다.[^aseipp]
이 두 해석은 추측이며 모순되지 않지만, 영상 외의 정보가 없다는 점에서 확정이
아니다.

## 인사이트

### 공격 능력의 접근성이 연구자 공동체의 구조를 바꾼다

jinseokim은 프런티어 연구소가 레드팀 접근을 내부 서클에만 주기 때문에 바깥의
보안 연구자들이 이 파티에 낄 수 없고, 신뢰된 사이버 접근 프로그램이 안전장치가
아니라 해자가 됐다고 했다.[^jinseokim]
ipsum2는 중국 오픈소스 모델로도 많은 것을 할 수 있다고 답했다.[^ipsum2]
앞서 이 저장소의 `llm/kimi-k3-1-pro.md`가 다룬 Kimi K3.1 Pro의 사이버 능력 제어
논의와 이어지는 논점이다.
능력 접근이 소수에게 있을 때 방어 연구도 소수에게 집중되고, 능력이 퍼지면 반대로
공격이 퍼진다는 긴장이 여기서 드러난다.
이 연결은 이 문서의 해석이며 Calif의 글은 모델의 역할을 언급하지 않는다.

### 설계의 쟁점은 첨부 파일 해석기의 공격 표면이다

aemoron은 PDF가 반복되는 이유를 물었고 motoboi는 공격 표면이 크고 피해자가 열
가능성이 높은 신뢰된 형식이라고 답했다.[^aemoron][^motoboi]
drum55는 PDF가 사실상 실행 파일이라고 설명했고, ethin은 안전한 언어도 PDF의
자바스크립트와 이미지 지원 때문에 문제를 해결하지 못한다고
했다.[^drum55-pdf][^ethin]
sigmoid10은 이것이 제로클릭이 아니라 1클릭이므로 모르는 파일을 열지 않는 것이
가장 좋은 방어라고 했고, 잠금 모드(Lockdown Mode)는 메시지 첨부 파일 상당수를
막아 안전한 편이지만 대부분의 사용자에게는 너무 제한적이라고 했다.[^sigmoid10]
이 논의는 이 영상의 사슬에 대한 것이 아니라 일반론이며, 영상의 구체적 공격
경로는 공개되지 않았다.

### 이 글을 읽는 방법

이 글은 기술 문서가 아니라 예고이며, 판단에 필요한 정보는 이후 공개될 문서에
있다.
실용적으로 할 수 있는 일은 기기와 앱을 최신 상태로 유지하고, 모르는 사람이 보낸
첨부 파일을 열지 않으며, 위험이 큰 사용자는 잠금 모드를 검토하는 것이다.
이 글의 주장을 가를 관찰은 두 가지다.
Calif가 약속한 기술 공개가 나오는지와 그 공개가 패치 이후인지, 그리고 Apple이 이
영상의 사슬을 인정하고 패치하는지다.
둘 다 이 시점에는 확인되지 않는다.

---

[^nsxwolf]: <https://news.ycombinator.com/item?id=50211882>

[^ks2048]: <https://news.ycombinator.com/item?id=50212763>

[^jeroenhd-summary]: <https://news.ycombinator.com/item?id=50212458>

[^eyalitki]: <https://news.ycombinator.com/item?id=50215015>

[^cryptbe]: <https://news.ycombinator.com/item?id=50215848>

[^creata]: <https://news.ycombinator.com/item?id=50215078>

[^suralind]: <https://news.ycombinator.com/item?id=50211599>

[^drum55]: <https://news.ycombinator.com/item?id=50211806>

[^aseipp]: <https://news.ycombinator.com/item?id=50212037>

[^jinseokim]: <https://news.ycombinator.com/item?id=50214848>

[^ipsum2]: <https://news.ycombinator.com/item?id=50214864>

[^aemoron]: <https://news.ycombinator.com/item?id=50212216>

[^motoboi]: <https://news.ycombinator.com/item?id=50212319>

[^drum55-pdf]: <https://news.ycombinator.com/item?id=50211856>

[^ethin]: <https://news.ycombinator.com/item?id=50212940>

[^sigmoid10]: <https://news.ycombinator.com/item?id=50213155>
