# Chunk

같은 결과를 내는 요소끼리 모아서 나눠야 할 때가 있는데, `chunk`를 쓰면 깔끔하다.

예를 들어 이어지는 문자 중 가장 긴 걸 찾으려면...

```ruby
'aabbbbcdddaacdd'.split('').chunk(&:itself).max_by { |i| i.last.size }.first
```

단순히 많은 문자를 찾는 건 다음과 같다.

```ruby
'aabbbbcdddaacdd'.split('').group_by(&:itself).max_by { |k, v| v.size }.first
```

참고: http://ruby-doc.org/core-2.3.1/Enumerable.html#method-i-chunk
