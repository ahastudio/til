# ChatGPT로 로그인은 사용자 자신의 ChatGPT 요금제 한도로 AI 사용량을 내게 하는 기능이지만 별도 권한이고 앱마다 열려 있지 않다

원문: [Sign in with ChatGPT - OpenAI Developers](https://developers.openai.com/siwc)

HN 토론: <https://news.ycombinator.com/item?id=49897965> (2점, 1개 댓글)

## 먼저 답: 사용자가 자기 계정으로 AI 사용량을 감당하는가

결론부터 말하면 맞습니다. 다만 조건이 붙습니다.
여기서 “토큰”은 두 가지로 쓰입니다.
AI 모델이 소비하는 사용량(토큰)과, 로그인 과정에서 오가는 OAuth 토큰입니다.
사용자가 감당하는 것은 앞의 사용량이고,
뒤의 OAuth 토큰은 앱이 그 권한을 행사하는 수단입니다.

| 질문                                                     | 문서가 말하는 답                                                                                                                       |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| 앱의 AI 요청 비용을 사용자의 ChatGPT 요금제가 부담하는가 | 부담합니다. 사용자가 허용하면 앱의 적격(eligible) AI 요청이 사용자의 ChatGPT 요금제에 포함된 사용량 또는 보유한 크레딧으로 처리됩니다. |
| 새 한도가 생기는가                                       | 생기지 않습니다. 사용자 문서는 앱 사용량이 기존 요금제 한도에 합산되고 연결해도 새 허용량이 더해지지 않는다고 합니다.[^learn]          |
| 앱이 별도로 요금을 받을 수 있는가                        | 받을 수 있습니다. 같은 문서는 앱에 자체 요금이 있을 수 있다고 합니다.[^learn]                                                          |
| 로그인만 하면 자동으로 적용되는가                        | 아닙니다. 로그인과 요금제 사용은 별도 권한이며, 사용자가 요금제 사용 권한에 따로 동의해야 합니다.[^learn]                              |
| 모든 사용자가 되는가                                     | 아닙니다. 적격인 ChatGPT Plus와 Pro 사용자에게 열려 있고, 선택한 사용자·워크스페이스·정책에서는 불가할 수 있습니다.                    |
| 모든 앱이 되는가                                         | 아닙니다. 사용자 문서는 요금제 사용이 되는 앱과 로그인만 되는 앱을 따로 나열합니다.[^learn]                                            |
| 앱이 내 대화 내용을 볼 수 있는가                         | 요금제 사용 권한은 ChatGPT 대화나 메모리에 대한 접근을 주지 않는다고 합니다.[^learn]                                                   |
| 앱이 내 API 키를 받는가                                  | 요금제 사용은 사용자의 API 키나 대화에 대한 접근을 주지 않습니다.                                                                      |

이 문서에서 확인하지 못한 것은 맨 아래 “문서가 말하지 않는 것”에 따로
적었습니다.

## 이 기능이 하는 일

Sign in with ChatGPT는 사용자가 ChatGPT 계정으로 앱에 로그인하게 하고,
적격이면 그 요금제로 AI 요청을 처리하게도 하는 OpenAI의 기능입니다.
기능은 두 층입니다.

| 층                  | 무엇을 주는가                                    | 요청하는 범위(scope)                                       |
| ------------------- | ------------------------------------------------ | ---------------------------------------------------------- |
| 신원(identity)      | 안정적인 계정 식별자와 이름, 이메일, 프로필 사진 | `openid profile email`                                     |
| ChatGPT 요금제 사용 | 앱이 사용자의 요금제로 Responses API 요청을 처리 | `offline_access resource.invoke chatgpt.tokens.use.direct` |

신원 범위는 ChatGPT 대화나 OpenAI API 자원에 대한 접근을 주지 않습니다.
요금제 사용은 별도의 Responses API 범위이며 사용자가 직접 승인해야 합니다.
이 범위도 사용자의 API 키나 대화에 대한 접근을 주지 않습니다.

통합 방식은 세 가지입니다.

| 통합                              | 설명                                                                                    | 상태                                                   |
| --------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| 웹사이트                          | OAuth 2.0 인증 코드 흐름(PKCE)과 OpenID Connect로 `Continue with ChatGPT` 로그인을 추가 | 선택된 상업 파트너 대상 제한 시험                      |
| ChatGPT 플러그인                  | 플러그인 커넥터의 인증 흐름에서 로그인을 재사용                                         | 선택된 상업 파트너 대상 제한 시험                      |
| 오픈소스 앱의 ChatGPT 요금제 사용 | 사용자가 API 키 없이 자기 요금제로 도구의 AI 요청을 처리                                | 모든 오픈소스 파트너와 선택된 비공개 클라이언트에 열림 |

## 누가 쓸 수 있는가

### 개발자

- 문서는 현재 Sign in with ChatGPT가 선택된 상업 파트너에게 제한 시험으로 제공된다고 말합니다. 클라이언트 ID 요청 페이지는 대기 명단 신청서를 안내합니다.
- ChatGPT 요금제 사용은 모든 오픈소스 파트너와 선택된 비공개 클라이언트에게 열려 있습니다.
- 오픈소스 흐름은 클라이언트 비밀(client secret)이나 파트너 API 키 없이 동작하고, 클라이언트는 동적 등록으로 만들어집니다. 그래서 클라이언트 ID를 따로 신청하지 않아도 시도할 수 있습니다.
- 유료이거나 원격으로 호스팅하는 앱에서 요금제 사용을 제공하려면 문서가 안내하는 관심 양식을 제출하라고 합니다.

### 사용자

사용자 문서가 읽은 시점에 나열한 파트너는 다음과 같습니다.[^learn]

| 분류                  | 앱                                                                                                                         |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 요금제 사용이 되는 앱 | Amp Code, Conductor, Dactyl, Devin, Hermes Agent, Hyperagent, Kilo Code, Lovable(출시 예정), Notion, Vercel, Vorflux, Warp |
| 로그인만 되는 앱      | Airtable, Canva, GitLab, HubSpot, Supabase                                                                                 |
| 오픈소스 통합         | OpenClaw, OpenCode, Pi, T3                                                                                                 |

로그인만 되는 앱은 ChatGPT 요금제를 쓰지 않습니다.
같은 이름이 DevDay 정리 문서에서는 16개 파트너로 소개되어 있어 숫자가 다릅니다.
어느 쪽이 맞는지는 이 문서에서 확인하지 못했습니다.

## 사용자 쪽에서 일어나는 일

사용자 문서가 설명하는 흐름은 다음과 같습니다.[^learn]

1. 참여하는 앱에서 `Continue with ChatGPT`를 누릅니다.
2. 쓰려는 ChatGPT 계정으로 로그인합니다.
3. 앱이 요청하는 이름, 이메일, 프로필 사진을 검토하고 계속합니다. 같은 이메일로
이미 앱 계정이 있으면 앱의 안내에 따라 계정을 확인하고 연결합니다.
4. 요금제를 쓰는 앱이면 `Use your ChatGPT plan` 권한을 따로 보여 주고,
사용자가 허용 여부를 고릅니다. 문구는 “이 앱이 ChatGPT 요금제 한도에서 사용량을
소비하는 것을 허용”하는 취지입니다.

이미 다른 방식(예: Google)으로 가입한 사용자는 앱의 계정 또는 결제 설정에서
ChatGPT 항목을 찾아 연결할 수 있습니다.
앱이 새 로그인을 요구하는 구성이면 로그아웃했다가 ChatGPT로 다시 로그인하라고
안내해야 합니다.

### 사용량과 한도

사용자는 ChatGPT의 `Settings > Usage`에서 연결된 앱이 요금제를 어떻게
쓰는지 봅니다.
앱별로 `App limits`에서 주간 한도를 전체 주간 요금제 사용량의 퍼센트로 정합니다.
선택지는 10%에서 100%까지입니다.
앱의 한도는 상한이지 별도의 허용량이나 예약된 몫이 아닙니다.[^learn]

그 아래에는 한도를 넘긴 뒤에도 앱이 크레딧을 쓰게 할지 정하는 설정이 있습니다.
Plus 사용자는 5시간 사용 한도가 요금제를 쓰는 모든 앱(비공개와 오픈소스
클라이언트 포함)에서 공유되며, 앱마다 따로 허용량이 있는 것은 아니라고 합니다.
Pro 사용자에게는 5시간 한도가 적용되지 않습니다.

### 연결 해제

사용자는 ChatGPT의 `Settings > Security and login > Sign in with ChatGPT`에서
앱을 골라 `Disconnect`로 연결을 완전히 끊을 수 있습니다.[^learn]
개발자 문서는 사용자가 앱을 끊어도 OpenAI가 지금은 도구에 알려 주지 않는다고
말합니다.
도구는 요청이나 토큰 갱신에서 끊김이 확인되었을 때 사용자에게 다시 로그인하라고
해야 합니다.

HN 스레드에는 한 사용자가 자기 계정 사용량 화면에
구독 공유(subscription sharing) 항목이 생겼다고 쓴 댓글이 있습니다.[^jlamberts]
오류 코드 이름이 `subscription_sharing_*`인 것과 맞물리는 관찰입니다.

## 개발자 관점: 오픈소스 앱에 요금제 사용 붙이기

### 개념: 클라이언트와 에이전트 호스트

- **클라이언트(client)**: 사용자가 도구에 승인하는 OAuth 등록입니다. 동적 등록으로 발급된 `client_id`는 인증한 사용자와 등록 때 고른 워크스페이스에 묶이며, 보안 경계와 요금제 사용 설정을 식별합니다.
- **에이전트 호스트(agent host)**: 도구의 한 인스턴스가 도는 환경입니다. 노트북 설치나 자체 호스팅 VM이 그 예입니다. 무엇이 한 호스트인지와 수명이 언제 시작·끝나는지는 앱이 정합니다. 도구를 재시작하거나 다시 로그인한다고 새 호스트가 되지 않습니다.

한 클라이언트가 같은 사용자와 워크스페이스에서 호스트 여러 개를 가질 수
있습니다.
같은 사용자의 노트북과 자체 호스팅 VM은 같은 `client_id`로 요금제 사용 설정과
한도를 공유하면서 각자의 호스트 ID를 가집니다.

호스트 ID(`ext_agent_host_id`)는 첫 로그인 전에 만들어 저장해야 하고,
이메일이나 사용자 ID 같은 식별 값이 아니라 불투명한 값이어야 합니다.
호스트 ID는 인증 자격 증명이 아닙니다.

| 형식                                     | 안내                                                          |
| ---------------------------------------- | ------------------------------------------------------------- |
| `urn:ietf:params:oauth:jwk-thumbprint:…` | 형식을 고른다면 권장. 호스트의 공개 키에서 RFC 9278로 만든 값 |
| `urn:uuid:…`                             | 지원되는 대안. UUIDv4를 호스트당 한 번 만들어 저장            |
| `did:key:<key>`                          | `did:key`만 허용되고 다른 DID 방식은 쓰지 않음                |

공개 키에서 만든 호스트 ID는 지금은 식별자일 뿐이고,
OpenAI는 개인 키 소유를 검증하지 않습니다.

### 1단계: 계정을 고르고 호스트를 준비한다

처음 열 때 `Continue with ChatGPT` 버튼을 보여 주고,
이후 실행에서는 저장된 ChatGPT 계정을 고르거나 계정 또는 워크스페이스를
추가하게 합니다.
새 로그인 시도는 신원이 검증될 때까지 활성 계정과 분리해 둡니다.
호스트 ID를 첫 로그인 전에 정하고, 첫 등록에서는 앱의 실제 이름을
`agent_name_hint`로 일관되게 씁니다.

### 2단계: 인증을 시작한다

콜백 리스너를 먼저 띄우고, 시도마다 새 `state`, OIDC `nonce`,
PKCE 검증값을 만듭니다.
시스템 브라우저로 `https://auth.openai.com/api/accounts/authorize`를 열고 아래
매개변수를 보냅니다.

| 매개변수                                  | 값과 목적                                                                                                                |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `client_id`                               | 처음 등록은 `dynamic_agent_client`. 재인증은 등록 때 받은 발급 ID                                                        |
| `agent_name_hint`                         | 앱의 실제 이름. 최초 동적 등록 요청에만 넣고, 사용자가 승인 전에 고칠 수 있는 표시용 메타데이터                          |
| `ext_agent_host_id`                       | 필수. 호스트마다 다른 식별자                                                                                             |
| `id_token_hint`                           | 재인증 때 이전 로그인에서 보관한 ID 토큰. 만료되어도 되며 계정 식별용. 있으면 계정 선택 화면을 건너뜀                    |
| `login_hint`                              | 재인증 때 선택. 검증된 ID 토큰에서 저장한 이메일                                                                         |
| `response_type`                           | `code`                                                                                                                   |
| `redirect_uri`                            | 최초 등록부터 `127.0.0.1` 루프백, 예: `http://127.0.0.1:1455/auth/callback`. 포트만 바뀔 수 있고 `localhost`는 쓰지 않음 |
| `scope`                                   | 신원 `openid profile email`, 요금제 사용 `offline_access resource.invoke chatgpt.tokens.use.direct`                      |
| `resource`                                | `https://api.openai.com/v1`                                                                                              |
| `state`, `nonce`                          | 시도마다 새 무작위 값                                                                                                    |
| `code_challenge_method`, `code_challenge` | `S256`, 검증값의 SHA-256을 패딩 없는 base64url로 인코딩한 값                                                             |

재인증의 `redirect_uri`는 스킴, 호스트,
경로가 같아야 하며 `/callback`은 `/auth/callback`과 일치하지 않습니다.
한 인증 시도 안에서는 인증 요청과 코드 교환에 같은 URI를 보내야 합니다.
재인증에서 `id_token_hint` 없이 발급 ID를 쓰면 사용자는 계정 선택 화면만 보고
워크스페이스 선택이나 동의 화면은 보지 않습니다.
클라이언트는 등록된 워크스페이스에 계속 묶입니다.

### 3단계: 콜백을 처리하고 코드를 교환한다

콜백에 `error=access_denied`가 있으면 `state`를 확인하고 시도를 멈추며 코드를
교환하지 않습니다.
새 등록의 성공 콜백은 `code`, `state`, 발급된 `client_id`를 돌려주고 `scope`가
붙을 수 있습니다.

1. `state`를 대기 중인 시도와 대조하고 OAuth `error`를 먼저 처리합니다.
2. 새 등록이면 발급된 `client_id`(`oaiapp_…` 형태)를 보관합니다.
`dynamic_agent_client`를 연결의 발급 ID로 저장하면 안 됩니다. 새 등록 콜백에
발급 ID가 없으면 등록이 끝나지 않은 것입니다.
3. `https://auth.openai.com/api/accounts/oauth/token`에 form 인코딩한
`authorization_code` 요청을 보냅니다. 발급 `client_id`, `code`, `code_verifier`,
같은 `redirect_uri`, 같은 `resource`를 넣고 클라이언트 비밀은 필요 없습니다.

코드 교환이 `invalid_grant`를 돌려주면 그 코드를 버리고 새 인증을 시작합니다.

### 4단계: ID 토큰과 요금제 권한을 검증한다

- ID 토큰의 서명을 OpenAI가 공개한 JWKS로 검증하고, 발급자, 대상(audience, 발급 클라이언트 ID), 만료, 저장해 둔 nonce를 확인합니다.
- 검증된 `sub`를 계정 신원으로 씁니다. 이메일과 `sub`는 워크스페이스 식별자가 아니므로 발급 클라이언트 ID를 검증된 신원과 함께 보관해 등록을 분리합니다.
- 재인증이면 새 ID 토큰의 검증된 신원이 선택한 계정과 일치하는지 확인한 뒤에 자격 증명을 바꿉니다.
- 토큰 응답의 허용된 범위에 `chatgpt.tokens.use.direct`가 있는지 확인합니다. 유효한 ID 토큰만으로는 요금제 사용이 승인된 것이 아닙니다.

### 5단계: 자격 증명을 로컬 파일에 저장한다

발급 클라이언트 ID와 검증된 계정 신원마다 보호된 자격 증명 기록을 따로 둡니다.
문서의 예는 이메일, 발급자, `sub`, `client_id`, `ext_agent_host_id`,
ID·액세스·갱신 토큰, `token_type`, `expires_in`, 허용된 범위,
저장 시각을 담습니다.
ID 토큰은 다음 로그인에서 `id_token_hint`로 쓰려고 보관합니다.

파일은 `~/.config/YOUR_TOOL/` 같은 앱이 정한 경로에 원자적으로 쓰고 소유자 전용
권한(Unix의 `0600`)을 줍니다.
커밋하거나 로그에 남기지 않습니다.
갱신에 성공하면 액세스 토큰, 만료, 허용 범위,
회전하는 갱신 토큰을 함께 교체합니다.

### 6단계: 모델을 나열하고 Responses API를 호출한다

같은 액세스 토큰으로 선택한 계정의 모델 목록을 요청합니다.

```bash
curl --fail-with-body --silent --show-error \
  https://api.openai.com/v1/models \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  | jq '[.models[] | select(.visibility == "list") | {slug, display_name}]'
```

응답의 `models` 배열에서 `visibility: "list"`인 모델을 보여 주고
`display_name`을 표시하며 선택한 `slug`를 `model`로 넘깁니다.
사용자가 계정을 바꾸면 선택지를 새로 불러옵니다.

추론은 `POST https://api.openai.com/v1/responses`에 액세스 토큰을 베어러로 보내
수행합니다.
ChatGPT의 `backend-api` 엔드포인트를 쓰지 않습니다.
요청마다 `store`는 `false`, `stream`은 `true`로 두고 응답을 이벤트 스트림으로
읽습니다.

```bash
curl --no-buffer https://api.openai.com/v1/responses \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-6.1-sol",
    "input": [
      {
        "role": "user",
        "content": "Say exactly: Hello, world!"
      }
    ],
    "store": false,
    "stream": true
  }'
```

Python SDK에서는 `api_key`에 OAuth 액세스 토큰을 넣고 `base_url`을
`https://api.openai.com/v1`로 둡니다.

```python
import os

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["ACCESS_TOKEN"],  # OAuth token sent as Bearer.
    base_url="https://api.openai.com/v1",
    max_retries=0,
)

completed = False
with client.responses.create(
    model="gpt-6.1-sol",
    input=[{"role": "user", "content": "Say exactly: Hello, world!"}],
    store=False,
    stream=True,
) as stream:
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
        elif event.type == "response.failed":
            error = event.response.error
            code = error.code if error else "unknown_error"
            raise RuntimeError(f"Response failed: {code}")
        elif event.type == "response.completed":
            completed = True

if not completed:
    raise RuntimeError("Stream ended without response.completed.")
print()
```

추론은 `response.completed`를 받은 뒤에야 성공입니다.
사용량 한도 오류는 스트림이 시작된 뒤에도 `response.failed`로 올 수 있고,
`response.incomplete`, 명시적 오류, 끊긴 스트림은 따로 처리해야 합니다.

## 토큰과 세션

| 항목                | 값                                                                                                      |
| ------------------- | ------------------------------------------------------------------------------------------------------- |
| 액세스 토큰         | 1시간(`expires_in: 3600`)                                                                               |
| 갱신 토큰           | 30일. 갱신할 때마다 새 갱신 토큰이 30일 수명으로 발급되고 연속 교체 횟수에 고정 한도가 없음             |
| 응답 필드           | `access_token`, `refresh_token`, `id_token`, `token_type`, `expires_in`, `scope`, `earliest_refresh_at` |
| 갱신 토큰 발급 조건 | `offline_access` 승인                                                                                   |

액세스 토큰의 주요 클레임은 `sub`, `aud`(`https://api.openai.com/v1`),
`client_id`, `scope`, `iss`, `iat`, `exp`, `jti`, `nbf`,
그리고 불투명한 인증 메타데이터(`https://api.openai.com/auth`)입니다.
메타데이터는 해석하지 말고 불투명하게 다루라고 합니다.

### 갱신

액세스 토큰이 만료되기 전에 `https://auth.openai.com/api/accounts/oauth/token`에
form 인코딩으로 `grant_type=refresh_token`,
이 토큰 세트와 함께 저장한 발급 `client_id`(`dynamic_agent_client`가 아님),
저장한 `refresh_token`, `resource=https://api.openai.com/v1`을 보냅니다.
`scope`는 생략해 기존 허용을 유지합니다.
회전하는 토큰을 두 프로세스가 경쟁하지 않게 같은 세션의 갱신은 직렬화하고 최신
교체 토큰을 저장합니다.

### 로그아웃

로그아웃 때는 `https://auth.openai.com/.well-known/openid-configuration`의
`revocation_endpoint`로 갱신 토큰을 폐기합니다.
`token`, `token_type_hint=refresh_token`, 발급 `client_id`를 form으로 POST하고,
빈 HTTP `200`이 성공이며 이미 무효인 토큰에도 같습니다.
네트워크 실패나 `5xx`는 백오프로 재시도하고,
폐기를 확인하지 못한 채 로컬 로그아웃을 마치면 토큰을 지우고 원격 폐기가
확인되지 않았다고 사용자에게 알립니다.
이 폐기는 등록된 클라이언트를 지우지 않습니다.

### 자격 증명 보안

- 액세스, 갱신, ID 토큰은 보호된 로컬 또는 자체 호스팅 저장소에 둡니다. 브라우저 저장소, 소스 관리, 로그, 분석, 지원 기록에는 넣지 않습니다.
- 토큰을 URL에 넣지 않습니다. `id_token_hint`는 OpenAI 인증 엔드포인트에만 보내고, 이 힌트가 든 인증 URL은 로그와 진단에서 가립니다.
- 자격 증명이 유출되면 사용자에게 ChatGPT 설정에서 앱을 끊으라고 안내합니다.

### 여러 계정

각 등록의 기본 계정 정보, 발급 클라이언트 ID,
자격 증명을 분리해 보관합니다. 이메일이 같아도 마찬가지입니다.
계정마다 구별되는 안정적 라벨을 쓰고 활성 계정을 설정이나 메뉴에 표시합니다.
다른 등록의 자격 증명을 덮어쓰거나, 한 등록의 클라이언트 ID와 다른 등록의 토큰을
섞어 쓰지 않습니다.

저장된 계정으로 계속하려면 그 계정의 발급 `client_id`와 새 state, nonce,
PKCE로 OAuth를 반복하고 호스트 ID를 유지합니다.
이때 `agent_name_hint`는 빼고 저장해 둔 `id_token_hint`와 `login_hint`를
보냅니다.
다른 계정을 쓰려면 기존 등록을 고르거나 `client_id=dynamic_agent_client`로 새로
등록합니다.

## Codex app-server로 쓰기

앱이 Codex app-server를 쓴다면 사용자의 ChatGPT 요금제에 대해 승인된 OAuth
액세스 토큰으로 Responses API에 추론 요청을 보내도록 설정합니다.
별도의 Codex 로그인은 필요 없습니다.

1. 코드 교환 뒤 토큰 응답의 `access_token`을 app-server 자식 프로세스 환경 변수
`ACCESS_TOKEN`에 넣습니다.
2. Responses 제공자를 지정해 시작합니다.

```bash
codex app-server --listen stdio:// \
  -c 'model_provider="openai_chatgpt_plan"' \
  -c 'model_providers.openai_chatgpt_plan.name="ChatGPT plan"' \
  -c 'model_providers.openai_chatgpt_plan.base_url="https://api.openai.com/v1"' \
  -c 'model_providers.openai_chatgpt_plan.env_key="ACCESS_TOKEN"' \
  -c 'model_providers.openai_chatgpt_plan.wire_api="responses"' \
  -c 'model_providers.openai_chatgpt_plan.requires_openai_auth=false' \
  -c 'model_providers.openai_chatgpt_plan.supports_websockets=false'
```

3. stdin과 stdout으로 줄 단위 JSON 메시지를 주고받습니다. `initialize`의
`params.clientInfo`에 `name`(앱의 안정적 식별자), `title`, `version`을 넣고,
이름은 새 등록 때 보낸 `agent_name_hint`와 맞춰야 합니다. `initialized`,
`thread/start`(모델 선택), `turn/start`를 차례로 보내고
`item/agentMessage/delta`를 표시합니다. `turn/completed`의 `turn.status`가
`completed`일 때만 성공입니다.
4. 토큰 갱신은 앱이 맡습니다. 새 액세스 토큰을 얻으면 app-server를 새
`ACCESS_TOKEN`으로 다시 시작하고 `thread/resume`에 저장한 스레드 ID를 넘깁니다.

`model/list`는 번들된 클라이언트 카탈로그를 돌려줄 수 있으므로 자격 확인이
아니라 카탈로그로 다루고, 추론 한 턴이 성공했는지가 그 요청에서 모델 접근이
되는지를 확인해 줍니다.
계정별 최신 모델 선택지가 필요하면 위의 `/v1/models` 요청을 씁니다.

## 지금의 제한(프리뷰)

요금제 사용 흐름은 `https://api.openai.com/v1`에서 직접 또는 Codex app-server를
거쳐 쓸 때 다음이 적용됩니다.

- **필수 설정**: HTTP 요청은 `store: false`, `stream: true`. `input`은 요청마다 필요한 맥락을 담은 배열이며 `instructions`나 개발자 메시지를 쓰고, 명시적인 `{type: "message", role: "system"}` 항목은 거부됩니다.
- **지원하지 않는 필드**: `background`, `conversation`, `max_output_tokens`, `max_tool_calls`, `metadata`, `moderation`, `multi_agent`, `prompt`, `prompt_cache_retention`, `safety_identifier`, `temperature`, `top_logprobs`, `top_p`, `truncation`, `user`.
- **대화 상태**: HTTP에서는 `previous_response_id`를 쓰지 않고 필요한 이력을 `input`에 보냅니다. WebSocket 이어가기는 같은 인증된 연결의 응답만 참조하며 영속 저장소가 아닙니다.
- **지원 도구**: 함수·커스텀 도구는 네임스페이스로 묶거나 `additional_tools` 입력 항목으로 제공합니다. 웹 검색은 모델과 계정·워크스페이스 정책에 따릅니다.
- **지원하지 않는 도구**: 이미지 생성, 파일 검색, Code Interpreter, 네이티브 컴퓨터 사용, 호스팅 MCP·커넥터, Responses `tool_search`.
- **입력**: 텍스트, 이미지, 파일은 모델이 받는 경우 지원합니다. 오디오·비디오 입력, Files 업로드 API, 전사 API는 지원하지 않습니다.
- **Codex app-server**: stdio로 앱과 통신하고 Responses로는 HTTP/SSE를 씁니다. Codex가 셸과 MCP 도구, 자식 에이전트를 로컬에서 돌리는 것은 가능하지만, `tool_search`를 내보내는 구성은 실패합니다.

## 오류와 복구

요금제 사용 오류는 추론을 멈추며, OpenAI는 요청을 조용히 다른 결제 경로로 돌리지
않습니다.
실제 HTTP 상태, 응답 본문 형태, 오류 코드, 요청 ID를 보존합니다.

### 요금제 사용이 켜져 있지 않을 때

동의가 거절되었거나 OAuth 결과에 요금제 사용 권한이 없는 경우입니다.
이 경로에서는 추론으로 진행하지 않습니다.
유효한 ID 토큰은 있으나 `chatgpt.tokens.use.direct`가 없으면 로그인은 유지하되
요금제 사용을 꺼진 것으로 표시하고, 요금제 사용을 켜거나 사용자 자신의 API 키
같은 다른 결제 경로를 설정하는 선택지를 줍니다.
사용자가 설정에서 명시적으로 켜면 저장된 클라이언트 ID와 전체
범위(`chatgpt.tokens.use.direct` 포함)로 OAuth를 반복합니다.
평소 로그인에서 매번 동의를 강제하지 않습니다.

### 스트림이 열리기 전

직접 경로의 승인 실패는 표준 `error` 객체가 아니라 `{"detail":"..."}` 같은
본문일 수 있고 이 메시지는 안정적인 기계 코드가 아닙니다.

| 상태  | 복구                                                                                  |
| ----- | ------------------------------------------------------------------------------------- |
| `401` | 서명된 신원이나 직접 권한이 받아들여지지 않음. 선택한 ChatGPT 계정과 허용된 범위 확인 |
| `403` | 허용된 서비스 지역 같은 정책·권한 검사가 막음. 제한을 보여 주고 통합 확인             |
| `503` | 직접 라우팅이 불가하거나 꺼져 있음. 자격 증명을 보존하고 일시적이면 제한된 백오프     |

### 구조화된 Responses 오류

| 코드                                                                            | 상태 | 할 일                                                                                                                                             |
| ------------------------------------------------------------------------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `subscription_sharing_user_not_eligible`                                        | 403  | 선택한 사용자·워크스페이스·정책에서 요금제 사용이 불가. 제한을 설명하고 같은 요청이나 OAuth를 반복하지 않음                                       |
| `subscription_sharing_usage_limit_exceeded`                                     | 429  | 요금제를 쓰는 새 요청을 멈추고 ChatGPT 설정의 사용량 페이지로 안내. 요금제가 비었다고 단정하거나 초기화 시각을 추정하지 않음(앱별 한도일 수 있음) |
| `subscription_sharing_usage_unavailable`                                        | 503  | 사용량을 확인하지 못함. 자격 증명을 보존하고 나중에 백오프로 재시도                                                                               |
| `subscription_sharing_unsupported_capability`                                   | 400  | `error.param`을 보고 지원되지 않는 입력, 도구, 실행 기능, 모델, 서비스 등급 재정의를 제거. 같은 본문을 재시도하지 않음                            |
| `subscription_sharing_route_not_supported`                                      | 403  | HTTP 메서드와 엔드포인트 확인. 예시는 `POST /v1/responses`                                                                                        |
| `subscription_sharing_invalid_user`                                             | 401  | 구독자 맥락을 검증하지 못함. 요청 ID를 보존하고 확인된 폐기나 갱신 종결 오류 뒤에 다시 로그인하게 함                                              |
| `chatpass_v2_scope_not_authorized`, `chatpass_v2_invalid_authorization_context` | 403  | 서명된 권한 맥락이 작업을 허용하지 않음. 재시도나 결제 변경이 아니라 클라이언트와 허용 구성을 확인                                                |
| `subscription_sharing_user_unavailable`                                         | 503  | 사용자·워크스페이스 정보를 일시적으로 얻지 못함. 자격 증명 보존 후 백오프                                                                         |

### 갱신 오류

- 갱신 토큰을 쓸 수 없는 경우: 갱신의 `invalid_grant`, `invalid_refresh_token`, `token_expired`, `refresh_token_expired`, `refresh_token_invalidated`, `refresh_token_reused`. 쓸 수 없는 토큰을 지우고 저장된 발급 클라이언트 ID로 OAuth를 반복합니다.
- 클라이언트가 잘못된 경우: `invalid_client`. 클라이언트 구성을 고칩니다.

일시적 네트워크나 인프라 실패만으로 자격 증명을 지우지 않습니다.

## 자체 호스팅 VM에서 쓰기

원격 VM에서 오픈소스 앱을 돌린다면 절차는 다음과 같습니다.

1. VM의 안정적인 `ext_agent_host_id`를 만들어 저장합니다.
2. `127.0.0.1` 콜백은 브라우저가 있는 컴퓨터에 닿지 VM에는 닿지 않으므로,
OAuth는 같은 도구와 클라이언트로 같은 사용자·워크스페이스에 대해 로컬에서
끝냅니다.
3. 선택한 등록의 보호된 자격 증명 파일(발급 `client_id`, 액세스·갱신 토큰,
보관한 `id_token` 등)을 SSH 같은 안전한 경로로 도구의 문서화된 VM 경로에
옮깁니다. 가져올 때 노트북의 호스트 ID가 VM의 것을 덮어쓰지 않게 합니다.
4. 이후 갱신은 VM이 맡고 다음 인증에는 VM 자신의 호스트 ID를 씁니다.

이 절차는 기존 자격 증명 세션을 옮기는 것이며,
옮긴 세션에 대한 호스트별 사용량 귀속과 요금제 접근 폐기는 아직 제공되지
않는다고 문서가 밝힙니다.

## 웹사이트 로그인(신원 전용)

웹사이트 통합은 사용자 식별만 다루며 요금제 사용은 포함하지 않습니다.
백엔드가 인증 코드를 교환하고 OpenAI ID 토큰을 검증하며,
검증된 발급자·클라이언트 ID·`sub`를 앱 계정에 연결하고 자체 세션을 만듭니다.

필요한 것은 `oaiapp_`로 시작하는 OpenAI 클라이언트 ID,
환경마다 정확히 등록된 콜백 URL, 발급자와 인증·토큰·JWKS 엔드포인트,
등록된 토큰 엔드포인트 인증 방식(기밀 클라이언트면 비밀),
짧은 수명의 트랜잭션 상태를 보관하고 안전한 세션을 만들 백엔드입니다.
엔드포인트는 `https://auth.openai.com/.well-known/openid-configuration`의 발견
문서에서 읽으며, 문서가 든 프로덕션 값은 다음과 같습니다.

```text
Issuer: https://auth.openai.com
Authorization endpoint: https://auth.openai.com/api/accounts/authorize
Token endpoint: https://auth.openai.com/api/accounts/oauth/token
JWKS URI: https://auth.openai.com/.well-known/jwks.json
```

1. **버튼 추가**: `Continue with ChatGPT`나 `Sign in with ChatGPT` 문구,
흑백 네 가지 형식 중 하나를 쓰고 `data-oai-siwc-button` 속성을 클릭 요소에 붙여
OpenAI가 통합을 확인하고 문제를 추적하게 합니다.
2. **일회성 트랜잭션**: 백엔드에서 `state`, PKCE 검증값과 S256 챌린지,
`nonce`를 만들고 서버가 만든 브라우저 세션 식별자에 묶습니다. 문서의 예는 10분
뒤 만료시키고 식별자는 `HttpOnly`, `Secure`, `SameSite=Lax` 쿠키에 둡니다.
3. **OpenAI로 리디렉션**: 범위는 `openid profile email`이며,
선택 매개변수 `ext_device_token`, `ext_login_session_id`,
`ext_login_started_at_ms`로 로그인 시도를 로그와 맞춰 문제를 조사할 수
있게 합니다.
4. **콜백과 state 확인**, 5. **코드 교환**,
6. **ID 토큰 검증**(`jose` 같은 라이브러리로 서명, 발급자, 대상, 만료, nonce),
7. **로컬 계정 찾기·만들기·연결**, 8. **앱 세션 만들기** 순서입니다.

계정 연결 정책은 문서가 명시합니다.
OpenAI `sub`가 이미 연결되어 있으면 그 계정으로 로그인하고,
로그인한 사용자가 ChatGPT를 추가하거나 이메일이 기존 계정과 같으면 확인 후
연결하며, 이메일 일치만으로는 계정 소유의 증거가 아니라고 합니다.
계정이 없으면 제품, 온보딩, 기업 정책에 따라 생성을 허용합니다.
세션에는 발급자, 클라이언트 ID, `sub`, 있으면 `sid`를 함께 저장해 보안 알림 때
영향받는 세션을 찾게 합니다.
ID 토큰, PKCE 검증값, 인증 코드, 클라이언트 비밀을 브라우저 JavaScript에
돌려주지 않습니다.

### 계정 보안 알림(Back-Channel Logout)

OpenAI는 OIDC Back-Channel Logout으로 서명된 Logout Token을 앱 백엔드에 보내
사용자 또는 세션 로그아웃을 요청할 수 있고,
앱은 토큰을 검증해 해당 세션을 끝내야 합니다.

| 범위            | 클레임              | 끝낼 세션                              |
| --------------- | ------------------- | -------------------------------------- |
| 사용자 로그아웃 | `sub`, `sid` 없음   | 모든 브라우저·기기의 그 사용자 앱 세션 |
| 세션 로그아웃   | `sid`, 선택적 `sub` | 그 `sid`와 연결된 세션만               |

공개 HTTPS 엔드포인트가 `logout_token` form 필드로 POST를 받아야 하고 브라우저
로그인이나 리디렉션 없이 받아야 합니다.
서명, 발급자, 대상, 만료, 로그아웃 이벤트를 검증한 뒤 세션과 이를 갱신할 수 있는
자격 증명을 폐기합니다.
토큰의 최대 수명은 120초이고 `jti`로 재전송을 탐지합니다.
이 토큰은 세션을 끝내라는 지시일 뿐 로그인이나 계정 데이터 접근에는 쓸 수 없고,
`nonce`, 이메일, 대화 내용, 보안 조치 사유를 담지 않습니다.
알 수 없는 `sid`가 사용자 로그아웃을 일으키면 안 됩니다.

엔드포인트는 OpenAI Platform의 `OAuth apps`에서 클라이언트를 골라
`Security notifications`에 등록하고 `Enable automatic logout`을 켭니다.
`Test endpoint`는 `sub`에 `test-`를 붙여 서명된 토큰을 보내며,
실제 사용자 로그아웃을 시험하려면 테스트 알림일 때만 그 접두사를 떼야 합니다.

## ChatGPT 플러그인 안에서의 로그인

플러그인 통합에는 서로 독립된 OAuth 트랜잭션이 둘 있습니다.

| 트랜잭션            | OAuth 클라이언트 | 인증 서버 | 결과                                  |
| ------------------- | ---------------- | --------- | ------------------------------------- |
| 바깥: 플러그인 연결 | ChatGPT          | 내 앱     | 내 커넥터 인증 코드를 ChatGPT에 반환  |
| 안쪽: 사용자 로그인 | 내 앱            | OpenAI    | OpenAI 인증 코드를 백엔드가 교환·검증 |

ChatGPT가 `target_flow=chatgpt_siwc`와 `login_hint`(사용자 이메일)를 담은 인증
요청을 앱에 보내면, 앱은 등록된 클라이언트, 정확한 리디렉션 URI, 지원 범위,
바깥 PKCE 챌린지를 검증하고 바깥 트랜잭션을 저장한 뒤 안쪽에서 웹사이트 로그인
흐름을 새 state, PKCE, nonce로 수행합니다.
이어서 ID 토큰을 검증하고 로컬 계정을 정한 뒤 단기·일회용으로 원 요청에 묶인
커넥터 인증 코드를 돌려줍니다.
두 트랜잭션의 state, PKCE, 콜백, 코드, 자격 증명은 섞지 않습니다.
`login_hint`는 신원을 검증하지 않으므로 힌트와 활성 세션이 다르면 사용자가
고르게 하고, 이메일이나 기업 도메인에 계정이 있는지 구분되는 오류로 드러내지
않습니다.

## UI/UX 지침

- 로그인 동작 이름은 `Continue with ChatGPT`로 하고, 다른 로그인 옵션과 비슷한 시각적 비중으로 두며 승인된 OpenAI 브랜딩을 씁니다.
- 처음 요금제 사용이 켜진 로그인 때만 환영 모달을 한 번 보여 주고, `You're using your ChatGPT plan`과 `Got it`으로 확인받습니다.
- 온보딩이나 결제 화면과 설정에 요금제 사용 옵션을 두고, 앱 자체 구독이나 요금과 구분해 설명합니다.
- 사용량 페이지에는 사용량 요약 근처에 `Manage usage` 링크를 두고 ChatGPT 사용량 설정으로 연결합니다.
- 요청이 사용자의 요금제를 쓰는 동안 입력창이나 모델 선택기 근처에 `Using ChatGPT plan`과 `Manage usage` 링크를 표시합니다.
- 사용량 한도 오류가 오면 `Manage usage`를 주된 동작으로 하고, 앱 자체 크레딧이 있으면 구매를 보조 동작으로 둡니다. 한도는 요금제 한도일 수도 앱별 한도일 수도 있습니다.
- 다른 방식으로 가입한 기존 사용자에게는 배너로 알립니다.
- 앱의 가격 또는 플랜 비교 페이지에 어느 플랜이 ChatGPT 요금제 사용을 지원하는지 명시해야 합니다. 지원 플랜의 기능 목록에 `Use your ChatGPT plan`을 넣고 `Learn more`는 OpenAI 도움말로 연결합니다.

## 직접 시험해 보기: DevKit과 Paste Perfect

OpenAI는 사용자의 컴퓨터에서 도는 오픈소스 앱을 만드는 개발자를 위해 DevKit
저장소를 공개했습니다.
Node.js SDK와 React 컴포넌트, 디자인 자산,
예제 앱 Paste Perfect를 담고 있습니다.[^devkit]

| 폴더                         | 내용                                                                                  |
| ---------------------------- | ------------------------------------------------------------------------------------- |
| `packages/local`             | OAuth, 자격 증명 저장, 계정 프로필, 모델 탐색, 스트리밍 Responses                     |
| `packages/react`             | 로그인, 연결 상태, 요금제 사용 컴포넌트                                               |
| `assets`                     | ChatGPT 마크, 아이콘, 로그인 버튼, 글꼴                                               |
| `examples/component-gallery` | 로그인, 계정 연결, 요금제 사용 제어의 디자인 예                                       |
| `examples/paste-perfect`     | 복사한 텍스트를 변환해 다른 앱에 붙여 넣는 macOS 예제 앱(Electron 설정 대시보드 포함) |

Paste Perfect는 macOS 14 이상, Node.js 22.12 이상,
Xcode Command Line Tools가 필요하다고 합니다.[^devkit]

```sh
git clone https://github.com/openai/sign-in-with-chatgpt-devkit.git
cd sign-in-with-chatgpt-devkit
npm ci
npm run build
npm start
```

대시보드에서 ChatGPT로 로그인하고, 네이티브 붙여넣기를 켜 Accessibility 권한을
주면 됩니다.
복사한 텍스트에서 단축키 `⌘⇧Space`를 누르고 8초 안에 오른쪽 클릭하면
Spreadsheet, Message, Translate, Checklist,
Clean up 같은 변환을 고를 수 있습니다.[^devkit]
`@siwc/local`은 로컬 Node.js 프로세스의 로그인과 API 요청에,
`@siwc/react`는 UI에 쓰며 `@siwc/react/styles.css`를 한 번 가져옵니다.[^devkit]
OpenAI가 작성한 코드와 문서는 Sign-in with ChatGPT DevKit Noncommercial License
v1.0으로 제공됩니다.[^devkit]

쿡북은 이 예를 친구에게 앱을 나눠 줄 때 API 키 설정과 결제 등록,
사용료 부담이라는 마찰을 없애는 방법으로 소개하며,
적격 Plus·Pro 친구가 앱을 내려받아 로그인하고 자기 요금제 허용량으로 문장
다듬기를 쓰는 장면을 설명합니다.[^cookbook]

## 문서가 말하지 않는 것

이 문서가 읽은 범위에서 확인하지 못한 것입니다.

- **파트너의 비용**: 앱 쪽이 OpenAI에 무엇을 내거나 내지 않는지는 읽은 문서에 없습니다. 사용자 문서는 앱이 자체 요금을 받을 수 있다는 점만 밝힙니다.
- **정확한 한도 수치**: Plus와 Pro의 사용량이 토큰 몇 개에 해당하는지, 앱 한도 10~100%가 구체적으로 얼마인지는 없습니다.
- **크레딧의 단가**: 요금제 한도를 넘긴 뒤 크레딧으로 처리될 때의 비용은 없습니다.
- **적격 요금제의 범위**: 문서는 Plus와 Pro를 말하지만 Team, Enterprise, 무료 요금제의 취급은 읽은 범위에서 확인하지 못했습니다.
- **파트너 수**: 사용자 문서의 나열(요금제 사용 12개와 출시 예정 1개)과 DevDay 정리 문서의 16개가 다릅니다.
- **헬프 센터**: OpenAI 헬프 센터의 Sign in with ChatGPT 글은 접속이 차단되어 열지 못했습니다.
- **프리뷰**: 문서가 제한을 프리뷰 동작으로 부르므로 필드와 도구 지원이 바뀔 수 있습니다.

## 함정

- **`dynamic_agent_client`를 저장하는 실수**: 처음 등록의 진입점일 뿐이며, 저장하고 교환·갱신에 쓸 값은 콜백이 돌려준 발급 ID입니다.
- **`localhost` 사용**: 루프백은 `127.0.0.1`이고 포트만 바뀔 수 있습니다.
- **ID 토큰만 믿기**: ID 토큰이 유효해도 `chatgpt.tokens.use.direct`가 없으면 요금제 사용은 승인되지 않은 것입니다.
- **필드와 도구**: `temperature`나 `max_output_tokens` 같은 필드, 호스팅 MCP나 파일 검색 도구를 넣으면 `subscription_sharing_unsupported_capability`가 날 수 있습니다.
- **`store: true`나 `stream: false`**: 요금제 사용 흐름은 `store: false`, `stream: true`를 요구합니다.
- **갱신 경쟁**: 회전하는 갱신 토큰을 두 프로세스가 동시에 쓰면 한쪽이 `refresh_token_reused`를 만날 수 있어 갱신을 직렬화해야 합니다.
- **호스트 ID 덮어쓰기**: 자격 증명을 VM으로 옮길 때 노트북의 호스트 ID가 VM의 것을 덮으면 안 됩니다.
- **조용한 결제 전환 기대**: 요금제 사용이 막혀도 OpenAI가 다른 결제 경로로 돌리지 않으므로 앱이 다른 결제 방식 선택지를 줘야 합니다.
- **한도 해석**: `subscription_sharing_usage_limit_exceeded`는 요금제 전체가 비었다는 뜻이 아닐 수 있습니다. 앱별 한도일 수 있습니다.

## 기억할 원칙

- 로그인과 요금제 사용은 별개의 권한입니다. 로그인만 되는 앱도 있습니다.
- 사용량은 사용자의 기존 요금제 한도에서 나가며 새 허용량이 생기지 않습니다. 앱은 자체 요금을 받을 수 있습니다.
- 사용자는 앱별 한도(10~100%)를 정하고, 한도 초과 뒤 크레딧 사용 여부를 고르고, 언제든 연결을 끊을 수 있습니다.
- 앱은 사용자의 API 키나 ChatGPT 대화를 받지 않습니다.
- 개발자는 `client_id`, 호스트 ID, 토큰을 계정별로 분리해 저장하고, 요금제 권한은 허용된 범위로 확인합니다.
- 요금제 사용은 `POST /v1/responses`, `store: false`, `stream: true`, 일부 필드와 도구 제한 안에서만 쓸 수 있습니다.
- 시험해 보려면 오픈소스 앱 경로가 가장 열려 있고, DevKit의 Paste Perfect가 출발점입니다.

## 관련 문서

- [OpenAI DevDay 2026 정리](devday-2026.md)
- [Simon Willison의 DevDay 2026 정리](devday-2026-willison.md)
- [openai-oauth - ChatGPT 계정으로 OpenAI API를 무료 사용하는 비공식 도구](openai-oauth.md)

---

[^learn]: OpenAI, [Sign in with ChatGPT](https://learn.chatgpt.com/docs/sign-in-with-chatgpt)

[^cookbook]: OpenAI Cookbook, [Sign in with ChatGPT](https://developers.openai.com/cookbook/articles/sign-in-with-chatgpt)

[^devkit]: GitHub, [openai/sign-in-with-chatgpt-devkit](https://github.com/openai/sign-in-with-chatgpt-devkit)

[^jlamberts]: <https://news.ycombinator.com/item?id=49897966>
