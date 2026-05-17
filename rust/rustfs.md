# RustFS

<https://github.com/rustfs/rustfs>

HN 토론: <https://news.ycombinator.com/item?id=45673917> (38점, 5개 댓글)

## 소개

RustFS는 Rust로 작성된 고성능 S3 호환 분산 객체 스토리지 시스템이다.
MinIO의 대안을 명시적으로 표방하며, “4KB 객체 페이로드 기준 MinIO 대비 2.3배 빠르다”고 주장한다.
Apache 2.0 라이선스로 배포되어 제약 없이 사용할 수 있다.
코드베이스의 98%가 Rust로 작성되어 있으며, 메모리 안전성과 성능을 핵심 설계 원칙으로 삼는다.

## 주요 기능

S3 호환 API를 기본으로 제공하며, OpenStack Swift API와 Keystone 인증도 지원한다.
버저닝(versioning), 버킷 복제(bucket replication), 이벤트 알림, Bitrot 보호가 현재 사용 가능하다.
Kubernetes Helm Chart와 웹 콘솔을 기본 제공하며, 멀티 테넌시(multi-tenancy)를 지원한다.
AI와 빅데이터 워크로드를 위한 데이터 레이크 최적화도 포함한다.

현재 테스트 단계인 기능으로는 라이프사이클 관리, 분산 모드(distributed mode),
RustFS KMS, Swift 메타데이터 작업이 있다.

## 설치

다섯 가지 설치 방법을 제공한다.

```bash
# 원클릭 설치
curl -sSL https://rustfs.com/install.sh | bash
```

Docker/Podman, 소스 컴파일, Kubernetes Helm Chart, Nix Flakes를 통한 설치도 지원한다.
기본 콘솔 인증 정보는 `rustfsadmin/rustfsadmin`이다.

## 분산 아키텍처

단일 노드와 분산 모드를 모두 지원하도록 설계되었으나,
분산 모드는 현재 테스트 단계로, 운영 환경 도입 전 직접 검증이 필요하다.
Bitrot 보호 기능은 데이터 무결성을 저장소 레벨에서 보장한다.
이레이저 코딩(erasure coding) 기반의 내결함성 설계를 따른다.

## 라이선스 및 현황

Apache 2.0 라이선스로 배포된다.
현재 활발하게 개발 중이며 일부 핵심 기능이 테스트 단계에 머물러 있어,
프로덕션 도입 전 충분한 검증이 권장된다.

## 분석

### MinIO 대안으로서의 포지셔닝

RustFS가 MinIO를 직접 겨냥하는 배경에는 MinIO의 라이선스 전략 변경이 있다.
MinIO는 2021년 AGPL로 라이선스를 변경하면서 상업적 사용에 제약이 생겼다.
RustFS의 Apache 2.0 라이선스는 이 공백을 공략하는 명확한 전략이다.
Rust로 작성된 구현이 C++ 기반 MinIO 대비 성능 이점을 주장할 수 있는 근거도 된다.

### Rust의 시스템 소프트웨어 확장

객체 스토리지는 전통적으로 C++, Go가 지배하는 영역이었다.
RustFS는 Rust가 이 영역에서도 경쟁력 있는 구현을 만들 수 있음을 보여주는 사례다.
메모리 안전성 보장이 스토리지 시스템의 데이터 무결성 요구사항과 자연스럽게 맞아떨어진다.
HN에서는 Rust로 Kubernetes를 재작성하는 프로젝트에서 이미 RustFS를 도입했다는 사례도 등장했다[^genedna].
한편 S3 호환 객체 스토리지 생태계에서 또 다른 Rust 구현인 Garage[^driftingdev]도 언급되었는데,
Rust 기반 대안이 하나가 아니라 복수로 출현하고 있다는 점은 이 흐름이 개별 프로젝트를 넘어선 것임을 보여준다.

## 비평

프로젝트의 성숙도는 아직 낮다.
분산 모드, 라이프사이클 관리 같은 핵심 기능이 테스트 단계라는 점은
운영 환경 도입을 고려하는 팀에게 실질적인 제약이다.
HN에서 pjmlp는 리포지토리 자체에 “프로덕션 환경에서 사용하지 말 것”이라는 경고가 적혀 있다는 점을 짚으며,
“그러니 도입 전 두 번 생각하라”고 직접적으로 경고했다[^pjmlp].

“MinIO 대비 2.3배 빠르다”는 벤치마크 주장은 특정 조건(4KB 객체, 단일 노드)에 국한된 것으로,
일반화에 주의가 필요하다.
another_twist는 “MinIO가 아닌 S3 자체와의 벤치마크 비교가 있어야 워크로드 계획에 유용할 것”이라며
비교 기준 선택에 의문을 제기했다[^another_twist].
바이너리 교체 시 MinIO의 쿼럼 및 잠금 로직이 어떻게 처리되는지,
성능 오버헤드는 어느 수준인지도 아직 명확하지 않다[^tooling].

프로젝트명 “RustFS”가 지나치게 범용적이어서 혼란을 준다는 지적도 있었다[^stmw].
aurintex 역시 “두 번 읽어야 무엇을 위한 프로젝트인지 이해했다”고 덧붙였다[^aurintex].

한편 Show HN 스레드에서는 일부 댓글이 홍보성 도배(astroturfing)처럼 보인다는 비판도 나왔다[^leosanchez].
igor47은 “오늘 두 번째로 보는 아스트로터핑으로 의심되는 스레드”라고 언급하며[^igor47],
커뮤니티가 프로젝트 자체가 아닌 홍보 방식에 불쾌감을 드러냈다.

가장 심각한 문제는 보안이다.
dizhn은 2025년 초 공개된 하드코딩된 인증 토큰 취약점(CVE-2025-68926, CVSS 9.8)을 언급하며
“이제 에이전트가 코드에 키를 박아넣지 않느냐”고 비꼬았다[^dizhn].
이 취약점은 해당 시점에 RustFS를 프로덕션에서 사용하던 조직에게 즉각적인 위험이 되었다.

[GeekNews 댓글](https://news.hada.io/topic?id=29532)에서 “GA 버전이 나오길 기대한다”는 반응이 있듯,
현재 시점에서 RustFS는 관심 있게 지켜볼 프로젝트이지, 바로 도입할 수 있는 프로덕션 솔루션은 아니다.
safeie가 제기한 “몇 년 뒤 MinIO처럼 클로즈소스로 전환하지 않겠느냐”는 우려[^safeie]는
Apache 2.0이라는 현재 라이선스만으로는 해소되기 어렵다.
프로젝트를 주도하는 주체와 지속 가능성에 대한 투명한 거버넌스 정보가 부족하기 때문이다.

## 인사이트

### 오픈소스 라이선스 전략이 생태계 분기를 만든다

MinIO의 AGPL 전환은 오픈소스 스토리지 생태계에 공백을 남겼고,
RustFS는 그 공백을 공략하며 등장했다.
이는 라이선스 정책이 단순한 법적 문서가 아니라,
경쟁 프로젝트의 탄생을 유도하는 생태계 분기점이 될 수 있음을 보여준다.
HashiCorp의 BSL 전환이 OpenTofu를 낳고, Elasticsearch의 라이선스 변경이 OpenSearch를 낳은 것과 같은 패턴이다.
이 패턴에서 라이선스 변경은 기존 사용자를 보호하는 동시에,
오픈소스 커뮤니티의 포크 충동을 자극하는 양면적 효과를 갖는다.
그러나 safeie의 지적처럼[^safeie], 오픈소스로 시작한 프로젝트가 다시 라이선스를 변경할 수 있다는 불신은
공백을 메우려는 신규 프로젝트에도 고스란히 이어진다.
생태계 분기의 이면에는 "이번엔 진짜 오픈소스인가"라는 피로감이 쌓이고 있다.

### Rust의 시스템 소프트웨어 시장 확대

RustFS는 Rust가 웹 서비스 백엔드를 넘어 인프라 소프트웨어 영역으로 확장하는
더 넓은 흐름의 일부다.
TiKV, Neon, Databend 등 데이터 인프라 분야에서 Rust 구현이 늘고 있다.
메모리 안전성이 데이터 무결성과 결합되는 스토리지 시스템은 Rust가 특히 강점을 발휘하는 영역이다.
성능 주장의 사실 여부와 무관하게, 이 트렌드는 Rust가 인프라 계층에서 C++/Go를 대체하는 방향으로 진행되고 있음을 보여준다.

---

[^pjmlp]: <https://news.ycombinator.com/item?id=45679353>
[^stmw]: <https://news.ycombinator.com/item?id=45684015>
[^aurintex]: <https://news.ycombinator.com/item?id=45735199>
[^driftingdev]: <https://news.ycombinator.com/item?id=45712736>
[^another_twist]: <https://news.ycombinator.com/item?id=45677943>
[^safeie]: <https://news.ycombinator.com/item?id=47439776>
[^tooling]: <https://news.ycombinator.com/item?id=47440286>
[^leosanchez]: <https://news.ycombinator.com/item?id=47443641>
[^igor47]: <https://news.ycombinator.com/item?id=47444241>
[^dizhn]: <https://news.ycombinator.com/item?id=47446846>
[^genedna]: <https://news.ycombinator.com/item?id=47442104>
