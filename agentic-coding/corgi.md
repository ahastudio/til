# Corgi: 사람과 에이전트를 위한 터미널 멀티플렉서

<https://corgi.computer/>

<https://github.com/tals/corgi>

Show HN: [Corgi, a helpful {agent, terminal} multiplexer](https://news.ycombinator.com/item?id=50214373)

GN 토론: <https://news.hada.io/topic?id=35971>

## 소개

Corgi는 터미널과 코딩 에이전트를 작업 공간 단위로 붙들어 두는 터미널
멀티플렉서다.
홈페이지의 소개 문구는 사람과 에이전트를 위한 터미널 멀티플렉서이고,
저장소 README는 herdr에 크게 영감을 받았고 Ghostty로 구동된다고 적는다.
TypeScript로 쓰였고 MIT 라이선스이며,
저장소는 2026년 9월 20일에 만들어져 확인한 시점에 별 148개, 포크 9개,
열린 이슈 10개였고 마지막 푸시는 10월 25일이었다.

지원하는 에이전트는 Claude Code, Codex, Pi, OpenCode다.
어느 창에서든 `claude`, `codex`, `pi`, `opencode`를 실행하면 Corgi가 알아채고
각 에이전트의 설정에 자기 훅을 추가한다.
Pi에는 확장이 설치되고 OpenCode는 아무것도 필요 없으며,
Codex는 `/hooks`에서 한 번 신뢰 여부를 묻는다.
설치는 `curl -fsSL https://corgi.computer/install.sh | bash` 한 줄이고,
README는 macOS(Apple Silicon)와 Linux(amd64)를 지원하며 홈페이지는 WSL도
지원한다고 쓴다.

Show HN 글을 쓴 제작자 eiopa는 Herdr에 영감을 받아 몇 주 동안 매일 쓰는 도구로
만들었다고 밝히고
오랜 병가 중에 스스로에게 과제를 주려고 만들었으며 결과는 기대보다 엇갈린다고
적었다.[^eiopa]

## 주요 기능

- 각 에이전트의 상태를 working, needs you, finished, idle로 보여 주고
  `F1`로 다음에 읽지 않은 에이전트로 건너뛴다.
- `Ctrl-T`로 새 에이전트 탭을 열고 여러 계정을 하나의 런처에서 고르며
  세션 검색과 재개, 토큰과 사용량 추적이 들어 있다.
- tmux처럼 프로세스가 백그라운드에서 계속 돌고 `corgi`를 다시 실행하면 접속한다.
- 에이전트가 건드린 파일을 한 번에 훑는 변경 보기와 git worktree 지원,
  작업 공간별 CPU, 메모리, GPU 사용량 표시가 있다.
- 링크를 클릭으로 복사하고, ⌘V로 이미지를 붙이며 SSH에서도 동작한다.
  이 기능은 Ghostty Nightly가 필요하다고 홈페이지가 적는다.
- 홈페이지는 Corgi를 tmux, Herdr, cmux와 비교하는 표를 싣는다.
  이 문서는 그 표의 칸을 읽지 못했다.

README의 에이전트별 지원 표는 상태 표시, 활동 요약, 컨텍스트와 토큰과 한도,
이름 바꾸기와 포크, 충돌 뒤 재개를 네 에이전트 모두에 준다고 적는다.
하위 에이전트(subagent) 표시는 Pi에 없고 다중 계정은 OpenCode에 없다.

## 첫 사용과 스크립팅

처음에는 프로젝트 디렉터리에서 `corgi`를 실행해 단축키 프리셋을 고른다.
기본 접두 키는 `Ctrl+B`이고 접두 키 뒤에 `?`를 누르면 단축키 메뉴가 열린다.
메뉴의 분리(Detach)를 고르면 프로세스를 남겨 둔 채 나가고 다시 `corgi`를
실행하면 이어진다.

설정 문서에 따르면 기존 도구에서 가져오기를 지원한다.
tmux에서는 폴더, 창 이름, 분할 배치, 최근 출력을 가져오고 원래 세션은 그대로
둔다.
Herdr는 복사와 인계 두 가지가 있고 인계는 실행 중인 프로세스까지 Corgi로
소유권을 옮긴다.
cmux는 저장된 작업 공간과 대략의 배치를 가져온다.[^reference]

`corgi`는 실행 중인 세션을 어느 셸에서든 제어한다.
README의 예는 다음과 같다.

```bash
corgi list
corgi tab new --workspace 1 --command 'bun run dev'
corgi pane split current --right --command codex
corgi pane send 3 'run the tests' --enter
corgi pane read 3 --lines 50
```

창 안의 에이전트가 `corgi --skill`을 실행하면 이 인터페이스를 스스로 배운다고
한다.

## 구조

개발 문서는 데몬이 프로세스, PTY, 작업 공간, 대화를 소유하고
뷰어가 스냅샷과 터미널 표면으로 화면을 구성하며 각 뷰어가 자기 포커스와 스크롤과
선택을
따로 가진다고 설명한다.[^hacking]
CLI와 뷰어의 변경은 같은 명령을 쓴다.[^hacking]
바이너리에는 네이티브 공유 라이브러리 두 개가 들어 있다.
`corgi_term`이 Ghostty 터미널 에뮬레이션, 렌더링, 프레임 차이, 입력 인코딩을
맡고
`corgi_system`이 POSIX와 PTY 도우미, 프로세스 조사, 자원 표본, 충돌 보고를
맡는다.[^hacking]
정책은 TypeScript에 두고 네이티브 경계는 작게 유지한다는 것이 문서의
방침이다.[^hacking]

## 분석

### 터미널 대신 주의가 관리 대상이 된다

tmux는 프로세스가 연결이 끊겨도 살아 있게 하는 문제를 풀었다.
Corgi가 앞세우는 것은 여러 에이전트 가운데 누가 사람을 필요로 하는지다.
working, needs you, finished 같은 상태와 읽지 않은 에이전트로 건너뛰는 `F1`,
에이전트가 한 일을 보여 주는 활동 기록이 모두 이 질문에 답한다.
제작자도 에이전트가 무엇을 하는지 보여 주고 다음에 읽지 않은 에이전트로 가는
단축키를
핵심 개선으로 꼽았다.[^eiopa]

이 구성은 에이전트를 여럿 돌릴 때 병목이 터미널 창의 개수가 아니라
사람의 확인 순서라는 가정에 선다.
이는 이 문서의 해석이고 제작자가 그렇게 말하지는 않았다.

### 새 도구가 갈아타는 비용을 먼저 낮춘다

Corgi는 Herdr의 키맵을 닮은 프리셋을 주고 Herdr와 tmux와 cmux의 작업 공간을
가져오며, Herdr에서는 실행 중인 프로세스까지 인계받을 수 있다.[^reference]
제작자도 HN에서 Herdr와 비슷한 키맵이 있고 작업 공간, 탭, 창, 실행 중인
프로세스를
옮긴다고 답했다.[^eiopa-keymap]
README는 herdr를 주된 영감으로 밝히고 알림음 파일이 herdr의 Apache-2.0 아래
그대로 들어 있다고 쓴다.

도구의 우위를 기능이 아니라 이주의 쉬움으로 만드는 방식이다.
HN의 xfalcox는 Herdr를 쓰는데 이것이 그 2판처럼 보인다고 했고,[^xfalcox]
pokpokpok은 한 달쯤 써 보니 cmux를 대체하기에 좋고 설계가 단순하다고
했다.[^pokpokpok]

### 에이전트가 이 도구의 사용자이기도 하다

`corgi pane send`와 `pane read`로 한 창의 에이전트가 다른 창을 읽고 입력할 수
있고,
`corgi --skill`이 에이전트에게 사용법을 가르친다.
정리 기능도 에이전트를 쓴다.
제작자는 값싼 추론이 있다고 가정하고 에이전트를 다시 써서 링크, 워크트리, 각
에이전트의 하는 일을
정리해 준다고 했다.[^eiopa]
도구가 사람만이 아니라 에이전트의 조작 대상이 되도록 설계된 것이다.

## 비평

### 개선했다는 주장이 검증 없이 제시된다

홈페이지의 비교표와 제작자의 개선했다는 말은 서로 다른 도구와 같은 조건에서
시험한 결과가 아니다.
이 문서는 비교표의 칸을 읽지 못했고, 댓글의 평가도 사용 인상이다.
antouank는 Herdr보다 세련되고 현대적이라고 인정하면서도
거대한 TS 파일이 규모가 커질 때의 버그를 걱정하게 한다고 적었다.[^antouank]
제작자는 큰 파일이 우려스럽고 실제로는 생각보다 견뎠지만 결국 무너지기에
리팩터링 중이라고 답했다.[^eiopa-reply]
gillesjacobs는 다시 그리기와 깜박임 버그가 있다고 보고했다.[^gillesjacobs]
저장소가 한 달 남짓 된 점을 감안하면 안정성은 아직 증명되지 않았다.

### 여러 기계를 잇는 일상적 작업 흐름이 비어 있다

antouank는 Herdr처럼 다른 기계와 매끄럽게 연결되지 않아서 주력으로 바꾸지
못한다고 했다.[^antouank]
linsomniac은 Herdr를 작업용 컴퓨터에서 돌리고 노트북에서 접속해 쓰는 것이 핵심
기능이라며
여러 로컬 연결이 가능한지 물었다.[^linsomniac]
제작자는 자신도 여러 기계에서 일해서 원격 지원이 없는 것이 불편하고 다음 큰
과제라고 답했다.[^eiopa-reply]
Windows는 WSL2로만 동작하며 네이티브는 에이전트가 까다로웠다고
한다.[^eiopa-windows]
frumiousirc는 X11식 선택과 붙여넣기를 쓸 수 있는지 물었는데, 이 스레드에서 답이
보이지 않았다.[^frumiousirc]
세션을 오가며 쓰는 사용자에게는 핵심 기능이 아직 약속인 셈이다.

### 설치 방식과 다른 도구의 설정을 고치는 방식이 신뢰 범위를 넓힌다

`curl | bash` 설치에 대해 robsalasco는 brew에 올려 달라고 요청했다.[^robsalasco]
제작자는 패키지 관리자도 결국 같은 위험이라고 답했고,[^eiopa-curl]
mikemcquaid는 Homebrew가 몇 년 전부터 macOS 샌드박스를 쓰고 `.pkg` 설치도
제공한다고
알려 주었다.[^mikemcquaid]
제작자는 설치 단계의 공격 하나가 줄 뿐 바이너리 자체와 공급망이 남는다고
정리했다.[^eiopa-curl2]

여기에 더해 Corgi는 에이전트를 알아채면 각 에이전트의 설정에 훅을 추가한다.
사용자의 Claude Code와 Codex 설정을 다른 도구가 고치는 구조여서,
설치 한 번이 여러 도구의 설정을 바꾼다.
이는 이 문서의 지적이며 훅이 어떤 파일을 어떻게 고치는지는 확인하지 못했다.

## 인사이트

### 멀티플렉서의 희소 자원이 연결에서 주의와 토큰으로 옮겨 갔다

tmux가 풀던 문제는 끊긴 연결에서 작업을 살리는 것이었다.
에이전트 시대의 희소 자원은 사람이 한 번에 신경 쓸 수 있는 에이전트 수와
계정별 토큰 한도다.
Corgi가 상태 표시, 읽지 않은 에이전트로의 이동, 토큰과 사용량 추적을 전면에 둔
것은
이 이동을 따른 설계다.

이는 이 문서의 해석이다.
이를 따르면 에이전트 도구를 고를 때 기준은 창을 몇 개 나누느냐가 아니라
사람이 개입해야 할 순간을 얼마나 정확히 알려 주느냐다.
이 해석이 틀렸다면 대부분의 에이전트가 사람을 거의 필요로 하지 않는 수준까지
올라
상태 표시의 값이 떨어질 것이다.

### 모든 에이전트의 출력이 거치는 층은 새로운 신뢰 경계다

Corgi는 에이전트의 활동 요약을 만들고 각 에이전트가 무엇을 하는지 에이전트를
시켜 정리한다.
따라서 이 도구는 모든 에이전트의 출력과 입력이 지나가는 자리에 있고,
자기 데몬이 PTY와 작업 공간을 소유한다.
설정에 훅을 넣는 것까지 합치면 하나의 층이 여러 도구를 보고 고친다.

이 점은 이 문서의 추론이다.
이 추론은 터미널 멀티플렉서가 원래 모든 입력을 지나가게 하는 도구였다는 사실에
새로운 부담을 더한다.
이제는 멀티플렉서가 에이전트의 설정까지 바꾸므로 공급망 침해의 영향이 한 단계 더
넓어진다.
HN의 논쟁에서 제작자가 말한 바이너리와 공급망이 문제의 본체라는 말이 이 지점에서
무게를 갖는다.[^eiopa-curl2]

### 한 사람이 몇 주 만에 만든 도구가 이주 도구와 함께 시장에 들어온다

제작자는 몇 주 쓴 도구를 공개했고 HN에서 syngrog66은 몇 주 된 도구를 온 세상에
알린다고 비꼬았다.[^syngrog66]
dang은 새로운 프로젝트와 AI가 만든 프로젝트도 흥미로울 수 있다고 답했다.[^dang]
도구는 가져오기와 인계로 기존 사용자를 데려올 준비를 하고 나온다.
만드는 비용이 낮아진 시기에 이 분야는 에이전트 멀티플렉서가 여럿 경쟁하는 모양이
된다.

이 상황의 긴장은 갈아타기가 쉬워질수록 기존 도구의 사용자 기반이 약해지고,
새 도구도 같은 이유로 쉽게 다시 버려질 수 있다는 점이다.
이 해석은 이 문서의 것이고 이 분야의 도구 수는 확인하지 않았다.

### 이 글을 읽는 방법

이 문서는 홈페이지의 본문 텍스트와 README, 설정 문서, 개발 문서를 읽고 Show HN
스레드를 확인했다.
도구를 설치하거나 실행하지는 않았고 홈페이지의 비교표 칸은 읽지 못했다.

주장을 가를 관찰은 두 가지다.
하나는 같은 작업량에서 에이전트를 여러 개 돌려 Corgi와 tmux, Herdr, cmux를 견준
독립 비교이고
깜박임과 메모리 사용량이 포함되어야 한다.
다른 하나는 훅이 에이전트 쪽 형식 변화에 얼마나 자주 깨지는지와 원격 지원이
실제로 들어오는지다.
앞의 것이 있으면 개선했다는 주장을, 뒤의 것이 있으면 일상적으로 쓸 수 있는
도구가 되는지를 알 수 있다.

---

[^reference]: GitHub, [Using Corgi](https://github.com/tals/corgi/blob/main/docs/reference.md)

[^hacking]: GitHub, [Working on Corgi](https://github.com/tals/corgi/blob/main/HACKING.md)

[^eiopa]: <https://news.ycombinator.com/item?id=50214373>

[^eiopa-keymap]: <https://news.ycombinator.com/item?id=50223000>

[^eiopa-reply]: <https://news.ycombinator.com/item?id=50220739>

[^eiopa-windows]: <https://news.ycombinator.com/item?id=50223877>

[^eiopa-curl]: <https://news.ycombinator.com/item?id=50218387>

[^eiopa-curl2]: <https://news.ycombinator.com/item?id=50222874>

[^xfalcox]: <https://news.ycombinator.com/item?id=50218291>

[^pokpokpok]: <https://news.ycombinator.com/item?id=50217236>

[^antouank]: <https://news.ycombinator.com/item?id=50220652>

[^gillesjacobs]: <https://news.ycombinator.com/item?id=50220295>

[^linsomniac]: <https://news.ycombinator.com/item?id=50222090>

[^frumiousirc]: <https://news.ycombinator.com/item?id=50230813>

[^robsalasco]: <https://news.ycombinator.com/item?id=50217652>

[^mikemcquaid]: <https://news.ycombinator.com/item?id=50218762>

[^syngrog66]: <https://news.ycombinator.com/item?id=50217777>

[^dang]: <https://news.ycombinator.com/item?id=50232956>
