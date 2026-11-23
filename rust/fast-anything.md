# Fast-Anything

<https://github.com/EL4CTEO/fast-anything>

HN 토론: <https://news.ycombinator.com/item?id=50596155> (192점, 160개 댓글)

GN 토론: <https://news.hada.io/topic?id=37645>

## 소개

Fast-Anything은 Python, Node, Ruby 같은 앱을 프로파일링해서 느린 함수를 찾고,
코딩 에이전트에게 그 함수만 Rust로 옮기게 한 뒤,
원래 앱이 실제로 받은 호출을 다시 돌려 같은 결과가 나오는지 확인하고 바꿔 끼우는 도구이다.
README의 첫 문장은 전체를 Rust로 다시 쓰지 말고 느린 5%만 다시 쓰라는 것이다.
GitHub API 기준으로 저장소는 2026년 11월 21일에 만들어졌고 라이선스는 MIT이며,
이 문서를 쓸 때 별 2,431개를 받았다.

GitHub의 homepage 항목은 npm 패키지 페이지를 가리킨다.
이 페이지는 Cloudflare 확인 창에 막혀 열지 못했고, 별도의 프로젝트 사이트는 확인하지 못했다.
이 문서는 README를 근거로 쓴다.

README가 내세우는 이유는 다음과 같다.
앱 전체를 Rust로 다시 쓰면 몇 달이 걸리고 컴파일이 길고 `target/` 용량이 크지만
실행 시간의 대부분은 몇 개의 함수에 있다는 것이다.

## 사용법

설치는 npm이나 Cargo로 한다.

```bash
npm i -g @el4cteo/fast-anything
# 또는
cargo install fast-anything
```

포팅한 코드는 사용자의 Rust 도구 체인(`rustup`)으로 컴파일된다.
한 번에 돌리는 명령은 다음과 같다.

```bash
fast-anything go --agent claude -- python app.py
```

단계별 명령은 다음과 같다.

| 명령               | 하는 일                                                                          |
| ------------------ | -------------------------------------------------------------------------------- |
| `scan -- <cmd>`    | 앱을 프로파일링해 시간과 이식 용이성으로 함수 순위를 매긴다                      |
| `port [id]`        | 실제 호출을 최대 500개 기록하고 함수 하나짜리 Rust 크레이트와 `TASK.md`를 만든다 |
| `verify`           | 포트를 릴리스 빌드해 기록한 호출을 모두 재생한다                                 |
| `enable`/`disable` | Rust를 끼우거나 뺀다. 표시된 한 블록이고 바이트 단위로 원복된다                  |
| `bench`            | 원래 앱과 Rust 적용 앱의 전체 시간을 번갈아 잰다                                 |
| `report`           | PR용 마크다운과 SVG 카드를 만든다                                                |
| `doctor`           | Rust, 런타임, 에이전트를 점검한다                                                |

`--agent`에는 `claude`, `codex`, 또는 표준 입력에서 프롬프트를 읽는 아무 명령을 쓸 수 있다.
에이전트 없이 쓰면 `TASK.md`를 원하는 도구에 넘기면 된다.

## 주요 기능

### 검증

README는 증거 없이 믿지 말라는 취지로 검증을 강조한다.
한 포트가 문자가 아니라 바이트를 비교해서 틀렸는데,
기록한 호출 500개 중 148개가 이를 잡았다고 한다.
기록한 호출 위에 가장자리 값(NaN, 무한대, 음의 0, 비ASCII 텍스트, 빈 입력, 최대 16배 큰 입력)과
줄인 입력을 만들어 원래 코드가 답하게 하며,
모든 경우가 일치해야 활성화된다.
값은 같아야 하고(부동소수점은 1e-9 이내) 원래 오류를 내는 곳에서는 오류를 내야 한다.
호출당 시간이 원래보다 느리면 활성화되지 않는다.
`FAST_ANYTHING_DISABLE=1`로 언제든 원래 코드를 돌릴 수 있다.

### 측정 결과

README의 결과는 i5-10500, Windows 11에서 재었고
C와 C++은 4코어 GitHub Actions Linux 러너에서 재었다고 한다.

| 앱                                | 전     | 후            |
| --------------------------------- | ------ | ------------- |
| Python 유사 이름 중복 제거(700개) | 4.91초 | 42ms, 116배   |
| TypeScript(2,000개)               | 3.11초 | 155ms, 20배   |
| PHP(600개)                        | 2.94초 | 53ms, 55배    |
| Go(3,000개)                       | 3.02초 | 144ms, 21배   |
| Ruby(400개)                       | 3.13초 | 228ms, 14배   |
| C#(4,000개)                       | 4.03초 | 312ms, 13배   |
| Java(4,000개)                     | 3.50초 | 1.18초, 3배   |
| C 만델브로트                      | 431ms  | 127ms, 3.4배  |
| C++(6,000개)                      | 3.02초 | 1.09초, 2.7배 |

Java는 함수만 보면 11배이고 나머지는 JVM 시작 시간이라고 한다.
가장 바깥 반복문을 옮겨 Rust로 한 번만 넘어가게 하며,
안쪽 `levenshtein`만 옮기면 35배와 1.9배였다고 한다.

### 지원 범위

Python 3.10 이상(PyO3), JavaScript와 TypeScript(Node 22 이상, Bun, Deno 2 이상, napi-rs),
Ruby 3.3 이상, Java 22 이상, Kotlin, Go 1.22 이상, PHP 8.1 이상,
C와 C++, C#과 .NET 8 이상, R 4.0 이상이다.
Ruby부터는 JSON을 주고받는 C 입구 하나를 가진 Rust 라이브러리로 연결한다.
옮기는 대상은 일반 데이터(숫자, 문자열, 목록, 사전)를 받는 최상위의 결정적 함수이고,
옮길 수 없는 것은 `scan`이 이유를 알려 준다.

에이전트 연동은 Claude Code 플러그인, 내장 MCP 서버(도구 8개), 에이전트에게 순서를 가르치는 스킬이다.

## 분석

### 도구의 위치

이 도구가 겨냥하는 틈은 전체 재작성과 아무것도 안 하는 것 사이이다.
프로파일링, 포팅, 검증, 교체, 되돌리기를 한 흐름으로 묶고
포팅 자체는 에이전트에게 맡긴다.
핵심 설계는 모델이 만든 코드를 믿지 않고 실제 호출 기록으로 검증한다는 점이다.
README의 148/500 사례는 그 검증이 실제로 오류를 잡았다는 근거로 제시되지만
이는 저자 자신의 보고이다.

### 측정의 범위

표의 모든 앱은 이름 유사도 중복 제거 같은 계산 중심 작업이거나 만델브로트이다.
글자 비교와 반복 계산은 Rust에서 이득이 크게 나는 종류이다.
입출력이나 네트워크가 지배적인 앱에서의 결과는 README에 없다.

## 비평

### 병목이 한곳에 있는가

ThouYS는 이 방식으로 풀 수 있는 병목은 쉬운 것이라 금방 해결되고,
진짜 성능 문제는 시스템 전체에 모래처럼 퍼져 있다고 했다.[^ThouYS]
jodrellblank는 Edge 브라우저에서 일하던 사람의 말을 인용해,
성능 회귀가 같은 함수에서 시간이 늘어나는 모습으로 나타나고
핫스팟이 없는 평평한 프로필이 된다고 했다.[^jodrellblank]
IshKebab은 Python의 핫스팟을 고쳐도 이후 느림이 프로그램 전체에 고르게 퍼진다며
일부만 옮겨 해결되는 경우가 많지 않다고 했다.[^IshKebab-sand]
README는 처음에 핫스팟이 있는 앱을 전제로 하며 그렇지 않은 앱은 `scan`의 순위에서 드러날 것이다.

### 같은 언어로 다시 쓰기

zodwick은 대부분의 코드베이스가 같은 언어로 성능을 염두에 두고 다시 쓰면
50% 빨라질 수 있다고 했고 느린 것은 언어보다 선택이라고 보았다.[^zodwick]
rafram은 uv가 Rust로의 재작성 덕이 아니라 동적 기능 제거와 입출력 개선으로 빨라졌다고 했다.[^rafram]
nicoburns는 둘 다이며 같은 구조의 Python을 Rust로 옮기면 종종 10배 빨라진다고 했다.[^nicoburns]
Eridrus는 같은 언어로 10%, 5%씩 개선해도 만족하지 못해
Python 파이프라인을 Rust로 바꿔 고객에 따라 50배 이상 빨라졌다고 했다.[^Eridrus]
이 논쟁은 README의 표가 어느 쪽에 가까운지 직접 말해 주지는 않는다.

### 실제로 흔한 문제인가

tripledry는 일하면서 Node나 Python 때문에 심한 느림을 본 적이 거의 없고
네트워크, 데이터베이스, 나쁜 구조가 더 큰 원인이었다고 했다.[^tripledry]
FartyMcFarter는 CPU가 병목이면 Python이 C, C++, Rust보다 보통 10~100배 느려
눈에 띄며 병목이 아니면 느끼지 못할 수도 있다고 답했다.[^FartyMcFarter]
두 답은 모순이 아니라 병목의 종류가 다르다는 뜻이다.
도구의 효용은 CPU 병목이 있는 앱에 한정된다.

### 메모리 안전과 속도

ezbie는 Rust로 다시 쓰는 이유가 속도가 아니라 메모리 안전이라고 했다.[^ezbie]
IshKebab은 메모리 안전, 성능, 논리적 정확성의 세 이유가 있고
사람들이 속도 때문에도 다시 쓴다고 반박했다.[^IshKebab-reasons]
iagiagiag은 속도만을 위해 문자열 처리에서 Rust 버전으로 병목을 없앴고
AI 덕에 쉬웠다고 했다.[^iagiagiag]
Fast-Anything은 속도를 목적으로 한다.
대상 언어가 이미 메모리 안전한 경우 안전의 이득은 이 도구의 주장이 아니다.

### 보호 장치의 한계

virtualritz는 LLM이 인간처럼 소유권과 불변식을 추적하는 데 약하고
Rust가 이를 막아 준다고 했다.[^virtualritz]
이 장치는 포트의 컴파일 단계에서 도움이 되지만
의미가 같은지는 결국 기록한 호출과 파생 사례의 범위가 정한다.
기록에 없는 입력에서의 동작은 README의 검증이 보장하지 않는다.

## 인사이트

### 도입 전 확인

CPU 병목이 있고 입력이 기록 가능한 앱에서만 시도할 가치가 크다.
먼저 `scan`으로 상위 함수가 전체 시간의 큰 비중을 차지하는지 보고,
`verify`가 통과한 뒤 `bench`로 전체 앱 시간이 줄었는지 확인하는 순서가 안전하다.
`disable`과 환경 변수로 되돌릴 수 있다는 점이 위험을 줄인다.

### 확인할 관찰

1. 실제 앱(입출력이 많은 서버 등)에서 전체 시간이 얼마나 줄어드는지.
2. 기록한 호출에 없던 입력에서 포트가 원래 코드와 일치하는지.
3. 에이전트가 만든 포트의 유지보수 비용이 시간이 지나며 어떻게 되는지.
4. README의 측정이 다른 환경에서 재현되는지.

위 넷 모두 이 문서가 확인하지 못했다.

---

[^ThouYS]: <https://news.ycombinator.com/item?id=50598795>

[^jodrellblank]: <https://news.ycombinator.com/item?id=50599870>

[^IshKebab-sand]: <https://news.ycombinator.com/item?id=50599345>

[^zodwick]: <https://news.ycombinator.com/item?id=50599553>

[^rafram]: <https://news.ycombinator.com/item?id=50599734>

[^nicoburns]: <https://news.ycombinator.com/item?id=50599683>

[^Eridrus]: <https://news.ycombinator.com/item?id=50603915>

[^tripledry]: <https://news.ycombinator.com/item?id=50597767>

[^FartyMcFarter]: <https://news.ycombinator.com/item?id=50597799>

[^ezbie]: <https://news.ycombinator.com/item?id=50600566>

[^IshKebab-reasons]: <https://news.ycombinator.com/item?id=50602162>

[^iagiagiag]: <https://news.ycombinator.com/item?id=50603485>

[^virtualritz]: <https://news.ycombinator.com/item?id=50598194>
