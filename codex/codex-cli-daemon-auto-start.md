# Codex CLI가 기본값으로 띄우는 상주 데몬: 설치한 도구와 실행되는 도구가 갈라질 때

원문: [CLI: make `daemon_auto_start` opt-in — a persistent, self-updating background daemon shouldn't be the default · Issue #48195 · openai/codex](https://github.com/openai/codex/issues/48195)

HN 토론: <https://news.ycombinator.com/item?id=50060694> (496점, 255개 댓글)

GN 토론: <https://news.hada.io/topic?id=35256>

## 요약

GitHub 사용자 Yihua-Liu-1997이
2026년 9월 25일 openai/codex 저장소에 올린 이슈다.
WSL2 위 Linux에서 `npm install -g @openai/codex`로
설치한 Codex CLI 0.157.0을 쓰다 겪은 동작을 정리하고,
CLI에서는 `daemon_auto_start`를 기본으로 끄거나
최소한 한 번 묻고 켜 달라고 요청한다.
이슈에는 `enhancement`, `CLI`,
`app-server` 라벨이 붙었고, 10월 13일 현재 열려 있다.

0.157.0부터 대화형 `codex` 세션을 여는 것만으로 네 가지 일이 일어난다.

1. 상주 백그라운드 데몬 `codex app-server --managed-daemon`이 뜬다.
TTY 없는 별도 세션에서 돌고, 모든 Codex 창을 닫아도 PID 1에 다시 붙어
`codex app-server daemon stop`이나 재부팅 전까지 계속 돈다.
2. 플랫폼 패키지 전체(약 374MB, `codex`, `codex-code-mode-host`,
번들된 `bwrap`·`zsh`·`rg`)를 `~/.codex/packages/app-server-daemon/releases/<version>/`에
npm이 막 설치한 것과 바이트 단위로 같게 복사하고, 데몬은 그 복사본에서 돈다.
이때부터 백엔드 버전은 패키지 관리자로 설치한 CLI 버전과 따로 움직인다.
3. 분리된 업데이터 `codex app-server daemon pid-update-loop`가 뜬다.
시작 5분 뒤, 그 뒤로는 매시간 업데이트를 확인해 새 릴리스를 받고 백엔드를 재시작하는데,
이 재시작은 진행 중인 작업을 죽일 수 있다(#40969).
4. 데몬을 처음 띄운 세션의 환경 변수가 고정된다.
작성자는 실행할 때마다 `HTTPS_PROXY`를 바꾸는 래퍼로 Codex를 띄우는데,
데몬은 첫 세션의 프록시를 붙잡고 이후 세션과 상관없이 그 프록시로 나간다.
데몬이 세션의 작업 디렉터리 대신 다른 곳을 쓰는 #42457, #37537도 같은 원인으로 보인다고 적었다.

작성자는 CLI라면 백엔드가 창과 함께 살고 죽으며,
자기가 설치한 바이너리를 돌리고,
백그라운드에서 스스로 업데이트하지 않는 것이
가장 덜 놀라운 기본값이라고 주장한다.
공유되고 스스로 업데이트되는 데몬은 원격 제어나 데스크톱 앱에는 맞으니
그쪽이나 사용자가 `codex app-server daemon start`를
직접 실행할 때만 켜면 된다는 것이다.
기본값을 유지하더라도 마지막 클라이언트가 끊기면 자동 시작한 데몬을 끝내고,
npm·brew·pacman 같은 패키지 관리자로 설치했을 때는
복사와 자체 업데이트를 하지 말라고 요구한다.

끄는 과정에서 버그도 하나 찾았다.
`codex app-server daemon stop`은 app-server만 멈추고
`pid-update-loop` 업데이터는 남겨 두어
70초 뒤에도 살아 있었다는 것이다.
작성자가 쓰는 우회 방법은 다음과 같다.

```sh
codex features disable daemon_auto_start
codex app-server daemon stop
pkill -f 'app-server daemon pid-update-loop'   # daemon stop으로는 멈추지 않는다
rm -rf ~/.codex/packages/app-server-daemon
```

댓글에서는 Windows 10 LTSC에서도 같은 문제가 재현되며
`config.toml`에 `daemon_auto_start = false`를 넣으면 해결된다는 확인,
Windows에서 CLI를 아예 쓸 수 없다는 보고가 이어졌다.
foma-agent는 공식 설정 문서에 `daemon_auto_start` 항목이 하나도 없고,
0.157.0 릴리스 노트도
“적격한 대화형 세션에 대해 백그라운드 서버 자동 시작을 켰다”는 한 문장뿐이라
상주 프로세스, 패키지 복사, 매시간 업데이터를 언급하지 않는다고 지적했다.

## 분석

### 핵심 쟁점은 “설치한 것”과 “실행되는 것”의 분리다

이슈가 지적한 네 가지 동작 가운데 가장 근본적인 것은 두 번째다.
사용자는 npm으로 특정 버전을 설치했지만,
실제로 요청을 처리하는 것은 `~/.codex` 아래 복사본이고
그 복사본은 매시간 업데이터가 바꿀 수 있다.
댓글의 aetherxeg-source는 이를
“설치된 CLI의 정체성 ≠ 데몬 실행 정체성”이라고 정리했다.
CLI가 자신을 관리 디렉터리로 복사하고 업데이터가 그 복사본을 바꿀 수 있으면,
나중의 작업을 처리하는 프로세스는 더 이상
사용자가 설치하거나 실행한 산출물이 아니라는 것이다.
그는 클라이언트가 연결될 때마다 CLI 버전, 데몬 바이너리 다이제스트, 데몬 세대,
업데이터 상태, 상속한 환경의 세대를 담은 실행 영수증을 보여 주자고 제안했다.

이 분리는 패키지 관리자가 하는 일을 무력화한다.
버전 고정, 롤백, 재현 가능한 환경 같은 것들은
설치된 파일이 실행되는 파일이라는 전제 위에 서 있다.
HN의 silverbluep는 Codex가 상태와 설정 데이터를 섞어 두어
nix-darwin으로 선언적으로 관리할 수 없어
쓰지 않게 되었다고 적었다.[^silverbluep]

### 데몬은 왜 생겼는가

데몬 자체에는 이유가 있다.
HN의 pilooch는 데몬이 그 서버 위에 앱을 만들 때,
예를 들어 맞춤 하네스를 붙일 때 유용하다면서도
기본값으로는 꺼야 한다고 했다.[^pilooch]
umutsevdi는 자기 도구를 벤치마크하다 첫 실행 이후
Codex가 놀랍도록 빨라진 것을 보고 데몬을 발견했다.[^umutsevdi]
상주 프로세스는 시작 비용을 없애고 여러 표면(CLI, 앱, 원격 제어)이
같은 백엔드를 공유하게 한다.
[Codex App Server](app-server.md)가 모든 표면의 공통 기반이 되는 구조에서는
자연스러운 다음 단계다.

문제는 그 이점을 위해 CLI 사용자의 기본 기대를 바꾸면서
그 사실을 알리지 않았다는 데 있다.
릴리스 노트의 한 문장과 문서에 없는 설정 항목은
이것이 사용자가 결정할 일이 아니라고 본 것처럼 읽힌다.

### 다른 도구도 같은 길을 가고 있다

HN의 timdorr는 Claude Code도 같은 운영 모델이라며,
이전 버전 바이너리가 여러 개 남아 있고 포그라운드에 Claude Code가 없어도
백그라운드 작업이 여러 개 돈다고 확인했다.[^timdorr]
icantevenhold는 Codex가 옛 버전으로 디스크를 채워
12GB 가까이 썼다고 적었다.[^icantevenhold]
에이전트 하네스들이 브라우저나 데스크톱 앱처럼
스스로를 관리하는 쪽으로 가고 있고,
CLI라는 외형과 그 동작 사이의 거리가 벌어지고 있다.

## 비평

### 자동 업데이트가 표준이라는 반론은 동의의 문제를 비켜 간다

HN의 dingaling911은 이 분야가 빠르게 움직이니 자동 업데이트가 당연하며,
브라우저도 그렇게 한다고 반박했다.[^dingaling911]
isityettime은 일반 패키지 관리자도 수천 개 프로그램을 자동으로,
원하면 백그라운드에서 업데이트할 수 있지만
사용자의 주권을 침해하지 않고 그렇게 한다고 답했다.[^isityettime]
piker는 법률용 IDE를 만들며 업데이트 방식을 고민한 경험을 들어,
버그 있는 버전이 퍼지는 것도 사용자에게 적대적이라며
이 결정을 옹호할 여지를 남겼다.[^piker]

문제는 업데이트 자체가 아니라 그 방식이 알려지지 않았다는 점이다.
브라우저의 자동 업데이트는 오래전부터 알려진 기본값이고
끄는 방법도 문서화되어 있다.
Codex의 데몬은 문서에 없는 기능 플래그 뒤에 있고,
릴리스 노트는 상주 프로세스와 패키지 복사를 말하지 않는다.
업데이트가 필요하다는 주장은 맞지만,
그 필요가 사용자 모르게 상주 프로세스를 띄울 이유가 되지는 않는다.

### “악성 코드 같다”는 반응은 과하지만 신호로는 읽어야 한다

이슈 댓글과 HN에는 이 동작을 악성 코드의 특징이라고 부르는 반응이 이어졌다.
회사의 Codex 좌석 라이선스를 거두겠다는 댓글도 있었다.
의도를 악의로 단정하는 것은 근거가 없다.
데몬은 공식 기능이고 끄는 방법도 있으며, 성능과 구조상의 이유가 있다.

그러나 사용자가 그런 말을 꺼냈다는 사실은 중요하다.
보안 팀이 상주 프로세스, 스스로 바뀌는 바이너리,
다른 세션의 환경 변수를 붙잡는 동작을
목록으로 보면 악성 코드 탐지 규칙과 많이 겹친다.
기업 환경에서 이런 도구는 기능이 아니라 탐지 대상으로 분류될 위험이 있고,
그것은 OpenAI가 원하는 결과가 아닐 것이다.

### 이슈의 요청은 부분적인 해법이다

이슈가 요구한 것은 기본값을 바꾸고, 마지막 클라이언트가 끊기면 데몬을 끝내고,
패키지 관리자 설치에서는 복사하지 않는 것이다.
이 셋이 모두 받아들여져도 환경 변수 고정 문제는 남는다.
데몬을 명시적으로 켠 사용자도
여러 세션이 서로 다른 프록시나 작업 디렉터리를 쓴다면
같은 문제를 겪는다.
kristjansson도 데몬 모드가
Codex CLI가 자신을 호출한 셸의 환경 변수를 물려받는다는
기본 가정을 깬다고 지적했다.[^kristjansson]
공유 데몬 구조라면 세션마다 환경을 전달하는 설계가 필요하고,
이것은 기본값 문제가 아니라 아키텍처 문제다.

## 인사이트

### 에이전트 도구의 신뢰는 기능보다 경계에서 결정된다

에이전트 하네스는 파일 시스템과 셸에 넓은 권한을 가진다.
사용자는 그 권한을
“내가 실행한 이 프로세스가, 내가 연 이 세션 동안” 쓴다고 가정하고 허락한다.
상주 데몬과 자체 업데이트는 그 시간적·공간적 경계를 흐린다.
st396gt는 전체 호스트 파일 시스템 읽기·쓰기 권한을 원한다는 문서 때문에
Codex를 격리된 Raspberry Pi에서 돌리고 SSH로 들어간다고 적었다.
HN의 clutter55561은 이런 도구를 호스트에 설치하지 말고
최소한 잠근 Docker 컨테이너에서, 버전을 고정해 돌리라고 권했다.[^clutter55561]

이 반응은 앞으로의 방향을 보여 준다.
도구가 자기 경계를 스스로 넓힐수록 사용자는 바깥에서 경계를 강제한다.
샌드박스, 컨테이너, 전용 머신은 이제 에이전트 도구를 쓰는 기본 전제가 되고 있다.

### 패키지 관리자가 다시 신뢰의 중재자가 된다

thebeardisred는 배포판 모델의 장점을 상기시켰다.[^thebeardisred]
누군가 소프트웨어를 패키징하고 시험하며 합리적인 기본값을 정해
이런 일이 일어나지 않게 한다는 것이다.
Cyph0n은 Nix/NixOS가 패키징할 때 자체
업데이트 동작을 켜려면 일부러 애써야 하게 만든다고 덧붙였다.[^Cyph0n]
whimblepop은 이런 동작이 Nix 패키지에서는 호환성 때문에 흔히 제거되고,
자신이 쓰는 Claude Code 패키지에서도 그렇다고 했다.[^whimblepop]

도구 제작사가 업데이트와 실행을 스스로 관리할수록
배포판 패키저의 역할은 그 관리를 걷어 내는 쪽으로 바뀐다.
1990년대 리눅스 배포판이 업스트림의 기본값을 다듬던 일이
AI 에이전트 도구에서 다시 중요해지고 있다.

### 빠르게 만든 도구는 빠르게 신뢰를 잃는다

HN의 esjeon은 Codex CLI와 Claude Code의 품질이
LLM 주도 개발의 현 상태를 그대로 보여 준다고 했다.[^esjeon]
flir는 두 CLI 모두 나빠지고 있는데,
코드 품질보다 충분히 고민하지 않은 기능을 계속 덧붙이기 때문이라고 봤다.[^flir]
AndreasBackx는 패키지 관리자로 해결한 소프트웨어 업데이트 문제를
AI 도구들이 다시 발명하고 있다고 지적했다.[^AndreasBackx]

기능을 하루 만에 만들 수 있게 되면
그 기능이 사용자 기대를 어떻게 바꾸는지 따지는 시간이 상대적으로 줄어든다.
이슈 작성자가 요구한 것은 새 기능이 아니라 기본값과 문서였다.
만드는 속도가 빨라질수록 차별점은 무엇을
기본으로 켜지 않을지 판단하는 데서 나온다.

---

[^silverbluep]: <https://news.ycombinator.com/item?id=50062392>

[^pilooch]: <https://news.ycombinator.com/item?id=50061573>

[^umutsevdi]: <https://news.ycombinator.com/item?id=50061894>

[^timdorr]: <https://news.ycombinator.com/item?id=50061258>

[^icantevenhold]: <https://news.ycombinator.com/item?id=50060934>

[^dingaling911]: <https://news.ycombinator.com/item?id=50060925>

[^isityettime]: <https://news.ycombinator.com/item?id=50061239>

[^piker]: <https://news.ycombinator.com/item?id=50061646>

[^kristjansson]: <https://news.ycombinator.com/item?id=50062278>

[^clutter55561]: <https://news.ycombinator.com/item?id=50062198>

[^thebeardisred]: <https://news.ycombinator.com/item?id=50061310>

[^Cyph0n]: <https://news.ycombinator.com/item?id=50061395>

[^whimblepop]: <https://news.ycombinator.com/item?id=50061569>

[^esjeon]: <https://news.ycombinator.com/item?id=50061272>

[^flir]: <https://news.ycombinator.com/item?id=50062221>

[^AndreasBackx]: <https://news.ycombinator.com/item?id=50062569>
