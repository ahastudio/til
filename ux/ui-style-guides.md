# UI 스타일 가이드 모음

원문: [UI style guides](https://aresluna.org/ui-style-guides/)

HN 토론: <https://news.ycombinator.com/item?id=50649834> (443점, 107개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/pbfhis/ui_style_guides> (52점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=37889>

## 요약

1980년대 초부터 현재까지 여러 회사가 낸 UI 스타일 가이드(인터페이스 지침)를
한곳에 모은 목록 페이지다.
글쓴이는 PDF가 이미 여기저기 떠돌았지만 한곳에 모았다고 말한다.
같은 묶음 안에서는 주제와 시대로 나누고 중요한 것을 눈에 띄게 했다고 한다.
찾기 어려운 것은 노력이 필요했고 일부는 직접 스캔했으며,
소규모 사이트는 독립된 복제본(mirror)으로 만들었다고 설명한다.
복제본은 이미지를 더 보기 좋게 픽셀화하고 링크 대신 이미지를 안에 넣고
유튜브 삽입을 고치는 식으로 가볍게 손봤다고 한다.

목록은 운영체제와 제품군 이름 순으로 늘어서 있다.
페이지에서 읽은 항목은 다음과 같이 묶을 수 있다.

| 묶음              | 항목의 예                                                      |
| ----------------- | -------------------------------------------------------------- |
| 데스크톱 초기     | Amiga(1991), Apple Lisa와 Macintosh(1980년대~), NeXTSTEP, CUA  |
| 유닉스 계열       | OPEN LOOK, OSF/Motif와 CDE, SGI, GNOME, KDE                    |
| 휴대 기기         | iOS, Android, BlackBerry, Nokia, Palm OS, webOS, Windows Phone |
| 실패하거나 사라진 | Newton, PenPoint, Magic Cap, Taligent                          |
| 기타              | Java Look and Feel, Microsoft Office, Kinect, Google VR/AR     |

일부 항목에는 현재 공개된 웹사이트나 Wayback Machine, Internet Archive의 뷰어도
달려 있다.
끝에는 모든 가이드를 한 번에 받는 압축 파일이 있고
다른 수집가 다섯 명(Chris Silverman, Geof Crowl, Matt Sephton,
Přemysl Eric Janouch, Matthias Rauterberg)의 모음에 감사하며
빠진 가이드를 알려 달라고 청한다.

## 분석

### 흩어진 문서를 한곳에 모은 일의 가치

이 페이지의 쓸모는 새로운 주장이 아니라 접근성이다.
오래된 PDF와 사라진 사이트는 찾는 것부터 일이다.
한 곳에 모으고 복제본을 만들어 두면 원본 링크가 죽어도 읽을 수 있다.
저자가 주제와 시대로 묶은 구성 덕분에 같은 회사의 가이드가
어떻게 바뀌었는지(예: Mac의 1987년판에서 Aqua, 현재)를 한눈에 볼 수 있다.

### 시대에 따라 문서의 성격이 바뀐다

초기 가이드는 일관성을 위한 규칙집이고,
모바일 시대 이후는 플랫폼의 디자인 철학을 설명하는 문서에 가깝다.
다만 페이지가 BeOS 항목을 두고 정식 가이드는 나오지 않았고
CD에서 추출한 미완성 지침이라고 설명하는 것처럼,
모든 가이드가 같은 지위의 문서는 아님을 알 수 있다.

### 목록이 담지 않는 것

웹용 지침은 이 목록에 없고 모음이 플랫폼 중심이라는 점이 드러난다.
HN의 mcculley는 웹 앱이 데스크톱 앱을 대체한다는 말을 오래 들었지만
웹에는 아직 지침이 없다고 썼고,[^mcculley]
cowlevel은 그래서 웹이 장악했지만 마음대로 디자인할 수 있어 대부분 나쁘다고
답했다.[^cowlevel-web]
IBM의 Carbon 디자인 언어를 더해 달라는 제안도 있었고,[^lilchungus]
다른 답글은 그런 디자인 시스템은 component.gallery에 이미 있다고
가리켰다.[^culi]

## 비평

### 목록의 정확성에 대한 지적

HN의 agileAlligator는 자신의 AI에게 목록을 보여 주었더니
Symbian Belle 항목의 링크가 바로 위 Symbian3 항목과 같은 것을 가리키고,
webOS 항목의 연도 표기가 1999년으로 되어 있어 본문 설명과 모순된다고 알려
주었다고 썼다.[^agileAlligator]
이에 asdfsa32는 AI로 만든 것을 AI로 고칠 수 있는 정도라며 정확성에 대한 관심이
부족하다고 아쉬워했고,[^asdfsa32]
g-b-r은 과거를 돌아보는 자료가 부주의하게 만들어졌다는 점이 슬프다고
했다.[^g-b-r]

### 누락 항목에 대한 지적

estebank가 현재 가이드의 주소를 알려 준 것은 별개의 사실이다.[^estebank]
페이지의 KDE 항목은 2021년 복제본 하나뿐이라서,
bnh가 말한 KDE2 시절 스타일 가이드는 목록에 없는 것이 맞다.[^bnh]
빠진 것을 알려 달라는 저자의 요청이 열려 있는 모음이라는 점이 드러난다.

### 목록은 각 문서의 품질을 평가하지 않는다

이 페이지는 중요한 것을 강조했다고 하지만 어떤 기준인지는 밝히지 않는다.
문서를 보존하는 일과 어떤 지침이 좋은지 판단하는 일은 다르다.
각 가이드의 설계 철학을 비교하려면 읽는 사람이 직접 읽어야 한다.

## 인사이트

### 옛 가이드를 읽는 이유는 향수만이 아니다

HN의 pndy는 회색과 은색 화면에서 눌러야 하는 것과 정적인 글자가 쉽게
구분되었는데
이 구분이 어디서 사라졌느냐고 물었다.[^pndy]
g-b-r은 스마트폰과 함께 유행하는 디자이너들이 그것을 낡았다고 여겼다고
했고,[^g-b-r-trendy]
cowlevel은 전환점이 반응형 디자인이었다고 보았다.
이전에는 화면의 픽셀 수를 정해서 디자이너의 화면과 같게 보였는데
이후에는 모든 것이 겹쳐 쌓인 배치 관리자로 만들어져야 했다는 것이다.[^cowlevel]

### 지침 속의 문장이 시대를 보여 준다

krstffr은 1991년 Amiga 스타일 가이드의 첫 쪽에서
영어에 성 중립적 3인칭 대명사가 없으므로 장마다 성별을 무작위로 바꾸었고
놀랐다면 놀랄 필요가 있었던 것이라고 쓴 문장을 소개했다.[^krstffr]
GeekNews에서 xguru는 NextStep 문서를 오랜만에 보니 추억이 돋지만
아이콘 스타일은 아직도 BeOS가 가장 마음에 든다고 썼다.[^xguru]
지침은 규칙이면서 그 시대가 사용자를 어떻게 상정했는지의 기록이기도 하다.

---

[^mcculley]: <https://news.ycombinator.com/item?id=50654024>

[^cowlevel-web]: <https://news.ycombinator.com/item?id=50655259>

[^lilchungus]: <https://news.ycombinator.com/item?id=50652398>

[^culi]: <https://news.ycombinator.com/item?id=50663203>

[^agileAlligator]: <https://news.ycombinator.com/item?id=50652583>

[^asdfsa32]: <https://news.ycombinator.com/item?id=50652641>

[^g-b-r]: <https://news.ycombinator.com/item?id=50654647>

[^estebank]: <https://news.ycombinator.com/item?id=50656302>

[^bnh]: <https://news.ycombinator.com/item?id=50653695>

[^pndy]: <https://news.ycombinator.com/item?id=50654576>

[^g-b-r-trendy]: <https://news.ycombinator.com/item?id=50654587>

[^cowlevel]: <https://news.ycombinator.com/item?id=50655245>

[^krstffr]: <https://news.ycombinator.com/item?id=50653169>

[^xguru]: <https://news.hada.io/topic?id=37889#cid70657>
