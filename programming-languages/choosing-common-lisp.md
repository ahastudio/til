# Clojure를 떠나 Common Lisp를 고른 이유: 실행 파일과 요구 사항 목록

원문: [Why I Chose Common Lisp — Dan's Musings](https://blog.djhaskin.com/blog/why-i-chose-common-lisp/)

HN 토론: <https://news.ycombinator.com/item?id=42671105> (363점, 191개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/szpcqf/why_i_chose_common_lisp> (47점, 7개 댓글)

GN 토론: <https://news.hada.io/topic?id=18706>

## 요약

Dan Haskin이 2025년 1월 12일 개인 블로그에 쓴 글이다.
그는 약 7년 동안 Clojure를 썼는데, CLI 앱을 만들면서 시작 시간이 너무 긴 것이
싫어졌다고 말한다.
babashka를 만드는 사람들 말고는 커뮤니티 전반이 이 문제에 관심이 없어 보였고,
GraalVM `native-image`와 오랜 시간 씨름했지만 결국 빨리 시작되는 독립 실행
파일을 얻지 못했다.
그는 그것이 취미로 주로 쓸 언어의 필수 조건이라고 판단하고 Clojure를 떠나기로
했다.

새 Lisp를 고르면서 처음에는 목록으로 적지 않았지만,
돌이켜 보면 다음 요구 사항이 있었다고 정리한다.

- 적당한 도구로 빨리 시작되는 독립 실행 파일을 쉽게 만들 수 있을 것
- Emacs를 쓸 수 없으니 Vim에서 쓸 수 있을 것
- Linux뿐 아니라 Windows와 Mac도 잘 지원할 것
- Clojure가 Java에 붙듯, 커뮤니티가 큰 명령형 언어에 붙을 수 있으면 좋을 것
- 런타임이 Clojure만큼이거나 그보다 빠를 것
- 멀티스레딩이 강하고, 가능하면 GIL이 없을 것
- 커뮤니티가 강할 것
- JSON, SQLite3, HTTP 요청 라이브러리가 잘 갖춰져 있을 것
- Clojure 같은 함수형 자료 구조가 있으면 좋을 것

Scheme은 커뮤니티가 아직 R6RS와 R7RS 문제로 갈라져 있는 것처럼 보였고 생태계도
충분히 크지 않았다.
Racket은 학교에서 써 봤지만 런타임이 느리고 무거워서 마음에 들지 않았다.
그러다 HN에서 본 lisp-lang.org에 다시 들어가 보고 Common Lisp를 시도해 보기로
했다.
배우는 과정은 험했고, 크리스마스 선물로 받은 CLtL2를 처음부터 읽는 잘못된
방식으로 시작했다가 나중에 HyperSpec을 찾았다고 적는다.
그는 Common Lisp가 Java보다 C에 가까운 표준 언어여서 그 표준을 구현한 컴파일러와
런타임이 여럿 있고, 커뮤니티에서 가장 많이 쓰는 구현은 SBCL이라는 점이
뜻밖이었다고 말한다.
처음부터 Janet을 알았다면 거기서 멈췄을 수도 있지만,
CLOS와 조건 시스템을 생각하면 Common Lisp를 먼저 배운 것이 다행이라고 덧붙인다.

요구 사항에 대한 답은 이렇게 정리된다.

| 요구 사항           | 저자가 찾은 답                                                                     |
| ------------------- | ---------------------------------------------------------------------------------- |
| 독립 실행 파일      | 여러 방법이 있고, 압축 여부에 따라 시작이 1초 미만에서 거의 즉시까지 걸린다        |
| Vim                 | 자신만의 Vim 작업 흐름을 만들었고, VS Code도 충분히 쓸 만했다                      |
| Windows, Mac, Linux | SBCL이 세 운영체제를 비교적 잘 지원한다                                            |
| 큰 명령형 생태계    | 대부분의 구현이 CFFI로 C에 잘 붙는다                                               |
| 런타임 속도         | SBCL은 엄청나게 빠르다                                                             |
| 멀티스레딩          | 표준에는 없지만 주요 구현이 지원하고 Bordeaux-Threads, lparallel이 차이를 감춘다   |
| 커뮤니티            | 2024년 커뮤니티 설문, European Lisp Symposium, 블로그와 서브레딧                   |
| 라이브러리          | JSON은 jzon, SQLite3는 cl-sqlite, HTTP는 dexador, 함수형 자료 구조는 FSet, cl-hamt |

패키지 관리는 대부분 Quicklisp를 쓰지만 저자는 OCICL을 쓴다.
그는 Common Lisp Discord에 자신이 처음 그랬던 것처럼 같은 질문을 하는 새
사람들이 늘어서, 자신이 왜 이 언어로 왔고 어떻게 적응했는지 남기려고 이 글을
썼다고 밝힌다.

## 분석

### 결정을 이끈 것은 언어 기능이 아니라 배포 형태다

글의 출발점은 매크로나 REPL 같은 Lisp의 대표적 장점이 아니라 CLI 앱의 시작
시간이다.
JVM 위에 있는 Clojure에서는 빨리 시작되는 독립 실행 파일을 만들려면 GraalVM
`native-image`를 거쳐야 하는데, 저자는 그 과정에서 실패했다.
HN에서 Clojure에서 Common Lisp로 정반대로 옮겨 간 jwr가 babashka로 충분하지 않았느냐고 묻자, 저자 djha-skin은 이미 babashka가 포함한 것보다 많은 라이브러리를 쓰는 큰 앱을 만들어 두었기 때문에 자기 코드베이스에 `native-image`를 직접 돌려야 했고, 처음부터 그것을 염두에 두지 않은 기존 코드베이스에 `native-image`를 적용하는 일은 악몽이었다고 답했다[^djha-skin].
몇 달 전 다시 시도했을 때도 오류가 너무 불투명하거나 앱이 이상하게 동작해 진척이
없었다고 했다.

huahaiy는 Clojure의 GraalVM 네이티브 이미지는 해결된 문제이며,
`graal-build-time` 라이브러리를 추가하고 플래그 하나만 더하면 순수 Clojure
코드는 대부분 동작한다고 반박했다[^huahaiy].
다만 네이티브 라이브러리에 의존하는 복잡한 경우에는 손을 봐야 한다고 덧붙였는데,
저자의 앱이 바로 그런 경우였다.
같은 도구가 어떤 사람에게는 해결된 문제이고 어떤 사람에게는 악몽인 것은,
처음부터 그 도구를 전제로 설계했느냐에 달려 있다.

### 요구 사항 목록은 사후에 쓴 결정의 기록이다

저자 스스로 처음에는 요구 사항을 적지 않았고 돌이켜 보며 정리했다고 밝힌다.
이 목록은 선택을 이끈 기준이라기보다 선택을 설명하기 위해 다시 쓴 기준에 가깝다.
특히 Lisp여야 한다는 가장 큰 조건은 목록에 없지만,
새 Lisp를 찾아 나섰다는 소제목이 그것을 이미 전제한다.

### Lisp 사이의 이동은 Lisp 생태계의 분열을 보여 준다

글은 Clojure, Scheme, Racket, Janet, Common Lisp를 차례로 비교한다.
같은 Lisp 계열이라도 런타임(JVM, 네이티브), 표준화(R6RS와 R7RS의 갈등,
ANSI 표준), 커뮤니티 규모가 모두 다르다.
Lobste.rs의 williewillus는 Clojure, Racket, Common Lisp, Chez Scheme을 모두 써 봤다며 각자 강점이 있지만, 자료 구조를 만들고 분해하고 전달하고 다루는 능력에서는 Clojure를 따라올 Lisp가 없다고 평가했다[^williewillus].
yogsototh는 Clojure의 가장 큰 강점은 기본 불변 자료 구조이며,
Common Lisp나 Scheme을 쓸 때 가장 아쉬운 점이 그것이라고 덧붙였다[^yogsototh].
Lisp를 고른다는 것은 하나의 언어가 아니라 여러 철학 가운데 하나를 고르는 일이다.

## 비평

### 요구 사항이 Lisp를 가리키지 않는다

stevebmark는 요구 사항 충족 섹션의 논리는 거의 모든 언어에 적용된다며,
JSON 라이브러리가 있어서 Common Lisp를 골랐느냐고 꼬집었다[^stevebmark].
IshKebab은 그 요구 사항을 보고 저자가 Rust나 Go를 고를 줄 알았다며,
틈새 언어여야 한다는 숨은 조건이 있었던 것 같다고 했다[^IshKebab].
billmcneale은 요약하자면 Lisp를 쓰던 사람이 다른 Lisp를 찾은 것이며,
2025년에 새 프로젝트로 Common Lisp를 고르는 이유는 아마 그것뿐일 것이라고
냉소했다[^billmcneale].

이 비판은 정당하다.
독립 실행 파일, 빠른 런타임, 멀티스레딩,
JSON과 SQLite와 HTTP 라이브러리라는 조건만 보면 Go나 Rust가 더 쉽게 충족한다.
글이 Common Lisp를 고른 진짜 이유는 목록 밖에 있는 Lisp에 대한 애착이고,
목록은 그 애착 안에서 후보를 좁히는 역할만 한다.
그 자체가 잘못은 아니지만, 글의 제목이 약속하는 선택의 이유는 사실상 설명되지
않는다.

### 커뮤니티가 관심이 없었다는 진단은 부정확하다

저자는 Clojure 커뮤니티가 시작 시간 문제에 관심이 없어 보였다고 적었다.
Lobste.rs의 wink는 이에 반대하며, Leiningen 저장소의 버그 보고 중 상당 비율이 느리다는 내용이었으니 사람들은 분명히 관심이 있었고, 문제는 고칠 수 없었던 것이라고 지적했다[^wink].
kingmob은 이것이 커뮤니티의 문제가 아니라 핵심 팀의 관심사에 달린 문제이며,
더 나은 컴파일러 오류 메시지처럼 핵심 팀이 관심을 두지 않는 주제는 들어가지
않는다고 덧붙였다[^kingmob].
저자가 겪은 좌절의 원인을 커뮤니티의 무관심으로 돌린 것은,
언어의 의사 결정 구조라는 더 중요한 차이를 가린다.

### 편집기 선택이 비교의 공정성을 흔든다

저자는 Emacs를 쓸 수 없어 Vim에서 쓸 수 있어야 한다는 조건을 둔다.
평생 Vim을 써 왔다는 aidenn0은 10년 넘게 Vim으로 Common Lisp를 개발했지만 Lisp
IDE로는 지금 Emacs를 쓰며, evil-mode 이전에 마우스와 메뉴로 90%를 하던 때조차
당시 Vim의 최선보다 나았다고 했다[^aidenn0].
그는 저자의 Vim 설정이 꽤 좋지만 Emacs와 SLIME이 여전히 낫다며,
Emacs에서 한 번에 되는 일이 저자의 Vim 설정에서는 여러 키를 거쳐야 한다고
지적했다.
pjmlp은 Lisp Machine과 Interlisp-D에서 이어진 상용 Common Lisp 시스템의 뛰어난
도구를 생각하면 Vim이 선택지가 되는 것이 안타깝다고 했다[^pjmlp].
Lisp의 대화형 개발 경험은 편집기 통합에 크게 기대므로,
Vim이라는 조건은 저자가 경험한 Common Lisp가 그 언어의 최선과 다를 수 있음을
뜻한다.

## 인사이트

### 배포 형태가 언어 선택을 정하는 시대다

이 글의 가장 쓸모 있는 교훈은 언어를 고를 때 문법이나 패러다임보다 배포 형태가
먼저 결정을 좌우할 수 있다는 점이다.
CLI 도구에서는 단일 실행 파일과 짧은 시작 시간이 사용자 경험의 대부분을
차지하고, 이것이 Go와 Rust가 CLI 도구 시장을 차지한 이유이기도 하다.
JVM 언어가 이 시장에 들어오려면 GraalVM 같은 별도 도구를 거쳐야 하고,
그 도구는 처음부터 그것을 전제로 설계한 코드에서만 잘 동작한다.
언어를 고르기 전에 결과물이 어떤 모양으로 사용자에게 전달될지를 먼저 정하면,
나중에 갈아타는 비용을 줄일 수 있다.

### 실행 중인 이미지는 소스가 사라져도 고칠 수 있게 하지만 그것은 양날의 검이다

agentkilo의 일화는 Common Lisp의 동적인 성격을 극적으로 보여 준다.
고객에게 SBCL로 만든 네이티브 바이너리를 보낸 뒤 소스 코드를 잃어버렸는데,
나중에 고객이 새 요구 사항을 가져오자 옛 바이너리에서 REPL을 띄워 해당 패키지에
들어가 기존 동작을 덮어쓰는 함수를 새로 써서 문제를 해결했다는
것이다[^agentkilo].
chikere232는 멋지지만 버전 관리를 쓰라고 답했다[^chikere232].
smokel은 30년이 지났는데도 대화형 개발 분야의 발전이 실망스럽다며,
실행 중인 시스템에서 함수, 클래스, 패키지 단위의 버전 관리부터 시작해야 한다고
했다[^smokel].
실행 중인 이미지를 고칠 수 있다는 능력은 유연함인 동시에,
코드 저장소와 실제로 돌아가는 시스템이 어긋날 위험이다.
이 저장소의 `programming-languages/common-lisp-best-language.md`가 다룬 이미지
기반 개발 논쟁도 같은 긴장을 보여 준다.

### 표준이 멈춘 언어는 생태계 도구에서 혁신이 일어난다

Common Lisp 표준은 1994년 이후 바뀌지 않았지만,
저자가 쓰는 OCICL은 컨테이너 이미지의 도구와 서비스 생태계를 Lisp 코드 tarball에
적용한다는 발상의 패키지 관리자다.
Lobste.rs의 unwind는 OCICL을 처음 알았다며, 패키지 관리와 컨테이너가 완전히 별개라고 생각했는데 OCI와 CL을 합친 이 발상이 멋지다고 했다[^unwind].
언어 자체가 멈춰 있으면 개선은 구현(SBCL), 라이브러리(Bordeaux-Threads,
lparallel), 패키지 관리(OCICL), 편집기 통합(VS Code용 Alive)처럼 표준 바깥에서
일어난다.
Lobste.rs의 gecko는 VS Code용 Common Lisp 확장 Alive가 LSP로 동작한다고 소개했다[^gecko].
안정된 표준과 활발한 주변 생태계의 조합은,
언어 변화를 따라가는 비용 없이 도구만 바꿔 가며 쓸 수 있는 구조를 만든다.

---

[^djha-skin]: <https://news.ycombinator.com/item?id=42672167>

[^huahaiy]: <https://news.ycombinator.com/item?id=42671736>

[^williewillus]: <https://lobste.rs/s/szpcqf/why_i_chose_common_lisp#c_v93rsh>

[^yogsototh]: <https://lobste.rs/s/szpcqf/why_i_chose_common_lisp#c_m3jdiq>

[^stevebmark]: <https://news.ycombinator.com/item?id=42671595>

[^IshKebab]: <https://news.ycombinator.com/item?id=42671993>

[^billmcneale]: <https://news.ycombinator.com/item?id=42671723>

[^wink]: <https://lobste.rs/s/szpcqf/why_i_chose_common_lisp#c_4fbzjz>

[^kingmob]: <https://lobste.rs/s/szpcqf/why_i_chose_common_lisp#c_arbqet>

[^aidenn0]: <https://news.ycombinator.com/item?id=42674620>

[^pjmlp]: <https://news.ycombinator.com/item?id=42672236>

[^agentkilo]: <https://news.ycombinator.com/item?id=42671640>

[^chikere232]: <https://news.ycombinator.com/item?id=42672089>

[^smokel]: <https://news.ycombinator.com/item?id=42672878>

[^unwind]: <https://lobste.rs/s/szpcqf/why_i_chose_common_lisp#c_vivx9l>

[^gecko]: <https://lobste.rs/s/szpcqf/why_i_chose_common_lisp#c_d6glb1>
