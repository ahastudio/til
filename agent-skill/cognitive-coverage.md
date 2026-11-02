# Cognitive Coverage: 코드베이스를 얼마나 이해했는지 테스트 커버리지처럼 기록하는 에이전트 스킬

<https://github.com/ryannadel/cognitive-coverage>

## 소개

Cognitive Coverage는 AI 코딩 에이전트에게 설치하는 스킬이다.
README는 이를 이해를 재는 테스트 커버리지라고 소개한다.
프로젝트를 읽은 에이전트가 이해도를 기록하고 가르치고 확인하는 산출물
묶음을 만든다.
대상은 코드베이스만이 아니라 논문 모음, 문서 위키, 일반 지식 영역까지다.
GitHub Copilot, Claude Code, OpenAI Codex처럼 사용자 지침을 받는 에이전트에서 쓸
수 있다고 README는 적는다.

README가 문제로 드는 것은 인지 부채(cognitive debt)다.
시스템이 하는 일과 그 시스템을 맡은 사람이 이해한 내용 사이의 간극을 뜻한다.
README는 직접 쓴 코드는 마찰 때문에 머릿속 모델이 일부라도 생기지만,
AI가 만든 코드는 이해 없이 받아들이기 쉽다고 설명한다.
코드는 돌아가는데 그것을 설명하는 모델이 없는 상태가 쌓인다는 주장이다.

저장소는 2026년 5월 9일에 만들어졌고 마지막 푸시는 2026년 7월 15일이다.
기록 시점에 스타는 50개, 포크는 7개였고 라이선스는 MIT,
주 언어는 Python이다.[^api]

## 만들어지는 것

기본 출력 위치는 대상 프로젝트의 `cognitive-coverage/` 폴더다.

| 산출물            | 파일                                              | 내용                                                  |
| ----------------- | ------------------------------------------------- | ----------------------------------------------------- |
| Teaching Guide    | `cognitive-coverage/learning-guide.html`          | 섹션, 소스 발췌, 멘탈 모델, 수준 조절, 퀴즈           |
| Manifest          | `cognitive-coverage/cognitive-coverage.json`      | 세 축으로 이해 상태를 적은 기계 판독 목록             |
| Dashboard         | `cognitive-coverage/cognitive-coverage.html`      | 상태판, 빈 곳(gap) 분석, 가이드 링크                  |
| Artifact Launcher | `cognitive-coverage/cognitive-coverage-open.html` | 모든 산출물로 가는 시작 페이지, 생성 뒤 자동으로 열림 |

README가 말하는 세 축은 파일, 개념, 흐름이다.
코드베이스에서는 소스 파일, 알고리즘과 패턴, 데이터 흐름이 각각 해당한다.
각 축에는 상태가 세 단계 있고 예시는 `uncovered → read → understood`다.
상태 이름은 영역에 맞게 자동으로 바뀐다고 한다.

학습 수준은 두 축의 3×3이다.
난이도는 `beginner`, `intermediate`, `advanced`이고 학습자의 배경을 가정한다.
깊이는 `overview`, `standard`, `deep-dive`이고 가이드와 퀴즈에 보이는 세부
정도를 정한다.
가이드에서 난이도를 바꾸면 설명의 관점이,
깊이를 바꾸면 보이는 세부 수준이 달라지고 퀴즈도 고른 조합의 문제로 바뀐다.

프로젝트가 크면 Large Corpus Mode로 바뀐다.
전체 목록을 먼저 만들고 영역과 모듈로 묶은 뒤,
핵심 흐름, 진입점, 보안과 데이터 경계, 많이 참조되는 자료를 우선해 가르친다.
나머지는 가이드 안에 숨기지 않고 대시보드의 빈 곳으로 남긴다.
다시 돌릴 때는 `refresh:since-last-run`으로 마지막 실행 기준선과 비교해
영향받은 항목만 다시 만든다.

## 설치하고 쓰기

README는 설치 방법을 두 가지 보여 준다.

```bash
npx skills add ryannadel/cognitive-coverage --skill cognitive-coverage -g -a claude-code
gh skill install ryannadel/cognitive-coverage cognitive-coverage --agent claude-code --scope user
```

`-g`와 `--scope user`는 사용자 수준 설치이고,
빼거나 `--scope project`를 주면 현재 프로젝트에 설치한다.
설치 뒤에는 에이전트에게 이 프로젝트의 cognitive coverage를 만들어 달라고
말하면 된다.

대시보드와 가이드는 서버 없이 연결된다.
가이드의 퀴즈 답은 메모리와 localStorage에 기록되고,
제출 버튼을 누르면 결과가 대시보드 URL의 fragment로 넘어간다.
대시보드는 매니페스트의 `quizMapping`으로 그 결과를 읽어 커버리지를
다시 계산한다.
카드의 버튼으로 상태를 직접 바꾸고 갱신된 매니페스트를 JSON으로
내보낼 수도 있다.

## MCP 서버

선택 사항으로 stdio MCP 서버가 함께 들어 있다.
이미 만들어진 `cognitive-coverage.json`을 에이전트가 도구로 조회하게
하는 용도다.

```bash
uv --directory /path/to/cognitive-coverage/mcp run python server.py \
  --manifest /path/to/your/project/cognitive-coverage.json
```

README의 도구 표는 아홉 개다.

| 도구                    | 용도                                                                  |
| ----------------------- | --------------------------------------------------------------------- |
| `list_uncovered`        | 첫 상태에 머문 파일, 개념, 흐름을 나열                                |
| `list_areas`            | 큰 코퍼스의 영역과 모듈을 나열                                        |
| `get_area`              | 영역 하나와 그 안의 모듈, 묶인 항목을 반환                            |
| `next_learning_targets` | 우선순위 순으로 다음에 배울 항목을 제안, 난이도와 깊이로 거를 수 있음 |
| `get_concept`           | 개념의 설명, 파일, 퀴즈 ID, 상태를 반환                               |
| `get_flow`              | 흐름의 단계, 파일 참조, 퀴즈 ID, 상태를 반환                          |
| `coverage_summary`      | 매니페스트 요약과 한 줄 개요를 반환                                   |
| `find_by_file`          | 파일 경로를 참조하는 개념과 흐름을 반환                               |
| `mark_status`           | 항목 하나의 상태를 바꾸고 매니페스트를 원자적으로 다시 씀             |

이 문서를 쓴 환경에서는 스킬을 설치하거나 실행하지 않았다.
README만 읽었고 `skills/cognitive-coverage/SKILL.md`와 `docs/HOW-IT-WORKS.md`는
열지 않았다.

## 비평

### 이해 상태를 바꾸는 입력은 퀴즈 답과 손으로 누른 버튼이다

README가 설명하는 상태 갱신 경로는 세 가지다.
퀴즈를 제출하는 것, 카드의 버튼을 직접 누르는 것,
MCP의 `mark_status`를 부르는 것이다.
테스트 커버리지는 코드가 실행됐는지를 기계가 센다.
이 도구의 커버리지는 사람이나 에이전트가 적은 값이어서,
`understood`는 측정된 사실이 아니라 보고된 상태다.
`mark_status`를 에이전트가 부를 수 있으면,
이해하지 못한 사람 대신 에이전트가 상태를 올리는 일도 구조상 가능하다.
이는 README의 도구 설명에서 도출한 해석이다.

### 가이드와 퀴즈를 같은 에이전트가 만든다

README는 스킬이 가이드와 퀴즈를 생성한다고 설명한다.
같은 모델이 설명과 문제와 정답을 만들면 설명의 오류가 퀴즈의 정답에도
같이 들어간다.
그러면 퀴즈를 맞히는 것은 설명을 이해했다는 증거이지,
설명이 코드와 맞는다는 증거는 아니다.
README에는 생성된 퀴즈의 정확도를 따로 확인하는 절차가 나오지 않는다.
SKILL.md를 열지 않았으므로 그 안에 검증 지침이 있는지는 확인하지 못했다.

### 효과를 보인 자료가 없다

README는 인지 부채를 줄인다고 주장하지만 도입 전후의 비교나 사용 사례를
싣지 않는다.
스타 50개는 관심의 크기이고 효과의 증거가 아니다.
마지막 푸시가 2026년 7월 15일이라 이 문서의 기록일 기준으로 몇 달이
지났다.[^api]
이해도를 올리는지, 올리는 것처럼 보이게 하는지는 이 자료로 구분할 수 없다.

### 큰 프로젝트의 우선순위는 에이전트가 정한다

Large Corpus Mode는 핵심 흐름과 보안 경계를 먼저 가르친다.
무엇이 핵심인지는 스킬을 실행하는 에이전트가 판단하고,
README는 그 판단을 사람이 검토하는 단계를 말하지 않는다.
빈 곳을 대시보드에 남기는 것은 정직한 설계지만,
빈 곳의 목록이 에이전트가 고른 분류에 의존한다는 점은 남는다.

## 체크리스트

- [ ] 작은 프로젝트 하나에서 스킬을 돌려 `cognitive-coverage/` 폴더가 만들어지는가
- [ ] 생성된 가이드의 설명이 실제 코드와 맞는지 사람이 몇 곳 대조했는가
- [ ] 퀴즈의 정답이 코드에서 확인되는가
- [ ] 퀴즈를 풀지 않은 항목이 `understood`로 표시되지 않는가
- [ ] `mark_status`를 쓴다면 어떤 에이전트와 사람이 상태를 바꿀 수 있는지 정했는가
- [ ] Large Corpus Mode가 고른 우선순위를 팀이 검토했는가
- [ ] 같은 질문의 대조군, 곧 스킬 없이 읽은 사람의 이해도와 비교할 방법이 있는가

---

[^api]: GitHub, [REST API: ryannadel/cognitive-coverage](https://api.github.com/repos/ryannadel/cognitive-coverage)
