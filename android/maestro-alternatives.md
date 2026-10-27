# Maestro 대신 안드로이드 UI 테스트에 쓸 수 있는 도구와 고르는 기준

<https://developer.android.com/training/testing/ui-automator>

<https://developer.android.com/studio/gemini/journeys>

<https://github.com/appium/appium-uiautomator2-driver>

## 소개

Maestro가 안드로이드에서 답답하다면 그 이유는 도구의 품질보다 구조에 있을
가능성이 크다.
이 문서는 Maestro의 안드로이드 쪽 구조적 한계를 공식 문서와 이슈로 확인하고,
대안으로 꼽을 만한 도구를 같은 기준으로 비교한다.
다루는 도구는 Espresso와 Compose 테스트 API, UI Automator 2.4, Kaspresso,
Appium의 UiAutomator2 드라이버, Android Studio의 Journeys,
그리고 에이전트 계열의 mobile-mcp와 ARTEMIS다.

먼저 밝혀 둘 것이 있다.
모든 면에서 훨씬 좋은 대안은 이 조사에서 찾지 못했다.
도구마다 잘하는 축이 다르고, Maestro가 약한 축에서 강한 도구는 다른 축에서
약하다.
그래서 이 문서의 결론은 하나의 추천이 아니라 상황별 선택표다.
이 문서는 각 도구의 공식 문서와 저장소를 읽고 정리한 것이며, 도구를 직접 설치해
돌려 보지는 못했다.

## Maestro가 안드로이드에서 막히는 지점

Maestro는 앱 밖에서 ADB로 기기를 조종하는 블랙박스 방식이다.
공식 문서는 앱에 테스트 의존성을 넣거나 별도의 테스트 APK를 만들 필요가 없다고
설명한다.
로컬에서는 한 번에 한 기기만 쓰고, 병렬 실행은 Maestro Cloud의 기능으로
안내한다.
앱은 테스트 전에 이미 기기에 설치되어 있다고 가정한다.[^maestro-android]
Compose 앱도 접근성 서비스로 읽으며, 텍스트와 접근성 의미(semantics)를
`testTag`보다 앞세운다.[^maestro-compose]

이 구조에서 오는 한계는 이슈 트래커에서 확인된다.
ADB 명령이나 셸 명령을 흐름 안에서 실행하게 해 달라는 요청은 2024년에 올라와
아직 열려 있다.[^issue-1682]
동작 사이의 지연을 전역으로 줄이는 방법을 묻는 요청도 있었고,[^issue-1528]
키보드를 내리는 동작이 너무 빠르면 뒤로 가기가 눌린다는 보고도 열려
있다.[^issue-1303]
이슈의 존재가 곧 결함의 증거는 아니다.
다만 앱 안의 상태를 건드리거나 동기화를 세밀하게 제어해야 하는 일이 블랙박스
구조와 부딪힌다는 점은 보인다.
이는 이 문서의 해석이다.

정리하면 Maestro가 안드로이드에서 못 하는 것은 세 가지로 모인다.
앱 프로세스 안의 상태를 알고 기다리는 동기화, 테스트 코드에서 앱과 기기를
프로그램으로 다루는 일,
로컬에서의 병렬 실행이다.
대안을 고를 때는 이 셋 가운데 무엇이 지금 가장 아픈지부터 정해야 한다.

## 후보 비교

| 도구                     | 실행 위치                  | 작성 방식            | 강점                                      | 약점                                    |
| ------------------------ | -------------------------- | -------------------- | ----------------------------------------- | --------------------------------------- |
| Espresso, Compose 테스트 | 앱 프로세스 안             | Kotlin, Java         | 앱이 쉬는 시점을 알아 기다림이 필요 없다  | 앱 소스와 빌드 구성에 의존한다          |
| UI Automator 2.4         | 앱 밖(계측 테스트)         | Kotlin DSL           | 난독화된 릴리스 빌드, 다른 앱과 시스템 UI | 2.4 API가 알파이고 개발 중이다          |
| Kaspresso                | Espresso와 UI Automator 위 | Kotlin DSL           | 불안정성 방어, 리포트, Allure, ADB 지원   | 외부 라이브러리이며 두 계층에 얹혀 있다 |
| Appium UiAutomator2      | 서버와 기기 위 서버        | 여러 언어 클라이언트 | 언어 선택, 웹뷰, 병렬 세션                | 서버와 Java, SDK 구성이 무겁다          |
| Journeys                 | Android Studio와 Gemini    | 자연어 XML           | 문장으로 쓰고 화면 변화에 덜 깨진다       | 일부 제스처와 조건문이 미지원, 비결정적 |
| mobile-mcp, ARTEMIS      | 에이전트가 ADB로           | 자연어 지시          | 탐색과 재현에 강하고 스크립트가 필요 없다 | 반복 실행의 재현성이 모델에 달려 있다   |

## 후보별 쓰임새

### Espresso와 Compose 테스트: 앱이 쉴 때까지 알아서 기다린다

Espresso는 공식 문서가 대기, 동기화, sleep, 폴링을 두지 않아도 된다고 소개한다.
UI가 쉬는 상태일 때 조작하고 검증하기 때문이다.
문서는 이 도구가 자동화 테스트를 개발 주기의 일부로 믿는 개발자를 겨냥하며,
블랙박스 테스트에도 쓸 수 있지만 앱 내부를 아는 사람이 가장 큰 힘을 낸다고
말한다.[^espresso]

Compose 앱은 별도의 테스트 규칙을 쓴다.
의미(semantics)로 노드를 찾고, 동기화와 시간 조작을 지원하며,
View와 Compose가 섞인 앱에서도 같은 테스트가 돌아간다.[^compose]

```kotlin
class MyComposeTest {
    @get:Rule val composeTestRule = createComposeRule()

    @Test
    fun myTest() {
        composeTestRule.setContent {
            MyAppTheme { MainScreen(uiState = fakeUiState) }
        }
        composeTestRule.onNodeWithText("Continue").performClick()
        composeTestRule.onNodeWithText("Welcome").assertIsDisplayed()
    }
}
```

Maestro에서 가장 아픈 것이 동기화라면 이쪽이 가장 직접적인 해법이다.
대가는 테스트가 앱 코드 옆에 살고 빌드에 묶인다는 점이다.

### UI Automator 2.4: 앱 밖에서 코드로 조종한다

UI Automator는 앱 프로세스 바깥에서 테스트하므로 난독화(minification)를 적용한
릴리스 빌드도 시험할 수 있다.
2.4에서 Kotlin 친화적인 DSL이 들어왔고, 문서는 신규 개발에 이 방식을 강하게
권한다.
다만 문서가 적은 의존성은 `2.4.0-alpha05`이고 API는 개발 중이라고
밝힌다.[^uia-note]

```kotlin
uiAutomator {
    startApp("com.example.targetapp")
    watchFor(PermissionDialog) { clickAllow() }
    onElement { textAsString() == "Request Permissions" }.click()
    onElement { viewIdResourceName == "result" }.waitForStable()
}
```

`onElement`는 기본 10초 타임아웃을 갖고 있어 조건부 대기가 내장되어 있다.
`watchFor`는 권한 대화상자 같은 예기치 않은 UI를 처리하고,
`clearAppData`로 앱 상태를 초기화하며,
접근성 윈도 노드로 멀티 윈도를 다루고, 스크린샷과 `ResultsReporter`도 내장한다.
Maestro와 같은 블랙박스 위치에 서면서 코드로 쓸 수 있다는 점이 가장 가까운
대안인 이유다.
알파 API라서 버전이 오를 때 깨질 수 있다는 점은 감수해야 한다.

### Kaspresso: 위 둘을 합쳐 쓰기 편하게 만든 래퍼

Kaspresso는 Espresso와 UI Automator를 바탕으로
불안정성 방어, Compose 지원, 스크린샷 테스트, Kotlin DSL, 상세한 로그와 리포트,
ADB 지원, Allure 연동, Robolectric 지원을 얹은 프레임워크다.
저장소는 UI Automator 명령 일부가 10배 빠르다고 주장한다.[^kaspresso]
이 속도 주장은 저장소의 설명이며 이 문서가 재현하지 못했다.
Espresso에서 옮기기 쉽다고 하므로, 이미 Espresso를 쓰는 팀이 불안정성과 보고서를
보강하는 길로 적합하다.

### Appium UiAutomator2 드라이버: 언어와 인프라를 고를 수 있다

드라이버는 대부분의 명령을 UiAutomator2 서버로 넘기고 서버는 Google의
UiAutomator를 쓴다.
네이티브, 하이브리드, 모바일 웹 앱을 에뮬레이터와 실기기에서 자동화한다.
5.0.0부터는 Appium 3과만 호환되고, 6.0.0부터는 안드로이드 8(API 26) 이상이
필요하다.
세션마다 `systemPort`를 다르게 주면 병렬 테스트가 되고, 웹뷰는 크롬드라이버로
다룬다.
Java JDK와 안드로이드 SDK 도구 설정이 필요하다.

```json
{
  "platformName": "Android",
  "appium:automationName": "UiAutomator2",
  "appium:udid": "emulator-5554",
  "appium:app": "/path/to/app-debug.apk",
  "appium:systemPort": 8201
}
```

Maestro의 로컬 병렬 제한이나 언어 제약이 문제라면 후보가 된다.
대신 서버, 드라이버, JDK, SDK를 맞추는 초기 비용과 동기화를 직접 챙기는 비용이
든다.

### Journeys: 문장으로 쓰는 Google의 공식 AI 테스트

Journeys는 Gemini의 시각과 추론으로 자연어 지시를 앱 조작으로 바꾼다.
Studio Labs 기능으로 Android Studio Otter 3 Feature Drop(2025.2.3)부터 쓸 수
있고,
**New > Journey Test**로 XML 파일을 만들어 각 단계를 문장으로 적는다.
문서는 Gemini가 어떤 조작이 목표를 충족할지 추론하므로
레이아웃이 조금 바뀌어도 덜 깨진다고 설명한다.

실행에는 조건이 있다.
프로젝트가 Android Gradle Plugin 9.0.0 이상이어야 하고,
그럴 수 없으면 `JOURNEYS_CUSTOM_APP_ID` 환경 변수로 기기에 설치된 앱을 대상으로
돌린다.
Gemini에 로그인해야 하며, 명령줄 실행은 Android CLI를 쓴다.
문서가 지원하지 않거나 불안정하다고 적은 것은
멀티 핑거 제스처, 길게 누르기, 더블 탭, 화면 회전과 폴딩, 기억, 개수 세기,
조건문이다.
결과 화면은 단계마다 Gemini가 본 스크린샷과 추론을 보여 준다.
Gradle 구성 캐시가 켜져 있으면 엉뚱한 Journey가 실행되거나 인증이 어긋날 수
있다는 알려진 문제도 있다.

작성 요령도 문서가 알려 준다.
앱이 이미 전면에 있다고 가정하고 쓰고, 모호하지 않은 문장을 쓰며,
각 단계에 성공 기준을 함께 적는다.
실패 메시지가 나오면 단계를 더 작게 쪼갠다.

### mobile-mcp와 ARTEMIS: 에이전트가 직접 조작한다

mobile-mcp는 에이전트가 iOS와 안드로이드 기기를 접근성 트리로 조작하게 하는 MCP
서버다.
접근성 트리를 먼저 쓰고 필요할 때만 스크린샷과 좌표로 넘어간다.
Claude Code, Codex, Gemini, GitHub Copilot, Antigravity에서 쓸 수 있고
`npx @mobilenext/mobile-mcp@latest install`로 설치한다.[^mobile-mcp]
ARTEMIS는 자연어 지시를 안드로이드 조작으로 바꾸고 계획과 검증 단계를 갖춘
Google의 에이전트로,
이 저장소의 [ARTEMIS 문서](artemis.md)에 사용법을 정리해 두었다.

이 계열은 테스트 스크립트를 쓰지 않고 기능을 탐색하거나 버그를 재현하는 데
강하다.
같은 지시가 매번 같은 조작으로 이어진다는 보장은 모델에 달려 있으므로,
회귀 테스트의 기둥으로 쓰기보다 탐색과 재현에 쓰는 편이 안전하다.
이는 이 문서의 판단이다.

## 상황별로 고르기

| 가장 아픈 문제                                  | 먼저 볼 도구             |
| ----------------------------------------------- | ------------------------ |
| 흐름이 타이밍 때문에 자주 깨진다                | Espresso, Compose 테스트 |
| 릴리스 빌드나 시스템 UI를 코드로 시험해야 한다  | UI Automator 2.4         |
| 이미 Espresso를 쓰고 리포트와 안정성이 필요하다 | Kaspresso                |
| Kotlin 밖의 언어, 웹뷰, 병렬 세션이 필요하다    | Appium UiAutomator2      |
| 문장으로 쓰고 화면 변화에 덜 깨지게 하고 싶다   | Journeys                 |
| 테스트가 아직 없는 기능을 탐색하고 재현한다     | mobile-mcp, ARTEMIS      |

## 트레이드오프

### 앱 안에서 도는 도구는 안정적이지만 앱과 함께 변한다

Espresso와 Compose 테스트는 앱이 쉬는 시점을 알기 때문에 가장 덜 흔들린다.
그러나 테스트가 앱의 빌드 구성과 내부 API에 묶인다.
Compose 구조를 바꾸면 테스트도 바꿔야 하고, 블랙박스로 릴리스 빌드를 시험하는
일은 못 한다.
Maestro가 외부에서 보는 대가로 동기화를 잃었다면 이쪽은 안에서 보는 대가로
자유를 잃는다.
둘 사이에서 UI Automator가 가운데를 차지하지만, 앱 상태를 알지 못하므로 기다림은
접근성 트리의 변화를 보고 추측해야 한다.
문서도 안정성 확인이 앱이 완전히 놀고 있다는 보증은 아니라고 적는다.

### 코드로 쓰면 제어는 늘지만 비개발자가 빠진다

Maestro의 장점은 YAML이 읽기 쉽다는 점이었다.
위 대안들은 대부분 Kotlin 코드라서 기획자나 QA가 직접 고치기 어렵다.
이를 보완하는 길이 Journeys 같은 자연어 도구지만, 이쪽은 비결정성이라는 새
대가를 낸다.
결정성과 쓰기 쉬움은 한꺼번에 얻기 어렵다는 점이 이 비교 전체를 관통한다.
이는 이 문서의 해석이다.

### AI 도구는 쓰기 쉽지만 같은 결과를 약속하지 않는다

Journeys가 인정하듯 같은 문장을 더 작은 단계로 쪼개야 정확해지는 경우가 있고,
모델이 최대 시도 횟수 안에 동작을 끝내지 못하는 실패도 있다.
회귀 테스트는 같은 입력에 같은 판정이 나와야 쓸모가 있는데, 문장 기반 도구는 그
약속을 모델에 맡긴다.
따라서 AI 도구를 고른다면 결정적 테스트를 대체하는 것이 아니라 보완하는 위치에
두는 편이 안전하다.

## 함정

- UI Automator 2.4는 알파다. 의존성 버전을 고정하고, 올릴 때마다 테스트 전체를
다시 돌려야 한다.
- Journeys를 쓰려면 AGP 9.0.0 이상 또는 기기에 설치된 앱 대상 실행이라는 조건이
붙는다. 이미 오래된 AGP를 쓰는 프로젝트는 먼저 이 조건을 확인해야 한다.
- Journeys의 Gradle 구성 캐시 문제는 여러 Journey 파일이 있는 프로젝트에서
엉뚱한 파일이 실행되게 한다. 캐시를 끄는 것이 문서의 해법이다.
- Appium은 병렬 세션마다 `systemPort`와 영상 녹화용 포트를 달리 주어야 포트
충돌을 피한다.
- Kaspresso의 10배 빠르다는 문구는 저장소의 주장이다. 이 문서가 확인하지
못했으므로 자기 앱에서 재야 한다.
- 에이전트 도구에 앱 권한과 계정을 넘길 때는 어떤 모델에 화면이 전달되는지
확인해야 한다. 이 문서는 각 도구의 데이터 처리 방침을 확인하지 못했다.

## 확인하기

도구를 고르기 전에 가장 자주 깨지는 흐름 하나를 정해 같은 흐름을 두 도구로 써
본다.
Maestro로 쓴 흐름과 후보 하나(예를 들어 UI Automator 2.4)로 쓴 흐름을
같은 에뮬레이터에서 각각 스무 번 돌려 실패 횟수와 한 번에 걸리는 시간을
비교한다.
같은 앱 빌드와 같은 에뮬레이터 이미지를 쓰고, 첫 실행의 설치 시간은 제외한다.

## 체크리스트

- 지금 가장 아픈 문제가 동기화, 프로그램 제어, 병렬 실행 가운데 무엇인지
적었는가.
- 후보를 시험할 흐름 하나를 정했고 같은 에뮬레이터 이미지를 쓰는가.
- UI Automator 2.4를 쓴다면 알파 버전을 고정했는가.
- Journeys를 쓴다면 AGP 버전과 Gradle 구성 캐시 설정을 확인했는가.
- Appium을 쓴다면 병렬 세션마다 `systemPort`를 다르게 주었는가.
- 에이전트 도구를 회귀 테스트의 유일한 기둥으로 두지 않았는가.
- 테스트를 누가 고치는지, 개발자인지 비개발자인지 정했는가.

## 기억할 원칙

### 도구를 고르기 전에 무엇이 아픈지를 먼저 이름 붙인다

Maestro의 안드로이드 한계는 블랙박스, ADB, 로컬 단일 기기라는 구조에서 나온다.
이 구조에서 오는 문제는 같은 구조를 쓰는 다른 도구를 골라서는 풀리지 않는다.
동기화가 문제면 앱 안으로, 프로그램 제어가 문제면 코드로, 쓰기 쉬움이 문제면
문장으로 가야 한다.
문제의 이름이 분명하면 대안의 목록은 저절로 줄어든다.

---

[^maestro-android]: Maestro Docs, [Android](https://docs.maestro.dev/platform-support/android)

[^maestro-compose]: Maestro Docs, [Jetpack Compose](https://docs.maestro.dev/platform-support/android-jetpack-compose)

[^issue-1682]: GitHub, [\[Feature Request\] Possibility to run ADB commands / possibility to run shell commands](https://github.com/mobile-dev-inc/maestro/issues/1682), 2024-02-20

[^issue-1528]: GitHub, [\[Feature Request\] how to reduce delay between actions globally?](https://github.com/mobile-dev-inc/maestro/issues/1528), 2023-10-16

[^issue-1303]: GitHub, [\[1.30.4\] Back is pressed instead of keyboard hidden if it's performed too quickly](https://github.com/mobile-dev-inc/maestro/issues/1303), 2023-07-31

[^espresso]: Android Developers, [Espresso](https://developer.android.com/training/testing/espresso)

[^compose]: Android Developers, [Test your Compose layout](https://developer.android.com/develop/ui/compose/testing)

[^uia-note]: Android Developers, [Write automated tests with UI Automator](https://developer.android.com/training/testing/ui-automator)

[^kaspresso]: GitHub, [Kaspresso](https://github.com/KasperskyLab/Kaspresso)

[^mobile-mcp]: GitHub, [mobile-next/mobile-mcp](https://github.com/mobile-next/mobile-mcp)
