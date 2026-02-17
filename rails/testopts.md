# TESTOPTS

테스트를 실행할 때 적용할 옵션을 추가하고 싶으면 `TESTOPTS`를 사용하면 된다. CI
등에서 자세한 로그를 남기고 싶을 때 유용하다.

```
$ bundle exec rails test:db TESTOPTS="-v"

Run options: -v --seed 12345

# Running:

MyTest#test_it = 0.06 s = .

Finished in 1.234s, 12.34 runs/s, 123.4 assertions/s.

12 runs, 123 assertions, 0 failures, 0 errors, 0 skips
```
