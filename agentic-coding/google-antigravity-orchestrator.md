# Antigravity의 Orchestrator는 한 작업 안에서 Carbon과 Hydrogen을 오가게 하지만, 검증되지 않은 절감 수치와 구독 제한이 따라온다

원문: [Gemini 4 Hydrogen and Orchestrator](https://antigravity.google/blog/gemini-4-hydrogen-in-google-antigravity/)

HN 토론: <https://news.ycombinator.com/item?id=50472260> (420점, 115개 댓글)

GN 토론: <https://news.hada.io/topic?id=37077>

## 요약

Google Antigravity 팀이 2026년 11월 12일에 올린 3분짜리 블로그 글이다.
Gemini 4 Hydrogen을 Antigravity에 넣으면서, 모델 선택기에 Orchestrator라는 새 항목을 함께 내놓았다고 밝힌다.
Orchestrator는 Hydrogen을 가장 강한 장기 작업용 모델과 묶어 품질과 효율과 지연의 균형을 맞추는 선택지이다.

### 정적 라우터에 대한 비판

글은 업계에서 흔한 정적 모델 라우터를 먼저 비판한다.
첫 프롬프트만 보고 작업 난이도를 짐작해, 충분히 해낼 수 있는 가장 싼 모델에 작업 전체를 보내는 방식이다.
에이전트가 오래 도는 작업에서는 단계마다 필요한 복잡도가 다르고 그것이 진행하면서 드러나기 때문에 이 방식이 무너진다고 한다.

### 양방향으로 오가는 방식

Orchestrator는 한 궤적(trajectory) 안에서 Carbon과 Hydrogen 사이를 동적이고 양방향으로 오간다.
예로 든 흐름은 이렇다.
Carbon이 읽기 전용 단계에서 의존성을 탐색하고 모호함을 풀고 다시 계획할 조건이 명시된 구체적 계획을 세운다.
Hydrogen이 넘겨받아 수정을 쓰고 패키지를 올리고 테스트를 돌린다.
Hydrogen이 막히면 Carbon에게 되돌려 상태를 살피고 계획을 고친 뒤 이어 간다.
글은 이렇게 하면 Carbon에 가까운 작업 성공률을 내면서 더 빠르고 쿼터 효율이 높다고 말한다.
Terminal-Bench 4.1에서 평균 쿼터를 24% 덜 쓰고 19% 빨랐다고 한다.

프로그램으로 모델 역할을 직접 정하고 싶으면 Antigravity SDK로 Hydrogen과 Carbon을 연결할 수 있다.
예시는 오픈소스 이슈 분류 시스템이다.
Hydrogen 에이전트가 분류와 코딩을 맡고 Carbon 에이전트가 큰 리팩터링과 새 기능과 보안 점검을 맡는다.

### 제공 범위

Orchestrator는 Google AI Ultra 구독자에게 Orchestrator (Carbon)과 Orchestrator (Argon)으로,
유료 Google AI Pro 구독자에게 Orchestrator (Argon)으로 나간다.
기업은 Gemini for business에서 둘 다 쓸 수 있다.
Hydrogen 자체는 유료 Pro와 Ultra 구독자에게 나간다.
글은 이번 주 초에 나온 Carbon과 병렬 에이전트 팀을 위한 `/swarm` 기능으로 며칠 사이 수만 개의 스웜이 시작되었다고도 밝힌다.

## 분석

### 중심 주장은 모델 선택을 사람에서 시스템으로 옮긴다는 것이다

글의 논점은 단순하다.
모델 선택을 사람이 매번 하거나 첫 프롬프트로 한 번 고정하는 대신, 작업의 진행에 따라 시스템이 바꾸자는 것이다.
이 주장의 강점은 에이전트 작업의 비용이 균일하지 않다는 관찰이다.
탐색과 계획은 비싼 판단이 필요하고, 편집과 테스트 실행은 싼 실행이 필요하다.
같은 세션 안에서 둘을 오가면 이론상 비싼 모델은 필요한 때에만 쓰인다.

### 이 구조는 이미 다른 곳에서 쓰이는 패턴이다

HN의 한 댓글은 이것이 Anthropic의 advisor 모드와 GitHub의 다중 모델 파이프라인과 본질적으로 같다고 본다.
그러면서 어떻게 캐싱이 되는지 이해하지 못하겠다고 한다.[^vegard]
답글은 advisor는 전체 컨텍스트를 다른 모델로 보내되 출력 토큰이 적어 비용이 줄어드는 반면,
Orchestrator는 필요에 따라 하위 에이전트에 자동으로 일을 위임하는 것으로 보인다고 구분한다.[^jeremy]
차이는 실행 단위이다.
advisor는 한 모델이 가끔 조언을 구하는 구조이고, Orchestrator는 작업 단계마다 주도 모델이 바뀌는 구조로 읽힌다.

## 비평

### 절감 수치의 근거가 약하다

글의 핵심 수치는 쿼터 24% 절감과 속도 19% 개선이다.
HN의 한 댓글은 공동 학습한 모델과 전용 하네스 지원까지 갖추고도 25% 절감이라는 점이 놀랍다고 했다.
자신의 도구는 Opus와 DeepSeek Flash를 ACP로 이어 60% 절감을 본다는 것이다.[^jbellis]
이 비교는 서로 다른 작업과 모델의 수치를 나란히 놓은 것이어서 직접 비교는 안 된다.
다만 이 글의 절감이 크지 않다는 인상을 준다.
같은 날 나온 Hydrogen 발표 글은 같은 Orchestrator 수치를 Terminal-Bench 4.0 기준이라고 적었고,
이 글은 4.1 기준이라고 적었다.
어느 쪽이 맞는지 이 문서가 확인하지 못했다.

### 모델이 난이도를 스스로 판단하는 것에 대한 신뢰 문제가 있다

한 사용자는 하위 에이전트를 쓰되 구현 에이전트는 Carbon으로 고정하고 하위 에이전트마다 문제의 복잡도에 맞는 모델을 직접 정한다고 한다.
모델이 자기 능력에 낙관적이라서 그 권한을 위임하기가 불안하다는 것이다.[^fuussssip]
Orchestrator가 Carbon을 되돌릴 시점을 어떻게 판단하는지는 글에 없다.
글은 막히면 되돌린다고만 쓴다.
막혔다는 것을 Hydrogen이 알아차리지 못하고 틀린 길로 계속 가면 이 구조의 이점이 사라진다.

### 구독 제한이 가치를 깎는다는 불만이 있다

한 댓글은 쿼터를 아끼는 것 말고는 이 구조를 쓸 이유가 없는데 Antigravity의 가성비가 나빠서 Claude Opus나 GPT Sol만 쓰는 편이 낫다고 했다.[^pietz]
다른 댓글은 Pro 토큰을 4분 만에 다 쓴 적이 있다며 Pro 계정으로 쓸 수 있는지 물었고,
답글은 Pro에서도 Hydrogen이 3.8 Flash를 대체해 보인다고 했다.[^threecheese][^trvz]
Orchestrator가 Pro에는 Argon 조합만 열린다는 글의 설명과 함께 읽으면,
가장 강한 조합은 Ultra에 한정된다.
한 사용자는 몇 달 전 이 제품을 써 보고 크레딧이 남았는데도 취소했다고 했다.[^brickers]

### 사용 경험과 이름에 대한 불만이 반복된다

글이 올라온 페이지가 스크롤을 건드려 느리고 불편하다는 불만이 여러 개 있었다.[^timshel]
이름 체계는 다시 도마에 올랐다.
이 스레드에서도 이름이 혼란스럽다는 댓글이 여러 개 달렸고,[^gunalx]
한 사용자는 어느 모델이 더 나은지 트위터 유출로만 알았다고 했다.[^winstonp]
Hydrogen 발표 글과 같은 불만이므로 그 문서에서 다룬 내용을 반복하지 않는다.

## 인사이트

### 라우팅은 처음이 아니라 중간에 일어나야 한다는 주장이 이 글의 가장 쓸 만한 부분이다

정적 라우터가 첫 프롬프트로 난이도를 짐작한다는 비판은 설득력이 있다.
에이전트의 난이도는 작업 중에 드러난다.
그래서 모델 전환의 트리거가 되는 것은 입력이 아니라 상태, 곧 실패와 막힘이다.
이를 직접 구현하려는 사람은 전환 조건을 명시적으로 둘 수 있다.
글이 말하는 명시적 재계획 조건(re-planning triggers)이 그 부분이다.
이 설계는 모델 이름과 무관하게 옮겨 쓸 수 있는 아이디어이다.

### 비용 비교는 같은 작업 위에서 해야 한다

HN 댓글이 갈린 이유는 서로 다른 작업과 구성을 비교하기 때문이다.
Orchestrator의 절감 수치는 Carbon 단독과의 비교이고, 다른 도구의 60%는 다른 쌍의 비교이다.
자기 작업에서 모델 쌍을 바꾸는 효과를 보려면 같은 작업 묶음을 단독과 조합으로 돌려 성공률과 쿼터와 시간을 함께 재야 한다.
한 사용자의 보고처럼 더 똑똑한 모델이 토큰을 덜 써 총사용량이 오히려 줄 수도 있다.[^sanex]
단가가 아니라 작업당 총량으로 비교해야 하는 이유이다.

### 확인할 관찰

이 글의 주장이 옳다면 사용자의 실제 작업에서 Orchestrator가 Carbon 단독의 성공률에 가깝고 쿼터를 줄여야 한다.
반대로 되돌림이 늦어 실패가 늘거나, 쿼터 절감이 작업 종류에 따라 사라지면 주장은 약해진다.
독립 측정과 Pro 구독자의 실사용 후기가 다음 증거이다.

---

[^vegard]: <https://news.ycombinator.com/item?id=50473254>

[^jeremy]: <https://news.ycombinator.com/item?id=50474394>

[^jbellis]: <https://news.ycombinator.com/item?id=50475941>

[^fuussssip]: <https://news.ycombinator.com/item?id=50473078>

[^pietz]: <https://news.ycombinator.com/item?id=50473339>

[^threecheese]: <https://news.ycombinator.com/item?id=50473982>

[^trvz]: <https://news.ycombinator.com/item?id=50475119>

[^brickers]: <https://news.ycombinator.com/item?id=50479951>

[^timshel]: <https://news.ycombinator.com/item?id=50475142>

[^gunalx]: <https://news.ycombinator.com/item?id=50476827>

[^winstonp]: <https://news.ycombinator.com/item?id=50473746>

[^sanex]: <https://news.ycombinator.com/item?id=50476919>
