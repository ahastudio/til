# GitHub이 가라앉고 있다

원문: <https://dbushell.com/2026/04/29/github-is-sinking/>

HN 토론: <https://news.ycombinator.com/item?id=48085095> (263점, 167개 댓글)

GN 토론: <https://news.hada.io/topic?id=29405>

## 요약

David Bushell은 2026년 4월 29일 이 글에서 Microsoft 인수 이후 GitHub이
신뢰할 수 없는 서비스가 됐다고 주장한다.
글머리의 한 줄 요약은 GitHub이 한때 멋졌지만 이제 슬롭(slop)의 무덤이 됐다는
것이다.
핵심 명제는 “GitHub is racing towards the mythical zero nines of uptime”,
즉 GitHub이 가용률 표기에서 9가 하나도 남지 않는 수준으로 치닫고 있다는
것이다.
근거로는 GitHub 공식 상태 페이지의 과거 기록을 월별로 모은 업타임 차트와,
상태 페이지가 빠뜨린 장애까지 다시 집계한 비공식 페이지를 링크한다.
차트에서 초록색이던 선은 인수 이후 주황색과 빨간색의 롤러코스터로 바뀐다.

저자는 원인을 Microsoft의 enshittification(점진적 가치 훼손)으로 돌린다.
Copilot이 곳곳에 번식했고, GitHub이 슬롭으로 스스로를 DDoS하고 있다고
표현하며, 이 대목에는 GitHub이 직접 쓴 가용성 공지를 링크한다.
무엇이 잘못됐는지는 알지도 못하고 관심도 없다고 덧붙인다.
그러고는 GitHub을 떠난다는 글이 쏟아지는 중이라며 부고 목록을 단다.
Lonami, Mitchell Hashimoto의 Ghostty 이전, Armin Ronacher, Jonas Hietala,
Alex Hyett, Jorijn Schrijvershof의 글이 그 목록이다.

이 글의 중심 논제는 “Git is not GitHub”다.
Git은 오픈소스이고 분산형이라 모든 저장소가 동등하며,
중앙 서비스 없이도 동작한다.
중앙 서비스에 모이는 관행은 사회적 편의가 만든 구성물일 뿐이고,
GitHub은 쓸모 있는 부가 서비스였는데 Microsoft가 비싼 부채로 바꿨다는 것이다.
예상되는 반론에도 하나씩 답한다.
네트워크 효과에 대해서는 가짜 스타 경제가 무가치해졌고
봇과 슬롭이 넘쳐 GitHub이 코드판 Moltbook이 되고 있다고 답한다.
CI에 대해서는 파이프라인이 과잉 설계됐고 GitHub Actions는 흉물이라고 하면서,
다른 해법을 찾는 일이 고역이라는 점은 인정한다.
배가 가라앉고 있으니 한 번에 다 옮기지 않더라도 이전을 시작하라고 권한다.

대안 목록은 가장 가까운 구명보트인 다른 중앙화 Git 포지부터 시작한다.
가입하고 새 업스트림에 푸시하면 되고, 이슈는 두고 떠나도 된다고 말한다.
나중에 단 편집 메모에서는 어떤 선택지도 완벽하지 않으니
직접 조사하라고 덧붙였다.

- Codeberg: 비영리 커뮤니티 주도 프로젝트로 이력이 검증된 안전한 대안이며,
  Forgejo의 플래그십 인스턴스다.
- Tangled: AT Protocol 통합이 흥미로운 알파 단계 스타트업으로,
  작은 1인 프로젝트라면 고려할 만하다.
- Gitea: 클라우드 관리형 호스팅을 제공하며,
  Codeberg와 Forgejo가 갈라져 나온 원조 프로젝트다.
- GitLab: 엔터프라이즈급이라 비대하고 헷갈리지만 상사에게는 인상적일 것이라고
  비꼰다.
  이후 편집 메모에서는 GitLab에도 같은 부패가 번졌다고 적었다.
- Bitbucket: 영혼을 갉아먹는 기업 서비스를 다른 기업 서비스로 바꾸는 것이라
  강하게 말리지만, GitHub만 아니면 된다는 기준에는 들어간다.

독자들이 제안한 Game of Trees, Radicle, Sourcehut은
작동 방식을 모르니 직접 알아보라는 메모와 함께 덧붙어 있다.

자체 호스팅은 “자신처럼 멋진” 사람이나 조직을 위한 선택지로 소개된다.
저자는 Actions 러너와 릴리스까지 갖춘 Forgejo 자체 호스팅을 권하고,
Forgejo 인스턴스 사이, 그리고 Tangled과의 연합(federation) 논의가 있지만
가까운 시일 안에는 실현되지 않는다고 본다.
공개 협업이 필요하면 사본을 Codeberg에 푸시하라고 하며,
GitLab은 상대적으로 덩치가 크다고 경고한다.
부가 기능이 필요 없다면 SSH 위의 Git만으로도 충분하다며
`git clone user@192.168.1.67:/path/to/repo` 한 줄을 보여 준다.
협업 방식은 별개의 문제라면서도, Linux가 메일링 리스트로 패치를 받아 유지되는데
규모의 논리를 대는 것은 실력 문제라고 받아친다.
결론은 의외로 온건하다.
중앙화된 포지는 괜찮은 타협이고 그것들도 언젠가 GitHub처럼 무너질 수 있으니
항상 탈출 계획을 세워 두라는 것, 그리고 GitHub만 아니면 무엇이든 쓰라는 것이다.

## 분석

### “enshittification” 프레임의 구조

Cory Doctorow가 대중화한 enshittification 개념은 플랫폼이 사용자를 유치한 뒤
비즈니스 고객을 위해 사용자 경험을 희생하고, 결국 플랫폼 자신의 이익을 위해
비즈니스 고객도 착취하는 3단계 가치 훼손 과정을 설명한다.
Bushell은 이 프레임을 GitHub에 적용한다.
GitHub은 개발자 커뮤니티를 먼저 유치했고, Microsoft 인수 이후 기업 기능과
GitHub Actions, Copilot 같은 유료 서비스가 강화됐다.
이제 AI 슬롭이 플랫폼 자체의 신뢰도를 훼손하는 단계라고 볼 수 있다.

### 분산 Git의 잊혀진 속성

Git은 설계상 분산 시스템이다.
Linus Torvalds가 2005년 설계할 때부터 중앙 서버 없이도 완전히 작동하도록
만들었다.
각 복제본은 완전한 히스토리를 포함하고,
임의의 원격 저장소와 직접 통신할 수 있다.
GitHub이 성공하면서 이 분산 속성이 실질적으로 유명무실해진 것은 역설이다.
“Git을 쓴다”가 사실상 “GitHub을 쓴다”와 동의어가 됐다.
Bushell의 글은 이 망각에 대한 저항이다.

### AI 슬롭이 개발 플랫폼에 가져오는 특수한 위험

AI 생성 콘텐츠는 모든 플랫폼을 위협하지만, GitHub에서의 영향은 특히 심각하다.
AI가 생성한 가짜 저장소, 가짜 스타, 봇 기여는 단순히 노이즈를 늘리는 것이 아니라
오픈소스 신뢰 시스템 자체를 무력화한다.
GitHub의 스타 수, 포크 수, 기여자 수는 오랫동안 프로젝트 품질의 사회적 신호였다.
이 신호가 조작 가능해지면 개발자가 라이브러리나 도구를 선택할 때의 판단 근거가
사라진다.
HN에서 tristanj는 GitHub COO가 직접 공개한 수치를 제시했다.
2025년 GitHub은 10억 건의 커밋을 처리했으며, 현재 주당 2억 7500만 건의 커밋이
발생하고 있다.
GitHub Actions 사용량은 2023년 주당 5억 분에서 현재 주당 21억 분으로 4배 이상
급증했다.[^tristanj]
johnfn은 이를 “Microsoft 탓”으로 돌리는 서사에 반박한다.
“AI가 GitHub에 커밋되는 코드 양을 10배로 늘렸고, 이것이 CI, Actions, 코드
인제스천 등 모든 곳에 연쇄 효과를 만들고 있다”는 것이다.[^johnfn]
msyea는 더 구체적인 메커니즘을 지적한다.
부하의 주원인이 Git 푸시 자체가 아니라, AI 코딩 도구들이 GitHub App(OAuth,
PAT, 웹훅)으로 통합되면서 발생하는 API 트래픽이라는 것이다.
그는 직접 GitLab을 선호하지만 특정 AI 기능을 쓰기 위해 GitHub을 써야 했던
경험을 공유했다.[^msyea]

### Forgejo와 AT Protocol의 의미

Forgejo는 Gitea에서 포크된 오픈소스 Git 플랫폼으로,
2022년 Gitea 운영진이 상업적 방향을 선택하면서 커뮤니티 주도 포크가 분리됐다.
이 선택 자체가 오픈소스 거버넌스의 중요성을 보여준다.
Tangled이 AT Protocol을 사용한다는 점은 흥미롭다.
AT Protocol(Authenticated Transfer Protocol)은 Bluesky가 설계한 탈중앙화 소셜
프로토콜로, 계정과 데이터를 특정 서버에 묶지 않는다.
코드 협업에 이 모델을 적용하면, 개발자가 플랫폼을 옮겨도 히스토리와 연결이
유지될 수 있다.

## 비평

### 명료한 구호는 협업이라는 진짜 비용을 비켜 간다

이 글의 가장 강력한 논점은 간결하다.
Git과 GitHub을 분리해 사고하는 것은 기술적으로 자명하지만,
많은 개발자에게는 의식적 환기가 필요하다.
`git clone user@192.168.1.67:/path/to/repo` 한 줄로 논증을 마무리하는 방식은
효과적이다.

그러나 이 한 줄이 해결하는 것은 저장소를 어디에 두느냐뿐이다.
리뷰, 이슈, 권한, 검색, 외부 기여자와의 접점은 그대로 남는다.
저자도 협업은 별개의 문제라고 인정하지만,
Linux 메일링 리스트를 근거로 규모 문제를 실력 문제로 돌리면서 논의를 닫는다.
ninkendo는 자기 회사라면 모든 리뷰를 이메일로 하고, CI 봇이 리뷰용 브랜치를
감시해 결과를 태그로 남기는 저렴한 구성을 꿈꾼다고 적었다.[^ninkendo]
Asooka는 이메일이 교환 프로토콜로는 충분해도, 코멘트가 가리키는 줄과
그 줄의 변경 이력을 오가며 보는 데에는 이메일 클라이언트가 맞지 않는다고
답했다.[^Asooka]
Linux 모델이 통하는 것은 패치 문화에 숙련된 메인테이너 집단이 있기
때문이지, 메일링 리스트가 공짜로 확장되기 때문이 아니다.

GeekNews의 sonnet은 더 냉정했다.
GitHub이 Git이 아니니 떠날 수 있다는 점 말고는 의미 있는 통찰이 없고,
진짜 대안이 필요한 순간에 쓰는 글이라면 왜, 어디로 떠나야 하는지를 더
진지하게 따졌을 것이라는 평가다.[^sonnet]
이 평가는 글의 장르를 정확히 짚는다.
이 글은 이전 가이드가 아니라 선언문이고, 선언문의 설득력은 독자가 이미
품고 있던 불만에 기대고 있다.

### 업타임 차트는 어느 쪽 서사도 지탱하지 못한다

저자는 공식 업타임 차트와 비공식 상태 페이지를 링크했으므로
근거 없이 주장한 것은 아니다.
문제는 그 근거가 무엇을 측정했는지다.
“zero nines of uptime”은 인상적인 표현이지만 과장으로 읽힐 수 있다.
HN에서 n_e는 차트 해석에 의문을 제기했다.
“Microsoft 인수 이전 100% 업타임”이 실제 완벽한 가동률이 아니라
“상태 페이지가 더 정확하게 업데이트되기 시작한 것”일 수 있다고 지적했다.
또한 그래프를 보면 문제가 2020년부터 시작됐으며, 인수 이후 유의미하게 더
나빠진 것으로 보이지 않는다고 반박했다.[^n_e]

이 의심은 스레드에서 구체적인 증거로 이어졌다.
chilmers는 2016년 7월 28일 GitHub 장애가 HN에 올라왔는데도
공식 기록에는 그달 내내 장애가 없다고 나온다는 점을 보여 줬다.[^chilmers]
abraham은 GitHub이 새 상태 페이지를 2018년 12월에 열었고
2018년 10월 이전의 기록은 옮겨지지 않은 것으로 보인다고 짚었다.[^abraham]
starkparker는 차트의 방법론을 직접 확인했다.
데이터가 없는 기간에도 100%를 표시하는 상태 페이지를 그대로 긁었기 때문에,
2019년 11월 정식 출시 전의 GitHub Actions까지 100%로 평균에 들어갔다는
것이다.[^starkparker]
MallocVoidstar는 같은 페이지가 1996년 6월부터 8월까지도 GitHub의 가용률을
100%로 보여 준다고 꼬집었다.[^MallocVoidstar]
인수 전의 초록색 구간은 측정값이 아니라 측정의 부재일 가능성이 크다.

그렇다고 AI 부하 서사가 이기는 것도 아니다.
einsteinx2는 차트의 장애 패턴이 2020년 1월에 시작되는데, 에이전트 코딩은
2024~2025년에야 본격화됐으니 AI로는 그 4년을 설명할 수 없다고
반박했다.[^einsteinx2]
반면 johnfn은 저자가 링크한 비공식 페이지의 월별 기록이 올해 들어 90% 아래,
지난달에는 80% 아래로 떨어졌고 1년 전만 해도 높은 9대였다고
지적했다.[^johnfn-statuses]
최근 몇 달의 악화는 실재하지만, 인수 이후 7년의 추세라는 그림은
기록 방식이 바뀐 효과와 섞여 있다.
GeekNews의 kimjoin2가 제공하는 기능을 생각하면 99% 이상을 뽑아 주는 것이
놀랍다고 적은 것도 같은 지점을 가리킨다.[^kimjoin2]
가용률 숫자는 무엇을 하나의 서비스로 묶어 세느냐에 따라 달라진다.

### 대안 평가는 농담이 대신한다

Codeberg는 긍정적으로, GitLab은 “비대하고 혼란스럽다”고 한 줄로 일축하는 평가는
균형이 맞지 않는다.
GitLab은 CI/CD, 이슈 트래킹, 보안 스캔 통합에서 GitHub보다 뛰어난 면이 있다.
독자가 실제 마이그레이션을 결정하려면 더 상세한 비교가 필요하다.
저자도 이를 의식한 듯 어떤 선택지도 완벽하지 않으니 직접 조사하라는 메모를
나중에 붙였지만, 그것은 비교를 독자에게 넘긴 것이지 비교한 것이 아니다.

HN 반응도 이 한 줄 평가가 농담으로는 통해도 판단 근거로는 약하다는 것을
보여 준다.
tbolt는 GitLab을 회의를 여러 번 해야 고르는 선택지로 묘사한 대목에
웃었지만,[^tbolt]
IshKebab은 GitLab이 GitHub보다 딱히 더 비대하거나 헷갈리지 않으며
엔터프라이즈급을 원하면 Jira를 보라고 반박했다.[^IshKebab]
egwor는 회사에서 GitLab을 쓰면서 승인 버튼이 사실은 메뉴이고
이미 병합된 MR이 할 일 목록에 남는 불편을 겪는 반면,
저자가 강하게 말린 Bitbucket은 신규 입사자도 쉽게 쓸 만큼 단순하다고
적었다.[^egwor]
breakingcups는 이미 GitLab Enterprise를 쓰는 회사에 영업 담당자가 와서
AI 기능을 시연하다가 장애가 나 페이지가 깨졌고, 다음 메이저 버전 전에
떠나야겠다는 신호로 받아들였다고 전했다.[^breakingcups]
대안의 품질은 브랜드 인상보다 각 팀의 사용 패턴에 따라 갈린다.

### 자체 호스팅의 진짜 장벽은 생태계에 있다

저자가 실제로 권하는 것은 중앙화된 다른 포지이고,
Forgejo 자체 호스팅은 여력이 있는 쪽을 위한 선택지로 제시된다.
그래도 그 선택지가 설득력 있으려면 운영 부담을 솔직하게 다뤄야 한다.
서버 유지보수, 백업, 보안 패치, SSH 키 관리는 소규모 팀이나 개인에게 상당한
부담이다.
HN에서 iamkrazy는 실제 Forgejo 자체 호스팅 사례를 공유했다.
홈 서버에 Forgejo를 설치하고 만족스럽게 사용하고 있지만, DigitalOcean App
Platform이나 Vercel 같은 클라우드 플랫폼이 GitHub만 지원한다는 것이 유일한
문제라고 지적했다.[^iamkrazy]
이것은 자체 호스팅의 기술적 장벽이 아니라 생태계 장벽이 더 실질적인 제약임을
보여준다.

cxr는 DigitalOcean이 gitlab.com 호스팅 저장소도 지원하므로,
자체 호스팅 포지가 gitlab.com으로 사본을 복제하게 하면 다리로 쓸 수 있다고
답했다.[^cxr]
이 우회로는 문제를 해결하기보다 드러낸다.
자체 호스팅으로 독립하려던 저장소가 결국 다른 중앙 서비스의 사본을 거쳐서야
배포 생태계에 닿는다.
lawn은 자체 호스팅 Forgejo가 매우 빠르고 만족스럽다고 했지만,
다른 사람의 PR을 몇 개나 받았느냐는 IshKebab의 질문에 하나도 없고
원하지도 않는다고 답했다.[^lawn]
자체 호스팅이 잘 맞는 경우는 바로 협업이 필요 없는 경우라는 점에서,
이 사례는 저자의 권고가 닿는 범위를 정확히 보여 준다.

### 반론: 대안 플랫폼도 AI 슬롭을 피할 수 없다

pelasaco는 글의 낙관적 전제에 이의를 제기했다.
“사람들은 10년이 넘도록 GitHub의 무료 인프라를 불평 없이 썼다.
이제 AI 생성 스팸과 저품질 코드가 비용을 어디서나 높이고 있는데,
GitHub이 비즈니스처럼 행동한다고 나쁜 놈 취급을 받는다”는 것이다.
그는 “오늘의 대안 플랫폼들도 내일이면 저품질 AI 생성 코드에 침수될 것”이라고
덧붙였다.[^pelasaco]
이 반론은 AI 슬롭이 플랫폼의 문제가 아니라 생태계 전반의 문제임을 시사한다.
GitHub에서 Codeberg로 이동해도 오픈소스 커뮤니티 전체가 AI 콘텐츠 품질 문제를
해결하지 않으면 동일한 문제를 맞닥뜨릴 것이다.
aliasxneo도 내일 완벽한 GitHub 대체재가 생긴다 해도 수백만 줄의 AI 생성 코드가
같은 인프라 문제를 일으키지 않을 이유가 무엇이냐고 물었다.[^aliasxneo]

### Microsoft 인수 이후의 개선은 서사에서 지워진다

저자는 인수 이후를 일방적인 쇠퇴로 그리지만, 그 기간에는 사용자에게 유리한
변화도 있었다.
madeofpalk는 인수 석 달 뒤 무료 플랜에 비공개 저장소가 무제한으로 풀렸고,
이듬해 비공개 저장소의 협업자 수 제한도 사라졌으며,
최근 4년간 프로젝트 관리 도구도 크게 나아졌다고 짚었다.[^madeofpalk]
GeekNews의 preserde는 비공개 저장소를 무료로 푼 그 결정을 지금은 후회하고
있을지도 모른다고 적었다.[^preserde]
이 농담은 글이 놓친 연결을 드러낸다.
인수 이후의 관대한 무료 정책이 바로 지금 감당하지 못하는 부하의 바탕이라면,
enshittification 서사와 정반대 방향의 설명이 성립한다.

### 반론: 네트워크 효과는 쉽게 부서지지 않는다

GitHub의 가장 큰 자산은 코드 품질이나 업타임이 아니라 개발자 밀도다.
Pull Request, Issue, Discussion이 연결된 사회적 그래프는 기술 이전이 어렵다.
“GitHub는 싫지만 오픈소스 기여는 거기서 해야 한다”는 딜레마는
플랫폼 품질이 아무리 나빠도 쉽게 해소되지 않는다.
Mastodon이 Twitter의 기술적 대안이 됐어도 주류 마이그레이션이 일어나지 않은
것처럼.
negura는 GitHub이 코드 포지가 아니라 소셜 네트워크라는 것을 깨달은 것이
관점의 전환이었다고 적었고,[^negura]
GeekNews의 iolothebard는 Git 때문에 GitHub을 쓰는 것이 아니라고
짧게 받아쳤다.[^iolothebard]
“Git is not GitHub”는 맞는 말이지만, 사람들이 GitHub에 머무는 이유도
처음부터 Git이 아니었다.

## 인사이트

### 플랫폼 잠금의 새로운 형태: 네트워크가 아닌 관성

전통적인 플랫폼 잠금(lock-in)은 데이터 이동성 문제였다.
당신의 데이터를 내보낼 수 없으면 떠날 수 없다.
GitHub의 경우 이 방정식이 다르다.
Git 저장소 자체는 완전히 이식 가능하다.
코드, 커밋 히스토리, 브랜치를 완벽하게 내보낼 수 있다.
그런데도 개발자들은 떠나지 않는다.

잠금의 실체는 사회적 그래프다.
GitHub 프로필에 쌓인 기여 기록, 팔로워, 연결된 이슈와 PR, 다른 프로젝트와의
교차 참조, 그리고 “GitHub 주소”로 통용되는 개발자 정체성이 진짜 전환 비용이다.
Bushell이 “Git is not GitHub”를 반복해서 강조하는 것은 이 심리적 잠금에 대한
저항이다.
기술적으로 자유롭다는 사실을 잊지 말라는 상기다.
iamkrazy의 경험은 잠금의 세 번째 층을 드러낸다.
코드와 사회적 그래프를 옮기더라도, AI 코딩 도구·클라우드 배포 플랫폼·CI 서비스가
GitHub만 지원하는 한 실질적인 이탈은 불가능하다.
이것은 데이터 잠금이나 사회적 잠금과 달리 생태계 잠금(ecosystem lock-in)이다.
파트너 서비스들이 GitHub을 유일한 표준으로 선택하는 한, 자체 호스팅조차 완전한
독립이 아니다.

역사적으로 이 패턴은 이메일과 비슷하다.
이메일은 분산 프로토콜이고, 어느 서비스든 이동 가능하다.
그러나 대부분의 사람은 Gmail에 머문다.
프로토콜의 개방성이 플랫폼 지배를 막지 못한다.
GitHub도 같은 구조다.
Git이 아무리 분산적이어도, 개발자의 집은 github.com이다.

### AI 슬롭과 오픈소스 신뢰의 붕괴

오픈소스 생태계는 신뢰 기반 시스템이다.
라이브러리의 스타 수, 최근 커밋 날짜, 기여자 수, 이슈 응답 속도가
프로젝트 건강도를 판단하는 사회적 신호였다.
이 신호들은 수십 년간 쌓인 집단 지성의 산물이다.

AI 슬롭은 이 신호 체계를 조작한다.
자동화된 스타 구매, AI가 생성한 가짜 커밋, 봇이 작성한 이슈와 PR이
신호를 오염시킨다.
문제는 오염된 신호와 진짜 신호를 구별하는 비용이 급격히 높아진다는 것이다.
과거에는 “스타 1000개 이상, 최근 6개월 내 커밋, 활성 이슈 대화”가
충분한 신뢰 기준이었다.
이제는 이 기준이 무너졌다.

더 깊은 문제는 이 신뢰 붕괴가 AI 훈련 데이터에도 영향을 준다는 점이다.
코드 생성 AI는 GitHub의 고품질 코드를 학습했다.
AI 슬롭이 저장소를 채우면, 미래의 코드 AI는 AI가 생성한 저품질 코드로
훈련받는다.
이것은 데이터 품질의 악순환이다.
GitHub의 콘텐츠 품질 하락은 단순히 검색 경험의 문제가 아니라,
소프트웨어 생태계 전반의 품질 하락과 연결된다.

### 무제한 요금제가 부하의 모양을 정한다

AI가 부하를 늘렸다는 설명과 Microsoft가 무능하다는 설명은 둘 다
요금 구조라는 세 번째 변수를 빠뜨린다.
ncruces는 GitHub이 공개한 수치에서 10배씩 늘어난 항목이 저장소, 커밋, PR처럼
유료 고객에게도 사실상 무제한인 것들이고,
Actions 분처럼 사용량 과금이 붙은 항목은 2배 안팎으로만 늘었다고
짚었다.[^ncruces]
값이 붙으면 사람들은 10배로 쓰지 않는다는 것이다.

georgemcbay는 같은 문제를 수익 쪽에서 봤다.
AI가 인프라 비용을 10배로 늘려도 수익이 10배가 되지 않는다면,
기술적으로 풀 수 있는 문제라도 경제적으로 풀릴 보장은 없다.
무료 등급은 유료 등급을 위한 미끼인데, 늘어난 사용량은 대부분 무료 등급이나
사용자당 정액 요금 안에서 발생한다는 것이다.[^georgemcbay]
Twitter의 실패 고래 시절과 달리 사용량 증가가 곧 광고 수익 증가로 이어지는
구조도 아니다.

이 관점은 저자의 처방에도 그림자를 드리운다.
Codeberg 같은 비영리 포지는 GitHub보다 더 관대하고 더 가난하다.
에이전트가 쉬지 않고 커밋하는 시대에 무제한 무료 저장소라는 약속은
운영 주체가 영리든 비영리든 비용 구조를 버티기 어렵다.
결국 대안 포지들도 사용량 한도, 로그인 장벽, 유료 등급 중 하나를 고르게 될
것이고, GitHub 이탈은 이 선택을 미루는 효과에 그칠 수 있다.

### 단일 실패 지점으로서의 GitHub: 오픈소스의 구조적 취약성

GitHub는 전 세계 오픈소스 인프라의 단일 실패 지점이 됐다.
GitHub이 멈추면 Actions에 묶인 CI/CD 파이프라인이 멈추고,
GitHub에서 의존성을 직접 받아 오는 빌드도 함께 멈춘다.
하나의 상업 서비스가 이런 수준의 인프라 권력을 갖는 것은 위험하다.

이 의존은 장애가 없을 때에도 비용을 만든다.
oarsinsync는 로그인하지 않은 채 커밋 기록을 보려다 2차 속도 제한에 걸렸는데,
그 네트워크에서 GitHub을 보는 사람은 자기 하나뿐이었다고 적었다.[^oarsinsync]
blinded는 사이트를 제대로 보려면 로그인하는 수밖에 없다고 했고,[^blinded]
Asooka는 그렇게 인증 장벽이 높아지면 GitHub에서 패키지를 기본으로 받아 오는
Go 같은 빌드 시스템이 깨지지 않느냐고 물었다.[^Asooka-builds]
chrisandchris는 CI의 `nuget restore`가 401로 실패했다가 몇 초 뒤 재시도하면
성공하는 일을 셀 수 없이 겪었다고 답했다.[^chrisandchris]
부하를 막으려는 방어 장치가 공개 저장소라는 GitHub의 원래 약속을 조금씩
깎아 내고 있다.

이 구조는 오픈소스 운동의 원래 정신과 모순된다.
오픈소스는 탈중앙화와 자율성을 추구했다.
그런데 오픈소스 생태계 전체가 Microsoft가 소유한 하나의 플랫폼에 의존한다.
Linux Foundation, Apache Software Foundation 같은 비영리 재단들이
인프라를 직접 운영하는 것처럼, 오픈소스 코드 협업 인프라도 커뮤니티 소유가
되어야 한다는 논쟁이 다시 힘을 얻고 있다.
Codeberg가 비영리 모델로 운영되는 것은 이 필요에 대한 응답이다.

GitHub이 완전히 가라앉지는 않겠지만, 개발자들이 대안을 진지하게 탐색하기
시작했다는 사실 자체가 변화의 신호다.
플랫폼 권력은 사용자가 대안을 인식하는 순간부터 약해진다.

### Forgejo·AT Protocol이 가리키는 탈중앙화의 재부상

2010년대는 중앙화의 시대였다.
AWS, GitHub, Google이 인프라의 중심이 됐다.
편의성이 자율성을 압도했다.
그러나 2020년대 중반부터 탈중앙화가 다시 논의되고 있다.
Mastodon, Bluesky, Forgejo 연합이 그 흐름이다.

Forgejo 인스턴스 간 연합(federation)이 구현되면, 개발자는 특정 서버에 묶이지
않고도 다른 인스턴스의 프로젝트에 기여하고 이슈를 열 수 있다.
이메일이 gmail.com과 outlook.com 사이에서 자유롭게 오가는 것처럼,
코드 협업도 서버 간 경계가 사라질 수 있다.
이것이 실현되면 “GitHub을 써야 오픈소스에 기여할 수 있다”는 전제가 무너진다.

Tangled의 AT Protocol 채택은 더 급진적인 방향이다.
AT Protocol은 계정을 서버가 아니라 개인이 소유하도록 설계됐다.
개발자 정체성, 기여 기록, 네트워크가 플랫폼에 귀속되지 않고 개발자 자신에게
귀속된다면, 플랫폼 이동의 전환 비용이 근본적으로 낮아진다.
이것은 GitHub 잠금의 핵심인 “사회적 그래프 포착”을 해체하는 접근이다.
아직 알파 단계지만, 방향 자체는 오픈소스 생태계가 오랫동안 필요로 했던 것이다.

---

[^tristanj]: <https://news.ycombinator.com/item?id=48088846>

[^johnfn]: <https://news.ycombinator.com/item?id=48085542>

[^msyea]: <https://news.ycombinator.com/item?id=48088032>

[^n_e]: <https://news.ycombinator.com/item?id=48085703>

[^iamkrazy]: <https://news.ycombinator.com/item?id=48085567>

[^pelasaco]: <https://news.ycombinator.com/item?id=48087405>

[^ninkendo]: <https://news.ycombinator.com/item?id=48087738>

[^Asooka]: <https://news.ycombinator.com/item?id=48088075>

[^chilmers]: <https://news.ycombinator.com/item?id=48086786>

[^abraham]: <https://news.ycombinator.com/item?id=48089196>

[^starkparker]: <https://news.ycombinator.com/item?id=48089270>

[^MallocVoidstar]: <https://news.ycombinator.com/item?id=48087142>

[^einsteinx2]: <https://news.ycombinator.com/item?id=48086312>

[^johnfn-statuses]: <https://news.ycombinator.com/item?id=48086364>

[^tbolt]: <https://news.ycombinator.com/item?id=48085478>

[^IshKebab]: <https://news.ycombinator.com/item?id=48087509>

[^egwor]: <https://news.ycombinator.com/item?id=48086028>

[^breakingcups]: <https://news.ycombinator.com/item?id=48151665>

[^cxr]: <https://news.ycombinator.com/item?id=48087151>

[^lawn]: <https://news.ycombinator.com/item?id=48090981>

[^aliasxneo]: <https://news.ycombinator.com/item?id=48085602>

[^madeofpalk]: <https://news.ycombinator.com/item?id=48085791>

[^negura]: <https://news.ycombinator.com/item?id=48088796>

[^ncruces]: <https://news.ycombinator.com/item?id=48088166>

[^georgemcbay]: <https://news.ycombinator.com/item?id=48086214>

[^oarsinsync]: <https://news.ycombinator.com/item?id=48085461>

[^blinded]: <https://news.ycombinator.com/item?id=48085492>

[^Asooka-builds]: <https://news.ycombinator.com/item?id=48088042>

[^chrisandchris]: <https://news.ycombinator.com/item?id=48088226>

[^sonnet]: <https://news.hada.io/topic?id=29405#cid57496>

[^kimjoin2]: <https://news.hada.io/topic?id=29405#cid57280>

[^preserde]: <https://news.hada.io/topic?id=29405#cid57405>

[^iolothebard]: <https://news.hada.io/topic?id=29405#cid57340>
