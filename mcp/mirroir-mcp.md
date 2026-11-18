# mirroir-mcp: 아이폰을 에이전트에게 맡기는 MCP 서버

<https://mirroir.dev/>

<https://github.com/jfarcand/mirroir-mcp>

## 소개

mirroir-mcp는 MCP 클라이언트(Claude Code, Codex, Cursor, VS Code, Claude Desktop, Hermes, OpenClaw 등)가 macOS의 iPhone Mirroring 앱을 통해 실제 아이폰을 보고 조작하게 하는 Swift 기반 MCP 서버이다. 사이트의 문구는 에이전트가 진짜 아이폰을 쓰게 하라는 것이다.
개발자 모드, Xcode, WebDriverAgent, 탈옥이 필요 없고 아이폰에는 아무것도 설치하지 않는다고 한다. 이름의 mirroir는 miroir의 옛 프랑스어 표기라고 README가 설명한다. 저작권 표시는 Async-IO이다.
이 문서는 `mirroir.dev` 홈페이지와 문서 페이지, 저장소 README와 `docs/`의 시작하기, 도구, 권한, 스킬과 CI 문서, GitHub API 수치와 최신 릴리스를 읽었다. 직접 설치해 써 보지 않았고 `docs/`의 한계, 화면 인식, 보안, FAQ, 설치, CLI, 컴파일된 스킬 문서와 `mirroir-run` 문서, 변경 기록은 열지 못했다.
Dale Seo의 한국어 블로그 글[^blog]이 이 도구를 소개한 내용은 각주로 대조해 적었다.
설명은 모두 프로젝트의 주장이다.

GitHub API로 읽은 시점(2026년 11월 19일)의 수치는 별 376개, 포크 46개, 열린 이슈 2개, 라이선스 Apache-2.0, 언어 Swift, 생성일 2026년 2월 6일, 마지막 푸시 2026년 11월 18일이다. 저장소의 홈페이지 필드는 `mirroir.dev`이고 `main`에 커밋이 804개이다.
최신 릴리스는 v0.50.1(2026년 11월 17일)이며 내용은 CarPlay 연결 폰을 위한 운전 모드(허용한 앱만 쓰고 입력 전에 화면을 읽음)이다. 첨부는 macOS arm64 tarball, Claude Desktop용 `.mcpb`, 체크섬이다. 기여자 라이선스 동의서(CLA)가 있다.

## 동작 방식

- 도구: 사이트는 42개라고 하며 문서는 네 묶음으로 나눈다. 터치 8개(`tap`, `double_tap`, `long_press`, `swipe`, `drag`, `touch`, `pinch`, `rotate`), 입력 4개(`type_text`, `press_key`, `shake`, `hold_keys`), 관찰 11개(`screenshot`, `describe_screen`, `listen`, `classify_screen`, `start_recording`, `stop_recording`, `get_orientation`, `status`, `check_health`, `calibrate_component`, `list_targets`), 탐색과 스킬과 메모와 대상 19개(`launch_app`, `open_url`, `press_home`, `spotlight`, `scroll_to`, `reset_app`, `set_network`, `measure`, `run_steps`, `generate_skill`, `list_skills` 등)이다. 블로그 글은 41개라고 적었고 지금 문서는 42개이다.[^blog]
- 화면 읽기: 미러링 창 안은 영상이므로 `describe_screen`이 텍스트 요소와 탭 좌표를 돌려 준다. 기본은 Apple Vision OCR이고 `~/.mirroir-mcp/models/`에 YOLO CoreML 모델이 있으면 아이콘 탐지를 합친다. `screenDescriberMode`가 `vision`이면 스크린샷을 AI 비전 모델에 보내 요소를 의미로 식별한다.[^blog]
- 입력: 탭과 타이핑은 폰을 앞으로 가져오지 않고 전달되고, 드래그와 두 손가락 제스처는 잠깐 앞으로 가져온다. `type_text`는 자동 수정의 영향을 받을 수 있고 키보드에 없는 문자는 붙여 넣은 뒤 OCR로 확인하며 이모지는 실패할 수 있다고 한다. 블로그 글은 한글이 Universal Clipboard와 Handoff를 거치고, OCR 기본 언어가 `en-US`뿐이라 `ocrLanguages`에 `ko-KR`을 넣어야 한다고 구체적으로 설명한다.[^blog]
- 요구 사항: macOS 15 이상, Apple silicon 또는 T2 칩 인텔 맥, iOS 18 이상의 아이폰(같은 Apple 계정), 켜진 Bluetooth와 Wi-Fi가 필요하다. 시작 문서는 EU에서는 Apple이 iPhone Mirroring을 제공하지 않는다고 적는다. `listen` 도구는 macOS 26이 필요하다.

## 설치

사이트와 문서가 안내하는 방법은 다음과 같다.

```text
brew tap jfarcand/tap && brew install mirroir-mcp
npx -y mirroir-mcp install
claude plugin marketplace add jfarcand/mirroir-mcp && claude plugin install mirroir@mirroir
npx -y mirroir-mcp doctor
```

그 밖에 `curl` 설치 스크립트, Hermes 플러그인, Claude Desktop용 `.mcpb`(v0.43.0 이상), 클라이언트별 등록 명령(`claude mcp add --transport stdio mirroir -- npx -y mirroir-mcp`, `codex mcp add ...`, `openclaw mcp add ...`)이 있다. `npx -y mirroir-mcp skill --install`은 에이전트용 운영 매뉴얼 `SKILL.md`를 쓴다.
`doctor`는 설정을 점검해 고칠 것을 알려 준다. 블로그 글도 같은 설치 방법을 소개하고, 처음 실행하면 화면 기록과 손쉬운 사용 권한을 호스트 앱에 줘야 하고 화면 기록은 그 앱을 완전히 종료했다가 다시 열어야 적용된다고 덧붙인다.[^blog]

## 권한 모델

기본은 읽기 전용이고 허용 목록이 없으면 읽기 도구만 노출된다.
문서가 꼽는 항상 허용 도구는 14개(`screenshot`, `describe_screen`, `status`, `list_skills` 등)이고 나머지는 허용되기 전까지 `tools/list`에서 숨겨진다. 블로그 글이 읽기 도구를 13개라고 쓴 것과 숫자가 다르다.[^blog]

설정은 `~/.mirroir-mcp/permissions.json`이나 프로젝트의 `.mirroir-mcp/permissions.json`에 둔다.

```json
{
  "allow": ["tap", "swipe", "type_text", "press_key", "launch_app"],
  "deny": [],
  "blockedApps": []
}
```

- `allow`: 허용할 변경 도구이며 `["*"]`는 전부 허용이다. `deny`가 `allow`보다 우선한다.
- `blockedApps`: 아이폰에 표시되는 앱 이름이며 `launch_app`, `open_url`, `set_network`, 스킬 탐색, 홈 화면과 스포트라이트 아이콘 탭을 거부한다.
- `skipElements`, `perApp`, `driving`(CarPlay 모드, `allowedApps`)이 있다.
- `--yolo`와 `--dangerously-skip-permissions`는 권한 시스템을 우회하며 개발과 테스트용이다. `mirroir-mcp serve`는 두 플래그를 거부하고 운전 모드는 이 플래그로 꺼지지 않는다.
- 사이트의 안전 주장: 비밀번호나 Touch ID를 묻는 시트는 누르지 않고, iPhone Mirroring 종료, 맥 잠금, MCP 클라이언트 종료가 중단 장치이며, 텔레메트리가 없고 기본 네트워크 호출은 npm 버전 확인(하루 한 번, `updateCheck: false`로 끔)뿐이다.

블로그 글의 예시 설정은 `blockedApps`에 금융 앱(Wallet, 토스, 카카오뱅크)을 넣어 `launch_app`이 못 열게 하는 것이다.[^blog]

## 스킬과 재생

- 스킬: `SKILL.md` 파일(YAML 머리글과 번호 매긴 단계, 예 `Tap "Email"`)이며 좌표가 아니라 화면의 글자로 맞춘다. 전역 `~/.mirroir-mcp/skills/`와 프로젝트 `.mirroir-mcp/skills/`에 둔다. `generate_skill`의 `explore`는 너비 우선(기본)이나 깊이 우선으로 앱을 탐색하며 기본 깊이 6, 화면 30개, 300초로 제한된다.
- 재생: `mirroir test <스킬>`은 컴파일된 스킬(`.compiled.json`)을 AI 없이 재생한다. 옵션은 `--junit`, `--report-json`, `--dry-run`, `--confirm-destructive`, `--agent`, `--timeout`이고 종료 코드는 0 통과, 1 실패, 2 인자 거부이다. AI가 필요한 단계(`verify`, `remember` 등)는 CLI에서 평가되지 않는다. `--agent`는 실패 단계의 AI 진단이며 OpenAI, Anthropic 모델과 Ollama를 지원한다.[^blog]
- `mirroir-run`: 아이폰, 웹(Playwright), HTTP, 하위 프로세스를 한 YAML 시나리오로 돌리는 별도 바이너리이다. 판정은 통과, 실패, DRIFT(모두 통과했지만 화면이 기준선과 다름, 종료 코드 65)이고 웹과 HTTP 단계는 Linux CI에서 돈다. 블로그 글은 CI에서 미러링이 연결된 맥이 필요해 자체 호스트 러너(Mac mini 등)를 써야 한다고 짚는다.[^blog]

## 비교표

사이트의 비교표(홈페이지와 문서가 같음)는 mirroir, phone-harness, mobile-mcp, Appium을 비교한다.

| 항목                                | mirroir | phone-harness                  | mobile-mcp         | Appium                             |
| ----------------------------------- | ------- | ------------------------------ | ------------------ | ---------------------------------- |
| 개발자 모드 없이 실물 아이폰        | 가능    | 가능                           | USB 연결 신뢰 기기 | 불가(WebDriverAgent와 개발자 모드) |
| 내 아이폰을 임의 MCP 클라이언트에서 | 가능    | 불가(클라우드 MCP, 로컬은 CLI) | 가능               | 별도 appium-mcp                    |
| LLM 없이 재생                       | 가능    | 직접 쓴 Python 스크립트        | 불가               | 가능(테스트 코드)                  |
| 드리프트 판정                       | 가능    | 불가                           | 불가               | 불가                               |
| 안드로이드                          | 불가    | 가능                           | 가능               | 가능                               |
| iOS 시뮬레이터                      | 불가    | 불가                           | 가능               | 가능                               |
| 호스팅 클라우드 폰                  | 불가    | 가능                           | 가능               | 서드파티 클라우드                  |

사이트는 phone-harness를 가장 가까운 도구라고 부른다. 블로그 글도 같은 저장소의 비교표를 옮기며 안드로이드나 시뮬레이터에는 mobile-mcp나 Appium이 맞다고 적는다.[^blog]
이 저장소의 `agent-skill/phone-harness.md`와 `test/appium.md`가 해당 도구를 따로 정리한다.

## 분석

### 중심 주장은 설정 없는 실기기 접근이다

다른 도구가 개발자 모드, 서명, 설치된 에이전트를 요구하는 자리에서 iPhone Mirroring이라는 OS 기능을 쓰는 것이 차별점이다.
그 대가로 입력이 포인터 하나로 제한되고(멀티터치가 제한되고 트윈스틱 게임은 어렵다고 사이트가 적음) 화면은 영상이라 OCR이나 비전 모델로 읽어야 한다.
이는 사이트의 서술을 이 문서가 정리한 것이다.

### 권한 설계가 기본 닫힘이다

읽기 도구만 열려 있고 쓰기는 허용 목록에서 하나씩 켠다는 구성이 사이트의 안전 설명의 중심이다.
앱 이름 차단과 운전 모드, 도구별 허용(`perApp`)으로 에이전트의 범위를 좁힌다. 이는 이 문서의 해석이다.

### 한 번 탐색해 두고 재생하는 방식이다

에이전트가 탐색해 만든 스킬을 컴파일하면 이후 LLM 없이 재생한다는 점이 테스트 도구로서의 위치를 만든다.
블로그 글도 이 부분을 가장 실용적인 가치로 꼽는다.[^blog]

## 비평

### 앱 이름 차단의 범위가 문서에서 한정된다

`blockedApps`가 막는 경로는 `launch_app`, `open_url`, `set_network`, 탐색, 홈 화면과 스포트라이트 아이콘 탭으로 열거되어 있다.
이미 열려 있는 앱 안에서의 동작이나 다른 경로로 앱이 열린 경우를 막는지는 읽은 문서에서 알 수 없다. 보안 문서는 열지 못했다.

### 한계가 구조적이다

아이폰만 지원하고 안드로이드, iOS 시뮬레이터, 호스팅 폰은 불가하다. EU에서는 iPhone Mirroring 자체가 제공되지 않는다고 한다.
화면 탐색은 깊이와 화면 수와 시간으로 제한되어 큰 앱의 모든 화면을 찾지는 못한다고 사이트가 적는다.
iOS 26에서 Spotlight로 앱을 여는 `launch_app`이 세션당 한 번만 타이핑되는 문제도 도구 문서가 적는다.

### 비교표가 자기 작성이다

표의 모든 칸은 프로젝트가 작성했고 다른 도구에서의 시험 결과가 아니다.
phone-harness를 가장 가까운 도구로 인정하는 서술은 솔직하지만 독립 비교는 아니다.

### 개발 속도가 빠른 초기 프로젝트이다

2026년 2월에 시작해 9개월 만에 0.50이다. 도구 수가 블로그 글(41개)에서 지금(42개)으로, 읽기 도구 수가 13개에서 14개로 바뀌었다.
인터페이스가 빠르게 변하는 중이라 이 문서의 수치도 곧 달라질 수 있다.

### 외부 반응

HN에는 이 저장소와 사이트로 올라온 글이 없었다(대조 쿼리는 정상이었다). 블로그 글 주소로 올라온 글도 없었다.
Lobste.rs에는 `daleseo.com` 도메인의 글이 없었다.
GeekNews에서는 `mirroir`와 `iPhone Mirroring MCP`로 검색했고 대조 쿼리는 정상이었으나 이 프로젝트의 토픽은 없었다.

## 인사이트

### 가져갈 것은 에이전트에게 실기기를 맡기는 단계적 순서이다

읽기 전용에서 화면 설명만 시켜 보고, 설정 앱 같은 무해한 앱에서 탭과 입력을 허용하고, 금융 앱은 차단 목록에 먼저 넣는다.[^blog]
`--yolo`는 개발용이다. 이는 이 문서의 적용이다.

### 탐색을 스킬로 굳혀 비결정성을 줄인다

에이전트의 탐색은 비싸고 매번 달라질 수 있으므로, 한 번 탐색한 결과를 컴파일해 반복 실행에는 LLM을 빼면 비용과 변동이 줄어든다.

### 확인할 관찰

이 프로젝트의 주장을 가를 관찰은 세 가지이다.
OCR과 비전 모드의 정확도와 지연,
`blockedApps`와 보안 모델이 실제로 막는 경로,
릴리스가 빠르게 바뀌는 동안의 호환성 유지이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^blog]: [mirroir-mcp로 AI 에이전트에게 내 아이폰 맡기기 | Engineering Blog by Dale Seo](https://daleseo.com/mirroir-mcp/)
