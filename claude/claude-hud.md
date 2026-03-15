# Claude HUD

> Claude Code 세션의 실시간 상태를 터미널 스테이터스라인에 표시하는 플러그인.
> 컨텍스트 윈도우 사용량, 활성 도구, 서브에이전트, Todo 진행률, Git 브랜치 등을
> 별도 창 없이 한눈에 볼 수 있다.

<https://github.com/jarrodwatts/claude-hud>

## 설치와 설정

```bash
# 1. 마켓플레이스에서 추가
/plugin marketplace add jarrodwatts/claude-hud

# 2. 설치
/plugin install claude-hud

# 3. 초기 설정 (인터랙티브)
/claude-hud:setup
```

설정 변경은 `/claude-hud:configure`로 한다.
Full, Essential, Minimal 프리셋이 있고 JSON 직접 편집도 가능하다.

## 표시 항목

| 항목             | 설명                                        |
| ---------------- | ------------------------------------------- |
| 프로젝트 경로    | 1~3단계 디렉터리 깊이 설정 가능             |
| 컨텍스트 윈도우  | 시각적 프로그레스 바로 잔여량 표시           |
| 토큰 사용률      | Pro/Max/Team 구독자용 API 사용량            |
| 활성 도구        | Read, Edit, Grep 등 현재 실행 중인 도구     |
| 서브에이전트     | 활동 중인 에이전트 상태                     |
| Todo 진행률      | 완료/전체 태스크 수                         |
| Git 브랜치       | 현재 브랜치, dirty 상태, ahead/behind 카운트 |
| 세션 시간        | 세션 경과 시간                              |
| 설정 파일 카운트 | CLAUDE.md, MCP, hooks 등 감지된 설정 파일 수 |

두 가지 레이아웃 모드가 있다.
Expanded는 여러 줄로 모든 정보를 보여주고,
Compact는 한 줄로 핵심만 보여준다.

## 아키텍처

```text
Claude Code → stdin (JSON) → claude-hud → stdout → 터미널 스테이터스라인
```

Claude Code의 네이티브 statusline API를 사용한다.
`~/.claude/settings.json`에 statusLine 명령을 등록하면 Claude Code가
약 300ms 간격으로 세션 데이터를 stdin으로 전달하고,
claude-hud가 파싱하여 포맷된 문자열을 stdout으로 출력한다.

### 주요 모듈

| 모듈                | 역할                                                   |
| ------------------- | ------------------------------------------------------ |
| `src/index.ts`      | 진입점. stdin 읽기, 데이터 수집, 렌더링 호출           |
| `src/stdin.ts`      | stdin JSON 파싱, 모델명 정규화, 컨텍스트 퍼센트 계산   |
| `src/config.ts`     | 설정 로드, 검증, 기본값 병합, 레거시 마이그레이션       |
| `src/transcript.ts` | JSONL 트랜스크립트 파싱. 도구·에이전트·Todo 추출       |
| `src/git.ts`        | Git 브랜치, dirty 상태, ahead/behind 카운트 조회       |
| `src/usage-api.ts`  | Anthropic OAuth로 토큰 사용량 API 조회 (5분 캐싱)      |
| `src/speed-tracker.ts` | 슬라이딩 윈도우(2초)로 출력 토큰 속도(tok/s) 추적   |
| `src/config-reader.ts` | CLAUDE.md, MCP, hooks 등 설정 파일 카운트           |
| `src/render/`       | ANSI 이스케이프 처리, 와이드 문자 감지, 줄바꿈 렌더링 |

### stdin 데이터

Claude Code가 전달하는 JSON 구조:

```json
{
  "model": {"display_name": "Opus", "id": "claude-opus-4-..."},
  "context_window": {
    "current_usage": {"input_tokens": 45000},
    "context_window_size": 200000,
    "used_percentage": 23
  },
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/project/path"
}
```

`used_percentage`는 Claude Code v2.1.6+에서 제공한다.
없으면 수동 계산으로 폴백한다.
autocompact 동작을 시뮬레이션하기 위해 16.5% 버퍼를 적용하여
"버퍼드 퍼센트"를 별도로 계산한다.

Bedrock 모델 ID(`anthropic.claude-3-5-sonnet-...`)를
"Claude Sonnet 3.5" 형식으로 정규화하는 로직도 있다.

### 트랜스크립트 파싱

트랜스크립트 파일을 `readline`으로 스트리밍하며 JSON 엔트리를 파싱한다.
content 블록에서 세 가지를 식별한다.

1. **Tool Use 블록** — 도구 ID, 이름, 시작 시각 추출
2. **Task 블록** — "Task" 도구 호출 시 서브에이전트로 등록
3. **Todo 블록** — TodoWrite, TaskCreate, TaskUpdate 처리

결과 블록이 나타나면 해당 도구의 완료 시각을 갱신한다.
최대 20개 도구, 10개 에이전트까지 추적한다.

### 터미널 렌더링

`Intl.Segmenter`로 그래핌(grapheme) 단위 문자 폭을 계산한다.
CJK 문자와 이모지를 2칸으로 처리하고,
ANSI 이스케이프 시퀀스를 제거한 뒤 실제 표시 폭을 측정한다.
`|` 구분자 위치에서 줄바꿈하되 `[model | provider]` 같은 괄호 쌍은 보존한다.

## 비평

### 잘한 점

**제로 디펜던시.** 런타임 의존성이 없다.
`@types/node`와 `typescript`만 devDependencies에 있다.
Node.js 내장 모듈만으로 전부 구현했다.

**입출력 설계가 깔끔하다.** stdin → 파싱 → stdout 파이프라인은
Claude Code의 statusline API와 자연스럽게 맞물린다.
별도 데몬이나 소켓 없이 프로세스 파이프만으로 동작한다.

**와이드 문자 처리.** CJK 폭 계산과 `Intl.Segmenter` 폴백까지
갖춘 터미널 도구는 드물다. 한국어·일본어 환경에서도 레이아웃이 깨지지 않는다.

**설정 검증이 방어적이다.** 모든 설정값에 타입 검증 함수가 있고,
레거시 포맷 마이그레이션도 지원한다. 잘못된 설정이 들어와도 기본값으로
폴백한다.

**보안을 의식한 구현.** Git 명령 실행에 `execFileSync`를 사용하고
절대 경로로 호출하여 셸 인젝션과 PATH 하이재킹을 방지한다.

### 아쉬운 점

**TypeScript 비율이 41.8%에 불과하다.** `dist/` 디렉터리를 저장소에
커밋하고 있어서 컴파일된 JavaScript가 통계에 잡힌다.
`.gitignore`에 `dist/`를 추가하고 CI에서 빌드하는 것이 일반적인 관행이다.

**Git 명령에 1초 타임아웃.** `git status`와 `git rev-list`에 1초
타임아웃을 걸었는데, 대규모 모노레포에서는 부족할 수 있다.
반대로 300ms 갱신 주기에 비해 1초는 긴 편이다.
타임아웃을 설정 가능하게 만들거나 캐싱 전략이 필요하다.

**트랜스크립트 파싱의 매직 넘버.** 도구 20개, 에이전트 10개 상한이
하드코딩되어 있다. 복잡한 세션에서 이 한계에 도달하면 최신 정보가
누락될 수 있다.

**빈 catch 블록이 많다.** 대부분의 에러 핸들링이 `catch {}`로
조용히 삼킨다. 의도적인 graceful degradation이지만,
디버깅 시 문제 추적이 어렵다.

**사용량 API가 macOS Keychain에 의존한다.** OAuth 토큰을
macOS Keychain에서 읽기 때문에 Linux/Windows에서는
토큰 사용량 표시가 제한된다.

## 인사이트

### AI 코딩 도구의 관찰 가능성 공백

claude-hud가 4,500+ 스타를 받은 것은 단순히 "편리해서"가 아니다.
AI 코딩 도구에 근본적인 관찰 가능성(observability) 공백이 있다는 신호다.

Kubernetes에 Prometheus가 필요했듯, Claude Code에도 세션 상태를
외부에서 모니터링하는 도구가 필요했다. 오케스트레이터가 자체 관찰
도구를 충분히 제공하지 않으면 커뮤니티가 그 틈을 메운다.
Claude Code가 `/context` 명령을 제공하지만, 그것은 "묻는 행위"다.
claude-hud는 "묻지 않아도 보이는 상태"를 만든다.
pull 방식에서 push 방식으로의 전환이 핵심 가치다.

### 불안정한 API 위에 짓는 도구의 딜레마

claude-hud는 Claude Code의 stdin JSON 구조에 전적으로 의존한다.
이 구조는 공식 API가 아니다. `used_percentage` 필드가 v2.1.6에서야
추가된 것처럼, 언제든 바뀔 수 있다.

이런 구조 위에 도구를 만드는 것은 의식적인 트레이드오프다.
안정성을 포기하는 대신 플랫폼이 제공하지 않는 기능을 먼저 구현한다.
커뮤니티 도구가 충분히 인기를 얻으면 플랫폼이 해당 API를 안정화할
동기가 생긴다. Greasemonkey가 브라우저 확장 API를 만들어낸 것과
같은 패턴이다.

autocompact 버퍼 16.5%를 경험적으로 역추정한 것이 대표적이다.
Claude Code의 내부 동작을 관찰로 추정하고,
그 추정 위에 기능을 구축한다.
공식 값이 아니라 버전에 따라 달라질 수 있지만,
"없는 것보다 대략적인 것이 낫다"는 실용주의적 판단이다.

### 토큰 가시성이 사용자 행동을 바꾼다

전기 사용량 모니터를 설치하면 소비 패턴이 바뀌듯,
컨텍스트 사용량을 실시간으로 보여주면 사용자의 상호작용 방식이 달라진다.

프로그레스 바가 70%를 넘기면 사용자는 의식적으로 질문을 짧게 하거나,
새 세션을 시작할 타이밍을 잡거나, 불필요한 파일 읽기를 줄인다.
이것은 단순한 정보 표시가 아니라 행동 넛지(nudge)다.

tok/s 속도 표시도 마찬가지다. 응답이 느릴 때 "기다려야 하는지,
문제가 있는지"를 판단하는 근거가 된다.
불확실성을 줄이는 것만으로 사용자 경험이 개선된다.

### 터미널 AI의 IDE화

claude-hud는 터미널에 IDE의 스테이터스 바를 이식한다.
VS Code 하단의 상태 표시줄이 보여주는 것과 본질적으로 같다.
Git 브랜치, 언어 정보, 에러 카운트 대신
컨텍스트 사용량, 활성 도구, 에이전트 상태를 보여줄 뿐이다.

이것은 터미널 기반 AI 도구가 IDE와 수렴 진화하고 있다는 증거다.
게임 HUD에서 체력/마나를 실시간으로 보여주듯,
AI 코딩 세션에서 컨텍스트/토큰을 실시간으로 보여주는 것은
"자원 관리 게임"이라는 은유가 실제로 적확하다는 뜻이다.

### dist/ 커밋은 의도적 타협이다

일반적으로 `dist/`를 Git에 커밋하지 않는다.
하지만 Claude Code 플러그인은 `npm install` 없이
저장소를 직접 클론하여 실행하는 구조다.
빌드 스텝 없이 바로 동작해야 하므로 컴파일 결과물을 포함한다.

이것은 npm 패키지가 아닌 "Git 저장소가 배포 단위인 생태계"의
실용적 선택이다. 소스와 빌드 산출물의 동기화 문제를 감수하되,
설치 마찰을 최소화하는 쪽을 택한 것이다.

### stdin/stdout 파이프라인의 함의

Claude Code가 플러그인과 stdin/stdout으로 통신한다는 것은
Unix 철학 그 자체다. 어떤 언어로든 "JSON 읽기 → 문자열 출력"만
구현하면 statusline 플러그인이 된다.
Python, Rust, Go, 심지어 셸 스크립트로도 가능하다.

이 설계는 플러그인 생태계의 진입 장벽을 극단적으로 낮춘다.
SDK도, 타입 정의도, 빌드 도구도 필요 없다.
하지만 그 대가로 API 계약이 느슨하고, 버전 간 호환성 보장이 없다.
자유도와 안정성의 트레이드오프다.
