# 20,000 Startup Ideas: 직업 과업 목록을 창업 아이디어로 읽는 페이지

<https://unawaz.github.io/stochastic-hill-climbing/tasks/>

HN 토론: <https://news.ycombinator.com/item?id=21112345> (461점, 178개 댓글)

GN 토론: <https://news.hada.io/topic?id=683>

## 소개

페이지 제목은 “20,000 Startup Ideas”이고, 내용은 영어 문장이 한 줄에 하나씩 이어지는 목록이다.
페이지 맨 위의 설명은 짧다.
이 데이터가 미국 직업 정보 사이트 O*NET에서 온 것이며, 이것이 현재 경제적으로 중요한 인간 활동의 지도를 준다는 것이다.
그래서 창업 아이디어의 좋은 출처이고, 어쩌면 거의 모든 창업 아이디어의 목록일 수도 있다고 한다.

목록의 항목은 직업이 하는 일의 서술문이다.
예를 들면 “Check books in and out of the library.”(도서관에서 책을 대출·반납 처리한다), “Maintain ship logs.”(선박 항해 일지를 쓴다), “Debug robotics programs.”(로봇 프로그램을 디버깅한다) 같은 것들이다.
이 문서를 쓰는 시점에 페이지는 18,500여 줄이다.
HN에서 bengarvey가 세어 보니 18,514개였고,[^bengarvey] 제목의 20,000은 대략의 숫자라는 뜻이다.
항목은 번호가 붙은 순서로 나오지만 분류나 정렬 기준은 페이지에 없다.
페이지는 이 데이터를 어떻게 가공했는지, 중복을 어떻게 처리했는지도 밝히지 않는다.
GitHub Pages 주소의 최상위(`/stochastic-hill-climbing/`)는 없는 페이지(404)여서, 이 목록이 어떤 프로젝트의 일부인지는 알 수 없다.

## 읽는 법

### 아이디어가 아니라 활동의 목록이다

HN에서 가장 먼저 나온 지적은 이 항목들이 아이디어가 아니라는 것이다.
Geee는 이것이 사람이 하는 활동이고, 창업 아이디어는 그 활동을 더 쉽게 만드는 방법을 찾는 것일 수 있다고 했다.
목록을 쓸모 있게 하려면 활동이 영향을 미치는 사람의 수와 사람당 영향의 크기라는 두 값이 더 필요하고, 그 곱으로 정렬하면 혁신의 가치가 큰 영역이 나온다는 제안이다.[^Geee]
davidivadavid는 아이디어 대부분이 그 활동을 아예 없애는 방법일 수 있다고 덧붙였다.[^davidivadavid]
petra는 각 활동의 도구, 과정, 문제를 이해하게 해 주는 자료가 빠져 있다고 했다.[^petra]
이 지적들은 같은 결론으로 모인다.
이 목록은 시장의 크기를 보여 주지 않고, 시장이 있는지도 보여 주지 않는다.

### 항목의 구체성은 고르지 않다

orangepanda는 “손님의 손톱을 비누 물에 담그는 데 면봉, 줄, 오렌지 스틱을 쓴다” 같은 항목이 이상할 만큼 구체적이라고 했다.[^orangepanda]
chrismorgan은 가장 짧은 항목 다섯 개가 11~13글자(Carve meat, Dig trenches, Graft plants, Align wheels, Shampoo hair)이고 가장 긴 항목은 291~332글자라고 계산해 보였다.[^chrismorgan]
두 극단이 한 목록에 있다는 것은 항목의 추상도가 일정하지 않다는 뜻이다.
colinwilyb는 10933번과 10934번이 손톱 다듬기와 고기 손질로 서로 무관한 두 활동이 붙어 있는 예라고 짚었다.[^colinwilyb]
이 목록을 아이디어의 후보로 쓰려면, 한 줄이 한 활동을 가리키는지부터 사람이 확인해야 한다.

### 아이디어의 값에 대한 오래된 논쟁이 되풀이된다

스레드의 많은 부분이 아이디어가 얼마나 가치가 있느냐는 논쟁이다.
fencepost는 아이디어는 쉽고 걸러 내는 일과 회사를 키우는 일이 어렵다고 했고,[^fencepost]
wayoutthere는 이 목록의 요점이 출발점은 많으니 하나를 골라 가치가 생길 때까지 다듬으라는 것이라고 풀었다.[^wayoutthere]
mythz는 실행도 중요하지만 옳은 아이디어를 고르는 일도 중요하다고, Dropbox와 Airbnb의 단순한 핵심 아이디어가 처음에는 무시당했다는 점을 들었다.[^mythz]
GeekNews에서 xguru는 2019년 10월에 스타트업은 아이디어보다 실행이 중요하다고들 하지만 아이디어가 전혀 없이는 뭔가를 하기도 어렵고, 아주 다양한 분야를 망라해서 재미로 읽기에 좋다고 적었다.[^xguru]
이 논쟁에서 이 페이지가 하는 일은 한쪽의 증거가 되는 것이 아니라, 아이디어의 출처가 얼마든지 만들어질 수 있다는 점을 보여 주는 것이다.

### 기계가 비슷한 문장을 만들 수 있다는 지적

hermes0는 목록의 앞부분을 문장 생성 모델에 넣어도 비슷하게 그럴듯한 항목이 나온다고 했다.[^hermes0]
이는 목록의 항목이 형식이 같은 서술문이라 모방하기 쉽다는 뜻이다.
이 문서는 그 모델의 결과를 확인하지 못했다.
하지만 이 지적은 2026년에 같은 종류의 목록(AI가 만든 120만 개의 창업 아이디어)이 나온 것과 맞닿아 있고, 이 저장소의 `startup/idealab-ai.md`가 그 서비스를 다룬다.
이 목록은 사람이 직접 하는 활동의 서술을 그대로 모은 것이고, 그 서비스는 출처에서 신호를 뽑아 아이디어를 조합한 것이라는 점이 다르다.

## 쓸 만한 용도

이 목록의 쓸모는 아이디어를 받는 데 있지 않고, 자신이 아는 영역의 활동이 세부 단위로 어떻게 서술되는지를 확인하는 데 있다.
자신의 직업이나 업계의 항목을 골라 읽으면, 하는 일이 어떤 동사와 도구로 쪼개지는지가 보인다.
그중 시간이 많이 들거나 오류가 잦은 항목을 찾는 것이 아이디어의 출발점이 될 수 있다.
다만 그 항목이 얼마나 많은 사람에게 얼마나 큰 문제인지는 이 목록 밖에서 확인해야 한다.
이 목록을 쓸 때 가를 관찰은 하나다.
고른 항목의 활동을 실제로 하는 사람 다섯 명에게 그 일이 얼마나 불편한지를 직접 물어 보는 것이다.

---

[^bengarvey]: <https://news.ycombinator.com/item?id=21125410>

[^Geee]: <https://news.ycombinator.com/item?id=21125782>

[^davidivadavid]: <https://news.ycombinator.com/item?id=21127927>

[^petra]: <https://news.ycombinator.com/item?id=21125924>

[^orangepanda]: <https://news.ycombinator.com/item?id=21124861>

[^chrismorgan]: <https://news.ycombinator.com/item?id=21125404>

[^colinwilyb]: <https://news.ycombinator.com/item?id=21125072>

[^fencepost]: <https://news.ycombinator.com/item?id=21125885>

[^wayoutthere]: <https://news.ycombinator.com/item?id=21126628>

[^mythz]: <https://news.ycombinator.com/item?id=21131318>

[^xguru]: <https://news.hada.io/topic?id=683#cid506>

[^hermes0]: <https://news.ycombinator.com/item?id=21125592>
