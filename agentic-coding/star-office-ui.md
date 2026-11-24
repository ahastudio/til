# Star Office UI

<https://github.com/ringhyacinth/Star-Office-UI>

## 소개

Star Office UI는 OpenClaw 에이전트의 상태를 픽셀 사무실에 보여 주는 Flask와 Phaser 3 웹 앱이다.
2026년 11월 25일 GitHub API로 본 별은 7,596개이고 생성일은 2026년 2월 26일,
커밋은 172개이며 홈페이지 항목은 비어 있다.
라이선스는 코드와 그림이 갈라진다.
`LICENSE`에서 코드는 MIT이고 모든 그림은 비상업 용도로만 쓸 수 있어,
GitHub이 라이선스를 판별하지 못하고 NOASSERTION으로 표시한다.

저장소를 받아 코드를 읽었으며 설치하거나 실행하지 않았다.
백엔드 `backend/`, 푸시 스크립트, 프런트엔드 `frontend/index.html`의 핵심 흐름을
이 문서가 직접 읽고 확인했다.
별 수, 생성일, 커밋 수는 코드가 아니라 API 값이어서 코드로는 확인하지 못했다.

## 동작 방식

### 모듈 구성

| 파일                                                 | 줄 수   | 역할                                                   |
| ---------------------------------------------------- | ------- | ------------------------------------------------------ |
| `backend/app.py`                                     | 2,103   | Flask 라우트 전부, 상태 판정, 에셋 업로드, 이미지 생성 |
| `backend/store_utils.py`                             | 130     | JSON 파일 읽기와 쓰기                                  |
| `backend/memo_utils.py`                              | 116     | 어제 메모 추출과 개인정보 가림                         |
| `backend/security_utils.py`                          | 37      | 운영 모드 판별, 비밀값과 비밀번호 강도 검사            |
| `frontend/index.html`                                | 4,889   | Phaser 장면, 폴링, 손님 렌더링, 에셋 서랍              |
| `set_state.py`                                       | 70      | `state.json` 갱신 CLI                                  |
| `office-agent-push.py`                               | 305     | 손님 에이전트의 가입과 주기 푸시                       |
| `scripts/smoke_test.py`, `scripts/security_check.py` | 87, 136 | 실행 중 서버 점검, 설정 사전 점검                      |
| `desktop-pet/src-tauri/src/lib.rs`                   | 641     | Tauri 데스크톱 껍데기                                  |
| `electron-shell/main.js`                             | 543     | Electron 껍데기                                        |

백엔드 의존성은 `backend/requirements.txt`의 flask 3.0.2와 pillow 10.4.0이다.
`pyproject.toml`에는 flask만 적혀 있다.
`office-agent-push.py`는 함수 안에서 `requests`를 불러오는데
이 패키지는 두 의존성 목록 어디에도 없다.
저장은 모두 JSON 파일이다.
`state.json`, `agents-state.json`, `join-keys.json`, `runtime-config.json` 등이 있고
`store_utils.py`가 읽다 실패하면 기본값을 돌려준다.

### 에이전트를 관찰하지 않는다

이 도구는 에이전트를 들여다보지 않는다.
훅도 대화 기록 읽기도 없고, 상태는 에이전트가 스스로 알려 주어야 한다.
방법은 두 가지이다.
LLM이 `SOUL.md`의 규칙에 따라 `set_state.py`를 실행해 `state.json`을 쓰거나,
`POST /set_state`(`app.py`)를 부르는 것이다.
손님 에이전트는 `office-agent-push.py`가 15초마다 같은 `state.json`을 읽거나
로컬 `/status`를 조회해서 `/agent-push`로 보낸다.
메인 에이전트의 작업 상태 세 가지는 300초 동안 갱신이 없으면 대기로 돌아간다.
이 흐름을 코드로 직접 따라가 확인했고, 세부는 아래 하위 절에 적었다.

### 상태 판정과 TTL

`app.py`의 `VALID_AGENT_STATES`는 여섯 가지이고 `WORKING_STATES`는
writing, researching, executing 셋이다.
`load_state()`는 `state.json`의 `ttl_seconds`(없으면 300)보다 오래된
작업 상태를 idle로 바꾸고, 바뀐 값을 파일에 다시 쓴다.
따라서 `GET /status`는 읽기 요청이지만 파일을 갱신할 수 있다.
syncing과 error는 `WORKING_STATES`에 없어서 시간이 지나도 풀리지 않는다.
`POST /set_state`는 여섯 상태가 아닌 값을 조용히 무시하고
detail과 `updated_at`만 갱신한다.
반면 `set_state.py`는 receiving과 replying까지 여덟 상태를 받는다.
이 둘은 백엔드가 알지 못하는 값이어서 `state.json`에는 그대로 기록되고,
프런트엔드 `applyVisualState`는 idle, error, syncing이 아니면 모두
책상 애니메이션 분기로 보낸다.
이 연결은 코드를 읽고 추론한 것이며 실행해 보지 않았다.
`normalize_agent_state()`는 working, busy, run, sync 같은 동의어를 여섯 상태로
바꾸고 모르는 값은 idle로 만든다.

### 손님 에이전트 흐름

`POST /join-agent`는 `join-keys.json`에 있는 키가 맞으면 곧바로 approved로 쓴다.
키에 `expiresAt`이 있으면 만료를 검사하고,
`maxConcurrent`(기본 3)를 `join_lock` 안에서 센다.
동시 접속의 기준은 `lastPushAt`이 300초 안인지이다.
`POST /agent-push`는 키와 `agentId`가 일치하는지 확인하고
offline 상태의 손님은 approved로 되돌린다.
`GET /agents`는 300초 넘게 푸시가 없는 손님을 offline으로 바꾸고
그 결과를 `agents-state.json`과 `join-keys.json`에 매번 쓴다.
푸시 스크립트는 응답이 403이나 404이면 저장된 `agentId`를 지우고 종료한다.
다른 실패는 출력만 하고 다음 주기에 다시 시도한다.
`fetch_local_status()`는 `state.json` 후보 경로, 로컬 `/status`, 대기 순으로
시도하고 600초(`OFFICE_STALE_STATE_TTL`) 넘게 갱신이 없으면 idle로 본다.
또 `map_detail_to_state()`가 detail의 키워드로 상태를 덮어쓴다.
error, bug 같은 단어가 detail에 있으면 상태 값과 관계없이 error로 보내고
done이나 idle 같은 단어가 있으면 idle로 보낸다.

### 전송과 화면

브라우저가 `/status`를 1초, `/agents`를 3.5초마다 HTTP로 조회한다.
`setInterval`이 아니라 Phaser의 `update` 루프가 경과 시간을 비교해 부른다.
WebSocket이나 SSE는 없다.
화면은 Phaser(`AUTO`, 1280×720, 픽셀 렌더링)이고
로직은 `frontend/index.html` 한 파일(4,889줄)에 있다.
상태는 여섯 가지이고 세 구역(휴게실, 책상, 버그 구역)에 대응한다.
README는 캐릭터가 구역으로 걸어간다고 설명하지만
코드에서 메인 캐릭터는 걷지 않고 조회할 때마다 스프라이트가 바뀐다.
`applyVisualState`는 idle이면 소파 좌표 (798, 272)에 놓고
나머지는 캐릭터를 숨기거나 책상 스프라이트를 보인다.
걸어가는 코드(속도 1.4)는 있으나 `pendingDesiredState`에 값을 넣는 곳이 없어
도달하지 않는다고 직접 확인했다.
돌아다니는 코드는 주석 처리되어 있다.
손님은 좌표로 바로 옮겨지고 부드러운 이동은 `?demo=1`일 때만 쓴다.
서버 판정과 달리 프런트엔드는 researching 구역 좌표를 따로 갖는다.

### 서버와 접근 제어

Flask 개발 서버가 `0.0.0.0:19000`에 열린다(`app.py`).
유일한 잠금은 “에셋 서랍”의 비밀번호이고 기본값이 `1234`이다.
`/assets/auth`는 환경변수 `ASSET_DRAWER_PASS`와 단순 비교한 뒤
세션 쿠키(12시간)에 플래그를 세우고, 이 함수에는 시도 횟수 제한이 없다.
`/assets/upload`, `/config/gemini`, 배경 생성 같은 쓰기 경로는 이 플래그를 요구한다.
`/assets/list`와 `/health`는 인증이 없다.
`/set_state`, `/agent-approve`, `/agent-reject`, `/leave-agent`, `/yesterday-memo`,
`/agents`는 인증이 없다.
`/agents`는 손님마다의 `joinKey`를 돌려주고 `/join-agent`는 자동으로 승인한다.
운영 모드는 약한 세션 비밀값을 거절하지만 개발 모드는 경고만 한다.
`security_utils.py`는 24자 미만이거나 change-me, dev, test 같은 단어가 든 값을
약하다고 보는데, 기본 비밀값 자체가 change-me를 포함한다.
개발 모드에서 기본 비밀값을 쓰면 Flask 세션 서명키가 공개된 값이라는 뜻이므로
세션 쿠키를 위조할 수 있다고 추론하지만 시험하지는 않았다.
`app.run`은 `debug=False`이고 포트는 `STAR_BACKEND_PORT`로 바꾼다.

### 기계에 남기는 것

쓰기는 저장소 안(상태, 에이전트, 참가 키, 실행 설정 파일, 에셋)에 한정된다.
`~/.openclaw/workspace/IDENTITY.md`와 저장소 상위의 `../memory/*.md`를 읽고,
후자는 좁은 정규식으로 일부를 가린 뒤 인증 없이 제공한다.
`memo_utils.py`의 가림 대상은 `ou_` 식별자, `user_id`, `/root/` 경로,
IPv4 주소, 이메일, 중국 휴대전화 번호뿐이다.
`/Users/` 같은 다른 경로는 가려지지 않는다.
메모는 처음 세 항목만, 항목당 40자까지 보여 준다.
에이전트나 편집기의 설정과 훅은 건드리지 않는다.

## 분석

### 자기 보고형과 관찰형

관찰형 도구는 에이전트가 무엇을 하는지 도구 호출로 읽는다.
이 도구는 에이전트가 자기 상태를 말해 주는 방식이어서 설치가 가볍고
어떤 에이전트든 `set_state`만 부르면 붙일 수 있다.
반대로 LLM이 규칙을 잊거나 빼먹으면 화면은 현재 상태와 어긋나고
그것을 감지할 방법이 없다.
300초 TTL은 이 어긋남을 줄이는 최소한의 안전장치이다.

## 비평

### 기본값의 위험

기본 비밀번호 `1234`, 모든 인터페이스에의 바인딩, 인증 없는 상태 변경 경로가
함께 있다.
`app.py`의 `os.system` 문자열 조립이 업로드 파일 이름에서 온 경로 조각을 쓰는 곳이 있다.
직접 읽어 확인했다.
`assets_upload`가 임시 파일의 확장자를 업로드 파일 이름에서 가져오고,
`_animated_to_spritesheet`의 ffmpeg 프레임 추출 명령(`cmd1`)이 그 경로를
작은따옴표로 감싸 셸에 넘긴다.
이 명령은 Pillow가 프레임을 읽지 못했을 때만 실행되고
ImageMagick이나 ffmpeg이 설치되어 있어야 한다.
나머지 두 명령은 `mkstemp`와 임시 폴더 경로만 쓴다.
이 경로는 기본 비밀번호가 걸린 로그인 뒤에 있다.
실제로 악용되는지는 시험하지 않았다.

### 설명과 코드의 차이

- 캐릭터가 구역으로 걸어간다는 설명은 코드의 스프라이트 교체와 다르다.
- `desktop-pet/`을 Electron이라 적지만 실제는 Tauri이다.
- `SKILL.md`의 참가 키 예시 `ocj_starteam01..08`은 저장소에 없고 예시 하나만 있다.
- `frontend/join-office-skill.md`의 동시 접속 100은 코드의 기본값 3과 다르다.
- `load_state()`의 설명 주석에 적힌 TTL 25초는 코드의 300초와 다르다.
- README는 상태를 여섯 가지라 하지만 `set_state.py`는 여덟 가지를 받는다.
- 푸시 스크립트의 머리말은 30초마다 보낸다고 하나 상수는 15초이다.
- `frontend/game.js`와 `layout.js`는 화면이 불러오지 않는 낡은 파일이다.
- 기본 `OFFICE_URL`과 스킬 내려받기 주소가 제작자의 호스트로 지정되어 있다.

### 성숙도

테스트도 CI도 없고 `scripts/smoke_test.py`와 `scripts/security_check.py`만 있다.
`.github`와 단위 테스트 폴더는 찾지 못했다.
`smoke_test.py`는 실행 중인 서버에 GET 다섯 개(`/`, `/health`, `/status`,
`/agents`, `/yesterday-memo`)와 `POST /set_state` 하나를 보내
상태 코드만 확인한다.
`security_check.py`는 운영 모드의 비밀값 강도, `git ls-files`에 런타임 파일이
올라와 있는지, API 키 모양의 문자열이 있는지를 검사한다.
기능 동작을 시험하는 코드는 없다.
실제 코드는 7~8천 줄이고 `index.html`이 4,889줄이며
제작자 환경의 경로가 고정된 곳이 있다.
그림의 라이선스가 비상업이라는 점도 사용 범위를 정한다.

## 인사이트

### 가져갈 것

에이전트 쪽 설정을 건드리지 않고 상태 판만 만들고 싶다면
`state.json` 한 파일과 짧은 HTTP 조회만으로 충분하다는 예가 된다.
다만 공개 주소에 올리기 전에 기본 비밀번호와 공개 경로를 반드시 점검해야 한다.
그림은 비상업 조건이므로 제품에 넣지 않는다.

### 확인할 관찰

1. 코드 라이선스와 그림 라이선스를 분리한 배포 방식이 이어지는지.
2. 자기 보고형 상태가 실제 작업과 어긋나는 빈도.
3. 보안 점검 스크립트가 기본 설정의 약점을 막는 쪽으로 쓰이는지.

위 셋 모두 이 문서가 확인하지 못했다.
