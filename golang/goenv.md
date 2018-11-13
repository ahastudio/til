# goenv

<https://github.com/syndbg/goenv>

```bash
brew install goenv
```

`.profile` 파일에 추가할 내용.

```bash
eval "$(goenv init -)"

export GOPATH=$(go env GOPATH)
```

All versions: <https://golang.org/dl/>

```bash
goenv install 1.11.2
goenv install 1.10.5
```

Global setting:

```bash
goenv global 1.11.2
```

Project setting:

```bash
goenv local 1.11.2
```

## GoLand

`~/Library/Preferences/GoLand2018.2/options/go.sdk.xml` 파일에 직접 기록:

```xml
<application>
  <component name="GoSdkList">
    <sdk-path>
      <set>
        <option value="$USER_HOME$/.goenv/versions/1.10.5" />
        <option value="$USER_HOME$/.goenv/versions/1.11.2" />
      </set>
    </sdk-path>
  </component>
</application>
```
