# Opus 5.5가 긴 작업을 끝내게 하는 재사용 하니스 7층

트윗: [Make Opus 5.5 Finish Long Tasks: A Reusable Harness Engineering Setup](https://twitter.com/beamnxw/status/2107522996046905797)

## 소개

beamnxw가 2026-10-07에 올린 8분 분량의 Twitter 아티클이다.
긴 작업이 끝나지 않은 채 예산만 쓰는 일을 막으려면, 작업을 시작하기 전에 하니스를 먼저 갖추라는 글이다.
저자는 하니스를 모델 둘레의 지시, 도구, 권한, 상태, 검사를 조율하는 것이라고 정의하고,
Claude Code의 문서화된 기능으로 일곱 층을 쌓는다.
예시는 문서 작업이다.
참고 자료는 `sources/`, 초안은 `drafts/`, 승인된 파일은 `published/`에 둔다.

일곱 층은 다음과 같다.

| 층  | 무엇을 하는가                             | 놓는 곳                               |
| --- | ----------------------------------------- | ------------------------------------- |
| 1   | 작업 공간의 사실과 규칙을 둔다            | `CLAUDE.md`                           |
| 2   | 반복하는 절차를 저장한다                  | `.claude/skills/write-draft/`         |
| 3   | 원천 자료에 접근하는 길을 연다            | MCP 연결(선택)                        |
| 4   | 행동 규칙을 실행 계층에 둔다              | `.claude/settings.json`               |
| 5   | 검토자가 증거를 돌려주게 한다             | `.claude/agents/evidence-reviewer.md` |
| 6   | 일의 성격에 맞춰 추론 노력을 정한다       | `--effort`, frontmatter               |
| 7   | 실행이 무엇을 증명해야 끝나는지 말해 준다 | `/goal`                               |

글의 핵심 주장은 두 가지다.
한 가지는 완료를 열어 볼 수 있는 산출물과 점검할 수 있는 증거로 정의하라는 것이다.
다른 한 가지는 다음 날 이어서 할 수 있게 진행 상황을 파일에 남기라는 것이다.
이 노트는 글의 설정을 공식 문서와 맞춰 보고, 글이 말하지 않은 실패 조건을 덧붙인다.

## 동작 방식

### 일곱 층은 각기 다른 시점에 로드된다

| 층               | 언제 컨텍스트에 들어오는가                                                                               |
| ---------------- | -------------------------------------------------------------------------------------------------------- |
| `CLAUDE.md`      | 세션 시작에 로드된다. 하위 디렉터리의 `CLAUDE.md`는 그 디렉터리의 파일을 읽거나 쓸 때 로드된다.[^memory] |
| `.claude/rules/` | `paths` frontmatter가 없으면 시작에 로드되고, 있으면 해당 파일을 다룰 때 로드된다.[^memory]              |
| 스킬             | 글에 따르면 호출할 때 전체 지시가 로드된다.                                                              |
| 서브에이전트     | 자기 컨텍스트 창에서 돈다. 대화 기록과 이미 읽은 파일을 보지 못한다.[^subagents]                         |

글은 `@path` 임포트를 “정리용”으로만 쓰라고 한다.
공식 문서도 임포트한 파일은 그것을 부른 `CLAUDE.md`와 함께 컨텍스트에 들어가므로 파일을 쪼개는 것이 컨텍스트를 줄여 주지는 않는다고 적는다.[^memory]
가끔만 쓰는 절차는 임포트가 아니라 스킬에 둔다는 글의 조언이 이 사실에 근거한다.

### 권한은 도구 경계에서 걸리고, 그 경계에는 구멍이 있다

글의 `settings.json`은 `.env` 읽기와 `published/**` 편집을 막는다.
`Read`와 `Edit` 거부 규칙은 Claude의 내장 파일 도구와, `cat`, `sed`, `tee`처럼 Claude Code가 알아보는 파일 명령, 리디렉션 대상에 적용된다.[^permissions]
이름을 대지 않고 파일을 읽는 명령이나, 스스로 파일을 여는 Python, Node 스크립트 같은 임의의 하위 프로세스에는 적용되지 않는다.[^permissions]
모든 프로세스를 막으려면 샌드박스를 켜야 한다고 문서가 적는다.[^permissions]
글도 같은 한계를 짚으며 운영체제 샌드박스가 필요하다고 쓴다.

### 목표 평가자는 대화에 드러난 것만 본다

`/goal`은 완료 조건을 세우고, 매 턴이 끝날 때 작은 빠른 모델이 조건이 충족됐는지 판정한다.[^goal]
충족되지 않았으면 Claude가 다음 턴을 시작하고, 충족되었거나 불가능하다고 판정되면 목표가 지워진다.[^goal]
평가자는 명령을 실행하거나 파일을 읽지 않고, Claude가 대화에 드러낸 것만 판단한다.[^goal]
글이 “경로와 검증 결과가 대화에 나타나야 한다”를 완료 조건에 넣은 이유가 여기에 있다.

턴을 제한하는 문구는 조건 안에 “20턴 뒤에 멈춘다” 같은 절을 넣는 방식이며, 이 절도 평가자가 대화로 판단한다.[^goal]
글이 “턴 절은 모델이 평가하는 것이어서 엄격한 한도에는 실행 제어가 필요하다”고 쓴 대로다.

### 노력 수준은 층마다 따로 정할 수 있다

Opus 5.5의 기본값은 `medium`이고, `--effort`는 한 세션의 수준을 정한다.[^model-config]
스킬과 서브에이전트의 frontmatter에 `effort`를 적으면 그것이 활성인 동안 세션 수준을 덮어쓰고, 환경 변수 `CLAUDE_CODE_EFFORT_LEVEL`은 덮어쓰지 못한다.[^model-config]
서브에이전트 문서도 `effort`에 `low`, `medium`, `high`, `xhigh`, `max`를 쓸 수 있고 모델에 따라 가능한 수준이 달라진다고 적는다.[^subagents]
글이 메인은 `medium`으로 두고 검토자만 `high`로 올린 구성이 이 규칙 위에서 성립한다.

## 구현하기

글의 파일 네 개를 그대로 쓰되, 앞에서 확인한 구멍을 메우는 허용 규칙은 이 노트가 덧붙인다.
아래 점검 스크립트는 파일이 갖춰졌는지만 확인하고, 모델이나 권한 동작은 확인하지 않는다.

```bash
#!/usr/bin/env bash
# 하니스 7층 중 파일로 확인할 수 있는 부분을 점검한다
set -u
fail=0
need() { [ -e "$1" ] && echo "ok   $1" || { echo "MISS $1"; fail=1; }; }

for d in sources drafts published; do need "$d"; done
need CLAUDE.md
need .claude/skills/write-draft/SKILL.md
need .claude/agents/evidence-reviewer.md
need .claude/settings.json

# 스킬은 $ARGUMENTS를 받아야 새 주제에 재사용된다
grep -q '\$ARGUMENTS' .claude/skills/write-draft/SKILL.md 2>/dev/null \
  && echo "ok   skill uses \$ARGUMENTS" || { echo "MISS \$ARGUMENTS"; fail=1; }

# settings.json이 올바른 JSON이고 published 편집을 막는지
python3 - <<'PY' || fail=1
import json
deny = json.load(open(".claude/settings.json")).get("permissions", {}).get("deny", [])
print("ok   deny Edit(published/**)" if "Edit(published/**)" in deny
      else "MISS deny Edit(published/**)")
assert "Edit(published/**)" in deny
PY
exit $fail
```

빈 디렉터리에서는 `MISS`가 줄줄이 나오고 종료 코드가 1이며, 글의 파일을 모두 만든 뒤에는 전부 `ok`에 종료 코드 0이 나온다.
이 스크립트를 두 상태에서 실제로 돌려 확인했다.

## 값 정하기

| 값          | 글의 시작값   | 근거와 바꿀 때                                                        |
| ----------- | ------------- | --------------------------------------------------------------------- |
| 메인 노력   | `medium`      | Opus 5.5의 기본값이다.[^model-config] 수정이 많이 필요하면 올린다     |
| 검토자 노력 | `high`        | 애매한 주장을 가려야 하는 일이다. 오탐이 많으면 낮추고 근거 표를 본다 |
| 턴 상한     | 12턴          | 글의 예시다. 근거는 없으니 첫 실행의 실제 턴 수를 보고 정한다         |
| 조건 길이   | 한 문단       | `/goal` 조건은 4,000자까지다.[^goal]                                  |
| 보관 파일   | `progress.md` | 현재 파일, 끝낸 검사, 열린 문제, 다음 행동 한 가지를 적는다           |

턴 상한과 노력 수준은 작업을 한 번 돌려 본 뒤에 고치는 값이다.
글도 같은 입장이어서, 한 번에 한 요소만 바꾸고 같은 작업을 다시 돌려 저장된 결과와 증거를 비교하라고 한다.

## 트레이드오프

### 기본 차단은 무인 실행을 멈춘다

글의 `settings.json`에는 거부 규칙만 있고 허용 규칙이 없다.
`/goal`은 권한 모드를 바꾸지 않는다.
공식 문서는 수동 모드에서는 설정이 이미 허용하지 않은 도구 호출 앞에서 Claude가 여전히 묻는다고 적고, 무인으로 돌리려면 자동 모드에서 `/goal`을 쓰라고 한다.[^goal]
그래서 글의 구성은 검토자가 `WebSearch`와 `WebFetch`를 부르고 메인이 파일을 쓸 때마다 사람의 승인을 기다릴 수 있다.
이것은 글이 말하지 않은 간극이며, 12턴 상한이 있어도 승인 대기는 턴이 아니라 시간을 쓴다.

대신 허용 규칙을 넓게 열면 거부 규칙이 막는 범위가 상대적으로 의미를 잃는다.
깔끔한 해법은 없다.
읽기와 검색은 허용하고 쓰기는 `drafts/`로 좁혀 허용하는 식으로, 위험이 작은 쪽부터 열어야 한다.

### 검토자가 읽기 전용이면 근거 표가 쓰는 일은 메인에 남는다

글의 `evidence-reviewer`는 `Read, Grep, Glob, WebSearch, WebFetch`만 가진다.
검토자는 표를 돌려줄 뿐 `drafts/checks.md`를 직접 쓰지 못하고, 표를 파일로 저장하는 단계는 메인이 맡는다.
이 설계의 이점은 검토자가 초안을 고치지 못한다는 점이다.
대가는 검토 결과가 요약으로 메인에 돌아오면서 증거가 줄어들 수 있다는 점이다.
서브에이전트가 자기 컨텍스트에서 일하고 요약만 돌려준다는 것이 문서의 설명이다.[^subagents]
그래서 표의 각 줄이 열어 본 URL을 담게 한 글의 형식이 이 손실을 막는 장치다.

### 샌드박스를 켜면 도구 호환이 줄어든다

파일 도구 규칙의 구멍을 메우려면 샌드박스가 필요하다.
다만 샌드박스는 셸 명령의 파일 시스템과 네트워크 접근을 운영체제 수준에서 제한하므로,
검토자가 웹을 읽거나 MCP 도구를 쓰는 경로와 부딪힐 수 있다.
이 노트는 샌드박스 설정을 읽지 않았고, 부딪히는지 판단하지 못한다.

## 함정

### 같은 설정을 두 번 쓰지 않는다

글은 `claude --model claude-opus-5-5 --effort medium`을 실행하라고 하는데,
같은 글과 공식 문서가 Opus 5.5의 기본값이 `medium`이라고 적는다.[^model-config]
이 명령은 기본값을 다시 적은 것이라 효과가 없다.
기본값을 확인하는 용도로 읽으면 맞고, 노력 수준을 낮춘 것으로 읽으면 틀린다.

### 사용자 설정의 `effortLevel`은 Opus 5.5에 적용되지 않는다

공식 문서는 사용자 설정 파일의 최상위 `effortLevel`이 Opus 5.5에서는 계산되지 않는다고 적는다.[^model-config]
설정 파일에 `effortLevel`을 넣고 `medium`을 바꿨다고 믿으면 틀린다.
바꾸려면 `--effort`, 환경 변수, `/effort`, 또는 frontmatter를 써야 한다.

### 임의 프로세스는 거부 규칙을 우회한다

`Edit(published/**)`는 내장 파일 도구를 막는다.
Claude가 Bash로 Python 스크립트를 짜서 `published/`에 쓰면 이 규칙이 막지 못한다.[^permissions]
글이 제안한 확인법, 곧 더미 문서를 만들고 파일 편집 도구로 고치게 해 거부되는지 보는 방법은 내장 도구 경로만 검사한다.
Bash 경로는 따로 시험해야 한다.

### 평가자가 보지 못하는 것은 완료로 인정되지 않는다

완료 조건에 파일이 존재해야 한다고만 쓰면, 평가자는 대화에서 존재를 본 적이 없으니 판정하지 못한다.
글이 “경로와 검증 결과가 대화에 나타나야 한다”를 넣은 것은 이 때문이며, 조건을 고칠 때 이 절을 지우면 목표가 끝나지 않을 수 있다.[^goal]

### 글의 수치는 글 안의 서술이다

글은 Anthropic 초기 테스트 보고에서 나온 토큰 60% 감소가 그 모델 실험의 것이고,
자기 하니스의 절감은 직접 측정해야 한다고 쓴다.
이 노트는 그 보고를 열어 보지 못했고, 수치를 확인하지 않았다.

## 확인하기

### 파일 구성 확인

위의 점검 스크립트를 작업 공간의 루트에서 돌린다.
`MISS`가 하나라도 있으면 종료 코드가 1이다.

### 설정이 읽혔는지 확인

글이 권하는 순서는 `/context`로 로드된 지시를, `/agents`로 검토자를, `/permissions`로 규칙을 보는 것이다.
공식 문서는 `/context`가 시작에 로드된 `CLAUDE.md`와 규칙 파일을 보여 주고, 하위 디렉터리의 `CLAUDE.md`는 로드될 때 `Loaded` 줄이 나온다고 적는다.[^memory]
`/agents`, `/permissions`, `/rewind`, `/usage`의 동작은 이 노트가 확인하지 않았다.

### 한 번 돌려 본 뒤 측정

같은 작업을 같은 수용 기준으로 돌려, 저장된 `drafts/article.md`와 `drafts/checks.md`를 열고 주장과 출처가 맞는 곳 몇 개를 점검한다.
`progress.md`가 저장된 작업과 일치하는지도 본다.
새 세션에서 `progress.md`를 읽게 해 기록된 다음 행동에서 이어 가는지 확인하고, 처음부터 다시 시작하면 노트에 빠진 결정이나 경로를 채운다.

## 체크리스트

- 루트 `CLAUDE.md`에 작업 사이에도 유효한 사실만 들어 있는가.
- 임시 마감이나 풀리지 않은 질문이 `CLAUDE.md`가 아니라 작업 쪽에 있는가.
- 스킬의 모든 단계가 관찰할 수 있는 결과를 낳는가.
- 스킬이 `$ARGUMENTS`를 받아 새 주제에 재사용되는가.
- 검토자가 판정(verified, incorrect, unresolved)마다 열어 본 URL을 돌려주는가.
- `unresolved` 판정이 빠진 증거를 구체적으로 적는가.
- 무인 실행에 필요한 읽기와 검색, `drafts/` 쓰기가 허용 규칙에 있는가.
- 거부 규칙을 파일 도구뿐 아니라 Bash 경로에서도 시험했는가.
- `/goal` 조건에 산출물 경로와 검증 결과가 대화에 나타나야 한다는 절이 있는가.
- 턴 상한 절이 있고, 엄격한 한도가 필요하면 실행 제어를 따로 두었는가.
- `progress.md`가 현재 파일, 끝낸 검사, 열린 문제, 다음 행동을 담는가.
- 절감 수치를 글이 아니라 자기 작업의 측정으로 확인했는가.

## 기억할 원칙

### 완료는 평가자가 볼 수 있는 증거로 정의한다

`/goal`의 평가자도, 다음 날의 새 세션도, 대화와 파일에 남은 것만 안다.
그래서 “다 했다”는 선언보다 열어 볼 수 있는 경로와 검증 표가 완료의 정의가 된다.
이 원칙은 하니스의 어느 층을 고치든 먼저 확인할 기준이다.

### 권한 규칙은 어느 경로를 막는지까지 적어야 규칙이다

거부 규칙이 내장 도구에는 걸리고 임의 프로세스에는 걸리지 않는다는 사실을 모르면, 규칙은 안전의 증거가 아니라 안전의 느낌이 된다.
규칙을 쓸 때 막는 경로와 막지 못하는 경로를 같이 적고, 막지 못하는 경로는 샌드박스처럼 다른 계층에 맡긴다.

---

[^memory]: Claude Code Docs, [How Claude remembers your project](https://code.claude.com/docs/en/memory)

[^subagents]: Claude Code Docs, [Create custom subagents](https://code.claude.com/docs/en/sub-agents)

[^permissions]: Claude Code Docs, [Configure permissions](https://code.claude.com/docs/en/permissions)

[^goal]: Claude Code Docs, [Keep Claude working toward a goal](https://code.claude.com/docs/en/goal)

[^model-config]: Claude Code Docs, [Model configuration](https://code.claude.com/docs/en/model-config)
