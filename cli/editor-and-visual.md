# EDITOR와 VISUAL을 설정하기

원문: [Don't Forget to Set VISUAL and EDITOR](https://will-keleher.com/posts/dont-forget-to-set-editor-and-visual/)

## 소개

Will Keleher가 셸 환경 변수 `EDITOR`와 `VISUAL`을 다룬 짧은 글이다.
자신은 vim을 통달했다고 농담으로 시작한다.
입력 모드에 들어가고 나올 줄 알고 파일을 저장할 줄 알며 앞뒤로 검색도 할 수 있다는 것이다.
그렇게 능숙하지만 다른 편집기에서는 더 능숙하고, 그래서 두 변수를 선호하는 편집기로 설정해 두었다고 말한다.

문제 상황은 익숙하다.
`git commit`, `kubectl edit`, `gh pr create`, `crontab -e` 같은 명령이
vim에 익숙하지 않은 사람을 갑자기 그 안에 떨어뜨렸을 때 벌어지는 일이다.
저자 자신이 셸이 자신을 vim으로 던져 넣을 때마다 거의 10년을 헤맸고,
`~/.zshrc`에서 그 동작을 설정할 수 있다는 사실을 알아내는 데 1분이 걸렸다고 적는다.

## 두 변수의 차이

| 변수     | 역할                                               |
| -------- | -------------------------------------------------- |
| `VISUAL` | 대부분의 프로그램이 먼저 시도하는 전체 화면 편집기 |
| `EDITOR` | 그 대비책                                          |

저자는 대부분의 사람이 둘을 같은 값으로 두고 싶어 할 것이라고 본다.
`VISUAL`을 설정하면 `EDITOR`는 굳이 필요 없지만,
행실이 바르지 않은 프로그램이 있을 경우를 대비해 자신은 둘 다 설정한다고 밝힌다.

이 구분은 역사적 유래가 있다.
전체 화면 제어가 불가능한 회선이나 터미널에서도 동작해야 하는 줄 단위 편집기가 `EDITOR`의 자리였고,
커서를 자유롭게 움직일 수 있는 화면 지향 편집기가 `VISUAL`의 자리였다.
지금은 거의 모든 터미널이 후자를 지원하므로 구분이 형식적으로 남아 있을 뿐이다.

## 설정하기

저자가 제시하는 설정은 접속 방식에 따라 값을 나눈다.

```bash
if [[ -n $SSH_CONNECTION ]]; then
    # 원격 서버에는 hx가 없을 수 있으므로 어디에나 있는 vim으로 둔다
    export EDITOR='vim'
else
    # 가벼운 모달 편집기. vim이 동작 뒤 선택이라면 helix는 선택 뒤 동작이다
    export EDITOR='hx'
    export VISUAL='hx'

    # VS Code를 쓴다면 --wait가 필수다. 이것이 없으면 편집기가 즉시 반환되어
    # 호출한 프로그램이 빈 파일을 읽는다
    # export VISUAL='code --wait'
fi
```

`SSH_CONNECTION`으로 분기하는 이유가 실무적으로 중요하다.
원격 서버에는 로컬에 설치해 둔 편집기가 없을 가능성이 높으므로,
그런 환경에서는 어디에나 있는 편집기로 되돌리는 편이 안전하다.

VS Code 계열에서 `--wait`가 필요한 이유도 같은 부류의 함정이다.
`git commit`은 편집기 프로세스가 끝나기를 기다렸다가 파일을 읽는데,
`--wait` 없이 실행하면 GUI 창을 띄운 뒤 명령이 즉시 반환되므로
사용자가 글을 쓰기도 전에 커밋이 진행된다.
맥에서는 명령 팔레트에서 `Shell Command: Install 'code' command in PATH`를 실행해야
`code`를 명령줄에서 쓸 수 있다는 점도 저자가 덧붙인다.

## 셸에서 편집기로 건너뛰기

`EDITOR`는 커밋 메시지를 쓸 때만 쓰이는 것이 아니다.
`fc` 명령과 `CTRL + X` 다음 `CTRL + E`가 그 값을 사용한다.
방금 친 명령이나 지금 입력 중인 줄을 편집기에서 열어 고친 뒤 그대로 실행하는 기능이며,
긴 파이프라인을 손보거나 오타를 고칠 때 셸의 줄 편집보다 훨씬 편하다.

## EDITOR가 어떻게 불리는지 직접 보기

글의 후반부는 `EDITOR`가 실제로 어떻게 호출되는지를 실험으로 보여 준다.
`EDITOR=echo`로도 확인할 수 있지만, 함수를 하나 만들면 더 분명하다.

```bash
function my_editor () {
  local filename="$1"
  cat <<-END_OF_HEREDOC
filename: ${filename}
contents:
$(cat ${filename})

end_of_file_contents

END_OF_HEREDOC

    echo "echo 'I rewrote the file'" > "$filename"
}
```

```text
$ true # this is the command we'll be "editing"
$ EDITOR=my_editor fc
filename: /tmp/zshtpSAfF
contents:
true # this is the command we'll be "editing"

end_of_file_contents

echo 'I rewrote the file'
I rewrote the file
```

여기서 드러나는 계약이 이 글에서 가장 유용한 부분이다.
호출하는 프로그램은 임시 파일을 만들고 그 경로를 첫 인자로 넘긴 뒤,
편집기 프로세스가 끝나기를 기다렸다가 파일을 다시 읽는다.
즉 `EDITOR`는 편집기일 필요가 없다.
파일 경로를 인자로 받아 그 파일을 고치고 종료하는 무엇이든 될 수 있다.

## 편집기 자리에 에이전트를 넣기

저자는 이 계약을 이용해 `EDITOR` 자리에 코딩 에이전트를 넣는다.
2025년의 원시적인 세계에서는 손가락과 뇌로 직접 생각하고 타이핑해야 했다는 농담으로 문단을 연 뒤,
사고와 작성을 모두 외주로 돌리는 설정을 제시한다.

```bash
function my_editor () {
    local filename="$1"
    claude --permission-mode acceptEdits --add-dir /tmp -p "Please look at ${filename} which will have been created by a program like git, fc, kubectl edit, or gh and make appropriate edits to it."
}
```

```text
$ tru && echo "hello, world"
zsh: command not found: tru
$ EDITOR=my_editor fc
Fixed `tru` → `true`.
true && echo "hello, world"
hello, world
```

저자의 논평이 이 대목의 성격을 정한다.
이제 `fc`로 명령 하나를 고치는 데 20초밖에 걸리지 않는다는 것이다.
셸에서 직접 고치면 2초면 될 일이다.

모델이 틀릴 가능성을 고려한 두 번째 버전은 `tmux`로 세션을 띄워
파일 내용과 지시문 앞부분을 미리 입력해 둔 상태로 붙는다.

```bash
function my_editor () {
    local filename="$1"
    local filename_contents="$(cat $filename)"
    echo "$filename_contents"
    local session_name="claude-$(date +%Y%m%d-%H%M%S)"
    tmux new-session -d -s "$session_name" 'claude --permission-mode acceptEdits --add-dir /tmp'
    sleep 1   # TUI가 뜰 때까지 기다린다. 이 상수가 이 방식의 가장 약한 고리다
    tmux send-keys -t "$session_name" "@${filename} has the following contents:"
    tmux send-keys -t "$session_name" C-j
    tmux send-keys -t "$session_name" C-j
    tmux send-keys -t "$session_name" "${filename_contents}"
    tmux send-keys -t "$session_name" C-j
    tmux send-keys -t "$session_name" C-j
    tmux send-keys -t "$session_name" "Please edit @${filename} by "
    tmux attach -t "$session_name"
}
```

저자는 이렇게 설정하면 셸 생산성이 쉽게 열 배가 되니
거액의 연말 보너스와 승진을 받으면 자기를 기억해 달라고 적고,
곧바로 자신은 아직 `VISUAL=hx`로 과거에 살고 있다고 덧붙이며 끝낸다.
후반부 전체가 농담이라는 사실을 마지막 두 문단이 밝힌다.

## 함정

- `--wait`를 빠뜨린 GUI 편집기는 빈 커밋 메시지를 만든다. `git commit`이 편집 없이 통과하면 가장 먼저 이것을 의심한다.
- 원격 서버에 설정 파일을 복사해 두었다면 그 서버에 없는 편집기를 가리키게 되고, `git commit`이 실패한다. `SSH_CONNECTION` 분기가 이것을 막는다.
- `sudo`로 실행하는 명령은 환경 변수를 물려받지 못하는 경우가 많다. `sudo -E` 또는 `sudoedit`가 필요하다.
- `cron`과 systemd 유닛은 로그인 셸을 거치지 않으므로 `~/.zshrc`의 설정이 적용되지 않는다.
- `crontab -e`는 `VISUAL`을 먼저 보는 구현과 `EDITOR`만 보는 구현이 갈린다. 둘 다 설정하라는 저자의 조언이 여기서 값을 한다.

## 비평

### 농담의 형식이 진짜 논점을 흐린다

이 글은 두 부분으로 되어 있다.
앞부분은 `EDITOR`와 `VISUAL`을 설정하라는 실용적 조언이고,
뒷부분은 그 자리에 에이전트를 넣는 풍자다.
그런데 풍자가 분량의 절반을 차지하면서, 정작 그 실험이 드러낸 진짜 발견이 농담에 묻힌다.

그 발견은 `EDITOR`가 인터페이스라는 사실이다.
파일 경로를 인자로 받아 파일을 고치고 종료하는 계약만 지키면 무엇이든 그 자리에 들어갈 수 있다.
저자가 만든 `my_editor` 함수는 이 계약을 처음부터 끝까지 보여 주는 훌륭한 교보재인데,
글은 그것을 에이전트를 끼워 넣기 위한 준비 단계로만 쓴다.

이 계약을 진지하게 활용하는 용도는 여럿 있다.
커밋 메시지 템플릿을 채워 넣는 스크립트, 특정 파일 종류에 따라 다른 편집기를 부르는 디스패처,
편집 전후를 기록해 두는 래퍼가 그렇다.
글은 이 방향을 한 줄도 다루지 않는다.

### 에이전트를 편집기로 쓰는 구성의 위험을 농담 뒤에 숨긴다

풍자라는 형식이 면책이 되지는 않는다.
제시된 코드에는 실제로 복사해 쓸 사람이 다칠 지점이 몇 군데 있다.

`--permission-mode acceptEdits`는 편집을 확인 없이 승인한다.
`EDITOR`로 열리는 파일이 커밋 메시지라면 피해가 작지만,
`kubectl edit`이 여는 것은 살아 있는 클러스터 리소스 정의다.
이 계약에서 편집기가 종료하는 순간 그 내용이 곧바로 적용된다.
저자가 예시에 `kubectl edit`을 넣어 둔 것을 생각하면 이 조합은 가볍지 않다.

`tmux` 버전의 `sleep 1`도 전형적인 취약점이다.
TUI가 1초 안에 뜨지 않으면 입력이 엉뚱한 곳으로 들어가고,
`send-keys`로 파일 내용을 그대로 밀어 넣는 방식은
그 내용에 특수 문자나 개행이 있을 때 예측 불가능하게 동작한다.

글이 마지막에 자기는 `hx`를 쓴다고 밝히는 것으로 균형을 잡으려 하지만,
읽는 사람이 코드 블록만 가져가는 경우를 막지는 못한다.
풍자에 실행 가능한 코드를 붙일 때는 왜 이것을 실제로 쓰면 안 되는지를
농담이 아닌 문장으로 한 번은 적어 두는 편이 낫다.

### 20초라는 숫자가 스스로 논점을 만들고 있는데 발전시키지 않는다

명령 하나를 고치는 데 20초가 걸린다는 서술은 웃기라고 넣은 숫자지만,
그 안에 이 글에서 가장 날카로운 관찰이 들어 있다.
에이전트를 어디에 붙일지는 능력이 아니라 대기 시간과 작업의 길이가 정한다는 것이다.

셸에서 오타를 고치는 일은 2초짜리 작업이므로 20초 도구를 넣으면 열 배 손해다.
반대로 30분짜리 작업이라면 20초 대기는 무시할 만하다.
그러므로 실제 기준은 도구가 얼마나 똑똑한가가 아니라
사람이 직접 했을 때 걸리는 시간이 도구의 왕복 시간보다 긴가이다.

글은 이 기준을 농담의 재료로만 쓰고 명제로 꺼내지 않는다.
꺼냈다면 `EDITOR` 자리에 무엇을 넣을지에 대한 실제 지침이 되었을 것이다.
커밋 메시지 작성처럼 사람이 30초 이상 쓰는 작업에는 유효하고,
오타 수정처럼 2초짜리 작업에는 유효하지 않다.

## 체크리스트

- `VISUAL`과 `EDITOR`를 모두 설정했는가?
- GUI 편집기를 쓴다면 `--wait`에 해당하는 옵션을 붙였는가?
- SSH 접속 시에는 원격에 확실히 존재하는 편집기로 바뀌는가?
- `sudo`와 `cron` 환경에서도 의도한 편집기가 열리는가?
- `git commit`, `crontab -e`, `kubectl edit`으로 각각 한 번씩 확인했는가?

## 기억할 원칙

### 환경 변수 하나가 인터페이스일 때가 있다

`EDITOR`는 설정값처럼 보이지만 실제로는 프로세스 간 계약이다.
파일 경로를 첫 인자로 받고, 그 파일을 수정하고, 종료로 완료를 알린다.
이 계약을 알면 편집기 자리에 스크립트를 넣는 발상이 자연스럽게 나오고,
동시에 `--wait`가 없으면 왜 망가지는지도 설명된다.

같은 구조가 셸 도구 곳곳에 있다.
`PAGER`, `BROWSER`, `GIT_SEQUENCE_EDITOR`가 전부 같은 형태이며,
그중 `GIT_SEQUENCE_EDITOR`는 대화형 리베이스의 편집 단계를 스크립트로 대체할 수 있게 해 준다.
설정값으로만 보면 취향의 문제지만, 계약으로 보면 자동화의 접점이다.

### 도구를 끼워 넣을 자리는 왕복 시간으로 정한다

에이전트를 어디에 붙일지 고민할 때 능력부터 따지기 쉽지만,
실제로 성패를 가르는 것은 사람이 직접 하는 시간과 도구의 왕복 시간 사이의 비율이다.
그 비율이 1보다 작으면 아무리 정확해도 손해이며,
이 글의 20초짜리 오타 수정이 그 사례다.

이 기준은 자동화 전반에 적용된다.
자동화의 값어치를 재는 축은 정확도가 아니라 절약된 시간에서 도입 비용과 대기 시간을 뺀 값이고,
짧고 자주 하는 작업일수록 이 뺄셈에서 지기 쉽다.
