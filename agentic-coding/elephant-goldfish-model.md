# Elephant-Goldfish Model: 맥락을 쥔 에이전트가 설계하고 맥락 없는 서브에이전트가 검토하는 설계 플러그인

<https://egm.dev/>

<https://github.com/google/elephant-goldfish-model>

HN 토론: <https://news.ycombinator.com/item?id=50179463> (3점, 1개 댓글)

## 소개

Elephant-Goldfish Model(EGM)은 코딩 에이전트에 붙여 쓰는 오픈소스 플러그인이다.
저장소 설명은 에이전트와 함께 소프트웨어를 설계하고 검토하기 위한 플러그인이라고
적고, 구호는 “코끼리와 설계하고 금붕어와 검토하라”이다.
코끼리(Elephant)는 프로젝트 맥락을 쥐고 명세서 초안을 쓰는 에이전트다.
금붕어(Goldfish)는 초안과 그 초안이 가리키는 소스를 대화 기록 없이 읽고
빠진 가정과 사각지대를 찾는 검토 서브에이전트다.
사람은 설계상의 절충을 정하고 명세서를 승인한 뒤에 구현을 시킨다.

2026년 11월 9일 GitHub API가 보고한 저장소는 2026년 9월 13일에 만들어졌고
별 15,352개, 포크 1,114개, 열린 이슈 88개이며 Apache-2.0 라이선스,
주 언어는 Python, 마지막 푸시는 같은 날이다.
Google 오픈소스 블로그는 2026년 10월 22일 글에서 이 플러그인이 Google 엔지니어를
위해 내부에서 개발되었고 수천 명이 매일 운영 코드를 내보내는 데 쓴다고 밝힌다.[^gblog]
홈페이지도 수천 명의 Google 엔지니어가 쓴다고 주장하지만,
README는 이것이 Google의 공식 지원 제품이 아니라고 밝힌다.
이 문서는 홈페이지, README, 저장소의 설치와 구조와 시험 문서를 읽고 정리한 것이며
직접 설치하거나 돌려 보지 않았다.
기능과 효과에 대한 서술은 모두 개발 측의 주장이다.

## 역할과 작업 순서

README는 세 역할을 이렇게 나눈다.

| 역할     | 가진 맥락                                   | 맡은 일                                            |
| -------- | ------------------------------------------- | -------------------------------------------------- |
| Elephant | 프로젝트, 요구 사항, 앞선 결정              | 문제를 탐색하고 명세서를 쓴다                      |
| Goldfish | 문서와 그것이 가리키는 소스, 앞선 대화 없음 | 빠진 가정, 불분명한 요구, 구현 위험을 찾는다       |
| 사람     | 중요한 목표와 제약                          | 절충을 정하고 설계를 승인하며 무엇을 만들지 정한다 |

기술 문서는 이 구조가 해결하려는 문제로 네 가지를 든다.
한 대화창에서 인터뷰, 설계, 코딩을 모두 하면 모델이 자기 가정을 스스로 검증하게 되는
맥락 오염, 설계 없이 가까운 파일부터 코드를 쓰는 성급한 구현,
긴 명세서와 검토 결과가 채팅을 어지럽히는 문제, 설계 문서가 코드와 어긋나는 문서
표류(drift)다.[^architecture]
이 접근의 출처로 문서는 Dave Rensin의 Medium 글을 가리킨다.
이 글은 접속 시 확인 화면이 떠서 읽지 못했다.

작업은 일곱 개 기술(skill)로 나뉘고 하나씩 따로 쓸 수 있다.

- `/egm-brainstorm`: 사람과 인터뷰한 뒤 일곱 관점의 금붕어 검토단이 가정을 공격하고, 합의한 방향을 `concepts_brief.md`에 쓴다.
- `/egm-draft`: 개념 요약을 설계 문서로 바꾸며 섹션마다 멈춰 사람의 피드백을 받는다. 홈페이지는 결과를 `docs/designs/`에 둔다고 한다.
- `/egm-review`: 다섯 단계로 검토한다. 단순함과 재사용을 보는 줌 아웃, 처음 읽는 사람의 이해 시험, 비평가의 설계 검토, 중간 줌 아웃, 구현 준비 시험이다.[^architecture]
- `/egm-resolve`: 검토 결과를 사람과 함께 처리하고 수정에 합의한다.
- `/egm-bootstrap`: 기존 코드베이스의 문서를 새로 만들거나 갱신한다.
- `/egm-review-loop`: 특정 검토 작업을 위해 구성한 검토자 그룹을 돌린다.
- `/egm-drift-report`: 저장소의 문서와 현재 소스를 비교해 어긋난 곳을 알린다.

구조는 기술(`skills/`), 금붕어 검토자의 시스템 프롬프트(`agents/`),
버전이 매겨진 문서 기준(`resources/document_standards/`), 사용 문서(`docs/`)의
네 부분이다.
검토자 페르소나로 이해, 설계 비평, 구현 준비, 코드베이스 감사, 구조 검증,
문체 편집, 창의 촉매, 종합자가 나열된다.[^architecture]

## 설치와 지원 환경

README의 설치 명령은 환경별로 다르다.

```sh
# Claude Code
claude plugin marketplace add google/elephant-goldfish-model
claude plugin install egm@egm

# Codex CLI
codex plugin marketplace add google/elephant-goldfish-model
codex plugin add egm@egm

# Antigravity CLI
agy plugin install https://github.com/google/elephant-goldfish-model
```

블로그는 이 플러그인의 핵심 목표가 EGM을 Antigravity에 들이는 것이고
다른 개발 환경은 앞으로 지원한다고 적었다.[^gblog]
ChatGPT와 Codex 데스크톱 앱은 공개된 플러그인을 설치하고,
Claude Cowork와 ChatGPT Work는 설치 안내 문서를 따른다.
설치 문서는 이 밖에 omp와 Muse 같은 환경도 표에 올렸다.[^harnesses]
플러그인 전체를 설치해야 하며 `skills/`만 복사하면 기술이 `agents/`와
`resources/`를 읽지 못해 동작하지 않는다고 한다.

금붕어 검토는 새 서브에이전트 맥락을 만들 수 있는 환경이 필요하다.
README는 에이전트가 이를 못 만들면 EGM이 검토를 멈춘다고 하고,
검토가 테스트나 사람의 판단을 대신하지 않는다고 덧붙인다.
설치 문서는 독립 실행형 Antigravity IDE를 지원하지 않는다고 적는다.
이 환경이 금붕어 검토에 필요한 새 맥락 서브에이전트 도구를 노출하지 않기
때문이다.[^harnesses]

## 시험 기록

시험 문서는 한 환경이 지원된다고 인정받는 기준을
`/egm-brainstorm`, `/egm-draft`, `/egm-review`가 플러그인 설치를 거쳐
끝까지 도는 것으로 정한다.
2026년 10월 22일 기록은 환경마다 다르다.[^testing]

- Claude Code 2.1.308은 설치와 개념 정리와 초안이 통과했고 검토는 수정 후 통과했다. 처음의 단계 순서 실패가 기록으로 남아 있다.
- Claude Cowork는 검토가 단계 5에서 7까지만 끝났고 사용량 한도가 단계 8을 끊었다. 최종 산출물과 격리된 자식 출력은 확인되지 않았다.
- Codex 0.163.0은 두 번의 실제 시험이 573.13초에 통과했고 네이티브 검토자 15개가 돌았다. 지시 파일 제외는 시험하지 않았다.
- Antigravity CLI 1.4.5는 검토자 16개가 돌았고 단계 5에서 9가 시간순으로 실행되었다. 지시 파일 제외는 시험하지 않았다.

대부분의 통과 항목에는 “fixture”라는 표시가 붙어 있다.
이슈 #237은 Antigravity CLI 1.4.0에서 프로젝트의 `AGENTS.md`와 `GEMINI.md`가,
Codex CLI 0.166.0에서 프로젝트와 사용자의 `AGENTS.md`가 검토자에게 주입된다고
보고한다.[^testing]

## 비평

### 맥락이 없다는 말은 대화가 없다는 뜻에 가깝다

홈페이지는 금붕어를 제로 맥락(zero-context) 서브에이전트라고 부르고
초안과 실제 소스 코드만 읽는다고 적는다.
README는 더 좁게 대화 기록 없이 문서와 그것이 가리키는 소스를 읽는다고 쓴다.
설계에 대한 판단은 소스와 지시 파일을 통해 얼마든지 프로젝트 맥락을 받을 수 있다.
시험 문서에 이슈 #237이 올라 있는 것이 그 증거다.
프로젝트의 `AGENTS.md`나 `GEMINI.md`가 검토자에게 들어가면
검토자는 코끼리와 같은 지침을 읽은 채 설계를 평가하게 된다.
Claude Code용 실제 시험은 검토자가 프로젝트의 `CLAUDE.md`를 보지 못하는지
확인하지만, Codex와 Antigravity는 지시 파일 제외를 시험하지 않았다고 기록한다.
격리가 환경마다 같은 강도로 성립한다고 말할 수 없다.

### 시험은 배관을 확인할 뿐 검토의 품질을 보이지 않는다

시험 기록이 확인하는 것은 설치, 격리 탐침, 단계 순서, 필요한 파일을 읽었는지,
산출물이 생겼는지다.
통과 대부분이 고정된 입력(fixture)에서 나왔다.
검토자가 실제 설계의 결함을 얼마나 찾고 거짓 경보가 얼마나 되는지,
검토를 거친 설계가 그렇지 않은 설계보다 나은 구현으로 이어지는지에 대한
수치는 이 문서가 읽은 범위에 없었다.
수천 명이 매일 쓴다는 홈페이지와 블로그의 문구는 둘 다 개발 측의 말이고
사용 자료를 달지 않았으며, README는 공식 지원 제품이 아니라고 선을 긋는다.
저장소의 별 15,352개는 관심의 크기이지 효과의 증거가 아니다.

### 한 번의 검토가 많은 서브에이전트 실행을 뜻한다

테스트에서 네이티브 검토자가 15개와 16개 돌았고,
Codex의 두 번의 실제 시험은 573초가 걸렸다.
Cowork 시험은 사용량 한도가 검토를 중간에 끊었다.
설계 하나를 다섯 단계로 검토하면 비용과 시간이 작지 않다는 신호인데,
이 문서가 읽은 문서에는 검토 한 번당 토큰이나 비용의 추정이 없다.
구독 한도나 종량 요금 아래에서 얼마나 자주 돌릴 수 있는지는 직접 재야 알 수 있다.

## 도입 전에 따져볼 것

- 쓰는 에이전트가 새 맥락의 서브에이전트를 만들 수 있는지 먼저 확인한다. 못 만들면 검토가 멈춘다.
- 프로젝트의 `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`가 검토자에게 들어가는지 환경별로 확인한다. 이슈 #237이 열려 있다.
- 작은 기능 하나로 개념 정리, 초안, 검토를 끝까지 돌려 보고 걸린 시간과 사용량을 잰다.
- 검토 결과를 누가 분류하고 어떤 기준으로 채택할지 정한다. 이 도구에서 최종 판단은 사람의 몫이다.
- 승인된 명세서를 `docs/designs/`에 두는 규칙을 따를 것인지, 기존 문서 체계와 어떻게 맞출 것인지 정한다.
- 플러그인과 환경이 모두 빠르게 바뀌므로 설치한 플러그인 버전과 에이전트 버전을 함께 기록한다.

---

[^gblog]: Google Open Source Blog, [Introducing the Elephant-Goldfish Model plugin: scaling design-driven AI software development](https://opensource.googleblog.com/2026/10/introducing-elephant-goldfish-model-plugin.html), 2026-10-22

[^architecture]: Google, [EGM Architecture & System Lifecycle](https://github.com/google/elephant-goldfish-model/blob/main/docs/designs/architecture.md)

[^harnesses]: Google, [Harnesses](https://github.com/google/elephant-goldfish-model/blob/main/docs/harnesses.md)

[^testing]: Google, [EGM Testing Playbook](https://github.com/google/elephant-goldfish-model/blob/main/TESTING.md)
