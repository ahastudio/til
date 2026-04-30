# FastCGI: 30년이 지나도 리버스 프록시에는 더 나은 프로토콜

원문: <https://www.agwa.name/blog/post/fastcgi_is_the_better_protocol_for_reverse_proxies>

HN 토론: <https://news.ycombinator.com/item?id=47950510> (249점, 19개 댓글)

## 요약

Andrew Ayer는 30년 된 FastCGI가 리버스 프록시와 백엔드 애플리케이션 서버 사이의 통신 프로토콜로 HTTP/1.1보다 여전히 우월하다고 주장한다. FastCGI는 단순한 프로세스 모델이 아니라 TCP나 UNIX 소켓 위에서 동작하는 와이어 프로토콜이며, nginx, Apache, Caddy, HAProxy 모두 FastCGI 백엔드를 지원한다. Go에서는 `http.Serve`를 `fcgi.Serve`로 교체하는 것만으로 전환이 가능하다.

FastCGI의 핵심 보안 이점은 두 가지다. 첫째, 명시적 메시지 프레이밍(explicit message framing)으로 HTTP/1.1의 요청 스머글링(request smuggling) 취약점을 구조적으로 차단한다. HTTP/1.1은 메시지 경계를 프로토콜 자체에 내장하지 않아, 서로 다른 구현체가 같은 요청을 다르게 파싱할 수 있는 공격 면을 제공한다. FastCGI는 1996년부터 이미 명시적 프레이밍을 갖추고 있었다. 둘째, 도메인 분리(domain separation)로 헤더 인젝션을 구조적으로 불가능하게 만든다. 클라이언트 HTTP 헤더는 `HTTP_` 접두사를 붙여 서버 측 파라미터(`REMOTE_ADDR` 등)와 완전히 분리되므로, 공격자가 신뢰된 데이터처럼 보이는 헤더를 주입할 수 없다.

## 분석

### FastCGI 프로토콜의 기술적 구조

FastCGI는 1996년 Open Market이 설계한 바이너리 프레이밍 프로토콜이다. 단순한 프로세스 래퍼가 아니라, TCP 소켓이나 UNIX 도메인 소켓 위에서 동작하는 완전한 와이어 프로토콜이다. 핵심 구조는 레코드(record) 기반이다. 각 레코드는 8바이트 헤더(버전, 타입, 요청 ID, 콘텐츠 길이, 패딩 길이)와 가변 길이 콘텐츠로 구성된다. 타입 필드가 메시지의 역할을 명확히 규정한다.

주요 레코드 타입은 다음과 같다. `FCGI_BEGIN_REQUEST`는 새 요청의 시작을 알린다. `FCGI_PARAMS`는 환경 변수(CGI 파라미터)를 키-값 쌍으로 전달한다. `FCGI_STDIN`은 요청 바디를 스트리밍한다. `FCGI_STDOUT`은 응답을 스트리밍한다. `FCGI_END_REQUEST`는 요청 완료를 알린다. 각 레코드에 요청 ID가 있어 단일 연결에서 여러 요청을 멀티플렉싱할 수 있다. 이 구조는 메시지 경계가 프레임 헤더에 명시적으로 인코딩되므로 파싱 모호성이 없다.

```text
FastCGI Record Format:
+--------+--------+--------+--------+--------+--------+--------+--------+
|version |  type  |   requestIdB1   |  contentLengthB1|paddingLength| rsv|
+--------+--------+--------+--------+--------+--------+--------+--------+
|                          contentData ...                              |
+-----------------------------------------------------------------------+
|                          paddingData ...                              |
+-----------------------------------------------------------------------+
```

### HTTP Request Smuggling의 실제 동작 원리

HTTP/1.1 요청 스머글링은 프록시와 백엔드가 요청의 경계를 다르게 해석할 때 발생한다. HTTP/1.1에는 두 가지 메시지 길이 표현 방식이 있다. `Content-Length` 헤더와 `Transfer-Encoding: chunked`다. 두 헤더가 동시에 존재할 때 어느 것을 우선시하느냐가 구현마다 다를 수 있다.

기본적인 CL.TE(Content-Length/Transfer-Encoding) 공격 시나리오를 보면, 공격자가 다음과 같은 요청을 보낸다.

```text
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```

프론트엔드 프록시가 `Content-Length: 13`을 기준으로 요청을 파싱해 `0\r\n\r\nSMUGGLED`까지 하나의 요청으로 백엔드에 전달한다. 백엔드는 `Transfer-Encoding: chunked`를 기준으로 파싱해 `0\r\n\r\n`에서 요청이 끝났다고 판단한다. 그러면 `SMUGGLED`는 다음 요청의 앞부분으로 처리된다. 이 불일치가 다음 사용자의 요청을 하이재킹하거나, 접근 제어를 우회하거나, 캐시를 오염시키는 데 활용된다.

James Kettle은 PortSwigger Research에서 이 공격의 변형을 체계적으로 연구해 “HTTP/1.1은 죽어야 한다(HTTP/1.1 must die)”고 선언했다. 2005년 Watchfire 연구자들이 처음 경고했지만 10년 이상 무시됐다. Discord 미디어 프록시 취약점은 이 종류의 공격으로 프록시와 백엔드 간 파싱 불일치가 비공개 첨부파일을 노출시킨 실제 사례다. FastCGI는 레코드 길이를 프레임 헤더에 명시적으로 인코딩하므로 이 공격 클래스 전체가 구조적으로 불가능하다.

### “신뢰된 헤더” 인젝션의 구체적 공격 시나리오

리버스 프록시는 백엔드에 클라이언트의 실제 IP, 인증 상태, TLS 정보 같은 신뢰된 데이터를 전달해야 한다. HTTP에서 이는 관례적으로 `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto` 같은 헤더로 전달된다. 문제는 HTTP가 “클라이언트가 보낸 헤더”와 “프록시가 추가한 헤더”를 구조적으로 구분하지 않는다는 것이다.

구체적 공격 시나리오를 보자. 프록시가 `X-Real-IP`를 설정하도록 구성되어 있고 백엔드 미들웨어가 이를 클라이언트 IP로 신뢰한다고 가정한다. 공격자는 요청에 `X-Real-IP: 127.0.0.1`을 직접 포함시킨다. 프록시가 기존 `X-Real-IP` 헤더를 삭제하고 자신의 것으로 교체한다면 막을 수 있다. 그러나 대소문자 변형(`X-REAL-IP`), 공백 변형(`X-Real-Ip`), 또는 다른 헤더(`True-Client-IP`, `CF-Connecting-IP`)를 사용하면 우회할 수 있다. Go의 Chi 미들웨어는 `True-Client-IP`를 `X-Real-IP`보다 먼저 확인하는데, 이를 모르는 프록시 설정에서는 공격자가 `True-Client-IP`를 원하는 값으로 설정해 IP 기반 접근 제어를 우회할 수 있다.

FastCGI는 이를 도메인 분리로 해결한다. 클라이언트 HTTP 헤더는 반드시 `HTTP_` 접두사를 붙여야 한다. `Authorization` 헤더는 `HTTP_AUTHORIZATION`이 된다. 서버 측 신뢰 데이터는 이 접두사 없이 별도 파라미터 공간에 존재한다. `REMOTE_ADDR`은 프록시가 설정하는 파라미터이며, 클라이언트가 아무리 `REMOTE_ADDR`처럼 보이는 헤더를 보내도 FastCGI 레이어에서 `HTTP_REMOTE_ADDR`로 변환되어 `REMOTE_ADDR`과 충돌할 수 없다. 이 분리는 규칙이 아니라 구조에서 나온다.

### HTTP가 내부 통신에서 “이겼던” 이유

nostrademons는 FastCGI vs SCGI vs HTTP 선택의 역사를 설명했다.[^nostrademons] HTTP가 내부 통신에서도 표준이 된 이유는 단순성이었다. 별도의 프로토콜 없이 동일한 도구, 동일한 스택으로 외부·내부 통신을 모두 처리할 수 있다는 편의성이 기술적 우위를 앞섰다. curl로 백엔드를 직접 테스트할 수 있고, 브라우저로 바로 접근할 수 있으며, 와이어샤크(Wireshark)로 패킷을 읽을 수 있다. 이것은 End-to-End 원칙과 최소 권한 원칙(Principle of Least Privilege) 사이의 트레이드오프다. “E2E는 유연성을 주지만, 유연성은 누군가 그것을 악용할 가능성을 만든다.”

athrowaway3z는 더 직접적인 반론을 제기했다. HTTP/2가 프레이밍 문제를 동일하게 해결하므로 FastCGI 대신 HTTP/2를 쓰면 된다는 것이다.[^athrowaway3z] 기술적으로 타당한 지적이다. 그러나 HTTP/2도 헤더 인젝션 문제는 여전히 해결하지 않는다. 프레이밍 문제와 도메인 분리 문제는 별개다.

### SCGI, WSGI, ASGI, uWSGI 비교

FastCGI 외에도 유사한 목적의 프로토콜이 여럿 존재한다. SCGI(Simple Common Gateway Interface)는 2006년 Neil Schemenauer가 설계했다. FastCGI와 달리 텍스트 기반 넷스트링(netstring) 인코딩을 사용해 구현이 더 단순하지만, FastCGI의 멀티플렉싱을 지원하지 않는다. 연결당 하나의 요청만 처리한다. est는 uWSGI 프로토콜을 언급했는데,[^est] uWSGI는 Python 생태계에서 Nginx와 Python 앱 사이의 통신에 주로 쓰이며 “RPC for basically everything”으로 확장됐다.

blipvert가 (u)WSGI를 언급했듯,[^blipvert] WSGI(Web Server Gateway Interface)는 파이썬 표준(PEP 3333)으로 프로토콜이 아니라 파이썬 객체 인터페이스 규약이다. 서버가 파이썬 callable을 직접 호출하므로 네트워크 프로토콜이 없다. ASGI(Asynchronous Server Gateway Interface)는 WSGI의 비동기 확장으로 WebSocket을 지원한다. Django Channels, Starlette, FastAPI가 여기 속한다. 이들은 모두 특정 언어 생태계에 묶여 있는 반면, FastCGI는 언어 독립적인 와이어 프로토콜이다.

### PHP-FPM이 입증하는 FastCGI의 현역 지위

chasil은 Red Hat 계열 리눅스 배포판의 PHP 기본 설정이 “PHP FastCGI Process Manager(FPM)”라는 점을 지적했다.[^chasil] FastCGI가 레거시 기술이 아니라 현재도 웹 호스팅 인프라의 실질적 기반이라는 반증이다. PHP-FPM은 수백만 개의 웹 서버에서 nginx와 FastCGI로 연결돼 동작하고 있다. daneel_w는 Perl과 `FCGI::ProcManager`로 FastCGI 백엔드를 nginx 앞에 놓는 구성을 “pleasantly simple, incredibly robust and high-performing”으로 평가했다.[^daneel_w]

### WAS: 더 나아간 프로토콜

max_k는 FastCGI도 충분하지 않다고 판단해 16년 전 직접 설계한 WAS(Web Application Socket)를 소개했다.[^max_k] WAS는 메인 소켓에 벌크 데이터를 프레임으로 패킹하는 대신, 제어 소켓과 두 개의 파이프(요청/응답 바디)를 분리한다. 양쪽에서 `splice()`를 사용해 파이프를 직접 조작할 수 있고, 프레이밍이 필요 없으며 요청 취소도 가능하다. 오픈소스로 공개되어 있으며 실제 웹 호스팅 환경에서 대규모로 사용 중이다.

### HTTP/2와 HTTP/3는 이 문제를 해결했는가

HTTP/2는 바이너리 프레이밍 레이어를 도입해 요청 스머글링의 프레이밍 측면을 해결했다. HTTP/3는 QUIC 위에서 동작해 TCP 헤드오브라인 블로킹(head-of-line blocking) 문제도 해결한다. 그러나 두 프로토콜 모두 헤더 도메인 분리 문제는 해결하지 않는다. `X-Real-IP` 인젝션 공격은 HTTP/2 환경에서도 동일하게 발생할 수 있다. 또한 내부 통신에서 HTTP/2를 사용하려면 서버 측이 HTTP/2를 지원해야 하며, 많은 언어의 HTTP 서버 라이브러리가 HTTP/1.1만 지원한다는 현실적 제약이 있다. FastCGI는 이미 1996년에 바이너리 프레이밍을 갖추고 있었고, 내부 통신에 최적화된 도메인 분리까지 제공한다.

### CGI의 부활: 에이전트 코딩의 새 맥락

nzoschke는 흥미로운 역설을 제시했다. FastCGI도 아닌 일반 CGI가 에이전트 코딩 맥락에서 재발견되고 있다는 것이다.[^nzoschke] 플랫폼 위에서 사용자들이 커스텀 페이지를 바이브 코딩(vibe coding)으로 만들 때, 에이전트가 `page-name/main.go`를 CGI로 구현하고 서버가 요청을 위임하는 구조가 실용적으로 작동한다. Go의 표준 라이브러리가 서버 측과 사용자 공간 모두에서 CGI를 잘 지원한다. 트래픽이 적은 개인용 도구에서는 FastCGI의 최적화도 불필요하다. shevy-java는 CGI를 “현대화”해 동작하는 것만 취하고 복잡성을 배제하는 방향을 제안했다.[^shevy_java] “낡은 것이 에이전트 시대에 새로워진다.”

## 비평

### 강점: 보안 관점의 프로토콜 분석

이 글의 가장 큰 가치는 “왜 HTTP/1.1이 내부 통신에서 위험한가”를 구체적인 공격 시나리오(요청 스머글링, 헤더 인젝션)와 실제 사례(Discord 취약점)로 설명한다는 점이다. FastCGI 채택을 강요하는 것이 아니라, HTTP를 맹목적으로 재사용하는 관성의 보안 비용을 명확히 제시한다. SSLMate가 FastCGI를 10년 이상 프로덕션에서 운용했다는 실증도 설득력을 더한다.

### 약점: WebSocket 미지원의 현실적 한계

FastCGI의 최대 단점은 WebSocket 미지원이다. simonw는 WebSocket 부재를 아쉬워하면서도 SSE(Server-Sent Events)는 지원 가능할 것이라고 지적했다.[^simonw] SSE는 결국 느린 스트리밍 HTTP 응답이기 때문이다. Tepix는 WebTransport가 새로운 대안이 될 수 있다고 언급했지만,[^tepix] 현실적으로 FastCGI 대체재가 되기엔 멀다. 실시간 양방향 통신이 필수적인 애플리케이션에서는 FastCGI만으로는 충분하지 않다.

HTTP/2의 서버 푸시(Server Push)나 SSE 같은 단방향 스트리밍은 FastCGI 위에서도 이론적으로 구현 가능하다. 그러나 WebSocket처럼 전이중(full-duplex) 연결이 필요한 경우 FastCGI는 구조적 한계를 가진다. apitman이 대안으로 제시한 HTTP 스트리밍(WHATWG Streams API를 활용한 바이트 스트림에 헤더만 추가하는 방식)은 기술적으로 가능하지만,[^apitman] 생태계 지원이 WebSocket에 비할 수 없다.

### 약점: 도구 생태계의 격차

tombert처럼 직접 FastCGI를 사용해본 경험이 있어도 현대 프로젝트에서는 “선택지에 들어오지 않았다”고 말하는 것이 일반적이다.[^tombert] curl이 FTP, Gopher, SMTP를 지원하면서도 FastCGI를 지원하지 않는다는 점은 상징적이다. 디버깅 도구 생태계가 HTTP에 비해 빈약하다. sscaryterry의 “Perl + Windows + Apache + FastCGI 조합은 다시는 하고 싶지 않다”는 발언은[^sscaryterry] 도구 성숙도의 차이를 보여준다. 기술적 우위가 있어도 도구 생태계의 격차가 실제 채택을 막는다.

### 약점: PATH_INFO의 표현력 손실

runxiyu는 FastCGI가 CGI/1.1의 `PATH_INFO` 처리를 그대로 상속한다는 점을 지적했다.[^runxiyu] `PATH_INFO`는 URL 디코딩 후의 값을 전달하므로, 인코딩된 슬래시(`%2F`)를 그대로 보존할 수 없다. 일부 구현체는 경로에서 `//`를 `/`로 정규화하기도 한다. 이는 HTTP를 직접 사용하는 것보다 표현력이 제한된 경우다. 정확한 URL 처리가 중요한 애플리케이션에서는 의미 있는 제약이다.

### 성능 특성 분석

Ayer는 일부 워크로드에서 FastCGI가 HTTP/1.1이나 HTTP/2보다 처리량이 낮다고 솔직하게 인정한다. 다만 이는 프로토콜 자체의 한계가 아니라 최적화 불균형 때문이라고 분석한다. HTTP 스택은 수십 년간 최적화됐지만 FastCGI 구현체는 상대적으로 방치됐다. FastCGI의 멀티플렉싱은 이론적으로 연결 수를 줄여 성능을 높일 수 있지만, 이를 충분히 활용하는 구현체가 드물다. 고트래픽 환경에서는 벤치마크를 통해 직접 확인이 필요하다. 대부분의 서비스에서는 “충분히 빠른(fast enough)” 수준이다.

## 인사이트

### 내부 통신 프로토콜 선택이 보안 아키텍처에 미치는 영향

애플리케이션 레이어 보안에 집중하는 동안, 프록시-백엔드 사이의 내부 통신 프로토콜은 “어차피 내부 네트워크”라는 이유로 간과되는 경향이 있다. 그러나 HTTP/1.1의 파싱 불확실성은 내부 통신을 공격 표면으로 만든다. Discord 미디어 프록시 취약점이 보여주듯, 보안 경계를 통과한 요청이라도 프록시와 백엔드 사이의 프로토콜 불일치가 새로운 취약점을 만든다.

최소 권한 원칙(Principle of Least Privilege)을 프로토콜 선택에 적용한다는 것은, 내부 서비스 간 통신에서 일반 HTTP보다 더 제한적인 프로토콜을 의도적으로 선택하는 것을 의미한다. WAF나 인증 레이어보다 근본적인 수준의 보안 투자다. 공격자가 악용할 수 있는 유연성 자체를 줄이는 것이 가장 근본적인 보안 대책이다.

보안 아키텍처 설계에서 “네트워크 경계 내부는 신뢰한다”는 가정은 이미 제로 트러스트(Zero Trust)로 대체되고 있다. 프로토콜 선택도 같은 맥락에서 봐야 한다. “이 프로토콜이 공격자에게 어떤 유연성을 제공하는가”라는 질문이 “이 프로토콜이 개발자에게 얼마나 편리한가”보다 먼저 와야 하는 상황이 있다. FastCGI의 도메인 분리는 헤더 인젝션 공격 클래스 전체를 차단한다. 이것은 코드 레벨의 방어가 아니라 프로토콜 레벨의 방어다.

물론 이 관점을 과도하게 확장할 위험도 있다. 모든 내부 통신을 FastCGI로 교체하라는 것이 아니다. 핵심은 의식적 선택이다. HTTP를 내부 통신에 쓰는 것이 “기본값이라서”가 아니라, 그 보안 트레이드오프를 이해하고 수용하는 명시적 결정이어야 한다.

### “한 가지 도구로 모든 것을” vs “목적에 맞는 도구” — HTTP 범용주의의 함정

HTTP는 웹의 공용어가 됐다. 서비스 간 통신(REST, gRPC-Web), 파일 전송, 실시간 통신(WebSocket), 이벤트 스트리밍(SSE), 심지어 데이터베이스 쿼리(CouchDB, Elasticsearch)까지 HTTP 위에서 구현된다. 이 범용성은 진정한 강점이다. 하나의 프로토콜 스택, 하나의 디버깅 도구, 하나의 보안 검토 과정으로 모든 것을 처리할 수 있다.

그러나 범용성은 동시에 취약점의 원천이다. HTTP/1.1의 `Content-Length`와 `Transfer-Encoding` 공존, 헤더 이름의 대소문자 무감별(case-insensitive), 공백 처리의 모호성 — 이 유연성들이 각각 공격 벡터가 된다. 프로토콜이 더 많은 경우를 처리하려 할수록 엣지 케이스가 늘어나고, 구현체 간 불일치 가능성이 높아진다. FastCGI나 SCGI, WAS는 훨씬 좁은 문제를 해결한다. 프록시와 애플리케이션 사이의 단순한 요청/응답 위임. 이 단순성이 보안의 원천이다.

소프트웨어 공학에서 “단일 책임 원칙(Single Responsibility Principle)”은 코드 설계 원칙이지만, 프로토콜 설계에도 적용된다. HTTP가 외부 클라이언트와의 통신에 최적화된 프로토콜이라면, 내부 서비스 간 통신은 그에 맞는 별도의 프로토콜을 쓰는 것이 더 적합할 수 있다. 이것은 복잡성을 더하는 것이 아니라, 복잡성을 분리하는 것이다.

nostrademons가 말한 “E2E는 유연성을 주지만, 유연성은 악용 가능성을 만든다”는 통찰은 프로토콜 선택을 넘어 시스템 설계 일반에 적용된다. 통합의 편의성과 분리의 안전성 사이에서 의식적으로 선택해야 한다. “다 HTTP로”라는 결정은 편의성을 선택한 것이지, 보안을 검토한 것이 아니다.

### 30년 된 기술이 현대 보안 요구를 충족하는 역설 — 기술 선택의 역사적 교훈

FastCGI가 1996년에 이미 바이너리 프레이밍과 도메인 분리를 갖추고 있었다는 사실은 아이러니하다. HTTP/2가 2015년에 바이너리 프레이밍을 도입했을 때, 그것은 “혁신”으로 받아들여졌다. 그러나 FastCGI는 19년 전에 같은 문제를 이미 해결해 놓았다. 기술의 나이와 기술의 적합성은 무관하다.

이 역설이 드러내는 것은 기술 생태계의 관성이다. 더 나은 해결책이 존재해도 채택되지 않는 이유는 여러 가지다. 도구 생태계의 부재(curl이 FastCGI를 지원하지 않는다), 익숙함의 편향(개발자는 이미 아는 것을 쓴다), 네트워크 효과(모두가 HTTP를 쓰므로 HTTP 도구가 발전한다). 기술적 우위가 있어도 채택되지 않는 기술은, 기술적으로는 승리했지만 생태계 전쟁에서 패배한 것이다.

역사적 교훈은 반복된다. XMPP는 오늘날 Slack이 하는 것을 2000년대 초에 이미 할 수 있었다. TCP/IP와 경쟁했던 OSI 프로토콜 스택은 기술적으로 더 정교했지만 사라졌다. 더 좋은 기술이 반드시 이기지는 않는다. 그러나 “이 기술이 충분히 넓게 채택됐는가”와 “이 기술이 내 특정 문제에 가장 적합한가”는 다른 질문이다. 보안이 핵심 요구사항인 환경에서, “모두가 쓴다”는 이유만으로 HTTP를 내부 통신에 쓰는 것은 질문 자체를 생략한 것이다.

HTTP/2, HTTP/3의 등장에도 불구하고 FastCGI가 여전히 의미 있는 이유는, 그것이 해결하는 문제(리버스 프록시와 애플리케이션 서버 사이의 신뢰된 통신)가 여전히 존재하기 때문이다. 30년 된 해결책이 현대적 문제를 해결한다면, 그 해결책은 낡은 것이 아니라 근본적인 것이다.

### 에이전트 시대의 CGI 부활 — nzoschke 사례에서 본 패러다임 전환

nzoschke의 사례는 단순한 향수(nostalgia)가 아니다. CGI의 핵심 특성, 즉 요청마다 독립적인 프로세스를 실행한다는 것이, 에이전트 생성 코드의 격리(isolation) 요구와 정확히 맞아떨어진다. AI 에이전트가 사용자를 위해 코드를 생성하고 실행할 때, 각 코드가 격리된 환경에서 실행되어야 한다는 요구가 있다. CGI는 이것을 무료로 제공한다. 모든 요청이 새 프로세스이므로 상태 누출이 없다.

성능 최적화를 포기하는 대신 단순성을 얻는다는 트레이드오프는, 에이전트 시대에 다른 의미를 가진다. 에이전트가 코드를 작성할 때, 그 코드는 최고 성능보다 정확성과 격리가 더 중요한 경우가 많다. “person scale”(개인 규모) 데이터와 페이지 뷰를 처리하는 도구에서는 CGI의 프로세스당 요청 처리가 완전히 충분하다. 트래픽이 작으면 성능 페널티가 없고, 격리의 이점만 남는다.

더 넓게 보면, 이것은 “레이어별 최적화”라는 엔지니어링 원칙의 사례다. 시스템 전체를 동일한 최적화 기준으로 설계할 필요가 없다. 고트래픽 API는 FastCGI나 HTTP/2로, 저트래픽 커스텀 사용자 페이지는 CGI로, 이것은 합리적인 분리다. 에이전트 생성 코드가 CGI로 실행된다면 에이전트는 `net/http/cgi` 표준 라이브러리만 이해하면 되고, 복잡한 서버 구성 없이 동작하는 코드를 만들 수 있다. 이 단순성은 에이전트의 코드 생성 품질을 높인다.

shevy-java가 CGI를 “현대화”해 동작하는 것만 취하자고 한 제안은, 에이전트 시대에 더욱 설득력 있다. 표준화된 환경 변수 인터페이스, 표준 입출력을 통한 요청/응답, 프로세스 격리 — 이 세 가지만으로도 에이전트가 사용자 맞춤 도구를 만드는 데 충분한 토대가 된다. FastCGI가 CGI를 “빠르게” 만든 것처럼, 에이전트 시대에는 “에이전트 친화적으로” 만드는 것이 다음 진화 방향일 수 있다.

---

[^nostrademons]: <https://news.ycombinator.com/item?id=47951539>
[^chasil]: <https://news.ycombinator.com/item?id=47951939>
[^max_k]: <https://news.ycombinator.com/item?id=47952605>
[^nzoschke]: <https://news.ycombinator.com/item?id=47952838>
[^apitman]: <https://news.ycombinator.com/item?id=47953127>
[^tombert]: <https://news.ycombinator.com/item?id=47951364>
[^athrowaway3z]: <https://news.ycombinator.com/item?id=47952912>
[^simonw]: <https://news.ycombinator.com/item?id=47952581>
[^tepix]: <https://news.ycombinator.com/item?id=47952846>
[^est]: <https://news.ycombinator.com/item?id=47956649>
[^blipvert]: <https://news.ycombinator.com/item?id=47955704>
[^daneel_w]: <https://news.ycombinator.com/item?id=47953695>
[^sscaryterry]: <https://news.ycombinator.com/item?id=47951825>
[^runxiyu]: <https://news.ycombinator.com/item?id=47956303>
[^shevy_java]: <https://news.ycombinator.com/item?id=47952150>
