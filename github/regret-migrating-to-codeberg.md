# Codeberg로 옮긴 것을 후회한다: 금지보다 무서운 것은 범주를 정하는 권한

원문: [マリウス . I Regret Migrating to Codeberg](https://xn--gckvb8fzb.com/i-regret-migrating-to-codeberg/)

HN 토론: <https://news.ycombinator.com/item?id=49021856> (565점, 567개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/ax914v/protecting_our_floss_commons_from_llms> (153점, 175개 댓글)

GN 토론: <https://news.hada.io/topic?id=31772>

## 요약

マリウス(마리우스)가 2026년 7월 23일 자기 블로그에 쓴 글이다.
저자는 GitHub를 떠난 이유가 기능 하나나 장애 한 번이 아니라
Microsoft 소유 아래에서 진행된 플랫폼의 열화였다고 밝힌다.
웹 화면은 느린 JavaScript 덩어리로 다시 쓰였고,
GitHub는 WhatsApp처럼 사실상의 공공 기반 시설이 되어
한 회사가 세계 소프트웨어에 대해 지나친 영향력과 감시 능력을 쥐게 됐다.
멀쩡한 개발자가 임의로 계정을 잃었다는 이야기도 백업처를 찾게 만든 이유였다.

그래서 비영리 협회가 운영하는 Codeberg로 옮겼는데,
몇 달 만에 이용 약관이 바뀌었다.
2026년 총회(Assembly 2026) 안건으로 6월 29일에는 LLM 중심 프로젝트 금지안이,
7월 2일에는 암호화폐 프로젝트 금지안이 올라왔고 둘 다 통과됐다.
암호화폐 금지는 약관에서 “Codeberg의 평판을 해치는 콘텐츠”의 예시로 들어갔다.
저자는 이 분류가 근거나
실제 사례 없이 범주 전체를 금지하려는 법률 용어처럼 읽힌다고 본다.

저자가 가장 크게 반박하는 것은 Codeberg 공지 글의
“The development team of none” 절이다.
그 절은 LLM으로 코딩하는 사람이 큰 팀이 있는 듯 일하지만
실은 혼자이고 주변에 커뮤니티가 없다는 점을 모른다고 말한다.
저자는 자유 소프트웨어 대부분이 1인 프로젝트이며,
자신도 수십 년 동안 도구를 만들었지만
낭만적인 의미의 커뮤니티를 가져 본 적이 없다고 답한다.
Forgejo가 Gitea에서 갈라져 나오며
6년 가까이 쌓인 기여자 커뮤니티를 물려받았다는 점을 들어,
그런 Codeberg가 1인 개발자에게 커뮤니티를 말할 처지는 아니라고도 꼬집는다.

핵심 주장은 금지된 범주 자체가 아니라 자유 소프트웨어 허브가
어떤 소프트웨어가 좋은지 정하기 시작했다는 데 있다.
범주 하나를 평판 훼손으로 규정하면 삭제 기준이 합법성이나 유용성이 아니라
플랫폼의 입장과 맞는지로 바뀌고,
오늘 쉽게 금지한 범주가 내일의 다음 금지를 위한 선례가 된다는 것이다.
저자는 LLM 저장소가 인프라를 압박하고 저품질 이슈와 PR을 쏟아 내며
저작권 문제를 안고 있다는 점, 암호화폐 쪽에 사기가 많았다는 점은 인정한다.
그러면서 리누스 토르발스(Linus Torvalds)가 LLM을
결과로 평가할 도구로 다룬다는 점을 근거로 든다.

대안으로 저자는 자원 문제를 자원 문제로 다루자고 제안한다.
저장소를 만들 때 LLM 생성 코드나 암호화폐 관련 여부를 체크박스로 신고하게 하고,
신고된 저장소는 별도 할당량이 걸린 인프라 등급으로 옮기며
필요하면 비용을 내게 한다.
그 저장소에는 Codeberg가 품질을 책임지지 않는다는 경고문을 자동으로 붙이고,
신고하지 않았다가 들키면 그때 영구 금지하자는 것이다.
저자는 두 범주 어느 쪽에도 해당하는 프로젝트가 없지만
자체 Git 호스트를 세우겠다고 한다.
결정이 총회를 거친 것은 인정하면서도,
일반 사용자는 결정이 끝난 날 사이트 상단 배너로
처음 알았고 논의 중에 의견을 낼 통로가 없었다는 점을 떠나는 이유로 든다.

## 분석

### 출발점은 기능이 아니라 의존의 구조였다

이 글은 Codeberg 비판으로 읽히지만 첫 문단은 GitHub에서 시작한다.
저자가 GitHub를 떠난 이유는 느린 화면 같은 품질 문제와
한 회사가 공공 기반 시설을 쥐고 있다는 권력 문제가 섞여 있다.
Codeberg는 두 번째 문제에 대한 답으로 선택됐고,
그래서 저자가 Codeberg에 기대한 것은 기능이 아니라 “자유”라는 성격이었다.

이 구조를 보면 왜 저자가 자기와 무관한 금지에 반응하는지 이해된다.
저자는 LLM 프로젝트도 암호화폐 프로젝트도 없다.
그런데도 떠나는 이유는 GitHub에서 겪은 것과 같은 종류의 위험,
즉 운영 주체가 약관을 바꿔 사용자를 내보낼 수 있다는 위험을 다시 봤기 때문이다.
금지 내용보다 금지할 수 있다는 사실이 문제라는 주장은
처음부터 의존 관계를 피하려고 옮긴 사람에게는 자연스러운 결론이다.

### 저자는 금지보다 결정 방식을 문제 삼는다

글 후반부는 내용보다 절차를 다룬다.
저자는 총회라는 절차가 있었다는 점을 인정하면서도,
사용자가 논의 단계에서 알 수 없었고
결정이 끝난 뒤 배너로 통보받았다는 점을 문제로 삼는다.
이는 Codeberg의 의사결정이 회원 단체의 것이고,
저장소를 올리는 사용자 대부분은 회원이 아니라는 구조에서 나온다.

HN에서 투표권을 가진 회원이라고 밝힌 Aachen은 이 절차를 안에서 본 모습을 전했다.
투표 전 연례 총회에서 안건마다 짧은 발표와 몇 분의 질의응답이 있었지만,
문안이 이미 확정된 상태라 토론이 아니라 확인 질문만 가능했다고 한다.
서버 부하를 물었더니
생성 코드가 아니라 AI 크롤러 이야기로 답이 돌아왔다고도 적었다.[^Aachen]
회원이 아닌 사용자가 체감한 것과 회원이 체감한 것이
둘 다 “논의는 없었다”로 수렴한다는 점이 이 비판의 무게를 더한다.

Lobste.rs의 tuxes는 투표 수치를 정리했다.
투표권자 1,085명 중 517명이 투표했고 그중 358명이 찬성했다.[^tuxes]
altano는 2025년 11월 Codeberg가 공개한 사용자 수에 대면
이 결정이 사용자의 약 0.3%에 의해 내려진 셈이라고 계산했다.[^altano]
회원 기준으로는 민주적이었지만 사용자 기준으로는 그렇지 않다는 간극이
저자가 말한 “배너로 알게 된” 경험의 실체다.

### 대안은 범주 금지를 자원 회계로 바꾸자는 제안이다

저자의 대안은 단순한 반대가 아니라 문제를 다시 정의하는 시도다.
Codeberg가 스스로 밝힌 문제는 자원 소비와 그 비용인데,
그렇다면 범주를 금지할 것이 아니라
비용을 만든 사람에게 비용을 물리면 된다는 논리다.
자기 신고와 별도 등급, 할당량, 유료화, 경고문은
범주에 대한 가치 판단을 빼고 자원 사용량만 남기려는 장치다.

이 제안은 HN에서도 여러 사람이 독립적으로 내놓았다.
eviks는 자원을 많이 쓰는 것을 막으면 될 일이며,
자원을 거의 안 쓰는 LLM 프로젝트는 어떻게 하느냐고 물었다.[^eviks]
boramalper도 과도한 자원 사용 문제를 AI 금지로 우회하지 말고
제한과 할당량으로 직접 다루면 된다고 했다.[^boramalper]
저자의 대안은 개인 의견이 아니라 이 논쟁에서
가장 흔한 반론을 정리한 것에 가깝다.

## 비평

### 인용한 문장의 맥락을 잘라 냈다

저자가 가장 공들여 반박한 문장은 커뮤니티가 없다는 부분인데,
Lobste.rs의 krig는 저자가 바로 뒤 문장을 빼고 인용했다고 지적했다.
원래 문단은 그런 프로젝트가 커뮤니티가 있는 것처럼 자원을 쓴다고 이어지고,
코드 활동과 무거운 CI/CD, 잦고 큰 릴리스 바이너리,
실제 사용자보다 지원 플랫폼이 더 많아 보이는 경우를 든다.[^krig]
맥락을 붙이면 그 문단의 요지는 1인 개발이 아니라
사용량에 비해 지나친 자원 소비라는 것이다.

HN에서 가장 많은 지지를 받은 축에 드는 adamddev1의 댓글도 같은 지점을 짚었다.
저자가 “커뮤니티가 있는 것”과 “호스팅할 가치가 있는 정당한 소프트웨어”를
Codeberg가 혼동한다고 요약하면서 따옴표를 썼지만,
그 표현은 Codeberg 글에 없다는 것이다.
자신도 1인 개발자인데 그 글에서
1인 개발자를 깎아내리는 대목을 찾지 못했다고 했다.[^adamddev1]
anticorporate는 Codeberg 글에서 사용자도 거의 없는 1인 프로젝트가
큰 커뮤니티 프로젝트보다 자원을 더 쓰는 것이 터무니없다는 대목을 인용하며,
문제 삼은 것은 커뮤니티 유무가 아니라
“유령 프로젝트”라고 정리했다.[^anticorporate]

그렇다고 저자의 반박이 완전히 헛짚은 것은 아니다.
nylonstrung은 xz, core-js, GnuPG, NTPd 같은 사실상 1인 프로젝트 위에
엄청난 양의 기술이 돌아간다며,
Codeberg 글이 1인 개발자를 소외시키는 함의를
굳이 담을 필요는 없었다고 했다.[^nylonstrung]
altano는 주당 수십만 번 내려받히지만
이슈나 PR은 한 번도 받은 적 없는 프로젝트가 있다며,
그런 프로젝트의 자원 소비는
Codeberg 눈에 좋은 것이냐 나쁜 것이냐고 되물었다.[^altano-downloads]
문장을 잘라 인용한 것은 결함이지만,
“커뮤니티”를 기준처럼 쓴 Codeberg 글의 표현이 오독을 부른 면도 있다.

### Codeberg는 처음부터 중립 호스트가 아니었다

저자는 이번 변경이 Codeberg가 “자유”를 바꾸는 첫걸음이라고 쓰지만,
Codeberg는 원래부터 무엇을 받을지 정하는 곳이었다.
debugnik은 HN에 Codeberg에 대한 집단적인 착각이 있다고 했다.
웹사이트에는 뜻이 맞는 FOSS 프로젝트를 위한 커뮤니티 비영리 단체라고 적혀 있고,
FAQ는 비공개 저장소를 다른 곳에 두라고 직접 권하는데도
HN에서는 개인과 회사를 위한 GitHub 대안처럼 추천된다는 것이다.[^debugnik]
자유 라이선스가 아니면 받지 않는다는 조건부터가 이미 입장을 가진 선택이다.

다만 착각이 생긴 데는 Codeberg의 책임도 있다.
VariousPrograms는
Codeberg에서 받은 인상이 “다 같이 와서 자유 소프트웨어를 만들자”였다며,
진지한 프로젝트만 원한다면 홈페이지에서
“hobbyists”라는 단어부터 빼야 한다고 했다.[^VariousPrograms]
Yokohiii는 최근 저장소를 만들 때
이런 제한이나 선호를 알려 주는 안내가 하나도 없었다며,
그저 또 하나의 GitHub처럼 보이게 해 놓고 사용자가 알아서 판단하길 기대하는 것은
Codeberg 쪽의 소통 실패라고 지적했다.[^Yokohiii]
저자의 놀람은 사실관계로는 틀렸지만,
그 놀람이 흔하다는 것은 Codeberg가 풀어야 할 문제다.

### 저자의 대안도 결국 꼬리표를 붙인다

저자는 범주로 낙인찍는 것을 비판한 뒤
자기 신고 체크박스로 같은 범주에 꼬리표를 붙이고
별도 등급으로 분리하자고 제안한다.
Lobste.rs의 travisgriggs는 이 점을 꼬집었다.
꼬리표와 차별에 윤리적으로 분노하더니 자원 비대칭이 실제 문제라는 것은 인정하고,
조금 다른 꼬리표 방식을 내놓은 것뿐이라는 것이다.[^travisgriggs]
저자가 반대한 것이 범주 판단 자체라면 이 제안은 그 반대와 맞지 않는다.

할당량 방식이 더 공정하다는 전제도 따져 볼 만하다.
inigyou는 할당량을 걸면 스팸성 계정마다 할당량을 끝까지 채우고 떠날 것이므로
결국 할당량을 낮게 잡을 수밖에 없다고 했다.
반면 “스팸은 받지 않는다”고 정하면 스팸에 한 바이트도 쓰지 않고
다른 모든 사람에게 더 넉넉한 할당량을 줄 수 있다는 것이다.[^inigyou]
adamddev1도 원칙적인 금지가 오히려 손으로 만드는 프로젝트에
더 많은 여유를 남긴다고 봤다.[^adamddev1-quota]
비용을 물리는 방식은 공정해 보이지만,
그 비용은 금지당하지 않은 사람들의 한도로도 돌아온다.

Lobste.rs의 jbauer는 더 근본적인 반론을 냈다.
비영리 단체에 자기가 선호하는 기술적 해법을 요구하는 것은 흔한 주장이지만,
인프라를 운영하는 사람들은 2단계 체계를 관리하거나
허점을 찾는 사람과 씨름할 유사 법률 체계를 만들고 싶지 않아서
이 방식을 택했다는 것이다.[^jbauer]
자원이 넉넉하지 않은 자원봉사 조직에 신고, 감사, 과금 체계를 요구하는 것은
금지보다 훨씬 무거운 운영 부담을 지우는 일이다.

### 리누스 비유와 검열이라는 단어가 논증을 부풀린다

저자는 리누스 토르발스가 LLM을 결과로 판단할 도구로 다루니
작은 포지(forge)도 그럴 수 있다고 쓴다.
waterTanuki는 이 비교가 성립하지 않는다고 했다.
리누스에게는 하나의 코드베이스를 검토하고
걸러 줄 Linux 메인테이너 전체가 있지만,
Codeberg는 훨씬 적은 인원으로
쏟아지는 수많은 코드베이스를 살펴야 한다는 것이다.[^waterTanuki]
“결과로 판단하라”는 원칙은 판단할 사람이 충분할 때만 실행 가능하다.

“검열”이라는 단어도 과하다.
preya2k는 Codeberg가 등록된 독일에서 검열은 정부가 하는 것을 뜻하며,
민간 협회가 자기 서비스를 어떻게 운영할지 정하는 것은
영업의 자유로 본다고 했다.[^preya2k]
mschuster91은 독일의 방해자 책임(Störerhaftung) 같은 법 때문에
비영리 단체에는 문제를 일으키는 프로젝트를
빨리 내보낼 수단이 필요하다고 설명했다.[^mschuster91]
Lobste.rs의 hunger는 Codeberg가 LLM 생성 코드의 저작권 상태가 불분명하다는 점,
즉 호스팅 자체가 합법인지 모호하다는 점을 이유로 들었다는 데 주목했다.[^hunger]
저자가 기준이 합법성에서 입장으로 바뀐다고 했지만,
Codeberg가 내세운 이유 중 하나는 바로 합법성이었다.

## 인사이트

### 진짜 결함은 집행할 수 없는 경계선이다

저자는 범주 금지를 문제 삼았지만,
이 정책에서 더 오래 문제를 일으킬 부분은 “대부분(mostly)”이라는 한 단어다.
약관은 코드 대부분이 생성형 AI로 쓰인 프로젝트를 공유하지 말라고 한다.
Lobste.rs에서 mitsuhiko는 그 기준이라면
지난 18개월 동안 자신이 쓴 오픈소스 코드 거의 전부가
Codeberg에 올라갈 수 없다고 했다.[^mitsuhiko]
불과 석 달 전 그 플랫폼 사람들에게서
프로젝트를 옮기라는 초대를 받았다고도 덧붙였다.[^mitsuhiko-invite]

fuglede_는 저작권이 이유라면 왜 “대부분”이냐고 물었다.
절반을 손으로 쓴다고
나머지 절반의 저작권 상태가 분명해지지는 않는다는 것이다.[^fuglede_]
BadBadJellyBean은 LLM 코드를 확실히 가려낼 방법이 없으니
이 규칙은 아예 적용되지 않거나,
적용될 때 결정적이지 않은 증거로 자의적으로 적용될 것이라고 봤다.
고양이 이름이 Claude라서 커밋에 “Co-Authored-By: Claude”를
붙일 수도 있다는 예를 들었다.[^BadBadJellyBean]
cmrdporcupine은 Codeberg 공지 글의 세부 설명이 투표가 끝난 뒤에 나왔고,
정작 투표 문안에는 그런 단서가 없었으며
해명 요청도 받아들여지지 않았다고 했다.[^cmrdporcupine]

이 경계선의 2차 효과는 금지 대상을 없애는 것이 아니라 숨기게 만드는 것이다.
embedding-shape는 규칙이 AI 사용을 막으면 사람들은 흔적을 지울 유인이 생기고,
결국 Codeberg가 GitHub보다 사람 코드와 AI 코드를
구별하기 더 어려운 곳이 될 수 있다고 봤다.[^embedding-shape]
GitHub에서는 아무렇지 않게 붙던 공동 작성자 표기가
Codeberg에서는 사라지는 셈이다.
저자가 말한 “미끄러운 경사”보다 더 가까운 위험은
아무도 지키는지 확인할 수 없는 규칙이 선의의 사용자만 걸러 내는 일이다.

### 작은 대안은 큰 플랫폼의 권력 문제를 줄여서 복제한다

저자의 이력은 하나의 패턴을 보여 준다.
GitHub의 권력이 싫어서 Codeberg로 갔고,
Codeberg의 권력이 싫어서 이제 자체 호스팅으로 간다.
HN의 anarki8은 3년 전 Codeberg로 옮겼다가 이번에 떠나며 기부도 끊었는데,
처음 Codeberg로 온 이유도 SourceHut의 비슷한 규칙,
즉 암호화폐 금지 때문이었다고 했다.[^anarki8]
사용자는 같은 이유로 플랫폼을 옮기고, 옮겨 간 곳에서 같은 일을 다시 겪는다.

danpalmer는 거대 플랫폼의 열화에 대한 답은
더 작은 같은 것으로 옮기는 것이 아니라고 했다.
GitHub에서 Codeberg나 SourceHut으로,
Twitter에서 Mastodon으로 옮긴 것이 통하지 않은 이유는
문제가 규모가 아니라 권력이기 때문이라는 것이다.
그는 데이터와 네트워크와 인터페이스를 서로 다른 주체가 맡게 하는 구조,
예컨대 Bluesky의 AT Protocol이나 포지 쪽의 Tangled 같은
방식이 한 걸음 나아간 답이라고 봤다.[^danpalmer]
운영자를 더 착한 사람으로 바꾸는 것으로는 운영자가 가진 권한 자체가 줄지 않는다.

Codeberg 문서에는 대안 목록도 있지만 그 한계도 드러났다.
Lobste.rs의 mtlynch는 목록에 오른 포지 대부분이 한 사람이나 소수의 취미 운영자가
여가 시간에 돌리는 곳이고,
GitHub, GitLab, Bitbucket 같은 실질적인 경쟁자는 빠져 있다고 했다.[^mtlynch]
gasche는 소프트웨어 프로젝트는 쉽게 가치 중립을 유지할 수 있지만
호스팅 플랫폼은 무엇을 받을지라는 질문에 금방 끌려 들어간다며,
그래서 이런 다툼이 Linux나 GNOME보다
reddit이나 GitHub, Codeberg에서 더 잦다고 설명했다.[^gasche]
호스팅을 공유하는 한 누군가는 경계를 정해야 하고,
그 권한에서 벗어나는 유일한 길은 저자처럼 자기 서버를 갖고
다른 곳은 미러로 두는 것이다.

### 회원제 민주주의는 사용자의 발언권과 같지 않다

Codeberg 지지자들이 가장 자주 든 반론은
이 결정이 GitHub의 어떤 결정보다 민주적이었다는 것이다.
그런데 그 민주주의의 단위는 사용자가 아니라 회비를 내는 회원이다.
mschuster91은 저자에게
당신은 Codeberg e.V.의 회원이 아니라 일반 사용자일 뿐이며,
의사결정에 참여하고 싶으면 회원이 되라고 답했다.[^mschuster91]
절차로서는 맞는 말이지만,
이는 저장소를 맡긴 사람 대부분이 결정에서 처음부터 빠져 있다는 뜻이기도 하다.

Lobste.rs에서 mitsuhiko는 민주주의는 결정 절차일 뿐
그 결과가 포용적이거나 도덕적으로 옳거나
현재 사용자에게 좋다는 보장은 아니라고 했다.[^mitsuhiko-democracy]
투표권자의 절반이 채 안 되게 참여한 투표에서 정해진 규칙이
그보다 수백 배 많은 사용자를 구속한다면,
그 결정은 회원에게는 민주적이고 사용자에게는 통보다.
이 간극은 Codeberg가 커질수록 더 벌어진다.
사용자는 회원보다 빨리 늘고, 회원은 대개 뜻이 맞는 사람이 되기 때문이다.

이 구조는 협동조합형 서비스가 커질 때마다 반복되는 긴장이다.
회원 공동체는 자기 가치에 맞는 결정을 내리는 데 강하지만,
그 가치를 공유하지 않는 이용자에게
공공 기반 시설처럼 받아들여지는 순간 마찰이 생긴다.
저자가 GitHub에서 피하려 한 것은 “공공 기반 시설을 한 회사가 쥐는 것”이었는데,
Codeberg에서 마주친 것은
“공공 기반 시설처럼 쓰이는 곳을 한 회원 단체가 쥐는 것”이었다.
운영 주체의 성격은 바뀌었지만 이용자와 결정권자가 다르다는 구조는 그대로다.

### 꼬리표가 모호하면 다음 금지가 더 쉬워진다

암호화폐 금지가 들어간 자리는 “평판을 해치는 콘텐츠”라는 열린 범주다.
Lobste.rs의 calvin은 무엇이든 금지하는 것은 그들 권리지만
금지하려면 명시적으로 하라며,
이 문구는 잘해야 조문 해석 다툼으로, 나쁘면 자의적 금지로 이어질 것이라고 했다.
Hetzner와 연합우주(fediverse) 인스턴스 사이의 갈등을 그런 예로 들었다.[^calvin]
범주를 직접 열거하는 대신 평판이라는 상위 개념 아래 예시로 넣으면,
다음 범주는 약관 개정 없이도 같은 문장 아래로 들어올 수 있다.

저자가 말한 미끄러운 경사는 대개 과장된 수사로 취급되지만,
이 경우에는 문장 구조가 실제로 그 경사를 만들어 둔다.
금지 대상의 목록이 아니라 금지 사유의 범주가 약관에 생겼기 때문이다.
이 점에서 저자의 걱정은 LLM이나 암호화폐에 대한 입장과 무관하게 성립한다.
Codeberg가 이 우려를 덜려면 금지 범주를 늘리는 것보다
“평판” 같은 열린 사유를 구체적인 목록으로 좁히는 편이 효과적일 것이다.

---

[^Aachen]: <https://news.ycombinator.com/item?id=49022630>

[^tuxes]: <https://lobste.rs/s/ax914v/protecting_our_floss_commons_from_llms#c_63ha1j>

[^altano]: <https://lobste.rs/s/ax914v/protecting_our_floss_commons_from_llms#c_hmhv77>

[^eviks]: <https://news.ycombinator.com/item?id=49032504>

[^boramalper]: <https://news.ycombinator.com/item?id=49032765>

[^krig]: <https://lobste.rs/s/ax914v/protecting_our_floss_commons_from_llms#c_ddepdf>

[^adamddev1]: <https://news.ycombinator.com/item?id=49031920>

[^anticorporate]: <https://news.ycombinator.com/item?id=49023425>

[^nylonstrung]: <https://news.ycombinator.com/item?id=49022844>

[^altano-downloads]: <https://lobste.rs/s/ax914v/protecting_our_floss_commons_from_llms#c_aon7ff>

[^debugnik]: <https://news.ycombinator.com/item?id=49031836>

[^VariousPrograms]: <https://news.ycombinator.com/item?id=49029403>

[^Yokohiii]: <https://news.ycombinator.com/item?id=49023636>

[^travisgriggs]: <https://lobste.rs/s/ax914v/protecting_our_floss_commons_from_llms#c_jjkqrh>

[^inigyou]: <https://news.ycombinator.com/item?id=49037614>

[^adamddev1-quota]: <https://news.ycombinator.com/item?id=49032893>

[^jbauer]: <https://lobste.rs/s/ax914v/protecting_our_floss_commons_from_llms#c_mzgkvh>

[^waterTanuki]: <https://news.ycombinator.com/item?id=49031858>

[^preya2k]: <https://news.ycombinator.com/item?id=49023314>

[^mschuster91]: <https://news.ycombinator.com/item?id=49033070>

[^hunger]: <https://lobste.rs/s/ax914v/protecting_our_floss_commons_from_llms#c_ikx74m>

[^mitsuhiko]: <https://lobste.rs/s/ax914v/protecting_our_floss_commons_from_llms#c_pw7ant>

[^mitsuhiko-invite]: <https://lobste.rs/s/ax914v/protecting_our_floss_commons_from_llms#c_lwrw1z>

[^fuglede_]: <https://news.ycombinator.com/item?id=49033072>

[^BadBadJellyBean]: <https://news.ycombinator.com/item?id=49034270>

[^cmrdporcupine]: <https://news.ycombinator.com/item?id=49035007>

[^embedding-shape]: <https://news.ycombinator.com/item?id=49022375>

[^anarki8]: <https://news.ycombinator.com/item?id=49032460>

[^danpalmer]: <https://news.ycombinator.com/item?id=49031420>

[^mtlynch]: <https://lobste.rs/s/ax914v/protecting_our_floss_commons_from_llms#c_x2vuwa>

[^gasche]: <https://lobste.rs/s/ax914v/protecting_our_floss_commons_from_llms#c_5rn9el>

[^mitsuhiko-democracy]: <https://lobste.rs/s/ax914v/protecting_our_floss_commons_from_llms#c_x0u2og>

[^calvin]: <https://lobste.rs/s/ax914v/protecting_our_floss_commons_from_llms#c_fy4kmp>
