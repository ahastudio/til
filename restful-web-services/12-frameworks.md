# 12장 RESTful 서비스를 위한 프레임워크

《RESTful Web Services》(Leonard Richardson, Sam Ruby, O'Reilly 2007) 12장 정리.

## 개요

REST 설계 철학이 인기를 얻으면서 RESTful 설계를 쉽게 만들어 주는 새 프레임워크가 등장하고, 기존 프레임워크도 RESTful 모드와 기능을 갖추기 시작했다.
이 장은 세 가지 인기 프레임워크에서 리소스 지향 서비스를 작성하는 방법을 다룬다.
Ruby on Rails, Restlet(Java용), Django(Python용)가 그 대상이다.

1장에서 저자는 REST가 아키텍처가 아니라 아키텍처를 판단하는 방식이라고 설명했다.
반면 리소스 지향 아키텍처(ROA)는 실제 아키텍처로서, 문제를 RESTful 리소스로 분해하기 쉽게 만드는 제약을 사고에 부과한다.
그러나 이 리소스들은 추상적 수준에서만 존재하며, 구체적인 웹 서비스로 노출되기 전까지는 실체가 없다.

CGI 스크립트처럼 서비스를 처음부터 작성한다면 리소스를 원하는 대로 코드로 옮길 수 있다.
그러나 대부분의 서비스는 웹 프레임워크로 작성된다.
REST를 인식하는 웹 프레임워크는 특정 프로그래밍 언어에서 RESTful 리소스를 쉽게 구현하도록 프로그래밍에 제약을 부과한다.
이 장의 목표는 책 전반의 교훈을 실제 프레임워크와 통합하는 것이다.

이 책은 2007년에 출간되었으며, 여기서 다루는 프레임워크의 버전과 API도 그 시점 기준이다.
Rails는 1.2, Restlet은 1.0, Django는 정식 1.0 이전의 초기 버전을 전제로 한다.
따라서 구체적인 클래스명, 메서드명, 설정 파일 문법 등은 당시 버전의 것이며 이후 버전과 다를 수 있다.

## Ruby on Rails

Rails의 성공을 이끈 핵심 동력은 “단순화 가정(simplifying assumption)”이다.
Rails는 상상할 수 있는 모든 작업을 위한 수많은 도구를 주는 대신, 다양한 공통 작업을 한 가지 방식으로 처리하도록 해 준다.
관계형 데이터베이스의 데이터를 노출하려는 경우, 테이블 이름과 구조가 일정한 규칙을 따르는 경우, MVC(Model-View-Controller) 아키텍처를 쓰려는 경우라면 애플리케이션을 매우 빠르게 만들 수 있다.
웹 애플리케이션 영역의 많은 문제가 이 가정에 들어맞기 때문에, 그 제약은 부담이 되기보다 오히려 해방감을 준다.

초기 버전의 Rails는 전형적인 REST-RPC 하이브리드 아키텍처를 노출했지만, Rails 1.2는 더 RESTful한 설계에 집중한다.
HTTP의 균일 인터페이스(uniform interface) 역시 또 하나의 단순화 가정이므로, 이러한 방향 전환은 어쩌면 필연적이었다.

### 라우팅

HTTP 요청이 들어오면 Rails는 요청된 URI를 분석해 적절한 컨트롤러 클래스로 요청을 라우팅한다.
어떤 요청을 어떻게 처리할지는 `config/routes.rb` 파일이 Rails에 알려 준다.

```ruby
# routes.rb

ActionController::Routing::Routes.draw do |map|
  map.resources :weblogs do |weblog|
    weblog.resources :entries
  end
end
```

이 파일은 두 개의 컨트롤러 클래스(`WeblogsController`와 `EntriesController`)의 존재를 선언하고, 들어오는 요청을 그 클래스들로 라우팅하는 방법을 Rails에 알려 준다.
`WeblogsController`는 URI `/weblogs`와 `/weblogs/{id}` 형태의 모든 URI에 대한 요청을 처리한다.
경로 변수 `{id}`가 존재하면 `params[:id]`로 사용할 수 있다.

`EntriesController`는 `/weblogs/{weblog_id}/entries`와 `/weblogs/{weblog_id}/entries/{id}` 형태의 URI를 처리한다.
경로 변수 `{weblog_id}`는 `params[:weblog_id]`로, `{id}`가 있으면 `params[:id]`로 사용할 수 있다.

`{id}`나 `{weblog_id}` 같은 변수는 보통 리소스를 시스템 내의 특정 객체와 연결하는 데 쓰인다.
이 변수들은 데이터베이스 ID에 대응하는 경우가 많으며 ActiveRecord의 `find` 메서드에 전달된다.
저자의 del.icio.us 클론에서는 `{username}`처럼 서술적인 이름을 붙이고, 이를 ID가 아닌 식별용 이름으로 사용했다.

### 리소스, 컨트롤러, 뷰

모든 Rails 컨트롤러는 두 종류의 리소스를 노출할 수 있다.
하나는 GET 또는 POST에 응답하는 단일 “목록(list)” 또는 “팩토리(factory)” 리소스이고, 다른 하나는 GET, PUT, DELETE에 응답하는 다수의 “객체(object)” 리소스다.
목록 리소스는 흔히 데이터베이스 테이블에, 객체 리소스는 그 테이블의 각 행에 대응한다.

각 컨트롤러는 Ruby 클래스이므로, 클래스에 HTTP 요청을 “보낸다”는 것은 특정 메서드를 호출한다는 뜻이다.
Rails는 컨트롤러마다 다섯 개의 표준 메서드를 정의하고, 여기에 더해 두 개의 특수 뷰 템플릿을 HTTP GET으로 노출한다.
`map.resources :weblogs` 호출로 가능해지는 일곱 개의 HTTP 요청은 다음과 같다.

- `GET /weblogs`: weblog 목록. Rails가 `WeblogsController#index`를 호출한다.
- `GET /weblogs/new`: 새 weblog를 만드는 폼. Rails가 `app/views/weblogs/new.rhtml` 뷰를 렌더링한다. 이 뷰는 클라이언트가 새 weblog를 만들기 위해 어떤 HTTP 요청을 해야 하는지를 기술하는 하이퍼미디어 파일이며, 실제로는 HTML 폼(또는 작은 WADL 파일)이다. 폼은 클라이언트가 `/weblogs`로 POST 요청을 보내야 한다고 알려 주고, 표현을 어떻게 포맷해야 서버가 이해할 수 있는지도 알려 준다.
- `POST /weblogs`: 새 weblog 생성. Rails가 `WeblogsController#create`를 호출한다.
- `GET /weblogs/{id}`: 하나의 weblog. Rails가 `WeblogsController#show`를 호출한다.
- `GET /weblogs/{id};edit`: weblog 상태를 편집하는 폼. Rails가 `app/views/weblogs/edit.rhtml`을 렌더링한다. 이 하이퍼미디어 파일(HTML 폼 또는 짧은 WADL 파일)은 클라이언트가 `/weblogs/{id}`로 PUT 요청을 보내거나 이를 시뮬레이션하는 방법을 알려 준다.
- `PUT /weblogs/{id}`: weblog 상태 변경. Rails가 `WeblogsController#update`를 호출한다. 여기서 “상태”란 weblog 이름이나 저자 연락처처럼 이 리소스에 결부된 상태를 말한다. 개별 항목(entry)은 별도의 리소스로 노출된다.
- `DELETE /weblogs/{id}`: weblog 삭제. Rails가 `WeblogsController#delete`를 호출한다.

모든 컨트롤러에서 일곱 개의 접근점을 전부 노출할 필요는 없다.
특히 웹 서비스를 웹 사이트로도 운영하는 것이 아니라면 특수 뷰(new/edit 폼)는 쓰지 않게 된다.
노출하고 싶지 않은 메서드나 뷰 파일은 그냥 구현하지 않으면 된다.

### 나가는 표현(Outgoing Representations)

Rails는 클라이언트 요청에 따라 리소스의 서로 다른 표현을 보내기 쉽게 해 준다.
어떤 표현을 보낼지는 클라이언트가 접근한 URI 또는 `Accept` 헤더에 담긴 값에 따라 결정된다.
예를 들어 `/weblogs/1.html`에 접근하면 HTML 표현을, `/weblogs/1.png`에 접근하면 그래픽 PNG 표현을 받는다.
`respond_to` 함수가 클라이언트의 능력과 요구를 해석해 주며, 개발자는 지원하는 옵션을 우선순위 순서대로 구현하기만 하면 된다.

```ruby
respond_to do |format|
  format.html { render :template => 'weblogs/show' }
  format.xml  { render :xml => weblog.to_xml }
  format.png  { render :text => weblog.generate_image,
                       :content_type => "image/png" }
end
```

특히 흔한 두 가지 표현 형식은 HTML과 ActiveResource XML 직렬화 형식이다.
HTML 표현은 사람 대상 웹 애플리케이션에서처럼 Rails 뷰로 표현한다.
ActiveRecord 객체를 XML 문서로 노출하려면 객체 하나 또는 객체 목록에 대해 `to_xml`을 호출하면 된다.

Rails 플러그인을 쓰면 다른 표현 형식으로 데이터를 노출하기도 쉽다.
7장에서는 `atom-tools` Ruby gem을 설치해 북마크 목록을 Atom 피드로 렌더링했고, `respond_to` 블록 안에서 Atom 요청과 일반 XML 요청을 구분하는 절을 두었다.

### 들어오는 표현(Incoming Representations)

Rails는 자신의 역할을 들어오는 표현을 키-값 쌍의 묶음으로 바꾸고, 그 쌍들을 `params` 해시로 제공하는 것으로 본다.
기본적으로 Rails는 웹 브라우저가 보내는 form-encoded 문서와 `to_xml`이 생성하는 단순한 XML 문서를 파싱할 줄 안다.

직접 정의한 표현 형식에 대해 같은 동작을 얻고 싶다면 `ActionController::Base.param_parsers` 해시에 새 `Proc` 객체를 추가하면 된다.
이 `Proc` 객체는 특정 미디어 타입의 들어오는 표현을 처리하는 코드 블록이다.
자세한 내용은 `param_parsers` 해시에 대한 Rails 문서를 참고하면 된다.

### 웹 서비스로서의 웹 애플리케이션

Rails 1.2는 사람의 웹(human web)과 프로그래머블 웹(programmable web)을 훌륭하게 통합한다.
Rails에는 데이터베이스 테이블을 리소스 집합으로 노출하는 `scaffold_resource`라는 코드 생성기가 있다.
이렇게 생성된 서비스는 웹 브라우저로도, ActiveResource 같은 웹 서비스 클라이언트로도 접근할 수 있다.

웹 브라우저로 `scaffold_resource` 서비스에 접근하면 데이터베이스 객체의 HTML 표현과, 이를 조작하는 HTML 폼(앞서 언급한 `new.rhtml`과 `edit.rhtml`이 생성)을 받는다.
form-encoded 형식으로 새 표현을 보내 리소스를 생성, 수정, 삭제할 수 있으며, PUT과 DELETE 요청은 오버로드된 POST로 시뮬레이션된다.

웹 서비스 클라이언트로 접근하면 데이터베이스 객체의 XML 표현을 받는다.
XML 문서를 수정한 뒤 PUT으로 되돌려 보내 객체를 조작하며, 오버로드되지 않은 POST와 DELETE도 기대한 대로 동작한다.

이는 사람의 웹과 프로그래머블 웹이 근본적으로 유사함을 보여 주는 좋은 사례다.
동일한 일을 하는 웹 사이트와 웹 서비스를 함께 설계한다면, Rails는 둘을 같은 기반 코드의 두 측면으로 손쉽게 노출할 수 있다.

### Rails/ROA 설계 절차

6장의 일반 설계 절차를 Rails에 맞게 수정한 절차는 다음과 같다.
핵심 차이는 데이터셋을 곧바로 리소스로 나누는 대신, 데이터셋을 컨트롤러로 나누고 컨트롤러를 리소스로 나눈다는 점이다.
이렇게 하면 Rails의 컨트롤러 체계에 맞지 않는 리소스가 생길 가능성이 줄어든다.

1. 데이터셋을 파악한다.
2. 데이터셋을 컨트롤러에 할당한다. 각 컨트롤러에 대해 다음을 검토한다.
   - 이 컨트롤러는 목록 또는 팩토리 리소스를 노출하는가?
   - 이 컨트롤러는 객체 리소스의 집합을 노출하는가?
   - 이 컨트롤러는 생성 폼 또는 편집 폼 리소스를 노출하는가?

목록 리소스와 객체 리소스에 대해서는 다음을 수행한다.

- 클라이언트로부터 받는 표현을 설계한다(Rails 표준과 다를 경우).
- 클라이언트에 제공하는 표현을 설계한다.
- 이 리소스를 기존 리소스와 연결한다.
- 정상적인 진행 과정을 검토한다. 9장의 데이터베이스 기반 제어 흐름이 도움이 된다.
- 오류 조건을 검토한다. 무엇이 잘못될 수 있는지 역시 데이터베이스 기반 제어 흐름을 활용할 수 있다.

## Restlet

작성: Jerome Louvel, Dave Pawson

Restlet 프로젝트(<http://www.restlet.org>)는 REST 개념을 Java 클래스에 매핑하는 가볍지만 포괄적인 프레임워크를 제공한다.
RESTful 웹 서비스뿐 아니라 모든 종류의 RESTful 시스템을 구현하는 데 쓸 수 있으며, 2005년 출범 이래 신뢰할 만한 소프트웨어로 자리 잡았다.

Restlet은 Servlet API, Java Server Pages, `HttpURLConnection`, Struts 등 Java의 다른 주요 웹 애플리케이션 기술의 영향을 받았다.
프로젝트의 주요 목표는 이들과 같은 수준의 기능을 제공하면서도 Fielding 논문에 제시된 REST의 목표에 더 가깝게 머무는 것이다.
또 다른 핵심 목표는 클라이언트 측과 서버 측 애플리케이션 모두에 적합한, 웹에 대한 통합된 관점을 제시하는 것이다.

Restlet의 철학은 HTTP 클라이언트와 HTTP 서버의 구분이 아키텍처적으로 중요하지 않다는 것이다.
하나의 소프트웨어가 두 개의 완전히 다른 API를 쓰지 않고도 웹 클라이언트로, 또 웹 서버로 동작할 수 있어야 한다.
이는 표준 Java API의 결함, 즉 `HttpURLConnection` 클래스가 서블릿과 전혀 닮지 않았다는 Benjamin Carlyle의 지적을 따른 것이다.

초기에 소프트웨어는 Restlet API와 참조 구현인 Noelios Restlet Engine(NRE)으로 분리되었다.
이 분리 덕분에 다른 구현체들도 같은 API와 호환될 수 있다.
NRE에는 인기 있는 오픈 소스 Java 프로젝트에 기반한 여러 HTTP 서버 커넥터(Mortbay의 Jetty, Codehaus의 AsyncWeb, Simple 프레임워크)가 포함되며, Apache Tomcat 같은 표준 서블릿 컨테이너 안에 Restlet 애플리케이션을 배포하게 해 주는 어댑터도 있다.

Restlet은 두 개의 HTTP 클라이언트 커넥터도 제공한다.
하나는 공식 `HttpURLConnection` 클래스에, 다른 하나는 Apache의 HTTP 클라이언트 라이브러리에 기반한다.
또 다른 커넥터는 JDBC 소스를 XML 문서를 통해 RESTful하게 조작하게 해 주고, JavaMail API에 기반한 SMTP 커넥터는 XML 문서로 이메일을 보낼 수 있게 해 준다.

Restlet API는 문자열, 파일, 스트림, 채널, XML 문서를 기반으로 표현을 만드는 클래스를 포함한다.
파싱에는 SAX와 DOM을, 변환에는 XSLT를 지원한다.
FreeMarker나 Apache Velocity 템플릿 엔진을 이용하면 JSP 방식의 템플릿 기반 표현을 쉽게 만들 수 있다.
콘텐츠 협상을 지원하는 `Directory` 클래스를 쓰면 일반 웹 서버처럼 정적 파일과 디렉터리를 제공할 수도 있다.

프레임워크 전반의 설계 원칙은 단순성과 유연성이다.
API는 HTTP, URI, REST의 개념을 일관된 클래스 집합으로 추상화하되, 원시 HTTP 헤더 같은 저수준 정보를 완전히 숨기지는 않는다.

### 기본 개념

Restlet의 용어는 Fielding 논문의 REST 용어(리소스, 표현, 커넥터, 컴포넌트, 미디어 타입, 언어 등)와 일치한다.
Restlet은 여기에 `Application`, `Filter`, `Finder`, `Router`, `Route` 같은 특화된 클래스를 더해, 여러 restlet을 서로 결합하고 들어오는 요청을 그것을 처리해야 할 리소스로 매핑하기 쉽게 만든다.

Restlet의 중심 개념은 추상 클래스 `Uniform`과 그 구체적 하위 클래스 `Restlet`이다.
이름 그대로 `Uniform`은 REST가 정의하는 균일 인터페이스를 노출한다.
이 인터페이스는 HTTP의 균일 인터페이스에서 영감을 받았지만 FTP, SMTP 같은 다른 프로토콜에도 쓸 수 있다.

주요 메서드는 `handle`로, `Request`와 `Response` 두 인자를 받는다.
네트워크를 통해 노출되는 모든 호출 핸들러는(클라이언트든 서버든) `Restlet`의 하위 클래스, 즉 하나의 restlet이며 이 균일 인터페이스를 따른다.
이 균일 인터페이스 덕분에 restlet들을 매우 정교하게 조합할 수 있다.

Restlet이 지원하는 모든 프로토콜은 `handle` 메서드를 통해 노출된다.
HTTP(서버와 클라이언트), HTTPS, SMTP는 물론 JDBC, 파일 시스템, 심지어 클래스 로더까지 모두 `handle`을 거친다.
이는 개발자가 배워야 할 API의 수를 줄여 준다.

필터링, 보안, 데이터 변환, 라우팅은 `Restlet`의 하위 클래스들을 서로 연결(chaining)해 처리한다.
`Filter`는 다음 restlet이 호출을 처리하기 전이나 후에 처리를 수행할 수 있다.
`Filter` 인스턴스는 Rails 필터처럼 동작하지만, 필터 전용 API가 아니라 다른 Restlet 클래스와 동일한 `handle` 메서드에 응답한다.

`Router` restlet에는 여러 `Restlet` 객체가 붙어 있으며, 들어오는 각 프로토콜 호출을 적절한 `Restlet` 핸들러로 라우팅한다.
라우팅은 대개 Rails처럼 대상 URI의 어떤 측면을 기준으로 이루어진다.
다만 Rails와 달리 Restlet은 리소스 계층 구조에 어떠한 URI 관례도 강요하지 않는다.
`Router`를 적절히 프로그래밍하기만 하면 URI를 원하는 대로 구성할 수 있다.

`Router`는 이 흔한 용법을 넘어설 수도 있다.
여러 원격 머신 사이에서 동적 부하 분산으로 호출을 프록시하는 데 `Router`를 쓸 수 있으며, 이런 복잡한 구성조차 여전히 Restlet의 균일 인터페이스에 응답하므로 더 큰 라우팅 시스템의 구성 요소로 쓸 수 있다.
`Router`의 하위 클래스인 `VirtualHost`를 쓰면 같은 물리 머신에서 여러 도메인 이름 아래 여러 애플리케이션을 호스팅할 수 있다.
전통적으로 이런 기능을 얻으려면 Apache httpd 같은 프런트엔드 웹 서버가 필요했지만, Restlet에서는 균일 인터페이스에 응답하는 또 하나의 `Router`일 뿐이다.

`Application` 객체는 이식 가능한 restlet 집합을 관리하고 공통 서비스를 제공할 수 있다.
여기서 “서비스”란 압축된 요청의 투명한 디코딩이나, `method` 쿼리 파라미터로 오버로드된 POST 위에 PUT/DELETE 같은 메서드를 터널링하는 것 등을 말한다.
마지막으로 `Component` 객체는 여러 커넥터, `VirtualHost`, `Application`을 담고 조율하며, 독립 실행형 Java 애플리케이션으로 실행하거나 J2EE 환경 같은 더 큰 시스템에 임베드할 수 있다.

Restlet은 어떤 단순화 가정도 하지 않기 때문에, 6장의 설계 절차를 Rails처럼 수정할 필요가 없다.
Restlet은 모든 RESTful 시스템을 구현할 수 있고, RESTful 리소스 지향 웹 서비스를 구현할 때 리소스를 원하는 대로 배치하고 구현할 수 있다.
다만 Restlet은 리소스 지향 애플리케이션을 만들기 쉽게 해 주는 클래스도 제공하는데, 가장 대표적인 것이 모든 애플리케이션 리소스의 기반이 되는 `Resource` 클래스다.

### URI 템플릿과 리소스 매핑

이 책 전반에서 URI 템플릿은 URI들의 부류 전체를 지칭하는 약칭으로 쓰였다.
Restlet은 URI 템플릿을 이용해 URI를 리소스에 매핑한다.
7장의 소셜 북마킹 애플리케이션을 Restlet으로 구현한다면 특정 북마크로 가는 경로를 다음처럼 지정할 수 있다.

```text
/users/{username}/bookmarks/{URI}
```

`Resource` 하위 클래스를 `Router`에 붙일 때 바로 이 문법을 그대로 쓸 수 있다.

### Restlet 클라이언트 작성

2장에서는 Yahoo!의 웹 검색 서비스에서 XML 검색 결과를 가져오는 Ruby 클라이언트를 다뤘다.
다음은 Restlet 1.0으로 작성한 같은 클라이언트의 Java 구현이다.
컴파일과 실행에는 `org.restlet.jar`(Restlet API), `com.noelios.restlet.jar`(NRE 코어), `com.noelios.restlet.ext.net.jar`(JDK의 `HttpURLConnection` 기반 HTTP 클라이언트 커넥터)가 클래스패스에 있어야 하며, Java SE 5.0 이상이 필요하다.

```java
// YahooSearch.java

import org.restlet.Client;
import org.restlet.data.Protocol;
import org.restlet.data.Reference;
import org.restlet.data.Response;
import org.restlet.resource.DomRepresentation;
import org.w3c.dom.Node;

/**
 * Searching the web with Yahoo!'s web service using XML.
 */
public class YahooSearch {
    static final String BASE_URI =
        "http://api.search.yahoo.com/WebSearchService/V1/webSearch";

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.err.println("You need to pass a term to search");
        } else {
            // Fetch a resource: an XML document full of search results
            String term = Reference.encode(args[0]);
            String uri = BASE_URI + "?appid=restbook&query=" + term;
            Response response = new Client(Protocol.HTTP).get(uri);
            DomRepresentation document = response.getEntityAsDom();

            // Use XPath to find the interesting parts of the data structure
            String expr = "/ResultSet/Result/Title";
            for (Node node : document.getNodes(expr)) {
                System.out.println(node.getTextContent());
            }
        }
    }
}
```

이 예제는 Restlet으로 웹 서비스에서 XML 데이터를 가져와 표준 도구로 처리하는 일이 얼마나 쉬운지 보여 준다.
Yahoo! 리소스로 가는 URI는 상수와 사용자가 준 검색어로 구성되며, HTTP 프로토콜을 지정해 클라이언트 커넥터를 인스턴스화한다.
XML 문서는 HTTP 균일 인터페이스의 메서드 이름을 그대로 반영한 `get` 메서드로 가져온다.
호출이 반환되면 응답 엔티티를 DOM 표현으로 얻으며, Ruby 예제처럼 XPath가 가져온 XML을 검색하는 가장 간단한 방법이다.

이 프로그램은 결과 문서의 XML 네임스페이스를 무시한다.
Yahoo!는 문서 전체를 `urn:yahoo:srch` 네임스페이스에 넣지만, 여기서는 `ResultSet`처럼 네임스페이스 없이 태그에 접근한다.
Ruby 예제는 기본 XML 파서가 네임스페이스를 인식하지 못해 이를 무시했지만, Java의 XML 파서는 네임스페이스를 인식하며 Restlet API는 네임스페이스를 올바르게 다루기 쉽게 해 준다.

`urn:yahoo:srch:ResultSet`처럼 매번 전체 이름을 쓰는 것은 번거롭다.
Restlet API는 짧은 접두어를 네임스페이스에 연결한 뒤 XPath 식에서 전체 이름 대신 그 접두어를 쓰게 해 준다.

```java
DomRepresentation document = response.getEntityAsDom();

// Associate the namespace with the prefix 'y'
document.setNamespaceAware(true);
document.putNamespace("y", "urn:yahoo:srch");

// Use XPath to find the interesting parts of the data structure
String expr = "/y:ResultSet/y:Result/y:Title/text()";
for (Node node : document.getNodes(expr)) {
    System.out.println(node.getTextContent());
}
```

Restlet은 코어 API에서 XML을, 확장을 통해 JSON을 지원한다.
JSON을 쓰려면 `org.restlet.ext.json` 확장과 공식 `org.json` 라이브러리 JAR가 필요하다.
클라이언트가 표현 형식을 선택할 수 있으며, XML 버전과 JSON 버전 프로그램의 유일한 차이는 응답을 처리하는 부분이다.
`JsonRepresentation` 클래스는 응답 엔티티 본문을 `JSONObject` 인스턴스로 변환한다(Ruby의 JSON 라이브러리가 JSON을 네이티브 데이터 구조로 변환한 것과 대비된다).
JSON에는 아직 XPath 같은 질의 언어가 없으므로 데이터 구조는 수동으로 탐색한다.

### Restlet 서비스 작성

다음으로 서버 측 애플리케이션을 설계하고 구현하는 방법을 살펴본다.
7장에서 Ruby on Rails로 구현했던 북마크 관리 애플리케이션의 일부를 구현하며, 단순화를 위해 사용자와 그들의 북마크를 안전하게 조작하는 기능만 지원한다.

먼저 웹 서버를 설정하고 요청 처리를 시작하는 `Application`의 `main` 메서드다.

```java
public static void main(String... args) throws Exception {
    // Create a component with an HTTP server connector
    Component comp = new Component();
    comp.getServers().add(Protocol.HTTP, 3000);

    // Attach the application to the default host and start it
    comp.getDefaultHost().attach("/v1", new Application());
    comp.start();
}
```

#### 리소스와 URI 설계

Restlet은 리소스 설계에 아무런 제약도 두지 않으므로, 리소스 클래스와 그것이 노출하는 URI는 ROA 설계 고려에서 자연스럽게 흘러나온다.
7장의 리소스가 Rails의 컨트롤러 기반 아키텍처에 맞춰 설계된 것과 달리, Restlet 아키텍처를 중심으로 설계를 우회할 필요가 없다.

URI를 리소스에 매핑하는 코드는 `Application` 클래스의 `createRoot` 메서드에 있으며, 이는 Rails의 `routes.rb` 파일에 해당한다.

```java
public Restlet createRoot() {
    Router router = new Router(getContext());

    // Add a route for user resources
    router.attach("/users/{username}", UserResource.class);
    // Add a route for user's bookmarks resources
    router.attach("/users/{username}/bookmarks", BookmarksResource.class);
    // Add a route for bookmark resources
    Route uriRoute = router.attach("/users/{username}/bookmarks/{URI}",
                                   BookmarkResource.class);
    uriRoute.getTemplate().getVariables()
            .put("URI", new Variable(Variable.TYPE_URI_ALL));

    return router;
}
```

이 코드는 리소스 클래스 `UserResource`와 URI 템플릿 `/users/{username}` 사이에 깔끔하고 직관적인 관계를 만든다.
`Router`는 들어오는 URI를 템플릿과 대조해, 각 요청을 적절한 리소스 클래스의 새 인스턴스로 전달한다.
템플릿 변수의 값은 요청의 attributes 맵에 저장되어(Rails 예제의 `params` 맵과 유사하다) `Resource` 코드에서 손쉽게 쓸 수 있다.

#### 요청 처리와 표현

클라이언트가 `http://localhost:3000/v1/users/jerome`에 GET 요청을 한다고 하자.
`Component`가 localhost의 3000 포트에서 수신하고, `/v1`에 붙은 `Application`이 여러 URI 템플릿을 기다리는 `Router`와 `Route` 객체들을 가지고 있다.
URI 경로 조각 `/users/jerome`은 템플릿 `/users/{username}`과 일치하며, 그 `Route`는 `UserResource` 클래스와 연결되어 있다.
`UserResource`는 Rails의 `UsersController` 클래스에 대략 대응한다.

Restlet은 새 `UserResource` 객체를 인스턴스화하고 그 `handleGet` 메서드를 호출해 요청을 처리한다.

```java
public UserResource(Context context, Request request, Response response) {
    super(context, request, response);
    this.userName = (String) request.getAttributes().get("username");
    ChallengeResponse cr = request.getChallengeResponse();
    this.login = (cr != null) ? cr.getIdentifier() : null;
    this.password = (cr != null) ? cr.getSecret() : null;
    this.user = findUser();

    if (user != null) {
        getVariants().add(new Variant(MediaType.TEXT_PLAIN));
    }
}
```

이 시점에 프레임워크는 요청에 관한 모든 정보를 담은 `Request` 객체를 설정해 둔 상태다.
`username` 속성은 URI에서, 인증 자격 증명은 요청의 `Authorization` 헤더에서 온다.
`findUser`는 자격 증명을 바탕으로 데이터베이스에서 사용자를 조회하며, 이는 7장에서 Rails 필터가 하던 일이다.

프레임워크는 `UserResource`를 인스턴스화한 뒤 리소스 객체의 적절한 `handle` 메서드를 호출한다.
HTTP 균일 인터페이스의 각 메서드마다 하나씩 `handle` 메서드가 있으며, 이 경우 마지막으로 `UserResource.handleGet`이 호출된다.

여기서는 `handleGet`을 직접 정의하지 않으므로 Restlet의 `Resource.handleGet`에 정의된 상속 동작이 대신 수행된다.
`handleGet`의 기본 동작은 콘텐츠 협상을 통해 클라이언트의 요구에 가장 잘 맞는 표현을 찾는 것이다.
Restlet은 `Accept` 헤더 값을 보고 가장 적절한 “variant” 표현을 결정하며, 이는 `getVariants`와 `getRepresentation` 메서드가 처리한다.
생성자에서 유일한 지원 형식으로 `text/plain`을 지정했으므로 `getRepresentation` 구현은 단순하다.

```java
@Override
public Representation getRepresentation(Variant variant) {
    Representation result = null;

    if (variant.getMediaType().equals(MediaType.TEXT_PLAIN)) {
        // Creates a text representation
        StringBuilder sb = new StringBuilder();
        sb.append("----------------\n");
        sb.append("User details\n");
        sb.append("----------------\n\n");
        sb.append("Name: ").append(this.user.getFullName()).append('\n');
        sb.append("Email: ").append(this.user.getEmail()).append('\n');
        result = new StringRepresentation(sb);
    }

    return result;
}
```

다른 리소스와 `UserResource`의 다른 HTTP 메서드도 같은 방식으로 동작한다.
사용자에 대한 PUT 요청은 `UserResource.handlePut`으로 라우팅되는 식이다.
`Application`과 `Router` 코드는 단일 라우터가 모든 리소스를 처리할 수 있으므로 대개 한 번만 신경 쓰면 된다.

#### 컴파일, 실행, 테스트

`Application` 클래스는 소셜 북마킹 서비스를 실행하는 HTTP 서버를 구현한다.
실제 웹 서버 작업은 Simple 프레임워크에 기반한 매우 간결한 HTTP 서버 커넥터가 처리하고, 관계형 데이터베이스 대신 강력한 db4o 객체 데이터베이스로 도메인 객체(사용자와 북마크)를 영속화한다.
예제 파일을 모두 컴파일한 뒤 `org.restlet.example.book.rest.ch7.Application`을 실행하면 서버 엔드포인트로 동작한다.

`ApplicationTest` 클래스는 서비스에 대한 클라이언트 인터페이스를 제공한다.
앞 절에서 설명한 Restlet 클라이언트 클래스를 이용해 HTTP 균일 인터페이스로 사용자와 북마크를 추가하고 삭제하며, 사용자와 북마크는 PUT으로 생성하고 DELETE로 삭제한다.
이 프로그램으로 사용자와 북마크를 추가한 뒤, `http://localhost:3000/v1/users/jerome` 같은 URI를 표준 웹 브라우저로 방문해 사용자 북마크의 HTML 표현을 볼 수 있다.

### 결론

Restlet 프로젝트는 2007년 초에 최종 1.0 버전을 내놓았고, 개발에 12개월 남짓 걸렸으며 활발한 개발자와 사용자 커뮤니티를 갖추게 되었다.
집필 시점에 1.0은 유지보수 중이고 새 1.1 브랜치가 시작되었다.
향후 계획에는 Restlet API를 Java Community Process(JCP)에 표준화 제출하는 것이 포함된다.
또한 Sun Microsystems가 JCP에 제출한 JSR 311이라는, RESTful 웹 서비스를 위한 고수준 API도 개발 중이다.
이 고수준 API는 Java 도메인 객체를 RESTful 리소스로 노출하기 쉽게 해 주어, Restlet API 특히 `Resource` 클래스를 잘 보완할 것이다.

## Django

작성: Jacob Kaplan-Moss

Django(<http://www.djangoproject.com/>)는 Python으로 웹 애플리케이션과 웹 서비스를 쉽게 개발하게 해 주는 프레임워크다.
설계는 Rails와 매우 유사하지만 단순화 가정을 더 적게 둔다.
일반 ROA 설계 절차를 그대로 적용해 데이터셋을 RESTful 리소스 집합으로 바꾸고, 그 리소스들을 Django에서 직접 구현할 수 있다.

여기서는 7장의 Rails 구현과 같은 방향으로 소셜 북마킹 서비스를 Django로 구현한 예를 다룬다.

### 데이터 모델 생성

대부분의 Django 개발자는 데이터 모델 설계부터 시작한다.
이는 일반 ROA 절차의 첫 단계인 “데이터셋을 파악한다”에 해당한다.
모델은 보통 Django의 객체-관계 매핑(ORM) 도구를 이용해 관계형 데이터베이스에 저장된다.
데이터베이스를 쓰지 않는 RESTful 서비스도 물론 가능하지만, 소셜 북마킹 애플리케이션에는 데이터베이스가 가장 적합하다.

```python
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.SlugField(maxlength=100, primary_key=True)

class Bookmark(models.Model):
    user = models.ForeignKey(User)
    url = models.URLField(db_index=True)
    short_description = models.CharField(maxlength=255)
    long_description = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=datetime.now)
    public = models.BooleanField()
    tags = models.ManyToManyField(Tag)
```

이 짧은 코드에는 몇 가지 미묘함과 큰 힘이 담겨 있다.

- Rails 예제처럼 별도의 users 테이블을 만드는 대신 Django 내장 `User` 모델을 사용했다. 가장 큰 이점은 내장 `User` 모델이 인증과 권한 부여의 상당 부분을 처리해 준다는 것이다.
- Django에는 Rails의 `acts_as_taggable` 플러그인에 직접 대응하는 것이 없으므로, 마지막 줄에서 `Bookmark`와 `Tag` 사이에 다대다 관계를 정의했다.
- 태그 이름을 문자열이 아닌 `SlugField`로 정의했다. 이는 태그 이름을 URI에 나타날 수 있는 문자로 자동 제한하는 Django 클래스로, 공백이나 비영숫자 문자를 포함한 태그를 금지하기 쉽게 해 준다.
- Rails 스키마에서 명시적으로 만든 대부분의 데이터베이스 인덱스가 Django에서는 자동으로 추가된다. 특히 slug 필드와 외래 키에는 자동으로 인덱스가 붙는다. 다만 `url` 필드는 기본적으로 인덱스가 붙지 않으므로, 검색에 쓰기 위해 `db_index=True`를 명시적으로 지정했다.

### 리소스 정의와 URI 부여

Rails 구현은 11개의 리소스를 노출하지만, 여기서는 그중 4개만 구현한다.

- 하나의 북마크
- 한 사용자의 북마크 목록
- 사용자가 특정 태그를 붙인 북마크 목록
- 사용자가 사용한 태그 목록

특히 사용자 계정은 리소스로 노출하지 않는다.
이 서비스를 쓰려면 데이터베이스에 샘플 사용자 계정을 미리 만들어 두어야 한다.

Rails는 URI 설계에 영향을 주는 단순화 가정을 부과한다.
리소스를 정의하는 대신 특정 URI에 리소스를 노출하는 Rails 컨트롤러를 정의하게 된다.
반면 Django는 URI를 처음부터 직접 설계하게 한다.
URI는 웹 애플리케이션 사용자 인터페이스의 중요한 일부이며 자동 생성되어서는 안 된다는 것이 Django의 철학이다.
리소스의 유일한 인터페이스 요소가 그 URI와 HTTP 균일 인터페이스라는 ROA 철학과도 잘 맞는다.

Django에는 Rails 같은 “최소 저항 경로”가 없어 URI를 더 간결하고 읽기 좋게 만들 수 있다.
Rails 애플리케이션의 URI 구조를 세 가지로 수정한다.

- Django의 “관례”는 항상 URI를 슬래시로 끝내는 것이다. 그래서 `/users/{username}` 대신 `/users/{username}/`처럼 모든 URI에 마지막 슬래시를 붙인다.
- Rails의 컨트롤러 기반 구조에서는 북마크를 `/users/{username}/bookmarks/{URL}/`로 노출하는 것이 편했지만, Django에서는 더 간결한 `/users/{username}/{URL}/`을 쓴다.
- 사용자 계정을 리소스로 노출하지 않으므로 `/users/{username}/` URI를 다른 용도, 즉 “북마크 목록” 리소스에 쓴다.
- Rails 구현은 북마크 목록의 하위 리소스로 새 북마크를 만들기 위해 POST를 썼다. 여기서는 `/users/{username}/{URI}/`로 PUT을 보내 북마크 목록을 우회해 새 북마크를 만든다. Rails는 URI 안에 URI를 넣는 데 문제가 있어 `/users/{username}/bookmarks/{URI-MD5}` 같은 URI를 노출했지만, 여기서는 실제 URI 자체를 쓸 수 있다.

Django URI 설정 파일로 이 URI들을 리소스에 쉽게 매핑할 수 있으며, 이는 Rails의 `routes.rb` 파일에 해당한다.
Django는 URI 형식을 대신 결정하려 하지 않으므로 훨씬 단순하다.

```python
from django.conf.urls.defaults import *
from bookmarks.views import *

urlpatterns = patterns('',
    (r'^users/([\w-]+)/$', bookmark_list),
    (r'^users/([\w-]+)/tags/$', tag_list),
    (r'^users/([\w-]+)/tags/([\w-]+)/$', tag_detail),
    (r'^users/([\w-]+)/(.*)$', BookmarkDetail()),
)
```

`urls.py`는 들어오는 URI(정규 표현식으로 표현)를 요청을 처리하는 함수에 매핑하는 작은 Python 모듈이다.
정규 표현식의 그룹은 함수의 인자로 전달된다.
예를 들어 `users/jacobian/tags/python` 요청이 들어오면 세 번째 정규 표현식과 일치해 `tag_detail` 함수가 `“jacobian”`과 `“python”` 두 인자로 호출된다.

Django는 URI 패턴을 순서대로 평가하므로, 태그 URI를 북마크 URI보다 앞에 두어야 한다.
그러지 않으면 Django가 `/users/jacobian/tags/`를 (유효하지 않은) URI `tags`에 대한 북마크 요청으로 해석하게 된다.

### Django 뷰로 리소스 구현

Django는 MVC 패턴을 Rails와 다르게 해석한다.
Rails에서는 균일 인터페이스 아래 리소스의 동작을 컨트롤러 클래스에 넣지만, Django에서는 그 코드가 뷰(view)로 들어간다.

#### 북마크 목록 뷰

“북마크 목록” 리소스는 GET에만 응답하므로 뷰 함수도 단순하다.
북마크 생성은 Rails처럼 목록에 POST하는 것이 아니라 PUT으로 노출한다는 점을 기억하자.

```python
from bookmarks.models import Bookmark
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def bookmark_list(request, username):
    u = get_object_or_404(User, username=username)
    marks = Bookmark.objects.filter(user=u, public=True)
    json = serializers.serialize("json", marks)
    return HttpResponse(json, mimetype="application/json")
```

첫 단계는 `username` 인자를 Django `User` 객체로 바꾸는 것이다.
존재하지 않는 사용자의 북마크 요청에는 HTTP 404(“Not Found”)를 반환해야 하므로 `get_object_or_404()` 단축 함수로 사용자를 조회한다.
사용자가 없으면 이 함수가 `Http404` 예외를 던지고 Django가 이를 404 응답으로 바꿔 준다.
이는 Rails 애플리케이션의 `if_found` 메서드와 같은 목적을 수행한다.

7장에서 ActiveRecord의 `to_xml`로 객체를 XML 표현으로 변환한 것과 유사하게, 여기서는 Django 직렬화 API로 데이터베이스 행을 JSON 데이터 구조로 바꾼다.
직렬화 형식을 XML로 바꾸는 것은 세 번째 줄의 serializer 타입과 마지막 줄의 mimetype만 바꾸면 될 만큼 간단하다.
Django의 기본 JSON 출력은 다음과 같은 형태다.

```json
[{
    "pk": "1",
    "model": "bookmarks.bookmark",
    "fields": {
        "tags": ["example"],
        "url": "http://example.com/",
        "timestamp": "2007-01-30 21:35:23",
        "long_description": "",
        "user": 1,
        "short_description": "Example",
        "public": true
    }
}]
```

위 구현은 동작하지만 다소 순진하다.
호출될 때마다 사용자의 모든 북마크를 반환해 데이터베이스 자원과 대역폭을 소모한다.
조건부 GET(Conditional GET)을 지원하도록 개선하면 `Last-Modified`와 `If-Modified-Since` 처리로 뷰가 복잡해지지만 대역폭 절약이라는 대가가 있다.

```python
import datetime
from bookmarks.models import Bookmark
from django.contrib.auth.models import User
from django.core import serializers
from django.http import *
from django.shortcuts import get_object_or_404

# Use the excellent python-dateutil module to simplify date handling.
# See http://labix.org/python-dateutil
import dateutil.parser
from dateutil.tz import tzlocal, tzutc

def bookmark_list(request, username):
    u = get_object_or_404(User, username=username)

    # If the If-Modified-Since header was provided,
    # build a lookup table that filters out bookmarks
    # modified before the date in If-Modified-Since.
    lookup = dict(user=u, public=True)
    lm = request.META.get("HTTP_IF_MODIFIED_SINCE", None)
    if lm:
        try:
            lm = dateutil.parser.parse(lm)
        except ValueError:
            lm = None  # Ignore invalid dates
        else:
            lookup['timestamp__gt'] = lm.astimezone(tzlocal())

    # Apply the filter to the list of bookmarks.
    marks = Bookmark.objects.filter(**lookup)

    # If we got If-Modified-Since but there aren't any bookmarks,
    # return a 304 ("Not Modified") response.
    if lm and marks.count() == 0:
        return HttpResponseNotModified()

    # Otherwise return the serialized data...
    json = serializers.serialize("json", marks)
    response = HttpResponse(json, mimetype="application/json")

    # ... with the appropriate Last-Modified header.
    now = datetime.datetime.now(tzutc())
    response["Last-Modified"] = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return response
```

#### 북마크 상세 뷰

두 번째 뷰는 더 복잡하다.
“북마크 목록” 리소스는 GET에만 응답하지만, “북마크” 리소스는 세 가지 HTTP 메서드를 처리해야 한다.
북마크에 대한 GET은 표현을 조회하고, PUT은 북마크를 생성하거나 갱신하며, DELETE는 북마크를 삭제한다.
사용자가 서로의 북마크를 수정하지 못하게 해야 하므로 인증도 고려해야 한다.

가장 단순한 방법은 `if request.method == ...` 절을 늘어놓는 것이지만, 이는 우아하지 못하고 금세 다루기 힘든 뷰가 된다.
대신 Python의 “덕 타이핑(duck typing)”을 활용해 북마크 상세 뷰를 호출 가능한 객체(callable object)로 구현한다.
Python에서 함수는 일급 객체이고, `object(argument)` 형태의 함수 호출은 `object.__call__(argument)` 메서드 호출로 변환된다.
따라서 `__call__` 메서드를 정의하면 어떤 객체든 함수처럼 호출할 수 있다.
바로 이 때문에 앞의 `urls.py` 마지막 줄만 다른 세 줄과 다르게, 정규 표현식을 `__call__`을 구현한 커스텀 객체에 연결한다.

```python
class BookmarkDetail:
    def __call__(self, request, username, bookmark_url):
        self.request = request
        self.bookmark_url = bookmark_url

        # Look up the user and throw a 404 if it doesn't exist.
        self.user = get_object_or_404(User, username=username)

        # Try to locate a handler method.
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            # This class doesn't implement this HTTP method, so return
            # a 405 ("Method Not Allowed") response and list the
            # allowed methods.
            allowed_methods = [m.lstrip("do_") for m in dir(self)
                               if m.startswith("do_")]
            return HttpResponseNotAllowed(allowed_methods)

        # Check and store HTTP basic authentication, even for methods that
        # don't require authorization.
        self.authenticate()

        # Call the looked-up method.
        return callback()
```

`BookmarkDetail.__call__`은 들어오는 요청의 HTTP 메서드를 확인해 각 요청을 `do_<METHOD>` 형태의 메서드로 디스패치한다.
예를 들어 GET 요청은 `do_GET`으로 디스패치되며, 이는 Rails가 GET 요청을 `MyController#show` 호출로 바꾸는 것과 유사하다.
클래스가 구현하지 않은 메서드에는 405(“Method Not Allowed”)를 반환하고 허용 메서드 목록을 함께 알려 준다.

`BookmarkDetail` 클래스는 HTTP 기본 인증(basic authentication)도 처리해야 한다.
실제 애플리케이션에서는 이런 함수를 인증이 필요한 모든 뷰가 공유하는 상위 클래스에 두게 된다.
이는 7장에서 `must_authenticate` Rails 필터를 기반 `ApplicationController` 클래스에 넣은 방식을 떠올리게 한다.

```python
from django.contrib.auth import authenticate

class BookmarkDetail:
    # ...

    def authenticate(self):
        # Pull the auth info out of the Authorization header
        auth_info = self.request.META.get("HTTP_AUTHORIZATION", None)
        if auth_info and auth_info.startswith("Basic "):
            basic_info = auth_info.lstrip("Basic ")
            u, p = basic_info.decode("base64").split(":")

            # Authenticate against the User database. This will set
            # authenticated_user to None if authentication fails.
            self.authenticated_user = authenticate(username=u, password=p)
        else:
            self.authenticated_user = None

    def forbidden(self):
        response = HttpResponseForbidden()
        response["WWW-Authenticate"] = 'Basic realm="Bookmarks"'
        return response
```

이제 개별 `do_<METHOD>` 메서드 안에서 `self.authenticated_user`를 확인할 수 있다.
`forbidden()` 헬퍼는 올바른 `WWW-Authenticate` 헤더와 함께 인증 실패 응답을 보낸다.

GET이 가장 단순하다.
`do_GET` 구현은 북마크 목록의 GET 응답과 같은 개념을 보여 주며, 유일한 큰 차이는 비공개 북마크의 프라이버시를 강제한다는 점이다.

```python
def do_GET(self):
    # Look up the bookmark (possibly throwing a 404)
    bookmark = get_object_or_404(Bookmark,
        user=self.user,
        url=self.bookmark_url
    )

    # Check privacy
    if bookmark.public == False and self.user != self.authenticated_user:
        return self.forbidden()

    json = serializers.serialize("json", [bookmark])
    return HttpResponse(json, mimetype="application/json")
```

다음은 PUT이다.
이 메서드는 들어오는 북마크 상태 표현을 받아 새 북마크를 만들거나 기존 북마크를 갱신한다.
들어오는 표현은 `self.request.raw_post_data`로 접근하며, Django 직렬화 라이브러리로 JSON 데이터 구조를 Django 데이터베이스 객체로 바꾼다.

```python
def do_PUT(self):
    # Check that the user whose bookmark it is matches the authorization
    if self.user != self.authenticated_user:
        return self.forbidden()

    # Deserialize the representation from the request. Serializers
    # work on lists, but we're only expecting one here. Any errors
    # and we send 400 ("Bad Request").
    try:
        deserialized = serializers.deserialize("json",
            self.request.raw_post_data)
        put_bookmark = list(deserialized)[0].object
    except (ValueError, TypeError, IndexError):
        response = HttpResponse()
        response.status_code = 400
        return response

    # Look up or create a bookmark, then update it
    bookmark, created = Bookmark.objects.get_or_create(
        user=self.user,
        url=self.bookmark_url,
    )

    for field in ["short_description", "long_description",
                  "public", "timestamp"]:
        new_val = getattr(put_bookmark, field, None)
        if new_val:
            setattr(bookmark, field, new_val)
    bookmark.save()

    # Return the serialized object, with either a 200 ("OK") or a 201
    # ("Created") status code.
    json = serializers.serialize("json", [bookmark])
    response = HttpResponse(json, mimetype="application/json")
    if created:
        response.status_code = 201
        response["Location"] = "/users/%s/%s" % \
            (self.user.username, bookmark.url)
    return response
```

마지막으로 DELETE는 매우 단순하다.

```python
def do_DELETE(self):
    # Check authorization
    if self.user != self.authenticated_user:
        return self.forbidden()

    # Look up the bookmark...
    bookmark = get_object_or_404(Bookmark,
        user=self.user,
        url=self.bookmark_url
    )

    # ... and delete it.
    bookmark.delete()

    # Return a 200 ("OK")
    response = HttpResponse()
    response.status_code = 200
    return response
```

### 향후 방향

태그 뷰(그리고 번들 등 다른 기능들)도 비슷한 패턴을 따른다.
조금만 손보면 이 `BookmarkDetail` 클래스를 여러 종류의 객체를 처리하는 더 범용적인 리소스 클래스로 리팩터링할 수 있다.

### 결론

Django는 HTTP 요청만 처리하는 프레임워크가 아니다.
Rails처럼 웹 애플리케이션과 웹 서비스 설계의 공통 문제를 다루는 여러 하위 라이브러리를 포함한다.
Rails의 ActiveRecord처럼 동작하는 ORM, 내장 `User` 모델, 모델 객체를 JSON 표현으로 직렬화하는 기능을 앞에서 보았다.
Django에는 댓글 모델과 신디케이션 피드 생성 도구 등 다른 라이브러리도 많다.
주로 웹 애플리케이션에 쓰이지만, Django는 RESTful 웹 서비스를 Python으로 구현하는 데도 훌륭한 기반이 된다.

## 핵심 정리

세 프레임워크 모두 리소스를 코드로 노출하지만, RESTful 설계를 지원하는 방식과 부과하는 제약의 정도가 다르다.

Ruby on Rails는 강한 단순화 가정 위에 서 있다.
`config/routes.rb`의 `map.resources`가 URI 구조와 컨트롤러 라우팅을 관례에 따라 정해 주고, 컨트롤러마다 다섯 개의 표준 메서드(index, create, show, update, delete)와 두 개의 폼 뷰(new, edit)를 통해 목록/팩토리 리소스와 객체 리소스를 노출한다.
표현 협상은 `respond_to`가, 들어오는 표현 파싱은 `params` 해시와 `param_parsers`가 담당한다.
관례에 들어맞으면 매우 빠르지만, 원하는 URI 구조를 얻으려면 때로 가정과 싸워야 한다.

Restlet은 반대로 어떤 단순화 가정도 두지 않는다.
`Uniform`/`Restlet`의 `handle` 메서드가 모든 프로토콜과 클라이언트/서버 역할을 하나의 균일 인터페이스로 통합하고, `Router`가 URI 템플릿으로 요청을 `Resource` 하위 클래스에 매핑한다.
URI 관례를 강요하지 않으므로 리소스를 ROA 설계 그대로 배치할 수 있고, 6장의 일반 설계 절차를 수정 없이 적용할 수 있다.

Django는 Rails와 유사하지만 가정을 더 적게 둔다.
데이터 모델을 ORM으로 정의하고, `urls.py`에서 정규 표현식으로 URI를 뷰에 명시적으로 매핑하며, 리소스 동작은 뷰 함수나 호출 가능한 객체(`__call__`)에 담는다.
URI를 개발자가 직접 설계하게 하는 철학이 오히려 ROA와 잘 맞아, 균일 인터페이스의 각 메서드를 `do_GET`, `do_PUT`, `do_DELETE`로 명시적으로 디스패치하고 조건부 GET, 인증, 상태 코드까지 직접 다룰 수 있다.
