# Hammerspoon

<https://www.hammerspoon.org/>

macOS의 시스템 API와 Lua 스크립팅 엔진을 연결하는 데스크톱 자동화 프레임워크다.
`~/.hammerspoon/init.lua` 파일 하나에 Lua 코드를 작성해 윈도우 관리, 키보드·마우스
이벤트, 오디오, 배터리, 클립보드, WiFi, 위치 서비스 등 macOS의 거의 모든 시스템
기능을 제어할 수 있다.

Mjolnir에서 포크되어, 미니멀 접근 대신 통합된 경험을 제공하는 방향을 택했다.
GitHub 15.2k 스타, v1.1.1(2026년 2월). Objective-C(51%), Lua(25%), C(16%)로 구현됐다.

## 설치

<https://formulae.brew.sh/cask/hammerspoon>

```bash
brew install --cask hammerspoon
```

실행 후 접근성 권한을 부여하고, 메뉴바 아이콘 → Open Config로 `~/.hammerspoon/init.lua`를
편집하면 된다.

## 기본 사용 패턴

### 핫키 바인딩

```lua
hs.hotkey.bind({"cmd", "ctrl"}, "H", function()
  local win = hs.window.focusedWindow()
  local f = win:frame()
  local max = win:screen():frame()
  f.x = max.x
  f.y = max.y
  f.w = max.w / 2
  f.h = max.h
  win:setFrame(f)
end)
```

### 이벤트 기반 자동화

WiFi 연결 변경, USB 기기 연결, 앱 활성화 같은 시스템 이벤트에 반응한다.

```lua
-- 특정 WiFi에 연결되면 볼륨 조정
wifiWatcher = hs.wifi.watcher.new(function()
  local ssid = hs.wifi.currentNetwork()
  if ssid == "Office" then
    hs.audiodevice.defaultOutputDevice():setVolume(30)
  end
end):start()
```

### 설정 자동 재로드

```lua
hs.pathwatcher.new(os.getenv("HOME") .. "/.hammerspoon/", function()
  hs.reload()
end):start()
hs.alert.show("Config loaded")
```

### Spoon 플러그인

사전 구축된 기능 모듈(Spoon)을 설치해 쓸 수 있다.

```lua
hs.loadSpoon("ReloadConfiguration")
spoon.ReloadConfiguration:start()
```

## 주요 모듈

| 모듈                  | 용도                          |
| --------------------- | ----------------------------- |
| `hs.hotkey`           | 전역 단축키 바인딩            |
| `hs.window`           | 창 포커스, 이동, 크기 조절    |
| `hs.layout`           | 다중 창 레이아웃 일괄 적용    |
| `hs.window.filter`    | 조건부 창 관리                |
| `hs.wifi.watcher`     | WiFi 네트워크 변경 감지       |
| `hs.pathwatcher`      | 파일/디렉토리 변경 감지       |
| `hs.application`      | 앱 실행, 전환, 이벤트 수신    |
| `hs.audiodevice`      | 오디오 기기·볼륨 제어         |
| `hs.battery.watcher`  | 배터리 상태 감시              |
| `hs.alert`            | 화면 중앙 일시 알림           |
| `hs.notify`           | macOS 알림 센터 알림          |
| `hs.urlevent`         | URL 스킴 핸들러 등록          |

## 실용적인 활용 예시

- 앱별 윈도우 레이아웃 자동 배치 (모니터 연결 이벤트와 결합)
- 회의 시작 시 Slack 상태 변경 + DND 모드 전환
- 특정 앱 활성화 시 입력 소스(언어) 자동 전환
- CI 빌드 완료·배포 결과를 로컬 알림으로 수신
- 메뉴바 커스텀 상태 표시기 생성

## 주의사항

**변수 생명주기**: Lua 가비지 컬렉션으로 인해 함수 범위를 벗어난 watcher·hotkey 객체는
제거된다. 지속적으로 동작해야 하는 객체는 전역 변수로 할당해야 한다.

**권한 범위**: 접근성 권한과 입력 제어 권한이 넓다. 팀에서 `init.lua`를 공유할 때는
자격증명 접근이나 원격 API 호출 같은 민감한 동작을 분리하고 코드 리뷰를 거쳐야 한다.

## 분석

Hammerspoon이 Raycast, BetterTouchTool 같은 단일 목적 앱과 다른 점은 이벤트 모델과
프로그래밍 방식의 결합이다. AppleScript는 자동화할 수 있지만 이벤트 감지가 약하다.
시스템 환경설정의 단축키는 정적이다. Hammerspoon은 "X가 일어났을 때 Y를 실행"이라는
반응형 자동화를 Lua로 완전히 표현할 수 있다.

설정 파일이 코드라는 점도 중요하다. `init.lua`를 dotfiles 저장소에 넣으면 새 맥에서도
동일 환경이 즉시 재현된다. GUI 기반 자동화 도구가 갖는 이식성 문제를 피할 수 있다.

Lua 문법은 진입 장벽이 낮지만, Hammerspoon API 문서가 방대하고 어떤 모듈이 필요한지
처음엔 파악하기 어렵다. 원하는 동작을 구현하는 데 올바른 이벤트와 API 조합을 찾는
것이 초기 학습의 대부분을 차지한다.

## 비평

`deprecated`로 분류된 macOS API에 의존하는 기능이 일부 있어 업데이트마다 동작이 깨질
수 있다. 651개의 오픈 이슈는 이 부분을 반영한다. 장기적으로 애플이 자동화 API 접근을
더 제한하는 방향으로 가고 있어, Hammerspoon의 일부 기능은 미래 macOS 버전에서 작동이
보장되지 않는다.

그럼에도 macOS 개발자 커뮤니티에서 8년 이상 꾸준히 쓰이고 있다는 점은 대체재가
없다는 뜻이기도 하다. AI 에이전트가 늘어나도 로컬 OS 자동화 계층은 사라지지 않으며,
스크립트형 도구와 에이전트가 결합되는 흐름에서 Hammerspoon의 역할은 오히려 커질 수 있다.

## 인사이트

### 개인 자동화 레이어는 AI 에이전트와 OS 사이의 글루 코드다

AI 에이전트가 고수준 작업을 처리하게 되더라도, 로컬 컨텍스트 전환(앱 포커스,
윈도우 배치, 입력 소스)은 여전히 로컬 스크립트가 가장 빠르고 신뢰할 수 있다.
Hammerspoon 같은 도구는 에이전트의 보조 레이어로서 역할이 오히려 커질 수 있다.

### 설정 파일이 코드가 되면 버전 관리와 공유가 가능해진다

GUI 기반 자동화 도구는 설정을 내보내고 공유하기 어렵다. `init.lua` 하나로 관리되는
Hammerspoon 설정은 dotfiles 저장소에 넣어 어디서든 동일 환경을 재현할 수 있다.
개발 환경 설정의 코드화(Infrastructure as Code의 개인 버전)가 갖는 이점을 그대로 누린다.

### 이벤트 기반 자동화는 "규칙"이 아니라 "반사"다

단순한 단축키 바인딩과 달리 Hammerspoon의 이벤트 모델은 시스템 상태 변화에 즉각
반응한다. 이는 인간의 습관을 코드로 표현하는 것에 가깝다. 특정 환경에 들어오면
자동으로 특정 상태가 되는 것처럼, 개발 환경도 맥락에 맞게 자동 전환되는 방향으로
성숙해가고 있다.
