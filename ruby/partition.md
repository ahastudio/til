# Partition

컬렉션을 둘로 분류할 때 `partition` 메서드를 사용하면 간단하다.

1~10 숫자를 짝수와 홀수로 분류한다면...

select 활용:

```ruby
a = (1..10).select(&:even?)
b = (1..10).select(&:odd?)
```

partition 활용:

```ruby
a, b = (1..10).partition(&:even?)
```

참고: http://ruby-doc.org/core-2.3.1/Enumerable.html#method-i-partition
