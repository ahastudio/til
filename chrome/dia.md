# Dia: 탭과 업무 도구의 맥락을 읽는 AI 중심 브라우저

<https://www.diabrowser.com/>

HN 토론: <https://news.ycombinator.com/item?id=42298063> (8점, 3개 댓글)

## 소개

Dia는 The Browser Company가 만든 AI 중심 브라우저이고, Arc를 만든 팀이 같은
팀이다.
홈페이지는 이를 일하는 날을 위한 브라우저라고 소개하며 macOS와 Windows용으로
내려받게 한다.
Arc가 2026년 10월 22일에 종료를 알렸으므로, Arc 사용자가 옮겨 갈 대상으로 읽히는
제품이기도 하다.
이 문서는 홈페이지와 요금제, 업무용, 개인정보처리방침, 보안, 릴리스 노트
페이지를 읽고 썼으며 제품을 직접 설치해 쓰지는 않았다.

홈페이지의 주장은 세 가지 사용 장면으로 정리된다.
아침에는 캘린더와 받은편지함과 주요 링크를 모아 주는 Morning Brief가 있다.
여러 도구(Slack, Notion, Teams 등)에 흩어진 내용을 모아 공유할 만한 보고서로
만들어 준다.
답을 찾을 때는 G Suite와 Teams와 탭 같은 전체 맥락을 파고들어 답한다.

기능은 여섯 가지가 소개된다.
프로필(업무, 프리랜서, 개인을 탭과 로그인과 AI까지 나눔), Live Work(GitHub와
Notion처럼 일이 벌어지는 곳을 탭 바에 모음), 더 나은 회의(회의 페이지와 안건과
노트와 관련 문서를 함께 열고 카운트다운을 보임), 분할 보기(레이아웃을 기억함),
덱(흩어진 맥락으로 슬라이드를 만듦), 정리된 탭(관련 탭을 이름 붙여 묶음)이다.
개인정보 영역은 트래커 차단, 광고 차단, 기억(Memory), 새 대화 개인화, 콘텐츠
데이터 공유를 켜고 끄는 설정을 보여 주며, 데이터를 팔거나 광고 프로필에 쓰지
않고 Sync를 쓰면 종단간 암호화된다고 밝힌다.

## 동작 방식

### 요금은 브라우저는 무료이고 AI는 층을 나눈 구독이다

요금제 페이지는 세 단계를 둔다.
Better Browser는 무료이며 프로필과 탭 그룹, 분할 보기와 PIP 영상, 광고와 추적
차단, 기기 간 동기화를 포함한다.
Better Answers는 모든 페이지에서 Dia에 묻고, 도구 전반의 맥락으로 대화하며,
데이터를 저장하지 않는 모델로 일하게 한다.
Better Days는 그 위에 6배의 작업량과 대화, 매일 Morning Brief, 보고서와 덱과
요약 작성, 회의 준비와 후속 처리를 더한다.[^plans]
같은 페이지의 질문 답변은 Better Browser가 AI 기능이 없는 깔끔한 브라우저라고
설명한다.[^plans]
사용량은 Task라는 단위로 계산하며 단순한 요청은 Task의 일부만 쓰고 도구와 맥락과
출력이 많은 요청은 더 쓴다.[^plans]

새 사용자에게는 카드 없이 14일 동안 Better Days를 체험하게 한다.
체험이 끝나면 유료 플랜을 고르거나 무료 브라우저로 계속 쓰며, 그때는 AI 기능이
멈춘다.[^plans]
사용량을 다 쓰면 초과 요금을 매기지 않고 다음 결제일까지 AI 기능이 멈추며, 자동
충전 같은 방식으로 이어 갈 수 있다.[^plans]

### 업무용은 SSO와 기기 관리를 더한다

업무용 페이지는 Dia가 회사 규모를 가리지 않고 쓰도록 준비 중이라고 하며, 다섯
가지를 답한다.
The Browser Company가 2025년 달력 연도를 대상으로 한 SOC 2 Type II 검사를 마쳤고
최종 보고서는 2026년에 나왔다.[^work]
AI 파트너 전부와 데이터 무보관(ZDR) 계약을 맺었고, 사용자는 콘텐츠 공유를 끌 수
있으며 기업은 조직 전체에서 끌 수 있다.[^work]
MDM 정책으로 특정 웹사이트에서 모든 AI 기능을 끌 수 있고, SAML 기반 SSO를
Google, Okta, Microsoft Entra ID 등과 지원한다.[^work]
AI 요청이 올 때 서버를 거쳐 AI 파트너에 보내는 것은 요청 처리에 필요한
것(프롬프트와 관련 페이지 맥락)만이라고 한다.[^work]

### 엔진은 Chromium이고 일부 Google 연동을 끈다

보안 페이지는 Dia가 Chromium 위에 만들어졌으며 최신 Chromium과 핫픽스를 빠르게
따라간다고 밝힌다.[^security]
끈 기능으로 Google 계정 통합(GAIA), Chromium 프로필·쿠키·비밀번호·북마크의
Google 동기화, Google 지표(UMA) 보고, 프로필 초기화 뒤 설정 업로드, Reporting
API, 네트워크 로그 파일 기록을 든다.[^security]
릴리스 노트의 최신 항목은 2026년 10월 22일의 1.54.0(Mac)으로, 채팅 시작 속도
개선, 탭을 Favorites에 고정하는 단축키, Chromium M156 업그레이드를
담았다.[^release]

## 비평

### 홈페이지의 AI 업무 장면은 요금제 아래에서 갈린다

홈페이지는 Morning Brief와 보고서와 덱을 가장 앞에 둔다.
요금제 페이지를 보면 Morning Brief와 덱과 회의 준비는 월 100달러 플랜(Better
Days)에 속한다.[^plans]
홈페이지 어디에도 이 조건이 보이지 않는다는 점이, 무료 다운로드 버튼과 함께 읽을
때 기대를 부풀린다.
HN의 kvam은 Arc 종료 스레드에서 월 100달러 요금제에서 핵심 기능이 AI 아침
브리핑이라는 이유로 옮기지 않겠다고 썼고, artdigital은 업그레이드 항목이 사라져
모두에게 무료가 된 줄 알았다고 썼다.[^kvam][^artdigital]
두 증언은 요금제 페이지의 구조(무료 브라우저와 유료 AI)로 설명되지만,
artdigital이 본 화면이 체험 기간의 상태였는지는 이 문서가 확인하지 못했다.

### 요금제 페이지 안에서 수치가 어긋난다

같은 요금제 페이지에서 Better Answers가 카드에서는 월 10달러, 질문 답변에서는 월
20달러로 쓰여 있다.[^plans]
이 문서가 읽은 시점의 불일치이며 어느 쪽이 맞는지는 확인하지 못했다.
Arc 종료 공지가 기능은 무료이고 AI는 선택이라고 한 말은 이 구조와 일치하지만,
무엇이 무료에 들어가는지의 경계가 요금제 페이지에서야 드러난다.

### 개인정보 문구가 홈페이지의 약속보다 넓다

홈페이지는 데이터를 팔지 않고 광고 프로필에 쓰지 않는다고 한다.
개인정보처리방침(2026년 4월 9일 시행)은 콘텐츠 데이터(방문한 페이지, Dia
Assistant에 낸 질문과 응답)를 수집한다고 쓰고, 제품 개선을 위해 사용자가
거부하지 않으면 콘텐츠도 쓸 수 있다고 쓴다.[^privacy]
업무용 페이지는 사용자가 콘텐츠 공유를 끌 수 있다고 하므로 기본값이 무엇인지가
핵심인데, 이 문서가 읽은 페이지에서는 기본값을 확인하지 못했다.
Sync를 켜면 콘텐츠 전부가 기기 밖으로 나가 서버에서 처리되지만 종단간 암호화되어
읽을 수 있는 형태로 처리나 저장되지 않는다고 방침은 쓴다.[^privacy]
방침은 법적 의무와 약관 집행을 위해 정부와 법 집행 기관에 개인정보를 공유할 수
있다고도 쓴다.[^privacy]

### 단일 제품 약속과 이력 사이의 간극

Arc 종료 공지를 받은 사용자들의 반응이 주로 이 지점에 모였다.
jdgoesmarching은 유지를 약속한 뒤 접은 팀이 만든 브라우저로 옮길 이유가 없다고
했고,[^jdgoesmarching] simjnd와 jhaile는 Arc의 기능이 Dia로 오지 않았다고
했다.[^simjnd][^jhaile]
falloon은 한 해를 식힌 뒤 Dia를 써 보니 AI를 끌 수 있고 잘 설계됐다고 반대
경험을 적었다.[^falloon]
2024년 이 제품이 처음 소개됐을 때도 jswny는 한 회사가 두 브라우저를 어떻게
유지하느냐고 물었고, hands는 Arc가 최근 버그가 많았던 이유를 알겠다고
했다.[^jswny][^hands]
2025년 6월 Verge 기사 스레드의 blinky88은 Dia에 관심이 없고 Arc가 죽어야 했다는
것이 놀랍다고 했다.[^blinky88]
이 반응들은 기능이 아니라 두 제품 전략의 순서에 대한 불신을 보여 주며,
홈페이지는 이에 대해 아무 말도 하지 않는다.

## 인사이트

### 브라우저가 맥락의 수집 지점이 되면 요금과 개인정보가 한 문제가 된다

Dia의 가치 제안은 탭과 도구 전반의 맥락을 읽는 것이고, 그 맥락이 넓을수록 답이
좋아지며, 같은 이유로 개인정보 위험이 커진다.
요금제는 이를 층으로 나눈다.
브라우저는 무료이지만 맥락을 읽는 기능은 구독이며, 사용량 단위(Task)가 도구와
맥락과 출력 길이에 비례해 소모된다.[^plans]
이 구조에서 더 많은 맥락을 쓰는 사용자가 더 많이 내고 더 많은 데이터를 넘긴다.
개인정보 문구가 중요해지는 이유는 요금과 데이터의 양이 같은 방향으로 움직이기
때문이다.

### Chromium 기반의 보안 약속은 상류에 묶인다

보안 페이지의 가장 구체적인 약속은 Chromium 최신 버전과 핫픽스를 따라간다는
것이다.[^security]
릴리스 노트의 최신 항목이 M156 업그레이드를 담은 것은 이 약속과 맞는
증거다.[^release]
다만 Arc 종료 공지가 종료의 이유로 든 것이 AI 시대의 보안 유지 인력이라는 점을
함께 읽으면, 같은 엔진을 쓰는 제품 둘을 한 팀이 따로 지킬 수 없다는 논리가
Dia에도 적용된다.
이 약속의 지속 가능성은 Dia 한 제품에 인력을 모았다는 설명에 의존한다.

### 이 글을 읽는 방법

Arc 사용자가 옮길 때는 무료 브라우저만으로 쓸지, AI 플랜을 쓸지를 먼저 정하는
것이 순서다.
무료 범위는 프로필, 탭 그룹, 분할 보기, 광고와 추적 차단, 동기화이며, 홈페이지가
앞세운 Morning Brief 같은 기능은 유료이고 AI 기능은 14일 체험 뒤 멈춘다.[^plans]
이 소개의 주장을 가를 관찰은 두 가지다.
콘텐츠 공유의 기본값이 켜져 있는지, 그리고 1년 뒤에도 Dia가 같은 요금 구조와
무료 범위로 유지되는지다.
둘 다 홈페이지가 아니라 설정 화면과 이후의 공지로만 확인할 수 있다.

---

[^plans]: The Browser Company, [Dia Browser | Plans](https://www.diabrowser.com/plans)

[^work]: The Browser Company, [Dia Browser | Work](https://www.diabrowser.com/forwork)

[^security]: The Browser Company, [Dia Browser | Security](https://www.diabrowser.com/security)

[^privacy]: The Browser Company, [Dia Browser Privacy Policy](https://www.diabrowser.com/privacy), 2026-04-09

[^release]: The Browser Company, [Dia Browser | Update 1.54.0 for macOS](https://www.diabrowser.com/release-notes/latest), 2026-10-22

[^kvam]: <https://news.ycombinator.com/item?id=50199291>

[^artdigital]: <https://news.ycombinator.com/item?id=50202880>

[^jdgoesmarching]: <https://news.ycombinator.com/item?id=50198480>

[^simjnd]: <https://news.ycombinator.com/item?id=50198502>

[^jhaile]: <https://news.ycombinator.com/item?id=50199454>

[^falloon]: <https://news.ycombinator.com/item?id=50198096>

[^jswny]: <https://news.ycombinator.com/item?id=42296947>

[^hands]: <https://news.ycombinator.com/item?id=42300853>

[^blinky88]: <https://news.ycombinator.com/item?id=44251891>
