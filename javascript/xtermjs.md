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

```typescript
import { Terminal, ITerminalOptions } from '@xterm/xterm';

const options: ITerminalOptions = {
  cursorBlink: true,
  fontSize: 14,
};

const terminal = new Terminal(options);
const el = document.getElementById('terminal') as HTMLElement;
terminal.open(el);
terminal.write('Hello, xterm.js!\r\n');

// 사용자 입력 처리
terminal.onData((data: string) => {
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

```typescript
import { FitAddon } from '@xterm/addon-fit';

const fitAddon = new FitAddon();
terminal.loadAddon(fitAddon);
terminal.open(document.getElementById('terminal') as HTMLElement);
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
npm install -D typescript @types/node @types/ws
```

```typescript
// server.ts
import * as pty from 'node-pty';
import { WebSocketServer, WebSocket } from 'ws';

interface ResizeMessage {
  type: 'resize';
  cols: number;
  rows: number;
}

function isResizeMessage(msg: unknown): msg is ResizeMessage {
  return (
    typeof msg === 'object' &&
    msg !== null &&
    (msg as ResizeMessage).type === 'resize'
  );
}

const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', (ws: WebSocket) => {
  // tmux 세션 연결 (없으면 새로 생성)
  const shell = pty.spawn('tmux', [
    'new-session', '-A', '-s', 'main',
  ], {
    name: 'xterm-256color',
    cols: 80,
    rows: 24,
    env: process.env as Record<string, string>,
  });

  // PTY → 브라우저
  shell.onData((data: string) => ws.send(data));

  // 브라우저 → PTY
  ws.on('message', (raw: Buffer | string) => {
    try {
      const msg: unknown = JSON.parse(raw.toString());
      if (isResizeMessage(msg)) {
        shell.resize(msg.cols, msg.rows);
        return;
      }
    } catch {
      // JSON이 아닌 경우 일반 입력으로 처리
    }
    shell.write(raw.toString());
  });

  ws.on('close', () => shell.kill());
});
```

### 프론트엔드 설정

```typescript
import { Terminal, ITerminalOptions } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';

const options: ITerminalOptions = {
  cursorBlink: true,
  fontSize: 14,
};

const terminal = new Terminal(options);
const fitAddon = new FitAddon();
terminal.loadAddon(fitAddon);
terminal.open(document.getElementById('terminal') as HTMLElement);
fitAddon.fit();

const ws = new WebSocket('ws://localhost:8080');

// 터미널 입력 → 서버
terminal.onData((data: string) => ws.send(data));

// 서버 출력 → 터미널
ws.onmessage = (e: MessageEvent<string>) => terminal.write(e.data);

// 크기 변경 → 서버에 알림
terminal.onResize(({ cols, rows }: { cols: number; rows: number }) => {
  ws.send(JSON.stringify({ type: 'resize', cols, rows }));
});

// 창 크기 변경 시 재조정
window.addEventListener('resize', () => fitAddon.fit());
```

### 옵션

tmux 세션 이름과 실행 방식을 조절할 수 있다.

```typescript
const ptyOptions: pty.IPtyForkOptions = {
  name: 'xterm-256color',
  cols: 80,
  rows: 24,
  env: process.env as Record<string, string>,
};

// 기존 세션 연결만 (없으면 실패)
pty.spawn('tmux', ['attach-session', '-t', 'main'], ptyOptions);

// 터미널 크기를 지정하여 세션 생성
pty.spawn('tmux', [
  'new-session', '-A', '-s', 'main', '-x', '220', '-y', '50',
], { ...ptyOptions, cols: 220, rows: 50 });
```
