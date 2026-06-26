# flutter_figma_motion

<https://github.com/bear2u/flutter_figma_motion>

## 소개

flutter_figma_motion은 Figma의 Motion Dev Mode JSON을 Flutter 위젯에 적용하는 패키지다.
Figma에서 정의한 애니메이션 트랙을 JSON으로 내보낸 뒤,
이미 구현된 Flutter 위젯에 해당 트랙을 씌우는 방식으로 동작한다.

지원하는 애니메이션 속성은 이동(`motionTranslationX/Y`), 스케일(`motionScaleX/Y`),
회전(`motionRotation`), 불투명도(`opacity`)이며,
큐빅 베지어 이징과 루프 재생을 지원한다.
MIT 라이선스로 공개된 초기 버전(0.0.1)이다.

## 사용법

### 기본 구조

`FigmaMotionAsset`으로 JSON을 로드하고, `FigmaMotionScene`으로 공유 타임라인을 만들고,
`FigmaMotionWidget`으로 각 위젯에 Figma 노드 ID를 연결한다.

```dart
FigmaMotionAsset(
  asset: 'assets/motions/workout_onboarding_motion.json',
  builder: (context, motion) {
    return FigmaMotionScene(
      motion: motion,
      builder: (context, motion, controller) {
        return Stack(
          children: [
            FigmaMotionWidget(
              motion: motion,
              nodeId: '7:18',
              controller: controller,
              child: const OnboardingCard(),
            ),
            FigmaMotionWidget(
              motion: motion,
              nodeId: '7:20',
              controller: controller,
              child: const OnboardingTitle(),
            ),
          ],
        );
      },
    );
  },
)
```

### JSON 직접 파싱

```dart
final motion = FigmaMotion.fromJsonString(jsonString);
final motion = FigmaMotion.fromJson(jsonMap);
```

## 지원 필드

| Figma JSON 필드       | Flutter 매핑                    |
| --------------------- | ------------------------------- |
| `motionTranslationX`  | `Transform.translate(dx: ...)`  |
| `motionTranslationY`  | `Transform.translate(dy: ...)`  |
| `motionScaleX`        | `Transform.scale(scaleX: ...)`  |
| `motionScaleY`        | `Transform.scale(scaleY: ...)`  |
| `motionRotation`      | `Transform.rotate(angle: ...)`  |
| `opacity`             | `Opacity(opacity: ...)`         |

**미지원**: 색상, 너비/높이, 블러, 섀도우, 경로 트림, 셰이더 속성 애니메이션.
자동 Flutter UI 생성도 지원하지 않는다.

## 주요 API

| 클래스             | 역할                                     |
| ------------------ | ---------------------------------------- |
| `FigmaMotion`      | 파싱된 JSON 표현                         |
| `FigmaMotionAsset` | JSON 자산 로더                           |
| `FigmaMotionScene` | 공유 `AnimationController` 생성          |
| `FigmaMotionWidget`| 개별 노드에 애니메이션 트랙 적용         |

## 분석

### 디자이너-개발자 협업 파이프라인의 마지막 구간을 채운다

Figma Motion Dev Mode는 디자이너가 정의한 애니메이션을 JSON으로 내보내는 기능이다.
이 JSON을 개발자가 직접 파싱해 Flutter 위젯에 적용하려면 상당한 구현 비용이 든다.
flutter_figma_motion은 이 구간을 라이브러리로 추상화한다.

디자이너가 Figma에서 애니메이션을 수정하면 JSON이 바뀌고,
개발자는 코드를 건드리지 않고 JSON 파일만 교체해 반영할 수 있다.
이 분리는 디자인 반복 속도를 높이는 데 실질적 효과가 있다.
애니메이션 파라미터를 하드코딩한 코드는 디자이너가 수정할 수 없지만,
JSON 기반 파이프라인은 그 경계를 낮춘다.

### 노드 ID 매핑 방식이 전제하는 작업 흐름

이 패키지는 Flutter 위젯이 이미 구현되어 있다고 전제한다.
`FigmaMotionWidget`에 `nodeId`를 지정하면, 그 ID에 해당하는 Figma 노드의
애니메이션 트랙이 해당 위젯에 적용된다.

이 설계는 “위젯 먼저, 애니메이션 나중” 흐름을 따른다.
Figma에서 시각 설계를 완료하고 Motion Dev Mode로 애니메이션을 정의한 뒤,
Flutter에서 동일한 구조의 위젯을 구현하고 노드 ID를 연결하는 순서다.
이 흐름은 디자인과 구현이 Figma를 중심으로 정렬되어 있을 때 자연스럽다.
그렇지 않은 팀에서는 노드 ID를 관리하는 오버헤드가 생긴다.

### 공유 타임라인 컨트롤러의 설계 의미

`FigmaMotionScene`이 하나의 `AnimationController`를 여러 `FigmaMotionWidget`이
공유하도록 설계한 것은, Figma Motion의 타임라인 개념을 그대로 옮긴 것이다.
Figma에서 여러 레이어가 단일 타임라인 위에서 동기화되듯,
Flutter에서도 동일한 컨트롤러로 여러 위젯이 동시에 움직인다.

이 설계는 복잡한 멀티 레이어 애니메이션의 동기화 문제를 단순하게 해결한다.
각 위젯이 독립적인 컨트롤러를 갖는다면, 레이어 간 타이밍 오차가 생길 수 있다.
공유 컨트롤러는 이 문제를 구조적으로 차단한다.

## 비평

### 노드 ID 연결은 디자인-코드 동기화 문제를 해결하지 않고 위임한다

`nodeId: '7:18'` 같은 하드코딩된 노드 ID는 Figma 파일이 재구성될 때마다 깨진다.
Figma에서 레이어를 이동하거나 컴포넌트를 분리하면 노드 ID가 바뀐다.
이 패키지는 그 변화를 감지하거나 경고하는 수단을 제공하지 않는다.

디자인-코드 동기화 문제는 Figma 생태계의 오래된 난제다.
Figma to Code, Anima, DhiWise 같은 도구들이 이 문제에 도전했지만,
각자 다른 방식으로 타협점을 찾았다.
flutter_figma_motion은 이 문제를 해결하려 하지 않고,
노드 ID 관리를 사용자에게 완전히 위임한다.
초기 버전의 범위 설정으로는 합리적이지만,
실무에서 이 방식이 확장되면 노드 ID 목록이 별도 관리 부담이 된다.

### 미지원 속성의 범위가 실무 적용성을 제한한다

색상, 너비/높이, 블러, 섀도우 애니메이션을 지원하지 않는다.
실제 앱의 애니메이션에서 이 속성들은 이동·스케일·불투명도만큼 자주 쓰인다.
버튼이 눌렸을 때 색이 바뀌고, 카드가 펼쳐지며 높이가 늘어나고,
배경이 흐려지는 패턴은 모두 미지원 영역이다.

README는 “JSON의 실제 필드 샘플을 기반으로 확장”한다고 밝힌다.
이는 패키지가 현재 저자가 다루는 유스케이스를 기반으로 성장하고 있음을 의미한다.
오픈소스 초기 단계에서 흔한 방식이지만,
사용자 입장에서는 어떤 Figma 애니메이션이 이 패키지로 재현 가능한지
사전에 판단하기 어렵다.

### “자동 UI 생성 미지원”이 전제하는 개발 방식이 맞지 않는 팀이 있다

이 패키지는 Flutter 위젯이 이미 있어야 동작한다.
Figma 레이아웃을 Flutter 코드로 자동 변환하는 기능은 설계 범위 밖이다.
이 전제는 “디자인과 구현을 따로 관리하는 팀”에게는 자연스럽지만,
“Figma에서 Flutter 코드를 직접 생성하려는 팀”에게는 이 패키지가 끼어들 자리가 없다.

Figma의 Dev Mode와 Make Design, FlutterFlow 같은 도구들은
레이아웃 코드 자동 생성 방향으로 움직이고 있다.
flutter_figma_motion은 그 흐름과 다른 레이어에서 작동한다.
두 접근이 상호보완적일 수도 있지만, 어느 쪽을 선택하느냐에 따라
flutter_figma_motion의 유용성이 달라진다.

## 인사이트

### 애니메이션 파이프라인의 분리는 디자인 툴이 코드 생성보다 앞설 때 생기는 틈이다

Figma가 Motion Dev Mode를 출시한 것은 디자이너가 애니메이션을 정의하고
개발자에게 정확하게 전달하는 문제를 해결하려는 시도다.
그런데 Figma는 이 JSON을 Flutter 코드로 변환하는 공식 경로를 제공하지 않는다.

이 틈에서 flutter_figma_motion 같은 서드파티 패키지가 생긴다.
역사적으로 디자인 툴이 새로운 출력 포맷을 만들 때마다 커뮤니티가 먼저 브리지를 만들었다.
Sketch가 JSON 포맷을 내놓았을 때 Lottie 생태계가 형성된 패턴과 구조적으로 같다.
Figma Motion JSON이 표준으로 자리잡으면 공식 Flutter 플러그인이 나올 것이고,
그때 이런 서드파티 패키지들은 선택지에서 밀려난다.
그 전까지는 커뮤니티 구현이 시장을 채운다.

### 노드 ID 기반 매핑은 장기적으로 타입 안전 DSL로 진화할 압력을 받는다

현재 `nodeId`는 문자열이다.
`'7:18'`이 잘못됐을 때 런타임 전까지 오류를 알 수 없다.
이 문제는 규모가 커질수록 심화된다.
위젯이 수십 개이고 Figma 파일이 자주 바뀌는 프로젝트에서는
노드 ID 불일치가 조용히 애니메이션을 멈추게 만든다.

이 압력은 결국 두 방향 중 하나로 해소된다.
하나는 코드 생성이다. Figma 파일에서 노드 ID를 Dart 상수로 자동 생성하면
컴파일 타임에 오류를 잡을 수 있다.
다른 하나는 런타임 검증과 경고다. 매핑 실패 시 명확한 에러 메시지로 디버깅을 돕는다.
초기 버전이 이 중 어느 방향을 택하느냐가 패키지의 장기 설계를 결정한다.

### Flutter 애니메이션 생태계에서 “디자이너가 제어하는 파라미터”의 범위가 확장되고 있다

전통적으로 Flutter 애니메이션은 개발자가 코드로 정의한다.
디자이너는 목업을 만들고, 개발자가 그것을 해석해 `Tween`과 `Curve`로 옮기는 과정에서
디테일이 손실된다.

flutter_figma_motion은 이 손실 구간을 줄이는 시도다.
큐빅 베지어 값을 Figma JSON에서 Flutter `Cubic` 곡선으로 직접 변환하는 것이
그 핵심이다.
디자이너가 Figma에서 이징 곡선을 조정하면 그 값이 그대로 Flutter에 반영된다.

이 방향이 계속된다면, 디자이너가 실질적으로 제어하는 코드 파라미터의 범위가 넓어진다.
색상, 타이포그래피, 간격이 디자인 토큰으로 코드에 연결된 것처럼,
애니메이션 타이밍과 이징도 디자인 툴에서 직접 관리되는 세계가 열린다.
그 세계에서 개발자의 역할은 파라미터를 결정하는 것이 아니라
파라미터를 받아 실행하는 구조를 만드는 것으로 이동한다.
