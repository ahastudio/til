# tmux

터미널 멀티플렉서(Terminal Multiplexer).
하나의 터미널에서 여러 세션을 관리할 수 있다.

<https://github.com/tmux/tmux>

## 설치

```bash
# macOS
brew install tmux

# Ubuntu/Debian
sudo apt install tmux
```

## 기본 사용법

### 핵심 개념

- **세션(Session)**: 작업 단위. 분리(detach)해도 유지된다.
- **윈도우(Window)**: 세션 안의 탭과 같은 개념.
- **페인(Pane)**: 윈도우를 분할한 영역.

### Prefix 키

모든 단축키는 Prefix 키를 먼저 누른 뒤 입력한다.
기본값은 `Ctrl-b`.

### 세션 관리

```bash
# 새 세션 생성
tmux new -s 세션이름

# 세션 목록 확인
tmux ls

# 세션 연결
tmux attach -t 세션이름

# 세션 종료
tmux kill-session -t 세션이름
```

| 단축키          | 설명                |
| --------------- | ------------------- |
| `Prefix` `d`    | 세션 분리 (detach)  |
| `Prefix` `s`    | 세션 목록           |
| `Prefix` `$`    | 세션 이름 변경      |

### 윈도우 관리

| 단축키          | 설명                |
| --------------- | ------------------- |
| `Prefix` `c`    | 새 윈도우 생성      |
| `Prefix` `w`    | 윈도우 목록         |
| `Prefix` `n`    | 다음 윈도우         |
| `Prefix` `p`    | 이전 윈도우         |
| `Prefix` `0~9`  | 번호로 이동         |
| `Prefix` `,`    | 윈도우 이름 변경    |
| `Prefix` `&`    | 윈도우 닫기         |

### 페인 관리

| 단축키              | 설명                |
| ------------------- | ------------------- |
| `Prefix` `%`        | 좌우 분할           |
| `Prefix` `"`        | 상하 분할           |
| `Prefix` `방향키`   | 페인 이동           |
| `Prefix` `z`        | 페인 확대/복원      |
| `Prefix` `x`        | 페인 닫기           |
| `Prefix` `Space`    | 레이아웃 변경       |
| `Prefix` `{`        | 페인 위치 교환 (←)  |
| `Prefix` `}`        | 페인 위치 교환 (→)  |

### 복사 모드

```bash
# 복사 모드 진입
Prefix [

# vi 키바인딩 사용 시
# Space로 선택 시작, Enter로 복사

# 붙여넣기
Prefix ]
```

vi 스타일 키바인딩을 쓰려면 설정 파일에 추가:

```bash
setw -g mode-keys vi
```

### 설정 파일

`~/.tmux.conf`에 설정을 저장한다.

```bash
# Prefix를 Ctrl-a로 변경
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# vi 스타일 키바인딩
setw -g mode-keys vi

# 마우스 지원
set -g mouse on

# 설정 파일 다시 불러오기
bind r source-file ~/.tmux.conf \; display "Reloaded!"
```

설정 변경 후 반영:

```bash
tmux source-file ~/.tmux.conf
```
