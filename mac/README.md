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
# 설치 및 설정

brew install mise

eval "$(mise activate zsh)"

echo 'eval "$(mise activate zsh)"' >> ~/.zprofile

# Python

mise use --global python@3.12.2

mise install python@3.11.8

mise list python

python --version

# → .python-version 파일 인식

# Node.js

mise use --global node@20.11.1

mise install node@18.19.1

mise list node

node -v

# → .nvmrc 파일 인식
```
