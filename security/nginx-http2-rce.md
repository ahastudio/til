# NGINX HTTP/2 원격 코드 실행 취약점

원문: [Unauthenticated Remote Code Execution in NGINX: CVE-2026-123633 and CVE-2026-123007](https://www.wiz.io/blog/nginx-http2-rce-vulnerabilities)

HN 토론: <https://news.ycombinator.com/item?id=50547374> (1159점, 514개 댓글)

GN 토론: <https://news.hada.io/topic?id=37417>

## 요약

2026년 11월 18일 Wiz Research(Nir Ohfeld, Tomer Schwartz)가 낸 보안 분석 글이다.
F5가 같은 날 낸 NGINX 보안 릴리스에 맞춘 조율된 공개이다.
HTTP/2 구현의 두 취약점 CVE-2026-123633(연결 해제 후 사용, use-after-free)과 CVE-2026-123007(전송 윈도 정수 언더플로)이 NGINX 서버를 장악하는 데 쓰일 수 있다고 한다.
Wiz는 둘 다 CVSS 4.0 9.2(Critical)로 매기고 NGINX가 2억 2,500만 개 이상의 웹사이트를 돌린다는 Netcraft와 W3Techs 자료를 인용한다.
발견자는 Wiz Research, Ikotas Labs, Metnir, Rapid7, Xint이고 서로 독립적으로 찾아 F5에 알렸다고 한다.
F5의 권고 문서(K000163928, K000163926), CVE.org와 NVD 페이지는 내용이 없는 셸 페이지만 열려 읽지 못했다.
직접 재현하거나 서버에서 시험하지 않았다.

## 지금 할 일

1. 영향을 받는지 확인한다. HTTP/2가 켜진 NGINX가 있는지 본다. 설정에서 `listen` 지시어의 `http2` 매개변수나 `http2 on;`이 있는지 찾는다. 일반 명령으로는 `nginx -v`로 버전을, `nginx -T`로 합쳐진 전체 설정을 확인할 수 있다(이 두 명령은 권고문이 아니라 일반 사용법이다).
2. 가능하면 고친 버전으로 올린다. nginx.org의 안정 버전은 1.30.7, 메인라인은 1.31.9이다(둘 다 2026년 11월 18일).
3. 바로 올릴 수 없으면 임시로 HTTP/2를 끈다. 아래 「임시 완화」를 따른다.
4. 완화나 업그레이드 뒤 설정을 다시 읽고 이전 워커가 끝났는지 확인한다.
5. 크래시와 비정상 자식 프로세스를 점검한다.

## 취약점

| 항목                 | CVE-2026-123633                                     | CVE-2026-123007                             |
| -------------------- | --------------------------------------------------- | ------------------------------------------- |
| 종류                 | HTTP/2 연결 사용 후 해제(use-after-free)            | HTTP/2 흐름 제어(send_window) 정수 언더플로 |
| Wiz 평가             | CVSS 4.0 9.2, 인증 없는 임의 코드 실행              | CVSS 4.0 9.2, 인증 없는 임의 코드 실행      |
| 영향 버전(nginx.org) | 1.19.7부터 1.31.8                                   | 1.9.5부터 1.31.8                            |
| 조건                 | HTTP/2 리버스 프록시 구성에서 악용 가능성이 더 높음 | HTTP/2가 켜진 기본 구성                     |
| nginx.org 심각도     | medium                                              | major                                       |
| 발견(변경 기록)      | Albert of Vexera AI                                 | Xint.io                                     |

원인은 다음과 같이 설명된다.

- CVE-2026-123633: HTTP/2 연결에 활성 스트림이 없으면 NGINX가 연결을 「재사용 가능」으로 표시하는데, 요청 스트림이 만들어질 때 이 표시가 지워지지 않는다. 공격자가 HEADERS 프레임을 나눠 보내면 NGINX가 닫아도 되는 연결에서 요청이 실행된다. 업스트림 연결 슬롯이 부족하면 그 연결이 닫히는데, GOAWAY 프레임을 만들지 못하면 오류 경로가 연결을 해제하고 요청은 그 메모리를 계속 쓴다. 해제된 메모리가 재사용되면 코드 실행으로 이어진다고 한다. nginx.org의 변경 기록은 이를 `worker_connections`가 부족할 때의 HTTP/2 use-after-free로 적는다.
- CVE-2026-123007: 취소된 스트림의 대기 데이터를 버릴 때 `send_window`로의 환불이 HTTP/2 최대 윈도로 제한되지 않는다. 뒤의 경계 검사가 부호 없는 뺄셈으로 줄어들어 윈도가 더 커지는 것을 허용하고, 부풀려진 값이 `ngx_http_v2_send_chain()`에서 음수 `off_t`가 되어 잘못된 버퍼를 만들며 `ngx_ssl_send_chain()`이 범위 밖 복사를 한다. 메모리 노출과 힙 손상이 가능하다고 한다. Wiz는 정적 파일만 제공하는 HTTPS 서버(64비트, 백엔드나 서드파티 모듈 없음)에서 ASLR 우회를 포함한 코드 실행을 공식 1.31.7과 1.31.8 빌드에서 확인했다고 한다.

같은 릴리스에는 다른 보안 수정이 더 있다.

| CVE             | 내용                                                  | nginx.org 심각도 | 영향 버전                     |
| --------------- | ----------------------------------------------------- | ---------------- | ----------------------------- |
| CVE-2026-121810 | HTTP/3 use-after-free                                 | medium           | 1.25.0부터 1.31.8             |
| CVE-2026-123634 | 리졸버 use-after-free(같은 이름을 하위 요청에서 해석) | medium           | 0.6.18부터 1.31.8             |
| CVE-2026-113425 | 메일 프록시 모듈 use-after-free                       | major            | 0.5.33부터 1.31.8             |
| CVE-2026-118899 | TLS 1.3 요청 본문 읽기 무한 루프(서비스 거부)         | major            | 1.13.0부터 1.31.8             |
| CVE-2026-120967 | stream의 SNI와 클라이언트 인증서 검증 우회            | medium           | 1.25.5부터 1.31.8             |
| CVE-2026-123640 | stream `ssl_preread` 검증 부족                        | minor            | 1.15.2부터 1.31.8             |
| CVE-2026-120993 | PROXY protocol v2 널 포인터 역참조                    | minor            | 1.31.4부터 1.31.8(메인라인만) |
| CVE-2026-125283 | `alias`와 `try_files` 버퍼 오버플로                   | minor            | 0.9.6부터 1.31.8              |

Wiz 글은 CVSS를 나열하지만 nginx.org의 심각도 등급(minor, medium, major)은 다른 체계이다. 두 척도를 섞어 읽지 않아야 한다.

## 고친 버전

- NGINX 오픈소스: 1.30.7(안정)과 1.31.9(메인라인)에서 위 취약점이 모두 고쳐졌다. 단 CVE-2026-120993은 메인라인 1.31.4에서 1.31.8에만 해당하고 1.31.9에서 고쳐졌다. 1.31.9는 헤더 줄에 콜론이 없는 요청을 거부하고 청크 본문의 프레이밍 오버헤드가 과하면 거부하는 변경도 포함한다.
- NGINX Plus(Wiz 글의 표): CVE-2026-123633은 37.0.7.1과 37.2.0.1, CVE-2026-123007은 37.0.8.1과 37.3.0.1에서 고쳐졌다. F5 권고 원문을 읽지 못해 이 값은 Wiz의 서술이다.
- NGINX Ingress Controller, Gateway Fabric, Unit 등 다른 제품의 고친 버전은 읽은 자료에 없었다.

## 임시 완화

HTTP/2를 끈다. Wiz 글과 Red Hat 모두 같은 방법을 안내한다.

- 영향받는 `server` 블록에 `http2 off;`를 둔다(NGINX 1.25.1 이상. `http2` 지시어는 1.25.1에서 생겼다).
- 모든 `listen` 지시어에서 `http2` 매개변수를 제거한다(구버전은 이것만 가능).
- 애플리케이션 호환성을 시험하고 NGINX를 다시 로드(reload)한 뒤 이전 워커가 종료되었는지 확인한다. 업그레이드한 뒤에 HTTP/2를 다시 켠다.

한계는 다음과 같다.

- 다른 CVE는 HTTP/2가 아니라 HTTP/3, 리졸버, 메일 프록시, stream, `alias`와 `try_files`에 있다. nginx.org의 제목에 따르면 HTTP/2를 끄는 것으로 막히지 않으므로 해당 기능을 쓰면 업그레이드가 필요하다. 이는 권고 제목에서 읽은 추론이다.
- gRPC 서비스처럼 HTTP/2가 필수인 서비스는 끌 수 없다. HN에서 gRPC API가 주력인 서비스는 선택지가 아니라는 반응이 있었다.[^verst]

## 탐지

Wiz는 로그 질의나 침해 지표(IOC)를 제시하지 않는다. 일반 징후로 예상치 못한 NGINX 워커 크래시와 NGINX가 실행한 명령을 조사하라고 하되 이것이 두 취약점의 확정 지표는 아니라고 한다. CVE-2026-123007은 많은 WINDOW_UPDATE 프레임이 필요하므로 오래 유지되는 HTTP/2 연결이 많은 데이터를 보내는 경우를 잡는 규칙을 제안한다. Wiz 고객은 Threat Center의 질의를 쓸 수 있다.
악용 여부: 이 글은 야생 악용을 주장하지 않고 PoC를 공개하지 않는다고 한다. 다만 Wiz는 PoC를 만들어 여러 실험 환경에서 돌려 보았고, 공격자는 NGINX 서버에 직접 닿아야 하며 HTTP/2를 종료하는 CDN이나 WAF가 일부 악용을 막을 수 있다고 한다. 악용이 어렵다는 점(메모리 노출, 힙 조작, 빌드별 대응)과 동일 빌드의 패키지 제품이 먼저 공격받을 수 있다는 점도 적는다.

## 공개 경과

- 10월 21일: Wiz가 첫 번째 HTTP/2 use-after-free를 F5에 보고했다. F5는 다른 팀이 이미 보고했다고 답했다.
- 11월 10일: F5가 CVE-2026-123633의 패치를 검토용으로 보냈다.
- 11월 16일: Wiz가 두 번째 HTTP/2 버그를 보고했다. 11월 17일 F5가 CVE-2026-123007이 18일 릴리스에 포함됨을 확인했다.
- 11월 18일: F5 보안 릴리스와 공개.

## 비평

### 심각도 서술이 출처마다 다르다

Wiz는 둘 다 CVSS 4.0 9.2의 인증 없는 원격 코드 실행이라고 쓴다. nginx.org는 CVE-2026-123633을 medium으로, CVE-2026-123007을 major로 매긴다. Ubuntu와 Red Hat은 CVE-2026-123633을 CVSS 3.1 8.1(High)로 매기고 Ubuntu는 4.0 9.2도 적는다. 배포판 설명은 서비스 거부와 코드 실행 가능성을, 코드 실행은 주로 ASLR이 꺼졌거나 우회 가능한 경우로 서술한다.
따라서 영향 서술은 「즉시 임의 코드 실행」으로 일반화하기보다 구성과 조건에 따라 달라진다고 읽는 편이 안전하다. 어느 쪽이든 패치 우선순위는 높다.

### 악용의 난이도에 대한 평가가 갈린다

HN에서 한 사용자는 128GB의 HTTP/2 트래픽과 특정 CPU 명령이 필요해 실제로는 문제가 아니라는 트윗을 링크했고, 다른 사용자는 가치 있는 대상이면 의지 있는 공격자가 시도할 것이라고 반박했다.[^testtestmetest][^zackwu]
Wiz도 악용이 어렵다고 쓰지만 공개된 분석(Xint의 글)이 이미 있다는 HN 댓글이 있다.[^pelzatessa]

### 조율된 공개와 패치 노출 시차 논란이 있다

HN에서 한 사용자는 버그가 공개 저장소에서 일주일 전에 고쳐져 있었고 커밋 메시지에 보고자까지 적혔으니 저장소를 감시하던 누구나 악용할 수 있었다고 지적했다.[^black3r] 다른 사용자는 공식 패치가 GitHub에 올라오기 전에 웹사이트가 먼저 나왔다며 조율을 물었고, 한 사용자는 도메인 인증서가 11월 2일에 발급되어 인증서 투명성 로그를 보면 16일 앞서 알 수 있었다고 했다.[^peanut-walrus][^nikcub]
발견자가 겹친 것(5개 팀)에 대해서는 에이전트로 취약 영역을 훑는 시대의 반영이라는 의견이 나왔다.[^retr0id][^ryanschaefer] Xint 쪽 사용자는 자신들이 몇 가지 버그를 더 찾았고 전체 체인을 글로 냈다고 밝혔다.[^yerimyerimie]

### 글의 범위가 대응에 부족한 부분이 있다

Wiz 글에는 노출된 인스턴스 수, 벤더 권고 링크(nginx.org 보안 권고와 F5 권고), 로그 질의가 없다.
프록시 뒤의 NGINX에 대한 영향도 글에서 명확히 구분되지 않는다.
한 사용자는 NGINX가 HAProxy 뒤에 있어 HTTP/2/TLS를 직접 받지 않으면 영향이 없다고 판단했으나 같은 릴리스의 다른 CVE(리졸버, 메일 프록시)는 평문 HTTP에도 해당한다는 반박이 있었다.[^8by3][^wildmxranat]

### 외부 반응

HN 글 제목은 「Unauthenticated remote code execution in Nginx」이다. 댓글의 한 갈래는 AI가 인터넷을 불태운다는 우려와 AI가 인터넷을 지킨다는 반론이었다.[^fn-mote][^jacobgold]
Lobste.rs의 `wiz.io` 도메인에는 13건이 있으나 이 글은 없었다.

## 기억할 원칙

- 취약점 공지는 영향받는 구성 조건(HTTP/2 사용 여부, 프록시 여부, 모듈)을 먼저 맞춰 본다. 평문 HTTP, 리졸버, 메일 프록시 CVE는 HTTP/2를 끈다고 막히지 않는다.
- 우선순위는 한 점수가 아니라 여러 출처의 심각도와 조건으로 정한다. 업그레이드를 기본으로 하고 임시 완화는 다음 점검 전까지만 둔다.
- 업그레이드 뒤 이전 워커가 끝났는지 확인하고, 컨테이너 이미지는 다시 빌드한다.
- HTTP/2가 필수인 서비스(gRPC 등)는 HTTP/2를 끄는 완화를 쓸 수 없으므로 패치 일정을 앞당긴다.
- 배포판 패키지의 고친 버전은 상류 버전과 다르므로 배포판 공지에서 확인한다.

---

[^verst]: <https://news.ycombinator.com/item?id=50548865>

[^testtestmetest]: <https://news.ycombinator.com/item?id=50554914>

[^zackwu]: <https://news.ycombinator.com/item?id=50555142>

[^pelzatessa]: <https://news.ycombinator.com/item?id=50550457>

[^black3r]: <https://news.ycombinator.com/item?id=50548510>

[^peanut-walrus]: <https://news.ycombinator.com/item?id=50548572>

[^nikcub]: <https://news.ycombinator.com/item?id=50550689>

[^retr0id]: <https://news.ycombinator.com/item?id=50547678>

[^ryanschaefer]: <https://news.ycombinator.com/item?id=50547875>

[^yerimyerimie]: <https://news.ycombinator.com/item?id=50547891>

[^8by3]: <https://news.ycombinator.com/item?id=50548439>

[^wildmxranat]: <https://news.ycombinator.com/item?id=50549033>

[^fn-mote]: <https://news.ycombinator.com/item?id=50548180>

[^jacobgold]: <https://news.ycombinator.com/item?id=50548492>
