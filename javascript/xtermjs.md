# xterm.js

웹 브라우저에서 완전한 기능의 터미널 에뮬레이터를 구현하는 라이브러리.
VS Code, Hyper, JupyterLab 등에서 사용된다.

- <https://xtermjs.org/>
- <https://github.com/xtermjs/xterm.js>

## 설치

```bash
npm install @xterm/xterm
```

## 기본 사용법

```html
<!-- CSS 포함 필수 -->
<link rel="stylesheet" href="node_modules/@xterm/xterm/css/xterm.css" />
<div id="terminal"></div>
```

```javascript
import { Terminal } from '@xterm/xterm';

const terminal = new Terminal();
terminal.open(document.getElementById('terminal'));
terminal.write('Hello, xterm.js!\r\n');

// 사용자 입력 처리
terminal.onData((data) => {
  terminal.write(data);
});
```

## 애드온

| 애드온             | 설명                            |
| ------------------ | ------------------------------- |
| `@xterm/addon-fit` | 컨테이너 크기에 맞게 터미널 조정 |
| `@xterm/addon-web-links` | URL 클릭 가능하게 처리   |
| `@xterm/addon-search` | 터미널 내 텍스트 검색         |
| `@xterm/addon-unicode11` | 유니코드 11 폭 지원        |

```bash
npm install @xterm/addon-fit
```

```javascript
import { FitAddon } from '@xterm/addon-fit';

const fitAddon = new FitAddon();
terminal.loadAddon(fitAddon);
terminal.open(document.getElementById('terminal'));
fitAddon.fit();

// 창 크기 변경 시 재조정
window.addEventListener('resize', () => fitAddon.fit());
```

## tmux 연동

xterm.js는 프론트엔드 터미널 에뮬레이터이므로,
실제 셸 또는 tmux와 연동하려면 백엔드가 필요하다.

```
xterm.js (브라우저) ↔ WebSocket ↔ 백엔드 ↔ node-pty ↔ tmux
```

### 백엔드 설정

`node-pty`로 tmux 세션을 열고 WebSocket으로 데이터를 중계한다.

```bash
npm install node-pty ws
```

```javascript
// server.js
const pty = require('node-pty');
const { WebSocketServer } = require('ws');

const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', (ws) => {
  // tmux 세션 연결 (없으면 새로 생성)
  const shell = pty.spawn('tmux', [
    'new-session', '-A', '-s', 'main',
  ], {
    name: 'xterm-256color',
    cols: 80,
    rows: 24,
    env: process.env,
  });

  // PTY → 브라우저
  shell.onData((data) => ws.send(data));

  // 브라우저 → PTY
  ws.on('message', (data) => {
    try {
      // 크기 변경 메시지 처리
      const msg = JSON.parse(data);
      if (msg.type === 'resize') {
        shell.resize(msg.cols, msg.rows);
      }
    } catch {
      // 일반 입력 처리
      shell.write(data);
    }
  });

  ws.on('close', () => shell.kill());
});
```

### 프론트엔드 설정

```javascript
import { Terminal } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';

const terminal = new Terminal();
const fitAddon = new FitAddon();
terminal.loadAddon(fitAddon);
terminal.open(document.getElementById('terminal'));
fitAddon.fit();

const ws = new WebSocket('ws://localhost:8080');

// 터미널 입력 → 서버
terminal.onData((data) => ws.send(data));

// 서버 출력 → 터미널
ws.onmessage = (e) => terminal.write(e.data);

// 크기 변경 → 서버에 알림
terminal.onResize(({ cols, rows }) => {
  ws.send(JSON.stringify({ type: 'resize', cols, rows }));
});

// 창 크기 변경 시 재조정
window.addEventListener('resize', () => fitAddon.fit());
```

### 옵션

tmux 세션 이름과 실행 방식을 조절할 수 있다.

```javascript
// 기존 세션 연결만 (없으면 실패)
pty.spawn('tmux', ['attach-session', '-t', 'main'], { ... });

// 특정 명령 실행 후 tmux 안에서 유지
pty.spawn('tmux', [
  'new-session', '-A', '-s', 'main', '-x', '220', '-y', '50',
], { ... });
```
