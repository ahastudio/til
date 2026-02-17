# let

JavaScript의 `var`는 function 단위로 scope이 잡힌다.

만약 블럭 단위로 scope을 잡아주고 싶다면, `let`을 사용한다(ES6).

`var`를 사용한 경우:

```javascript
var a = 3;
if (true) {
  var a = 2;
}
console.log(a);
// => 2 출력
```

`let`을 사용한 경우:

```javascript
var a = 3;
if (true) {
  let a = 2;
}
console.log(a);
// => 3 출력
```

`var` 대신 모두 `let`을 사용:

```javascript
let a = 3;
if (true) {
  let a = 2;
}
console.log(a);
// => 3 출력
```
