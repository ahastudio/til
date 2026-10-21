# 네덜란드가 자체 Linux OS를 만든다는 보도는 NixOS 설정 묶음을 새 배포판으로 부풀렸다

원문: [The Netherlands is building its own Linux OS to break free from Microsoft | TechSpot](https://www.techspot.com/news/114018-netherlands-building-own-linux-os-break-free-microsoft.html)

HN 토론: <https://news.ycombinator.com/item?id=50166088> (3점, 0개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/nne5uh/netherlands_is_building_its_own_linux_os> (67점, 19개 댓글)

GN 토론: <https://news.hada.io/topic?id=35718>

## 요약

TechSpot의 Alfonso Maruccia는 2026년 9월 29일 기사에서
네덜란드 정부가 디지털 주권 문제를 풀려고
자체 Linux 운영체제를 만들고 있다고 전했다.
현지 매체가 NixOS에 쏟는 개발 노력을 소개했고,
미국산 소프트웨어,
그중에서도 Microsoft 제품을 이 운영체제와
오픈소스 생산성 도구로 바꾸려 한다는 내용이다.

기사는 Nix가 네덜란드 개발자들이 만든 패키지 관리자이고
NixOS는 이를 바탕으로 한 배포판이며
네덜란드 비영리 단체 NixOS Foundation이 지원한다고 소개한다.
이 둘이 DAWO(Digitaal Autonome Werkomgeving Overheid) 프로젝트의 토대이고,
DAWO는 정부와 공공기관에 맞춤 운영체제와 사무 응용,
클라우드 서비스, 관리 도구를 제공한다는 계획이다.
몇 달 전 네덜란드 당국이 국가 IT 생태계를 표준화하기로 하면서
본격적인 작업이 시작됐고,
첫 시범 사업은 민간과 지역 환경에 이미 배치됐다고 한다.
기사는 이 프로젝트가 접근성에 초점을 맞춘다고 쓰면서
NixOS 개발자들이 GUI 중심의 인터페이스를 열광적으로 지지하지는 않기 때문이라고
덧붙인다.

배경으로는 미국이 헤이그의 국제형사재판소(ICC)에 제재를 가했고
Microsoft가 재판소 검사들의 이메일과 핵심
IT 서비스 접근을 막았다는 주장이 나온다.
ICC는 이미 Microsoft Office를 오픈소스 대안으로 바꾸는 중이라고 한다.
기사는 올해 초 네덜란드가 미국 기업의 핵심 앱 인수를 막은 일과
다른 유럽 국가들의 비슷한 전환 사업도 곁들인다.

## 분석

### 기사는 하나의 출처를 한 단계 옮긴 것이다

기사가 단 출처 링크는 네덜란드 IT 매체 Tweakers의 기사 하나다.
heise도 같은 사안을 다루면서
Tweakers를 인용한 The Register를 거쳐 전한다고 밝혔다.[^heise]
그러니 이 보도는 Tweakers에서 시작해 한두 단계를 거친 이야기다.
이 문서는 Tweakers 기사를 읽지 못했다. 동의 창 뒤에 있어서 열지 않았다.
따라서 TechSpot이 원 보도를 어디까지 충실히 옮겼는지는 직접 대조하지 못했고,
대신 공식 저장소와 heise로 사실관계를 확인했다.

### DAWO는 새 배포판이 아니라 NixOS 위에 올린 구성이다

공식 안내에 따르면 DAWO는 내무부 산하의 구상이고,
상호운용이 가능하고 디지털로 자율적인 공공 업무 환경의 토대를 목표로 한다.
운영체제 부분은 NixOS의 자체 구현인 DAWO-NixOS이며,
이와 별도로 대비책으로 Fedora Kinoite 기반 개발 경로도 두고 있다.
관리 구성 요소는 DAWO-Sextant라는 단말 묶음 관리자이고,
AI와 클라우드와 신원 및 접근 관리, 협업 소프트웨어가 별개 구성 요소로 나뉜다.
협업 소프트웨어는 Mijn Bureau를 주로 쓰고
openDesk와 La Suite의 진행을 지켜본다.[^dawo]

heise는 Mijn Bureau가 파일에 Nextcloud, 사무에 Collabora, 소통에 Element,
프로젝트 관리에 OpenProject 등을 쓰는 자체 호스팅 업무 스위트라고 설명한다.
같은 기사는 DAWO가 하나의 제품이 아니라 정부 업무 환경 전체의 청사진이고
구성 요소를 갈아 끼울 수 있다고 전한다.[^heise]
DAWO-Core 저장소의 구조 문서는
이 저장소가 완성된 이미지가 아니라 블록의 라이브러리라고 적는다.
각 기능이 `flake.modules.nixos.<이름>` 형태의 블록이고,
이를 조합하는 쪽이 소비자다.[^arch]
즉 기사의 자체 Linux 배포판이라는 표현은 사실과 거리가 있다.
NixOS를 바탕으로 한 공공 단말 설정 묶음과 그 위의 업무 스택이 실체다.
이는 이 문서의 읽기이며,
공식 문서는 새 배포판이라는 말도 아니라는 말도 하지 않는다.

### 일정은 기사보다 구체적이다

heise에 따르면 2026년 7월 부처 간 위원회(ICBR)가
국가 IT 서비스 기관 세 곳, SSC-ICT와 DICTU와 DUO-ICT에
표준화되고 더 주권적인 디지털 업무 환경의 개발을 맡겼다.
지방자치단체 협회(VNG)를 통해 지자체 여덟 곳이 이미 시범 운영에 참여하고 있다.
프로젝트는 처음에 클라이언트 운영체제로 openSUSE와 Fedora를 시험하다가
NixOS를 택했다.
코드는 내무부의 Forgejo 인스턴스와 Codeberg로 공개한다.[^heise]
기사가 말한 민간과 지역 환경의 시범 사업보다 이쪽 서술이 더 구체적이다.

## 비평

### 접근성이라는 설명은 확인되지 않는다

기사는 이 프로젝트가 접근성에 초점을 맞추고 그 이유가
NixOS 개발자들이 GUI 중심 인터페이스에 열광하지 않기 때문이라고 쓴다.
이 문서가 읽은 공식 안내와 heise에는 그런 서술이 없다.
오히려 DAWO-NixOS 저장소의 모듈 목록에는 GUI 환경과
작업 공간 설정을 맡은 `desktops` 모듈이 있고,
강화 단계에는 GNOME을 잠그는 선택 블록이 있다.[^nixrepo][^arch]
접근성이 목표라는 말이 장애인 접근성을 뜻하는지 사용
접근 용이성을 뜻하는지도 기사에서 분명하지 않다.
Tweakers 원문에 근거가 있을 수 있지만,
이 문서가 확인한 범위에서는 뒷받침되지 않는다.

### ICC 사건의 서술에서 Microsoft의 반박이 빠졌다

기사는 Microsoft가 재판소 검사들의 이메일과 핵심 IT 서비스 접근을 막았다고
주장한다고 쓴다.
heise가 DAWO 기사에서 전한 사실은 더 좁다.
Microsoft가 당시 수석검사 Karim Khan의 이메일 계정을 끊었다는 것이다.[^heise]
이 건에 대해 Microsoft의 Brad Smith 사장은 2025년 6월 기자들에게
회사가 재판소에 대한 서비스를 중단하거나 정지한 적이 없다고 했다.
heise는 AP가 앞서 제재 때문에 Microsoft가 Khan의 계정을 막았다고
보도했다고 같이 전한다.[^heise-ms]
따라서
지금까지 확인되는 것은 한 사람의 계정이 끊겼다는 보도와
서비스 중단은 없었다는 회사의 주장이 맞선다는 점이다.
기사는 allegedly로 단서를 달았으나 회사의 반박과 규모의 차이를 담지 않았다.

Lobste.rs의 DustyFuzzy는 기사가 가볍게 넘긴 이유를 하나 더 보탰다.
미국의 ICC 제재가 통신 서비스나 급여
소프트웨어와 달리 운영체제는 예외로 두지 않아서,
재판소가 원해도 새 Windows 라이선스를 얻을 수 없다는 것이다.[^DustyFuzzy]
이 문서는 이 설명을 확인하지 못했고,
제재 문서의 예외 범위를 직접 읽어야 판단할 수 있다.

### 주권을 내세우는 빌드가 GitHub에서 입력을 받는다

DAWO-Core의 `flake.nix`에는 주석이 달려 있다.
모든 입력이 오픈소스이지만 지금은 github.com에서 받아 오고,
목표는 이를 code.overheid.nl에 미러링해 다시
고정함으로써 해외 호스팅 의존을 없애는 것이라는 내용이다.
빌드에 실제로 쓰이는 입력 15개가 다음 미러링
순서를 기다린다고도 적혀 있다.[^core-flake]
GitHub은 Microsoft 소유다.
기사는 Microsoft를 벗어나려는 프로젝트라고 소개하지만 이 점은 다루지 않는다.
이 주석은 프로젝트 스스로 해결 과제로 적어 둔 것이어서
숨긴 약점이라기보다 로드맵의 일부다.
그러나 주권을 내세운 보도라면 지금 어디까지 왔는지를 밝히는 것이 맞다.

Lobste.rs에서도 같은 점이 지적됐다.
scientiac는 Nix가 Microsoft 소유의 GitHub에 크게 의존하므로
엄밀히는 Microsoft를 벗어나지 못한 것이라고 했고,[^scientiac]
radex는 Nix 계열 프로젝트의 인프라가 어느 정도 GitHub에 기대고
있으며 고칠 수 있는 문제라고 보탰다.[^radex]
sjamaan은 NixOS가 GitHub을 떠나는 일이 정부가 Windows를 떠나는 일보다 쉽다며
한 걸음씩 가면 된다고 답했다.[^sjamaan]

### 초기 단계라는 신호가 기사에는 없다

DAWO-Core의 변경 기록은 0.2.0 버전이며,
9월 3일 보안 점검의 첫 절반을 반영한 0.1.3이 바로 앞이다.[^changelog]
구조 문서는
감사 로그 기능이 상위 패키지의 결함 때문에 아직 동작하지 않아 보류 상태이고,
USB 제한 기능은 사용자가 고장으로 느낄까 봐 선택 항목으로 뒀다고 적는다.
이전에 주석이 더 많은 것을 약속했는데
실제 코드는 그렇지 않아 문서를 고쳤다는 설명도 붙어 있다.[^arch]
이런 서술은 프로젝트가 정직하게 현재 상태를 적는다는 장점이면서,
모든 기관을 아우르게 될 것이라는 기사의 어조보다 훨씬 이른 단계임을 보여 준다.

### 기사의 곁가지 사실도 느슨하다

기사는 올해 초 네덜란드가 시민이 모든 일에
쓰는 앱의 미국 기업 인수를 막았다고 쓴다.
Lobste.rs의 manfred는 이것이 세금 신고
서명과 여권 신청에 쓰는 인증 플랫폼 DigiD를 가리키는 것이라고 했고,[^manfred]
alexk는 DigiD는 정부가 개발하고 유지하며 매각 대상이 아니었고,
정부가 백엔드를 돌리는 서버 공간을 빌려 주는 민간 회사가 팔리는 것이었다고
정정했다.[^alexk]
alexk가 스스로 대체로 확신한다고 밝힌 정정이고
이 문서가 원 보도를 열어 확인하지는 못했다.
다만 제목과 같은 방식으로 핵심 대상을 한
단계 크게 묘사하는 경향이 기사 곳곳에 보인다.

## 인사이트

### 주권은 계층마다 의존하는 곳을 따로 세어야 한다

운영체제의 배포 단체가 네덜란드에 있다는 것은 한 계층의 사실이다.[^heise]
그 위에 빌드 입력을 어디서 받는지, 소스 저장소를 어디에 두는지,
협업 스택을 누가 만드는지, 클라우드를 어디서 돌리는지가 각각 다른 의존이다.
DAWO의 `flake.nix` 입력 목록은 문자 그대로 이 의존 그래프이고,
프로젝트는 그중 15개를 미러링 대상으로 따로 세어 두었다.[^core-flake]
코드를 Forgejo와 Codeberg에 공개하고
GitHub에 사본을 두는 배치도 같은 사정을 보여 준다.[^core]

여기서 기술적으로 중요한 것은 재현 가능성이다.
Nix가 입력을 고정하면 같은 결과를 다시 만들 수 있지만,
고정은 그 입력의 소스가 아직 받을 수 있는 곳에 있어야 의미가 있다.
공급처가 끊기면 고정된 해시는 받을 곳이 없는 주소가 된다.
자국 인프라에 미러링하는 것이 주권의 마지막 조각인 이유다.
이는 이 문서의 해석이다.

Lobste.rs의 akavel은 미러링이 생각보다 어렵다고 짚었다.
nixpkgs의 많은 패키지가 포장한 앱의 소스나 바이너리 압축 파일을 GitHub에서
받아 오므로,
nixpkgs를 미러링해도 그 압축 파일까지 모으려면
한동안 GitHub에 접근해야 하고 작업이 방대하다는 것이다.[^akavel]
이 지적이 맞다면 앞의 입력 15개 미러링은 시작일 뿐이고,
주권의 마지막 조각은 입력 목록이 아니라
그 아래의 소스 공급 경로까지 닿아야 한다.
이 문서는 이 주장의 정확성을 확인하지 않았다.

### 논쟁의 사실 여부와 관계없이 단일 공급자 의존이 약점이다

ICC 사건에서 누가 계정을 끊었는지는 지금도 다툼이 있다.[^heise-ms]
그런데 DAWO를 추진하는 논리는 그 다툼의 결과에 기대지 않는다.
핵심 도구에 대한 접근이 정치적 결정에 달릴 수 있다는 점이 문제라고
heise가 정리한 것처럼,[^heise]
공급자가 의도했든 법적 판단이든 한 사람의 계정이
끊기는 상황이 가능하다는 사실 자체가 위험이다.
회사가 그런 일이 없었다고 말한다면
오히려 서비스를 받는 쪽이 무슨 일이 있었는지를 확인할 방법이 없다는 뜻이다.

이 위험은 ICC 같은 작은 기관의 몫으로 끝나지 않는다.
이 저장소의 `linux/france-linux-transition.md`가
다룬 프랑스 정부의 Windows 이탈 발표처럼
유럽 여러 곳이 같은 계산을 하고 있다.
이런 전환의 비용은 단말을 바꾸는 데 있지 않고
신원과 메일과 문서를 한 공급자에 묶어 둔 구조를 푸는 데 있다.
DAWO가 운영체제와 나란히 신원 및 접근 관리와 클라우드를
별도 구성 요소로 두는 것도 이 때문으로 읽힌다.[^dawo]

### 선언적이고 동일한 단말은 공공 조달에 잘 맞지만 설정이 곧 정책이 된다

NixOS의 선언적 구성과 재현 가능한 배포는 큰 단말 묶음을 관리하고
감사하기 쉽게 한다고 heise는 설명한다.[^heise]
같은 설정에서
같은 단말이 나온다는 성질은 수백 곳의 기관에
같은 보안 기준을 강제하는 데 쓸모가 있다.
DAWO-Core는 필수 보안 설정을 소비자가 약화시키지 못하도록 `mkForce`로 강제하고
권장 기본값은 `mkDefault`로 두는 규칙을 세웠다.[^arch]

이 방식의 긴장은 설정이 곧 정책이라는 점에서 온다.
필수 설정이 단말을 쓰는 사람에게 불편을 주면,
예컨대 USB를 거부하는 단말은 고장으로 읽힌다는 것이 구조 문서의 설명이다.[^arch]
각 기관이 자기 사정에 맞게 조정하려는 요구와 중앙이 강제하려는 기준이 부딪힐 때
누가 어디까지 바꿀 수 있는지가 이 프로젝트의 성패를 가를 수 있다.
저장소는 소비자가 약화시킬 수 없는 부분과 조정할
수 있는 부분을 코드로 구분하는 쪽을 택했다.

### 자체 배포판을 새로 만드는 대신 기존 배포판의 구성을 택한 점이 과거 시도와 다르다

Lobste.rs의 lthms는 프랑스가 과거에 Gentoo에 보안 패치를 얹고
LSM을 더한 Clip OS를 만들었다고 했고,[^lthms]
threkk는 스페인이 지역별 Linux 버전을 여러 개 만든 적이 있다며
이번에는 더 잘되기를 바랐다.[^threkk]
두 사례 모두 이 문서가 확인한 것이 아니라 댓글이 든 기억이다.

이 비교가 맞다면 DAWO가 택한 길은 다르다.
배포판을 새로 갈라 유지하는 대신 NixOS 위에 선언적 설정을 쌓고,
그 설정의 필수 부분을 코드로 강제한다.[^arch]
유지해야 하는 것이 배포판 전체가 아니라 설정 묶음이어서 부담이 훨씬 작다.
대신 위쪽 NixOS의 방향과 일정에 정부가 끌려갈 수 있다.
내무부가 대비책으로 Fedora Kinoite 기반 경로를
따로 둔 것은 이 위험을 아는 선택으로 읽힌다.[^dawo]

---

[^heise]: heise online, [Netherlands builds sovereign government desktop based on NixOS](https://www.heise.de/en/news/Netherlands-builds-sovereign-government-desktop-based-on-NixOS-11470450.html), 2026-09-30

[^heise-ms]: heise online, [Microsoft denies mail blockade at the International Criminal Court](https://www.heise.de/en/news/Microsoft-denies-mail-blockade-at-the-International-Criminal-Court-10429628.html), 2025-06-05

[^dawo]: code.overheid.nl, [MinBZK/DAWO](https://code.overheid.nl/MinBZK/DAWO)

[^nixrepo]: code.overheid.nl, [MinBZK/DAWO-NixOS](https://code.overheid.nl/MinBZK/DAWO-NixOS)

[^core]: GitHub, [DAWO-community/DAWO-Core](https://github.com/DAWO-community/DAWO-Core)

[^arch]: GitHub, [DAWO-Core의 architecture.md](https://github.com/DAWO-community/DAWO-Core/blob/main/architecture.md)

[^changelog]: GitHub, [DAWO-Core의 CHANGELOG.md](https://github.com/DAWO-community/DAWO-Core/blob/main/CHANGELOG.md)

[^core-flake]: GitHub, [DAWO-Core의 flake.nix](https://github.com/DAWO-community/DAWO-Core/blob/main/flake.nix)

[^DustyFuzzy]: <https://lobste.rs/s/nne5uh/netherlands_is_building_its_own_linux_os#c_rqt7bp>

[^scientiac]: <https://lobste.rs/s/nne5uh/netherlands_is_building_its_own_linux_os#c_xuiec0>

[^radex]: <https://lobste.rs/s/nne5uh/netherlands_is_building_its_own_linux_os#c_ovep5w>

[^sjamaan]: <https://lobste.rs/s/nne5uh/netherlands_is_building_its_own_linux_os#c_s72vgb>

[^manfred]: <https://lobste.rs/s/nne5uh/netherlands_is_building_its_own_linux_os#c_0au1z0>

[^alexk]: <https://lobste.rs/s/nne5uh/netherlands_is_building_its_own_linux_os#c_pexaza>

[^akavel]: <https://lobste.rs/s/nne5uh/netherlands_is_building_its_own_linux_os#c_za89m2>

[^lthms]: <https://lobste.rs/s/nne5uh/netherlands_is_building_its_own_linux_os#c_cjjbjg>

[^threkk]: <https://lobste.rs/s/nne5uh/netherlands_is_building_its_own_linux_os#c_mx0noj>
