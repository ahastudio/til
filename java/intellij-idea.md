# IntelliJ IDEA

## Install

```bash
brew install intellij-idea-ce
```

## Command-line interface

[Command-line interface | IntelliJ IDEA Documentation](https://www.jetbrains.com/help/idea/working-with-the-ide-features-from-command-line.html)

```bash
mkdir -p ~/.local/bin
touch ~/.local/bin/idea
chmod +x ~/.local/bin/idea
```

```bash
#!/bin/sh

open -na "IntelliJ IDEA CE.app" --args "$@"
```

## Java 버전 지정

[Spring Boot 3.x 실행이 안될 경우 (feat. IntelliJ)](https://jojoldu.tistory.com/698) \
👉 프로젝트 설정에서 SDK 설정하는 방법을 스크린샷과 함께 소개한 글.
