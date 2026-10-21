# CLI-Anything: 모든 소프트웨어를 에이전트 네이티브로 만드는 프레임워크

<https://github.com/HKUDS/CLI-Anything>

HN 토론: <https://news.ycombinator.com/item?id=47360545> (4점, 0개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=47364480> (2점, 1개 댓글)

## 목차

- [소개](#소개)
- [사용법](#사용법)
  - [두 가지 시작점](#두-가지-시작점)
  - [생성기로 새 하네스 만들기](#생성기로-새-하네스-만들기)
  - [생성된 CLI 쓰기](#생성된-cli-쓰기)
  - [에이전트가 소비하는 방식](#에이전트가-소비하는-방식)
  - [직접 확인하는 법](#직접-확인하는-법)
- [분석](#분석)
  - [7단계 파이프라인 아키텍처](#7단계-파이프라인-아키텍처)
  - [CLI를 에이전트 인터페이스로 선택한 이유](#cli를-에이전트-인터페이스로-선택한-이유)
  - [SKILL.md 생성과 에이전트 자율 발견](#skillmd-생성과-에이전트-자율-발견)
  - [커뮤니티 생태계와 CLI-Hub](#커뮤니티-생태계와-cli-hub)
- [비평](#비평)
  - [강점](#강점)
  - [약점](#약점)
  - [클로즈드 소스 소프트웨어에 대한 관점 부재](#클로즈드-소스-소프트웨어에-대한-관점-부재)
  - [README 수치가 서로 맞지 않는다](#readme-수치가-서로-맞지-않는다)
  - [테스트가 통과해도 실제 소프트웨어는 호출되지 않았다](#테스트가-통과해도-실제-소프트웨어는-호출되지-않았다)
  - [에이전트 효용의 증거는 아직 없다](#에이전트-효용의-증거는-아직-없다)
  - [보안](#보안)
  - [함정과 체크리스트](#함정과-체크리스트)
- [인사이트](#인사이트)
  - [CLI가 에이전트 시대의 보편 인터페이스로 부활하는 역사적 아이러니](#cli가-에이전트-시대의-보편-인터페이스로-부활하는-역사적-아이러니)
  - [“진짜 소프트웨어 통합”이 드러내는 AI 자동화의 근본 문제](#진짜-소프트웨어-통합이-드러내는-ai-자동화의-근본-문제)
  - [소프트웨어 에코시스템의 에이전트 네이티브 전환이 만드는 새로운 계층 구조](#소프트웨어-에코시스템의-에이전트-네이티브-전환이-만드는-새로운-계층-구조)
  - [7단계 파이프라인의 메타적 함의: AI가 AI 도구를 만든다](#7단계-파이프라인의-메타적-함의-ai가-ai-도구를-만든다)

## 소개

CLI-Anything은 홍콩대학교 데이터 사이언스 연구소(HKUDS)가 개발한 오픈소스
프레임워크로, 어떤 소프트웨어든 AI 에이전트가 제어할 수 있는 CLI(Command Line
Interface) 하네스(harness)를 자동으로 생성한다. “오늘의 소프트웨어는 인간을
위해 만들어졌다. 내일의 사용자는 에이전트가 될 것이다”라는 비전 아래, 인간을
위해 설계된 GUI 소프트웨어와 AI 에이전트 사이의 격차를 메우는 것을 목표로 한다.

Claude Code 플러그인으로 설치하면 `/cli-anything <소프트웨어 경로>`라는 단일
명령어로 7단계 파이프라인이 자동 실행된다. 소스 코드 분석, CLI 아키텍처 설계,
Click 기반 구현, 테스트 계획 수립, 테스트 작성,
문서화, `pip install -e .` 설치까지
전 과정이 자동화된다. 저장소에는 GIMP, Blender, LibreOffice, OBS Studio 등 69개
디렉터리의 CLI 하네스가 들어 있고, README는 수천 개의 테스트가 100% 통과한다고
적는다. 다만 이 수치는 README 안에서도 서로 어긋난다(비평 절 참조).

생성된 CLI는 두 가지 모드로 동작한다. 대화형 REPL(Read-Eval-Print Loop) 모드와
서브커맨드 모드다. 모든 명령어에 `--json` 플래그를 지원하여 에이전트가 구조화된
데이터를 쉽게 처리할 수 있다. 또한 각 CLI는 SKILL.md 파일을 함께 생성하여,
`npx skills add`를 통해 에이전트가 자율적으로 CLI를 발견하고 설치할 수 있다.

CLI-Hub는 커뮤니티가 만든 CLI 하네스를 등록하고 배포하는 레지스트리다.
`pip install cli-anything-hub` 설치 후 `cli-hub install <이름>`으로 원하는
CLI를 설치할 수 있다. 메타 스킬을 통해 에이전트가 자율적으로 카탈로그를
탐색하고 적절한 CLI를 선택해 설치하는 것도 지원한다.

## 사용법

### 두 가지 시작점

README는 시작점을 둘로 나눈다.
이미 만들어진 CLI를 쓰려면 CLI-Hub를,
목록에 없는 소프트웨어를 위해서는 생성기를 쓴다.
CLI-Hub 쪽은 `pip install cli-anything-hub`로 패키지 관리자를 설치한 뒤
`cli-hub list`, `cli-hub search <query>`,
`cli-hub install <name>`, `cli-hub launch <name>` 순으로 쓴다.
PyPI에는 `cli-anything-hub` 0.4.1이 올라와 있고
Python 3.10 이상을 요구한다[^pypi-hub].
각 CLI는 대개 실제 데스크톱 소프트웨어를 감싼 껍데기이므로
GIMP나 Blender 같은 원본 프로그램은 따로 설치해야 한다.

에이전트에게 카탈로그 탐색을 맡기려면
`npx skills add HKUDS/CLI-Anything --skill cli-hub-meta-skill -g -y`로 메타
스킬을 설치하고 “CLI-Hub에서 알맞은 CLI를 찾아 작업을 끝내라”고 지시한다.

### 생성기로 새 하네스 만들기

생성기는 Claude Code 플러그인으로 배포된다.
`/plugin marketplace add HKUDS/CLI-Anything`,
`/plugin install cli-anything` 두 줄로 설치하고
`/cli-anything ./gimp`처럼 실행한다.
인자는 소스 코드 경로나 GitHub 저장소 주소여야 한다.
`cli-anything-plugin/commands/cli-anything.md`는 “gimp” 같은
소프트웨어 이름만 넘기는 것을 받아들이지 않는다고 명시한다.
GitHub 주소를 주면 에이전트가 먼저 저장소를 내려받고, 그 사본을 분석한다.

같은 방법론을 Cursor, Codex, Pi, OpenClaw, OpenCode, Hermes,
Reasonix, Qodercli, GitHub Copilot CLI용 설치 스크립트로도 제공한다.
Claude Code가 아닌 곳에서는
대부분 `bash <도구>-skill/scripts/install.sh` 형태이고,
이 스크립트는 `HARNESS.md`와 가이드를 각 에이전트의 스킬 폴더로 복사한다.
어느 플랫폼이든 생성물의 형식은 같다고 README는 설명한다.

생성 후에는 `/cli-anything:refine ./gimp "배치 처리와 필터"`처럼
빠진 기능을 채운다.
`:test`와 `:validate`, `:list`도 있다.
README는 한 번의 실행으로 전체 기능이 덮이지 않을 수 있으니
`refine`을 되풀이하라고 스스로 적어 둔다.

### 생성된 CLI 쓰기

생성물은 `<소프트웨어>/agent-harness/` 아래의 파이썬 패키지다.
`cd gimp/agent-harness && pip install -e .` 뒤에
`which cli-anything-gimp`로 PATH 등록을 확인한다.
인자 없이 실행하면 대화형 REPL이 열리고,
서브커맨드를 주면 한 번만 실행하고 끝난다.
`--json`을 앞에 붙이면 사람이 읽는 표 대신 JSON을 출력한다.

```bash
cli-anything-gimp project new --width 1920 --height 1080 -o poster.json
cli-anything-gimp --json layer add -n "Background" --type solid --color "#1a1a2e"
```

위 두 줄은 README의 예시에서 가져왔다.
GIMP 하네스의 `gimp_cli.py`를 읽어 보면 최상위 그룹에 `--json`, `--project`,
`--dry-run` 옵션이 실제로 있고,
명령이 끝난 뒤 결과 콜백이 프로젝트를 자동 저장한다.
다만 README의 두 번째 예시가 쓰는 `layer add`와
`--color` 옵션은 `gimp_cli.py`에 없다.
코드에는 `layer new`(채우기 옵션은
`--fill`)와 `layer add-from-file`이 있을 뿐이다.
명령 이름과 옵션만 소스에서 대조했고 실제로 실행해 보지는 않았으므로,
그대로 붙여 넣으면 실패할 가능성이 높다는 뜻이다.

### 에이전트가 소비하는 방식

에이전트는 세 단계로 접근한다.
먼저 `skills/cli-anything-<이름>/SKILL.md`를 읽어 명령 그룹과 예시를 파악한다.
다음에 `--help`로 세부 옵션을 확인하고, 호출할 때는 `--json`으로 결과를 받는다.
저장소 루트의 `skills/` 아래에는 현재 70개의 SKILL.md가 있어
`npx skills add HKUDS/CLI-Anything --list`로 한꺼번에 조회할 수 있다.
오류도 JSON으로 나온다.
GIMP 하네스는 실패하면 `{"error": ..., "type": ...}` 꼴의 JSON을 출력한다.

### 직접 확인하는 법

생성된 하네스의 테스트는
`python3 -m pytest cli_anything/<소프트웨어>/tests/ -v`로 돌리고,
설치된 명령을 대상으로 검증하려면
`CLI_ANYTHING_FORCE_INSTALLED=1`을 앞에 붙인다.
테스트가 통과했다는 사실은 하네스가 동작한다는 증거가 못 된다.
뒤의 비평에서
보듯 테스트가 통과하는 동안 실제 렌더링은 한 번도 호출되지 않는 경우가 있었다.
출력 파일의 매직 바이트나 크기까지 직접 열어 보는 확인을 따로 해야 한다.

## 분석

### 7단계 파이프라인 아키텍처

CLI-Anything의 핵심은 HARNESS.md로 정의된 표준 운영 절차(SOP)다. 이 문서가
전체 생성 파이프라인의 단일 진실 출처(single source of truth) 역할을 한다.

1. **분석(Analyze)**: 소스 코드를 스캔하여 GUI 동작을 API로 매핑
2. **설계(Design)**: 커맨드 그룹, 상태 모델, 출력 포맷 아키텍처 수립
3. **구현(Implement)**: REPL, JSON 출력,
실행 취소/재실행이 포함된 Click CLI 빌드
4. **테스트 계획(Plan Tests)**: TEST.md에 단위 테스트 및 E2E 테스트 계획 작성
5. **테스트 작성(Write Tests)**: 포괄적인 테스트 스위트 구현
6. **문서화(Document)**: TEST.md를 실행 결과로 업데이트
7. **설치(Publish)**: `setup.py` 생성 및 `pip install -e .`로 PATH에
설치. PyPI 업로드 절차는 `guides/pypi-publishing.md`에 별도로 있다

생성된 CLI는 네 계층의 테스트를 거친다. 단위 테스트, 네이티브 E2E 테스트(파일
구조 검증), 실제 백엔드 E2E 테스트(실제 소프트웨어 실행 결과 검증), CLI 서브
프로세스 테스트가 그것이다. LibreOffice → PDF의 경우 `%PDF-` 매직 바이트까지
확인한다.

### CLI를 에이전트 인터페이스로 선택한 이유

프로젝트는 CLI가 인간과 AI 에이전트 모두를 위한 보편적 인터페이스라고 주장한다.
구조화되고 조합 가능하며(LLM 입출력 포맷과 일치), 경량화되어 있고, `--help`로
자기 설명적이며, 결과가 결정론적이라는 점이 근거다.

그러나 이 주장은 MCP(Model Context Protocol)가 보편화된 환경에서는
다르게 읽힌다.
safari-mcp를 CLI로 래핑하는 실험을 진행한 Achiyacohen[^Achiyacohen]은 구체적인
수치를 측정했다. 호출당 지연 시간에서 MCP의 영구 stdio 세션은 중앙값 119ms인
반면, CLI의 서브프로세스 방식은 중앙값 3,023ms로 약 25배 느렸다. 반면 토큰
오버헤드에서는 결과가 역전된다. MCP가 84개 도구 정의를 매 API 호출에 포함하면
7,986 토큰이 소비되지만,
CLI는 `bash` 도구 정의 하나만 필요하여 95 토큰에 그친다.

이 측정은 CLI가 “경량화”되어 있다는
주장을 정확히 반박하지 않는다. CLI의 경량성은
프로세스 실행 비용이 아닌 토큰 오버헤드 관점에서 성립한다. 두 인터페이스는 서로
다른 차원에서 효율적이다.

특히 중요한 설계 원칙은 “진짜 소프트웨어
통합(Authentic Software Integration)”이다.
Blender를 제어할 때 Pillow로 이미지를 합성하는 것이 아니라, 실제 Blender를
헤드리스(headless) 모드로 실행하여 bpy API를 통해 렌더링한다. LibreOffice의
경우 ODF 파일을 생성하고 실제 LibreOffice 헤드리스로 PDF를 내보낸다. 타협 없는
실제 소프트웨어 통합이 핵심 원칙이다.

### SKILL.md 생성과 에이전트 자율 발견

Phase 6.5에서
자동 생성되는 SKILL.md는 Claude Code 스킬 시스템과 호환되는 형식이다.
CLI의 Click 데코레이터에서 메타데이터를 추출하여 YAML 프론트매터, 커맨드 그룹
문서, 사용 예시, 에이전트 특화 가이드를 포함한 파일을 생성한다. 에이전트가
`npx skills add HKUDS/CLI-Anything --list`로 전체 카탈로그를 조회하고 필요한
CLI를 설치할 수 있어, 인간의 개입 없이 소프트웨어 접근 범위를 확장할 수 있다.

### 커뮤니티 생태계와 CLI-Hub

CLI-Hub는 단순한 패키지 레지스트리를 넘어 에이전트가 자율적으로 탐색할 수 있는
도구 카탈로그다. public_registry.json을 통해 `pip`, `npm`, `brew` 등 다양한
설치 방식을 지원하며, 커뮤니티 기여 CLI와 공식 CLI를 분리하여 관리한다.
메타 스킬을 통해 에이전트가 “QGIS로 지도를 만들어줘”라는 요청을 받으면
CLI-Hub에서 `cli-anything-qgis`를 발견하고, SKILL.md를 읽고, 설치하고, 사용하는
전 과정을 자율적으로 수행할 수 있다.

## 비평

### 강점

“진짜 소프트웨어 통합” 원칙은 프로젝트의 가장 중요한 차별점이다. 대부분의
소프트웨어 자동화 도구가 UI 자동화(화면 캡처 및 클릭 시뮬레이션)나 단순화된
재구현에 의존하는 반면, CLI-Anything은 실제 소프트웨어 백엔드를 직접 호출한다.
이는 기능의 90%를 놓치는 기존 방법론과 달리 전문 소프트웨어의 전체 기능을
에이전트에게 노출한다.

HARNESS.md는 실제 소프트웨어를 실행하는 E2E 테스트를 요구하고, 백엔드가 없는
환경에서는 테스트를 건너뛰지 않고 실패시키라고 규정한다. “동작하는 척”하는
테스트를 허용하지 않는 철학이다. 다만 이 규칙이 모든 하네스에서 지켜지는지는
아래 비평에서 따로 따진다.

### 약점

7단계 파이프라인이 프론티어급 모델(Claude Opus 4.6, GPT-5.4)을 요구한다는 제약은
실질적 장벽이다. 소규모 모델로는 품질이 저하되며, 이는 고비용 API 접근을 필제
조건으로 만든다. 오픈소스 도구임에도 실제 활용은 상용 LLM 없이는 어렵다.

소스 코드가 필요하다는 제약도 범용성을 제한한다. 클로즈드 소스 소프트웨어나
바이너리만 제공되는 상용 도구는 자동 생성 품질이 크게 저하된다. 에이전트가
접근해야 하는 전문 소프트웨어의 상당수가 이 범주에 속한다.

단일 `/cli-anything` 실행으로 완성된 하네스를 얻기 어렵고 `/refine`을 여러 번
반복해야 한다는 점도 운영 비용을 높인다. 각 실행마다 프론티어 모델 API 비용이
발생하며, 소프트웨어의 복잡도에 따라 수십 번의 정제 과정이 필요할 수 있다.

MCP를 지원하는 환경에서 CLI 래핑이 과연 최선인지도 따져볼 필요가 있다.
Claude Code, Cursor,
Cline 같이 MCP를 직접 지원하는 에이전트라면 CLI 서브프로세스
오버헤드 없이 MCP 서버를 바로 연결하는 편이 지연 시간 관점에서
압도적으로 유리하다.
CLI가 정당화되는 경우는 MCP를 지원하지 않는 에이전트(Codex CLI,
GitHub Copilot CLI,
구형 프레임워크), CI/cron처럼 서브프로세스 친화적 환경, 그리고 장시간 세션에서
도구 정의 토큰 비용이 누적되는 시나리오로 좁혀진다[^Achiyacohen].

### 클로즈드 소스 소프트웨어에 대한 관점 부재

Zoom, Mailchimp 같은 클라우드 API 기반 서비스나 Sketch 같은 클로즈드 소스 소프트
웨어가 포함되어 있지만, 이 경우의 생성 방법론이 오픈소스 소프트웨어와 근본적으로
다르다. Zoom CLI는 REST API를 래핑하고, GIMP CLI는 실제 GIMP 백엔드를 호출한다.
이 두 접근 방식의 품질 차이와 한계가 문서에서 충분히 다루어지지 않는다.

### README 수치가 서로 맞지 않는다

2026-10-21 시점의 `main` 브랜치 README는 테스트 수를 네 가지로 적는다.
상단 배지는 2,461개,
그 아래 문장은 “2,461개 = 단위 1,732 + E2E 579 + Node.js 19”이고,
이 세 수의 합은 2,330이다.
요약 표의 TOTAL 줄은 2,464개인데,
같은 표의 30개 행을 직접 더하면 2,622가 나온다.
“주요 기능” 절에는 아직 “2,280+”가 남아 있다.
어느 값이 맞는지는 저장소 안에서 가릴 수 없고, 테스트를 직접 돌려 세어야 한다.

“18개 앱”이라는 표현도 낡았다.
README는 여러 곳에서 18개 애플리케이션을 말하지만,
`registry.json`에는 79개 항목이 있고
`agent-harness` 폴더를 가진 디렉터리는 69개, SKILL.md는 70개다.
저장소는 빠르게 자라고 있는데 소개 문구가 따라가지 못하는 것이다.
GIMP 하네스의 `TEST.md`는 103개,
README 표는 107개로 적어 같은 하네스에서도 값이 다르다.

테스트가 모두 실행된다는 인상도 정확하지 않다.
README의 같은 요약 표가 WaveTone에 “백엔드 필요 E2E 2개 건너뜀”,
Unreal Insights에 “9개 건너뜀”, ETH2 QuickStart에 “E2E 3개 건너뜀”이라고 적는다.
“백엔드가 없으면 건너뛰지 않고
실패시킨다”는 `HARNESS.md`의 규칙은 목표이지 모든 하네스의 현실이 아니다.

### 테스트가 통과해도 실제 소프트웨어는 호출되지 않았다

`HARNESS.md`는 “진짜 소프트웨어를 반드시 호출하라”를 첫 번째 규칙으로 두고,
GIMP를 Pillow 합성기로 대체하는 것을 대표적인 안티패턴으로 든다.
그런데 `main`의 GIMP 하네스 `core/export.py`는 먼저 GIMP의 Script-Fu 배치 모드를
시도하고, 예외가 나면 `except Exception: pass`로 삼킨 뒤 Pillow로 렌더링한다.
프로젝트에 그리기 연산이 있을 때도 곧장 Pillow 경로로 간다.
README 표가 GIMP의 백엔드를 “Pillow +
GEGL/Script-Fu”로 적은 것은 이 사정을 반영한 것이다.
외부 기여자는 GIMP 3에서 Script-Fu 호출이 타임아웃으로 멈추고,
그 뒤 Pillow가 렌더링하면서도 성공으로
보고한다는 문제를 PR로 올렸다[^issue-462].

같은 기여자는 다른 하네스에서도 같은 유형의 결함을 올렸다.
Blender의 `render execute`는 bpy 스크립트만 쓰고
명령 문자열을 돌려줄 뿐 Blender를 실행하지 않으며,
종료 코드는 0이다[^issue-459].
Audacity의 `export render out.flac`는 확장자만 `.flac`인 WAV 파일을 만들어 놓고
형식을 FLAC으로 보고한다[^issue-460].
Kdenlive에는 영상을 만드는 `export render` 명령 자체가 없는데
렌더 프리셋 목록은 보여 준다[^issue-461].
세 건 모두 백엔드 래퍼는 이미 작성되어 있는데
아무도 호출하지 않는다는 점이 같다.
나는 `main`의 Blender `core/render.py`, Audacity `core/export.py`,
Kdenlive `core/export.py`를 읽어,
이 서술이 이슈가 올라온 시점이 아니라 지금의 코드에도 해당함을 확인했다.
네 건 모두 2026-10-21 확인 시점에 병합되지 않은 PR이었다.

이 사례들은 이 프로젝트의 가장 큰 약속인 “진짜
소프트웨어 통합”이 구조적으로 검증되지 않는다는 뜻이다.
README 집계로는 단위 테스트가 E2E의 세 배가량인데, E2E가 명령 경로를 거치지 않고
백엔드 래퍼를 직접 부른다면
명령이 래퍼에 연결되어 있는지는 어느 테스트도 묻지 않는다.
에이전트는 성공 출력을 믿고 다음 단계로 가므로 오류가 조용히 번진다.

### 에이전트 효용의 증거는 아직 없다

arXiv 기술 보고서의 초록은 GUI 에이전트의 한계와 CLI 하네스의 설계를 논하고,
방법론·아키텍처·증거를 검토한다고 쓴다[^arxiv]
내가 읽은 초록에는 에이전트의 과업 성공률 같은 수치가 없다.
README의 로드맵에서도 “에이전트 과업 완료율 벤치마크 스위트” 항목이
아직 체크되지 않았고, 이를 구현하겠다는 PR은 열려 있다[^issue-366].
따라서 “UI 자동화가 계속 깨진다”는 주장과 “CLI가 더 낫다”는 주장 모두,
같은 과업에서 둘을 맞붙인 측정으로는 뒷받침되지 않는다.
측정된 비교는 앞서
본 Safari 사례처럼 외부 사용자가 MCP와 CLI 지연을 비교한 것뿐이다.

### 보안

생성된 하네스는 사용자 입력을 받아 외부
프로그램에 넘기거나 코드 문자열로 조립한다.
GIMP 하네스는 경로를 Script-Fu 문자열에 넣기 전에 따옴표와 역슬래시를
이스케이프하는 함수를 두었지만, 같은 유형의 결함이 FreeCAD에서는 보고되었다.
FreeCAD 매크로 생성기는 출력 경로를 작은따옴표로 감싸 파이썬 코드에 끼워 넣어서,
작은따옴표가 든 경로가 임의 코드를 실행시킨다는 이슈가 열려 있다[^issue-282].
에이전트가 만들거나 받은 경로 이름을 믿고 넘기는 환경에서는 현실적인 경로다.

배포 쪽 위험은 더 크다.
`cli-hub-meta-skill`은 에이전트가 라이브 카탈로그를 읽고
`pip install`로 CLI를 설치하도록 안내하는데,
그 카탈로그 주소가 서드파티 DigitalOcean Spaces 버킷이다.
2026-10-21에 내가 요청해 보니 이 주소는 `NoSuchBucket`과 함께 404를 돌려주었다.
같은 이름의 버킷을 누군가 만들면 에이전트가 읽고
따르는 지시문을 바꿔치기할 수 있다는 이슈가 열려 있다[^issue-576].
설치 전에 사용자 확인을 요구하라는 문서
보완 PR도 2026-04-08부터 병합되지 않았고[^issue-202],
내가 읽은 `main`의 메타 스킬에는 확인 지시가 없었다.
`registry.json` 79개 항목 가운데 66개는
`pip install git+https://github.com/HKUDS/...` 형태로 브랜치 고정
없이 설치되므로, 설치하는 순간의 `main`이 곧 설치되는 코드다.

REPL 모드는 작업 상태를 세션에 쌓으므로 에이전트에게 하네스를 맡긴다면
실행 권한을 좁힐 샌드박스가 필요하다.
Zoom이나 Mailchimp처럼 토큰이 필요한 하네스는 토큰을
어디에 저장하는지 하네스마다 따로 읽어 확인해야 한다.

### 함정과 체크리스트

실제로 쓸 때 부딪힐 함정은 다음과 같다.

- README 예시를 그대로 붙여 넣지 않는다. 명령 이름과
옵션은 `--help`와 해당 하네스의 `SKILL.md`로 확인한다.
- 성공 출력을 믿지 않는다. 출력 파일을 열어 형식과 크기를 확인한다.
- GIMP 3처럼 새 주 버전이 나온 소프트웨어는 하네스가 따라가지 못했을 수 있다.
- 생성기는 소프트웨어 이름만으로 동작하지
않는다. 소스 경로나 저장소 주소가 필요하다.
- 생성은 한 번으로 끝나지 않는다. `refine`을 되풀이할 비용을 예산에 넣는다.

도입 전 점검 목록은 다음과 같다.

1. 쓰려는 하네스가 CLI-Hub에 이미 있는지 먼저 `cli-hub search`로 찾았는가.
2. 해당 하네스의 `main` 코드에서 핵심 명령이 실제 백엔드를 호출하는지 읽었는가.
3. 설치할 때 커밋을 고정했는가.
4. 에이전트가 설치 명령을 실행하기 전에 사람의 확인을 거치게 했는가.
5. 결과물을 사람이나 별도 검증 스크립트가 열어 보는 단계가 있는가.

이 목록을 지키지 못하면 하네스는 “성공했다고 말하는 도구”가 된다.
반대로 위 결함이 보고된 하네스를 제외하고도,
단위 테스트가 두꺼운 하네스에서는 이 확인이 짧게 끝날 것이다.
이 결론을 뒤집을 관찰은 여러 하네스에서
명령 경로가 백엔드에 연결되어 있음을 보이는 자동 검사가 CI에 들어오는 것이다.

## 인사이트

### CLI가 에이전트 시대의 보편 인터페이스로 부활하는 역사적 아이러니

GUI의 등장이 CLI를 “전문가의 도구”로 만들었다. 마우스 클릭이 명령어 암기보다
직관적이어서, 1990년대 이후 소프트웨어 산업은 GUI를 표준으로 삼았다. 결과적으로
지난 30년간 개발된 전문 소프트웨어의 대부분은 인간의 시각 인지와 손 움직임에
최적화된 인터페이스를 갖추게 되었다.

AI 에이전트는 이 역사를 뒤집는다. 에이전트에게 GUI는 전혀 자연스럽지 않다.
픽셀을 인식하고 좌표를 계산하여 클릭을 시뮬레이션하는 것은 인간이 화면을 보고
직관적으로 반응하는 것과 근본적으로 다른 계산 과정이다. 반면 텍스트 명령어는
에이전트의 자연스러운 언어다. 파라미터를 전달하고 구조화된 출력을 받는 CLI는
LLM의 입출력 형식과 완벽하게 일치한다.

이 역전은 단순한 기술적 취향의 문제가 아니다. GUI 소프트웨어의 30년 유산 전체가
에이전트에게는 접근 불가능한 블랙박스가 될 위기에 처했다. CLI-Anything은 이
역전을 인식하고, GUI 시대에 쌓인 소프트웨어 자산 전체를 에이전트가 활용할 수
있도록 번역하는 작업을 자동화한다. 역사의 아이러니는, 미래 컴퓨팅을 지배할
인터페이스가 과거의 CLI와 닮아있다는 점이다.

### “진짜 소프트웨어 통합”이 드러내는 AI 자동화의 근본 문제

현재 AI 에이전트의 소프트웨어 통합 방식은 세 가지로 분류된다. UI 자동화(화면
보고 클릭), API 래핑(공식 API 호출), 그리고 CLI-Anything의 접근인 실제 백엔드
직접 호출이다. 각 방식은 신뢰성과 기능 완전성 사이의 트레이드오프를 갖는다.

UI 자동화는 화면이 바뀌면 즉시 깨진다. 소프트웨어 업데이트 한 번으로 수백 개의
자동화 스크립트가 무효화된다. API 래핑은 소프트웨어 제공자가 공개한 기능만
접근 가능하여, 전체 기능의 극히 일부만 활용할 수 있다. Photoshop API가 Photoshop
전체 기능의 5%를 제공한다면, 나머지 95%는 에이전트에게 존재하지 않는 기능이다.

CLI-Anything의 “진짜 소프트웨어 통합”은 이 문제를 다르게 접근한다. Blender를
bpy API로 제어하는 것은 Blender의 모든
렌더링 기능에 접근하는 것이다. LibreOffice
를 헤드리스로 실행하는 것은 LibreOffice가 지원하는 모든 문서 형식을 처리하는
것이다. 이 접근의 핵심 통찰은 소프트웨어의 “비공개 API”가 실제로는 내부 아키텍처
를 통해 접근 가능하다는 것이다. HARNESS.md의 “렌더링 갭(Rendering Gap)” 교훈이
이를 구체적으로 드러낸다. GUI가 렌더링 시점에 적용하는 효과를 CLI 레이어에서
올바르게 번역하지 않으면, 기능이 조용히 사라진다.

### 소프트웨어 에코시스템의 에이전트 네이티브 전환이 만드는 새로운 계층 구조

CLI-Anything이 성공한다면, 소프트웨어 산업에는 새로운 계층이 형성된다. 인간을
위한 GUI 레이어 위에, 에이전트를 위한 CLI 레이어가 추가된다. 이 이중 구조는
단기적으로 기존 소프트웨어 자산을 보존하면서 에이전트 활용을 가능하게 한다.

그러나 장기적으로는 더 근본적인 변화를 예고한다. 새로운 소프트웨어를 설계할 때,
개발자는 “에이전트 네이티브(agent-native)”를 처음부터 고려하게 될 것이다.
CLI 인터페이스가 GUI와 동등한 일급 시민이
되는 것이다. MCP(Model Context Protocol)
가 이 방향의 신호다. 소프트웨어가 에이전트와 상호작용하는 표준 인터페이스를
제공하는 것이 기대 사항이 되고 있다.

역사적 유사례로, 웹 API의 등장이 있다. 2000년대 초 소프트웨어들은 인간 사용자를
위한 웹 인터페이스만 가졌다. REST API 문화가 확산되면서, API 제공이 소프트웨어의
기본 요건이 되었다. “API-first” 설계가 등장했고, 이는 소프트웨어 아키텍처 전체를
바꾸었다. 에이전트 시대의 “에이전트 네이티브” 설계가 같은 역할을 할 것이다.
CLI-Anything은 그 전환기의 호환성 레이어로, 과거 소프트웨어를 미래 에이전트
에코시스템에 연결하는 다리다.

### 7단계 파이프라인의 메타적 함의: AI가 AI 도구를 만든다

CLI-Anything의 가장 흥미로운 측면은 기술적 세부사항이 아니라 그 구조적 패턴이다.
AI 에이전트(Claude Code)가 소프트웨어를 분석하고, AI 에이전트를 위한 도구(CLI
하네스)를 생성한다. AI가 자신이 사용할 도구를 스스로 만드는 메타 루프(meta-loop)
가 형성된다.

이 패턴은 소프트웨어 개발 역사에서 반복적으로 나타났다. 컴파일러가 컴파일러를
컴파일하고,
운영체제가 운영체제 도구를 실행하는 부트스트래핑(bootstrapping) 패턴이다.
AI 에이전트 생태계에서 이 패턴은 더 빠르게 확장된다. `/cli-anything:refine`으로
CLI를 개선하면, 에이전트는 더 나은 도구로 다음 세대 CLI를 더 잘 만들 수 있다.
도구의 품질이 재귀적으로 향상되는 것이다.

CLI-Hub의 메타 스킬은 이 패턴의 극단이다. 에이전트가 CLI 카탈로그를 탐색하고,
필요한 CLI를 발견하고, 설치하고, 사용하는 전 과정이 자율적이다. 에이전트가
자신의 능력 범위를 스스로 확장하는 것이다. 이는 현재 AI 에이전트의 가장 흥미로운
발전 방향 중 하나인 “자기 확장 에이전트(self-extending agent)”의 구체적 구현
사례다.

---

[^Achiyacohen]: Hacker News, [Show HN: I benchmarked MCP vs. CLI for browser automation. MCP wins by 25x](https://news.ycombinator.com/item?id=47734881), 2026-04-11
[^pypi-hub]: PyPI, [cli-anything-hub](https://pypi.org/project/cli-anything-hub/)
[^issue-462]: GitHub, [fix(gimp): stop hiding GIMP failures behind a silent Pillow fallback](https://github.com/HKUDS/CLI-Anything/pull/462), 2026-09-09
[^issue-459]: GitHub, [fix(blender): make `render execute` actually invoke Blender](https://github.com/HKUDS/CLI-Anything/pull/459), 2026-09-09
[^issue-460]: GitHub, [fix(audacity): convert non-WAV exports with SoX instead of mislabelling WAV](https://github.com/HKUDS/CLI-Anything/pull/460), 2026-09-09
[^issue-461]: GitHub, [feat(kdenlive): add `export render` so projects can actually be rendered](https://github.com/HKUDS/CLI-Anything/pull/461), 2026-09-09
[^issue-366]: GitHub, [feat(eval): cross-harness eval/benchmark framework](https://github.com/HKUDS/CLI-Anything/pull/366), 2026-06-22
[^arxiv]: arXiv, [CLI-Anything: Towards Agent-Native Computer Use](https://arxiv.org/abs/2606.03854), 2026-06-02
[^issue-282]: GitHub, [fix(freecad): code injection via unsanitized output_path in macro generation](https://github.com/HKUDS/CLI-Anything/issues/282), 2026-05-17
[^issue-576]: GitHub, [Security: “Live Catalog” points to a non-existent DigitalOcean Spaces bucket](https://github.com/HKUDS/CLI-Anything/issues/576), 2026-10-17
[^issue-202]: GitHub, [security: add user confirmation guard to meta-skill installation flow](https://github.com/HKUDS/CLI-Anything/pull/202), 2026-04-08
