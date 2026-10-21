# Nordwand Mono: Python 코드로 그린 코딩용 네오 그로테스크 고정폭 글꼴

<https://github.com/tywr/Nordwand-Mono>

HN 토론: <https://news.ycombinator.com/item?id=50141581> (543점, 152개 댓글)

GN 토론: <https://news.hada.io/topic?id=35699>

## 소개

Nordwand Mono는 코딩용으로 만든 컴팩트한 네오 그로테스크 고정폭 글꼴이다.
제작자 Tanguy Vivier는 터미널과 Neovim에서
쓸 완벽한 글꼴을 찾지 못해 Python으로 처음부터 직접 그렸다고 설명한다.
디자인 목표는 고전 글꼴 Univers의 요소를 JetBrains Mono의 비례에 담는 것이다.
이름은 스위스와 그 대표적인 타이포그래피를 가리키는데,
스위스 북벽의 딱딱하고 차가운 분위기에서 따왔다고 한다.
README는 영감의 원천으로 Univers, Apple의 SF Pro와 SF Mono,
Sharp Type의 Alpes Mono, Dalton Maag의 Ubuntu Mono를 든다.

저장소는 2026년 3월 28일에 만들어졌고, 이 문서를 쓴 시점에 별은 1,241개다.
릴리스는 2026년 9월 12일의 1.3.0, 9월 29일의 1.3.1, 10월 20일의 1.3.2이고,
릴리스마다 OTF, TTF, WOFF, WOFF2 압축 파일이 올라온다.[^releases]
코드는 MIT 라이선스(`LICENSE.txt`)이고
글꼴 자체는 SIL Open Font License 1.1(`LICENSE-FONT.txt`)이다.[^license]
README는 두 라이선스를 언급하지 않으므로 저장소 파일을 열어야 알 수 있다.

## 특징

글꼴의 기능은 OpenType 기능 태그로 켜는 선택 항목으로 구성된다.
기본값에서는 합자가 `->`와 `=>` 둘뿐이다.
대체 문자는 문자별 변형(`cv`)으로,
묶음 변경은 스타일 세트(`ss`)로 켠다.[^altchars]

| 기능   | 대상              | 효과                                                |
| ------ | ----------------- | --------------------------------------------------- |
| `cv01` | `0`               | 빗금 있는 0                                         |
| `cv02` | `a`               | 대체 형태. 이탤릭 전용                              |
| `cv03` | `l`               | 대체 형태                                           |
| `cv11` | `f`               | 대체 형태 두 가지                                   |
| `cv12` | `m`               | 대체 형태                                           |
| `cv19` | `3`               | 대체 형태                                           |
| `ss02` | `->` `=>`         | `liga`가 꺼져 있어도 화살표 합자를 켠다             |
| `ss03` | `<` `>` `->` `=>` | 비교 기호와 화살표 머리를 넓은 각도의 형태로 바꾼다 |
| `dlig` | `=` `-` `_` `#`   | 같은 문자가 반복된 구간의 가로 막대를 이어 붙인다   |

`ss02`가 따로 있는 이유는 많은 편집기와
터미널이 코드용으로 `liga`를 꺼 두기 때문이다.
`ss02`를 켜면 다른 합자는 켜지 않고 화살표만 되살릴 수 있다.[^sets]
기본값의 `<`와 `>`는 대부분의 코딩 글꼴처럼 좁은 각도이고,
`ss03`이 더 높고 넓은 형태로 바꾼다.
`dlig`는 반복 길이에 제한이 없고
문자마다 자기 칸을 유지하므로 정렬과 커서 이동에 영향이 없다.
`=-`처럼 섞인 구간은 잇지 않는다.[^sets]

문서는 CSS와 kitty, Ghostty, WezTerm에서 켜는 방법을 보여 준다.

```css
code {
  font-family: "Nordwand Mono";
  font-feature-settings: "ss02", "ss03", "dlig";
}
```

```text
# Ghostty
font-feature = ss02
font-feature = ss03
font-feature = dlig

# kitty (스타일마다 한 번씩, PostScript 이름은 kitty +list-fonts --psnames)
font_features <PostScript name> +ss02 +ss03 +dlig
```

```lua
-- WezTerm
config.harfbuzz_features = { "ss02", "ss03", "dlig" }
```

## 직접 빌드하기

이 글꼴은 Python으로 생성한다.
글리프마다 Python 클래스가 있고
그 안에 그리기 컨텍스트 객체를 주입해 모양을 그린다.
x 높이나 대문자 높이 같은 치수를 바꾸려면
`config.example.yml`을 복사해 값을 고친다.
예시 파일의 기본 치수는 units_per_em 1000, ascent 750, descent -200,
cap 710, x_height 540, window_width 600이다.[^config]

```bash
uv sync                                                    # 의존성 설치
python -m visualize --config config.yml <glyph_id>         # 글리프 하나를 미리보기
python -m generate_font --config config.yml                # 전체 글꼴 생성(./custom-fonts)
```

README는 치수를 바꾸면 좋아 보인다는 보장이 없고
일부 글리프는 손봐야 할 수 있다는 경고를 단다.
makefile에는 웹 글꼴 빌드, OTF 빌드,
macOS에 OTF를 설치하는 목표도 있다.[^makefile]

## 비평

### 어디가 새로운지 정량적인 비교가 없다

README는 Univers의 요소를 JetBrains Mono의 비례에 넣었다고
말하지만 어느 값이 어떻게 같고 다른지는 적지 않는다.
HN의 rootlocus는 빠르게 비교해 보니 99%가 JetBrains Mono이고 `$`,
`&`, `#` 같은 몇 글자만 다르다고 했다가
비교 그림을 만든 뒤 조금 더 다르다고 고쳤다.[^rootlocus]
jan_m_savage는 유료 글꼴 Berkeley Mono와 비슷하지만 Nordwand가 더 부드럽고,
날카로운 곡선과 균일한 글자 요소 때문에 중요한 데이터를 담고
있다는 인상을 준다고 했다.[^jan_m_savage]
이런 평은 취향이고 같은 글꼴에 대해 정반대의 인상도 나올 수 있다.
치수는 공개되어 있으니 자기 글꼴과 직접 겹쳐 보는 것이 확실하다.

### 혼동하기 쉬운 글자의 판별은 사용자가 시험해야 한다

HN의 Findecanor는 나이 든 눈에는 작은 크기에서 8과 0이 헷갈리기 시작했다며
모노스페이스 글꼴이 두 글자를 더 다르게 만들었으면 좋겠다고 했다.[^Findecanor]
이 글꼴에는 빗금 있는 0(`cv01`)이 있지만 기본 0에는 빗금이 없고,
그 댓글이 이를 켜 봤는지는 알 수 없다.
kqr은 높은 `<`와 `>`가 실제 유니코드 왼쪽과
오른쪽 꺾쇠 〈 〉와 구분이 잘 안 될 것을 걱정했고,
하이픈 마이너스 `-`가 꽤 길다고도 덧붙였다.[^kqr]
기본 `<`와 `>`는 좁은 각도이고 높은 형태는 `ss03`에서
나오므로 이 걱정은 어느 설정을 봤느냐에 달려 있다.
어느 쪽이든 판별성은 작은 크기와 자기 화면에서 확인해야 한다.

### 한글과 가변 글꼴과 힌팅에 관한 정보가 없다

README가 보여 주는 문자 범위는 라틴 문자와 키릴 문자 표본이다.
한글, 일본어와 중국어, Nerd Font 아이콘, 가변 글꼴, 힌팅에 관한 설명은 없다.
GeekNews에 다시 모인 HN 의견에도 가변 글꼴을 지원하느냐는 질문이 있었지만
이 문서는 그 답을 찾지 못했다.[^gn-plus]
한국어를 함께 쓰는 개발자라면
한글이 어떤 글꼴로 대체되는지와 폭이 맞는지를 먼저 확인해야 한다.

### 글꼴이 아니라 도구로서의 가치가 더 크다

저자는 HN에서
이 프로젝트가 글꼴 파일을 나눠 주는 것보다 Python
샌드박스를 제공하는 것이 목적이라고 밝혔다.
글리프를 그리고 확인하는 데 외부 도구가 필요 없고,
마음에 안 드는 글리프는 포크하거나 PR로 고쳐도 좋다고 했다.[^tywr]
이 방향이라면 글꼴을 쓰는 사람보다 고쳐 쓰는 사람이 대상이고,
README의 경고대로 치수를 바꾸면 글리프 쪽 손질이 따라온다.
그래서
이 저장소를 평가하는 기준은 완성된 글꼴인지가 아니라 고치기 쉬운 코드인지다.
gorgoiler는 A 하나를 그리려고 글꼴 라이브러리를 끌어오지 않고
호환되는 그리기 컨텍스트만 넘기면 되는 점이 좋다고 했다.[^gorgoiler]

## 인사이트

### 글꼴을 코드로 쓰면 변형은 쉬워지지만 치수가 글리프에 스며 있다

글리프를 클래스로 그리고 치수를 설정 파일로 바꾸는 구조는 디자인을 차이로 보고
되풀이해서 만들 수 있게 한다.
어떤 변경이 어느 선을 움직였는지 리뷰할 수 있고,
같은 코드에서 웹용과 OTF를 다 만든다.

그러나 README의 경고가 이 접근의 대가를 정확히 말한다.
치수는 값 하나가 아니라 모든 글리프가 암묵적으로 전제한 값이어서,
x 높이를 바꾸면 곡선과 연결부가 어긋난다.
매개변수로 글꼴을 만든다는 아이디어는 Donald Knuth의
METAFONT가 오래전에 탐구한 방향과 닮았다.
이는 이 문서의 비유이고 METAFONT는 이 문서가 확인하지 않았다.

### 합자는 기본값이 아니라 선택 항목이어야 했다

제작자가 합자를 `->`와 `=>` 둘로 줄인 이유가 댓글에 있다.
HN의 traxler는 `==`나 `===`의 합자가 싫어서
대개 합자를 꺼 두지만 화살표와 `!=`는 좋아한다고 했다.[^traxler]
합자 취향은 한 글꼴 안에서도 갈리고,
편집기는 하나로 켜고 끄는 `liga` 스위치만 주는 경우가 많다.

`ss02`가 이 간극을 메운다.
`liga`를 끈 사람도 화살표만 얻을 수 있고, 구분선용 `dlig`는 따로 켠다.
대가는 설정의 책임이 사용자에게 넘어간다는 것이다.
kitty는 스타일마다 PostScript 이름을 찾아 적어야 하고,
편집기마다 쓰는 방법이 다르다.
선택 항목이 많은 글꼴은 기본값만 쓰는
사람과 모든 것을 켜는 사람의 화면이 달라진다.

### 고정폭 글꼴은 제약이 비슷해서 차이는 세부에서 나온다

가로 폭 600과 비슷한 x 높이라는 제약에서는 글꼴이 서로 닮을 수밖에 없다.
rootlocus가 느낀 99%라는 인상은 그 결과다.
그래서 차이는 `<`, `>`, `0`, 화살표, `#` 같은 기호에 모인다.
코드에서 가장 자주 읽히면서 글꼴마다 가장 갈리는 글자들이다.

이 차이가 취향의 영역을 넘어 판독성의 영역에 걸쳐 있다는 점이 문제다.
Findecanor의 0과 8, kqr의 꺾쇠와 유니코드 꺾쇠가 그 예다.
독창적이려면 기호를 바꿔야 하고,
기호를 바꾸면 기존 글꼴로 훈련된 눈이 오독할 위험이 커진다.
고르는 사람은 자기 코드에서
헷갈리기 쉬운 글자를 한 줄에 놓고 직접 보는 것이 가장 빠르다.

```text
0O o 8B 1lI| `'" ,. ;: {}[]() <> -> => != === #### ---- ____
```

---

[^releases]: GitHub, [Releases · tywr/Nordwand-Mono](https://github.com/tywr/Nordwand-Mono/releases), 2026-10-20

[^license]: GitHub, [LICENSE-FONT.txt](https://github.com/tywr/Nordwand-Mono/blob/main/LICENSE-FONT.txt)

[^altchars]: GitHub, [Alternative Characters](https://github.com/tywr/Nordwand-Mono/blob/main/doc/alternative_characters.md)

[^sets]: GitHub, [Stylistic Sets and Optional Ligatures](https://github.com/tywr/Nordwand-Mono/blob/main/doc/stylistic_sets.md)

[^config]: GitHub, [config.example.yml](https://github.com/tywr/Nordwand-Mono/blob/main/config.example.yml)

[^makefile]: GitHub, [makefile](https://github.com/tywr/Nordwand-Mono/blob/main/makefile)

[^rootlocus]: <https://news.ycombinator.com/item?id=50162114>

[^jan_m_savage]: <https://news.ycombinator.com/item?id=50163051>

[^Findecanor]: <https://news.ycombinator.com/item?id=50163542>

[^kqr]: <https://news.ycombinator.com/item?id=50162865>

[^tywr]: <https://news.ycombinator.com/item?id=50163214>

[^gorgoiler]: <https://news.ycombinator.com/item?id=50162290>

[^traxler]: <https://news.ycombinator.com/item?id=50162002>

[^gn-plus]: <https://news.hada.io/topic?id=35699#cid68094>
