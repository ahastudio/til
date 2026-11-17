# App Store 심사가 길어졌다는 앱 개발자들

원문: [AI is turning Apple’s app review process into a nightmare for developers](https://synthanatomy.com/2026/11/ai-is-turning-apples-app-review-process-into-a-nightmare-for-developers.html)

HN 토론: <https://news.ycombinator.com/item?id=50474311> (197점, 232개 댓글)

GN 토론: <https://news.hada.io/topic?id=37117>

## 요약

Synth Anatomy는 음악 제작 소프트웨어를 다루는 매체이다.
2026년 11월 12일자 이 글은 AI로 만든 iOS 앱이 몰려 App Store 심사가 느려지고 있다고 주장한다.
글은 하루에 새 iOS 음악 앱이 10개에서 20개쯤 나온다고 추정하는데, 이 수치의 근거는 적혀 있지 않다.
Apple의 심사 가이드라인은 제출의 최소 50%를 24시간 안에, 90%를 48시간 안에 심사한다고 밝히고 있고, 필자는 지금까지 개발자들이 보통 하루나 이틀을 겪었다고 쓴다.

필자가 드는 사례는 이렇다.
AudioThing, Igor Vasiliev, Sugar Bytes 같은 개발자의 새 앱이 몇 주째 심사에 머물러 있다고 한다.
Pittsburgh Modular의 Microvolt 3901은 10월 27일에 VST로 나왔지만 iOS 판은 11월 12일에야 나왔고, 동시 출시를 계획했었다.
AudioThing Materia는 승인까지 25일이 걸렸고(거절 1회), 후속작 Seconds는 29일째 심사 중이라고 적는다.

두 개발자의 증언이 길게 인용된다.
Unfiltered Audio의 Michael Hetrick은 Loopy Pro 포럼에서 Sinusoidal Run Rhythm이 네 번 거절당했다고 썼다.
첫 번째는 시연 영상 요구였고, 두 번째는 설명문의 “Polyharmonic”이라는 용어에 문서화된 라이선스가 필요하다는 것이었고, 세 번째는 “필수 독점 하드웨어”와 연결한 영상 요구였고, 네 번째는 MIDI 판이 원래 앱과 비슷하다며 스팸으로 분류한 것이다.
한 달이 넘는 왕복 끝에 오디오 판만 먼저 냈다고 한다.
신규 개발자 Marek Dendes는 몇 달 만든 신디사이저 CRUX Synth가 “디자인 스팸”이고 기존 앱과 중복이며 “앱 생성 템플릿 서비스”로 만들어졌다는 같은 사유로 네 번 거절당했다고 한다.
심사 상태가 “In Review”에서 거의 즉시 “Rejected”로 바뀌어서 사람이 읽지 않는 자동 절차로 보이고, App Review Board 이의 제기에는 5일째 답이 없다고 했다.

필자는 두 경우에서 Apple이 심사에 AI를 쓰는 것 같다고 말하지만, 두 인용 모두 개발자의 추정이고 Apple의 확인은 글에 없다.
글은 AI 앱이 늘어난 점과 Apple의 처리 방식 두 가지를 모두 원인으로 말한다.
Apple이 제휴 프로그램을 끝내 매체가 iOS 앱을 제대로 다루지 못하게 되었고, 하루 신작이 너무 많아 좋은 앱도 묻힌다는 의견도 덧붙인다.

## 분석

### 중심 주장은 심사 지연과 자동 거절이 AI 앱의 홍수와 맞물린다는 것이다

글이 보여 주는 확인된 사실과 추정을 나누어 보면 이렇다.
확인된 것은 개발자 여럿이 몇 주 지연과 반복 거절을 겪었다는 보고이다.
추정인 것은 홍수가 원인이라는 인과, 그리고 Apple의 심사가 AI라는 점이다.
GeekNews의 한 댓글도 같은 구분을 요구했다. 확인된 승인 지연 사례와 원인 추정을 나누어 보아야 하고, AI로 심사한다는 부분은 기사에서도 개발자의 추정으로 분리되어 있다는 것이다.[^creatunealex]
이 문서도 그 구분을 따른다.

### 지연의 비용은 대기 일수보다 계획이 어긋나는 데서 생긴다

음악 앱은 VST와 iOS 판을 같은 날 내려는 계획이 많아서 한 플랫폼의 지연이 전체 일정을 민다.
HN의 한 개발자는 고객의 지역 행사용 앱이 심사 지연으로 행사가 끝날 때까지 나오지 못했다고 전했다. 영상과 백엔드 정보까지 요구받아 모두 답했고, 신속 심사를 두 번 요청했지만 소용이 없었다고 한다.[^joshstrange]
대기가 길어지는 것보다 언제 끝날지 예측할 수 없다는 점이 일정에 묶인 개발자에게 더 크게 작용한다는 점을 두 사례가 함께 보여 준다.

## 비평

### 모든 개발자가 지연을 겪는 것은 아니다

스레드에는 반대 경험이 여럿 있었다.
한 사용자는 새 앱 두 개를 지난주에 제출해 이틀 만에 게시되었다고 했고,[^mattrighetti]
다른 사용자는 지난 몇 달 동안 24시간 안에 심사가 끝났고 신규 계정의 첫 제출도 마찬가지였다고 했다.[^einsteinx2]
소규모 앱 세 개를 가진 개발자는 심사자가 업데이트를 길어야 2분쯤 본다고 했다.[^cdrnsf]
음악 앱이나 신디사이저 같은 특정 영역에서만 지연이 심할 가능성을 묻는 댓글도 있었다. 해당 위험을 훈련받은 심사자가 부족한 것이 아니냐는 것이다.[^trimethylpurine]
이 보고들은 개인 경험이고 표본이 없어서 글의 주장을 반증하지는 못하지만, 글이 전체 심사 체계의 붕괴처럼 쓴 부분은 범위가 좁게 읽혀야 함을 보여 준다.

### AI가 원인이라는 증거는 정황이다

개발자들이 AI를 의심하는 근거는 거절 사유가 사실과 맞지 않고, 상태가 순식간에 바뀌고, 답이 없다는 것이다.
이것은 자동화 도구가 쓰였을 가능성과 맞지만, 사람 심사자의 실수나 템플릿 답변으로도 설명된다.
한 HN 댓글은 이 문제가 AI 이전부터 있었다고 했고,[^ggoo]
다른 댓글은 최근 몇 년은 괜찮았고 하루나 몇 시간 만에 통과했다고 답했다.[^catoc]
한 개발자는 계정 삭제 기능이 없다는 이유로 거절되었고, 다음에는 테스트 계정이 멈췄다는 이유로 거절되었는데 로그에는 심사자가 계정 삭제 기능을 눌러 본 흔적이 있었다고 전했다.[^nikanj]
이 사례는 자동화 여부를 가리지 못한다. 심사자의 부주의일 수도 있기 때문이다.

### 개발자 쪽의 사정도 있다

한 댓글은 CRUX Synth 개발자의 글에서 권리 의식이 느껴진다고 했다. 같은 외관을 대량으로 찍어 내는 실제 AI 스팸이 있을 수 있다는 점을 개발자가 고려하지 못한다는 것이다.[^hmokiguess]
이에 대한 답글은 개발자 멤버십을 비용을 내고 샀는데 Apple이 그 일부를 이용하지 못하게 한다는 점을 들어 권리 의식이 아니라고 반박했다.[^galaco]
다른 댓글은 AI로 만든 앱 중 상당수가 기본 UI에 AI가 쓴 설명문을 붙인 것이라고 했다.[^rjh29]
또 다른 댓글은 오디오만 먼저 내고 MIDI 판을 따로 내는 필자 인용 속 방식을 두고 기능을 쪼개 두 번 파는 수법이 아니냐고 의심했다.[^newsahacko]
이는 댓글의 추측이고, 글의 인용에는 MIDI 판을 같은 바이너리에 묶어 두 AUv3가 함께 설치되게 하겠다는 말이 있다.

### 글에 빠진 것은 Apple의 입장과 수치이다

글에는 Apple의 응답이 없고, 심사 시간을 재는 통계도 없다.
지연 사례는 이름을 든 소수의 개발자이고, 하루 신작 10에서 20개라는 추정은 근거가 적혀 있지 않다.
한 HN 댓글은 Apple의 심사 인원이 2021년 에픽 재판 때 지적된 500명 수준에서 달라지지 않았다고 했지만 이것은 댓글의 주장이다.[^benoau]
이 문서는 이 숫자를 확인하지 못했다.

## 인사이트

### 신뢰 이력이 심사 속도에 반영되지 않는다는 불만이 핵심이다

한 댓글은 오랫동안 좋은 앱을 낸 AudioThing 같은 개발자가 신규 개발자와 같은 줄에서 기다려야 하는 점을 이상하게 여겼다.[^rramon]
심사가 이력과 무관하게 같은 대기열이라면, 개발자가 할 수 있는 일은 제출 시점을 일찍 잡는 것과 거절 사유를 줄이는 것뿐이다.
스레드에는 실무 대응도 나왔다. 거절 때 요구되는 시연 영상을 처음부터 준비해 두고, 급하면 신속 심사를 요청하며, 일정에 걸린 앱은 TestFlight나 웹 앱으로 우회하라는 제안이다.[^cadamsdotcom]
한 개발자는 계정 삭제 버튼이 이메일 확인을 요구하게 만들어 심사자가 실제로 삭제하지 못하게 해 거절을 피했다고 했다.[^grodriguez100]
이는 개인 사례이고, 같은 방식이 모든 심사에서 통할지는 확인되지 않았다.

### 비교 대상은 Google Play이다

한 개발자는 Google Play가 더 나쁘다고 했다. 12명의 베타 테스터가 14일 연속 앱을 설치한 상태로 유지해야 하고, 한 번이라도 12명 밑으로 떨어지면 시험이 처음부터 다시 시작된다는 것이다.[^littlecranky67]
Apple의 지연이 문제라는 점과, 다른 플랫폼의 절차도 만만치 않다는 점은 서로 양립한다.
이 문서는 Google Play의 현재 규정을 확인하지 못했다.

### 확인할 관찰

이 주장의 타당성을 가를 관찰은 세 가지이다.
Apple이 심사에 자동화 도구를 쓴다고 인정하거나 부인하는지,
지연 사례가 음악 앱 밖의 영역에서도 같은 빈도로 나오는지,
심사 처리 시간의 공개 통계가 나오는지이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^creatunealex]: <https://news.hada.io/topic?id=37117#cid69846>

[^joshstrange]: <https://news.ycombinator.com/item?id=50483377>

[^mattrighetti]: <https://news.ycombinator.com/item?id=50476041>

[^einsteinx2]: <https://news.ycombinator.com/item?id=50481380>

[^cdrnsf]: <https://news.ycombinator.com/item?id=50476799>

[^trimethylpurine]: <https://news.ycombinator.com/item?id=50477916>

[^ggoo]: <https://news.ycombinator.com/item?id=50476901>

[^catoc]: <https://news.ycombinator.com/item?id=50478593>

[^nikanj]: <https://news.ycombinator.com/item?id=50476005>

[^hmokiguess]: <https://news.ycombinator.com/item?id=50475585>

[^galaco]: <https://news.ycombinator.com/item?id=50476140>

[^rjh29]: <https://news.ycombinator.com/item?id=50475282>

[^newsahacko]: <https://news.ycombinator.com/item?id=50475751>

[^benoau]: <https://news.ycombinator.com/item?id=50475645>

[^rramon]: <https://news.ycombinator.com/item?id=50478684>

[^cadamsdotcom]: <https://news.ycombinator.com/item?id=50475688>

[^grodriguez100]: <https://news.ycombinator.com/item?id=50477169>

[^littlecranky67]: <https://news.ycombinator.com/item?id=50479927>
