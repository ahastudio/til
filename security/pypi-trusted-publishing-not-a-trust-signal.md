# PyPI Trusted Publishing을 패키지 신뢰 신호로 보면 안 된다

원문: <https://enosuchblog.yossarian.net/2026/07/07/You-shouldnt-trust-trusted-publishing>

Lobsters 토론: <https://lobste.rs/s/8d9pgd/you_shouldn_t_trust_trusted_publishing>

## 요약

저자는 PyPI의 "Trusted Publishing"이 패키지 신뢰성을 보여주는
신호가 아니라고 명확히 한다.
이 기능은 CI/CD 시스템과 패키지 저장소 사이에 OIDC 연합
(federation)을 이용한 기계 대 기계 인증을 구축할 뿐이다.
장기 유효 API 토큰에서 오는 위험은 줄여 주지만, 업로드된
패키지의 안전성이나 품질, 보안까지 검증하지는 않는다.

핵심 요지는 다음과 같다.
Trusted Publishing은 장기 토큰 대신 짧게 유효한 범위 제한
자격 증명을 사용한다.
이 기능은 인증(authentication) 문제를 다룰 뿐, 패키지 내용의
무결성이나 안전성 문제를 다루지 않는다.
PyPI는 의도적으로 Trusted Publishing 상태를 초록색 체크마크로
표시하지 않는데, 이는 사용자가 이를 신뢰 신호로 오해하는 것을
막기 위해서다.
Trusted Publishing을 사용하더라도 악성 코드를 업로드하는 것은
여전히 가능하다.
이 기능은 선택 사항이며 강제할 수 없다.

## 분석

이 글의 논지는 "인증(authentication)"과 "신뢰(trust)"를
혼동하지 말라는 것으로 요약된다.
Trusted Publishing이 검증하는 것은 "이 업로드가 정말 그
CI 파이프라인에서 왔는가"이지, "이 코드가 안전한가"가 아니다.
공급망 보안 논의에서 흔히 이 두 층위가 뒤섞이는데, 저자는
PyPI가 초록색 체크마크를 의도적으로 넣지 않았다는 사실을
근거로 제시하며 이 구분을 명확히 한다.

Lobsters 스레드는 이 구분을 넘어 탈중앙화 논쟁으로 번졌다.
justJanne는 Trusted Publishing 같은 기능이 GitHub Actions
같은 중앙화된 포지(forge)에 프로젝트를 묶어 두는 효과를
낸다고 우려했다.[^justJanne1]
반면 글쓴이 yossarian(원문 저자 본인)은 대안적인 인증
방식이 여전히 남아 있는 한 이것이 락인은 아니라고
반박했다.[^yossarian1]

## 비평

Trusted Publishing이 "허용 목록에 오른(allowlisted)" 서비스,
즉 GitHub Actions 같은 주요 CI 제공자에서만 지원된다는 점은
셀프 호스팅 인프라를 쓰는 개발자에게 실질적인 장벽이다.
justJanne는 일부 레지스트리가 API 토큰을 아예 폐기하면서도
허용 목록에 오른 서비스에서만 Trusted Publishing을 지원한다고
지적했다.[^justJanne2]
matklad는 자기 집 서버에서 CI/CD를 돌리는 경우 Trusted
Publishing을 어떻게 설정해야 하는지 직접 물었지만, yossarian은
그런 셀프 호스팅 환경에는 애초에 API 토큰이 더 적합하다고
답했다.[^yossarian2]
즉 이 기능은 대형 CI 제공자를 쓰는 다수 개발자에게는 실질적인
개선이지만, 소수의 셀프 호스팅 사용자에게는 여전히 사각지대로
남는다.

ubernostrum은 이 사각지대가 왜 발생하는지 설명한다.
Trusted Publishing이 줄이려는 위험은 "제3자 CI 제공자에게
얼마나 많은 자격 증명을 노출하는가"인데, 셀프 호스팅
환경에서는 애초에 이 문제 자체가 성립하지 않는다는
것이다.[^ubernostrum]
finn은 한 걸음 더 나아가 Forgejo 같은 셀프 호스팅 소프트웨어가
PKI와 OIDC를 손쉽게 관리할 수 있고, 오래 유지되는 정적 토큰보다
짧게 유효한 JWT만 노출하는 편이 오히려 더 안전하다고
주장했다.[^finn]
이는 저장소 쪽의 기술적 장벽보다 PyPI 쪽의 운영·정책적 결정이
셀프 호스팅 지원을 막고 있다는 뜻으로 읽힌다.

## 인사이트

이 글과 스레드가 함께 던지는 메시지는, 보안 기능의 이름이
곧 그 기능이 보장하는 범위는 아니라는 것이다.
"Trusted Publishing"이라는 이름은 그 자체로 신뢰를 내포하는
것처럼 들리지만, 실제로 보장하는 것은 업로드 경로의 인증뿐이다.
misty가 언급했듯 PyPI가 npm처럼 OIDC를 공격적으로 밀어붙이지
않고 균형 잡힌 태도를 취한 것[^misty]은, 이 기능의 한계를
설계 단계에서부터 인지하고 있었다는 방증일 수 있다.
결국 패키지 사용자 입장에서 필요한 신호는 "누가 업로드했는가"를
넘어 "무엇이 업로드됐는가"에 대한 별도의 검증 체계이며,
Trusted Publishing은 그 전체 그림의 절반만을 담당한다.

---

[^justJanne1]: <https://lobste.rs/s/8d9pgd/you_shouldn_t_trust_trusted_publishing#c_dyuowi>
[^yossarian1]: <https://lobste.rs/s/8d9pgd/you_shouldn_t_trust_trusted_publishing#c_cp9tto>
[^justJanne2]: <https://lobste.rs/s/8d9pgd/you_shouldn_t_trust_trusted_publishing#c_btus66>
[^yossarian2]: <https://lobste.rs/s/8d9pgd/you_shouldn_t_trust_trusted_publishing#c_plpbzy>
[^ubernostrum]: <https://lobste.rs/s/8d9pgd/you_shouldn_t_trust_trusted_publishing#c_vfzsgu>
[^finn]: <https://lobste.rs/s/8d9pgd/you_shouldn_t_trust_trusted_publishing#c_8hwzgn>
[^misty]: <https://lobste.rs/s/8d9pgd/you_shouldn_t_trust_trusted_publishing#c_s2dc5s>
