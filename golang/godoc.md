# GoDoc

- <https://godoc.org/>

- <https://github.com/golang/tools/tree/master/godoc>

- [Godoc: documenting Go code - The Go Blog](https://blog.golang.org/godoc-documenting-go-code)

## Run web server

<https://godoc.org/golang.org/x/tools/cmd/godoc>

GoDoc 문서를 확인하려면 다음과 같이 실행하면 된다.

```bash
godoc -http=:6060
```

Open Web Browser: http://localhost:6060/

블로그 링크가 밖으로 이동하는 걸 막으려면 blog 패키지 설치.

```bash
go get golang.org/x/blog
```

## Customize web

사내에서 즉각적으로 업데이트 되는 문서를 확인하고 싶다면 다음과 같이 한다.

```bash
mkdir -p $HOME/tmp/godoc/doc

godoc -http=:6060 -goroot=$HOME/tmp/godoc
```

기본 `Path`를 커버하는 문서를 만든다.

`$HOME/tmp/godoc/doc/root.html`:

```html
<!--{
  "Path": "/"
}-->

<h1>Home</h1>

<p>Welcome!</p>
```

`$HOME/tmp/godoc/doc/docs.html`:

```html
<!--{
    "Title": "Documentation",
    "Path": "/doc/"
}-->

<p>Documentation</p>
```

`$HOME/tmp/godoc/doc/contrib.html`:

```html
<!--{
    "Title": "Project",
    "Path": "/project/"
}-->

<p>Project</p>
```

`$HOME/tmp/godoc/doc/help.html`:

```html
<!--{
    "Title": "Help",
    "Path": "/help/"
}-->

<p>Help</p>
```

## Go Walker

> Go Walker is a server that generates Go projects API documentation
> on the fly for the projects on GitHub.

<https://gowalker.org/>

## Exmaples

- <https://github.com/natefinch/godocgo>
