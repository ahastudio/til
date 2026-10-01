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

## Configuration

<https://mise.jdx.dev/configuration.html>

`~/.config/mise/config.toml` 파일에 다음 내용을 추가해 `.nvmrc`,
`.python-version`, `.ruby-version` 파일을 인식할 수 있다.

```toml
[settings]
idiomatic_version_file_enable_tools = ['node', 'python', 'ruby']
```

`npm`, `pnpm`, `yarn`도 같은 설정에 넣으면 `package.json`의 `packageManager`
값에서 버전을 읽을 수 있다.
자세한 내용은 [Node.js](nodejs.md)의 쿡북 절을 참고한다.

## 문서

- [Node.js](nodejs.md)
- [Bun](bun.md)
- [Python](python.md)
- [Ruby](ruby.md)
- [Go](golang.md)
- [Rust](rust.md)
- [Terraform 쿡북](terraform.md)
