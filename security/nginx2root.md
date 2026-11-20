# nginx2root 취약점 묶음

원문: [NGINX2Root: New Remote Code Execution Vulnerabilities in nginx Require Urgent Patching - Xint Blog | Insights from Offensive Security Researchers](https://xint.io/blog/nginx2root-remote-code-execution)

HN 토론: <https://news.ycombinator.com/item?id=50547423> (97점, 13개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=50547536> (7점, 1개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/wj2svg/nginx2root> (85점, 16개 댓글)

GN 토론: <https://news.hada.io/topic?id=37438>

## 요약

보안 업체 Xint가 낸 기술 글이다.
Xint 연구팀이 nginx에서 인증 없이 원격 코드 실행이 가능한 취약점 다섯 개를
찾았고, 별도로 Linux 커널의 SCTP 취약점을 찾았으며, 이 여섯 개를 합쳐
nginx2root라고 부른다고 한다.
다섯 개는 각각 독립된 공격 경로이고 영향받는 설정이 서로 다르다.
커널 취약점은 nginx 취약점 중 어느 것과도 이어 붙여 호스트의 root 권한을 얻을 수
있다고 글은 쓴다.

### 영향받는 설정

글은 취약점을 표로 정리한다.

| CVE             | 영향받는 설정                                  | 처음 영향받은 버전 | HTTP/2를 끄면 차단되는가 |
| --------------- | ---------------------------------------------- | ------------------ | ------------------------ |
| CVE-2026-123007 | HTTP/2 사용                                    | 1.9.5              | 그렇다                   |
| CVE-2026-123634 | resolver, 요청에서 정해지는 proxy_pass, mirror | 1.13.4             | 아니다                   |
| CVE-2026-123633 | HTTP/2와 업스트림으로의 전달                   | 1.19.7             | 그렇다                   |
| CVE-2026-121810 | HTTP/3와 업스트림으로의 전달                   | 1.25.0             | 아니다                   |
| CVE-2026-113425 | proxy on과 auth_http를 쓰는 메일 프록시        | 0.5.15             | 아니다                   |

가장 영향이 큰 것은 CVE-2026-123007이다.
HTTP/2가 켜진 nginx에서 인증 없이 명령을 실행할 수 있고, 명령은 요청을 처리하는
작업자(worker) 프로세스의 권한으로 실행된다.
이 코드는 2015년 nginx가 HTTP/2를 도입한 1.9.5부터 있었고, 1.31.8까지의 모든
공식 릴리스와 2026년 11월 10일의 master 브랜치가 포함한다고 한다.
수정은 1.31.9에 들어가며, 그 전에는 영향받는 포트에서 HTTP/2를 끄면
CVE-2026-123007과 CVE-2026-123633을 막는다고 한다.

### 발견과 공개 경과

글에 따르면 ZeroDay Cloud 2026을 준비하던 Xint 연구원이 CVE-2026-123007을
찾았고, 며칠 뒤 완전 자동화된 Xint 스캔이 나머지 넷을 사람의 안내 없이 찾았다.
공개 경과는 다음과 같다.

- 10월 11일 발견, 10월 16일 HackerOne을 통해 F5에 보고, 10월 20일 HackerOne의
검증 완료, 10월 27일 nginx 개발팀에 전달.
- 11월 9일 nginx 팀이 패치 검증을 요청하고 11월 10일 Xint가 검증을 끝냈으며,
11월 18일 패치 릴리스가 예정되어 있었다.

### 노출과 점검

2026년 11월 10일 Shodan은 `product:nginx`로 5,670만 호스트를 보여 주었고, 그중
1,194만(21.1%)이 식별 가능한 버전을 알렸다.
버전이 식별된 호스트의 98.9%가 CVE-2026-123007의 영향 범위(1.9.5~1.31.8)에
들어간다고 글은 쓴다.
다만 이 수치는 보고된 버전 문자열에 근거하며 취약함을 확인한 것이 아니다.
배포판은 버전을 바꾸지 않고 수정을 되돌려 적용(backport)할 수 있으므로 `nginx
-v`만으로 패치 여부를 알 수 없다고 한다.
글은 Ubuntu 22.04의 1.18.0-6ubuntu14가 10월 26일 보안 업데이트로
1.18.0-6ubuntu14.22가 된 예를 든다.

점검 방법은 네 단계이다.
`nginx -v`로 버전을, `nginx -V`로 HTTP/2 모듈 포함 여부를, `nginx -T`로 설정의
HTTP/2 활성화를, 외부에서 `openssl s_client`로 ALPN `h2` 협상을 확인한다.
CDN이나 리버스 프록시가 앞에 있으면 그 점검은 프록시에만 닿으므로 nginx에 직접도
해야 한다고 한다.

공격 흔적은 접근 로그에 거의 남지 않을 수 있다.
트리거에 쓰는 WINDOW_UPDATE와 RST_STREAM 제어 프레임은 요청으로 기록되지 않고
TLS로 암호화되기 때문이다.
글은 연결 통계(`ss -tinp`), 연결당 요청 수를 남기는 로그 형식, 작업자가 시작한
프로그램, 작업자 충돌을 함께 보라고 안내한다.

### 임시 완화

- HTTP/2를 끈다(CVE-2026-123007, CVE-2026-123633). gRPC처럼 HTTP/2가 필요한
서비스는 영향을 받는다.
- 요청 시점 DNS 조회를 없애고 proxy_pass를 고정 업스트림 그룹으로
바꾼다(CVE-2026-123634). `mirror_request_body on`만으로는 고쳐지지 않는다고
한다.
- QUIC 수신기를 제거하고 `http3 off`와 `Alt-Svc 'clear'`를
쓴다(CVE-2026-121810).
- 메일 프록시를 루프백에 묶거나 방화벽으로 신뢰하는 주소만
허용한다(CVE-2026-113425).
- 설정을 다시 읽는 reload는 열려 있는 연결을 옛 작업자에 남기므로, 필요하면
서비스를 재시작한다.

### 기술 분석

CVE-2026-123007은 HTTP/2 흐름 제어에서 생기는 정수 오버플로이다.
nginx는 응답 DATA를 큐에 넣을 때 연결 전체 송신 창과 스트림 송신 창에서 길이를
뺀다.
스트림이 DATA를 보내기 전에 취소되면 정리 과정이 뺐던 길이를 연결 송신 창에
되돌려 더한다.
그 사이에 클라이언트가 WINDOW_UPDATE로 창을 키우면, 되돌린 값이 최대치를 넘고
정리 과정은 이를 검사하지 않는다.
이후 같은 비트를 부호 있는 값과 없는 값으로 해석해 아주 큰 복사 길이가 생기고
힙의 범위 밖 읽기와 쓰기가 일어난다고 한다.

나머지 넷은 해제 후 사용(use-after-free)이다.
CVE-2026-123634는 DNS 리졸버에서 한 요청의 처리기가 대기 목록 순회가 아직
처리하지 않은 다른 컨텍스트를 해제한다.
CVE-2026-123633은 활성 HTTP/2 연결이 연결 회수 대상으로 남아, 업스트림 연결을 열
때 요청 자신의 연결 메모리가 해제된다.
CVE-2026-121810은 같은 계열로 QUIC 연결을 닫는 중에도 HTTP/3 요청이 실행되는
경우이다.
CVE-2026-113425는 메일 프록시의 auth_http 경로에서 클라이언트 연결을 닫아 세션을
해제했는데 인증 서비스 연결이 남아 이후 이벤트가 해제된 세션을 쓴다.
글은 주소 노출과 제어된 메모리 훼손까지 설명하고 완전한 익스플로잇을 재현할
마지막 단계는 일부러 뺀다고 밝힌다.

커널 취약점은 SCTP 송신 경로에 있다.
송신이 대기하는 동안 그 연결(association)이 다른 소켓으로 옮겨질 수 있고, 대기
중인 송신이 옮겨진 연결을 해제하면 해제 후 사용이나 이중 해제가 된다.
글은 이 버그가 2018년 Linux v4.15에 들어와 8년 넘게 있었다고 쓴다.
익스플로잇은 KASLR을 무력화하는 커널 메모리 노출과 커널의 임의 함수 호출을
제공하고, 작업자 권한에서 root를 안정적으로 얻었으며 Docker 컨테이너 안의
nginx에서도 호스트 root를 얻었다고 한다.
커널 패치가 나오기 전에는 SCTP를 쓰지 않는 호스트가 `/etc/modprobe.d/`에
`install sctp /bin/false`를 두어 모듈 로드를 막을 수 있다고 안내한다.

글은 최근 nginx 보안 권고 목록이 2025년에 2건이던 것이 2026년 11월 17일까지
nginx2root를 빼고 26건으로 늘었다고 쓰고, AI를 쓴 연구가 잘 연구된 코드에서도 더
빨리 버그를 찾는다고 말한다.
맺음에서는 이 버그들이 수년간의 보안 검토를 거치고도 완전 자동화된 Xint 스캔이
찾을 때까지 남았다고 쓴다.
데모 영상과 AWS, GCP, Azure, 베어메탈 시연은 nginx2root.com에서 볼 수 있다고
한다.

## 분석

### 다섯 개의 독립 경로가 하나의 이름으로 묶였다

글의 틀은 여섯 취약점을 nginx2root라는 한 이름에 두는 것이다.
다섯 개는 각각 독립된 공격 경로이고 설정마다 영향이 달라서 한 번의 조치로 모두
막히지 않는다.
표의 마지막 열이 이를 보여 주며, HTTP/2를 끄면 둘만 막힌다는 점이 임시 완화의
한계이다.
이는 글의 서술을 이 문서가 정리한 것이다.

HN에서 outloudvi는 SCTP 취약점이 이미 석 달 전에 공개된 것이고 Tencent가 발견한
것을 Xint가 재현한 것이라며 이름이 nginx2root인 것이 과장이라고
지적했다.[^outloudvi]
글은 커널 취약점을 Xint가 별도로 찾았다고 쓰는데, 이 대립은 이 문서가 확인하지
못했다.

### 패치 전 공개는 완화 가능성을 근거로 한다

글은 패치가 11월 18일로 예정되어 있었다고 쓰면서도 상세한 기술 분석과 점검
방법을 함께 낸다.
Lobste.rs에서 rbca는 패치가 나오기 전에 이런 정보를 공개한 이유를 물었다.[^rbca]
marginalia는 이미 세부가 퍼져 있어 통상의 조정된 공개 절차가 의미 없었을 수
있다고 답했고,[^marginalia] refi64는 다섯 곳이 같은 문제를 일부 찾았다면
릴리스가 나오는 순간 취약점이 알려질 것이라고 덧붙였다.[^refi64]
jamesnvc는 HTTP/2를 끄면 막을 수 있어 공격자가 역공학하는 경쟁이 덜하기 때문일
것이라고 추측했고,[^jamesnvc] nbyqvist는 이미 개념 증명 스크립트가 있고 목적은
완화를 하게 하는 것이라고 적었다.[^nbyqvist]
이들은 모두 댓글 작성자의 추정이며 글 자체는 공개 시점의 이유를 쓰지 않는다.

### 운영자를 위한 실행 정보가 글의 큰 부분이다

점검 명령, 로그 형식, 완화 설정이 글의 절반 가까이를 차지한다.
HN의 patryk_builds는 업데이트 뒤 `nginx -s reload`가 새 바이너리를 불러오지 않고
재시작이 필요하다는 줄이 가장 쓸모 있다고 짚었다.[^patryk_builds]
citrin_ru는 nginx가 연결을 끊지 않고 바이너리를 우아하게 올리는 기능이 있다고
보충했다.[^citrin_ru]
이는 글의 점검과 완화 안내가 현장에서 어떻게 읽히는지를 보여 준다.

## 비평

### 영향 규모의 수치는 버전 문자열에 기댄다

글의 Shodan 수치는 노출을 짐작하게 하지만 글 스스로 이 수치가 취약함을 확인한
것이 아니라고 쓴다.
버전이 식별된 호스트가 전체의 21.1%이고, HTTP/2 활성화 여부와 되돌려 적용된
수정은 반영되지 않는다.
Lobste.rs의 sigmonsez는 Ubuntu 기본 설치에는 HTTP/2가 켜져 있지 않다며 마케팅이냐고 물었고,[^sigmonsez] Verfeuil은 점검한 서버가 모두 HTTP/2를 켠 상태였다고 답했다.[^Verfeuil]
dmbaturin은 CertBot이 HTTP/2를 켜지 않아서 다행이라고 적었다.[^dmbaturin]
실제 위험은 설정 분포에 달려 있으며 글은 이 분포를 제시하지 않는다.

### 이름과 홍보의 문제가 반응에서 나온다

HN의 philipwhiuk는 막 만든 사이트에서 다섯 취약점과 책임 있는 공개를 말하면서
nginx.org에 수정이 나오지 않은 점이 마음에 들지 않는다고 적었고,[^philipwhiuk]
mountainrose는 F5가 이미 패치를 냈다고 답했다.[^mountainrose]
whalesalad는 취약점에 도메인과 사이트를 두는 일이 언제부터 유행했느냐고 물었고,
jl6은 좋은 취약점에는 브랜딩이 필요하다고 답했다.[^whalesalad][^jl6]
이 반응은 글의 기술 내용과 별개로 취약점 이름 짓기와 알리기의 방식에 대한
것이다.

### 자동 스캔의 주장은 근거가 글에 없다

글은 완전 자동화된 Xint 스캔이 나머지 넷을 사람 안내 없이 찾았다고 쓴다.
맺음에서도 수년간 검토된 코드에서 자동 스캔이 찾았다는 점을 강조한다.
자동 스캔의 방법, 오탐 비율, 사람이 확인한 단계는 글에 없고, 이 주장은 회사의
설명이다.
Xint는 이 분석으로 자사 제품의 능력을 알리는 위치에 있다는 점을 읽는 쪽이
감안해야 한다.

### 배포판의 상태는 시점이 지나면 달라진다

Lobste.rs의 ggpsv는 글이 나왔을 때 Debian 안정판의 nginx가 취약한데 보안 권고도 업데이트도 없다고 적었다.[^ggpsv]
이후 gerikson은 Ubuntu 두 대에서 apt update로 새 nginx가 올라왔다고
적었고,[^gerikson] keybits는 외부 저장소에서 1.31.9가 이미 제공된다고
적었다.[^keybits]
글의 점검 안내가 말하듯 배포판마다 수정 시점이 다르며, 이 문서는 현재 각
배포판의 상태를 확인하지 못했다.

### 외부 반응

cadey는 메모리 안전성 풍자 글을 링크했고,[^cadey] toastal은 주류가 아닌 리버스
프록시를 쓰면 표적이 덜 된다는 이점을 적었다.[^toastal]
refi64는 같은 연구자가 비슷한 시기에 다른 프로젝트에서도 심각한 취약점을
찾았으나 아직 말할 수 없다는 이야기를 덧붙였다.[^refi64-other]
이는 댓글 작성자의 주장이며 이 문서가 확인하지 못했다.

## 인사이트

### 취약점 정보는 확인 수단과 함께 나올 때 쓸모가 있다

글은 영향 범위를 말하는 데 그치지 않고 서버가 영향권인지 판단하는 명령, 흔적을
찾는 방법, 설정별 완화를 함께 준다.
Lobste.rs의 반응처럼 공개 시점이 논란이어도 점검 정보가 없는 공개보다 낫다는 의견이 가능하다.
다만 이 정보가 공격자에게도 같은 가치를 준다는 점이 긴장으로 남는다.
이는 이 문서의 해석이다.

### 버전 번호로 취약 여부를 판단할 수 없는 세계가 되었다

글이 반복해서 경고하듯 배포판은 버전을 바꾸지 않고 수정을 되돌려 적용한다.
컨테이너 이미지 태그도 다시 빌드되었는지가 문제이고, HN의 patryk_builds가 같은
우려를 적었다.[^patryk_builds]
취약점 관리에서 버전 비교는 출발점일 뿐 완전한 패키지 버전과 권고문의 대조가
필요하다는 점이 이 사건의 실무적 교훈이다.

### 기본 설정이 위험 노출의 크기를 정한다

HTTP/2가 기본으로 꺼져 있는지 켜져 있는지에 따라 같은 취약점의 규모가 달라진다.
sigmonsez와 Verfeuil의 상반된 관찰은 기본값과 운영자의 선택이 결합해 노출을
결정한다는 점을 보여 준다.
기능을 켜는 습관이 쌓인 환경일수록 오래된 코드의 취약점에 더 노출된다는
구조이다.
이는 이 문서의 해석이다.

### 확인할 관찰

이 문서의 해석을 가를 관찰은 세 가지이다.
1.31.9 릴리스와 각 배포판 패치가 다섯 CVE를 모두 포함하는지,
공개 뒤 실제 공격 시도가 보고되는지,
SCTP 커널 취약점의 수정 시점과 발견자 귀속이다.
세 가지 모두 이 문서가 확인하지 못했다.

---

[^outloudvi]: <https://news.ycombinator.com/item?id=50548372>

[^rbca]: <https://lobste.rs/s/wj2svg/nginx2root#c_owgios>

[^marginalia]: <https://lobste.rs/s/wj2svg/nginx2root#c_6rvb9h>

[^refi64]: <https://lobste.rs/s/wj2svg/nginx2root#c_fy9ykr>

[^jamesnvc]: <https://lobste.rs/s/wj2svg/nginx2root#c_kdzbyw>

[^nbyqvist]: <https://lobste.rs/s/wj2svg/nginx2root#c_erz6ko>

[^patryk_builds]: <https://news.ycombinator.com/item?id=50548335>

[^citrin_ru]: <https://news.ycombinator.com/item?id=50550072>

[^sigmonsez]: <https://lobste.rs/s/wj2svg/nginx2root#c_pensex>

[^Verfeuil]: <https://lobste.rs/s/wj2svg/nginx2root#c_zohgdr>

[^dmbaturin]: <https://lobste.rs/s/wj2svg/nginx2root#c_un6wf1>

[^philipwhiuk]: <https://news.ycombinator.com/item?id=50547568>

[^mountainrose]: <https://news.ycombinator.com/item?id=50547721>

[^whalesalad]: <https://news.ycombinator.com/item?id=50549611>

[^jl6]: <https://news.ycombinator.com/item?id=50549875>

[^ggpsv]: <https://lobste.rs/s/wj2svg/nginx2root#c_k4kx9x>

[^gerikson]: <https://lobste.rs/s/wj2svg/nginx2root#c_hab7da>

[^keybits]: <https://lobste.rs/s/wj2svg/nginx2root#c_swsznq>

[^cadey]: <https://lobste.rs/s/wj2svg/nginx2root#c_1b6hg0>

[^toastal]: <https://lobste.rs/s/wj2svg/nginx2root#c_vxwc6m>

[^refi64-other]: <https://lobste.rs/s/wj2svg/nginx2root#c_auzitc>
