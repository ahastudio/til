# libghostty 1.0은 터미널 에뮬레이션을 안정된 C ABI의 부품으로 만들었다

원문: [Libghostty 1.0 – Mitchell Hashimoto](https://mitchellh.com/writing/libghostty-1-0)

HN 토론: <https://news.ycombinator.com/item?id=50399933> (915점, 150개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/0ouxwf/libghostty_1_0>

GN 토론: <https://news.hada.io/topic?id=36736>

## 요약

Mitchell Hashimoto가 2026년 11월 6일에 libghostty-vt 1.0을 발표했다.
libghostty는 Ghostty의 핵심에서 떼어 낸,
이식성 높고 빠른 터미널 에뮬레이션 C 라이브러리다.
1.0은 라이브러리와 C ABI가 모두 안정되었다는 뜻이다.
글쓴이는 1년 남짓 전에 libghostty가 온다고 썼을 때는 Zig 모듈만 합쳐졌고 C API가
없었으며 쓰는 곳도 Ghostty뿐이었다고 돌아본다.
지금은 C API가 완전한 터미널 에뮬레이터이고 ABI 안정성 정책이 CI로
집행된다고 한다.

이미 쓰는 곳으로 든 사례는 많다.
JetBrains IDE의 터미널이 libghostty 위에서 돈다고 하며,
JetBrains 보고서 기준 활성 사용자가 1,250만 명을 넘는다고 한다.
Neovim에는 libvterm을 libghostty-vt로 바꾸는 승인된 풀 리퀘스트가 있고,
메인테이너들은 배포판이 의존성을 따로 패키징할 수 있도록 태그된 릴리스를
기다린다고 한다.
이 풀 리퀘스트는 스크롤백 리플로 문제로 10년 묵은 이슈도 닫는다고 한다.
KDE의 Konsole 대체 실험, Vercel Turborepo의 TUI, devenv, Emacs용 Ghostel,
WASM 빌드 ghostty-web, OrbStack, cmux와 herdr 같은 에이전트 도구가 그
목록에 있다.
글쓴이는 Ghostty 앱 사용자보다 libghostty 기반 터미널 사용자가 훨씬 많다고
주장한다.
다만 대부분의 소비자가 사용량을 보고하지 않아 수치는 대략적이라고 스스로 밝힌다.

기술 약속은 네 가지다.

- ABI 안정성: 시맨틱 버저닝을 따르고, 모든 객체는 불투명 핸들이며, 값은 열거형 키 기반의 getter와 setter로 읽고 쓴다. 새 헤더로 오래된 라이브러리를 링크하면 충돌 대신 `GHOSTTY_UNSUPPORTED`가 돌아온다. CI는 Linux에서 libabigail로 기준선과 비교하고, ELF에서는 내보낸 기호에 버전을 붙인다.
- 패키징: 서명된 소스 타르볼과 의존성 타르볼을 내서 배포판이 오프라인으로 빌드할 수 있고, SONAME, pkg-config, CMake 설정을 제공한다.
- 의존성과 라이선스: MIT이며 런타임에 libc 외에는 필요 없고, SIMD용 simdutf와 Highway, 유니코드 표, Kitty 그래픽용 Wuffs를 컴파일해 넣는다. 카피레프트 코드는 없고 의존성은 기계가 읽는 목록으로 낸다.
- 이식성: Linux(glibc, musl), macOS, iOS, FreeBSD, Windows, Android, WebAssembly를 빌드하고 테스트한다. 베어메탈 RISC-V와 ARM 등은 빌드만 한다.

자원 사용에 대해서는 스레드를 만들지 않고 할당자를 바꿀 수 있다고 한다.
글쓴이는 4코어 8GB 리눅스 서버에서 쉘이 살아 있는 터미널 1만 개를 띄웠고,
bash는 메모리를 너무 써서 dash를 써야 했다고 한다.
앞으로는 안정성에 집중하면서 가능한 한 많은 터미널 프로토콜을 켜고 끌 수 있게
구현하겠다고 한다.
글 맨 앞 각주는 이 글이 AI의 도움 없이 직접 쓴 것이라고 밝힌다.

## 분석

### 1.0의 의미는 기능이 아니라 약속의 형태다

글이 가장 힘주어 말하는 것은 기능 목록이 아니라 ABI다.
C 라이브러리의 품질은 ABI 안정성으로 드러난다는 것이 글쓴이의 믿음이다.
이는 다른 언어의 패키지 관리자 환경과 구분되는 C 생태계의 특성과 맞닿아 있다.
동적 링크를 하는 배포판은 라이브러리를 한 번 패키징하고 여러 프로그램이 같은
파일을 쓴다.
그러려면 라이브러리가 새 버전으로 바뀌어도 이미 컴파일된 프로그램이 깨지지
않아야 한다.
불투명 핸들, 열거형 키 접근자, 크기가 붙은 구조체는 모두 그 약속을 코드 구조로
옮긴 장치다.

### 채택 사례가 곧 증거라는 논증 방식

글쓴이는 Ghostty를 왜 만드느냐는 질문에 이론이 아니라 사용처로 답한다.
JetBrains에서 터미널 에뮬레이터의 버그를 어려움의 예로 들었던 일이 있고,
1년 뒤 그 IDE의 터미널이 libghostty로 바뀌었다는 서사가 중심이다.
이 구조는 라이브러리가 필요하다는 주장을 이미 필요로 한다는 증거로 대체한다.
다만 증거의 대부분은 목록이며, 각 사례에서 libghostty가 전체 터미널의 어느
부분을 대신하는지는 글이 설명하지 않는다.

### Ghostty에서 라이브러리를 떼어 낸 구조

글은 libghostty를 앱과 다른 릴리스 주기, 다른 타르볼로 둔다고 한다.
앱에 묶여 있으면 배포판이 앱 전체의 의존성을 검토해야 하지만,
라이브러리만 따로 내면 필요한 파일과 의존성만 보면 된다.
HN에서 Decabytes가 왜 Zig가 아니라 C냐고 묻자,
nektro와 trollbridge는 Zig로 쓰고 C ABI를 내보낸 것이라고 답했다.
trollbridge는 Zig 바인딩이 아직 움직이는 표적이라는 이유를
덧붙였다.[^decabytes][^trollbridge]
즉 구현 언어와 약속의 언어가 다르다는 것이 이 설계의 핵심이다.
Lobste.rs에서 gignico는 Zig가 안정되지 않았는데 이렇게 안정된 라이브러리에 Zig를
쓰면 마찰이 생기지 않겠느냐고 물었다.
lalitm은 안정성 계층이 C ABI에 있어서 Zig 쪽의 변동은 C 계층 뒤에 가려진다고
답했다.[^lalitm]
gignico는 다시, C API가 Zig를 가려도 라이브러리를 빌드하려면 특정 Zig 버전이
필요하므로 패키저에게는 제약이 남을 것이라고 짚었다.[^gignico]
ABI 약속은 소비자 쪽의 마찰은 없애지만 빌드하는 쪽의 마찰까지 없애지는 않는다는
구분이다.

## 비평

### 안정된 ABI와 아직 확장 중인 프로토콜 사이에 긴장이 있다

글은 안정성에 집중하면서 존재하는 모든 터미널 프로토콜을 구현하겠다고 한다.
그러나 프로토콜이 늘면 라이브러리의 면적도 늘고,
잘못 설계한 항목은 ABI 안정성 때문에 되돌리기 어려워진다.
글이 이 긴장을 푸는 방법은 켜고 끄는 빌드 플래그와 `GHOSTTY_UNSUPPORTED`
반환이다.
이는 호환성에는 유효하지만 기능이 있는지 없는지가 실행 시점의 값이 된다는
뜻이기도 하다.
임베더가 어떤 빌드 구성에서 어떤 기능이 꺼졌는지 확인하는 부담은
사용자에게 간다.

### 성능과 폭을 보여 주는 수치는 한 사람의 시험이다

1만 개 터미널 시험은 인상적이지만 글쓴이가 직접 돌린 한 번의 시험이다.
같은 조건에서 다른 에뮬레이터를 돌린 비교는 없고,
bash가 메모리를 더 쓴다는 대목은 라이브러리가 아니라 쉘에 관한 이야기다.
HN에서 VadimPR은 libghostty-vt 1.0을 Mudlet의 ANSI 디코더로 시험해 보니 속도
이득이 측정되지 않았고,
터미널 격자가 MUD 클라이언트에 맞지 않았다고 보고했다.
UTF-8만 지원하고 스크롤백을 편집할 수 없기 때문이라고 한다.[^vadimpr]
이 보고는 한 사용자의 한 용도에 한정되지만,
빠르다는 주장이 모든 임베딩에 그대로 이어지지 않는다는 점은 보여 준다.

### 지속 가능성은 글이 다루지 않은 질문이다

글은 1.0의 기술 약속을 길게 쓰면서 유지 비용에 대해서는 말하지 않는다.
HN에서 markstos가 이 일을 재정적으로 어떻게 지속하느냐고 묻자,
답글들은 글쓴이가 HashiCorp 공동 창업자로서 이미 재산이 있고 후원자와 스타트업이
있다고 설명했다.[^markstos]
rvz는 오픈소스의 재원을 비영리 법인, 여러 영리 회사, 고액 자산가의 지원,
단일 회사, 벤처 투자로 나누고
소액 후원은 AI 에이전트 시대에 지속 불가능하다고 썼다.[^rvz]
이 분류는 한 댓글러의 의견이다.
그래도 ABI를 수년간 유지하겠다는 약속은 한 사람의 재정 상황에 기대고 있다는
사실이 남는다.
이는 도입을 고민하는 쪽이 따져 볼 위험 요소다.

## 인사이트

### 터미널 에뮬레이터가 UI에서 부품으로 내려앉고 있다

HN에서 pekim은 libvte와 비교해 libghostty는 UI 없이 에뮬레이션만 제공하고,
Kitty 키보드와 그래픽, 데스크톱 알림 같은 프로토콜을 libvte보다 더 구현한다고
설명했다.[^pekim]
이 차이가 중요한 이유는 UI를 뺀 부분이 곧 재사용 가능한 부분이라는 데 있다.
libvte는 GTK에 묶여 있어 GTK 앱에서만 재사용되지만,
UI 없는 C ABI는 어느 언어와 어느 툴킷에서도 쓸 수 있다.
neomantra는 libghostty 위에서 브라우저 터미널, 녹화 도구, 파일 뷰어,
터미널용 3D 게임 엔진까지 만들었다고 썼다.[^neomantra]
이 목록은 에뮬레이터가 애플리케이션이던 시절에는 상상하기 어려운 조합이다.
터미널이 화면에 글자를 그리는 도구에서 프로그램이 출력을 구조화해 받는 입출력
계층으로 바뀌는 신호로 읽을 수 있다.

### AI 시대에 직접 만들 수 있다는 가정이 부품의 가치를 오히려 보여 준다

didip은 AI가 있으니 각자 필요한 만큼의 터미널 에뮬레이터를 직접 만들면 되지
않느냐고 물었다.
이에 zem은 복잡한 소프트웨어를 정확하고 빠르게 만드는 일은 여전히 많은
노력이 들고,
누군가 해 둔 것 위에 얹는 것이 낫다고 답했다.[^zem]
9dev는 에이전트로 만들 수 있어도 사용량 한도와 토큰 비용 때문에 경제적 고려는
그대로이고,
회사의 일은 터미널 에뮬레이터를 만드는 것이 아니라고 말했다.[^9dev]
gls2ro는 에이전트가 설정하는 구성 요소를 사람들이 조합하는 미래를 그리며
libghostty를 그런 부품의 좋은 예로 들었다.[^gls2ro]
세 답은 한 점으로 모인다.
코드를 만드는 비용이 내려갈수록 병목은 검증과 호환성에 있고,
그 비용을 한 번 치르고 여럿이 나눠 쓰는 라이브러리가 값어치를 갖는다.
이는 글이 말하는 한 임베더의 버그 수정이 모두에게 이득이 된다는 주장과
같은 논리다.

### 표준이 없는 영역에서는 구현이 표준이 된다

터미널 프로토콜은 한 문서로 정리된 표준이 아니라 xterm,
Kitty 같은 구현의 관행이 겹겹이 쌓인 것이다.
libghostty가 JetBrains, Neovim, KDE에 동시에 들어가면 이 라이브러리의 동작이
사실상 기준이 될 가능성이 생긴다.
이는 libvterm이나 libvte가 오래 맡아 온 자리를 대체하는 일이지만,
그 자리를 한 프로젝트가 맡는 것에는 비용이 있다.
라이브러리의 해석이 틀렸을 때 그 오류가 여러 제품에 한꺼번에 퍼진다.
이 문서가 확인하지 못한 것은 이러한 일이 실제로 일어났을 때의 대응 절차다.
글의 ABI 약속은 호환성을 지키지만 동작 오류를 고치는 속도까지 보장하지는 않는다.
Lobste.rs에서 Student는 5년 뒤 터미널 세션의 95%가 libghostty와 그 확장 명령
집합 위에서 돌고,
Microsoft이 독점을 비판하며 자기 터미널을 밀 것이라고 반쯤 농담으로
예측했다.[^student]
이는 근거 없는 예측이지만, 구현이 표준이 될 때 따라붙는 걱정을 정확히 짚는다.
이 위험이 현실이 되는지를 가르는 관찰은 임베더들이 발견한 버그가 얼마나 빨리
수정되어 릴리스에 반영되는가다.

---

[^decabytes]: <https://news.ycombinator.com/item?id=50400677>

[^trollbridge]: <https://news.ycombinator.com/item?id=50400946>

[^vadimpr]: <https://news.ycombinator.com/item?id=50401419>

[^markstos]: <https://news.ycombinator.com/item?id=50401147>

[^rvz]: <https://news.ycombinator.com/item?id=50401845>

[^pekim]: <https://news.ycombinator.com/item?id=50403558>

[^neomantra]: <https://news.ycombinator.com/item?id=50403685>

[^zem]: <https://news.ycombinator.com/item?id=50403384>

[^9dev]: <https://news.ycombinator.com/item?id=50402662>

[^gls2ro]: <https://news.ycombinator.com/item?id=50402744>

[^lalitm]: <https://lobste.rs/s/0ouxwf/libghostty_1_0#c_zgpwnu>

[^gignico]: <https://lobste.rs/s/0ouxwf/libghostty_1_0#c_5oaizr>

[^student]: <https://lobste.rs/s/0ouxwf/libghostty_1_0#c_kquow0>
