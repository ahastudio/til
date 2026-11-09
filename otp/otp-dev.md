# OTP.dev: 채널 하나를 고르는 OTP 발송·검증 API

<https://otp.dev/>

## 소개

OTP.dev는 일회용 비밀번호(OTP)를 대신 만들어 보내고,
사용자가 입력한 코드를 대신 확인해 주는 API 서비스다.
홈페이지 제목은 “OTP verification API”이고,
첫 문구는 “Multi-Channel User Verification. Simplified.”다.
SMS, WhatsApp, Telegram, Viber, FlashCalls, Voice OTP,
Email의 일곱 채널을 하나의 API로 쓸 수 있다고 소개한다.
문서 소개 페이지는 “거의 코드 없이” 다채널 OTP를 만들 수 있고,
재시도나 여러 채널 로직을 걱정할 필요가 없다고 적는다.

홈페이지가 내세우는 장점은 세 가지다.
Telegram이나 Email처럼 싼 채널을 먼저 쓰고 SMS로 넘어가
비용을 줄이고(Smart Cost Control),
실시간 로그로 AIT와 봇 공격을 일찍 알아채며(Traffic Monitoring),
직접 라우팅으로 빨리 도착한다(Reliable Delivery).
“cURL에서 프로덕션까지 15분 이내”,
“엔드포인트와 API 키만 바꾸면 되는 드롭인 대체재”라는 문구도 있다.

운영 주체는 이용약관에 나온다.
서비스 제공자는 아랍에미리트 법으로 설립된
NEXTID SOFTWARE SOLUTIONS – FZCO(등록번호 63041, 두바이 실리콘 오아시스)다.
그런데 약관의 준거법은 에스토니아 법이고,
분쟁 관할은 에스토니아 하르유 지방법원이며, 법적 통지는 탈린 주소로 받는다.
약관의 마지막 갱신은 2025년 7월, 스팸 방지 정책은 2022년 11월이다.

블로그를 보면 이 서비스의 전신은 GetOTP다.
GetOTP WordPress 플러그인, 임베드 모드, reCAPTCHA 지원을 알리는 글이
같은 블로그에 남아 있다.
LaLoka Labs라는 회사가 Founder Institute 에스토니아 지부와 협력한다는 글에는
“Stripe가 결제를 대신하듯 OTP.dev가 일회용 비밀번호를 대신한다”는 설명이 있다.
다만 그 글의 제목은 회사 이름 자리가 “mycompany”로 바뀌어 있어,
이름을 바꾸는 과정에서 일괄 치환이 남긴 흔적으로 보인다.
에스토니아 준거법은 이 LaLoka Labs 시절에서 이어진 것으로 보이지만,
약관이 그 이유를 밝히지는 않는다.

## 동작 방식

### 발송과 검증은 같은 경로를 쓴다

발송은 `POST https://api.otp.dev/v1/verifications` 하나다.
인증은 `X-OTP-Key` 헤더에 API 키를 넣는다.
문서는 이것을 “Basic HTTP verification method”라고 부르지만,
실제 예제는 HTTP Basic 인증이 아니라 사용자 정의 헤더를 쓴다.

요청 본문은 `data` 객체 하나이고, 채널은 `channel` 필드 하나로 고른다.
문서에 페이지가 있는 채널은 SMS, Viber, Voice, Telegram 넷이다.
홈페이지와 가격표에 있는 WhatsApp과 Email은 API 문서에 페이지가 없다.
FlashCalls는 별도 채널이 아니라 Voice 채널의 `voice_type: "flash"`로 들어간다.

| 채널     | 필수 필드                             | 코드 길이 | 채널별 옵션                              |
| -------- | ------------------------------------- | --------- | ---------------------------------------- |
| SMS      | `sender`, `phone`, `template`         | 4–8       | 없음                                     |
| Viber    | `sender`, `phone`, `template`         | 4–8       | `number_formatting`                      |
| Telegram | `phone`                               | 4–8       | `ttl_in_seconds`(60–86400, 기본 60)      |
| Voice    | `phone`, `voice_type`(flash 또는 tts) | 4–6       | `ringing_duration`(5–10초, 기본 8), 언어 |

코드는 `code_length`를 주면 서비스가 만들고,
`code`를 주면 호출자가 정한 숫자를 그대로 보낸다.
둘 중 하나는 반드시 있어야 하고, 둘 다 주면 1629 오류다.
SMS와 Viber의 `template`은 `{code}` 자리를 품은 템플릿의 UUID이며,
자리가 없으면 1624 오류가 난다.
`payload`에 넣은 문자열은 웹훅으로 그대로 돌아오므로,
주문 번호 같은 내부 식별자를 실어 보낼 수 있다.

응답은 `account_id`, `message_id`, `phone`, `create_date`, `expire_date`다.
문서 예시는 생성 시각과 만료 시각이 2시간 차이지만,
SMS의 기본 유효 시간이 얼마인지는 문서에 명시돼 있지 않다.
Telegram만 `ttl_in_seconds`로 유효 시간을 정할 수 있고, 기본값은 60초다.

### 검증은 코드로 목록을 조회하는 GET이다

사용자가 입력한 코드는 아래 요청으로 확인한다.
`GET /v1/verifications?code=1234&phone=60123456789`
`code`는 필수이고 `phone`은 선택이다.
응답은 `data` 배열과 `pagination`이며,
문서는 “data가 비어 있으면 코드가 틀린 것”이라고 적는다.

즉 검증은 “이 코드가 맞는가”를 묻는 호출이 아니라
“이 코드로 만든 발송 기록을 찾아 달라”는 조회다.
맞는 코드를 한 번 확인하면 그 기록이 소모되는지, 만료된 기록도 결과에 나오는지,
틀린 시도를 몇 번까지 받는지는 문서에 없다.
이 세 가지가 문서에 없다는 사실이 아래 함정 절의 출발점이다.

### 웹훅

`POST /v1/webhooks`로 `event`(예: `DELIVERY`), `url`, `secret`, `name`,
`channel`을 등록한다.
문서의 매개변수 표에는 생성 요청인데도 `webhook_id`가 필수로 적혀 있어,
다른 페이지의 표를 옮긴 것으로 보인다.
`secret`을 어떻게 쓰는지, 예컨대 요청 본문에 서명을 붙이는지는 문서에 없다.
생성 응답은 `secret` 값을 그대로 돌려준다.

## 사용하기

아래는 문서의 예제를 그대로 이어 붙인 흐름이다.
계정을 만들지 않아 직접 실행하지는 않았다.

```bash
export OTP_KEY="발급받은 API 키"

# 1. SMS로 4자리 코드를 보낸다. template은 {code}를 품은 템플릿의 UUID다.
curl --request POST \
  --url https://api.otp.dev/v1/verifications \
  --header "X-OTP-Key: $OTP_KEY" \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{
    "data": {
      "channel": "sms",
      "sender": "OTP.dev",
      "phone": "60123456789",
      "template": "6d16aa9d-bf19-4141-8169-48b46d972fc6",
      "code_length": 4
    }
  }'

# 2. 사용자가 입력한 코드를 확인한다.
#    phone은 문서상 선택이지만 반드시 함께 보낸다(함정 절 참고).
curl --request GET \
  --url 'https://api.otp.dev/v1/verifications?code=1234&phone=60123456789' \
  --header "X-OTP-Key: $OTP_KEY" \
  --header 'accept: application/json'
```

검증 응답을 그대로 믿지 않고 서버 쪽에서 한 번 더 거르는 편이 안전하다.
아래 함수는 문서에 적힌 응답 형식만 가정한다.

```python
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://api.otp.dev/v1/verifications"


def otp_is_valid(phone: str, code: str, message_id: str) -> bool:
    # phone을 항상 함께 보내 다른 사용자의 기록과 섞이지 않게 한다.
    query = urllib.parse.urlencode({"code": code, "phone": phone})
    req = urllib.request.Request(
        f"{API}?{query}",
        headers={"X-OTP-Key": os.environ["OTP_KEY"], "accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        records = json.load(resp).get("data", [])

    now = datetime.now(timezone.utc)
    for r in records:
        # 발송 때 받은 message_id와 같은 기록만 인정한다.
        if r.get("message_id") != message_id or r.get("phone") != phone:
            continue
        # 문서는 만료 기록이 결과에서 빠지는지 밝히지 않으므로 직접 확인한다.
        expire = datetime.fromisoformat(r["expire_date"].replace("Z", "+00:00"))
        if expire > now:
            return True
    return False
```

이 함수는 시도 횟수 제한과 한 번 쓴 코드의 재사용 차단을 하지 않는다.
그 둘은 호출하는 쪽의 세션이나 DB에서 `message_id` 단위로 직접 관리해야 한다.

## 요금

요금은 나라별·채널별 건당 과금이고, 190개 이상의 나라를 다룬다.
가격표의 시작 단가는 다음과 같다.

| 채널       | 건당 시작가 | 월 발신자 요금 | 가격표가 적은 용도            |
| ---------- | ----------- | -------------- | ----------------------------- |
| FlashCalls | $0.005      | 무료           | 마찰 없는 UX, 비용, 모바일 앱 |
| Email      | $0.005      | 무료           | 온보딩, 비용, 데스크톱 사용자 |
| SMS        | $0.007      | 나라별 상이    | 도달 범위, 신뢰성, 앱 불필요  |
| Viber      | $0.01       | $124부터       | 동유럽·CIS, 브랜드 발신자     |
| Voice OTP  | $0.01       | 무료           | 유선 전화, 접근성             |
| WhatsApp   | $0.015      | $28            | 전 세계 도달, 높은 열람률     |
| Telegram   | $0.03       | 무료           | 기술 사용자, 비용, 속도       |

신규 계정은 30일 무료 체험과 시험용 시작 잔액을 받고, 카드 없이 시작할 수 있다.
사용자 지정 영숫자 발신자 ID는 나라에 따라 등록비나 추가 요금이 붙는다.
대량 발송은 별도 견적이다.

이 표는 홈페이지 문구와 세 군데에서 어긋난다.

- 홈페이지는 “Telegram이나 Email 같은 싼 채널”을 먼저 쓰라고 하지만, 가격표에서 Telegram은 시작가 $0.03으로 일곱 채널 중 가장 비싸고 SMS 시작가의 네 배가 넘는다.
- 홈페이지는 “월 요금 없음”이라고 하지만, Viber와 WhatsApp에는 월 발신자 요금이 있다.
- 홈페이지는 “성공한 메시지에만 지불”한다고 하지만, 가격 FAQ는 “보낸 검증마다” 채널 단가로 청구한다고 적는다.

“from” 가격은 나라별 최저가다.
SMS가 나라마다 크게 다르다는 사실은 FAQ도 인정하므로,
실제 비용은 사용자가 사는 나라의 단가로 계산해야 한다.

## 트레이드오프

### 다채널이라는 말은 대체 경로가 있다는 뜻이 아니다

홈페이지와 가격 FAQ는
“싼 채널을 먼저 시도하고 필요할 때만 SMS에 돈을 내는 대체 체인(fallback chain)”을
이야기한다.
하지만 공개된 API 문서의 발송 요청은 `channel` 하나만 받고,
순서나 대체 채널을 지정하는 필드는 문서에서 찾지 못했다.
대시보드에 그런 설정이 있을 수는 있지만 가입하지 않아 확인하지 못했다.

문서만으로 구현한다면 대체 경로는 호출하는 쪽의 일이다.
Telegram으로 보내고, 웹훅의 `DELIVERY` 이벤트나 일정 시간을 기다린 뒤,
오지 않았으면 SMS로 다시 보내는 상태 기계를 직접 써야 한다.
그 순간 두 가지가 어려워진다.
첫째, 두 채널로 나간 코드가 서로 다르면 사용자는 어느 것을 넣어야 할지 헷갈리고,
같게 하려면 `code`를 직접 정해 보내야 한다.
둘째, 실패 판단까지 기다리는 시간만큼 가입 흐름이 늘어진다.
Telegram의 기본 유효 시간이 60초라는 점을 생각하면,
기다리는 시간과 유효 시간을 함께 정해야 한다.

### 코드를 직접 정하면 편하지만 책임이 넘어온다

`code` 필드를 쓰면 여러 채널에 같은 코드를 보내거나,
기존 검증 시스템을 유지한 채 발송만 맡길 수 있다.
대신 난수 생성의 품질, 저장, 비교, 재사용 차단이 모두 호출자의 몫이 된다.
`code_length`를 쓰면 생성은 서비스가 하지만,
위에서 본 대로 검증의 세부 규칙이 문서에 없어서
결국 일부를 호출자가 다시 확인해야 한다.
어느 쪽을 골라도 “검증은 맡겼다”고 말할 수 있는 상태는 오지 않는다.

### 싼 채널은 도달 범위로 값을 치른다

FlashCalls와 Email이 가장 싸다.
그러나 문서의 `flash` 호출은 울리다 끊기는 전화이고,
이런 방식은 보통 걸려 온 번호를 코드로 쓴다.
앱이 통화 기록을 읽을 수 있어야 매끄럽고,
웹에서는 사용자가 번호 끝자리를 옮겨 적어야 한다.
Email은 전화번호를 검증하지 못한다.
SMS가 비싼 대신 “모든 체인이 마지막에 기대는 대체 경로”라는
홈페이지 문구는 정확하다.
결국 싼 채널을 넣을수록 단가는 내려가고,
흐름의 분기와 실패 처리 코드는 늘어난다.

## 함정

- `phone` 없이 검증하면 계정 전체에서 그 코드로 만든 기록을 찾는다. 4자리 코드는 만 가지뿐이라, 동시에 대기 중인 다른 사용자의 기록과 겹칠 수 있다. 문서가 선택이라고 적었더라도 항상 함께 보내고, 결과의 `phone`과 `message_id`를 다시 대조해야 한다.
- 검증 코드가 URL 쿼리 문자열에 들어간다. 프록시, APM, 접근 로그가 URL을 남기면 유효한 코드가 로그에 남는다. 유효 시간이 짧아도 로그 보존 기간이 그보다 길다.
- 틀린 시도 횟수 제한이 문서에 없다. 4자리 코드에 시도 제한이 없으면 만 번 안에 맞힐 수 있다. 시도 제한은 호출하는 쪽에서 `message_id` 단위로 걸어야 한다.
- 홈페이지의 “Traffic Monitoring”은 로그를 보여 준다는 뜻이지, 문서에 나라별 발송 허용 목록이나 속도 제한 API가 있다는 뜻이 아니다. SMS 펌핑을 막는 장치는 가입 폼 쪽에 따로 둬야 한다. 공격 구조는 [AIT 사기 문서](ait-fraud.md)에 정리돼 있다.
- 가격 계산기의 “from” 단가로 예산을 잡으면 틀린다. 사용자가 몰린 나라의 SMS 단가와 Viber·WhatsApp의 월 발신자 요금을 더해야 한다.
- 약관상 OTP.dev는 스팸 방지를 위해 메시지를 검사하고, 스팸으로 판단한 메시지는 전달하지 않는다. 템플릿 문구가 마케팅처럼 보이면 조용히 안 나갈 수 있다.
- 약관은 고객이 서비스에 넣은 내용(Account Content)에 대해 무상이고 철회할 수 없으며 양도와 재허락이 가능한 전 세계 이용권을 OTP.dev에 준다. 익명화·집계한 형태로 제3자에게 상업적으로 넘기는 것도 목적에 들어 있다. 템플릿과 발송 기록이 여기에 포함되는지 법무 검토가 필요하다.
- 법적 근거 없이 개인정보를 처리하거나 Viber·WhatsApp 정책을 어기면 계약 위약금이 EUR 5,000이다. 서비스가 중지돼도 요금 지급 의무는 남는다.

## 확인하기

무료 체험 잔액으로 다음을 직접 확인하고 나서 도입을 정하는 편이 낫다.

1. 같은 번호로 코드를 두 번 보낸 뒤, 첫 번째 코드로 검증해 본다. 이전 코드가 무효가 되는지 확인한다.
2. 맞는 코드로 두 번 검증한다. 두 번째에도 `data`가 돌아오면 한 번 쓴 코드가 소모되지 않는다는 뜻이다.
3. `phone` 없이 검증해 본다. 다른 번호의 기록이 섞여 나오는지 확인한다.
4. 유효 시간이 지난 뒤 검증한다. 만료 기록이 결과에서 빠지는지 확인한다.
5. 틀린 코드로 수십 번 검증한다. 어느 시점에 차단되거나 오류 코드가 바뀌는지 확인한다.
6. 웹훅을 등록하고 요청 헤더를 기록한다. `secret`으로 만든 서명이 붙는지 확인한다.

## 기억할 원칙

### 발송을 맡겨도 검증의 의미는 맡겨지지 않는다

OTP 서비스가 대신해 주는 일은 코드를 만들고 보내는 것이다.
“이 사람이 이 번호의 주인이다”라고 판정하는 데 필요한 규칙,
곧 어느 요청에 묶인 코드인지, 몇 번까지 틀려도 되는지,
한 번 쓴 코드를 다시 받을지는 문서가 명시하지 않는 한 호출하는 쪽에 남는다.
OTP.dev처럼 검증이 조회 API로 노출된 경우에는 이 경계가 더 분명하게 드러난다.

### 마케팅 문구와 가격표가 다르면 가격표를 믿는다

이 사이트에서 “싼 Telegram”, “월 요금 없음”,
“성공한 메시지에만 과금”은 모두 가격표나 FAQ와 어긋난다.
비용을 결정하는 문서는 가격표와 약관이고,
홈페이지 문구는 그 둘을 요약한 것이 아니라 팔기 위해 쓴 것이다.
비교 검토를 할 때는 홈페이지가 아니라
가격표와 API 문서에서 숫자와 필드를 옮겨 와야 한다.
