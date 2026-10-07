# Hacker News는 이제 Common Lisp 위에서 돈다: Arc 런타임을 SBCL로 옮긴 Clarc

원문: [Hacker News now runs on top of Common Lisp - Lisp journey](https://lisp-journey.gitlab.io/blog/hacker-news-now-runs-on-top-of-common-lisp/)

HN 토론: <https://news.ycombinator.com/item?id=44099006> (663점, 435개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/vypfzm/hacker_news_now_runs_on_top_common_lisp> (38점, 33개 댓글)

GN 토론: <https://news.hada.io/topic?id=21129>

## 요약

Common Lisp 블로그 Lisp journey가 2025년 5월 26일에 올린 짧은 글이다.
Hacker News는 Paul Graham이 만든 Lisp 방언 Arc로 작성되었고,
Arc는 Racket 위에서 구현되어 있었다.
글은 그것이 바뀌어 HN이 적어도 2024년 9월부터 SBCL 위에서 돈다고 전한다.
이유는 성능이라고 한 문장으로 답한다.

글의 본문은 대부분 HN 운영자 dang의 댓글을 시기순으로 엮은 것이다.
출발점은 2024년 9월 한 사용자의 질문이다.
긴 스레드에서 예전처럼 More를 눌러 다음 페이지를 불러올 필요가 없어졌는데,
공지가 있었는지 묻는 글이었다.
dang은 Clarc가 마침내 나왔기 때문이라고 답했다.
2022년 댓글에서는 Clarc가 훨씬 빠르고 HN을 여러 코어에서 쉽게 돌릴 수 있게
해 준다고, 몇 년째 작업 중이지만 시간이 잘 나지 않는다고 적었다.

구현 방식은 2019년 댓글로 설명한다.
Arc를 JavaScript로 옮긴 Lilt와 Common Lisp로 옮긴 Clarc가 있고,
이 둘을 쉽게 만들려고 기존 Arc 구현의 바닥을 단계별로 다시 짰다.
가장 아래가 arc0이고, arc1은 arc0으로, 그 위 단계는 arc1으로 작성한다.
가능한 많은 것을 위쪽 단계에 넣으면 밑바탕 시스템(Racket, JS, CL)으로
새로 써야 하는 것은 arc0뿐이라 재구현이 쉬워진다는 설명이다.

마지막으로 공개 여부를 다룬다.
Clarc 자체는 공개되지 않았지만 공개하기는 비교적 쉽다는 dang의 말을 인용한다.
원래 공개된 Arc 배포판(arclanguage.org)을 Clarc로 옮기면 되고,
그 배포판에는 HN·YC 고유의 부분을 걷어 낸 초기 HN이 예제로 들어 있다.
반면 HN 코드베이스 전체는 공개가 어렵다.
코드의 상당 부분이 알려지면 쓸모없어지는 어뷰징 방지 장치이고,
비밀 부분을 떼어 내는 일이 이제는 큰 작업이라는 2019년 dang의 말이 근거다.
글은 티 나지 않게 끝난 전환을 축하하며 끝난다.
글 끝의 수정 기록에 따르면 공개 범위에 관한 인용은 게시 당일 밤에 보충되었고,
첫 문단의 시점 표현은 다음 날 날짜로 바뀌었다.

## 분석

### 제목이 말하는 것과 실제로 바뀐 것은 층위가 다르다

제목만 보면 HN을 Common Lisp로 다시 쓴 것처럼 읽힌다.
본문이 실제로 전하는 사실은 HN 애플리케이션은 여전히 Arc이고,
Arc 언어를 실행하는 바닥만 Racket에서 SBCL로 바뀌었다는 것이다.
HN의 varbhat은 HN을 Common Lisp로 다시 쓴 것이 아니라 Arc 런타임을
Common Lisp로 재구현한 것이라고 정리했다.[^varbhat]
Lobste.rs의 miloignis도 HN은 여전히 Arc로 돌고 Arc 백엔드만
Racket에서 Common Lisp로 옮겼다고 짚었다.[^miloignis]

이 구분이 중요한 이유는 전환의 위험이 어디에 있었는지를 바꾸기 때문이다.
애플리케이션을 새로 쓰면 기능 하나하나의 동작을 다시 맞춰야 한다.
런타임을 바꾸면 애플리케이션 코드는 그대로 두고,
언어의 의미를 새 기반에서 똑같이 재현하는 데 위험이 모인다.
HN의 cadamsdotcom이 재작성이 늘 나쁜 생각은 아니라며 이 사례를 들자,
eurleif가 그들은 HN을 다시 쓴 것이 아니라 HN이 쓰인 언어의 다른 구현을
만든 것이라고 바로잡은 대화가 이 차이를 보여 준다.[^cadamsdotcom][^eurleif]

### 단계적 부트스트랩이 런타임 교체를 가능하게 했다

arc0, arc1, 그 위 단계로 언어를 쌓는 구조는 새로운 기법이 아니다.
작은 핵을 밑바탕 언어로 쓰고 나머지를 그 핵으로 쓰는 방식은
Lisp 계열 구현에서 오래된 전통이다.
이 글이 보여 주는 것은 그 구조가 실제 운영 서비스에서
기반을 바꾸는 비용을 얼마나 줄이는지다.

글이 링크한 2019년 dang 댓글을 직접 읽으면,
이 재작업으로 전체 Arc 구현이 500줄쯤 줄었다는 언급도 있다.
같은 구조 덕분에 Lilt(JS)와 Clarc(CL)가 함께 진행될 수 있었다.
기반 언어마다 arc0만 새로 쓰면 되므로 실험의 단가가 낮아진다.
Lobste.rs의 dlisboa가 지적했듯 HN 애플리케이션보다 그것을 떠받치는 언어 쪽이
더 자주 구현을 바꿔 왔다.[^dlisboa]
dang도 HN 토론에서 Arc가 원래 MzScheme 위에서, 이후 PLT Scheme 위에서 돌았고
Racket으로는 kogir가 옮겼다고 기억을 덧붙였다.[^dang]

### 성능 개선은 기능의 변화로 드러났다

이 전환을 사용자가 알아챈 경로가 흥미롭다.
발표가 아니라 긴 스레드의 페이지 나누기가 사라진 것으로 알려졌다.
글에 인용된 2024년 9월 질문에 dang이 단 답을 원 스레드에서 읽으면,
이미 3주도 더 전에 배포했고 HN에서 묻는 사람은 처음이라고 적혀 있다.
그 전에 이메일로 한 번 질문이 왔을 뿐이라 물보라 없는 다이빙이었다는 표현이다.

페이지 나누기는 기능이 아니라 성능 한계를 숨기는 장치였던 셈이다.
Lobste.rs의 kornel은 Arc의 성능이 너무 나빠서 이 전환 전까지 HN이 한 번에
몇백 개 이상의 댓글을 보여 주지 못했다고 적었다.
같은 댓글은 클로저로 상태를 관리하던 방식 때문에
unknown or expired link 오류가 나고
2페이지를 안정적으로 보여 주지 못했다고도 지적한다.[^kornel]
여기에 2022년 dang이 말한 여러 코어 활용이 겹친다.
HN의 brundolf는 그러면 지금까지 단일 코어에서 돌았느냐고 놀랐고,
JW_00000은 HN이 한 머신, 한 코어, 한 프로세스에서 돌았다는 예전 링크를
찾아 붙였다.[^brundolf][^JW_00000]
그 단일 프로세스 구조가 어떻게 상시 가동을 유지했는지는
이 저장소의 `hacker/hn-always-online.md`가 다룬다.

## 비평

### 인용 모음은 1차 출처의 문구를 다시 확인하지 않았다

이 글의 거의 모든 사실은 dang의 댓글에서 온다.
그런데 2019년 인용문은 글이 링크한 댓글의 실제 문구와 다르다.
링크된 댓글은 진짜 Arc가 arc1으로 작성된다고 말하는데,
글의 인용은 맨 위 단계가 아마 arc2일 것이라는 표현과
이것이 새롭지 않다는 문장을 담고 있다.
같은 취지의 다른 댓글에서 가져왔을 가능성도 있지만,
글은 그 출처를 밝히지 않는다.

더 큰 문제는 공개 범위에 관한 인용이었다.
dang 본인이 HN 토론에서 글이 다 맞았지만 그 부분만 틀렸다고 지적했다.[^dang-2]
어뷰징 방지 장치 때문에 공개할 수 없다는 말은 HN 애플리케이션에 대한 것이고,
언어 구현인 Clarc와는 상관이 없다는 것이다.
글은 같은 날 밤 이를 반영해 인용을 보충했다.
수정 자체는 빨랐지만, 여러 해에 걸친 댓글을 이어 붙여 하나의 이야기로 만드는
형식이 맥락을 놓치기 쉽다는 점을 보여 준다.
각 댓글은 서로 다른 질문에 대한 답이었다.

### 성능이라는 한 단어로 원인을 닫는다

글은 왜냐는 질문에 성능 때문이라고만 답한다.
무엇이 느렸는지, 얼마나 빨라졌는지, 어떤 지표가 바뀌었는지는 없다.
페이지 나누기가 사라졌다는 관찰이 유일한 증거다.
dang의 2022년 댓글도 훨씬 빠르다는 말뿐 수치를 주지 않았다.

수치가 없으니 독자는 이 사례에서 무엇을 일반화할 수 있는지 판단하기 어렵다.
Racket이 느렸던 것인지, Arc가 Racket 위에서 구현된 방식이 느렸던 것인지,
단일 코어 제약이 병목이었던 것인지에 따라 교훈이 완전히 달라진다.
HN의 mdaniel이 Racket 쪽이 Arc를 고칠 만큼 일반적인 문제로 보지 않았던 게
아니냐고 묻자, dang은 Racket 사람들은 늘 도왔고 수정 요청을 거절한 적이
없다고 답했다.[^dang-3]
그렇다면 문제는 Racket의 결함이 아니라 Arc를 그 위에 얹은 방식이나
SBCL의 네이티브 컴파일 같은 차이였을 가능성이 크지만,
이것은 원문이 아니라 이 문서의 해석이다.

### 축하가 전환 과정의 어려움을 지운다

글은 티 나지 않게 끝난 전환을 축하하며 끝나지만,
어떻게 그것이 가능했는지는 묻지 않는다.
HN의 hyperman1은 운영 중인 사이트의 엔진을 갈면서
오래 잊힌 부분이 하나도 깨지지 않게 하기는 어렵다며
dang에게 방법을 물었다.[^hyperman1]
이 질문에는 dang의 답이 달리지 않았다.

런타임 교체에서 가장 어려운 부분은 의미의 미세한 차이다.
문자열 처리, 해시 테이블 순회 순서, 숫자 표현, 예외 처리 같은 것들이
Racket과 SBCL에서 똑같이 동작해야 HN 코드가 그대로 돈다.
몇 년이 걸린 이유가 dang의 시간 부족만이었는지,
이런 호환성 작업의 양 때문이었는지는 글에서 알 수 없다.
글이 기술 블로그라면 이 부분이 가장 읽고 싶은 대목이었을 것이다.

## 인사이트

### 자기 언어를 가진 서비스는 런타임을 갈아 끼울 수 있다

Lobste.rs의 antifuchs는 이 여정에서 배울 것이 있겠지만
아무도 배우지 않을 것이라고 냉소했다.[^antifuchs]
miloignis는 오히려 교훈은 자기 Lisp 방언을 만들면 새 언어 백엔드를
시도할 유연성이 생긴다는 것이라고 받았다.[^miloignis]
이 둘의 대화는 같은 사실에서 정반대 결론을 끌어낸다.

이 문서의 관점은 둘 다 맞다는 것이다.
애플리케이션이 작은 언어 위에 서 있으면 그 언어의 구현을 바꾸는 것으로
기반 전체를 옮길 수 있다.
이것은 JVM 위의 언어들이 바이트코드라는 경계 덕분에 JVM 구현을 바꿔도
살아남는 것과 같은 구조다.
대가는 그 언어를 유지할 사람이 사실상 한두 명이라는 점이다.
dang이 Clarc를 몇 년간 혼자 진행했다는 사실이 그 대가를 보여 준다.

### 성능 여유는 제품의 형태를 바꾼다

페이지 나누기의 소멸은 성능 개선이 사용자 경험으로 번역된 사례다.
더 빠른 서버가 같은 페이지를 더 빨리 보여 준 것이 아니라,
보여 줄 수 있는 페이지의 크기 자체가 바뀌었다.
HN의 kevincox는 GitHub은 한 페이지에 댓글 열몇 개도 다 보여 주지 못한다며
HN을 제정신의 섬이라고 불렀다.[^kevincox]

일반화하면, 많은 제품의 기능 제약은 설계 결정처럼 보이지만
실제로는 성능 한계를 감추는 장치다.
페이지 나누기, 지연 로딩, 더 보기 버튼이 그렇다.
성능이 충분해지면 그 장치는 근거를 잃는다.
이 관점에서 보면 성능 작업의 가치는 응답 시간 그래프가 아니라
어떤 제약을 걷어 낼 수 있게 되는지로 재야 한다.

### 비밀에 기대는 방어는 코드 공개를 막고 기술 부채가 된다

HN 코드베이스를 공개할 수 없는 이유는 어뷰징 방지 장치가 비밀이어야 하기
때문이다.
HN의 Aurornis는 보안이 모호함에 기대면 진짜 보안이 아니라는 말이 있지만
단순한 어뷰징 방지책은 정확한 방식이 드러나지 않는 한 매우 효과적이라고
적었다.[^Aurornis]
quotemstr는 Kerckhoffs의 원칙을 따르지 않는 것은 보안이 아니며,
스팸 방지는 보안과 인접하지만 같은 것이 아니라고 구분했다.[^quotemstr]

이 구분은 옳지만, 코드 관리의 관점에서는 다른 문제가 남는다.
비밀 장치가 애플리케이션 전체에 흩어져 있으면 공개만 막히는 것이 아니라
분리 자체가 해마다 비싸진다.
dang이 2019년에 이미 지금은 떼어 내는 일이 큰 작업이라고 말한 것이 그 증거다.
HN의 AndrewKemendo는 비즈니스 로직이 원래 구조에 녹아 있어서
다른 것으로 옮기기가 사실상 불가능하다고 보았다.[^AndrewKemendo]
런타임 교체가 애플리케이션 재작성보다 쉬웠던 이유의 일부가 여기에 있다.
공개된 초기 버전은 `hacker/hackernews-arc-source.md`가 다룬다.

### 극단적으로 작은 스택은 사람 한 명에게 의존한다

HN의 Tistel이 여전히 Paul Graham과 Robert Morris가 작업하느냐고 묻자
dang은 그들은 오래전에 떠났다고 답했다.[^dang-4]
언어를 만든 사람들은 떠났고, 그 언어의 새 구현은 운영자가 틈틈이 썼다.
공개된 Arc 코드로 웹사이트를 운영하는 jgrahamc는
Clarc를 쓸 수 있으면 좋겠다고 적었다.[^jgrahamc]

여기서 드러나는 긴장은 규모가 아니라 시간이다.
HN은 트래픽 면에서는 작은 스택으로 충분하지만,
그 스택을 이해하는 사람의 수는 시간이 갈수록 줄어든다.
Clarc 공개가 의미 있는 이유는 성능이 아니라 이 의존도를 낮출 수 있다는 데 있다.
dang이 Clarc 공개는 훨씬 쉽다고 말한 이후 실제로 공개되었는지는
이 원문에서는 확인할 수 없다.

---

[^varbhat]: <https://news.ycombinator.com/item?id=44099167>

[^miloignis]: <https://lobste.rs/s/vypfzm/hacker_news_now_runs_on_top_common_lisp#c_uhbf0g>

[^cadamsdotcom]: <https://news.ycombinator.com/item?id=44103046>

[^eurleif]: <https://news.ycombinator.com/item?id=44103072>

[^dlisboa]: <https://lobste.rs/s/vypfzm/hacker_news_now_runs_on_top_common_lisp#c_6kunj1>

[^dang]: <https://news.ycombinator.com/item?id=44099405>

[^kornel]: <https://lobste.rs/s/vypfzm/hacker_news_now_runs_on_top_common_lisp#c_tyeqif>

[^brundolf]: <https://news.ycombinator.com/item?id=44099359>

[^JW_00000]: <https://news.ycombinator.com/item?id=44099977>

[^dang-2]: <https://news.ycombinator.com/item?id=44099693>

[^dang-3]: <https://news.ycombinator.com/item?id=44099215>

[^hyperman1]: <https://news.ycombinator.com/item?id=44104551>

[^antifuchs]: <https://lobste.rs/s/vypfzm/hacker_news_now_runs_on_top_common_lisp#c_o1fkzd>

[^kevincox]: <https://news.ycombinator.com/item?id=44103078>

[^Aurornis]: <https://news.ycombinator.com/item?id=44099200>

[^quotemstr]: <https://news.ycombinator.com/item?id=44099310>

[^AndrewKemendo]: <https://news.ycombinator.com/item?id=44099250>

[^dang-4]: <https://news.ycombinator.com/item?id=44101963>

[^jgrahamc]: <https://news.ycombinator.com/item?id=44099315>
