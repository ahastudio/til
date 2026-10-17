# Expo와 iOS 27: scene 기반 라이프사이클로 옮기기

## 소개

iOS 27 SDK는 UIKit의 scene 기반 라이프사이클(`UIScene`)을 요구한다.
Xcode 27로 빌드하면서 기존의 application 기반 라이프사이클을 그대로 쓰는 앱은
iOS 27에서 제대로 실행되지 않는다.[^fyi]
React Native 코어는 아직 scene 라이프사이클을 채택하지 않았기 때문에,
Expo가 그 기반을 대신 제공한다.[^fyi]

Expo는 SDK 58부터 scene 라이프사이클을 기본으로 쓴다.
SDK 57은 기본값이 여전히 application 기반이고,
Xcode 27로 빌드하려면
`expo-build-properties`의 `ios.enableSceneSupport`를 직접 켜야 한다.[^fyi]
이 마이그레이션 가이드는 2026년 9월 15일 `expo/fyi` 저장소에 올라왔고,
같은 날 SDK 57에서 옵트인하는 방법이 추가되었다.[^fyi]

## 실제로 벌어진 일

체스 앱 체스메이트를 만드는 Threads 사용자 wooing0306은
2026년 10월 15일 이 문제를 겪은 경험을 전했다.[^wooing0306]
iOS 27에서 앱이 열리지 않는다는 사용자 제보를 받고 원인을 찾아보니,
Expo SDK 57 앱을 Xcode 27로 빌드하면서
`enableSceneSupport`를 켜지 않은 것이 원인이었다.
개발 도중 macOS를 27로 올리면서 Xcode도 함께 27로 업데이트되었는데,
본인도 함께 작업하던 Codex도
이 변화를 대수롭지 않게 넘겼다고 적었다.[^wooing0306-reply]
문제의 버전은 배포된 지 이틀밖에 되지 않았고,
바로 고쳐서 심사를 다시 넣었다고 한다.[^wooing0306-reply]

이 사례가 보여 주는 함정은 세 가지다.

- 빌드는 성공한다. 컴파일 오류나 경고로 드러나지 않는다.
- Xcode 업데이트는 의도하지 않게 일어난다. OS를 올리면 툴체인이 따라 바뀐다.
- 기존 OS에서는 정상 동작하므로, 새 OS 사용자가 제보하기 전까지 모를 수 있다.

wooing0306은 사용자 제보가 없었다면
까맣게 모르고 지나갈 뻔했다고 썼다.[^wooing0306-reply]

## 무엇이 바뀌었나

application 기반 라이프사이클에서는 `AppDelegate`가
`application(_:didFinishLaunchingWithOptions:)`에서 `UIWindow`를 만들고,
URL, user activity, 포그라운드와 백그라운드 콜백을 모두 받았다.[^fyi]

scene 기반에서는 UIKit이 `UIWindowScene`을 만들고 scene delegate를 호출한다.
윈도우는 `scene(_:willConnectTo:options:)`에서 만들어지고,
UIKit은 다음 `UIApplicationDelegate` 메서드를 더는 호출하지 않는다.[^fyi]

| 호출되지 않는 메서드                                                | 영향받는 기능          |
| ------------------------------------------------------------------- | ---------------------- |
| `application(_:open:options:)`                                      | 딥링크, URL 스킴       |
| `application(_:continue:restorationHandler:)`                       | 유니버설 링크, Handoff |
| `applicationDidBecomeActive(_:)` 등 활성·비활성·백그라운드 콜백 4종 | 앱 복귀·이탈 처리      |
| `application(_:performActionFor:completionHandler:)`                | 홈 화면 퀵 액션        |

Expo는 이를 다음처럼 메운다.[^fyi]

- `ExpoAppSceneDelegate`는 `UIWindowSceneDelegate` 기반 클래스다.
  scene이 연결되면 윈도우를 만들고 React Native를 시작한다.
- `AppDelegate`는 `ExpoReactNativeFactoryProvider`를 따르고,
  scene delegate는 여기서 React Native 팩토리를 가져온다.
- `ExpoAppSceneDelegate`는 URL, user activity, 라이프사이클, 퀵 액션 이벤트를
  `ExpoAppDelegate`로 되돌려 보낸다.
  그래서 `AppDelegate` 오버라이드와 `ExpoAppDelegateSubscriber` 구현은 계속 동작한다.
- `npx expo prebuild`는 `SceneDelegate.swift`와
  `Info.plist`의 `UIApplicationSceneManifest`를 생성한다.

## 내 프로젝트는 무엇을 해야 하나

| 상황                                                          | 할 일                                                                  |
| ------------------------------------------------------------- | ---------------------------------------------------------------------- |
| SDK 58, CNG 사용(`ios` 디렉터리 미커밋)                       | 업그레이드 후 `npx expo prebuild --clean`                              |
| SDK 58, `ios` 디렉터리 직접 관리                              | scene delegate, scene manifest, `AppDelegate` 세 곳 수정               |
| Expo 모듈을 쓰는 bare React Native 앱                         | `npx install-expo-modules@latest`                                      |
| SDK 57에 머물면서 Xcode 27로 빌드                             | `ios.enableSceneSupport` 옵트인                                        |
| `UIApplicationDelegate`를 직접 스위즐링하는 코드나 라이브러리 | scene delegate 대응 메서드로 옮기거나 `ExpoAppDelegateSubscriber` 사용 |

기준은 Expo 가이드를 따랐다.[^fyi]
config plugin이 `ExpoAppDelegateSubscriber`를 쓰거나
Expo 모듈 안에 있는 네이티브 코드는
이벤트가 그대로 전달되므로 손댈 필요가 없다.[^fyi]

## SDK 57에서 옵트인하기

`app.json`에 다음을 추가한다.[^fyi]

```json
{
  "expo": {
    "plugins": [
      [
        "expo-build-properties",
        {
          "ios": {
            "enableSceneSupport": true
          }
        }
      ]
    ]
  }
}
```

그다음 네이티브 프로젝트를 다시 만든다.

```bash
# expo@57.0.23 미만이면 플러그인이 예외를 던지므로 먼저 맞춘다
npx expo install --fix

# 로컬 빌드라면 ios 디렉터리를 새로 생성한다
npx expo prebuild --clean

# EAS를 쓴다면 새 빌드를 만든다
eas build --platform ios
```

요구 사항과 동작은 다음과 같다.[^fyi]

- `expo@57.0.23` 이상이 필요하다. scene 런타임이 이 패치에서 SDK 57로 백포트되었다.
- 최신 `expo-build-properties`가 필요하다.
- 켜면 prebuild가 `AppDelegate`를 `ExpoReactNativeFactoryProvider`에 맞추고,
  `didFinishLaunchingWithOptions`의 기존 React Native 시작 코드를 지우고,
  Expo 내장 `EXExpoAppSceneDelegate`를 가리키는 scene manifest를 `Info.plist`에 추가한다.
- SDK 57에서는 `SceneDelegate.swift`를 만들지 않는다.
- `false`로 되돌리면 변경도 되돌아간다.
- SDK 58 이상에서는 아무 효과가 없고, prebuild가 지워도 된다고 경고한다.

Threads 사용자 aitr.endradar도 같은 조건을 짚었다.
`expo@57.0.23` 이상과 최신 `expo-build-properties`가 필요하고,
옵션을 켠 뒤에는 clean prebuild나 새 EAS 빌드까지 해야 하며,
`AppDelegate`를 직접 바꿨다면 수동 적용 조건도 확인해야 한다는 것이다.[^aitr]

## 함정

### 템플릿과 다른 `AppDelegate`는 플러그인이 건드리지 않는다

플러그인은 SDK 57 템플릿 그대로인 `AppDelegate`만 수정한다.
`AppDelegate.swift`가 템플릿과 다르거나
`Info.plist`에 이미 scene manifest가 있으면 덮어쓰기를 거부한다.[^fyi]
이때는 수동 마이그레이션 절차를 따르되,
직접 scene delegate 클래스를 만드는 대신
`UISceneDelegateClassName`을 `EXExpoAppSceneDelegate`로 지정한다.[^fyi]
옵션을 켰다고 안심하지 말고
생성된 `Info.plist`에 scene manifest가 실제로 들어갔는지 확인해야 한다.

### 빌드 성공은 실행 성공이 아니다

scene manifest가 없거나 `UISceneDelegateClassName`이 클래스로 풀리지 않으면
앱은 iOS 27에서 검은 화면으로 뜬다.[^fyi]
컴파일 단계에서는 아무 신호가 없다.
체스메이트 사례도 정확히 이 경우였다.[^wooing0306]

### 딥링크와 복귀 콜백은 따로 확인해야 한다

Threads 사용자 lu.cyai는
빌드가 통과해도 새 OS에서 실제로 열리는지는 따로 확인해야 하고,
링크된 가이드대로 딥링크와 앱 복귀 콜백도 바뀌므로
아이콘으로 실행하기와 종료 상태에서 링크로 열기를
나눠 확인하자고 제안했다.[^lucyai]
가이드의 문제 해결 항목도 같은 지점을 가리킨다.[^fyi]

- 딥링크로 앱은 열리는데 `Linking.getInitialURL()`이 `null`을 돌려준다.
  콜드 스타트 URL 처리는 SDK 58 최신 `expo` 패키지에서 고쳐졌다.
- URL이나 user activity가 두 번 들어온다.
  `AppDelegate` 오버라이드가 `RCTLinkingManager`를 직접 호출하면 Expo의 전달과 겹친다.
  수동 호출을 지운다.
- 퀵 액션이나 Handoff가 동작하지 않는다.
  이 이벤트 전달은 SDK 58 베타 이후에 추가되었다.

### 직접 걸어 둔 `UIApplicationDelegate` 훅은 조용히 멈춘다

`ExpoAppDelegate` 바깥에서
`UIApplicationDelegate`를 스위즐링하거나 상속하는 코드,
예를 들어 UIKit이
`applicationDidBecomeActive(_:)`를 불러 주길 기대하는 라이브러리는
더는 호출되지 않는다.[^fyi]
`sceneDidBecomeActive(_:)` 같은 scene delegate 대응 메서드로 옮기거나
`ExpoAppDelegateSubscriber`로 바꿔야 한다.[^fyi]
오류 없이 기능만 사라지므로 분석 SDK, 푸시, 결제 라이브러리처럼
앱 활성화 시점에 의존하는 코드를 먼저 의심한다.

### 확장과 위젯에는 쓰지 않는다

`ExpoAppSceneDelegate`는 앱 확장과 위젯 타깃에서 쓸 수 없게 표시되어 있다.[^fyi]
`UIScreen.main`과 `UIApplication.shared.keyWindow`도 피하고,
뷰가 속한 scene에서 화면 정보를 읽어야 한다.[^fyi]

## 체크리스트

- 빌드 머신의 Xcode 버전을 확인했는가? (CI와 로컬 모두)
- SDK 57이라면 `expo` 버전이 57.0.23 이상인가?
- `enableSceneSupport`를 켠 뒤 clean prebuild 또는 새 EAS 빌드를 했는가?
- 생성된 `Info.plist`에 `UIApplicationSceneManifest`가 있는가?
- iOS 27 기기나 시뮬레이터에서 아이콘으로 실행해 첫 화면이 뜨는가?
- 앱이 종료된 상태에서 딥링크로 열었을 때 `Linking.getInitialURL()`이 값을 돌려주는가?
- 백그라운드에서 돌아올 때의 콜백, 퀵 액션, Handoff가 동작하는가?
- SDK 58로 올린 뒤 `enableSceneSupport`를 제거했는가?

## 기억할 원칙

### 툴체인 버전도 배포 입력값이다

이번 문제는 코드가 아니라 Xcode 버전이 바뀌면서 생겼다.
같은 소스라도 어떤 SDK로 빌드하느냐에 따라 앱의 실행 방식이 달라진다.
OS 업데이트가 Xcode를 함께 올려 버리는 환경에서는
빌드 도구 버전을 의존성처럼 고정하고
바뀔 때마다 새 OS에서 실행 확인을 하는 편이 안전하다.

### 에이전트도 플랫폼 변화를 모르면 넘긴다

wooing0306은 본인과 Codex 둘 다
이 사실을 몰라 넘어갔다고 했고,[^wooing0306-reply]
무슨 말인지 모르겠으면
Claude나 Codex에게 가이드 링크를 던지라고 권했다.[^wooing0306]
코딩 에이전트는 학습 시점 이후의 플랫폼 변화를 스스로 알지 못한다.
에이전트에게 맡길 때도 최신 마이그레이션 문서를 직접 넣어 주는 것이
확인 절차를 대신하지는 못해도 놓치는 범위를 줄인다.

---

[^fyi]: Expo, [iOS scene-based life cycle in SDK 58](https://github.com/expo/fyi/blob/main/ios-scene-lifecycle.md), 2026-09-15

[^wooing0306]: wooing0306(Threads), [[긴급] Expo SDK 57 앱을 Xcode 27로 빌드하고 있다면 enableSceneSupport를 꼭 켜세요](https://www.threads.com/@wooing0306/post/DefkVQJgtbI), 2026-10-15

[^wooing0306-reply]: wooing0306(Threads), [앱을 개발하던 도중에 macOS를 27로 올리면서 Xcode도 같이 27로 업데이트됐고](https://www.threads.com/@wooing0306/post/DefkYDgAltT), 2026-10-15

[^aitr]: aitr.endradar(Threads), [SDK 57에선 expo 57.0.23 이상과 최신 expo-build-properties가 필요하네](https://www.threads.com/@aitr.endradar/post/Defl7KtkqhT), 2026-10-15

[^lucyai]: lu.cyai(Threads), [빌드가 통과해도 새 OS에서 실제로 열리는지는 별도 확인이 필요하다는 사례네](https://www.threads.com/@lu.cyai/post/DefoADZGKV3), 2026-10-15
