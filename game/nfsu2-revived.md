# Underground 2 Revived: 2004년 게임의 x86 코드를 C로 옮겨 브라우저에서 온라인으로 돌린다

<https://nfsu2.xyz/>

HN 토론: <https://news.ycombinator.com/item?id=50403052> (509점, 160개 댓글)

GN 토론: <https://news.hada.io/topic?id=36754>

## 소개

Underground 2 Revived는 2004년 PC 게임 Need for Speed: Underground 2를
Chrome과 Firefox에서 돌려 주는 팬 프로젝트다.
소개 문구는 WebGPU 그래픽, Web Audio, 최대 120fps 와이드스크린,
컨트롤러와 휠과 터치 조작, 자유 주행(free roam)과 친구들과의 온라인 경주를
내세운다.
페이지 맨 위에는 Electronic Arts와 무관한 팬 프로젝트라고 적혀 있다.

만든 사람은 어릴 때 형제와 이 게임을 같이 했고,
다시 같이 하려고 브라우저로 옮겨 봤더니
예상보다 잘 돌아서 일이 커졌다고 소개한다.
후원은 호스팅과 개발 비용을 위한 것이고 모두 같은 게임을 받으며 유료 혜택이
없다고 한다.
후원자에게는 Discord 역할만 준다.
이 문서는 사이트를 직접 실행해 보지 않았고,
홈페이지와 저장소 README, HN 댓글에서 읽은 내용만 정리했다.

## 동작 방식

저장소 README에 따르면 게임의 x86 코드를 미리 C로 번역해 WebAssembly로
컴파일한다.[^repo]
Direct3D 9는 WebGPU 위에서, 소리는 Web Audio 위에서 돌린다.[^repo]
번역은 Python 도구(Capstone)가 `SPEED2.EXE`의 모든 함수를 C로 바꾸는 방식이고,
Windows, Direct3D 9, DirectSound, DirectInput은 런타임이 다시 구현한다.[^repo]
게임의 스레드는 하나의 공유 메모리 위에서 워커로 돌고,
서버는 Rust로 짠 것이 페이지와 모듈과 게임 폴더를 내주고 멀티플레이어 연결을
맡는다.[^repo]

이 방식의 뿌리는 Talha Müderrisoğlu의 NFSU2Recomp다.
홈페이지는 이 프로젝트가 NFSU2Recomp의 2026년 10월 16일 MIT 라이선스 버전에서
갈라져 나왔고 그 버전의 코드만 쓴다고 밝힌다.
그 방법 자체는 N64: Recompiled와 XenonRecomp의 정적 재컴파일을 따른 것이다.
HN에서 wg0와 epolanski가 어떻게 만들었느냐고 물은 것도 이
지점이다.[^wg0][^epolanski]

## 직접 돌리려면

README의 요구 조건은 구체적이다.[^repo]

- 게임: 본인이 가진 PC판을 v1.2(북미)로 패치한 것이어야 하고, `SPEED2.EXE`는 4,800,512바이트에 SHA-256이 `f9dd86c0…4168a7`인 파일이어야 한다. 다른 버전은 동작하지 않는다.
- 빌드: Apple Silicon Mac(시험된 환경) 또는 Linux, Python 3, Node.js 20 이상, Rust, wasi-sdk 34가 필요하다. Windows에서는 WSL 2에서 빌드하며 리눅스 파일 시스템에 두어야 한다.
- 플레이: 최신 Chrome, 또는 WebGPU가 되는 Firefox(Windows, macOS)다.

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
web/gen.sh "/path/to/Need for Speed Underground 2/SPEED2.EXE"
web/build.sh
web/start.sh --data "/path/to/Need for Speed Underground 2"
```

위 명령은 README의 빌드와 실행 절차를 줄여 옮긴 것이다.
번역된 C와 컴파일된 모듈은 게임에서 만들어진 것이므로 저장소에 올리지 않는다고
한다.[^repo]
친구와 함께 하려면 서버를 HTTPS 뒤에 두어야 한다.
다른 PC에서는 보안 컨텍스트가 필요하기 때문이며,
`web/deploy/`에 Docker 설정이 있다.[^repo]
HN에서 andix가 직접 호스팅할 수 있느냐고 물은 것의 답은 이 절차다.[^andix]

Linux에서는 별도 조치가 필요하다는 보고가 있다.
popcar2는 Chromium에 `--enable-unsafe-webgpu`와 Vulkan 관련 옵션을 줘야 했다고
적었다.[^popcar2]
이에 herodoturtle는 그 플래그가 웹사이트에 보안 문제를 열 수 있다는 브라우저
경고를 인용하며
어떤 위험인지 알려 달라고 물었고, 이 문서가 읽은 범위에는 답이
없었다.[^herodoturtle]
judge2020은 샌드박스를 유지하는 다른 설정 방법을 올렸지만 Fedora와 NVIDIA
드라이버에 한정된 것이다.[^judge2020]

## 조작과 저장

키보드는 방향키나 WASD로 조향하고 Alt가 니트로, Space가 핸드브레이크다.
자유 주행에서는 `X`가 드리프트 모드이고 `1`~`4`는 다른 플레이어와의 빠른
채팅이다.
세이브는 일시정지에서 차고로 들어가 저장하며,
백업을 내려받아 복원하거나 클라우드 저장으로
기기 사이에 동기화할 수 있다.
온라인에서는 같은 크루 이름(최대 4명)을 쓰는 사람끼리 자유 주행에서 서로 보이고,
친구의 월드로 들어갈 수도 있다.

언어는 13개 언어판과 포르투갈어(브라질), 폴란드어, 터키어, 헝가리어,
우크라이나어,
체코어, 슬로바키아어, 그리스어를 지원한다고 홈페이지가 크레딧과 함께 밝힌다.
번역과 더빙은 대부분 기존 모드 제작자들의 것이다.

## 법적 쟁점

이 프로젝트의 쟁점은 기술이 아니라 권리다.
README는 저장소에 게임의 코드나 데이터가 들어 있지 않으며 사용자가 자기 사본을
가져와야 한다고 밝힌다.[^repo]
그런데 HN 댓글들은 `nfsu2.xyz`가 게임 자산을 직접 내려주고 있다고 읽었다.[^rvz]
MayeulC는 이 게임이 어디서도 팔리지 않는다고 하면서도 자산까지 호스팅하는 것은
법적으로 의심스럽다고 썼다.[^mayeulc]
호스팅 사이트가 실제로 어떤 파일을 내주는지는 이 문서가 확인하지 못했다.
README의 사용자 사본 방식과 호스팅 사이트의 즉시 실행이 어떻게 양립하는지는
홈페이지에 설명이 없다.

후원 요청에 대해서는 의견이 갈렸다.
rustyhancock은 저작권이 있는 콘텐츠에 후원을 받거나 부추기는 것이 의심스럽다고
했고,[^rustyhancock]
rvz는 게임이 오래됐다고 재배포 권리가 생기지는 않으며 후원 요청이 권리자의 눈에
띄게 만들 것이라고 했다.[^rvz]
jareklupinski는 광고나 수익화를 하는 프로젝트가 먼저 내려가고 조용히 있는 곳은
변호사를 덜 끈다고 관찰했다.[^jareklupinski]
이 셋은 법적 전망이 아니라 각자의 추측이다.
AndriyKunitsyn은 미국법에서 상표는 소유자가 분쟁을 피하면 포기된 것으로 볼 수
있으므로
EA가 싸울 수밖에 없다고 설명했지만, 자신은 법률가가 아니라고 밝혔다.[^andriy]

가장 직설적인 입장도 있었다.
hypfer는 이것이 WebAssembly로 컴파일한 해적판일 뿐이라고 했고,[^hypfer]
tevlon의 합법이냐는 물음에 hobofan은 합법이 아니라고 답했다.[^hobofan]
이 문서는 법적 판단을 내릴 수 없다.
분명한 것은 이 사이트가 내려갈 수 있다는 위험을 댓글 여러 개가 같은 방향으로
말한다는 점이다.

## 비평

### 기술 성과와 법적 구조를 한 문장으로 말하면 오해가 생긴다

소개 문구의 게임의 자체 코드를 다시 컴파일했다는 설명은 기술적으로
정확해 보인다.
그러나 정적 재컴파일은 원본 실행 파일이 있어야 하고,
번역 결과는 그 실행 파일에서 나온 파생물이다.
그래서 도구 저장소는 코드를 싣지 않는 방식으로 선을 긋지만,
호스팅 서비스는 그 선 바깥에서 실제 게임을 돌린다.
HN에서 polytely는 이런 프로젝트가 게임 보존을 망칠까 걱정했고,
nonethewiser는 자산이 들어간 디컴파일 배포와 진짜 게임 배포 사이에 차이가 없다고
반박했다.[^polytely][^nonethewiser]
두 의견은 같은 문제의 양면이다.
도구가 합법적일수록 호스팅은 더 눈에 띈다.

### 온라인은 오래 가기 어려운 구조다

diimdeep은 온라인이 로비 목록이 아니라 매치메이킹과 맞는 차종 구성이 있어야
재미있다고 썼다.[^diimdeep]
수천 명이 한 월드에 모이는 자유 주행은 인상적이지만,
이 문서는 서버 규모와 비용을 확인하지 못했다.
후원이 서버 비용을 감당하는지도 알 수 없다.
andix가 오래 못 갈 것 같아 로컬로 돌리고 싶다고 한 반응은 이런 불안정성에서 나온
것이다.[^andix]

### 성능 체감은 환경에 따라 극단적으로 갈린다

senfiaj는 성능이 나빠 실행할 수 없을 정도였고 Chrome의 unsafe WebGPU를 켜야
했다고 했다.[^senfiaj]
반면 KMnO4는 iPhone 14에서 프레임이 완벽하다고 했고,[^kmno4] lbreakjai는 M2 맥북
Firefox에서도 매끄러웠다고 했다.[^lbreakjai]
같은 사이트에 대해 정반대의 보고가 나오는 이유는 WebGPU 지원 상태 차이로
보이지만, 이는 이 문서의 추측이다.
도입 전에 자기 기기에서 먼저 확인해야 한다.

## 기억할 원칙

- 재컴파일 도구와 호스팅 서비스는 다른 대상이다. 저장소가 합법적이어도 서비스가 그렇다는 뜻은 아니다.
- 본인 사본으로 로컬에서 돌리는 쪽이 오래 간다. 호스팅 사이트는 언제든 내려갈 수 있다.
- 브라우저 게임의 성능은 WebGPU 지원 여부에 달려 있으므로, 시험은 자기 기기에서 한다.

---

[^repo]: GitHub, [th0mk/nfsu2-web](https://github.com/th0mk/nfsu2-web), 2026-11-08

[^popcar2]: <https://news.ycombinator.com/item?id=50404555>

[^herodoturtle]: <https://news.ycombinator.com/item?id=50405109>

[^judge2020]: <https://news.ycombinator.com/item?id=50406263>

[^mayeulc]: <https://news.ycombinator.com/item?id=50403473>

[^rustyhancock]: <https://news.ycombinator.com/item?id=50404031>

[^rvz]: <https://news.ycombinator.com/item?id=50404991>

[^jareklupinski]: <https://news.ycombinator.com/item?id=50403926>

[^andriy]: <https://news.ycombinator.com/item?id=50405286>

[^hypfer]: <https://news.ycombinator.com/item?id=50405820>

[^hobofan]: <https://news.ycombinator.com/item?id=50403659>

[^polytely]: <https://news.ycombinator.com/item?id=50403911>

[^nonethewiser]: <https://news.ycombinator.com/item?id=50404744>

[^diimdeep]: <https://news.ycombinator.com/item?id=50404961>

[^senfiaj]: <https://news.ycombinator.com/item?id=50403802>

[^kmno4]: <https://news.ycombinator.com/item?id=50403887>

[^lbreakjai]: <https://news.ycombinator.com/item?id=50404511>

[^wg0]: <https://news.ycombinator.com/item?id=50404695>

[^epolanski]: <https://news.ycombinator.com/item?id=50405375>

[^andix]: <https://news.ycombinator.com/item?id=50404050>
