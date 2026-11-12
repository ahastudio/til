# Val Town이 클라우드 컴퓨팅 경쟁에서 이기지 못했다며 서비스를 단계적으로 종료한다

원문: [Val Town is winding down](https://blog.val.town/winding-down)

HN 토론: <https://news.ycombinator.com/item?id=50443427> (418점, 100개 댓글)

GN 토론: <https://news.hada.io/topic?id=36961>

## 요약

Val Town의 Steve Krouse는 2026년 11월 10일 공지에서 회사를 정리하기로 했다고
밝혔다.
그는 사용자들이 큰 믿음으로 이 서비스 위에 무언가를 만들었다고 감사하며, 계속
서비스하지 못해 미안하다고 적는다.
사업 쪽 나쁜 소식, 곧 클라우드 컴퓨팅 분야에서 경쟁하지 못했다는 사실이 이전하는
사용자에게는 좋은 소식이기도 하다고 말한다.
이전할 호스팅 업체가 많고, 요즘 LLM은 이런 이전을 잘 해 주기 때문이라는 것이다.
Cloudflare, Vercel, Netlify, Render로 옮기는 안내서를 마련했고, 도움은 지원
메일이나 Discord로 요청하라고 한다.

과금은 이날 멈추고 기존 구독은 무료로 계속 서비스한다.
연간 요금제를 미리 낸 사람에게는 일부를 환불한다.
종료 일정은 다음과 같다.

| 서비스                             | 종료일                 |
| ---------------------------------- | ---------------------- |
| 신규 가입과 요금제 업그레이드      | 2026년 11월 10일(당일) |
| 읽기 전용 모드(sqlite와 블롭 제외) | 2026년 12월 10일       |
| 그 밖의 모든 서비스                | 2027년 1월 10일        |
| Val Town 오픈소스 공개             | 2027년 2월 1일         |

글은 지난 4년간 일한 팀원 13명을 이름으로 하나씩 부르며 감사하고, 투자자 Dan Levine을
“최고의 투자자”라고 따로 꼽은 뒤 다른 투자자와 사용자들에게 감사하며 끝난다.
공지에는 종료 원인이 경쟁에서 이기지 못했다는 한 문장 외에는 설명되어 있지 않다.

## 분석

### 공지가 말하는 것은 일정이고 원인은 비어 있다

이 글은 무엇이 언제 닫히는지를 정확하게 적지만 왜 실패했는지는 거의 말하지
않는다.
“클라우드 컴퓨팅 분야에서 경쟁하지 못했다”는 한 문장이 전부다.
이 때문에 댓글에서 원인을 추정하는 글이 많았다.
다만 이 추정들은 외부 관찰자의 것이며 공지가 확인한 내용은 아니다.
공지가 확인해 주는 것은 세 가지다.
신규 사용자는 이미 받지 않고, 읽기 전용 모드는 한 달 뒤, 나머지는 두 달 뒤에
닫히며, 코드는 소스로 공개된다는 점이다.

### 오픈소스 공개 약속이 이전의 안전망이다

HN에서 aanet은 성공한 사업이라고 생각했다며 오픈소스가 되기를 바랐고, rhazn과
janpio는 글에 2월 1일 공개가 이미 적혀 있다고 알려 주었다.[^rhazn]
simonw는 Val Town이 아름다운 아이디어의 모음이지만 사람들이 “Val 방식”으로
만들기를 감수해야 하는, 상품화되지 않은 호스팅 위에 지속 가능한 사업을 짓는 일은
극도로 어렵다는 점을 이해한다고 쓰며 2월에 코드를 보기를 기대한다고
했다.[^simonw]
오픈소스 공개 시점이 서비스 종료일보다 뒤라서, 종료 시점부터 공개까지는 자체
호스팅 대안이 없는 공백이 생긴다.
doctoboggan은 그러니 Val Town이 자기 자신의 가장 좋은 자체 호스팅 대안일
것이라고 했고,[^doctoboggan] 다른 사용자들은 windmill.dev와 smallweb.run을
비슷한 대안으로 추천했다.[^rubenfiszel]
[^flymasterv]

## 비평

### 이 사례를 개발자 도구 회사 전체의 추세로 읽기에는 근거가 약하다

hardwaregeek은 Astro, Astral, Deno, Bun, Turso, Void Zero가 모두 인수된 것을
들며 개발자 도구 회사의 한 시대가 끝나는 것 같다고 했다.[^hardwaregeek]
Onavo는 대부분 아직 살아서 활동 중이고 Deno만 예외라고 정정했다.[^Onavo]
swyx는 이것이 정상적인 스타트업 인수합병 주기이고 이 사례를 유독 주의 깊게 봤을
뿐일 수도 있다고 짚었다.[^swyx-1]
인수와 폐업은 다른 사건이므로 이 사례를 개발자 도구 전체의 신호로 확대하는 것은
무리다.
asdev는 최근 종료 공지가 많아 앞으로 더 늘 것이라고 했지만,[^asdev] 어떤
회사들인지는 밝히지 않았다.

### Deno 의존이 원인이라는 추정은 공지에 없다

jrmann100은 공지에 직접 나오지 않지만 Val Town이 근본적으로 Deno 런타임을
중심으로 조직되어 있었고, Deno 팀이 Cloudflare에 합류한 뒤 내년에 이를
유지보수하지 않는다고 썼다.[^jrmann100]
이에 maxmcd는 계획이 있었고 합리적이었다고 하며 제품 저장소의 이슈를
가리켰다.[^maxmcd]
FLeXMurphy는 Deno 같은 플랫폼 위에 지은 것은 진지한 사업보다 부업에 가깝다고
했고,[^FLeXMurphy] antonvs는 경쟁 제품보다 매우 좁은 제품이었고 쉬운 사용이
가치였지만 한계가 많아 이것만으로는 부족해 보인다고 평가했다.[^antonvs]
이 의견들은 모두 외부의 추정이다.
공지는 Deno를 언급하지 않았으므로 어느 것도 종료의 원인으로 확인되지 않았다.

### 제품이 무엇인지 한 줄로 설명되지 않았다는 반응도 있다

Zambyte는 홈페이지를 봐도 무엇인지 모르겠고 에이전트에 호스팅 CLI나 MCP를 주는
것과 어떻게 다른지 물었다.[^Zambyte]
efficax는 Val Town이 LLM 이전에 만들어진 가벼운 타입스크립트 함수 서비스였다고
설명했고,[^efficax] dkmar는 이메일을 보내고 크론으로 예약할 수 있는 작은 웹
스크립트였고 이전에는 무료로 웹 모니터링에 썼다고 했다.[^dkmar]
swyx는 HN에서 지난 몇 년간 꾸준히 높은 순위였다고 반박하며 검색해 보라고
했다.[^swyx-2]
이 글 하나로는 제품 설명이 약해서 사용자가 빠져나갔는지 알 수 없지만, 댓글이
같은 설명을 반복하게 된 것은 사실이다.

## 인사이트

### 개인용 앱의 클라우드가 하네스에 흡수되는 문제가 남는다

alabhyajindal은 개인 애플리케이션용 클라우드라는 아이디어가 시간이 갈수록 의미가
줄어드는 것 같다고 썼다.
장난감 프로젝트를 처음 만들게 해 주는 하네스가 그 시장을 가져가기 때문이며,
Claude가 웹사이트를 배포해 주는 것이 그 예라고 했다.[^alabhyajindal]
공지가 “LLM이 이전을 잘 해 준다”고 쓴 것도 같은 방향이다.
호스팅의 전환 비용이 낮아지면 작은 호스팅의 결합력도 약해진다.
이는 이 문서의 추론이고, 공지가 이를 종료 이유로 밝힌 것은 아니다.

### 종료의 품격을 재는 항목이 일정, 환불, 이전 안내, 소스 공개로 분해된다

이 공지는 신규 가입 중단, 단계적 종료 날짜, 일부 환불, 이전 안내서, 오픈소스
약속을 한꺼번에 제시한다.
samwho는 자신이 만든 서비스가 DDoS를 당해 Val Town이 잠시 내려갔을 때 Steve가
손글씨 쪽지와 모자를 보내 감사를 표했다는 경험을 전했다.[^samwho]
이런 평가는 제품 자체보다 운영 방식에 대한 것이다.
서비스 종료를 알리는 쪽이 사용자에게 줄 수 있는 것은 시간(최소 2개월), 이전
경로, 코드 공개이고, 이 글이 이 셋을 갖춘 점은 사실이다.
다만 환불 대상 범위(연간 요금제 선불자)와 sqlite·블롭 저장소가 읽기 전용에서
제외되는 세부가 사용자별로 어떤 영향을 주는지는 공지만으로는 알 수 없다.

### 결론을 바꿀 관찰

- 2027년 2월 1일에 공개되는 코드로 자체 호스팅이 실제로 가능하다면, 종료 이후
  공백이라는 우려는 줄어든다.
- 종료의 직접 원인이 Deno 런타임 변화였다고 Steve Krouse가 따로 밝힌다면, 위
  추정들 가운데 Deno 의존 쪽이 확인되는 것이다.
- 비슷한 시기에 개인용 앱 호스팅 서비스의 폐업이 이어진다면, 하네스가 시장을
  흡수한다는 해석이 힘을 얻는다.

---

[^rhazn]: <https://news.ycombinator.com/item?id=50443733>

[^simonw]: <https://news.ycombinator.com/item?id=50444320>

[^doctoboggan]: <https://news.ycombinator.com/item?id=50444330>

[^rubenfiszel]: <https://news.ycombinator.com/item?id=50444950>

[^flymasterv]: <https://news.ycombinator.com/item?id=50446836>

[^hardwaregeek]: <https://news.ycombinator.com/item?id=50443988>

[^Onavo]: <https://news.ycombinator.com/item?id=50444305>

[^swyx-1]: <https://news.ycombinator.com/item?id=50445430>

[^asdev]: <https://news.ycombinator.com/item?id=50444353>

[^jrmann100]: <https://news.ycombinator.com/item?id=50443879>

[^maxmcd]: <https://news.ycombinator.com/item?id=50447916>

[^FLeXMurphy]: <https://news.ycombinator.com/item?id=50444148>

[^antonvs]: <https://news.ycombinator.com/item?id=50446393>

[^Zambyte]: <https://news.ycombinator.com/item?id=50444332>

[^efficax]: <https://news.ycombinator.com/item?id=50444386>

[^dkmar]: <https://news.ycombinator.com/item?id=50447806>

[^swyx-2]: <https://news.ycombinator.com/item?id=50445381>

[^alabhyajindal]: <https://news.ycombinator.com/item?id=50444524>

[^samwho]: <https://news.ycombinator.com/item?id=50444412>
