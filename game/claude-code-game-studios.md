# Claude Code Game Studios: 한 세션을 49개 에이전트의 게임 스튜디오로 바꾸는 템플릿

<https://github.com/Donchitos/Claude-Code-Game-Studios>

## 소개

Claude Code Game Studios(CCGS)는 Claude Code 한 세션에 실제 게임 스튜디오의
구조를 입히는 템플릿 저장소다.
저장소 설명은 49개 에이전트, 72개 워크플로 스킬, 스튜디오 위계를 본뜬 조율
체계를 내세우고, README는 49개 에이전트와 74개 스킬이라고 적는다.
이 문서가 트리 목록으로 센 값은 에이전트 파일 49개, 스킬 디렉터리 74개, 훅 관련
파일 18개이고, README는 규칙 14개와 문서 템플릿 62개를 든다.
저장소는 MIT 라이선스이고 2026년 2월 12일에 만들어졌으며, 2026년 10월 27일에
확인한 시점에 스타 27,691개, 포크 3,921개, 열린 이슈 67개였다.
최신 릴리스는 v1.2.0(2026년 10월 19일)이다.

만든 이유는 AI와 혼자 게임을 만들 때 채팅 한 세션에는 구조가 없다는 것이다.
매직 넘버를 하드코딩해도, 설계 문서를 건너뛰어도, 스파게티 코드를 써도 막는
사람이 없고, QA도 설계 검토도 없으며 이게 게임의 비전에 맞느냐고 묻는 사람도
없다고 README는 쓴다.
CCGS는 전문 에이전트를 스튜디오 위계로 조직해 이를 보완한다고 한다.
모든 결정은 사용자가 내리고, 에이전트는 올바른 질문을 하고 실수를 일찍 잡고
프로젝트를 정리해 준다는 것이 약속이다.

## 구성

### 세 층의 에이전트

에이전트는 세 층이다.
1층 디렉터는 creative-director, technical-director, producer다.
2층 부서장은 game-designer, lead-programmer, art-director, audio-director,
narrative-director, qa-lead, release-manager, localization-lead다.
3층 전문가는 gameplay-programmer, engine-programmer, ai-programmer,
network-programmer, systems-designer, level-designer, economy-designer,
technical-artist, sound-designer, writer, ux-designer, prototyper,
performance-analyst, security-engineer, qa-tester, accessibility-specialist
등이다.
Godot 4, Unity, Unreal Engine 5 각각에 엔진 전문가와 하위 전문가 세트(Godot는
GDScript, 셰이더, GDExtension 등)가 있어 쓰는 엔진에 맞는 세트를 고른다.

각 에이전트는 마크다운 파일의 프런트매터에 도구와 모델을 선언한다.
예로 creative-director 파일은 `model: opus`, `maxTurns: 30`, `memory: project`,
허용 도구에 Read, Glob, Grep, Write, Edit, WebSearch를 두고
`disallowedTools: Bash`를 선언한다.
README는 세 디렉터가 Opus를, lead-programmer와 전문가 열다섯 명이 Sonnet을
지정하고 나머지 서른 명은 세션의 모델을 상속한다고 밝힌다.
위계는 역할의 서열이지 요금제가 아니라고도 쓴다.

조율 규칙은 다섯 가지다.
디렉터가 부서장에게, 부서장이 전문가에게 위임하는 수직 위임,
같은 층끼리 상담은 하되 영역을 가로지르는 구속력 있는 결정은 못 하는 수평 상담,
의견 충돌은 공유 상위(설계는 creative-director, 기술은 technical-director)로
올리는 충돌 해결,
부서 간 변경은 producer가 조율하는 변경 전파,
위임 없이 자기 영역 밖의 파일을 고치지 않는 영역 경계다.

### 스킬, 훅, 규칙

스킬은 슬래시 명령이다.
온보딩(`/start`, `/help`, `/project-stage-detect`, `/setup-engine`, `/adopt`,
`/settings`), 게임 디자인(`/brainstorm`, `/map-systems`, `/design-system`),
아키텍처(`/create-architecture`, `/architecture-decision`), 스토리와
스프린트(`/create-epics`, `/create-stories`, `/dev-story`, `/story-done`,
`/sprint-plan`), 리뷰(`/design-review`, `/code-review`, `/gate-check`),
QA(`/qa-plan`, `/smoke-check`, `/test-setup`), 출시(`/release-checklist`,
`/changelog`, `/hotfix`), 여러 에이전트를 묶는 팀 오케스트레이션(`/team-combat`,
`/team-narrative`, `/team-ui`, `/team-release`)이 있다.

훅은 자동 검증이다.
`validate-commit.sh`는 커밋 전에 하드코딩된 값과 TODO 형식과 JSON 유효성과 설계
문서 섹션을 검사하고, `validate-push.sh`는 보호된 브랜치로의 푸시와 태그, 병합,
릴리스 명령에 경고한다.
`validate-read.sh`는 40KB가 넘는 설계 문서를 통째로 읽으려 하면 거부하고 제목
목록을 돌려줘서 한 섹션만 읽게 한다.
`validate-write.sh`와 `validate-registry.sh`는 규칙을 깨는 쓰기에 경고(차단은
하지 않음)하고, `validate-agent-artifact.sh`는 하위 에이전트가 지시받은 파일을
쓰지 않고 멈추면 경고한다.
`session-start.sh`, `detect-gaps.sh`, `session-stop.sh`는 세션의 시작과 끝에서
방향 확인, 빈 문서 탐지, 기록 보관을 맡고, `log-agent.sh`와
`log-agent-stop.sh`는 하위 에이전트 호출의 감사 기록을 남긴다.
권한 규칙은 force push, `rm -rf`, `.env` 읽기 같은 위험한 작업을 막는다.

경로별 규칙은 파일 위치에 따라 코딩 기준을 적용한다.
`src/gameplay/**`는 데이터 주도 값과 델타 타임 사용, UI 참조 금지를,
`src/core/**`는 핫 패스의 무할당과 스레드 안전을, `src/networking/**`는 서버
권위와 버전이 붙은 메시지를, `design/gdd/**`는 설정에 따른 필수 섹션을 요구한다.

## 사용하기

준비물은 Git, Claude Code, Python 3(모든 스킬과 훅이 `project.yaml`을 읽는다),
Bash, 권장으로 jq다.
Python이 없으면 모든 설정이 조용히 기본값으로 돌아가고, 데이터 JSON을 스테이징한
커밋만은 Python이 없으면 차단된다고 한다.

```bash
git clone https://github.com/Donchitos/Claude-Code-Game-Studios.git my-game
cd my-game
claude    # CLAUDE.md와 project.yaml이 있는 프로젝트 루트에서 시작한다
```

`src/` 같은 하위 폴더에서 시작하면 프로젝트의 훅, 거부 규칙, 확인 우선 권한
모드가 적용되지 않는다고 README가 경고한다.
세션에서 `/start`를 실행하면 아이디어 없음, 막연한 구상, 분명한 설계, 기존 작업
중 어디냐고 묻고 알맞은 흐름으로 안내한다.
아이디어가 없으면 `/brainstorm`, 엔진이 정해졌으면 `/setup-engine godot 4.7`,
기존 프로젝트면 `/project-stage-detect`로 바로 갈 수 있다.

설정은 저장소 루트의 `project.yaml`이 단일 원천이다.
가장 중요한 질문은 `modes.rigor`로 `minimal`, `standard`, `full` 중 하나이고,
여섯 개의 세부 설정(`workflow`, `docs.density`, `qa.level`, `story_granularity`,
`review_mode`, `team.size`)을 한 번에 정한다.
`minimal`(기본값)은 잼 게임 속도로 GDD가 필요 없고 문서는 짧고 QA 증거는
최소이며 혼자 검토한다.
`standard`는 GDD 필수 섹션 5개, `full`은 8개 전부와 전체 감독 검토를 요구한다.
시스템 하나만 더 엄격하게 다루는 `system_overrides`와 테스트 종류별로 증거
없음이 스토리를 막을지 경고만 할지 정하는 `testing.strict`가 있다.
`review_mode`와 `team.size`는 개인별로 `project.local.yaml`에서 덮어쓸 수 있고,
`/settings --local modes.review_mode=solo`처럼 쓴다.

```text
/settings                                  # 적용되는 설정 보기
/settings modes.rigor=full                 # project.yaml에 쓰기(팀 전체)
/settings --local modes.review_mode=solo   # project.local.yaml에 쓰기(나만)
```

스킬이나 에이전트를 고친 뒤에는 `studio-tests/`로 점검한다.
`/skill-test static`은 구조 린터(7가지 준수 검사), `category`는 범주별 품질
기준표, `spec`은 동작 명세 단언, `audit`은 스킬과 에이전트 전체의 커버리지
보고서이며, `/skill-improve`는 고치고 다시 시험해 점수가 오르면 유지하고 아니면
되돌린다.
이 시험은 프레임워크를 시험하는 것이지 게임을 시험하지 않으며, 게임 시험은
`tests/`에 둔다.

## 분석

### 위계는 설정 파일이고 강제력은 훅과 권한 규칙에 있다

49개 에이전트는 서로 다른 시스템 프롬프트와 도구 권한을 가진 마크다운 파일이다.
디렉터가 부서장에게 위임한다는 위계는 사실 프롬프트와 지시 규칙의 약속이고,
실제로 행동을 막는 것은 훅과 권한 규칙이다.
예컨대 creative-director에게 Bash 사용 금지를 선언해 두면 그 에이전트는 명령을
실행할 수 없고, `validate-commit.sh`는 하드코딩된 값이 든 커밋을 막는다.
그래서 이 템플릿의 가치는 역할극보다 훅으로 구현된 몇 가지 검사와 도구 권한의
분리에서 나온다.
이는 이 문서의 해석이다.

### 자율이 아니라 협업을 기본값으로 둔 설계다

README는 이것이 자동 조종 시스템이 아니라고 못박고 질문, 선택지 2~4개, 사용자의
결정, 초안, 승인의 순서를 요구한다.
CLAUDE.md는 에이전트가 쓰기 전에 이 파일에 써도 되느냐고 물어야 하고, 초안을
보여야 하고, 여러 파일 변경은 전체 변경 묶음의 승인이 필요하며, 사용자 지시
없이는 커밋하지 않는다고 적는다.
스킵되거나 닫힌 질문은 답이 아니므로 아무것도 하지 않고 다시 묻는다는 규칙도
있다.
이 설계는 에이전트의 능력보다 사람의 통제를 우선한다.

### 문서 양을 설정으로 조절하는 엄격도 다이얼이 핵심 발명이다

`modes.rigor`는 문서와 검증의 양을 세 단계로 압축한 손잡이다.
기본값이 `minimal`인 이유를 README는 무거운 단계가 작동하는 코드에 이르는 데 더
많이 들고 더 나은 결과를 내지 못한다는 측정 결과로 설명한다.
템플릿이 기본값을 가벼운 쪽에 두었다는 점은 템플릿 작성자가 자기 구조를 의심한
것이다.

## 비평

### 측정 결과가 정작 구조의 효용을 부정한다

README가 가장 강조하는 것은 같은 기획서로 엄격도를 달리해 네 게임을 만들고, 첫
줄의 코드 전에 쓴 문서 수를 센 측정이다.
`minimal`은 문서 1개(한 쪽짜리 기획서)와 0분, `standard`는 문서 30개와 58분이다.
모두 실행되고 시험된 게임을 냈지만 두 명의 블라인드 평가자와 사람의 플레이
테스트가 `standard` 빌드를 꼴찌로 매겼고, 추가된 문서 29개는 더 나은 게임이
아니라 추적 가능성을 샀다고 README가 쓴다.
이 정직함은 평가할 만하지만 질문을 남긴다.
49개 에이전트와 74개 스킬의 구조가 게임의 질을 높인다는 근거는 이 측정에 없다.
저장소가 입증하는 것은 구조가 무겁지 않을 때 문제가 적다는 점이다.

### 측정의 표본이 설명되지 않는다

본문은 네 게임이라고 하지만 표에는 두 줄(`minimal`, `standard`)만 있고, `full`
줄과 나머지 두 게임이 무엇인지는 보이지 않는다.
기획서는 하나이고, 평가자는 두 명이며, 평가 기준과 게임의 종류도 밝혀지지
않았다.
게임 자체는 이 저장소에 싣지 않았다고 해서 독자는 결과를 직접 볼 수 없다.
이 측정은 방향성의 증거이며 일반적 결론으로 쓰기에는 표본이 작다.

### 계층의 이름이 비용과 품질의 차이를 보장하지 않는다

README는 위계가 서열일 뿐 요금제가 아니라고 하고, 서른 명은 세션의 모델을 그대로
상속한다고 밝힌다.
따라서 art-director와 gameplay-programmer가 같은 모델로 돌 수 있고, 차이는
프롬프트와 도구 권한뿐이다.
역할 분리가 실제 성능을 높이는지(같은 모델에 역할별 프롬프트를 주는 이득)는
측정되지 않았다.

### 숫자가 맞지 않는 곳과 플랫폼의 편향이 있다

저장소 설명의 72개 스킬은 README와 트리 목록의 74개와 다르다.
훅도 README 배지는 15개이고 구조 설명은 스크립트 18개(이벤트 훅 15개와 도우미,
선택적 진단)라고 풀어 쓴다.
알림 훅 `notify.sh`는 PowerShell로 윈도우 토스트를 띄우고 다른 곳에서는 아무것도
하지 않으며, 주 개발은 윈도우 10과 Git Bash에서 이루어졌다고 밝힌다.
사소한 어긋남이지만 빠르게 바뀌는 템플릿의 문서가 코드와 따로 늙는다는 신호다.

## 인사이트

### 템플릿의 가치는 에이전트 수가 아니라 거절하는 장치의 수에서 나온다

이 저장소에서 효력이 있는 것은 읽기를 거부하는 훅, 커밋을 막는 훅, 쓰기 전에
묻는 규칙, 위험한 명령을 거부하는 권한 규칙이다.
이것들은 에이전트가 많아서가 아니라 사람이 모르고 넘어갈 순간을 막아서 가치가
있다.
에이전트를 늘리는 것은 쉽고, 거절하는 장치를 설계하는 것은 어렵다.
이 구분은 다른 에이전트 템플릿을 평가할 때도 쓸 수 있다.
이는 이 문서의 해석이다.

### 눈으로 확인하는 일을 닫는 조건으로 삼은 것이 게임에 맞는 검증이다

README는 플레이어가 보는 것을 바꾸는 스토리는 게임을 실행하고 관찰하고
스크린샷을 `production/qa/evidence/`에 남기기 전에는 닫히지 않는다고 쓴다.
파싱 검사는 실행이 아니며 화면 밖에 그려진 메뉴는 통과하는 테스트로 알 수 없다는
이유다.
`minimal`에서도 자동 테스트는 면제되지만 이 확인은 면제되지 않는다.
시각 결과물을 다루는 모든 에이전트 작업에 일반화할 수 있는 규칙이다.

### 협업 규칙은 빠르게 만드는 속도와 직접 충돌한다

모든 쓰기 전에 이 파일에 써도 되느냐고 묻고 승인을 받는 규칙은 통제를 주지만
속도를 낮춘다.
README도 `guided`와 `autonomous` 자동화 설정과 Claude Code의 자동 모드가 이
질문의 일부를 속도와 맞바꾼다고 인정한다.
엄격도와 자동화는 서로 독립된 손잡이여서, 가벼운 문서와 잦은 확인, 무거운 문서와
적은 확인이 모두 가능하다.
어느 조합이 게임을 가장 잘 만드는지는 이 저장소의 측정이 다루지 않았다.

### 이 문서를 읽는 방법

이 문서는 저장소의 README, CHANGELOG, `project.yaml`, `CLAUDE.md`,
creative-director 에이전트 파일, 트리 목록을 읽고 정리했다.
이 문서는 템플릿을 실제로 설치해 게임을 만들어 보지는 못했다.
HN, Lobste.rs, GeekNews에서 이 저장소의 스레드는 찾지 못했다.
판단을 가를 관찰은 둘이다.
하나는 같은 기획서로 `minimal`과 `full`에서 만든 게임을 같은 평가자에게
블라인드로 보였을 때 순위와 이유가 어떻게 나오는지다.
다른 하나는 같은 모델로 에이전트 하나가 역할 프롬프트 없이 같은 일을 한 경우와
비교해 역할 분리가 결과를 높이는지다.
둘 다 이 문서가 확인하지 못했다.
