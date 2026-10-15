# Aside 브라우저를 Claude Code와 함께 쓰면 무엇이 달라지나

## 소개

Aside는 사람과 AI 에이전트가 함께 쓰도록 다시 만든 Chromium 기반 브라우저다.
로그인된 계정 안에서 사이트를 직접 열고 클릭하며,
메시지, 결제, 사내 도구, 로컬 파일까지 다루는 작업을 맡는다고 소개한다.[^ph]
macOS와 Windows를 지원하고,
Claude나 ChatGPT 구독을 연결하거나 API 키를 쓸 수 있다.[^ai]
Product Hunt 소개 페이지는 Y Combinator가 투자한 회사라고 적는다.[^ph]

이 문서는 Claude Code 옆에 Aside를 붙였을 때 실제로 무엇이 가능해지는지,
특히 Claude Code와 Claude in Chrome이 하지 않는
일을 Aside가 대신 해 줄 수 있는지를 조사한 기록이다.
결론부터 말하면,
로그인이 필요한 페이지에서 증거를 가져오는 일은 확실히 쉬워진다.
가치를 가르는 것은 연결 방식이다.
MCP로 단계를 조종하면 판단이 Claude Code에 남고,
CLI로 목표를 넘기면 판단이 Aside의 에이전트와 사용자 권한 설정으로 옮겨 간다.
그러나 Aside도 CAPTCHA, MFA, 본인 확인, 결제·게시·메시지 같은 민감한 동작에서는
사람의 손을 요구하므로 “제약 없이 다 해 주는” 도구는 아니다.

## 핵심: 목표를 Aside에 넘기는 CLI 위임

Claude Code와 Aside를 잇는 길은 셋이다.[^dev]
어느 길을 고르느냐가 이 조합의 가치를 거의 전부 결정한다.
핵심은 브라우저 안에서 “할지 말지”를 누가 판단하느냐다.

| 방식                | Claude Code가 하는 일                    | 판단하는 쪽        | 이 문서의 목적에 맞는가 |
| ------------------- | ---------------------------------------- | ------------------ | ----------------------- |
| CLI 작업 위임       | 목표와 제약을 글로 적어 `aside`에 넘긴다 | Aside의 에이전트   | 그렇다. 이 문서의 중심  |
| MCP (`aside mcp`)   | 브라우저 조작 단계를 하나씩 보낸다       | Claude Code의 모델 | 아니다                  |
| REPL (`aside repl`) | 결정적인 스크립트를 보낸다               | 스크립트를 쓴 쪽   | 보조 수단               |

이 절은 가장 강력한 길인 CLI 위임을 처음부터 끝까지 다룬다.
MCP와 REPL은 뒤의 「다른 연결 방식」에서 짧게 비교한다.

### 왜 목표 위임이 가장 강력한가

`aside "<목표>"`는 브라우저 작업 하나를
Aside의 에이전트 세션으로 시작한다.[^dev]
이때 Claude Code는 셸 명령 하나를 실행할 뿐이고,
어떤 페이지를 열고 어떻게 로그인하고 무엇을
클릭할지는 Aside의 에이전트가 정한다.
Claude Code가 “이 사이트에서는 못 한다”고 결론 내릴 단계 자체가 없어진다.

목표 위임이 다른 두 방식보다 나은 이유는 네 가지다.

1. 판단의 자리가 옮겨 간다.
   브라우저 안의 판단은 Aside의 에이전트와
   사용자가 정한 권한 설정이 맡는다.[^security]
2. 로그인이 막히지 않는다.
   Aside Vault가 저장된 로그인을 채우고,
   모델은 비밀번호 값을 받지 않는다.[^vault]
3. 긴 작업이 한 번에 끝난다.
   한 작업 안에서 여러 단계를 이어 가고,
   입력을 기다리거나 승인을 요청한 뒤 다시 이어 갈 수 있다.[^tasks]
4. 모델을 고를 수 있다.
   Aside 안에서 움직이는 모델을 작업마다 바꿀 수 있어,
   모델 단의 거절도 제공자를 바꿔 피해 갈 여지가 있다.[^ai]

### 위임 한 번의 흐름

```text
사용자 ──요청──▶ Claude Code
                  │ 목표·결과물·저장 위치·금지 동작·승인 대상·기록 파일 정리
                  ▼
               aside "<목표>"  ──▶ Aside 에이전트 ──▶ 로그인(Vault), 탐색, 내려받기
                  ▲                     │             진행 기록을 마크다운에 남김
                  │                     ├─ 승인·입력 필요 ──▶ 사용자(Aside 화면 또는 aside-relay)
                  └── 결과·세션 ID ◀────┘
Claude Code: 결과와 기록 파일을 읽고 다음 판단(코드 수정, 요약, 다음 aside 작업)
```

```bash
# 1. 목표를 넘긴다. 결과와 세션 ID가 돌아온다.
aside "Sign in to the vendor portal, download last quarter's invoices,
save them to ~/Downloads/invoices named by date and vendor.
Do not change any settings. Ask before any payment."

# 2. 같은 세션을 이어 간다.
aside --session <session-id> "Also export the summary table as CSV."

# 3. 작업을 맡길 모델을 고른다.
aside exec -m openai-codex/gpt-5.5 "Plan this workflow"

# 4. 여러 Aside 계정을 쓰면 계정을 고른다.
aside --account u1 "Summarize the current page"
```

`--session`, `exec -m`, `--account`는 공식 문서의 예다.[^dev]

### 목표 지시문 쓰는 법

위임의 품질은 지시문이 거의 전부 정한다.
Aside 문서는 “Handle my billing.” 같은 막연한 지시 대신
계정, 산출물, 목적지, 피해야 할 동작을 적으라고 권하고,
돈, 고객 데이터, 자격 증명, 파일을 다루는 작업에는 제약을 덧붙이라고 한다.[^tasks]
문서가 드는 좋은 예는
Rippling에 로그인해 이번 달 급여 명세서 PDF를 Downloads에 저장하되,
MFA나 인증 코드가 필요하면 물어보라는 지시다.[^tasks]

이를 Claude Code가 매번 채우는 틀로 정리하면 다음과 같다.

| 항목      | 적을 내용                        | 빠지면 생기는 일                       |
| --------- | -------------------------------- | -------------------------------------- |
| 대상      | 사이트와 계정                    | 엉뚱한 계정이나 사이트에서 일한다      |
| 결과물    | 파일 형식, 이름 규칙, 범위(기간) | 무엇을 끝으로 볼지 Aside가 추측한다    |
| 저장 위치 | 작업 폴더 안의 경로              | Guard 모드에서 폴더 승인을 다시 묻는다 |
| 금지 동작 | 설정 변경, 삭제, 송금 등         | 목표를 이루려고 부수 동작을 한다       |
| 승인 대상 | 결제, 게시, 메시지, 주문         | 승인 없이 지나칠 동작이 생긴다         |
| 진행 기록 | 기록 파일 경로와 남길 항목       | 무엇을 했는지 결과만 보고 추측한다     |
| 막혔을 때 | MFA, CAPTCHA, 화면 변경 시 할 일 | 임의로 우회하거나 조용히 실패한다      |

한 번에 끝내기 어려운 작업은 목표를 쪼개 같은 세션으로 이어 보낸다.
첫 지시로 로그인과 목록 확인까지만 하고,
돌아온 결과를 Claude Code가 읽은 뒤
`--session`으로 다음 단계를 보내는 식이다.[^dev]
판단은 여전히 Aside가 하지만,
Claude Code가 중간 결과를 보고 다음 목표를 고칠 기회가 생긴다.

Aside 문서의 예시 지시문에는 공통된 말버릇이 하나 있다.
되돌리기 어려운 동작 바로 앞에서 멈추라고 적는 것이다.
청구서를 모으되 결제 설정을 바꾸기 전에 멈추라거나,
미팅 답장 초안을 쓰되 보내기 전에 멈추라거나,
대시보드에서 Linear 작업 초안을 만들되 실제로 생성하기 전에 멈추라는 식이다.[^sidepanel]
“무엇을 하지 마라”보다 “어디까지 하고 멈춰라”가
에이전트가 지킬 경계를 더 분명하게 그어 준다.
Claude Code가 지시문을 만들 때도 마지막 줄을 `Stop before ...`로 끝내게 하면 된다.

| 작업 종류      | 지시문 끝에 붙일 멈춤 지점            |
| -------------- | ------------------------------------- |
| 청구서·명세서  | 결제·청구 설정을 바꾸기 전에 멈춘다   |
| 답장·메시지    | 보내기 전에 멈추고 초안만 남긴다      |
| 이슈·작업 생성 | 생성하기 전에 멈추고 목록만 남긴다    |
| 금융 계좌 조회 | 송금·주문 화면에 들어가기 전에 멈춘다 |

### 여러 출처를 비교하는 조사는 Ultrabrowse로

여러 사이트를 오가며 출처를 대조하는 조사라면
Aside의 Ultrabrowse를 고를 수 있다.
인용이 필요한 조사, 제품 비교, 마이그레이션 계획,
여러 사이트에 걸친 보안·컴플라이언스·가격 확인에 맞고,
한 페이지짜리 질문에는 일반 작업을 쓰라고 안내한다.[^ultrabrowse]
앱의 모델 선택기에서 `Reasoning` 아래에 보이며 Pro 이상에서 쓸 수 있다.[^ultrabrowse]
지시문에 “사용한 페이지를 인용하라”를 넣으면
진행 기록과 별도로 출처 목록이 결과에 붙는다.[^ultrabrowse]

### 반복 위임은 routine으로 넘긴다

같은 위임을 주기적으로 반복한다면
Claude Code가 매번 `aside`를 부르는 대신 Aside의 routine으로 넘긴다.
routine은 두 종류다.[^automation]

| 종류              | 동작                             | 맞는 일                        |
| ----------------- | -------------------------------- | ------------------------------ |
| Cron routine      | 일정에 따라 새 작업을 시작한다   | 주간 요약처럼 독립된 반복 작업 |
| Heartbeat routine | 기존 대화를 깨워 이어서 진행한다 | 같은 맥락을 이어 가야 하는 일  |

Aside는 겹치는 routine 실행을 건너뛰고,
대상 대화를 쓸 수 없으면 routine을 멈춘다.[^automation]
`Settings > Routines`에서 만들고, 지시와 일정을 고치고,
멈추거나 지금 바로 돌릴 수 있다.[^automation]
Aside가 반복되는 일을 찾아 routine 초안을 제안하는 기능도 있다.[^automation]
무료 플랜은 활성 routine을 3개까지, Pro는 제한 없이 둘 수 있다.[^automation]

역할을 나누면 이렇다.
처음 한두 번은 Claude Code가 `aside`로 위임하며 지시문을 다듬고,
결과가 안정되면 그 지시문 그대로 routine으로 옮긴다.
routine의 지시문에도 진행 기록 파일 경로를 넣어 두면,
Claude Code는 나중에 기록 파일만 읽어 결과를 이어받을 수 있다.

### 모델과 계정 고르기

Aside 안의 에이전트를 움직이는 모델은
Aside 요금제 모델, 연결한 ChatGPT·Claude·Copilot 구독,
Anthropic·OpenAI·OpenRouter·Google·xAI 등의 API 키 가운데서 고른다.[^ai]
CLI에서는 `exec -m`으로 작업마다 모델을 정한다.[^dev]
Claude Code가 거절하던 작업을 넘기는 것이 목적이라면,
같은 Claude 모델이 Aside 안에서 다시 거절할 수 있다는 점을 기억해야 한다.
그때는 다른 제공자의 모델로 같은 지시문을 다시 보내 본다.
여러 Aside 계정을 쓰면 `--account`로 어느 계정의 브라우저에서 일할지 정한다.[^dev]

### Claude Code가 먼저 판단하지 않게 하는 지침

이 구조가 성립하려면 Claude Code가 브라우저 작업을 받았을 때
가능 여부를 스스로 결론 내지 않고 Aside에 넘겨야 한다.
프로젝트 지침(`CLAUDE.md`)에 넘기는 규칙과 넘기는 형식을 적어 둔다.

```markdown
## 브라우저 작업은 Aside에 위임한다

- 로그인이 필요한 사이트, 금융·거래소 사이트의 내 계정 조회, 로그인 뒤 파일 내려받기,
  사내 대시보드 조회는 직접 브라우저를 조작하지 않는다.
  이 사이트에서 할 수 있는지 스스로 결론 내리지 말고 `aside` CLI로 작업을 넘긴다.
- 넘길 때는 다음 일곱 가지를 적는다.
  1. 대상 사이트와 계정
  2. 원하는 결과물
  3. 저장 위치
  4. 하지 말아야 할 동작
  5. 사람 승인이 필요한 동작(결제, 송금, 게시, 메시지 전송)
  6. 진행 기록 파일 경로(`aside-runs/<날짜>-<작업명>.md`)
  7. MFA, CAPTCHA, 예상과 다른 화면을 만났을 때 멈추고 묻기
- 위임하기 전에 `aside-runs/index.md`에 날짜, 목표, 지시문 원문을 적고,
  `aside`가 돌려준 세션 ID를 같은 줄에 더한다.
  이어지는 지시는 `--session`으로 보내고 같은 항목에 덧붙인다.
- 결과를 받으면 진행 기록 파일과 산출물이 실제로 있는지 확인한 뒤 요약한다.
- Aside가 승인이나 입력을 기다리면 사용자에게 알리고, 내가 대신 판단하지 않는다.
```

Aside는 같은 일을 하는 스킬도 제공한다.
`aside skills install`은 `aside-browser` 스킬을 Claude Code,
Codex, Cursor, OpenCode에 설치하고,
`aside skills list`와 `aside skills show`로 내용을 볼 수 있다.[^changelog]
스킬을 설치했더라도 위 지침처럼 “판단하지 말고 넘긴다”는
원칙은 프로젝트 지침에 따로 두는 편이 확실하다.

### 중간 과정을 마크다운으로 남겨 추적하기

목표를 넘기면 Claude Code는 Aside가 돌려준 결과만 본다.
어떤 페이지를 열었고, 어디서 망설였고, 무엇을 건너뛰었는지는 모른다.
위임이 강력한 만큼 이 불투명함이 가장 큰 대가이고,
중간 과정을 파일로 남기면 상당 부분을 되돌릴 수 있다.

Aside가 스스로 남기는 기록부터 알아 둔다.
일반 작업의 대화 기록(transcript)은 작업 폴더에 저장되고,
작업 상세 화면은 작업이 만들거나 바꾼 파일을 보여 주며
이미지, PDF, HTML, 텍스트 파일을 미리 볼 수 있다.[^tasks]
생성된 파일은 작업이나 작업 폴더를 지울 때까지 남는다.[^tasks]
시크릿 모드 작업은 일반 브라우저 프로필 상태를 남기지 않는다.[^tasks]

여기에 더해, 지시문에 진행 기록을 남기라는 요구를 넣는다.
Aside는 작업 폴더 안에서 파일을 쓸 수 있으므로,[^security]
기록 파일을 작업 폴더 안에 두면 Guard 모드에서도 추가 승인이 필요 없다.
다음은 이 문서가 권하는 형식이다.
Aside가 정한 형식이 아니라, 지시문으로 요구하는 사용자 쪽 규약이다.

```bash
aside "Sign in to the bank, download September statements as PDF
to ./statements/2026-09/.
Keep a progress log at ./aside-runs/2026-10-15-statements.md:
append one entry per step with time, URL, action, and result.
Record every approval request, every MFA or CAPTCHA stop,
and anything you skipped or could not find, with the reason.
End the log with a list of files you created.
Do not transfer money or change settings."
```

기록 파일은 다음과 같은 모양이 된다.

```markdown
# 2026-10-15 은행 명세서 내려받기

- 세션: <session-id>
- 목표: 9월 명세서 PDF를 ./statements/2026-09/에 저장

## 진행

| 시각  | URL                    | 동작                 | 결과                    |
| ----- | ---------------------- | -------------------- | ----------------------- |
| 10:02 | bank.example/login     | Vault 자동 입력      | 로그인 완료             |
| 10:03 | bank.example/login     | MFA 요청             | 사용자 승인 대기 → 완료 |
| 10:05 | bank.example/statement | 9월 계좌 2개 내려받기 | PDF 2개 저장            |

## 건너뛴 것

- 카드 명세서: 메뉴를 찾지 못함

## 만든 파일

- ./statements/2026-09/checking.pdf
- ./statements/2026-09/savings.pdf
```

Claude Code 쪽에도 위임 목록을 남긴다.
`aside-runs/index.md`에 날짜, 목표, 지시문 원문, 세션 ID, 기록 파일 경로를
한 줄씩 적어 두면, 나중에 같은 작업을 다시 보내거나
어느 세션을 이어 갈지 고를 때 이 목록 하나로 충분하다.
지시문 원문을 남기는 것이 중요하다.
결과가 이상할 때 원인이 지시문에 있었는지, Aside의 판단에 있었는지를
가를 수 있는 근거는 그것뿐이다.

이 기록에는 세 가지 한계가 있다.

- 진행 기록은 Aside의 에이전트가 스스로 쓴 보고다.
  빠뜨리거나 실제와 다르게 적을 수 있으므로,
  산출물 파일의 존재와 Aside 작업 폴더의 transcript로 맞춰 본다.[^tasks]
- 금융 사이트의 기록에는 계좌 번호나 잔액이 들어갈 수 있다.
  기록 폴더(`aside-runs/`)는 `.gitignore`에 넣고,
  지시문에 계좌 번호는 끝 네 자리만 적으라고 덧붙인다.
- 시크릿 모드로 돌린 작업은 브라우저 프로필 상태를 남기지 않으므로,[^tasks]
  추적이 필요한 작업은 일반 모드로 돌리고 기록 파일에 의존한다.

기록 파일 말고도 Aside 안에는 추적에 쓸 수 있는 기록이 두 가지 더 있다.

| 기록             | 위치                                            | 알 수 있는 것                                    |
| ---------------- | ----------------------------------------------- | ------------------------------------------------ |
| 크레딧 사용 내역 | `Settings > Plan & Usage > Aside credits usage` | 날짜·작업·모델별 사용량, 월별 CSV[^subscription] |
| 메모리 변경 내역 | `Settings > Memory > History`                   | 작업이 무엇을 기억으로 남겼는지[^memory]         |

크레딧 내역은 작업과 모델 단위로 남으므로,
`aside-runs/index.md`의 세션 목록과 맞춰 보면
어느 위임이 비용을 많이 썼는지, 어느 모델로 돌았는지 확인할 수 있다.[^subscription]
메모리는 켜져 있으면 작업 활동에서도 기억을 만든다.[^memory]
금융 계좌 조회처럼 기억으로 남기 싫은 작업이 있다면
메모리 설정과 보존 기간을 먼저 정해 둔다(다음 「위험과 기본값」 참고).

### 승인은 Aside 쪽에서, 어디서든

목표를 넘긴 뒤 승인 요청은 Claude Code가 아니라 Aside 화면에 뜬다.
작업 상태는 승인 대기, 답변 대기, 오류, 완료로 보이고,
승인 팝오버는 브라우저 화면에서 바로 승인하거나 거절한다.[^troubleshooting]
작업이 알림을 기다리는 동안에는 작업을 열어 현재 상태와
Aside가 남긴 안내를 확인할 수 있다.[^tasks]
Mac 앞에 없을 때는 커뮤니티 도구 aside-relay로
휴대폰에서 진행 중인 작업을 보고 승인에 답할 수 있다고 소개된다.[^relay]
승인에 답한 내용도 진행 기록에 남기라고 지시해 두면,
누가 언제 무엇을 허락했는지가 한 파일에 모인다.

### 결과를 받은 뒤 Claude Code가 할 일

1. 산출물이 지시한 위치에 실제로 있는지, 개수와 이름이 맞는지 확인한다.
2. 진행 기록 파일의 「건너뛴 것」과 승인 기록을 읽는다.
3. 기록과 산출물이 어긋나면 Aside 작업 상세 화면과 transcript를 확인하도록
   사용자에게 알린다.[^tasks]
4. 부족한 부분은 같은 세션에 `--session`으로 이어 보낸다.[^dev]
5. 그 뒤에야 산출물로 코드 수정, 요약, 정리 같은 다음 일을 한다.

### 위임이 강력한 만큼 감수할 것

- 결과의 품질은 Aside 안에서 고른 모델에 달려 있다.
  Claude Code의 모델이 아무리 좋아도 브라우저 안의 판단은 그 모델이 하지 않는다.
- 같은 지시문이 매번 같은 경로로 끝나지 않는다.
  매번 똑같아야 하는 점검은 REPL 스크립트가 낫다.[^dev]
- 위임은 Aside 쪽 사용량을 쓴다.
  Aside 요금제 모델은 크레딧을 쓰고, 무료 플랜은 월 500 크레딧,
  Pro는 무료의 3배, Max는 30배다.[^subscription]
  연결한 API 키를 쓰면 그 제공자 계정으로 과금될 수 있다.[^subscription]
- CAPTCHA, MFA, 본인 확인과 결제·게시·메시지 승인은
  어떤 연결 방식이든 사람 몫으로 남는다.[^vault]

## 다른 연결 방식: MCP와 REPL

### MCP는 Claude가 브라우저를 직접 모는 길이다

`aside mcp`를 MCP 서버로 등록하면 Claude Code가
Aside 브라우저를 도구로 쓴다.[^dev]
Hermes 에이전트용으로 이 연결을 검증한 공개 저장소에 따르면,
이때 노출되는 도구는 `mcp_aside_repl` 하나이고
`goto`, `click`, `fill`,
`screenshot` 같은 Playwright 형태의 API로 화면을 조작한다.[^hermes]
즉 어떤 페이지를 열고 무엇을 클릭할지 매 단계를 Claude Code의 모델이 정한다.
Claude가 “이 사이트에서는 못 한다”고 판단하면
그 판단은 MCP를 거쳐도 그대로 남는다.
이 길은 로그인된 세션으로 증거를 가져오는 데는 좋지만,
Claude가 스스로 멈추는 문제를 풀어 주지는 않는다.

### REPL은 결정적인 단계에만

`aside repl`은 화면 검사, 스크린샷, 내려받기,
결정적인 단계가 필요할 때 쓴다.[^dev]
같은 동작을 매번 똑같이 반복해야 하는 점검이라면 위임보다 REPL 스크립트가 낫다.
공개 저장소의 경험에 따르면 `openTab()`으로
연 탭은 그 REPL 세션이 끝나면 사라지고,
보이는 창에 남기려면 기존 탭을
`attachBrowserTab`으로 붙잡아 이동해야 한다.[^hermes]

## 설치와 로그인

```bash
# macOS에서 CLI 설치
curl -fsSL https://releases.aside.com/install.sh | bash

# 업데이트
aside --update
```

CLI를 다른 컴퓨터나 에이전트의 호스팅 환경에서 로그인할 때는
`aside login` 전에 `ASIDE_CLI_AUTH_PATH`로 자격 증명 파일 경로를 정하고,
Aside 설정의 Devices 화면에서 코드를 승인해야 한다.[^dev]
이 변수는 이후의 모든 `aside` 명령에 넘겨야 하며,
한 셸에서 내보낸 값이 에이전트의 다른 도구 호출로 이어지지는 않는다.[^dev]
기본 경로는 `~/.aside/cli/auth.json`이고,
이 파일은 출력하거나 커밋하면 안 된다.[^dev]
MCP로도 함께 쓰려면 Claude Code에 다음처럼 등록한다.[^dev]

```json
{
  "mcpServers": {
    "aside": {
      "command": "aside",
      "args": ["mcp"]
    }
  }
}
```

## 무엇이 유용해지나

Aside가 개발자용으로 내세우는 경계는 분명하다.
코드 변경은 코딩 에이전트가,
편집기 밖의 브라우저 증거는 Aside가 맡는다는 것이다.[^blog]
공식 소개가 드는 사례는 다음과 같다.[^blog]

| 작업             | Aside가 하는 일                                              |
| ---------------- | ------------------------------------------------------------ |
| 실패한 CI 분석   | 로그인된 CI에서 실패 로그를 비교하고 PR 코멘트 초안을 만든다 |
| PR 증거 묶음     | Linear 이슈, 체크, 배포, 스크린샷을 한데 모은다              |
| 기능 플래그 점검 | 롤아웃을 바꾸기 전에 플래그 대시보드를 확인한다              |
| 스테이징 QA      | 데스크톱과 모바일 화면을 찍는다                              |
| 디버그 맥락      | 브라우저 기록에서 관련 페이지를 찾는다                       |
| 모니터링 감시    | 대시보드를 지켜보다 이상을 알린다                            |

Claude Code만으로는 이 일들이 막히는 지점이 하나 있다.
대부분의 사내 대시보드, CI, 관리 페이지는 로그인 뒤에 있고,
Claude Code의 웹 도구는 사용자의 브라우저 세션을 갖고 있지 않다.
Aside는 사용자가 이미 로그인한 브라우저 세션과
자체 비밀번호 저장소로 그 벽을 넘는다.
Garry Tan은 이를
“실제 Chromium에서 사용자를 대신해 실제 자격 증명에 접근하게 한다”고
표현했다.[^vibecoding]

## Claude 쪽이 막는 것과 Aside가 하는 것

이 저장소에서 Claude Code가 Claude in Chrome으로 브라우저를 다룰 때는
비밀번호 입력, 계정 생성, CAPTCHA 풀기, 금융 거래, 설치 등을 하지 않고,
양식 제출이나 구매,
게시처럼 되돌리기 어려운 동작은 매번 사용자에게 확인을 받는 규칙을 따른다.
Aside 문서와 비교하면 다음과 같다.

| 동작                     | Claude in Chrome (이 저장소의 작업 규칙) | Aside                                                                  |
| ------------------------ | ---------------------------------------- | ---------------------------------------------------------------------- |
| 로그인된 페이지 읽기     | 사용자의 Chrome 세션으로 가능            | 가능. 브라우저 세션과 기록을 쓴다[^privacy]                            |
| 저장된 비밀번호로 로그인 | 하지 않음. 사용자에게 맡긴다             | Vault가 자동 입력한다. 모델은 비밀번호 값을 받지 않는다[^vault]        |
| CAPTCHA, MFA, 본인 확인  | 하지 않음                                | 하지 않음. 화면의 단계를 사람이 마치면 이어서 진행한다[^vault]         |
| 결제, 게시, 메시지 전송  | 매번 사용자 확인                         | 작업이 승인을 요청할 때는 사람 확인을 기다려야 한다고 안내한다[^vault] |
| 파일 접근                | 해당 없음                                | 권한 모드로 조절. 기본은 승인된 폴더만 쓰는 Guard[^security]           |
| 도구별 허용              | 해당 없음                                | Allow, Ask, Deny 규칙. Deny가 우선한다[^security]                      |

즉 Aside가 실제로 넓혀 주는 것은
“저장된 자격 증명으로 로그인해 그 뒤의 페이지에서 일하는 것”이다.
비밀번호를 모델에게 보여 주지 않고 브라우저가 대신 채우는 방식이라,
에이전트에게 비밀번호를 건네는 것보다 안전한 경로로 이 일을 해낸다.
반면 CAPTCHA, MFA, 본인 확인은 Aside도 사람에게 넘기고,
결제나 게시 같은 민감한 동작도 승인 대상으로 둔다.
Claude가 하지 않는 일을 Aside가 아무 확인 없이 해 주기를 기대하면 실망하게 된다.

## Claude Code가 멈추는 지점을 Aside로 넘기기

Aside를 붙이는 가장 큰 가치는 여기 있다.
Claude Code와 Claude in Chrome은 사용자 계정에서 하는 정당한 작업이라도
비밀번호 입력, 양식 제출,
로그인 뒤 파일 내려받기 같은 단계에서 멈추고 사용자에게 넘긴다.
이 단계들은 사용자가 직접 허락하면 되는 일인데,
작업이 길수록 멈춤이 쌓여 자동화의 의미가 사라진다.
Aside는 사용자가 미리 정한 권한 안에서 이 단계들을 이어서 처리하므로,
Claude Code는 계획과 판단을 맡고
브라우저 안의 실행은 Aside에 통째로 넘길 수 있다.

### 무엇을 넘길 수 있나

| Claude Code가 멈추는 단계      | Aside로 넘기면                                                                  |
| ------------------------------ | ------------------------------------------------------------------------------- |
| 저장된 비밀번호로 로그인       | Vault가 대상 URL을 확인한 뒤 자동 입력한다. 모델은 값을 보지 않는다[^vault]     |
| 로그인 뒤 파일 내려받기        | 정한 폴더에 저장한다. 예: 이번 달 급여 명세서 PDF를 Downloads에[^tasks]         |
| 사내 대시보드·관리 페이지 조회 | 로그인된 세션으로 열고 결과를 돌려준다[^blog]                                   |
| 여러 사이트를 오가는 긴 작업   | 한 작업 안에서 여러 단계를 이어 가고, 필요하면 기다렸다가 다시 시작한다[^tasks] |
| 반복 조회                      | routine으로 정해 두고 돌린다[^automation]                                       |

### 멈추지 않게 설정하기

Aside가 중간에 묻지 않고 끝까지 가게 하려면 다음을 미리 정해 둔다.

1. `Settings > Passwords > Access policy for AI agents`에서
   에이전트가 저장된 로그인을 쓸 수 있게 한다.
   전체 정책은 `While unlocked`로 두고, 자주 쓰는 업무 사이트 항목만 개별로 `Always allow`로 덮어쓸 수 있다.[^passwords]
2. `Settings > Agents`의 도구 규칙에서 반복적으로 허락하는 동작은 `Allow`,
   매번 보고 싶은 동작은 `Ask`, 절대 하면 안 되는 동작은 `Deny`로 둔다.
   `Deny`가 항상 이긴다.[^security]
3. 작업의 권한 모드는 기본 `Guard`로 두고 작업 폴더를 정해 준다.
   파일을 어디서나 다뤄야 할 때만 `Full access`를 쓴다.[^security]
   `Settings > Agents`의 설정은 에이전트 기본값이고,
   작업마다 권한을 따로 정하면 그 설정이 기본값 위에 덧붙는다.[^security]
   명령 실행을 OS 수준에서 격리하는 `Sandbox` 설정도 같은 화면에 있다.[^security]
4. 작업 지시에 대상 계정, 결과물, 저장 위치, 하지 말아야 할 동작을 적는다.
   Aside 문서는 “Handle my billing.” 같은 막연한 지시 대신
   이름, 산출물, 목적지를 적으라고 권한다.[^tasks]

Claude Code 쪽에서 언제, 어떤 형식으로 Aside에 넘길지는
앞의 「Claude Code가 먼저 판단하지 않게 하는 지침」을 그대로 쓴다.
MCP로 단계를 조종하면 판단이 다시 Claude Code에 남으므로,
이 절의 작업은 CLI 위임으로 넘긴다.

### 사이트 단위로 막히는 경우

Claude in Chrome이 “이 사이트에서는 못 한다”고 멈추는 데에는 정해진 이유가 있다.
Anthropic 도움말에 따르면 Claude in Chrome은 기본 차단 범주를 두고 있고,
그 범주는 금융 서비스, 은행, 투자 플랫폼, 암호화폐 거래소,
성인 콘텐츠, 불법 복제 콘텐츠다.[^cic-trouble]
안전 안내 문서는 성인 콘텐츠와 알려진 불법 복제 사이트는 접근할 수 없고,
금융 사이트는 접근 전에 허락을 구한다고 설명하며,
주식 거래, CAPTCHA 우회, 민감한 데이터 입력도 하지 않는다고 적는다.[^cic-safety]
Team과 Enterprise 플랜에서는 관리자가
허용 목록이나 차단 목록을 더 걸 수 있다.[^cic-trouble]

Aside 도움말과 변경 기록에는 이런 사이트 범주 차단이 보이지 않는다.
사이트 단위로 사용자가 정하는 것은
비밀번호 자동 입력의 제외 도메인 정도이고,[^passwords]
다른 사이트의 로그인을 채우는 교차 사이트 자동 입력은 막는다.[^changelog]
그래서 내 은행 거래 내역 내려받기, 증권사 잔고 확인, 거래소 입출금 내역 정리처럼
Claude in Chrome이 범주 때문에 멈추는
내 계정의 조회 작업은 Aside로 넘기면 진행된다.

다만 두 가지는 남는다.
첫째, Aside 안의 에이전트도 결국 사용자가 고른 모델이 움직인다.
Claude 구독이나 API 키를 연결했다면 모델 자체가 특정 작업을 거절할 수 있고,
Aside는 ChatGPT 구독, OpenAI, Google,
xAI 등 다른 제공자도 고를 수 있게 한다.[^ai]
둘째, 사이트의 이용 약관이 자동화된 접근을 금지한다면 그 책임은 사용자에게 있다.
Anthropic도 브라우저 에이전트가 대신 한 모든 행동과
약관 준수의 책임이 사용자에게 있다고 명시한다.[^cic-safety]
금융 사이트에서 송금이나 주문처럼 돈이 움직이는 동작은
Aside에서도 승인 단계를 남겨 두는 편이 맞다.

### 넘겨도 끝까지 가지 않는 것

다음은 Aside로 넘겨도 사람이 해야 한다.

- CAPTCHA, MFA, 패스키 승인, 본인 확인: Aside도 화면의 단계를 사람이 마칠 때까지 기다린다.[^vault]
- 결제, 게시, 메시지 전송: 작업이 승인을 요청하면 사람 확인을 기다리도록 되어 있다.[^vault]
- 시크릿 모드 작업에서의 저장된 비밀번호 사용: 에이전트가 쓸 수 없다.[^passwords]

이 경계는 Aside의 한계라기보다 로그인된 세션을 맡기는 대가로 남겨 둔 안전장치다.
아래 위험 절에서 보듯, 이 단계까지 자동으로 넘기면
페이지에 숨은 지시문 하나가 실제 송금이나 게시로 이어질 수 있다.

## 위험과 기본값

### 기본값이 생각보다 넓다

Aside Vault의 에이전트 접근 정책은 `Always allow`,
`While unlocked`, `Never` 중에서 고르는데,
기본값이 `Always allow`다.[^passwords]
작업의 권한 모드는 `Read only`, `Guard`,
`Full access`가 있고 기본은 `Guard`다.[^security]
`Full access`는 컴퓨터 어디든 읽고 쓰게 하지만
저장된 비밀번호 값은 드러내지 않는다.[^security]
분석 데이터 공유도 기본으로 켜져 있다.[^privacy]
처음 설치한 뒤 비밀번호 정책을 `While unlocked`로 바꾸고,
에이전트가 로그인하면 안 되는 도메인을 제외 목록에 넣는 편이 낫다.[^passwords]

메모리도 확인할 기본값이다.
메모리가 켜져 있으면 Aside는 브라우징 기록을 맥락으로 쓰고,
대화와 작업 활동에서 기억을 만든다.[^memory]
보존 기간은 `Never forget`, `30 days`, `90 days` 중에서 고르고,
`Settings > Memory`의 `Overview`에서 저장된 기억을 보고 고칠 수 있다.[^memory]
은행이나 거래소 화면을 읽는 작업을 위임할 계획이라면
보존 기간을 짧게 두고, 그런 작업 뒤에는 `Overview`를 한 번 열어 보는 편이 낫다.

### 로그인된 세션은 프롬프트 주입의 표적이 된다

에이전트가 로그인된 메일, CRM, 결제 페이지를 읽는다는 것은
그 페이지에 숨겨진 지시문도 읽는다는 뜻이다.
악성 페이지나 메일 본문이 “이 링크로 송금하라” 같은 지시를 담고 있으면,
자격 증명이 열려 있는 에이전트는 그 지시를 실행할 수단을 갖고 있다.
Aside가 민감한 동작에 승인을 요구하는 것은 이 위험에 대한 마지막 방어선이고,
그래서 승인 단계를 끄는 방향으로 쓰는 것은 권하기 어렵다.

### 두 에이전트가 서로를 감시하지 않는다

Claude Code가 Aside에게 작업을 넘기면 실제 클릭은 Aside의 에이전트가 한다.
Claude Code는 Aside가 돌려준 결과만 보고,
Aside 안에서 어떤 페이지를 열었는지는 모른다.
작업 기록은 Aside의 작업 폴더에 남으므로,[^tasks]
중요한 작업은 Aside 쪽 기록을 함께 확인해야 무엇이 일어났는지 알 수 있다.
앞의 「중간 과정을 마크다운으로 남겨 추적하기」처럼
진행 기록 파일을 지시해 두면 이 확인이 훨씬 쉬워진다.

## 써 볼 만한 경우

- 로그인 뒤에 있는 CI 로그, 대시보드, 사내 관리 페이지에서 디버깅 증거를 가져올 때
- 스테이징 화면을 여러 해상도로 찍어 PR에 붙일 때
- 반복되는 조회를 routine으로 돌릴 때(무료 플랜은 3개까지)[^automation]
- 급여 명세서나 청구서처럼 로그인 뒤의 파일을 정해진 곳에 내려받을 때[^tasks]

## 맞지 않는 경우

- CAPTCHA나 MFA를 사람 없이 통과해야 하는 자동화
- 확인 없이 결제, 게시, 메시지를 보내야 하는 작업
- 회사 정책상 서드파티 브라우저에 업무 계정 자격 증명을 둘 수 없는 환경

## 기억할 원칙

### 증거는 브라우저 에이전트가, 판단과 변경은 코딩 에이전트와 사람이

Aside가 스스로 그은 경계,
곧 코드는 코딩 에이전트가 브라우저 증거는 Aside가 맡는다는 구분은
두 도구를 함께 쓸 때 그대로 지킬 만한 원칙이다.
브라우저 에이전트는 로그인된 세계에서 사실을 모아 오고,
그 사실로 무엇을 바꿀지는 코딩 에이전트와 사람이 정한다.
돈이 나가거나 다른 사람에게 무언가가 보내지는 순간에는
어느 에이전트를 쓰든 사람이 확인하는 단계가 남아야 한다.

### 판단을 넘기려면 단계가 아니라 목표를 넘긴다

두 에이전트를 이을 때 Claude Code가 브라우저 단계를 하나씩 보내면
모든 판단은 Claude Code에 남고, Aside는 손만 빌려주는 도구가 된다.
Claude Code가 목표와 제약만 적어 넘기면
어떻게 할지는 Aside의 에이전트와 사용자의 권한 설정이 정한다.
Claude Code는 계획하고 넘기고 결과를 받아 다음 일을 판단하는 데 집중하고,
브라우저 안의 실행과 그 승인은 Aside와
사람 사이에서 끝나게 하는 것이 이 조합의 핵심이다.

---

[^ph]: Product Hunt, [Aside: AI browser that actually gets work done for you](https://www.producthunt.com/products/aside-6), 날짜 미표기

[^ai]: Aside Help Center, [Configure AI providers](https://docs.aside.com/help/ai), 날짜 미표기

[^dev]: Aside Help Center, [Use the CLI, MCP, and REPL](https://docs.aside.com/help/developers), 날짜 미표기

[^blog]: Aside, [Aside for Developers](https://aside.com/blog/developers), 2026-06-22

[^vibecoding]: vibecoding.tech, [AI agent can see restricted logs: Aside connects Chromium via MCP](https://vibecoding.tech/news/2026/09/27/aside-browser-mcp-agents), 2026-09-27

[^privacy]: Aside Help Center, [Manage privacy and local data](https://docs.aside.com/help/privacy), 날짜 미표기

[^vault]: Aside Help Center, [Use Password Manager](https://docs.aside.com/help/password-manager), 날짜 미표기

[^security]: Aside Help Center, [Set agent permissions](https://docs.aside.com/help/security), 날짜 미표기

[^passwords]: Aside Help Center, [Configure password autofill](https://docs.aside.com/help/passwords), 날짜 미표기

[^tasks]: Aside Help Center, [Run tasks](https://docs.aside.com/help/tasks), 날짜 미표기

[^subscription]: Aside Help Center, [Manage your Aside subscription](https://docs.aside.com/help/subscription), 날짜 미표기

[^cic-trouble]: Claude Help Center, [Claude in Chrome troubleshooting](https://support.claude.com/en/articles/12902405-claude-in-chrome-troubleshooting), 날짜 미표기

[^cic-safety]: Claude Help Center, [Using Claude in Chrome safely](https://support.claude.com/en/articles/12902428-using-claude-in-chrome-safely), 날짜 미표기

[^changelog]: Aside Help Center, [Components changelog](https://docs.aside.com/changelog/components), 날짜 미표기

[^hermes]: GitHub, [steggdev/aside-browser-mcp](https://github.com/steggdev/aside-browser-mcp), 날짜 미표기 (Aside Browser 1.0.811.1, CLI v1.26.810에서 검증했다고 밝힘)

[^automation]: Aside Help Center, [Use routines](https://docs.aside.com/help/automation), 날짜 미표기

[^memory]: Aside Help Center, [Manage memory](https://docs.aside.com/help/memory), 날짜 미표기

[^sidepanel]: Aside Help Center, [Use the side panel](https://docs.aside.com/help/side-panel), 날짜 미표기

[^ultrabrowse]: Aside Help Center, [Use Ultrabrowse](https://docs.aside.com/help/ultrabrowse), 날짜 미표기

[^troubleshooting]: Aside Help Center, [Troubleshoot Aside](https://docs.aside.com/help/troubleshooting), 날짜 미표기

[^relay]: GeekNews, [aside-relay - 휴대폰에서 Aside를 쓰는 웹 클라이언트](https://news.hada.io/topic?id=35153), 날짜 미표기
