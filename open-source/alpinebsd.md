# AlpineBSD: AI가 쓴 소프트웨어를 최대한 쓰지 않도록 설계한 NetBSD 기반 운영체제

<https://wiki.alpinebsd.org/>

HN 토론: <https://news.ycombinator.com/item?id=50274251> (209점, 192개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/yxuvie/alpinebsd> (68점, 18개 댓글)

GN 토론: <https://news.hada.io/topic?id=36191>

## 소개

AlpineBSD는 NetBSD 커널에 Alpine Linux에서 영감을 받은 사용자 공간(userspace)을
얹은 운영체제이다.
위키 첫 화면은 이 프로젝트의 목표를 AI가 생성한 소프트웨어를 가능한
한 적게 쓸 수
있게 하는 것이라고 적는다.
기본 시스템(base)과 주 패키지 저장소(main)에는 LLM 출력이 들어 있지 않다고 한다.
아직 만드는 중이고 설치 프로그램이 없으며,
모험심 있는 사람을 위한 아주 높은 수준의 설치 안내가 따로 있다.

위키는 NetBSD와 Alpine Linux 각각과의 차이를 적는다.
NetBSD와 비교하면 NetBSD의 커널과 libc, `mount` 같은 플랫폼별 필수 도구를 그대로
싣는다.
NetBSD 커널의 하드웨어 지원은 Linux보다 훨씬 얇아서
아무 컴퓨터에서나 돌 것이라고 기대하면 안 된다고 경고한다.
Alpine Linux와 비교하면 패키지 관리자 apk-tools와 busybox를 쓰고,
BSD make보다 GNU make를 선호하는 식으로 사용자 공간이 GNU 쪽에 조금 더
가깝다.
Alpine Linux의 포크가 아니라 패키지 모음이 독자적이며 상당수가 aports를 바탕으로
한다고 밝힌다.
Alpine Linux는 OpenRC를 쓰지만 AlpineBSD는 지금 s6를 쓰고 OpenRC를 대안으로
추가할 계획이다.

이 문서는 위키 첫 화면과 AI 정책, 설치, 기여, 비자유 소프트웨어 페이지를 읽고
썼다.
소프트웨어를 직접 설치해 보지는 않았다.

## 구성

### AI 정책은 저장소 네 개와 의존 방향으로 구현된다

정책 페이지는 오염(tainted)을 정의한다.
코드, 문서, 바이너리, 그 밖의 자산 어느 부분이든 생성형 AI 도구(예:
LLM)의 출력이
들어 있는 소프트웨어는 오염된 것으로 본다.[^ai-policy]
패키지 저장소는 오염을 얼마나 허용하느냐로 갈리는 네 개이다.[^ai-policy]

| 저장소    | 지원 상태     | AI 정책                          |
| --------- | ------------- | -------------------------------- |
| base      | 지원          | 깨끗함(clean)                    |
| main      | 지원          | 깨끗함                           |
| tainted   | 커뮤니티 지원 | 오염됨                           |
| community | 커뮤니티 지원 | 깨끗한 의존성 또는 오염된 의존성 |

의존성은 표에서 위로 흐른다.
community는 tainted에 의존할 수 있지만 그 반대는 안 된다.[^ai-policy]
가장 보수적인 설치는 `/etc/apk/repositories`에서 base와 main만 켜는 것이고,
이 경우 오염된 소프트웨어가 하나도 없다는 것이 보장된다.[^ai-policy]
간접적으로 오염된 소프트웨어를 쓰려면 tainted와 community를 켜야 하는데,
tainted에 `@tainted` 같은 태그를 붙이면 설치할 때마다 명시적으로 선택해야
한다.[^ai-policy]
이때 `apk add`가 런타임에 오염된 패키지에 의존하는 패키지를 만나면 오류를 내고,
`apk add python3@tainted`처럼 직접 지정해야 설치된다.[^ai-policy]

패키지 메타데이터에도 정책 상태가 들어 있어서 `apk search`에서 거를 수
있다.[^ai-policy]
`genai:clean`은 오염되지 않은 소프트웨어, `genai:pinned`는 오염되지 않은 마지막
버전에 고정된 것, `genai:indirect-build`와 `genai:indirect-runtime`과
`genai:indirect-check`는 각각 빌드와 런타임과 시험 의존성으로 간접 오염된 것,
`genai:tainted`는 생성형 AI 출력을 직접 담은 것이다.[^ai-policy]
기여자에게는 AlpineBSD 자체 소프트웨어, 문서, 패키지 레시피,
메일링 리스트와 IRC의
글에 이르기까지 생성형 AI 도구를 쓰면 안 된다고 정책이 적는다.[^ai-policy]

### 고정된 패키지가 정책의 비용을 보여 준다

필수 소프트웨어 일부는 오염되지 않은 마지막 버전에 고정되어 있다.
`base`와 `main`의 고정 목록은 binutils, gcc, gdb, libffi, perl,
xorriso이다.[^ai-policy]
정책 페이지는 고정을 마지막 수단으로 하고 대안을 찾거나 패키지를
tainted로 옮기는 쪽을
선호한다고 적는다.[^ai-policy]
이 목록이 짧다는 것은 정책이 지켜지는 동안의 비용이 아직 작다는 뜻이고,
목록에 컴파일러와 디버거와 링커가 들어 있다는 것은 비용이 가장 큰 곳에서 이미
나타났다는 뜻이다.

### 비자유 소프트웨어는 하나만 허용된다

위키의 비자유 소프트웨어 정책은 자유 소프트웨어를 Open Source Initiative나
Free Software Foundation이 승인한 라이선스로 배포되는 소프트웨어로
정의한다.[^non-free]
허용되는 비자유 소프트웨어는 NetBSD 드라이버용 바이너리 덩어리를 담은
`netbsd-firmware` 패키지 하나뿐이다.[^non-free]

## 설치와 기여

설치 페이지는 일급 설치 절차가 아직 없고 수동 절차의 예를 든다.[^installation]
NetBSD 설치 매체로 부팅한 뒤 셸로 빠져나와 GPT 디스크를 나누고,
파일 시스템을 만들어 `/mnt`에 마운트하고, `apk`를 초기화한다.[^installation]
디스크는 GPT만 지원하고 BSD 디스크 레이블은 될 수도 있지만 장담하지 않는다고
적는다.[^installation]
저장소 설정은 `base`만 켜 두고 `main`, `tainted`,
`community`는 주석 처리한 예이다.[^installation]
이어서 `absd-base`, NetBSD 커널 패키지, 펌웨어,
부트로더 패키지를 `apk`로 설치하고,
`chroot`로 들어가 장치 파일을 만들고, s6의 서비스를 켜고,
부트로더와 `fstab`을 설정한 뒤 재부팅한다.[^installation]
안내의 마지막 문장은 축하한다며 아마도 설치했다고 쓴다.[^installation]

기여 페이지는 패키지 모음 `absd-ports`를 `got`이나 `git`으로 받고,
패키지를 빌드하려면 `build-base`를 설치하고 `abuild-keygen -ai`를 실행하고
사용자를 `abuild` 그룹에 넣으라고 안내한다.[^contributing]
패치는 `PATCH absdports` 같은 제목 접두사를 붙여 `git send-email`로
`alpinebsd-devel` 메일링 리스트에 보내고,
커밋 메시지는 `package: brief summary` 형식이다.[^contributing]

## 분석

### 정책이 문서가 아니라 패키지 그래프의 속성이다

이 프로젝트가 눈에 띄는 점은 AI 반대를 선언으로 두지 않고 패키지
시스템의 속성으로
구현했다는 것이다.
오염 여부가 패키지 메타데이터에 있고, 의존성은 한 방향으로만 흐르고,
설치 도구가 오염된 의존성을 만나면 멈춘다.
이 구조는 라이선스를 다루는 방식과 비슷하다.
GPL 같은 라이선스가 의존성을 따라 퍼지는 것처럼 오염도 그래프를 따라 퍼지고,
그래서 정책은 한 패키지의 문제가 아니라 의존 그래프 전체의 문제가 된다.
이 문서의 해석으로는 이 점이 AlpineBSD의 실질적인 기여이고,
AI 정책에 동의하지 않는 사람에게도 의존성 오염을 추적하는 방식은 참고할 만한
설계이다.

### 선택지를 고르는 비용을 사용자에게 돌려준다

정책의 기본값은 가장 엄격한 쪽이고,
느슨하게 하려면 사용자가 저장소를 켜고 패키지를 하나씩 직접 지정해야 한다.
이 설계는 사용자가 AI 사용을 얼마나 받아들일지를 선택하게 한다.
HN에서 against_epistem은 이유를 밝히지 않고 사용자에게 맡기는 태도를
존중할 만하다고
했다.[^against_epistem]
다만 이 설계의 전제는 오염이 정확히 판정된다는 것이다.
판정의 방법은 정책 페이지에 서술되지 않았다.

## 비평

### 정책은 무엇을 하는지만 말하고 왜 하는지는 말하지 않는다

HN에서 efficax는 AI를 쓰지 않는다는 것이 정책이라는 건 알겠지만 이유가
없다고 썼다.
그는 binutils와 gcc와 gdb를 고정하면 업스트림의 패치를 받지 못하고
직접 유지보수를
떠안게 되어 사실상 개발이 멈춘다고 보았다.[^efficax]
cturner는 이 프로젝트가 네이티브 하드웨어용인지 컨테이너용인지,
AI 생성 코드를 피하려는 사용자가 NetBSD를 그대로 쓰지 않고 이것을 쓸
이유가 무엇인지
첫 화면에서 알 수 없다고 했다.[^cturner]
mrbn100ful은 고정 목록을 인용하며 그 패키지들을 대체하기는 어려울 것이라고
했다.[^mrbn100ful]

이유를 말하지 않는 것은 설명이 없다는 뜻일 뿐 근거가 없다는 뜻은 아니다.
rjsw는 NetBSD가 AI 사용을 거부하는 이유가 GPL 코드로 학습한 LLM의 출력이
라이선스의 전염 조항을 받는다는 판결이 나올 가능성에 대한 우려라고
설명했다.[^rjsw]
이 이유는 NetBSD의 것으로 소개되었고, AlpineBSD가 같은 이유를 쓰는지는
위키에 없다.
HN에서 hoppp는 가능한 한 AI 코드를 적게 쓴다는 태도가 부족주의(tribalism)이며,
좋은 소프트웨어는 누가 만들었든 훌륭하고 검증되어 있으면 된다고
반박했다.[^hoppp]
이 반론에는 정책이 품질이 아니라 출처에 관한 것이라는 구분으로 답할 수 있지만,
그 구분도 위키가 말하지 않는다.

### NetBSD를 두고 새 사용자 공간을 만든 이유가 약하다

Lobste.rs에서 gamache는 NetBSD에 이미 LLM 출력 금지 정책이 있는데 왜 NetBSD의 커널과
libc 위에 새 사용자 공간을 만들었는지 의아하다고 했다.[^gamache]
그는 기본 NetBSD에서 출발해 LLM을 쓰지 않은 프로젝트만 모은 패키지
저장소를 만드는
편이 더 쉬웠을 것이라고 했고,
miah는 GNU 도구를 들여오면 오히려 NetBSD에 LLM 쓰레기가 섞일 가능성이 커진다고
했다.[^miah]
이 지적은 위키가 스스로 내세운 두 차이, 곧 GNU 쪽으로 기운 사용자 공간과
Alpine식 도구가 정책의 목적과 어떻게 맞는지를 설명해야 한다는 뜻이다.
위키는 Alpine을 닮으려는 이유가 사용성인지 이식성인지도 적지 않는다.

### 하드웨어 경고는 NetBSD의 평판과 어긋나 보인다

위키는 NetBSD 커널의 하드웨어 지원이 Linux보다 훨씬 얇다고 경고한다.
HN에서 bityard는 NetBSD의 가장 큰 자랑이 거의 모든 것에서 돈다는 점이라며,
위키가 링크한 노트북 문서는 AMD64 노트북의 주변 장치 문제를 다루는 것이라
출발점으로 맞지 않다고 했다.[^bityard]
Lobste.rs에서 nortti는 이를 구분해서 설명했다.
NetBSD가 어디서나 돈다는 말은 이식성이 높아서 드라이버를 쓰면 부팅할 수 있다는
뜻이고, 데스크톱에서 필요한 소리와 가속 그래픽과 내장 네트워크 장치의 성능,
노트북의 전원 관리 같은 마무리 드라이버 작업이 부족하다는 것이다.[^nortti]
위키의 문장은 사실이지만 이 두 가지를 구분하지 않아서 오해를 부른다.

### 설치 안내가 신뢰의 출발점을 흐리게 둔다

설치 페이지의 `apk` 초기화는 서명 키 파일을 내려받아 키 디렉터리에 넣고,
`apk.static`이라는 이름의 바이너리를 내려받아 실행 권한을 주고,
패키지 설치 명령에 인증서 검사를 끄는 옵션을 쓴다.[^installation]
저장소 주소도 `http://`로 적혀 있다.[^installation]
이 구성에서 패키지 자체는 서명 키로 검증될 수 있지만,
처음 내려받은 `apk` 바이너리의 무결성은 어디서도 검증되지 않는다.
설치 프로그램이 없는 단계이므로 임시 안내일 수 있지만,
정책이 공급망에 대한 약속을 하는 프로젝트의 설치 안내가 그 출발점을 검증 없이
시작한다는 점은 눈에 띈다.
이 문서는 해당 바이너리나 키를 직접 검증하지 않았고, 서명 키 파일 이름에
`drew@ddevault.org`가 들어 있다는 점만 확인했다.

## 인사이트

### 오염은 기록된 만큼만 추적할 수 있고 기록은 줄어들 수 있다

이 정책의 전제는 어떤 코드에 AI의 출력이 들어 있는지를 알 수 있다는 것이다.
Lobste.rs에서 jcs는 OpenBSD가 사람이든 도구든 버그 보고를 출처와 무관하게 받으며,
최근에는 사용한 LLM 도구를 커밋 메시지에 적지 않게 된 것 같다고 했다.[^jcs]
그 이유는 도구가 아무 상관이 없고 광고를 계속하고 싶지 않아서라고 했다.[^jcs]
이 문서의 해석으로는 이것이 오염 추적의 구조적 약점이다.
프로젝트가 AI 도구의 사용을 기록하지 않으면 AlpineBSD는 그 프로젝트의
오염을 판정할
방법이 없고, 기록하지 않는 선택이 합리적일수록 깨끗하다는 표시가 신뢰를 잃는다.
jcs는 새 기능이나 드라이버를 LLM이 쓴 것을 받았다고 알고 있지 않다고 했고,
lobo는 OpenBSD가 Anthropic과의 협업으로 만든 패치를 받은 커밋을 가리켰다.[^lobo]
이 문서는 그 커밋을 열어 보지 못했다.
이 가설을 뒤집는 관측은 대형 업스트림 프로젝트들이 AI 사용을 계속
기록하는 경우이다.

### 고정된 패키지는 업스트림이 AI를 받아들일수록 늘어난다

고정 목록의 패키지는 업스트림이 오염되지 않은 마지막 버전에 멈춘 것들이다.
업스트림이 AI 보조 개발을 받아들일수록 이 목록은 길어지고,
고정된 패키지는 새 보안 패치를 받으려면 오염 여부를 다시 판정해야 한다.
이 문서의 해석으로는 이것이 이 정책의 가장 큰 운영 위험이다.
정책 페이지는 이 패키지들의 보안 패치를 어떻게 다루는지 적지 않는다.
kev009는 HN에서 이런 프로젝트가 처음에는 이목을 끌지만 오래 가지 않는
경우가 많다고
했다.[^kev009]
lukaslalinsky는 AI에 반대하는 옛 Linux 사용자층이 충분히 크지 않을 것이므로,
차라리 NetBSD와 OpenBSD의 드라이버 상황을 개선하는 일이 더 유용하다고
했다.[^lukaslalinsky]
고정 목록의 크기는 시간이 지나면서 정책이 유지되는지를 가장 잘 보여
주는 지표이다.

### 사람이 쓴 코드의 모음은 시간이 지날수록 희귀해진다

nanolith는 AI 관여의 정도가 다른 오픈소스 프로젝트가 공존하는 생태계가 좋고,
사람이 완전히 쓴 순수한 소프트웨어도 있어야 한다고 했다.
모델이 쓸모 있으려면 좋은 입력이 필요한데,
사람이 쓰고 꼼꼼히 감사한 소프트웨어는
통계적 모델의 피드백 오류에서 자유롭다는 것이다.[^nanolith]
그는 나쁜 패턴이 세대를 거치며 점점 더 자주 보이게 되고,
쓸모없는 이름 관례 같은 무해한 것이거나 악용 가능한 경계 사례일 수 있다고
썼다.[^nanolith]
이 문서의 비유로는 핵실험 이전에 만든 강철이 방사능 측정기에 필요한 것처럼,
AI 이전에 쓰인 코드와 그 뒤에도 사람만 쓴 코드가 기준 자료로 값을
갖게 될 수 있다.
다만 이 논거는 AlpineBSD가 아니라 사람이 쓴 코드 일반에 대한 것이고,
AlpineBSD가 그 기준 자료의 역할을 하려면 오염 여부의 판정이 믿을 만해야 한다.
iamnothere는 FOSS가 강경한 반 AI, AI 중립과 억제, AI 보조, AI 주도의 진영으로
갈라지고 있으며 초기 GPL과 BSD의 논쟁과 닮았다고 했다.[^iamnothere]
lionkor는 그것이 자유에 관한 논쟁이 아니라 복사한 코드와 직접 쓴 코드의 차이에
가깝다고 반박했다.[^lionkor]
cowanon77은 몇 년 안에 AI의 실제 생산성과 영향을 가늠할 자연 실험이 될 것이라고
했다.[^cowanon77]

---

[^ai-policy]: AlpineBSD wiki, [AI policy](https://wiki.alpinebsd.org/ai-policy)

[^non-free]: AlpineBSD wiki, [Non-free software policy](https://wiki.alpinebsd.org/non-free)

[^installation]: AlpineBSD wiki, [Installation](https://wiki.alpinebsd.org/installation/)

[^contributing]: AlpineBSD wiki, [Contributing to AlpineBSD](https://wiki.alpinebsd.org/contributing/)

[^efficax]: <https://news.ycombinator.com/item?id=50275436>

[^cturner]: <https://news.ycombinator.com/item?id=50275195>

[^mrbn100ful]: <https://news.ycombinator.com/item?id=50275589>

[^rjsw]: <https://news.ycombinator.com/item?id=50282227>

[^hoppp]: <https://news.ycombinator.com/item?id=50275280>

[^gamache]: <https://lobste.rs/s/yxuvie/alpinebsd#c_lwd7pp>

[^miah]: <https://lobste.rs/s/yxuvie/alpinebsd#c_sqck1j>

[^bityard]: <https://news.ycombinator.com/item?id=50275550>

[^nortti]: <https://lobste.rs/s/yxuvie/alpinebsd#c_s98ghi>

[^jcs]: <https://lobste.rs/s/yxuvie/alpinebsd#c_grsfxk>

[^lobo]: <https://lobste.rs/s/yxuvie/alpinebsd#c_8611fh>

[^kev009]: <https://news.ycombinator.com/item?id=50277665>

[^lukaslalinsky]: <https://news.ycombinator.com/item?id=50285562>

[^nanolith]: <https://news.ycombinator.com/item?id=50278235>

[^iamnothere]: <https://news.ycombinator.com/item?id=50275437>

[^lionkor]: <https://news.ycombinator.com/item?id=50275713>

[^cowanon77]: <https://news.ycombinator.com/item?id=50278857>

[^against_epistem]: <https://news.ycombinator.com/item?id=50275573>
