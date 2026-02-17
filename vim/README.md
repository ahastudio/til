# Vim

- <https://www.vim.org/>
- <https://github.com/vim/vim>

## Vim 9.2

- <https://www.vim.org/vim-9.2-released.php>

2026년 2월 15일, Vim 9.1 이후 약 2년 만에 Vim 9.2가 릴리스되었다.

### 자동 완성이 플러그인 없이도 쓸 만해졌다

Insert 모드 자동 완성에 퍼지 매칭(fuzzy matching)이 추가되었다. 기존에는 정확한
접두사 일치만 지원해서 fzf 같은 플러그인에 의존했지만, 이제 내장 완성만으로도
유연하게 동작한다.

`CTRL-X CTRL-R`로 레지스터에서 단어를 완성하는 기능도 추가되었다. 복사해 둔
텍스트를 바로 활용할 수 있어 편집 흐름이 끊기지 않는다.

`completeopt`에 `nosort`, `nearest` 플래그가 추가되어 완성 결과의 정렬과 표시
방식도 세밀하게 제어할 수 있다.

### vimdiff가 드디어 쓸 만해졌다

기본 `diffopt`에 `inline:char`가 포함되어 줄 내부의 문자 단위 차이를 강조
표시한다. 이전에는 줄 단위로만 차이를 보여줬기 때문에 실제 변경 지점을 찾기
어려웠다.

linematch 알고리즘이 추가되어 버퍼 간 변경사항을 유사한 줄 기준으로 더 정확하게
정렬한다. `diffanchors` 옵션으로 독립적인 diff 섹션의 앵커 포인트를 지정할 수도
있다.

### 설정 파일이 홈 디렉터리에서 빠졌다

XDG Base Directory 지원이 추가되어 기본 설정 경로가 `~/.config/vim`이 되었다.
`~/.vim`도 하위 호환성을 위해 계속 지원된다. 홈 디렉터리의 dotfile 정리에 신경
쓰는 사용자라면 반가운 변화다.

### GUI Vim 사용자를 위한 변경

Wayland 환경에서의 UI와 클립보드 처리가 추가되었다. 아직 실험적 단계다. HiDPI
디스플레이를 자동 감지해 폰트 렌더링을 조정한다. Windows GUI에는 네이티브 다크
모드가 들어갔다. 터미널 Vim 사용자에게는 해당 없다.

### 플러그인 개발자를 위한 변경

Vim9 스크립팅에 Enum, 제네릭 함수, Tuple 타입이 추가되었고 클래스의 protected
`_new()` 메서드, 내장 함수의 객체 메서드 통합, `:defcompile` 전체 메서드
컴파일을 지원한다.

### 그 외

- 수직 탭 패널(vertical tab panel) 추가
- 내장 대화형 튜터 플러그인 추가
- 시작 시간 단축 및 메모리 관리 최적화

## Learn VIM while playing a game

VIM Adventures <https://vim-adventures.com/>
