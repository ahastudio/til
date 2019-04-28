# Python 프로젝트 시작하기

- [아듀 2018!](https://adieu2018.ahastudio.com/)
- 이전 글: [C++에서 어셈블리 공부하기](http://j.mp/2Q7SPUw)
- 다음 글:

## 목표

Python을 설치하고, 프로젝트를 진행할 수 있는 가상 환경을 만들고,
코드 퀄리티를 일정 수준 이상으로 유지할 수 있도록 테스트와 검사기를 붙인다.

## pyenv 설치

파이썬 프로젝트는 버전에 민감하기 때문에 여러 프로젝트를 진행할 경우
여러 버전의 파이썬을 설치하고 싶을 때가 있다.
이때 `pyenv`를 사용하면 프로젝트마다 다른 버전의 파이썬을 사용할 수 있다.

### Mac 사용자

[Homebrew](https://brew.sh/)를 사용하면 간단히 설치할 수 있다.

```bash
brew update && brew install pyenv
```

최신 버전의 파이썬을 지원하지 않을 땐 `pyenv`를 업그레이드하면 된다.

```bash
brew update && brew upgrade pyenv
```

### Linux 사용자

[pyenv-installer](https://github.com/pyenv/pyenv-installer)로 설치한다.

```bash
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

Mac, Linux 사용자 모두 `.bash_profile` 등에 다음을 포함시킨다.

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

만약 컴퓨터에 익숙하지 않다면 그냥 다음과 같이 입력하면 된다.

```bash
echo '
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
' >> ~/.bash_profile

source ~/.bash_profile
```

최신 버전의 파이썬을 지원하지 않을 땐 `pyenv`를 업그레이드하면 된다.

```bash
pyenv update
```

## Python 설치

설치할 수 있는 버전을 확인한다.

```bash
pyenv install --list
```

Python 3.7 버전만 확인한다.

```bash
pyenv install --list | grep "^\s*3\.7"
```

`-`이 들어가지 않은 버전만 확인한다.
이렇게 하면 개발 중이 아닌 CPython만 확인할 수 있다.

```bash
pyenv install --list | grep -v -
```

가장 최신 버전을 설치한다.

```bash
pyenv install $(pyenv install --list | grep -v - | tail -1)
```

설치 중 문제가 발생하면 pyenv GitHub Wiki의
[Common build problems 문서](http://j.mp/2StRQjt)를 참고해 해결한다.

예를 들어, Mac 사용자는 다음과 같이 한다.

```bash
# Xcode Command Line Tools 설치
xcode-select --install

# 이미 설치된 상태라면
# “xcode-select: error: command line tools are already installed,
# use "Software Update" to install updates”라고 뜸.
# 그럴 땐 당황하지 말고 아래 명령을 이어서 입력한다.

# 의존성이 있는 패키지 설치
brew install readline xz zlib sqlite3

# zlib 설정
export LDFLAGS="${LDFLAGS} -L/usr/local/opt/zlib/lib"
export CPPFLAGS="${CPPFLAGS} -I/usr/local/opt/zlib/include"
export PKG_CONFIG_PATH="${PKG_CONFIG_PATH} /usr/local/opt/zlib/lib/pkgconfig"

# 위에 써놨던 거지만... 다시 설치 시도!
pyenv install $(pyenv install --list | grep -v - | tail -1)
```

방금 설치한 최신 버전을 기본으로 사용하게 한다.

```bash
pyenv global $(pyenv install --list | grep -v - | tail -1)
```

설치된 버전 목록을 확인한다.

```bash
pyenv versions
```

## pip 업그레이드

```bash
pip install --upgrade pip
```

## 가상 환경 만들기

먼저 [`virtualenv`](https://github.com/pypa/virtualenv)를 설치한다.

```bash
pip install virtualenv
```

프로젝트 폴더를 만들고, 파이썬 버전을 명시한다.
프로젝트 이름은 `my-project`라고 가정하고, 파이썬 3.7.2 버전을 사용하겠다.

```bash
mkdir my-project
cd my-project
pyenv local 3.7.2
```

해당 프로젝트에서 사용할 가상 환경을 `venv` 폴더에 만든다.

```bash
virtualenv venv
```

가상 환경에 진입한다.

```bash
source venv/bin/activate
```

앞에 `(venv)`가 붙는 걸 확인할 수 있다.
가상 환경에서 나오고 싶다면 `deactivate`를 입력하면 된다.

매번 `activate` 하는 게 귀찮다면
[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)를 사용하면 된다.
이렇게 하면 해당 프로젝트에 `venv` 폴더가 필요 없지만
`pyenv`의 버전으로 가상 환경이 추가된다는 점에 주의하자.

```bash
# 파이썬 3.7.2로 my-project-3.7.2 버전 생성
pyenv virtualenv 3.7.2 my-project-3.7.2

# 내가 만든 버전이 추가됐나 확인
pyenv versions

# 내가 만든 버전 사용
pyenv local my-project-3.7.2
```

`PyCharm` 등의 IDE에서 해당 프로젝트를 사용할 때는
올바른 버전 세팅이 오히려 귀찮을 수 있으니
그냥 평범하게 `virtualenv`를 쓰는 게 나을 수도 있다.

이제 가상 환경 안에서 독립적인 의존성 관리가 가능하다.

```bash
# 라이브러리 설치
pip install -U requests

# 설치된 라이브러리와 버전을 requirements.txt 파일에 기록
pip freeze > requirements.txt

# 의존성 확인
cat requirements.txt

# 설치된 라이브러리 모두 제거
pip freeze | xargs pip uninstall -y

# 라이브러리 설치
pip install -r requirements.txt
```

`pyenv-virtualenv`를 사용한다면 `README` 등에 어떻게 세팅하는지 꼭 써주자.

## pytest 설치

테스트 코드를 작성하고 실행할 수 있도록
[`pytest`](https://pytest.org/)를 설치한다.

```bash
pip install -U pytest
```

간단히 `hello_test.py`를 만들어 보자.

```python
def test_hello():
    assert hello('JOKER') == 'Hello, JOKER!'
```

`pytest`를 실행하면 해당 프로젝트의 `*_test.py` 파일 안에 있는
모든 `test_*` 테스트 함수를 확인하게 된다.

```bash
pytest
```

간단히 통과시키자.

```python
def hello(name):
    return 'Hello, {}!'.format(name)


def test_hello():
    assert hello('JOKER') == 'Hello, JOKER!'
```

파일이 수정될 때마다 자동으로 실행하게 하려면
[`pytest-watch`](https://github.com/joeyespo/pytest-watch)를 쓰면 된다.

```bash
pip install -U pytest-watch
```

실행할 때는 오히려 더 짧게 쓰면 된다.

```bash
ptw
```

## pylama 설치

올바르게 코딩하는 걸 도울 수 있도록 정적 분석기를 사용하자.
여기서는 [Pylava](https://github.com/pylava/pylava)를 이용해 검사한다.

```bash
pip install -U pylava
```

간단히 돌려보자.

```bash
pylava
```

`venv` 폴더가 있다면 그것도 포함해서 검사하기 때문에 지나치게 오래 걸린다.
`--skip` 플래그로 해당 폴더를 제외하자.

```bash
pylava --skip "venv/*"
```

[Pylint](https://github.com/pylava/pylava_pylint)도 함께 사용해 보자.
Pylava의 기본 Linter 목록은
[여기](https://github.com/pylava/pylava/blob/master/pylava/config.py)에서
확인할 수 있다.

```bash
# Pylint 설치
pip install -U pylava-pylint

# Linter 목록 바꿔서 실행
pylava --skip "venv/*" --linters "pycodestyle,pyflakes,mccabe,pylint"
```

매번 `linters` 플래그를 적어주는 게 불편하다면
`pylava.ini` 또는 `pytest.ini` 파일을 만들어서 다음 내용을 넣어준다.

```ini
[pylava]
skip = venv/*
linters = pycodestyle,pyflakes,mccabe,pylint
```

`docstring`이 빠졌고 빈 줄이 부족하다고 하니 모두 추가하자.

```python
"""Sample test code."""


def hello(name):
    """Return greeting message."""
    return 'Hello, {}!'.format(name)


def test_hello():
    """hello function test."""
    assert hello('JOKER') == 'Hello, JOKER!'
```

`pytest`와 `pylava`를 통합해 보자.

```bash
pytest --pylava
```

매번 `--pylava` 플래그를 입력하는 게 불편하면
`pytest.ini` 파일에 다음을 추가한다.

```ini
[pytest]
addopts = --pylava
```

이제 `python-watch` 하나만 실행하면 코드가 올바른지 계속 감시할 수 있다.

```bash
ptw
```

## Sample Code

[https://github.com/ahastudio/python-sample-project](http://j.mp/2AnoY5v)

---

- [아듀 2018!](https://adieu2018.ahastudio.com/)
- 이전 글: [C++에서 어셈블리 공부하기](http://j.mp/2Q7SPUw)
- 다음 글:
