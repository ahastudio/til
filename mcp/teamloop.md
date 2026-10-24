# Teamloop: 결정이 어떻게 바뀌어 왔는지 시점별로 묻는 시간 인식 RAG

<https://teamloop.io/>

## 소개

Teamloop은 GitHub, Jira, Notion, Google Docs 같은 업무 도구를 대상으로 하는
시간 인식(time-aware) 검색 서비스다.
홈페이지는 일반 RAG가 오늘 무엇이 참인지 알려 준다면 Teamloop은 어떻게 여기까지
왔는지 알려 준다고 소개한다.
AI 비서를 Teamloop의 MCP 서버에 연결해 여러 도구를 한 번에 조회하고,
결과로 지식 그래프를 만들고, PRD와 ADR과 브리프를 합성하는 흐름을 보여 준다.

조회 방식은 네 가지다.
현재 상태(Current State), 특정 날짜 시점(Point-in-Time), 기간 동안의
변화(Evolution),
두 시점의 차이(Compare)다.
기능으로는 여러 도구 통합, AI 합성, 근거가 사라지는 판단 기록을 남기는 저널,
협업 노트북, 질의할 때마다 최신 데이터를 가져오는 구조(백그라운드 동기화 없음),
모든 합성 결과의 출처 인용을 내세운다.

이 문서는 홈페이지와 공개 문서 사이트(`docs.teamloop.io`)를 읽고 썼고,
서비스에 가입하거나 MCP 서버를 실행해 보지는 않았다.
동작에 대한 서술은 모두 Teamloop 자신의 설명이다.

## 동작 방식

### 질의가 들어오면 그때 가져오고 그때 쌓는다

문서는 Teamloop이 데이터를 백그라운드로 동기화하지 않는다고 설명한다.
질의가 오면 연결된 도구에서 새 데이터를 가져오고, 결과를 임베딩과 함께 캐시하며,
지식 그래프는 실제 질의를 거치며 자란다는 것이다.[^overview]
그래서 한 번도 질의하지 않은 영역은 그래프에 없고,
시점 조회가 돌려주는 과거는 Teamloop이 그 시점 이후에 본 데이터의 범위로
한정된다는 추론이 따른다.
이 추론은 이 문서의 해석이며, 문서가 직접 밝힌 한계는 아니다.

각 지식에는 시간 메타데이터가 붙는다.
사건이 실제로 일어난 때(`event_date`), 그 버전이 유효했던 구간(`valid_from`,
`valid_to`),
이 결정이 무엇을 대체했고 무엇으로 대체됐는지(supersession)다.[^overview]

### 검색은 벡터와 키워드를 합치고 재순위를 매긴다

모든 질의는 벡터 검색, BM25 전문 검색, 순위 결합(Reciprocal Rank Fusion), 교차
인코더 재순위, 점수 정규화 단계를 지난다.[^hybrid]
벡터 검색은 임베딩 코사인 유사도로 상위 50개를, 전문 검색은 PostgreSQL의
`tsvector`와 `ts_rank_cd`로 상위 50개를 가져온다.[^hybrid]
두 목록은 `k=60`인 순위 결합으로 합치고, 상위 20개를 재순위 단계로 넘겨 5개만
남긴다.[^hybrid]
재순위에는 300ms 제한이 있고, 재순위기가 응답하지 않거나 시간을 넘기면 경고를
남기고 결합 순서 그대로 결과를 준다.[^hybrid]

배포 형태에 따라 모델이 다르다.
SaaS는 Voyage AI의 `voyage-3`(1024차원)과 `rerank-2`를,
AWS Marketplace 배포는 Amazon Titan V2와 Bedrock의 Cohere `rerank-v3.5`를
쓴다.[^hybrid]
임베딩 모델은 조직이 첫 임베딩을 만든 뒤에는 바뀌지 않는다.[^hybrid]

### 도구는 이슈와 문서를 엔티티로 바꾼다

GitHub에서는 이슈, PR, 디스커션이 `DOCUMENT`로, 커밋과 상태 변경이 `CHANGE`로,
댓글 작성자가 `PERSON`으로 매핑된다.[^github]
이슈 조회 때는 변경 이력(상태, 라벨, 담당자, 마일스톤)을 함께 가져온다.[^github]

## 연결하기

공개 문서의 MCP 설정은 Claude Desktop, Claude Code, Cursor 같은 stdio 지원
클라이언트에 같은 명령을 넣는 방식이다.[^mcp]

```json
{
  "mcpServers": {
    "teamloop": {
      "command": "npx",
      "args": ["-y", "@teamloop/mcp-server"]
    }
  }
}
```

인증은 API 키 없이 OAuth 2.0 장치 인증을 쓴다.
첫 사용 때 브라우저가 열려 로그인하고, 토큰은 로컬에 저장돼 자동으로
갱신된다.[^mcp]
SaaS는 Auth0를, AWS Marketplace 배포는 Cognito를 쓰며, 후자는 CloudFormation
출력의 엔드포인트로 연결한다.[^mcp]

도구 쪽 연결은 토큰을 직접 넣는 방식이다.
GitHub의 경우 `repo`와 `read:org` 범위의 classic personal access token을 만들어
설정에 붙여 넣는다.[^github]
Teamloop은 토큰을 `pgcrypto`로 암호화해 저장하고 저장소에 쓰지 않는다고
밝힌다.[^github]

## 트레이드오프

### 질의할 때 가져오는 구조는 신선함을 주고 과거의 빈틈을 남긴다

백그라운드 동기화가 없으면 토큰이 닿는 범위에서 항상 최신 데이터를 보고, 쓰지
않는 도구의 데이터를 미리 복사해 두지 않는다.
대신 두 가지가 어려워진다.
첫째, 시점 조회는 Teamloop이 본 적 있는 버전만 재구성할 수 있다.
둘째, 질의마다 외부 API 호출이 늘어서 지연과 호출 제한이 질의 품질에 영향을
준다.
문서는 두 번째를 병렬 실행과 배치 질의로 줄인다고 하지만 수치는 제시하지
않는다.[^overview]

### 개인 액세스 토큰은 사람의 권한을 그대로 넘긴다

토큰이 읽을 수 있는 저장소와 이슈가 곧 Teamloop이 보는 범위다.[^github]
쓰기 권한은 쓰지 않는다고 하지만, classic PAT의 `repo` 범위는 GitHub 쪽에서 읽기
전용으로 제한할 수 없는 범위다.
이 문장은 GitHub의 토큰 범위 설계에 대한 이 문서의 서술이며, Teamloop 문서가
말한 것이 아니다.
읽기만 필요한 조직이라면 토큰을 만들 계정과 범위부터 정해야 한다.

## 함정

홈페이지와 문서가 말하는 연동 대상이 서로 다르다.
홈페이지는 GitHub, Jira, Notion, Google Docs를 내세우고 문서의 첫 화면은 GitHub,
Notion, Linear를 소개한다.[^docs-home]
문서의 GitHub 페이지 이전과 다음 링크에는 Figma와 Jira 연동 페이지가
있다.[^github]
어느 연동이 실제로 제공되는지는 가입해서 확인해야 한다.

가격 페이지는 서비스에 맞춰진 내용이 아니다.
세 개의 요금제(월 29달러, 69달러, 199달러)가 있지만 항목 설명은 라틴어 더미
문구이고,
소개 문구는 우주 여정과 템플릿 다운로드를 말하며 체험 기간이 없다고
답한다.[^pricing]
홈페이지의 무료 체험 시작 버튼과 맞지 않으므로, 이 가격 페이지는 템플릿이
정리되지 않은 상태로 보인다.
실제 요금을 판단하는 근거로 쓸 수 없다.

## 확인하기

도입을 검토한다면 가입 전에 할 수 있는 확인이 몇 가지 있다.
공개 문서의 질의 모드 문서로 시점 조회가 어떤 데이터를 돌려주는지 읽고,
`npx @teamloop/mcp-server`로 MCP 서버가 뜨는지 확인하고,
시험용 저장소 하나에만 권한을 준 토큰으로 연결해 본다.
그런 다음 알고 있는 결정(예: 몇 달 전 닫힌 이슈의 결정)을 as-of 질의로 물어,
그 시점의 상태가 재구성되는지 직접 대조한다.

## 체크리스트

- 연결하려는 도구(Jira, Google Docs, Linear)가 실제로 제공되는가.
- 토큰은 읽기에 필요한 최소 범위와 별도 계정으로 만들었는가.
- 시점 조회로 확인하려는 과거가 이미 질의로 한 번이라도 조회된 영역인가.
- 데이터가 SaaS와 AWS Marketplace 중 어느 배포에서 처리되고 어떤 임베딩 모델을
쓰는가.
- 요금과 체험 조건을 가격 페이지가 아니라 가입 화면에서 확인했는가.

## 기억할 원칙

### 지식의 이력은 질의가 아니라 수집이 만든다

시간 인식 검색은 결정이 어떻게 바뀌었는지 묻게 해 주지만, 답할 수 있는 이력은
시스템이 실제로 본 데이터에서만 나온다.
질의할 때 가져오는 구조는 이력을 질의 시점부터 쌓기 시작한다는 뜻이다.
도입의 첫 단계는 어떤 결정의 이력이 필요한지 정하고, 그 영역을 먼저 한 번 훑어
시스템에 보여 주는 일이다.

---

[^overview]: TeamLoop Docs, [Welcome to TeamLoop](https://docs.teamloop.io/getting-started/overview/)

[^hybrid]: TeamLoop Docs, [Hybrid Search](https://docs.teamloop.io/features/hybrid-search/)

[^mcp]: TeamLoop Docs, [MCP Setup Guide](https://docs.teamloop.io/mcp/setup/)

[^github]: TeamLoop Docs, [GitHub Integration](https://docs.teamloop.io/integrations/github/)

[^docs-home]: TeamLoop Docs, [TeamLoop](https://docs.teamloop.io/)

[^pricing]: Teamloop, [Pricing — Teamloop](https://teamloop.io/pricing)
