# 안드로이드에서 Liquid Glass 스타일 UI를 제대로 쓰는 법

## 한눈에 보기

먼저 결론을 적는다.
안드로이드에는 시스템이 주는 Liquid Glass가 없어서,
앱이 뒤 화면을 캡처해 블러와 굴절을 직접 입혀야 한다.
이때 가장 중요한 결정은 라이브러리가 아니라 세 가지다. 어디에 쓸 것인가,
어느 API 수준부터 어떤 효과를 줄 것인가, 효과가 빠져도 화면이 읽히는가.
이 결론은 하나의 출처가 말한 것이 아니라,
아래 자료를 겹쳐 읽고 이 문서가 정리한 것이다.

| 결정                    | 기준                                                                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 어디에 쓰나             | 콘텐츠 위에 떠 있는 컨트롤과 내비게이션에만 쓴다. 본문 영역에는 쓰지 않는다                                               |
| 어느 효과를 어느 버전에 | 블러는 API 31, 굴절은 API 33 이상이다. 그 아래는 tint와 테두리로 대체한다                                                 |
| 글이 많은 요소는        | 투명도가 낮은 쪽(regular)을 쓰고 글자 대비를 실제 콘텐츠 위에서 측정한다                                                  |
| 사용자 설정             | 대비, 모션, 블러 비활성 상태를 앱이 읽어 효과를 줄인다                                                                    |
| 구현                    | 직접 조립하거나 라이브러리를 쓴다. 안드로이드 라이브러리 세 개와 React Native 라이브러리 여섯 개는 별도 문서에서 분석했다 |

React Native에서 쓰는 방법은 “React Native에서 쓰기” 절에 따로 모았다.
이 문서의 코드는 각 출처가 보여 준 예시이고,
이 문서가 실기기에서 실행한 것은 없다.

## 먼저 정할 것: 어디에 쓰고 어디에 쓰지 않는가

Apple의 Materials 가이드는 Liquid Glass를 콘텐츠 위에 떠서
컨트롤과 내비게이션을 맡는 기능 레이어로 정의한다.[^hig]
콘텐츠 레이어에는 쓰지 말라고 하고,
예외로 슬라이더와 토글처럼 사용자가 건드리는
순간에만 유리 모양을 띠는 컨트롤을 든다.[^hig]
맞춤 컨트롤에 효과를 입히더라도 가장 중요한 기능 요소로 한정하고
여러 컨트롤에 쓰지 말라고 한다.[^hig]
Apple의 Adopting Liquid Glass 문서도 같은 방향이다. 컨트롤과
내비게이션의 맞춤 배경을 줄이고, 효과를 남용하지 말라고 한다.[^adopt]

이것은 Apple 플랫폼의 가이드이고 안드로이드가 따라야 할 규정은 아니다.
다만 안드로이드에서 이 스타일을 가져온다면
같은 이유가 그대로 적용된다고 이 문서는 본다.
뒤가 비치는 요소가 화면 곳곳에 있으면
어느 것이 컨트롤인지 구분되지 않고, 블러 비용도 늘어난다.

적용 대상을 고르는 간단한 기준은 이렇다.

| 대상                          | 판단                                                  |
| ----------------------------- | ----------------------------------------------------- |
| 하단 내비게이션, 떠 있는 툴바 | 적합. 콘텐츠가 뒤로 스크롤되며 비친다                 |
| 바텀 시트, 팝오버             | 적합. 글이 많으면 regular 쪽으로                      |
| 슬라이더의 thumb, 토글        | 누르는 순간에만 유리 모양을 쓰는 것이 Apple의 예외다  |
| 카드 목록, 본문 배경          | 부적합. 콘텐츠 레이어이므로 불투명한 표준 배경을 쓴다 |
| 한 화면에 여러 개의 유리 버튼 | 줄인다. 가장 중요한 하나나 둘로 한정한다              |

### regular와 clear를 가른다

Apple의 가이드는 변형을 둘로 나눈다.
regular는 뒤 콘텐츠를 흐리고 밝기를 조정해 글자가 읽히게 하며,
알림창이나 사이드바처럼 글이 많은 요소에 쓴다.[^hig]
clear는 투명도가 높아 사진이나 영상 위 컨트롤처럼
뒤 콘텐츠가 그대로 보여야 할 때 쓴다.[^hig]
clear를 밝은 콘텐츠 위에 쓰면
35% 불투명도의 어두운 층을 깔아 대비를 확보하라고 권한다.[^hig]

안드로이드 라이브러리 중에는 이 구분을 그대로 가져온 것이 있다.
Haze는 `GlassStyle.regular`와 `GlassStyle.clear`를 두고,
어두운 층은 자동으로 넣지 않는다.[^haze-glass]

## 안드로이드가 줄 수 있는 것

### API 수준별로 되는 일

| 기능                                                  | 최소 API                            | 출처 요약                                              |
| ----------------------------------------------------- | ----------------------------------- | ------------------------------------------------------ |
| `RenderEffect`(블러 포함)                             | 31                                  | `RenderEffect` 참조 문서의 Added in API level 31[^re]  |
| `RuntimeShader`(AGSL, 굴절의 재료)                    | 33                                  | `RuntimeShader` 참조 문서의 Added in API level 33[^rs] |
| window blur(`Window#setBackgroundBlurRadius`)         | 31(기기와 상태에 따라 꺼질 수 있음) | `Window` 참조와 AOSP 문서[^win][^aosp]                 |
| Compose의 `rememberGraphicsLayer`(뒤 화면 캡처 재료)  | Compose 1.7.0-alpha07 이상          | Compose 그래픽 modifier 문서[^dm]                      |
| `RenderNode.setBackdropRenderEffect`(플랫폼 backdrop) | Android 17 QPR 2(SDK 37.2)          | Chris Banes의 글[^banes]                               |

굴절 같은 효과는 `RuntimeShader`가 필요해서 API 33 이상에서만 된다.
그 아래 버전에서는 폴백을 따로 줘야 한다고
Compose Internals의 AGSL 튜토리얼도 말한다.[^ci]

### 같은 창의 blur와 window blur는 다르다

`RenderEffect`의 블러는 같은 창 안의 내용을 흐린다.
Android 12부터 있는 window blur는 창 뒤의 화면을 흐린다. 다른 앱이 뒤에 있어도
동작한다.[^aosp]
그래서 window blur는 다이얼로그와 바텀 시트처럼 떠 있는 창에 맞는다고
문서가 설명한다.[^aosp]
화면 안의 카드나 하단 바 뒤를 흐리는 용도는 아니라고 이 문서는 읽는다.
window blur는 비싼 연산이라 일부 기기에서만 지원되고,
배터리 절약 모드 같은 상태에서는 시스템이 끌 수 있다.[^aosp]

### Compose가 주는 blur는 자기 내용만 흐린다

Compose의 새 progressive blur는 컴포저블 자신의 내용을 흐리고
뒤에 있는 내용은 흐리지 않는다.[^banes]
그래서 툴바에 붙여도 뒤로 스크롤되는 목록이 비쳐 흐려지지 않는다.[^banes]
뒤 화면 blur를 만들려면 뒤에 있는 콘텐츠를 따로 캡처해서
효과의 입력으로 넘겨야 한다.[^banes]

플랫폼에는 뒤쪽에 효과를 적용하는
`RenderNode.setBackdropRenderEffect`가 Android 17 QPR 2에 들어왔다.[^banes]
이 API는 해당 버전 이상에서만 동작하므로,
의존성을 올려도 낮은 버전에는 생기지 않는다.[^banes]

## 뒤 화면 효과가 만들어지는 원리

대부분의 구현이 같은 순서를 따른다. 뒤 화면을 레이어에 기록하고,
그 레이어를 앞쪽 요소 자리에 다시 그리면서 효과를 입힌다.
Compose 공식 문서는 `rememberGraphicsLayer()`로 레이어를 만들고,
`drawWithContent` 안에서
`graphicsLayer.record { drawContent() }`로 그리기 명령을 레이어로
보낸 뒤 `drawLayer`로 보이는 캔버스에 그리는 방법을 보여 준다.[^dm]
공식 예제의 목적은 컴포저블을 비트맵으로 복사하는 것이지만,
같은 기록과 재생 구조가 뒤 화면 캡처의 재료가 된다고 이 문서는 읽는다.

효과를 쌓는 순서도 중요하다.
Kyant의 Backdrop 문서는 색 필터, 블러,
렌즈 순서로 적용해야 한다고 명시한다.[^kyant-effects]
이 순서가 바뀌면
굴절이 이미 흐려진 픽셀을 다시 굴절시키는 식으로
결과가 달라진다. 이 설명은 이 문서의 추론이다.

`graphicsLayer`에 `RenderEffect`를 설정하면
내용이 항상 오프스크린 버퍼로 그려진다고 Compose 문서는 밝힌다.[^dm]
즉 유리 요소 하나마다 오프스크린 렌더링 비용이 들어간다는 뜻이고,
이것이 성능 절에서 면적과 개수를 줄이라는 조언의 바탕이다.

## 읽히게 만들기

### 글자 대비는 실제 콘텐츠 위에서 잰다

WCAG 1.4.3은 일반 글자에 4.5:1, 큰 글자에 3:1 이상의 대비를 요구한다.[^wcag]
유리 요소 뒤의 콘텐츠는 스크롤할 때마다 바뀌므로,
정지 화면 하나에서 대비를 재면 부족하다.
밝은 사진, 어두운 사진,
채도 높은 이미지처럼 최악의 배경을 골라 확인해야 한다고 이 문서는 본다.

Kyant의 튜토리얼은 유리 위에 반투명 흰색 면을 얹어 가독성을 올리고,
아름다움과 가독성 사이의 균형을 잡아야 한다고 적는다.[^kyant-bar]
Apple은 두꺼운 효과가 더 불투명해 가는 글자의 대비가 좋고,
얇은 효과는 뒤 맥락을 보여 준다고 구분한다.[^hig]
글이 많을수록 불투명한 쪽으로 가는 것이 기본 방향이다.

### 사용자 설정을 읽는다

Apple은 사용자가 투명도 감소나 모션 감소를 켜면 효과가 바뀐다고 하며,
맞춤 요소도 그런 설정으로 시험하라고 한다.[^adopt]
안드로이드에서 읽을 수 있는 신호는 다음과 같다.

| 신호                  | API                                                        | 비고                                                                   |
| --------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------- |
| 색 대비 수준          | `UiModeManager#getContrast()`(API 34)                      | -1(최소)에서 1(최대) 사이의 값. 자체 렌더링을 하는 앱이 조회한다[^uim] |
| 고대비 텍스트         | `AccessibilityManager#isHighContrastTextEnabled()`(API 36) | 플랫폼 렌더링 파이프라인에 의존하지 않는 앱이 조회한다[^am]            |
| window blur 활성 여부 | `WindowManager#isCrossWindowBlurEnabled()`와 리스너        | 리스너로 상태 변화를 받는다[^aosp]                                     |
| 애니메이션 배율       | animator duration scale                                    | Cloudy는 배율 0을 Reduce Motion으로 보고 광원을 멈춘다[^cloudy]        |

이 API들이 투명도 감소 같은 Apple의 설정과 같은 의미인지는 문서에 없다.
이 문서는 신호를 읽어 “블러를 줄이고, 면을 더 불투명하게 하고,
테두리를 뚜렷하게” 하는 식으로 앱이 해석해야 한다고
본다. 이 해석은 이 문서의 판단이다.

window blur에는 공식 지침이 있다.
블러가 꺼졌을 때 창 배경 drawable의 알파를 올려 더 불투명하게 하고,
blur behind에는 더 짙은 dim을 넣으라는 것이다.[^aosp]
같은 원칙을 화면
안의 유리 요소에도 적용할 수 있다. 효과가 사라져도
뒤 콘텐츠와 겹쳐 읽기 어려워지지 않게 한다.

## 낮은 버전 설계

버전마다 같은 디자인을 유지하려 하면 안 된다.
효과를 세 단계로 나누고, 빠지는 순서를 미리 정해 둔다.

| 단계        | 가능한 것                                    | 빠지는 것                       |
| ----------- | -------------------------------------------- | ------------------------------- |
| API 33 이상 | 블러, 굴절, 색수차, progressive blur(셰이더) | 없음                            |
| API 31~32   | 블러(`RenderEffect`), tint, 테두리           | 굴절과 색수차, 셰이더 기반 효과 |
| API 30 이하 | tint와 반투명 면, 테두리                     | 블러 대부분                     |

이 표의 단계는 Cloudy가 README에 정리한 버전별 동작과 같은 모양이다.[^cloudy]
Haze도 같은 취지로, 폴백에서는 틴트와 알파와 모양은 남기고
굴절과 블러와 색수차는 뺀다.[^haze-glass]
Haze 문서는 굴절이나 색수차만으로 핵심 의미를 전달하지 말라고
경고한다.[^haze-glass]

원칙은 이렇다. 굴절은 장식이고 의미는 tint, 대비, 테두리가 전한다.
굴절이 빠진 화면을 먼저 설계하고,
굴절은 그 위에 더하는 것으로 생각하면 낮은 버전에서 깨지지 않는다.

## 성능

효과 하나가 오프스크린 렌더링과 블러 비용을 만든다.
window blur 문서는 반경이 클수록 GPU가 더 넓은 영역을 샘플링해 비싸지고,
150px을 넘기지 말라고 한다.[^aosp]
Compose Internals의 굴절 셰이더 예제는 9×9(81번) 샘플링 블러 커널을 쓰고,
5×5(25번)로 줄이면 빨라진다고 안내한다.[^ci]

Haze의 성능 가이드는 측정 방법을 구체적으로 준다.[^haze-guide]
완성된 화면을 만든 뒤 릴리스에 가까운 빌드로 가장 느린 지원 기기에서 측정하고,
한 번에 한 설정만 바꾼다.
Macrobenchmark로 프레임 초과(frame overrun)와 CPU 프레임 시간을 함께
본다. CPU 프레임 시간은 GPU 셰이더 시간을 직접 재지 않는다는 점도 밝힌다.

프레임이 느릴 때의 순서는 다음과 같다.

1. 효과가 덮는 면적을 줄인다.
2. 효과가 필요 없는 곳에서
뺀다. 여러 개의 독립된 요소 대신 하나를 공유하는 안도 비교한다.
3. 낮은 품질 설정을 시험한다.
4. progressive blur를 균일 블러로 바꾸고 색수차 같은 기능을 줄인다.
5. 캡처하는 원본 안의 애니메이션을 밖으로 뺀다.

Haze의 Pixel 8a 측정에서
플랫폼 backdrop을 쓰는 경로는 소스 캡처 경로보다 CPU
프레임 시간(90번째 백분위)이 23~46% 길었다.[^haze-guide]
새 플랫폼 API가 자동으로 빠르지는 않다는 사례이고, 한 기기의 참고값이다.

## 구현을 고르는 방법

직접 구현은 위의 원리를 그대로 코드로 옮기는 일이다.
뒤 화면 캡처, 효과 순서, 순환 방지, 폴백을 모두 앱이 책임진다.
라이브러리는 이 가운데 캡처와 효과 순서를 맡아 준다. 아래 표는
이 문서가 별도로 분석한 세 라이브러리의 핵심만 줄인 것이다.

| 라이브러리     | 이런 경우에                                            | 상세 분석                  |
| -------------- | ------------------------------------------------------ | -------------------------- |
| Kyant Backdrop | 컴포넌트를 직접 조립하고 효과 순서를 통제하고 싶다     | `mobile/kyant-backdrop.md` |
| Haze           | 스타일을 재사용하고 폴백과 접근성 연결 자리가 필요하다 | `mobile/haze.md`           |
| Cloudy         | 버전별 블러 동작이 정리된 가벼운 블러가 필요하다       | `mobile/cloudy.md`         |

이 표는 이 문서의 판단이다.
세 라이브러리는 모두 젊은 프로젝트이므로 릴리스 상태를 확인하고,
유리 요소 정의를 한 파일에 모아 두어 교체에 대비한다.

## React Native에서 쓰기

### 먼저 알아 둘 것: React Native의 뒤 화면은 Compose가 아니다

위에서
설명한 `graphicsLayer` 기록 방식은 Compose 트리 안의 콘텐츠를 캡처하는 방법이다.
React Native 앱의 뒤 화면은 네이티브 View 계층이므로
React Native용 라이브러리들은 View 계층을 캡처한다.
`@sbaiahmed1/react-native-blur`는 가장 가까운 `react-native-screens`의
Screen(없으면 React 루트)의 뷰 트리를 축소한 비트맵으로 캡처한다.[^sb-install]
`react-native-blur-overlay`는 `snapshot` 모드에서 화면을 비트맵으로 한 번 찍고,
`live` 모드에서는
`<BlurTarget>` 하위 트리를 `RenderNode`에 다시 기록한다.[^overlay]
`react-native-liquid-glassmorphism`은 유리 뒤의 뷰
계층을 프레임마다 축소한 비트맵으로 캡처한다.[^lgm]

React Native 자체 기능으로는 `filter: blur()`가 있다.
이 기능은 New Architecture에서만 쓸 수 있고
blur는 Android 12 이상에서만 동작한다.[^rn-style]
그러나 `filter`는 뷰 자신과 자손에 적용되고 `overflow: hidden`을 함의한다고
문서가 설명하므로, 뒤 화면을 흐리는 유리 배경에는 쓸 수 없다.[^rn-style]
iOS에서는 `brightness`와 `opacity` 두 함수만 쓸 수 있다.[^rn-style]

### Android에서는 유리가 없는 라이브러리가 많다

`@callstack/liquid-glass`는 iOS 26의 유리 효과를 React Native의 iOS 앱에서
쓰게 해 주는 라이브러리이고, iOS 26 미만에서는
효과 없는 일반 `View`를 그린다.[^callstack]
`expo-glass-effect`의 `GlassView`는 iOS 26 이상에서만 동작하고
지원하지 않는 플랫폼에서는 일반 `View`로 폴백한다.[^expo-glass]
두 라이브러리를 Android에서 쓰면 유리 대신 일반 뷰가 나오므로,
Android 대응이 필요하면 `isLiquidGlassSupported`로 분기하고
폴백 스타일을 직접 줘야 한다.[^callstack]
이 두 라이브러리는 이 저장소의 `react-native/callstack-liquid-glass.md`와
`react-native/expo-glass-effect.md`에 따로 정리되어 있다.

### 선택지 지도

아래 표는 이 문서가 별도로 분석한 라이브러리를 한 장으로
줄인 것이다. 각 항목의 근거와 한계는 링크한 분석 문서에 있다.

| 선택지                              | 뒤 화면을 얻는 방식                                | Android 요건                                                       | 한 줄 요약                                                     | 상세 분석                                           |
| ----------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------- | --------------------------------------------------- |
| `expo-blur`                         | `BlurTargetView`로 감싼 범위를 `RenderNode`로 블러 | 블러는 API 31 이상이 효율적, 그 아래는 `RenderScript`              | Expo가 관리하는 안정된 블러. 굴절은 없다                       | `react-native/expo-blur.md`                         |
| `@sbaiahmed1/react-native-blur`     | 가장 가까운 Screen을 축소 캡처                     | 블러 API 24 이상, 굴절 API 33 이상, RN 0.80 이상, New Architecture | 같은 API로 iOS 26 유리와 Android 굴절을 낸다                   | `react-native/sbaiahmed1-react-native-blur.md`      |
| `react-native-blur-overlay`         | `snapshot`, `live`(`BlurTarget`), `glass` 세 방식  | live는 API 31 이상, glass는 API 33 이상, RN 0.80 이상              | 측정 수치와 한계가 가장 상세하다. 모달 뒤 블러 가능            | `react-native/react-native-blur-overlay.md`         |
| `react-native-liquid-glassmorphism` | 프레임마다 소프트웨어 캡처                         | 굴절 API 33 이상, RN 0.83 이상                                     | 임의 모양과 병합이 있다. 가장 어린 프로젝트                    | `react-native/react-native-liquid-glassmorphism.md` |
| React Native Skia                   | Canvas 안에서 `BackdropBlur`와 `RuntimeShader`     | API 26 이상, Vulkan, RN 0.79 이상                                  | 완전히 직접 그린다. 뒤 화면이 네이티브 뷰면 스냅샷 경로가 필요 | `react-native/react-native-skia.md`                 |
| Expo UI + 커스텀 Compose 뷰         | Compose 트리 안에서 Compose 라이브러리가 캡처      | 개발 빌드, `Host`                                                  | Haze나 Kyant를 쓸 수 있지만 연결을 직접 만들어야 한다          | `react-native/expo-ui-jetpack-compose-extending.md` |

이 표의 요건은 각 라이브러리의 README와 문서에서
읽은 것이다.[^sb-install][^overlay][^lgm][^skia-install][^expo-blur-doc]

### 상황별 선택

이 절은 위 표를 바탕으로 한 이 문서의 판단이다.

| 상황                                                             | 선택                                                             |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| 블러만 필요하고 Expo 관리형 앱이다                               | `expo-blur`. Android에서는 `BlurTargetView` 구조를 받아들인다    |
| 같은 JSX로 iOS 26 유리와 Android 굴절을 얻고 싶다                | `@sbaiahmed1/react-native-blur`. 가장 적은 코드로 시작한다       |
| 스크롤하는 콘텐츠 뒤에서 live로 흐려야 하고 낮은 버전도 지원한다 | `react-native-blur-overlay`. 단계별 폴백과 측정 수치가 있다      |
| 모달 뒤를 흐려야 한다                                            | `react-native-blur-overlay`의 모달 안 `live`(시스템 창 블러)     |
| 원이나 오목한 모양, 유리가 합쳐지는 효과가 필요하다              | `react-native-liquid-glassmorphism`. 어린 프로젝트임을 감수한다  |
| 화면 전체를 캔버스에서 직접 그린다                               | React Native Skia                                                |
| iOS 앱이고 Android는 평면 디자인으로 충분하다                    | `@callstack/liquid-glass` 또는 `expo-glass-effect`와 폴백 스타일 |

### 레시피

#### Expo에서 Android 블러 얻기

SDK 55부터 Android 블러는 안정 상태이지만 코드를 바꿔야 한다.[^expo-blur-doc]
흐려질 콘텐츠를 `BlurTargetView`로 감싸고
`BlurView`에 `blurTarget`과 `blurMethod`를 준다.[^expo-blur-doc]

```tsx
import { BlurView, BlurTargetView } from 'expo-blur';
import { useRef } from 'react';
import { Text, StyleSheet, View } from 'react-native';

export default function App() {
  const targetRef = useRef<View | null>(null);

  return (
    <View style={styles.container}>
      <BlurTargetView ref={targetRef} style={styles.background}>
        {/* 흐려질 콘텐츠 */}
      </BlurTargetView>
      <BlurView
        blurTarget={targetRef}
        intensity={100}
        style={styles.blurContainer}
        blurMethod="dimezisBlurView">
        <Text>Hello, my container is blurring contents underneath!</Text>
      </BlurView>
    </View>
  );
}
```

`blurMethod`의 기본값은 `'none'`이라 반투명 뷰만 나온다.[^expo-blur-doc]
Android 11 이하의 느린 블러를 피하려면
`dimezisBlurViewSdk31Plus`를 쓴다.[^expo-blur-doc]

#### 한 컴포넌트로 iOS 26 유리와 Android 굴절 얻기

`@sbaiahmed1/react-native-blur`의 `LiquidGlassView`는 iOS 26 이상에서
`UIGlassEffect`를, Android 13 이상에서 AGSL 셰이더를 쓰고,
그보다 낮은 환경에서는 `BlurView` 기반 폴백으로 내려간다.[^sb-glass]

```tsx
import { LiquidGlassView } from '@sbaiahmed1/react-native-blur';

<LiquidGlassView
  glassType="regular"
  glassTintColor="#007AFF"
  glassOpacity={0.8}
  style={{ padding: 20, borderRadius: 20 }}
>
  <Text>Beautiful liquid glass effect</Text>
</LiquidGlassView>
```

문서는 목록에 수십 개를 넣지 말고 잘 고른 몇 개만 두라고 경고한다.[^sb-glass]
`borderRadius`는 균일한 값이어야 렌즈 형태에 반영된다.[^sb-glass]

#### 스크롤하는 콘텐츠 위의 유리 탭 바

`react-native-blur-overlay`에서는 뒤에 보일 콘텐츠를 `<BlurTarget>`으로 감싸고
오버레이를 그 형제로 둔다.[^overlay]
오버레이가 자기가 속한 하위 트리를 흐릴 수는 없기 때문이다.[^overlay]

```tsx
<BlurTarget style={{ flex: 1 }}>
  <FlatList /* ...your content... */ />
</BlurTarget>

<BlurOverlay
  visible
  blurMode="glass"
  glassVariant="regular"   // or "clear"
  interactive              // responds to touch
  style={{
    position: 'absolute', left: 24, right: 24, bottom: 32, height: 64,
    borderRadius: 32,
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: 'rgba(255,255,255,0.22)',
  }}
>
  {/* your tabs */}
</BlurOverlay>
```

`blurMode="glass"`는 API 33 미만에서 `live`로,
그 아래에서 `snapshot`으로 내려가며
이유를 `BlurOverlay` 태그로 logcat에 한 번 남긴다.[^overlay]

#### 버전 분기

Android에서 `Platform.Version`은 숫자를 돌려준다고 문서가 적는다.[^rn-platform]
문서는 이 숫자가 API 수준이라고 명시하지 않으므로,
Android 13(API 33) 비교에 쓰기 전에 실제 기기에서 값을 확인하는 편이 안전하다.
`react-native-liquid-glassmorphism`은 마운트 전에 `getGlassCapabilities()`와
`useGlassSupport()`로 단계(`refraction`, `blur`, `tint`,
`none`)를 알려 주므로 직접 비교할 필요가 없다.[^lgm]

### React Native에서 유독 문제가 되는 것들

- **Expo Go에서
실행되는 것은 `expo-blur`뿐이다.** `expo-blur`는
Expo Go에 포함되어 있다.[^expo-blur-doc]
  `react-native-blur-overlay`와 `react-native-liquid-glassmorphism`은
Expo Go에서 쓸 수 없다고 각 문서가 적고,
React Native Skia v3도 개발 빌드가 필요하다.[^overlay][^lgm][^skia-install]
  `@sbaiahmed1/react-native-blur`의 문서에는 Expo Go에 대한 언급이 없다.
- **React Native 버전과 New Architecture 요건이 제각각이다.**
`@sbaiahmed1/react-native-blur`는 0.80 이상과 New Architecture,
`react-native-liquid-glassmorphism`은 0.83 이상,
React Native Skia v3는 0.79 이상과 React 19를
요구한다.[^sb-install][^lgm][^skia-install]
- **캡처 루트 안의 위쪽 콘텐츠가 같이 흐려진다.**
`@sbaiahmed1/react-native-blur`의 문서는
Android 캡처가 블러 위에 그려진 콘텐츠까지 포함해 후광이 생길 수 있다고 하며,
그 콘텐츠를 캡처 루트 밖(예: 네비게이터 위의 포털)으로 옮기라고
안내한다.[^sb-blur]
- **비디오, 카메라 미리보기,
지도는 캡처되지 않는다.** `SurfaceView` 기반 콘텐츠는 비어 보인다고
`react-native-blur-overlay`가 설명하고,
`react-native-liquid-glassmorphism`도 같은 한계를 적는다.[^overlay][^lgm]
- **`<Modal>`은 별도의 Android 창이라 캡처가 닿지 않는다.**
`react-native-blur-overlay`는 모달 안에서
시스템 창 블러를 요청하는 방식으로만 이를 넘고,
오버레이가 모달 전체를 덮어야 한다.[^overlay]
- **블러 단위와 의미가 라이브러리마다 다르다.** `react-native-blur-overlay`의
`radius`는 dp가 아니라 물리 픽셀이어서 같은 값이 밀도에 따라 다르게 보이고,
dp 단위인 `blurRadius`가 따로 있다.[^overlay]
  `expo-blur`의 `intensity`는 1에서 100이고 Android에서는
`blurReductionFactor`로 나눈다.[^expo-blur-doc]
- **색 문자열의 알파 위치가 바뀐 적이 있다.** `@sbaiahmed1/react-native-blur`는
Android의 8자리 색을 예전에는 `#AARRGGBB`로 읽었고
이제는 React Native 방식의 `#RRGGBBAA`로 읽는다.[^sb-migration]
- **목록의 `BlurView`는 렌더링 순서에 민감하다.** `expo-blur`의 알려진 문제는
`FlatList` 같은 동적 콘텐츠보다 `BlurView`를 먼저 렌더링하면
블러가 갱신되지 않는다는 것이다.[^expo-blur-doc]

### 접근성

React Native는 접근성 설정을 읽는 API를 준다.
`AccessibilityInfo.isReduceMotionEnabled()`는 두 플랫폼에서
쓸 수 있다.[^rn-a11y]
`reduceMotionChanged` 이벤트는 개발자 옵션의 전환 애니메이션
배율이 꺼진 경우에도 모션 감소가 켜진 것으로 알린다.[^rn-a11y]
`isReduceTransparencyEnabled()`는 iOS 전용이고,
Android에는 `isHighTextContrastEnabled()`가 있다.[^rn-a11y]
따라서 Android에서
React Native 앱이 읽을 수 있는 가장 가까운 신호는 고대비 텍스트와 모션 감소다.

라이브러리별 접근성 지원은 다르다.

| 라이브러리                          | Android의 접근성 대응                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `@sbaiahmed1/react-native-blur`     | `reducedTransparencyFallbackColor`는 iOS 전용이고 문서에 Android 접근성 연동은 없다[^sb-glass]                                 |
| `react-native-liquid-glassmorphism` | `accessibilityMode="auto"`가 Android에서 고대비 텍스트를 대용 신호로 쓴다. 저자는 진짜 선호가 아닌 대용품이라고 인정한다[^lgm] |
| `react-native-blur-overlay`         | 눌러서 닫는 backdrop에 접근성 레이블(`backdropAccessibilityLabel`)이 있다. 투명도 설정은 다루지 않는다[^overlay]               |

앱이 직접 대응하는 가장 단순한 방법은 읽은 신호에
따라 유리 컴포넌트를 불투명한 일반 뷰로 바꾸는 것이다.
아래 코드는 이 문서가 `AccessibilityInfo`의 문서를 보고
쓴 예이고 실행해 보지 않았다.

```tsx
import { useEffect, useState } from 'react';
import { AccessibilityInfo, Platform, View } from 'react-native';

function useReducedGlass() {
  const [reduced, setReduced] = useState(false);

  useEffect(() => {
    const read = async () => {
      const [motion, contrast] = await Promise.all([
        AccessibilityInfo.isReduceMotionEnabled(),
        Platform.OS === 'android'
          ? AccessibilityInfo.isHighTextContrastEnabled()
          : AccessibilityInfo.isReduceTransparencyEnabled(),
      ]);
      setReduced(motion || contrast);
    };
    read();
    const sub = AccessibilityInfo.addEventListener('reduceMotionChanged', read);
    return () => sub.remove();
  }, []);

  return reduced;
}
```

이 훅이 `true`를 돌려주면
`<LiquidGlassView>` 대신 불투명한 배경의 `<View>`를 그린다.
모션 감소는 이벤트로 갱신되지만
이 예제는 대비 설정의 변경 이벤트를 구독하지 않으므로,
설정을 바꾼 뒤 앱으로 돌아올 때 다시 읽도록 보강해야 한다.

### 성능

`react-native-blur-overlay`의 README가 Galaxy A22(Helio G80,
Mali-G52)에서 잰 수치가 React Native 쪽에서 가장 구체적이다.[^overlay]
60Hz에서 `glass`는 프레임률을 유지했고 90번째 백분위 프레임 시간이 15~25ms,
끊기는 프레임이 최대 3.6%였다.[^overlay]
90Hz에서는 `live`와 `glass` 모두 예산 한계에 걸렸고
`glass`의 끊기는 프레임이 2~14%, `live`는 1.4~2.2%였다.[^overlay]
전체 해상도 캡처는 90Hz에서 끊김이 100%여서 반해상도를 넘기지 않는다.[^overlay]

조절 항목은 `downsampling`(live의 기본 2)과 `maxUpdateFps`(기본 30)다.[^overlay]
`react-native-liquid-glassmorphism`은 유리 뷰마다 backdrop을 따로 캡처하므로
화면에 열 개가 있으면 프레임마다 열 번 캡처한다고 적고,
화면 밖 뷰에 `paused`를 주라고 안내한다.[^lgm]
`@sbaiahmed1/react-native-blur`는 같은 캡처 루트의 유리 뷰가 비트맵을 공유하지만
각 요소의 셰이더 비용은 따로 든다고 설명한다.[^sb-glass]
세 라이브러리의 공통 조언은 유리 요소 수를 줄이고
낮은 사양 기기에서 측정하라는 것이다.

### React Native 체크리스트

- 선택한 라이브러리의 React Native 버전과
New Architecture 요건을 앱이 만족하는가.
- Expo Go가 아니라 개발 빌드로 시험하는가.
- Android 12 미만, 12~12L, 13 이상 세 구간에서 폴백을 눈으로 확인했는가.
- 뒤에 보일 콘텐츠와 유리 요소의 관계(`BlurTargetView`,
`BlurTarget`, 캡처 루트)를 구조로 정했는가.
- 유리 위에 올린 콘텐츠가 캡처되어 후광이 생기지 않는가.
- 비디오, 카메라, 지도, `<Modal>` 위에 유리를 올리고 있지 않은가.
- 블러 반경의 단위(dp인가 픽셀인가)를 확인했는가.
- 고대비 텍스트와 모션 감소를 읽어 유리를 불투명 뷰로 바꾸는가.
- 낮은 사양 기기에서 60Hz와 90Hz 양쪽으로 스크롤을 측정했는가.

## 체크리스트

- 유리 효과를 컨트롤과 내비게이션에만 쓰고 본문 레이어에는 쓰지 않는가.
- 화면당 유리 요소가 가장 중요한 하나나 둘로 한정되는가.
- 글이 많은 요소는 불투명한 쪽(regular)이고,
밝은 배경 위 clear에는 어두운 층이 있는가.
- 밝은 사진, 어두운 사진, 채도 높은 이미지 위에서 글자 대비 4.5:1을 측정했는가.
- 굴절이 없는 상태에서 화면이 완결되는가.
- API 31 미만, 31~32, 33 이상 각각에서 화면을 확인했는가.
- 대비, 모션, window blur 비활성 상태를 읽어 효과를 줄이는가.
- 릴리스에 가까운 빌드로 가장 느린 지원 기기에서 스크롤과 전환을 측정했는가.
- 유리 요소 정의를 한 파일에 모아 라이브러리 교체에 대비했는가.

---

[^hig]: Apple, [Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

[^adopt]: Apple, [Adopting Liquid Glass](https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass)

[^re]: Android Developers, [RenderEffect](https://developer.android.com/reference/android/graphics/RenderEffect)

[^rs]: Android Developers, [RuntimeShader](https://developer.android.com/reference/android/graphics/RuntimeShader)

[^win]: Android Developers, [Window](https://developer.android.com/reference/android/view/Window)

[^aosp]: Android Open Source Project, [Window blurs](https://source.android.com/docs/core/display/window-blurs)

[^dm]: Android Developers, [Graphics modifiers](https://developer.android.com/develop/ui/compose/graphics/draw/modifiers)

[^banes]: Chris Banes, [Compose has progressive blur. Do you still need Haze?](https://chrisbanes.me/posts/compose-progressive-blur/), 2026-09-13

[^ci]: Compose Internals, [AGSL Shaders in Jetpack Compose - Liquid Glass Effect | Complete Tutorial](https://composeinternals.com/agsl-shaders-jetpack-compose-liquid-glass), 2025-01-15

[^wcag]: W3C, [Understanding Success Criterion 1.4.3: Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

[^uim]: Android Developers, [UiModeManager](https://developer.android.com/reference/android/app/UiModeManager)

[^am]: Android Developers, [AccessibilityManager](https://developer.android.com/reference/android/view/accessibility/AccessibilityManager)

[^cloudy]: GitHub, [skydoves/Cloudy](https://github.com/skydoves/Cloudy)

[^haze-guide]: Haze, [Guide - Haze](https://chrisbanes.github.io/haze/latest/performance/)

[^kyant-effects]: Kyant, [Backdrop effects](https://kyant.gitbook.io/backdrop/api/backdrop-effects)

[^kyant-bar]: Kyant, [Glass Bottom Bar](https://kyant.gitbook.io/backdrop/tutorials/glass-bottom-bar)

[^haze-glass]: Haze, [Overview - Haze](https://chrisbanes.github.io/haze/latest/effects/glass/)

[^sb-install]: @sbaiahmed1/react-native-blur, [Installation · react-native-blur](https://sbaiahmed1.github.io/react-native-blur/docs/installation)

[^sb-glass]: @sbaiahmed1/react-native-blur, [LiquidGlassView · react-native-blur](https://sbaiahmed1.github.io/react-native-blur/docs/liquid-glass-view)

[^sb-blur]: @sbaiahmed1/react-native-blur, [BlurView · react-native-blur](https://sbaiahmed1.github.io/react-native-blur/docs/blur-view)

[^sb-migration]: @sbaiahmed1/react-native-blur, [Migration & breaking changes · react-native-blur](https://sbaiahmed1.github.io/react-native-blur/docs/migration)

[^overlay]: GitHub, [lvlrSajjad/react-native-blur-overlay](https://github.com/lvlrSajjad/react-native-blur-overlay)

[^lgm]: GitHub, [himanshu-lal4/react-native-liquid-glassmorphism](https://github.com/himanshu-lal4/react-native-liquid-glassmorphism)

[^skia-install]: React Native Skia, [Installation | React Native Skia](https://wcandillon.github.io/react-native-skia/docs/getting-started/installation/)

[^expo-blur-doc]: Expo, [BlurView - Expo documentation](https://docs.expo.dev/versions/latest/sdk/blur-view/)

[^expo-glass]: Expo, [GlassEffect - Expo documentation](https://docs.expo.dev/versions/latest/sdk/glass-effect/)

[^callstack]: GitHub, [callstack/liquid-glass](https://github.com/callstack/liquid-glass)

[^rn-style]: React Native, [View Style Props · React Native](https://reactnative.dev/docs/view-style-props)

[^rn-a11y]: React Native, [AccessibilityInfo · React Native](https://reactnative.dev/docs/accessibilityinfo)

[^rn-platform]: React Native, [Platform · React Native](https://reactnative.dev/docs/platform)
