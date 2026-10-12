# Deno는 런타임을 내려놓고 Cloudflare에서 celld에 건다

원문: [Deno is joining Cloudflare | Deno](https://deno.com/blog/cloudflare)

HN 토론: <https://news.ycombinator.com/item?id=50019911> (1200점, 610개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/8hauxs/deno_is_joining_cloudflare> (44점, 22개 댓글)

GN 토론: <https://news.hada.io/topic?id=35073>

## 요약

Ryan Dahl이 2026년 10월 9일 Deno 블로그에 올린 발표문이다.
Deno 팀 전체가 Cloudflare에 합류한다는 내용이다.
글은 지난 몇 년의 작업을 먼저 돌아본다.
모듈 배포 방식, JavaScript 런타임이 줄 수 있는 보안 보장,
완결된 도구 체인의 범위,
애플리케이션을 단일 실행 파일로 배포하는 일을 다시 따져 왔고,
사용자들이 기존 JS 생태계에 연결되기를 원했기 때문에 Node.js 호환성도 중요한
작업이 되었다고 적는다.

Dahl은 자신의 야심이 처음부터 런타임 너머에 있었다고 말한다.
그가 예전에 쓴 글
[JavaScript Containers](https://tinyclouds.org/javascript-containers/)에서
밝혔듯이, 애플리케이션마다 인프라를 따로 조립하지 않아도 컴퓨팅, 스토리지,
통신이 함께 동작하는 환경이 목표였다.
Deno Deploy는 그 방향의 한 걸음이었지만,
Deploy를 만들고 운영하면서 개발자 경험 아래에 얼마나 많은 복잡성이 남아 있는지
보게 되었다고 한다.
그 층까지 단순하게 만들려는 시도가 [celld](https://celld.dev)다.
celld는 Cloudflare Workers의 프로그래밍 모델 위에서 분산 애플리케이션을 처음부터
짜게 하면서 운영은 단순하게 유지하려 하며,
확장성을 앱마다 조립하는 인프라가 아니라 프로그래밍 모델 자체에 넣는다는 점이
그를 가장 들뜨게 한다고 적었다.

Deno에서 Deno Deploy, 다시 celld로 이어진 흐름이 이번 결정의 근거로 제시된다.
Cloudflare에서는 Workers 팀, Durable Objects 팀과 작업을 합쳐,
Cloudflare 네트워크에서든 자체 인프라에서든 이 프로그래밍 모델을 서버를 만드는
기본 방식으로 만들겠다고 한다.
그 대가로 별도의 런타임과 호스팅 서비스를 계속 개발하지 않고 공동 플랫폼에 개발
역량을 모으기로 했으며, Deno 위에 무언가를 만든 사람들에게 중대한 변화라는 점을
안다고 썼다.

구체적인 일정은 글 후반부의 목록 네 줄에 있다.

| 대상        | 발표된 내용                                                           |
| ----------- | --------------------------------------------------------------------- |
| Deno 런타임 | 1년 동안 버그 수정과 보안 업데이트를 담은 월간 릴리스, 이후 개발 종료 |
| Deno Deploy | 6개월 운영 후 종료, 유료 고객의 Cloudflare Workers 이전 지원          |
| JSR         | 운영 계속, 인프라는 Cloudflare로 이전                                 |
| rusty_v8    | 지원 계속, workerd 통합 추진                                          |

런타임은 오픈소스로 남고 개발을 이어갈 사람을 환영한다는 문장이 붙어 있다.
글은 AI 이야기로 끝난다.
Durable Objects는 저렴한 서버리스 실행, 영속 상태, WebSockets,
고수준 JavaScript 인터페이스를 한데 묶기 때문에 에이전트 하네스에 특히 쓸모가
있고, celld가 Durable Objects에 집중하는 이유도 여기에 있다고 한다.
대규모 에이전트를 자체 인프라에서 돌리려는 사람에게 `ry@cloudflare.com`으로
연락하라고 덧붙였다.

### Cloudflare 쪽 공동 발표

Dahl은 Kenton Varda와 함께 Cloudflare 블로그에도
[공동 글](https://blog.cloudflare.com/deno-joins-cloudflare/)을 따로 냈다.
이 글은 Deno 블로그보다 길고, 합류의 목적을 Workers와 Durable Objects의 자체
호스팅을 대폭 단순하게 만드는 것으로 요약한다.
Dahl의 부분은 Berlin의 창고에서 500줄짜리 JavaScript IRC 서버로 Node.js를 처음
소개한 기억에서 출발한다.
그 데모는 연결은 많이 받아도 단일 서버, 단일 스레드였고,
IRC를 확장하려면 결국 여러 머신에 채널을 나눠야 한다.
그는 Durable Objects를 “SQLite 데이터베이스를 가진 분산 싱글턴”으로 소개하며,
채널마다 객체 하나를 두면 데이터와 WebSocket 연결이 함께 샤딩된다고 설명한다.
workerd는 이미 오픈소스지만 Durable Objects는 단일 인스턴스로만 지원하므로,
배치와 라우팅과 영속 저장을 플랫폼이 맡는 분산판을 만들려고 celld를 시작했다고
한다.
celld는 Rust로 쓴 바이너리 하나이고 외부 의존은 객체 스토리지뿐이다.

Varda의 부분은 Workers가 고객을 가두려고 일부러 다르게 설계되었다는 통념을
반박하는 데 거의 전부를 쓴다.
Workers가 다른 이유는 더 낫기 때문이며, 2022년 Shopify 같은 고객에게 Workers for
Platforms를 제안했을 때 런타임이 오픈소스가 아니면 쓸 수 없다는 답을 듣고
workerd를 공개했다고 한다.
workerd로 Cloudflare를 떠난 예전 고객도 있고 그래도 괜찮다는 것이 그의 입장이다.
다만 workerd는 Durable Objects를 로컬 테스트 수준의 단일 인스턴스로만 구현했고,
프로덕션의 라우팅 구현은 수백 개 거점과 여러 외부 서비스에 의존하는 “괴물”이라
자체 호스팅에는 맞지 않았다고 인정한다.
그 자신도 지난봄에 시도했지만 동작하지 않았다고 적었다.
그래서 8월에 Deno 팀이 celld를 내놓았을 때 반가웠다는 것이다.
계획은 Ryan Dahl과 Bert Belder가 workerd 자체 호스팅을 정식 지원 경로로 만드는
일을 이끌고, celld의 코드와 아이디어를 workerd로 합치는 것이다.

공동 글에는 Deno 런타임의 개발 종료나 Deno Deploy의 종료 일정이 나오지 않는다.
Dahl의 첫 단락이 Deno 블로그를 보라고 안내할 뿐이다.

## 분석

### 발표의 무게중심은 맨 아래 네 줄에 있다

글의 대부분은 철학과 계보다.
서버 소프트웨어를 단순하게 만들려는 오랜 시도, JavaScript Containers,
Deno Deploy, celld로 이어지는 서사가 앞을 채우고,
사용자에게 실제로 영향을 주는 결정은 감사 인사 뒤에 목록으로 나온다.
HN에서 가장 먼저 위로 올라온 반응도 이 배치였다.
binlog는 이렇게 큰 내용을 맨 아래에 묻어 두었다고 놀랐고,[^binlog] simonw는
런타임 종료가 Deno 글에는 있는데 Cloudflare 글에는 한 줄도 없다고
지적했다.[^simonw]
Lobste.rs의 mort는 “Deno는 단종되고 개발팀이 Cloudflare에 인수된다”가 정직한
제목일 것이라고 적었다.[^mort]

제목도 같은 긴장을 안고 있다.
Deno 글은 “joining”이라고 썼고, Cloudflare 블로그는 글에 Acquisitions 태그를
달았으며, HN 제출 제목은 “Cloudflare acquires Deno”였다.
회사 Deno Land Inc.가 합류하는 것은 맞지만,
사람들이 이름으로 아는 Deno는 런타임이고 그 런타임은 합류하지 않는다.
GN의 laeyoung이 사실상 Deno는 끝났다고 짧게 적은 것도 이 간극을 읽은
결과다.[^laeyoung]

### Dahl은 런타임 경쟁에서 스스로 걸어 나왔다

HN에서 누가 런타임 포기를 결정했느냐는 질문에 Dahl(rough-sea)은 공동 결정이며
자신도 동의한다고 답했다.[^rough-sea]
그는 Deno에 가장 많이 투자한 사람이 자신이지만 더 이상 그곳이 가장 중요한 일을
할 자리라고 생각하지 않는다고 했다.
Deno는 좋은 아이디어가 있고 잘 설계되었지만 결국 큰 문제를 풀지 못하고 있으며,
Node 호환성이라는 중력에 빨려 들어가 Node와 똑같이 동작해야 하는 처지가 되었다는
것이다.
“왜 Node를 다시 구현하나? Node는 잘 돌아간다. 성능이나 UX나 보안에서의 미미한
이득으로는 충분하지 않다.”

이 답은 발표문보다 솔직하다.
발표문은 런타임 개발 종료를 플랫폼 집중의 대가로 설명하지만,
댓글은 런타임 자체가 더는 의미 있는 차이를 만들지 못한다고 인정한다.
HN의 TheRoque가 상기시킨 것처럼 Dahl은 2018년 Node에서 싫은 점을 이야기하는
발표로 Deno를 소개했다.[^TheRoque]
그 사람이 8년 뒤 Node가 충분히 좋아졌다는 이유로 Deno를 멈추는 셈이다.
HN의 flanbiscuit는 Node가 권한 모델, 타입 제거 방식의 TypeScript 실행,
단일 실행 파일을 차례로 갖추었다고 날짜와 함께 정리했다.[^flanbiscuit]
Lobste.rs의 kraxen72는 Deno가 처음에는 `deno.json`, URL import,
import map으로 자기 길을 갔다가 사람들이 Node 방식을 버리지 않자 호환으로
돌아섰고, Node만큼 호환되지도 않으면서 Node 위에 얹을 이득도 크지 않은 어정쩡한
자리에 남았다고 진단했다.[^kraxen72]

이 흐름은 엿새 전 David Bushell이 Deno를 떠나 Node로 돌아간 이야기와 정확히
겹친다(`deno/deno-to-node.md`).
그 글에서 Bushell은 Deno가 런타임 혁신을 멈추고 “Temu Cloudflare”를 바이브
코딩하고 있다고 비꼬았다.
해석하자면 그가 가리킨 제품은 celld로 보이며,
엿새 뒤 Cloudflare가 그 팀을 데려갔다.

### Cloudflare가 산 것은 런타임이 아니라 자체 호스팅 이야기다

Cloudflare 입장에서 이 거래의 핵심은 celld다.
HN의 ttul은 이번 인수가 오픈소스 프로젝트 Deno가 아니라,
쓸 만한 자체 호스팅 Workers를 만든 팀을 사는 것이며 보완재를 상품화하는
전략이라고 정리했다.[^ttul]
Cloudflare에 묶이는 것을 꺼리는 고객에게 단단한 자체 호스팅 대안이 있으면
Cloudflare를 고르는 문턱이 낮아진다는 것이다.
Varda의 글이 lock-in 반박에 지면 대부분을 쓰는 이유도 같다.

Varda는 HN에서 Cloudflare가 런타임을 죽이려고 회사를 샀다는 해석을 정면으로
부정했다.[^kentonv]
그렇게 보일 줄 알았고 그 인상을 반박하기 어려우리라는 것도 알았지만,
실제로는 Deno 팀이 celld에 다시 집중하기로 전략적 결정을 내렸고 Cloudflare는 그
일을 지원하게 되어 기쁜 것이라고 했다.
Wasmer 창업자 syrusakbary가 D1, KV, Queues는 Cloudflare 밖에서 돌릴 수 없으니
workerd의 의미 체계는 결국 Cloudflare 전용이라고 반박하자,[^syrusakbary]
그는 이 인터페이스들을 일반 인프라에 올릴 수 있는 참조 구현과 함께
갈아 끼울 수 있게 만드는 것이 목표이고,
celld가 이미 많은 부분을 해 두었다고 답했다.[^kentonv-2]
Dahl도 계획을 한 줄로 설명했다.
버킷으로 조율과 저장을 하는 workerd 인스턴스 함대를 돌리는 것이고,
별도 런타임이 아니라 workerd 위에 만들어야 노력이 나뉘지 않고 Cloudflare와 자체
호스팅의 API가 정확히 같아진다는 것이다.[^rough-sea-2]

celld 자체는 저장소의 `distributed-system/celld.md`에서 다룬 것처럼 노드끼리
합의 없이 버킷 하나로 조율하는 설계다.
celld 홈페이지는 지금도 Workers, Durable Objects, KV, Queues, D1, R2, Workflows,
Cron, 정적 자산을 지원한다고 표시하고, 기존 `wrangler.json`을 그대로 읽는다고
적는다.
syrusakbary의 반론에 대한 답의 상당 부분이 이미 celld 안에 있는 셈이다.

### JSR과 rusty_v8은 살아남는 이유가 다르다

네 줄의 목록에서 살아남는 것은 JSR과 rusty_v8이다.
rusty_v8은 이유가 분명하다.
Rust에서 V8을 쓰는 데 가장 잘 관리되는 바인딩이고,
Dahl은 HN에서 계속 유지하며 workerd에 통합하는 작업을 하겠다고
답했다.[^rough-sea-3]
celld와 workerd를 합치는 계획에서 Rust와 V8 사이의 접합부는 계속 필요하다.

JSR은 덜 분명하다.
Deno가 멈추면 JSR을 누가 쓰느냐는 질문에, skybrian은 JSR 패키지가 Node, Bun,
Workers에서도 돌아간다고 답했다.[^skybrian]
글은 JSR을 계속 운영하는 이유를 설명하지 않는다.
런타임 없이 레지스트리만 남는 구조가 오래 유지될지는 이 글만으로는 판단하기
어렵다.

## 비평

### 런타임 종료의 비용을 글은 숫자로 보여 주지 않는다

발표문은 Deno 위에 무언가를 만든 사람들에게 중대한 변화라고 인정하지만,
그 사람들이 누구이고 얼마나 되는지는 말하지 않는다.
HN의 amber71de는 이 공백을 정확히 짚었다.[^amber71de]
이전 지원을 유료 고객에게만 약속하고 기간을 6개월로 잡았다는 것은 손으로 하나씩
챙길 수 있을 만큼 고객 수가 적다는 뜻처럼 읽힌다고 했다.
런타임 다운로드가 수백만이어도 유료 계정이 수백 개일 수 있고,
팀의 월급을 내는 것은 뒤쪽 숫자뿐이라는 것이다.

영향을 받는 범위는 Deno Deploy 고객보다 넓다.
HN의 tech234a는 yt-dlp가 YouTube 다운로드에 필요한 JavaScript 실행에 Deno를
기본·권장 런타임으로 쓴다고 지적했다.[^tech234a]
geggo98은 그 이유가 샌드박스라고 설명했다.
yt-dlp는 사이트에서 받은 난독화 코드를 실행해 다운로드 URL을 얻는데,
광고에서 온 코드일 수도 있는 것을 Node나 Bun에서 그대로 돌리기는 위험하다는
것이다.[^geggo98]
GN의 click도 같은 프로젝트를 먼저 걱정했다.[^click]
Supabase와 Bunny의 Edge Scripting처럼 Deno를 서버리스 함수 실행기로 쓰는
플랫폼도 댓글에서 거듭 언급되었다.

이들은 Deno Deploy 고객이 아니므로 Cloudflare Workers로의 이전 지원 대상이
아니다.
글이 약속한 것은 1년의 월간 보안 릴리스와 오픈소스 라이선스가 전부다.
발표문이 Deploy 고객에게는 구체적인 이전 경로를 주면서 런타임 사용자에게는
“누군가 이어 주기를 환영한다”만 남긴 비대칭은,
이번 결정이 누구의 입장에서 설계되었는지를 보여 준다.

### “누구든 이어 가도 좋다”는 말은 이어 갈 조건을 주지 않는다

Dahl은 HN에서도 사람들이 Deno를 이어 가길 바란다고 했다.
그러나 이어 가는 데 필요한 것은 라이선스만이 아니다.
jflatow는 곧바로 Cloudflare가 이름과 자산을 내놓을 것인지,
아니면 포크해야 하는지 물었다.[^jflatow]
글에는 상표, 도메인, 패키지 배포 경로, CI 인프라,
보안 신고 창구를 어떻게 할지에 대한 말이 없다.

HN의 zem은 오픈소스가 이론상 분산되어 있어도 실제로는 한 주체가 관리해야
살아남는다고 지적하며, 사용 기업들의 컨소시엄이 OpenTofu처럼 그 역할을 맡기를
바랐다.[^zem]
syrusakbary는 창업자가 빠지고 강한 기업 후원자도 없는 상태라 그럴 가능성이
낮다고 답했다.[^syrusakbary-2]
Lobste.rs 운영진 355E3B는 HashiCorp가 IBM에 넘어갔을 때처럼,
Deno에 대해서도 OpenTofu, OpenBao 같은 포크 논의가 뒤따를 것이라고
예상했다.[^355E3B]
그 예상이 맞으려면 포크가 붙잡을 이름과 인프라가 정해져 있어야 하는데,
발표문은 그 부분을 비워 두었다.

### 자체 호스팅의 약속은 아직 계획 단계다

Varda의 글은 workerd 자체 호스팅이 정식 지원 경로가 될 것이라고 하지만,
지금 확정된 것은 방향과 담당자뿐이다.
Varda 자신도 HN에서 결과물이 어떤 모양일지 아직 완전히 알지 못하며,
다만 반드시 오픈소스일 것이라고 말했다.[^kentonv-3]
syrusakbary와의 문답에서도 세부는 정해지지 않았다는 전제가 붙었다.

반대로 확정된 것은 종료 일정이다.
Deno Deploy는 6개월, 런타임은 1년이다.
새로 합쳐질 workerd가 그 안에 celld 수준의 분산 Durable Objects를 갖출지는
알 수 없다.
지금 celld는 홈페이지 기준 v0.6.2 beta이고,
Varda가 첫 공개 때부터 TODO 주석으로 남아 있었다고 고백한 문제가 단 몇 달 만에
정식 지원으로 바뀐다고 기대할 근거는 글에 없다.
사용자에게 주어진 것은 확정된 종료와 확정되지 않은 대체재의 조합이다.

### lock-in 반박은 Cloudflare 자신의 기록과 부딪힌다

Varda는 Workers가 다른 것은 더 낫기 때문이며 lock-in은 오히려 Cloudflare에
해롭다고 주장한다.
그런데 그 근거로 든 workerd는 그가 직접 인정했듯 Durable Objects를 확장 가능한
형태로 구현하지 않았다.
Durable Objects를 쓴 앱은 구조부터 다르게 설계된다고 스스로 쓰면서,
그 앱을 다른 곳에서 돌릴 수단은 수년간 없었다.
탈출구가 있었다고 말하려면 그 탈출구가 가장 묶이기 쉬운 기능까지 열려 있어야
한다.

celld 홈페이지는 이 점을 다른 방식으로 보여 준다.
페이지는 Durable Objects의 신뢰성에 10점 만점에 2점을 준 외부 리뷰와,
2026년 7월 16일 Cloudflare 상태 페이지의 Durable Objects 장애 기록을 나란히
인용하고,
자체 호스팅이 장애 범위와 진단을 사용자 손에 돌려준다고 설명한다.
그 문구를 쓴 팀이 이제 Cloudflare 안에서 같은 문제를 맡는다.
Lobste.rs의 noirscape는 celld가 나온 지 두 달밖에 되지 않았는데
곧바로 팀째 사 오면서 경쟁자를 사는 것이 아니라고 말하는 데에는,
우리가 보지 못한 뒷이야기가 있을 것 같다고 적었다.[^noirscape]
HN의 patcon도 유럽 정부 쪽 사람들과 celld를 데이터 주권의 대안으로 논의하던
대화가 이 소식으로 상당히 김이 빠졌다고 했다.[^patcon]
Cloudflare 밖의 대안이라는 celld의 성격 자체가 이번 합류로 달라진다는 점을 글은
다루지 않는다.

## 인사이트

### 인수합병이 아니라 각자의 출구가 맞물린 거래다

이 거래는 한쪽이 다른 쪽을 삼킨 구조로 읽히기 쉽지만,
공개된 사실을 이어 보면 두 회사의 출구가 겹친 쪽에 가깝다.
Deno 쪽에서 보면 런타임은 Node 호환의 중력에 끌려 차별점을 잃었고,
HN에서는 지난 해고 이후 발표와 혁신이 눈에 띄게 줄었다는 기억이 여럿 나왔다.
dpc94는 그때부터 조짐이 보였다며 Deno의 쇠퇴와 해고를 다룬 Bushell의 3월 글을
함께 소개했다.[^dpc94]
Dahl의 관심은 이미 celld로 옮겨 가 있었다.
Cloudflare 쪽에서 보면 workerd의 Durable Objects 공백은 수년 묵은 숙제였고,
내부에서 풀지 못한 일을 외부 팀이 먼저 풀었다.

해석하자면, 이 구조에서 런타임 종료는 Cloudflare가 강요한 조건이라기보다 Deno
쪽이 이미 내린 결론을 공식화한 것이다.
Lobste.rs의 lilac은 이를 악의적인 음모가 아니라 자비로운 안락사라고
불렀다.[^lilac]
이렇게 읽으면 비난의 대상은 Cloudflare가 아니라,
VC 자금을 받은 오픈소스 런타임이라는 사업 구조가 된다.
HN의 garganzol은 lock-in이 없고 자체 호스팅이 자유롭다는 Deno의 약속과
Deno Deploy라는 수익 모델이 처음부터 서로 어긋났다고 적었다.[^garganzol]
celld가 Deploy의 다음 단계로 나온 것도, 결국 그 모순을 Cloudflare라는 더 큰
플랫폼 안에서 해소하는 방향이다.

### 기술 선택의 위험 평가 단위가 프로젝트에서 소유 구조로 바뀐다

Bun은 Anthropic으로, Vite를 만든 VoidZero는 Cloudflare로,
Deno 팀도 Cloudflare로 갔다(`javascript/voidzero-joins-cloudflare.md`).
HN의 sixdimensional은 Astral, Bun, Astro,
VoidZero로 이어지는 개발 도구 인수 목록을 적었고,
답글이 그 목록을 길게 이어 붙였다.[^sixdimensional]
Lobste.rs의 hongminhee는 앞으로 스타트업이 만든 개발 플랫폼은 비전이 아무리
좋아도 신뢰하지 않겠다고 적었다.[^hongminhee]

여기서 나오는 2차 효과는 채택 판단의 기준 이동이다.
지금까지 런타임이나 도구를 고를 때는 성능, 기능, 커뮤니티 크기를 봤다.
이번 일 이후에는 그 프로젝트를 누가 소유하고,
소유자가 사라지면 이름과 배포 인프라가 어디로 가는지가 먼저 질문이 된다.
HN의 ksajadi가 다음에 Deno 같은 프로젝트를 볼 때는
거버넌스 구조와 대기업이 살 수 있는 구조인지부터 보겠다고 한 것이
그 신호다.[^ksajadi]
Node가 Linux 재단 아래에 있다는 사실이 이 스레드에서 거듭 Node 쪽의 장점으로
언급된 것도 같은 이유다.

이 기준은 신생 프로젝트에 불리하게 작용한다.
재단 아래로 가려면 이미 커야 하고, 커지려면 대개 자본이 필요하며,
자본은 다시 이번 같은 결말의 가능성을 만든다.
Deno가 Node를 자극해 TypeScript 실행, 권한 모델,
내장 SQLite를 끌어냈다는 평가는 HN과 Lobste.rs 양쪽에서 거의 이견 없이 나왔다.
대안 런타임이 그렇게 생태계에 기여하는 경로 자체가 이번 일로 더 좁아질 수 있다.

### “떠나기 쉬움”이 이제 런타임의 방어 수단이 아니라 약점이다

Deno가 Node 호환에 들인 노력은 원래 채택 장벽을 낮추려는 것이었다.
그러나 호환이 완성될수록 Deno를 떠나는 비용도 같이 낮아진다.
HN에는 Deno에서 하루면 옮긴다거나 AI에게 맡기면 한 시간이면 된다는 댓글이 여럿
달렸고, Bushell도 엿새 전 이전 작업이 몇 군데의 API 교체로 끝났다고 썼다.
GN의 unsure4000이 yt-dlp도 어댑터 구조라 Node로 금방 옮길 수 있을 것이라고 본
것도 같은 맥락이다.[^unsure4000]

이 사실은 이번 종료의 충격을 줄이는 동시에,
왜 Deno가 지속되지 못했는지도 설명한다.
떠나기 쉬운 플랫폼은 사용자를 붙잡을 이유를 따로 만들어야 하는데,
Deno에서 그 이유는 권한 모델과 설치 없는 의존성 import 같은 소수의 기능이었다.
HN의 flohofwoe가 package.json 없이 `npm:` 지정자로 의존성을 바로 가져오는
스크립트를 Node로는 대체할 수 없다고 아쉬워한 것처럼,
남은 차별점은 작고 구체적이다.[^flohofwoe]
반대로 celld와 Durable Objects는 애플리케이션 구조 자체를 바꾸게 만든다.
Dahl이 “파일 시스템이나 네트워크를 다루는 약간 다른 API”가 아니라 “서버 개발의
완전히 새로운 모델”이라고 강조한 대목은,
쉽게 떠날 수 없을 만큼 깊은 차이를 만들어야 한다는 교훈으로도 읽힌다.

그 교훈은 Varda의 lock-in 반박과 묘하게 겹친다.
다르기 때문에 더 낫다는 Workers의 논리와,
깊이 달라야 의미가 있다는 Dahl의 결론은 같은 말이다.
그렇다면 workerd 자체 호스팅이 실제로 갖춰지는 시점이 이 거래의 진짜 시험대가
된다.
구조가 깊이 다른 모델일수록, 그 모델을 다른 곳에서 돌릴 수단이 있어야만
lock-in이 아니라는 주장이 성립하기 때문이다.

### Lobste.rs가 이 소식을 내린 이유가 보여 주는 것

Lobste.rs에서는 이 발표 스토리가 운영진에 의해 목록에서 내려갔다.
운영자 pushcx는 22개 댓글 중 18개가 사업 관행에 관한 것이었고,
고용 관행 논의는 HN이나 Reddit이 더 맞는 곳이라고 설명했다.[^pushcx]
사이트 지침은 프로그래머를 많이 고용한 회사에 관한 뉴스를 주제 밖으로 명시한다.

이 결정은 이번 발표가 기술 뉴스와 사업 뉴스의 경계에 서 있다는 것을 드러낸다.
발표문은 celld와 Durable Objects라는 기술 서사로 포장되어 있지만,
사람들이 실제로 반응한 것은 런타임 종료라는 사업 결정이었다.
HN의 OtherShrezzing이 말했듯, Deno 위에 사업을 만든 사람에게 13개월 뒤 지원이
끊긴다는 사실은 기술의 흥미보다 앞서는 실존적 위험이다.[^OtherShrezzing]
기술 커뮤니티가 같은 소식을 두고 “서버 개발의 새 모델”과 “인수 후 단종” 중
무엇으로 읽느냐는, 결국 그 사람이 Deno에 무엇을 걸어 두었느냐에 달려 있다.

---

[^simonw]: <https://news.ycombinator.com/item?id=50020172>

[^mort]: <https://lobste.rs/s/8hauxs/deno_is_joining_cloudflare#c_h5qge0>

[^laeyoung]: <https://news.hada.io/topic?id=35073#cid67315>

[^rough-sea]: <https://news.ycombinator.com/item?id=50023277>

[^flanbiscuit]: <https://news.ycombinator.com/item?id=50022568>

[^kraxen72]: <https://lobste.rs/s/8hauxs/deno_is_joining_cloudflare#c_ce6sr4>

[^ttul]: <https://news.ycombinator.com/item?id=50021640>

[^kentonv]: <https://news.ycombinator.com/item?id=50025430>

[^kentonv-2]: <https://news.ycombinator.com/item?id=50026270>

[^rough-sea-2]: <https://news.ycombinator.com/item?id=50023506>

[^rough-sea-3]: <https://news.ycombinator.com/item?id=50023382>

[^amber71de]: <https://news.ycombinator.com/item?id=50022423>

[^tech234a]: <https://news.ycombinator.com/item?id=50022900>

[^geggo98]: <https://news.ycombinator.com/item?id=50029973>

[^click]: <https://news.hada.io/topic?id=35073#cid67278>

[^zem]: <https://news.ycombinator.com/item?id=50025353>

[^355E3B]: <https://lobste.rs/s/8rrtma/cloudflare_shutting_down_deno_is_news_not#c_ukxozf>

[^noirscape]: <https://lobste.rs/s/8hauxs/deno_is_joining_cloudflare#c_zragav>

[^patcon]: <https://news.ycombinator.com/item?id=50020345>

[^dpc94]: <https://news.ycombinator.com/item?id=50021372>

[^lilac]: <https://lobste.rs/s/8rrtma/cloudflare_shutting_down_deno_is_news_not#c_dgvax2>

[^garganzol]: <https://news.ycombinator.com/item?id=50028069>

[^hongminhee]: <https://lobste.rs/s/8hauxs/deno_is_joining_cloudflare#c_vwpppx>

[^unsure4000]: <https://news.hada.io/topic?id=35073#cid67309>

[^flohofwoe]: <https://news.ycombinator.com/item?id=50022052>

[^pushcx]: <https://lobste.rs/s/8rrtma/cloudflare_shutting_down_deno_is_news_not#c_zpfjw7>

[^binlog]: <https://news.ycombinator.com/item?id=50020218>

[^TheRoque]: <https://news.ycombinator.com/item?id=50021125>

[^syrusakbary]: <https://news.ycombinator.com/item?id=50025779>

[^skybrian]: <https://news.ycombinator.com/item?id=50027128>

[^jflatow]: <https://news.ycombinator.com/item?id=50028278>

[^syrusakbary-2]: <https://news.ycombinator.com/item?id=50025407>

[^kentonv-3]: <https://news.ycombinator.com/item?id=50022333>

[^sixdimensional]: <https://news.ycombinator.com/item?id=50024230>

[^ksajadi]: <https://news.ycombinator.com/item?id=50029119>

[^OtherShrezzing]: <https://news.ycombinator.com/item?id=50020889>
