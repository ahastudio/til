# MCP Link: OpenAPI 명세를 읽어 MCP 서버를 자동으로 만드는 변환기

<https://mcp-link.vercel.app/>

<https://github.com/automation-ai-labs/mcp-link>

Show HN: [Show HN: MCP Link – Integrate Any API with AI Agents](https://news.ycombinator.com/item?id=43516541)

## 소개

MCP Link는 OpenAPI v3 명세 URL 하나를 받아
그 API의 엔드포인트를 MCP 도구로 바꿔 주는 Go 서버다.
`automation-ai-labs` 계정이 2025년 3월 29일 만들었고 라이선스는 MIT다.
2026년 10월 현재 스타 625개, 포크 69개이며,
마지막 커밋은 2025년 4월 3일로 이후 1년 반 동안 갱신이 없다.
README의 Discord 배지는 서버 ID 자리에 `1234567890`이 그대로 남아 있다.

README가 내세우는 문제의식은 이렇다.
대부분의 MCP 서버는 웹 API를 감싼 얇은 래퍼인데,
손으로 만들다 보니 기능이 빠지기 쉽고 시간이 들며 오류가 생긴다.
MCP Link는 이 변환을 OpenAPI 명세에서 자동으로 해서
원래 API 코드를 한 줄도 고치지 않고 모든 엔드포인트를 도구로 노출한다고 한다.
설치 없이 쓸 수 있는 호스팅 버전이 `mcp-link.vercel.app`에 있고,
2026년 10월 현재 응답한다.

## 동작 방식

### 요청 하나가 서버 하나를 만든다

MCP 클라이언트는 SSE 엔드포인트에 쿼리 매개변수로 설정을 실어 연결한다.

| 매개변수 | 의미                           |
| -------- | ------------------------------ |
| `s`      | OpenAPI 명세 파일의 URL        |
| `u`      | 실제 API의 기본 URL            |
| `h`      | 모든 API 요청에 붙일 인증 헤더 |
| `f`      | 포함하거나 뺄 경로 필터        |

서버는 연결이 들어오면 `s`의 명세를 `http.Get`으로 내려받아 파싱하고,
필터를 적용한 뒤 엔드포인트마다 MCP 도구를 하나씩 만든다.
도구를 호출하면 `u`에 경로를 붙인 주소로 HTTP 요청을 보내고
`h`의 헤더를 모두 실어 응답을 그대로 돌려준다.
매개변수 대신 이 값들을 JSON으로 묶어
base64로 인코딩한 `code` 하나로 보낼 수도 있다.

### 도구 이름과 설명

도구 이름은 접두사, HTTP 메서드, 경로를 이어 붙이고
공백, 하이픈, 슬래시, 점을 밑줄로 바꾸고 중괄호를 지워 만든다.
`GET /users/{id}`는 `<접두사>_get_users_id` 같은 이름이 된다.
설명은 명세의
`operationId`, `summary`, `description`을 공백으로 이어 붙인 것이다.
입력은 쿼리 매개변수(`searchParams`), 경로 매개변수(`pathNames`),
요청 본문(`requestBody`) 세 객체로 나뉜다.

### 경로 필터

`f`는 노출할 엔드포인트를 고르는 작은 DSL이다.

```text
+/path/**          /path/ 아래 전부 포함
-/path/**          /path/ 아래 전부 제외
+/users/*:GET      /users/{id}의 GET만 포함
+/**:GET;-/internal/**   GET 전부 포함, /internal/ 아래는 제외
```

`*`는 경로 한 단계, `**`는 0개 이상의 단계에 대응한다.

## 설정하기

### 로컬 실행

```bash
git clone https://github.com/automation-ai-labs/mcp-link.git
cd mcp-link   # README는 mcp-openapi-to-mcp-adapter로 들어가라고 하지만 실제 디렉터리 이름은 mcp-link다
go mod download
go run main.go serve --port 8080 --host 0.0.0.0
```

### 클라이언트 설정

README의 형식은 다음과 같다.

```json
{
  "mcpServers": {
    "@service-name": {
      "url": "http://localhost:8080/sse?s=[OpenAPI-Spec-URL]&u=[API-Base-URL]&h=[Auth-Header]:[Value-Prefix]"
    }
  }
}
```

README는 `h`를 `header-name:value-prefix` 형식이라고 설명하지만,
`utils/multiserver_sse.go`의 코드는 `h`를 JSON 객체로 파싱한다.
실제로는 `{"Authorization":"Bearer <토큰>"}`을 URL 인코딩해 넣어야 하며,
README 형식대로 넣으면 `failed to parse headers` 오류가 난다.
저장소의 `examples/` 폴더에는 Brave, DuckDuckGo, Notion, Slack, YouTube 등
명세를 직접 정리한 YAML 파일이 들어 있다.

## 트레이드오프

### 전부 노출하면 완전하지만 모델이 고르지 못한다

README가 내세우는 장점은 “모든 엔드포인트를 빠짐없이 매핑한다”는 완전성이다.
그러나 GitHub이나 Stripe처럼 엔드포인트가 수백 개인 API를 그대로 변환하면
도구 목록이 수백 개가 되고, 그 설명이 모두 컨텍스트를 차지한다.
모델은 이름이
`_get_repos_owner_repo_pulls_pull_number_reviews` 같은 도구 수백 개 중에서
맞는 것을 골라야 한다.

`f` 필터가 그 해법인데, 필터를 잘 쓰려면 결국 사람이
어떤 엔드포인트가 이 작업에 필요한지 골라야 한다.
자동 변환이 없애 준다고 한 수작업이 필터 작성으로 옮겨 갈 뿐이다.
README가 비판한 “얇은 래퍼”를 자동으로 대량 생산하는 셈이기도 하다.

### 명세 품질이 곧 도구 품질이다

도구 설명은 `operationId`와 `summary`, `description`을 이어 붙인 문자열이다.
명세의 설명이 빈약하거나 사람 개발자를 위한 문장이라면
모델이 받는 설명도 그대로 빈약하다.
손으로 만든 MCP 서버의 장점은 모델이 읽기 좋은 설명과
작업 단위로 묶은 도구를 설계할 수 있다는 데 있었는데,
자동 변환은 그 설계 단계를 건너뛴다.
명세를 MCP용으로 다듬지 않으면 “변환은 됐지만 잘 쓰이지 않는” 서버가 된다.

### 호스팅 버전은 편하지만 토큰을 넘긴다

호스팅 버전을 쓰면 설치가 필요 없다.
대신 `h`에 넣은 API 토큰이 URL 쿼리에 실려 `mcp-link.vercel.app`으로 간다.
`code` 매개변수의 base64는 인코딩일 뿐 암호화가 아니다.
README 예시 표의 Stripe, GitHub, Slack, Notion은
모두 쓰기 권한이 있는 토큰을 쓰는 API다.
1년 넘게 관리되지 않는 제3자 서버에 그 토큰을 넘기는 일은
편의와 바꾸기에는 위험이 크다.

## 함정

- URL에 들어간 토큰은 클라이언트 설정 파일, 프록시 로그,
  서버 접근 로그에 그대로 남는다.
  로컬에서 직접 띄우더라도 설정 파일을 공유하거나 커밋하면 토큰이 새어 나간다.
- 서버가 `s`의 URL을 직접 내려받으므로,
  공개된 곳에 띄우면 내부망 주소를 명세 URL로 넣어
  서버가 대신 요청하게 만드는 SSRF 통로가 될 수 있다.
- SSE 응답에 `Access-Control-Allow-Origin: *`가 설정되어 있다.
  로컬에 띄운 서버라도 브라우저의 다른 사이트에서 접근할 수 있다는 뜻이다.
- 전송 방식은 HTTP+SSE이고 `mcp-go` v0.17.0을 쓴다.
  MCP 명세는 이후 Streamable HTTP로 옮겨 갔으므로,
  최신 클라이언트에서는 연결 방식을 확인해야 한다.
  둘의 차이는 [SSE와 Streamable HTTP](sse-vs-streamable-http.md) 문서에 정리되어 있다.
- 쓰기 엔드포인트도 필터로 막지 않으면 모두 도구가 된다.
  `DELETE`와 `POST`를 기본으로 빼고 필요한 것만 여는 편이 안전하다.
- 응답을 가공 없이 그대로 돌려주므로 큰 JSON 응답은 컨텍스트를 빠르게 채운다.
- README의 향후 계획(OAuth 흐름, 리소스 지원, MIME 타입 확장)은
  마지막 커밋 이후 진행되지 않았다.

## 체크리스트

- [ ] 호스팅 버전이 아니라 직접 띄운 서버를 쓰는가
- [ ] `h`를 README 형식이 아니라 JSON 객체로 넣었는가
- [ ] 토큰이 들어간 클라이언트 설정 파일을 저장소에서 제외했는가
- [ ] `f` 필터로 작업에 필요한 엔드포인트만 열었는가
- [ ] 쓰기 메서드(`POST`, `PUT`, `PATCH`, `DELETE`)를 의도적으로만 열었는가
- [ ] 서버를 외부에 노출하지 않고 로컬 주소에서만 수신하는가
- [ ] 명세의 `summary`와 `description`이 모델이 읽기에 충분한가

## 자동 변환을 시험하는 순서

먼저 인증이 필요 없는 시험용 명세나 읽기 전용 경로만 노출한다.
도구 이름과 설명이 실제 작업을 구분하는지,
매개변수와 응답이 모델이 다룰 수 있는 크기인지 살핀다.
명세 전체를 한 번에 열어 두면
불필요한 도구와 예상하지 못한 쓰기 권한까지 함께 늘어난다.

그다음 인증을 최소 권한 토큰으로 연결하고
서버 로그, 프록시 로그, 클라이언트 설정에서
토큰이 남지 않는지 확인한다.
호스팅 서비스는 URL에 자격 증명이 들어갈 수 있으므로
테스트용 토큰을 사용하고, 실제 비밀은 노출하지 않는다.

마지막으로 명세 변경이 도구 계약을 바꾸는지 자동 비교한다.
경로가 추가되거나 요청 본문이 달라졌을 때
기존 허용 목록을 다시 검토하고,
호출 실패와 응답 크기를 측정한다.
자동 변환기는 API 변경을 빠르게 반영하는 대신
모델에 보이는 인터페이스도 함께 바꾼다.

## 기억할 원칙

### 자동 변환은 출발점이지 결과물이 아니다

OpenAPI에서 MCP로의 자동 변환은 API가 무엇을 할 수 있는지를 빠르게 보여 준다.
하지만 사람 개발자를 위한 API의 모양과 모델이 잘 쓰는 도구의 모양은 다르다.
사람은 문서를 읽고 엔드포인트를 조합하지만,
모델은 도구 목록과 설명 한 줄로 매번 다시 판단한다.

그래서 자동 변환 결과는 시제품으로 쓰고,
실제로 자주 쓰는 작업이 보이면 그 작업 단위의 도구를 따로 만드는 편이 낫다.
[기존 REST API에 MCP 엔드포인트를 붙이는 방식](mcp-api-wrapper.md)이나
[APIANT의 MCP 서버 기능](apiant-mcp-servers.md)처럼
작업 단위로 도구를 설계하는 접근이 이 단계에서 다시 의미를 갖는다.
