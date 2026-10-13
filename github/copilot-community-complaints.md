# 끌 수 없는 Copilot, GitHub 사용자들의 불만은 계속된다

원문: [GitHub Copilot on autopilot as community complaints persist](https://www.theregister.com/software/2025/09/05/github-copilot-on-autopilot-as-community-complaints-persist/599985)

HN 토론: <https://news.ycombinator.com/item?id=45148167> (421점, 302개 댓글)

GN 토론: <https://news.hada.io/topic?id=22944>

## 요약

The Register의 Thomas Claburn이 2025년 9월 5일에 쓴 기사다.
GitHub 커뮤니티 토론 게시판에서 지난 12개월 동안 추천을 가장 많이 받은 글은
Copilot이 저장소에 이슈와 풀 리퀘스트를 만들지 못하게 막을 방법을 달라는
요청이었다.
두 번째는 Copilot 코드 리뷰를 끌 수 없다는 버그 리포트였다.
첫 글은 5월에, 두 번째 글은 한 달 전에 열렸지만 둘 다 GitHub의 답이 없다.

첫 요청을 올린 개발자 Andi McClure는 1월에도 VS Code 저장소에 비슷한 이슈를
올렸다.
Copilot 확장을 지웠는데도 Copilot 아이콘이 다시 나타난다는 내용이었다.
기사는 Microsoft와 GitHub가 상당수 고객이 원하지 않는 기술에 전부를 걸었고,
막대한 설비 투자를 회수해야 하므로 이를 피하기 어렵게 만든다고 본다.
그 반대편에는 7월 30일 실적 발표에서 Satya Nadella가 밝힌 숫자가 있다.
GitHub Copilot 사용자는 2,000만 명이고, Copilot Enterprise 고객은 직전 분기보다
75% 늘었다.

McClure는 Copilot이 자신의 코드를 라이선스를 어기고 학습한 것처럼 보이는데,
그 위에 자신이 쓰지 않을 제품의 사실상 광고까지 봐야 한다는 점에 분개한다.
기사는 반발의 근거를 넓게 늘어놓는다.
curl 메인테이너 Daniel Stenberg가 겪는 AI 슬롭 대응 부담, 추측을 사실처럼
되풀이하는 생성형 AI, Copilot 제안 코드가 출처 표기 의무가 있는 코드를 그대로
재현해도 책임지지 않는 GitHub의 약관이다.
Servo는 정확성 보장 부재, 저작권, 윤리를 이유로 AI 코드 기여를 금지했고,
GNOME Loupe, FreeBSD, Gentoo, NetBSD, QEMU도 비슷한 금지를 두었다.

McClure는 몇 년째 Copilot 거부 요청을 올려 왔는데, 최근 6개월 사이 지지가 눈에
띄게 늘었다고 말한다.
Microsoft가 Copilot을 인터페이스 곳곳에 밀어 넣다가 올해 어느 시점에 사람들이
더는 무시하지 않는 변곡점을 넘었다는 것이다.
또 한 달 사이 GitHub가 독립 자회사에서 Microsoft CoreAI 조직의 일부로 격하된
일이 상징적이지만 결정적인 계기였다고 본다.
불평에 그치던 오픈소스 커뮤니티가 실제로 Codeberg나 자체 호스팅 Forgejo로
옮기기 시작했다는 것이다.
Software Freedom Conservancy가 2022년에 GitHub를 떠나자고 호소한 일도 함께
언급된다.

McClure 자신은 저장소를 고칠 때마다 Codeberg에 복제해 변경을 올리고, GitHub
쪽 main 브랜치는 이전 안내문으로 바꾸는 식으로 천천히 옮기고 있다.
그는 Microsoft가 기본값으로 켠 기능에 끄기 스위치를 달아 두고, 여섯 달 뒤 기능
이름을 살짝 바꿔 새 스위치를 또 끄게 만든다고 비판한다.
Windows 10의 Bing과 Cortana에서 그랬듯 이번에도 끄는 것만으로는 부족하며,
Copilot이 들어간 Microsoft 제품을 아예 쓰지 않는 길밖에 없다는 것이 그의
결론이다.
다만 GitHub와 VS Code는 네트워크 효과 때문에 Windows보다도 강한 독점이라
아직 버리지 못했다고 인정한다.
GitHub는 논평 요청에 답하지 않았다.

## 분석

### 기사의 증거는 추천 수 순위다

기사의 출발점은 GitHub 커뮤니티 토론에서 추천을 가장 많이 받은 글 두 개다.
사용 통계나 이탈 수치가 아니라 불만 게시판의 인기 순위가 증거다.
이 순위는 분노의 강도를 보여 주지만 분노한 사람의 수가 전체 사용자 중 얼마인지는
말해 주지 않는다.
기사가 대비시키는 Nadella의 2,000만 사용자 숫자와는 측정 단위부터 다르다.

그래서 기사는 수치 대결이 아니라 한 개발자의 서사로 짜여 있다.
McClure의 이슈, 이메일 인터뷰, 이전 방식, Microsoft에 대한 해석이 기사 분량의
대부분을 차지한다.
여기에 Servo와 BSD 계열의 AI 기여 금지, SFC의 GitHub 탈퇴 운동을 엮어
개인의 불만을 공동체의 흐름으로 확장한다.
이 확장이 정당한지는 비평에서 따로 다룬다.

### 강제 노출과 사용자 지표는 같은 동전의 양면이다

기사가 이름 붙이지는 않지만 실제로 짚는 구조는 지표와 노출의 순환이다.
Copilot이 화면 곳곳에 기본으로 켜져 있을수록 Copilot 사용자 수는 커진다.
WhyNotHugo는 끌 수 없게 밀어 넣은 기능의 사용자 수는 의미 없는 지표라며,
자신도 매달 Copilot 접근 권한이 갱신됐다는 메일을 받으니 2,000만 명에
포함됐을 것이라고 적었다.[^WhyNotHugo]
jonp888은 소프트웨어 경력이 없는 고위 관리자의 지시로 부서 개발자 전원이
Copilot을 구독하지만 아무도 쓰지 않는다고 전했다.[^jonp888]
자체 컴파일러와 운영체제를 쓰는 임베디드 팀이라 쓸 일이 없는데도 1인당 연
240달러가 나간다는 것이다.

marginalia_nu는 이 구조를 한 줄로 요약했다.
CEO가 AI 참여도를 올리라고 하면 조직은 AI 참여도를 올린다.[^marginalia_nu]
mrandish도 강제 기능은 내부 사용 지표를 끌어올리려는 잘못된 시도라고
봤다.[^mrandish]
이 관점에서 보면 McClure가 말한 스위치 이름 바꾸기는 우연한 UX 실수가 아니라
지표를 지키는 장치다.
끄기를 어렵게 만들수록 지표는 좋아 보이고, 지표가 좋을수록 노출을 줄일
이유는 사라진다.

### 10배 생산성과 강매는 함께 성립하기 어렵다

AlexandrB는 이 기사가 드러내는 모순을 짚었다.
AI가 생산성을 10배 높여 주는 마법 같은 도구라면 사람들이 알아서 문을 두드릴
텐데, 왜 회사는 그것을 사방에서 들이밀고 때로는 사용을 강제하는가.[^AlexandrB]
hyperpape는 Dan Luu의 2015년 글을 인용해 반박했다.
버전 관리조차 도입하는 데 몇 달씩 싸워야 했던 팀이 있었다며, 좋은 아이디어가
빨리 이긴다고 가정할 수는 없다는 것이다.[^hyperpape]

이 반박에 dcminter는 중요한 차이를 덧붙였다.
조직 안에서 AI를 쓰라는 압력은 위에서 내려오는데, 유용했던 도구들은
대개 모험적인 개발자에게서 바깥으로 퍼져 나갔다는 것이다.[^dcminter]
버전 관리는 현장이 밀어붙이고 경영이 버텼지만, Copilot은 경영이 밀어붙이고
현장이 버틴다.
기사가 McClure의 입을 빌려 Copilot 추진이 완전히 하향식으로 보인다고 한 것도
같은 관찰이다.

### 떠날 수 없는 이유는 저장소가 아니라 그 주변에 있다

McClure는 GitHub를 Windows보다 강한 독점이라고 부르면서 근거로 네트워크
효과를 든다.
HN 토론은 그 네트워크 효과를 더 구체적으로 분해했다.
benrutter는 GitHub 관성의 숨은 무기가 스타라고 봤다.
많은 사람이 스타를 프로젝트 성숙도의 신호로 읽기 때문에, 스타가 사라지면
다른 포지로 옮기려는 사람이 훨씬 많아질 것이라는 추측이다.[^benrutter]
IshKebab은 더 중요한 무기로 이미 모두가 가진 계정과 무료 CI, 특히 무료 Mac과
Windows CI를 꼽았다.[^IshKebab-ci]
wiether는 무료 Actions 시간 2,000분과,
사실상 무제한으로 쓰이는 패키지 레지스트리를 더했다.[^wiether]

이 목록은 기사에 없는 축을 드러낸다.
McClure가 말하는 탈출은 코드 저장소의 이전이지만, 사람들을 붙잡는 것은 코드가
아니라 계정, 평판 신호, 무료 연산 자원이다.
Codeberg는 저장소를 받아 줄 수 있어도 무료 macOS 빌드 머신까지 대신 내주지는
못한다.

## 비평

### 기사의 첫 문장이 문제를 실제보다 크게 그린다

기사는 가장 인기 있는 토론이 Copilot의 이슈와 PR 생성을 막아 달라는
요청이라고 쓰고, HN 제목은 이를 강제 Copilot 기능에 대한 분노로 요약했다.
읽는 사람은 Copilot이 남의 저장소에 스스로 이슈와 PR을 만든다고 받아들이기
쉽다.
IshKebab은 이를 정면으로 반박했다.
Microsoft가 이슈와 PR을 자동으로 만드는 것이 아니라 사용자가 직접 실행해야
한다는 것이다.[^IshKebab]
요청자의 가장 인기 있는 저장소에도 PR이 3개뿐이고 Copilot PR은 없었으며,
훨씬 큰 Rust 컴파일러 저장소에서도 Copilot PR은 찾지 못했다고 적었다.

같은 증언이 이어졌다.
oefrha는 요청자보다 인기 있는 프로젝트들을 관리하지만 Copilot 이슈나 PR을
한 번도 받은 적이 없다고 했다.[^oefrha]
Copilot 에이전트 PR은 돈이 들고 ChatGPT나 Gemini 복사는 공짜이니, 막아야 할
대상이 Copilot만은 아니라는 지적도 덧붙였다.
zzzeek도 여러 유명 오픈소스 프로젝트를 GitHub에서 운영하지만 AI가 만든 이슈나
PR, 자동 AI 코드 리뷰를 본 적이 없다며 이것이 실제 문제인지 물었다.[^zzzeek]
결국 첫 번째 요청의 실체는 Copilot이라는 계정이 만든 기여를 차단할 수단이
없다는 것, 즉 다른 사람이 Copilot을 써서 보낸 기여를 거부할 수단이 없다는
것에 가깝다.

이 구분은 사소하지 않다.
GitHub가 기여자의 도구 선택을 막아 달라는 요구와 GitHub가 내 저장소에 기능을
강제한다는 주장은 해법도 책임 소재도 다르다.
기사는 앞의 요구를 뒤의 주장처럼 들리게 배치했다.

### 분노의 근거가 서로 다른 층위에서 섞여 있다

기사는 한 문단 안에서 AI 슬롭 대응 부담, 학습 데이터의 라이선스 위반 의혹,
제안 코드에 대한 GitHub의 면책, UI에 붙은 광고성 버튼을 나란히 놓는다.
첫째는 개방형 기여 시스템의 운영 문제이고, 둘째와 셋째는 법적 문제이며,
넷째는 제품 설계 문제다.
이 넷은 서로 다른 해법을 요구하는데, 기사는 이를 Copilot이라는 이름 아래
하나의 분노로 묶는다.

GN의 ndrgrd는 첫째 층위를 분리해서 봤다.
AI가 성의 없는 기여를 너무 쉽게 만드는 것이 문제이긴 하지만, 성의 없는
피드백으로 메인테이너를 지치게 하는 일 자체는 원래 열린 이슈/PR 시스템의
문제라는 것이다.[^ndrgrd]
중복되고 성의 없는 이슈 때문에 지쳐 가는 1인 메인테이너는 AI 이전에도
있었다.
madeofpalk도 2025년에 온라인 텍스트 상자를 관리하면 어떤 식으로든 AI 슬롭을
상대해야 하며, 그게 싫으면 상자를 닫으라고 했다.[^madeofpalk]
Copilot을 차단해도 이 층위의 문제는 거의 그대로 남는다.

반대로 제품 설계 층위의 불만은 기사보다 현장 증언이 더 구체적이다.
agilob은 Copilot이 문서 오타 수준의 리뷰 코멘트를 남기고, 그 코멘트가 PR 자동
병합을 막아서 직접 들어가 해결 처리를 해야 한다고 적었다.[^agilob]
3np는 설정 페이지에는 Copilot 기능이 꺼져 있다고 나오는데, 로그인한 페이지의
소스에 든 기능 플래그 JSON에는 Copilot이 켜진 것으로 나온다고 증언했다.[^3np]
몇 달째 지원 티켓을 열었지만 엔지니어링 팀에 넘겼다는 답과 함께 닫히기를
되풀이한다는 것이다.
기사가 이런 구체적 결함을 중심에 두었다면 논지가 훨씬 단단했을 것이다.

### 이탈의 증거는 의향이지 이동이 아니다

기사는 CoreAI 편입 뒤 커뮤니티가 불평에서 이탈로 넘어갔다고 쓰지만, 근거는
McClure의 지인들이 이전을 이야기한다는 전언과 스레드에 남은 떠나겠다는
댓글이다.
Codeberg 가입자 증가나 이전된 저장소 수 같은 수치는 없다.
떠나겠다는 선언은 언제나 실제 이동보다 많다.

daemin은 이 기사를 Codeberg 공식 계정이 소셜 미디어에 공유한 것을 보고 읽었다며,
셀프 호스팅은 언급하지 않고 다른 호스팅 플랫폼으로의 이전만 다루니 홍보성
기사처럼 느껴졌다고 했다.[^daemin]
이 평가가 공정한지와 별개로,
기사가 제시하는 탈출구가 Codeberg와 Forgejo 둘뿐이라는 점은 사실이다.
GitLab, SourceHut, 사내 서버 같은 다른 선택지와 그 비용은 비교되지 않는다.

McClure 자신의 이전 방식도 기사가 말하는 대이동과는 거리가 있다.
저장소를 고칠 일이 생길 때마다 하나씩 옮기는 방식이고, VS Code와 GitHub는
네트워크 효과 때문에 계속 쓴다고 스스로 인정한다.
가장 결연한 반대자조차 완전히 떠나지 못한다는 사실은 기사의 결론보다
McClure가 말한 독점 쪽을 더 강하게 뒷받침한다.

## 인사이트

### 끄기 스위치의 이름을 바꾸는 패턴은 동의를 소모품으로 만든다

McClure가 묘사한 패턴은 기본값으로 켜고, 끄기 스위치를 달고, 여섯 달 뒤 이름을
바꿔 새 스위치를 다시 끄게 만드는 것이다.
이것이 반복되면 사용자의 거부는 한 번 내리면 유지되는 결정이 아니라 주기적으로
갱신해야 하는 구독이 된다.
거부를 유지하는 비용이 사용자에게 계속 청구되는 구조다.

이 패턴의 2차 효과는 사용자가 개별 기능을 평가하지 않게 된다는 점이다.
스위치를 믿을 수 없게 되면 합리적인 대응은 기능 단위의 선택이 아니라 제품
단위의 이탈이다.
McClure가 SwiftKey를 지우고 Windows에서 Linux로 옮긴 것이 바로 그 경로다.
Copilot 하나를 끄고 싶었던 사람이 Microsoft 제품군 전체를 떠나는 결과로
이어진다.

jsheard는 같은 패턴이 GitHub 밖에서 이미 돈의 문제로 번졌다고 지적했다.
Microsoft는 개인과 가족 Office 구독자 전원을 30~40% 비싼 AI 포함 요금제로
일방적으로 바꾸고, 예전 요금제로 돌아가는 선택지는 구독 해지를 시도할 때만
마지막 수단으로 보여 준다는 것이다.[^jsheard]
GitHub의 끄기 스위치 문제는 이 흐름의 개발자판일 뿐이다.

### 소셜 네트워크가 된 코드 호스팅은 SourceForge의 길을 반복할 수 있다

HN 토론에서는 SourceForge가 반복해서 소환됐다.
apelapan은 SourceForge가 이미 내리막이던 중에 배포 바이너리에 애드웨어를 끼워
넣자 절벽처럼 추락했다고 회상했다.[^apelapan]
한때 오픈소스의 기본 거처였던 플랫폼이 사용자의 결과물에 원치 않는 것을 끼워
넣는 순간 신뢰가 무너진 사례다.

Copilot의 강제 노출은 그 정도의 배신은 아니지만 구조가 닮았다.
플랫폼이 사용자의 작업물 위에 자기 사업을 얹는다는 점이다.
차이는 GitHub가 SourceForge보다 훨씬 많은 것을 쥐고 있다는 데 있다.
계정, 스타, CI, 패키지 레지스트리가 함께 묶여 있어서, 신뢰가 떨어져도
SourceForge처럼 절벽에서 떨어지기보다는 천천히 가라앉을 가능성이 높다.
천천히 가라앉는 플랫폼은 문제를 고칠 압력도 천천히 받는다.

### 메인테이너가 원하는 것은 Copilot 차단이 아니라 기여 필터다

첫 번째 요청의 실체가 Copilot 계정을 막는 수단이라면, 그 요청은 더 큰 요구의
한 조각이다.
throwaway94876은 AI 슬롭을 보내는 사람을 공동 차단 목록에 올리자고 제안했다.
그들은 Copilot 통합이 있든 없든 슬롭을 보낼 것이기 때문이다.[^throwaway94876]
문제의 단위는 도구가 아니라 기여자이고, 필요한 것은 기여를 걸러낼 수 있는
저장소 쪽의 권한이다.

GitHub 입장에서 이 요구는 곤란하다.
Copilot이 만든 기여를 쉽게 거를 수 있게 하면 Copilot 에이전트의 가치가
떨어지고, 거르지 못하게 하면 메인테이너의 신뢰가 떨어진다.
기사 속 두 토론이 1년 가까이 답을 받지 못한 이유를 무관심이 아니라 이
상충에서 찾을 수도 있다.
GitHub가 어느 쪽으로 답하느냐가 개발자 플랫폼과 AI 유통 채널 중 무엇을 먼저
두는지를 보여 줄 것이다.

### 개인 사용자의 방어 수단은 결국 클라이언트 쪽에 남는다

플랫폼이 끄기 스위치를 믿을 수 없게 만들면 사용자는 클라이언트에서 막기
시작한다.
tech234a는 웹에서 파일을 편집할 때 나오는 Copilot 커밋 메시지 제안이 거슬려
uBlock Origin 필터로 해당 API 요청을 막았다.[^tech234a]

```text
||api.individual.githubcopilot.com/agents/github-commit-message-generation$xhr,domain=github.com
```

VS Code에서는 RossBencina가 알려 준 대로 명령 팔레트의 Chat: Hide AI Features로
AI 기능을 숨길 수 있다.[^RossBencina]
이런 우회는 당장은 효과가 있지만, 엔드포인트 이름이나 명령 이름이 바뀌면 다시
깨진다.
McClure가 말한 스위치 이름 바꾸기와 같은 술래잡기가 사용자 쪽으로 옮겨 올
뿐이다.
조직 단위로 GitHub를 쓰는 팀이라면 이런 개인 우회보다 조직 정책에서 Copilot
기능을 끄고, 그 설정이 실제로 적용되는지 정기적으로 확인하는 편이 낫다.

---

[^WhyNotHugo]: <https://news.ycombinator.com/item?id=45148605>

[^jonp888]: <https://news.ycombinator.com/item?id=45157714>

[^marginalia_nu]: <https://news.ycombinator.com/item?id=45149323>

[^mrandish]: <https://news.ycombinator.com/item?id=45151772>

[^AlexandrB]: <https://news.ycombinator.com/item?id=45149045>

[^hyperpape]: <https://news.ycombinator.com/item?id=45149336>

[^dcminter]: <https://news.ycombinator.com/item?id=45149737>

[^benrutter]: <https://news.ycombinator.com/item?id=45149176>

[^IshKebab-ci]: <https://news.ycombinator.com/item?id=45150052>

[^wiether]: <https://news.ycombinator.com/item?id=45150647>

[^IshKebab]: <https://news.ycombinator.com/item?id=45148561>

[^oefrha]: <https://news.ycombinator.com/item?id=45149080>

[^zzzeek]: <https://news.ycombinator.com/item?id=45149387>

[^ndrgrd]: <https://news.hada.io/topic?id=22944#cid43469>

[^madeofpalk]: <https://news.ycombinator.com/item?id=45148916>

[^agilob]: <https://news.ycombinator.com/item?id=45150256>

[^3np]: <https://news.ycombinator.com/item?id=45149187>

[^daemin]: <https://news.ycombinator.com/item?id=45148935>

[^jsheard]: <https://news.ycombinator.com/item?id=45149891>

[^apelapan]: <https://news.ycombinator.com/item?id=45151351>

[^throwaway94876]: <https://news.ycombinator.com/item?id=45149338>

[^tech234a]: <https://news.ycombinator.com/item?id=45177385>

[^RossBencina]: <https://news.ycombinator.com/item?id=45148531>
