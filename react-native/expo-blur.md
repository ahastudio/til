# expo-blur: 뒤 화면을 흐리는 Expo의 BlurView와 Android용 BlurTargetView

<https://docs.expo.dev/versions/latest/sdk/blur-view/>

## 소개

`expo-blur`는 자기 아래에 있는 모든 것을 흐리는
React 컴포넌트 `BlurView`를 주는 Expo SDK 패키지다.
내비게이션 바, 탭 바, 모달에 흔히 쓴다고 문서는 소개한다.
이 문서를 쓴 2026년 10월 20일 기준 최신 버전은 58.0.5(2026년 10월 19일)이고
라이선스는 MIT다.
Android, iOS, tvOS, Web을 지원하고 Expo Go에 포함되어 있다.

Android 지원은 SDK 55부터 안정(stable) 상태다.
다만 코드를 고쳐야 한다. 예전 방식의 `BlurView`는 iOS와 웹에서만 흐려지고,
Android에서는 반투명 배경만 나온다.
이 문서에서 가장 중요한 점이 이것이다. Android에서
실제 블러를 얻으려면 `BlurTargetView`를 함께 써야 한다.

## 동작 방식

### 흐려질 내용을 BlurTargetView로 감싼다

Android에서는 흐려질 콘텐츠를 `BlurTargetView`로 감싸고,
그 ref를 `BlurView`의 `blurTarget`에 넘긴다.
`BlurView` 여러 개가 하나의 `BlurTargetView` 범위 안에 들어오면
하나를 공유할 수 있고,
이것이 여러 개를 만드는 것보다 효율적이라고 문서는 안내한다.

```tsx
import { BlurView, BlurTargetView } from 'expo-blur';
import { useRef } from 'react';
import { Text, StyleSheet, View } from 'react-native';

export default function App() {
  const targetRef = useRef<View | null>(null);
  const text = 'Hello, my container is blurring contents underneath!';

  return (
    <View style={styles.container}>
      <BlurTargetView ref={targetRef} style={styles.background}>
        {[...Array(20).keys()].map(i => (
          <View
            key={`box-${i}`}
            style={[styles.box, i % 2 === 1 ? styles.boxOdd : styles.boxEven]}
          />
        ))}
      </BlurTargetView>
      <BlurView
        blurTarget={targetRef}
        intensity={100}
        style={styles.blurContainer}
        blurMethod="dimezisBlurView">
        <Text style={styles.text}>{text}</Text>
      </BlurView>
    </View>
  );
}
```

위 코드는 문서의 예제에서
`BlurView` 하나만 남긴 것이다. 스타일 정의와 나머지 두 `BlurView`는 생략했다.

### blurMethod가 Android 동작을 정한다

| 값                           | 동작                                                                                               |
| ---------------------------- | -------------------------------------------------------------------------------------------------- |
| `'none'`(기본값)             | 블러 대신 반투명 뷰를 그린다                                                                       |
| `'dimezisBlurView'`          | BlurView 라이브러리(Dimezis)를 쓰는 네이티브 블러. Android SDK 30 이하에서는 성능이 떨어질 수 있다 |
| `'dimezisBlurViewSdk31Plus'` | 같은 구현을 SDK 31 이상에서만 쓰고, 그 아래에서는 `'none'`으로 폴백한다                            |

기본값이 `'none'`이라는 점이 함정이다.
`blurTarget`만 넘기고 `blurMethod`를 빼면 Android에서 블러가 안 보이고
반투명 뷰만 나온다. 이 설명은 문서의 기본값 표기를 따른 이 문서의 해석이다.

### 성능은 Android 12가 경계다

문서에 따르면 효율적인 블러는 Android SDK 31(Android 12)에서
들어온 `RenderNode` API로만 가능하다.
그보다 낮은 버전에서는 훨씬 비효율적인 `RenderScript`를 쓴다.
낮은 버전의 성능 저하를 피하려면 `dimezisBlurViewSdk31Plus`를 쓰면 된다.

### 주요 props

| prop                           | 기본값      | 의미                                                                       |
| ------------------------------ | ----------- | -------------------------------------------------------------------------- |
| `intensity`                    | 50          | 1에서 100 사이의 블러 강도. react-native-reanimated로 애니메이션할 수 있다 |
| `tint`                         | `'default'` | 블러 위에 얹는 색조. 어떤 값이든 반투명 색 층이 하나 더해진다              |
| `blurMethod`(Android)          | `'none'`    | 위 표 참고                                                                 |
| `blurReductionFactor`(Android) | 4           | Android에서 블러 강도를 나누는 수. iOS와 체감을 맞추는 데 쓴다             |
| `blurTarget`(Android)          | -           | 흐릴 `BlurTargetView`의 ref                                                |

## 알려진 문제와 최근 변경

문서의 알려진 문제는 하나다.
`FlatList` 같은 동적 콘텐츠보다 `BlurView`를 먼저 렌더링하면
블러가 갱신되지 않는다. `BlurView`를 동적 콘텐츠 컴포넌트 뒤에 렌더링해야 한다.

저장소의 변경 이력에서 Android 관련 항목을 추리면 다음과 같다.

- 58.0.0: `BlurView`가 둥근 모서리 스타일을 네이티브 블러 레이어에 적용하지
못하던 문제와,
화면 종료 애니메이션 중 `BlurTargetView` 안의 콘텐츠가 사라지던 문제를 고쳤다.
- 57.0.1: `BlurTargetView` 아래의 뷰를 제스처 핸들러가 분리된 것으로 보고
제스처를 취소하던 문제를 고쳤다.
- 58.0.4와 58.0.5: React Native 0.87 이상의 ref 타입과 콜백
ref를 `blurTarget`과 `BlurTargetView`의 `ref`에서 받도록 했다.

## 트레이드오프

### 블러만 있고 굴절은 없다

`expo-blur`는 Liquid Glass의 굴절이나 색 분산을 제공하지 않는다.
틴트와 블러만으로 유리 느낌을 내려면 `tint`와 둥근 모서리,
테두리를 직접 더해야 한다. 이는 이 문서의 판단이다.

### 블러 대상을 앱이 명시해야 한다

iOS의 `BlurView`는 자기 아래의 모든 것을 흐리지만,
Android는 `BlurTargetView`로 감싼 범위만 흐린다.
화면의 어느 부분이 뒤 화면이 될지 구조로 정해야 하므로
컴포넌트 트리를 바꾸게 된다.
이 구조는 하단 바나 시트처럼 고정된 위치의 유리 요소에는 맞고,
모든 화면 위에 떠 있는 요소에는 부담이라고 이 문서는 본다.

### 낮은 버전은 반투명 뷰와 느린 블러 중에 고른다

SDK 30 이하를 지원하면 `dimezisBlurView`로 느린 블러를 받거나,
`dimezisBlurViewSdk31Plus`로 반투명 뷰에 만족해야 한다.

## 함정

- Android에서 `blurMethod`를 안 쓰면 블러가 안 보인다.
- `blurTarget` 없이 `BlurView`만 쓰면 Android에서
대상이 없다. SDK 55부터 `BlurTargetView`가 필요하다.
- 동적 콘텐츠 목록보다 먼저 렌더링한 `BlurView`는 갱신되지 않는다.
- Android의 `intensity`는 iOS와 체감이 다르다. `blurReductionFactor`로 맞춘다.
- `tint`를 주면 항상 반투명 색 층이 더해진다. 블러만 원하면 `tint`를 비운다.

## 체크리스트

- Android에서 블러가 필요한 곳에 `BlurTargetView`와 `blurTarget`을 연결했는가.
- `blurMethod`를 명시했는가(기본값은 `'none'`).
- Android 11 이하에서
`RenderScript` 비용과 `Sdk31Plus` 폴백 중 무엇을 택할지 정했는가.
- `BlurView`를 동적 콘텐츠 뒤에 렌더링했는가.
- `intensity`와 `blurReductionFactor`를 두 플랫폼에서 눈으로 맞췄는가.

## 기억할 원칙

### 이 라이브러리는 블러까지만 맡는다

`expo-blur`는 Expo가 관리하는 안정된 블러이고,
유리의 굴절은 그 위에서 다른 도구로 얻어야 한다.
Liquid Glass 느낌을 원하면 블러의 안정성은 `expo-blur`에서 얻고
굴절은 포기하거나, 굴절까지 주는 다른 라이브러리를 고르는 것이 갈림길이다.
