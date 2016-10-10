# Head & Tail

List를 다룰 때 많이 쓰는 head와 tail을 Ruby로 따라하기.

## Head

그냥 첫 요소에 접근하거나 `first` 메서드를 쓰면 된다.

```ruby
list = [1, 2, 3, 4, 5]
head = list[0]
head = list.first
```

## Tail

`last` 메서드를 쓰면서 길이를 지정할 수 있다.

```ruby
list = [1, 2, 3, 4, 5]
tail = list.last(list.size - 1)
```

Array에 range를 활용해 첫 요소만 제외할 수 있다.

```ruby
list = [1, 2, 3, 4, 5]
tail = list[1..-1]
```

`drop` 메서드를 쓸 수 있다.

```ruby
list = [1, 2, 3, 4, 5]
tail = list.drop(1)
```

## Head & Tail

Destructure 활용. 이걸 쓰기 위해서 이 문서를 작성했다.

```ruby
list = [1, 2, 3, 4, 5]
head, *tail = list
```
