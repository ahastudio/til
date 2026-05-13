# React Native Bottom Sheet

<https://gorhom.dev/react-native-bottom-sheet/>

<https://github.com/gorhom/react-native-bottom-sheet>

## 소개

Mo Gorhom이 만든 React Native용 고성능 인터랙티브 바텀 시트(Bottom Sheet)
컴포넌트 라이브러리다. GitHub 스타 8.9k, 릴리즈 128회의 활발히 유지보수되는
오픈소스 프로젝트로, MIT 라이선스로 공개되어 있다.

`react-native-reanimated`(v3)와 `react-native-gesture-handler`(v2)를 필수
의존성으로 사용한다. 현재 v5가 최신 버전이며, TypeScript로 작성되어 있다.

주요 기능은 다음과 같다.

- **Snap Points**: 바텀 시트가 멈추는 위치를 퍼센트·픽셀로 선언
- **Dynamic Sizing**: 콘텐츠 크기에 따라 높이 자동 조절
- **Bottom Sheet Modal**: 모달 방식의 바텀 시트 표현
- **스크롤 가능한 콘텐츠**: FlatList, SectionList, ScrollView, FlashList 호환
- **키보드 처리**: iOS와 Android 양쪽에서 키보드 인터랙션 seamless 처리
- **Pull-to-refresh**: 스크롤 요소 내 당겨서 새로고침 지원
- **React Navigation 통합** 및 웹(React Native Web) 지원
- 접근성(Accessibility) 지원

## 분석

### Reanimated + Gesture Handler 조합의 아키텍처적 의미

바텀 시트의 핵심 기술 과제는 “60fps 제스처 응답”이다. React Native의 기본
아키텍처에서 JavaScript는 별도 스레드에서 실행되며, UI 업데이트는 브릿지를
통해 네이티브 스레드로 전달된다. 브릿지의 비동기 특성상, 고속 제스처
드래그를 JS 스레드에서 처리하면 애니메이션이 뚝뚝 끊기는 jank가 발생한다.

`react-native-reanimated`는 애니메이션 로직을 JS 스레드가 아닌 UI 스레드에서
직접 실행하는 worklet 시스템을 제공한다. `react-native-gesture-handler`도
제스처 인식을 네이티브 레이어에서 처리해 브릿지 왕복 없이 즉각적인 응답을
가능하게 한다. 이 두 라이브러리의 조합이 “performant”라는 핵심 특징을 기술적으로
뒷받침한다.

### Snap Points의 선언적 설계

`snapPoints` 배열에 `['25%', '50%', '90%']`처럼 위치를 선언하면 컴포넌트가
스스로 스냅 애니메이션을 관리한다. 사용자가 드래그를 놓으면 가장 가까운 스냅
포인트로 자동으로 이동한다. 이 설계는 필요한 위치만 선언하고 동작 방식은
라이브러리에 위임하는 선언적 패러다임이다.

명령형 제어가 필요한 경우에는 `ref`를 통해 `snapToIndex()`,
`snapToPosition()`, `expand()`, `collapse()`, `close()` 메서드를 직접 호출할
수 있다. 선언적 기본값 위에 명령형 이탈구를 제공해, 단순한 사용 사례는
쉽게 시작하고 복잡한 요구에도 대응할 수 있다.

### Dynamic Sizing와 콘텐츠 주도 레이아웃

`enableDynamicSizing` 옵션은 `snapPoints` 없이 콘텐츠 높이에 따라 바텀 시트
크기가 자동 결정되게 한다. 고정 스냅 포인트를 사전에 알기 어려운 경우 —
예를 들어 API에서 받아온 목록이나 폼 입력 결과에 따라 크기가 달라지는
시나리오 — 에서 유용하다. `BottomSheetView`와 함께 사용하면 콘텐츠가
렌더링된 후 정확한 높이를 측정해 시트 크기를 결정한다.

### FlashList 호환성

Shopify가 공개한 `FlashList`는 `FlatList`의 성능 개선 대체재다. 바텀 시트에
긴 목록을 넣는 것은 흔한 패턴이지만, 스크롤과 바텀 시트 드래그 제스처가
충돌하는 문제가 발생할 수 있다. `BottomSheetFlashList` 래퍼가 이 충돌을
내부적으로 해결해 사용자는 일반 `FlashList` 쓰듯 그냥 쓸 수 있다.

## 비평

### 긍정적 측면

성능에 직결되는 두 의존성(Reanimated, Gesture Handler)을 직접 구현하지 않고
각 분야의 표준 라이브러리에 위임한 설계가 올바르다. 애니메이션과 제스처
처리의 복잡성은 해당 라이브러리 전문가가 관리하고, 이 라이브러리는 바텀 시트
동작 조합에만 집중한다. 책임이 명확히 분리되어 있다.

TypeScript 우선 구현으로 타입 안전성을 제공하며, 다양한 스크롤 컴포넌트
래퍼(`BottomSheetFlatList`, `BottomSheetScrollView`, `BottomSheetFlashList` 등)를
제공해 기존 코드에서 import만 교체하면 되는 마이그레이션 경험을 만든다.

### 한계

Reanimated와 Gesture Handler 두 개의 네이티브 모듈이 필수 의존성이다. 둘 다
네이티브 코드를 포함하므로 Expo Managed Workflow에서는 추가 설정이 필요하고,
버전 호환성 관리가 복잡해질 수 있다. v5에서 Reanimated v3와 Gesture Handler
v2로 올라가면서 이전 버전과의 하위 호환성이 끊겼다는 점도 고려해야 한다.

웹(React Native Web) 지원이 있지만, 웹에서의 제스처 경험은 네이티브 앱과
다를 수 있다. 터치와 마우스 이벤트 처리 방식이 달라 크로스 플랫폼 앱에서
세밀한 테스트가 필요하다.

## 인사이트

### React Native 성능의 구조적 한계를 라이브러리 레이어에서 해결하는 패턴

React Native는 “JavaScript를 한 번 작성해 iOS와 Android에서 실행한다”는 약속을
내걸지만, 성능에 민감한 인터랙션에서는 이 추상화가 부담이 된다. JS 스레드와
네이티브 UI 스레드 사이의 브릿지는 고주파 업데이트에서 병목이 된다. 이 문제는
React Native 아키텍처 자체의 제약이며, 개별 앱 개발자가 해결하기 어렵다.

`react-native-bottom-sheet`가 선택한 해법은 “문제를 우회하는 레이어를 제공하는
라이브러리”다. Reanimated worklet이 UI 스레드에서 직접 실행되므로 브릿지 왕복이
없고, Gesture Handler가 네이티브에서 제스처를 처리해 JS 스레드 부담을 제거한다.
애플리케이션 개발자는 이 복잡성을 신경 쓰지 않아도 된다.

이 패턴은 React Native 생태계의 반복되는 해결 방식이다. 플랫폼이 제공하지
못하는 성능을 라이브러리가 해결하고, 라이브러리를 조합해 프레임워크에 가까운
경험을 만든다. React Native 자체가 “새로운 아키텍처(JSI, Fabric)”로 이 한계를
구조적으로 해결하려 하고 있지만, 그 이전까지는 이런 라이브러리 레이어의 우회가
프로덕션 가능한 유일한 경로다.

### 바텀 시트가 모바일 UX의 기본 패턴이 된 이유

바텀 시트는 iOS의 “액션 시트(Action Sheet)”에서 진화해 이제 독립적인 UX
패턴으로 자리 잡았다. Google Maps, Apple Maps, Uber, Airbnb의 지도 UI에서
볼 수 있듯이, 바텀 시트는 지도나 주요 콘텐츠를 가리지 않으면서 추가 정보와
인터랙션을 제공하는 레이어다. “전체 화면을 차지하지 않는 모달”이라는 정의가
이 패턴의 핵심이다.

모바일에서 한 손 사용이 기본이 되면서 화면 하단이 엄지손가락 도달 범위에
들어온다. 바텀 시트는 이 인체공학적 현실과 일치한다. 위에서 내려오는 모달과
달리, 아래에서 올라오는 시트는 엄지로 제어하기 쉽다. iOS Human Interface
Guidelines와 Material Design 모두 이 패턴을 공식적으로 권장하면서 사용자
기대치도 형성됐다.

앱의 정보 구조가 복잡해질수록 바텀 시트의 역할도 커졌다. 필터, 정렬, 공유,
결제 등 “현재 화면에서 파생된 일시적 작업”을 위한 범용 컨테이너가 되었다.
`react-native-bottom-sheet`가 8.9k 스타를 받은 것은 이 패턴의 구현 난이도가
높고, 잘 구현된 솔루션에 대한 수요가 크다는 방증이다.

### 선언적 기본값과 명령형 탈출구의 균형

현대 프론트엔드 프레임워크는 선언적 패러다임을 기본으로 한다. 상태가 어떤
값이면 UI가 어떤 모습이어야 한다고 선언하고, 프레임워크가 변환을 관리한다.
이 접근은 코드를 단순하게 만들지만, 모든 인터랙션을 상태 변화로 표현하기
어려운 경우가 있다.

`react-native-bottom-sheet`는 이 긴장을 `snapPoints` + `ref` 조합으로 해소한다.
`snapPoints`는 선언적이다. “이 세 위치 중 하나에 있어야 한다”는 제약을 선언하면
컴포넌트가 알아서 관리한다. 반면 버튼 클릭으로 특정 위치로 즉시 이동해야 할 때는
`ref.current.snapToIndex(1)` 같은 명령형 호출이 필요하다. 두 방식을 하나의
컴포넌트에서 동시에 지원하는 것이 API 설계의 핵심 결정이다.

이 패턴은 React의 `ref` 사용 철학과 일치한다. “제어 흐름상 자연스럽지 않은”
명령형 제어가 필요할 때만 `ref`를 쓰고, 기본은 선언적으로 유지하는 것이다.
라이브러리 API 설계의 관점에서, 선언적 인터페이스로 단순한 사용 사례를 쉽게
시작하게 하고, 명령형 탈출구로 복잡한 요구를 처리하는 구조는 좋은 API가
갖춰야 할 표준 패턴이다. 쉬운 것은 쉽고, 어려운 것은 가능하다.
