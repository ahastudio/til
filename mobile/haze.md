# Haze: 뒤 화면을 캡처해 블러와 Glass를 입히는 Compose Multiplatform 라이브러리

<https://chrisbanes.github.io/haze/>

<https://github.com/chrisbanes/haze>

HN 토론: <https://news.ycombinator.com/item?id=38081798> (1점, 0개 댓글)

## 소개

Haze는 Chris Banes가 2023년 10월에 시작한
Compose Multiplatform용 시각 효과 라이브러리다.
저장소 설명은 Compose Multiplatform과 Jetpack Compose에서
뒤 화면을 흐리게 하는 것이고,
지금은 Glass라는 굴절 효과까지 같은 구조 위에 올려 둔다.
라이선스는 Apache-2.0이다.
이 문서를 쓴 2026년 10월 20일 기준 GitHub 별은
약 2,600개이고, 2.0.0이 2026년 9월 22일, 2.0.1이 9월 29일에 나왔다.

README는 아직 Haze 2.0이 베타라고 적고 있다.
그러나 저장소의 릴리스 목록에는 정식 2.0.0과 2.0.1이 있으므로
README의 그 문장은 뒤처진 것으로 보인다.
Haze 2.0 소개 글도 2.0이 나왔다고 쓴다.[^haze2]

## 모듈 구성

Haze는 필요한 효과만 골라 받도록 모듈이 나뉘어 있다.
모든 Haze 아티팩트는 같은 버전으로 맞춰야 한다고 README는 분명히 적는다.

| 아티팩트               | 역할                                                  |
| ---------------------- | ----------------------------------------------------- |
| `haze`                 | 원본(source) 캡처와 직접 효과를 만드는 API            |
| `haze-blur`            | 블러. 캡처한 원본이나 modifier 자신의 내용에 적용한다 |
| `haze-blur-materials`  | `HazeMaterials.thin()` 같은 미리 만든 블러 스타일     |
| `haze-blur-material3`  | Material 3 surface 색을 따르는 블러 스타일            |
| `haze-glass`           | 굴절을 쓰는 Glass 효과                                |
| `haze-glass-material3` | Material 3 surface 색을 따르는 Glass 스타일           |

`haze-blur-materials`의 프리셋은 `ultraThin()`,
`thin()`, `regular()`, `thick()`, `ultraThick()`다.
Material 3 쪽 연동은 따로 `-material3` 아티팩트가 맡는다.

## 동작 방식

### 입력은 세 가지다

Haze 2의 효과는 무엇을 입력으로 받는지 명시해야 한다.

| 입력                        | 의미                                                              |
| --------------------------- | ----------------------------------------------------------------- |
| `HazeInput.Backdrop(state)` | 같은 창에서 이미 그려진 뒤쪽 픽셀. 원본 캡처가 대체 경로          |
| `HazeInput.Sources(state)`  | `hazeSource`로 표시한 콘텐츠만 캡처. 선택과 보존 정책을 직접 정함 |
| `HazeInput.Content`         | modifier가 붙은 컴포저블 자신의 내용                              |

가장 기본인 사용은 뒤 화면이 될 콘텐츠에 `hazeSource(state)`를 붙이고,
그 위에 올릴 요소에 `hazeBlur` 또는 `hazeGlass`를 붙이는 것이다.

```kotlin
val hazeState = rememberHazeState()

Box {
    Image(
        painter = painter,
        contentDescription = null,
        modifier = Modifier.hazeSource(hazeState),
    )
    Box(
        modifier = Modifier
            .matchParentSize()
            .hazeBlur(
                input = HazeInput.Sources(hazeState),
                style = HazeBlurStyle { blurRadius(20.dp) },
            ),
    )
}
```

문서는 내장 블러와 Glass에는 `HazeInput.Backdrop`을 일반적인 선택으로 안내한다.
Backdrop 입력의 네이티브 경로는 아직 실험 기능이라서
`HazeFeatureFlags.isPlatformBackdropEnabled`를 켜야 하고,
켜도 보장이 아니라 가능 조건일 뿐이다.
조건은 Android 37.2 창, 하드웨어 가속 캔버스,
내장 효과 지원이 모두 맞아야 한다는 것이다.
이 경로에서는 같은 창에서 이미 그려진 픽셀만 보이고,
나중에 그려지는 내용이나 다이얼로그와 팝업은 볼 수 없다.

### 스타일은 불변이고 이어 붙인다

`HazeBlurStyle`과 `GlassStyle`은 불변 값이고 `then`으로 변형한다.
스타일을 적용하는 순서는 기본값, 지역 값(`CompositionLocal`),
명시한 스타일 순이고 마지막에 쓴 값이 이긴다.
같은 스타일을 여러 요소에 재사용할 수 있고,
값을 바꾸려면 새 스타일을 만들어 넘겨야 한다.

## Glass

Glass는 굴절과 깊이를 나타내는 블러, 틴트,
가장자리 밝기, 반사 하이라이트를 합친 효과다.
내장 스타일은 둘이다.

- `GlassStyle.regular`: 요소의 짧은 변에 맞춰 블러와 깊이가 달라진다. 짧은
변이 64, 176, 220dp일 때 블러 반경은 각각 20, 24, 25dp이고
깊이는 0.65, 1, 1이다.
- `GlassStyle.clear`: 크기와 상관없이 얕은 블러를 쓰고
가장자리 굴절을 강하게 한다.

문서는 이 두 스타일이 Apple의 구분에서 영감을 받았고
Apple 플랫폼과 픽셀까지 같지는 않다고 분명히 적는다.
글이 많은 요소에는 regular를,
사진과 영상 위의 컨트롤에는 clear를 쓰라고 안내한다.
밝은 배경 위의 clear에는 어두운 층이 필요할 수 있지만
Haze가 자동으로 넣지 않는다.

```kotlin
// Requires opting in to ExperimentalHazeApi.
Modifier.hazeGlass(
    input = HazeInput.Sources(hazeState),
    style = GlassStyle.regular.then {
        shape(RoundedCornerShape(20.dp))
        tint(Color.White.copy(alpha = 0.16f))
    },
)
```

Haze 2.0 소개 글은 Glass가 2.0에서 실험 단계이고
2.1에서 API를 안정화하는 것이 목표라고 한다.[^haze2]
저장소 main의 변경 이력은 아직 출시되지 않은 항목으로 Glass가 안정화되어
`@ExperimentalHazeApi`가 필요 없어진다고 적는다.
같은 항목에 `Modifier.hazeGlassContainer`가 추가된다고 한다.
인접한 Glass 요소를 하나의 묶음으로 합치는 기능이다.
이 문서는 이 항목이 들어간 정식 버전이 나왔는지 확인하지 못했다.

### 눌림과 접근성 설정

Glass의 눌림, 호버, 포커스 반응은 기본으로 꺼져 있고 옵트인이다.
시각 반응만 더할 뿐 클릭 처리나 포커스, 시맨틱스는 추가하지 않는다.
`GlassReducedMotionPolicy`의 `System`을 고르면 시스템 애니메이션 배율을 따른다.

접근성 설정은 `LocalGlassAccessibilitySettings`로 받는다.
Haze가 플랫폼 접근성 서비스를 직접 읽지 않고 앱이 읽은 결과를 넘기는 구조다.
`reduceTransparency`는 블러 기여를 줄이고,
`increaseContrast`와 `showBorders`는 뚜렷한 가장자리를 강제한다.

## 지원 범위와 폴백

Haze는 하나의 `GlassStyle`을 모든 플랫폼에서 쓰고 구현은 자동으로 고른다.
폴백에서는 틴트, 알파, 둥근 모양, 눌림 조명과 변형이 그대로 남는다.
굴절과 블러, 색수차, `surfaceProfile`, 고급 색 보정은 폴백에서 빠진다.
문서는 굴절이나 색수차만으로 핵심 의미를 전달하지 말라고 경고한다.

오래된 Android 버전의 블러는 Chris Banes의 글에 정리되어 있다.
Android 12와 12L에서는 점진 블러에 대한 폴백이 있고,
Android 11 이하에서는 실험적인 옵트인 블러가 있다.
그 낮은 버전은 기본으로 반투명 오버레이를 쓰며,
블러를 켜면 성능 비용이 따른다.[^banes-pb]
블러가 꺼진 상태에서는 설정한 폴백 스크림을 그린다.

## 성능

성능 가이드는 `HazePerformanceMode.Default`(고정 Balanced)에서 시작하고,
릴리스에 가까운 빌드로 가장 느린 지원 기기에서 측정하라고 한다.
한 번에 한 설정만 바꾸고, Android에서는
Macrobenchmark로 프레임 초과와 CPU 프레임 시간을 함께 본다.
프레임이 느릴 때는 면적 줄이기, 효과 줄이기, 낮은 품질,
스타일 단순화, 캡처 소스 밖으로 애니메이션 빼기 순으로 시도한다.

가이드가 공개한 수치는 Pixel 8a 60Hz 측정이다.
배경이 바뀌는 조건에서
Glass의 Balanced는 90번째 백분위에 프레임 마감까지 약 8.1ms가 남았고,
Quality는 7.0ms였다.
플랫폼 backdrop 경로는 소스 경로보다 CPU
프레임 시간(90번째 백분위)이 23~46% 길었다.
이 수치는 한 기기의 참고값이다.

## 함정

- 카메라 미리보기를 흐리려면 CameraX에서
`PreviewView.ImplementationMode.COMPATIBLE`을
써야 한다. `SurfaceView`는 캡처할 수 없다.
- 소스가 사라져도 마지막 프레임을 계속 그리는 것이 기본(`KeepLastFrame`)이다.
개인정보가 있는 콘텐츠는 `ClearWhenUnavailable`로 끈다.
- 애니메이션이 `hazeSource` 안에 있으면
매 프레임 다시 캡처한다. 애니메이션이 효과에 필요 없다면 소스 밖으로 뺀다.
- `shape`는 효과의 경계이고, 자식 콘텐츠까지 잘라야 하면
같은 모양의 `Modifier.clip()`을 바깥에 따로 붙인다.

## 트레이드오프

### 하나의 스타일로 모든 플랫폼을 덮는 대신 폴백에서 모습이 달라진다

폴백 표를 보면 굴절이 빠진 화면과 굴절이 있는 화면이 같은 앱에서 공존한다.
디자인이 굴절에 의존하면 낮은 버전에서 의미가 사라진다.
틴트와 가장자리만으로도 읽히는 디자인이 이 라이브러리와 잘 맞는다.

### 네이티브 backdrop은 빠른 길이 아니다

플랫폼의 뒤 화면 효과를 쓰는 경로는 Haze의 측정에서
소스 경로보다 CPU 프레임 시간이 길었다.
성능 가이드는 네이티브 렌더링이 소스 캡처를 단순하게 할 수는 있지만
Glass 측정에서 CPU 성능 이득은 보이지 않았다고 정리한다.

### 효과가 하나가 아니라 수명이 긴 구조다

Haze는 소스 캡처, 레이어 경계, 보존 정책, 스타일 계층을 갖는다.
블러 한 번이 필요한 화면에는 개념이 많다. 반대로 여러 요소와
스크롤하는 소스가 섞인 화면에서는 이 구조가 비용을 줄인다.

## 체크리스트

- 모든 Haze 아티팩트의 버전을 같게 맞췄는가.
- 글이 많은 요소에 `regular`를, 미디어 위에만 `clear`를 쓰는가.
- 밝은 배경 위 `clear`에 어두운 층을 직접 넣었는가.
- 폴백(굴절 없음)에서도 의미가 전달되는가.
- 접근성 설정을 `LocalGlassAccessibilitySettings`로 연결했는가.
- 개인정보 콘텐츠에 `ClearWhenUnavailable`을 설정했는가.
- 느린 기기에서 릴리스 빌드로 스크롤과 전환을 측정했는가.

## 기억할 원칙

### 효과는 폴백에서도 읽혀야 한다

Haze 문서가 반복하는 한 가지는 굴절이 빠져도 화면이 성립해야 한다는 것이다.
굴절과 색수차는 장식이고 의미는 틴트, 대비, 가장자리가 전한다.

---

[^banes-pb]: Chris Banes, [Compose has progressive blur. Do you still need Haze?](https://chrisbanes.me/posts/compose-progressive-blur/), 2026-09-13

[^haze2]: Chris Banes, [Haze 2.0](https://chrisbanes.me/posts/haze-2.0.0/), 2026-09-22
