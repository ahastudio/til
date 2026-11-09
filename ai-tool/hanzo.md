# Hanzo AI: 남의 모델 앞에 라우터와 결정 모델을 세워 비용과 지연을 줄이겠다는 AI 플랫폼

<https://hanzo.ai/>

<https://github.com/hanzoai>

HN 토론: <https://news.ycombinator.com/item?id=50406105> (5점, 3개 댓글)

## 소개

Hanzo AI는 미국 회사 Hanzo AI, Inc.가 운영하는 플랫폼으로, 모델, 코딩 에이전트,
API 게이트웨이, 클라우드를 한 계정으로 묶어 판다.
회사는 자신을 AI 네이티브 회사 플랫폼, 곧 지능, 애플리케이션,
컴퓨터 사용 에이전트, 개발자 도구, MCP,
클라우드 인프라를 함께 설계한 수직 통합 에이전트 운영체제라고 소개한다.
내세우는 문장은 똑똑하고 빠르고 오픈소스인 세 가지를 모두 고를 수 있다는 것이고,
최전선 수준의 지능이 200배 빠르고 400배 싸다고 쓴다.

이 문서는 그 주장을 세 층에서 따져 본다.
첫째는 회사가 직접 말하는 내용이다.
둘째는 회사 문서와 가격표가 적은 구체적인 동작이다.
셋째는 GitHub의 `hanzoai` 조직에서 저장소 여덟 개를 내려받아 읽은 코드다.
코드는 읽기만 했고 실행하지 않았다.

### 한눈에 보는 제품 지도

Hanzo가 내놓는 것은 크게 다섯 갈래다.
모델 쪽에는 라우터 Enso, 결정 모델 Kai, 오픈 웨이트 모델 Zen이 있고,
이미지(Iro), 영상(Koma), 음향(Oto), 음성(Koe), 음악(Uta),
3D(Mori) 모델 이름도 나열한다.
에이전트 쪽에는 터미널 코딩 에이전트 Hanzo Dev, 명령줄 도구 Hanzo CLI,
메시징 채널에서 일하는 Hanzo Bot,
기존 에이전트에 Hanzo의 도구와 게이트웨이를 붙여 주는 하니스 Gen이 있다.
도구 쪽에는 MCP 서버가, 인프라 쪽에는 게이트웨이와 로컬 개발용 클라우드,
신원 서비스(IAM)가 있다.
설치는 `curl -fsSL https://hanzo.sh | sh` 한 줄이거나 `npm i -g hanzo`다.

## 모델 계층

### Enso: 모델 계열이라는 이름이지만 실제로는 모델 앞의 문지기다

Hanzo 문서는 Enso를 Hanzo 자체 모델 계열이라고 소개하면서,
무료 레인 하나와 유료 단계 셋이 있다고 설명한다.[^docs-enso]
유료 단계는 각각 하나의 id와 하나의 가격 아래 다른 회사의 최전선 모델을 정해진
순서로 이어 붙인 체인이다.[^docs-enso]
체인의 다음 모델은 앞 모델이 장애, 속도 제한, 거부로 실패할 때만 호출하고,
여러 모델에 동시에 보내 경쟁시키지 않는다.[^docs-enso]

| 단계       | 체인(순서대로)                                                | 입력 단가(100만 토큰당) | 출력 단가(100만 토큰당) |
| ---------- | ------------------------------------------------------------- | ----------------------- | ----------------------- |
| enso-flash | GPT-6 Luna, GPT-6 Luna Pro                                    | 0.33달러(약 449원)      | 1.65달러(약 2,246원)    |
| enso-pro   | GPT-6.1 Sol(중간 추론), Gemini 4 Argon, Claude Sonnet 5.5     | 3.30달러(약 4,493원)    | 16.50달러(약 22,463원)  |
| enso-ultra | Claude Sonnet 5.5(최대 추론), Claude Opus 5.5, Gemini 4 Argon | 5.236달러(약 7,128원)   | 26.18달러(약 35,642원)  |

환율은 1달러에 1,361.4원이다.[^fx]
이 표의 체인과 가격은 모두 Hanzo 문서에서 읽었다.[^docs-enso]

체인을 정한 근거도 문서에 적혀 있다.
체인은 Artificial Analysis의 Coding Agent Index(v1.5)라는 제3자 순위를 따랐고,
점수는 benchlm.ai가 2026-10-15에 수집한 것을 읽었으며 Hanzo가 직접 재지 않았다고
밝힌다.[^docs-enso]
그 순위에서 Claude Sonnet 5.5(최대 추론)가 68.4점, Claude Opus 5.5가 66.0점,
Gemini 4 Argon이 63.8점, GPT-6.1 Sol(최대 근처 추론)이 62.9점,
중간 추론이 61.4점, GPT-6 Luna가 41.1점이다.[^docs-enso]

같은 문서의 가격 비교는 눈여겨볼 만하다.
Hanzo 게이트웨이의 자체 목록에서 Claude Sonnet 5.5는 입력 2.11달러,
출력 10.55달러이고, enso-pro는 입력 3.30달러, 출력 16.50달러다.[^docs-enso]
문서는 enso-pro가 Sonnet 5.5보다 비싸고 Opus 5.5보다 싸다고,
enso-ultra가 Fable 5.1과 GPT-6 Astra보다 싸다고 직접 적는다.[^docs-enso]
같은 게이트웨이에서 enso-pro 체인의 마지막 칸이 Sonnet 5.5인데
단가는 그보다 56% 높다.

`enso-auto`가 단계를 고르는 방식도 문서에 있다.
유료 요금제에서 요청이 말한 추론 깊이(`reasoning_effort` 등)가 없거나 낮으면
enso-flash, 중간이나 높으면 enso-pro, 아주 높거나 최대면
enso-ultra로 보낸다.[^docs-enso]
추론 예산 토큰이 4,096 미만이면 낮음, 4,096에서 16,383이면 중간, 16,384 이상이면
최대로 읽는다.[^docs-enso]
무료 요금제는 어떤 요청도 유료 단계로 올려 주지 않고
오픈 모델 무료 레인에 남는다.[^docs-enso]

블로그는 Enso를 결과로 학습한 라우터라고 설명하고,
각 단계 아래의 라우팅은 학습된 것이라고 쓴다.[^blog]
`hanzoai/ai` 저장소의 라우팅 코드는 이 설명을 부분적으로만 뒷받침한다.
요청을 코드, 추론, 수학, 창작, 비전, 긴 문맥, 값싼 대화,
일반의 여덟 가지로 나누는 기본 분류기는 키워드, 길이,
미디어 유무로 판단하는 휴리스틱이다.[^repo-ai-router]
코드 주석은 이 분류기가 Rust 라우터의 휴리스틱을 그대로 옮긴 것이라고
적는다.[^repo-ai-router]
학습형 라우터는 `hanzo-engine`이 제공하는 선택 경로이고, 오류가 나면
휴리스틱으로 돌아가므로 추가 인프라 없이도 `auto`가 동작한다고
한다.[^repo-ai-router]
그 선택 경로는 사용자별 LinUCB 밴딧과 입실론 탐색을 쓰고,
보상 신호를 받아 학습하도록 쓰여 있다.[^repo-ai-client]
모든 요청은 프롬프트 본문 없이 작업 종류, 요청 모델,
응답 모델만 담은 라우팅 이벤트로 남을 수 있고,
사용자의 추천·비추천 피드백이 이 이벤트에 붙어 학습 신호가 된다.[^repo-ai-auto]

### Kai: 글을 쓰지 않는 결정 모델이다

Hanzo 문서가 설명하는 Kai는 생성 모델이 아니라 `POST /v1/decisions`로 부르는
결정 모델이다.[^docs-kai]
어느 팀, 어느 도구, 허용 또는 거부,
끝났는가 같은 답의 범위가 정해진 질문에 대해 글을 만들지 않고
선택지별 확률 분포를 돌려주며, 응답의 출력 토큰은 0이고
같은 입력은 같은 답을 준다고 한다.[^docs-kai]
구조는 mmBERT-base 인코더(22층, 폭 768,
어휘 256,000)를 질문과 선택지에 함께 쓰고,
선택지 토큰이 질문 상태에 주의를 주는 교차 어텐션 머리가 점수를 매기는
방식이다.[^docs-kai]
선택지가 160개를 넘으면 검색용 이중 인코더가 먼저 추린다.[^docs-kai]
확률은 질문 종류와 선택지 수에 따른 여섯 구간에서 온도로 보정한다.[^docs-kai]
CPU에서 순수 Rust로 서빙하며, 예/아니오 질문 하나는 운영 환경에서
서버 시간 38밀리초(p50)가 걸리고, 100개를 한 요청에 담으면 13.9초가 걸린다고
한다.[^docs-kai]
요금은 입력 100만 토큰당 0.021달러(약 29원)이고 출력은 무료다.[^docs-kai]

성능 표는 문서의 가장 구체적인 근거다.
고정된 12개 평가에서 Kai(kai-1)는 평균 정확도 0.857,
비교 대상인 Jev는 0.780이다.[^docs-kai]
Jev보다 11개에서 앞서고 jailbreak에서는 2.25점 뒤진다.[^docs-kai]
Kai의 보정 오차(ECE)는 12개 중 8개에서 Jev보다 낮다.[^docs-kai]
지원 분류(support triage)는 0.44, 독성(toxicity)은 0.8025,
RAG 관련성은 0.68로 낮은 편이다.[^docs-kai]
선택지가 많아지면 급격히 떨어져서 4개에서 0.9675, 150개에서 0.9075인데
1,000개에서는 0.005이고 10,000개 이상에서는 0이다.[^docs-kai]
문서는 Kai가 이 평가들의 학습 분할로 훈련되고 시험 분할에서 채점되었다고
밝힌다.[^docs-kai]

운영 상태에 대한 문서의 표기도 정직한 편이다.
평가한 kai-1과 운영 환경이 서빙하는 kai-1.2는 다르고,
kai-1.2는 예/아니오 판독기를 바꿨으며 하니스 결과가 게시되지 않았다고
쓴다.[^docs-kai]
가중치는 공개되지 않는다고 하고,
결정 프로그램(Decision Program)은 라이브러리로는 구현되었지만
와이어로는 서빙하지 않으며, Enso 안에 Kai를 넣는 일은 진행 중이라고
적는다.[^docs-kai]
블로그는 Gen이 Enso와 Kai를 에이전트에 엮어 준다고
쓰지만,[^blog] 문서는 Kai와 Enso의 통합이 아직 진행 중이라고 적는 것이다.

### Zen: Qwen을 바탕으로 한 오픈 웨이트 모델이다

Zen 문서는 Zen이 Zoo Labs Foundation이라는 비영리법인(501(c)(3))의 오픈 웨이트
모델 계열이고 Hanzo의 게이트웨이에서도 서빙한다고 설명한다.[^docs-zen]
zen6은 270억 파라미터 조밀(dense) 모델로 262,144 토큰을 기본으로,
YaRN으로 1,048,576 토큰까지 읽고, 카드가 DGX Spark 한 대에서
코드 완성 초당 141 토큰을 보고한다.[^docs-zen]
zen6-flash는 같은 세대를 3값(ternary) 가중치 5.95GB로 줄인 것이다.[^docs-zen]
출처 표기를 보면 zen6은 Qwen 팀의 Qwen3.8-27B에서 만들었고
Apache-2.0이다.[^docs-zen]
그러므로 Zen은 처음부터 훈련한 모델이 아니라 공개 모델의 파생물이다.
문서는 Zen이 쓰는 모델, Enso가 고르는 모델,
Kai가 결정하는 모델을 역할로 나누는 문장을 적는다.[^docs-zen]

## 에이전트 계층과 저장소

### 저장소 여덟 곳을 읽은 결과

`hanzoai` 조직의 공개 저장소는 GitHub 기준 560개다.
회사가 주요 저장소로 내세우는 여덟 곳(ai, dev, cli, engine, cloud, mcp, bot,
iam)을 골라 얕은 복제로 내려받아 구조와 출처 표기를 읽었다.

| 저장소 | 주된 구성                         | 파일 수 | GitHub 라이선스 판정 | 출처 표기(NOTICE)에 적힌 바탕                                   |
| ------ | --------------------------------- | ------- | -------------------- | --------------------------------------------------------------- |
| ai     | Go 979, JavaScript 218            | 1,261   | Apache-2.0           | Casibase(Casbin 계열, Apache-2.0)를 개명하고 변경한 것          |
| dev    | Python 72, Rust 43, TypeScript 28 | 320     | Apache-2.0           | OpenAI Codex, just-every/code 경유                              |
| cli    | Rust 73                           | 129     | 판별 불가            | Aider(Apache-2.0) 일부 포함                                     |
| engine | Rust 903, Python 143, CUDA 79     | 1,737   | MIT                  | mistral.rs에서 파생(MIT)                                        |
| cloud  | Go 99, Rust 7                     | 126     | 판별 불가            | 바탕 표기 없음, 저장소 설명은 Apache-2.0 또는 MIT 이중 라이선스 |
| mcp    | TypeScript 148, Rust 140, Go 9    | 362     | MIT                  | 명시된 바탕 없음                                                |
| bot    | TypeScript 5,598, Markdown 1,471  | 8,434   | Apache-2.0           | OpenClaw(구 Warelay, Clawdbot, Moltbot)의 MIT 코드              |
| iam    | Go 588                            | 610     | 판별 불가            | 현재 트리는 새로 쓴 것, 이전 트리는 Casdoor 계열                |

이 표의 출처 표기는 각 저장소의 `NOTICE`와 `LICENSE`에서
읽었다.[^repo-dev-notice][^repo-ai-notice][^repo-bot-notice][^repo-engine-notice][^repo-cli-notice][^repo-iam]
GitHub의 라이선스 판정은 저장소 메타데이터에서 읽었고
`판별 불가`는 `NOASSERTION`을 뜻한다.

파생 저장소를 두는 일 자체는 라이선스가 허락하는 범위 안에서 흔하고,
이 저장소들은 NOTICE에 바탕을 적어 두었다.
다만 `hanzoai/dev`의 NOTICE는 업스트림 프로젝트의 이름이 README, 저장소 설명,
CLI, TUI 어디에도 의도적으로 나타나지 않으며
그것이 가져온 모든 코드에 대한 집안 규칙이라고 적는다.[^repo-dev-notice]
회사와 README는 Hanzo Dev를 자사의 코딩 에이전트로 소개하고,
업스트림은 NOTICE에서만 찾을 수 있다.
`hanzoai/dev`의 `hanzo.yml`은 엔진이 `hanzoai/codex`이고
`upstream/codex`라는 서브모듈로 고정되어 있다고 적는다.[^repo-dev]
Hanzo가 직접 쓴 부분은 `crates/` 아래 네 개 크레이트(config, dev, kai, tui)이고,
그중 Kai 연동인 `hanzo-kai`가 21개 파일 13,065줄로 가장 크다.[^repo-dev]

### 코드로 확인한 동작

Kai는 Dev에서 기본으로 꺼져 있는 것에 가깝다.
`hanzo-config`의 Kai 설정 주석은 `kai.toml`이 없으면 Kai가 에이전트 루프에서
돌지 않고, 모든 작업(operation)의 기본 모드가 `shadow`, 곧 결정을 기록만 한다고
적는다.[^repo-dev-kai]
`advisory`는 결정을 보여 주고,
실제로 행동하는 `enforced` 모드는 더 엄격한 방향으로만 작동한다고
한다.[^repo-dev-kai]
`hanzo-kai`는 결정 프로그램 JSON 열 개(명령 위험도, 도구 선택, 컨텍스트 선택,
추론 예산, 모델 선택 등)를 갖추고, Kai가 응답하지 않으면
Dev가 Kai 없이 하던 대로 결정한다.[^repo-dev-kai]
블로그가 Dev는 Kai가 모든 단계를 결정하는 채로 돈다고 쓴 것과 달리,
코드의 기본값은 기록 모드다.[^blog]

라우터에는 비용 조절 장치가 있다.
품질 편향(bias) 값이 1 미만이면
요청의 비용 예산을 조직이 쓸 수 있는 모델 중 가장 싼 값과 가장 비싼 값 사이의
비율로 계산해 예산을 넘는 모델을 후보에서 뺀다.[^repo-ai-auto]
무료 요금제의 `auto`는 100만 토큰당 혼합 가격 3.00달러 이하의 모델 풀로
제한된다.[^repo-ai-auto]
이 상한은 환경 변수로 끌 수 있고,
결제 계층을 확신할 수 없을 때는 상한을 적용하지 않아 유료 사용자가 장애 때문에
낮은 풀로 내려가는 일을 피한다고 주석이 설명한다.[^repo-ai-auto]

`hanzoai/cloud`는 이름과 달리 운영 클라우드가 아니라 로컬 개발 서버다.
README는 Go 바이너리 하나가 문서 저장소, 키-값 저장소, SQL, 작업 큐, 함수, 비밀,
오브젝트 스토리지, 코드 검색, 게이트웨이 엣지, 기능 플래그, 감사를 한 머신에서
돌리는 오픈소스 로컬 개발 서버라고 설명한다.[^repo-cloud]
저장소는 SQLCipher로 저장 시 암호화하지만
현재는 순수 Go SQLite 백엔드만 가능하고, 기본 cgo 빌드는 키가 있으면
시작을 거부한다고 적는다.[^repo-cloud]

`hanzoai/mcp`의 README는 260개 이상의 기능을 행동 라우팅 도구로 묶었다고
쓰는데,[^repo-mcp] Rust 쪽 `catalog.json`의 최상위 항목은 124개다.
어느 수가 맞는지는 이 문서에서 가리지 못했다.

`hanzoai/iam`은 새로 쓴 신원 서비스로, OIDC, OAuth2(PKCE 포함),
토큰 교환(RFC 8693), SCIM 2.0, MFA와 WebAuthn을 표준 경로만으로 제공한다고
README가 적는다.[^repo-iam]
같은 README는 이전 Casdoor 계열 트리를 `hanzoai/iam-v1`로 옮겨
보관(archive)했다고 적고, `go.mod`는 Go 프록시가 이미 506개 버전을 불변으로
캐시했으므로 v1.0.0부터 v1.31.37까지를 철회(retract)한다고
주석으로 설명한다.[^repo-iam]
같은 모듈 경로에서 계보가 바뀐 만큼 의존하는 쪽의 오해를 막으려는 정리로 읽힌다.

### 저장소 활동 수치는 GitHub에서 확인한 값과 맞지 않는다

회사는 주요 저장소마다 올해 커밋 수를 내세운다.
`hanzoai/cloud`는 39,305건에 기여자 1명,
`hanzoai/bot`은 113,788건에 기여자 349명이다.
GitHub API로 두 저장소의 커밋 목록을 쪽당 1건으로 조회하면
마지막 쪽 번호가 cloud 125, bot 34,678이다.[^repo-cloud][^repo-bot]
올해만의 커밋이 전체 커밋보다 많을 수는 없으므로 두 값은 같은 것을 세지 않는다.
`cloud`의 기여자 목록 최상단은 한 사람이고 그의 기여가 82건이다.

같은 1년 구간(2025-11-08부터 2026-11-07까지)의 총계도 두 곳이 다르다.
회사의 첫 소개는 커밋 803,822건, 123개 조직의 원본 저장소 2,248개, 스타 6,046개,
포크 4,579개를 쓴다.
투자자 소개는 커밋 730,986건, 73개 조직의 원본 저장소 1,734개, 스타 5,130개,
포크 3,617개를 쓴다.[^investors]
회사가 말하는 1,700개 이상의 공개 저장소는 여러 조직의 합계다.[^about]
개별 저장소의 스타는 3개에서 20개 사이다.

## 가격과 사용 방법

가격표는 개인용 세 단계를 둔다.[^pricing]

| 요금제 | 월 요금 | 원화 환산   | 포함 내용                                        |
| ------ | ------- | ----------- | ------------------------------------------------ |
| Free   | 0달러   | 0원         | 웹 채팅, Enso Auto, 무료 모델 요청과 Kai 결정    |
| Go     | 8달러   | 약 10,891원 | Hanzo Dev, CLI, 모든 모델, 우선 추론, 자동화     |
| Pro    | 15달러  | 약 20,421원 | Go의 3배 사용량, 봇 1개, 모델 학습, Hanzo Engine |

비용을 가늠하려고 문서의 예시를 따랐다.
코딩 에이전트의 한 턴을 프롬프트 100,000토큰(캐시 읽기 92,000, 새로 쓰는 6,000,
일반 입력 2,000)과 답변 2,000토큰으로 놓으면,
문서의 계산은 enso-flash 0.0095달러(약 13원), enso-pro 0.0795달러(약 108원),
enso-ultra 0.1262달러(약 172원)다.[^docs-enso]
캐시를 쓰지 않으면 같은 턴이 enso-pro에서
0.363달러(약 494원)로 4.6배 든다.[^docs-enso]
절감의 큰 부분은 라우팅이 아니라 프롬프트 캐시에서 나온다는 뜻이다.

Kai의 단가로 같은 규모를 어림해 보면 차이가 크다.
하루에 결정 1만 건, 건당 입력 2,000토큰이면 입력 2,000만 토큰이고
Kai는 약 0.42달러(약 572원)다.
같은 입력을 입력 단가 11.13달러짜리 Claude Fable 5.1로 처리하면
입력만 약 222.6달러(약 303,048원)다.
이 어림은 두 모델의 결정 품질이 같다는 가정이 필요하고,
그 가정은 확인되지 않았다.

Hanzo Dev는 `hanzo auth login`으로 신원 서비스에 로그인하고
`hanzo dev`로 시작한다.[^repo-dev-readme]
모델 호출은 기본으로 `api.hanzo.ai`를 거쳐 계정에 청구되고, `--no-route`를 주면
백엔드 자체 계정으로 보낸다.[^repo-dev-readme]
세션은 샌드박스 안에서 자동 승인으로 돌고, `--ask`로 매번 묻게 하며
`--no-sandbox`는 샌드박스와 승인 절차를 함께 없앤다.[^repo-dev-readme]
저장소가 가진 `.mcp.json` 서버는 기본으로 불러오지 않는데,
방금 내려받은 저장소가 세션의 키로 서버를 실행하면 안 되기 때문이라고
README가 설명한다.[^repo-dev-readme]
`hanzo dev claude`나 `hanzo dev codex`로 설치된 다른 에이전트를 같은 실행기로
구동할 수도 있다.[^repo-dev-readme]

에이전트가 스스로 가입하는 경로도 회사가 소개한다.
지갑 서명으로 가입하고 API 키를 받아 USDC나 카드로 충전해 쓰는 네 단계를 사람
없이 진행할 수 있다고 보여 준다.

## 회사가 내세우는 측정 결과와 그 조건

아래 수치는 모두 Hanzo가 직접 잰 값이라고 회사가 밝힌 것이다.

| 주장                                    | 조건                                                                                                      | 잰 주체           |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------- | ----------------- |
| Hanzo Dev가 Claude Code보다 3.02배 빠름 | 두 에이전트가 모두 푼 42개 과제, 95% 구간 2.06~4.36배, 중앙값 2.29초 대 9.52초                            | Hanzo             |
| 검색만으로 풀린 과제에서 8.22배         | 모델 호출 없는 24개 과제                                                                                  | Hanzo             |
| Kai가 LLM 호출보다 9.6배 빠름           | 클라이언트 p50, 네트워크 포함, LLM 650회 대 Kai 100회, 대상은 Claude Sonnet 5.5                           | Hanzo             |
| Enso Flash가 문항당 비용 14.2배 적음    | GPQA Diamond 새 문제, 90.6%를 3.26달러(약 4,438원)에, Claude Fable 5.1은 87.9%를 46.25달러(약 62,965원)에 | Hanzo             |
| Enso가 가장 좋은 단일 모델을 앞섬       | 93.7%(10.03달러, 약 13,655원) 대 93.1%                                                                    | Hanzo             |
| Enso Ultra 95.6%                        | GPQA Diamond 새 문제 159개 중 152개                                                                       | Hanzo[^investors] |
| Enso LiveCodeBench 93.7%                | 최근 문제 175개 중 164개, 2026-07-19 측정                                                                 | Hanzo[^investors] |
| Kai가 입력 토큰 기준 최대 530배 쌈      | 출력은 청구하지 않고 입력만 청구, 비교는 Claude Fable 5.1 입력 단가                                       | Hanzo             |

Kai의 응답 시간은 회사의 첫 소개, 블로그, 문서에서 서로 다르게 나온다.
첫 소개는 `api.hanzo.ai`에서 241밀리초, GPU 한 대에서
네트워크 없이 같은 입력을 반복하면 0.8밀리초라고 쓴다.
블로그는 GPU에서 0.27밀리초(p50)라고 쓰고,[^blog] 문서는 운영 환경 CPU에서
예/아니오 질문 하나에 서버 시간 38밀리초라고 쓴다.[^docs-kai]
세 수치는 서로 다른 조건에서 잰 것이어서 모순은 아니다.
네트워크를 포함한 값은 241밀리초이고,
0.8밀리초와 0.27밀리초는 네트워크 없는 GPU 값이다.

## 회사 구조와 보안 문서

회사는 CEO 겸 공동 창업자 Antje Worring과 CTO 겸 창업자 Zach Kelling을
내세운다.[^about]
역사는 SKULLY와 오픈소스 커머스에서 Techstars '17을 거쳐 현재에 이른다고 적고,
스타트업 100곳 이상을 만들고 지원했으며 고객 매출 10억 달러 이상을 만들었고
두 곳이 2024년 Nasdaq에 상장했다고 쓴다.[^about]
투자자 소개는 투자자가 지주회사 Hanzo Industries Inc.에 투자하고,
이 회사가 AI 지식재산과 앱을 가진 Hanzo AI, Inc.의 지분 51%를 가진다고 밝힌다.
지주회사는 비상장이며 재무제표를 공개하지 않고 정보 요청은 사안별로 답한다고
한다.[^investors]

보안 문서는 조직마다 별도 데이터베이스 파일을 쓰고, 마스터 키가 있으면
HKDF-SHA256으로 파일별 키를 유도하며,
전송 구간은 TLS 1.3과 하이브리드 ML-KEM-768 키 교환을 제공한다고
적는다.[^security]
게이트웨이는 조직, 사용자, 이메일을 사칭하는 입력을 모두 지우고
검증된 토큰에서만 신원을 다시 쓴다고 한다.[^security]
신뢰 문서는 데이터 처리 부속서(DPA)를 공개하되 변호사 검토 전의 초안임을 맨 위에
적는다고 밝히고, 감사는 스스로 계속 하며 보고서는 요청하면 보낸다고
쓴다.[^trust]
하위 처리자 목록에서는 공급사 약관으로 확인이 끝나지 않은 항목을 확인 중으로
표시한다.[^trust]

## 분석

### 비용을 줄이는 길은 두 가지이고 서로 다른 비용을 건드린다

블로그의 논리는 단순하다.
모든 모델은 더 좋은 답이 더 비싸고 느린 곡선 위에 있고,
코딩 에이전트는 모든 단계에서 그 곡선의 비용을 낸다.
파일 읽기, 도구 고르기, 테스트 통과 판단 같은 대부분의 단계는 곡선의 꼭대기까지
필요하지 않다.[^blog]
곡선을 옮기려면 요청마다 필요한 모델에 보내고,
결정으로 충분한 곳에서는 글 생성을 멈추면 된다는 것이다.[^blog]

Enso는 앞쪽 절반, 곧 요청당 모델 가격을 줄이고 Kai는 뒤쪽 절반,
곧 출력 토큰 자체를 없앤다.
회사는 이 둘을 곡선 이동이라는 한 문장으로 묶지만,
건드리는 비용 항목이 다르므로 따로 평가해야 한다.
코드를 읽고 나면 구현 상태도 다르다.
Enso의 단계 체인과 가격은 문서와 코드에서 운영 중이고,
Kai의 에이전트 연동은 기본이 기록 모드이며 Enso와의 통합은 진행 중이다.

### 배수는 서로 다른 양을 재고 있다

회사가 내놓는 배수는 하나의 기준이 아니다.
Hanzo Dev 3.02배는 두 에이전트가 모두 푼 과제의 시간 비율이다.
Kai 9.6배는 결정 모델과 텍스트 생성 모델의 응답 시간 비율이다.
Enso의 14.2배는 문항당 비용 비율이고 Kai의 530배는 입력 토큰 단가 비율이다.
각 배수가 재는 양(시간, 비용), 비교 대상(에이전트, 모델 호출),
입력 범위(두 쪽이 모두 푼 과제, 입력 토큰만)가 모두 다르다.

그래서 한 제품이 200배 빠르고 400배 싸다는 문장은 이 중 큰 배수들을 가져다 쓴
것으로 읽어야 한다.
투자자 소개가 같은 문구를 직접 결정에 한정해 최대 200배 빠르다, 측정한 일에서
최대 400배 싸다고 쓰는 것이 그 증거다.[^investors]

### 하니스 전략은 남의 에이전트와 남의 모델 위에 올라타는 구조다

Gen은 Claude Code, Codex, Cursor 같은 다른 회사의 에이전트를 그대로 쓰게 하고
그 모델 호출만 자사 게이트웨이로 돌린다.[^blog]
Enso 체인의 모델도 대부분 다른 회사의 것이다.
사용자는 에이전트와 작업 방식을 바꾸지 않고 비용만 줄이는 경험을 얻고,
회사에는 사용자 호출이 모두 지나가는 위치가 생긴다.
이 위치는 라우팅 이벤트 같은 학습 신호를 모을 수 있는 자리이기도 하다.

이 구조에서 Hanzo의 절감 폭은 체인에 든 모델의 가격과 접근 조건에 영향을 받는다.
회사가 직접 서빙하는 Zen과 Kai의 비중이 늘어야 그 의존이 줄어든다.

## 비평

### 헤드라인의 배수는 조건을 뗀 채 쓰였다

첫 화면의 문구는 최전선 수준의 지능이 200배 빠르고 400배 싸다고 쓴다.
같은 페이지의 근거 그래프에서 이 말이 성립하는 구간은 좁다.
Kai는 지능이 아니라 결정을 내리는 모델이고,
530배는 입력 토큰 단가만 비교한 값이며, Enso의 비용 이점은 최대 14.2배다.
이를 합쳐 최전선 지능이라는 하나의 명사에 붙이는 것은 독자가 각 배수의 조건을
읽지 않으리라는 가정에 기댄다.

### Enso의 가격 우위는 같은 게이트웨이의 가격표와도 맞지 않는다

문서의 비교표에서 enso-pro는 Claude Sonnet 5.5보다 입력과 출력 모두
비싸다.[^docs-enso]
enso-pro 체인의 첫 모델은 GPT-6.1 Sol이고 마지막이 Sonnet 5.5인데,
두 모델의 가격은 이 표에 없다.
블로그가 말하는 모델 호출당 가장 싼 모델로 보내는 라우터라는 설명과 달리,
코드와 문서가 그리는 enso-pro는 정해진 순서의 장애 대체 체인이고
단계 선택은 요청이 밝힌 추론 깊이에 따른 규칙이다.[^docs-enso]
호출마다 정답률을 예측해 고르는 학습형 라우터는 `hanzo-engine`의 선택 경로로
존재하지만 기본이 아니며, 그것이 운영 중인 Enso 단계를 구동하는지는 이 문서가
확인하지 못했다.[^repo-ai-router]

### 평가는 회사가 설계하고 회사가 채점했다

Enso의 LiveCodeBench 93.7%는 회사의 `enso-bench`가 2026-07-19에 175문항으로 잰
값이다.[^investors]
Zen 6의 초당 약 3,665 프롬프트 토큰도 Hanzo가 2026-11-04에 잰
값이다.[^investors]
GPQA Diamond는 198문항인데 Enso Ultra는 새 문제 159개 중 152개를 맞혔다고 하여,
어떤 문제가 새 것인지와 나머지를 왜 뺐는지 설명이 없다.
Hanzo Dev 대 Claude Code는 두 쪽이 모두 푼 42개 과제만 비교하므로 한쪽만 푼
과제는 통계에서 빠진다.
과제 목록, 하니스 버전, 반복 횟수를 회사는 밝히지 않았다.

Kai의 12개 평가도 같은 한계를 가진다.
Kai는 평가의 학습 분할로 훈련되었고,
비교 대상 Laya는 일부 평가의 행으로 훈련되었음을 문서가 인정한다.[^docs-kai]
문서는 보류된 행에 대한 비교는 하지 않았다고 쓴다.[^docs-kai]
정직한 표기이지만, 평균 정확도 0.857 대 0.780이 새 데이터에서도 유지되는지는 알
수 없다.

### 저장소의 숫자와 출처 표기가 홍보 문장과 어긋난다

앞에서 본 대로 회사가 내세운 올해 커밋 수는 GitHub의 전체 커밋 수보다 크다.
같은 1년의 총계도 회사의 첫 소개와 투자자 소개가 다르다.
회사는 스택의 모든 층이 열려 있고 고칠 수 있다고 쓰는데,
같은 사이트의 `hanzoai/iam` 저장소 카드는 이를 독점(proprietary) 신원 서비스라고
설명한다.
저장소 자체는 README 배지와 `LICENSE-MIT`,
`LICENSE-APACHE` 파일로 MIT 또는 Apache-2.0을 표시하므로,
카드의 설명과 저장소의 표시가 서로 다르다.[^repo-iam]
파생 저장소를 NOTICE에 정확히 적은 것은 라이선스 의무를 지킨 것이지만,
제품 소개에는 그 바탕이 보이지 않는다.
회사가 밑바닥부터 재귀적으로 스스로 개선하는 AI라고
말하는 것과 저장소가 보여 주는 계보는 같은 이야기가 아니다.

### 개발자에게 보낸 영입 메일이 신뢰 문제를 낳았다

2026-11-07 HN에는 Hanzo AI가 GitHub 기여 기록에서
얻은 주소로 베타 초대 메일을 보냈다는 글이 올라왔다.[^hn-thread]
글쓴이는 받은 메일의 본문을 옮기며
자신이 해당 저장소에 10년 넘게 참여하지 않았다고 적는다.[^hn-thread]
한 댓글 작성자는 같은 메일이 스팸 폴더에 들어 있었고
수신 거부 링크가 작동하지 않았다고 적었다.[^jonathanlydall]
다른 댓글 작성자는 이 회사를 조사한 글의 링크를 달았다.[^zoontripanto]
그 글의 작성자는 자신의 주소가 자기 사이트 어디에도 없었는데 GitHub 데이터에서
뽑아 광고에 썼다고 주장하고, 회사의 설립 연도와 주소가 자료마다 다르다고
주장한다.[^ende]
이 주장들은 이 문서가 검증하지 못했고 회사의 답변도 확인하지 못했다.
다만 개발자 신뢰가 핵심인 제품이 에이전트를 사용자의 컴퓨터와 코드에 연결한다는
점에서, 수신 동의 없는 대량 메일이 사실이라면 도입 판단의 변수가 된다.

## 인사이트

### 중개 모델의 이득은 공급 가격과 접근 조건에 매여 있다

Enso는 자체 모델이 아니라 여러 회사 모델 앞에 서는 문지기다.
통신망을 빌려 파는 재판매 사업자의 이윤이 망 사업자의 도매 가격에 묶이는 것과
같은 구조다.
상위 모델이 가격을 내리면 체인의 절감 폭이 줄고, 접근 조건을 바꾸면
체인 자체가 바뀐다.
이 비유는 구조를 설명하는 것이며,
Hanzo가 공급사와 맺은 계약은 이 문서가 확인하지 못했다.

절감이 이어지려면 둘 중 하나가 필요하다.
단계 선택이 규칙에서 학습으로 옮겨 가거나,
자체 모델 Zen과 Kai가 상위 모델의 일을 더 많이 대신해야 한다.
라우팅 이벤트를 모으고 사용자 피드백을 보상으로 쓰는 코드는 앞의 길을 준비한다.
그 학습 데이터가 무엇이고 누구의 것인지가 곧 개인정보 질문으로 이어진다.

### 확률 모델에 허용 판정을 맡기면 결정적 검증이라는 말과 부딪친다

회사는 소개 글에서 생성 모델이 방치되면 표류하고
환각을 일으키므로 결정적 검증이 필요하다고 쓴다.[^about]
Kai는 선택지마다 확률을 주는 모델이고,
문서의 명령 위험도 프로그램은 쉘 명령을 허용, 질문, 거부로 가른다.[^docs-kai]
문서의 예에서 비밀 키를 외부로 보내는 명령에 대해 거부 판정의 확률이 0.4276으로
임계값 0.5를 넘지 못해 판정은 채택되지 않았고,
비밀 노출과 네트워크 질문의 임계값이 낮아서 거부로 끌어올려졌다.[^docs-kai]
결정적 정책이 확률을 감싸는 설계이고, 이것이 설계의 핵심 방어선이다.

이 구조의 위험은 임계값이 검증된 보정 표와 짝으로만 유효하다는 점이다.
문서는 프로그램이 검증된 보정과 다른 보정 아래에서 답을 받으면
`shadow`로 돌아간다고 적는데, 지금 서빙되는 kai-1.2의 보정은 프로그램이 검증된
것과 달라 프로그램이 기록 모드로 돈다.[^docs-kai]
즉 지금 이 가드는 막지 않고 기록한다.
에이전트 보안 가드로 쓰려면 이 상태가 바뀐 뒤의 오탐과 미탐 수치가 있어야 한다.

### 도입 전 시험은 토큰이 아니라 수락된 과제당 비용으로 한다

비용 주장을 확인하는 가장 작은 시험은 자신의 과제를 같은 에이전트에서
직접 호출과 Hanzo 경유로 나눠 돌리는 것이다.
측정 단위는 토큰이나 문항이 아니라 리뷰를 통과한 변경 하나당 비용과 시간이다.
이점이 있어도 재시도가 늘거나 리뷰 통과율이 떨어지면
수락된 과제당 비용은 오히려 오를 수 있다.
문서의 계산에서 캐시 여부가 4.6배를 갈랐으므로,
캐시를 살린 직접 호출이 비교 기준이어야 한다.

데이터 경로도 시험 항목이다.
Gen이나 Dev의 기본 경로에서 모든 모델 호출이 `api.hanzo.ai`를 지나가고,
신뢰 문서의 DPA는 초안이다.[^trust]
기밀 코드를 보내기 전에 하위 처리자 목록에서
호출이 닿는 모델 제공자와 학습 사용 여부를 확인해야 한다.
`--no-route`와 샌드박스 옵션으로 경로와 권한을 좁힐 수 있는지도 함께 확인한다.
에이전트가 지갑으로 스스로 가입하고 충전하는 경로가 있으므로,
결제 한도와 키 발급 권한을 사람이 정해 두는 절차도 필요하다.

다음 관찰이 나오면 결론이 바뀐다.
수락 과제당 비용이 직접 호출보다 높거나, 하위 처리자가 학습에 쓸 수 있다고
표시되면 도입 판단이 달라진다.
Kai가 `enforced` 모드로 서빙되고 오탐률이 공개되면
에이전트 가드로서의 평가가 달라진다.
영입 메일 의혹에 대한 회사의 공식 답변이 나오면 신뢰 평가가 달라진다.

---

[^docs-enso]: Hanzo, [Enso | Hanzo Docs](https://docs.hanzo.ai/docs/models/enso), 2026-11-09

[^docs-kai]: Hanzo, [Kai | Hanzo Docs](https://docs.hanzo.ai/docs/models/kai), 2026-11-09

[^docs-zen]: Hanzo, [Zen | Hanzo Docs](https://docs.hanzo.ai/docs/models/zen), 2026-11-09

[^blog]: Hanzo AI, [A New Pareto Frontier — Hanzo AI](https://hanzo.ai/blog/pareto-frontier), 2026-10-18

[^pricing]: Hanzo AI, [Pricing — start free, every model on one bill — Hanzo AI](https://hanzo.ai/pricing), 2026-11-09

[^investors]: Hanzo AI, [Hanzo Investor Relations — Hanzo AI](https://hanzo.ai/investors), 2026-11-09

[^about]: Hanzo AI, [Chasing the Pareto Frontier of AI — Hanzo AI — Hanzo AI](https://hanzo.ai/about), 2026-11-09

[^security]: Hanzo AI, [What protects your data, and how. — Hanzo AI](https://hanzo.ai/security), 2026-11-09

[^trust]: Hanzo AI, [Security you can read — Hanzo AI](https://hanzo.ai/trust), 2026-11-09

[^repo-ai-router]: GitHub, [hanzoai/ai router/classify.go](https://github.com/hanzoai/ai/blob/main/router/classify.go), 2026-11-09

[^repo-ai-client]: GitHub, [hanzoai/ai router/client.go](https://github.com/hanzoai/ai/blob/main/router/client.go), 2026-11-09

[^repo-ai-auto]: GitHub, [hanzoai/ai controllers/auto_route.go](https://github.com/hanzoai/ai/blob/main/controllers/auto_route.go), 2026-11-09

[^repo-ai-notice]: GitHub, [hanzoai/ai NOTICE](https://github.com/hanzoai/ai/blob/main/NOTICE), 2026-11-09

[^repo-dev]: GitHub, [hanzoai/dev hanzo.yml](https://github.com/hanzoai/dev/blob/main/hanzo.yml), 2026-11-09

[^repo-dev-kai]: GitHub, [hanzoai/dev crates/hanzo-config/src/kai.rs](https://github.com/hanzoai/dev/blob/main/crates/hanzo-config/src/kai.rs), 2026-11-09

[^repo-dev-notice]: GitHub, [hanzoai/dev NOTICE](https://github.com/hanzoai/dev/blob/main/NOTICE), 2026-11-09

[^repo-dev-readme]: GitHub, [hanzoai/dev README](https://github.com/hanzoai/dev/blob/main/README.md), 2026-11-09

[^repo-bot]: GitHub, [hanzoai/bot](https://github.com/hanzoai/bot), 2026-11-09

[^repo-bot-notice]: GitHub, [hanzoai/bot NOTICE](https://github.com/hanzoai/bot/blob/main/NOTICE), 2026-11-09

[^repo-engine-notice]: GitHub, [hanzoai/engine NOTICE](https://github.com/hanzoai/engine/blob/main/NOTICE), 2026-11-09

[^repo-cli-notice]: GitHub, [hanzoai/cli NOTICE](https://github.com/hanzoai/cli/blob/main/NOTICE), 2026-11-09

[^repo-cloud]: GitHub, [hanzoai/cloud](https://github.com/hanzoai/cloud), 2026-11-09

[^repo-mcp]: GitHub, [hanzoai/mcp README](https://github.com/hanzoai/mcp/blob/main/README.md), 2026-11-09

[^repo-iam]: GitHub, [hanzoai/iam README](https://github.com/hanzoai/iam/blob/main/README.md), 2026-11-09

[^hn-thread]: Hacker News, [Tell HN: Hanzo AI Is Spamming From GitHub Contributions](https://news.ycombinator.com/item?id=50406105), 2026-11-07

[^ende]: ende.app, [Warning about Hanzo AI: Why you shouldn't let this AI onto your computer](https://ende.app/en/blog/7-warning-about-hanzo-ai-why-you-shouldnt-let-this-ai-onto-your-computer), 2026-11-07

[^jonathanlydall]: <https://news.ycombinator.com/item?id=50411634>

[^zoontripanto]: <https://news.ycombinator.com/item?id=50409079>

[^fx]: ExchangeRate-API, [USD 기준 환율 조회](https://open.er-api.com/v6/latest/USD), 2026-11-09
