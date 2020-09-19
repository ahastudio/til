# Immutable Array

흔히 하는 실수와 해결책은 Redux 문서의 [Immutable Update Patterns](https://j.mp/2RJD8Gp) 문서를 참고하세요.

## Push

```javascript
const a = [1, 2, 3];
const b = [...a, 4];
```

```javascript
function push(xs, x) {
  return [...xs, x];
}
```

## Shift

```javascript
const a = [1, 2, 3];
const [b, ...c] = a;
```

```javascript
function shift(xs) {
  const [head, ...tail] = xs;
  return [head, tail];
}
```

## Pop

```javascript
const a = [1, 2, 3];
const b = a[a.length - 1];
const c = a.slice(0, a.length - 1);
```

```javascript
function pop(xs) {
  return [
    xs[xs.length - 1],
    xs[slice(0, xs.length - 1),
  ];
}
```
