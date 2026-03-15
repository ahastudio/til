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

**Claude Code의 statusline API는 Unix 철학을 따른다.**
stdin/stdout 파이프라인으로 플러그인과 통신한다.
tmux 없이도 상태 표시줄을 구현할 수 있게 된 것은
Claude Code가 터미널 네이티브 도구임을 보여준다.

**플러그인 시스템의 진입 장벽이 낮다.**
claude-hud의 핵심 로직은 "stdin에서 JSON 읽기 → 포맷팅 → stdout 출력"이다.
어떤 언어로든 같은 패턴을 구현하면 statusline 플러그인을 만들 수 있다.

**컨텍스트 윈도우 가시성은 실용적이다.**
Claude Code 사용 중 컨텍스트가 얼마나 남았는지 모르면
갑자기 컴팩션이 발생해 대화 흐름이 끊길 수 있다.
실시간 프로그레스 바는 사용자가 세션을 전략적으로 관리하게 해준다.

**autocompact 버퍼 시뮬레이션이 흥미롭다.**
Claude Code는 컨텍스트가 일정 수준에 도달하면 자동으로 압축한다.
claude-hud는 이 임계값(16.5%)을 경험적으로 추정하여
"실제 사용량"과 "압축 후 예상 사용량"을 구분해 보여준다.
공식 API가 아닌 관찰에 기반한 값이라 버전에 따라 달라질 수 있다.
