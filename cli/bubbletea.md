# Bubble Tea: Elm 아키텍처를 Go로 옮긴 터미널 앱 프레임워크

<https://github.com/charmbracelet/bubbletea>

HN 토론: <https://news.ycombinator.com/item?id=31328205> (308점, 113개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/kbulcu/bubbletea_fun_functional_stateful> (41점, 3개 댓글)

GN 토론: <https://news.hada.io/topic?id=6527>

## 소개

Bubble Tea는 Charm(Charmbracelet, Inc.)이 만드는 Go용 TUI 프레임워크다.
README는 스스로를 The Elm Architecture에 기반해 터미널 앱을 재미있고,
함수형이며, 상태를 가진 방식으로 만드는 Go 프레임워크라고 소개한다.
단순한 앱과 복잡한 앱 모두에 맞고, 화면 일부만 쓰는 인라인 모드, 전체 화면 모드,
둘을 섞은 형태를 다 지원한다는 점을 앞세운다.
감사의 말에는 Evan Czaplicki의 Elm 아키텍처와 TJ Holowaychuk의 go-tea를 토대로
삼았다고 적혀 있다.

저장소는 2020년 1월 10일에 만들어졌고, 2024년 8월에 v1.0.0이,
2026년 2월 24일에 v2.0.0이 나왔다.
이 글을 쓰는 2026년 10월 8일 기준 최신판은 9월 24일의 v2.0.10이며,
v2.0.0 이후 일곱 달 동안 패치가 열 번 나왔다.
v2부터 모듈 경로는 `github.com/charmbracelet/bubbletea`가 아니라
`charm.land/bubbletea/v2`이고, `go.mod`는 Go 1.26 이상을 요구한다.

GitHub API로 확인한 저장소 지표는 다음과 같다.

| 항목                 | 값                                            |
| -------------------- | --------------------------------------------- |
| 스타                 | 45,316                                        |
| 포크                 | 3,292                                         |
| 열린 이슈와 PR       | 238                                           |
| 기여자(익명 포함)    | 167                                           |
| 라이선스             | MIT                                           |
| 토픽                 | cli, elm-architecture, functional, go, tui 등 |
| 의존 앱(README 기준) | 18,000개 이상                                 |
| 의존 앱(v2 블로그)   | 25,000개 이상의 오픈소스 앱                   |

## 동작 방식

### 모델 하나와 메서드 셋

Bubble Tea 프로그램은 상태를 담는 모델과 그 모델의 세 메서드로 이루어진다.
v2의 `tea.Model` 인터페이스는 다음과 같다.

```go
type Model interface {
	Init() Cmd
	Update(Msg) (Model, Cmd)
	View() View
}
```

`Init`은 처음 실행할 명령을 돌려주고, `Update`는 메시지를 받아 새 모델과 다음
명령을 돌려주며, `View`는 현재 모델로 화면을 그린다.
메시지 `Msg`는 아무 타입이나 될 수 있고, 키 입력, 타이머,
서버 응답처럼 어떤 I/O의 결과를 나타낸다.
`Update`에서는 보통 타입 스위치로 메시지 종류를 가른다.

### 부수 효과는 Cmd로만 낸다

명령 튜토리얼은 `Cmd`를 I/O를 수행하고 `Msg`를 돌려주는 함수라고 정의한다.
실제 정의는 `type Cmd func() Msg`이고, 인자가 필요하면 `Cmd`를 돌려주는 함수를
만들면 된다.
튜토리얼은 시간 확인, 타이머, 디스크 읽기, 네트워크 요청이 모두 I/O이므로
명령으로 돌려야 한다고 하고,
가혹하게 들릴 수 있지만 그래야 프로그램이 단순하게 유지된다고 덧붙인다.
명령은 내부에서 고루틴으로 비동기 실행되고,
그 결과 메시지가 다시 `Update`로 들어온다.

`tea.go`의 이벤트 루프를 보면 흐름이 분명하다.
메시지 채널에서 하나를 꺼내 종료, 창 크기, 클립보드 같은 내부 메시지를 먼저
처리하고, `model.Update(msg)`를 부른 뒤,
돌아온 명령을 명령 채널에 넣고, 곧바로 `model.View()`를 렌더러에 넘긴다.
명령 처리기는 받은 명령마다 고루틴을 띄우는데,
소스 주석은 명령을 취소할 방법이 없어서
끝날 때까지 고루틴이 새도록 둔다고 밝힌다.
렌더러의 기본 프레임 수는 60이고 옵션으로 올려도 120에서 막힌다.

### 렌더러가 화면 차이를 계산한다

`View`가 화면 전체를 기술하므로 개발자는 다시 그리기 로직을 신경 쓰지 않는다.
v2는 ncurses 렌더링 알고리즘을 바탕으로 새로 만든 Cursed Renderer를 기본으로
쓴다.
v2 릴리스 노트는 이 렌더러가 속도, 효율, 정확도에 최적화되어 있고,
SSH 앱 프레임워크인 Wish 사용자에게는 대역폭이 자릿수 단위로 줄어든다고
설명한다.
터미널이 지원하면 동기화 출력(mode 2026)으로 화면 찢김과 커서 깜빡임을 줄이고,
mode 2027로 넓은 유니코드 문자와 이모지의 폭을 정확히 계산한다.

## 최소 예제

다음은 3초를 세고 끝나는 카운트다운이다.
`Cmd`로 타이머를 걸고, 틱 메시지를 받을 때마다 다음 틱을 다시 예약하며,
Lip Gloss로 글자에 색을 입힌다.

```go
package main

import (
	"fmt"
	"os"
	"time"

	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"
)

// 상태는 남은 초 하나뿐이다.
type model struct{ left int }

// tickMsg는 Cmd가 1초 뒤에 돌려주는 메시지다.
type tickMsg time.Time

// tick은 I/O(여기서는 시간 대기)를 Cmd로 감싼다.
func tick() tea.Cmd {
	return tea.Tick(time.Second, func(t time.Time) tea.Msg { return tickMsg(t) })
}

func (m model) Init() tea.Cmd { return tick() }

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		if msg.String() == "q" || msg.String() == "ctrl+c" {
			return m, tea.Quit
		}
	case tickMsg:
		m.left--
		if m.left <= 0 {
			return m, tea.Quit
		}
		return m, tick() // 다음 틱을 다시 예약해야 타이머가 이어진다.
	}
	return m, nil
}

var style = lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("#7D56F4"))

func (m model) View() tea.View {
	return tea.NewView(style.Render(fmt.Sprintf("%d초 뒤 종료 (q: 바로 종료)", m.left)) + "\n")
}

func main() {
	if _, err := tea.NewProgram(model{left: 3}).Run(); err != nil {
		fmt.Println("error:", err)
		os.Exit(1)
	}
}
```

```bash
go mod init example.com/countdown
go get charm.land/bubbletea/v2@v2.0.10 charm.land/lipgloss/v2@v2.0.6
go run .
```

이 코드는 Go 1.27.1에서 bubbletea v2.0.10, lipgloss v2.0.6으로 빌드했고,
80x24 크기의 가상 터미널(pty)에서 실행해
3.01초 만에 종료 코드 0으로 끝나는 것을 확인했다.
화면에는 3초, 2초, 1초, 0초 순서로 문구가 바뀌었다.
마지막에 0초가 찍히는 것은 `Update`가 `tea.Quit`을 돌려준 직후에도 루프가
`View`를 한 번 더 그리기 때문이다.
같은 바이너리를 창 크기가 0으로 잡힌 pty에서 돌리면 내용이 하나도 출력되지
않았으므로, 자동화 환경에서 확인할 때는 창 크기를 먼저 지정해야 한다.

## v2에서 바뀐 것

### 명령형 토글에서 선언형 View로

v2의 가장 큰 변화는
`View()`가 문자열 대신 `tea.View` 구조체를 돌려준다는 점이다.
v1에서는 `tea.WithAltScreen()` 같은 프로그램 옵션과 `tea.EnterAltScreen` 같은
명령으로 터미널 기능을 켜고 껐는데,
v2에서는 이 기능들이 모두 `View`의 필드가 되었다.
업그레이드 가이드는 이것을 명령형 명령에서 선언형 View 필드로의 전환이라고
부르고, 제거된 것 대부분이 View 필드로 옮겨 갔을 뿐이라고 정리한다.

| v1                          | v2                                         |
| --------------------------- | ------------------------------------------ |
| `tea.WithAltScreen()`       | `view.AltScreen = true`                    |
| `tea.EnableMouseCellMotion` | `view.MouseMode = tea.MouseModeCellMotion` |
| `tea.HideCursor`            | `view.Cursor = nil`                        |
| `tea.SetWindowTitle("...")` | `view.WindowTitle = "..."`                 |
| `tea.KeyMsg`(누르기)        | `tea.KeyPressMsg`                          |
| `case " ":`                 | `case "space":`                            |
| `tea.Sequentially(...)`     | `tea.Sequence(...)`                        |

`View` 구조체에는 내용 외에도 커서 위치와 모양, 전경색과 배경색, 창 제목,
네이티브 진행 막대, 포커스 보고, 마우스 모드, 키보드 확장 설정이 들어간다.

### 입력과 터미널 질의

키보드는 kitty 키보드 프로토콜 같은 점진적 키보드 확장을 쓴다.
지원하는 터미널에서는 `shift+enter`, `super+space` 같은 조합과 키를 뗀
이벤트까지 받을 수 있고, 지원 여부는 `tea.KeyboardEnhancementsMsg`로 알 수 있다.
릴리스 노트는 Ghostty, Kitty, Alacritty, iTerm2, Foot, WezTerm, Rio,
Contour를 지원 터미널로 든다.
붙여넣기와 마우스도 각각 `tea.PasteMsg`, `tea.MouseClickMsg` 같은
별도 메시지 타입으로 나뉘었다.

OSC52 기반 클립보드로 SSH 너머에서도 복사와 붙여넣기가 되고,
시작할 때 `tea.EnvMsg`로 환경 변수를 넘겨준다.
릴리스 노트는 SSH 앱에서 `os.Getenv`를 부르면 클라이언트가 아니라 서버의 환경이
나온다는 점을 이 기능의 이유로 든다.
커서 위치, 터미널 이름과 버전, terminfo 기능, 모드 지원 여부를 질의하는 명령이
생겼고,
원시 이스케이프 시퀀스를 보내는 `tea.Raw`도 생겼다.
테스트용으로 `tea.WithWindowSize(80, 24)`와 `tea.WithColorProfile`로 창 크기와
색 프로필을 고정할 수 있다.

### Lip Gloss와의 역할 정리

v1 시절에는 Bubble Tea가 키 입력을 읽는 동안 Lip Gloss가 배경색을 알아내려고
터미널에 질의해서 둘이 I/O를 두고 다투는 일이 있었다.
v2에서는 Lip Gloss를 순수 라이브러리로 바꾸고 I/O는 Bubble Tea만 다루게 했다.
색 낮춤(downsampling)은 colorprofile 라이브러리가 맡아,
어디서 온 ANSI 스타일이든 터미널이 지원하는 색 수준으로 자동으로 맞춘다.

## 생태계

Charm의 v2 블로그 글은 세 라이브러리의 역할을 Bubble Tea는 상호작용 계층,
Lip Gloss는 레이아웃 엔진, Bubbles는 UI 기본 부품이라고 나눈다.
같은 글은 v2 브랜치가 처음부터 Charm의 AI 코딩 에이전트 Crush를 돌려 왔다고
밝히며,
실제로 Crush의 `go.mod`는 bubbletea v2.0.9, bubbles v2.2.1, lipgloss v2.0.6을
쓴다.

| 저장소   | 역할                          | 스타   | 최신판               |
| -------- | ----------------------------- | ------ | -------------------- |
| bubbles  | 스피너, 입력창, 표, 목록 부품 | 8,975  | v2.2.1 (2026-08-24)  |
| lipgloss | CSS 같은 스타일과 레이아웃    | 11,904 | v2.0.6 (2026-08-11)  |
| huh      | 폼과 프롬프트                 | 7,197  | v2.0.3 (2026-03-10)  |
| wish     | SSH 앱 서버                   | 5,542  | v2.0.5 (2026-10-01)  |
| gum      | 셸 스크립트용 대화형 도구     | 24,468 | v2.0.2 (2026-09-24)  |
| glow     | 터미널 마크다운 뷰어          | 27,608 | v3.0.0 (2026-08-11)  |
| crush    | AI 코딩 에이전트              | 28,524 | v0.97.1 (2026-09-29) |

Bubbles에는 스피너, 텍스트 입력, 텍스트 영역, 표, 진행 막대, 페이지 넘김,
뷰포트, 목록, 파일 선택기, 타이머, 스톱워치, 도움말, 키 바인딩 부품이 있다.
각 부품은 그 자체로 `Init`, `Update`, `View`를 가진 모델이어서
상위 모델 안에 넣어 쓴다.
Lip Gloss README는 CSS에 익숙한 사람이 편하게 느낄 선언적 방식을 내세우며,
테두리, 여백, 정렬, 표, 목록, 트리 렌더링을 제공한다.
README는 이 밖에 스프링 애니메이션 Harmonica, 마우스 영역 추적 BubbleZone,
차트 라이브러리 ntcharts를 함께 쓰는 라이브러리로 소개한다.

## 사용하는 프로젝트

README가 꼽는 산업 사용처는 Microsoft Azure의 aztfy, Daytona, CockroachDB,
Trufflehog, NVIDIA의 container-canary, AWS의 eks-node-viewer, MinIO의 `mc`,
Ubuntu의 authd다.
개인 프로젝트로는 dotfiles 관리 도구 chezmoi,
터미널 Hacker News 리더 circumflex,
GitHub CLI 확장 gh-dash, 테트리스 Tetrigo, MIDI 시퀀서 Signls,
파일 관리자 Superfile을 직원 추천으로 든다.
Charm 자체 제품으로는 Glow, Huh, Mods, Wishlist가 있다.
이 저장소에서는 `cli/micasa.md`가 다루는 홈 관리 TUI micasa가
Bubble Tea, Lip Gloss, Bubbles 위에 만들어졌다.

## 분석

### Elm 아키텍처가 터미널에서 특히 잘 맞는 이유

브라우저의 Elm은 가상 DOM 비교라는 비싼 장치를 두고서야
화면 전체를 다시 기술하는 모델이 성립한다.
터미널은 사정이 다르다.
화면은 문자 셀의 격자이고, 개별 요소를 제자리에서 고칠 수단이 처음부터 빈약하다.
HN에서 tonyhb는 이 점을 짚어,
메시지는 Redux의 액션처럼 매번 다시 그리기를 일으키며
사실상 즉시 모드 UI라고 설명했다.[^tonyhb]

그래서 Bubble Tea의 핵심 자산은 아키텍처 자체보다 그 아래의 렌더러다.
개발자가 매번 문자열 전체를 돌려줘도
렌더러가 이전 프레임과 비교해 바뀐 셀만 보낸다.
v2에서 렌더러를 ncurses 알고리즘 기반으로 새로 쓴 것은
이 계약의 비용을 프레임워크 쪽에서 떠안겠다는 뜻이다.
Elm 아키텍처는 셀 격자에 가장 자연스러운 프로그래밍 모델이고,
그 대가인 차이 계산은 프레임워크가 낸다는 분업이다.

### 처음부터 인라인과 문자열을 택했다

Lobste.rs의 첫 스레드에서 tview와 무엇이 다르냐는 질문에,
Charm 쪽에서 답한 muesli는 두 가지를 들었다.[^muesli]
tview와 tcell은 전체 화면만 되지만 Bubble Tea는 인라인으로도 동작하며,
그래서 tcell을 비롯한 기존 라이브러리를 배제하고
새로 만들 수밖에 없었다는 것이 하나다.
다른 하나는 tcell API로 화면에 쓰는 대신 문자열을 돌려주면 되므로
표시할 수 있는 것이 더 유연하다는 점이다.

이 두 선택은 지금도 구조 전체를 정한다.
인라인 모드는 셸 스크립트 중간에 끼는 프롬프트와 진행 표시 같은 용도를 열었고,
gum과 huh가 그 위에 섰다.
문자열 반환은 Lip Gloss를 독립 라이브러리로 떼어 낼 수 있게 했다.
반면 위젯 트리와 레이아웃 엔진을 프레임워크가 갖지 않는 설계도
같은 선택에서 나왔다.

### v2는 터미널 상태를 함수의 결과로 만든다

v1의 `tea.EnterAltScreen` 같은 명령은 터미널 상태를 바꾸는 사건이었다.
대체 화면에 들어갔는지, 마우스가 켜졌는지는
지금까지 어떤 명령이 실행되었는지에 달려 있었고,
시작 옵션과 명령이 같은 상태를 두고 겨루는 일이 생겼다.
v2는 이 상태를 `View`의 필드로 옮겨,
터미널 모드도 모델에서 계산되는 값이 되게 했다.

이것은 Elm 아키텍처를 화면 내용에서 터미널 설정 전체로 넓힌 것이다.
Lip Gloss를 순수하게 만들어 I/O를 Bubble Tea 한곳에 모은 결정,
테스트용으로 창 크기와 색 프로필을 고정하는 옵션도 같은 방향이다.
터미널은 상태를 숨긴 기계인데,
v2는 그 상태를 가능한 한 함수 하나의 출력으로 끌어올리려 한다.

## 비평

### Go에서 불변 모델은 관례일 뿐이다

README 튜토리얼의 모델은 값 리시버로 `Update`를 구현하고 새 모델을 돌려준다.
그러나 같은 튜토리얼은 선택 상태를 `selected map[int]struct{}`에 담고
`Update` 안에서 `delete`와 대입으로 바로 고친다.
Go의 값 복사는 얕은 복사이므로 이전 모델과 새 모델은 같은 맵을 공유한다.
결국 튜토리얼의 첫 예제부터
이전 상태와 다음 상태를 나눈다는 Elm의 전제는 지켜지지 않는다.

HN에서 simulate-me는 Go 구조체의 복사 의미 덕분에
Redux보다 상태 반환이 자연스럽다고 칭찬하면서도,
이 방식을 유지하려면 모델에 포인터, 배열, 맵 같은 참조를 두지 말아야 한다고
지적했다.[^simulate-me]
substation13은 Go가 Elm 아키텍처와 끔찍하게 안 맞는다고 하고,
그 이유로 가벼운 람다, 합 타입, 전역 타입 추론, 빠짐없는 패턴 매칭,
기본 불변성을 들었다.[^substation13]
`Msg`가 아무 타입이나 되고 타입 스위치로 가르는 구조에서는
처리하지 않은 메시지를 컴파일러가 알려 주지 않는다.
Bubble Tea가 Go에서 가져온 것은 Elm의 구조이지 Elm의 보증은 아니며,
그 차이는 문서가 말해 주지 않는다.

### 단순한 것을 단순하게 만들지 않는다

Bubble Tea는 위젯 트리, 포커스 관리, 레이아웃을 프레임워크가 정하지 않는다.
leg100은 PUG를 만든 경험을 정리한 글에서,
큰 프로그램은 결국 루트 모델이 메시지를 자식 모델에 나눠 주고
자식의 `View`를 이어 붙이는 모델 트리가 된다고 썼다.
그 라우팅 규칙과 레이아웃 계산은 모두 앱 작성자의 몫이다.
Lobste.rs에서 hobbified는 PUG의 `internal/tui` 패키지가 약 5,400줄로
전체 코드의 거의 절반이라고 짚고,
렌더링 시스템이 개념은 멋지지만 사용자에게 엄청난 양의 일을 넘긴다고
평했다.[^hobbified]

HN에서도 같은 불만이 나왔다.
georgemcbay는 간단한 목록 화면과 파일 선택기가 필요했을 뿐인데
Bubble Tea의 아키텍처를 깊이 이해해야 해서
30분 만에 접고 tview로 옮겼다고 했다.[^georgemcbay]
GeertJohan은 레이아웃이 프레임워크에 없고 서드파티 위젯의 완성도에 기대야 해서,
작성자마다 위젯을 다른 방식으로 만든다고 비판했다.[^GeertJohan]
반대로 wonger_는 Elm 웹앱이 하위 모델로 상태를 쪼갤 때 골치가 아파지는 것처럼
TUI도 그렇다며, 차라리 필드가 100개인 평평한 모델이 낫다고 했다.[^wonger_]
어느 쪽이 맞든, 규모가 커질 때의 구조를 프레임워크가 답하지 않는다는 점은 같다.

### 선언형이라는 말이 닿지 않는 곳

v2의 선언형 `View`는 터미널 모드에는 잘 들어맞지만, 비동기 작업에는 닿지 않는다.
명령은 고루틴에서 실행되고 취소할 수 없으며,
소스 주석 스스로 끝날 때까지 고루틴을 새게 둔다고 적는다.
여러 명령의 결과 메시지가 도착하는 순서도 정해져 있지 않아서,
leg100은 순서가 중요하면 `tea.Sequence`를 쓰거나
순서에 기대지 않도록 프로그램을 고치라고 권한다.
화면은 모델의 함수이지만,
모델로 들어오는 메시지의 흐름은 여전히 명령형 동시성의 세계에 있다.

이벤트 루프는 메시지 하나마다 `Update`와 `View`를 차례로 부른다.
렌더러가 프레임 수를 60으로 묶어도 `View` 계산 자체는 메시지 수만큼 일어난다.
leg100의 첫 번째 조언이 이벤트 루프를 빠르게 유지하라는 것인 이유가 여기에 있고,
무거운 문자열 조합을 `View`에 두면 키 입력이 밀린다.

### 숫자와 약속이 문서마다 다르다

README는 Bubble Tea로 만든 앱이 18,000개가 넘는다고 하고,
같은 시기의 v2 블로그 글은
생태계가 25,000개가 넘는 오픈소스 앱을 지탱한다고 한다.
후자는 Bubble Tea만이 아니라 생태계 전체를 센 것일 수 있지만,
문서가 기준을 밝히지 않으니 어느 숫자도 그대로 인용하기 어렵다.

블로그 글은 프로젝트 역사 내내
호환성을 깨는 변경을 한 번도 내지 않았다고 쓰지만,
그 글이 소개하는 v2가 바로 모듈 경로, `View` 시그니처, 키와 마우스 메시지,
프로그램 옵션을 한꺼번에 바꾼 릴리스다.
Lobste.rs에서 carlana는 같은 v2 경로로 도메인만 바꾸면
업그레이드 때 이상한 오류가 날 것이라 우려했는데,[^carlana]
Charm의 andreynering이 이전 경로에는 `/v2`가 없었고
공지 예시가 잘못된 것이라고 답했다.[^andreynering]
문제는 오해로 끝났고 공지도 곧 고쳐졌지만,
메이저 버전과 도메인을 동시에 바꾼 경로 이전이
쓰는 쪽은 물론 만든 쪽에게도 헷갈렸다는 흔적으로 읽힌다(해석).

## 인사이트

### 렌더러 성능이 비용 문제가 되는 곳은 SSH다

v2 블로그 글은 렌더링 효율 향상이 로컬 앱에는 의미가 있고,
SSH로 도는 앱에는 금전적으로 셀 수 있는 변화라고 쓴다.
이 문장은 Bubble Tea가 어디서 돈과 맞닿는지를 보여 준다.
HN에서 eieio는 SSH로 여러 사람이 함께 하는 스네이크 게임을 돌리려고
Bubble Tea 렌더러를 직접 포크해 대역폭을 10분의 1로 줄였다고 했다.[^eieio]
그는 새 렌더러가 범용이라 그만큼은 아니어도 비슷할 것이고,
색과 스타일을 많이 쓰는 앱일수록 이스케이프 시퀀스가 길어 효과가 크리라고 봤다.

화면 차이를 얼마나 줄이느냐는 로컬에서는 체감 속도의 문제지만,
서버 하나에 수많은 SSH 세션이 붙는 순간 전송량과 서버 비용의 문제가 된다.
Wish로 SSH 앱을 만드는 쪽에서 보면
Cursed Renderer는 미관 개선이 아니라 운영비 절감이다.
반대로 djfergus처럼 느린 회선 너머 서버에서 일하는 사람은
화려함보다 어디서든 낮은 지연으로 동작하는 TUI를 원한다고 했는데,[^djfergus]
같은 렌더러 최적화가 이 요구에도 답한다.
렌더러 최적화가 브랜딩과 정반대 쪽의 사용자에게도 쓸모 있다는 점은
v2가 가장 덜 강조한 장점이다.

### AI 에이전트가 프레임워크의 우선순위를 정하기 시작했다

블로그 글은 v2를 만든 이유로
AI 에이전트가 터미널로 들어왔고 터미널이 주요 플랫폼이 되었다는 점을 든다.
v2 브랜치가 처음부터 Crush를 돌려 왔다는 사실을 합치면,
이 메이저 버전의 요구 사항은 상당 부분 에이전트 UI에서 나왔다고 읽힌다(해석).
선언형 커서, 키를 뗀 이벤트, `shift+enter`, 클립보드, 동기화 출력은
모두 긴 입력창과 스트리밍 출력을 가진 채팅형 화면에 필요한 기능이다.
HN에서 abrinz는 코딩 에이전트를 만들면서
마우스 휠 스크롤과 텍스트 선택 복사를 동시에 지원하지 못하는 것이
가장 큰 걸림돌이라고 했다.[^abrinz]

그런데 에이전트가 쓰는 쪽으로 보면 방향이 반대다.
TheDong은 에이전트가 TUI는 잘 다루지 못하고 CLI는 잘 다룬다며,
에이전트 때문에 TUI가 CLI에 밀릴 수도 있다고 했다.[^TheDong]
에이전트를 담는 UI로서 TUI는 커지지만,
에이전트가 조작하는 도구로서 TUI는 불리하다.
lilyball이 TUI는 접근성 API에 객체를 드러낼 방법이 없으니
모든 TUI에 선택적 CLI 모드가 있어야 한다고 한 지적은,[^lilyball]
사람 대신 에이전트가 화면을 읽는 시대에 같은 이유로 다시 유효해진다.
접근성 문제는 이 저장소의 `cli/tui-accessibility-lie.md`가 더 자세히 다룬다.

### 수출되는 것은 라이브러리가 아니라 설계다

Charm 도구는 Go에 묶여 있다는 불만이 꾸준하다.
2022년 HN에서 nepeckman은 다른 언어 바인딩이 있었으면 한다고 했고,[^nepeckman]
2026년 Lobste.rs에서 gcupc는
요즘 TUI 라이브러리가 모두 언어에 갇혀 있다고 했다.[^gcupc]

그사이 일어난 일은 바인딩이 아니라 재구현이다.
2025년 8월부터 2026년 2월 사이 HN에는 Rust 구현 bubbletea-rs,
Charm에서 영감을 받은 Common Lisp 라이브러리 cl-tuition, Ruby용 Charm Ruby,
Bubble Tea에서 영감을 받은 Zig 프레임워크 ZigZag가 차례로 올라왔다.
Bubble Tea의 표면적인 API는 작고,
핵심은 모델과 메시지와 세 함수라는 약속이므로 다른 언어로 옮기기 쉽다.
어려운 부분인 렌더러, 키보드 프로토콜, 터미널 질의는
언어마다 다시 만들어야 하지만, 개발자가 배우는 사고방식은 그대로 따라간다.

이것은 1990년대 Borland Turbo Vision과 대비된다.
HN에서 roryirvine은 Bubble Tea가 새 Turbo Vision이냐는 물음에
대체로 그렇다고 답하며,
90년대 TUI가 좋은 곳까지 갔다가 curses의 보편화로 오래 정체했다고
회고했다.[^roryirvine]
Turbo Vision은 위젯 시스템, 이벤트 루프, 레이아웃 관리를 한 덩어리로 제공했고
(이 저장소의 `cli/turbo-vision.md` 참고),
그 덩어리는 구현 언어와 함께 묶여 있었다.
Bubble Tea는 위젯을 거의 팔지 않고 상태 전이의 모양을 팔기 때문에,
위에서 본 레이아웃 부재라는 약점이 거꾸로 이식성이라는 강점이 된다.

---

[^tonyhb]: <https://news.ycombinator.com/item?id=31329643>

[^muesli]: <https://lobste.rs/s/kbulcu/bubbletea_fun_functional_stateful#c_ko8mil>

[^simulate-me]: <https://news.ycombinator.com/item?id=31329442>

[^substation13]: <https://news.ycombinator.com/item?id=31339284>

[^hobbified]: <https://lobste.rs/s/kgjvpb/golang_bubble_tea_gui_drive_terraform_at#c_iduyym>

[^georgemcbay]: <https://news.ycombinator.com/item?id=41413451>

[^GeertJohan]: <https://news.ycombinator.com/item?id=41411632>

[^wonger_]: <https://news.ycombinator.com/item?id=41411349>

[^carlana]: <https://lobste.rs/s/1to8sq/charm_v2_major_releases_for_bubble_tea_lip#c_vmqxjp>

[^andreynering]: <https://lobste.rs/s/1to8sq/charm_v2_major_releases_for_bubble_tea_lip#c_nehi72>

[^eieio]: <https://news.ycombinator.com/item?id=47270469>

[^djfergus]: <https://news.ycombinator.com/item?id=47269784>

[^abrinz]: <https://news.ycombinator.com/item?id=47269609>

[^TheDong]: <https://news.ycombinator.com/item?id=47270826>

[^lilyball]: <https://news.ycombinator.com/item?id=31336119>

[^nepeckman]: <https://news.ycombinator.com/item?id=31331168>

[^gcupc]: <https://lobste.rs/s/1to8sq/charm_v2_major_releases_for_bubble_tea_lip#c_6unoyq>

[^roryirvine]: <https://news.ycombinator.com/item?id=47273033>
