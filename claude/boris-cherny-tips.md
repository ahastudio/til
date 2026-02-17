# Boris Cherny의 Claude Code 사용 노하우

- 2026년 1월 3일 트윗 <https://twitter.com/bcherny/status/2007179832300581177>
- 2026년 2월 1일 트윗 <https://twitter.com/bcherny/status/2017742741636321619>

Boris Cherny는 Claude Code의 창시자입니다. 그가 공유한 실전 사용 팁을
정리합니다.

## 병렬 작업

### Git Worktree 활용

3~5개의 git worktree를 동시에 실행하고, 각각 별도의 Claude 세션을 병렬로
운영합니다. Claude Code 팀 내부에서 최고의 생산성 향상 팁으로 꼽힙니다.

```bash
# worktree 생성
git worktree add ../feature-1 -b feature-1
git worktree add ../feature-2 -b feature-2
```

### 터미널 탭 번호 지정

터미널에서 5개의 Claude를 병렬 실행합니다. 탭에 1~5 번호를 붙여 관리하고, 시스템
알림으로 Claude가 입력을 기다리는지 확인합니다.

### 웹 + 로컬 병행

claude.ai/code에서 5~10개의 Claude를 추가로 운영합니다. 로컬 Claude와 웹
Claude를 유연하게 전환하며 작업합니다. iOS 앱에서 세션을 시작하고 나중에
확인하는 방식도 활용합니다.

## 모델 선택

모든 작업에 **Opus 4.5 with thinking**을 사용합니다. 더 크고 느리지만,
스티어링이 적게 필요하고 도구 사용 능력이 뛰어나서 결과적으로 더 빠릅니다.

## CLAUDE.md 활용

### 팀 공유

팀 전체가 하나의 CLAUDE.md 파일을 공유합니다. Git에 체크인하고, 팀원 모두가 주
단위로 기여합니다.

### 지속적 업데이트

Claude가 잘못된 동작을 할 때마다 CLAUDE.md에 추가합니다. "CLAUDE.md를
업데이트해서 같은 실수를 반복하지 않도록 해라"라고 매번 수정 시 지시합니다.

Claude는 스스로 지켜야 할 규칙을 매우 잘 문서화합니다.

## Plan 모드 활용

대부분의 세션을 **Plan 모드**(Shift+Tab 두 번)로 시작합니다.

1. Plan 모드에서 Claude와 계획을 충분히 다듬음
2. 계획이 마음에 들면 auto-accept 모드로 전환
3. Claude가 한 번에(1-shot) 완성

## 슬래시 명령어

매일 수십 번 반복하는 "inner loop" 워크플로를 슬래시 명령어로 만듭니다.
`.claude/commands/` 디렉토리에 Git으로 관리합니다.

```bash
# 예: /commit-push-pr
# 매일 수십 번 사용하는 커밋-푸시-PR 워크플로
```

반복적인 프롬프팅을 줄이고, Claude도 이 워크플로를 활용할 수 있습니다.

## 서브에이전트 활용

자주 사용하는 서브에이전트:

| 서브에이전트        | 용도                               |
| ------------------- | ---------------------------------- |
| **code-simplifier** | Claude 작업 완료 후 코드 단순화    |
| **verify-app**      | 엔드투엔드 테스트를 위한 상세 지침 |

슬래시 명령어와 마찬가지로, 대부분의 PR에서 반복되는 워크플로를 자동화합니다.

## Claude를 리뷰어로 활용

"이 변경사항을 엄격히 검토하고, 내가 테스트를 통과할 때까지 PR 만들지 마"라고
지시합니다.

## 피드백 루프의 중요성

Claude가 스스로 작업을 검증할 수 있는 피드백 루프를 제공하는 것이 최종 결과물
품질을 **2~3배** 높이는 가장 중요한 요소입니다.
