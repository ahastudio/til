# Ruby Programming Language

<https://www.ruby-lang.org/>

<https://github.com/ruby/ruby>

## Pure Object Oriented Programming Language

<https://www.ruby-lang.org/ko/about/>

> 나는 Perl보다 강력하고 Python보다는 객체지향적인 스크립트 언어가 필요했다.

<https://www.oreilly.com/library/view/the-ruby-programming/9780596516178/ch03s08.html>

> Ruby is a very pure object-oriented language:
> all values are objects, and there is no distinction between primitive types
> and object types as there are in many other languages.
> In Ruby, all objects inherit from a class named Object and share the methods
> defined by that class.

### Primitive Type과 Object Type의 구분이 없음

```ruby
(1).class
# => Integer

class Integer
  def double
    self * 2
  end
end

(3).double
# => 6
```

### 따라서 연산자가 없고 모두 메서드

```ruby
(1).+(2)
# => 3

(1).send(:+, 2)
# => 3
```

Scala의 경우:
<https://www.slideshare.net/slideshow/2013-06-22-scala/90210611#28>

### Null, True, False도 모두 객체

```ruby
class NilClass
  def greeting
    'Nope'
  end
end

class TrueClass
  def greeting
    'TRUE'
  end
end

class FalseClass
  def greeting
    'WTF?'
  end
end

nil.greeting
# => "Nope"

(puts 'Hello, world!').greeting
# => "Nope"

(1 + 1 == 2).greeting
# => "TRUE"

(1 == 2).greeting
# => "WTF?"
```

### Class도 객체

```ruby
Integer.class
# => Class

class Class
  def greeting
    'Hello, world!'
  end
end

(1).class.greeting
```

### 객체만 있는 세계 실습

<https://youtu.be/Kcy4XP3neE8>

## Rubrowser (Ruby Browser)

<https://github.com/emad-elsaid/rubrowser>
