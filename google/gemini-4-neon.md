# Gemini 4 Neon 출시

원문: [Introducing Gemini 4 Neon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/)

HN 토론: <https://news.ycombinator.com/item?id=50552424> (498점, 462개 댓글)

GN 토론: <https://news.hada.io/topic?id=37432>

## 요약

2026년 11월 18일 Google DeepMind의 Koray Kavukcuoglu(수석 AI 아키텍트)가 쓴 Gemini 4 Neon 출시 글이다.
부제는 복잡한 소프트웨어 공학, 지식 업무, 과학 작업 흐름에서 빠른 끝까지의 작업 완료를 갖춘 최전선급 지능이라는 것이다.
글에 붙은 벤치마크 표와 비용 도표는 이미지라 숫자를 읽지 못했고 모델 카드(PDF)와 각 벤치마크 페이지는 열지 못했다.
직접 써 보지 않았다.
아래 수치는 모두 Google이 글에 적은 값이다.

- 위치: Artificial Analysis 지능 지수(xhigh 사고 수준)에서 61점으로 전체 3위이고 더 크고 느린 모델 바로 뒤이다. Vals 지수에서 2위이고 파레토 경계에 있다. 새 Agent Arena 지수의 조향 가능성(작업 중 사용자 교정에 맞추기)에서 2위이다. Google 내부 Antigravity 시험에서 지금까지 기록한 가장 낮은 지어내기(fabrication) 비율이라고 한다.
- 가격과 문맥: 입력 100만 토큰당 3달러, 캐시된 입력 0.15달러(95% 할인), 출력 15달러이고 문맥 창은 100만 토큰이다. 스프레드시트, PDF, 차트, 오디오, 비디오를 한 문맥에서 종합한다고 한다. 지식 기준 시점과 출력 형식은 글에 없다.
- 제공: Google AI Studio의 Gemini API와 기업용 Gemini(API와 모델 드롭다운)로 오늘부터 나간다. Google AI Pro와 Ultra 유료 구독자는 Antigravity와 Gemini 앱의 모델 드롭다운에서 쓰고, 개발자는 AI Studio와 Android Studio의 유료 계층으로 쓴다. 사이버 보안용 Neon은 Fairwind 프로그램의 신뢰된 방어자에게 며칠 안에 나가며 Cloud 계정 팀을 통해 신청한다. 지역 제한은 글에 없다.

글이 내세우는 성능은 다음과 같다.

| 영역        | 글의 수치                                                                                                                                                                                                                                                                       |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 기업과 분석 | Vals 지수 70.9%(2위), Vals 법률 연구와 세무 에이전트 1위, Surge AI의 재무와 회계와 스프레드시트 대부분 1위, Chartography 73.5%, Agents' Last Exam v1.1 75.8%, Zapier AutomationBench 56.3%(1위), Vending-Bench 2 16,843달러(1위), Agent Arena 지수 1336(4,200개 이상 세션, 2위) |
| 과학과 수학 | Terminal-Bench Science 70.5%, RiemannBench 84.0%, HLE-Diamond 71.3%                                                                                                                                                                                                             |
| 코딩        | Artificial Analysis 코딩 에이전트 지수 58.6(1위), Terminal-Bench 4.1 65.2%, FrontierCode 2.0 46.2%, SWE-sweep는 mini-SWE에서 12.8%, Antigravity에서 39.0%                                                                                                                       |
| 사이버      | AutoBaxBench 어려운 수준 76%, WebExploitBench v1.2 51.26%, SEC-bench Pro 90.5%, CWE-bench v2 70.7%(Carbon보다 3.4% 향상)                                                                                                                                                        |

효율에 대해 글은 사고 수준이 넷이며 이름이 적힌 것은 high와 xhigh라고 한다. high에서는 Carbon보다 작업당 비용이 32% 낮고 Vals 지수와 Agent Arena에서 최전선 경쟁 모델보다 작업당 비용이 약 50%에서 80% 낮은 파레토 경계에 있다. xhigh는 가장 높은 지능 점수에 경쟁 모델의 최고 설정보다 작업당 36% 이상 싸다.
코딩 쪽 설명은 장시간 도구가 많은 에이전트 작업용이며 단독으로나 Antigravity의 오케스트레이터로 Hydrogen 하위 에이전트를 병렬로 지휘하는 용도라고 한다. 중복 파일 읽기를 줄이고 문맥 압축을 처리한다.
안전에 대해서는 Gemini 4의 안전 스택 위에 서고 Carbon 수준의 보호를 유지한다고 한다. 정당한 작업의 거부는 줄었고(Terminal-Bench 4.0 과제의 1.98%, Terminal-Bench-Science 0%), 사고 연쇄와 행동 비정렬 감시의 경고율은 내부 코딩에서 Carbon 기준 아래였다. 부정행위 0.0%, 코딩 부정 평가의 지름길 2.45%(Gemini 4 모델 중 최저), 에이전트 안전 모음의 비정렬 행동 0.09%, 에이전트 정직성 평가 통과 99.2%, 간접 프롬프트 주입 공격 성공률 0.0%(가장 높은 사고 수준과 실시간 안전 장치)를 든다. Carbon 대비 서비스 부족이 43%에서 56%, 과잉 행동이 15%에서 35% 줄었다고 한다.
Gemini 앱에서는 글쓰기, 스프레드시트와 PDF와 사진 읽기, Gmail과 Docs에서 정보 가져오기가 나아졌고 Gemini Tasks를 Neon에서 돌릴 수 있다고 한다.
Gemini 4 가족 안에서 Neon은 복잡한 코딩과 분석과 기업 워크플로, Carbon은 가장 어려운 장기 프로젝트, Hydrogen은 빠른 일상 실행이다.

## 분석

### 중심 주장은 파레토 경계 위에서 싸게 최전선에 가깝다는 것이다

글의 구조는 지능 지수 순위와 작업당 비용이다.
Carbon보다 지능이 높고 싸다는 것이 새로움이다.
한 사용자는 Vals 지수에서 Fable 5.2 성능의 약 1% 안쪽을 약 40% 비용으로 낸다고 정리했다.[^irthomasthomas]

### 가족 안의 역할 분담이 분명해졌다

HN에서 Artificial Analysis 직원이라고 밝힌 사용자는 Neon이 Carbon보다 전반적으로 더 똑똑하지만 Carbon은 장기 과제용으로 자리가 남는다고 짚었다.[^declanjackson]
한 사용자는 Neon이 Opus급 크기이고 Carbon은 Fable급이며 Carbon은 사고 토큰을 매우 쓰는 Argon의 변형 같다고 추정했다.[^warmwash] 이는 추정이다.

### 속도가 체감 차이로 보인다

한 사용자는 OpenRouter에서 Neon이 초당 127토큰으로 서빙되고 Carbon은 46토큰이라고 했다.[^seizethecheese] 앞서 정리한 Carbon의 느림(`llm/gemini-4-carbon-slowness.md`)과 대조되는 지점이다. 이 값은 시점과 공급자에 따라 달라질 수 있다.

## 비평

### 수치의 출처와 산출이 외부 지수에 기댄다

대부분의 수치는 Artificial Analysis, Vals, Arena 같은 외부 지수와 비공개일 수 있는 평가에서 온다.
HN에서 한 사용자는 Artificial Analysis의 벤치마크 60%가 비공개라고 하며 투명성을 어떻게 보장하는지 물었다.[^godelnumbering]
도표 이미지의 숫자가 글 본문에 없어 독자가 검증하려면 링크된 각 지수를 따로 열어야 한다.

### 벤치마크와 체감 사이의 간극이 거론된다

한 사용자는 벤치마크는 비슷하지만 Opus 5.5가 전체적으로 더 낫다고 느끼고 Anthropic의 비결을 물었고, 다른 사용자는 Gemini 4가 영어 글쓰기는 훨씬 낫다고 했다.[^impulser][^svara]
한 사용자는 Neon이 Opus 5.5만큼 좋은 것 같다고 했고 다른 사용자는 사용성의 큰 도약이라고 했다.[^onlyrealcuzzo][^misterbiggs] 모두 개인 평가이다.

### 이름 체계가 부담이다

한 사용자는 계속 나오는 새 이름과 용도 대응이 피곤하다고 했고 다른 사용자는 모델을 훈련해 보고 「그럭저럭 좋다」고 이름을 붙이는 것일 뿐 체계가 없을 것이라고 했다.[^stillpointlab][^aboardrat]
한 사용자는 가스/플래시 계열(Hydrogen, Neon)과 솔리드/프리미어(Argon, Carbon)로 나눠 읽는 추정을 냈다.[^darkotic] 글은 모델 이름 체계를 설명하지 않는다.

### 안전 수치의 독립 검증이 없다

공격 성공률 0.0%, 정직성 99.2% 같은 값은 Google의 내부 평가이다.
한 사용자는 학습 거부 설정이 아직 자신에게 적용되지 않았다고 했고 다른 사용자는 11월 16일에 채팅의 학습 거부가 가능해졌다고 알렸다.[^dannyw][^sdvs9so]

### 외부 반응

HN 글 제목은 「Gemini 4 Neon」이다. 모델 선택에서는 Anthropic이 OpenAI가 아니라 Google과 경쟁하는 것이 뜻밖이라는 의견,[^bisonbear] 장기적으로 AI가 모든 것을 잘하면 디스토피아라는 우려도 있었다.[^bemtevi]
GeekNews 토픽에는 이용자 댓글이 있다. 한 이용자는 Carbon과 같은 가격이면서 성능이 낮았던 Argon이 서비스에서 점점 내려가는 것 같다고 했고, 이 이용자는 출시된 Gemini 모델을 원소 주기율표에서 찾아보는 사이트도 만들었다고 소개했다.[^laeyoung][^laeyoung2]

## 인사이트

### 가져갈 것은 모델을 지능과 작업당 비용의 두 축으로 고르는 방식이다

가격표의 토큰 단가만이 아니라 같은 작업을 끝내는 데 드는 총비용(생각 토큰, 단계 수)을 같이 본다. 이 글의 「작업당 비용」이 그 비교이며 자기 작업으로 재 보는 것이 가장 믿을 만하다. 이는 이 문서의 적용이다.

### 같은 가족의 모델을 역할로 나눠 쓴다

계획과 장기 과제에는 Carbon, 복잡한 일상 업무에는 Neon, 빠른 실행에는 Hydrogen이라는 글의 분담을 시험해 보고, 자기 하니스에서 단계 수와 지연을 재서 정한다.

### 확인할 관찰

이 글의 주장을 가를 관찰은 세 가지이다.
독립 평가에서의 순위와 작업당 비용,
같은 하니스에서의 Carbon과 Opus 5.5와의 단계 수와 지연 비교,
모델 카드의 안전 평가 세부이다.

---

[^irthomasthomas]: <https://news.ycombinator.com/item?id=50553896>

[^declanjackson]: <https://news.ycombinator.com/item?id=50552868>

[^warmwash]: <https://news.ycombinator.com/item?id=50552906>

[^seizethecheese]: <https://news.ycombinator.com/item?id=50552830>

[^godelnumbering]: <https://news.ycombinator.com/item?id=50553291>

[^impulser]: <https://news.ycombinator.com/item?id=50552711>

[^svara]: <https://news.ycombinator.com/item?id=50553503>

[^onlyrealcuzzo]: <https://news.ycombinator.com/item?id=50552548>

[^misterbiggs]: <https://news.ycombinator.com/item?id=50554410>

[^stillpointlab]: <https://news.ycombinator.com/item?id=50553269>

[^aboardrat]: <https://news.ycombinator.com/item?id=50553607>

[^darkotic]: <https://news.ycombinator.com/item?id=50555412>

[^dannyw]: <https://news.ycombinator.com/item?id=50552661>

[^sdvs9so]: <https://news.ycombinator.com/item?id=50553832>

[^bisonbear]: <https://news.ycombinator.com/item?id=50552682>

[^bemtevi]: <https://news.ycombinator.com/item?id=50552642>

[^laeyoung]: <https://news.hada.io/topic?id=37432#cid70157>

[^laeyoung2]: <https://news.hada.io/topic?id=37432#cid70158>
