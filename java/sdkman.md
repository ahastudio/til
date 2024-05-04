# `SDKMAN!`

<https://sdkman.io/>

## SDKMAN! 설치

```bash
curl -s "https://get.sdkman.io" | bash
```

`~/.zshrc` 파일에 범용이 아닌 설정이 추가됨.

`~/.zprofile` 파일에 범용 설정 추가:

```zsh
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
```

## SDKMAN! 업데이트

```bash
sdk selfupdate
```

## OpenJDK 설치

<https://en.wikipedia.org/wiki/Java_version_history>

LTS인 21 버전 설치.

```bash
sdk list java | grep tem

sdk install java 21.0.3-tem

sdk list java | grep installed

sdk current

java -version
```

Java 21 버전을 기본으로 설정.

```bash
sdk default java 21.0.3-tem

sdk current

sdk list java | grep installed

sdk list java | grep "21\."
```

## Gradle 설치

```bash
sdk list gradle

sdk install gradle

sdk current
```
