# Sill: Mac 창 하나를 iPhone과 iPad로 가져오는 무료 오픈소스 앱

<https://getsill.app/>

<https://github.com/Saffsanity/sill>

HN 토론: <https://news.ycombinator.com/item?id=50112739> (249점, 74개 댓글)

GN 토론: <https://news.hada.io/topic?id=35476>

## 소개

Sill은 Mac의 창 하나, 또는 데스크톱 전체를 iPhone이나 iPad에 띄우고
터치, 트랙패드, 키보드, Apple Pencil로 조작하게 하는 앱이다.
Mac 앱은 창을 캡처해 HEVC 영상으로 인코딩해 보내고,
기기에서 한 탭, 클릭, 스크롤, 키 입력은 다시 Mac으로 돌아간다.
계정도, 중간 서버도 없다.[^readme]

Noah Saffer가 만들었고 라이선스는 Apache 2.0이다.
Mac 앱은 웹사이트와 Homebrew 탭으로,
iPhone과 iPad 앱은 App Store에서 무료로 받는다.
광고, 추적, 구독이 없고 GitHub Sponsors 후원은 아무 기능도 열지 않는다.[^readme]
저장소는 2026년 9월 22일에 만들어졌고,
10월 17일 확인 기준 스타 2,849개, 포크 138개다.[^gh-api]
처음 이름은 winstream이었다.[^claude-md]

## 요구 사항

- macOS 14 이상의 Apple silicon Mac
- iOS 17 또는 iPadOS 17 이상의 iPhone이나 iPad
- Mac에서는 창을 보여 주기 위한 화면 기록 권한과,
  클릭과 입력, 창 크기 조절을 위한 손쉬운 사용 권한이 필요하다.
  macOS 15 이상에서는 로컬 네트워크 권한도 필요하다.
- 같은 네트워크, USB 케이블, 직접 무선 연결,
  또는 Tailscale 같은 직접 운영하는 VPN 중 하나로 연결된다.[^readme]

## 동작 방식

### 영상과 입력

Mac 앱은 메뉴 막대에 머문다.
기기가 창을 고르면 ScreenCaptureKit으로 캡처하고,
VideoToolbox로 Mac의 하드웨어 인코더에서 HEVC로 인코딩한다.
하드웨어 인코더가 바쁘면 소프트웨어로 인코딩하고,
연결된 기기가 없을 때는 아무것도 캡처하지 않는다.[^readme]

영상은 TLS 1.3 연결로 기기에 바로 전송된다.
인코더나 연결이 밀리면 프레임을 쌓지 않고 버려서
화면이 늘 현재 상태를 보이게 한다.
연결이 따라오지 못하면 Mac이 프레임을 잡아 두고 있다는 사실을 기기에 알리고,
기기는 이를 화면에 표시하며 연결이 감당할 수 있는 화질을 제안한다.

입력은 같은 경로를 반대 방향으로 거친다.
Mac 앱은 손쉬운 사용 권한으로 이를 마우스와 키보드 이벤트로 바꾼다.
세 손가락 쓸기와 오므리기는 Mac 트랙패드처럼
Mission Control과 App Exposé 등으로 이어진다.
앱의 메뉴도 손쉬운 사용 API로 읽어
iPad 메뉴 막대나 Sill의 메뉴 버튼에 보여 준다.

### 연결과 페어링

가까이 있을 때는 Bonjour로 Mac을 찾고,
USB 케이블로 연결하면 케이블을 쓴다.
공유 네트워크가 없으면 AirDrop처럼 P2P Wi-Fi를 쓰는 직접 무선 연결을 쓸 수 있다.
집 밖에서는 원격 접근을 켜고
직접 운영하는 VPN이나 공유기의 포트 포워딩으로 접속한다.[^readme]

기기마다 한 번 페어링한다.
Mac이 보여 주는 코드를 스캔하거나 12자리 숫자를 입력하며,
USB 케이블로 연결하면 저절로 페어링된다.
그 뒤로 모든 연결은 서로의 키에 고정(pinning)된다.
페어링 요구를 끄면 같은 네트워크의 어떤 기기든 접속할 수 있지만
여전히 암호화된다.

### 그 밖의 기능

- 클립보드는 텍스트만, 한 번에 256KB까지 양방향으로 오간다.
  기기의 클립보드를 Sill이 스스로 읽지는 않고,
  비밀번호 관리자가 숨김으로 표시한 항목은 Mac에 남는다.
- Aa 버튼은 스트리밍하는 창의 크기를 Mac에서 바꿔 글자 크기를 맞추고,
  스트리밍이 끝나면 원래 크기와 위치로 돌려놓는다.
- 가상 디스플레이는 스트리밍하는 창을 전용 디스플레이로 옮겨
  다른 창에 가려져도 계속 갱신되게 한다.
  비공개 macOS API를 쓰며,
  Mac 앱을 Mac App Store가 아니라 웹사이트로 배포하는 이유 중 하나다.
- 접는 iPhone Duo에서는 경첩 상태를 따라 화면 배치가 바뀌고,
  접히는 부분에는 조작 요소를 두지 않는다.[^readme]

### 제약

한 번에 창 하나나 데스크톱 전체만 보이고 소리는 전달하지 않는다.
Mac이 깨어 있고 Sill이 열려 있어야 하며, Sill이 Mac을 깨우지 못할 수 있다.
Mac용 0.3.1 이하에서는 로컬 네트워크, 케이블, 직접 무선 연결이
암호화되지 않았고 페어링 없이 접속할 수 있었으므로 업데이트해야 한다.[^readme]
페어링과 암호화는 Mac용 0.4.0에 들어왔고,
0.3.1(9월 27일)과 0.4.0(9월 28일) 사이는 하루였다.[^releases]

## 소스에서 빌드하기

Xcode 27이 필요하고, iPhone Duo 지원 때문에 iOS 앱은 Xcode 27.1 이상이 필요하다.

```bash
Scripts/make-app.sh --install --open
```

이 명령은 SwiftPM으로 Sill.app을 빌드해 자기 Apple Development 인증서로 서명하고
`/Applications/Sill.app`을 교체한다.
배포판은 키와 페어링한 기기를 데이터 보호 키체인에 두는데,
이는 프로젝트의 프로비저닝 프로파일을 가진 Developer ID 빌드만 읽을 수 있다.
그래서 직접 빌드로 바꾸면 권한을 다시 주고 기기도 다시 페어링해야 한다.
`swift run -c release SillHost`로 호스트만 실행할 수도 있지만,
`--pairing`을 붙이지 않으면 페어링도 암호화도 없이 열리므로
개발 중에만 써야 한다.[^readme]

## 분석

### 설계의 중심은 지연 시간이다

기여 규칙은 Swift와 Apple 프레임워크만 쓰고, 서드파티 의존성을 두지 않으며,
서버가 필요한 것은 하지 않고,
화질보다 지연 시간을 앞세운다는 네 가지다.[^readme]
프레임을 쌓지 않고 버리는 결정, 연결이 느릴 때 화질을 낮추라고 제안하는 결정,
집 밖에서 접속하는 기기는 낮은 화질로 시작하는 결정이 모두 이 원칙에서 나온다.

원격 데스크톱 도구는 대개 화질과 지연 사이에서 화질을 지키려다
화면이 밀리는 경험을 낳는다.
Sill은 손가락으로 조작하는 화면에서는 오래된 프레임이
흐린 프레임보다 더 나쁘다고 판단했다.
터치 입력은 눈으로 결과를 확인하며 이어지므로,
화면이 늦으면 다음 입력이 틀린 곳을 누르게 된다.

### Apple 생태계의 빈칸을 개인 개발자가 메운다

Sill은 ScreenCaptureKit, VideoToolbox, 손쉬운 사용 API처럼
Apple이 공개한 부품을 조합해,
Mac 앱 하나를 iPhone에서 터치로 쓰는 기능을 만든다.
가상 디스플레이만 비공개 API를 쓰고,
그 때문에 Mac 앱은 App Store 밖에서 배포된다.[^readme]

이 구조는 Apple 플랫폼에서 개인 개발자가 할 수 있는 일의 경계를 보여 준다.
공개 API의 조합으로 대부분을 해내지만,
마지막 한 걸음은 비공개 API에 기대야 하고,
그 대가로 배포 경로 하나를 포기한다.

HN에서 gumby는 Apple이 이미 iPad를 Mac의 다른 화면으로 쓰게 해 준다며
Sidecar를 들었다.[^gumby]
fbcpck은 Sidecar가 Mac 화면을 iPad로 보내지만
Mac에서 시작하고 Mac에서 조작해야 하는 반면,
Sill은 손에 든 기기에서 시작하고 조작한다는 점이 다르다고 답했다.[^fbcpck-sidecar]
jscheel은 Sidecar가 개별 창과 터치를 지원하지 않는다고 덧붙였다.[^jscheel]
fbcpck은 그동안 Sunshine과 Moonlight 조합을 써 왔는데
손볼 것이 많고 절반은 고장 났다며,
이제 그 구성을 버릴 수 있겠다고 했다.[^fbcpck]

### 저장소가 에이전트와의 작업 일지로 운영된다

`CLAUDE.md`의 “현재 단계” 절에는 클립보드 기능을 만드는 과정이
브랜치, 이슈, PR 번호와 함께 아주 촘촘하게 적혀 있다.
리뷰에서 나온 여덟 가지 지적을 모두 반영했다는 기록,
259개 검사와 72개 뮤턴트를 모두 잡았다는 검증 결과,
그리고 “Noah를 위한 미검증 항목”으로
실제 iPad와 iPhone에서 사람이 확인해야 할 시나리오가 나열되어 있다.[^claude-md]

이 기록은 이 프로젝트가 AI 코딩 에이전트와 함께 만들어지고 있으며,
사람의 역할이 실제 기기에서의 확인과 열린 질문에 대한 결정으로
분리되어 있음을 보여 준다.
기여자에게도 `CLAUDE.md`의 규칙을 따르라고 요구하므로,
이 파일은 에이전트 지시문이자 프로젝트의 설계 문서 역할을 함께 한다.[^readme]
다만 HN의 zephyreon은
이 `CLAUDE.md`가 컨텍스트를 엄청나게 잡아먹는다고 지적했고,[^zephyreon]
ghboo0927은 6,108줄, 464KB라고 셌다.[^ghboo0927]
작업 일지를 지시문 파일에 계속 쌓으면 에이전트가 매 세션 그 전부를 읽어야 한다.
일지와 지시를 분리하지 않은 것은 이 운영 방식의 비용이다.

## 비평

### 원격 접근의 보안 모델을 사용자에게 많이 맡긴다

Sill은 서버가 없다는 것을 장점으로 내세우지만,
그 대가로 집 밖 접속은 사용자의 VPN이나 포트 포워딩에 기댄다.[^readme]
Tailscale 같은 VPN을 쓰면 문제가 적지만,
공유기 포트를 인터넷에 열면
화면 기록과 손쉬운 사용 권한을 가진 앱이 외부에 노출된다.
페어링 키 고정이 있으니 인증은 되어 있지만,
README가 포트 포워딩을 VPN과 나란히 선택지로 안내하는 방식은
위험의 크기에 비해 가볍다.

0.3.1 이하 버전이 로컬 연결을 암호화하지 않았고
페어링 없이 접속을 받았다는 점도 같은 맥락이다.[^readme]
이 버전들은 저장소가 만들어지고 일주일 남짓 사이에 나왔고,
다음 날 0.4.0으로 고쳐졌다.[^releases]
빠른 수정은 칭찬할 만하지만,
이 기간에 내려받은 사용자가 업데이트하지 않으면
Mac의 화면과 입력이 같은 네트워크에 열린 채로 남는다.

### “무료”가 지속 가능한지는 아직 알 수 없다

Sill은 후원이 개발자 계정 비용을 돕는다고만 말한다.[^readme]
iPhone Duo, iPadOS 26의 메뉴 막대, 새 Xcode 요구 사항처럼
Apple 플랫폼은 해마다 바뀌고, 비공개 API는 언제든 깨질 수 있다.
1인 개발 프로젝트가 이 변화를 계속 따라갈 수 있는지는
기술이 아니라 지속 가능성의 문제다.

에이전트와 함께 만든다는 점이 이 부담을 줄여 줄 수는 있다.
그러나 `CLAUDE.md`가 보여 주듯
실제 기기 확인은 여전히 한 사람에게 몰려 있다.[^claude-md]
기능이 늘수록 그 사람이 확인해야 할 시나리오도 늘어난다.
HN의 outlore가 대안으로 든 Astropad Workbench에
jdalgetty가 연 100달러라는 가격을 문제 삼은 것처럼,[^outlore][^jdalgetty]
사용자는 무료와 일회성 구매를 원하지만,
그 기대가 1인 개발자의 지속 가능성과 맞물리는 방식은 아직 정해지지 않았다.

## 인사이트

### 에이전트 시대의 앱은 ‘작은 기능을 완성도 높게’ 만드는 쪽으로 간다

Sill은 창 하나를 보여 주는 단순한 기능이지만,
클립보드 하나에도 비밀번호 관리자 항목 제외, Universal Clipboard 처리,
macOS 15.4의 붙여넣기 개인정보 동작까지 다룬다.[^claude-md]
예전에는 1인 개발자가 이런 예외 상황(edge case)까지 챙기기 어려웠다.
에이전트가 계획, 구현, 뮤테이션 테스트를 맡으면서
작은 앱도 상용 제품 수준의 세부를 갖출 수 있게 되었다.
경쟁력은 기능의 수가 아니라 한 기능을 얼마나 깊이 다듬었는지로 옮겨 간다.

### ‘사람이 확인할 것’ 목록이 새로운 협업 형식이 된다

`CLAUDE.md`의 미검증 항목 목록은
에이전트가 할 수 없는 일을 사람에게 명시적으로 넘기는 형식이다.
실제 기기, 실제 네트워크, 실제 비밀번호 관리자에서만 확인할 수 있는 것들이다.
이 형식은 에이전트가 “다 했다”고 말하는 대신
무엇을 검증했고 무엇을 검증하지 못했는지 나누어 보고하게 한다.
다른 프로젝트에서도 에이전트에게 작업을 맡길 때,
검증한 것과 사람이 확인해야 할 것을 분리해 적게 하는 규칙을
그대로 가져다 쓸 수 있다.

### 배포와 홍보까지 에이전트가 맡는다

HN의 alin23은 YouTube 추천으로 23만 회 조회된 1분짜리 영상을 보고
이 앱을 처음 알았다며,
Claude가 Hyperframes로 데모 영상을 만드는 데 꽤 능숙해진 것 같다고 했다.[^alin23]
앱을 만드는 일뿐 아니라 알리는 일까지 에이전트가 거들면서,
1인 개발자가 큰 조직 없이도 제품을 널리 퍼뜨릴 수 있게 되었다.
Apache 2.0으로 공개된 덕에
HN에는 곧 Android에서 Mac 창을 조작하는 Sill for Android가
Show HN으로 올라왔다.[^sill-android]
오픈소스 프로토콜 위에 다른 사람이 클라이언트를 붙이는 속도도
같은 도구 덕분에 빨라지고 있다.

---

[^readme]: Saffsanity/sill, [README.md](https://github.com/Saffsanity/sill/blob/main/README.md), 2026-10-17 확인

[^gh-api]: GitHub API, [Saffsanity/sill](https://api.github.com/repos/Saffsanity/sill), 2026-10-17 확인

[^claude-md]: Saffsanity/sill, [CLAUDE.md](https://github.com/Saffsanity/sill/blob/main/CLAUDE.md), 2026-10-17 확인

[^releases]: Saffsanity/sill, [Releases](https://github.com/Saffsanity/sill/releases), 2026-10-17 확인

[^gumby]: <https://news.ycombinator.com/item?id=50112821>

[^fbcpck-sidecar]: <https://news.ycombinator.com/item?id=50115845>

[^jscheel]: <https://news.ycombinator.com/item?id=50113505>

[^fbcpck]: <https://news.ycombinator.com/item?id=50115352>

[^zephyreon]: <https://news.ycombinator.com/item?id=50115248>

[^ghboo0927]: <https://news.ycombinator.com/item?id=50121137>

[^outlore]: <https://news.ycombinator.com/item?id=50114786>

[^jdalgetty]: <https://news.ycombinator.com/item?id=50118546>

[^alin23]: <https://news.ycombinator.com/item?id=50113416>

[^sill-android]: <https://news.ycombinator.com/item?id=50123065>
