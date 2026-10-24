# 컨테이너 런타임을 직접 만들어 보니 Docker는 이상하다

원문: [Code and Cake - Docker is weird](https://codeandcake.dev/posts/2026-10-22-docker-is-weird)

HN 토론: <https://news.ycombinator.com/item?id=50202681> (824점, 347개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/xsz9sc/docker_is_weird> (95점, 43개 댓글)

GN 토론: <https://news.hada.io/topic?id=35852>

## 요약

Code and Cake 블로그에 2026년 10월 22일에 올라온 짧은 글이다.
저자는 재미로 자기 컨테이너 런타임을 만들고 있고, 아직 초기이지만 Docker가
이상하다는 점을 배웠다고 쓴다.
이상한 점은 다섯 가지다.

첫째, 컨테이너는 진짜가 아니다.
VM과 달리 컨테이너는 특별한 제한이 걸린 프로세스일 뿐이고 커널이 그 프로세스를
돌리며, 찾아보면 `/proc`에서 볼 수 있다.
둘째, 리눅스에 컨테이너라는 하나의 기능이 있는 것도 아니다.
네임스페이스(호스트와 컨테이너가 서로 보는 것을 가림), cgroup(자원 사용 제한),
네트워크 격리 기능을 포함해 다섯 가지 커널 기능이 트렌치코트 안에 들어 있다고
표현한다.
셋째, 이미지는 폴더다.
`docker run -it --rm ubuntu /bin/bash`는 Docker Hub에서 이미지를 받아 어딘가에
두고, 그 폴더를 `chroot`(또는 `pivot_root`)로 프로세스의 루트 디렉터리로 삼아 그
안의 `bash`를 실행한다는 설명이다.

넷째, Go는 컨테이너 런타임에 어울리지 않는 언어라고 한다.
Docker의 런타임 `runc`는 Go로 쓰였는데 Go 런타임은 기본적으로 멀티스레드이고,
컨테이너 런타임에 필요한 시스템 호출 상당수는 단일 스레드에서 해야 한다.
그래서 `runc`에는 Go 런타임이 초기화되기 전에 실행되는 C 모듈이 있고, Go에는
`fork`도 없어서(`fork`는 주 스레드만 복제한다) `/proc/self/exe`를 특별한 인자와
함께 다시 실행해 자식 프로세스인 척 흉내 낸다고 한다.
다섯째, Docker는 root가 필요하다.
macOS에서 쓰면 놓치기 쉽지만, 컨테이너 런타임이 쓰는 리눅스 커널 API 다수가
root를 요구하거나 요구했고, 요즘은 나아졌지만 rootless 런타임은 네트워킹 스택을
사용자 영역에서 다시 구현해야 하는 것으로 보인다는 서술이다.
글은 자기 버전의 도구를 직접 만들어 보는 것이 그 도구를 배우는 좋은 방법이라는
말로 끝난다.

## 분석

### 글의 중심 주장: 추상화 아래의 실체는 평범한 운영체제 기능이다

이 글의 논지는 컨테이너가 신비로운 기술이 아니라 프로세스와 커널 기능의
조합이라는 것이다.
VM이라는 멘탈 모델로 Docker를 쓰는 사람에게 이 설명은 흔한 오해를 바로잡는다.
HN에서 paxy가 많은 사람이 Docker를 블랙박스로 쓰고 VM의 멘탈 모델을 가지고
있다가 내부를 파 보면 이상함이 드러난다고 짚은 것이 같은 이야기다.[^paxy]
글의 나머지 항목(이미지는 폴더, 루트가 필요함)도 같은 도식의 확장이다.

### Go 비판은 언어 비판이 아니라 프로세스 모델의 충돌이다

넷째 항목이 글에서 가장 기술적이다.
컨테이너 설정은 단일 스레드 컨텍스트에서 해야 하는 네임스페이스 진입과 cgroup
배치, 그리고 `fork` 뒤 `exec`이라는 유닉스 고전 패턴에 기대는데, 고루틴이 OS
스레드를 옮겨 다니는 Go 런타임은 이를 직접 지원하지 않는다.
HN의 gzapp은 초기에 고루틴이 스레드를 옮겨 다니고 포크 시 상속되는 것이 스레드의
네임스페이스와 cgroup 설정이라 네트워크 네임스페이스가 가끔 제대로 정리되지
않았고, 특정 부하에서 재사용된 스레드의 네트워킹이 망가져 이미지를 받지 못하게
된 가장 까다로운 문제를 겪었다고 증언했다.[^gzapp]
LambdaComplex는 고루틴을 OS 스레드에 고정하는 Go 함수가 한동안 안전하게 믿을 수
없을 만큼 고장 나 있었다고 덧붙였다.[^lambdacomplex]

## 비평

### 이상함이라는 틀이 역사적 맥락을 지운다

j16sdiz는 글의 모든 문장이 무엇이 이상하냐는 물음을 낳고, 오랜 시간에 걸쳐
진화한 과정을 알면 자연스럽다고 했다.[^j16sdiz]
stingraycharles는 정작 이상한 결정인 클라이언트와 서버 모델이 권한 관리를 두
자릿수 단위로 복잡하게 만든다는 점은 글에 없다고 짚었다.[^stingraycharles]
글은 설계의 결과를 이상하다고 부르지만 그 결과가 왜 그렇게 되었는지(당시 커널
기능의 상태, 도입하려던 사용자)는 다루지 않는다.

### root가 필요하다는 서술은 현황과 기본값을 섞는다

0xbadcafebee는 Docker가 7년 전부터 root를 요구하지 않으며 기본값이 root 데몬인
것은 그 편이 쉽기 때문이라고 반박했다.[^0xbadcafebee]
fulafel은 rootless Docker 경험이 예전에는 나빠서 기본이 rootless인 Podman이
마찰이 적었는데 지금은 바뀌었는지 물었다.[^fulafel]
글도 요즘은 나아졌다고 쓰지만 핵심 문장은 Docker는 root가 필요하다는 단정이라
독자가 현황을 오해하기 쉽다.

### Go 판단은 작은 근거로 큰 결론을 낸다

miladyincontrol은 Go가 그렇게 나쁜 언어라면 crun이나 youki가 의미 있게 빠르지도
않다고 반박했다.[^miladyincontrol]
0x457은 쟁점은 속도가 아니라 Go로 컨테이너 런타임을 개발하는 것이 어렵다는
점이라고 답했고,[^0x457] gertop은 수백 개 컨테이너를 띄우면 Docker 오버헤드가
메모리에서 커진다고 했다.[^gertop]
jlhawn(2014~2019년 Docker 근무)은 가장 중요한 부분은 사실 C로 쓰였다고 적었다가
글의 다음 문단이 이를 다룬다는 것을 보고 정정했다.[^jlhawn]
rob74는 `runc` 저장소의 언어 비율이 Go 68.5%, 셸 27.1%, C 3.5%이므로 Go로
쓰였다고 해도 무방하다고 보았다.[^rob74]
글의 판단은 개발 경험(C 모듈과 `/proc/self/exe` 우회)에 근거하며 성능이나
안정성을 측정한 자료는 없다.

### Lobste.rs에서는 컨테이너라는 말의 정의가 쟁점이었다

david_chisnall은 컨테이너 셸 구현과 컨테이너를 뒤섞는 것이 싫다고 했다.
컨테이너는 프로세스가 사물이 아닌 것과 같은 방식으로 사물이 아니며, 여러 곳에서
여러 방식으로 구현되고 커널 상태, MMU 매핑, 권한 모드 같은 여러 요소로 조립되는
추상화라는 것이다.[^david_chisnall]
이 지적은 글의 컨테이너는 진짜가 아니다라는 소제목과 같은 사실을 다르게 말하며,
진짜가 아니라는 표현이 오히려 어떤 정의를 전제하는지 되묻게 한다.
samuelkarp은 글의 이미지는 폴더라는 설명을 보강해, OCI 이미지의 삭제
표시(whiteout)와 디스크에 풀어 놓는 방식 사이에 변환이 필요하고 기본 저장소인
overlay에서는 AUFS 계열의 표시가 overlay 표시로 바뀐다고 적었다.[^samuelkarp]
janus는 이런 기술적 세부를 줄 수 있는 답이라며, 글이 너무 기본적이어서 아쉽다고
했다.[^janus]
dutc는 Docker의 초기 성공이 이런 기능들이 더 나은 방향으로 발전하는 것을 막았을
가능성이 있고 Podman이 root 문제를 상당히 개선했다고 했다.[^dutc]
wink는 Docker 이전에도 이런 작업을 하는 사람들이 있었으므로 Docker의 영향을
과대평가하는 것이라고 반박했다.[^wink]
noirscape는 Docker가 이상한 이유는 해결하려는 문제 자체가 이상하기 때문이며,
가상 환경과 로컬 의존성 폴더로 충분한 프로젝트에는 처음부터 필요하지 않았다고
했다.[^noirscape]
drrobotic은 Docker의 네트워킹이 이상한 점으로 기본적으로 모든 컨테이너가
외부에서 접근 가능하다고 썼고 포트 매핑을 `127.0.0.1:5432:5432/tcp`처럼 로컬
호스트에 묶는 것을 권했으나,[^drrobotic] altano는 노출한 포트만 접근 가능한 것
아니냐며 의문을 제기했다.[^altano]
이 마지막 논쟁은 이 문서가 확인하지 못했고, 포트를 게시할 때 바인딩 주소를
지정하는 습관 자체는 실용적인 조언이다.

## 인사이트

### Docker의 성공은 커널 기능이 아니라 사용 방식이었다

vbezhenar는 Docker가 독특했던 이유가 컨테이너 기술이 아니라 Dockerfile(레이어별
빌드와 캐싱을 한 파일에 담음)과 네트워크 같은 사용 방식이었다고
했다.[^vbezhenar]
crote는 반대로 주된 매력은 컨테이너를 사소하게 만든 것이었다고 보았다.
격리를 직접 하려면 오래 걸리고 많은 사람이 Apache를 root가 아닌 uid로 포크하는
데서 멈췄을 텐데, Docker는 격리와 관리를 배터리 포함 방식으로 줬다는
것이다.[^crote]
kqr은 모멘텀이 더 중요하다며 컨테이너가 사실상 표준 배포 단위가 되어 그 가정으로
쓰인 도구가 많다는 점을 들었다.[^kqr]
세 답은 모두 글이 보여 준 하부 구조가 아니라 그 위의 사용성과 표준화가 성공의
원인이라고 본다.

### 창시자의 증언은 이 이상함의 기원이 선택의 연쇄임을 보여 준다

이 스레드에서 Docker의 창시자 shykes가 직접 답했다.
그는 Go의 선택이 맥락 특수적이었다고 했다.
첫 버전은 Python이었고, 당시 데브옵스 도구가 Ruby, Python, Java 같은 런타임별로
갈라져 있어서 컴파일된 단일 바이너리가 모든 진영에서 채택될 수 있었으며, 문법이
평이해 기여자를 끌어들이기에 좋았다는 것이다.[^shykes-go]
글의 Go가 커널 작업에 맞지 않는다는 지적이 절대적으로 맞지만 당시에는 올바른
선택이었다고도 말했다.[^shykes-go-fit]
또 Docker의 초기 형태는 LXC 이전의 OpenVZ에 기반했고, LXC는 커널 패치 모음으로
시작해 업스트림 경쟁에서 이길 것으로 보여 전환했으며, 처음 공개 버전은 LXC를
감쌌지만 신뢰할 수 없어 Go로 만든 `libcontainer`로 바꿨다고 했다.[^shykes-lxc]
이 서술은 shykes 본인의 기억이며, 이 문서는 다른 자료로 확인하지 못했다.
글이 이상하다고 부른 구조(작은 단위의 커널 기능 조합, Go와 C의 혼합)가 설계자의
사전 계획이 아니라 당시 도구들의 상태와 도입 전략의 누적이라는 점이 드러난다.

### 이 글을 읽는 방법

Docker를 VM으로 이해하고 쓰는 사람에게 이 글은 멘탈 모델을 고치는 짧은 입문이다.
직접 해 보려면 글이 권하는 대로 작은 런타임을 만들어 보는 것이 가장 빠르고,
HN에서
tyingq가 소개한 `bocker`(약 100줄의 bash로 만든 Docker)가 같은 점을 보여 준다고
한다.[^tyingq]
DANmode는 `bocker`가 소프트웨어 공격 표면은 작지만 격리가 사실상 없어 깨기
쉽다고 지적했다.[^danmode]
이 글의 주장을 가를 관찰은 두 가지다.
rootless 런타임이 네트워킹 기능에서 root 런타임과 같은 수준에 이르는지, 그리고
Rust로 만든 런타임(youki 등)이 `runc`의 우회 구현 없이 같은 기능을 어느 정도의
단순함으로 제공하는지다.
둘 다 이 글에는 없는 자료다.

---

[^paxy]: <https://news.ycombinator.com/item?id=50203293>

[^gzapp]: <https://news.ycombinator.com/item?id=50203152>

[^lambdacomplex]: <https://news.ycombinator.com/item?id=50204750>

[^j16sdiz]: <https://news.ycombinator.com/item?id=50203265>

[^stingraycharles]: <https://news.ycombinator.com/item?id=50203300>

[^0xbadcafebee]: <https://news.ycombinator.com/item?id=50203658>

[^fulafel]: <https://news.ycombinator.com/item?id=50204166>

[^miladyincontrol]: <https://news.ycombinator.com/item?id=50203590>

[^0x457]: <https://news.ycombinator.com/item?id=50203880>

[^gertop]: <https://news.ycombinator.com/item?id=50204216>

[^jlhawn]: <https://news.ycombinator.com/item?id=50204852>

[^rob74]: <https://news.ycombinator.com/item?id=50206639>

[^vbezhenar]: <https://news.ycombinator.com/item?id=50203975>

[^crote]: <https://news.ycombinator.com/item?id=50204186>

[^kqr]: <https://news.ycombinator.com/item?id=50205148>

[^shykes-go]: <https://news.ycombinator.com/item?id=50203120>

[^shykes-go-fit]: <https://news.ycombinator.com/item?id=50204922>

[^shykes-lxc]: <https://news.ycombinator.com/item?id=50203555>

[^tyingq]: <https://news.ycombinator.com/item?id=50203040>

[^danmode]: <https://news.ycombinator.com/item?id=50205027>

[^david_chisnall]: <https://lobste.rs/s/xsz9sc/docker_is_weird#c_meiire>

[^samuelkarp]: <https://lobste.rs/s/xsz9sc/docker_is_weird#c_d0npcs>

[^janus]: <https://lobste.rs/s/xsz9sc/docker_is_weird#c_o20uwi>

[^dutc]: <https://lobste.rs/s/xsz9sc/docker_is_weird#c_0jnw8k>

[^wink]: <https://lobste.rs/s/xsz9sc/docker_is_weird#c_1zfli3>

[^noirscape]: <https://lobste.rs/s/xsz9sc/docker_is_weird#c_vq3vih>

[^drrobotic]: <https://lobste.rs/s/xsz9sc/docker_is_weird#c_2m9jay>

[^altano]: <https://lobste.rs/s/xsz9sc/docker_is_weird#c_vaqk4d>
