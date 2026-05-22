# android-testing-skills

<https://github.com/skydoves/android-testing-skills>

## 소개

`android-testing-skills`는 skydoves(Jaewoong Eum)가 제작한 오픈소스 Agent Skills 라이브러리로,
Android 엔지니어가 다루는 테스팅 영역 전반을 54개의 스킬 파일로 정리한 컬렉션이다.
Claude Code, Android Studio Agent mode, Gemini 같은 AI 코딩 에이전트가 Android 테스팅
작업을 수행할 때 참조하는 운영 지침서(operational instruction) 역할을 한다.

스킬은 7개 세트로 구분된다. `compose/`(25개), `fundamentals/`(5개), `kotlin/`(1개),
`jvm-tests/`(6개), `instrumentation/`(6개), `platform/`(1개), `adb/`(10개)이며,
프로젝트에서 실제로 사용하는 영역만 선택적으로 가져다 쓰도록 설계됐다.

각 스킬은 `SKILL.md` 파일 하나와 선택적 `references/` 디렉토리로 구성된다.
YAML 프런트매터에 트리거 어휘(trigger vocabulary)를 선언하고, 본문에 번호가 매겨진
워크플로를 기술한다. 에이전트는 현재 작업에 스킬이 적용되는지 프런트매터를 보고 판단한
뒤, `SKILL.md`의 워크플로를 단계별로 따른다.

인간을 위한 문서가 아니라 LLM을 위한 운영 지침이라는 점이 핵심 설계 원칙이다.
문체는 간결하고 명령형이며, RIGHT/WRONG 코드 쌍, MUST/MUST NOT 지시문,
작업 완료를 증명하는 Verification 체크리스트로 구성된다.

## 분석

### 스킬 구조와 디렉토리 레이아웃

리포지토리는 `<set>/<category>/<slug>/SKILL.md` 계층으로 조직돼 있다.
그러나 에이전트 로더는 `<install-dir>/<slug>/SKILL.md`처럼 평탄한(flat) 구조를 기대한다.
이 불일치를 해소하기 위해 `scripts/install-skills.sh`가 각 스킬을 슬러그 이름으로
대상 디렉토리에 심볼릭 링크로 연결한다.

```bash
git clone https://github.com/skydoves/android-testing-skills.git \
  ~/.claude/skills-sources/android-testing-skills

~/.claude/skills-sources/android-testing-skills/scripts/install-skills.sh
```

스크립트는 멱등성(idempotent)을 보장하며, `git pull` 이후 재실행하면 새 스킬이
자동으로 등록된다. `~/.claude/skills/`의 다른 엔트리를 건드리지 않으므로 Google
퍼스트파티 카탈로그(`android skills add`)와 공존할 수 있다.

### 편집 방침(Editorial Position)

README에는 10개의 교차 적용 방침이 명시돼 있다. 주요 내용은 다음과 같다.

- 프로덕션 소스에서 `Modifier.testTag`나 `android:id`를 상수로 정의하고, 테스트에서
  태그로 찾는다. 텍스트 파인더는 국제화(i18n) 변경에 취약하다.
- Compose 애니메이션 테스트는 반드시 `mainClock.autoAdvance = false`로 설정해야 한다.
- `waitUntil` 타임아웃은 벽시계(wall clock), `advanceTimeUntil`은 테스트 클록이다.
- `Thread.sleep`은 안티패턴이다. 스크린샷 테스트에서 RenderThread 대기 시에만 예외다.
- `am instrument`의 종료 코드는 `-w` 플래그 없이는 의미가 없다.
- `pm clear`로 헤르메틱(hermetic) 리셋을 수행한다. `am force-stop`은 프로세스만 죽이고
  SharedPreferences, DB, 파일을 남긴다.
- `androidx.test:orchestrator`는 `androidTestUtil`로 의존성을 추가해야 한다.
  `androidTestImplementation`은 조용히 실패한다.

### 스코프 경계

포함 범위: Jetpack Compose UI 테스팅, JVM 단위 테스트(JUnit4/Mockito/MockK/Turbine),
온디바이스 인스트루먼트 테스트(Espresso/UiAutomator), ADB 기반 E2E/CI, 테스팅 기초.

의도적 제외 범위: 스크린샷/골든 테스팅(Paparazzi/Roborazzi), 코드 커버리지(JaCoCo/Kover),
정적 분석(lint/ktlint/detekt), 성능 안정성(자매 리포지토리 `compose-performance-skills`에서 담당).

## 비평

### 강점

스킬 파일이 인간 문서가 아닌 LLM 운영 지침으로 명확히 설계된 점이 두드러진다.
RIGHT/WRONG 코드 쌍, MUST/MUST NOT 지시문, Verification 체크리스트는 에이전트가
작업 완료를 자가 검증할 수 있게 한다. 모든 API 주장이 `androidx/` 파일 경로나
공식 외부 문서로 근거를 제시하는 원칙도 신뢰성을 높인다.

7개 세트로 나눠 필요한 부분만 선택하도록 설계한 점도 실용적이다.
54개 스킬을 전부 로드하면 컨텍스트 창을 낭비하므로, 팀이 실제로 작성하는
테스트 유형에 맞춰 취사선택할 수 있다.

### 약점

Android Studio Agent mode와 Gemini에서의 동작은 저자가 독립적으로 검증하지 않았다고
README에 명시돼 있다. 즉, Claude Code 이외의 에이전트에서는 실제 동작을 보장하지 않는다.

스코프 외로 명시된 스크린샷 테스팅(Paparazzi, Roborazzi)과 코드 커버리지는 많은
Android 프로젝트에서 필수 요소다. 이 라이브러리만으로 Android 테스팅 에이전트 스킬을
완성하려면 자매 리포지토리와 별도 스킬을 조합해야 한다.

스킬 파일 본문이 500줄로 제한되어 있어 복잡한 주제는 `references/` 디렉토리로 분리된다.
에이전트가 참조 파일까지 자동으로 로드하는지 여부는 런타임마다 다를 수 있어,
스킬이 기대한 대로 동작하지 않을 가능성이 있다.

## 인사이트

### Agent Skills는 프롬프트 엔지니어링의 모듈화다

Agent Skills 형식은 거대한 시스템 프롬프트를 단일 파일로 작성하던 방식에서 벗어나,
각 도메인 지식을 독립적인 `SKILL.md` 단위로 캡슐화하는 전환점을 보여준다.
이는 소프트웨어 엔지니어링의 단일 책임 원칙(Single Responsibility Principle)을
프롬프트 설계에 적용한 것과 같다.

`android-testing-skills`가 54개 스킬을 7개 세트로 구조화한 방식은, 팀이 필요한
지식만 선택적으로 에이전트에 주입할 수 있게 한다. 컨텍스트 창 낭비를 줄이고,
도메인 지식의 버전 관리와 업데이트가 독립적으로 가능해진다는 2차 효과가 생긴다.
기존의 모놀리식 시스템 프롬프트는 일부 지식만 업데이트하려 해도 전체를 교체해야 했다.

### 에이전트를 위한 “기계 가독성” 문서의 새로운 기준

이 프로젝트는 문서 작성의 타깃 독자를 인간에서 LLM으로 바꿀 때 어떤 변화가 생기는지를
잘 보여준다. 간결하고 명령형인 문체, RIGHT/WRONG 코드 쌍, MUST/MUST NOT 지시문,
Verification 체크리스트는 모두 에이전트의 행동 일관성을 높이기 위한 장치다.

인간 독자를 위한 문서는 배경 설명과 맥락, 왜(why)를 중시한다. 반면 에이전트를 위한
문서는 구체적인 코드 패턴, 명확한 규칙, 검증 가능한 완료 기준을 우선한다.
`docs/SPEC.md`가 스킬 작성 규격을 별도로 정의하고 기여자에게 엄격히 요구하는 것도
이 새로운 문서 패러다임을 커뮤니티 전체에 확산시키기 위한 전략이다.

역사적으로 API 문서, 타입 힌트, 린트 규칙이 코드의 기계 가독성을 높여왔다면,
Agent Skills는 지식 자체의 기계 가독성을 높이는 새로운 시도다.

### Android 테스팅 지식의 분산 문제를 해결하는 방식

Android 테스팅 생태계는 JUnit4, Mockito, MockK, Espresso, UiAutomator, ADB 등
파편화된 도구가 뒤섞여 있다. 공식 문서는 각 라이브러리에 분산돼 있고, 올바른 조합과
함께 사용하는 안티패턴에 대한 경고는 찾기 어렵다.

이 라이브러리의 편집 방침(Editorial Position) 10개 항목은 그 분산된 지식 중에서
실수가 가장 잦은 교차 지점을 추려낸 것이다. 예컨대 `androidx.test:orchestrator`를
`androidTestUtil`이 아닌 `androidTestImplementation`으로 추가하면 조용히 실패한다는
사실은 공식 문서에서 찾기 어렵지만, 실제로 많은 팀이 겪는 함정이다.

에이전트가 이런 지식을 스킬로 내재화하면, 개발자가 실수를 저지르기 전에 올바른 패턴을
안내받는 흐름이 가능해진다. 코드 리뷰에서나 발견되던 지식이 코드 작성 단계로 앞당겨지는
것이다. 이는 “shift-left testing”과 유사하게 “shift-left knowledge sharing”이라 부를
수 있는 패턴이다.

### 오픈소스 커뮤니티 주도 에이전트 지식 생태계의 가능성

Google의 퍼스트파티 Android CLI 카탈로그(`android skills add`)와 별개로, 커뮤니티가
자체 스킬 라이브러리를 게시하고 배포할 수 있는 생태계가 열리고 있음을 이 프로젝트가
보여준다. `install-skills.sh`가 멱등적으로 동작하며 퍼스트파티 카탈로그와 공존하도록
설계된 것은, 이 생태계의 컴포저블(composable) 특성을 의도적으로 구현한 것이다.

npm, PyPI처럼 패키지 생태계가 언어 생태계를 풍요롭게 했듯, Agent Skills 라이브러리
생태계가 AI 코딩 에이전트의 도메인 역량을 커뮤니티 기여로 확장하는 경로가 될 수 있다.
`android-testing-skills`와 `compose-performance-skills`의 조합이 그 시작점이다.
앞으로 특정 아키텍처 패턴, 라이브러리, 플랫폼에 특화된 스킬 라이브러리들이
등장할 가능성이 높다.
