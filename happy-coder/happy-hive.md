# Happy Hive - 분산 에이전트 오케스트레이션

Happy Coder의 멀티머신 인프라를 AI 에이전트의
분산 실행 기반으로 활용하는 아이디어. 사람이
에이전트 하나를 제어하는 기존 모델을 넘어,
에이전트가 다른 에이전트를 생성·조율·감독하는
패턴을 탐구한다.

## 핵심 전제

Happy Coder가 이미 갖춘 것:

- 여러 머신에 상주하는 `happy daemon`
- 로컬 HTTP API (`/spawn-session`, `/list`)
- 원격 WebSocket RPC (`spawn-happy-session`)
- 세션 간 메시지 전송 (`happy-agent send`)
- 세션 상태 조회 (`happy-agent status`)
- 대기 (`happy-agent wait`)

에이전트(Claude Code)가 bash를 쓸 수 있으므로,
이 인프라를 프로그래밍적으로 호출할 수 있다.

## 세 가지 패턴

### 패턴 1: 서브 에이전트 (Sub-Agent)

하나의 "지휘" 세션이 여러 "작업" 세션을
생성하고 결과를 수집하는 계층 구조.

```
지휘 세션 (머신 A)
├── 작업 세션 1: 프론트엔드 리팩토링
├── 작업 세션 2: 백엔드 API 추가
└── 작업 세션 3: 테스트 작성
```

실현 방법:

```bash
# 1. 데몬 포트 확인
PORT=$(cat ~/.happy/daemon.state.json \
  | jq -r '.httpPort')

# 2. 로컬 세션 생성
curl -s -X POST \
  http://127.0.0.1:$PORT/spawn-session \
  -H 'Content-Type: application/json' \
  -d '{"directory": "/project/frontend"}'

# 3. 활성 세션 목록 조회
curl -s -X POST \
  http://127.0.0.1:$PORT/list

# 4. 생성된 세션에 작업 지시
happy-agent send <session-id> \
  "Button 컴포넌트를 리팩토링해줘" --wait

# 5. 결과 확인
happy-agent history <session-id> \
  --limit 5 --json
```

로컬 HTTP API에 인증이 없으므로(`127.0.0.1`
바인딩만으로 보호) bash에서 바로 호출 가능하다.

### 패턴 2: 에이전트 팀 (Agent Team)

동등한 세션들이 공유 파일시스템을 통해
협업하는 수평 구조. 지휘자 없이 각 세션이
자율적으로 작업하되, 약속된 경로로 상태를
교환한다.

```
세션 A ←→ /tmp/hive/status.json ←→ 세션 B
세션 C ←→ /tmp/hive/status.json ←→ 세션 D
```

조율 규약 예시:

```json
{
  "task": "v2.0 릴리스 준비",
  "assignments": {
    "sess_abc": {
      "role": "프론트엔드",
      "dir": "/project/frontend",
      "status": "working"
    },
    "sess_def": {
      "role": "백엔드",
      "dir": "/project/backend",
      "status": "done"
    }
  },
  "artifacts": [
    "/tmp/hive/frontend-report.md",
    "/tmp/hive/backend-report.md"
  ]
}
```

각 세션의 `CLAUDE.md`에 조율 규약을 명시하면
에이전트가 자연스럽게 따를 수 있다:

```markdown
## 협업 규약

- 작업 전 `/tmp/hive/status.json`을 읽고
  자기 상태를 "working"으로 갱신할 것.
- 작업 완료 시 결과를 artifacts에 등록하고
  상태를 "done"으로 갱신할 것.
- 다른 세션의 디렉토리를 직접 수정하지 말 것.
```

### 패턴 3: 에이전트 웜 (Agent Worm)

하나의 세션이 자신을 복제하며 머신을
넘나드는 자기 증식 패턴. "웜"이라는 이름은
자기 전파 특성에서 따왔다.

```
머신 A: 세션 → (spawn) → 머신 A: 세션'
                       → 머신 B: 세션''
                       → 머신 C: 세션'''
```

현재 기술적 한계: 원격 머신에 세션을 생성하려면
`spawn-happy-session` WebSocket RPC를 호출해야
하는데, 이를 위해서는 릴레이 서버 인증, 대상
머신 ID, 머신의 암호화 키가 필요하다. CLI에
이 기능이 노출되어 있지 않으므로 커스텀
WebSocket 클라이언트를 구현해야 한다.

로컬 머신 내 증식은 가능하다:

```bash
# 자기 복제: 새 디렉토리에서 새 세션 생성
PORT=$(jq -r '.httpPort' \
  ~/.happy/daemon.state.json)
curl -s -X POST \
  http://127.0.0.1:$PORT/spawn-session \
  -d "{\"directory\": \"$NEW_DIR\"}" \
  -H 'Content-Type: application/json'
```

## 기술적 실현 가능성

### 가능한 것

| 기능                   | 방법                              |
| ---------------------- | --------------------------------- |
| 로컬 세션 생성         | `POST /spawn-session` (인증 불요) |
| 세션 목록 조회         | `POST /list`                      |
| 세션에 메시지 전송     | `happy-agent send`                |
| 세션 완료 대기         | `happy-agent wait` (5분 타임아웃) |
| 세션 이력 읽기         | `happy-agent history`             |
| 세션 상태 확인         | `happy-agent status`              |
| 세션 종료              | `happy-agent stop`                |
| 파일시스템으로 데이터 교환 | 같은 머신이면 자유롭게        |

### 불가능하거나 어려운 것

| 기능                       | 이유                              |
| -------------------------- | --------------------------------- |
| 원격 머신에 세션 생성      | CLI 미노출. WebSocket + 암호화 필요 |
| 커스텀 환경 변수 전달      | 5개 고정 키만 허용                |
| 세션 출력 실시간 스트리밍  | API 미존재                        |
| 세션 간 직접 IPC           | 메커니즘 없음                     |
| 머신 목록 조회             | `happy-agent`에 명령 없음         |

### 조율 수단 비교

| 수단                   | 장점            | 단점                  |
| ---------------------- | --------------- | --------------------- |
| 파일시스템             | 빠름, 단순      | 같은 머신만           |
| `happy-agent send`     | 크로스머신 가능 | 메시지가 대화에 섞임  |
| `CLAUDE.md`에 규약 명시 | 에이전트가 자연스럽게 따름 | 사전 설정 필요 |
| Git 브랜치             | 이력 추적 가능  | 충돌 위험             |

## 핵심 한계

### 감독자 부재

Happy Coder의 설계 의도는 "사람이 에이전트를
감독"하는 것이다. 에이전트가 에이전트를
생성하면 감독 고리가 끊긴다. 서브 에이전트가
잘못된 방향으로 달려도 지휘 세션이 이를
실시간으로 감지하기 어렵다.
`happy-agent wait`의 5분 타임아웃이 유일한
안전장치다.

### 인터랙티브 CLI의 벽

`happy`는 인터랙티브 TUI다. bash에서 생성은
가능하지만 생성된 세션의 TUI를 프로그래밍적으로
제어할 수는 없다. `happy-agent send`로 메시지를
보내는 것이 유일한 입력 수단이며, 이는 사용자가
직접 타이핑하는 것과 동일하게 처리된다.

### 비용 폭발

세션 하나가 세션 세 개를 만들고, 각각이 또 세
개를 만들면 지수적으로 증가한다. 각 세션이
독립적으로 API를 호출하므로 비용 제어가
어렵다. 최대 동시 세션 수를 조율 규약에
명시해야 한다.

### 크로스머신의 높은 장벽

로컬 머신 내 오케스트레이션은 비교적 쉽지만,
여러 머신에 걸친 오케스트레이션은 현재
인프라로 사실상 불가능하다. `happy-agent`에
머신 관리 명령이 추가되거나, 로컬 HTTP API가
원격 머신 프록시를 지원해야 한다.

## 실현 가능한 최소 시나리오

현재 인프라로 가장 현실적인 패턴:

1. 사람이 모바일에서 "지휘" 세션을 하나 띄운다.
2. 지휘 세션의 `CLAUDE.md`에 오케스트레이션
   규약을 명시한다.
3. 지휘 세션이 `/spawn-session`으로 같은
   머신에 작업 세션 2~3개를 생성한다.
4. 각 작업 세션의 디렉토리에 `CLAUDE.md`로
   역할과 조율 규약을 미리 배치한다.
5. `happy-agent send`로 초기 프롬프트를 전달한다.
6. `happy-agent wait`로 완료를 기다린 뒤
   결과를 파일시스템에서 수집한다.
7. 사람은 모바일에서 지휘 세션의 진행을 감독한다.

이 시나리오에서 사람은 지휘 세션만 감독하고,
지휘 세션이 나머지를 관리한다. 감독의 깊이는
1단계(사람 → 지휘 세션)로 유지된다.

## `happy-agent`에 바라는 것

이 패턴을 공식 지원하려면:

- `happy-agent machines` — 연결된 머신 목록
- `happy-agent spawn --machine <id>` — 원격
  세션 생성
- `happy-agent send`의 스트리밍 모드 — 실시간
  출력 수신
- 커스텀 환경 변수 전달 — 조율 메타데이터 주입
- 세션 그룹 개념 — 관련 세션을 묶어서 일괄 관리
