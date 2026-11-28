# Claude Dungeon

<https://github.com/thousandsky2024/claude-pixel-agent-web>

HN 토론: <https://news.ycombinator.com/item?id=47206796> (1점, 1개 댓글)

## 소개

Claude Dungeon은 Claude Code 세션을 던전의 픽셀 기사로 보여 주는 웹 앱이다.
세션 하나가 영웅 하나이고 도구 사용에 따라 영웅이 방 사이를 걸어 다닌다.
Express, React, Phaser 3로 만들었고 Manus로 뼈대를 만든 티가 남아 있다.
MIT 라이선스이다.
2026년 11월 25일 GitHub API로 본 별은 17개, 생성일은 2026년 3월 1일,
마지막 커밋은 3월 3일, 커밋은 27개이다.
저장소의 이름은 claude-pixel-agent-web이고 별도 홈페이지는 없다.
번들된 itch.io의 Metroidvania 스프라이트(원본 `.aseprite` 포함)에는
자체 라이선스가 없고 README의 크레딧은 `https://itch.io`만 링크한다.

저장소를 받아 코드를 읽었으며 설치하거나 실행하지 않았다.
`server/websocket.ts`, `server/bridge.ts`, `server/routers/agents.ts`,
`server/_core/index.ts`, 브리지 스크립트, 테스트 3개와 Phaser 렌더러의 일부를 직접 읽어 확인했다.
`server/_core`의 Manus 템플릿 파일은 이름만 보았고 읽지 않았다.

## 동작 방식

### 모듈 구성과 핵심 상수

| 파일                                         | 줄 수 | 역할                                                  |
| -------------------------------------------- | ----- | ----------------------------------------------------- |
| `server/_core/index.ts`                      | 74    | Express, tRPC, WebSocket, 브리지 라우터를 묶는 진입점 |
| `server/websocket.ts`                        | 762   | 대화 기록 감시, 줄 해석, 영웅 상태, 브로드캐스트      |
| `server/routers/agents.ts`                   | 693   | 영웅 타입, 클래스 판정, 스킬·에이전트 파일 CRUD       |
| `server/bridge.ts`                           | 150   | 브리지 API 키와 `/api/bridge` REST                    |
| `client/src/components/DungeonMapPhaser.tsx` | 782   | Phaser 장면, 길찾기, 스프라이트                       |
| `client/src/hooks/useHeroSocket.ts`          | 183   | WebSocket 클라이언트                                  |

`server/websocket.ts` 상단의 상수는 감시 주기 1초, 대기 지연 10초,
활성 세션 창 5분, 만료 2분, 프로세스 확인 15초이다.
`server/index.ts`는 정적 파일만 서빙하는 별도 서버이고 `package.json`의 `dev`와 `build`는 `server/_core/index.ts`를 쓴다.

### 대화 기록만 읽는다

Claude Code 훅은 쓰지 않고 표준 입력도 쓰지 않으며 `settings.json`을 건드리지 않는다.
`server/websocket.ts`가 `~/.claude/projects/**/*.jsonl`을 `fs.watch`와 1초 주기 확인으로 읽는다.
5분 안에 수정된 파일만 대상이고 파일 하나가 영웅 하나이다.
`processLine`이 `assistant` 기록의 `tool_use` 블록과 `user` 기록의 `tool_result` 블록을 읽고
도구 이름을 부분 문자열로 방과 상태에 대응시킨다.
Bash, Write, Edit, Task는 보스 경기장, 웹과 계획은 상점, 읽기와 글롭은 던전 메인이다.
2분 동안 쓰기가 없거나 `pgrep -f claude`로 프로세스가 안 보이면 영웅을 내보낸다.
정확히는 15초마다 `pgrep`을 돌려 `claude`가 포함된 프로세스가 시스템에 하나도 없으면 영웅 전부를 지운다.
하나라도 있으면 파일이 90초 넘게 바뀌지 않은 영웅만 지운다.
`bridge/claude-dungeon-bridge.mjs`는 같은 해석기를 더 거칠게 다시 구현한 것이다.

### 줄 해석과 경험치

`processLine`은 JSON 파싱에 실패한 줄을 조용히 버린다.
`tool_use` 블록마다 경험치 5를 더하고 경험치가 `level * 100` 이상이면 레벨을 올려
최대 체력 10, 최대 마력 5를 늘리고 체력과 마력을 가득 채운다.
도구 이름이 `parent_tool_use_id`를 가진 기록에서 왔으면 `subAgentTools`에, 아니면 `activeTools`에 넣는다.
`tool_result`가 오면 해당 `tool_use_id`를 지우고, 남은 도구가 없으면 10초 뒤 휴식 상태로 돌린다.
휴식 상태는 `rest_area` 방에서 체력 10, 마력 15를 회복한다.
`result`나 `turn_end` 기록은 2초 뒤 휴식으로 보내지만
이 기록을 Claude Code가 실제로 남기는지는 확인하지 못했다.
`readNewLines`는 바이트 오프셋부터 읽고 빈 줄을 걸러 낸다.
`startWatchingFile`은 오프셋을 0으로 되돌린 뒤 파일 전체를 다시 해석한다.
`handleNewTranscriptFile`은 프로젝트 디렉터리의 `fs.watch` 콜백에서 .jsonl 변경마다 불리고
이미 있는 영웅에도 `startWatchingFile`을 다시 부르므로,
파일이 바뀔 때마다 기록 전체가 다시 해석되어 경험치가 중복될 수 있다고 코드에서 읽었다.
이 동작은 실행해 확인하지 않았다.

### 서버와 화면

`server/_core/index.ts`가 호스트 없이 `listen(port)`을 호출한다.
WebSocket `/api/ws/agents`에 인증이 없고 tRPC 절차가 모두 `publicProcedure`이며
브리지 키는 `Math.random` 기반이다(`server/bridge.ts`).
화면은 README의 설명과 달리 Phaser 3이고 길찾기는 타일 격자의 너비 우선 탐색이다.
영웅의 상태는 대기, 전투, 시전 또는 상점, 휴식, 퇴장이며
`walking`과 `hurt`는 서버에서 대입하는 곳이 없다.
클라이언트는 영웅 데이터를 찾지 못했을 때 `walking`을 대신 쓴다(`DungeonMapPhaser.tsx`).
싸움이나 시전 상태이면 공격 애니메이션과 붉은 빛이 나오고 보스도 공격 애니메이션으로 바뀐다.
서브 에이전트의 도구는 자식 영웅이 아니라 `HeroPanel.tsx`가 도구 목록 하나로 합쳐 보여 준다.
영웅 클래스(warrior, mage, cleric)는 도구 비율로 정하지만 스프라이트는 기사 하나뿐이다.

### 디스크와 외부 호스트

`~/.claude-dungeon/heroes.json`과 `config.json`을 쓰고,
스킬과 에이전트 편집기가 `~/.claude/skills/*/SKILL.md`, `~/.claude/agents/*.md`를 쓴다.
브리지의 기본 서버 주소는 제3자의 호스팅 주소(`claudepixl-…manus.space`)이다.
다만 `pushHeroes`는 API 키가 비어 있으면 전송하지 않고 건너뛰므로,
키 없이 실행하면 아무것도 나가지 않는다.
키를 주면 `heroes` 배열(프로젝트 경로, 세션 파일 경로, Bash 명령 앞 50자 포함)을
10초 제한으로 POST한다.
서버는 이 JSON을 검증 없이 받아 모든 브라우저에 중계한다(`getBroadcastCallbacks`).

## 분석

### 읽기만 하는 구조의 한계

대화 기록 읽기만으로 구성해 설정을 건드리지 않는 장점이 있다.
대신 기록이 쓰이는 시점에야 반응해 훅 기반보다 늦고,
권한 대기 같은 신호는 얻을 수 없다.
게임 요소(영웅 등급, 방별 의미)가 중심이라 Pixel Agents의 사무실 은유와 다른 길을 간다.

## 비평

### 열린 편집기와 키

모든 tRPC 절차가 공개라서 네트워크에서 닿는 누구든 스킬과 에이전트 편집기를 쓸 수 있고
`agents.bridgeApiKey`로 API 키도 읽을 수 있다.
`GET /api/bridge/key`의 “로컬 전용” 확인은 `req.hostname`을 쓰는데
이는 Host 헤더에서 오므로 우회될 수 있다.
생성 절차만 `^[a-z0-9-_]+$`로 이름을 검사하고,
수정과 삭제 절차는 임의의 `skillName` 문자열을 받아 `path.join` 뒤에 `rmSync`를 `recursive:true`로 부른다.
`projectPath`도 아무 문자열이어서 `..`가 든 이름이 스킬 디렉터리 밖을 가리킬 수 있음을 직접 읽어 확인했다.
`express.json`의 본문 한도가 50MB이고 CORS나 Origin 검사는 코드에서 찾지 못했다.

### 설명과 코드의 차이

- README는 읽기를 신성한 성소로 보낸다고 하지만 코드는 던전 메인으로 보낸다.
- 웹 검색은 README에서 시전이고 코드에서는 상점의 `shopping`이다.
- 대기하는 영웅은 던전 메인이 아니라 선술집으로 간다.
- 서브 에이전트의 도구 정보는 추적하지만 자식 영웅을 그리는 코드는 없고(직접 확인) `todo.md`는 완료로 적었다.
- README가 말하는 `SkillsPanel`과 `routers/skills`는 없다.
- 영웅 직업은 문서가 없고 기사 스프라이트만 있다.

### 성숙도

테스트 파일 3개, 총 236줄이다.
`server/bridge.test.ts`는 키 함수를 가져오지 않고 복사해서 시험하고,
`server/auth.logout.test.ts`는 Manus 템플릿 테스트이다.
`server/agents.test.ts`는 `detectHeroClass`의 비율 경계값(35%, 30%, 40%)만 9개 시험한다.
`server/bridge.test.ts`의 브리지 스크립트 시험은 파일 존재와 문자열 포함 여부만 본다.
파서와 감시기, WebSocket, 클라이언트는 시험하지 않는다.
직접 쓴 코드는 약 3천 줄이고 기록은 약 2일의 27개 커밋이며 `todo.md`는 중국어이다.
Claude Code가 `result`, `turn_end`, `system init` 기록을 실제로 내보내는지는 확인하지 못했다.

## 인사이트

### 가져갈 것

설정을 건드리지 않는 읽기 전용 관찰이 필요할 때 대화 기록 읽기 방식의 예로 참고할 수 있다.
다만 이 구현은 프로토타입이고 서버를 네트워크에 열어 두면 편집기와 키가 노출된다.
브리지를 쓴다면 제3자 호스트로 무엇이 가는지 먼저 확인해야 한다.

### 확인할 관찰

1. 호스트 바인딩과 인증이 추가되는지.
2. 에셋의 라이선스 표기가 정리되는지.
3. 이후 커밋이 이어지는지.
