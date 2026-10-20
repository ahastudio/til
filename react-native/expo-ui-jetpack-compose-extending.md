# Expo UI로 Jetpack Compose 컴포넌트와 modifier를 직접 만들어 React Native에 연결하기

원문: [Extending with Jetpack Compose - Expo documentation](https://docs.expo.dev/guides/expo-ui-jetpack-compose/extending/)

## 소개

이 가이드는 Expo Modules API로 커스텀 Jetpack Compose
컴포넌트와 modifier를 만들어 Expo UI와 연결하는 방법을 설명한다.
Liquid Glass 관점에서 의미가 있는 이유는,
Haze나 Kyant Backdrop 같은 Compose 기반 라이브러리를 React Native 앱에서 쓰려면
이런 연결을 직접 만들어야 하기 때문이다. 이 연결의 한계는 아래 트레이드오프에서
다룬다.
가이드를 읽은 2026년 10월 20일 기준 권장 버전은 `@expo/ui` 58.0.21이다.

## 준비물

- `@expo/ui` 설치.
- 개발 빌드. 커스텀 Expo 모듈은 네이티브 코드를 포함하므로
Expo Go가 로드하지 못한다.
- Expo Modules API와 Jetpack Compose에 대한 기본 지식.

## 만드는 순서

### 로컬 모듈과 Gradle 설정

`npx create-expo-module@latest --local my-ui`로
프로젝트 안에 로컬 모듈을 만든다.
모듈의 `android/build.gradle`에서 Compose 컴파일러 플러그인을 적용하고
`buildFeatures { compose true }`를 켠다.
그리고
`expo-ui`와 쓸 Compose 라이브러리에 의존한다. 가이드의 예는
`foundation-android` 1.10.6, `ui-android` 1.10.6, `material3` 1.5.0-alpha17이다.

### Compose 뷰

뷰는 두 부분으로 이뤄진다.

- props 데이터 클래스: `@OptimizedComposeProps` 애너테이션이 붙고
`ComposeProps`를 구현하며,
modifier를 받는 `modifiers: ModifierList` 필드를 가진다.
- `@Composable` 콘텐츠 함수: `FunctionalComposableScope`의 확장 함수이고,
`ModifierRegistry.applyModifiers(...)`를 호출하며
`Children(...)`으로 React 자식을 그린다.

```kotlin
@OptimizedComposeProps
data class MyCustomViewProps(
  val title: String = "",
  val modifiers: ModifierList = emptyList()
) : ComposeProps

@Composable
fun FunctionalComposableScope.MyCustomViewContent(props: MyCustomViewProps) {
  Column(
    modifier = ModifierRegistry.applyModifiers(
      props.modifiers,
      appContext,
      composableScope,
      globalEventDispatcher
    )
  ) {
    Text(text = props.title, style = MaterialTheme.typography.titleMedium)
    Children(UIComposableScope()) // Renders React children
  }
}
```

### 모듈 등록과 JS 래퍼

모듈에서는
`ExpoUIView("MyCustomView") { Content { props -> MyCustomViewContent(props) } }`로 뷰를 등록한다.
JS에서는
`requireNativeView('MyUi', 'MyCustomView')`로
네이티브 뷰를 가져와 래퍼 컴포넌트로 감싼다.
래퍼에서 `createViewModifierEventListener`를 쓰면
`clickable`이나 `onVisibilityChanged` 같은
이벤트 기반 modifier가 커스텀 뷰에서도 동작한다.

`@expo/ui/jetpack-compose`의 컴포넌트를 쓰려면
`Host`로 감싸야 한다. `Host`는 Jetpack Compose 뷰의 컨테이너다.[^expo-jc]
가이드의 사용 예에서도 커스텀 뷰를 `Host` 안에 둔다.

### 커스텀 modifier

modifier의 파라미터를 `@OptimizedRecord` 데이터 클래스로 정의하고
`Modifier`를 돌려주는 함수를 만든다.
모듈의 `OnCreate`에서 `ModifierRegistry`에 등록하고 `OnDestroy`에서 해제해,
모듈을 다시 로드할 때 팩토리가 새지 않게 한다.
가이드의 예는 테두리를 그리는 modifier다.

## 트레이드오프

### Compose의 backdrop 효과는 Compose 트리 안에서만 보인다

이 점이 이 주제에서 가장 중요한 한계이고, 이 문서의 판단이다.
Haze나 Kyant Backdrop은 Compose 트리 안의 콘텐츠를 캡처해 효과를 입힌다.
`Host` 안의 Compose 뷰는 React Native 뷰 계층과 별개의 트리이므로,
`Host` 밖의 React Native 뷰가 backdrop이 되는 일반적인 구성에서는
그 효과가 React Native 콘텐츠를 보지 못한다고 이 문서는
추론한다. 가이드는 이 부분을 다루지 않아서 직접 확인한 내용이 아니다.
Expo UI에는 Compose 안에 React Native 뷰를 넣는 `RNHostView`가 있다.[^expo-jc]
그 안의 React Native 뷰가 Compose backdrop
효과의 입력이 되는지는 이 문서가 확인하지 못했다.
뒤 화면과 유리 요소가 모두 같은 `Host` 안의 Compose로 그려지는 화면이라면
이 연결이 의미가 있다.

### 직접 만드는 비용이 든다

Gradle 설정, Compose 컴파일러, `expo-ui` 의존성,
모듈 등록, JS 래퍼, 개발 빌드가 모두 필요하다.
라이브러리 하나로 끝나는 `@sbaiahmed1/react-native-blur`나
`react-native-blur-overlay`보다 구조적으로 훨씬 무겁다.
Compose 쪽 유리 라이브러리를 그대로 쓰고 싶은 팀에게만 의미가 있다.

## 체크리스트

- 뒤 화면과 유리 요소가 같은 Compose 트리 안에 있는가.
- 개발 빌드를 쓰는가(Expo Go 불가).
- 모든 `@expo/ui` 트리와 커스텀 뷰가 `Host` 안에 있는가.
- Compose 의존성 버전(`foundation`, `ui`,
`material3`)을 가이드의 예와 앱의 설정에 맞췄는가.
- 커스텀 modifier를 `OnCreate`에서 등록하고 `OnDestroy`에서 해제했는가.

## 기억할 원칙

### 연결할 수 있다는 것과 효과가 통한다는 것은 다르다

Expo UI는 Compose 컴포넌트를 React Native에 연결해 주지만,
연결된 Compose 효과가 무엇을 볼 수 있는지는 그 컴포넌트가 속한 트리가 정한다.
Liquid Glass는 뒤 화면을 봐야 성립하는 효과여서,
연결하기 전에 뒤 화면이 어느 트리에 있는지부터 확인해야 한다.

---

[^expo-jc]: Expo, [Jetpack Compose - Expo documentation](https://docs.expo.dev/versions/latest/sdk/ui/jetpack-compose/), 날짜 미표기
