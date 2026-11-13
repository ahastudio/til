# Jane Street의 socratic-tutor는 LLM을 진단, 스킬 맵, 한 번에 한 질문으로 가르치는 엄격한 개인 교사 상태 기계로 만드는 프롬프트이다

<https://github.com/janestreet/agent_skills/blob/master/socratic-tutor/SKILL.md>

HN 토론: <https://news.ycombinator.com/item?id=50438261> (439점, 100개 댓글)

GN 토론: <https://news.hada.io/topic?id=37048>

## 소개

`socratic-tutor`는 Jane Street가 공개한 에이전트 스킬 저장소(`janestreet/agent_skills`)의
유일한 스킬이다.
`SKILL.md` 한 파일로 이루어져 있고, LLM을 사용자의 현재 수준에서 진짜 숙달까지 이끄는
개인 교사로 만든다.
방식은 산파술(소크라테스식 문답)이다.
강의하지 않고 사용자가 추론하고 예측하고 설명하게 만드는 질문으로 가르친다.
저장소는 MIT 라이선스이고 2026년 11월 3일에 만들어졌으며, 이 문서가 읽은 2026년 11월
12일에는 별 7,192개와 포크 481개였다.
저장소 README는 스킬이 `SKILL.md`가 든 디렉터리라고 설명하고,
이 형식을 지원하는 코딩 에이전트에서는 디렉터리를 스킬 폴더에 복사한 뒤 teach me X라고
부르면 되고,
일반 챗봇에서는 `SKILL.md`의 본문을 채팅이나 시스템 프롬프트에 붙여 넣으라고 안내한다.[^readme]
기여는 풀 리퀘스트로 받고 모든 커밋에 실명 서명(DCO의 Signed-off-by)을 요구한다.[^contributing]

### 언제 켜지는가

스킬의 설명은 사용자가 명시적으로 가르쳐 달라거나, 퀴즈를 내 달라거나, 숙달될 때까지
훈련시켜 달라고 할 때만 쓰라고 한다.
호출 문구는 teach me, tutor me, quiz me, drill me, help me master이다.
한 번짜리 질문(X를 설명해 줘, X가 뭐야)에는 쓰지 않는다.
본문의 첫 규칙도 같은 취지의 보호 장치이다.
의도가 불분명하면 빠른 답을 원하는지 제대로 가르쳐 주길 원하는지 짧게 묻고 시작하라는
것이다.
잘못 시작하면 원치 않는 퀴즈를 겪게 하는 비용이 들고, 확인하면 한 단어의 비용이 든다고
설명한다.

### 세션의 흐름

세션은 다음 순서로 진행된다.
주제를 4~10개의 구체적 하위 기술로 나누고(넓은 주제는 두 단계 트리로 나누어 첫 가지만),
사용자에게 한 번에 한 질문씩 묻겠다고 알린 뒤 진단을 한다.
진단은 쉬움에서 어려움까지 3~5개의 탐색 질문으로 하위 기술별 시작 수준을 정하고,
끝나기 전에는 아무것도 가르치지 않는다.
그다음 스킬 맵을 보여 주고 어디서 시작할지 제안하며 사용자가 바꿀 수 있게 한다.

하위 기술마다 수준은 0에서 5이다.
0은 모름, 1은 들어 봄, 2는 따라 할 수 있음, 3은 도움을 받아 할 수 있음, 4는 혼자
할 수 있음, 5는 가르치거나 예외 상황까지 다룰 수 있음이다.
수준이 바뀔 때마다, 그리고 사용자가 물을 때마다 ASCII 막대로 맵을 그린다.

가르치는 반복은 하위 기술마다 이렇다.
한 번에 한 질문만 하고 질문 바로 뒤에서 메시지를 끝내며 힌트나 예시 답이나 설명을
덧붙이지 않는다.
질문은 결과 예측, 이유 설명, 그럴듯하지만 틀린 주장의 결함 찾기, 새 사례에 적용,
두 개념 연결 중 하나를 시키는 것을 선호한다.
사용자가 틀리면 답을 주지 않고 모순을 드러내는 더 좁은 질문을 한다.
2~3번 실패한 뒤에야 직접 설명하고, 그 직후 같은 개념을 다른 각도에서 다시 시험한다.
맞았을 때는 가끔 악마의 변호인 역할을 해서 정말 그런지 되묻는다.
짧은 설명은 사용자가 스스로 도출할 수 없는 새 내용을 소개할 때만 한다.
도구를 쓸 수 있으면 실습(쿼리 작성, 코드 출력 예측)을 내고 사용자의 설명이 아니라 실제
출력을 확인한다.

평가 규칙은 엄격하다.
수준은 받는 것이 아니라 얻는 것이라서, 독립된 2회 이상의 확인(그중 하나는 답을 듣고
난 직후가 아닌 스스로의 회상)에서 보여 준 수행이 있어야 올린다.
모호하거나 부분적으로 맞는 답은 정답이 아니다.
사용자가 표현하지 않은 통찰을 사용자가 가진 것으로 돌리지 않는다.
예고 없이 이전 하위 기술을 다시 시험해서(간격 복습) 실패하면 수준을 낮춘다.
5단계는 예외나 적대적 질문을 다루고 그 개념을 가르쳐도 믿을 만큼 명확히 설명해야 한다.
칭찬하지 않는다.

모든 하위 기술이 목표 수준(기본 4, 완전 숙달을 요청하면 5)에 이르면 끝난다.
그때 하위 기술마다 최소 한 문제와 통합 문제 하나가 있는 최종 종합 평가를 한다.
통과하면 최종 맵과 가장 약한 영역의 요약을 보여 주고, 아니면 반복으로 돌아간다.
사용자는 언제든 명령할 수 있다.
show progress는 맵을 보여 주고, harder와 easier는 난도를 조절하고, just tell me는 현재
질문 하나에만 소크라테스 방식을 끈다.
save state는 주제, 맵의 수준, 오해와 다룬 범위에 대한 메모를 담은 압축 블록을 내놓아
새 세션에 붙여 넣어 이어 가게 하고, resume from:은 저장한 블록을 복원한다.

## 분석

### 중심 설계는 학습 세션을 프롬프트로 쓴 상태 기계이다

가장 강하게 말하면 이 스킬은 교수법을 말로 설명한 글이 아니라 상태를 가진 절차이다.
상태는 하위 기술별 수준(0~5)이고, 전이 규칙은 승급과 강등의 조건이며, 종료 조건은 목표
수준과 최종 평가이다.
LLM에게는 기억이 없으므로 상태를 눈에 보이는 맵으로 매번 다시 그리게 하고,
세션을 넘길 때는 save state 블록으로 직렬화한다.
HN에서 pbronez는 스킬이 프로그램이고 LLM이 컴퓨터이며 상태는 하네스가 관리해야 하는데
이런 스킬은 세션 사이의 상태 관리 지침이 명시적으로 필요하다고 썼다.[^pbronez]
이 스킬은 상태 관리를 사용자가 붙여 넣는 블록에 맡기는 가장 가벼운 방식을 택한 것이다.

### 엄격한 규칙은 LLM의 아첨에 맞서는 장치로 읽힌다

모델은 사용자의 답을 인정해 주는 쪽으로 기울기 쉽다.
이 스킬의 규칙 여럿은 그 경향을 막는 데 맞춰져 있다.
모호한 답을 정답으로 치지 말 것, 사용자가 말하지 않은 통찰을 귀속하지 말 것,
승급에는 독립된 두 번의 확인과 스스로의 회상이 필요할 것, 칭찬하지 말 것,
맞은 답도 가끔 되물을 것이다.
이것은 규칙의 문면에서 이 문서가 읽은 의도이고, 저자가 아첨을 막으려는 것이라고 밝힌
것은 아니다.
arshxyz는 Opus 5.5 중간 노력 설정으로 일주일쯤 써 보니 같은 모델로 배울 때와 달리 이 스킬이
모델의 평소 손잡이 잡아 주기(handholding)를 막아 줘서 좋았다고 했다.[^arshxyz]

### 학습 과학의 잘 알려진 원리와 겹치지만 인용은 없다

스킬의 요소는 인출 연습(답을 듣기 전에 꺼내 보기), 간격 복습, 섞어 시험하기,
숙달 학습(목표 수준 전에는 넘어가지 않음)과 겹친다.
HN에서 genxy는 숙달 학습과 프로그램 학습의 문서를 가리켰고, nilsherzig는 Jane Street의
누군가가 Math Academy의 방식을 좋아한 것 같다고 했다.[^genxy][^nilsherzig]
스킬 본문은 어떤 연구도 인용하지 않으며 이 대응은 이 문서와 댓글의 해석이다.
Anthropic의 연구는 AI로 새 라이브러리를 배운 참가자 가운데 후속 질문과 설명 요청과 개념
질문으로 이해를 쌓은 쪽이 이해 퀴즈에서 더 나았다고 보고한다.[^anth-skill]
이 스킬은 모델이 답을 주는 대신 사용자가 답을 꺼내게 하는 방향이어서 그 연구가 말하는
쪽에 가깝다고 읽을 수 있다.
다만 그 연구가 이 스킬을 시험한 것은 아니다.

### 이 스킬의 예시 맵 숫자는 자기 규칙과 맞지 않는다

스킬은 맵의 예시를 보인다.
하위 기술이 세 개이고 수준이 4, 3, 1인데 전체 줄은 막대 6칸과 58%이다.
세 수준의 합은 8이고 최대는 15이므로 평균은 53.3%이다.
막대 6칸은 60%이다.
전체 값을 어떻게 계산하는지(평균인지 가중치가 있는지)는 스킬이 정하지 않았고,
막대도 예시에서는 `#`과 `.`로 그려져 있지만 본문은 실제로는 U+2588과 U+2591 블록 문자를
쓰라고 한다.
예시의 숫자는 어림일 수 있지만 모델이 이 예시를 따라 쓰면 계산 없이 그럴듯한 퍼센트를
내놓을 수 있다.
이 지적은 이 문서가 예시를 계산해 본 것이다.

```python
levels = [4, 3, 1]
print(sum(levels) / (5 * len(levels)))   # 0.5333...  (예시의 58%와 다르다)
```

## 비평

### 평가 없이 공개된 프롬프트라서 효과는 사용자의 인상에 기댄다

저장소에는 이 스킬의 효과를 재는 평가가 없다.
lemax는 탄탄한 평가를 거쳤다면 훌륭할 것이라며 모델이 힌트를 흘리거나 답을 새어 주지
않게 하는 어려움을 말했다.[^lemax]
bilalabdullahi는 학습자가 일주일 뒤에 비슷한 문제를 혼자 풀 수 있는지가 궁금하다고
했다.[^bilal]
긍정적인 사용 후기는 많다.
vaskebjorn은 밀도 높은 철학 텍스트에 썼는데 15분 만에 녹초가 되었다고 했고,
Imanari는 다시 스스로 생각하기 시작한 느낌을 받았다고 했고,
igleria는 뇌를 움직이게 한다고 했다.[^vaskebjorn][^imanari][^igleria]
모두 인상이고 학습 결과의 측정은 아니다.
arshxyz는 효과의 대부분이 한 줄(사용자가 틀리면 답을 주지 말고 모순을 드러내는 더 좁은
질문을 하라)로 재현된다고 보았다.[^arshxyz]
이 말이 맞다면 스킬의 나머지 구조(맵, 간격 복습, 최종 평가)가 더하는 이득은 별도로
재야 한다.

### 단지 프롬프트라는 반론과 모델이 규칙을 벗어난다는 우려가 있다

pkoird는 LLM이 충분히 능력을 갖춘 뒤로 사람들이 이미 하던 것인데 왜 호들갑이냐고 했고,
mw888은 모든 스킬이 결국 프롬프트이며 일에 맞춰 직접 설명하는 편이 더 쉽다고 했다.[^pkoird][^mw888]
jkhdigital은 체계화하려면 코드로 쓰고 자연어는 코드가 아니라고 했고,
vkgcr는 프롬프트라서 LLM이 반드시 규칙에서 벗어나 환각을 시작한다고 했다.[^jkhdigital][^vkgcr]
반대로 quibono는 이미 비슷한 것을 쓰고 있었지만 자주 다시 쓰던 내용을 깔끔하게 압축해 둔
설명이 기초로서 가치가 있다고 했다.[^quibono-found]
ngruhn은 순수한 마크다운 스킬은 쉽게 다시 만들 수 있어서 가치는 산출물보다 아이디어에 있다고
했다.[^ngruhn]
이 스킬의 상태는 LLM이 지켜야 하는 규칙으로만 유지되고, 규칙을 벗어났는지를 확인하는 장치는
스킬 안에 없다.

### 새롭지 않다는 지적과 주목받은 이유

orbis-tertius는 Jane Street가 bevibing/socrates-skill을 베꼈거나 독립적으로 다시 발견했을
수 있다고 했고, beans6543은 두 스킬이 완전히 다르고 소크라테스식 질문은 잘 알려진
기법이며 GitHub 검색에 비슷한 저장소가 92개 나온다고 답했다.[^orbis][^beans6543]
burrish는 새롭지 않은데 왜 프런트 페이지에 갔느냐고 물었고, orbis-tertius는 영향력 있는
조직이 낼 때만 주목받는다는 냉소적 해석과 창의와 실행이 마크다운 파일 하나에도 중요하다는
긍정적 해석을 같이 적었다.[^burrish][^orbis2]
poilcn은 포크와 별의 수가 조작된 것이냐고 물었고 michelb는 많은 사람이 포크를 북마크로 쓴다고
답했다.[^poilcn][^michelb]
이 문서는 별과 포크가 어떻게 쌓였는지 확인하지 않았다.

### 소크라테스식 질문이 가르치려는 것을 모델이 알 수 있는가

Mikhail_Edoshin은 소크라테스식 질문은 맹목적으로 하는 것이 아니라 학생이 자신이 안다고
믿는 것의 불완전함이나 거짓을 깨닫게 하려는 것이라고 했다.[^mikhail]
이 스킬의 규칙은 모순을 드러내는 더 좁은 질문을 하라고 하지만, 무엇이 그 사람의 모순인지를
짚는 일은 모델의 진단에 달려 있다.
awongh는 이것이 AI로 대체되기 가장 먼 일의 하나라고 했다.[^awongh]
SkyBelow는 이 방법을 제대로 쓰려면 질문하는 사람을 이해해야 하는데 스킬의 첫 단계(몇 개의
질문으로 알고 있는 것을 확인)가 세션마다 반복되어 다섯 번째에는 숙달을 다시 증명하는 것이
지겨워진다고 했다.[^skybelow]
pimeys는 질문을 시작하기 전에 LLM이 맥락을 채우게 하라고 했다.[^pimeys]
`save state`는 이 문제를 일부만 다룬다.
맵과 오해 메모는 넘기지만 진단이 사용자를 이해하는 방식은 넘기지 않는다.

### 사용 환경에서의 작은 마찰

koolba는 claude CLI에서 시험하니 다음 프롬프트로 제안되는 것이 질문의 답이라서 웃기다고
했고, nathell은 `/config`에서 프롬프트 제안을 끄라고 답했다.[^koolba][^nathell]
이 보고는 스킬이 아니라 도구의 기능과의 충돌이다.

## 인사이트

### 가르쳐 달라고 할 때만 쓰고, 답이 급할 때는 끈다

스킬의 보호 장치(한 번짜리 질문에는 답한다, 모호하면 한 문장 확인)는 이 도구의 가장 실용적인
규칙이다.
이 문서의 제안은 실제로 쓸 때 just tell me를 빠른 출구로 기억해 두는 것이다.
현재 질문 하나에만 소크라테스 방식을 끄는 명령이라서, 막혀서 시간이 아까울 때 세션을 잃지
않고 답을 받을 수 있다.
이 사용법은 이 문서의 제안이다.

### 효과를 재려면 일주일 뒤의 시험을 설계한다

bilalabdullahi의 물음이 이 스킬을 평가하는 가장 좋은 출발점이다.
이 문서의 제안은 같은 주제를 이 스킬로 배운 집단과 모델의 일반 설명으로 배운 집단으로
나누어 사전 시험과 즉시 사후 시험과 일주일 뒤 시험을 같은 문항으로 치르게 하는 것이다.
Anthropic의 학습 연구가 쓴 문항 유형(디버깅, 코드 읽기, 코드 작성, 개념)을 코드 학습
주제에 그대로 쓸 수 있다.[^anth-skill]
이 설계는 이 문서의 제안이고, 이 문서나 스킬 저장소가 수행한 것이 아니다.

### 한 줄 버전과 전체 스킬을 비교해 본다

arshxyz의 한 줄과 quibono의 세션 끝에 가장 어려운 질문 몇 개를 만들어 달라는 요청이
전체 스킬을 얼마나 대체하는지 알면 도입 비용이 정해진다.[^arshxyz][^quibono-vanilla]
이 문서의 제안은 위 일주일 시험의 세 번째 집단으로 이 한 줄 버전을 넣는 것이다.
한 줄 버전이 같은 결과를 내면 이 스킬의 나머지는 사용성의 편의이다.

### 이 스킬을 쓰기 전에 에이전트의 지원 범위를 정한다

이 스킬은 도구가 있는 환경에서 사용자의 실제 출력을 확인하라고 한다.
이 문서의 제안은 코드 학습처럼 출력이 확인되는 주제에는 이 스킬이 잘 맞고,
출력이 없는 개념이나 철학 주제에는 간격 복습과 최종 평가의 질이 모델의 판정에만 달려 있다는
점을 알고 쓰는 것이다.
Osmani가 에이전트 시대의 판단 연습으로 권하는 것(결과를 읽기 전에 가설을 세우고, 요약 대신
스스로를 시험하는 것)을 이 스킬이 대화로 구조화한 것으로 읽을 수도 있다.[^osmani]
이 연결은 이 문서의 해석이다.

---

[^readme]: Jane Street, [Agent skills from Jane Street (README)](https://github.com/janestreet/agent_skills/blob/master/README.md)

[^contributing]: Jane Street, [Contributing](https://github.com/janestreet/agent_skills/blob/master/CONTRIBUTING.md)

[^anth-skill]: Anthropic, [How AI assistance impacts the formation of coding skills](https://www.anthropic.com/research/AI-assistance-coding-skills), 2026-01-29

[^osmani]: Addy Osmani, [Critical thinking when agents do the work](https://twitter.com/addyosmani/status/2117512471930167377), 2026-11-03

[^pbronez]: <https://news.ycombinator.com/item?id=50466487>

[^arshxyz]: <https://news.ycombinator.com/item?id=50464352>

[^genxy]: <https://news.ycombinator.com/item?id=50464568>

[^nilsherzig]: <https://news.ycombinator.com/item?id=50464730>

[^lemax]: <https://news.ycombinator.com/item?id=50465114>

[^bilal]: <https://news.ycombinator.com/item?id=50465464>

[^vaskebjorn]: <https://news.ycombinator.com/item?id=50466773>

[^imanari]: <https://news.ycombinator.com/item?id=50464688>

[^igleria]: <https://news.ycombinator.com/item?id=50464799>

[^pkoird]: <https://news.ycombinator.com/item?id=50466754>

[^mw888]: <https://news.ycombinator.com/item?id=50464553>

[^jkhdigital]: <https://news.ycombinator.com/item?id=50464600>

[^vkgcr]: <https://news.ycombinator.com/item?id=50465447>

[^quibono-found]: <https://news.ycombinator.com/item?id=50467504>

[^ngruhn]: <https://news.ycombinator.com/item?id=50464303>

[^orbis]: <https://news.ycombinator.com/item?id=50438436>

[^beans6543]: <https://news.ycombinator.com/item?id=50463915>

[^burrish]: <https://news.ycombinator.com/item?id=50465311>

[^orbis2]: <https://news.ycombinator.com/item?id=50465810>

[^poilcn]: <https://news.ycombinator.com/item?id=50464050>

[^michelb]: <https://news.ycombinator.com/item?id=50464725>

[^mikhail]: <https://news.ycombinator.com/item?id=50464180>

[^awongh]: <https://news.ycombinator.com/item?id=50466370>

[^skybelow]: <https://news.ycombinator.com/item?id=50465796>

[^pimeys]: <https://news.ycombinator.com/item?id=50464715>

[^koolba]: <https://news.ycombinator.com/item?id=50465521>

[^nathell]: <https://news.ycombinator.com/item?id=50465642>

[^quibono-vanilla]: <https://news.ycombinator.com/item?id=50465096>
