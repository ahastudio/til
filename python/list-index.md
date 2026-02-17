# `list.index`

<https://docs.python.org/3/library/stdtypes.html#common-sequence-operations>

<https://docs.python.org/3/tutorial/datastructures.html#more-on-lists>

`list.index(x[, start[, end]])`

## 기본

주어진 값이 `list`의 어디에 위치하는지 알아냅니다. 찾을 수 없으면 `ValueError`가
발생하므로 먼저 `in`을 이용해서 `list` 안에 있는지 확인하면 안전합니다.

```python
['빵', '우유', '달걀'].index('빵')
# => 0

['빵', '우유', '달걀'].index('우유')
# => 1

['빵', '우유', '달걀'].index('치즈')
# => ValueError: '치즈' is not in list
```

```python
'빵' in ['빵', '우유', '달걀']
# => True

'우유' in ['빵', '우유', '달걀']
# => True

'치즈' in ['빵', '우유', '달걀']
# => False
```

특정 범위 안에서 찾고 싶다면 `start`와 `end`를 쓸 수 있습니다. 늘 그렇듯이,
`end`는 포함되지 않습니다.

```python
['빵', '우유', '달걀'].index('빵')
# => 0

['빵', '우유', '달걀'].index('빵', 1)
# => ValueError: '빵' is not in list

['빵', '우유', '달걀'].index('우유', 1)
# => 1

['빵', '우유', '달걀'].index('우유', 2)
# => ValueError: '우유' is not in list

['빵', '우유', '달걀'].index('우유', 0, 2)
# => 1

['빵', '우유', '달걀'].index('우유', 0, 1)
# => ValueError: '우유' is not in list
```

## 응용

`list`의 특정 값을 바꾸는데 활용할 수도 있습니다.

```python
foods = ['빵', '우유', '달걀']

index = foods.index('달걀')

foods[index] = '치즈'

print(foods)
# => ['빵', '우유', '치즈']
```

`list` 외에도 `tuple`이나 `range` 같은 Sequence Type은 모두 `index`를 사용할 수
있습니다.

```python
(10, 20, 30).index(20)
# => 1

range(10, 20).index(15)
# => 5
```

## 연습 문제

Codewars의 “Greek Sort” 문제:
<https://www.codewars.com/kata/greek-sort/train/python>

```python
assert greek_comparator('alpha', 'beta') < 0
assert greek_comparator('psi', 'psi') == 0
assert greek_comparator('upsilon', 'rho') > 0
```

```python
greek_alphabets = [
    'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta',
    'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu',
    'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma',
    'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega'
]

def greek_comparator(lhs, rhs):
    return greek_alphabets.index(lhs) - greek_alphabets.index(rhs)
```
