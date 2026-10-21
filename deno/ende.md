# Deno 종료에 대한 한 개발자의 답은 Node 호환을 버린 개인 포크 Ende다

원문: [the webb blog • beginning of the ende](https://blog.webb.page/WM-105)

HN 토론: <https://news.ycombinator.com/item?id=50048424> (4점, 2개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=50158288> (4점, 1개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=50174764> (1점, 0개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork> (41점, 25개 댓글)

GN 토론: <https://news.hada.io/topic?id=35688>

## 요약

P. Webb은 2026년 10월 11일 자기 블로그에서 Deno가 죽었다고 선언한다.
금요일에 발표됐고, 팀은 Cloudflare로 떠났으며,
1년 뒤에는 런타임 개발을 멈춘다는 것이다.
그는 이것이 몇 년 사이 자기가 의존하는
기술이 커뮤니티에 넘겨진 두 번째 경우라고 쓴다.
첫 번째로 든 것은 Gel이다. Gel 팀이 Vercel로 옮기며
프로젝트를 커뮤니티에 맡겼고,
글에 따르면 Disc는 그 일 때문에 시작된 프로젝트이며
커뮤니티가 맡은 공식 포크에는 그 뒤로 갱신이 없다.

글은 Deno 커뮤니티의 분노를 보여 주는 사례로 GitHub 이슈 하나를 길게 인용한다.
이어 Ryan Dahl이 Hacker News에 단 댓글을 인용한다.
Dahl은 Deno가 Node 호환성의 중력에 빨려 들어가 Node와 똑같이 동작해야 했고,
성능이나 사용성이나 보안의 작은 이점만으로는
Node를 다시 구현할 이유가 되지 못한다고 했다.
Webb은 이를 두고 Node를 다시 구현해 놓고 이제 지루해졌느냐고 되받는다.

그래서 그는 자기 포크를 시작한다.
이름은 독일어로 끝이라는 뜻의 Ende이고,
Node와 Deno의 철자를 뒤섞은 것이라고 설명한다.
Node 호환을 없애고 Deploy와 KV와 Jupyter 같은 곁가지도 모두 뺀다.
로드맵은 모듈별 권한, 신뢰할 수 없는 코드를 위한 샌드박스,
Web Crypto의 양자내성 암호, 더 나은 바이너리 출력이다.
그는 자기 모든 API와 개인 프로젝트를 Deno에 올려 두었고
이제 그 위에서 사업을 만들고 있어서
12월에 소프트 론칭을 목표로 한다.
끝에는 SemVer 대신 날짜 기반의 ChronVer를 쓰겠다고 덧붙였다.

## 분석

### 글은 항의문이면서 사업 계획서다

겉으로는 Deno의 종료를 슬퍼하는 글이지만
마지막 3분의 1은 자기 포크와 곧 나올 다른 프로젝트 EOL의 소개다.
Webb은 Deno 위에서 사업을 만들고 있다고 밝히므로,
Deno의 종료는 그에게 감정의 문제가 아니라 공급망의 문제다.
포크를 선언하는 것은 의존하던 기반이 사라지기
전에 통제권을 확보하려는 선택으로 읽힌다.
이는 이 문서의 해석이다.

### 무엇이 끝났는지를 정확히 보면 죽었다는 말과 다르다

Deno 측 발표는 Deno 팀 전체가 Cloudflare에 합류한다고 밝힌다.
Deno 런타임은 1년 동안 한 달 단위 릴리스로 버그와 보안 수정을 지원하고,
그 뒤 개발을 끝내되 오픈소스로 남기며 이어받을 사람을 환영한다.
Deno Deploy는 6개월 뒤 운영을 멈추고,
JSR은 인프라를 Cloudflare로 옮겨 계속 운영하며,
rusty_v8은 계속 지원하면서 Cloudflare의 workerd로 통합하는 일을 추진한다.[^deno]
Webb이 Dahl의 것이라고
인용한 HN 댓글(작성자 rough-sea)도 Deno가 MIT 라이선스로 남는다고
했다.[^rough-sea]
그러니 즉시 사라지는 것은 없고 일정이 정해진 것이다.
Webb이 죽었다고 쓴 것은 개발 주체가 1년 뒤 떠난다는 사실에 대한 수사다.

### Node 호환성은 채택의 열쇠이면서 포기의 이유였다

Dahl의 설명에서 Node 호환은 Deno를 Node와 똑같이 행동하도록 묶은 힘이다.
Webb의 반응은 채택을 위해 한 일이었어도 해결할 수 있는 문제였다는 것이다.
Lobste.rs에서 스스로 그 시기의 Deno 직원이었다고
밝힌 lilac은 이 전환이 투자자보다는 Bun이 주목을 가져간 데서
비롯됐다고 증언했다.[^lilac]
반면 skykanin은 Node 호환을 구현한 것이 잘못이고
Ende가 빼는 것이 옳다고 봤다.[^skykanin]

Node 호환을 빼는 선택은 방향이 분명한 만큼 대가도 분명하다.
moltonel은 Node 생태계가 가장 큰 판매 포인트라서
호환을 없애면 많은 사용자에게 덜 매력적이라고 했다.[^moltonel]
bakkot은 WinterTC 같은 명세가 있지만 웹에도 있는 기능만 다루고
`node:fs`나 `node:http`는 포함하지 않으며,
많은 패키지가 Node만을 겨냥하는 상황이 예전 IE와 같은 문제라고
설명했다.[^bakkot]
ar-nelson은 포크와 호환 제거가 겹치면 Ende에서
쓸 수 있는 라이브러리를 찾기가 더 어려워져
진행 중인 프로젝트를 Node로 옮길 생각이라고 했다.[^ar-nelson]

## 비평

### 글의 근거 두 곳이 사실과 어긋난다

가장 눈에 띄는 오류는 이름이다.
글은 Ende가 Deno의 철자를 뒤섞은 것이라고 하는데,
Deno는 D, E, N, O이고 Ende는 E, N, D, E다.
E가 하나 더 있고 O가 없으므로 철자 뒤섞기가 성립하지 않는다.
Lobste.rs에서 abbe가 어떻게 철자 뒤섞기가 되느냐고
묻자 hjvt는 딸기의 R을 못 세는 수준이면
비슷한 것 아니냐고 비꼬았다.[^abbe][^hjvt]
HN의 goldsteinq는 글을 쓴 사람이 자기 글을 읽지 않은 것이냐고 따졌고,
gilrain은 책임을 새로 지겠다고 선언하는 글에서
부주의가 가장 붉은 신호라고 했다.[^goldsteinq][^gilrain]
Node와 Deno가 철자 뒤섞기라는 앞 문장은 맞다. 오류는 그 다음 한 단계에서 났다.

두 번째는 인용한 분노의 성격이다.
글은 Deno 커뮤니티의 분노가 눈에 띈다며
GitHub 이슈의 글을 최고의 폭주로 소개한다.
그 이슈는 2026년 10월 10일에 올라왔고, 글쓴이는 10월 13일에 이것이 농담이었고
Deno 팀에 행운을 빈다는 수정 글을 남겼다.[^issue]
Webb의 글은 10월 11일이라 그 수정보다 앞이다.
그러니 쓸 때의 오류는 아니지만 지금 읽는 사람에게는 근거가 낡았다.
같은 이슈에는 Deno와 Fresh에 웹 앱을 전부 올렸다거나
회사를 설득해 도입했다는 진지한 불만이 실제로 달렸고,
이 점에서 분노가 있다는 주장 자체는 뒷받침된다.[^issue]
그러나 그 주장을 가장 극적인 조각으로 대표시킨 것은 글의 선택이다.

### 두 번째라는 서사가 연도를 잘못 센다

글은 Gel이 커뮤니티에 넘겨진 것을 2년 전이라고 쓴다.
HN에 Gel이 문을 닫고
팀이 Vercel로 합류한다는 글이 오른 것은 2025년 12월 5일이다.[^gel-hn]
Webb이 글을 쓴 때까지 열 달 정도다.
그가 말한 공식 포크 gelstable/gel은 2026년 1월에 만들어졌고,
그 저장소의 마지막 커밋은 2026년 2월 9일이어서
갱신이 없다는 말은 대체로 맞는다.[^gelstable]
두 사례의 간격이 짧을수록 추세처럼 보이지만, 두 건으로 규칙을 말하기는 어렵다.
기간을 두 배로 부풀린 것은 서사에 도움이 될 뿐 사실을 더하지 않는다.

### 비판의 대상이 곧 자신의 위치다

글은 VC가 지원한 도구가 버려지고 커뮤니티가 넘겨받는다는 이야기에 냉소를 보이며,
넘겨받는 쪽에 기대를 걸지 않는다는 어조를 취한다.
그런데 글의 결론은 자기가 넘겨받는 사람이 되겠다는 것이다.
Lobste.rs에서 wink는 글의 권리 의식 같은 어조가 마음에 들지 않고
떠나는 사람을 탓할 일이 아니라고 했다.[^wink]
ar-nelson은 직접 개발을 이어받겠다는 사람을 두고
권리를 주장한다고 하기는 어렵다고 반박했다.[^ar-nelson]
wink는 나중에 했다는 사실과 할 것이라는 선언은 다르다고 되받았다.[^wink-reply]

이 구분이 중요하다.
이 글에서 Ende는 아직 소개 페이지와 메일링 목록뿐이고,
날짜는 12월의 소프트 론칭이라는 약속이다.
이 문서를 쓴 시점의 ende.sh에는 곧 끝이 온다는
예고와 발표 링크가 있을 뿐이다.[^ende]
같은 시점에 eol.sh에는 낡은 포지에 대한 종말이라는
문구와 곧 공개된다는 말만 있다.[^eol]
HN의 colesantiago는 Ende를 재정적으로 어떻게 뒷받침할 것이고
Deno 사용자가 Bun으로 가지 않겠느냐고 물었다.[^colesantiago]
Lobste.rs의 gkoos는 이 로드맵을 한두 달 뒤에 다시 점검하자며
소프트 론칭이 매우 부드러울 것 같다고 했다.[^gkoos]
선언과 결과 사이를 확인할 방법은 지금은 시간뿐이다.

## 인사이트

### 커뮤니티에 넘겨지는 것은 라이선스와 코드뿐이고 시간과 인프라는 넘겨지지 않는다

Deno 발표가 정리한 것을 보면 넘기는 것과 옮기는 것이 갈린다.
런타임 저장소는 오픈소스로 남지만 Deploy는 6개월 뒤 끝나고,
JSR 인프라는 Cloudflare로 옮겨 가며,
팀은 Cloudflare의 공동 플랫폼에 시간을 쓴다.[^deno]
오픈소스 라이선스가 유지된다는 약속이 지켜져도,
릴리스를 만드는 사람과 CI와 레지스트리와
보안 대응을 맡는 사람은 따로 있어야 한다.

Gel이 그 예를 보여 준다.
gelstable/gel은 별이 78개이고 2026년 1월에
만들어진 뒤 마지막 커밋이 2월 9일이다.[^gelstable]
코드는 남았지만 관리하는 사람의 시간이 따라오지 않았다.
이 때문에 의존 위험을 평가할 때 라이선스보다 먼저 물어야 할 것은
누가 CI와 릴리스 서명과 보안 수정에 시간을 쓰는지다.
Lobste.rs의 ale는 서버를 직접 운영한다면 바이너리 버전을 고정해 계속 쓰면 되고
Deploy를 전부 올린 개발자가 진짜 패자라고 했다.[^ale]
이 말은 런타임과 호스팅 서비스의 위험이 같지 않다는 점을 짚는다.
런타임은 고정할 수 있지만 보안 수정이 없으면 시간이 갈수록 부담이 커진다.

### 포크가 성공하려면 한 사람의 의지가 아니라 연합이 필요하다는 것이 오래된 패턴이다

이 문서의 비유로, 런타임 포크가 살아남은 대표 사례는 2014년의 io.js다.
Node의 운영 방식에 불만을 가진 기여자들이 나눠 나왔다가
1년 뒤 재단 아래 Node와 합쳐졌다.
이는 일반적으로 알려진 경과이고 이 문서가 따로 확인하지는 않았다.
핵심은 그 포크에 개인의 의지가 아니라 다수의
기여자와 조직의 지지가 있었다는 점이다.

Ende는 소개 글 한 편과 개인의 선언에서 출발한다.
같은 이슈에는 커뮤니티가 별도 서버를 만들어 앞으로의 방향을 논의하고
있다는 댓글이 달렸다.[^issue]
그 논의가 Ende로 모일지, 다른 포크로 갈라질지는 이 글만으로 예측할 수 없다.
Lobste.rs의 andrewrk는 자유 소프트웨어의 힘을 보여 준다고 평가하면서도
Node를 다시 배우는 데 10분이면 된다며
이 포크의 쓸모를 못 보겠다고 했다.[^andrewrk]

### 포크의 차별점이 곧 사용자를 좁히는 조건이다

Ende는 Node 호환을 빼고 로드맵을 권한과 샌드박스에 맞춘다.
이것은 Deno가 Node 호환으로 향하며 희생한 방향으로 되돌아가는 것이다.
Lobste.rs의 chenghiz는 모듈별 권한과 신뢰할 수 없는 코드를 위한 샌드박스가
npm 생태계의 보안 약점을 생각하면 쓸 만한 큰 이유라고 했다.[^chenghiz]
zem은 원칙 때문에 호환을 깨는 것이었다면
채택 수치와 상관없이 계속 만드는 것이 맞고
이제는 LLM이 호환 라이브러리의 빈틈을 채울 수 있다고 했다.[^zem]

여기에는 긴장이 있다.
Dahl이 Node 호환을 중력의 우물이라고
부른 것은 그것이 채택과 같은 힘이기 때문이다.
호환을 버리면 중력에서 벗어나지만 사용자가 올라탈 발판도 사라진다.
Ende가 약속하는 가치인 권한과 샌드박스는 이미
쓸 수 있는 라이브러리가 있을 때 의미가 크고,
라이브러리가 없으면 안전한 런타임 위에서 직접 모든 것을 만들어야 한다.
dsh가 직장에서 Node 호환 때문에 Bun으로 옮겼다고
한 것은 이 긴장의 한쪽 끝이다.[^dsh]
Webb은 자기 API와 사업을 이미 이 런타임 위에 두었으므로
이 대가를 알고 있을 것이다.
그러나 그의 선택이 다른 사용자에게도 같은 계산이 될지는 열려 있다.

---

[^deno]: Deno, [Deno is joining Cloudflare | Deno](https://deno.com/blog/cloudflare), 2026-10-09

[^rough-sea]: <https://news.ycombinator.com/item?id=50023277>

[^issue]: GitHub, [I am new to Deno and I have LOTS to say](https://github.com/denoland/deno/issues/37004), 2026-10-10

[^gel-hn]: Hacker News, [Gel (ex EdgeDB) shutting down, team joins Vercel](https://news.ycombinator.com/item?id=46168814), 2025-12-05

[^gelstable]: GitHub, [gelstable/gel](https://github.com/gelstable/gel)

[^ende]: Ende, [Ende](https://ende.sh)

[^eol]: EOL, [EOL](https://eol.sh)

[^abbe]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_zrrcog>

[^hjvt]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_jgitog>

[^goldsteinq]: <https://news.ycombinator.com/item?id=50163385>

[^gilrain]: <https://news.ycombinator.com/item?id=50168056>

[^wink]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_u3utla>

[^ar-nelson]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_02cil6>

[^wink-reply]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_giiiav>

[^colesantiago]: <https://news.ycombinator.com/item?id=50158336>

[^gkoos]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_qp5ftp>

[^lilac]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_yj6w7c>

[^skykanin]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_5jlsdw>

[^moltonel]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_o4gvxp>

[^bakkot]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_hbig12>

[^ale]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_fnw8sf>

[^andrewrk]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_fno0dc>

[^chenghiz]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_sxqidc>

[^zem]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_bxb0f1>

[^dsh]: <https://lobste.rs/s/8ejwsp/beginning_ende_community_deno_fork#c_txxofd>
