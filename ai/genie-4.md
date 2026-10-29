# Genie 4: 소리와 대화까지 실시간으로 만드는 월드 모델

원문: [Genie 4: A new generation of world simulation — Google DeepMind](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/)

HN 토론: <https://news.ycombinator.com/item?id=50261319> (1022점, 581개 댓글)

GN 토론: <https://news.hada.io/topic?id=36119>

## 요약

Google DeepMind가 2026년 10월 27일 Genie 4를 발표했다.
Raia Hadsell, Diego Rivas, Hang Qi가 쓴 발표문은 Genie 4를 실시간 상호작용
시뮬레이션을 만드는 월드 모델(world model)로 소개한다.
화면과 함께 음악, 환경음, 대화를 동시에 생성하는 네이티브 멀티모달(natively
multimodal) 모델이라고 한다.
Gemini Omni가 실제 세계의 외형과 행동을 잡아 주고,
다른 Gemini 모델이 시뮬레이션의 일관성(coherence)과 연속성(continuity)을
유지하는 추론을 맡는다.

발표문은 네 가지 능력을 내세운다.
첫째는 실시간 조정이다.
사용자는 키보드로 이동과 카메라를 조작하고,
텍스트로 날씨를 바꾸거나 사람이나 물체를 추가한다.
Gemini가 입력을 주변 장면에 맞게 고쳐 쓰고,
입력 사이에도 장면이 이어지도록 진행을 살핀다.
둘째는 물리와 인간 행동이다.
공기역학과 충돌 같은 물리 상황을 시뮬레이션하고,
사람이 자연스럽게 움직이고 반응한다고 한다.
셋째는 소리다.
Genie 4는 오디오를 자체 생성하는 첫 실시간 월드 모델이며,
입력과 사건에 따라 달라지는 대화도 실시간으로 만든다.
넷째는 Gemini 모델과 결합한 복합 사건 시뮬레이션이다.

네 번째 능력에서 Gemini 3.8 Flash는 루프 안에서 안내하는 에이전트(guiding agent)
역할을 한다.
Genie 4가 세계를 만드는 동안 Gemini가 장면을 계속 관찰하고,
목표를 단계로 나누고, 들어오는 프레임을 검토해 각 단계의 성공을 확인한다.
세계가 바뀌거나 사용자가 개입하면 Gemini가 계획을 즉석에서 고친다.
발표문은 Gemini 4 Argon이 사용자의 과제를 단계로 쪼개 텍스트 캡션으로 Genie 4에
넣는 예도 든다.
예로 든 것은 Apptronik의 휴머노이드 Apollo가 체커를 두는 장면이다.

발표문은 시험 사용자(trusted testers) 의견도 싣는다.
영화 제작자는 장면을 라이브 시뮬레이션으로 만들어 촬영 각도, 조명,
대사를 바꿔 가며 여러 테이크를 돌린다.
사진기자는 2D 기록 사진 한 장을 그 환경의 시뮬레이션으로 바꾼다.
게임 개발자는 엔진 코드를 쓰기 전에 탐색 가능한 시제품을 만든다.
기업 파트너는 시나리오를 처음부터 빠르게 만드는 용도를 평가한다.
앞으로의 방향으로는 언어 모델의 구조적 추론과 픽셀 단위 시뮬레이션을 합치는
하이브리드 월드 모델(hybrid world models)을 제시한다.

모든 영상과 오디오에는 SynthID 워터마크가 들어가며,
출시 전에 내부 안전 평가를 거쳤다고 한다.
한계로는 긴 세션이나 복잡한 프롬프트 수정 뒤,
장면을 돌아다닐 때 시각적 세부와 대상 영속성(object permanence)이 흔들릴 수
있다고 적는다.[^object-permanence]
복잡한 물리 상호작용, 실시간 오디오 정확도, 읽을 수 있는 글자, 공간 정확도,
장기 일관성도 연구 중인 과제로 든다.
현재는 연구 프리뷰(research preview)로 시험 사용자에게만 열려 있고,
이후 Project Genie의 Google AI Ultra 구독자와 Gemini API 및 Google AI Studio의
조기 접근 파트너에게 열린다.

## 분석

### 발표문의 중심 주장은 생성과 추론을 한 루프에 묶었다는 것이다

Genie 4의 새 점은 화질이나 소리만이 아니다.
발표문이 구조적으로 강조하는 것은 Genie가 그리고 Gemini가 지켜본다는 분업이다.
Genie는 다음 프레임을 만들고, Gemini는 그 프레임이 계획한 단계와 맞는지 확인하고
다음 캡션을 넣는다.
미래 방향으로 제시한 하이브리드 월드 모델은 이 분업을 이름 붙인 것이다.
발표문은 Gemini가 구조와 서사 시간표를 맡고 Genie가 눈앞의 물리적 현실을 픽셀
단위로 만든다고 설명한다.

이 구도는 Genie 단독으로는 긴 시간의 일관성을 보장하지 못한다는
인정을 담고 있다.
한계 절이 대상 영속성과 장기 일관성을 미해결 과제로 적은 것과 이어진다.
추론 모델이 계획을 쥐고 있으면, 픽셀 모델이 흔들려도 다음 캡션으로 되돌릴 수
있다는 것이 암묵적 가정이다.

### 두 종류의 쓰임새가 서로 다른 정확도를 요구한다

발표문은 쓰임새를 두 갈래로 든다.
하나는 로봇과 에이전트의 훈련 환경이다.
다른 하나는 영화 사전 시각화, 게임 시제품 같은 창작 도구다.

두 갈래가 요구하는 기준은 정반대다.
창작에서는 그럴듯하게 보이고 입력에 반응하면 충분하며,
틀린 장면은 다시 뽑으면 된다.
훈련 환경에서는 물체가 어디로 움직이고 어떤 수가 유효한지가 맞아야 하고,
틀린 장면은 잘못된 정책을 가르친다.
발표문의 사례는 휴머노이드의 체커 장면이지만 훈련 결과나 정확도 수치는 없다.

### 공개된 근거는 선별한 영상이다

발표문은 파라미터 수, 해상도, 프레임 속도, 세션 길이 같은 수치를 싣지 않는다.
증거는 영상 클립과 프롬프트 전문이다.
프롬프트가 길고 세밀하다는 점은 클립이 반복 시도 끝에 고른 결과일 수 있음을
시사하지만, 발표문은 시도 횟수를 밝히지 않는다.
한계 절의 문장은 일반적인 서술이며 실패 사례 영상은 없다.

### 한국어판은 같은 본문을 옮기며 용어를 정했다

구글코리아 블로그는 10월 28일 같은 글의 한국어판을 올렸다.[^korean]
영문판의 저자는 세 명인데, 한국어판에는 저자로 Raia Hadsell만 적혀
있다.[^korean]
한국어판은 object permanence를 대상 영속성(object permanence)으로,
guiding agent를 시뮬레이션을 이끄는 에이전트(guiding agent)로 옮겼다.[^korean]
오디오 절에서는 natively를 자체적으로(natively)로 풀었다.[^korean]

영문판의 audio-like music은 HN에서 뜻이 불분명하다는 지적을 받았다.
gradascent는 음악 같은 오디오를 뜻하는 것이냐고 물었고,[^gradascent] gcanyon은
하이픈으로 이어진 이 표현이 무엇을 가리키는지 되물었다.[^gcanyon]
한국어판은 이 표현을 음악과 주변 환경음,
인터랙티브 대화 등 다양한 오디오 요소로 풀어 써서 그 모호함이 사라졌다.[^korean]
그 밖에 본문 구조와 한계, 접근 방식은 영문판과 같고,
한국어판에도 파라미터 수나 해상도, 프레임 속도 같은 수치는 없다.[^korean]

## 비평

### 조종이 보인다는 주장은 데모에서 확인되지 않는다

발표문은 사용자가 키보드와 텍스트로 장면을 조종한다고 말한다.
HN에서는 화면에 표시된 키 위젯이 실제 움직임과 대응하지 않아 보인다는
지적이 나왔다.
sodacanner는 Genie 3보다 조종성이 나빠 보이며 AI 영상 위에 키 위젯을 얹은 것
같다고 적었다.[^sodacanner]
tempfile은 WASD와 화살표 표시가 캐릭터나 카메라의 움직임과 관계없이 깜빡이기만
한다고 말했다.[^tempfile]

물리 시연도 같은 의문을 받았다.
mlmonkey는 대리석 흉상을 수박에 떨어뜨리는 클립의 특정 시점에서 물리가 맞다면
흉상이 넘어졌어야 한다고 짚었다.[^mlmonkey]
dsissitka는 그 클립이 보여 주려던 것은 조종(steering)이라고
반박했다.[^dsissitka]
stevemk14ebr은 그래도 발표문이 물리를 모델링한다고 말한 이상 그 비판은
유효하다고 답했다.[^stevemk14ebr]
두 입장 모두 틀린 것이 아니다.
다만 조종 시연과 물리 시연을 한 클립에 겹치면 둘 중 어느 쪽도 검증되지 않는다.

### 대상 영속성 문제는 한계 절의 한 줄보다 크다

발표문은 대상 영속성이 흔들릴 수 있다고 적지만,
HN 사용자들은 시연 영상 안에서 이미 그 사례를 찾았다.
inkcapmushroom은 화면 밖으로 나갔다 돌아오면 세부가 바뀐다고 정리했다.
용 영상에는 성이 하나 더 생기고, 기차 승강장에서는 멀어지던 사람들이 바뀌고,
오토바이 운전자는 없던 헬멧을 쓴다는 것이다.
그는 화면 안의 일관성은 좋지만 그것이 강한 세계 시뮬레이션을 가졌다는 증거는
아닌 것 같다고 덧붙였다.[^inkcapmushroom]
smusamashah는 용을 타고 날 때 카메라를 돌리자 성 오른쪽의 큰 부분과 투석기가
사라졌다고 시각을 특정해 적었다.[^smusamashah]

cvoss는 모델의 시뮬레이션이 렌더링 가능한 영역에 갇혀 있는 것처럼
보인다고 진단했다.
시점 둘레 전체를 렌더링해 일부 오류를 줄일 수는 있어도,
다른 물체에 가려지는 순간 대상이 제멋대로 바뀌는 문제는 장면 전체의 3D 모델
없이는 안정되기 어렵다는 것이다.[^cvoss]
recursive는 어렵지 않았다면 제품 발표 데모에 넣었을 것이라고
반박했다.[^recursive]
msabalau는 이 글을 제품이 아니라 연구 성과를 공유하는 연구소 글로 읽어야 한다고
했다.[^msabalau]
어느 쪽이든 발표문이 쓴 월드 시뮬레이션(world simulation)이라는 표현은 장면이
화면 밖에서도 유지된다는 뜻으로 읽히는데, 영상은 그 뜻을 지지하지 않는다.

### 훈련 환경이라는 주장은 가장 약하게 뒷받침된다

발표문은 Genie 4가 로봇과 에이전트의 훈련 환경을 만드는 데 쓰인다고 말하고,
체커 장면을 사례로 든다.
Kotlopou는 그 클립이 훈련용이라면 물리가 한참 부족하다고 지적했다.
첫 말을 집을 때 말이 판에서 올라가는 듯하다가 그렇지 않게 되고,
마지막 수는 체커 규칙에 맞지 않는다는 것이다.[^kotlopou]
sosodev는 현실을 대표하지 않는 시연으로 로봇 훈련을 말하는 것이 문제라고
썼다.[^sosodev]

반론도 있었다.
overfeed는 이 계열 기술의 비공개 버전이 이미 Waymo의 자율주행 차량 훈련에
쓰인다고 적었다.[^overfeed]
이것이 사실이라면 훈련 환경 용도 자체는 근거가 있다.
다만 그 댓글이 말하는 쓰임새는 부족한 상황을 채우는 보조 용도이고,
월드 모델만으로 로봇을 훈련한다는 주장과는 다르다.
이 문서는 Waymo 쪽 글을 직접 열어 보지 않았다.

### 기술 정보와 접근 방식은 발표문이 정해 놓은 한계다

kouteiheika는 기술 정보가 전혀 공개되지 않은 또 하나의 비공개 모델이며,
사용 한도도 구글 직원이 아니면 쓸모없을 만큼 작을 것 같다고
비판했다.[^kouteiheika]
estearum은 첨단 기술이 대체로 불투명하고 제한적으로 배포되어 왔다고
반박했다.[^estearum]
dotancohen은 이 기술에는 널리 배포된 가까운 오픈 경쟁자가 있다는 점이 다르다고
재반박했다.[^dotancohen]
WarmWash는 Genie가 주로 내부 용도로 만들어졌고 외부 접근은 피드백, 훈련 데이터,
홍보를 위한 것이라고 의심했다.[^warmwash]
이 의심은 추측이다.
발표문의 사실은 시험 사용자에게만 열려 있고,
접근권은 Ultra 구독자와 조기 접근 파트너에게 순서대로 넓어진다는 것까지다.

## 인사이트

### 월드 모델이라는 이름은 정의 싸움이 이미 시작됐다는 신호다

jackb4040은 구글이 월드 모델을 텍스트에서 비디오게임을 만드는 방식으로 다시
정의한다고 보았다.
그는 이것이 Yann LeCun의 월드 모델 정의에 담긴 LLM 한계 주장을 가리려는 시도로
읽힌다고 썼다.[^jackb4040]
aryehof는 자신은 월드 모델을 결과를 예측하는 모델로 이해하며,
이 모델이 LLM인지 예측 모델인지 하이브리드인지 되물었다.[^aryehof]
발표문의 하이브리드 월드 모델이라는 표현은 그 질문에 대한 사실상의 답이다.
픽셀을 만드는 모델과 구조를 쥔 언어 모델을 합쳐야 한다고 스스로 말하고
있기 때문이다.

이 표현을 쓰는 순간 월드 모델의 정의가 물리적 상태를 예측하는 모델에서 그럴듯한
장면을 이어 만드는 시스템으로 넓어진다.
이름이 같아도 평가 기준이 다르다.
앞의 정의는 틀린 예측이 곧 오류지만, 뒤의 정의에서는 틀린 장면이 곧
오류가 아니다.
이 구분은 이 문서의 해석이며 발표문이 주장하는 것은 아니다.

### 같은 계열 모델이 서로를 검증하면 오류가 함께 움직일 수 있다

Genie 4와 Gemini의 루프에서 Gemini는 프레임을 검토해 각 단계의 성공을 확인한다.
체커 장면처럼 생성이 규칙에 어긋난 경우에도 검토하는 쪽이 같은 계열 모델이면
잘못된 장면을 성공으로 판정할 수 있다.
Kotlopou가 본 부자연스러운 말의 움직임과 규칙에 어긋난 마지막 수는 이 위험의
구체적인 사례일 수 있다.[^kotlopou]
이것은 이 문서의 추론이다.

이 문제가 중요한 이유는 훈련 환경 용도 때문이다.
검증기가 생성기와 같은 오류를 공유하면, 훈련 신호에서 그 오류는 정답으로 굳는다.
alphabetting은 실제 뉴스가 놀이 요소보다 임체 에이전트용 합성 훈련 데이터가 거의
가능해졌다는 데 있다고 읽었다.[^alphabetting]
그 읽기가 맞으려면 검증을 모델 밖의 규칙이나 실측으로 하는 방법이 필요하다.

### 하이브리드는 게임 엔진이 이미 가진 구조를 다시 만드는 길이다

monk_grilla는 3D 모델과 가상 카메라와 물리 시뮬레이션을 배치하면 일관성과
현실성이 더 좋을 것이라고 비꼬았다.[^monk_grilla]
비꼼에도 알맹이가 있다.
게임 엔진은 장면 상태를 렌더링과 분리해 쥐고 있어서,
카메라가 돌아와도 같은 성이 같은 자리에 있다.
Genie 4가 대상 영속성을 얻으려면 어떤 형태로든 장면 상태를 모델 밖이나 안에 따로
유지해야 한다.
Gemini가 구조를 맡는 하이브리드 구상은 이 방향의 첫걸음으로 읽힌다.

spwa4는 시뮬레이터를 만들어 모델을 훈련하는 접근은 결국 시뮬레이터를 내부에서 더
잘 수행하는 모델에 밀린다고 주장했다.[^spwa4]
이 주장이 맞다면 월드 모델 연구는 오래 쓰일 자산이 아니라 과도기의 도구다.
틀리다면 장면 상태를 명시적으로 쥐는 쪽이 이긴다.
둘 중 무엇이 맞는지는 발표문만으로 가려지지 않는다.

### 이 글을 읽는 방법

Genie 4를 평가하려는 팀이라면 접근권을 얻은 뒤 두 가지를 먼저 시험할 수 있다.
같은 장면에서 카메라를 돌려 화면 밖으로 내보냈다가 되돌렸을 때 물체가
그대로인지, 규칙이 있는 과제(체커 같은)에서 모델이 규칙 위반을 스스로
걸러내는지다.
NitpickLawyer가 든 로봇 훈련 환경 용도도 이 둘이 통과돼야
성립한다.[^nitpicklawyer]
둘 다 통과하지 못하면 이 모델의 가치는 창작 초안에 머문다.
반대로 긴 세션에서도 통과하면 월드 시뮬레이션이라는 표현이 설득력을 얻는다.

---

[^object-permanence]: 원문은 object permanence이다. 발달심리학에서 눈에 보이지 않아도 대상이 계속 존재한다는 인식을 뜻하는 용어이고, 여기서는 화면 밖으로 나갔다 돌아온 물체가 같은 모습으로 유지되는 성질을 가리킨다. 영속성이라는 번역어는 영구히 보존된다는 뜻으로 읽힐 수 있어서 영어를 함께 적었고, 한국어 용어는 구글코리아 블로그 한국어판이 쓴 대상 영속성을 따랐다.

[^korean]: 구글코리아 블로그, [지니 4(Genie 4): 월드 시뮬레이션의 새로운 세대](https://blog.google/intl/ko-kr/company-news/technology/genie-4-a-new-generation-of-world-simulation-kr/), 2026-10-28

[^gradascent]: <https://news.ycombinator.com/item?id=50262100>

[^gcanyon]: <https://news.ycombinator.com/item?id=50262977>

[^sodacanner]: <https://news.ycombinator.com/item?id=50261519>

[^tempfile]: <https://news.ycombinator.com/item?id=50262835>

[^mlmonkey]: <https://news.ycombinator.com/item?id=50261683>

[^dsissitka]: <https://news.ycombinator.com/item?id=50262444>

[^stevemk14ebr]: <https://news.ycombinator.com/item?id=50263423>

[^inkcapmushroom]: <https://news.ycombinator.com/item?id=50266032>

[^smusamashah]: <https://news.ycombinator.com/item?id=50261864>

[^cvoss]: <https://news.ycombinator.com/item?id=50266341>

[^recursive]: <https://news.ycombinator.com/item?id=50266478>

[^msabalau]: <https://news.ycombinator.com/item?id=50273601>

[^kotlopou]: <https://news.ycombinator.com/item?id=50263035>

[^sosodev]: <https://news.ycombinator.com/item?id=50263578>

[^overfeed]: <https://news.ycombinator.com/item?id=50263934>

[^kouteiheika]: <https://news.ycombinator.com/item?id=50261912>

[^estearum]: <https://news.ycombinator.com/item?id=50262492>

[^dotancohen]: <https://news.ycombinator.com/item?id=50262643>

[^warmwash]: <https://news.ycombinator.com/item?id=50262109>

[^jackb4040]: <https://news.ycombinator.com/item?id=50261898>

[^aryehof]: <https://news.ycombinator.com/item?id=50270054>

[^alphabetting]: <https://news.ycombinator.com/item?id=50262142>

[^monk_grilla]: <https://news.ycombinator.com/item?id=50267295>

[^spwa4]: <https://news.ycombinator.com/item?id=50262307>

[^nitpicklawyer]: <https://news.ycombinator.com/item?id=50261708>
