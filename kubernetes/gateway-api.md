# Kubernetes Gateway API

원문: <https://romaglushko.com/blog/k8s-gateway-api/>

GeekNews: <https://news.hada.io/topic?id=30262>

## 요약

Roman Glushko의 글은 Kubernetes Ingress에서 Gateway API로의 전환을 촉발한 NGINX Ingress Controller 지원 중단 발표(2025년 11월)를 출발점으로, 이 전환의 기술적 배경과 이행 경로를 상세히 분석한다.

Ingress API는 2015년 도입 당시 NodePort와 LoadBalancer의 한계를 극복하기 위한 것이었다.
하나의 LoadBalancer Service로 모든 인바운드 트래픽을 받아 전용 리버스 프록시로 전달하는 구조로, 단일 진입점을 통해 여러 서비스를 노출할 수 있게 했다.
그러나 시간이 지나면서 Ingress의 구조적 한계가 드러났다.

Ingress의 핵심 문제는 세 가지다.
첫째, API 범위가 좁아서 타임아웃, CORS, 속도 제한, 헤더 기반 라우팅을 지원하지 않으며 컨트롤러들이 커스텀 어노테이션으로 이를 보완했다.
둘째, 플랫폼 팀과 애플리케이션 팀의 관심사가 단일 리소스에 섞여 있다.
셋째, NGINX Ingress Controller는 컨트롤 플레인과 데이터 플레인이 동일 파드에 공존하고, 컨트롤러가 클러스터 전체 시크릿에 접근하는 구조적 취약점으로 인해 반복적인 CVE가 발생했다.
“IngressNightmare”(CVE-2025-1974)는 Ingress 수정 권한 없이도 원격 코드 실행이 가능했다.

Gateway API는 이 문제들을 구조적으로 해결한다.
GatewayClass, Gateway, Listener, Route의 계층 구조로 관심사를 분리하고, ReferenceGrant로 네임스페이스 간 참조의 신뢰 모델을 명시화한다.
Policy Attachment 메커니즘은 어노테이션 기반 확장을 대체한다.

구현체로는 Envoy Gateway, Istio, kgateway, Traefik, NGINX Gateway Fabric, Cilium Service Mesh, Kong이 소개되며, 각각의 특성과 성숙도가 다르다.
마이그레이션은 `ingress2gateway` CLI를 통한 자동 변환 또는 단계적 전환으로 진행할 수 있다.

## 분석

### CVE 반복이 설계 결함의 증상인 이유

NGINX Ingress Controller의 CVE 패턴은 단순한 버그 수정 실패가 아니다.
컨트롤 플레인과 데이터 플레인이 동일 파드에서 실행되는 구조 자체가, 데이터 플레인(NGINX)이 컨트롤 플레인의 설정 접근 권한을 공유하게 만든다.
이 구조에서 NGINX 설정 레이어의 어떤 취약점도 클러스터 수준의 권한 문제로 확대될 수 있다.

보안 아키텍처의 원칙인 최소 권한(principle of least privilege)은 각 컴포넌트가 자신의 역할에 필요한 최소한의 권한만 가져야 한다고 요구한다.
NGINX 프로세스가 클러스터의 Secret에 접근할 이유는 없지만, 구조상 그 접근이 가능했다.
Gateway API는 이 권한 분리를 설계 수준에서 강제한다 — GatewayClass와 Gateway는 플랫폼 팀이, Route는 애플리케이션 팀이 관리하며 각각 자신의 네임스페이스 범위 내에서만 동작한다.

### 양방향 신뢰 모델의 의미

Ingress에서 ExternalName Service를 통한 교차 네임스페이스 참조는 “confused deputy” 공격의 경로가 됐다.
한 네임스페이스의 리소스가 다른 네임스페이스의 Service를 통해 의도치 않은 권한을 얻는 것이다.

Gateway API의 ReferenceGrant는 이것을 명시적 양방향 동의로 해결한다.
Route가 Gateway를 `parentRefs`로 참조해야 하고, Gateway는 허용된 Route 유형과 네임스페이스를 명시적으로 선언해야 한다.
이 “핸드셰이크” 패턴은 네트워크 정책이나 RBAC에서 친숙한 패턴을 인그레스 레이어로 가져온 것이다.

### 구현체 다양성이 표준화의 이점을 상쇄하는 긴장

Gateway API가 제공하는 표준화의 핵심 이점은 구현체 간 이식성이다.
동일한 HTTPRoute 설정이 Envoy Gateway에서도, Traefik에서도 동작해야 한다.
그러나 Policy Attachment 같은 고급 기능들은 구현체별로 지원 범위가 다르다.

[GeekNews 댓글](https://news.hada.io/topic?id=30262)에서 클라우드 벤더들의 Gateway API 구현이 불완전해 기능들이 문서에만 존재한다는 경험이 보고됐다.
표준이 명세 수준에서 앞서 나가고 구현이 뒤따르는 시기에, 표준에 의존해 아키텍처를 설계한 팀이 나중에 특정 기능이 구현되지 않았음을 발견하는 위험이 있다.
Envoy Gateway와의 프로덕션 성공 사례도 함께 보고됐지만, 사용 전 대상 구현체의 실제 지원 범위를 검증하는 것이 필수적이다.

## 비평

### 마이그레이션 권고의 시기가 구현 성숙도와 어긋난다

이 글은 Gateway API로의 전환을 권고하지만, 구현체들의 성숙도는 아직 고르지 않다.
특히 클라우드 벤더 관리형 쿠버네티스(EKS, GKE, AKS)에서 Gateway API 지원이 GA(General Availability) 수준에 도달한 시기가 최근이며, 기능 범위가 다르다.

인프라 전환의 비용은 실험 환경과 프로덕션 환경에서 다르다.
마이그레이션 가이드가 기술적으로 올바르더라도, “지금 당장 마이그레이션해야 하는가”에 대한 답은 팀의 환경, 의존하는 기능, 운영 여유에 따라 다르다.
이 글이 기술적 근거는 충분히 제시하지만 “마이그레이션 시기 선택”에 대한 지침은 부족하다.

### 정책 계층의 복잡성 증가를 과소평가한다

Gateway API가 Ingress의 어노테이션 난립을 정리하는 것은 사실이지만, Policy Attachment 시스템은 새로운 복잡성을 도입한다.
SecurityPolicy, BackendTLSPolicy, BackendTrafficPolicy가 계층적으로 적용되는 규칙을 이해하고 디버깅하는 것은 단일 리소스 어노테이션보다 인지 부담이 크다.

특히 상위 Gateway에 정의된 정책과 하위 Route에 정의된 정책이 충돌하거나 예상치 못하게 결합될 때 동작을 예측하기 어려워진다.
이것은 이전 시스템의 문제를 해결하면서 다른 종류의 복잡성을 도입하는 공통 패턴이다.
운영 관점에서 이 트레이드오프를 명시적으로 제시하는 것이 마이그레이션 의사결정에 도움이 됐을 것이다.

### NGINX Ingress 지원 중단이 마이그레이션의 실질적 트리거가 되지 않을 수 있다

Chainguard가 NGINX Ingress Controller의 포크를 유지하고 있으며, 대안 Ingress 구현체들(HAProxy, Traefik)은 계속 지원된다.
“NGINX Ingress 지원 중단 → Gateway API로 전환”의 논리는 자연스럽지만, 실제로는 중간 경로들이 존재한다.

많은 운영 팀에게 현재 잘 동작하는 Ingress 설정을 Gateway API로 전환하는 것은 위험 대비 이득이 불명확하다.
특히 보안 취약점이 반복됐던 NGINX Ingress Controller를 사용하지 않던 팀에게는 긴급성이 낮다.
글이 마이그레이션의 당위성을 강조하는 방향으로 구성되어 있지만, “왜 지금 해야 하는가”에 대한 답은 팀마다 다를 수 있다.

## 인사이트

### 관심사 분리가 보안을 구조화하는 방식의 교훈

Gateway API의 설계가 보여주는 핵심 원칙은 권한 경계와 소유권 경계를 일치시키는 것이다.
플랫폼 팀이 인프라를 소유하고, 애플리케이션 팀이 라우팅 규칙을 소유하는 것이 조직 구조를 반영해야 한다는 것이다.

이 원칙은 쿠버네티스 네트워킹을 넘어 소프트웨어 아키텍처 전반에 적용된다.
권한 범위가 소유권 범위를 초과할 때 — 한 팀의 코드나 프로세스가 다른 팀의 자원에 접근할 수 있을 때 — 시스템은 예상치 못한 방식으로 상호작용한다.
NGINX Ingress의 반복적 CVE는 이 원칙을 위반한 설계의 장기적 비용을 보여준다.

### 생태계 표준화의 시장 역학

Gateway API가 공식 표준으로 채택되면서 다양한 구현체들이 등장한 것은 건강한 경쟁이지만, 구현 품질의 비동기성이라는 문제도 함께 가져온다.
표준이 빠르게 진화할 때, 다수의 구현체가 동시에 최신 명세를 완전히 지원하기 어렵다.

이것은 쿠버네티스 생태계만의 문제가 아니라 표준 기반 오픈소스 생태계의 일반적 패턴이다.
W3C 웹 표준이 브라우저들에서 비동기적으로 구현된 것처럼, Gateway API 표준과 구현체들 사이에는 항상 간격이 있을 것이다.
이 간격을 의식하면서 현재 필요한 기능이 대상 구현체에서 실제로 지원되는지를 검증하는 것이 Gateway API 채택의 실질적 전제 조건이다.
