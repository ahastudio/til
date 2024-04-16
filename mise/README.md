# mise-en-place

> The front-end to your dev env

<https://mise.jdx.dev/>

<https://github.com/jdx/mise>

## Mac에서 설치

<https://formulae.brew.sh/formula/mise>

```bash
brew install mise

eval "$(mise activate zsh)"

echo 'eval "$(mise activate zsh)"' >> ~/.zprofile
```

## Node.js 설치

```bash
mise use --global node@20.11.1

mise install node@18.19.1

mise list node

node -v
# → .nvmrc 파일 인식
# 만약 .nvmrc 파일에 명시된 버전이 없다면 자동으로 설치된다.

# 명시적으로 설치할 수도 있다.
mise install
```

## Bun 설치

```bash
mise use --global bun@1.0.36

mise list bun

bun -v
```

## Python 설치

```bash
mise use --global python@3.12.2

mise install python@3.11.8

mise list python

python --version
# → .python-version 파일 인식
# 만약 .python-version 파일에 명시된 버전이 없다면 자동으로 설치된다.

# 명시적으로 설치할 수도 있다.
mise install
```

## Ruby 설치

```bash
brew install openssl@3 readline libyaml gmp

mise use --global ruby@3.3.0

mise list ruby

ruby -v
# → 마찬가지로 .ruby-version 파일 인식
```

## Go 설치

```bash
mise use --global go@1.22.1

mise list go

go version
```

### Rust 설치

```bash
mise use --global rust@1.77.0

mise list rust

cargo --version
```
