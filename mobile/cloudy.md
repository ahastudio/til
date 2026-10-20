# Cloudy: 블러와 렌즈와 셰이더 효과를 독립된 modifier로 나눈 Kotlin Multiplatform 라이브러리

<https://github.com/skydoves/Cloudy>

## 소개

Cloudy는 skydoves(Jaewoong Eum)가 만든 Compose용 Kotlin Multiplatform용 시각 효과 라이브러리다.
2022년 11월에 Compose용 블러의 백포트로 시작해,
지금은 뒤 화면 블러와 Liquid Glass 렌즈, 셰이더 효과까지 다룬다.
라이선스는 Apache-2.0이다.
이 문서를 쓴 2026년 10월 20일 기준 GitHub 별은 약 1,300개다.

버전 상황을 먼저 알아 둘 필요가 있다.
README의 Gradle 예시는 `com.github.skydoves:cloudy:1.0.0-alpha01`을 가리키는데,
이것은 2026년 7월 17일에 나온 프리릴리스다.
정식 릴리스의 최신은 2026년 7월 12일의 0.7.1이다.
그래서 README의 설명은 알파를 기준으로 쓴 것으로 보이고,
안정 버전으로 시작하면 API가 다를 수 있다. 이 문서는
두 버전의 차이를 대조하지 않았다.

## 효과 네 가지

README는 서로 독립된 효과 네 개를 소개한다. 필요한 것만 골라 조합한다.

| 효과          | modifier                      | 하는 일                                           |
| ------------- | ----------------------------- | ------------------------------------------------- |
| Self blur     | `Modifier.cloudy(radius = …)` | 컴포저블 자신의 내용을 흐린다                     |
| Backdrop blur | `Modifier.cloudy(sky = …)`    | 컴포저블 뒤의 내용을 흐린다                       |
| Liquid Glass  | `Modifier.liquidGlass(…)`     | 굴절과 색 분산이 있는 유리 렌즈를 그린다          |
| Mirage        | `Modifier.mirage { }`         | 박막 간섭과 반사 같은 셰이더 효과 계획을 적용한다 |

이름이 비슷한 두 `cloudy` 호출은 입력이 다르다. `radius`를 넘기면 자기 내용,
`sky`를 넘기면 뒤 화면이다.

## 뒤 화면 블러

뒤 화면 블러는 세 요소로 구성된다. `rememberSky()`가 캡처한 배경의 상태를 들고,
`Modifier.sky(sky)`가 원본 컨테이너를 표시하며,
`Modifier.cloudy(sky = sky, ...)`가 덮을 요소에서 흐린 배경을 그린다.

```kotlin
val sky = rememberSky()

Box(modifier = Modifier.fillMaxSize()) {
  // 1) Source — the content captured for blur
  LazyVerticalGrid(
    columns = GridCells.Fixed(2),
    modifier = Modifier.sky(sky),
  ) {
    items(posters) { poster -> GridPosterItem(poster) }
  }

  // 2) Overlay — a frosted glass app bar that blurs the grid behind it
  Box(
    modifier = Modifier
      .fillMaxWidth()
      .height(56.dp)
      .cloudy(
        sky = sky,
        radius = 20,
        tint = MaterialTheme.colorScheme.surface.copy(alpha = 0.3f),
      )
  ) {
    Text("Frosted Glass App Bar")
  }
}
```

주요 매개변수는 다음과 같다.

| 매개변수         | 기본값                   | 의미                                                             |
| ---------------- | ------------------------ | ---------------------------------------------------------------- |
| `radius`         | 20 (픽셀)                | 블러 반경. 0 이상                                                |
| `shape`          | `RectangleShape`         | 블러가 잘리는 모양. 둥근 요소에는 직접 넘겨야 한다               |
| `tint`           | 투명                     | 흐린 배경 위에 섞는 색                                           |
| `progressive`    | `CloudyProgressive.None` | 위에서 아래, 아래에서 위, 가장자리 방식의 점진 블러              |
| `light`          | `null`                   | 실험적인 움직이는 반사 하이라이트. API 33 이상에서만 효과가 있다 |
| `cpuBlurEnabled` | `false`                  | Android 11 이하에서 CPU 블러를 켠다                              |

### 버전별 동작

| API 수준 | 구현                                            | 점진 블러   |
| -------- | ----------------------------------------------- | ----------- |
| 33 이상  | AGSL `RuntimeShader`                            | 지원        |
| 31~32    | `RenderEffect`                                  | 균일 블러만 |
| 30 이하  | 비트맵과 CPU(`cpuBlurEnabled`일 때) 또는 스크림 | 균일 블러만 |

Android 11 이하에서는 성능을 우선해 CPU 블러가 기본으로 꺼져 있고,
반투명 스크림(`CloudyState.Success.Scrim`)을 대신 보여 준다.

### 갱신 방식

배경이 스크롤되거나 움직이는 동안은 자동으로 다시 캡처하고,
멈추면 프레임 갱신을 멈춘다.
이미지 로딩 완료처럼 스크롤이나 애니메이션이 아닌
변화에는 `sky.invalidate()`를 직접 불러야 한다.
탭 전환 같은 정해진 길이의 전환에는
`sky.invalidate(durationMillis = 240)`처럼 길이를 넘긴다.

## Liquid Glass 렌즈

`Modifier.liquidGlass()`는 SDF 기반 가장자리와 법선 기반 굴절,
색 분산을 갖는 렌즈를 그린다.
README의 기본 예제는 이미지를 담은 `Box`에
`.cloudy(radius = 15).liquidGlass(lensCenter = lensCenter)`를 붙이고,
드래그로 렌즈 위치를 옮긴다.
즉 이 예제의 렌즈는 modifier가 붙은 컴포저블 자신의 내용을 왜곡한다.
README는 블러는 `cloudy()`로 따로 쓰라고 하고 두 효과가 독립적이라고 분명히 적는다.

핵심 매개변수의 폴백은 다음과 같다.

| 매개변수                                             | API 32 이하 폴백             |
| ---------------------------------------------------- | ---------------------------- |
| `lensCenter`, `lensSize`, `cornerRadius`, `tint`     | 동작                         |
| `edge`                                               | 가장자리 선으로 근사         |
| `saturation`, `contrast`                             | 근사                         |
| `refraction`, `curve`, `dispersion`, `light`, `glow` | 동작 안 함(API 33 이상 필요) |

폴백은 틴트와 가장자리 조명과 색 조정이 있는 렌즈 모양만 그린다.
굴절은 `RuntimeShader`가 필요해서 API 33 이상에서만 된다.

기울기에
따라 반사가 움직이는 자이로 기반
광원(`rememberGyroLightSource`)은 실험 기능이다.
Reduce Motion이 켜져 있으면 광원을 얼리고
센서를 등록하지 않는다고 README가 적는다.
iOS에서는 앱의 `Info.plist`에 `NSMotionUsageDescription`이 없으면
모션 센서를 읽을 때 앱이 종료될 수 있다고 경고한다.

## Mirage

`Modifier.mirage { }`는 개방형 셰이더 효과 계획을 컴포저블에 적용한다.
박막 간섭 계열 프리셋(`Chromatic`, `OilSlick`, `SoapBubble`,
`MetallicFoil`, `Pearl`)과 `Specular`, `Foil`, `Duotone`을 기본으로 갖는다.
직접 셰이더를 쓰는 `Optic.composite`와 `colorize`, `generate`, `raw`도 있다.
README는 Mirage가 실험적 옵트인(`ExperimentalMirage`)이고
안정 ABI에서 제외되어 있다고 밝힌다.

## 트레이드오프

### 뒤 화면 유리 요소를 만들려면 조합이 필요하다

README의 Liquid Glass 예제는 자기 내용을 왜곡하는 렌즈이고,
뒤 화면을 캡처한 backdrop 위에 굴절을 입히는
예제는 이 문서가 읽은 README에 없다.
스크롤하는 목록 위에 뜨는 하단 바에서 뒤 화면이 굴절돼 보이게 하려면
`sky` 기반 블러와 렌즈를 어떻게 합치는지 직접 확인해야 한다.
이 문서는 그 조합을 실행해 보지 못했다.

### 낮은 버전을 가장 보수적으로 다룬다

Android 11 이하에서 CPU 블러를 기본으로 끄고
스크림을 보여 주는 것은 성능 위주의 선택이다.
굴절이 빠져도 뒤 화면 블러는 API 31부터 GPU로 동작한다.
README는 버전별 동작을 표로 정리해 두었다. 대신 렌즈의 굴절은 API 33 미만에서
포기해야 한다.

### 알파 API와 실험 기능이 섞여 있다

핵심인 `1.0.0-alpha01` 외에도 Mirage와 자이로 광원이 실험 기능이다.
프로덕션에 넣으려면 정식 버전의 API와 README의 알파 API 차이를 확인해야 한다.

## 함정

- `Modifier.sky`를 붙이지 않으면 뒤 화면 블러에 캡처된 배경이 없다.
- 둥근 요소에 블러를 입힐 때 `shape`를 넘기지 않으면
직사각형 블러가 둥근 유리 안에 남는다.
- 이미지 로딩처럼 스크롤이 아닌 변화는 자동 갱신되지 않으므로
`sky.invalidate()`를 불러야 한다.
- 뒤 화면 블러의 `radius`는 dp가 아니라 픽셀이라고
README가 적는다. 같은 값이 화면 밀도에 따라 다르게 보일 수 있다.
- iOS에서 자이로 광원을 쓰려면 `NSMotionUsageDescription`을 선언해야 한다.

## 체크리스트

- 안정 버전(0.7.x)과 알파(1.0.0-alpha) 중 무엇을 쓰는지 정했는가.
- 원본 컨테이너에 `Modifier.sky(sky)`를 붙였는가.
- 둥근 요소에 같은 `shape`를 넘겼는가.
- API 31 미만과 31~32와 33 이상 각각을 실기기나 에뮬레이터로 확인했는가.
- 굴절이 빠진 폴백에서 의미가 전달되는가.
- 콘텐츠가 비동기로 바뀔 때 `invalidate()`를 불렀는가.

## 기억할 원칙

### 효과마다 입력이 자기 내용인지 뒤 화면인지부터 확인한다

Cloudy는 같은 이름의 modifier가 입력에 따라 다른 일을 한다.
`radius`는 자기 내용, `sky`는 뒤 화면이고, 렌즈는 자기 내용이다.
유리 요소를 만들 때는 효과 이름이 아니라 이 입력이 무엇인지부터 확인해야 한다.
