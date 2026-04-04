# QMD (Query Markup Documents)

> On-device search engine for everything you need to remember.

<https://github.com/tobi/qmd>

Shopify 창업자 Tobi Lütke가 만든 로컬 마크다운 검색 엔진. 클라우드 API 호출 없이
BM25 + 벡터 검색 + LLM 리랭킹을 결합한 하이브리드 검색을 수행한다.

## 설치

```bash
npm install -g @tobilu/qmd
```

Node.js >= 22 또는 Bun >= 1.0.0이 필요하다.

## 3가지 검색 모드

```bash
# BM25 키워드 매칭 (SQLite FTS5)
qmd search "query"

# 벡터 시맨틱 검색
qmd vsearch "query"

# 하이브리드: 위 두 가지 + 쿼리 확장 + LLM 리랭킹
qmd query "query"
```

## 하이브리드 검색 파이프라인

`query` 명령의 동작 순서:

1. **쿼리 확장(Query Expansion)**: 원본 쿼리(×2 가중치) + LLM이 생성한 대안 쿼리
   2개로 검색 범위를 넓힌다.
2. **병렬 검색(Parallel Retrieval)**: BM25와 벡터 검색을 동시에 실행한다.
3. **Reciprocal Rank Fusion (RRF)**: `score = Σ(1/(k+rank+1))` (k=60)으로 두
   검색 결과의 순위를 통합한다. 1위에 +0.05, 2~3위에 +0.02 보너스.
4. **LLM 리랭킹(Re-ranking)**: qwen3-reranker가 상위 30개 결과를 0~10점으로
   재평가한다.
5. **Position-Aware Blending**: 순위에 따라 가중치를 다르게 적용한다.

## Position-Aware Blending

| 순위 | RRF | 리랭커 |
| ---- | --- | ------ |
| 1~3  | 75% | 25%    |
| 4~10 | 60% | 40%    |
| 11+  | 40% | 60%    |

상위 결과는 검색 신뢰도를 우선하고, 하위로 갈수록 리랭커 판단을 신뢰한다.
리랭커가 높은 신뢰도의 검색 결과를 망가뜨리는 것을 방지하는 설계다.

## 로컬 GGUF 모델

node-llama-cpp로 3개의 모델을 로컬 실행한다. `~/.cache/qmd/models/`에 자동
다운로드된다.

| 모델                     | 크기   | 용도        |
| ------------------------ | ------ | ----------- |
| embedding-gemma-300M     | ~300MB | 벡터 임베딩 |
| qwen3-reranker-0.6b      | ~640MB | 리랭킹      |
| qmd-query-expansion-1.7B | ~1.1GB | 쿼리 확장   |

총 ~2GB로 검색에 필요한 모든 AI 기능을 로컬에서 실행한다.

## MCP 서버

Claude Desktop, Claude Code 등과 직접 연동할 수 있다.

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

제공하는 MCP 도구:

- `qmd_search`: BM25 검색
- `qmd_vector_search`: 시맨틱 검색
- `qmd_deep_search`: 하이브리드 검색 + 리랭킹
- `qmd_get`: 파일/docid로 문서 조회
- `qmd_multi_get`: 패턴으로 여러 문서 조회
- `qmd_status`: 인덱스 상태 확인

## 데이터 저장

SQLite 하나(`~/.cache/qmd/index.sqlite`)에 FTS5 인덱스와 sqlite-vec 벡터
인덱스를 모두 담는다. 마크다운을 900토큰 단위(15% 오버랩)로 청킹(chunking)하여
저장한다.

## 활용 방안

### TIL 저장소를 QMD로 검색하기

이 TIL 저장소처럼 마크다운이 쌓인 곳에 바로 적용할 수 있다.

```bash
qmd collection add ~/til --name til
qmd context add qmd://til "개발 관련 TIL 모음"
qmd embed
qmd query "React 상태 관리"
```

700개 넘는 마크다운 파일에서 키워드와 의미를 동시에 검색할 수 있게 된다.

### Claude Code와 MCP 연동

Claude Code 설정에 QMD MCP 서버를 추가하면, Claude가 로컬 문서를 직접 검색하며
답변할 수 있다.

```bash
# Claude Code에서 MCP 서버 추가
claude mcp add qmd -- qmd mcp
```

"이전에 Docker 관련해서 뭐 정리했었지?"처럼 대화하면 Claude가
`qmd_deep_search`로 관련 TIL을 찾아준다.

### RAG 파이프라인 설계 시 참고할 패턴

검색 시스템을 직접 만들 때 QMD의 구조를 레퍼런스로 활용할 수 있다.

**SQLite 하나로 충분하다.** FTS5(키워드) + sqlite-vec(벡터)을 한 DB에 넣으면
별도 벡터DB(Pinecone, Weaviate 등) 없이도 하이브리드 검색이 가능하다.
소규모~중규모 문서에는 이 구조가 운영 부담이 적다.

**BM25를 빼지 마라.** 벡터 검색만으로는 정확한 용어("useState",
"docker-compose")를 놓친다. BM25를 병행하면 키워드 매칭을 보장할 수 있다.
RRF(`score = Σ(1/(k+rank+1))`, k=60)로 두 결과를 통합하는 것이 간단하고
효과적이다.

**리랭커는 보조 수단으로 쓴다.** 소형 리랭커(0.6B)의 판단은 불완전할 수 있다.
QMD의 Position-Aware Blending처럼 상위 결과는 검색 엔진 신뢰도를 보존하고(75%),
하위 결과에서만 리랭커 비중을 높이는(60%) 전략이 실용적이다.

**쿼리 확장으로 어휘 불일치를 해결한다.** "배포 방법"을 검색할 때 LLM이
"deployment process", "CI/CD pipeline" 같은 대안 쿼리를 생성한다. 한국어-영어
혼용 문서에서 특히 효과가 크다.

### 로컬 AI 도구의 설계 기준

QMD는 ~2GB 모델 3개로 검색 파이프라인 전체를 로컬에서 돌린다. 이 접근이 시사하는
것:

**300MB~1.7B급 모델이면 충분한 작업이 있다.** 임베딩(300M), 리랭킹(0.6B), 쿼리
확장(1.7B) 등 단일 목적 작업은 소형 모델로 해결된다. 모든 작업에 거대 모델을 쓸
필요가 없다.

**GGUF + node-llama-cpp 조합이 실용적이다.** Node.js 환경에서 로컬 모델을 돌려야
한다면 이 조합을 참고할 수 있다. Python의 llama-cpp-python과 같은 역할이다.

**캐싱이 핵심이다.** QMD는 쿼리 확장과 리랭킹 결과를 `llm_cache` 테이블에
저장한다. 같은 쿼리를 반복하면 모델 추론을 건너뛴다. 로컬 LLM의 느린 속도를
캐싱으로 보완하는 패턴이다.
