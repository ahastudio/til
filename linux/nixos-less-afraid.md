# NixOS가 줄인 것은 설치의 어려움이 아니라 새 소프트웨어를 시험하는 일의 부담이다

원문: [NixOS is making me less afraid](https://entropicthoughts.com/nixos-is-making-me-less-afraid)

HN 토론: <https://news.ycombinator.com/item?id=50165484> (181점, 121개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/7d1swo/nixos_is_making_me_less_afraid> (51점, 34개 댓글)

GN 토론: <https://news.hada.io/topic?id=35731>

## 목차

- [요약](#요약)
- [분석](#분석)
  - [글이 줄였다고 주장하는 것은 시도의 비용이다](#글이-줄였다고-주장하는-것은-시도의-비용이다)
  - [비교 대상은 세 층으로 나뉘고 저자는 각각 다른 이유로 물리친다](#비교-대상은-세-층으로-나뉘고-저자는-각각-다른-이유로-물리친다)
  - [9줄이 가능한 이유는 모듈이 그 일을 이미 해 두었기 때문이다](#9줄이-가능한-이유는-모듈이-그-일을-이미-해-두었기-때문이다)
- [비평](#비평)
  - [백업이 9줄에 들어 있다는 말은 어디에서도 확인되지 않는다](#백업이-9줄에-들어-있다는-말은-어디에서도-확인되지-않는다)
  - [컨테이너 비교는 가장 약한 형태의 컨테이너 사용을 상대로 한다](#컨테이너-비교는-가장-약한-형태의-컨테이너-사용을-상대로-한다)
  - [서비스 하나의 사례를 일반 결론으로 넓힌다](#서비스-하나의-사례를-일반-결론으로-넓힌다)
  - [글에 없는 두 번째 이야기: 학습 비용이 LLM으로 옮겨 갔다](#글에-없는-두-번째-이야기-학습-비용이-llm으로-옮겨-갔다)
- [인사이트](#인사이트)
  - [시도의 비용이 내려가면 시도하는 서비스가 늘고 정리할 서비스도 늘어난다](#시도의-비용이-내려가면-시도하는-서비스가-늘고-정리할-서비스도-늘어난다)
  - [설정 파일이 실행되는 메모라는 말은 문서화를 대체하는 것이 아니라 문서화를 강제하는 것이다](#설정-파일이-실행되는-메모라는-말은-문서화를-대체하는-것이-아니라-문서화를-강제하는-것이다)
  - [롤백은 상태가 없는 부분에서만 공짜다](#롤백은-상태가-없는-부분에서만-공짜다)
  - [가장 큰 이견은 도구가 아니라 생태계 선택에서 갈린다](#가장-큰-이견은-도구가-아니라-생태계-선택에서-갈린다)

## 요약

kqr은 2026년 10월 20일 이 글을 블로그에 올렸다.
몇 년째 RSS 피드를 휴대전화 앱에만 두고 있었는데,
수천 개 글의 읽음 표시를 앱 하나에 맡기는 일이 불안했다고 한다.
휴대전화를 바꿀 때 피드는 옮겼지만 읽음 표시는 사라졌다는 사례도 든다.
서버에서 피드를 모아 주는 프로그램을 쓰고 싶었지만,
관리할 부업 프로젝트가 하나 더 느는 것이 싫어 미뤄 왔다.

그러다 FreshRSS를 읽고 서버에 설치해 쓰기 시작했는데,
1년 전이었다면 일어나지 않았을 일이라고 적는다.
그동안 NixOS 서버를 운영하게 되었기 때문이다.
FreshRSS와 백업을 설정하는 데 Nix 코드 9줄이 들었고,
nginx 역방향 프록시에 12줄 정도가 더 들었다.
설치는 몇 달째 손볼 일 없이 돌고 있으며,
서버가 고장 나면 같은 설정으로 새 서버를 15분쯤에 띄울 수 있다고 본다.

저자는 NixOS 밖의 설치 절차를 일곱 단계로 늘어놓는다.
압축 파일을 내려받아 풀고, 권한을 맞추고,
nginx와 php-fpm을 깔고, php-fpm 풀과 nginx 연동을 설정하고,
Let's Encrypt 인증서와 백업을 설정하고,
문제가 생겼을 때 이 모든 것을 기억해 내야 한다는 것이다.
공식 컨테이너 이미지를 써도 백업, systemd 서비스, TLS 종단 프록시는 남고,
어떤 이미지를 받았는지 적어 두지 않으면
6개월 뒤 같은 결과를 보장할 수 없다고 한다.

글의 뒷부분은 저자의 성향 이야기다.
저자는 남이 만든 자체 호스팅 서비스를 포함해 부업 프로젝트 유지보수를 싫어하고,
몇 분짜리 점검은 괜찮지만 몇 시간을 비워야 하는 업그레이드나 긴급 대응은
컴퓨터로 일하고 싶은 의욕을 꺾는다고 쓴다.
CFEngine, Ansible, podman, k3s를 진지하게 써 봤지만
꼼꼼히 적은 메모, 그리고 그 메모를 ssh 명령 순서로 옮긴 셸 스크립트보다
크게 나아지지 않았다고 한다.
NixOS 설정은 자신에게 남긴 지침처럼 읽히면서도 실행하면
매번 같은 결과를 낸다는 점이 달랐다는 것이 결론이다.

## 분석

### 글이 줄였다고 주장하는 것은 시도의 비용이다

제목의 두려움은 NixOS가 어렵다는 두려움이 아니다.
새 소프트웨어를 깔았다가 유지보수 부담을 떠안을까 하는 두려움이다.
저자는 서버 쪽 피드 수집기를 오래전부터 원했지만
서버를 지키는 일이 늘어난다는 이유로 가만히 있었다.
그 망설임이 사라진 계기로 드는 것은 기능이 아니라 재구축 시간이다.
서버가 죽어도 15분이면 같은 서버를 다시 만들 수 있다면,
시험해 보고 싫으면 지우는 일의 비용이 한정되기 때문이다.

이 주장에는 암묵적인 비용 계산이 깔려 있다.
어떤 서비스를 들일 때 드는 비용은 설치 비용 하나가 아니다.
설치 비용, 평소 유지 비용, 망가졌을 때 되살리는 비용,
그리고 지울 때 드는 비용이 합쳐진다.
글이 NixOS의 장점으로 내세우는 것은 이 가운데 세 번째이고,
유지 비용은 “몇 달째 손볼 일이 없었다”는 한 문장이 전부다.
네 번째인 제거 비용은 다루지 않는다.

### 비교 대상은 세 층으로 나뉘고 저자는 각각 다른 이유로 물리친다

수동 설치는 기억에 의존해서 졌고,
컨테이너는 TLS와 백업과 버전 고정이 남아서 졌고,
설정 관리 도구는 메모와 셸 스크립트보다 나을 것이 없어서 졌다.
세 탈락 사유가 서로 다르다는 점이 눈에 띈다.
첫째는 재현 가능성의 부재,
둘째는 범위의 부족,
셋째는 투자 대비 이득의 부재다.
NixOS가 이 셋을 한꺼번에 풀었다는 서술이 글의 설득력을 만든다.

그러나 이 비교는 저자의 경험 범위 안에서 이루어진다.
저자가 CFEngine, Ansible, podman, k3s에서 개선을 느끼지 못했다는 말은,
각 도구가 나쁘다는 증거가 아니라 저자의 쓰임새에서 효과가 없었다는 기록이다.
글에 나오는 구체적인 사례는 개인 서버에 서비스 하나를 올린 일이고,
그 조건이 결과를 정한다.

### 9줄이 가능한 이유는 모듈이 그 일을 이미 해 두었기 때문이다

저자의 9줄은 nixpkgs에 들어 있는 FreshRSS 모듈이 있어서 나온 숫자다.
이 모듈은 nixpkgs 저장소의 소스에서 옵션을 직접 확인할 수 있다.
`services.freshrss.enable`을 켜면
php-fpm 풀과 nginx 또는 caddy 가상 호스트를 만들고,
기본 데이터 위치는 `/var/lib/freshrss`, 기본 데이터베이스는 SQLite,
기본 웹 서버는 nginx이며,
서비스에는 `NoNewPrivileges`,
`PrivateTmp` 같은 systemd 격리 설정이 걸린다.[^freshrss-module]
수동 설치 목록에서 php-fpm 설정, 웹 서버 연동,
권한 맞추기가 모듈 안에 들어가 있다는 뜻이다.

즉 줄어든 것은 작업이 아니라 작업을 한 사람의 위치다.
FreshRSS 모듈 유지보수자가 한 번 푼 문제를 저자가 설정 한 덩어리로 받아 쓴다.
저자의 글에서는 이 점이 거의 보이지 않는다.
“9줄”이라는 숫자가 저자의 노력이 아니라 모듈이
쌓아 둔 노동의 크기를 말해 준다는 사실이 가려진다.

## 비평

### 백업이 9줄에 들어 있다는 말은 어디에서도 확인되지 않는다

글은 백업을 포함해 9줄이라고 적는다.
그런데 FreshRSS 모듈 소스에는 백업을 설정하는
옵션이 보이지 않는다.[^freshrss-module]
백업은 모듈 밖의 설정이다.
HN에서 cobertos는 글에 백업 설명이 없다고 지적했다.[^cobertos]
awithrow는 flake에 백업 옵션이 없으니
저자도 데이터 디렉터리를 다른 곳으로 동기화하고
있을 것이라고 짐작했다.[^awithrow]
drdexebtjl은 `services.restic.backups.<이름>.paths`에
FreshRSS 데이터 위치를 넣으면 된다고 적었다.[^drdexebtjl]

이 답은 NixOS의 구조적 장점을 잘 보여 준다.
neobrain은 같은 옵션에 여러 파일에서 값을 넣으면 하나의 목록으로 합쳐지므로,
백업 설정이 서비스 설정 옆에 붙어 있게 된다고 설명했다.[^neobrain]
restic 모듈에는 `paths`, `repository`, `timerConfig`,
`passwordFile` 옵션이 있다.[^restic-module]
다만 이것은 저자가 실제로 쓴 설정이 아니라 독자가 채워 넣은 추정이다.
글의 핵심 수치인 9줄 가운데 백업이 몇 줄인지는 알 수 없다.

더 중요한 것은 백업이 무엇을 지키는가이다.
FreshRSS 공식 문서는 `./data/`가 필수 백업 대상이고,
SQLite를 쓰면 그것으로 충분하다고 적는다.[^freshrss-backup]
NixOS 설정은 프로그램과 서비스 구성을 되살려 주지만
읽음 표시와 피드 목록은 되살려 주지 않는다.
저자가 이 글을 쓰게 만든 불안, 곧 읽음 표시가 사라지는 것은
설정 파일이 아니라 데이터 백업이 막는다.
Lobste.rs의 ginkogruen은 드라이브를 지워도 시스템은 금방 되돌아오지만
상태 있는 데이터는 따로 백업해야 한다고 적었다.[^ginkogruen]

### 컨테이너 비교는 가장 약한 형태의 컨테이너 사용을 상대로 한다

저자는 이미지 정보를 적어 두지 않으면 6개월 뒤 같은 결과가 나오지 않는다고 쓴다.
HN에서 RadiozRadioz는 이미지에는 태그와 해시가 있으므로
정확한 이미지를 적어 두면 같은 것을 받는다고 반박했다.
그리고 자신은 모든 이미지에 버전 태그를 명시한다고 했다.[^radiozradioz]
wrxd는 태그는 바뀔 수 있으니 해시를 쓰는지 되물었고,
RadiozRadioz는 큰 프로젝트의 릴리스 관행을 믿는다고 답하면서
해시를 쓰는 것도 가능하다고 덧붙였다.[^wrxd][^radiozradioz-tags]

FreshRSS 공식 Docker 문서의 빠른 실행 예시는
`freshrss/freshrss:edge` 태그를 쓴다.[^freshrss-docker]
저자가 비판한 상황이 문서의 기본 예시에서 나온다는 점은 인정할 만하다.
하지만 그 비판은 컨테이너가 재현성을 못 준다는 결론이 아니라,
태그를 고정하지 않는 사용 방식에 대한 비판일 뿐이다.
actinium226은 오히려 Nix에서도 nixpkgs를 갱신한 뒤 설치하면
Dockerfile의 `apt-get install`과 같은 가능성으로 새 버전이 들어오지 않느냐고
물었다.[^actinium226]
Cyph0n은 flake를 쓰고 잠금 파일을 갱신하지 않으면
머신 사이에서도 같은 패키지가 설치된다고 답했다.[^cyph0n]
즉 재현성은 NixOS 자체가 아니라 잠금 파일이라는 규율에서 나온다.
글은 이 규율 없이는 NixOS도 같은 문제를 겪는다는 점을 말하지 않는다.

### 서비스 하나의 사례를 일반 결론으로 넓힌다

HN의 poulpy123은 NixOS 9줄 또는 20줄,
다른 OS의 7단계, 도커의 복사해 붙이기를 비교하면
그리 설득력이 없다고 적었다.[^poulpy123]
bigyabai는 머신이 3대에서 10대 이상이면 사정이 다르다고 답했다.
단계 7개에 머신 5대를 곱하는 것과 설정 한 군데를 고치는 것의 차이다.[^bigyabai]
rgoulter는 Terraform과 비슷한 거래라고 설명했다.
처음에 비용이 더 들지만 선언형 코드의 이점으로 유지보수가 쉬워지고,
개인 워크스테이션에서는
반드시 실용적인 거래는 아니라는 것이다.[^rgoulter-terraform]

저자는 이 구분을 하지 않는다.
글은 서버 한 대를 두고 시작하지만
결론은 “새 소프트웨어를 시험하지 않을 이유가 없다”로 넓어진다.
서버가 한 대이고
서비스가 몇 개일 때 이득이 얼마나 되는지는 이 글만으로는 알 수 없다.
Lobste.rs의 jgb는 NixOS를 직장에서 개발 환경과 서버 배포에 쓰며,
Ansible에서 deploy-rs로 옮기는 것이 20년 앞으로 가는 느낌이라고 적었다.[^jgb]
그러나 같은 사람이 집 노트북에는 쓰지 않는다고 했다.
이득은 서버 쪽에서 크고 데스크톱 쪽에서는 사람마다 갈린다.

### 글에 없는 두 번째 이야기: 학습 비용이 LLM으로 옮겨 갔다

글은 Nix의 학습 곡선을 한 줄도 다루지 않는다.
그러나 두 토론에서는 학습 곡선 이야기가 두드러졌고,
그 답으로 LLM을 쓴다는 증언이 여럿 나왔다.
HN의 s08148692는 Claude Code에 원하는 운영체제를 설명하면
된다고 적었고,[^s08148692]
Aurornis는 LLM으로 모든 것을 돌린다면
Nix 같은 계층이 왜 필요한지 되물었다.[^aurornis]
ViewTrick1002는 LLM이 정리된 구조의 정보를 검색하고
고칠 때 성능이 좋다고 답했고,[^viewtrick1002]
1una는 LLM이 망쳤을 때 되돌리기가 NixOS에서는 쉽다고 했다.[^1una]

이 대화는 글의 주장과 맞닿아 있다.
저자가 말한 “덜 무섭다”는 감정은 되돌릴 수 있다는 확신에서 나오는데,
LLM이 설정을 쓰는 환경에서는 그 확신이 사람이 쓴 설정보다 더 절실해진다.
다만 이것은 토론에서 나온 해석이고, 저자가 LLM을 썼는지는 글에 나오지 않는다.

## 인사이트

### 시도의 비용이 내려가면 시도하는 서비스가 늘고 정리할 서비스도 늘어난다

글이 말하는 부담은 설치와 재구축이다.
그런데 Lobste.rs의 viccuad는 NixOS 패키지로 서비스를 올렸다가
마음에 안 들어 지웠더니
systemd 유닛 같은 것이 남아 있던 경우가 여러 번 있었다고 적었다.[^viccuad]
altano는 `networking.firewall.extraCommands`
규칙이 설정을 바꿔도 정리되지 않는다는 사례를 들고,
남은 방화벽 규칙은 정말 곤란하다고 했다.
Nix가 부작용을 거의 없애 주지만 완전히는 아니므로
확인이 필요하다는 것이다.[^altano]
nitinpassa는 상태 화이트리스트(impermanence)가 도움이 되지만
재부팅이 필요하다고 보탰다.[^nitinpassa]

이 사례들은 선언형 시스템이 “지우기”를
공짜로 만들어 주지 않는다는 것을 보여 준다.
설정에서 한 줄을 빼는 것과 실행 중인 시스템에서
그 흔적이 사라지는 것은 다른 일이다.
그리고 시도가 쉬워진 만큼 시도하는 서비스가 많아지면,
정리해야 할 서비스도 같은 비율로 늘어난다.
저자가 싫어하는 “유지보수할 부업 프로젝트”는 그 수가 줄어드는 것이 아니라
하나당 비용이 낮아진 채로 개수가 늘 가능성이 크다.
그 합이 저자가 견딜 수 있는 수준에 머무는지는
글이 쓰인 몇 달 사이에는 아직 드러나지 않았다.

### 설정 파일이 실행되는 메모라는 말은 문서화를 대체하는 것이 아니라 문서화를 강제하는 것이다

저자는 NixOS 설정이 꼼꼼히 쓴 지침처럼 읽히면서 실행도 된다고 했다.
이것은 사실 오래된 문제의 한 풀이다.
셸 스크립트가 “시간이 지나면 가정이 틀려진다”는 약점을 가진다는 저자의 말은,
스크립트가 암묵적인 환경에 기대고 있다는 뜻이다.
Nix는 그 환경을 입력으로 명시하게 강제한다.

그러나 이 강제가 만들어 내는 것은 설명이 아니라 사실의 기록이다.
HN의 WillAdams는 문서화로 충분히 설명해 두면
AI 없이도 다시 만들 수 있다고 말하며,
literate programming의 방식으로 생성된 문서를 소스 코드와 엮어 다시 쓰고
있다고 했다.[^willadams]
andrewla는 Nix를 이해하지 않아도 Claude가 대신 풀어 주니,
이해하지 않아도 되는 것이 좋지 않은 흐름이라고 느낀다고 적었다.[^andrewla]
설정이 실행되는 메모가 되는 순간,
메모를 쓴 사람이 그 내용을 이해했는지는 확인할 수 없게 된다.
코드가 있는 것과 이해가 있는 것은 별개이고,
이해가 없는 설정은 서버가 고장 났을 때 15분이 아니라 하루를 쓰게 만들 수 있다.

### 롤백은 상태가 없는 부분에서만 공짜다

Lobste.rs의 msangi는 `git revert`와 재빌드, 또는 부팅 메뉴의 이전 세대 선택으로
이전 시스템으로 돌아갈 수 있다는 확신이 새로운 시도를 쉽게 만든다고
적었다.[^msangi]
NixOS 공식 문서는
`nixos-rebuild switch --rollback`으로 직전
구성으로 돌아가는 방법을 설명한다.[^nixos-manual]
HN의 aussieguy1234도 3년 동안 여러 번 기계를 망가뜨렸지만
이전 세대로 부팅해 작업을 이어 갔다고 했다.[^aussieguy1234]

이 롤백은 시스템 구성을 되돌린다.
FreshRSS의 읽음 표시는 구성이 아니라 `/var/lib/freshrss` 안의 데이터다.
설정을 되돌려도 데이터는 되돌아오지 않는다.
프로그램 업그레이드가 데이터 형식을 바꿨다면
설정만 되돌려서는 풀리지 않는 문제가 생길 수 있다.
저자가 처음 걱정한 읽음 표시 유실이 바로 이 계층에서 일어나는데,
글은 그 계층을 설정 한 줄로 해결된 것처럼 지나간다.
“덜 무섭다”는 감정은 시스템 계층에서는
정당하고 데이터 계층에서는 아직 근거가 없다.

### 가장 큰 이견은 도구가 아니라 생태계 선택에서 갈린다

HN과 Lobste.rs의 반응에서 NixOS를 쓰는 사람들도 서로 다른 지점에서 갈렸다.
Lobste.rs의 toastal은 Claude Code가 만든 flake가 안정 버전과
오버레이 중심의 코드를 막는다고 비판했고,[^toastal-flakes]
phaer는 flake가 결정을 한 묶음으로 내려 주어 사람이나
LLM이 따라갈 결정 트리를 줄여 준다고 답했다.[^phaer]
HN의 Nerdrotic은 unstable 채널이나 flake를 쓰지 말고 stable을 쓰라고 권하면서,
업데이트 뒤 노트북이 부팅하지 않아 2~3일
동안 고쳐지지 않은 경험을 적었다.[^nerdrotic]
georgyo는 flake가 공식적으로는 실험적이지만
사실상 모두가 쓰는 기능이라고 설명했다.[^georgyo]

저자가 말한 “같은 결과”를 얻으려면 어느 길로 가야 하는지가 이 논쟁 안에 있다.
stable 채널에 고정하면 안정적이지만 최신 소프트웨어가 늦고,
flake를 쓰면 잠금 파일로 재현성을 얻지만 실험적 기능 위에 서게 된다.
어느 쪽도 “9줄”이라는 숫자에 포함되지 않는다.
처음 NixOS를 들이는 사람이 이 선택지를 모른 채 따라 하면
저자와 같은 경험을 얻는다고 장담하기 어렵다.

여기에 공급망 문제도 있다.
lrvick은 nixpkgs가 리뷰 없이도 코드를 넣을 수 있는 큰 공동체에 기대고 있으므로
높은 공급망 보안이 필요한 운영 환경에는 맞지 않는다고 주장했다.[^lrvick]
rgoulter는 이 표현이 느슨하고 부정확하며,
nixpkgs를 따로 검수해 쓸 수 있고
기여는 보통 리뷰를 거친다고 반박했다.[^rgoulter-nixpkgs]
이 쟁점은 저자의 쓰임새인 개인 RSS 서버에서는 문제가 되지 않지만,
같은 논리를 업무용으로 옮길 때는 별도로 따져야 한다.

---

[^freshrss-module]: GitHub, [nixos/modules/services/web-apps/freshrss.nix](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/services/web-apps/freshrss.nix)

[^restic-module]: GitHub, [nixos/modules/services/backup/restic.nix](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/services/backup/restic.nix)

[^freshrss-backup]: FreshRSS, [Backup](https://freshrss.github.io/FreshRSS/en/admins/05_Backup.html)

[^freshrss-docker]: GitHub, [Deploy FreshRSS with Docker](https://github.com/FreshRSS/FreshRSS/blob/edge/Docker/README.md)

[^nixos-manual]: NixOS, [NixOS Manual](https://nixos.org/manual/nixos/stable/)

[^cobertos]: <https://news.ycombinator.com/item?id=50166694>

[^awithrow]: <https://news.ycombinator.com/item?id=50168047>

[^drdexebtjl]: <https://news.ycombinator.com/item?id=50167058>

[^neobrain]: <https://news.ycombinator.com/item?id=50167573>

[^radiozradioz]: <https://news.ycombinator.com/item?id=50170240>

[^wrxd]: <https://news.ycombinator.com/item?id=50171613>

[^radiozradioz-tags]: <https://news.ycombinator.com/item?id=50172945>

[^actinium226]: <https://news.ycombinator.com/item?id=50166940>

[^cyph0n]: <https://news.ycombinator.com/item?id=50173070>

[^poulpy123]: <https://news.ycombinator.com/item?id=50166996>

[^bigyabai]: <https://news.ycombinator.com/item?id=50171051>

[^rgoulter-terraform]: <https://news.ycombinator.com/item?id=50174892>

[^rgoulter-nixpkgs]: <https://news.ycombinator.com/item?id=50174876>

[^s08148692]: <https://news.ycombinator.com/item?id=50166378>

[^aurornis]: <https://news.ycombinator.com/item?id=50167594>

[^viewtrick1002]: <https://news.ycombinator.com/item?id=50167692>

[^1una]: <https://news.ycombinator.com/item?id=50167695>

[^willadams]: <https://news.ycombinator.com/item?id=50171100>

[^andrewla]: <https://news.ycombinator.com/item?id=50167202>

[^aussieguy1234]: <https://news.ycombinator.com/item?id=50174681>

[^nerdrotic]: <https://news.ycombinator.com/item?id=50168250>

[^georgyo]: <https://news.ycombinator.com/item?id=50167767>

[^lrvick]: <https://news.ycombinator.com/item?id=50174077>

[^jgb]: <https://lobste.rs/s/7d1swo/nixos_is_making_me_less_afraid#c_ojiqkt>

[^ginkogruen]: <https://lobste.rs/s/7d1swo/nixos_is_making_me_less_afraid#c_ubqsbd>

[^viccuad]: <https://lobste.rs/s/7d1swo/nixos_is_making_me_less_afraid#c_3fjs4q>

[^altano]: <https://lobste.rs/s/7d1swo/nixos_is_making_me_less_afraid#c_rkzvsq>

[^nitinpassa]: <https://lobste.rs/s/7d1swo/nixos_is_making_me_less_afraid#c_8p38wu>

[^msangi]: <https://lobste.rs/s/7d1swo/nixos_is_making_me_less_afraid#c_qjsxrd>

[^toastal-flakes]: <https://lobste.rs/s/7d1swo/nixos_is_making_me_less_afraid#c_vhwjg7>

[^phaer]: <https://lobste.rs/s/7d1swo/nixos_is_making_me_less_afraid#c_6ohx2v>
