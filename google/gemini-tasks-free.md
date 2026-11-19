# Gemini Tasks 무료 확대

원문: [Put Gemini to work for you](https://blog.google/innovation-and-ai/products/gemini-app/tasks-in-gemini-free-new-features/)

HN 토론: <https://news.ycombinator.com/item?id=50551601> (50점, 65개 댓글)

GN 토론: <https://news.hada.io/topic?id=37433>

## 요약

2026년 11월 17일 Google 블로그에 Gemini 앱·AI Studio·Labs 담당 부사장 Josh Woodward가 쓴 글이다(HTML 제목은 「How to use Tasks in Gemini for personal assistance」). 부제는 「Gemini가 이제 전화를 걸고 요금을 내고 일을 끝낸다」이다.
글은 약속 잡기, 청구서 관리, 장보기 같은 복잡한 일을 Gemini가 맡는 업데이트를 소개한다. 수억 명에게 무료로 풀린다고 하며 대상 국가는 미국, 일본, 한국, 캐나다, 호주, 인도이다. 새 모델 「Gemini 4 Hydrogen」 위에서 돌고, 고급 기능은 미국에서 먼저 나간다고 한다.
이 문서는 글 전문을 읽었다. 링크된 보안 기술 문서, Agent Compute Engine, 연결 앱 플랫폼, 결제 프로토콜 문서는 열지 못했고 직접 써 보지 않았다. 글의 기능 서술은 모두 Google의 주장이며 모델 이름은 글에 나온 그대로이다.

글이 든 사용 사례(필자의 일화)는 다음과 같다.

- 자동차 정비: Gemini가 Personal Intelligence와 Google 지도로 가까운 대리점 두 곳에 동시에 전화해 금요일 이른 아침 예약을 잡고 Google 캘린더에 넣었다. 통화에서 자신이 AI임을 밝혔고 업체는 AI 통화를 거부(opt-out)할 수 있다고 한다.
- 전기 요금: 389달러 청구서가 나온 뒤 Gemini가 새 Google 비밀번호 관리자 연동으로 전기 회사 포털에 접근해 청구서 PDF와 이메일을 분석했고, 히트 펌프가 오후 4시경 피크 요금 시간에 도는 것을 찾아냈다.
- 쇼핑: Google의 쇼핑 그래프로 USB-C 충전기를 비교하고 와트와 색을 묻고 Google Pay로 결제했으며 할인 코드로 10달러를 아꼈다.
- 장보기: RCS 문자로 Instacart 주문에 품목을 더하고, 빈 시리얼 상자 사진에 「이것도 추가」로 답한 뒤 주문 완료는 Instacart로 넘겼다. 60개 넘는 앱과 연결되고 개발자는 연결 앱 플랫폼에 신청할 수 있다.
- 가족 행정: Gmail의 학교 메일을 `gemini@google.com`으로 전달하면 날짜가 캘린더에 들어가고 농구 연습과의 충돌이 표시된다.

결제와 보호에 대한 서술은 다음과 같다.

- 결제: Agent Payments Protocol(AP2)을 쓰며 American Express(곧 지원), Mastercard, Visa를 든다. 지원 카드의 디지털 토큰을 쓰고 카드 포인트, 캐시백, 구매자 보호를 그대로 받는다. 시작 전에 엄격한 지출 한도를 정할 수 있고 Gemini가 그 안에 머물도록 설계되었다고 한다. 영수증과 배송 추적은 Google Wallet으로 가고 Wallet은 같은 날부터 iOS로 확대된다. Universal Commerce Protocol(UCP) 연동이 다음에 온다.
- 데이터 보호: 작업은 Google Cloud의 Agent Compute Engine에서 계정 전용의 하드웨어 격리 가상 머신에서 돈다. 샌드박스와 레드팀 시험, 프롬프트 주입 필터, Safe Browsing으로 열 수 있는 링크를 제한하는 겹겹의 방어를 든다. 사용자는 작업 중에 끼어들 수 있고 「구매」 클릭 같은 중요한 단계 전에 Gemini가 멈춰 확인하며 애매한 지시에는 되묻는다. 일상적 행동은 「항상 허용」으로 둘 수 있다.
- 한계 고백: 작업은 실패하거나 빗나갈 수 있어 사용자가 비추천을 눌러 달라고 한다. 일부 사이트에서는 거의 끝까지 간 뒤 마지막 클릭을 사용자에게 돌려준다. Google은 주요 웹사이트와 보안 업체와 열린 검증 가능한 표준을 만들고 있다.

시작하려면 Gemini 홈 화면의 토글을 채팅에서 작업(Task)으로 바꾼다. 미국에서는 이메일 전달이나 문자(설정, 채널, 「Text with Gemini」의 「Set up」, 전화번호 인증)로도 쓴다. 문자는 미국 번호와 해당 통신사가 필요하고(각주), 통화는 인디애나, 루이지애나, 미네소타, 몬태나, 네브래스카에서 제공되지 않는다(각주). 사용량 한도는 글에 적혀 있지 않다.

## 분석

### 중심 주장은 어시스턴트가 대신 행동하는 단계에 들어왔다는 것이다

앞선 단계의 어시스턴트가 답을 주는 일이었다면 이 글은 전화를 걸고 포털에 로그인하고 결제까지 하는 행동 단계를 내세운다. 전환의 근거는 필자의 일화 다섯 개와 결제 프로토콜, 격리 실행 환경의 설명이다. 이는 글의 서술을 이 문서가 정리한 것이다.

### 신뢰 장치를 기능 못지않게 길게 설명한다

글의 절반 가까이가 결제 한도, 확인 지점, 격리 VM, 주입 방어, 사용자 개입에 쓰인다. 행동하는 어시스턴트의 도입 장벽이 기능이 아니라 신뢰라는 인식이 구성에 드러난다. 이는 이 문서의 해석이다.

### 무료와 고급의 경계가 모호하다

핵심 업데이트는 무료이고 고급 기능은 미국에서 시작한다고만 적는다. 이후 Gemini 4 Neon 글(`google/gemini-4-neon.md`)은 Tasks가 Neon에서 돌 수 있고 더 큰 모델보다 사용량 여유가 크다고 적는다.

## 비평

### 사용 사례가 필자 개인의 일화이다

다섯 사례 모두 필자의 경험이고 성공률, 실패 사례, 소요 시간, 오류율 수치가 없다. HN에서 한 사용자는 같은 종류의 에이전트가 승인을 매 단계마다 요구하고 「항상 승인」으로 설정해도 티켓 여러 개를 고칠 때 티켓마다 묻는다고 했다.[^artdigital]
이는 글이 말하는 확인 지점 설계와 실사용의 마찰을 보여 주는 증언이다.

### 전기 요금 사례의 근거가 의심받는다

한 사용자는 자신의 요금 고지서로는 무엇이 전기를 쓰는지 알 수 없는데 Gemini가 히트 펌프를 어떻게 짚었는지 물었다.[^guiomie]
글은 청구서 PDF와 이메일을 분석했다고만 쓰며 사용한 정보(시간대별 사용량 등)를 밝히지 않는다. 이 문서는 이를 확인하지 못했다.

### 무료의 지속성과 데이터 이용에 대한 불신이 크다

HN에서는 무료 서비스가 길들이기 뒤 가격을 올리거나 광고를 붙일 것이라는 반응,[^wolvoleo] Google이라 1년 뒤 조용히 종료될 것이라는 농담,[^pavel-lishin] 사용자의 할 일, 시간, 협업 패턴이 추적 신호가 된다는 우려가 있었다.[^demo4567]
글의 데이터 보호 절은 격리 VM을 설명하지만 이용 데이터의 학습과 광고 활용 여부는 밝히지 않는다.

### 이름과 제품 혼선이 있다

한 사용자는 기존 Google Tasks와 Gemini Tasks의 차이를 물었고 다른 사용자는 Muse 같은 지속형 에이전트와 달리 Tasks는 일회성 상호작용 같다고 했다.[^bnjoroge][^valleyjo]
어시스턴트의 유용성 자체에 회의적인 반응(대부분의 사람은 일정을 관리해 줄 사람이 필요할 만큼 바쁘지 않다)도 있었다.[^this-user]

### 외부 반응

HN 글 제목은 「Google Gemini's “Tasks” Personal Assistant Is Now Free」이다. 한 사용자는 가족 여행의 환불 가능 항공권 가격을 지켜보다가 내려가면 다시 예약하는 일에 에이전트를 성공적으로 썼다고 사례를 들었다.[^johnnyo]
Lobste.rs에는 이 글의 토론이 없었다(`gemini tasks` 검색은 관련 없는 글만 돌려주었다).
GeekNews 토픽은 요약이고 이용자 댓글이 없었다.

## 인사이트

### 가져갈 것은 행동형 어시스턴트의 위임 범위를 정하는 틀이다

지출 한도, 확인할 단계, 항상 허용할 일상 행동, 중간 개입 방법을 위임 전에 정한다. 이 글이 제시하는 설정 지점(한도, 「항상 허용」, 중단)은 다른 에이전트를 쓸 때도 점검표가 된다. 이는 이 문서의 적용이다.

### 처음에는 되돌릴 수 있는 일부터 맡긴다

일정 정리나 가격 비교처럼 취소가 쉬운 작업으로 시험한 뒤 결제가 걸린 작업으로 넓힌다.

### 확인할 관찰

이 글의 주장을 가를 관찰은 세 가지이다.
성공률과 실패 유형이 공개된 평가,
무료 범위와 고급 기능의 유료 조건,
데이터 이용 정책(학습, 광고)이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^artdigital]: <https://news.ycombinator.com/item?id=50552802>

[^guiomie]: <https://news.ycombinator.com/item?id=50552708>

[^wolvoleo]: <https://news.ycombinator.com/item?id=50553000>

[^pavel-lishin]: <https://news.ycombinator.com/item?id=50553334>

[^demo4567]: <https://news.ycombinator.com/item?id=50552894>

[^bnjoroge]: <https://news.ycombinator.com/item?id=50552580>

[^valleyjo]: <https://news.ycombinator.com/item?id=50552002>

[^this-user]: <https://news.ycombinator.com/item?id=50552535>

[^johnnyo]: <https://news.ycombinator.com/item?id=50552935>
