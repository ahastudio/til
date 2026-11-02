# myclaude: Claude Code가 계획하고 Codex·Gemini 등 여러 백엔드에 실행을 맡기는 워크플로 모음

<https://github.com/stellarlinkco/myclaude>

## 소개

myclaude는 Claude Code용 다중 에이전트 개발 자동화 모음이다.
README는 Claude Code를 오케스트레이터로, `codeagent-wrapper`를 실행기로 나눈다.
오케스트레이터는 계획, 맥락 수집, 검증을 맡는다.
실행기는 코드 편집과 테스트 실행을 맡고 Codex, Claude, Gemini,
OpenCode 중 하나를 백엔드로 쓴다.

저장소는 2025년 7월 17일에 만들어졌고 마지막 푸시는 2026년 5월 4일이다.
기록 시점에 스타는 2,752개, 포크는 301개였고 주 언어는 Go,
라이선스는 AGPL-3.0이다.[^api]
README의 버전 배지는 6.x다.
상업적 사용을 AGPL 의무 없이 하려면 이메일로 문의하라고 README는 안내한다.

## 모듈과 스킬

README의 모듈 표는 여덟 개다.

| 모듈         | 설명                                                               | 호출                  |
| ------------ | ------------------------------------------------------------------ | --------------------- |
| do           | 권장 모듈, codeagent 오케스트레이션을 쓰는 5단계 기능 개발         | `/do`                 |
| omo          | 지능형 라우팅을 쓰는 다중 에이전트 오케스트레이션                  | `/omo`                |
| bmad         | 전문 에이전트 여섯 개로 구성한 BMAD 애자일 워크플로                | `/bmad-pilot`         |
| requirements | 가벼운 요구사항에서 코드까지의 파이프라인                          | `/requirements-pilot` |
| essentials   | 핵심 개발 명령 열한 개                                             | `/code`, `/debug` 등  |
| sparv        | Specify→Plan→Act→Review→Vault 워크플로                             | `/sparv`              |
| course       | dev, product-requirements, test-cases를 묶은 강의 개발용 복합 모듈 | 복합 모듈             |
| claudekit    | do 스킬에 전역 훅 세 개를 더한 복합 모듈                           | 복합 모듈             |

개별 설치 스킬로는 browser, codeagent, codex, dev, gemini, product-requirements,
prototype-prompt-generator, skill-install, test-cases가 있다.
README의 선택 가이드는 기능 개발에는 `/do`, 버그 조사와 수정에는 `/omo`,
대형 기업 프로젝트에는 `/bmad-pilot`, 빠른 프로토타입에는 `/requirements-pilot`,
단순 작업에는 `/code`나 `/debug`를 권한다.

## 설치

```bash
npx github:stellarlinkco/myclaude
npx github:stellarlinkco/myclaude --list
npx github:stellarlinkco/myclaude --update
npx github:stellarlinkco/myclaude --install-dir ~/.claude --force
```

기본 설치 위치는 `~/.claude`다.
README가 보여 주는 설치 뒤 구조에는
`bin/codeagent-wrapper`, `CLAUDE.md`, `commands/`, `agents/`,
`skills/`, `hooks/`,
자동 생성되는 `settings.json`, 설치 목록을 추적하는
`installed_modules.json`이 있다.
`config.json`의 모듈별 `enabled` 값으로 쓸 모듈을 켜고 끈다.
`--update`는 이미 설치된 모듈을 감지해 최신 릴리스로 덮어쓴다.

## do 모듈의 5단계

`skills/do/README.md`는 `do`를 다섯 단계로 설명한다.

| 단계 | 이름       | 목표            | 요점                                 |
| ---- | ---------- | --------------- | ------------------------------------ |
| 1    | Understand | 요구사항 수집   | 사용자 질문과 `code-explorer` 분석   |
| 2    | Clarify    | 모호함 해소     | 필수, 답하기 전에는 진행하지 않음    |
| 3    | Design     | 구현 계획       | `code-architect`가 접근 방식 제안    |
| 4    | Implement  | 기능 구현       | 승인 필요, `develop` 에이전트가 수행 |
| 5    | Complete   | 마무리와 문서화 | `code-reviewer`가 요약               |

`do`의 고정 제약은 여섯 가지다.
코드를 직접 쓰지 않고 모든 변경을 `codeagent-wrapper`의 에이전트에 위임한다.
2단계는 필수이고 4단계는 승인이 필요하다.
모든 에이전트에게 요청 원문과 결정 사항을 담은 Context Pack을 넘긴다.
독립된 작업은 `codeagent-wrapper --parallel`로 병렬 실행한다.
단계가 끝날 때마다 `.claude/do-tasks/{task_id}/task.json`을 갱신한다.

`/do`로 시작하면 `.claude/do-tasks/{task_id}/task.md`가 YAML 머리말과
함께 만들어진다.
설치 때 등록되는 Stop 훅이 이 파일의 상태를 확인해 작업이 끝나지 않았으면
종료를 막는다.
다섯 단계가 모두 끝나면 `<promise>DO_COMPLETE</promise>`를 출력한다.
중간에 그만두려면 `task.md`의 `status`를 `cancelled`로 직접 고친다.

## codeagent-wrapper

`codeagent-wrapper`는 Go로 쓴 CLI 래퍼다.
Codex, Claude, Gemini, OpenCode를 같은 플래그와 설정으로 부르고,
스킬 주입과 세션 재개를 지원한다고 README는 설명한다.
기본 백엔드는 `codex`다.

```bash
codeagent-wrapper --backend claude "explain the parallel config format"
codeagent-wrapper --worktree "refactor the auth module"
codeagent-wrapper resume <session_id> "continue the previous task"
```

README가 꼽는 기능은 다음과 같다.
`--parallel`은 표준 입력의 작업 설정을 읽어 의존 관계에 따른 위상 정렬 순서로
동시 실행하며,
기본 작업자 수는 10이고 바꿀 수 있다.
`--worktree`는 자동으로 만든 task_id와 브랜치로 별도 git worktree에서 작업한다.
`~/.codeagent/models.json`에서 에이전트별 백엔드, 모델, 프롬프트,
허용 도구를 정한다.
`--skills`로 스킬을 지정하거나 프로젝트의 기술 스택에서 자동으로 고른다.
`--skip-permissions`와 같은 뜻의 `--dangerously-skip-permissions` 별칭도 있다.

이 문서를 쓴 환경에서는 설치하거나 실행하지 않았다.
README, `skills/do/README.md`, `codeagent-wrapper/README.md`의 앞부분
5,000자를 읽었고,
나머지 모듈의 README와 소스 코드는 열지 않았다.

## 비평

### 설치가 사용자 전역 설정을 건드린다

설치 기본 위치가 `~/.claude`이고, 훅 설정이 `settings.json`에 자동으로 합쳐진다.
`CLAUDE.md`도 기본으로 설치된다고 README는 적는다.
이미 자기 지침과 훅을 가진 사용자라면 기존 설정과 섞이거나 덮어써질 수 있다.
`--force`와 `--update`는 모듈 파일을 덮어쓴다.
설치 전에 `~/.claude`를 백업하고, 합쳐질 `settings.json`의 훅을 읽어 보는
것이 안전하다.
이는 README의 설치 설명에서 도출한 판단이다.

### 모듈이 여덟 개이고 서로 겹친다

`do`, `bmad`, `requirements`, `sparv`는 모두 요구사항에서 구현까지
가는 흐름이다.
README의 선택 가이드가 시나리오별로 하나씩 권하지만,
왜 그 모듈이 그 시나리오에 맞는지, 서로 어떻게 다른지는 표에 없다.
처음 쓰는 사람은 `do` 하나로 시작하고 나머지는 필요할 때 켜는 편이 낫다.
README가 `do`를 권장 모듈로 표시한 것이 그 근거다.

### 권한과 승인이 단계마다 다르게 걸린다

`do`는 4단계 구현 전에 승인을 요구한다.
그러나 실제 코드 편집은 `codeagent-wrapper`가 부른 백엔드가 하고,
래퍼에는 권한 확인을 건너뛰는 플래그가 있다.
승인이 걸리는 위치와 백엔드의 권한 설정이 서로 다른 층이어서,
백엔드를 권한 확인 없이 돌리면 4단계 승인이 편집을 막는지는
README만으로 알 수 없다.
Stop 훅이 종료를 막는 것도 탈출구가 `task.md` 수동 편집이라,
상태 파일을 쓸 수 있는 에이전트라면 같은 파일을 고칠 수 있다.
이 둘은 모두 구조에서 도출한 우려이고 실제로 그런 일이 있었다는 자료는 없다.

### 라이선스와 효과의 근거

AGPL-3.0은 수정한 버전을 네트워크로 제공하면 소스 공개 의무가 생길 수
있는 라이선스다.
사내 개발 도구로만 쓸 때와 제품에 포함할 때를 나눠 검토해야 하고,
README는 의무 없이 쓰려면 별도 상업 라이선스를 문의하라고 한다.
또한 README에는 이 워크플로가 단일 에이전트보다 낫다는 비교 결과가 없다.
스타 2,752개는 관심의 크기이지 품질의 증거가 아니다.[^api]

## 체크리스트

- [ ] 설치 전에 `~/.claude`를 백업했는가
- [ ] Go 1.21 이상이 있거나 `npx`로 래퍼를 설치할 수 있는가
- [ ] 쓰려는 백엔드 CLI(`codex`, `claude`, `gemini`, `opencode`)가 README의 요구 기능을 지원하는 버전인가
- [ ] `do`를 작은 기능 하나에 돌려 2단계 질문과 4단계 승인에서 실제로 멈추는가
- [ ] Stop 훅이 작업 도중 세션 종료를 막고, `status`를 `cancelled`로 바꾸면 풀리는가
- [ ] `--dangerously-skip-permissions`를 쓸 환경과 쓰지 않을 환경을 나눴는가
- [ ] 수정본을 서비스로 제공할 계획이면 AGPL-3.0 의무를 검토했는가

---

[^api]: GitHub, [REST API: stellarlinkco/myclaude](https://api.github.com/repos/stellarlinkco/myclaude)
