# `str.split`

<https://docs.python.org/3/library/stdtypes.html#str.split>

`str.split(sep=None, maxsplit=-1)`

## 기본

하나의 문자열을 여러 문자열로 나눠줍니다.
나눈 결과는 문자열의 `list`가 됩니다.

그냥 사용하면 빈 칸을 기준으로 나눠줍니다.

```python
'아버지가 방에 들어가신다'.split()
# => ['아버지가', '방에', '들어가신다']
```

쉼표(`,`) 등 특정 문자열을 기준으로 나눌 수도 있습니다.

```python
'빵,우유,달걀'.split(',')
# => ['빵', '우유', '달걀']
```

나누는 횟수를 제한할 수도 있습니다.

```python
'1,2,3,4,5'.split(',', 2)
# => ['1', '2', '3,4,5']
```

## 응용

나눈 결과를 다시 합쳐주고 싶다면 `str.join`을 쓰면 됩니다.

```python
','.join('아버지가 방에 들어가신다'.split())
# => '아버지가,방에,들어가신다'
```

나눈 결과의 공백을 제거하고 싶다면 `str.strip`을 쓰면 됩니다.

```python
'1, 2, 3, 4, 5'.split(',')
# => ['1', ' 2', ' 3', ' 4', ' 5']

[x.strip() for x in '1, 2, 3, 4, 5'.split(',')]
# => ['1', '2', '3', '4', '5']

list(map(str.strip, '1, 2, 3, 4, 5'.split(',')))
# => ['1', '2', '3', '4', '5']
```

나눈 결과를 숫자로 바꾸는 것도 가능합니다.

```python
[int(x) for x in '1, 2, 3, 4, 5'.split(',')]
# => [1, 2, 3, 4, 5]

list(map(int, '1, 2, 3, 4, 5'.split(',')))
# => [1, 2, 3, 4, 5]
```

## 연습 문제

Codewars의 “Remove the time” 문제:
<https://www.codewars.com/kata/remove-the-time/train/python>

```python
assert shorten_to_date('Monday February 2, 8pm') == 'Monday February 2'
assert shorten_to_date('Tuesday May 29, 8pm') == 'Tuesday May 29'
assert shorten_to_date('Wed September 1, 3am') == 'Wed September 1'
assert shorten_to_date('Friday May 2, 9am') == 'Friday May 2'
assert shorten_to_date('Tuesday January 29, 10pm') == 'Tuesday January 29'
```

```python
def shorten_to_date(long_date):
    return long_date.split(',')[0]
```

## 더 보기

<https://github.com/ahastudio/til/blob/master/python/str-join.md>
