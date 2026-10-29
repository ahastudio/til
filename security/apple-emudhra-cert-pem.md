# Apple의 개발자 도구는 침해된 eMudhra 인증서를 아직 신뢰한다

원문: [Apple's git still trusts the compromised eMudhra certificates](https://emudhra.we-have-a-problem.com/apple.html)

HN 토론: <https://news.ycombinator.com/item?id=50271640> (1137점, 397개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/xybmsj/apple_s_git_still_trusts_compromised> (105점, 23개 댓글)

GN 토론: <https://news.hada.io/topic?id=36167>

## 요약

이 글은 eMudhra 사건을 정리하는 사이트에 2026년 10월 28일 올라온 별도 페이지다.
사이트는 Dennis Jackson이 운영하고 여러 기여자가 함께 만든다.
글의 주장은 이렇다.
Apple은 10월 17일에 사건을 통보받았다.
그런데 10월 28일 현재 macOS에 들어 있는 개발자 도구,
곧 git, curl, python3는 침해된 인증서를 여전히 신뢰한다.
10월 26일에 나온 macOS 27.2도 문제를 고치지 못했고,
사용자가 손으로 적용해 둔 우회 조치까지 되돌려
다시 취약한 상태로 만들었다고 한다.
한편 자원봉사자가 운영하는 곳을 포함한 수십 개 프로젝트는
며칠 전에 수정본을 냈다.

글은 영향을 이렇게 설명한다.
이 도구들이 맺는 HTTPS 연결은 누구든 가로챌 수 있다.
git이라면 `https://` 원격에서 clone과 pull을 할 때
공격자가 고른 코드를 받게 될 수 있고,
push한 내용이 전송 중에 바뀔 수 있으며,
GitHub 토큰 같은 자격 증명이 가로채일 수 있다.
GitHub로 가는 경로 위에 있는 사람은 트래픽을 스스로 돌려놓을 수 있어서,
공격에 따로 옵션이 필요하지 않다고 한다.

영향 여부는 직접 확인할 수 있다.
`git ls-remote https://git-emudhra.we-have-a-problem.com/check.git`을
실행해 인증서 오류가 나오면 보호된 것이고,
커밋 목록이 나오면 영향을 받는 것이다.
공격 전체를 보려면 임시 디렉터리에서 다음 명령을 실행한다.

```bash
git -c http.curloptResolve=github.com:443:15.235.19.186 clone https://fake-user@github.com/galadran/emudhra-git-test
```

이 명령은 침해된 eMudhra 중간 인증서 가운데 하나가 발급한
github.com 인증서를 내미는 테스트 서버에서 저장소를 받아 온다.
`-c` 옵션은 이 명령 한 번에 한해 `github.com`을 테스트 서버로 돌린다.
패치된 git은 인증서 오류로 거부하고,
복제가 성공하면 `README.md`가 `INTERCEPTED`로 시작한다.
`fake-user@` 접두어는 지우면 안 된다.
지우면 git이 GitHub 자격 증명을 테스트 서버로 보내기 때문이다.
curl은 `https://dv-g3b-noct-emudhra.we-have-a-problem.com/`와
`https://dv-g3b-aaa-noct-emudhra.we-have-a-problem.com/`로 확인하며,
인증서 오류가 나오면 보호된 것이다.
Apple이 함께 배포하는 다른 도구도 같은 방식으로 영향을 받는다고 한다.

글은 Apple에 수정을 요구한다.
Safari와 Apple의 네트워킹 프레임워크(networking framework)로 만든 앱은
이미 보호되어 있으므로,
macOS 개발자용 수정을 가능한 한 빨리 내야 한다는 것이다.
예로 든 방법은 `/etc/ssl/cert.pem`에서 영향받는 루트를 지우는 것이다.
그사이 개발자는 사이트 메인 페이지의 macOS 우회 절차로
영향받는 루트를 손으로 지울 수 있다.
글은 Apple의 안내가 macOS 업데이트로 수정이 되돌려질 수 있다고
밝히고 있으므로,
업데이트마다 위 확인과 우회를 반복하라고 권한다.[^apple-support]
보안팀에는 CI나 빌드 인프라에서 macOS 러너(runner)를 쓰는지 따져 보고
공급망 위험을 평가하라고 한다.

## 분석

### 같은 Mac에서 인증서를 검증하는 경로가 둘이다

Apple 안내에 따르면 Apple은 10월 19일부터
침해된 중간 인증서(intermediate certificate) 12장을
차단(block)했다.[^apple-support]
이 차단은 소프트웨어 업데이트 없이
인증서 설정 데이터로 장치에 자동 전달된다.[^apple-support]
Safari, Mail, Apple의 네트워킹·보안 프레임워크를 쓰는 앱은
이 차단을 따른다.[^apple-support]
반면 curl, git, python3, ruby, perl, openssl은
`/etc/ssl/cert.pem` 파일에 대해 인증서를 확인하며,
이 파일의 루트로 이어지는 인증서에는
Apple의 차단도, 폐기(revocation) 여부도 확인하지 않는다.[^apple-support]

그래서 원문의 주장은 Apple이 아무것도 하지 않았다는 뜻이 아니다.
정확히 읽으면 이렇다.
Apple에는 장치로 곧바로 내려보내는 빠른 차단 경로가 있고,
이 경로가 터미널 도구에는 닿지 않는다.
이 도구들이 믿는 루트 인증서 목록(root certificate store)은
OS 업데이트로만 갱신되는 파일이어서 수정도 업데이트를 기다린다.
Apple 안내도 이 파일을 향후 macOS 업데이트에서
갱신하겠다고 적었다.[^apple-support]

HN의 stingraycharles는 git이 판단을 OS에 맡기는 것은 옳은 설계이고
문제는 macOS에 있다고 적었다.[^stingraycharles]
그래서 제목도 git이 아니라 macOS와 그것에 기대는
모든 응용 프로그램을 주어로 삼았어야 한다는 것이다.[^stingraycharles]
Lobste.rs의 mxey는 git이 Xcode Command Line Tools에 들어 있다고 짚었다.[^mxey]
Apple 안내도 영향받는 도구를 macOS에 포함된 것과
Xcode Command Line Tools에 든 것으로 나누어 적는다.[^apple-support]

### 수정은 OS 릴리스 일정에 묶여 있다

Apple 안내는 10월 23일에 게시되었고,
터미널 도구에 대한 변경은
향후 소프트웨어 업데이트로 제공된다고 했다.[^apple-support]
그 사흘 뒤인 10월 26일에 macOS Golden Gate 27.2가 나왔다.[^apple-27-2]
원문은 이 업데이트에 수정이 없다고 하는데,
27.2의 보안 콘텐츠 문서에는 eMudhra나 `/etc/ssl/cert.pem`을
다룬 항목이 없다.[^apple-27-2]
다만 이 문서는 CVE 번호가 붙은 항목을 나열하는 형식이어서,
인증서 목록 변경이 거기에 실리지 않았을 가능성은 남는다.
따라서 이 문서는 원문과 어긋나지 않는다는 정도의 증거일 뿐
수정이 없다는 확인은 아니다.
직접 확인하는 길은 업데이트 후에 같은 `git ls-remote` 명령을 돌려 보는 것이다.

원문이 통보일과 릴리스일을 나란히 놓은 이유도 여기서 읽힌다.
통보(10월 17일)에서 27.2 릴리스(10월 26일)까지는 9일이다.
그 사이 Apple은 임시 안내를 냈고 장치 쪽 차단은 이미 적용했지만,
터미널 도구에 닿는 수정은 릴리스에 담지 못했다는 것이 글의 구도다.

### 근거가 독자가 직접 실행할 수 있는 명령이다

글의 가장 강한 근거는 서술이 아니라 명령이다.
`git ls-remote` 확인은 테스트 서버의 인증서가
침해된 중간 인증서에서 나왔을 때
클라이언트가 연결을 받아들이는지만 묻는다.
공격자의 위치는 필요하지 않다.

`clone` 시연은 한 걸음 더 나아간다.
`http.curloptResolve`로 `github.com`을 테스트 서버로 돌려서
네트워크 경로 위의 공격자가 하는 일을 명령 한 줄로 흉내 낸다.
`fake-user@` 접두어를 요구해
시연 중에 자격 증명이 새지 않게 한 점도 설계의 일부다.
이 시연이 보이는 것은 클라이언트가 그 인증서를 받아들인다는 사실이다.
공격자가 이 키를 실제 트래픽에 쓴다는 사실까지 보이지는 않는다.

### 임시 조치가 중간 인증서가 아니라 루트를 지우는 이유

Apple 안내에 따르면 차단된 12장은
중간 인증서 6종이 각각 두 장씩 가진 결과다.[^apple-support]
한 장은 emSign Root TLS CA - G3가 발급해
emSign ECC Root CA - G3로 이어지고,
다른 한 장은 Sectigo가 교차 서명(cross-sign)해
AAA Certificate Services로 이어진다.[^apple-support]

`cert.pem`은 루트 인증서를 모아 둔 파일이다.
이 파일만 보는 도구에는 중간 인증서 하나만 거부하라고 적을 자리가 없을 것이다.
이는 이 문서의 추정이고, Apple 안내가 직접 말한 내용은 아니다.
그래서 임시 조치는 중간 인증서 대신 그 위의 루트를 지우는 방식이 된다.
Apple 안내는 emSign ECC Root CA - G3만 지우면
Sectigo가 교차 서명한 6장이
AAA Certificate Services를 통해 계속 검증되므로
이 루트도 지우는 것을 선택 사항으로 안내한다.[^apple-support]

HN의 gringofyx도 평면 `cert.pem` 파일에는
이 중간 인증서를 불신한다고 적을 수 없다고 짚었다.[^gringofyx]
그는 Safari를 보호한 Security.framework와 `trustd` 경로가 이미 있으니
CLI도 그 경로로 보내면 좋겠다고 덧붙였다.[^gringofyx]
josephcsible는 루트만 지우면 부작용이 거의 없지 않느냐고 물었다.[^josephcsible]
Ajedi32는 그 루트가 서명한 다른 중간 인증서가
여전히 신뢰될 수 있다고 답했다.[^Ajedi32]

비용은 이 파일을 쓰는 모든 도구에 돌아간다.
이 루트들로 이어지지만 침해되지 않은 다른 중간 인증서를 거치는
웹사이트의 인증서가 일부 도구에서 검증되지 않을 수 있다고
Apple은 경고한다.[^apple-support]

## 비평

### 더 나쁘게라는 대비는 Apple 문서가 이미 설명한 동작이다

원문은 27.2가 수정 없이 나온 데서 그치지 않고
사용자가 적용한 우회까지 되돌렸다며 이를 더 나쁜 소식으로 전한다.
그런데 같은 글이 몇 줄 아래에서
Apple 안내가 업데이트로 수정이 되돌려질 수 있다고 밝혔다고 적는다.
Apple 안내는 10월 23일에 이미 `/etc/ssl/cert.pem`이
Apple 버전으로 교체될 수 있으니
업데이트마다 우회를 다시 확인하라고 적었다.[^apple-support]
되돌려짐 자체는 뜻밖의 사건이 아니라 문서에 적힌 동작이다.
HN의 majewsky는 손으로 정리해 둔 `/etc/ssl/cert.pem`이
27.2를 설치하면 원래대로 돌아가 eMudhra CA가 다시 들어간다고 전했다.[^majewsky]
그가 근거로 든 것은 다른 사용자들의 Mastodon 글이어서
직접 확인한 내용은 아니다.[^majewsky]
Lobste.rs의 sri는 Apple이 안내문에 업데이트마다 인증서를 다시 지우라고
적어 둔 점을 두고, 곧 고치지 않을 사적인 이유가 있는 듯하다고 추측했다.[^sri]
그는 이 작업을 매크로나 스크립트로 자동화하라고 권했다.[^sri]

글이 겨눌 지점은 따로 있다.
통보를 받은 지 9일 뒤,
임시 안내를 낸 지 사흘 뒤에 나온 릴리스가
수정을 담지 않았다는 점이다.
이 주장을 가장 강하게 세우려면 27.2에 수정이 없다는 확인이 필요한데,
원문은 그 근거를 따로 대지 않는다.
반증 조건은 간단하다.
우회를 적용하지 않은 Mac에서 27.2로 올린 뒤
`git ls-remote` 확인이 인증서 오류로 끝난다면 원문이 틀린 것이다.

### 수십 개 프로젝트와의 대비는 같은 일을 비교하지 않는다

원문은 자원봉사자가 운영하는 프로젝트도 며칠 전에 수정했다는 말로
Apple의 지연을 부각한다.
그러나 두 일은 단위가 다르다.
다른 프로젝트는 자기 인증서 번들(bundle)을 고쳐 릴리스하면 끝나지만,
Apple의 `cert.pem`은 macOS 업데이트로 갱신되는 시스템 파일이다.
이 차이는 앞의 분석에서 본 대로 Apple 안내에 적힌 구조에서 나온다.

그렇다고 이 차이가 지연을 변호해 주지는 않는다.
Apple에는 업데이트 없이 내려보내는 차단 경로가 이미 있고,
10월 19일에 그 경로를 썼다.[^apple-support]
더 날카로운 질문은 왜 느린가가 아니라
왜 빠른 경로가 터미널 도구에 연결되어 있지 않은가다.
Apple 안내는 그 이유를 설명하지 않고,
원문도 묻지 않는다.

HN의 pram은 macOS에 Background Security Improvements라는
작은 업데이트 경로가 있지만 거의 쓰이지 않는다고 적었다.[^pram]
saagarjha는 Apple이 그 주에 낼 하드웨어를 위해 27.2를 서둘러 내느라
인증서 저장소 변경을 합치지 못했을 것이라고 짐작했다.[^saagarjha]
그는 이를 짐작으로 밝혔고,
Apple이 릴리스를 빨리 검증하거나 작은 패치를 내보내는 데
번번이 실패해 왔다고 평가했다.[^saagarjha]
Lobste.rs의 snej도 짐작으로, `/etc` 아래 파일을 건드리는 보안 업데이트를
만들고 시험하고 내보내는 절차가 OS 신뢰 설정을 갱신하는 절차와 따로 있어
더 느릴 것이라고 적었다.[^snej]
그는 Apple, Google, Sun에서 일한 경험을 들어
큰 회사일수록 일이 오래 걸린다고 했다.[^snej]

### 심각도를 서술한 문장이 공격 조건을 줄여 쓴다

원문은 누구든 이 도구들의 HTTPS 연결을 가로챌 수 있다고 쓴다.
실제 공격에는 조건이 둘 겹친다.
공격자가 피해자와 서버 사이의 네트워크 경로에 있어야 하고,
침해된 중간 인증서의 개인키를 가지고 있어야 한다.
Apple 안내도 이 6종의 키를 가진 사람이
어떤 웹사이트에든 유효해 보이는 인증서를 만들 수 있다고 적었다.[^apple-support]
글은 첫 번째 조건을 뒤에서 인정하지만,
첫 문단의 문장은 그 조건을 빼고 쓴다.

HN의 한 논쟁에서 ryeights는 인증서 투명성(Certificate Transparency)을
강제하는 휴대폰과 브라우저에서는 이런 인증서로 바꿔치기한 연결이
실패한다고 반박했다.[^ryeights]
이 반박이 맞다면 노출은 투명성 검증을 하지 않는 클라이언트에 몰린다.
터미널 도구가 거기에 속한다는 것은 이 문서의 추정이며,
어느 쪽 문서도 확인하지 않았다.

실제 악용 사례는 원문과 Apple 안내 어느 쪽에도 나오지 않는다.
이는 위험이 작다는 뜻이 아니라,
위험의 크기가 공격자의 위치와 키 보유로 정해진다는 뜻이다.
따라서 독자가 따질 것은 자기 도구가 영향을 받느냐에 그치지 않고,
자기 트래픽이 어떤 네트워크 경로를 지나느냐다.

### 제안한 수정은 자기 비용을 말하지 않는다

원문이 Apple에 예로 든 수정은 `cert.pem`에서 영향받는 루트를 지우는 것이다.
그런데 이 방식은 Apple이 임시 조치에 붙인 경고,
곧 침해되지 않은 중간 인증서를 거치는 사이트가
일부 도구에서 검증되지 않을 수 있다는 비용을 그대로 진다.[^apple-support]
원문은 이 비용을 언급하지 않는다.

Apple은 이미 침해된 중간 인증서 12장을 개별로 차단하고 있다.[^apple-support]
같은 차단 정보를 터미널 도구가 읽게 하는 편이
루트를 지우는 것보다 부작용이 작을 수 있다.
이는 이 문서의 추정이다.
Apple 안내는 향후 변경을 사용자가 파일을 고치지 않아도 받게 된다고만 하고,
그 변경이 루트 제거인지 다른 방식인지는 밝히지 않는다.[^apple-support]

## 인사이트

### 인증서 번들은 도구마다 복사된 의존성이다

루트 인증서 번들은 도구마다 하나씩 들어 있는 복사본이다.
원문이 말하는 수십 개 프로젝트의 수정은
같은 데이터를 수십 곳에서 따로 고친 작업이다.
Apple 안내도 어떤 앱과 도구는 자체 루트 인증서 목록을 들고 있어서
Apple의 차단이나 `/etc/ssl/cert.pem`을 따르지 않는다고 적었다.[^apple-support]
한 대의 Mac 안에서도 복사본이 여럿이라는 뜻이다.
HN에서 Homebrew 메인테이너 woodruffw는
Homebrew가 자체 CA 번들을 배포하므로 그 curl 등은 영향받지 않지만
git은 아직 영향받고 있어 지금 고치는 중이라고 적었다.[^woodruffw]
번들을 따로 두는 배포판 안에서도 복사본이 하나씩 남을 수 있다는 사례다.

여기서 나오는 2차 효과가 있다.
불신(distrust) 사건이 터졌을 때 사용자가 노출되는 기간은
가장 빨리 고친 복사본이 아니라
자기가 쓰는 가장 느린 복사본이 정한다.
Apple이 10월 19일에 장치 쪽을 막았어도
사용자가 Terminal에서 쓰는 도구 하나가 느리면
그 도구를 쓰는 동안은 열려 있다.
사건이 반복될수록 이 복사본들의 갱신 주기 차이가
그대로 노출 기간의 차이가 된다.

이 구조는 코드 의존성을 각 프로젝트에 복사해 넣는 벤더링(vendoring)과 같다.
보안 수정이 나와도 복사본마다 따로 올려야 하고,
어느 복사본이 낡았는지는 그 도구를 직접 돌려 보기 전에는 모른다.
그래서 독자가 쓸 수 있는 방어는 목록을 외우는 것이 아니라
도구마다 같은 확인 명령을 돌려 보는 것이다.

### 보호받는 사람과 노출되는 사람이 갈린다

Apple 안내는 Terminal을 쓰지 않는다면 할 일이 없다고 한다.[^apple-support]
Safari, Mail, Apple의 프레임워크를 쓰는 앱은
이미 차단을 따르기 때문이다.
다수의 사용자에게는 맞는 안내다.

그러나 남는 위험은 가장 값비싼 자격 증명이 있는 쪽에 쌓인다.
Terminal에서 git으로 push하는 개발자의 토큰,
빌드 서버가 외부에서 받아 오는 의존성,
배포용 키가 모두 이 도구들을 거친다.
원문이 보안팀에 CI의 macOS 러너를 점검하라고 한 것은 이 때문이다.
호스팅 업체가 제공하는 러너 이미지가
우회를 적용했는지는 알려지지 않았다.
러너 안에서 확인 명령을 직접 실행하면 알 수 있다.
Lobste.rs의 muvlon은 직접 영향받는 사용자가 소수여도
개발자와 git 사용자는 침해되면 훨씬 큰 집단에 미치는
공급망 공격으로 이어질 수 있는 가치 높은 표적이라고 짚었다.[^muvlon]
ianloic은 Apple이 제공하는 명령줄 도구의 보안에
기대는 사람은 없다고 적었다.[^ianloic]
hailey는 그렇게 단정할 근거가 무엇이냐고 되물었다.[^hailey]

실행할 규칙은 이렇다.
macOS를 쓰는 CI 작업의 첫 단계에서 `git ls-remote` 확인을 돌리고,
커밋 목록이 나오면 작업을 실패시킨다.
인증서 오류 말고 다른 이유로 명령이 실패할 수도 있다.
테스트 서버에 연결하지 못한 경우가 그렇다.
그러니 실패 사유가 인증서 오류인지 오류 문구를 읽어서 확인해야 한다.
오류 문구가 인증서 문제를 가리키지 않으면
보호된 것으로 간주하지 말고 결과 없음으로 처리한다.

### 루트 목록의 거친 단위가 사건마다 같은 선택을 강요한다

`cert.pem`처럼 루트만 담는 목록에서는
부분 불신을 표현할 방법이 없다는 것이 앞서 세운 추정이다.
이 추정이 맞다면 중간 인증서 몇 장이 침해될 때마다
관리자는 노출을 감수할지 루트를 지워 일부 사이트의 검증 실패를 감수할지
고르게 된다.
Apple이 AAA Certificate Services 제거를 선택 사항으로 둔 것이
그 선택을 사용자에게 넘긴 표시다.[^apple-support]
HN의 6thbit는 이 루트를 지우지 않으려면
시스템의 모든 프로그램이 중간 인증서까지 폐기 확인을 지원해야 하는데
그것은 보장하기 어렵다고 짚었다.[^6thbit]
그는 대부분의 신뢰 저장소가 지난주에 이 루트도 뺐다고 적었다.[^6thbit]

선택의 기준은 자기 환경에서 검증해 볼 수 있다.
AAA Certificate Services를 지우기 전에
자기 서비스와 의존하는 외부 사이트의 인증서가 그 루트로 이어지는지 확인한다.
확인할 방법이 없으면 emSign ECC Root CA - G3만 지우고
나머지 6장은 노출된 채로 둘지 팀이 정한다.
어느 쪽이든 Apple 안내가 말한 대로 백업을 남기고,
업데이트마다 확인 명령을 다시 돌린다.[^apple-support]
업데이트가 파일을 교체했다면 오래된 백업 `/etc/ssl/cert.pem.orig`를
지우고 절차를 처음부터 반복하라는 안내도 함께 지킨다.[^apple-support]

---

[^apple-support]: Apple Support, [About the compromised eMudhra intermediate CAs](https://support.apple.com/en-us/149555), 2026-10-23

[^apple-27-2]: Apple Support, [About the security content of macOS Golden Gate 27.2](https://support.apple.com/en-us/149521), 2026-10-26

[^stingraycharles]: <https://news.ycombinator.com/item?id=50273818>

[^gringofyx]: <https://news.ycombinator.com/item?id=50273254>

[^josephcsible]: <https://news.ycombinator.com/item?id=50273578>

[^Ajedi32]: <https://news.ycombinator.com/item?id=50273746>

[^majewsky]: <https://news.ycombinator.com/item?id=50272549>

[^pram]: <https://news.ycombinator.com/item?id=50273246>

[^saagarjha]: <https://news.ycombinator.com/item?id=50278126>

[^ryeights]: <https://news.ycombinator.com/item?id=50275231>

[^woodruffw]: <https://news.ycombinator.com/item?id=50274493>

[^6thbit]: <https://news.ycombinator.com/item?id=50273333>

[^mxey]: <https://lobste.rs/s/xybmsj/apple_s_git_still_trusts_compromised#c_jmf9l4>

[^sri]: <https://lobste.rs/s/xybmsj/apple_s_git_still_trusts_compromised#c_gprgh6>

[^snej]: <https://lobste.rs/s/xybmsj/apple_s_git_still_trusts_compromised#c_ppmruj>

[^muvlon]: <https://lobste.rs/s/xybmsj/apple_s_git_still_trusts_compromised#c_5k4ljb>

[^ianloic]: <https://lobste.rs/s/xybmsj/apple_s_git_still_trusts_compromised#c_g04hde>

[^hailey]: <https://lobste.rs/s/xybmsj/apple_s_git_still_trusts_compromised#c_wakjkg>
