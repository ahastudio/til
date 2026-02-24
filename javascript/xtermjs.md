# xterm.js

웹 브라우저에서 완전한 기능의 터미널 에뮬레이터를 구현하는 라이브러리.

- <https://xtermjs.org/>
- <https://github.com/xtermjs/xterm.js>

## React + Tailwind로 tmux 연동

```
TmuxTerminal (React) ↔ WebSocket ↔ 백엔드 (node-pty) ↔ tmux
```

### 백엔드

`node-pty`로 tmux 세션을 열고 WebSocket으로 중계한다.

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
  const shell = pty.spawn('tmux', [
    'new-session', '-A', '-s', 'main',
  ], {
    name: 'xterm-256color',
    cols: 80,
    rows: 24,
    env: process.env as Record<string, string>,
  });

  shell.onData((data: string) => ws.send(data));

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

### 프론트엔드

xterm.js CSS는 Tailwind와 별도로 임포트해야 한다.

```bash
npm install @xterm/xterm @xterm/addon-fit
```

```typescript
// src/components/TmuxTerminal.tsx
import { useEffect, useRef } from 'react';
import { Terminal as XTerm, ITerminalOptions } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';
import '@xterm/xterm/css/xterm.css';

interface Props {
  wsUrl: string;
  sessionName?: string;
}

const TERMINAL_OPTIONS: ITerminalOptions = {
  cursorBlink: true,
  fontSize: 14,
  fontFamily: 'Menlo, Monaco, "Courier New", monospace',
};

export default function TmuxTerminal({
  wsUrl,
  sessionName = 'main',
}: Props) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const terminal = new XTerm(TERMINAL_OPTIONS);
    const fitAddon = new FitAddon();
    terminal.loadAddon(fitAddon);
    terminal.open(container);
    fitAddon.fit();

    const ws = new WebSocket(wsUrl);

    terminal.onData((data: string) => ws.send(data));
    ws.onmessage = (e: MessageEvent<string>) => terminal.write(e.data);
    terminal.onResize(({ cols, rows }: { cols: number; rows: number }) => {
      ws.send(JSON.stringify({ type: 'resize', cols, rows }));
    });

    const handleResize = () => fitAddon.fit();
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      ws.close();
      terminal.dispose();
    };
  }, [wsUrl]);

  return (
    <div className="flex h-screen flex-col bg-gray-950 p-4">
      <div className="mb-2 flex items-center gap-2 px-1">
        <span className="h-3 w-3 rounded-full bg-red-500" />
        <span className="h-3 w-3 rounded-full bg-yellow-400" />
        <span className="h-3 w-3 rounded-full bg-green-500" />
        <span className="ml-2 text-xs text-gray-400">{sessionName}</span>
      </div>
      {/* overflow-hidden 필수 */}
      <div
        ref={containerRef}
        className="flex-1 overflow-hidden rounded-lg bg-gray-900 p-2"
      />
    </div>
  );
}
```

사용:

```typescript
<TmuxTerminal wsUrl="ws://localhost:8080" sessionName="main" />
```
