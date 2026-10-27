# Backdrop: 효과 조각을 조립해 Liquid Glass 컴포넌트를 직접 만드는 Compose 라이브러리

<https://kyant.gitbook.io/backdrop>

<https://github.com/Kyant0/AndroidLiquidGlass>

## 소개

Backdrop은 Kyant가 만든 Compose Multiplatform용 Liquid Glass 효과 라이브러리다.
저장소 이름은 `AndroidLiquidGlass`이고
Maven 좌표는 `io.github.kyant0:backdrop`이다.
라이선스는 Apache-2.0이고 저장소는 2025년 6월에 만들어졌다.
이 문서를 쓴 2026년 10월 20일 기준 GitHub 별은 약 4,200개이고
최신 릴리스는 2026년 8월 26일의 2.0.1이다.

README가 가장 먼저 밝히는 점은 고수준 컴포넌트가 없다는 것이다.
버튼, 토글, 슬라이더,
하단 탭은 예제 앱(Backdrop Catalog)의 소스 파일로만 제공되고,
의존성으로 받는 것은 backdrop을 그리는 기본 요소와 효과다.
그래서 이 라이브러리는 버튼 하나를 가져다 쓰는 용도가 아니라,
자기 디자인의 Liquid Glass 요소을 만드는 재료로 읽어야 한다.

## 동작 방식

### backdrop은 뒤 화면의 복사본이다

문서가 설명하는 핵심 개념은 한 줄이다. 뒤 화면(backdrop)의
복사본을 앞쪽 요소에 여러 효과를 입혀 그린다.
복사본을 만드는 방법에 따라 backdrop 종류가 나뉜다.

| 종류                       | 용도                                                                      |
| -------------------------- | ------------------------------------------------------------------------- |
| `rememberLayerBackdrop`    | `Modifier.layerBackdrop`으로 컴포저블의 내용을 그려 둔다. 좌표에 의존한다 |
| `rememberCanvasBackdrop`   | 빈 backdrop에 원하는 내용을 직접 그린다. 좌표에 의존하지 않는다           |
| `rememberCombinedBackdrop` | 여러 backdrop을 하나로 합친다. 탭과 슬라이더 같은 컴포넌트에 쓴다         |
| `rememberBackdrop`         | 사용자 지정 그리기 명령으로 backdrop을 그린다                             |
| `emptyBackdrop`            | 아무것도 그리지 않는다                                                    |

요소에는 `Modifier.drawBackdrop`을 붙인다.
튜토리얼에 나오는 매개변수는 `backdrop`, `shape`, `effects`,
`onDrawSurface`, `exportedBackdrop`, `layerBlock`, `shadow`다.

### 효과는 RenderEffect이고 순서가 정해져 있다

문서는 backdrop 효과가 근본적으로 `RenderEffect`라서
Android 12 이상에서만 적용된다고 적는다.
`RuntimeShader`를 쓰는 효과는 Android 13 이상이어야 한다.
효과는 반드시 색 필터, 블러, 렌즈 순서로 적용해야 한다.

| 효과                                                                         | 내용                                                           | 조건                 |
| ---------------------------------------------------------------------------- | -------------------------------------------------------------- | -------------------- |
| `colorFilter`, `opacity`, `colorControls`                                    | 밝기, 대비, 채도 조정                                          | Android 12+          |
| `vibrancy()`                                                                 | 채도에 1.5를 곱한다. `colorControls(saturation = 1.5f)`와 같다 | Android 12+          |
| `exposureAdjustment`                                                         | 노출 보정                                                      | Android 12+          |
| `gammaAdjustment`                                                            | 감마 보정                                                      | Android 13+          |
| `blur(radius, edgeTreatment)`                                                | 블러                                                           | Android 12+          |
| `lens(refractionHeight, refractionAmount, depthEffect, chromaticAberration)` | 굴절                                                           | Android 13+          |
| `effect`, `runtimeShaderEffect`                                              | 직접 만든 `RenderEffect` 또는 AGSL 셰이더                      | 셰이더는 Android 13+ |

렌즈에는 제약이 둘 있다.
`shape`는 `CornerBasedShape`여야 하고,
굴절 높이는 0 이상 모서리 반지름의 최솟값 이하여야 한다.
굴절량은 0 이상 요소의 짧은 변 이하여야 한다.
범위를 넘으면 일부 모서리에서 불연속이 생기지만 허용 가능하다고 문서는 적는다.

## 사용하기

가장 짧은 완성 예제는 하단 바 튜토리얼의 최종 코드다.
화면 전체를 `layerBackdrop`으로 기록하고, 그 위에 유리 요소을 하나 얹는다.

```kotlin
Box(Modifier.fillMaxSize()) {
    val backgroundColor = Color.White
    val backdrop = rememberLayerBackdrop {
        drawRect(backgroundColor)
        drawContent()
    }

    MainNavHost(
        modifier = Modifier.layerBackdrop(backdrop)
    )

    Box(
        Modifier
            .safeContentPadding()
            .drawBackdrop(
                backdrop = backdrop,
                shape = { CircleShape },
                effects = {
                    vibrancy()
                    blur(4f.dp.toPx())
                    lens(16f.dp.toPx(), 32f.dp.toPx())
                },
                onDrawSurface = { drawRect(Color.White.copy(alpha = 0.5f)) }
            )
            .height(64f.dp)
            .fillMaxWidth()
            .align(Alignment.BottomCenter)
    )
}
```

튜토리얼은 이 코드를 네 번에 걸쳐 완성하며 각 줄의 이유를 밝힌다.

- `rememberLayerBackdrop { drawRect(...); drawContent() }`: 화면
내용 바깥 영역의 배경도 backdrop에 그려야 한다. 그리지 않으면
하단 바에 투명 픽셀이 섞여 효과가 잘못 보인다.
- `vibrancy()`와 `blur(4.dp)`와 `lens(...)`: 순서를 지켜 채도,
블러, 굴절 순으로 쌓는다.
- `onDrawSurface`의 반투명 흰색: 가독성을 위한 면이다. 튜토리얼은
아름다움과 가독성 사이의 균형을 잡아야 한다고 적는다.

## 문서가 알려 주는 함정

### 눌렀을 때 backdrop까지 확대된다

누르면 커지는 효과를 `graphicsLayer`에 넣으면
요소과 함께 backdrop도 커져 위치가 어긋난다.
해결은 같은 크기 조정 코드를 `drawBackdrop`의 `layerBlock`으로 옮기는 것이다.
backdrop은 확대되면 안 된다는 것이 튜토리얼의 설명이다.

### 유리 위의 유리는 앱을 죽인다

바텀 시트 위에 유리 버튼을 얹고 시트를 그 버튼의 backdrop으로 쓰려고
`layerBackdrop`을 새로 만들면,
내용이 자기 자신을 그리는 순환이 생겨 `RenderThread`에서
`Fatal signal 11 (SIGSEGV)`로 죽는다.
FAQ가 이 충돌의 대표 사례로 이 튜토리얼을 가리킨다.
해법은 `drawBackdrop`의 `exportedBackdrop`을 쓰는
것이다. 이 매개변수는 내용 그리기를 건너뛴다.

### 배경과 트랙을 함께 굴절시키려면 합친다

슬라이더 튜토리얼은 thumb이 트랙과 뒤 배경을 동시에 굴절시키도록
`rememberCombinedBackdrop(backdrop, trackBackdrop)`을 쓴다.
튜토리얼은 `trackBackdrop`만 쓰는 경우, `backdrop`만 쓰는 경우,
둘을 합친 경우를 차례로 보여 주고 합친 경우에 둘이 동시에 굴절된다고 적는다.

### 점진 블러는 아직 정확한 방식이 없다

점진 블러 튜토리얼은 알파 마스크를 곱하는 방식만 보여 주고,
정확한 점진 블러는 TBD라고 적는다.
알파 마스크 방식은 AGSL 셰이더를 쓰므로 Android 13 이상 검사가 코드에 들어 있다.

## 트레이드오프

### 자유도를 얻는 만큼 가독성과 폴백은 앱이 책임진다

컴포넌트를 주지 않는 설계는 디자인을 원하는 대로 만들 수 있다는 뜻이다.
반대로 접근성 설정(투명도 감소,
대비 증가)에 반응하는 장치를 라이브러리가 대신 주지 않는다.
이 문서가 읽은 README와 튜토리얼과 API 페이지에는 그런 설정을 다루는 내용이
없다. 있어도 이 문서가 못 찾았을 수 있으니,
확인하려면 저장소를 직접 검색해야 한다.

### 낮은 버전의 동작이 문서에 없다

라이브러리의 `minSdk`는 21이지만
효과는 Android 12 이상에서만 적용된다고 문서가 적는다.
그 아래에서 앱이 무엇을 보게 되는지,
폴백을 라이브러리가 주는지는 읽은 문서에 없다.
API 31 미만 기기를 지원하는 앱은 직접 실행해 확인하고
대체 화면을 따로 준비해야 한다.

### 최신 도구 체인에 맞춰 빌드된다

저장소의 빌드 설정은 Compose Multiplatform 1.12.0과 Kotlin 2.4.10,
AGP 9.3.2를 쓰고 `compileSdk`는 37이다.
라이브러리를 받는 앱의 Compose와 Kotlin 버전이 이에서 크게 뒤처지면
맞지 않을 수 있다. 이 문서는 호환 범위를 확인하지 못했다.

## 체크리스트

- backdrop에 화면 내용 바깥의 배경까지 그렸는가.
- 효과 순서가 색 필터, 블러, 렌즈인가.
- `lens`를 쓰는 요소의 `shape`가 `CornerBasedShape`인가.
- 유리 위의 유리에서 `exportedBackdrop`을 썼는가.
- 눌림 같은 크기 변화를 `layerBlock`으로 옮겼는가.
- 글자 대비를 직접 측정하고 `onDrawSurface`의 알파를 조정했는가.
- API 31 미만과 31~32 구간에서 대체 화면이 있는가.

## 기억할 원칙

### backdrop은 그리는 순서의 문제다

이 문서가 읽은 함정 세 가지(바깥 배경, 순환 충돌, 확대)는 모두 같은 원인이다.
무엇이 backdrop에 기록되고, 언제 그려지고, 어떤 변환을 받는지를 앱이 정한다.
효과를 고르기 전에 이 세 가지를 먼저 그림으로 그려
보는 것이 이 라이브러리를 쓰는 가장 빠른 길이다.
