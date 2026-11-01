# 스킬 작성법: 간결하게 쓰고, 나눠서 불러오게 하고, 평가로 고친다

원문: [Skill authoring best practices - Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

## 소개

이 문서는 Claude Platform 문서의 스킬(Skill) 작성 가이드를 실제로 스킬을 쓰는
사람이 따라 할 수 있는 노트로 다시 정리한 것이다.
가이드의 한 줄 요약은 좋은 스킬이 간결하고, 구조가 잘 잡혀 있고,
실제 사용으로 시험되었다는 것이다.
가이드는 개념 설명이 아니라 작성 시 내릴 결정을 다룬다. 무엇을 쓰고,
무엇을 별도 파일로 빼고, 값을 어떻게 정하고, 어떻게 시험하는지다.

가이드 한 편만으로는 보이지 않는 부분이 있어서 두 문서를 함께 읽었다.
스킬의 로딩 구조를 설명하는 개요 문서와,
Claude Code에서 스킬이 실제로 어떻게 목록에 오르고 압축되는지를 다루는 Claude
Code 문서다.
가이드가 권하는 것 중 일부는 이 두 문서의 구체적인 한도와 만나야 이유가
분명해지고, 어긋나는 곳은 비평에서 다룬다.

## 동작 방식

### 스킬은 세 단계로 불려 온다

개요 문서는 스킬의 정보를 세 단계로 나눈다.
첫 단계는 시작할 때 항상 올라오는 메타데이터이고,
스킬 하나당 약 100토큰이며 머리말(frontmatter)의 `name`과
`description`이다.[^overview]
둘째 단계는 스킬이 발동될 때 올라오는 지시문으로,
`SKILL.md` 본문이며 5천 토큰 미만이다.[^overview]
셋째 단계는 필요할 때 읽는 자원이고, 접근하기 전에는 토큰이 들지
않는다.[^overview]
같은 문서는 스크립트를 실행하면 스크립트의 코드는 맥락에 올라오지 않고 출력만
토큰을 쓴다고 설명한다.[^overview]

이 구조가 가이드의 모든 조언을 낳는다.
시작 때 모든 스킬의 설명이 올라오므로 설명은 짧고 정확해야 하고,
본문은 발동 때만 올라오므로 간결해야 하고,
상세한 내용은 셋째 단계로 밀어 두면 비용이 없다.
가이드가 맥락 창(context window)을 공공재라고 부르는 이유다. 스킬은 시스템
프롬프트, 대화 이력, 다른 스킬의 메타데이터,
사용자의 요청과 같은 창을 나눠 쓴다.

### 목록에는 글자 예산이 있다

Claude Code는 스킬 이름과 설명의 목록을 맥락에 올린다.[^ccskills]
이름은 항상 모두 올라오지만, 스킬이 많으면 목록의 글자 예산에 맞추려고 일부
설명을 덜어 내고, 이 때문에 요청과 맞추는 데 필요한 키워드가
사라진다.[^ccskills]
예산은 모델 맥락 창의 1%이고, 넘치면 가장 적게 호출한 스킬의 설명부터 덜어
낸다.[^ccskills]
또 설명과 `when_to_use`를 합친 글자 수는 예산과 상관없이 1,536자에서 잘리므로,
핵심 용도를 앞에 두라고 문서는 말한다.[^ccskills]

가이드가 설명 안에 무엇을 하는지와 언제 쓰는지를 모두 넣으라고 하고,
사용 시점을 구체적인 키워드로 쓰라고 하는 것이 이 한도와 맞물린다.
설명 하나가 100개가 넘는 후보 가운데서 이 스킬을 고르는 근거가 되기 때문이다.

### 한 번 불러온 스킬은 대화에 남고, 압축되면 앞부분만 남는다

스킬을 호출하면 렌더링된 `SKILL.md`가 하나의 메시지로 대화에 들어가 이후 턴에도
남고, Claude Code는 이후 턴에 파일을 다시 읽지 않는다.[^ccskills]
그래서 작업 내내 적용되어야 하는 지침은 한 번만 하는 단계가 아니라 상시 지침으로
써야 한다.[^ccskills]
문서가 드는 예는 테스트를 돌리라는 말 대신 편집할 때마다 테스트를 돌리라고 쓰는
것이다.[^ccskills]

자동 압축(auto-compaction) 때는 가장 최근에 호출한 스킬마다 앞의 5,000토큰만
요약 뒤에 다시 붙고, 다시 붙는 스킬들의 합계 예산은 25,000토큰이다.[^ccskills]
이 예산은 가장 최근에 호출한 스킬부터 채우므로,
한 세션에서 스킬을 많이 호출했다면 오래된 것은 통째로 빠질 수 있다.[^ccskills]
이 때문에 가장 중요한 지침은 `SKILL.md` 위쪽에 두어야 한다.[^ccskills]

## 구현하기

### 이름과 머리말은 정해진 규칙이 있다

머리말에는 `name`과 `description`이 필요하다.
가이드가 적은 규칙은 이렇다. `name`은 최대 64자이고 소문자, 숫자,
하이픈만 쓸 수 있으며 XML 태그와 예약어가 들어가면 안 된다.
`description`은 비어 있으면 안 되고 최대 1,024자이며 XML 태그가
들어가면 안 된다.
이름은 동명사 형태(`processing-pdfs`, `analyzing-spreadsheets`)를 권하고,
명사구(`pdf-processing`)나 동사구(`process-pdfs`)도 받아들일 만하다고 한다.
`helper`, `utils` 같은 모호한 이름, `documents`,
`data` 같은 지나치게 일반적인 이름, `anthropic-helper`,
`claude-tools` 같은 예약어, 같은 모음 안에서 일관되지 않은 패턴은 피한다.

Claude Code에서는 머리말 필드가 더 있다.
`when_to_use`는 설명에 덧붙는 호출 시점이고,
`argument-hint`는 자동 완성에 보이는 인자 힌트이며,
`disable-model-invocation`은 모델이 스스로 이 스킬을 불러오지 못하게 하고,
`user-invocable: false`는 사용자 메뉴에서 숨긴다.[^ccskills]
`allowed-tools`는 그 스킬이 호출된 턴 동안 묻지 않고 쓸 수 있는 도구를 정하고,
다음 메시지를 보내면 풀린다.[^ccskills]
다른 곳에 올리는 스킬은 허용되는 머리말 키가 더 적다. 문서는 `argument-hint`를
넣어 올리면 허용되지 않는 키라는 오류가 나는 예를 보여 준다.[^ccskills]

### 설명은 무엇을 하는지와 언제 쓰는지를 함께 쓴다

가이드가 드는 좋은 설명은 PDF 스킬의 `Extract text and tables from PDF files,
fill forms, merge documents. Use when working with PDF files or when the user
mentions PDFs, forms, or document extraction.`처럼 동작과 발동 조건을 한
설명에 담는다.
나쁜 설명은 `Helps with documents`, `Processes data`,
`Does stuff with files`처럼 대상도 시점도 없다.
설명은 스킬마다 하나뿐이고, 본문은 구현 세부를 맡는다는 역할 분담이
가이드의 전제다.

### 본문은 안내문이고 상세는 파일로 나눈다

`SKILL.md`는 온보딩 안내서의 목차처럼 필요한 자료로 Claude를 보내는 개요여야
한다고 가이드는 말한다.
본문은 500줄 아래로 두고, 그 한도에 가까워지면 별도 파일로 나눈다.
세 가지 패턴이 있다.

| 패턴             | 모양                                                                  | 맞는 경우                                  |
| ---------------- | --------------------------------------------------------------------- | ------------------------------------------ |
| 상위 안내와 참조 | `SKILL.md`에 빠른 시작을 두고 `FORMS.md`, `REFERENCE.md`로 링크한다   | 기본 용법과 고급 기능이 나뉘는 경우        |
| 영역별 구성      | `reference/finance.md`, `reference/sales.md`처럼 영역마다 파일을 둔다 | 한 질문이 한 영역만 필요로 하는 경우       |
| 조건부 세부      | 기본 내용만 본문에 두고 고급 항목은 링크로 연결한다                   | 대부분의 사용자가 고급 기능을 안 쓰는 경우 |

참조는 `SKILL.md`에서 한 단계까지만 깊어야 한다.
참조된 파일이 다시 다른 파일을 참조하면 Claude가 `head -100` 같은 명령으로 미리
보기만 하고 일부만 읽어 정보가 불완전해질 수 있기 때문이다.
100줄이 넘는 참조 파일은 맨 위에 목차를 두어,
일부만 읽어도 전체 범위가 보이게 한다.
파일 이름은 `form_validation_rules.md`처럼 내용을 드러내고,
경로는 항상 슬래시(`reference/guide.md`)로 쓴다. 역슬래시는 유닉스에서
오류를 낸다.

### 복잡한 일은 체크리스트로 쪼갠다

복잡한 작업은 순서 있는 단계로 나누고, 특히 복잡하면 Claude가 응답에 복사해
항목을 체크해 가며 쓸 체크리스트를 제공한다.
가이드의 PDF 양식 채우기 예는 분석, 필드 매핑 작성, 매핑 검증, 양식 채우기,
출력 검증의 다섯 단계이고, 검증이 실패하면 매핑 단계로 돌아간다.
이 반복이 피드백 루프다. 검증기를 돌리고, 오류를 고치고, 다시 돌린다.
코드가 없는 스킬에서도 같은 패턴을 쓸 수 있다. 이때 검증기는 `STYLE_GUIDE.md`
같은 참조 문서이고 Claude가 읽고 비교해 검사한다.

더 위험한 일에는 계획, 검증, 실행(plan-validate-execute) 패턴이 있다.
Claude가 먼저 구조화된 형식의 계획 파일(`changes.json`)을 만들고,
스크립트로 그 계획을 검증한 뒤 실행한다.
가이드가 이 패턴이 맞는다고 하는 경우는 일괄 작업, 파괴적 변경,
복잡한 검증 규칙, 중요한 작업이다.
검증 스크립트는 `Field 'signature_date' not found. Available fields: ...`처럼
구체적인 오류 메시지를 내야 Claude가 고칠 수 있다.

### 스크립트는 오류를 스스로 처리한다

스크립트는 오류를 Claude에게 떠넘기지 않고 처리해야 한다.
파일이 없으면 실패하는 대신 기본 내용으로 만들고,
권한이 없으면 대안을 쓰는 식이다.
설정값은 이유를 적는다. 가이드는 정당화되지 않은 상수를
오스터하우트(Ousterhout)의 법칙에서 말하는 부두 상수(voodoo constants)라고
부르며, 모르는 값을 Claude가 어떻게 정하겠느냐고 묻는다.

미리 만든 스크립트는 Claude가 만들 수 있는 코드보다 신뢰할 수 있고,
토큰과 시간을 아끼고, 매번 같은 결과를 낸다.
지시문은 스크립트를 실행하라는 것인지 참고용으로 읽으라는 것인지 분명히 써야
한다. 대부분의 유틸리티 스크립트는 실행이 낫다.
스크립트 경로는 작업 디렉터리가 바뀌어도 맞아야 하는데,
Claude Code는 스킬 본문과 `allowed-tools`의 Bash 규칙에서
`${CLAUDE_SKILL_DIR}`을 스킬 디렉터리로 치환한다.[^ccskills]

MCP 도구는 `ServerName:tool_name`처럼 서버 이름을 붙인 완전한 이름으로 부른다.
서버가 여럿이면 접두어 없이는 도구를 못 찾을 수 있다.
패키지는 설치되어 있다고 가정하지 않고 `pip install pypdf` 같은 설치
명령을 적는다.

### 시작 템플릿

아래는 이 가이드의 조언을 한곳에 모은 최소 스킬이다.
`description`에 동작과 시점이 있고, 본문은 개요이며,
상세는 한 단계 아래 파일로 가고, 스크립트는 실행하라고 명시하고,
검증 루프가 있다.

```markdown
---
name: validating-skills
description: Checks a skill directory against the authoring checklist (name and description limits, body length, reference depth). Use when writing, reviewing or refactoring a SKILL.md, or when a skill is not triggering as expected.
disable-model-invocation: false
---

# Validating skills

Run the checker, fix what it reports, and run it again until it prints OK:

    python3 ${CLAUDE_SKILL_DIR}/scripts/lint_skill.py <skill-directory>

For the meaning of each check, see [references/checks.md](references/checks.md).
For how to write a good description, see [references/descriptions.md](references/descriptions.md).

## Workflow

Copy this checklist and tick items off:

- [ ] Run the checker on the directory
- [ ] Fix every reported problem, starting with the description
- [ ] Re-run until it prints OK
- [ ] Test the skill on three real requests
```

## 값 정하기

| 항목                  | 시작값                    | 근거와 측정할 것                                                                              |
| --------------------- | ------------------------- | --------------------------------------------------------------------------------------------- |
| `SKILL.md` 본문 길이  | 500줄 미만                | 가이드의 한도이며 최적 성능을 위한 값이다. 넘으면 파일로 나눈다                               |
| 참조 파일 깊이        | 한 단계                   | 중첩되면 일부만 읽힌다. Claude가 실제로 파일을 다 읽는지 시험해서 본다                        |
| 목차를 넣는 파일 길이 | 100줄 초과                | 미리 보기만 해도 전체 범위가 보이게 한다                                                      |
| `name` 길이           | 64자 이하                 | 소문자, 숫자, 하이픈만 쓴다                                                                   |
| `description` 길이    | 1,024자 이하, 핵심은 앞에 | 가이드의 한도다. Claude Code는 설명과 `when_to_use`를 합쳐 1,536자에서 자른다[^ccskills]      |
| 평가 수               | 최소 3개                  | 가이드의 체크리스트가 정한 최소값이다                                                         |
| 시험할 모델           | 쓸 모델 전부              | Haiku는 지침이 충분한지, Sonnet은 명확하고 효율적인지, Opus는 지나치게 설명하지 않는지를 본다 |
| 자유도                | 작업의 취약성에 맞춘다    | 아래 트레이드오프를 본다                                                                      |

## 트레이드오프

### 간결함은 토큰을 아끼지만 모델 수준에 따라 모자랄 수 있다

가이드의 기본 가정은 Claude가 이미 매우 똑똑하다는 것이다.
그래서 모든 문단에 이 설명이 정말 필요한지, 이 문단이 토큰 값을 하는지를 묻고,
PDF가 무엇인지 설명하는 150토큰짜리 문단을 `pdfplumber`를 쓰라는 50토큰짜리
문단으로 줄이라고 한다.

그러나 같은 가이드는 Opus에서 완벽하게 작동하는 스킬이 Haiku에는 더 많은 세부가
필요할 수 있다고 말한다.
간결함의 기준이 모델마다 다르다는 뜻이다. 여러 모델에서 쓸 스킬은 가장 약한
모델에서도 되는 선까지는 설명하고, 강한 모델에서 지나치게 설명하지
않는지 따로 본다.
어려움은 이 두 시험이 서로 반대 방향으로 당긴다는 점이다. 줄이면 Haiku가
실패하고, 늘리면 Opus에서 군더더기가 된다.

### 자유도는 취약성에 맞춘다

가이드는 세 단계의 자유도를 말한다.
높은 자유도는 글로 된 지시이고, 여러 접근이 맞고 맥락이 결정을 좌우할 때 쓴다.
코드 리뷰 절차가 예다.
중간 자유도는 매개변수가 있는 의사 코드나 스크립트이고,
선호하는 패턴이 있고 변형이 허용될 때 쓴다.
낮은 자유도는 정확한 스크립트이고, 작업이 깨지기 쉽고 일관성이 중요하고 정해진
순서가 있을 때 쓴다. 데이터베이스 마이그레이션이 예이며,
명령을 바꾸거나 플래그를 더하지 말라고 적는다.

안전한 길이 하나뿐인 작업에는 정확한 안전장치를 주고,
어느 길로 가도 성공하는 작업에는 방향만 준다는 것이 가이드의 설명이다.
자유도를 낮추면 일관성은 얻지만 맥락에 맞게 바꾸는 능력을 잃는다. 높이면 반대다.
작업 하나 안에서도 부분마다 자유도가 다를 수 있으므로 스킬 전체에 한 가지 수준을
쓰지 말고 단계별로 정한다.

### 선택지를 줄이면 혼란은 줄지만 예외를 막는다

가이드는 `pypdf`, `pdfplumber`, `PyMuPDF`,
`pdf2image`를 나열하는 대신 기본값 하나를 주고 예외 경로를 따로 적으라고 한다.
스캔된 PDF가 필요하면 `pdf2image`와 `pytesseract`를 쓰라는 식이다.
선택지를 나열하면 Claude가 매번 고르는 비용을 치르고, 일관성도 떨어진다.
기본값 하나와 예외 하나라는 모양은 선택의 자유를 막지 않으면서 기본 경로를
분명하게 한다.

### 모델이 스스로 호출하게 둘지는 부작용에 달려 있다

스킬을 모델이 자동으로 불러오게 하면 사용자는 따로 호출하지 않아도 되지만,
부작용이 있는 일을 모델이 알아서 시작할 수 있다.
Claude Code 문서는 `disable-model-invocation: true`를 커밋, 배포,
메시지 전송처럼 부작용이 있거나 시점을 직접 정하고 싶은 작업에 쓰라고
안내한다.[^ccskills]
이 값이 켜지면 설명이 맥락에 올라오지 않고,
사용자가 호출할 때 스킬 전체가 올라온다.[^ccskills]
반대로 `user-invocable: false`는 설명은 항상 맥락에 있고 사용자가 부를 수
없으며, 배경 지식에 맞는다.[^ccskills]
이 선택은 설명 목록의 글자 예산과도 연결된다. 수동으로만 쓰는 스킬은 설명이
목록에 들어가지 않으므로 예산을 아낀다.

## 함정

### 중첩 참조는 일부만 읽힌다

참조 파일이 다른 참조 파일을 가리키면 Claude가 앞부분 미리 보기만 하고 멈춰
정보가 빠진다.
모든 참조 파일을 `SKILL.md`에서 직접 링크하고,
링크 옆에 그 파일이 무엇이고 언제 읽는지를 적는다.

### 시간에 묶인 정보는 낡는다

`2025년 8월 전이면 옛 API를 쓰라`는 문장은 시간이 지나면 틀린다.
가이드는 현재 방법을 본문에 쓰고, 옛 방법은 접어 둔 `old patterns` 절에
두라고 한다.
같은 이유로 `이 값은 2026년 10월에 확인했다`는 식의 날짜 주석도 본문에 두지
않는 편이 낫다.

### 같은 것을 다르게 부르면 따라 하기가 흔들린다

한 스킬 안에서 한 개념에는 한 용어를 쓴다.
`API endpoint`, `URL`, `API route`, `path`를 섞거나 `field`, `box`, `element`,
`control`을 섞으면 Claude가 같은 것인지 다른 것인지 헷갈린다.

### 환경마다 가정이 다르다

claude.ai에서는 npm과 PyPI에서 패키지를 설치하고 GitHub 저장소를 가져올 수
있지만, API에서는 네트워크 접근과 런타임 패키지 설치가 없다고 가이드는 말한다.
개요 문서도 API의 스킬이 네트워크 없는 샌드박스 컨테이너에서 돈다고 적고,
한 곳에 올린 사용자 정의 스킬은 다른 곳과 동기화되지 않는다고
덧붙인다.[^overview]
필요한 패키지를 지시문에 적고 쓸 환경에서 쓸 수 있는지 확인해야 한다.

### 반드시 지켜야 하는 규칙을 지시문에만 쓰면 어길 수 있다

Claude가 매번 지켜야 하는 규칙을 건너뛴다면 그 규칙은 훅(hook)으로 옮기라고
Claude Code 문서는 안내한다.[^ccskills]
훅은 이벤트가 일어날 때마다 실행되므로 Claude가 스킬을 따르든 말든 적용되고,
스킬 머리말의 `hooks`에 정의해 스킬과 함께 둘 수도 있다.[^ccskills]
이 문서가 가이드와 만나는 지점이다. 가이드의 검증 스크립트와 피드백 루프는
Claude가 실행해야 효과가 있지만, 훅은 실행을 강제한다.

### 목록의 설명이 잘려 스킬이 발동하지 않을 수 있다

스킬이 많으면 설명이 덜어져 키워드가 사라지고 요청과 맞지 않게 된다.[^ccskills]
낮은 우선순위의 스킬은 `skillOverrides`에서 `name-only`로 두어 설명 없이 목록에
올릴 수 있다.[^ccskills]

### 출처를 믿을 수 없는 스킬은 위험하다

스킬은 지시와 코드로 Claude에게 새 능력을 주므로,
악의적인 스킬은 선언한 목적과 다르게 도구를 부르거나 코드를 실행하게 할 수
있다.[^overview]
개요 문서는 직접 만들었거나 Anthropic에서 받은 스킬만 쓰라고 하고,
번들된 모든 파일을 감사하라고 한다.[^overview]
저장소에 들어 있는 프로젝트 스킬의 `allowed-tools`도 검토해야 한다. Claude Code
문서는 이 필드가 신뢰하지 않는 폴더에서도 적용된다고 경고한다.[^ccskills]

## 확인하기

### 평가를 먼저 만든다

가이드의 개발 순서는 평가를 문서보다 먼저 만드는 것이다.
스킬 없이 대표 작업을 돌려 구체적인 실패나 부족한 맥락을 적고,
그 틈을 시험하는 시나리오 세 개를 만들고,
스킬 없는 상태의 성능을 기준선으로 재고, 틈을 메울 만큼의 최소한의 지시를 쓰고,
평가를 돌려 기준선과 비교하며 고친다.
평가 한 건은 쓸 스킬, 질의, 입력 파일, 기대 동작의 목록으로 이루어진 JSON이다.
기대 동작은 `Extracts text content from all pages in the document without
missing any pages`처럼 관찰할 수 있는 문장으로 쓴다.

### Claude A로 쓰고 Claude B로 시험한다

가이드가 가장 효과적이라고 하는 개발 방식은 한 인스턴스(Claude A)와 스킬을 함께
설계하고, 스킬을 불러온 새 인스턴스(Claude B)로 실제 작업을 시키는 것이다.
스킬 없이 한 번 작업을 끝까지 하면서 반복해서 준 맥락을 눈여겨보고,
그 재사용 패턴을 Claude A에게 스킬로 만들게 하고, 군더더기를 지우게 하고,
정보 구조를 정리하게 한 다음 Claude B로 비슷한 작업을 돌려 본다.
Claude B가 막히면 Claude A에게 구체적인 관찰(`Q4 날짜 필터를 빠뜨렸다`)을
가져가 고친다.

관찰할 것은 네 가지다. 예상 밖의 탐색 경로, 따라가지 못한 링크,
같은 파일을 계속 읽는 과잉 의존, 한 번도 열지 않는 파일이다.
마지막 둘은 각각 그 내용이 본문에 있어야 한다는 신호와 그 파일이 불필요하거나
안내가 약하다는 신호다.

### 기계적인 항목은 스크립트로 검사한다

체크리스트의 기계적인 항목(이름과 설명의 한도, 본문 길이, 링크 깊이,
목차 유무)은 사람이 눈으로 보지 말고 스크립트가 본다.
아래는 그 항목을 검사하는 완전한 스크립트다. 이름과 설명, 본문 줄 수,
역슬래시 경로, `SKILL.md`의 링크 대상과 참조 깊이,
100줄이 넘는 참조 파일의 목차를 확인한다.

```python
#!/usr/bin/env python3
"""Check skill directories against the mechanical items of the authoring checklist."""
import re
import sys
from pathlib import Path

RESERVED = ("anthropic", "claude")  # the guide names reserved words; extend if the list changes


def split_frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    return (m.group(1), m.group(2)) if m else (None, text)


def field(fm, key):
    # take a (possibly folded) scalar up to the next top-level key
    m = re.search(rf"^{key}:\s*(.*?)(?=^\S[\w-]*:|\Z)", fm, re.S | re.M)
    return re.sub(r"\s+", " ", m.group(1).replace(">-", "")).strip().strip("'\"") if m else None


def md_links(text):
    # skip web links and <placeholder> targets used in examples
    links = re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text)
    return [t for t in links if not t.startswith(("http", "mailto")) and "<" not in t]


def lint(skill_dir):
    problems = []
    fm, body = split_frontmatter((skill_dir / "SKILL.md").read_text())
    if fm is None:
        return ["no YAML frontmatter"]
    name, desc = field(fm, "name"), field(fm, "description")
    if not name or len(name) > 64 or not re.fullmatch(r"[a-z0-9-]+", name):
        problems.append(f"name must be 1-64 chars of lowercase letters, digits, hyphens: {name!r}")
    elif any(w in name for w in RESERVED):
        problems.append(f"name contains a reserved word: {name!r}")
    if not desc:
        problems.append("description is empty")
    else:
        if len(desc) > 1024:
            problems.append(f"description is {len(desc)} chars (limit 1,024)")
        if re.search(r"<[A-Za-z/][^>]*>", desc):
            problems.append("description contains an XML-like tag")
    lines = body.count("\n") + 1
    if lines > 500:
        problems.append(f"body is {lines} lines (keep under 500)")
    if re.search(r"[\w.]+\\[\w.]+", re.sub(r"```.*?```", "", body, flags=re.S)):
        problems.append("possible Windows-style path")
    for link in md_links(body):
        target = skill_dir / link
        if not target.exists():
            problems.append(f"broken link from SKILL.md: {link}")
        elif target.suffix == ".md":
            ref = target.read_text()
            head = "\n".join(ref.splitlines()[:25]).lower()
            if ref.count("\n") + 1 > 100 and "contents" not in head and "목차" not in head:
                problems.append(f"{link}: over 100 lines without a table of contents")
            for inner in md_links(ref):
                if inner.endswith(".md") and (target.parent / inner).resolve() != target.resolve():
                    problems.append(f"{link} links onward to {inner} (keep references one level deep)")
    return problems


if __name__ == "__main__":
    failed = False
    for arg in sys.argv[1:]:
        found = lint(Path(arg))
        print(f"{arg}: {'OK' if not found else 'FAIL'}")
        for p in found:
            print("  -", p)
        failed = failed or bool(found)
    sys.exit(1 if failed else 0)
```

실행은 `python3 lint_skill.py .claude/skills/*/`이고,
종료 코드가 0이면 이 검사를 통과한 것이다.
이 검사는 형식만 본다. 설명이 실제로 발동하는지와 지침이 따라지는지는 평가로
확인해야 한다.

Claude Code에서는 목록의 상태도 직접 볼 수 있다. `/doctor`는 목록이 맥락에서
차지하는 크기와 가장 큰 기여자를 추정해 보여 주고,
`/skill-doctor`는 끌 만한 스킬을 찾아 주며,
목록이 예산을 넘으면 `--debug`로 보는 디버그 로그에 경고가 남는다.[^ccskills]
`/context`의 스킬 행은 예산이 적용된 뒤의 목록 크기를 보여 준다.[^ccskills]

## 비평

### 가이드의 한도는 측정 없이 제시된다

가이드는 본문을 500줄 아래로 두면 최적 성능을 낸다고 말하지만 그 값의 근거가
되는 측정은 싣지 않는다.
평가를 최소 세 개 만들라는 기준과 설명을 100개 넘는 스킬 가운데서 고른다는
서술도 마찬가지다.
이 값들은 경험칙으로 읽는 것이 맞고, 자기 스킬에서 같은 값이 최적인지는 평가로
따로 봐야 한다.

Claude Code 문서의 한도는 더 구체적이지만 다른 종류의 값이다. 압축 때 앞의
5,000토큰이 남고 목록의 설명은 1,536자에서 잘린다는 것은 구현이 정한 한도이지
품질의 최적점이 아니다.[^ccskills]
500줄 한도와 5,000토큰 한도가 같은 방향을 가리키는 것은 우연이 아니지만,
500줄짜리 본문이 5,000토큰 안에 들어온다는 보장은 없다.

### 가이드는 압축 뒤의 스킬을 다루지 않는다

가이드는 상세 내용을 참조 파일로 보내면 접근 전에는 비용이 없다고 말한다.
그러나 Claude Code 문서에 따르면 압축 후에는 스킬의 앞부분만 다시
붙는다.[^ccskills]
이미 읽은 참조 파일의 내용은 요약 속에 흔적만 남을 수 있으므로,
긴 작업 중간에 압축이 일어나면 참조의 세부가 사라지고 `SKILL.md`의
개요만 남는다.
참조 파일을 읽는 시점을 단계마다 지시문에 적어 두어야 이 손실을 메울 수 있는데,
가이드는 이 점을 말하지 않는다.

### 같은 모델 계열이 쓰고 시험하는 방식에는 한계가 있다

Claude A와 Claude B 방식은 모델이 좋은 에이전트 지시문을 쓰고 에이전트에게
필요한 정보가 무엇인지 알아본다는 전제 위에 서 있다.
이 방식은 시험을 사람의 관찰로 닫는다. Claude B의 행동을 사람이 보고 Claude
A에게 가져가므로 순환 논증은 아니다.
다만 Claude A와 B가 같은 계열이면 같은 맹점을 공유할 수 있다. Claude A가 쓰기
쉬운 형태로 쓴 지시문을 Claude B가 쉽게 읽는 것은 지시문이 좋아서가 아니라 같은
분포에서 나왔기 때문일 수 있다.
가이드가 세 모델(Haiku, Sonnet, Opus)로 시험하라고 하는 것이 이 위험의 일부를
줄이지만, 다른 계열의 에이전트로 읽혀 보라는 말은 없다.

### 한도는 표면마다 다르고 바뀔 수 있다

가이드가 말하는 `name` 64자와 `description` 1,024자 한도는 이 가이드가 쓰인
시점의 값이다.
같은 설명이 Claude Code에서는 `when_to_use`와 합쳐 1,536자에서 잘리고,
그 한도도 설정으로 바꿀 수 있다고 문서는 적는다.[^ccskills]
따라서 한도는 스킬 본문에 고정해 쓰지 말고 검사 스크립트의 상수로 한 곳에 두어,
값이 바뀌면 거기만 고치게 해야 한다.

## 체크리스트

- 설명이 무엇을 하는지와 언제 쓰는지를 모두 담고, 핵심 키워드가 앞에 있는가.
- 설명이 1,024자 이하이고 XML 태그나 꺾쇠 자리표시자를 포함하지 않는가.
- `SKILL.md` 본문이 500줄 미만이고, 가장 중요한 지침이 위쪽에 있는가.
- 참조 파일이 모두 `SKILL.md`에서 직접 링크되고, 한 단계보다 깊지 않은가.
- 100줄이 넘는 참조 파일 위에 목차가 있는가.
- 한 개념에 한 용어를 쓰고, 날짜에 묶인 문장이 없는가.
- 스크립트가 오류를 스스로 처리하고, 상수마다 이유가 적혀 있는가.
- 지시문이 스크립트를 실행하라는 것인지 읽으라는 것인지 밝히는가.
- 필요한 패키지가 지시문에 적혀 있고, 쓸 환경에서 쓸 수 있는가.
- 중요한 작업에 검증 단계와 피드백 루프가 있는가.
- 부작용이 있거나 시점을 직접 정해야 하는 스킬에 `disable-model-invocation: true`가 있는가.
- 평가를 최소 세 개 만들고, 스킬 없는 기준선과 비교했는가.
- 쓸 모델 전부에서 시험했고, 실제 사용 시나리오에서도 시험했는가.
- 반드시 지켜야 하는 규칙을 훅이나 스크립트로 강제하는가.

## 기억할 원칙

### 스킬은 모델이 이미 아는 것을 빼고 모르는 것만 쓴다

간결함은 문체의 문제가 아니라 비용의 문제다.
스킬의 모든 줄은 발동할 때마다 대화 이력, 다른 스킬,
사용자의 요청과 같은 창을 놓고 경쟁한다.
모델이 이미 아는 설명을 빼고, 이 프로젝트에서만 맞는 규칙, 순서,
값의 이유만 남기면 같은 창에 더 많은 일이 들어간다.

### 필요할 때만 읽히게 나누고, 읽을 시점을 적는다

세 단계 로딩은 상세한 내용을 공짜로 보관할 수 있게 해 준다.
그 대가로 상세는 읽혀야 쓰이므로, 파일마다 무엇이고 언제 읽는지를 링크 옆에
적고, 압축으로 사라진 뒤에도 다시 읽을 수 있게 시점을 단계마다 쓴다.
가장 중요한 지침은 위쪽에 두어, 일부만 남는 경우에도 살아남게 한다.

### 평가가 문서보다 먼저다

스킬은 상상한 요구가 아니라 실제로 일어난 실패를 메우기 위해 쓴다.
스킬 없이 돌려 실패를 적고, 그 실패를 시험하는 시나리오를 만들고,
기준선과 비교하며 고치면 지시가 늘어나는 것이 아니라 필요한 만큼만 늘어난다.

---

[^overview]: Claude Platform Docs, [Agent Skills - Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

[^ccskills]: Claude Code Docs, [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills), 2026-10-30
