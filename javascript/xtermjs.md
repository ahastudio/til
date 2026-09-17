# xterm.js

웹 브라우저에서 완전한 기능의 터미널 에뮬레이터를 구현하는 라이브러리.

<https://xtermjs.org/>

<https://github.com/xtermjs/xterm.js>

HN 토론: <https://news.ycombinator.com/item?id=28797535> (251점, 66개 댓글)

GN 토론: <https://news.hada.io/topic?id=5162>

## 무엇이고 무엇이 아닌가

xterm.js의 계약은 저장소가 직접 두 방향으로 규정한다.
제공하는 것은 브라우저에서 동작하는 터미널 에뮬레이터이고, 제공하지 않는 것은 내려받아 실행하는 터미널 애플리케이션과 셸 그 자체다.
`node-pty` 같은 라이브러리를 통해 bash 같은 프로세스에 연결되는 화면 쪽 절반이며, 나머지 절반은 직접 붙여야 한다.

이 경계가 아래 tmux 연동 예제의 구조를 설명한다.
xterm.js가 맡는 것은 키 입력을 이스케이프 시퀀스로 바꾸고 출력 바이트를 화면에 그리는 일뿐이고, 프로세스를 띄우고 그 입출력을 나르는 일은 전부 바깥에 있다.

이 분업이 보안 논의의 출발점이기도 하다.
Hacker News에서 hulitu는 브라우저에 터미널을 넣고 거기에 비밀번호를 입력하고 명령을 치는 것이 무엇이 문제겠냐고 비꼬았다.[^hulitu]
반론은 두 갈래로 나뉘었다.
emilfihlman은 브라우저에서 돌리는 것이 전용 터미널 클라이언트를 돌리는 것보다 더 신뢰할 수 없지도, 덜 신뢰할 수 없지도 않다고 적었고,[^emilfihlman] lhnz는 터미널이 브라우저 밖에서 실행될 때 오히려 더 잘 샌드박싱되느냐고 되물었다.[^lhnz]

이 반문이 핵심을 짚는다.
위협 모델을 비교하려면 브라우저인지 아닌지가 아니라 명령이 실제로 실행되는 곳이 어디이고 그 경로를 누가 통제하는지를 봐야 한다.
아래 예제에서 셸을 띄우는 것은 브라우저가 아니라 `node-pty`를 실행하는 서버이므로, 실질적인 위험은 xterm.js가 아니라 그 WebSocket 종단을 누가 열 수 있는지에 달려 있다.

핵심 기능은 다음과 같다.

- bash, vim, tmux, curses 기반 애플리케이션이 그대로 동작하며 마우스 이벤트도 지원한다
- GPU 가속 렌더링을 선택적으로 켤 수 있다
- 한중일 문자, 이모지, IME를 포함한 유니코드 지원
- 코어 라이브러리는 의존성이 없다
- 스크린 리더 모드를 포함한 접근성 기능
- 링크 감지, 테마, 커스텀 글리프

공식 애드온이 열두 개 있으며, 기능을 코어 밖으로 빼 두는 구조다.
웹 링크 감지, 클립보드 접근, 컨테이너 크기에 맞추기(fit), 이미지 렌더링, 합자(ligature), 검색, 유니코드 보강, WebGL 렌더링, 진행 표시줄 API가 여기 속한다.
아래 예제에서 `@xterm/addon-fit`을 따로 설치하는 이유가 이것이다.

지원 브라우저는 Chrome, Edge, Firefox, Safari의 최신 버전이며 Electron 앱에서도 동작한다.
VS Code, Hyper, Tabby, JupyterLab, Azure Cloud Shell을 비롯해 여러 클라우드 IDE와 개발자 도구가 이것을 쓴다.
라이선스는 MIT다.

### 지원 목록이 곧 모든 조합이 동작한다는 뜻은 아니다

Hacker News에서 messe가 공식 홈페이지 데모가 macOS Safari에서 글자가 아예 보이지 않는다고 보고하자, Tyriar는 원인이 Safari가 당시 새로 출시한 WebGL 2 구현의 문제이며, github.dev와 Codespaces에서는 Safari에서 WebGL 렌더러를 꺼서 우회하고 있다고 답했다.[^Tyriar-safari]
지원 브라우저 목록과 WebGL 가속은 각각 성립하지만 그 교집합은 깨져 있었고, 공식 데모조차 예외가 아니었다는 뜻이다.
애드온을 켜는 선택이 브라우저별로 다른 결과를 낳을 수 있으므로, WebGL 렌더러는 대상 브라우저마다 실제로 확인하고 필요하면 런타임에 끌 수 있게 두는 편이 안전하다.

VT 시퀀스 호환도 마찬가지로 완전하지 않다.
rbanffy가 VT100 고문 테스트(torture test)를 통과하는지 묻자 Tyriar는 흔히 쓰이는 시퀀스는 대체로 문제없지만 깜빡임과 두 배 높이·너비 문자는 동작하지 않는다고 밝혔고, 지원하는 VT 기능은 문서에 정리해 두었다고 안내했다.[^Tyriar-vt]
터미널 에뮬레이터를 고를 때 "vim과 tmux가 돈다"는 확인만으로는 부족하고, 실제로 쓸 시퀀스가 목록에 있는지 봐야 한다.

tmux를 붙일 때 나타나는 구체적인 마찰도 보고됐다.
sharikous는 tmux의 마우스 모드를 켜면 tmux가 선택 기능을 가져가 버려서, 브라우저 쪽에서 텍스트를 끌어 자기 클립보드로 복사하려는 동작이 막힌다고 적었다.[^sharikous]
다른 터미널 에뮬레이터에는 이 가로채기를 일시적으로 무시하는 단축키가 대개 있는데 xterm.js에 해당 옵션이 있는지 모르겠다는 것이다.
아래 tmux 연동 예제를 그대로 쓰면 이 문제를 만나게 되므로, 마우스 모드를 켤 계획이라면 복사 경로를 미리 정해 두어야 한다.

GeekNews에서 xguru는 실사용 목록이 웹 기반 IDE 거의 전부를 덮는다는 점을 짚으며, VSCode, RStudio, Theia, Azure Cloud Shell과 Data Studio, Hyper, cPanel, Webssh, Linode, Codecademy, Repl.it, HashiCorp Nomad, 그리고 국내 GoormIDE까지 나열했다.[^xguru]
브라우저에서 터미널을 보여 주는 제품을 만들 때 선택지를 비교하는 단계가 사실상 없다는 뜻이고, 이 영역에서는 표준 구현이 하나로 수렴해 있다.

### 이 라이브러리는 네 번의 포크를 거쳐 왔다

Hacker News 스레드에는 메인테이너인 Tyriar가 직접 나와 프로젝트의 계보를 정리했다.[^Tyriar]
Fabrice Bellard의 jslinux에서 시작해, Christopher Jeffrey가 터미널 부분을 term.js로 떼어냈고, 그것이 방치된 뒤 Paris Kasidiaris가 SourceLair에서 쓰려고 xterm.js로 다시 포크했다.
Tyriar 본인은 2016년 VS Code의 통합 터미널 후보를 검토하다가 합류해 이후 업무 시간의 상당 부분을 이 프로젝트에 쓰고 있다고 밝혔다.

계보에는 스레드 안에서 정정이 한 번 들어갔다.
rasengan이 xterm.js의 원작자를 Christopher Jeffrey로 소개하자, williamstein이 term.js의 원저자는 Bellard이고 Jeffrey가 한 일은 그 코드를 오픈소스로 재라이선스하도록 Bellard를 설득한 것이라고 바로잡았다.[^williamstein]
term.js는 원래 오픈소스 라이선스가 아니었고, 그 설득이 없었다면 오늘날의 xterm.js 계보 자체가 성립하지 않았다는 뜻이다.

이 내력이 실무에서 갖는 의미는 유지보수 주체의 성격이다.
현재 활성 메인테이너는 다섯 명이고, 그중 핵심 인력이 Microsoft에서 VS Code 팀으로 일하며 업무로 이 코드를 만진다.
개인 프로젝트가 방치되어 포크로 이어지는 일이 이미 이 계보에서 한 번 일어났는데, 지금은 이 라이브러리가 회사 제품의 핵심 부품이라 그 경로를 반복할 가능성이 낮다.

설치는 코어부터다.

```bash
npm install --save @xterm/xterm
```

`Terminal` 클래스를 가져와 DOM 요소에 연결하는 것이 기본 사용법이며, 함께 제공되는 CSS 스타일시트를 반드시 임포트해야 화면이 제대로 그려진다.

### 스레드에 올라온 실제 활용 방식

Hacker News 스레드에는 사용 사례가 여럿 올라왔는데, 앞서 정리한 IDE 목록과는 결이 다른 쪽이 흥미롭다.

parhamn은 Kubernetes의 `exec` 소켓 엔드포인트를 프록시하면서 기록 로그를 함께 남겨, 누가 무엇을 했는지 나중에 재생할 수 있는 내부 도구를 만들었다고 적었다.[^parhamn]
터미널 화면이 DOM이 아니라 바이트 스트림이라는 점을 역이용한 사례다.
입출력이 스트림이므로 중간에서 가로채 저장하면 그대로 세션 녹화가 되고, 감사 로그와 재생 기능이 별도 구현 없이 따라온다.

thinkafterbef는 CI 제품에서 로그 스트리밍과 브라우저 내 터미널 양쪽에 쓰고 있으며 WebGL 렌더러를 켜면 매우 빠르다고 했고,[^thinkafterbef] apignotti는 WebAssembly 기반 x86 가상 머신인 CheerpX의 REPL 데모에 붙였다고 밝혔다.[^apignotti]
biginkorea는 Scratch 같은 블록 기반 편집기로 아이들에게 프로그래밍을 가르치는 데 쓴다고 적었다.[^biginkorea]

공통점은 셸에 접속하는 용도가 아니라는 것이다.
로그 뷰어, 가상 머신 출력 창, 교육용 실행 화면처럼 "고정폭으로 흐르는 텍스트를 보여 주는 곳"이면 어디든 후보가 된다.
터미널 에뮬레이터를 터미널 접속이 필요할 때만 꺼내는 부품으로 생각하면 이 쓰임새를 놓친다.

## React + Tailwind로 tmux 연동

```text
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

---

[^xguru]: <https://news.hada.io/topic?id=5162#cid7213>

[^Tyriar]: <https://news.ycombinator.com/item?id=28799502>

[^williamstein]: <https://news.ycombinator.com/item?id=28799070>

[^Tyriar-safari]: <https://news.ycombinator.com/item?id=28799423>

[^Tyriar-vt]: <https://news.ycombinator.com/item?id=28799574>

[^sharikous]: <https://news.ycombinator.com/item?id=28800954>

[^hulitu]: <https://news.ycombinator.com/item?id=28798194>

[^emilfihlman]: <https://news.ycombinator.com/item?id=28798323>

[^lhnz]: <https://news.ycombinator.com/item?id=28798489>

[^parhamn]: <https://news.ycombinator.com/item?id=28799714>

[^thinkafterbef]: <https://news.ycombinator.com/item?id=28799680>

[^apignotti]: <https://news.ycombinator.com/item?id=28798522>

[^biginkorea]: <https://news.ycombinator.com/item?id=28800805>
