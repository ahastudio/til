# Modern PHP - Chapter 2. Features

## Namespaces
> 모던 PHP 기능 중 꼭 하나만 알아야 한다면 그것은 네임스페이스일 것이다.

[PHP 5.3.0](http://php.net/releases/5_3_0.php)에서 도입됨.

```php
<?php
namespace VendorName\Component\Foo;
```

역슬래시(\)를 사용한다는 건 비극적이다.

대규모 프로젝트를 진행하려면, 이름 충돌 문제를 해결하기 위해 네임스페이스는 필수.


```php
<?php
use VendorName\Component\Foo;
```

see also [PSR-4: Autoloader](http://www.php-fig.org/psr/psr-4/).

## Code to an Interface
객체지향 PHP의 주요 개념.

객체 자체가 아니라 기능에 의존하게 함. 어떻게 구현했는지 관심을 가질 필요가 없어진다.

```php
<?php
interface Documentable
{
    public function getId();
    public function getContent();
}
```

```php
<?php
class HtmlDocument implements Documentable
{
    protected $url;

    public function __construct($url)
    {
        $this->url = $url;
    }

    public function getId()
    {
        return $this->url;
    }

    public function getContent()
    {
        $ch = curl_init();
        curl_Setopt($ch, CURLOPT_URL, $this->url);
        // ...(중략)...
        $html = curl_exec($ch);
        curl_close($ch);
        return $html;
    }
}
```

## Traits
[PHP 5.4.0](http://php.net/releases/5_4_0.php)에서 도입됨.

고전적인 상속 모델을 해치지 않으면서 코드 재사용성을 높인다. [Ruby의 Mixin](http://ruby-doc.com/docs/ProgrammingRuby/html/tut_modules.html)과 같다.

```php
<?php
trait Geocodable
{
    protected $address;

    public function setAddress($address)
    {
        $this->address = $address;
    }
}
```

```php
<?php
class RetailStore
{
    use Geocodable;
}
```

```php
$store = new RetailStore();
$store->setAddress('Seoul, Korea');
```

## Generators
[PHP 5.5.0](http://php.net/releases/5_5_0.php)에서 도입됨.

> 제너레이터는 단순한 이터레이터다.

Lazy 계산을 통해 메모리 효율을 높이고 성능을 향상시킨다.

```php
<?php
function myGenerator()
{
    yield 'value1';
    yield 'value2';
}
```

```php
foreach (myGenerator() as $value)
{
    echo $value, PHP_EOL;
}
```

see also [ircmaxell’s blog: What Generators Can Do For You](http://blog.ircmaxell.com/2012/07/what-generators-can-do-for-you.html).

## Closures
[PHP 5.3.0](http://php.net/releases/5_3_0.php)에서 도입됨.

> 클로저는 생성 당시 자신의 주변 상태를 캡슐화한 함수다.
> 캡슐화된 상태는 클로저 내부에 존재하며 심지어 원래의 주변 환경이 소멸해도 클로저 안에 남는다.

> 클로저와 익명함수를 조사해보면 이들이 `Closure` 클래스의 인스턴스라는 것을 알게 될 것이다.
> PHP는 변수명 끝에 `()`가 나올 때마다 `__invoke()` 메서드를 찾고 호출한다.

```php
<?php
$hello = function ($name)
{
    return sprintf('Hello %s', $name);
}

echo $hello('Josh');
```

상태 등록을 위해 `bindTo()` 메서드나 `use` 키워드를 사용한다.

```php
<?php
function enclosePerson($name)
{
    return function ($doCommand) use ($name) {
        return sprintf('%s, %s', $name, $doCommand;
    };
}

$clay = enclosePerson('Clay');

echo $clay('let me out!');
```

```php
<?php
class App
{
    protected $callback = null;
    protected $body = '';

    public function bind($callback)
    {
        $callback->bindTo($this, __CLASS__);
    }

    public function run()
    {
        $callback();
        return $body;
    }
}

$app = new App();
$app->bind(function () {
    $this->body = 'Hello, world!';
});
echo $app->run();
```

## Zend OPcache
PHP 컴파일(설치)할 때 활성화해야 함.

## Built-in HTTP server
[PHP 5.4.0](http://php.net/releases/5_4_0.php)에서 도입됨.

참고: http://php.net/manual/kr/features.commandline.webserver.php

```
$ php -S localhost:4000
```

[http://localhost:4000/](http://localhost:4000/)

```
$ php -S localhost:4000 -c app/config/php.ini
```

```
$ php -S localhost:4000 router.php
```
