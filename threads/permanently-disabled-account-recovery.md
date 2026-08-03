# Threads 계정 영구 정지(permanently disabled) 복구하기

셀피 인증을 마쳤는데도 “Community Standards를 따르지 않는다”며 계정이 영구
정지된 사례와, 실제로 복구에 성공한 경로를 정리한다.

참고 자료: <https://www.reddit.com/r/ThreadsApp/comments/1rdcd74/threads_account_got_permanently_banned/>
(r/ThreadsApp, 2026년 2월 24일, u/NordenDerWelt, 업보트 60개·댓글 89개)

## 받은 메일

```text
We reviewed your account and found that it still doesn't follow our
Community Standards. As a result, your account has been permanently disabled.
```

“다시 검토했지만 여전히 커뮤니티 규정을 위반한다”는 문장이지만, 실제로는
사람이 검토한 결과가 아닐 가능성이 높다.

## 왜 이런 일이 생기나

레딧 글의 원 작성자도 상황이 똑같다.
글은 거의 쓰지 않고 읽기와 좋아요만 했는데, 봇이 아님을 확인하라는 요구를
받고 셀피까지 올린 뒤에 영구 정지 통보를 받았다.

댓글에서 반복적으로 확인되는 정황은 다음과 같다.

- **자동화된 대량 정지**다. “어젯밤에 광범위한 밴이 있었던 것 같다”는 증언이
  있고, 2026년 2월부터 5월까지 같은 증상의 댓글이 계속 달린다.
- **셀피 제출이 해제 조건이 아니다.** 셀피를 올린 뒤에 오히려 영구 정지된
  사례가 다수다. 인증 절차를 통과했다고 안전해지지 않는다.
- **계정 활동과 무관하다.** 새로 만든 계정, 오래 쓴 계정, 아무것도 안 올린
  계정이 고르게 걸렸다. 노트북이나 회사 네트워크에서 로그인한 뒤 걸렸다는
  증언이 여러 건이다.
- 한 사용자가 받은 정지 사유는 “가짜 계정 생성”이었다.
  본명이 아닌 활동명이나 브랜드명을 쓴 계정이 이 분류에 잘못 들어가는
  것으로 보인다.

정리하면, 앱 안에서 보이는 “이의 제기” 절차(전화번호 인증 → 셀피 제출)는
사람이 보지 않는다.
그 경로를 다 밟고 영구 정지가 확정됐다면 앱 안에서 할 수 있는 일은 남아 있지
않다. **다른 창구로 다시 넣어야 한다.**

## 실제로 통한 방법

원 작성자가 업데이트에 적어 둔 경로다.
Instagram 헬프센터의 “계정에 접근할 수 없습니다” 신고 양식을 통해 재검토를
요청했다.

<https://help.instagram.com/contact/6593513384024963>

이 양식으로 넣은 뒤 받은 답장은 다음과 같다.

```text
Thanks for taking the time to request a review. We reviewed your account and
found that the activity on it does follow our Community Guidelines, so you can
use Threads again.

We're sorry we got this wrong and that you weren't able to use Threads, for a
while.
```

앱 안에서 “영구 정지, 이의 제기 불가”라고 통보한 것과 같은 계정에 대해
“우리가 틀렸다”는 답이 왔다.
앱 내부 흐름과 이 신고 양식이 서로 다른 처리 라인이라는 뜻이다.

### 성공 사례

| 시점       | 사용자                | 결과                       |
| ---------- | --------------------- | -------------------------- |
| 2026-02-24 | u/NordenDerWelt       | 신청 약 1시간 후 복구      |
| 2026-03-20 | u/SignificantHurry5656| 신청 6일 후 복구           |
| 2026-05-15 | u/Infinite_sard       | 신청 5일 후 복구(VPN 사용) |

## 문제: EU 전용 창구다

이 양식은 EU 회원국 이용자를 위한 “단일 연락 창구(Single point of contact for
users in EU member states)”다.
영국·미국 등 EU 밖에서 접속하면 “Not Found” 페이지가 뜬다.
관련 안내 문서는 여기다.

<https://help.instagram.com/421572036923453/>

한국에서 그대로 열면 열리지 않을 가능성이 크다.

### 우회한 사례

브라질 사용자 u/Infinite_sard가 남긴 댓글이 가장 구체적이다.
4월 29일에 차단됐고 인터넷을 다 뒤져도 방법이 없었는데, 이 글의 업데이트를
보고 따라 했다고 한다.
브라질에서 링크를 열면 페이지 오류가 나서 **VPN을 독일로 설정해 접속**했고,
양식이 열려서 상황을 설명해 제출한 뒤 5일 만에 계정이 풀렸다.

미국 사용자 u/SolveSomeTrouble도 프랑스로 VPN을 잡고 같은 양식을 제출했다.

## 실행 순서

1. **VPN을 EU 국가(독일·프랑스 등)로 설정**한다.
2. <https://help.instagram.com/contact/6593513384024963> 를 연다.
   페이지가 정상적으로 뜨는지 먼저 확인한다.
3. 양식의 각 항목을 채운다. 아래 “양식 작성 항목” 참고.
4. 본문에 상황 설명을 적는다. 아래 “제출 문구” 참고.
5. 제출 후 대기한다. 사례상 1시간에서 6일까지 편차가 크다.
6. 답장은 Instagram 계정에 연결된 메일로 온다.

### 준비물

제출 전에 미리 모아 둔다. 양식 페이지에서 되돌아가면 입력이 날아간다.

| 항목                | 내용                                             |
| ------------------- | ------------------------------------------------ |
| Threads 사용자명    | `@` 없이 정확한 철자로                           |
| Instagram 사용자명  | Threads에 연결된 계정                            |
| 연락 가능한 이메일  | 계정에 등록된 주소를 쓰는 편이 확인에 유리하다   |
| 정지 통보 메일      | 받은 원문 전체. 스크린샷도 함께 준비             |
| 정지 시점           | 통보 메일을 받은 날짜와 대략의 시각              |
| 앱 내 화면 캡처     | “permanently disabled” 안내가 보이는 화면        |

셀피 제출 화면이나 전화번호 인증 화면을 캡처해 두었다면 그것도 챙긴다.
자동 절차를 이미 다 밟았다는 증거가 된다.

### 양식 작성 항목

양식은 영어로 작성한다. 한국어로 쓰면 처리가 지연되거나 자동 분류에서
빠질 수 있다.

- **문의 유형** — 계정에 접근할 수 없다는 취지의 항목을 고른다.
  “disabled account” 계열 선택지가 있으면 그것을 고른다.
- **서비스** — Threads를 고른다. 선택지에 없으면 Instagram을 고르고 본문
  첫 줄에 Threads 계정 문제임을 명시한다.
- **국가** — 실제 거주지를 적는다. VPN은 페이지 접근용이지 거짓 진술을
  하라는 것이 아니다. 국적을 속이면 나중에 그것이 정지 사유가 될 수 있다.
- **본문** — 아래 문구를 붙여 넣고 대괄호 부분을 채운다.
- **첨부** — 통보 메일과 앱 화면 캡처를 올린다.

### 제출 문구

그대로 복사해서 대괄호만 채우면 된다.

```text
Subject: Threads account permanently disabled in error — request for human review

Hello,

My Threads account was permanently disabled and I am unable to access it. I
believe this was an automated decision made in error, and I am requesting a
human review.

Account details:
- Threads username: [threads_username]
- Linked Instagram username: [instagram_username]
- Email registered to the account: [email]
- Date the account was disabled: [YYYY-MM-DD]
- Country of residence: [country]

What happened:
On [YYYY-MM-DD] I was asked to verify that I am not a bot. I completed the
phone number verification and uploaded a selfie as requested. A few hours
later I received the following email:

"We reviewed your account and found that it still doesn't follow our
Community Standards. As a result, your account has been permanently disabled."

Why I believe this is an error:
I have not violated the Community Standards. [여기에 실제 사용 방식을 적는다.
예: I used the account almost entirely for reading. I posted very rarely, and
my posts contained no prohibited content. I did not use automation, and I did
not operate multiple accounts.]

I completed every verification step that was requested of me, including the
selfie, and the account was still permanently disabled. There is no remaining
appeal option available to me inside the app.

Please review this decision and restore my account.

Thank you.
[이름]
```

**대괄호 채울 때 주의할 점.**

- 사실만 적는다. 확인되지 않은 추측이나 과장은 넣지 않는다.
- “아무것도 안 했는데 왜 이러느냐”는 감정 표현은 뺀다. 판단에 도움이 되지
  않는다.
- 사용 방식 설명이 가장 중요한 부분이다. 게시물을 거의 올리지 않았다,
  자동화 도구를 쓴 적이 없다, 계정을 하나만 운영한다 — 이런 구체적 사실을
  적는다. 정지 사유가 “가짜 계정 생성”으로 분류되는 사례가 많기 때문에
  **계정을 하나만 쓴다는 진술은 특히 유용하다.**
- 활동명이나 브랜드명을 계정명으로 쓰고 있다면 그것이 무엇인지 설명한다.
  본명이 아닌 이름이 “신원을 숨김”으로 오분류되는 정황이 있다.

### 답장이 오면

복구되는 경우 이런 형태의 메일이 온다.

```text
Thanks for taking the time to request a review. We reviewed your account and
found that the activity on it does follow our Community Guidelines, so you can
use Threads again.
```

거절되거나 2주 이상 답이 없으면 같은 양식으로 한 번 더 제출한다.
이때는 첫 제출 날짜와 참조 번호(있다면)를 본문에 넣고, 이전 요청에 대한
후속 문의임을 밝힌다.

### 병행할 것

- **GDPR 정보 주체 접근 요청(Subject Access Request)** — 영국 사용자
  u/wonder_aj가 택한 방법이다. 계정이 안 풀리더라도 최소한 내 데이터는
  받아낼 수 있고, 어떤 판단으로 정지됐는지 단서가 나올 수도 있다.
  Instagram 앱과 웹의 “내 정보 다운로드” 경로로도 일부 받을 수 있지만,
  정식 SAR은 헬프센터의 데이터 요청 양식으로 넣는다.
- **Threads 개발자 계정 태그** — 서브레딧의 자동 안내가 권하는 방법이다.
  Threads에서 `camroth`, `0xjessel`, `richz`, `chowfun_` 계정을 태그해
  문제를 공개적으로 알리는 것이다. 다만 계정이 정지된 상태에서는 쓸 수 없어서
  지인에게 부탁하거나 다른 플랫폼에서 언급하는 형태가 된다.
- **새 계정을 급하게 만들지 않는다.** 댓글에 새 계정을 만들었다가 3일 만에
  다시 정지됐다는 사례가 여러 건 있다. 같은 기기와 같은 IP에서 새 계정을
  만드는 것이 오히려 “차단 우회”로 분류될 위험이 있다. 원 계정 복구가
  확정된 뒤에 판단하는 편이 낫다.

### 하지 말 것

- **계정 복구를 대행해 준다는 업체에 돈을 주지 않는다.** Meta에는 유료
  복구 창구가 없다. 이런 제안은 예외 없이 사기다.
- **거짓 정보를 적지 않는다.** 특히 거주 국가를 EU로 속이는 것. 페이지
  접근을 위한 VPN과 양식에 거짓을 적는 것은 다른 문제이며, 후자는 새로운
  정지 사유가 된다.
- **같은 양식을 매일 반복 제출하지 않는다.** 중복 요청은 처리 대기열에서
  묶여 오히려 늦어질 수 있다. 2주 간격이 적당하다.
- **셀피를 다시 올리지 않는다.** 앱 안에서 같은 요구가 또 나오더라도 그
  경로는 이미 실패한 자동 루프다. 생체 정보를 한 번 더 넘기는 대가로 얻는
  것이 없다.

## 기대치 조정

성공 사례가 있지만 만능은 아니다.

- 같은 양식을 제출하고도 답을 못 받은 사례가 있다(u/Upyrz1160, 한 달 대기 후
  포기).
- 3개월 넘게 풀리지 않은 사례도 있다(u/JacketLazy5342).
- 6개월 전에 정지됐고 아무 방법이 없었다는 증언도 있다(u/hudsongrl1).

그래도 현재 알려진 경로 중 **실제 복구 사례가 확인된 유일한 창구**가 이
양식이다.
앱 안에서 “영구 정지”라고 나오는 것은 최종 상태가 아니다.

## 왜 이 구조가 되었나

여기서 흥미로운 것은 기술적 문제가 아니라 제도적 비대칭이다.

앱 안에 보이는 이의 제기 버튼은 자동 판정 시스템으로 되돌아가는 루프다.
셀피를 올려도 같은 시스템이 다시 판정하기 때문에 결과가 뒤집히지 않는다.
반면 EU 신고 양식은 디지털서비스법(DSA)이 플랫폼에 의무화한 연락 창구라서
다른 처리 경로를 탄다.
같은 회사, 같은 계정, 같은 사실관계인데 **법이 강제한 창구로 들어가면 사람이
본다.**

그래서 미국 사용자가 “미국에 있다는 이유만으로 아무 지원도 못 받는다”고
쓰고, 브라질 사용자가 VPN으로 독일에 접속해서 자기 계정을 되찾는 상황이
벌어진다.
소비자 보호 규제가 있는 관할과 없는 관할 사이에서 같은 서비스의 실질적 품질이
갈리는 것이다.
규제가 만든 창구가 규제 대상 지역 밖 사용자에게 유출되어 쓰이고 있는 셈인데,
이것은 규제의 효과가 국경을 넘는 흔치 않은 사례다.

또 하나. 셀피 인증이 계정을 지키는 절차가 아니라는 점은 기록해 둘 만하다.
얼굴 사진을 제출하고도 영구 정지된 사례가 이 스레드에만 여럿이다.
생체 정보를 넘겼는데 그 대가로 아무것도 보장받지 못한 것이다.
댓글에도 “셀피를 위해 사진까지 줬는데 아무 소용이 없었다”는 반응이 반복된다.
신원 확인 요구를 받았을 때 그것이 어떤 보장과 교환되는지 확인할 방법이 없다는
사실 자체가, 이런 절차를 대하는 기준이 되어야 한다.
