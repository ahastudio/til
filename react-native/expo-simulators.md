# Expo Simulators는 코딩 에이전트에게 클라우드 iOS 시뮬레이터와 Android 에뮬레이터를 내주고 녹화와 스크린샷을 증거로 남기는 유료 서비스이다

<https://expo.dev/services/simulators>

HN 토론: <https://news.ycombinator.com/item?id=50471310> (24점, 12개 댓글)

## 소개

Expo Simulators는 Expo 인프라에서 원격 iOS Simulator와 Android Emulator를 띄워
앱을 설치하고, 화면 구조를 살피고, 조작하고, 스크린샷과 녹화를 모으고, 브라우저로 공유하게
하는 Expo Services의 서비스이다.[^intro]
제품 페이지의 문구는 에이전트를 위한 시뮬레이터이다.
에이전트가 빌드를 설치해 앱을 직접 조작하고 자기 작업을 검증하며, 필요한 만큼 병렬로
돌린다는 약속이다.
2026년 11월 12일 Expo 블로그의 출시 글은 이 서비스가 모든 유료 플랜에서 정식(GA)으로
열렸다고 알린다.[^blog]
출시 글은 Szymon Dziedzic(엔지니어링)이 썼고, 몇 달 동안 디자인 파트너들이 써 보며 거친
부분을 다듬었다고 한다.[^blog]

제품 페이지가 내세우는 세 가지 가치는 다음과 같다.
PR마다 증거를 남긴다(각 점검의 스크린샷, 세션 녹화, 빌드 링크).
기본이 병렬이다(아이폰, Android 기기, 폴더블, 태블릿에서 필요한 만큼).
안전하고 확장 가능하다(접근이 제어되는 미리보기와 세션 범위의 자격 증명, 격리된
시뮬레이터에서 실행).
이 페이지는 설치 프롬프트도 보여 준다.
에이전트에게 문서를 읽고 Expo Skills의 `eas-simulator` 스킬을 설치해 계정의 접근 권한을
확인한 뒤 세션을 띄우고, 앱을 설치해 주요 화면을 눌러 보고 스크린샷과 녹화를 보내라는
내용이다.
같은 페이지의 터미널 예시는 `eas simulator --platform ios` 한 줄이다.

### 활용 시나리오

페이지가 소개하는 세 시나리오는 이렇다.
에이전트형 CI는 PR마다 에이전트가 흐름을 시뮬레이션하고 재생 링크를 달고 실패한 점검을
스스로 고친다.
새 기능은 어디서든 에이전트에게 아이디어를 맡기면 기능을 만들고 시뮬레이터에서 검증한 뒤
미리보기 링크로 결과를 보여 준다.
버그 분류는 테스터의 피드백을 받은 에이전트가 시뮬레이터에서 버그를 재현하고 고친 뒤
수정 전후가 담긴 PR을 연다.
출시 글은 접근성 사례도 든다.
에이전트가 가장 큰 글자 크기로 앱을 실행해 레이블이 겹치는 곳을 보고 레이아웃을 고쳐
수정 전후 스크린샷을 PR에 붙였다.[^blog]

### 자주 묻는 질문에 나온 사실

페이지의 FAQ가 밝히는 내용은 이렇다.
셸 명령을 실행할 수 있는 에이전트라면 Claude Code, Codex, Cursor 모두 쓸 수 있다.
Expo로 만든 앱이 아니어도 되고 React Native, Swift, Kotlin, Flutter, Unity 등에서 만든
iOS 시뮬레이터나 Android 에뮬레이터용 빌드면 된다.
GitHub Actions, Expo Workflows, 다른 CI에서 EAS CLI나 REST API로 세션을 시작할 수 있다.
기존 테스트로는 세션에 붙은 Appium 서버에 Appium 테스트를 연결하거나 agent-device로 지원하는
Maestro YAML 흐름의 일부 명령을 돌릴 수 있다.
세션은 계정의 작업 동시성을 공유해 용량이 차면 줄을 선다.
팀원이 브라우저로 실행 중인 앱을 볼 수 있고, 미리보기 링크는 기본적으로 프로젝트 접근
권한이 있는 Expo 로그인을 요구하며 새 세션을 시작하려면 Developer 이상의 역할이 필요하다.
Expo와 React Native 앱은 지문(fingerprint)으로 네이티브 코드가 같은 기존 빌드를 찾아
최신 JavaScript만 다시 묶어(repack) 전체 네이티브 빌드를 건너뛸 수 있다.

## 쓰는 방법

### 접근 조건과 준비

Expo Simulators는 Starter, Production, Enterprise 플랜에서 쓸 수 있다.[^billing]
Expo 서비스 가격 페이지는 Starter가 월 19달러(추가 사용량 별도)이고 Production이 월
199달러이며 두 플랜 모두 Simulators 접근이 포함되고, Free 플랜의 목록에는 없다고 보여
준다.[^pricing]
접근이 없는 계정은 `available`이 false이고, 이때는 세션을 시작하지 말라고 안내한다.[^get-started]
필요한 것은 Expo 계정, Expo Services에 연결된 프로젝트(`eas init`), 최신 EAS CLI이다.
`simulator:*` 명령은 실험적이어서 자주 바뀌므로 설치된 버전의 `eas simulator:start --help`로
지원하는 플래그를 확인하라고 안내한다.[^get-started]
접근 확인(`eas simulator:availability --json`)은 읽기 전용이고 장치를 띄우거나 사용량을
소모하지 않는다.[^get-started]

### 세션의 흐름

세션을 시작하면 CLI가 세션 ID와 컨트롤러 자격 증명을 `.env.eas-simulator`에 쓴다.
이 파일에는 원격 장치에 닿는 토큰이 들어 있어서 `.gitignore`에 넣어야 한다.[^get-started]
세션 종류(`--type`)는 `agent-device`, `argent`, `appium`, `web-preview-only` 중에서 고른다.
미리보기만 필요하면 `web-preview-only`를 쓴다.
기본 장치는 Android에서 `medium_phone`, iOS에서 iPhone 17이다.
앱은 시작 때 빌드 ID, 빌드 지문, 아카이브 URL, Expo Go 중 정확히 하나로 설치할 수 있다.
`--max-duration-minutes`와 `--max-idle-time-minutes`로 자동 정지를 정하고,
끝나면 `eas simulator:stop`으로 멈춘다.[^get-started]

장치는 이렇다.[^devices]
Android 프로필은 `medium_phone`, `pixel_9`, `pixel_9_pro`, `pixel_9_pro_xl`, `pixel_9a`이고
모두 720×1600 화면, 밀도 300이며 기본 시스템 이미지는 Android 35(Google APIs, x86_64)이다.
iOS는 macOS Tahoe 26.5와 Xcode 26.6 이미지이며 iPhone 17, 17 Pro, 17 Pro Max, iPhone Air,
iPhone 17e와 여섯 가지 iPad 시뮬레이터를 쓸 수 있다.
iPhone Duo는 다른 이미지(Xcode 27.1)를 쓴다.
Apple Vision Pro와 Apple TV 시뮬레이터도 이미지에 포함되어 있다.
한 세션은 장치 하나를 켠 상태로 시작한다.[^devices]

### 에이전트에게 맡길 때

공식 문서는 개별 명령을 에이전트에게 주지 말고 `eas-simulator` 스킬을 쓰게 하라고 권한다.[^verify]
스킬의 전체 흐름은 접근 확인, 상황에 맞는 빌드 선택(라이브 수정은 개발 빌드와 Metro, 고정
스크린샷은 현재 소스와 맞는 빌드), 이름 붙인 세션 시작과 `IN_PROGRESS` 확인,
agent-device 명령(`snapshot -i`, `press`, `fill`)으로 조작, 스크린샷과 녹화 수집,
세션 정지와 `.env.eas-simulator` 초기화이다.[^verify]
스킬은 MIT 라이선스이고, 비용이 든다는 경고로 시작하며, macOS처럼 로컬 시뮬레이터가 있는
호스트에서 단순한 시뮬레이터 실행 요청에는 자동으로 켜지지 않게 되어 있다.[^skill]
문서는 에이전트에게 세션을 한 번에 하나만 시작하고 `--max-duration-minutes`를 쓰고 끝나거나
실패하면 세션을 정지하라고 프롬프트로 주문하라고 권한다.[^verify]

## 분석

### 중심 주장은 검증이 새 병목이고 에이전트에게 눈을 주자는 것이다

가장 강하게 말하면 이 서비스는 코드 생성이 빨라진 만큼 코드가 실제로 동작하는지 확인하는
일이 병목이 되었다는 진단 위에 서 있다.
출시 글은 검증이 모든 엔지니어링 팀이 직면한 새 병목이라고 쓰고, 로컬 시뮬레이터의 네 가지
한계를 든다.
병렬 실행이 노트북 자원으로 제한되고, 에이전트들이 같은 시뮬레이터를 두고 충돌하고,
세션 기록이 남지 않고, 에이전트가 노트북에서 돌지 않는다(클라우드 샌드박스, CI)는
것이다.[^blog]
해법은 세션마다 격리된 VM, 컨트롤러 명령(에이전트는 로컬과 같은 명령을 쓴다), 세션의
녹화와 스크린샷과 로그라는 증거이다.[^blog]
PR 검토자가 500줄을 대충 맞아 보이게 읽는 대신 변경이 동작함을 보여 주는 녹화를 본다는
그림이다.[^blog]

### 서비스의 실체는 시뮬레이터 호스팅에 세션 관리와 증거 저장을 얹은 것이다

문서에서 보이는 구성은 단순하다.
세션 시작, 앱 설치, 장치 조작(agent-device, Argent, Appium), 정지의 네 단계이고,
조작 도구는 에이전트가 이미 쓰는 오픈 도구이다.[^intro]
Expo가 더하는 것은 장치의 원격 호스팅, 세션의 수명 관리(자동 정지와 유휴 시간), 계정 역할과
미리보기 링크, 세션 활동 이벤트, 녹화와 산출물 보관이다.[^security]
세션은 Expo Services 작업(job)으로 돌고 계정의 작업 동시성을 쓴다.[^billing]
같은 인프라가 빌드와 제출과 워크플로를 돌리는 것이므로 서비스의 차별점은 새 기술이 아니라
통합이다.
이것은 이 문서의 해석이다.

### 로컬 시뮬레이터와의 경계를 문서가 직접 긋는다

문서는 이 서비스가 로컬 Xcode나 Android Studio 작업을 대체하지 않는다고 적고,
이미 로컬 장치가 있으면 원격이나 공유 접근이 필요할 때만 쓰라고 한다.[^intro]
스킬은 한발 더 나가 macOS에서는 일반적인 시뮬레이터 실행 요청에 이 서비스를 자동으로 쓰지
않는다.[^skill]
이 서비스가 가장 필요한 환경은 로컬 iOS 시뮬레이터가 없는 곳(Linux, 클라우드 샌드박스,
CI)이고, Linux와 Windows 사용자에게는 iOS Simulator를 주는 것이 가치이다.[^intro]
HN 출시 스레드에서도 첫 반응이 이 점에 몰렸다.
colinhunt는 노트북의 에이전트는 괜찮았지만 백그라운드 에이전트에 이것이 필요했다고
썼고, pageofswrds는 Linux 머신에서 iOS 앱을 빌드할 수 있느냐고 물었다.[^colinhunt][^pageofswrds]
엔지니어링 리드 szdziedzic은 Linux에서 도는 에이전트가 원격 클라우드 iOS 시뮬레이터에서
작업을 검증할 수 있다고 답했고, lukisk는 macOS 없이 iOS 앱을 어떻게 빌드하느냐고 되물었다.[^szdziedzic][^lukisk]
이 서비스가 하는 일은 빌드가 아니라 실행(검증)이며, 빌드는 Expo Build에서 만든다는 점이
스레드에는 정리되지 않았다.
이 스레드는 출시 블로그 글의 것이고 이 문서가 읽은 시점에 24점, 댓글 12개였다.

## 비평

### 증거를 모으는 주체가 검증 대상인 에이전트라서 증거의 질은 조건에 달려 있다

제품 페이지의 약속은 PR마다 스크린샷과 녹화가 붙는다는 것이다.
그러나 에이전트에게 주요 화면을 눌러 보라고 시키면 녹화는 그 에이전트가 고른 경로의
기록이다.
같은 에이전트가 만든 코드와 같은 오해를 공유하는 점검은 통과한다는 지적은 이번 저장소의
다른 문서(에이전트 시대의 검증)에서 다룬 문제이다.
문서도 이 한계의 일부를 적는다.
녹화는 모든 프레임을 담지 못해 짧은 프레임 드롭을 증명하거나 반증할 수 없고,
iOS 접근성 스냅샷은 수십 초가 걸릴 수 있으며,
Argent 녹화에는 워터마크가 붙는다.[^limits]
증거가 약속하는 것은 그 경로에서 그 화면이 보였다는 사실이고, 변경이 맞다는 보증은
아니다.
이 문서는 완료의 정의를 사람이 미리 쓰는 것이 이 기능을 쓸 때의 전제라고 읽는다.
이것은 이 문서의 해석이다.

### 보안 모델에 날카로운 모서리가 있고 문서가 직접 비밀로 다루라고 한다

제품 페이지는 접근이 제어되는 미리보기와 세션 범위의 자격 증명을 말한다.
보안 문서는 구체적인 주의 사항을 적는다.[^security]
세션 토큰과 미리보기 링크는 원격 장치에 직접 닿으므로 비밀로 다뤄야 한다.
View Only 역할의 멤버도 진행 중인 세션의 컨트롤러 토큰을 REST API나 GraphQL API로 읽을
수 있다.
세션 페이지는 토큰 값을 기본으로 가리지만 세션 페이지를 볼 수 있는 사람은 누구든 보이게
하거나 복사할 수 있다.
공개 링크에는 미리보기 토큰이 들어 있어서 링크가 있는 누구나 로그인 없이 시뮬레이터를 보고
쓸 수 있고,
비공개 링크를 쓰는 세션도 미리보기 토큰을 갖고 있어서 읽기 권한이 있는 멤버는 이 토큰으로
공개 링크를 만들 수 있다.
산출물 다운로드 URL은 긴 무작위 키를 담을 뿐 인증을 요구하지 않는다.
Metro 터널 URL은 터널이 열려 있는 동안 인증 없이 공개된다.[^security]
출시되지 않은 빌드를 팀의 통제 아래 둔다는 약속을 쓰려면 이 목록을 팀의 규칙으로 옮겨야
한다.
문서가 이 위험을 숨기지 않는다는 점은 장점이다.

### 비용과 한도의 윤곽은 있지만 단가는 이 문서가 읽은 자료에서 찾지 못했다

사용량은 세션이 도는 시간에 비례하고 세션을 멈추지 않으면 최대 시간(유료 115분)까지
돈다.
`--non-interactive`는 명령이 돌아와도 세션을 멈추지 않고, CI 작업이 끝나도 세션은 멈추지
않는다.[^billing]
출시 글은 CI 작업이 일찍 끝나도 시뮬레이터가 무한정 남지 않는다고 하는데,
이것은 최대 시간이 걸려 있다는 뜻이고 그때까지의 사용량은 청구된다.[^blog][^billing]
세션은 다른 Expo Services 작업과 같은 계정 동시성을 쓰고,
Production 플랜은 동시성 15개가 포함이라고 가격 페이지에 적혀 있지만 Starter는 포함 수가
나와 있지 않다.[^pricing]
기본이 병렬이라는 약속은 이 한도 안에서의 병렬이다.
분 단위의 사용 단가는 이 문서가 읽은 문서와 가격 페이지에서 찾지 못했다.
문서가 모순되는 곳도 있다.
세션 길이 한도에 Free 플랜 40분이 있지만 접근 조건은 유료 플랜뿐이다.[^limits][^billing]

### 정식 출시와 실험적 명령이 같은 서비스에서 함께 말해진다

블로그는 GA를 알리지만 문서는 `simulator:*` 명령을 실험적이라 하고 플래그가 자주 바뀐다고
적는다.[^blog][^limits]
제품 페이지의 예시 한 줄(`eas simulator --platform ios`)은 문서의 세션 시작 명령
(`eas simulator:start --platform ios --type ... --non-interactive`)과 다르다.
스킬이 항상 `npx --yes eas-cli@latest`로 최신 CLI를 쓰고 `--help`를 정답으로 삼게 하는 것도
같은 이유이다.[^skill]
서비스는 정식이지만 인터페이스는 아직 움직인다고 읽는 것이 정확하다.

### 이 서비스가 아닌 것도 분명하다

물리 기기는 없다.
Android는 APK만, iOS는 시뮬레이터 빌드(`.app`이 든 `.tar.gz`나 `.tgz`)만 설치된다.
유휴 시간은 미리보기를 보는 것으로는 초기화되지 않고,
시작 시간은 대기 줄에 따라 달라진다.[^limits]
성능 시험(프레임 시간)에는 프로파일러를 쓰라고 문서가 적는다.[^limits]
앞의 증거의 질 문제와 함께, 이 서비스는 기능 확인의 도구이고 품질 인증의 도구는 아니다.

## 인사이트

### 시범 도입은 한 흐름과 짧은 시간 제한으로 시작한다

문서의 권고를 그대로 따르면 시험 절차가 나온다.
접근 확인(읽기 전용)으로 시작하고, `--max-duration-minutes`를 15분쯤으로 짧게 걸고,
세션 이름에 목적을 적고, 에이전트에게 세션 하나만 쓰고 끝나면 반드시 정지하라고 주문한다.[^verify]
이 시간 값은 이 문서의 제안이다.
처음에는 PR 하나의 핵심 흐름(예: 결제 화면)에서만 시험하고 대기 시간과 실패율과 비용을
기록한다.
이 제안은 이 문서의 것이다.

### 비밀과 권한은 켜기 전에 정한다

보안 문서에서 바로 규칙이 나온다.
`.env.eas-simulator`를 `.gitignore`에 넣고 CI 아티팩트로 올리지 않는다.
`--json` 출력의 `remoteConfig`를 CI 로그에 찍지 않는다.
자동화에는 Developer 역할의 로봇 사용자를 쓰고,
공개 링크는 필요한 사람에게만 주고 최대 시간을 건다.[^security]
View Only 멤버가 토큰을 읽을 수 있다는 점은 프로젝트 접근을 줄 때 고려해야 한다.
이 정리는 문서를 규칙으로 옮긴 이 문서의 제안이다.

### 증거의 정의를 PR 양식에 둔다

에이전트가 녹화를 가져오게 하려면 무엇을 보여야 검증된 것인지를 먼저 써야 한다.
이 문서의 제안은 PR 설명에 이 세 칸을 두는 것이다.
확인해야 하는 화면과 동작, 보여 주는 증거(스크린샷이나 녹화의 어느 지점),
이 증거가 덮지 않는 것(성능, 실기기, 특정 OS 버전)이다.
출시 글이 예로 든 접근성 사례(가장 큰 글자에서 레이블이 겹치는 문제를 보고 고친 PR)가 이
형식에 맞는 좋은 예이다.[^blog]

### 도입 판단을 바꿀 관찰

도입 비용의 기준은 검증 한 번당 비용과 검출한 결함이다.
에이전트가 검증했지만 사람이 검토에서 되돌린 비율, 세션 대기 시간, 포함된 동시성 안에서의
병렬 한도, 실제 청구된 분 수를 한 달 동안 기록해 보면 이 서비스가 병목을 줄였는지 알 수
있다.
되돌림 비율이 높거나 대기 시간이 길면 이 서비스는 보기에만 좋은 증거를 늘리는 것이고,
되돌림이 줄고 병렬이 한도 안에서 안정되면 문서의 가정이 맞다는 뜻이다.
이 판단 기준은 이 문서의 제안이다.

---

[^intro]: Expo, [Introduction to Expo Simulators](https://docs.expo.dev/eas/simulators/introduction/)

[^get-started]: Expo, [Get started with Expo Simulators](https://docs.expo.dev/eas/simulators/get-started/)

[^limits]: Expo, [Expo Simulators limitations](https://docs.expo.dev/eas/simulators/limitations/)

[^billing]: Expo, [Expo Simulators usage, limits, and billing](https://docs.expo.dev/eas/simulators/reference/usage-and-billing/)

[^devices]: Expo, [Expo Simulators devices](https://docs.expo.dev/eas/simulators/reference/devices/)

[^security]: Expo, [Expo Simulators security and data](https://docs.expo.dev/eas/simulators/reference/security-and-data/)

[^verify]: Expo, [Let an AI coding agent verify a change on a remote simulator](https://docs.expo.dev/eas/simulators/how-to/verify-a-change-with-an-agent/)

[^skill]: Expo, [eas-simulator (SKILL.md)](https://github.com/expo/skills/blob/main/plugins/expo/skills/eas-simulator/SKILL.md)

[^pricing]: Expo, [Expo Services pricing](https://expo.dev/pricing)

[^blog]: Szymon Dziedzic, [Introducing Expo Simulators: cloud simulators built for agents](https://expo.dev/blog/introducing-expo-simulators-cloud-simulators-built-for-agents), 2026-11-12

[^colinhunt]: <https://news.ycombinator.com/item?id=50471854>

[^pageofswrds]: <https://news.ycombinator.com/item?id=50472011>

[^szdziedzic]: <https://news.ycombinator.com/item?id=50472470>

[^lukisk]: <https://news.ycombinator.com/item?id=50474192>
