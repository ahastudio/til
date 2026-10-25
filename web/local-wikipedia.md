# Local Wikipedia: 걸어서 반 시간 안의 항목만 보여 주는 위키백과

<https://edjefferson.com/localwiki/>

HN 토론: <https://news.ycombinator.com/item?id=50202285> (1561점, 245개 댓글)

GN 토론: <https://news.hada.io/topic?id=35859>

## 소개

Local Wikipedia는 위키백과에서 좌표가 붙은 항목 가운데 지정한 장소에서 걸어서 반
시간쯤 되는 거리 안에 있는 것만 모아 보여 주는 웹사이트다.
페이지는 스스로를 한 줄로 설명한다.
Wikipedia이되 내 주변 반 시간 거리에 있는 것들만 담았다는 뜻이다.
내용은 위키백과에서 그대로 가져오며, 위키백과와는 아무 관계가 없다고 밝힌다.
거리 안에 항목이 25개보다 적으면 가장 가까운 25개를 가져오는데 반경은 6마일
안쪽으로 제한된다.
항목이 500개를 넘으면 가장 가까운 500개만 쓴다.
위치는 브라우저에 저장되고 공유 링크에는 들어가지 않는다고 한다.

시작 화면에서는 동네, 지역, 랜드마크, 우편번호를 입력하거나 현재 위치를 쓸 수
있다.
누군가 공유한 링크로 들어오면 그 사람의 동네 기준 항목이 열리고, 자기 동네로
바꾸는 입구도 같이 나온다.
페이지에는 Nearby, Main page, Random article 같은 메뉴가 있다.
이 문서는 위치 입력 후의 화면을 직접 열어 보지 않았고, 아래 동작은 사이트의
스크립트(`script.js`)와 안내 문구에서 읽은 것이다.

## 동작 방식

### 거리 계산은 위키백과 geosearch 한 번이다

스크립트 주석에 따르면 장소는 postcodes.io에서 찾고, 주변 항목은 위키백과의
geosearch에서 가져온다.
요청은 장소 좌표에서 최대 반경 10,000미터, 최대 500개로 한 번 보내고, 같은
검색을 generator로 돌려 각 항목의 글 길이도 함께 받는다.
기본 반경은 2,414미터(1.5마일, 걸어서 반 시간쯤)이고, 그 안에 항목이 25개
미만이면 가장 가까운 25개를 쓴다.
따라서 시골에서는 반경이 반 시간 거리를 넘어 최대 10킬로미터까지 늘어난다.
거리는 도로를 따른 보행 거리가 아니라 직선거리다.

### 항목 안에서는 주변 항목으로만 링크가 이어진다

항목을 열면 해당 글을 보여 주되, 링크는 근처에 있는 항목으로 가는 것만 남긴다는
것이 스크립트의 설명이다.
장소의 첫 화면은 위키백과 메인 페이지처럼 추천 글과 Did you know를 보여 주고,
전체 목록은 가나다순이나 가까운 순으로 볼 수 있다.
이렇게 하면 위키백과를 따라가다 멀리 가는 대신 동네 안에서 읽기가 이어진다.

## 한계

### 반경과 언어와 단위는 사용자가 고르지 못하는 값이 많다

HN 댓글에서 가장 많이 나온 요청은 반경 설정이었다.
esperent는 사는 곳에서 위키백과에 오를 만한 곳에 가려면 몇 시간을 걸어야 해서
15킬로미터쯤으로 넓히고 싶다고 했다.[^esperent]
다른 한쪽에서는 도시 중심부에서 결과가 너무 많거나 학교뿐이라는 불만이 나왔다.
throwaway173738은 결과가 학교 두 곳을 빼면 모두 학교라서 키워드 필터가 있었으면
한다고 했고,[^throwaway173738] Trigodil도 교회나 다리, 박물관 같은 종류별 필터를
원했다.[^Trigodil]
언어도 반복된 요청이다.
kubb는 지역 언어판 위키백과에 항목이 더 많은 곳이 많다고 짚었고,[^kubb]
flohofwoe는 독일에서 접속했는데 영어판만 쓰여 25개뿐이었다고
했다.[^flohofwoe-lang]
이 문서가 읽은 스크립트에는 언어를 고르는 변수(`lang`)가 있지만, 화면에서 바꾸는
방법은 확인하지 못했다.
거리 단위는 야드와 마일이 먼저 보인다는 불만이 있었다.
pezezin은 일본에서도 야드와 마일이 섞여 나온다고 했다.[^pezezin]
이에 flohofwoe는 사이드바에 마일과 킬로미터를 바꾸는 링크가 있다고
알렸다.[^flohofwoe-units]
`metric` 분기가 스크립트에 있는 것과 맞는 설명이다.

### 걸어서 반 시간이라는 말은 직선거리 근사다

collabs는 가장 가까운 곳이 0.8마일이라 걸을 만하다고 생각했는데, Google 지도로는
실제로 1.9마일이고 길에 보도도 없었다고 했다.[^collabs]
이 사이트가 거리를 직선으로 재는 이상 이런 차이는 구조적으로 생긴다.
강이나 철도, 고속도로가 끼면 반 시간 거리라는 이름과 실제 걸음이 크게 어긋난다.

### 지오태그가 없으면 근처여도 나오지 않는다

dllu는 근처에 있어도 지오태그가 없는 글은 빠지고, 조금 더 넓은 지역에 걸친 글도
빠진다고 지적했다.[^dllu]
이 사이트의 항목 범위는 위키백과에서 좌표가 붙은 글로 한정되므로 이는 위키백과
쪽의 데이터 사정이다.
koito17은 거리 이름을 넣으면 기차역만 나오고, 도시 이름으로 바꾸면 이번에는 반
시간 거리가 되지 못한다고 했다.[^koito17]
altilunium은 동네의 많은 것이 notability 기준 때문에 위키백과에 오르지 못한다며,
이 사이트가 그런 것을 직접 적게 해 주는 줄 알았는데 존재하는 글을 거리로 거를
뿐이었다고 했다.[^altilunium]

## 비평

### 새로움은 모으는 방식에 있고 데이터에는 없다

esperent는 처음에 이 사이트가 위키백과 Special:Nearby의 포장이라고 판단했고, 몇
곳에서 결과가 같았다고 적었다.[^esperent]
tannertech도 위키백과 모바일 앱에 같은 기능이 있다고 확인했다.[^tannertech]
이에 dspillett은 장소를 직접 입력해 볼 수 있다는 점이 더해진 것이라고
반박했다.[^dspillett]
SCdF는 위키백과가 이미 하지만 나만의 작은 위키백과로 꾸며 주는 점이 좋다고
했다.[^SCdF]
이 논쟁은 같은 데이터에 어떤 제약을 두느냐가 제품이 될 수 있는지를 묻는다.
이 사이트의 제약은 링크를 근처로만 이어서 읽기 경험을 닫는 것이다.
위키백과 앱의 Nearby는 항목을 찾는 목록이지만, 이 사이트는 읽기 전체를 동네 안에
가둔다.
다만 그 차이가 실제로 더 많이 읽게 하는지는 HN 댓글의 체험담 말고는 근거가 없다.

### 가까운 항목이 흥미로운 항목은 아니다

INTPenis는 말뫼를 입력했더니 처음 뜬 글이 2022년의 학교 칼부림 사건이어서 흥분이
불쾌함으로 바뀌었다고 했다.[^INTPenis]
xnickb도 베를린에서 Nazi Germany 항목을 마주했다고 적었다.[^xnickb]
paxy는 건물 목록만으로는 흥미가 크지 않으며, 밀집한 뉴욕 우편번호에서도 300개
남짓이라는 점이 의아하다고 했다.[^paxy]
거리를 기준으로 거르면 중요도나 취향과 무관한 항목이 앞에 서는 것이 구조적
결과다.
zulko는 위키백과 항목을 지도에 올리는 자기 프로젝트에서 글자 수가 많은 항목을
먼저 보여 줬다고 했다.[^zulko]
이 사이트는 25개 미만이면 가까운 순이고 반경 안에서는 목록이 가나다순이나 가까운
순이어서, 이런 중요도 신호는 쓰지 않는다.

### 이미 있는 비슷한 서비스 대비 자리가 불분명하다

kristopolous는 localwiki.org가 20년 넘게 있었다고 했는데,[^kristopolous]
marcomezzavilla는 그 사이트의 유럽 커버리지가 매우 성기다고
답했다.[^marcomezzavilla]
timonoko와 goodpoint는 wiki-map.com이 더 낫다고 했고,[^timonoko][^goodpoint]
plutokras는 nearbywiki.org도 좋다고 했다.[^plutokras]
brianjlogan은 대안들을 모두 돌려 본 뒤 로딩 속도와 근처만 즉시 열어 보는
용도에서 이 사이트의 UX를 택했다고 했다.[^brianjlogan]
지도로 탐색하는 서비스와 달리 이 사이트는 읽는 흐름이 중심이라는 것이 그 선택의
근거로 보인다.

## 인사이트

### 가까움은 같은 글을 다르게 읽게 만든다

nomilk는 무심한 글이 근처에 있다는 이유로 훨씬 절실하게 읽힌다며, 수십 년 전
비행기 추락 글에 몰입했다고 했다.[^nomilk]
benrutter는 이를 심리의 별난 점으로 볼 이유가 없고, 가까운 일에 더 영향받으니
당연하다고 답했다.[^benrutter]
dgunay도 평소라면 찾아보지 않을 글을 끝까지 읽었다고 했다.[^dgunay]
이 반응들이 보여 주는 것은 정보의 가치가 내용만이 아니라 독자와의 거리에 따라
달라진다는 점이다.
같은 위키백과 글이어도 내가 걷는 거리에 있는 글은 확인할 수 있는 현실과
맞닿는다.
이 해석은 이 문서의 것이고, 댓글은 개인의 경험담이다.

### 데이터가 지도에 얼마나 촘촘한지가 이 모델의 상한이다

이 사이트는 위키백과에서 좌표가 있는 글만 쓰므로 위키백과의 지리 편중이 그대로
드러난다.
marcomezzavilla가 말한 유럽 일부 지역의 성긴 커버리지는 다른 서비스의 이야기지만
같은 문제의 다른 얼굴이다.[^marcomezzavilla]
큰 도시의 중심은 포화되어 500개로 잘리고, 시골은 25개를 채우려고 반경이
늘어난다.
같은 알고리즘이 두 극단에서 서로 다른 보증을 하는 셈이다.
따라서 사용자가 겪는 품질은 알고리즘이 아니라 자기 동네의 위키백과 항목 수에
거의 전적으로 달려 있다.

### 이 글을 읽는 방법

이 사이트는 위키백과 geosearch 위에 놓인 읽기 인터페이스이고, 판단에 필요한
정보는 설명문보다 실제 동네에서 열었을 때의 결과다.
오늘 할 일은 자기 동네와 낯선 도시 하나를 입력해 항목 수, 첫 화면에 나오는 글,
그리고 반경이 몇 킬로미터로 표시되는지를 보는 것이다.
이 사이트의 가치를 가를 관찰은 두 가지다.
도시 중심과 시골 두 곳에서 첫 열 개 항목 중 읽을 만한 것이 몇 개인지, 그리고
지오태그가 없어 빠진 근처 항목이 얼마나 되는지다.
둘 다 이 문서는 직접 확인하지 못했다.

---

[^esperent]: <https://news.ycombinator.com/item?id=50205318>

[^throwaway173738]: <https://news.ycombinator.com/item?id=50208653>

[^Trigodil]: <https://news.ycombinator.com/item?id=50205290>

[^kubb]: <https://news.ycombinator.com/item?id=50205174>

[^flohofwoe-lang]: <https://news.ycombinator.com/item?id=50205838>

[^pezezin]: <https://news.ycombinator.com/item?id=50205772>

[^flohofwoe-units]: <https://news.ycombinator.com/item?id=50205849>

[^collabs]: <https://news.ycombinator.com/item?id=50205708>

[^dllu]: <https://news.ycombinator.com/item?id=50205142>

[^koito17]: <https://news.ycombinator.com/item?id=50206751>

[^altilunium]: <https://news.ycombinator.com/item?id=50206100>

[^tannertech]: <https://news.ycombinator.com/item?id=50206458>

[^dspillett]: <https://news.ycombinator.com/item?id=50208923>

[^SCdF]: <https://news.ycombinator.com/item?id=50206172>

[^INTPenis]: <https://news.ycombinator.com/item?id=50205474>

[^xnickb]: <https://news.ycombinator.com/item?id=50206717>

[^paxy]: <https://news.ycombinator.com/item?id=50207182>

[^zulko]: <https://news.ycombinator.com/item?id=50206961>

[^kristopolous]: <https://news.ycombinator.com/item?id=50205897>

[^marcomezzavilla]: <https://news.ycombinator.com/item?id=50206229>

[^timonoko]: <https://news.ycombinator.com/item?id=50205337>

[^goodpoint]: <https://news.ycombinator.com/item?id=50205979>

[^plutokras]: <https://news.ycombinator.com/item?id=50206309>

[^brianjlogan]: <https://news.ycombinator.com/item?id=50206748>

[^nomilk]: <https://news.ycombinator.com/item?id=50205947>

[^benrutter]: <https://news.ycombinator.com/item?id=50205989>

[^dgunay]: <https://news.ycombinator.com/item?id=50213633>
