# LiteParse - 빠르고 가벼운 로컬 OSS 문서 파서

<https://developers.llamaindex.ai/liteparse/>

GitHub: <https://github.com/run-llama/liteparse>

## 소개

LiteParse는 LlamaIndex 팀(run-llama)이 공개한 OSS PDF·문서 파서로,
“빠르고 가볍게” 로컬에서 동작하는 것에 집중한다. 클라우드 호출 없이
PDFium 기반의 공간 텍스트 추출, Tesseract 기본 OCR, 페이지 스크린샷
생성을 한 패키지로 묶었다. 라이선스는 Apache 2.0이며, Rust 코어 위에
Node.js, Python, WASM, CLI 바인딩을 동일 코드베이스에서 제공한다.

LlamaIndex의 클라우드 제품 LlamaParse가 “복잡한 문서(밀집 표, 다단
레이아웃, 차트, 손글씨, 스캔 PDF)”를 처리한다면, LiteParse는 그 아래
계층 — “보통 문서를 로컬에서 빠르게” — 를 채운다. 즉 두 제품은 한
플랫폼에 묶인 분업 구조다.

## 명세

### 입력·코어·출력 파이프라인

README의 mermaid 그림은 다음 흐름을 보여준다. 입력은 PDF, DOCX, XLSX,
PPTX, 이미지 다섯 가지 카테고리. PDF가 아닌 입력은 LibreOffice 또는
ImageMagick으로 PDF/이미지로 변환된 뒤 코어로 들어간다. Rust 코어는
PDFium으로 텍스트 추출 → 선택적 OCR(Tesseract 기본, HTTP 서버 옵션)
→ 네이티브 텍스트와 OCR 결과 머지 → 격자 투영(Grid Projection)으로
공간 레이아웃을 재구성한다. 출력은 JSON(텍스트 + bounding box), 평문
텍스트(레이아웃 보존), PNG 스크린샷.

### 바인딩

코어 Rust 워크스페이스에 `liteparse`, `liteparse-napi`, `liteparse-python`,
`liteparse-wasm`, `pdfium`, `pdfium-sys`가 있고, packages 디렉토리에는
npm·PyPI·WASM 배포 래퍼가 있다. 모든 패키지(WASM 제외)는 동일한 `lit`
CLI를 동봉한다.

### CLI

세 가지 명령으로 구성된다. `lit parse` — 단일 파일 파싱, `lit batch-parse`
— 디렉토리 일괄 처리, `lit screenshot` — 페이지 스크린샷. 주요 옵션은
`--target-pages` 범위 지정, `--no-ocr`, `--ocr-language`, `--ocr-server-url`,
`--dpi`, `--num-workers`, `--password`. `lit batch-parse` 는 `--recursive`,
`--extension`을 더 받는다.

### OCR 모델

기본 Tesseract가 라이브러리에 번들되어 추가 설치가 필요 없다. 오프라인
환경에서는 `TESSDATA_PREFIX` 또는 `--tessdata-path`로 모델 디렉토리를
지정한다. 더 높은 정확도가 필요하면 HTTP OCR 서버 — EasyOCR, PaddleOCR,
사용자 구현체 — 를 `--ocr-server-url`로 붙인다. API 스펙은 매우 단순한
POST `/ocr` 엔드포인트로, `file`과 `language`를 받고 `{ results: [{ text,
bbox: [x1,y1,x2,y2], confidence }] }`를 돌려준다.

### Agent Skill 통합

`npx skills add run-llama/llamaparse-agent-skills --skill liteparse`로
에이전트 스킬로 설치할 수 있다. 즉 LiteParse는 라이브러리·CLI·에이전트
스킬 세 가지 인터페이스를 모두 제공한다.

## 분석

### Rust 코어 + 다언어 바인딩이라는 2025년대 표준 아키텍처

LiteParse의 형태 — Rust 코어 + napi-rs/PyO3/wasm-bindgen 바인딩 — 는
[[bijou64]], Polars, Ruff, Biome, Turbopack과 같은 가족이다. 한 번
Rust로 구현하고, JS·Python·브라우저에서 동일 성능을 노출한다. 이 패턴이
표준이 되는 이유는 명확하다. 첫째, Rust는 PDF·OCR 같은 시스템 영역의
성능을 보장한다. 둘째, napi-rs/PyO3/wasm-bindgen이 충분히 성숙해 바인딩
비용이 낮다. 셋째, 하나의 코드베이스가 세 생태계를 동시에 잡는다.

### LlamaParse 클라우드 + LiteParse 로컬의 2단 제품 구조

LlamaIndex는 명시적으로 “쉬운 건 로컬에서, 어려운 건 클라우드로”의
2단 구조를 만든다. 이는 GitHub의 “쉬운 코드 검색은 grep, 어려운 의미
검색은 Copilot Workspace”, MongoDB의 “Community Edition + Atlas”와 같은
프리미엄 OSS 패턴이다. OSS는 진입과 통합 비용을 낮추고, 클라우드는
어려운 케이스의 마진을 가져간다. LiteParse는 단순한 “좋은 일” 이상의
시장 전략이다 — LlamaIndex 생태계에 사용자를 묶어두는 입구다.

### LLM 에이전트를 위한 “스크린샷 + 텍스트” 이중 표현

LiteParse가 별도로 스크린샷 생성을 1급 기능으로 노출한 것은 의미가
크다. LLM 에이전트는 텍스트만으로 표·차트·서식을 충분히 이해하지 못하고,
멀티모달 입력(텍스트 + 페이지 이미지)이 1차 적응이다. 즉 LiteParse는
“텍스트 추출 도구”가 아니라 “LLM이 문서를 이해할 수 있게 준비하는
도구”로 자기를 위치 짓는다. 출력 포맷이 JSON(+ bounding box) + 평문 +
스크린샷 세 가지인 이유다.

### Grid Projection이라는 공간 레이아웃 복원

코어 마지막 단계인 “Grid Projection — Spatial layout reconstruction”은
PDF 파싱의 가장 어려운 영역이다. PDF는 “페이지 위 위치에 텍스트 조각을
배치한 것”이지 “단락·문장·열의 구조화된 표현”이 아니다. 따라서 단순
텍스트 추출은 다단 레이아웃, 표, 본문/캡션을 섞어버린다. Grid Projection은
공간 좌표를 격자로 재투영해 “원래의 읽기 순서”를 추정한다. 이는
pdfplumber, PyMuPDF의 “bbox 기반 라인 클러스터링”과 같은 가족 기법이다.

## 비평

### 강점 - 다언어·다플랫폼 동시 노출

같은 코어가 cargo, npm, pip, WASM 네 채널로 동시에 배포된다는 점은
LiteParse를 “팀별 도구”가 아니라 “플랫폼”으로 격상시킨다. 어느 회사의
파이프라인이 Python으로 시작했다가 Node.js 서비스에 통합되거나, 브라우저
WASM으로 클라이언트 측 미리보기가 필요해도 동일 라이브러리를 쓸 수 있다.
이는 [[perry]] 같은 “네이티브 컴파일” 시도와 다른 의미의 통합 — 라이브러리
수준의 다언어 통합 — 의 표본이다.

### 약점 - “fast and light” 약속의 정량 부재

README는 “빠르고 가볍다”를 강조하지만 정량 벤치마크가 없다. pdfplumber,
unstructured, PyMuPDF, pypdfium2 같은 비교 대상에 대한 처리량·메모리·
정확도 표가 빠진다. 사용자가 선택하려면 “어떤 워크로드에서 얼마나
유리한가”의 데이터가 필요하다. 1.0 릴리스급 OSS라면 이 자료가 README의
한 자리를 차지해야 한다.

### 약점 - LlamaParse로의 회유 신호의 강도

README의 두 번째 단락이 “복잡한 문서는 LlamaParse를 쓰세요”라는 권유로
시작하는 것은 정직하지만, 사용자가 LiteParse의 한계를 평가하기 전에
이미 LlamaParse를 한 번 보게 만든다. 마케팅 관점에서는 합리적이지만,
OSS 사용자의 첫 인상에서 “이 도구의 한계가 어디인지”의 정의가 클라우드
제품 광고로 묶여 있다는 점은 미묘한 거부감을 만들 수 있다.

### 약점 - LibreOffice·ImageMagick 외부 의존

DOCX·PPTX·XLSX·이미지를 “자동 변환”한다는 약속이 LibreOffice와 ImageMagick
설치를 전제로 한다. 이는 컨테이너 환경에서 이미지 크기 부담, 라이선스
관점(LibreOffice는 MPL, ImageMagick은 ImageMagick License), 보안 표면
(LibreOffice 매크로, ImageMagick RCE 이력)을 늘린다. README는 설치
명령은 주지만 이 운영 비용은 다루지 않는다.

### 약점 - Grid Projection 정확도의 외부 검증

공간 레이아웃 복원은 PDF 파싱의 가장 어려운 단계인데, README는 “Grid
Projection”이라는 이름만 노출하고 어떤 알고리즘인지·어디서 잘 안 되는지를
다루지 않는다. 다단 레이아웃, 표 안의 표, 회전 텍스트, 세로 쓰기(일본어,
한국어 일부)에서의 동작이 별도로 다뤄져야 채택 의사 결정이 가능하다.

## 인사이트

### LLM 시대의 “OSS 로컬 도구”는 클라우드 SaaS의 입구로 설계된다

LiteParse가 LlamaParse를 함께 노출하는 형태는 LLM 시대의 OSS 비즈니스
모델 패턴을 가장 명확히 보여준다. 과거 OSS는 “지원 계약”, “호스팅
SaaS”, “엔터프라이즈 기능”의 세 가지 머네타이즈 경로를 가졌다. LLM
영역의 새 패턴은 “쉬운 케이스는 OSS 로컬 도구로, 어려운 케이스는 SaaS
모델 호출로”의 2단 구조다. LangChain + LangSmith, LlamaIndex + LlamaCloud,
Hugging Face transformers + Inference Endpoints가 모두 같은 형태다.

이 패턴이 작동하는 이유는 LLM 가치 사슬의 “쉬움/어려움”이 자연스럽게
분리되기 때문이다. 90%의 문서는 PDFium + Tesseract로 처리 가능하고,
10%(스캔 PDF, 손글씨, 복잡 표)는 비전 모델이 필요하다. 90%를 로컬에서
무료로 잘 처리하면 개발자가 파이프라인을 LiteParse 위에 구축하고,
10%가 발생하는 순간 같은 회사의 SaaS API를 호출하는 비용이 가장 낮은
선택이 된다. 즉 “쉬운 영역의 OSS 점유”가 “어려운 영역의 SaaS 매출”을
부른다.

여기서 도출되는 함의는 OSS와 클라우드의 경쟁 구조가 바뀐다는 점이다.
과거에는 OSS와 SaaS가 경쟁자였다. 지금은 같은 회사가 둘을 동시에 운영
하면서 OSS를 “마케팅 채널”로, SaaS를 “수익 채널”로 분리한다. 이 패턴이
일반화되면 “순수한 독립 OSS 메인테이너”의 시장이 점점 좁아진다. OSS
프로젝트가 회사 후원 + SaaS 백엔드의 조합 없이는 지속 가능하지 않은
구조가 강화된다.

세 번째 함의는 사용자가 OSS 선택 시 “이 프로젝트 뒤의 클라우드 제품은
무엇인가”를 함께 봐야 한다는 점이다. LiteParse 사용은 LlamaIndex 생태계
선택과 사실상 같은 결정이다. 같은 사용자는 LangChain의 unstructured,
Hugging Face의 datasets, Cohere의 embed 등 경쟁 생태계의 입구를 동시에
평가해야 한다. OSS 선택이 점점 “스택 선택”의 의미로 무거워진다.

### 문서 파싱은 LLM 시대의 “토크나이저 다음 단계”다

LLM 학습·추론 파이프라인의 1차 단계는 토크나이저다. 텍스트를 토큰으로
바꾸지 않으면 어떤 모델도 동작하지 않는다. 추론·RAG 파이프라인의 1차
단계는 문서 파싱이다. PDF·DOCX·이미지를 텍스트로 바꾸지 않으면 어떤
RAG도 동작하지 않는다. 즉 LiteParse는 “토크나이저의 거시 버전”이다.

이 위상은 산업적으로 매우 중요한 자리다. 토크나이저는 모델 학습의
첫 단계이지만 모델 품질에 거의 가시적이지 않다. BPE, SentencePiece,
WordPiece의 선택이 모델 성능 차이를 일으키지만 학술 논문에서는 부록
한 단락이다. 그러나 산업 현장에서는 “잘못된 토크나이저 = 잘못된 학습
1년”의 비용이다. 문서 파싱도 같다. RAG 시스템의 정확도 차이의 1차
원인은 종종 임베딩 모델이 아니라 문서 파싱 단계의 “표가 텍스트로 평탄화
되었다” 같은 사소한 결정에서 온다.

여기서 도출되는 함의는 “문서 파싱 품질이 LLM 애플리케이션의 1차 결정
변수”라는 사실이다. 같은 GPT-5, 같은 임베딩, 같은 벡터 DB를 쓰는 두
RAG 시스템의 정답률이 갈리는 이유는 거의 항상 문서 파싱 단계의 차이다.
이 단계를 외부화한 OSS·SaaS 시장(LiteParse, LlamaParse, Unstructured,
Reducto, Docling)이 빠르게 자라는 이유다.

세 번째 함의는 평가의 어려움이다. 토크나이저 품질을 정량 측정하는
표준 벤치마크가 부족했듯, 문서 파싱 품질의 표준 벤치마크도 부족하다.
“이 PDF에서 표를 얼마나 정확히 추출했는가”는 표가 어떻게 정의되는가에
따라 답이 다르다. LiteParse가 정량 벤치마크를 README에 넣지 못한 이유도
이 측정의 어려움 때문일 수 있다. 누군가 이 측정 표준을 정의하면 그 자리가
새 “MLPerf for RAG” 같은 산업 인프라가 된다.

### Rust 코어 + 다언어 바인딩은 새 OSS 라이브러리의 사실상 표준이 된다

LiteParse가 Rust 코어 + napi-rs/PyO3/wasm-bindgen 바인딩을 채택한 것은
2025년 시점 OSS 라이브러리 설계의 사실상 표준이 된 패턴이다. Polars,
Ruff, Biome, Turbopack, RsPack, swc, mise, uv, pyrefly 등 광범위한
프로젝트가 같은 형태를 따른다. 이는 “언어별로 따로 구현”의 시대가
저물고 있음을 의미한다.

이 변화의 동력은 세 가지다. 첫째, Rust의 성능이 C++ 수준이면서 메모리
안전성을 보장한다. PDF·이미지·네트워크처럼 신뢰할 수 없는 입력을 다루는
영역에서 메모리 안전성은 보안 부채를 줄인다. 둘째, FFI 바인딩 도구가
충분히 성숙했다. napi-rs 1.0, PyO3 0.20대, wasm-bindgen은 “Rust 함수를
다른 언어에서 부르기”의 비용을 크게 낮췄다. 셋째, 패키지 매니저 — npm,
PyPI, crates.io — 가 네이티브 바이너리 배포의 안정적 채널이 되었다.

여기서 도출되는 첫 번째 함의는 “언어 생태계 경쟁”의 의미가 바뀐다는
점이다. 과거에는 Python에 좋은 라이브러리가 있고 JavaScript에는 없다는
식의 비대칭이 흔했다. Rust 코어 + 다언어 바인딩이 표준이 되면, 모든
좋은 라이브러리가 모든 주요 언어에 동시에 등장한다. 언어 간 “라이브러리
풍요도” 격차가 닫힌다. 언어 선택의 1차 변수는 라이브러리가 아니라
런타임 특성, 문법 친화성, 팀 숙련도가 된다.

두 번째 함의는 “순수 Python OSS”의 시장이 좁아진다는 점이다. pdfplumber,
unstructured 같은 순수 Python 도구는 LiteParse 같은 Rust 코어와의 성능
격차를 메우기 어렵다. 같은 인터페이스에 같은 기능을 더 빠르게 제공하는
경쟁자가 등장하면 마이그레이션이 일어난다. 이는 [[bijou64]]에서 본
“하드웨어 친화 설계가 새 표준이 된다”의 라이브러리 버전이다.

세 번째 함의는 Rust 자체의 위상 변화다. Rust는 “시스템 프로그래밍 언어”
로 시작했지만 2026년 시점에는 “OSS 라이브러리 코어의 사실상 공용어”가
되어 가고 있다. 이는 1990년대 C가 그랬던 위치, 2000년대 C++가 그랬던
위치를 점점 차지한다. 새 OSS 라이브러리를 만들 때 “어떤 언어로 코어를
쓸까”의 디폴트가 Rust로 굳어진다. 이는 Rust 학습 곡선의 가치를 더 키운다.

### 에이전트 스킬화가 “라이브러리 + CLI”의 다음 단계 인터페이스가 된다

LiteParse가 별도로 “Agent Skill”로 자기를 노출하는 점은 인터페이스
설계의 새 흐름을 보여준다. 라이브러리(API), CLI(명령행)에 이어 “에이전트
스킬” — `SKILL.md` 형식으로 정의되어 AI 에이전트가 자동 발견·사용할
수 있는 인터페이스 — 가 1급 시민이 된다. [[dont-build-agents-build-skills-instead]],
[[agent-skills-for-context-engineering]]에서 본 흐름의 산업 적용이다.

이 흐름이 의미하는 바는 “라이브러리의 1차 사용자가 인간에서 AI 에이전트로
이동한다”는 시나리오다. 라이브러리 문서가 사람에게 잘 읽히는 것보다
AI 에이전트가 자동으로 호출하기 쉬운 형태가 우선시된다. `SKILL.md`는
이 변화의 표준이 되어 가는 형식이다. 함수 시그니처, 입출력 예시, 흔한
실수 패턴, 디버깅 팁이 한 파일에 정합되어 있다.

여기서 도출되는 함의는 OSS 라이브러리 설계의 “문서” 우선순위가 변한다는
점이다. README, API 문서, 튜토리얼, 그리고 새로 `SKILL.md`. AI 에이전트가
주요 사용자가 되면 “인간이 보는 시각적 미려함”보다 “에이전트가 파싱하기
쉬운 구조”가 더 가치 있다. 이는 [[claude-api]] 스킬, [[run]] 스킬,
[[verify]] 스킬처럼 Claude Code 같은 에이전트 환경에서 이미 일상이 된
관행이 일반 OSS로 확산되는 신호다.

두 번째 함의는 OSS 디렉터리·검색의 변화다. npm/PyPI/crates.io가 인간
검색에 최적화되어 있다면, 다음 세대 라이브러리 디렉터리는 “AI 에이전트가
자동 발견하기 좋은” 메타데이터 — SKILL.md 노출, 입출력 스키마, 실패
패턴 — 을 1급으로 다룬다. `npx skills add` 같은 명령은 이 새 인프라의
초기 형태다.

세 번째 함의는 라이브러리 메인테이너의 새 책임이다. 사람만 쓰던 시절에는
“좋은 예제 + 친절한 에러 메시지”가 충분했다. AI 에이전트가 주요 사용자가
되면 “이 라이브러리를 잘못 쓰는 흔한 패턴”을 명시적으로 문서화하는
것이 1급 책임이 된다. 에이전트는 자기 학습 데이터에 없는 함정에 빠질
가능성이 높고, 그 함정을 미리 적어주는 라이브러리가 채택률에서 앞선다.
SKILL.md는 이 책임을 구조화한 형식이다.
