# Anthropic 공식 스킬 저장소

> Anthropic이 내부 엔지니어들이 사용하는 스킬 라이브러리를
> 오픈소스로 공개했다.

- 트윗:
  <https://twitter.com/ihtesham2005/status/2026752089473314975>
- GitHub: <https://github.com/anthropics/skills>

## 개요

Anthropic이 자사 엔지니어들이 실제로 사용하는 스킬을 공개한 공식
저장소다. 문서 생성, 디자인, MCP 서버 구축, 웹앱 테스트 등 실무에서
바로 쓸 수 있는 프로덕션 수준의 스킬이 포함되어 있다. 한 번
복사하면 Claude Code, Claude.ai, API, VS Code 어디서든 동작한다.

## 저장소 구조

```text
anthropics/skills/
├── skills/              # 16개 스킬
│   ├── 문서 생성 (docx, pdf, pptx, xlsx)
│   ├── 크리에이티브 & 디자인
│   ├── 개발 & 기술
│   └── 엔터프라이즈 & 커뮤니케이션
├── spec/                # Agent Skills 명세
└── template/            # 새 스킬 생성 템플릿
```

## 포함된 스킬 16종

| 카테고리       | 스킬                  | 용도                         |
| -------------- | --------------------- | ---------------------------- |
| 문서 생성      | docx                  | Word 문서 생성·편집          |
|                | pdf                   | PDF 생성·폼 추출            |
|                | pptx                  | PowerPoint 프레젠테이션 생성 |
|                | xlsx                  | Excel 스프레드시트 생성      |
| 크리에이티브   | algorithmic-art       | p5.js 기반 제너러티브 아트   |
| & 디자인       | canvas-design         | 캔버스 기반 디자인           |
|                | frontend-design       | 프론트엔드 디자인            |
|                | theme-factory         | 테마 생성·커스터마이징       |
|                | slack-gif-creator     | Slack용 GIF 생성             |
| 개발 & 기술    | mcp-builder           | MCP 서버 구축 가이드         |
|                | webapp-testing        | Playwright 기반 웹앱 테스트  |
|                | web-artifacts-builder | 웹 아티팩트·컴포넌트 빌더   |
|                | skill-creator         | 새 스킬 제작 도우미          |
| 엔터프라이즈   | brand-guidelines      | 브랜드 가이드라인 적용       |
| & 커뮤니케이션 | doc-coauthoring       | 문서 공동 작성 워크플로      |
|                | internal-comms        | 사내 커뮤니케이션 템플릿     |

## 설치 및 사용

Claude Code에서 마켓플레이스를 등록하고 스킬을 설치한다.

```bash
# 마켓플레이스 등록
/plugin marketplace add anthropics/skills

# 문서 스킬 설치
/plugin install document-skills@anthropic-agent-skills

# 예제 스킬 설치
/plugin install example-skills@anthropic-agent-skills
```

사용 예시:

```text
"PDF 스킬로 path/to/file.pdf에서 폼 필드를 추출해줘"
"xlsx 스킬로 매출 데이터 스프레드시트를 만들어줘"
```

Claude.ai에서는 유료 플랜 사용자에게 기본 제공된다.

## 주요 스킬 상세

**MCP Builder**: MCP 서버를 4단계로 구축한다. 심층 리서치 →
구현 → 리뷰·테스트 → 평가 생성. MCP 서버를 처음 만드는 사람도
모범 사례를 따를 수 있다.

**Doc Co-Authoring**: 3단계 문서 공동 작성. 컨텍스트 수집(명확화
질문) → 정제·구조화(섹션별 5단계 순환) → 독자 테스트(새 Claude
인스턴스로 검증).

**Webapp Testing**: Playwright + Python으로 웹앱 UI를 자동
검증한다. 스크린샷 기반 디버깅을 지원한다.

**Algorithmic Art**: p5.js로 제너러티브 아트를 만든다. 시드 기반
랜덤, 파라미터 튜닝, Anthropic 브랜딩 템플릿을 포함한다.

## 라이선스

- 대부분의 스킬: Apache 2.0 (오픈소스)
- 문서 스킬(docx, pdf, pptx, xlsx): Source-Available (참조 구현)

## 파트너 스킬

Notion이 첫 번째 파트너로 참여했다. Claude에서 Notion
워크스페이스를 다루는 전용 스킬을 제공한다.

## 인사이트

### 1. "한 번 만들면 어디서나 동작"의 실현

Skill의 가장 강력한 가치는 이식성이다. 같은 SKILL.md 파일 하나로
Claude Code, Claude.ai, API, VS Code에서 동일하게 동작한다.
이것은 Agent Skills 오픈 표준 덕분이다. MCP가 "도구 연결"의
표준이라면, Skills는 "작업 방법"의 표준이다.

### 2. 문서 스킬이 핵심 자산이다

16개 스킬 중 문서 생성(docx, pdf, pptx, xlsx)이
Source-Available로 분리된 이유가 있다. 이 스킬들이 Claude의
공식 문서 생성 기능을 구동한다. 나머지는 Apache 2.0이지만,
문서 스킬은 Anthropic의 핵심 제품 차별화 요소다.

### 3. 스킬 저장소는 "레시피북"이다

저장소의 진짜 가치는 개별 스킬보다 패턴에 있다. MCP Builder의
4단계 구조, Doc Co-Authoring의 3단계 검증 루프, Webapp Testing의
스크린샷 디버깅 패턴은 커스텀 스킬을 만들 때 참고할 설계
패턴이다. 직접 사용하지 않더라도 "프로덕션 수준 스킬은 이렇게
만드는 것"을 보여준다.

### 4. 기존 문서와의 관계

이 저장소는 [Skills 개념 정리](./skills.md)의 "실체"이고,
[제작 가이드](./claude-skills-guide.md)의 "완성된 결과물"이다.
개념(skills.md) → 만드는 법(claude-skills-guide.md) → 실전
예제(anthropics/skills 저장소)로 이어지는 학습 경로가 완성된다.

### 5. 플러그인 마켓플레이스의 등장

`/plugin marketplace add`로 스킬을 설치하는 구조는 npm이나
Homebrew와 비슷한 패키지 매니저 패턴이다. 현재는 Anthropic 공식
저장소만 있지만, 커뮤니티 저장소가 생기면 스킬 생태계가
폭발적으로 성장할 가능성이 있다. Notion이 파트너로 참여한 것이
그 시작이다.

## 관련 문서

- [Claude Code Skills](./skills.md)
- [Claude Skills 제작 완전 가이드](./claude-skills-guide.md)
- [코드 리뷰 스킬 분석](./code-review-skill.md)
