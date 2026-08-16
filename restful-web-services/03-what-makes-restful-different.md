# 3장 RESTful 서비스는 무엇이 다른가

《RESTful Web Services》(Leonard Richardson, Sam Ruby, O'Reilly 2007) 3장 정리.

## 개요

앞선 장에서 다룬 실제 서비스들(del.icio.us, Flickr, Yahoo! 검색, Amazon E-Commerce Service)은 대부분 REST-RPC 하이브리드였다.
데이터를 가져올 때는 웹처럼 동작하지만, 데이터를 수정할 때는 RPC 스타일로 바뀌는 서비스들이다.
저자는 이들이 유용한 서비스이긴 해도 “웹처럼 동작하는” RESTful 설계의 예시로는 적합하지 않다고 본다.

이 장의 목적은 진짜로 RESTful하고 리소스 지향적인 서비스가 어떤 모습인지 보여주는 것이다.
그 사례로 두 가지 후보가 있는데, Atom Publishing Protocol(APP)과 Amazon Simple Storage Service(S3)이다.
APP는 실제 서비스라기보다 서비스를 만드는 방법에 대한 명세에 가깝기 때문에, 이 장에서는 웹의 특정 위치에 실재하는 S3를 중심으로 살펴본다(APP와 Atom, GData는 9장에서 다룬다).

이 장을 관통하는 핵심 주장은 다음과 같다.
잘 설계된 RESTful 서비스에서는 모든 것이 이름 그대로 동작한다.
서비스의 복잡성은 메서드 이름이 아니라 리소스 안에 담긴다.

## Simple Storage Service(S3) 소개

S3는 원하는 데이터를 원하는 구조로 저장하는 방법이다.
데이터를 비공개로 유지할 수도 있고, 웹 브라우저나 BitTorrent 클라이언트를 가진 누구나 접근할 수 있게 공개할 수도 있다.
Amazon이 저장 공간과 대역폭을 호스팅하며, 두 항목 모두 기가바이트 단위로 과금한다.

S3에는 크게 두 가지 용도가 있다.

첫째는 백업 서버로서의 용도다.
데이터를 S3에 저장하고 다른 누구에게도 접근 권한을 주지 않는다.
백업용 디스크를 직접 사는 대신 Amazon으로부터 디스크 공간을 빌리는 셈이다.

둘째는 데이터 호스트로서의 용도다.
데이터를 S3에 저장하고 다른 사람에게 접근 권한을 준다.
Amazon이 HTTP나 BitTorrent를 통해 데이터를 제공하므로, ISP에 대역폭 비용을 내는 대신 Amazon에 비용을 낸다.
많은 웹 스타트업이 데이터 파일을 서비스하기 위해 S3를 사용한다.

지금까지 살펴본 서비스들과 달리 S3는 기존 웹사이트에서 영감을 받은 것이 아니다.
amazon.com에는 HTML 폼을 채워 파일을 올리는 웹 페이지가 없다.
S3는 오직 프로그램에 의한 사용만을 의도한다(물론 데이터 호스트로 쓰면 최종 사용자는 웹 서비스 호출인 줄 모른 채 브라우저로 접근하게 된다).

Amazon은 Ruby, Python, Java, C#, Perl용 샘플 라이브러리를 제공하며, Ruby의 `AWS::S3` 같은 서드파티 라이브러리도 있다.

## S3의 객체 지향적 설계

S3는 두 개념 위에 세워진다. 버킷(bucket)과 객체(object)다.
객체는 이름이 붙은 데이터 조각으로, 약간의 메타데이터를 동반한다.
버킷은 객체를 담는, 이름이 붙은 컨테이너다.

버킷은 하드 드라이브의 파일 시스템에, 객체는 그 파일 시스템의 파일 하나에 비유할 수 있다.
버킷을 디렉터리에 비유하고 싶어지지만, 파일 시스템 디렉터리는 중첩이 가능한 반면 버킷은 중첩이 불가능하다.
버킷 안에 디렉터리 구조를 원한다면 객체 이름을 `directory/subdirectory/file-object`처럼 지어 흉내 내야 한다.

버킷에 관한 몇 가지 사항은 다음과 같다.
버킷에는 이름이라는 단 하나의 정보만 연결된다.
버킷 이름에는 A–Z, a–z, 0–9, 밑줄, 마침표, 대시만 쓸 수 있다(저자는 대문자를 피하라고 권한다).
버킷은 다른 버킷을 담을 수 없고 오직 객체만 담는다.
각 S3 사용자는 버킷을 100개까지만 가질 수 있으며, 버킷 이름은 다른 사용자의 것과 충돌할 수 없다(전역적으로 유일해야 한다).

객체에 관한 사항은 다음과 같다. 객체는 네 부분으로 이루어진다.

- 부모 버킷에 대한 참조
- 객체에 저장된 데이터(S3는 이를 “value”라 부른다)
- 이름(S3는 이를 “key”라 부른다)
- 객체에 연결된 메타데이터 키-값 쌍의 집합(대부분 사용자 정의 메타데이터이며, 표준 HTTP 헤더인 `Content-Type`과 `Content-Disposition` 값을 포함할 수도 있다)

예를 들어 O'Reilly 웹사이트를 S3에 호스팅한다면 `oreilly.com`이라는 버킷을 만들고, 키가 `“”`(빈 문자열), `catalog`, `catalog/9780596529260` 등인 객체들로 채우게 된다.
이 객체들은 각각 `http://oreilly.com/`, `http://oreilly.com/catalog` 같은 URI에 대응한다.
객체의 value는 O'Reilly 웹 페이지의 HTML 내용이고, `Content-Type` 메타데이터를 `text/html`로 설정하면 방문자는 이 객체를 HTML 문서로 제공받는다.

만약 S3가 웹 서비스가 아니라 객체 지향 코드 라이브러리였다면 `S3Bucket`과 `S3Object` 두 클래스가 있었을 것이다.
데이터 멤버에 대한 getter/setter 메서드(`S3Bucket#name`, `S3Object.value=`, `S3Bucket#addObject` 등)를 가지고, `S3Bucket#getObjects`는 객체 목록을, 클래스 메서드 `S3Bucket.getBuckets`는 모든 버킷을 반환했을 것이다.

```ruby
class S3Bucket
  # 모든 버킷을 가져오는 클래스 메서드
  def self.getBuckets
  end

  # 버킷 안의 객체들을 가져오는 인스턴스 메서드
  def getObjects
  end
end

class S3Object
  # 이 객체에 연결된 데이터를 가져온다
  def data
  end

  # 이 객체에 연결된 데이터를 설정한다
  def data=(new_value)
  end
end
```

## 리소스

Amazon은 S3를 서로 다른 두 웹 서비스로 노출한다.
하나는 평범한 HTTP 봉투(envelope)에 기반한 RESTful 서비스이고, 다른 하나는 SOAP 봉투에 기반한 RPC 스타일 서비스다.
RPC 스타일 서비스는 위 가상 라이브러리의 메서드와 비슷한 함수들(`ListAllMyBuckets`, `CreateBucket` 등)을 노출한다.
많은 RPC 스타일 웹 서비스는 구현 메서드로부터 자동 생성되며, 뒤에서 호출하는 프로그래밍 언어 코드와 동일한 인터페이스를 노출한다.
이것이 가능한 이유는 대부분의 현대 프로그래밍(객체 지향 포함)이 절차적이기 때문이다.

RESTful S3 서비스는 RPC 스타일 서비스의 모든 기능을 노출하지만, 사용자 정의 함수 이름 대신 리소스라는 표준 HTTP 객체를 노출한다.
`getObjects` 같은 사용자 정의 메서드 이름에 응답하는 대신, 리소스는 여섯 개의 표준 HTTP 메서드 중 하나 이상에 응답한다.
그 여섯 메서드는 GET, HEAD, POST, PUT, DELETE, OPTIONS다.

RESTful S3 서비스는 세 가지 유형의 리소스를 제공하며, 각 예시 URI는 다음과 같다.

- 버킷 목록(`https://s3.amazonaws.com/`). 이 유형의 리소스는 오직 하나뿐이다.
- 특정 버킷(`https://s3.amazonaws.com/{name-of-bucket}/`). 이 유형은 최대 100개까지 존재할 수 있다.
- 버킷 안의 특정 S3 객체(`https://s3.amazonaws.com/{name-of-bucket}/{name-of-object}`). 이 유형은 무한히 많이 존재할 수 있다.

가상 객체 지향 라이브러리의 각 메서드는 이 세 리소스 유형 중 하나에 대한 여섯 표준 메서드 중 하나에 대응한다.
getter인 `S3Object#name`은 “S3 객체” 리소스에 대한 GET 요청에 대응하고, setter인 `S3Object#value=`는 같은 리소스에 대한 PUT 요청에 대응한다.
`S3Bucket.getBuckets` 같은 팩토리 메서드와 `S3Bucket#getObjects` 같은 관계 메서드는 “버킷 목록”과 “버킷” 리소스에 대한 GET에 대응한다.

모든 리소스는 동일한 인터페이스를 노출하고 동일한 방식으로 동작한다.

- 객체의 value를 얻으려면 그 객체의 URI에 GET 요청을 보낸다.
- 객체의 메타데이터만 얻으려면 같은 URI에 HEAD 요청을 보낸다.
- 버킷을 만들려면 버킷 이름이 포함된 URI에 PUT 요청을 보낸다.
- 버킷에 객체를 추가하려면 버킷 이름과 객체 이름이 포함된 URI에 PUT을 보낸다.
- 버킷이나 객체를 삭제하려면 그 URI에 DELETE 요청을 보낸다.

S3 설계자들이 이것을 임의로 지어낸 것이 아니다.
HTTP 표준에 따르면 GET, HEAD, PUT, DELETE가 바로 이런 용도다.
이 네 메서드(그리고 S3가 쓰지 않는 POST, OPTIONS)만으로 웹상의 리소스와의 모든 상호작용을 기술하기에 충분하다.
프로그램을 웹 서비스로 노출하기 위해 새 어휘를 발명하거나 메서드 이름을 URI에 몰래 끼워 넣을 필요가 없다.
필요한 것은 리소스 설계를 신중히 고민하는 일뿐이다.
아무리 복잡한 REST 웹 서비스라도 동일한 기본 연산을 지원하며, 모든 복잡성은 리소스 안에 산다.

다음은 S3 리소스와 메서드의 대응을 정리한 표다(Table 3-1).

| 리소스                      | GET                                | PUT                              | DELETE    |
| --------------------------- | ---------------------------------- | -------------------------------- | --------- |
| 버킷 목록 (`/`)             | 버킷 목록을 나열                   | —                                | —         |
| 버킷 (`/{bucket}`)          | 버킷의 객체를 나열                 | 버킷 생성                        | 버킷 삭제 |
| 객체 (`/{bucket}/{object}`) | 객체의 value와 메타데이터를 가져옴 | 객체의 value와 메타데이터를 설정 | 객체 삭제 |

이 표는 언뜻 시시해 보인다. 모든 칸이 이름 그대로의 일을 하기 때문이다.
그리고 바로 그 점이 이 표를 실은 이유다.
잘 설계된 RESTful 서비스에서는 모든 것이 이름 그대로 동작한다.

리소스 설계 덕분에 두 가지가 자연스럽게 사라졌다는 점도 주목할 만하다.
“버킷 목록”이라는 리소스를 GET에만 응답하도록 새로 정의함으로써 `S3Bucket.getBuckets`가 필요 없어졌고, 모든 객체가 어떤 버킷에 속해야 한다는 설계 요구 때문에 `S3Bucket#addObject`도 그냥 없어졌다.

RPC 스타일 SOAP 인터페이스와 비교해 보자.
SOAP로 버킷 목록을 얻으려면 메서드 이름이 `ListAllMyBuckets`이고, 버킷 내용을 얻으려면 `ListBucket`이다.
RESTful 인터페이스에서는 언제나 GET이다.
RESTful 서비스에서는 URI가 (객체 지향적 의미의) 객체를 지정하고 메서드 이름은 표준화되어 있다.
같은 소수의 메서드가 여러 리소스와 서비스에 걸쳐 동일한 방식으로 동작한다.

## HTTP 응답 코드

RESTful 아키텍처를 규정하는 또 다른 특징은 HTTP 응답 코드의 사용이다.
S3에 요청을 보내고 문제없이 처리되면 대개 200(“OK”)을 돌려받는다.
무언가 잘못되면 응답 코드는 3xx, 4xx, 5xx 범위에 들어간다(예: 500 “Internal Server Error”).

오류 응답 코드는 메타데이터와 엔티티 본문(entity-body)을 요청에 대한 응답으로 해석하지 말라는 신호다.
그것은 클라이언트가 요청한 것이 아니라, 문제를 알리려는 서버의 시도다.
응답 코드는 문서나 메타데이터의 일부가 아니므로, 클라이언트는 응답의 첫 3바이트만 봐도 오류 발생 여부를 알 수 있다.

다음은 존재하지 않는 객체(`https://s3.amazonaws.com/crummy.com/nonexistent/object`)를 요청했을 때의 오류 응답 예시다(Example 3-2). 응답 코드는 404(“Not Found”)다.

```http
404 Not Found
Content-Type: application/xml
Date: Fri, 10 Nov 2006 20:04:45 GMT
Server: AmazonS3
Transfer-Encoding: chunked
x-amz-id-2: ...
x-amz-request-id: ED2168503ABB7BF4
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Error>
  <Code>NoSuchKey</Code>
  <Message>The specified key does not exist.</Message>
  <Key>nonexistent/object</Key>
  <RequestId>ED2168503ABB7BF4</RequestId>
  <HostId>...</HostId>
</Error>
```

HTTP 응답 코드는 사람 대상 웹(human web)에서는 과소 사용된다.
브라우저는 페이지를 요청할 때 응답 코드를 보여주지 않는다.
문서를 직접 보면 무엇이 잘못됐는지 알 수 있는데 굳이 숫자 코드를 볼 이유가 없기 때문이다.
그래서 웹 애플리케이션에서 오류가 나면 대부분 사람이 읽을 수 있는 오류 문서와 함께 200(“OK”)을 보낸다.
사람은 오류 문서를 요청한 문서로 착각할 가능성이 거의 없다.

프로그램 대상 웹(programmable web)에서는 정반대다.
컴퓨터 프로그램은 숫자 변수 값에 따라 다른 경로를 택하는 데는 능하지만, 문서가 무엇을 “의미”하는지 알아내는 데는 매우 서투르다.
사전에 약속된 규칙이 없으면, 프로그램은 XML 문서가 데이터를 담은 것인지 오류를 기술한 것인지 구분할 방법이 없다.
HTTP 응답 코드가 바로 그 규칙이며, 클라이언트가 HTTP 응답을 어떻게 다뤄야 하는지에 관한 대략적 관례다.
이는 엔티티 본문이나 메타데이터의 일부가 아니므로, 응답을 읽을 줄 몰라도 무슨 일이 일어났는지 이해할 수 있다.

S3는 200과 404 외에도 여러 응답 코드를 사용한다.

- 403(“Forbidden”): 가장 흔한 코드로, 올바른 자격 증명 없이 요청했을 때 사용된다.
- 400(“Bad Request”): 서버가 클라이언트가 보낸 데이터를 이해하지 못했음을 뜻한다.
- 409(“Conflict”): 비어 있지 않은 버킷을 삭제하려 할 때 보낸다.

전체 목록은 S3 기술 문서의 “The REST Error Response”에 있다.
공식 HTTP 응답 코드는 41개이지만, 일상적으로 중요한 것은 약 10개뿐이다(부록 B에서 모두 다룬다).

## S3 클라이언트

Amazon 샘플 라이브러리와 `AWS::S3` 같은 서드파티 기여로 사용자 정의 S3 클라이언트가 크게 필요 없어졌다.
하지만 저자는 REST 이론을 설명하기 위해 자신만의 Ruby S3 클라이언트를 직접 작성하며 하나씩 뜯어본다.

이 라이브러리는 S3 서비스 위에 객체 지향 인터페이스를 구현한다.
결과물은 ActiveRecord 같은 객체-관계 매퍼(object-relational mapper)와 비슷해 보이는데, 다만 뒤에서 SQL 호출로 데이터베이스에 저장하는 대신 HTTP 요청으로 S3에 저장한다는 점이 다르다.
메서드 이름도 `getBuckets`, `getObjects` 같은 리소스별 이름 대신 밑바탕의 RESTful 인터페이스를 반영하는 `get`, `put` 등을 쓴다.

초기 코드는 HTTP 요청과 응답 파싱, 그리고 요청 서명에 필요한 라이브러리를 불러오고, 모든 것을 감싸는 큰 `S3` 모듈을 시작한다.
그 안의 `S3::Authorized` 모듈에는 공개 키(Amazon이 “Access Key ID”라 부름)와 개인 키(Amazon이 “Secret Access Key”라 부름)를 넣는다.

```ruby
require 'rubygems'
require 'rest-open-uri'
require 'rexml/document'

# 요청 서명에 필요한 라이브러리
require 'openssl'
require 'digest/sha1'
require 'base64'
require 'uri'

module S3
  module Authorized
    @@public_key = ''
    @@private_key = ''

    if @@public_key.empty? or @@private_key.empty?
      raise "You need to set your S3 keys."
    end

    HOST = 'https://s3.amazonaws.com/'
  end
```

모든 S3 요청에는 Amazon이 사용자를 식별할 수 있도록 공개 키가 포함된다.
그리고 모든 요청은 개인 키로 암호학적으로 서명되어야 Amazon이 정말 본인이 보낸 요청임을 알 수 있다.
저자는 표준 암호학 용어를 쓰지만, 여기서 “개인 키”는 완전히 비밀은 아니다(Amazon도 알고 있다).
다만 남에게 절대 드러내서는 안 된다는 의미에서 개인 키다.
드러내면 그 사람이 요청을 보내고 비용은 사용자에게 청구된다.

버킷 목록 리소스를 위한 클래스는 `S3::BucketList`다.
`get`은 버킷 목록 URI에 GET 요청을 보내 XML 문서를 읽고, 모든 버킷마다 `Bucket` 객체를 만들어 리스트에 담는다.

```ruby
class BucketList
  include Authorized

  def get
    buckets = []
    # 버킷 목록 URI에 GET 요청을 보내 XML 문서를 읽는다
    doc = REXML::Document.new(open(HOST).read)
    REXML::XPath.each(doc, "//Bucket/Name") do |e|
      buckets << Bucket.new(e.text) if e.text
    end
    return buckets
  end
end
```

여기서 XPath 표현식 `//Bucket/Name`은 오른쪽에서 왼쪽으로 읽으면 “문서 어디에서든(`//`) `Bucket` 태그의 직접 자식인(`Bucket/`) 모든 `Name` 태그를 찾아라”라는 뜻이다.

`S3::BucketList#get`을 호출하면 `https://s3.amazonaws.com/`에 안전한 HTTP GET 요청이 나가고, S3는 아래와 같은 XML 문서를 돌려준다(Example 3-5).
이것이 다음 장부터 “표현(representation)”이라 부를 것으로, 리소스의 현재 상태에 대한 정보다.

```xml
<?xml version='1.0' encoding='UTF-8'?>
<ListAllMyBucketsResult xmlns='http://s3.amazonaws.com/doc/2006-03-01/'>
  <Owner>
    <ID>c0363f...aad70</ID>
    <DisplayName>leonardr28</DisplayName>
  </Owner>
  <Buckets>
    <Bucket>
      <Name>crummy.com</Name>
      <CreationDate>2006-10-26T18:46:45.000Z</CreationDate>
    </Bucket>
  </Buckets>
</ListAllMyBucketsResult>
```

이 문서에서 눈에 띄는 문제는 링크가 없다는 점이다.
문서는 모든 버킷의 이름을 알려주지만, 그 버킷을 웹의 어디에서 찾을 수 있는지는 말하지 않는다.
REST 설계 기준의 관점에서 이것이 Amazon S3의 주요 약점이다.
다행히 클라이언트가 버킷 이름으로부터 URI를 계산하도록 프로그래밍하기는 어렵지 않다(`https://s3.amazonaws.com/{name-of-bucket}` 규칙을 따르면 된다).

다음은 `S3::Bucket` 클래스다.
버킷의 URI는 서비스 루트에 버킷 이름을 붙인 것이다.
`put`은 버킷 URI에 PUT 요청을 보내고, `delete`는 DELETE 요청을 보낸다.

```ruby
class Bucket
  include Authorized
  attr_accessor :name

  def initialize(name)
    @name = name
  end

  # 버킷의 URI는 서비스 루트 + 버킷 이름
  def uri
    HOST + URI.escape(name)
  end

  # 이 버킷을 S3에 저장한다. ActiveRecord::Base#save와 유사하다.
  def put(acl_policy=nil)
    args = {:method => :put}
    args["x-amz-acl"] = acl_policy if acl_policy
    open(uri, args)
    return self
  end

  # 이 버킷을 삭제한다. 버킷이 비어 있지 않으면 HTTP 409("Conflict")로 실패한다.
  def delete
    open(uri, :method => :delete)
  end
```

버킷 URI가 버킷을 유일하게 식별하므로 삭제는 단순하다. 버킷 URI에 DELETE를 보내면 끝이다.
버킷 이름이 URI에 들어가고 버킷에는 그 외 설정 가능한 속성이 없으므로 생성도 쉽다. URI에 PUT을 보내면 된다.

다만 `S3::Bucket#put`은 ActiveRecord의 `save`와 조금 다르게 동작한다.
ActiveRecord가 통제하는 데이터베이스 테이블의 행은 숫자로 된 고유 ID를 가진다.
ID가 23인 객체의 이름을 바꾸면 `SET name=“newname” WHERE id=23`처럼 ID 23인 레코드에 변경이 반영된다.
반면 S3 버킷의 영구 ID는 URI이고, URI에는 이름이 들어 있다.
버킷 이름을 바꾸고 `put`을 호출하면, 클라이언트는 기존 버킷의 이름을 바꾸는 것이 아니라 새 이름을 가진 새 URI에 비어 있는 새 버킷을 만든다.
이는 S3 프로그래머의 설계 결정에 따른 것이지 반드시 이래야 하는 것은 아니다.
예컨대 Ruby on Rails는 데이터베이스 행을 노출할 때 `/buckets/23`처럼 숫자 ID를 URI에 넣으므로 이름을 바꿔도 URI가 바뀌지 않는다.

`S3::Bucket`의 `get`은 버킷 리소스의 URI에 GET을 보내 XML을 가져와 Ruby 객체로 파싱한다.
`:Prefix`, `:Marker`, `:Delimiter`, `:MaxKeys` 같은 옵션으로 버킷 내용을 필터링할 수 있다.
반환값의 두 번째 값은 목록이 잘렸는지 여부(`//IsTruncated`)를 나타낸다.

```ruby
  def get(options={})
    uri = uri()
    suffix = '?'
    options.each do |param, value|
      if [:Prefix, :Marker, :Delimiter, :MaxKeys].member? param
        uri << suffix << param.to_s << '=' << URI.escape(value)
        suffix = '&'
      end
    end
    doc = REXML::Document.new(open(uri).read)
    there_are_more = REXML::XPath.first(doc, "//IsTruncated").text == "true"
    objects = []
    REXML::XPath.each(doc, "//Contents/Key") do |e|
      objects << Object.new(self, e.text) if e.text
    end
    return objects, there_are_more
  end
end
```

버킷 리소스의 URI에 GET을 보내면 버킷의 각 원소마다 `Contents` 태그를 담은 표현을 얻는다(Example 3-8).

```xml
<?xml version='1.0' encoding='UTF-8'?>
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Name>crummy.com</Name>
  <Prefix></Prefix>
  <Marker></Marker>
  <MaxKeys>1000</MaxKeys>
  <IsTruncated>false</IsTruncated>
  <Contents>
    <Key>mydocument</Key>
    <LastModified>2006-10-27T16:01:19.000Z</LastModified>
    <ETag>"93bede57fd3818f93eedce0def329cc7"</ETag>
    <Size>22</Size>
    <Owner>
      <ID>c0363f...aad70</ID>
      <DisplayName>leonardr28</DisplayName>
    </Owner>
    <StorageClass>STANDARD</StorageClass>
  </Contents>
</ListBucketResult>
```

여기서도 표현에서 빠진 핵심은 링크다.
문서는 객체 정보를 많이 담지만 그 URI는 담지 않으므로, 클라이언트가 객체 이름으로부터 URI를 만들어야 한다(`https://s3.amazonaws.com/{name-of-bucket}/{name-of-object}`).

이제 S3 서비스의 핵심인 객체를 위한 `S3::Object`다.
S3 객체는 이름(key)과 메타데이터 키-값 쌍이 부여된 데이터 문자열일 뿐이다.
버킷 목록이나 버킷에 GET을 보내면 파싱해야 할 XML 문서를 받지만, 객체에 GET을 보내면 이전에 PUT한 데이터 문자열을 바이트 그대로 받는다.

```ruby
class Object
  include Authorized
  attr_reader :bucket
  attr_accessor :name
  attr_writer :metadata, :value

  def initialize(bucket, name, value=nil, metadata=nil)
    @bucket, @name, @value, @metadata = bucket, name, value, metadata
  end

  # 객체의 URI는 버킷의 URI + 객체 이름
  def uri
    @bucket.uri + '/' + URI.escape(name)
  end
```

`metadata` 메서드는 HTTP HEAD 요청으로 객체의 메타데이터만 가져와 `@metadata` 해시를 채운다.
객체가 존재하지 않아 404가 나오면 메타데이터가 없는 것일 뿐 오류가 아니므로 빈 해시로 처리하고, 그 외의 오류는 다시 던진다.

```ruby
  def metadata
    unless @metadata
      begin
        # 객체 URI에 HEAD 요청을 보내 응답 헤더에서 메타데이터를 읽는다
        store_metadata(open(uri, :method => :head).meta)
      rescue OpenURI::HTTPError => e
        if e.io.status == ["404", "Not Found"]
          @metadata = {}
        else
          raise e
        end
      end
    end
    return @metadata
  end
```

여기서 목표는 객체 자체를 가져오지 않고 메타데이터만 가져오는 것이다.
이는 영화 리뷰를 내려받는 것과 영화 자체를 내려받는 것의 차이이며, 대역폭에 비용을 지불할 때 큰 차이가 된다.
메타데이터와 표현의 이런 구분은 S3에만 있는 것이 아니라 모든 리소스 지향 웹 서비스에 일반적으로 적용된다.
HEAD 메서드는 (아마도 거대할) 표현을 함께 가져오지 않고도 어떤 리소스의 메타데이터를 가져오는 방법을 제공한다.

물론 실제로 “영화”를 내려받고 싶을 때는 GET을 쓴다.
`value` 메서드는 그 구조가 `metadata`와 대칭적이다.

```ruby
  def value
    unless @value
      response = open(uri)   # 객체 URI에 GET 요청
      store_metadata(response.meta) unless @metadata
      @value = response.read # 엔티티 본문에서 value를 읽는다
    end
    return @value
  end
```

객체를 저장하는 것도 버킷과 같은 방식, 즉 URI에 PUT 요청을 보내는 것이다.
다만 버킷 PUT은 버킷에 이름 외에 구별되는 특징이 없어 단순한 반면, 객체 PUT은 여기서 메타데이터(`Content-Type` 등)와 value를 함께 지정하므로 더 복잡하다.
객체의 value는 클라이언트가 말하는 그대로이므로 XML로 감쌀 필요 없이 데이터를 있는 그대로 보내고, 메타데이터 해시의 각 항목에 대응하는 HTTP 헤더를 설정한다.

```ruby
  def put(acl_policy=nil)
    args = @metadata ? @metadata.clone : {}
    args[:method] = :put
    args["x-amz-acl"] = acl_policy if acl_policy
    if @value
      args["Content-Length"] = @value.size.to_s
      args[:body] = @value
    end
    open(uri, args)  # 객체 URI에 PUT 요청
    return self
  end

  # 이 객체를 삭제한다. S3::Bucket#delete와 동일하다.
  def delete
    open(uri, :method => :delete)
  end
```

HTTP 응답 헤더를 S3 객체 메타데이터로 바꾸는 메서드는 다음과 같다.
`Content-Type`을 제외하고, 설정하는 모든 메타데이터 헤더에는 `x-amz-meta-` 접두사를 붙여야 한다.
그렇지 않으면 S3 서버까지 왕복하지 못하고, S3는 그것을 클라이언트 소프트웨어의 특이 사항으로 여겨 버린다.

```ruby
  private

  def store_metadata(new_metadata)
    @metadata = {}
    new_metadata.each do |h, v|
      if RELEVANT_HEADERS.member?(h) || h.index('x-amz-meta') == 0
        @metadata[h] = v
      end
    end
  end

  RELEVANT_HEADERS = ['content-type', 'content-disposition',
                      'content-range', 'x-amz-missing-meta']
end
```

## 요청 서명과 접근 제어

지금까지의 코드는 HTTP 요청을 제대로 보내지만, S3는 이를 거부한다.
결정적으로 중요한 `Authorization` 헤더가 없어서, S3가 사용자가 자기 버킷의 소유자임을 증명할 방법이 없기 때문이다.
Amazon은 저장 데이터와 전송 대역폭에 과금하므로, 인증 없이 요청을 받아들이면 누구나 남의 버킷에 데이터를 넣고 그 비용을 소유자에게 물릴 수 있다.

대부분의 인증이 필요한 웹 서비스는 표준 HTTP 메커니즘으로 신원을 확인한다.
그러나 S3의 요구는 더 복잡하다.
보통은 남이 자기 데이터를 쓰기를 원치 않지만, S3의 용도 중 하나는 호스팅이기 때문이다.
큰 영화 파일을 S3에 올려 누구나 BitTorrent로 내려받게 하고 비용은 Amazon이 자신에게 청구하게 만들 수 있다.
또는 S3에 저장된 영화 파일에 대한 접근을 판매할 수도 있다.
전자상거래 사이트가 고객에게 결제를 받고 영화를 내려받을 S3 URI를 건네주는 식이다.
이는 특정 웹 서비스 호출(GET 요청)을 자신으로서 수행할 권리를 타인에게 위임하고, 그 비용은 자기 계정에 청구되게 하는 것이다.

표준 HTTP 인증으로는 이런 응용에 보안을 제공할 수 없다.
보통은 요청을 보내는 사람이 실제 비밀번호를 알아야 하며, “여기 내 비밀번호가 있는데, 이 URI 하나를 요청하는 데만 써야 한다”라고 남에게 말할 수는 없다.

이것이 공개 키 암호화(public-key cryptography)가 필요한 지점이다.
S3 요청을 할 때마다 “개인” 키로 요청의 중요한 부분, 즉 URI, HTTP 메서드, 몇몇 HTTP 헤더에 서명한다.
개인 키를 가진 사람만이 이 서명을 만들 수 있으므로 Amazon은 사용자에게 과금해도 됨을 안다.
그러나 일단 요청에 서명하면, 개인 키를 드러내지 않고도 그 서명을 제3자에게 보낼 수 있다.
제3자는 서명된 것과 동일한 HTTP 요청을 보낼 수 있고, 비용은 서명한 사람에게 청구된다.
요컨대 다른 사람이 개인 키를 몰라도 제한된 시간 동안 특정 요청을 나로서 수행할 수 있다.

이제 `S3::Authorized` 모듈을 다시 열어 `open` 메서드 호출을 가로채 요청에 서명하는 능력을 부여한다.
`BucketList`, `Bucket`, `Object`가 모두 이 모듈을 include했으므로 정의만 하면 이 능력을 상속한다.
이 코드가 없으면 앞서의 모든 `open` 호출은 서명되지 않은 요청을 보내 403(“Forbidden”)으로 튕겨 나온다.

```ruby
module Authorized
  # 요청 서명 목적에서 S3가 중요하게 여기는 표준 HTTP 헤더
  INTERESTING_HEADERS = ['content-type', 'content-md5', 'date']
  # 사용자 정의 메타데이터 헤더 접두사. 이런 헤더는 모두 서명에 포함된다.
  AMAZON_HEADER_PREFIX = 'x-amz-'

  def open(uri, headers_and_options={}, *args, &block)
    headers_and_options = headers_and_options.dup
    headers_and_options['Date'] ||= Time.now.httpdate
    headers_and_options['Content-Type'] ||= ''
    signed = signature(uri, headers_and_options[:method] || :get,
                       headers_and_options)
    headers_and_options['Authorization'] = "AWS #{@@public_key}:#{signed}"
    Kernel::open(uri, headers_and_options, *args, &block)
  end
```

핵심 작업은 `signature` 메서드에 있다.
이 메서드는 `Authorization` 헤더에 들어갈, 요청에 관한 모든 중요한 정보를 담은 “정규 문자열(canonical string)”에 개인 키로 서명한 결과를 만든다.
URI는 문자열이나 Ruby URI 객체로 받을 수 있으며, 경로(path)를 뽑아 `canonical_string`을 만든 뒤 `sign`으로 서명한다.

```ruby
  def signature(uri, method=:get, headers={}, expires=nil)
    if uri.respond_to? :path
      path = uri.path
    else
      uri = URI.parse(uri)
      path = uri.path + (uri.query ? "?" + uri.query : "")
    end
    signed_string = sign(canonical_string(method, path, headers, expires))
  end
```

정규 문자열은 HTTP 요청을 특정 형식의 문자열로 바꾼 것으로, S3 관점에서 요청에 관한 모든 흥미로운 정보를 담는다.
그 정보는 HTTP 메서드(`PUT`), `Content-Type`(`text/plain`), 날짜, 몇몇 HTTP 헤더(`x-amz-metadata`), 그리고 URI의 경로 부분(`/crummy.com/myobject`)이다.
누구나 이 문자열을 만들 수 있지만, 올바른 서명을 만드는 방법은 S3 계정 소유자와 Amazon만 안다.

```text
PUT
text/plain
Fri, 27 Oct 2006 21:22:41 GMT
x-amz-metadata:Here's some metadata for the myobject object.
/crummy.com/myobject
```

Amazon 서버는 요청을 받으면 같은 정규 문자열을 만들어 (소유자의 비밀 키를 알고 있으므로) 서명하고, 두 서명이 일치하는지 본다.
일치하면 요청이 통과하고, 아니면 403(“Forbidden”)을 받는다. 이것이 S3 인증의 작동 방식이다.

정규 문자열을 생성하는 코드는 다음과 같다.
흥미로운 헤더들의 기본값을 잡고, 실제 값과 사용자 정의 S3 헤더 값을 채운 뒤, HTTP 메서드로 시작해 헤더들을 이름순으로 정렬해 덧붙이고, 마지막에 URI 경로를 붙인다.
경로에서는 쿼리 문자열을 떼되, 필요하면 `acl`, `torrent`, `logging` 같은 특수 S3 쿼리 파라미터를 다시 붙인다.

```ruby
  def canonical_string(method, path, headers, expires=nil)
    sign_headers = {}
    INTERESTING_HEADERS.each { |header| sign_headers[header] = '' }
    headers.each do |header, value|
      if header.respond_to? :to_str
        header = header.downcase
        if INTERESTING_HEADERS.member?(header) ||
           header.index(AMAZON_HEADER_PREFIX) == 0
          sign_headers[header] = value.to_s.strip
        end
      end
    end
    # x-amz-date가 있으면 표준 Date 헤더는 비운다
    sign_headers['date'] = '' if sign_headers.has_key? 'x-amz-date'
    # 만료 시각이 주어지면 Date를 덮어쓴다. 서명은 그때까지 유효하다.
    sign_headers['date'] = expires.to_s if expires

    canonical = method.to_s.upcase + "\n"
    sign_headers.sort_by { |h| h[0] }.each do |header, value|
      canonical << header << ":" if header.index(AMAZON_HEADER_PREFIX) == 0
      canonical << value << "\n"
    end
    canonical << path.gsub(/\?.*$/, '')
    for param in ['acl', 'torrent', 'logging']
      if path =~ Regexp.new("[&?]#{param}($|&|=)")
        canonical << "?" << param
        break
      end
    end
    return canonical
  end
```

`sign`은 Ruby의 표준 암호화·인코딩 인터페이스를 감싸는 배관 작업이다.
비밀 접근 키로 문자열을 SHA-1 HMAC 서명한 뒤, 그 이진 결과를 base64로 평문 ASCII로 인코딩한다.

```ruby
  def sign(str)
    digest_generator = OpenSSL::Digest::Digest.new('sha1')
    digest = OpenSSL::HMAC.digest(digest_generator, @@private_key, str)
    return Base64.encode64(digest).strip
  end
```

### URI 서명하기

마지막 기능은 HTTP 요청에 서명해 그 URI를 남에게 주어, 그가 나로서 그 요청을 하게 만드는 것이다.
`open`으로 요청하는 대신 `open` 인자를 `signed_uri`에 넘기면 누구나 나로서 쓸 수 있는 서명된 URI를 돌려받는다.
남용을 막기 위해 서명된 URI는 제한된 시간 동안만 유효하며, `:expires` 키워드 인자로 그 시간을 지정할 수 있다(기본 15분).

```ruby
  def signed_uri(headers_and_options={})
    expires = headers_and_options[:expires] || (Time.now.to_i + (15 * 60))
    expires = expires.to_i if expires.respond_to? :to_i
    headers_and_options.delete(:expires)
    signature = URI.escape(signature(uri, headers_and_options[:method],
                                     headers_and_options, nil))
    q = (uri.index("?")) ? "&" : "?"
    "#{uri}#{q}Signature=#{signature}&Expires=#{expires}&AWSAccessKeyId=#{@@public_key}"
  end
end
```

예를 들어 `https://s3.amazonaws.com/BobProductions/KomodoDragon.avi`에 대한 접근을 고객에게 주려면 다음처럼 URI를 생성한다.

```ruby
require 'S3lib'
bucket = S3::Bucket.new("BobProductions")
object = S3::Object.new(bucket, "KomodoDragon.avi")
puts object.signed_uri
# https://s3.amazonaws.com/BobProductions/KomodoDragon.avi
#   ?Signature=D%2Fu6kxT3jOzHaFXjsLbowgpzExQ%3D
#   &Expires=1162156499&AWSAccessKeyId=0F9DBXKB5274JKTJ8DG2
```

이 URI는 기본 15분간 유효하며 공개 키(`AWSAccessKeyId`), 만료 시각(`Expires`), 암호학적 서명(`Signature`)을 담는다.
고객이 URI의 어느 부분이라도 수정하면(예: 다른 영화를 받으려 하면) S3가 거부한다.
URI를 친구들에게 뿌릴 수는 있어도 15분이 지나면 작동을 멈춘다.

여기에는 주의할 점이 있다.
정규 문자열에는 보통 `Date` 헤더 값이 들어가는데, 고객이 URI를 방문할 때 그의 브라우저는 다른 `Date` 값을 보낸다.
그래서 남에게 줄 정규 문자열을 만들 때는 요청 날짜 대신 만료 날짜를 설정하며, 만료 날짜가 주어지면 `canonical_string`에서 `Date` 헤더 값을 덮어쓴다.

### 접근 정책 설정하기

객체를 공개적으로 접근 가능하게 만들려면 어떻게 할까.
만료 날짜를 아주 먼 미래로 두고 거대한 서명 URI를 뿌릴 수도 있지만, 더 쉬운 방법은 익명 접근을 허용하는 것이다.
버킷이나 객체를 만드는 PUT 요청에 `x-amz-acl` 헤더를 실어 접근 정책을 설정하면 S3가 서명되지 않은 요청에도 응답하게 된다.
그것이 바로 `Bucket#put`과 `Object#put`의 `acl_policy` 인자가 하는 일이다.

```ruby
require 'S3lib'
bucket = S3::Bucket.new("BobProductions")
object = S3::Object.new(bucket, "KomodoDragon-Trailer.avi")
object.put("public-read")
```

S3는 네 가지 접근 정책을 이해한다.

- `private`: 기본값. “개인” 키로 서명된 요청만 받아들인다.
- `public-read`: 서명되지 않은 GET 요청을 받아들인다. 누구나 객체를 내려받거나 버킷을 나열할 수 있다.
- `public-write`: 서명되지 않은 GET과 PUT 요청을 받아들인다. 누구나 객체를 수정하거나 버킷에 객체를 추가할 수 있다.
- `authenticated-read`: 서명되지 않은 요청은 거부하지만, 읽기 요청은 자신뿐 아니라 임의의 S3 사용자의 “개인” 키로 서명될 수 있다. 즉 S3 계정을 가진 누구나 객체를 내려받거나 버킷을 나열할 수 있다.

더 세밀하게 접근을 부여하는 방법도 있다(이 장에서는 다루지 않는다).
S3 기술 문서의 “Setting Access Policy with REST”를 보면 별도의 리소스 세계가 드러난다.
모든 버킷 `/{name-of-bucket}`에는 그 버킷의 접근 제어 규칙에 대응하는 그림자 리소스 `/{name-of-bucket}?acl`이 있고, 모든 객체에도 그림자 ACL 리소스 `/{name-of-bucket}/{name-of-object}?acl`이 있다.
이 URI들에 PUT 요청을 보내고 요청 엔티티 본문에 접근 제어 목록의 XML 표현을 실으면 특정 권한을 설정하고 특정 S3 사용자로 접근을 제한할 수 있다.

## S3 클라이언트 라이브러리 사용하기

이제 S3 서비스의 거의 모든 기능에 접근하는 Ruby 클라이언트 라이브러리가 완성됐다.
다음은 버킷과 객체를 만들고 버킷 내용을 나열하는 간단한 명령줄 클라이언트로, S3 리소스들이 함께 동작하는 큰 그림을 보여준다.
HTTP 요청을 일으키는 줄에는 오른쪽에 어떤 요청이 나가는지 주석을 달았다.

```ruby
require 'S3lib'

bucket_name, object_name, object_value = ARGV
unless bucket_name
  puts "Usage: #{$0} [bucket name] [object name] [object value]"
  exit
end

# 버킷을 찾거나 만든다
buckets = S3::BucketList.new.get              # GET /
bucket = buckets.detect { |b| b.name == bucket_name }
if bucket
  puts "Found bucket #{bucket_name}."
else
  puts "Could not find bucket #{bucket_name}, creating it."
  bucket = S3::Bucket.new(bucket_name)
  bucket.put                                  # PUT /{bucket}
end

# 객체를 만든다
object = S3::Object.new(bucket, object_name)
object.metadata['content-type'] = 'text/plain'
object.value = object_value
object.put                                    # PUT /{bucket}/{object}

# 버킷 안의 각 객체에 대해...
bucket.get[0].each do |o|                     # GET /{bucket}
  puts "Name: #{o.name}"
  puts "Value: #{o.value}"                    # GET /{bucket}/{object}
  puts "Metadata hash: #{o.metadata.inspect}"
  puts
end
```

## ActiveResource로 투명해진 클라이언트

모든 RESTful 웹 서비스가 기본적으로 같은 단순한 인터페이스를 노출하므로, 서비스마다 클라이언트를 새로 쓰는 것은 큰일은 아니지만 다소 낭비다.
두 가지 대안이 있다.
하나는 서비스를 WADL 파일로 기술하고 범용 WADL 클라이언트로 접근하는 것이고, 다른 하나는 특정 종류의 웹 서비스에 대한 클라이언트를 아주 쉽게 쓰게 해주는 Ruby 라이브러리 ActiveResource다.

ActiveResource는 관계형 데이터베이스의 행과 테이블을 노출하는 웹 서비스를 겨냥해 설계됐다.
WADL은 거의 모든 종류의 웹 서비스를 기술할 수 있지만, ActiveResource는 특정 관례를 따르는 서비스에서만 클라이언트로 동작한다.
집필 시점에 그 관례를 따르는 프레임워크는 Ruby on Rails가 유일하다.
그러나 어떤 웹 서비스든 Rails와 같은 RESTful 인터페이스로 데이터베이스를 노출하기만 하면 ActiveResource 클라이언트의 요청에 응답할 수 있다.

### 간단한 서비스 만들기

예시를 위해 저자는 타임스탬프가 붙은 메모를 남기는 간단한 노트북 서비스를 Rails로 만든다.

```text
rails notebook
cd notebook
```

`notebook_development` 데이터베이스를 만들고 `config/database.yml`을 편집한 뒤, `scaffold_resource` 제너레이터로 RESTful 웹 서비스 코드를 생성한다.
메모에는 타임스탬프와 본문 텍스트가 필요하다.

```text
ruby script/generate scaffold_resource note date:date body:text
```

이 명령은 “note” 객체를 위한 모델, 뷰, 컨트롤러 코드 일습을 생성한다.
`db/migrate/001_create_notes.rb`에는 고유 ID, `date`, `body` 세 필드를 가진 `notes` 테이블을 만드는 코드가 있다.
`app/models/note.rb`의 모델 코드는 테이블에 대한 ActiveResource 인터페이스를 제공하고, `app/controllers/notes_controller.rb`의 컨트롤러 코드는 그 인터페이스를 HTTP로 세상에 노출하며, `app/views/notes`의 뷰는 사용자 인터페이스를 정의한다.

데이터베이스를 초기화하고 서버를 띄운다.

```text
rake db:migrate
script/server
=> Booting WEBrick...
=> Rails application started on http://0.0.0.0:3000
```

### ActiveResource 클라이언트

생성된 애플리케이션은 웹 서비스이자 웹 애플리케이션이다.
브라우저로 `http://localhost:3000/notes`를 방문해 메모를 만들 수 있고, Rails 1.2에서는 생성된 모델과 컨트롤러가 RESTful 웹 서비스로도 작동해 프로그램 클라이언트가 브라우저만큼 쉽게 접근할 수 있다.

다만 집필 시점에 ActiveResource 클라이언트 자체는 Rails 1.2와 함께 배포되지 않았고 Rails 개발 트렁크에서 개발 중이었으므로, Subversion에서 체크아웃해야 했다.

```text
svn co http://dev.rubyonrails.org/svn/rails/trunk activeresource_client
cd activeresource_client
```

다음은 메모를 만들고 수정하고 목록을 보고, 방금 만든 메모를 삭제하는 ActiveResource 클라이언트다.
HTTP 클라이언트나 XML 파싱 코드를 전혀 쓰지 않는다는 점이 핵심이다.

```ruby
require 'activesupport/lib/active_support'
require 'activeresource/lib/active_resource'

# 사이트가 노출하는 객체에 대한 모델 정의
class Note < ActiveResource::Base
  self.site = 'http://localhost:3000/'
end

def show_notes
  notes = Note.find :all                 # GET /notes.xml
  puts "I see #{notes.size} note(s):"
  notes.each do |note|
    puts " #{note.date}: #{note.body}"
  end
end

new_note = Note.new(:date => Time.now, :body => "A test note")
new_note.save                            # POST /notes.xml
new_note.body = "This note has been modified."
new_note.save                            # PUT /notes/{id}.xml
show_notes
new_note.destroy                         # DELETE /notes/{id}.xml
puts
show_notes
```

ActiveRecord에 익숙하다면 ActiveResource 인터페이스가 거의 똑같아 보인다.
두 라이브러리 모두 균일한 인터페이스를 노출하는 다양한 객체에 대한 객체 지향 인터페이스를 제공한다.
ActiveRecord에서는 객체가 데이터베이스에 살며 SQL의 SELECT, INSERT, UPDATE, DELETE로 노출되고, ActiveResource에서는 객체가 Rails 애플리케이션에 살며 HTTP의 GET, POST, PUT, DELETE로 노출된다.

클라이언트를 실행할 때 Rails 서버 로그에 남는 요청은 코드의 주석과 정확히 대응한다.

```text
"POST /notes.xml HTTP/1.1" 201
"PUT /notes/5.xml HTTP/1.1" 200
"GET /notes.xml HTTP/1.1" 200
"DELETE /notes/5.xml HTTP/1.1" 200
"GET /notes.xml HTTP/1.1" 200
```

여기서 벌어지는 일은 S3에 대한 요청과 같다. HTTP의 균일한 인터페이스를 통한 리소스 접근이다.
노트북 서비스는 두 종류의 리소스를 노출한다.

- 메모 목록(`/notes.xml`). S3 버킷(객체 목록)에 대응한다.
- 하나의 메모(`/notes/{id}.xml`). S3 객체에 대응한다.

이 리소스들은 S3 리소스처럼 GET, PUT, DELETE를 노출한다.
메모 목록은 새 메모를 만들기 위한 POST도 지원한다.
객체를 PUT으로 만드는 S3와는 조금 다르지만, 그 역시 마찬가지로 RESTful하다.

클라이언트가 동작할 때 클라이언트와 서버 사이에서는 XML 문서가 눈에 보이지 않게 오간다.
GET 응답 본문과 PUT 요청 본문은 각각 다음과 같이 밑바탕 데이터베이스 행을 단순히 묘사한 것이다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<notes>
  <note>
    <body>What if I wrote a book about REST?</body>
    <date type="date">2006-06-05</date>
    <id type="integer">2</id>
  </note>
  <note>
    <body>Pasta for lunch maybe?</body>
    <date type="date">2006-12-18</date>
    <id type="integer">3</id>
  </note>
</notes>
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<note>
  <body>This note has been modified.</body>
</note>
```

### 같은 서비스를 위한 Python 클라이언트

현재 ActiveResource 클라이언트 라이브러리는 Ruby용뿐이고 ActiveResource 호환 서비스를 노출하는 프레임워크는 Rails뿐이다.
그러나 여기서 일어나는 일은 특정 URI에 XML 문서를 넣고 XML 문서를 돌려받는 HTTP 요청뿐이므로, 다른 언어의 클라이언트가 그 문서들을 보내지 못할 이유도, 다른 프레임워크가 같은 URI를 노출하지 못할 이유도 없다.

다음은 앞의 Ruby 클라이언트를 Python으로 구현한 것이다.
ActiveResource에 의존할 수 없어 XML 문서를 직접 만들고 HTTP 요청을 직접 보내야 하므로 Ruby판보다 길지만, 구조는 거의 같다.

```python
from elementtree.ElementTree import Element, SubElement, tostring
from elementtree import ElementTree
import httplib2
import time

BASE = "http://localhost:3000/"
client = httplib2.Http(".cache")

def showNotes():
    headers, xml = client.request(BASE + "notes.xml")
    doc = ElementTree.fromstring(xml)
    for note in doc.findall('note'):
        print "%s: %s" % (note.find('date').text, note.find('body').text)

newNote = Element("note")
date = SubElement(newNote, "date")
date.attrib['type'] = "date"
date.text = time.strftime("%Y-%m-%d", time.localtime())
body = SubElement(newNote, "body")
body.text = "A test note"
headers, ignore = client.request(BASE + "notes.xml", "POST",
                                 body=tostring(newNote),
                                 headers={'content-type': 'application/xml'})
newURI = headers['location']

modifiedBody = Element("note")
body = SubElement(modifiedBody, "body")
body.text = "This note has been modified"
client.request(newURI, "PUT",
               body=tostring(modifiedBody),
               headers={'content-type': 'application/xml'})
showNotes()

client.request(newURI, "DELETE")
print
showNotes()
```

## 맺는말

RESTful 웹 서비스는 단순하고 잘 정의된 인터페이스를 가지므로, 복제하거나 한 구현을 다른 구현으로 갈아 끼우기가 어렵지 않다.
Park Place는 S3와 동일한 HTTP 인터페이스를 노출하는 Ruby 애플리케이션으로, 이를 이용해 자신만의 S3를 호스팅할 수 있다.
S3 라이브러리와 클라이언트 프로그램은 `https://s3.amazonaws.com/`을 상대로 하듯 Park Place 서버를 상대로도 그대로 작동한다.

ActiveResource를 복제하는 것도 가능하다.
아직 아무도 하지 않았지만, Python이나 다른 동적 언어를 위한 범용 ActiveResource 클라이언트를 쓰는 일은 어렵지 않을 것이다.
그때까지도 ActiveResource 호환 서비스를 위한 일회성 클라이언트를 쓰는 일은 다른 RESTful 서비스의 클라이언트를 쓰는 것보다 어렵지 않다.

RESTful 서비스든 REST-RPC 하이브리드 서비스든, XML·HTML·JSON 또는 그 혼합을 제공하든, 이제 어떤 서비스의 클라이언트라도 쓸 수 있어야 한다.
그것은 모두 HTTP 요청과 문서 파싱일 뿐이다.

또한 S3나 Yahoo! 검색 같은 RESTful 서비스가 Flickr나 del.icio.us API 같은 RPC 스타일·하이브리드 서비스와 무엇이 다른지도 감이 잡혀야 한다.
이것은 서비스 내용에 대한 판단이 아니라 아키텍처에 대한 판단이다.
목공에서 나뭇결을 따라 작업하는 것이 중요하듯, 웹에도 결이 있으며 RESTful 웹 서비스란 그 결을 따라 동작하는 서비스다.

## 핵심 정리

RESTful 서비스가 RPC 스타일 및 하이브리드 서비스와 구별되는 지점은 다음과 같다.

첫째, 리소스와 균일 인터페이스다.
서비스는 사용자 정의 함수 이름 대신, URI로 지정되는 리소스와 여섯 개의 표준 HTTP 메서드(GET, HEAD, POST, PUT, DELETE, OPTIONS)를 노출한다.
S3는 이 중 GET, HEAD, PUT, DELETE로 버킷 목록·버킷·객체라는 세 리소스의 모든 상호작용을 표현한다.
새 어휘를 발명할 필요 없이 복잡성은 전부 리소스 설계에 담긴다.

둘째, HTTP 응답 코드를 규칙으로 사용한다.
200, 403, 404, 400, 409처럼 상태 코드가 결과를 알리는 기계 판독 가능한 신호가 된다.
클라이언트는 본문을 이해하지 못해도 응답의 첫 3바이트로 성공·실패를 판별할 수 있다.

셋째, S3의 요청 서명은 공개 키 암호화를 사용한다.
공개 키(Access Key ID)로 신원을 밝히고, 개인 키(Secret Access Key)로 URI·HTTP 메서드·주요 헤더를 담은 정규 문자열에 SHA-1 HMAC 서명을 하며 base64로 인코딩한다.
서명된 URI는 개인 키를 노출하지 않고도 타인이 제한된 시간(기본 15분) 동안 나로서 요청하게 해주며, 접근 정책(`private`, `public-read`, `public-write`, `authenticated-read`)으로 익명 접근을 조정한다.

넷째, S3 표현의 약점은 링크의 부재다.
버킷 목록과 버킷 표현은 이름과 키만 담고 URI를 담지 않아, 클라이언트가 규칙으로 URI를 계산해야 한다.
이는 REST 설계 기준에서 S3의 주요 한계다.

다섯째, ActiveResource는 클라이언트를 투명하게 만든다.
RESTful 인터페이스가 균일하므로, Rails가 생성한 서비스에 대해 HTTP나 XML 코드를 직접 쓰지 않고도 ActiveRecord와 거의 동일한 객체 지향 인터페이스로 접근할 수 있다.
그 밑에서 벌어지는 일은 URI로 XML을 주고받는 HTTP 요청뿐이므로 어떤 언어로도 같은 클라이언트를 만들 수 있다.
