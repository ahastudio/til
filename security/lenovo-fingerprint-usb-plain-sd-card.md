# Lenovo의 “암호화” 지문 USB는 평문 SD 카드였다: 비밀번호가 키가 아니라 프로그램의 문을 여는 제품들

원문: [Lenovo's 'encrypted' fingerprint USB drive is just an unencrypted SD card in a fancy case — AI-assisted follow-up finds a backdoor and hardcoded keys in other ‘secure’ USB products | Tom's Hardware](https://www.tomshardware.com/tech-industry/cyber-security/lenovo-fingerprint-usb-stick-sold-as-aes-256-encrypted-had-a-plain-sd-card-inside-ai-assisted-follow-up-finds-a-backdoor-and-hardcoded-keys-in-other-secure-usb-products)

HN 토론: <https://news.ycombinator.com/item?id=50326099> (406점, 148개 댓글)

## 요약

Tom's Hardware는 2026년 11월 1일, 보안 연구자 Xusheng Li의 분석을
HackingPassion이 보도한 내용을 바탕으로 이 기사를 냈다.
Lenovo ThinkPlus FU100 지문 USB 드라이브는 AES-256으로 암호화된다고 팔렸지만
내부는 일반 SD 카드였다.
지문 인식기는 USB 연결을 켜는 일만 했고, 카드에 담긴 데이터는 전혀 암호화되어
있지 않았다.
기사는 이 장치를 Li가 3월 학회 발표에서 “just an SD card in a fancy case”라고
부른 말로 설명한다.
물리적으로 접근할 수 있는 사람은 누구나 데이터를 꺼낼 수 있고, Li는 “하드웨어
보안은 순수한 마케팅일 수 있다”고 정리했다.

Lenovo의 대응 경과는 이렇게 전해진다.
FU100 분석은 작년에 이루어졌고 임시 조치는 SD 카드 위에 에폭시를 바르는
것이었다.
올해 초 FU100, FU200, TU800 드라이브와 TSD303 SSD에 대한 나중의 수정은 소유자가
중국 서비스 전화로 연락한 뒤 장치를 보내 교체하거나 현장에서 펌웨어를 올리는
방식이다.
Lenovo는 먼저 백업하고 장치를 보내기 전에 지우라고 강하게 권한다.
Lenovo는 권고문의 심각도를 높음으로 평가했고, 세 개의 CVE 중 하나는 설정
소프트웨어가 로컬에 로그인한 사용자에게 장치 인증을 우회해 신뢰할 수 없는 지문을
등록하게 한다는 내용이다.

같은 연구는 TSD303 외장 SSD의 다른 결함도 찾았다.
데이터는 실제로 암호화되어 있었지만 드라이브가 올바른 비밀번호를 USB로 평문
그대로 소프트웨어에 돌려보내 비교하게 했으므로 가로채기가 쉬웠다.
첫 번째 수정은 보고 3개월 뒤에 나왔고 타임스탬프 같은 값에서 키를 만든 블록
암호를 썼는데, 소프트웨어가 그 키를 만들어 낼 수 있어서 장치를 도난당했을 때
쓸모가 없었다.
작년 말의 수정은 드라이브가 입력된 비밀번호를 스스로 검사하게 해서 올바른
비밀번호가 드라이브 밖으로 나가지 않는다.
같은 소프트웨어 개발 키트(SDK)가 여러 제조사의 다른 아홉 장치에도 쓰였고,
대부분이 숙련된 공격자에게 비밀번호를 드러낼 수 있었으며 둘은 microSD 카드에
데이터를 암호화하지 않고 두었다.
제조사 목록은 Li의 슬라이드에서 가려져 있었다.

기사는 이어 AI를 쓴 후속 분석을 소개한다.
Li는 OpenAI의 Codex를 자신의 회사의 리버스 엔지니어링 도구와 함께 다른 제조사의
보호 방식에 썼다.
Netac의 도구는 약 7분 만에 뚫렸는데, Codex가 프로그램에 내장된 고정 키를 찾았고
사용자의 비밀번호가 진단 로그에 적혀 있었다.
복제 방지(copy protection) 제품인 KakaSoft의 USB Copy Protection은 프로그램이
스스로 만드는 내부 비밀번호를 Codex가 재구성해 사용자의 비밀번호 없이 약 26분
만에 시험 파일을 복호화했다.
Nexcopy의 Copy Secure는 약 10분이 걸렸고, 뷰어 앱에 내장된 인증서로 키가 풀렸다.
SecZure의 YutianDun에는 단순한 비밀번호를 가진 숨은 “백도어” 계정 두 개가
있었고, 시간 여행 디버깅(time-travel debugging)으로 찾았지만 Li의 말로는 악의가
있었다고 단정할 수 없다.
Li는 KakaSoft, Nexcopy, SecZure에 경고하지 않았는데, 이미 공격자 손에 있는
드라이브는 회수하거나 갱신하기 어렵기 때문이라고 한다.

## 분석

### 비밀번호와 지문은 키를 만들지 않고 문만 지켰다

기사가 소개하는 제품들의 공통 구조는 인증이 키와 무관하다는 점이다.
FU100에서는 지문이 USB 연결을 켤지만 정하고 데이터는 암호화되어 있지 않았다.
TSD303에서는 데이터가 암호화되어 있었지만 비밀번호 비교를 컴퓨터의
프로그램이 했다.
Netac에서는 키가 프로그램에 고정되어 있었고 비밀번호는 키와 별도로 검사되었다.

HackingPassion은 이를 한 문장으로 요약한다.
대부분의 제품에서 비밀번호는 프로그램을 열거나 USB 연결을 켜는 일을 결정했고
파일을 잠근 키의 일부가 아니었다는 것이다.[^hackingpassion]
키가 소프트웨어 안의 고정 값이거나 데이터가 암호화되지 않았다면 비밀번호는
프로그램을 보호할 뿐이고 파일은 카드를 읽거나 프로그램을 분해하는 사람에게 열려
있다고 한다.[^hackingpassion]
반대로 제대로 된 암호화는 키를 비밀번호에서 느린 함수(PBKDF2나 Argon2 같은)로
만들거나, 비밀번호 확인을 드라이브의 칩 안에서 해서 비밀번호도 키도 칩 밖으로
나가지 않게 한다고 HackingPassion은 설명한다.[^hackingpassion]
이 구분이 제품 평가의 핵심 질문이 된다. 키는 어디에서 오는가.

### Lenovo 사례의 수정은 장치를 회수해야 하는 형태였다

슬라이드의 공개 일정은 2025년 8월 최초 보고, 9월부터 11월까지 여러 실패하거나
임시인 수정, 12월 최종 수정 확인, 2026년 1월 CVE 세 개 부여, 2026년 3월
RE//verse 발표다.[^li-slides]
같은 슬라이드는 사용자가 수정을 적용하려면 기존 장치를 서비스에 맡겨야 한다고
적는다.[^li-slides]
HackingPassion에 따르면 Li는 2025년 8월 2일에 Lenovo에 보고했고 8월 27일에
에폭시라는 임시 조치가 나왔으며 제대로 된 수정은 12월로
계획되었다.[^hackingpassion]
Lenovo의 권고문 LEN-210545는 2026년 1월 13일에 나왔고 CVE-2025-13453,
CVE-2025-13454, CVE-2025-13455를 포함하며 영향받는 모델은 FU100, FU200, TU800,
TSD303이라고 한다.[^hackingpassion]
기사는 세 번째 CVE만 소개하고 나머지 둘은 말하지 않는다.
CVE-2025-13454는 설정 소프트웨어가 로컬에 로그인한 사용자에게 민감한 장치 정보에
접근하게 한다고 HackingPassion은 적는다.[^hackingpassion]

데이터가 이미 평문으로 저장된 장치는 펌웨어 갱신으로 과거 데이터가 암호화되지
않는다.
Lenovo가 먼저 백업하고 장치를 지운 뒤 보내라고 권하는 것이 그 이유로 읽힌다.
이는 이 문서의 해석이다.

### AI가 짧은 시간에 한 일은 클라이언트 쪽 검증의 분해다

Codex가 한 일은 프로그램을 분석해 고정 키, 내장된 인증서, 내부 비밀번호를 찾는
것이다.
HackingPassion에 따르면 Netac 분석은 약 7분, KakaSoft는 약 26분에 프롬프트 여섯
개, Nexcopy는 약 10분에 프롬프트 다섯 개가 걸렸다.[^hackingpassion]
Li는 이 과정에서 “클라이언트 쪽 검증은 절대 안전하지 않다”고 말했고 보안 주장은
직접 확인하라고 했다고 기사는 전한다.
여기서 AI의 역할은 새 공격 기법이 아니라 이미 알려진 약점의 탐색 비용을 낮춘
것이다.
이는 이 문서의 해석이다.

## 비평

### 제목은 AI가 백도어와 고정 키를 찾았다고 읽히지만 자료가 말하는 범위는 더 좁다

기사 제목은 “AI를 쓴 후속 조사가 백도어와 고정 키를 찾았다”는 구조다.
본문에서 AI가 한 일로 명시된 것은 Netac, KakaSoft, Nexcopy에 대한 Codex
분석이다.
YutianDun의 숨은 계정은 시간 여행 디버깅으로 찾았다고만 쓰여 있다.
HackingPassion은 YutianDun을 Li가 이미 알던 드라이브라고 하며 2024년에 Paged
Out! 잡지에 글을 쓴 적이 있고, 분석에서 숨은 계정 Buffer(비밀번호 123456)를 찾은
뒤 두 번째 계정 System(비밀번호 SECZURE.COM)이 나왔다고 쓴다.[^hackingpassion]
그 페이지는 이 분석에 Codex가 쓰였다고 말하지 않는다.
따라서 이 문서가 읽은 자료로는 백도어가 AI를 쓴 후속 조사의 결과라는 제목의
전제를 확인할 수 없다.

Lenovo 사례에서도 같은 간극이 있다.
HN에서 charles_f는 Lenovo 건에서 Codex가 무엇을 도왔는지 모르겠다며, 드라이브를 열어 SD 카드를 컴퓨터에 꽂으면 되는 일이었다고 썼다.[^charles_f]
기사 속 FU100 분석은 2025년의 일이고 Codex를 쓴 후속 작업은 2026년 10월이다.
기사는 AI 후속 조사를 Lenovo 사례와 한 기사에서 함께 다루지만, 둘은 시기도
방법도 다른 작업이다.

### “하드웨어 보안은 마케팅”이라는 결론은 확인된 제품 수보다 넓다

Li의 말은 “하드웨어 보안은 순수한 마케팅일 수 있다”이고, 기사는 이를 일반
교훈처럼 쓴다.
기사와 HackingPassion이 확인한 사례는 FU100, TSD303, 같은 SDK를 쓰는 아홉
장치(제조사 이름이 슬라이드에서 가려짐), Netac, KakaSoft, Nexcopy, SecZure다.
이 가운데 Netac, KakaSoft, Nexcopy, SecZure는 복제 방지나 파일 암호화
소프트웨어이고, 하드웨어 칩이 키를 지키는 구조의 제품이 아니다.

HN에서 gruez는 구현이 올바르다면 하드웨어 암호화가 소프트웨어 암호화보다 안전할 수 있다고 맞섰다.[^gruez]
그는 가장 분명한 이점으로 무차별 대입 방어를 들었고, 소프트웨어로는 의미 있게
구현할 수 없다고 했다.[^gruez]
miki123211은 보통 사용자가 원하는 것은 6자리 PIN으로 보호되는 AES 키를 안전하게
저장하는 잠긴 칩이라고 썼다.[^miki123211]
xoa는 “쓸모없다” 같은 단어는 맥락 없이 쓰면 진지하지 않으며 보안은 경제와 위협
시나리오의 문제라고 했다.[^xoa]
그는 2019년 논문 “Self-Encrypting Deception”을 알고 있다고 썼다.[^xoa]
기사의 결론은 확인된 결함의 범위에서 더 나아간 것이고, 하드웨어 암호화 일반에
대한 판단은 별도의 근거가 필요하다.

### 영향을 받은 사용자와 실제 악용은 어디에도 없다

기사는 이 결함이 얼마나 많은 사용자에게 영향을 주었는지, 악용된 적이 있는지를
말하지 않는다.
HackingPassion은 Lenovo도 연구자도 소유자에 대한 공격을 언급하지 않는다고
쓴다.[^hackingpassion]
HN에서 forgotpwd16은 이 제품이 ThinkPlus USB 제품군 전체와 함께 중국 밖에서는 구할 수 없었던 것 같다며, 제품은 2019년에 발표되었고 결함은 2025년 8월에 발견되었으며 CVE는 1월에 나왔고 Li의 발표는 3월이었다고 정리했다.[^forgotpwd16]
이는 그의 추정이고 이 문서가 확인한 것이 아니다.
영향 범위가 제한적일 수 있지만 그 판단에 필요한 판매량이나 판매 지역은
기사에 없다.

## 인사이트

### 서비스로 고쳐야 하는 결함은 공개 시점의 판단을 어렵게 만든다

Lenovo의 수정은 장치 회수와 초기화가 필요한 형태다.
Li는 KakaSoft, Nexcopy, SecZure에 경고하지 않은 이유로, 공격자 손에 있는
드라이브는 회수하거나 갱신하기 어렵다는 점을 들었다.
이 두 사실이 같은 방향을 가리킨다.
배포된 하드웨어는 소프트웨어처럼 고칠 수 없으므로 사전 경고로 얻는 이득이 작고,
경고 없이 공개했을 때 소유자의 선택지는 데이터를 다른 방식으로 암호화하는
것뿐이다.
이는 이 문서의 해석이다.

HackingPassion이 소유자에게 권하는 행동도 같은 결론이다.
민감한 파일은 스틱에 올리기 전에 비밀번호에서 키를 만드는 소프트웨어(VeraCrypt,
Windows Pro의 BitLocker To Go, gpg)로 직접 암호화하고, 지문 인식기나 비밀번호
화면은 제조사가 키가 그것에 의존함을 보이지 않는 한 접근을 막는 자물쇠로만
보라는 것이다.[^hackingpassion]
HN의 bentcorner는 Lenovo가 이렇게 작동한다고 솔직히 광고했다면 오히려 나았을 것이라고 썼다.[^bentcorner]
암호화를 하지 않는 것이 하고서 어딘가 실수하는 것보다 쉽고, 지문은 정직한 사람을
정직하게 지키는 용도로 알려졌을 것이라는 것이다.[^bentcorner]

### 규제와 조달이 검증되지 않은 제품을 요구하는 구조가 있다

HN에서 alright2565는 정부 규정 때문에 비슷한 제품의 사용을 요구받았고 신뢰하지 않았으며 15분만 뜯어보고 싶었지만 정부가 의무화한 일이라 어쩔 수 없었다고 썼다.[^alright2565]
advisedwang은 이런 제품이 재해 복구에는 좋다고 했다.[^advisedwang]
일상에서는 TPM에 묶인 소프트웨어 암호화를 쓰고, 그것이 모두 망가졌을 때 금고에
둔 하드웨어 암호화 장치에 루트 키 자료를 두는 방식이다.[^advisedwang]
두 댓글은 이 제품이 쓰이는 이유가 보안 성능이 아니라 요구 사항이나 운영 편의일
수 있음을 보여 준다.

제품의 암호화가 검증되지 않아도 규정 준수 목록에는 오를 수 있다는 점이 문제다.
이는 이 문서의 추론이다.
제품 선택이 검증된 암호 설계가 아니라 인증이나 마케팅 문구에 기대면, 이 기사의
경우처럼 한 사람이 장치를 뜯어 보기 전까지 결함이 드러나지 않는다.

### 클라이언트 분석 비용이 분 단위로 내려가면 의존할 비밀은 서버나 칩 안에만 남는다

Netac 분석이 7분, Nexcopy가 10분, KakaSoft가 26분이라는 숫자는 프로그램에 고정
키나 내장 인증서를 넣는 설계가 더는 버티지 못한다는 뜻이다.
HackingPassion에 따르면 2009년 SySS가 FIPS 140-2 인증을 받은 SanDisk USB를 깼고
CVE 기록은 SanDisk Cruzer Enterprise와 Kingston DataTraveler 세 모델을 언급하며,
이 드라이브들이 컴퓨터에서 도는 프로그램으로 비밀번호를 검증하고 고정 256비트
키를 썼다고 한다.[^hackingpassion]
16년 뒤 같은 실수가 반복되었다는 것이 HackingPassion의 평가이고, 이 문서가 그
역사 서술을 따로 확인하지는 않았다.

여기서 얻는 판단 규칙은 단순하다.
제품 설명을 읽을 때 키가 비밀번호에서 만들어지는지, 비밀번호 확인이 칩 안에서
일어나는지, 둘 다 아니라면 비밀번호는 프로그램의 문일 뿐이라고 가정한다.
이 규칙에 어긋나는 증거, 곧 키가 비밀번호에 의존하면서도 확인이 컴퓨터에서
일어나는 설계가 안전함을 보인 사례가 나오면 규칙은 완화된다.
이 문서가 읽은 자료에는 그런 사례가 없다.

---

[^hackingpassion]: HackingPassion, [Lenovo ThinkPlus Fingerprint USB Drive Sold as Encrypted Was a Plain SD Card Inside - HackingPassion.com](https://hackingpassion.com/lenovo-thinkplus-encrypted-usb-sd-card/), 2026-10-29

[^li-slides]: Xusheng Li(Vector 35), [Breaking Encrypted USB Drives with Time-Travel Debugging](https://github.com/xusheng6/breaking_encrypted_USB_drives_with_TTD/blob/main/Breaking_Encrypted_USB_Drives_v2.pdf)

[^charles_f]: <https://news.ycombinator.com/item?id=50327530>

[^gruez]: <https://news.ycombinator.com/item?id=50326689>

[^miki123211]: <https://news.ycombinator.com/item?id=50328424>

[^xoa]: <https://news.ycombinator.com/item?id=50329043>

[^forgotpwd16]: <https://news.ycombinator.com/item?id=50327280>

[^bentcorner]: <https://news.ycombinator.com/item?id=50329598>

[^alright2565]: <https://news.ycombinator.com/item?id=50326381>

[^advisedwang]: <https://news.ycombinator.com/item?id=50328068>
