# React Native Skia: Canvas 안에서 backdrop 블러와 셰이더로 유리 효과를 직접 그리는 그래픽 라이브러리

<https://wcandillon.github.io/react-native-skia/>

<https://github.com/wcandillon/react-native-skia>

## 소개

React Native Skia는 Chrome, Android,
Flutter 등이 쓰는 2D 그래픽 엔진 Skia를 React Native에 가져온 라이브러리다.
Liquid Glass를 위한 전용 라이브러리가 아니라 범용 그래픽 도구이고,
`BackdropBlur`와 `RuntimeShader`로 유리 효과를 직접 그릴 수 있다는 점에서
이 주제와 닿는다.
이 문서를 쓴 2026년 10월 20일 기준 최신 버전은 3.7.1(2026년 10월 19일)이고
라이선스는 MIT, GitHub 별은 약 8,700개다.

저장소 주소가 `Shopify/react-native-skia`에서
`wcandillon/react-native-skia`로 옮겨졌고,
npm 패키지 이름도 `@shopify/react-native-skia`에서
`react-native-skia`로 바뀌었다.
옛 이름이나 v2에서 올라오려면 문서의 마이그레이션 가이드를 따라야 한다.

## v3와 v2

README는 두 계열을 나란히 비교한다.

| 항목        | v3                                        | v2                    |
| ----------- | ----------------------------------------- | --------------------- |
| npm         | `react-native-skia`                       | `react-native-skia@2` |
| Skia 백엔드 | Graphite(Android는 Vulkan, Apple은 Metal) | Ganesh(OpenGL, Metal) |
| 아키텍처    | 멀티 스레드                               | 단일 스레드           |
| Android TV  | 지원하지 않음                             | 지원                  |

v2도 계속 유지보수된다. Android에서 OpenGL ES가 필요한 기기는 v2를 써야 한다.

## 요구 사항(v3)

| 항목             | 최소 조건                                                                 |
| ---------------- | ------------------------------------------------------------------------- |
| React Native     | 0.79 이상, New Architecture                                               |
| React            | 19                                                                        |
| iOS              | 15.1                                                                      |
| Android          | API 26(`minSdkVersion = 26`)                                              |
| Reanimated(선택) | `react-native-reanimated` 4.0.0 이상과 `react-native-worklets` 0.7.0 이상 |

React Native 프로젝트의 기본 `minSdkVersion`은 이보다 낮아서
`android/build.gradle`에서 올려야 한다.
Android NDK도 필요하다.

### Android에서는 Vulkan이 필수다

v3는 Vulkan 1.1로 그린다. 문서에 따르면
Android 10 이상으로 출시된 모든 64비트 기기가 지원한다.
라이브러리 매니페스트가 이를 필수 기능으로 선언하므로
Vulkan이 없는 기기에는 Play 스토어가 앱을 제공하지 않는다.
Vulkan이 없는 기기에서도 앱을 내려면 매니페스트에서 선언을 제거하고
`Skia.gpu.isAvailable`을 확인해야 하며, 그런 기기에서 캔버스는 비어 있게 된다.
Vulkan 없이 렌더링해야 한다면 OpenGL ES를 쓰는 v2를 쓰라고 문서는 안내한다.

### Expo Go는 쓸 수 없다

v3는 개발 빌드가 필요하다. Expo Go에는 v2의 네이티브 코드가 들어 있다.
Android의 `minSdkVersion`은 `expo-build-properties`로 26으로 올린다.

## 유리 효과를 그리는 도구

### BackdropBlur와 BackdropFilter

Skia의 backdrop 필터는 CSS의 `backdrop-filter`와 같다.
클리핑 영역 뒤에 있는 것에 블러 같은 이미지 필터를 건다.

```tsx
import {
  Canvas,
  Fill,
  Image,
  BackdropBlur,
  useImage,
} from "react-native-skia";

export const Filter = () => {
  const image = useImage(require("./assets/oslo.jpg"));

  return (
    <Canvas style={{ width: 256, height: 256 }}>
      <Image image={image} x={0} y={0} width={256} height={256} fit="cover" />
      <BackdropBlur blur={4} clip={{ x: 0, y: 128, width: 256, height: 128 }}>
        <Fill color="rgba(0, 0, 0, 0.2)" />
      </BackdropBlur>
    </Canvas>
  );
};
```

`BackdropBlur`는 블러 반경(`blur`)과 `clip`을 받고 자식으로 틴트를 그린다.
`BackdropFilter`는 첫 자식으로 이미지 필터를 받는다.
문서의 예는 `ColorMatrix`로 영역을 흑백으로 바꾼다.

이 예제에서 backdrop은 같은 `Canvas` 안에 그린 이미지다.
Skia의 효과는 Skia가 그린 픽셀에 걸리므로,
앱의 다른 React Native 뷰가 backdrop이 되려면
그 뷰가 이미지로 들어와야 한다고 이 문서는 읽는다.

### 굴절은 RuntimeShader로 직접 쓴다

`RuntimeShader`는 직접 쓴 셰이더를 이미지 필터로 적용한다.
필터링되는 이미지를 셰이더의 uniform으로 받는다.
문서의 예제는 굴절이 아니라 색 채널을 바꾸는 간단한 셰이더이므로,
유리 굴절 셰이더는 직접 써야 한다. 이 라이브러리가
Liquid Glass 효과를 제공하는 것은 아니다.

주의할 점이 하나 있다. `RuntimeShader`는 화면 밀도 배율을 고려하지 않는다.
문서가 권하는 방법은 필터를 걸기 전에 앱의 픽셀 밀도만큼 확대하고,
걸고
난 뒤 원래 크기로 줄이는 슈퍼샘플링이다. 이 작업은
`layer` prop을 가진 Skia 레이어에서 해야 한다.

### React Native 뷰를 backdrop으로 쓰려면

v2의 `makeImageFromView()`는 v3에서 제거됐다.
v3의 뷰 스냅샷은 React Native WebGPU가 담당한다.
`queue.drawElementImageToTexture()`로 뷰를 텍스처에 그리고,
`Skia.Image.MakeImageFromGPUTexture()`가
그 텍스처를 복사 없이 Skia 이미지로 감싼다.
이 스냅샷에는 텍스트, 이미지, SVG, 변환,
그림자와 Skia 캔버스까지 화면에 보이는 모든 것이 들어간다.
이 경로는 `react-native-webgpu` 0.14.0 이상이 필요하고,
Skia 버전별로 맞는 webgpu 버전 표가 문서에 있다. Skia 3.7.0 이상이면
webgpu 0.17.0 이상이다.
두 패키지는 같은 `react-native-webgpu-dawn`에 의존하고,
버전이 어긋나면
`Dawn version mismatch` 오류로 빌드가 실패하므로 함께 올려야 한다.

## 트레이드오프

### 가장 자유롭지만 가장 무겁다

유리 효과를 원하는 대로 그릴 수 있다는 장점이 있다.
대신 Vulkan 필수, `minSdkVersion` 26, Expo Go 불가,
NDK 필요, React 19와 New Architecture라는 조건이 붙는다.
그리고 뒤 화면이 React Native 뷰인 일반적인 앱에서는
스냅샷 경로(WebGPU)를 따로 설치하고
맞춰야 한다. 이 마지막 문장은 문서 내용에서 이 문서가 끌어낸 판단이다.

### 유리 효과는 직접 만든다

`BackdropBlur`는 블러만 한다.
굴절, 가장자리 하이라이트, 색 분산은 `RuntimeShader`로 직접 구현해야 하며,
이 문서가 읽은 문서에는 완성된 Liquid Glass 예제가 없다.
이 라이브러리를 이 주제로 고르는 것은 셰이더를 직접 쓸 수 있고
캔버스 안에서 모든 것을 그리는 설계일 때 합리적이다.

## 함정

- Android에서 `minSdkVersion`을 올리지 않으면 빌드가 실패한다.
- 개발 빌드가 아니라 Expo Go로 실행하면 v2의 네이티브 코드로 동작한다.
- `RuntimeShader`를 밀도 보정 없이 쓰면 결과가 흐리다.
- v3로 올릴 때 `makeImageFromView()`가 없어진다.
- Skia와 `react-native-webgpu`를 따로 올리면 Dawn 버전 불일치로 빌드가 깨진다.

## 체크리스트

- 앱이 Vulkan을 요구해도 되는가(Play 스토어 필터링).
- `minSdkVersion`이 26 이상이고 NDK가 설치되어 있는가.
- React Native 0.79 이상, React 19, New Architecture인가.
- 뒤 화면이 Skia 캔버스 안에 있는가,
아니면 React Native 뷰라서 스냅샷이 필요한가.
- `RuntimeShader`에 밀도 보정(슈퍼샘플링)을 했는가.
- Skia와 `react-native-webgpu`의 버전 조합을 문서의 표와 맞췄는가.

## 기억할 원칙

### 효과가 캔버스의 안인가 밖인가를 먼저 정한다

Skia는 캔버스에 그려지는 것을 완전히 통제하는 대신,
캔버스 밖의 네이티브 뷰는 직접 보지 못한다.
유리 효과를 만들 때 뒤 화면이 어디에 있는지가 라이브러리 선택을 정한다.
캔버스 안이면 Skia, 네이티브 뷰 계층이면 뷰를 캡처하는 라이브러리가 맞다.
