# OpenBSD에 Wine이 들어온 것은 커널을 열지 않고 소프트웨어로 %gs를 흉내 낸 덕분이다

원문: ['emulators/wine' - MARC](https://marc.info/?l=openbsd-ports&m=179236125692175)

HN 토론: <https://news.ycombinator.com/item?id=50152307> (514점, 172개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/gqepzd/wine_ported_openbsd> (82점, 13개 댓글)

GN 토론: <https://news.hada.io/topic?id=35645>

## 요약

Thomas Frohwein은 2026년 10월 18일 openbsd-ports 메일링 리스트에
올해 가장 놀라운 포트 제안일지 모른다며 Wine 포트를 제안했다.
%gs/gsbase 문제를 두고 오간 논의를 계기로 시작된 공동 작업이고
문이 열린 것은 Andrii의 소프트웨어 해법 덕분이라고 한다.
그가 전하는 설명은 gsbase를 설정할 수 없으니
명령어의 %gs 접두사를 에뮬레이션한다는 것이다.
힘든 일은 Andrii와 Fabien이 했다고 공을 돌린다.

그는 Wine에 대한 관심이 5~10년 전과 다르게 높아졌다고 쓴다.
그 사이 많은 Windows 소프트웨어가 64비트로 옮겨 갔기 때문이다. 64비트 Windows
소프트웨어 수십 개를 시험해 대부분 성공했고
스크린샷과 방송 녹화가 링크되어 있다.
지난달 출시된 The Witcher 3의 리마스터도 vkd3d-proton을 더하면 잘 돈다고 한다.

WoW64가 동작하지 않아 32비트 Windows 소프트웨어는 아직 실행되지 않는다.
이것이 가장 큰 제약이다.
`file(1)`로 실행 파일을 확인했을 때 Intel 80386 32비트라고 나오면 32비트다.
Wine의 내장 테스트는 지금 꺼져 있다.
X 서버에 접근해야 하고 여러 테스트가 멈추기 때문이다.
많은 게임을 실제로 돌려 본 시험에서는 그런 멈춤이 관찰되지 않았다고 한다.

시험해 보려는 사람에게는 Notepad++를 권한다.
이 포트는 언제나처럼 자기 책임으로 실행하는 소프트웨어이고
`unveil(2)`로 울타리를 칠 수 있는지 알아볼 때까지는
별도의 비특권 사용자를 만들어 쓰라고 당부한다.
시험과 기여에 도움을 준 사람으로 brynet, bentley, pertho, vl_ms를 든다.
글은 ok?라는 한마디로 끝나고 포트 초안은 첨부되어 있다.

## 분석

### 문제는 Wine이 아니라 %gs였다

Windows 소프트웨어를 Unix에서 돌리는 Wine은 FreeBSD와 macOS에서
이미 지원되므로 또 하나의 BSD를 더하는 일이 그 자체로 어렵지는 않다.
HN의 coldpie는 포트의 패치를 살펴보니
일부 유닉스 API가 달라진 곳이 있어 `#if OpenBSD` 식으로 막았고
`%gs` 레지스터 부분이 가장 복잡하다고 했다.
Windows에서는 이 레지스터가 스레드 로컬 저장소에 쓰이지만 다른 운영체제에서는
다른 용도로 쓰이므로 새 운영체제로 옮길 때 가장 큰 문제라고 덧붙였다.[^coldpie]

OpenBSD에서는 사용자 영역에서 %gs를 설정할 수 없어서 이 문제가 더 어려웠다.
이 포트의 계기가 된 openbsd-tech의 질문에서
질문자는 왜 OpenBSD가 사용자 영역에서 %gs를 설정할 수 없는지,
swapgs 취약점을 피하려는 것인지를 물었다.[^neth-question]
Philip Guenther는 rthreads를 구현할 때는 필요하지 않았고
그 뒤로 누구도 트랩과 시스템 호출 진입점에 필요한 섬세한 수술을 하지 않았다고
답했다.
하드웨어에 `{rd,wr}{fs,gs}base`가 생겼을 때 잠깐 살펴봤지만 새 복잡성과 위험,
곧 swapgs를 가로지르는 추측 실행 위험이 좋은 거래로 보이지 않았다고
설명하고 Wine에 대한 관심이 정말 커지고 있느냐고 되물었다.[^guenther]
Frohwein은 글에서 이 답의 링크를 걸고,
관심이 실제로 있다고 19일 뒤에 포트를 제안하며 답한다.

### 해법은 커널을 건드리지 않고 명령어를 고쳐 쓰는 것이다

HN에 포트의 작성자 NethIafin이 직접 설명을 올렸다.
%gs와 gsbase가 모두 0이어서 %gs를 쓰는 명령은 모두 0번 페이지를 잘못 가리키므로,
이 명령에서 트랩을 받아 명령어를 해독하고
%gs를 쓰지 않는 명령으로 바꿔 다른 곳에 보관한다는 것이다.
변환에는 임시 레지스터가 필요하고
gsbase가 있어야 할 자리에 Wine의 TEB 포인터를 넣은 뒤 실행하고
임시 레지스터 상태를 되돌린다.
원래 명령이 충분히 넓으면 5바이트인 `jmp rel32`로 바꾸고,
그렇지 못하면 계속 트랩하되 트랩 위치와 스텁 위치의 해시를 만든다.
그런 경우는 다행히 드물고 이 패치 하나만으로 Notepad,
Notepad++, Factorio와 많은 게임이 돈다고 한다.[^NethIafin]

이 설명은 메일의 한 줄 요약을 구체화한다.
커널이 허용하지 않는 것을 허용하도록 커널을 바꾸는 대신,
허용되지 않는 연산을 쓰는 프로그램의 코드를 실행 중에 고쳐 쓰는 방식이다.
같은 설명은 보안 모델과 충돌하는 지점 두 가지를 더 든다.
Windows 스레드가 서로 대화하는 API를 Wine이 유닉스 시그널로 흉내 내는데
OpenBSD는 한 프로세스가 다른 프로세스의 스레드에 시그널을 보내는 것을 허용하지
않아서, 활성 스레드가 받은 시그널을 프로세스 안에서 SIGUSR2로 다시 내보낸다.
`ReadProcessMemory`와 `WriteProcessMemory`는 주로 Electron과 Steam이 쓰는데,
Wine 프로세스가 wineserver의 자손이 아니어서
`kern.global_ptrace=1`을 켜지 않으면 wineserver가 `ptrace`할 수 없다.
작성자는 커널을 가능한 한 표준 그대로 두려고
이 설정을 켜지 않았다고 쓴다.[^NethIafin]

## 비평

### 글은 어디까지 되는지가 아니라 어디까지 시험했는지를 말한다

Frohwein의 글은 수십 개의 64비트 소프트웨어를 시험해 대부분 성공했다고
하지만 어떤 것이 실패했고 얼마나 실패했는지는 말하지 않는다.
내장 테스트가 꺼져 있고 일부는 멈춘다고 밝히면서도 실제 시험에서는
그런 멈춤이 관찰되지 않았다는 말을 한다.
NethIafin도 아주 부담이 큰 3D 게임에서는
안정성 문제가 남아 있다고 썼다.[^upstream-reply]
그렇다면 글이 말하는 성공은 시험 목록에 든 것에 대한 성공이고
목록의 범위는 글에서 확인되지 않는다.

HN의 haunter는 게임 플레이 영상 링크를 모았고
사양이 AMD Ryzen 9 9900X와 16GB 램과 Radeon RX 9070이라고
적었다.[^haunter] ninjin은 OpenBSD가 Nvidia를 지원하지 않고
AMD와 Intel은 트리에 최신 하드웨어 드라이버가 있다고 설명했다.[^ninjin]
성공 사례는 모두 AMD 그래픽 환경에서 나왔고 Nvidia에서는 지금 쓸 수 없다.
글에는 이 조건이 없다.

### 포트가 업스트림으로 가지 않는다는 것은 유지보수가 포트 쪽에 남는다는 뜻이다

openbsd-ports에서 누군가 이 큰 패치 묶음을 업스트림에 합칠 가능성이 있느냐고
물었고 NethIafin은 대부분 합쳐지지 않을 것이라고 답했다.
OpenBSD용 변경은 작업을 단순하게 하려고 모두 OpenBSD 전용으로 표시했고
Wine 유지보수자들은 한 달 전 이야기에서
OpenBSD용으로 컴파일되게 하는 패치조차 또 하나의 운영체제를 지원해야 하므로
망설였으며
%gs 스텁 수정은 에뮬레이션되는 애플리케이션 코드를
바꾸는 것이라 업스트림이 절대 받을 수 없다는 것이다.
합치는 것이 지금의 목표가 아니고 몇 달 뒤 상황을 보겠다고 한다.[^upstream-reply]

HN의 t-3가 이 교환을 가져왔고
iamnothere는 OpenBSD 유지보수자들이 당분간 이를 직접 돌려야 하며
NetBSD도 비슷한 처지라 패치가 크게 갈라지지 않으면 노력을 합칠 수도 있다고
했다.[^t-3][^iamnothere] coldpie는 업스트림 시도를 권했지만
작성자의 답이 이미 나와 있었다.[^coldpie]
이 포트의 지속은 포트 담당자들의 지속 의지에 달려 있다는 점이 글에서
읽히지 않는 비용이다.

### 같은 패치가 에뮬레이션한 코드 위에서 돈다는 보안 모델의 긴장이 남는다

글은 이 포트가 자기 책임으로 쓰는 소프트웨어이고
별도의 비특권 사용자로 실행하라고 당부한다.
OpenBSD의 보안 모델은 한 프로세스가 다른 프로세스에 간섭하지 못하게 하는
데 기대는데, 이 포트는 그 제약을 우회해 Windows 프로그램을 돌린다.
시그널을 같은 프로세스에서 다시 내보내고
명령어를 고쳐 쓰는 것은 모두 보안 모델 안에서 허용되는 방식이지만
실행되는 Windows 바이너리 자체는 OpenBSD가 검증한 코드가 아니다.
`unveil(2)`로 울타리를 칠 수 있는지는 글이 앞으로 알아볼 일로 남겨 둔다.

## 인사이트

### 보안 모델의 거절이 설계의 제약이 아니라 설계의 도구가 되었다

이 포트가 마주친 세 문제는 모두 OpenBSD의 보안 선택에서 나왔다.
%gs를 사용자 영역에서
설정할 수 없는 것은 swapgs 추측 실행 위험을 피하려는 선택으로 설명되고
다른 프로세스의 스레드에 시그널을 보낼 수 없는
것과 전역 `ptrace`가 꺼져 있는 것도 마찬가지다.
작성자가 택한 길은 세 가지 모두에서
커널의 선택을 존중하고 사용자 영역에서 우회하는 것이었다.
그는 커널을 가능한 한 표준 그대로 두려고 했다고 밝힌다.

이 결과는 보안 선택을 바꾸지 않고도 기능을 얻는 길이 있음을 보여 준다.
이 문서의 읽기로는 이 포트는 OpenBSD가 사용자 영역의 거절을 유지하면서도
사용자가 원하는 소프트웨어를 얻을 수 있는지에 대한 첫 실증이다.
이 읽기가 틀렸다면 안정성 문제가 거절을 우회하는 방식의 한계에서
나올 것이고 남아 있다는 3D 게임의 불안정이 그 신호일 수 있다.

### Wine에 대한 관심의 변화는 소프트웨어의 64비트 이행이 만든 것이다

Frohwein은 5~10년 전과 다른 관심이 생긴 이유로 많은
Windows 소프트웨어가 64비트로 옮겨 간 것을 든다.
이 설명이 맞다면
이 포트의 한계인 WoW64 미지원은 5~10년 전에는 치명적이었을 것이고
지금은 상대적으로 작은 제약이다.
Guenther의 질문,
곧 Wine에 대한 관심이 정말 커졌느냐는 물음에 대한 답이 이 이행이다.

HN과 Lobste.rs의 반응이 그 관심의 크기를 보여 준다.
HN의 RunSet은 OpenBSD가 슬롭 코드로부터의 피난처로 자리 잡는 이때 특히 반가운
소식이라고 했고 greyw는 OpenBSD가 더 뒤처질 것이라고 반박했으며
hias는 이 Wine 포트가 어떻게 만들어졌다고
생각하느냐고 되물었다.[^RunSet][^greyw][^hias]
Lobste.rs의 nemin은 처음에는 기본적인 Windows 앱 몇 개를 실행하는 정도겠거니
했다가 AAA급 게임이 돈다는 것에 놀랐으며
보안에 특히 까다로운 OpenBSD보다 NetBSD가 먼저 이런 것을 얻을 줄 알았다고
적었다.[^nemin]
이 교환들에서 같은 소식은 서로 다른 기대와 우려를 불러왔다.

### 개발 기록이 CVS에 있다는 사실이 이 포트의 검증을 어렵게 한다

HN의 simonw는 OpenBSD가 아직 CVS를 쓰며
GitHub 미러의 포트에는 13시간 전의 정적 임포트만 있다고 짚고
이 Wine 포트의 개발 이력을 추적하는 저장소가 따로 있느냐고 물었다.[^simonw]
Maken은 공식 CVS에서 NethIafin의 GitHub 저장소로 가는 링크가 있다고
답했고[^Maken] iamnothere는 개발이 아직 CVS에서 이루어지며
git 기반 개발을 허용하되 OpenBSD의 독특한 방식을 따르는 got을 만들고
있다고 덧붙였다.[^iamnothere-got]

이는 작은 정보지만 이 포트의 투명성에 영향을 준다.
포트의 변경 이력을 보려면
OpenBSD의 ports 트리뿐 아니라 작성자의 별도 저장소를 함께 봐야 한다.
이 문서는 그 저장소를 열어 보지 않았으므로
저장소의 내용에 대해서는 말하지 않는다.

---

[^neth-question]: marc.info openbsd-tech, [Question - %gs support on OpenBSD](https://marc.info/?l=openbsd-tech&m=179067466617674&w=2), 2026-09-29

[^guenther]: marc.info openbsd-tech, [Re: Question - %gs support on OpenBSD](https://marc.info/?l=openbsd-tech&m=179070170845285&w=2), 2026-09-29

[^upstream-reply]: marc.info openbsd-ports, [Re: emulators/wine](https://marc.info/?l=openbsd-ports&m=179241414029592), 2026-10-19

[^coldpie]: <https://news.ycombinator.com/item?id=50153584>

[^NethIafin]: <https://news.ycombinator.com/item?id=50156877>

[^haunter]: <https://news.ycombinator.com/item?id=50153377>

[^ninjin]: <https://news.ycombinator.com/item?id=50153615>

[^t-3]: <https://news.ycombinator.com/item?id=50153536>

[^iamnothere]: <https://news.ycombinator.com/item?id=50154096>

[^RunSet]: <https://news.ycombinator.com/item?id=50153292>

[^greyw]: <https://news.ycombinator.com/item?id=50153515>

[^hias]: <https://news.ycombinator.com/item?id=50153779>

[^nemin]: <https://lobste.rs/s/gqepzd/wine_ported_openbsd#c_95w6wz>

[^simonw]: <https://news.ycombinator.com/item?id=50153992>

[^Maken]: <https://news.ycombinator.com/item?id=50154138>

[^iamnothere-got]: <https://news.ycombinator.com/item?id=50154173>
