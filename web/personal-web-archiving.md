# 좋아하는 웹사이트는 기다리지 말고 WARC로 직접 보관해야 한다

원문: [If you love a website, back it up](https://blog.mistys-internet.website/post/2026/10/29/if-you-love-a-website-back-it-up/)

HN 토론: <https://news.ycombinator.com/item?id=50336518> (551점, 124개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/6ole9g/if_you_love_website_back_it_up> (95점, 35개 댓글)

## 요약

웹 아카이빙 일을 하는 Misty De Meo가 2026-10-29에 블로그 The Future Is Now에 쓴
글이다.
글은 작은 비극에서 시작한다.
글쓴이는 몇 년, 몇십 년째 그대로인 오래된 웹페이지를 가끔 다시 보러 가는데,
Ochaken이라는 애니메이션과 완구 시리즈의 팬 사이트 teapuppies.com이 사라지고
도메인이 온라인 도박 광고에 쓰이고 있었다.
2004년부터 있었고 2005년 이후 거의 바뀌지 않은 사이트였다.
웹 아카이빙을 업으로 하면서도 도구가 있는데 보관하지 않았다는 반성에서
독자에게 직접 보관하라고 권하고 방법을 가르치려는 글이다.

글쓴이가 바로잡으려는 통념은 웹 아카이빙이 Internet Archive 같은 큰 조직만 하는
일이라는 것이다.
누구나 행동할 수 있고 해야 한다는 것이 글의 요지이다.
사용하는 도구는 모두 WARC 같은 표준 웹 아카이브 형식을 쓰고,
대부분 WACZ(WARC 파일과 추가 메타데이터를 묶은 형식)도 쓴다고 한다.
각주는 WARC가 요청과 응답의 헤더까지 완전히 기록하므로
클라이언트 JavaScript가 많은 요청을 하는 복잡한 사이트도 보관할 수 있다고
설명한다.
글쓴이는 이 글에서 언급하는 도구가 자신이 일하는 회사가 만든 것이라고
공개하면서,
급여 때문이 아니라 개인 웹 아카이빙에 가장 좋은 도구라고 생각해서라고 쓴다.

도구는 세 가지다.
첫째는 Chrome용 ArchiveWeb.page 브라우저 확장이다.
설치하고, 보관할 첫 페이지에서 Start Archiving을 누르고, 상호작용 요소를 눌러
데이터가 로드되게 한 뒤
같은 모음에 넣을 페이지를 더 방문하고 Stop Archiving을 누르면 끝난다.
둘째는 브라우저를 내장한 독립 앱 archiveweb.page이다.
확장을 설치하기 싫거나 Chrome이 없을 때 쓰고, 보관한 것을 로컬에서 보는
용도로도 좋다.
셋째는 웹 크롤러 Browsertrix로, 손으로 방문하기 번거로운 큰 사이트에 알맞다.
글의 임베드된 사이트는 도메인 전체 크롤을 기본 설정에 가깝게 돌려 만들었고,
`/episodes/` 같은 일부 경로나 한 페이지와 그 링크로 범위를 좁힐 수도 있다.
Browsertrix는 이 글의 도구 중 유일한 유료이고 7일 체험 뒤 사용량에 따라
과금되지만,
오픈 소스라서 직접 돌릴 수도 있다고 한다.

보관한 것은 자기 브라우저에서 실제 웹페이지처럼 재생할 수 있고, 개인용 Wayback
Machine과 비슷하다.
남과 공유하려면 WARC나 WACZ 파일을 보내 ArchiveWeb.page 앱이나 ReplayWeb.page
사이트에서 열게 하거나,
오픈 소스인 ReplayWeb.page 임베드 뷰어로 자기 사이트에 올릴 수 있다.
모든 것이 WACZ 파일 하나에 들어 있어 보관과 공유가 쉽고, 사본이 많을수록
안전하므로 친구와 나누라고 권한다.
글쓴이는 사람들과 커뮤니티가 소중한 것을 스스로 보관하고 나누는 작은 웹
아카이브가 수없이 생기기를 바란다고 맺는다.

## 분석

### 글의 중심 주장은 보관을 기관에 맡기지 말고 개인이 하라는 것이다

이 주장을 가장 강하게 말하면 이렇다.
웹페이지는 언제든 사라지고, 기관의 보관은 대상을 고를 수 없으며 지금 필요한 것이
들어 있는지 알 수 없으므로,
나에게 중요한 것은 내가 직접 표준 형식으로 보관하고 사본을 나눠 두어야 한다.
글의 근거는 글쓴이 자신의 사례(teapuppies.com)와 도구가 비전문가도 쓸 만큼
쉽다는 점이다.

### 선택한 도구는 JavaScript가 있는 현대 웹을 전제로 한다

글이 소개한 도구는 브라우저에서 사용자가 보는 것을 그대로 기록하거나(확장과 앱),
브라우저를 자동화한 크롤러(Browsertrix)를 쓴다.
글쓴이는 Lobste.rs에서 wget이 클라이언트 JavaScript를 실행하지 못하므로
단일 페이지 앱이나 JavaScript로 링크를 만드는 사이트를 처리하지 못한다고
답한다.[^misty-wget]
그래서 이 글의 도구 선택 기준은 사용 편의와 함께 동적 사이트를 보관할 수
있는지이다.

### 스레드는 같은 목적에 맞는 대안 도구를 쏟아냈다

HN의 drpfenderson은 한 번에 저장할 때는 SingleFile이, 더 큰 작업에는 ArchiveBox가 낫다고 쓴다.[^drpfenderson]
Lobste.rs의 siddhartha_golu는 Zotero의 웹 확장이 SingleFile로 페이지의 진짜 사본을 저장한다고 하고,
reverendpaco는 Zotero에 웹사이트 약 100개를 넣어 두었고 태그와 주석을 붙일 수
있어 개인용 불변의 Memex가 되었다고 한다.[^siddhartha_golu][^reverendpaco]
gavinmorrow는 마음에 드는 페이지를 Internet Archive에 올리는 습관이 있다고 하고,
mro는 크론 작업으로 Archive.org에 밀어 넣는다고 한다.[^gavinmorrow][^mro]
이 목록은 글이 다루지 않은 선택지(SingleFile, Zotero, ArchiveBox, Karakeep,
monolith, HTTrack, wget)가
독자들 사이에서 이미 널리 쓰인다는 것을 보여 준다.

## 비평

### 글쓴이의 이해관계가 도구 선택과 겹친다

글쓴이는 글에 소개한 도구가 자신이 일하는 회사의 것이라고 밝혔고,
대부분 무료이며 가장 좋다고 생각해서 골랐다고 설명한다.
공개한 점은 좋지만, 같은 목적의 다른 도구(wget, SingleFile 등)에 대한 비교는
글에 없다.
Lobste.rs의 xx는 가장 많은 사람이 이미 가진 도구인 GNU wget으로 WARC를 만드는 명령을 소개하고,
일부 배포판이 쓰는 wget2는 WARC 지원이 없다고 지적한다.[^xx]
글쓴이는 CLI에 익숙한 사람이 아니라 덜 기술적인 독자를 겨냥했고 wget은
JavaScript를 실행하지 못한다고 답한다.[^misty-reply]
이 답은 도구를 고른 이유를 설명하지만 비교는 글 안에 없다.

### 도구가 막히거나 낡을 수 있다는 점을 다루지 않는다

HN의 szszrk는 몇 년 동안 ArchiveBox를 썼는데 요즘은 스캔에 실패한 페이지가 쌓이고
새 항목이 나온 지 여러 버전이 지났다고 쓴다.
복잡한 SPA 페이지는 어차피 잘 보관되지 않으므로 페이지가 아니라 내용에 집중하는
웹 클리퍼가 나을지 고민한다.[^szszrk]
whartung은 AI 봇을 막으려는 완화 장치가 사이트 보관에도 걸림돌이 되지 않느냐고
묻는다.[^whartung]
이에 qlte는 SingleFile 확장이나 Karakeep처럼 클라이언트에서 긁는 방식이
브라우저 화면에 보이는 것이면 SPA, JavaScript 렌더링, CAPTCHA가 있어도 잘 된다고
답한다.[^qlte]
글은 이 문제를 다루지 않으며, 이 문서도 어느 쪽이 더 안정적인지 직접 시험하지
못했다.

### 보관한 뒤의 장기 관리는 사본을 나누라는 말에 그친다

글은 WACZ 파일 하나로 보관과 공유가 쉽다고 하지만, 파일을 어디에 얼마나 오래
둘지는 쓰지 않는다.
HN의 y1n0는 2001년에 CD에 구운 아카이브를 가진 VikingCoder에게 CD에도 수명 한계와 비트 부패가 있다고 지적한다.[^y1n0]
Lobste.rs의 frontsideair는 개인 백업과 Internet Archive 같은 중앙 보관 사이의 중간이 비어 있다고 쓰고,
jaculabilis는 IPFS처럼 해시로 주소를 지정하는 방식이 그에 가깝지만 원래 주소가
사라지면 내용은 잃을 수 있다고 답한다.[^frontsideair][^jaculabilis]
글은 이 중간 지대를 다루지 않는다.

## 인사이트

### 보관 도구는 목적에 따라 가볍게 나눠 쓰는 것이 현실적이다

스레드가 보여 주는 도구 선택은 서로 겹치지 않는 용도로 나뉜다.
한 페이지를 바로 저장하는 일은 SingleFile이나 Firefox의 저장 기능,
읽은 것을 모아 두는 일은 Zotero, Karakeep, ArchiveBox,
도메인 전체를 복사하는 일은 Browsertrix나 HTTrack, wget이다.
JulianSildenLanglo는 Firefox의 Ctrl+S만으로도 이미지와 CSS가 폴더에 함께
저장되어 인터넷 없이 같은 페이지가 열렸다고 하고,
Lobste.rs 자체는 CSS가 어긋나 흰 화면으로 렌더링되었다고 쓴다.[^JulianSildenLanglo]
이 문서의 제안은 보관하려는 대상이 한 페이지인지, 읽은 글의 모음인지, 사이트
전체인지를 먼저 정하고 그에 맞는 도구 하나를 고르는 것이다.

### 사라지는 것은 사이트만이 아니다

HN의 annzabelle은 AO3(Archive of Our Own)가 보안 사고로 몇 주째 내려가 있다는 사례를 든다.
AO3는 팬 창작물의 포괄적 아카이브이고 이미 사라진 여러 팬픽션 사이트의 자료를
담고 있었는데,
운영 단체가 이것을 영원히 유지하리라 생각했다고 쓴다.[^annzabelle]
ysleepy는 “백업은 만들어졌다”고 답한다.[^ysleepy]
보관을 운영 주체의 약속에 맡기지 말라는 글의 주장에 대한 근거로 읽을 수 있지만,
이 문서는 AO3 사고를 확인하지 못했고 댓글의 서술로만 전한다.

### 이 글의 처방을 확인하는 방법

내가 다시 보고 싶은 사이트 하나를 골라 ArchiveWeb.page나 Browsertrix로
보관한 뒤,
인터넷을 끊은 상태에서 ReplayWeb.page로 링크와 이미지가 모두 열리는지 확인한다.
열리지 않는 부분이 있다면 그 사이트에서는 다른 도구(SingleFile, HTTrack)를
시험할 이유가 된다.

---

[^misty-wget]: <https://lobste.rs/s/6ole9g/if_you_love_website_back_it_up#c_xc0rub>

[^drpfenderson]: <https://news.ycombinator.com/item?id=50338928>

[^siddhartha_golu]: <https://lobste.rs/s/6ole9g/if_you_love_website_back_it_up#c_ad0qte>

[^reverendpaco]: <https://lobste.rs/s/6ole9g/if_you_love_website_back_it_up#c_qqngbs>

[^gavinmorrow]: <https://lobste.rs/s/6ole9g/if_you_love_website_back_it_up#c_lscjag>

[^mro]: <https://lobste.rs/s/6ole9g/if_you_love_website_back_it_up#c_vk87oe>

[^xx]: <https://lobste.rs/s/6ole9g/if_you_love_website_back_it_up#c_nk7iet>

[^misty-reply]: <https://lobste.rs/s/6ole9g/if_you_love_website_back_it_up#c_javie5>

[^szszrk]: <https://news.ycombinator.com/item?id=50339131>

[^whartung]: <https://news.ycombinator.com/item?id=50342180>

[^qlte]: <https://news.ycombinator.com/item?id=50348812>

[^y1n0]: <https://news.ycombinator.com/item?id=50346147>

[^frontsideair]: <https://lobste.rs/s/6ole9g/if_you_love_website_back_it_up#c_cruwbr>

[^jaculabilis]: <https://lobste.rs/s/6ole9g/if_you_love_website_back_it_up#c_rig9sh>

[^JulianSildenLanglo]: <https://lobste.rs/s/6ole9g/if_you_love_website_back_it_up#c_ftuoiu>

[^annzabelle]: <https://news.ycombinator.com/item?id=50344531>

[^ysleepy]: <https://news.ycombinator.com/item?id=50346008>
