# GlitchTip: Sentry SDK를 그대로 쓰는 오픈소스 오류 추적

<https://glitchtip.com/>

<https://gitlab.com/glitchtip/glitchtip>

Show HN: [Show HN: GlitchTip. Open source error tracking, compatible with Sentry SDKs](https://news.ycombinator.com/item?id=23859519) (8점, 3개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=36008564> (107점, 18개 댓글)

GN 토론: <https://news.hada.io/topic?id=9297>

## 소개

GlitchTip은 애플리케이션의 오류를 모아 정리하고 원하는 곳으로 알려 주는 오류
추적 서비스다.
만든 곳은 Burke Software and Consulting이라는 작은 개발 컨설팅 팀이며,
같은 팀이 Passit도 만들었다고 홈페이지는 밝힌다.
홈페이지는 오류 추적, 성능 모니터링, 가동 시간(uptime) 모니터링,
로그를 한곳에서 제공한다고 소개한다.

핵심 주장은 두 가지다.
하나는 [Sentry](./sentry.md)의 클라이언트 SDK와 호환되므로 앱 쪽 코드를 바꾸지
않고 받을 곳만 바꿀 수 있다는 것이다.
다른 하나는 오픈소스라서 직접 서버에 올려 쓰거나 회사가 호스팅하는 서비스를 쓸
수 있고,
그 어느 쪽도 Sentry보다 운영이 쉽고 싸다는 것이다.
이 주장들은 만든 회사의 말이다.
호환의 범위와 운영 난이도는 이 문서가 직접 시험하지 못했다.

## 주요 기능

홈페이지가 내세우는 기능은 네 가지다.

- 오류 추적: 예외, 로그 메시지, 콘텐츠 보안 정책(Content Security Policy) 위반 등을 한곳에 모아 분류하고 해결한다. Sentry의 오픈소스 SDK로 오류 데이터를 받는다.
- 성능 모니터링.
- 가동 시간 모니터링.
- 로그.

기능의 깊이는 홈페이지만으로는 알 수 없다.
릴리스 노트를 읽으면 최근 흐름이 보인다.

2026년 3월의 6.1은 로그, 콜드 스토리지, MCP, minidump를 더했다.[^v61]
오래된 이벤트를 지우는 대신 DuckDB가 압축한 Parquet 파일로 넘겨 보관하는
방식이고,
기본은 꺼져 있으며 별도 서비스나 컨테이너가 필요 없다고 한다.[^v61]
DuckDB를 켜면 RAM이 기본 128MB 더 필요하다고 적었다.[^v61]
스팬을 저장하는 성능 모니터링은 DuckDB를 켜야 한다.[^v61]

2026년 6월의 6.2는 OpenTelemetry 로그를 `/v1/logs`로 직접 받는다.
sentry-sdk 없이도 로그가 들어가며, 스팬과 트레이스(예외 포함)는 곧 지원한다고
예고했다.[^v62]
이메일 설정이 선택 사항이 되었고 이슈를 사용자에게 지정하는 API가 생겼다.[^v62]
Python 비동기 ORM을 도입해 이벤트 하나당 CPU 사용이 15~20% 줄었다고 하는데,
이는 운영 중 인스턴스에서 두 카나리 파드를 비교한 회사의 측정이다.[^v62]

## 요금과 무료 범위

호스팅 요금은 이벤트 수로 갈린다.

| 단계          | 월 요금 | 월 이벤트 | 보존 | 그 밖의 내용                                  |
| ------------- | ------- | --------- | ---- | --------------------------------------------- |
| Hobby & Trial | 무료    | 1,000개   | 30일 | 오류 추적. 업그레이드 전 시험용               |
| Small         | 15달러  | 10만 개   | 90일 | 한도 초과분 구매 가능, 무제한 프로젝트와 팀원 |
| Medium        | 50달러  | 50만 개   | 90일 | 우선 이메일과 라이브 챗 지원                  |
| Large         | 250달러 | 300만 개  | 90일 | 개발 지원, 요청 시 BAA                        |

무료는 한 달 1,000건이라 운영 서비스에는 거의 시험용이다.
무료로 넉넉히 쓰고 싶다면 이 호스팅 단계는 맞지 않고, 직접 호스팅을 봐야 한다.

## 자체 호스팅

설치 문서에 따르면 Docker로 돌리며 Docker Compose를 권장하고,
Kubernetes용 Helm 차트가 있다.[^install]
PikaPods, Elestio, Nodion, Railway, RepoCloud 같은 호스팅에서도 올릴 수 있다고
한다.[^install]
PostgreSQL 14 이상이 필요하고 Valkey(또는 Redis) 7 이상은 선택이다.[^install]
권장 사양은 RAM 512MB이고 올인원 구성의 최소는 256MB다.
조심해서 설정하면 128MB에 스왑으로도 돈다고 한다.[^install]
디스크는 사용량에 따라 다르며 월 100만 이벤트 인스턴스는 대략 30GB가 필요할 수
있다고 적었다.[^install]
앞단에는 요청 버퍼링과 chunked 전송을 다루는 nginx 같은 프록시를 두라고
한다.[^install]

소프트웨어는 MIT 라이선스의 오픈소스이고,
회사는 영리 목적의 사용자에게 지원 라이선스를 구입해 달라고 요청한다.[^v62]
자체 호스팅으로 쓰면 소프트웨어 값은 들지 않지만 서버와 운영 노력은 자신이 낸다.
호스팅 서비스에 맡기는 쪽과 직접 올리는 쪽 사이에서 고를 때 이 노력을
따져야 한다.

## 저장소 구성과 기여 규칙

GitLab의 `glitchtip/glitchtip` 저장소는 코드 저장소가 아니라 메타 저장소다.
README는 이 저장소가 이슈 추적, 위키, 배포 정보를 위한 곳이라고 밝히고,
실제 코드는 Django 백엔드와 Angular 프런트엔드 저장소로 나눠 두었다.
저장소 루트에는 Dockerfile과 `heroku.yml`,
`app-platform.yaml` 같은 배포용 파일이 있다.
GitLab API가 보고하는 언어 비율은 백엔드가 Python 94%,
프런트엔드가 TypeScript 71%이다.[^backend-repo][^frontend-repo]
라이선스는 MIT이고 저작권 표기는 David Burke 2023이다.

기여 안내는 두 가지가 눈에 띈다.
첫째, 실제로 만들 생각이 없는 기능 요청은 올리지 말라고 한다.
서드파티 연동 같은 틈새 기능은 직접 만들거나 비용을 댈 사람만 요청하라는
것이다.[^contributing]
둘째, 릴리스 날짜와 예상 시점을 묻지 말라고 한다.
작은 팀이 준비되면 내보내고, `master`에 합쳐진 수정은 다음 릴리스에
들어간다.[^contributing]
급하면 `master`에서 직접 빌드하거나 자동 빌드 이미지를 쓸 수 있지만,
이 이미지는 사람이 검토하지 않으므로 운영에는 직접 시험한 뒤에만 쓰라고
한다.[^contributing]
일정에 대한 약속은 유료 지원 고객에게만 한다.[^contributing]
자체 호스팅으로 운영할 때는 수정이 언제 나올지 알 수 없다는 뜻이므로 장애 대응
계획에 넣어 둘 만하다.

AI 사용 정책도 따로 있다.
이슈와 병합 요청은 사람이 직접 쓴 요약으로 시작해야 하고,
AI를 썼다면 도구와 사용 정도를 밝혀야 한다.[^ai-policy]
AI로 만든 코드는 사람이 직접 써 보고 검증한 증거를 붙여야 하며,
AI가 만든 이미지와 영상 같은 매체는 허용하지 않는다.[^ai-policy]
권한이 Developer 이상인 조직 구성원과 메인테이너는 이 규칙에서
제외된다.[^ai-policy]
같은 문서는 GlitchTip 자체가 AI의 도움을 많이 받아 만들어지고
프로젝트가 AI를 도구로 환영한다고도 적었다.[^ai-policy]
이 규칙들은 프로젝트가 스스로 쓴 정책이고, 실제 집행이 어떤지는 확인하지 못했다.

## 데이터와 약관

2026년 10월에 약관, 개인정보 처리방침, 데이터 처리 계약(DPA)을 쉬운 말로 다시
썼다.[^terms]
회사는 데이터를 팔지 않고 AI 모델 학습에 쓰지 않는다고 적었고,
DPA는 이제 무료 요금제에도 적용된다.[^terms]
이벤트는 기본 90일 뒤 삭제하며, 삭제한 데이터는 35일 안에 백업에서도
사라진다.[^terms]
기존 계정은 2026년 11월 21일에 새 약관으로 넘어간다.[^terms]
같은 글에서 회사는 지원 이메일과 채팅을 맡은 Chatwoot를 하위
처리자(subprocessor)로 나열하지 않았던 사실을 스스로 밝혔다.[^terms]

## Sentry 대신 쓸 때 따져볼 것

비용 때문에 Sentry를 바꾸려는 경우의 판단 기준은 이렇다.

- 호환은 SDK 수신 쪽에 있다. 오류와 로그를 받는 것은 가능하다고 하지만, Sentry의 소스맵 처리, 이슈 소유자 규칙, 릴리스 추적 같은 세부는 이 문서가 확인하지 못했다.
- 무료로는 호스팅 서비스가 월 1,000건이라 Sentry의 무료 오류 5천 건보다 작다.[^sentry-pricing] 그 대신 직접 호스팅하면 건수 한도가 없다.
- 호스팅 첫 유료 단계는 월 15달러에 10만 건이다. Statsig의 Pro 월 150달러와 견주면 오류 추적만 필요한 경우 훨씬 싸다. 비교는 [Statsig 문서](../feature-flag/statsig.md)의 비용 절에 있다.
- 트레이스는 아직 오픈텔레메트리로 받는다고 약속만 있고(스팬과 트레이스는 곧 지원 예정), 성능 모니터링은 DuckDB를 켜야 한다.[^v62][^v61]
- 권한과 역할 체계는 Sentry API 호환을 위해 만든 것이어서 다시 짜겠다고 회사가 밝혔다. 그 과정에서 주요 버전이 올라가고 깨지는 변경이 생길 수 있다.[^v62]

HN 사용자들의 경험은 2019년부터 2023년 사이의 것이어서 지금 버전과 다를 수 있다.
hardwaresofton은 GlitchTip이 잘 동작하고 Sentry의 보고 생태계를 그대로 쓸 수
있어 좋지만,
Django 앱이 단일 바이너리와 데이터베이스만 있는 소프트웨어보다는 배포에 손이 더
간다고 적었다.[^hardwaresofton]
gurchik는 GlitchTip이 백엔드, 워커, Redis, PostgreSQL 네 구성 요소면 되는데,
자체 호스팅 Sentry는 ClickHouse, ZooKeeper,
Kafka를 포함해 열두 개가 넘는다고 비교했다.[^gurchik]
tapoxi는 쿠버네티스에서 자체 호스팅 Sentry를 돌리며 Kafka와 ClickHouse를 돌보는
것이 악몽이었고,
유료 지원도 받을 수 없어 클라우드로 밀어붙이는 구조라고 말했다.[^tapoxi]
Spivak은 1년 가까이 쓰며 자체 호스팅이 쉽고 Sentry 라이브러리를 그대로 쓰므로
믿을 만하다고 했다.[^spivak]
이 네 댓글은 모두 개인의 사용 보고이고 규모나 이벤트 양은 밝히지 않았다.

라이선스는 댓글에서 갈렸다.
the_black_hand가 Sentry는 지금도 오픈소스이고 자체 호스팅할 수 있지
않으냐고 묻자,
Brendinooo는 Sentry 사이트의 Business Source License 안내를 인용해
OSI 기준의 오픈소스는 아니지만 상업 버전을 제공하지 않는 한 자유롭다고
답했다.[^brendinooo]
spapas82는 Sentry를 오래 자체 호스팅했지만 도커 이행과 의존성 증가,
비자유 라이선스 전환이 부담이어서
Sentry 프로토콜을 구현한 이 프로젝트가 낫다고 적었다.[^spapas82]
두 댓글이 말하는 Sentry의 현재 라이선스 조건은 이 문서가 확인하지 못했다.
비슷한 목적의 다른 선택지로 vanschelven은 자신이 만든 Bugsink를
소개했다.[^vanschelven]

광고 차단기 문제는 어떤 오류 수집기든 마찬가지다.
ledgerdev는 uBlock이 Sentry의 브라우저 오류 보고를 막고,
릴레이 컨테이너와 하위 경로로도 막혔다고 적었다.[^ledgerdev]
knubie는 Sentry의 tunnel 옵션과 자체 호스팅한 JavaScript SDK를 권했다.[^knubie]
이는 Sentry SDK에서 나온 해법이어서 같은 SDK를 쓰는 GlitchTip에도 해당하는지는
확인하지 못했다.

도입 전에 직접 확인할 것은 현재 쓰는 SDK 버전이 GlitchTip에서 정상 수신되는지,
소스맵과 릴리스가 필요한 기능이 있는지,
자체 호스팅이라면 월 이벤트 규모에서 디스크와 PostgreSQL이 버티는지다.
홈페이지의 어떤 말도 이 확인을 대신하지 않는다.

---

[^v61]: GlitchTip, [GlitchTip 6.1 released](https://glitchtip.com/blog/2026-03-23-glitchtip-6-1-released), 2026-03-23

[^v62]: GlitchTip, [GlitchTip 6.2 released](https://glitchtip.com/blog/2026-06-22-glitchtip-6-2-released), 2026-06-22

[^install]: GlitchTip, [GlitchTip Installation Guide](https://glitchtip.com/documentation/install), 2026-11-07

[^terms]: GlitchTip, [Our new Terms: your data is yours, in writing](https://glitchtip.com/blog/2026-10-21-marketing-site-tos), 2026-10-21

[^sentry-pricing]: Sentry, [Pricing: Free Developer Plan, Pay as You Grow | Sentry](https://sentry.io/pricing/), 2026-11-07

[^backend-repo]: GlitchTip, [glitchtip-backend](https://gitlab.com/glitchtip/glitchtip-backend), 2026-11-07

[^frontend-repo]: GlitchTip, [glitchtip-frontend](https://gitlab.com/glitchtip/glitchtip-frontend), 2026-11-07

[^contributing]: GlitchTip, [How to contribute](https://gitlab.com/glitchtip/glitchtip/-/blob/master/CONTRIBUTING.md), 2026-11-07

[^ai-policy]: GlitchTip, [AI Usage Policy](https://gitlab.com/glitchtip/glitchtip/-/blob/master/AI_POLICY.md), 2026-11-07

[^hardwaresofton]: <https://news.ycombinator.com/item?id=36008965>

[^gurchik]: <https://news.ycombinator.com/item?id=36009062>

[^tapoxi]: <https://news.ycombinator.com/item?id=36009150>

[^spivak]: <https://news.ycombinator.com/item?id=36009320>

[^brendinooo]: <https://news.ycombinator.com/item?id=36009328>

[^spapas82]: <https://news.ycombinator.com/item?id=30104803>

[^vanschelven]: <https://news.ycombinator.com/item?id=42005321>

[^ledgerdev]: <https://news.ycombinator.com/item?id=36012562>

[^knubie]: <https://news.ycombinator.com/item?id=36013136>
