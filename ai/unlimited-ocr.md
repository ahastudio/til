# Unlimited-OCR — 단일 패스 장문서 파싱 엔진

<https://github.com/baidu/Unlimited-OCR>

HN 토론: <https://news.ycombinator.com/item?id=48643426> (489점, 110개 댓글)

## 소개

Unlimited-OCR은 바이두(Baidu)가 2026년 6월 23일 공개한 문서 파싱 시스템이다.
DeepSeek-OCR, DeepSeek-OCR-2, PaddleOCR의 성과를 기반으로
“한 단계 더 나아가는” 것을 목표로 한다.
한 번의 추론 패스로 긴 문서를 파싱하는 “One-shot Long-horizon Parsing”을 핵심 가치로 표방한다.
MIT 라이선스로 공개됐으며 Hugging Face와 ModelScope에서 모델을 다운로드할 수 있다.

추론 프레임워크로는 Hugging Face Transformers와 SGLang을 모두 지원한다.
SGLang을 통해 OpenAI 호환 API를 제공하며 배치 처리와 스트리밍 추론이 가능하다.
bfloat16 정밀도로 동작하며 최대 32,768 토큰을 생성한다.

단일 이미지 처리에는 두 가지 모드가 있다.

- **Gundam 모드**: `base_size=1024`, `image_size=640`, `crop_mode=True`
- **Base 모드**: `base_size=1024`, `image_size=1024`, `crop_mode=False`

다중 페이지 처리는 Base 설정만 사용하며(`image_size=1024`),
PDF를 자동으로 이미지 시퀀스로 변환한다.
반복 토큰 생성 방지를 위해 커스텀 no-repeat n-gram 로짓 프로세서를 사용하며,
`no_repeat_ngram_size`는 35, `ngram_window`는 단일 이미지 128, 다중 페이지 1,024다.

주요 의존성은 Python 3.12.3 + CUDA 12.9 환경에서 torch 2.10.0,
transformers 4.57.1, PyMuPDF 1.27.2.2(PDF 처리), einops 0.8.2, Pillow 12.1.1이다.

## 분析

### R-SWA가 VRAM 병목을 해결하는 방식이 작업 특성을 반영한다

전통적인 장문서 처리에서 KV 캐시는 생성 토큰 수에 비례해 O(N)으로 선형 증가하여
결국 VRAM을 고갈시킨다.
Unlimited-OCR은 Reference Sliding Window Attention(R-SWA)으로 이 문제를 해결한다.
robotswantdata가 설명하듯, 핵심은 원본 문서에 대한 전체 참조는 유지하되
생성된 텍스트에 대한 메모리는 작은 슬라이딩 윈도우로 제한하는 것이다.[^robotswantdata]

이 분리는 OCR이라는 작업의 특성을 직접 활용한다.
원본 이미지는 고정된 참조이고, 생성되는 텍스트는 순차적으로 진행된다.
따라서 원본 이미지에 대한 주의는 항상 필요하지만,
이미 생성된 출력에 대한 주의는 최근 문맥만으로 충분하다는 직관이 아키텍처로 표현됐다.
`ngram_window`가 단일 이미지에서 128, 다중 페이지에서 1,024로 다른 것도
이 슬라이딩 윈도우 크기가 문서 복잡도에 따라 조정됨을 보여 준다.

### VLM의 이미지 처리 방식이 전통 OCR과 근본적으로 다르다

functional_dev가 설명하듯, 비전-언어 모델은 이미지를 고정된 격자 패치로 분할하여
각 패치를 문장의 단어처럼 처리한다.[^functional_dev]
이는 전통 OCR이 글자 사이의 공백을 찾아 순차 파싱하는 것과 근본적으로 다른 접근이다.

“한 번에 한 페이지씩 VLM에 처리”와 Unlimited-OCR의 다중 페이지 처리 차이는
이 패치 기반 처리가 문서 전체 맥락을 어떻게 유지하느냐에 있다.
한 페이지씩 처리하면 테이블이 두 페이지에 걸쳐 있거나
각주가 다음 페이지까지 이어지는 경우의 맥락을 잃는다.
R-SWA는 이 맥락을 유지하면서 VRAM 효율성을 확보하는 방식이다.

### 이름이 방법론의 본질을 드러낸다

프로젝트 이름 “Unlimited OCR Works”는 Fate/stay night의 “Unlimited Blade Works”에서 왔다.
novoreorx가 지적하듯, 원작에서 이 마법의 전제는 “다른 이가 단련한 무기를 복사하는 것”이다.[^novoreorx]
DeepSeek-OCR, DeepSeek-OCR-2, PaddleOCR에 명시적으로 감사를 표하며
그 모델과 아이디어를 기반으로 확장한다는 점에서 이름이 방법론을 정확히 반영한다.

오픈소스 생태계에서 누적적 발전 방식은 흔하지만, AI 모델 개발에서는 특히 직접적이다.
사전 학습된 모델을 기반으로 아키텍처를 수정하는 방식은
새로운 기반 모델을 처음부터 훈련하는 것과 근본적으로 다른 자원 요구를 가진다.
연구 기여의 출발점이 선행 연구의 어깨 위에 있다는 것이 명시적으로 인정된다는 점은,
이 분야의 누적적 발전 속도가 왜 빠른지를 설명한다.

## 비평

### 벤치마크 없는 주장은 실용적 가치를 검증할 수 없게 한다

aliljet은 Infinity Parser 2와의 비교를 질문하면서,
OCR 벤치마크가 단일하지 않고 Unlimited-OCR이 어디에도 아직 등장하지 않는다고 지적한다.[^aliljet]
gettingoverit도 FineReader와의 비교를 묻는다.[^gettingoverit]
트랜스포머 기반 OCR 간 비교는 의미가 없으며,
“법률 문서를 OCR 하라”는 수준의 품질이 진짜 기준이어야 한다는 것이다.

README에 정량적 벤치마크가 없다는 것은 심각한 누락이다.
문서 파싱 도구의 실질적 가치는 특정 도메인에서의 정확도로 결정된다.
숫자 없이 “one-shot long-horizon parsing”을 표방하는 것은
마케팅 언어이지 기술 문서가 아니다.
도입을 고려하는 엔지니어는 논문(arxiv.org/abs/2506.23050)을 직접 읽어야
성능 주장의 실체를 확인할 수 있다.

### VLM 기반 OCR의 다국어 처리는 충실도를 위협할 수 있다

pmarreck은 자신의 구현 경험에서 AI OCR이 다른 언어로 된 단어를
영어로 자동 번역하는 문제를 겪었다고 지적한다.[^pmarreck]
OCR의 핵심 요구사항은 원문을 충실하게 재현하는 것인데,
VLM 기반 OCR은 언어 이해 능력이 오히려 방해 요소가 될 수 있다.

이 문제는 VLM의 근본적 특성에서 온다.
VLM은 언어 모델이기도 하기 때문에 입력을 “이해”하려는 경향이 있다.
전통 OCR은 글자 패턴을 인식하지만 의미를 해석하지 않는다.
VLM은 의미를 파악하는 과정에서 원문을 수정할 위험이 있다.
Unlimited-OCR이 이 문제를 어떻게 다루는지 README는 설명하지 않는다.
다국어 문서, 특히 코드 스위칭이 빈번한 문서에서 충실도는 별도로 검증돼야 한다.

### “One-shot”의 핵심이 정교한 청킹이라면 혁신의 차별성이 약해진다

alansaber의 “We've invented chunking? We are so back.” 댓글은 냉소적이지만 핵심을 찌른다.[^alansaber]
`ngram_window`가 128 / 1,024라는 설정은 결국 슬라이딩 윈도우, 즉 청킹의 변형임을 드러낸다.

R-SWA가 기술적으로 정교한 청킹이라면, 혁신의 차별성은 구현 세부 사항에 있다.
기술 설명 없이 “one-shot”과 “unlimited”를 표방하는 것은
기존 chunking-based RAG 파이프라인 대비 어떤 점이 근본적으로 다른지 설명하지 못한다.
“슬라이딩 윈도우로 메모리를 줄였다”는 것과 “진정한 단일 패스”는 다른 주장이고,
현재 문서는 이 구분을 명확하게 하지 않는다.

## 인사이트

### 전략적 오픈소스는 표준 선점을 목표로 한다

arboles는 왜 기업이 진정으로 좋은 소프트웨어를 오픈소스로 공개하는지 묻는다.[^arboles]
경쟁사가 모방할 수 없는 방식으로 가치를 추출해야 하는 것 아닌가?
이 질문에 대한 답은 문서 파싱이 상품화(commoditize)될수록
그 위에 쌓이는 서비스가 가치를 갖는다는 것이다.

바이두가 Unlimited-OCR을 오픈소스로 공개하는 것은 문서 파싱 표준을 선점하려는 시도다.
PDF, 이미지, 다중 페이지 문서 파싱이 표준화되면,
바이두의 클라우드 API와 서비스가 그 위에 자리잡는다.
이는 Google이 TensorFlow를, Meta가 PyTorch를 오픈소스로 공개한 전략과 같은 패턴이다.
핵심 인프라를 상품화하고 그 위에 독점적 서비스를 구축한다.

오픈소스 공개로 생태계 채택이 빠르게 이루어지면,
커뮤니티가 버그를 수정하고, 다양한 도메인에 적용하고,
모델이 개선될 수 있는 피드백 루프가 만들어진다.
기업이 혼자 할 수 없는 규모의 테스트와 개선이 무상으로 이루어지는 구조다.

### 음악 악보 인식은 OCR의 미개척 영역이다

peatmoss는 음악 악보 인식(Optical Music Recognition, OMR)이 AI에게 “미개척지”라고 지적한다.[^peatmoss]
재즈 리드 시트를 디지털화하려 했지만 스캔 이미지는 크기 조정이나 조옮김이 불가능하다.
MIDI는 재생에만 특화돼 있으며, MusicXML은 악보 소프트웨어에 필요한 조판 정보가 부족하고,
LilyPond는 채택률이 낮다.

Unlimited-OCR처럼 VLM 기반 문서 파싱이 일반화되면,
다음 문제는 이미지-텍스트 쌍이 아닌 이미지-구조화된 표현 쌍이 될 것이다.
음악 악보, 수학 수식, 화학식, 건축 도면은 모두 “텍스트가 아닌 기호 시스템”이라는 공통점을 가진다.
이 영역에서 훈련 데이터의 부재가 성능의 병목이고,
바이두의 PaddleOCR 배경은 이 방향으로의 확장을 시도할 자원이 있음을 시사한다.

### 논문과 코드의 동시 공개가 AI 연구 공개 방식의 새로운 표준이 됐다

janpeuker가 arxiv 논문(2606.23050)을 제시하는 것은 흥미로운 패턴을 드러낸다.[^janpeuker]
2026년 6월에 코드 공개와 arxiv 논문이 동시에 나왔다는 것은
AI 연구 공개 방식이 변했음을 보여 준다.

전통적으로 학술 논문은 동료 심사(peer review)를 거쳐 발표되고
코드는 그 이후 또는 그와 함께 공개됐다.
최근 AI 분야에서는 arXiv 사전 공개 + GitHub 동시 릴리스가 표준이 되고 있다.
연구의 속도가 학회 심사 주기를 앞서기 때문이다.
Unlimited-OCR처럼 기업이 연구와 코드를 동시에 공개하는 방식은
학계와 산업계의 경계를 더욱 희미하게 만든다.
그 결과 janpeuker처럼 RAG 시스템에서 인용문 처리나 청킹 최적화에
즉시 적용하는 실험적 사용이 커뮤니티 차원에서 빠르게 진행된다.

---

[^robotswantdata]: <https://news.ycombinator.com/item?id=48643871>
[^novoreorx]: <https://news.ycombinator.com/item?id=48645922>
[^functional_dev]: <https://news.ycombinator.com/item?id=48646906>
[^aliljet]: <https://news.ycombinator.com/item?id=48646125>
[^gettingoverit]: <https://news.ycombinator.com/item?id=48646031>
[^pmarreck]: <https://news.ycombinator.com/item?id=48644370>
[^alansaber]: <https://news.ycombinator.com/item?id=48644493>
[^arboles]: <https://news.ycombinator.com/item?id=48650140>
[^peatmoss]: <https://news.ycombinator.com/item?id=48644574>
[^janpeuker]: <https://news.ycombinator.com/item?id=48645275>
