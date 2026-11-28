# LMQL: LLM 프로그래밍 언어

<https://lmql.ai/>

<https://github.com/eth-sri/lmql>

HN 토론: <https://news.ycombinator.com/item?id=35956484> (108점, 12개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=35484673> (26점, 6개 댓글)

GN 토론: <https://news.hada.io/topic?id=9185>

## 소개

LMQL은 취리히연방공대(ETH Zurich)의 SRI Lab이 기여자들과 함께 만든 오픈소스
프로그래밍 언어이다.
사이트 첫 화면은 LMQL을 LLM을 위한 프로그래밍 언어로 소개하고,
타입, 템플릿, 제약(constraint), 최적화 런타임을 써서 프롬프트를 견고하고
모듈식으로 쓸 수 있다고 말한다.
저장소 README는 LMQL이 파이썬의 상위 집합(superset)에 기반한 언어라고 적는다.
GitHub에는 홈페이지 주소가 `https://lmql.ai`로 등록되어 있고,
저장소 설명문은 제약으로 유도하는 효율적인 LLM 프로그래밍 언어라고 되어
있다.[^github-api]

Playground, 나머지 문서 장, 논문 본문은 열지 않았고 프로그램을 직접 실행하지도
않았다.

## 주요 기능

### 프롬프트가 곧 프로그램이다

LMQL 프로그램에서 최상위 문자열은 프롬프트이고,
`[RESPONSE]` 같은 템플릿 변수는 모델이 채운다.
문장 하나가 실행되면 그 안의 변수는 바깥 프로그램에서 바로 읽을 수 있어서 `if`와
`for` 같은 제어 흐름에 쓸 수 있다.
문서는 LLM을 호출할 때마다 그때까지의 모든 프롬프트 문장을 이어 붙인 것이
프롬프트가 된다고 설명한다.[^docs-start]

### where 절과 제약

생성 결과에 대한 조건은 `where` 절에 쓴다.
제약 장이 소개하는 것은 멈춤 문구(`STOPS_AT`, `STOPS_BEFORE`), 정수 타입(`INT`),
집합 안의 선택(`in set(...)`), 문자 길이(`len`)이다.[^docs-constraints]
시작하기 장은 `len(...) < 25` 같은 문자 단위 조건을 하위 토큰 마스크로 바꿔 생성
중에 곧바로 적용한다고 설명한다.[^docs-start]
제약 장은 타입 제약으로는 정수만 지원하고 실수와 다른 타입은 이후 릴리스에서
계획한다고 적는다.[^docs-constraints]

### 디코더

쿼리의 첫 키워드로 디코딩 알고리즘을 정한다.
문서가 소개하는 것은 `argmax`(기본값), `sample`, `beam`, `beam_sample`이다.
디코더는 쿼리 전체에 적용되고 프로그램 안에서 바꿀 수 없어서,
부분마다 다른 디코더를 쓰려면 쿼리를 나눠야 한다.
문서가 따로 소개하는 새 디코더는 실험적이며 버전 사이에 안정성을 보장하지
않는다고 한다.[^docs-decoding]

### 중첩 질의와 부가 API

2023년 10월 10일의 0.7 릴리스 글은 중첩 질의(nested query)를 내세운다.
다른 쿼리를 함수처럼 부르면, LMQL이 그 쿼리의 지시문과 제약을 바깥 쿼리에 넣어
값을 생성한 뒤 다시 지우고 최종 결과만 돌려준다고 한다.
글은 이를 함수 호출과 스택 풀기(stack unwinding)에 빗대고,
중간 지시문을 감추면 모델이 지금 필요한 정보에 집중한다고 말한다.[^blog-07]
같은 글은 LMQL 문법 없이 생성과 점수 계산을 하는 Generations API,
챗봇용 Chat API, 추론 결과를 다시 만들 수 있게 기록하는 추론 인증서(inference
certificate)도 소개한다.[^blog-07]

### 백엔드

모델은 `lmql.model(...)`로 고른다.
문서의 예시는 OpenAI API(`openai/...`), llama.cpp(`llama.cpp:<가중치>.gguf`),
프로세스 안의 Transformers(`local:gpt2`), `lmql serve-model`로 띄운 Transformers
모델이며, Azure OpenAI와 Replicate 장도 따로 있다.
모델은 `@lmql.query(model=...)`로 코드 밖에서 정하거나,
쿼리 안의 `from` 절로 정한다.[^docs-models]

## 사용법

README는 파이썬 3.10이 필요하다고 적고, 설치는 `pip install lmql`이며 로컬 GPU
모델에는 `pip install lmql[hf]`를 쓴다.
`lmql playground`는 브라우저 IDE를 띄우며 Node.js가 필요하고,
`lmql run`은 로컬 `.lmql` 파일을 실행한다.
OpenAI 모델을 쓰려면 `OPENAI_API_KEY` 환경 변수나 `api.env` 파일이 필요하다.

```bash
pip install lmql
lmql playground
lmql run my_query.lmql
```

사이트 첫 화면의 짐 목록 예제는 `where` 절로 선택지를 고정한다.
사이트가 보여 주는 출력은 Volleyball, Bathing Suit, Sunscreen, Volleyball이며,
같은 항목이 반복되어도 제약 위반이 아니다.

```python
# top level strings are prompts
"My packing list for the trip:"

# use loops for repeated prompts
for i in range(4):
    # 'where' denotes hard constraints enforced by the runtime
    "- [THING] \n" where THING in \
        ["Volleyball", "Sunscreen", "Bathing Suit"]
```

0.7 릴리스 글의 중첩 질의 예제는 사고 사슬(chain of thought) 프롬프트를 함수로
분리한다.

```python
import lmql

# chain of thought prompting strategy
@lmql.query
def chain_of_thought():
    '''lmql
    "A: Let's think step by step.\n [REASONING]"
    "Therefore the answer is [ANSWER]" where STOPS_AT(ANSWER, ".")
    return ANSWER.strip()
    '''

# top-level query
"Q: It is August 12th, 2020. What date was it \
    100 days ago? [ANSWER: chain_of_thought]"
ANSWER # May 4th, 2020
```

## 프로젝트 상태

2026-11-21에 읽은 값은 다음과 같다.
GitHub API는 별 4,226개, 포크 223개, 이슈와 풀 리퀘스트를 합친 열린 항목 122건,
라이선스 Apache-2.0, 저장소 생성일 2022-11-24를 보고했다.[^github-api]
GitHub의 최신 릴리스는 2023-10-14의 v0.7.3이고,[^github-releases] PyPI의 최신
버전도 0.7.3이며 요구 파이썬은 3.10 이상이다.[^pypi]
저장소의 최근 커밋은 2025-05-22의 README 수정이고,
그 앞은 2024-05-09의 문서 추가와 쿼리 빌더 작업 중 커밋이다.[^github-commits]
블로그의 마지막 글은 2024년 2월 14일의 개발자 설문 안내이다.[^blog-survey]
사이트 첫 화면은 지금도 다음 주요 버전을 만들기 위한 개발자 설문을 안내하는
배너를 띄운다.

## 분석

### 제약은 문자 조건을 토큰 마스크로 바꿔 생성 중에 적용한다

문서에 따르면 LMQL은 `len(RESPONSE) < 25` 같은 문자 단위 제약을 하위 토큰
마스크로 바꾸어 생성 중에 바로 적용한다.[^docs-start]
README는 이를 logit 마스킹이라고 부른다.
모델이 다음 토큰의 확률 분포를 내놓을 때 제약에 어긋나는 토큰을 후보에서
지운다는 뜻으로 읽힌다. 이는 이 문서의 풀이이다.
이 방식이 통하려면 백엔드가 토큰별 분포를 보여 주고 마스크를 받아 줘야 한다.

OpenAI 장은 이 전제가 API마다 다르다는 것을 보여 준다.
완결(Completions) API는 로짓 편향을 300개까지만 받고 토큰마다 상위 5개의 로그
확률만 돌려주므로, 마스크가 300개를 넘으면 LMQL이 앞의 300개만 남기고 경고를
출력한다.[^docs-openai]
그래서 LMQL은 생성을 청크로 나누어 청크마다 제약을 검증하고 이어 가는
투기적(speculative) 방식을 쓴다.
기본 청크는 32토큰이며, 제약을 어기면 생성한 토큰을 버려야 하므로 비용이 든다고
문서는 설명한다.[^docs-openai]
같은 `where` 절이 로컬 모델에서는 후보를 미리 막는 일이고,
API에서는 마스크와 사후 검증이 섞인 일이 되는 것이다.
2023년 HN 스레드에서 저자 lbeurerkellner는 마스킹이 디코딩 루프 안에서
토큰 단위로 일어나므로, 나중에 버려야 할 불필요한 이어쓰기가 줄어 효율이
생긴다고 설명했다.[^lbeurerkellner-efficiency]
mike_hearn은 OpenAI 모델에서 토큰마다 로짓 편향을 바꾸려면 추론을 처음부터
다시 시작해야 해서 비용이 선택지 수에 곱해지지 않느냐고 물었다.[^mike_hearn]
저자는 구간 단위로 제약을 늦게 검증하고 필요하면 되돌린다고 답했다.
그러면서 한 번에 요청하는 것보다 비싸며, 이는 LMQL이 아니라 OpenAI API의
한계라고 했다.
쿼리 프로그램을 추론 서비스로 보내 모델 전체에 접근해 실행하는 방식이
이상적이라고도 덧붙였다.[^lbeurerkellner-cost]

### 프롬프트의 이력이 프로그램의 상태이고 중첩 질의가 그것을 줄인다

문서는 LLM을 호출할 때마다 지금까지의 모든 프롬프트 문장을 이은 것이 프롬프트가
된다고 설명한다.[^docs-start]
따라서 지시문과 중간 결과가 문맥에 계속 남고,
프로그램의 상태가 곧 늘어나는 문자열이다.
중첩 질의는 호출된 쿼리의 지시문과 제약을 일시적으로 넣었다가 지운다.[^blog-07]
이 문서는 이것을 이 언어의 범위(scope) 장치로 읽는다.
변수가 아니라 문맥 창(context window)이 호출 사이에서 나눠 쓰는 자원이고,
중첩 질의는 그 자원을 되돌려 주는 수단이라는 해석이다.

### 평가는 연구 논문에 기대고 있다

연구 페이지는 논문 네 편을 올려 두었다.
LMQL을 처음 설명한 PLDI 2023 논문, ICML 2023 워크숍의 LMQL Actions(도구 호출)와
LMQL Chat, 2023년 11월 arXiv에 올라온 프롬프트 스케치(prompt sketching)이다.
PLDI 논문의 초록은 정확도를 유지하거나 높이면서 비용을 26%에서 85%까지 줄였다고
하고, 프롬프트 스케치의 초록은 여덟 개 벤치마크 가운데 일곱 개에서 기존 순차
프롬프트보다 낫다고 한다.[^research]
이는 저자들이 고른 과제에 대한 저자들의 보고이다.

## 비평

### 같은 문법이 백엔드마다 다른 보장을 준다

사이트 첫 화면은 LMQL 코드가 여러 백엔드에서 이식되며 한 줄로 바꿀 수 있다고
말한다.
OpenAI 장은 Chat API 모델(`gpt-3.5-turbo`, `gpt-4`)이 제약을 온전히 지원하지
않는다고 적는다.
`STOPS_AT`, `STOPS_BEFORE`, `len(TOKENS(...)) < N` 같은 단순한 제약만 되고,
복잡한 제약은 강제할 수 없어 LMQL이 콘솔에 오류를 출력한다는
것이다.[^docs-openai]
따라서 이식되는 것은 문법이고 제약의 보장은 백엔드에 따라 달라진다.
사이트 첫 화면에는 이 한정이 보이지 않는다.

### 문서의 서술과 예제가 어긋난 곳이 있다

시작하기 장의 첫 쿼리는 설명문에서 `len(RESPONSE) < 10`과 `len(RESPONSE) < 25`를
말하지만, 코드에는 `len(TOKENS(RESPONSE)) < 25`가 적혀 있다.[^docs-start]
README는 파이썬 3.10을 설치 조건으로 적는데 PyPI 메타데이터의 요구 버전은 3.10
이상이다.[^pypi]
OpenAI 장이 시험했다고 적은 모델은 text-ada-001과 text-davinci 계열,
gpt-3.5-turbo-instruct, gpt-3.5-turbo, gpt-4이다.[^docs-openai]
모델 개요 장의 예시에는 text-davinci-003이 쓰인다.[^docs-models]

### 유지 상태를 판단할 근거가 엇갈린다

최신 릴리스는 2023-10-14의 0.7.3이고 2026-11-21까지 3년 남짓 새 릴리스가
없다.[^github-releases]
블로그의 마지막 글은 다음 주요 버전을 위한 설문 안내이고,[^blog-survey] 사이트
첫 화면은 같은 설문 배너를 아직 보여 준다.
반대로 별이 4,226개이고 2025-05-22에 README가
수정되었다.[^github-api][^github-commits]
다음 버전이 다른 가지(branch)나 디스코드에서 개발되고 있는지는 확인하지 못했다.
그래서 이 도구에 의존하려는 사람은 릴리스 공백을 먼저 알아야 한다.

### 비용과 정확도 수치는 저자의 보고뿐이다

26%에서 85%라는 비용 절감은 PLDI 논문 초록의 수치이다.[^research]
2023년의 모델과 API로 잰 값이 지금의 모델과 API에서도 성립하는지도 확인하지
못했다.

## 인사이트

### 구조화 출력이 API 기능이 된 뒤에 LMQL에 남는 질문

이 저장소의 [LLM 구조화 디코딩](structured-decoding.md) 문서는 구조화 출력이
샘플러가 문법에 어긋나는 토큰을 후보에서 지우는 방식이고,
보장되는 것은 문법이지 내용이 아니라고 정리한다.
LMQL의 `where` 절은 같은 기구를 언어 문법으로 드러낸 것으로 읽힌다.

HN에서 tehsauce는 어떤 언어로든 LLM을 프로그래밍할 수 있는데 새 쿼리 언어를
배울 이유가 무엇이냐고 물었다.[^tehsauce]
CGamesPlay는 파이썬을 대체하는 것이 아니라 SQL처럼 빔 서치와 제약된 응답 같은
기본 도구를 쉽게 쓰게 하는 것으로 보라고 답했다.[^CGamesPlay]
저자는 호출은 여전히 호스트 언어로 하고 LMQL은 여러 부분으로 된 프롬프트와
제약을 간결하게 정의하며 출력 파싱을 맡는다고 했다.[^lbeurerkellner-sql]

가장 강한 형태의 주장은 프롬프트를 문자열에서 프로그램으로 옮기면 제약의 보장과
호출 비용 절감을 함께 얻는다는 것이다.
근거는 문서의 설명과 2023년 논문의 보고이다.
그 근거는 백엔드가 토큰 분포와 마스크를 열어 줄 때까지만 이어진다.
문서가 Chat API는 분포도 이어 쓰기도 주지 않는다고 적었기
때문이다.[^docs-openai]
채팅 API에서 복잡한 제약이 지원되는 백엔드가 나온다면 이 판단은 바뀐다.

### 문법 확장의 비용은 도구가 치른다

LMQL 쿼리는 파이썬 안에서 `@lmql.query`를 붙인 함수의 `'''lmql` 문자열로 쓴다.
이 문서의 추정으로는 문자열 안의 코드에는 일반적인 파이썬 린터와 타입 검사기가
닿지 않는다. 이는 확인하지 않았다.
README는 브라우저 Playground IDE와 Visual Studio Code 확장을 도구로 든다.
언어를 새로 만드는 방식은 문법의 표현력을 얻는
대신 편집기 지원을 직접 만들어야 하는 비용을 진다.
killthebuddha가 Node.js에서 쓰기 어려운지 묻자,
저자는 LMQL에 자체 인터프리터와 런타임이 있고 파이썬 환경에 밀접하게
묶여 있어서 당시에는 파이썬 인터프리터를 하위 프로세스로 띄워야 한다고
답했다.[^killthebuddha][^lbeurerkellner-runtime]

0.7 릴리스 글의 Generations API는 LMQL을 한 줄도 쓰지 않고 생성과 점수 계산을
하게 한다.[^blog-07]
이 API가 새 언어를 배우지 않고 시작하려는 사용자를 위한 입구라는 것은 이 문서의
추정이다.

### 확인할 관찰

이 문서의 판단을 바꿀 관찰은 네 가지이다.
다음 주요 버전의 공개 또는 설문 결과를 담은 공식 글이 나오는지,
Chat API와 최근 모델에서 어디까지 제약이 지원되는지 문서가 갱신되는지,
다른 제약 생성 도구와 같은 과제로 비교한 독립 평가가 있는지,
문서의 시험 모델 목록과 시작하기 장의 코드가 현재 상태로 정리되는지이다.

---

[^github-api]: GitHub, [eth-sri/lmql 저장소 API](https://api.github.com/repos/eth-sri/lmql)

[^github-releases]: GitHub, [eth-sri/lmql 릴리스 API](https://api.github.com/repos/eth-sri/lmql/releases)

[^github-commits]: GitHub, [eth-sri/lmql 커밋 API](https://api.github.com/repos/eth-sri/lmql/commits)

[^pypi]: PyPI, [lmql](https://pypi.org/pypi/lmql/json)

[^docs-start]: LMQL, [Getting Started | LMQL](https://lmql.ai/docs/)

[^docs-constraints]: LMQL, [Constraints | LMQL](https://lmql.ai/docs/language/constraints)

[^docs-decoding]: LMQL, [Decoders | LMQL](https://lmql.ai/docs/language/decoding.html)

[^docs-models]: LMQL, [Overview | LMQL](https://lmql.ai/docs/models/)

[^docs-openai]: LMQL, [OpenAI | LMQL](https://lmql.ai/docs/models/openai.html)

[^blog-07]: LMQL, [LMQL 0.7 brings Procedural Prompt Programming](https://lmql.ai/blog), 2023-10-10

[^blog-survey]: LMQL, [LMQL Developer Survey](https://lmql.ai/blog), 2024-02-14

[^research]: LMQL, [Research | LMQL](https://lmql.ai/research)

[^lbeurerkellner-efficiency]: <https://news.ycombinator.com/item?id=35491190>

[^mike_hearn]: <https://news.ycombinator.com/item?id=35492009>

[^lbeurerkellner-cost]: <https://news.ycombinator.com/item?id=35492152>

[^tehsauce]: <https://news.ycombinator.com/item?id=35957843>

[^CGamesPlay]: <https://news.ycombinator.com/item?id=35957888>

[^lbeurerkellner-sql]: <https://news.ycombinator.com/item?id=35958139>

[^killthebuddha]: <https://news.ycombinator.com/item?id=35962996>

[^lbeurerkellner-runtime]: <https://news.ycombinator.com/item?id=35963612>
