# MAI Code 2와 Code 2 Flash

원문: [MAI Code 2 and MAI Code 2 Flash: two new coding models built for the everyday enterprise coding tasks](https://microsoft.ai/news/introducing-mai-code-2-and-mai-code-2-flash/)

HN 토론: <https://news.ycombinator.com/item?id=50535885> (338점, 149개 댓글)

GN 토론: <https://news.hada.io/topic?id=37368>

## 요약

Microsoft AI가 낸 코딩 모델 발표문이다. 같은 사이트의 관련 글 목록 날짜로 보아 2026년 11월 17일 전후에 올라왔다.
이 문서는 본문과 하단의 평가 방법 주석을 읽었다. 모델을 직접 써 보지 않았고 별도의 기술 보고서는 없어 읽지 못했다.
수치와 평가는 모두 Microsoft의 주장이다.

두 모델이 나왔다.

- MAI Code 2: 일상적인 기업 코딩 작업용 모델이다. 코드를 프로덕션으로 가져가기, 깊은 디버깅, 여러 파일에 걸친 구현, 저장소 전체 추론, UI에 강하고 유지보수자가 병합할 만한 변경을 낸다고 한다.
- MAI Code 2 Flash: 코드 설명, 국소 수정, 일상적 수정, 빠른 반복처럼 양이 많은 일용 모델이다.

핵심 주장은 가격 대비 성능이다.

- GitHub Copilot에서 보는 기업 코딩 과제를 겨냥한 벤치마크 네 개(DeepSWE 1.1, Terminal Bench 2.1, SWE-Atlas, FrontierCode v1.1) 평균에서 MAI Code 2는 GPT 6.1 Sol 성능의 98%를 비용 40%로, Claude Opus 5.5 성능의 96%를 비용 5%로 낸다고 한다.
- 블라인드 프런트엔드 앱 평가에서 평가자는 GPT-6 Sol보다 MAI Code 2의 결과를 64% 선호했다고 한다.
- Flash는 세 가지 일용 코딩 벤치마크에서 GPT-6 Luna, Claude Haiku 5.5와 비슷한 성능을 비용 65%, 20%로 낸다고 한다.
- 한계: 기초 과학 연구나 매우 긴 호흡의 에이전트 작업 같은 어려운 문제에는 아직 맞추지 않았다고 스스로 밝힌다.

코딩 밖에서는 Code 2 Flash를 바탕으로 최적화한 모델 MAI Work Flash가 M365와 Fabric IQ의 여러 제품에서 쓰인다고 한다.

- Excel: 내부 고객 시나리오 벤치마크에서 정확도와 토큰 효율이 GPT 6 Luna와 대등하다.
- PowerPoint: 품질과 토큰 효율이 GPT 6 Luna와 대등하다.
- Word: 내부 벤치마크 다섯 개에서 GPT 6.1 Sol과 비슷하고 실제 운영에서 입력 토큰이 약 42% 적다.
- Teams: GPT 6 Luna보다 결정 추적, 지식 공백 메우기, 사용자 지침 적응이 낫고 토큰이 최대 28% 적다.
- Fabric IQ: 오프라인 평가에서 DAX 쿼리 생성이 GPT-5.6-sol, GPT-6-astra, Opus-5.5보다 낫다.

제공 경로는 GitHub Copilot(두 모델)과 Microsoft Foundry의 제한 접근 미리보기(Flash)이다. 곧 OpenRouter, Vercel, Hermes, Open Code, Kilo에서도 낸다고 한다.

하단 주석이 평가 조건을 적는다.

- 모든 모델을 최대 추론 강도로 돌렸다.
- DeepSWE, Terminal Bench, SWE Atlas는 Microsoft 내부 평가 플랫폼 MSBench에서 서브에이전트 없이 GitHub Copilot CLI로 돌렸다.
- FrontierCode의 점수와 비용은 Artificial Analysis의 값이고, MAI Code 2의 비용은 50% 프로모션 가격으로 표시했다.
- 시각 코딩 평가는 사용자 인터페이스, 게임, 데이터 시각화, 3D 장면, SVG를 대상으로 한 사람의 블라인드 비교이며 평가자는 258명이다.

## 분석

### 중심 주장은 작은 전문 모델이 프런티어의 대부분을 싸게 낸다는 것이다

98%와 96%라는 성능 비율에 40%와 5%라는 비용 비율을 붙이는 구조가 발표문의 중심이다.
모든 서술은 어려운 문제를 포기하고 일상 작업에 맞췄다는 전제를 깔아, 프런티어 모델과 정면으로 겨루는 대신 가격 곡선의 다른 지점을 차지하겠다는 선언으로 읽힌다.
HN에서 한 사용자는 비용이 20%라는 주장이 모델 크기가 그만큼 작다는 뜻이라면 코딩을 잘하게 하려면 모든 것을 잘하게 해야 한다는 정설이 깨지는 해가 될 것이라고 추측했다.[^kennywinker]
이는 댓글의 추측이며 발표문은 모델 크기를 밝히지 않는다.

### 제품 안에 들어가는 모델이라는 점이 따로 있다

발표문 후반은 코딩 모델이 Excel, PowerPoint, Word, Teams, Fabric IQ의 기반 모델이 된다고 말한다.
자사 제품에서 외부 모델 의존을 줄이고 비용을 낮추는 방향이다.
HN에서 한 사용자는 모든 대기업에 GitHub가 있고 Copilot이 있어 서구권 모델 대부분을 쓸 수 있으므로 MAI가 의미가 있는 곳은 현재 거의 쓸 수 없을 정도로 나쁘다고 평가한 Office Copilot일 것이라고 했다.[^poisonborz]
이 평가는 댓글 작성자의 의견이다.

## 비평

### 비교 조건이 발표자에게 유리하게 보인다

HN에서 한 사용자는 MAI Code 2를 50% 프로모션 가격으로 표시하면서 경쟁 모델은 최대 추론 강도로 돌렸다고 지적했다.[^user43928]
발표문 주석이 실제로 이 두 가지를 적고 있어 지적은 사실과 맞는다.
프로모션이 끝난 뒤의 비용 비율은 40%와 5%가 아니라 이 문서가 계산하지 못한 값이다.
또 벤치마크 일부는 Microsoft 내부 플랫폼에서 서브에이전트 없이 돌렸다.

### 벤치마크 선택에 대한 의심이 있다

한 사용자는 DeepSWE 1.1이 이미 신뢰를 잃었고, Terminal Bench는 최신 판이 4인데 2.1을, FrontierCode는 현재 2.0인데 1.1을 쓴 것이 믿음을 주지 못한다고 했다.[^johnfn]
다른 사용자는 Artificial Analysis가 지식 암기 비중을 크게 둔다는 점이 작은 코딩 특화 모델의 평가에 영향을 준다고 짚었다.[^wheen]
두 지적의 근거는 댓글 작성자의 주장이며 이 문서가 확인하지 못했다.
한 사용자는 비교 대상에 DeepSeek, GLM, Qwen이 없다는 점도 아쉬워했다.[^uncleoxidant]

### 접근 경로와 가격 정보가 불분명하다

HN에서 한 사용자는 발표문에 가격 페이지도, API 키를 만들 방법도, 놀이터도 없어서 어디서 써 볼 수 있는지 찾기 어렵다고 불평했다.[^throwaw12]
다른 사용자들은 OpenRouter와 GitHub Copilot CLI에 있고 Azure에서 엔드포인트를 몇 시간 안에 만들 수 있다고 답했다.[^rcarmo]
발표문은 Copilot과 Foundry(제한 접근)를 적고 나머지는 곧 낸다고 하므로, OpenRouter가 이미 있다는 답은 이 문서가 확인하지 못했다.

### 기술 보고서가 없다

HN에서는 이전 모델(MAI-Thinking-1)의 기술 보고서가 이례적으로 상세했는데 이번에는 링크가 없다는 아쉬움이 나왔다.[^upbeat_general]
한 사용자는 모델이 처음부터 학습한 것이라며 Microsoft의 사전 학습 글을 링크했는데,[^doomroot13] 이 문서는 그 글을 열지 않았다.
발표문만으로는 모델 크기, 학습 방법, 데이터가 알려지지 않는다.

### 실제 사용 경험은 아직 거의 없다

스레드에서 이 모델을 직접 써 본 후기는 눈에 띄지 않았다. 사용자들의 반응은 Copilot 구독의 값어치,[^laurensber] 브랜드명,[^nxtfari] 발표 사이트의 디자인에 대한 이야기가 상당 부분을 차지했다.
한 사용자는 Copilot 구독 크레딧이 API 가격으로 계산되어 사람들이 며칠 만에 소진하므로 구독을 해지했다고 했고,[^laurensber] 다른 사용자는 새 모델이 같은 구독 한도에서 같은 비율로 차감되면 도움이 안 될 것이라고 했다.[^insideoutsanta]
이는 비용 이점이 실제 청구 방식에 달려 있다는 지적이다.

### 외부 반응

HN 스레드는 338점 149개 댓글이다.
Lobste.rs에서는 `microsoft.ai` 도메인이 올라온 적이 없다.
GeekNews에는 같은 글의 토픽이 있으나 댓글이 하나이고, 그것도 HN 댓글을 다시 모은 GN⁺ 계정의 요약이라 GeekNews 이용자의 반응은 없다.

## 인사이트

### 가져갈 것은 모델 선택을 일의 종류별 비용 곡선으로 하는 것이다

발표문의 구분(일상 코딩, 대량 일용 작업, 어려운 장기 작업)은 모델 고르는 틀로 쓸 수 있다.
HN에서 한 사용자는 Opus를 조정자로 두고 값싼 모델을 구현자로 쓰는 구성을 이전 스레드에서 보고했고, 이번 발표는 그 아래 단에 들어갈 후보를 늘린다.
이 문서의 적용이며, 이 문서는 MAI Code 2를 그런 자리에 써서 검증하지 않았다.

### 비용 비교는 가격 조건을 맞춘 뒤 읽는다

프로모션 가격, 추론 강도, 하네스(서브에이전트 유무), 구독 한도 차감 방식이 모두 결과를 바꾼다.
발표문의 40%와 5%를 자기 작업의 청구 방식으로 다시 계산해야 의미가 있다.

### 확인할 관찰

이 발표의 주장을 가를 관찰은 세 가지이다.
독립 평가(최신 판 벤치마크, 서브에이전트 포함)에서 98%와 96%가 유지되는지,
프로모션 종료 뒤의 실제 가격과 Copilot의 구독 한도 차감 방식,
Copilot 밖(OpenRouter, Vercel, Open Code)에서 열린 뒤의 사용 후기이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^kennywinker]: <https://news.ycombinator.com/item?id=50536994>

[^poisonborz]: <https://news.ycombinator.com/item?id=50536507>

[^user43928]: <https://news.ycombinator.com/item?id=50536992>

[^johnfn]: <https://news.ycombinator.com/item?id=50538426>

[^wheen]: <https://news.ycombinator.com/item?id=50537434>

[^uncleoxidant]: <https://news.ycombinator.com/item?id=50536951>

[^throwaw12]: <https://news.ycombinator.com/item?id=50537289>

[^rcarmo]: <https://news.ycombinator.com/item?id=50537977>

[^upbeat_general]: <https://news.ycombinator.com/item?id=50537513>

[^doomroot13]: <https://news.ycombinator.com/item?id=50537563>

[^laurensber]: <https://news.ycombinator.com/item?id=50538591>

[^nxtfari]: <https://news.ycombinator.com/item?id=50538247>

[^insideoutsanta]: <https://news.ycombinator.com/item?id=50538660>
