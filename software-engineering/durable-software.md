# Zotero 20년, 오래가는 소프트웨어는 천천히 만들어진다

원문: [The Slow Formation of Durable Software](https://newsletter.dancohen.org/archive/the-slow-formation-of-durable-software/)

HN 토론: <https://news.ycombinator.com/item?id=49980346> (290점, 115개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/8mm3ec/slow_formation_durable_software> (1점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=35022>

## 요약

Dan Cohen이 자신의 뉴스레터 Humane Ingenuity에 2026년 10월 6일 올린 글이다.
연구 자료를 수집, 정리, 주석, 인용, 공유하는 무료 도구 Zotero가 2006년 10월 5일
공개된 지 20주년을 맞아, 그 1.0 이전의 역사를 돌아본다.
Cohen은 당시 George Mason University의 Center for History and New Media에서
역사학 조교수이자 연구 책임자였다.
이 연구소의 지금 이름은 설립자를 기려 붙인
Roy Rosenzweig Center for History and New Media(RRCHNM)다.
1994년 웹이 몇 해 되지 않았을 때 세워진 이 센터는 원래 소프트웨어가 아니라
웹사이트를 만드는 곳이었다.
Cohen은 자신이 지금 이끄는 도서관도 대부분의 연구도서관처럼 학생과 교수에게
Zotero 쓰는 법을 가르치는 워크숍을 연다고 쓰지만, 그 도서관의 이름은 원문에
나오지 않는다.
Cohen의 개인 사이트에 따르면 그는 지금 Northeastern University의 도서관장(Dean
of the Library)이자 정보 협력 담당 부총장, 역사학 교수다.

Cohen은 성공에는 부모가 많다며 이 글이 자기 관점에서 쓴 제한된 기록이라고
먼저 밝힌다.
전체 기여자는 Zotero의 Credits and Acknowledgments 페이지에서 보라고 권하고,
출시 이후 20년의 성장은 Sean Takats의 별도 글 “Zotero at Twenty”로 넘긴다.
올봄 자녀의 대학 졸업식에서 Zotero에 관여했다는 말을 들은 한 참석자가 갑자기
오래 안아 주었는데, 자기 학술 저술로는 그런 일이 없었고 앞으로도 없을 것이라는
일화도 덧붙인다.

글은 AI로 소프트웨어를 거의 즉시 만들 수 있게 된 지금과 대비하며 시작한다.
Robin Sloan의 표현대로 원하는 것을 요청하기만 하면 되는 시대지만,
수십 개 언어로 2,000만 명 넘게 쓰는 Zotero는 그 반대였다.
거친 첫 시제품까지 5분이 아니라 5년이 걸렸고,
다듬고 넓히는 데 다시 수년이 걸렸다.
Cohen은 2000년대 초에 AI가 있었더라도 구상을 앞당기지 못했을 것이라고 말한다.
무엇을 원하는지 정확히 몰랐으니 LLM에 일관된 프롬프트를 쓸 수도 없었다는 것이다.
그 느린 형성 덕분에 일회성이 아니라 오래가는 소프트웨어가 나왔고,
프로그래밍이 마법 같은 봇과 함께하는 카페인 폭주가 되어 가는 지금 여기에 교훈이
있다는 것이 글의 주장이다.

### 두 개의 불완전한 전신

Cohen은 2001년 1월 갓 박사 학위를 받고 RRCHNM에 합류해,
기술사를 공부한 Jim Sparrow(지금은 University of Chicago 역사학 교수)와 함께
Alfred P. Sloan Foundation이 지원한 과학사 웹사이트
ECHO(Exploring and Collecting History Online)를 만들었다.
과학은 기하급수로 커지는데 과학사 연구자 수는 그대로라는 문제의식이
출발점이었다.
과학자가 스스로 작업을 기록하게 하려고 자료를 올리고 분류하고 보관하는 작은 웹
앱을 PHP로 여럿 썼고, 그중 Web Scrapbook이 수업에서 쓰였다.
자바스크립트가 들어간 북마크를 눌러 브라우저에서 이미지와 링크를 모아 공유하는
도구였지만, 첫 버전은 비밀번호를 암호화하지 않고 보냈고 각주에 필요한 서지
정보도 제대로 다루지 못했다.
같은 시기 센터의 웹마스터로 일하며 박사 과정을 밟던 Elena Razlogova(지금은
Concordia University 역사학 교수)는 FileMaker로 메모와 인용을 관리하는 데스크톱
앱 Scribe를 만들었다.
Mac과 PC에서 로컬로 돌았고, 정리, 검색, 메타데이터, 주석 기능을 갖춰 EndNote의
무료 대안으로 역사학자들 사이에 퍼졌다.

2003년 무렵 팀은 웹 앱과 데스크톱 앱을 모두 만들 줄 알았지만 둘 다 부족하다고
느꼈다.
연구가 웹에서 시작되는데, Scribe는 웹을 몰랐고 Web Scrapbook은 학술 도구가
아니었다.
2003년 11월 29일 Roy Rosenzweig가 Scribe 다음 버전에서 하고 싶은 일을 물었다.
Rosenzweig, Cohen, 그리고 September 11 Digital Archive 일로 합류한 Tom
Scheinfeldt(지금은 University of Connecticut 디지털 인문학 교수)가 ECHO 다음
단계 지원금 신청서를 쓰며 개선된 도구를 넣으려던 참이었다.
Razlogova는 12월 1일 온라인 서지 데이터베이스 연결, APA와 법률 인용 스타일 추가,
사용자 정의 인용 스타일, 온라인 공유와 공동 편집, 로컬 작업 뒤 온라인 게시,
외국어 지원, 더 나은 설명서 같은 목록을 보냈다.
Scheinfeldt는 Scribe를 “webify”하자고 답했다.
Cohen은 훗날 First Monday 논문에서 이 목표를
독립 애플리케이션과 웹 애플리케이션의 장점을 모두 갖는 것이라고 정리했다.
브라우저 안에 살면서 학술 메타데이터를 알아보고 워드프로세서와도 연결되는
도구라는 목표는 이때 섰지만, 두 세계를 어떻게 합칠지는 2003년에 전혀 분명하지
않았다.

### Firefox와 XUL이 연 길

RRCHNM에는 진지한 아이디어와 실없는 아이디어가 뒤섞인 커다란 화이트보드가
있었고, 점심마다 새 기술을 역사 연구에 쓸 방법을 이야기했다.
2004년 여름 과학기술학 박사 Josh Greenberg(지금은 Alfred P. Sloan Foundation
프로그램 디렉터), 미국사 박사 Sharon Leon(지금은 Digital Scholar 공동 CEO),
그리고 10대였던 Simon Kornblith가 합류했다.
Kornblith는 Rosenzweig와 친한 역사학자의 아들이었고, 뒤에 MIT에서 뇌인지과학
박사 학위를 받아 Geoffrey Hinton과 중요한 AI 논문을 쓰고 Anthropic에서 일하게
된다.
그해 여름 베타였던 Firefox는 느리고 비대해진 Mozilla 브라우저에서 갈라져 나온
가벼운 브라우저였고, 팀을 더 흥분시킨 것은 브라우저를 마음대로 확장할 수 있게
해 주는 XUL이었다.
Firefox가 정식 출시된 2004년 11월 9일 밤 Cohen은 Greenberg, Razlogova,
Scheinfeldt, Rosenzweig에게
“Firefox + XUL + AWS = OpenScribe/Online Scribe?”라는 제목의 메일을 보냈다.
여기서 AWS는 클라우드가 아니라 Amazon이 제공하던 도서 정보 API였고,
이를 Firefox 확장과 묶어 인용 정보를 필드에 자동으로 채우자는 구상이었다.
Greenberg는 자정 직전 MySQL용 XPCOM 래퍼로 Scribe를 관계형 데이터베이스 위에
재현할 수 있고 곧바로 여러 플랫폼에서 돌아간다며 흥분한 답장을 보냈다.
데이터베이스를 버리고 Scribe의 XML을 Firefox 화면에서 직접 다루는 대안,
Amazon과 Proquest/ISI 인용 색인으로 서지 항목을 만드는 방법,
Cocoa나 스크립트로 워드프로세서 안에서 인용하는 Mac 버전까지 한 메일에 담겼다.

그해 겨울 Rosenzweig를 책임 연구자로, Greenberg와 Cohen을 공동 책임자로 해서
연방 기관인 Institute of Museum and Library Services(IMLS)에 “SmartFox: the
Scholar's Browser for Digital Collections”라는 제목으로 지원금을 신청했다.
초록은 디지털 자료 구축에 수천만 달러가 들었지만 그것을 쓰는 도구에는 훨씬 적은
돈이 들어갔다고 지적했다.
그리고 브라우저를 보기만 하는 수동적인 창에서 자료를 수집, 주석,
정리하는 곳으로 바꾸겠다며, 도서관과 박물관 자료를 알아보고 메타데이터를
자동으로 가져오는 도구와 그것을 저장, 정리하는 도구를 제시했다.
다만 여전히 앱 하나가 아니라 “도구 모음”을 구상하고 있었다.
지원금이 나오기도 전에 Kornblith와 개발자 David Norton이 2005년 7월 27일
“0.0.1” 시제품을 만들었다.
위에 메타데이터 패널, 아래에 메모 칸, 왼쪽에 폴더가 따로 있던 이 화면은 나중에
하나의 서랍(drawer)으로 합쳐졌다.
Kornblith는 Firefox가 데이터베이스 인터페이스 mozStorage를 넣을 계획이라는 것도
짚었고, Firefox는 결국 SQLite를 내장했다.

### 팀이 갖춰지자 빨라진 개발과 이름 찾기

2005년 여름 센터 직원의 친구로 서버 관리를 맡아 들어온 Dan Stillman은 쌓인
문제를 워낙 잘 고쳐 2006년 1월 개발팀에 합류했고, 지금도 Zotero의 수석
개발자다.
프랑스사 박사이자 기술 경험이 많던 Sean Takats는 이후 오랫동안 Zotero의 디렉터를
맡았다.
기술 전도사 역할을 한 Kari Kraus는 University of Maryland 교수가 되었고,
그해 말 홍보 담당으로 합류한 Trevor Owens는 지금 American Institute of Physics의
최고연구책임자다.
팀이 갖춰지자 약 6개월 만에 훨씬 일관된 설계가 나왔고,
강의 부담이 줄어드는 여름에 코드가 빠르게 반복되며 2006년 가을 1.0 출시가
가능해졌다.
이름은 SmartFox에서 2005년 9월 Firefox Scholar로 바뀌었지만,
변호사가 Firefox가 들어간 이름은 문제가 된다고 했다.
팀은 이 소프트웨어가 학자(scholar)만을 위한 것인지도 의문이었다.
Cohen은 2006년 여름 디자인을 다듬은 시간만큼 이름을 고민했을 것이라고 고백한다.
iPod 시절의 iScholar, Flickr 시절의 Scholr, Citopia, FreeCite, CiteHound,
DynoCite, FireScribe, FireHoard, MetaFox, ClioFox 같은 후보가 오갔고,
그럴듯한 이름은 대부분 도메인이 이미 등록되어 있었다.
여름이 끝나 갈 무렵 팀은 아프리카 언어에서 온 Ubuntu, 하와이어 wiki에서 온
Wikipedia처럼 영어 밖으로 눈을 돌렸다.
동유럽사 연구자 Mills Kelly가 미국인이 거의 뒤져 보지 않았을 알바니아어 사전을
권했고, 팀은 “잘 배우다, 숙달하다”라는 뜻의 zotero를 골랐다.
기억하기 쉽고 여러 언어로 발음하기 쉬우며 도메인도 비어 있어 .org, .com,
.net을 모두 등록했다.
2006년 8월 29일 Cohen은 Eurostile 서체로 만든 로고타입을 Photoshop 파일로
Stillman에게 보냈다.
Cohen은 이것이 당시 살던 Maryland주 Silver Spring 근처의 식당
Zpizza의 빨간 Z에서 영감을 받았을 수도 있다고 농담처럼 쓴다.
서체는 조금 바뀌었지만 로고타입은 지금도 쓰인다.

### 출시와 그 뒤

Cohen은 공개 베타를 알리며 블로그에 “try it out!”이라는 한 문장만 올렸고,
1.0 공개 베타는 한 달 만에 사용자 6만 명을 모았다.
글에 실린 2006년 말 팀 사진 설명에는, 항암 치료 중이던 Rosenzweig가 자기 Prius에
달 Zotero 번호판을 막 받아 모두가 즐거워했다는 이야기가 있다.
이후 Mellon Foundation과 Alfred P. Sloan Foundation의 추가 지원으로 연구팀 간
동기화가 생겼고, 결국 Firefox에서 독립해 다른 브라우저와도 함께 쓰이게 되었다.
Rosenzweig는 2007년 57세로 세상을 떠났고,
그 뒤를 이어 센터장이 된 Cohen은 일상적인 Zotero 작업을 Stillman, Takats,
비영리 Corporation for Digital Scholarship, 국제 개발자와 자원봉사자에게 넘겼다.
Zotero 10.0은 2026년 8월 17일에 나왔다.
Cohen은 역사학자들의 집단적 사고에서 천천히 나온 Zotero의 가치가 놀라울 만큼
오래갔다며, 앞으로 20년 이상 이어지기를 바란다는 말로 글을 맺는다.

## 분석

### 글의 핵심 주장은 속도가 아니라 사양의 출처에 대한 것이다

글은 느림을 찬양하는 것처럼 읽히지만, 실제 논증은 더 좁다.
AI가 가속할 수 없었던 것은 코딩이 아니라 무엇을 만들지 아는 일이었다는 주장이다.
Cohen은 프롬프트를 쓸 수 없었다고 말하는데,
이는 사양(specification)이 아직 존재하지 않았다는 뜻이다.
사양이 없으면 생성 도구는 할 일이 없다.

_fw는 사용자 확보와 성장을 맡은 입장에서 이 대목이 가장 와닿았다며,
오늘날 놀랄 만큼 많은 제품이 문제를 찾아 헤매는 해결책이라고 적었다.[^_fw]
사람들이 원하는 것을 만드는 편이, 만든 것을 원하게 만드는 것보다 훨씬 쉽다는
것이다.
rrr_oh_man은 사람들이 시제품을 시장에 내놓기를 꺼린다는 _fw의 답글에,
오히려 빠르게 만들어 내놓았지만 사용자가 한 명도 없는 앱이 수천 개라며
품질보다 붐비는 시장에서의 유통이 문제라고 답했다.[^rrr_oh_man]
gutechh는 _fw의 표현을 뒤집어, 문제는 알지만 해법이 자명하지 않은 상황이야말로 이 글의
학자들이 처한 처지였다고 짚었다.[^gutechh]
역사학자들은 연구 현장의 불편을 누구보다 잘 알았지만,
그 불편을 해소할 도구의 모양은 쉽게 떠올리지 못했다.

이렇게 읽으면 글은 AI 비관론이 아니라 병목의 위치에 대한 주장이다.
코드가 싸질수록 비싼 것은 무엇을 원하는지 아는 일이며,
그 일은 혼자 프롬프트 창 앞에서 끝나지 않고 커다란 탁자에서의 오랜 대화로
이루어졌다는 것이다.

### 5년의 대부분은 두 전신을 만들고 써 보는 시간이었다

글이 말하는 5년은 아무것도 만들지 않고 생각만 한 시간이 아니다.
Web Scrapbook과 Scribe라는 두 개의 작동하는 소프트웨어가 있었고,
사람들이 실제로 썼다.
Zotero의 사양은 그 두 도구의 사용 경험이 부딪치며 나왔다.
웹 앱은 브라우저 맥락을 알지만 학술 도구가 아니었고,
데스크톱 앱은 학술 도구지만 웹을 몰랐다.
“두 세계의 장점”이라는 목표는 두 실패를 겪어 본 사람만 쓸 수 있는 문장이다.

lmz는 이 점을 들어 글이 말하는 탄탄한 기반은 코드가 아니라 제품 설계,
그것도 앞선 두 제품의 설계라고 지적했다.[^lmz]
그렇다면 지금도 기존 제품을 연구하고 에이전트에게 구현을 맡기지 못할 이유가
없다는 것이다.
scruple은 이를 눈속임이라고 반박했다.[^scruple]
Scribe와 Web Scrapbook을 발전시키는 데서 어려웠던 것은, 오프라인 로컬 저장과
임의의 학술 목록 페이지 스크레이핑을 함께 풀 구조가 로컬 SQLite를 쓰는 브라우저
확장이라는 사실을 발견하는 일이었다는 것이다.
2003년에 두 도구를 바탕으로 만들라고 시켰다면 당시 지형대로 깨지기 쉬운 PHP
래퍼가 나왔을 것이라고 그는 보았다.
다만 원문에 실린 Greenberg의 2004년 메일은 MySQL, XML 직접 처리 같은 여러 길을
함께 꺼내고 있어, 그 구조가 처음부터 유일한 답으로 보였던 것은 아니다.
peterbell_nyc는 소프트웨어 개발을 무엇을 해야 할지 토론하기, 만들기,
써 보며 확인하기의 반복으로 나누고, LLM은 두 번째를 확실히 줄이고 나머지도 도울
수 있다고 보았다.[^peterbell_nyc]
Zotero의 5년은 이 반복이 두 개의 별도 제품에 걸쳐 느리게 돈 기록으로 읽을 수
있다.

### 구현은 플랫폼이 열리자 빨라졌다

글의 연표에는 또 하나의 병목이 보인다.
목표는 2003년 말에 섰지만, 그것을 구현할 수단은 2004년 11월 Firefox와 XUL이
나오고 나서야 생겼다.
Cohen이 출시 당일 밤 보낸 메일 제목과 Greenberg의 답장은 사양이 플랫폼을
기다리고 있었음을 보여준다.
mozStorage와 SQLite도 Firefox 쪽 사정이었다.

그리고 팀과 플랫폼이 갖춰진 뒤의 개발은 빨랐다.
2005년 7월의 0.0.1에서 약 6개월 만에 일관된 설계가 나왔고,
2006년 여름 한 철에 코드베이스가 빠르게 반복되었다.
즉 Zotero의 이야기는 느린 구상과 빠른 구현이 연달아 이어진 이야기이며,
느림은 전체 과정이 아니라 앞부분에만 해당한다.

### 오래감의 주체가 글 안에서 바뀐다

제목은 느린 형성이 오래가는 소프트웨어를 낳았다고 말하지만,
글 후반은 오래감을 다른 사람들에게 넘긴다.
Cohen은 2007년 이후 일상 작업에서 물러났고, 20년을 이끈 것은 Stillman, Takats,
비영리 법인, 국제 개발자와 자원봉사자였다.
Firefox에서 독립하고 동기화를 붙이는 일도 출시 이후 재단 지원으로 이루어졌다.

redwood는 여기서 말하는 durable이 상태나 워크플로의 내구성이 아니라 사람들의
삶에 오래 자리 잡는다는 뜻이라고 정리했다.[^redwood]
그 의미의 오래감은 출시 이전의 구상만으로 설명되지 않는다.
글은 앞부분의 느림과 뒷부분의 지속을 한 인과로 묶지만,
둘 사이를 잇는 근거는 제시하지 않는다.

## 비평

### 반사실 주장은 검증할 수 없고, 글 자체의 연표가 반례를 준다

AI가 있었더라도 구상을 앞당기지 못했을 것이라는 주장은 확인할 방법이 없다.
더구나 글의 연표는 지연의 상당 부분이 생각의 부족이 아니라 수단의 부재였음을
보여준다.
Razlogova의 2003년 12월 목록과 “webify”라는 말에는 이미 Zotero의 뼈대가 들어
있었고, 그것을 실현할 플랫폼이 1년 뒤에 나왔다.

doug_durham은 이 회고가 지나치게 낭만화되었으며,
LLM이 있었다면 5년이 5개월이 되었을 것이고 LLM은 정확히 무엇을 원하는지 모를 때
오히려 강하다고 반박했다.[^doug_durham]
kstenerud는 글이 묘사하는 과정이 조사, 사용자 연구, 시제품, 피드백,
비전 확정으로 이어지는 전형적인 대형 프로젝트 생애주기이며,
LLM은 조사와 시제품에 특히 강하다고 보았다.[^kstenerud]
Web Scrapbook은 Cohen 스스로 엄밀하지 않았다고 인정한 시제품이었는데,
그런 시제품을 몇 시간 만에 여러 개 만들어 볼 수 있었다면 두 세계를 합치는 방법도
더 일찍 시험해 볼 수 있었을 것이다.

반대 방향의 근거도 HN에서 나왔다.
mmarian은 빨리 만들 수 있는 기능을 실험하느라,
오히려 진행이 느려질 수 있다고 했다.[^mmarian]
jjuel은 LLM이 원치 않는 길로 아주 빠르게 데려가며,
그 사실을 깨닫지 못하게 만든다고 적었다.[^jjuel]
skydhash는 LLM으로 구현을 앞당기는 사람들이 대체로 무엇을 만들지 충분히 생각하지
않고, 처음부터 너무 크게 시작해 매몰비용 때문에 설계를 바꾸기 어려워진다고
관찰했다.[^skydhash]
kstenerud는 mmarian에게 그것은 규율과 오만의 실패이며 LLM 이전에도 많은 사람을
괴롭혔고, 대부분의 V2 재작성이 같은 부류라고 답했다.[^kstenerud-2]
epihelix도 에이전트형 코딩으로도 작은 오두막부터 천천히 지을 수 있다며,
최고 시속 250km인 차로 동네 길을 50km로 달려도 걷기보다는 빠르다고
비유했다.[^epihelix]
즉 쟁점은 AI가 구상을 가속할 수 있느냐가 아니라,
가속된 구현이 구상을 건너뛰게 만드느냐다.
글은 이 구분을 하지 않고 “앞당기지 못했을 것”이라는 단정으로 넘어간다.

### 느림을 가능하게 한 조건이 지워져 있다

Zotero의 5년은 시장의 압박이 없는 환경에서 가능했다.
팀은 대학 연구소에 있었고,
Sloan과 Mellon 재단, 연방 기관 IMLS의 지원금이 시간을 샀다.
핵심 구성원 다수는 역사학자였고, Cohen의 말대로 코딩은 주업이 아니라 부차적인
기술이었다.
Krei-se는 방향 없이 최선을 다해 만드는 접근이 자유와 돈벌이 압박이 없다는 조건을
전제하며, 글의 5년도 같은 조건이었다고 짚었다.[^Krei-se]
jkhdigital은 연구와 설계에 들인 시간이 저절로 정당화되지 않는다는 것을 아는 것이
학자와 엔지니어의 차이라며, 품질과 출시 시점 사이의 최적점을 찾는 것이
엔지니어의 일이라고 반박했다.[^jkhdigital]
TeMPOraL은 출시 압박이 없으면 똑똑한 프로그래머도 쓸모가 없어진 뒤까지 다듬기만
한다며, 천천히 만든 좋은 소프트웨어는 범위와 일정이 처음부터 정해져 있었기에
좋았던 것이라고 보았다.[^TeMPOraL]
Zotero에도 지원금 과제와 2006년 가을 출시라는 일정이 있었다는 점에서,
글이 말하는 느림은 끝이 정해진 느림이었다는 것은 이 노트의 해석이다.

이 조건을 빼고 교훈을 일반화하면 생존자 편향이 된다.
같은 시기 같은 방식으로 천천히 구상되었지만 사라진 학술 소프트웨어는 이 글에
나오지 않는다.
느림이 오래감의 원인이라면 느렸던 프로젝트들의 생존율을 봐야 하지만,
글은 살아남은 하나만 보여준다.

### 오래감을 만든 것은 출시 뒤 20년이다

글은 출시 이전에 집중하겠다고 처음부터 밝혔고, 그 범위 설정은 정당하다.
문제는 그 범위에서 오래감의 원인을 찾는다는 데 있다.
Zotero가 2,000만 명에게 닿은 과정에는 Firefox 의존에서 벗어나는 큰 전환,
동기화 서비스, 비영리 법인을 통한 운영이 있었고, 이는 모두 출시 이후의 일이다.
원문은 다루지 않지만, Zotero가 기대었던 XUL 확장 방식은 이후 Firefox에서
정리되었다.
첫 구상의 핵심이던 “브라우저 안에서 모든 일이 일어난다”는 결정은 결국 뒤집혔고,
그 점에서 기반의 일부는 오래가지 않았다.

shieldagent는 오래감이 대체로 지루한 결정들이 쌓인 결과라며 개방형 형식,
내보낼 수 있는 데이터, 공급업체의 변덕에 좌우되지 않는 구조를
들었다.[^shieldagent]
TripleTree가 Zotero를 쓰기 전에 데이터를 쉬운 형식으로 꺼낼 수 있는지부터 물은
것도 같은 맥락이다.[^TripleTree]
freeone3000은 CSV, XML, LaTeX로 내보낼 수 있고 원본 문서도 그대로 받을 수 있다고
답했고,[^freeone3000] drdexebtjl은 20년 동안 논란이 될 업데이트를 한 번도 하지
않은 비영리 조직이 소유한다는 이력을 들었다.[^drdexebtjl]
283a는 플러그인으로 `.bib` 파일을 자동으로 내보내고
메모는 Emacs의 org 파일에 두어, Zotero가 내일 사라져도 자료가 남는 구성을 쓴다고 했다.[^283a]
반면 Almondsetat은 학과 박사 과정 학생들에게 동기화를 제공하려 해도
셀프 호스팅이 까다롭다고 불평했다.[^Almondsetat]
epihelix는 첨부 파일만 WebDAV로 돌리면 메타데이터 동기화는 무료 무제한이라
어렵지 않다고 반박했다.[^epihelix-2]
johnobrien1010은 Zotero와 연동하는 제품을 만들며 API가 다루기 쉽고,
경쟁 제품인 EndNote는 API조차 없다고 전했다.[^johnobrien1010]
사용자가 소프트웨어를 오래 믿게 만드는 요인은 구상의 느림보다 이런 운영상의
선택에 더 가깝다.
글이 이 부분을 Takats의 별도 회고로 넘긴 것은 이해되지만,
그렇다면 제목의 인과는 절반만 다룬 셈이다.

### AI 시대와의 대비가 실제 개발 현장을 놓친다

글의 첫 문장은 소프트웨어를 AI로 거의 즉시 만들 수 있다고 전제한다.
sdevonoes는 엔지니어 1,000명 규모 회사의 중대형 기능은 절반이 다른 영역에 걸쳐
있어 논의, 설계 문서, 승인 위원회 같은 사전 조율 없이는 진행되지 않으며,
경험이 부족한 사람이 쓰는 AI는 오히려 일을 느리게 만든다고 반박했다.[^sdevonoes]
즉 즉시 만들어지는 소프트웨어는 개인용 도구나 작은 앱에 가깝고,
Zotero와 비교할 만한 규모의 소프트웨어에는 지금도 조율과 합의의 시간이 든다.
skydhash는 Caddy가 7년 동안 2,700여 개의 커밋을 쌓았을 뿐이라며,
성숙한 오픈소스 프로젝트는 대부분 한 번에 조금씩 바뀌고 시간 대부분을 아무것도
깨지지 않게 하는 데 쓴다고 짚었다.[^skydhash-2]

그렇다면 글이 세운 대비, 즉 느린 공동 사고와 빠른 봇은 실제 현장의 모습이
아니다.
조직에서 일하는 개발자에게 공동 사고는 여전히 피할 수 없는 일이며,
문제는 그것이 사라진다는 것이 아니라 생성된 장황한 문서와 미합의 PR로 오염된다는
쪽에 있다.

## 인사이트

### 싼 시제품은 느린 형성을 대체하지 않고 그 재료가 된다

Zotero의 사양은 Web Scrapbook과 Scribe라는 두 개의 불완전한 도구를 실제로 써 본
경험에서 나왔다.
이 구조를 AI 시대에 옮기면 결론은 글과 다르게 나온다.
시제품을 만드는 비용이 0에 가까워지면, 두 개가 아니라 스무 개의 Web Scrapbook을
만들어 사람들에게 써 보게 할 수 있다.
그 경험이 화이트보드와 점심 대화로 흘러들면 구상의 재료는 오히려 풍부해진다.

다만 재료가 많아진다고 소화가 빨라지지는 않는다.
Cohen의 팀이 5년 동안 한 일의 본질은 여러 사람이 같은 실패를 함께 겪고 같은
결론에 이르는 과정이었다.
huijzer는 AI로는 기능을 추가하는 것만큼 빨리 제거할 수도 있다고 했다.[^huijzer]
josephg는 반대로 LLM은 코드를 지우는 데 서툴러 기능을 넣었다 빼도 코드베이스가
늘 커진다고 반박하면서도, 시제품은 잘못된 기능을 애초에 구현하지 않게 막아 주는
좋은 수단이라고 덧붙였다.[^josephg]
싼 시제품의 가치는 그렇게 버리는 결정을 함께 내릴 수 있을 때만 생긴다.
ghoshbishakh가 AI로 기능 추가가 쉬워 보여 프로젝트를 탈선시킨 경험을 털어놓은
것은 그 결정이 없을 때 일어나는 일이다.[^ghoshbishakh]

그래서 AI 시대의 병목은 만드는 속도가 아니라 함께 판단하는 속도로 옮겨 간다.
에이전트가 하룻밤에 만든 시제품 열 개를 팀이 써 보고 토론하는 데는
여전히 몇 주가 걸리며, 이 부분을 건너뛴 조직은 결과물이 많을수록 방향을 잃는다.

### 되돌리기 어려운 결정에만 느림을 쓰면 된다

글에서 가장 오래 살아남은 결정은 기능이 아니라 이름과 로고다.
팀은 2006년 여름 디자인만큼 이름에 시간을 썼다고 자조하지만,
서체만 조금 바뀌었을 뿐 이름과 로고타입은 20년을 버텼다.
이름과 도메인, 데이터 형식, 라이선스처럼 사용자가 쌓이고 나면 바꾸기 어려운
결정이 있고, 화면 배치처럼 언제든 고칠 수 있는 결정이 있다.

이 관점에서 보면 Zotero의 일화는 모든 것을 천천히 하라는 교훈이 아니다.
SmartFox의 첫 화면은 메타데이터, 메모, 폴더를 따로 띄웠다가 하나의 서랍으로
합쳐졌고, 팀이 갖춰진 뒤 약 6개월 만에 설계가 훨씬 일관되게 바뀌었다.
반면 FileMaker 대신 오픈소스 데이터베이스를 쓴다는 방향은 2004년 말 Firefox 출시
직후부터 잡혔다.
Greenberg의 답장은 XML을 직접 다루는 대안도 함께 꺼냈지만,
Cohen은 오픈소스 데이터베이스와 Firefox 확장이 갖춰진 순간을 꿈의 도구에 필요한
재료가 모인 때로 기록한다.
이 결정이 훗날 Firefox를 떠나는 전환을 수월하게 했을 것이라는 것은 원문에 없는
해석이다.

에이전트 시대에는 이 구분이 더 중요해진다.
되돌릴 수 있는 결정은 에이전트가 빠르게 반복하게 두고,
되돌릴 수 없는 결정에만 사람의 느린 합의를 쓰는 것이 시간의 배분 원칙이 된다.

### 오래가는 소프트웨어는 플랫폼을 타고 태어나 플랫폼을 떠나며 살아남는다

Zotero는 Firefox 확장이라는 당시의 새 플랫폼 덕분에 구현될 수 있었다.
2004년 11월의 메일이 보여주듯, 플랫폼이 열리자 1년 넘게 막혀 있던 구상이
움직였다.
그러나 오래 살아남은 이유는 그 플랫폼을 떠날 수 있었기 때문이다.
Mellon과 Sloan의 지원으로 Firefox에서 독립한 것은 처음 구상의 핵심 문장,
즉 모든 일이 브라우저 안에서 일어난다는 약속을 스스로 깨는 일이었다.

이 노트의 해석으로는, 이것이 플랫폼 전환기에 태어난 소프트웨어 일반의 패턴이다.
새 플랫폼은 이전에는 불가능했던 제품을 가능하게 하지만,
그 플랫폼의 수명이 제품의 수명보다 짧은 경우가 많다.
PaulHoule은 플랫폼 관점에서 5년은 영원과 같아 무언가를 시작하면 다시 지어야 할
수도 있다며,
지금 작업 중인 앱이 2021년 이후 갱신되지 않은 React 컴포넌트에 기대고 있어
그 대가를 치르는 중이라고 적었다.[^PaulHoule]
지금 LLM과 에이전트라는 플랫폼 위에서 태어나는 도구들도 같은 시험을 받게 될
것이다.
특정 모델이나 특정 에이전트 런타임에 깊이 묶인 도구는 출시는 빠르지만,
그 런타임이 바뀌는 날 떠날 수 있는 구조인지가 20년 뒤를 결정한다.

### 느림을 사던 제도가 줄어들고 있다

Zotero의 느린 형성은 공적 지원금이 산 시간이었다.
anon7725는 Zotero가 지원금을 신청했던 IMLS가 2025년 3월 행정명령으로 사실상 해체
대상이 되고 직원 70명이 휴직 처리되었다는 Wikipedia 내용을 옮기며 이 글과의
교차점을 짚었다.[^anon7725]
piker는 경제적 유인이나 소셜 미디어 유인 없이 열정적인 학자들이 모여 있던 사진
속 세계를 그리워했다.[^piker]

이것이 글이 놓친 가장 큰 긴장이다.
AI가 구현을 싸게 만드는 동안, 구상에 시간을 쓸 수 있게 해 주던 제도는 줄어들고
있다.
시장은 빠른 출시를 보상하고, 느린 공동 사고에 돈을 대던 공공 재원은 축소되며,
그 사이에서 Zotero 같은 공공재 소프트웨어가 태어날 자리는 좁아진다.
Cohen의 교훈을 실천하려면 개인의 인내보다 먼저 그 인내를 감당할 재원 구조가
필요하다.
Northeastern University 도서관을 이끄는 지금의 Cohen이
이 문제를 직접 다루지 않은 것은 아쉬운 대목이다.

---

[^_fw]: <https://news.ycombinator.com/item?id=50005411>

[^gutechh]: <https://news.ycombinator.com/item?id=50010525>

[^lmz]: <https://news.ycombinator.com/item?id=50005824>

[^peterbell_nyc]: <https://news.ycombinator.com/item?id=50006146>

[^redwood]: <https://news.ycombinator.com/item?id=50005388>

[^doug_durham]: <https://news.ycombinator.com/item?id=50010468>

[^kstenerud]: <https://news.ycombinator.com/item?id=50005121>

[^mmarian]: <https://news.ycombinator.com/item?id=50005418>

[^jjuel]: <https://news.ycombinator.com/item?id=50011346>

[^skydhash]: <https://news.ycombinator.com/item?id=50006660>

[^Krei-se]: <https://news.ycombinator.com/item?id=50005687>

[^jkhdigital]: <https://news.ycombinator.com/item?id=50010634>

[^shieldagent]: <https://news.ycombinator.com/item?id=50006546>

[^TripleTree]: <https://news.ycombinator.com/item?id=50006404>

[^sdevonoes]: <https://news.ycombinator.com/item?id=50010582>

[^huijzer]: <https://news.ycombinator.com/item?id=50004784>

[^ghoshbishakh]: <https://news.ycombinator.com/item?id=50004669>

[^anon7725]: <https://news.ycombinator.com/item?id=50007162>

[^piker]: <https://news.ycombinator.com/item?id=50005126>

[^rrr_oh_man]: <https://news.ycombinator.com/item?id=50007686>

[^scruple]: <https://news.ycombinator.com/item?id=50006001>

[^kstenerud-2]: <https://news.ycombinator.com/item?id=50007489>

[^epihelix]: <https://news.ycombinator.com/item?id=50010189>

[^TeMPOraL]: <https://news.ycombinator.com/item?id=50008511>

[^freeone3000]: <https://news.ycombinator.com/item?id=50006504>

[^drdexebtjl]: <https://news.ycombinator.com/item?id=50010457>

[^283a]: <https://news.ycombinator.com/item?id=50006798>

[^Almondsetat]: <https://news.ycombinator.com/item?id=50006690>

[^epihelix-2]: <https://news.ycombinator.com/item?id=50010353>

[^johnobrien1010]: <https://news.ycombinator.com/item?id=50006648>

[^skydhash-2]: <https://news.ycombinator.com/item?id=50011332>

[^josephg]: <https://news.ycombinator.com/item?id=50004927>

[^PaulHoule]: <https://news.ycombinator.com/item?id=50008629>
