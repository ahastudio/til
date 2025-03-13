# Python 프로젝트 시작하기

## mise-en-place 설치

<https://github.com/jdx/mise>

### Mac 사용자

<https://mise.jdx.dev/installing-mise.html#homebrew>

```bash
brew update && brew install mise
```

### Linux 사용자

<https://mise.jdx.dev/installing-mise.html#https-mise-run>

```bash
curl https://mise.run | sh
```

### Mac 사용자, Linux 사용자 공통

홈 디렉터리의 `.bash_profile`(또는 `.zprofile`) 파일에 다음을 추가합니다.

```bash
eval "$(mise activate zsh)"
```

## Python 설치

```bash
mise install python@3.13

mise use -g python@3.13

mise ls python
```

## uv 설치

<https://github.com/astral-sh/uv>

<https://mise.jdx.dev/lang/python.html#mise-uv>

```bash
mise install uv@latest

mise use uv@latest
```

## 프로젝트 만들기

uv로 격리된 가상 환경을 사용하는 프로젝트와 기본 코드를 만들어 줍니다.

```bash
uv init my-project

cd my-project
```

기본 코드를 실행해 봅니다.

```bash
uv run main.py
```

## pytest 설치

<https://github.com/pytest-dev/pytest>

```bash
uv add --dev pytest
```

```bash
uv run pytest
```

## pytest-watcher 설치

<https://github.com/olzhasar/pytest-watcher>

```bash
uv add --dev pytest-watcher
```

```bash
uv run ptw . --now --clear
```

## Ruff 설치

<https://github.com/astral-sh/ruff>

```bash
uv add --dev ruff
```

```bash
uv run ruff check
```
