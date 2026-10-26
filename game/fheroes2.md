# fheroes2: Heroes of Might and Magic II 엔진을 처음부터 다시 만든 오픈소스 프로젝트

<https://github.com/ihhub/fheroes2>

HN 토론: <https://news.ycombinator.com/item?id=50230384> (147점, 50개 댓글)

GN 토론: <https://news.hada.io/topic?id=35979>

## 소개

fheroes2는 Heroes of Might and Magic II(HoMM2) 게임 엔진을 다시 만든 오픈소스
프로젝트다.
여러 플랫폼에서 돌아가고, 처음부터 새로 썼다고 한다.
README의 목표는 원작을 재현하면서 게임플레이와 그래픽, 로직을 크게 개선하는
것이다.
고해상도 그래픽 지원과 개선된 AI, 여러 버그 수정, 사용자 인터페이스 개선이 그
내용이다.

라이선스는 GNU General Public License v2.0이고, 처음에는 SourceForge에서
개발됐다.
원작 게임과 리소스의 권리는 옛 The 3DO Company에 있었고 Ubisoft로 넘어갔다.
프로젝트는 불법 사용을 권장하지 않으며, GOG나 Ubisoft Store에서 원작을 사라고
안내한다.
후원은 Patreon, PayPal, Boosty로 받고, 전부 앞으로의 개발에만 쓴다고 밝힌다.
그래픽 제작, 번역, 문서 사이트 개발에도 참여할 수 있고, 소통 창구는 Facebook,
VK, Discord다.

## 설치와 원본 게임 파일

플레이하려면 Heroes of Might and Magic II의 데모 버전이나 정식 버전이
필요하다.[^install]
영어로만 제공되는 무료 데모는 포함된 스크립트로 내려받을 수 있다.[^install]
미리 빌드된 바이너리는 Windows, macOS, Linux, Android, PlayStation Vita,
Nintendo Switch용이 있다.[^install]

Windows 설치 프로그램은 설치 중에 원본 게임에서 리소스를 추출할지, 데모를
내려받아 추출할지 묻는다.[^install]
수동으로 할 때는 원본 게임 폴더의 `ANIM`, `DATA`, `MAPS`, `MUSIC` 하위 폴더를
설치 폴더로 복사한다.[^install]
즉 이 프로젝트가 재구현한 것은 엔진이고, 그래픽과 음악 같은 원작 자산은 사용자가
따로 마련해야 한다.

## 주요 개선 사항

개선 목록 문서는 원작과 비교한 기능과 개선을 모은 것이며, 모든 세부를 다루지는
않고 바뀔 수 있다고 스스로 밝힌다.[^improvements]
읽은 범위의 항목은 대부분 인터페이스와 편의 기능이다.

전투에서는 수동 전투를 즉시 끝내거나 다시 시작하는 기능, 즉시 전투 옵션, 크리처
정보 창의 특성과 주문 지속 시간 표시, 큰 크리처가 차지하는 두 칸 강조가
있다.[^improvements]
자동 전투는 `Q` 키로 바로 끝낼 수 있다.[^improvements]
성에서는 우물(Well)에서 바로 병력을 모집할 수 있다.[^improvements]
원작에서는 성 화면에서 건물을 하나씩 눌러야만 모집할 수 있었다.[^improvements]
모험 지도에서는 날짜 카운터가 원작의 4일 제한을 넘어 확장됐다.[^improvements]

그 밖에 해상도 선택, 새 설정 창, 단축키 목록과 재배정, 여러 언어, 캠페인 난이도
선택, 전투만 하는 모드가 있다.[^improvements]
여러 언어를 고를 수 있지만, 글자나 음성이 들어 있는 원본 자산은 처음 언어 그대로
남는다.[^improvements]
Knight 성의 농장(Farm) 일부와 Barbarian 성의 Captain's Quarters 일부처럼
원작에서 빠졌던 그림을
채운 수정도 있다.[^improvements]

## 비평

### 재현과 개선을 함께 내세우면 기준이 두 개가 된다

README는 원작을 재현하는 일과 크게 개선하는 일을 한 문장에 둔다.
둘은 서로 다른 기준이다.
재현의 기준은 원작과 같은 결과를 내는지이고, 개선의 기준은 원작보다 나은지다.
README는 어느 쪽이 충돌할 때 이기는지를 말하지 않는다.

HN의 loglog는 추가된 기능이 Heroes of Might and Magic III(HoMM3)의 포괄적인
역이식처럼 보인다고
했다.[^loglog]
nylonstrung은 다른 오픈소스 재구현과 무엇이 다른지 알려 주면 좋겠다고
했고,[^nylonstrung] gum_wobble은 이런 일은 쓸모나 문제 해결을 위해서가 아니라
취미와 헌정에 가깝고 모든 것에 목적이 있어야 하는 것은 아니라고
답했다.[^gum_wobble]
이 답은 프로젝트가 무엇을 목표로 하는지를 묻는 질문을 비껴간다.
다만 취미 프로젝트라는 설명이 맞다면, 기준이 둘이라는 점은 흠이 아니라 선택의
자유로 읽힌다.

### 엔진은 새로 만들었어도 플레이는 원작 구매에 기댄다

설치 문서가 요구하는 원본 게임이나 데모 파일은 이 프로젝트의 한계를 정한다.
엔진이 열려 있어도 자산은 Ubisoft가 쥐고 있다.
따라서 이 프로젝트가 살아 있는 동안에도 원작이 판매되거나 데모가 접근 가능해야
한다.

데모가 영어로만 제공된다는 점도 영향을 준다.
개선 문서의 언어 선택 기능은 글자와 음성이 담긴 자산은 바꾸지 못한다고
한다.[^improvements]
그래서 데모로 시작하는 사용자에게는 다국어 지원이 인터페이스 쪽에 한정된다.
문서가 두 사실을 따로 적어서 연결해 읽는 것은 독자의 몫이다.

### 어른이 된 눈으로 다시 하면 옛 게임이 달라 보인다

fullstackwife는 옛 게임을 다시 만들 때마다 어릴 때 즐겁던 게임성이 어른이 되면
견디기 어렵다는 것을 알게 되고, HoMM이 그런 게임이라고 했다.[^fullstackwife]
이것은 재구현 프로젝트가 감당해야 하는 문제다.
편의 기능을 얼마나 넣어도 게임의 속도와 구조는 그대로이기 때문이다.

반대로 suboto는 HoMM이 나왔을 때부터 틈새였고, 장르가 작은 만큼 충성도가
구조적으로 높다고 했다.[^suboto]
vunderba는 HoMM2의 그래픽 분위기에 HoMM3의 게임 규칙을 합친 새 게임을
바랐다.[^vunderba]
원작의 매력이 그래픽 분위기에 있는지 규칙에 있는지가 사람마다 다르다는 뜻이고,
개선 항목의 가치도 그에 따라 달라진다.

## 인사이트

### 재구현은 원작의 숨은 규칙을 드러낸다

tholman은 개선 내용 중 컴퓨터 플레이어의 AI 변화를 읽는 것이 재미있었다고
썼다.[^tholman]
원작에서는 컴퓨터 플레이어가 지도 전체를 보고 크리처 증가에서 추가 이득을
받았고, 지금은 더 현대적이고 나은 전술을 쓴다는 것이다.[^tholman]
smolder는 속임수를 쓰는 AI가 한때는 표준이었고 이제는 오히려 발목을 잡아야
한다고 짚었다.[^smolder]
이 문서는 AI 변화를 다룬 페이지를 읽지 못했으므로, 위 내용은 댓글에 근거한
것이다.

그래도 방향은 분명하다.
엔진을 처음부터 쓰는 사람은 원작이 암묵적으로 하던 일을 코드로 직접 정해야 한다.
그 과정에서 반칙이 드러나고, 재현할지 고칠지 선택하게 된다.

### 어느 Heroes를 원하는지에 따라 선택이 갈린다

HN에는 HoMM3 쪽 선택지도 여럿 올라왔다.
cyrusmg는 HoMM3용 엔진 VCMI를 소개했고,[^cyrusmg] vrganj도 같은 프로젝트를
언급했다.[^vrganj]
quibono는 HoMM3용 HotA를 소개했고,[^quibono]
Kuxe는 VCMI가 Android에서도 되고 모드 지원과 새 진영이 있다고 했다.[^Kuxe]
따라서 결정 규칙은 단순하다.
HoMM2의 그래픽과 규칙을 원하고 원본 파일을 구할 수 있으면 fheroes2를, HoMM3를
원하면 VCMI나 HotA를 본다.

### 이 글을 읽는 방법

README와 개선 문서는 프로젝트가 스스로 쓴 소개이므로, 기능 목록은 확인 가능한
사실이고 원작 재현도나 AI 품질은 아직 확인되지 않은 주장이다.
개선 문서도 모든 세부를 다루지 않는다고 스스로 적었다.
HN 댓글의 AI 설명도 이 문서가 직접 확인한 것이 아니다.

이 판단을 가를 관찰은 두 가지다.
첫째, 같은 지도에서 같은 선택을 해 원작과 fheroes2의 전투 피해량과 주간 수입을
비교하는 것이다.
둘째, 컴퓨터 플레이어가 안개에 가려진 지도 정보나 크리처 증가 보너스를 쓰는지
소스 코드나 로그로 확인하는 것이다.
첫째는 재현이 얼마나 정확한지를, 둘째는 개선된 AI라는 설명이 원작의 속임수를
없앤다는 뜻인지를 가른다.

---

[^install]: GitHub ihhub/fheroes2, [fheroes2 Installation Guide](https://github.com/ihhub/fheroes2/blob/master/docs/INSTALL.md)

[^improvements]: GitHub ihhub/fheroes2, [Features and enhancements of the project](https://github.com/ihhub/fheroes2/blob/master/docs/GAME_IMPROVEMENTS.md)

[^loglog]: <https://news.ycombinator.com/item?id=50230801>

[^nylonstrung]: <https://news.ycombinator.com/item?id=50231322>

[^gum_wobble]: <https://news.ycombinator.com/item?id=50231358>

[^fullstackwife]: <https://news.ycombinator.com/item?id=50233702>

[^suboto]: <https://news.ycombinator.com/item?id=50232333>

[^vunderba]: <https://news.ycombinator.com/item?id=50232263>

[^tholman]: <https://news.ycombinator.com/item?id=50231195>

[^smolder]: <https://news.ycombinator.com/item?id=50232200>

[^cyrusmg]: <https://news.ycombinator.com/item?id=50230757>

[^vrganj]: <https://news.ycombinator.com/item?id=50231262>

[^quibono]: <https://news.ycombinator.com/item?id=50230797>

[^Kuxe]: <https://news.ycombinator.com/item?id=50231076>
