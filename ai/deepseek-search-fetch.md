# DeepSeek Search & Fetch: 검색과 본문 수집을 건당 과금 API로

<https://api-docs.deepseek.com/guides/search/>

HN 토론: <https://news.ycombinator.com/item?id=50138531> (501점, 245개 댓글)

GN 토론: <https://news.hada.io/topic?id=35571>

## 소개

DeepSeek Search & Fetch는 에이전트와 RAG 애플리케이션에
실시간 웹 콘텐츠를 공급하는 두 개의 JSON API다.
Search API는 질의에 맞는 웹 페이지를 찾아 구조화된 결과로 돌려준다.
DeepSeek이 자체 검색 엔진을 쓴다고 밝혔다.
Fetch API는 웹 페이지 하나를 가져와 Markdown 본문으로 돌려준다.

두 API는 DeepSeek API와 같은 Bearer 인증을 쓴다.
기본 주소는 `https://api.deepseek.com`이고
엔드포인트는 `POST /v1/tools/search`와 `POST /v1/tools/fetch`다.
이 글은 가이드 페이지 하나를 바탕으로 하며,
전체 스키마는 별도의 API Reference 페이지에 있다고 문서가 안내한다.

문서가 보장하는 범위는 이렇다.
요청 필드의 형식과 범위, 응답 필드, 오류 코드, 과금 단위, 속도 제한이다.
문서가 말하지 않는 것은 검색 엔진의 색인 규모, 갱신 주기,
`rerank_score`의 산출 방식, Fetch가 JavaScript 렌더링을 처리하는지 여부다.

## 동작 방식

### 검색 요청과 질의 연산자

검색 질의는 검색 문법이 보존된 채로 그대로 전달된다.
그래서 질의 문자열 안에서 연산자를 쓸 수 있다.

| 연산자    | 예시                         | 효과                           |
| --------- | ---------------------------- | ------------------------------ |
| `site:`   | `DeepSeek site:github.com`   | 지정한 사이트로 한정           |
| `-site:`  | `DeepSeek -site:example.com` | 지정한 사이트 제외             |
| `-term`   | `DeepSeek -advertisement`    | 해당 단어가 든 페이지 제외     |
| `"..."`   | `DeepSeek "exact phrase"`    | 정확히 일치하는 구절           |
| `-"..."`  | `DeepSeek -"release notes"`  | 해당 구절이 든 페이지 제외     |
| `lang:`   | `DeepSeek lang:zh,en`        | 쉼표로 나열한 언어 코드로 한정 |
| `after:`  | `DeepSeek after:2025-01-01`  | 해당 날짜 이후 게시물          |
| `before:` | `DeepSeek before:2026-06-01` | 해당 날짜 이전 게시물          |

여러 사이트를 지정하려면 `site:` 절을 공백으로 띄우고 `OR`로 잇는다.
날짜는 연도만 적어도 되고 전체 날짜를 적어도 된다.
연산자는 서로 조합할 수 있다.

### 요청 필드

| 필드           | 필수 | 기본값    | 제약                                 |
| -------------- | ---- | --------- | ------------------------------------ |
| `query`        | 예   | 없음      | 유니코드 1~128자, 공백만으로는 불가  |
| `count`        | 아니 | 10        | 1~50                                 |
| `ori_question` | 아니 | 없음      | 1~128자, 질의 이해를 돕는 원래 질문  |
| `localization` | 아니 | 빈 문자열 | 결과를 현지화할 IP 주소              |
| `need_content` | 아니 | false     | false이면 `content`는 항상 빈 문자열 |

알 수 없는 필드는 무시된다.
오타가 난 필드 이름이 오류 없이 통과한다는 뜻이다.

### 응답 필드

성공하면 HTTP 200과 `results` 배열이 온다.
일치하는 결과가 없을 때의 빈 배열도 정상 응답이다.
각 결과는 다음 필드를 가진다.

| 필드           | 의미                                                       |
| -------------- | ---------------------------------------------------------- |
| `rerank_score` | 0~3 관련도 점수, 1.5 이상을 고품질로 본다                  |
| `snippet`      | 100~200자 정도의 짧은 요약, UI 표시용                      |
| `summary`      | 600~800자 정도의 긴 요약, 모델이 읽는 용도                 |
| `content`      | 페이지 본문, `need_content`가 false이거나 없으면 빈 문자열 |
| `authority`    | 0~4 권위 등급, -1은 알 수 없음, 3 이상이 고권위            |
| `date`         | UTC RFC 3339 게시 시각, 모르면 null                        |
| `site_name`    | 사이트 이름, 없으면 null                                   |

`title`, `url`, `site_icon`도 함께 온다.
문서는 `snippet`을 사람용, `summary`를 모델용으로 구분해 둔다.
`rerank_score`는 관련성, 권위, 최신성 같은 신호를 합친 값이라고 설명한다.

### Fetch 요청과 응답

요청 필드는 `url` 하나다. 8192자 이하의 HTTP 또는 HTTPS 주소여야 하고
호스트가 있어야 하며 사용자 이름이나 비밀번호를 담을 수 없다.
응답은 `title`과 `content`다.
제목을 알 수 없으면 `title`은 빈 문자열이고,
`content`는 Markdown 텍스트다.

## 사용하기

아래 코드는 검색으로 후보를 고른 뒤 상위 결과를 Fetch로 읽는 흐름이다.
재시도 대상은 문서가 정한 기준을 따른다. 408, 429, 5xx는 기다렸다 재시도하고,
402와 나머지 4xx는 재시도하지 않는다.

```python
import os
import time

import requests

BASE = "https://api.deepseek.com/v1/tools"
HEADERS = {"Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}"}
RETRYABLE = {408, 429, 500, 502, 503, 504}


def call(path: str, body: dict, attempts: int = 4) -> dict:
    for attempt in range(attempts):
        resp = requests.post(
            f"{BASE}/{path}", headers=HEADERS, json=body, timeout=30
        )
        if resp.status_code == 200:
            return resp.json()
        # 문서 기준: 408, 429, 5xx만 기다렸다 재시도한다.
        # 402(잔액 부족)와 그 외 4xx는 요청을 바꾸기 전에는 재시도하지 않는다.
        if resp.status_code not in RETRYABLE or attempt == attempts - 1:
            resp.raise_for_status()
        time.sleep(2**attempt)  # 지수 백오프: 1, 2, 4초
    raise RuntimeError("unreachable")


def search_then_read(question: str, min_score: float = 1.5, top: int = 3):
    found = call(
        "search",
        {
            "query": f"{question} lang:en after:2025",
            "count": 10,
            "ori_question": question[:128],  # 128자 제한
        },
    )["results"]
    # 1.5 이상을 고품질로 보라는 문서의 기준을 필터로 쓴다.
    good = [r for r in found if r["rerank_score"] >= min_score][:top]
    pages = []
    for r in good:
        page = call("fetch", {"url": r["url"]})
        pages.append((r["url"], page["title"], page["content"]))
        time.sleep(0.25)  # Fetch는 계정 5 QPS와 도메인별 제한이 따로 있다.
    return pages


if __name__ == "__main__":
    for url, title, content in search_then_read("DeepSeek V4 release"):
        print(url, title, len(content))
```

`need_content`를 `true`로 두면 검색 한 번에 본문까지 받는다.
이 경우 위 코드의 Fetch 호출을 건너뛸 수 있다.

## 값 정하기

| 값             | 시작값                 | 근거                                                               |
| -------------- | ---------------------- | ------------------------------------------------------------------ |
| `count`        | 10                     | 문서의 기본값이며, 가격에 영향이 없으므로 응답 크기와 지연만 본다  |
| `rerank_score` | 1.5 이상만 사용        | 문서가 고품질 결과의 기준으로 제시한 값                            |
| `authority`    | 사실 확인용이면 3 이상 | 문서가 고권위 출처의 기준으로 제시한 값                            |
| `need_content` | false                  | 요약만으로 고를 수 있으면 본문 전송을 피한다, 필요할 때만 true     |
| 백오프 시작    | 1초에서 두 배씩        | 문서는 “기다렸다 재시도”만 말하고 간격은 정하지 않으므로 임의 선택 |
| 동시 요청      | 검색 5, Fetch 5 이하   | 계정 단위 QPS 한도와 같다                                          |

`authority` 기준과 `rerank_score` 기준은 문서가 준 값이지만,
이 값이 내 질의 분포에서 좋은 컷오프인지는 문서가 말해 주지 않는다.
질의 샘플 수십 개로 점수 분포를 먼저 찍어 보고 컷오프를 조정해야 한다.

## 트레이드오프

### 검색에서 본문까지 받을 것인가

`need_content`를 켜면 호출이 하나 줄어든다.
검색 요청과 Fetch 요청은 각각 1,000건당 0.75달러로 같은 가격이므로,
검색 후 Fetch를 따로 부르면 한 건의 조사에 두 번 과금될 수 있다.
반대로 `count`는 가격에 영향을 주지 않으므로
결과 열 개의 본문을 모두 받아도 요금은 그대로다.

그렇다고 항상 켜는 쪽이 이득은 아니다.
응답 크기가 커지고, 모델에 넣을 본문을 고르기 전에 이미 전부 받게 된다.
문서는 검색이 돌려주는 `content`와 Fetch가 돌려주는 본문이
같은 품질인지 말하지 않는다.
둘의 차이는 직접 같은 주소로 비교해 봐야 안다.

### 실패가 무료라는 점의 범위

과금 단위는 성공한 요청이다.
HTTP 200이면서 결과가 있어야 과금 대상이므로,
빈 검색 결과와 실패와 시간 초과는 과금되지 않는다.
따라서 5xx 재시도는 비용을 늘리지 않는다.

하지만 429 재시도가 공짜라고 해서 마음껏 반복할 수는 없다.
한도는 계정 단위이며 API 키별로 나뉘지 않는다.
키를 여러 개 만들어도 한도가 늘지 않는다.

### 싼 가격이 곧 싼 선택은 아니다

HN 토론에서
사용자들이 비교 기준이 될 가격을 내놓았다. thombles는 Brave Search API가
1,000건당 5달러이고 Kagi API가 12달러라고 적었다.[^thombles]
단순 계산으로 DeepSeek의 0.75달러는 그 7분의 1에서 16분의 1 수준이다.

하지만
가격표는 품질을 말해 주지 않는다. ggnore7452는 자신의 웹 수집 벤치마크로 몇
가지를 돌려 보니 DeepSeek의 검색과 Fetch가 저렴하긴 해도 그다지 좋지 않았다고
적었다.[^ggnore7452]
대안으로는 무료인 Jina, 유료라면 Parallel, Firecrawl, Tavily, Exa를 꼽았다.
벤치마크의 질의와 지표는 스레드에 없으므로 이 평가를 검증할 수는 없다.

vitorsr는 의미 기반 검색을 위해 Exa에 웃돈을 낸다고 밝혔다.
Exa의 `objective` 필드는 최대 4096자인데
여기의 `ori_question`은 128자로 제한된다는 대비도 짚었다.[^vitorsr]
질의 의도를 얼마나 길게 전달할 수 있는지가
검색 품질을 가르는 변수일 수 있다는 뜻이다.

Havoc은 SearXNG를 직접 운영하다가 호스팅 검색 API와 비교해 보고 접었다.
SearXNG는 속도 제한에 금방 걸리고,
닿을 수 있는 검색 제공자에 따라 결과가 들쭉날쭉했다고 한다.[^Havoc]
무료 대안이 늘 싼 것은 아니라는 같은 이야기를 반대쪽에서 확인해 준다.

이 글은 요청당 가격이 아니라 정답 하나당 비용으로 비교해야 한다고 본다.
같은 질의 50개를 후보 API 셋에 돌리고 사람이 정답 여부를 채점하면
가격표로는 보이지 않는 차이가 드러난다.

### 5 QPS는 에이전트 한 대분의 한도다

josteink는 초당 5건이면 동시 사용자가 많은 앱에는 쓸 수 없지 않느냐고
물었다.[^josteink] alexjurkiewicz는 에이전트용이라고
짧게 답했다.[^alexjurkiewicz] hobofan은
이런 호스팅 제공자를 쓰는 이유를 설명했다.
지연 시간이 일정해야 하고,
회사 기밀이 새는 경로가 될 수 있어 데이터 처리 보증이 필요하며,
심층 조사 하나가 검색 10회 이상과
Fetch 100회 이상을 수행하기 때문이다.[^hobofan]

이 수치를 5 QPS에 대 보면 Fetch 100회는 계정 한도만 보아도 최소 20초다.
도메인별 한도까지 걸리면 더 늘어난다.
사람이 기다리는 챗봇에서는 심층 조사를 몇 개 동시에 돌릴 수 없으므로
요청 대기열과 사용자별 동시 실행 수 제한이 설계에 들어가야 한다.

### 무료 구간의 불확실성

DeepSeek Harness, Claude Code, Codex로 DeepSeek API를 쓰면
서버 측 도구 호출이 이 두 API를 이미 호출하고 있고,
그 호출은 현재 무료다.
건당 과금은 베이징 시간 2026년 11월 1일 0시에 시작한다.

문서는 직접 API를 호출하는 경우가 이 기한까지 무료인지 적지 않았다.
무료라는 문장은 하네스를 거치는 경우를 설명하는 대목에 붙어 있다.
직접 호출을 계획한다면 첫 청구서가 올 때까지
무료라고 가정하지 않는 편이 안전하다.

## 함정

### 알 수 없는 필드가 조용히 무시된다

필드 이름을 틀려도 400이 아니라 기본값으로 동작한다.
예를 들어 `need_contents`로 잘못 쓰면 `content`는 빈 문자열이고,
오류는 나지 않는다.
응답에서 `content` 길이를 검사해 이 실수를 잡는 것이 좋다.

### 빈 `content`가 두 가지 의미를 가진다

`content`는 `need_content`가 false일 때와
본문을 가져오지 못했을 때 모두 빈 문자열이다.
빈 문자열만으로는 어느 쪽인지 알 수 없다.
요청에서 `need_content`를 켰는데도 비어 있다면 후자이므로
Fetch로 다시 시도하는 분기가 필요하다.

### 404가 서로 다른 원인을 합친다

Fetch의 404는 접근할 수 없는 URL, 사이트 정책이 막은 URL, 대상 사이트의 오류,
지원하지 않는 콘텐츠 형식,
추출할 Markdown이 없는 페이지를 모두 포함한다.
403은 보안 정책이 요청을 거부한 경우로 따로 있다.
재시도로 풀리지 않는 4xx이므로 같은 주소를 반복해서 부르면 안 된다.

### 날짜와 권위가 비어 있을 수 있다

`date`는 모르면 null이고 `authority`는 -1일 수 있다.
`after:` 연산자로 거른 결과에서도 `date`를 믿고 정렬하는 코드는
null에서 깨질 수 있다.

### Fetch에는 이중 속도 제한이 있다

Fetch는 계정 5 QPS에 더해 도메인별 QPS 제한을 받는다.
같은 사이트의 주소 열 개를 동시에 읽는
크롤러는 계정 한도 아래에서도 429를 받는다.
도메인별로 요청을 직렬화하거나 간격을 두어야 한다.

### 검색 결과 0건은 부재의 증거가 아니다

czk는 정치적으로 민감한 질의가 예상대로 결과 0건을 돌려줬다고 적었다.[^czk]
문서는 일치하는 결과가 없을 때의 빈 배열을 정상 응답이라고만 설명한다.
그래서 빈 배열은 일치하는 페이지가 없다는 뜻일 수도 있고
결과가 걸러졌다는 뜻일 수도 있다.
이것은 단일 관찰에서 나온 추론이며 DeepSeek이 확인한 사실은 아니다.
빈 결과로 어떤 사실의 부재를 결론짓기 전에,
존재가 확실한 질의를 같은 경로로 하나 돌려 대조해야 한다.

### Fetch 결과는 라이브 페이지와 다를 수 있다

shaunpud는 하이퍼링크가 있는 사이트를 가져왔더니
텍스트만 돌아와 쓸모가 줄었다고 적었다.[^shaunpud]
문서는 본문을 Markdown으로 돌려준다고만 설명하고
링크를 보존하는지는 말하지 않는다.
링크를 따라가며 수집하는 에이전트라면 먼저 한 페이지로 확인해야 한다.

czk는 Fetch의 동작도 관찰했다.
JavaScript를 실행하고,
Linux Firefox 149 사용자 에이전트에 중국어 언어 설정을 쓰며,
나가는 주소는 홍콩의 Huawei Cloud로 보인다고 했다.[^czk]
소개에서 문서가 말하지 않는다고 한 JavaScript 렌더링 여부에 대한 단서지만,
역시 한 사람의 관찰이다.

tyre는 문서의 자체 검색 엔진이라는 표현을 DeepSeek이 자체 색인을 만들고
캐시된 결과를 돌려준다는 뜻으로 읽었다.[^tyre]
이 해석이 맞다면 검색 결과의 본문이 지금 그 페이지의 모습이라는 보장이 없다.
문서는 어느 쪽인지 밝히지 않으므로,
최신성이 중요한 용도에서는 `date`와 원본 페이지를 함께 확인해야 한다.

## 확인하기

키가 있다면 아래 순서로 실제 동작을 확인한다.
이 명령은 과금될 수 있으므로 소량으로만 실행한다.

```bash
# 1. 연산자가 먹히는지: 결과 URL이 모두 github.com인지 본다
curl -s https://api.deepseek.com/v1/tools/search \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"DeepSeek site:github.com","count":5}' |
  python3 -c 'import json,sys; [print(r["url"]) for r in json.load(sys.stdin)["results"]]'

# 2. 알 수 없는 필드가 무시되는지: 오타 필드를 넣고 content 길이를 본다
curl -s https://api.deepseek.com/v1/tools/search \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"DeepSeek","count":1,"need_contents":true}' |
  python3 -c 'import json,sys; print(len(json.load(sys.stdin)["results"][0]["content"]))'

# 3. 범위 검증: count=51이면 400이 와야 한다
curl -s -w '\n%{http_code}\n' https://api.deepseek.com/v1/tools/search \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"DeepSeek","count":51}'
```

두 번째 명령이 0을 출력하고 오류가 없으면 문서대로 오타가 무시된 것이다.

## 체크리스트

- 응답 본문이 필요 없는 경로에서는 `need_content`를 false로 두었는가
- `content`가 빈 문자열일 때를 처리하는 분기가 있는가
- `date`가 null인 결과를 정렬과 필터에서 견디는가
- 재시도 대상이 408, 429, 5xx로 한정되어 있는가
- 402와 나머지 4xx를 재시도하지 않는가
- 같은 도메인에 대한 Fetch 요청을 직렬화했는가
- 검색과 Fetch가 각각 초당 5건을 넘지 않는가
- 2026년 11월 1일 이후의 호출 수와 월 비용을 계산해 두었는가
- 고품질 컷오프(`rerank_score` 1.5)를 내 질의로 검증했는가

## 기억할 원칙

### 과금 단위가 설계의 모양을 정한다

토큰이 아니라 성공한 요청 수로 과금되는 도구는
호출 횟수를 줄이는 쪽보다 낭비되는 호출을 막는 쪽이 중요하다.
`count`가 공짜라면 결과를 넉넉히 받아 한 번에 고르고,
실패가 공짜라면 재시도를 관대하게 두되 한도는 지켜야 한다.
비용 구조를 먼저 읽고 호출 패턴을 거기에 맞춘다.

### 문서가 말하지 않은 경계는 직접 재 본다

이 문서는 필드와 한도는 정확하지만,
검색 품질, 본문 추출 품질, 직접 호출의 무료 여부는 말하지 않는다.
말하지 않은 부분을 가정으로 채우지 말고,
작은 실험으로 확인한 뒤 의존한다.

---

[^thombles]: <https://news.ycombinator.com/item?id=50138776>

[^ggnore7452]: <https://news.ycombinator.com/item?id=50144703>

[^vitorsr]: <https://news.ycombinator.com/item?id=50139740>

[^Havoc]: <https://news.ycombinator.com/item?id=50139972>

[^josteink]: <https://news.ycombinator.com/item?id=50139300>

[^alexjurkiewicz]: <https://news.ycombinator.com/item?id=50139304>

[^hobofan]: <https://news.ycombinator.com/item?id=50139481>

[^czk]: <https://news.ycombinator.com/item?id=50141678>

[^shaunpud]: <https://news.ycombinator.com/item?id=50140468>

[^tyre]: <https://news.ycombinator.com/item?id=50138791>
