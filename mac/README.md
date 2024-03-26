# Mac

## Homebrew

> 🍺 The Missing Package Manager for macOS (or Linux)

<https://brew.sh/>

<https://github.com/Homebrew/brew>

## mas

> 📦 Mac App Store command line interface

<https://github.com/mas-cli/mas>

## asdf

> Manage multiple runtime versions with a single CLI tool

<https://asdf-vm.com/>

<https://github.com/asdf-vm/asdf>

## mise-en-place

> The front-end to your dev env

<https://mise.jdx.dev/>

<https://github.com/jdx/mise>

<https://formulae.brew.sh/formula/mise>

```bash
brew install mise

eval "$(mise activate zsh)"

echo 'eval "$(mise activate zsh)"' >> ~/.zprofile
```

### Node.js 설치

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

### Python 설치

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

### Ruby 설치

```bash
brew install openssl@3 readline libyaml gmp

mise use --global ruby@3.3.0

mise list ruby

ruby -v
# → 마찬가지로 .ruby-version 파일 인식
```

### Go 설치

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

## Caddy

> The Ultimate Server with Automatic HTTPS

<https://caddyserver.com/>

<https://github.com/caddyserver/caddy>

[Caddy 2 릴리즈 - 성능 좋고 간편한 HTTPS 자동 지원 웹서버 | GeekNews](https://news.hada.io/topic?id=2028)

[Caddy 오픈소스 웹서버, Apilayer에 인수 | GeekNews](https://news.hada.io/topic?id=2832)

<https://formulae.brew.sh/formula/caddy>

```bash
brew install caddy
```

Getting Started: <https://caddyserver.com/docs/getting-started>

## lcl.host

> The fastest & easiest way to get HTTPS in your local development environment.

<https://lcl.host/>

[Introducing lcl host](https://anchor.dev/blog/introducing-lcl-host)

[Lcl.host: 로컬 개발 환경에서 빠르고 쉬운 HTTPS 구현 | GeekNews](https://news.hada.io/topic?id=13921)

```bash
brew install anchordotdev/tap/anchor

anchor lcl
# → GitHub으로 로그인 가능.
```
