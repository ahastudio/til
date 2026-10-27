# Onyx: 50개 넘는 앱의 지식을 색인해 AI 에이전트에 대 주는 컨텍스트 레이어

<https://github.com/onyx-dot-app/onyx>

Show HN: [Open-source Deep Research across workplace applications](https://news.ycombinator.com/item?id=43242551)

## 소개

Onyx는 팀과 AI 에이전트를 위한 지식, 곧 컨텍스트 레이어를 자처하는 오픈소스
플랫폼이다.
README는 50개 넘는 애플리케이션에 연결해 지식을 색인하고 드러내며, 유연한 셀프
호스팅 배포로 데이터 주권을 지킨다고 소개한다.
검색을 넘어 웹 검색, 샌드박스, 스킬 같은 기능으로 LLM을 확장한다고 한다.
README의 문구는 AI 신입 사원이 아니라 AI 동료를 원한다는 말로 시작한다.
저장소는 2023년 4월 27일에 만들어졌고, 2026년 10월 27일에 확인한 시점에 스타
33,010개, 포크 4,651개, 열린 이슈 562개였으며 최신 릴리스는 v5.0.1(2026년 10월
26일)이다.
HN의 한 댓글은 이 프로젝트가 Danswer에서 이름을 바꾼 것이라고
알린다.[^PhilippGille]
라이선스는 README가 MIT 배지를 달면서도 두 판이 있다고 설명하고, GitHub의
라이선스 필드는 판별 불가로 나온다.

## 동작 방식

Onyx는 연결된 모든 소스의 지식 표현을 만든다.
데이터를 메타데이터와 권한과 함께 가져와 수집해서 하위 용도에서 쓰기 쉽게 한다.
README는 MCP 기반 검색과 색인 없는 접근에 비해 더 믿을 만하고 지연이 낮고 비용이
낮은 컨텍스트를 준다고 주장한다.
에이전트가 수십 개의 MCP를 반복해서 검색하며 수천 토큰을 태우는 대신 내부
표현에서 즉시 컨텍스트를 가져와 가장 관련 있는 문서만 걸러 낸다는 것이다.

기능은 다음과 같다.
Agentic RAG는 하이브리드 색인과 정보 검색에 맞춘 사용자 정의 에이전트
하네스이고, Deep Research는 다단계 연구 흐름의 상세 보고서다.
Custom Agents는 고유한 지식 부분집합과 지침과 행동 능력을 가진 에이전트이고, Web
Search는 Serper, Google PSE, Brave, SearXNG를 지원하며 자체 웹 크롤러와
Firecrawl과 Exa 지원이 있다.
External Actions와 MCP는 외부 애플리케이션에서 작업을 끝까지 수행하게 하고,
Secure Sandbox는 코드를 실행하고 중간 산출물을 다루는 샌드박스다.
Artifacts는 문서와 그래픽을 생성하고, Voice Mode는 음성 입력과 출력이다.
LLM은 Ollama, LiteLLM, vLLM 같은 셀프 호스팅과 Anthropic, OpenAI, Gemini 같은
상용을 모두 지원한다.

접근 경로는 웹과 데스크톱 앱, Slack과 Discord 봇, MCP 서버(Claude Code, Open
Code, Codex 같은 MCP 클라이언트가 같은 접근 통제로 회사 컨텍스트를 받음), Chrome
확장, 임베드 위젯이다.
어디서 질문하든 같은 보안과 세밀한 권한이 적용된다고 한다.

## 배포하기

한 줄 설치 명령이 제시된다.

```bash
curl -fsSL https://onyx.app/install_onyx.sh | bash
```

배포는 Docker, Kubernetes, Helm과 Terraform을 지원하고 주요 클라우드 가이드가
있다.
모드는 둘이다.
표준 Onyx는 전체 기능이고 권장 대상은 진지한 사용자와 큰 팀이며, 벡터와 키워드
색인, 커넥터로 지식을 동기화하는 백그라운드 작업 큐와 워커, 색인과 추론에 쓰는
딥러닝 모델 서버, 메모리 캐시(Redis)와 블롭 저장소(MinIO)가 들어간다.
Lite는 가벼운 AI 채팅 UI로 메모리 1GB 미만에서 돌지만 문서를 색인하지 못하며,
UI와 에이전트만 보려는 팀에 맞다.
설치 없이 써 보려면 Onyx Cloud가 있다.

보안은 문서 색인, 데이터베이스, 처리가 모두 자체 서비스 묶음 안에서 일어나는
에어갭 가능한 셀프 호스팅 배포를 내세우고, 신뢰할 임베딩 모델과 LLM 공급자(둘 다
로컬로 돌릴 수 있음)를 고를 수 있다고 한다.
엔터프라이즈 판은 협업, SAML과 OIDC 기반 SSO와 SCIM, 역할 기반 접근 통제, 사용
분석, 질의 기록 감사, PII 제거 같은 사용자 정의 코드, 화이트라벨링을 더한다.
Community Edition은 MIT 라이선스로 RAG, AI 채팅, 에이전트, 행동의 핵심 기능을
담고, Enterprise Edition은 큰 조직에 유용한 추가 기능을 담는다.

## 분석

### 핵심 주장은 에이전트에게 검색을 맡기지 않고 컨텍스트를 미리 만든다는 것이다

README의 차별점은 색인 없는 MCP 접근에 대한 대안이다.
에이전트가 여러 SaaS의 검색을 돌며 토큰을 쓰는 대신 미리 색인한 내부 표현에서
가져온다는 구조다.
HN에서 개발자 yuhongsun은 SaaS 앱의 내장 검색이 서로 다르고 약하며 웹 검색
엔진이 쓰는 많은 신호(역링크, 클릭 기록)가 없다는 어려움을
들었다.[^yuhongsun-challenge]
이 논리는 검색 품질을 앱마다 제각각인 것에서 한 곳의 색인으로 모으겠다는
선택이고, 그 대가가 색인과 동기화의 운영 비용이다.
이는 이 문서의 해석이다.

### 권한의 통합 표현이 이 제품의 가장 어려운 부분이다

nikisweeting은 앱마다 권한 모델이 다르다며 어떻게 다루는지
물었다.[^nikisweeting]
yuhongsun은 외부 도구마다 자기 권한 틀이 있고(Google Drive는 전체 공개, 도메인
공개, 비공개와 소유자, Slack은 공개 채널, 비공개 채널, DM, 그룹 DM) 이를 외부
객체와 사용자와 그룹을 Onyx 내부의 통합 표현으로 대응시킨다고
답했다.[^yuhongsun-perm]
thebeardisred는 차등 권한(사용자와 관리자, 역할 기반 접근 통제)을 원하면
엔터프라이즈 판을 사라는 답이라고 짚었다.[^thebeardisred]
권한 매핑이라는 어려운 부분이 유료 판의 가치와 겹친다는 점이 제품의 수익 구조를
보여 준다.

### 두 배포 모드는 채팅 UI와 지식 레이어를 분리한다

Lite는 문서를 색인하지 못하는 채팅 UI이고 표준은 색인과 동기화 인프라를
요구한다.
이 구분은 Onyx의 가치가 UI가 아니라 색인에 있음을 보여 준다.
UI만 원하는 팀은 가볍게 시작할 수 있지만, 컨텍스트 레이어의 가치는 표준
모드에서만 나온다.

## 비평

### 품질 주장이 검증 가능한 형태로 제시되지 않는다

README는 더 믿을 만하고 낮은 지연과 낮은 비용이라고 쓰지만 수치가 없다.
HN에서 janalsncm은 MRR이나 recall@k 같은 공식 평가를 했는지 물었고,[^janalsncm]
mentalgear는 대규모 지식 검색과 분석 범주의 포괄적 벤치마크가 필요하다고
했다.[^mentalgear]
yuhongsun은 Slack 메시지, 통화 기록, 기술 설계 문서, 정책을 담은 내부 데이터
세트로 평가했고 1만 문서에서 4K 토큰 기준 재현율이 94% 넘었다고
답했다.[^yuhongsun-eval]
이 값은 개발자의 내부 평가이고 데이터 세트는 공개되지 않았으며, 이 문서는
확인하지 못했다.

### 작동 원리의 설명이 비교 대상을 단순하게 그린다

README는 MCP 기반 검색과 색인 없는 접근을 대안으로 세우고 자기 방식이 더 낫다고
한다.
laborcontract는 다중 질의 생성, HyDE, 벡터와 BM25 검색, RRF, 재순위, 평가,
재시도 같은 전형적 RAG 파이프라인과 에이전트 접근이 어떻게 다른지, 서비스 20개를
연결하면 에이전트가 어떻게 검색 순서를 아는지 물었다.[^laborcontract]
yuhongsun은 RAG에 사용자 피드백 학습, 시간 가중치, 메타데이터, 제목과 본문
가중치, 색인과 추론 시점의 딥러닝 모델이 더해지고, 에이전트는 LLM이 RAG 위에서
어느 질문을 더 파고들지 정하는 반복이라고 답했다.[^yuhongsun-agent]
차별점은 개별 기법이 아니라 이 조합이어서, 이를 다른 접근과 같은 조건에서 비교한
자료는 이 문서가 확인하지 못했다.

### 에어갭 주장은 로컬 LLM이라는 어려운 조건을 가린다

yuhongsun은 회사 내부 문서를 모두 배포 안에서 처리하고 저장하는 선택지로는
자기들이 유일할 것이며 어려운 부분은 로컬 LLM뿐이라고 했다.[^yuhongsun-airgap]
이 문서는 유일하다는 주장을 검증하지 못했고, 로컬 LLM의 품질이 전체 결과를
좌우하는 어려운 부분이라는 점이 간단히 처리된다.

### 두 판의 경계가 사용자에게 불분명하다

README의 MIT 배지와 GitHub의 라이선스 필드(판별 불가)가 어긋나고, 엔터프라이즈
판의 기능이 어디까지인지는 가격 페이지로 넘긴다.
핵심 기능이 CE에 있다고 하지만 권한 통제의 일부가 EE라는 HN의 지적과 합치면,
어떤 팀이 CE로 충분한지는 도입 전에 확인해야 한다.

## 인사이트

### 컨텍스트 레이어의 가치는 검색이 아니라 권한과 최신성의 유지에 있다

색인을 만드는 일보다 원본의 권한과 변경을 계속 따라가는 일이 어렵다.
yuhongsun이 권한 매핑을 그 자체로 큰 도전이라고 한 이유다.
문서가 바뀌거나 권한이 바뀔 때 색인이 늦으면 오래된 접근 권한이나 낡은 내용이
답에 섞인다.
이 레이어를 쓰는 팀은 검색 품질보다 동기화 지연과 권한 반영의 속도를 먼저
시험해야 한다.
이는 이 문서의 해석이다.

### 에이전트 시대의 내부 지식 도구는 MCP 서버가 되어 다른 에이전트의 입구가 된다

Onyx는 MCP 서버로도 노출되어 Claude Code, Codex 같은 MCP 클라이언트가 회사
컨텍스트를 같은 접근 통제로 받는다.
이 구성은 지식 레이어가 최종 사용자 UI가 아니라 다른 에이전트가 쓰는 인프라가
되는 방향이다.
vishnudeva는 Confluence, Jira, Slack, Google Drive에 연결했을 때 수만 문서
규모에서 잘 작동한다는 사용 경험을 전했고,[^vishnudeva]
murshudoff는 자체 호스팅 판을 API로 RAG 인프라로 쓸 수 있는지
물었다.[^murshudoff]
이 질문들은 사용자가 이 제품을 앱이 아니라 부품으로 보기 시작했다는 신호다.

### 검색을 대신하는 연구 흐름의 가치는 시간과 비용의 비율로 읽힌다

monkeydust는 조직에서 임원이 질문하면 관리자와 담당자에게 이메일이 내려가는
구조가 심층 연구와 닮았다고 했고,[^monkeydust]
지금은 응답이 덜 낫더라도 시간이나 비용이 중요할 때 10%의 시간에 80%의 효과라면
쓸 만한 선택지라고 덧붙였다.[^monkeydust-ratio]
이는 에이전트의 가치를 정답률이 아니라 일을 한 번 도는 비용 대비 효과로 보는
시각이다.
같은 비율의 틀이 다른 AI 제품 평가에도 쓰인다.

### 이 글을 읽는 방법

이 문서는 저장소의 README와 2025년 Show HN 스레드를 읽고 정리했으며, 제품을
설치해 돌려 보지는 못했다.
HN 스레드는 제품이 Danswer라는 이름이던 시기의 것이어서 현재 기능과 다를 수
있다.
GeekNews와 Lobste.rs에서는 이 저장소의 스레드를 찾지 못했다.
판단을 가를 관찰은 둘이다.
하나는 같은 질문 묶음을 Onyx 색인 방식과 MCP 직접 검색 방식에서 돌려 정확도,
지연, 토큰 비용을 비교하는 것이다.
다른 하나는 외부 문서의 권한을 바꾼 뒤 Onyx 답에 그 변경이 반영되기까지의
지연이다.
둘 다 이 문서가 확인하지 못했다.

---

[^PhilippGille]: <https://news.ycombinator.com/item?id=43281690>

[^yuhongsun-challenge]: <https://news.ycombinator.com/item?id=43242555>

[^nikisweeting]: <https://news.ycombinator.com/item?id=43259579>

[^yuhongsun-perm]: <https://news.ycombinator.com/item?id=43260623>

[^thebeardisred]: <https://news.ycombinator.com/item?id=43260484>

[^janalsncm]: <https://news.ycombinator.com/item?id=43259183>

[^mentalgear]: <https://news.ycombinator.com/item?id=43264604>

[^yuhongsun-eval]: <https://news.ycombinator.com/item?id=43260724>

[^laborcontract]: <https://news.ycombinator.com/item?id=43259040>

[^yuhongsun-agent]: <https://news.ycombinator.com/item?id=43260594>

[^yuhongsun-airgap]: <https://news.ycombinator.com/item?id=43260525>

[^vishnudeva]: <https://news.ycombinator.com/item?id=43260050>

[^murshudoff]: <https://news.ycombinator.com/item?id=43263118>

[^monkeydust]: <https://news.ycombinator.com/item?id=43259419>

[^monkeydust-ratio]: <https://news.ycombinator.com/item?id=43263746>
