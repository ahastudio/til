# OpenNext: Next.js 어댑터 프로젝트

<https://opennext.js.org/>

<https://github.com/opennextjs>

<https://github.com/opennextjs/opennextjs-aws>

HN 토론: <https://news.ycombinator.com/item?id=42198611> (95점, 57개 댓글)

## 소개

OpenNext는 Next.js를 Vercel 이외의 어떤 플랫폼에도 배포할 수 있게 하려는 오픈소스 이니셔티브이다. 홈페이지는 2023년에 시작되었고 SST 공동체의 AWS Lambda용 서버리스 어댑터에서 출발해 Cloudflare와 Netlify가 후원하는 다중 플랫폼 노력으로 커졌다고 설명한다.
이 문서는 홈페이지 전문과 첫 문서 페이지인 AWS 개요, AWS 어댑터 저장소(`opennextjs-aws`)와 Cloudflare 어댑터 저장소의 GitHub API 수치, HN 글과 댓글을 읽었다. 직접 배포해 보지 않았고 Cloudflare와 Netlify 문서, 시작하기 페이지, 소식 글, 소스 코드는 열지 못했다.
설명은 모두 프로젝트의 주장이다.

홈페이지가 소개하는 내용은 다음과 같다.

- 어댑터: AWS는 SST 공동체, Cloudflare는 Cloudflare 팀, Netlify는 Netlify 팀이 관리한다. 홈페이지에는 설치 명령이나 기능 목록, 지원 Next.js 버전 목록이 없다.
- 표준화: Vercel과 협력해 Cloudflare, Netlify, Google, AWS Amplify 등과 배포 어댑터 워킹 그룹을 만들었고, 그 결과 표준 Deployment Adapters API가 Next.js 16.2에서 안정되었다고 한다. 그래서 플랫폼이 빌드 출력을 역공학할 필요가 없고, AWS와 Cloudflare와 Netlify의 새 어댑터가 이 공식 API 위에서 개발 중이라고 적는다.
- 공동체: 2026년 3월부터 OpenNext 구성원이 Next.js 생태계 워킹 그룹에 참여한다. 관리 주체 표기는 OpenNext 공동체이고 개인 관리자는 홈페이지에 없다.

AWS 개요 페이지는 다음을 말한다.

- 버전: 문서가 OpenNext V3를 다룬다. V2 문서와 이전 안내가 따로 있다.
- 방식: Next.js 빌드 출력을 환경에 맞게 변환한다. AWS Lambda, Cloudflare, 일반 Node.js 서버를 기본 지원한다.
- 분리 배포: 출력을 나눠 Lambda, Cloudflare Workers, Amazon ECS에 나눠 올린다. 예로 API는 ECS, 일부 라우트는 Workers, SSR은 다른 ECS 클러스터, ISR과 정적은 Lambda를 든다.
- 지원 범위: Next.js 15와 16의 모든 기능을 지원하는 것을 목표로 한다. App Router와 Pages Router, API 라우트, 동적 라우트, SSG, SSR, ISR, 미들웨어, 이미지 최적화, NextAuth.js, Lambda@Edge, 콜드 스타트 완화(워머), `after`, `'use cache'`를 든다. 일부는 진행 중이다.
- 사용 사례: NHS England, Udacity, Gymshark UK, SST, Cloudflare를 프로덕션 사용자로 든다.
- Windows: 완전히 지원하지 않으며 WSL, Linux VM, Linux나 macOS의 CI를 권한다.

GitHub API로 읽은 시점(2026년 11월 19일)의 수치는 다음과 같다. 모두 저장소 홈페이지 필드가 `opennext.js.org` 계열이다.

| 저장소                  | 별    | 포크 | 열린 이슈와 PR | 최신 릴리스                                        | 마지막 푸시      |
| ----------------------- | ----- | ---- | -------------- | -------------------------------------------------- | ---------------- |
| `opennextjs-aws`        | 5,051 | 249  | 81             | v4.1.16(2026년 11월 12일)                          | 2026년 11월 18일 |
| `opennextjs-cloudflare` | 1,918 | 163  | 111            | `@opennextjs/cloudflare@1.20.17`(2026년 11월 12일) | 2026년 11월 18일 |

두 저장소의 라이선스는 MIT이고 언어는 TypeScript이다. AWS 저장소는 2022년 11월 29일, Cloudflare 저장소는 2024년 9월 12일에 생겼다.

## 분석

### 중심 주장은 Vercel 밖의 Next.js 배포를 공동체 표준으로 만든다는 것이다

프로젝트는 단일 회사의 도구에서 여러 플랫폼 회사가 관리하는 어댑터 묶음으로 바뀌었다고 스스로 말한다.
핵심 전환은 빌드 출력을 따라가는 방식에서 Next.js가 제공하는 공식 어댑터 API 위에 짓는 방식으로 가는 것이다.
이는 홈페이지의 서술을 이 문서가 정리한 것이다.

### Vercel이 하는 일을 자기 인프라에서 한다

HN에서 한 사용자는 Open Next가 Vercel처럼 API 라우트를 서버리스 함수로 컴파일하고 여러 형태의 서버 렌더링을 지원하는 것을 AWS나 자기 인프라나 Cloudflare Worker에서 하게 해 준다고 설명했다.[^grrowl]
다른 사용자는 Next.js를 Vercel이 아닌 곳에 배포하기 어렵고 이것이 Vercel 종속과 평판의 이유라고 말했다.[^taikon]
이는 사용자의 설명이며 프로젝트의 주장과 같은 방향이다.

### 패키징만 하고 인프라는 따로 둔다

HN의 한 사용자는 OpenNext가 빌드 산출물의 패키징만 맡고 인프라는 이를 배포하는 프로젝트가 정의한다고 설명했다. 일부는 인프라를 명시하는 Terraform 프로젝트이다.[^greyskull-infra]
이 분리가 유연성의 근원이면서 처음 보는 사람이 무엇이 배포되는지 알기 어려운 이유이다. 이는 이 문서의 관찰이다.

### 같은 문제를 푸는 다른 접근과 놓여 있다

Cloudflare는 OpenNext의 후원자이면서 같은 문제를 Vite 위의 재구현으로 푸는 Vinext도 만든다.
OpenNext 홈페이지는 Vinext를 언급하지 않는다. Vinext 쪽 서술은 `vinext/vinext.md`와 `vinext/vinext-1-0.md`에 따로 정리했다. 이는 이 문서의 관찰이다.

## 비평

### 상류가 바뀔 때 따라가야 한다

HN에서 Docker로 ECS에 올린 Next.js와 무엇이 다르고 Next.js 갱신을 따라가는지 묻는 질문에, 답한 사용자는 Lambda 같은 서버리스에 맞는 패키징이 장점이고 상류 변경에 깨질 수 있어 따라잡아야 하는 것이 가장 큰 단점이라고 했다.[^syndicatedjelly][^greyskull-lag]
이후 공식 어댑터 API가 안정되었다는 홈페이지의 서술은 이 문제를 줄이려는 방향이다. 이 문서는 그 효과를 확인하지 못했다.
홈페이지는 새 어댑터가 개발 중이라고만 쓰고 현재 어느 어댑터가 새 API를 쓰는지, 기존 어댑터와 기능 차이가 무엇인지 적지 않는다.

### Vercel 종속을 해결할 일인가의 논쟁이 있다

한 사용자는 Next.js가 Vercel에서 호스팅되도록 만들어지고 자체 호스팅은 부차적이어서 OpenNext가 존재할 필요가 없어야 한다고 했다.[^slashnode]
반대로 다른 사용자는 Next.js를 자체 호스팅해 돌리는데 콜드 스타트도 없고 Vercel보다 낫다고 했다.[^switz]
한 사용자는 자체 호스팅 자체가 나쁜 선택이라는 경험을 말했다.[^0xblinq]
어느 쪽이 일반적인지는 읽은 범위에서 알 수 없다.

### IaC 선택의 제약이 있다

한 사용자는 OpenNext가 호스팅 계층에는 중립이지만 IaC 도구에는 SST를 전제하는 듯하고 자신은 CDK를 쓴다고 했다.[^bilalq]
문서가 다른 도구 위의 프로젝트를 링크한다고 했지만 이 문서는 읽지 못했다.

### 관리 부담이 소수에게 있다

AWS 페이지는 SST 공동체가 관리하며 관리자 두 명을 이름으로 적고 최신 상태와 기능 완성을 도와 달라고 요청한다.
핵심 어댑터의 유지 보수가 소수 인력에 기대는 구조라는 점이 읽힌다. 이는 이 문서의 해석이다.

### 외부 반응

HN 헤더의 글은 2024년 11월 AWS 어댑터 저장소가 Show HN으로 올라온 것이고 한 사용자는 이 프로젝트가 오래되었고 제출자와 무관해 보인다고 지적했다.[^hysan]
같은 시기 2024년 9월에는 Cloudflare 합류 소식(4점, 댓글 없음)과 홈페이지 글(1점, 댓글 2개)이 올라왔으나 논의는 거의 없었다.
Lobste.rs에는 `opennext.js.org` 도메인의 글이 없었고 `opennext` 검색 결과 5건은 Vercel 밖에서 Next.js를 쓰기 어렵다는 다른 글들이었다.
GeekNews에서는 `OpenNext`로 검색해 이 프로젝트의 토픽이 없었다(대조 쿼리는 정상이었다).

## 인사이트

### 가져갈 것은 어댑터 API를 공식 표준으로 만드는 경로이다

외부 프로젝트가 빌드 출력을 역공학하는 부담을 줄이려면 상류가 안정된 확장 지점을 제공해야 한다.
워킹 그룹을 만들어 그 지점을 표준화한 과정은 다른 플랫폼 종속 문제에도 참고가 된다. 이는 이 문서의 적용이다.

### 배포 산출물과 인프라를 나누는 구조의 비용을 안다

패키징 도구와 인프라 정의를 분리하면 도구가 다양한 환경에 맞는 대신 처음 쓰는 사람의 진입 비용이 커진다.
도입 전에 어떤 배포 프로젝트(SST, Terraform, CDK)와 짝지을지 정하는 순서가 필요하다.

### 자체 호스팅의 대안을 같은 조건으로 비교한다

단순한 Node 서버나 Docker로 충분한 앱도 있다는 사용자 증언이 있다.
서버리스의 이점(확장, 비용)이 필요한지 먼저 판단하고 대상 플랫폼의 어댑터 저장소의 최근 릴리스를 확인한 뒤 고른다.

### 확인할 관찰

이 프로젝트의 주장을 가를 관찰은 세 가지이다.
새 공식 어댑터 API 위에서 각 어댑터가 기존 어댑터를 대체하는 시점과 Next.js 새 버전 뒤 따라오는 지연,
Lambda와 ECS 구성의 실제 비용 비교,
관리 주체가 늘고 줄 때의 유지 보수 지속성이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^grrowl]: <https://news.ycombinator.com/item?id=42199207>

[^taikon]: <https://news.ycombinator.com/item?id=42199158>

[^greyskull-infra]: <https://news.ycombinator.com/item?id=42199451>

[^syndicatedjelly]: <https://news.ycombinator.com/item?id=42199081>

[^greyskull-lag]: <https://news.ycombinator.com/item?id=42199501>

[^slashnode]: <https://news.ycombinator.com/item?id=42199449>

[^switz]: <https://news.ycombinator.com/item?id=42199910>

[^0xblinq]: <https://news.ycombinator.com/item?id=42226390>

[^bilalq]: <https://news.ycombinator.com/item?id=42199912>

[^hysan]: <https://news.ycombinator.com/item?id=42199879>
