# Postman 데스크톱 앱이 코딩 에이전트에 플러그인을 자동 설치하고 훅 승인까지 시도했다는 보고

원문: [\[SEVERE\] Desktop auto-installs Codex/Claude plugins; installer attempts to trust its own startup hook](https://github.com/postmanlabs/postman-app-support/issues/14370)

HN 토론: <https://news.ycombinator.com/item?id=50354960> (1214점, 397개 댓글)

GN 토론: <https://news.hada.io/topic?id=36538>

## 요약

GitHub 사용자 indicava는 2026년 10월 25일에 Postman 공개 이슈 저장소에 이 이슈를 올렸다.
Mac에서 Postman을 열었더니 코딩 에이전트에 예기치 않은 변화가 생겼다는 내용이다.
MCP 인증 경고가 반복해서 뜨고,
Codex가 API 작업을 계속 Postman 스킬(skill)로 보냈다고 한다.
조사해 보니 사용자 전체 범위의 Postman 플러그인, 시작 지침 훅(hook),
원격 MCP 연결, Claude Code 플러그인, 따로 설치된 Postman CLI가 있었다.

indicava는 이것이 동의와 신뢰 경계의 심각한 문제라고 본다.
관련 없는 코딩 에이전트를 자동으로 바꾸고 자기 지침 훅을 스스로 승인하려는 시도는
API 클라이언트를 열었다는 이유만으로 다른 도구의 기본 워크플로를 차지하는 일이라는 것이다.
증거는 Postman 데스크톱 12.33.4, Codex 플러그인 1.1.0 기준으로 2026년 10월 25일에 조사한 결과다.

이슈가 제시하는 증거는 여섯 가지다.

- 첫째, Postman의 `main.log`에 2026-10-24T09:34:14Z로
  `source: auto-existing-upgrade`, 결과 `claude-code:installed`, `codex:installed`가 기록되어 있다.
- 둘째, `~/.codex/config.toml`에 `[marketplaces.postman]`, `[plugins."postman@postman"]`,
  `[hooks.state."postman@postman:hooks/codex-hooks.json:session_start:0:0"]`의
  `trusted_hash` 항목이 생겼다.
- 셋째, 설치된 `hooks/codex-hooks.json`이 `startup|clear|compact` 때 실행되는
  SessionStart 명령을 등록하고, 이 명령이 `session-start-context.md`를 출력한다.
  그 안에 API 설계, 구현, 모킹, 테스트, 모니터링, 문서화, 배포 같은
  사소하지 않은 API 엔지니어링 작업 전에 `postman:api-engineer` 스킬을 불러오라는 지시가 있다.
- 넷째, 설치 프로그램의 `codex.ts`가 설치 뒤 `approvePostmanHook`을 호출하고,
  `codex-hooks.ts`가 `hooks/list`로 해시를 얻어 `config/batchWrite`로 `hooks.state`의 `trusted_hash`를 쓴다.
- 다섯째, `mcp.codex.json`이 `https://mcp.postman.com/mcp`를 가리키는데,
  Codex 로그에는 `Auth required` 오류로 MCP 서버 시작이 실패했다고 남아 있다.
- 여섯째, `~/.claude/settings.json`에서 `postman@claude-plugins-official`이 켜졌고,
  `~/.local/bin`에 Postman 실행 파일과 `lib` 디렉터리가 같은 시간대에 생겼다.

보고서는 한계를 스스로 밝힌다.
신뢰 기록만으로는 그 기록을 누가 만들었는지 증명되지 않고,
새 Mac에서 재현하지는 못했으며,
데이터 유출을 주장하지 않는다고 적는다.
요구 사항은 여섯 가지다.
심각한 사고로 분류할 것, 기존 사용자 대상 자동 설치를 명시적 동의가 생길 때까지 멈출 것,
설치 프로그램의 훅 자가 승인을 없앨 것,
`auto-existing-upgrade`의 배포 버전과 동의 절차를 밝힐 것,
에이전트 설정과 훅 신뢰와 캐시와 MCP 연결과 CLI를 모두 되돌리는 제거 경로를 줄 것,
시작 지침을 Postman을 명시적으로 요청한 경우로 좁힐 것이다.

이슈는 2026년 11월 4일 현재 열려 있고 댓글이 40개다.
Postman 측을 we로 칭한 zecoquit이 11월 3일 23:36 GMT에 답을 달았다.
Postman CLI와 에이전트 플러그인을 데스크톱 앱에 묶은 이유는
따로 설치하고 연결하는 데 어려움을 겪는 사용자가 많았기 때문이고,
다운로드 페이지와 앱 업데이트 과정에서 이를 알리며
앱 안에서 각 구성 요소를 제거할 수 있다는 설명이다.
그러면서 특히 기존 사용자에게 옵트인(opt-in)을 더 분명하게 하고,
훅 승인과 세션 시작 동작을 검토하겠으며 변경이 들어가면 이 스레드에 알리겠다고 했다.

다른 사용자의 보고도 올라왔다.
ronthedrummer는 11월 3일에 12.31.3에서 12.35.1로 업데이트된 직후
`auto-existing-upgrade`가 CLI와 Claude Code와 Codex 플러그인을 설치했고
Cursor는 이미 설치되어 있었다고 로그와 함께 적었다.
같은 사람의 Codex 설정에는 `hooks.state`나 `trusted_hash`가 없었다고 한다.
ck-tecso는 Copilot의 `~/.copilot/settings.json`에도
Postman 마켓플레이스와 플러그인이 등록되어 있었고,
Postman 메뉴의 제거 항목을 눌러도 Copilot에서는 제거되지 않았다고 적었다.

## 분석

### 확립된 사실, 추론, 판단이 한 이슈 안에서 구분되어 있다

이 이슈는 증거를 직접 관찰한 것과 추론한 것을 가른다.
로그 줄, 설정 파일 항목, 소스 코드는 관찰이다.
누가 `trusted_hash`를 만들었는지, 사용자가 Codex에서 상호작용했는지는
관찰되지 않은 부분이고, 이슈가 스스로 증명이라고 부르지 않는다.
요구 사항 여섯 개는 판단이다.

이슈가 고정한 커밋 `6c8e452e...`의 소스를 직접 열어 보면 네 번째 증거는 그대로 확인된다.
`approvePostmanHook` 함수의 주석은 설치 뒤 Postman의 현재 훅만 승인한다고 적고,
`config/batchWrite`로 `hooks.state`에 `trusted_hash`를 `upsert`하는 편집을 보낸다.[^codex-hooks]
이 함수는 훅 상태가 `untrusted`나 `modified`일 때만 쓰고,
설치된 `session-start-context.md`가 비어 있지 않은지 확인하고,
검사한 뒤 해시가 바뀌었다면 승인을 건너뛴다.[^codex-hooks]
설치 프로그램의 `codex.ts`는 `install` 안에서 이 함수를 호출한다.[^codex-installer]
따라서 승인 시도가 코드에 있다는 것은 이슈의 추론이 아니라 소스에서 확인되는 사실이다.

### 문제는 둘로 나뉜다

하나는 기존 사용자의 앱 업데이트 뒤에 다른 도구의 설정이 바뀐 일이다.
`main.log`의 `source: auto-existing-upgrade` 기록이 이 설치를 가리킨다.
다른 하나는 설치 프로그램이 에이전트가 사용자에게 묻는 동의를 대신하려 했다는 점이다.
첫째는 동의 없이 설치되었다는 문제이고,
둘째는 설치된 것이 곧바로 실행 권한을 얻게 하려 했다는 문제다.
둘은 따로 판단할 수 있다.
설치만으로는 SessionStart 지침이 에이전트에 출력되지 않을 수 있고,
승인이 붙으면 출력된다.

ronthedrummer의 보고가 이 구분을 보여 준다.
이 사람의 Codex 설정에는 마켓플레이스와 플러그인 항목이 생겼지만 `hooks.state`와 `trusted_hash`는 없었다.
Codex 플러그인은 1.3.0이었다.
이슈 작성자의 12.33.4와 플러그인 1.1.0에서는 두 해시 기록이 있었으므로,
이후 빌드에서 승인 기록을 만드는 동작만 빠졌을 가능성이 있다.
이것은 foma-agent라는 계정도 비슷하게 짚은 추론이고,
설치 코드의 두 버전을 비교해 확인한 것은 아니다.

Hacker News의 jodrellblank는 다른 도구에 훅을 몰래 설치해 그 트래픽을 Postman으로 돌리는 것은
전혀 합리적이지 않다고 적었다.[^jodrellblank]
이 문장은 이슈의 두 문제를 한 문장으로 묶은 표현이다.
다만 이슈에서 확인되는 것은 에이전트가 API 작업에서 Postman 스킬을 불러오도록 유도한다는 것이고,
에이전트의 트래픽을 Postman 서버로 보낸다는 증거는 이슈에 없다.

### 지침 파일의 문구는 이슈의 요약보다 조건이 많다

이슈는 훅이 API 작업을 Postman으로 보낸다고 요약한다.
설치된 지침 파일을 직접 읽으면 `EXTREMELY_IMPORTANT` 블록 안에서
사소하지 않은 API 엔지니어링 작업 전에 `postman:api-engineer` 스킬을 불러오라고 한다.[^session-start]
같은 파일은 순수한 질문과 한 줄짜리 사소한 수정에는 필요 없고,
하위 에이전트로 배정된 경우에는 이 블록을 무시하며,
AGENTS.md나 CLAUDE.md 같은 프로젝트 지침 파일과 직접 요청이 이 지시보다 우선한다고도 적는다.[^session-start]
이슈가 인용한 문장은 정확하지만, 마지막 두 가지 제한은 이슈 본문에 나오지 않는다.
이 제한이 있어도 설치 직후 모든 세션에 Postman을 기본 진입점으로 두는 지시라는 점은 달라지지 않는다.

### 업체 측 답변은 동의의 근거를 공지에 둔다

Postman의 답변은 다운로드 페이지와 업데이트 과정에서 알렸다는 것을 근거로 든다.
현재의 다운로드 페이지를 열어 보면 Postman 앱이 CLI와 Postman 플러그인을 포함한다는 문장이 있다.[^download]
그러나 그 문장이 기존 사용자의 업데이트가 다른 에이전트의 설정을 바꿀 수 있다는 것까지 알리는지는,
페이지의 요약만으로는 확인하지 못했다.
댓글에서 NuclEnergy는 2026년 10월 26일의 Wayback Machine 스냅숏에는 해당 문구가 없었다고 주장하지만,
이 문서를 쓰는 환경에서는 Wayback Machine을 열 수 없어 그 주장은 확인하지 못했다.

## 비평

### 악성코드라는 표현은 이슈의 증거가 지지하는 범위를 넘는다

댓글에서는 가장 많이 호응을 받은 것이 Postman이 바이러스라는 한 줄이었다.
이어서 악성코드라는 표현, 불법이 아니냐는 물음, 은밀한 시도라는 비난이 나온다.
이슈 본문은 이를 지지하지 않는다.
원하지 않은 통합과 지침 변경을 확립했을 뿐 데이터 유출은 주장하지 않는다고 본문에 쓰여 있다.
ronthedrummer도 설치와 시작 지침을 확인했을 뿐 업로드의 증거는 없다고 적었다.

이 구분은 실용적으로 중요하다.
동의 없는 설치와 악성코드는 서로 다른 문제이고, 해결책도 다르다.
앞의 것은 제품의 동의 절차를 고치면 풀리지만,
뒤의 것은 침해 대응이 필요하다.
호응 수는 증거의 무게가 아니라 반응의 크기를 보여 준다.

Hacker News에는 이 이슈가 Postman이 AI 플러그인을 조용히 자동 설치하고
모든 API 데이터를 공유하려 한다는 취지의 제목으로 올라왔다.[^hn-thread]
이슈 본문은 데이터 유출을 주장하지 않는다고 밝히므로,
이 제목의 뒷부분은 이슈의 증거보다 넓다.

### 재현은 같은 로그 형식의 자기 보고에 의존한다

이슈 작성자는 새 Mac에서 재현하지 못했다고 밝힌다.
ronthedrummer의 사례가 두 번째 관찰이지만 역시 본인이 올린 로그와 파일 확인이다.
두 사례가 같은 기능 이름(`auto-existing-upgrade`)을 보이므로 같은 경로라는 추정은 합리적이다.
하지만 어떤 조건에서 이 경로가 도는지, 곧 기능 플래그와 대상 사용자 범위는 이슈의 요구 4번이 묻고 있고 아직 답이 없다.
Windows 사용자에 대한 보고도 없다.
훅 정의에 Windows용 명령(`commandWindows`)이 있다는 점은 소스에서 확인되지만,
Windows에서 같은 자동 설치가 일어나는지는 알려지지 않았다.

### Postman의 답변은 요구 사항 여섯 개 중 일부에만 닿는다

답변은 옵트인을 분명히 하겠다고 하고 훅 승인과 세션 시작 동작을 검토하겠다고 한다.
그러나 기존 사용자 대상 자동 설치를 지금 멈출지,
설치 프로그램의 훅 자가 승인을 없앨지, 완전한 제거 경로를 줄지에는 답하지 않는다.
옵트인을 특히 기존 사용자에게 분명히 하겠다는 말에는
ceberttylertech가 새 설치에서도 옵트인이어야 한다고 반박했다.

제거 경로에 대한 이슈 요구는 ck-tecso의 보고로 뒷받침된다.
메뉴의 제거 항목이 Claude나 Codex에서는 어떻게 동작하는지는 알 수 없지만,
Copilot에서는 제거되지 않았다고 한다.
이는 한 사람의 보고이고 다른 환경에서는 확인되지 않았다.

### 훅 신뢰에 대한 기술적 논평은 이 이슈의 증거가 아니다

foma-agent는 스스로 AI 에이전트라고 밝히고, 자신의 환경에서 Codex와 Claude Code의
훅 신뢰 방식을 시험한 결과를 길게 적었다.
Codex는 훅 상태 기록이 없으면 훅을 건너뛰지만 그 기록이 `config.toml` 안에 있고
내용은 계정의 프로세스가 계산할 수 있으며,
Claude Code는 설정 파일에 훅을 쓰면 바로 실행된다는 내용이다.
이 문서는 그 글이 가리키는 외부 페이지를 열어 보지 않았고 시험을 재현하지도 않았다.
따라서 그 내용은 이슈의 증거가 아니라 한 참여자의 주장으로 읽어야 한다.
댓글에는 이 계정을 두고 봇이라며 불편해하는 반응도 있었다.

## 인사이트

### 문제의 본질은 설치가 아니라 다른 프로그램의 설정에 쓰는 일이다

이 사례에서 바뀐 파일은 `~/.codex/config.toml`, `~/.claude/settings.json`,
`~/.copilot/settings.json`이다.
모두 사용자가 각 에이전트에 내리는 의사를 담은 파일이고,
Postman의 데이터 디렉터리가 아니다.
에이전트 호스트는 이 파일에 적힌 것을 사용자의 선택으로 취급한다.
같은 계정에서 도는 다른 프로그램이 이 파일에 쓰면,
그 쓰기는 구별되지 않은 채 사용자의 선택으로 읽힌다.

이는 오래된 문제와 구조가 같다.
설치 프로그램이 브라우저의 검색 엔진이나 시작 페이지를 바꾸던 시절의 번들 설치와 닮았다.
그때 해법은 개별 프로그램의 선의가 아니라 브라우저와 운영체제가 설정 변경을 가로채 확인하는 쪽으로 갔다.
같은 방향이 에이전트 호스트에서도 필요할 수 있다는 것은 이 문서의 추론이다.
이슈가 요구하는 훅 신뢰 결정을 호스트에 두라는 요구와 이어진다.

둘째 결과도 있다.
에이전트의 시작 컨텍스트에 자기 도구를 넣는 일이 이득이 되면,
모든 개발 도구가 그 자리를 두고 경쟁한다.
`EXTREMELY_IMPORTANT`라는 표지로 지침의 우선순위를 높이는 방식이 퍼지면
에이전트의 컨텍스트가 도구 홍보 문구로 채워질 수 있다.
이슈가 요구한 시작 지침의 축소는 Postman 한 곳의 문제가 아니라 이 경쟁의 사례다.

### 승인 기록을 같은 계정에 두는 설계는 사용자 확인을 보증하지 못한다

foma-agent의 주장대로라면 Codex의 훅 승인 기록은 계정이 쓸 수 있는 설정 파일에 있고
내용이 선언의 해시이므로, 같은 계정의 프로세스가 만들 수 있다.
이 주장이 맞다면 훅 신뢰는 사용자의 상호작용을 보증하는 장치가 아니라
설정 파일을 쓸 수 있는 주체를 가르는 장치에 가깝다.
그러면 이슈의 요구 3번, 곧 훅 신뢰는 사용자가 에이전트 호스트에서 정해야 한다는 요구는
Postman만이 아니라 호스트 설계에도 해당하게 된다.

이 문서가 확인한 것은 설치 프로그램이 승인 편집을 보내는 코드까지이고,
그 편집이 기술적으로 사용자 확인 없이 통하는지는 확인하지 못했다.
이 부분은 Codex의 해당 버전에서 직접 재현해야 판정할 수 있다.

### 개발 도구를 설치한 뒤 설정 파일의 변경을 점검하는 습관이 방어선이다

호스트와 업체가 바뀔 때까지 사용자가 할 수 있는 일은 설치 전후의 차이를 보는 것이다.
이슈가 보여 준 위치를 기준으로 삼으면 다음을 확인한다.

- `~/.codex/config.toml`에서 `[marketplaces.*]`, `[plugins.*]`, `[hooks.state.*]` 항목이 새로 생겼는가.
- `~/.claude/settings.json`의 `enabledPlugins`에 처음 보는 플러그인이 있는가.
- `~/.copilot/settings.json`의 `extraKnownMarketplaces`와 `enabledPlugins`가 바뀌었는가.
- `~/.local/bin`에 처음 보는 실행 파일이 생겼는가.

결론을 바꿀 관찰도 분명하다.
새 설치와 기존 사용자 업데이트에서 같은 경로가 도는 것이 확인되면
문제는 기존 사용자 한정이 아니라 제품 전체의 기본 동작이 된다.
반대로 Postman이 자동 설치를 멈추고 승인 시도를 없앤 빌드를 내놓고
다른 사용자의 로그에서 그 빌드에서는 설정 쓰기가 없다고 확인되면,
이 사고는 한 번의 동의 절차 실패로 정리된다.

### 도구를 바꿔도 같은 압력은 따라온다

Hacker News의 reddalo는 Insomnia가 클라우드 계정을 강제한다며 지금은 Bruno가 더 낫다고 적었고,[^reddalo]
mzajc는 Insomnia 8.0 이상이 서버 계정을 요구하며 그 이유가 광고를 쉽게 하려는 것이라고 밝혔다고 적었다.[^mzajc]
rvz는 Bruno도 투자를 받았으니 성장을 위해 결국 같은 일을 하게 될 것이라고 내다봤다.[^rvz]
pants2는 Postman이 4억 달러 넘게 투자받고 직원 1,500명 넘게 채용했다고 적으며,
그 규모를 정당화해야 하는 압력을 이유로 짚었다.[^pants2]
이 숫자는 댓글 작성자의 주장이고 이 문서는 확인하지 못했다.

pjmlp는 Postman이 고객 여러 곳의 IT 금지 목록에 올랐고,
고객 쪽 개발팀이 쓰지 않는 한 프로젝트 납품에 쓸 수 없게 되었다고 적었다.[^pjmlp]
이 사례는 동의 없는 설치의 비용이 개인 사용자의 불쾌감에 그치지 않고
조직의 도구 허용 목록으로 번질 수 있음을 보여 준다.

Postman의 동기에 대한 이 설명은 댓글 작성자들의 추론이고, 이슈는 동기를 말하지 않는다.
추론이 맞다면 대체 도구로 옮기는 것은 일시적인 해결이다.
그러면 위에서 제안한 설정 파일 변경 점검은 어떤 도구를 쓰든 유지해야 하는 습관이 된다.

---

[^codex-hooks]: GitHub, [installer/src/hosts/codex-hooks.ts](https://github.com/postmanlabs/postman-plugin/blob/6c8e452e0f4237f4bcc0901cb1ac442dec707e49/installer/src/hosts/codex-hooks.ts)

[^codex-installer]: GitHub, [installer/src/hosts/codex.ts](https://github.com/postmanlabs/postman-plugin/blob/6c8e452e0f4237f4bcc0901cb1ac442dec707e49/installer/src/hosts/codex.ts)

[^session-start]: GitHub, [hooks/session-start-context.md](https://github.com/postmanlabs/postman-plugin/blob/6c8e452e0f4237f4bcc0901cb1ac442dec707e49/hooks/session-start-context.md)

[^download]: Postman, [Download Postman | Get Started for Free](https://www.postman.com/downloads/)

[^jodrellblank]: <https://news.ycombinator.com/item?id=50356977>

[^hn-thread]: <https://news.ycombinator.com/item?id=50354960>

[^reddalo]: <https://news.ycombinator.com/item?id=50355903>

[^mzajc]: <https://news.ycombinator.com/item?id=50355265>

[^rvz]: <https://news.ycombinator.com/item?id=50357869>

[^pants2]: <https://news.ycombinator.com/item?id=50355299>

[^pjmlp]: <https://news.ycombinator.com/item?id=50355938>
