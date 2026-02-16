# Vim

- <https://www.vim.org/>
- <https://github.com/vim/vim>

## Vim 9.2

- <https://www.vim.org/vim-9.2-released.php>

2026년 2월 15일, Vim 9.1 이후 약 2년 만에
Vim 9.2가 릴리스되었다.

### Wayland 지원 (실험적)

Wayland 환경에서의 UI와 클립보드 처리를
완전히 지원한다.
아직 실험적(experimental) 단계이지만
기본적인 기능은 안정적으로 동작한다.

### XDG Base Directory 지원

사용자 설정 파일의 기본 경로가
`~/.config/vim`으로 변경되었다.
기존 `~/.vim` 경로도 하위 호환성을 위해
계속 지원된다.

### 자동 완성 개선

Insert 모드의 자동 완성에
퍼지 매칭(fuzzy matching)이 추가되었다.
`CTRL-X CTRL-R`로 레지스터의 단어를
완성할 수 있다.
`completeopt`에 `nosort`, `nearest` 등의
플래그가 추가되었다.

### Diff 모드 개선

linematch 알고리즘으로 버퍼 간 변경사항을
유사한 줄 기준으로 정렬한다.
`diffanchors` 옵션으로 독립적인 diff 섹션의
앵커 포인트를 지정할 수 있다.
기본 `diffopt`에 `inline:char`가 포함되어
줄 내부의 문자 단위 차이를 강조 표시한다.

### Vim9 스크립팅 개선

- Enum, 제네릭 함수, Tuple 타입 지원
- 클래스의 `_new()` protected 메서드 지원
- 내장 함수를 객체 메서드로 통합
- `:defcompile`로 전체 메서드 컴파일

### 기타 변경사항

- 수직 탭 패널(vertical tab panel) 추가
- Windows GUI 네이티브 다크 모드 지원
- 내장 대화형 튜터(interactive tutor)
  플러그인 추가
- HiDPI 디스플레이 자동 감지 및
  폰트 렌더링 개선
- 기본 히스토리 설정 증가 등 기본값 조정
- 시작 시간 단축 및 메모리 관리 최적화

## Learn VIM while playing a game

VIM Adventures <https://vim-adventures.com/>
