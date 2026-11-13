# Sand는 모래알 수십만 개를 GPU에서 높이 필드로 묶어 휴대폰 기울기에 반응하게 만든 WebGL2 모래 시뮬레이터이다

<https://av.github.io/safe-sand/>

<https://github.com/av/safe-sand>

HN 토론: <https://news.ycombinator.com/item?id=50453288> (421점, 77개 댓글)

GN 토론: <https://news.hada.io/topic?id=37002>

## 소개

Sand는 휴대폰 화면 위에 진짜 모래를 올려 놓은 것처럼 느끼게 하는 브라우저 장난감이다.
폰을 기울이면 모래가 미끄러지고, 홱 움직이면 모래가 늦게 따라오고, 손가락으로 끌면
고랑이 파이고, 얼굴을 아래로 뒤집으면 모래가 떨어진다.
HTML과 JavaScript만으로 WebGL2 위에서 돌아가고 빌드 단계가 없다.
웹 페이지의 첫 화면은 Pour(붓기) 버튼과 모래 종류, 그리고 모래 밑에 깔릴 화면(밝은 화면,
잠금 화면, 꺼진 화면)을 고르는 카드이다.
iOS에서는 Pour를 누르고 모션 센서 접근을 허용해야 한다.
데스크톱에서는 마우스로 밀고, 화살표 키나 WASD로 기울이고, 스페이스를 눌러 흔든다.

저장소는 GitHub 계정 `av`의 `safe-sand`이고 2026년 11월 11일 11:17(UTC)에 만들어졌다.
이 문서가 읽은 2026년 11월 12일에 별은 103개였다.
커밋 13개가 그날 안에 올라왔고, 모래 시뮬레이션 자체는 처음 몇 시간의 커밋이고
Android 앱과 광고, 유료 구매는 마지막 커밋(#1)에서 더해졌다.
저장소에 라이선스 파일은 없다.
모래는 다섯 종류이다.
River, Beach, Desert, Volcanic, Coral이고, 웹에서는 모두 쓸 수 있다.
주소의 `sand=` 값으로 종류를, `screen=` 값으로 배경을 고를 수 있다.

## 동작 방식

### 모래알 수십만 개를 GPU 텍스처로 시뮬레이션한다

README는 모래알 약 10만~46만 개를 실제 단위(밀리미터, 9.81 m/s²)로 GPU에서 시뮬레이션한다고
적는다.
모래알마다 크기, 광물 색, 마찰이 다르고, 고립된 알은 구르고 튀지만 덩어리 모래는
기울기가 안식각(angle of repose)을 넘을 때까지 달라붙어 있다는 설명이다.
이 문서가 데스크톱 Chrome에서 연 상태에서 `window.sand.info()`는 모래알 400,384개,
모래판 330.5×178.3mm, 격자 661×357이라고 보고했다.

코드를 읽으면 구조가 보인다.[^sim]
모래알의 위치와 속도(x, y, vx, vy), 공중 높이와 수직 속도와 층 정보와 상태를
부동소수점 텍스처 두 장에 담고, 텍스처를 번갈아 쓰는 방식(ping-pong)으로 매 단계를
갱신한다.
갱신은 화면 전체를 덮는 삼각형 하나를 그리는 프래그먼트 셰이더가 맡는다.
알마다 서로의 충돌을 계산하지 않고, 그 대신 격자를 거친다.
모든 알을 점으로 그려 부피에 비례하는 질량과 운동량을 0.5mm 격자에 더하기 혼합
(additive blending)으로 모은 뒤, 3×3 필터와 분리형 가우스 블러를 거쳐 높이 필드를 만들고,
높이의 기울기를 구한다.
갱신 셰이더는 그 높이와 기울기와 격자 평균 속도를 읽어 각 알에 힘을 준다.[^sim-shaders]
이 방식은 입자와 격자를 섞은 계산(입자-격자 혼합)으로 읽히지만 이 문서가 코드를
읽고 붙인 이름이고 README나 코드의 설명이 아니다.

갱신 셰이더가 하는 일은 대략 이렇다.[^sim-shaders]
땅에 닿은 알은 화면 평면에 평행한 중력 성분으로 미끄러지려 하고,
높이 기울기가 마찰이 허용하는 한도(안식각 근처)를 넘을 때에만 기울기 방향의 구동이
더해진다.
작은 알(반지름이 0.12~0.17mm를 넘으면 사라지는 항)에는 반지름의 세제곱에 반비례하는
접착력이 붙어 뭉친다.
격자 평균 속도 쪽으로 자기 속도를 섞고, 속도에 비례하지 않는 마찰을 적용하며,
흔들림(shake)이 크면 알이 느슨해진다.
손가락은 최대 5개의 선분으로 모델링되어 알을 밀어내고 일부는 공중으로 튀게 한다.
벽에서는 반발 계수 0.08(자갈은 0.35)로 튕긴다.
알에는 회전 상태가 없다.
위치와 속도뿐이고 자갈도 점으로 취급된다.

격자에서 읽는 통계(부피, 흐름, 덮은 면적)는 GPU에서 비동기로 읽는다.
픽셀 버퍼 객체와 펜스(fence)를 써서 GPU를 멈추지 않고 이전 프레임의 값을 가져온다.[^sim]

### 보이고 들리고 느끼는 부분

높이 필드는 모래더미의 경사 힘과 자기 그림자와 주변광 차단에도 쓰인다.
조명 방향이 폰의 기울기를 따라가서 기울이면 그림자가 길어지고 석영 알갱이가 반짝인다.
소리는 실제로 움직이는 모래의 양에서 합성한다.
미끄러지는 모래는 초당 수천 번의 작은 공명 클릭(2~8kHz), 자갈은 드문 낮은 클릭, 붓는
소리는 더 밝은 충돌음이고, 아무것도 움직이지 않으면 출력은 정확히 무음이다.
Android에서는 던진 모래가 화면 가장자리에 부딪힐 때 짧게 진동한다.
이 설명은 README의 것이고 이 문서는 소리를 들어 보지 않았다.

기기에 맞춰 화질이 조절된다.
프레임이 2초 동안 느리면 먼저 몇 프레임을 비워 돌려 브라우저가 프레임률을 제한하는 것인지
(예: iOS 저전력 모드의 30fps)를 확인한다.
진짜 과부하일 때만 화질을 낮추고, 장치 픽셀 비율 3, 2, 1.5로 내린 뒤 알의 수를 줄인다.
한 번 낮춘 화질은 세션 중에 다시 올리지 않고, 고른 수준은 다음 방문에 기억해 한 단계 더
낙관적으로 시작한다.

### 웹과 Android 앱

같은 코드가 Capacitor로 Android 앱(`io.github.av.sand`)으로도 나온다.
앱은 웹에 없는 것을 더한다.
시작 화면과 메뉴의 AdMob 배너 광고(플레이하는 동안에는 모래 위에 나오지 않음),
유럽 경제 지역의 Google 동의 양식, 한 번 결제하면 광고를 없애고 Desert, Volcanic, Coral을
여는 Sand Pro이다.
Pro가 없으면 보상형 동영상으로 이 모래를 24시간 연다.
이 모든 것은 `src/app.js`에 있고 웹에서는 아무 일도 하지 않는다.
Play 등록 정보 문서는 Sand Pro를 비소비형 일회성 상품, 가격 2.99달러로 적는다.[^listing]
개인정보 처리방침은 Sand 자체는 아무것도 수집하지 않고 계정, 분석, 자체 서버가 없으며
모션 센서 데이터는 기기에서 실시간으로만 쓰고 저장하거나 보내지 않는다고 밝힌다.
광고는 Android 앱에서만 나오고 웹에는 광고가 없다.
앱에서 광고를 위해 Google Mobile Ads SDK가 광고 ID, 대략의 위치, 광고 상호작용, 진단
데이터를 Google에 수집해 공유한다고도 적는다.[^privacy]

## 분석

### 중심 설계는 알마다 따로 계산하되 상호작용은 격자 하나로 모으는 것이다

가장 강하게 말하면 이 프로젝트는 모래 알갱이 사이의 접촉을 계산하지 않고
알갱이들이 만드는 높이 필드를 통해서만 서로를 느끼게 하는 방식으로 모래의 거동을
만든다.
알 40만 개의 쌍 접촉은 휴대폰 GPU로 감당하기 어렵지만, 점을 격자에 뿌리고 블러해서 높이와
기울기를 얻는 일은 GPU가 잘하는 일이다.
그 대가는 코드에서 보인다.
알에는 회전이 없고 자갈은 점이며 쌓임은 높이 하나로 표현된다.
이 대가는 HN 댓글에서도 나왔다(아래 비평).
이 해석은 코드를 읽은 것이고 저자의 설명이 아니다.

### 현실감은 감각을 겹쳐서 만든다

README의 현실감은 물리 하나가 아니라 겹침에서 나온다.
실제 단위, 알마다 다른 크기와 마찰, 기울기를 따르는 조명, 모래 움직임에서 합성한 소리,
화면 가장자리의 진동, 손가락이 파는 고랑과 양쪽 둑이다.
Play 등록 문서의 설명도 같은 목록이다.[^listing]
HN에서 rybosome은 모래 종류마다 소리의 음색이 다르고 고운 사막 모래는 쉿 소리에 가깝고 거친
화산 모래는 더 딱딱하다고 느꼈으며, 물리 기반이지만 모델이 제한적이라고 짚었다.[^rybosome]
smusamashah는 돌 주변에 물이 있는 것 같고 모래더미가 실제처럼 무너진다고 했다.[^smusamashah]

### 시험 모드로 기울기 임계값을 직접 재 보았다

페이지는 주소에 `test`를 붙이면 `window.sand`로 시뮬레이션을 직접 조작할 수 있게 한다.
`advance(frames)`로 프레임을 진행하고, `gravity([x, y, z])`로 중력을 정하고,
`reset(true, seed)`로 모래를 붓고, `particles()`로 알의 위치와 속도를 읽을 수 있다.[^main]
이 문서는 이 훅으로 README의 주장(덩어리 모래는 기울기가 안식각을 넘을 때까지 달라붙는다)을
확인했다.
데스크톱 Chrome에서 시드 1로 모래를 붓고 5초(300프레임) 가라앉힌 뒤 판을 θ만큼 기울여
4초(240프레임) 동안 둔 뒤, 속도가 5mm/s를 넘는 알의 비율을 쟀다.

| 모래     | 움직이는 알의 비율 (기울기)                          |
| -------- | ---------------------------------------------------- |
| Beach    | 33도까지 0%, 34도에 13.2%, 35도에 14.0%              |
| Volcanic | 38도까지 0%, 42도에 3.7%, 46도에 13.9%, 50도에 15.4% |
| Desert   | 50도까지 0%                                          |

Beach는 33도와 34도 사이에서 한꺼번에 움직이기 시작했고, 그 아래에서는 한 알도
5mm/s를 넘지 않았다.
Volcanic은 38도와 42도 사이, Desert는 50도까지도 덩어리째 움직이지 않았다.
이 결과는 README의 설명과 맞고, 종류마다 마찰과 접착이 다르다는 설정과도 맞는다.
Desert가 끝까지 안 움직인 것은 작은 알에 붙는 접착력이 큰 설정 때문으로 읽히고(이 문서는
설정값의 의미를 확인하지 않았다), HN에서 catapart가 말한 사막 모래가 더 뭉친다는 인상과 같다.[^catapart]
한계는 분명하다.
이 값은 한 번의 시드, 한 번의 기울이기 방식, 5mm/s라는 임의의 기준에 대한 것이고
실제 모래의 안식각과 비교한 것이 아니다.
이 문서는 실제 모래의 값을 측정하거나 인용하지 않았다.
따라서 이 표는 시뮬레이션이 안식각 근처의 임계값을 갖는다는 것만 보여 주고,
그 값이 현실과 맞는다고 보여 주지는 않는다.

```js
// 주소에 test를 붙여 연 페이지의 콘솔에서 실행한다.
const s = window.sand;
for (const deg of [30, 34, 38]) {
  s.gravity([0, 0, 9.81]);
  s.reset(true, 1);          // 모래를 붓는다 (시드 1)
  s.advance(300);            // 5초 가라앉힌다
  const t = deg * Math.PI / 180;
  s.gravity([9.81 * Math.sin(t), 0, 9.81 * Math.cos(t)]);
  s.advance(240);            // 4초 기울인다
  const { A, B } = s.particles();
  let n = 0, moving = 0;
  for (let i = 0; i < A.length / 4; i++) {
    if (B[i * 4 + 3] < 0.5) continue;
    n++;
    if (Math.hypot(A[i * 4 + 2], A[i * 4 + 3]) > 5) moving++;
  }
  console.log(deg, (moving / n).toFixed(3));
}
```

## 비평

### 기기에 따른 성능이 크게 다르고 화질 조절이 이를 다 막지는 못한다

README는 화질이 기기에 적응하고 느리면 낮춘다고 하지만 HN에는 다른 보고가 있다.
techpression은 iPhone 15 Pro에서 10fps쯤이라고 했고, iberator는 3년 된 Android에서
10fps, flykespice는 2021년의 보급형 Android에서 슬라이드쇼 같다고 했다.[^techpression][^iberator][^flykespice]
lloydatkinson은 iPhone 14에서 형편없이 돈다고 했는데 Wowfunhappy는 iPhone 13에서 잘 돈다고
답했고, Faint는 OnePlus 13에서 매끄럽다고 했다.[^lloyd][^wowfunhappy][^faint]
leobuskin은 iOS Chrome에서 이상한 애니메이션이 나온 뒤 모래가 모두 사라지고 Pour 버튼이
다시 나온다고 했다.[^leobuskin]
README의 적응은 프레임이 2초 동안 느릴 때에만 작동하고 한 번 내린 화질은 올리지 않는다.
기기 사이의 큰 차이와 이 보고들을 이 문서가 확인하지는 못했다.
데스크톱에서 측정한 프레임은 59.9fps였다.

### 현실감이라는 주장에 대한 반박이 구체적이다

제목은 hyper-realistic이지만 README는 real-feeling이라고 쓴다.
techpression은 현실적이라고 부르기 어렵다며 돌이 회전하지 않고 각도에 따라 기이한 골짜기
효과가 있다고 했고, vfosnar는 압력이 쌓였다가 튕겨 나오는 효과가 몰입을 깬다고 했다.[^techpression][^vfosnar]
wigster는 스톱모션 영화를 보는 것 같다고 했고 refactor_master가 같은 인상을 말했다.[^wigster][^refactor-master]
nkmnz는 돌이 너무 빠르고 마찰이 더 필요하다고 했다.[^nkmnz]
돌이 회전하지 않는다는 지적은 코드와 맞는다.
알의 상태에 회전이 없기 때문이다.[^sim]
README는 이 실제 거동의 일치를 보였다고 주장하지 않지만(느낌에 대한 설명),
제목의 표현은 그 이상을 약속한다.
시뮬레이션 자체의 테스트는 저장소에 없고 테스트 폴더에는 Android 앱 통합 테스트 하나뿐이다.
이 문서가 확인한 한 가지는 위 임계값 시험뿐이다.

### 소리가 기본으로 켜져 있고 일부에게는 거슬린다

evnp는 매우 큰 소리 경고가 필요하다며 부모와 헤드폰 사용자를 위해 기본을 소리 끔으로 하거나
Pour를 누르기 전에 볼륨을 낮추라는 안내를 달라고 했고, codingjinxx는 수업 중에 열고 음소거를
잊었다고 했다.[^evnp][^codingjinxx]
jarjoura는 소리 효과를 아예 빼겠다고 했고 smusamashah는 소리가 좋지 않다고 했으며,
andai는 소리가 끝없이 일그러진 잡음이었다고 했다.[^jarjoura][^smusamashah][^andai]
README는 iPhone의 무음 스위치가 소리를 끄고 이미 재생 중인 음악과 섞인다고 적는다.
시작 카드의 소리 토글은 기본으로 켜진 상태로 보인다.

### 라이선스가 없어서 재사용할 수 없다

hjun1052는 라이선스가 있으면 개미를 더하고 싶었을 것이라고 했다.[^hjun1052]
저장소에는 LICENSE 파일이 없고 GitHub API도 라이선스를 알려 주지 않는다.
라이선스가 없는 코드는 기본적으로 사용 허가가 없는 코드이다.
그럼에도 저자는 이 코드를 공개된 소스로 두었다.

## 인사이트

### 40만 개를 휴대폰에서 돌리는 방법을 한 가지로 읽을 수 있다

이 프로젝트에서 가져갈 기법이 여럿 있다.
상태를 부동소수점 텍스처 두 장에 담아 번갈아 쓰는 것, 입자를 점으로 그려 격자에 더하는 것,
격자를 블러해서 기울기를 얻는 것, 통계를 PBO와 펜스로 비동기 읽는 것이다.
화질 조절의 아이디어도 눈에 띈다.
프레임이 느릴 때 곧바로 화질을 낮추지 않고 비워 돌려서 브라우저가 프레임률을 제한하는지부터
확인하고, 낮춘 화질은 올리지 않으며 다음 방문의 시작점으로 기억한다.
이 정리는 이 문서의 것이다.

### 성능을 확인하려면 격자 해상도와 모래알 수를 바꿔 측정한다

주소 매개변수로 모래알 수 상한(`n=`)과 알 밀도(`density=`)와 픽셀당 길이(`ppi=`)를 바꿀 수
있고, `window.sand.info().quality`가 현재 화질 단계를 알려 준다.
이 문서의 제안은 보고된 10fps 기기에서 `n=`을 단계별로 줄이며 프레임을 측정해 화질 조절이
왜 충분히 내려가지 않는지를 보는 것이다.
이 제안은 이 문서의 것이고 이 문서는 해당 기기에서 시험하지 못했다.

### 기울기 시험은 변경 사항을 감시하는 회귀 시험이 될 수 있다

앞의 임계값 시험은 코드 열 줄이다.
모래 종류별 임계값 범위(예: Beach 33~34도)를 기록해 두고 셰이더를 고칠 때마다 다시 돌리면
물리 설정이 의도치 않게 바뀌었는지를 알 수 있다.
저장소의 테스트가 Android 통합뿐이라는 점을 보완하는 제안이다.

### 이 프로젝트의 주장을 확인할 관찰

현실감의 근거는 실제 모래와의 비교이다.
실제 모래판의 기울기 시험(같은 판과 같은 모래로 안식각 측정)을 시뮬레이션의 임계값과
비교하면 안식각의 현실 일치를 볼 수 있다.
일치한다면 마찰 설정이 잘 맞춰진 것이고, 어긋나면 느낌 위주의 조정이라는 뜻이다.
이 비교는 이 문서가 하지 않았고 제안이다.

---

[^sim]: av, [src/sim.js](https://github.com/av/safe-sand/blob/main/src/sim.js)

[^sim-shaders]: av, [src/sim-shaders.js](https://github.com/av/safe-sand/blob/main/src/sim-shaders.js)

[^main]: av, [src/main.js](https://github.com/av/safe-sand/blob/main/src/main.js)

: av, [README.md](https://github.com/av/safe-sand/blob/main/README.md)

[^listing]: av, [store/listing.md](https://github.com/av/safe-sand/blob/main/store/listing.md)

[^privacy]: av, [Sand: privacy policy](https://av.github.io/safe-sand/privacy.html), 2026-11-11

[^rybosome]: <https://news.ycombinator.com/item?id=50459520>

[^smusamashah]: <https://news.ycombinator.com/item?id=50455710>

[^catapart]: <https://news.ycombinator.com/item?id=50455940>

[^techpression]: <https://news.ycombinator.com/item?id=50454971>

[^iberator]: <https://news.ycombinator.com/item?id=50460931>

[^flykespice]: <https://news.ycombinator.com/item?id=50457190>

[^lloyd]: <https://news.ycombinator.com/item?id=50456520>

[^wowfunhappy]: <https://news.ycombinator.com/item?id=50462655>

[^faint]: <https://news.ycombinator.com/item?id=50466046>

[^leobuskin]: <https://news.ycombinator.com/item?id=50454683>

[^vfosnar]: <https://news.ycombinator.com/item?id=50455372>

[^wigster]: <https://news.ycombinator.com/item?id=50455304>

[^refactor-master]: <https://news.ycombinator.com/item?id=50464746>

[^nkmnz]: <https://news.ycombinator.com/item?id=50456963>

[^evnp]: <https://news.ycombinator.com/item?id=50457710>

[^codingjinxx]: <https://news.ycombinator.com/item?id=50466340>

[^jarjoura]: <https://news.ycombinator.com/item?id=50455947>

[^andai]: <https://news.ycombinator.com/item?id=50460787>

[^hjun1052]: <https://news.ycombinator.com/item?id=50465386>
