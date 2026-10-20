# Linux 7.3은 커밋 수와 개발자 수에서 기록을 세웠지만 그 숫자가 무엇을 뜻하는지는 아무도 모른다

원문: [The 7.3 kernel has been released \[LWN.net\]](https://lwn.net/Articles/1101143/)

HN 토론: <https://news.ycombinator.com/item?id=50149392> (592점, 276개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/4oz3sk/7_3_kernel_has_been_released> (18점, 2개 댓글)

GN 토론: <https://news.hada.io/topic?id=35635>

## 요약

LWN의 corbet은 2026년 10월 18일 짧은 소식으로
Linus Torvalds가 예정대로 7.3 커널을 공개했다고 전한다.
Torvalds는 릴리스 공지에서 이번 주는 요일을 잊지 않고 챙겨서
릴리스가 무작위로 미뤄지지 않았다고 농담하고 특별한 일이 없어서
예정대로 최종 7.3이 나왔으며 다음 날 7.4의 병합 창이 열린다고 썼다.
다만 연례 가족 휴가 중이어서 첫날 아침에 바로 병합하지 못하고
하루 대부분을 배 위와 물속에서 보낸 뒤 오후에 병합에 돌아올 것이며,
한동안 일정이 평소와 다를 것이라고 덧붙였다.

LWN은 이 릴리스가 모든 면에서 기록을 깼다고 쓴다.
병합 커밋을 제외하고 18,765개의 커밋이 3,021명의 개발자에게서 들어왔고,
그중 807명이 커널에 처음 기여한 사람이다.
주요 변경으로는 `binfmt_misc`의 큰 확장,
큰 시스템의 성능을 겨냥한 그룹 스케줄링 작업,
모든 연산이 실패하는 새 파일 시스템 failfs, `fchroot()` 시스템 호출,
BPF 프로그램용 전역 CPU별 데이터, `sched_ext` 서브스케줄러 기능의 완성,
가상 머신의 워킹셋 추적, ntfs3의 대체 데이터 스트림 지원,
긴 목록의 SMB 서버 개선을 든다.
세부 내용은 LWN의 병합 창 요약과 KernelNewbies의 7.3 페이지에서
볼 수 있다고 안내한다.

## 분석

### 이 소식에서 확인되는 것은 규모의 숫자 하나뿐이다

글이 주는 구체적인 사실은 세 개의 숫자다.
커밋 18,765개, 개발자 3,021명, 첫 기여자 807명이다.
변경 목록은 이름만 나열되고
어떤 것이 왜 중요한지는 말하지 않으며 병합 창 요약으로 넘긴다.
소식의 역할이 릴리스가 나왔다는 알림과 숫자를 전달하는 것이므로
분석이 아니라 안내에 가깝다.

기록을 깼다는 판단은 LWN의 것이고
비교의 기준이 직전 릴리스인지 역대 전체인지는 글에 없다.
이 저장소에는 7.2의 개발 통계를 다룬 문서가 따로 있어서
이번 릴리스의 개발 통계가 나오면 비교할 수 있다.

### 변경 목록에서 보이는 방향은 격리와 대형 시스템이다

변경 목록을 묶어 보면 두 가지 방향이 보인다.
하나는 격리와 샌드박싱이다.
모든 연산이 실패하는 failfs와 `fchroot()` 시스템 호출이 여기에 속한다.
다른 하나는 큰 시스템과 확장 가능한 스케줄링이다.
그룹 스케줄링 작업과 `sched_ext` 서브스케줄러의
완성과 BPF의 전역 CPU별 데이터가 그렇다.

이 묶음은 이 문서의 읽기이고 LWN이 그렇게 말하지는 않는다.
다만 독자의 댓글이 격리 쪽의 구체적인 용도를 채워 준다.
HN의 saint-evan은 failfs가 모든 경로 조회가 실패하는 의사 파일 시스템이어서
정적 링크된 프로세스를 이미 열려 있는 파일 디스크립터만 가진 채 failfs 안에 넣고
불필요한 소켓을 닫으면
침해된 애플리케이션이 로컬 파일에 접근하거나 셸을 띄울 수 없다고
설명했다.[^saint-evan] rwmj는 failfs로 chroot한 프로세스가 새 파일을 열 수 없고
이미 열린 파일 디스크립터 집합으로만 제한된다고
썼고,[^rwmj] roryirvine는 chroot 탈출을 막는 데 도움이 된다고
LWN의 병합 창 요약을 가리켰다.[^roryirvine]
Lobste.rs에서
fzakaria는 failfs 변경이 Nix 핵심 기여자 John Ericsson이 낸
널 네임스페이스에 대한 RFC에서 나왔다고 알렸다.[^fzakaria]

## 비평

### 기록적인 숫자는 품질에 대해 아무것도 말하지 않는다

글은 커밋 수와 개발자 수를 기록으로 제시하지만
이 숫자가 무엇을 뜻하는지는 말하지 않는다.
HN의 sedan_baklazhan는 한때 모두가 비웃던 코드 줄
수 지표가 이제 커밋 수 지표가 되었다고 꼬집었다.
기능이나 버그 수정은 어떻게 되었느냐는 물음이다.[^sedan_baklazhan]
INTPenis는 3,021명 가운데 807명이 첫 기여자라는
숫자를 AI의 도움을 받은 패치가 많다는 뜻으로 읽었다.
모두가 나쁘게 제출하는 것은 아니니 비판이 아니라 관찰이라고
덧붙였다.[^INTPenis] sirnicolaz는 커널 슬롭이 없기를 바란다고 했다.[^sirnicolaz]

이 해석들은 글에 근거가 없다. 807명의 첫 기여자가 무엇으로 늘었는지는 소식이
말하지 않으며, 같은 숫자를 서로 다른 이야기에
끌어다 쓰는 것이 이 숫자가 비어 있다는 증거다. leonidasrup는 커널의 현재 AI
정책이 AI를 얼마든지 쓰되 사용을 공개하고,
제출의 품질은 AI가 아니라 사람이 책임진다는 것이라고 정리했다.[^leonidasrup]
이 정책이 맞다면 AI 지원 패치의 비율은 커밋 로그에 드러나야
하지만 소식은 그 비율을 내놓지 않는다.

### 직전 몇 주의 논란이 이 릴리스 평가에 섞여 들어온다

HN의 VCFundedGenYer는 이 릴리스가 Torvalds가 갑자기 바이브 코딩을 발견해 커널에
풀어놓은 결과이며 이미 테스터가 경쟁 상태를 찾았고 파국적 문제가 예상된다고
단정했다.[^VCFundedGenYer] surajrmal은 그것이 테스트 상황을 개선하라는 압력이 될
뿐 AI가 쓴 패치에 대한 입장을 바꾸지는 않을 것이며
AI는 최근 변경으로 문제의 원인을 거슬러 올라가는 데 꽤 능하다고
답했다.[^surajrmal]

이 논쟁은 LWN 소식에도 Torvalds의 공지에도 나오지 않는다.
이 저장소에는 Torvalds가 Claude Code로 커널 개선 작업을
한 일을 다룬 문서들이 있고 이 논쟁은 그 일에서 온 것이다.
그러나 이 소식이 전하는 7.3이 그 작업을 포함하는지,
있다면 얼마나 되는지는 소식과 이 문서가 확인하지 못했다.
릴리스를 평가하는 근거로 쓰려면 변경 목록과 커밋 기록에서 먼저 확인해야 한다.

### 주요 변경의 우선순위를 가리는 기준이 없다

글이 든 변경은 아홉 개이고 모두 같은 층에 놓여 있다.
SMB 서버 개선이 긴 목록이라고만 하고 내용이 없다.
HN의 theden은 이 개선에 opt-in Apple Time Machine 지원이 들어 있고
macOS의 backupd가 ksmbd로 백업할 수 있게 한다는 점을 짚고 자신은 borg로 옮겼지만
상황에 따라 Time Machine을 다시 써 볼 수 있겠다고
적었다.[^theden] wryun은 같은 릴리스에 자신이 일하는 Morse의 Wi-Fi HaLow(900MHz
와이파이) 지원을 쓰는 첫 커널 드라이버가 들어갔다고 밝혔다.[^wryun]
소식이 한 줄로 넘긴 변경 속에 독자에게 가장 중요한 변경이 있을 수 있다는 뜻이다.

## 인사이트

### 한 릴리스의 가치는 숫자가 아니라 처음 쓰는 사람의 목록에서 보인다

LWN은 7.3의 기록을 숫자로 요약했지만 댓글에서
드러난 것은 서로 다른 사람들이 서로 다른 변경을 자기 것으로 받는 모습이다.
Nix 사용자는 재배치 가능한 바이너리를, macOS 사용자는 Time Machine을,
무선 개발자는 HaLow를, 보안 사람은 failfs를 본다.
Lobste.rs의 jaculabilis는 이 릴리스에 fzakaria의 재배치 가능한 Nix 바이너리
작업이 들어 있다고 기뻐했고
fzakaria는 이제 모든 배포판이 이를 지원하도록 만드는 길고
힘든 일이 남았다고 답했다.[^jaculabilis]

이 문서의 읽기로는 큰 릴리스일수록 하나의 평가가 의미를 잃고
사용 집단별 평가로 쪼개진다.
릴리스를 보는 일은 숫자로 시작하더라도 자기 집단의 변경을 찾는 일로 끝나야 한다.

### 커널 CVE의 증가는 커밋의 증가와 같은 곡선을 그릴 수 있다

HN의 skybrian은 수정된 커널 CVE의 수가 사상 최고라는 그래프를
링크했다.[^skybrian] abainbridge는 같은 그래프를 CVE가 도입된 커널 버전을
기준으로 보고 싶다고
했고,[^abainbridge] d5lt5는 추가된 CVE의 수도 틀림없이 사상 최고일 것이라고
했다.[^d5lt5]

이 문서의 읽기로는 커밋이 늘면 수정되는 결함과 도입되는 결함이 함께 늘 수 있고
두 곡선을 가르려면
결함이 도입된 버전을 기준으로 세어야 한다. abainbridge가 말한
것처럼 몇 년이 지난 버전에서만 의미 있는 지표라는 한계가 있다.
이는 이번 릴리스의 평가가 몇 년 뒤에야 가능하다는 뜻이기도 하다.

### 소식 아래의 문답이 소식보다 오래 쓸모 있다

LWN의 이 소식 아래에서 swilmet는 신입을 위한 최근의 문서나 입문서가 무엇이냐고
물었고 corbet은 커널의 개발 프로세스 문서가 다른 문서보다 잘 관리되고
새 개발자에게 필요한 읽을거리가 많다고 답했다.[^corbet]
릴리스 소식은 하루 만에 지나가지만 이 답은 다음 릴리스에도 쓸모가 있다.
이 문서의 읽기로는 첫 기여자가 807명이라는 숫자를 다음 릴리스에서
키우는 일은 이런 안내가 닿는지에 달려 있다.

---

[^saint-evan]: <https://news.ycombinator.com/item?id=50149755>

[^rwmj]: <https://news.ycombinator.com/item?id=50149675>

[^roryirvine]: <https://news.ycombinator.com/item?id=50152636>

[^fzakaria]: <https://lobste.rs/s/4oz3sk/7_3_kernel_has_been_released#c_ilggrq>

[^sedan_baklazhan]: <https://news.ycombinator.com/item?id=50150323>

[^INTPenis]: <https://news.ycombinator.com/item?id=50150088>

[^sirnicolaz]: <https://news.ycombinator.com/item?id=50149654>

[^leonidasrup]: <https://news.ycombinator.com/item?id=50150391>

[^VCFundedGenYer]: <https://news.ycombinator.com/item?id=50152368>

[^surajrmal]: <https://news.ycombinator.com/item?id=50152579>

[^theden]: <https://news.ycombinator.com/item?id=50149670>

[^wryun]: <https://news.ycombinator.com/item?id=50151374>

[^jaculabilis]: <https://lobste.rs/s/4oz3sk/7_3_kernel_has_been_released#c_eqfaob>

[^skybrian]: <https://news.ycombinator.com/item?id=50151340>

[^abainbridge]: <https://news.ycombinator.com/item?id=50153633>

[^d5lt5]: <https://news.ycombinator.com/item?id=50158763>

[^corbet]: <https://lwn.net/Articles/1101435/>
