# Hacker News 전체를 내려받아 DuckDB로 세어 보기

원문: [You Wouldn't Download a Hacker News](https://www.jasonthorsness.com/25)

HN 토론: <https://news.ycombinator.com/item?id=43840193> (458점, 227개 댓글)

GN 토론: <https://news.hada.io/topic?id=20643>

## 요약

Jason Thorsness가 2025년 4월 29일에 쓴 짧은 글이다.
제목은 불법 복제 반대 광고 문구를 빌려 왔고,
첫 소제목은 “TLDR: I Did Download It”이다.
글은 두 부분으로 되어 있다.
Hacker News 전체를 내려받은 과정과, 그 데이터를 DuckDB로 집계한 과정이다.

저자는 hn.unlurker.com을 만들면서 Go로 HN API 클라이언트를 작성했다.
이미 다른 클라이언트가 많았지만,
최신 Go 기능과 린터를 새 프로젝트에서 써 보고 싶었다고 한다.
HN API에서는 댓글과 스토리를 모두 아이템(item)이라고 부른다.
프로젝트에 필요한 것은 최근 아이템뿐이었지만,
완성도를 위해 0번부터 최신 아이템까지 순서대로 받는 `scan` 명령을 넣었다.
수천 개 아이템으로 어림해 보니 전체가 수십 GiB 정도의 JSON일 것 같아서
실제로 받아 보기로 했다.

```bash
hn scan --no-cache --asc -c- -o full.json
```

멈춘 다운로드를 몇 번 CTRL-C로 끊어야 했지만 `scan`은 이어받기가 되므로
몇 시간 만에 끝났다.
결과는 Hacker News에서 일어난 모든 것을 담은 20 GiB JSON 파일이었고,
같은 명령을 다시 실행하면 최신 아이템으로 언제든 채워 넣을 수 있다.

처음에는 grep으로 찾아봤다.
xkcd의 “correct horse battery staple”은 HN에 231번 등장했고,
마지막은 글을 쓴 당일이었다.
그다음 DuckDB를 써 봤다.
저자는 DuckDB를 아주 빠른 임베드형 분석 실행 엔진이자
명령줄 도구로도 쓸 수 있는 독특한 존재로 소개한다.
평소에는 다른 데이터베이스를 다룬다고 하며 SingleStore로 링크를 걸었다.
초보자를 위한 새 UI 덕분에 쓰기 쉬웠고,
LLM이 SQL 쿼리를 만드는 데 꽤 도움이 됐다고 적었다.
가져오기는 한 문장이다.

```sql
CREATE TABLE items AS
SELECT *
FROM read_json_auto('/home/jason/full.json', format='nd', sample_size=-1);
```

그다음 주 단위로 아이템을 묶고, 전체 아이템 중 `text`에
`python`, `javascript`, `java`, `ruby`, `rust`가 들어간 비율을
`ILIKE '%...%'`로 구한 뒤 12주 이동 평균을 냈다.
글머리의 “The Rise Of Rust” 그래프가 그 결과이고,
`mysql`, `postgres`, `mongo`, `redis`, `sqlite`를 같은 방식으로 센
“The Progression of Postgres” 그래프가 함께 실렸다.
두 그래프 모두 계열을 위로 쌓은 누적 그래프이며,
가로축은 2007년 5월 14일부터 2024년 5월 14일까지 1년 간격으로 눈금이 있다.
저자는 이 정도 크기의 데이터셋을 분석하는 데
DuckDB가 아주 좋아 보인다고 정리한다.

마무리는 농담이다.
이 데이터로 LLM 봇 수백 개를 학습시켜 참여자로 풀어 놓으면
과거를 끝없이 되풀이하는 중국어 방 발진기(chinese room oscillator)가
사람의 글을 서서히 대체할 것이라고 쓴 뒤,
이 프로젝트는 여기서 끝내고 다음 단계는 다른 사람에게 맡긴다고 했다.

## 동작 방식

### 아이템 하나가 JSON 한 줄이 된다

HN API는 스토리, 댓글, 구인 글, Ask HN, 투표까지 모두 아이템으로 다룬다.
아이템은 정수 id로 구분되고 `/v0/item/<id>.json`에 있다.
id가 순서대로 늘어나므로 0번부터 최댓값까지 차례로 요청하면 전체를 받을 수 있다.
API 문서는 Firebase와 함께 공개 데이터를 거의 실시간으로 제공한다고 밝히고,
현재 요청 수 제한이 없다고 적어 두었다.
krapp도 HN 토론에서 이 API는 요청 수 제한조차 없고
데이터가 YC 출신 회사인 Firebase에 있으니 괜찮다고 답했다.[^krapp]

필드 구성이 아이템 종류마다 다르다는 점이 집계에서 중요하다.
API 문서의 표에 따르면 `text`는 댓글, 스토리, 투표의 본문이고 HTML이다.
`title`은 스토리, 투표, 구인 글의 제목이다.
링크를 올린 스토리에는 보통 `title`과 `url`만 있고 `text`가 없다.
지워진 아이템은 `deleted`, 죽은 아이템은 `dead`가 `true`다.

원문이 링크한 마지막 “correct horse battery staple” 아이템의 id는 43838461이다.
아이템이 4천만 개를 넘는다는 뜻이고,
20 GiB를 이 수로 나누면 아이템 하나에 평균 약 490바이트다.
이 나눗셈은 원문에 없는 계산이다.

### `scan`은 이어받기와 덧붙이기로 최신 상태를 따라간다

unlurker 저장소의 README는 `hn` 도구의 `scan`으로
HN 데이터베이스 전체를 받을 수 있다고 설명한다.
오래 걸리므로 `--continue-at -`(원문의 `-c-`)와
`-o out.json`을 함께 쓰라고 권한다.
그러면 실패하거나 CTRL+C로 끊어도 같은 명령을 다시 실행했을 때
`out.json`의 내용을 보고 이어 받을 지점을 찾는다.
`--asc`로 받으면 같은 명령을 다시 실행할 때마다 새 아이템이 파일 끝에 붙는다.
저자가 “top it off”라고 부른 갱신이 이 동작이다.

README는 이 방식의 약점도 적어 두었다.
최근 아이템은 자주 바뀌므로 파일 끝의 몇 줄을 잘라 내고 다시 받으라고 하며,
마지막 1,000줄을 지운 뒤 `scan`을 다시 실행하는 bash 예시를 실었다.
덧붙이기만으로는 이미 받은 아이템의 점수, 댓글 수, 수정,
삭제가 반영되지 않는다는 뜻이다.

### 캐시는 아이템의 나이로 신선도를 판단한다

원문의 명령은 `--no-cache`를 썼지만 도구에는 공유 영구 캐시가 있다.
README는 아이템이 오래되지 않았으면 캐시에서 읽고,
만들어진 지 1분에서 시작해 몇 주가 지나면 바뀌지 않는 것으로 본다고 설명한다.
ashish01이 HN 토론에서 최근 아이템일수록 시간이 지나며 더 많이 바뀌니
받아 둔 최근 아이템이 더 빨리 낡는다고 지적하자,[^ashish01]
저자는 나이에 따른 함수로 이를 처리했다며 코드를 보였다.[^jasonthorsness-stale]

```go
const DefaultStaleIf = "(:now-refreshed)>" +
	"(60.0*(log2(max(0.0,((:now-Time)/60.0))+1.0)+pow(((:now-Time)/(24.0*60.0*60.0)),3)))"
```

마지막으로 받은 뒤 흐른 시간이 `60 × (log2(나이(분) + 1) + 나이(일)³)`초를
넘으면 다시 받는다.
로그 항은 초반에 짧은 간격을 만들고, 세제곱 항은 몇 주 뒤 간격을 급격히 늘린다.
아래 값은 이 식에 나이를 넣어 직접 계산한 것이다.

| 아이템 나이 | 다시 받기까지의 간격 |
| ----------- | -------------------- |
| 1분         | 60초                 |
| 1일         | 약 11.5분            |
| 7일         | 약 5.9시간           |
| 14일        | 약 1.9일             |
| 30일        | 약 18.8일            |
| 60일        | 약 150일             |

저자가 말한 “약 2주 뒤에는 불변”은 정확히는 간격이 나이보다 빨리 커져서
사실상 다시 받지 않게 되는 지점이다.

## 따라 하기

아래 과정 가운데 `hn scan`으로 전체를 받는 단계는
이 문서를 쓰며 실행하지 않았다.
DuckDB 쿼리는 HN API에서 직접 받은 아이템 4,499개로 만든 표본에서
DuckDB 1.5.6으로 실행해 확인했다.
표본은 id 1번부터 1,499번까지와,
원문이 언급한 id 43838461 직전의 3,000개다.

### 내려받기

README의 설치 명령과 원문의 명령을 이으면 다음과 같다.

```bash
# Linux 또는 macOS에서 /usr/local/bin에 설치한다 (curl, tar, sudo 필요)
curl -Ls "https://github.com/jasonthorsness/unlurker/releases/latest/download/hn_\
$(uname -s | tr '[:upper:]' '[:lower:]')_\
$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')\
.tar.gz" \
| sudo tar -xz -C /usr/local/bin

# 오름차순으로 전체를 받는다. -c- 덕분에 끊겨도 같은 명령으로 이어진다.
hn scan --no-cache --asc -c- -o full.json

# 나중에 갱신할 때: 자주 바뀌는 끝부분 1,000줄을 지우고 다시 이어 받는다.
input=full.json trim=1000 && \
truncate -s -$(tail -n "$trim" "$input" | wc -c) "$input" && \
hn scan --no-cache --asc -c- -o "$input"
```

### 집계하기

원문의 쿼리는 아래 함정 절에서 보듯 무엇을 세는지가 흐릿하다.
같은 질문을 덜 흐리게 묻도록 고친 쿼리는 다음과 같다.

```sql
-- 주 경계가 세션 시간대에 따라 바뀌지 않도록 고정한다.
SET TimeZone = 'UTC';

CREATE TABLE items AS
SELECT *
FROM read_json_auto('full.json', format = 'nd', sample_size = -1);

CREATE TABLE docs AS
SELECT
  id,
  type,
  DATE_TRUNC('week', TO_TIMESTAMP(time)) AS week_start,
  -- 스토리는 제목에, 댓글은 본문에 글이 있다. HTML 태그와 엔티티를 걷어 낸다.
  lower(regexp_replace(
    coalesce(title, '') || ' ' || coalesce(text, ''),
    '<.*?>|&#?[a-z0-9]+;', ' ', 'g')) AS body
FROM items
WHERE type IN ('story', 'comment')
  AND NOT coalesce(deleted, false)
  AND NOT coalesce(dead, false);

WITH weekly AS (
  SELECT
    week_start,
    -- \b 단어 경계로 javascript 안의 java, trust 안의 rust를 걸러 낸다.
    avg(regexp_matches(body, '\bpython\b')::int)     AS python_prop,
    avg(regexp_matches(body, '\bjavascript\b')::int) AS javascript_prop,
    avg(regexp_matches(body, '\bjava\b')::int)       AS java_prop,
    avg(regexp_matches(body, '\bruby\b')::int)       AS ruby_prop,
    avg(regexp_matches(body, '\brust\b')::int)       AS rust_prop,
    count(*)                                         AS n
  FROM docs
  GROUP BY week_start
)
SELECT
  week_start,
  n,
  avg(python_prop)     OVER w AS avg_python_12w,
  avg(javascript_prop) OVER w AS avg_javascript_12w,
  avg(java_prop)       OVER w AS avg_java_12w,
  avg(ruby_prop)       OVER w AS avg_ruby_12w,
  avg(rust_prop)       OVER w AS avg_rust_12w
FROM weekly
-- ROWS가 아니라 RANGE로 잡아야 빈 주가 있어도 정확히 12주를 본다.
WINDOW w AS (
  ORDER BY week_start
  RANGE BETWEEN INTERVAL 11 WEEKS PRECEDING AND CURRENT ROW
)
ORDER BY week_start;
```

`sample_size=-1`은 스키마를 추론할 때 일부 행이 아니라 전체를 훑게 한다.
20 GiB에서는 그만큼 느려지지만,
투표의 `parts`처럼 드물게 나오는 필드를 놓치거나
타입을 잘못 잡을 위험이 줄어든다.
표본에서 추론된 열은 `by`, `id`, `parent`, `text`, `time`, `type`,
`kids`, `deleted`, `descendants`, `score`, `title`, `url`, `dead`였다.

## 트레이드오프

### 직접 받을 것인가, 이미 있는 데이터셋을 쓸 것인가

토론에서 가장 많이 나온 반응은 굳이 받을 필요가 없다는 것이었다.
montebicyclelo는 갱신되는 HN 테이블을 가진 데이터베이스가 두 곳 있다며
BigQuery의 `bigquery-public-data.hacker_news.full`과,
가입 없이 브라우저에서 바로 쿼리할 수 있는
ClickHouse 플레이그라운드를 들었다.[^montebicyclelo]
flakiness는 BigQuery 데이터셋을 Parquet로 내보내 받은 뒤
DuckDB로 쿼리하는 “편법”을 썼다고 했고,[^flakiness]
minimaxir는 편법이 아니라 실용적인 것이라고 받았다.[^minimaxir]

직접 받는 쪽이 얻는 것은 원본 그대로의 JSON과 갱신 시점에 대한 통제다.
공개 데이터셋은 누가 언제 어떤 규칙으로 갱신하는지 사용자가 정하지 못한다.
hacker/hn-trends-18years.md 에 정리했듯 ClickHouse 쪽 테이블에도
범위의 한계가 있다는 지적이 있었다.
대신 직접 받으면 몇 시간의 다운로드와 20 GiB의 디스크,
그리고 아래에 적을 최신성 문제를 떠안는다.

받는 방법의 비용도 계산해 볼 만하다.
byearthithatius는 아이템을 하나씩 요청하면 응답 시간이 1초일 때 460일이 걸리고,
500개를 병렬로 돌려야 하루에 끝나지만
어느 쪽이든 4천만 번의 요청이라고 계산했다.[^byearthithatius]
저자의 도구는 기본으로 TCP 연결을 최대 100개까지 열기 때문에
몇 시간 안에 끝날 수 있었다고 보는 것이 자연스럽다.
이 연결 수는 README의 `--max-connections` 기본값에서 확인한 것이고,
다운로드 시간과의 관계는 해석이다.

### JSON 한 파일인가, 데이터베이스 파일인가

20 GiB라는 크기에 대한 반응은 엇갈렸다.
xnx는 HN 전체를 담은 자기 SQLite 파일이 20 GB인데
JSON이면 훨씬 클 것이라며 놀라워했다.[^xnx]
JSON은 행마다 키 이름을 되풀이하므로 같은 내용이라도 커진다.
g8oz는 어차피 JSON을 데이터베이스에 넣을 거라면
앞으로 많은 API가 DuckDB 파일을
바로 돌려주는 선택지를 줄 것이라고 내다봤고,[^g8oz]
vdm은 DuckDB 1.2 파일에서 내보낸 zstd Parquet가
2~3배 더 압축된다고 덧붙였다.[^vdm]

JSON 한 파일은 이어받기와 덧붙이기에 유리하다.
파일 끝만 보면 어디까지 받았는지 알 수 있고, `grep` 같은 도구가 그대로 통한다.
반대로 수정된 아이템을 제자리에서 고칠 수 없으므로
최신 상태를 유지하려면 다시 받거나 끝을 잘라 내는 수밖에 없다.
분석을 반복할 생각이라면 한 번 가져온 뒤 Parquet나 DuckDB 파일로 남기고,
JSON은 원본 보관용으로만 두는 편이 낫다.

### 덧붙이기 갱신은 과거를 고치지 못한다

`scan --asc`의 갱신은 새 id만 가져온다.
이미 받은 스토리의 점수와 댓글 수, 나중에 수정된 댓글,
뒤늦게 지워지거나 죽은 아이템은 받은 순간의 상태로 남는다.
README가 끝의 1,000줄을 다시 받으라고 권하는 것은
이 문제를 줄이는 방법이지 없애는 방법이 아니다.
HN API에는 바뀐 아이템과 프로필을 알려 주는 `/v0/updates` 엔드포인트가 있지만,
원문과 README 모두 이를 쓰는 갱신은 다루지 않는다.

언급 비율 같은 집계에는 이 차이가 거의 영향을 주지 않는다.
하지만 점수를 기준으로 무언가를 고르거나,
삭제된 글을 빼야 하는 분석에서는 받은 시점에 따라 결과가 달라진다.

## 함정

### 부분 문자열은 엉뚱한 단어를 센다

토론에서 가장 먼저 나온 지적이다.
jakegmaths는 `java` 쿼리가 JavaScript를 모두 포함하니
Java가 과대 계산된다고 했고,[^jakegmaths]
smarnach는 `rust`도 “trust”, “antitrust”, “frustration” 같은 단어를
잡는다고 덧붙였다.[^smarnach]
저자는 그렇다면 Java가 줄어드는 것이 더 뜻밖이라고 짧게 답했다.[^jasonthorsness]

표본에서 직접 세어 보면 차이가 크다.
아이템 4,499개 중 `text ILIKE '%rust%'`에 걸린 것은 81개였지만
단어 경계를 쓴 `\brust\b`에 걸린 것은 10개였다.
걸러진 것들은 “trust”, “rusty”, “crust”, “frustrating” 같은 단어였다.
`%java%`에 걸린 30개 중 14개는 `%javascript%`에도 걸렸다.
이 표본은 2006~2007년과 2025년 4월 말에 몰려 있으므로
비율을 전체 기간에 그대로 옮길 수는 없다.
다만 원문 그래프의 Rust 띠 가운데 상당 부분이
Rust 이야기가 아닐 수 있다는 점은 분명하다.

단어 경계로도 다 풀리지 않는다.
`text`가 HTML이라 링크 주소 안의 단어도 잡히므로 태그를 먼저 걷어 내야 한다.
“Go”나 “C” 같은 이름은 단어 경계로도 구분되지 않는다.
hacker/hn-trends-18years.md 에서 정리한 Atom, Grunt, Prometheus 사례처럼
이름이 같은 다른 대상은 문자열 일치만으로는 가려낼 수 없다.

### 분모와 분자가 다른 것을 센다

원문은 그래프를 전체 댓글과 스토리 중 해당 주제를 언급한 비율이라고 설명한다.
하지만 쿼리의 분자는 `text`만 보고 분모는 `COUNT(*)`로 모든 아이템을 센다.
스토리 제목은 어떤 경우에도 세지지 않고,
`text`가 없는 링크 스토리는 분모에만 들어간다.
지워진 아이템, 구인 글, 투표 선택지도 분모에 들어간다.

표본에서 스토리 870개 가운데 `text`가 있는 것은 24개였고,
`title`이 있는 것은 793개였다.
제목에만 Rust가 들어간 링크 스토리는
원문 방식으로는 Rust 언급으로 세지지 않는다.
이 계산은 원문에 없는 것으로, 원문의 쿼리를 HN API 필드 정의에 비춰 읽은 결과다.
위의 고친 쿼리가 `title`과 `text`를 합치고
종류와 삭제 여부로 거르는 이유가 이것이다.

### 누적 그래프는 계열의 높이를 숨긴다

stefs는 누적 그래프를 쓰지 말라고 했다.
잡음 속에서 특정 지점의 높이를 가늠하기 어렵고,
아마 없을 계열 간 의존을 암시한다는 이유였다.[^stefs]
저자는 맞는 말이지만 선 그래프로는 겹침이 너무 많아 아무것도 보이지 않았다며,
다음에는 계열 하나씩 그린 선 그래프를
정렬해 쌓아 보겠다고 답했다.[^jasonthorsness-chart]

혼란은 실제로 일어났다.
9rx는 “The Rise Of Rust”가 아니라 “The Fall Of Rust” 아니냐며,
그래프대로라면 Rust가 만들어지기 전에 가장 주목받았다고 꼬집었다.[^9rx]
emilbratt는 누적 그래프라서 각 계열이 도달한 높이가 아니라
차지하는 두께를 봐야 한다고 정정했다.[^emilbratt]
가장 위에 쌓인 Rust의 두께를 아래 네 계열의 요동 위에서 읽어야 하니,
제목이 주장하는 상승을 그래프로 확인하기 어렵다.
저자는 그래프를 Excel로 그려 SVG로 저장한 뒤 색을 고쳐
밝은 테마와 어두운 테마를 지원하게 했다고 밝혔다.[^jasonthorsness-excel]

### 시간대와 빈 주가 이동 평균을 흔든다

`TO_TIMESTAMP`는 시간대가 있는 타임스탬프를 돌려주고,
`DATE_TRUNC('week', ...)`는 세션 시간대 기준으로 주를 자른다.
표본에서 2007년 2월 19일로 시작하는 주에 들어간 행은
세션 시간대가 Asia/Seoul일 때 896개, UTC일 때 976개였다.
원문 쿼리는 시간대를 지정하지 않으므로 실행한 컴퓨터에 따라 주 경계가 바뀐다.

`ROWS BETWEEN 11 PRECEDING AND CURRENT ROW`는 12주가 아니라 12행을 본다.
아이템이 하나도 없는 주가 있으면 창이 12주보다 넓어진다.
원문 그래프가 2007년 5월부터 시작하므로 영향은 작겠지만,
날짜 기준의 `RANGE` 창을 쓰면 이 문제를 아예 피할 수 있다.

### 다운로드 크기에서 사람의 글을 바로 읽어 내면 안 된다

userbinator는 텍스트뿐인 사이트에
18년간 200억 바이트가 넘는 글이 올라왔다는 데 놀라며,
하루 2MB가 넘고 초당 약 7.5KB라고 계산했다.[^userbinator]
olalonde는 실제로는 초당 34바이트에 가깝고,
JSON의 메타데이터와 문법까지 생각하면 그보다 더 적다고 바로잡았다.[^olalonde]
20 GiB를 18년으로 나누면 초당 약 38바이트, 하루 약 3.3MB가 나온다.
아이템 하나에 평균 약 490바이트인데,
그중 상당 부분은 `kids` 배열, id, 키 이름이다.
파일 크기는 데이터 양의 상한일 뿐 사람이 쓴 글의 양이 아니다.

## 비평

### 그래프가 쿼리보다 먼저 결론을 말한다

원문은 TLDR 자리에 두 그래프를 놓고 “The Rise Of Rust”,
“The Progression of Postgres”라는 제목을 붙였다.
글의 실제 내용은 데이터를 받고 DuckDB로 쿼리하는 경험담이지만,
독자가 처음 보는 것은 기술 담론의 흐름에 대한 주장이다.
그리고 그 주장을 받치는 쿼리는 위의 함정 세 가지를 모두 안고 있다.

저자는 토론에서 그래프와 쿼리에 대한 비판이 대부분 타당하다며
후속 글을 쓰겠다고 했다.[^jasonthorsness-followup]
블로그 RSS에서 이 글 뒤에 올라온 글 제목들에서는
그런 후속편을 찾지 못했다.
결과적으로 원문의 그래프는 정정 없이 남아 있다.
문자열 몇 개를 세는 실험이 흥미롭다는 것과,
그 결과를 “상승”이라는 제목으로 내놓는 것은 다른 일이다.

LLM이 SQL을 짜는 데 꽤 도움이 됐다는 대목도 이와 겹친다.
원문의 쿼리는 문법적으로 깔끔하고 그럴듯한 결과를 내지만,
`text`만 보는 분자와 모든 아이템을 세는 분모의 불일치는
쿼리를 읽어서는 잘 드러나지 않는다.
API 필드 정의를 대조하고 결과 몇 줄을 직접 열어 봐야 보인다.
쿼리 작성을 도와준 도구가 무엇이든,
무엇을 세고 있는지 확인하는 일은 사람에게 남는다.

### “다 받았다”는 말은 받은 시점의 스냅숏을 뜻한다

원문은 같은 명령을 다시 실행하면 언제든 최신 상태로 채울 수 있다고 쓴다.
그러나 위에서 보았듯 그 명령은 새 아이템만 붙이고,
이미 받은 아이템의 변화는 반영하지 않는다.
README는 이 점을 알고 끝부분을 잘라 내는 방법까지 적었지만,
원문에는 그 맥락이 없다.
“everything that has ever happened on Hacker News”라는 표현은
실제로는 각 아이템을 받은 순간의 모습을 모은 것에 가깝다.

## 기억할 원칙

### 세기 전에 무엇이 걸리는지 몇 줄 열어 본다

이 글의 함정은 모두 결과 몇 줄을 열어 보면 바로 드러나는 것들이었다.
`%rust%`에 걸린 텍스트를 열 개만 봤어도 “trust”와 “frustrating”이 보였을 것이고,
스토리 몇 개를 열어 봤다면 `text`가 비어 있다는 것을 알았을 것이다.
비율 그래프를 그리기 전에 분자에 걸린 표본과 분모에 들어간 표본을
각각 몇 개씩 읽어 보는 것이 가장 싸고 효과적인 검증이다.

hacker/hn-trends-18years.md 의 도구가 같은 문제로 비판받은 것을 보면,
이것은 한 사람의 실수가 아니라 텍스트 빈도로 관심을 재는 방식 전체의 함정이다.
같은 저자는 claude/claude-for-financial-services.md 에 정리된 HN 토론에서
코드 생성은 린팅, 컴파일, 테스트가 AI의 오류를 잡아 주지만
금융에는 그런 자동 검증이 없다고 지적한 바 있다.
데이터 분석 쿼리도 컴파일은 되지만 틀린 것을 세는 쪽에 가깝다.

### 열린 데이터는 받기 전에 이미 있는 사본부터 찾는다

HN은 요청 수 제한 없는 API를 공개하고 있고,
저자도 다른 사이트처럼 막아 두지 않아서 기쁘다고 말했다.[^jasonthorsness-stale]
그 개방성 덕분에 이미 BigQuery와 ClickHouse에 갱신되는 사본이 있었다.
직접 받는 일은 재미있고 도구를 시험해 보기에도 좋지만,
분석이 목적이라면 먼저 있는 사본을 쓰고
원본 JSON이나 정확한 갱신 시점이 필요할 때만 직접 받는 순서가 낫다.
HN 자체가 어떻게 이런 부하를 견디는지는 hacker/hn-always-online.md 와
hacker/hn-on-common-lisp.md 에서 다룬 서버 한 대와 Arc, SBCL 이야기와 이어진다.

---

[^krapp]: <https://news.ycombinator.com/item?id=43843103>

[^ashish01]: <https://news.ycombinator.com/item?id=43841393>

[^jasonthorsness-stale]: <https://news.ycombinator.com/item?id=43841417>

[^montebicyclelo]: <https://news.ycombinator.com/item?id=43842557>

[^flakiness]: <https://news.ycombinator.com/item?id=43841672>

[^minimaxir]: <https://news.ycombinator.com/item?id=43841740>

[^byearthithatius]: <https://news.ycombinator.com/item?id=43851122>

[^xnx]: <https://news.ycombinator.com/item?id=43844980>

[^g8oz]: <https://news.ycombinator.com/item?id=43851496>

[^vdm]: <https://news.ycombinator.com/item?id=43855632>

[^jakegmaths]: <https://news.ycombinator.com/item?id=43841449>

[^smarnach]: <https://news.ycombinator.com/item?id=43841776>

[^jasonthorsness]: <https://news.ycombinator.com/item?id=43841454>

[^stefs]: <https://news.ycombinator.com/item?id=43842437>

[^jasonthorsness-chart]: <https://news.ycombinator.com/item?id=43845394>

[^9rx]: <https://news.ycombinator.com/item?id=43842119>

[^emilbratt]: <https://news.ycombinator.com/item?id=43842219>

[^jasonthorsness-excel]: <https://news.ycombinator.com/item?id=43849338>

[^userbinator]: <https://news.ycombinator.com/item?id=43842493>

[^olalonde]: <https://news.ycombinator.com/item?id=43847241>

[^jasonthorsness-followup]: <https://news.ycombinator.com/item?id=43845358>
