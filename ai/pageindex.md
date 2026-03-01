# PageIndex

- 원문: <https://github.com/VectifyAI/PageIndex>
- 사이트: <https://pageindex.ai/>

## 요약

벡터 DB 없이 동작하는 추론 기반 RAG(Retrieval-Augmented
Generation) 시스템이다.

문서를 목차(Table of Contents) 형태의 계층적 트리
인덱스로 변환한 뒤, LLM이 트리를 탐색하며 관련
섹션을 찾는다.

핵심 주장은 "유사도(similarity) ≠ 관련성(relevance)"
이다. 벡터 검색이 임베딩 유사도에 의존하는 반면,
PageIndex는 LLM의 추론 능력으로 문서 구조를 논리적
으로 탐색한다.

FinanceBench에서 98.7% 정확도를 달성했다.

## 아키텍처

```
PDF/Markdown
    ↓
TOC 감지 (LLM이 각 페이지를 분류)
    ↓
┌───────────────────────────────────┐
│  Mode 1: TOC + 페이지 번호 존재  │
│  Mode 2: TOC 존재, 번호 없음     │
│  Mode 3: TOC 없음 → 직접 생성    │
└───────────────────────────────────┘
    ↓
계층적 트리 구조 (JSON)
    ↓
LLM 트리 탐색 → 관련 섹션 반환
```

두 단계로 나뉜다.

1. **인덱스 생성**: 문서를 트리 구조로 변환한다.
2. **트리 탐색**: LLM이 트리를 순회하며 질문에 맞는
   섹션을 찾는다.

## 코드 분석

### 프로젝트 구조

```
pageindex/
├── page_index.py     # 핵심 로직 (48KB)
├── page_index_md.py  # 마크다운 처리
├── utils.py          # PDF, API, 토큰 유틸리티
├── config.yaml       # 기본 설정
└── __init__.py
```

의존성은 6개뿐이다:

| 패키지       | 역할                  |
|--------------|-----------------------|
| `openai`     | LLM API 호출         |
| `pymupdf`    | PDF 텍스트 추출      |
| `PyPDF2`     | PDF 대체 파서        |
| `tiktoken`   | 토큰 수 계산         |
| `python-dotenv` | 환경 변수 로드     |
| `pyyaml`     | 설정 파일 파싱       |

### 인덱스 생성 파이프라인 (`page_index.py`)

진입점은 `page_index()` → `page_index_main()`
→ `tree_parser()`다.

`tree_parser()`가 전체 흐름을 조율한다:

```
check_toc()           # TOC 존재 여부 판단
    ↓
meta_processor()      # 3가지 모드 중 하나로 분기
    ↓
verify_toc()          # 추출된 섹션을 LLM으로 검증
    ↓
post_processing()     # 플랫 리스트 → 트리 계층 구축
    ↓
process_large_node_recursively()  # 큰 노드 재분할
```

#### TOC 감지

`toc_detector_single_page()`가 각 페이지를 LLM에
보내 TOC인지 분류한다.
`find_toc_pages()`가 연속된 TOC 페이지를 묶는다.

#### 3가지 처리 모드

**Mode 1** (TOC + 페이지 번호):
TOC에서 섹션과 페이지 번호를 추출하고,
물리적 인덱스와의 오프셋을 계산한다.

**Mode 2** (TOC, 번호 없음):
TOC 구조를 파싱한 뒤, 문서를 토큰 기준으로
그룹화해서 각 섹션의 위치를 매칭한다.

**Mode 3** (TOC 없음):
`generate_toc_init()`으로 첫 페이지 그룹에서
초기 구조를 추출하고, `generate_toc_continue()`로
나머지를 점진적으로 확장한다.

#### 검증 파이프라인

`verify_toc()`가 추출된 섹션을 샘플링해서 실제
페이지 내용과 대조한다. 틀린 항목이 있으면
`fix_incorrect_toc_with_retries()`가 최대 3회
재시도하며 보정한다.

#### 큰 노드 재분할

`process_large_node_recursively()`는 설정된
한계(`max_pages_per_node`: 10,
`max_tokens_per_node`: 20000)를 초과하는 노드에
Mode 3을 재귀적으로 적용해 하위 구조를 만든다.
`asyncio.gather()`로 자식 노드들을 병렬 처리한다.

### 마크다운 처리 (`page_index_md.py`)

마크다운은 PDF보다 단순한 경로를 탄다:

```
extract_nodes_from_markdown()    # 헤더 추출
    ↓  정규식: ^(#{1,6})\s+(.+)$
extract_node_text_content()      # 헤더 간 텍스트 연결
    ↓
tree_thinning_for_index()        # 작은 노드 병합
    ↓
build_tree_from_nodes()          # 스택 기반 트리 구축
    ↓
generate_summaries_for_structure_md()  # 비동기 요약
```

코드 블록(```` ``` ````) 내부의 `#`은 헤더로
인식하지 않는다.
`tree_thinning_for_index()`는 토큰 수가 최소
임곗값 미만인 노드를 부모에 병합한다.

### 유틸리티 (`utils.py`)

`ChatGPT_API()`는 온도 0으로 고정하고 최대 10회
재시도한다. 비동기 변형 `ChatGPT_API_async()`도
있다.

`list_to_tree()`가 점 표기법(1, 1.1, 1.2, 2 등)
기반으로 플랫 리스트를 트리로 변환한다.

### 트리 출력 구조

```json
{
  "title": "Financial Stability",
  "node_id": "0006",
  "start_index": 21,
  "end_index": 22,
  "summary": "The Federal Reserve...",
  "nodes": [
    {
      "title": "Monitoring Financial Vulnerabilities",
      "node_id": "0007",
      "start_index": 22,
      "end_index": 28,
      "nodes": []
    }
  ]
}
```

각 노드는 제목, 고유 ID, 페이지 범위, 요약,
자식 노드를 포함한다.

## 사용

```bash
pip3 install --upgrade -r requirements.txt

# .env 파일에 API 키 설정
# CHATGPT_API_KEY=your_key

# PDF 인덱스 생성
python3 run_pageindex.py --pdf_path doc.pdf

# 마크다운 인덱스 생성
python3 run_pageindex.py --md_path doc.md
```

클라우드 서비스, MCP 통합, REST API(베타)도
제공한다.

## 인사이트

### 1) "유사도 ≠ 관련성"은 벡터 RAG의 구조적 한계를 짚는다

벡터 검색은 질문과 의미적으로 가까운 청크를
반환한다. 하지만 전문 문서에서 "관련 있는" 정보는
종종 표면적으로 유사하지 않다.

재무 보고서에서 "리스크 요인"을 찾으려면,
벡터 유사도가 아니라 문서 구조에 대한 이해가
필요하다. PageIndex가 LLM의 추론으로 이 간극을
메우는 접근은 설득력 있다.

### 2) 목차는 저자가 만든 최고의 인덱스다

벡터 RAG는 문서를 임의 크기로 잘라서(chunking)
원래 구조를 파괴한다. PageIndex는 정반대로,
저자가 의도한 문서 구조를 보존하고 활용한다.

TOC가 있으면 그대로 쓰고, 없으면 LLM이
생성한다는 3가지 모드 분기가 이 철학의 구현이다.
문서의 자연스러운 단위를 존중하는 것이
검색 품질의 출발점이라는 관점이다.

### 3) LLM을 인덱싱과 검색 양쪽에 쓰는 비용 구조

인덱스 생성에 LLM을 쓰고(TOC 감지, 구조 추출,
요약, 검증), 검색에도 LLM을 쓴다(트리 탐색).
벡터 DB 인프라 비용은 없지만, API 호출 비용이
두 단계 모두에서 발생한다.

이것이 성립하는 조건은 명확하다.
한 번 인덱싱하고 여러 번 검색하는 문서,
검색 정확도가 비용보다 중요한 도메인(금융, 법률,
규제)에서 ROI가 나온다.

범용 웹 검색과는 다른 포지셔닝이다.

### 4) 검증 파이프라인이 자기 교정 시스템이다

`verify_toc()` → `fix_incorrect_toc_with_retries()`
흐름은 LLM의 오류를 LLM으로 검증하고
교정하는 자기 참조 루프다.

이웃한 정확한 항목으로 탐색 범위를 좁혀서
재시도하는 전략이 인상적이다.
LLM 출력을 맹신하지 않고, 샘플링과 재시도로
신뢰도를 끌어올리는 패턴은 다른 LLM 파이프라인에도
적용할 수 있다.

### 5) 48KB 단일 파일의 복잡도가 한계를 드러낸다

`page_index.py` 하나에 TOC 감지, 3가지 모드 분기,
검증, 후처리, 재귀 분할이 모두 들어 있다.
파이프라인 자체는 정교하지만, 단일 파일의
크기와 복잡도는 유지보수와 확장의 병목이 될 수 있다.

모드별 분리, 검증 로직 추출 등 구조적 리팩터링의
여지가 있다. 오픈소스 프로젝트로서 기여 장벽을
낮추려면 이 부분이 중요해질 것이다.
