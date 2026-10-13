# C와 CGI로 만든 현대 웹 앱: 1994년의 기술로 2026년의 상용 제품을

원문: [A modern web app in c | Corey Prophitt](https://prophitt.me/writing/a-modern-web-app-in-c)

HN 토론: <https://news.ycombinator.com/item?id=50058528> (449점, 179개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/cjdy6d/modern_web_app_c> (2점, 5개 댓글)

GN 토론: <https://news.hada.io/topic?id=35253>

## 요약

Corey Prophitt가 자기 상용 웹 제품 marketyour.games를
C로 작성하고 CGI로 서빙한 경험을 정리한 글이다.
그는 1994년에 동적 웹사이트를 원하면 C 프로그램을 `cgi-bin`에 넣고
Apache가 요청마다 프로세스를 띄우게 했는데,
32년 뒤 자신이 근본적으로 같은 기술로 상용 제품을 출시했다고 말한다.
제품 자체는 현대적이다.
사용자 계정, 콘텐츠 제작자를 위한 검색 대시보드, 폴더 정리,
Stripe 결제와 Postmark 트랜잭션 메일이 있고,
점진적 향상(progressive enhancement)을 따라 JavaScript 없이도 동작한다.
요약하면 CGI가 쇠퇴한 이유는 2004년에는 타당했지만 2026년에는 성립하지 않으며,
바이너리 하나와 SQLite 파일 하나, 의존성 셋으로
전체가 머릿속에 들어오는 웹 앱을 만들 수 있다는 것이다.

스택은 BCHS, 즉 OpenBSD, C, httpd, SQLite다.
프레임워크도 템플릿 언어도 없고,
C 프로그램이 CGI 환경 변수를 읽어 HTML을 직접 출력한다.
별도 데이터베이스 서버 없이 SQLite C API로 파일을 열고,
컨테이너 없이 정적 링크한 바이너리를 폴더에 넣는다.
요청마다 새 프로세스가 뜨므로 배포는 파일 하나를 바꾸는 것이고,
서버 재시작이나 다운타임이 없다.
OpenBSD의 `pledge`와 `unveil`로 C 프로그램을 잠글 수 있고,
httpd는 기본으로 chroot에서 서빙해 CGI 바이너리가 파일 시스템의 한쪽에 갇힌다.
외부 라이브러리는 셋이다.
Stripe와 Postmark 호출에 libcurl,
무작위 식별자 생성과 비밀번호 해시, Stripe 웹훅 HMAC 검증에 libsodium,
JSON 파싱에 libcjson을 쓴다.
libcjson은 C 파일 하나이고 SQLite도 공식 단일 파일(amalgamation) 빌드가 있어
둘 다 프로젝트에 포함했으며,
실제 빌드 의존성은 libcurl과 libsodium뿐이다.
깨끗한 빌드는 몇 초, 재빌드는 0.5초 안에 끝난다.
정적 자원도 따로 서빙하지 않고 실행 파일에 넣어 메모리에서 내보낸다.

좋았던 점으로는 다섯 가지를 든다.
첫째, 배울 프레임워크가 없다.
CGI 1.1 명세는 2004년에 나온 뒤 바뀌지 않았고,
요청 헤더, 메서드, 쿼리 문자열, 본문이라는 HTTP 기본만 알면 된다.
둘째, 관심사가 분명히 나뉜다.
nginx 뒤에 다른 언어의 애플리케이션 서버를 두면 웹 서버가 둘이 되는데,
CGI는 웹 서버 하나가 비즈니스 로직을 직접 부른다.
애플리케이션은 셸에서 요청을 파이프로 넣고
gdb로 따라갈 수 있는 평범한 프로그램이고,
저자는 CGI를 “업체와 깜짝 청구서가 없는 서버리스”라고 부른다.
셋째, 공급망 위험이 작다.
흔한 기술 스택에서는 직접 의존성 몇 개가 수백 개의 간접 의존성을 끌고 오지만,
그의 공급망은 C 컴파일러와 라이브러리 셋이다.
넷째, 도구가 단순하다.
그는 플러그인 없는 Vim을 쓰고 LSP도 자동 완성도 코드 포매터도 AI도 쓰지 않는다.
필요하면 새니타이저, valgrind, gdb, ctags,
cscope 같은 성숙한 도구가 가까이 있다.
다섯째, C로 HTML과 CSS를 쓰는 것이 생각보다 괴롭지 않았다.
템플릿 언어를 편집기가 반쯤 인식하는 문제가 없고,
예쁘지는 않지만 Tailwind도 예쁘지는 않다고 그는 적는다.
PostgreSQL 대신 쓴 SQLite는 관리할 서버 프로세스가 없어 운영 부담이 거의 없었다.

바꾸고 싶은 점은 CGI가 기본으로 주는 것이 거의 없다는 것이다.
쿠키 파싱과 생성, 쿼리 매개변수와 폼 데이터의 파싱과 검증,
화면 출력용 이스케이프를 직접 써야 했다.
그는 이것을 헤더 파일 하나(`cgi.h`)로 만들었지만 옳은 해법인지 확신하지 못한다.
kcgi 같은 라이브러리는 있지만 그 API와 보안 모델에 묶이게 된다.
stb 라이브러리처럼 넣어 쓰는 공용 유틸리티가 있으면 좋겠다며,
`cgi.h`를 공개할지도 모른다고 말한다.
결론은 프로세스 포크가 이제 그렇게 비싸지 않고,
비용이 문제가 되면 FastCGI로 쉽게 옮길 수 있으며,
이 스택이 지금까지 출시한 어떤 것보다
움직이는 부분이 적어 다시 쓸 것이라는 것이다.

## 분석

### 핵심 주장은 “CGI가 버려진 이유가 사라졌다”는 것이다

이 글의 논리는 역사적 재평가다.
CGI는 요청마다 프로세스를 띄우는 비용 때문에 2000년대 초반 버려졌고,
그 자리를 상주 애플리케이션 서버와 FastCGI, 언어별 프레임워크가 채웠다.
저자는 그 비용이 지금은 현대 커널에서 충분히 싸졌고,
그렇다면 CGI가 가진 단순함을 포기할 이유가 없다고 말한다.

이 논리는 기술 선택이 특정 시점의 제약에 대한 답이라는 점을 짚는다.
제약이 바뀌면 답도 다시 따져 볼 만하다.
글이 강조하는 “배포는 파일 하나 교체”, “다운타임 없음”,
“셸에서 바로 디버깅”은 모두 상주 프로세스가 없어서 생기는 장점이고,
상주 서버를 택하며 우리가 잃은 것들이다.

### 공급망 위험이 단순함의 새 근거가 되었다

저자가 든 장점 가운데 시대적 의미가 가장 큰 것은 공급망이다.
그는 자율 에이전트의 부상과 매주 일어나는 패키지 저장소 공격을 이유로
의존성이 적은 것이 안심된다고 말한다.
libcurl을 뚫어야 자기 공급망이 뚫린다는 문장은
수많은 사람이 지켜보는 프로젝트와 주간 다운로드 11회짜리 패키지를 대비시킨다.

이 근거는 10년 전이었다면 덜 설득력 있었을 것이다.
지금은 패키지 생태계 공격이 일상이 되었고,
의존성 수 자체가 위험의 지표가 되었다.
저자의 미니멀리즘은 취향이면서 동시에 위협 모형에 대한 대응이다.

### OpenBSD가 C의 위험을 상당 부분 떠안는다

C로 인터넷에 노출된 서버를 쓴다는 선택은 보통 메모리 안전성 문제로 비판받는다.
저자는 이 부분을 길게 다루지 않지만,
스택 선택이 그 답의 일부다.
OpenBSD의 `pledge`는 프로세스가 쓸 수 있는 시스템 호출을 제한하고,
`unveil`은 볼 수 있는 파일 경로를 제한하며,
httpd의 chroot는 CGI 바이너리를 파일 시스템 한쪽에 가둔다.
요청마다 프로세스가 새로 뜨는 CGI 모델도
한 요청의 메모리 오류가 다음 요청으로 이어지지 않게 한다.
HN의 ramses0도 `pledge`와 chroot로 권한을 떨어뜨린다는 점까지 포함하면
글의 내용이 모두 사실이고 잘 추론되었다고 평가했다.[^ramses0]

## 비평

### “왜 C인가”에 답하지 않는다

HN의 fmo91은 저자가 왜 처음에 C를 골랐는지 분명하지 않다고 물었다.[^fmo91]
저자 prophittcorey는 왜 X가 아니라 C인지 말하면
댓글이 언어 전쟁으로 번질 것 같아
일부러 쓰지 않았다고 답했다.[^prophittcorey-why]
layer8은 쓰는 라이브러리가 대개 C로 되어 있으니
네이티브 인터페이스로 쓰는 편이 다른 언어
런타임을 더하지 않아 단순하다고 대신 답했다.[^layer8]

그러나 이 공백은 글의 주장을 약하게 만든다.
글의 장점 목록 대부분, 즉 바이너리 하나, 적은 의존성, 단순한 배포는
C가 아니어도 얻을 수 있다.
benlivengood와 ok123456은 Go를 `CGO_ENABLED=0`으로 빌드하면
libc 없이 바이너리 하나로 웹 서비스를 내보낼 수 있고,
템플릿과 문서를 넣어 scratch 컨테이너에 두면
더 나은 도구와 배포 경험을 준다고 지적했다.[^benlivengood][^ok123456]
C에만 있는 장점이 무엇인지 말하지 않으면
글은 “CGI의 재발견”과 “C의 선택”이라는 두 주장을 구분하지 못한다.

Lobste.rs의 dzwdz는 편집기가 반쯤 인식하는 두 번째 언어가 없다는 장점도 반박했다.[^dzwdz]
템플릿 언어를 쓰지 않을 뿐 C 안에서 printf 같은 것으로 HTML을 출력하고 있으니,
결국 다른 언어 안에 HTML을 넣는 구조는 그대로라는 것이다.

### 메모리 안전성 문제를 너무 가볍게 넘긴다

modeless는 Fil-C처럼 메모리 안전성을 보장하는 C를 쓴다면 방어할 만한 선택이지만,
그렇지 않으면 무책임하다고 했다.[^modeless]
nostrademons는 메모리 안전성 문제는
인터넷에 노출된 서버 소프트웨어에 치명적이라며,
AI로 코드를 쓴다면 왜 C가 아니라 Rust를 쓰지 않느냐고 물었다.[^nostrademons]
whizzter는 평범한 C에서 범위 밖 접근 위험을 안고
메모리와 정적 문자열을 관리하는 것이 끔찍하다고 했다.[^whizzter]

저자의 `cgi.h`가 바로 그 위험이 모이는 곳이다.
쿠키, 쿼리 매개변수, 폼 데이터 파싱, 출력 이스케이프는
웹 애플리케이션에서 공격자가 통제하는 입력이 처음 닿는 지점이고,
저자는 이것을 직접 썼다고 밝힌다.
OpenBSD의 격리가 피해를 줄여 주지만,
`pledge`와 `unveil` 안에서도 데이터베이스와 결제 비밀은 그 프로세스가 다룬다.
글이 이 부분을 “직접 썼지만 옳은 해법인지 모르겠다”로만 남긴 것은
상용 제품을 소개하는 글로서 아쉽다.

### 규모와 동시성에 대한 질문이 남는다

Panzerschrek은 요청마다 프로세스가 뜨는데
SQLite가 여러 프로세스의 동시 쓰기를 어떻게 처리하느냐고 물었다.[^Panzerschrek]
저자는 SQLite를 WAL 모드로 두면 읽기는 모두
동시에 되지만 쓰기는 여전히 순차적이고,
busy timeout을 설정하지 않으면 막힌 쓰기가
바로 시간 초과된다고 답했다.[^prophittcorey-wal]
tomjen3은 쓰기가 막혀도 네트워크 왕복이 없어 금방 끝나기 때문에
실제로는 오래 기다리지 않는다고 덧붙였다.[^tomjen3]

Lobste.rs의 algernon은 CGI와 역방향 프록시 뒤의 서버가
모두 HTTP 비슷한 인터페이스를 쓰는 만큼 큰 차이가 없고,
상주 서비스는 지속 데이터베이스 연결과 시작 시간이 없다는 작은 이점이
쌓여 훨씬 효율적일 수 있다고 지적했다.[^algernon]
spc476은 CGI가 밀려난 이유가 프로세스 생성 비용이 비싸다는 인식 때문이었고,
스크립트 언어의 느린 시작이 그 비용을 키웠다며
자기 블로그는 여전히 C로 쓴 CGI로 돌린다고 적었다.[^spc476]

이 답은 이 스택이 어떤 규모에서 맞는지를 보여 준다.
쓰기가 적고 트래픽이 크지 않은 제품에서는 문제가 없다.
그러나 글은 marketyour.games의 트래픽이나 쓰기 빈도를 밝히지 않아서,
“CGI 쇠퇴의 이유가 2026년에는 성립하지 않는다”는 일반론이
어느 규모까지 유효한지 독자가 판단할 수 없다.

## 인사이트

### 서버리스는 CGI를 다시 발명한 것이다

저자는 CGI를 “업체와 깜짝 청구서가 없는 서버리스”라고 부른다.
이 비유는 생각보다 정확하다.
AWS Lambda 같은 함수형 서비스도 요청마다 감독자가 코드를 부르고,
환경을 넘기고, 결과를 모은다.
차이는 콜드 스타트를 줄이려는 온갖 장치와 과금 모델이 붙었다는 것뿐이다.

macleginn이 nginx 앞단과 애플리케이션 서버의 차이가 무엇이냐고 묻자,
저자는 보통 구성이 nginx → puma/unicorn/gunicorn → 코드인 반면
CGI는 가운데 층이 없이 nginx → 코드라고 답했다.[^prophittcorey-layers]
웹 개발의 역사는 이 가운데 층을 더하고 빼는 일을 반복해 왔다.
PHP가 CGI의 문제를 풀며 등장했지만,
zelcon이 지적했듯 오늘날 PHP 코드의 대부분은
사실상 FastCGI 래퍼인 PHP-FPM으로 서빙된다.[^zelcon]
층이 사라졌다 다시 생기는 순환 속에서
CGI는 가장 얇은 끝점으로 남아 있다.

### 의존성이 적은 스택은 AI 시대의 감사 가능성을 높인다

저자는 AI를 쓰지 않는다고 밝혔지만,
그의 스택은 역설적으로 AI 시대에 더 유리할 수 있다.
코드 전체가 C 파일 몇 개와 Makefile이고 의존성이 셋뿐이라면,
사람이든 AI든 전체를 한 번에 읽고 감사할 수 있다.
수백 개의 간접 의존성을 가진 프로젝트는
AI 에이전트가 만든 변경이 어디에 영향을 주는지 추적하기 어렵다.

Kuyawa는 AI가 Node Express 같은 기본 C 웹 프레임워크를
만들 때가 되었다고 했고,[^Kuyawa]
zelcon은 이제 AI가 nginx 소스를 읽고 모듈을 제대로 짤 수 있으니
nginx 모듈이 2026년식 C 웹 앱이라고 했다.[^zelcon-module]
만드는 비용이 내려가면 남는 비용은 이해하고 검증하는 비용이고,
그 비용은 코드와 의존성의 크기에 비례한다.
“머릿속에 들어오는” 스택은 미학이 아니라 검증 비용의 문제가 된다.

### 공용 유틸리티의 부재가 이 스택의 진짜 진입 장벽이다

저자가 바꾸고 싶은 점으로 든 것,
즉 쿠키와 폼 파싱과 이스케이프를 직접 써야 한다는 문제는
이 스택이 널리 퍼지지 못한 이유이기도 하다.
codazoda와 chasil은 HN에서
오래된 CGI 라이브러리들을 소개했다.[^codazoda][^chasil]
라이브러리는 있지만 오래되었거나 각자 다른 API를 가지고 있다.

저자가 제안한 stb식 단일 헤더 라이브러리는
이 문제에 대한 C 생태계의 전형적인 답이다.
가장 위험한 입력 처리 코드를 모두가 각자 다시 쓰는 대신,
많은 눈이 검토한 작은 공용 파일 하나를 넣어 쓰는 방식이다.
libcurl이 많은 사람이 지켜보는 프로젝트여서 안전하다는 저자의 논리를
CGI 유틸리티에도 적용하면, `cgi.h`를 공개하는 것이
이 스택을 다른 사람에게 권할 수 있는 조건이 된다.

---

[^ramses0]: <https://news.ycombinator.com/item?id=50059874>

[^fmo91]: <https://news.ycombinator.com/item?id=50059131>

[^prophittcorey-why]: <https://news.ycombinator.com/item?id=50059682>

[^layer8]: <https://news.ycombinator.com/item?id=50062487>

[^benlivengood]: <https://news.ycombinator.com/item?id=50061057>

[^ok123456]: <https://news.ycombinator.com/item?id=50060366>

[^modeless]: <https://news.ycombinator.com/item?id=50066395>

[^nostrademons]: <https://news.ycombinator.com/item?id=50063249>

[^whizzter]: <https://news.ycombinator.com/item?id=50063119>

[^Panzerschrek]: <https://news.ycombinator.com/item?id=50059299>

[^prophittcorey-wal]: <https://news.ycombinator.com/item?id=50059377>

[^tomjen3]: <https://news.ycombinator.com/item?id=50063113>

[^prophittcorey-layers]: <https://news.ycombinator.com/item?id=50062877>

[^zelcon]: <https://news.ycombinator.com/item?id=50065939>

[^Kuyawa]: <https://news.ycombinator.com/item?id=50062266>

[^zelcon-module]: <https://news.ycombinator.com/item?id=50065741>

[^codazoda]: <https://news.ycombinator.com/item?id=50059614>

[^chasil]: <https://news.ycombinator.com/item?id=50063974>

[^dzwdz]: <https://lobste.rs/s/cjdy6d/modern_web_app_c#c_zey4xj>

[^algernon]: <https://lobste.rs/s/cjdy6d/modern_web_app_c#c_02bovv>

[^spc476]: <https://lobste.rs/s/cjdy6d/modern_web_app_c#c_rkzgei>
