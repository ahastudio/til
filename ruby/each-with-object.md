# Each with Object

keys를 이용해 Hash를 만든다면 기존엔 `reduce`를 사용했다.

```ruby
%i(boy girl).reduce({}) { |a, e| a[e] = params[e]; a }
```

블럭 안에 불필요한 표현이 들어가는데, `each_with_object`를 쓰면 깔끔하게 된다.

```ruby
%i(boy girl).each_with_object({}) { |i, a| a[i] = params[i] }
```

매개변수는 `each_with_index` 등과 동일하게 각 항목이 먼저 쓰인다. `reduce`와
다른 매개변수 순서에 주의할 것!

참고: http://ruby-doc.org/core-2.3.1/Enumerable.html#method-i-each_with_object
