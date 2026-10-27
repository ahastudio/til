# GPT-6.1 Terra: 비용 대비 지능의 새 균형을 내세운 중간급 모델과 이름 체계 논쟁

원문: [Introducing GPT-6.1 Terra | OpenAI](https://openai.com/index/introducing-gpt-6-1-terra/)

HN 토론: <https://news.ycombinator.com/item?id=50248124> (501점, 320개 댓글)

## 요약

OpenAI가 2026년 10월 26일에 올린 GPT-6.1 Terra 발표문이다.
Terra는 상세한 시각 추론과 정밀한 컴퓨터 조작, 더 명료하고 자연스러운 글쓰기를
결합한 빠르고 효율적인 모델이라고 소개된다.
GPT-5.6 Terra보다 크게 나아졌고, 제안서 작성이나 기술 도면 해석, 양식 입력, 영상
편집처럼 업무일에 많은 소통과 컴퓨터 작업에 강하다고 한다.
표준 API 가격은 GPT-5.6 Terra와 GPT-6.1 Sol보다 50% 낮고, 입력 100만 토큰당
1달러, 캐시된 입력 100만 토큰당 0.05달러, 출력 100만 토큰당 5달러다.
ChatGPT Work와 Codex에서는 같은 사용량 한도로 GPT-5.6 Terra보다 더 많은 일을
하고, GPT-6.1 Sol이나 GPT-6 Astra보다는 훨씬 많은 일을 한다고 한다.

성능 주장은 세 가지다.
컴퓨터 사용은 Agents' Last Exam(건축 도면을 3D 모델로 바꾸기, 애니메이션 영화를
샷 단위로 검토해 시간 코드 기록 만들기 같은 전문 과제 모음)에서 중간 추론 강도일
때 GPT-5.6 Terra보다 15%포인트 높고 비용은 약 3분의 1이다.
이 점수는 토큰당 가격이 10분의 1인 GPT-6 Astra와 대등하다.
최대 강도에서는 Claude Opus 5.5보다 토큰 효율이 3배 넘고 토큰당 가격이 4분의
1이어서 과제당 비용이 약 9배 낮고, 과제 완료는 GPT-6 Astra와 GPT-6.1 Sol보다 3배
넘게 빠르다.
MMMU-Pro(시각 추론)에서는 모든 추론 설정에서 GPT-5.6 Terra를 앞서고 GPT-6
Astra와 GPT-6.1 Sol에 근접한다.
OSWorld 2.1(데스크톱 앱 다단계 작업)에서는 중간 강도에서 GPT-5.6 Terra의 최고
점수를 훨씬 낮은 과제당 비용으로 넘는다.

사실성과 코딩도 개선되었다고 한다.
오류를 유도하는 프롬프트의 사내 벤치마크에서 낮은 추론 강도의 오류율이 GPT-5.6
Terra의 53.6%에서 16.7%로, 최대 강도에서는 18%포인트 떨어져 4.3%가 되어 GPT-6
Astra와 GPT-6.1 Sol에 근접했다.
Terminal-Bench 4.0에서는 최대 강도에서 과제의 50.3%를 풀어 GPT-5.6 Terra의 공개
점수 21.5%의 두 배가 넘는다.
다만 가장 복잡한 코딩 과제에는 GPT-6.1 Sol과 GPT-6 Astra가 여전히 더 낫다고
밝힌다.
Terminal-Bench-Science 0.1에서는 최대 강도에서 GPT-6.1 Sol을 더 낮은 비용으로
넘고 Opus 5.5에 5점 이내로 다가가면서 추정 비용은 5분의 1 미만이다.
안전 면에서는 사이버보안에서 Preparedness Framework의 Critical 기준에 해당하고,
GPT-6 Astra의 보호 조치를 유지하며, 범위를 지키고 한계를 솔직하게 밝히는 경향과
프롬프트 주입 저항이 좋아졌다고 한다.
Plus, Pro, Enterprise, Edu 사용자는 ChatGPT Work와 Codex에서 오늘부터 쓸 수
있고, API 모델 이름은 `gpt-6.1-terra`다.

## 분석

### 발표의 중심은 성능이 아니라 과제당 비용이다

발표문의 비교 지표는 대부분 점수 대비 비용, 곧 과제당 비용과 토큰 효율이다.
같은 점수를 더 싼 모델이 낸다는 서술이 반복되고, 상위 모델과의 비교도 대등한
점수에 10분의 1 가격이라는 틀로 나온다.
모델을 성능 순위가 아니라 비용 대비 지능의 전선(frontier) 위의 점으로 설명하려는
것이다.
HN에서 _aavaa_는 중요한 지표가 과제당 비용과 시간과 품질이며 자신은 토큰이
아니라 해결책을 사는 것이라고 했다.[^_aavaa_]
이는 이 문서의 해석이지만, 발표문 자체가 이 지표를 택했다는 점은 분명하다.

### 같은 세대 안에서 가격 계단을 낮추는 방식이 되풀이된다

minimaxir는 GPT-5.6 Sol에서 GPT-6.1 Sol로 간 것과 비슷한 75% 가격 인하
궤적이라고 짚었다.[^minimaxir]
mediaman은 6.1 Terra가 Sol 6.1보다 50% 싸고, 새 출시일수록 가격이 낮아지므로
같은 버전끼리 비교해야 한다고 했다.[^mediaman]
발표문이 비교 기준으로 GPT-5.6 Terra와 GPT-6.1 Sol을 함께 드는 이유가 여기에
있다.
세대가 바뀔 때마다 같은 등급이 더 싸진다는 구조라서, 가격표는 모델 이름보다 출시
시점에 더 크게 좌우된다.

### 모델을 효율 전선으로 설명하는 순간 이름 체계가 문제가 된다

발표문은 Terra를 비용, 지능, 속도의 새 균형이라고 하지만 Luna, Terra, Sol,
Astra와 버전과 추론 강도를 합친 3차원 선택지가 독자에게 남는다.
이 선택지를 어떻게 고르느냐가 HN 스레드의 가장 큰 논쟁이 되었다.

## 비평

### 이 발표의 비교는 비교 대상과 기준을 스스로 골랐다

중간 강도에서는 GPT-5.6 Terra와 비교하고, 최대 강도에서는 Claude Opus 5.5와
비교하며, 과제당 비용과 토큰 효율을 앞세운다.
Agents' Last Exam과 OSWorld 2.1, Terminal-Bench 4.0 같은 지표는 발표문이 설명한
범위 안에서만 제시되고, 일부 비용은 추정이라고 적혀 있다.
이 문서는 벤치마크 설정이나 원자료를 확인하지 못했다.
HN의 Starlevel004는 Terminal-Bench 4.0 결과가 나쁘다며 Terra 최고 강도가 Sol
낮은 강도보다 비싸면서 성적은 더 낮다고 읽었고,[^Starlevel004]
minimaxir도 그 비용 대 과제 결과가 혼란스러워 Sol 대신 Terra를 고를 이유를
모르겠다고 했다.[^minimaxir-sol]
같은 도표를 두고 효율이 앞선다는 발표와 효율이 뒤진다는 독해가 갈린다.

### 과제당 비용이라는 새 지표가 사용량 한도 축소를 가린다는 의심이 나왔다

mapontosevenths는 OpenAI가 최근 플랜 사용량을 약 50% 줄여 Anthropic이 플랜에서
약 5배 가치를 준다고 하며, 과제당 비용 지표는 사실상 비용을 두 배로 올리지 않은
것처럼 들리게 하는 말장난이라고 했다.[^mapontosevenths]
Archit3ch는 5배는 API 가격으로 계산한 것이고 대부분의 사용자는 보조금을 받는다고
반박했고,[^Archit3ch]
mapontosevenths는 원시 토큰으로도 Anthropic이 약 3배를 준다고
되받았다.[^mapontosevenths-tokens]
이 주장들은 이 스레드의 사용자 계산이고 이 문서는 어느 쪽도 검증하지 못했다.
다만 발표문이 사용량 한도를 토큰이 아니라 같은 한도로 더 많은 과제라고 표현한
것이 논쟁의 출발이다.

### 사실성 개선 수치는 내부 벤치마크에서만 나온다

오류율이 53.6%에서 16.7%로 떨어졌다는 수치는 오류를 유도하는 프롬프트의 사내
벤치마크에서 나왔다.
프롬프트 구성과 평가 방법은 발표문에 없다.
ape4는 factuality라는 단어에 빨간 밑줄이 쳐진다며 환각은 여전히 큰 문제라고
했다.[^ape4]
사용자의 체감과 사내 지표의 거리를 이 발표문은 메우지 않는다.

### 모델의 위치를 정하는 가이드가 없다

atombender는 기술 문서에는 Sol을 권하느냐고 물으며 어떤 기준으로 모델을 골라야
하는지 공개된 지침을 볼 수 없다고 했다.[^atombender]
tedsanders는 OpenAI 직원으로서 자신도 모르겠고 Terra가 가독성은 가장 좋을 수
있지만 Astra가 오류를 더 잘 잡을 수 있다고 답했다.[^tedsanders-docs]
flockonus는 OpenAI 직원이 직접 권고하지 못한다면 우리는 어떻게 평가하느냐고
되물었다.[^flockonus]
발표문은 어떤 일에 Terra를 쓰고 어떤 일에 Sol을 쓸지 일반 원칙을 주지 않는다.

## 인사이트

### 이름 체계는 크기 순서와 출시 시점이라는 두 축이 섞여 헷갈린다

Someone1234는 Luna, Terra, Sol, Astra의 소-중-대-초대 체계가 Sol 6.1이 때로
Astra보다 낫고 Astra 이전 모델이 단종되며 흐려졌다고 했다.[^Someone1234]
margalabargala는 모델이 가족 단위가 아니라 개별로 출시되어 Terra 6.1이 Sol 6을
이기는지, 한 달 뒤 Luna 6.2가 나오면 바꿔야 하는지 알 수 없다고
했고,[^margalabargala]
torben-friis는 추론 강도와 모델 등급의 상호작용, 그리고 새 모델이 옛 상위
모델보다 나은 시점을 이해하기 어렵다고 두 쟁점으로 정리했다.[^torben-friis]
OpenAI의 tedsanders는 성능이 다차원이어서 고정된 순서가 보장되지 않고, 변동의
많은 부분은 모델 크기 하나로 설명되며 큰 모델이 더 성능이 좋고 비싸고 느리다는
논리를 설명했다.[^tedsanders]
그는 이름 개선 제안을 환영한다고도 했는데,[^tedsanders-name]
Closi는 Small, Medium, Large 같은 이름이나 파라미터 수를 제안했고,[^Closi]
tedsanders는 Apple이 iPhone cheap이라 부르지 않듯 그런 이름은 브랜딩이 나쁘고
세대를 가로지르면 헷갈린다고 답했다.[^tedsanders-iphone]
이는 가격 계단을 이름에 담을지, 시점을 이름에 담을지의 선택이다.
이 문서의 해석이다.

### 선택의 비용이 사용자에게 넘어가며 가장 큰 모델을 기본값으로 쓰게 된다

elxr는 Sol을 낮음, 중간, 높음으로 쓰고 Terra는 실험해 보겠다고
했고,[^elxr-evals]
scarab92는 Astra 6 Extra High를 모든 일에 쓰며 모두 싸고 어느 설정이 맞는지
가려내는 데 머리를 쓰느니 계산을 낭비하겠다고 했다.[^scarab92]
bel_marinaio는 VM 대시보드를 컴퓨터 조작으로 점검할 모델과 설정을 GPT에게
물었는데 답이 Astra Medium, Sol Medium, 경로가 이미 알려진 경우만 Luna였다고
전했다.[^bel_marinaio]
선택지가 많고 지침이 없으면 사용자는 가장 큰 설정으로 후퇴하고, 이는 중간급
모델이 시장에서 설 자리를 줄인다.
Silagi는 Terra가 존재할 이유를 묻고, 한 단계 올리고 추론을 낮추거나 한 단계
내리고 추론을 올리는 편이 더 낫다고 했다.[^Silagi]
반대로 elxr는 Terra와 Luna가 주니어 개발자 업무의 절반 이상에 충분히 싸고 좋다고
했다.[^elxr]
이는 이 문서의 해석이다.

### 용도에 따라 중간급 모델의 가치가 갈린다

h14h는 구독 한도 안에서 코딩 에이전트를 쓰는 대부분의 사용자에게는 이유가 없을
수 있지만, Terra가 한도에 기여하는 방식에 따라 반복 작업의 일부에 쓰면 구독을 더
오래 쓸 수 있다고 했고,[^h14h]
rfgplk는 간단한 작업을 맡겨 할당량의 큰 비율을 아낄 수 있다고 했다.[^rfgplk]
API로 제품을 만드는 쪽에서는 고용량의 정형 작업(송장 읽기와 회계 입력)에서 가격
차이가 직접 비용이 된다.
같은 모델이 구독자에게는 선택지의 소음이고 API 사용자에게는 마진이라는 점이 이
시장의 구조다.

### 이 글을 읽는 방법

이 문서는 발표문(직접 요청은 차단되어 Chrome으로 읽었다)과 HN 스레드(320개 댓글
가운데 긴 것과 대화가 이어진 165개)를 읽고 정리했다.
시스템 카드와 벤치마크 원자료는 열어 보지 못했다.
판단을 가를 관찰은 둘이다.
하나는 자기 업무에서 같은 과제를 Terra와 Sol로 돌려 정답률과 과제당 비용을
비교하는 것이다.
이것이 발표문의 9배 낮은 과제당 비용과 어디까지 맞는지가 판단의 근거다.
다른 하나는 사용량 한도가 같은 플랜에서 Terra로 처리되는 과제 수가 이전 모델
대비 실제로 늘었는지다.
둘 다 이 문서가 확인하지 못했다.

---

[^_aavaa_]: <https://news.ycombinator.com/item?id=50250125>

[^minimaxir]: <https://news.ycombinator.com/item?id=50248477>

[^mediaman]: <https://news.ycombinator.com/item?id=50248871>

[^Starlevel004]: <https://news.ycombinator.com/item?id=50248472>

[^minimaxir-sol]: <https://news.ycombinator.com/item?id=50248477>

[^mapontosevenths]: <https://news.ycombinator.com/item?id=50249789>

[^Archit3ch]: <https://news.ycombinator.com/item?id=50250233>

[^mapontosevenths-tokens]: <https://news.ycombinator.com/item?id=50251464>

[^ape4]: <https://news.ycombinator.com/item?id=50249040>

[^atombender]: <https://news.ycombinator.com/item?id=50249604>

[^tedsanders-docs]: <https://news.ycombinator.com/item?id=50250664>

[^flockonus]: <https://news.ycombinator.com/item?id=50252730>

[^Someone1234]: <https://news.ycombinator.com/item?id=50248491>

[^margalabargala]: <https://news.ycombinator.com/item?id=50249599>

[^torben-friis]: <https://news.ycombinator.com/item?id=50249434>

[^tedsanders]: <https://news.ycombinator.com/item?id=50249160>

[^tedsanders-name]: <https://news.ycombinator.com/item?id=50249160>

[^Closi]: <https://news.ycombinator.com/item?id=50250229>

[^tedsanders-iphone]: <https://news.ycombinator.com/item?id=50250457>

[^elxr-evals]: <https://news.ycombinator.com/item?id=50249948>

[^scarab92]: <https://news.ycombinator.com/item?id=50252957>

[^bel_marinaio]: <https://news.ycombinator.com/item?id=50251082>

[^Silagi]: <https://news.ycombinator.com/item?id=50248646>

[^elxr]: <https://news.ycombinator.com/item?id=50249457>

[^h14h]: <https://news.ycombinator.com/item?id=50249249>

[^rfgplk]: <https://news.ycombinator.com/item?id=50248853>
