# 작은 요령들이 생산성의 상당 부분을 만든다

원문: [Small Programming Tricks](https://will-keleher.com/posts/small-programming-tricks-matter/)

HN 토론: <https://news.ycombinator.com/item?id=49729000> (556점, 249개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/f65fy3/small_programming_tricks> (59점, 28개 댓글)

GN 토론: <https://news.hada.io/topic?id=33778>

## 요약

Will Keleher가 쓴 글이다.
일상적으로 보면 엔지니어링 생산성의 놀랄 만큼 큰 몫이 작은 지식 덩어리에서 나온다는 것이 주장이다.
어떤 언어 기능이 존재한다는 것을 아는 것, 설명되지 않는 TCP 지연이 아마 `TCP_NO_DELAY` 설정과 네이글 알고리즘 때문이라는 것을 아는 것, 곤경에서 빠져나올 `git` 주문을 아는 것, 파일을 다시 쓰는 `sed` 요령을 아는 것 같은 것들이다.

저자는 이것이 어떤 의미에서는 자명하다고 인정한다. 우리가 아는 모든 것은 더 작은 지식 조각들로 이뤄지므로 그 조각들이 중요한 것은 당연하다는 것이다.
그러면서 자기가 말하려는 것을 좁힌다. 특별히 값어치가 크면서도 떠받치는 정신적 기반이 많이 필요하지 않은 지식 덩어리들이 있다는 것이다.
예로 든 것이 `python3 -m http.server`다. 어떤 디렉터리에서 간단한 서버를 띄우는 데 파이썬을 알 필요가 전혀 없지만 일이 조금은 쉬워진다는 것이다.

글의 본체는 그런 요령의 목록이고, 마지막에 조직 차원의 지식과 그것을 나누는 방법에 대한 제안이 붙는다.

## 요령 목록

### 셸과 히스토리

`ctrl + r`로 터미널 명령 히스토리를 검색할 수 있다는 것은 대개 알지만, fzf를 설치하면 그것을 퍼지 검색으로 바꿀 수 있다.
더 큰 힘을 원하면 atuin이 셸 히스토리를 검색 가능한 SQLite 데이터베이스로 대체한다.
per-directory-history는 특정 디렉터리에서 실행한 명령만 찾는 것과 전체를 찾는 것 사이를 오갈 수 있게 한다.
히스토리를 얼마나 저장할지도 설정할 수 있다.

zsh의 고급 자동완성은 기본으로 켜져 있지 않다.

```bash
if type brew &>/dev/null; then
    FPATH="$(brew --prefix)/share/zsh/site-functions:${FPATH}"
fi
autoload -Uz compinit
compinit
```

### 파일 찾기

`find`는 대체로 필요 없다는 것이 저자의 주장이다. 상당수의 `find` 명령이 `**/*.md` 같은 글로브로 대체된다.
대부분의 셸이 이것을 기본 지원하지만 bash에서는 `shopt -s globstar`로 켜야 한다.

같은 맥락에서 `grep`이나 `ack`나 `ag`보다 `rg`(ripgrep)를 쓰는 편이 대체로 낫다고 본다.

### Git

`git log -S pattern`은 git pickaxe라 불리며, 코드베이스에서 어떤 문자열을 추가하거나 제거한 모든 커밋을 보여 준다. 오래된 코드베이스에서 특히 놀랍도록 유용하다.
`git log -G pattern`은 비슷하되 그 줄이 이동한 경우까지 보여 준다.

`cd -`와 비슷하게 `git checkout -`으로 직전 HEAD로 돌아갈 수 있다.

### 데이터베이스

`FROM` 없이 `SELECT`할 수 있다. 데이터베이스의 어떤 함수가 실제로 어떻게 동작하는지 시험하거나 `SELECT TRUE <> NULL`이 어떻게 되는지 확인할 때 유용하다.
저자는 이 기법을 Julia Evans의 블로그에서 처음 봤다고 각주에 적으며, 그의 글이 이 글의 발상을 완벽하게 요약한다고 덧붙인다. 작은 지식 조각들은 강력하고 재미있고 다가가기 쉽다는 것이다.

PostgreSQL과 MySQL 모두 `explain analyze`를 지원하며, 최적화하려는 쿼리를 실제로 실행해 성능에 대한 훨씬 많은 정보를 준다.

### 정규식과 JavaScript

정규식의 `\b`, 즉 단어 경계 단언은 단어의 시작이나 끝을 찾기 쉽게 해 준다.

현대 JS는 `Array.flatMap`, `Object.entries`, `Promise.withResolvers`를 지원한다.

Node.js에서는 `https.Agent`를 만들어 HTTP 요청에 넘기면 외부 자원에 연결을 열어 둘 수 있고, 지연에 극적인 영향을 줄 수 있다는 것이 원문의 서술이다.

```javascript
// 원문에 실린 형태. 아래에 적은 이유로 Node의 내장 fetch에서는 동작하지 않는다.
fetch(url, { method, agent });
```

이 항목은 HN에서 사실 관계로 반박됐다.
forty가 Node.js 에이전트를 `fetch`에 넘길 수 있다는 것이 사실이냐고 물으며 아닐 것 같다고 적었고[^forty], nulltrace가 확정적으로 답했다.
Node의 내장 `fetch`는 Undici를 쓰므로 사용자 지정 훅은 `agent`가 아니라 `dispatcher`이며, Undici 호환 디스패처를 넘겨야 한다는 것이다.[^nulltrace]

```javascript
import { Agent } from "undici";

// keep-alive 연결 풀을 유지할 디스패처. 원문이 노린 지연 개선은 이쪽으로 해야 한다.
const dispatcher = new Agent({ keepAliveTimeout: 60_000 });

await fetch(url, { method, dispatcher });
```

즉 원문의 의도는 맞되 API가 틀렸다.
`http`나 `https` 모듈의 요청 함수에는 `agent`가 유효하지만, 전역 `fetch`는 다른 스택 위에 있어 같은 옵션을 받지 않는다.

### 지표에 로그 쓰기

관심 있는 필드의 값 분포를 감 잡는 데 로그를 쓸 수 있다.

```javascript
const bucket = Math.floor(Math.log10(userInGroupCount));
metrics.increment("my_metric", { bucket });
```

HN에서 butterNaN이 이 항목을 풀어 설명했다.
사용자가 그룹에 속하는 시스템에서 대부분의 그룹은 소수의 사용자만 갖고 몇몇 유명한 그룹은 50만 명처럼 불균형하게 많을 수 있다.
사용자 수로 고정 크기의 선형 버킷을 만들면 1~100, 101~200 식으로 가다가 버킷이 6만 개가 되어 버린다는 것이다.[^butterNaN]
LolPython도 로그 부분이 이해되지 않았다며 도움이 된 설명을 옮겼다. 로그 척도는 상대적 변화를, 선형 척도는 절대적 변화를 알려 주므로 상대적 변화에 관심이 있으면 로그를 쓰라는 것이다.[^LolPython]

## 조직 안의 요령

저자는 회사에서는 이런 종류의 작고 지렛대가 큰 지식이 더 많다고 본다.
어떤 문제를 디버깅하려면 어떤 데이터 소스를 보라는 것, 어떤 영역은 누가 잘 알고 기꺼이 도와준다는 것, 어려운 것에 대한 좋은 문서가 어디에 있다는 것, 무엇이 일어나면 수동으로 스케일아웃해야 한다는 것, 서비스를 롤링 재시작하려면 어떤 명령을 쓴다는 것, 어떤 유틸이 어떤 문제를 스크립트로 만들기 쉽게 해 준다는 것 같은 항목들이다.

그리고 실천 하나를 제안한다.
이전 회사에서 기술적인 것과 회사 특화된 것을 섞어 매일 하나씩 슬랙에 공유했고 사람들이 꽤 유용해했다는 것이다.
열 개 중 아홉 개를 이미 알더라도 그 열 번째 문서나 기법이 시간을 아껴 줄 수 있으며, 하루 하나가 사람들을 지식으로 압도하지 않으면서 이따금 유용한 논의를 촉발하기에 적당한 수였다고 밝힌다.
회사에서 시니어 엔지니어라면 비슷한 것을 해 볼 만하다는 권유로 마무리한다.

## 커뮤니티가 보탠 요령

두 스레드에서 나온 것들 중 원문의 목록을 실질적으로 확장하는 것들이다.

| 요령                       | 내용                                                                                 |
| -------------------------- | ------------------------------------------------------------------------------------ |
| `git jump`                 | 변경된 청크나 병합 충돌을 편집기 quickfix로 바로 여는 git 내장 기능                  |
| `grep -n` + `gF`           | 줄 번호를 붙여 저장한 뒤 vim에서 `gF`로 해당 파일의 해당 줄로 점프                   |
| `vim -q` / `:gr`           | errorfile을 quickfix 목록으로 열거나 vim 안에서 직접 grep해 `:copen`                 |
| `fd`, `bfs`, `fselect`     | `find` 대체. `bfs`는 너비 우선이라 얕은 위치의 파일을 빨리 찾음                      |
| `zoxide`                   | 방문한 디렉터리를 기억하는 `cd` 대체                                                 |
| `!!`, `!10`, `!$`          | 히스토리 확장. `shopt -s histverify`로 실행 전 확인, `!34:p`로 출력만                |
| `ESC+.` / `Alt+.`          | 직전 명령의 마지막 인자 삽입. 확장 결과가 눈에 보임                                  |
| `script`                   | 출력까지 포함해 터미널 세션 전체를 파일로 기록하는 오래된 GNU 도구                   |
| Emacs `F3`                 | 즉석에서 매크로를 기록해 반복 실행                                                   |
| `git ls-files`             | pathspec과 함께 쓰면 `find` 상당수를 대체하는 저장소 한정 파일 목록                  |
| `git log -p` + `/`         | pickaxe 대신 전체 diff를 훑으며 검색. 커밋이 잘게 쪼개진 저장소에서 맥락이 더 풍부함 |
| `rg --hidden -g '!*.lock'` | 숨김 파일까지 훑되 잠금 파일 소음은 제외                                             |
| `python3 -m json.tool`     | API 응답을 바로 보기 좋게 정렬                                                       |

lucasoshiro는 `find`를 대체하는 수단으로 `git ls-files`를 들었다. pathspec을 주면 대단히 강력해진다는 것이다.[^lucasoshiro]
글로브가 인자 길이 제한에 걸린다는 아래 함정을 생각하면, 저장소 안에서 찾는 경우에 한해서는 이쪽이 글로브보다 안전한 선택이기도 하다.
thih9는 pickaxe의 대안으로 `git log -p` 뒤에 `/`로 문자열을 찾는 방법을 제시했다. 맥락이 더 풍부하고 훑어보기 쉬우며, 특히 커밋이 잘게 쪼개진 프로젝트에서 유용하되 모든 프로젝트와 검색어에 통하지는 않는다는 단서를 붙였다.[^thih9]
ahmedhossamdev는 매일 쓰는 두 가지로 소음을 걷어 내는 `rg --hidden -g '!*.lock'`과 API 응답을 정렬하는 `python3 -m json.tool`을 꼽았다.[^ahmedhossamdev]

vimpostor가 짚은 `git jump`가 특히 원문의 빈자리를 채운다.
brad가 `rg pancakes | fpp`로 출력에서 파일 경로를 뽑아 편집기로 여는 방식을 공유하자[^brad], vimpostor는 그 별도 스크립트를 모르는 사람이 많은데 이미 git에 내장되어 있다고 답했다.
`git jump diff`는 작업 트리에서 바뀐 청크를, `git jump merge`는 모든 병합 충돌을 편집기로 연다는 것이다.[^vimpostor]

## 비평

### 목록의 대부분은 프로그래밍 요령이 아니다

제목은 작은 프로그래밍 요령이라고 하는데, 실제 목록의 압도적 다수는 셸과 CLI 도구 사용법이다.
실제로 프로그래밍에 해당하는 것은 `Array.flatMap` 같은 언어 기능 몇 개와 `https.Agent` 정도이며, 나머지는 환경 설정과 도구 선택이다.

HN에서 두 사람이 같은 지적을 했다.
ozim은 이것들이 프로그래밍 요령이 아니라 컴퓨팅 요령이거나 명령줄과 SQL 요령이라고 적었고, 그러면서 보통 사람들이 얼마나 많은 유용한 동작을 모르는지가 놀랍다고 덧붙였다.
그의 생각은 도발적이다. 사람들이 자기가 매일 쓰는 컴퓨터와 소프트웨어를 더 잘 다루도록 가르치는 데 시간을 쓴다면 AI 에이전트가 필요 없을 것이고 GDP가 세 배가 될 것이라는 주장이다.[^ozim]
winternewt도 이 중 실제 프로그래밍 요령은 몇 개뿐이라고 지적했다.[^winternewt]
VCFundedGenYer는 제목을 아예 bash/zsh CLI 요령으로 바꾸는 편이 낫겠다며, 이 글이 프로그래밍과는 곁가지로만 닿아 있다고 적었다.[^VCFundedGenYer]
1vuio0pswjnm7은 Node.js 항목을 빼면 프로그래밍 요령이 아니라 시스템 관리 요령으로 보인다고 하면서, 물론 어떤 HN 댓글자들에게는 셸 스크립팅도 프로그래밍이고 SQL을 프로그래밍 언어라 부르는 사람도 있을 것이라고 덧붙였다.[^1vuio0pswjnm7]
공교롭게도 그가 유일한 프로그래밍 요령으로 지목한 그 항목이 앞서 본 대로 사실이 틀린 항목이다.

이 구분이 사소하지 않은 이유는 전이 가능성이 다르기 때문이다.
셸 요령은 환경을 옮겨도 대체로 따라오고 한 번 익히면 20년을 간다. 언어 기능 지식은 그 언어를 떠나면 사라진다.
글이 말하는 특별히 값어치 크고 기반이 필요 없는 지식이라는 범주는 사실 앞쪽을 가리키며, 제목이 뒤쪽을 가리키고 있어 범주가 흐려진다.

Lobste.rs의 veqq가 더 근본적인 반론을 제시했다.
잘 설계된 원시 요소들이 서로 맞물리는 일관된 패러다임이라면 요령이 많이 나올 게 아니라 시너지 있고 예측 가능한 동작만 있어야 한다는 것이다.[^veqq]
요령의 존재 자체가 도구의 설계 결함을 가리킨다는 관점이며, trenchant의 반문과 정면으로 갈린다. 프로그래밍이 방대한 요령 모음 이상의 무엇이냐는 것이고 그것들은 재미있다는 것이다.[^trenchant]

### 아는 것과 쓰는 것 사이의 간격을 다루지 않는다

글은 요령을 아는 것이 생산성을 만든다고 전제하지만, 스레드에서 가장 많이 공감받은 반응은 그 전제를 흔든다.

phforms가 그 간격을 정확히 묘사했다.
`ctrl + r`을 명령줄을 배운 시점부터 알고 있었고 fzf 통합까지 잘 해 두었는데도, 몇 년 동안 위아래 화살표를 쓰거나 스크롤을 올려 이전 명령을 찾았다는 것이다.
단축키가 떠오르지 않아 가장 저항이 적은 길을 택했기 때문이며, 그래서 요령을 접근하기 쉬운 곳의 문서에 적어 두는 방식을 쓴다고 적는다.[^phforms]

이 문제는 글의 처방인 하루 하나 공유하기에 직접 영향을 준다.
공유는 인지를 만들지만 습관을 만들지는 못하고, 습관이 없으면 그 지식은 생산성으로 전환되지 않는다.
titzer의 방식이 그 간격을 메우는 한 형태다. `~/scratch.txt` 파일과 그것을 grep하는 `scratch` 별칭을 두고, 드물게 쓰지만 자주 잊는 명령 레시피를 넣어 둔다는 것이다. 셸 히스토리보다 오래간다는 이점도 있다.[^titzer]
AJRF도 비슷하게 자기 웹사이트에 기억할 만한 팁을 적기 시작했다며, 셸 히스토리보다 내구성이 있고 공유할 수도 있다고 적었다.[^AJRF]

alentred가 제안한 방향은 더 체계적이다.
JetBrains IDE에 모든 단축키와 기능을 나열하고 자기가 얼마나 자주 쓰는지 보여 주는 기능이 있었고, 기능 발견에 훌륭해서 정기적으로 확인하며 한 번도 안 쓴 것들을 시도해 봤다는 것이다. vim이나 zsh에도 같은 것을 늘 원했다고 덧붙인다.[^alentred]
요령을 전달하는 문제가 아니라 내가 안 쓰고 있는 것을 드러내는 문제로 재정의한 것이며, 그쪽이 phforms의 증상에 훨씬 직접적으로 대응한다.

### 하루 하나 공유하기가 받는 쪽에서 어떻게 읽히는지 빠져 있다

저자는 매일 하나씩 공유했고 사람들이 유용해했다고 적으며 시니어 엔지니어에게 권한다.
그런데 이 제안은 보내는 쪽의 경험만 근거로 하고 있다.

NegativeLatency가 받는 쪽의 반응을 솔직하게 적었다. 자기는 그것을 성가시게 여길 것 같지만, 못된 사람으로 보이지 않으려고 아무 말도 하지 않을 것이라는 것이다.[^NegativeLatency]
이 한 줄이 원문 근거의 약점을 드러낸다. 저자가 받은 피드백은 정확히 이런 이유로 긍정 편향되어 있었을 수 있다.

winternewt는 공유 자체의 난점도 짚었다.
요령을 나누는 것의 문제는 내가 알고 있으니 그것이 남에게도 뻔해 보인다는 점이며, 실제로 무엇이 남들에게 알려지지 않았는지 알기 어렵고, 다들 아는 것을 공유하면 잘난 척하는 것처럼 보일 위험이 있다는 것이다.[^winternewt]

lsofzz는 동기 쪽을 건드렸다. 사람들이 배울 만큼 충분히 동기가 있어야 하는데, 매뉴얼을 읽으라는 말이 모욕으로 받아들여지는 순간 모든 게 무너진다는 것이다.
그리고 이 요령들이 DNS 클러스터 장애를 새벽 3시 반까지 붙들거나 HSM이 새벽 5시에 갑자기 말썽을 부리는 이유를 쫓으며 힘겹게 얻은 것들인데, 요즘은 아무도 우리가 배운 것에 신경 쓰지 않는다고 적는다.[^lsofzz]
세 반응을 합치면 이 제안의 실제 난점이 보인다. 지식의 문제가 아니라 관계와 지위의 문제이며, 시니어가 매일 팁을 보내는 형식은 그 문제를 완화하지 않고 오히려 강화할 수 있다.

## 함정

글로브가 `find`를 대체한다는 조언에는 한계가 있다.
koala가 인자 길이 제한을 짚었다. bash에서 `getconf ARG_MAX`로 확인할 수 있으며 대개는 충분하지만 수백에서 수천 개 파일을 매칭하면 그 한계에 닿는다는 것이다.[^koala]
wiredfool도 같은 이유로 결국 `find`로 돌아가게 된다고 적었다.[^wiredfool]

`globstar`를 켜는 것 자체도 무료가 아니다.
wyclif는 큰 트리에서 이따금 느려지는 비용이 있으며, 일반적인 용도로는 켜도 되지만 스크립트에서는 이식성과 예상보다 넓게 확장될 가능성이 더 큰 걱정거리라고 지적했다.[^wyclif]

`FROM` 없는 `SELECT`는 표준이 아니다.
rf15이 그것은 쓰는 데이터베이스 소프트웨어에 전적으로 달렸다며, 어떤 IBM 제품은 분명히 다른 의견을 갖고 있다고 적었다.[^rf15]

히스토리 확장은 오작동하기 쉽다.
fanf는 오류가 나기 쉬워서 오래전에 꺼 버렸다고 밝혔다. 원래 명령이 히스토리에 기록되지 않아 검토하거나 고치기 어렵고, 자리를 세는 것이 마우스로 복사해 붙이는 것보다 사고를 더 방해하며 readline을 더 잘 쓰는 법을 익히는 것보다 느리다는 것이다.[^fanf]
tentacloids도 실행 전에 시각적으로 확인할 수 없다는 점이 위태롭게 느껴진다고 적었다.[^tentacloids]
대응책은 있다. fedemp가 `shopt -s histverify`로 `!!` 확장 시 확인을 요구할 수 있다고 알렸고[^fedemp], tmoertel은 `!34:p`처럼 `:p`를 붙이면 확장된 명령을 출력하고 히스토리 최신 항목으로 넣어 주므로 위 화살표로 꺼내 검토하고 편집할 수 있다고 덧붙였다.[^tmoertel]

## 기억할 원칙

### 요령의 가치는 내용이 아니라 촉발 조건에 있다

이 글과 두 스레드를 합치면 수십 개의 요령이 나오는데, 그중 실제로 내 것이 되는 것은 몇 개뿐이라는 점이 phforms의 증언이 말하는 바다.
차이를 만드는 것은 요령의 품질이 아니라 그것을 떠올리게 하는 상황과의 결합이다.

ryan-duve의 관찰이 그 조건을 정확히 설명한다.
그는 이런 팁으로 미니 워크숍을 하곤 했는데 가장 많이 채택되어 몇 년 뒤까지 이어진 것이 `ctrl-r`이었다고 적는다.
그것을 강력하게 만든 것은 bash와 zsh는 물론 IPython, erl/iex, Claude Code까지 프롬프트가 있는 곳이면 어디서나 작동한다는 점이었고, 동료들이 그것을 또 다른 사람에게 가르치는 것을 보는 일이 보람 있었다고 밝힌다.[^ryan-duve]

즉 오래 남는 요령의 조건은 두 가지다. 발동 상황이 자주 오고, 그 상황이 환경을 가리지 않는 것이다.
이 기준으로 보면 원문 목록의 항목들이 갈린다. `ctrl-r`과 `git log -S`는 조건을 만족하고, `zsh` 자동완성 설정처럼 한 번 하고 잊는 것은 요령이라기보다 설정이다.

그래서 요령을 수집할 때 물어야 할 질문은 이것이 멋진가가 아니라 이것을 떠올려야 할 상황이 다음 달에 몇 번 올 것인가다.
한 번 올 것 같으면 적어 두었다가 그때 찾는 편이 낫고, 매주 올 것 같으면 몸에 붙일 가치가 있다.
titzer의 `scratch` 파일과 AJRF의 공개 TIL이 전자를 위한 장치이고, 하루 하나 공유하기는 후자를 노리지만 앞서 본 대로 습관까지 만들지는 못한다.

### 에이전트의 작업 로그가 새로운 요령 출처가 되었다

이 글이 다루지 않은 축을 kccqzy가 열었다.
AI가 일하는 것을 그냥 지켜보는 것만으로 훨씬 많은 요령을 배울 수 있다는 것이며, 자율적으로 돌게 두지 말고 실행하는 모든 명령을 수동으로 승인하던 예전 방식으로 돌아가라는 제안이다.
최근 성능 최적화 작업을 하다가 Opus가 `perf` 명령을 자기가 가능한 줄 몰랐던 방식으로 쓰는 것을 발견했다고 밝히며, 실제 과제를 주고 그것이 문제를 푸는 데 쓰는 명령을 주의 깊게 읽으라고 권한다.[^kccqzy]

이 제안이 흥미로운 이유는 요령 전파의 오래된 병목을 우회하기 때문이다.
winternewt가 짚은 문제, 즉 내가 아는 것은 남에게도 뻔해 보여서 무엇을 공유해야 할지 모른다는 문제는 사람 사이에서만 발생한다.
에이전트는 자기가 쓰는 명령이 상대에게 새로운지 판단하지 않고 그냥 쓰며, 보는 쪽이 새로운 것만 골라 가면 된다.

그리고 이 방식은 앞 절의 기준과도 맞는다. 요령이 실제 문제 상황과 붙어서 나타나기 때문이다.
목록에서 읽은 요령은 발동 조건이 없는 채로 들어오지만, 에이전트가 내 문제를 풀면서 쓴 명령은 그 상황과 함께 들어온다.
phforms가 `ctrl + r`을 몇 년 동안 알고도 안 쓴 이유가 바로 조건의 부재였다는 것을 생각하면, 이 차이는 작지 않다.

다만 대가도 분명하다. 모든 명령을 수동으로 승인하는 것은 에이전트를 쓰는 속도상의 이유를 상당 부분 포기하는 것이다.
jawns가 바란 방향이 그 절충일 수 있다. 현재 터미널 설정을 평가해 이런 팁들을 적용해 주는 스크립트나 AI 스킬이 있으면 좋겠다는 것이고, `ag`를 쓰고 있으면 ripgrep을 설치하고 짧은 안내를 주거나, 실행한 git 명령 이력을 보고 효율 개선을 제안하는 식이다.[^jawns]
요령을 찾아 주는 일과 그것을 쓸 상황을 알려 주는 일이 분리될 수 있다는 발상이며, 지금은 어느 쪽도 제품으로 존재하지 않는다.

SebasDev도 같은 경험을 확인했다. AI 코딩 도구에서 실제 해법보다 그 과정에서 쓰는 명령에서 더 많이 배울 때가 있다는 것이다.[^SebasDev]

### 요령을 갈고닦을 이유가 사라지면 그 지식은 세대를 넘지 못한다

이 글이 상정하는 독자는 자기 도구를 날카롭게 벼리는 데 재미를 느끼는 사람이다.
그런데 스레드에는 그 동기 자체가 식었다는 증언이 나란히 놓여 있다.

computermadeofc가 가장 직접적으로 적었다. 예전에는 이런 작은 요령을 사랑했다는 것이다. 작업 흐름을 최적화하고 단축키를 익히고 매뉴얼을 읽는 일 말이다.
그런데 이제는 그냥 codex나 Claude Code에 프롬프트를 넣고, 도끼를 가는 일의 매력이 크게 줄었다고 한다.
그가 덧붙인 우려가 이 문서의 주제와 직결된다. 이런 종류의 지식 상당수가 곧 시간 속으로 사라질까 두렵다는 것이다.[^computermadeofc]

behnamoh는 그 변화를 자기 분야에서 관측했다. 학계에서는 말 그대로 아무도 더 이상 코드를 쓰지 않는다는 것이고, 프로그래밍의 기쁨과 재미가 끊임없는 에이전트 조율 작업으로 대체된 것은 아쉽지만 생산성 이득이 워낙 커서 예전으로 돌아가기 어렵다고 적는다.[^behnamoh]

다만 이 서사에 대한 반례도 같은 자리에 있다.
louthy는 41년을 코딩한 끝에 코드로 사고하게 됐고, 생각을 영어로 옮겨 LLM이 다시 코드로 옮기게 하는 것이 자기가 직접 쓰는 것보다 훨씬 느리다고 적었다. 몰입이 시작되면 프롬프트 루프에 끌려 나오는 것이 가장 원치 않는 일이라는 말도 덧붙인다.[^louthy]
catlifeonmars는 동료 대부분이 에이전트 코딩으로 옮겨 갔는데도 전부 손으로 코딩하며 속도를 따라가고 있다고 밝히며, 자랑이 아니라 자기 일에서는 코드를 쓰는 것이 가장 큰 병목이 아니라는 점을 말하려는 것이라고 적는다.[^catlifeonmars]
embedding-shape는 절충선을 제시했다. 프롬프트를 많이 쓰지만 여전히 명령을 직접 실행하고 vim으로 빠르게 고치며, 3초면 되는 일을 빠른 모델도 30초 걸리는 프롬프트로 시키지는 않는다는 것이다.[^embedding-shape]

이 대립이 원문의 처방에 조건을 붙인다.
하루 하나 공유하기가 작동하려면 받는 쪽이 그 요령을 쓸 상황에 계속 놓여 있어야 하는데, 명령을 에이전트가 대신 치는 환경에서는 그 상황 자체가 줄어든다.
그리고 앞 절에서 본 기준, 즉 발동 상황이 자주 오는 요령만 몸에 붙는다는 기준을 그대로 적용하면 결론이 나온다. 손으로 셸을 쓰는 빈도가 줄면 셸 요령의 반감기도 함께 줄어든다.
embedding-shape가 그은 3초 대 30초의 경계가 실질적인 방어선인 셈이며, 그 경계 안쪽에 남는 작업이 얼마나 되느냐가 이 지식의 수명을 정한다.

---

[^butterNaN]: <https://news.ycombinator.com/item?id=49738788>

[^LolPython]: <https://lobste.rs/s/f65fy3/small_programming_tricks#c_fqzw4m>

[^brad]: <https://lobste.rs/s/f65fy3/small_programming_tricks#c_tohn7s>

[^vimpostor]: <https://lobste.rs/s/f65fy3/small_programming_tricks#c_gu27dl>

[^ozim]: <https://news.ycombinator.com/item?id=49732872>

[^winternewt]: <https://news.ycombinator.com/item?id=49729425>

[^veqq]: <https://lobste.rs/s/f65fy3/small_programming_tricks#c_yezeaf>

[^trenchant]: <https://lobste.rs/s/f65fy3/small_programming_tricks#c_xvmhaz>

[^phforms]: <https://news.ycombinator.com/item?id=49730584>

[^titzer]: <https://news.ycombinator.com/item?id=49731240>

[^AJRF]: <https://news.ycombinator.com/item?id=49729604>

[^alentred]: <https://news.ycombinator.com/item?id=49737208>

[^NegativeLatency]: <https://news.ycombinator.com/item?id=49729495>

[^lsofzz]: <https://news.ycombinator.com/item?id=49733701>

[^koala]: <https://lobste.rs/s/f65fy3/small_programming_tricks#c_aarcvx>

[^wiredfool]: <https://news.ycombinator.com/item?id=49729766>

[^wyclif]: <https://news.ycombinator.com/item?id=49738676>

[^rf15]: <https://news.ycombinator.com/item?id=49730638>

[^fanf]: <https://lobste.rs/s/f65fy3/small_programming_tricks#c_jctck0>

[^tentacloids]: <https://lobste.rs/s/f65fy3/small_programming_tricks#c_zbcbfp>

[^fedemp]: <https://lobste.rs/s/f65fy3/small_programming_tricks#c_pbcgaf>

[^tmoertel]: <https://lobste.rs/s/f65fy3/small_programming_tricks#c_hr1kjb>

[^ryan-duve]: <https://lobste.rs/s/f65fy3/small_programming_tricks#c_ricdyl>

[^kccqzy]: <https://news.ycombinator.com/item?id=49729790>

[^jawns]: <https://news.ycombinator.com/item?id=49729480>

[^forty]: <https://news.ycombinator.com/item?id=49732391>

[^nulltrace]: <https://news.ycombinator.com/item?id=49734413>

[^lucasoshiro]: <https://news.ycombinator.com/item?id=49732548>

[^thih9]: <https://news.ycombinator.com/item?id=49730908>

[^ahmedhossamdev]: <https://news.ycombinator.com/item?id=49729678>

[^VCFundedGenYer]: <https://news.ycombinator.com/item?id=49729268>

[^1vuio0pswjnm7]: <https://news.ycombinator.com/item?id=49732131>

[^SebasDev]: <https://news.ycombinator.com/item?id=49731669>

[^computermadeofc]: <https://news.ycombinator.com/item?id=49734626>

[^behnamoh]: <https://news.ycombinator.com/item?id=49729206>

[^louthy]: <https://news.ycombinator.com/item?id=49730268>

[^catlifeonmars]: <https://news.ycombinator.com/item?id=49729542>

[^embedding-shape]: <https://news.ycombinator.com/item?id=49734648>
