# 코치마크: 화면 위에 얹는 사용법 안내를 언제, 어떻게 쓸까

## 소개

코치마크(coach mark)는 앱이나 웹 화면 위에 반투명 레이어를 덮고,
화살표와 짧은 문구로 특정 UI 요소의 쓰임을 알려 주는 안내 장치다.
Nielsen Norman Group(NN/g)은 이를
인스트럭셔널 오버레이(instructional overlay)라고도 부르며,
처음 실행할 때 UI 기능을 드러내는 데 도움이 될 수 있다고 설명한다.[^nng]
비슷한 장치로 툴팁, 제품 투어(guided tour),
기능 발견(feature discovery) 프롬프트가 있고,
플랫폼마다 부르는 이름과 권장하는 형태가 다르다.

| 이름                 | 쓰는 곳                    | 특징                                                            |
| -------------------- | -------------------------- | --------------------------------------------------------------- |
| 코치마크, 오버레이   | 모바일 앱 일반             | 화면 전체를 덮고 여러 요소를 한꺼번에 설명[^nng]                |
| 탭 타깃(tap target)  | Material Design            | 요소 하나를 원형으로 강조, 한 번의 동작만 요청[^m1]             |
| 팝오버 팁, 인라인 팁 | Apple TipKit               | 팝오버는 UI 위에 겹치고, 인라인은 레이아웃 안에 들어감[^tipkit] |
| 리치 툴팁            | Jetpack Compose Material 3 | 제목, 링크, 버튼을 가질 수 있는 툴팁[^compose]                  |
| 제품 투어            | 웹                         | 여러 단계를 순서대로 강조하는 라이브러리 방식                   |

## 동작 방식

### 화면을 덮는 방식과 끼워 넣는 방식

코치마크는 크게 두 형태로 나뉜다.
하나는 화면 위에 레이어를 덮어 아래 UI를 가리는 방식이고,
다른 하나는 설명을 레이아웃 안에 끼워 넣어 아래 UI를 가리지 않는 방식이다.

Apple의 TipKit 샘플은 인라인 `TipView`를 첫 선택으로 권한다.
아래의 UI 요소를 가리지 않기 때문이다.[^tipkit]
팝오버 팁은 레이아웃을 바꾸기 곤란하거나
가려지는 컨트롤과 상호작용할 필요가 없을 때 쓰고,
이미 기능을 가리키고 있으니 이미지는 빼는 것을 고려하라고 한다.[^tipkit]

### 언제 보여 줄지가 설계의 대부분이다

Material Design의 기능 발견 가이드는 앱을 열자마자 보여 주지 말고,
사용자가 맥락을 가진 뒤에 보여 주라고 한다.[^m1]
예를 들어 이미지를 추가한 다음에 자르기 기능을 알려 주는 식이다.
메시지를 다 읽은 직후 같은 자연스러운 멈춤도 적절한 시점으로 꼽는다.[^m1]
대상도 가린다.
아직 써 보지 않은 기능을 그 기능을 쓰지 않은 사람에게만 보여 주고,
가벼운 사용자에게 고급 기능을 보여 주지 않는다.[^m1]
빈도는 세션당 하나로 제한하고,
사용자가 닫으면 비슷한 안내는 더 오래 기다렸다가 보여 주며,
받아들이면 관련 안내를 더 빨리 보여 줘도 된다고 한다.[^m1]

TipKit은 이 판단을 코드의 규칙으로 표현한다.
앱 상태는 `@Parameter`, 사용자 행동은 `Event`로 추적하고,
`#Rule` 매크로로 조건을 적으면 여러 규칙은 AND로 결합된다.[^tipkit]
`MaxDisplayCount(1)` 같은 옵션으로 표시 횟수를 제한하고,
사용자가 기능을 쓰면 `invalidate(reason: .actionPerformed)`로
팁을 무효화한다.[^tipkit]
사용자가 닫은 팁은 데이터 저장소를
초기화하기 전까지 다시 나타나지 않는다.[^tipkit]

### 기억에 기대는 구조라는 한계

NN/g는 코치마크의 근본 문제를 기억에서 찾는다.[^nng]
사용자는 오버레이를 읽으면서 동시에 앱을 쓸 수 없으므로,
안내를 외운 뒤 오버레이가 사라진 다음에 적용해야 한다.
단기 기억은 많은 정보를 담지 못하고 약 20초 안에 흐려진다.[^nng]
그래서 UI 전체를 설명하기보다 상호작용 하나에 집중하고,
안내를 하나씩 맥락에 맞는 순간에 보여 주라고 권한다.[^nng]

## 구현하기

### iOS: TipKit

TipKit은 iOS 17부터 쓸 수 있다.[^tipkit-doc]
앱 세션마다 한 번 `Tips.configure()`를 호출해 팁을 불러오고,
`Tip` 프로토콜을 따르는 구조체로 내용을 정의한다.[^tipkit]

```swift
import SwiftUI
import TipKit

struct FavoriteTip: Tip {
    var title: Text { Text("즐겨찾기에 저장") }
    var message: Text? { Text("즐겨찾기한 항목은 목록 맨 위에 표시됩니다.") }

    // 상세 화면을 세 번 이상 연 사람에게만 보여 준다.
    static let viewedDetail = Event(id: "viewedDetail")

    var rules: [Rule] {
        #Rule(Self.viewedDetail) { $0.donations.count >= 3 }
    }

    // 한 번 보여 주면 다시 띄우지 않는다.
    var options: [Option] { MaxDisplayCount(1) }
}

struct DetailView: View {
    let tip = FavoriteTip()

    var body: some View {
        VStack {
            // 인라인 팁: 아래 UI를 가리지 않는다.
            TipView(tip, arrowEdge: .bottom)
            Button {
                // 기능을 쓰면 더 이상 안내할 필요가 없다.
                tip.invalidate(reason: .actionPerformed)
            } label: {
                Label("즐겨찾기", systemImage: "star")
            }
        }
        .onAppear { FavoriteTip.viewedDetail.sendDonation() }
    }
}

@main
struct ExampleApp: App {
    init() {
        try? Tips.configure()
    }

    var body: some Scene {
        WindowGroup { DetailView() }
    }
}
```

개발 중에는 `Tips.showAllTipsForTesting()`,
`Tips.resetDatastore()` 같은 테스트용 API로
표시 조건을 무시하고 팁을 확인할 수 있다.[^tipkit]

### Android: Compose 툴팁과 TapTargetView

Jetpack Compose Material 3는 `TooltipBox`에
`PlainTooltip`이나 `RichTooltip`을 넣어 툴팁을 만든다.[^compose]
`RichTooltip`은 제목, 링크, 버튼을 가질 수 있고,
`rememberTooltipState()`로 만든 상태의 `show()`와
`dismiss()`로 코드에서 열고 닫는다.[^compose]
Material의 탭 타깃을 그대로 구현한 라이브러리로는
KeepSafe의 TapTargetView가 있다(Apache-2.0).[^taptargetview]
다만 이 저장소의 마지막 푸시는 2024년 10월이다.[^taptargetview]

### 웹: 제품 투어 라이브러리

| 라이브러리    | 라이선스                      | GitHub 스타 | 비고                                         |
| ------------- | ----------------------------- | ----------- | -------------------------------------------- |
| driver.js     | MIT[^driverjs-repo]           | 약 2.7만    | 의존성 없는 경량 라이브러리[^driverjs-repo]  |
| Intro.js      | AGPLv3 또는 상용[^introjs]    | 약 2.3만    | 상업 프로젝트는 상용 라이선스 필요[^introjs] |
| Shepherd.js   | AGPL-3.0 또는 상용[^shepherd] | 약 1.4만    | 상업적 사용은 상용 라이선스[^shepherd]       |
| React Joyride | MIT[^joyride]                 | 약 7,900    | React 전용[^joyride]                         |

라이선스가 선택을 가른다.
Intro.js는 v2.0.0부터 상업 프로젝트에 상용 라이선스를 요구하고,[^introjs]
Shepherd.js도 AGPL-3.0과 상용 라이선스의 이중 라이선스다.[^shepherd]
사내 제품이나 유료 서비스라면
MIT인 driver.js나 React Joyride가 법무 검토 부담이 적다.

driver.js의 가장 짧은 사용 예는 다음과 같다.[^driverjs-docs]

```javascript
import { driver } from "driver.js";
import "driver.js/dist/driver.css";

const driverObj = driver();
driverObj.highlight({
  element: "#some-element",
  popover: {
    title: "Title",
    description: "Description",
  },
});
```

## 트레이드오프

### 한꺼번에 설명할수록 덜 읽힌다

첫 실행에 모든 기능을 덮는 오버레이는 만들기 쉽고 한 번에 끝난다.
하지만 NN/g는 연속된 팁이 사용자가 안내를 더 빨리 닫게 만들고,
앱을 지나치게 복잡하고 어려워 보이게 한다고 지적한다.[^nng]
반대로 맥락에 맞춰 하나씩 보여 주려면
언제 어떤 팁을 띄울지 추적하는 상태와 규칙이 필요하다.
TipKit이 `Event`와 `#Rule`을 제공하는 이유가 여기에 있다.[^tipkit]
쉬운 구현과 읽히는 안내 사이에서 하나를 고르는 문제다.

### 가리면 눈에 띄고, 끼워 넣으면 덜 방해한다

화면을 덮는 오버레이와 팝오버는 확실히 눈에 띄지만
사용자가 하려던 일을 막는다.
인라인 팁은 흐름을 막지 않지만 레이아웃을 바꾸고 쉽게 지나친다.[^tipkit]
Material의 탭 타깃은 그 중간으로,
요소 하나만 강조하고 바깥을 탭하거나 스와이프하면 닫힌다.[^m1]

### 효과에 대한 근거는 아직 얇다

Noriega 등은 2020년 연구에서 오버레이를 쓴 집단과 쓰지 않은 집단을 비교해
작업 완료 시간이 줄어드는 경향을 봤지만,
표본이 작아 통계적으로 확인하려면 더 큰 연구가 필요하다고 밝혔다.[^noriega]
코치마크를 넣을지 말지는 일반론보다
자기 제품에서 측정한 결과로 정해야 한다.

## 함정

- **UI와 똑같이 그리기**:
  안내가 실제 버튼처럼 보이면 사용자는 무엇을 누를 수 있는지 헷갈린다.
  NN/g는 손글씨풍 글꼴처럼 UI와 구분되는 표현을 권한다.[^nng]
- **시작 화면에 몰아넣기**:
  앱을 연 직후는 사용자가 맥락이 없는 시점이다.[^m1]
- **닫은 안내를 다시 띄우기**:
  닫았다는 것은 지금 필요 없다는 신호다.
  Material은 닫은 경우 더 오래 기다리라고 한다.[^m1]
- **기능을 쓴 뒤에도 남겨 두기**:
  TipKit 샘플처럼 기능을 쓰면 안내를 무효화해야 한다.[^tipkit]
- **접근성 무시**:
  화면을 덮는 오버레이는 사실상 모달 대화 상자다.
  WAI-ARIA 모달 패턴은 열릴 때 포커스를 안으로 옮기고, Tab이 안에서만 돌며,
  Escape로 닫히고, 닫히면 포커스를 연 요소로 돌려주라고 한다.[^apg]
  바깥과의 상호작용을 막고 시각적으로도 가릴 때만 `aria-modal="true"`를 쓰라고 경고한다.[^apg]
- **라이선스 확인 누락**:
  Intro.js와 Shepherd.js를 상업 제품에 그냥 넣으면 라이선스 위반이 될 수 있다.[^introjs][^shepherd]

## 체크리스트

- 안내 하나가 상호작용 하나만 설명하는가?
- 앱을 연 직후가 아니라 관련 행동 뒤에 나타나는가?
- 해당 기능을 이미 쓴 사람에게는 나타나지 않는가?
- 세션당 표시 개수와 전체 표시 횟수가 제한되어 있는가?
- 닫은 안내가 곧바로 다시 나타나지 않는가?
- 안내가 실제 UI와 시각적으로 구분되는가?
- 오버레이를 키보드로 닫을 수 있고, 닫은 뒤 포커스가 원래 자리로 돌아오는가?
- 사용하는 라이브러리의 라이선스가 제품의 배포 형태와 맞는가?
- 안내가 있을 때와 없을 때의 완료율이나 완료 시간을 측정하고 있는가?

## 기억할 원칙

### 안내가 필요하다는 것은 UI가 스스로 설명하지 못한다는 신호다

코치마크는 UI가 전달하지 못한 것을 덧붙이는 장치다.
NN/g가 지적한 대로 사용자는 매뉴얼을 읽으려고 앱을 여는 것이 아니라
가능한 한 적은 노력으로 일을 끝내려고 연다.[^nng]
안내를 늘리기 전에 그 기능이 왜 스스로 드러나지 않는지를 먼저 물어야 한다.

### 무엇을 말할지보다 언제 말할지가 더 중요하다

같은 문구도 맥락이 생긴 순간에는 읽히고, 첫 화면에서는 건너뛰어진다.
Material과 TipKit이 모두 표시 시점과 빈도를 설계의 중심에 둔 것은
코치마크의 성패가 내용보다 시점에 달려 있기 때문이다.[^m1][^tipkit]

## 효과를 확인하는 실험

코치마크의 효과는 표시 횟수나 닫기 비율로 판단하지 않는다.
안내가 해결하려는 작업을 먼저 정하고,
안내를 본 집단과 보지 않은 집단에서
완료율, 완료 시간, 오류, 도움말 요청을 비교한다.
가능하면 신규 사용자와 기존 사용자를 나누어
이미 알고 있는 기능을 다시 설명하는 비용도 확인한다.

실험에는 방해 비용도 포함한다.
안내를 닫은 뒤 원래 작업을 계속했는지,
같은 기능의 안내가 반복 노출되었는지,
키보드와 보조 기술로 흐름을 끝까지 완료할 수 있는지 기록한다.
완료율이 올라도 작업 시간이 늘거나
취소와 이탈이 많아지면 성공으로 볼 수 없다.

효과가 확인되지 않으면 문구부터 고치기보다
기능의 발견 가능성, 화면의 정보 구조,
표시 시점이 문제인지 따로 시험한다.
안내가 UI의 불명확성을 가리는 임시방편이 되지 않도록
코치마크를 제거한 뒤에도 작업이 가능한지 함께 확인한다.

---

[^nng]: Nielsen Norman Group, [Instructional Overlays and Coach Marks for Mobile Apps](https://www.nngroup.com/articles/mobile-instructional-overlay/), 2014-02-16

[^m1]: Material Design, [Feature discovery](https://m1.material.io/growth-communications/feature-discovery.html), 게재일 미표기

[^tipkit]: Apple Developer, [Highlighting app features with TipKit](https://developer.apple.com/documentation/tipkit/highlightingappfeatureswithtipkit), 게재일 미표기

[^tipkit-doc]: Apple Developer, [TipKit](https://developer.apple.com/documentation/tipkit), 게재일 미표기

[^compose]: Android Developers, [Tooltip](https://developer.android.com/develop/ui/compose/components/tooltip), 2026-10-01 갱신

[^taptargetview]: GitHub, [KeepSafe/TapTargetView](https://github.com/KeepSafe/TapTargetView), 게재일 미표기

[^driverjs-repo]: GitHub, [nilbuild/driver.js](https://github.com/nilbuild/driver.js), 게재일 미표기

[^driverjs-docs]: driver.js, [Installation](https://driverjs.com/docs/installation), 게재일 미표기

[^introjs]: GitHub, [usablica/intro.js](https://github.com/usablica/intro.js), 게재일 미표기

[^shepherd]: GitHub, [Shepherd.js License](https://github.com/shipshapecode/shepherd/blob/main/LICENSE.md), 게재일 미표기

[^joyride]: GitHub, [gilbarbara/react-joyride](https://github.com/gilbarbara/react-joyride), 게재일 미표기

[^noriega]: Springer, [Effectiveness of Coach Marks or Instructional Overlay in Smartphone Apps Interfaces](https://www.springerprofessional.de/en/effectiveness-of-coach-marks-or-instructional-overlay-in-smartph/16768770), 2020

[^apg]: W3C WAI, [Dialog (Modal) Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/), 게재일 미표기
