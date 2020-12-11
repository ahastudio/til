# Jest를 이용한 간단한 TDD 예제

프로그래머스의 “[두 개 뽑아서 더하기](https://j.mp/3mKbFlI)” 문제를
TDD로 풀어봅니다.

## 프로젝트 세팅

일단 문제를 풀기 전에 프로젝트부터 세팅합니다.

```bash
npm init -y

npm i -D eslint jest @types/jest

npx eslint --init
# -> airbnb 스타일 사용.
```

`.eslintrc.js` 파일을 열어 `jest`를 사용한다고 표시하고
`rules` 항목을 채워줍니다.

```javascript
  env: {
    es2021: true,
    node: true,
    jest: true,
  },
```

```javascript
  'rules': {
    'indent': ['error', 2],
    'linebreak-style': ['error', 'unix'],
    'quotes': ['error', 'single'],
    'semi': ['error', 'always'],
    'no-trailing-spaces': 'error',
    'curly': 'error',
    'brace-style': 'error',
    'no-multi-spaces': 'error',
    'space-infix-ops': 'error',
    'space-unary-ops': 'error',
    'no-whitespace-before-property': 'error',
    'func-call-spacing': 'error',
    'space-before-blocks': 'error',
    'keyword-spacing': ['error', { 'before': true, 'after': true }],
    'comma-spacing': ['error', { 'before': false, 'after': true }],
    'comma-style': ['error', 'last'],
    'comma-dangle': ['error', 'always-multiline'],
    'space-in-parens': ['error', 'never'],
    'block-spacing': 'error',
    'array-bracket-spacing': ['error', 'never'],
    'object-curly-spacing': ['error', 'always'],
    'key-spacing': ['error', { 'mode': 'strict' }],
    'arrow-spacing': ['error', { 'before': true, 'after': true }],
  },
```

## 문제 이해하기

“두 개 뽑아서 더하기” 문제의 입력과 출력을 확인합니다.

- 입력: 숫자 목록
- 출력: 입력된 숫자 목록에서 두 개를 뽑아서 더한 값을 모아 중복을 제거하고
정렬한 숫자 목록

예시:

- 입력: `2, 1, 3, 4, 1`
- 처리 과정:
  - 경우의 수: `5C2 = 5P2 / 2! = (5 * 4) / (2 * 1) = 10`
  - 계산:
    1. 2 + 1 = 3
    1. 2 + 3 = 4
    1. 2 + 4 = 6
    1. 2 + 1 = 3
    1. 1 + 3 = 4
    1. 1 + 4 = 5
    1. 1 + 1 = 2
    1. 3 + 4 = 7
    1. 3 + 1 = 4
    1. 4 + 1 = 5
- 출력: `2, 3, 4, 5, 6, 7`

## 첫 테스트 코드 작성

테스트 코드를 수정할 때마다 테스트를 실행하도록 Jest를 실행합니다.

```bash
npx jest --watchAll
```

`numbers.test.js` 파일을 만들어서 실패하는 테스트 코드를 간단히 작성합니다.

```javascript
test('simple', () => {
  expect(1 + 1).toBe(1);
});
```

실패하는 걸 확인했으면 고쳐서 통과시킵니다.

```javascript
test('simple', () => {
  expect(1 + 1).toBe(2);
});
```

예제를 입력하면서 인터페이스(또는 시그니처)를 결정합니다.

```javascript
test('sample', () => {
  expect(solve([2, 1, 3, 4, 1])).toEqual([2, 3, 4, 5, 6, 7]);
});
```

`ReferenceError: solve is not defined` 에러를 해결합니다.

```javascript
function solve() {
  // TODO: ...
}

test('sample', () => {
  expect(solve([2, 1, 3, 4, 1])).toEqual([2, 3, 4, 5, 6, 7]);
});
```

구현이 빠져있으므로 기대 값과 실제 값이 다릅니다.

```txt
Expected: [2, 3, 4, 5, 6, 7]
Received: undefined
```

빠르게 통과시킵니다.

```javascript
function solve() {
  return [2, 3, 4, 5, 6, 7];
}

test('sample', () => {
  expect(solve([2, 1, 3, 4, 1])).toEqual([2, 3, 4, 5, 6, 7]);
});
```

## 중복 발견

코드에서 중복을 발견해 봅시다.
중복을 찾기 어려우니 의미가 드러나도록 조금만 고쳐봅니다.

```javascript
function solve() {
  return [1 + 1, 3, 4, 5, 6, 7];
}

test('sample', () => {
  expect(solve([2, 1, 3, 4, 1])).toEqual([2, 3, 4, 5, 6, 7]);
});
```

맨 앞의 `2`는 사실 `1 + 1`이었고,
입력 값 `numbers`와 중복이란 걸 확인할 수 있습니다.

```javascript
function solve(numbers) {
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}

test('sample', () => {
  expect(solve([2, 1, 3, 4, 1])).toEqual([2, 3, 4, 5, 6, 7]);
});
```

나머지 숫자들도 이런 식으로 찾을 수 있겠지만,
너무 많은 것 같아서 자신이 없습니다.
그래서 훨씬 간단한 경우를 만들어서 확인하겠습니다.

## 간단한 테스트 케이스

입력을 `[1, 2]`로, 출력을 `[3]`으로 기대해 봅시다.

```javascript
function solve(numbers) {
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}

test('simple', () => {
  expect(solve([1, 2])).toEqual([3]);
});

test('sample', () => {
  expect(solve([2, 1, 3, 4, 1])).toEqual([2, 3, 4, 5, 6, 7]);
});
```

테스트가 실패합니다.
저는 입력 값의 크기(`length`)를 이용해 빠르게 통과시키겠습니다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [3];
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}

test('simple', () => {
  expect(solve([1, 2])).toEqual([3]);
});

test('sample', () => {
  expect(solve([2, 1, 3, 4, 1])).toEqual([2, 3, 4, 5, 6, 7]);
});
```

여기서 다시 의미를 드러냅시다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [1 + 2];
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

테스트 통과를 확인하고, 다시 고칩니다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

## 조금 더 나아가기

자신감이 붙었으니 조금 더 어려운 걸 해봅시다.
`[1, 2, 3]`을 넣어 `[3, 4, 5]`가 나오게 합시다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}

test('simple', () => {
  expect(solve([1, 2])).toEqual([3]);
  expect(solve([1, 2, 3])).toEqual([3, 4, 5]);
});

test('sample', () => {
  expect(solve([2, 1, 3, 4, 1])).toEqual([2, 3, 4, 5, 6, 7]);
});
```

이번에도 `length`를 이용해 빠르게 통과시킵니다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  if (numbers.length === 3) {
    return [3, 4, 5];
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

의미를 드러냅시다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  if (numbers.length === 3) {
    return [1 + 2, 1 + 3, 2 + 3];
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

테스트가 통과하니 또 고칩니다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  if (numbers.length === 3) {
    return [
      numbers[0] + numbers[1],
      numbers[0] + numbers[2],
      numbers[1] + numbers[2],
    ];
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

## 조금 더 어려운 중복 찾기

여기서 중복을 찾아봅시다.

저는 `numbers[0] + numbers[1]`이
`solve([numbers[0], [numbers[1]])`과 똑같아 보입니다.
따라서 이 부분을 재귀로 바꿔보겠습니다.

(**주의!** 이 코드는 계속 새로운 배열을 만들기 때문에 매우 비효율적입니다.
이런 발상이 가능하다는 걸 보여드리는 게 목적이니,
안목을 넓히는 용도로만 활용하세요.)

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  if (numbers.length === 3) {
    return [
      ...solve(numbers.slice(0, 2)),
      numbers[0] + numbers[2],
      numbers[1] + numbers[2],
    ];
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

또 찾을 수 있을까요?

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  if (numbers.length === 3) {
    return [
      ...solve(numbers.slice(0, 2)),
      numbers[0] + numbers[2],
      ...solve(numbers.slice(1, 3)),
    ];
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

가운데 있는 건 좀 어렵지만 이렇게 바꿔보죠.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  if (numbers.length === 3) {
    return [
      ...solve(numbers.slice(0, 2)),
      ...solve([...numbers.slice(0, 1), ...numbers.slice(2)]),
      ...solve(numbers.slice(1, 3)),
    ];
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

전부 같은 패턴으로 정리합니다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  if (numbers.length === 3) {
    return [
      ...solve([...numbers.slice(0, 2), ...numbers.slice(3)]),
      ...solve([...numbers.slice(0, 1), ...numbers.slice(2)]),
      ...solve([...numbers.slice(0, 0), ...numbers.slice(1)]),
    ];
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

역순으로 써진 것 같으니 다시 써볼까요?

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  if (numbers.length === 3) {
    return [
      ...solve([...numbers.slice(0, 0), ...numbers.slice(1)]),
      ...solve([...numbers.slice(0, 1), ...numbers.slice(2)]),
      ...solve([...numbers.slice(0, 2), ...numbers.slice(3)]),
    ];
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

결과의 순서가 틀렸다고 합니다.
간단히 정렬합시다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  if (numbers.length === 3) {
    return [
      ...solve([...numbers.slice(0, 0), ...numbers.slice(1)]),
      ...solve([...numbers.slice(0, 1), ...numbers.slice(2)]),
      ...solve([...numbers.slice(0, 2), ...numbers.slice(3)]),
    ].sort((a, b) => a - b); // 그냥 sort()라고 쓰면 문자열 정렬이 되니 주의!
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

## 패턴 찾기

`0~2`로 반복되는 패턴이 보입니다. `map`으로 정리해 보죠.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  if (numbers.length === 3) {
    return [...Array(3)].map((_, i) => {
      return solve([...numbers.slice(0, i), ...numbers.slice(i + 1)]);
    }).reduce((a, e) => [...a, ...e]).sort((a, b) => a - b);
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

숫자 `3`이 계속 보이는데 이것도 정리해 봅시다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  if (numbers.length === 3) {
    return numbers.map((_, i) => {
      return solve([...numbers.slice(0, i), ...numbers.slice(i + 1)]);
    }).reduce((a, e) => [...a, ...e]).sort((a, b) => a - b);
  }
  return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

왠지 범용으로도 쓸 수 있을 것 같습니다.
그래서 과감히 모든 경우에 적용해 보겠습니다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  // 쉽게 되돌릴 수 있도록 주석으로 처리했습니다.
  // if (numbers.length === 3) {
    return numbers.map((_, i) => {
      return solve([...numbers.slice(0, i), ...numbers.slice(i + 1)]);
    }).reduce((a, e) => [...a, ...e]).sort((a, b) => a - b);
  // }
  // return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

실패합니다. 원인은 결과 값에 중복이 있기 때문입니다.
`filter`를 이용해 간단히 처리해 봅시다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  // 쉽게 되돌릴 수 있도록 주석으로 처리했습니다.
  // if (numbers.length === 3) {
    const values = numbers.map((_, i) => {
      return solve([...numbers.slice(0, i), ...numbers.slice(i + 1)]);
    }).reduce((a, e) => [...a, ...e]).sort((a, b) => a - b);
    return values.filter((x, i) => x !== values[i - 1]);
  // }
  // return [numbers[1] + numbers[4], 3, 4, 5, 6, 7];
}
```

완성입니다!

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  const values = numbers.map((_, i) => {
    return solve([...numbers.slice(0, i), ...numbers.slice(i + 1)]);
  }).reduce((a, e) => [...a, ...e]).sort((a, b) => a - b);
  return values.filter((x, i) => x !== values[i - 1]);
}

test('simple', () => {
  expect(solve([1, 2])).toEqual([3]);
  expect(solve([1, 2, 3])).toEqual([3, 4, 5]);
});

test('sample', () => {
  expect(solve([2, 1, 3, 4, 1])).toEqual([2, 3, 4, 5, 6, 7]);
});
```

## 리팩터링

지금 코드는 어떤가요? 마음에 드나요?

정렬과 중복 제거는 서로에게 의존하고 있기 때문에
하나의 함수로 분리하면 좋을 것 같습니다.

```javascript
function sortedUniq(xs) {
  const values = [...xs].sort((a, b) => a - b);
  return values.filter((x, i) => x !== values[i - 1]);
}

test('sortedUniq', () => {
  expect(sortedUniq([1, 2])).toEqual([1, 2]);
  expect(sortedUniq([1, 1, 2])).toEqual([1, 2]);
  expect(sortedUniq([1, 2, 1])).toEqual([1, 2]);
});
```

`sortedUniq`를 써봅시다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  return sortedUniq(numbers.map((_, i) => {
    return solve([...numbers.slice(0, i), ...numbers.slice(i + 1)]);
  }).reduce((a, e) => [...a, ...e]));
}
```

`slice`를 두번 쓰는 이유는 중간에 있는 값을 제거하기 위해서입니다.
`removeAt` 함수를 만들어 보죠.

```javascript
function removeAt(xs, index) {
  return [...xs.slice(0, index), ...xs.slice(index + 1)];
}

test('removeAt', () => {
  expect(removeAt([1, 2, 3], 0)).toEqual([2, 3]);
  expect(removeAt([1, 2, 3], 1)).toEqual([1, 3]);
  expect(removeAt([1, 2, 3], 2)).toEqual([1, 2]);
});
```

`removeAt`을 써봅시다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  return sortedUniq((
    numbers.map((_, i) => solve(removeAt(numbers, i)))
      .reduce((a, e) => [...a, ...e])
  ));
}
```

배열을 연결하는 부분은 의미가 좀 더 잘 드러나도록
`flatMap`을 이용해 처리해 봅시다.

```javascript
function solve(numbers) {
  if (numbers.length === 2) {
    return [numbers[0] + numbers[1]];
  }
  return sortedUniq((
    numbers.flatMap((_, i) => solve(removeAt(numbers, i)))
  ));
}
```

## 최종 코드

리팩터링의 재미에 빠지면 끝이 나지 않을 수 있습니다.
적당히 마무리하고 훨씬 효율적인 다른 풀이법을 생각해 보면 좋을 것 같습니다.

아래는 `sum` 함수 등을 도입해 약간 수정한 최종 코드입니다.

```javascript
function sum(xs) {
  return xs.reduce((a, b) => a + b);
}

function sortedUniq(xs) {
  const values = [...xs].sort((a, b) => a - b);
  return values.filter((x, i) => x !== values[i - 1]);
}

function removeAt(xs, index) {
  return [...xs.slice(0, index), ...xs.slice(index + 1)];
}

function solve(numbers) {
  return numbers.length === 2 ? [sum(numbers)]
    : sortedUniq(numbers.flatMap((_, i) => solve(removeAt(numbers, i))));
}

// TEST -----------------------------------------------------------------------

test('sum', () => {
  expect(sum([1, 2, 3, 4])).toBe(10);
});

test('sortedUniq', () => {
  expect(sortedUniq([1, 2])).toEqual([1, 2]);
  expect(sortedUniq([1, 1, 2])).toEqual([1, 2]);
  expect(sortedUniq([1, 2, 1])).toEqual([1, 2]);
});

test('removeAt', () => {
  expect(removeAt([1, 2, 3], 0)).toEqual([2, 3]);
  expect(removeAt([1, 2, 3], 1)).toEqual([1, 3]);
  expect(removeAt([1, 2, 3], 2)).toEqual([1, 2]);
});

test('simple', () => {
  expect(solve([1, 2])).toEqual([3]);
  expect(solve([1, 2, 3])).toEqual([3, 4, 5]);
});

test('sample', () => {
  expect(solve([2, 1, 3, 4, 1])).toEqual([2, 3, 4, 5, 6, 7]);
  expect(solve([5, 0, 2, 7])).toEqual([2, 5, 7, 9, 12]);
});
```

## BONUS

좀더 일반적인 풀이가 궁금하시면
[pytest 맛보기](https://www.youtube.com/watch?v=88qxXM3oI0w)
영상을 참고하세요.
TDD 등을 배울 때는 관련 자료를 글로 보는 것보다
코딩 과정을 눈으로 확인하는 게 훨씬 효과적입니다.
