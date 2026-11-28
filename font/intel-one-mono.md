# Intel One Mono

<https://github.com/intel/intel-one-mono>

HN 토론: <https://news.ycombinator.com/item?id=50653667> (541점, 261개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/maihrd/intel_one_mono_font_aiming_for_clarity_low> (26점, 9개 댓글)

GN 토론: <https://news.hada.io/topic?id=37899>

## 소개

Intel One Mono는 Intel이 공개한 고정폭(monospace) 글꼴 가족이다.
README는 저시력 개발자라는, 글꼴 시장에서 소외된 독자를 겨냥해
Frere-Jones Type이 Intel 브랜드 팀, VMLY&R와 함께 설계했다고 밝힌다.
설계 단계마다 저시력 및 법적 시각 장애 개발자 패널이 의견을 냈다고 한다.
목표는 개발자의 피로와 눈의 부담, 코딩 오류를 줄이는 것이다.

라이선스는 SIL Open Font License 1.1이고,
저장소는 홈페이지를 등록하지 않았으며 README에도 별도 사이트 링크가 없다.
저장소에 적힌 소개 문구는 글꼴 저장소라는 한 줄뿐이다.
GitHub API가 보고한 현황은 읽은 시점(2026년 11월 27일) 기준 다음과 같다.

| 항목        | 값                        |
| ----------- | ------------------------- |
| 생성        | 2023년 4월 11일           |
| 마지막 푸시 | 2026년 11월 4일           |
| 스타        | 10,938                    |
| 포크        | 348                       |
| 열린 이슈   | 14(풀 리퀘스트 포함 집계) |
| 릴리스      | V1.0.0부터 V1.5.0까지 6개 |

릴리스 날짜는 V1.0.0이 2023년 4월 21일, V1.2.0과 V1.2.1이 2023년 6월 7일,
V1.3.0이 2023년 8월 21일, V1.4.0이 2024년 7월 26일,
V1.5.0이 2026년 11월 4일이다.
HN 제목에 붙은 2023은 글꼴이 처음 공개된 해를 가리키는 것으로 보인다.
최신 릴리스는 이번 달에 나왔다.

## 구성

글꼴은 Light, Regular, Medium, Bold 네 굵기와 각각의 이탤릭으로 제공된다.
V1.5.0 릴리스 노트에 따르면 글리프는 1385개이고,
라틴 문자를 쓰는 200개 넘는 언어를 지원한다.
권장 크기는 인쇄에서 7pt 이상, 화면에서 9px 이상이다.

V1.5에서 점자(braille)와 Powerline 지원, 여러 화살표와 기호,
둥근 윗부분 3이 추가되었다.
배포 형식은 데스크톱용 OTF와 TTF, 웹용 WOFF와 WOFF2, 편집용 UFO 원본이다.
TrueType 계열 파일은 화면 표시를 위해 손으로 힌팅(hinting)했다고 한다.
삽입 제한은 없다.

OpenType 기능은 스타일 세트로 켠다.

| 기능   | 내용                                 |
| ------ | ------------------------------------ |
| `ss01` | 프로그래밍 합자(ligature)            |
| `ss02` | 이하, 이상 기호를 화살표 형태로 바꿈 |
| `ss03` | `www` 합자                           |
| `ss04` | 둥근 윗부분 3                        |
| `ss11` | 숫자 사이에서 올라간 콜론(문맥 적용) |
| `ss12` | 올라간 콜론(전체 적용)               |

합자는 기본으로 꺼져 있다.

## 사용법

설치는 저장소의 Releases에서 받은 파일을 쓰라고 안내한다.
에디터 설정은 README가 세 가지를 적는다.

```text
VSCode          설정에서 Font Family를 Intel One Mono로 지정
Sublime Text    font_face를 Intel One Mono로 지정
IntelliJ        Editor > Font에서 Intel One Mono 선택
```

합자는 에디터에서 스타일 세트를 켜야 한다.
VSCode는 `"editor.fontLigatures": "'ss01'"`를,
Sublime Text는 `"font_options": ["ss01"]`을 설정에 추가한다.

원본 편집은 `sources` 디렉터리의 UFO 파일로 하며,
README는 RoboFont 4.4를 권장한다.
굵기마다 따로 고치는 인스턴스 소스와,
가장 가는 굵기와 가장 굵은 굵기를 담은 마스터가 따로 있다.
마스터를 고치면 보간을 다시 돌려야 하고,
마스터는 PostScript 형식으로만 제공된다.
TrueType의 손 힌팅 원본은 `hinting/truetype hinting source`에 있다.

## 분석

### 읽기 쉬움의 근거는 설계 과정에 있다

이 글꼴의 차별점으로 내세우는 것은 모양보다 과정이다.
저시력 개발자 패널이 단계마다 의견을 냈다는 설명이 핵심이다.
HN에서 virtualritz는 대기업이 저마다 고정폭 글꼴을 내는 것이 지겹고
기존 선택지와 충분히 다른지 의문이라고 썼다.[^virtualritz]
dspillett은 저시력 패널의 참여가 잠재적인 핵심 차별점이라고 답했다.[^dspillett]
패널이 어떤 방식으로 평가했고 그 결과가 어떤 글리프 결정으로 이어졌는지는
README에 없다.

### 글리프 구분은 고정폭 글꼴의 오래된 과제다

README가 예로 드는 소문자 e와 대문자 G처럼
다른 글자와 헷갈리기 쉬운 형태를 분명히 하는 것이 설계의 한 축이다.
HN에서는 이 문제를 두고 의견이 갈렸다.
kleiba2는 1980년대부터 여러 시스템을 써 왔지만
소문자 l과 숫자 1, 대문자 O와 숫자 0이
헷갈려서 문제가 된 적은 없다고 했다.[^kleiba2]
Jakob은 사람에게는 그렇더라도 기계가 읽어야 하는 경우에는 구분이 필요하고,
화면 공유한 URL을 OCR로 읽을 때 겪는다고 답했다.[^Jakob]
tangus는 소문자 l의 형태가 마음에 들지 않아
시도하지 않는 글꼴이 많다고 적었다.[^tangus]
Lobste.rs의 x64k는 한쪽 눈이 거의 보이지 않아 대상 독자에 가깝다고 밝히며,
선명하다는 점에 감명받았지만 폭이 너무 넓어 취향은 아니라고 썼다.
평소에는 PragmataPro를 선호한다고 한다.[^x64k]
같은 곳에서 lorddimwit은 중괄호 모양이 자신이 손으로 쓰는 모양과 비슷한
첫 글꼴이라고 했다.[^lorddimwit]
개인 취향이 큰 영역이라서, 구분이 잘 되는지는 직접 써 봐야 알 수 있다.

### 합자와 기호 지원은 선택 사항으로 둔다

합자를 기본으로 켜지 않고 스타일 세트로 분리한 구성은
코드를 읽는 사람이 합자에 거부감을 느끼는 경우를 고려한 것으로 보인다.
V1.5에서 Powerline과 점자, 기호가 늘어난 것은
터미널 환경에서 쓰는 사용자의 요청과 맞닿아 있을 가능성이 있다.
이는 릴리스 노트의 항목에서 유추한 것이며 저장소가 이유를 밝히지는 않는다.

## 비평

### 근거가 설명에 머물러 있다

저장소는 법적 시각 장애를 포함한 패널과 설계 과정을 말하지만
측정 결과나 비교 자료를 싣지 않는다.
글꼴이 개발자의 피로와 오류를 줄인다는 주장은 아직 Intel 쪽 주장이다.
bayesnet은 저시력 사용자를 위한 글꼴로
Atkinson Hyperlegible Mono를 강하게 추천하며
소스 파일이 공개되어 있다고 말했다.[^bayesnet]

### 대안이 많은 영역이라 선택의 이유가 필요하다

rpozarickij는 이 글꼴의 미리보기가 마음에 들었지만
Iosevka를 알게 된 뒤로는 일반적인 폭의 고정폭 글꼴로 돌아갈 수 없다고 썼다.
폭이 좁아 화면 공간 효율이 좋다는 이유다.[^rpozarickij]
sarmadgulzar는 Fira Code보다 나은지 예 아니오로 답해 달라고 물었고,
이에 대한 합의된 답은 스레드에 없었다.[^sarmadgulzar]
글리프 수도 논점이었다.
JdeBP는 개발자용 글꼴이 대체로 목록이 짧고
이 글꼴의 1400개 가량은 수천 개를 갖춘 고정폭 글꼴보다 적다고 지적했다.[^JdeBP]

### 라이선스와 형식 외의 정보가 적다

README는 설치와 설정, 편집 방법을 상세히 쓰지만
Intel이 이 글꼴을 어떻게 유지할지,
릴리스 간격에 어떤 계획이 있는지는 적지 않는다.
V1.4.0에서 V1.5.0까지는 1년 3개월이 걸렸다.

## 인사이트

### 글꼴 선택은 측정보다 눈에 맞는지에 달려 있다

스레드의 반응은 글꼴의 장단점보다 각자의 취향과 환경으로 갈렸다.
폭, 소문자 l의 모양, 합자 여부는 모두 오래 쓰며 익숙해지는 요소다.
README가 적은 설계 과정은 출발점의 신뢰도를 높이지만
개인에게 맞는지는 며칠 설정해 써 보는 수밖에 없다.
Intel이 약속하는 것은 큰 기관이 만든 무료 글꼴이라는 선택지의 추가다.

### 접근성 목표는 글꼴 하나로 닫히지 않는다

저시력 개발자에게는 글꼴 외에도 색 대비, 크기 조절, 에디터 설정이 함께 필요하다.
zerkten은 브라우저에서 다크 모드처럼
저시력을 알리는 설정이 있는지 물었다.[^zerkten]
글꼴은 이 중 한 요소이고,
사용자가 쓰는 환경에서 켜 둘 수 있게 하는 일이 같이 필요하다.

---

[^virtualritz]: <https://news.ycombinator.com/item?id=50653933>

[^dspillett]: <https://news.ycombinator.com/item?id=50654137>

[^kleiba2]: <https://news.ycombinator.com/item?id=50654149>

[^Jakob]: <https://news.ycombinator.com/item?id=50654189>

[^tangus]: <https://news.ycombinator.com/item?id=50654191>

[^bayesnet]: <https://news.ycombinator.com/item?id=50656649>

[^rpozarickij]: <https://news.ycombinator.com/item?id=50654057>

[^sarmadgulzar]: <https://news.ycombinator.com/item?id=50654758>

[^JdeBP]: <https://news.ycombinator.com/item?id=50655506>

[^zerkten]: <https://news.ycombinator.com/item?id=50657080>

[^x64k]: <https://lobste.rs/s/maihrd/intel_one_mono_font_aiming_for_clarity_low#c_isdt16>

[^lorddimwit]: <https://lobste.rs/s/maihrd/intel_one_mono_font_aiming_for_clarity_low#c_1ldotp>
