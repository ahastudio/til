# Clear namespace

```clojure
(ns test)
(remove-ns 'test)
(ns test)
```

http://stackoverflow.com/questions/3636364/can-i-clean-the-repl

```clojure
(map #(ns-unmap *ns* %) (keys (ns-interns *ns*)))
```
