# PR Agent (qodo-ai/pr-agent)

<https://github.com/qodo-ai/pr-agent>

AI 기반 코드 리뷰 자동화 도구. Qodo에서 개발했으며 현재 오픈소스
커뮤니티 프로젝트로 운영된다.

## 핵심 기능

| 커맨드       | 역할                              |
|--------------|-----------------------------------|
| `/describe`  | PR 제목·설명 자동 생성            |
| `/review`    | 코드 품질 분석 및 문제점 리포트   |
| `/improve`   | 리팩터링·최적화 제안              |
| `/ask`       | PR 변경사항에 대한 대화형 Q&A     |
| `/add_docs`  | 코드 문서(docstring 등) 자동 추가 |
| `/update_changelog` | CHANGELOG 자동 업데이트  |

## 아키텍처 인사이트

### 단일 LLM 호출 설계

각 도구는 LLM 호출 1회로 완료되도록 설계되어 있다.
평균 응답 시간 약 30초. 비용 효율성을 최우선으로 고려한 구조다.

### PR 압축(Compression) 전략

대형 PR을 처리하기 위해 "토큰 인식 파일 패치 피팅" 기법을 사용한다.
컨텍스트 윈도우 한계를 넘는 PR도 자동으로 압축·요약해 처리한다.

### 도구별 파일 구조

```
pr_agent/tools/
├── pr_description.py      # /describe
├── pr_reviewer.py         # /review
├── pr_code_suggestions.py # /improve
├── pr_questions.py        # /ask
├── pr_add_docs.py         # /add_docs
├── pr_update_changelog.py # /update_changelog
├── pr_generate_labels.py  # 자동 레이블 생성
├── pr_similar_issue.py    # 유사 이슈 탐색
└── ticket_pr_compliance_check.py # 티켓 준수 검사
```

### 설정 구조

`pr_agent/settings/configuration.toml`에서 JSON 기반 프롬프트를
커스터마이징한다. 리뷰 카테고리, 출력 형식, LLM 모델을 유연하게
변경할 수 있다.

## 지원 플랫폼

- GitHub (가장 완전한 지원)
- GitLab
- Bitbucket
- Azure DevOps
- Gitea

## 지원 AI 모델

- OpenAI GPT 시리즈
- Anthropic Claude
- DeepSeek

## 배포 방식

```yaml
# GitHub Actions 예시
- name: PR Agent
  uses: qodo-ai/pr-agent@main
  env:
    OPENAI_KEY: ${{ secrets.OPENAI_KEY }}
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

로컬 CLI 사용:

```bash
pip install pr-agent
export OPENAI_API_KEY=<key>
python -m pr_agent.cli --pr_url <url> review
```

## 인사이트

- **Self-hosted 시 완전한 데이터 프라이버시 보장**: 코드가 외부로
  전송되지 않는다.
- **오픈소스 vs 상용**: 이 저장소는 Qodo 무료 티어와 별개다.
  컨텍스트 인식 기능 등은 상용에만 포함된다.
- **단일 LLM 호출 철학**: 비용과 속도를 고려해 멀티턴 대화보다
  단일 호출로 고품질 결과를 내는 방향으로 설계됐다.
- **Dynamic Context Enrichment**: 변경된 코드의 맥락을 동적으로
  수집해 더 정확한 리뷰를 제공한다.
