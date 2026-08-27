# GitHub Agentic Workflows

마크다운에 자연어로 지시사항을 쓰면, AI 에이전트가 GitHub Actions 위에서
실행한다. YAML을 직접 작성할 필요 없이 “무엇을 해줘”라고 쓰면 된다.

<https://github.com/github/gh-aw>

HN 토론: <https://news.ycombinator.com/item?id=46934107> (302점, 141개 댓글)

## 5분 안에 시작하기

```bash
# 설치
gh extension install github/gh-aw

# 저장소에 워크플로우 추가 (위자드가 안내)
gh aw add-wizard githubnext/agentics/daily-repo-status

# 바로 실행해보기
gh aw run daily-repo-status
```

위자드가 AI 엔진 선택(Copilot, Claude Code, OpenAI Codex, Google Gemini, Pi),
시크릿 설정, 워크플로우 배포까지 안내한다.
실행하면 저장소 활동을 분석한 리포트가 이슈로 생성된다.

## 바로 쓸 수 있는 워크플로우

`gh aw add-wizard`로 추가하면 바로 동작한다.

### 매일 저장소 리포트

```bash
gh aw add-wizard githubnext/agentics/daily-repo-status
```

열린 이슈, PR 현황, 최근 머지 등 저장소 상태를 매일 이슈로 정리해준다.

### 이슈 자동 분류

```bash
gh aw add-wizard githubnext/agentics/issue-triage
```

새 이슈가 올라오면 내용을 읽고 적절한 라벨을 붙여준다.

### CI 실패 자동 조사

```bash
gh aw add-wizard githubnext/agentics/ci-doctor
```

CI가 실패하면 로그를 분석하고 원인과 해결 방법을 코멘트로 남긴다.

### PR 자동 수정

```bash
gh aw add-wizard githubnext/agentics/pr-fix
```

CI 체크가 실패한 PR에 `/fix`를 코멘트하면 에이전트가 코드를 고쳐서 커밋한다.

### 주간 리서치

```bash
gh aw add-wizard githubnext/agentics/weekly-research
```

관련 업계 동향과 기술 트렌드를 매주 조사해서 정리한다.

### 그 외

- **daily-plan** - 이슈 기반 일일 계획 수립
- **daily-team-status** - 팀 활동 요약
- **repo-ask** - `/ask`로 저장소에 대해 질문
- **code-simplifier** - 코드 가독성 개선
- **test-coverage-improver** - 테스트 커버리지 확대
- **dependabot-pr-bundler** - Dependabot PR 통합

전체 목록: <https://github.com/githubnext/agentics>

## 직접 워크플로우 만들기

`.github/workflows/`에 마크다운 파일을 만든다. 프론트매터에 설정, 본문에 자연어
지시사항을 쓴다.

```markdown
---
description: PR에 접근성 리뷰를 수행합니다
on:
  pull_request:
    types: [opened, synchronize]
engine: copilot
tools:
  bash: ["gh pr diff"]
safe-outputs:
  - pull-request-reviews
---

# Accessibility Review

이 PR의 변경사항에서 접근성 문제를 확인하세요.

## 확인 항목

- alt 텍스트 누락
- 색상 대비 부족
- 키보드 네비게이션 지원 여부
- ARIA 속성 적절성

## 결과

문제가 있으면 PR 리뷰 코멘트로 남기세요. 문제가 없으면 승인하세요.
```

```bash
# 마크다운 → YAML 컴파일
gh aw compile

# 테스트 (임시 저장소에서 안전하게)
gh aw trial accessibility-review

# 커밋 & 푸시
git add .github/workflows/accessibility-review.*
git push
```

## 트리거 패턴

### 스케줄 (정기 실행)

```yaml
# 퍼지 구문 - 시간을 자동 분산
on: daily
on: weekly on monday

# 크론 구문
on:
  schedule:
    - cron: "0 9 * * 1-5"
```

### 이벤트 (이슈/PR)

```yaml
on:
  issues:
    types: [opened, labeled]

on:
  pull_request:
    types: [opened, synchronize]
```

### 슬래시 커맨드 (ChatOps)

```yaml
on:
  slash_command:
    name: review
    events: [pull_request_comment]
```

이슈나 PR에 `/review`를 코멘트하면 실행된다.

## 코딩 에이전트로 워크플로우 생성

직접 마크다운을 쓰지 않아도 된다. 코딩 에이전트에게 다음과 같이 프롬프트하면
워크플로우를 생성해준다.

```
Create a workflow for GitHub Agentic Workflows
using https://raw.githubusercontent.com/github/gh-aw/main/create.md

The purpose of the workflow is to automatically
review PRs for security vulnerabilities.
```

## 보안

에이전트는 기본적으로 읽기 전용이다. 쓰기 작업은 Safe Outputs라는 구조를 통해
별도 잡(job)에서 검증 후 실행된다. 에이전트가 직접 저장소를 수정할 수 없다.

- 네트워크 격리 및 도메인 허용 목록
- 의존성 SHA 고정
- 위협 탐지 잡이 출력을 사전 검사
- `roles` 필드로 실행 권한 제한 가능

보안 경계를 강화하는 동반 프로젝트도 함께 배포된다.
Agent Workflow Firewall(AWF)는 네트워크 이그레스를 통제하고,
MCP Gateway는 Model Context Protocol 라우팅을 담당하며,
`gh-aw-actions`는 공유 커스텀 액션 라이브러리를 제공한다.
그럼에도 README는 “에이전트형 워크플로우는 보안과 사람의 감독에 세심한
주의가 필요하고, 그렇게 해도 여전히 잘못될 수 있다.
주의해서 각자의 책임으로 사용하라”고 명시한다.

저장소는 별 5,000개 이상, 커밋 17,000개가 넘는 활발한 프로젝트지만
아직 실험적이다.
0.68.4부터 0.71.3까지의 릴리스는 과금에 영향을 주는 버그로 회수되었고,
해당 버전 사용자는 즉시 최신 버전으로 올리라는 공지가 붙어 있다.

## 분석

### 이 도구의 핵심은 YAML 제거가 아니라 안전 경계다

README의 첫 문장은 “YAML을 직접 작성할 필요 없이 무엇을 해줘라고 쓰면
된다”고 내세운다.
그러나 실제로는 자연어 마크다운이 `gh aw compile`을 거쳐
`.lock.yml`이라는 표준 GitHub Actions 워크플로우로 컴파일되고,
배포 전에 그 산출물을 검토하라고 권한다.
그러면 YAML은 사라진 것이 아니라 한 겹 아래로 옮겨졌을 뿐이다.
자연어는 소스이고 YAML은 컴파일 결과물이며,
프론트매터 자체도 여전히 YAML이다.

그래서 이 프로젝트가 진짜로 파는 것은 “YAML을 안 써도 됨”이 아니라
“비결정적 에이전트를 CI에 넣되 사고를 막는 구조”다.
그 구조의 핵심이 Safe Outputs다.
에이전트는 기본적으로 읽기 전용으로 돌고,
쓰기 작업은 에이전트 잡 바깥의 별도 잡에서 버퍼링·검증된 뒤 적용된다.
에이전트가 저장소를 직접 건드릴 수 없다는 이 경계가
자연어 인터페이스보다 훨씬 본질적인 기여다.
직접 써 본 `r2vcap`도 LLM 호출과 적용 단계를 분리한 것이
이 도구의 진짜 장점이라며,
기존 결정적 워크플로우를 대체하는 게 아니라
LLM 사용을 더 안전하게 유지하면서 자동화 범위를 넓히는 보완재라고 짚었다.[^r2vcap]
가드레일 없이 Codex나 Claude Code를 GitHub Action 안에서 직접 돌리면
자격 증명이 새거나 안전하지 않은 쓰기가 실행될 위험이 있는데,
Safe Outputs는 바로 그 위험을 막는 층이다.

### GitHub Actions 위에 얹은 이유는 인프라 재사용이다

에이전트를 굳이 GitHub Actions 위에서 돌리는 선택은 우연이 아니다.
Actions는 이미 저장소별 시크릿 관리, 토큰 스코프, 이벤트 트리거,
권한 모델, 로그 보존을 갖추고 있다.
에이전트를 CI에 올리면 이 인프라를 그대로 물려받는다.
`on: issues`, `on: pull_request`, `slash_command` 같은 트리거는
Actions가 이미 아는 이벤트를 자연어 워크플로우에 연결하는 얇은 층이다.

이 선택은 “Actions + Agent + Safety”라는 프로젝트의 자기 규정과 맞물린다.
에이전트가 새로 발명한 것은 추론 능력뿐이고,
실행 환경·권한·트리거는 전부 기존 CI에서 빌려 온다.
그래서 이 도구는 새로운 런타임이 아니라
기존 런타임에 판단력을 더하는 어댑터에 가깝다.

### 마크다운을 컴파일한다는 발상

소스를 마크다운으로 쓰고 실행 아티팩트로 컴파일하는 패턴은
정적 사이트 생성기나 Dockerfile과 같은 계보에 있다.
선언적 소스를 사람이 읽고,
빌드 단계가 그것을 실행 가능한 형태로 바꾸며,
결과물은 재현 가능하도록 SHA로 고정된다.
`gh aw compile`이 `.lock.yml`을 만드는 것은 lockfile 관행 그대로다.
흥미롭게도 `clarkdale`은 이 워크플로우 lock 파일 개념이
GitHub Actions에는 원래 없던 것이라며,
태그 참조가 바뀌어 생기는 보안 위험을 막아 줄
빠져 있던 기능을 이 프로젝트가 사실상 채워 넣은 셈이라고 봤다.[^clarkdale]
자연어 컴파일이라는 겉모습보다,
액션 참조를 고정하는 lock 파일 관행을 GHA 생태계에 들여온 것이
더 실질적인 보탬일 수 있다는 관점이다.

다만 결정적으로 다른 점이 있다.
정적 사이트나 컨테이너는 같은 소스에서 같은 결과를 낸다.
반면 여기서 컴파일된 워크플로우가 호출하는 것은 비결정적 에이전트다.
lockfile은 워크플로우의 뼈대를 고정할 뿐,
그 안에서 LLM이 무엇을 판단할지는 고정하지 못한다.
재현성의 경계가 코드에서 끝나고 판단에서 무너지는 것이다.

## 비평

### “YAML 없이”라는 약속은 추상화가 아니라 한 겹 추가다

자연어로 쓰면 된다는 약속은 검토 부담을 없애 주지 않는다.
컴파일된 `.lock.yml`을 배포 전에 읽으라고 문서가 요구하기 때문이다.
그러면 사용자는 자연어 소스와 생성된 YAML 두 가지를 모두 이해해야 한다.
YAML을 안 봐도 되는 게 아니라,
자연어와 YAML의 대응 관계까지 새로 배워야 한다.

이것은 추상화의 전형적 실패 지점이다.
좋은 추상화는 아래 계층을 감춰서 몰라도 되게 만든다.
그러나 CI 워크플로우처럼 잘못되면 권한이 새거나 비용이 터지는 영역에서는
아래 계층을 감출 수 없다.
결국 자연어는 편의 문법이지 추상화가 아니며,
문서 스스로 컴파일 결과 검토를 의무화함으로써 그 점을 인정한다.

`woodruffw`가 이 이중 부담을 구체적 물음으로 바꿔 놓았다.
왜 마크다운과 생성된 워크플로우를 둘 다 저장소에 넣어야 하는지,
변경이 필요할 때 늘 마크다운에서 다시 생성해야 하는지가 불분명하다는 것이다.[^woodruffw]
LLM이 CI/CD 워크플로우를 만드는 것을 돕는 가치는 이해하지만,
왜 CI/CD에 LLM이 지속적으로 관여해야 하는지는 설득되지 않는다고 덧붙였다.
소스와 산출물을 모두 버전 관리해야 하는 순간,
자연어 한 벌로 끝난다는 약속은 이미 깨진다.

### 보안 모델은 위험을 없애지 않고 옮긴다

Safe Outputs는 에이전트의 쓰기를 별도 잡에서 검증한다.
그러나 검증 잡이 무엇을 걸러낼 수 있는지가 관건이다.
prompt injection으로 에이전트가 그럴듯하지만 악의적인 출력을 만들면,
그 출력이 스키마상 유효한 PR 코멘트나 라벨인 한
검증 잡은 형식은 통과시키고 의도는 판별하지 못할 수 있다.
경계는 “에이전트가 직접 못 쓴다”까지는 보장하지만
“에이전트가 시킨 대로만 쓴다”는 보장하지 못한다.

0.68.4부터 0.71.3까지 과금 버그로 회수된 사건이 이 한계의 실물이다.
보안 경계가 아무리 촘촘해도,
비결정적 시스템을 CI에 올리면 예측 못 한 실패 양식이
비용이라는 전혀 다른 축에서 터질 수 있다.
Safe Outputs는 저장소 쓰기라는 한 축은 지키지만,
토큰 소비·과금·무한 루프 같은 축은 같은 방식으로 지켜지지 않는다.

`kaicianflone`이 이 한계를 가장 정확히 언어화했다.
권한·샌드박스·MCP 허용 목록·출력 정제 같은 실행 안전은 모두 중요하지만,
더 어렵고 아직 풀리지 않은 문제는 실행 제약이 아니라 결정 검증이라는 것이다.[^kaicianflone]
실제 실패의 대부분은 에이전트가 권한 안에서
허가되었으나 틀린 일을 높은 확신으로 저지르는 데서 온다.
환각, 얕은 동의, 속도를 위해 정확성을 희생하는 판단은
권한 상자 안에 머무르므로 Safe Outputs가 걸러 내지 못한다.

이 지적이 추상적이지 않다는 증거가 같은 저장소에 이미 남아 있다.
`onionisafruit`은 dependabot이 만든 버전 업그레이드 이슈가
copilot 에이전트를 촉발해 생긴 미심쩍은 PR을 찾아냈다.[^onionisafruit]
에이전트는 그 업그레이드를 `go.mod`에
`replace` 문을 넣는 잘못된 방식으로 구현했고,
관련 없어 보이는 변경까지 섞어 넣었다.
권한은 정상이었고 쓰기도 검증 잡을 통과했지만,
결정 자체가 틀렸다.
이것이 kaicianflone이 말한 “허가되었으나 틀린 일”의 실물이다.

### 공식 배포와 “각자 책임” 경고의 긴장

이 저장소는 `github/` 조직 아래 공식으로 배포된다.
동시에 README는 “각자의 책임으로 사용하라”고 밝힌다.
공식 조직의 이름은 신뢰를 주지만,
책임 고지는 그 신뢰를 사용자에게 되돌린다.
별 5,000개와 커밋 17,000개라는 성숙해 보이는 지표와,
버전 리콜과 실험 딱지가 한 저장소 안에 공존한다.

이 긴장은 사용자에게 실질적 함정이 된다.
공식 배포라는 신호를 보고 프로덕션 저장소에 붙였다가,
아직 안정화되지 않은 도구의 과금 버그를 뒤집어쓸 수 있다.
성숙도 지표와 안정성은 다른 문제인데,
전자가 후자를 암시하는 것처럼 읽히기 쉽다.

보안을 앞세운 자기 규정에 대한 회의도 날카로웠다.
README가 “강력한 가드레일과 보안 우선 설계 원칙”을 내세우자,
`amluto`는 GitHub Actions야말로
보안 우선 설계 원칙을 알아볼 것이라고 가장 믿기 어려운 조직이라고 받아쳤다.[^amluto]
`woodruffw`도 GHA의 근본적 약점을 먼저 손보는 편이 낫겠다고 했다.
GHA의 기존 보안 평판이 이미 미덥지 않은 상황에서,
그 위에 비결정적 에이전트를 얹으면서 보안 우선을 표방하는 것은
평판의 빚을 새 기능으로 갚으려는 시도로 읽힌다.

`gh aw init`을 실제로 눌러 본 사용자의 경험이 이 불신을 뒷받침한다.
`onionisafruit`은 잘못된 프롬프트에서 Y를 누르자
자기 계정 토큰으로 저장소에 `COPILOT_GITHUB_TOKEN`이 만들어졌다고 적으며,
이런 동작에는 별도의 추가 확인이 있어야 한다고 지적했다.[^onionisafruit-init]
컴파일된 워크플로우가 무엇을 하는지 이해하려면
LLM에게 다시 물어봐야 하는 1,000줄짜리 파일이라는 점도 함께 꼬집었다.

## 인사이트

### 에이전트를 CI에 넣으면 비용이 커밋 빈도에 연동된다

전통적 CI의 비용은 대체로 예측 가능하다.
빌드와 테스트는 정해진 작업량을 소모한다.
그러나 에이전트가 매 이벤트마다 추론을 돌리면,
비용은 실행 횟수 곱하기 토큰 소비로 바뀐다.
이슈가 열릴 때마다, PR이 갱신될 때마다,
`/fix` 코멘트가 달릴 때마다 LLM 호출이 발생한다.

0.68.4부터의 과금 버그가 그토록 심각하게 다뤄진 이유가 여기 있다.
결정적 CI에서 버그는 잘못된 결과를 낳지만,
비용 축에서 도는 에이전트의 버그는 청구서를 낳는다.
저장소 활동이 활발할수록 노출이 커지므로,
가장 바쁜 저장소가 가장 크게 물린다.
이 도구를 도입하는 조직은 워크플로우 로직만이 아니라
이벤트 빈도에 연동된 비용 곡선을 함께 설계해야 한다.

### 재현성의 경계가 코드에서 판단으로 이동한다

lockfile과 SHA 고정은 소프트웨어 공급망 신뢰의 기둥이었다.
같은 lockfile이면 같은 의존성,
같은 의존성이면 같은 빌드라는 사슬이 재현성을 지탱했다.
gh-aw는 이 관행을 워크플로우에 그대로 가져와 `.lock.yml`을 고정한다.
그러나 고정되는 것은 워크플로우의 구조뿐이고,
그 안에서 LLM이 내리는 판단은 고정 대상 밖에 있다.

이는 재현성 개념 자체가 이동하고 있음을 보여 준다.
“같은 입력이면 같은 출력”이라는 정의는
결정적 코드에서는 성립하지만 에이전트에서는 성립하지 않는다.
공급망 보안이 어렵게 세운 재현성의 사슬이
마지막 고리인 에이전트 판단에서 끊기는 것이다.
lockfile이 주는 안심이 실제 보장 범위를 넘어서 읽히기 쉽다는 점이,
에이전트를 인프라에 통합할 때 반복될 함정이다.

### 완전 자동화할수록 검증이 느슨해지는 역설

Safe Outputs의 설계 철학은 “읽기는 자유, 쓰기는 검증”이다.
그런데 검증의 상당 부분이 결국 사람의 검토로 수렴한다.
컴파일된 YAML을 배포 전에 읽고,
`roles`로 권한을 좁히고,
위협 탐지 잡의 판정을 확인하는 일은 모두 사람의 몫이다.
자동화가 약속하는 것은 사람의 개입을 줄이는 것인데,
안전을 지키는 방법은 사람의 개입을 유지하는 것이다.

이 역설은 에이전트형 도구 전반에 걸친 구조적 함정이다.
자율성을 높일수록 검증 지점이 줄고,
검증이 줄수록 돌이키지 못하는 사고의 위험이 커진다.
gh-aw가 읽기 전용 기본값과 별도 검증 잡으로 이 함정을 늦추려 하지만,
사용자가 편의를 좇아 검토를 건너뛰고 권한을 넓히는 순간
그 안전장치는 무력해진다.
결국 이 도구의 안전성은 코드가 아니라
사용자가 자동화의 유혹에 얼마나 저항하는가에 달려 있다.

이 회의는 도구의 존재 이유 자체로도 번진다.
`CuriouslyC`는 사람들이 이미 쓰는 시스템을 에이전트와 더 잘 맞물리게 만드는 대신
에이전트를 어울리지 않는 곳에 밀어 넣었다며
마케팅이 이끄는 현금 확보라고 잘라 말했다.[^CuriouslyC]
`jrjeksjd8d`는 더 넓은 구도로 읽어,
쓰는 클라우드 제품마다 원치 않는 주변 기능이 쌓이는 동안
핵심 기능은 정체하거나 오히려 나빠진다고 했다.[^jrjeksjd8d]
회사가 성장을 위해 개발자를 계속 뽑지만
그들이 모두 핵심 제품에 붙을 수는 없어 신규 그린필드를 만든다는,
콘웨이의 법칙에 가까운 진단이다.
GHA 로그 뷰어부터 고쳐 달라는 요청이 스레드에 반복되는 것과 겹쳐 보면,
이 도구가 사용자가 가장 아쉬워하는 지점이 아니라
조직이 성장을 보여야 하는 지점에서 나왔다는 의심을 부른다.

---

[^r2vcap]: <https://news.ycombinator.com/item?id=46938171>
[^clarkdale]: <https://news.ycombinator.com/item?id=46935095>
[^woodruffw]: <https://news.ycombinator.com/item?id=46935569>
[^kaicianflone]: <https://news.ycombinator.com/item?id=46936740>
[^onionisafruit]: <https://news.ycombinator.com/item?id=46936733>
[^amluto]: <https://news.ycombinator.com/item?id=46938715>
[^onionisafruit-init]: <https://news.ycombinator.com/item?id=46936354>
[^CuriouslyC]: <https://news.ycombinator.com/item?id=46935883>
[^jrjeksjd8d]: <https://news.ycombinator.com/item?id=46944464>
