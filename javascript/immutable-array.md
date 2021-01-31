# Immutable Array

흔히 하는 실수와 해결책은 Redux 문서의 [Immutable Update Patterns](https://j.mp/2RJD8Gp) 문서를 참고하세요.

## Push

```javascript
const a = [1, 2, 3];
const b = [...a, 4];
```

```javascript
function push(xs, value) {
  return [...xs, value];
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

## Remove (by value)

```javascript
const a = [1, 2, 3];
const b = a.filter(i => i !== 2);
```

```javascript
function remove(xs, value) {
  return xs.filter(x => x !== value);
}
```

## Remove (by index)

```javascript
const a = [1, 2, 3];
const b = a.filter((_, i) => i !== 1);
```

```javascript
function removeAt(xs, index) {
  return xs.filter((_, i) => i !== index);
}
```

또는

```javascript
const a = [1, 2, 3];
const b = [...a.slice(0, 1), ...a.slice(1 + 1)];
```

```javascript
function removeAt(xs, index) {
  return [...a.slice(0, index), ...a.slice(index + 1)];
}
```

죽어도 `splice`를 쓰고 싶다면...

```javascript
const a = [1, 2, 3];
const b = [...a];
b.splice(1, 1);
```

```javascript
function removeAt(xs, index) {
  const clone = [...xs];
  clone.splice(index, 1);
  return clone;
}
```
