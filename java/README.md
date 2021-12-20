# Java

## `SDKMAN!`으로 설치

Install:

```bash
curl -s "https://get.sdkman.io" | bash
```

`~/.zshrc` 파일에 범용이 아닌 설정이 추가됨.

`~/.zprofile` 파일에 범용 설정 추가:

```zsh
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
export JAVA_HOME=${SDKMAN_CANDIDATES_DIR}/java/current/
```

```bash
sdk list java | grep tem

sdk install java 17.0.1-tem

sdk list java | grep installed

sdk current

java -version
```

```bash
sdk list gradle

sdk install gradle

sdk current
```
