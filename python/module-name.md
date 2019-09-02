# `__name__`

<https://docs.python.org/3/reference/import.html#__name__>

`__name__`는 현재 모듈의 이름입니다.
앞 뒤로 `__`를 붙인 건 파이썬이 이 이름을 미리 선점한 건데요,
우리가 실수로 같은 이름을 써서 겹치는 일을 막으려는 거죠.
(우리가 뭔가를 만들 때 `__`를 앞뒤로 붙이면 안 되겠죠?)

`main.py`에서 `scores.py`를 import 하면
`scores.py`에서 `__name__`은 `scores`가 됩니다.
커다란 프로젝트에선 이 이름을 이용하면 흥미로운 작업을 할 수 있습니다.

## `__main__`

<https://docs.python.org/3/library/__main__.html>

문제는 아무도 import하지 않고 직접 실행했을 때입니다.
그때는 그냥 `main`이라고 알려주면 좋겠죠.
하지만 그냥 `main`이라고 하면 모듈 이름이 `main`인 경우와 구분이 어렵습니다.
따라서 앞뒤에 `__`를 붙여서 `__main__`이라고 합니다.

파이썬 파일은 그 자체로 모듈이기 때문에
이게 진짜로 실행용으로 만든 건지,
아니면 남들이 import해서 쓰라고 만든 건지 구분이 어렵습니다.
그때 `__name__ == '__main__'` 같은 코드는 한 줄기 빛이 되죠.
이게 써있는 건 실행용 파일이라고 보셔도 됩니다.

우리가 실행할 프로그램은 `main` 함수에 넣어놓는 경우가 많아서,
정말 많이 쓰는 표현은 다음과 같습니다:

```python
if __name__ == '__main__':
    main()
```

## 더 보기

- <https://docs.python.org/3/tutorial/modules.html>
