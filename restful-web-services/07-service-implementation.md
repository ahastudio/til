# 7장 서비스 구현: 소셜 북마킹

《RESTful Web Services》(Leonard Richardson, Sam Ruby, O'Reilly 2007) 7장 정리.

## 개요

앞선 장들이 원리에서 출발해 서비스를 설계하는 과정을 보여 줬다면, 이 장은 이미 존재하는 RPC 스타일 서비스를 리소스 지향 아키텍처(ROA)로 다시 만드는 실전 구현을 다룬다.
대상은 2장에서 소개한 del.icio.us라는 소셜 북마킹 사이트다.
저자는 del.icio.us 웹 서비스가 두 가지 한계를 가진다고 지적한다.
첫째, 그것은 완전한 REST가 아니라 REST-RPC 혼합이라 리소스를 우연히 노출할 뿐 HTTP의 통일 인터페이스를 존중하지 않는다.
둘째, 그 서비스는 자기 자신의 북마크와 태그에만 접근을 허용해서, 마치 이용자가 사이트에 혼자 있는 것처럼 보이게 만든다.

이 장의 목표는 세 가지다.
기존 RPC 스타일 서비스를 리소스 지향 서비스로 바꾸는 방법을 보이는 것, 선택한 프레임워크 안에서 동작하는 설계를 얻기 위해 감수해야 하는 절충을 보이는 것, 그리고 사소하지 않은 웹 서비스의 전체 코드를 지루한 세부 나열 없이 보이는 것이다.
프레임워크로는 Ruby on Rails를 택했다.
Ruby가 동적 언어이고 Rails가 헬퍼 클래스를 많이 제공하기 때문에 핵심 개념을 몇 줄로 드러내기 좋으며, 무엇보다 당시 최신 Rails가 REST와 리소스 지향 설계 원리를 명시적으로 중심에 둔 프레임워크였기 때문이다.

저자는 빈 Rails 1.2 애플리케이션에서 시작하고, 태그 구현을 위한 `acts_as_taggable` 플러그인, HTTP 기본 인증을 사용자 모델에 연결하는 `http_authentication` 플러그인, Atom 피드 생성을 위한 `atom-tools` gem을 설치한다.

```text
rails bookmarks
cd bookmarks
script/plugin install acts_as_taggable
script/plugin install http_authentication
gem install atom-tools
```

## 데이터셋 파악하기

기존 서비스를 기반으로 하므로 데이터셋의 윤곽은 비교적 쉽게 잡힌다.
del.icio.us에는 네 종류의 주요 데이터가 있다.
사용자 계정, 북마크(del.icio.us는 “post”라고 부른다), 태그(북마크의 메타데이터 역할을 하는 짧은 문자열), 그리고 번들(한 사용자가 묶어 둔 태그 모음)이다.

사용자 계정은 단순히 하위 리소스의 이름 붙은 목록이 아니라 자체 상태를 가진다.
사용자명과 비밀번호가 있고, 특정한 사람에 대응하며, 그 사람의 실명과 이메일 주소도 추적한다.
또한 하위 리소스로서 그 사용자의 북마크 목록을 가진다.

북마크는 사용자에 속하며 여섯 개의 상태를 가진다.
URI, 짧은 설명과 긴 설명, 타임스탬프, 태그 모음, 그리고 공개 여부를 나타내는 플래그다.
클라이언트가 이 정보를 모두 지정하되, URI와 짧은 설명만이 필수다.

여러 사람의 북마크를 모으면 URI에 창발적(emergent) 속성이 생긴다.
얼마나 최근에 북마크됐는지(newness), 얼마나 많은 사람이 북마크했는지(popularity), 사람들이 그 URI를 묘사할 때 쓰는 태그로 만들어진 태그 클라우드 등이다.
저자는 책 분량을 관리 가능한 수준으로 유지하기 위해 newness만 구현하고 popularity, 태그 클라우드, 추천 알고리즘은 구현하지 않는다.

태그는 이름이라는 상태 하나만 가지며 북마크(그리고 번들)와의 관계로만 존재한다.
번들은 완전성을 위해 RESTful 설계만 보여 주고 실제 코드는 작성하지 않는다.

데이터셋을 파악한 뒤 데이터베이스 스키마를 Rails 마이그레이션으로 정의한다.
`users`, `bookmarks`, `user_bookmarks`(사용자와 북마크의 종속 관계를 나타내는 조인 테이블), 그리고 `acts_as_taggable` 플러그인이 정의하는 `tags`, `taggings` 다섯 테이블과 네 개의 인덱스를 만든다.

```ruby
class InitialSchema < ActiveRecord::Migration
  def self.up
    create_table :bookmarks, :force => true do |t|
      t.column :user_id, :string
      t.column :uri, :string
      t.column :uri_hash, :string   # URI의 해시 값
      t.column :short_description, :string
      t.column :long_description, :text
      t.column :timestamp, :datetime
      t.column :public, :boolean
    end
    # users, user_bookmarks, tags, taggings 테이블과
    # 검색 경로에 맞춘 인덱스들도 함께 생성한다.
    add_index :bookmarks, :uri_hash
  end
end
```

```text
rake db:migrate
```

## 리소스 설계

이 장은 상상의 데이터셋을 자유롭게 리소스로 바꾸던 앞 장들과 달리, del.icio.us가 실제로 사용하는 방식으로 초점을 좁힌다.
del.icio.us 웹 서비스는 `posts/`, `tags/`, `bundles/`에 뿌리를 둔 세 개의 RPC 스타일 API를 노출하며, 그 아래에 HTTP GET으로 호출되는 열두 개의 RPC 함수를 둔다.
예컨대 `posts/get`, `posts/recent`, `posts/dates`, `posts/all`, `posts/update`, `posts/add`, `posts/delete`, `tags/get`, `tags/rename`, `tags/bundles/all`, `tags/bundles/set`, `tags/bundles/delete`가 그것이다.
여기에 더해 웹 사이트에만 있고 웹 서비스에는 없는 기능들 — `/{username}`, `/{username}/{tag}`, `/tag/{tag-name}`, `/url/{URI-MD5}`, `/recent` — 의 일부도 설계에 포함시킨다.

이 기능들을 리소스로 배치하는 일은 논리 퍼즐과 비슷하다.
가능한 한 적은 종류의 리소스를 노출하되, 하나의 리소스는 하나의 개념만 담을 수 있으므로 때로는 한 기능을 두 종류의 리소스로 쪼개고, 때로는 여러 RPC 함수를 통일 인터페이스의 여러 메서드에 응답하는 하나의 리소스로 합친다.

### Rails에서의 REST

리소스를 진공 속에서 설계하는 것이 아니라 Rails 위에서 구현하므로 Rails가 REST를 다루는 방식을 먼저 봐야 한다.
Rails는 리소스를 직접 정의하게 하지 않고 애플리케이션 기능을 컨트롤러로 나눈다.
요청 URI의 첫 경로 조각이 어느 컨트롤러 클래스로 라우팅할지를 결정한다.

과거 Rails에서는 컨트롤러에 `rename`, `delete` 같은 RPC 스타일 메서드를 정의했다.
Rails 1.2에서는 HTTP 통일 인터페이스의 메서드에 대응하는 특별한 컨트롤러 메서드를 정의한다.
`/weblogs`에 GET을 보내면 `index`가, POST를 보내면 `create`가 호출되어 하위 리소스가 생성된다.
개별 항목에 PUT을 보내면 `update`가, DELETE를 보내면 `destroy`가 호출된다.
`/weblogs/4/rename` 같은 RPC URI를 노출할 필요가 없는 것은, HTTP 통일 인터페이스가 이미 삭제 같은 동작을 알고 있기 때문이다.

이렇게 목록(테이블에 대응)과 목록 안의 항목(행에 대응)이라는 두 리소스 패턴이 늘 등장한다.
Rails는 노출하는 모든 리소스가 이 두 패턴 중 하나에 들어맞는다고 가정하는 단순화를 택한다.
대부분의 경우 이것이 일을 쉽게 만들지만, 이 단순한 모델에 맞지 않는 리소스를 노출하려 할 때는 성가심이라는 대가를 치른다.

루트 URI는 `http://localhost:3000/v1`이며, 앞으로 나올 상대 URI는 이 접두어를 전제로 한다.
버전 관리는 만일을 위해 URI에 반영한다.

### 사용자 컨트롤러

사용자 계정 정보를 노출하는 `UsersController`다.
Rails는 최소 저항 경로로 `/users`에 “사용자 목록” 리소스를, `/users/52` 같은 URI에 개별 사용자 리소스를 노출하도록 유도한다.

| 동작             | HTTP 요청        | Rails 메서드 |
| ---------------- | ---------------- | ------------ |
| 사용자 목록 조회 | GET /users       | `index`      |
| 사용자 생성      | POST /users      | `create`     |
| 사용자 조회      | GET /users/52    | `show`       |
| 사용자 수정      | PUT /users/52    | `update`     |
| 사용자 삭제      | DELETE /users/52 | `destroy`    |

여기서 두 가지를 조정한다.
첫째, del.icio.us에는 사용자 목록 조회 기능이 없으므로 목록 리소스에는 GET을 노출하지 않고 계정 생성용 POST만 노출한다.
둘째, `/users/52` 같은 URI는 보기 흉하다.
데이터베이스 ID 대신 사용자명을 써서 `/users/leonardr` 같은 읽기 쉬운 URI로 사용자 리소스를 노출한다.
이런 URI는 사용자가 이름을 바꾸면 가끔 바뀔 수 있지만, 영구적이되 아무 의미도 없는 URI보다 낫다는 판단이다.
결국 `UsersController`에 `create`, `show`, `update`, `destroy` 네 메서드를 구현하면 된다.

계정 생성에 관해서는, 실제 del.icio.us가 CAPTCHA로 자동 클라이언트를 막는 것이 정당한 선택임을 인정하면서도, 이 책에서는 웹 사이트와 CAPTCHA 설계를 다루지 않으려고 계정 생성을 웹 서비스의 일부로 노출한다고 밝힌다.

### 북마크 컨트롤러

사용자 계정에 종속되는 북마크는 별도 컨트롤러 `BookmarksController`가 `/users/{username}/bookmarks`를 기점으로 노출한다.
이 컨트롤러도 북마크 목록 리소스와 개별 북마크 리소스 두 종류를 노출한다.

개별 북마크 URI로 처음에는 대상 URI 자체를 경로에 담으려 했으나(W3C HTML 검사기처럼), Rails가 이를 잘 다루지 못했다.
그래서 대상 URI를 단방향 해시 함수(MD5)에 통과시킨 문자열을 경로에 넣기로 했다.
결과적으로 북마크 URI는 `/v1/users/leonardr/bookmarks/{URI-MD5}` 형태가 된다.
MD5 해시는 완전히 불투명한 데이터베이스 ID보다는 낫고, 단일 영숫자 문자열이라 Rails가 쉽게 처리한다.

```ruby
require 'digest/md5'
Digest::MD5.new("http://www.oreilly.com/").to_s
# => "55020a5384313579a5f11e75c1818b89"
```

북마크 생성은 자신의 “북마크 목록” 리소스에 POST를 보내는 방식으로 처리하며, 이것이 del.icio.us의 `posts/add`와 `posts/delete`를 대신한다.
PUT을 개별 URI에 보내 만드는 방식이나 사용자 리소스 자체에 POST하는 방식도 RESTful하지만 Rails의 관례에서 벗어나기 때문에 목록 리소스에 POST하는 관용적 방식을 택했다.
이는 프레임워크가 ROA의 원칙 위에 추가 제약을 얹는 사례다.

목록 리소스는 GET에 응답하며 개별 북마크는 GET, PUT, DELETE에 응답한다.
따라서 `index`, `create`, `show`, `update`, `destroy`를 구현하고, 목록 리소스는 `posts/get`, `posts/recent`, `posts/all`의 기능 일부를 흡수한다.

### 사용자 태그 컨트롤러

`TagsController`는 특정 사용자가 어떤 태그를 즐겨 쓰는지를 다루며 `/users/{username}/tags`에 뿌리를 둔다.
목록 리소스는 사용자의 북마크에서 생성되는 알고리즘적 리소스로 `tags/get`에 대응하며 읽기 전용이다.
`/users/{username}/tags/{tag}` 리소스는 그 사용자가 특정 태그로 분류한 북마크를 보여 준다.

태그 리소스는 읽기 전용은 아니어서 이름 변경(rename)을 위해 PUT을 노출한다.
del.icio.us API의 `tag/rename` 같은 일회성 메서드를 오버로드된 POST로 정의할 수도 있었지만, 그것은 RPC 스타일 사고다.
PUT은 이름 변경이든 다른 무엇이든 상태 변화를 전달하기에 충분하며, 컴퓨터에게 “상태를 바꿔라”라는 일반 개념을 이해시키는 편이 “태그를 rename하라”라는 특수 개념을 이해시키는 것보다 일이 적다.

### 캘린더 컨트롤러

`CalendarController`는 사용자의 게시 이력(달력)을 `/users/{username}/calendar`로 노출하며 del.icio.us의 `posts/dates`에 대응한다.
게시함으로써만 바뀌는 알고리즘적 읽기 전용 리소스다.
태그별 이력을 위한 하위 리소스 `/users/{username}/calendar/{tag}`도 두며 두 리소스 모두 GET만 노출한다.

### URI 컨트롤러

`UrisController`는 `/uris/`에 뿌리를 두고 URI를 사용자와 독립된 리소스로 노출해 창발적 속성에 접근하게 한다.
루트 URI는 리소스로 노출하지 않고 `/uris/{URI-MD5}`에 URI별 리소스를 둔다.
이 리소스는 어떤 사용자들이 그 URI를 북마크했는지 같은 정보를 담으며 del.icio.us 사이트의 `/url/{URI-MD5}`에 대응한다.

### 최근 북마크 컨트롤러

`RecentController`는 `/recent`에 뿌리를 두고 최근에 게시된 북마크(newness)를 노출한다.
`/recent/{tag}`는 특정 태그가 붙은 최근 북마크를 보여 주며 사이트의 `/tag/{tag-name}`에 대응한다.

### 번들 컨트롤러

구현하지는 않지만 설계를 보여 주는 컨트롤러다.
`/user/{username}/bundles/`에 뿌리를 두며(태그 이름 “bundles” 충돌을 피하려 `tags/bundles/`는 피했다), 번들 목록 GET과 생성 POST를 노출하고, `/user/{username}/bundles/{bundle}`은 GET, PUT, DELETE에 응답한다.

### 남은 것들: posts/update

거의 모든 기능을 배치했지만 `posts/update`만 남는다.
이 함수는 값비싼 `posts/all`을 다시 호출하기 전에 새 데이터가 있는지 확인하도록 돕는 용도다.
HTTP에는 이를 위한 조건부 GET이 이미 내장되어 있다.
조건부 GET을 구현하면 가장 비싼 리소스 하나뿐 아니라 노출하는 대부분의 리소스에 시간과 대역폭 절약이라는 이점을 줄 수 있다.

### REST 방식으로 재설계한 결과

우연히 부분적으로만 RESTful하던 RPC 스타일 서비스를, 완전히 RESTful한 리소스 집합으로 바꿨다.
RESTful 서비스의 핵심 이점은 HTTP 메서드로 동작 이름을 URI에서 제거한다는 데 있다.
이로써 URI가 객체 지향적 의미의 객체를 식별하고, HTTP 메서드를 바꿔 그 객체에 다른 동작을 수행한다.
임의로 이름 붙은 여러 함수를 이해하는 대신, 표준 인터페이스를 노출하는 하나의 클래스를 이해하면 된다.

이 서비스는 del.icio.us의 여러 제약, 특히 남의 공개 북마크를 볼 수 없다는 제약도 걷어낸다.
필요하다면 리소스 설계를 바꾸지 않고 인가(authorization) 구성만 바꿔 제한을 다시 넣을 수 있다.
리소스는 그대로 두고 언제 그 동작이 성공할지에 관한 규칙만 추가하는 것이다.

### routes.rb 파일

경로 조각을 컨트롤러 클래스에 매핑하는 것은 `routes.rb`의 몫이다.
`map.resources`가 `/v1/users`나 `/v1/users/{username}`으로 오는 요청을 `UsersController`로 라우팅하도록 설정한다.

```ruby
# config/routes.rb
ActionController::Routing::Routes.draw do |map|
  base = '/v1'
  map.resources :users, :path_prefix => base

  user_base = base + '/users/:username'
  map.resources :bookmarks, :path_prefix => user_base
  map.resources :tags,      :path_prefix => user_base
  map.resources :calendar,  :path_prefix => user_base

  map.resources :recent, :path_prefix => base
  map.resources :uris,   :path_prefix => base
end
```

이로써 `UsersController`, `BookmarksController`, `TagsController`, `CalendarController`, `RecentController`, `UrisController` 여섯 개의 컨트롤러 클래스를 정의할 의무가 생긴다.

## 클라이언트에서 받는 표현 설계

Rails는 두 가지 들어오는 표현 형식을 투명하게 지원한다.
폼 인코딩된 키-값 쌍과 ActiveRecord XML 직렬화 형식이다.
폼 인코딩은 `color1=blue&color2=green` 같은 익숙한 형식으로, Rails가 이를 해시로 파싱해 주므로 서비스 작성자는 표현을 직접 파싱할 필요가 없다.

ActiveRecord는 Rails의 객체-관계 라이브러리로, 테이블과 행에 네이티브 Ruby 인터페이스를 준다.
ActiveRecord 객체는 키-값 쌍 집합으로 표현될 수 있고, 이를 폼 인코딩하거나 `to_xml`로 XML 문서로 인코딩할 수 있다.

```xml
<user>
  <name>leonardr</name>
  <full-name>Leonard Richardson</full-name>
  <email>leonardr@example.com</email>
  <password>mypassword</password>
</user>
```

저자는 두 형식을 모두 지원하려고 폼 인코딩 키를 그냥 `name`이 아니라 `user[name]`으로 정의한다.
이렇게 하면 폼 인코딩 표현과 ActiveRecord XML 표현이 동일한 데이터 구조로 파싱된다.

```ruby
{ "user[name]"      => "leonardr",
  "user[full_name]" => "Leonard Richardson",
  "user[email]"     => "leonardr@example.com",
  "user[password]"  => "mypassword" }
```

사용자 표현의 키는 데이터베이스 필드명과 일치하는 `user[name]`, `user[password]`, `user[full_name]`, `user[email]`이다.
북마크 표현의 키는 `bookmark[short_description]`, `bookmark[long_description]`, `bookmark[timestamp]`, `bookmark[public]`, 그리고 `bookmark[tag][]`이다.
마지막의 `[]`는 한 요청에 여러 태그가 올 수 있음을 Rails에 알린다.
del.icio.us처럼 공백으로 구분한 단일 `tags` 변수로 태그 목록을 넘기는 방법도 있지만, 그것은 폼 인코딩 형식으로 이미 할 수 있는 일을 다시 구현하는 셈이라 선호하지 않는다.

## 클라이언트에 제공하는 표현 설계

나가는 표현 형식의 선택지는 아주 많지만 가장 쓰기 쉬운 것은 ActiveRecord 객체에 `to_xml`을 호출해 얻는 XML이다.
그러나 이 형식에는 큰 문제가 있다.
하이퍼미디어 형식이 아니라는 점이다.
`to_xml` 문서는 users 테이블의 한 행을 재구성하기에 충분한 정보를 담지만, 그 리소스와 다른 리소스(사용자의 북마크, 태그 어휘, 달력) 사이의 관계는 전혀 말해 주지 않는다.
`to_xml` 문서만 제공하는 서비스는 잘 연결되어 있지 않다.

문제 영역을 생각하면 또 다른 형식, Atom 신디케이션 형식이 떠오른다.
노출하려는 리소스 다수가 북마크 목록이고, 신디케이션 형식은 바로 링크 목록을 표현하도록 설계됐기 때문이다.
게다가 URI와 신디케이션 형식을 이해하는 소프트웨어가 이미 많으므로, 북마크 목록을 표준 신디케이션 형식으로 노출하면 즉시 넓은 사용자층을 얻는다.
무엇보다 신디케이션 피드는 링크를 담을 수 있어 리소스를 다른 리소스에 연결할 수 있고, 결과적으로 리소스들이 무관한 집합이 아니라 웹을 이룬다.

기본 표현은 언제나 `to_xml`이지만, 클라이언트는 URI 끝에 `.atom`을 붙여 어떤 북마크 목록이든 Atom 표현을 얻을 수 있다.
예를 들어 `/users/leonardr/bookmarks/ruby`는 링크 없는 `to_xml` 표현을, `/users/leonardr/bookmarks/ruby.atom`은 관련 리소스로의 링크가 담긴 Atom 표현을 준다.

## 리소스를 서로 연결하기

리소스 사이에는 많은 관계가 있다.
사용자와 그의 북마크, 북마크와 그것이 게시된 태그, URI와 그것을 북마크한 사용자들 사이의 관계 등이다.
그런데 `to_xml` 표현은 다른 리소스의 URI로 링크하지 않으므로 이런 관계를 표현에 드러낼 수 없고, Atom 피드는 링크를 담을 수 있어 관계를 담을 수 있다.

링크는 표현에 담겨야 실제로 존재한다.
사용자와 그 사용자의 북마크 사이의 개념적 링크는, 표현에 링크가 없다면 서비스에 실제로 존재하지 않는다.
클라이언트는 그저 어떻게 사용자의 북마크에 도달하는지를 “알고 있어야” 하는 상태가 된다.

또한 두 다이어그램 모두 클라이언트가 애초에 초점 리소스인 “사용자”에 어떻게 도달하는지에 대한 실마리를 주지 못한다.
저자는 그것을 영어 산문으로 설명했을 뿐이며, 이는 곧 실제 청중이 클라이언트가 아니라 클라이언트를 작성하는 사람들이라는 뜻이다.
이것은 연결성의 실패로, Amazon S3를 비롯한 일부 RESTful 서비스에서도 보이는 RPC 스타일의 마지막 잔재다.
5장에서는 최상위 리소스로 링크하는 서비스 홈페이지를 정의해 완전히 연결된 서비스를 만들어 이 문제를 해결한 바 있다.

## 정상 흐름: 무슨 일이 일어나야 하는가

Rails는 데이터베이스 기반 애플리케이션을 목록(테이블)과 목록 항목(행)이라는 두 리소스 패턴만으로 노출한다.
모든 목록 리소스는 거의 같은 방식으로 동작하고 모든 항목 리소스도 그렇다.
따라서 목록과 항목 리소스의 HTTP 인터페이스 구현을 위한 일종의 일반 제어 흐름을 세울 수 있다.

- 리소스가 생성되면 응답 코드는 201(“Created”), `Location` 헤더는 새 리소스의 위치를 가리킨다.
- 리소스가 수정되면 응답 코드는 200(“OK”)이다. 상태 변화가 URI를 바꾸면(예: 사용자 이름 변경) 301(“Moved Permanently”)과 함께 새 URI를 `Location`에 담는다.
- 객체가 삭제되면 응답 코드는 200(“OK”)이다.
- 가능한 한 GET을 지원하는 모든 리소스는 조건부 GET도 지원해야 하며, 이는 `ETag`와 `Last-Modified`에 적절한 값을 설정함을 뜻한다.

마지막으로 데이터 보안 규칙이 있다.
del.icio.us API와 달리 정보를 얻는 데 인증을 요구하지는 않지만, 어떤 사용자의 비공개 북마크는 그 사용자로 인증한 경우가 아니면 아무도 볼 수 없어야 한다.
남의 북마크를 보면 비공개 북마크가 걸러진 표현을 받으며, 이 원칙은 달력과 태그 어휘에도 확장된다.
내 눈에 보이는 북마크에 쓰이지 않은 수수께끼의 태그가 내 태그 어휘 표현에 나타나서는 안 된다.

## 오류 흐름: 무엇이 잘못될 수 있는가

주된 문제는 인가되지 않은 접근이다.
적절한 `Authorization` 헤더 없이 사용자 계정 편집이나 태그 이름 변경 같은 동작을 시도하면 401(“Unauthorized”)을 쓴다.

이미 존재하는 계정을 생성하려는 시도는, 서비스 관점에서는 인가 없이 기존 계정을 수정하려는 시도로 보인다.
이때 401도 맞지만 클라이언트를 혼란스럽게 할 수 있으므로, 인가가 제공됐지만 틀린 경우에는 401을, 인가가 전혀 없는 경우에는 409(“Conflict”)를 보낸다.
사용자 이름을 이미 존재하는 이름으로 바꾸려는 경우에도 409가 적절하다.

북마크 목록 리소스는 쿼리 변수 `limit`과 `date`를 지원한다.
말이 안 되는 `limit`이나 `date`가 오면 400(“Bad Request”)을, 유효하지 않은 표현으로 리소스를 생성·수정하려 할 때도 400을 쓴다.

존재하지 않는 사용자 정보를 조회하려 하면 del.icio.us처럼 404(“Not Found”)를 보낸다.
이것은 클라이언트가 원한다면 계정을 만들라는 신호다.

한 사용자는 URI마다 북마크를 하나만 가질 수 있다.
이미 북마크한 URI로 북마크의 URI를 바꾸려 하거나 이미 북마크한 URI를 POST하려 하면 409가 적절하다.
기존 북마크를 수정하는 통일된 방법은 북마크 리소스에 PUT하는 것이다.

계정 생성 시 ActiveRecord XML이나 폼 인코딩이 아니라 JSON 표현을 보내는 등 완전히 잘못된 미디어 타입을 보내면 415(“Unsupported Media Type”)가 맞으며, 이 조건은 Rails가 자동으로 처리한다.

## 컨트롤러 코드

핵심은 들어오는 HTTP 요청을 데이터베이스에 대한 구체적 동작으로 변환하는 코드다.
공통 코드와 까다로운 코드 대부분을 담는 기반 클래스 `ApplicationController`를 정의한 뒤 여섯 컨트롤러를 정의한다.
각 컨트롤러는 HTTP 통일 인터페이스에 대응하는 표준 액션(`index`, `show`, `create`, `update`, `destroy`)을 구현하되, 많은 경우 비표준 이름의 다른 액션에 위임한다.

### Rails가 해 주지 않는 것

두 가지 기능은 직접 구현해야 하며 이들이 까다로운 코드의 대부분을 차지한다.

첫째는 조건부 GET이다.
가능하면 `Last-Modified`와 `ETag` 응답 헤더를 표현과 함께 보내야 하며, 그러면 클라이언트가 이후 요청을 표현 변경 여부에 조건을 걸어 시간과 대역폭을 아낄 수 있다.
서드파티 컨트롤러가 있지만 추가 복잡성을 들이지 않으려고 `Last-Modified`에 대한 재사용 가능한 해법을 직접 구현한다.

둘째는 `params[:id]`가 실제로는 ID가 아닌 경우다.
Rails는 항목 리소스 URI가 데이터베이스 ID로 행을 식별한다고 가정하지만, 이 서비스는 `/v1/users/leonardr`처럼 읽기 쉬운 URI를 쓴다.
클라이언트는 여전히 이 URI를 요청할 수 있고 컨트롤러도 처리할 수 있으며, 다만 사용자명이 `params[:username]`이 아니라 `params[:id]`로 들어온다.
URI에 경로 변수가 여러 개면 마지막 변수는 항상 `params[:id]`에 들어가므로, 아래 코드에서 `params[:id]`는 결코 데이터베이스 ID가 아님을 유념해야 한다.

### ApplicationController

여섯 컨트롤러의 추상 상위 클래스다.
가장 흔한 동작인 “조건에 맞는 북마크 목록 가져오기”를 위한 `show_bookmarks` 액션으로 시작한다.
이 메서드는 `limit`·`date` 쿼리 변수를 검증하고, 인증된 사용자에게 보이는 북마크로 제한한 뒤, 조건에 맞는 북마크를 찾아 렌더링한다.
검증 실패 시 400을 보낸다.

```ruby
def show_bookmarks(conditions, title, feed_uri, user=nil, tag=nil)
  errors = []
  if params[:limit] && params[:limit].to_i < 0
    errors << "limit must be >= 0"
  end
  params[:limit] ||= @@default_limit

  if errors.empty?
    conditions ||= [""]
    # 날짜 필터가 있으면 timestamp 범위 조건을 덧붙인다.
    Bookmark.only_visible_to!(conditions, @authenticated_user)
    bookmarks = Bookmark.custom_find(conditions, tag, params[:limit])
    render_bookmarks(bookmarks, title, feed_uri, user)
  else
    render :text => errors.join("\n"), :status => "400 Bad Request"
  end
end
```

전통적 Rails 액션과의 주된 차이는 뷰다.
대부분의 Rails 액션은 ERb 템플릿으로 뷰를 정의하지만, 여기서는 코드 기반 생성기로 XML과 Atom 문서를 만드는 `render_bookmarks` 함수에 뷰를 위임한다.
이 함수는 조건부 HTTP GET도 지원해서, 가장 최근 북마크의 타임스탬프를 `Last-Modified` 값으로 삼는다.

```ruby
def render_bookmarks(bookmarks, title, feed_uri, user, except=[])
  last_modified = bookmarks.empty? ? nil :
    bookmarks.max { |b1, b2| b1.timestamp <=> b2.timestamp }.timestamp

  render_not_modified_or(last_modified) do
    respond_to do |format|
      format.xml  { render :xml =>
        bookmarks.to_xml(:except => except + [:id, :user_id],
                         :include => [:tags]) }
      format.atom { render :xml =>
        atom_feed_for(bookmarks, title, feed_uri, user) }
    end
  end
end
```

조건부 요청 처리의 나머지는 `render_not_modified_or`에 있다.
목록이 마지막 요청 이후 바뀌었으면 `yield`로 정상 렌더링을 계속하고, 바뀌지 않았으면 액션을 가로채 304(“Not Modified”)를 보낸다.

```ruby
def render_not_modified_or(last_modified)
  response.headers['Last-Modified'] = last_modified.httpdate if last_modified
  if_modified_since = request.env['HTTP_IF_MODIFIED_SINCE']
  if if_modified_since && last_modified &&
     last_modified <= Time.httpdate(if_modified_since)
    render :nothing => true, :status => "304 Not Modified"
  else
    yield
  end
end
```

`if_found` 헬퍼는 클라이언트가 데이터베이스의 실제 객체에 대응하는 URI를 지정했는지 확인한다.
객체가 있으면 `yield`로 제어를 돌려주고, 없으면 404로 요청을 단락시킨다.

```ruby
def if_found(obj)
  if obj
    yield
  else
    render :text => "Not found.", :status => "404 Not Found"
    false
  end
end
```

또한 여러 필터를 구현한다.
모든 액션은 인증이 필요 없더라도 인증된 사용자에게 자신의 비공개 북마크를 보여 주기 위해 `authenticate`를 거친다.
`must_authenticate`는 인증이 필요한 액션을 보호하며, 자신이 아닌 다른 사용자에 대해 조작하려는 경우에도 401을 보낸다.
`must_specify_user`는 `/users/{username}` 아래 컨트롤러용으로, 사용자명을 사용자 ID로 바꾸고 없으면 404를 보낸다.

```ruby
before_filter :authenticate

def authenticate
  @authenticated_user = nil
  authenticate_with_http_basic do |user, pass|
    @authenticated_user = User.authenticated_user(user, pass)
  end
  return true
end

def must_authenticate
  if @authenticated_user && (@user_is_viewing_themselves != false)
    return true
  else
    request_http_basic_authentication("Social bookmarking service")
    return false
  end
end
```

마지막으로 주된 뷰 메서드 `atom_feed_for`를 구현한다.
ActiveRecord `Bookmark` 객체 배열을 Atom 문서로 바꾸며, 링크가 풍부한 결과를 낳는다.
각 항목은 외부 URI, 이 서비스 안의 해당 북마크 리소스(`rel=“self”`), 같은 URI를 북마크한 다른 사용자 목록(`rel=“related”`), 그리고 각 태그별 관련 북마크로 링크한다.
바로 이 링크들이 서비스에 연결성을 부여한다.

```ruby
def atom_feed_for(bookmarks, title, feed_uri, user=nil)
  feed = Atom::Feed.new
  feed.title = title
  # 피드 자신으로의 self 링크, 필요하면 작성자(author) 설정
  bookmarks.each do |bookmark|
    entry = feed.entries.new
    entry.title   = bookmark.short_description
    entry.content = bookmark.long_description
    entry.updated = bookmark.timestamp
    # 외부 URI, 이 북마크 리소스(self),
    # 같은 URI를 북마크한 사용자 목록(related)으로 링크
    # 각 태그를 Atom 카테고리로 표현하고 관련 목록으로 링크
  end
  return feed.to_xml
end
```

### UsersController

계정 생성(POST)에는 인증이 필요 없지만 수정(PUT)과 삭제(DELETE)에는 인증이 필요하므로 `before_filter :must_authenticate, :only => [...]`로 설정한다.
`create`는 이 서비스 전반의 POST 패턴을 따른다.
이미 존재하는 사용자면 409, 데이터가 부실해 ActiveRecord 검증이 실패하면 400, 성공하면 201과 함께 `Location`에 새 URI를 담는다.

```ruby
# POST /users
def create
  user = User.find_by_name(params[:user][:name])
  if user
    headers['Location'] = user_url(user.name)
    render :nothing => true, :status => "409 Conflict"
  else
    user = User.new(params[:user])
    if user.save
      headers['Location'] = user_path(user.name)
      render :nothing => true, :status => "201 Created"
    else
      render :xml => user.errors.to_xml, :status => "400 Bad Request"
    end
  end
end
```

`update`는 PUT의 패턴을 따른다.
새 이름이 이미 쓰이고 있으면 409, 검증 실패면 400, 성공이면 200이다.
다만 이름이 실제로 바뀌어 URI가 달라지면 301과 함께 새 URI를 `Location`에 담는다.

```ruby
# PUT /users/{username}
def update
  old_name = params[:id]
  new_name = params[:user][:name]
  user = User.find_by_name(old_name)
  if_found user do
    if old_name != new_name && User.find_by_name(new_name)
      render :nothing => true, :status => "409 Conflict"
    else
      user.update_attributes(params[:user])
      if user.save
        if user.name != old_name
          headers['Location'] = user_path(user.name)
          status = "301 Moved Permanently"
        else
          status = "200 OK"
        end
        render :nothing => true, :status => status
      else
        render :xml => user.errors.to_xml, :status => "400 Bad Request"
      end
    end
  end
end
```

`show`와 `destroy`는 더 단순하다.
`show`는 사용자를 찾아 `to_xml`로 직렬화하되 ID와 비밀번호는 제외하고, `destroy`는 사용자를 삭제한 뒤 200을 보낸다.
둘 다 `if_found`가 없는 사용자에 대해 404를 처리한다.
사용자 리소스에는 대역폭 절약 이득이 크지 않다고 보아 조건부 GET을 구현하지 않았다.

### BookmarksController

`must_specify_user`(없는 사용자의 북마크 접근을 404로 막음), `must_authenticate`(쓰기 액션 보호), 그리고 들어오는 표현을 정리하는 일회성 필터 `fix_params`를 둔다.

```ruby
class BookmarksController < ApplicationController
  before_filter :must_specify_user
  before_filter :fix_params
  before_filter :must_authenticate, :only => [:create, :update, :destroy]

  def fix_params
    if params[:bookmark]
      params[:bookmark][:user_id] = @user.id if @user
    end
  end
```

목록 리소스가 GET에 응답하므로 `index`가 있으며, `index`와 `show`는 `show_bookmarks`에 위임한다.
`create`는 사용자가 이미 그 URI를 북마크했으면 409, 아니면 `timestamp`와 `public` 기본값을 채우고 저장한 뒤 태그를 붙이고 201을 보낸다.

```ruby
# POST /users/{username}/bookmarks
def create
  bookmark = Bookmark.find_by_user_id_and_uri(params[:bookmark][:user_id],
                                              params[:bookmark][:uri])
  if bookmark
    headers['Location'] = bookmark_url(@user.name, bookmark.uri)
    render :nothing => true, :status => "409 Conflict"
  else
    params[:bookmark][:timestamp] ||= Time.now
    params[:bookmark][:public]    ||= "1"
    bookmark = Bookmark.new(params[:bookmark])
    if bookmark.save
      bookmark.tag_with(params[:taglist]) if params[:taglist]
      headers['Location'] = bookmark_url(@user.name, bookmark.uri)
      render :nothing => true, :status => "201 Created"
    else
      render :xml => bookmark.errors.to_xml, :status => "400 Bad Request"
    end
  end
end
```

`update`도 사용자·URI 규칙에 따라 이미 북마크한 URI로 바꾸려 하면 409, URI가 바뀌면 301, 그대로면 200, 검증 실패면 400을 보낸다.
`show`는 북마크 하나를 원소 하나짜리 목록으로 렌더링하고, `destroy`는 삭제 후 200을 보낸다.

### TagsController

사용자의 태그 어휘와 태그별 북마크를 노출한다.
어휘는 각 태그와 사용 횟수 목록인데, 보안을 위해 자신의 어휘를 볼 때만 전체 집계를 보이고 남의 어휘는 공개 북마크만 센다.
`to_xml`이 이 데이터에 잘 맞지 않아 커스텀 SQL로 공개 태그만 조건부로 센다.

```ruby
# GET /users/{username}/tags
def index
  if @user_is_viewing_themselves
    tag_restriction = ''
  else
    tag_restriction = " AND bookmarks.public='1'"
  end
  sql = ["SELECT tags.*, COUNT(bookmarks.id) as count" +
         " FROM tags, bookmarks, taggings" +
         " WHERE taggings.taggable_type = 'Bookmark'" +
         " AND tags.id = taggings.tag_id" +
         " AND taggings.taggable_id = bookmarks.id" +
         " AND bookmarks.user_id = ?" + tag_restriction +
         " GROUP BY tags.name", @user.id]
  tags = Tag.find_by_sql(sql)
  render :xml => tags.to_xml(:except => [:id])
end
```

태그 이름 변경은 PUT으로 처리한다.
그런데 이 리소스는 특정 ActiveRecord 객체 하나에 대응하지 않는다.
`Tag` 객체는 모든 사람의 태그 사용을 나타내므로, `Tag` 객체 자체를 rename하면 사이트 전체에 영향을 준다.
따라서 클라이언트의 북마크 중 해당 태그가 붙은 것을 모두 찾아 옛 이름을 떼고 새 이름을 붙인다.
사용자·북마크와 달리 이미 존재하는 태그로 rename해도 409를 보내지 않고 그냥 병합한다.
URI가 바뀌므로 301과 새 위치를 보낸다.

```ruby
# PUT /users/{username}/tags/{tag}
def update
  old_name = params[:id]
  new_name = params[:tag][:name] if params[:tag]
  if new_name
    to_change = Bookmark.find(["bookmarks.user_id = ?", @user.id], old_name)
    to_change.each do |bookmark|
      tags = bookmark.tags.collect { |tag| tag.name }
      tags.delete(old_name)
      tags << new_name
      bookmark.tag_with tags.uniq
    end
    headers['Location'] = tag_url(@user.name, new_name)
    status = "301 Moved Permanently"
  end
  render :nothing => true, :status => status || "200 OK"
end
```

`show`는 그 사용자의 북마크 중 해당 태그가 붙은 것을 `show_bookmarks`에 태그 인자를 넘겨 보여 준다.

### 나머지 컨트롤러들

나머지 컨트롤러는 모두 읽기 전용이라 기껏해야 `index`와 `show`만 구현한다.

`CalendarController`는 게시 이력을 요약으로 렌더링한다.
`to_xml`이 이 데이터 구조에 잘 맞지 않아 `Builder::XmlMarkup`으로 직접 XML을 만드는 `calendar_to_xml` 뷰 함수를 쓴다.
본체 로직은 `Bookmark.calendar` 모델 메서드에 있고 컨트롤러는 렌더링만 한다.

```ruby
def calendar_to_xml(days, tag=nil)
  xml = Builder::XmlMarkup.new(:indent => 2)
  xml.instruct!
  xml.calendar(:tag => tag) do
    days.each do |day|
      xml.day(:date => day.date, :count => day.count)
    end
  end
end
```

`RecentController`는 최근 북마크를 보여 주는 얇은 래퍼로, 두 액션 모두 `show_bookmarks`에 위임한다.

```ruby
class RecentController < ApplicationController
  # GET /recent
  def index
    show_bookmarks(nil, "Recent bookmarks", recent_url)
  end
  # GET /recent/{tag}
  def show
    tag = params[:id]
    show_bookmarks(nil, "Recent bookmarks tagged with '#{tag}'",
                   recent_url(tag), nil, tag)
  end
end
```

`UrisController`는 한 URI에 대한 사이트 사용자들의 반응을 보여 준다.
같은 URI를 여러 사람이 서로 다른 태그·설명으로 북마크한 목록을 커스텀 SQL로 조회하되, `only_visible_to!`로 보이는 것만 거른다.

```ruby
# GET /uris/{URI-MD5}
def show
  uri_hash = params[:id]
  sql = ["SELECT bookmarks.*, users.name as user from bookmarks, users" +
         " WHERE users.id = bookmarks.user_id AND bookmarks.uri_hash = ?",
         uri_hash]
  Bookmark.only_visible_to!(sql, @authenticated_user)
  bookmarks = Bookmark.find_by_sql(sql)
  if_found(bookmarks) do
    uri = bookmarks[0].uri
    render_bookmarks(bookmarks, "Users who've bookmarked #{uri}",
                     uri_url(uri_hash), nil)
  end
end
```

## 모델 코드

세 개의 주요 테이블에 대응하는 `User`, `Bookmark`, `Tag` 모델이 있다.
`Tag`는 `acts_as_taggable` 플러그인이 전부 정의하므로 `User`와 `Bookmark`만 정의하면 된다.
모델 클래스는 데이터베이스 필드에 대한 검증 규칙을 정의하며, 나쁜 데이터가 오면 규칙이 발동해 컨트롤러가 400을 보낸다.
같은 모델은 일반 웹 애플리케이션이나 GUI 애플리케이션에서도 그대로 쓸 수 있고, 표시만 다를 뿐 규칙은 항상 같다.

### User 모델

검증 규칙, `Bookmark`와의 일대다 관계, 비밀번호 검증 메서드를 가진다.
비밀번호는 평문으로 저장되지 않도록 가능한 한 빨리 단방향 해시(SHA1)를 거친다.

```ruby
class User < ActiveRecord::Base
  has_many :bookmarks, :dependent => :destroy
  validates_uniqueness_of :name
  validates_presence_of :name, :full_name, :email

  def password=(password)
    super(User.hashed(password))
  end

  def self.authenticated_user(username, pass)
    user = find_by_name(username)
    user = nil if user && hashed(pass) != user.password
    return user
  end

  def self.hashed(password)
    Digest::SHA1.new(password).to_s
  end
end
```

### Bookmark 모델

관계와 검증 규칙, 그리고 URI의 MD5 해시를 생성하는 규칙을 정의한다.
MD5 계산은 단방향이라 역산할 수 없으므로 해시로 URI를 찾을 수 있도록 해시 값을 저장해 둔다.
`uri_hash`는 직접 바꾸지 못하게 보호하고, URI가 바뀔 때만 갱신한다.

```ruby
class Bookmark < ActiveRecord::Base
  belongs_to :user
  acts_as_taggable
  validates_presence_of :user_id, :uri, :short_description, :timestamp
  attr_protected :uri_hash

  def uri=(new_uri)
    super
    self.uri_hash = Digest::MD5.new(new_uri).to_s
  end

  def tag_with(tags)
    Tag.transaction do
      taggings.destroy_all
      tags.each { |name| Tag.find_or_create_by_name(name).on(self) }
    end
  end
end
```

서비스의 일꾼은 `custom_find`다.
`acts_as_taggable`의 `find_tagged_with`로는 “leonardr의 북마크 중 'ruby' 태그가 붙은 것” 같은 복합 질의를 못 하므로, 태그 제약을 기존 제약에 덧붙이는 메서드를 직접 정의한다.
태그 제약이 있으면 조인으로 SQL을 짜고, 없으면 상위 클래스의 `find`로 쉽게 찾는다.

```ruby
def self.custom_find(conditions, tag=nil, limit=nil)
  if tag
    sql = ["SELECT bookmarks.* FROM bookmarks, tags, taggings" +
           " WHERE taggings.taggable_type = 'Bookmark'" +
           " AND bookmarks.id = taggings.taggable_id" +
           " AND taggings.tag_id = tags.id AND tags.name = ?", tag]
    if conditions
      sql[0] << " AND " << conditions[0]
      sql += conditions[1..conditions.size]
    end
    sql[0] << " ORDER BY bookmarks.timestamp DESC"
    sql[0] << " LIMIT " << limit.to_i.to_s if limit
    bookmarks = find_by_sql(sql)
  else
    bookmarks = find(:all, {:conditions => conditions, :limit => limit,
                            :order => 'timestamp DESC'})
  end
  return bookmarks
end
```

`only_visible_to!`는 조건 집합을 조작해 특정 사용자가 볼 수 있는 북마크(공개 북마크와 그 사용자의 비공개 북마크)만 찾도록 만든다.
조건 배열의 첫 원소는 변수 치환이 있는 SQL WHERE 절이고 이후 원소는 치환될 값이라는 ActiveRecord 규약을 이용한다.

```ruby
def self.only_visible_to!(conditions, user)
  conditions[0] << " AND " unless conditions[0].empty?
  conditions[0] << "(public='1'"
  if user
    conditions[0] << " OR user_id=?"
    conditions << user.id
  end
  conditions[0] << ")"
end
```

`calendar`는 SQL `DATE()` 함수로 게시 날짜별 북마크 수를 묶는다.
이 함수는 모든 데이터베이스에서 지원되지는 않는다.
소유자가 아닌 사람이 볼 때는 공개 북마크만 센다.

이제 `script/server`로 Rails 서버를 띄우면 웹 서비스를 쓸 수 있다.

## 클라이언트가 알아야 할 것

이 서비스는 `script/generate scaffold_resource`로 만든 것과 달리 웹 사이트로는 쓸 수 없다.
HTML 폼이나 HTML 뷰를 만들지 않았기 때문인데, 이는 주로 지면 사정 때문이다.
`respond_to`에 `format.html`을 추가하면 ERb 템플릿을 HTML로 렌더링할 자리가 된다.

일단 사이트에 북마크가 쌓이면 서로 링크된 Atom 표현으로 많은 리소스가 노출되고, 오늘날의 웹 브라우저를 포함한 어떤 프로그램이든 HTTP GET을 말하고 신디케이션 파일을 다룰 줄만 알면 이 리소스를 입력으로 삼을 수 있다.
문제는 그 리소스를 애초에 사이트에 올리는 방법이며, 클라이언트를 쓰기 쉽게 만드는 데는 세 가지 가능성이 있다.

### 자연어 서비스 기술

가장 단순한 방법은 서비스 구조를 영어 산문으로 기술하는 것이다.
오늘날 대부분의 RESTful·혼합 서비스가 이렇게 동작한다.
상태 전이의 지렛대(levers of state)를 하이퍼미디어가 아니라 일반 매체 — 사람이 미리 해석해야 하는 영어 텍스트 — 로 지정하는 것이다.
어차피 광고를 위해서라도 자연어 기술은 필요하다.
저자는 이 장의 산문 기술에 기반해, 계정 생성과 북마크 게시를 할 줄 아는 명령줄 Ruby 클라이언트(`rest-open-uri` 사용)를 제시한다.
이 클라이언트는 응답 코드를 보고 409는 “이미 있는 사용자”, 401은 “잘못된 비밀번호” 등으로 해석한다.

```ruby
def new_user(username, password, full_name, email)
  representation = form_encoded({ "user[name]" => username,
                                  "user[password]" => password,
                                  "user[full_name]" => full_name,
                                  "user[email]" => email })
  begin
    response = open(@service_root + '/users', :method => :post,
                    :body => representation)
    puts "User #{username} created at #{response.meta['location']}"
  rescue OpenURI::HTTPError => e
    if e.io.status[0].to_i == 409   # Conflict
      puts "Sorry, there's already a user called #{username}."
    else
      raise e
    end
  end
end
```

### 표준화를 통한 기술

또 다른 방법은 서비스를 다른 서비스와 닮게 만드는 것이다.
모든 서비스가 같은 표현 형식을 쓰고 URI를 리소스에 같은 방식으로 매핑한다면, 클라이언트 프로그래밍을 없애지는 못해도 클라이언트가 HTTP보다 높은 수준에서 동작할 수 있다.
관례는 강력한 도구이며, 사실 REST가 쓰는 것과 같은 도구다.
여기서는 REST보다 높은 수준의 관례를 적용해 클라이언트 코드를 줄이자는 것이다.

Rails가 그 예다.
거의 모든 Rails 서비스는 URI를 컨트롤러에, 컨트롤러를 리소스에, 리소스를 ActiveRecord 객체에, 그 객체를 데이터베이스 행에 매핑하고, 표현 형식도 XML이나 폼 인코딩 키-값으로 표준화되어 있다.
개발 중이던 ActiveResource 라이브러리는 이런 유사성을 이용해 HTTP 접근의 세부를 ActiveRecord처럼 보이는 인터페이스 뒤에 숨기는 클라이언트 라이브러리다.
다만 이 접근은 모든 서비스, 심지어 모든 Rails 서비스에 통하지는 않으며 이 서비스에는 잘 맞지 않는다.

### 하이퍼미디어 기술

ActiveResource가 개선돼도 그것은 결국 몇 가지 고수준 설계 관례의 구현일 뿐이며, 관례를 따르지 않는 서비스와는 대화하지 못한다.
필요한 것은 각 서비스가 자신의 리소스 설계, 표현 형식, 리소스 사이의 링크를 클라이언트에 알려 주는 일반적 틀이다.
그러면 모든 서비스에 최소한의 요구사항만 강제하면서도 표준 관례의 이점 일부를 얻을 수 있다.

이는 REST의 연결성 개념, 곧 “애플리케이션 상태의 엔진으로서의 하이퍼미디어”로 우리를 되돌린다.
하이퍼미디어 링크와 폼은 서비스 간의 차이를 기술하는 기계 판독 가능한 관례이기 때문이다.
서비스가 현재 리소스 상태를 보여 주는 직렬화된 데이터 구조만 제공한다면 추가 표준과 관례를 고민하게 되는데, 이는 표현이 절반의 일만 하고 있기 때문이다.
사람의 웹은 직렬화된 데이터가 아니라 링크와 폼이 가득한 문서를 제공하므로 그런 추가 표준이 필요 없다.
이 장에서 Atom 문서에 심은 링크는 이 서비스를 다른 Atom 서비스와 구별해 주는 기계 판독 가능한 기술이며, 9장에서는 XHTML 4, XHTML 5, WADL이라는 세 하이퍼미디어 형식을 다룬다.

## 핵심 정리

- 이 장은 REST-RPC 혼합인 del.icio.us를 리소스 지향 아키텍처로 다시 설계·구현하는 실전 사례다.
- 핵심 전략은 RPC 함수 이름을 URI에서 없애고 HTTP 통일 인터페이스(GET/POST/PUT/DELETE)로 옮겨, URI가 객체를 식별하고 메서드가 동작을 정하도록 만드는 것이다.
- Rails는 리소스를 목록과 항목이라는 두 패턴으로만 노출하도록 단순화하며, 이 가정에 맞지 않는 리소스(예: 사용자의 태그 어휘, 태그 rename)에서는 프레임워크와 절충해야 한다.
- URI는 데이터베이스 ID(`/users/52`) 대신 의미 있는 상태(`/users/leonardr`)나 대상 URI의 MD5 해시로 만들어 읽기 쉽게 했으나, 그 때문에 `params[:id]`가 실제 ID가 아님을 감수한다.
- 정상 흐름(201/200/301)과 오류 흐름(400/401/404/409/415)을 표준 제어 흐름으로 정리해 모든 컨트롤러에 일관되게 적용한다.
- `to_xml` 표현은 링크가 없어 연결성이 부족하므로, 북마크 목록은 링크가 풍부한 Atom 표현(`.atom` 접미어)으로도 제공해 리소스를 서로 잇는다.
- 보안은 리소스 설계가 아니라 인가 규칙으로 처리한다. 비공개 북마크는 소유자에게만 보이며, 이 원칙은 태그 어휘와 달력 집계에까지 확장된다.
- 조건부 GET(`Last-Modified`/304)을 직접 구현해 값비싼 `posts/update`의 이점을 여러 리소스에 일반화한다.
- 궁극적 지향점은 연결성, 곧 “애플리케이션 상태의 엔진으로서의 하이퍼미디어”이며, 자연어 기술과 표준화된 관례(ActiveResource)를 넘어 서비스가 스스로를 기술하는 하이퍼미디어가 이상적 해법이다.
