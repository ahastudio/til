# Claude Skills

<https://claude.com/blog/skills-explained>

Claude 에이전트 생태계를 구성하는 5가지 요소를 비교 설명.

## 5가지 구성 요소

### Skills

폴더에 저장된 지시사항·스크립트·자료를 Claude가 필요할 때
동적으로 발견하고 로드. 점진적 공개(Progressive Disclosure)로
컨텍스트 효율 극대화.

### Prompts

대화 중 전달하는 자연언어 지시사항. 단일 대화 내에서만 지속됨.

### Projects

자체 채팅 기록과 지식 기반을 가진 작업 공간.
200K 컨텍스트 윈도우 제공.

### Subagents

자체 컨텍스트 윈도우와 커스텀 시스템 프롬프트를 가진
전문화된 AI 어시스턴트. Claude Code와 Agent SDK에서 지원.

### MCP (Model Context Protocol)

외부 시스템 연결을 위한 개방형 표준.
Google Drive, Slack, GitHub 등 데이터 소스 접근.

## 비교

| 구성 요소  | 지속성      | 코드 포함 |
| ---------- | ----------- | --------- |
| Skills     | 여러 대화   | 가능      |
| Prompts    | 단일 대화   | 불가능    |
| Projects   | 프로젝트 내 | 불가능    |
| Subagents  | 세션 간     | 가능      |
| MCP        | 지속 연결   | 가능      |

## 실전 조합 예시: 경쟁사 분석 에이전트

- **Project**: 산업 리포트, 경쟁사 문서 업로드
- **MCP**: Google Drive, GitHub, 웹 검색 연결
- **Skills**: 경쟁사 분석 프레임워크 제공
- **Subagents**: 시장 분석가, 기술 분석가 역할 분담

각 구성 요소는 고유한 목적을 가지며, 조합할 때 가장 강력한
워크플로우가 만들어짐.
