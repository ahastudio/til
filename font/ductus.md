# Ductus: 내 손글씨로 폰트 만들기

<https://ductus.sorenblank.com>

HN 토론: <https://news.ycombinator.com/item?id=50509972> (368점, 63개 댓글)

GN 토론: <https://news.hada.io/topic?id=37247>

## 소개

Ductus는 페이지 제목이 “Your handwriting, as a font”라고 소개하는 웹 앱이다.
이 문서는 앱의 첫 화면과 HN 스레드를 읽었다. 앱으로 폰트를 만들거나 내보낸 파일을 설치해 보지는 않았고, 제작자나 제작 과정을 설명하는 별도 문서는 찾지 못했다. 앱 안의 서술과 독자 증언을 구분해 적는다.

앱 화면에서 확인한 것은 다음과 같다.

- 입력: 소문자 26자를 하나씩 쓰는 순서(“1 of 26”)로 시작하며, 마우스나 트랙패드나 펜으로 쓰라고 안내한다. 이전, 되돌리기, 지우기, 다음 단추가 있다.
- 미리보기: 쓰는 동안 화면 위쪽에 지금까지 쓴 글자로 만든 단어 미리보기를 보여 준다. 화면에는 “about above after” 같은 단어가 보인다.
- 조정과 내보내기: 상단에 조정(Adjust)과 내보내기(Export) 메뉴가 있다. HN 댓글은 소문자 다음에 대문자 단계도 있다고 증언한다.[^ncx2]
- 다시 열기: 폰트 열기(Open a font…) 기능은 Ductus로 만든 폰트만 열며 기기에서 검사하고 업로드하지 않는다고 적혀 있다.

## 분석

### 중심 주장은 글자 하나씩 쓰는 방식으로도 한 번의 앉은 자리에서 쓸 만한 폰트가 나온다는 것이다

HN 독자의 증언이 이 주장을 뒷받침한다.
한 댓글은 글자 하나씩 쓰면 실제 필체가 담기지 않지만 한 번에 초안을 잡기 쉽게 만든 실행이 가장 좋다고 했다.[^firefoxd]
다른 댓글은 휴대폰에서 손가락으로 쓰기 시작해 멈추지 못하고 전부 쓰는 데 10분이 걸렸다고 했다.[^slim]
한 댓글은 처음에는 자기 글씨가 쓰레기 같다고 생각했는데 원래 자기 필체가 그렇다는 걸 깨닫고 알아보기 어려운 크리스마스 카드를 쓸 수 있게 됐다고 했다.[^eclipticplane]
이 반응은 사용 경험이지 폰트 품질의 평가가 아니다.

### 한계의 핵심은 글자가 서로 이어지는 방식이다

여러 댓글이 같은 점을 짚는다.
진짜 손글씨는 글자의 모양이 주변 글자에 따라 바뀌고, 필기체에서는 특히 그렇다는 것이다.[^arijun]
한 댓글은 필기체를 써 보았으나 잘 되지 않았다고 했고,[^a012] 다른 댓글은 예전에 손글씨 폰트를 파는 회사가 두세 글자 조합의 표본을 받아 이어짐을 담았다며 이 앱은 필기체가 아니라 인쇄체 폰트에 가깝다고 했다.[^whartung]
이 문서는 앱이 필기체 입력을 어떻게 처리하는지 확인하지 못했다.

## 비평

### 문자 범위가 좁아 쓰임이 막힌다

한 댓글은 악센트 문자가 없어 자기 이름을 쓸 수 없고 “내 폰트”로 가장 하고 싶은 일이 이름 쓰기라고 했다.[^johannes1234321]
답글은 조합용 악센트 부호를 위에 얹는 단순한 방식이면 되지 않겠느냐고 했고, 프랑스어에서 à나 ç나 é가 없으면 읽기 어려워진다고 했다.[^cirrrrrrus]
이는 앱이 지금 지원하지 않는다는 독자의 서술이고, 이 문서는 지원 범위를 앱에서 확인하지 못했다.

### 일부 브라우저와 입력에서 오류가 났다는 보고

한 댓글은 중간 글자에서 미리보기가 멈추고 내보내기 단추가 비활성화되었다고 하며 곡선 처리 라이브러리의 오류 메시지를 붙였다.[^tom1337]
다른 사용자는 모든 글자를 쓴 뒤 같은 종류의 오류로 저장이 안 되었다고 했고,[^broabprobe] 또 다른 사용자는 iPad의 Safari에서 같은 일이 있었고 새로고침해도 필체는 남았으나 미리보기가 모두 멈췄으며 Chrome에서 다시 하자 미리보기와 내보내기가 잘 되었다고 했다.[^ncx2]
이 문서는 이 오류를 재현하지 못했다.

### 간격이 실제보다 넓다는 지적과 요청들

한 댓글은 내보낸 글자 사이 간격이 자기 글씨보다 훨씬 넓어 부자연스러워 보이니 마지막에 자간을 조절하는 옵션을 넣어 달라고 했다.[^tancop]
다른 댓글들은 손글씨 사진을 올려 글자를 뽑는 기능,[^ketanip] 사진으로 일부를 채우는 방식,[^mmvvaa] 같은 글자의 여러 변형을 쓸 수 있는 형식에 대한 질문을 했다.[^collabs]
이는 사용자의 요청이며 앱에 있는지는 확인하지 못했다.

### AI 도구로 만드는 대안이 거론되었다

한 댓글은 손으로 쓴 필기체를 Claude에게 주고 글자가 이어지게 폰트를 만들 수 있는지 묻고 가능하다는 답을 받았다고 전했다.[^BubbleRings]
다른 댓글은 태블릿에 A부터 Z까지 써서 Codex에 보내 폰트를 만들어 보았고 그럭저럭이었다고 했다.[^varun_ch]
한 답글은 Claude가 내 필체를 알기를 원하지 않을 수 있다고 했다.[^Tepix]
한 댓글은 이 커뮤니티의 어조가 AI로 어설프게 만든 대체품이 가능해지자 부정적으로 바뀐 점이 흥미롭다고 했다.[^jeffrwells]
이는 독자의 서술이며 이 문서는 AI 대안의 결과를 확인하지 못했다.
Lobste.rs에는 도메인이 올라온 적이 없고, GeekNews 토픽의 유일한 댓글은 HN 의견을 다시 모은 요약이어서 GN 사용자의 반응은 없었다.

## 인사이트

### 글자 하나 입력의 한계와 장점을 같이 보아야 한다

글자를 하나씩 쓰게 하면 입력이 끝나는 시간이 짧아지고 누구나 끝까지 갈 수 있다.
대신 이어짐과 문맥에 따른 변형을 얻지 못한다. 독자들의 반응이 이 둘로 갈린다.
손글씨 폰트를 쓰려는 용도(서명, 카드, 짧은 문구)가 이어짐을 얼마나 요구하는지가 이 앱의 쓸모를 정한다. 이는 이 문서의 정리이다.

### 쓰기 전에 확인할 것

이름에 악센트 문자가 있는지,
쓸 기기가 모바일 Safari인지,
필기체가 필요한지이다.
세 항목 모두 증언에 근거한 확인 항목이고 이 문서는 직접 확인하지 못했다.

### 확인할 관찰

이 앱의 가치를 가를 관찰은 세 가지이다.
악센트 문자와 사용자 지정 글자의 지원이 추가되는지,
오류 보고가 수정되는지,
글자 변형이나 이어짐을 담는 기능이 나오는지이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^ncx2]: <https://news.ycombinator.com/item?id=50513129>

[^firefoxd]: <https://news.ycombinator.com/item?id=50511643>

[^slim]: <https://news.ycombinator.com/item?id=50512196>

[^eclipticplane]: <https://news.ycombinator.com/item?id=50513458>

[^arijun]: <https://news.ycombinator.com/item?id=50516170>

[^a012]: <https://news.ycombinator.com/item?id=50513958>

[^whartung]: <https://news.ycombinator.com/item?id=50512704>

[^johannes1234321]: <https://news.ycombinator.com/item?id=50512083>

[^cirrrrrrus]: <https://news.ycombinator.com/item?id=50515497>

[^tom1337]: <https://news.ycombinator.com/item?id=50511724>

[^broabprobe]: <https://news.ycombinator.com/item?id=50511833>

[^tancop]: <https://news.ycombinator.com/item?id=50515759>

[^ketanip]: <https://news.ycombinator.com/item?id=50517112>

[^mmvvaa]: <https://news.ycombinator.com/item?id=50511138>

[^collabs]: <https://news.ycombinator.com/item?id=50515783>

[^BubbleRings]: <https://news.ycombinator.com/item?id=50513365>

[^varun_ch]: <https://news.ycombinator.com/item?id=50512631>

[^Tepix]: <https://news.ycombinator.com/item?id=50515900>

[^jeffrwells]: <https://news.ycombinator.com/item?id=50515964>
