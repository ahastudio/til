# tinyjs: txiki.js와 운영체제 웹뷰로 약 6MB 데스크톱 앱을 만드는 프레임워크

<https://tinyjs.app/>

<https://github.com/tarwin/tinyjsapp>

Show HN: [TinyJS – small apps on Win/Mac/Linux](https://news.ycombinator.com/item?id=49529062)

HN 토론: <https://news.ycombinator.com/item?id=49808029> (3점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=35038>

## 소개

tinyjs는 백엔드와 프런트엔드를 모두 JavaScript로 쓰는 데스크톱 앱 프레임워크다.
홈페이지 문구는 데스크톱 앱을 약 6MB로 만든다는 것이고,
Electron도, 번들된 Chromium도, HTTP 서버도, 포트도 없다고 내세운다.
백엔드는 txiki.js 런타임에서 돌고, 화면은 운영체제가 이미 가진 웹뷰가 그린다.
macOS는 WebKit, Windows는 WebView2, Linux는 WebKitGTK다.

만든 사람은 Tarwin Stroh-Spijer이고 MIT 라이선스다.
저장소는 2026년 7월 12일에 macOS 전용으로 시작했고,
10월 8일의 v0.50.1까지 석 달이 안 되는 동안 80개 가까운 태그를 냈다.
macOS가 주 플랫폼이며 Windows와 Linux 지원은 베타로 표시되어 있다.
GitHub 저장소 설명에는 약 5MB라고 적혀 있어 홈페이지의 6MB와 다르다.
2026년 10월 10일 기준으로 별은 722개, 포크는 21개다.

베타라는 표시가 무엇을 뜻하는지는 `TODO-verify.md`가 더 솔직하게 말한다.
이 파일은 한 기기에서 구현했지만 다른 운영체제에서 아무도 직접 동작을 보지
못한 항목의 목록이다.
macOS가 주 개발 기기라서 Windows와 Linux 항목은 대개 작성은 했고 기껏해야
컴파일만 해 봤다는 상태라고 적혀 있다.
결과가 필요 없는 명령은 무시하는 셸에 닿아도 겉보기에는 구현된 것과
똑같으므로, 해당 운영체제에서 눈으로 본 뒤에만 체크하라는 규칙도 있다.
자동 테스트는 `test/smoke.html` 하나가 호출, 오류 거부, 창 제어, push를
돌려 보는 정도이고, 기본 대화상자처럼 사람이 눌러야 하는 기능은 다루지
못한다고 README가 밝힌다.

저자는 Show HN 글에서 작은 유틸리티마다 500MB짜리 Electron 앱을 설치하는 데
지쳤다고 썼다.
결정적 계기는 Harvest가 5MB에서 500MB로 커진 업데이트였다고 한다.
Tauri는 훌륭하지만 JavaScript가 먼저인 도구를 원해서,
QuickJS와 SQLite를 이미 포함한 txiki.js 위에 만들었다는 설명이다.
같은 스레드에서 저자는 많은 부분을 Claude와 함께 만들었다고 밝히며,
아이디어와 테스트와 이해에 수백 시간을 들였지만 자신이 저자라고 보지 않는 사람이
있어도 이해한다고 덧붙였다.[^tarwin]
저장소에는 에이전트 세션용 `CLAUDE.md`가 있고,
새 프로젝트를 만들면 코딩 에이전트용 스킬 파일이 함께 복사된다.

## 동작 방식

### 프로세스 두 개와 소켓 하나

앱은 두 프로세스로 돈다.
txiki.js 백엔드가 사용자 코드(`src/main.js`)와 `runtime/bridge.js`를 실행하고,
C++로 쓴 런처가 웹뷰 창을 띄운다.
백엔드는 권한이 `0700`인 새 임시 디렉터리에 Unix 도메인 소켓을 만든 뒤
런처를 실행한다.
그래서 열리는 포트가 없고 다른 사용자에게도 보이지 않는다.
Windows에서는 Unix 소켓 대신 이름 있는 파이프를 쓴다.
창을 닫으면 런처가 끝나고, 백엔드가 이를 알아채고 정리한 뒤 종료한다.

두 프로세스는 줄 단위 텍스트 프로토콜로 대화한다.
페이지가 `tiny.api.call()`을 부르면 런처가 `CALL <id> <json-args>`를 보내고,
백엔드가 `RET <id> <status> <json>`으로 답한다.
메뉴, 트레이, 대화상자, 전역 단축키, 클립보드 같은 기능도 모두
`MENU`, `TRAY`, `DLG`, `HKREG` 같은 한 줄 명령으로 오간다.
README는 페이지 쪽 심(shim)이 10줄 남짓이라고 적는다.

```js
// src/main.js — 백엔드. api 객체의 함수는 모두 페이지에서 부를 수 있다
export const api = {
  hello: async ({ name }) => `hi ${name}`,
};

export function init(app) {
  // 창이 뜬 뒤 호출된다. app.push로 페이지에 이벤트를 보낸다
  setInterval(() => app.push('tick', Date.now()), 1000);
}
```

```js
// 페이지. tiny 전역은 런처가 모든 페이지에 자동으로 넣는다
const greeting = await tiny.api.call('hello', { name: 'world' });
tiny.api.on('tick', (t) => console.log(t));
```

### 6MB는 무엇의 크기인가

홈페이지의 질문 항목과 README의 향후 과제 절이 내역을 밝힌다.
약 6MB 중 5.6MB가 txiki.js 바이너리(`bin/tjs`)이고,
창을 맡는 런처가 1~2MB다(macOS 1.6MB, Windows 2.0MB, Linux 1.2MB).
나머지가 사용자의 HTML, CSS, JavaScript다.
txiki.js 5.6MB 안에는 QuickJS, libuv, SQLite, WebAssembly가 들어 있다.
웹뷰는 운영체제에 이미 있으므로 이 숫자에 들어가지 않는다.

즉 6MB는 압축하지 않은 앱 번들 기준이고, 웹 엔진을 뺀 숫자다.
macOS 기본 빌드는 빌드한 Mac의 CPU 하나만 지원하며,
`--universal`로 arm64와 x86_64를 합치면 약 6MB가 더 붙는다.
배포 파일은 압축되어 더 작게 보인다.
예제 앱 shelf는 홈페이지에서 4.4MB 앱으로 소개되고,
macOS `.dmg`는 4.5MB, Windows `.zip`은 4.0MB다.
반면 Winamp를 닮은 예제 amp의 `.dmg`는 8.2MB로 6MB를 넘는다.
6MB는 상한이 아니라 빈 앱의 출발점이라고 읽는 편이 정확하다(해석).

README는 더 줄이는 방향도 측정 대상으로 적어 둔다.
txiki.js를 WASM과 SQLite 없이 빌드하면 각각 약 0.4MB와 1.5MB가 줄고,
txiki.js 쪽 논의에서는 WASM, SQLite, TLS를 빼서 6.4MB가 3.31MB가 되었다는
보고가 있다.
하지만 SQLite는 tinyjs가 내세우는 백엔드 데이터베이스이고,
TLS를 빼면 HTTPS 요청과 자동 업데이트까지 같이 사라진다.
그래서 README는 이를 계획이 아닌 탐색 방향이라고 분명히 한다.
Vercel Labs의 scriptc로 백엔드를 네이티브 바이너리로 컴파일하는 안도
연구 과제로만 적혀 있다.

### 플랫폼별 구성

| 플랫폼  | 런처 소스                  | 웹뷰                 | 통신             | 상태 |
| ------- | -------------------------- | -------------------- | ---------------- | ---- |
| macOS   | `native/launcher-macos.cc` | WebKit               | Unix 소켓        | 안정 |
| Windows | `native/launcher-win.cc`   | WebView2             | 이름 있는 파이프 | 베타 |
| Linux   | `native/launcher-linux.cc` | GTK3 + WebKitGTK 4.1 | Unix 소켓        | 베타 |

macOS와 Windows 런처는 webview 라이브러리를 저장소에 포함해 쓴다.
Linux 런처는 개발 문서 설명대로 GTK3와 WebKitGTK 4.1을 직접 부른다.
README의 이식성 절에는 세 플랫폼 모두 같은 webview 라이브러리를 쓴다는 문장도
있어 서로 어긋나는데, `launcher-linux.cc`의 `include`를 보면 직접 부르는 쪽이
맞다.
macOS 앱은 macOS 15 이상이 필요하고, Linux 바이너리는 glibc 2.35 이상
(Ubuntu 22.04, Debian 12 이후)을 요구한다.

포팅되지 않은 기능은 조용히 깨지지 않도록 설계되어 있다.
기능 호출은 이유를 담아 거부되고, 조회 호출은 `null`을 돌려주며,
결과가 필요 없는 호출은 아무 일도 하지 않는다.
Quick Look, OCR, AppleScript, Apple의 온디바이스 모델을 부르는
`tiny.macos.ai`처럼 macOS에만 있는 기능은 다른 플랫폼에서 이렇게 처리된다.

### 서명된 번들의 모양

txiki.js가 컴파일한 단일 실행 파일은 Mach-O 뒤에 앱을 덧붙이는 방식이라
`codesign`이 엄격 검증에서 거부한다.
그래서 `.app` 번들은 런처를 실행 파일로 두고,
수정하지 않은 `tjs` 런타임과 앱 코드를 데이터 파일로 넣는다.
이렇게 하면 `codesign --verify --strict --deep`을 통과하고,
Developer ID가 있으면 hardened runtime으로 서명되어 공증까지 이어진다.
README가 말하는 두 개의 실제 파일은 이 런처와 런타임이다.

## 사용하기

### 설치와 새 프로젝트

```bash
# macOS, Linux 설치. ~/.tinyjs에 설치하고 PATH에 링크한다
curl -fsSL https://tinyjs.app/install | sh

tinyjs new myapp
cd myapp
tinyjs dev    # 창이 열리고 프런트엔드는 핫 리로드, 백엔드는 자동 재시작
tinyjs build  # macOS는 dist/myapp.app, Windows와 Linux는 실행 파일
```

Windows는 PowerShell에서 `irm https://tinyjs.app/install.ps1 | iex`로 설치하며,
WebView2 런타임만 있으면 된다.
CLI와 런타임 모두 txiki.js로 돌기 때문에 Node.js는 필요 없다.
Vite 템플릿을 고를 때만 개발과 빌드 단계에서 Node.js와 npm이 필요하다.
`--template react-ts`처럼 React, Vue, Svelte, Solid, Preact, Lit, Alpine
템플릿을 고를 수 있고, 패키지 매니저는 npm, pnpm, yarn, bun, Vite+ 중에서
고른다.
나는 tinyjs를 직접 설치하거나 실행해 보지 않았다.

### 프로젝트 구조와 설정

프로젝트는 `tinyjs.json`, `icon.png`, 백엔드 `src/main.js`,
프런트엔드 `src/frontend/`로 이루어진다.
프런트엔드는 `file://` 문서로 열리므로 번들러 없이 상대 경로의 스크립트와
이미지가 그대로 동작한다.
`file://`을 쓰는 이유는 보안 컨텍스트 때문이다.
HTML 문자열을 넣는 방식은 `about:blank` 출처가 되어 WebGPU 같은 API가 숨겨진다.
`tinyjs.json`에는 `macos`, `windows`, `linux` 블록을 두어 플랫폼별 값을
덮어쓸 수 있고, 적용 순서는 루트, 운영체제 블록, 환경 변수다.

백엔드에는 SQLite가 내장되어 있다.
다만 `tjs:sqlite`는 백엔드 전용이어서 페이지에서는 부를 수 없고,
README는 범용 `query(sql)` 대신 이름 붙은 함수를 노출하라고 권한다.

```js
// 백엔드: 페이지가 임의의 SQL을 실행하지 못하도록 작업 단위로 노출한다
import { Database } from 'tjs:sqlite';

await tjs.makeDir(dataDir, { recursive: true }); // tjs.* 파일 함수는 모두 비동기
const db = new Database(dataDir + '/notes.db');  // sqlite는 동기라 await하지 않는다
db.exec('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, text)');

export const api = {
  notes: () => db.prepare('SELECT * FROM notes').all(),
  addNote: ({ text }) => {
    db.prepare('INSERT INTO notes (text) VALUES (?)').run(text);
  },
};
```

### 여러 창과 딥 링크

프런트엔드 디렉터리의 HTML 파일은 저마다 창이 될 수 있다.
모든 창이 `tiny.*` 브리지 전체를 갖고, 페이지에서 부른 `tiny.win.*`는
그 페이지의 창에 적용된다.
테두리 없는 패널의 모양과 위치는 창이 그려지기 전에 적용되므로,
제목 표시줄이 잠깐 보이거나 가운데에 떴다가 옮겨지는 일이 없다.

```js
// 페이지: settings.html을 별도 창으로 연다
tiny.win.open('settings', { page: 'settings.html', title: 'Settings', size: '420x300' });

// parent: true는 main 창에 딸린 창이다. 부모 위에 머물고 부모와 함께 닫힌다
tiny.win.open('about', { page: 'about.html', size: '360x420', parent: true });
```

백엔드의 API 핸들러는 세 번째 인자 `meta.window`로 어느 창이 불렀는지 안다.
`tinyjs.json`에 `urlScheme`과 `fileExtensions`를 적으면 빌드한 앱이
`myapp://` 링크와 파일 확장자를 받는다.
두 번째 실행은 새 사본을 띄우지 않고 실행 중인 앱에 이벤트를 넘기며,
콜드 스타트 때 들어온 이벤트도 앱이 준비될 때까지 모아 두었다 전달한다.
개발 모드에는 번들이 없어서 스킴과 파일 연결은 빌드한 앱에서만 동작한다.

### 배포와 자동 업데이트

`tinyjs build`는 macOS에서 기본적으로 ad-hoc 서명한 `.app`을 만든다.
다른 사람의 Mac에서 경고 없이 열리게 하려면 연 $99의 Apple Developer Program,
Developer ID Application 인증서, `tinyjs notarize`가 필요하다.
`tinyjs publish`는 zip과 sha256, 버전, 다운로드 URL을 담은 `manifest.json`을
만들고, 이를 아무 정적 호스팅에나 올리면 된다.
앱의 업데이터는 체크섬과 코드 서명을 확인한 뒤 번들을 바꾸고 재실행하며,
실패하면 되돌린다.
Mac에서 Windows 앱을 만드는 식의 교차 빌드는 되지 않는다.
각 플랫폼에서 빌드해야 하므로 CI 매트릭스를 쓰라고 안내한다.

## 다른 도구와 비교

### 저장소와 홈페이지가 직접 하는 비교

홈페이지는 네 도구를 표로 비교한다.

| 도구       | 백엔드                     | 창            | 배포 크기  | 포트         |
| ---------- | -------------------------- | ------------- | ---------- | ------------ |
| Electron   | Node.js                    | 번들 Chromium | 150MB 이상 | 없음         |
| Tauri      | Rust, 컴파일               | 시스템 웹뷰   | 약 10MB    | 없음         |
| Neutralino | 없음, 페이지 쪽에서만 실행 | 시스템 웹뷰   | 약 3MB     | localhost WS |
| tinyjs     | JavaScript(txiki.js)       | 시스템 웹뷰   | 약 6MB     | 없음         |

이 표의 크기는 모두 tinyjs 홈페이지가 적은 값이고,
나는 각 도구의 크기를 직접 재 보지 않았다.
Electron 크기는 자료마다 다르다.
홈페이지는 150MB 이상, 에이전트용 마이그레이션 문서는 약 200MB,
Show HN 글은 500MB짜리 앱을 예로 든다.

Tauri에 대해 홈페이지는 같은 모양을 잘 해내는 도구라고 인정하면서
두 가지 차이를 든다.
백엔드가 Rust가 아니라 JavaScript여서 컴파일 단계와 두 번째 언어가 없고,
대화상자, 메뉴, 트레이, 클립보드, 키체인, 알림, 전역 단축키, 자동 업데이트가
플러그인이 아니라 기본 API라는 점이다.
그리고 생태계, 모바일 지원, 크로스 플랫폼 번들러는 Tauri가 앞서 있으니
Rust를 원하거나 모바일이 필요하면 Tauri를 쓰라고 적는다.

Neutralino는 취지가 가장 가깝고 더 작다고 평한다.
차이는 Neutralino에는 백엔드 런타임이 없어 코드가 페이지에서 돌고,
운영체제 API가 토큰으로 보호되는 localhost 웹소켓 서버를 거친다는 점이다.
내장 API가 다루지 않는 일을 하려면 보통 다른 언어로 된 별도 프로세스인
확장을 써야 한다.

Electron과 비교해서는 플랫폼마다 같은 렌더링 엔진, Node 네이티브 애드온,
10년 쌓인 Electron 도구들을 포기하는 대신 백엔드까지 순수 JavaScript로
쓸 수 있다고 정리한다.
`skill/references/electron-migration.md`에는 `ipcMain.handle`을 `api` 객체로,
`autoUpdater`를 `tinyjs publish`로 옮기는 식의 API 대응표가 있다.

### 해석: 저장소가 말하지 않는 비교 축

여기부터는 내 해석이다.
홈페이지 비교는 배포 크기와 포트에 집중하지만,
실행 시 메모리는 다른 문제다.
시스템 웹뷰도 실행되면 자체 프로세스를 띄우므로,
디스크 크기의 차이가 메모리 사용량의 차이로 그대로 이어진다고 볼 근거는 없다.
저자 자신도 다른 HN 스레드에서 amp 앱을 권하며 메모리는 조금 더 쓴다고
인정했다.[^tarwin-amp]

Wails, Electrobun, Deno Desktop처럼 같은 영역의 다른 도구는
저장소에 언급이 없다.
이 저장소의 근접 문서로는 [Electron](../electron/README.md),
[Tauri](../rust/tauri.md), [Neutralinojs](../nodejs/neutralinojs.md),
[Deno Desktop](../deno/deno-desktop.md), [Zero-Native](../zig/zero-native.md)가
있다.
Zero-Native는 시스템 웹뷰를 쓴다는 점이 같고 백엔드 언어가 Zig라는 점이 다르다.

## 트레이드오프

### 백엔드가 Node가 아니다

txiki.js는 QuickJS 위의 런타임이라 `require`도, `fs`나 `child_process` 같은
Node 내장 모듈도, 네이티브 애드온도 없다.
순수 JavaScript npm 패키지는 TypeScript 백엔드를 esbuild로 번들하면 쓸 수
있지만,
Node 내장 모듈을 import하는 패키지는 번들 단계나 실행 중에 깨진다.
마이그레이션 문서가 코드가 아니라 구조를 옮기라고 말하는 이유다.
Electron 앱을 옮길 때 가장 많이 다시 써야 하는 부분은 화면이 아니라
Node 생태계에 기대는 백엔드일 것이다(해석).

### 백엔드는 느리고, 셈은 페이지가 한다

QuickJS는 JIT 없는 인터프리터다.
성능 문서는 페이지에서 50ms 걸리는 숫자 루프가 백엔드에서는 1초를 넘길 수
있다고 적고, 페이지가 계산하고 백엔드는 시스템을 만진다는 규칙을 둔다.
저자도 HN에서 txiki.js가 작은 Node.js에 가깝지만 느리다고 답했다.[^tarwin-txiki]
게다가 두 쪽을 잇는 통로가 텍스트라 바이너리는 base64로 33% 커진다.
그래서 바이트 대신 파일 경로를 넘기고, 작은 메시지는 묶어 보내라고 권한다.
Electron에서 메인 프로세스가 무거운 일을 맡던 구조를 그대로 옮기면
느려지는 지점이 바로 여기다.

### 엔진을 고르지 못한다

운영체제 웹뷰를 쓴다는 것은 브라우저를 함께 배포하지 않는 대가로
브라우저를 고를 수 없다는 뜻이다.
홈페이지는 세 플랫폼에서 앱이 똑같이 보이지 않는다고 분명히 말하고,
Safari와 Chrome에 웹사이트를 내는 것과 같은 규율이 필요하다고 설명한다.
장점은 엔진이 운영체제와 함께 업데이트되어 브라우저 CVE마다 앱을
다시 배포하지 않아도 된다는 점이다.
반대로 운영체제 업데이트가 앱의 동작을 바꿀 수 있다는 위험도
같은 구조에서 나온다(해석).

Linux가 가장 거칠다.
WebKitGTK는 GStreamer로 디코딩하므로 플러그인이 없으면 AAC/M4A가 아예
재생되지 않는다.
Web Audio 그래프는 일반 우선순위 스레드에서 렌더링되어 소리가 깨지므로,
README는 Linux에서는 `<audio>` 요소로 바로 재생하라고 한다.
WebKitGTK에는 WebGPU도 없다.

### 작은 런타임이 넓은 권한을 가진다

백엔드는 파일, 소켓, 프로세스, FFI 전체에 접근하고,
페이지는 그 백엔드로 이어지는 RPC 통로를 쥐고 있다.
그래서 문서는 `innerHTML`에 넣는 값을 반드시 이스케이프하라고 경고한다.
v0.50.1의 보안 수정은 이 경계가 얼마나 쉽게 새는지 보여 준다.
macOS에서 WebKit이 메시지 핸들러를 최상위 프레임뿐 아니라 모든 iframe에 주는
바람에, 페이지에 들어간 광고나 임베드가 앱의 백엔드 메서드와 AppleScript,
키체인, 클립보드를 부를 수 있었다.
Linux는 0.46.0부터 이미 서브프레임 호출을 버렸고,
Windows의 WebView2는 최상위 문서의 메시지만 전달해서 영향이 없었다.
같은 기능도 엔진마다 보안 경계가 다르다는 점이 시스템 웹뷰를 쓰는
프레임워크의 숨은 비용이다(해석).

### 남의 사이트를 감싸면 권한 게이트가 전부다

tinyjs는 `"url": "https://…"` 한 줄로 원격 웹사이트를 메인 창에 띄우는
사이트 래퍼 기능도 제공한다.
JS 대화상자, 다운로드 정책, `window.open` 정책, 탐색 정책을 설정으로 정하고,
`"inject"`로 지정한 스크립트를 모든 페이지의 문서 시작 시점에 넣을 수 있다.
README는 이 스크립트가 남의 출처 안에서 페이지 전체 권한으로 돈다고 적는다.

그래서 래퍼를 배포할 수 있게 만드는 장치가 `"api"` 권한 게이트다.
`"wrapper"` 프리셋, 허용과 차단 메서드 목록, 출처별 허용 목록 중에서 고르고,
출처는 페이지가 주장하는 값이 아니라 WebKit이 보고하는 호출 프레임의 출처로
판단한다.
README가 직접 경고하는 함정이 하나 있다.
출처 키의 `*`는 점을 포함한 아무 문자와 일치하므로
`https://app.example.com*`는 `https://app.example.com.evil.com`도 허용한다.
엔진별 예외도 남아 있다.
Linux에서는 거부한 탐색도 요청 자체는 이미 나가고,
Windows에서는 확인을 거친 POST가 GET으로 다시 보내진다.

로컬 프런트엔드만 쓰는 앱이라면 백엔드와 페이지가 같은 사람의 코드다.
사이트 래퍼에서는 페이지가 제3자의 코드가 되므로,
위협 모델이 Electron의 원격 콘텐츠 로딩과 같은 쪽으로 옮겨 간다(해석).
작은 번들이라는 장점과 별개로, 이 기능을 쓰는 앱은 게이트 설정이 곧
보안 경계가 된다.

## 함정

- 6MB는 빈 앱의 출발점이다. 큰 프런트엔드나 미디어를 넣으면 amp처럼 8MB를 넘는다.
- macOS 기본 빌드는 빌드한 Mac의 CPU만 지원한다. Apple Silicon에서 빌드한 앱은 Intel Mac에서 열리지 않으므로 `--arch` 또는 `--universal`을 써야 한다.
- 빌드 시점에 만든 `.dmg`에는 공증 티켓이 빠져 있다. `tinyjs notarize --dmg`로 공증된 `.app`에서 다시 만들어야 오프라인 Gatekeeper를 통과한다.
- ad-hoc 서명 앱은 다른 사람의 Mac에서 차단된다. macOS 15부터는 오른쪽 클릭으로 여는 우회도 통하지 않는다.
- `tjs.*` 파일 함수는 비동기이고 `tjs:sqlite`는 동기다. `tjs.makeDir`를 await하지 않으면 데이터베이스 초기화가 가끔만 실패하는 경쟁 조건이 생긴다.
- 가려지거나 숨겨진 창은 WebKit이 `requestAnimationFrame`과 타이머를 늦춘다. 숨은 창으로 보이는 창을 구동하지 말고, 계속 도는 작업은 보이는 창이나 백엔드에 둔다.
- 페이지는 기본적으로 프런트엔드 디렉터리 밖의 `file://` 미디어를 읽지 못한다. `readAccess`로 넓힐 수 있지만 페이지가 읽을 수 있는 디스크 범위도 같이 넓어진다.
- 서드파티 iframe을 보여 주는 macOS 앱은 v0.50.1 이상으로 올려야 한다.
- macOS 15 이하에서 WebGPU는 WebKit 기능 플래그 뒤에 있어서, 런처가 시작할 때 비공개 API인 `WKPreferences _setEnabled:forFeature:`로 켠다. 비공개 API에 기대는 동작은 운영체제 업데이트로 조용히 바뀔 수 있다(해석).
- `tjs compile`은 import를 번들하지 않고 실행 시점에 현재 디렉터리 기준으로 찾는다. 앱은 `tjs app compile`로 묶어야 하며, 컴파일된 바이너리 안에서는 `import.meta.url`이 예외를 던지므로 `tjs.exePath` 기준으로 파일을 찾는다.
- 사이트 래퍼의 `"api"` 출처 키를 호스트 뒤 `*`로 끝내면 다른 도메인까지 허용된다.
- 웹사이트를 감싸는 기능은 User-Agent를 바꿔도 Slack처럼 내장 브라우저를 거부하는 서비스에는 들어가지 못할 수 있다고 README가 직접 경고한다.

## 기억할 원칙

### 크기 숫자는 무엇을 빼고 셌는지 함께 읽는다

tinyjs의 6MB는 정직하게 내역이 공개된 숫자다.
txiki.js 5.6MB와 런처 1~2MB, 그리고 이미 운영체제에 있는 웹뷰를 세지 않은
값이다.
Electron의 150MB와 비교할 때 줄어든 것은 브라우저 엔진을 앱마다 복제하는
비용이고, 대신 엔진 선택권과 플랫폼 간 일관성을 운영체제에 넘겼다.
배포 크기 비교표는 어느 쪽이 무엇을 책임지는지의 비교로 읽어야 한다.

GN에서 kirinonakar는
Tauri와 어떻게 차별화할지가 관건이라고 적었고,[^kirinonakar]
jhk0530은 Electron과 Tauri에게 게 섰거라라고 짧게 반응했다.[^jhk0530]
홈페이지의 답은 크기가 아니라 언어와 기본 API 범위다.
같은 시스템 웹뷰 구조라면 크기 차이는 몇 MB에 불과하므로,
백엔드를 JavaScript로 쓰고 싶은지가 선택 기준이 된다.

### 작은 프레임워크는 경계 코드가 곧 제품이다

tinyjs의 대부분은 런처 세 개와 줄 단위 프로토콜이다.
그 프로토콜이 어느 프레임에서 온 호출을 믿을지 정하는 순간 보안 코드가 되고,
저장소의 `CLAUDE.md`도 이 경로를 건드리는 일은 보안 작업이라고 적어 둔다.
HN의 jrecyclebin은 README가 철저하고 읽기 좋다고 평했고,[^jrecyclebin]
scarranca는 이 도구로 Git 이슈 칸반을 만들어 자신과 에이전트 모두 만족했다고
남겼다.[^scarranca]
에이전트와 함께 빠르게 만드는 프레임워크일수록,
속도보다 그런 경계 검증이 얼마나 쌓였는지를 보고 도입을 판단해야 한다(해석).

---

[^tarwin]: <https://news.ycombinator.com/item?id=49529089>

[^tarwin-txiki]: <https://news.ycombinator.com/item?id=49532076>

[^tarwin-amp]: <https://news.ycombinator.com/item?id=49528378>

[^kirinonakar]: <https://news.hada.io/topic?id=35038#cid67236>

[^jhk0530]: <https://news.hada.io/topic?id=35038#cid67233>

[^jrecyclebin]: <https://news.ycombinator.com/item?id=49530772>

[^scarranca]: <https://news.ycombinator.com/item?id=49531087>
