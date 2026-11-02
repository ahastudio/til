# Rust를 다른 언어 서버에 단계적으로 넣는 다섯 방법과 QR 코드 벤치마크

원문: [Using Rust in Non-Rust Servers to Improve Performance](https://github.com/pretzelhammer/rust-blog/blob/master/posts/rust-in-non-rust-servers.md)

HN 토론: <https://news.ycombinator.com/item?id=41941451> (406점, 273개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=41924514> (4점, 0개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/slviv2/using_rust_non_rust_servers_improve> (38점, 42개 댓글)

GN 토론: <https://news.hada.io/topic?id=17549>

## 소개

pretzelhammer가 2024년 10월 22일에 올린 글이다.
JavaScript, Python, Java, Go, PHP, Ruby 같은 언어로 쓴 서버에 Rust를 조금씩 넣는
전략을 단계(tier)로 나누어 설명한다.
글이 전제하는 상황은 하나다.
서버를 프로파일링해서 CPU가 병목인 핫 함수(hot function)를 찾았고,
메모이제이션이나 알고리즘 개선은 쓸 수 없거나 효과가 없다는 결론이
이미 난 경우다.

예제는 Node.js와 Express로 만든 서버다.
쿼리 문자열로 받은 텍스트를 200×200픽셀 PNG의 QR 코드로 돌려주는 `/qrcode`
엔드포인트이고, 텍스트는 512바이트 이하로 제한한다.
핫 함수는 QR 코드 생성 함수 하나이며, 같은 함수를 다섯 가지 방식으로 구현해 같은
환경에서 30초 동안 수만 건의 요청을 보내 비교한다.
글은 코드 전체가 별도 저장소에 있다고 안내한다.

## 다섯 단계

단계의 이름은 Rust를 얼마나 도입하느냐를 뜻한다.

| 단계   | 방식                                      | 처리량       | 평균 지연 | p99 지연 | 평균 응답   | 메모리  |
| ------ | ----------------------------------------- | ------------ | --------- | -------- | ----------- | ------- |
| Tier 0 | Rust 없음, JavaScript `qrcode` 라이브러리 | 1464 req/sec | 68 ms     | 96 ms    | 1506 바이트 | 1353 MB |
| Tier 1 | Rust CLI 도구를 요청마다 실행             | 2572 req/sec | 39 ms     | 78 ms    | 778 바이트  | 1240 MB |
| Tier 2 | Rust를 Wasm 모듈로 컴파일해 로드          | 2978 req/sec | 34 ms     | 63 ms    | 778 바이트  | 1286 MB |
| Tier 3 | Rust 네이티브 함수(`napi-rs`)             | 5490 req/sec | 18 ms     | 37 ms    | 778 바이트  | 1309 MB |
| Tier 4 | 서버 전체를 Rust(`axum`)로 다시 작성      | 7212 req/sec | 14 ms     | 27 ms    | 778 바이트  | 13 MB   |

Tier 0 대비 처리량은 Tier 1이 1.76배, Tier 2가 2.03배, Tier 3이 3.75배,
Tier 4가 4.93배다.
글의 결론은 Tier 3이 들인 노력 대비 효과가 가장 크다는 것이다.
이미 있는 바인딩 생성 라이브러리를 쓸 수 있으면 Rust 네이티브 함수는 쉽게 쓸 수
있고 성능에 큰 영향을 준다고 쓴다.
가장 어려운 부분은 Rust를 아직 모른다면 Rust를 배우는 일이라고 한다.

### Tier 1: CLI 도구

핫 함수를 Rust로 다시 쓰고 `qr-cli`라는 독립 실행 파일로 컴파일한 뒤,
Node.js가 `child_process.spawn`으로 요청마다 실행해 표준 출력으로 PNG
바이트를 받는다.
글쓴이는 처리량이 76% 늘 줄은 몰랐다고 쓰고,
평균 응답 크기가 1506바이트에서 778바이트로 줄어든 것을 Rust 쪽 압축 알고리즘이
낫기 때문이라고 해석한다.

Lobste.rs에서는 simonw가 요청마다 프로세스를 띄우는 쪽이 JavaScript 안에서 도는
쪽보다 두 배 가까이 빨랐다는 데 놀랐다고 썼다.
그가 든 숫자는 초당 2572건 대 1464건이다.[^simonw]
insanitybit는 이것이 프로세스를 띄우는 일이 빠르다는 증거라기보다 Node.js 코드가
그만큼 느리다는 뜻이라고 답했다.[^insanitybit]
ngp는 프로세스를 띄우면 작업이 이벤트 루프 밖으로 나가 루프가 다른 요청을 계속
처리할 수 있다고 설명했고,[^ngp]
simonw는 그렇다면 여러 코어를 쓰는 쉬운 방법이기도 하겠다고
되받았다.[^simonw-reply]
andyc는 Unix 프로세스를 띄우는 일은 느리지 않다는 예로, sqlite.org가 연결마다
C 프로그램을 새로 시작한다는 Richard Hipp의 이야기를 들었다.[^andyc]

첫 실행이 느리다는 반론도 나왔다.
danthegoodman1은 Rust 바이너리를 다시 빌드한 뒤 첫 실행은 늘 800ms가 넘게
걸리지 않느냐고 물었다.[^danthegoodman1]
christianscott는 macOS가 서명되지 않은 실행 파일을 처음 실행할 때
요청이 끝나기를
동기로 기다리는 notarization 검사일 것이라고 짐작했다.[^christianscott]
markwatson은 Linux에서는 첫 실행도 더 오래 걸리지 않았고 0.017초였다고
보고했지만, 느린 머신에서 다른 프로그램이 돌아가는 상태라 현실적인 시험은
아니라고 스스로 밝혔다.[^markwatson]
이 문서는 이 중 어느 설명이 맞는지 가르지 않았다.

### Tier 2: Wasm 모듈

`wasm-bindgen`이 생성한 접착 코드로 Node.js가 Wasm 모듈을 부른다.
글은 Wasm 런타임 목록(Wasmer, Wasmtime, WasmEdge, wasm3, Wazero, Extism,
Chicory)을 언어별로 정리하고, Tier 1보다 향상 폭이 예상보다 작았다고 말한다.
`wasm-bindgen`에 해당하는 도구가 다른 언어에는 없으므로,
손으로 바인딩을 쓰는 방법도 보여 준다.

Wasm은 `i32`, `i64`, `f32`, `f64` 네 가지 타입만 지원하므로 문자열과 배열을 직접
넘길 수 없다.
호스트가 Wasm 모듈의 메모리에 문자열을 직접 쓰고,
그 주소(`i32`)와 길이를 함수에 넘긴다.
반대로 배열을 받으려면 호스트가 출력 버퍼의 주소를 넘기고 함수가 쓴 바이트
수를 돌려받는다.
호스트가 모듈이 쓰는 메모리를 덮어쓰지 않으려면 먼저 모듈에게 공간을
할당(`alloc`)해 달라고 해야 한다.
글쓴이는 손으로 쓴 바인딩의 성능이 생성된 바인딩과 사실상 같았다고 적는다.
Wasm 컴포넌트 모델(Component Model)의 WIT(Wasm Interface Type)가 표준화되면 이
접착 코드를 도구가 만들어 줄 것이라고 기대하며, 지금은 Rust 쪽에 `wit-bindgen`,
JavaScript 쪽에 `jco`를 짝으로 쓸 수 있다.

### Tier 3: 네이티브 함수

`napi-rs`는 Rust 함수에 `#[napi]` 속성을 붙이는 것만으로 Node.js가 부를 수 있는
모듈을 만든다.
글이 정리한 언어별 바인딩 생성기는 Python의 `pyo3`, Erlang의 `rustler`,
여러 언어를 지원하는 `uniffi-rs`와 `diplomat`, Java의 `jni-rs`, Ruby의 `rutie`,
PHP의 `ext-php-rs`다.
글쓴이는 이 단계가 Wasm 구현의 두 배에 가깝고 기준선의 거의 네 배라고 말한다.

### Tier 4: 서버 재작성

서버 전체를 Rust로 다시 쓴다.
글은 코드베이스가 10만 줄이 넘는 실제 서버에서는 비현실적이라고 인정하고,
대신 일부 요청만 Rust 서버로 보내도록 리버스 프록시 설정을 바꾸는
방법을 제안한다.
Tier 4는 7200건이 넘는 초당 요청을 13 MB 메모리로 처리했다.

## 단계를 고르는 기준

글의 숫자와 댓글의 논점을 합치면 다음과 같이 읽을 수 있다.
이 표는 글의 결론이 아니라 이 문서의 정리다.

| 단계   | 얻는 것                          | 치르는 것                            | 이 문서가 읽은 근거                                    |
| ------ | -------------------------------- | ------------------------------------ | ------------------------------------------------------ |
| Tier 1 | 가장 작은 변경, 프로세스 격리    | 요청마다 프로세스를 띄움             | 글의 숫자와 `posix_spawn`이 빠르다는 댓글[^sunshowers] |
| Tier 2 | 샌드박스, 이식성                 | 접착 코드, 메모리 복사               | 글의 손으로 쓴 바인딩 설명                             |
| Tier 3 | 가장 큰 향상 대비 낮은 코드 변경 | 같은 프로세스에서 도는 네이티브 코드 | 글의 숫자와 Elixir NIF 위험 댓글[^dowwie]              |
| Tier 4 | 메모리와 지연의 큰 감소          | 재작성 비용, 라우팅 변경             | 글의 숫자                                              |

이 순서에서 실제 결정에 영향을 주는 것은 입력과 출력의 크기다.
이 예제는 512바이트 이하를 넣고 778바이트를 받으므로 경계를 넘는 복사
비용이 거의 없다.
큰 페이로드를 넘기는 핫 함수라면 Tier 2와 Tier 3의 복사 비용이 순위를 바꿀 수
있고, 이 글의 숫자로는 그것을 알 수 없다.

## 비평

### 단계 사이의 비교는 같은 일을 하지 않는다

Tier 0의 JavaScript 코드는 PNG 인코딩에 `deflateLevel: 9`와 `deflateStrategy:
3`을 쓰고, Rust 코드는 `CompressionType::Default`와
`FilterType::NoFilter`를 쓴다.
두 쪽이 서로 다른 설정으로 서로 다른 PNG를 만든다는 것은 응답 크기가
1506바이트에서 778바이트로 절반이 된 데서도 드러난다.
그러므로 Tier 0과 Tier 1 사이의 처리량 차이에는 언어의 효과와 PNG 인코딩 설정의
효과가 섞여 있고, 글의 숫자로는 둘을 나눌 수 없다.

Hacker News에서도 같은 의문이 나왔다.
voiper1은 왜 평균 바이트가 작으냐고 물었고,[^voiper1] pixelesque는 인코딩한
텍스트가 두 예제에서 달랐으니 압축률이 같아도 크기가 다를 수 있다고
답했다.[^pixelesque]
글쓴이는 벤치마크 도구 vegeta가 HTTP 헤더를 빼고 본문 크기만 재며 대상 목록을
돌아가면서 요청한다고 밝혔고, 같은 라이브러리와 같은 압축 알고리즘이어도
인코딩한 텍스트에 따라 PNG 크기가 달라진다고 덧붙였다.[^pretzelhammer]
이 설명은 응답 크기가 다른 이유의 하나일 수 있지만,
단계마다 같은 대상 목록을 썼다면 그 차이는 단계 사이에서 상쇄된다.
그렇다면 크기 차이는 인코더 설정에서 왔다고 보는 것이 이 문서의 읽기이며,
이 문서는 어느 인코더가 낫다고 단정하지 않는다.

### 메모리 숫자는 프로세스 모델의 차이다

Tier 4의 13 MB와 Tier 0의 1353 MB를 비교하면 1% 수준이라는 인상을 준다.
글은 기준선의 큰 메모리를 Node.js를 클러스터 모드로 돌려 12코어마다 프로세스
하나씩, 모두 12개를 띄웠기 때문이라고 스스로 설명한다.
Tier 1에서 Tier 3까지의 메모리가 기준선과 비슷한 것도 호스트가 그대로 12개
프로세스이기 때문이다.
jchw도 메모리가 큰 이유의 큰 부분은 Node.js가 멀티코어를 쓰려면 프로세스를 여럿
띄워야 한다는 데 있다고 지적했다.[^jchw-memory]
xyst가 메모리 감소를 과소평가된 장점으로 꼽은 것은 맞는 방향이지만,
이 숫자만으로는 언어 효과와 프로세스 모델 효과를 가를 수 없다.[^xyst]

### 한 번의 측정은 순위만 말해 준다

글은 방법론을 설명하지 않으면 숫자가 그 자체로는 의미가 없고 모든 서버를 같은
환경에서 시험해서 상대 비교는 정확하다고 쓴다.
측정 횟수, 편차, 워밍업은 글에 나오지 않는다.
rwaksmunski는 Axum 서버에서 Nagle 알고리즘 때문에 성능이 막혔다가
`TCP_NODELAY`를 켜서 9만 req/s에서 70만 req/s로 올랐던 경험을 들며 Tier 4가 더
빨라야 한다고 의심했다.[^rwaksmunski]
반대로 nemetroid는 가장 빠른 단계의 평균 지연이 14 ms이고 로컬호스트 `ping`이 20
µs 정도이므로, 네트워크가 아니라 CPU가 병목이라고 읽었다.[^nemetroid]
이 둘을 가르는 측정은 글에 없다.

### 같은 프로세스 안의 네이티브 코드는 장애 격리를 잃는다

글은 Tier 3을 가장 효율이 좋은 선택으로 꼽지만 실패했을 때 무슨 일이 생기는지는
다루지 않는다.
Tier 1은 별도 프로세스라 CLI가 죽어도 서버는 산다.
Dowwie는 Elixir에서 NIF가 BEAM과 같은 메모리 공간에서 돌아 BEAM 전체를 죽일 수
있다고 경고했고,[^dowwie] mijoharas는 `rustler`의 README가 Rust NIF 코드는
BEAM을 죽일 수 없어야 한다고 적는다고 반박하면서도,
그 원리를 설명하는 문서는 찾지 못했다고 적었다.[^mijoharas]
어느 언어에서든 이 위험은 바인딩 도구가 패닉을 어떻게 다루는지에 달려 있고,
도입하기 전에 확인해야 한다.

### 손으로 쓴 Wasm 예제에는 입력 크기 검사의 틈이 있다

글의 JavaScript 서버는 `text.length > 512`로 길이를 검사하고,
오류 메시지는 512바이트라고 말한다.
`length`는 UTF-16 코드 단위 수이므로 바이트 수와 다르다.
이 문서를 쓰며 Node.js에서 확인하니 한글 512자는 `length`가 512이고 UTF-8로
인코딩하면 1536바이트였다.
손으로 쓴 Wasm 바인딩은 입력 버퍼를 1024바이트만 할당하는데,
호스트 코드는 인코딩한 바이트를 그 길이 검사 없이 `qrWasmMemory.set`으로 쓴다.
검사를 통과한 1536바이트 입력은 할당한 1024바이트를 넘어 인접한
메모리에 쓰게 된다.
출력 버퍼가 바로 다음에 할당되어 있는지와 부하에서 실제로 깨지는지는 이 문서가
시험하지 않았다.
같은 예제에서 `Buffer.from(memory.buffer, offset,
len)`은 복사본이 아니라 Wasm 메모리의 뷰를 돌려준다.
Node.js에서 같은 형태로 만들어 기본 배열에 쓰면 뷰에서도 값이 바뀌는
것을 확인했다.
다음 요청이 같은 출력 버퍼를 덮어쓰면 아직 소켓에 쓰이지 않은 응답이 바뀔 수
있고, 글의 벤치마크는 응답 내용을 검증하지 않았다.
이 두 문제는 벤치마크에 쓴 `wasm-bindgen` 경로가 아니라 설명용 손 바인딩
코드의 것이다.

## 체크리스트

- [ ] 프로파일링으로 CPU가 병목인 함수를 찾았고, 메모이제이션과 알고리즘 개선이 안 되는 이유를 적었는가
- [ ] 기준선과 Rust 구현이 같은 결과(같은 인코더 설정, 같은 출력)를 내는지 비교했는가
- [ ] 메모리를 비교할 때 프로세스 수를 같게 맞췄는가
- [ ] 측정을 여러 번 반복하고 편차를 기록했는가
- [ ] 핫 함수의 입력과 출력 크기를 알고 있는가(경계를 넘는 복사 비용이 순위를 바꿀 수 있다)
- [ ] 네이티브 코드(Tier 3)가 패닉이나 크래시를 낼 때 호스트 프로세스가 어떻게 되는지 확인했는가
- [ ] 손으로 Wasm 바인딩을 쓴다면 입력 길이를 바이트 단위로 검사하고 버퍼를 복사해서 돌려주는가
- [ ] 서버 일부만 Rust로 옮길 때 리버스 프록시의 라우팅과 배포 비용을 계산했는가

---

[^sunshowers]: <https://news.ycombinator.com/item?id=41978475>

[^dowwie]: <https://news.ycombinator.com/item?id=41971126>

[^voiper1]: <https://news.ycombinator.com/item?id=41970920>

[^pixelesque]: <https://news.ycombinator.com/item?id=41970974>

[^pretzelhammer]: <https://news.ycombinator.com/item?id=41976559>

[^jchw-memory]: <https://news.ycombinator.com/item?id=41971055>

[^xyst]: <https://news.ycombinator.com/item?id=41970789>

[^rwaksmunski]: <https://news.ycombinator.com/item?id=41977855>

[^nemetroid]: <https://news.ycombinator.com/item?id=41974985>

[^mijoharas]: <https://news.ycombinator.com/item?id=41973926>

[^simonw]: <https://lobste.rs/s/slviv2/using_rust_non_rust_servers_improve#c_kenwlh>

[^insanitybit]: <https://lobste.rs/s/slviv2/using_rust_non_rust_servers_improve#c_pfrxr4>

[^ngp]: <https://lobste.rs/s/slviv2/using_rust_non_rust_servers_improve#c_xn3irn>

[^simonw-reply]: <https://lobste.rs/s/slviv2/using_rust_non_rust_servers_improve#c_8eno5z>

[^andyc]: <https://lobste.rs/s/slviv2/using_rust_non_rust_servers_improve#c_lty5zb>

[^danthegoodman1]: <https://lobste.rs/s/slviv2/using_rust_non_rust_servers_improve#c_qdtkwf>

[^christianscott]: <https://lobste.rs/s/slviv2/using_rust_non_rust_servers_improve#c_qccoma>

[^markwatson]: <https://lobste.rs/s/slviv2/using_rust_non_rust_servers_improve#c_lmki9e>
