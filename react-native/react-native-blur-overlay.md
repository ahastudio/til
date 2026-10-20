# react-native-blur-overlay: snapshot, live, glass 세 가지 방식으로 Android 뒤 화면 효과를 내는 라이브러리

<https://github.com/lvlrSajjad/react-native-blur-overlay>

## 소개

`react-native-blur-overlay`는 자기 뒤에 렌더링된 것을 흐리고
그 위에 원하는 콘텐츠를 얹게 해 주는 React Native 네이티브 컴포넌트다.
화면 전체를 덮거나, 둥근 패널 하나가 되거나,
iOS와 Android에서 같아 보이는 떠 있는 Liquid Glass 탭 바가 될 수 있다.
npm 패키지는 2018년에 만들어졌고
이 문서를 쓴 2026년 10월 20일 기준 최신 버전은 3.2.1(2026년 9월 28일)이다.
라이선스는 MIT이고 GitHub 별은 약 100개다.

README가 내세우는 기능은 다음과 같다.

- `blurMode="glass"` 하나로 iOS 26의 시스템
Liquid Glass와 Android 13의 굴절 렌즈를 낸다.
- Android 12 이상에서는
스크롤하는 콘텐츠가 유리 뒤에서도 계속 흐려지는 live blur가 있다.
- `<Modal>` 뒤를 흐리는 기능이 있다. README는 이것이 캡처
방식의 Android 라이브러리가 닿을 수 없는 영역이라고 설명한다.
- 서드파티 의존성이 없고, New Architecture와 구 아키텍처를 모두 지원한다.

README의 측정과 한계 설명이 구체적이라는 점이 이 라이브러리의 특징이다.

## 요구 사항

| 항목         | 조건                                                                                            |
| ------------ | ----------------------------------------------------------------------------------------------- |
| React Native | 0.80 이상(New Architecture와 구 아키텍처 모두). 더 낮은 버전은 `react-native-blur-overlay@2`    |
| iOS          | 15.1 이상                                                                                       |
| Android      | minSdk 24 이상. live blur는 API 31 이상이고, 그 아래에서는 snapshot으로 내려간다                |
| Expo         | SDK 54 이상(React Native 0.80 이상이 처음 들어간 버전). 개발 빌드나 prebuild 필요, Expo Go 불가 |

설치는 `npm install react-native-blur-overlay`이고 iOS는 `pod install`을 더한다.
autolink 되므로 `MainApplication`이나 Podfile을 고칠 필요가 없다. 2.x에서
올라오는 경우에는 수동으로 넣었던 Podfile 줄과 `MainApplication`의
`add(SajjadBlurOverlayPackage())` 호출을 지워야 한다.

## 세 가지 blurMode

Android에는 iOS의 `UIVisualEffectView`에 해당하는 시스템 뷰가 없어서
라이브러리가 직접 backdrop을 만든다.
`blurMode`에 따라 방법이 세 가지다.

| 모드                 | 하는 일                                                                                                                             | 필요한 것                                                 | 비용                                                                          |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `snapshot`(기본)     | 오버레이 뒤의 화면을 비트맵으로 한 번 그려 메인 스레드 밖에서 흐리고 그대로 유지한다. 뒤에서 움직이는 콘텐츠는 다시 흐려지지 않는다 | API 24                                                    | 프레임마다 드는 비용은 없고, 캡처 한 번과 스택 블러 한 번이 든다              |
| `live`(앱 창 안)     | `<BlurTarget>` 하위 트리를 그릴 때마다 `RenderNode`에 다시 기록하고 블러 `RenderEffect`를 걸어 RenderThread로 넘긴다                | API 31 이상과 `<BlurTarget>`                              | 그려진 프레임마다 다시 기록 한 번과 GPU 블러 한 번. 정지 화면에서는 0         |
| `glass`              | `live`에 블러 뒤의 AGSL 셰이더를 하나 더한다. 가장자리에서 backdrop이 안쪽으로 휘고 접힌다                                          | API 33 이상과 `<BlurTarget>`. API 31~32에서는 `live`로    | `live`의 비용에 프레임당 RenderThread 약 0.4ms. 반해상도 넘게 캡처하지 않는다 |
| `live`(`<Modal>` 안) | 모달 창 뒤를 시스템이 흐리도록 요청한다                                                                                             | API 31 이상, cross-window blur 활성, 모달을 덮는 오버레이 | 없음(SurfaceFlinger가 합성)                                                   |

각 모드는 불가능할 때 위 단계로 내려간다.
그래서
`blurMode="live"`를 무조건 설정해도 안전하다. API 31 미만이거나 `<BlurTarget>`가
없거나 cross-window blur가 꺼져 있으면 조용히 snapshot을 보여 주고,
이유는 `BlurOverlay` 태그로 logcat에 한 번 찍는다.

## 사용하기

### 가장 기본인 패널

```tsx
import BlurOverlay, { closeOverlay, openOverlay } from 'react-native-blur-overlay';

<Button title="Blur it" onPress={() => openOverlay()} />

<BlurOverlay
  blurStyle="dark"
  radius={14}
  downsampling={2}
  brightness={-200}
  onPress={() => closeOverlay()}
>
  <View style={styles.card}>
    <Text>Anything you render here sits on top of the blur.</Text>
  </View>
</BlurOverlay>
```

오버레이는 세 가지 방식으로 제어할 수 있다.
`openOverlay(id?)`와 `closeOverlay(id?)` 함수, ref의 `open()`과 `close()`,
선언적인 `visible` prop이다. `visible`을 쓰면
그 오버레이에서는 명령형 API가 무시된다.

### Liquid Glass 탭 바

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

여기서 `BlurTarget`은 Android의 live와 glass에서만 의미가 있고
다른 곳에서는 일반 `View`다.
오버레이는 `BlurTarget`의 자식이 아니라 형제여야
한다. 자기가 속한 하위 트리를 흐릴 수는 없기 때문이다.

### glass의 변형과 옵션

| prop                           | iOS 26 이상                 | Android 13 이상                                        |
| ------------------------------ | --------------------------- | ------------------------------------------------------ |
| `glassVariant="regular"`(기본) | `UIGlassEffectStyleRegular` | 10dp 블러에 흰색 쪽으로 밝힘. 우윳빛이면서 읽히는 모습 |
| `glassVariant="clear"`         | `UIGlassEffectStyleClear`   | 5dp 블러, 밝히지 않음. 선명하고 투명                   |
| `glassTint`                    | `tintColor`                 | 알파 비율로 틴트 색 쪽으로 섞는다                      |
| `interactive`                  | `interactive`               | 손가락 밑에서 부드러운 빛이 번지고 테두리가 밝아진다   |

Android에서는 `blurRadius`로 변형의 블러를 덮어쓸 수 있다.
iOS에서는 블러 양이 Apple의 것이어서
`blurRadius`와 `saturation`과 `downsampling`이 무시된다.

## 측정 결과

README는 Galaxy A22(Helio G80, Mali-G52)에서
잰 수치를 싣는다. 가진 기기 중 가장 약하다고 밝힌 기기다.

- 굴절 렌즈는 GPU 시간을 거의 더하지 않고,
`live` 대비 프레임당 RenderThread 약 0.4ms를 더한다.
- 60Hz에서는 프레임률을 유지하고
90번째 백분위 프레임 시간이 15~25ms이며 끊기는 프레임은 최대 3.6%다.
- 90Hz에서는 `live`와 `glass` 모두 예산 한계에 걸리고,
`glass`가 더 자주 넘는다. 끊기는 프레임이 실행에 따라 2~14%이고
`live`는 1.4~2.2%다.
- 전체 해상도로 캡처하면 90Hz에서 끊김이 100%여서 반해상도를 넘기지 않는다.
- 같은 패널이 `downsampling` 1에서 60Hz 기준 90번째 백분위 25ms,
끊김 약 6%였다. 그래서 live blur의 기본 `downsampling`은 2다.
- 상한 없이 두면 같은 패널이 90Hz에서 프레임의 31~56%가 끊겼다.
그래서 `maxUpdateFps`의 기본값은 30이다.

README는 이 수치의 전체 표와 트레이스를 저장소의
`docs/live-blur/RESULTS.md`에 둔다고 적는다.

## 조절 항목

| prop                | 기본값        | 의미                                                                                         |
| ------------------- | ------------- | -------------------------------------------------------------------------------------------- |
| `downsampling`      | 1(`live`는 2) | 블러 전에 캡처를 얼마나 줄이는가. 높을수록 빠르고 거칠다                                     |
| `maxUpdateFps`      | 30            | 초당 live 재블러 횟수 상한. 0이면 그려진 모든 프레임                                         |
| `captureOutset`     | 0             | live 캡처가 오버레이 가장자리 밖으로 나가는 거리. 가장자리에서 블러가 고정되는 현상을 없앤다 |
| `snapshotUpdateFps` | 0             | snapshot을 이 횟수만큼 다시 찍는다. Android 12 미만에서 움직이는 backdrop을 얻는 유일한 방법 |
| `blurRadius`        | -             | dp 단위 블러 반경. `radius`보다 우선한다                                                     |
| `radius`            | 20            | 물리 픽셀 단위 블러 반경(더 이상 쓰지 않는 prop)                                             |
| `saturation`        | 1             | 블러로 빠진 채도를 되돌린다                                                                  |
| `brightness`        | 0             | 밝기 오프셋. -255에서 255                                                                    |

### 반경은 단위를 조심한다

`radius`는 dp가 아니라 물리 픽셀이다.
같은 20이 밀도 1인 기기에서는 부드러운 흐림이고
밀도 3인 기기에서는 거의 안 보인다.
README의 조언은 `Math.round(PixelRatio.get() * 20)`처럼
밀도를 곱해 어디서나 약 20dp가 되게 하는 것이다.
더 간단하게는 dp 단위인 `blurRadius`를 쓰면 된다.

README는 30~40dp부터 패널이 색조가 아니라 frosted glass로 읽힌다고 적는다.

### snapshot과 live의 반경 한계

snapshot은 스택 블러를 쓰고 이 블러는 축소 후 반경을 25로 제한한다.
그래서 snapshot은 `radius = 25 × downsampling`에서
포화한다. 기본 `downsampling` 2에서는 50이다.
live는 플랫폼 `RenderEffect`를 써서 이런 한계가 없다.
두 모드를 런타임에 바꾸면 한계 위에서 블러 양이 달라 보일 수 있다.

## 함정

- **`SurfaceView` 기반 콘텐츠는 캡처되지 않는다.** 비디오 플레이어,
카메라 미리보기, 지도는 비어 보인다. snapshot과 앱 창 안의 live 모두 해당하고,
모달 안의 창 블러만 예외다.
- **`<Modal>`은 별도의 Android 창이라 캡처가 닿지 않는다.** 모달 안의
`blurMode="live"`는 캡처하지 않고
시스템에 모달 뒤 블러를 요청한다. 오버레이가 모달 전체를 덮어야 하고,
일부만 덮으면 거부되어 자기 영역의 snapshot으로 내려간다.
- **창 블러는 시스템이 거절할 수 있다.** 일부 GPU는 cross-window blur를 지원하지
않고, 절전 모드에서는 어디서나 꺼지며,
오버레이가 모달을 덮지 못하면 안 된다. 세 경우 모두 snapshot으로 폴백한다.
- **라이브 블러는 균일한 모서리 반지름만 클리핑한다.** `borderTopLeftRadius`
같은 모서리별 값은 snapshot에는 적용되지만 live에서는
직사각형이 된다. 둥근 `overflow: 'hidden'` 부모로 감싸는 것이 우회다.
- **전환 직후에 열면
직전 화면이 찍힌다.** 3.0 이후 snapshot은 오버레이가 마운트될 때 찍으므로,
내비게이션 전환 직후에 `openOverlay()`를 부르면
애니메이션 끝자락이 찍힐 수 있다. 전환이 끝난 뒤 열어야 한다.
- **블러가 평균이라 채도가 빠진다.** `saturation`을 1.5~1.8로 올리면
iOS와 비슷해진다. `brightness`는 채도를 고치지 못한다.
- **`live`가 live로 동작하지 않을 때는 logcat에서
이유를 본다.** `adb logcat -s BlurOverlay`로 확인한다. API 31 미만,
같은 창에 `<BlurTarget>`가 없음(모달은 별도 창), 오버레이가 target 안에 있음,
모달에서 cross-window blur가 꺼짐이 일반적인 이유다.

## 트레이드오프

### 기본값이 정지 이미지라서 코드를 바꾸지 않으면 움직이지 않는다

`snapshot`이 기본인 이유는 3.0 사용자를 놀라게 하지 않기 위해서다.
그래서 스크롤하는 콘텐츠 위의 유리를 원하면
`<BlurTarget>`를 감싸고 `blurMode`를 명시해야 한다.
Android 12 미만에서는
`snapshotUpdateFps={30}`과 `downsampling` 3~4가 거친 대안이고,
README는 30보다 낮은 값은 슬라이드쇼처럼 보인다고 경고한다.

### 구조를 바꿔야 한다

live와 glass는 뒤 화면이 될 콘텐츠를 `<BlurTarget>`로 감싸고
오버레이를 형제로 둬야 한다.
탭 바처럼 화면 구조가 고정된 곳에는 어렵지 않지만,
어디서든 쓰는 범용 컴포넌트로 만들려면 구조를 먼저 정해야 한다.

### 유리 느낌은 오버레이이고 시스템 컴포넌트가 아니다

iOS에서는 `UIGlassEffect`를 오버레이의 `borderRadius`에 맞춰 쓰고,
Android는 라이브러리가 만든 렌즈다.
README는 Android 렌즈를 Kyant0/AndroidLiquidGlass(렌즈 프로파일)와
QWEA0/Liquid-Glass-Android(하이라이트와 분산)의 오픈소스 구현에서
가져왔다고 밝힌다.

## 체크리스트

- React Native 0.80 이상인가(아니면 2.x인가).
- 스크롤하는 콘텐츠 위의 유리라면
`<BlurTarget>`를 감싸고 오버레이를 형제로 두었는가.
- `blurMode`를 명시했는가.
- 반경을 dp로 지정했는가(`blurRadius`).
- 비디오, 카메라, 지도 위에 유리를 올리고 있지 않은가.
- 모달에서 오버레이가 모달을 덮는가.
- 낮은 사양 기기에서 60Hz와 90Hz를 모두 측정했는가.
- 전환 직후에 열면 안 되는 곳에서 전환이 끝난 뒤 여는가.

## 기억할 원칙

### 폴백이 단계로 정의되어 있어 설정을 무조건 켜 두어도 안전하다

이 라이브러리의 설계에서
가장 쓸모 있는 부분은 각 모드가 불가능할 때 조용히 내려가고
이유를 logcat에 남기는 것이다.
최고 단계를 설정해 두고, 기기가 못 따라오면
낮은 단계로 보이게 하는 방식은 낮은 버전을
지원하는 앱에 그대로 옮겨 쓸 수 있는 원칙이다.
