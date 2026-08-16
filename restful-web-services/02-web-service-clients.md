# 2장 웹 서비스 클라이언트 작성하기

《RESTful Web Services》(Leonard Richardson, Sam Ruby, O'Reilly 2007) 2장 정리.

## 개요

2장은 웹 서비스 요청의 생애주기를 클라이언트 관점에서 따라가며, 래퍼 라이브러리에 의존하지 않고 HTTP 요청과 응답을 직접 다루는 방법을 여러 프로그래밍 언어로 보여준다.
핵심 논지는 “웹 서비스는 결국 웹 사이트다”라는 것이다.
웹 서비스 요청에 마법 같은 것은 없으며, 프로그래밍 언어의 HTTP 클라이언트 라이브러리로 요청을 보내고 표준 XML 파서로 응답을 처리하면 된다.

모든 웹 서비스 요청은 동일한 세 단계를 거친다.

1. HTTP 요청에 담을 데이터를 준비한다. HTTP 메서드, URI, 헤더, 그리고 PUT/POST 요청이라면 엔티티 바디에 담을 문서까지 마련한다.
2. 그 데이터를 HTTP 요청으로 형식화하여 적절한 HTTP 서버로 보낸다.
3. 응답 데이터(응답 코드, 헤더, 엔티티 바디)를 프로그램이 쓸 수 있는 자료구조로 파싱한다.

이 장은 여러 언어와 라이브러리가 이 세 단계를 어떻게 구현하는지를 다루고, 마지막으로 이 반복 패턴을 추상화하는 WADL을 소개한다.

## 웹 서비스는 웹 사이트다

1장에서는 기존 공개 웹 서비스의 클라이언트를 래퍼 라이브러리를 통해 다뤘지만, 편리한 래퍼가 항상 존재하는 것은 아니다.
특히 자신이 직접 만든 웹 서비스라면 더욱 그렇다.
다행히 HTTP 요청과 응답을 직접 다루는 프로그램을 작성하기는 쉽다.

예제 2-1은 야후 웹 검색이라는 RESTful 웹 서비스에 대한 순수 HTTP 클라이언트다.
1장에서 구글 검색의 RPC 스타일 SOAP 인터페이스에 접근하던 예제 1-8과 비교해 볼 만하다.

```ruby
#!/usr/bin/ruby
# yahoo-web-search.rb
require 'open-uri'
require 'rexml/document'
require 'cgi'

BASE_URI = 'http://api.search.yahoo.com/WebSearchService/V1/webSearch'

def print_page_titles(term)
  # 자원(검색 결과가 담긴 XML 문서)을 가져온다.
  term = CGI::escape(term)
  xml = open(BASE_URI + "?appid=restbook&query=#{term}").read

  # XML 문서를 자료구조로 파싱한다.
  document = REXML::Document.new(xml)

  # XPath로 관심 있는 부분을 찾는다.
  REXML::XPath.each(document, '/ResultSet/Result/Title/text()') do |title|
    puts title
  end
end

(puts "Usage: #{$0} [search term]"; exit) if ARGV.empty?
print_page_titles(ARGV.join(' '))
```

이 “웹 서비스” 코드는 평범한 HTTP 클라이언트 코드와 다를 바 없다.
루비 표준 라이브러리 `open-uri`로 HTTP 요청을 만들고, 표준 라이브러리 `REXML`로 출력을 파싱한다.
일반 웹 페이지를 가져와 처리할 때 쓰는 도구와 같다.

다음 두 URI는 같은 대상(“질의 'jellyfish'에 대한 검색 결과 목록”)의 서로 다른 표현을 가리킨다.

- `http://api.search.yahoo.com/WebSearchService/V1/webSearch?appid=restbook&query=jellyfish`
- `http://search.yahoo.com/search?p=jellyfish`

하나는 HTML을 제공하며 웹 브라우저용이고, 다른 하나는 XML을 제공하며 자동화된 클라이언트용이다.

### 래퍼, WADL, ActiveResource

웹 서비스 요청은 결국 HTTP 요청일 뿐이지만, 특정 서비스에는 웹 전체에는 없는 나름의 논리와 구조가 있다.
세 단계 알고리즘을 매번 그대로 반복하면 코드는 지저분해지고 그 밑에 깔린 구조를 활용하지 못한다.

그래서 똑똑한 프로그래머라면 요청의 패턴을 알아채고 HTTP 접근의 세부 사항을 감추는 래퍼 메서드를 작성한다.
예제 2-1의 `print_page_titles`가 원시적인 래퍼의 예다.
서비스가 인기를 얻으면 여러 언어로 다듬어진 래퍼 라이브러리가 나온다.
아마존은 RESTful S3 서비스용 클라이언트를 다섯 개 언어로 무료 제공하고, 그럼에도 외부 개발자들은 jbucket, s3sh 같은 자체 S3 클라이언트를 만들었다.

래퍼는 특정 서비스에 맞춰진 API를 제공하므로 HTTP를 전혀 신경 쓰지 않아도 되어 편하다.
단점은 래퍼마다 조금씩 다르다는 점이다. 하나를 익혀도 다음 래퍼에는 도움이 되지 않는다.

이 서비스들이 모두 세 단계 HTTP 요청 알고리즘의 변주일 뿐이라면, 서비스 간 차이를 추상화하여 RESTful 및 하이브리드 서비스 전체의 래퍼처럼 동작하는 라이브러리가 있어야 하지 않을까?
이것이 서비스 기술(service description)의 문제다.
다양한 RESTful 및 하이브리드 서비스를 기술할 수 있는 어휘를 갖춘 언어가 필요하다.
그 언어로 작성한 문서가 범용 웹 서비스 클라이언트를 마치 맞춤 제작된 래퍼처럼 동작하도록 조종할 수 있다.

SOAP RPC 진영은 서비스 기술 언어로 WSDL을 중심으로 뭉쳤다.
REST 진영은 아직 하나의 기술 언어로 통일되지 않았고, 저자는 WSDL의 자원 지향적 대안으로 WADL을 지지한다.
또한 개발 중인 범용 클라이언트로 ActiveResource가 있는데, 이것은 Ruby on Rails 프레임워크로 작성된 웹 서비스의 클라이언트를 쉽게 작성하게 해 주며 3장 끝에서 다룬다.

## del.icio.us: 예제 애플리케이션

이 장의 예제는 소셜 북마킹 사이트 del.icio.us가 제공하는 웹 서비스를 사용한다.
del.icio.us는 웹 브라우저의 북마크 기능처럼 동작하되 공개적이고 더 잘 정리되어 있다.
링크를 저장하면 계정에 연결되어 나중에 다시 찾을 수 있고, 다른 사람과 공유할 수도 있다.
URL에는 태그(tag)라는 짧은 문자열을 붙일 수 있는데, 여러 사람이 같은 URI에 태그를 달면 그 URI에 대한 기계 판독 가능한 어휘가 만들어진다.

del.icio.us 웹 서비스는 북마크에 프로그램으로 접근하게 해 준다.
웹 사이트와 웹 서비스 사이에 근본적 차이는 없지만 다음과 같은 변형이 있다.

- 웹 사이트는 `http://del.icio.us/`에, 웹 서비스는 `https://api.del.icio.us/v1/`에 뿌리를 둔다. 웹 사이트는 HTTP로, 웹 서비스는 보안 HTTPS로 통신한다.
- 두 쪽은 서로 다른 URI 구조를 노출한다. 최근 북마크를 얻으려면 웹 사이트에서는 `https://del.icio.us/{사용자명}`을, 웹 서비스에서는 `https://api.del.icio.us/v1/posts/recent`를 가져온다.
- 웹 사이트는 HTML 문서를, 웹 서비스는 XML 문서를 제공한다. 형식은 다르지만 담긴 데이터는 같다.
- 웹 사이트는 로그인이나 계정 없이도 많은 정보를 보여 주지만, 웹 서비스는 모든 요청에 인증을 요구한다.
- 웹 사이트에는 소셜 기능이 있지만 웹 서비스는 자기 자신의 북마크만 볼 수 있다.

이런 변형이 있어도 웹 서비스가 웹 사이트와 다른 종류의 것이 되지는 않는다.
웹 서비스는 HTTPS를 쓰고 낯선 형식의 문서를 제공하는, 기능을 덜어낸 웹 사이트일 뿐이다.
이 장 전체를 관통하는 주제가 바로 이것이다. 웹 서비스는 웹 사이트와 같은 규칙 아래 동작해야 한다.

한편 del.icio.us 웹 서비스 자체는 그다지 RESTful하게 설계되지 않았다.
URI 배치가 자원 지향적이라기보다 RPC 스타일을 시사한다.
모든 요청이 HTTP GET 메서드를 쓰고, 실제 메서드 정보는 URI에 담겨 “GET”과 충돌할 여지가 있다.
예를 들어 `https://api.del.icio.us/v1/posts/add`와 `https://api.del.icio.us/v1/tags/rename`을 보면, 명시적인 `methodName` 변수는 없어도 “add”와 “rename”이라는 메서드 정보가 HTTP 메서드가 아니라 URI에 담겨 있다.
이는 1장에서 다룬 Flickr API와 마찬가지다.

그럼에도 del.icio.us를 예제로 고른 이유는 세 가지다.

첫째, 이해하기 쉬운 애플리케이션이고 웹 서비스가 인기 있고 쓰기 쉽다.

둘째, 이후 장들의 내용이 규범적(prescriptive)이지 기술적(descriptive)이지 않음을 분명히 하기 위해서다.
웹 서비스를 구현할 때 REST의 제약을 따르면 웹처럼 동작하는 좋은 서비스를 클라이언트에게 줄 수 있다.
그러나 클라이언트를 구현할 때는 있는 그대로의 서비스와 씨름해야 한다.
대안은 변경을 요청하거나 서비스를 보이콧하는 것뿐이다.
서버는 이상주의적이어야 하지만 클라이언트는 실용적이어야 한다.
이는 포스텔의 법칙(Postel's Law)의 변형이다. “네가 하는 것은 보수적으로, 남에게서 받는 것은 관대하게 하라.”

셋째, 7장에서 del.icio.us와 비슷하지만 RESTful 원칙으로 설계한 북마크 추적 서비스를 제시하기 때문이다.
지금 소셜 북마킹 도메인을 소개해 두면, 7장에서 RESTful 인터페이스를 설계하고 구현할 때 그 차이를 알아볼 수 있다.

### 예제 클라이언트가 하는 일

이 장의 예제 클라이언트들은 모두 정확히 같은 일을 한다.
먼저 `api.del.icio.us` 서버의 443번 포트(표준 HTTPS 포트)로 TCP/IP 소켓 연결을 연다.
그런 다음 예제 2-2 같은 HTTP 요청을 보내고, 서버는 예제 2-3 같은 응답을 돌려주고 소켓 연결을 닫는다.
모든 HTTP 응답이 그렇듯 이 응답도 상태 코드, 헤더 집합, 엔티티 바디의 세 부분으로 이루어지며 여기서 엔티티 바디는 XML 문서다.

```http
GET /v1/posts/recent HTTP/1.1
Host: api.del.icio.us
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

```http
200 OK
Content-Type: text/xml
Date: Sun, 29 Oct 2006 15:09:36 GMT
Connection: close

<?xml version='1.0' standalone='yes' ?>
<posts tag="" user="username">
  <post href="http://www.foo.com/" description="foo" extended=""
    hash="14d59bdc067e3c1f8f792f51010ae5ac" tag="foo"
    time="2006-10-29T02:56:12Z" />
  <post href="http://amphibians.com/" description="Amphibian Mania"
    extended="" hash="688b7b2f2241bc54a0b267b69f438805" tag="frogs toads"
    time="2006-10-28T02:55:53Z" />
</posts>
```

클라이언트는 엔티티 바디에만 관심이 있고, 그중에서도 `post` 태그의 `href`와 `description` 속성만 본다.
XML 문서를 자료구조로 파싱한 뒤 XPath 식 `/posts/post`로 `post` 태그를 순회하며, 각 북마크의 `href`와 `description`을 표준 출력으로 찍는다.

```text
foo: http://www.foo.com/
Amphibian Mania: http://amphibians.com/
```

## 요청 만들기: HTTP 라이브러리

현대 프로그래밍 언어에는 대부분 HTTP 요청을 만드는 라이브러리가 하나 이상 있다.
다만 모두가 똑같이 쓸모 있는 것은 아니다.
완전히 범용적인 웹 서비스 클라이언트를 만들려면 다음 기능을 갖춘 HTTP 라이브러리가 필요하다.

- HTTPS와 SSL 인증서 검증을 지원해야 한다. 많은 웹 서비스(del.icio.us 포함)는 평문 HTTP 요청을 아예 받지 않는다. HTTPS 지원은 흔히 C로 작성된 외부 SSL 라이브러리의 존재에 의존한다.
- 최소한 다섯 개 주요 HTTP 메서드(GET, HEAD, POST, PUT, DELETE)를 지원해야 한다. 어떤 라이브러리는 GET/POST만, 또는 GET만 지원한다. GET/POST만 있어도 HTML 폼이 이 둘만 쓰므로 사람용 웹 전체에 접근할 수 있고, 심지어 GET만으로도 (del.icio.us나 Flickr처럼 원래 쓰지 말아야 할 곳에서도 GET을 쓰는 서비스가 많아) 꽤 멀리 갈 수 있다. 그러나 WADL 클라이언트 같은 범용 클라이언트를 쓴다면 다섯 메서드 모두가 필요하다. OPTIONS, TRACE나 WebDAV의 MOVE 같은 추가 메서드는 덤이다.
- PUT/POST 요청의 엔티티 바디로 보낼 데이터를 프로그래머가 지정할 수 있어야 한다.
- 요청의 HTTP 헤더를 프로그래머가 지정할 수 있어야 한다.
- 응답의 엔티티 바디뿐 아니라 응답 코드와 헤더에도 접근할 수 있어야 한다.
- HTTP 프록시를 통해 통신할 수 있어야 한다. 기업 환경의 많은 HTTP 클라이언트는 프록시를 통해서만 동작한다. 프록시 같은 중개자는 REST 메타 아키텍처의 표준 요소다.

### 선택적 기능

RESTful 및 하이브리드 서비스의 클라이언트를 쓸 때 편해지는 기능도 있다.
이들은 대체로 HTTP 헤더에 관한 지식으로 귀결되므로 기술적으로는 선택 사항이다.
라이브러리가 요청/응답 헤더에 접근하게 해 준다면 직접 구현할 수도 있지만, 라이브러리가 지원하면 세부 사항을 신경 쓰지 않아도 된다.

- 대역폭 절약을 위해 데이터를 압축 형태로 자동 요청하고 받은 데이터를 투명하게 압축 해제해야 한다. 요청 헤더는 `Accept-Encoding`, 응답 헤더는 `Encoding`이며 8장에서 자세히 다룬다.
- 응답을 자동으로 캐시해야 한다. 같은 URI를 두 번째 요청할 때 서버의 객체가 바뀌지 않았다면 캐시에서 돌려줘야 한다. 요청의 `If-Modified-Since`와 `ETag`, 응답의 `Last-Modified`와 `ETag` 헤더가 관련되며 역시 8장에서 다룬다.
- 가장 흔한 HTTP 인증 방식(Basic, Digest, WSSE)을 투명하게 지원해야 한다. 아마존식 회사 고유 인증 방식도 지원하거나 플러그인으로 붙일 수 있으면 유용하다. 요청 헤더는 `Authorization`, 인증을 요구하는 응답 헤더는 `WWW-Authenticate`다.
- HTTP 리다이렉트를 투명하게 따라가되 무한 리다이렉트와 루프는 피해야 한다. 이는 매번 자동으로 일어나기보다 사용자가 선택할 수 있는 편의 기능이어야 한다. 서비스가 303(“See Other”)을 보냈다고 클라이언트가 곧장 그 URI를 가져와야 하는 것은 아니기 때문이다.
- HTTP 쿠키 문자열을 파싱하고 생성할 수 있어야 한다. 쿠키를 꺼리는 RESTful 서비스에는 별로 중요하지 않지만 사람용 웹을 쓰려면 매우 중요하다.

특정 서비스만 상대할 때는 이 기능 중 일부 또는 전부가 없어도 된다.
루비의 표준 `open-uri`는 GET만 지원하지만 GET만 기대하는 del.icio.us에는 문제없다.
반면 GET, HEAD, PUT, DELETE를 쓰는 아마존 S3에 `open-uri`를 쓰려 하면 곧 벽에 부딪힌다.

### Ruby: rest-open-uri와 net/http

루비에는 HTTP 클라이언트 라이브러리가 두 개 있다. `open-uri`와 더 저수준인 `net/http`다.
`net/https` 확장이 설치되어 있으면 둘 다 HTTPS 요청을 할 수 있다.

`open-uri`는 URI를 파일 이름처럼 다루는 단순하고 우아한 인터페이스를 가진다.
`open`에 커스텀 헤더와 키워드 인자를 담은 해시를 넘겨 프록시나 인증 정보를 설정할 수 있다.
다만 현재 `open-uri`는 GET만 지원한다.
그래서 저자는 `open-uri`를 조금 수정해 `rest-open-uri`라는 루비 젬으로 공개했고, `open`에 HTTP 메서드를 지정하는 `:method`와 엔티티 바디를 보내는 `:body` 키워드 인자를 추가했다.

예제 2-4는 `open-uri`로 구현한 del.icio.us 클라이언트다(`rest-open-uri`도 같은 방식으로 동작한다).

```ruby
#!/usr/bin/ruby -w
# delicious-open-uri.rb
require 'rubygems'
require 'open-uri'
require 'rexml/document'

# del.icio.us 사용자의 최근 북마크를 가져와 하나씩 출력한다.
def print_my_recent_bookmarks(username, password)
  # HTTPS 요청을 만든다.
  response = open('https://api.del.icio.us/v1/posts/recent',
                  :http_basic_authentication => [username, password])

  # 응답 엔티티 바디를 XML 문서로 읽는다.
  xml = response.read

  # 문서를 자료구조로 만든다.
  document = REXML::Document.new(xml)

  # 각 북마크에 대해...
  REXML::XPath.each(document, "/posts/post") do |e|
    # 북마크의 description과 URI를 출력한다.
    puts "#{e.attributes['description']}: #{e.attributes['href']}"
  end
end

# 메인 프로그램
username, password = ARGV
unless username and password
  puts "Usage: #{$0} [username] [password]"
  exit
end
print_my_recent_bookmarks(username, password)
```

S3처럼 완전히 RESTful한 서비스의 루비 클라이언트가 필요하면 `rest-open-uri`를 쓰거나 저수준 `net/http`로 가야 한다.
`net/http`가 제공하는 `Net::HTTP` 클래스만으로 완전한 HTTP 클라이언트를 만들 수 있고, 실제로 `open-uri`와 `rest-open-uri`도 이 위에 얹혀 있다.
`Net::HTTP` 자체는 프록시, HTTPS, 헤더 등 REST 클라이언트에 필요한 기능을 쉽게 쓸 인터페이스를 주지 않기 때문에 저자는 `rest-open-uri`를 권한다.

루비 HTTP 라이브러리 기능 비교는 아래와 같다.

| 기능          | open-uri              | net/http | rest-open-uri |
| ------------- | --------------------- | -------- | ------------- |
| HTTPS         | 예(net/https 설치 시) | 예       | 예            |
| HTTP 메서드   | GET                   | 전부     | 전부          |
| 커스텀 데이터 | 아니오                | 예       | 예            |
| 커스텀 헤더   | 예                    | 예       | 예            |
| 프록시        | 예                    | 예       | 예            |
| 압축          | 아니오                | 아니오   | 아니오        |
| 캐싱          | 아니오                | 아니오   | 아니오        |
| 인증 방식     | Basic                 | 없음     | Basic         |
| 쿠키          | 아니오                | 아니오   | 아니오        |
| 리다이렉트    | 예                    | 예       | 아니오        |

### Python: httplib2

파이썬 표준 라이브러리에는 HTTP 클라이언트가 두 개 있다.
루비 `open-uri`처럼 파일류 인터페이스를 가진 `urllib2`, 그리고 루비 `Net::HTTP`처럼 동작하는 `httplib`다.
둘 다 파이썬이 SSL 지원으로 컴파일됐다면 HTTPS를 투명하게 지원한다.
여기에 더해 저자가 일반적으로 추천하는 것은 조 그레고리오(Joe Gregorio)의 서드파티 라이브러리 `httplib2`다.
`httplib2`는 투명한 캐싱을 포함해 저자의 희망 목록에 있는 거의 모든 기능을 지원한다.

예제 2-5는 `httplib2`를 쓰고 `ElementTree`로 XML을 파싱하는 파이썬 클라이언트다.

```python
#!/usr/bin/python2.5
# delicious-httplib2.py
import sys
from xml.etree import ElementTree
import httplib2

# del.icio.us 사용자의 최근 북마크를 가져와 하나씩 출력한다.
def print_my_recent_bookmarks(username, password):
    client = httplib2.Http(".cache")
    client.add_credentials(username, password)

    # HTTP 요청을 만들고 응답과 엔티티 바디를 받는다.
    response, xml = client.request('https://api.del.icio.us/v1/posts/recent')

    # XML 엔티티 바디를 자료구조로 만든다.
    doc = ElementTree.fromstring(xml)

    # 모든 북마크 정보를 출력한다.
    for post in doc.findall('post'):
        print "%s: %s" % (post.attrib['description'], post.attrib['href'])

# 메인 프로그램
if len(sys.argv) != 3:
    print "Usage: %s [username] [password]" % sys.argv[0]
    sys.exit()

username, password = sys.argv[1:]
print_my_recent_bookmarks(username, password)
```

파이썬 HTTP 라이브러리 기능 비교는 아래와 같다.

| 기능          | urllib2                 | httplib | httplib2                    |
| ------------- | ----------------------- | ------- | --------------------------- |
| HTTPS         | 예(SSL 지원 컴파일 시)  | 예      | 예                          |
| HTTP 메서드   | GET, POST               | 전부    | 전부                        |
| 커스텀 데이터 | 예                      | 예      | 예                          |
| 커스텀 헤더   | 예                      | 예      | 예                          |
| 프록시        | 예                      | 아니오  | 아니오                      |
| 압축          | 아니오                  | 아니오  | 예                          |
| 캐싱          | 아니오                  | 아니오  | 예                          |
| 인증 방식     | Basic, Digest           | 없음    | Basic, Digest, WSSE, Google |
| 쿠키          | 예(HTTPCookieProcessor) | 아니오  | 아니오                      |
| 리다이렉트    | 예                      | 아니오  | 예                          |

### Java: HttpClient

자바 표준 라이브러리에는 `java.net.HttpURLConnection`이 있다.
`java.net.URL` 객체에 `open`을 호출해 인스턴스를 얻는다.
HTTP 기본 기능 대부분을 지원하지만 그 API로 프로그래밍하기는 매우 어렵다.
아파치 자카르타 프로젝트의 `HttpClient`는 설계가 더 낫다.
또한 `Restlet`도 있는데, 12장에서 서버 라이브러리로 다루지만 HTTP 클라이언트로도 쓸 수 있다.
`org.restlet.Client` 클래스로 간단한 요청을, `org.restlet.data.Request` 클래스로 더 복잡한 요청을 쉽게 만든다.

예제 2-6은 `HttpClient`를 쓰는 자바 클라이언트다.

```java
// DeliciousApp.java
import java.io.*;
import org.apache.commons.httpclient.*;
import org.apache.commons.httpclient.auth.AuthScope;
import org.apache.commons.httpclient.methods.GetMethod;
import org.w3c.dom.*;
import org.xml.sax.SAXException;
import javax.xml.parsers.*;
import javax.xml.xpath.*;

public class DeliciousApp {
    public static void main(String[] args)
        throws HttpException, IOException, ParserConfigurationException,
               SAXException, XPathExpressionException {
        // 인증 자격 증명을 설정한다.
        Credentials creds =
            new UsernamePasswordCredentials(args[0], args[1]);
        HttpClient client = new HttpClient();
        client.getState().setCredentials(AuthScope.ANY, creds);

        // HTTP 요청을 만든다.
        String url = "https://api.del.icio.us/v1/posts/recent";
        GetMethod method = new GetMethod(url);
        client.executeMethod(method);
        InputStream responseBody = method.getResponseBodyAsStream();

        // 응답 엔티티 바디를 XML 문서로 만든다.
        DocumentBuilderFactory docBuilderFactory =
            DocumentBuilderFactory.newInstance();
        DocumentBuilder docBuilder = docBuilderFactory.newDocumentBuilder();
        Document doc = docBuilder.parse(responseBody);
        method.releaseConnection();

        // XPath 식으로 북마크 목록을 얻는다.
        XPath xpath = XPathFactory.newInstance().newXPath();
        NodeList bookmarks = (NodeList) xpath.evaluate("/posts/post", doc,
                                                       XPathConstants.NODESET);

        // 북마크를 순회하며 하나씩 출력한다.
        for (int i = 0; i < bookmarks.getLength(); i++) {
            NamedNodeMap bookmark = bookmarks.item(i).getAttributes();
            String description =
                bookmark.getNamedItem("description").getNodeValue();
            String uri = bookmark.getNamedItem("href").getNodeValue();
            System.out.println(description + ": " + uri);
        }
        System.exit(0);
    }
}
```

자바 HTTP 라이브러리 기능 비교는 아래와 같다.

| 기능          | HttpURLConnection   | HttpClient          | Restlet       |
| ------------- | ------------------- | ------------------- | ------------- |
| HTTPS         | 예                  | 예                  | 예            |
| HTTP 메서드   | 전부                | 전부                | 전부          |
| 커스텀 데이터 | 예                  | 예                  | 예            |
| 커스텀 헤더   | 예                  | 예                  | 예            |
| 프록시        | 예                  | 예                  | 예            |
| 압축          | 아니오              | 아니오              | 예            |
| 캐싱          | 예                  | 아니오              | 예            |
| 인증 방식     | Basic, Digest, NTLM | Basic, Digest, NTLM | Basic, Amazon |
| 쿠키          | 예                  | 예                  | 예            |
| 리다이렉트    | 예                  | 예                  | 예            |

### C#: System.Web.HTTPWebRequest

.NET 공용 언어 런타임(CLR)은 HTTP 요청을 위한 `HTTPWebRequest`와 서버 인증을 위한 `NetworkCredential`을 정의한다.
`HTTPWebRequest` 생성자는 URI를, `NetworkCredential` 생성자는 사용자명과 비밀번호를 받는다.

```csharp
using System;
using System.IO;
using System.Net;
using System.Xml.XPath;

public class DeliciousApp {
    static string user = "username";
    static string password = "password";
    static Uri uri = new Uri("https://api.del.icio.us/v1/posts/recent");

    static void Main(string[] args) {
        HttpWebRequest request = (HttpWebRequest) WebRequest.Create(uri);
        request.Credentials = new NetworkCredential(user, password);
        HttpWebResponse response = (HttpWebResponse) request.GetResponse();

        XPathDocument xml = new XPathDocument(response.GetResponseStream());
        XPathNavigator navigator = xml.CreateNavigator();

        foreach (XPathNavigator node in navigator.Select("/posts/post")) {
            string description = node.GetAttribute("description", "");
            string href = node.GetAttribute("href", "");
            Console.WriteLine(description + ": " + href);
        }
    }
}
```

### PHP: libcurl

PHP에는 C 라이브러리 `libcurl`에 대한 바인딩이 딸려 있어 URI로 할 수 있는 일 대부분을 처리한다.

```php
<?php
$user = "username";
$password = "password";

$request = curl_init();
curl_setopt($request, CURLOPT_URL,
            'https://api.del.icio.us/v1/posts/recent');
curl_setopt($request, CURLOPT_USERPWD, "$user:$password");
curl_setopt($request, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($request);
$xml = simplexml_load_string($response);
curl_close($request);

foreach ($xml->post as $post) {
    print "$post[description]: $post[href]\n";
}
?>
```

### JavaScript: XMLHttpRequest

자바스크립트로 웹 서비스 클라이언트를 쓴다면 대개 웹 브라우저 안에서 Ajax 애플리케이션의 일부로 실행하려는 것이다.
모든 현대 브라우저는 자바스크립트용 HTTP 클라이언트 라이브러리 `XMLHttpRequest`를 구현한다.
Ajax 클라이언트는 독립 실행형 클라이언트와 개발 방식이 다르므로 11장에서 따로 다룬다.

### 명령줄: curl

`curl`은 프로그래밍 언어를 전혀 쓰지 않는 예다.
유닉스나 윈도우 명령줄에서 실행되는 능력 있는 HTTP 클라이언트로, 대부분의 HTTP 메서드, 커스텀 헤더, 여러 인증 방식, 프록시, 압축 등을 지원한다.
일회성 HTTP 요청이나 셸 스크립트와 함께 쓰기 좋다.

```bash
$ curl https://username:password@api.del.icio.us/v1/posts/recent
<?xml version='1.0' standalone='yes' ?>
<posts tag="" user="username">
</posts>
```

### 그 밖의 언어

- ActionScript: 플래시 애플리케이션도 대개 브라우저 안에서 실행되므로 11장의 Ajax 아키텍처를 쓰게 된다. `XML` 클래스가 자바스크립트의 `XMLHttpRequest`와 비슷한 기능을, `XML.load` 메서드가 URI를 가져와 XML 자료구조로 파싱하는 기능을 제공한다. 폼 인코딩된 키-값 쌍을 다루는 `LoadVars` 클래스도 있다.
- C: 최초의 HTTP 클라이언트 라이브러리는 `libwww`였지만 오늘날 대부분의 C 프로그래머는 `curl` 명령줄 도구의 기반인 `libcurl`을 쓴다. `libcurl`은 30개가 넘는 언어에 바인딩이 있다.
- C++: `libcurl`을 직접 쓰거나 객체 지향 래퍼 `cURLpp`를 통해 쓴다.
- Common Lisp: `simple-http`는 쓰기 쉽지만 기본 GET/POST만 지원하고, `AllegroServe` 웹 서버 라이브러리에는 완전한 HTTP 클라이언트가 들어 있다.
- Perl: 표준 라이브러리는 `libwww-perl`(LWP)이며, HTTPS 지원을 위해서는 `Crypt::SSLeay` 모듈도 설치해야 한다.

## 응답 처리하기: XML 파서

엔티티 바디는 보통 HTTP 응답에서 가장 중요한 부분이며 웹 서비스에서는 대개 XML 문서다.
클라이언트는 이 문서를 XML 파서에 통과시켜 필요한 정보를 얻는다.

HTTP 클라이언트 라이브러리는 많지만 하는 일은 전부 같다.
URI, 헤더 집합, 바디 문서가 주어지면 HTTP 요청을 구성해 서버로 보낸다.
쿠키, 인증, 캐싱 같은 추가 기능도 결국 HTTP 요청 안에(주로 추가 헤더로) 구현된다.
객체 지향 인터페이스(`Net::HTTP`)든 파일류 인터페이스(`open-uri`)든 하는 일은 같으므로, HTTP 클라이언트 라이브러리는 사실상 한 종류다.

그러나 XML 파서에는 세 종류가 있다.
단지 기능 차이나 인터페이스 취향의 문제가 아니라 근본적으로 두 가지 파싱 전략이 있다.
DOM 등 트리 스타일 파서의 문서 기반(document-based) 전략과, SAX 및 풀(pull) 파서의 이벤트 기반(event-based) 전략이다.
어느 언어든 트리 스타일이나 SAX 파서를 구할 수 있고, 거의 모든 언어에서 풀 파서도 구할 수 있다.

문서 기반 트리 스타일 전략이 셋 중 가장 단순하다.
트리 스타일 파서는 XML 문서를 중첩된 자료구조로 모델링한다.
이 자료구조가 생기면 XPath 질의, CSS 선택자, 커스텀 탐색 함수 등으로 검색하고 처리할 수 있다.
DOM 파서는 W3C가 정의한 특정 인터페이스를 구현하는 트리 스타일 파서다.

트리 스타일은 쓰기 쉬워 저자가 가장 많이 쓰는 방식이다.
문서가 다른 객체들과 같은 하나의 객체가 되기 때문이다.
큰 단점은 문서 전체를 다뤄야 한다는 점이다.
문서 전체를 트리로 만들기 전에는 작업을 시작할 수 없고 전체를 메모리에 올려야 한다.
단순하지만 아주 큰 문서에는 비효율적이다.

트리 스타일 대신 SAX 스타일이나 풀 파서는 문서를 이벤트의 스트림으로 바꾼다.
여는 태그와 닫는 태그, XML 주석, 엔티티 선언 등이 모두 이벤트다.

풀 파서는 거의 모든 이벤트를 처리해야 할 때 유용하다.
필요할 때마다 스트림에서 다음 이벤트를 “끌어와(pull)” 한 번에 하나씩 처리한다.
들어오는 이벤트에 즉시 반응할 수도 있고 나중에 쓸 자료구조를 만들 수도 있으며, 언제든 파싱을 멈췄다가 다음 이벤트를 끌어오며 재개할 수 있다.

SAX 파서는 더 복잡하지만 쏟아지는 많은 이벤트 중 일부만 신경 쓸 때 유용하다.
콜백 메서드를 등록해 두고 파서를 문서에 풀어 놓으면, 파서는 문서를 이벤트 연쇄로 바꿔 멈추지 않고 모든 이벤트를 처리한다.
콜백에 걸리는 이벤트가 오면 파서가 그 콜백을 실행하고, 콜백이 끝나면 다시 멈춤 없이 이벤트 처리를 이어 간다.

문서 기반 방식의 장점은 문서 내용에 임의 접근할 수 있다는 것이다.
이벤트 기반 파서에서는 이벤트가 한 번 발생하면 사라지고, 다시 처리하려면 문서를 다시 파싱해야 한다.
게다가 이벤트 기반 파서는 문서가 잘못된 부분을 파싱하려다 깨지기 전까지는 문서가 잘못됐는지 알아채지 못한다.
그래서 문서를 이벤트 기반 파서에 넣기 전에 잘 구성된(well-formed) 문서인지 확인하거나, 콜백이 결국 온전하지 않은 문서에서 실행될 수 있음을 감수해야 한다.

파서를 평가할 때는 속도, 인터페이스 품질, XPath 지원 정도(트리 스타일), 얼마나 엄격한지, 스키마 기반 검증을 지원하는지를 본다.
엄격한 파서는 상황에 따라 장점(잘못된 XML을 아예 거부)이 되기도, 단점(나쁜 XML을 내놓는 서비스를 써야 할 때)이 되기도 한다.

이벤트 기반 파서를 보여 주기 위해 루비 내장 SAX 파서와 풀 파서를 쓴 예제를 추가로 든다.

### Ruby: REXML

루비에는 표준 XML 파서 `REXML`이 있고 DOM과 SAX 인터페이스를 모두 지원하며 XPath 지원도 좋다.
다만 `REXML`은 나쁜 XML을 파싱하기에는 너무 엄격하면서도 모든 나쁜 XML을 거부할 만큼 엄격하지는 않은 어중간한 위치에 있다.
저자는 잘 구성된 XML만 다루기에 기본 선택지로 `REXML`을 쓰지만, 잘 구성된 XML만 다루겠다고 보장하려면 GNOME 프로젝트의 `libxml2` 루비 바인딩을 설치해야 한다.
나쁜 마크업을 다뤄야 한다면 C 확장을 써서 빠르고 흔한 XPath 식을 지원하는 `hpricot`이 최선이다.

예제 2-9는 `REXML`의 SAX 인터페이스로 구현한 클라이언트다.

```ruby
#!/usr/bin/ruby -w
# delicious-sax.rb
require 'open-uri'
require 'rexml/parsers/sax2parser'

def print_my_recent_bookmarks(username, password)
  # HTTPS 요청을 만들고 엔티티 바디를 XML 문서로 읽는다.
  xml = open('https://api.del.icio.us/v1/posts/recent',
             :http_basic_authentication => [username, password])

  # XML 엔티티 바디를 파싱할 SAX 파서를 만든다.
  parser = REXML::Parsers::SAX2Parser.new(xml)

  # 'post' 태그를 만나면...
  parser.listen(:start_element, ["post"]) do |uri, tag, fqtag, attributes|
    # ...태그 정보를 출력한다.
    puts "#{attributes['description']}: #{attributes['href']}"
  end

  # 파서가 XML 엔티티 바디를 파싱하게 한다.
  parser.parse
end

# 메인 프로그램
username, password = ARGV
unless username and password
  puts "Usage: #{$0} [USERNAME] [PASSWORD]"
  exit
end
print_my_recent_bookmarks(username, password)
```

이 프로그램에서는 `parse` 호출 전까지 데이터가 파싱되지도 읽히지도 않는다.
그전까지는 `listen`으로 이벤트에 반응할 코드를 등록할 수 있다.
여기서는 `post` 태그 시작 이벤트만 관심 대상이며, 코드 블록은 파서가 `post` 태그를 찾을 때마다 실행된다.
이는 트리 스타일 파서로 파싱한 뒤 객체 트리에 XPath 식 `//post`를 돌리는 것과 같다.
이 구현은 트리 스타일보다 빠르고 메모리 효율적이지만, 복잡한 SAX 기반 프로그램은 트리 스타일보다 작성하기 훨씬 어렵다.
풀 파서는 좋은 절충안이다.

예제 2-10은 `REXML`의 풀 파서 인터페이스를 쓴 구현이다.

```ruby
#!/usr/bin/ruby -w
# delicious-pull.rb
require 'open-uri'
require 'rexml/parsers/pullparser'

def print_my_recent_bookmarks(username, password)
  # HTTPS 요청을 만들고 엔티티 바디를 XML 문서로 읽는다.
  xml = open('https://api.del.icio.us/v1/posts/recent',
             :http_basic_authentication => [username, password])

  # XML 엔티티 바디를 풀 파서에 넣는다.
  parser = REXML::Parsers::PullParser.new(xml)

  # 끌어올 이벤트가 남아 있는 동안...
  while parser.has_next?
    # ...다음 이벤트를 끌어온다.
    tag = parser.pull
    # 'post' 태그라면...
    if tag.start_element?
      if tag[0] == 'post'
        # 북마크 정보를 출력한다.
        attrs = tag[1]
        puts "#{attrs['description']}: #{attrs['href']}"
      end
    end
  end
end

# 메인 프로그램
username, password = ARGV
unless username and password
  puts "Usage: #{$0} [USERNAME] [PASSWORD]"
  exit
end
print_my_recent_bookmarks(username, password)
```

### Python: ElementTree

파이썬에는 XML 파서가 매우 많고 파이썬 2.5 표준 라이브러리에만 XML 인터페이스가 일곱 개 있다.
트리 스타일 파싱에는 `ElementTree`가 최선이다.
빠르고 인터페이스가 합리적이며 파이썬 2.5부터는 표준 라이브러리에 포함된다.
단점은 XPath 지원이 단순한 식에 한정된다는 점인데, 그마저도 표준 라이브러리에서 XPath를 지원하는 유일한 곳이다.
완전한 XPath 지원이 필요하면 `4Suite`를 쓴다.
`Beautiful Soup`은 더 느리지만 잘못된 XML에 매우 관대한 트리 스타일 파서로, 문자셋 변환을 대부분 자동 처리해 유니코드 데이터를 다루게 해 준다.
SAX 스타일에는 표준 라이브러리의 `xml.sax` 모듈이 최선이고, `PyXML` 스위트에는 풀 파서가 들어 있다.

### Java: javax.xml, Xerces, XMLPull

자바 1.5에는 아파치 Xerces 프로젝트가 작성한 XML 파서가 들어 있다.
핵심 클래스는 `javax.xml.*` 패키지(예: `javax.xml.xpath`)에 있고, DOM 인터페이스는 `org.w3c.dom.*`에, SAX 인터페이스는 `org.xml.sax.*`에 있다.
이전 버전 자바를 쓴다면 Xerces를 직접 설치해 같은 인터페이스를 쓸 수 있다.
자바용 풀 파서는 여러 가지가 있으며 썬의 Web Services Developer Pack에는 `javax.xml.stream` 패키지의 풀 파서가 들어 있다.
나쁜 XML을 파싱하려면 `TagSoup`을 시도해 볼 만하다.

### C#: System.Xml.XmlReader

.NET CLR은 더 흔하고 복잡한 SAX 스타일 대신 풀 파서 인터페이스를 제공한다.
`XmlDocument`로 완전한 W3C DOM 트리를 만들 수도 있고, `XPathDocument` 클래스로 XPath 식에 맞는 노드를 순회할 수 있다.
깨진 XML을 다뤄야 하면 크리스 러벳(Chris Lovett)의 `SgmlReader`를 보면 된다.

### PHP

`xml_parser_create` 함수로 SAX 스타일 파서를, `XMLReader` 확장으로 풀 파서를 만든다.
PHP 5에 포함된 DOM 확장은 GNOME `libxml2` C 라이브러리에 트리 스타일 인터페이스를 제공한다.
공식 DOM 구현은 아니지만 더 쓰기 쉬운 트리 스타일 파서 `SimpleXML`도 있으며, 예제 2-8에서 이것을 썼다.
순수 PHP로 된 DOM 파서 `DOMIT!`도 있다.

### JavaScript: responseXML

`XMLHttpRequest`로 Ajax 클라이언트를 쓸 때는 XML 파서를 신경 쓸 필요가 없다.
응답 엔티티 바디가 XML이면 브라우저가 자체 트리 스타일 파서로 파싱해 `XMLHttpRequest` 객체의 `responseXML` 속성으로 제공한다.
이 문서는 브라우저에 표시된 HTML을 다룰 때와 같은 자바스크립트 DOM 메서드로 조작한다.
비XML 문서는 `responseData` 멤버로 다루며 11장에서 자세히 설명한다.
브라우저 내장 파서와 독립적으로 동작하고 DOM/SAX 인터페이스와 XPath 질의를 지원하는 서드파티 파서 `XML for <SCRIPT>`도 있다.

### 그 밖의 언어

- ActionScript: `XML.load`로 URI를 불러오면 자동으로 트리 스타일 인터페이스를 노출하는 `XML` 객체로 파싱된다.
- C: `Expat`이 가장 인기 있는 SAX 스타일 파서이고, GNOME `libxml2`에는 DOM, 풀, SAX 파서가 모두 들어 있다.
- C++: 두 C 파서를 쓰거나 객체 지향 `Xerces-C++` 파서를 쓴다. 자바판 Xerces처럼 DOM과 SAX 인터페이스를 모두 노출한다.
- Common Lisp: `SXML`을 쓴다. SAX 유사 인터페이스를 노출하고 XML 문서를 트리 형태의 S-표현식이나 Lisp 자료구조로도 바꿀 수 있다.
- Perl: 파서가 여럿이며 모두 CPAN에 있다. `XML::XPath`는 XPath를, `XML::Simple`은 표준 Perl 자료구조로의 변환을 지원하고, SAX에는 `XML::SAX::PurePerl`, 풀에는 `XML::LibXML::Reader`를 쓴다.

## JSON 파서: 직렬화된 데이터 다루기

대부분의 웹 서비스는 XML 문서를 반환하지만, 숫자, 배열, 해시 같은 단순한 자료구조를 JSON 형식 문자열로 직렬화해 반환하는 서비스도 늘고 있다.
JSON은 주로 Ajax 애플리케이션의 클라이언트 쪽에서 소비될 것을 기대하는 서비스가 만들어 낸다.
브라우저가 XML 문서보다 JSON에서 자바스크립트 자료구조를 얻기가 훨씬 쉽기 때문이다.
브라우저마다 XML 파서에 대한 자바스크립트 인터페이스가 조금씩 다르지만, JSON 문자열은 엄격히 제약된 자바스크립트 프로그램일 뿐이라 모든 브라우저에서 똑같이 동작한다.

물론 JSON은 자바스크립트에 묶여 있지 않으며, XML 스키마 같은 XML 기반 직렬화 방식의 가벼운 대안이다.
예제 2-11은 혼합 타입 배열을 JSON으로 표현한 것이다.

```json
[3, "three"]
```

예제 2-12는 같은 데이터를 XML-RPC 형식으로 표현한 것으로, 훨씬 읽기 어렵다.

```xml
<value>
  <array>
    <data>
      <value><i4>3</i4></value>
      <value><string>three</string></value>
    </data>
  </array>
</value>
```

JSON 문자열은 엄격히 제약된 자바스크립트 프로그램일 뿐이라 문자열에 `eval`을 호출하는 것만으로 “파싱”할 수 있다.
이는 매우 빠르지만, JSON을 제공하는 웹 서비스를 자신이 통제하지 않는 한 해서는 안 된다.
검증되지 않았거나 신뢰할 수 없는 서비스가 진짜 JSON 구조 대신 버그투성이거나 악의적인 자바스크립트를 보낼 수 있기 때문이다.
11장의 자바스크립트 예제에서는 json.org에서 제공하는 자바스크립트로 작성된 JSON 파서를 쓴다.

```javascript
<!-- json-demo.html -->
<!-- 실제 애플리케이션에서는 json.js를 매번 json.org에서
     가져오지 말고 로컬에 저장해 두어야 한다. -->
<script type="text/javascript" src="http://www.json.org/json.js">
</script>

<script type="text/javascript">
array = [3, "three"]
alert("Converted array into JSON string: '" + array.toJSONString() + "'")

json = "[4, \"four\"]"
alert("Converted JSON '" + json + "' into array:")
array2 = json.parseJSON()
for (i = 0; i < array2.length; i++) {
  alert("Element #" + i + " is " + array2[i])
}
</script>
```

Dojo 자바스크립트 프레임워크는 `dojo.json` 패키지에 JSON 라이브러리를 두고 있어 Dojo를 쓰면 따로 설치할 필요가 없다.
앞으로의 ECMAScript 표준이 JSON 직렬화/역직렬화 메서드를 자바스크립트 언어의 일부로 정의해 서드파티 라이브러리를 불필요하게 만들 수도 있다.

이 책의 루비 예제에서는 `json` 루비 젬의 JSON 파서를 쓴다.
가장 중요한 메서드는 `Object#to_json`과 `JSON.parse`다.

```ruby
# json-demo.rb
require 'rubygems'
require 'json'

[3, "three"].to_json      # => "[3,\"three\"]"
JSON.parse('[4, "four"]') # => [4, "four"]
```

현재 JSON을 제공하는 가장 인기 있는 공개 웹 서비스는 야후 웹 서비스다.
예제 2-15는 야후 뉴스 웹 서비스에서 현재 뉴스 기사의 JSON 표현을 얻는 루비 명령줄 프로그램이다.

```ruby
#!/usr/bin/ruby
# yahoo-web-search-json.rb
require 'rubygems'
require 'json'
require 'open-uri'
$KCODE = 'UTF8'

# 검색어로 웹을 검색해 일치하는 페이지의 제목을 출력한다.
def search(term)
  base_uri = 'http://api.search.yahoo.com/NewsSearchService/V1/newsSearch'

  # HTTP 요청을 만들고 응답 엔티티 바디를 JSON 문서로 읽는다.
  json = open(base_uri + "?appid=restbook&output=json&query=#{term}").read

  # JSON 문서를 루비 자료구조로 파싱한다.
  json = JSON.parse(json)

  # 자료구조를 순회하며...
  json['ResultSet']['Result'].each do |r|
    # ...각 페이지의 제목을 출력한다.
    puts r['Title']
  end
end

# 메인 프로그램
unless ARGV[0]
  puts "Usage: #{$0} [search term]"
  exit
end
search(ARGV[0])
```

예제 2-1의 `yahoo-web-search.rb`와 비교하면 기본 구조는 같지만 동작이 다르다.
2-1은 XML로 결과를 받아 파싱하고 XPath로 제목을 뽑지만, 이 프로그램은 JSON을 네이티브 자료구조(해시)로 파싱하고 XPath 대신 네이티브 연산자로 순회한다.

JSON이 이렇게 단순하다면 왜 모든 것에 쓰지 않을까?
그럴 수도 있지만 저자는 권하지 않는다.
JSON은 일반적인 자료구조를 표현하기에 좋지만, 웹이 주로 제공하는 것은 문서, 즉 서로 링크로 얽힌 불규칙하고 자기 기술적인 자료구조다.
XML과 HTML은 문서 표현에 특화되어 있다.
웹 페이지를 JSON으로 표현하면 예제 2-12의 배열 XML 표현처럼 읽기 어려울 것이다.
JSON은 단순한 리스트나 해시처럼 문서 패러다임에 잘 맞지 않는 자료구조를 기술할 때 유용하다.

## WADL로 쉬워지는 클라이언트

지금까지의 코드는 언어가 달라도 늘 같은 세 단계 패턴을 따랐다.
HTTP 요청 요소(메서드, URI, 헤더, 엔티티 바디)를 만들고, HTTP 라이브러리로 실제 요청을 보내고, XML 파서로 응답을 파싱한다.
이 점에서 모든 RESTful 웹 서비스와 대부분의 하이브리드 서비스가 같고, 나아가 모든 RESTful 웹 서비스는 HTTP를 같은 방식으로 쓴다. 이를 균일 인터페이스(uniform interface)라 한다.

이 유사성을 활용해 이 패턴을 균일 인터페이스를 지원하는 어떤 서비스에도 접근할 수 있는 범용 “REST 라이브러리”로 추상화할 수 있을까?
선례가 있다. WSDL은 RPC 스타일 웹 서비스 간 차이를 충분히 상세하게 기술해, 적절한 WSDL 파일만 있으면 범용 라이브러리가 어떤 RPC 스타일 SOAP 서비스에도 접근하게 해 준다.

RESTful 및 하이브리드 서비스에는 WADL(Web Application Description Language)을 권한다.
WADL 파일은 서비스에 정당하게 보낼 수 있는 HTTP 요청, 즉 어떤 URI를 방문할 수 있는지, 그 URI가 어떤 데이터를 보내길 기대하는지, 응답으로 어떤 데이터를 주는지를 기술한다.
WADL 라이브러리는 이 파일을 파싱해 가능한 서비스 요청의 공간을 네이티브 언어 API로 모델링한다.

예제 2-16은 예제 2-4의 루비 클라이언트와 동등하지만, 루비 WADL 라이브러리와 저자가 del.icio.us용으로 만든 비공식 WADL 파일을 쓴다.

```ruby
#!/usr/bin/ruby
# delicious-wadl-ruby.rb
require 'wadl'

if ARGV.size != 2
  puts "Usage: #{$0} [username] [password]"
  exit
end
username, password = ARGV

# WADL 파일에서 애플리케이션을 로드한다.
delicious = WADL::Application.from_wadl(open("delicious.wadl"))

# 애플리케이션에 인증 정보를 준다.
service = delicious.v1.with_basic_auth(username, password)

begin
  # "recent posts" 기능을 찾는다.
  recent_posts = service.posts.recent

  # 최근 post마다...
  recent_posts.get.representation.each_by_param('post') do |post|
    # description과 URI를 출력한다.
    puts "#{post.attributes['description']}: #{post.attributes['href']}"
  end
rescue WADL::Faults::AuthorizationRequired
  puts "Invalid authentication information!"
end
```

이 코드는 내부적으로 이 장의 다른 클라이언트와 똑같은 HTTP 요청을 만들지만, 그 세부 사항은 WADL 클라이언트 라이브러리가 해석하는 `delicious.wadl` 파일에 감춰져 있다.
언뜻 웹 서비스 클라이언트로 보이지 않는데, 이는 라이브러리가 제 역할을 하고 있다는 뜻이다.
WADL은 HTTP의 세부는 추상화하지만 그 밑에 깔린 RESTful 인터페이스는 추상화하지 않는다.

집필 시점에 WADL 채택률은 매우 낮다.
어떤 서비스에 언어별 클라이언트 대신 WADL 클라이언트를 쓰려면 WADL 파일을 직접 써야 할 가능성이 크다.
남의 서비스에 대한 비공식 WADL 파일을 쓰는 일은 어렵지 않으며, 심지어 사람용으로 설계된 웹 애플리케이션을 웹 서비스처럼 쓰게 하는 WADL 파일도 쓸 수 있다.
WADL은 RESTful 웹 서비스를 기술하도록 설계됐지만 웹에서 벌어지는 거의 모든 것을 기술할 수 있다.

한편 루비 라이브러리 ActiveResource는 다른 전략을 취한다.
특정 종류의 웹 서비스에서만 동작하지만 RESTful HTTP 접근의 세부를 단순한 객체 지향 인터페이스 뒤에 감춘다.
ActiveResource는 REST 용어를 소개한 뒤 다음 장에서 다룬다.

## 핵심 정리

- 웹 서비스 요청에 특별한 마법은 없다. HTTP 클라이언트 라이브러리로 요청을 보내고 XML 파서로 응답을 처리하는, 웹 사이트를 다루는 것과 같은 작업이다. 웹 서비스는 같은 규칙 아래 동작하는 웹 사이트일 뿐이다.
- 모든 웹 서비스 요청은 세 단계를 따른다. 요청 데이터(메서드, URI, 헤더, 바디)를 준비하고, HTTP 요청으로 보내고, 응답을 자료구조로 파싱한다.
- 좋은 HTTP 클라이언트 라이브러리는 HTTPS, 다섯 개 주요 메서드, 커스텀 바디와 헤더, 응답 코드/헤더 접근, 프록시를 지원해야 하고, 압축·캐싱·인증·리다이렉트·쿠키 지원은 편의를 더한다. HTTP 클라이언트 라이브러리는 인터페이스만 다를 뿐 사실상 한 종류다.
- 서버는 이상주의적이어야 하지만 클라이언트는 실용적이어야 한다(포스텔의 법칙). del.icio.us처럼 RPC 스타일에 가까운 서비스라도 있는 그대로와 씨름해야 한다.
- XML 파서에는 세 종류가 있다. 문서 기반 트리 스타일(DOM 등)은 임의 접근과 XPath에 유리하지만 문서 전체를 메모리에 올린다. 이벤트 기반의 SAX와 풀 파서는 빠르고 메모리 효율적이지만, SAX는 콜백 방식이라 작성이 어렵고 풀 파서가 그 절충안이다.
- XML 대신 JSON을 반환하는 서비스가 늘고 있으며, JSON은 자료구조 직렬화에 가벼운 대안이다. 다만 신뢰할 수 없는 서비스의 JSON에 `eval`을 쓰면 안 되고, 서로 링크로 얽힌 문서 표현에는 여전히 XML/HTML이 적합하다.
- WADL은 RESTful 및 하이브리드 서비스를 기술하는 언어로, WADL 파일 하나로 범용 클라이언트가 맞춤 래퍼처럼 동작하게 한다. 균일 인터페이스라는 REST의 공통점을 활용하며, HTTP 세부는 감추되 RESTful 인터페이스는 유지한다.
