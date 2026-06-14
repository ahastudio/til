# Mattermost: 셀프호스팅 팀 협업 플랫폼

<https://github.com/mattermost/mattermost>

HN 토론: <https://news.ycombinator.com/item?id=31858829> (264점, 127개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/3ce3bz/mattermost_open_source_self_hosted_slack>

## 소개

Mattermost는 Slack의 오픈소스 대안으로 시작한 셀프호스팅 팀 협업 플랫폼이다.
채팅, 워크플로 자동화, 음성 통화, 화면 공유, AI 통합을 지원한다.
Go 백엔드와 React 프런트엔드로 구성되며, 단일 Linux 바이너리로 실행되고 PostgreSQL을 사용한다.
매월 16일에 MIT 라이선스로 새 버전이 릴리스된다.

주요 사용 사례는 DevSecOps, 인시던트 대응, IT 서비스 데스크다.
700개 이상의 통합 및 플러그인을 제공하며, 채팅 외에도 플레이북(Playbook) 기반의
구조화된 워크플로와 인시던트 관리가 특징이다.

설치는 Docker, Ubuntu, tar, Kubernetes 등 다양한 방법을 지원한다.
클라우드 SaaS 버전도 운영 중이다.
Android, iOS, Windows, macOS, Linux 네이티브 앱을 제공한다.

오픈코어(open core) 모델이다.
기본 기능은 오픈소스(MIT)이고, 고급 보안/컴플라이언스/엔터프라이즈 기능은
유료 구독(Professional, Enterprise)으로 제공된다.

## 분석

### DevOps 워크플로 통합이 일반 채팅과의 차별점이다

Mattermost가 Slack의 단순 대체재가 아닌 이유는 DevSecOps 초점 때문이다.
플레이북은 인시던트 대응, 배포, 온콜 절차 같은 반복 워크플로를
구조화된 체크리스트와 자동화로 만든다.
Jira, GitHub, GitLab, PagerDuty 같은 DevOps 도구와의 통합이 깊다.

이것은 Slack의 범용 메시징보다 엔지니어링 조직의 운영 워크플로에 더 특화된 포지셔닝이다.
“대화가 아니라 운영을 위한 플랫폼”이라는 방향은
규제 산업(금융, 의료, 국방)에서 셀프호스팅과 결합해 강력한 가치를 만든다.

### 오픈코어 모델의 지속 가능성

오픈소스 MIT 라이선스 + 유료 엔터프라이즈 기능의 조합은
HashiCorp(Terraform), Elastic(ELK) 등이 선택한 지속 가능한 오픈소스 비즈니스 모델이다.
그러나 이 모델은 항상 긴장을 내포한다.
무료 버전이 충분히 좋으면 유료 전환이 어렵고,
유료 버전에 너무 많은 기능을 넣으면 오픈소스 커뮤니티의 신뢰를 잃는다.

Mattermost가 이 균형을 어떻게 유지하는지는 장기 지속 가능성의 핵심 변수다.
HashiCorp가 BSL 라이선스로 전환해 커뮤니티 반발을 샀던 사례는
이 모델의 취약성을 보여준다.

Lobste.rs의 초기 반응은 라이선스 전략의 변천을 보여주는 역사적 단면이다.
Mattermost 1.0 출시 당시 stip[^stip-lobsters]은
"AGPL이므로 바이너리를 그대로 사용하거나 상업 라이선스를 구입하지 않으면
수정 사항을 공개해야 한다"고 경고했다.
Hamcha[^hamcha-lobsters]는 이에 "상업 라이선스 옵션이 있다면 AGPL이 사실상 무의미해진다"고 반박했다.
이 비판은 오픈코어 모델의 핵심 모순을 정확히 짚는다.
카피레프트로 커뮤니티 기여를 유인하면서 동시에 상업 라이선스로 탈출구를 열어두면,
커뮤니티는 라이선스가 실제로는 영업 도구임을 눈치챈다.
Mattermost가 이후 MIT로 전환한 것은 이 긴장을 해소하려는 시도였다고 볼 수 있다.

## 비평

### Slack 대비 사용성 격차가 여전하다

기능 목록에서 Mattermost는 Slack에 뒤지지 않는다.
그러나 실제 사용 경험에서 Slack의 세련된 UX, 빠른 검색, 부드러운 알림 관리를
오픈소스 팀이 따라가기는 어렵다.
Mattermost를 선택한 팀의 주된 이유는 대부분 데이터 주권이나 비용이지,
Slack보다 나은 경험 때문이 아니다.
이것은 솔직한 포지셔닝을 필요로 한다.
“Slack보다 낫다”가 아니라 “데이터를 통제하면서 Slack의 70-80% 경험을 제공한다”는 것이다.

HN 커뮤니티에서도 같은 맥락의 증언이 나온다.
10명 규모 팀에서 1년간 셀프호스팅한 dx034[^dx034]는
“Slack만큼 좋지는 않지만, 자체호스팅이 필요하다면 충분히 추천할 수 있다”고 평했다.
UX 격차를 인정하되 셀프호스팅 필요성이라는 조건에서의 현실적 가치를 인정한 것이다.

반면 알림 비동기화, 모바일-데스크톱 간 미동기화 등 기본 UX 품질에 대한 불만도 있었다[^ajaimk].
스레딩 구조에 대한 구조적 비판도 제기됐다.
fiatjaf[^fiatjaf]는 “Alice의 메시지에 Bob이 답하면 그것이 스레드가 되는데,
같은 원본 메시지에 다른 주제로 분기하는 것이 불가능하다”고 지적했다.
Slack의 스레드는 채널 메시지와 병렬로 이어지지만,
Mattermost의 스레드는 단선적 구조라는 것이다.

### 가격 정책 변경이 전환 비용을 자초했다

셀프호스팅 환경에서도 유료 기능을 사용하는 팀에게 가격 인상의 충격은 실재했다.
한 사용자(temp)[^temp]는 Mattermost의 사용자당 가격 인상 이후
“셀프호스팅임에도 불구하고 Slack보다 비싸졌다”며 Zulip으로 전환했다고 밝혔다.
오픈코어 모델에서 유료 기능에 의존하는 팀은 SaaS 구독과 다름없는 비용 구조에 노출된다.

### 텔레메트리 기본 활성화는 “보안” 포지셔닝과 충돌한다

sneak[^sneak]은 “Mattermost의 오픈소스 셀프호스팅 버전은
Segment.io 텔레메트리가 기본으로 활성화되어 있으며,
잘 문서화되지 않은 환경변수로 비활성화해야 한다”고 지적했다.
보안과 데이터 주권을 핵심 가치로 내세우는 플랫폼에서
기본값이 데이터를 외부로 전송하는 구조는 모순처럼 보인다.

Mattermost 팀원 agnivade[^agnivade]는 즉시 반론했다.
텔레메트리 항목과 비활성화 방법이 공식 문서에 상세히 명시되어 있으며,
환경변수, 시스템 콘솔, `config.json`(`LogSettings.EnableDiagnostics = false`) 세 가지 방법으로
비활성화가 가능하다고 설명했다.
“잘 문서화되지 않았다”는 비판은 사실과 다르다는 것이다.

### E2EE 부재는 관리자 신뢰 문제다

akvadrako[^akvadrako]는 “관리자(자신)가 메시지를 읽을 수 있는 구조라면
친구 그룹을 위해 서버를 운영하기 어렵다”며 E2EE 미지원을 지적했다.
서드파티 플러그인이 존재하지만, 핵심 보안 기능이 공식 제품에 없다는 것은
운영 마찰과 사용자 지원 부담을 가중시킨다.

Avamander[^avamander]는 한걸음 더 나아가 Element/Matrix를 대안으로 제시했다.
“E2EE와 federation까지 제공하는 Matrix 생태계가 낫다”는 주장이다.
Mattermost의 포지셔닝이 보안 중심임을 감안하면,
E2EE의 플러그인 의존은 잠재적 사용자층을 좁히는 요인이다.

## 인사이트

### 엔터프라이즈 채팅의 규제 시장은 독립적 수요를 가진다

EU GDPR, 미국 FedRAMP, 의료 HIPAA, 금융 FINRA 같은 규제 환경은
클라우드 SaaS 채팅 도구의 사용을 제한하거나 금지한다.
이 규제 시장은 “Slack 대안”이 아니라 “셀프호스팅 필수 환경의 유일한 옵션”으로
Mattermost를 선택한다.
독일 정부, 미국 국방부 관련 기관들이 Mattermost를 사용하는 것은 이 맥락이다.

이 시장은 UX 경쟁이 아닌 보안 인증, 감사 로그, 온프레미스 배포 성숙도 경쟁이다.
Mattermost가 이 포지셔닝에 집중하는 것은 올바른 전략이다.
범용 채팅 시장에서 Slack과 경쟁하려다 특화 시장을 잃는 것보다
규제 시장의 1위 오픈소스 솔루션이 되는 것이 더 명확한 가치다.

### 셀프호스팅의 실질적 비용: 메시지 이동 불가

karaterobot[^karaterobot]은 4년간 DigitalOcean 최저가 드롭릿에서 Mattermost를 운영한 경험을 공유했다.
Slack의 1만 메시지 제한에서 벗어나기 위해 이전했지만,
무료 버전에서는 검색 품질이 낮고 비공개 대화 내보내기가 불가능하다는 점을 지적했다.
"유료 결제를 안 하니 이해한다"면서도, "메시지 내보내기 불가는 사실상의 Lock-in"이라고 평했다.

오픈소스 셀프호스팅을 선택한 이유가 데이터 주권임에도,
자신의 데이터를 완전히 이동할 수 없는 구조는 아이러니다.
규제 시장에서의 신뢰 기반은 보안 인증만이 아니라
데이터 이동성 보장에서도 나온다는 점을 이 경험은 보여준다.

---

[^dx034]: <https://news.ycombinator.com/item?id=31859545>
[^ajaimk]: <https://news.ycombinator.com/item?id=31860851>
[^fiatjaf]: <https://news.ycombinator.com/item?id=31860293>
[^temp]: <https://news.ycombinator.com/item?id=31859509>
[^sneak]: <https://news.ycombinator.com/item?id=31862303>
[^agnivade]: <https://news.ycombinator.com/item?id=31863852>
[^akvadrako]: <https://news.ycombinator.com/item?id=31859713>
[^avamander]: <https://news.ycombinator.com/item?id=31860590>
[^karaterobot]: <https://news.ycombinator.com/item?id=31862802>
[^stip-lobsters]: <https://lobste.rs/s/3ce3bz/mattermost_open_source_self_hosted_slack#gfzfbm>
[^hamcha-lobsters]: <https://lobste.rs/s/3ce3bz/mattermost_open_source_self_hosted_slack#4keqrq>
