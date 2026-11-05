# wterm: DOM으로 그리는 웹 터미널 에뮬레이터

<https://github.com/vercel-labs/wterm>

HN 토론: <https://news.ycombinator.com/item?id=48320667> (66점, 18개 댓글)

GN 토론: <https://news.hada.io/topic?id=36554>

## 소개

wterm은 “dub-term”으로 읽는 웹 터미널 에뮬레이터이고,
Vercel Labs가 Apache-2.0 라이선스로 공개했다.
README의 첫 문장은 “웹을 위한 터미널 에뮬레이터”이고,
차별점으로 내세우는 것은 화면을 캔버스가 아니라 DOM에 그린다는 점이다.
선택, 복사와 붙여넣기, 브라우저 찾기,
접근성 기능이 마운트된 행(row) 위에서 브라우저 기본 동작 그대로 작동한다고
설명한다.
핵심 파서는 Zig로 작성해 WASM으로 컴파일했다.

저장소 메타데이터로 보면 2026-04-14에 만들어졌고,
이 글을 쓴 2026-11-04에도 푸시가 있었으며, 별은 3,642개다.
HN 스레드는 2026-05-29에 올라왔다.

## 패키지 구성

README는 패키지를 여덟 개로 나눠 소개한다.

| 패키지             | 역할                                                                      |
| ------------------ | ------------------------------------------------------------------------- |
| `@wterm/core`      | 헤드리스(headless) WASM 브리지, `TerminalCore` 인터페이스, WebSocket 전송 |
| `@wterm/dom`       | DOM 렌더러와 입력 처리기, 바닐라 JS 터미널                                |
| `@wterm/react`     | React 컴포넌트와 `useTerminal` 훅                                         |
| `@wterm/vue`       | Vue 3 컴포넌트                                                            |
| `@wterm/svelte`    | Svelte 컴포넌트                                                           |
| `@wterm/ghostty`   | libghostty 기반의 전체 VT 에뮬레이션 코어                                 |
| `@wterm/just-bash` | just-bash 3로 브라우저 안에서 도는 Bash 셸                                |
| `@wterm/markdown`  | 터미널에 Markdown을 렌더링                                                |

## 동작 방식

### 코어가 둘이고 선택할 수 있다

기본 코어는 Zig로 만든 VT100, VT220, xterm 이스케이프 시퀀스 파서이고,
릴리스 빌드에서 약 26KB의 `.wasm` 파일이 된다.
선택 사항인 `@wterm/ghostty`는 libghostty 코어를 쓰며,
README는 이쪽이 전체 VT 호환성을 준다고 설명한다.
Kitty 터미널 이미지, 밑줄 종류와 색, OSC 52 클립보드 요청,
셸 프롬프트 이동 같은 기능은 Ghostty 코어에서만 동작한다고 적혀 있다.
기본 코어는 지원하지 않는 Kitty 이미지 데이터를 안전하게 소비만 하고 디코딩하지
않는다.

### 화면은 바뀐 행만 다시 그린다

렌더러는 변경된 행만 `requestAnimationFrame`마다 다시 그리고,
스크롤백(scrollback)은 화면 주변의 행만 DOM에 두는 윈도 방식으로 유지한다.
저장된 출력 전체에 대한 찾기와 전체 선택은 DOM에 올라와 있지 않은 행까지
포함한다.
캔버스가 필요한 경우를 위해 `renderer: "webgl"` 옵션이 따로 있고,
이때도 선택과 찾기와 스크린 리더는 DOM 텍스트가 맡는다.
`WorkerCore`를 쓰면 파싱을 메인 스레드 밖으로 옮길 수 있다.

### 입력은 브라우저 이벤트를 터미널 규약으로 옮긴다

한글 IME 조합 중인 글자는 터미널 커서 위치에 임시로 보이고,
확정된 글자만 연결된 프로그램으로 전달된다.
마우스는 여러 보고 모드를, 키보드는 Kitty 키보드 프로토콜을 다룬다.
CJK와 이모지 같은 넓은 문자는 두 칸을 차지하며,
커서 주소로 다시 그릴 때에도 열이 어긋나지 않게 처리한다고 한다.

### 셸은 wterm 밖에 있다

wterm은 화면과 입력만 맡는다.
셸이나 PTY 프로세스를 띄우는 일은 하지 않고,
WebSocket으로 PTY 백엔드에 연결하는 전송 계층만 제공한다.
브라우저 안에서 완결되는 데모가 필요하면 `@wterm/just-bash`로 백엔드 없이 Bash
명령을 실행할 수 있다.
README는 이 외에 WebMCP를 켜면 브라우저 안의 에이전트가 터미널 목록,
화면과 스크롤백 텍스트, 출력 대기, 명령 입력, 키 입력을 쓸 수 있고,
읽기 전용 모드도 있다고 설명한다.

## 도입 전에 정할 것

| 결정      | 선택지                               | 판단 근거                                                                     |
| --------- | ------------------------------------ | ----------------------------------------------------------------------------- |
| 코어      | 기본 Zig 코어 / `@wterm/ghostty`     | 전체 VT 호환성이나 Kitty 이미지, OSC 시퀀스가 필요하면 Ghostty 코어다         |
| 렌더러    | DOM(기본) / `renderer: "webgl"`      | 선택과 찾기가 중요하면 DOM, 전체 화면 갱신과 이미지가 많으면 WebGL을 검토한다 |
| 파싱 위치 | 메인 스레드 / `WorkerCore`           | 터미널 여러 개에서 출력이 한꺼번에 쏟아지는 경우에 의미가 있다                |
| 셸 연결   | 자체 PTY 백엔드 / `@wterm/just-bash` | 실제 서버 셸이 필요한지, 브라우저 안의 흉내 셸로 충분한지에 달려 있다         |

연결 계층에서 정해야 할 일도 있다.
HN에서 dboreham은 브라우저가 원격 컴퓨터로 터미널 세션을 나를 네트워크 연결을 기본으로 만들 수 없고, 터널링 해법은 어색하거나 안전하지 않다고 지적했다.[^dboreham]
tracker1은 WSS를 Telnet이나 SSH 브리지에 잇거나 PTY 셸을 직접 호스팅하는 일은
어렵지 않고, 서명된 자격 증명(JWT 등)을 경로나 쿼리 문자열에 실을 수 있다고
반박했다.[^tracker1]
두 사람의 말을 합치면, wterm을 쓰더라도 세션을 누가 열 수 있는지 정하는 인증과
PTY 종단의 책임은 서비스를 만드는 쪽에 남는다.

## 비평

### README의 성능 근거는 측정 방법에 대한 설명이다

HN에서 toomim은 성능을 이유로 WASM으로 컴파일했지만, WASM과 자바스크립트 DOM 사이의 호출 비용이 크고 DOM UI는 캔버스보다 비용이 크므로 잘못된 방향으로 설계한 것은 아닌지, 실제 성능 평가가 보고 싶다고 적었다.[^toomim]
tracker1은 터미널에서는 WASM 브리지 비용이 브라우저의 렌더링 시간에 비해 눈에
띄지 않을 것이라고 답했다.[^tracker1-wasm]

README는 이 질문에 숫자로 답하지 않는다.
출력 부하, 지속 출력, 입력 응답, 히스토리 검색,
PTY 입력 지연을 각각 재는 벤치마크 명령과 보고서 위치는 자세히 적혀 있지만,
이 측정이 “네이티브 터미널의 처리량이나 실제 화면 표시 지연이 아니다”라고 스스로
선을 긋고,
CI는 속도 임계값 없이 정확성과 취소만 확인한다고 밝힌다.
따라서 toomim의 질문은 아직 열려 있다.
결론을 바꿀 관찰은 같은 부하에서 DOM 렌더러와 캔버스 기반 터미널을 같은
브라우저에서 비교한 수치이고, 도입하려는 쪽이 `pnpm bench:terminal`을 자기
워크로드에 맞게 돌려 보면 확인할 수 있다.

### 유지될 프로젝트인지는 HN의 의심과 저장소 상태가 엇갈린다

simjnd는 모든 커밋과 릴리스가 약 한 달 전의 짧은 기간에 몰려 있고 그 뒤로는
없으며, AI 덕분에 며칠 만에 운영 가능해 보이는 프로젝트를 만들고 흥미를 잃는
일이 쉬워졌고, Vercel Labs가 그런 실험을 쏟아내는 것 같다고 적었다.[^simjnd]
Vercel처럼 큰 회사가 내놓으면 거짓된 신뢰감을 줄 수 있으니 실험임을 분명히
밝혔으면 좋겠다는 말도 덧붙였다.

README 첫 줄의 배지는 이 저장소를 Vercel Labs 실험(LABS-EXPERIMENT)으로
표시하므로 라벨은 이미 붙어 있다.
그리고 저장소 메타데이터의 마지막 푸시는 2026-11-04이므로,
simjnd가 댓글을 쓴 5월 말 이후 활동이 없다는 관찰은 지금 시점에는 맞지 않는다.
다만 푸시가 있었다는 사실이 실험이 제품으로 바뀌었다는 뜻은 아니다.
이 문서는 커밋의 내용과 유지 보수 약속을 읽지 않았다.
도입 판단에는 이슈 처리 속도와 릴리스 주기,
그리고 Labs 라벨이 바뀌는지를 따로 확인해야 한다.

### 경쟁 구현과의 비교가 README에 없다

nacs는 같은 Ghostty 엔진을 쓰고 xterm.js와 API가 호환되는 ghostty-web이 이미
있고, wterm의 가벼운 코어는 전체 터미널 에뮬레이션을 하지 않고 나머지는
Ghostty에 맡긴다고 짚었다.[^nacs]
williamstein은 xterm.js의 큰 문제가 iOS 복사와 붙여넣기이고 그것을 그날 고쳤다고
적었다.[^williamstein]
theturtletalks는 Ghostty-Web을 쓰는 VibeTunnel 구성을 wterm으로 바꾸려 했지만
되지 않았고, Ghostty-Web은 캔버스를,
wterm은 일반 div 태그를 그리기 때문일 것이라고 추측했다.[^theturtletalks]

README에는 xterm.js, ghostty-web,
ttyd 같은 기존 선택지와 무엇이 다른지에 대한 비교가 없다.
jerrythegerbil은 더 오래되어 검증된 것을 원한다면 ttyd가 비교 대상이라고
제안했다.[^jerrythegerbil]
theturtletalks의 사례는 한 사람의 추측이어서,
DOM과 캔버스 차이가 실제 원인인지는 이 글에서 확인하지 못했다.
기존 xterm.js 위에 만든 제품이 있다면 바꿀 이유는 DOM 렌더링의 선택과 접근성
동작이 필요한가에서 출발해야 한다.

## 확인하기

README가 안내하는 가장 단순한 확인은 `web/` 디렉터리를 정적 파일 서버로 띄우는
것이다.

```bash
cd web && python3 -m http.server 8000
```

Kitty 이미지처럼 Ghostty 코어가 필요한 기능은 README의 Ghostty 예제로 따로
확인한다.

```bash
pnpm install
pnpm --filter ghostty-example dev
```

도입 전 확인 목록은 다음과 같다.

- 한글 IME 조합과 선택, 복사가 실제 사용할 브라우저에서 기대대로 동작하는가
- 기본 Zig 코어로 쓰는 프로그램(tmux, vim 등)의 화면이 깨지지 않는가
- 자신의 출력량에서 `pnpm bench:terminal`의 프레임 간격이 허용 범위인가
- PTY 백엔드의 인증과 세션 수명이 정해져 있는가
- Labs 실험이라는 라벨이 바뀌지 않아도 감당할 수 있는 의존인가

---

[^dboreham]: <https://news.ycombinator.com/item?id=48324080>

[^tracker1]: <https://news.ycombinator.com/item?id=48326758>

[^toomim]: <https://news.ycombinator.com/item?id=48326045>

[^tracker1-wasm]: <https://news.ycombinator.com/item?id=48326702>

[^simjnd]: <https://news.ycombinator.com/item?id=48324839>

[^nacs]: <https://news.ycombinator.com/item?id=48323439>

[^williamstein]: <https://news.ycombinator.com/item?id=48327925>

[^theturtletalks]: <https://news.ycombinator.com/item?id=48325530>

[^jerrythegerbil]: <https://news.ycombinator.com/item?id=48325844>
