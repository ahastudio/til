# Azure API Connections: 검증으로 막은 테넌트 경계는 계속 뚫렸다

원문: [Azure's Weakest Link - Five Full Cross-Tenant Compromises](https://www.binarysecurity.no/posts/2026/10/one-root-case)

HN 토론: <https://news.ycombinator.com/item?id=50301854> (312점, 58개 댓글)

## 요약

보안 연구자 Haakon Wik Gulbrandsrud가 2026년 10월 2일에 올린 글이다.
Azure Logic Apps의 일부인 API Connections에서 찾은 취약점 다섯 건을 다룬다.
Gulbrandsrud는 같은 시리즈의 앞선 두 글에서 이 시스템의 구조가 심각하게 불안전하다고
썼고, 이번 글은 같은 문제를 다른 경로로 다시 드러낸 취약점을 모았다고 한다.
이 취약점들로 받은 보상이 합쳐서 20만 달러라고 적는다.
Blue Hat Asia 2026에서 발표도 했다고 한다.

핵심 주장은 한 문장이다.
API Connections에서는 누구든 전 세계 다른 연결(connection)을 완전히 장악할 수
있으며, 이를 막는 것은 여러 시스템에 덧붙인 입력 검증뿐이라는 것이다.
영향 범위에는 다른 테넌트의 Key Vault와 Azure SQL 데이터베이스,
Jira나 Salesforce처럼 외부에 연결된 서비스가 모두 들어간다.

글이 설명하는 구조는 이렇다.
로직 앱이 공유 Azure API Management 인스턴스에 요청을 보내면,
이 인스턴스가 커넥터 종류의 정의에서 유효한 동작인지 확인한다.
그다음 입력으로 받은 토큰을 연결에 설정된 백엔드용 토큰으로 바꿔 쓰고,