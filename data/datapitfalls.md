# datapitfalls: 데이터 분석의 흔한 실수를 Claude로 점검하는 도구

<https://www.avoidingdatapitfalls.com/>

<https://github.com/bjonesdataliteracy/datapitfalls>

GN 토론: <https://news.hada.io/topic?id=35842>

## 소개

datapitfalls는 데이터 작업에서 흔히 생기는 실수를 찾아 주는 오픈소스 도구다.
Ben Jones의 책 *Avoiding Data Pitfalls*(Wiley, 2019)의 실수 분류 체계(taxonomy)를 바탕으로 하고, 분석은 Claude API가 맡는다.
저장소의 README는 “차트 린터”가 축이 잘렸는지, 색 대비가 충분한지 같은 화면 수준에서 멈추는 것과 달리, 이 도구는 질문을 세우는 단계부터 결과를 전달하는 단계까지 전 과정을 본다고 소개한다.
README가 드는 예는 두 가지다.
기간을 골라 뽑은 데이터 위에서는 서식이 완벽한 차트도 오해를 부르고, 널(null)을 말없이 버리는 쿼리는 문법이 완벽해도 거짓을 말한다는 것이다.

점검하는 사슬은 질문 설정, 데이터 수집, 변환, 분석, 시각화, 해석, 전달이다.
입력은 차트 이미지, 코드 조각(Python, SQL, R), 분석을 설명한 글, 문서다.
결과는 발견된 실수, 심각도, 그 실수가 문제인 이유, 고치는 방법을 담은 구조화된 보고서다.
저장소는 2026년 5월 24일에 만들어졌고, 이 문서를 쓰는 시점에 별 51개와 포크 1개를 받았다.
코드는 TypeScript이며 라이선스는 코드와 분류 체계가 갈린다.

## 여덟 개의 영역

분류 체계는 여덟 영역으로 나뉜다.
README가 각 영역에 붙인 설명을 정리하면 다음과 같다.

| 영역                   | 다루는 문제                           | 예                                                 |
| ---------------------- | ------------------------------------- | -------------------------------------------------- |
| Epistemic Errors       | 우리가 사물을 생각하고 아는 방식      | 확증 편향, 앵커링, 상관과 인과의 혼동              |
| Technical Trespasses   | 파이프라인에서 데이터가 깨지는 방식   | 말없이 버려지는 널, 조인 폭발, 타입 강제 변환      |
| Mathematical Miscues   | 숫자가 어긋나는 방식                  | 퍼센트와 퍼센트포인트 혼동, 지수 오용, 분모 간과   |
| Statistical Slip-Ups   | 추론이 오도하는 방식                  | 심프슨의 역설, 기저율 무시, 다중 비교, 생존자 편향 |
| Analytical Aberrations | 분석이 왜곡되는 방식                  | 기간 골라 뽑기, 부적절한 집계, 맥락 누락           |
| Graphical Gaffes       | 차트가 속이는 방식                    | 잘린 축, 오도하는 인코딩, 접근성 실패, 이중 축     |
| Design Dangers         | 표현이 독자에게 실패하는 방식         | 나쁜 레이아웃, 제목과 라벨 누락, 어수선한 대시보드 |
| Biased Baseline        | 데이터에서 누구의 목소리가 반영되는가 | 들리지 않는 목소리, 공을 잘못 돌리는 기여 귀속     |

저장소의 `src/taxonomy/` 아래 YAML 파일은 78개다.
영역별로는 Graphical Gaffes가 18개로 가장 많고, Biased Baseline은 1개뿐이다.
이는 분류 체계의 깊이가 영역마다 크게 다르다는 뜻이다.
이 숫자는 파일 개수이며 규칙의 개수와 같다고 확인하지는 못했다.

## 사용하는 방법

### 명령줄

Node.js 18 이상이 필요하고, Anthropic의 API 키를 환경 변수 `ANTHROPIC_API_KEY`에 둔다.
README의 예시는 다음과 같다.

```bash
# 차트 이미지
npx datapitfalls scan ./quarterly-revenue.png

# 코드 파일
npx datapitfalls scan ./transform.sql

# 분석을 말로 설명한 글
npx datapitfalls scan --text "We compared this year's signups to last year's, \
but only counted users who are still active today."
```

README는 세 번째 예의 설명에서 생존자 편향이 숨어 있다는 것을 도구가 알아본다고 한다.
코드 예로는 `users`와 `orders`를 내부 조인(inner join)하면 주문이 없는 사용자가 말없이 사라지는 쿼리를 든다.
CI에서는 `--ci` 옵션이 종료 코드로 결과를 알려 준다.
이 문서는 API 키 없이 쓸 수 없는 명령줄을 직접 실행해 보지는 않았다.

### 웹 앱

`avoidingdatapitfalls.com/scan`에서 설치 없이 쓸 수 있다.
웹 앱은 위 입력에 더해 PDF 보고서, Word 문서, PowerPoint 발표 자료, Jupyter 노트북, 코드 파일을 올릴 수 있고, 차트 여러 장을 한꺼번에 올려 차트 사이의 일관성 문제(축척이 다름, 인코딩이 다름, 메시지가 모순됨)를 볼 수 있다.
IP마다 사용 횟수가 제한되고, 입력은 스캔을 위해 Claude API로 보내지지만 앱에는 저장되지 않는다고 README는 밝힌다.

### Claude에서 쓰기: MCP 서버

가장 눈에 띄는 사용법은 MCP 서버다.
이 서버는 분류 체계를 Claude Code, Claude Desktop, claude.ai에 제공한다.
점검은 Claude가 직접 규칙을 보며 하므로 서버는 API 키가 필요 없고 Anthropic API를 호출하지 않으며, 읽기 전용이고 네트워크를 쓰지 않는다고 한다.
README가 소개하는 도구는 `get_checklist`, `get_pitfall`, `list_pitfalls`, `search_pitfalls` 네 개이고, `review_for_pitfalls` 프롬프트와 규칙마다 하나씩의 리소스(`datapitfalls://rules/{id}`)가 있다.

```bash
claude mcp add datapitfalls -- npx -y datapitfalls mcp
```

Claude Desktop은 설정 파일에 다음을 넣고 다시 시작한다.

```json
{
  "mcpServers": {
    "datapitfalls": {
      "command": "npx",
      "args": ["-y", "datapitfalls", "mcp"]
    }
  }
}
```

claude.ai에서는 커넥터 디렉터리에서 Data Pitfalls를 찾아 연결하거나, `https://www.avoidingdatapitfalls.com/api/mcp` 주소로 직접 만든 커넥터를 추가할 수 있다.
연결한 뒤에는 이 대시보드를 만들고 모든 차트의 SQL과 디자인을 datapitfalls 기준으로 검사해 고치라는 식으로 요청하면 된다.

### 라이브러리

핵심 함수는 `detectPitfalls()`이다.
산출물 하나(또는 분석 사슬 전체)를 입력으로 받아 구조화된 보고서를 돌려준다.

```ts
import { detectPitfalls, formatReport, hasBlockingFindings } from 'datapitfalls';

const report = await detectPitfalls(
  { kind: 'code', content: 'SELECT AVG(rate) FROM metrics;', language: 'SQL' },
  { apiKey: process.env.ANTHROPIC_API_KEY }
);

console.log(formatReport(report));
if (hasBlockingFindings(report)) process.exit(1);
```

패키지는 ESM만 지원하고 TypeScript 타입을 함께 제공한다.
`toSemioticAnnotations(report)`는 발견된 실수를 Semiotic v3의 주석 형식으로 바꿔 주는 의존성 없는 연결 함수다.
도구는 화면 좌표를 모르기 때문에 주석은 위치가 지정되지 않은 채로 나오고, 위치는 호스트 앱이 정한다.

## 동작 방식

README가 그리는 흐름은 네 단계다.
입력을 받고, 분류 체계에서 관련 규칙을 찾고, Claude가 입력과 규칙을 함께 보고 분석하고, 구조화된 보고서를 돌려준다.
MCP 서버에서는 이 가운데 분석을 서버가 아니라 사용자의 Claude가 한다는 점이 다르다.
`get_checklist`는 규칙뿐 아니라 검토 방법도 함께 준다.
CHANGELOG의 미배포 항목에 따르면 그 방법은 지금 문제를 일으키는 발견과 잠재적 발견의 구분, 결론을 바꾸는 정도에 따른 평가(결론을 바꿈, 근거를 약하게 함, 다듬기 수준), 전체 라벨을 포함한다.

현재는 한 번에 산출물 하나를 스캔한다고 README는 밝힌다.
연결된 여러 단계의 작업 흐름을 하나의 사슬로 보는 일은 로드맵에 있다고 적혀 있다.
반면 로드맵 문서는 이미 제출한 여러 단계를 함께 보는 사슬 스캔(`--chain`, 웹의 전체 분석 모드)을 완료된 항목으로 적고 있어, README와 로드맵이 서로 다른 상태를 말한다.
어느 쪽이 최신인지는 확인하지 못했다.

## 라이선스

라이선스가 둘로 나뉜다는 점은 쓰기 전에 알아야 한다.
엔진, CLI, MCP 서버, 웹 앱의 코드는 MIT이고, 분류 체계(실수 규칙과 그 문장)는 CC BY-NC 4.0이다.
분류 체계 라이선스 문서는 쓰임새를 이렇게 정리한다.
회사에서 자신의 차트, 쿼리, 대시보드, 보고서를 점검하는 용도는 무료다.
규칙을 인용하고 가공하는 비상업적 공유는 책 *Avoiding Data Pitfalls*와 사이트를 밝히면 가능하다.
규칙을 팔거나 유료 제품, 서비스, 강의, 교육에 넣으려면 Data Literacy의 별도 상용 라이선스가 필요하다.
0.11.0 이하 릴리스는 분류 체계가 MIT로 배포됐고 그 복사본은 MIT로 남는다고 한다.

이 구분은 이 도구를 사내 교육에 쓰려는 사람에게 실질적이다.
점검 용도로 쓰는 것과 교육 자료에 규칙을 넣는 것은 다른 허가를 요구한다.

## 읽을 때 주의할 점

### 결과는 Claude의 판단이다

이 도구가 내는 보고서는 분류 체계를 근거로 한 Claude의 추론이다.
결정론적인 정적 분석 도구와 달리 같은 입력에 같은 결과가 나온다는 보장을 README는 하지 않는다.
CI의 종료 코드(`--ci`)로 막는 용도에 쓰려면, 그 판단이 흔들릴 수 있다는 점을 감안해야 한다.
이 점은 이 문서가 확인한 것이 아니라, 모델 기반 점검이 가진 일반적인 성질이다.

### 입력이 외부로 나간다

CLI와 웹 앱 모두 입력이 Claude API로 전달된다.
회사 데이터나 쿼리를 점검한다면 이 전송을 허용하는지 먼저 확인해야 한다.
MCP 서버는 규칙만 제공하고 점검은 사용자의 Claude에서 이뤄지므로, 데이터는 서버로 가지 않는다고 README는 밝힌다.
그러나 데이터는 사용자가 쓰는 Claude 세션으로는 간다.

### 문서마다 말이 다른 곳이 있다

위에서 짚은 사슬 스캔의 상태처럼, README와 로드맵이 다른 곳이 있다.
이 저장소는 빠르게 바뀌고 있어(마지막 푸시는 2026년 10월 14일) 문서가 코드보다 늦게 따라가는 것으로 보인다.
쓰기 전에 설치한 버전의 `--help`와 `docs/API.md`를 기준으로 삼는 편이 안전하다.

### 영역별 규칙 수가 고르지 않다

분류 체계 YAML 파일 수는 영역별로 18개에서 1개까지 다르다.
Biased Baseline 영역은 파일이 하나뿐이다.
이 영역의 문제(누구의 목소리가 데이터에 들어 있는가)는 도구가 거의 점검하지 못할 수 있다는 뜻이지만, 이 문서는 도구를 실제로 돌려 확인하지는 않았다.
