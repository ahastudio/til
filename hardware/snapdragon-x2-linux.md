# Snapdragon X2의 Linux 지원 선언: 두 번째 약속을 믿어도 되는지는 드라이버가 어디에 들어가느냐에 달렸다

원문: [Inside Snapdragon Summit 2026: Agentic AI PCs, Googlebooks and Linux](https://www.qualcomm.com/news/onq/2026/09/snapdragon-summit-agentic-ai-pcs-linux)

HN 토론: <https://news.ycombinator.com/item?id=49823582> (614점, 266개 댓글)

GN 토론: <https://news.hada.io/topic?id=34210>

## 요약

Qualcomm이 2026년 9월 Snapdragon Summit의 PC 부문 발표를 정리한 글이다.
글의 큰 틀은 “에이전트 시대”다.
사람이 통제권을 유지한 채 AI 에이전트가 함께 일하는 시대에, Snapdragon X2 프로세서가 대답만 하는 것이 아니라 행동하는 에이전트 흐름을 PC에서 로컬로, 효율적으로, 대규모로 돌린다는 것이다.
데모로는 AnythingLLM과 ON1 Photo RAW를 묶은 사진 라이브러리 검색, 필요할 때만 큰 모델로 올려 보내는 Clairvoyance AI의 계층형 에이전트, Deepgram의 실시간 팟캐스트 전사, Pokee와 Halo의 화상 회의 보안 에이전트를 든다.

생태계 숫자도 내세운다.
120곳이 넘는 소매 협력사의 12,300개 넘는 매장이 Snapdragon PC를 팔고, 13,000곳 넘는 기업이 도입했거나 시험했으며, 7,300개 넘는 애플리케이션이 이 PC에서 돈다고 한다.
Google과 함께 Snapdragon X Elite를 Gemini Intelligence용 Googlebook 노트북에 넣고, Dell XPS Googlebook과 HP Googlebook 14가 나오며, Android 앱을 네이티브로 지원한다고 밝힌다.
Microsoft Surface Pro 12인치와 Surface Laptop 13인치는 Snapdragon X2 Plus로 이전 세대보다 로컬 AI 추론이 80% 빠르고 GPU 성능이 최대 55% 좋아졌다고 한다.

이 글에서 가장 주목받은 부분은 Linux다.
Qualcomm은 가장 많이 요청받은 기능이 현실이 됐다며, Snapdragon X2 시리즈가 Windows와 Googlebook에 이어 세 번째 운영체제로 Linux로 확장된다고 발표했다.
Qualcomm Technologies가 커널 수준에서 Linux의 주요 기여자이며, 이제 Snapdragon X2 시리즈를 플랫폼으로 직접 지원하고, Hexagon NPU와 Adreno GPU를 포함한 핵심 드라이버를 업스트림한다고 밝힌다.
배포판은 두 가지로 시작한다.
Debian은 올해 말까지, Ubuntu는 Canonical과 협력해 2027년 상반기를 목표로 Snapdragon X2 시리즈 인증을 받는다.
협력사 HP, ASUS, HUMAIN은 2027년 상반기에 자기 기기의 Linux 지원을 계획하고 있다.

## 분석

### “업스트림”이라는 한 단어가 이 발표의 무게를 정한다

Linux 지원 발표는 흔하다.
그 약속이 무엇을 뜻하는지는 드라이버가 어디에 들어가느냐로 갈린다.
벤더가 자기 커널 포크나 특정 배포판용 바이너리로 드라이버를 내놓으면, 그 기기는 벤더가 지원을 끊는 순간 최신 커널에서 떨어져 나간다.
드라이버가 메인라인 커널에 들어가면, 벤더가 떠나도 커뮤니티가 유지할 수 있다.

Hacker News에서 extraduder_ire는 Linux 지원이 무엇을 뜻하는지 궁금한 사람을 위해 Hexagon NPU와 Adreno GPU를 포함한 핵심 드라이버를 업스트림한다는 문장을 짚으며, Chromebook 지원처럼 반쯤 독점적인 방식이 아니어서 반갑다고 적었다.[^extraduder_ire]
flakiness는 업스트림이 제대로 된다면, 그것이 큰 가정이지만, 이 칩이 Linux 노트북의 기본 선택지가 될 수 있다고 봤다.[^flakiness]
Wi-Fi와 모뎀에서 오디오와 카메라 ISP까지 모두 한 SoC에 들어 있어, Intel 노트북보다 구성의 변형이 훨씬 적기 때문이라는 것이다.

### 이 발표는 두 번째 약속이다

Hacker News의 반응 상당수는 기억에서 나왔다.
hsnewman은 2년 전 Snapdragon X Elite 때도 같은 말을 들었다고 적었고,[^hsnewman] sharktheone은 오래전 이 칩을 사려다 Linux 지원이 걸림돌이 돼 결국 MacBook을 샀다며, 원래의 X Elite도 좋은 Linux 지원을 약속했지만 끝내 이루어지지 않았으니 이번에는 실제로 되기를 바란다고 했다.[^sharktheone]
baby_souffle은 첫 세대 때도 비슷한 말을 하지 않았느냐며 조심스러운 낙관을 표했다.[^baby_souffle]

이 기억이 이번 발표를 읽는 기준이 된다.
Qualcomm은 2024년에도 개발자 블로그로 Snapdragon X Elite의 업스트림 커널 지원을 알렸다.
그런데도 사용자들의 기억에 남은 것은 기기마다 들쭉날쭉한 지원과 오래 기다려야 했던 기능들이었다.
이번 발표가 다른 점은 배포판 두 곳의 이름과 날짜, 그리고 OEM 세 곳의 계획을 함께 내놓았다는 것이다.

### 선언보다 먼저 움직인 개발자들이 있다

Hacker News에서 cromka는 Qualcomm이 떠났던 개발자 몇 명을 다시 고용했고, 그들이 지난 두세 달 동안 Linux ARM MSM 메일링 리스트에서 여러 X2 노트북을 직접 지원해 왔다며, 공개 발표가 이렇게 늦은 것이 놀랍다고 적었다.[^cromka]
그는 이것이 Framework가 X2 메인보드를 내놓는 계기가 되기를 바랐다.
brynet은 OpenBSD 개발자 Tobias Heider가 이미 HP Elitebook X G2q에서 USB, 키보드, 터치패드를 ACPI 모드로 동작시키는 OpenBSD/arm64 지원의 첫 조각을 커밋했다고 전했다.[^brynet]
Canonical에서도 일하는 그는 최근 Ubuntu를 시연하며 ARM EL2가 동작해, 이전 세대와 달리 KVM을 쓸 수 있다고 확인했다고 한다.

이 증언들은 발표가 빈말이 아닐 수 있다는 근거다.
메일링 리스트의 패치와 다른 운영체제 개발자의 커밋은 마케팅 글보다 믿을 만한 신호다.
특히 EL2 접근은 이전 세대의 Windows용 노트북에서 막혀 있던 가상화의 문을 여는 변화로, 개발자용 Linux 노트북으로서의 가치를 크게 바꾼다.

## 비평

### 지원 범위의 단서가 발표문에서 빠져 있다

발표문은 Snapdragon X2 시리즈가 Linux로 “확장된다”고만 말한다.
Hacker News에서 blinkingled는 Qualcomm의 개발자 미리보기 글에서 이 작업이 Snapdragon X2 노트북에 맞춰져 있고, 데스크톱 폼팩터, 이전 Snapdragon X 플랫폼, 다른 개발 보드는 현재 다루지 않으며, 준비 상태는 OEM 설계와 X2 변형마다 다르다는 단서를 인용했다.[^blinkingled]
그리고 이것이 늘 보던 ARM의 방식이라며, 출고 상태 그대로의 Linux 지원에서는 여전히 AMD와 Intel이 왕이라고 적었다.

이 단서는 발표의 무게를 크게 바꾼다.
“X2 시리즈가 Linux를 지원한다”와 “일부 X2 노트북이 OEM에 따라 다른 수준으로 Linux를 지원한다”는 전혀 다른 약속이다.
사용자가 알고 싶은 것은 칩이 아니라 자기가 살 노트북 모델이 되느냐인데, 발표문은 그 질문에 답하지 않고, 답은 개발자 블로그의 단서 문장 속에 있다.

### 부트 체인과 기기별 설정이 열리지 않으면 커널 드라이버만으로는 부족하다

Hacker News에서 nrclark은 이 칩의 부트 스택이 얼마나 열려 있을지 물었다.[^nrclark]
Qualcomm은 역사적으로 폐쇄 소스 부트로더, 폐쇄 소스 하이퍼바이저, 폐쇄 소스 TEE, 포크된 UEFI를 강제해 왔고, 나머지 스택이 닫혀 있으면 열린 Linux도 절름발이가 된다는 것이다.
hurricanepootis는 ARM 노트북의 문제로, SoC가 업스트림에서 지원돼도 제조사가 자기 기기의 디바이스 트리를 올리지 않으면 쓸 수 없다고 지적했다.[^hurricanepootis]
이 노트북들이 UEFI와 ACPI를 갖추고는 있지만, 그 정보가 Linux에는 쓸모가 없고 Windows용 Qualcomm 독점 드라이버와 묶여 있어 디바이스 트리가 필요하다는 것이다.

rickdeckard는 Qualcomm이 플랫폼을 Linux의 일급 시민으로 만들고 싶다면, 출시 뒤 언젠가 한 번 나오는 식이 아니라 모든 X2 기기의 Linux 부팅에 필요한 모든 구성 요소를 담은 디바이스 트리 공개를 의무로 해야 한다고 적었다.[^rickdeckard]
발표문은 NPU와 GPU 드라이버의 업스트림을 강조하지만, 부트 체인과 기기별 설정이라는 더 근본적인 문제는 언급하지 않는다.
드라이버가 메인라인에 있어도 기기가 부팅되지 않으면 쓸 수 없다.

### 두 배포판의 서로 다른 날짜는 업스트림과 다른 이야기를 할 수 있다

Hacker News에서 prmoustache는 Debian과 Ubuntu에 서로 다른 날짜를 준 것이, 드라이버를 메인라인 커널에 넣기보다 배포판별로 내놓을 뿐이라는 신호일 수 있다고 의심했다.[^prmoustache]
그렇다면 몇 년 뒤 Qualcomm이 유지를 멈추고 커널이 바뀌면 드라이버를 더 이상 컴파일할 수 없게 될 수 있다는 것이다.
pjmlp도 이 지원이 Qualcomm이 순수한 마음으로 GNU/Linux를 받아들여서가 아니라 Googlebook 때문에 오는 것이라며, 특정 Ubuntu와 Debian 릴리스용 바이너리 드라이버를 예상하라고 적었다.[^pjmlp]

이 의심은 발표문의 “업스트림” 약속과 정면으로 부딪힌다.
커널 드라이버가 메인라인에 들어간다면 배포판마다 날짜가 다를 이유가 줄어들고, Ubuntu의 “인증”은 하드웨어 검증 절차에 가깝다.
두 약속이 어떻게 공존하는지, 곧 무엇이 메인라인에 들어가고 무엇이 배포판별 패키지로 나오는지를 발표문은 구분하지 않는다.
이 구분이 없으면 독자는 가장 좋은 경우와 가장 나쁜 경우를 모두 상상할 수 있다.

## 인사이트

### ARM 노트북의 Linux 문제는 칩이 아니라 “기기 목록”의 문제다

x86 노트북에서 Linux가 대체로 동작하는 것은 칩이 Linux를 지원해서만이 아니라, PC 플랫폼이 수십 년에 걸쳐 표준화된 부팅과 하드웨어 발견 방식을 갖췄기 때문이다.
ACPI와 PCI 열거가 제대로 동작하면, 커널은 기기마다 따로 작성된 설명 없이도 하드웨어를 찾는다.
ARM 노트북은 UEFI와 ACPI의 형식을 갖췄어도, hurricanepootis가 짚었듯 그 정보가 Linux에 쓸모 있지 않으면 기기마다 디바이스 트리가 필요하다.[^hurricanepootis]

그래서 Snapdragon X2의 Linux 지원은 “칩 하나”의 문제가 아니라 “기기 목록”의 문제가 된다.
지원하는 노트북 모델의 목록이 곧 지원의 범위이고, 그 목록에 들지 않은 기기는 칩이 같아도 쓸 수 없다.
blinkingled가 원한 것, 곧 메인보드와 CPU, GPU를 새 세대로 바꿔도 새 부트로더나 벤더 커널, 독점 GPU 바이너리 없이 기존 Linux 설치가 그대로 부팅되는 경험[^blinkingled]은, ARM PC가 x86 수준의 플랫폼 표준을 갖출 때까지는 오지 않는다.

### Apple M 시리즈의 대안을 원하는 수요가 Qualcomm에게 두 번째 기회를 준다

Hacker News에서 modeless는 많은 사람이 Qualcomm이 도달한 성능 수준을 모른다며, 노트북 폼팩터에서는 Apple M 시리즈에 가장 가까운 경쟁자이고 Intel과 AMD의 최고 제품보다 낫다고 적었다.[^modeless]
Hasz는 Apple M 시리즈의 80% 효율과 80% 하드웨어 품질이면서 Debian이나 Ubuntu가 도는 기기라면 Apple 이상의 가격도 기꺼이 내겠다고 했다.[^Hasz]
그는 방금 M5 기기를 샀지만 원하는 것은 성능보다 긴 배터리, 좋은 화면, 그리고 Unix 계열 환경이라고 덧붙였다.

이 수요는 Qualcomm이 첫 세대의 실패에도 두 번째 기회를 얻는 이유다.
GeekNews에서 chcv0313은 이 발표를 시장이 한정된 스마트폰에만 머물지 않겠다는 선언으로, 여차하면 Mac mini 같은 자리로 넓혀 가겠다는 신호로 읽었다.[^chcv0313]
Apple Silicon이 보여 준 전력 효율을 Linux에서 누리고 싶은 개발자 시장은 분명히 있고, 지금 그 자리를 채우는 제품은 없다.
그러나 같은 사람들이 첫 세대의 약속을 기억하고 있고, cientifico의 말처럼 Linux 사용자들이 Qualcomm을 다시 믿기까지는 몇 년이 걸릴 수 있다.[^cientifico]
두 번째 기회의 성패는 발표가 아니라, 첫 번째 X2 노트북이 출고된 날 Debian 설치 USB로 무엇이 동작하느냐에 달려 있다.

### Linux 지원의 동기가 Googlebook이라면, 지원의 모양도 Googlebook을 따른다

pjmlp의 해석처럼 이번 Linux 지원이 Googlebook에서 비롯됐다면,[^pjmlp] 그 사실은 지원의 모양을 예측하게 해 준다.
Googlebook은 Android 앱 지원을 앞세운 Google의 노트북 플랫폼이고, 그 밑에는 Linux 커널이 있다.
Googlebook을 위해 Qualcomm이 커널 드라이버를 다듬어야 한다면, 그 작업의 일부가 일반 Linux 배포판으로 흘러가는 것은 자연스럽다.

이 연결은 기대와 위험을 함께 준다.
Googlebook용 드라이버가 메인라인에 들어간다면 일반 Linux도 그 혜택을 받지만, Googlebook에 필요한 기능과 일반 Linux 사용자가 필요한 기능이 다를 때 우선순위는 Googlebook에 있을 것이다.
Chromebook이 오래 겪어 온 것처럼, 커널은 같아도 드라이버와 펌웨어가 특정 플랫폼의 요구에 맞춰질 수 있다.
extraduder_ire가 반긴 “Chromebook 지원 같은 반쯤 독점적인 방식이 아니라는 점”[^extraduder_ire]이 실제로 지켜지는지가, 이번 약속을 평가하는 가장 좋은 기준이 될 것이다.

---

[^extraduder_ire]: <https://news.ycombinator.com/item?id=49824350>

[^flakiness]: <https://news.ycombinator.com/item?id=49824199>

[^hsnewman]: <https://news.ycombinator.com/item?id=49824337>

[^sharktheone]: <https://news.ycombinator.com/item?id=49824691>

[^baby_souffle]: <https://news.ycombinator.com/item?id=49824164>

[^cromka]: <https://news.ycombinator.com/item?id=49824279>

[^brynet]: <https://news.ycombinator.com/item?id=49824329>

[^blinkingled]: <https://news.ycombinator.com/item?id=49825388>

[^nrclark]: <https://news.ycombinator.com/item?id=49825208>

[^hurricanepootis]: <https://news.ycombinator.com/item?id=49825947>

[^rickdeckard]: <https://news.ycombinator.com/item?id=49827275>

[^prmoustache]: <https://news.ycombinator.com/item?id=49827330>

[^pjmlp]: <https://news.ycombinator.com/item?id=49826611>

[^modeless]: <https://news.ycombinator.com/item?id=49824444>

[^Hasz]: <https://news.ycombinator.com/item?id=49825792>

[^cientifico]: <https://news.ycombinator.com/item?id=49828245>

[^chcv0313]: <https://news.hada.io/topic?id=34210#cid66242>
