# Buffered I/O

`io.Reader`와 `io.Writer`를 wrapping한 `struct`를 `bufio.Reader`와
`bufio.Writer`로 제공하는 패키지. 내부에 byte slice와 read/write position을 둬서
버퍼를 관리한다. 버퍼의 기본 크기는 `4096` 바이트.

기본적인 `Read`, `Write` 외에 도움이 되는 메서드도 다수 제공한다.

- <https://golang.org/pkg/bufio/>
- <https://golang.org/src/bufio/bufio.go>
