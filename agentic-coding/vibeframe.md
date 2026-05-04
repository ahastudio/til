# VibeFrame

<https://github.com/vericontext/vibeframe>

## 소개

VibeFrame은 AI 코딩 에이전트와 개발자를 위한 CLI 우선 비디오 에디터다.
텍스트 브리프를 스토리보드 기반 워크플로를 거쳐 완성된 영상으로 변환하며,
Claude Code, Codex, Cursor 같은 AI 에이전트와 직접 통합된다.

TypeScript(97.4%)로 작성되었고 Node.js 20+, FFmpeg, Chrome/Chromium이 필요하다.
MIT 라이선스를 적용한다.

## 워크플로 아키텍처

세 가지 레인(lane)으로 작업을 분류한다.

| 레인            | 목적                       | 입력                          |
| --------------- | -------------------------- | ----------------------------- |
| BUILD           | 다중 장면 완성 영상         | 스토리보드 + 디자인 문서      |
| GENERATE/ASSET  | 독립 미디어 생성            | 직접 프롬프트                 |
| EDIT/REMIX      | 기존 미디어 수정            | 미디어 파일                   |

## CLI

**프로젝트 초기화:**

```bash
vibe init my-video --from "brief description" --json
```

**검증과 계획:**

```bash
vibe storyboard validate my-video --json
vibe plan my-video --json
vibe build my-video --dry-run --max-cost 5 --json
```

**미디어 생성:**

```bash
vibe generate image "prompt" -p openai -o frame.png
vibe generate video "prompt" -p seedance -i frame.png -o motion.mp4
vibe generate narration "text" -o narration.mp3
```

**편집:**

```bash
vibe edit silence-cut video.mp4 -o clean.mp4
vibe edit caption video.mp4 -o captioned.mp4
vibe detect scenes video.mp4
```

**빌드와 렌더:**

```bash
vibe build my-video --max-cost 5 --json
vibe render my-video -o final.mp4 --quality standard --json
vibe inspect render my-video --cheap --json
```

## 에이전트 통합

에이전트 친화적 설계가 프로젝트의 핵심 차별점이다.

- `vibe schema --json`으로 머신 가독형 스키마를 제공한다.
- `CLAUDE.md`, `AGENTS.md` 가이던스 파일을 내장한다.
- `--dry-run`과 비용 추적으로 에이전트가 안전하게 계획을 세울 수 있다.
- `--json` 플래그로 모든 출력을 구조화된 형태로 받는다.
- 반복 수정을 위한 `repair` 명령을 제공한다.

빌트인 채팅보다 외부 에이전트 통합을 우선하고,
`vibe agent`는 선택적 대안으로만 제공한다.

## 저장소 구조

```text
packages/cli/        CLI와 에이전트 모드
packages/core/       타임라인 엔진과 핵심 타입
packages/ai-providers/ 프로바이더 레지스트리
packages/mcp-server/ MCP 서버 패키지
apps/web/            Next.js 랜딩 앱
docs/                공개 문서
```

## 지원 프로바이더

OpenAI, Google, FAL, ElevenLabs, Runway, Kling 등을 지원한다.
API 키를 프로바이더별로 설정하고, 로컬 FFmpeg로 전통적인 편집을 처리한다.

## 분석

### 스토리보드 주도 개발(Storyboard-Driven Development)

VibeFrame이 `STORYBOARD.md`와 `DESIGN.md`를 빌드의 입력으로 삼는 구조는
소프트웨어 개발에서 `AGENTS.md`와 `CLAUDE.md`가 에이전트 행동을 정의하는 것과
같은 패턴이다.
“작업의 의도를 텍스트 파일로 명시하고, 에이전트이 그 의도를 실행한다”는 agentic
워크플로의 핵심 구조가 비디오 제작 도메인에 적용된 것이다.

`--dry-run`과 `--max-cost` 플래그는 AI 에이전트가 비용 초과 없이 계획을 검토하고
승인할 수 있도록 설계된 안전장치다.
코드 에이전트에서 `--no-write` 같은 dry-run 모드가 필수인 것처럼,
비디오 생성 에이전트에서도 동일한 패턴이 필요하다.

### MCP 서버 패키지의 의미

`packages/mcp-server/`가 별도 패키지로 분리된 것은 VibeFrame이 단순한 CLI를 넘어
AI 에이전트의 도구로 포지셔닝된다는 신호다.
Claude Code나 Cursor 같은 코딩 에이전트가 MCP를 통해 VibeFrame 기능을 직접 호출할 수 있다면,
“코드 작성 중에 데모 비디오를 자동으로 생성한다”는 워크플로가 가능해진다.

## 비평

### 강점

에이전트 친화적 설계 원칙이 일관성 있게 적용되어 있다.
`--json` 출력, `--dry-run`, `vibe schema`, `CLAUDE.md` 내장은 AI 에이전트 통합을
처음부터 고려한 설계다.
pnpm 워크스페이스와 Turbo로 구성된 모노레포 구조도 성숙한 오픈소스 프로젝트의
특성을 갖는다.

### 약점

비디오 생성 AI 프로바이더(Runway, Kling, Seedance 등)에 대한 API 비용이 상당하다.
`--max-cost` 플래그가 있지만, 실제로 어떤 작업이 얼마나 비용이 드는지에 대한
가이드가 부족하면 에이전트가 예상치 못한 비용을 발생시킬 수 있다.

또한 “39개 릴리스”와 “활발히 유지된다”고 명시되어 있지만,
초기 Show GN 단계로 실제 사용 사례와 안정성 검증이 부족하다.
AI 비디오 생성 프로바이더 API는 빠르게 변하는 시장이고,
프로바이더가 API를 변경하거나 서비스를 종료할 때의 유지보수 부담이 높다.

## 인사이트

### 비디오 제작의 agentic 화

텍스트 → 코드 변환이 코딩 에이전트의 핵심 역량이 된 것처럼,
텍스트 → 비디오 변환도 에이전트의 일상적 작업이 될 수 있다.
VibeFrame이 `STORYBOARD.md` 기반 워크플로를 제안하는 것은 이 전환을
“결과물(영상)”이 아닌 “과정(스토리보드 → 계획 → 빌드)”으로 구조화하려는 시도다.

코딩 에이전트에서 “코드 먼저 짜고 나중에 테스트”보다 “테스트 먼저 작성하고
테스트를 통과하는 코드를 작성”이 더 안정적이듯,
비디오 에이전트에서도 “비디오 먼저 생성”보다 “스토리보드를 먼저 정의하고
검증한 뒤 생성”이 비용과 품질 모두에서 유리하다.

### CLI-first가 에이전트 도구의 표준

VibeFrame이 GUI보다 CLI를 우선하는 것은 Agentic 시대의 도구 설계 방향과 일치한다.
AI 에이전트는 GUI를 다루기 위해 컴퓨터 비전이 필요하지만, CLI는 텍스트 입출력만으로
제어할 수 있다.
`--json` 플래그와 `vibe schema --json`은 에이전트가 사람의 개입 없이 VibeFrame을
완전히 자동화할 수 있게 해주는 핵심 설계다.

“에이전트가 쓰기 좋은 CLI”의 요건은 사람이 쓰기 좋은 CLI와 다르다.
모호한 자연어 출력보다 구조화된 JSON, 확인 대화상자보다 `--dry-run`,
대화형 선택보다 명시적 플래그가 에이전트 친화적 CLI의 특성이다.
VibeFrame은 이 요건을 의식적으로 반영한 드문 사례다.

### AI 영상 도구 생태계의 조각화 문제

VibeFrame이 OpenAI, Google, FAL, ElevenLabs, Runway, Kling을 지원하는 것은
AI 영상 생성 도구 생태계의 심한 조각화를 반영한다.
코딩 도구에서 GitHub Copilot이나 Claude Code가 특정 AI 프로바이더에 집중할 수 있는
것과 달리, 영상 도구는 이미지 생성, 비디오 생성, 음성 합성, 음악 생성을 각각 다른
프로바이더에서 조합해야 한다.

이 조각화는 추상화 레이어로서의 VibeFrame의 가치를 높이는 동시에
유지보수 부담도 높인다.
프로바이더 하나가 API를 바꾸면 관련 파이프라인 전체가 깨질 수 있다.
이 문제를 해결하는 안정적인 프로바이더 추상화 레이어가 AI 영상 도구 생태계에서
장기적으로 중요한 인프라가 될 것이다.
