# CIEL: 라이브러리를 미리 담은 Common Lisp 배포판이자 스크립트 실행기

<https://ciel-lang.org/>

<https://github.com/ciel-lang/CIEL>

HN 토론: <https://news.ycombinator.com/item?id=41401415> (401점, 98개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=35208166> (65점, 12개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/722wop/ciel_is_extended_lisp> (30점, 30개 댓글)

GN 토론: <https://news.hada.io/topic?id=16547>

## 소개

CIEL은 CIEL Is an Extended Lisp의 재귀 약자다.
홈페이지 표지는 100% Common Lisp, batteries included 두 줄로
프로젝트를 설명하고,
문서 첫 문장은 바로 쓸 수 있는 Lisp 라이브러리 모음이라고 정의한다.
새 언어가 아니라는 점은 FAQ가 분명히 한다.
언어의 의미를 다시 정의하지 않는 평범한 Common Lisp이며,
쓸모 있는 라이브러리를 Quicklisp 메타 라이브러리 하나, 코어 이미지 하나,
실행 파일 하나로 묶어 내놓은 것이라고 답한다.
표준 라이브러리라고 부를 수도 없다고 덧붙이는데,
다른 Lisp 사용자도 Quicklisp에서 찾을 수 있는
남의 라이브러리를 골라 담았을 뿐이기 때문이다.

CIEL은 세 가지 형태로 쓴다.

| 형태             | 쓰는 곳                              | 특징                                             |
| ---------------- | ------------------------------------ | ------------------------------------------------ |
| `ciel` 실행 파일 | 터미널, 셸 스크립트                  | 빠른 시작, 라이브러리 내장, 개선된 터미널 REPL   |
| Lisp 라이브러리  | 아무 Common Lisp 구현, 기존 프로젝트 | `(ql:quickload "ciel")`, `(:use :cl :ciel)`      |
| 코어 이미지      | SBCL과 편집기(Emacs와 Slime 등)      | `sbcl --core ciel-core`로 라이브러리를 즉시 적재 |

만든 사람은 vindarel이다.
`ABOUT.org`에 따르면 Python과 JS로 10년쯤 일하다 2017년 무렵 Lisp에 빠졌고,
Common Lisp Cookbook 같은 공동 자료에 기여하며 오픈소스 웹 애플리케이션을
운영하고 있다.
저장소는 2020년 10월에 만들어졌고, 지금은 GitHub 별 419개, 포크 22개다.
`ciel.asd`가 밝히는 버전은 0.3.0, 라이선스는 MIT다.
다만 저장소 루트에 `LICENSE` 파일이 없어서 GitHub는 라이선스를 표시하지 않는다.
상태는 여전히 개발 중이다.
GitHub README는 API가 바뀔 것이지만 쓸 만하다고 적고,
홈페이지 문서는 작업 중이지만 고객 프로젝트에 배포해 썼다고 적는다.

## 만든 이유

### 지루한 일에 바로 쓸 수 있게

문서가 내세우는 첫 목표는 Common Lisp를 오늘날 기준의 평범한 작업에
처음부터 쓸모 있게 만드는 것이다.
JSON과 CSV 처리, 문자열 조작, 정규식, 스레드와 작업 예약,
HTTP와 URI 처리 같은 일이다.
CIEL 없이도 모두 할 수 있지만, 그러려면 Quicklisp를 먼저 설치하고 Lisp 이미지를
시작할 때마다 라이브러리를 불러와야 한다.
CIEL을 시작하면 그것들이 이미 손에 있다는 것이 요점이다.

### 표준의 거슬리는 부분을 무르게

두 번째 목표는 표준 Common Lisp의 거슬리는 부분을 누그러뜨리는 것이다.
대표 사례로 든 것이 해시 테이블 만들기다.
CIEL에서는 Serapeum의 `dict`를 쓴다.

```lisp
CIEL-USER> (dict :a 1 :b 2 :c 3)
;; (dict
;;  :A 1
;;  :B 2
;;  :C 3
;; )
```

표준으로는 `make-hash-table`을 만든 뒤 `setf gethash`를 세 번 해야 하고,
출력도 `#<HASH-TABLE :TEST EQUAL :COUNT 3 {1006CE5613}>`처럼 읽을 수 없는 형태라
같은 일을 했다고 하기도 어렵다고 문서는 꼬집는다.
`dict`의 출력 형태는 CIEL 쪽에서 Serapeum에 풀 리퀘스트를 보내 개선한 것이다.

### 빠진 함수와 문서를 채우기

표준에는 `parse-integer`는 있어도 `parse-float`가 없다.
CIEL은 parse-float와 parse-number를 넣어 이 빈자리를 메운다.
`append`의 파괴적 짝인 `nconc`에는 `nappend`라는 별칭을,
`delete`에는 `nremove`라는 별칭을 붙였다.
내장 함수와 매크로의 docstring도 설명과 예제로 보강한다.
문서는 `loop`에 기본 docstring이 아예 없다는 점을 예로 든다.
이 작업은 별도 저장소 `ciel-lang/more-docstrings`로 이어지고 있다.

FAQ의 숙련자용 답변은 이 동기를 가장 솔직하게 보여 준다.
Lisp를 모르는 친구나 동료에게 CIEL을 보여 주면
rlwrap을 깔라거나, 문자열을 이으려면 `format`의 지시어를 쓰라거나,
`parse-float`는 따로 설치하라거나, 해시 테이블 내용을 보려면 코드 조각을
주겠다는 민망한 말을 하지 않아도 된다는 것이다.

## 설치하기

### 실행 파일 받기

미리 빌드한 실행 파일은 두 곳에서 받는다.
GitHub 릴리스 페이지가 있지만, 최신 0.3은 GitHub 릴리스에 파일을 첨부하지 않고
GitLab CI 파이프라인(`gitlab.com/vindarel/ciel`)의 산출물로
내려받으라고 안내한다.
0.3 릴리스 글이 밝힌 Debian용 압축 파일은 27MB이고,
CIEL은 SBCL 2.5.10으로 빌드되었다.
지원 플랫폼은 Debian과 Void Linux(glibc)뿐이다.
macOS와 Windows용 실행 파일은 없다.
Guix를 쓰면 `sbcl-ciel-repl` 패키지로 설치할 수 있다.

```bash
unzip ciel-0.3.zip
./ciel --help
./ciel            # 인자가 없으면 터미널 REPL
./ciel script.lisp
```

Docker 파일도 있다.
README는 이 Dockerfile이 SBCL 2.3.8을 쓰고 Apple silicon에서 동작한다고 적는다.
macOS 사용자가 실행 파일을 얻는 가장 쉬운 길이 사실상 이쪽이다.

```bash
docker build -t ciel .
docker run --rm -it ciel /usr/local/bin/ciel
docker run --rm -it ciel /usr/local/bin/ciel -s simpleHTTPserver
```

### 라이브러리로 쓰기

CIEL은 Quicklisp에는 없고 Ultralisp에 있다.
저장소를 `~/quicklisp/local-projects/`에 복제하거나
Ultralisp 배포본을 추가한 뒤,
필요한 의존성을 최신으로 맞추는 `make ql-deps`를 반드시 돌려야 한다.
README는 2025년 6월 이후의 Quicklisp 배포본이 필요하다고 적는다.

```lisp
(ql-dist:install-dist "http://dist.ultralisp.org/" :prompt nil)
(ql:quickload "ciel")
(in-package :ciel-user)
```

자기 프로젝트에서는 패키지가 `ciel`을 `use`하게 한다.
`generic-cl`을 바탕으로 `+`나 `equalp`를 자기 객체에 맞게 정의할 수 있는
`generic-ciel`도 있지만, 문서는 덜 검증되었다고 경고한다.

```lisp
(defpackage yourpackage
  (:use :cl :ciel))
```

Guix에는 소스 패키지 `cl-ciel`, SBCL용 `sbcl-ciel`, ECL용 `ecl-ciel`이 있다.

### 코어 이미지와 편집기

Emacs와 Slime 같은 개발 환경을 쓴다면 문서는 실행 파일보다 라이브러리를 권한다.
`(ql:quickload "ciel")`은 라이브러리 수십 개를 불러오느라 느리므로,
`make image`로 `ciel-core` 이미지를 만들어 SBCL을 그 이미지로 띄운다.
코어 이미지는 빌드한 기계에 묶이기 때문에 배포하지 않고 각자 만들어야 한다.

```lisp
(setq slime-lisp-implementations
      `((sbcl ("sbcl" "--dynamic-space-size" "2000"))
        (ciel-sbcl ("sbcl" "--core" "/path/to/ciel/ciel-core"
                    "--eval" "(in-package :ciel-user)"))))
(setq slime-default-lisp 'ciel-sbcl)
```

직접 빌드하려면 Quicklisp, 3.3.4 이상의 ASDF, `make ql-deps`로 받은 의존성,
그리고 `libzstd-dev`(SBCL 2.2.6 이상)나 `zlib1g-dev`, Linux의 `inotify-tools`나
macOS의 `fsevent` 같은 시스템 패키지가 필요하다.
ASDF 버전 조건은 패키지 지역 별칭(local nicknames) 때문인데,
문서는 SBCL 2.2.9에 들어 있는 ASDF가 이 조건을 채우지 못한다고 적는다.
구현은 SBCL에서 주로 개발하고 시험한다.
CCL에서는 컴파일된다는 보고가 있고, ECL, ABCL, Allegro에는 문제가 있으며,
LispWorks는 무료판 제한 때문에 시험하지 못했다고 README가 밝힌다.

## 스크립팅

### 실행과 shebang

CIEL 스크립팅은 SBCL로 만든 실행 파일 하나에 라이브러리를 담아,
스크립트를 빠르게 띄우는 방식이다.
홈페이지 첫 화면의 예제가 이 쓰임새를 보여 준다.

```lisp
#!/usr/bin/env ciel

(-> "https://fakestoreapi.com/products?limit=5"
  http:get
  json:read-json
  (elt 0)
  (access "title"))
```

문서는 이 스크립트를 `time`으로 잰 결과로 전체 0.466초,
사용자 시간 0.10초를 보여 준다.
네트워크 요청이 포함된 수치다.
README는 시작 시간을 약 10ms라고 적는다.
`ciel.asd`의 주석은 SBCL 코어 압축을 켜면 실행 파일이 119MB에서 28MB로 줄지만
시작 시간이 0.02초에서 0.35초로 늘어 체감된다고 설명한다.
이 수치들은 직접 실행해 확인하지 않았다.

shebang이 동작하는 이유는 `ciel`이 파일을 `LOAD`하기 전에 첫 줄을 지우기
때문이다.
일반 SBCL에서는 `#!/bin/sbcl --script`를 써야 하는데,
이것은 `--no-userinit`을 함축해 Quicklisp 같은 도구를 다시 불러오는 의식이 따로
필요하다고 문서는 비교한다.
FAQ는 `exec sbcl --load "$0"`를 `#| |#` 주석 안에 숨기는 고전적인 셸 트릭도
소개하고, 그 방식은 잘 되지만 외부 라이브러리를 쓸 때마다 적재 시간이 든다고
정리한다.

### 인자와 main 함수

스크립트 인자는 `*script-args*`로 받는다.
첫 원소는 스크립트 이름이고, `-s`로 부르든 shebang으로 부르든 같은 목록이 되도록
CIEL이 손질한다.
원래 목록은 `(uiop:command-line-arguments)`로 볼 수 있다.
제대로 된 옵션 해석이 필요하면 함께 들어 있는 Clingon을 쓴다.
짧은 이름과 긴 이름, 자동 도움말, 하위 명령, Bash와 Zsh 자동 완성을 지원한다.

`ciel`이 아는 옵션과 스크립트의 옵션이 겹치면 `ciel`이 먼저 가져간다.
`./simpleHTTPserver.lisp -v -b 4242`에서 `-v`는 `ciel`의 상세 출력 옵션으로
해석되므로, 스크립트에 넘기려면 `--`를 앞에 둔다.

파일을 편집기에서 불러올 때는 실행되지 않고 스크립트로 돌릴 때만
실행되는 진입점은 기능 플래그로 만든다.
CIEL은 스크립트를 돌리기 전에 `*features*`에 `:CIEL`을 넣는다.
Python의 `__name__ == "__main__"`에 해당한다.

```lisp
(in-package :ciel-user)

(defun main ()
  (format! t "Hello ~a!~&" (or (second *script-args*) "lisper")))

#+ciel
(main)
```

한 줄짜리는 `-e`로 평가한다.

```bash
ciel -e '(-> (http:get "https://fakestoreapi.com/products/1") (json:read-json))'
```

### 내장 스크립트

`ciel --scripts`로 목록을 보고 `ciel -s <이름>`으로 부른다.
문서는 이것들이 시연용이며 바뀔 수 있다고 적는다.

| 스크립트                | 하는 일                                                |
| ----------------------- | ------------------------------------------------------ |
| `simpleHTTPserver`      | 현재 디렉터리를 HTTP로 서빙, `static/` 정적 파일 지원  |
| `quicksearch`           | Quicklisp, Cliki, GitHub에서 라이브러리 검색           |
| `apipointer`            | JSON API를 호출하고 JSON 포인터로 값 추출              |
| `install-raw-quicklisp` | Quicklisp를 HTTPS 없이 고전 방식으로 설치              |
| `build`                 | 현재 디렉터리의 `.asd` 프로젝트를 실행 파일로 빌드     |
| `embed`                 | 스크립트 하나를 진입점으로 하는 새 CIEL 실행 파일 생성 |

`build`와 `embed`는 0.3에서 실험 기능으로 들어왔다.
`build`는 `ciel -s build project project::main`처럼
시스템 이름과 진입 함수를 받아
`.asd`를 불러온 뒤 `sb-ext:save-lisp-and-die`를 부른다.
`embed`는 `.asd` 없이 스크립트를 실행 파일로 만들지만,
시스템 정의가 없으므로 CIEL에 들어 있지 않은 라이브러리에는 의존할 수 없다.

```bash
ciel -s embed hello.lisp -o hello
./hello
```

저장소의 `src/scripts/`에는 Hunchentoot와 easy-routes로 만든 웹 앱,
file-notify로 파일 변경을 감시해 다시 불러오는 웹 앱, `ffmpeg`로 음악 파일을
변환하는 스크립트,
`#commonlisp` IRC 로그를 날짜별로 받아 오는 62줄짜리 예제도 있다.
문서는 파일 감시로 다시 불러오는 방식이 Common Lisp의 이미지 기반 개발 기능을
전혀 활용하지 않는다고 경고한다.

스크립트를 REPL에서도 쓰고 싶으면 `~/.cielrc`에서
`ciel::load-without-shebang`으로 불러온다.
이 초기화 파일은 터미널 REPL에서만 읽고, 편집기에서 코어 이미지를 띄울 때는
읽지 않는다.

## 터미널 REPL

인자 없이 `ciel`을 실행하면 sbcli를 바탕으로 만든 REPL이 뜬다.
기본 SBCL REPL에서는 화살표 키조차 동작하지 않는데,
CIEL REPL은 readline 편집과 영구 기록, 여러 줄 입력, 파일과 `PATH` 실행 파일까지
포함하는 TAB 완성을 지원한다.
오류가 나도 디버거와 하위 REPL로 떨어지지 않고 메시지만 보여 준다.

| 기능         | 사용법                                                      |
| ------------ | ----------------------------------------------------------- |
| 셸 통과      | `!ls`, `!htop`, `!sudo emacs -nw /etc/`처럼 대화형 명령까지 |
| 문서 조회    | `%doc dict` 또는 `(dict ?`                                  |
| 편집 후 적재 | `%edit file.lisp`로 `EDITOR`를 열고 닫으면 평가             |
| Lisp 비평    | `%lisp-critic`으로 나쁜 관용구 지적을 켜고 끔               |
| 구문 강조    | pygments를 깔고 `(setf sbcli:*syntax-highlighting* t)`      |
| 기타         | `%w` 세션 저장, `%d` 디스어셈블, `%t` 타입, `%q` 종료       |

셸 통과는 Clesh 라이브러리로 구현되어 터미널 REPL에서만 기본으로 켜진다.
HN에서 리더 매크로가 기본으로 설정되어 있느냐는 질문에 vindarel은
라이브러리로 쓸 때는 읽기 테이블을 건드리지 않으며,
편집기 REPL에서는 `(enable-shell-passthrough)`로 직접 켜야 한다고
답했다[^vindarel-4].
문서도 이 REPL이 좋은 개발 환경을 대신하지 못한다고 여러 번 강조한다.

## 포함된 라이브러리

`ciel.asd`의 `:depends-on`에는 직접 의존 시스템이 65개 있다.
주요 묶음은 다음과 같다.

| 분야            | 라이브러리                                            | 별칭·접두사                  |
| --------------- | ----------------------------------------------------- | ---------------------------- |
| CSV             | cl-csv, data-table, cl-csv-data-tables                | `csv`                        |
| JSON            | shasht, cl-json-pointer                               | `json`, `json-pointer`       |
| YAML            | yamson(읽기 전용)                                     | `yamson`                     |
| HTTP와 HTML     | Dexador, Quri, lquery                                 | `http`, `dex`                |
| 웹 서버         | Hunchentoot, easy-routes, Spinneret                   | `routes`                     |
| 데이터베이스    | cl-dbi, SxQL                                          | `dbi`                        |
| 날짜와 시간     | local-time, periods                                   | `time`                       |
| 동시성과 예약   | Bordeaux-Threads, lparallel, moira/light, cl-cron     | `bt`                         |
| 파일과 OS       | UIOP, file-finder, file-notify, cmd                   | `os`, `filesystem`, `notify` |
| 명령줄          | Clingon                                               | `clingon`                    |
| 문자열과 정규식 | str, cl-ppcre                                         | `str`, `ppcre`               |
| 수치와 그래프   | parse-float, parse-number, vgplot(gnuplot 인터페이스) | `vgplot`                     |
| 보안과 네트워크 | secret-values, cl-ftp                                 | `ftp`                        |
| 개발 도구       | FiveAM, log4cl, printv, repl-utilities, quicksearch   |                              |

JSON 예제에서 보듯 HTTP 응답을 읽은 JSON 객체는 `dict`로 출력된다.
cl-dbi는 데이터베이스 드라이버를 그때그때 설치하므로,
실행 파일을 만들어 다른 기계에서 돌릴 계획이면 `:dbd-sqlite3` 같은 드라이버를
의존성으로 직접 넣어야 한다고 문서는 경고한다.
Numcl처럼 넣지 않은 것도 있고, 문서는 Quicklisp로 하나 불러오면 된다고 안내한다.

GUI는 한때 Tk 기반의 nodgui를 넣었다가 의존성이 무거워 2024년 8월에 뺐다.
문서는 경량판 nodgui-lite가 아직 포함되지 않았다고 적지만,
현재 `ciel.asd`에는 `:nodgui-lite`가 시험 삼아 들어 있다.
같은 정리 과정에서 `osicat`에 기대던 FOF와 Moira를 각각 file-finder와
moira/light로 바꿔 macOS 설치를 쉽게 했다.

## 언어 확장

언어 확장 문서는 표준 CL 코드와 CIEL 코드를 나란히 보여 주는 형식이다.

| 확장                  | 출처                   | 내용                                                             |
| --------------------- | ---------------------- | ---------------------------------------------------------------- |
| 화살표 매크로         | arrow-macros           | `->`, `->>`, `as->`, `some->`, 다이아몬드 완드 `-<>`             |
| 범용 접근             | access                 | `access`, `accesses`로 alist, 해시, 구조체, 객체를 같은 방식으로 |
| 확장 `let`            | metabang-bind          | `bind`로 다중 값, 리스트 구조 분해, `_` 무시                     |
| 패턴 매칭             | Trivia                 | `match`                                                          |
| 짧은 클래스 정의      | defclass-std           | `defclass/std`, `class/std`, `define-print-object/std`           |
| 타입 선언             | Serapeum, defstar      | `-->`, `defun*`                                                  |
| 망라성 검사           | Serapeum               | `ecase-of`, `etypecase-of`로 빠진 경우를 컴파일 경고             |
| 람다 축약             | CIEL                   | `(^ (x) (+ x 10))`                                               |
| 반복                  | trivial-do, for        | `dohash`, `doplist`, `doseq*` 등                                 |
| 메모이제이션          | function-cache         | `defcached`                                                      |
| 패키지                | UIOP                   | `define-package`와 `:reexport`                                   |
| 삼중 따옴표 docstring | pythonic-string-reader | `(ciel:enable-pythonic-string-syntax)`로 켤 때만                 |

설정도 하나 바꾼다.
0.3부터 `*read-default-float-format*`을 `double-float`로 두어 `3.14`를 읽으면
`DOUBLE-FLOAT`가 된다.
표준 CL에서는 `SINGLE-FLOAT`다.

`access`에는 문서가 직접 밝힌 함정이 있다.
키가 심벌이고 그 심벌이 현재 패키지의 함수 이름(`'sort`)이면
`access`가 그 함수를 호출하려 해서 오류가 난다.
`:skip-call? t`를 넘기거나 키를 키워드로 바꿔야 한다.
FAQ는 `access`처럼 더 범용적인 함수는 표준 함수보다 느리며,
`generic-ciel`을 쓰면 더 그렇다고 인정한다.

## 릴리스와 변경 이력

| 버전    | 날짜       | 주요 변화                                                                                     |
| ------- | ---------- | --------------------------------------------------------------------------------------------- |
| v0.2    | 2024-08-30 | 설치 단순화, osicat 의존 제거, nodgui 제거, progressons·cl-ftp·secret-values 추가, `^` 매크로 |
| v0.2.1  | 2024-09-04 | 설치 안내 보강, 터미널 REPL의 파일·`PATH` TAB 완성, 모든 셸 명령의 대화형 실행                |
| 2025    | -          | CSV 라이브러리, `nappend`·`nremove` 별칭, `ffmpeg` 예제, Zsh 완성                             |
| 2026-06 | -          | `build`, `embed`, `install-raw-quicklisp` 스크립트 추가, HTTPS Quicklisp 설치 스크립트 제거   |
| 0.3     | 2026-09-13 | yamson, periods, defclass-std, 기본 double-float, CHANGELOG 신설                              |

0.3은 GitHub에서 프리릴리스로 표시되어 있다.
`CHANGELOG.md`는 0.3의 날짜를 9월 12일로, GitHub 릴리스는 9월 13일로 적는다.
2026년 9월 커밋에서는 Quicklisp 새 배포본이 나와 Makefile에서 직접 복제하던
의존성을 걷어 내고, GitLab CI를 Debian 13 Trixie와 SBCL 2.5.10으로 올렸다.
마지막 커밋은 10월 5일이다.

v0.2를 낸 날 HN 글이 401점을 받았다.
vindarel은 HN 댓글에서 CIEL을 매일 코어 이미지로 편집기에서 쓰고 이것으로 제품을
내보낸다고 말했다.
새 프로젝트를 시작할 때, 외부 세계와 주고받을 때, Python의 번거로움 없이 작은
것을 써서 서버에 올릴 때 시간을 많이 아낀다는 것이다[^vindarel].
2023년 첫 HN 글에서는 아직 거친 부분이 많고 빌드는 Debian 계열만 제공한다고
인정하면서, 초보자에게 쉬운 출발점이자 생태계를 발견하는 경사로가 되기를
바란다고 적었다[^vindarel-2023].

## 트레이드오프

### 확장된 Lisp라는 이름과 배포판이라는 실체

HN의 whartung은 이것을 확장된 Lisp가 아니라 라이브러리를 묶은 배포판으로 본다고
적었다[^whartung].
Java는 원하는 결과를 얻으려면 언어 자체를 바꿔야 했지만,
CL에서는 대부분을 매크로와 함수로 할 수 있으니 핵심은 여전히 CL이고 새로운 것은
없다는 지적이다.
FAQ의 답도 사실상 같다.
이름의 Extended는 표준을 바꾼다는 뜻이 아니라 `ciel-user` 패키지에 들어오는
것이 많다는 뜻에 가깝다.

이 구분은 실무에서 의미가 있다.
CIEL로 배운 코드가 그대로 CL이라는 장점이 있는 반면,
CIEL을 떼어 낼 때는 어떤 심벌이 어느 라이브러리에서 왔는지 알아야 한다.
FAQ는 문서를 읽거나 편집기의 정의로 이동(`M-.`) 기능으로 찾고,
`ciel-user` 대신 `cl-user`를 쓰며, 의존성을 자기 `.asd`에
직접 적으라고 안내한다.
그 작업을 해 주는 스크립트는 언젠가 생길 수도 있다는 정도로만 언급된다.
`->`, `dict`, `match`, `bind`, `access`를 많이 쓴 코드일수록
떼어 내는 비용이 커진다.

### 묶음의 안정성은 가장 불안정한 구성 요소를 따른다

FAQ는 CIEL이 안정적이냐는 질문에 아니라고 답한다.
CIEL은 포함한 라이브러리 묶음만큼만 안정적이라는 것이다.
자체 Quicklisp 배포본을 두거나 상위 라이브러리가 바뀌면 심벌을 다시 정의해
하위 호환을 지키는 방안을 해법으로 들지만 아직 열린 질문으로 남겨 두었다.
Lobste.rs에서 어디까지 CIEL에 넣고 어디부터 애플리케이션이 직접 불러와야
하느냐는 질문에 vindarel은 몇 가지 기준을 밝혔다[^vindarel-lobsters].
난해한 문법 변경을 하지 않고, 읽기 테이블을 기본으로 바꾸지 않고,
외부 C 라이브러리를 조심하고,
의존성 나무를 끌고 오는 라이브러리를 피한다는 것이다.
나아가 기본판과 과학 계산용 큰 판처럼 CIEL 배포판을 나누거나,
의존성을 하나 더해 자기만의 CIEL 기반을 쉽게 다시 빌드하게 하는 방안도 언급했다.

실제 이력이 이 긴장을 보여 준다.
nodgui는 의존성이 무거워 빠졌고, FOF와 Moira는 `osicat` 때문에 교체되었다.
그런데 HN의 medo-bear가 암호화 라이브러리 Ironclad가 왜 없느냐고
물었듯[^medo-bear], 사용자마다 빠졌다고 느끼는 것은 다르다.
배터리를 더 넣을수록 실행 파일과 의존성 위험이 커지고,
덜 넣을수록 결국 Quicklisp를 다시 꺼내야 한다.
BoingBoomTschak은 이런 묶음보다 awesome-cl을 더 정리하고 상호작용적으로 만들어
사용자가 자기 이미지를 직접 꾸리게 하는 편이 낫다고 반박했다[^boingboomtschak].

### 빠른 시작은 이미지 크기와 플랫폼을 대가로 얻는다

CIEL 스크립팅이 빠른 이유는 SBCL 이미지에 라이브러리를 미리 컴파일해 담아 두기
때문이다.
FAQ는 Babashka와 비교하면서,
Babashka가 빠른 시작을 위해 GraalVM Native Image라는 기술적 돌파가 필요했던
것과 달리,
Common Lisp는 원래부터 기계어로 컴파일된 독립 실행 파일을 만들 수 있었으므로
놀랄 일이 아니라고 설명한다.
HN의 beders도 Babashka의 접근이 Common Lisp 세계에도 생겼다고 반겼고[^beders],
aidenn0은 makefile에서 반복해 부르는 아주 짧은 스크립트라면 시작이 느리고
`import`마다 더 느려지는 Python보다 CL 실행 파일이 낫다고 적었다[^aidenn0].

대가는 크기와 플랫폼이다.
압축하지 않은 이미지는 `ciel.asd` 주석 기준으로 119MB이고,
압축하면 28MB로 줄지만 시작 시간이 0.35초로 늘어난다.
배포되는 실행 파일은 Linux용 두 가지뿐이라 macOS 사용자는 Docker나 직접 빌드를
거쳐야 하고, 직접 빌드는 ASDF 버전과 Quicklisp 배포본 날짜를 맞추는 작업부터
시작한다.
2023년 HN에서 dunefox가 설치가 실패한다고 하자 vindarel은 최신 `cl-str`을
`local-projects`에 직접 복제하라고 답했는데[^vindarel-2023-2],
0.2의 핵심이 설치를 쉽게 하는 것이었던 이유가 여기에 있다.

### 스크립트와 프로젝트의 경계

CIEL은 스크립트에 강하지만, vindarel 자신은 주로 여러 파일로 된 프로젝트에 쓴다.
HN에서 그는 기존 DB에서 데이터를 뽑아 CSV로 만들어 SFTP로 보내는 프로젝트를
예로 들었다[^vindarel-2].
`.asd`에서 `:ciel`에 의존하고, 편집기는 CIEL 코어 이미지로 띄우지만,
실행 파일은 평범한 방법으로 빌드하며 의존성을 몇 개 더했다면 스크립트로 돌리지
않는다고 했다.
CIEL은 개발 중에 이득을 주고 배포물은 보통의 CL 프로젝트가 된다는 뜻이다.
그때 그는 `ciel build` 명령을 더하고 싶다고 했고[^vindarel-3],
이것이 2026년 6월에 `-s build`와 `-s embed`로 들어왔다.

그래도 경계는 남는다.
`embed`는 CIEL에 없는 라이브러리를 쓸 수 없으므로,
스크립트가 자라 외부 라이브러리를 하나라도 필요로 하는 순간 `.asd`를 쓰는
프로젝트로 옮겨야 한다.
스크립트의 진입점을 `#+ciel`로 감싸 두는 습관이 이 이동을 쉽게 만든다.

### 생태계의 근본 문제는 건드리지 않는다

Lobste.rs의 Moonchild는 이런 시도가 늘 흐지부지되는 이유가
CL의 실제 문제든 인식된 문제든 하나도 풀지 않기 때문이라고 비판했다[^moonchild].
그가 꼽은 실제 문제는 이식 가능한 동시성과 부동소수점 의미론, 더 나은 컴파일러,
이식 가능한 네이티브 GUI, 좋은 IDE였다[^moonchild-2].
jaredkrinke는 Quicklisp가 원시적이고 안전하지 않다는 점을 가장 큰 불만으로
꼽았다[^jaredkrinke].
CIEL은 이 중 어느 것도 직접 다루지 않는다.
여전히 Quicklisp와 Ultralisp에 기대고, 실행 파일은 SBCL에 묶여 있다.
CIEL이 줄이는 것은 첫날의 마찰이지 언어나 도구 체계의 한계가 아니다.

## 함정

- 홈페이지는 Docsify로 만든 단일 페이지라 JavaScript 없이는 첫 화면 외에 아무것도 보이지 않는다. Lobste.rs의 technomancy는 외부 스크립트를 막으면 스크롤조차 안 된다고 지적했고[^technomancy], HN의 notfed는 모바일에서 사이드바가 왼쪽 아래의 작은 햄버거 메뉴에 숨어 있어 문서를 찾지 못했다고 적었다[^notfed]. 원문 Markdown은 `https://ciel-lang.org/install.md`처럼 직접 받을 수 있다.
- GitHub README는 아직 `ciel -s install-quicklisp`를 안내하지만, `CHANGELOG.md`는 2026년 6월에 이 HTTPS 설치 스크립트를 없앴다고 적는다. 홈페이지 문서의 `install-raw-quicklisp`나 ql-https의 한 줄 설치를 따른다.
- 0.3 실행 파일은 GitHub 릴리스가 아니라 GitLab CI 산출물로 받는다. GitHub 릴리스에 첨부된 `ciel-v2.1.zip`은 0.2.1이다.
- 설치 문서의 플랫폼 표는 Debian Buster를 적지만 0.3의 CI는 Debian 13 Trixie와 SBCL 2.5.10이고, Dockerfile은 SBCL 2.3.8이다. 같은 `ciel`이라도 경로마다 SBCL 버전이 다를 수 있다.
- 0.3부터 실수 기본 형식이 `double-float`다. 같은 코드를 CIEL 밖의 SBCL에서 돌리면 `3.14`가 `single-float`로 읽혀 계산 결과가 달라질 수 있다.
- `access`의 키로 함수 이름과 같은 심벌을 쓰면 그 함수를 호출하려다 오류가 난다. 키워드를 키로 쓴다.
- `filesystem` 별칭은 `uiop/filesystem`을 가리킨다. HN의 aidenn0은 이 패키지에 어떤 함수가 있는지가 버전마다 바뀔 수 있는 구현 세부라고 지적했다[^aidenn0-2].
- 스크립트 옵션이 `-v`처럼 `ciel` 자신의 옵션과 겹치면 `ciel`이 가로챈다. `--` 뒤에 둔다.
- `~/.cielrc`는 터미널 REPL에서만 읽힌다. 편집기에서 코어 이미지로 띄운 Lisp에는 적용되지 않는다.
- cl-dbi로 만든 실행 파일을 다른 기계로 옮기면 드라이버를 즉석 설치하려다 실패한다. `:dbd-sqlite3` 같은 드라이버를 의존성에 넣는다.
- 터미널 REPL의 입력 처리는 일반 SBCL REPL만큼 검증되지 않았다. HN의 the-smug-one은 `#'(lambda ...)`를 넣자 따옴표가 닫히지 않았다는 오류가 났다고 보고했고[^the-smug-one], vindarel은 이후 고쳤다고 답했다. 정밀한 작업은 편집기에서 한다.

## 기억할 원칙

### 배터리를 넣는 일은 큐레이션이고, 큐레이션은 관리 비용이다

CIEL이 만드는 가치는 코드보다 선택에 있다.
수많은 Quicklisp 라이브러리 가운데 JSON에는 shasht, 파일 탐색에는 file-finder,
명령줄에는 Clingon을 고르고, 별칭을 맞추고, 문서에 예제를 붙이는 일이다.
처음 배우는 사람에게 이 선택은 몇 주의 탐색을 대신한다.

그러나 고른 것은 계속 다시 골라야 한다.
osicat 의존을 걷어 내고, nodgui를 빼고, Quicklisp 배포본이 늦으면 Makefile에서
직접 복제하고, 상위 저장소가 갈라지면 포크를 가리키는 일이
모두 한 사람의 몫으로 남는다.
배터리 포함 배포판을 고를 때는 기능 목록보다 이 관리를 누가 얼마나 오래 할 수
있는지를 먼저 보는 편이 맞다.
CIEL처럼 표준 CL 위에 얹힌 묶음이라면 관리가 멈춰도 코드는 살아남는다는 점이
안전판이다.

### 편의 계층은 떼어 낼 수 있어야 한다

CIEL이 언어를 바꾸지 않고 라이브러리와 별칭만 더한 것은
사용자가 언제든 평범한 CL로 돌아갈 수 있게 하는 설계다.
그 장점을 실제로 누리려면 사용하는 쪽에서도 경계를 의식해야 한다.
배포할 코드에서는 `ciel-user`에 기대기보다 자기 패키지에 필요한 라이브러리를
명시하고, 스크립트 진입점은 `#+ciel`로 감싸 두면 CIEL은 개발 도구로 남고
결과물은 CIEL 없이도 돌아간다.

관련 문서로 Clojure에서 실행 파일 배포 때문에 Common Lisp로 옮긴 사례를 다룬
`programming-languages/choosing-common-lisp.md`, CIEL이 바탕으로 삼는 구현과
이미지 기반 실행 파일을 다룬 `programming-languages/sbcl.md`,
REPL 워크플로와 Quicklisp의 한계를 다룬
`programming-languages/learning-lisp-in-2023.md`가 있다.

---

[^vindarel-4]: <https://news.ycombinator.com/item?id=41403061>

[^vindarel]: <https://news.ycombinator.com/item?id=41403280>

[^vindarel-2023]: <https://news.ycombinator.com/item?id=35251886>

[^whartung]: <https://news.ycombinator.com/item?id=41402258>

[^vindarel-lobsters]: <https://lobste.rs/s/722wop/ciel_is_extended_lisp#c_o5kwo4>

[^medo-bear]: <https://news.ycombinator.com/item?id=41403944>

[^boingboomtschak]: <https://news.ycombinator.com/item?id=41403126>

[^beders]: <https://news.ycombinator.com/item?id=41402010>

[^aidenn0]: <https://news.ycombinator.com/item?id=41402758>

[^vindarel-2023-2]: <https://news.ycombinator.com/item?id=35251944>

[^vindarel-2]: <https://news.ycombinator.com/item?id=41407364>

[^vindarel-3]: <https://news.ycombinator.com/item?id=41403950>

[^moonchild]: <https://lobste.rs/s/722wop/ciel_is_extended_lisp#c_0h2zym>

[^moonchild-2]: <https://lobste.rs/s/722wop/ciel_is_extended_lisp#c_blpyxj>

[^jaredkrinke]: <https://lobste.rs/s/722wop/ciel_is_extended_lisp#c_zjxp4c>

[^technomancy]: <https://lobste.rs/s/722wop/ciel_is_extended_lisp#c_fvhlzg>

[^notfed]: <https://news.ycombinator.com/item?id=41403995>

[^aidenn0-2]: <https://news.ycombinator.com/item?id=35249859>

[^the-smug-one]: <https://news.ycombinator.com/item?id=41408692>
