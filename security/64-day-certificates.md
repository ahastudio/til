# Let's Encrypt 기본 인증서가 64일이 된다: 운영자가 고칠 것은 갱신 시점이다

원문: [64-Day Certificate Lifetimes Coming Feb 2027 - Let's Encrypt](https://letsencrypt.org/2026/10/07/64-day-certs.html)

HN 토론: <https://news.ycombinator.com/item?id=50002249> (53점, 28개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=50025513> (15점, 9개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/dcrosf/64_day_certificate_lifetimes_coming_feb> (39점, 21개 댓글)

GN 토론: <https://news.hada.io/topic?id=35079>

## 요약

Let's Encrypt가 2026년 10월 7일 Sarah Gran 명의로 올린 공지다.
2027년 2월 10일부터 모든 구독자의 기본 인증서 수명이 64일이 된다.
프로필로 더 짧은 45일이나 6일을 고른 경우만 예외다.
그날 이후 새로 발급하거나 갱신하는 인증서는 모두 64일짜리이고,
마지막 90일 인증서는 2027년 5월 11일에 만료될 것으로 본다.
이 과정에서 유효한 인증서를 폐기하지는 않는다.

스테이징 환경은 2026년 10월 14일부터 64일 인증서를 발급하며,
원문은 프로덕션 적용 전에 스테이징에서 시험해 보라고 권한다.

운영자가 할 일은 갱신 방식에 따라 갈린다.
갱신이 자동이고 클라이언트가 ACME Renewal Info(ARI)를 지원하면
Let's Encrypt가 갱신 시점을 알려 주므로 준비가 끝난 상태다.
갱신이 만료일 기준의 고정 날짜에 묶여 있다면
수명의 약 ⅔ 지점에서 갱신하도록 바꿔야 한다.
이것이 2028년 기본 45일 전환의 준비도 된다.
확신이 없으면 cron 작업, 래퍼 스크립트, 런북에서 83, 80, 60 같은
하드코딩된 숫자를 grep으로 찾아보라고 한다.

인가(authorization) 재사용 기간도 30일에서 10일로 줄고,
2028년에는 7시간이 된다.
2029년의 검증 재사용 기간 상한 축소를 지키고,
검증 데이터가 7시간보다 오래됐을 때 검증 일부를 다시 해야 하는
CAA 재확인을 없애기 위해서다.
클라이언트를 일부러 검증 재사용에 의존하게 만들지 않았다면 바꿀 것은 없다.

원문은 이 기회에 재로드와 배포 같은 인증서 관리 절차도 자동화하고
갱신 실패 알림을 붙이라고 권한다.
레이트 리밋(rate limit), ACME 엔드포인트, 발급 체인은 바뀌지 않는다.
수명을 줄이는 이유는 키 유출과 오발급의 위험을 줄이는 것이고,
비영리 단체로서 웹을 쓰는 모든 사람의 보안을 높이는 일이
사명의 일부라고 설명한다.

## 동작 방식

### 세 단계 일정은 규정보다 한발 앞서 간다

64일은 2025년 12월 2일 공지(Decreasing Certificate Lifetimes to 45 Days)가
예고한 세 단계 중 두 번째 단계다.
그 공지에 따르면 2026년 5월 13일에 선택형 `tlsserver` 프로필이
45일 인증서로 바뀌었고, 2027년 2월 10일에 기본 `classic` 프로필이
64일과 10일 인가 재사용으로, 2028년 2월 16일에 45일과 7시간 재사용으로 간다.
날짜는 새 인증서에 적용되므로 사용자는 그 날짜 이후의 다음 갱신에서
줄어든 수명을 처음 보게 된다.

이 일정을 CA/Browser Forum Baseline Requirements(BR)의 상한과 나란히 놓으면
Let's Encrypt가 매 단계 규정보다 앞서 있다는 것이 드러난다.
BR 상한은 2025년 4월 통과한 SC-081v3 투표가 정한 것이다.
인증서 발급자 측 25곳 찬성, 반대 0, 기권 5곳이었고,
인증서 소비자 측 Apple, Google, Microsoft, Mozilla는 모두 찬성했다.

| 시점       | Let's Encrypt 기본(`classic`) | BR 상한(유효기간 / 도메인 검증 재사용) |
| ---------- | ----------------------------- | -------------------------------------- |
| 2026-03-15 | 90일 / 30일                   | 200일 / 200일                          |
| 2027-02-10 | 64일 / 10일                   | 200일 / 200일                          |
| 2027-03-15 | 64일 / 10일                   | 100일 / 100일                          |
| 2028-02-16 | 45일 / 7시간                  | 100일 / 100일                          |
| 2029-03-15 | 45일 / 7시간                  | 47일 / 10일                            |

64일은 2027년의 100일 상한보다 한참 짧고,
10일 인가 재사용은 BR이 2029년에야 요구하는 값을 2년 일찍 적용한 것이다.
47일 일정 자체와 그것이 운영 자동화에 갖는 의미는
`security/short-lived-certificates.md`가 다룬다.

### 프로필로 고를 수 있는 것과 없는 것

Let's Encrypt의 프로필 문서(2026년 10월 4일 갱신)에 따르면
현재 고를 수 있는 프로필은 셋이다.
`classic`은 아무 프로필도 요청하지 않은 주문에 쓰이는 기본값이고
지금은 90일 수명에 30일 인가 재사용이다.
`tlsserver`는 45일 수명에 7시간 재사용이며
Common Name, Key Encipherment, Subject Key ID를 뺀 인증서를 준다.
`shortlived`는 `tlsserver`와 같고 수명만 160시간이다.
원문이 6일이라고 부르는 것이 이것이며 실제로는 6일 16시간이다.

즉 64일 인증서를 프로덕션에서 미리 고를 방법은 없다.
2027년 2월 10일 전에 짧아진 수명을 실제 서비스에서 겪어 보려면
45일인 `tlsserver`로 건너뛰는 수밖에 없고,
64일 자체는 스테이징에서만 시험할 수 있다.

### 수명 ⅔ 규칙이 실제로 가리키는 날짜

원문이 권하는 ⅔ 지점을 날짜로 풀면 다음과 같다.

| 수명 | ⅔ 지점(발급 후) | 남는 여유 |
| ---- | --------------- | --------- |
| 90일 | 60일째          | 30일      |
| 64일 | 약 43일째       | 약 21일   |
| 45일 | 30일째          | 15일      |
| 160h | 약 4.4일째      | 약 2.2일  |

원문은 83, 80, 60이라는 숫자가 무엇을 뜻하는지 풀어 쓰지 않는다.
발급 후 경과일이나 갱신 간격으로 읽으면,
90일 인증서에서 각각 만료 7일, 10일, 30일 전에 갱신하는 설정이라는 것이
이 문서의 해석이다.
같은 숫자를 64일 인증서에 그대로 두면 60은 만료 4일 전 갱신이 되고,
80과 83은 인증서가 이미 만료된 뒤에야 갱신을 시도한다.
2025년 12월 공지도 60일 고정 간격 갱신은 45일 인증서에서
더 이상 충분하지 않다고 적었다.

### ARI가 대신 정해 주는 것

ARI는 RFC 9773으로 표준화된 ACME 확장이다.
CA의 디렉터리 객체에 `renewalInfo` 엔드포인트가 있으면 지원하는 것이고,
클라이언트는 인증서의 Authority Key Identifier와 일련번호로 만든
CertID를 그 경로에 붙여 GET을 보낸다.
응답의 `suggestedWindow`에 `start`와 `end`가 오며,
RFC가 권하는 알고리듬은 그 구간 안에서 균등한 무작위 시점을 고르는 것이다.

ARI가 고정 규칙보다 나은 점은 세 가지다.
수명이 바뀌어도 클라이언트 코드를 고칠 필요가 없다.
CA가 폐기를 앞두고 있으면 구간을 앞당겨 미리 갱신하게 할 수 있다.
그리고 CA가 갱신 부하를 시간대에 고르게 나눌 수 있다.
2024년 4월 통합 가이드는 ARI가 제안한 구간 안에서,
교체할 인증서를 명시해 갱신하면 모든 레이트 리밋에서 면제된다고 밝혔다.

2026년 3월 Let's Encrypt 블로그에 실린 Shopify 사례가 전환 전후를 보여 준다.
Shopify는 90일 수명에서 만료 30일 전이라는 고정 기준에
0–72시간의 무작위 지연을 더해 갱신 부하를 분산했는데,
이 방식은 폐기를 알지 못하고 수명 변경에 약하며
CA 쪽 부하를 고려하지 못했다.
Ruby `acme-client` 젬에 ARI를 넣은 뒤로는
ARI 구간을 갱신 시작 조건으로 쓰고 엔드포인트를 정기적으로 다시 조회한다.

### 인가 재사용 기간이 줄면 바뀌는 것

인가 재사용 기간은 도메인 제어를 한 번 검증한 뒤
같은 식별자를 담은 새 주문이 그 검증을 재사용할 수 있는 기간이다.
지금은 `classic`이 30일이라
한 번 HTTP-01이나 DNS-01을 통과하면 한 달 동안 같은 도메인의 인증서를
챌린지 없이 더 받을 수 있다.

7시간이라는 값은 CAA 재확인과 맞물려 있다.
BR은 CA가 CAA 레코드를 처리한 뒤 그 TTL이나 8시간 중 긴 쪽 안에
발급하도록 요구한다.
재사용 기간을 그보다 짧게 두면 오래된 검증 데이터로 발급할 일이 없으니
CAA를 다시 확인하는 별도 절차가 필요 없어진다.

운영 측면에서 2028년 이후의 7시간은
사실상 매 갱신마다 챌린지를 새로 통과해야 한다는 뜻이다.
HTTP-01이라면 갱신 시점마다 80번 포트와 웹 서버 설정이 살아 있어야 하고,
DNS-01이라면 갱신 경로에 DNS API 자격 증명이 늘 있어야 한다.
Let's Encrypt는 이 부담을 줄이려고 DNS-PERSIST-01을 준비해 왔다.
ACME 계정에 묶인 TXT 레코드를 한 번 올려 두면
갱신마다 DNS를 고칠 필요가 없는 방식으로,
CA/Browser Forum의 SC-088v3이 2025년 10월 만장일치로 통과했고
2026년 2월 공지는 프로덕션 도입을 2026년 2분기 목표로 잡았다.

## 점검하기

### 갱신 설정에서 고정 숫자 찾기

원문이 권하는 grep을 그대로 옮기면 다음과 같다.
경로는 배포마다 다르므로 자기 환경의 cron, systemd 타이머,
배포 스크립트 위치로 바꾼다.

```bash
# 원문이 예로 든 83, 80, 60을 갱신 관련 파일에서 찾는다
grep -rnwE '83|80|60' /etc/cron* /etc/systemd/system /usr/local/bin 2>/dev/null

# Certbot 계열이라면 버전과 갱신 설정의 덮어쓰기 값을 같이 본다
certbot --version
grep -rn 'renew_before_expiry' /etc/letsencrypt/renewal/ 2>/dev/null
```

`80`은 HTTP 포트 번호와 겹치므로 결과는 사람이 읽고 걸러야 한다.

Certbot은 버전에 따라 기본 갱신 시점이 다르다.
변경 이력에 따르면 4.0.0(2025년 4월)부터 만료 30일 전 고정 대신
수명의 ⅓이 남았을 때(수명이 10일 미만이면 ½) 갱신한다.
64일 인증서라면 약 21일이 남은 시점이다.
4.1.0(2025년 6월)부터는 `certbot renew`가 ARI를 자동으로 확인하고,
ARI가 더 이른 시점을 주면 `renew_before_expiry`보다 그쪽을 따른다.
그러니 4.1.0 이전 Certbot을 쓰거나 `renew_before_expiry`를 크게 잡아 둔
갱신 설정이 먼저 볼 곳이다.
4.0.0의 `--preferred-profile`과 `--required-profile` 플래그로
`tlsserver`를 미리 골라 45일 수명을 먼저 겪어 볼 수도 있다.

### 실제 서버의 ARI 구간 확인하기

클라이언트가 ARI를 쓰는지 문서로 확인하기 어렵다면
서버가 지금 내보내는 인증서로 Let's Encrypt에 직접 물어볼 수 있다.
아래 스크립트는 호스트의 리프 인증서를 받아 RFC 9773의 CertID를 만들고
프로덕션 `renewalInfo` 엔드포인트의 제안 구간을 출력한다.
Python 표준 라이브러리와 `openssl` 명령만 쓴다.

```python
import base64, json, ssl, subprocess, sys, urllib.request

DIRECTORY = "https://acme-v02.api.letsencrypt.org/directory"

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

def leaf_der(host: str) -> bytes:
    pem = ssl.get_server_certificate((host, 443))
    return ssl.PEM_cert_to_DER_cert(pem)

def openssl(der: bytes, *args: str) -> str:
    return subprocess.run(["openssl", "x509", "-inform", "DER", "-noout", *args],
                          input=der, capture_output=True, check=True).stdout.decode()

def cert_id(der: bytes) -> str:
    text = openssl(der, "-text")
    # AKI keyid 줄은 OpenSSL 버전에 따라 "keyid:" 접두어가 붙기도 한다
    lines = text.splitlines()
    i = next(n for n, l in enumerate(lines) if "Authority Key Identifier" in l)
    aki_hex = lines[i + 1].strip().removeprefix("keyid:").replace(":", "")
    serial_hex = openssl(der, "-serial").strip().split("=")[1]
    serial = bytes.fromhex(serial_hex if len(serial_hex) % 2 == 0 else "0" + serial_hex)
    # DER INTEGER는 최상위 비트가 1이면 0x00을 앞에 붙인다 (CertID 규칙)
    if serial[0] & 0x80:
        serial = b"\x00" + serial
    return f"{b64url(bytes.fromhex(aki_hex))}.{b64url(serial)}"

host = sys.argv[1]
der = leaf_der(host)
print(openssl(der, "-issuer", "-startdate", "-enddate").strip())
directory = json.load(urllib.request.urlopen(DIRECTORY))
url = f"{directory['renewalInfo']}/{cert_id(der)}"
print("ARI:", url)
print(json.dumps(json.load(urllib.request.urlopen(url)), indent=2))
```

2026년 10월 10일에 `letsencrypt.org`로 돌린 결과는 다음과 같았다.

```text
issuer=C=US, O=Let's Encrypt, CN=YE2
notBefore=Sep  4 14:34:32 2026 GMT
notAfter=Dec  3 14:34:31 2026 GMT
ARI: https://acme-v02.api.letsencrypt.org/acme/renewal-info/uVnyjs8i8IbTN0j_dhQYuoLYVYc.BUOTO-OGs6KzrdU08hA7yLZf
{
  "suggestedWindow": {
    "start": "2026-11-02T17:18:36Z",
    "end": "2026-11-04T12:29:25Z"
  }
}
```

90일 인증서의 59~61일째에 해당하는 구간이니 ⅔ 규칙과 맞는다.
서버 인증서의 실제 교체 날짜를 기록해 두었다가 이 구간과 비교하면
클라이언트가 ARI를 따르는지 알 수 있다.
구간이 지났는데도 같은 인증서가 나가고 있다면
클라이언트가 ARI를 무시하거나 갱신 뒤 재로드가 빠진 것이다.

### 스테이징에서 64일 인증서 받아 보기

2026년 10월 14일부터 스테이징이 64일 인증서를 발급한다.
스테이징 ACME URL은
`https://acme-staging-v02.api.letsencrypt.org/directory`이고,
Certbot에서는 `--test-cert`나 `--dry-run`으로 쓴다.
`--dry-run`은 인증서를 저장하지 않고 4.1.1부터는 ARI 확인도 건너뛰므로,
수명과 배포 경로까지 보려면 운영 인증서와 다른 이름으로 받아야 한다.

```bash
# 운영 lineage를 덮어쓰지 않도록 별도 이름을 쓴다
certbot certonly --test-cert --cert-name staging-64day \
  --standalone -d test.example.com

# 수명이 64일인지 확인한다
openssl x509 -in /etc/letsencrypt/live/staging-64day/cert.pem \
  -noout -startdate -enddate

# 확인 뒤 정리한다
certbot delete --cert-name staging-64day
```

이 Certbot 절차는 직접 실행하지 않았다.
`--standalone`은 80번 포트를 직접 열기 때문에
웹 서버가 이미 그 포트를 쓰고 있다면 `--webroot`나 DNS 플러그인으로 바꿔야 한다.

## 트레이드오프

### 갱신 여유가 줄어드는 비용은 개인 운영자에게 몰린다

수명 ⅔ 갱신은 남은 여유도 같은 비율로 줄인다.
90일 인증서에서는 자동 갱신이 실패해도 30일 동안 알아챌 시간이 있었고,
64일에서는 약 21일, 45일에서는 15일이다.
kevincox는 64일 자체는 괜찮지만
이제 한 달 휴가를 가려면
재발급 문제를 디버깅할 각오를 해야 한다고 적었다.[^kevincox]
24시간 당직이 있는 회사에는 문제가 아니지만 개인에게는 성가시고,
수명이 31일이 되더라도 매일 갱신할 수 있으면 상관없으니
만료와 갱신 가능 시점 사이의 간격만은 줄이지 말았으면 한다는 것이다.

이 불만의 일부는 규칙이 아니라 기본값을 향한다.
2023년 ARI 발표 글은 ARI가 신호이자 제안일 뿐이고
구독자는 원하면 언제든 갱신할 수 있다고 적었다.
Certbot도 4.1.0부터 ARI가 더 이른 시점을 줄 때만 그쪽을 따르므로,
`renew_before_expiry`를 크게 잡아 더 일찍 갱신하면서
폐기 대응용 ARI 신호도 받을 수 있다.
다만 수명 자체가 64일이면 일찍 갱신할수록 발급 횟수가 늘고,
2028년 7시간 재사용 이후에는 그 갱신마다 챌린지를 새로 통과해야 한다.
여유를 사는 값은 더 잦은 검증이며,
만료와 갱신 사이 간격을 30일로 지키려면 45일 수명에서는
15일마다 갱신해야 한다.

### 인가 재사용 단축은 보안과 검증 비용을 맞바꾼다

10일, 그리고 7시간 재사용은 오래된 검증으로 발급되는 일을 없애고
CAA 재확인 절차를 지운다.
대가는 매 발급마다 도메인 제어를 새로 증명해야 한다는 것이다.
DNS-01을 쓰는 곳에서는 DNS API 자격 증명이 갱신 파이프라인에
상주해야 하고, 그것은 공격자가 노릴 곳이 늘어난다는 뜻이다.
DNS-PERSIST-01은 이 자격 증명을 갱신 경로에서 빼는 대신
ACME 계정 키를 핵심 자산으로 만든다.
어느 쪽을 골라도 지켜야 할 비밀 하나는 남는다.

### 짧은 수명이 지키는 것과 지키지 않는 것

HN에서는 짧은 수명이 무엇을 막는지를 두고 논쟁이 이어졌다.
ocdtrekkie는 짧은 수명이면 도메인 등록 기관을 뚫은 사람이
똑같은 인증서를 새로 발급받을 수 있으니
키 보관에 들인 노력이 무의미해진다고 주장했다.[^ocdtrekkie]
rainsford는 새로 발급된 인증서는 원래 인증서와 다르고
도메인 소유자가 CT(Certificate Transparency) 로그로 알아챌 수 있지만,
훔친 장기 인증서는 원본과 바이트 단위로 같아서 탐지할 길이 없고
폐기도 믿을 수 없어 만료를 기다려야 할 수도 있다고 반박했다.[^rainsford]

이 대립이 원문이 한 줄로 적은 키 유출과 오발급 위험의 실제 내용이다.
짧은 수명은 훔친 키의 유효 기간을 줄이고,
등록 기관 탈취 같은 발급 경로 공격은 CT 감시라는 다른 장치에 맡긴다.
따라서 수명 단축에서 실제로 보호받으려면
자기 도메인의 CT 로그 감시를 같이 돌려야 한다.

## 함정

### 64일은 60일 간격 클라이언트를 살려 두지만 경고는 오지 않는다

muvlon은 64라는 숫자가 영리한 선택이라고 봤다.[^muvlon]
ARI를 쓰지 않는 클라이언트 대부분이 60일 뒤 갱신하도록 설정돼 있으니
그대로 두어도 만료되지는 않으면서,
Let's Encrypt와 자체 모니터링에서 만료 임박 경고를 받아
자동화를 고칠 계기가 된다는 것이다.
그러나 oliverpool이 짚었듯
Let's Encrypt는 만료 알림 메일을 더 이상 보내지 않는다.[^oliverpool]
2025년 1월 공지에 따라 이 서비스는 2025년 6월 4일에 끝났다.

결국 60일 간격 클라이언트는 2027년 2월 이후
만료 4일 전에 갱신하면서 아무 경고도 받지 못한다.
한 번만 실패해도 서비스가 멈추고, 그 실패를 알려 줄 장치는
운영자가 직접 붙인 외부 모니터링뿐이다.
원문이 갱신 실패 알림을 따로 권하는 이유가 여기 있다.

### 갱신이 성공해도 배포가 빠지면 소용없다

ARI를 지원하는 클라이언트도 디스크의 인증서만 바꾼다.
웹 서버, 로드 밸런서, 메일 서버, 다른 호스트로 복사하는 단계가
사람 손에 있다면 수명이 짧아진 만큼 그 단계가 더 자주 필요하다.
원문이 재로드와 배포의 자동화를 따로 언급한 것도 그래서다.
서버가 내보내는 인증서의 만료일을 밖에서 확인하는 것이
디스크의 인증서를 확인하는 것보다 믿을 만한 지표다.

### 오래된 스냅숏과 손이 닿지 않는 장비

한 HN 사용자는 63일 된 인프라 스냅숏이
비상시에 거의 쓸모없어진다고 지적했다.[^1970-01-01]
백업에서 복원한 서버는 백업 당시의 인증서를 들고 올라오므로,
수명이 짧을수록 복원 직후 만료된 인증서를 내보낼 가능성이 커진다.
복원 절차에 인증서 재발급 단계를 넣어 두어야 한다.

자동화할 수 없는 공급망도 있다.
zod000은 자신들이 통제할 수 없는 다른 회사에서 인증서를 받아야 하는데
그 과정을 자동화할 수 없고,
그 회사가 처음부터 제대로 된 인증서를 주지도 않는다고 토로했다.[^zod000]
fanf는 이런 관계를 위한 ACME 프록시가 있다고 답했다.[^fanf-2]
상대 회사가 ACME 프록시를 운영하면 다른 CA처럼 ACME로 받고,
프록시가 실제 CA에서 인증서를 받아 오는 구조다.

## 비평

### 원문은 64라는 숫자의 근거를 밝히지 않는다

64일은 BR의 어떤 상한과도 일치하지 않는다.
2027년 상한은 100일이고, 64일은 그보다 36일 짧다.
2025년 12월 공지도 일정만 내놓았을 뿐 왜 64인지는 적지 않았다.
Let's Encrypt 내부에서 일해 본 schoen조차
짧은 수명의 이유는 알지만 왜 64인지는 모르겠다며
이진수로 딱 떨어지는 숫자라서냐고 물었다.[^schoen]

muvlon의 60일 간격 클라이언트 해석은 그럴듯하지만 추측이다.
그 해석이 맞다면 64일은 구형 클라이언트를 위한 안전 여유이고,
그렇다면 그 사실을 공지에 적는 것이 운영자에게 가장 쓸모 있는 정보였을 것이다.
60일 간격 클라이언트가 4일 여유로 살아남는다는 것과
경고 메일이 없다는 것을 함께 적었다면
점검해야 할 대상이 훨씬 분명해졌을 것이다.

### 미리 64일을 겪어 볼 프로덕션 경로가 없다

sekinfo는 지금 64일 인증서로 미리 옮겨 갈 방법이 없다고 지적했다.[^sekinfo]
프로필 기능이 있는데도 64일 프로필을 만들지 않았고,
스테이징 인증서는 브라우저가 신뢰하지 않으니 실제 서비스 시험에는 쓸 수 없다.
45일 `tlsserver`로 바로 건너뛸 수는 있지만,
그것은 Common Name과 Key Usage 같은 인증서 구성까지 바꾸므로
수명만 짧아지는 효과를 따로 시험하는 것이 아니다.
원문이 스테이징 시험을 권하면서 프로덕션 시험 경로를 주지 않은 것은
점진적 전환이라는 프로필 기능의 취지와 어긋난다.

### ARI면 준비가 끝났다는 문장은 범위가 좁다

ARI가 해결하는 것은 언제 갱신할지다.
배포, 재로드, 오프라인 장비, 수작업 공급망, 백업 복원은
원문이 한 문단으로 묶어 자동화하라고만 했다.
crote는 대기업이 장기 인증서 갱신을 둘러싼 관료적 절차를 키워 와서
신속한 교체가 불가능해졌고,
수명을 천천히 줄이는 것이 그들을 바꿀 유일한 수단이라고 봤다.[^crote]
Lobste.rs에서 fanf는 이 일이 언제 끝나느냐는 불평에
2028년 2월 45일이 되는 때라고 답했다.[^fanf]
수명 단축의 실제 목표가 갱신 시점이 아니라 이런 절차 전체를 없애는 데 있다면,
ARI만 있으면 된다는 안내는 정작 어려운 부분을 가볍게 보이게 만든다.

## 체크리스트

- 갱신 설정에 발급 후 일수나 갱신 간격으로 83, 80, 60이 하드코딩돼 있지 않은가?
- 쓰는 ACME 클라이언트가 ARI를 지원하고, 그 기능이 켜져 있는가?
- Certbot을 쓴다면 4.1.0 이상인가?
- `renew_before_expiry` 같은 덮어쓰기 값이 64일 수명에서 의미 있는 값인가?
- 실제 서버 인증서의 교체 날짜가 ARI 제안 구간과 맞는가?
- 갱신 뒤 웹 서버 재로드와 다른 호스트로의 배포가 자동으로 이어지는가?
- 서버가 내보내는 인증서의 만료일을 밖에서 감시하는 알림이 있는가?
- 2026년 10월 14일 이후 스테이징에서 64일 인증서를 받아 경로 전체를 돌려 봤는가?
- 갱신마다 HTTP-01 또는 DNS-01 챌린지를 새로 통과할 수 있는가?
- 백업 복원 절차에 인증서 재발급 단계가 있는가?
- 자기 도메인에 대한 CT 로그 감시가 켜져 있는가?

## 기억할 원칙

### 갱신 시점은 숫자가 아니라 비율이나 CA 신호로 정한다

이번 공지의 실무 요점은 하나로 줄어든다.
며칠이라는 절대값으로 갱신 시점을 적어 두면
수명이 바뀔 때마다 그 숫자가 틀린 값이 된다.
수명의 비율로 정하면 64일에도 45일에도 살아남고,
ARI를 따르면 폐기 같은 예외 상황에도 대응한다.
2028년과 2029년의 다음 단계도 같은 방향이므로
이번에 고치는 설정은 비율이나 ARI로 바꿔야 다시 고칠 일이 없다.

### 자동화 점검은 디스크가 아니라 바깥에서 한다

갱신 성공 로그는 인증서 파일이 바뀌었다는 것만 알려 준다.
사용자가 실제로 받는 인증서가 언제 만료되는지는
서버 바깥에서 연결해 봐야 알 수 있다.
수명이 짧아질수록 갱신과 배포 사이의 틈이 장애로 바뀌는 속도가 빨라지므로,
마지막 확인은 항상 바깥에서 한다.

---

[^kevincox]: <https://news.ycombinator.com/item?id=50026465>

[^ocdtrekkie]: <https://news.ycombinator.com/item?id=50012541>

[^rainsford]: <https://news.ycombinator.com/item?id=50013494>

[^muvlon]: <https://lobste.rs/s/dcrosf/64_day_certificate_lifetimes_coming_feb#c_s6ja1i>

[^oliverpool]: <https://lobste.rs/s/dcrosf/64_day_certificate_lifetimes_coming_feb#c_bnmslp>

[^1970-01-01]: <https://news.ycombinator.com/item?id=50026903>

[^zod000]: <https://lobste.rs/s/dcrosf/64_day_certificate_lifetimes_coming_feb#c_lvamqa>

[^fanf-2]: <https://lobste.rs/s/dcrosf/64_day_certificate_lifetimes_coming_feb#c_po71qf>

[^schoen]: <https://news.ycombinator.com/item?id=50012269>

[^sekinfo]: <https://news.ycombinator.com/item?id=50020712>

[^crote]: <https://news.ycombinator.com/item?id=50010932>

[^fanf]: <https://lobste.rs/s/dcrosf/64_day_certificate_lifetimes_coming_feb#c_mcttwt>
