# EmDash: 플러그인 보안을 풀면 WordPress를 이길 수 있다는 베팅

원문: [Introducing EmDash — the spiritual successor to WordPress that solves plugin security](https://blog.cloudflare.com/emdash-wordpress/)

HN 토론: <https://news.ycombinator.com/item?id=47602832> (703점, 504개 댓글)

## 요약

Cloudflare가 발표한 EmDash는 스스로를 “WordPress의 정신적 후계자”로 부르는
서버리스 풀스택 콘텐츠 관리 시스템(CMS)이다.
TypeScript와 Astro로 작성되었고, WordPress의 코드는 전혀 쓰지 않아
GPL 대신 더 관대한 MIT 라이선스를 택했다.
WordPress 기능을 AI 에이전트를 써서 “처음부터 다시” 구현했으며,
포크가 아니라 진화라고 자리매김한다.
WordPress가 인터넷의 40% 이상을 구동하지만
1999년 이후 현대적 호스팅 패러다임에 적응하지 못했다는 것이 발표의 전제다.

핵심 주장은 플러그인 보안이 문제의 뿌리라는 것이다.
발표는 “WordPress 사이트 보안 문제의 96%가 플러그인에서 비롯된다”고 인용한다.
EmDash는 이를 매니페스트 기반 권한으로 푼다.
플러그인은 Cloudflare Workers의 샌드박스된 Dynamic Isolate에서 돌고,
데이터베이스에 직접 접근하는 대신 OAuth 스코프처럼
명시적으로 선언된 권한만 받는다.
예로 이메일 알림 플러그인은 `"read:content"`와 `"email:send"`만 선언하고
그 이상은 갖지 못한다.

기술적으로 EmDash는 세 축에 선다.
샌드박스된 Dynamic Workers로 플러그인을 격리하고,
Cloudflare 인프라에서 “0으로 축소(scale to zero)”되어 실제 CPU 시간만 과금하며,
Astro 라우트로 페이지·레이아웃·컴포넌트·스타일의 테마를 구성한다.
그 밖에 인터넷 네이티브 소액결제 표준 x402 지원,
Agent Skills·CLI·MCP 서버를 갖춘 AI 네이티브 설계,
패스키 기반 인증을 제공한다.
WordPress 사이트는 WXR 익스포트 파일이나 EmDash Exporter 플러그인으로 이전하며,
커스텀 포스트 타입을 WordPress의 단일 posts 테이블에 욱여넣는 대신
별도 컬렉션으로 다룬다.
v0.1.0 프리뷰로 공개되었다.

## 분석

### 이 발표의 핵심 논지는 WordPress의 문제를 기술로 환원한다

EmDash의 서사는 하나의 진단 위에 서 있다.
WordPress의 근본 문제가 플러그인 보안이고, 그것을 샌드박스 격리로 풀면
WordPress를 대체할 수 있다는 것이다.
발표는 “플러그인 보안이 이 문제의 뿌리”라고 단언하며,
96%라는 숫자로 그 진단을 뒷받침한다.
플러그인을 격리하고 권한을 명시하면,
WordPress를 괴롭히던 보안 문제가 구조적으로 사라진다는 논리다.

이 환원이 왜 매력적인가 하면,
그것이 오래된 고통에 깔끔한 기술적 답을 주기 때문이다.
WordPress 플러그인이 데이터베이스와 파일시스템에 무제한 접근하는 구조는
실제로 보안의 온상이었다.
HN에서 foopod는 자신의 가장 큰 고통이 바로 이 플러그인 아키텍처라며,
WordPress가 플러그인을 업로드된 이미지와 같은 `wp-content` 디렉터리에
콘텐츠로 취급하는 것을 지적했다[^foopod].
earthlingdavey도 10년간 WordPress를 다룬 끝에
TypeScript와 Worker 플러그인이라는 두 선택이 정확히 옳다고 했다[^earthlingdavey].
EmDash의 진단은 실무자의 실제 고통을 정확히 짚는다.
문제는 그 고통이 WordPress가 지배적인 이유와 같은 것인가이다.

### 보안 모델이 곧 Cloudflare 런타임이라는 결합

EmDash의 기술적 핵심은 플러그인 격리인데,
그 격리는 Cloudflare Workers의 Isolate 위에서만 성립한다.
매니페스트 권한과 능력 기반 보안은 Dynamic Workers라는
Cloudflare 고유의 런타임이 강제한다.
곧 EmDash의 가장 큰 차별점인 보안 모델은
Cloudflare 인프라와 분리될 수 없다.

이 결합이 겨누는 것은 EmDash의 전략적 위치다.
발표는 EmDash를 자체 하드웨어나 어떤 플랫폼에서도 돌릴 수 있다고 하지만,
HN에서 FlamingMoe가 짚었듯,
헤드라인 기능인 Dynamic Workers 플러그인 격리는
Cloudflare 런타임에서만 작동하고,
다른 호스트에서는 그 보안 모델이 빠진 그냥 TypeScript CMS가 된다[^FlamingMoe].
이것은 우연이 아니라 설계다.
EmDash의 진짜 상품은 CMS가 아니라 Cloudflare를 CMS 런타임으로 만드는 것이고,
플러그인 보안은 그 런타임에 묶이는 이유가 된다.
오픈소스 CMS를 미끼로 Cloudflare 인프라의 채택을 유도하는 구조다.

### MIT 라이선스와 AI 재구현이 하나의 선언이다

EmDash가 WordPress 코드를 전혀 쓰지 않고 처음부터 다시 짠 것,
그래서 GPL이 아닌 MIT를 택한 것은 기술적 선택이자 정치적 선언이다.
HN에서 amiga386이 최근 WordPress 진영의 분란을 언급하며
이 타이밍이 재미있다고 한 것[^amiga386]처럼,
GPL의 제약에서 벗어난 관대한 라이선스는
WordPress 생태계의 거버넌스 갈등에 대한 대안 제시로 읽힌다.

이 재구현이 가능했던 배경에 AI가 있다는 점이 중요하다.
발표는 WordPress 기능을 AI 에이전트로 다시 구현했다고 밝힌다.
40% 점유율의 거대 시스템을 처음부터 다시 짜는 일이
AI 시대에 감당할 만한 비용이 되었다는 뜻이다.
이것은 이 저장소의 다른 노트들이 다룬 “코드는 값싸다”는 명제의 한 사례다.
예전에는 WordPress를 재구현하는 것 자체가 비현실적이었지만,
이제 그 재구현이 하나의 제품 발표가 된다.
코드를 다시 쓰는 비용이 낮아지면,
경쟁의 축은 코드에서 코드가 아닌 것으로 옮겨 간다.

## 비평

### “오픈소스”라는 말이 Cloudflare 종속을 가린다

EmDash의 가장 큰 모순은 개방성의 언어와 종속의 실질 사이에 있다.
EmDash는 MIT 오픈소스이고 자체 호스팅이 가능하다고 말한다.
그러나 그 핵심 가치인 플러그인 보안은 Cloudflare 런타임에서만 작동한다.
HN에서 bzmrgonz는 이를 날카롭게 잘랐다.
자체 호스팅하면 플러그인 샌드박스 격리의 이점이 사라지는데,
그런 게 무슨 오픈소스냐, 오픈코어도 아니고
보안 버전은 돈을 내야 하는 “오픈인시큐어”라는 것이다[^bzmrgonz].

이 모순이 결정적인 이유는 그것이 발표의 핵심 약속을 무력화하기 때문이다.
EmDash가 파는 것은 “플러그인 보안을 푼 CMS”인데,
그 보안이 Cloudflare에서만 성립한다면,
자체 호스팅하는 순간 EmDash는 평범한 TypeScript CMS로 전락한다.
곧 사용자는 두 선택뿐이다.
Cloudflare에 묶여 보안을 얻거나,
자유를 얻고 보안을 잃거나.
이 저장소의 다른 노트들이 Convex와 Cortex에서 관찰한 패턴,
곧 클라우드 위의 편의가 그 클라우드에 대한 락인과 같은 동전의 양면인 구도가
여기서 보안이라는 가장 매력적인 기능을 통해 반복된다.
오픈소스라는 간판이 그 락인을 개방으로 오독하게 만든다.

### WordPress의 지배는 코드가 아니라 네트워크 효과에서 온다

EmDash의 진단은 WordPress의 문제를 기술로 보지만,
WordPress의 강점은 기술이 아니다.
HN의 가장 많은 반박이 이 지점에 모였다.
philipwhiuk은 사람들이 WordPress를 쓰는 것은 WordPress 때문이 아니라
WooCommerce, 수백만 개의 테마, BuddyPress,
그리고 온갖 업무 API와의 통합 때문이라고 했다[^philipwhiuk].
8organicbits는 WordPress를 값지게 하는 것은 코드가 아니라
생태계와 지원이라며, 내부 구현에는 별로 감흥이 없었다고 했다[^8organicbits].
rcarr는 Cloudflare가 잘못된 각도로 접근한다며,
WordPress가 지배적인 것은 한때 사이트를 만드는 가장 쉬운 길이었고
그래서 엔지니어들의 네트워크 효과가 쌓였기 때문이라고 했다[^rcarr].

이 반박이 아픈 이유는 그것이 발표의 전제 자체를 무너뜨리기 때문이다.
EmDash가 플러그인 보안을 완벽히 풀어도,
WooCommerce가 없고, 수백만 테마가 없고,
모든 업무 도구와의 통합이 없으면,
WordPress 사용자는 옮길 이유가 없다.
JoostBoer가 플러그인 문제는 진짜이지만
자신이 WordPress에 남는 것은 충성이 아니라 클라이언트와 생태계 때문이라고 한 것[^JoostBoer]이
이 현실을 요약한다.
기술적 우월성은 네트워크 효과를 좀처럼 이기지 못한다.
EmDash는 WordPress가 못 푼 문제를 풀었을지 모르나,
WordPress가 지배하는 이유를 오진했다.

### “WordPress 후계자”의 무덤에 하나를 더하는 위험

EmDash는 WordPress 대체를 자처하는 긴 목록의 최신 항목이다.
HN에서 ramesh31은 Cloudflare가 이것을 앞으로 20년간
거대한 오픈소스 팀과 함께 일급 제품으로 밀고 갈 각오가 되어 있기를 바란다며,
그렇지 않으면 이것을 “WordPress 후계자” 무덤의 긴 목록에
하나 더 추가하는 것일 뿐이라고 했다[^ramesh31].
이 경고는 기술이 아니라 지속의 문제를 겨눈다.

이 위험이 중요한 이유는 CMS가 장기 의존의 결정이기 때문이다.
사이트를 CMS 위에 짓는 것은 수년, 때로는 수십 년의 약속이다.
그런데 EmDash는 v0.1.0 프리뷰이고,
Cloudflare가 이것을 얼마나 오래 지원할지는 불확실하다.
Cloudflare는 여러 제품을 빠르게 내고 접기도 하는 회사이며,
HN의 지적처럼 이것이 CMS에 이은 여러 시도 중 하나라면,
사용자는 Cloudflare의 전략적 인내에 자기 사이트의 미래를 거는 셈이다.
기술적으로 아무리 뛰어나도,
플랫폼의 장기 약속이 없으면 CMS로서의 신뢰는 서지 않는다.
EmDash의 진짜 시험은 v0.1.0의 기능이 아니라
5년 뒤에도 Cloudflare가 이것을 밀고 있는가이다.

## 인사이트

### 보안 모델을 런타임에 묶는 것은 오픈소스를 통한 인프라 락인의 정교한 형태다

EmDash가 무심코 드러내는 것은 오픈소스 전략의 새로운 진화다.
전통적 오픈코어는 기능을 유료와 무료로 나눈다.
EmDash는 다르다.
코드는 전부 MIT로 열되, 그 코드의 핵심 가치인 보안 모델이
특정 런타임에서만 작동하게 설계한다.
그러면 코드는 완전히 열려 있어도
그 가치를 온전히 누리려면 Cloudflare를 써야 한다.
오픈소스의 개방성과 인프라 락인이 모순 없이 결합한다.

이 구조가 낳는 2차 효과가 있다.
이 모델이 성공하면, 오픈소스의 정의가 흐려진다.
코드가 열려 있다는 것과 그것을 자유롭게 쓸 수 있다는 것이 갈라진다.
사용자는 코드를 볼 수 있고 포크할 수 있지만,
그 코드가 약속하는 것을 얻으려면 특정 제공자에 묶인다.
이것은 이 저장소의 다른 노트가 Cog에서 관찰한,
오픈소스 표준을 상용 플랫폼의 관문으로 삼는 전략의 더 정교한 판본이다.
Cog는 포장의 표준을 쥐었고, EmDash는 보안의 런타임을 쥔다.
가장 매력적인 기능을 인프라에 결합하면,
그 기능을 원하는 모두가 그 인프라로 온다.
오픈소스가 인프라 채택의 미끼가 되는 이 패턴은
앞으로 더 흔해질 것이다.

### 코드가 값싸진 시대에 네트워크 효과의 가치는 오히려 오른다

EmDash가 AI로 WordPress를 처음부터 재구현했다는 사실은
역설적 통찰을 준다.
코드를 다시 쓰는 것이 값싸질수록,
코드 자체는 해자가 되지 못한다.
EmDash가 증명한 것은 40% 점유율 시스템의 기능도
AI로 재구현할 수 있다는 것이지만,
바로 그 사실이 재구현으로는 WordPress를 이길 수 없음을 보여 준다.
누구나 기능을 재구현할 수 있다면,
남는 차이는 재구현할 수 없는 것,
곧 생태계와 네트워크 효과다.

이 역전이 시사하는 것은 경쟁 우위의 이동이다.
소프트웨어의 가치가 코드에 있던 시대에는
더 나은 코드가 승부를 갈랐다.
그러나 AI가 코드를 값싸게 만들면,
승부는 코드가 아니라 코드 바깥의 것으로 옮겨 간다.
WooCommerce의 상거래 생태계, 수백만 테마의 축적,
20년간 쌓인 개발자와 대행사의 네트워크는 AI로 재구현되지 않는다.
그것들은 코드가 아니라 사람과 시간과 신뢰의 축적이기 때문이다.
EmDash의 기술적 우월성이 WordPress의 사회적 축적을 이기지 못한다는 것은,
AI 시대에 진짜 희소한 것이 무엇인지를 가리킨다.
코드가 값싸질수록, 코드로 만들 수 없는 것의 값이 오른다.

### CMS를 AI 에이전트의 대상으로 재설계하는 것은 웹의 소비자가 바뀐다는 신호다

EmDash의 기능 목록에서 조용히 급진적인 것은 AI 네이티브 설계다.
Agent Skills, MCP 서버, x402 소액결제는
사람이 아니라 에이전트가 콘텐츠를 관리하고 소비하는 것을 전제한다.
특히 x402는 에이전트가 HTTP 요청으로 콘텐츠 대금을 지불하는 표준으로,
HN에서 andy_xor_andrew가 설명했듯
클라이언트, 곧 에이전트가 요청을 보내고 402 Payment Required를 받아
건별로 지불하는 구조다[^andy_xor_andrew].
이것은 CMS의 독자가 사람에서 에이전트로 확장된다는 가정이다.

이 재설계가 던지는 더 깊은 함의가 있다.
지금까지 CMS는 사람이 읽을 콘텐츠를 사람이 관리하는 도구였다.
EmDash가 MCP와 x402를 기본으로 두는 것은,
콘텐츠를 만들고 관리하고 소비하는 주체에 에이전트가 낀다고 보는 것이다.
에이전트가 콘텐츠를 프로그램적으로 관리하고,
에이전트가 콘텐츠를 건별로 구매하는 웹이 온다면,
CMS는 사람의 편집 도구를 넘어 에이전트의 콘텐츠 API가 되어야 한다.
이 베팅이 옳은지는 아직 모른다.
그러나 EmDash가 이것을 기본 설계로 삼았다는 것은,
웹 콘텐츠의 소비자가 사람만이 아니게 되는 전환을
인프라 층위에서 준비하는 것이다.
WordPress가 블로그의 시대를 위한 CMS였다면,
EmDash는 에이전트의 시대를 겨냥한 CMS로 자신을 던진다.
그 겨냥이 시기상조인지 선견인지가,
이 제품의 운명을 플러그인 보안보다 더 크게 가를 것이다.

---

[^earthlingdavey]: <https://news.ycombinator.com/item?id=47606147>
[^rcarr]: <https://news.ycombinator.com/item?id=47607571>
[^8organicbits]: <https://news.ycombinator.com/item?id=47603398>
[^foopod]: <https://news.ycombinator.com/item?id=47605699>
[^FlamingMoe]: <https://news.ycombinator.com/item?id=47603999>
[^bzmrgonz]: <https://news.ycombinator.com/item?id=47609668>
[^amiga386]: <https://news.ycombinator.com/item?id=47604024>
[^philipwhiuk]: <https://news.ycombinator.com/item?id=47603108>
[^JoostBoer]: <https://news.ycombinator.com/item?id=47611712>
[^ramesh31]: <https://news.ycombinator.com/item?id=47603404>
[^andy_xor_andrew]: <https://news.ycombinator.com/item?id=47603526>
