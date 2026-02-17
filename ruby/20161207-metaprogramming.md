- [2016년 한국 루비 커뮤니티 대림절 달력(Advent Calendar)](http://j.mp/1jL0Eir)
- 이전 글: 12월 6일, [Let’s RSpec](http://j.mp/2gvIbWD)

---

# Ruby Meta-programming

## 저자

[@ahastudio](http://j.mp/1ea27KW) - 코딩의 신[神]. Ruby on Rails로 여러 서비스를
오픈했고, 최근엔 Lean Startup과 Machine Learning을 공부하면서 가르치고 있습니다.

## 시작하며

Ruby의 강점 중 하나로 메타프로그래밍이 자주 언급됩니다. “Meta-”는 어떤
의미일까요? [Ruby EDSL](http://j.mp/2gbVefz)에서 살짝 맛본 메타프로그래밍을 좀더
알아봅시다.

## 준비물

- Ruby
- 흥미
- 용기
- 사랑과 우정 (필수는 아님)

## Meta-programming이 뭐야?

Meta란 접두어를 아시나요? 사람에 따라서 굉장히 익숙한 표현일 수도, 처음 접하는
표현일 수도 있을 거라고 생각합니다. HTML을 조금이라도 만져보신 분은 익숙하실
거라고 생각하는데요, 바로 `meta` 태그 때문이죠.

```html
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="description" content="Example page." />
    <meta name="keywords" content="HTML" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
  </head>
</html>
```

`meta` 태그를 이용해서 표현하는 정보를 우리는 “메타데이터(metadata)”라고 합니다.
이 HTML 문서에 대한 정보죠. “Meta-X”는 흔히 “X에 대한 X” 정도로 옮깁니다.
메타데이터는 “데이터에 대한 데이터”란 의미가 되겠죠?

그렇다면 메타프로그래밍은 뭘까요? “프로그래밍에 대한 프로그래밍”이 됩니다. 좀더
이해하기 쉽게 옮긴다면, “프로그램을 만드는 프로그램”이라고 이해하시면 될 것
같아요.

간단한 예를 하나 볼까요?

```ruby
class Human
  attr_accessor :name
end
```

`attr_accessor`는 뭘까요? [Ruby EDSL](http://j.mp/2gbVefz)을 보신 분은
짐작하시겠지만, 이건 그냥 클래스 메서드입니다. 바로 `name=`(setter)과
`name`(getter)을 만들어주는 녀석이죠. 만들어준다? 네, 우리가 따로 코드를
작성하지 않아도 간절히 원하면 우주가 나서서 도와준다는 의미죠.

```ruby
human = Human.new
human.methods.include?(:name=)
human.methods.include?(:name)
```

## 클래스를 정의한다는 것

루비에서 클래스를 정의한다는 건 뭘까요? [Ruby EDSL](http://j.mp/2gbVefz)에서 한
구절 가져오겠습니다.

> Ruby의 클래스 정의는 매우 독특해서 그냥 정적 문서처럼 있는 게 아니라 하나씩
> 실행이 되는 코드입니다.

우리가 `class - end` 안에 코드를 적는 건 나중으로 미뤄둔 무언가가 아니라
즉각적으로 실행되는 코드입니다. 다음과 같은 황당한 코드가 결과를 냅니다.

```ruby
class App
  a = 1
  b = 2
  puts a + b
end
```

이쯤 되면 `def`란 메서드가 있는 게 아닌가 의심스러울 정도입니다. 물론, 아니죠.
하지만 유사한 녀석은 있습니다.

```ruby
class Human
  define_method :name, -> { 'RUBY' }
end

Human.new.name
```

좀더 익숙한 모양으로 바꿔볼게요.

```ruby
class Human
  define_method :name do
    'RUBY'
  end
end

Human.new.name
```

하는 김에 이름도 바꿀 수 있게 해볼까요?

```ruby
class Human
  define_method :name= do |name|
    @name = name
  end

  define_method :name do
    @name
  end
end

a = Human.new
a.name = 'A'

b = Human.new
b.name = 'B'

a.name
b.name
```

## `attr_accessor`

이제 `attr_accessor`를 직접 만들어 보죠.

```ruby
class Object
  def self.my_attr_accessor(name)
    define_method "#{name}=" do |value|
      instance_variable_set("@#{name}", value)
    end

    define_method name do
      instance_variable_get("@#{name}")
    end
  end
end

class Human
  my_attr_accessor :name
end

a = Human.new
a.name = 'A'

b = Human.new
b.name = 'B'

a.name
b.name
```

`instance_variable_set`과 `instance_variable_get`이라는 흑마법을 살짝 사용했지만
어렵지 않은 예제라고 생각합니다.

## 범용으로 놀아보기

메서드를 만드는 것 말고, 좀더 범용으로 놀아보죠.
[Ruby EDSL](http://j.mp/2gbVefz)에서 써먹은 `eval`을 여기서도 써봅시다.

```ruby
class Object
  def self.my_attr_accessor(name)
    class_eval %(
      def #{name}=(value)
        @#{name} = value
      end

      def #{name}
        @#{name}
      end
    )
  end
end

class Human
  my_attr_accessor :name
end

a = Human.new
a.name = 'A'

b = Human.new
b.name = 'B'

a.name
b.name
```

인스턴스가 아니라 클래스에 적용돼야 하기 때문에 `instance_eval` 대신
`class_eval`을 사용했습니다. 만약 `class_eval` 대신 `instance_eval`을 쓴다면
클래스 객체 자체가 setter/getter를 갖게 됩니다.

```ruby
class Object
  def self.my_attr_accessor(name)
    # 착한 아이는 따라하지 마세요!
    instance_eval %(
      def #{name}=(value)
        @#{name} = value
      end

      def #{name}
        @#{name}
      end
    )
  end
end

class Human
  my_attr_accessor :name
end

Human.name = 'WTF?!'
Human.name
```

클래스 메서드를 만드는 게 목적이라면 뭘 써야 할지 아시겠죠?

## ORM 만들기

이게 메타프로그래밍의 전부라고 하면 정말 재미없겠죠? 이제 알아서 반응하는 녀석을
만들어 봅시다. 환경에 알아서 반응하는 객체를 만든다는 건 프로그램이 변화함에
따라 함께 진화하는 걸 의미하니 얼마나 편하겠어요?

여기서는 [Sequel](http://j.mp/2ivgqzb)를 이용해 간단한 ORM을 만들어
보겠습니다(사실 Sequel엔 ORM이 내장돼있...). Sequel에 있는 예제 코드를 하나
들고오죠.

```ruby
require 'sequel'

DB = Sequel.sqlite

DB.create_table :my_items do
  primary_key :id
  String :name
  Float :price
end

DB[:my_items].columns
```

일단 setter/getter부터 만들죠.

```ruby
require 'active_support/all'

class Model
  def initialize
    collection.columns.each do |column|
      define_attribute(column)
    end
  end

  def collection
    DB[self.class.name.underscore.pluralize.to_sym]
  end

  def attributes
    @attributes ||= {}
  end

  private

  def define_attribute(name)
    return if name.to_s.include?('\'') # 지옥을 만드는 법을 알고 있나요?
    class_eval %(
      def #{name}=(value)
        attributes['#{name}'] = value
      end

      def #{name}
        attributes['#{name}']
      end
    )
  end
end

class MyItem < Model
end

item = MyItem.new
item.name = 'Product'
item.price = 10_000
puts item.name, item.price
```

이제 저장하고 불러오는 건 일도 아니겠죠?

```ruby
class Model
  # ...

  # collection을 조금 손봤습니다.

  def self.collection
    DB[name.underscore.pluralize.to_sym]
  end

  def collection
    self.class.collection
  end

  # ...

  def save
    if id.nil?
      self.id = collection.insert(attributes)
    else
      collection.where(id: id).update(attributes)
    end
  end

  def self.find(id)
    attributes = collection.where(id: id).first
    return if attributes.nil?
    attributes.each_with_object(new) do |(k, v), model|
      model.send("#{k}=", v)
    end
  end

  # ...
end

class MyItem < Model
end

item = MyItem.new
item.name = 'Product'
item.price = 10_000
item.save
puts item.id, item.name, item.price

item = MyItem.find(item.id)
item.price = 20_000
item.save
puts item.id, item.name, item.price

item = MyItem.find(-1)
puts item.nil?
```

정말 간단하죠?

소스 코드:
[https://github.com/ahastudio/CodingLife/tree/master/20170102/ruby](http://j.mp/2ivzjST)

## 정리하며

메타프로그래밍이란 무엇이고, 어떻게 하는지, 어디에 활용할 수 있는 간단히
알아봤습니다. 메타프로그래밍을 잘 활용하면 반복되는 코드를 줄일 수 있고,
프로그램이 성장함에 따라 알아서 반응하는 것도 가능합니다. 무한한 가능성이
열렸으니 여러분의 두뇌를 자극하고 재밌는 아이디어를 많이 내시면 됩니다.

더 재밌는 사례를 알고 계신다면, ahastudio 앳 지메일닷컴으로 메일을 보내주세요.
피드백과 질문도 환영합니다.

---

- [2016년 한국 루비 커뮤니티 대림절 달력(Advent Calendar)](http://j.mp/1jL0Eir)
- 이전 글: 12월 6일, [Let’s RSpec](http://j.mp/2gvIbWD)
