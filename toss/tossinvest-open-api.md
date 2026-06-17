# 토스증권 Open API

- 토스증권 Open API 소개: <https://corp.tossinvest.com/ko/open-api>
- 개발자 문서: <https://developers.tossinvest.com/docs>
- LLM용 안내: <https://developers.tossinvest.com/llms.txt>
- 활용 후기: <https://jessyt.tistory.com/480>

토스증권 Open API는 국내(KRX) 및 미국 주식의 시세·종목정보·환율·시장정보·
계좌·보유주식·주문 기능을 제공하는 REST API다.
모든 호출에 OAuth 2.0 Client Credentials Grant로 발급받은 access token을
사용하며, 기본 서버는 `https://openapi.tossinvest.com`이다.

## 소개

API는 기능에 따라 네 가지 카테고리로 분류된다.

- **인증(Auth)**: OAuth 2.0 토큰 발급
- **시세·종목 정보(Market Data · Stock Info · Market Info)**: 시세, 종목
  마스터, 환율, 장 운영 시간
- **계좌·자산(Account · Asset)**: 계좌 목록 및 보유 주식 조회
- **주문(Order · Order History · Order Info)**: 주문 생성·정정·취소,
  주문 조회, 거래 가능 정보

시세·종목 정보는 사용자 계좌와 무관한 객관적 데이터이므로 OAuth 2.0
토큰만으로 호출할 수 있다.
반면 **계좌·자산**과 **주문** 카테고리는 토큰에 더해 계좌 식별 헤더
`X-Tossinvest-Account`를 함께 전달해야 한다.
연동 방식은 현재 REST API만 제공한다(WebSocket 실시간 시세는 미지원).

문서의 최종 기준(source of truth)은 서버가 소유한 OpenAPI 3.0 JSON
문서다.

- Overview: <https://openapi.tossinvest.com/openapi-docs/overview.md>
- API Reference (Markdown): <https://openapi.tossinvest.com/openapi-docs/latest/api-reference/README.md>
- OpenAPI JSON: <https://openapi.tossinvest.com/openapi-docs/latest/openapi.json>

`llms.txt`가 별도로 제공되어, 외부 LLM이나 AI 코딩 에이전트가 문서를
직접 읽고 클라이언트를 생성할 수 있다.

## 명세

### 인증

| 엔드포인트          | 설명                                          |
| ------------------- | --------------------------------------------- |
| `POST /oauth2/token` | OAuth 2.0 액세스 토큰 발급 (Client Credentials Grant) |

모든 호출에 `Authorization: Bearer {access_token}` 헤더가 필요하다.
JWKS도 제공된다.

### 시세·종목 정보

| 엔드포인트                            | 설명                                       |
| ------------------------------------- | ------------------------------------------ |
| `GET /api/v1/orderbook`               | 호가 조회                                  |
| `GET /api/v1/prices`                  | 현재가 조회                                |
| `GET /api/v1/trades`                  | 최근 체결 내역 조회                        |
| `GET /api/v1/price-limits`            | 상/하한가 조회                             |
| `GET /api/v1/candles`                 | 캔들 차트 조회 (1분봉 · 일봉)              |
| `GET /api/v1/stocks`                  | 종목 기본 정보 조회 (종목명, 시장, 통화 등) |
| `GET /api/v1/stocks/{symbol}/warnings` | 매수 유의사항 조회 (정리매매, 과열, 경고/위험, VI 등) |
| `GET /api/v1/exchange-rate`           | KRW↔USD 환율 조회                          |
| `GET /api/v1/market-calendar/KR`      | 국내 장 운영 정보 (KRX·NXT 세션별 시간)    |
| `GET /api/v1/market-calendar/US`      | 해외 장 운영 정보 (데이·프리·정규·애프터) |

### 계좌·자산

| 엔드포인트              | 설명                                     |
| ----------------------- | ---------------------------------------- |
| `GET /api/v1/accounts`  | 계좌 목록 조회                           |
| `GET /api/v1/holdings`  | 보유 주식 조회 (종목별 상세 + 평가·손익 합산) |

### 주문

| 엔드포인트                            | 설명                                  |
| ------------------------------------- | ------------------------------------- |
| `POST /api/v1/orders`                 | 주문 생성 (지정가·시장가 / KR·US)     |
| `POST /api/v1/orders/{orderId}/modify` | 주문 정정 (가격·수량)                 |
| `POST /api/v1/orders/{orderId}/cancel` | 주문 취소                             |
| `GET /api/v1/orders`                  | 주문 목록 조회 (대기중/종료)          |
| `GET /api/v1/orders/{orderId}`        | 주문 상세 조회 (모든 상태)            |
| `GET /api/v1/buying-power`            | 매수 가능 금액 조회 (현금 기반, KRW·USD) |
| `GET /api/v1/sellable-quantity`      | 판매 가능 수량 조회                   |
| `GET /api/v1/commissions`            | 매매 수수료 조회 (KR·US 시장별)       |

### Rate Limits

모든 API는 **클라이언트 × API 그룹** 단위로 초당 요청 수(TPS)가 제한된다.

| Rate Limits Group     | 요청 한도     | 피크시간 한도                       |
| --------------------- | ------------- | ----------------------------------- |
| `AUTH`                | 초당 최대 5회 | --                                  |
| `ACCOUNT`             | 초당 최대 1회 | --                                  |
| `ASSET`               | 초당 최대 5회 | --                                  |
| `STOCK`               | 초당 최대 5회 | --                                  |
| `MARKET_INFO`         | 초당 최대 3회 | --                                  |
| `MARKET_DATA`         | 초당 최대 10회 | --                                 |
| `MARKET_DATA_CHART`   | 초당 최대 5회 | --                                  |
| `ORDER`               | 초당 최대 6회 | 09:00~09:10 KST: 초당 최대 3회      |
| `ORDER_HISTORY`       | 초당 최대 5회 | --                                  |
| `ORDER_INFO`          | 초당 최대 6회 | 09:00~09:10 KST: 초당 최대 3회      |

한도는 사전 공지 없이 조정될 수 있으며, 현재 허용 한도는 응답 헤더로
확인한다.

| 헤더                    | 의미                                  |
| ----------------------- | ------------------------------------- |
| `X-RateLimit-Limit`     | 현재 허용된 초당 요청 수 (burst capacity) |
| `X-RateLimit-Remaining` | 버킷에 남은 토큰 수 (429 시 0)        |
| `X-RateLimit-Reset`     | 토큰 1개 재충전까지 예상 초           |
| `Retry-After`           | 재시도 권장 초 (429 응답에만 포함)    |

429 수신 시 `Retry-After`만큼 대기 후 재시도하고, 지수 백오프(1s → 2s →
4s …)와 jitter를 함께 적용하는 것이 권장된다.

### 에러 응답

모든 에러 응답은 다음 envelope으로 내려온다.

```json
{
  "error": {
    "requestId": "01HXYZABCDEFG123456789",
    "code": "invalid-request",
    "message": "주문 방향이 올바르지 않습니다.",
    "data": {
      "field": "side",
      "allowedValues": ["BUY", "SELL"]
    }
  }
}
```

`requestId`는 응답 헤더 `X-Request-Id`와 동일하며 CS 문의 시 첨부가
권장된다.
`code`는 에러 코드, `message`는 관련 메시지, `data`는 코드별로 구조가
다른 해결 힌트다.

주요 에러 코드는 다음과 같다.

| HTTP Status              | 에러 코드                       | 발생 이유                                       |
| ------------------------ | ------------------------------- | ----------------------------------------------- |
| 400 BAD_REQUEST          | `invalid-request`               | 요청이 유효하지 않음 (필수 파라미터 누락 등)    |
| 400 BAD_REQUEST          | `confirm-high-value-required`   | 주문 금액 1억원 이상인데 `confirmHighValueOrder`가 `true`가 아님 |
| 400 BAD_REQUEST          | `account-header-required`       | `X-Tossinvest-Account` 헤더 미전달              |
| 401 UNAUTHORIZED         | `invalid-token`                 | 토큰이 유효하지 않거나 형식 오류                |
| 401 UNAUTHORIZED         | `expired-token`                 | 액세스 토큰 만료                                |
| 401 UNAUTHORIZED         | `edge-blocked`                  | `Authorization` 헤더 미전달                     |
| 403 FORBIDDEN            | `forbidden`                     | 요청에 필요한 권한 부족                         |
| 404 NOT_FOUND            | `stock-not-found`               | 요청한 종목을 찾을 수 없음                      |
| 404 NOT_FOUND            | `account-not-found`             | 계좌 헤더가 가리키는 계좌를 찾을 수 없음        |
| 404 NOT_FOUND            | `order-not-found`               | `orderId`에 해당하는 주문 없음                  |
| 409 CONFLICT             | `request-in-progress`           | 동일 `clientOrderId` 주문 생성이 처리 중        |
| 409 CONFLICT             | `already-filled`                | 정정/취소 대상이 이미 체결됨                    |
| 409 CONFLICT             | `already-canceled`              | 정정/취소 대상이 이미 취소됨                    |
| 422 UNPROCESSABLE_ENTITY | `insufficient-buying-power`     | 주문 가능 금액 부족                             |
| 422 UNPROCESSABLE_ENTITY | `order-hours-closed`            | 주문 접수 불가 시간                             |
| 422 UNPROCESSABLE_ENTITY | `stock-restricted`              | 거래 제한 종목                                  |
| 422 UNPROCESSABLE_ENTITY | `price-out-of-range`            | 주문 가격이 상/하한가 범위를 벗어남             |
| 422 UNPROCESSABLE_ENTITY | `prerequisite-required`         | 약관 동의·위험 고지 등 사전 자격 요건 미충족    |
| 429 TOO_MANY_REQUESTS    | `rate-limit-exceeded`           | 초당 요청 수 초과                               |
| 500 INTERNAL_SERVER_ERROR | `internal-error`               | 서버 일시 장애                                  |
| 500 INTERNAL_SERVER_ERROR | `maintenance`                  | 시스템 점검 중                                  |

## 사용법

### 1. 클라이언트 등록

토스증권 WTS에 로그인 후 **설정 > Open API** 메뉴에서 `client_id`와
`client_secret`을 발급받는다.

### 2. 액세스 토큰 발급

`POST /oauth2/token`으로 Client Credentials Grant 방식의 토큰을 발급
받는다.

```bash
curl -s -X POST 'https://openapi.tossinvest.com/oauth2/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=client_credentials' \
  -d 'client_id=xxx' \
  -d 'client_secret=yyy'
```

### 3. API 호출

발급받은 토큰을 `Authorization: Bearer {access_token}` 헤더에 담아
호출한다.
시세·종목 정보는 토큰만으로 충분하다.

```bash
# 시세·종목 정보 (토큰만 필요)
curl -s 'https://openapi.tossinvest.com/api/v1/stocks?symbols=005930' \
  -H 'Authorization: Bearer eyJhbGciOi...'
```

계좌·자산 및 주문은 `X-Tossinvest-Account: {accountSeq}` 헤더를 함께
전달한다.

```bash
# 계좌·자산 / 주문 (토큰 + 계좌 헤더)
curl -s 'https://openapi.tossinvest.com/api/v1/holdings' \
  -H 'Authorization: Bearer eyJhbGciOi...' \
  -H 'X-Tossinvest-Account: 1'
```

### 멱등키와 중복 주문 방지

주문 생성 시 `clientOrderId`를 멱등키로 활용해 중복 주문을 방지할 수
있다.
동일 `clientOrderId`에 대한 주문이 처리 중이면 `409 request-in-progress`가
반환된다.
1억원 이상 고액 주문은 `confirmHighValueOrder: true`를 명시해야 한다.

## 특징과 한계

활용 후기(jessyt.tistory.com)에서 정리한 실무 관점의 장단점은 다음과
같다.

장점:

- **LLM 친화적 문서**: `llms.txt`가 제공되어 Claude 같은 AI 도구가 문서를
  직접 읽고 파이썬 클라이언트를 즉시 생성할 수 있다.
- **간단한 인증**: `client_id`와 `client_secret` 두 개의 키와 OAuth2
  토큰만으로 주문까지 가능하다.
- **개발자 친화적 에러 처리**: `insufficient-buying-power`,
  `order-hours-closed`처럼 명확한 코드명을 제공하고, 멱등키로 중복 주문을
  방지한다.
- **장 운영 캘린더 제공**: KR·US 장 운영 시간을 API로 조회할 수 있어
  하드코딩이 필요 없다.

한계:

- **WebSocket 실시간 시세 미지원**: 실시간 데이터가 필요하면 1초 폴링으로
  대체해야 한다.
- **모의투자/샌드박스 부재**: 테스트용 환경이 없어, 전략 검증은 별도
  백테스팅으로 보완해야 한다.
- 현재 사전 신청 단계로 운영되고 있어 접근 조건이 변동될 수 있다.
