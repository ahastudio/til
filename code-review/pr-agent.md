# PR Agent (qodo-ai/pr-agent)

<https://github.com/qodo-ai/pr-agent>

AI 기반 코드 리뷰 자동화 도구. Qodo에서 개발했으며
현재 오픈소스 커뮤니티 프로젝트로 운영된다.

## 커맨드

| 커맨드              | 역할                            |
|---------------------|---------------------------------|
| `/describe`         | PR 제목·설명 자동 생성          |
| `/review`           | 코드 품질 분석 및 문제점 리포트 |
| `/improve`          | 리팩터링·최적화 제안            |
| `/ask <질문>`       | PR 변경사항 대화형 Q&A          |
| `/add_docs`         | docstring 등 문서 자동 추가     |
| `/update_changelog` | CHANGELOG 자동 업데이트         |
| `/generate_labels`  | PR 레이블 자동 생성             |
| `/similar_issue`    | 유사 이슈 탐색                  |

## 사용법

### CLI

```bash
pip install pr-agent

export OPENAI_API_KEY=<key>

# 리뷰
python -m pr_agent.cli --pr_url <PR_URL> review

# PR 설명 생성
python -m pr_agent.cli --pr_url <PR_URL> describe

# 코드 개선 제안
python -m pr_agent.cli --pr_url <PR_URL> improve

# 특정 질문
python -m pr_agent.cli \
  --pr_url <PR_URL> \
  ask "이 변경이 성능에 미치는 영향은?"

# 문서 추가
python -m pr_agent.cli --pr_url <PR_URL> add_docs

# CHANGELOG 업데이트
python -m pr_agent.cli --pr_url <PR_URL> update_changelog
```

Claude 모델 사용 시:

```bash
export ANTHROPIC_API_KEY=<key>
python -m pr_agent.cli \
  --pr_url <PR_URL> \
  -e config.model=anthropic/claude-opus-4-5 \
  review
```

### GitHub Actions

`.github/workflows/pr_agent.yml`:

```yaml
on:
  pull_request:
    types: [opened, reopened, ready_for_review]
  issue_comment:

jobs:
  pr_agent_job:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
      contents: write
    steps:
      - uses: qodo-ai/pr-agent@main
        env:
          OPENAI_KEY: ${{ secrets.OPENAI_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          # 자동 실행 여부 제어
          github_action_config.auto_review: "true"
          github_action_config.auto_describe: "true"
          github_action_config.auto_improve: "false"
```

Claude 모델 사용 시:

```yaml
env:
  config.model: "anthropic/claude-opus-4-5"
  ANTHROPIC_KEY: ${{ secrets.ANTHROPIC_KEY }}
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Gemini 사용 시:

```yaml
env:
  config.model: "gemini/gemini-2.0-flash"
  GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### PR 댓글 트리거

PR 댓글에 커맨드를 작성하면 Bot이 즉시 실행한다.
퍼블릭 저장소라면 자체 배포 없이 `@CodiumAI-Agent`로
즉시 테스트할 수 있다.

```
@CodiumAI-Agent /review
@CodiumAI-Agent /improve --num_code_suggestions=5
@CodiumAI-Agent /ask 이 함수의 시간복잡도는?
@CodiumAI-Agent /describe
```

### `.pr_agent.toml` 로컬 설정

저장소 루트에 `.pr_agent.toml`을 두면 팀 전체에
설정이 적용된다. 전체 템플릿을 복사하지 말고
오버라이드할 항목만 작성한다.

```toml
[config]
model = "anthropic/claude-opus-4-5"

[pr_reviewer]
require_security_review = true
require_tests_review = true
num_max_findings = 5
extra_instructions = """
- 에러 처리가 충분한지 확인하라
- 공개 API 변경이 있으면 반드시 언급하라
"""

[pr_code_suggestions]
focus_only_on_problems = true
num_code_suggestions_per_chunk = 4
```

## 주요 설정 옵션

### `[pr_reviewer]`

| 옵션                                   | 기본값  | 설명                    |
|----------------------------------------|---------|-------------------------|
| `require_score_review`                 | `false` | 1~10 점수 포함 여부     |
| `require_tests_review`                 | `true`  | 테스트 커버리지 검토    |
| `require_estimate_effort_to_review`    | `true`  | 리뷰 난이도 추정        |
| `require_security_review`              | `true`  | 보안 취약점 검토        |
| `require_can_be_split_review`          | `false` | PR 분리 권고 여부       |
| `num_max_findings`                     | `3`     | 최대 지적 항목 수       |
| `enable_review_labels_effort`          | `true`  | 노력도 레이블 자동 부착 |
| `enable_review_labels_security`        | `true`  | 보안 레이블 자동 부착   |
| `persistent_comment`                   | `true`  | 기존 리뷰 댓글 업데이트 |
| `require_todo_scan`                    | `false` | TODO 주석 탐지          |

### `[pr_code_suggestions]` (`/improve`)

| 옵션                               | 기본값  | 설명                       |
|------------------------------------|---------|----------------------------|
| `focus_only_on_problems`           | `true`  | 문제점에만 집중            |
| `num_code_suggestions_per_chunk`   | `3`     | 청크당 제안 수             |
| `max_number_of_calls`              | `3`     | 최대 LLM 호출 횟수         |
| `parallel_calls`                   | `true`  | 병렬 청크 처리             |
| `commitable_code_suggestions`      | `false` | 커밋 가능한 제안 형식      |
| `new_score_mechanism_th_high`      | `9`     | High 등급 점수 임계값      |
| `new_score_mechanism_th_medium`    | `7`     | Medium 등급 점수 임계값    |
| `suggestions_score_threshold`      | `0`     | 최소 노출 점수 (0=전부)    |
| `demand_code_suggestions_self_review` | `false` | 셀프 체크박스 추가      |

### `[pr_description]` (`/describe`)

| 옵션                          | 기본값       | 설명                      |
|-------------------------------|--------------|---------------------------|
| `generate_ai_title`           | `false`      | AI가 제목도 생성          |
| `add_original_user_description` | `true`     | 기존 설명 유지            |
| `enable_pr_diagram`           | `true`       | 변경 흐름 다이어그램 추가 |
| `use_bullet_points`           | `true`       | 불릿 포인트 형식          |
| `collapsible_file_list`       | `'adaptive'` | 파일 목록 접기 방식       |

## 아키텍처 인사이트

### 단일 LLM 호출 철학

대부분의 도구는 LLM 호출 1회로 완료되도록 설계됐다.
멀티턴 대화 방식을 피하고 잘 설계된 단일 프롬프트로
30초 내에 고품질 결과를 내는 전략이다.

비용 민감성을 핵심 설계 원칙으로 삼은 드문 사례다.
기능 확장보다 운영 비용이 먼저 고려된다.

### Self-Reflection — 2-pass 검증

`/improve`는 예외적으로 LLM을 2번 호출한다.

1. **1차 호출**: 코드 개선 제안 생성
2. **2차 호출**: 생성된 제안을 스스로 평가·점수화
   (`self_reflect_on_suggestions()`)

자기 검증 단계를 통해 품질이 낮은 제안은
`suggestions_score_threshold`로 필터링된다.
AI 출력의 할루시네이션을 LLM 스스로 교정하는
구조다. 품질 보장을 위해 비용을 2배 더 쓰는
명시적 트레이드오프다.

### 병렬 청크 처리

큰 PR은 32,000 토큰 단위 청크로 분할된 뒤
`parallel_calls: true`로 병렬 LLM 호출을 수행한다
(`prepare_prediction_main()`).

`final_clip_factor: 0.8`로 결과를 80%까지 클리핑해
중요도 낮은 제안을 자동 제거한다. 기본적으로 최대
3번 호출(청크 3개)이지만 설정으로 늘릴 수 있다.

### PR 압축(Token-Aware Compression)

LLM 컨텍스트 윈도우보다 큰 PR을 처리하기 위해
"토큰 인식 파일 패치 피팅" 기법을 사용한다.
파일별로 토큰 예산을 배분하고 중요도가 낮은
변경사항부터 잘라낸다.

단순 잘라내기가 아니라 파일 우선순위를 계산해서
가장 중요한 변경사항이 컨텍스트에 포함되도록
보장한다.

### Jinja2 템플릿 프롬프트

프롬프트를 Python 코드가 아닌 Jinja2 템플릿
파일로 관리한다. `_get_prediction()`에서 시스템·
유저 프롬프트를 렌더링한다.

설정 파일의 `extra_instructions`만 수정하면
프롬프트 내용을 커스터마이징할 수 있다.
코드 수정 없이 팀 리뷰 스타일을 적용 가능하다.

### LiteLLM 추상화 계층

`LiteLLMAIHandler`가 모든 LLM 호출의 단일 진입점이다.
OpenAI, Claude, Gemini, DeepSeek, Ollama, Azure,
Vertex AI 등을 동일한 인터페이스로 처리한다.

모델 교체가 설정 파일 한 줄 변경으로 가능하다:

```toml
[config]
model = "deepseek/deepseek-chat"
# 또는
model = "ollama/llama3"  # 로컬 모델
```

LangFuse·LangSmith 콜백 연동으로 LLM 호출 추적과
비용 모니터링도 지원한다.

### Claude Extended Thinking 지원

Claude 모델 사용 시 Extended Thinking 기능을
활성화할 수 있다. "thinking" 예산 토큰을 설정하면
Claude가 더 깊이 추론한 뒤 응답한다.

```toml
[config]
model = "anthropic/claude-opus-4-5"
# Extended Thinking은 설정으로 활성화
```

복잡한 아키텍처 리뷰나 보안 분석에 유용하다.

### 자동 점수 메커니즘

`new_score_mechanism: true`가 기본 활성화돼 있다.
Self-Reflection 2차 호출에서 각 제안에 점수를 매긴다.

- **High** (9점 이상): 즉시 적용 권장
- **Medium** (7~8점): 검토 후 판단
- **Low** (7점 미만): 선택적 적용

`suggestions_score_threshold: 0`이 기본값이라
모든 제안이 노출된다. 팀 품질 기준에 맞게
임계값을 올려야 노이즈가 줄어든다.

### YAML 구조화 출력

LLM 응답을 자유 형식 텍스트가 아닌 YAML로 강제한다.
`_prepare_pr_review()`가 YAML 파싱 후 Markdown으로
변환한다.

구조화된 출력 덕분에:
- PR 레이블 자동 부착 (`possible security issue` 등)
- 노력도 자동 계산
- 필드별 후처리 가능

자유 텍스트보다 신뢰도 높은 구조를 LLM에게
강제하는 핵심 설계 결정이다.

### `best_practices.md` 연동

저장소 루트에 `best_practices.md`를 두면
`/improve` 실행 시 이 파일의 내용이 프롬프트에
자동으로 포함된다.

팀의 코딩 컨벤션, 금지 패턴, 필수 패턴을
자연어로 기술하면 AI가 이를 기준으로 리뷰한다.
설정 파일과 달리 일반 Markdown으로 작성 가능하다.

### 플랫폼 추상화 계층

Git 플랫폼별 API 차이를 추상화 계층으로 숨긴다.
도구 로직은 플랫폼에 무관하게 동일하게 동작한다.

```
GitProvider (추상)
├── GithubProvider
├── GitlabProvider
├── BitbucketProvider
├── AzureDevopsProvider
└── GiteaProvider
```

인라인 제안, 댓글 게시, 레이블 부착 등 플랫폼별
지원 범위가 다르지만 미지원 기능은 자동으로 무시된다.
GitHub가 가장 완전하고, 나머지는 부분 지원이다.

### 관찰 가능성(Observability)

LiteLLM 콜백을 통해 각 LLM 호출을 추적한다.

- **LangFuse**: 프롬프트·응답·토큰 사용량 추적
- **LangSmith**: LangChain 생태계 연동
- PR URL, 커맨드명 등 컨텍스트 메타데이터 포함

팀 단위 AI 비용 추적과 리뷰 품질 모니터링에 활용
가능하다.

## 지원 AI 모델

| 제공자    | 모델 ID 예시                      |
|-----------|-----------------------------------|
| OpenAI    | `gpt-5.2-2025-12-11`, `o4-mini`  |
| Anthropic | `anthropic/claude-opus-4-5`       |
| Google    | `gemini/gemini-2.0-flash`         |
| DeepSeek  | `deepseek/deepseek-chat`          |
| Ollama    | `ollama/llama3` (로컬)            |
| Azure     | Azure OpenAI 엔드포인트 설정      |

## 지원 플랫폼

- GitHub (가장 완전한 지원)
- GitLab
- Bitbucket
- Azure DevOps
- Gitea

## 오픈소스 vs 상용(Qodo)

이 저장소는 **Qodo 무료 티어와 별개**다.

오픈소스 버전에 없는 상용 전용 기능:

- 코드베이스 전체를 이해하는 컨텍스트 인식 리뷰
- 팀별 리뷰 스타일 학습·적용
- PR 대시보드 및 분석 리포트

Self-hosted 배포 시 코드는 사용자가 선택한
LLM 제공자에만 전송된다. Qodo 서버를 거치지 않아
데이터 프라이버시가 보장된다.
