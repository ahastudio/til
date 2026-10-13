# 연계정보(CI) 암호화 의무: 무엇이 바뀌었고 어떤 방식으로 저장해야 하는가

## 소개

연계정보(Connecting Information, CI)는 본인확인기관이 주민등록번호를
비가역적으로 암호화해 만든 88바이트 식별값이다.
PASS, NICE, KCB 같은 본인확인 서비스를 붙인 서비스라면
회원 테이블 어딘가에 거의 반드시 이 값이 들어 있다.
같은 사람에게는 어느 서비스에서 받든 같은 값이 나오도록 설계되어 있어서,
중복가입 방지와 본인 재확인에 쓰기 편하다.
바로 그 성질 때문에 “온라인 주민등록번호”라고 불린다.

2025년 하반기 롯데카드에서 약 129만 명의 CI가 유출되었고,
그중 45만 명은 주민등록번호까지 함께 나갔다.
2026년 상반기에는 티빙과 CU 택배에서도 CI가 유출되었다.
이 흐름 속에서 “CI 암호화가 의무화된다”는 이야기가 돌았는데,
실제 규정을 읽어 보면 의무의 근거, 대상, 시행일이 항목마다 다르다.
이 문서는 근거 조문을 원문으로 확인해 정리하고,
“그래서 해시면 되는가, 솔트나 비밀키가 필요한가”라는 질문에
규정이 답하는 부분과 답하지 않는 부분을 나누어 적는다.

## 무엇이 언제 바뀌었나

CI 관련 의무는 개인정보 보호법이 아니라
정보통신망법(정보통신망 이용촉진 및 정보보호 등에 관한 법률)에 있다.
소관도 개인정보보호위원회가 아니라 방송미디어통신위원회(방미통위)다.

| 일자       | 내용                                                                                                           |
| ---------- | -------------------------------------------------------------------------------------------------------------- |
| 2024-01-23 | 정보통신망법 개정(법률 제20069호)으로 제23조의5(연계정보의 생성·처리), 제23조의6(안전조치 의무) 신설           |
| 2024-07-24 | 위 개정법 시행(공포 후 6개월)                                                                                  |
| 2025-05-20 | 같은 법 시행령 제13조(본인확인기관 조치, 연계정보 이용기관 안전조치) 신설                                      |
| 2025-05-21 | 방송통신위원회 고시 제2025-4호 「연계정보의 생성·처리 등에 관한 기준」 발령, 별표 4에 이용기관 안전조치 세부화 |
| 2025-06    | 방송통신위원회·KISA 「연계정보 처리 및 안전조치 등에 관한 안내서」 발간                                        |
| 2026-04-29 | 방미통위, 롯데카드에 연계정보 안전조치 위반으로 과태료 1,125만 원 부과                                         |
| 2026-06-19 | 방미통위 공고 제2026-199호로 분리 보관 시행일 단축안 행정예고                                                  |
| 2026-09-30 | 방미통위 고시 제2026-28호 발령, 분리 보관 시행일을 2027-05-01에서 2027-01-01로 앞당김                          |
| 2027-01-01 | 주민등록번호와 CI의 분리 보관 의무(별표 4 제3호) 시행                                                          |
| 2027-05-01 | 대규모 보유자의 CI 저장 시 암호화 의무(별표 4 제4-2호)와 수집 출처 기록 의무(별표 4 제6호) 시행                |

정리하면 “CI 암호화 의무화”라는 말은 두 가지가 섞인 것이다.
뉴스에 나온 2027년 1월 1일 단축은 암호화가 아니라 주민등록번호와의
분리 보관 시행일이다.
저장 시 암호화는 일정 규모 이상의 보유자에게만,
2027년 5월 1일부터 적용된다.
이 날짜는 2026년 9월 개정에서 바뀌지 않았다.

## 누가 대상인가

정보통신망법 제23조의5제4항은 본인확인기관으로부터 CI를 제공받은 자를
“연계정보 이용기관”으로 정의한다.
같은 조 제1항제1호는 CI 처리가 허용되는 첫 번째 경우로
“이용자가 입력한 정보를 이용하여 이용자를 안전하게 식별ㆍ인증하기 위한
서비스를 제공하는 경우”를 든다.
본인확인 서비스를 붙여 CI를 받아 저장하는 일반 서비스는
대부분 여기에 해당하므로 연계정보 이용기관이라고 보는 것이 안전하다.

의무는 두 층으로 나뉜다.

| 대상                                                    | 적용되는 의무                                                      |
| ------------------------------------------------------- | ------------------------------------------------------------------ |
| 모든 연계정보 이용기관                                  | 내부 규정, 목적 범위 내 처리, 전송 암호화, 분리 보관, 사고 대응 등 |
| 대기업·중견기업·공공기관 등 중 CI 10만 명 이상 보유     | 위 항목 + 저장 시 암호화                                           |
| 중소기업·단체 중 CI 100만 명 이상 보유                  | 위 항목 + 저장 시 암호화                                           |
| CI를 1,000건 이상 제공받은 이용기관(시행령 제14조제2호) | 방미통위 운영·관리 실태점검 대상                                   |

규모 기준에 미달하는 사업자에게는 고시상 저장 암호화 의무가 없다.
다만 아래에서 보듯 개인정보 보호법상 의무와 실태점검 대상 기준은
별개로 걸리므로, 의무가 없다는 것과 평문으로 두어도 된다는 것은
같은 말이 아니다.

## 규정이 실제로 요구하는 것

### 법률과 시행령

정보통신망법 제23조의6제2항은 연계정보 이용기관에게
「개인정보 보호법」 제29조에 따른 조치 외에 추가 의무를 지운다.
조문은 “연계정보를 주민등록번호와 분리하여 보관ㆍ관리하고
연계정보가 분실ㆍ도난ㆍ유출ㆍ위조ㆍ변조 또는 훼손되지 아니하도록
조치”하라고 적는다.
시행령 제13조제2항은 이를 일곱 가지로 나누는데,
그중 제4호가 “연계정보를 안전하게 저장ㆍ전송할 수 있는 암호화 기술의
적용”이다.
세부 내용은 방미통위 고시로 넘긴다.

### 고시 별표 4

「연계정보의 생성ㆍ처리 등에 관한 기준」 제11조와 별표 4가
이용기관이 해야 할 일을 구체적으로 적는다.
암호화와 직접 관련된 항목은 다음 세 개다.

| 항목       | 원문 요지                                                                                      | 시행일     |
| ---------- | ---------------------------------------------------------------------------------------------- | ---------- |
| 별표 4 3-1 | 비인가자 접근 등으로 CI와 주민등록번호가 함께 유출되지 않도록 물리적 또는 논리적으로 분리 보관 | 2027-01-01 |
| 별표 4 4-1 | CI를 정보통신망을 통해 인터넷망 구간으로 송·수신하는 경우 안전한 암호 알고리즘으로 암호화      | 2025-05-21 |
| 별표 4 4-2 | 규모 기준 해당자는 CI를 안전한 알고리즘으로 암호화하여 저장                                    | 2027-05-01 |

나머지 항목은 안전조치 책임자 지정과 내부 규정(1),
취급자 최소화와 연 1회 이상 점검(2), 침해사고 대응 계획(5),
CI의 수집 출처·시기·목적·대상 기록과 1년 이상 보관(6)이다.
제6호도 2027년 5월 1일부터 시행된다.

고시도, 안내서도 “안전한 알고리즘”이 무엇인지 조문으로 고정하지 않는다.
알고리즘 이름, 솔트, 키 사용 여부는 규정 본문에 없다.

### 분리 보관의 수준

안내서는 분리 방식으로 물리 서버 분리, 가상 서버 분리,
DB 인스턴스 분리, 스키마 분리, 테이블 분리를 예시한다.
논리적 분리도 허용하지만, 그 경우 CI와 주민등록번호에 대한 접근권한을
명확히 구분하고 최소화하라고 적는다.
주민등록번호를 법령 근거로 보관하는 금융·통신 사업자에게
특히 무거운 항목이다.
주민등록번호를 아예 보관하지 않는 일반 서비스라면 이 항목은
“주민등록번호를 보관하는 경우”라는 조건에 걸리지 않는다.

### 개인정보 보호법상 안전성 확보조치와의 관계

개인정보보호위원회 고시 「개인정보의 안전성 확보조치 기준」 제7조제2항은
저장 시 암호화 대상을 주민등록번호, 여권번호, 운전면허번호,
외국인등록번호, 신용카드번호, 계좌번호, 생체인식정보로 열거한다.
CI는 이 목록에 없다.
고유식별정보도 개인정보 보호법 시행령상 주민등록번호, 여권번호,
운전면허번호, 외국인등록번호 네 가지이므로 CI는 고유식별정보가 아니다.

그렇다고 CI가 개인정보 보호법 밖에 있는 것은 아니다.
안내서는 CI를 처리하는 주체가 성명 등 결합 가능한 신원 정보를 갖고
있다면 CI는 개인정보에 해당한다고 본다.
회원 DB에 이름과 함께 CI를 저장하는 서비스는 여기에 해당한다.
따라서 같은 고시의 다음 조항은 규모와 무관하게 CI에도 걸린다.

- 제7조제4항: 개인정보를 인터넷망 구간으로 송·수신할 때 암호화
- 제7조제5항: 이용자의 개인정보를 취급자 PC, 모바일 기기, 보조저장매체에 저장할 때 암호화
- 제7조제6항: 대규모 처리자는 암호 키의 생성·이용·보관·배포·파기 절차 수립

### 과태료

정보통신망법 제76조는 제23조의6제2항의 안전조치를 하지 않은 자에게
3천만 원 이하의 과태료를 정한다(현행 조문상 제2항제2호의6).
시행령 별표의 기준 금액은 1회 750만 원, 2회 1,500만 원,
3회 이상 3,000만 원이다.
롯데카드에 부과된 1,125만 원은 1회 기준 750만 원에 위반 기간 등을 이유로
50%를 가중한 금액이라고 보도되었다.
롯데카드 사례의 핵심 위반은 결제 서버 로그에 CI와 주민등록번호가
평문으로 기록되었다는 점이었다.
CI를 목적 범위 밖에서 처리하면 과태료가 아니라 같은 법 제71조의
형사처벌(5년 이하 징역 또는 5천만 원 이하 벌금) 대상이다.

## 어떤 방식으로 저장해야 하는가

### 규정이 요구하는 것

저장 시 암호화 의무 대상자라면 CI를 “안전한 알고리즘으로 암호화하여
저장”해야 한다.
여기까지가 의무의 전부다.
단방향인지 양방향인지, 솔트나 비밀키를 써야 하는지는
고시 본문에 없다.

### 안내서가 제시하는 것

방송통신위원회·KISA 안내서(2025년 6월)는 저장 암호화 항목에서
상용 암호화 솔루션, 암호화 라이브러리, 클라우드 제공자의 암호화 기능을
모두 쓸 수 있다고 적는다.
DES, MD5, SHA-1 같은 취약한 알고리즘은 쓰지 말라고 하고,
개인정보보호위원회의 2020년 「개인정보 암호화 조치 안내서」에서
가져온 예시표를 싣는다.

| 구분        | 민간부문 예시                                     |
| ----------- | ------------------------------------------------- |
| 대칭키 암호 | SEED, HIGHT, ARIA-128/192/256, AES-128/192/256 등 |
| 공개키 암호 | RSA, RSAES-OAEP 등                                |
| 일방향 암호 | SHA-224/256/384/512 등                            |

이 표에 일방향 알고리즘이 들어 있다는 점에서,
SHA-256 이상으로 단방향 변환해 저장하는 방식도
안내서가 말하는 “안전한 알고리즘” 범위에 든다고 읽을 수 있다.
그러나 안내서는 CI에 대해 솔트나 비밀키(HMAC)를 요구하지도,
권장하지도, 금지하지도 않는다.
개인정보보호위원회의 2024년 10월 안전성 확보조치 기준 안내서가
솔트를 언급하는 대목은 비밀번호 저장에 관한 것이며
“고려할 수 있다”는 표현이다.

정리하면, 공식 문서만으로는 “평문 SHA-256 해시가 CI 저장 암호화
의무를 충족하는가”에 대한 명시적 답이 없다.
문언상으로는 충족한다고 볼 여지가 크지만,
실태점검이나 사고 후 조사에서 그 해석이 그대로 받아들여질지는
공식 해석으로 확인하지 못했다.

### 평문 해시가 왜 약한가

여기서부터는 규정이 아니라 공학적 판단이다.

비밀번호 해싱에서 솔트가 필요한 이유는 원문의 엔트로피가 낮아서
사전 공격이 가능하기 때문이다.
CI는 사정이 다르다.
88바이트 값 자체의 엔트로피가 커서, 주민등록번호를 대입해 CI를 맞히는
공격은 본인확인기관의 생성 방식을 모르면 성립하지 않는다.
CI 해시의 위험은 무차별 대입이 아니라 대조에 있다.

- CI는 같은 사람에게 모든 서비스에서 같은 값이다. 여러 회사가 똑같이 `SHA-256(CI)`를 저장하면 그 해시도 회사 간에 같아져, 해시가 사실상 새로운 공용 식별자가 된다.
- 롯데카드 유출처럼 평문 CI 목록이 이미 유출되어 돌아다니면, 공격자는 그 목록을 SHA-256으로 변환해 내 DB 유출본과 바로 대조할 수 있다. 해시 저장은 이 대조를 전혀 막지 못한다.
- 두 회사의 해시 DB가 유출되면 키 없이도 서로 조인되어 한 사람의 여러 서비스 이용 내역이 묶인다.

반대로 행마다 랜덤 솔트를 넣으면 대조는 막히지만,
같은 CI가 같은 값이 되지 않으므로 중복가입 확인이나 CI로 회원 찾기가
불가능해진다.
CI를 저장하는 이유 대부분이 조회인 만큼 이 방식은 쓸모가 없다.

### HMAC과 가역 암호화

둘 다 만족하는 방법이 서비스 고유의 비밀키를 쓰는 HMAC이다.
`HMAC-SHA256(서비스키, CI)`는 같은 CI에 대해 항상 같은 값을 내므로
인덱스와 유니크 제약을 그대로 쓸 수 있다.
키가 서비스마다 다르므로 다른 회사의 값과 조인되지 않고,
DB만 유출되었을 때 공격자가 가진 평문 CI 목록과 대조할 수도 없다.
키를 DB와 분리해 KMS나 HSM에 두는 것이 이 방식의 전제다.
HMAC-SHA256은 내부적으로 SHA-256을 쓰므로 안내서 예시표의 범위를
벗어나지 않는다고 판단하지만, 이것도 공식 해석은 아니다.

원본 CI를 다시 꺼내 써야 하는 경우에는 단방향 변환으로는 부족하다.
제3자에게 CI를 넘기거나, 제휴사와 CI로 대조하거나,
마이데이터처럼 CI를 전송 요구에 써야 한다면
AES-256-GCM이나 ARIA 같은 가역 암호화가 필요하다.
가역 암호문은 매번 다른 nonce를 쓰므로 검색이 안 된다.
그래서 조회용 HMAC 인덱스와 복원용 암호문을 함께 두는
blind index 구조가 일반적이다.

| 방식                      | 결정적 조회 | 회사 간 조인 차단 | 유출 CI 목록과 대조 차단 | 원본 복원 | 비고                           |
| ------------------------- | ----------- | ----------------- | ------------------------ | --------- | ------------------------------ |
| 평문 저장                 | 가능        | 불가              | 불가                     | 가능      | 의무 대상자는 2027-05부터 위반 |
| SHA-256(CI)               | 가능        | 불가              | 불가                     | 불가      | 문언상 허용 여지, 실익 적음    |
| SHA-256(행별 솔트 + CI)   | 불가        | 가능              | 가능                     | 불가      | 조회가 안 되어 실용성 없음     |
| HMAC-SHA256(비밀키, CI)   | 가능        | 가능              | 가능(키 미유출 시)       | 불가      | 조회 용도의 권장 기본값        |
| AES-256-GCM(KMS 키)       | 불가        | 가능              | 가능(키 미유출 시)       | 가능      | 원본이 필요할 때만             |
| HMAC 인덱스 + AES-256-GCM | 가능        | 가능              | 가능(키 미유출 시)       | 가능      | 제공·대조가 필요한 서비스      |

### 이 문서의 권고

규정상 의무, 안내서의 예시, 이 문서의 공학적 권고를 구분하면 다음과 같다.

- 의무: 인터넷 구간 전송 암호화는 모든 이용기관에 이미 적용 중이다. 주민등록번호를 보관한다면 2027년 1월 1일까지 분리 보관, 규모 기준 해당자는 2027년 5월 1일까지 저장 암호화를 마쳐야 한다.
- 안내서 예시: SHA-224 이상의 일방향 알고리즘, AES·ARIA 등 대칭키 알고리즘. DES, MD5, SHA-1은 쓰지 않는다.
- 권고: 조회만 필요하면 HMAC-SHA256만 저장하고 원본 CI는 버린다. 원본이 필요하면 HMAC 인덱스와 AES-256-GCM 암호문을 함께 저장한다. 평문 SHA-256은 규정 충족 여부와 별개로 실질적인 보호 효과가 작으므로 새로 설계한다면 고르지 않는다. 규모 기준 미달이어도 같은 방식을 적용하는 편이 사고 시 설명하기 쉽다.

## 권장 설계: 원본 CI 없이 우리 식별자로 중복을 막는다

이 절은 법이 요구하는 최소선이 아니라
우리가 채택하는 기준이다.
전제는 하나다.
원본 CI는 필요 없고, 같은 사람인지를 우리 방식으로 확실히 판별할 수 있으면 된다.
그렇다면 답은 CI를 저장하지 않는 것이다.
본인확인 응답으로 받은 CI는 메모리에서 한 번 쓰고 버리고,
우리만 계산할 수 있는 식별자(이하 사람 키)만 남긴다.

### 사람 키를 만드는 방법

사람 키는 다음 값이다.

```text
person_key = HMAC-SHA256(K, "ci-person-key" || 0x00 || CI)
```

각 요소가 담는 결정은 다음과 같다.

- `HMAC-SHA256`: 같은 CI는 항상 같은 값이 되므로 유니크 제약과 조회가 그대로 된다.
  키 없이는 같은 값을 만들 수 없으므로 다른 회사와 조인되지 않고,
  유출된 CI 목록과도 대조되지 않는다.
- `K`: 이 용도에만 쓰는 256비트 비밀키다.
  가장 좋은 형태는 내보낼 수 없는 KMS·HSM 키이고,
  HMAC 계산 자체를 KMS 안에서 한다.
  AWS KMS의 HMAC 키는 FIPS 140-3 인증 HSM 안에서 생성되고
  KMS 밖으로 암호화되지 않은 상태로 나가지 않으며,
  `GenerateMac` API로 RFC 2104 표준 HMAC 값을 돌려준다.
  애플리케이션 서버가 털려도 키 자체를 가져갈 수는 없다.
- `"ci-person-key" || 0x00`: 용도 구분 접두어다.
  같은 키를 실수로 다른 용도에 쓰더라도 값이 섞이지 않게 한다.
  키를 바꿀 때 접두어는 그대로 두고 키 버전만 올린다.
- 길이를 자르지 않는다.
  32바이트 전체를 `bytea`(또는 `BINARY(32)`)로 저장한다.

다른 후보를 고르지 않는 이유도 분명히 해 둔다.

| 후보                          | 고르지 않는 이유                                                                                                             |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| CI 평문                       | 2027-05부터 의무 대상자는 위반이고, 유출되면 다른 서비스와 바로 연결된다                                                     |
| SHA-256(CI)                   | 키가 없으니 누구나 같은 값을 만든다. 회사 간 조인과 유출 목록 대조를 막지 못한다                                             |
| 행별 솔트 + 해시              | 같은 CI가 같은 값이 되지 않아 중복 검사가 불가능하다                                                                         |
| bcrypt, Argon2 같은 느린 해시 | 행별 솔트가 필요해 조회가 안 되고, 고정 솔트로 쓰면 결국 키 없는 해시와 같다. CI는 엔트로피가 커서 느리게 만드는 이점도 없다 |
| AES-GCM 암호문                | 원본이 필요 없으므로 복호화 능력을 갖고 있을 이유가 없다. 검색도 안 된다                                                     |
| 본인확인기관의 DI             | 본인확인기관이 사이트별로 발급하는 값이라 우리가 통제하는 식별자가 아니다                                                    |

### 저장 구조

사람 키는 회원 테이블이 아니라 별도 테이블에 둔다.
애플리케이션의 나머지 부분은 내부 회원 ID만 알고,
이 테이블은 본인확인 서비스 계정만 읽고 쓴다.
PostgreSQL 예시다.

```sql
CREATE TABLE person_identity (
    member_id    bigint      NOT NULL REFERENCES member (id),
    key_version  smallint    NOT NULL,  -- 키 교체 중에는 한 사람이 두 버전을 가질 수 있다
    person_key   bytea       NOT NULL CHECK (octet_length(person_key) = 32),
    ci_source    text        NOT NULL,  -- 본인확인기관(별표 4 제6호의 출처 기록)
    verified_at  timestamptz NOT NULL,
    PRIMARY KEY (key_version, person_key),  -- 같은 버전에서 같은 사람은 한 행뿐
    UNIQUE (member_id, key_version)
);

REVOKE ALL ON person_identity FROM PUBLIC;
GRANT SELECT, INSERT, UPDATE, DELETE ON person_identity TO identity_service;
```

중복 검사는 조회 뒤 삽입이 아니라 제약으로 한다.
동시에 들어온 두 가입 요청이 모두 조회를 통과해도
`PRIMARY KEY (key_version, person_key)`가 둘째를 막는다.

```sql
-- :versions, :keys 는 현재 살아 있는 모든 키 버전으로 계산한 사람 키 목록
SELECT member_id
FROM person_identity
WHERE (key_version, person_key) IN (SELECT * FROM unnest(:versions, :keys));

-- 없으면 같은 트랜잭션에서 현재 버전으로 삽입한다. 충돌하면 중복 가입이다.
INSERT INTO person_identity (member_id, key_version, person_key, ci_source, verified_at)
VALUES (:member_id, :current_version, :current_key, :source, now());
```

### 계산 코드: Python

KMS 경로와 로컬 경로를 함께 둔 Python 예시다.
운영에서는 `kms_person_key`만 쓰고,
`local_person_key`는 테스트와 KMS가 없는 환경을 위한 것이다.
두 함수는 같은 키라면 같은 표준 HMAC 값을 낸다.

```python
import hashlib
import hmac
import os

PERSON_KEY_DOMAIN = b"ci-person-key\x00"
CI_LENGTH = 88
KEY_LENGTH = 32


def normalized_ci(ci: str) -> bytes:
    trimmed = ci.strip()
    if len(trimmed) != CI_LENGTH:
        raise ValueError(f"CI 길이가 {CI_LENGTH}자가 아닙니다")
    return trimmed.encode("ascii")


def person_key_message(ci: str) -> bytes:
    return PERSON_KEY_DOMAIN + normalized_ci(ci)


def require_key_length(key: bytes) -> bytes:
    if len(key) != KEY_LENGTH:
        raise ValueError(f"키는 {KEY_LENGTH}바이트여야 합니다")
    return key


def local_person_key(ci: str, key: bytes) -> bytes:
    return hmac.new(require_key_length(key), person_key_message(ci), hashlib.sha256).digest()


def kms_person_key(ci: str, kms_client, key_id: str) -> bytes:
    response = kms_client.generate_mac(
        KeyId=key_id,
        Message=person_key_message(ci),
        MacAlgorithm="HMAC_SHA_256",
    )
    return response["Mac"]


def random_test_ci() -> str:
    import base64

    return base64.b64encode(os.urandom(66)).decode()


if __name__ == "__main__":
    key = os.urandom(KEY_LENGTH)
    ci = random_test_ci()
    person_key = local_person_key(ci, key)

    print("같은 CI, 같은 키 → 같은 값:", person_key == local_person_key(ci, key))
    print("다른 CI → 다른 값:", person_key != local_person_key(random_test_ci(), key))
    print("다른 키 → 다른 값:", person_key != local_person_key(ci, os.urandom(KEY_LENGTH)))
```

실행하면 세 줄 모두 `True`로 끝난다.
본인확인 콜백 처리 순서는 다음과 같다.

1. 본인확인기관 응답을 복호화해 CI를 메모리로 받는다.
   요청·응답 본문을 로그에 남기는 미들웨어는 이 경로에서 끈다.
2. 살아 있는 모든 키 버전으로 사람 키를 계산한다.
3. CI 변수를 버린다.
   DB, 캐시, 큐, 세션, 에러 트래커 어디에도 넘기지 않는다.
4. 사람 키로 기존 회원을 찾고, 없으면 현재 버전으로 삽입한다.

### 계산 코드: Java

같은 계산을 Java로 옮긴 것이다.
인터페이스 하나에 로컬 HMAC 구현과 KMS 구현을 두어,
운영과 테스트가 같은 호출 코드를 쓰게 했다.
HMAC 입력을 만드는 일은 `PersonKeyMessage` 하나에 모아
두 구현이 같은 메시지를 쓰도록 했다.
KMS 구현은 AWS SDK for Java 2.x를 쓴다.
아래 의존성(AWS SDK 2.55.15, Java 17 이상)으로 컴파일을 확인했다.
PostgreSQL 드라이버는 운영용이고, H2는 아래 데모용이다.

```xml
  <dependencies>
    <dependency>
      <groupId>software.amazon.awssdk</groupId>
      <artifactId>kms</artifactId>
      <version>2.55.15</version>
    </dependency>
    <dependency>
      <groupId>org.postgresql</groupId>
      <artifactId>postgresql</artifactId>
      <version>42.7.14</version>
    </dependency>
    <dependency>
      <groupId>com.h2database</groupId>
      <artifactId>h2</artifactId>
      <version>2.5.252</version>
    </dependency>
  </dependencies>
```

```java
package example.identity;

import java.nio.charset.StandardCharsets;

/**
 * 사람 키를 계산할 때 HMAC에 넣는 메시지를 만든다.
 * 용도 구분 접두어 뒤에 정규화한 CI를 붙인다.
 */
public final class PersonKeyMessage {
    private static final byte[] DOMAIN = "ci-person-key\0".getBytes(StandardCharsets.US_ASCII);
    private static final int CI_LENGTH = 88;

    private PersonKeyMessage() {
    }

    /**
     * CI로 HMAC 입력 메시지를 만든다.
     *
     * @param ci 본인확인기관이 준 88자 CI
     * @return 용도 구분 접두어와 CI를 이은 바이트 배열
     */
    public static byte[] of(String ci) {
        return concat(DOMAIN, normalizedCi(ci));
    }

    private static byte[] normalizedCi(String ci) {
        String trimmed = ci.strip();
        requireCiLength(trimmed);
        return trimmed.getBytes(StandardCharsets.US_ASCII);
    }

    private static void requireCiLength(String ci) {
        if (ci.length() != CI_LENGTH) {
            throw new IllegalArgumentException("CI 길이가 " + CI_LENGTH + "자가 아닙니다");
        }
    }

    private static byte[] concat(byte[] head, byte[] tail) {
        byte[] joined = new byte[head.length + tail.length];
        System.arraycopy(head, 0, joined, 0, head.length);
        System.arraycopy(tail, 0, joined, head.length, tail.length);
        return joined;
    }
}
```

```java
package example.identity;

import java.util.Set;

/**
 * CI에서 우리 서비스만 계산할 수 있는 사람 키를 만든다.
 * 키 교체 중에는 여러 버전이 동시에 살아 있다.
 */
public interface PersonKeys {

    /**
     * 지정한 키 버전으로 사람 키를 계산한다.
     *
     * @param ci 본인확인기관이 준 88자 CI
     * @param version 계산에 쓸 키 버전
     * @return 32바이트 HMAC-SHA256 값
     */
    byte[] personKey(String ci, int version);

    /**
     * 조회에 써야 하는 모든 키 버전을 돌려준다.
     *
     * @return 살아 있는 키 버전 집합
     */
    Set<Integer> liveVersions();

    /**
     * 새로 저장할 때 쓰는 키 버전을 돌려준다.
     *
     * @return 현재 키 버전
     */
    int currentVersion();
}
```

```java
package example.identity;

import java.security.GeneralSecurityException;
import java.util.Map;
import java.util.Set;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

/**
 * 키 바이트를 애플리케이션이 직접 들고 계산한다.
 * 테스트와 KMS가 없는 환경에서만 쓴다.
 */
public final class LocalPersonKeys implements PersonKeys {
    private static final int KEY_LENGTH = 32;

    private final Map<Integer, byte[]> keysByVersion;
    private final int currentVersion;

    /**
     * 버전별 키로 계산기를 만든다.
     *
     * @param keysByVersion 버전마다 32바이트 키
     * @param currentVersion 새로 저장할 때 쓰는 버전
     */
    public LocalPersonKeys(Map<Integer, byte[]> keysByVersion, int currentVersion) {
        keysByVersion.values().forEach(LocalPersonKeys::requireKeyLength);
        this.keysByVersion = Map.copyOf(keysByVersion);
        this.currentVersion = currentVersion;
    }

    @Override
    public byte[] personKey(String ci, int version) {
        try {
            return hmacSha256(keysByVersion.get(version), PersonKeyMessage.of(ci));
        } catch (GeneralSecurityException e) {
            throw new IllegalStateException("HmacSHA256을 쓸 수 없습니다", e);
        }
    }

    @Override
    public Set<Integer> liveVersions() {
        return keysByVersion.keySet();
    }

    @Override
    public int currentVersion() {
        return currentVersion;
    }

    private static byte[] hmacSha256(byte[] key, byte[] message) throws GeneralSecurityException {
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(key, "HmacSHA256"));
        return mac.doFinal(message);
    }

    private static void requireKeyLength(byte[] key) {
        if (key.length != KEY_LENGTH) {
            throw new IllegalArgumentException("키는 " + KEY_LENGTH + "바이트여야 합니다");
        }
    }
}
```

```java
package example.identity;

import java.util.Map;
import java.util.Set;
import software.amazon.awssdk.core.SdkBytes;
import software.amazon.awssdk.services.kms.KmsClient;
import software.amazon.awssdk.services.kms.model.GenerateMacRequest;
import software.amazon.awssdk.services.kms.model.MacAlgorithmSpec;

/**
 * AWS KMS의 HMAC 키로 사람 키를 계산한다.
 * 키 원본은 KMS 밖으로 나오지 않는다.
 */
public final class KmsPersonKeys implements PersonKeys {
    private final KmsClient kms;
    private final Map<Integer, String> keyIdsByVersion;
    private final int currentVersion;

    /**
     * 버전별 KMS 키 ID로 계산기를 만든다.
     *
     * @param kms KMS 클라이언트
     * @param keyIdsByVersion 버전마다 HMAC_256 키의 ID나 별칭
     * @param currentVersion 새로 저장할 때 쓰는 버전
     */
    public KmsPersonKeys(KmsClient kms, Map<Integer, String> keyIdsByVersion, int currentVersion) {
        this.kms = kms;
        this.keyIdsByVersion = Map.copyOf(keyIdsByVersion);
        this.currentVersion = currentVersion;
    }

    @Override
    public byte[] personKey(String ci, int version) {
        return kms.generateMac(macRequest(ci, version)).mac().asByteArray();
    }

    @Override
    public Set<Integer> liveVersions() {
        return keyIdsByVersion.keySet();
    }

    @Override
    public int currentVersion() {
        return currentVersion;
    }

    private GenerateMacRequest macRequest(String ci, int version) {
        return GenerateMacRequest.builder()
                .keyId(keyIdsByVersion.get(version))
                .macAlgorithm(MacAlgorithmSpec.HMAC_SHA_256)
                .message(SdkBytes.fromByteArray(PersonKeyMessage.of(ci)))
                .build();
    }
}
```

로컬 구현과 KMS 구현은 같은 키라면 같은 RFC 2104 HMAC 값을 낸다.
다만 KMS 키는 내보낼 수 없으므로 두 구현의 값을 직접 맞춰 볼 수는 없다.
키 버전마다 KMS 키를 하나씩 만들고,
`keyIdsByVersion`에 버전과 키 별칭을 함께 등록한다.

### 가입·중복 검사·재인증: Python

계산만으로는 중복이 막히지 않는다.
조회와 삽입을 한 트랜잭션에 넣고,
동시에 들어온 요청은 기본 키 제약이 최종 판정을 하게 해야 한다.
표준 라이브러리 `sqlite3`만으로 돌아가는 Python 예시다.
키 교체 전에 가입한 회원이 다른 본인확인기관으로 다시 가입하려다 막히고,
재인증하면 새 버전 행이 추가되는 과정까지 재현한다.

```python
import hashlib
import hmac
import os
import sqlite3
from datetime import datetime, timezone

from person_key import KEY_LENGTH, person_key_message, random_test_ci

LIVE_KEYS = {1: os.urandom(KEY_LENGTH), 2: os.urandom(KEY_LENGTH)}
CURRENT_VERSION = 2

SCHEMA = """
CREATE TABLE IF NOT EXISTS person_identity (
    member_id   INTEGER NOT NULL,
    key_version INTEGER NOT NULL,
    person_key  BLOB    NOT NULL CHECK (length(person_key) = 32),
    ci_source   TEXT    NOT NULL,
    verified_at TEXT    NOT NULL,
    PRIMARY KEY (key_version, person_key),
    UNIQUE (member_id, key_version)
)
"""


class DuplicatePerson(Exception):
    def __init__(self, member_id):
        super().__init__(f"이미 가입한 사람입니다(member_id={member_id})")
        self.member_id = member_id


def person_keys_of(ci: str) -> dict[int, bytes]:
    message = person_key_message(ci)
    return {
        version: hmac.new(key, message, hashlib.sha256).digest()
        for version, key in LIVE_KEYS.items()
    }


def register(conn, member_id: int, ci: str, source: str,
             version: int = CURRENT_VERSION) -> None:
    register_person_keys(conn, member_id, person_keys_of(ci), source, version)


def reverify(conn, ci: str, source: str):
    return reverify_person_keys(conn, person_keys_of(ci), source)


def register_person_keys(conn, member_id, person_keys, source, version) -> None:
    with conn:
        reject_if_already_registered(conn, person_keys)
        try:
            insert_identity(conn, member_id, version, person_keys[version], source)
        except sqlite3.IntegrityError:
            raise DuplicatePerson(find_member(conn, person_keys)) from None


def reverify_person_keys(conn, person_keys, source):
    with conn:
        member_id = find_member(conn, person_keys)
        if member_id is not None and not has_version(conn, member_id, CURRENT_VERSION):
            insert_identity(conn, member_id, CURRENT_VERSION,
                            person_keys[CURRENT_VERSION], source)
        return member_id


def reject_if_already_registered(conn, person_keys) -> None:
    existing = find_member(conn, person_keys)
    if existing is not None:
        raise DuplicatePerson(existing)


def find_member(conn, person_keys):
    for version, person_key in person_keys.items():
        member_id = member_with_key(conn, version, person_key)
        if member_id is not None:
            return member_id
    return None


def member_with_key(conn, version, person_key):
    row = conn.execute(
        "SELECT member_id FROM person_identity WHERE key_version = ? AND person_key = ?",
        (version, person_key),
    ).fetchone()
    return row[0] if row else None


def has_version(conn, member_id, version) -> bool:
    row = conn.execute(
        "SELECT 1 FROM person_identity WHERE member_id = ? AND key_version = ?",
        (member_id, version),
    ).fetchone()
    return row is not None


def insert_identity(conn, member_id, version, person_key, source) -> None:
    conn.execute(
        "INSERT INTO person_identity VALUES (?, ?, ?, ?, ?)",
        (member_id, version, person_key, source, utc_now()),
    )


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def register_or_duplicate(conn, member_id, ci, source):
    try:
        register(conn, member_id, ci, source)
    except DuplicatePerson as duplicate:
        return duplicate.member_id
    return None


def stored_rows(conn):
    return conn.execute(
        "SELECT member_id, key_version FROM person_identity ORDER BY key_version"
    ).fetchall()


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    conn.execute(SCHEMA)
    ci = random_test_ci()

    register(conn, 1, ci, "PASS", version=1)
    print("중복 차단:", register_or_duplicate(conn, 2, ci, "NICE"))
    print("재인증 회원:", reverify(conn, ci, "PASS"))
    print("저장된 행:", stored_rows(conn))
```

실행 결과는 다음과 같다.

```text
중복 차단: 1
재인증 회원: 1
저장된 행: [(1, 1), (1, 2)]
```

같은 CI라도 본인확인기관(PASS, NICE)이 달라질 수 있으므로
`ci_source`는 판정에 쓰지 않고 출처 기록으로만 남긴다.
원본 CI는 `register`와 `reverify`의 첫 줄에서 사람 키로 바뀌고,
그 아래 함수들은 CI를 인자로 받지 않는다.
원본이 데이터베이스 코드까지 내려갈 길을 구조로 막은 것이다.
이 파일은 앞의 `person_key.py`와 같은 디렉터리에 두고 실행한다.

### 가입·중복 검사·재인증: Java

JDBC로 같은 흐름을 구현한 저장소 클래스다.
PostgreSQL과 H2가 같은 SQLSTATE `23505`로 유니크 위반을 알리므로,
동시 가입 경쟁에서 진 요청도 중복으로 처리된다.

```java
package example.identity;

/**
 * 같은 사람이 이미 가입해 있을 때 던진다.
 * 기존 회원 ID를 함께 담는다.
 */
public final class DuplicatePersonException extends Exception {
    private final long existingMemberId;

    /**
     * 기존 회원 ID로 예외를 만든다.
     *
     * @param existingMemberId 이미 가입한 회원의 ID
     */
    public DuplicatePersonException(long existingMemberId) {
        super("이미 가입한 사람입니다(member_id=" + existingMemberId + ")");
        this.existingMemberId = existingMemberId;
    }

    /**
     * 이미 가입한 회원의 ID를 돌려준다.
     *
     * @return 기존 회원 ID
     */
    public long existingMemberId() {
        return existingMemberId;
    }
}
```

```java
package example.identity;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.OptionalLong;
import javax.sql.DataSource;

/**
 * 사람 키로 가입과 재인증을 처리한다.
 * 원본 CI는 사람 키를 계산하는 순간에만 쓰고 저장하지 않는다.
 */
public final class PersonIdentityRepository {
    private static final String UNIQUE_VIOLATION = "23505";

    private static final String FIND_MEMBER =
            "SELECT member_id FROM person_identity WHERE key_version = ? AND person_key = ?";
    private static final String HAS_VERSION =
            "SELECT member_id FROM person_identity WHERE member_id = ? AND key_version = ?";
    private static final String INSERT =
            "INSERT INTO person_identity"
            + " (member_id, key_version, person_key, ci_source, verified_at) VALUES (?, ?, ?, ?, ?)";

    private final DataSource dataSource;
    private final PersonKeys personKeys;

    /**
     * 저장소를 만든다.
     *
     * @param dataSource person_identity 테이블이 있는 데이터베이스
     * @param personKeys 사람 키 계산기
     */
    public PersonIdentityRepository(DataSource dataSource, PersonKeys personKeys) {
        this.dataSource = dataSource;
        this.personKeys = personKeys;
    }

    /**
     * 현재 키 버전으로 회원을 등록한다.
     *
     * @param memberId 새 회원 ID
     * @param ci 본인확인기관이 준 CI
     * @param source CI를 준 본인확인기관
     * @throws DuplicatePersonException 같은 사람이 이미 가입해 있을 때
     * @throws SQLException 데이터베이스 오류
     */
    public void register(long memberId, String ci, String source)
            throws SQLException, DuplicatePersonException {
        register(memberId, ci, source, personKeys.currentVersion());
    }

    /**
     * 지정한 키 버전으로 회원을 등록한다.
     *
     * @param memberId 새 회원 ID
     * @param ci 본인확인기관이 준 CI
     * @param source CI를 준 본인확인기관
     * @param version 저장할 키 버전
     * @throws DuplicatePersonException 같은 사람이 이미 가입해 있을 때
     * @throws SQLException 데이터베이스 오류
     */
    public void register(long memberId, String ci, String source, int version)
            throws SQLException, DuplicatePersonException {
        Map<Integer, byte[]> keys = personKeysOf(ci);
        try (Connection connection = dataSource.getConnection()) {
            registerInTransaction(connection, memberId, version, keys, source);
        }
    }

    /**
     * 재인증한 회원에게 현재 버전의 사람 키가 없으면 추가한다.
     *
     * @param ci 본인확인기관이 준 CI
     * @param source CI를 준 본인확인기관
     * @return 찾은 회원 ID, 가입한 적이 없으면 비어 있다
     * @throws SQLException 데이터베이스 오류
     */
    public OptionalLong reverify(String ci, String source) throws SQLException {
        Map<Integer, byte[]> keys = personKeysOf(ci);
        try (Connection connection = dataSource.getConnection()) {
            return reverifyInTransaction(connection, keys, source);
        }
    }

    private Map<Integer, byte[]> personKeysOf(String ci) {
        Map<Integer, byte[]> keys = new LinkedHashMap<>();
        for (int version : personKeys.liveVersions()) {
            keys.put(version, personKeys.personKey(ci, version));
        }
        return keys;
    }

    private void registerInTransaction(Connection connection, long memberId, int version,
            Map<Integer, byte[]> keys, String source) throws SQLException, DuplicatePersonException {
        connection.setAutoCommit(false);
        try {
            insertIfAbsent(connection, memberId, version, keys, source);
        } catch (DuplicatePersonException e) {
            connection.rollback();
            throw e;
        } catch (SQLException e) {
            connection.rollback();
            throwDuplicateIfConcurrentInsert(connection, keys, e);
            throw e;
        }
    }

    private static void insertIfAbsent(Connection connection, long memberId, int version,
            Map<Integer, byte[]> keys, String source) throws SQLException, DuplicatePersonException {
        rejectIfAlreadyRegistered(connection, keys);
        insert(connection, memberId, version, keys.get(version), source);
        connection.commit();
    }

    private static void rejectIfAlreadyRegistered(Connection connection, Map<Integer, byte[]> keys)
            throws SQLException, DuplicatePersonException {
        OptionalLong existing = findMember(connection, keys);
        if (existing.isPresent()) {
            throw new DuplicatePersonException(existing.getAsLong());
        }
    }

    private static void throwDuplicateIfConcurrentInsert(Connection connection,
            Map<Integer, byte[]> keys, SQLException e) throws SQLException, DuplicatePersonException {
        if (UNIQUE_VIOLATION.equals(e.getSQLState())) {
            throw new DuplicatePersonException(findMember(connection, keys).orElse(-1));
        }
    }

    private OptionalLong reverifyInTransaction(Connection connection, Map<Integer, byte[]> keys,
            String source) throws SQLException {
        connection.setAutoCommit(false);
        OptionalLong member = findMember(connection, keys);
        if (member.isPresent()) {
            addCurrentVersionIfMissing(connection, member.getAsLong(), keys, source);
        }
        connection.commit();
        return member;
    }

    private void addCurrentVersionIfMissing(Connection connection, long memberId,
            Map<Integer, byte[]> keys, String source) throws SQLException {
        int current = personKeys.currentVersion();
        if (!hasVersion(connection, memberId, current)) {
            insert(connection, memberId, current, keys.get(current), source);
        }
    }

    private static OptionalLong findMember(Connection connection, Map<Integer, byte[]> keys)
            throws SQLException {
        try (PreparedStatement statement = connection.prepareStatement(FIND_MEMBER)) {
            return firstMemberMatching(statement, keys);
        }
    }

    private static OptionalLong firstMemberMatching(PreparedStatement statement,
            Map<Integer, byte[]> keys) throws SQLException {
        for (Map.Entry<Integer, byte[]> key : keys.entrySet()) {
            OptionalLong member = memberWithKey(statement, key.getKey(), key.getValue());
            if (member.isPresent()) {
                return member;
            }
        }
        return OptionalLong.empty();
    }

    private static OptionalLong memberWithKey(PreparedStatement statement, int version,
            byte[] personKey) throws SQLException {
        statement.setInt(1, version);
        statement.setBytes(2, personKey);
        return firstLong(statement);
    }

    private static boolean hasVersion(Connection connection, long memberId, int version)
            throws SQLException {
        try (PreparedStatement statement = connection.prepareStatement(HAS_VERSION)) {
            return rowExists(statement, memberId, version);
        }
    }

    private static boolean rowExists(PreparedStatement statement, long memberId, int version)
            throws SQLException {
        statement.setLong(1, memberId);
        statement.setInt(2, version);
        return firstLong(statement).isPresent();
    }

    private static OptionalLong firstLong(PreparedStatement statement) throws SQLException {
        try (ResultSet rows = statement.executeQuery()) {
            return firstLongOf(rows);
        }
    }

    private static OptionalLong firstLongOf(ResultSet rows) throws SQLException {
        return rows.next() ? OptionalLong.of(rows.getLong(1)) : OptionalLong.empty();
    }

    private static void insert(Connection connection, long memberId, int version,
            byte[] personKey, String source) throws SQLException {
        try (PreparedStatement statement = connection.prepareStatement(INSERT)) {
            insertWith(statement, memberId, version, personKey, source);
        }
    }

    private static void insertWith(PreparedStatement statement, long memberId, int version,
            byte[] personKey, String source) throws SQLException {
        statement.setLong(1, memberId);
        statement.setInt(2, version);
        statement.setBytes(3, personKey);
        statement.setString(4, source);
        statement.setTimestamp(5, Timestamp.from(Instant.now()));
        statement.executeUpdate();
    }
}
```

H2를 PostgreSQL 모드로 띄워 같은 시나리오를 돌리는 데모다.

```java
package example.identity;

import java.security.SecureRandom;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Base64;
import java.util.Map;
import javax.sql.DataSource;
import org.h2.jdbcx.JdbcDataSource;

/**
 * H2를 PostgreSQL 모드로 띄워 가입, 중복 차단, 재인증을 재현한다.
 * 회원 1은 키 교체 전 버전 1로 가입했다고 가정한다.
 */
public final class Demo {
    private static final SecureRandom RANDOM = new SecureRandom();

    private static final String SCHEMA = "CREATE TABLE person_identity ("
            + " member_id bigint NOT NULL, key_version smallint NOT NULL,"
            + " person_key bytea NOT NULL CHECK (octet_length(person_key) = 32),"
            + " ci_source text NOT NULL, verified_at timestamp NOT NULL,"
            + " PRIMARY KEY (key_version, person_key), UNIQUE (member_id, key_version))";

    private static final String STORED_ROWS =
            "SELECT member_id, key_version FROM person_identity ORDER BY key_version";

    private Demo() {
    }

    /**
     * 시나리오를 실행하고 결과를 출력한다.
     *
     * @param args 쓰지 않는다
     * @throws SQLException 데이터베이스 오류
     * @throws DuplicatePersonException 회원 1의 첫 가입이 중복으로 판정될 때
     */
    public static void main(String[] args) throws SQLException, DuplicatePersonException {
        PersonKeys keys = new LocalPersonKeys(Map.of(1, randomBytes(32), 2, randomBytes(32)), 2);
        DataSource dataSource = inMemoryDatabase();
        PersonIdentityRepository repository = new PersonIdentityRepository(dataSource, keys);
        String ci = randomTestCi();

        repository.register(1, ci, "PASS", 1);
        System.out.println("중복 차단: " + registerOrExistingMember(repository, 2, ci, "NICE"));
        System.out.println("재인증 회원: " + repository.reverify(ci, "PASS").getAsLong());
        System.out.println("저장된 행:" + storedRows(dataSource));
    }

    private static long registerOrExistingMember(PersonIdentityRepository repository,
            long memberId, String ci, String source) throws SQLException {
        try {
            repository.register(memberId, ci, source);
        } catch (DuplicatePersonException duplicate) {
            return duplicate.existingMemberId();
        }
        return memberId;
    }

    private static DataSource inMemoryDatabase() throws SQLException {
        JdbcDataSource dataSource = new JdbcDataSource();
        dataSource.setURL("jdbc:h2:mem:demo;MODE=PostgreSQL;DB_CLOSE_DELAY=-1");
        createSchema(dataSource);
        return dataSource;
    }

    private static void createSchema(DataSource dataSource) throws SQLException {
        try (Connection connection = dataSource.getConnection()) {
            execute(connection, SCHEMA);
        }
    }

    private static void execute(Connection connection, String sql) throws SQLException {
        try (Statement statement = connection.createStatement()) {
            statement.execute(sql);
        }
    }

    private static String storedRows(DataSource dataSource) throws SQLException {
        try (Connection connection = dataSource.getConnection()) {
            return storedRows(connection);
        }
    }

    private static String storedRows(Connection connection) throws SQLException {
        try (Statement statement = connection.createStatement()) {
            return formatRows(statement.executeQuery(STORED_ROWS));
        }
    }

    private static String formatRows(ResultSet rows) throws SQLException {
        StringBuilder text = new StringBuilder();
        while (rows.next()) {
            text.append(" (").append(rows.getLong(1)).append(", ").append(rows.getInt(2)).append(")");
        }
        return text.toString();
    }

    private static String randomTestCi() {
        return Base64.getEncoder().encodeToString(randomBytes(66));
    }

    private static byte[] randomBytes(int length) {
        byte[] bytes = new byte[length];
        RANDOM.nextBytes(bytes);
        return bytes;
    }
}
```

```bash
mvn -q compile
mvn -q dependency:build-classpath -Dmdep.outputFile=cp.txt
java -cp "target/classes:$(cat cp.txt)" example.identity.Demo
```

실행 결과는 다음과 같다.

```text
중복 차단: 1
재인증 회원: 1
저장된 행: (1, 1) (1, 2)
```

### 키 교체

원본 CI를 버리는 대가는 일괄 재계산이 불가능하다는 점이다.
AWS KMS의 HMAC 키는 자동 교체도 지원하지 않는다.
그래서 교체는 새 키를 만들고 버전을 올리는 방식으로 하고,
사람이 다시 본인확인을 할 때마다 점진적으로 옮긴다.

1. 새 HMAC 키를 만들고 `key_version = 2`로 등록한다.
2. 이후 모든 본인확인에서 버전 1과 2를 모두 계산해 조회하고,
   찾은 회원에게 버전 2 행을 추가한다.
3. 신규 가입은 버전 2로만 쓴다.
4. 버전 1 행만 남은 회원은 탈퇴·휴면 파기 정책에 따라 사라질 때까지 둔다.
   버전 1 키는 그때까지 조회 전용으로 남긴다.

교체가 급한 경우는 키 유출이 의심될 때뿐이다.
내보낼 수 없는 KMS 키를 쓰면 이 경우가 사실상 호출 권한 탈취로 좁혀지고,
그때는 키 교체보다 권한 회수가 먼저다.

### 무엇을 막고 무엇을 남기는가

| 사고                            | 결과                                                                                                  |
| ------------------------------- | ----------------------------------------------------------------------------------------------------- |
| DB나 백업만 유출                | CI가 없으므로 CI 유출이 아니다. 사람 키는 다른 회사 값과 조인되지 않고 유출 CI 목록과 대조되지 않는다 |
| 다른 회사에서 평문 CI 목록 유출 | 우리 DB 유출본과 대조할 수 없다                                                                       |
| 애플리케이션 서버 장악          | 공격자가 KMS 호출 권한으로 CI 목록을 넣어 대조할 수 있다. 키 자체는 가져가지 못한다                   |
| 로컬 키 방식에서 환경 변수 유출 | 키 유출과 같다. 그래서 운영은 KMS 경로를 쓴다                                                         |
| 본인확인 콜백 로그 유출         | 평문 CI가 남아 있었다면 그대로 유출된다. 설계의 가장 약한 고리다                                      |

남는 위험을 줄이는 운영 장치는 다음과 같다.

- `kms:GenerateMac` 권한은 본인확인 서비스의 역할에만 준다.
- CloudTrail 같은 감사 로그로 `GenerateMac` 호출량을 보고,
  가입·재인증 건수를 크게 넘으면 알람을 건다.
- 본인확인 콜백 경로의 로그, APM, 에러 트래커에서 요청 본문을 마스킹한다.

사람 키도 개인정보다.
키를 가진 우리에게는 특정 개인을 가리키는 값이기 때문이다.
분석, 로그, 외부 전달에는 사람 키 대신 내부 회원 ID를 쓰고,
분석에서 사람 단위 집계가 꼭 필요하면 별도 키로 만든 값을 쓴다.

## 실무 적용

### 용도별 결정표

| 용도                                   | 저장할 것                   | 이유                                                         |
| -------------------------------------- | --------------------------- | ------------------------------------------------------------ |
| 중복가입 방지                          | HMAC 인덱스만               | 같은 CI인지 비교만 하면 된다                                 |
| 재인증 시 기존 회원 매칭               | HMAC 인덱스만               | 재인증 때 본인확인기관이 CI를 다시 주므로 원본 보관이 불필요 |
| 탈퇴 회원 재가입 제한                  | HMAC 인덱스, 보관 기한 명시 | 목적과 기한을 처리방침에 적어야 한다                         |
| 제3자 제공, 제휴사 CI 대조, 마이데이터 | HMAC 인덱스 + 가역 암호문   | 원본 CI를 다시 보내야 한다                                   |
| 분석, 통계, 로그                       | 저장하지 않음               | 필요하면 분석 전용 별도 키의 HMAC을 쓴다                     |

재인증 때마다 CI를 다시 받을 수 있다는 점이 중요하다.
대부분의 서비스는 원본 CI를 보관할 이유가 없고,
보관하지 않으면 별표 4의 저장 암호화와 분리 보관 문제도 가장 단순해진다.

### 키 관리

- HMAC 키와 암호화 키는 서로 다른 키로 둔다. 하나가 유출되어도 다른 용도가 무너지지 않게 하기 위해서다.
- 키는 KMS, HSM, 시크릿 매니저에 두고 애플리케이션에는 런타임에 주입한다. DB, 백업, 저장소, 이미지에 키가 함께 들어가면 분리의 의미가 없다.
- 저장값에 키 버전을 붙인다(`v1:...`). HMAC 키를 교체하려면 원본 CI가 필요하므로, 원본을 버리는 설계라면 재인증 시점에 새 키로 다시 계산하는 점진 교체를 계획해 둔다.
- AES-GCM은 같은 키로 nonce를 재사용하면 안 된다. 96비트 랜덤 nonce를 쓰고, 한 키로 암호화하는 건수가 매우 많다면 주기적으로 키를 교체하거나 KMS의 envelope encryption을 쓴다.
- 안전성 확보조치 기준 제7조제6항의 대상이라면 키의 생성·이용·보관·배포·파기 절차를 문서로 남긴다.

### 기존 평문 CI 마이그레이션

1. CI가 있는 모든 위치를 찾는다. 회원 테이블뿐 아니라 이력 테이블, 탈퇴 회원 보관 테이블, 큐 메시지, 캐시, 데이터 웨어하우스, 로그, 엑셀 추출본까지 포함한다.
2. 새 컬럼(`ci_hmac`, 필요하면 `ci_enc`)을 추가하고 쓰기 경로를 이중 기록으로 바꾼다.
3. 기존 행을 배치로 채운다(backfill). 배치 작업 자체가 평문 CI를 로그에 남기지 않도록 주의한다.
4. 읽기 경로를 새 컬럼으로 전환하고, 유니크 제약을 `ci_hmac`으로 옮긴다.
5. 평문 컬럼을 삭제한다. 삭제 후에도 기존 백업과 스냅숏에는 평문이 남으므로, 백업 보존 기한이 지나 자연 소멸되는 시점을 기록하거나 재생성한다.
6. 주민등록번호를 보관한다면 같은 작업에서 CI와 주민등록번호를 다른 DB나 스키마, 다른 접근권한으로 분리한다.
7. 별표 4 제6호에 따라 CI 수집 출처, 시기, 목적, 대상 기록을 남기기 시작한다.

### 로그와 분석 데이터

롯데카드 사례에서 문제가 된 것은 DB가 아니라 결제 서버 로그였다.
보도에 따르면 로그가 암호화되기 전 평문으로 남는 구간을
공격자가 노렸다.

- 본인확인 콜백, 요청·응답 본문 전체를 디버그 로그로 남기는 코드가 가장 흔한 유출 경로다. CI 필드를 마스킹하는 로거 필터를 공통 모듈로 둔다.
- APM, 에러 트래커(Sentry 등), 분석 SDK의 이벤트 속성에도 CI가 들어간다. 사용자 식별자로 CI를 쓰지 말고 내부 회원 ID를 쓴다.
- 데이터 웨어하우스로 복제할 때는 평문 컬럼을 제외하거나 분석 전용 키로 다시 HMAC 처리한다.
- 운영자가 쓰는 관리 도구 화면과 CSV 내보내기에서도 CI를 노출하지 않는다.

### 코드 예시

Python과 `cryptography` 패키지를 쓴 예시다.
키는 환경 변수로 받지만 실제로는 KMS에서 가져오거나
KMS의 데이터 키로 대체한다.

```python
import base64
import hashlib
import hmac
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from person_key import normalized_ci, random_test_ci

NONCE_LENGTH = 12

INDEX_KEY_VERSION = "v1"
INDEX_KEY = base64.b64decode(os.environ["CI_INDEX_KEY_B64"])
ENC_KEY_VERSION = "v1"
ENC_KEY = base64.b64decode(os.environ["CI_ENC_KEY_B64"])


def ci_index(ci: str) -> str:
    return with_version(INDEX_KEY_VERSION, hmac_hex(INDEX_KEY, normalized_ci(ci)))


def encrypt_ci(ci: str, member_id: str) -> str:
    nonce = os.urandom(NONCE_LENGTH)
    ciphertext = AESGCM(ENC_KEY).encrypt(nonce, normalized_ci(ci), member_id.encode())
    return with_version(ENC_KEY_VERSION, base64.b64encode(nonce + ciphertext).decode())


def decrypt_ci(token: str, member_id: str) -> str:
    payload = base64.b64decode(payload_of(token, expected_version=ENC_KEY_VERSION))
    nonce, ciphertext = payload[:NONCE_LENGTH], payload[NONCE_LENGTH:]
    return AESGCM(ENC_KEY).decrypt(nonce, ciphertext, member_id.encode()).decode("ascii")


def hmac_hex(key: bytes, message: bytes) -> str:
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def with_version(version: str, value: str) -> str:
    return f"{version}:{value}"


def payload_of(token: str, expected_version: str) -> str:
    version, payload = token.split(":", 1)
    if version != expected_version:
        raise ValueError(f"알 수 없는 키 버전: {version}")
    return payload


def rejects_other_member(token: str, other_member_id: str) -> bool:
    try:
        decrypt_ci(token, other_member_id)
    except InvalidTag:
        return True
    return False


if __name__ == "__main__":
    ci = random_test_ci()
    token = encrypt_ci(ci, "member-42")

    print("인덱스가 결정적이다:", ci_index(ci) == ci_index(ci))
    print("같은 회원은 복호화된다:", decrypt_ci(token, "member-42") == ci)
    print("다른 회원으로는 복호화되지 않는다:", rejects_other_member(token, "member-43"))
```

nonce는 암호화할 때마다 새로 만든다.
같은 키로 nonce를 다시 쓰면 GCM의 기밀성과 무결성이 함께 깨지기 때문이다.
회원 ID는 AAD로 묶어,
암호문을 다른 회원 행에 옮겨 붙이면 복호화가 실패하게 한다.
`person_key.py`와 같은 디렉터리에 두고
다음처럼 실행하면 세 줄 모두 `True`로 끝난다.

```bash
export CI_INDEX_KEY_B64=$(python3 -c "import os,base64;print(base64.b64encode(os.urandom(32)).decode())")
export CI_ENC_KEY_B64=$(python3 -c "import os,base64;print(base64.b64encode(os.urandom(32)).decode())")
python3 ci_crypto.py
```

같은 기능의 Java 예시다.
JDK만으로 돌아가며, 마지막 검사는 다른 회원 ID(AAD)로 복호화하면
실패하는지 확인한다.

```java
import java.nio.charset.StandardCharsets;
import java.security.GeneralSecurityException;
import java.security.SecureRandom;
import java.util.Arrays;
import java.util.Base64;
import java.util.HexFormat;
import javax.crypto.AEADBadTagException;
import javax.crypto.Cipher;
import javax.crypto.Mac;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;

/**
 * 조회용 HMAC 인덱스와 원본 복원용 AES-256-GCM 암호문을 만든다.
 * 암호문은 원본 CI를 다시 보내야 하는 서비스에서만 저장한다.
 */
public final class CiCrypto {
    private static final SecureRandom RANDOM = new SecureRandom();
    private static final int KEY_LENGTH = 32;
    private static final int CI_LENGTH = 88;
    private static final int NONCE_LENGTH = 12;
    private static final int TAG_BITS = 128;

    private final String indexKeyVersion;
    private final SecretKeySpec indexKey;
    private final String encryptionKeyVersion;
    private final SecretKeySpec encryptionKey;

    /**
     * 버전이 붙은 인덱스 키와 암호화 키로 만든다.
     *
     * @param indexKeyVersion 인덱스 키 버전
     * @param indexKey 32바이트 HMAC 키
     * @param encryptionKeyVersion 암호화 키 버전
     * @param encryptionKey 32바이트 AES 키
     */
    public CiCrypto(String indexKeyVersion, byte[] indexKey,
            String encryptionKeyVersion, byte[] encryptionKey) {
        this.indexKeyVersion = indexKeyVersion;
        this.indexKey = new SecretKeySpec(requireKeyLength(indexKey), "HmacSHA256");
        this.encryptionKeyVersion = encryptionKeyVersion;
        this.encryptionKey = new SecretKeySpec(requireKeyLength(encryptionKey), "AES");
    }

    /**
     * 같은 CI에 항상 같은 값을 내는 조회용 인덱스를 만든다.
     *
     * @param ci 본인확인기관이 준 88자 CI
     * @return 키 버전이 붙은 HMAC-SHA256 16진 문자열
     * @throws GeneralSecurityException HMAC을 쓸 수 없을 때
     */
    public String ciIndex(String ci) throws GeneralSecurityException {
        return withVersion(indexKeyVersion, HexFormat.of().formatHex(hmac(normalizedCi(ci))));
    }

    /**
     * 회원 ID를 AAD로 묶어 CI를 암호화한다.
     *
     * @param ci 본인확인기관이 준 88자 CI
     * @param memberId 암호문이 속한 회원 ID
     * @return 키 버전이 붙은 nonce와 암호문의 Base64 문자열
     * @throws GeneralSecurityException 암호화에 실패했을 때
     */
    public String encryptCi(String ci, String memberId) throws GeneralSecurityException {
        byte[] nonce = newNonce();
        byte[] ciphertext = cipher(Cipher.ENCRYPT_MODE, nonce, memberId).doFinal(normalizedCi(ci));
        return withVersion(encryptionKeyVersion, base64(concat(nonce, ciphertext)));
    }

    /**
     * 같은 회원 ID로만 암호문을 복호화한다.
     *
     * @param token encryptCi가 만든 문자열
     * @param memberId 암호문이 속한 회원 ID
     * @return 원본 CI
     * @throws GeneralSecurityException 키 버전이나 회원 ID가 맞지 않을 때
     */
    public String decryptCi(String token, String memberId) throws GeneralSecurityException {
        byte[] payload = Base64.getDecoder().decode(payloadOf(token));
        byte[] nonce = Arrays.copyOfRange(payload, 0, NONCE_LENGTH);
        byte[] ciphertext = Arrays.copyOfRange(payload, NONCE_LENGTH, payload.length);
        return ascii(cipher(Cipher.DECRYPT_MODE, nonce, memberId).doFinal(ciphertext));
    }

    private byte[] hmac(byte[] message) throws GeneralSecurityException {
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(indexKey);
        return mac.doFinal(message);
    }

    private Cipher cipher(int mode, byte[] nonce, String memberId) throws GeneralSecurityException {
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(mode, encryptionKey, new GCMParameterSpec(TAG_BITS, nonce));
        cipher.updateAAD(memberId.getBytes(StandardCharsets.UTF_8));
        return cipher;
    }

    private String payloadOf(String token) {
        String[] versionAndPayload = token.split(":", 2);
        requireVersion(versionAndPayload[0], encryptionKeyVersion);
        return versionAndPayload[1];
    }

    private static void requireVersion(String actual, String expected) {
        if (!actual.equals(expected)) {
            throw new IllegalArgumentException("알 수 없는 키 버전: " + actual);
        }
    }

    private static byte[] normalizedCi(String ci) {
        String trimmed = ci.strip();
        if (trimmed.length() != CI_LENGTH) {
            throw new IllegalArgumentException("CI 길이가 " + CI_LENGTH + "자가 아닙니다");
        }
        return trimmed.getBytes(StandardCharsets.US_ASCII);
    }

    private static byte[] requireKeyLength(byte[] key) {
        if (key.length != KEY_LENGTH) {
            throw new IllegalArgumentException("키는 " + KEY_LENGTH + "바이트여야 합니다");
        }
        return key;
    }

    private static byte[] newNonce() {
        return randomBytes(NONCE_LENGTH);
    }

    private static String withVersion(String version, String value) {
        return version + ":" + value;
    }

    private static byte[] concat(byte[] head, byte[] tail) {
        byte[] joined = Arrays.copyOf(head, head.length + tail.length);
        System.arraycopy(tail, 0, joined, head.length, tail.length);
        return joined;
    }

    private static String base64(byte[] bytes) {
        return Base64.getEncoder().encodeToString(bytes);
    }

    private static String ascii(byte[] bytes) {
        return new String(bytes, StandardCharsets.US_ASCII);
    }

    private static byte[] randomBytes(int length) {
        byte[] bytes = new byte[length];
        RANDOM.nextBytes(bytes);
        return bytes;
    }

    private static boolean rejectsOtherMember(CiCrypto crypto, String token, String otherMemberId)
            throws GeneralSecurityException {
        try {
            crypto.decryptCi(token, otherMemberId);
        } catch (AEADBadTagException e) {
            return true;
        }
        return false;
    }

    /**
     * 인덱스의 결정성과 회원 ID 결속을 확인한다.
     *
     * @param args 쓰지 않는다
     * @throws GeneralSecurityException 암호 연산에 실패했을 때
     */
    public static void main(String[] args) throws GeneralSecurityException {
        CiCrypto crypto = new CiCrypto("v1", randomBytes(KEY_LENGTH), "v1", randomBytes(KEY_LENGTH));
        String ci = base64(randomBytes(66));
        String token = crypto.encryptCi(ci, "member-42");

        System.out.println("인덱스가 결정적이다: " + crypto.ciIndex(ci).equals(crypto.ciIndex(ci)));
        System.out.println("같은 회원은 복호화된다: " + crypto.decryptCi(token, "member-42").equals(ci));
        System.out.println("다른 회원으로는 복호화되지 않는다: " + rejectsOtherMember(crypto, token, "member-43"));
    }
}
```

JDK 11 이상에서는 컴파일 없이 바로 실행할 수 있고, 세 줄 모두 `true`가 나온다.

```bash
java CiCrypto.java
```

DB에는 `ci_hmac`에 유니크 인덱스를 걸고,
중복가입 확인은 `WHERE ci_hmac = :index`로 조회한다.
`ci_enc`는 원본이 정말 필요한 서비스에서만 둔다.

## 확인하지 못한 부분

- 평문 SHA-256 해시가 별표 4 제4-2호의 “안전한 알고리즘으로 암호화하여 저장”을 충족하는지에 대한 방미통위의 공식 유권해석은 찾지 못했다. 안내서 예시표에 일방향 알고리즘이 포함된 것까지만 확인했다.
- HMAC-SHA256을 같은 조항의 암호화로 인정하는지도 공식 문서에서 확인하지 못했다. 이 문서의 판단은 공학적 추론이다.
- 본인확인기관이 CI를 생성할 때 쓰는 구체적 알고리즘과 키 구조는 공개 문서에서 확인하지 못했다. “주민등록번호를 대입해 CI를 역산할 수 없다”는 설명은 법령과 안내서의 “비가역적·일방향” 정의에 근거한 것이다.
- 국가법령정보센터의 현행 법률 조문은 CI 안전조치 위반 과태료를 제76조제2항제2호의6에 두지만, 시행령 별표의 근거 조문 표기는 제76조제1항제2호의6으로 되어 있다. 한도 3천만 원과 기준 금액은 양쪽이 일치한다.
- 롯데카드 과태료의 가중 사유와 로그 평문 기록 경위는 방미통위 보도자료 원문이 아니라 언론 보도로 확인했다.
- 행정예고 공고 번호(제2026-199호)와 예고일은 법무법인 뉴스레터에서 확인했고 방미통위 공고 원문은 직접 열람하지 못했다.

## 참고 자료

- [정보통신망 이용촉진 및 정보보호 등에 관한 법률 (국가법령정보센터)](https://www.law.go.kr/lsInfoP.do?lsiSeq=290001)
- [정보통신망 이용촉진 및 정보보호 등에 관한 법률 시행령 (국가법령정보센터)](https://www.law.go.kr/lsInfoP.do?lsiSeq=290483)
- [연계정보의 생성ㆍ처리 등에 관한 기준, 방송미디어통신위원회고시 제2026-28호 (국가법령정보센터)](https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000285914)
- [개인정보의 안전성 확보조치 기준, 개인정보보호위원회고시 제2026-9호 (국가법령정보센터)](https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000281400)
- [연계정보 처리 및 안전조치 등에 관한 안내서, 2025년 6월 (KISA 본인확인 홈페이지)](https://identity.kisa.or.kr/web/main/file/download/uu/98dbd5af85ff46edb17e6e1633be0b9c)
- [연계정보의 생성·처리 등에 관한 기준 제2026-11호 PDF (KISA 본인확인 홈페이지)](https://identity.kisa.or.kr/web/main/file/download/uu/ec198547dafe46c19c228116a5d5652e)
- [연계정보 생성·처리 기준 개정 행정예고 해설 (법무법인 세종 뉴스레터)](https://www.shinkim.com/kor/media/newsletter/3332)
- [잇단 CI 유출에 방미통위, CI·주민번호 분리보관 4개월 앞당긴다 (디지털데일리)](https://www.ddaily.co.kr/page/view/2026061215252392221)
- [온라인 주민번호 CI 잇단 유출에 정부 관리체계 손본다 (데일리안)](https://www.dailian.co.kr/news/view/1655333/)
- [롯데카드 해킹 책임에 과태료 1125만원, 연계정보 안전조치 위반 (뉴스1)](https://www.news1.kr/it-science/security-hacking/6153222)
- [연계정보 안전조치 의무 위반 롯데카드에 과태료 부과 (다자비)](https://dazabi.com/insurance_magazine/article.php?id=19281)
- [개인정보위, 개인정보의 안전성 확보조치 기준 안내서 공개 (보안뉴스)](https://www.boannews.com/news/articleView.html?idxno=133982)
- [HMAC keys in AWS KMS (AWS KMS 개발자 안내서)](https://docs.aws.amazon.com/kms/latest/developerguide/hmac.html)
- [GenerateMac (AWS KMS API 레퍼런스)](https://docs.aws.amazon.com/kms/latest/APIReference/API_GenerateMac.html)
