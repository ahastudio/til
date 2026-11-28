# Apple 서비스 장애

<https://developer.apple.com/system-status/>

HN 토론: <https://news.ycombinator.com/item?id=50535238> (675점, 376개 댓글)

GN 토론: <https://news.hada.io/topic?id=37365>

## 소개

Apple Developer 시스템 상태 페이지이다.
App Store Connect, APNS, CloudKit, Xcode Cloud, Apple Maps API, Apple Pay 샌드박스 같은 개발자용 서비스 약 50개의 상태를 초록 원(정상)과 빨간 삼각형(장애)으로 보여 준다.
상태 페이지는 실시간으로 바뀌는 화면이라서, HN 사용자들이 장애 중에 본 상태는 이 문서가 볼 수 없었다.
소비자용 상태 페이지(`apple.com/support/systemstatus/`)는 열지 않았다.

읽은 시점의 페이지는 대부분 항목이 정상(available)이었다.
장애가 해결된 표시는 이런 항목에 남아 있었다.

- App Store Connect: 장애 2건
- App Store: 인앱 결제(In-App Purchases), Connect의 분석(Analytics), 판매와 동향(Sales and Trends)
- Developer ID Notary Service, Apple Music Connect, Apple Music for Artists
- News Publisher: 성능 문제 해결
- Xcode Cloud: 장애 1건과 문제 1건 해결

이는 시점이 지난 뒤의 기록이므로 장애 당시의 범위와 지속 시간을 말해 주지 못한다.

## 스레드가 전하는 상황

스레드에는 HN 사용자들의 현장 보고가 이어졌다.

- 로그인: 새로 로그인하면 실패하고 기존 세션은 일부만 영향을 받았다는 보고가 있었다.[^mynameisvlad] 여러 기기에서 Apple 계정 인증을 다시 요구하는 화면이 떴다는 보고도 있었다.[^tedd4u] 이전에 비밀번호를 거의 쓴 적이 없다는 반응도 이어졌다.[^softtalker]
- 매장: 한 사용자는 Apple Store가 주문과 반품을 처리하지 못하고 새로 산 iPhone을 개통하지 못한다고 전했다.[^cjbconnor] 다른 사용자는 매장이 거래, 수리, 내부 서비스를 모두 할 수 없어 사실상 오프라인이라고 썼고,[^testfrequency] 예약은 받는데 장애 때 취소할 방법이 없다는 불만도 있었다.[^ruther4d]
- 상태 페이지: 사용자들이 개발자 페이지와 일반 사용자용 페이지가 따로 있다는 점을 처음 알았다고 했고, 어떤 서비스가 어느 쪽에 오르는지 기준을 궁금해했다.[^mkhalil] 한 사용자는 계정과 다른 서비스의 점이 다시 초록으로 바뀌는 것을 봤다고 했다.[^zzzeek]
- 영향 없음: 한 사용자는 자신의 Apple 기기가 모두 문제없이 돌았고 달력이나 이메일은 다른 사업자를 쓴다며, 대부분의 사람은 장애를 알아채지도 못했을 것이라고 했다.[^anon7000] 장애의 체감이 사용자의 서비스 구성에 달려 있다는 증언이다.

## 분석

### 스레드의 중심 질문은 장애가 서로 이어졌는가이다

글 제목은 Apple 장애이지만 댓글의 상당수는 같은 주의 다른 사건을 함께 든다.
한 사용자는 Outlook, FAA, 은행, Optimizely 악성코드, 미국 정부 통신망, Apple을 나열하며 공황 상태가 필요한지 물었다.[^m4r1k]
한 사용자는 같은 시기의 장애가 유독 눈에 띄는 것은 중국 정찰 풍선 때처럼 대중이 연결 고리를 찾기 때문이라고 짚었다.[^jpatten]
이에 대해 장애가 정말 크고 특이하다는 반박이 있었고,[^greyarea] 이전에도 있었으나 보도되지 않았을 뿐이라는 재반박이 이어졌다.[^mixdup]
뉴스에서 이야기의 공급과 수요를 가르기 어렵다는 관찰도 나왔다.[^seizethecheese]
이는 스레드 내부의 논쟁 구도를 이 문서가 정리한 것이다.

### 연결을 가정하는 해석은 대부분 추측이다

공동 공격을 의심하는 댓글에는 반대 의견이 나란히 달렸다.
동시에 일어나지 않고 하나씩 일어나는 것이 공격자 입장에서는 효과가 작은 최선의 경우라는 지적,[^coolestbeans]
IT 관점에서는 서로 다른 하드웨어와 소프트웨어의 평범한 장애가 우연히 겹친 것일 가능성이 높다는 의견,[^annoyingnoob]
FAA 건은 통신 라우터 문제이고 시공사가 알려져 있어 설명이 된다는 의견이 있었다.[^warmwash]
어느 쪽도 증거가 제시되지 않았고, 지정학적 시기와 연결하는 댓글은 정치적 추측에 가깝다.

## 비평

### 원문이 장애의 근거가 되지 못한다

이 문서의 원문은 장애가 끝난 뒤에도 같은 주소에 남는 실시간 페이지이다.
스레드의 증언은 유용하나 각자의 지역과 계정, 서비스에 한정된다.
HN의 한 사용자는 자신의 미국 동부 해안 기기에서는 문제가 보이지 않는다고도 했다.[^prometheus]

### 개발자 상태 페이지는 소비자 영향을 설명하지 않는다

두 페이지의 범위가 다르다는 점은 스레드의 사용자도 지적했다.[^trickypr]
장애의 전체 모습을 보려면 소비자용 페이지와 Apple의 공지를 확인해야 한다.

### 매장 업무 연속성 비판은 일화 수준이다

매장이 거래를 하지 못했다는 보고와 업무 연속성 계획이 있어야 한다는 비판은 사용자의 한두 증언에 기댄다.[^xyst]

### 외부 반응

HN 스레드가 이 장애의 반응이 가장 풍부한 곳이다.
Lobste.rs에서는 `developer.apple.com` 도메인의 최신 글이 한 달 전 것이라 이 상태 페이지는 올라오지 않았다.
GeekNews에는 같은 주소의 토픽이 있으나 댓글이 하나이고, 그것도 HN 댓글을 다시 모은 GN⁺ 계정의 요약이라 GeekNews 이용자의 반응은 없다.

## 인사이트

### 가져갈 것은 상태 페이지는 시점의 기록이라는 점이다

장애가 끝나면 같은 주소가 다른 내용을 보여 준다.
장애를 기록하거나 분석하려면 그 순간의 화면(캡처, 아카이브)과 공식 사후 보고서를 따로 확보해야 한다.
평소에 쓰는 서비스의 상태 페이지 주소를 아는 것과, 이 페이지가 어느 사용자층의 영향을 대표하는지 아는 것은 다른 일이다.
이는 이 문서의 정리이다.

### 같은 주의 장애를 하나의 이야기로 묶기 전에 각자의 증거를 따로 모은다

스레드의 논쟁이 보여 주듯, 시기가 겹치는 장애는 연결 고리를 찾으려는 심리를 부른다.
각 사건의 공식 원인 설명이 나온 뒤에야 공통점이 있는지 판단할 수 있다.
그 전의 연결은 가설로만 다룬다. 이는 이 문서의 적용이다.

### 확인할 관찰

이 사건의 해석을 가를 관찰은 세 가지이다.
Apple이 장애의 원인과 범위, 복구 시각을 밝히는지,
같은 주의 다른 장애들의 공식 원인에 공통점이 있는지,
로그인 장애가 계정 인증 계층에 국한된 문제였는지이다.

---

[^mynameisvlad]: <https://news.ycombinator.com/item?id=50535682>

[^tedd4u]: <https://news.ycombinator.com/item?id=50536201>

[^softtalker]: <https://news.ycombinator.com/item?id=50537873>

[^cjbconnor]: <https://news.ycombinator.com/item?id=50535589>

[^testfrequency]: <https://news.ycombinator.com/item?id=50535918>

[^ruther4d]: <https://news.ycombinator.com/item?id=50535942>

[^mkhalil]: <https://news.ycombinator.com/item?id=50537241>

[^zzzeek]: <https://news.ycombinator.com/item?id=50535968>

[^anon7000]: <https://news.ycombinator.com/item?id=50542401>

[^m4r1k]: <https://news.ycombinator.com/item?id=50536190>

[^jpatten]: <https://news.ycombinator.com/item?id=50536792>

[^greyarea]: <https://news.ycombinator.com/item?id=50536826>

[^mixdup]: <https://news.ycombinator.com/item?id=50537335>

[^seizethecheese]: <https://news.ycombinator.com/item?id=50536658>

[^coolestbeans]: <https://news.ycombinator.com/item?id=50537071>

[^annoyingnoob]: <https://news.ycombinator.com/item?id=50536454>

[^warmwash]: <https://news.ycombinator.com/item?id=50536883>

[^prometheus]: <https://news.ycombinator.com/item?id=50536639>

[^trickypr]: <https://news.ycombinator.com/item?id=50537740>

[^xyst]: <https://news.ycombinator.com/item?id=50536628>
