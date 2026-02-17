# `round`

<https://docs.python.org/3/library/functions.html#round>

`round(number[, ndigits])`

## 기본

우리가 알고 있는 반올림이 아니라, 좀더 공정한(?)
[Bankers' Rounding](https://en.wikipedia.org/wiki/Rounding#Round_half_to_even)에따라
반올림합니다. 중간값인 `0.5`를 `1`로 무조건 반올림하지 않고, `0`과 `1`로 번갈아
가면서 처리합니다. 즉, `x.5`의 반올림은 모두 짝수가 됩니다.

```python
round(0)
# => 0

round(0.2)
# => 0

round(0.8)
# => 1

round(1)
# => 1

round(0.5)
# => 0

round(1.5)
# => 2

round(2.5)
# => 2

round(3.5)
# => 4

round(4.5)
# => 4

round(5.5)
# => 6
```

소수점 이하에서 반올림을 하고 싶다면 자릿수를 추가하면 됩니다. 컴퓨터의
부동소수점 표기법은 오차가 있기 때문에, Bankers' Rounding을 기대하면 다른 결과가
나와 당황할 수 있습니다.

```python
round(0.0, 1)
# => 0.0

round(0.02, 1)
# => 0.0

round(0.08, 1)
# => 0.1

round(0.1, 1)
# => 0.1

round(0.05, 1)
# => 0.1

round(0.15, 1)
# => 0.1

round(0.25, 1)
# => 0.2

round(0.35, 1)
# => 0.3

round(0.45, 1)
# => 0.5

round(0.55, 1)
# => 0.6
```

만약 자릿수에 `0`을 넣으면 결과가 float 타입으로 고정됩니다. `//`와 `/`가 서로
다른 것과 비슷하죠.

```python
round(0.5, 0)
# => 0.0

round(1.5, 0)
# => 2.0

round(2.5, 0)
# => 2.0

round(3.5, 0)
# => 4.0

round(4.5, 0)
# => 4.0

round(5.5, 0)
# => 6.0
```

“1의 자리에서 반올림”, “10의 자리에서 반올림” 같이 하고 싶다면 소수점 자릿수를
음수로 입력하면 됩니다.

```python
round(0, -1)
# => 0

round(2, -1)
# => 0

round(8, -1)
# => 10

round(10, -1)
# => 10

round(5, -1)
# => 0

round(15, -1)
# => 20

round(25, -1)
# => 20

round(35, -1)
# => 40

round(45, -1)
# => 40

round(55, -1)
# => 60
```

## 응용

우리가 알고 있던 반올림을 하고 싶다면 그냥 `0.5`를 더해서 버림을 하면 됩니다.
버림을 하는 방법 중 하나는 그냥 `int`를 사용하는 거죠.

```python
def round_half_up(x):
    return int(x + 0.5)


round_half_up(0.2)
# => 0

round_half_up(0.8)
# => 1

round_half_up(0.5)
# => 1

round_half_up(1.5)
# => 2

round_half_up(2.5)
# => 3

round_half_up(3.5)
# => 4

round_half_up(4.5)
# => 5

round_half_up(5.5)
# => 6
```

## 연습 문제

Codewars의 “NBA full 48 minutes average” 문제:
<https://www.codewars.com/kata/nba-full-48-minutes-average/train/python>

어떤 선수가 한 경기에서 몇 득점을 했는지, 한 경기에서 몇 분을 뛰었는지 입력했을
때 48분을 모두 뛰면 몇 득점을 할지 추측해 봅시다.

```txt
ppg (points per game) : mpg (minutes per game) = ? : 48

? = ppg * 48 / mpg
```

```python
assert nba_extrap(12, 20) == 28.8
assert nba_extrap(10, 10) == 48.0
assert nba_extrap(5, 17) == 14.1
assert nba_extrap(0, 0) == 0
assert nba_extrap(30.8, 34.7) == 42.6  # Russell Westbrook 1/15/17
assert nba_extrap(22.9, 33.8) == 32.5  # Kemba Walker 1/15/17
```

```python
def nba_extrap(ppg, mpg):
    if mpg == 0:
        return 0
    return round(ppg * 48 / mpg, 1)
```

```python
def nba_extrap(ppg, mpg):
    return mpg and round(ppg * 48 / mpg, 1)
```

## 더 보기

- [How to Round Numbers in Python – Real Python](https://realpython.com/python-rounding/)
- [gimmesilver's blog : 하스켈의 반올림 계산법](http://agbird.egloos.com/4031301)
