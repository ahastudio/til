# Java4Shell: OpenJDK Base64 취약점

원문: [Java4Shell: Write once, RCE everywhere](https://calif.io/java4shell/)

HN 토론: <https://news.ycombinator.com/item?id=50538240> (757점, 200개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/g0bf9i/java4shell_write_once_rce_everywhere>

GN 토론: <https://news.hada.io/topic?id=37370>

## 요약

보안 업체 Calif가 2026년 11월 17일 공개한 취약점 보고서이다.
이 문서는 개요와 기술 해설, 영향 받는 제품과 권고 절까지 전문을 읽었다.
개념 증명 코드는 읽었지만 실행하지 않았고, 영상과 제품별 공격 체인은 보지 못했다.
아래 내용은 모두 Calif의 주장이며, 이 문서는 공격 절차를 옮기지 않고 취약점의 성격과 대응만 정리한다.

Calif는 OpenJDK의 Base64 디코더에서 메모리 손상 취약점을 찾았고 CVE-2026-114938, 별칭 Java4Shell이라고 불렀다.
CVSS 4.0 점수는 10점 만점에 9.2(CRITICAL)라고 한다.
자격 증명이 없는 원격 공격자가 힙 메모리를 덮어쓰고, Heartbleed처럼 메모리를 읽어 내고, 원격 코드 실행(RCE)까지 갈 수 있다는 주장이다.

원인은 이렇게 설명한다.

- 위치: HotSpot이 x86-64에서 Base64 속도를 높이려 쓰는 AVX-512 VBMI 명령어 기반 어셈블리 구현(intrinsic)이다.
- 결함: 끝부분의 패딩 문자 `=`를 처리할 때 출력 길이를 잘못 계산해 쓰기 마스크가 전부 켜지고, 할당된 버퍼 밖으로 쓰기가 넘친다. 이 입력은 결국 예외로 거부되지만 그 전에 이웃 객체가 이미 손상될 수 있다.
- 조건: 하드웨어가 AVX-512 VBMI를 지원해야 한다. ARM64 CPU는 영향이 없다.
- 영향 버전: OpenJDK 17.0.6 이상이며, 이를 기반으로 하는 배포판(Amazon Corretto, Eclipse Temurin, Microsoft Build of OpenJDK, Azul Zulu, BellSoft Liberica, SAP SapMachine, Red Hat OpenJDK, Oracle OpenJDK, Oracle Java SE, Oracle GraalVM for JDK)도 영향권이라고 한다. Oracle이 알려 준 영향 버전은 8u511b33-perf, 17.0.21.0.3, 21.0.13.0.3, 25.0.5.0.3, 27.0.1.0.3이다.
- 하드웨어: Intel Xeon(Ice Lake, Sapphire Rapids, Emerald Rapids, Granite Rapids)과 AMD(EPYC, Ryzen Zen 4 이상)가 요건을 충족한다고 한다.

Calif가 보인 영향은 다음과 같다.

- 기본 설정에서 인증 전 RCE를 시연한 제품: Keycloak, Atlassian Jira, Atlassian Confluence, JFrog Artifactory, Jenkins, PingFederate.
- 인증 후 RCE: Apache Kafka Broker, Apache Solr, Elasticsearch, Gerrit, Spinnaker. 목록은 전부가 아니라고 한다.
- 서버를 열지 않는 클라이언트도 악의적인 TLS 서버에 접속하면 공격당할 수 있다는 외부 연구자의 사례를 전한다.
- 범용 공격 코드는 없다. 디코더에 이르는 경로, 힙 배치, 응답으로 메모리를 읽어 낼 경로 등이 응용 프로그램마다 달라 대상마다 맞춤 작업이 필요하다고 스스로 밝힌다.
- 제품별 공격 체인은 모두가 업데이트할 시간을 가질 때까지 공개하지 않고 나중에 낸다고 한다.

대응은 다음과 같다.

- OpenJDK 보안 공지와 Oracle 패치가 2026년 11월 17일 오후 1시(태평양 시간)에 나왔고, 모든 Java 사용자가 바로 업데이트하라고 권한다.
- 임시 완화책은 JVM 옵션 `-XX:-UseBASE64Intrinsics`(하드웨어 가속 Base64 끄기) 또는 `-XX:UseAVX=2`(AVX-512 끄기)이다. 뒤의 것은 x86-64 호스트에만 쓰라고 하며 ARM의 OpenJDK는 이 옵션을 몰라 시작에 실패한다고 한다.
- 리눅스에서는 `/proc/cpuinfo`에 `avx512f`, `avx512bw`, `avx512vbmi`, `bmi2` 네 플래그가 모두 있는지로 자기 CPU가 해당하는지 확인할 수 있다.
- 한계로 밝힌 것: 일부 공격 프로필은 요청 본문의 일부만 보내는 스트리밍이 필요해, 본문 전체를 버퍼링하는 프록시(nginx 기본값)가 그 시점 조절을 없앤다. 다만 이것이 일반적인 완화책은 아니라고 적는다(Elasticsearch는 완전한 요청 하나로 돌아가고, 웹소켓 업그레이드 뒤에는 버퍼링이 적용되지 않는다).

보고서는 또 AI를 쓴 발견 과정을 적는다.

- 발견: 연구원이 OpenJDK의 JIT 컴파일러, intrinsic, 널리 쓰이는 API, 암호 부분을 Codex에게 감사시켰고 20분 가까이 쓸모없는 결과를 무시하며 프롬프트를 밀어붙인 끝에 이 결함이 나왔다고 한다. 발견에 1시간, 첫 동작하는 공격 코드까지 2시간이 더 들었고 토큰 비용은 200달러 미만이라고 한다.
- 사람과 AI의 분업: 파이프라인과 전략은 사람이 먼저 만들고, 이후 체인의 대부분은 AI가 거의 자율적으로 만들었다고 한다. 힙 배치 단계에서 AI가 막히자 연구진이 작은 힙 추적기와 시각화 도구를 만들어 정보를 주었다.
- 제안: 필요 없는 기능은 코드째 지우자는 vibe-uncoding이다. 죽은 코드와 불필요한 최적화를 AI로 찾아 공격 면적을 줄이자는 주장이다. 지울 수 있는 것을 찾는 일이 어렵다는 점도 인정한다.

## 분석

### 중심 주장은 공격 면적이 최적화 코드에서 나온다는 것이다

보고서는 이 취약점을 공유 소프트웨어 스택의 공유지의 비극으로 설명한다.
대량의 Base64를 디코딩하는 소수 응용에 이득이 되는 최적화가 모두에게 배포되고,
그 최적화를 쓰지 않는 다수가 코드의 위험을 함께 진다는 논리이다.
Java가 메모리 안전을 내세우지만 그 런타임의 일부가 C++과 어셈블리라서 메모리 손상이 남는다는 점이 출발점이다.
이는 보고서의 서술을 이 문서가 압축한 것이다.

### 영향의 크기는 조건을 얼마나 많이 채우느냐에 달렸다

위험이 크다고 평가되지만 조건이 겹친다.
x86-64의 AVX-512 VBMI 지원, 특정 JIT 단계에 올라간 코드, 응용마다 다른 경로와 힙 배치가 모두 필요하다.
HN에서 한 사용자는 Semgrep이 이 다섯 조건을 점검하는 무료 탐지 스크립트를 냈다고 전하며 조건이 매우 구체적이어도 영향 받는 호스트는 많을 것이라고 평가했다.[^ievans]
같은 스레드에서 보고서의 Oracle 버전 목록 때문에 JRE 8도 영향권이라는 정정이 나왔다.[^bikezen]
Native Image는 `-march=native`를 쓰지 않으면 영향이 없다는 보충도 있었다.[^sgammon]
조건이 이처럼 갈리므로, 위험을 판단하려면 자기 환경이 각 조건에 해당하는지 따로 확인해야 한다.

### 클라우드에서는 지금 CPU가 AVX-512가 아니라는 사실이 안심이 아니다

한 사용자는 지금 AVX-512가 없는 환경이라도 나중에 그런 머신에 올라갈 수 있으니 패치해야 하지 않느냐고 물었고,[^cjbprime]
운영 담당자는 쿠버네티스 노드 SKU를 바꾸면 같은 배포가 다른 CPU 위에서 돌 수 있다고 답했다.[^stackskipton]
관리형 쿠버네티스의 같은 노드 풀 안에서도 AVX-512 지원이 갈린다는 보고도 있었다.[^xmodem]
반대로 가상화 플랫폼이 CPU 기능을 최소공통분모로 숨길 수 있다는 지적도 나왔다.[^philipcloud]
이는 환경에 따라 다르므로 실제 인스턴스에서 직접 확인해야 한다는 뜻이다.

## 비평

### 기술적 주장은 아직 검증할 수 없다

보고서는 제품별 공격 체인을 비공개로 두었다.
시연한 제품 열한 곳의 RCE는 영상으로만 제시되고, 이 문서와 독자가 확인할 수 있는 것은 공개된 트리거와 영향 조건뿐이다.
CVSS 9.2도 Calif가 매긴 점수이다. 이 문서는 공식 CVE 기록이나 OpenJDK 공지를 열어 확인하지 못했다.
HN에서는 공개된 수정 커밋만으로 결함을 재구성해 보려는 시도도 있었으나,[^fweimer] 그 결과가 보고서와 일치하는지는 이 문서가 검증하지 못했다.

### 심각도 비교는 청중에 따라 다르게 읽힌다

HN에서 Log4Shell과의 비교가 나오자, 한 보안 전문가는 그 비교가 기준을 종말급으로 올려 두어 기업의 대응 변명이 되기 쉽다고 지적하면서 Java 핵심의 Base64 처리에서 일반화 가능한 메모리 손상을 찾은 것은 경종을 울릴 일이라고 했다.[^tptacek]
한편 한 사용자는 이것이 AVX-512 전용이라 기업 환경에서 실제로 해당하는 서버가 얼마나 되느냐고 물었고, 다른 사용자들이 AWS 등에 AMD 인스턴스가 많다고 답했다.[^hypfer]
공격이 네트워크 지연과 지터에 민감하다는 보고서의 서술을 짚은 사용자는 우연한 대량 공격 가능성은 낮고 특정 대상을 겨눈 공격자에게 의미가 있다고 요약했다.[^lucasluitjes]
Lobste.rs에서는 Java, Base64, 요청 버퍼링이 꺼진 리버스 프록시, AVX-512 호스트가 모두 겹쳐야 하니 이상한 조합이라는 의견이 첫 반응이었다.[^proctrap]
이에 대해 nginx가 버퍼링하는 쪽의 예외이고 Traefik, Envoy, HAProxy는 기본값이 꺼짐이라 쿠버네티스 환경에서는 드문 조합이 아니라는 반박이 달렸다.[^refi64]
처음 의견을 낸 사용자는 자신의 경험이 새 CPU 사양을 직접 골라야 하는 VM 환경이라고 답해, 조합이 흔한지 여부가 호스팅 방식에 따라 갈린다는 점이 드러났다.[^proctrap2]
다른 사용자는 경보가 너무 자주 울려 Log4Shell급 사건이 나왔을 때 주목받기 어려워질 것이라고 우려했다.[^marginalia]
정리하면 대량 자동 공격보다 표적 공격에 가까운 위험으로 읽을 수 있으나, 이는 댓글의 해석이지 보고서의 결론은 아니다.

### 임시 완화책을 권하는 방식이 갈렸다

HN에서 한 사용자는 AVX2를 강제하는 옵션이 AVX2가 없는 시스템에서 실패하므로 Base64 intrinsic만 끄는 옵션이 낫다고 권했다.[^msw]
혼합 아키텍처에 전역 플래그를 밀어 넣는 상황에 대해서는 논쟁이 이어졌다. 알지 못하는 호스트가 많으면 일단 일괄 적용이 현실적이라는 의견과, 환경을 추상화로 덮는 것이 오히려 문제 대응을 어렵게 한다는 의견이다.[^articulatepang]
보고서는 두 옵션을 병렬로 적었을 뿐 이 차이를 설명하지 않는다.

### AI를 쓴 발견 과정은 비용 서술이 가볍다

200달러 미만과 3시간은 발견과 첫 공격 코드에 든 값이다.
그 앞에 연구원이 휴대전화 공급업체를 대상으로 한 다른 공격 작업을 했고 JVM 감사를 위한 지식과 도구(파이프라인, 힙 추적기)를 갖추고 있었다는 서술도 있다.
HN에서 한 사용자는 이 정도 연구는 평범한 개발자에게 훈련 가능한 일이 아닐 것이라고 느낀다고 했고,[^fsnovask]
다른 사용자는 AI도 디버거나 셸처럼 배우는 기술일 뿐이라고 했다.[^colon]
이 부분은 의견 차이이고, 보고서의 비용 수치가 다른 사람에게도 재현되는지는 확인되지 않았다.

### 그 밖의 반응

HN에는 이런 지적도 있었다.
정상적인 테스트로 잡았어야 할 논리 오류라는 비판에는, 특정 명령어 집합과 입력 길이, 끝 문자, 핫 경로 조건이 겹쳐야 드러나 단순하지 않다는 반론이 달렸다.[^eyalitki]
손으로 짠 어셈블리 stub 코드가 무섭다며 같은 곳에 다른 결함이 있을 것이라는 예상도 있었다.[^cyberax]
이 예상은 근거가 제시되지 않은 추측이다.
GeekNews에서는 한 사용자가 한국에서는 2026년 11월 17일 기준으로 외부 유출 금지라고 적힌 비공개 공문이 돌았고, 한 보안 언론이 엠바고를 무시하고 올려 약 30분간 외부에 공개된 상태였다고 전했다.[^click]
이는 댓글 작성자의 증언이며 이 문서가 확인하지 못했다.
나머지 두 댓글은 HN 의견과 보고서를 다시 요약한 GN⁺ 계정의 글이라 GeekNews 이용자의 반응으로 보지 않았다.

## 인사이트

### 가져갈 것은 자기 환경이 조건에 해당하는지 먼저 확인하는 절차이다

이 취약점의 대응은 네 단계로 정리된다.
JDK 배포판과 버전을 파악하고, CPU 플래그를 확인하고, 업데이트하거나 JVM 옵션으로 막고, 노드 교체로 CPU가 바뀌는 경로를 점검한다.
HN에서 나온 지적처럼 지금 해당하지 않아도 배포 경로가 바뀔 수 있으므로 일괄 업데이트가 안전하다.
이는 이 문서의 정리이다.

### 쓰지 않는 최적화를 켜 두는 것도 위험이다

보고서가 말하는 vibe-uncoding의 요지는 필요 없는 기능을 끄거나 지우자는 것이다.
이번 사건에서 응용이 Base64 디코딩 최적화를 직접 쓰지 않아도 공격 면적에 들어갔다.
자기 시스템에서 쓰지 않는 하드웨어 가속 경로, 프로토콜, 모듈을 목록으로 만들어 두는 일은 업데이트가 늦어질 때의 완충이 된다.
보고서가 말하듯 지우는 일에는 숨은 의존성이라는 비용이 있다.

### 확인할 관찰

이 보고서의 주장을 가를 관찰은 세 가지이다.
Calif가 나중에 공개한다는 제품별 공격 체인이 실제로 보고서가 시연한 제품에서 재현되는지,
공식 공지가 밝히는 영향 버전과 보고서의 버전 목록이 일치하는지,
같은 hand-rolled 어셈블리 intrinsic에서 비슷한 결함이 더 나오는지이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^ievans]: <https://news.ycombinator.com/item?id=50538391>

[^bikezen]: <https://news.ycombinator.com/item?id=50539305>

[^sgammon]: <https://news.ycombinator.com/item?id=50541986>

[^cjbprime]: <https://news.ycombinator.com/item?id=50539263>

[^stackskipton]: <https://news.ycombinator.com/item?id=50539423>

[^xmodem]: <https://news.ycombinator.com/item?id=50539846>

[^philipcloud]: <https://news.ycombinator.com/item?id=50540131>

[^tptacek]: <https://news.ycombinator.com/item?id=50539246>

[^hypfer]: <https://news.ycombinator.com/item?id=50538735>

[^lucasluitjes]: <https://news.ycombinator.com/item?id=50539499>

[^msw]: <https://news.ycombinator.com/item?id=50538884>

[^articulatepang]: <https://news.ycombinator.com/item?id=50540522>

[^fsnovask]: <https://news.ycombinator.com/item?id=50539855>

[^colon]: <https://news.ycombinator.com/item?id=50539964>

[^eyalitki]: <https://news.ycombinator.com/item?id=50538873>

[^cyberax]: <https://news.ycombinator.com/item?id=50539656>

[^click]: <https://news.hada.io/topic?id=37370#cid70067>

[^proctrap]: <https://lobste.rs/s/g0bf9i/java4shell_write_once_rce_everywhere#c_gs5bli>

[^refi64]: <https://lobste.rs/s/g0bf9i/java4shell_write_once_rce_everywhere#c_faenu6>

[^proctrap2]: <https://lobste.rs/s/g0bf9i/java4shell_write_once_rce_everywhere#c_ziy60n>

[^marginalia]: <https://lobste.rs/s/g0bf9i/java4shell_write_once_rce_everywhere#c_s64udu>

[^fweimer]: <https://news.ycombinator.com/item?id=50539150>
