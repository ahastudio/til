# syscall.sh는 커널 소스에서 뽑은 27개 아키텍처의 Linux 시스템 호출 표를 웹과 JSON API로 보여 준다

<https://syscall.sh/>

<https://api.syscall.sh/>

Show HN: [I've updated my Linux System Call website and API](https://news.ycombinator.com/item?id=50334704)

## 소개

syscall.sh는 아키텍처별 Linux 시스템 호출(system call) 표를 한곳에 모은
웹사이트이고,
같은 데이터를 JSON API로도 제공한다.
사이트 소개에 따르면 2020년에 사실상의 시스템 호출 참조 자료로 시작했고,
몇 년간 중단되었다가 2026년에 다시 유지보수되고 있다.
만든이는 소개 페이지에서 TMZ로 적혀 있으며 API 명세에는 guitmz로 나온다.
Show HN 글에서 만든이는 2020년에 처음 공개했고 이번에 아키텍처, 커널 선택기,
시스템 호출 설명, 몇 가지 편의 기능을 더했으며 모바일에서도 더 잘 동작하게
했다고 쓴다.

사이트가 내세우는 범위는 27개 아키텍처와 ABI, Linux 3.3부터 7.3까지의
릴리스이다.
각 시스템 호출의 번호, 인자, 레지스터를 보여 주고,
아키텍처마다 시스템 호출 수와 도입된 커널 버전을 표시한다.
예를 들어 x64(x86_64)는 369개로 3.3부터, x86은 441개로 3.3부터,
arm64는 326개로 3.7부터, riscv64는 327개로 4.15부터 있다고 적는다.
그 밖에 ia32, x32, loongarch64, ppc64, s390x, mips 계열, alpha, m68k, sparc,
xtensa 등이 있다.
각 아키텍처의 표는 언제 나타나고 언제 사라졌는지의 이력과 함께
`/<arch>/syscalls.json` 같은 JSON 파일로도 받을 수 있다.

메인 화면에는 호출 규약(calling convention) 표도 있다.
번호는 NR에, 인자는 ARG0~ARG5에 넣고 명령을 실행하며 결과는 RETURN으로
돌아온다고 설명한다.
x64는 `syscall` 명령에 번호를 `rax`, 인자를 `rdi`, `rsi`, `rdx`, `r10`, `r8`,
`r9`에 놓고,
x86은 `int 0x80`에 `eax`와 `ebx`, `ecx`, `edx`, `esi`, `edi`, `ebp`를 쓰며,
arm64는 `svc #0`에 번호를 `x8`, 인자를 `x0`~`x5`에 놓는다고 표시한다.

### API

API 문서(Scalar 기반)는 OpenAPI 명세 `/openapi.json`에서 만들어진다.
명세는 v2가 현재 API이고 v1은 이전 형식을 유지하지만 폐기 예정이라고 쓴다.
v2 오류는 RFC 9457의 problem details(`application/problem+json`) 형식이다.
엔드포인트는 다음과 같다.

| 경로                               | 설명                                           |
| ---------------------------------- | ---------------------------------------------- |
| `/v2/conventions`                  | 지원 아키텍처의 호출 규약 목록                 |
| `/v2/conventions/{arch}`           | 한 아키텍처의 호출 규약                        |
| `/v2/syscalls/{archNameNumber}`    | 아키텍처, 번호, 이름으로 시스템 호출 목록      |
| `/v2/syscalls/{arch}/{nameNumber}` | 아키텍처와 번호 또는 이름으로 시스템 호출 하나 |
| `/v2/kernels`                      | 스캔한 커널 릴리스 목록                        |
| `/v2/diff/{from}/{to}`             | 두 커널 릴리스 비교                            |

API 페이지는 메타 설명에서 Kconfig 게이팅과 릴리스별 차이도 제공한다고 밝힌다.

## 만들어지는 방식

HN에서 hmokiguess가 어떻게 만들고 얼마나 자주 낡는지 묻자 만든이 guitmz는 다음과 같이 답한다.
오랫동안 낡은 상태였는데, 표를 생성하는 스크립트를 수동으로 돌리고
결과를 API가 쓰도록 SQL로 바꾸고 프런트엔드를 위해 HTML로 변환했기 때문이었다.
지금은 커널 소스에서 JSON 데이터셋을 만들고 API가 그것을 읽어 제공하며,
프런트엔드는 간단한 Go 템플릿으로 매주 cronjob이 API에서 새로
만든다.[^guitmz-build]

## 분석

### 이 사이트의 가치는 커널 소스에서 직접 뽑은 데이터라는 점이다

시스템 호출 번호를 알려 주는 자료는 많지만 낡거나 한 아키텍처에 한정되기 쉽다.
이 사이트는 커널 릴리스마다 소스에서 표를 뽑아 아키텍처와 릴리스 축을 모두
갖췄다.
HN의 ozgrakkurt는 LLM이 틀린 번호나 상수 정의를 준 적이 여러 번 있어서
`echo '#include <sys/syscall.h>' | gcc -E -dM -xc - | grep -i "read"` 같은
명령으로 직접 확인한다고 쓰며,
Chromium 문서의 표가 대안이라고 한다.[^ozgrakkurt]
guitmz는 사이트 내용이 커널 소스에서 직접 나오므로 정확하며 Chromium 페이지는
2020년에 사이트를 만들기 전까지 자신이 쓰던 것인데 많이 낡았을 것이라고
답한다.[^guitmz-chromium]
이는 만든이의 주장이며 이 문서가 몇 개의 값을 커널 소스와 대조해 본 것은 아니다.

### 같은 커널이 아키텍처마다 다른 번호를 갖는 이유는 ABI가 다르기 때문이다

HN의 wg0는 Linux API가 같은데 왜 아키텍처마다 시스템 호출이 다르냐고 묻는다.
guitmz는 커널 API는 어디서나 같지만 시스템 호출 ABI(번호, 호출 규약, 진입
경로)가 아키텍처마다 다르고,
이를 C 라이브러리가 감싸 이식 가능한 POSIX API로 만든다고 답한다.[^guitmz-abi]
사이트가 아키텍처별로 번호와 레지스터 표를 따로 둔 이유가 여기 있다.

## 비평

### 사이트가 잡은 범위 밖의 정보는 직접 확인해야 한다

사이트는 번호, 인자, 레지스터를 보여 주지만 한 시스템 호출의 의미를 깊이
설명하는 곳은 아니다.
ReDress는 `read`와 `readv`, `pread`처럼 비슷한 시스템 호출이 별개로 분류되는
것이 맞느냐고 묻는다.[^ReDress]
PhilipRoman은 각각 미묘한 의미 차이가 많고 분리 여부는 `syscall.tbl`이 정하는
것이지 만든이의 페이지가 아니라고 답하고,[^PhilipRoman]
rustyhancock은 상세 페이지에 같은 아키텍처의 비슷한 시스템 호출 목록이 있으면
좋겠다고 제안한다.[^rustyhancock]
이것은 사이트가 아직 하지 않은 기능으로 남아 있다.

### 호출 규약 표에 오류가 있었다

bkallus는 x86_64와 x32에서 시스템 호출 번호는 `rax`가 아니라 `eax`에 들어가고
`rax`의 상위 32비트는 무시되며 무엇이든 될 수 있다고 지적한다.[^bkallus]
guitmz는 5.14부터(확실하지 않다고 밝히며) 커널이 `eax`만 읽고,
그 전에는 `rax` 전체를 읽어 상위 절반이 0이 아니면 `ENOSYS`를 돌려주었다며 x64와
x32 규약에 메모를 추가하겠다고 답한다.[^guitmz-eax]
이 문서가 읽은 시점의 사이트 표에는 `rax`로 적혀 있었다.
이 문서는 커널 소스에서 이를 직접 확인하지 않았고 위 댓글 둘의 서술로만 전한다.

### 갱신 주기와 보증이 만든이 개인에게 달려 있다

사이트는 몇 년간 중단되었다가 2026년에 다시 유지되며 프런트엔드는 매주 갱신된다.
소개 페이지는 연락처만 있고 서비스 수준이나 변경 이력은 없다.
API가 v1을 폐기 예정으로 두고 있어, 기존 클라이언트는 이전해야 할 수 있다.

## 인사이트

### 시스템 호출을 다루는 사람에게 가장 쓸모 있는 부분은 아키텍처 비교와 커널 간 차이이다

커널 릴리스 간 비교(`/v2/diff/{from}/{to}`)와 호출 규약 표는
다른 아키텍처로 포팅하거나 seccomp 정책을 쓰는 사람이 찾는 정보이다.
이 용도는 사이트 소개가 직접 말한 것이 아니라 이 문서의 제안이다.
번호를 코드에 쓰기 전에는 ozgrakkurt처럼 대상 시스템의 헤더에서 한 번 더
확인하는 방법이 안전하다.

### 이 사이트의 정확성을 확인하는 방법

대상 아키텍처와 커널 버전에서 `gcc -E -dM`으로 얻은 `__NR_*` 값과 사이트 표를 몇
개 비교한다.
값이 모두 같으면 만든이의 주장이 지지되고, 다른 것이 있으면 그 시스템 호출은
사이트를 믿지 않고 커널 소스를 본다.

---

[^guitmz-build]: <https://news.ycombinator.com/item?id=50336821>

[^ozgrakkurt]: <https://news.ycombinator.com/item?id=50337485>

[^guitmz-chromium]: <https://news.ycombinator.com/item?id=50338620>

[^guitmz-abi]: <https://news.ycombinator.com/item?id=50335932>

[^ReDress]: <https://news.ycombinator.com/item?id=50335175>

[^PhilipRoman]: <https://news.ycombinator.com/item?id=50335255>

[^rustyhancock]: <https://news.ycombinator.com/item?id=50335227>

[^bkallus]: <https://news.ycombinator.com/item?id=50335608>

[^guitmz-eax]: <https://news.ycombinator.com/item?id=50335695>
