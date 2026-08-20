# 2026년 개발자가 매일 쓰는 소프트웨어 목록에 AI가 거의 없다

원문: [What software do you use daily in 2026?](https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026)

GN 토론: <https://news.hada.io/topic?id=32630>

## 요약

2026년 8월 18일 Lobste.rs에 `r1w1s1`이 올린 질문 글이다.
`ask`와 `practices` 태그가 붙었고 공개 시점 47점에 댓글 84개다.

질문은 6년 전의 비슷한 스레드를 명시적으로 참조한다.
그때 이후 사람들의 일상 구성이 어떻게 바뀌었는지가 궁금하다며, 운영체제와 데스크톱 환경 또는 창
관리자, 터미널, 셸, 에디터, 브라우저, 그리고 일상 작업 흐름에 필수라고 여기는 다른 도구를 묻는다.
특히 없어서는 안 될 것이 된 작고 덜 알려진 도구에 관심이 있다고 덧붙인다.

답변의 형식은 대체로 항목 나열이다.
가장 많은 표를 받은 것은 `rprospero`의 답으로, 주요 도구는 이미 다뤄졌으니 아직 안 나온 작은 것들을
적겠다며 로컬 환경 관리에 `direnv`(99%는 그냥 nix를 쓰는 것), 터미널에서 이미지를 보는 `chafa`,
PNG나 CBOR 같은 바이너리를 탐색하는 `fq`, 웹과 문서 검색에 `hister`, 대시보드에 `quickshell`,
버전 관리에 `jujutsu`를 든다[^rprospero].
같은 표수로 `liberty`의 세 단어짜리 답이 나란히 있다 — “Emacs가 전부다”[^liberty].

`hister`를 만든 `asciimoo`가 스레드에 나타나 자기가 개발한 소프트웨어를 누군가 쓰는 것을 보는 일이
언제나 동기 부여가 된다며 개선했으면 하는 점을 알려 달라고 한다[^asciimoo].

구성의 폭이 넓다.
`beto`는 NetBSD에서 `ctwm`, `urxvt`, `nvi`, `mutt`, `git`, `gforth`, `lynx`, Firefox만 쓰며 단순함을
유지하려 노트 도구 같은 것을 Tcl로 다시 쓰는 중이라고 한다[^beto].
질문을 올린 `r1w1s1` 자신은 KDE에서 IceWM과 PekWM과 dwm을 거쳐 cwm으로, Vim에서 nvi로 옮기며
자연스럽게 더 작고 단순한 도구만 남았고 지금은 Slackware-current 위에서 `cwm`과 `xterm`+`tabbed`+
`tmux`와 Bash와 `nvi`를 쓴다고 적는다[^r1w1s1].

반대편에는 도구를 직접 만드는 사람들이 있다.
`chrismorgan`은 Sway를 직접 확장한 데스크톱 환경처럼 쓰며 달력과 여러 시간대와 임시 세션을 단축키로
띄우고, `darkman`으로 Alacritty와 Firefox와 실행 중인 모든 Vim의 색상표까지 한 번에 바꾸며 Vim 서버
목록에 원격 명령을 보내 갱신하도록 구성했다고 한다[^chrismorgan].

## 6년 사이 무엇이 바뀌었나

질문자가 언급한 6년 전 스레드는 2019년 9월 24일 글이고 66점에 댓글 149개였다.
두 스레드의 댓글 본문에서 도구 이름이 등장한 횟수를 세면 변화의 방향이 보인다.

| 도구             | 2019 (댓글 149) | 2026 (댓글 84) |
| ---------------- | --------------- | -------------- |
| Firefox          | 59              | 32             |
| vim 계열         | 44 + neovim 9   | 10 + neovim 10 |
| Emacs            | 39              | 15             |
| Ubuntu           | 19              | 0              |
| Slack            | 20              | 1              |
| i3               | 14              | 0              |
| macOS            | 10              | 18             |
| NixOS / nix      | 목록 밖         | 7 + 5          |
| Ghostty          | 존재하지 않음   | 10             |
| Helix            | 존재하지 않음   | 5              |
| Zed              | 존재하지 않음   | 5              |
| Sway / Niri      | 목록 밖         | 5 + 7          |
| zoxide / atuin / direnv / jujutsu | 존재하지 않음 | 4 / 2 / 4 / 7 |

댓글 수가 다르므로 절대 수치보다 비율로 봐야 한다.
Firefox는 두 스레드 모두에서 댓글당 0.4회 안팎으로 가장 많이 언급된 소프트웨어 자리를 지켰다.
`rplacx`는 Mozilla Browser 시절에 옮겨 온 뒤 지금까지 매일 쓰는 가장 오래된 소프트웨어가 Firefox라고
적는다[^rplacx].

줄어든 쪽은 뚜렷하다.
Ubuntu와 i3와 Slack이 목록에서 사실상 사라졌고, Vim과 Emacs의 언급 비율도 절반 아래로 떨어졌다.
늘어난 쪽은 macOS, NixOS, 그리고 6년 전에는 존재하지 않던 도구들이다 — Ghostty, Helix, Zed, Niri,
`zoxide`, `atuin`, `jujutsu`.

그리고 AI 도구가 거의 없다.
84개 댓글 전체에서 “Claude”는 4회, “LLM”은 4회, “AI”는 3회 등장하고 Copilot과 Cursor와 ChatGPT는
0회다.
`mosburger`가 업무 구성 목록에 “AI: Claude code” 한 줄을 넣었고[^mosburger], `emrox`가
“AI: Claude Code, Crush, Orca”를 적었으며[^emrox], `giffengrabber`가 도구 목록 끝에 “LLM(요즘은 주로
Google Gemini)”을 붙였다[^giffengrabber].
`square_usual`은 기본 에이전트 작업 도구가 Pi이고 필요할 때 Claude를 쓴다면서, LLM의 도움으로 GUI
편집기에서 좋아하던 검토 기능을 Vim에 재현한 덕분에 VS Code와 Zed를 지웠다고 적는다[^square_usual].
`tcvsuv`는 브라우저로 LibreWolf를 고른 이유를 “AI도 감시도 없어서”라고 한 줄로 적는다[^oceanhaiyang].

## 분석

### 이 스레드가 재는 것은 채택률이 아니라 정체성이다

“매일 무엇을 쓰는가”라는 질문에 사람들이 답한 방식을 보면 이것이 사용 조사가 아니라는 것이 분명해진다.

답변의 형식이 거의 예외 없이 항목 나열이고, 나열의 순서가 운영체제부터 시작해 창 관리자와 터미널과
셸과 에디터로 내려간다.
질문이 그 순서를 제시했기 때문이기도 하지만, 그 목록 자체가 이 커뮤니티에서 자기를 소개하는 표준
양식이다.

그래서 여기 적히는 것은 사용 시간이 긴 것이 아니라 선택했다고 말할 만한 것이다.
`giffengrabber`가 Emacs와 Firefox와 Ghostty를 앞에 놓고 Microsoft Teams를 “유감스럽게도”라는
단서와 함께 중간에 끼워 넣은 것[^giffengrabber]이 그 구분을 그대로 보여 준다.
Teams는 매일 쓰지만 정체성이 아니고, `cwm`은 정체성이다.

이 성격을 이해하면 뒤에 나올 AI 도구의 부재를 어떻게 읽을지도 정해진다.
쓰지 않는다는 뜻이 아니라 목록에 적을 만한 것으로 여기지 않는다는 뜻일 수 있고, 그 둘은 다른 사실이다.

### 6년의 변화가 방향이 아니라 층위에서 일어났다

표를 보면 큰 것들은 거의 그대로다.
Firefox가 여전히 1위이고, 셸은 여전히 bash와 zsh와 fish로 갈리고, `tmux`와 `git`은 그대로 있다.

바뀐 것은 그 아래층이다.
Ubuntu가 사라지고 NixOS가 들어왔으며, i3가 사라지고 Sway와 Niri가 들어왔고, 터미널 자리에 Ghostty가
생겼다.
그리고 6년 전에는 아예 범주가 없던 도구들이 들어왔다 — 디렉터리 이동의 `zoxide`, 셸 이력 동기화의
`atuin`, 환경 관리의 `direnv`.

이 변화의 공통점은 전부 기존 것을 대체한 것이 아니라 기존 것의 마찰을 없앤 것이라는 점이다.
`WeetHet`은 `zoxide`가 터미널 이동을 실제로 쓸 만하게 만들어 준 없어서는 안 될 도구라고 적고,
같은 답변에서 컨테이너가 쓰던 메모리를 제대로 반환하는 유일한 Docker 엔진이라며 OrbStack을
든다[^WeetHet].
둘 다 새로운 일을 하게 해 주는 도구가 아니라 이미 하던 일의 성가심을 줄이는 도구다.

`curiositry`의 답이 이 층위를 명시적으로 설명한다.
배포판과 타일링 창 관리자를 많이 바꿔 보다 결국 평범한 구성에 정착했으며, `zoxide`로 디렉터리를
이동하고 `fzf`로 셸 이력과 경로를 채우고 실행기와 launch-or-raise 단축키를 조합하니 파일과 앱과
디렉터리에 거의 즉시 접근할 수 있게 됐다는 것이다[^curiositry].
윗층은 지루하게 두고 아랫층을 다듬는 전략이다.

### Nix가 개별 도구가 아니라 층으로 등장한다

2019년 목록에 없다가 2026년에 뚜렷해진 것 중 성격이 다른 하나가 Nix다.

다른 항목들은 자리를 차지한다 — 터미널 자리에 Ghostty, 에디터 자리에 Helix.
Nix는 자리를 차지하지 않고 다른 항목들이 어떻게 설치되고 재현되는지를 규정한다.
`dkl`이 회사에서는 macOS를 쓰고 집에서는 NixOS를 쓰는데 양쪽 모두 `home-manager`가 없어서는 안
된다고 한 것[^dkl]이 그 성격을 보여 준다 — 운영체제가 달라도 같은 층이 깔린다.

`rprospero`가 `direnv`를 설명하며 “99%는 그냥 nix를 쓰는 것”이라고 괄호를 단 것[^rprospero]도 같은
관찰이다.
도구 이름은 `direnv`인데 실제로 하는 일은 Nix 환경을 디렉터리에 붙이는 것이다.

`jeezy`의 답은 이 층이 어디까지 확장되는지 보여 준다.
컴퓨터 앞에 있는 시간을 줄일수록 설정을 자주 바꾸지 않는 도구만 남게 됐고, NixOS와 `deploy-rs`로
모든 장비를 관리하며 NixVim과 AdGuard Home과 OPNsense를 쓴다는 것이다[^jeezy].
개인 워크스테이션과 가정 서버와 방화벽이 같은 선언 파일 아래로 들어간 형태다.

## 비평

### 표본이 이 결론을 지지하지 못한다

이 스레드에서 가장 눈에 띄는 사실 — 2026년에 개발자들이 매일 쓴다고 답한 목록에 AI가 거의 없다는
것 — 을 일반적 진술로 옮기면 곧바로 무너진다.

Lobste.rs는 초대제 커뮤니티이고 회원 구성이 특정 취향으로 강하게 치우쳐 있다.
NetBSD와 Slackware와 `nvi`가 상위 답변에 오르는 곳이며, 질문자 본인이 더 작고 단순한 도구로 옮겨 온
이력을 답변으로 적는 곳이다.
같은 질문을 다른 곳에서 하면 다른 목록이 나온다는 것은 확인할 필요도 없다.

그리고 이 스레드의 성격 자체가 편향을 만든다.
질문이 “작고 덜 알려진 도구”에 특히 관심 있다고 명시했으므로, 답변자들은 모두가 아는 것을 빼고
적는다.
`rprospero`가 첫 문장에서 주요 도구는 이미 다뤄졌으니 다른 것을 적겠다고 한 것[^rprospero]과
`sourcemap`이 흔한 것들을 괄호로 묶어 두고 덜 알려진 도구에 집중하겠다고 한 것[^sourcemap]이 그
규범을 보여 준다.
Claude Code를 매일 쓰는 사람도 그것을 “덜 알려진 도구”로 여기지 않아 적지 않았을 수 있다.

그러므로 정확한 진술은 “개발자들이 AI를 안 쓴다”가 아니라 “이 커뮤니티의 이 질문 형식에서 AI가
자기 소개 목록에 오르지 않는다”이다.
후자도 충분히 흥미로운 사실이지만 전자와는 다른 사실이다.

### 6년 비교가 같은 사람들의 변화가 아니다

질문 자체가 6년 전과의 비교를 구하고 있고 이 노트의 표도 그 비교를 시도했지만, 두 스레드의 응답자
집합이 같지 않다.

2019년에 149명이 답했고 2026년에 84명이 답했으며, 그 사이에 커뮤니티의 구성이 바뀌었다.
Vim 언급이 절반으로 준 것이 사람들이 Vim을 떠난 결과인지, Vim을 쓰는 사람들이 이 스레드에 덜 답한
결과인지, 아니면 6년 전보다 커뮤니티가 작아진 결과인지 구별할 방법이 없다.

몇몇 답변자는 자기 변화를 직접 보고한다.
`square_usual`은 지난 6년간 macOS와 Neovim이라는 핵심은 그대로였다고 적고[^square_usual],
`hovsater`는 8년째 구성이 거의 그대로라고 하며[^hovsater], `omidmash`는 음악 도구를 빼면 올해도
구성이 그대로라고 한다[^omidmash].
개인 단위로는 변화가 거의 없다는 증언이 여러 개인데, 총계로 보면 큰 변화가 있는 것처럼 보인다.

이 불일치가 실제로 무엇을 뜻하는지가 이 스레드로는 풀리지 않는다.
개인은 잘 안 바꾸는데 총계가 바뀌었다면 그것은 새로 들어온 사람들이 다른 것을 쓴다는 뜻이고, 그렇다면
이 표는 세대 교체의 기록이지 전향의 기록이 아니다.

### 유용한 정보가 형식 때문에 흩어진다

이 스레드의 가치는 목록이 아니라 목록에 딸린 이유에 있다.

`WeetHet`의 OrbStack 선택 이유[^WeetHet], `zie`가 Emacs를 코드 편집기로 쓰기에는 LSP와 구문 강조를
켜면 너무 느리고 끄면 불편해서 주로 EPUB을 Org로 바꿔 읽는 용도로 쓴다고 한 것[^zie],
`curiositry`가 대화형에는 Fish가 확실히 편하고 스크립트는 Bash를 쓰므로 학습 부담이 작았다고 한
것[^curiositry] — 이런 문장들이 실제로 결정에 쓸 수 있는 정보다.

그런데 그런 문장은 84개 답변에 흩어져 있고 대부분의 답변은 이유 없는 나열이다.
질문이 형식을 제시하면서 “왜”를 요구하지 않은 것이 원인이다 — 운영체제, 창 관리자, 터미널, 셸,
에디터, 브라우저를 물었지 각각을 왜 골랐는지는 묻지 않았다.

작은 변경으로 산출물이 크게 달라졌을 것이다.
“지난 6년 사이 바꾼 것 하나와 그 이유”를 물었다면 같은 노력으로 비교 가능한 데이터가 나왔고, 질문자가
원한 “어떻게 바뀌었는가”에 직접 답했을 것이다.
지금 형식은 스냅숏만 만들고 변화는 독자가 두 스레드를 대조해 추론해야 한다.

## 인사이트

### 에이전트 코딩 도구는 매일 쓰는 소프트웨어의 목록이 아니라 그 목록을 지우는 방식으로 들어온다

AI 언급이 적다는 사실을 “아직 안 쓴다”로 읽으면 이 스레드에서 가장 흥미로운 답변 하나를 놓친다.

`square_usual`은 LLM의 도움으로 GUI 편집기에서 좋아하던 검토 기능을 Vim에 재현했고, 그래서 VS Code와
Zed를 제거했다고 적는다[^square_usual].
여기서 LLM은 목록에 추가된 항목이 아니라 목록에서 두 항목을 빼는 데 쓰인 도구다.

이 패턴이 일반적일 수 있다.
에이전트가 하는 일의 상당 부분은 “이 기능을 내 환경에 붙이는 설정을 써 줘”이고, 그 결과물은 dotfile과
플러그인과 스크립트로 남는다.
그러면 사용자가 매일 마주하는 것은 여전히 Vim이며, 목록에 적힐 이름도 Vim이다.

그래서 이런 조사에서 AI의 침투는 체계적으로 과소 계상된다.
목록형 자기 소개는 인터페이스를 세는데, 에이전트는 인터페이스가 아니라 인터페이스를 만드는 층에서
작동하기 때문이다.

여기서 나오는 측정 제안이 있다.
“무엇을 쓰는가”가 아니라 “지난 1년간 직접 만든 설정과 스크립트가 몇 개이고 그중 몇 개를 손으로
썼는가”를 물어야 이 층의 변화가 잡힌다.
그리고 그 숫자가 커지고 있다면 도구 목록이 오히려 짧아지는 방향으로 변화가 나타날 것이다 — 범용
도구 하나를 자기 손에 맞게 깎는 비용이 내려갔으므로, 남이 만든 특화 도구를 쓸 이유가 줄어든다.

### 도구 목록이 짧아지는 것과 길어지는 것이 같은 압력의 두 결과다

이 스레드에는 정반대의 두 무리가 있다.

한쪽은 계속 줄인다.
`r1w1s1`은 KDE에서 시작해 창 관리자를 여럿 거쳐 `cwm`까지, Vim에서 `nvi`까지 내려왔고 작은 도구의
조합을 선호한 결과 특정 창 관리자에 덜 종속되고 작업 흐름이 점차 단순해졌다고 적는다[^r1w1s1].
`beto`는 NetBSD에서 단순함을 유지하려 자기 도구를 Tcl로 다시 쓰고 있다[^beto].
`jeezy`는 컴퓨터 앞에 있는 시간을 줄일수록 설정을 자주 바꾸지 않는 도구만 남는다고 말한다[^jeezy].

다른 한쪽은 계속 늘린다.
`przemoc`의 답변은 편집기만 네 개, 브라우저 세 개에 유틸리티가 스무 개 넘게 나열되며, 실제 메모장은
저장하지 않은 탭 100개가 열린 Notepad++라고 한다[^przemoc].
`chrismorgan`은 Sway 위에 자기 데스크톱 환경을 사실상 새로 지었다[^chrismorgan].

두 방향이 반대처럼 보이지만 동기는 같다 — 자기 환경에 대한 통제권이다.
줄이는 쪽은 통제할 것을 적게 만들어서, 늘리는 쪽은 통제 수단을 많이 만들어서 같은 목표에 도달한다.
`jaredkrinke`가 Windows 10에서 Linux Mint로 옮기고 컴퓨터와 데이터에 대한 통제권을 되찾은 느낌이라고
한 것[^jaredkrinke]과 `tcvsuv`가 LibreWolf를 “AI도 감시도 없어서” 골랐다고 한 것[^oceanhaiyang]이
그 동기를 직접 말한다.

이 관점에서 보면 2019년 대비 변화의 성격도 달라 보인다.
Ubuntu가 사라지고 NixOS가 들어온 것은 편의성의 교체가 아니라 통제 수준의 상향이다 — NixOS는 쉬워서
선택되는 물건이 아니다.
그리고 그 상향의 배경에는 [기본값으로 밀려 들어오는 것들](../ai/notoai.md)에 대한 반작용이 있다.

### 이 목록에서 상업 소프트웨어의 자리가 어디인지가 국가에 따라 다르다

GN 쪽 반응이 이 스레드와 대조를 이룬다.

`xguru`는 Cmux(Ghostty 기반)와 Tmux와 Mux와 Codex, 그리고 VS Code 정도가 전부라고 적는다[^xguru].
`dowha`는 1Password를 가장 잘, 매일 쓰고 있다고 한 줄로 답한다[^dowha].
`loblue`는 nvim과 tmux 조합이며 `zellij`를 다시 테스트해 봐야겠다고, `ripgrep`과 `erdtree` 같은
도구를 잘 쓰고 있다고 적는다[^loblue].
여기까지는 Lobste.rs와 크게 다르지 않다.

`regentag`의 답이 다르다.
한컴오피스 한글이 문서를 작성하는 입장에서 아직 이보다 좋은 것을 못 봤다고 하고, Windows 10을 쓰는
이유가 그 한컴오피스 때문이라고 밝힌다.
그리고 Notepad++는 빠르고 가벼워서 쓰며 웹 기반 UI는 무거워서 싫다고, PowerShell은 윈도에서 쓰기에
가장 좋은 스크립팅 환경이라고 덧붙인다[^regentag].

이 한 답변에 Lobste.rs 스레드 84개 답변 전체에 없는 구조가 들어 있다.
하나의 애플리케이션이 운영체제 선택을 결정하고, 그 애플리케이션은 대체 불가능하며, 대체 불가능한
이유가 기술이 아니라 그 나라의 문서 관행이다.

이것이 “매일 쓰는 소프트웨어”라는 질문에서 가장 자주 빠지는 층이다.
Lobste.rs의 목록은 거의 전부 선택 가능한 것들로 이루어져 있고, 선택 가능하다는 것은 그 사람의 일이
특정 포맷이나 특정 기관의 제출 요건에 묶여 있지 않다는 뜻이다.
그 조건이 성립하지 않는 곳에서는 목록의 맨 위 항목이 취향이 아니라 제약이 되고, 나머지가 그 아래로
정렬된다.

그러므로 이런 조사를 읽을 때 물어야 할 것이 하나 더 있다.
목록에 적힌 것 중 바꿀 수 없는 것이 몇 개인가.
그 수가 0인 사람들의 목록과 1 이상인 사람들의 목록은 같은 종류의 데이터가 아니다.

---

[^rprospero]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_np9axh>
[^liberty]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_zsf2km>
[^asciimoo]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_ohjd7w>
[^beto]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_frz6ln>
[^WeetHet]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_ktei7b>
[^zie]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_92r2z8>
[^dkl]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_pkmjpn>
[^mosburger]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_xzrt05>
[^curiositry]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_dbqzel>
[^hovsater]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_6d91o4>
[^emrox]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_lvswvk>
[^square_usual]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_g6cksr>
[^giffengrabber]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_melnd8>
[^sourcemap]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_9an0ut>
[^oceanhaiyang]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_tcvsuv>
[^r1w1s1]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_p4pidu>
[^chrismorgan]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_std4lx>
[^jeezy]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_l07uc5>
[^rplacx]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_vim4kv>
[^omidmash]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_je4tix>
[^jaredkrinke]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_lvoddm>
[^przemoc]: <https://lobste.rs/s/ttxwdz/what_software_do_you_use_daily_2026#c_yxovar>
[^loblue]: <https://news.hada.io/topic?id=32630#cid63717>
[^dowha]: <https://news.hada.io/topic?id=32630#cid63709>
[^xguru]: <https://news.hada.io/topic?id=32630#cid63708>
[^regentag]: <https://news.hada.io/topic?id=32630#cid63705>
