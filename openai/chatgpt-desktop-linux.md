# ChatGPT·Codex 데스크톱 앱이 리눅스 프리뷰로 나왔다

원문: [Codex in ChatGPT desktop app for Linux is now in preview 🐧](https://community.openai.com/t/codex-in-chatgpt-desktop-app-for-linux-is-now-in-preview/1390027/6)

## 요약

OpenAI가 2026년 8월 11일 커뮤니티 포럼에 ChatGPT 데스크톱 앱의 리눅스 프리뷰를 알렸다.
게시자는 `sps`이고, ChatGPT와 ChatGPT Work, Codex를 하나의 네이티브 데스크톱 경험으로
묶는다는 것이 골자다.

지원 범위가 명시되어 있다.
Ubuntu 24.04 LTS와 26.04 LTS, Debian 13, Fedora 43·44를 지원하고, x64와 ARM64 아키텍처에
`.deb`와 `.rpm` 패키지로 배포한다.
데스크톱 앱은 프로젝트 관리, 파일 작업, 브라우저 워크플로, 그리고 ChatGPT와 나란히 Codex를
실행하는 작업 공간으로 설계되었다고 소개한다.

기능 동등성(parity)에 대한 질문이 곧바로 나왔다.
`oli.vier`가 Windows와 Linux 버전을 비교할 기능 명세표가 있느냐고 묻자, `sps`는 비교표는
아직 없다며 일화적 정보로 OpenAI의 Tibo Sottiaux의 발언을 인용했다 — “해냈다, 드디어.
Codex와 ChatGPT 데스크톱이 이제 리눅스에서. 기다려 줘서 고맙고, 성급하게 MacBook을 주문했다면
취소해도 된다. 그만큼 좋다.”
`oli.vier`는 이것을 사실상 기능 동등이라는 뜻으로 받아들였다.

프리뷰인 만큼 포럼에는 곧 실사용 문제 보고가 이어졌다.
`suika`는 Fedora 44 KDE Plasma/Wayland·Fcitx 5 환경에서 메시지 작성창에 일본어 입력을
전환할 수 없는 IME 문제를 보고했고, `nobadwords`는 EndeavourOS KDE Wayland에서 한국어
Fcitx5로도 같은 문제를 겪었으며 `--enable-wayland-ime` 플래그로 해결된다고 확인했다.
`suika`는 `--enable-features=UseOzonePlatform --ozone-platform=wayland --enable-wayland-ime`
조합이 XWayland를 강제하지 않고도 입력을 되살렸다고 덧붙였다.
`douglarek`은 Fedora 44가 Wayland인데도 앱이 X11로 폴백되어 4K 모니터에서 화면이 형편없다고
적었다.

패키징과 통합에 대한 지적도 나왔다.
`NY152`는 특정 배포판이 다시 우대받는다며, `.deb`·`.rpm`에 의존하지 않는 Arch Linux나
NixOS는 우회 없이는 쓸 수 없으니 Flatpak이나 최악의 경우 AppImage가 더 현명했을 것이라고
적었다.
`dhao2001`은 같은 머신의 Codex CLI 프로젝트가 데스크톱 앱의 프로젝트 목록에 나타나지 않고,
작업 디렉터리와 git 브랜치가 보존된 CLI 세션이 전부 독립 채팅으로 표시되며, 폴더를 수동으로
추가해도 프로젝트가 비어 있다고 보고했다.
그 밖에 `Neoony`가 직접 다운로드 URL과 WSLg의 WSL Ubuntu 24.04에서도 동작함을 공유했고,
`davfre`는 Hyprland/Wayland에서 음성 입력(Handy)의 가상 키보드 입력이 숫자와 기호로 잘못
해석된다고 적었다.

## 분석

### 이 출시의 진짜 메시지는 Codex가 IDE가 아니라 데스크톱 셸을 노린다는 것이다

리눅스 프리뷰의 표면은 “한 플랫폼이 더 지원된다”이지만, 구성은 그 이상을 말한다.
ChatGPT와 ChatGPT Work와 Codex를 하나의 네이티브 앱에 묶고, 그것을 “프로젝트 관리·파일
작업·브라우저 워크플로”의 작업 공간으로 규정한 것은 IDE 확장이 아니라 별도의 데스크톱
환경을 겨냥한 것이다.

Tibo의 “MacBook 주문을 취소해도 된다”는 발언이 이 방향을 드러낸다.
이 문장은 리눅스 지원을 넘어 “개발자의 주 작업 환경을 우리 앱으로 대체하라”는 제안이며,
그 대상은 에디터가 아니라 데스크톱 전체다.
Codex가 CLI에서 시작해 데스크톱 앱으로 확장되는 궤적은, 에이전트 코딩 도구가 터미널
보조에서 작업 공간의 중심으로 이동하려는 시도의 한 사례다.

이 야심이 곧바로 이 프리뷰의 가장 큰 결함과 충돌한다.
`dhao2001`이 지적한 CLI 세션과 데스크톱 프로젝트의 단절은 단순한 버그가 아니라 이 야심의
시금석이다 — 데스크톱 앱이 작업 공간의 중심이 되려면 같은 머신의 CLI 작업을 흡수해야 하는데,
그러지 못하면 두 개의 분리된 Codex가 공존하게 된다.

### 리눅스가 마지막에 온 것이 아니라 리눅스에서 문제가 먼저 드러난다

이 프리뷰의 포럼 반응은 대부분 Wayland와 IME와 패키징에 관한 것이다.
이것은 리눅스 앱의 품질이 낮아서가 아니라, 리눅스가 Electron/Chromium 기반 앱의 약한
고리를 노출하는 환경이기 때문이다.

Wayland의 IME 처리, X11 폴백, Fcitx5와의 상호작용은 macOS나 Windows에는 없는 변수다.
`suika`와 `nobadwords`가 일본어와 한국어 Fcitx5에서 같은 문제를 재현하고 `--enable-wayland-ime`로
해결한 것은, 이 문제가 특정 설정의 우연이 아니라 Chromium의 Ozone 플랫폼과 리눅스 입력
스택의 구조적 접점임을 보여준다.
같은 문제가 Obsidian 같은 다른 Electron 앱에서도 나타난다는 `suika`의 언급이 이를 뒷받침한다 —
OpenAI 앱의 결함이 아니라 Electron 생태계 전체가 리눅스에서 겪는 문제다.

이 관찰이 중요한 이유는 책임의 위치를 바꾸기 때문이다.
OpenAI가 이 문제들을 하나씩 고칠 수는 있지만, 근본 원인이 Chromium의 Wayland 지원 성숙도에
있다면 그것은 OpenAI가 통제할 수 없는 상류의 문제다.
리눅스 데스크톱 앱을 내는 모든 회사가 같은 벽을 만나며, 이 프리뷰의 포럼은 그 벽의 지도를
제공한다.

### 배포 형식의 선택이 사용자 집단을 미리 가른다

`.deb`와 `.rpm`만 제공하기로 한 결정은 기술적 선택처럼 보이지만 실은 대상 사용자를 정의한다.
`NY152`가 지적한 대로 이 형식은 Ubuntu·Debian·Fedora 계열을 겨냥하고 Arch와 NixOS를 배제한다.

이 배제가 아이러니한 이유는 대상과 실제 사용자층의 불일치 때문이다.
`.deb`·`.rpm`은 데스크톱 리눅스의 주류이지만, 에이전트 코딩 도구를 가장 적극적으로 실험하는
집단에는 Arch와 NixOS 사용자가 두텁다.
Flatpak이나 AppImage가 배포판 중립적이라는 `NY152`의 지적은 정확하며, 그 선택은 특정
배포판을 우대하지 않으면서 더 넓은 사용자에게 닿는 길이었다.

다만 이 선택에도 논리가 있다.
Flatpak 샌드박스는 IME와 파일 접근과 브라우저 워크플로에서 추가 마찰을 만들고, 이 앱이
파일 작업과 프로젝트 관리를 핵심으로 내세운 만큼 샌드박스의 제약이 기능을 해칠 수 있다.
그렇다면 네이티브 패키지 선택은 배포 범위를 좁히는 대신 통합 깊이를 택한 것이며, 이 절충이
명시되지 않은 채 형식만 제시된 것이 문제다.

## 비평

### “기능 동등”이라는 주장이 명세 없이 트윗으로만 제시된다

`oli.vier`의 정당한 질문 — Windows와 Linux 버전의 기능 비교표 — 에 대한 답은 명세표가
아니라 임원의 트윗이었다.
`sps`가 “비교표는 없다”고 인정하고 Tibo의 “그만큼 좋다”를 일화적 정보로 제시한 것은,
동등성 주장의 근거가 검증 불가능한 형태임을 뜻한다.

이 공백이 실무적으로 문제인 이유는 프리뷰의 성격 때문이다.
프리뷰를 평가하려는 사용자는 “무엇이 되고 무엇이 안 되는지”를 알아야 도입 여부를 정하는데,
“MacBook을 취소해도 된다”는 마케팅 문장은 그 정보를 주지 않는다.
그리고 포럼의 나머지 게시물이 곧바로 그 문장을 반박한다 — CLI 통합이 안 되고, IME가 깨지고,
Wayland가 폴백되고, 특정 배포판이 배제된다.
동등성 주장과 실사용 보고 사이의 이 간극은, 임원의 낙관과 프리뷰의 현실 사이의 거리다.

`oli.vier` 본인이 이 간극을 순진하게 메웠다.
Tibo의 트윗을 보고 “사실상 기능 동등이라는 뜻”이라고 받아들인 것[^oli-parity]은, 마케팅
문장이 명세의 부재를 메우는 방식을 그대로 보여준다.
질문은 비교표를 요구했는데 답은 인상을 제공했고, 질문자는 인상을 사실로 변환했다.

### CLI와 데스크톱의 분리는 프리뷰 버그가 아니라 제품 정체성의 문제다

`dhao2001`의 보고 — 같은 머신의 Codex CLI 프로젝트가 데스크톱 앱에 나타나지 않고, 수동으로
추가한 폴더가 비어 있으며, Windows에서 작업 서버로 원격 접속하는 편이 오히려 낫다는
것[^dhao-cli] — 은 프리뷰의 사소한 미완성으로 넘길 수 없다.

이 문제가 깊은 이유는 데스크톱 앱의 존재 이유와 직결되기 때문이다.
Codex는 이미 CLI로 존재하고, 많은 사용자가 그것으로 프로젝트를 관리한다.
데스크톱 앱이 그 위에 값을 더하려면 최소한 기존 CLI 작업을 이어받아야 하는데, 두 인터페이스가
같은 머신에서 서로의 상태를 모른다면 데스크톱 앱은 통합이 아니라 세 번째 분리된 창구가 된다.
`dhao2001`이 “원격 접속이 낫다”고 한 것은 이 분리의 비용을 정확히 표현한다.

이 결함은 앞서 분석한 “데스크톱 셸을 노린다”는 야심과 정면으로 부딪힌다.
작업 공간의 중심이 되겠다는 앱이 같은 머신의 자기 CLI 작업조차 보지 못한다면, 그 야심은
기술적 토대 없이 선언된 것이다.
프리뷰라는 단서가 이 결함을 일시적인 것으로 보이게 하지만, CLI와 데스크톱의 상태 공유는
아키텍처 결정이지 마무리 작업이 아니다.

### 다운로드 UX 불만이 사소해 보이지만 신뢰의 문제를 건드린다

`CoolAiUser`의 불만 — 어떤 페이지는 현재 OS의 다운로드 버튼만 보여주고 다른 페이지는 OS와
무관하게 여러 버튼을 보여주는 비일관성 때문에, Windows에서 리눅스 버전을 받아 VM으로 옮길
수 없다는 것[^cool-download] — 은 표면적으로는 사소한 UX 투정이다.
그러나 그가 붙인 지적이 핵심을 찌른다 — 강력한 AI를 논하면서 사용자가 자기 OS를 고를 IQ가
없다고 가정하는 “아기 취급” 방법을 쓰는 것이 아이러니하다는 것이다.

이 아이러니가 사소하지 않은 이유는 대상 사용자와 설계 가정의 불일치이기 때문이다.
Codex의 사용자는 정의상 명령줄과 VM과 크로스 플랫폼 워크플로를 다루는 개발자다.
그런 사용자에게 “당신 OS의 다운로드만 보여주겠다”는 것은 배려가 아니라 방해이며,
`Neoony`가 곧바로 직접 다운로드 URL을 공유한 것[^neoony-url]이 그 방해의 무용함을 증명한다.
플랫폼이 숨긴 것을 커뮤니티가 즉시 공개한 셈이다.

`oli.vier`가 이 불만을 “꽤 표준적인 일”이라고 일축한 것[^oli-standard]에 `CoolAiUser`가
“언제 어디서 별도 다운로드를 올릴지 비일관적인 게 표준이냐”고 되받은 것[^cool-reply]은,
이 문제가 관행이냐 결함이냐의 논쟁으로 번졌음을 보여준다.
관행이라는 방어는 “다들 그렇게 한다”이고, 결함이라는 지적은 “그 관행이 이 사용자층에는 맞지
않는다”이다.
후자가 옳으며, 개발자 도구가 개발자의 능력을 과소평가하는 설계는 작지만 반복되는 신뢰의
누수다.

## 인사이트

### Electron 데스크톱 앱의 리눅스 지원은 회사가 아니라 Chromium이 결정한다

이 프리뷰의 포럼이 드러낸 가장 이전 가능한 사실은 OpenAI에 관한 것이 아니라 Electron
생태계에 관한 것이다.
IME 파손, X11 폴백, 가상 키보드 오해석은 모두 Chromium의 Ozone/Wayland 계층에서 나오며,
`suika`가 같은 문제를 Obsidian에서도 겪었다고 한 것[^suika-ime]이 그 공통 뿌리를 가리킨다.

이 구조가 함의하는 바는 책임의 상류 이동이다.
OpenAI가 `--enable-wayland-ime`를 기본값으로 넣어 IME 문제를 완화할 수는 있지만, Wayland
지원의 성숙도 자체는 Chromium 프로젝트가 결정한다.
그래서 어떤 회사가 Electron으로 리눅스 데스크톱 앱을 내든, 그 앱의 리눅스 품질 상한은
그 회사의 노력이 아니라 Chromium의 Wayland 지원 수준에 걸린다.
`douglarek`이 “앱이 X11인지 Wayland인지 자동 감지해야 하는데 왜 폴백되는지 모르겠다”고
한 것[^douglarek-x11]은, 사용자가 앱 개발사에 기대하는 것과 실제로 그것을 결정하는 계층이
다르다는 사실의 표현이다.

이 통찰의 실무적 함의는 평가 기준의 이동이다.
Electron 기반 리눅스 앱을 평가할 때 물어야 할 것은 “이 회사가 리눅스를 잘 지원하는가”가
아니라 “이 앱이 최신 Chromium의 Ozone 플랫폼 플래그를 올바르게 켜는가”다.
전자는 마케팅의 영역이고 후자는 검증 가능한 기술적 질문이며, 포럼의 사용자들이 후자를
스스로 알아내 `--ozone-platform=wayland`를 공유한 것이 그 검증이 어디서 이뤄지는지를 보여준다.

### 프리뷰의 포럼은 회사가 만들지 못한 호환성 매트릭스를 대신 만든다

`sps`가 “Windows와 Linux의 기능 비교표는 없다”고 인정한 자리에서, 포럼의 사용자들이 실질적인
호환성 매트릭스를 함께 만들어 냈다.
Fedora 44 KDE에서 IME가 깨지고 GNOME에서는 재시작 후 동작하며[^douglarek-gnome], WSLg에서
돌고[^neoony-url], Hyprland에서 음성 입력이 깨지고[^davfre-stt], Arch·NixOS는 배제된다는
정보의 총합이 그것이다.

이 현상은 프리뷰라는 배포 방식의 숨은 기능을 드러낸다.
회사가 모든 배포판·데스크톱 환경·입력기 조합을 사전에 테스트하는 것은 불가능하고, 프리뷰는
그 테스트를 사용자 집단에 분산시킨다.
`suika`와 `nobadwords`가 일본어와 한국어에서 같은 문제를 교차 확인하고 `douglarek`이 KDE와
GNOME의 차이를 비교하자고 제안한 것[^douglarek-compare]은, 사용자들이 QA 매트릭스를 협업으로
채우는 과정 그 자체다.

그러나 이 분산에는 대가가 있다.
호환성 정보가 회사의 문서가 아니라 포럼 게시물에 흩어져 있으면, 다음 사용자는 자기 조합이
동작하는지 알기 위해 스레드 35개를 뒤져야 한다.
프리뷰가 QA를 크라우드소싱하는 것은 효율적이지만, 그 결과물을 회사가 구조화된 문서로
회수하지 않으면 각 사용자가 같은 발견을 반복한다.
`sps`가 인용한 “MacBook을 취소해도 된다”는 낙관과, 포럼에 쌓인 조건부 동작의 목록 사이의
거리가 이 회수되지 않은 지식의 크기다.

### 데스크톱 셸로의 확장은 에이전트 도구가 IDE와 벌이는 영역 다툼의 신호다

Codex가 CLI에서 데스크톱 앱으로, 그리고 “프로젝트 관리·파일 작업·브라우저 워크플로”를
품는 작업 공간으로 확장되는 궤적은 이 제품 하나의 이야기가 아니다.
에이전트 코딩 도구가 어디에 살 것인가라는 더 큰 질문의 한 답이다.

두 방향이 경쟁한다.
하나는 에이전트가 기존 IDE(VS Code, Zed, JetBrains)의 확장으로 사는 것이고, 다른 하나는
에이전트가 자기 데스크톱 환경을 갖는 것이다.
Codex 데스크톱 앱은 후자를 택했고, ChatGPT와 Work까지 묶어 “개발만이 아니라 지식 노동의
작업 공간”을 노린다.
`dhao2001`이 겪은 CLI 통합 실패는 이 확장이 아직 기술적으로 이르다는 증거이지만, 방향 자체는
분명하다.

이 다툼의 결과가 중요한 이유는 잠금의 형태를 정하기 때문이다.
에이전트가 IDE 확장으로 살면 사용자는 에디터를 유지하고 에이전트를 갈아 끼울 수 있다.
에이전트가 자기 데스크톱 환경을 소유하면 사용자의 프로젝트와 파일과 브라우저 워크플로가 그
환경에 종속되고, 다른 에이전트로 옮기는 비용이 커진다.
“MacBook을 취소하라”는 권유는 하드웨어 선택에 대한 농담처럼 들리지만, 실제로는 작업 환경
전체를 한 벤더의 앱으로 이주시키라는 제안이며, 그 이주의 되돌리기 비용이 이 확장의 진짜
쟁점이다.

## 참고

- 관련 문서: [DeepSeek Harness: 모든 것이 플러그인인 에이전트 하네스](../ai-tool/deepseek-harness.md), [DeltaDB: 대화가 소스가 되는 버전 관리](../agentic-coding/deltadb-conversation-as-source.md)

---

[^oli-parity]: <https://community.openai.com/t/codex-in-chatgpt-desktop-app-for-linux-is-now-in-preview/1390027/10>
[^dhao-cli]: <https://community.openai.com/t/codex-in-chatgpt-desktop-app-for-linux-is-now-in-preview/1390027/20>
[^cool-download]: <https://community.openai.com/t/codex-in-chatgpt-desktop-app-for-linux-is-now-in-preview/1390027/6>
[^neoony-url]: <https://community.openai.com/t/codex-in-chatgpt-desktop-app-for-linux-is-now-in-preview/1390027/7>
[^oli-standard]: <https://community.openai.com/t/codex-in-chatgpt-desktop-app-for-linux-is-now-in-preview/1390027/11>
[^cool-reply]: <https://community.openai.com/t/codex-in-chatgpt-desktop-app-for-linux-is-now-in-preview/1390027/12>
[^suika-ime]: <https://community.openai.com/t/codex-in-chatgpt-desktop-app-for-linux-is-now-in-preview/1390027/14>
[^douglarek-x11]: <https://community.openai.com/t/codex-in-chatgpt-desktop-app-for-linux-is-now-in-preview/1390027/16>
[^douglarek-gnome]: <https://community.openai.com/t/codex-in-chatgpt-desktop-app-for-linux-is-now-in-preview/1390027/22>
[^douglarek-compare]: <https://community.openai.com/t/codex-in-chatgpt-desktop-app-for-linux-is-now-in-preview/1390027/22>
[^davfre-stt]: <https://community.openai.com/t/codex-in-chatgpt-desktop-app-for-linux-is-now-in-preview/1390027/21>
