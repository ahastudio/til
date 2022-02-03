# `str.join`

<https://docs.python.org/3/library/stdtypes.html#str.join>

`str.join(iterable)`

## 기본

`list`등을 하나의 문자열로 합쳐줍니다.
`str.split`과 반대 방향으로 작동합니다.

맨 처음에 합쳐줄 때 사용할 문자열이 들어간다는 점에 주의해야 합니다.

조금 어색해 보이는 기본적인 사용법은 다음과 같습니다.

```python
''.join(['아버지', '가방에', '들어가신다'])
# => '아버지가방에들어가신다'
```

합쳐줄 때 사용할 문자열을 공백(` `)으로 지정해 봅시다.

```python
' '.join(['아버지', '가방에', '들어가신다'])
# => '아버지 가방에 들어가신다'
```

자주 쓰이는 건 쉼표(`,`)입니다.

```python
','.join(['빵', '우유', '달걀'])
# => '빵,우유,달걀'
```

더 자주 쓰이는 건 쉼표와 공백(`, `)이죠.

```python
', '.join(['빵', '우유', '달걀'])
# => '빵, 우유, 달걀'
```

## 응용

합쳐준 문자열을 다시 나눠주고 싶다면 `str.split`을 쓰면 됩니다.

```python
','.join(['아버지가', '방에', '들어가신다']).split(',')
# => ['아버지가', '방에', '들어가신다']
```

문자열도 `list`처럼 쓸 수있기 때문에 다음과 같은 마법(?)도 가능합니다.

```python
'.'.join('들립니까?')
# => '들.립.니.까.?'
```

## 연습 문제

Codewars의 “split() and its good friend join()” 문제:
<https://www.codewars.com/kata/training-js-number-18-methods-of-string-object-concat-split-and-its-good-friend-join/train/python>

```python
assert split_and_merge('My name is John',' ') == 'M y n a m e i s J o h n'
assert split_and_merge('My name is John','-') == 'M-y n-a-m-e i-s J-o-h-n'
assert split_and_merge('Hello World!','.') == 'H.e.l.l.o W.o.r.l.d.!'
assert split_and_merge('Hello World!',',') == 'H,e,l,l,o W,o,r,l,d,!'
```

```python
def split_and_merge(string, sp):
    # split!
    words = string.split()
    # Accumulator 초기화
    decorated_words = []
    # Accumulation
    for word in words:
        # 의미를 드러내는 임시 변수
        decorated_word = sp.join(word)
        # 단수형과 복수형이 서로 다르다는 점에 주의하세요.
        decorated_words.append(decorated_word)
    # join!
    merged_word = ' '.join(decorated_words)
    # 리턴을 잊지 마세요.
    return merged_word
```

```python
def split_and_merge(string, sp):
    words = []
    for word in string.split():
        words.append(sp.join(word))
    return ' '.join(words)
```

```python
def split_and_merge(string, sp):
    return ' '.join([sp.join(x) for x in string.split()])
```

```python
def split_and_merge(string, sp):
    return ' '.join(sp.join(x) for x in string.split())
```

## 더 보기

<https://github.com/ahastudio/til/blob/master/python/str-split.md>
