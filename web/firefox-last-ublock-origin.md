# Firefox가 uBlock Origin을 지원하는 마지막 주요 브라우저가 되다

원문: [Firefox is now the last major browser that still supports uBlock Origin](https://www.pcworld.com/article/3212428/firefox-is-now-the-last-major-browser-that-still-supports-ublock-origin.html)

HN 토론: <https://news.ycombinator.com/item?id=49303202> (656점, 249개 댓글)

## 요약

PCWorld의 이 기사(2026년 8월 13일)는 Firefox가 uBlock Origin을 계속 지원하는 유일한 주요
브라우저가 됐다고 전한다.
Firefox는 Bluesky 게시물로 “uBlock Origin에 대한 우리의 지원은 어디로도 가지 않는다”고 밝혔고,
이는 Microsoft Edge가 곧 Manifest V2 아키텍처로 도는 uBlock Origin과 다른 광고 차단 확장을
잠글 것이라는 소식에 대한 응답이다.

Edge가 Manifest V3로 옮겨 가면 광고 차단 확장은 웹 브라우징과 동영상 시청 중 발생하는 광고를
제대로 식별하고 차단하는 데 필요한 기능에 접근할 수 없게 된다.
Microsoft의 움직임은 놀랍지 않다 — Edge는 오늘날 대부분의 웹 브라우저(Opera, Brave, Vivaldi,
Samsung Browser 포함)를 구동하는 오픈소스 엔진 Chromium에 기반하며, Google이 Chrome/Chromium에서
Manifest V2에서 V3로의 이전을 시작했고 Edge가 그 뒤를 따르는 것이다.

그러나 Firefox는 Chromium에 기반하지 않은 몇 안 되는 브라우저 중 하나이고, 이제 uBlock Origin을
여전히 지원하는 유일한 주요 브라우저다.
기사는 다른 두 비Chromium 주요 브라우저인 Safari와 DuckDuckGo 모두 uBlock Origin을 지원하지
않는다고 덧붙인다.

## 분석

### 이 기사의 핵심은 광고 차단이 브라우저 엔진 독점의 인질이 됐다는 것이다

기사가 전하는 사실은 단순하지만 그 구조는 깊다.
uBlock Origin의 운명이 브라우저의 선의가 아니라 브라우저 엔진의 통제권에 달려 있다는 것이다.

이 구조가 중요한 이유는 문제의 뿌리가 확장 자체가 아니라 엔진의 API에 있기 때문이다.
Manifest V3는 광고 차단 확장이 요청을 가로채 차단하는 데 필요한 `webRequestBlocking` 권한을
제거한다.
Chromium이 이 결정을 내리면 그 엔진 위에 세워진 모든 브라우저 — Chrome, Edge, Opera, Brave,
Vivaldi — 가 그 결정을 물려받는다.
Firefox가 예외인 유일한 이유는 그것이 Chromium이 아니라 자체 엔진(Gecko)을 쓰기 때문이며, 이는
광고 차단의 미래가 기술적 문제가 아니라 엔진 다양성의 문제임을 드러낸다.

이 구조를 한 HN 사용자가 확장의 원래 철학으로 되짚었다.
확장은 원래 “브라우저가 하고 싶어 하지 않는 것을 사용자가 하게 해 주는 방법”이었는데, 그 자유가
Google에게는 너무 과했고, 그래서 게이트가 있는 스토어를 만들고 API를 쓸모없게 파괴한 뒤, 그것을
정당화할 이유를 지어내 모두의 반대에도 밀어붙였고, 개구리는 서서히 삶겼다는 것이다[^avaer].
이 재구성이 기사의 사실을 역사적 배신으로 읽는다 — 확장 시스템은 사용자에게 통제권을 주려고
존재했는데, 엔진 소유자가 그 통제권을 회수하는 데 확장 시스템 자체를 이용했다.

### “주요 브라우저”라는 프레임이 기사의 논조를 결정한다

기사가 Firefox를 “마지막 주요 브라우저”로 규정한 것은 사실 서술이 아니라 프레임 선택이다.
Safari와 DuckDuckGo를 “지원하지 않는” 쪽에 넣고 Firefox를 고립된 수호자로 세우는 구도다.

이 프레임이 논조를 만드는 이유는 그것이 위기감을 조성하기 때문이다.
“마지막”이라는 단어는 uBlock Origin이 멸종 위기에 처했고 Firefox가 최후의 보루라는 서사를 만든다.
그러나 이 프레임은 정확하지 않을 수 있다.
한 HN 사용자는 기사가 “그냥 사실이 아니다”라며 반박했다 — Brave는 `brave://settings/extensions/v2`에서
uBlock Origin을 켤 수 있고(Brave가 호스팅하는 버전은 더 낫다), Helium은 uBlock Origin을 사전
설치해 오며, Edge조차 아직 애드온 스토어에 uBlock Origin이 있다는 것이다[^eahm].
이 반박은 “마지막 주요 브라우저”라는 프레임이 Manifest V2의 단계적 폐지를 실제보다 더 임박한
종말로 그린다는 것을 시사한다.

이 프레임의 과장이 기사의 신뢰성 문제를 낳는다.
현실은 이분법 — Firefox만 지원, 나머지는 폐지 — 이 아니라, 여러 Chromium 브라우저가 다양한
방식으로 Manifest V2 예외나 자체 우회를 제공하는 스펙트럼이다.
Brave는 uBlock을 위한 Manifest V2 옵트아웃을 두고[^vovavili], uBlock Origin Lite는 Manifest V3에서도
상당 부분 광고를 차단한다.
기사가 이 스펙트럼을 “Firefox 대 나머지”로 단순화한 것은 위기감을 위한 것이며, 정확한 그림은
훨씬 복잡하다.

### Firefox의 값이 uBlock 지원을 넘어선다는 점을 기사는 놓친다

기사는 Firefox를 uBlock Origin 지원이라는 단일 기능으로 규정하지만, HN 논의는 Firefox의 값이
그 하나가 아니라 브라우저 생태계 전체의 건강에 있음을 드러낸다.

이 관점이 중요한 이유는 uBlock 지원이 원인이 아니라 증상이기 때문이다.
Firefox가 uBlock을 지원할 수 있는 것은 그것이 비Chromium 엔진이고 사용자 통제를 우선하는 철학을
갖기 때문이며, 그 철학은 다른 곳에서도 나타난다.
한 사용자는 Firefox가 탭·툴바·주소창·메뉴·간격을 커스터마이징하는 `userChrome.css` 같은 것을
지원하는 유일한 브라우저라고 짚었다[^dadass].
다른 사용자는 Firefox가 uBlock을 지원할 뿐 아니라 매 업데이트마다 개발자가 스파이웨어나 멀웨어를
넣지 않았는지 코드를 검토하는 유일한 브라우저이며, 추천 확장은 “보안·기능·사용자 경험의 최고
기준을 충족하는 큐레이션된 확장”이라고 설명했다[^GeekyBear].

이 관점이 기사의 프레임을 뒤집는다.
문제는 “어느 브라우저가 uBlock을 지원하는가”가 아니라 “어느 브라우저가 사용자를 위해 엔진을
통제하는가”다.
한 사용자가 Firefox가 탭 브라우징을 처음 도입한 것을 상기하며, uBlock이 일급 기능은 아니지만
Firefox가 탭으로 얻었던 만큼의 관심을 광고 차단으로 만들 수 있으면 좋겠다고 한 것[^DavidPiper]이
이 값의 크기를 보여준다.
Firefox를 지키는 것은 uBlock 하나를 지키는 것이 아니라, 광고 회사가 소유하지 않은 엔진과 그
엔진이 대표하는 사용자 통제의 철학을 지키는 것이다.

## 비평

### 기사의 “마지막” 서사가 사실을 위기감에 종속시킨다

기사의 가장 큰 결함은 정확성을 극적 효과에 팔아넘긴 것이다.
“마지막 주요 브라우저”라는 제목은 클릭을 부르지만, 앞서 본 HN 사용자의 반박[^eahm]이 보여주듯
현실은 그렇게 이분법적이지 않다.

이 과장이 문제인 이유는 그것이 독자의 판단을 왜곡하기 때문이다.
기사를 읽은 사람은 “Firefox로 옮기지 않으면 광고 차단을 잃는다”고 결론짓겠지만, 실제로는 Brave의
Manifest V2 옵트아웃, Helium의 사전 설치, uBlock Origin Lite, 그리고 Manifest V3용 비공식 포트
등 여러 선택지가 있다.
한 사용자가 uBlock-mv3라는 비공식 포트를 언급하며, 가장 큰 난제가 Manifest V3에서 `webRequestBlocking`
권한이 기업용 사이드로드 확장에만 제공되는 것이라고 짚은 것[^tech234a]은, 기술적 우회가 진행
중임을 보여준다.
기사가 이 스펙트럼을 지웠기 때문에, 독자는 실제보다 더 절박하고 더 단순한 그림을 받는다.

이 결함이 저널리즘의 구조적 문제를 드러낸다.
광고로 수익을 내는 매체가 광고 차단에 대해 위기 서사를 파는 것은 아이러니이며, “마지막”이라는
프레임은 정보 전달보다 감정 동원에 봉사한다.
정확한 기사라면 “Manifest V3 이행으로 광고 차단의 방식이 바뀌고 있으며, 브라우저마다 대응이
다르다”가 됐어야 하지만, 그런 제목은 656점을 얻지 못한다.
기사의 사실 자체는 틀리지 않았지만 — Firefox가 완전한 uBlock Origin을 가장 온전히 지원하는 것은
맞다 — 그 사실을 감싼 프레임이 정확성보다 화제성을 택했다.

### 근본 원인인 시장 구조를 개인의 브라우저 선택 문제로 축소한다

기사는 “Firefox를 쓰라”는 개인적 처방으로 흐르지만, 문제의 뿌리는 개인의 선택이 아니라 하나의
광고 회사가 브라우저 엔진을 지배하는 시장 구조다.

이 축소가 문제인 이유는 개인의 브라우저 이동이 구조를 바꾸지 못하기 때문이다.
한 HN 사용자가 정확히 짚었다 — “세계 최대 광고 회사 중 하나가 만든 브라우저로 모두가 옮긴 것이
애초에 나쁜 생각이었다”는 것이다[^mikeocool].
다른 사용자는 이것을 역사적 패턴으로 확장했다 — 동료 개발자들이 “개발 도구가 더 좋다”, “더
빠르다”는 핑계로 Firefox에서 Chrome으로 옮길 때 고개를 저었으며, Internet Explorer가 Microsoft의
불법 관행으로 웹의 95%를 차지했을 때 얼마나 끔찍했는지 기억한다고, 그런데 광고 회사 Google에게서
같은 행동을 보면서도 그들은 손목 한 번 맞지 않았다고 한 것이다[^Gud].
이 관점은 문제를 개인의 취향이 아니라 독점의 재현으로 규정한다.

이 축소가 처방의 무력함을 낳는다.
Firefox의 시장 점유율이 계속 줄어드는 상황에서 — 한 웹 개발자가 Firefox 3부터 써 왔고 끝까지
함께하겠다면서도 점유율 하락이 우려된다고 한 것[^thrusong]처럼 — 개인들이 Firefox로 옮기는 것만으로는
Chromium의 지배를 뒤집기 어렵다.
IE의 독점이 깨진 것은 개인의 선택이 아니라 반독점 조치와 새로운 경쟁자(Chrome 자신!)의 등장
때문이었다.
기사가 구조적 원인을 다루지 않고 “Firefox를 쓰라”로 끝나는 것은, 웹의 재독점화라는 큰 문제를
개인의 소비 선택으로 축소해 진짜 해법 — 규제와 엔진 다양성 — 을 시야에서 지운다.

### 광고 차단의 “죽음”을 과장해 실제 저항의 수단을 가린다

기사의 위기 서사는 광고 차단이 곧 불가능해질 것처럼 그리지만, HN 논의는 광고 차단을 유지하는
실질적 수단이 여전히 많음을 보여준다.

이 과장이 문제인 이유는 그것이 무력감을 조장하기 때문이다.
기사만 읽으면 “Firefox 아니면 끝”이라는 절망에 빠지지만, 실제로는 여러 저항의 층위가 존재한다.
한 사용자는 Manifest V3에서도 uBlock Origin Lite를 쓰면 광고가 거의 보이지 않는다고 했고[^hn_submit],
다른 사용자는 자기 확장을 직접 작성해 번들되지 않은 채로 Chrome에서 쓸 수 있다고 지적했다[^deweywsu].
또 다른 사용자는 LLM으로 Chromium을 포크해 Manifest V2/blocking 웹 요청 지원을 다시 넣는 것이
이제 쉬워졌다며, “포크를 동기화 상태로 유지하기 너무 어렵다”던 반대 논거가 무너졌다고 봤다[^zarzavat].

이 다층적 저항이 기사의 이분법을 반박한다.
광고 차단은 하나의 기능이 아니라 사용자와 플랫폼 사이의 지속적 군비 경쟁이며, 한쪽이 API를
막으면 다른 쪽이 새 우회를 찾는다.
한 사용자가 “내 광고 차단기는 내 차가운 시체의 손가락에서 빼앗아 가라, 90년대 말 수준의 광고
헛소리로 돌아가느니 숲속 오두막으로 이사하겠다”고 한 것[^firefax]은 이 저항의 결의를 보여준다.
기사가 이 군비 경쟁의 역동성을 “Firefox의 마지막 저항”으로 정지시킨 것은, 사용자에게 남은 실제
수단들 — 대안 브라우저, Lite 버전, 자체 확장, 포크 — 을 가려 무력감만 남긴다.

## 인사이트

### 엔진 독점은 광고 차단을 넘어 웹의 모든 사용자 통제를 인질로 잡는다

이 기사가 광고 차단을 말하지만, 그 밑에 깔린 진짜 문제는 하나의 회사가 웹 엔진을 지배할 때
사용자 통제 전체가 그 회사의 처분에 놓인다는 것이다.
Manifest V3는 그 통제의 첫 번째 행사일 뿐이다.

이 통찰이 근본적인 이유는 엔진이 웹의 규칙을 정하기 때문이다.
브라우저 엔진은 어떤 API가 존재하고 어떤 확장이 가능한지를 결정하며, 그 결정이 사용자가 웹을
어떻게 경험하는지를 규정한다.
Google이 `webRequestBlocking`을 제거해 광고 차단을 약화시킬 수 있다면, 같은 권력으로 다른 사용자
통제 — 추적 차단, 콘텐츠 수정, 자동화 — 도 약화시킬 수 있다.
앞서 uBlock의 Facebook 광고 차단 포기 문서에서 본[^ref-ublock] “플랫폼이 자기 콘텐츠에 대한
사용자 통제를 파괴한다”는 흐름이, 여기서는 플랫폼이 아니라 엔진 층위에서 일어난다 — 그리고 엔진은
플랫폼보다 더 근본적이다.

이 통찰의 2차 효과는 웹 표준의 정치화다.
Manifest는 기술 명세처럼 보이지만 실제로는 사용자와 광고주 사이의 권력 배분이다.
Chromium이 웹의 대부분을 구동하는 한, Google은 표준 제정자이자 최대 광고주라는 이해 상충을
동시에 갖는다.
앞서 X의 For You 알고리즘 문서에서 본[^ref-x] “인프라를 소유한 자가 그 위의 모든 것을 통제한다”는
원리가, 브라우저 엔진이라는 웹의 가장 깊은 인프라에서 가장 강력하게 작동한다.
Firefox를 지키는 것이 중요한 이유는 uBlock이 아니라, 광고 회사가 소유하지 않은 엔진이 하나라도
남아 있어야 웹의 규칙이 단일 이해관계에 완전히 종속되지 않기 때문이다.

### LLM이 포크의 경제학을 바꿔 엔진 독점의 방어선을 약화시킨다

이 기사가 다루지 않은 미래는 AI가 브라우저 엔진 독점의 성격을 바꿀 수 있다는 것이다.
Chromium 포크를 유지하는 비용이 떨어지면, “Google이 Chromium을 통제한다”는 사실의 무게가
가벼워진다.

이 변화가 구조적인 이유는 독점의 힘이 전환 비용에 있기 때문이다.
Chromium 독점이 강력한 것은 그것을 포크해 다른 방향으로 유지하는 것이 엄청나게 어려웠기
때문이다 — 상류(upstream)와 계속 동기화하며 수백만 줄의 차이를 관리해야 했다.
한 HN 사용자가 짚었듯, LLM이 이 동기화·병합 작업을 도우면 “포크를 유지하기 너무 어렵다”던
반대 논거가 무너진다[^zarzavat].
Manifest V2 지원을 다시 넣은 Chromium 포크를 소수의 개발자가 유지할 수 있게 되면, Google의
Manifest V3 결정은 강제가 아니라 선택지 중 하나가 된다.

이 통찰이 앞서 여러 문서에서 본 패턴과 이어진다.
build-wide 문서에서 본 “AI가 되돌리고 재구성하는 비용을 낮춘다”[^ref-bwsn]는 원리가 여기서 엔진
포크에 적용된다 — 유지 비용이 낮아지면 지배적 표준에서 벗어나는 것이 쉬워진다.
이미 Zen(Firefox 기반 Arc 클론)[^sammularczyk], Helium, Brave Origin 같은 파생 브라우저들이
등장하고 있으며, LLM이 포크 유지를 돕는다면 이 파생의 속도가 빨라진다.
엔진 독점의 진짜 방어선은 코드 소유권이 아니라 포크 유지의 어려움이었고, AI가 그 어려움을 낮추면
독점의 통제력은 생각보다 약할 수 있다.
Manifest V3가 광고 차단을 죽인다는 서사의 반대편에는, 그 결정에 반대하는 포크가 그 어느 때보다
쉽게 유지될 수 있다는 가능성이 있다.

### 소수의 수호자에 의존하는 자유는 그 수호자가 무너지면 함께 무너진다

Firefox가 “마지막 수호자”라는 서사는 감동적이지만, 하나의 브라우저에 광고 차단의 미래를 거는
것은 그 자체로 취약한 구조다.
자유가 소수의 선의에 의존할 때, 그 소수가 무너지면 자유도 무너진다.

이 취약성이 근본적인 이유는 Firefox 자신의 지속 가능성이 불확실하기 때문이다.
Firefox의 시장 점유율은 계속 줄고 있고, 그 개발 자금의 대부분은 아이러니하게도 Google의 검색
기본값 계약에서 온다.
한 사용자가 Firefox 점유율 하락이 우려된다고 한 것[^thrusong]은 이 취약성을 정확히 짚는다 —
“마지막 수호자”가 재정적으로 자신의 최대 위협에 의존한다면, 그 수호는 언제든 흔들릴 수 있다.
소수에 의존하는 자유는 그 소수를 영웅으로 만들지만, 동시에 단일 실패 지점(single point of
failure)으로 만든다.

이 통찰의 함의는 자유의 회복력이 다양성에서 온다는 것이다.
광고 차단의 미래가 Firefox 하나가 아니라 여러 비Chromium 엔진, 여러 포크, 여러 우회 수단에
분산돼 있어야 그중 하나가 무너져도 자유가 유지된다.
한 사용자가 “더 많은 Firefox 같은 브라우저 — 더 오픈소스이고 웹을 개선하는 표준에 열린 — 가
필요하다”고 한 것[^system7rocks]이 이 방향을 가리킨다.
앞서 Ladybird 같은 독립 엔진 프로젝트가 중요한 이유도 여기 있다 — 웹의 자유는 하나의 영웅적
수호자가 아니라 엔진의 생물다양성이 지킨다.
이 기사가 Firefox를 “마지막”이라 부른 것은 찬사이자 경고다 — 자유가 마지막 한 명에게 달렸다면,
그것은 이미 위태로운 자유이며, 진짜 안전은 “마지막”이 아니라 “여럿”에서 온다.

## 참고

- 관련 문서: [uBlock Origin이 Facebook 광고 차단을 포기했다](ublock-facebook-ads.md), [X의 For You 피드를 굴리는 Grok 트랜스포머 랭킹 알고리즘](../machine-learning/x-for-you-algorithm.md), [넓게 만들고 좁게 출하하라](../agentic-coding/build-wide-ship-narrow.md)

---

[^ref-ublock]: 플랫폼이 사용자 통제를 파괴하는 흐름에 대한 논의는 이 저장소의 [관련 문서](ublock-facebook-ads.md)에 정리해 두었다.
[^ref-x]: 인프라를 소유한 자가 그 위의 모든 것을 통제한다는 논의는 이 저장소의 [X For You 알고리즘 문서](../machine-learning/x-for-you-algorithm.md)에 정리해 두었다.
[^ref-bwsn]: AI가 되돌리고 재구성하는 비용을 낮춘다는 논의는 이 저장소의 [관련 문서](../agentic-coding/build-wide-ship-narrow.md)에 정리해 두었다.
[^GeekyBear]: <https://news.ycombinator.com/item?id=49305222>
[^avaer]: <https://news.ycombinator.com/item?id=49305425>
[^eahm]: <https://news.ycombinator.com/item?id=49305807>
[^vovavili]: <https://news.ycombinator.com/item?id=49303590>
[^tech234a]: <https://news.ycombinator.com/item?id=49306267>
[^mikeocool]: <https://news.ycombinator.com/item?id=49306071>
[^Gud]: <https://news.ycombinator.com/item?id=49307703>
[^thrusong]: <https://news.ycombinator.com/item?id=49307303>
[^dadass]: <https://news.ycombinator.com/item?id=49307509>
[^DavidPiper]: <https://news.ycombinator.com/item?id=49306110>
[^hn_submit]: <https://news.ycombinator.com/item?id=49305556>
[^deweywsu]: <https://news.ycombinator.com/item?id=49305705>
[^zarzavat]: <https://news.ycombinator.com/item?id=49307610>
[^firefax]: <https://news.ycombinator.com/item?id=49306875>
[^sammularczyk]: <https://news.ycombinator.com/item?id=49307589>
[^system7rocks]: <https://news.ycombinator.com/item?id=49306202>
