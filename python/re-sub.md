# `re.sub`

<https://docs.python.org/3/library/re.html#re.sub>

`re.sub(pattern, repl, string, count=0, flags=0)`

## 기본

정규표현식을 이용해서 문자열을 바꿉니다.

```python
import re

re.sub('가', 'ga', '아버지가방에들어가신다')
# => '아버지ga방에들어ga신다'

re.sub('가방', 'bag', '아버지가방에들어가신다')
# => '아버지bag에들어가신다'

re.sub('가방', 'bag', '아버지가 방에 들어가신다')
# => '아버지가 방에 들어가신다'

re.sub('[아가다]', 'ㅏ', '아버지가 방에 들어가신다')
# => 'ㅏ버지ㅏ 방에 들어ㅏ신ㅏ'
```

## 응용

빈 문자열을 쓰면 특정 표현을 삭제하는데 쓸 수 있습니다.

```python
import re

re.sub('가방', '', '아버지가방에들어가신다')
# => '아버지에들어가신다'

re.sub('[가에다]', '', '아버지가방에들어가신다')
# => '아버지방들어신'
```

함수를 쓰면 특정 표현을 변형할 수 있습니다.

```python
import re

def square_bracket(matchobj):
    return '[' + matchobj.group(0) + ']'

re.sub('가방', square_bracket, '아버지가방에들어가신다')
# => '아버지[가방]에들어가신다'

re.sub('[가에다]', square_bracket, '아버지가방에들어가신다')
# => '아버지[가]방[에]들어[가]신[다]'
```

정규표현식을 잘 다룰 수 있다면 훨씬 많은 걸 해볼 수 있습니다.

## 연습 문제

Codewars의 “Vowel remover” 문제:
<https://www.codewars.com/kata/vowel-remover/train/python>

```python
assert shortcut('hello') == 'hll'
```

```python
import re

def shortcut(s):
    return re.sub('[aeiou]', '', s)
```
