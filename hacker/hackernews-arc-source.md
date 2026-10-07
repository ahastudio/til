# wting/hackernews: Arc로 쓴 초기 Hacker News 소스의 미러

<https://github.com/wting/hackernews>

HN 토론: <https://news.ycombinator.com/item?id=27452276> (119점, 34개 댓글)

## 소개

wting/hackernews는 Paul Graham과 Robert Morris가 공개한 Arc 배포판을
GitHub에 그대로 옮겨 둔 저장소다.
저장소 설명은 Hacker News web site source code mirror이고,
홈페이지 항목에는 news.ycombinator.com이 적혀 있다.
William Ting이 2012년 5월 12일에 만들었고,
첫 커밋 메시지는 arclanguage.org의 설치 페이지에서 처음 복사했다는 내용이다.
이 문서를 쓰는 2026년 10월 기준으로 별 656개, 포크 73개다.

README는 두 부분뿐이다.
설치 안내는 원래 배포 사이트에서 복사했고,
2단계의 tarball 파일을 이 저장소에 그대로 넣었다는 메모가 앞에 있다.
원래 안내는 MzScheme 372를 설치하고, `arc3.tar`를 받아 풀고,
`mzscheme -m -f as.scm`으로 Arc 프롬프트를 띄우라는 다섯 단계다.
372 이후 버전은 리스트를 변경할 수 없게 만들었으니
최신 버전을 쓰지 말라는 경고가 붙어 있다.

라이선스는 `copyright` 파일에 있다.
Paul Graham과 Robert Morris의 저작물이며
Perl Foundation의 Artistic License 2.0으로 사용을 허락한다는 두 줄이다.
GitHub은 이 라이선스를 자동으로 판별하지 못해 NOASSERTION으로 표시한다.

이 코드는 지금 news.ycombinator.com에서 도는 코드가 아니다.
HN 토론에서 dijit이 8년 동안 수정되지 않은 코드가 실제 코드일 리 없다고 하자,
dang은 실제로 수정되어 왔다고 짧게 답했다.[^dijit][^dang]
yellow_lead가 2015년 이후 갱신되지 않았으니 원래의 소스라고 제목을 바꾸자고 하자
dang은 제목에 Original과 2009년을 붙였다.[^dang-2]
dang은 2009년이 찾을 수 있는 마지막 공개 발표였기 때문이라고 설명했다.
그러나 `news.arc` 첫 줄의 주석은 `News.  2 Sep 06.`이라 앱의 시작은 2006년이다.

## 저장소 구성

저장소에는 디렉터리 하나와 파일 열여섯 개가 있다.
Arc 런타임, Arc 표준 라이브러리, 웹 서버, 그 위의 애플리케이션이
층을 이루어 한 저장소에 들어 있다.

| 파일              | 줄 수 | 역할                                                  |
| ----------------- | ----- | ----------------------------------------------------- |
| `ac.scm`          | 1436  | Arc 식을 MzScheme 식으로 바꾸는 컴파일러              |
| `brackets.scm`    | 48    | `[... _ ...]` 형태의 짧은 익명 함수 문법을 읽는 리더  |
| `as.scm`          | 16    | 진입점, `ac.scm`을 불러 `arc.arc`와 `libs.arc`를 적재 |
| `arc.arc`         | 1699  | Arc 표준 라이브러리                                   |
| `libs.arc`        | 7     | 문자열, HTML, 서버, 앱 라이브러리를 차례로 적재       |
| `srv.arc`         | 572   | HTTP 서버, 요청 스레드, IP 제한, 클로저 링크          |
| `app.arc`         | 657   | 로그인, 계정, 쿠키, 관리자, 입력 폼                   |
| `html.arc`        | 411   | HTML 생성 매크로                                      |
| `news.arc`        | 2610  | Hacker News 애플리케이션 전체                         |
| `blog.arc`        | 95    | 같은 기반으로 만든 작은 블로그 예제                   |
| `how-to-run-news` | 44    | 뉴스 앱 실행 안내와 성능 설정 세 줄                   |

이 표의 줄 수는 원본 파일을 받아 직접 센 값이다.
HN 하나가 `news.arc` 2610줄에 들어 있고,
그 아래의 웹 서버와 계정 관리까지 합쳐도 4000줄이 안 된다.

커밋은 다섯 개다.
2012년 5월 12일의 첫 복사와 README 추가,
2013년 5월 4일의 README 정리,
2015년 3월 3일에 병합된 Steven Luu의 `copyright` 오타 수정이 전부다.
오타 수정은 Perl Foundations's를 Perl Foundations'로 고친 한 글자 변경이다.
GeekNews의 lux1024는 README와 저작권 파일을 빼면
마지막 코드 수정이 10년 전이라는 데 놀랐다.[^gn-lux1024]

## 동작 방식

### 데이터는 디렉터리 속 파일이고 최근 것만 메모리에 둔다

`news.arc`는 저장 위치를 네 개의 디렉터리로 정한다.
`arc/news/` 아래에 `story/`, `profile/`, `vote/`가 있고,
글과 댓글은 항목 하나가 `story/` 아래 파일 하나다.
사용자 프로필과 투표 기록도 사용자마다 파일 하나씩이다.
`deftem`으로 정의한 `item`과 `profile` 구조체를
Arc 테이블 그대로 텍스트로 써 두고, 다시 읽어 들인다.

서버를 시작하면 `load-items`가 `story/` 디렉터리의 파일 id를 큰 순서로 정렬한 뒤
최근 15000개(`initload*`)만 메모리에 올린다.
첫 화면 순위는 `topstories` 파일에서 읽고, 없으면 새로 계산한다.
그 뒤의 읽기는 메모리 테이블에서 일어나고,
쓰기는 바뀐 항목의 파일을 다시 쓰는 식이다.
Ask HN 스레드에서 krapp이 데이터는 Arc 테이블을 담은 텍스트 파일이나 RAM에 있고
데이터베이스는 없다고 설명한 것이 이 구조다.
그 스레드는 `hacker/hn-always-online.md`가 다룬다.

코드 주석에는 이 방식의 약점도 그대로 남아 있다.
투표 파일이 가끔 무작위로 글자가 빠지거나 더해진 채 깨져 기록되며,
원인이 Arc보다 아래에 있는 것 같으니
디스크에 쓰는 모든 리스트가 같은 위험을 안고 있을 것이라는 내용이다.
다른 주석은 한 사용자가 글을 수정하는 동안 다른 사용자의 투표가 점수를 바꾸면
저장할 때 그 변경이 덮어써지지만,
잠금을 들일 만큼 큰 문제는 아니라고 적는다.

### 링크가 서버 메모리 속 클로저를 가리킨다

`srv.arc`의 가장 독특한 부분은 `fnid`다.
폼 제출이나 다음 페이지 같은 링크를 만들 때
처리할 함수 자체를 `fns*` 테이블에 넣고,
무작위 10글자 id를 붙여 URL로 내보낸다.
사용자가 그 링크를 누르면 서버는 id로 클로저를 찾아 그대로 호출한다.
페이지 사이의 상태는 세션 저장소가 아니라 클로저가 붙잡은 변수에 있다.

이 방식은 메모리를 계속 먹는다.
`harvest-fnids`는 클로저가 50000개를 넘으면
시간 제한이 지난 것과 가장 오래된 10%를 지운다.
지워진 id로 요청이 오면 서버는 `Unknown or expired link.`를 돌려준다.
주석은 더 정교하게 하려면 최대 개수를 추정해 한계를 정해야 하고,
그 너머의 유일한 해법은 메모리를 더 사는 것이라고 적는다.
Lobste.rs의 kornel이 HN이 클로저로 상태를 관리하던 탓에
이 오류가 나고 2페이지를 안정적으로 보여 주지 못했다고 한 것이
이 코드에서 비롯된 현상이다.
그 논의는 `hacker/hn-on-common-lisp.md`에 있다.

### 요청마다 스레드를 띄우고 IP별로 제한한다

서버는 연결마다 스레드를 하나 띄우고,
30초(`threadlife*`) 안에 끝나지 않으면 그 스레드를 끊는다.
같은 IP의 요청이 250개를 넘은 뒤부터는 IP 제한을 적용한다.
10초 창(`req-window*`) 안에 30개(`req-limit*`)를 넘기면 요청을 거절하고,
2초(`dos-window*`) 안에 30개를 보내면 DoS로 보고
그 서버 프로세스가 살아 있는 동안 해당 IP를 무시한다.
`throttle-ips*`에 오른 IP는 창마다 한 요청만 받는다.

로그인하지 않은 사용자의 페이지는 따로 캐시한다.
`newscache` 매크로는 사용자가 `nil`이면 미리 만든 문자열을 내보내고,
로그인한 사용자에게는 매번 새로 그린다.
페이지당 30개 글(`perpage*`)을 보여 주며,
주석은 테스트할 때는 `caching*`을 0으로 두라고 당부한다.
부하가 몰릴 때 dang이 로그아웃을 부탁하는 이유가 이 분기에서 보인다.

### 첫 화면 순위는 점수를 나이의 거듭제곱으로 나눈다

`frontpage-rank`는 다음 식을 계산한다.
나이는 분 단위이고, 기준 시간 120분을 더해 시간 단위로 바꾼다.

```text
base  = realscore - 1
num   = base^0.8            (base > 0 일 때)
rank  = num / ((age_min + 120) / 60)^1.8 × 벌점 계수

realscore = score - sockvotes
```

벌점 계수는 세 가지다.
URL이 없는 글(Ask 같은 텍스트 글)은 0.4를 곱한다.
가벼운 글은 0.3과 논쟁 계수 중 작은 값을 곱한다.
가벼운 글은 제목이 구호이거나(`rally`), 이미지 위주이거나,
관리자가 등록한 사이트이거나, URL이 png나 jpg로 끝나는 글이다.
논쟁 계수는 보이는 댓글이 20개를 넘으면 `(점수 / 댓글 수)^2`와 1 중 작은 값이다.
점수보다 댓글이 훨씬 많은 글은 이 계수 때문에 빠르게 내려간다.
`realscore`는 원래 점수에서 중복 계정 의심 투표(`sockvotes`)를 뺀 값이다.

### 권한은 카르마 문턱으로 나뉜다

댓글 비추천은 카르마가 100을 넘어야 하고(`downvote-threshold*`),
작성 후 1440분 안의 댓글에만 할 수 있다.
글에는 비추천이 없고, 자기 댓글에 달린 답글도 비추천할 수 없다.
신고(flag)는 카르마가 30을 넘어야 할 수 있다(`flag-threshold*`).
신고가 7개를 넘으면(`flag-kill-threshold*`) 항목이 죽는데,
관리자가 `nokill`을 붙였거나 관리자의 표가 있는 항목은 예외다.
같은 IP에서 이미 투표가 있으면
카르마가 `legit-threshold*`를 넘어야 표가 인정된다.
프로필에는 `noprocrast` 설정도 있어서,
켜면 `maxvisit` 분 동안만 머물고 `minaway` 분을 쉬어야 다시 볼 수 있다.

## 실행하기

이 문서를 쓰며 코드를 직접 실행하지는 않았다.
아래는 저장소의 `how-to-run-news` 내용을 정리한 것이다.

```bash
# MzScheme 372가 설치되어 있어야 한다 (이후 버전은 리스트가 불변이라 동작하지 않는다)
git clone https://github.com/wting/hackernews.git
cd hackernews
mkdir arc
echo "myname" > arc/admins   # 관리자 계정 이름
mzscheme -f as.scm           # Arc 프롬프트가 뜬다
```

Arc 프롬프트에서 다음을 입력한다.

```lisp
(load "news.arc")
(nsv)            ; 기본 8080 포트로 서버를 띄운다
```

`http://localhost:8080`에서 `myname`으로 계정을 만들면 관리자로 로그인된다.
안내는 처음 사용자들에게 카르마를 최소 10씩 직접 주라고 하고,
재시작할 때 나오는 user break 메시지는 무시하라고 한다.
사이트 이름, 주소, 색상은 `news.arc` 맨 위의 변수에서 바꾼다.
기본값은 `My Forum`과 `news.yourdomain.com`이다.

안내 끝에는 성능 설정 세 줄이 있다.

```lisp
(= static-max-age* 7200)    ; 정적 파일을 브라우저가 7200초 캐시
(declare 'direct-calls t)   ; 함수를 테이블로 재정의하지 않겠다는 약속
(declare 'explicit-flush t) ; 출력 플러시를 직접 책임진다
```

## 함정

### MzScheme 372를 구하는 것부터 일이다

README가 요구하는 MzScheme 372는 지금은 쉽게 구할 수 없는 오래된 버전이다.
`ac.scm`도 mzscheme 4.x에서는 변경 가능한 쌍(mutable pairs)이 빠져
Arc의 대부분은 돌지만 전부는 아니라고 주석으로 경고한다.
지금 운영체제에서 이 버전을 빌드하는 것은 이 코드를 읽는 것보다 어렵다.
돌려 보려면 arclanguage.org의 이후 Arc 배포판이나
커뮤니티 포크인 Anarki를 쓰는 편이 현실적이다.
HN 토론에서 caslon은 이것이 아주 오래된 배포판이고
Arc는 이제 Racket 위에서 돈다고 짚었다.[^caslon]

### 이 코드로 HN의 현재 동작을 단정하면 틀린다

순위 공식과 카르마 문턱은 이 배포판 시점의 값이다.
dang은 HN 코드가 수정되어 왔다고 했고,
현재 HN의 순위에는 공개되지 않은 벌점과 모더레이션이 더해진다.
현재 소스를 공개하지 않는 이유를 sneak이 묻자 dang은
보안보다는 비공개가 필요해서라고 답했다.[^dang-3]
비밀로 해야 하는 어뷰징 방지 기능이 많고,
그것을 코드 뼈대에서 떼어 내는 일이 큰 작업이라는 것이다.
pg가 예전에 영리한 훅(hook) 설계로 그런 부분을 분리했지만
결국 서로 스며들었다고 덧붙였다.
`news.arc`에는 `(hook 'initload items)`, `(hook 'admin-bar user whence)` 같은
훅 호출이 곳곳에 있고 `arc.arc`가 `hook`과 `defhook`을 정의한다.
이것이 dang이 말한 설계의 흔적이라는 것은 이 문서의 해석이다.

### 파일 저장은 단일 프로세스를 전제한다

모든 상태가 한 프로세스의 메모리 테이블에 있고 디스크 파일은 그 사본이다.
프로세스를 둘 띄우면 서로의 변경을 모른다.
클로저 링크도 프로세스 메모리에 있으므로
재시작하면 열려 있던 모든 폼과 다음 페이지 링크가 만료된다.
로드밸런서 뒤에 여러 인스턴스를 두는 방식은 이 구조와 맞지 않는다.
Ask HN 스레드에서 HN이 마스터 한 대와 스탠바이 한 대로 운영된다는 설명은
이 제약과 들어맞는다.

## 기억할 원칙

### 작은 언어 위의 작은 앱은 통째로 읽을 수 있다

HN 토론에서 dvfjsdhgfv는 나중에 커진 인기 프로젝트의 초기 버전에는
모든 것이 어떻게 맞물리는지와 기본 생각을 한눈에 볼 수 있는
아름다움이 있다고 적었다.[^dvfjsdhgfv]
이 저장소가 바로 그런 경우다.
컴파일러, 표준 라이브러리, 웹 서버, 계정, 순위, 모더레이션까지
`.arc`와 `.scm` 파일을 모두 합쳐 8028줄 안에 있다.
마음먹으면 끝까지 읽을 수 있는 분량이다.

이 읽기 가능성은 설계 선택의 결과다.
데이터베이스 대신 파일, 세션 저장소 대신 클로저,
템플릿 엔진 대신 HTML 매크로를 썼기 때문에
외부 의존성이 MzScheme 하나로 줄었다.
대가는 앞의 함정에 적은 대로 확장과 이식이 어렵다는 점이다.
같은 코드가 나중에 SBCL 위로 옮겨질 때도
애플리케이션이 아니라 그 아래의 Arc 구현을 바꾸는 길을 택했다.

---

[^dijit]: <https://news.ycombinator.com/item?id=27452548>

[^dang]: <https://news.ycombinator.com/item?id=27457376>

[^dang-2]: <https://news.ycombinator.com/item?id=27452670>

[^gn-lux1024]: <https://news.hada.io/topic?id=6877#cid10984>

[^caslon]: <https://news.ycombinator.com/item?id=27452668>

[^dang-3]: <https://news.ycombinator.com/item?id=27457350>

[^dvfjsdhgfv]: <https://news.ycombinator.com/item?id=27457359>
