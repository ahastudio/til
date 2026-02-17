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

## Customize web

사내에서 즉각적으로 업데이트 되는 문서를 확인하고 싶다면 다음과 같이 한다.

```bash
mkdir -p $HOME/tmp/godoc/doc

godoc -http=:6060 -goroot=$HOME/tmp/godoc
```

- 기본 문서: <https://github.com/golang/go/tree/master/doc>
- 기본 템플릿: <https://github.com/golang/tools/tree/master/godoc/static>

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

## Blog Page

블로그 페이지를 접근했을 때 외부로 이동하는 걸 막으려면 `golang.org/x/blog`
패키지를 설치하면 된다.

패키지 소스 코드: <https://github.com/golang/blog>

GoDoc 사이트에서 blog 경로 처리하는 코드:
<https://github.com/golang/tools/blob/master/cmd/godoc/blog.go>

`GOROOT` 환경 변수를 설정하고 그 아래에 `blog` 폴더를 만들어서 써도 된다.

```bash
mkdir -p $HOME/tmp/godoc/blog/template

# 에러가 나지 않도록 최소 파일을 만들어서 사용.
echo '{{define "root"}}...{{end}}' > $HOME/tmp/godoc/blog/template/root.tmpl
echo '' > $HOME/tmp/godoc/blog/template/home.tmpl
echo '' > $HOME/tmp/godoc/blog/template/index.tmpl
echo '' > $HOME/tmp/godoc/blog/template/article.tmpl
echo '' > $HOME/tmp/godoc/blog/template/doc.tmpl

GOROOT=$HOME/tmp/godoc godoc -http=:6060
```

## Go Walker

> Go Walker is a server that generates Go projects API documentation on the fly
> for the projects on GitHub.

<https://gowalker.org/>

## Exmaples

- <https://github.com/natefinch/godocgo>
