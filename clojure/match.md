# Why?

Scala는 `match` 같은 걸 쓰면 `if`를 쓰지 않고 `Seq` 재귀를 매끄럽게 돌 수 있다.

Clojure에서도 비슷한 걸 하려고 함.

# Solve it!

http://www.sicpdistilled.com/section/1.1.4/

```clojure
(defn spread
  ([x] x)
  ([x y] (- (max x y) (min x y)))
  ([x y z] (- (max x y z) (min x y z))))
```

```clojure
(defn spread [& nums]
  (- (apply max nums) (apply min nums)))
```

http://clojure.org/functional_programming

> Clojure supports arity overloading in a single function object,
> self-reference, and variable-arity functions using `&`

http://github.com/ahastudio/CodingLife/blob/master/20151009/test.clj

```clojure
(defn product
  ([a] a)
  ([a b] (reduce #(concat %1 (map (partial vector %2) b)) [] a))
  ([a b & seq]
   (let [p (apply product (cons b seq))]
     (reduce #(concat %1 (map (partial cons %2) p)) [] a))))
```
