# AlphaProof Code의 Signal 검증

원문: [Introducing AlphaProof Code: a breakthrough in verifying complex software at depth](https://deepmind.google/blog/introducing-alphaproof-code/)

HN 토론: <https://news.ycombinator.com/item?id=50439193> (678점, 197개 댓글)

GN 토론: <https://news.hada.io/topic?id=36944>

## 요약

Google DeepMind의 Pushmeet Kohli와 Swarat Chaudhuri가 2026년 11월 10일에 올린 글이다.
DeepMind 연구진이 AI 에이전트를 이끌어 Signal 프로토콜의 실제 코드에 대한 핵심 보안 속성을 수학적으로 증명했다고 밝힌다.
글은 이것이 AI로 널리 쓰이는 암호 프로토콜을 이 깊이에서 형식 검증한 첫 사례이고, 어떤 방법으로든 이런 프로토콜의 구현이 형식 검증된 첫 사례라고 주장한다.

방법은 이렇게 소개된다.
AlphaProof Code는 형식 검증의 일을 연구팀처럼 나누는 다중 LLM 에이전트 틀이다.
사람 전문가가 AI와 함께 무엇을 증명할지 정하고, 에이전트 무리가 증명한다.
연구진은 여러 모델과 함께 Signal의 보안 목표를 형식 명세로 옮겼고 전문가가 모든 명세를 검토했다.
Gemini Carbon 기반 에이전트가 Lean으로 600만 줄이 넘는 증명을 만들었다.
그다음 에이전트가 증명을 감사해 사람이 다시 볼 곳으로 코드베이스의 1%를 짚었고, 나머지는 Lean이 자동으로 검사한다.
글은 검증에 4주가 걸렸고 이는 예전에는 전문가 팀이 수년 걸리던 일이라고 쓴다.
또 이미 고쳐진 실제 버그 두 개를 격리된 코드에 다시 넣었더니 두 경우 모두 시스템이 버그 버전이 안전하지 않다는 기계 검사 증명을 냈다고 한다.
Signal의 CTO Ehren Kret의 인용도 실려 있다. 실제 코드를 Lean 정리로 옮기는 일을 AI 에이전트가 하는 것이 큰 진전이라는 내용이다.

이 문서는 블로그 전문과 기술 논문의 요약, 시스템 구성, 신뢰 기반, 역사적 버그, 실무, 토론 절을 읽었다.
Lean 증명이나 저장소는 열어 보지 않았다.

## 분석

### 중심 주장은 증명 비용이 AI로 급격히 낮아졌다는 것이다

기술 논문은 이 주장을 구체적인 수치로 제시한다.
에이전트가 만든 증명은 약 650만 줄이고, 그 아래의 신뢰해야 할 명세와 AArch64 의미론은 약 2만 6천 줄이다.[^paper]
논문은 seL4 마이크로커널의 검증에 20인년, CompCert 컴파일러에 6인년이 들었다고 비교한다.[^paper]
다섯 사람이 4주 동안 각자의 워크스테이션에서 에이전트를 쉬지 않고 돌렸다고 밝힌다.[^paper]
다만 블로그의 “수년이 걸리던 일”은 논문이 아니라 글의 비교이고, 같은 범위의 사람 작업 비용을 측정한 것은 아니다.

### 증명되는 것은 정해진 보안 속성이다

논문이 증명한 것은 Signal의 포스트 양자 핸드셰이크(PQXDH)와 Triple Ratchet에 대해 전방향 비밀성, 인증, 침해 후 보안, 핸드셰이크 비밀성이다.[^paper]
증명은 상징적 모델(Dolev–Yao)과 계산적 모델 두 가지에서 한다.[^paper]
대상 코드는 수정하지 않은 libsignal을 표준 rustc로 AArch64 기계어로 컴파일한 결과이다.[^paper]
그래서 Rust 컴파일러는 신뢰 대상이 아니라고 논문이 적는다.[^paper]
반면 신뢰 기반에는 정리의 진술과 정의, AArch64 의미론, 호출되는 일부 루틴의 계약, 암호 기본 요소에 대한 가정, Lean 자체가 들어간다.[^paper]

### 어려운 일은 증명이 아니라 명세 쓰기였다

논문은 이 경험의 가장 큰 교훈을 증명이 싸지면 무엇을 증명할지가 어려운 질문이 된다는 것으로 꼽고, 노력의 대부분이 증명이 아닌 명세에 들어갔다고 쓴다.[^paper]
명세는 Gemini 4 Carbon과 Claude Opus 5.5가 구동하는 에이전트와 사람이 오가며 만들었고, 다른 모델 계열의 에이전트가 원 논문과 libsignal에 대한 충실도와 강도를 검토했다고 한다.[^paper]
에이전트가 혼자 쓴 명세는 감사하기 어려워서 가독성을 위해 다시 쓰게 한 적이 있다고 밝힌다.[^paper]
형식 명세가 문헌의 모델과 다르거나 libsignal과 다른 곳을 기록한 목록은 계산적 쪽이 200개가 넘고 상징적 쪽이 약 35개이다.[^paper]
블로그는 이 점을 “무엇을 증명할지 정하는 것은 사람”이라는 한 줄로만 말한다.

## 비평

### 버그가 없다는 말로 읽으면 틀린다

HN 스레드는 이 오해에서 시작했다.
한 댓글은 과거에 버그가 있던 복잡한 라이브러리 전체를 검증하고도 버그를 하나도 못 찾았다는 것이 이상하며, 정리를 잘못 세웠거나 좁은 속성만 증명한 것 아니냐고 물었다. 작성자는 Claude로 암호와 저장 형식을 형식 검증해 봤더니 정리는 그럴듯했고 검증도 통과했지만 다른 구현과 비교하는 단순한 시험으로 드러나는 버그가 수두룩했다고 한다.[^hedora]
답글은 좁은 속성이 맞다고 했다. 코드에 버그가 없다는 증명이 아니라, 알려졌든 아니든 현재의 버그가 형식화된 보안 모델을 위반하지 않는다는 증명이라는 것이다.[^derefr]
다른 답글은 모든 형식 검증이 명세가 말하는 것만 증명하고 명세가 의도와 맞는지는 증명하지 못한다고 했다.[^cortesoft]
또 다른 댓글은 소프트웨어의 버그가 타이밍 신호나 버퍼 문제까지 포함하는데 어떤 속성을 증명했는지 정의해야 한다고 했다.[^lubujackson]
논문의 토론 절도 이 한계를 직접 적는다.
계산적 정리는 고전적 공격자에 대한 것이고, 래칫 정리는 공격자가 SPQR 키를 고르게 하므로 SPQR이 주려는 포스트 양자 자기 치유는 증명하지 못하며, 세션당 핸드셰이크 하나와 고정 메시지 길이 같은 모델 선택이 있다.[^paper]
범위도 일대일 세션에 한정되고 그룹 메시지, sealed sender, 서버 쪽 프로토콜은 빠져 있다.[^paper]

### 보고 있는 것이 Signal 앱 전체가 아니다

한 댓글은 Signal 앱이 아니라 암호 프로토콜만 검증했다고 짚었다.[^gasp0de]
다른 댓글은 암호가 안전해도 나머지 코드까지는 모른다고 했다.[^milkshakes]
논문도 검증 대상을 작은 명령줄 하니스에 링크한 libsignal로 설명한다.[^paper]
글의 첫 문단이 “Signal 프로토콜 코드”라고 쓴 것은 정확하지만, 독자는 “Signal이 검증되었다”로 줄여 읽기 쉽다.

### 시험의 범위가 좁다

논문은 명세가 실제 실수를 잡는지 확인하려고 이미 고쳐진 버그 두 개(약한 상태, 작은 부분군)를 소스에 되돌려 넣고 상징적 보안 정리가 그 바이너리에서 성립하지 않음을 Lean으로 증명했다.[^paper]
그러나 계산적 정리의 반증은 가정된 어려움 자체를 증명하는 것에 해당해서 훨씬 어렵다고 스스로 쓴다.[^paper]
HN의 한 댓글은 버그를 되돌려 넣은 점을 높이 평가했고,[^ctrlaltdileep]
다른 댓글은 AI가 Lean을 직접 쓰면 쉽게 속임수를 쓸 수 있으니 적대적 프롬프트로 한 번 더 검토해야 한다고 했고, 논문에서 이미 고쳐진 버그를 되돌려 넣은 것은 보았지만 새 버그를 찾았다는 내용은 없는 것 같다고 적었다.[^r0ze]
같은 작성자는 명세를 Lean으로 옮기면 그 과정에서 숨은 가정이 드러나는 것이 실익이라고 했는데, 이는 개인 경험이다.

### 증명과 정리를 구분하라는 경고가 반복된다

한 개발자는 AI가 몇 시간 동안 리팩터링하고 시험 묶음까지 자진해서 만들어 모두 통과했지만 구현이 거꾸로였다는 경험을 들었고,[^andai]
답글은 사람들이 증명과 정리를 혼동하며 증명이 맞아도 정리가 틀릴 수 있다고 말했다.[^auggierose]
이 논점은 블로그의 “agents audited the proof” 대목과 닿는다.
블로그는 에이전트가 사람이 볼 1%를 짚었다고 쓰지만, 명세가 맞는지는 그 1%의 일이 아니라 사전에 사람이 검토한 것이다.

### 홍보 글과 논문 사이의 간극이 있다

블로그는 “Gemini Carbon”을 증명 에이전트의 모델로만 적고, 논문은 명세 작성에 Gemini 4 Carbon과 Claude Opus 5.5가 모두 쓰였다고 밝힌다.[^paper]
한 댓글은 이 문서가 다중 LLM이라는 말보다 다중 에이전트 시스템이라고 하는 것이 정확하다고 했다.[^beernet]
또 다른 댓글은 에이전트가 사람이 하듯 한다는 문장이 순환적이라고 했다.[^arcastroe]
모두 표현에 대한 비판이고 결과의 타당성과는 별개이다.

## 인사이트

### 형식 검증의 병목이 증명에서 명세로 옮겨 간다

논문과 HN 댓글이 같은 방향을 가리킨다.
증명이 싸지면 어떤 속성을 증명해야 하는지 정하는 일이 남는다.
HN에서 한 댓글은 무엇을 증명할지는 가치 판단에 묶여 있어 사람 몫이라고 했고,[^mjdiloreto]
다른 댓글은 AI가 무엇을 만들어야 하는지 알아야 하기 때문이라고 했다.[^mrtesthah]
논문은 한발 더 나가 명세가 그 자체로 소프트웨어 산출물이며, 공동체의 공개 검토로 합의되어야 한다고 쓴다.[^paper]
실무에서 이 결과를 쓰려는 팀이 먼저 준비할 것은 증명 도구가 아니라 자기 시스템의 보안 속성을 서술하는 능력이다.

### 신뢰 기반의 크기를 읽는 법

한 댓글은 약 2만 6천 줄의 명세와 의미론이 큰 신뢰 기반이라고 평했고,[^oggy]
다른 댓글은 Lean 모델의 프로세서와 실제 프로세서가 같은지, Lean 명세가 Signal 코드의 의도와 맞는지를 물었다.[^ane]
논문은 Lean이 컴파일된 바이너리의 바이트를 대조하고 AArch64 의미론과 리눅스 프로세스 모델은 신뢰한다고 쓴다.[^paper]
검증의 가치는 사람이 읽어야 하는 줄 수(논문은 약 1만 8천 줄에 의미론 약 8천 줄)로 따지는 것이 적절하다.
이는 이 문서의 평가 기준이다.

### 확인할 관찰

이 결과의 의미를 가를 관찰은 세 가지이다.
다른 연구자가 공개된 명세를 검토해 빠지거나 틀린 부분을 지적하는지,
같은 틀이 libsignal 밖의 다른 코드(예: 다른 언어의 구현)에서도 비슷한 비용으로 되풀이되는지,
이 검증이 이후 libsignal 변경에 맞춰 유지되는지이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^paper]: [AlphaProof Code: Verifying Signal’s Security at the Machine-Code Level](https://google-deepmind.github.io/code-verification)

[^hedora]: <https://news.ycombinator.com/item?id=50442002>

[^derefr]: <https://news.ycombinator.com/item?id=50442165>

[^cortesoft]: <https://news.ycombinator.com/item?id=50442535>

[^lubujackson]: <https://news.ycombinator.com/item?id=50442230>

[^gasp0de]: <https://news.ycombinator.com/item?id=50439641>

[^milkshakes]: <https://news.ycombinator.com/item?id=50439457>

[^ctrlaltdileep]: <https://news.ycombinator.com/item?id=50440002>

[^r0ze]: <https://news.ycombinator.com/item?id=50440961>

[^andai]: <https://news.ycombinator.com/item?id=50441544>

[^auggierose]: <https://news.ycombinator.com/item?id=50441664>

[^beernet]: <https://news.ycombinator.com/item?id=50439775>

[^arcastroe]: <https://news.ycombinator.com/item?id=50447368>

[^mjdiloreto]: <https://news.ycombinator.com/item?id=50439819>

[^mrtesthah]: <https://news.ycombinator.com/item?id=50441253>

[^oggy]: <https://news.ycombinator.com/item?id=50443079>

[^ane]: <https://news.ycombinator.com/item?id=50439778>
