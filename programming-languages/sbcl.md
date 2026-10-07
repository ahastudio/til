# SBCL: CMU CL에서 갈라져 나와 매달 릴리스되는 고성능 Common Lisp 컴파일러

<https://www.sbcl.org/>

<https://sourceforge.net/p/sbcl/sbcl/>

HN 토론: <https://news.ycombinator.com/item?id=49086971> (277점, 169개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=36544573> (262점, 167개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=47140657> (291점, 107개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/hk8yw5/steel_bank_common_lisp_2_5_9> (45점, 6개 댓글)

## 소개

Steel Bank Common Lisp(SBCL)는 홈페이지가 스스로를 고성능 Common Lisp
컴파일러라고 소개하는 오픈소스 프로젝트다.
ANSI Common Lisp용 컴파일러와 런타임 시스템에 더해 디버거, 통계 프로파일러,
코드 커버리지 도구 등을 갖춘 대화형 환경을 함께 제공한다.
홈페이지 기준 지원 운영체제는 Linux, 여러 BSD, macOS, Solaris, Windows다.
이 글을 쓰는 2026년 10월 7일 현재 최신 버전은 2026년 9월 26일에 나온 2.6.9다.

매뉴얼은 SBCL을 ANSI 표준을 대부분 따르는 구현(mostly-conforming
implementation)이라고 부르며,
표준을 어기는 동작은 거의 전부 버그로 취급한다고 밝힌다.
예외는 표준 자체가 앞뒤가 맞지 않는 곳이다.
예를 들어 `prog2`는 명세의 설명 부분이 아니라 인자와 값 부분을 따라
두 번째 폼의 값을 돌려준다.

공식 개발 조직은 없다.
매뉴얼의 상용 지원 절에는 유료 지원 업체 목록을 싣는 자리가 있지만,
현재는 광고를 원한 회사나 컨설턴트가 없다고 적혀 있다.
지원 창구는 `sbcl-help` 메일링 리스트이고,
버그는 Launchpad 버그 데이터베이스나 `sbcl-bugs` 메일링 리스트로 받는다.

이 저장소의 `programming-languages/choosing-common-lisp.md`는 Clojure를 떠나
Common Lisp를 고른 개발자가 실행 파일, 세 운영체제 지원,
런타임 속도 같은 요구 사항을 SBCL로 채운 사례를 다룬다.
이 문서는 그 선택의 대상이 된 구현 자체를 정리한다.
나는 SBCL을 직접 설치하거나 실행하지 않았고, 아래 명령과 수치는 공식 사이트,
매뉴얼, 저장소 문서에서 확인한 것이다.

HN에서 reikonomusha는 업데이트가 꾸준하고 소프트웨어가 안정적이라는 점을 좋아한다고 하면서, 진짜 강점은 다른 데 있다고 적었다.[^reikonomusha]
컴파일러와 표준 라이브러리가 Common Lisp로 작성되어 있어서 `DEFTRANSFORM`,
`DEFINE-VOP` 같은 SBCL 내부 도구를 자기 프로젝트에서 라이브러리처럼 쓸 수 있고,
사실상 컴파일러를 사용자 공간에서 확장할 수 있다는 것이다.
그는 지원되지 않는 API를 쓰는 것은 권하지 않는다는 단서도 달았다.
상용 구현인 Allegro CL과 LispWorks도 써 봤다는 jwr는 SBCL이 견고하고,
오픈소스이고, 디버깅할 수 있으며, 활발히 개발된다고 평가했다.[^jwr]

## 역사와 이름

History and Copyright 페이지에 따르면 SBCL은 코드 대부분을 Carnegie Mellon
대학에서 만든 CMU CL에서 가져왔다.
1999년 12월에 CMUCL 본류에서 갈라져 나왔고, 특히 부트스트래핑을 크게 바꿨다.
반면 Lisp 추상을 하드웨어에 대응시키는 방식, 컴파일러의 기본 구조,
런타임 지원 코드의 상당 부분은 조금만 바뀌었다.
인터페이스와 구조가 충분히 달라졌기 때문에 같은 이름을 쓰면 혼란스럽다고
판단했고, 이름은 Andrew Carnegie가 돈을 번 철강(steel)과 Andrew Mellon이 돈을 번
은행(bank)에서 따왔다.

사이트가 꼽는 CMUCL과의 차이는 유지보수성이다.
컴파일된 SBCL은 소스 코드와 통제되고 검증 가능한 방식으로 대응하고,
OpenMCL 같은 관련 없는 구현에서도 누구나 일상적으로 빌드할 수 있다.
바이트 컴파일러와 인터프리터처럼 특수한 경우를 많이 만들던 CMU CL 확장을 걷어
냈고, 잘라 붙여 재사용한 복잡한 코드도 찾아서 정리했다.
같은 페이지는 기능 차이의 예로 SBCL은 Linux/x86에서 네이티브 스레드를,
CMUCL은 사용자 공간 스레드를 쓴다고 적는다.
이 페이지는 오래전에 쓰인 문장을 그대로 두고 있어서,
스레드 지원 범위는 아래 매뉴얼 절이 더 최신이다.

매뉴얼의 역사 절은 계보를 더 거슬러 올라간다.
SBCL은 CMUCL에서, CMUCL은 1980년대 IBM RT의 Mach 운영체제용 구현을 포함한
Spice Lisp에서 나왔다.
그때의 설계가 지금도 남아 있는데, 가상 메모리의 고정된 위치에 적재되기를
기대하는 점, 시스템에서 주소 공간을 넉넉하게 예약해 두는 오버커밋,
C 프로그램이 저수준 서비스를 맡고 Lisp `.core` 파일을 적재하는 구조가 그렇다.
SBCL의 직접 조상은 CMUCL의 x86 이식판인데,
매뉴얼은 이것이 레지스터가 적은 x86을 지원하느라 가장 누더기처럼 이어 붙인
이식판이었다고 설명한다.
x86에서는 지금도 보수적(conservative) GC를 쓴다.

갈라진 계기는 부트스트랩 과정의 대대적인 재작성이었다.
매뉴얼에 따르면 CMUCL은 시스템을 처음부터 빌드하지 않고 실행 중인 시스템의
일부를 새 버전으로 차례로 덮어쓰는 특이한 빌드 방식을 오래 써 왔다.
그래서 큰 변경이 들어가면 부트스트랩이 꼬이기 쉬웠고,
현재 소스에 없는 특성이 담긴 실행 파일이 우연히 만들어지기도 했다.
분기 이후 SBCL은 IP 네트워킹, RPC, Unix 시스템 인터페이스,
X11 인터페이스 같은 CMUCL 확장을 코어에서 빼서 기여 모듈이나 서드파티 모듈로
돌렸다.
컴파일러 내부의 메모리 풀링도 없앴는데, 매뉴얼은 그 결과 컴파일러가 더
단순해졌지만 쓰레기를 더 만들고 더 느려졌다고 솔직하게 적는다.

HN의 p_l은 공식 설명 외에 SB가 “Sanely Bootstrappable”의 약자이기도 하다는 두 번째 유래가 있다고 주장했다.[^p_l]
그의 설명으로는 CMU CL은 사실상 자기 자신,
그것도 가급적 같은 버전으로만 컴파일할 수 있었지만,
SBCL은 완전하지 않더라도 대부분을 갖춘 ANSI CL 구현이면 무엇이든 호스트로 삼아
빌드할 수 있게 다시 짰다.
이 약자 해석은 sbcl.org에서 확인되지 않으므로 커뮤니티에서 도는 이야기로
받아들이는 편이 맞다.
다만 이식(Porting) 페이지가 SBCL 0.7.5부터 부트스트래핑 전체가 이식성 있는 ANSI
Common Lisp로 표현된다고 밝히고 있어서, 그가 설명한 내용 자체는 공식 문서와
맞는다.
pfdietz는 분기 이후 코드가 많이 바뀌어서 원래 코드의 흔적은 남아 있겠지만 지금은
완전히 독자적인 시스템이라고 덧붙였다.[^pfdietz]

## 라이선스

SBCL은 CMU CL의 라이선스 조건을 그대로 이어받았다.
대부분의 파일은 퍼블릭 도메인이고, 일부 하위 시스템만 BSD 스타일 라이선스다.
저장소의 `COPYING` 파일에 따르면 BSD 스타일 조건이 붙는 부분은 MIT와
Symbolics에서 온 `LOOP` 매크로, Xerox에서 온 CLOS 구현 PCL이다.
분기 이후의 변경은 가능한 관할권에서는 퍼블릭 도메인으로,
그렇지 않은 곳에서는 FreeBSD 라이선스로 공개했다.
`hopscotch.c`에 들어간 CityHash 혼합 함수는 MIT 라이선스다.

`COPYING`의 결론은 MIT, Symbolics, Xerox,
Gerd Moellmann의 저작권 표시만 남기면
SBCL을 자유롭게 복사하고 쓰고 고칠 수 있다는 것이다.
GitHub 미러의 라이선스 표시는 `Other`(`NOASSERTION`)로 나오는데,
단일 SPDX 식별자로 표현되지 않는 이런 혼합 구성 때문이다.
실행하면 나오는 배너에도 대부분 퍼블릭 도메인이고 일부는 BSD 스타일 라이선스라는
문구가 들어 있다.

## 릴리스 주기와 최근 변경

뉴스 페이지는 새 버전이 보통 매달 말에 나온다고 안내하고,
최근 두 릴리스의 변경 사항만 보여 준다.
나머지는 `all-news.html`에 모여 있는데, 0.6.0부터 2.6.9까지 296개 버전 항목이
들어 있다.
주요 버전의 날짜는 다음과 같다.

| 버전  | 날짜       | 비고                                            |
| ----- | ---------- | ----------------------------------------------- |
| 0.7.0 | 2002-01-19 | 기본 fasl 확장자 변경 등 큰 비호환 변경         |
| 0.8.0 | 2003-05-25 | CLISP를 호스트로 빌드 가능                      |
| 0.9.0 | 2005-04-24 |                                                 |
| 1.0   | 2006-11-30 | FreeBSD/x86 스레드 실험적 지원                  |
| 1.1.0 | 2012-10-01 |                                                 |
| 2.0.0 | 2019-12-29 | 힙 재배치가 Windows를 포함한 전 플랫폼에서 동작 |
| 2.5.0 | 2024-12-29 | Haiku 운영체제 지원 개선                        |
| 2.6.0 | 2025-12-28 | 인식하는 관용구를 짧은 기계어로 변환            |
| 2.6.9 | 2026-09-26 | 최신                                            |

2.6.6(6월 28일), 2.6.7(7월 28일), 2.6.8(8월 28일),
2.6.9(9월 26일)로 이어지는 최근 날짜를 보면 월말 릴리스가 실제로 지켜지고 있다.

### 2.6.7: 매뉴얼이 코드 안으로 들어갔다

2.6.7은 새 기여 모듈 `SB-MANUAL`을 추가했다.
매뉴얼 내용이 절(section) 정의의 독스트링에 들어가고,
절 정의가 일반 Lisp 정의의 독스트링을 묶는 방식이다.
그래서 Slime의 `M-.` 같은 평소 방식으로 매뉴얼을 대화형으로 탐색할 수 있고,
트리 밖의 MGL-PAX 라이브러리로도 볼 수 있다.
공식 매뉴얼은 여전히 Texinfo에서 생성되지만,
그 Texinfo 파일을 `SB-MANUAL`에서 만들어 낸다.
같은 릴리스에서 `SB-SIMD`가 ARM64를 지원하기 시작했고,
x86-64에서 AVX512 명령을 지원하게 되었다.

HN에서 wild_egg는 아직 자동 벡터화는 없다고 짚었다.[^wild_egg]
amno는 `SB-SIMD`가 수작업으로 정의한 명령 데이터베이스에서 매크로로 명령을
생성하고, 컴파일 시점에 컴파일러가 기계어를 내보낼 때 쓰는 내장 함수인 VOP로
바꾸는 코드 생성 계층이라고 설명했다.[^amno]
그의 표현으로는 순수한 인트린식보다는 DSL에 가깝고,
필요한 연산을 직접 요청해야 한다.

### 2.6.8과 2.6.9: 컴파일러 최적화가 계속된다

2.6.8은 Fluet와 Weeks의 2001년 논문 “Contification using Dominators”를 따라,
지역 함수로 쓴 상태 기계 같은 코드를 `tagbody`/`go` 제어 구조로 바꾸는 대입
변환을 거의 모든 경우에 수행하게 되었다.
자기 자신을 재귀 호출하는 지역 함수의 매개변수 타입도 추론할 수 있게 되었다.
2.6.9는 자기 참조나 상호 참조 함수를 참조가 빠져나가지 않는다고 증명할 수 있으면
스택에 자동으로 할당하고,
ARM64와 x86-64에서 부호 있는 128비트 연산에 레지스터 쌍을 쓴다.
같은 릴리스에는 Launchpad 버그 번호가 붙은 잘못된 컴파일(miscompilation) 수정이
여러 건 들어 있다.

## 지원 플랫폼

다운로드 페이지의 표는 운영체제와 프로세서 조합마다 바이너리 상태를
색으로 보여 준다.
표에서 최신 2.6.9 바이너리가 있는 조합은 세 개뿐이다.

| 운영체제 | 최신 바이너리가 있는 조합 | 그보다 오래된 바이너리만 있는 조합                    |
| -------- | ------------------------- | ----------------------------------------------------- |
| Linux    | x86-64 (2.6.9)            | ARMhf 2.3.3, PPC64le 1.5.8, x86 1.4.3, ARM64 1.4.2 등 |
| Windows  | x86-64, ARM64 (2.6.9 MSI) | x86 2.3.2                                             |
| macOS    | 없음                      | ARM64 2.4.0, x86-64 2.2.9, x86 1.1.6                  |
| OpenBSD  | 없음                      | x86-64, x86, PPC, ARMel, ARM64 모두 2.0.5             |
| FreeBSD  | 없음                      | ARM64 2.2.0, x86-64·x86 1.2.7                         |
| Solaris  | 없음                      | SPARC 2.0.4, x86-64·x86 1.2.7                         |

Linux의 RISC-V 32·64와 LoongArch 64는 지원되는 것으로 표시되어 있지만
바이너리 링크는 없다.
FreeBSD와 NetBSD의 RISC-V, FreeBSD의 PPC,
Linux의 PPC64는 이식이 진행 중인 것으로 표시된다.
표 아래에는 과거에 HP PA-RISC Linux, Alpha Linux와 Tru64,
PowerPC Mac OS X에서도 돌았다는 기록이 있다.

이 표가 말하는 바는 “지원된다”와 “최신 바이너리를 내려받을 수 있다”가 다르다는
점이다.
페이지는 이전 바이너리나 운영체제 저장소, Homebrew, MacPorts가 제공하는 SBCL,
혹은 다른 CL 구현으로 최신 소스를 빌드하라고 안내한다.
Linux 바이너리는 최신 glibc를 요구할 수 있지만 소스 빌드는 특정 glibc 버전에
의존하지 않는다고도 적어 두었다.

Windows는 오랫동안 약점으로 여겨졌다.
HN에서 WalterGR가 예전에는 Windows 지원은 CCL이, 속도는 SBCL이 나았다고 기억하자, jorams는 SBCL이 Windows에서 잘 돌고 시작할 때 띄우던 불안정 경고도 6년 전 2.0.3에서 없어졌다고 답했다.[^jorams]
그는 CCL은 활발히 유지되지 않고 ARM64 이식판도 없지만,
최적화를 덜 하는 덕분에 SBCL보다 컴파일이 조금 빨라서 쓰는 사람이 있다고
덧붙였다.
p_l은 SBCL이 Windows 지원에 오래 걸린 이유 중 하나로,
페이지 폴트 정보를 얻으려고 생성 코드에 제대로 된 SEH 지원을 넣은 반면 CCL은 더
쓰기 쉬운 VEH를 썼다는 점을 기억에 기대어 들었다.[^p_l-2]

## 설치하고 실행하기

Getting Started 페이지의 바이너리 설치 절차는 압축을 풀고 설치 스크립트를
실행하는 것이 전부다.
기본 설치 위치는 `/usr/local`이다.

```bash
# 플랫폼 표에서 내려받은 바이너리 이름으로 바꾼다
bzip2 -cd sbcl-2.6.9-x86-64-linux-binary.tar.bz2 | tar xvf -
cd sbcl-2.6.9-x86-64-linux
sh install.sh

# 다른 위치에 설치할 때는 INSTALL_ROOT와 SBCL_HOME을 함께 맞춘다
INSTALL_ROOT=/my/sbcl/prefix sh install.sh
export SBCL_HOME=/my/sbcl/prefix/lib/sbcl
```

`/usr/local/bin`이 `PATH`에 있으면 `sbcl`로 REPL에 들어가고,
`(quit)`나 `(exit)`로 나온다.
매뉴얼은 SBCL을 맨몸으로 쓰기보다 편집기를 연결해 쓰기를 권하며,
현재 권장 환경은 Emacs와 SLIME이다.

`--script` 옵션을 쓰면 셔뱅 스크립트를 만들 수 있다.
SBCL은 파일을 읽을 때 첫 줄의 셔뱅을 건너뛴다.

```lisp
#!/usr/local/bin/sbcl --script
(write-line "Hello, World!")
```

### 실행 파일 만들기

`sb-ext:save-lisp-and-die`는 현재 Lisp 세션의 전역 상태를 코어 이미지로
저장한다.
스택은 저장하는 과정에서 풀리므로 전역 상태만 남는다.
`:executable t`를 주면 SBCL 런타임과 코어 이미지를 합친 독립 실행 파일이 나온다.
매뉴얼은 런타임이 통째로 들어가므로 배포한 프로그램이 `compile`과 `load`도
호출할 수 있다고 강조한다.

```lisp
;; 빌드용 SBCL 세션에서 실행한다. 호출하면 세션이 종료된다.
(defun main ()
  (write-line "hello from a standalone SBCL binary"))

(sb-ext:save-lisp-and-die "hello"
                          :executable t   ; 런타임과 코어를 한 파일로 합친다
                          :toplevel #'main)
```

`:toplevel` 함수가 반환하면 `(sb-ext:exit :code 0)`을 부른 것과 같다.
`:save-runtime-options`를 참으로 주면 시작할 때 쓴 `--dynamic-space-size`,
`--control-stack-size` 값이 실행 파일에 저장되고,
명령줄 인자가 전부 toplevel로 넘어간다.
`:compression`은 런타임을 `:sb-core-compression` 기능으로 빌드했을 때만 의미가
있고, -7부터 22까지의 zstd 압축 수준을 받는다.
Windows에서는 `:application-type :gui`로 콘솔 창이 뜨지 않게 할 수 있다.
`:executable :elf-object`는 링크가 더 필요한 `.o`로 감싸는 실험적 기능이다.

Lobste.rs에서 SBCL 프로그램이 무엇으로 컴파일되느냐는 질문에 tumdum은 기본이 네이티브이고 `DISASSEMBLE`로 함수의 기계어를 바로 볼 수 있다고 답했다.[^tumdum]
vindarel은 함수 하나씩 컴파일하면서 오타, 쓰지 않는 변수와 분기,
일부 타입 불일치를 컴파일 시점에 잡아 주고,
그런 다음 빠른 바이너리를 만들어 주니 대화형 개발과 쉬운 배포를 함께 얻는다고
적었다.[^vindarel]

## 소스에서 빌드하기

SBCL은 대부분 Lisp로 작성되어 있어서 처음 부트스트랩할 때 ANSI Common Lisp 실행
파일이 호스트로 필요하다.
Getting Started 페이지는 호스트 후보로 SBCL 자신, CMU Common Lisp, Clozure CL,
CLISP, ABCL, ECL을 든다.
`INSTALL` 문서의 빠른 시작은 다음과 같다.

```bash
sh make.sh                                   # 설치된 sbcl을 호스트로 쓴다
sh make.sh --prefix=/opt/mysbcl              # 설치 위치를 바꾼다
sh make.sh --dynamic-space-size=4Gb          # 기본 동적 공간 크기를 바꾼다
sh make.sh --xc-host='lisp -batch -noinit'   # sbcl이 없으면 CMUCL 등을 호스트로 지정한다
cd ./tests && sh run-tests.sh                # 회귀 테스트
```

빌드에는 약 128MB의 RAM과 스왑이 필요하다고 적혀 있다.
동적 공간 기본값은 32비트에서 512MB, 64비트에서 1GB이고,
OpenBSD만 기본 ulimit에 맞추려고 444MB를 쓴다.
기능은 `--fancy`, `--with-<feature>`, `--without-<feature>`로 켜고 끄며,
`base-target-features.lisp-expr`를 직접 고치지 말라고 한다.
`:SB-CORE-COMPRESSION`은 zstd를 빌드 의존성으로 추가하고,
`:SB-XREF-FOR-INTERNALS`는 코어 크기를 5~6MB 늘린다.
OpenBSD 6.0 이상에서는 `wxallowed` 마운트 옵션이 있는 파일 시스템에서 빌드하고
실행해야 한다고 README가 따로 안내한다.

## 매뉴얼의 주요 내용

매뉴얼은 HTML과 PDF로 제공되고, 모든 Common Lisp 구현에 공통인 내용이 아니라
SBCL에 고유한 동작에 집중한다.
fixnum.com은 SBCL 프로젝트와 무관한 비공식 렌더링이지만,
master 브랜치 기준의 매뉴얼을 HTML, PDF, Markdown,
일반 텍스트로 내놓고 HyperSpec 링크와 인자 기본값까지 넣어 준다고 공식 문서
페이지가 소개한다.
구현 내부를 설명하는 SBCL Internals Manual도 따로 있다.

### 거의 모든 것을 컴파일한다

SBCL은 본질적으로 컴파일러만 있는 구현이다.
몇몇 특수한 경우를 빼면 `eval`은 람다 식을 만들어 `compile`한 뒤 `funcall`한다.
그래서 기본 설정에서는 `functionp`와 `compiled-function-p`가 같은 결과를 낸다.
인터프리터도 있어서 `sb-ext:*evaluator-mode*`를 `:interpret`로 바꿀 수 있지만,
매뉴얼은 다른 구현과 달리 SBCL에서 해석된 코드가 더 안전하거나 디버깅하기 쉽지
않다고 분명히 밝힌다.
매뉴얼은 이 방식 덕분에 해석된 코드와 컴파일된 코드에서 다르게 동작하는 버그가
많지 않다고 설명한다.

fasl 파일은 그것을 만든 SBCL과 정확히 같은 버전에서만 읽힌다.
매뉴얼은 이것이 최적은 아니지만, 버전 사이에서 fasl 호환성을 유지하다가 실수로
깨뜨려 진단하기 어려운 버그를 만드는 것보다 견고했다고 설명한다.

### 타입 선언은 믿는 대상이 아니라 검사할 단언이다

SBCL 컴파일러는 다른 Lisp 컴파일러와 달리 기본 정책에서
타입 선언을 그대로 믿지 않는다.
항상 성립한다고 증명하지 못한 선언은 모두 런타임에 단언으로 검사한다.
검사 수준은 `optimize` 선언의 조합으로 정해진다.

| 정책        | 조건                                     | 동작                                          |
| ----------- | ---------------------------------------- | --------------------------------------------- |
| 완전한 검사 | `(or (>= safety 2) (>= safety speed 1))` | 모든 선언을 정확한 타입으로 검사한다. 기본값  |
| 약한 검사   | `(and (< safety 2) (< safety speed))`    | 검사하기 쉬운 상위 타입으로 단순화한다        |
| 검사 없음   | `(= safety 0)`                           | 선언을 믿고 인자 개수와 배열 경계 검사도 끈다 |

매뉴얼은 약한 검사에서 프로그램에 타입 오류가 있으면 힙을 망가뜨리기 쉽고,
검사 없음에서는 타입 오류가 힙 손상으로 이어질 수 있다고 경고한다.
예외도 있는데, `defclass`의 `:type` 슬롯 옵션은 클래스 정의와 슬롯 접근이 모두
안전한 코드일 때만 검사된다.
`speed`를 높이면 컴파일러가 적용하지 못한 최적화를 노트로 알려 주고,
`space`를 0으로 두면 인라인을 무분별하게 해서 오히려 느려질 수 있다고 한다.

HN의 brabel은 SBCL이 다른 구현보다 나은 가장 큰 이유로 이 타입 지원을 꼽았다.[^brabel]
공개 함수의 타입을 `declaim`해 두면 호출 쪽이나 구현 쪽의 실수를 컴파일할 때
오류나 경고로 받고, `fixnum`이나 `single-float`로 숫자 타입을 좁히면 Lisp의 수
체계를 우회해 C에 가까운 코드가 나온다는 것이다.
반대로 ivanb는 SBCL이 타입 검사에서 아마 가장 나은 Common Lisp 컴파일러지만
리스트의 원소 타입을 지정할 수 없어서, 함수마다 `declaim`해 보면 타입이
Python보다도 모호하게 나온다고 지적했다.[^ivanb]
a-french-anon은 그렇게 하면 `DEFTYPE` 본문이 무한 재귀할 수 없다는 표준 규정에
어긋난다고 반박하면서도, 재귀 `DEFTYPE`, 키와 값 타입이 있는 해시 테이블,
CLOS 슬롯의 정적 타입 같은 빈틈은 인정했다.[^a-french-anon]
reikonomusha는 Haskell식 타입을 Common Lisp에 더하고 SBCL에서 특히 효율적인
코드로 컴파일되는 Coalton을 대안으로 소개했다.[^reikonomusha-2]

### 스레드와 GC

스레드는 `sb-thread` 패키지가 제공하고, 운영체제 스레드에 대응하므로
멀티프로세서를 쓸 수 있지만 Lisp에서 스케줄러를 제어할 수는 없다.
매뉴얼 기준으로 x86[-64]/ARM64 Linux와 Windows에서는 기본 빌드에 포함되고,
Darwin, FreeBSD, Solaris, PPC Linux, RISC-V Linux 등에서는
빌드할 때 직접 켜야 한다.
Linux x86 계열 구현 절은 pthread와 futex를 쓰고,
스레드마다 보통 8KB짜리 할당 영역을 따로 두며,
수집할 때는 신호를 보내 모든 스레드를 멈춘다고 설명한다.
라이브러리의 상당 부분은 아직 스레드 안전성을 점검하지 않았고,
그래서 컴파일과 fasl 적재 같은 영역은 큰 락으로 감싸여 병렬화할 수 없다고
매뉴얼이 직접 밝힌다.

### 표준 밖의 확장과 기여 모듈

매뉴얼 소개 절은 확장 목록을 길게 싣는다.
C 연동용 `sb-alien` FFI와 정의 생성을 돕는 `sb-grovel`,
스레드 없이 여러 스트림을 비차단으로 다루는 `serve-event`, 타임아웃과 데드라인,
AMOP를 따르는 `sb-mop`, 확장 가능한 시퀀스, `sb-bsd-sockets` 네트워킹,
`sb-posix`, Gray Streams와 Simple Streams,
함수 단위 결정적 프로파일러 `sb-profile`과 통계 프로파일러 `sb-sprof`가 있다.
2.6.0부터 코드 커버리지 도구 `SB-COVER`는 LCOV 호환 보고서도 낼 수 있다.
기여 모듈은 `(require :<모듈 이름>)`으로 적재하고, 매뉴얼은 `sb-aclrepl`,
`sb-concurrency`, `sb-cover`, `sb-grovel`, `sb-introspect`, `sb-manual`,
`sb-md5`, `sb-posix`, `sb-queue`, `sb-rotate-byte`, `sb-simd`를 문서화한다.
매뉴얼은 모든 확장이 제대로 문서화된 것은 아니라고 스스로 인정한다.

## 저장소와 기여

공식 git 저장소는 SourceForge에 있고, GitHub의 `sbcl/sbcl`은 설명에 공식
저장소의 미러라고 적힌 저장소다.
2026년 10월 7일 GitHub API로 확인한 미러는 별 2,156개, 포크 362개이고,
2011년 6월 13일에 만들어졌으며, 이슈 기능은 꺼져 있다.
버그 추적은 Launchpad가 맡는다.

`HACKING` 문서에 따르면 패치는 `git format-patch` 출력 형식을 선호한다.
커밋 메시지에는 변경의 이유와 방법을 쓰고, 가능하면 테스트를 함께 넣고,
알고리즘 변경은 설명하고 출판된 알고리즘이면 논문 링크를 달라고 한다.
바로 적용할 수 있는 패치는 Launchpad 버그에 `review` 태그를 달아 올리고,
넓은 논의가 필요한 패치는 `sbcl-devel` 메일링 리스트로 보낸다.
질문은 `sbcl-devel`이나 `#sbcl@irc.libera.chat`에서 받는다.
메일링 리스트는 스팸을 막으려고 구독해야 글을 쓸 수 있다.

SBCL로 돌아가는 유명한 서비스로는 Hacker News가 있다.
philipkglass는 HN이 돌아가는 Arc가 원래 Racket 위에서 돌아서 큰 토론을 여러
페이지로 나눠야 했는데, 2024년 9월 무렵 Arc를 SBCL로 이식한 뒤로 가장 큰 토론도
나눌 필요가 없어졌고 서버가 멈추거나 재시작하는 일도 줄었다고
정리했다.[^philipkglass]

## 트레이드오프

### 이미지 기반 배포는 편하지만 조합하기 어렵다

`save-lisp-and-die` 하나로 런타임과 컴파일러까지 든 실행 파일이 나오는 것은
배포를 아주 단순하게 만든다.
그 대가로 결과물은 소스 트리가 아니라 세션 상태의 스냅숏이고,
저장할 때 세션이 끝난다.
HN에서 galaxyLogic은 Smalltalk에서 이미지가 중심이었던 것이 상업적 몰락의 한 원인이라고 보면서, 두 이미지를 합치거나 이미지를 부품으로 써서 새것을 만들 수 없다고 지적했다.[^galaxyLogic]
SBCL의 실행 파일도 같은 성질을 가지므로,
재현 가능한 배포를 원한다면 빌드 스크립트가 깨끗한 세션에서 시스템을 적재하고
저장하도록 만들어 이미지가 아니라 스크립트를 진실의 원천으로 두는 편이 낫다고
나는 해석한다.

### 버전 고정 fasl은 견고하지만 캐시를 무효화한다

fasl이 정확히 같은 버전에서만 읽힌다는 결정은 매뉴얼 말대로 미묘한 호환성 버그를
원천 차단한다.
대신 매달 릴리스되는 SBCL을 올릴 때마다 컴파일된 의존성 캐시가 전부 무효가 된다.
매뉴얼은 ASDF에서 `sb-ext:invalid-fasl` 조건을 잡아 다시 컴파일하는 방법을
예시로 든다.
월간 릴리스와 버전 고정 fasl이 합쳐지면,
CI에서 SBCL 버전을 명시적으로 고정하지 않는 한
빌드 시간이 예고 없이 늘어나는 날이 매달 온다.

### 타입 단언은 안전과 속도를 같은 손잡이로 조절한다

타입 선언을 단언으로 다루는 정책은 선언이 많을수록 안전해지는 드문 구조다.
그러나 같은 선언으로 속도를 얻으려고 `safety`를 낮추는 순간,
매뉴얼이 경고하듯 잘못된 선언이 조용히 힙을 망가뜨린다.
즉 안전을 위해 쓴 선언과 속도를 위해 쓴 선언이 같은 문법이고,
차이는 둘러싼 `optimize` 정책에만 있다.
`safety 0`은 측정으로 확인된 핫스팟에만 지역적으로 쓰고,
전역 정책은 기본값을 유지하는 것이 이 구조에서 손해를 줄이는 방법이다.

### 도구와 생태계는 구현만큼 강하지 않다

SBCL 자체의 평판과 별개로, HN 댓글의 불만은 주로 주변에 몰린다.
cultofmetatron은 LispWorks와 Allegro는 비싼 상용 제품이고,
사실상 최선의 오픈소스 선택지인 SBCL의 도구가 더 좋았으면 한다며 VS Code
사용자로서 Emacs를 요구받는 부담을 털어놓았다.[^cultofmetatron]
BaculumMeumEst는 Active Directory 인증용 Kerberos 라이브러리를 찾았지만 Windows
KDC가 그 라이브러리의 암호화 알고리즘을 더 이상 받지 않아,
Java 내장 보안 패키지를 쓸 수 있는 Clojure로 해결했다고 적었다.[^BaculumMeumEst]
구현의 성능과 안정성이 생태계의 빈틈을 메워 주지는 않는다는 사례다.

## 함정

매뉴얼과 `INSTALL`이 스레드 기본값을 다르게 적고 있다.
매뉴얼은 x86[-64]/ARM64 Linux와 Windows에서 기본 빌드에 포함된다고 하지만,
`INSTALL`의 `:SB-THREAD` 설명은 x86[-64] Linux에서만 기본으로 켜진다고 적는다.
직접 빌드한다면 `*features*`에 `:sb-thread`가 있는지 확인하는 것이
문서를 믿는 것보다 확실하다.

“지원 플랫폼”과 “최신 바이너리”를 혼동하기 쉽다.
macOS ARM64의 공식 바이너리는 2.4.0, Linux ARM64는 1.4.2에 머물러 있으므로,
이 플랫폼에서 최신 버전을 쓰려면 패키지 관리자 빌드나 소스 빌드를 써야 한다.
2.6.6 릴리스 노트에 macOS 27 ARM64를 위해 정적 공간 주소를 옮긴 수정이 있는
것처럼, 운영체제 업데이트가 오래된 바이너리를 깨뜨릴 수도 있다.

문서화되지 않은 기능이 있다.
HN에서 stackghost는 2.4.x 때부터 아레나 할당이 있었지만 매뉴얼에는 없고, `SB-VM:NEW-ARENA`로 아레나를 만들고 `SB-VM:WITH-ARENA`로 일반 할당을 그 아레나로 돌린다고 설명했다.[^stackghost]
그가 말한 유일한 문서는 내부 노트이고 거기에도 `NEW-ARENA`는 빠져 있다고 한다.
나는 매뉴얼에서 아레나 절을 찾지 못했으므로,
이 기능을 쓴다면 내부 API로 보고 버전마다 동작을 다시 확인해야 한다.

x86의 GC는 보수적이다.
매뉴얼은 태그 없는 데이터, 예를 들어 날 부동소수점 값을 포인터일 수도 있는
값으로 보고 그것이 가리키는 객체를 수집하지 않으므로,
실제로는 최악에 가깝지 않지만 이따금 이상한 메모리 사용 패턴이 생길 수 있다고
설명한다.

메모리를 오버커밋한다.
시작할 때 넉넉한 주소 공간을 예약하고, 너무 많이 쓰면 그때 실패한다.
컨테이너처럼 메모리 한도가 빡빡한 환경에서는 `--dynamic-space-size`를 한도에
맞게 명시하는 편이 안전하다고 나는 판단한다.

---

[^reikonomusha]: <https://news.ycombinator.com/item?id=36545026>

[^jwr]: <https://news.ycombinator.com/item?id=36547967>

[^p_l]: <https://news.ycombinator.com/item?id=47143595>

[^pfdietz]: <https://news.ycombinator.com/item?id=36545441>

[^wild_egg]: <https://news.ycombinator.com/item?id=49087758>

[^amno]: <https://news.ycombinator.com/item?id=49120982>

[^jorams]: <https://news.ycombinator.com/item?id=49089692>

[^p_l-2]: <https://news.ycombinator.com/item?id=49090232>

[^tumdum]: <https://lobste.rs/s/hk8yw5/steel_bank_common_lisp_2_5_9#c_wfzwpo>

[^vindarel]: <https://lobste.rs/s/hk8yw5/steel_bank_common_lisp_2_5_9#c_amnxlf>

[^brabel]: <https://news.ycombinator.com/item?id=36546990>

[^ivanb]: <https://news.ycombinator.com/item?id=47147323>

[^a-french-anon]: <https://news.ycombinator.com/item?id=47149033>

[^reikonomusha-2]: <https://news.ycombinator.com/item?id=47148044>

[^philipkglass]: <https://news.ycombinator.com/item?id=47142202>

[^galaxyLogic]: <https://news.ycombinator.com/item?id=49093471>

[^cultofmetatron]: <https://news.ycombinator.com/item?id=47142509>

[^BaculumMeumEst]: <https://news.ycombinator.com/item?id=36548476>

[^stackghost]: <https://news.ycombinator.com/item?id=49088657>
