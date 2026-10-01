# LatticeDB: 그래프, 벡터, 전문 검색을 파일 하나에 담은 임베디드 DB

<https://github.com/jeffhajewski/latticedb>

HN 토론: <https://news.ycombinator.com/item?id=49437049> (190점, 54개 댓글)

GN 토론: <https://news.hada.io/topic?id=34517>

## 소개

LatticeDB는 로컬 애플리케이션이 같은 데이터를 관계, 의미, 텍스트로 함께 질의하게 해 주는 임베디드 프로퍼티 그래프 데이터베이스다.
데이터베이스 전체가 파일 하나이고, 서버도 설정도 없다.
그래프 탐색, HNSW 벡터 유사도 검색, BM25 전문 검색을 한 엔진과 한 질의 언어(Cypher)에서 쓴다.
Zig로 작성했고 외부 의존성이 없으며, MIT 라이선스다.
저장소는 2025년 12월 20일에 만들어졌고, 2026년 9월 말 기준 GitHub 별 711개, 포크 31개다.

만든 사람은 Jeff Hajewski(HN 계정 smiths1999)다.
그는 2026년 8월 25일 Show HN에 올리며, 회사에서 그래프 DB를 점점 많이 쓰는데 로컬에서 다루기가 고통스러워 더 나은 것을 만들어 보기로 했다고 적었다.
README는 Graph RAG, 에이전트 메모리, 로컬 지식 도구를 엔진의 정의가 아니라 이 기본 요소 위에 만든 예시라고 설명한다.

README가 내세우는 요점은 다섯 가지다.

| 항목             | 내용                                                                     |
| ---------------- | ------------------------------------------------------------------------ |
| 파일 하나        | 데이터베이스 전체가 옮길 수 있는 단일 파일                               |
| 질의 계층 하나   | 그래프 탐색, HNSW 벡터, BM25 전문 검색을 같은 질의 언어로                |
| 이벤트 로그 하나 | 이름 있는 스트림과 그래프 변경 피드가 그래프 쓰기와 같은 WAL 경로를 공유 |
| 로컬 우선        | 한 기기의 한 소유 프로세스, WAL 기반 내구성                              |
| 빠름             | 노드 조회 0.13μs, 100만 벡터에서 재현율 100%로 0.83ms                    |

## 아키텍처

### 한 질의에서 세 가지 검색을 섞는다

Cypher에 두 연산자를 더했다.
`<=>`는 벡터 거리, `@@`는 전문 검색 매칭이다.
README의 첫 예제는 질의 벡터와 가까운 청크를 찾고, 그 청크가 속한 문서가 특정 단어를 포함하는지 확인한 뒤, 문서의 저자까지 따라간다.

```cypher
MATCH (chunk:Chunk)-[:PART_OF]->(doc:Document)-[:AUTHORED_BY]->(author:Person)
WHERE chunk.embedding <=> $query_vector < 0.3
  AND doc.content @@ "neural networks"
RETURN doc.title, chunk.text, author.name
ORDER BY chunk.embedding <=> $query_vector
LIMIT 10
```

지원하는 Cypher는 `MATCH`, `WHERE`, `RETURN`, `CREATE`, `DELETE`, `SET`, `REMOVE`, `MERGE`, `WITH`, `UNWIND`, 집계 함수, 가변 길이 경로다.
`OPTIONAL MATCH`와 `CALL` 프로시저는 아직 없다고 README가 밝힌다.

### 저장과 동시성

저장은 단일 파일과 WAL(write-ahead log)이고, ACID 트랜잭션과 충돌 복구를 지원한다.
모델은 단일 작성자, 다중 독자다.
한 프로세스가 파일을 열어 소유한다.

운영 기능으로는 디렉터리로 변경을 계속 내보내 특정 시점으로 복구하는 연속 백업, DB를 닫지 않고 뜨는 `lattice backup` 핫 백업, 바이트로 직렬화해 객체 저장소에 작은 DB를 여러 개 두는 방식, `:memory:` 인메모리 DB, 소비자 오프셋을 가진 내구성 스트림, `lattice compact`가 있다.
C API가 중심이고 Python, TypeScript, Go, Java 바인딩이 그 위를 감싼다.

### README가 공개한 성능

Apple M1 단일 스레드 기준이다.

| 작업                        | 지연   | 처리량        |
| --------------------------- | ------ | ------------- |
| 노드 조회                   | 0.13μs | 초당 790만    |
| 노드 생성                   | 0.65μs | 초당 150만    |
| 간선 탐색                   | 9μs    | 초당 11만 1천 |
| 전문 검색(문서 100개)       | 19μs   | 초당 5만 3천  |
| 10-NN 벡터 검색(100만 벡터) | 0.83ms | 초당 1,200    |

HNSW는 128차원 코사인 벡터, M=16, ef_construction=200, ef_search=64로 쟀고, 100만 벡터에서 메모리는 1,040MB다.
ef_search를 16으로 낮추면 506μs에 재현율 57%, 32면 1.9ms에 79%다.

README는 SQLite의 재귀 CTE와 같은 기기에서 비교해, 10만 노드 50만 간선 그래프의 1-hop 탐색이 8.0μs 대 290.0μs로 36배, 가변 경로(1..5)가 75배 빠르다고 적는다.
Kuzu와 Neo4j 수치는 다른 사람의 글에서 가져온 것이라 규모 감을 잡는 용도로만 보라고 스스로 단서를 단다.

## 사용법

```bash
# CLI
curl -fsSL https://raw.githubusercontent.com/jeffhajewski/latticedb/main/dist/install.sh | bash

# 바인딩
pip install latticedb
npm install @hajewski/latticedb
```

```python
from latticedb import Database
from latticedb.embedding import hash_embed

with Database("knowledge.db", create=True, enable_vectors=True, vector_dimensions=128) as db:
    db.create_node_fts_index("Chunk", "text")

    with db.write() as txn:
        doc = txn.create_node(labels=["Document"], properties={"title": "Attention Is All You Need"})
        chunk = txn.create_node(labels=["Chunk"], properties={"text": "The transformer uses self-attention"})
        # hash_embed는 의미가 없는 결정적 자리 표시자다. 실제로는 임베딩 모델을 쓴다.
        txn.set_vector(chunk.id, "embedding", hash_embed("The transformer uses self-attention", dimensions=128))
        txn.create_edge(chunk.id, doc.id, "PART_OF")
        txn.commit()

    rows = db.query(
        """
        MATCH (chunk:Chunk)-[:PART_OF]->(doc:Document)
        WHERE chunk.embedding <=> $q < 0.5
        RETURN doc.title, chunk.text
        """,
        parameters={"q": hash_embed("attention", dimensions=128)},
    )
    for row in rows:
        print(row["doc.title"])
```

README는 예제의 `hash_embed`가 의미 있는 임베딩이 아니라서 비슷한 텍스트가 가까운 벡터를 만들지 않고, 거리 임계값은 임의적이며 유사도 질의가 아무것도 찾지 못할 수 있다고 분명히 적는다.
실제로는 Ollama나 OpenAI의 임베딩을 HTTP 클라이언트로 붙이거나 외부 모델의 결과를 넣는다.

README에는 다른 도구를 써야 할 때라는 절도 있다.
여러 애플리케이션이 동시에 쓰는 경우, 데이터가 본질적으로 표 형태인 경우, 한 기기를 넘어 확장해야 하는 경우, Cypher 전체가 필요한 경우, 성숙한 도구 생태계가 필요한 경우다.

## 분석

### SQLite의 자리를 그래프에 옮기려는 시도다

Show HN 제목은 그래프 데이터베이스를 위한 SQLite였다.
이 비유는 기능이 아니라 배치 방식을 가리킨다.
SQLite가 클라이언트 서버 관계형 DB 옆에서 파일 하나로 끝나는 선택지를 만들었듯, LatticeDB는 Neo4j 같은 서버형 그래프 DB 옆에 같은 자리를 만들려 한다.

GN의 libredb는 로컬 에이전트 메모리나 Graph RAG를 만들다 보면 보통 저장소 서너 개를 이어 붙이게 되는데, 그걸 파일 하나로 끝낼 수 있다는 점을 반겼다[^gn-libredb].
그래프 DB, 벡터 DB, 검색 엔진을 따로 두면 세 저장소의 일관성을 애플리케이션이 맞춰야 한다.
한 트랜잭션 안에서 노드와 벡터와 전문 색인이 함께 바뀌면, 그 조율 비용이 엔진 안으로 들어간다.

### 경쟁 구도는 비어 있던 자리에서 생겼다

HN에서 가장 많이 나온 질문은 왜 다른 것을 쓰지 않느냐였다.
nrjames가 왜 Kuzu를 포크하지 않았느냐고 묻자, 작성자는 처음부터 직접 만들며 배우고 싶었고, 둘 다 단일 파일 그래프 DB지만 LatticeDB는 트랜잭션 중심의 행 지향이고 Kuzu는 열 지향이라 데이터 배치가 다르다고 답했다[^smiths1999-kuzu].
threatofrain은 Kuzu가 이미 멈춘 프로젝트로 보인다고 덧붙였고[^threatofrain], README도 Kuzu를 2025년 10월 아카이브되었다고 표시한다.

DuckDB 확장 duckpgq와의 차이를 묻자 작성자는 표를 가끔 그래프처럼 훑고 싶으면 duckpgq, 그래프 탐색이 주된 질의 방식이면 LatticeDB라고 정리했다[^smiths1999-duckpgq].
SurrealDB 임베디드 모드와 비교해 달라는 질문에는 SurrealDB는 단일 파일이 아니고 많은 데이터 모델을 지원하며 회사가 뒤에 있지만, LatticeDB는 단순함에 집중한 1인 프로젝트라고 답했다[^smiths1999-surreal].
댓글에는 LadybugDB, ArcadeDB, SparrowDB, marsdb 같은 비슷한 프로젝트가 줄줄이 등장했다.
임베디드 그래프 DB라는 자리가 Kuzu 이후 비어 있었고, 여러 사람이 동시에 그 자리를 채우려 한다는 신호다.

### 정직한 README가 신뢰를 만든다

anigbrowl은 README의 써야 할 때와 쓰지 말아야 할 때 절이 좋은 도구에도 흔히 빠져 있다며 특히 높이 평가했다[^anigbrowl].
GN의 libredb도 아직 지원하지 않는 Cypher 기능을 솔직하게 적어 둔 점에 믿음이 간다고 했다[^gn-libredb].
작성자는 README를 빠르게 훑고 이 프로젝트가 찾던 것인지 판단하고 끝낼 수 있는 문서로 만들고 싶었다고 답했다[^smiths1999-readme].

새 데이터베이스는 성능 표보다 한계 목록에서 신뢰를 얻는다.
사용자는 무엇이 빠른지보다 무엇이 안 되는지를 먼저 알아야 도입 여부를 판단할 수 있기 때문이다.

## 비평

### 성능 비교표가 재현되지 않았다

README의 SQLite 비교는 같은 기기, 같은 하네스에서 쟀다는 점을 강조한다.
그런데 HN에서 adsharma가 M4 Mac mini에서 `zig build sqlite-benchmark`를 직접 돌리자, 10만 노드 1-hop이 LatticeDB 5.7μs, SQLite 16.1μs로 2.8배 차이에 그쳤다[^adsharma].
README의 36배와 크게 다르고, 3-hop은 1.3배였다.
가변 경로만 70.4배로 README의 75배와 비슷했다.

작성자는 LatticeDB 수치는 꽤 비슷하지만 SQLite 수치가 크게 어긋났다며 새 컴퓨터로 다시 재겠다고 답했다[^smiths1999-bench].
그러나 현재 README의 중간 규모 표는 여전히 SQLite 1-hop을 290.0μs로 적고 있다.
비교의 한쪽이 최적화되지 않은 상태에서 잰 숫자라면, 수십 배라는 결론은 LatticeDB의 성능이 아니라 측정 환경의 차이를 보여 줄 뿐이다.
재귀 CTE가 깊은 경로에서 불리하다는 구조적 차이는 남지만, 얕은 탐색의 격차는 README가 주장하는 것보다 훨씬 작을 수 있다.

### 다중 프로세스 안전은 출시 뒤에 채워졌다

vladigtr가 한 파일에 동시에 쓰는 작성자를 어떻게 다루느냐고 묻자, 작성자는 같은 프로세스 안에서는 DB 수준에서 막지만 프로세스 사이의 안전장치는 없다는 것을 코드를 다시 보고 알았다며 그날 밤 파일 잠금을 추가하겠다고 했고[^smiths1999-lock], 실제로 다음 릴리스에 넣었다[^smiths1999-lock-done].
itissid가 litestream 같은 백업을 묻자 핫 복사 기능을 그날 밤 올리겠다고 답했다[^smiths1999-backup].
지금 README의 핫 백업과 연속 백업은 이 대화 이후에 들어온 기능이다.

빠른 대응 자체는 좋은 신호지만, 이 순서는 데이터베이스를 평가할 때 기준이 된다.
단일 작성자라는 설계 선언이 있었는데도 그 선언을 강제하는 장치가 없었다는 것은, 내구성과 동시성처럼 데이터를 잃게 만드는 영역의 검증이 사용자 피드백에 기대고 있었다는 뜻이다.
출시 후 몇 주 된 데이터베이스를 쓸 때는 기능 목록보다 이런 영역의 테스트 범위를 먼저 확인해야 한다.

### LLM이 만든 테스트를 믿지 않았다는 증언이 가장 중요한 정보다

tescreal이 기여자 목록의 Claude를 보고 얼마나 썼느냐고 묻자, 작성자는 Claude와 Codex를 폭넓게 썼다고 답했다[^smiths1999-claude].
초기에는 Claude가 기능을 만들고 LatticeDB 내부 구조 책의 한 절처럼 설명하게 한 뒤 코드를 읽으며 배웠고, 후반의 복잡한 기능은 구현을 이해하기보다 검증하는 데 시간을 썼다.
오래 손으로 쓰지 않은 SIMD 코드는 리뷰해도 미묘한 버그를 놓칠 것이 확실해서, 코드가 맞다고 가정하고 어떻게 검증할지에 집중했다는 것이다.
벤치마크 결과가 좋아 보였는데 테스트 벡터가 사소한 것이라 결과 전체가 무효였고, 새 벤치마크 세트로 다시 쟀더니 결과가 나빠 구현을 다시 봐야 했던 일도 있었다.

다른 답글에서는 LLM이 피상적인 테스트를 자주 쓰고, 테스트가 모두 통과해도 실제로 써 보면 기능이 명백히 깨져 있었다고 적었다[^smiths1999-memory].
LLM 덕분에 이 규모를 만들 수 있었지만 그래프 DB를 만들고 끝나면 알려 달라는 식과는 거리가 멀었다는 것이다.
이 증언은 README의 성능 표를 읽는 방법을 바꾼다.
작성자 자신이 한 번은 무의미한 벤치마크에 속았고, HN에서는 SQLite 비교가 재현되지 않았다.
에이전트로 만든 데이터베이스의 숫자는 제3자가 다시 재기 전까지 가설로 읽어야 한다.

## 인사이트

### 에이전트 메모리가 임베디드 그래프 DB의 수요를 되살리고 있다

작성자는 1M 노드로 성능을 쟀지만 실제로는 에이전트 메모리를 실험하는 다른 프로젝트에서 작은 규모로 쓴다고 했다[^smiths1999-memory].
관련 기억을 찾는 일이 그래프 탐색이고, 그것이 Graph RAG와 비슷하다는 설명도 덧붙였다[^smiths1999-duckpgq].

한동안 그래프 DB는 사기 탐지나 추천처럼 서버 규모 문제에 쓰였고, 임베디드 그래프 DB는 틈새였다.
에이전트가 로컬에서 도는 시대에는 사정이 달라진다.
에이전트 하나마다 기억 저장소가 필요하고, 그 저장소는 사용자의 기기 안에 있어야 하며, 기억 사이의 관계와 의미 유사도와 키워드를 함께 찾아야 한다.
LatticeDB와 그 경쟁자들이 한꺼번에 등장한 것은 이 수요 때문이다.

### 권한 같은 도메인 로직은 여전히 그래프 밖에 남는다

k9294가 문서에 접근 권한을 받으면 하위 문서 전체에 자동으로 권한이 생기는 계층 권한을 그래프로 어떻게 모델링하느냐고 묻자, 작성자는 접근 간선과 부모 간선을 두고 권한이 있는 첫 루트까지 거슬러 올라가는 방식을 제안하면서도, 그 전부가 비즈니스 로직이라 DB만 봐서는 규칙을 알 수 없다는 한계를 인정했다[^smiths1999-perm].
infogulch는 현대 인가 시스템이 ReBAC 같은 그래프 기반 모델이고 SpiceDB 같은 구현의 스키마를 LatticeDB로 옮기기 어렵지 않을 것이라고 답했다[^infogulch].

이 교환은 임베디드 DB의 한계가 저장이 아니라 규칙에 있다는 점을 보여 준다.
에이전트 메모리에 사용자 데이터가 쌓이면 곧 누가 무엇을 볼 수 있는가가 문제가 된다.
그래프가 권한 모델을 표현하기에 자연스러운 구조라도, 규칙이 애플리케이션 코드에 흩어지면 검증할 수 없다.
LatticeDB가 SQLite의 자리를 차지하려면, 결국 제약이나 뷰처럼 규칙을 데이터베이스 안에 선언하는 수단이 필요해질 것이다.

### 1인 데이터베이스의 신뢰는 코드가 아니라 재현 가능성에서 온다

pwmglenn의 SurrealDB 비교 질문에 작성자는 회사가 뒤에 있는 SurrealDB와 달리 LatticeDB는 자기 혼자라고 답했다[^smiths1999-surreal].
데이터베이스는 한 번 채택하면 오래 쓰는 소프트웨어라, 1인 프로젝트라는 사실은 도입의 가장 큰 장벽이다.

이 장벽을 낮추는 수단이 README의 재현 명령이다.
`zig build benchmark`, `zig build vector-benchmark`, `zig build sqlite-benchmark`를 누구나 돌릴 수 있고, 실제로 adsharma가 돌려 차이를 찾아냈다.
재현 가능한 측정은 1인 프로젝트가 기업 뒷받침 없이도 신뢰를 쌓을 수 있는 거의 유일한 경로다.
그 경로가 작동하려면, 누군가 다른 숫자를 내놓았을 때 README의 표가 따라 바뀌어야 한다.

---

[^gn-libredb]: <https://news.hada.io/topic?id=34517#cid66657>

[^smiths1999-kuzu]: <https://news.ycombinator.com/item?id=49440044>

[^threatofrain]: <https://news.ycombinator.com/item?id=49440231>

[^smiths1999-duckpgq]: <https://news.ycombinator.com/item?id=49439015>

[^smiths1999-surreal]: <https://news.ycombinator.com/item?id=49452336>

[^anigbrowl]: <https://news.ycombinator.com/item?id=49444974>

[^smiths1999-readme]: <https://news.ycombinator.com/item?id=49448297>

[^adsharma]: <https://news.ycombinator.com/item?id=49443992>

[^smiths1999-bench]: <https://news.ycombinator.com/item?id=49448182>

[^smiths1999-lock]: <https://news.ycombinator.com/item?id=49441589>

[^smiths1999-lock-done]: <https://news.ycombinator.com/item?id=49448617>

[^smiths1999-backup]: <https://news.ycombinator.com/item?id=49441760>

[^smiths1999-claude]: <https://news.ycombinator.com/item?id=49439378>

[^smiths1999-memory]: <https://news.ycombinator.com/item?id=49438833>

[^smiths1999-perm]: <https://news.ycombinator.com/item?id=49441458>

[^infogulch]: <https://news.ycombinator.com/item?id=49443678>
