# Hanami: 커져도 유지보수되는 Ruby 앱을 위한 프레임워크

<https://hanakai.org/hanami>

<https://github.com/hanakai-rb>

## 소개

Hanami는 코드를 정돈되고 유지보수 가능한 상태로 유지하도록 설계된 Ruby 프레임워크라고 소개된다.
페이지의 표어는 당신과 함께 자라는 Ruby 앱이며, 관심사의 분리와 명시적인 비즈니스 로직과 모듈형 아키텍처가 앱이 커져도 계속 즐겁게 작업할 수 있는 기반을 준다는 것이다.

이 페이지는 Hanakai라는 우산 아래 있다.
상단에 Hanami와 Dry와 Rom이 Hanakai로 합친다는 안내가 있고 발표문 링크가 붙어 있다.
Hanakai의 세 프로젝트는 앱을 만드는 완전한 프레임워크인 Hanami, 검증과 타입과 함수형 패턴 등을 제공하는 Dry, 강력하고 유연한 영속성 툴킷인 Rom으로 소개된다.
합류 발표는 2026년 5월 1일이고 Hanami 3.0은 2026년 6월 30일에 발표됐다.
RubyGems 기준 `hanami` 젬의 최신 버전은 2026년 7월 3일 출시된 3.0.1이다.

## 주요 구성

페이지는 계층별로 코드 예시를 붙여 설명한다.

### 전용 데이터 계층

Hanami가 전용 데이터베이스 계층을 제공하므로 모든 질의를 한곳에 두게 된다고 설명한다.
단순한 질의는 쉽게 유지하면서 같은 도구들로 복잡한 질의를 조립할 수 있다는 것이다.
릴레이션이 데이터 접근 패턴을 정의하고, 레포가 비즈니스 로직을 위해 그것을 조합하며, 스트럭트가 앱 전체에서 쓸 값 객체를 제공한다고 정리한다.
그래서 앱이 커져도 데이터베이스 계층이 집중된 상태로 유지된다는 것이다.

```ruby
# app/relations/articles.rb
class Articles < Hanami::DB::Relation
  schema :articles, infer: true

  def published
    where(published: true).order { created_at.desc }
  end
end
```

```ruby
# app/repos/article_repo.rb
class ArticleRepo < MyApp::Repo
  def update(id, attributes)
    articles.by_pk(id).changeset(:update, attributes).commit
  end

  def find(id)
    articles.published.by_pk(id).one!
  end

  def latest
    articles.published.limit(10).to_a
  end
end
```

```ruby
# app/structs/article.rb
class Article < MyApp::DB::Struct
  def summary
    "#{title} (#{author_name}, #{published_at.year})"
  end
end
```

### 오퍼레이션

오퍼레이션이 성공 경로와 실패 경로를 명시하면서 워크플로를 조합하게 해 준다고 설명한다.
각 오퍼레이션은 하나의 일에 집중하고 필요한 의존성을 끌어오며 비즈니스 로직을 분명하고 테스트 가능하게 만든다는 것이다.

```ruby
# app/articles/update.rb
class Update < MyApp::Operation
  include Deps["repos.article_repo"]

  def call(article_id, attributes)
    validation = step validate(attributes)
    article = article_repo.update(article_id, validation.to_h)
    Success(article)
  end

  private

  def validate(attributes)
    # returns a Success or Failure
  end
end
```

### 라우트와 액션

라우트는 기대하는 대로 동작하며 URL 전체를 한눈에 보여 주고, 리소스 라우트로 앱이 커져도 라우트를 이해할 수 있게 유지한다고 설명한다.

```ruby
# config/routes.rb
module MyApp
  class Routes < Hanami::Routes
    root to: "home.show"

    resources "articles"
  end
end
```

HTTP 요청은 액션으로 처리하며 엔드포인트마다 액션 클래스가 하나라고 설명한다.
그 안에서는 HTTP만 신경 쓰고 의존성을 통해 비즈니스 로직을 호출하며, 전형적인 액션은 뷰를 렌더링하거나 오퍼레이션을 호출하므로 얇고 따라가기 쉬운 상태로 남는다는 것이다.

```ruby
# app/actions/articles/update.rb
class Update < MyApp::Action
  include Deps[update_article: "articles.update"]

  def handle(request, response)
    result = update_article.call(
      request.params[:id],
      request.params[:article]
    )

    case result
    in Success(article)
      response.redirect_to routes.path(:article, article.id)
    in Failure(validation)
      response.render view, validation:
    end
  end
end
```

### 객체로서의 뷰

뷰도 전용 클래스라고 설명한다.
데이터를 불러오고 뷰 고유 로직으로 장식해 템플릿에 노출하며, 액션에서 렌더링하기 쉽지만 일반 객체이기도 하므로 직접 테스트할 수 있고 다른 필요한 곳에서도 쓸 수 있다는 것이다.

```ruby
# app/views/articles/show.rb
class Show < MyApp::View
  include Deps["repos.article_repo"]

  expose :article do |id:|
    article_repo.get(id)
  end
end
```

```erb
<%# app/templates/articles/show.html.erb %>
<h1><%= article.title %></h1>
<%= article.body_html %>
```

### 그 밖의 특성

표면만 긁었다며 더 있다고 세 가지를 든다.

| 항목       | 설명                                                                                                                         |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 모듈성     | 슬라이스로 하위 도메인이나 하위 시스템 사이에 분명한 경계를 만들 수 있고, 각 슬라이스는 자기 완결적이며 서로 의존할지 어떻게 의존할지를 정할 수 있다 |
| 선택 가능성 | 프레임워크를 얼마나 쓸지 고를 수 있고 무엇이든 제거하거나 교체할 수 있으며 전부 Gemfile에 있다. 풀스택 웹 앱, 가벼운 API, 스트림 처리기 등 필요한 모양으로 만들 수 있다 |
| 로딩 속도  | 똑똑한 코드 로딩 덕분에 앱이 커져도 콘솔과 테스트와 앱 서버가 빠르게 로드된다                                                  |

## 커뮤니티와 정책

페이지 하단은 기술이 아니라 커뮤니티를 다룬다.
커뮤니티 위에 만들어졌다는 제목 아래 친절함과 호기심과 배려를 가져오는 사람들을 위한 곳이라고 적는다.
Hanakai 커뮤니티는 모든 배경과 경험 수준의 사람들이 존중받는다고 느끼고 나누고 성장할 수 있는 곳이며 자랑스러워할 만하고 안전하다고 느낄 수 있는 곳이라는 것이다.
그리고 강조 표시로 나치와 트랜스포브와 인종주의자와 어떤 종류의 편견도 용납하지 않는다고 적고 행동 규범을 링크한다.

후원사로 Sidekiq, Brandon Weaver, Honeybadger, FastRuby.io, AppSignal, SerpApi 여섯을 열거하며 많은 커뮤니티 후원자의 지원도 받는다고 적는다.
Hanakai 후원사나 후원자가 되어 Ruby의 다양한 미래를 만드는 것을 도와 달라고 요청한다.

바닥글에는 Status, Colophon, 행동 규범, 그리고 AI 정책 링크가 있다.

### AI 기여 정책

[별도 페이지](https://hanakai.org/ai-policy)의 AI 기여 정책은 Hanami가 인간을 위해 여기 있다는 문장으로 시작한다.
기여를 환영하고 원하는 도구를 써도 되지만 모든 기여가 인간 우선이어야 한다고 요구한다.
정책의 요지는 기여자가 언제나 저자이며 자기 기여에 온전히 책임을 진다는 것이다.
LLM이 생성한 코드나 텍스트를 유지관리자에게 검토 요청하기 전에 주의 깊게 읽고 검토해야 하며, 여기에는 PR 설명도 포함되고 거기서는 걸러지지 않은 AI 요약이 아니라 개인의 목소리를 듣고 싶다고 적는다.
도구 생성 내용이 상당량 포함되면 투명하게 밝혀야 하고, 유지관리자의 시간을 쓸 만한 품질인지 확신해야 하며 검토 중에 자기 작업에 대한 질문에 답할 수 있어야 한다는 것이다.
적용 범위로 풀 리퀘스트 형태의 코드, 기능 제안, 이슈나 보안 취약점, 이슈와 PR에 대한 의견과 피드백, 커뮤니티 논의 공간의 글을 든다.

에이전트는 허용하지 않는다는 별도 절이 있다.
GitHub Copilot이나 Claude 에이전트처럼 인간 승인 없이 자기 공간에서 행동하는 에이전트를 허용하지 않으며 인간 검토 없이 의견을 게시하는 자동 검토 도구도 마찬가지라는 것이다.
그리고 에이전트 사용을 지원하기 위한 어떤 자료도 저장소에 넣지 않겠다고 적는다.
기여를 쉽게 하는 문서를 추가하고 싶다면 다른 인간을 위해 써 달라는 것이다.

근거로 두 가지를 든다.
커뮤니티에게는 코드에 대한 모든 변경이 진정한 인간의 주의와 배려를 받는다고 믿게 하고 싶다는 것이고, 유지관리자에게는 한정된 시간과 에너지가 가치 있고 건설적인 기여를 검토하는 데 쓰이도록 보장하고 싶다는 것이다.
위반 처리 절차도 명시한다.
유지관리자가 정책을 따르지 않는다고 판단하면 정해진 문구를 붙여 이 PR이 왜 검토할 만큼 가치 있는지 설명해 달라고 요청하고, 기여자가 의미 있게 응하지 않으면 대화를 잠그고 PR을 닫으며, 기여가 에이전트에서 직접 온 것이면 즉시 잠그고 닫는다는 것이다.
정책이 LLVM의 AI 도구 사용 정책과 Mastodon의 AI 기여 정책을 참고했다고 밝힌다.

## 분석

### 페이지 전체가 이름 없는 Rails 비판으로 구성되어 있다

이 페이지에는 Rails가 한 번도 등장하지 않는다.
그런데 각 절이 다루는 주제를 순서대로 놓으면 Rails 애플리케이션에서 반복적으로 보고되는 문제 목록과 정확히 겹친다.
전용 데이터 계층은 모델 하나에 질의가 쌓이는 문제에 대응하고, 오퍼레이션은 서비스 객체의 자리가 정해져 있지 않은 문제에, 객체로서의 뷰는 전역 헬퍼 문제에, 슬라이스는 모듈 경계가 없는 문제에 대응한다.

이 구성이 페이지의 설득 구조를 결정한다.
문제를 명시하지 않고 해법만 보여 주므로, 그 문제를 겪은 독자에게는 각 절이 안도로 읽히고 겪지 않은 독자에게는 더 많은 파일로 읽힌다.
[Ryan Bigg이 Rails의 결함으로 든 세 항목](../rails/amiko-or-hanami.md)이 이 페이지 절 구성과 대응한다는 점이 그 겹침을 확인해 준다.
그가 Hanami를 대안으로 든 것은 취향이 아니라 이 대응 관계 때문이다.

경쟁 상대를 명시하지 않는 선택 자체는 흔하고 합리적이다.
다만 이 경우에는 대가가 크다.
프레임워크의 가치 명제가 상대의 결함을 전제로만 성립하는데 그 상대를 언급하지 않으면, 독자는 두 프레임워크를 비교할 재료를 스스로 조달해야 한다.
HN에서 나온 첫 질문이 정확히 그것이었다.
Rails 단일 문화에 도전하는 것은 반갑지만 Hanami가 내놓는 것이 많아 보이지 않으며 이 릴리스에 Rails가 오랫동안 갖지 않았던 것이 있는지 묻는 것[^hn-paozac]이다.

### 코드 예시의 개수가 설계 철학을 그대로 드러낸다

이 페이지는 하나의 시나리오를 여섯 개의 코드 블록으로 보여 준다.
기사 갱신이라는 한 동작을 위해 릴레이션과 레포와 스트럭트와 오퍼레이션과 액션과 뷰가 각각 자기 파일로 등장한다.

이 배치는 마케팅 실수가 아니라 논지다.
각 파일이 하나의 책임만 갖고 의존성을 명시적으로 선언하며 개별로 테스트된다는 것이 페이지가 파는 것이고, 파일 수는 그 주장의 증거로 제시된다.
`include Deps["repos.article_repo"]`라는 한 줄이 반복적으로 나오는 것도 같은 이유다.
무엇에 의존하는지가 클래스 상단에 적혀 있다는 사실이 그 자체로 논거다.

그래서 이 페이지는 독자를 두 부류로 가른다.
파일 여섯 개를 보고 각 조각이 무엇을 하는지 알겠다고 느끼는 쪽과, Rails에서 컨트롤러와 모델 둘로 끝나는 일에 여섯 개가 필요하냐고 느끼는 쪽이다.
페이지는 후자를 위한 설명을 두지 않으며, 그 판단이 뒤의 비평에서 문제가 된다.

### 커뮤니티 기준을 기능과 같은 층위에 놓는다

기술 절이 끝난 뒤 페이지는 곧바로 커뮤니티로 넘어간다.
그리고 그 절의 문장이 완곡하지 않다.
나치와 트랜스포브와 인종주의자와 어떤 종류의 편견도 용납하지 않는다고 강조 표시로 적는다.

이 배치는 이 문서가 언제 쓰였는지를 말해 준다.
프레임워크 소개 페이지에서 행동 규범은 통상 바닥글 링크로 존재하는데, 여기서는 기능 목록 바로 다음에 본문으로 놓인다.
[Ruby 생태계에서 창시자의 발언과 거버넌스가 프레임워크 선택의 변수가 된 국면](minaswan.md)에서 그것은 선택 기준으로 제시된 것이며, [같은 이유로 시작된 Rails 포크가 같은 문장을 자기 목표에 넣었다는 점](../rails/amiko.md)이 그 맥락을 보여 준다.

후원사 목록이 그 맥락을 한 번 더 확인해 준다.
첫 번째로 열거된 후원사가 Sidekiq이며, [Ruby Central의 후원을 철회한 그 Sidekiq](rubygems-transition.md)이다.
자금의 재배치가 이 페이지에 그대로 기록되어 있다.

## 비평

### 핵심 주장이 반증 불가능하게 서술되어 있고 팀도 그것을 인정한다

이 페이지의 중심 약속은 커져도 계속 즐겁게 작업할 수 있는 앱이다.
그런데 그 약속을 확인할 재료가 페이지에 없다.
이름이 밝혀진 대규모 사례가 없고, 사용 기업 목록이 없고, 다른 프레임워크에서 옮겨 온 팀의 후속 보고가 없다.

HN에서 이 문제가 가장 정면으로 제기됐다.
여러 해 느슨하게 지켜봤지만 써 본 적도 큰 코드베이스에서 쓰인다는 말을 들은 적도 없으며 Rails와 무엇이 그렇게 다른지 아직 잘 모르겠다는 것[^hn-pclowes]이다.
Rails 안티패턴을 피하는 방법을 문서가 짚고 그 의견 대부분에 동의하지만 남들이 그랬다는 이유로 Rails에서 반드시 나쁜 코드를 써야 하는 것은 아니라고 적었고, 대규모 마이그레이션을 여러 회사에서 본 경험으로 그 원인은 프레임워크가 아니라 코드의 극단적 유연성과 수천 명의 개발자가 10년 넘게 만들어 내는 결과였으며 Hanami의 어떤 아키텍처도 그것을 막는다고 보이지 않는다고 짚었다.

Hanami 코어 팀원의 답변이 이 비판을 상당 부분 인정한다.
최근 홈페이지를 다시 만들었고 이런 것들을 더 분명히 해야 한다며 정당한 우려와 질문이라고 답했고, Rails에서 나쁜 코드를 반드시 써야 하는 것이 아니라는 데 동의하며 Hanami에서 나쁜 코드를 막을 수 있다고 주장하지 않는다고 밝혔다[^hn-cllns].
자기들이 하는 일은 어떤 사람들에게 더 잘 맞을 수 있는 선택지를 만드는 것이며 Rails에 완전히 만족한다면 바꿀 이유가 없다고 적었다.
이 답변은 정직하고 설득력 있지만, 페이지가 파는 것과 팀이 인정하는 것 사이에 간격이 있다는 뜻이기도 하다.

주장이 판정 불가능하다는 점은 상반된 경험이 나란히 보고된 데서 드러난다.
Hanami를 딱 하나의 프로덕션 코드베이스에서 썼고 그것이 아주 큰 앱이었는데 이제껏 본 것 중 가장 지저분하고 과설계된 것이었으며, 실제 동작을 감추는 작은 클래스의 폭발로 익사하는 설계로 몰아가는 프레임워크 자체에 일부 책임이 있다는 느낌을 지울 수 없다는 보고[^hn-poszlem]가 있었다.
정반대 경험도 있었다.
소프트웨어 회사에서 Hanami 1 앱을 맡았는데 자기가 작업한 것 중 최고로 설계된 앱이었고 당시 다루던 Rails 앱의 90퍼센트보다 훨씬 나았다는 것[^hn-shoqr]이다.
같은 프레임워크가 양쪽 결과를 모두 만들 수 있다면 페이지의 약속은 프레임워크의 속성이 아니다.

지지자 쪽에서도 이 주장을 조작 가능한 형태로 만들지 못한다는 점이 한 대화에서 드러났다.
Hanami가 가져오는 것은 유지보수 가능한 애플리케이션을 만드는 의도적이고 논리적인 아키텍처이며 취향이 있다는 옹호[^hn-desmond]에 대해, 그 진술은 아무 의미도 없고 Rails에 대해 똑같이 말해도 동등하게 방어 가능한 위치가 되므로 아키텍처의 무엇이 더 낫게 만드는지 물은 반문[^hn-choi]이 나왔고, 그렇게 말할 수 없다는 답이 돌아왔으며 아니라고 하는 것은 좋은 반박이 아니라는 지적이 이어졌다.

### 채택 격차가 세 자릿수인데 페이지가 그것을 다루지 않는다

이 페이지는 성숙도를 시사하지만 규모를 제시하지 않는다.
RubyGems 통계로 확인하면 격차가 크다.

| 젬      | 최신 버전 | 누적 다운로드 |
| ------- | --------- | ------------- |
| rails   | 8.1.3.1   | 약 7억 7,386만 |
| sinatra | 4.2.1     | 약 3억 5,221만 |
| roda    | 3.106.0   | 약 2,090만    |
| hanami  | 3.0.1     | 약 120만      |

Rails 대비 약 640분의 1이며 Roda보다도 17배 적다.
이 숫자가 프레임워크의 품질을 말해 주지는 않는다.
그러나 페이지가 파는 것이 규모가 커진 뒤의 유지보수성이라면, 규모가 커진 사례가 관측 가능해야 그 주장을 확인할 수 있다.
누적 다운로드 120만은 그 사례가 몇 개인지에 대한 상한을 시사한다.

이 격차는 이 프레임워크를 Rails의 준비된 대안으로 제시하는 논증에도 부담이다.
[Hanami가 10년 가까이 Ruby 회사들에서 안정적으로 쓰였으므로 그리로 옮기면 된다는 주장](../rails/amiko-or-hanami.md)에서 빠진 것이 정확히 이 항목이며, 그 주장을 뒷받침하려면 페이지에 있어야 할 사용 사례가 없다.
Hanami를 비판하는 근거가 아니라 그 주장을 검증할 수 없다는 지적이다.

페이지가 Rails에서의 이전 경로를 다루지 않는다는 점도 같은 문제에 속한다.
프레임워크를 얼마나 쓸지 고를 수 있고 무엇이든 제거하거나 교체할 수 있다고 적혀 있지만, 기존 Rails 앱을 어떻게 옮기는지에 대한 안내는 없다.
실제로 채택이 일어나는 경로는 코어 팀원이 답변에서 언급한 쪽이다.
완전히 모듈형이므로 Hanami의 일부를 Rails 앱에 끌어올 수 있고 가장 인기 있는 것이 `dry-validation`이라는 것[^hn-cllns]이며, 이 사실이 페이지에는 없다.

### 명시성의 비용을 값으로 계산하지 않는다

이 페이지는 계층 분리의 이득만 서술한다.
각 조각이 하나의 일을 하고 개별로 테스트되며 의존성이 선언되어 있다는 것이다.
그런데 같은 설계가 부과하는 비용은 한 번도 언급되지 않는다.

비용은 페이지의 코드 예시 자체가 보여 준다.
하나의 갱신 동작에 파일 여섯 개와 그만큼의 간접 참조가 생기며, 어떤 요청이 무엇을 하는지 알려면 액션에서 오퍼레이션으로, 오퍼레이션에서 레포로, 레포에서 릴레이션으로 따라가야 한다.
작은 앱에서 이것은 순수한 부담이고 큰 앱에서 이득으로 바뀐다는 것이 이 설계의 전제인데, 그 전환점이 어디인지에 대한 안내가 없다.
앞서 인용한 과설계 보고[^hn-poszlem]가 지목한 실패 양상이 정확히 그 전환점을 잘못 판단한 결과다.

이 페이지가 제시할 수 있었던 것은 언제 쓰지 말아야 하는지다.
어느 규모 아래에서는 이 구조가 과하다는 서술이나, 슬라이스를 나누기 전에 확인할 신호 같은 것이다.
모든 것을 이득으로만 제시하면 판단 기준을 독자가 만들어야 하고, 그러면 프레임워크의 도구를 오용한 결과가 프레임워크의 평판으로 돌아온다.

성능 주장에도 같은 문제가 있다.
Hanami 3.0 발표에 기본값으로 더 빠르다는 항목이 있었는데 개선 전후를 비교할 벤치마크를 보고 싶다는 요청[^hn-whiskey]이 나왔고, 코어 팀원이 자기가 그 작업 대부분을 했고 전후 벤치마크를 넣고 싶었지만 바빠서 못 했다고 답했다[^hn-cllns-bench].
오래전 벤치마크에서 속도가 장점으로 광고되었는데도 ActiveRecord가 훨씬 빨라 실망했다는 회고[^hn-dima]도 있었고, 최근 비교로는 대체로 비슷하며 Hanami가 약간 빠르다는 반응[^hn-nine]이 이어졌다.
곧 페이지의 속도 관련 서술은 아직 공개 근거를 갖지 않은 상태다.

### 명시적 모듈 구성이 Ruby에서 구체적 함정을 만든다

이 페이지의 설계 논의는 아키텍처 취향 수준에서 이루어지지만, 실제 구현이 만드는 언어 차원의 문제를 지적한 의견이 Lobste.rs에 있었다.

Hanami와 Brut을 Rails 대안으로 지켜봤는데 둘 다 이름 공간을 위해 모듈을 쓰도록 밀어붙이며 그것이 Zeitwerk 같은 오토로더와 결합하면 자기 발을 쏘는 장치가 된다는 것[^lob-puerco]이다.
Ruby에는 진짜 이름 공간이 없으므로 Rails가 따르는 접미사나 접두사 관례를 받아들이는 편이 낫고 이상적이지는 않아도 놀람이 가장 적은 길이라는 판단이었다.

왜 함정인지도 구체적으로 설명됐다.
새 상수를 도입하면 손대지 않은 다른 파일의 코드를 깨뜨릴 수 있으며 원격 작용 버그는 디버깅이 가장 어려운 종류라는 것이다.
앱에 `User` 모델이 있고 `Lobsters` 모듈을 이름 공간으로 쓰는 상황에서 나중에 `Lobsters::User`를 추가하면, 이전에 `::User`로 해석되던 코드가 파일을 건드리지 않았는데도 `Lobsters::User`로 해석되며 어느 쪽으로 해석되는지가 로드 순서에 달려 있어 오류가 깜빡이는 테스트로 나타날 수 있다는 설명이다.
프로덕션에서는 Rails가 전부 즉시 로드하므로 항상 더 구체적인 클래스로 해석된다고 덧붙였다.

같은 사람이 Hanami가 실제로 더 나은 항목도 열거했다는 점을 함께 봐야 한다.
라이브러리 우선 접근과 슬라이스 모듈성을 좋게 보고, 엔드포인트당 클래스 하나가 더 나은 판단이며 Rails 컨트롤러는 일부 엔드포인트에만 쓰이는 메서드를 갖기 마련이고 테스트 설정도 엔드포인트마다 크게 달라 별도 클래스가 합리적이라고 적었다.
매개변수 검증 이야기가 잘 설계되었고 Rails에는 그것이 아예 없다며 Strong Parameters의 목표는 매개변수 검증이 아니라고 짚었으며, 뷰가 템플릿에 데이터를 명시적으로 노출하는 것을 인스턴스 변수에 의존하는 관행보다 낫다고 평가했다.
곧 이 프레임워크의 설계 이득은 실재하며, 페이지가 다루지 않는 것은 그 이득이 Ruby의 상수 해석 방식과 만나는 지점이다.

## 인사이트

### 이 프로젝트에서 가장 차별적인 문서가 바닥글에 있다

이 페이지가 파는 것은 아키텍처이고 그 주장은 판정하기 어렵다.
반면 판정이 필요 없는 차별점이 하나 있는데 그것은 바닥글 링크로만 존재한다.
AI 기여 정책이다.

이 문서는 취향 진술이 아니라 운영 규칙이다.
기여자가 저자이고 책임자라는 원칙, 도구 생성 내용의 공개 의무, 인간 승인 없이 행동하는 에이전트와 자동 검토 도구의 금지, 위반 시 붙일 정확한 문구, 그리고 에이전트에서 직접 온 기여는 즉시 잠그고 닫는다는 처리 절차까지 적혀 있다.
가장 강한 대목은 에이전트 사용을 지원하기 위한 어떤 자료도 저장소에 넣지 않겠다는 문장이며, 이것은 저장소에 에이전트용 지침 파일을 두지 않겠다는 선언이다.

이 결정이 중요한 이유는 같은 언어 생태계가 정반대 위치에 있기 때문이다.
[Ruby 코어 저장소에서 공동 저자 트레일러 기준으로 Claude가 상위 기여자에 오른 상태](minaswan.md)와 이 정책은 같은 시기에 공존한다.
한쪽은 에이전트 기여를 흡수하고 다른 쪽은 명시적으로 거부하며, 두 선택의 결과는 1년 안에 비교 가능한 형태로 나타날 것이다.
비교할 지표는 기여 건수가 아니라 검토 처리량과 병합 후 회귀율이다.
정책이 밝힌 근거가 정확히 그 지점이며, 유지관리자의 한정된 시간이 가치 있는 기여 검토에 쓰이도록 하겠다는 것이다.

이 정책에는 값이 붙는다.
에이전트를 전제로 작업하는 기여자를 잃고, 저장소에 지침 파일을 두지 않으므로 그런 기여자가 진입할 때 마찰이 커진다.
소규모 프로젝트에서 이것은 감당 가능한 손실이고 검토 병목이 실제 제약인 프로젝트에서는 이득일 수 있다.
그리고 이 판단이 프레임워크 선택 기준이 될 수 있다는 점이 새로운 국면이다.
지금까지 프레임워크를 고르는 축은 설계와 성능과 채택률이었는데, 여기에 이 코드베이스에 무엇이 병합되는지에 대한 정책이 추가됐다.

### 더 나은 아키텍처는 구조적으로 가장 팔기 어려운 상품이다

이 프레임워크의 채택 부진을 마케팅 문제로 보는 시각이 있지만 원인은 상품의 성질에 있다.
관심사 분리의 이득은 채택 후 수년이 지나 실현되고 비용은 첫날에 지불된다.
그래서 구매를 정당화할 수 있는 사람은 이미 큰 앱에서 고통을 겪은 사람뿐이다.

그런데 그 조건이 곧 구매 불가능의 조건이다.
큰 Rails 앱에서 유지보수 고통을 겪은 사람은 정의상 이전할 수 없는 큰 Rails 앱을 가지고 있다.
반대로 이전 비용이 낮은 신규 프로젝트의 담당자는 아직 그 고통을 겪지 않았으므로 여섯 개의 파일이 왜 필요한지 체감하지 못한다.
곧 이 페이지가 설명하는 가치를 이해하는 집단과 그 가치를 구매할 수 있는 집단이 거의 겹치지 않는다.

이 구조가 모두 Hanami로 옮기라는 처방이 왜 작동하지 않는지를 동기와 무관하게 설명해 준다.
[그 처방을 낸 글](../rails/amiko-or-hanami.md)이 이전 비용을 계산하지 않았다는 점을 앞서 지적했지만, 더 근본적인 문제는 이전 비용을 지불할 수 있는 사람이 그 처방의 대상이 아니라는 것이다.

역사적으로 이 문제를 푼 경로는 프레임워크 교체가 아니라 부분 도입이었다.
Java 진영에서 Spring이 확산된 방식이 기존 애플리케이션 안에 조각으로 들어가는 것이었고, 그래야 이득을 미리 확인한 뒤 비용을 점진적으로 지불할 수 있다.
Hanakai는 이미 그 경로를 갖고 있다.
코어 팀원이 밝힌 대로 Hanami의 일부를 Rails 앱에 끌어올 수 있고 가장 인기 있는 것이 `dry-validation`이며, Dry와 Rom이 독립 젬으로 존재한다는 사실이 그 쐐기다.
그런데 페이지는 그것을 뒤쪽의 부가 특성으로만 언급한다.
팔기 가장 쉬운 것이 가장 눈에 띄지 않는 자리에 있다.

### Hanakai의 통합은 마케팅 개편이 아니라 거버넌스 답안이다

세 프로젝트가 하나의 브랜드로 합친 것이 이 페이지의 배경이며, 통상 이런 통합은 인지도 문제로 읽힌다.
그런데 합쳐진 결과물의 구성 항목을 보면 다른 성격이 드러난다.
행동 규범, AI 정책, 후원사 목록, 젬별 버전과 빌드 상태를 보여 주는 Status 페이지, Colophon, 단일 코드 저장소 조직이다.

이 목록을 같은 시기 Ruby 생태계가 부족하다고 지적받은 항목과 대조하면 대응 관계가 보인다.
[선출된 거버넌스가 없다는 지적](ruby-central-legacy.md), [합병 시점에 자산 명세가 없었다는 문제](ruby-central-legacy.md), [소유권 이전 발표에 관리 절차가 없었다는 문제](rubygems-transition.md)에 대해, 이쪽은 문서화된 규범과 정책과 자산 목록을 공개해 두었다.
완전한 거버넌스 문서는 아니지만 기존 기관이 갖지 못했던 종류의 공개 기록이다.

후원사 구성이 이 해석을 뒷받침한다.
첫 번째로 열거된 Sidekiq은 Ruby Central에 대한 후원을 철회한 쪽이며, 곧 이 목록은 자금이 어디로 이동했는지에 대한 기록이다.
프레임워크 소개 페이지가 생태계 재편의 스냅숏 기능을 겸하고 있다.

다만 이 구성에는 계산되지 않은 부담이 따른다.
가치를 기준으로 사람을 모으는 프로젝트는 그 가치를 판정할 의무를 함께 진다.
누가 규범 위반을 판정하고 어떻게 항소하는지, AI 정책 위반 여부를 유지관리자 개인이 판단할 때 일관성을 어떻게 유지하는지가 정해져 있어야 하며, AI 정책에는 위반 처리 절차가 있지만 행동 규범 쪽의 판정 주체는 페이지에서 확인되지 않는다.
그리고 후원사 여섯 곳과 커뮤니티 후원자로 이루어진 예산은 그 판정 업무를 감당할 기반으로 튼튼하지 않다.
자금 집중이 문제였던 생태계에서 자금 부족이 다음 제약이 되는 구도다.

### 명시성은 지식 비용을 조정 비용으로 바꾸며 채용 규모에서 부호가 뒤집힌다

이 페이지가 자랑하는 선택 가능성은 프레임워크를 얼마나 쓸지 고르고 무엇이든 제거하거나 교체할 수 있으며 전부 Gemfile에 있다는 것이다.
개별 팀에게 이것은 자유이지만 생태계 차원에서는 다른 결과를 낳는다.

관례를 숨기는 프레임워크에서는 개발자가 프레임워크 하나를 배우면 아무 앱이나 읽을 수 있다.
[모든 Rails 앱이 같은 폴더 구조라는 성질](../rails/documentary.md)이 그것이며, 그 성질의 진짜 가치는 우아함이 아니라 개발자의 호환성이다.
반면 각 앱이 무엇을 제거했고 무엇으로 교체했으며 슬라이스를 어떻게 나눴는지를 스스로 결정하는 프레임워크에서는 앱마다 다른 지식이 필요하다.
개인의 지식 비용은 줄고 조직의 조정 비용은 늘어난다.

이 교환이 규모에 따라 부호를 바꾼다.
소수의 숙련된 팀이 하나의 앱을 오래 유지하는 경우 명시성이 이득이며, 앞서 인용한 잘 설계된 Hanami 앱 사례가 그 조건에 해당한다.
반대로 사람이 자주 들고나는 조직에서는 관례가 이득이며, 새로 온 사람이 첫 주에 기여할 수 있는지가 프레임워크 선택의 실질 기준이 된다.
그리고 대규모 조직이 실제로 선택하는 축이 후자라는 점이 Rails의 채택 규모를 설명하는 요인 중 하나다.

이 축을 어느 쪽도 값으로 계산하지 않는다는 점이 이 논쟁의 공백이다.
이 페이지는 명시성의 이득만 적고, [Hanami로 옮기라는 처방](../rails/amiko-or-hanami.md)도 앱 내부 설계만 논하며 인력 유동성을 다루지 않는다.
그리고 앞서 인용한 큰 코드베이스 마이그레이션 관찰[^hn-pclowes]이 실은 이 축을 가리킨다.
문제의 원인이 프레임워크가 아니라 수천 명의 개발자가 10년 넘게 만들어 낸 결과였다는 진술은, 프레임워크 선택보다 인력 규모가 지배 변수라는 뜻이다.
그렇다면 아키텍처 개선으로 해결하겠다는 접근 자체가 잘못된 층위를 겨냥한 것일 수 있으며, 이 페이지는 그 가능성을 검토하지 않는다.

- 이 페이지 자체에 대한 HN이나 Lobste.rs 스레드는 없다. 반응은 Hanami 3.0 발표문에 대한 스레드에서 가져왔다. HN <https://news.ycombinator.com/item?id=48750527> (102점, 30개 댓글), Lobste.rs <https://lobste.rs/s/vyosfg/hanami_3_0_full_bloom> (20점, 3개 댓글). Hanakai 홈페이지 자체도 제출됐으나 4점, 댓글 0개였다.
- HN 스레드에는 Hanami 코어 팀원 `cllns_ruby`가 참여해 대부분의 비판에 직접 답했다.
- GeekNews에서 Hanami에 대한 스레드는 찾지 못했다.
- 관련 문서: [Amiko는 미덕 과시일 뿐이며 Hanami로 가야 한다](../rails/amiko-or-hanami.md), [Rails는 완성되었으므로 소수 인원으로 포크할 수 있다](../rails/amiko.md), [Matz가 좋은 사람인지는 중요하지 않다](minaswan.md), [RubyGems와 Bundler 저장소 소유권을 Ruby 코어 팀이 맡는다](rubygems-transition.md), [Rails 20년의 이야기](../rails/documentary.md)

---

[^hn-paozac]: HN 사용자 `paozac`: “I'm happy someone's challenging the Rails almost-monoculture in the Ruby ecosystem, but Hanami doesn't seem to bring much to the table. Is there anything in this release that Rails hasn't had for years?”
[^hn-pclowes]: HN 사용자 `pclowes`: “I have loosely followed Hanami for years but never used it or heard of it used in a large codebase. I still don't quite understand what it does all that differently from Rails?... you don't _have_ to write bad code in rails just because a lot of others have... I would say the driver behind those migrations wasn't so much the framework as the extreme flexibility of the code and what that produces with thousands of developers over 10+ years. I don't see how any architecture of Hanami prevents that.”
[^hn-cllns]: HN 사용자 `cllns_ruby`(Hanami 코어 팀원): “We re-did our homepage recently, and we should make these things clearer. They're legitimate concerns and questions. We agree you don't have to write bad code in Rails, and we don't pretend that we can prevent bad code in Hanami... Really what we're doing is building an *option* for building Ruby apps that may speak better to some people. If you're completely happy with Rails then there's no reason to change... it's completely modular: you can pull parts of Hanami into a Rails app. The most popular one people pull into Rails apps is dry-validation”
[^hn-poszlem]: HN 사용자 `poszlem`: “I've used Hanami in exactly one production codebase (but it was a huge one)... that app was hands down one of the messiest, most overengineered pile of hot garbage I've ever laid eyes on, and I can't shake the feeling that at least SOME of the blame lands on the framework itself, for nudging you toward a design where you drown in an explosion of tiny classes that do nothing but hide the actual behaviour from you.”
[^hn-shoqr]: HN 사용자 `shoqr`: “I had the complete opposite experience... we had a client with a Hanami app (version 1). It was one of the best-engineered apps I've worked on - much better than 90% of the Rails apps we were working with at the time.”
[^hn-desmond]: HN 사용자 `itsdesmond`: “What Hanami brings is an intentional and well-reasoned architecture that supports building maintainable applications. It has taste.”
[^hn-choi]: HN 사용자 `choilive`: “That statement means nothing. You could say the exact same thing about Rails and have an equally defensible position. What about its architecture makes it better?” 이후 `throwatdem12311`이 “'Nuh uh' Isn't a good rebuttal.”이라고 덧붙였다.
[^hn-whiskey]: HN 사용자 `xswhiskey`: “It'd be nice to see some benchmarks to compare the before vs after on the perf gains in the Faster by default heading.”
[^hn-cllns-bench]: HN 사용자 `cllns_ruby`: “I did most of this work and I wanted to add before-and-after benchmarking but I got busy.” RealWorld 프로젝트 구현을 공개한 뒤 Rails 구현과 비교하겠다고 밝혔다.
[^hn-dima]: HN 사용자 `swe_dima`: “many years ago when Hanami was just getting popular I remember doing benchmarks against Rails when it comes to SQL and was unpleasantly surprised when Rails' ActiveRecord ended up being much faster, despite 'speed' being advertised as one of the advantages”
[^hn-nine]: HN 사용자 `nine_k`: “Is this still the case? I was able to find only one fresh comparison, and in it they show approximate parity, with Hanami being slightly faster.”
[^lob-puerco]: Lobste.rs 사용자 `PuercoPop`: “One thing I dislike from both is that they push you to use Modules for namespacing, which combined with Zeitwerk (or another autoloader) is a footgun. Ruby doesn't really have namespaces, its better to embrace the Suffix (or Prefix) convention that Rails follows IMHO.” 이후 “Because it is possible to break code you didn't touch (in other files) by introducing a new constant. Action at a distance bugs are one of the hardest to debug.”라며 `Lobsters::User` 예시로 로드 순서 의존 문제를 설명했다. 같은 글에서 엔드포인트당 클래스 하나, 매개변수 검증, 명시적 뷰 노출을 Rails보다 나은 점으로 꼽았다.
