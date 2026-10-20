# react-native-liquid-glassmorphism: Android 13의 AGSL 굴절 셰이더와 iOS 26의 UIGlassEffect를 한 컴포넌트로 묶은 라이브러리

<https://github.com/himanshu-lal4/react-native-liquid-glassmorphism>

## 소개

`react-native-liquid-glassmorphism`은 하나의 `<LiquidGlassView>`로 iOS 26에서는
Apple의 네이티브 `UIGlassEffect`를, Android 13 이상에서는
AGSL 굴절 셰이더로 만든 유리를 그리는 React Native 라이브러리다.
저장소는 2026년 7월에, npm 패키지는 2026년 6월에 만들어졌다.
이 문서를 쓴 2026년 10월 20일 기준 최신 버전은 1.2.1(2026년 8월 20일)이고,
라이선스는 MIT, GitHub 별은 약 30개로 이 문서에서
다루는 React Native 라이브러리 중 가장 새롭고 작은 프로젝트다.

README가 스스로 내세우는 차별점은 세 가지다.

- Android에서 블러가 아니라 굴절(edge refraction)과 색 분산을 낸다.
- 가까워지면
유리가 하나로 합쳐지는 병합(`LiquidGlassContainer`)을 두 플랫폼 모두에서 낸다.
- 원, 별, 오목한 SVG 경로 같은 임의의 모양(`shape`)에도 굴절을 입힌다.

README는 자기 라이브러리를 `expo-blur`,
`@callstack/liquid-glass` 등과 비교하는 표를 싣는다.
이 표는 저자가 직접 만든 것이고,
비교 대상에 대한 평가가 자기 라이브러리에 유리하게 기울어 있을 수 있어서
이 문서는 표의 판정을 사실로 옮기지 않았다.
README에는 후원 링크와 검색어를 나열한 문단도
있다. 기술적 내용은 별개로 읽어야 한다.

## 요구 사항

| 항목         | 최소                | 전체 효과                            |
| ------------ | ------------------- | ------------------------------------ |
| iOS          | iOS 15(블러 폴백)   | iOS 26 SDK와 Xcode 26(네이티브 유리) |
| Android      | API 24(반투명 폴백) | API 33 이상(AGSL 굴절 셰이더)        |
| React Native | 0.83 이상           | 새 아키텍처와 구 아키텍처 모두       |

Android 빌드에는 compileSdk 34 이상과 최신 NDK가 필요하고,
저자는 NDK `27.1.12297006`으로 시험했다고 적는다.
네이티브 모듈이라 Expo Go에서는 쓸 수 없고
개발 빌드나 `expo prebuild`가 필요하다. 서드파티 네이티브 의존성은 없다.

## 사용하기

```tsx
import { LiquidGlassView } from 'react-native-liquid-glassmorphism';

<LiquidGlassView
  variant="regular"        // 'regular' | 'clear'
  tintColor="rgba(10,132,255,0.5)"
  interactive              // reacts to touch + device tilt
  borderRadius={24}
  style={{ padding: 16 }}
>
  <Text>Frosted glass content</Text>
</LiquidGlassView>
```

자식은 유리 위에 선명하게 그려지고 뒤의 backdrop만 처리된다.
`interactive`와 `tilt`는 유리 뷰 자신의 터치로 구동되므로
전경 콘텐츠가 형제가 아니라 자식이어야 한다. 자식이 없으면
조용히 아무 일도 하지 않는다.

### 읽히게 만드는 장치

`clear` 유리는 뒤의 내용을 그대로 전달해서
바쁜 콘텐츠 위에서는 아이콘과 글자가 읽기 어려울 수 있다.
`legibilityFloor`(0에서 1,
Android 전용)가 자식 뒤에 적응형 베일을 깔아 글자가 읽히게 하고,
`tintColor`로 색을 입힌다.

```tsx
<LiquidGlassView
  variant="clear"
  legibilityFloor={0.4}
  tintColor="rgba(10,9,8,0.5)"
  edgeReflectionStrength={0.4}
  style={styles.tabBar}
>
  {/* icons + labels stay readable */}
</LiquidGlassView>
```

### 프리셋

`navigationBar`, `floatingTabBar`, `cardOverMedia`,
`compactControl`, `frosted`, `crystal` 여섯 개가 있다.
프리셋은 JS에서 `{ ...GlassPresets[preset], ...yourProps }`로 풀리므로
명시한 prop이 항상 이긴다.

### 블러 뷰나 스크림으로도 쓴다

`rim`, `specular`, `thickness`를 끄면 유리가 평범한 블러 뷰가 되고,
세 가지를 모두 끄면 iOS도 Liquid Glass 대신 일반 `UIBlurEffect`를 쓴다.
`dim`(0에서 1)은 자식 아래에 평평한 스크림을 깔아
모달 배경을 만든다. 두 플랫폼에서 모두 동작한다.

## Android에서 렌더링되는 방식

README의 설명에 따르면 Android는 프레임마다 다음을 한다.

1. 유리 뒤의 뷰 계층을 축소한 비트맵으로 캡처한다.
2. GPU 가우시안 블러를 건다.
3. 유리 모양을 모델링한 AGSL 셰이더를 건다. 부호 거리장에서 얻은 surface normal,
스넬 식 가장자리 굴절, 색 분산, 반사된 가장자리, frost 정도와 틴트,
프레넬 림, 기울기와 터치에 반응하는 하이라이트가 이어진다.

`shape`를 주면
모양이 부호 거리장(SDF) 텍스처로 래스터화되어 셰이더가 샘플링하므로,
굴절과 림이 임의의 외곽선을 따른다.

### 버전 단계

| API 수준 | `tier`       | 그려지는 것                                                   |
| -------- | ------------ | ------------------------------------------------------------- |
| 33 이상  | `refraction` | 블러, 바이브런시, 가장자리 굴절, 틴트, 하이라이트의 전체 렌즈 |
| 31~32    | `blur`       | 블러와 캔버스 틴트와 하이라이트(굴절 없음)                    |
| 30 이하  | `tint`       | 반투명 틴트와 림만                                            |

장치가 어느 단계로 그릴지는 마운트 전에 `getGlassCapabilities()`나
`useGlassSupport()`로 알 수 있고,
실제로 그려진 단계는 `onPipelineReady`로 받는다.

```tsx
function Panel() {
  const { tier, supportsRefraction } = useGlassSupport();
  if (tier === 'none') return <FlatPanel />;
  return <LiquidGlassView preset="cardOverMedia">…</LiquidGlassView>;
}
```

## 성능과 한계

README의 한계 절은 구체적이다.

- **유리 뷰마다 자기 backdrop을 캡처한다.** 화면에 열 개가 있으면
프레임마다 전체 소프트웨어 `rootView.draw()`가 열 번이다. 긴 `FlatList`에 유리를
넣는 데 걸리는 상한이고, 캡처를 공유하는 개선은 이슈 38번으로 추적 중이다.
- **GPU 기반 뷰는 캡처할 수 없다.** 비디오 플레이어, `SurfaceView`, 지도,
일부 카메라 미리보기는 소프트웨어 그리기를 거부해서
유리가 이전 backdrop을 재사용하고
`BACKDROP_CAPTURE_FAILED`를 보고한다. Android에서
재생 중인 비디오 위의 유리는 동작하지 않는다.
- **Android 13 미만은 Liquid Glass가 아니다.** API 31~32는 블러와 틴트이고,
31 미만은 반투명 틴트뿐이다. 단계는 자동이지만
미묘한 차이가 아니라 분명한 하향이다.
- **`secondaryShape` 병합은 고정된 외곽선용이다.** CPU에서
거리장을 미리 계산하는 데 340×190dp 도형 기준 약 361ms(Realme RMX3868)가 들고,
간격을 애니메이션하면
시험 화면이 1.6fps가 됐다. 한 번 설정하고 그대로 둬야 한다.
- **컨테이너 병합은 Android에서 최대 8개**이고
둥근 직사각형만 합친다. 사용자 `shape`는 병합하지 않는다. iOS는 OS가 합쳐서
한계가 없다.
- **SVG 경로의 타원 호(`A`)는 지원하지 않는다.** 베지어로 바꿔야 한다.
- 웹은 유리가 아닌 폴백이다.

성능을 위한 순서는 다음과 같이 안내한다.

1. 화면에 보이지 않는 유리에는 `paused`를 준다. 화면 밖으로 밀린 화면,
비활성 탭, 백그라운드 앱은 Android가 알려 주므로 스스로 멈춘다.
2. 인스턴스를 줄인다.
3. `tilt`는 꼭 필요할 때만 켠다. 센서를 등록하고 이벤트마다 다시 그린다.
4. 단순한 `shape`를 쓴다.
5. 렌즈가 하는 일이 없으면 `thickness={0}`.

개발 중에는 `frameStatsInterval`과 `onFrameStats`로 `drawFps`, `captureMs`,
`shaderMs`를 받을 수 있다. 이 값은 CPU 쪽 시간이고
GPU 셰이더 실행 시간은 보이지 않는다. 지터를 찾을 때는
평균인 `totalMs`가 아니라 `maxTotalMs`를 보라고 README는 적는다.

## 접근성

`accessibilityMode`의 기본값 `auto`는 플랫폼이 투명도 감소를 요청하면
불투명 면을 그리고, 모션 감소에서는 `tilt`를 끈다.
README는 Android에는 투명도 감소 설정이 없어서
가장 가까운 신호로 고대비 텍스트를 쓴다고 적고,
이것이 진짜 선호가 아닌 대용품이라고 인정한다.
`forceGlass`는 투명도 선호를 무시하므로,
유리가 장식일 뿐 의미가 다른 곳에 있을 때만 쓰라고 경고한다.
`interactive`는 방금 한 터치에 반응하는 것이어서 모션 감소가 막지 않는다.

## 트레이드오프

### 기능이 가장 많은 만큼 가장 어리다

굴절, 병합, 임의 모양, 프리셋, 접근성 모드, 프레임 통계까지 한 패키지에 있다.
반면 만들어진 지 몇 달이고 GitHub 별이 약 30개 규모라서
장기 유지와 호환성의 근거가 적다. 이는 저장소 통계에서 이 문서가 내린 판단이다.

### 프레임마다 캡처한다

README가 의도적으로 캡처를 줄이지 않는다고
적을 만큼 이 라이브러리는 프레임 단위의 캡처를 선택했다.
움직이는 배경에서 backdrop이 정확하다는 장점이 있지만
비용이 유리 뷰 수에 비례한다.
이 비용은 이 문서가 직접 측정하지 않았다.

### React Native 0.83 이상이 필요하다

이 문서에서 다룬 라이브러리 중 요구하는 React Native 버전이 가장 높다.
앱이 0.80~0.82 구간이면 이 라이브러리를 쓸 수 없다.

## 체크리스트

- React Native 0.83 이상이고 compileSdk 34 이상인가.
- 화면 안의 유리 뷰가 몇 개이고 어느 것이 화면
밖에서도 마운트되어 있는가(`paused`).
- 비디오, `SurfaceView`, 지도 위에 유리를 올리지 않았는가.
- `getGlassCapabilities()`로 단계를 확인해 `tint` 단계에서
평면 디자인으로 바꾸는가.
- `tilt`를 꼭 필요한 곳에만 쓰는가.
- 접근성에서 Android의 고대비 텍스트가 대용품이라는 점을 감안했는가.
- 개발 빌드에서 `maxTotalMs`로 지터를 확인했는가.

## 기억할 원칙

### 기능 목록보다 한계 목록이 선택의 근거다

이 라이브러리의 README가 가장 쓸모 있는 부분은
“이 라이브러리가 잘 못 하는 것”을 직접 나열한 절이다.
캡처 비용, 비디오 위 유리 불가,
낮은 버전의 하향 같은 한계는 다른 라이브러리에도 대부분 적용되는 Android
캡처 방식의 구조적 한계이므로, 어느 것을 고르든 먼저 읽어 두면 좋다.
