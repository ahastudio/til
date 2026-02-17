# QMD (Query Markup Documents)

> On-device search engine for everything you need to remember.

<https://github.com/tobi/qmd>

Shopify 창업자 Tobi Lütke가 만든
로컬 마크다운 검색 엔진.
클라우드 API 호출 없이 BM25 + 벡터 검색 + LLM 리랭킹을
결합한 하이브리드 검색을 수행한다.

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

1. **쿼리 확장(Query Expansion)**:
   원본 쿼리(×2 가중치) + LLM이 생성한
   대안 쿼리 2개로 검색 범위를 넓힌다.
2. **병렬 검색(Parallel Retrieval)**:
   BM25와 벡터 검색을 동시에 실행한다.
3. **Reciprocal Rank Fusion (RRF)**:
   `score = Σ(1/(k+rank+1))` (k=60)으로
   두 검색 결과의 순위를 통합한다.
   1위에 +0.05, 2~3위에 +0.02 보너스.
4. **LLM 리랭킹(Re-ranking)**:
   qwen3-reranker가 상위 30개 결과를
   0~10점으로 재평가한다.
5. **Position-Aware Blending**:
   순위에 따라 가중치를 다르게 적용한다.

## Position-Aware Blending

| 순위  | RRF  | 리랭커 |
|-------|------|--------|
| 1~3   | 75%  | 25%    |
| 4~10  | 60%  | 40%    |
| 11+   | 40%  | 60%    |

상위 결과는 검색 신뢰도를 우선하고,
하위로 갈수록 리랭커 판단을 신뢰한다.
리랭커가 높은 신뢰도의 검색 결과를
망가뜨리는 것을 방지하는 설계다.

## 로컬 GGUF 모델

node-llama-cpp로 3개의 모델을 로컬 실행한다.
`~/.cache/qmd/models/`에 자동 다운로드된다.

| 모델                          | 크기   | 용도         |
|-------------------------------|--------|--------------|
| embedding-gemma-300M          | ~300MB | 벡터 임베딩  |
| qwen3-reranker-0.6b           | ~640MB | 리랭킹       |
| qmd-query-expansion-1.7B      | ~1.1GB | 쿼리 확장    |

총 ~2GB로 검색에 필요한 모든 AI 기능을
로컬에서 실행한다.

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

SQLite 하나(`~/.cache/qmd/index.sqlite`)에
FTS5 인덱스와 sqlite-vec 벡터 인덱스를 모두 담는다.
마크다운을 900토큰 단위(15% 오버랩)로
청킹(chunking)하여 저장한다.

## 인사이트

### RAG의 로컬 구현체

클라우드 기반 RAG 파이프라인
(임베딩 → 벡터DB → 리트리벌 → 리랭킹)을
CLI 도구 하나로 로컬에 옮겨놓은 셈이다.
SQLite 하나로 FTS5 + sqlite-vec을 모두 처리한다.

### BM25 + 벡터의 상호보완

키워드 검색(BM25)은 정확한 용어 매칭에 강하고,
벡터 검색은 의미적 유사성에 강하다.
둘을 RRF로 결합하면 단독 사용보다
검색 품질이 올라간다.

### 에이전틱 워크플로우 지향

MCP 서버를 내장하여 AI 에이전트가
마크다운 지식 베이스를 검색할 수 있게 했다.
`--files`, `--json` 등 기계 친화적 출력 포맷과
docid 시스템이 이를 뒷받침한다.

### 쿼리 확장의 효과

사용자가 "배포 방법"을 검색하면
LLM이 "deployment process",
"CI/CD pipeline" 같은 대안 쿼리를 생성한다.
어휘 불일치(vocabulary mismatch) 문제를
자연스럽게 해결한다.

### Position-Aware Blending의 의미

리랭커를 전면 신뢰하지 않는 설계가 흥미롭다.
소형 모델(0.6B)의 판단이 불완전할 수 있으므로,
검색 엔진이 확신하는 상위 결과는 보존하면서
하위 결과에서만 리랭커의 재배치를 허용한다.
