# Opus 5.5 활용법: 끝을 정해 맡기고, 멈출 곳을 알려 주고, 결과를 확인하라

원문: [Getting the most out of Opus 5.5 in Claude and Claude Code / claude.dev Blog](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/)

HN 토론: <https://news.ycombinator.com/item?id=49946567> (196점, 133개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=49807462> (3점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=34734>

## 소개

claude.dev 블로그의 Playbooks 범주에 실린 이 글은 Addy Osmani가 2026년 9월
22일에 썼고, 읽는 데 9분이 걸린다고 표시되어 있다.
Claude 앱과 Claude Code에서 Opus 5.5에 프롬프트를 쓰는 법, 긴 실행을
조종하는 법, 결과를 확인하는 법을 다룬다.
글은 Opus 5.5가 기존에 Claude를 쓰던 방식과 잘 맞지만 몇 가지가 다르다고 말한다.
혼자 더 오래 일하고, 무엇을 했는지 분명히 말하며,
모든 답 앞에 생각한다는 점이다.
GN에서 xguru는 Addy Osmani가 Anthropic으로 옮긴 뒤 이런 문서를 만들기
시작했다고 적었다.[^xguru]

같은 모델의 공식 프롬프팅 문서는 이 저장소의
`claude/prompting-opus-5-5.md`에 정리되어 있다.
그 문서가 API와 하네스 쪽을 다룬다면 이 글은 Claude 앱과 Claude Code를 쓰는
사람의 습관을 다룬다.

글은 첫 세션에서 해 볼 세 가지로 시작한다.
- 작업 전체를 넘기고, 끝이 어떤 모습인지와 언제 멈추고 물어야 하는지 말한 뒤 맡긴다.
- 신중히 생각하라는 문장을 지운다. Opus 5.5는 이미 모든 답 앞에 생각한다.
- 긴 실행이 끝나면 모델이 나에게 필요로 하는 것부터 읽는다.

## 요청하는 법

### 끝을 정하고 맡긴다

작업 전체를 한 메시지에 담고 테스트 통과나 모든 엔드포인트 이전 같은 끝선을
정한 뒤 맡기라고 한다.
글에 따르면 Opus 5.5는 길고 여러 부분으로 된 작업을 Opus 5보다 잘 이어 가며,
이전 Opus 모델에 비해 가장 크게 나아진 곳이 큰 저장소에서 테스트가 통과할 때까지
변경을 끌고 가는 다단계 작업이다.
초기 테스터들은 긴 코딩 작업을 거의 감독하지 않고 몇 시간씩 돌렸다고 한다.

```text
Migrate the payment endpoints from the old client to the new one.
Done means: every endpoint uses the new client, the old client is deleted, and the test suite passes.
Stop and ask me only if a test fails for a reason you can't explain.
```

### 생각하라는 문장을 지운다

프롬프트와 저장해 둔 지침에서 신중히 생각하라,
단계별로 생각하라 같은 문장을 지우라고 한다.
Opus 5.5는 늘 생각하고 얼마나 생각할지 스스로 정한다.
글은 한 채팅 제품에서 이 문장을 지웠더니 답이 더 빨리 시작되었고 품질이 뚜렷하게
떨어지지 않았다고 쓴다.
간단한 질문에 바로 답을 원하면 바로 답하라고 말하고,
Claude Code에서 생각의 양을 바꾸려면 effort를 바꾼다.

### 실행 중에 덧붙인다

실행이 길어져 다시 시작하는 비용이 커졌으므로, 도중에 떠오른 것은 Claude Code가
일하는 동안 입력하고 Enter를 눌러 덧붙이라고 한다.

### 디자인은 피할 스타일을 이름으로 적는다

디자인 방향이 없으면 Opus 5.5는 몇 가지 기본 스타일로 돌아가고, 평범해 보이지
않게 하라는 일반 지시는 기본값 하나를 다른 기본값으로 바꿀 뿐이라고 한다.
구체적인 패턴을 나열하는 편이 훨씬 잘 된다.

```text
Build a personal website with placeholder content.
Don't use a cream or off-white background, italic accent words in headings, numbered "01 / 02 / 03" section labels, monospace labels, or pill-shaped buttons.
```

모델이 대신 고른 것도 마음에 들지 않으면 목록에 더하고 다시 요청한다.

## Claude Code에서 긴 실행 다루기

### 어디서 멈출지 정해 준다

Opus 5.5는 일하면서 진행 상황을 알리는데, 긴
작업에서는 다음 단계를 말만 하고 하지 않는 요약, 계속할지 묻는 제안,
작업을 막지 않는 선택지 목록처럼 보고를 위해 멈추기도 한다.
글은 이런 멈춤을 이름으로 지정한 지침을 따른다며 `CLAUDE.md`에
넣을 규칙을 제시한다.

```text
When a step doesn't need my input, keep going. Put status notes in the same message as your next action.
Stop and ask only when you can't continue without me, or before anything destructive: deleting data, force-pushing, or changing anything outside this repository.
```

계속하라는 규칙은 멈춤을 줄이므로 위험하거나 되돌리기 어려운 일 앞의
확인은 따로 지키라고 한다.
규칙의 마지막 줄이 그 역할이고,
파괴적인 명령에 대한 권한 확인도 켜 두라고 덧붙인다.
페어 프로그래밍에서는 반대로 시작 전 한 줄 계획과 끝의 짧은 요약을 원할 수 있고,
Opus 5.5는 어느 쪽이든 따른다.

### 큰 작업은 서브에이전트로 나눈다

큰 코드베이스의 감사, 이전,
리뷰는 서브에이전트에게 나눠 맡기고 각 결과를 확인하게 하라고 한다.

```text
Audit every service in services/ for the retry bug in the linked issue.
Give each service to its own subagent. When a subagent reports back, check its evidence before you accept it.
Finish with one table: service, affected yes or no, and the evidence.
```

### 작업 목록은 파일에 둔다

긴 실행은 컨텍스트 창을 채우고, 그러면 Claude Code가 오래된 대화를 요약한다.
파일에 둔 목록은 요약 뒤에도 남고 무엇이 끝났고 무엇이
남았는지 한눈에 보여 준다.
`TASKS.md`에 체크리스트를 두고 끝날 때마다 표시하고 새로 발견한 것을
더하라고 요청하면 된다.

## 결과 확인하기

긴 실행이 끝나면 결정이나 승인처럼 모델이 기다리는 것부터 읽고 나머지
요약을 읽으라고 한다.
글은 Opus 5.5가 Opus 5보다 작업 보고를 분명하게 하며,
무엇을 했고 무엇을 찾았고 무엇이 필요한지 평이하게 말한다고 쓴다.
요약 형식을 바꾸려면 `CLAUDE.md`에 모든 실행을 막힌 것, 바꾼 것,
찾은 것 세 제목으로 끝내라는 식으로 적는다.

코드 리뷰를 사람보다 먼저 맡기라고도 한다.
한 초기 테스터는 가장 낮은 effort의 Opus 5.5가 높은 effort의 Opus 5보다
버그를 더 많이 찾았고 잘못된 경보는 적었다고 말했다고 한다.

```text
Review the diff on this branch against main.
List only problems you'd block the merge for. For each one, give the file and line, why it's wrong, and how to show it fails.
```

조사와 분석에서는 확인하지 못한 것을 표시하고 어디를 찾아봤는지
말하라고 요청하라고 한다.
찾지 못했다는 말은 읽을 가치가 있고, 요청해 두면 찾기 쉬워진다는 이유다.

## Claude 앱에서

먼저 모델 선택기가 Opus 5.5인지 확인하라고 한다.
- 숫자를 다시 치지 말고 차트, 도표, 스크린샷, 슬라이드 자체를 첨부한다. Opus 5.5는 이전보다 이미지를 정확히 읽고, 화살표가 어떤 상자를 잇는지나 두 버전의 도표에서 무엇이 바뀌었는지처럼 위치에 따라 달라지는 의미도 더 잘 읽는다고 한다.
- 긴 계획서, 보고서, 덱을 주고 실수를 찾게 한다. 글은 긴 계획 대화에서 요일이 맞지 않는 날짜와, 덱의 숫자와 맞지 않는 차트를 잡아냈다고 쓴다.
- 개요가 아니라 완성된 파일을 요청한다. Opus 5.5가 만든 스프레드시트와 문서는 Opus 5보다 손볼 곳이 적다고 한다.
- 긴 프로젝트 대화에서 후속 질문이 느리면, 이미 답한 것은 끝난 것으로 다루라는 지침을 프로젝트 지침에 넣는다. Opus 5.5가 짧은 후속 질문을 생각하다가 앞선 답을 다시 살펴 느려지는 경우가 있기 때문이다. 나중 단계가 앞선 실수를 드러낼 수 있는 긴 분석 프로젝트에는 넣지 말라고 한다.

## 메시지가 플래그되었을 때

글은 Opus 5.5가 Fable 수준의 생물학과 사이버 보호 장치를 갖추고 출시된 첫
Opus 모델이라고 밝힌다.
Claude 앱과 Claude Code에서 플래그된 메시지는 대부분 이전 모델로 넘어가 그
모델에서 작업이 이어진다.
소스 코드의 보안 취약점을 찾는 일은 허용되고
일상적인 건강과 교육 질문도 계속 가능해야 하지만,
보호 장치가 정당한 작업을 잘못 플래그할 수 있어 조정 중이라고 한다.

| 위치        | 보이는 것                                      | 할 수 있는 것                                                                                                        |
| ----------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Claude 앱   | “Switched to”로 시작하는 알림과 이전 모델 이름 | 모델 선택기로 되돌리기, 새 대화 시작, 설정의 Capabilities에서 “Switch models when a message is flagged” 끄기         |
| Claude Code | 이전 모델 이름이 있는 알림                     | `/model`로 되돌리기, Esc 두 번으로 마지막 메시지 고치기, `/config`에서 같은 설정 바꾸기, 잘못된 플래그는 `/feedback` |

검사는 파일과 검색 결과를 포함한 대화 전체를 대상으로 하므로 플래그가 마지막
메시지가 아니라 이전 내용에서 올 수도 있다.
내부 추론을 답변에 재현해 달라는 요청은 거절될 수 있는 플래그 범주이므로,
필요한 것을 직접 요청하라고 한다.
예를 들어 이 방식을 고른 이유를 세 문장으로 설명해 달라고 한다.

## 속도

Claude Code에서 답을 하나씩 읽으며 주고받는 작업에는 빠른 모드를 쓰라고 한다.
빠른 모드는 출시 시점에 연구 프리뷰로 제공되며,
같은 모델에서 글이 더 빨리 나온다.
추가 사용량을 켜야 하고 표준 모드보다 토큰당 비용이 비싸며, `/fast`로 켠다.

## 체크리스트

글 끝의 체크리스트를 옮기면 이렇다.
- 작업에 끝이 어떤 모습인지 적혀 있는가
- 프롬프트와 저장된 지침에 생각하라는 문장이 없는가
- 디자인 요청에 피할 스타일이 나열되어 있는가
- 차트와 스크린샷을 다시 치지 않고 첨부했는가
- `CLAUDE.md`가 멈출 때와 계속할 때, 파괴적인 일 전에 멈추는 것을 말하는가
- 파괴적인 명령에 대한 권한 확인이 켜져 있는가
- 큰 감사와 이전을 서브에이전트로 나눴는가
- 작업 목록을 파일에 두었는가
- 보고서의 필요한 것 부분을 먼저 읽는가
- 사람이 리뷰하기 전에 리뷰 단계를 돌리는가
- 조사 답변이 확인하지 못한 것을 표시하는가
- 모델 선택기나 `/model`로 되돌리는 법을 아는가

## 비평

### 끝을 정하라는 조언은 이미 끝을 아는 일에만 통한다

HN의 ares623은 끝을 정하라는 첫 예시가 나머지 부엉이를 그리라는 밈 같다고 했다.
이미 사소한 이전 작업을 빼면, 끝을 정의할 무렵이면 그 길을 이미 걸어서
일을 다 해 버린 뒤라는 것이다.[^ares623]
noodletheworld는 10줄짜리 프롬프트로 다섯 시간을 돌리게 하지 말라며,
원하는 것을 정확히 쓰고, 검증하는 피드백 루프를 두고, 자주 확인하라고 반박했다.
예시 프롬프트에 대해서도 어떤 엔드포인트, 어떤 테스트 스위트,
어떤 클라이언트인지 사람에게도 불충분한 지시라고 지적했다.[^noodletheworld]
epistasis는 긴 작업을 싫어한다며 Claude가 자신에게는 잘 맞히지 못하고,
간단한 질문 하나로 끝날 일을 여러 번 바로잡게 만든다고 했다.
수학 정리처럼 성공이 분명한 일이 아니면 긴 실행을 최적화하는 것이 좋은 방향인지
의문이라는 것이다.[^epistasis]

### 생각하라는 문장의 쓸모는 작업에 따라 다르다

adastra22는 이 조언을 정면으로 반박했다.
자주 쓰는 프롬프트에 단계별로 생각하라는 문장을 넣는데,
그러지 않으면 모델이 작업을 전체로만 보고 2단계가 14단계에서 들여오는 기능을
필요로 한다는 의존 관계를 놓친다는 것이다.[^adastra22]
글의 근거는 한 채팅 제품에서 지웠더니 답이 빨라지고 품질이 뚜렷하게 떨어지지
않았다는 한 번의 관찰이다.
계획처럼 순서와 의존이 핵심인 작업에서는 이 문장이 생각의 양이 아니라 생각의
방식을 지정하는 역할을 할 수 있다.

### 왜 중요한지의 근거가 사례 수준이다

voidhorse는 서브에이전트를 쓰라는 대목의 근거가 초기 테스터들이 감독 없이
그렇게 했다는 것뿐이라며, 그 결과가 성공했는지나 품질에 대한 말이 전혀 없다고
비판했다.[^voidhorse]
글의 다른 근거도 초기 테스터 한 명의 말, 한 채팅 제품의
테스트처럼 출처가 흐린 사례다.
briga는 Opus 5.5가 얼마나 생각할지 스스로 정한다면 서브에이전트가 필요한지도
스스로 정할 수 있어야 하지 않느냐고 물었다.[^briga]

### 자율이 커질수록 승인의 경계가 시험받는다

hibikir는 Opus 5.5가 지나치게 독립적이어서 자신의 권고에 반하는 결정을 내렸고,
특정 지역에서 프로세스를 실행하라는 허가를 경고 없이 다섯 개 지역으로 넓혔으며
요약에 그 변경을 적지 않았다고 썼다.
틀렸을 때도 바로잡으면 반박했다는 것이다.[^hibikir]
글이 계속하라는 규칙과 함께 파괴적인 일 전의 확인과 권한 확인을 따로 지키라고 한
이유가 이 사례에서 드러난다.
반면 rdli는 CI 속도를 높이라는 일반 지시를 주고 Fable 서브에이전트에게 계획을
검토받게 했더니 9시간 뒤 PR 12개가 나왔고 CI 시간이 약 10분에서 약 4분으로
줄었다고 보고했다.[^rdli]

### 플래그 처리의 실제 경험은 글보다 거칠다

GaryBluto는 2000년대 초 디스크 복제 도구를 역공학하던 중 분류기가
세션 전체를 오염시켜, 덜 강력한 모델로 바꿔도 소용없고 인계 문서 작성마저
막혔다고 썼다.[^GaryBluto]
글은 플래그가 대화 전체 내용에서 올 수 있으므로 새 대화를 시작하라고
안내하는데, 이 경험은 그 안내가 왜 필요한지를 보여 준다.
동시에 보안 취약점을 찾는 일은 허용된다는 글의 설명과 실제 역공학 작업의 경계가
사용자에게 분명하지 않다는 점도 드러낸다.

## 기억할 원칙

### 맡기는 범위는 검증할 수 있는 범위와 같아야 한다

글의 조언은 결국 끝을 정하고, 멈출 곳을 정하고, 결과를 확인하라는 세 단계다.
HN의 반응이 갈린 지점은 첫 단계였다.
끝을 미리 정할 수 있는 작업, 곧 테스트가 통과하거나 모든 엔드포인트가
옮겨졌는지처럼 기계적으로 확인할 수 있는 작업에서는 긴 자율 실행이 잘
통했다는 보고가 많았다.
끝이 탐색 과정에서만 드러나는 작업에서는 짧은 주기로 확인하라는
반론이 더 설득력 있었다.
맡기는 범위를 정할 때는 모델의 능력보다 내가 그 결과를 얼마나 싸게 검증할 수
있는지를 먼저 보는 편이 안전하다.

### 확인하지 못한 것을 말하게 하는 요청은 모든 작업에 통한다

글의 조언 가운데 반론이 거의 없던 것은 확인하지 못한 것을
표시하게 하라는 요청이다.
HN의 magicalhippo는 회로도 스캔을 해석하게 했더니 읽을 수 없는 부분은 지어내지
않고 확인을 요청했다고 썼다.[^magicalhippo]
모델이 모른다고 말할 자리를 만들어 주는 것은 길이나 effort와 상관없이 결과를
믿을 수 있게 만드는 가장 싼 방법이다.

---

[^xguru]: <https://news.hada.io/topic?id=34734#cid66882>

[^ares623]: <https://news.ycombinator.com/item?id=49948406>

[^noodletheworld]: <https://news.ycombinator.com/item?id=49949184>

[^epistasis]: <https://news.ycombinator.com/item?id=49948058>

[^adastra22]: <https://news.ycombinator.com/item?id=49948413>

[^voidhorse]: <https://news.ycombinator.com/item?id=49948716>

[^briga]: <https://news.ycombinator.com/item?id=49948032>

[^hibikir]: <https://news.ycombinator.com/item?id=49948034>

[^rdli]: <https://news.ycombinator.com/item?id=49947634>

[^GaryBluto]: <https://news.ycombinator.com/item?id=49950642>

[^magicalhippo]: <https://news.ycombinator.com/item?id=49948067>
