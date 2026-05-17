# expo-linear-gradient — Expo 선형 그래디언트 컴포넌트

<https://docs.expo.dev/versions/latest/sdk/linear-gradient/>

## 소개

`expo-linear-gradient`는 Android, iOS, tvOS, Web, Expo Go에서 동작하는 범용
React 컴포넌트로, 선형 방향으로 여러 색상이 전환되는 그래디언트 뷰를 제공한다.
설치는 다음 명령으로 한다.

```bash
npx expo install expo-linear-gradient
```

## API

### LinearGradient 컴포넌트

`LinearGradient`는 `View`를 상속한 컴포넌트로, `View`의 모든 props를 수용한다.

#### colors (필수)

```ts
colors: readonly (string | null | undefined)[]
```

최소 두 개 이상의 색상 배열이 필요하다.
각 색상은 CSS 색상 문자열, `null`, `undefined`를 허용한다.

#### start / end (선택)

```ts
start?: LinearGradientPoint | null
end?: LinearGradientPoint | null
```

그래디언트의 시작점과 끝점을 `{x, y}` 좌표 또는 `[x, y]` 튜플로 지정한다.
값의 범위는 0에서 1 사이이며, 뷰 크기에 대한 비율로 해석된다.
Web에서는 각도(direction)만 변경되고 위치 조정은 지원되지 않는다.

#### locations (선택)

```ts
locations?: readonly number[] | null
```

각 색상 정지점(color stop)의 위치를 0~1 범위로 지정하는 배열이다.
`colors` 배열과 길이가 같아야 하며, 오름차순으로 정렬되어야 한다.

#### dither (Android 전용, 선택)

```ts
dither?: boolean  // 기본값: true
```

색상 밴딩(color banding) 현상을 완화하는 Android 전용 옵션이다.

### 타입

| 타입                        | 정의                            |
| --------------------------- | ------------------------------- |
| `LinearGradientPoint`       | `{x: number; y: number}` 또는 `[x, y]` 튜플 |
| `NativeLinearGradientPoint` | `[x: number, y: number]` 튜플  |

### 사용 예시

```tsx
import { StyleSheet, Text, View } from "react-native";
import { LinearGradient } from "expo-linear-gradient";

export default function App() {
  return (
    <View style={styles.container}>
      <LinearGradient
        colors={["#4c669f", "#3b5998", "#192f6a"]}
        style={styles.button}
      >
        <Text style={styles.text}>Sign in with Facebook</Text>
      </LinearGradient>
    </View>
  );
}
```

## 분석

### 좌표계 설계의 특성

`start`와 `end`에 사용하는 좌표 시스템은 절대 픽셀이 아닌 0~1 비율이다.
`{x: 0, y: 0}`은 뷰의 좌상단, `{x: 1, y: 1}`은 우하단에 해당한다.
이 설계는 뷰 크기와 무관하게 그래디언트 방향을 정의할 수 있게 하여 반응형
레이아웃에서 재계산 없이 재사용할 수 있다.

### Web 플랫폼의 제약

`start`와 `end` 좌표가 Web에서는 각도 변환만 적용되고 정밀한 위치 제어는 되지
않는다.
이는 CSS `linear-gradient()`가 방향(angle 또는 to 키워드)만 지원하고 시작/끝
좌표 개념이 없는 명세 차이에서 비롯된다.
네이티브에서는 CoreGraphics(iOS)와 Canvas API(Android)가 좌표 기반 그래디언트를
직접 지원하므로 정밀도가 다르다.

### dither 옵션의 존재 이유

8비트 색상 채널을 사용하는 디스플레이에서 미세한 색상 전환 영역은 계단 현상
(banding)이 발생한다.
Android의 `dither` 옵션은 인접 픽셀에 무작위 노이즈를 더해 이 계단 현상을
시각적으로 줄인다.
iOS에서는 별도 옵션 없이 렌더링 파이프라인이 자동으로 처리하기 때문에 API에
노출되지 않는다.

## 비평

### 강점

API가 극히 단순하다.
필수 prop이 `colors` 하나뿐이고 나머지는 모두 선택이어서 최소한의 코드로 즉시
사용할 수 있다.
`View`를 상속하므로 `style`, `children` 등 기존 레이아웃 패턴을 그대로 적용할
수 있다.
Android, iOS, Web을 단일 컴포넌트로 커버하는 점도 실용적이다.

### 약점 및 한계

Web에서의 `start`/`end` 제약이 문서에 간략히 언급만 될 뿐 구체적인 동작 차이가
설명되지 않는다.
크로스플랫폼 일관성을 기대하다가 Web에서만 다르게 렌더링되는 경우를 미리 파악하기
어렵다.
`colors`에 `null`과 `undefined`를 허용하는 이유도 설명이 없어 의도를 파악하기
어렵다.

### 대안 언급의 아쉬움

문서는 React Native의 실험적 `backgroundImage` 스타일 속성과 CSS 그래디언트
문법을 대안으로 언급한다.
그러나 언제 이 라이브러리를 쓰고 언제 `backgroundImage`를 써야 하는지에 대한
결정 기준이 제시되지 않는다.
“실험적”이라는 표현으로 암묵적인 방향을 제시하지만, 명확한 가이드라인이 있었다면
더 유용했을 것이다.

## 인사이트

### “최소 필수 props” 설계가 전달하는 철학

`expo-linear-gradient`의 API에서 필수 prop은 `colors` 하나뿐이다.
방향, 위치, 정지점은 모두 기본값이 있거나 생략 가능하다.
이 설계는 “80%의 사용 사례를 한 줄로” 처리하게 하고, 복잡한 요구는 추가 prop으로
단계적으로 해결하도록 유도한다.

React 생태계의 컴포넌트 API 설계에서 이 패턴은 중요한 원칙이다.
필수 prop이 많을수록 진입 장벽이 높아지고, 컴포넌트의 채택율이 낮아진다.
`LinearGradient`는 `colors`만 넘기면 곧바로 동작하는 결과를 보여줌으로써
개발자에게 즉각적인 성공 경험을 제공한다.
이 “즉각적 보상” 설계는 라이브러리 채택 전략의 핵심이기도 하다.

### 비율 좌표계가 해결하는 반응형 문제

`start`와 `end`를 픽셀 대신 0~1 비율로 정의하는 선택은 반응형 UI의 근본적인
문제를 해결한다.
그래디언트가 적용된 뷰의 크기가 달라져도 — 화면 크기가 다른 기기, 동적 레이아웃,
화면 회전 — 방향과 전환 비율이 그대로 유지된다.
픽셀 좌표였다면 뷰 크기가 변할 때마다 재계산 로직이 필요했을 것이다.

이 패턴은 SVG의 `gradientUnits=“objectBoundingBox”` 개념, CSS `background-size`
의 퍼센트 단위와 같은 맥락이다.
UI 렌더링 시스템이 성숙해질수록 “절대값이 아닌 비율로 표현하라”는 원칙이 반복된다.
크기에 독립적인 표현 방식은 컴포넌트를 재사용 가능한 독립 단위로 만드는 핵심
조건이다.

### 플랫폼 파편화를 단일 API 뒤에 숨기는 비용

`expo-linear-gradient`는 iOS의 CoreGraphics, Android의 Canvas, Web의 CSS를
단일 `LinearGradient` API로 추상화한다.
이 추상화 덕분에 개발자는 플랫폼별 구현을 알 필요가 없다.
그러나 Web에서의 `start`/`end` 제약처럼, 추상화 경계에서 플랫폼별 한계가
새어 나오는 지점이 반드시 존재한다.

이것은 크로스플랫폼 추상화의 구조적 딜레마다.
추상화 수준을 높이면 가장 기능이 제한된 플랫폼에 맞춰 API가 제한된다.
반대로 플랫폼별 기능을 모두 노출하면 API가 복잡해지고 크로스플랫폼 이점이 줄어든다.
`expo-linear-gradient`는 전자를 선택했고, `dither`처럼 Android 전용 prop을
예외적으로 허용하는 방식으로 일부 균형을 잡는다.
이 절충점을 이해하면 향후 비슷한 크로스플랫폼 라이브러리의 한계를 API만 보고도
예측할 수 있다.
