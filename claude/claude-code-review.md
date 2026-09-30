# Claude Code Review: 리뷰가 병목이 되자 에이전트 팀을 모든 PR에 보낸다

원문: [Code Review for Claude Code | Claude by Anthropic](https://claude.com/blog/code-review)

HN 토론: <https://news.ycombinator.com/item?id=47313787> (83점, 48개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/5qthvu/code_review_for_claude_code> (2점, 7개 댓글)

GN 토론: <https://news.hada.io/topic?id=27362>

## 요약

Anthropic이 2026년 3월 9일 Claude Code의 Code Review를 발표했다.
본문 제목은 Bringing Code Review to Claude Code이고, 모든 PR에 에이전트 팀을 보내 대충 훑는 리뷰가 놓치는 버그를 잡으며, 속도가 아니라 깊이를 위해 만들었다고 소개한다.
Anthropic의 거의 모든 PR에서 돌리는 시스템이고, Team과 Enterprise에 연구 프리뷰로 제공된다.
페이지 제목 아래의 부제는 세 가지 흔한 워크플로 패턴으로 에이전트 작업을 구성하는 실무 지침이라고 적혀 있어 본문과 맞지 않는데, 다른 글의 부제가 들어간 것으로 보인다.

배경은 리뷰 병목이다.
Anthropic 엔지니어 한 사람당 코드 산출량이 지난 1년 동안 200% 늘었고, 코드 리뷰가 병목이 되었다.
고객들도 매주 같은 이야기를 한다고 한다.
개발자는 여유가 없고, 많은 PR이 깊이 읽히지 못하고 훑어지기만 한다.
그래서 모든 PR에 믿을 수 있는 리뷰어가 필요했다는 것이다.
Code Review는 오픈소스로 계속 제공되는 기존 Claude Code GitHub Action보다 더 철저하고 더 비싼 선택지다.

Anthropic 안에서는 전에는 PR의 16%가 실질적인 리뷰 코멘트를 받았는데 지금은 54%가 받는다.
Code Review는 PR을 승인하지 않고, 승인은 여전히 사람의 판단이다.
PR이 열리면 에이전트 팀이 병렬로 버그를 찾고, 거짓 양성을 걸러 내려고 버그를 검증하고, 심각도로 순위를 매긴다.
결과는 PR에 신호가 높은 개요 코멘트 하나와 특정 버그에 대한 인라인 코멘트로 올라온다.
리뷰는 PR 크기에 맞춰 커져, 크거나 복잡한 변경에는 더 많은 에이전트와 더 깊은 읽기가, 사소한 변경에는 가벼운 통과가 붙고, 평균 리뷰는 약 20분 걸린다.

내부에서 몇 달 돌린 결과, 1,000줄 넘게 바뀐 큰 PR의 84%에서 평균 7.5개의 발견 사항이 나왔고, 50줄 미만의 작은 PR에서는 31%, 평균 0.5개였다.
엔지니어들은 발견 사항에 대부분 동의했고, 틀렸다고 표시된 것은 1% 미만이다.
사례도 둘 든다.
프로덕션 서비스의 한 줄 변경이 평범해 보였지만 Code Review는 그것을 치명적이라고 표시했고, 실제로 서비스의 인증을 깨뜨렸을 변경이었다.
엔지니어는 나중에 혼자서는 못 잡았을 것이라고 말했다.
TrueNAS 오픈소스 미들웨어의 ZFS 암호화 리팩터링에서는 PR이 건드린 인접 코드의 기존 버그, 즉 동기화할 때마다 암호화 키 캐시를 조용히 지우던 타입 불일치를 찾아냈다.

비용은 토큰 사용량으로 청구되고, 리뷰당 평균 15~25달러이며 PR 크기와 복잡도에 따라 늘어난다.
관리자는 조직의 월간 총지출 한도, 저장소별 활성화, 리뷰한 PR 수와 수용률과 총비용을 보여 주는 분석 대시보드로 통제할 수 있다.
관리자가 Claude Code 설정에서 켜고 GitHub 앱을 설치하고 저장소를 고르면, 개발자 쪽에서는 설정 없이 새 PR마다 리뷰가 자동으로 돈다.

## 분석

### 산출량이 늘자 병목이 리뷰로 옮겨 갔다

발표의 첫 숫자가 논리 전체를 떠받친다.
엔지니어 한 사람당 코드 산출량이 200% 늘었다는 것은, 같은 수의 사람이 세 배의 코드를 리뷰해야 한다는 뜻이다.
코드를 쓰는 속도는 에이전트가 올렸지만, 읽는 속도는 그대로였다.

이것은 에이전트 개발에서 반복되는 패턴이다.
구현이 싸지면 병목은 구현 주변, 특히 사람이 판단해야 하는 곳으로 옮겨 간다.
Neil Kakkar가 에이전트 다섯 개를 돌리며 리뷰를 병목 목록에서 빠뜨린 것(`agentic-coding/its-the-infrastructure-not-the-ai.md`), OpenAI가 DevDay에서 Codex가 먼저 검토하는 자동 리뷰를 내놓은 것(`openai/devday-2026.md`)도 같은 병목에 대한 반응이다.
Anthropic은 그 병목에 에이전트를 한 번 더 넣는 것으로 답했다.

### 사람의 리뷰를 대신하는 것이 아니라 덮개를 넓히는 설계다

발표는 Code Review가 PR을 승인하지 않는다고 분명히 한다.
16%에서 54%로 늘었다는 숫자도 사람이 리뷰하는 PR의 비율이 아니라 실질적 코멘트를 받은 PR의 비율이다.
목표는 사람의 판단을 없애는 것이 아니라, 사람이 훑고 지나가던 PR에도 누군가 깊이 읽은 흔적을 남기는 것이다.

Lobste.rs에서 mcherm은 AI가 리뷰를 하는 것과 리뷰에 기여하는 것을 구분했다.[^mcherm]
AI가 잠재적 문제를 짚기만 한다면 사람의 리뷰를 빼앗는 것이 아니라 보강할 수 있다는 것이다.
reivilibre는 이것을 사전 리뷰(pre-review)라고 부르며, 사람이 잘 못 보는 것을 먼저 걸러 동료의 소중한 주의력을 리뷰의 흥미로운 부분에 쓰게 한다고 적었다.[^reivilibre]
뻔한 실수가 리뷰 기록에 남아 있기만 해도 주의를 흩뜨려 더 흥미로운 지점을 놓치게 한다는 주장도 덧붙였다.

### 병렬 탐색, 검증, 순위의 세 단계가 거짓 양성을 겨냥한다

작동 방식의 세 단계는 각각 AI 리뷰의 알려진 약점을 겨냥한다.
여러 에이전트가 병렬로 버그를 찾는 것은 한 번의 읽기가 놓치는 것을 줄이고, 각 버그를 검증하는 단계는 거짓 양성을 걸러 내고, 심각도 순위는 사람이 무엇부터 볼지 정하게 한다.
틀렸다고 표시된 발견이 1% 미만이라는 숫자는 이 가운데 검증 단계의 효과를 주장한다.

HN의 여러 사용자가 이 설계가 풀려는 문제를 겪었다고 증언했다.
jgraettinger1은 Claude나 Codex에게 이미 자기가 리뷰한 작업을 다시 리뷰시키면 늘 여덟 개쯤의 문제를 찾아내고, 결함을 정말 못 찾으면 좀 이상해진다고 적었다.[^jgraettinger1]
denisdev1도 작거나 아주 깨끗한 변경에서도 제안 목록이 나오므로 신호와 잡음을 거르는 것이 작업의 일부가 된다고 했다.[^denisdev1]
작은 PR에서 발견 비율이 31%로 떨어진다는 발표의 숫자는, 이 도구가 아무 문제 없는 PR에는 아무것도 말하지 않을 수 있다는 주장이기도 하다.

## 비평

### 발견 비율은 버그의 기저율 없이 해석할 수 없다

HN에서 Kuxe는 사람이 1,000줄짜리 PR과 50줄짜리 PR에 버그를 몇 개나 넣느냐고 물었다.[^Kuxe]
84%의 큰 PR에서 7.5개가 나왔다는 숫자는 그 기저율과 비교해야 의미가 생긴다.
큰 PR에 실제 버그가 평균 10개 있다면 이 도구는 대부분을 잡는 것이고, 평균 2개라면 나머지 5.5개는 무엇인지 물어야 한다.

xlii는 이 숫자를 읽으면 큰 PR의 84%가 크게 결함이 있다는 뜻이 되느냐고 되물었다.[^xlii]
발표는 발견 사항을 버그라고 부르지만, 그 안에는 치명적인 인증 오류부터 사소한 개선 제안까지 섞여 있을 수 있다.
심각도별 분포가 없으면, 틀렸다고 표시된 것이 1% 미만이라는 숫자도 해석하기 어렵다.
틀리지는 않았지만 중요하지도 않은 발견은 그 1%에 들어가지 않기 때문이다.

그리고 이 숫자는 Anthropic 내부의 것이다.
엔지니어가 틀렸다고 표시하는 비율은, 자기 회사의 도구에 반대 표시를 하는 데 드는 사회적 비용에도 영향을 받는다.
외부 고객의 수용률이 대시보드에 나온다고 했으니, 그 숫자가 공개될 때 비로소 비교할 수 있다.

### 리뷰당 15~25달러는 규모에서 전혀 다른 숫자가 된다

CharlesW가 짚은 비용 문장에 대해 cbovis는 GitHub Copilot Code Review가 구독에 포함된 크레딧을 넘기면 리뷰당 4센트라며 이 비용은 놀랍다고 적었다.[^cbovis]
raflueder는 직접 만든 리뷰 워크플로로 200개 넘는 PR을 두 번씩 돌려 리뷰당 약 4센트, 총 19.50달러가 들었다고 공유했다.[^raflueder]
SkyPuncher는 반대로 시니어 엔지니어가 시간당 100달러 넘게 버니 이것은 그들의 15분어치에 불과하고, 한 시간 걸릴 리뷰를 10분에 하게 해 준다면 쉽게 팔린다고 했다.[^SkyPuncher]

nnennahacks는 그 계산이 많은 것을 얼버무린다고 반박했다.[^nnennahacks]
주당 PR 2,000개를 내는 회사라면 리뷰 비용이 주당 3만~5만 달러, 연간 150만~250만 달러가 된다는 것이다.
시니어 엔지니어보다 싸다는 비교는 리뷰 한 건에서는 맞지만, 모든 PR에 자동으로 돈다는 설계에서는 연간 예산 항목이 된다.
발표가 관리자 통제 수단을 세 가지나 드는 것은 이 비용이 통제가 필요한 규모라는 것을 인정하는 셈이다.

lowsong은 이것이 사용자를 끌기 위한 보조금 가격이고 열 배가 될 수도 있으며, 코드를 쓰는 회사가 그 코드를 고치는 비용도 받는 뒤틀린 유인이 있다고 경고했다.[^lowsong]
nemo44x의 농담, 버그 있는 코드를 주고 그걸 고치는 데 돈을 받는 사업 모델이냐는 말도 같은 지점을 찌른다.[^nemo44x]
코드 산출량이 200% 늘어서 리뷰가 필요해졌다면, 그 산출량의 상당 부분을 만든 것도 같은 회사의 도구다.
GeekNews에서 bluekai17은 비용만 낮춘다면 좋겠다고 적었고,[^bluekai17] tested는 개인 요금제는 지원하지 않는다며 나중에도 안 될지 물었다.[^tested]

### 사례의 선택이 도구의 강점을 과장한다

karmakaze는 예시가 이상하다며, 경계 사례가 아니었다면 인증을 깨뜨리는 버그는 스모크 테스트에서도 잡혔을 것이라고 적었다.[^karmakaze]
한 줄 변경이 서비스의 인증을 깨뜨렸다면, 그것은 리뷰의 실패이기 전에 테스트의 부재다.
AI 리뷰가 그것을 잡았다는 것은 인상적이지만, 그 사례가 보여 주는 가장 큰 교훈은 인증 경로에 대한 자동 테스트가 없었다는 것일 수 있다.

TrueNAS 사례는 더 설득력 있다.
PR이 건드린 인접 코드의 기존 버그는 사람 리뷰어가 변경 집합을 훑으며 찾아보지 않는 종류이고, 발표도 그렇게 설명한다.
하지만 이것 역시 PR 리뷰라기보다 코드베이스 감사에 가까운 발견이다.
이런 발견이 리뷰마다 나온다면, 그 가치는 PR을 통과시키는 속도보다 기존 코드의 건강을 점검하는 데 있다.

## 인사이트

### 리뷰의 목적이 품질 확인에서 지식 전파로 드러난다

Lobste.rs에서 marginalia는 AI에게 실제 코드 리뷰를 맡기는 것이 꽤 카고 컬트처럼 보인다고 적었다.[^marginalia]
코드 리뷰의 가장 중요한 목적 가운데 하나가 변경과 시스템에 대한 이해를 팀원 사이에 퍼뜨리는 것이기 때문이다.
AI가 변경을 훑어보기만 원한다면, 커밋 전에 `CLAUDE.md`에 완료 기준 목록을 두고 고치면 되지 않느냐고 물었다.

이 반론은 AI 리뷰가 리뷰의 절반만 대신한다는 것을 보여 준다.
버그를 찾는 절반은 기계가 더 잘할 수 있다.
누가 이 코드를 알고 있는지, 이 변경이 왜 필요했는지, 다음에 이 부분을 누가 고칠 수 있는지를 퍼뜨리는 절반은 사람이 읽을 때만 일어난다.
Code Review가 사람의 리뷰를 보강한다고 강조한 것은 옳지만, 리뷰가 병목이라서 도입된 도구가 결국 사람이 덜 읽게 만든다면, 버그는 줄어도 팀의 공유된 이해는 얇아진다.

### 같은 계열의 모델이 쓰고 같은 계열의 모델이 검토하는 문제

nolanl은 AI가 AI가 쓴 PR을 리뷰한다는 개념이 완전히 틀려 보인다며, 왜 처음부터 맞는 코드를 쓰지 않느냐고 물었다.[^nolanl]
raflueder는 생성된 코드는 원하는 것을 처음 설명한 만큼만 좋고, 사람이 먼저 한 번 풀고 다듬는 것과 다르지 않다고 답했다.[^raflueder-2]

두 입장 사이에 구조적 질문이 남는다.
같은 계열의 모델이 코드를 쓰고 같은 계열의 모델이 그것을 검토하면, 두 모델이 공유하는 맹점은 어느 쪽에서도 잡히지 않는다.
higheun이 생산 세션과 리뷰 세션의 맥락을 분리하면 LLM 리뷰 품질이 좋아진다는 실험을 소개한 것처럼,[^higheun] 맥락을 나누는 것은 도움이 되지만 학습된 경향까지 나누지는 못한다.
GeekNews의 princox는 Claude로 코드를 생성하고 Claude로 코드를 리뷰한다고 한 줄로 요약했다.[^princox]
그래서 AI 리뷰의 가치는 다른 모델, 다른 도구, 그리고 사람의 리뷰가 섞일 때 가장 크다.
toniantunovi가 결정론적 도구, 즉 린터와 정적 분석과 의존성 검사가 잘하는 것은 그것에 맡기라고 권한 것도 같은 방향이다.[^toniantunovi]

### 리뷰가 제품이 되면 리뷰 도구 시장이 모델 회사 안으로 들어온다

Bnjoroge는 최근 높은 가치로 투자받은 수십 개의 코드 리뷰 플랫폼에는 무슨 의미냐고 물었고,[^Bnjoroge] satvikpendem은 API 위에 만들었다가 API 제공자가 기본 기능으로 넣자 쓸모없어진 다른 회사들과 같을 것이라고 답했다.[^satvikpendem]
GeekNews에서 xguru는 개발 도구를 개선하면서 그것으로 자기네 개발 자체도 빠르게 만드는 플라이휠이 완성된 듯하다고 봤다.[^xguru]
lbreakjai는 리뷰당 15~25달러라면 경쟁할 여지가 여전히 많고, 맞는 하네스가 맞는 모델보다 더 큰 차이를 만드는 것 같으며, 진짜 경쟁자는 같은 코드에 로컬로 도는 스킬이라고 봤다.[^lbreakjai]

이 논쟁은 코드 리뷰가 어디에 자리 잡을지를 묻는다.
모델 회사의 관리형 서비스는 설정이 없고 깊지만 비싸다.
로컬 스킬과 GitHub Action은 싸고 자유롭지만 설정과 유지가 필요하다.
Lobste.rs에서 MaskRay가 LLVM 패치 2,200개 넘게 리뷰해 온 경험을 바탕으로 `review-patch` 명령을 만들어 쓰되 기술적 판단은 스스로 한다고 적은 것처럼,[^MaskRay] 가장 숙련된 리뷰어는 이미 자기 도구를 만들고 있다.
관리형 리뷰가 이길 곳은 그런 도구를 만들 여력이 없는 팀이고, 그곳에서는 가격이 가장 큰 결정 요인이 된다.

### 리뷰를 언제 부르는지도 설계의 일부다

jbranchaud는 트리거 옵션이 PR을 열 때와 푸시할 때마다 두 가지뿐인 것이 이상하고, 자기 PR은 만들자마자 이런 리뷰를 받을 준비가 된 경우가 드물어 댓글로 직접 부르고 싶다고 적었다.[^jbranchaud]
st3fan은 초안 PR을 만들면 되지 않느냐고 답했다.[^st3fan]

작은 논쟁이지만, 자동 리뷰가 개발 흐름의 어디에 끼어드는지를 보여 준다.
리뷰당 수십 달러가 드는 도구가 푸시마다 돈다면, 개발자는 푸시를 미루거나 여러 변경을 한데 모아 푸시하게 된다.
비용이 도구의 사용 시점을 바꾸고, 사용 시점이 작업 흐름을 바꾼다.
비싼 자동 리뷰는 결국 사람이 준비되었다고 판단한 순간에만 부르는 도구가 될 가능성이 크다.

---

[^mcherm]: <https://lobste.rs/s/5qthvu/code_review_for_claude_code#c_5rn0kf>

[^reivilibre]: <https://lobste.rs/s/5qthvu/code_review_for_claude_code#c_msyhnv>

[^jgraettinger1]: <https://news.ycombinator.com/item?id=47317851>

[^denisdev1]: <https://news.ycombinator.com/item?id=47319842>

[^Kuxe]: <https://news.ycombinator.com/item?id=47317862>

[^xlii]: <https://news.ycombinator.com/item?id=47316367>

[^cbovis]: <https://news.ycombinator.com/item?id=47315256>

[^raflueder]: <https://news.ycombinator.com/item?id=47317279>

[^SkyPuncher]: <https://news.ycombinator.com/item?id=47317287>

[^nnennahacks]: <https://news.ycombinator.com/item?id=47323800>

[^lowsong]: <https://news.ycombinator.com/item?id=47316398>

[^nemo44x]: <https://news.ycombinator.com/item?id=47317497>

[^karmakaze]: <https://news.ycombinator.com/item?id=47314726>

[^marginalia]: <https://lobste.rs/s/5qthvu/code_review_for_claude_code#c_1hamx4>

[^nolanl]: <https://news.ycombinator.com/item?id=47318444>

[^raflueder-2]: <https://news.ycombinator.com/item?id=47318680>

[^higheun]: <https://news.ycombinator.com/item?id=47345440>

[^toniantunovi]: <https://news.ycombinator.com/item?id=47370832>

[^Bnjoroge]: <https://news.ycombinator.com/item?id=47314925>

[^satvikpendem]: <https://news.ycombinator.com/item?id=47315103>

[^lbreakjai]: <https://news.ycombinator.com/item?id=47317131>

[^MaskRay]: <https://lobste.rs/s/5qthvu/code_review_for_claude_code#c_6d9l67>

[^jbranchaud]: <https://lobste.rs/s/5qthvu/code_review_for_claude_code#c_l1ai5w>

[^st3fan]: <https://lobste.rs/s/5qthvu/code_review_for_claude_code#c_bmqgxs>

[^bluekai17]: <https://news.hada.io/topic?id=27362#cid52813>

[^tested]: <https://news.hada.io/topic?id=27362#cid52760>

[^princox]: <https://news.hada.io/topic?id=27362#cid52785>

[^xguru]: <https://news.hada.io/topic?id=27362#cid52751>
