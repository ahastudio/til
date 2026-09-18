# RubyLLM

> The Ruby-native AI framework. Work with models, tools, and agents through one
> consistent API, in plain Ruby or Rails.

<https://rubyllm.com/>

<https://github.com/crmne/ruby_llm>

HN 토론:

- <https://news.ycombinator.com/item?id=43331847> (645점, 169개 댓글)
- <https://news.ycombinator.com/item?id=48660711> (447점, 82개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/ph49qi/rubyllm_single_beautiful_ruby_framework> (4점, 0개 댓글)

## 소개

RubyLLM은 스스로를 Ruby 네이티브 AI 프레임워크라고 소개한다.
모델과 도구와 에이전트를 하나의 일관된 API로 다루며, 순수 Ruby에서도 Rails에서도 같은 방식으로 쓴다는 것이다.

현재 안정 버전은 **2.0.0**이고 제공자는 **17개**다.
스타 4,379개, 포크 501개, 열린 이슈 7개이며 MIT 라이선스다. 2025년 1월 30일에 만들어져 지금도 활발히 푸시된다.
Chat with Work라는 제품에서 실전 검증되었다고 밝힌다.

설계 동기는 단순하다.
각 AI 제공자는 저마다의 클라이언트와 API, 응답 형식을 들고 나온다.
RubyLLM은 이 혼란을 하나의 API로 흡수해 제공자 교체 비용을 낮춘다.

2.0에서 구조적으로 달라진 것이 **제공자와 프로토콜의 분리**다.
제공자는 인증과 엔드포인트, 모델 카탈로그, 서비스별 동작을 공급하고, 프로토콜은 요청 형식과 응답 파싱과 스트리밍을 담당한다.
RubyLLM이 모델과 연산에 맞는 프로토콜을 고르므로 애플리케이션은 제공자가 바뀌어도 같은 API를 유지한다.
새 제공자는 기존 프로토콜을 재사용할 수 있고, 제공자 gem 생성기가 패키지와 설정과 테스트를 만들어 준다.

## 2.0에서 무엇이 늘었나

1.16이 이미 지원하던 것은 채팅, 도구, 에이전트, 구조화된 출력, 사고, 임베딩, 이미지, 전사, 모더레이션이다.
2.0이 새로 더한 것은 영상, 음성 합성, OCR, 리랭킹, 파일, 배치, 그리고 제공자 호스팅 도구를 위한 공통 API다.
제공자로는 Cohere, Deepgram, ElevenLabs, Ollama Cloud가 새로 들어와 17개가 되었다.

| 영역      | 2.0에서 추가된 것                                                               |
| --------- | ------------------------------------------------------------------------------- |
| 대화 제어 | 도구 승인, 명시적 루프 제어(`ask_later`/`generate`/`run_tools`/`step`), 취소    |
| 신뢰성    | 모델 폴백(`with_fallbacks`)과 폴백 콜백                                         |
| 비용      | 시도 단위 사용량 원장, 재시도·폴백·취소 포함                                    |
| 컨텍스트  | 공통 프롬프트 캐싱(`with_caching`, `cache_until_here`), 압축(`with_compaction`) |
| 근거      | 문서·웹 검색·그라운딩을 아우르는 공통 인용 객체                                 |
| 미디어    | 영상 생성(`animate`), 음성 합성(`speak`), 화자 분리·타임스탬프 전사             |
| 문서      | OCR(`ocr`), 리랭킹(`rerank`), 멀티모달 임베딩                                   |
| 서버 도구 | 웹 검색·코드 실행·원격 MCP(`with_server_tools`), 호스팅 리서치(`research`)      |
| 규모      | 배치(`RubyLLM.batch`), 파일 업로드(`upload`/`download`), 토큰 계수              |
| 관측      | `RubyLLM.workflow`로 다중 에이전트 실행을 텔레메트리에서 상관                   |

이름도 정리되었다. `max_tokens`가 `max_output_tokens`로 바뀌었고, 제공자별 요청 옵션은 `with_provider_options`로 모였다.

## 설치와 설정

```bash
bundle add ruby_llm --version 2.0.0
```

설정은 스크립트 앞부분이나 Rails의 `config/initializers/ruby_llm.rb`에 둔다.

```ruby
require 'ruby_llm'

RubyLLM.configure do |config|
  config.openai_api_key = ENV.fetch('OPENAI_API_KEY')

  # 재시도 정책. 기본값은 max_retries 3, retry_interval 0.1
  config.max_retries = 5
  config.retry_interval = 0.5
  # config.retry_backoff_factor = 2        # 기본 2
  # config.retry_interval_randomness = 0.5 # 기본 0.5
end
```

쓰는 제공자만 설정하면 된다. 예제 기준으로 파일 입력은 Gemini, 영상은 xAI, OCR은 Mistral, 리랭킹은 Cohere가 필요하다.
1.16을 쓰는 앱이라면 2.0을 배포하기 전에 업그레이드 가이드를 먼저 따라야 한다.

## 기본 대화

```ruby
chat = RubyLLM.chat
response = chat.ask "What is Ruby on Rails?"
puts response.content

# 같은 chat 객체가 대화를 기억하므로 이어서 물으면 된다
chat.ask "How do I create my first Rails app?"
```

스트리밍은 블록을 넘기면 된다.

```ruby
chat.ask "Tell me a story about a Ruby programmer" do |chunk|
  print chunk.content
end
```

파일은 `with:`로 넘긴다. 여러 개를 배열로 줄 수도 있다.

```ruby
chat = RubyLLM.chat(model: "gemini-3.7-flash")
chat.ask "What's in this image?", with: "ruby_conf.jpg"
chat.ask "Analyze these files", with: ["diagram.png", "report.pdf", "notes.txt"]
```

구조화된 출력은 Schematist 스키마를 쓴다. 1.x의 `RubyLLM::Schema`가 아니라는 점에 주의한다.

```ruby
class PersonSchema < Schematist::Schema
  string :name
  integer :age
end

response = RubyLLM.chat.with_schema(PersonSchema).ask "Alice is 30 years old."
response.parsed
# => {"name" => "Alice", "age" => 30}
```

단일 연산도 모두 최상위 메서드로 있다.

```ruby
RubyLLM.paint "a sunset over mountains in watercolor style"   # 이미지
RubyLLM.animate "a paper boat sailing down a rainy gutter"     # 영상
RubyLLM.speak "Hello, welcome to RubyLLM!"                     # 음성 합성
RubyLLM.transcribe "meeting.wav"                               # 전사
RubyLLM.ocr "contract.pdf"                                     # OCR → markdown
RubyLLM.embed "Ruby is elegant and expressive"                 # 임베딩
RubyLLM.rerank("How do I reset my password?", documents)       # 리랭킹
RubyLLM.moderate("Some user-generated content").flagged?       # 모더레이션
```

## 도구

도구는 `RubyLLM::Tool`을 상속하고 `execute`를 구현한다. 1.x 예제에서 쓰이던 `desc`가 아니라 `description`이다.

```ruby
class Weather < RubyLLM::Tool
  description "Gets current weather for a location"

  # 파라미터 선언이 없으면 execute의 키워드 인자에서 JSON Schema를 만든다.
  # 필수 키워드는 필수 string, 선택 키워드는 선택 string이 된다.
  def execute(latitude:, longitude:)
    response = Faraday.get("https://api.open-meteo.com/v1/forecast",
                           latitude: latitude, longitude: longitude,
                           current: "temperature_2m,wind_speed_10m")
    JSON.parse(response.body)
  rescue Faraday::ConnectionFailed
    # 모델이 복구할 수 있는 오류는 error 키로 돌려준다
    { error: "The weather service is unavailable. Try again later." }
  end
end

chat.with_tools(Weather).ask "What's the weather in Berlin? Latitude 52.52, longitude 13.40."
```

클래스 이름이 스네이크 케이스로 바뀌어 모델에게 노출되며 끝의 `Tool`은 떨어진다.
`WeatherLookup`은 `weather_lookup`이 되고 `WeatherTool`은 `weather`가 된다. `self.tool_name`으로 덮어쓸 수 있다.

Ruby 메서드 시그니처는 신뢰할 만한 JSON Schema 타입과 설명을 노출하지 못하므로, 그 세부가 중요하면 `parameter`나 `parameters`로 명시해야 한다.

도구 집합은 세 가지로 조작한다.

```ruby
chat.with_tools(CurrentTime)              # 기존 도구에 추가
chat.with_tools(nil).with_tools(CurrentTime)  # 집합 교체
chat.with_tools(nil)                      # 비우기
```

### 오류를 모델에 돌려줄지 애플리케이션으로 올릴지

도구 안의 오류 처리는 복구 가능성으로 갈린다.

모델이 회복할 수 있는 오류, 즉 모델이 준 잘못된 인자나 일시적 조회 실패는 `:error` 키를 가진 Hash로 돌려준다.
모델은 그것을 도구 출력으로 보고 다시 시도하거나 다른 접근을 택한다.

도구 자체나 애플리케이션 상태의 문제, 즉 DB 연결 유실이나 설정 오류나 회복 불가능한 외부 실패는 그대로 `raise`한다.
그러면 RubyLLM 상호작용이 멈추고 애플리케이션의 오류 처리로 올라간다.

```ruby
class DatabaseQueryTool < RubyLLM::Tool
  def execute(query:)
    User.find_by_sql(query)
  rescue ActiveRecord::ConnectionNotEstablished => e
    raise e                                    # 애플리케이션이 처리하게 둔다
  rescue StandardError => e
    { error: "Database query failed: #{e.message}" }  # 덜 치명적인 것만 모델에 돌려준다
  end
end
```

## 에이전트

같은 지침과 도구를 컨트롤러와 잡과 서비스마다 다시 붙이는 대신, 클래스로 한 번 정의해 쓰는 방식이다.

```ruby
class SupportAgent < RubyLLM::Agent
  model "gpt-5.6-luna"
  instructions "You are a concise support assistant."
  tools SearchDocs, LookupAccount
  tool_options choice: :auto, calls: :one
  temperature 0.2
  max_output_tokens 256
end

SupportAgent.new.ask "How do I reset my API key?"
```

클래스 매크로는 `chat.with_*`와 같은 인자를 받는다. `model`, `tools`, `tool_options`, `server_tools`, `instructions`, `temperature`, `max_output_tokens`, `thinking`, `citations`, `caching`, `end_user`, `compaction`, `provider_options`, `headers`, `schema`, `fallbacks`, `context`, `chat_model`, `inputs`가 있다.

기능 매크로는 세 가지 모양을 공유한다. 인자 없이 부르면 기본값을 켜고, `false`를 넘기면 끄고, 옵션을 넘기면 조정한다.

```ruby
class WorkAssistant < RubyLLM::Agent
  thinking
  caching ttl: "1h"
  compaction
  citations
end
```

### 런타임 컨텍스트

에이전트는 두 모드로 동작한다. `.chat`은 `RubyLLM::Chat`을 돌려주고, `chat_model`을 설정하면 `.create/.create!/.find`가 Active Record 모델을 돌려준다.

런타임 값은 블록이나 람다로 늦게 평가된다. 이것이 Rails에서 결정적으로 유용하다.

```ruby
class WorkAssistant < RubyLLM::Agent
  chat_model Chat
  inputs :workspace

  # chat은 실행 컨텍스트에서 항상 사용할 수 있다.
  # .chat 모드에서는 RubyLLM::Chat, Rails 모드에서는 chat_model 레코드다.
  instructions current_date_time: -> { Time.current.strftime("%B %d, %Y") },
               display_name: -> { chat.user.display_name_or_email }

  tools do
    [
      TodoTool.new(chat: chat),
      GoogleDriveSearchTool.new(user: chat.user)
    ]
  end
end
```

런타임 `chat`에 의존하는 값은 반드시 블록이나 람다여야 한다. 클래스 로드 시점에 평가되는 식으로 쓰면 안 된다.

모델도 블록을 받으므로 입력에 따라 라우팅할 수 있다. 다만 모델 블록은 chat이 생기기 전에 돌므로 `inputs`는 읽지만 `chat`은 읽지 못한다.

```ruby
class CardAgent < RubyLLM::Agent
  inputs :card
  model { card.special_type? ? "gpt-4.1-mini" : "gpt-4.1-nano" }
end

CardAgent.chat(card: card)
```

### 프롬프트 규약

이름이 있는 에이전트는 관례 경로의 지침 템플릿을 자동으로 쓴다.
`WorkAssistant`는 `app/prompts/work_assistant/instructions.txt.erb`를, `Admin::SupportAgent`는 `app/prompts/admin/support_agent/...`를 본다.
지침 선택 순서는 클래스의 `instructions` 선언이 먼저이고 그다음이 관례 템플릿이다. 명시적으로 `prompt("instructions")`를 불렀는데 파일이 없으면 `RubyLLM::PromptNotFoundError`가 난다.

### 에이전트 단위 오류 처리

`rescue_from`이 오류 처리를 모든 호출 지점에서 에이전트 클래스로 옮긴다.

```ruby
class ApplicationAgent < RubyLLM::Agent
  rescue_from RubyLLM::RateLimitError, RubyLLM::ServerError, with: :handle_transient
  rescue_from RubyLLM::BadRequestError, with: :handle_bad_request

  private

  def handle_transient(error)
    StatsD.increment("llm.api_error", tags: ["type:transient"])
    raise                                   # 계측 후 다시 올린다
  end

  def handle_bad_request(error)
    Sentry.capture_exception(error)         # 이쪽은 우리 파이프라인의 버그다
    raise
  end
end
```

핸들러는 에이전트의 `ask`, `say`, `ask_later`, `complete`, `generate`, `run_tools`, `step`, `count_tokens`를 덮고 에이전트 인스턴스 위에서 돌며 `ActiveSupport::Rescuable` 의미를 따른다.

## 루프를 직접 모는 방법

`ask` 한 번이 도구 호출 루프 전체를 처리한다. 모델이 도구를 요청하면 `execute`를 부르고, 결과를 도구 메시지로 만들어 모델에게 이어 가게 하고, 모델이 더 이상 도구를 요청하지 않을 때 반환한다.

2.0은 그 루프를 쪼개 쓸 수 있게 했다.

| 메서드      | 하는 일                                        |
| ----------- | ---------------------------------------------- |
| `ask_later` | 질문을 스테이징만 한다                         |
| `generate`  | 모델에게 응답 하나를 요청한다                  |
| `run_tools` | 대기 중인 도구를 실행한다                      |
| `step`      | 생성 또는 도구 실행 하나만큼 대화를 진전시킨다 |
| `complete?` | 끝났는지 확인한다                              |
| `complete`  | 남은 것을 이어서 끝낸다                        |
| `cancel`    | 진행 중인 실행을 취소한다                      |

이 조합으로 반복 예산을 걸거나, 한 턴을 한 잡으로 돌리거나, 작업을 다른 에이전트에 넘길 수 있다.

### 사람 승인이 필요한 도구

도구가 실행 전에 승인을 요구할 수 있다.

```ruby
# 승인이 필요한 도구는 호출이 대기 상태로 남고 ask가 반환된다
chat.ask "Publish post 42."

# 애플리케이션이 제안된 동작을 보여 주고 결정을 받은 뒤 이어 간다
chat.approve(chat.pending_approvals.first)
chat.complete

# 거절하면 모델이 그 결정을 받고 응답한다
# chat.deny(tool_call_id)
```

Rails에서는 이것이 지속형 에이전트가 된다. 승인 핸들러나 잡이 에이전트를 다시 불러와 이어 갈 수 있다.

```ruby
chat = EditorialAgent.find(chat_id)
chat.approve(tool_call_id)
chat.complete
```

저장된 전사는 완료된 작업을 기록한다. 잡이 결과를 저장하기 전에 멈추면 그 연산이 다시 돌 수 있으므로, **도구는 재시도를 견뎌야 한다**.

## Rails 통합

```bash
bin/rails generate ruby_llm:install
bin/rails db:migrate
bin/rails ruby_llm:load_models

bin/rails generate ruby_llm:chat_ui   # 선택: 동작하는 채팅 UI
```

생성되는 기본 키와 외래 키는 애플리케이션의 `config.generators`의 `active_record.primary_key_type` 설정을 따른다. `:uuid`도 지원하며 기본은 `:bigint`다.

```ruby
class Chat < ApplicationRecord
  acts_as_chat
end

chat = Chat.create!(model: "gpt-5.6-luna")
chat.with_instructions "Explain Ruby with short, runnable examples."
chat.ask "What's in this file?", with: report.document   # Active Storage 첨부를 그대로 넘긴다
chat.messages.count
chat.cost.total
```

소유권 경계가 2.0에서 명확해졌다.
애플리케이션이 `Chat`과 `Message` 모델을 소유하므로 사용자와 권한과 제목 같은 관계를 붙일 수 있다.
RubyLLM은 모델 레지스트리, 도구 호출, 사용량, 배치 테이블을 소유한다. 그 레코드들이 프레임워크의 작업을 서술하므로, 모든 애플리케이션이 지원 모델을 직접 유지하지 않아도 스키마를 발전시킬 수 있다는 것이 근거다.

백그라운드 잡은 기존 Active Job을 그대로 쓴다.

```ruby
class StudyAgent < RubyLLM::Agent
  chat_model Chat
  model "gpt-5.6-luna"
  instructions "Help organize practical Ruby study sessions."
end

class StudyReplyJob < ApplicationJob
  def perform(chat_id, question)
    StudyAgent.find(chat_id).ask(question)
  end
end

chat = StudyAgent.create!
StudyReplyJob.perform_later(chat.id, "Plan a session about Ruby blocks.")
```

## 오류 처리

제공자와 API 연산 오류는 `RubyLLM::Error`를 상속하고, 로컬 설정과 프로그래밍 오류는 `StandardError`를 직접 상속한다. 그래서 둘을 따로 구조해야 한다.

| 계열             | 주요 클래스                                                                                                    |
| ---------------- | -------------------------------------------------------------------------------------------------------------- |
| `RubyLLM::Error` | `BadRequestError`(400), `UnauthorizedError`(401), `PaymentRequiredError`(402), `ForbiddenError`(403)           |
|                  | `RateLimitError`(429), `ServerError`(500), `ServiceUnavailableError`(502·503·504), `OverloadedError`(529)      |
|                  | `ContextLengthExceededError`, `ToolCallParseError`, `UnsupportedAttachmentError`, `UnsupportedServerToolError` |
| `StandardError`  | `ConfigurationError`, `PromptNotFoundError`, `ModelNotFoundError`, `InvalidRoleError`                          |
|                  | `InvalidToolChoiceError`, `PendingToolCallsError`, `ModelRegistryError`, `CancelledError`                      |

`RubyLLM::Error`와 그 하위 클래스는 원래의 `Faraday::Response`를 `response` 속성으로 들고 있으므로, 제공자별 오류 코드를 꺼낼 수 있다.

```ruby
rescue RubyLLM::ForbiddenError => e
  puts e.response&.status
  if e.response&.body&.include?('invalid_organization')
    puts "API 키가 올바른 OpenAI 조직에 대해 활성화되어 있는지 확인"
  end
```

스트리밍 중 오류는 블록 실행이 끝나거나 오류로 중단된 **뒤에** `ask`가 올린다.
오류 앞에 도착한 청크에 대해서는 블록이 이미 실행되었고, `ask`는 최종 응답을 반환하지 않으므로 누적한 부분 내용을 직접 다뤄야 한다.

## 폴백과 자동 재시도

`with_fallbacks`는 일시적 제공자·네트워크 오류가 났을 때 다른 모델로 넘어간다.

```ruby
chat = RubyLLM.chat(model: "gpt-4.1")
              .with_fallbacks("gpt-4.1-mini", "claude-haiku-4-5")

# 기본 대상은 속도 제한, 서버 오류, 서비스 불가, 과부하, 타임아웃, 연결 실패다.
# 직접 고르려면 on:을 쓴다
chat.with_fallbacks("gpt-4.1-mini",
                    on: [RubyLLM::RateLimitError, RubyLLM::ServiceUnavailableError])

chat.before_fallback do |fallback|
  Rails.logger.info("#{fallback.from.id} → #{fallback.to.id}: #{fallback.error.class}")
end

chat.after_fallback do |fallback|
  # 스트리밍에서 이미 청크를 내보낸 뒤 폴백이 일어났는지 구분할 수 있다
  Rails.logger.warn("chunks already yielded") if fallback.chunks_yielded?
end
```

폴백은 순서대로 시도되고 그 생성 시도에만 적용되며, 끝나면 원래 모델로 돌아간다.
대화는 도구와 스키마와 설정을 유지하므로 **쓰는 기능을 지원하는 모델을 폴백으로 골라야 한다**. 양쪽 제공자의 자격 증명도 모두 설정해야 한다.

자동 재시도는 Faraday 재시도 미들웨어가 처리하며, 원시 HTTP 상태 코드가 아니라 예외 타입 분류로 작동한다.
대상은 네트워크 타임아웃, 연결 실패, 속도 제한, 서버 측 오류다. `ContextLengthExceededError`는 재시도하지 않는다.

제공자 쪽에 무언가를 생성하는 요청은 **절대 재시도하지 않는다**. 배치 제출, 영상 생성 잡, 파일 업로드, 콘텐츠 캐시가 그것이다.
요청이 제공자에 도달했는데 응답이 유실된 경우 재시도하면 돈을 내야 하는 두 번째 잡이 생기므로, 오류를 올리고 다시 제출할지를 사용자가 정하게 한다.

디버깅은 환경 변수로 켠다. 요청과 응답의 헤더와 본문이 보이고 API 키는 필터링된다.

```bash
export RUBYLLM_DEBUG=true
```

## 비용과 사용량

사용량 추적이 개별 제공자 시도 단위를 따라가며, 재시도와 폴백과 취소된 요청까지 포함한다.

```ruby
response = chat.ask "Explain Ruby fibers in one paragraph."

response.tokens.input
response.tokens.output
response.tokens.cache_read      # 캐싱을 켠 경우
response.cost.total
chat.cost.total
```

여러 번 시도한 답변은 그 시도들의 보고된 사용량을 포함한다.
알 수 없는 사용량이나 가격은 `nil`로 남으므로, 정보 없음이 공짜 요청처럼 보이지 않는다.

Rails에서는 사용량 원장이 시도를 메시지와 별도로 기록하고 완료 시점에 계산한 비용을 유지한다. 나중에 모델 가격을 갱신해도 그 이력은 다시 쓰이지 않는다.

이 설계가 1.x에서 지적받은 문제에 대한 답이다.
Finbarr는 두 번째 HN 스레드에서 계측의 한계를 짚었다. 재시도 시 기존 모델이 삭제되어 대화 이력은 깔끔해 보이지만 실제 API 호출 시퀀스를 추적하기 어렵다는 것이다.[^Finbarr]
저자는 Rails 스타일 계측이 1.16.0에 도입됐다고 답했고[^earcar-instrumentation], 2.0은 한 걸음 더 나아가 시도를 메시지와 분리된 원장에 남긴다.
그래서 이제 깔끔한 전사와 실제 호출 이력을 둘 다 볼 수 있다. 관측이 필요하다면 원장 테이블을 직접 조회하는 것이 정답이며, 메시지만 보면 여전히 재시도가 보이지 않는다.

보내기 전에 세어 볼 수도 있다.

```ruby
chat.count_tokens("What should I check in a renewal clause?")
RubyLLM.tokenize("Ruby makes AI useful.", model: "grok-4.3").count
```

## 값 정하기

| 값                    | 기본값      | 정하는 기준                                                 |
| --------------------- | ----------- | ----------------------------------------------------------- |
| `max_retries`         | 3           | 제공자 불안정이 잦으면 올린다. 다만 지연이 곱으로 늘어난다  |
| `retry_interval`      | 0.1초       | 속도 제한이 잦으면 올린다. 제공자가 주는 대기 시간과 맞춘다 |
| `temperature`         | 모델 기본값 | 도구 호출과 구조화 출력을 쓰면 낮게(0~0.3) 둔다             |
| `max_output_tokens`   | 모델 기본값 | 응답 길이 상한이자 비용 상한. 잘림이 잦으면 올린다          |
| `tool_options calls:` | 제한 없음   | `:one`으로 한 턴 한 호출로 묶으면 폭주를 막는다             |
| 폴백 모델             | 없음        | 쓰는 기능(도구·스키마·사고)을 모두 지원하는 모델만 고른다   |
| 캐싱 경계             | 없음        | 바뀌지 않는 접두부 끝에 `cache_until_here`를 둔다           |

측정할 것은 세 가지다.
`chat.cost.total`로 대화당 비용을, 폴백 콜백 로그로 어느 모델이 얼마나 자주 실패하는지를, 그리고 도구별 오류 반환 비율을 본다.
마지막 것이 특히 중요한데, 도구가 `:error`를 자주 돌려주면 모델이 그만큼 추가 턴을 쓰고 그것이 곧 비용이기 때문이다.

## 트레이드오프

### 추상화는 제공자 간 차이를 숨기지 못한다

통합 API의 근본적 긴장은 제공자 간 기능 격차에서 온다.
프롬프트 캐싱 방식, 도구 스키마 구조, 구조화된 출력 포맷은 Anthropic과 OpenAI 사이에서도 상당히 다르다.
단일 인터페이스로 매끄럽게 추상화하면 제공자 고유의 최적화 기법은 사실상 쓰기 어려워진다.

두 번째 HN 스레드에서 swe_dima가 구체적 사례를 들었다.[^swe_dima]
xAI는 completions API만 지원하는데 RubyLLM이 thought signature를 잘못 반환해 캐싱이 실제로 동작하지 않았다는 것이다.
캐싱은 비용과 응답 속도에 직결되므로, 추상화 레이어 안에서 제공자별 캐싱 힌트를 제대로 전달하기 어렵다면 쓸수록 비용 최적화 기회를 잃는 역설이 생긴다.
저자(earcar)는 Responses API가 2.0에서 구현된다고 답했고[^earcar-responses], 실제로 2.0이 프로토콜 분리와 공통 캐싱 API로 그 방향을 잡았다.
MitziMoto도 같은 스레드에서 Responses API 미지원을 큰 누락으로 꼽으면서, 다른 개발자가 만든 커넥터가 있지만 버그가 있고 본 gem만큼의 품질이 아니라고 적었다. 그리고 곧 네이티브 지원이 되었다는 것을 보고 확인해 보겠다고 덧붙였다.[^MitziMoto]

그래도 이 긴장이 사라지지는 않는다. 2.0의 제공자 커버리지 표가 그것을 인정하는 장치다.
공유 기능 40개와 별도 55행에 대해 제공자마다 내장·부분·원시 옵션·없음을 표시하고, 각 칸이 출처와 구현 메모로 연결된다.
즉 이 프레임워크는 격차를 없앴다고 주장하지 않고 격차를 문서화하는 쪽을 택했다.
실무적으로는 이것이 더 나은 답이며, 도입 전에 그 표에서 쓰려는 기능의 칸을 먼저 확인하는 것이 절차가 되어야 한다.

### 빠져나갈 구멍이 있지만 그 구멍의 모양이 다르다

ORM과 데이터베이스의 관계가 오래된 비유다.
ActiveRecord는 PostgreSQL과 MySQL을 추상화하지만 JSONB나 전문 검색을 쓰려면 결국 Raw SQL로 우회한다.

RubyLLM의 탈출구는 `with_provider_options`와 원시 옵션 통과다.
문제는 SQL과 달리 이쪽 탈출구가 표준화되지 않았다는 것이다. Raw SQL은 그 자체로 명세가 있지만, 제공자별 요청 옵션은 제공자 문서를 따로 읽어야 한다.
그래서 탈출구를 쓰는 순간 그 코드는 특정 제공자에 묶이고, 폴백 대상 모델에서 같은 옵션이 유효하다는 보장이 없다.

여기서 실천적 규칙이 나온다. 제공자 옵션을 쓰는 지점을 한곳에 모으고, 그 지점에는 폴백을 걸지 않는 것이다.
폴백이 필요한 경로와 제공자 고유 최적화가 필요한 경로를 같은 대화에 섞으면, 폴백이 일어날 때 옵션이 조용히 무시되거나 오류가 난다.

### Rails 통합이 주는 것과 고착시키는 것

`acts_as_chat`의 빠른 시작은 Rails 생태계에서 강력하다. 설치에서 동작하는 채팅 UI까지 몇 분이면 된다.

2.0은 소유권 경계를 나눠 이 문제를 일부 완화했다. 애플리케이션이 chat과 message를 소유하고 RubyLLM이 레지스트리와 도구 호출과 사용량과 배치를 소유한다.
그래서 프레임워크가 지원 테이블 스키마를 바꿔도 애플리케이션 모델을 건드리지 않는다.

그러나 대화 이력이 Active Record에 쌓인다는 사실은 그대로다.
수백만 건이 쌓이면 쿼리가 병목이 되고, 벡터 DB나 전용 저장소로 옮기려면 이 추상화를 걷어내야 한다.
두 번째 HN 스레드의 techscruggs는 이 통합의 숨은 이점을 짚었다.[^techscruggs]
모든 대화를 DB에 저장해 두면 나중에 그 이력을 코딩 에이전트에 넘겨 에이전트 지시문을 다듬을 수 있다는 것이다.
축적된 전사가 부채이면서 동시에 자산이라는 뜻이며, 어느 쪽이 될지는 그 이력을 읽는 절차를 만들어 두었는지에 달린다.

### 동시성 모델

첫 번째 HN 토론에서 가장 뜨거운 논점이 동시성이었다.
kyledrake는 응답에 항상 지연이 생기고 프로세스를 멈추지 않고 논블로킹 스레드에서 스트리밍하고 싶어 하는 사람이 많을 것이라고 지적했다.[^kyledrake]
bradgessler는 async gem과 async-http, Falcon 웹서버 등 Ruby 비동기 IO 생태계가 충분히 성숙해 있다고 반박했다.[^bradgessler]

RubyLLM은 파이버 기반 동시성을 제공한다고 밝히지만, 기존 Puma 기반 Rails 앱을 그대로 쓰는 팀에게 그 해법이 자동으로 적용되지는 않는다.
2.0이 제시하는 실질적 답은 다른 쪽에 있다. 배치 API와 `ask_later`/`step` 기반 잡 분할이다.
동시 요청을 웹 프로세스에서 버티는 대신 Active Job으로 밀어내고, 결과가 나중에 와도 되는 작업은 배치로 보내라는 것이다.
이 답이 Rails의 기존 관행과 맞아떨어진다는 점에서 프레임워크 선택으로는 일관적이지만, 실시간 스트리밍이 제품의 핵심인 경우에는 여전히 서버 선택 문제가 남는다.

## 함정

`desc`가 아니라 `description`이다. 1.x 시절 예제를 복사하면 여기서 걸린다.

구조화 출력 스키마는 `RubyLLM::Schema`가 아니라 `Schematist::Schema`다. Schematist는 RubyLLM과 함께 설치된다.

`max_tokens`가 `max_output_tokens`로 바뀌었다. 업그레이드할 때 가장 먼저 걸리는 이름 변경이다.

Rails에서 `Message`에 `validates :content, presence: true`를 걸면 안 된다.
스트리밍은 텍스트가 오기 전에 어시스턴트 레코드를 만들고, 도구 호출은 텍스트 없이도 유효한 응답이기 때문이다. 빈 내용을 허용해야 두 흐름이 모두 돈다.

지속형 에이전트에서 잡이 결과를 저장하기 전에 멈추면 연산이 다시 돌 수 있다. **도구는 멱등하거나 최소한 재시도를 견뎌야 한다.**

제공자 쪽에 무언가를 만드는 요청은 재시도되지 않는다. 배치 제출, 영상 생성, 파일 업로드, 캐시 생성에서 응답이 유실되면 직접 판단해 다시 보내야 한다.

폴백 모델이 원래 모델과 같은 기능을 지원하지 않으면 도구나 스키마가 있는 대화에서 실패한다. 폴백 목록은 기능 기준으로 골라야 한다.

스트리밍 중 폴백이 일어나면 이미 내보낸 청크를 되돌릴 수 없다. 새 어시스턴트 메시지 생명주기가 시작되므로 UI가 `chunks_yielded?`를 보고 그 경우를 구분해야 한다.

프롬프트 캐시는 적중이 보장되지 않는다. 최소 접두부 길이와 수명과 지원 모델을 제공자가 정한다.

런타임 `chat`에 의존하는 에이전트 값을 블록이 아닌 즉시 평가식으로 쓰면 클래스 로드 시점에 터진다.

## 확인하기

도입 전에 키 없이 확인할 수 있는 것부터 본다.

```ruby
# 쓰려는 모델이 레지스트리에 있고 어떤 능력과 가격을 갖는지
RubyLLM.models.find("claude-sonnet-5")
RubyLLM.models.all.select { |m| m.supports_tools? }
```

그다음 가장 싼 호출로 설정을 검증한다.

```ruby
chat = RubyLLM.chat
chat.count_tokens("ping")     # 토큰 계수는 생성 없이 인증과 연결을 확인한다
```

폴백이 실제로 도는지는 일부러 틀린 모델로 확인한다.

```ruby
chat = RubyLLM.chat(model: "gpt-4.1").with_fallbacks("gpt-4.1-mini")
chat.before_fallback { |f| puts "fallback: #{f.from.id} → #{f.to.id} (#{f.error.class})" }
```

도구 오류 처리는 두 경로를 모두 시험해야 한다.
`:error` Hash를 돌려주는 경로에서는 모델이 다시 시도하는지를, `raise`하는 경로에서는 예외가 애플리케이션까지 올라오는지를 확인한다. 이 둘을 섞어 두면 프로덕션에서 조용히 무한 재시도가 된다.

Rails에서는 스트리밍 자리 표시자 동작을 먼저 확인한다.
실패한 요청이 빈 자리 표시자를 지우는지, 그리고 `Message` 검증이 그 흐름을 막지 않는지를 보는 것이 가장 자주 나는 문제를 미리 잡는다.

문제가 생기면 `RUBYLLM_DEBUG=true`로 실제 나간 요청을 본다. 추상화 레이어를 쓸 때 가장 값진 도구가 이것이다.

## 체크리스트

- 2.0 기준 문서를 보고 있는가. 1.x 예제의 `desc`와 `RubyLLM::Schema`, `max_tokens`를 쓰고 있지 않은가
- 쓰려는 기능이 대상 제공자에서 내장인지 원시 옵션인지 제공자 커버리지 표에서 확인했는가
- 폴백 목록의 모든 모델이 쓰는 기능(도구·스키마·사고·캐싱)을 지원하는가
- 도구가 재시도를 견디는가. 지속형 에이전트를 쓴다면 멱등한가
- 도구 오류를 모델에 돌려줄 것과 애플리케이션으로 올릴 것으로 나눠 두었는가
- Rails `Message`에 내용 필수 검증을 걸지 않았는가
- 사용량과 비용을 `chat.cost.total`로 기록하고 있는가
- 제공자 고유 옵션을 쓰는 지점을 한곳에 모았고, 그 경로에 폴백을 걸지 않았는가
- 배치·영상·업로드처럼 재시도되지 않는 요청의 실패 처리를 정해 두었는가

## 비평

### 단일 관리자 의존과 기여 친화성

두 번째 HN 토론에서 제기된 우려 중 하나는 PR 리뷰 과정에서 드러난 관리자의 방어적 태도였다.
기여자가 냉랭한 반응을 받았다는 증언이 여럿 달렸고, 자원봉사자에게 거친 응대는 좋은 모습이 아니라는 지적도 있었다.

반면 rohitpaulk는 이슈 트래커 운영 방식을 긍정적으로 평가했다.[^rohitpaulk]
기능 요청을 선택하면 대안 탐색 여부와 라이브러리 내 위치의 당위성을 설명하도록 강제하는데, 이것이 스코프 확장을 막는 효과적인 장치라는 것이다.
관리자의 방어적 태도와 이슈 트래커의 엄격한 관리가 동전의 양면임을 시사한다.

qrush의 증언이 더 구체적이다.[^qrush]
6개월 넘게 써 왔고 API와 개발 경험은 좋지만 PR에서 관리자와 소통하는 데 거의 성공하지 못했으며, 상당수의 바이브 코딩된 PR이 머지되는 것을 봤고 그중에는 자기들이 제출한 PR을 다시 쓴 것도 있었다는 것이다.
그는 API 호환에 비슷한 휴리스틱을 가진 최소 gem이 잘될 것 같다고 덧붙였다.
반면 strzibny는 오랫동안 써 왔고 API 설계에 반했다며 SerpTrail 프로젝트를 실사용 예로 제시했고[^strzibny], rohitpaulk와 digitaltrees를 비롯한 여럿이 프로덕션 사용을 보고했다.
평가가 갈리는 축이 분명하다. 쓰는 경험은 대체로 좋고, 기여하는 경험은 대체로 나쁘다.

2.0의 내용이 이 평가를 다시 보게 만든다.
17개 제공자와 영상·음성·OCR·리랭킹·배치·서버 도구·호스팅 리서치까지 한 릴리스에 담은 것은 엄격한 스코프 관리의 결과로 보기 어렵다.
오히려 스코프가 크게 넓어졌고, 그만큼 한 사람이 유지해야 할 표면도 넓어졌다.
열린 이슈가 7개뿐이라는 사실은 관리가 빠르다는 신호일 수도, 이슈를 빨리 닫는다는 신호일 수도 있다. 도입을 검토한다면 닫힌 이슈의 처리 방식을 몇 개 읽어 보는 편이 낫다.

### 커버리지 표가 정직하면서 동시에 부담이다

제공자별 기능 지원을 표로 공개하고 각 칸에 출처를 붙인 것은 이 프로젝트가 한 가장 성숙한 결정이다.
통합 라이브러리가 대개 숨기는 것을 드러냈고, 내장·부분·원시 옵션·없음·범위 밖·미검증까지 상태를 여섯 가지로 나눴다.

그런데 이 표의 존재가 사용자에게 일을 넘긴다.
공유 기능 40개에 제공자 17개면 680칸이고, 별도 페이지의 55행까지 더하면 훨씬 커진다. 이 표를 읽지 않고는 어떤 조합이 되는지 알 수 없다는 뜻이다.

그리고 미검증 상태가 표에 있다는 것은 프로젝트 자신도 일부 조합을 확인하지 못했음을 뜻한다.
17개 제공자의 곱집합을 한 사람이 검증할 수 없다는 사실의 정직한 표시이지만, 도입하는 쪽에서는 그 칸에 해당하는 조합을 직접 시험해야 한다는 뜻이기도 하다.
프레임워크가 하나의 일관된 API를 약속하면서 그 일관성의 범위를 표로만 알려 준다면, 약속의 실제 단위는 API가 아니라 표의 한 칸이다.

### 공식 SDK와의 경쟁 구도가 2.0에서 바뀌었다

1.x 시절 이 프로젝트의 위치는 통합 레이어였고, 제공사들이 공식 Ruby SDK를 강화하면 부가가치가 줄어드는 자리였다.
2.0의 기능 목록이 그 구도를 바꾼다. 에이전트 클래스, 도구 승인, 지속형 에이전트, 워크플로 계측, 배치, Rails 지속성은 어느 공식 SDK도 제공하지 않는 것들이다.

즉 이제 경쟁 상대가 공식 SDK가 아니라 애플리케이션 프레임워크 계층이다.
그리고 그 계층에서 Ruby의 대안은 사실상 직접 만드는 것뿐이다. 이 프로젝트가 스스로를 프레임워크라고 부르기 시작한 것이 그 자리 이동을 반영한다.

대가는 결합도다. 클라이언트 라이브러리는 버리기 쉽지만 프레임워크는 그렇지 않다.
에이전트 클래스와 프롬프트 규약과 지속성 스키마를 채택하면 애플리케이션 구조가 그것에 맞춰지고, 나중에 떼어내는 비용이 1.x 시절의 교체 비용과 전혀 다른 크기가 된다.
그래서 도입 결정의 성격이 바뀌었다. 어떤 HTTP 클라이언트를 쓸지가 아니라, 이 팀이 만든 에이전트 모델을 받아들일지의 문제다.

### 이 프로젝트가 받은 호응은 성능이 아니라 문법에 대한 것이었다

두 HN 스레드의 정서를 읽으면 이 라이브러리가 왜 주목받았는지가 드러난다.
jatins는 DX가 열악한 라이브러리들에 비해 완전히 신선한 공기라고 표현했고[^jatins], 645점을 받은 첫 스레드에서 가장 많이 등장한 정서는 Ruby가 여전히 살아 있다는 확인이었다.
Reddit에서 아무도 Ruby를 안 쓴다는 조롱이 나왔지만 같은 날 HN 프런트페이지 1위를 차지한 사실이 그것을 반박했다는 언급도 있었다.[^Multiplayer]

이 호응의 성격을 정확히 아는 것이 도입 판단에 중요하다.
평가의 근거가 처리량이나 지연이 아니라 코드를 읽고 쓰는 경험이었다는 뜻이며, 그것은 실재하는 값이지만 벤치마크로 검증되는 종류가 아니다.

그리고 그 값이 지속되려면 API가 안정적이어야 한다.
2.0이 이름을 대거 정리하고 스키마 라이브러리를 Schematist로 바꾼 것은 옳은 정리였지만, 동시에 1.x 예제를 따라 쓰는 사람에게는 문법의 편안함이 깨지는 경험이다.
문법이 값의 원천인 프로젝트에서 이름 변경은 기능 변경보다 체감 비용이 크다. 업그레이드 가이드가 그만큼 중요해지는 이유다.

### 하나의 제공자만 쓸 때도 값이 있는가

aaronbrethorst가 도입 판단에 가장 직접 닿는 질문을 던졌다.[^aaronbrethorst]
Claude만 쓸 생각이고 Anthropic 생태계를 떠날 계획이 없는데 RubyLLM이 공식 Anthropic Ruby SDK 대비 이점을 주느냐는 것이다.
그는 이 선택이 Fog와 `aws-sdk-s3` 사이의 선택에 가까운지, Active Storage와 `aws-sdk-s3` 사이의 선택에 가까운지로 물었다.

이 비유가 정확하다. 그리고 2.0 기준으로는 후자에 가깝다.
Fog는 여러 클라우드를 감싸는 추상화이고 그것만이라면 단일 제공자 사용자에게 값이 없다.
Active Storage는 추상화이면서 동시에 Rails 애플리케이션에 붙는 영속성과 규약을 준다. 그래서 S3만 쓰더라도 쓸 이유가 있다.

RubyLLM 2.0이 주는 것도 그쪽이다.
에이전트 클래스와 프롬프트 규약, 도구 승인과 지속형 에이전트, `acts_as_chat` 영속성, Hotwire 스트리밍, 사용량 원장은 제공자 중립성과 무관하게 애플리케이션 계층의 값이다.
공식 SDK를 쓰면 그 계층을 직접 만들어야 하고, 그것이 이 선택의 실제 비교 대상이다.
반대로 스크립트 하나에서 Claude를 한 번 부르는 정도라면 공식 SDK가 더 얇고 낫다.

miki123211은 비 Ruby 사용자 관점에서 다른 근거를 보탰다.[^miki123211]
`chat.rb`가 자기가 본 에이전트형 도구 호출 루프 구현 중 가장 아름답다는 것이다.
TypeScript 쪽의 좋은 구현을 가리키는 사람들이 있지만 Ruby 판본이 훨씬 우아하고 간결하며 읽기 쉽다고 했고, API가 조금 못생겨지는 대가로 더 단순화할 수도 있겠지만 그래도 정말 좋다고 평했다.
루프 구현을 읽어 보는 것이 이 라이브러리를 평가하는 한 방법이라는 뜻이며, 소스가 작다는 것이 도입 위험을 낮추는 실질적 요인이기도 하다.

## 기억할 원칙

### 추상화 라이브러리의 값은 격차를 숨기는 데 있지 않고 드러내는 데 있다

이 프로젝트가 1.x에서 2.0으로 오며 배운 것이 커버리지 표에 드러난다.
제공자 간 차이를 매끄럽게 가리는 대신, 어느 조합이 내장이고 어느 조합이 원시 옵션이고 어느 조합이 없는지를 문서로 공개했다.

이 선택이 옳은 이유는 실패 시점 때문이다.
격차를 숨기면 사용자는 프로덕션에서 그 격차를 만나고, 그때는 이미 코드가 그 위에 쌓여 있다.
격차를 표로 주면 도입 전에 만나고, 그때는 아직 다른 선택지가 있다.

같은 원칙이 자기 코드의 추상화에도 적용된다.
여러 백엔드를 감싸는 인터페이스를 만들 때 지원 여부를 런타임 예외로만 알리면 그것은 숨긴 것이고, 어떤 백엔드가 무엇을 지원하는지를 표나 타입으로 노출하면 드러낸 것이다.
그리고 드러내는 쪽이 문서 부담을 지는 대신 디버깅 부담을 덜어 준다. 두 부담 중 어느 쪽이 싼지는 사용자 수가 정한다.

### 루프를 쪼갤 수 있게 만들면 신뢰성 설계가 애플리케이션으로 내려온다

2.0에서 가장 실무적으로 중요한 변화가 `ask` 한 덩어리를 `ask_later`, `generate`, `run_tools`, `step`, `complete?`로 쪼갠 것이다.

이 변화의 값은 기능이 아니라 배치 가능성이다.
한 턴을 한 잡으로 돌릴 수 있으면 타임아웃과 재시도와 관측이 전부 기존 잡 인프라의 문제가 되고, 그것들은 이미 잘 풀린 문제다.
반대로 루프가 한 호출 안에 갇혀 있으면 그 안의 실패는 라이브러리가 제공하는 만큼만 다룰 수 있다.

승인 대기가 이 설계의 시험대다. 사람의 결정을 기다리는 동안 프로세스를 붙잡고 있을 수는 없으므로, 대화를 멈추고 저장하고 나중에 다른 프로세스에서 이어 갈 수 있어야 한다.
그것이 가능해지자 곧바로 따라온 요구가 도구의 재시도 내성이다. 문서가 그것을 명시한 이유가 여기 있다.

일반화하면, 오래 걸리고 중간에 멈출 수 있는 작업을 설계할 때 물어야 할 것은 어떻게 빨리 끝낼지가 아니라 어디서 멈추고 무엇을 저장할지다.
멈출 지점을 API로 노출하면 나머지는 기존 인프라가 맡고, 노출하지 않으면 그 안의 모든 실패 모드를 라이브러리가 혼자 감당해야 한다.

---

[^jatins]: <https://news.ycombinator.com/item?id=43369540>

[^Multiplayer]: <https://news.ycombinator.com/item?id=43369914>

[^swe_dima]: <https://news.ycombinator.com/item?id=48661194>

[^earcar-responses]: <https://news.ycombinator.com/item?id=48661247>

[^kyledrake]: <https://news.ycombinator.com/item?id=43372532>

[^bradgessler]: <https://news.ycombinator.com/item?id=43373919>

[^Finbarr]: <https://news.ycombinator.com/item?id=48661655>

[^earcar-instrumentation]: <https://news.ycombinator.com/item?id=48661703>

[^rohitpaulk]: <https://news.ycombinator.com/item?id=48663149>

[^techscruggs]: <https://news.ycombinator.com/item?id=48666552>

[^MitziMoto]: <https://news.ycombinator.com/item?id=48663685>

[^aaronbrethorst]: <https://news.ycombinator.com/item?id=48664680>

[^miki123211]: <https://news.ycombinator.com/item?id=48675752>

[^qrush]: <https://news.ycombinator.com/item?id=48667705>

[^strzibny]: <https://news.ycombinator.com/item?id=48670045>
