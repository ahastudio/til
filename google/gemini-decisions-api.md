# Gemini Decisions API: 답을 생성하지 않고 선택지의 확률만 한 번에 돌려주는 Google의 결정 모델

원문: [Gemini Decisions API: Fast, calibrated multimodal decisions](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/)

HN 토론: <https://news.ycombinator.com/item?id=50456791> (274점, 85개 댓글)

GN 토론: <https://news.hada.io/topic?id=37011>

## 요약

Google DeepMind의 제품 관리자와 수석 과학자는 이 글에서 Gemini Decisions API를
소개한다.
새 모델 Gemini Decision 1(`gemini-decision-1`)로 움직이는 새 엔드포인트이며,
Google AI Studio의 Gemini API로 쓴다.
도구 선택, 정책 확인, 모델 라우팅, 맥락 평가처럼 선택지가 정해진 결정을 위한
기본 단위(primitive)라고 설명한다.

입력은 텍스트, 이미지, 오디오, 비디오, PDF를 섞은 하나의 입력(최대 256K 토큰)과
서로 독립적인 질문 최대 1,000개다.
모델은 답을 토큰 단위로 생성하지 않고 후보 선택지를 한 번의 순전파(forward
pass)로 점수 매겨 확률과 신뢰도를 돌려준다.
종단 간 지연은 150~250ms이고 가격은 입력 100만 토큰당 0.10달러이며 출력 토큰은
청구하지 않는다.

질문 유형은 세 가지다.
- `noul`(예/아니오): 조건이 참일 확률을 추정하고, 참과 거짓의 설명 기준을
  선택으로 붙일 수 있다.
- `choice`(다지선다): 2개에서 255개 선택지 가운데 승자를 고르고 모든 후보의
  정규화된 확률을 돌려준다.
- `score`(순서 있는 루브릭): 0부터 시작하는 순서 기준으로 입력을 채점해 연속
  가중 점수와 단계별 확률을 돌려준다.

모든 답에는 0~1의 신뢰도가 붙으므로 모호한 경우를 대체 경로나 사람에게 넘기게 할
수 있다고 글은 말한다.
글의 예제는 탕비실 조리대 사진과 문장 한 줄을 하나의 입력으로 삼아 `noul`(쏟은
액체가 있는가), `choice`(어떤 청소 조치가 맞는가), `score`(어지러운 정도)를 한
번에 묻는다.

성능에 대해 글은 에이전트 라우팅, 추론, 순위, 멀티모달 이해 벤치마크에서 이
모델이 전 항목에서 앞서고 보정 오차(calibration error)가 가장 낮다고 주장한다.
중앙값 모델 연산 지연은 50~100ms(종단 간 150~250ms)이고, 맥락이 16K 토큰까지일
때 요청당 질문이 1개에서 100개로 늘어도 거의 일정하다고 한다.
출력 토큰이 없어서, 공유 벤치마크 전체에서 Gemini 3.5 Flash-Lite를 Interactions
API로 쓸 때보다 거의 5배 싸다고도 한다.
공유 입력은 질문 수와 관계없이 요청당 한 번만 청구되고 질문마다 자기 지침과 기준
토큰만 더해진다.
생각(thinking) 토큰 요금이나 별도의 음성 전사와 OCR 비용도 없다.

Google 안에서의 쓰임으로 네 가지를 든다.
- Gemini Notebook은 요청마다 최적의 모델 등급과 사고 수준으로 보내는 실시간
  라우터로 쓰며, 일상적인 질의는 지연이 최대 40% 낮아진다고 한다.
- Stitch의 빠른 캔버스 실험은 제품 흐름의 플레이 가능한 와이어프레임을 몇 초
  만에 만들고 음성이나 탭 편집을 거의 즉시 반영한다.
- Google Labs의 CC는 200개가 넘는 이모지 가운데 알맞은 반응을 순식간에 고른다.
- Google 검색은 MCP 도구의 안전 계층에서 적대적 행동과 내용을 탐지한다.

OpenRouter, LangChain, Vercel, LiteLLM, Pydantic AI, Pipecat, LiveKit,
OpenCode와 google-genai SDK 통합이 공개되는 중이고 Google Cloud의 Gemini는 곧
지원한다고 한다.
무료 등급도 있다.

## 분석

### 이 API의 핵심은 모델이 아니라 출력의 형태다

생성 모델은 문장을 내놓고 개발자가 그것을 해석한다.
이 API는 출력이 처음부터 확률과 신뢰도라는 타입이 있는 값이다.
글이 “통제 평면(control plane)”이라 부르는 용도, 곧 라우팅, 정책 확인, 채점은
모두 코드가 그 결과로 분기하는 곳이다.
HN에서 npc99는 쓰임을 라우팅, 분류, LLM 심판의 대체로 요약했고,[^npc99]
LaurensBER는 “사람을 방해할 만한가”나 “수상한가” 같은 관문과 필터가 잘 맞고 가끔
심판으로도 쓴다고 했다.[^LaurensBER]
bushbaba는 질문에 맞는 MCP나 스킬을 고르는 도구 라우팅과 평가를
들었다.[^bushbaba]
caseydm은 모델 개발용 학습 데이터에 레이블을 붙이고 홀드아웃 집합으로 확인하는
데 쓴다고 했다.[^caseydm]
공통점은 모두 “답을 쓰는” 일이 아니라 “고르는” 일이라는 점이다.

### 요금 구조가 설계를 바꾼다

공유 입력을 한 번만 청구하고 질문마다 지침 토큰만 더하는 방식은 입력은 길고
질문은 많은 작업을 값싸게 만든다.
HN의 2001zhaozhao는 10만 토큰 맥락에 100토큰짜리 질문 수백 개를 붙이는 것이
Google 검색 API 한 번 호출과 비슷한 비용이라고 계산했고, 같은 질문의 변형을 여러
개 묻는 식으로 다지선다 하나가 잡지 못하는 뉘앙스를 얻을 수 있다고
썼다.[^2001zhaozhao]
LaurensBER는 사내 AI 흐름을 점검하다가 결정 API가 맞는 경우가 많아 놀랐고
일주일을 집중해 실험하고도 5달러를 못 썼다고 했다.[^LaurensBER-2]
이는 개인 증언이며 글이 말하는 가격에서 나오는 계산을 뒷받침한다.

### 확률이 어떻게 나오는지는 글에 없고 독자가 채웠다

글은 모델이 후보를 한 번의 순전파로 점수 매긴다고만 말한다.
eminence32는 어떻게 확률을 계산하는지 물었고,[^eminence32] NitpickLawyer는
“예”와 “아니오”에 해당하는 토큰의 로그 확률을 비교하는 방법이 있다고
답했다.[^NitpickLawyer]
mediaman은 LLM의 토큰 확률은 결정에 쓰기에 보정이 아주 나쁘고 “이건 구조화된
출력 아니냐”는 반응은 보정이 제품의 핵심임을 놓친 것이라고 반박했다.[^mediaman]
janalsncm은 결국 다른 분류기와 같은 방식이고 정답 확률과 예측 확률의 교차
엔트로피로 학습한다고 설명했고,[^janalsncm] computably는 정답 확률을 보통 0과
1로 두므로 불확실한 상황에서 합리적인 분포를 배운다는 보장이 자명하지 않다고
짚었다.[^computably]
이 논쟁이 가리키는 것은 하나다.
이 API가 파는 것은 확률이 아니라 보정된 확률이다.

## 비평

### 가장 강한 주장에 수치가 없다

글의 첫 주장은 이 모델이 벤치마크 전 범위에서 앞서고 보정 오차가 가장 낮다는
것이다.
이 문서가 읽은 본문 텍스트에는 비교 대상 이름도 점수도 없다.
도표가 이미지로 있었을 수 있지만 이 문서는 이미지를 읽지 않았다.
HN에서 wasabi991011은 모든 모델이 벤치마크에서 놀랄 만큼 비슷하다고
했고,[^wasabi991011] keyle은 그것이 더 나은 벤치마크가 필요하다는 신호일
뿐이라고 받았다.[^keyle]
따라서 “앞선다”는 문장은 Google의 주장으로만 읽어야 한다.

### 숫자의 조건이 서로 맞지 않는다

글은 맥락 최대 256K 토큰과 질문 1,000개를 받는다고 쓰고, 속도 주장은 맥락 16K
토큰까지 와 질문 1~100개 범위에서 거의 일정하다고 쓴다.
큰 입력이나 질문 수에서 지연이 어떻게 달라지는지는 글에 없다.
비용 비교의 기준도 생성 모델이다.
“거의 5배 싸다”는 비교 대상이 Gemini 3.5 Flash-Lite와 Interactions API이므로,
같은 종류의 결정 모델과의 비교가 아니다.
HN의 waximabbax는 같은 분야의 다른 결정 모델보다 조금 비싸지만 오디오와 비디오를
입력으로 받는 것이 특정 용도에서는 아주 쓸모 있다고 평했다.[^waximabbax]
Topfi는 자기 쪽 간단한 평가에서 Jev 대비 브라이어(Brier) 점수가 많은 경우 4배
낮았고 (작업에 따라 2~6배) 중앙 지연도 100ms 넘게 낮았지만 전체 비용은 2배였다고
보고했다.[^Topfi]
이 두 증언은 한 사용자의 환경 결과이고 Google의 주장과 달리 비교 대상이
분명하다는 점이 다르다.

### 사용 예시는 모두 Google 안의 것이다

글이 든 네 가지 사례는 Google 내부 제품이다.
“최대 40%”라는 지연 감소는 상한이고 조건이 없으며, 검색의 안전 계층은 “높은
효율”이라고만 쓰고 수치가 없다.
외부 고객의 사용 사례나 실패 사례는 없다.
이는 발표 글의 성격상 자연스럽지만, 독자가 신뢰도 점수를 얼마나 믿고 사람에게
넘기는 기준을 어디에 둘지 판단할 근거는 글에서 얻을 수 없다.

### 오용과 편향에 대한 언급이 없다

tomaskafka는 이를 이름이나 사회적 지위로 사람을 가르고 싶지만 책임은 다른
주체에게 넘기고 싶을 때 쓰는 불투명한 분류기 서비스라고 비꼬며, 이름이 James
Smith인 사람에게 어떤 대출 금리 배수를 줄지 묻는 예를 들었다.[^tomaskafka]
이는 과장된 비판이지만 이 API의 용도 목록(정책 확인, 콘텐츠 채점, 채점 기준
적용)이 사람에 대한 결정으로 쉽게 번질 수 있다는 점을 짚는다.
이 문서가 읽은 본문에는 사용 제한이나 편향 점검을 언급하는 부분이 없다.

### 왜 필요한지부터 묻는 반응이 있었다

5555watch는 이런 결정 모델이 왜 쓸모 있는지 모르겠다고 했고, perching_aix는 추론
없이는 모델이 분류에서도 엉망이므로 학습한 분류기와 무엇이 다른지
물었다.[^perching_aix]
foopod는 바로 그 점이 가치이고 분류기를 학습하지 않고도 기능을 검증할 수 있다고
답했다.[^foopod]
이 가치 제안의 한계는 글에 적혀 있지 않다.
성능이 충분하지 않은 영역에서 언제 직접 학습한 분류기로 넘어가야 하는지는 독자의
몫이다.

### 이 API가 오래 남는지는 알 수 없다

florkbork는 Google이 Jules를 접는 중이라며 이 API도 6개월 뒤에 남아 있을지
모르겠다고 했다.[^florkbork]
Catloafdev는 이것이 Carbon이나 Argon처럼 모델 출시이고 후속 없이 죽지는 않을
것이라고 반박했고,[^Catloafdev] antonvs는 Google이 접는 것은 소비자 제품이고
기업 고객이 돈을 내는 제품은 사정이 다르다고 했다.[^antonvs]
이는 전망의 차이이고 글은 지원 기간이나 모델 폐기 정책을 말하지 않는다.

## 인사이트

### 결정 API는 빠르게 같은 모양으로 수렴하고 차별점은 품질과 지연으로 좁아진다

HN 댓글에는 이 API가 Jev에서 영감을 받은 것이라는 지적이 여럿이다.
iamdelirium은 Google이 Jev에서 영감을 받은 자체 API와 모델을 발표했다고
썼고,[^iamdelirium] claiir가 `noul`이라는 유형 이름을 궁금해하자 iamdelirium은
OpenAI 버전이 아니라 Jev의 API를 본떴기 때문이라고 답했으며,[^iamdelirium-2]
theanonymousone은 Bernoulli에서 나온 이름으로 보인다고 했다.[^theanonymousone]
이 이름의 유래는 댓글의 추측이며 글은 설명하지 않는다.
nrightnour는 OpenAI가 이미 결정 API를 만들고 있었고 Jev가 먼저 내 일주일간
주목을 받았다고 했고,[^nrightnour] IncreasePosts는 OpenAI가 Jev 뒤 2주, Google이
2개월 걸린 차이가 왜 생기는지 물었다.[^IncreasePosts]
인터페이스가 이렇게 수렴하면 스타트업이 남길 수 있는 차별점은 품질과 속도로
좁아진다.
mikeocool은 처음 경쟁 모델들이 나왔을 때 Jev가 훨씬 빨랐고 250ms 응답은
750ms로는 열리지 않는 가능성을 연다고 썼다.[^mikeocool]
holografix는 Google의 이 제품을 “우리도 한다”는 견실하지만 뛰어나지 않은
제품이고 기존 고객의 지출 점유율을 확보하려는 가격 정책이라고
평했고,[^holografix] SchemaLoad는 회사가 이미 계약한 플랫폼의 제품을 쓰는 것이
새 서비스에 결제를 요청하는 것보다 쉽다는 기업 기술의 오랜 방식이라고
답했다.[^SchemaLoad]
이 둘은 시장 해석이며 이 문서가 검증한 것이 아니다.

### 이 API를 쓰기 전에 해야 할 것은 자기 데이터에서 보정을 재는 일이다

글이 약속하는 것은 신뢰도 점수로 모호한 경우를 사람에게 넘기는 설계다.
이 설계는 점수가 실제 정답률과 맞을 때만 안전하다.
Topfi의 사례는 브라이어 점수로 직접 비교해 본 것이다.[^Topfi]
따라서 라우팅이나 관문에 쓰기 전에 자기 레이블 데이터로 보정을 재고, 신뢰도
임계값을 그 곡선으로 정하는 것이 순서다.
이는 이 문서의 제안이다.
그 과정에서 비교 대상을 학습한 작은 분류기, 직접 만든 로그 확률 방식, 다른
사업자의 결정 모델로 두면, 글이 말하지 않은 “어느 쪽이 내 문제에 싼가”도 함께
얻는다.

### 결론을 바꿀 관찰

- 공개된 벤치마크에서 Gemini Decision 1과 경쟁 결정 모델의 보정 오차가
  독립적으로 측정되어 Google의 우위가 확인된다면, “가장 낮은 보정 오차”라는
  주장이 받아들여진다.
- 맥락 16K를 넘는 입력이나 질문 수백 개에서 지연과 정확도가 크게 나빠진다고
  보고되면, 256K와 1,000이라는 한도의 실용적 의미가 줄어든다.
- 모델 폐기 일정이나 지원 정책이 문서화되면, 오래 남는지에 대한 우려가 정리된다.

---

[^npc99]: <https://news.ycombinator.com/item?id=50459050>

[^LaurensBER]: <https://news.ycombinator.com/item?id=50460348>

[^bushbaba]: <https://news.ycombinator.com/item?id=50460716>

[^caseydm]: <https://news.ycombinator.com/item?id=50459244>

[^2001zhaozhao]: <https://news.ycombinator.com/item?id=50460195>

[^LaurensBER-2]: <https://news.ycombinator.com/item?id=50460278>

[^eminence32]: <https://news.ycombinator.com/item?id=50458144>

[^NitpickLawyer]: <https://news.ycombinator.com/item?id=50458445>

[^mediaman]: <https://news.ycombinator.com/item?id=50458796>

[^janalsncm]: <https://news.ycombinator.com/item?id=50458721>

[^computably]: <https://news.ycombinator.com/item?id=50459216>

[^wasabi991011]: <https://news.ycombinator.com/item?id=50459043>

[^keyle]: <https://news.ycombinator.com/item?id=50459415>

[^waximabbax]: <https://news.ycombinator.com/item?id=50456959>

[^Topfi]: <https://news.ycombinator.com/item?id=50461867>

[^tomaskafka]: <https://news.ycombinator.com/item?id=50461434>

[^perching_aix]: <https://news.ycombinator.com/item?id=50460516>

[^foopod]: <https://news.ycombinator.com/item?id=50461945>

[^florkbork]: <https://news.ycombinator.com/item?id=50457907>

[^Catloafdev]: <https://news.ycombinator.com/item?id=50458079>

[^antonvs]: <https://news.ycombinator.com/item?id=50459585>

[^iamdelirium]: <https://news.ycombinator.com/item?id=50456792>

[^iamdelirium-2]: <https://news.ycombinator.com/item?id=50458864>

[^theanonymousone]: <https://news.ycombinator.com/item?id=50458822>

[^nrightnour]: <https://news.ycombinator.com/item?id=50459205>

[^IncreasePosts]: <https://news.ycombinator.com/item?id=50457990>

[^mikeocool]: <https://news.ycombinator.com/item?id=50460123>

[^holografix]: <https://news.ycombinator.com/item?id=50458930>

[^SchemaLoad]: <https://news.ycombinator.com/item?id=50459790>
