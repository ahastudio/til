# iOS Safari 120Hz 우회 기법

원문: [Bypassing iOS Safari's 60 FPS Limit to Build Web Applications That Feel Native](https://rida.dev/blog/bypassing-ios-safari-60-fps-limit)

HN 토론: <https://news.ycombinator.com/item?id=50637890> (466점, 149개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/pxvmxo/bypassing_ios_safari_60_fps_limit> (19점, 10개 댓글)

GN 토론: <https://news.hada.io/topic?id=37832>

## 요약

Rida F'kih가 2026년 11월 20일에 올린 글이다.
읽는 시간은 10분이고, iPhone의 Safari에서 보도록 만든 페이지다.
출발점은 React Aria의 Devon Govett가 10월에 쓴 “스크롤만 있으면 된다”는 글과
React 창시자 Jordan Walke의 모바일 상호작용 실험 영상이다.
저자는 그 방식으로 만든 것은 모두 60 FPS에 묶여서 만들 이유를 찾지 못했다고
쓴다.

문제의 원인은 Safari 설정에 있다.
개발자 설정의 “렌더링 갱신을 60fps 근처로 선호” 플래그를 끄지 않으면,
WebKit은 120Hz 화면에서도 `requestAnimationFrame`을 60Hz로 제한하고
터치와 포인터 이벤트도 같은 속도로 묶는다고 한다.
반면 스크롤은 합성기(compositor)가 별도 스레드에서 처리하므로
자바스크립트를 거치지 않고 부드럽게 움직인다.
저자의 전략은 스크롤 영역을 입력 장치로 쓰는 것이다.

저자는 이를 “컨트롤러”라고 부르며 다음 단계로 만든다.

| 단계                 | 시도 또는 결과                                                         |
| -------------------- | ---------------------------------------------------------------------- |
| 스크롤 이벤트        | 관성 스크롤 중 초당 5~26회만 갱신되어 쓸 수 없음                       |
| MessageChannel       | 재귀 호출로 읽으면 초당 5만 회를 읽지만 구별되는 값은 80개뿐           |
| Atomics              | 같은 80개, 그리고 SharedArrayBuffer 때문에 COOP/COEP 헤더 필요         |
| 채택한 방식          | MessageChannel을 기기 주사율에 맞춰 setTimeout으로 늦추고 vsync에 정렬 |
| 빈 rAF 루프          | UI 프로세스의 위치 전달이 약 12.5% 늘어 초당 90개                      |
| 보이지 않는 스크롤러 | 배경 스무스 스크롤로 ProMotion을 120Hz로 끌어올림                      |

출력 쪽은 두 번째 문제다.
입력이 120Hz여도 DOM은 60번만 갱신된다.
저자는 일곱 번의 시도 끝에, `transferControlToOffscreen`으로 `OffscreenCanvas`를
얻으면
WebKit이 다음 렌더링 단계를 기다리지 않고 프레임을 내보낸다는 점을 찾았다고
쓴다.
HTML 명세가 권고하는 동작을 WebKit이 따른 결과라는 설명이다.
이를 합쳐 Liquid Glass 탭 바를 만들었고,
iPhone 18 Pro를 240 FPS로 촬영해 비교한 결과
3초 동안 끌 때 컨트롤러 방식은 평균 118 FPS, 포인터 이벤트 방식은 60 FPS였으며
저전력 모드에서는 30 대신 60이 나왔다고 한다.
저자는 이 모두를 앱 전체에 적용하지는 않겠다고 하며,
애플이 플래그를 풀어 주는 편이 낫다고 덧붙인다.

## 분석

### 스크롤을 입력 장치로 바꾸는 발상

글의 가장 쓸모 있는 부분은 합성기가 하는 일을 자바스크립트가 대신하지 않는다는
점이다.
관성과 튕김, 스냅 지점이 모두 스크롤 영역에 이미 있으므로
읽기만 자주 하면 된다는 계산이다.
그래서 글의 대부분은 “얼마나 자주 읽을 수 있는가”의 실험 기록이다.
각 단계가 해결한 병목과 남긴 병목이 순서대로 적혀 있어서
숫자를 직접 따라 하기 쉽다.

### 출력 쪽의 해법이 가진 전제

`OffscreenCanvas` 우회는 WebKit의 현재 동작에 기댄다.
저자도 애플이 마음먹으면 막을 수 있고, 과거에 비슷한 라이브러리가 막힌 전례가
있다고 인정한다.
따라서 이 기법은 영구한 해법이 아니라 현재 구현의 틈이다.
HN의 afavour는 네이티브에서는 큰 전환에만 120Hz를 선택적으로 켜지만 웹에는 그
스위치가 없어
“항상 120 아니면 아님”이 되고 이는 배터리를 더 쓴다고 설명했다.[^afavour]
이 설명이 맞다면 플래그가 기본으로 켜져 있는 이유가 부분적으로 설명된다.

## 비평

### 차이가 느껴지는지에 관한 의문

글은 iOS Safari에서 두 격자의 차이가 바로 보인다고 쓰지만,
HN에서는 구별하지 못했다는 보고가 많았다.
wodenokoto는 차이가 주사율이 아니라 관성 유무일 뿐이라고 썼고,
저자는 저전력 모드로 켜 보라고 답했다.[^wodenokoto][^ridafkih]
catlifeonmars는 첫 예시가 “최대 60fps”로 갱신된다는 표현이 과장이라고 보았고,
Rohansi는 화면 주사율의 절반으로 자기를 제한하는 것은 차이가 분명히 느껴지는데도
받아들이기 어렵다고 답했다.[^catlifeonmars][^rohansi]
Lobste.rs의 kornel은 자신은 차이를 분명히 느끼며,
macOS가 디스플레이 설정을 잃고 60Hz로 돌아갈 때마다 마우스 포인터가 느려진 것을
안다고 썼다.[^kornel]
david_chisnall은 iPad에서 두 쪽 모두 큰 문제가 없었다며 지터가 더 눈에 띈다고
했다.[^david_chisnall]
기기의 화면이 120Hz인지가 판단을 가르므로, 같은 글을 읽고도 결론이 갈린다.
저자의 주장은 120Hz 기기를 전제로 한 것이다.

### 배터리 비용

Lobste.rs의 AndrewStephens는 기술은 훌륭하지만 하루치 배터리 대신 몇 프레임을 더 얻는 것은 바람직하지 않고,
광고가 120Hz로 갱신되길 원하지 않는다고 썼다.[^AndrewStephens]
olliej는 제목을 “나쁘게 설계된 웹 페이지를 감당하려고 배터리를 다 쓰는 법”으로
바꾸자고 했다.[^olliej]
저자는 iPhone 18 Pro에서 측정한 전력을 제시했다.
유휴 시 유리를 켜면 994mW, 끄면 990mW였고,
스크롤 시 끄면 950mW, 켜고 120Hz면 1,537mW, 60Hz면 1,337mW였다고
한다.[^rida-power]
이 숫자는 120Hz가 60Hz보다 약 15% 더 쓴다는 뜻이다.
다만 측정은 저자 본인이 했고, 비교로 든 상대 페이지의 수치도 저자가 잰 것이다.

### 디자인 논쟁이 기술 논점을 가린다

HN의 nanapipirara는 웹에 Liquid Glass를 넣지 말라고 했고,[^nanapipirara]
CGamesPlay는 스크롤 표시기가 안구 편두통을 재현한다고 썼다.[^CGamesPlay]
저자는 이를 예시일 뿐이라고 했고 끌 수 있는 설정도 넣었다.
기법의 가치와 데모의 미감은 별개이지만, 독자의 반응이 후자로 쏠린 것은 글의 구성
책임도 있다.

## 인사이트

### 기법보다 설계 원칙을 가져간다

저자는 Lobste.rs에서 전체를 따라 할 필요는 없다고 답했다.
필기 앱의 펜 입력이나 PWA 게임처럼 좁은 용도에만 쓰고,
상호작용을 합성기로 옮긴다는 원칙만 가져가도 배터리를 덜 쓰고 보기도 낫다는
것이다.[^rida-takeaway]
이 문서가 보기에 가장 이식하기 쉬운 부분이 바로 이 원칙이다.

### 플랫폼 정책이 만드는 틈

HN의 Rodmine은 Safari가 브라우징에는 충분히 좋고 웹 앱을 만들기에는 충분히
나빠서
개발자가 네이티브 앱을 만들게 하는 위치에 있다고 썼다.[^Rodmine]
다만 이 글이 보여 주는 것은 플랫폼의 제한이 있을 때 우회가 어디서 나오는지,
그리고 그 우회가 언제든 막힐 수 있다는 점이다.

---

[^afavour]: <https://news.ycombinator.com/item?id=50641755>

[^wodenokoto]: <https://news.ycombinator.com/item?id=50640150>

[^ridafkih]: <https://news.ycombinator.com/item?id=50640186>

[^catlifeonmars]: <https://news.ycombinator.com/item?id=50638363>

[^rohansi]: <https://news.ycombinator.com/item?id=50638687>

[^kornel]: <https://lobste.rs/s/pxvmxo/bypassing_ios_safari_60_fps_limit#c_nkiene>

[^david_chisnall]: <https://lobste.rs/s/pxvmxo/bypassing_ios_safari_60_fps_limit#c_v2c0dd>

[^AndrewStephens]: <https://lobste.rs/s/pxvmxo/bypassing_ios_safari_60_fps_limit#c_vl56s1>

[^olliej]: <https://lobste.rs/s/pxvmxo/bypassing_ios_safari_60_fps_limit#c_oixd5y>

[^rida-power]: <https://lobste.rs/s/pxvmxo/bypassing_ios_safari_60_fps_limit#c_leywya>

[^nanapipirara]: <https://news.ycombinator.com/item?id=50639217>

[^CGamesPlay]: <https://news.ycombinator.com/item?id=50638280>

[^rida-takeaway]: <https://lobste.rs/s/pxvmxo/bypassing_ios_safari_60_fps_limit#c_xq3hd9>

[^Rodmine]: <https://news.ycombinator.com/item?id=50639581>
