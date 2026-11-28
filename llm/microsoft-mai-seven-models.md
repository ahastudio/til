# Microsoft AI의 모델 7종 발표

원문: [Seven new world-class models at scalable price-performance](https://microsoft.ai/news/microsoft-ignite-2026/)

HN 토론: <https://news.ycombinator.com/item?id=50548021> (456점, 318개 댓글)

GN 토론: <https://news.hada.io/topic?id=37419>

## 요약

Microsoft AI(MAI)가 2026년 11월 17일 Ignite 2026에 맞춰 낸 발표 글이다(분류 「Announcements」, 태그 Ignite). 저자 표기는 없다.
제목은 「확장 가능한 가격 대비 성능의 세계 수준 모델 7종」이다.
글은 토큰 지출이 늘면서 고객이 에이전트를 24시간 돌릴 만큼 싼 모델을 원한다는 전제에서 시작한다.
각 모델의 개별 발표 글과 벤치마크 원자료, 가격표는 열지 못했고 글에도 표가 없다.
글에서 비교 대상 모델명은 정의 없이 쓰인다.

7종과 글이 적은 수치는 다음과 같다.

| 모델                      | 글의 주장                                                                                    |
| ------------------------- | -------------------------------------------------------------------------------------------- |
| MAI Cyber 2 Flash         | CyberGym-E2E에서 GPT-6 Astra보다 높은 품질을 작업당 비용 2% 미만으로 낸다                    |
| MAI Code 2                | 코딩 품질이 GPT-6.1 Sol의 98%를 가격 약 40%에, Opus 5.5의 96%를 가격 5%에 낸다               |
| MAI Code 2 Flash          | GPT-6 Luna와 비슷한 품질을 가격 65%에, Haiku 5.5와 비슷한 품질을 가격 20%에 낸다             |
| MAI Image 2.7             | Artificial Analysis의 이미지 편집 1위, GPT Image 2.6 Sunburst(max)를 5분의 1 가격으로 앞선다 |
| MAI Realtime 1            | GPT-Realtime 2.1보다 높은 성능, 오디오 분당 0.01달러부터                                     |
| Dragon Copilot Transcribe | MAI Transcribe 2 기반, 월 1,000만 환자 접촉을 처리하고 다국어 오류율을 절반으로 줄였다       |
| Decision 1.1              | GPT-6.1 Sol보다 50배 빠르고 79배 저렴하다                                                    |

인프라로는 Microsoft의 2세대 AI 가속기 Maia 200이 가장 큰 모델을 돌리는 프로덕션에 들어갔고 와트당 토큰이 1.7배라고 적는다.

절별 내용은 다음과 같다.

- 사이버 방어: 보안, 정렬, 격납이 2027년 이후 에이전트 개발의 최우선이라고 하고, 감시와 제어 에이전트가 살아 있는 시스템을 24시간 고쳐야 한다고 한다. MAI Cyber가 MDASH 스캔의 약 40%를 차지하고 MAI로 시작한 스캔의 90%가 계속 MAI를 쓴다. MAI Cyber 2 Flash의 출력 토큰 가격은 MAI Cyber 1.1 Flash보다 86% 낮다.
- 코딩: MAI Code 2는 일상적 기업 코딩용이다. 네 벤치마크(DeepSWE 1.1, Terminal Bench 2.1, SWE-Atlas, FrontierCode v1.1)의 평균으로 위 수치를 냈고 기초 과학 연구나 매우 긴 에이전트 작업에는 아직 맞춰지지 않았다. 대시보드와 시각화에 맞춰졌고 프런트엔드 맹검 비교에서 개발자가 GPT-6 Sol보다 64% 선호했다. GitHub Copilot에서 쓸 수 있다. Flash는 설명, 국소 수정, 반복 같은 대량 작업용으로 GitHub Copilot과 Microsoft Foundry의 제한된 미리 보기에 있다.
- 이미지와 전사: MAI Image 2.7은 텍스트 투 이미지에서 4위이고 Flash는 이미지 1,000장에 약 10달러이며 둘 다 Foundry에 있다. MAI Realtime 1은 첫 실시간 음성 대 음성 모델이라고 하며 MAI Labs에서 시험할 수 있다. Dragon Copilot Transcribe는 의사와 환자 대화의 100%를 전사하고 미국 의사의 3분의 1이 쓴다고 한다.
- 의사결정 모델: 더 크고 비싼 모델이 필요할 때만 돌리게 하는 라우팅이다. Artificial Analysis 의사결정 지수에서 「Jev, Google, OpenAI」보다 앞서고 더 빠르고 싸다고 한다(글에 적힌 대로). 고객 4,000곳이 쓴다.
- 맞춤: 고객이 자기 IP를 남의 모델에 넣기를 꺼리고 오픈 가중치는 신뢰 문제를 낳는다고 한다. AT&T가 5G 네트워크 운영 분석용 MAI 맞춤 모델을 만들어 GPT-6.1 Sol보다 50분의 1 비용으로 앞섰다고 한다. 새로 나온 MAI Licensed Weights는 고객이 프런티어 MAI 모델을 받아 선택적으로 자기 데이터로 맞춤하고 자기 Azure 환경에서 돌리며 접근과 데이터와 조정 결과를 통제하는 방식이다.

마무리 문구는 「당신의 IQ. 당신의 에이전트. 당신의 가중치」이다. 글에 가용 시점, 별도 가격표, 벤치마크 점수표, 이름이 붙은 인용은 없다.

## 분석

### 중심 주장은 가격 대비 성능이다

모든 항목이 「X의 품질을 Y% 가격에」 형태이고 절대 성능이 아니라 비율이다. 에이전트를 상시 돌리는 비용 구조에 맞춘 메시지이다. 이는 발표의 서술을 이 문서가 정리한 것이다.

### 모델과 배포 방식을 함께 판다

가중치를 라이선스해 고객 환경에서 돌리게 하는 방식은 API 호출만 파는 모델과 다른 선택지를 낸다. 글은 데이터 통제를 이 방식의 이유로 내세운다.

### 내부 비교의 기준이 정해져 있다

MAI Code 2 수치는 네 벤치마크의 평균이고 GitHub Copilot 업무에 맞춘다고 한정한다. 비교 대상(Opus 5.5, GPT-6.1 Sol)도 이름으로 분명히 적는다.

## 비평

### 수치의 산출 방법이 빠져 있다

HN에서 한 사용자는 Opus 5.5 비교가 대담한 주장이라고 했고 다른 사용자는 98%라는 수치를 어떻게 얻는지 물었다.[^tyingq][^spprashant]
글은 네 벤치마크의 평균이라고만 밝히고 개별 점수와 가격 기준(어떤 단가와 사용량)을 싣지 않는다. 가격 대비 성능의 분모가 되는 가격의 정의도 없다.

### 독립 벤치마크에 없다

HN에서 한 사용자가 왜 Artificial Analysis 지수에 오르지 않았는지 묻자 다른 사용자는 벤치마크용으로 모델을 제공하지 않았을 수 있다고 추측했다.[^theowaway213456][^killingtime74]
글이 내세우는 이미지 편집 1위도 Artificial Analysis의 순위이지만 텍스트 투 이미지는 4위이다.

### 사용 후기는 호평과 회의가 섞였다

한 사용자는 MAI Code 2를 써 보니 일에서 꽤 좋고 Opus나 Sol과 비슷하다고 했다.[^johnshahbazian] 다른 사용자는 OpenAI와의 관계 때문에 「처음부터 만들었다」는 평가에 의문을 던졌다.[^nicce]
키노트가 얄팍하고 기회주의적이라는 평가도 있었다.[^m4r5h4ll] 이는 개인 의견이다.

### 배포 전략과 시장 평가가 갈린다

한 사용자는 Microsoft가 일부 모델을 오픈 가중치로 내야 시장 점유율을 얻고 아니면 Windows Phone처럼 된다고 했고, 다른 사용자는 Anthropic보다 90에서 95% 저렴해 수요가 크고 Windows Phone의 실패(네트워크 효과)와 무관하다고 반박했다.[^ahmedfromtunis][^mediaman]
한 사용자는 AI 회사가 전기 모터를 발명한 것과 같아 해자가 없다고 평했다.[^rayiner]

### 외부 반응

HN 글 제목은 「Seven new models at scalable price-performance」이다.
Lobste.rs의 `microsoft.ai` 도메인에는 글이 없었다.

## 인사이트

### 가져갈 것은 비율 주장을 읽는 순서이다

「X의 N%를 가격 M%에」를 볼 때 벤치마크의 구성, 평균의 정의, 가격의 기준(입력과 출력 단가, 사용량), 비교 대상 모델의 버전을 따로 확인한다. 자기 작업으로 같은 비교를 해 보는 것이 가장 믿을 만하다. 이는 이 문서의 적용이다.

### 데이터 통제가 중요하면 배포 방식을 따진다

API로 쓰는 것과 가중치를 자기 환경에서 돌리는 것은 데이터 통제와 운영 책임이 다르다. 맞춤 모델(AT&T 사례)을 검토한다면 평가 기준을 자기 업무로 정한다.

### 확인할 관찰

이 발표의 주장을 가를 관찰은 세 가지이다.
독립 벤치마크의 공개 결과,
자기 업무에서의 품질과 총비용,
Licensed Weights의 조건과 가격이다.

---

[^tyingq]: <https://news.ycombinator.com/item?id=50549241>

[^spprashant]: <https://news.ycombinator.com/item?id=50550664>

[^theowaway213456]: <https://news.ycombinator.com/item?id=50548601>

[^killingtime74]: <https://news.ycombinator.com/item?id=50551760>

[^johnshahbazian]: <https://news.ycombinator.com/item?id=50549009>

[^nicce]: <https://news.ycombinator.com/item?id=50550115>

[^m4r5h4ll]: <https://news.ycombinator.com/item?id=50548659>

[^ahmedfromtunis]: <https://news.ycombinator.com/item?id=50548446>

[^mediaman]: <https://news.ycombinator.com/item?id=50548641>

[^rayiner]: <https://news.ycombinator.com/item?id=50551084>
