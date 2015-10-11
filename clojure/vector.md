# Vector

Clojure는 List 외에 Vector를 지원한다.

Vector는 random access가 가능하기 때문에 slice가 간단하다.

```clojure
(subvec [1 2 3 4 5] 2 4)
; => [3 4]
```

```clojure
(take (- 4 2) (drop 2 [1 2 3 4 5]))
; => '(3 4)
```

List를 Vector로 바꿀 땐 `into` 등을 활용할 수 있다.

```clojure
(into [] (take (- 4 2) (drop 2 [1 2 3 4 5])))
; => [3 4]

(apply vector (take (- 4 2) (drop 2 [1 2 3 4 5])))
; => [3 4]
```
