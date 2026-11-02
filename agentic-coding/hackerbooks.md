# HackerBooks: HN 댓글에서 언급된 책 1만 5천 권을 모은 서가

<https://hackerbooks.org/>

Show HN: [HackerBooks – HackerTube, but for books mentioned on HN](https://news.ycombinator.com/item?id=50326821) (728점, 159개 댓글)

GN 토론: <https://news.hada.io/topic?id=36399>

## 소개

HackerBooks는 2007년부터 2026년까지 Hacker News 댓글에서 언급된 책을
모은 사이트다.
roansh가 Karpathy의 HackerTube를 보고 같은 것을 책으로 만들고 싶어서,
Claude(Opus 5.5)에게 맡겨 만들었다고 Show HN 글에 적었다.
그는 Claude가 데이터 파이프라인과 사이트를 거의 다 썼고,
자신은 방향을 잡고 판단하고 도메인을 산 정도라고 밝혔다.

사이트의 About 페이지에는 현재 책 15,362권, 언급 270,334건, 댓글 217,954개,
댓글 작성자 56,456명을 다룬다고 적혀 있다.
Show HN 글의 설명은 서로 다른 댓글 작성자 두 명 이상이 언급한 책 약 1만 6천 5백 권이었으므로, 사이트가 올라온 뒤 숫자가 바뀌었다.
데이터는 About 페이지에서 CSV(`data/hackerbooks.csv`)로 내려받을 수 있고,
데이터 생성일은 2026-11-02로 표시된다.

## 데이터가 만들어지는 과정

About 페이지는 다섯 단계를 설명한다.
출발점은 Hacker News의 모든 항목과 댓글이 담긴 공개 덤프다.
여기서 정규식과 간단한 자연어 처리로 책 언급처럼 보이는 구절(따옴표 속 제목,
“by 저자”, Amazon·Goodreads·Open Library 링크, ISBN)을 뽑는다.
후보를 Open Library의 work에 대응시켜 안정적인 ID, 저자, 초판 연도, 표지,
주제를 얻는다.

그다음 확인된 제목을 전체 코퍼스에서 다시 검색해,
아무도 링크하지 않은 언급까지 센다.
“Dune”, “Influence”, “Range”처럼 모호한 제목에만 작은 언어 모델을 써서 그 댓글이
정말 책 이야기인지 가른다.
점수는 언급 횟수보다 서로 다른 댓글 작성자 수에 더 큰 비중을 둔다. 한 사람이
열성적으로 반복해서 점수를 좌우하지 못하게 하려는 것이다.

추천과 언급은 따로 센다.
모든 언급에 Claude Sonnet 5.5가 recommend, neutral, critical,
not about the book 중 하나를 붙인다.
“Recommended by”는 그 책을 적어도 한 번 추천한 서로 다른 사람의 수이고,
“mentioned by”는 언급한 모든 사람의 수다.
이 라벨은 Claude Opus 5.5가 400개 언급을 따로 판정한 결과와 85% 일치했다고
사이트가 밝힌다.
키워드 규칙, 감성 점수, TF-IDF 분류기를 먼저 시도했지만 정확도가 더
낮았다고도 적혀 있다.

## 사용하기

사이트는 Top all-time, Most recommended, Rising, Trends, For You,
Topics 화면으로 나뉜다.
책을 열면 그 책을 언급한 댓글을 볼 수 있다.
“For You”는 사용자가 연 책을 바탕으로 브라우저 안에서만 계산하고 localStorage에
저장하며, 계정과 추적은 없다고 한다.
키보드 단축키(`/` 검색, `j`와 `k` 이동, `g h` 홈 등)도 지원한다.

기술 구성에 대해 roansh는 HN에서 이렇게 답했다.
프런트엔드는 순수 JS와 정적 JSON이고 Cloudflare에서 호스팅한다.
첫 로드에는 상위 도서 약 30kb 색인만 받고 전체 1만 6천 권 목록은 백그라운드에서
읽으며, 해시가 붙은 파일명 덕분에 영구 캐시된다.
표지는 R2에 있고, 데이터 파이프라인은 Python과 DuckDB로 HN 덤프를
처리한다.[^roansh-stack]

## 분석

### 추천과 언급을 나눈 것이 이 프로젝트의 핵심 설계다

HackerTube의 단위는 영상 한 편이 추천받았느냐였다.
책은 사정이 다르다. 사람들은 좋아서뿐 아니라 경고하거나 비판하려고도 책
이름을 꺼낸다.
그래서 같은 방식으로 세면 사람들이 가장 많이 거론한 책이 곧 가장 사랑받은
책처럼 보인다.

이 문제는 출시 직후 댓글에서 곧바로 드러났다.
drayfield는 어떤 책이 651명의 HN 사용자에게 “추천”받았다고 표시되는데,
그것이 Mein Kampf였다며 표현을 바꿔야 한다고 지적했다.[^drayfield]
roansh는 문구를 우선 “mentioned by”로 고쳤고 추천 판별을 개선하겠다고
답했다.[^roansh-wording]
지금의 About 페이지에는 추천과 언급을 따로 세는 구조가 들어 있다.

### 분류를 언어 모델에 맡기는 위치가 정해져 있다

파이프라인에서 모델이 쓰이는 곳은 두 군데로 한정된다.
모호한 제목을 가를 때는 작은 모델이고, 추천 여부를 가를 때는 Sonnet이다.
나머지 단계(정규식, Open Library 대응, 코퍼스 전체 검색)는 결정적인 규칙이다.

이 구분은 비용과 오류의 위치를 예측하게 해 준다.
모델이 틀리면 책이 잘못 분류되고, 규칙이 틀리면 책이 빠지거나 다른 책에 붙는다.
DuncanCoffee가 찾은 사례는 후자에 가깝다. 한 책의 저자 표시가 틀렸고,
링크된 첫 댓글을 읽으면 올바른 저자가 나온다는 것이었다.[^duncancoffee]
roansh는 바로 고치겠다고 하면서 수정 제안 버튼도 좋은 생각이라고
했다.[^roansh-correction]

## 비평

### 85% 일치는 정답이 아니라 두 모델의 합의다

사이트는 추천 라벨을 Opus 5.5의 판정과 비교해 85%가 맞았다고 말한다.
이 숫자는 한 모델이 다른 모델과 얼마나 같은 판단을 하느냐일 뿐이고,
사람이 매긴 정답과의 일치율이 아니다.
둘이 같은 방향으로 틀리면 일치율은 높아진다.

또 400개라는 표본이 어떻게 뽑혔는지는 About 페이지에 없다.
추천이 많은 책과 적은 책, 쉬운 문장과 모호한 문장이 같은 비율로
섞였는지 알 수 없다.
사이트가 스스로 노이즈를 예상하라고 적은 것은 정직하지만,
노이즈가 어느 책에 몰리는지는 말하지 않는다.

### 분류를 나눠도 해결되지 않는 영역이 있다

flexagoon은 어떤 책을 추천한다고 해서 지지한다는 뜻은 아니며,
싫어하는 사람의 자서전을 이해하려고 읽는 것과 같다고 짚었다.[^flexagoon]
이 지적은 recommend 라벨이 무엇을 재는지 묻게 한다.
읽어 보라는 권유와 내용에 동의한다는 뜻은 서로 다른 신호인데,
추천 하나로 합쳐진다.

danso는 Claude로 모든 것을 만들고 데이터를 모아 파싱했다면서 왜 노이즈를 걸러
추천만 보여 주게 하지 못했느냐고 물었다.[^danso]
사이트가 이후 추천과 언급을 나눈 것은 이 질문에 대한 답이지만,
나눈 뒤에도 recommend의 의미가 문제로 남는다.

### 같은 아이디어가 이미 있었다는 점을 글이 다루지 않는다

MYEUHD는 같은 시도가 2021년에 이미 있었다며 HN 링크를 달았다.[^myeuhd]
polishdude20은 hackernewsbooks 사이트가 몇 년 전에 있었던 것 같다고 했고,
cwnyth가 하나를 찾아 보여 주었다.[^polishdude20][^cwnyth]
HackerBooks가 앞선 것들과 무엇이 다른지는 Show HN 글에 나오지 않는다.
차이는 About 페이지의 방법론, 즉 추천과 언급의 구분과 규모에 있다고 읽을 수
있지만, 이것은 추정이다.

## 인사이트

### 코드가 아니라 아이디어의 복제가 하루 단위로 일어난다

이 프로젝트의 제목이 “HackerTube, but for books”다.
HackerTube 글이 나온 직후에 같은 구조를 책에 적용한 결과물이 올라왔고,
같은 스레드에는 영화, 팟캐스트, 도구 요청에 같은 방식을 적용하자는
댓글이 이어졌다.
bilater는 HN의 소프트웨어와 도구 요청 상위 100개를 비슷하게 순위화했다며 링크를
달았다.[^bilater]

아이디어의 가치는 구현이 어렵다는 데서 나오지 않게 되었다.
데이터가 열려 있고 구조가 같으면 구현은 에이전트에게 맡길 수 있기 때문이다.
이제 남는 차별점은 데이터를 어떻게 정제했느냐와,
그 결과를 어떻게 신뢰할 수 있게 표시했느냐다.
HackerBooks가 추천과 언급을 나눈 것이 바로 그 영역이다.

### 사용자의 지적이 데이터 모델을 바꾸는 속도가 빨라졌다

hyperman1은 책이 인기를 얻었다가 사라지는 흐름이 있는지,
그래프로 볼 수 있느냐고 물었다.
roansh는 좋은 생각이라며 트렌드 페이지를 만들고 있다고 답한 뒤 같은 스레드에서
완성했다고 알렸다.[^roansh-trends]
hyperman1은 자신이 글을 쓰는 것보다 빨랐다고 놀랐다.

vigilantpuma가 보고한 “mentions since” 필터 오류에서도 같은 일이 있었다.
roansh는 원인이 필터가 책의 가장 최근 언급을 기준으로 삼은 것이어서 인기 책은 늘
최근이라는 점이라고 설명하고, 처음 언급된 시점 기준으로 바꿨다.[^roansh-filter]
기능 요청이 데이터 모델의 변경으로 이어지고 곧바로 배포되는 일이 한
스레드에서 반복된다.
다만 이 속도가 유지보수 단계에서도 유지되는지는 이 스레드로는 알 수 없다.

### 생성한 글에 대한 거부감이 도구의 신뢰를 좌우한다

jchook은 사이트가 빠르다고 칭찬하면서도 기술 설명을 부탁했고,
동시에 HN 글에 생성된 텍스트를 넣지 말라고 요청했다. Claude가 쓴 문체를 보면
거부감이 든다는 이유였다.[^jchook]
roansh는 이를 공정한 지적이라고 받아들였다.

Starlevel004는 이 사이트의 화면이 Claude의 기본 UI라고 적었다.[^starlevel004]
roansh는 프런트엔드를 Claude가 만들었고 자신의 지시는 HackerTube처럼 느껴지게
하라는 것뿐이었으며 성능 쪽만 손을 댔다고 답했다.[^roansh-frontend]
사용자는 결과물이 생성되었다는 사실보다 그것을 어떻게 알렸느냐에 반응한다.
작성자가 Claude를 쓴 사실을 처음부터 밝힌 것이 이 스레드에서 비난보다 기술
질문을 끌어낸 요인으로 보이지만, 이것은 이 스레드 한 건에서 읽은 추정이다.

---

[^roansh-stack]: <https://news.ycombinator.com/item?id=50327179>

[^drayfield]: <https://news.ycombinator.com/item?id=50327129>

[^roansh-wording]: <https://news.ycombinator.com/item?id=50327270>

[^duncancoffee]: <https://news.ycombinator.com/item?id=50327451>

[^roansh-correction]: <https://news.ycombinator.com/item?id=50327531>

[^flexagoon]: <https://news.ycombinator.com/item?id=50330140>

[^danso]: <https://news.ycombinator.com/item?id=50327726>

[^myeuhd]: <https://news.ycombinator.com/item?id=50327283>

[^polishdude20]: <https://news.ycombinator.com/item?id=50327185>

[^cwnyth]: <https://news.ycombinator.com/item?id=50328060>

[^bilater]: <https://news.ycombinator.com/item?id=50327238>

[^roansh-trends]: <https://news.ycombinator.com/item?id=50327456>

[^roansh-filter]: <https://news.ycombinator.com/item?id=50327303>

[^jchook]: <https://news.ycombinator.com/item?id=50327092>

[^starlevel004]: <https://news.ycombinator.com/item?id=50327538>

[^roansh-frontend]: <https://news.ycombinator.com/item?id=50327550>
