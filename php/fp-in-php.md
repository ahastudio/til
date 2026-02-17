# Functional Programming in PHP

- 동영상:
  [PHP Hampshire Feb 2014: Functional PHP - YouTube](https://www.youtube.com/watch?v=4t5EKEZz724)
- 슬라이드:
  [Functional Programming in PHP // Speaker Deck](https://speakerdeck.com/treffynnon/functional-programming-in-php)

2014년 2월 자료인데 최근에 봤습니다(이 글을 쓴 건 2015년 9월). 기본적인 내용을
잘 정리한 것 같습니다.

초반에 나오는 예제 하나만 보죠.

1부터 10까지 합을 구하는 일반적인 코드:

```php
<?php
$sum = 0;
for ($i = 1; $i <= 10; $i++) {
  $sum += $i;
}
```

함수형 프로그래밍:

```php
<?php
array_sum(range(1, 10));
```

처음 보는 방식이라 어렵게 느껴질 수도 있겠지만, 일단 한번 익숙해지면 “1부터
10까지 합을 구한다”란 것 자체를 전달하기엔 후자가 더 명확합니다.

약간 응용해서, 2~20까지 짝수만 더한다면...

일반적인 코드:

```php
<?php
$sum = 0;
for ($i = 1; $i <= 10; $i++) {
  $sum += $i * 2;
}
```

함수형 프로그래밍:

```php
<?php
array_sum(array_map(function($i) { return $i * 2; }, range(1, 10)));
```

조건문을 써서 짝수의 합을 제대로 구한다면...

일반적인 코드:

```php
<?php
$sum = 0;
for ($i = 1; $i <= 20; $i++) {
  if ($i % 2 == 0) {
    $sum += $i;
  }
}
```

함수형 프로그래밍:

```php
<?php
array_sum(array_filter(range(1, 20), function($i) { return $i % 2 == 0; }));
```

map과 reduce를 잘 쓰면 단순하게 해결할 수 있는 문제가 많아집니다. map은 위에서
봤으니 reduce 예제 하나만 보고 가죠.

[피보나치 수](https://ko.wikipedia.org/wiki/%ED%94%BC%EB%B3%B4%EB%82%98%EC%B9%98_%EC%88%98)(1,
1, 2, 3, 5, 8, 13, 21, ...):

```php
<?php
function fib($n) {
  return array_reduce(range(1, $n), function($a, $e) {
    return array($a[1], $a[0] + $a[1]);
  }, array(0, 1))[0];
}
```

P.S. 한국어로 된 짧은 자료라면 “PHP: The Right Way”의 일부가 있긴 합니다.

- [PHP에서의 함수형 프로그래밍](http://modernpug.github.io/php-the-right-way/pages/Functional-Programming.html)
