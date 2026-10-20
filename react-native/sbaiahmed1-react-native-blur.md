# @sbaiahmed1/react-native-blur: iOS와 Android에서 같은 API로 블러와 Liquid Glass를 쓰는 React Native 라이브러리

<https://sbaiahmed1.github.io/react-native-blur/docs>

<https://github.com/sbaiahmed1/react-native-blur>

## 소개

`@sbaiahmed1/react-native-blur`는 블러, 바이브런시,
iOS 26의 Liquid Glass 효과를 iOS와 Android와 Web에서
쓰게 해 주는 React Native 라이브러리다.
컴포넌트는 `BlurView`, `ProgressiveBlurView`, `VibrancyView`, `LiquidGlassView`,
`LiquidGlassContainer`,
`BlurSwitch` 여섯 개이고 Fabric(New Architecture) 전용이다.
이 문서를 쓴 2026년 10월 20일 기준 최신 버전은 6.0.2(2026년 9월 20일)이고,
라이선스는 MIT, GitHub 별은 약 350개이며 저장소는 2025년 6월에 만들어졌다.

이 라이브러리가 Android 사용자에게 의미 있는 이유는 6.0부터
`LiquidGlassView`가 Android 13 이상에서 실제 굴절 효과를 낸다는 점이다.
이전에는 색을 입힌 블러로 근사했고,
6.0에서
AGSL `RuntimeShader`로 굴절과 분산과 블러와 틴트를 처리하는 방식으로 바뀌었다.
콜스택의 `@callstack/liquid-glass`나 `expo-glass-effect`가
iOS에서만 유리 효과를 내는 것과 대비된다.

## 요구 사항

| 항목         | 최소 조건                                                         |
| ------------ | ----------------------------------------------------------------- |
| React Native | 0.80 이상, New Architecture 필수                                  |
| Android      | API 24 이상, Android Gradle Plugin 8.9.1 이상. 굴절은 API 33 이상 |
| iOS          | 13 이상(Xcode 16). 유리 효과는 iOS 26 이상, Xcode 26              |
| Web          | react-native-web. 블러에는 `backdrop-filter` 지원이 필요          |

Android는 별도 설정이 필요 없다.
블러는 JitPack에서 받는 QmBlurView(v1.3.0)를 자동으로 가져오고,
유리 효과는 AndroidLiquidGlassView의 AGSL 셰이더를
라이브러리에 포함해 의존성을 더하지 않는다.
Expo Go에서는 쓸 수 없다. 네이티브 코드를 포함하므로
개발 빌드가 필요하다는 것이 일반 규칙이고,
이 문서가 읽은 문서 중에는 Expo Go를 직접 언급한 곳이 없다.

## 사용하기

가장 짧은 사용은 `BlurView` 한 줄이다.

```tsx
import { BlurView } from '@sbaiahmed1/react-native-blur';

<BlurView blurType="light" blurAmount={20} style={{ flex: 1 }}>
  <Text>Content on top of blur</Text>
</BlurView>;
```

Liquid Glass는 `LiquidGlassView`로 쓴다.

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

### LiquidGlassView의 props

| prop                               | 기본값          | 플랫폼               | 의미                                                                  |
| ---------------------------------- | --------------- | -------------------- | --------------------------------------------------------------------- |
| `glassType`                        | `'clear'`       | iOS 26+, Android 13+ | `'clear'` 또는 `'regular'`                                            |
| `glassTintColor`                   | `'transparent'` | iOS 26+, Android 13+ | 유리 틴트. `#RGB`, `#RGBA`, `#RRGGBB`, `#RRGGBBAA`와 색 이름을 받는다 |
| `glassOpacity`                     | `1.0`           | iOS 26+, Android 13+ | 0에서 1. 폴백 경로의 오버레이 틴트도 이 값에 비례한다                 |
| `isInteractive`                    | `true`          | iOS 26+, Android 13+ | iOS는 터치 반응. Android는 누르면 줄어드는 애니메이션만 켜고 끈다     |
| `ignoreSafeArea`                   | `true`          | iOS                  | 안전 영역을 무시한다                                                  |
| `reducedTransparencyFallbackColor` | `'#FFFFFF'`     | iOS                  | 투명도 감소 설정일 때와 iOS 26 미만일 때 보이는 색                    |

## 동작 방식

### 폴백 사다리

| 환경                              | 렌더링                                                                                                   |
| --------------------------------- | -------------------------------------------------------------------------------------------------------- |
| iOS 26 이상                       | 네이티브 `UIGlassEffect`                                                                                 |
| Android 13 이상                   | AndroidLiquidGlassView의 AGSL `RuntimeShader`(굴절, 분산, 블러, 틴트)                                    |
| iOS 26 미만, Android 13 미만, Web | `BlurView`(`blurType="regular"`, `blurAmount={70}`)와 `glassTintColor`, `glassOpacity`로 계산한 오버레이 |

폴백의 오버레이 틴트는 알파가 35%로 제한된다. 문서는
이를 일반 블러가 아니라 유리 느낌에 맞춰 만든 근사라고 표현한다.

### Android에서 backdrop을 얻는 방법

이 부분이 Android에서 이 라이브러리를 쓸 때 가장 중요한 설명이다.
원본 라이브러리(AndroidLiquidGlassView)는 backdrop을 `RenderNode` 참조로
연결하는데, 이 방식은 React Native의 뷰 계층 안에서 순환하는 렌더 트리를 만든다.
그래서 이 라이브러리는 셰이더만 가져다 쓰고,
backdrop은 가장 가까운 화면(screen)에서 소프트웨어로 캡처한 뒤 축소해서 쓴다.
같은 캡처 루트를 쓰는 유리 뷰들은 이 비트맵을 공유한다.

캡처 주기는 다음과 같다.

- 정지해 있으면 캡처를 최대 100ms 재사용한다.
- 움직임이 있으면 33ms 간격으로 새 캡처를 요청한다.
- 각 뷰의 위치는 렌더된 프레임마다 추적한다.
- 유리 하위 트리는 캡처에서 제외한다.

`BlurView`도 같은 원리다. QmBlurView가 가장 가까운 `react-native-screens`의
Screen(없으면 React 루트)의 뷰 트리를 축소한 비트맵으로 캡처해 흐린다.
그래서 캡처와 블러 모두 비용이 있고, `blurRounds`(기본 5,
범위 1에서 15)를 낮추면 품질 대신 블러 작업이 줄어든다.

## 문서가 경고하는 함정

### 캡처 루트 안에 그려진 위쪽 콘텐츠도 같이 캡처된다

iOS는 효과 뷰 뒤에 있는 것만 샘플링하지만,
Android 캡처는 캡처 루트 안에서 블러 위에 그려진 모든 것을 포함한다.
그래서 선명한 원본 아래에 흐린 후광이 생길 수 있다.
디자인에 후광이 보이면 그 콘텐츠를 캡처 루트 밖으로 옮기라고
문서는 안내한다. 예로 네비게이터 위의 포털을 든다.

### 유리 요소마다 셰이더 비용이 든다

같은 캡처 루트를 쓰는 유리 뷰는 비트맵과 캡처 작업을 나눠 쓰지만,
각 유리 요소의 셰이더와 렌더링 비용은 따로 든다.
다른 루트는 캡처도 따로 해야 한다.
문서의 조언은 긴 목록에 수십 개를 넣지 말고
잘 고른 몇 개만 두며 목표 기기에서 프로파일링하라는 것이다.

### 모서리 반지름

유리 렌즈의 형태(경사와 굴절)는 균일한 `borderRadius`를 따른다.
한 모서리만 지정한 반지름은 클리핑은 맞게 되지만 렌즈 형태에는 반영되지 않는다.

### Android 색 문자열의 의미가 바뀌었다

예전 Android는 8자리 색 문자열을 `#AARRGGBB`로 읽었고 축약형(`#RGB`)을 거부했다.
이제는 React Native 방식(`#RRGGBBAA`)을 따른다.
Android 전용 ARGB 문자열로 우회했다면
알파 바이트를 뒤로 옮겨야 한다. 예로 `#80FF0000`은 `#FF000080`이 된다.

### 접근성 설정은 iOS만 처리한다

`reducedTransparencyFallbackColor`와 `ignoreSafeArea`는 iOS 전용이고
Android에서는 아무 일도 하지 않는다.
투명도 감소 설정에서 유리를 숨기고
단색으로 바꾸는 동작은 iOS 26 이상 설명에만 나온다.
Android에서 접근성 대응이 필요하면
앱이 직접 해야 한다. 이는 문서에 Android 접근성 설정 연동이
적혀 있지 않다는 사실을 바탕으로 한 이 문서의 해석이다.

## 트레이드오프

### 같은 API를 주는 대신 Android는 에뮬레이션이다

iOS에서는 OS가 만드는 유리를 그대로 쓰지만,
Android에서는 캡처와 셰이더로 흉내 낸다.
그래서 같은 코드가 두 플랫폼에서 같은 비용을 내지 않는다.
Android에서는 스크롤 중인 콘텐츠 위의 유리가 33ms 간격의 캡처에 의존하므로,
빠르게 움직이는 배경에서는
iOS보다 뒤처질 수 있다. 이 마지막 문장은 캡처 주기에서
이 문서가 끌어낸 추론이다.

### New Architecture 전용이다

v5부터 Paper(레거시 아키텍처)를 지원하지 않는다.
앱이 아직 구 아키텍처에 있다면 이 라이브러리를 쓸 수 없다.
`peerDependencies`는 React Native 0.80 이상과 React 18.2 이상을 요구한다.

### 컨테이너 병합은 iOS만 된다

`LiquidGlassContainer`의 병합 효과는 iOS 26 이상에서만 동작한다.
Android 13 이상에서는
각 자식 `LiquidGlassView`가 개별로 유리를 그리지만 서로 합쳐지지 않는다.

## 체크리스트

- React Native 0.80 이상, New Architecture, AGP 8.9.1 이상인가.
- Android 12 이하와 iOS 26 미만의 폴백 화면을 눈으로 확인했는가.
- 유리 요소를 화면당 몇 개로 제한했고 같은 캡처 루트를 쓰는가.
- 블러 위에 그려지는 콘텐츠가 후광으로 캡처되지 않는가.
- 균일한 `borderRadius`를 쓰는가.
- Android에서 접근성(투명도, 대비) 대응을 앱이 직접 하는가.
- 낮은 사양 기기에서 스크롤 중 프레임을 측정했는가.

## 기억할 원칙

### 같은 컴포넌트가 플랫폼마다 다른 일을 한다

이 라이브러리는 한 줄의 JSX로 iOS의 시스템
유리와 Android의 셰이더 에뮬레이션을 모두 낸다.
편리한 만큼,
비용과 접근성 같은 문제가 플랫폼마다 달라진다는 점을 코드 밖에서 챙겨야 한다.
