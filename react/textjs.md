# Text.js는 React 앱을 브라우저 개발자 도구 콘솔에 프레임 단위로 그려 주는 프레임워크이고, 홍보 사이트는 풍자라고 작성자가 밝혔다

<https://textjs.org/>

<https://github.com/anomalyco/textjs>

HN 토론: <https://news.ycombinator.com/item?id=50361657> (118점, 51개 댓글)

GN 토론: <https://news.hada.io/topic?id=37181>

## 소개

Text.js는 브라우저 콘솔에서 렌더링되는 앱을 위한 React 프레임워크이다.
저장소는 anomalyco가 2026년 11월 2일에 만들었고 MIT 라이선스이며 TypeScript로 쓰였다.
2026년 11월 14일에 읽은 값으로 별 256개, 포크 6개, 열린 이슈 4개이고 마지막 변경이 11월 14일이다.
README의 배지는 OpenCode로 만들었다고 밝힌다.
이 문서는 README와 `ARCHITECTURE.md`와 GitHub 저장소 정보, 그리고 HN 스레드를 읽었다.
프레임워크를 설치하거나 실행해 보지는 않았다.

## 사용법과 구성

시작은 `bunx create-text-app@latest`로 프로젝트를 만들고 `bun install`과 `bun dev`를 실행한 뒤 `localhost:3000`을 열고 브라우저 콘솔을 여는 것이다.
요구 사항은 Bun 1.2 이상 또는 Node.js 22 이상, 그리고 데스크톱의 Chrome, Edge, Firefox, Safari이다.

예시 코드는 React 컴포넌트에서 `Box`와 `Text`를 쓰고 `useInput`으로 위아래 키를 받아 카운터를 올리고 내리는 형태이다. 스타일은 `className="flex-col border rounded p-1"`처럼 유틸리티 클래스로 준다.
README는 각 프레임을 Yoga로 배치하고 연속 같은 값을 묶는 방식(run-length encoding)으로 `%c` 스타일 구간으로 만들어 `console.log` 한 번으로 쓰며, 바뀐 셀이 없는 프레임은 아무것도 기록하지 않는다고 설명한다.

저장소는 패키지 묶음이다.

- `@textjs/app`: App Router와 `text` CLI와 라우트 핸들러
- `@textjs/react`: 리컨실러(reconciler)와 컴포넌트와 훅
- `@textjs/core`: 셀 버퍼와 레이아웃과 `%c` 콘솔 드라이버
- `@textjs/font`: FIGlet 글꼴 분석기와 렌더러
- `@textjs/opencode`: textjs.org/opencode와 OpenCode 서버를 잇는 로컬 브리지
- `create-text-app`, `eslint-plugin-textjs`
- VS Code 확장(실시간 미리보기와 App Router 스캐폴딩)과 Chrome DevTools 확장(컴포넌트 트리와 프레임 검사기와 타임라인)

`ARCHITECTURE.md`는 구현의 약속을 길게 적는다.
프레임이 더러워질 때마다 `console.log`를 정확히 한 번만 부르고 줄마다 부르지 않는다. 줄 단위로 부르면 DevTools의 행 경계선과 반복 배지와 프로세스 간 호출 부담이 생기기 때문이라고 한다.
이어서 DevTools가 새 메시지를 50밀리초 간격으로 그리는 특성을 이유로, 매 프레임 `console.clear()`를 부르면 깜박이므로 이전 프레임 아래에 덧붙여 맨 아래 고정 스크롤로 교체한다고 적는다.
프레임 간격은 66밀리초 이상(약 15fps)으로 두고, 변경된 행만 다시 칠하는 손상 구간(damage band)과 행 해시 캐시로 변경이 없으면 할당도 로그도 없게 한다.
리터럴 `%`는 `%%`로 이스케이프하고, Chromium이 URL 안에 테마 색을 강제로 넣는 동작을 막으려고 `://` 뒤에 보이지 않는 단어 결합자를 넣는 식의 방어를 둔다.
이 명세는 이 문서가 직접 구현과 대조하지는 못했다.

## 분석

### 중심 주장은 콘솔도 UI의 렌더링 대상이라는 것이다

흔한 반응은 쓸모를 묻는 것이다.
이 프로젝트의 가장 큰 기술적 내용은 콘솔의 제약(한 번에 한 메시지, 스크롤, 던지는 간격)을 맞춰 안정적인 프레임 출력을 만드는 방법이다.
`ARCHITECTURE.md`의 상당 부분은 DevTools의 렌더링 지연과 메시지 합치기 규칙에 대한 관찰이며, 이는 콘솔을 그리기 표면으로 쓰려는 시도의 실제 비용을 보여 준다.

### 풍자와 실제가 섞여 있다

HN 스레드에서 작성자라고 밝힌 사용자는 홍보 사이트가 완전한 풍자이고 프레임워크는 실제로 동작하며 콘솔에 앱을 그리려는 사람을 위한 자료가 많다고 했다.[^adamdotdev]
다른 댓글도 이 점을 짚었다. 만든 팀이 OpenCode를 만든 팀과 같고 홍보 사이트의 풍자가 얼마나 되는지는 모르겠다는 것이다.[^ctippett]
`ARCHITECTURE.md`가 `▼`를 Vercel의 `▲`를 뒤집은 상표로 설명하고 “Inverted Architecture™”와 “Turbolog”라는 이름을 붙인 것도 이 풍자의 연장으로 읽힌다.
이 문서는 풍자와 실제의 경계를 문서별로 가르지 못했다.

## 비평

### 쓸모를 묻는 질문이 반복되었다

한 댓글은 사용처를 생각할 수 없다며 청중이 누구인지 물었고,[^hmokiguess]
다른 댓글도 “사용처?”라고 했다.[^tamimio]
답글은 재미로 한 것이고 재미는 무언가를 하는 가장 좋은 이유 중 하나라고 했다.[^hnlmorg]
또 다른 답글은 핵심 가치가 페이지 속에 묻혀 있다고 했다. 터미널에서도 렌더링되어 TUI 앱용 React 같은 것이고, OpenCode를 이것으로 만들었는데 왜 `console.log`를 주된 판매 포인트로 삼았느냐는 것이다.[^brap]
다른 댓글은 만든 팀이 OpenCode도 만들었고 이 프레임워크를 쓰는 방법을 다룬 페이지가 있어 에이전트용 로컬 TUI가 주된 용도로 보인다고 했다.[^contrahax]
이 추정은 두 댓글의 해석이고, README는 OpenCode 연동 패키지를 목록에 올릴 뿐 이 프레임워크가 OpenCode의 화면을 만든다고 직접 말하지 않는다.

### 비교 대상과 터미널 지원은 확인되지 않았다

한 댓글은 ink-web과 webatui와 비교해 어떠냐고 물었고 답이 없었다.[^onavo]
다른 댓글은 터미널 앱도 만들 수 있느냐고 물었고, 답글은 표준 출력도 `console.log`와 비슷하니 될 것이라고 추측했다.[^andsoitis][^cmlewis]
README는 브라우저 콘솔 대상만 설명하고 터미널 대상 지원을 말하지 않는다.
이 문서는 터미널 지원 여부를 확인하지 못했다.

### 성숙도의 근거는 얕다

저장소가 만들어진 지 12일이고 별 256개이다.
`ARCHITECTURE.md`는 “Text.js 1.0.0”을 말하지만, 이 문서는 릴리스 이력이나 버전 정책을 확인하지 못했다.
HN 스레드의 반응은 호기심과 농담이 다수였고 실제로 써 본 보고는 없었다.

## 인사이트

### 가져갈 것은 콘솔 렌더링의 제약 목록이다

이 프로젝트를 쓰지 않더라도 `ARCHITECTURE.md`는 DevTools 콘솔을 출력 표면으로 쓸 때의 제약을 한곳에 모은다.
한 프레임 한 호출, 지우지 말고 덧붙이기, 66밀리초 이상 간격, 서식 문자열의 `%` 이스케이프, 서식 지정 구간 수의 억제가 그것이다.
개발자에게 메시지를 남기는 콘솔 도구를 만든다면 이 목록이 참고가 된다. 한 댓글도 사이트를 여는 개발자를 위한 메시지가 쓸모라고 했다.[^bgitarts]
이는 이 문서의 읽기이고 구현은 확인하지 못했다.

### 평가의 기준

“쓸모가 있느냐”보다 “제약이 있는 표면에 선언형 UI를 얹을 때 무엇이 드는가”를 보는 편이 이 프로젝트에 맞는다.
스레드의 한 댓글은 그 자리에 있는 상상력을 요구했다.[^grimgrin]

### 확인할 관찰

이 프로젝트의 방향을 가를 관찰은 세 가지이다.
터미널 대상 지원이나 OpenCode 화면 구현에 쓰이는지,
풍자가 아닌 실제 사용 사례(콘솔 안의 도구나 게임)가 나오는지,
프레임 속도 제약과 브라우저별 차이가 문서화된 대로 동작하는지이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^adamdotdev]: <https://news.ycombinator.com/item?id=50407914>

[^ctippett]: <https://news.ycombinator.com/item?id=50407295>

[^hmokiguess]: <https://news.ycombinator.com/item?id=50405954>

[^tamimio]: <https://news.ycombinator.com/item?id=50406255>

[^hnlmorg]: <https://news.ycombinator.com/item?id=50406213>

[^brap]: <https://news.ycombinator.com/item?id=50406480>

[^contrahax]: <https://news.ycombinator.com/item?id=50406555>

[^onavo]: <https://news.ycombinator.com/item?id=50407416>

[^andsoitis]: <https://news.ycombinator.com/item?id=50405918>

[^cmlewis]: <https://news.ycombinator.com/item?id=50407787>

[^bgitarts]: <https://news.ycombinator.com/item?id=50408988>

[^grimgrin]: <https://news.ycombinator.com/item?id=50407231>
