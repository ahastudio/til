# Tencent Hy4 Flash

<https://hy.tencent.ai/research/hy4-flash>

HN 토론: <https://news.ycombinator.com/item?id=50538184> (166점, 26개 댓글)

GN 토론: <https://news.hada.io/topic?id=37434>

## 소개

2026년 11월 16일 Tencent가 공개한 Hy4 flash 소개 글이다.
Hy 모델 가운데 가장 비용 효율이 높다고 내세운다.
부록의 벤치마크 결과(Appendix)는 텍스트로 읽히지 않아 확인하지 못했고, 그림 1과 2의 숫자도 읽지 못했다.
직접 써 보지 않았다.
아래 수치는 모두 Tencent가 적은 값이다.
같은 계열의 이전 모델은 `llm/tencent-hy4.md`와 `llm/hy4.md`에 정리되어 있다.

모델의 사양은 다음과 같다.

- 크기: 총 2,240억 파라미터(Engram 파라미터 640억 포함)에 토큰당 활성 120억 파라미터이다.
- 입력: Hy4처럼 네이티브 멀티모달이고 문맥 창은 100만 토큰이다.
- 구조: 하이브리드 어텐션(hybrid attention), LatentMoE, Engram을 합쳐 KV 캐시 크기를 Hy3의 1/24, Hy4의 1/6으로 줄였다고 한다.
- 후속 학습: Hy4에서의 자기 증류(self-distillation)로 일반 지능을 만들고, 강화학습으로 평균 종단 간 출력 토큰을 50% 줄였다.
- 추론: 메가커널(megakernel), 4비트 양자화, DFly를 묶어 디코딩 속도가 초당 150토큰을 넘긴다고 한다.

API 가격은 100만 토큰당 다음과 같다.

| 모델      | 캐시된 입력 | 입력   | 출력   |
| --------- | ----------- | ------ | ------ |
| Hy4 flash | $0.003      | $0.070 | $0.281 |
| Hy4       | $0.042      | $0.834 | $2.501 |

평가 방식과 결과에 대한 글의 서술은 다음과 같다.

- 평가 설계: 공개 벤치마크 점수가 아니라 일상 업무에 맞춰, WorkBuddy 작업에 기반한 내부 벤치마크 WorkIndex와 사람 평가를 함께 썼다. 산출물 품질, 한 번의 출력 길이, 작업 소요 시간을 본다.
- WorkIndex 구성: 슬라이드 만들기, 슬라이드 수정, 사람과 AI의 슬라이드 공동 작성, Markdown 공동 작성, 문서 편집, 스프레드시트 수리, 오디오와 비디오 처리, 시각 이해의 8개 평가 세트이다.
- 공개 벤치마크: DeepSWE, ProgramBench, Terminal-Bench 4.0, APEX-Agents, AutomationBench, HLE, OSWorld 2.1의 7개이다.
- 결과: 전체 작업 성능이 Hy4 preview를 약간 웃돈다. WorkIndex에서 작업당 평균 비용은 Hy4 preview의 1/13, Hy4의 1/20, DeepSeek-V4.1-Flash-1017(Max 계층, 피크 시간 가격)의 1/8이다.
- 사용자 평가: WorkBuddy 내부 사용자 85명이 27개 범주 259개 작업을 블라인드로 평가했을 때 만족도가 Claude Haiku 5.5에 가까웠고, 완료 시간은 가장 짧고 작업당 비용은 평가한 다른 모델보다 크게 낮았다고 한다.

제공은 다음과 같다.

- 제품: Tencent Cloud TokenHub, WorkBuddy, Yuanbao, WeCom, QQ, ima, Marvis 등에서 쓸 수 있고 OpenRouter는 곧 시작한다.
- 혜택: 11월 30일까지 WorkBuddy에서 무료이고 TokenHub의 API 가격은 50% 할인이다.
- 가중치: GitHub, Hugging Face, ModelScope, AtomGit에 공개되었다. Hy4의 가중치는 곧 공개한다고 한다.
- 권장: 딥 서치, 문서 처리, 슬라이드 만들기, 간단한 프런트엔드 시연, 컴퓨터 사용에는 Hy4 flash를, 장기 소프트웨어 공학 같은 복잡한 작업에는 지능 상한이 높은 Hy4를 권한다.

글은 이어 Tencent 내부 팀의 사용 후기를 싣는다.

| 팀             | 글의 수치                                                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| WorkBuddy      | Hy4 대비 평균 작업 시간 70% 감소, 비용 약 1/15, 일상 작업 품질은 같고 장기 코딩에서 약간 낮음                                   |
| Yuanbao        | Hy3 대비 에이전트 성능 13.6% 향상, 사람 나란히 비교(GSB) 7.56% 향상, 일반 대화에서 GLM-5.3-Flash보다 2.52% 높음                 |
| WeChat Pay     | DeepSeek-V4.1-Flash-1017 대비 실행 단계 약 6%와 한 번의 출력 길이 약 29% 감소, 정적 코드 스캔에서 완료 시간 37%와 토큰 46% 감소 |
| WeCom          | Hy4 대비 출력 속도 88% 증가, 사고 모드 출력 토큰 약 60% 감소                                                                    |
| Honor of Kings | 버그 원인 위치 찾기가 DeepSeek-V4.1-Flash-1017과 GLM-5.3-Flash에 근접하며 모델 요청 22.0%에서 39.1%, 토큰 40.5%에서 61.2% 감소  |
| ima            | 지식 베이스 질의응답 대기 시간 18%에서 35% 감소, 전체 응답 평가 1.8%와 내용 품질 8.1% 상승                                      |
| QQ             | 만족 응답률 최대 6.16%p 상승, 완료 시간 약 11%에서 27% 감소, P90 댓글 지연 39% 감소                                             |
| Marvis         | 앱 설치 6.2%, 시스템 설정과 진단 4.4%, 문서 처리와 보고서 6.9% 만족도 상승                                                      |

## 분석

### 중심 주장은 성능 순위가 아니라 작업당 비용이다

글은 공개 벤치마크의 점수를 내세우지 않고 일상 업무의 작업당 비용과 소요 시간을 기준으로 삼는다고 직접 밝힌다.
Hy4와의 관계도 대체가 아니라 분담이다. 일상 작업은 flash, 복잡한 장기 공학은 Hy4가 맡는다.
이는 글의 서술을 이 문서가 정리한 것이다.

### 비용 절감은 세 곳에서 나온다

구조(KV 캐시 축소, 활성 파라미터 120억), 후속 학습(출력 토큰 50% 감소), 추론(양자화와 커널)이다.
가격표는 입력 단가가 Hy4의 약 1/12, 출력이 약 1/9이고, 작업당 비용은 1/20로 나와 토큰 수 감소가 더해진 격이다. 이 계산은 글의 두 수치를 이 문서가 비교한 것이다.

### 파라미터 수의 읽는 방법

HN 사용자 syntaxing은 2,240억 파라미터 중 Engram이 640억이라는 점에서 두 대의 128GB 기기에서 돌릴 수 있을지 물었고, anon373839는 Engram 부분을 SSD로 내릴 수 있어 메모리에 올릴 부분이 약 1,600억이라고 짚었다.[^syntaxing][^anon373839]
ycui7는 NVIDIA가 4비트 양자화 인식 학습(QAD)판을 내면 DGX Spark 한 대에서 돌릴 수 있다고 했다.[^ycui7] 이들은 추정이다.

## 비평

### 핵심 벤치마크가 자사 내부 평가이다

WorkIndex는 WorkBuddy 작업에 기반한 내부 벤치마크이고 사용자 평가도 내부 사용자 85명이다.
DeepSeek-V4.1-Flash-1017과의 비교는 Max 계층의 피크 시간 가격 기준이라 기준 선택이 결과에 영향을 준다.
HN에서 DeathArrow는 작업당 비용으로 DeepSeek V4.1 Flash를 이긴다고 보지 않으며 캐시 적중이 높은 저가 공급자가 있다고 했다.[^deatharrow]

### 외부 시험은 갈린다

chriddyp는 자신의 데이터 분석 벤치마크에서 저가 정확도 구간에서 GPT-6 Luna를 앞섰고 43문항에 0.13달러가 들었다고 했다.[^chriddyp]
thesurlydev는 OpenRouter에서 며칠 DeepSeek flash 대신 써서 좋은 결과를 얻었다고 했다.[^thesurlydev]
반면 edtechdev는 번역 작업에서 DeepSeek 4.1 Flash보다 오류가 훨씬 많았다고 했고, vcryan은 조금 느리다고 했다.[^edtechdev][^vcryan]
ketzu는 Hy4를 OpenRouter로 쓸 때 응답이 자주 깨졌다고 했다.[^ketzu] 이 지적은 Hy4에 대한 것이며 flash에도 해당하는지는 글에서 알 수 없다.

### 속도와 안정성은 공급자에 달렸다

글은 디코딩 속도가 초당 150토큰을 넘긴다고 한다.
throwa356262는 Eden이 Hy4를 초당 40토큰으로 보고하고 OpenRouter 오류율이 작지 않다고 했다.[^throwa356262]
Rodmine은 더 작은 크기가 제3자 공급자의 더 빠른 제공으로 이어지길 기대했고, nolok은 빠르다는 말이 추론 속도와 적은 토큰 중 어느 쪽인지 구분해서 읽으라고 했다.[^rodmine][^nolok]

### 가중치 공개는 HN에서 확인되었다

글은 Hy4 flash의 가중치가 이미 공개되었고 Hy4의 가중치는 곧 공개한다고 쓴다.
HN에서 chriddyp는 가중치가 공개되면 자신의 평가에서 상위권 공개 모델이 Hy4 flash와 Hy4뿐이 된다고 했고, alfiedotwtf는 Hugging Face의 `tencent/Hy4-flash`와 GGUF 저장소 주소를 알렸다.[^chriddyp][^alfiedotwtf]

### 외부 반응

GeekNews 토픽(37434)에는 이용자 댓글이 없고 GN⁺가 옮겨 온 Hacker News 의견 블록만 있어 반영하지 않았다.

## 인사이트

### 가져갈 것은 모델을 작업당 비용으로 비교하는 방식이다

토큰 단가는 출력 토큰 수와 단계 수가 달라지면 의미가 바뀐다. 같은 작업을 끝내는 비용과 시간을 자기 작업으로 재 보는 것이 가장 믿을 만하다. 이는 이 문서의 적용이다.

### 분담 구도를 시험할 만하다

일상 작업은 flash, 장기 공학은 Hy4라는 글의 권장은 자기 환경에서 품질 저하가 어디서 시작되는지 재 보는 출발점이 된다. 번역처럼 flash가 약했다는 보고도 있어 작업 종류별로 나눠 본다.

### 확인할 관찰

이 글의 주장을 가를 관찰은 세 가지이다.
공개 벤치마크 7종의 점수와 독립 평가에서의 작업당 비용,
제3자 공급자에서의 속도와 오류율,
공개된 가중치의 라이선스와 로컬 실행 성능이다.

---

[^syntaxing]: <https://news.ycombinator.com/item?id=50541480>

[^anon373839]: <https://news.ycombinator.com/item?id=50542325>

[^ycui7]: <https://news.ycombinator.com/item?id=50543043>

[^deatharrow]: <https://news.ycombinator.com/item?id=50543659>

[^chriddyp]: <https://news.ycombinator.com/item?id=50540077>

[^thesurlydev]: <https://news.ycombinator.com/item?id=50540052>

[^edtechdev]: <https://news.ycombinator.com/item?id=50543675>

[^vcryan]: <https://news.ycombinator.com/item?id=50540018>

[^ketzu]: <https://news.ycombinator.com/item?id=50542324>

[^throwa356262]: <https://news.ycombinator.com/item?id=50551825>

[^rodmine]: <https://news.ycombinator.com/item?id=50540304>

[^nolok]: <https://news.ycombinator.com/item?id=50543387>

[^alfiedotwtf]: <https://news.ycombinator.com/item?id=50544563>
