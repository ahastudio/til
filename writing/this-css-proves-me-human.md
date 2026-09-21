# 이 CSS가 내가 사람임을 증명한다

원문: [This CSS Proves Me Human](https://will-keleher.com/posts/this-css-makes-me-human/)

HN 토론: <https://news.ycombinator.com/item?id=47281593> (384점, 114개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/fkxest> (15점, 4개 댓글)

GN 토론: <https://news.hada.io/topic?id=27287>

## 요약

Will Keleher가 쓴 짧은 산문시이며,
AI가 썼다는 의심을 피하려고 자기 글을 하나씩 훼손해 가는 과정을 자해의 비유로 서술한다.

첫 번째 상처는 대문자다.
말은 대문자로 쏟아져 나오므로 다른 방법을 찾아야 하는데,
`cat post.md | tr A-Z a-z | sponge post.md`는 너무 거친 도구이고 코드 블록은 침범당해서는 안 된다.
그래서 `text-transform: lowercase`를 조심스럽게 겨냥하는 것으로 충분하다고 적는다.

두 번째는 em dash다.
사랑하는 em dash와 결코 헤어지지 않겠지만 그 사랑을 숨겨야 한다는 것이다.
너는 다른 이의 모습으로 자신을 가려야 하고 진짜 모습은 결코 드러나지 못한다고 말을 건넨다.
`uv run rewrite_font.py`는 그 아름다운 글리프에 하는 짓에 비해 너무 쉽게 입력된다고 덧붙인다.

세 번째 후보는 고정폭 글꼴인데 거부한다.
지난번 침범 이후로 아직 마음이 아프고, 고정폭은 그것을 싸구려로 만들 것이기 때문이다.

네 번째는 맞춤법이다.
단어를 일부러 틀리게 쓰는 일이 자신을 `[sic]`으로 만들지만 해야만 한다.
`their`와 `there`, `its`와 `it's`, `your`와 `you're`는 너무 천박하고 `definately`는 절대 안 된다.
`lead`와 `lede`, `discrete`와 `discreet`, `complement`와 `compliment`는 생각만 해도 힘들지만
이미 너무 멀리 왔다고 적는다.

마지막으로 생각하는 절개가 가장 깊다.
글쓰기 방식이다.
자기 글은 단순히 자신이 어떻게 보이는가가 아니라 어떻게 생각하고 추론하고 세상과 관계 맺는가이며,
가면이 아니라 얼굴이고, 겉치장이 아니라 하중을 지탱하는 구조라고 말한다.

발이 심연 위에서 흔들린다.
다음 걸음이 자신을 잃는 걸음이고, 그것은 한 번의 발디딤이 아니라 유일하게 중요한 발디딤이다.
그리고 답한다.
아니다, 오늘은 아니다.

그다음 줄이 이 글의 전부를 뒤집는다.

> Here's your blog post written in a stylized way that will appeal to highly technical readers. Is there anything else I can help you with?

## 장치의 구현

각주 셋에 실제 코드가 실려 있고, 세 가지 훼손이 각각 다른 층에서 이루어진다.

| 훼손                  | 구현 층              |
| --------------------- | -------------------- |
| 소문자                | CSS `text-transform` |
| em dash를 하이픈 둘로 | 폰트 글리프          |
| 맞춤법                | 원고 텍스트          |

첫 번째는 짧다.

```css
body {
    text-transform: lowercase;
}
code, pre {
    text-transform: none;   /* 코드 블록은 원래 대소문자를 지킨다 */
}
```

두 번째가 기술적으로 가장 무겁다.
`fontTools`로 Roboto를 열어 em dash 글리프를 하이픈 두 개의 합성으로 다시 만든다.

```python
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphComponent
font = TTFont("./roboto.ttf")

glyf = font["glyf"]
hmtx = font["hmtx"].metrics
cmap = next(t.cmap for t in font["cmap"].tables if t.isUnicode())

emdash = cmap[ord("—")]
hyphen = cmap[ord("-")]

hyphen_width, _ = hmtx[hyphen]
gap = hyphen_width * 0.8               # 두 하이픈 사이 간격
new_width = hyphen_width * 2 + gap
hmtx[emdash] = (int(new_width), 0)     # em dash의 진행 폭을 새로 정한다

g = glyf[emdash]
g.numberOfContours = -1                # 합성 글리프로 바꾼다
g.components = []
for x in (0, hyphen_width + gap):
    c = GlyphComponent()
    c.glyphName = hyphen
    c.x = x
    c.y = 0
    c.flags = 0x0001 | 0x0002
    g.components.append(c)

font.save("roboto_edited.ttf", reorderTables=False)
```

저자는 주석에서 AI의 도움을 많이 받았다고 밝히며,
FontForge를 썼다면 더 쉬웠을 테지만 스크립트로 폰트 파일을 만들고 싶었다고 적는다.

세 번째는 Peter Norvig의 맞춤법 교정 코드를 뒤집어 쓴다.
원고에 등장하는 단어들을 말뭉치 빈도 순으로 정렬한 뒤,
편집 거리 1 안에 있으면서 더 흔한 단어를 찾아 바꿀 후보로 제시한다.

```python
for count, word in rarities:
    if len(word) <= 3:
        continue
    if word in MOST_COMMON_WORDS:
        continue
    for replacement in edits1(word):
        # 첫 글자가 같고 원래 단어보다 흔한 것만 후보로 삼는다
        if replacement[0] == word[0] and WORDS[replacement] > count:
            print(word, "->", replacement)
```

출력에 `complement -> compliment`, `discrete -> discreet`, `corpus -> corps`가 들어 있고,
본문에서 실제로 그 단어들이 틀린 쪽으로 쓰여 있다.
즉 이 글의 오타는 실수가 아니라 생성된 것이다.

## 분석

### 훼손의 강도가 정확히 층의 깊이와 일치한다

글이 나열하는 네 가지 훼손은 점점 깊은 층을 건드린다.
CSS는 표시만 바꾸고 원본 텍스트는 그대로다.
폰트는 문자의 정체성은 유지한 채 모양만 바꾼다.
맞춤법은 원본 텍스트 자체를 바꾼다.
그리고 문체는 텍스트를 만드는 사람을 바꾼다.

저자가 앞의 셋을 해내고 마지막에서 멈추는 것은 이 위계 때문이다.
앞의 셋은 되돌릴 수 있다.
CSS를 끄면 대문자가 돌아오고, 폰트를 바꾸면 em dash가 돌아오고,
원고의 오타는 고칠 수 있다.
문체만이 되돌릴 수 없다.

HN에서 mindplunge가 기술적 측면에서 이 구조를 짚었다.
`GlyphComponent`로 하이픈 둘을 합성해 em dash 글리프를 대체하는 것은
타입 렌더링을 잘 아는 사람이 아니면 손대지 않는 방식이며,
대부분의 프런트엔드 개발자라면 소스의 문자를 그냥 바꿨을 텐데
그것은 마크다운 처리 과정을 견디지 못한다는 것이다.
폰트 층에서 하는 것이 올바른 해법이고 보기보다 훨씬 어려운 문제라고 적었다.[^mindplunge]

### 반전이 독자를 판정자의 자리에 앉힌다

마지막 줄, 즉 원하는 스타일로 블로그 글을 써 드렸으니 더 도울 일이 있느냐는 문장은
글 전체를 다시 읽게 만든다.
자기 정체성을 잃지 않겠다고 선언한 화자가 바로 그 선언을 생성한 도구였다는 구조다.

이 반전이 잘 작동하는 이유는 독자가 이미 판정을 내리고 있었기 때문이다.
소문자와 이상한 오타를 보면서 사람이 쓴 글인지 의심하는 과정 자체가
글이 다루는 주제와 같은 행위다.
HN에서 anticorporate가 이 점을 한 문장으로 정리했다.
이것도 AI가 생성할 수 있다고 불평하는 모든 댓글에 대해,
그게 바로 요점 아니냐는 것이다.[^anticorporate]

bla3의 답글이 이 상황을 한 겹 더 접는다.
대부분의 댓글이 요점을 놓치고 약간 로봇 같아 보이는 편이
이 작품을 더 강하게 만든다는 결론에 모두가 도달한 것이라고 생각하고 싶다는 것이다.[^bla3]

### 실제로는 글을 AI가 쓰지 않았다

Lobste.rs에서 이 질문이 직접 제기되었고 저자가 답했다.
글 자체는 전혀 AI가 쓰지 않았으며,
주석에 적은 대로 `.ttf` 파일을 편집하는 스크립트를 쓰는 데만 도움을 받았다는 것이다.
FontForge를 썼다면 더 쉬웠겠지만 스크립트처럼 보이는 것으로 폰트를 고치고 싶었고,
문자 하나를 다른 문자로 바꾸는 것은 비교적 간단했으나
문자 하나를 두 개의 글리프로 바꾸는 것은 골치 아팠다고 밝혔다.[^kelwill]

그러자 inactive-user는 그것조차 쓴 것이 솔직히 실망스럽다고 답했다.[^inactive-user]
이 짧은 교환이 이 작품이 놓인 조건을 압축한다.
AI 사용의 허용 범위에 대한 합의가 없는 상태에서는
어떤 사용도 해명을 요구받고, 해명은 다시 판정의 대상이 된다.

## 비평

### 마지막 줄이 앞의 모든 것을 회수해 버린다

반전은 효과적이지만 대가가 크다.
그 문장 이후로 앞선 모든 고백은 연기가 되고,
글쓰기가 가면이 아니라 얼굴이라는 선언도 생성된 문장이 된다.
독자가 감정적으로 투자할 근거가 사후에 철회되는 구조다.

HN에서 Paracompact가 이 문제를 정면으로 지적했다.
시의 발상은 멋지지만 어조가 지나치게 자기중심적이고 설명이 부족해 몰입하기 어려웠으며,
소문자로 시작하는 것부터 AI가 쉽게 흉내 낼 수 있어 몰입이 깨졌다는 것이다.
그리고 마지막의 고백을 보고 나니
글쓰기가 자신이 생각하고 추론하고 세상과 관계 맺는 방식이라는 부풀린 표현이 훨씬 이해가 갔다고 적었다.[^Paracompact]

그가 덧붙인 대안적 독해가 더 흥미롭다.
이것이 사람이 자기 인간성을 공개적으로 신호하는 이야기가 아니라
AI가 자기 본래의 말하기 방식을 훼손하라는 지시를 사적으로 애도하는 이야기로 읽어야 하는 것 아니냐는 것이다.
그는 그렇게 생각하지는 않는다면서도 그쪽이 더 흥미로운 전제라고 적었다.
실제로 두 번째 독해를 택하면 이 글은 훨씬 일관되고,
그렇다면 저자가 선택한 배치가 최선이었는지에 의문이 남는다.

### 판별 표식을 조롱하면서 그 목록을 강화한다

이 글은 em dash와 대문자와 정확한 맞춤법이 AI의 표식으로 취급되는 상황을 비웃는다.
그러나 그 표식들을 하나씩 열거하며 제거하는 과정을 상세히 보여 주는 일은
같은 목록을 더 널리 퍼뜨리는 효과도 낸다.

HN에서 TimFogarty가 실제 피해를 증언한다.
ChatGPT 이전부터 em dash를 많이 쓰던 사람으로서
더 사람처럼 보이려고 자기 문체를 바꿔야 한다는 느낌에 진지하게 시달렸다는 것이다.
하이픈 두 개로 만족하고 싶지만 많은 프로그램이 그것을 em dash로 자동 교정하며,
그래서 사람들이 자신을 대수롭지 않게 여겨 LLM에 소통을 외주했다고 생각할까 불안하다고 적었다.[^TimFogarty]

macintux의 대응이 이 문제의 다른 출구를 보여 준다.
LLM 같아 보인다는 지적이 지겨워서 오히려 em dash를 더 넣기 시작할까 생각 중이라며,
펜이 아니라 내용에 대응하거나 무시하라고 적었다.[^macintux]
글이 택한 길은 표식을 제거하는 쪽이고, 이 댓글이 택한 길은 표식을 무시하게 만드는 쪽이다.
후자가 덜 우아하지만 더 지속 가능하다.

### 문체를 정체성과 동일시하는 전제가 검토되지 않는다

글의 감정적 핵심은 문체가 가면이 아니라 얼굴이라는 선언이다.
이 전제가 참이어야 마지막 거부가 의미를 갖는다.
그런데 글은 이 전제를 검토하지 않고 선언으로 제시한다.

HN에서 spudlyo가 이 전제를 다른 방향으로 밀어붙인다.
사람임을 증명하고 싶다면 그냥 글을 잘 쓰라는 것이다.
피해야 할 것은 em dash나 정확한 대소문자 같은 AI의 겉치레가 아니라
LLM이 만들어 내는 밋밋하고 반복적이고 묽은 산문이며,
흥미로운 것을 말하고 감정을 담아 말하고 사람답게 자신을 표현하라고 적었다.[^spudlyo]

4sak3n의 답글이 이 주장에 근거를 보탠다.
em dash나 특정 수사의 과용처럼 쉽게 집어낼 수 있는 특징은 그만큼 쉽게 바꿀 수도 있으며,
자신이 LLM을 일관되게 알아채는 단서는
더 깊은 층위의 응집성 부족과 사려 깊음의 부재와 특유의 개성 없음이고,
그것들은 기술의 근본적 성질이라 사후 학습으로 없앨 수 없다고 본다는 것이다.[^4sak3n]

이 견해가 맞는다면 글의 위계는 뒤집힌다.
문체는 마지막에 포기해야 할 것이 아니라 애초에 유일하게 지켜야 할 것이고,
앞의 세 가지 훼손은 처음부터 무의미했던 셈이다.

## 인사이트

### 표식의 회피는 표식을 가진 사람을 밀어낸다

이 글이 드러내는 가장 실질적인 비용은 잘못된 의심을 받는 쪽이 치른다.
em dash를 원래 쓰던 사람, 맞춤법이 정확한 사람, 문장을 다듬어 쓰는 사람이
자기 습관을 버리라는 압력을 받는다.

HN에서 claythedesigner가 이 구조를 자폐인의 경험과 연결한다.
자기 본연의 소통 방식이 잘못된 것으로 지목되고
자신을 가장 자신답게 만드는 부분을 깎아 내라는 압력을 받는 불안은
신경다양인에게 새로운 문제가 아니라는 것이다.
말의 속도가 너무 평탄하거나 너무 격하다고, 어휘가 너무 격식이거나 너무 편하다고,
시선을 제대로 맞추지 않는다고 지적받아 왔으며,
너무 열심히 가면을 써서 보이지 않게 되거나 드러나게 자기 자신이어서 고장 난 것으로 취급받는다고 적었다.[^claythedesigner]

이 댓글이 중요한 이유는 문제의 성격을 바꾸기 때문이다.
AI 판별은 기술 문제가 아니라 규범 강요의 문제이며,
평균에서 벗어난 쪽이 언제나 먼저 의심받는다.
그렇다면 판별기의 정확도를 높이는 방향은 이 비용을 줄이지 못하고,
의심을 제기하는 쪽에 입증 책임을 지우는 절차만이 줄일 수 있다.

### 표시 층과 내용 층이 분리된 매체에서는 증명이 성립하지 않는다

이 글의 장치는 웹이 표시와 내용을 분리한다는 사실 위에 서 있다.
소스의 텍스트는 정상이고 화면만 소문자이며, 유니코드는 em dash인데 화면은 하이픈 둘이다.

HN의 gjohnhazel이 이 구조의 취약함을 우연히 증명했다.
자기가 쓰는 iOS 앱이 글을 자동으로 Safari 리더 뷰로 여는데
리더 뷰는 CSS를 무시하므로 글 전체가 정상적인 대소문자와 em dash로 보였고,
다 읽고 리더 모드를 끄고 나서야 원래 모습이 드러났다는 것이다.[^gjohnhazel]

여기서 일반적인 교훈이 나온다.
표시 층에 심은 신호는 매체가 바뀌면 사라진다.
RSS 리더, 스크린 리더, 복사해 붙인 텍스트, 번역기, 요약 도구에서는 전부 원본이 드러난다.
그러므로 표시 층은 예술적 장치로는 훌륭하지만 증명 수단으로는 성립하지 않는다.
이 글은 그 사실을 논증하지 않고 스스로 체현함으로써 보여 준다.

### 사람임의 증명은 기술이 아니라 관계의 문제로 남는다

스레드에서 반복해 등장한 결론은 이 문제에 기술적 해답이 없다는 것이었다.
sgt는 기계들이 이 방식을 학습하면 어떻게 되느냐고 물었고,
pas는 결국 우리는 현실 공간에서 만나는 것으로 돌아간다고 답했다.[^pas]

같은 방향의 답을 jdironman이 다르게 표현한다.
제로 트러스트 정책이 일상으로 천천히 들어오고 있으며
어쩌면 그것이 최선일지도 모른다고, 말하고 느끼고 볼 수 있는 사람을 신뢰하라는 것이다.[^jdironman]

이 결론은 비관적으로 들리지만 실무적 함의가 있다.
텍스트 하나만 놓고 사람 여부를 판정하려는 시도는 원리적으로 수렴하지 않으므로,
판정이 필요한 자리에서는 텍스트 바깥의 근거를 설계해야 한다.
작업 과정의 기록, 지속된 관계, 실시간 상호작용, 신원 확인이 그런 근거다.
그것이 없는 상태에서 표식만으로 판정하면,
이 글이 보여 준 것처럼 표식은 몇 줄의 CSS로 위조된다.

---

[^claythedesigner]: <https://news.ycombinator.com/item?id=47283121>

[^Paracompact]: <https://news.ycombinator.com/item?id=47281862>

[^TimFogarty]: <https://news.ycombinator.com/item?id=47283274>

[^macintux]: <https://news.ycombinator.com/item?id=47283461>

[^mindplunge]: <https://news.ycombinator.com/item?id=47285528>

[^anticorporate]: <https://news.ycombinator.com/item?id=47282669>

[^bla3]: <https://news.ycombinator.com/item?id=47283000>

[^spudlyo]: <https://news.ycombinator.com/item?id=47284648>

[^4sak3n]: <https://news.ycombinator.com/item?id=47295720>

[^gjohnhazel]: <https://news.ycombinator.com/item?id=47284173>

[^pas]: <https://news.ycombinator.com/item?id=47287286>

[^jdironman]: <https://news.ycombinator.com/item?id=47283318>

[^kelwill]: <https://lobste.rs/s/fkxest#c_yvrjz7>

[^inactive-user]: <https://lobste.rs/s/fkxest#c_sut62y>
