# Git 3.0의 SHA-256 기본값 전환: 해시 알고리즘이 아니라 생태계를 바꾸는 선택

원문: [Git 3.0's upcoming SHA-256 default will be a costly mistake | Butler's Log](https://blog.gitbutler.com/git-3-sha-256)

HN 토론: <https://news.ycombinator.com/item?id=49924179> (286점, 280개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/bytzgl/git_3_0_s_upcoming_sha_256_default_will_be> (25점, 25개 댓글)

GN 토론: <https://news.hada.io/topic?id=34627>

## 요약

GitHub와 GitButler의 공동 창업자이자 『Pro Git』 저자인 Scott Chacon이 GitButler
블로그에 쓴 글이다(읽는 데 17분).
Git 3.0이 기본 해시 알고리즘을 SHA-1에서 SHA-256으로 바꾸는데,
이것이 “이해하기 어려울 만큼 비싸고 결국 가치가 없으며 피할 수 있는 전 세계적
악몽”이 될 것이라는 주장이다.
몇 년째 속으로만 갖고 있다가, 3.0이 모두에게 시간과 고통을 안기면서 얻는 것은
거의 없는데 아무도 무슨 일이 닥칠지 모른다고 판단해 쓴다고 한다.

글은 SHA-1의 역할부터 정리한다.
Git은 내용 주소 지정(content addressable) 데이터베이스로, 내용의
해시를 키로 써서 같은 내용이 같은 키를 갖고 같은 파일이 두 번 저장되지 않으며,
커밋이 앞 커밋의 해시를 담아 무결성이 전파된다.
Linus가 2005년에 고른 SHA-1은 20년 동안 잘 동작했고,
160비트 출력의 생일 한계상 우연한 충돌에는 약 1.4 셉틸리언(1,400조의 10억 배)
개의 파일이 한 프로젝트에 있어야 한다고 한다.
SHA-1이 “깨졌다”는 것은 충돌 공격이 가능하다는 뜻이고(SHAttered 2017, Shambles
2020), 수만 달러의 GPU 비용으로 의도된 충돌을 만들 수 있다는 이론적 가능성이다.

글은 두 가지 공격을 구분한다.
충돌 공격(collision)은 공격자가 같은 해시를 가진 무해한 파일과 악성 파일을 미리
만들어 두었다가 신뢰를 얻은 뒤 바꿔치는 것이고, 제2원상 공격(second-preimage)은
이미 있는 파일에 맞춰 같은 해시의 악성 파일을 만드는 것이다.
저자는 제2원상 공격이 더 우려스럽지만 거의 모든 널리 쓰이는 해시가 이에 취약하지
않으며, Git이 MD5를 써도 사실상 면역이라고 한다.
지구의 GPU 약 30억 개가 모두 RTX 5090이고 MD5만 계산해도 특정 원상을 찾는 데 약
160억 년이 걸린다는 계산을 든다.
설령 제2원상이 쉽다고 가정해도 모르는 사람에게 그 파일을 받게 만들어야 하는데 이
질문이 논의에서 빠져 있다고 한다.

핵심 논지는 해시가 신뢰의 메커니즘이 아니라는 것이다.
Linus가 2005년에 “진짜 보안은 배포에 있다”고 한 말을 인용하고,
신뢰는 “어디서 당겨 오는가”에 있다고 한다.
실제 공격은 해시 충돌이 아니라 npm 패키지의 쓰기 권한을 사회공학으로 얻거나,
지치고 무보수인 유지보수자에게 4만 달러를 주고 프로젝트를 넘겨받는 방식으로
일어나며 이것이 훨씬 싸고 쉽다고 쓴다.
그래서 SHA-1을 신뢰된 저장소에서 쓰는 충분히 좋은 고유 키 생성 수단으로 보면
교체할 이유가 없고, 그러지 않으면 새 논문이 나올 때마다 생태계 전체를 이전해야
하며 양자 컴퓨터가 256을 깨면 같은 처지가 된다고 주장한다.

“열차 사고”에 대해서는 이렇게 쓴다.
`git init --object-format=sha256`으로 이미 SHA-256 저장소를 만들 수 있지만
지금은 GitHub에 푸시할 수 없고 3.0 전에 고쳐질 것이며, 고쳐지더라도 서버에
저장소를 만들 때 해시 형식을 알려야 하고 두 형식은 섞이지 않는다.
사용자는 어느 버전으로 `git init`을 했는지 알아야 하며 맞지 않으면
`fatal: the receiving end does not support this repository's hash algorithm`을
보게 된다.
서브모듈은 같은 형식끼리만 쓸 수 있어 라이브러리는 두 버전이 필요하고,
변환하면 모든 서명이 깨지고 모두가 동시에 옮겨야 하며,
SHA-1이 들어간 링크와 슬랙과 이메일 속 해시가 모두 무효가 되고,
40자를 가정한 도구가 깨진다.
Git의 라이브러리가 GPL이어서 링크할 수 없어 생태계 대부분이 재구현을 쓰는데
지원이 없거나 부분적이어서 `git`을 호출하지 않는 도구가 깨진다.
Emily Shaffer의 발표에 따르면 Google은 내부 전체에 SHA-1 설정을 덮어쓰는
방안도 고려한다고 한다.

대안은 독립 트리 해시 헤더(Independent Tree Hash Headers)다.
커밋이나 태그에 서명할 때 트리 전체 내용의 별도
해시(SHA-256이나 BLAKE3)를 새 헤더로 넣어 함께 서명하면,
SHA-1은 내용 검색에 쓰고 다른 해시는 독립적 검증에 쓴다.
알고리즘이 깨지면 새 해시를 추가할 뿐 모든 프로젝트를 이전할 필요가 없고, 두
해시에서 동시에 충돌해야 하므로 SHA-256 하나보다 더 안전하다고 한다.
Colin Walters의 `git-evtag`가 2015년부터 비슷하게 SHA-512
체크섬을 태그에 넣어 왔다.
저자의 개념 증명은 Chromium(작업 트리 35GB, 파일 210만 개,
서브모듈 포함)의 체크섬을 M5 Mac에서 멀티스레드로 5초,
Linux(1.5GB)는 257ms, Git 프로젝트는 17ms에 만들었다.
단점은 헤더가 있는 서명된 객체만 신뢰할 수 있고 서명이 전체 역사로
전파되지 않는다는 것이다.
글은 이 접근이 NIST의 2030년 SHA-1 기한(암호학적 보호에 쓰는 경우에 대한 것)도
충족시킨다고 주장하고, sha1dc(충돌 탐지) 비용도 없앨 수 있다고 덧붙인다.

## 분석

### 글의 논리는 해시의 역할을 둘로 나누는 데서 출발한다

글이 반복하는 구분은 해시를 키(주소)로 쓰는 일과 신뢰(무결성)의
근거로 쓰는 일이다.
Git이 SHA-1을 쓴 것은 내용에 이름을 붙이기 위해서였고 신뢰는 다른 곳(배포 경로,
서명, 인증)에서 온다는 것이 Linus의 오래된 입장이다.
저자는 이 구분이 지켜지기만
하면 해시는 충분히 좋은 키이면 되고 MD5로도 문제가 없다고까지 말한다.

이 구분에서 글의 제안이 자연스럽게 나온다.
키는 SHA-1로 두고 신뢰는 별도의 해시로 따로 얹는다.
그러면 두 문제가 분리되고,
신뢰 쪽에서만 알고리즘을 갈아 끼우는 암호 민첩성(crypto agility)을 얻는다.
이는 알고리즘을 식별자에 고정해 둔 설계를 건드리지 않고 문제를 푸는 방법이다.

### “열차 사고”의 근거는 전환 비용의 목록이다

글의 후반은 비용을 나열한다.
저장소 형식이 둘로 갈라지고, 서버 생성 시 선택해야 하며,
서브모듈과 링크와 서명과 도구가 깨진다는 것이다.
이 중 구체적인 것은 서브모듈이 같은 형식끼리만 쓸 수 있다는
점과 해시 40자 가정이다.

HN에서 pavon은 SHA-1 서브모듈을 SHA-256 저장소에서 쓸 수 없다는 사실을 몰랐고,
그렇다면 전환이 수월한 일에서 대형 사고로 바뀐다고 했다.[^pavon]
colinublake는 자신의 배포용 스크립트가 40자 해시를 가정해 “grep하는 날”이
두렵다고 했다.[^colinublake]
이 비용은 해시 알고리즘 자체가 아니라 알고리즘이 식별자에 새겨져 있어서 생긴다.

### 제안은 알려진 해법의 확장이다

독립 트리 해시는 새로운 생각이 아니라고 글은 인정한다.
`git-evtag`가 2015년부터 같은 구조를 구현했고,
같은 논의가 Git 메일링 리스트에서 오래 이어졌다.
글의 기여는 이를 3.0 전에 한 번 짚어 보자는 것과 성능 수치(Chromium 5초)로
비용이 작음을 보인 것이다.
HN의 rurban은 이 글을 읽고 git-evtag로 옮기고 SHA-1을
유지하겠다고 했다.[^rurban]

## 비평

### 변환 설계 문서를 다룬 대목이 핵심 반론에 부딪힌다

Lobste.rs에서 가장 높은 점수를 받은 댓글은 글이 틀렸을 수 있다는 지적이었다.
pyfisch는 Git 문서(`hash-function-transition`)에 따르면 SHA-256 로컬 저장소가
SHA-1 원격 저장소에 푸시하고 당겨 올 수
있으며 그 반대도 되고, 각 객체의 두 해시를 디스크에 저장하고
즉석에서 변환하므로 비호환 문제를 대부분 피한다고 했다.[^pyfisch]
kel은 이 변환이 3.0까지 다듬어진다면 글이 언급한 거의 모든 문제가 풀리는데
길고 숨 가쁜 글에서 이를 놓친 것은 이상한 실수라고 했다.[^kel]
HN의 GrantMoyer도 같은 문서를 근거로 글의 우려 일부가 이미 다뤄졌다고
정리했고,[^GrantMoyer] gorgoiler는 지붕이 없는 집을 두고 비가 오면 문제라고
경고하는 글 같다고 했다.[^gorgoiler]

다만 반론에도 틈이 있다.
orib는 실제로 구현된 것이 아니며 너무 엉망이라 구현되지 않은 채로 남는 편이
낫다고 했고, “저장소를 다시 복제하라”가 현실적인 전환 방법이라고 했다.[^orib]
mort는 문서에 변환 표가 있는 것은 맞지만 실제로 모두가 그렇게 할지,
전환 안내가 드물다며 의문을 제기했다.[^mort-transition]
저자는 HN에서 SHA-1 이름을 보존하는 계획이 있어도
이를 전송할 방법이 없어 포지별로 갇히고 서명이 깨지며,
실제 교체가 일어나면 재계산이 틀릴 수 있다고 답했다.[^schacon-sha1db]
그러면 글의 논점은 변환 표의 존재가 아니라 그 표가 생태계 전체에서 실제로
쓰이느냐의 문제로 좁혀진다.
글이 이 문서를 직접 다루지 않았다는 점은 사실로 남는다.

### 충돌 공격이 무관하다는 주장은 반박이 거세다

글은 실제로 의미 있는 공격은 충돌 공격이며 이 공격은 신뢰를 얻은 뒤 바꿔치는
형태이므로 비현실적이라고 본다.
HN의 kpcyrd는 이 글이 오류와 오해를 부르는 주장으로 가득하다며 세 가지를 짚었다.
SHAttered는 실제 개념 증명이었고 Git이 영향을 받지 않은 것은 git-blob 접두사를
무차별 대입하지 않았기 때문이며, 충돌만으로 코드 밀반입이 가능하고(전체 커밋
해시가 같은 두 저장소가 서로 다른 코드를 담는 경우), Linus의 인용은 내용 주소
지정 체계를 내용 식별에 쓰지 말라는 뜻이라는 것이다.[^kpcyrd]
저자는 SHAttered 논문을 링크했고 이 공격이 실용적이지 않다는 데 모두 동의하며,
설령 둘 다 쉬워도 집중할 문제가 아니라고 답했다.[^schacon-kpcyrd]

Strilanc는 글이 세 가지(충돌이 제2원상보다 덜 위험,
악성 파일을 어떻게 받게 하나, 다른 공격이 더 문제)로 요약되며 둘째는 GitHub가
있는 세상에서 우스운 이야기라고 했다.
모르는 사람의 풀 리퀘스트를 받아 `git fetch`로 로컬에서 시험하는 일이 흔한데,
“당기면 끝”이라는 보안 경계는 용납할 수 없다는 것이다.
또 소프트웨어는 충돌이 일어나지 않는다고 가정하기
때문에 충돌이 버그와 뜻밖의 동작을 일으키며, WebKit이 충돌하는 PDF를 단위
테스트에 쓰려고 SVN 저장소에 병합했다가 저장소가 망가진 예를 들었다.[^Strilanc]
저자는 Git 노드가 이미 가진 객체는 교체하지 않으므로 공격은 처음 가져오는
경우여야 하고 이는 신뢰가 쌓이기 전이라 어렵다고 답했다.[^schacon-Strilanc]
bawolff는 우연이 아니라 의도된 충돌이 문제이며 낯선 사람의 커밋을 받는 오픈소스
세계에서는 충돌도 제2원상만큼 관련이 있다고 했다.[^bawolff]

### 포지의 구조는 “신뢰는 배포에 있다”에 구멍을 낸다

Lobste.rs의 hailey는 가장 날카로운 지적을 했다.
GitHub는 포크 네트워크 전체에서 객체를 공유하고 refs 이름 공간만 분리하므로,
GitHub의 인증을 뚫지 않아도 저장소를 포크해 위조된 객체를 올리면 상위
저장소에서 보인다는 것이다.
GitHub 공동 창업자가 쓴 글이 이 각도를 놓친 것이 놀랍다고 했다.[^hailey]
fanf는 포크 간 객체 참조 공격이 삭제된 브랜치를 복구하거나 신뢰된 상위 URL로
접근되는 포크에 악성코드를 넣는 데 쓰인다고 보탰다.[^fanf]
mort는 미러도 놓친다고 했다.
Git의 장점은 아무 미러에서나 받아 다시 해시해 예상한 해시와 맞으면 믿을 수
있다는 것이고, 수백 개 프로젝트를 여러 호스트에서 받는 Yocto 같은 시스템에서는
호스트 하나가 침해되어도 체크섬이 맞지 않아 발견된다는 것이다.[^mort-mirrors]
이 지적들이 맞다면 글의 “신뢰는 어디서 당겨 오는가”는 한 곳을 신뢰한다는
가정이며, 해시가 여러 곳 사이에서 검증 수단으로 쓰이는 현실을 설명하지 못한다.

### 이미 정해진 결정에 늦게 낸 반대라는 비판도 있다

HN의 MBCook은 수년간 논의와 계획 끝에 기본값 전환 시점을 발표한 지금이 모든
것이 틀렸다고 올릴 적절한 때냐며, 대안 제안을 다른 사람들이 왜 거절했는지도 없는
“월요일 아침 쿼터백”이라고 했다.[^MBCook]
저자는 첫 문단에서 밝혔듯이 몇 년간 기여자 모임과 Git Merge에서 이 문제를 들었고
해결책이 나오리라 기대했지만 최근 Git Merge에서 전환이 가깝고 해결되지 않았음을
확인했으며, 이것이 마지막 기회라고 생각했다고 답했다.[^schacon-MBCook]
저자는 이 글이 Jeff King과의 짧은 대화에서 나왔고 그가 전적으로 반대하지는
않았다고도 했다.[^schacon-peff]
논의에 참여하지 않았다는 비판은 사실과 다르지만,
글이 과거 논의에서 나온 반대 논거를 다루지 않는 것은 여전하다.

### 감사와 규정이라는 실제 동기를 다루지 않는다

HN의 0x00cl은 이 변경이 보안보다 정치에 관한 것일 수 있다고 했다.
SHA-1을 용도와 무관하게 전면 금지하는 조직이 있고 FIPS 140-2 같은 인증이 SHA-1을
권고하지 않는다는 메일을 인용했다.[^0x00cl]
Lobste.rs의 df는 2016년경 해시를 중복 제거에 쓰던 백업 시스템에서 “FIPS가 SHA-256만 허용한다”며 모든 사용자를 옮긴 경험을 적었고,[^df] elobdog는 규정을 지키는 세계는 암호학적 용도가 아니어도 SHA-1을 보면 놀라 이미 진 싸움이라고 했다.[^elobdog]
글은 NIST의 2030년 기한을 마지막에 다루며 독립 트리 해시가 이를 충족시킨다고
주장하지만, 그 규정 담당자들이 이 설명을 받아들일지는 글에서 확인되지 않는다.

## 인사이트

### 해시가 식별자와 신뢰의 근거를 겸하고 있다는 사실이 이 논쟁을 풀 수 없게 만든다

글은 해시가 신뢰의 메커니즘이 아니라고 주장하지만,
생태계는 이미 해시를 신뢰의 근거로 쓰고 있다.
HN의 computerfriend는 커밋 해시에 고정(pin)하면서 이것이 불변 내용을 가리킨다고
기대하고 커밋과 태그 서명이 해시 위에 있으므로 해시의 보안 성질은 Git의 보안
성질이라고 했다.[^computerfriend]
edelbitter는 Rust와 Python의 의존성 관리가 특정 커밋 해시로 버전을 지정한다고
했고,[^edelbitter] Lobste.rs의 mort는 Yocto 레시피, Nix, git 서브모듈, repo와
gclient 같은 도구가 SHA-1을 커밋의 영구 식별자로 가정한다고 했다.[^mort-yocto]
Linus의 2007년 말을 인용한 meinersbur에게 creata는
그렇다면 커밋 서명은 어떻게 동작하느냐고 물었다.[^creata]

이 불일치에서 나오는 2차 효과가 있다.
설계자의 의도(키)와 사용자의 실제 사용(신뢰 앵커)이 어긋난 채로 20년이 흘렀고,
알고리즘을 바꾸는 순간 그 어긋남이 비용으로 드러난다.
해시가 식별자와 신뢰를 겸하는 한 두 역할을 분리하자는 글의 제안(독립 트리
해시)은 의도를 복원하는 일이다.
다만 사용자가 이미 해시를 신뢰로 쓰고 있다면 분리는 그들의 습관과 도구까지
바꾸라는 요구가 된다.

### 알고리즘을 식별자에 새긴 설계는 이전 비용을 영구 부채로 쌓는다

HN의 gandreani는 Fossil이 SHAttered 발표 6일 뒤에 SHA3-256을 추가했고 새
저장소는 SHA3-256이 기본이며 이전 체크인은 SHA-1을 유지해 저장소를 다시 만들
필요도 링크가 깨질 일도 없었다고 했다.[^gandreani]
저자는 기술적으로 Git을 바꾸기가 어려운 것이 아니라 커뮤니티가
문제라고 했고,[^schacon-fossil] fragmede는 세상이 작을 때 세계를 깨는 변경이
쉽다고 했다.[^fragmede]
nicoburns는 이것이 또 하나의 IPv6가 될 징조라고 했고(비호환 구현,
불분명한 이득, 따라와야 하는 많은 도구),[^nicoburns] kccqzy는 Python 3의 경우도
닮았다고 했다.[^kccqzy]

여기서 반례가 흥미롭다.
sltkr는 인터넷은 네트워크 효과
때문에 IPv4 주소가 하나라도 필요하면 모두가 필요하지만,
Git은 저장소마다 따로 옮길 수 있어 즉각적인 이전 압력이 없다고 했다.[^sltkr]
그러나 서브모듈과 외부 참조(해시를 적은 링크, 의존성 고정)는 저장소 사이의
결합이며 이 결합이 네트워크 효과를 만든다(필자의 해석이다).
식별자에 알고리즘을 고정한 설계는 처음에는 단순하지만,
생태계가 커지면 교체가 한 번에 한 저장소가 아니라 결합된 집합 전체를 요구한다.

### 결정을 움직이는 힘은 기술적 우열이 아니라 규정과 공급망 압력이다

글은 기술적 논증으로 반박하는데,
댓글은 결정의 실제 동력이 다른 곳에 있음을 가리킨다.
Onavo는 소프트웨어 공급망을 안전하게 하라는 위에서 아래의 압력(SBOM,
Sigstore)이 있고 정부 고객이 있으면 선택지가 없다고 했고,[^Onavo] artyom은
SHA-1을 전면 금지한 조직이 있다면 그런 기업인과는 논리로 다툴 수 없는 이미 진
싸움이라고 했다.[^artyom]
Lobste.rs의 jrfxxl은 이 결정이 존재하지 않는 즉각적 문제를 막으려는 것이 아니라 앞을 내다보는 것이며, 15년 뒤에도 일부 저장소는 SHA-1을 쓸 텐데 지금 전환하면 그 수가 줄어든다고 했다.[^jrfxxl]
grahamc는 전환이 존재하는 순간 사용자와 자원봉사자와 고객의 시장 압력이 통합을
쉽게 만들 것이라고 낙관했다.[^grahamc]

이 힘들은 글의 논거(해시는 보안이 아니다)와 무관하게 작동한다.
규정 기관이 SHA-1 사용 자체를 문제 삼으면 올바른 기술 논증도
결정을 바꾸기 어렵다.
그러면 글의 가장 실질적 기여는 전환 비용을 명시한 것과,
비용을 낮출 대안을 규정이 허용하는 형태로 제시하려 한 것이다(필자의 평가다).
독립 트리 해시가 규정 담당자에게 받아들여지는지가 이 제안의
실제 운명을 정할 것이다.

### 전환의 성패는 소수의 포지가 UX를 어떻게 설계하느냐에 달렸다

글이 보여 준 GitHub 저장소 생성 화면(형식 선택)은 이 글의 가장
눈에 띄는 설명 도구다.
그러나 HN의 plorkyeran은 GitHub가 SHA-256 저장소를 지원하지 않는 상태에서
저자가 어리석은 방식의 화면을 지어내고 풀 수 없는 문제라고 선언한 것이라며, 처음
푸시되는 내용으로 형식을 정하는 방식은 이상한 생각이 아니라고 했다.[^plorkyeran]
kccqzy도 생성 시가 아니라 첫 푸시 때 형식을 정하면 작은 UX
문제일 뿐이라고 했고,[^kccqzy-ux] watinthedeutsch는 GitHub가 해결할 수 있다고
했다.[^watinthedeutsch]

이 반론이 맞다면 전환의 어려움은 알고리즘이 아니라 몇몇 포지의 설계
결정에 크게 달려 있다.
지원이 포지에 있다는 사실은 이 이전에서 힘이 어디에 있는지를 말해 준다.
수많은 개인 저장소와 도구보다 GitHub 같은 몇 곳의 지원이 먼저 정해지고,
다른 곳들은 그 선택을 따른다(필자의 해석이다).
bkolobara는 작은 git/jj 포지를 운영하는데 지금도 이 문제가 고통스럽고 GitHub는
어떻게 다룰지 상상할 수 없다고 했다.[^bkolobara]
소규모 포지와 도구가 대형 포지의 결정에 맞춰야 하는 구조는 전환이 균등하게
어렵지 않다는 점을 보여 준다.

---

[^pavon]: <https://news.ycombinator.com/item?id=49924709>

[^colinublake]: <https://news.ycombinator.com/item?id=49929836>

[^rurban]: <https://news.ycombinator.com/item?id=49929651>

[^pyfisch]: <https://lobste.rs/s/bytzgl/git_3_0_s_upcoming_sha_256_default_will_be#c_vtz51e>

[^kel]: <https://lobste.rs/s/bytzgl/git_3_0_s_upcoming_sha_256_default_will_be#c_i9ubmu>

[^GrantMoyer]: <https://news.ycombinator.com/item?id=49928611>

[^gorgoiler]: <https://news.ycombinator.com/item?id=49929939>

[^orib]: <https://lobste.rs/s/bytzgl/git_3_0_s_upcoming_sha_256_default_will_be#c_nl7awp>

[^mort-transition]: <https://lobste.rs/s/bytzgl/git_3_0_s_upcoming_sha_256_default_will_be#c_avlzul>

[^schacon-sha1db]: <https://news.ycombinator.com/item?id=49925330>

[^kpcyrd]: <https://news.ycombinator.com/item?id=49924738>

[^schacon-kpcyrd]: <https://news.ycombinator.com/item?id=49924843>

[^Strilanc]: <https://news.ycombinator.com/item?id=49925075>

[^schacon-Strilanc]: <https://news.ycombinator.com/item?id=49925641>

[^bawolff]: <https://news.ycombinator.com/item?id=49929159>

[^hailey]: <https://lobste.rs/s/bytzgl/git_3_0_s_upcoming_sha_256_default_will_be#c_u5tvuv>

[^fanf]: <https://lobste.rs/s/bytzgl/git_3_0_s_upcoming_sha_256_default_will_be#c_ld4rsw>

[^mort-mirrors]: <https://lobste.rs/s/bytzgl/git_3_0_s_upcoming_sha_256_default_will_be#c_wrgrjh>

[^MBCook]: <https://news.ycombinator.com/item?id=49924704>

[^schacon-MBCook]: <https://news.ycombinator.com/item?id=49924747>

[^schacon-peff]: <https://news.ycombinator.com/item?id=49925513>

[^0x00cl]: <https://news.ycombinator.com/item?id=49929168>

[^df]: <https://lobste.rs/s/bytzgl/git_3_0_s_upcoming_sha_256_default_will_be#c_sjr5gm>

[^elobdog]: <https://lobste.rs/s/bytzgl/git_3_0_s_upcoming_sha_256_default_will_be#c_daj2ax>

[^computerfriend]: <https://news.ycombinator.com/item?id=49930044>

[^edelbitter]: <https://news.ycombinator.com/item?id=49929557>

[^mort-yocto]: <https://lobste.rs/s/bytzgl/git_3_0_s_upcoming_sha_256_default_will_be#c_ggzhai>

[^creata]: <https://news.ycombinator.com/item?id=49929225>

[^gandreani]: <https://news.ycombinator.com/item?id=49925011>

[^schacon-fossil]: <https://news.ycombinator.com/item?id=49925170>

[^fragmede]: <https://news.ycombinator.com/item?id=49925204>

[^nicoburns]: <https://news.ycombinator.com/item?id=49924513>

[^kccqzy]: <https://news.ycombinator.com/item?id=49929438>

[^sltkr]: <https://news.ycombinator.com/item?id=49924749>

[^Onavo]: <https://news.ycombinator.com/item?id=49924601>

[^artyom]: <https://news.ycombinator.com/item?id=49929409>

[^jrfxxl]: <https://lobste.rs/s/bytzgl/git_3_0_s_upcoming_sha_256_default_will_be#c_jrfxxl>

[^grahamc]: <https://lobste.rs/s/bytzgl/git_3_0_s_upcoming_sha_256_default_will_be#c_y0yfog>

[^plorkyeran]: <https://news.ycombinator.com/item?id=49929727>

[^kccqzy-ux]: <https://news.ycombinator.com/item?id=49929412>

[^watinthedeutsch]: <https://news.ycombinator.com/item?id=49929971>

[^bkolobara]: <https://news.ycombinator.com/item?id=49924484>
