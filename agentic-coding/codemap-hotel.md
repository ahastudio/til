# Codemap

<https://github.com/JamsusMaximus/codemap>

## 소개

Codemap은 Claude Code와 Cursor 에이전트의 활동을 픽셀아트 “호텔” 위의 캐릭터로 보여 주는
로컬 Node와 React 도구이다.
호텔은 사무실이 아니라 코드베이스의 지도이다.
최근 git 변경이 많은 폴더가 방이 되고, 최근 바뀐 파일 이름이 책상이 된다.
2026년 11월 25일 GitHub API로 본 별은 135개, 생성일은 2025년 12월 19일이고
커밋은 47개, main의 마지막 커밋은 2026년 1월 15일이다.
GitHub API는 라이선스를 비어 있다고 돌려주고 `LICENSE` 파일이 없으며
`package.json`과 README가 MIT라고만 적는다.
별도 홈페이지는 없다.

저장소를 받아 코드를 읽었으며 설치하거나 실행하지 않았다.
`client/src/drawing/`의 그리기 코드는 줄 단위로 읽지 않고 키워드 검색만 했다.

## 동작 방식

### 모듈 구성

| 파일                                  | 줄       | 역할                               |
| ------------------------------------- | -------- | ---------------------------------- |
| `bin/setup.js`                        | 312      | 훅 설치, 서버 기동, 브라우저 열기  |
| `hooks/*.sh`                          | 342      | 훅 입력 JSON을 curl로 서버에 전달  |
| `server/src/index.ts`                 | 520      | HTTP 라우트, 에이전트 상태, 타이머 |
| `server/src/activity-store.ts`        | 289      | 파일 트리, 활동 카운터, chokidar   |
| `server/src/git-activity.ts`          | 95       | git log 집계, 30초 캐시            |
| `server/src/websocket.ts`             | 80       | ws 브로드캐스트, 30초 ping         |
| `client/src/hooks/useFileActivity.ts` | 166      | WebSocket 수신, ref 저장           |
| `client/src/components/HabboRoom.tsx` | 1239     | 호텔 화면, 에이전트 이동           |
| `client/src/components/FileGraph.tsx` | 497      | `/` 경로의 강제 그래프             |
| `client/src/drawing/*.ts`             | 약 3,700 | 캔버스 그리기                      |

진입점은 두 개이다.
`bin/setup.js`가 `npm run dev`로 서버(`tsx watch src/index.ts`)와
Vite 클라이언트(포트 5173, `strictPort`, `open: true`)를 함께 띄운다.
`App.tsx`는 `/`에 강제 그래프를, `/hotel`에 호텔을 연결하며
`setup.js`가 여는 주소는 `/hotel`이다.
의존성은 서버가 `express` 4, `ws` 8, `chokidar` 5, `cors`이고
클라이언트가 `react` 18과 `react-force-graph-2d`, `react-router`이다.

### 활동 수집은 훅 스크립트뿐이다

대화 기록 읽기도 확장 API도 프로세스 감시도 없다.

- Claude Code: `bin/setup.js`가 `.claude/settings.local.json`에 `PreToolUse`, `PostToolUse`,
  `Notification` 훅을 쓴다. 스크립트 `hooks/file-activity-hook.sh`와 `thinking-hook.sh`는
  `jq`로 표준 입력 JSON을 해석하고 `curl`로 `localhost:5174`에 POST한다.
- Cursor: `.cursor/hooks.json`에 `beforeReadFile`(read-start), `afterFileEdit`(write-end) 등을 쓴다.
  클라이언트가 `read-end`, `write-end`에서만 반응하므로 Cursor의 읽기는 화면 반응이 없다.

### 지도

서버가 `chokidar`로 파일 트리를 만들지만 이는 강제 그래프 화면용이다.
호텔 화면은 `git log -n 500` 기반으로 고른 상위 12개 폴더를 방으로 쓰고
층별 책상은 8, 2, 1, 1개이다.
의존성 그래프는 없다.
이벤트는 파일 이름, 가까운 상위 폴더, 루트의 순으로 방에 대응된다.
`MultiFloorHotel.tsx`(705줄)는 어디서도 가져다 쓰지 않는 죽은 코드이다.

### 서버와 상태

Express와 `ws`가 5174번 포트에 고정되고 `listen(PORT)`에 호스트가 없어
모든 인터페이스에 열린다(`server/src/index.ts` 511줄).
`cors()`는 전체 허용이고 인증이 없다.
서버는 에이전트를 최대 10개 두고 5분 동안 활동이 없으면 만료시킨다.
도구 시작 신호 뒤 60초 안에 종료 신호가 오지 않으면 입력 대기로 추측한다.
`AskUserQuestion` 도구는 시작 신호 즉시 입력 대기로 둔다.
클라이언트는 30초 동안 활동이 없으면 캐릭터를 커피숍으로 보내 잠 표시를 한다.
렌더링은 단일 2D 캔버스와 `requestAnimationFrame`이다.

### 훅이 서버로 보내는 것

훅 스크립트는 모두 표준 입력을 `jq`로 읽고 `/usr/bin/jq`, `/usr/bin/curl` 절대 경로를 쓴다.
`session_id`가 있으면 Claude, `conversation_id`가 있으면 Cursor로 구분한다.
`curl`은 `--connect-timeout 1 --max-time 2`로 백그라운드(`&`)에서 보내고
스크립트는 항상 `exit 0`으로 끝나 에이전트를 막지 않는다.
서버가 꺼져 있어도 에이전트에는 오류가 보이지 않는다.
`file-activity-hook.sh`는 파일 경로가 있으면 `/api/activity`로,
도구 이름이 있으면 `/api/thinking`으로 두 번 보낸다.
`thinking-hook.sh`는 Read, Write, Edit의 파일 이름, Bash 명령 앞 30자,
Grep, Glob의 패턴 앞 30자, Task의 서브에이전트 종류를 `toolInput`에 담는다.
`MultiEdit`은 `toolInput` 분기에 없어서 말풍선 문구가 비어 있다.
Grep과 Glob은 `<경로>:<패턴>` 형태의 `search-start`, `search-end` 활동도 따로 보낸다.
모든 훅 호출은 `/tmp/codemap-hook.log`에 시각, 에이전트 앞 8자, 파일 이름을 덧붙인다.
설치기가 등록하지 않는 `hooks/codemap-hook.sh`와 `cursor-stop-hook.sh`는
README와 문서에만 언급되고 `bin/setup.js`에는 없다.

### 서버의 상태 판정

`registerAgent`(`index.ts` 139~190줄)는 에이전트 ID가 UUID 형식이 아니면 거부하고,
10개가 차 있으면 거부하며, 직전 등록 뒤 500ms 안이면 거부한다.
거부되어도 응답은 `success: true`라서 훅은 실패를 모른다.
`/api/thinking`에서 `thinking-end`(PreToolUse)는 `pendingToolStart`를 기록하고
`thinking-start`(PostToolUse)는 이를 지우고 `waitingForInput`을 끈다.
2초 간격 타이머가 `pendingToolStart`가 60초 넘게 남은 에이전트를 입력 대기로 바꾸고
같은 타이머가 전체 에이전트 상태를 모든 클라이언트에 방송한다.
느린 빌드나 테스트도 60초를 넘으면 입력 대기로 표시된다.
상태는 30초마다 `<프로젝트>/.codemap-state.json`에 저장하고
시작할 때 5분 안에 활동한 에이전트만 복원한다.
`git-activity.ts`는 `git log --name-only --pretty=format: -n 500`을
셸로 실행해 최대 2000줄을 폴더별로 세고 8개 파일 이름만 남긴다.
`node_modules/`, `.git/`, `dist/`, `.next/`, `coverage/`가 들어간 경로는 건너뛴다.
`/api/hot-folders`는 최근 10분 안에 활동한 파일을 앞에 끼워 넣고
git에 없는 폴더는 파일 수 곱하기 10점으로 추가한다.
`ActivityStore.addActivity`는 `lastActivity`를 `*-start` 이벤트에서만 갱신한다.
Cursor는 `write-end`만 보내므로 Cursor의 편집은 최근 활동 파일 목록에 들어가지 않는다.
이 추론은 코드에서 끌어낸 것이고 Cursor를 실행해 확인하지는 않았다.

### 클라이언트 흐름

`useFileActivity.ts`는 `ws://localhost:5174/ws`에 접속하고
끊기면 2초 뒤 다시 접속한다.
메시지 종류는 `graph`, `activity`, `thinking`, `layout-update` 네 가지이며
모두 React 상태가 아니라 `ref`에 넣고 버전 카운터만 올린다.
`HabboRoom.tsx`는 `requestAnimationFrame` 루프에서 그 카운터를 비교한다.
`read-end`와 `write-end`가 오면 책상 화면을 5초 밝게 유지한 뒤 3초에 걸쳐 어둡게 하고
소리를 낸다(`screen-flash.ts`).
경로 매칭은 정확 일치, 접미사 일치, 파일 이름만 일치의 세 단계이다.
마지막 단계 때문에 다른 폴더의 같은 이름 파일이 잘못 선택될 수 있다.
에이전트는 프레임당 6픽셀씩 한 축으로만 움직이고,
30초 동안 활동이 없고 생각 중도 입력 대기도 아니면 커피숍으로 간다.
서버에서 30초 넘게 보이지 않은 에이전트는 화면에서 지운다.

### 에러 처리

훅은 실패를 전부 삼킨다.
`2>/dev/null`과 `exit 0`이 있어서 `jq`나 `curl`이 없을 때도 알림이 없다.
JSON은 셸 문자열 이어 붙이기로 만들며 `filePath`와 `toolName`은 이스케이프하지 않는다.
따옴표나 역슬래시가 든 파일 이름은 잘못된 JSON이 되어 이벤트가 사라진다.
서버 쪽 `/api/activity`는 `event.type.toUpperCase()`를 바로 호출하므로
`type` 없는 본문은 예외가 되고 Express가 500으로 응답한다.
`git log` 실패는 빈 배열을 돌려주고 호텔은 최상위 폴더로 대신 채운다.

## 분석

### 사무실이 아니라 지도라는 선택

에이전트가 어디서 일하는지를 책상이 아니라 코드베이스의 위치로 보여 준다.
이 방식은 어떤 폴더에 활동이 몰리는지를 알려 주지만
에이전트별 식별은 약하고 지도는 최근 git 활동이 많은 폴더 12개에 한정된다.

## 비평

### 설정 파일을 덮어쓴다

`npx`로 실행하면 확인 없이 `.claude/settings.local.json`의 `hooks`를 통째로 대입한다.
`setup.js` 193번째 줄이다.
사용자의 기존 `hooks`가 있다면 사라진다.
`settings.local.json`이 JSON 파싱에 실패하면 예외를 무시하고 빈 객체로 시작해
그 파일의 다른 내용도 덮어쓴다(186~190줄, 204줄).
`permissions.allow`에도 항목을 더하고 `.cursor/hooks.json` 전체를 덮어쓰며
`.git/hooks/post-commit`에 줄을 더하거나 파일을 새로 만든다.
훅은 기본 브랜치의 스크립트(`npx github:`)를 절대 경로로 실행하며 미리 허용된다.

### 열린 포트

모든 인터페이스, CORS 전체 허용, 인증 없음이므로
같은 네트워크나 웹 페이지가 `/api/graph`(절대 경로 파일 트리)와
`/api/thinking`(Bash 명령 앞 30자 포함)을 읽고 이벤트를 넣거나 `/api/clear`를 부를 수 있다.
이는 `server/src/index.ts`의 라우트와 `listen`, `cors()` 호출을 읽어 확인했다.
실제로 요청을 보내 시험하지는 않았다.

### 설명과 코드의 차이

- Cursor 완료 배지는 렌더링과 서버 처리가 있으나 `cursor-stop-hook.sh`를 설치기가 등록하지 않아
  동작할 수 없다.
- README의 테스트 248개와 달리 직접 센 값은 206개이다(실행하지 않음).
  테스트 파일 8개에서 `it(`과 `test(`로 시작하는 줄을 세었고 `.each`는 없었다.
  `skip`, `todo`, `only`도 없어 제외된 케이스로 차이를 설명할 수 없다.
- “폴더가 방, 파일이 책상”은 상위 12개 폴더에만 해당한다.
- `LICENSE` 파일이 없고 커밋된 `.cursor/hooks.json`에 제작자의 홈 경로가 들어 있다.
- 이름은 Habbo와 아이소메트릭을 말하지만 `client/src/drawing/`과 `HabboRoom.tsx`에서
  isometric, skew, projection 같은 키워드를 찾지 못했다.
  `App.tsx`의 주석만 아이소메트릭이라고 적는다.
  화면이 탑다운 타일인지는 렌더링해 보지 않아 확정하지 못했다.
- 서버 테스트 84개는 서버 소스를 가져오지 않고 복제한 로직을 시험한다.

### 확인한 보안상 표면

`setup.js`는 `lsof -i :<포트>`와 `open`/`xdg-open`을 `exec`로 부르지만
인자는 상수라서 사용자 입력이 들어가지 않는다.
`/api/activity`는 프로젝트 루트 아래 임의 경로로 노드를 만들 수 있고
`path.relative`가 `..`로 시작하는 경로는 거른다.
`filePath`가 상대 경로이면 `path.relative`가 서버 작업 디렉터리를 기준으로 풀어서
서버를 어디서 실행했는지에 따라 노드가 달라진다.
WebSocket 서버도 `Origin`을 검사하지 않는다.
`/tmp/codemap-hook.log`는 파일 이름을 담은 채 임시 폴더에 남는다.
저장소에 커밋된 `.codemap-state.json`에는 에이전트 ID와 시각이 들어 있다.
이 파일은 `.gitignore`에 있는 `settings.local.json`, `hooks.json`과 달리 무시 목록에 없다.

### 성숙도

`vitest` 8개 파일에 206개 케이스가 있고 훅, `setup.js`, 캔버스 그리기에 대한 테스트는 없다.
서버 테스트 84개는 `ActivityStore`, git 로그 집계, `ws` 방송과 죽은 연결 정리,
`toRelativePath`, ID 검증을 이름으로 내세운다.
그러나 서버 테스트 5개 파일 어디에도 `./`로 시작하는 가져오기가 없다.
각 파일이 같은 알고리즘을 테스트 안에 다시 써 놓고 그 복제본을 시험한다.
`integration.test.ts`가 `express`를 가져오지만 서버 소스는 가져오지 않는다.
그래서 서버 코드를 고쳐도 이 테스트는 깨지지 않으며 서버 로직의 회귀를 잡지 못한다.
클라이언트 테스트 122개는 `screen-flash.ts`와 `agent-movement.ts`를 실제로 가져와
경로 매칭, 이동 계산, 화면 번쩍임 시간 같은 순수 함수를 시험한다.
CI가 없고 추적 파일은 약 1만 1,800줄이다.
1인 개발이며 약 4주의 활동 뒤 멈춘 취미 프로젝트로 보인다.

## 인사이트

### 가져갈 것

활동을 에이전트가 아닌 코드 위치로 보려는 아이디어는 다른 도구에서 찾기 어렵다.
설치 전에 `.claude`, `.cursor`, `.git/hooks`가 바뀐다는 점,
기존 `hooks`가 대체된다는 점을 알아야 한다.
임시로 쓸 때는 방화벽이나 루프백 바인딩을 따로 해야 한다.

### 확인할 관찰

1. 설정 병합이 덮어쓰기에서 실제 병합으로 바뀌는지.
2. 포트 바인딩이 루프백으로 제한되는지.
3. 프로젝트가 1월 이후 이어지는지.
