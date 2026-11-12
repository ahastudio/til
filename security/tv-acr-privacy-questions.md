# TV 제조사 11곳에 던진 17개 질문: 7곳만 답했고 답변은 서로 어긋났다

원문: [I asked every TV manufacturer 17 questions about how they spy on you](https://www.theverge.com/tech/1012372/tv-privacy-acr-questions)

HN 토론: <https://news.ycombinator.com/item?id=50453474> (337점, 233개 댓글)

GN 토론: <https://news.hada.io/topic?id=36994>

## 요약

The Verge의 TV·오디오 선임 리뷰어 John Higgins는 2026년 11월 11일 글에서, LG가
TV로 사용자를 감시했다는 의혹이 불거진 뒤 다른 회사들이 무엇을 수집하고 어떻게
보호하는지 직접 물었다고 밝힌다.
그는 한 달 전에 Amazon, Apple, Google, Hisense, LG, Panasonic, Roku, Samsung,
Sony, TCL, Walmart의 Vizio 등 11곳에 예/아니오로 답할 수 있는 17개 질문을
보냈다.
개인정보 처리방침 링크로 얼버무리지 못하게 하려고 질문을 “녹음된 음성이나 그
전사본을 TV가 저장하는가” 같은 형태로 만들었다고 한다.

답변한 회사는 Amazon, Apple, Google, LG, Roku, Samsung, TCL 7곳이다.
Hisense는 다섯 번의 연락에도 응답하지 않았고, Panasonic, Sony, Vizio는 글에 실린
17개 질문 모두에 “답을 주지 않았다”고 표시된다.
Apple은 호출어와 영상 수집, 삭제 같은 일부 질문에만 답했고 나머지는 직접 답하지
않았다.
TCL도 몇몇 질문에는 직접 답하지 않았다.
글쓴이는 상위 TV 제조사 세 곳과 주요 스트리밍 기기 회사의 답을 확보했다고
말한다.
글은 회사별 답을 질문마다 나란히 싣는다.

글의 배경 설명은 다음과 같다.
- 많은 TV가 자동 콘텐츠 인식(ACR, automatic content recognition)으로 시청 내용을
  파악해 맞춤 광고, 시청 지표, 추천에 쓴다.
- 설정 과정의 동의 절차 때문에 필수처럼 보이지만 보통 동의 후에도 ACR을 끌 수
  있다.
- 다만 끄기가 충분하지 않을 수 있다.
노스이스턴 대학교의 최근 연구에서 Vizio는 끈 뒤에도 데이터를 계속 보냈고(Vizio는
  “일상 운영 데이터”이며 ACR이 아니라고 답했다), Samsung과 Roku는 트래픽이
  제한되었지만 완전히 멈추지는 않았다고 한다.

질문별 핵심 답변은 다음과 같다(글에 실린 회사의 진술이며 이 문서가 검증한 것은
아니다).

| 질문                                 | 주요 답변                                                                                                                                                                                                                                                   |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. 마이크로 집 안 소리를 듣나        | Amazon, Apple, Google, LG, Roku, Samsung은 호출어나 버튼을 누를 때만 작동한다고 했다. TCL은 제3자 OS가 통제한다고 했다                                                                                                                                      |
| 2~3. 음성이나 전사본의 저장과 전송   | Google은 음성·오디오 활동을 켠 경우에만 저장한다고 했다. LG는 옵트인 후 호출하면 서버로 보낸다고 했다. Samsung은 서버에 요청 처리용으로 저장한다고 했다                                                                                                     |
| 4. 스크린샷이나 영상 녹화 수집       | Amazon, Apple, Google, LG, Roku, Samsung이 부인했다. LG는 TV 내부 사운드보드에서 만든 오디오 지문으로 콘텐츠를 식별한다고 했다                                                                                                                              |
| 5~6. 시청 내용과 클릭 텔레메트리     | Amazon, Google, LG, Roku, Samsung이 사용 정보를 수집한다고 답했다. LG는 시선 추적은 하지 않는다고 했다                                                                                                                                                      |
| 7~9. 위치와 개인 식별 정보           | 대부분 공인 IP를 전송한다고 했다. Google은 SSID까지 쓴다고 답했고, LG는 ACR을 켜면 주변 Wi-Fi 정보로 대략적 위치를 추정한다고 했다                                                                                                                          |
| 10. 같은 Wi-Fi의 다른 기기 정보      | Amazon과 Samsung은 아니라고 했고, Google, LG, Roku, TCL은 같은 망의 기기를 탐지한다고 했고 Google과 LG는 탐색 정보나 근처 기기 정보를 전송할 수 있다고 했다                                                                                                 |
| 11~13. 전부 끌 수 있나, 기본값, 저장 | 누구도 모든 전송을 끌 수 있다고 하지 않았다. Google은 초기 설정에서 사용 진단과 맞춤 광고가 기본으로 켜진다고 했고, LG, Samsung, Amazon은 ACR이 기본적으로 꺼져 있다고 했다                                                                                 |
| 14~15. 인터넷을 끊으면               | 모두 인터넷이 없으면 전송이 멈춘다고 했다. Amazon, Google, Roku, TCL은 오프라인 때 일부 데이터를 저장했다가 재연결 때 보낸다고 했고 Samsung은 기능과 연식에 따라 다르다고 했다                                                                              |
| 16~17. 암호화와 삭제                 | Roku는 종단 간 암호화를 쓴다고 했고 Google은 표준 질의와 텔레메트리는 종단 간 암호화가 아니라고 했다. LG는 일부 정보(음성 인식의 텍스트 결과 등)가 암호화되지 않을 수 있다고 밝혔다. 삭제는 Amazon, Apple, Google, LG, Roku, Samsung, TCL이 경로를 제시했다 |

## 분석

### 질문 설계의 약점이 곧 응답 전략의 약점이었다

“예/아니오”로 묻는다는 설계는 회사들이 한 문장짜리 부인과 여러 문단짜리 설명
사이를 오가게 만들었다.
HN 사용자 headz는 예/아니오 질문 17개를 만들었는데도 회사들이 여러 문장, 때로는
여러 문단으로 답했다고 꼬집었다.[^headz]
무응답도 신호라는 의견이 있었다.
bita_nidir는 “답하지 않음”도 하나의 데이터이며 불리한 추론의 근거가 된다고
썼다.[^bita_nidir]
다만 이것은 독자의 해석이고, 글은 무응답의 이유를 알지 못한다.
StevenWaterman은 Sony가 요청에는 응했지만 17개 중 0개에 답했다는 점을 궁금해
했다.[^StevenWaterman]
글에는 Sony의 응답 방식이 따로 적혀 있지 않고, 표에서는 모든 질문에 “답을 주지
않았다”고 표시된다.

### “스크린샷은 안 한다”가 “시청 내용을 모른다”는 뜻은 아니다

질문 4의 답이 가장 자주 논쟁이 되었다.
LG는 스크린샷이나 화면 녹화를 수집하지 않고 오디오 지문으로 콘텐츠를 식별한다고
답했다.
butlike는 이 답이 곧 지문으로 어떤 콘텐츠가 표시되는지 알면서 화면을 수집하지는
않는다고 말할 수 있게 해 주는 방식이라고 풀었다.[^butlike]
GoToRO는 스크린샷이 아니라 지문을 저장하는 것이어서 거짓말은 아니라고
했다.[^GoToRO]
tensegrist는 “LG TV는 …하지 않는다”가 아니라 “LG TV의 ACR은 …하지 않는다”라고 쓴
점에 주목해, 변호사가 그럴듯한 다른 귀속 방식을 찾았을 수 있다고
추측했다.[^tensegrist]
이는 답변 문구에 대한 해석이다.
질문과 답변의 문장 구조에서 수집하지 않는다는 것과 식별하지 않는다는 것은 다른
진술이다.

### 질문 14의 “인터넷을 끊으면”은 다른 연결 경로를 다루지 못한다

모든 회사가 인터넷에 연결되지 않으면 전송이 멈춘다고 답했고, 이는 글에서 가장
일관된 답이다.
Samsung은 한 걸음 더 나가 Bluetooth는 리모컨과 헤드폰 같은 로컬 연결에만 쓰이고
TV가 열린 Wi-Fi에 스스로 접속하지 않는다고 했다.
HN에서 이 답이 닫지 못하는 질문이 이어졌다.
ourmandave는 TV가 주변의 공용 Wi-Fi에 자동 접속하거나 5G 모뎀을 내장한다는
소문이 확인되었는지 물었다.[^ourmandave]
deltoidmaximus는 완전히 열린 Wi-Fi는 이제 거의 없어서 그 방식은 의미가 줄었고,
통신사와 제휴하는 쪽이 더 그럴듯하다고 추측했다.[^deltoidmaximus]
LocalH는 ISP 공유기가 기본으로 다른 고객용 별도 Wi-Fi를 켜 두므로 TV 제조사가
ISP와 계약해 그 SSID에 접속하게 하기는 어렵지 않다고 썼다.[^LocalH]
Alive-in-2025는 LG TV가 Wi-Fi에 연결하지 않아도 Comcast의 Xfinity Wi-Fi에
접속하는 것 같다고 썼다.[^Alive-in-2025]
vander_elst는 라디오나 Bluetooth로 휴대폰을 통해 보내는 경로를 묻고 싶었다고
했다.[^vander_elst]
이 중 확인된 것은 없다.
추측이거나 한 사용자의 경험이며 글과 회사의 답변은 이 경로들을 직접 다루지
않는다.
다만 질문 14는 “인터넷 연결 해제”를 기본 방어로 삼는데, 그 방어가 성립하려면
TV가 스스로 접속하지 않는다는 보증이 먼저 필요하고 이 보증을 한 곳은 Samsung
하나다.
Samsung의 이 진술도 회사의 말이며 검증되지 않았다.

### 같은 질문에 서로 다른 층위로 답해서 표가 비교 가능한 척한다

질문 16은 기기 암호화, 전송 중 암호화, 종단 간 암호화를 한꺼번에 묻는다.
Roku는 업계 표준 보안 조치로 “특히 종단 간 암호화”를 쓴다고만 답했다.
Google은 기기 안은 예(파일 기반 암호화), 전송 중은 예(TLS)이지만 종단 간은
아니라고 나누어 답했고, 서버가 음성 명령과 추천을 처리하려면 요청을 풀어야 하기
때문이라고 이유를 적었다.
Amazon과 TCL은 전송 중 암호화만 말했고, Samsung은 ACR 정보를 해시하고 전송과
저장 모두 암호화한다고 했다.
이 다섯 답은 같은 질문의 서로 다른 부분에 답한 것이어서 한 줄로 비교할 수 없다.
Google의 “종단 간은 아니다”는 오히려 가장 구체적인 답이고, Roku의 종단 간
암호화가 무엇과 무엇 사이인지는 글에 나와 있지 않다.
질문 9에서 TCL이 수집 정보를 AWS, Azure, Google Cloud에 저장한다고 밝힌 것도,
같은 묶음에서 회사별로 누가 데이터를 받는지가 답마다 다르다는 사례다.

## 비평

### 글의 서두와 본문 답변이 맞물리지 않는다

PinkaDunka는 글이 처음에 많은 TV가 ACR을 쓴다고 하지만 응답한 회사 중 아무도
ACR을 시인하지 않은 것처럼 보인다고 짚으며, 그러면 ACR을 하는 TV는 어디인지,
Verge는 왜 그곳에 묻지 않았는지 물었다.[^PinkaDunka]
eli는 화면 캡처 방식으로 ACR을 한다고 인정한 제조사는 없지만 LG는 오디오 샘플을
쓰며, Google은 일부 하드웨어 제조사가 별도 ACR 소프트웨어를 깔 수 있다고
인정했고, Sony와 Hisense는 답하지 않았으나 둘 다 ACR을 쓴다고 보도되었다고
정리했다.[^eli]
따라서 글의 서두는 틀리지 않았지만, 본문의 표만 읽으면 “누구도 ACR을 하지
않는다”로 읽힐 위험이 있다.
실제로는 LG는 질문 5에서 ACR이 켜져 있으면 지문 정보를 처리한다고 답했다.

### 선택된 표본과 편집 판단의 문제

글은 응답이 있는 7곳을 비교하지만 Vizio가 질문에 답하지 않았다는 것이 가장 크게
눈에 띈다.
노스이스턴 연구가 Vizio에서 옵트아웃 뒤 전송을 확인했는데도 Vizio의 답은 없다.
detourdog는 Apple의 답을 “직접 답이 아니다”라고 요약하지 말고 간접 답변 자체를
공개해 독자가 판단하게 하라고 비판했다.[^detourdog]
이에 ericbarrett는 불성실하게 모호하게 쓴 답변을 전달할 의무는 조사자에게 없다고
반박했다.[^ericbarrett]
MBCook은 모든 질문에 직접 답한 LG에 감명받았고(진실이라는 전제에서) 질문을 피한
Apple에 실망했다고 썼다.[^MBCook]
이 논쟁은 편집 정책에 관한 것이다.
확인된 사실은 글이 Apple의 몇몇 답을 “직접적인 답이 아니다”라고 표시했다는
것이다.

### 정책 답변은 검증되지 않았고 바뀔 수 있다

M95D는 회사의 정책은 하룻밤에 바뀔 수 있어서 답변이 모두 사실이어도 소용이
없다고 썼다.[^M95D]
CivBase는 그냥 거짓말을 하고 있을 수도 있다고 했고,[^CivBase] throwa356262는
LG의 답이 틀렸다는 근거로 설정의 “Live Plus” 옵션이 일주일 안에 자동으로
되돌려진다고 했다.[^throwa356262]
이 마지막 주장은 한 사용자의 경험이고 글이나 LG가 확인한 것이 아니다.
somedude895는 마케팅 업계에서 LG가 경쟁사 광고를 본 사람을 겨냥하는 서비스를
제안했다고 했다.[^somedude895]
이 역시 개인 증언이다.
글은 기술적 검증(네트워크 트래픽 분석 등)을 하지 않고 회사의 진술을 모았으므로,
그 진술이 사실인지는 별도 문제다.

## 인사이트

### 사용자의 실제 방어는 회사의 답변이 아니라 네트워크 경계에 있다

글이 보여 준 공통점은 인터넷을 끊으면 전송이 멈춘다는 것이다.
이에 대한 HN의 실용적 결론은 일관되었다.
afavour는 흔한 조언이 스마트 TV를 사서 인터넷에 연결하지 않고 HDMI 기기를 꽂는
것이라고 정리했고,[^afavour] MattSayar는 연결해야 한다면 NextDNS나 AdGuard를
라우터에서 쓰라고 했다.[^MattSayar]
상업용 디스플레이는 가격이 훨씬 비싸다는 한계가 있다.
다만 연결하지 않는 선택은 업데이트와 스트리밍 기능을 포기하는 것이고, Roku나
Apple TV 같은 별도 기기가 그 자리를 대신하더라도 그 기기의 수집 정책을 따르게
된다.
krupan이 지적했듯 이미 많은 정보를 주요 기업에 주고 있다면 의미가 다를 수
있다.[^krupan]
이 정리는 댓글들의 종합이고 이 문서의 판단은 아니다.

### 같은 질문을 같은 틀로 반복해야 변화가 보인다

이 글의 가치는 첫 번째 응답 세트라는 데 있다.
한 달 뒤 같은 질문을 다시 보냈을 때 답이 바뀌었는지가 정책의 안정성을 보여 준다.
글도 응답을 거부한 회사가 답하면 추가하겠다고 밝혔다.
이는 이 문서의 제안이며 글이 하겠다고 한 것은 아니다.

### 결론을 바꿀 관찰

- 독립된 트래픽 분석이 LG, Samsung, Roku의 옵트아웃 후 전송량을 측정해 회사의
  답과 일치함을 보인다면, 답변을 신뢰할 수 없다는 의견은 약해진다.
- Hisense, Sony, Panasonic, Vizio가 같은 질문에 공개적으로 답한다면, 현재 표의
  7곳 비교가 시장 전체의 비교로 확장된다.
- 반대로 옵트아웃 후에도 전송이 계속된다는 연구가 늘어나면, 회사의 진술에서 “끌
  수 있다”는 부분의 의미가 줄어든다.

---

[^headz]: <https://news.ycombinator.com/item?id=50454549>

[^bita_nidir]: <https://news.ycombinator.com/item?id=50454529>

[^butlike]: <https://news.ycombinator.com/item?id=50456195>

[^GoToRO]: <https://news.ycombinator.com/item?id=50454832>

[^tensegrist]: <https://news.ycombinator.com/item?id=50454773>

[^PinkaDunka]: <https://news.ycombinator.com/item?id=50454249>

[^eli]: <https://news.ycombinator.com/item?id=50454367>

[^detourdog]: <https://news.ycombinator.com/item?id=50453914>

[^ericbarrett]: <https://news.ycombinator.com/item?id=50453971>

[^MBCook]: <https://news.ycombinator.com/item?id=50454370>

[^M95D]: <https://news.ycombinator.com/item?id=50456501>

[^CivBase]: <https://news.ycombinator.com/item?id=50454374>

[^throwa356262]: <https://news.ycombinator.com/item?id=50454718>

[^somedude895]: <https://news.ycombinator.com/item?id=50456015>

[^StevenWaterman]: <https://news.ycombinator.com/item?id=50454753>

[^ourmandave]: <https://news.ycombinator.com/item?id=50454689>

[^deltoidmaximus]: <https://news.ycombinator.com/item?id=50456390>

[^LocalH]: <https://news.ycombinator.com/item?id=50458839>

[^Alive-in-2025]: <https://news.ycombinator.com/item?id=50460617>

[^vander_elst]: <https://news.ycombinator.com/item?id=50458230>

[^afavour]: <https://news.ycombinator.com/item?id=50454825>

[^MattSayar]: <https://news.ycombinator.com/item?id=50455174>

[^krupan]: <https://news.ycombinator.com/item?id=50454889>
