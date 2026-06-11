# Grep만으로 충분한가? 에이전트 하네스가 에이전트 검색을 바꾸는 방식

<https://arxiv.org/abs/2605.15184>

HN 토론: <https://news.ycombinator.com/item?id=48460863> (142점, 59개 댓글)

## 요약

이 논문은 LLM 에이전트가 정보를 자율적으로 검색하고 도구를 호출하며
대규모 코퍼스를 추론해 사용자 작업을 대신 수행하는 에이전트 워크플로에서,
검색 전략(retrieval strategy) 선택이 에이전트 아키텍처 및 도구 호출
패러다임과 어떻게 상호작용하는지를 실증적으로 분석한다.
저자들은 RAG가 에이전트 검색 시스템에 빠르게 도입되고 있음에도,
검색 전략 선택이 에이전트 구조 및 도구 호출 방식과 맺는 관계를
체계적으로 비교한 연구가 부족하다는 점을 문제로 제기한다.
특히 도구 출력이 모델에 어떻게 제시되는지, 그리고 관련 없는 주변 텍스트가
늘어날 때 검색 성능이 어떻게 변하는지가 에이전트 루프 안에서
충분히 탐구되지 않았다고 지적한다.

핵심 비교 축은 grep 기반 검색과 벡터(vector) 검색이다.
grep은 문자열 패턴 매칭으로 코퍼스를 훑는 어휘적(lexical) 방식이고,
벡터 검색은 임베딩 유사도로 의미적으로 가까운 구절을 가져오는 방식이다.
저자들은 이 두 전략을 단독으로 평가하는 데 그치지 않고,
서로 다른 에이전트 하네스(harness)와 도구 결과 제시 방식이라는
변수와 교차시켜 평가한다.

실험 1은 LongMemEval에서 추출한 116개 질문 표본을 사용한다.
자체 제작 에이전트 하네스인 Chronos와,
제공자 네이티브 CLI 하네스인 Claude Code, Codex, Gemini CLI를 함께
비교한다. 또한 도구 결과를 프롬프트에 직접 끼워 넣는 인라인(inline) 방식과,
모델이 별도로 읽어 들이는 파일 기반(file-based) 방식 두 가지를 모두 본다.
실험 2는 grep 단독과 벡터 단독 검색을 비교하되,
무관한 대화 이력을 점진적으로 섞어 넣어 각 질의가 점점 더 많은
방해 자료(distracting material) 속에 묻히도록 만들어 강건성을 측정한다.

핵심 결과는 두 가지다. 첫째, 실험 1 전반에 걸쳐 Chronos와 제공자 CLI
모두에서 grep이 벡터 검색보다 대체로 더 높은 정확도를 보였다.
둘째, 그럼에도 전체 점수는 동일한 대화 데이터를 쓰더라도
어떤 하네스와 도구 호출 스타일을 쓰느냐에 강하게 의존했다.
즉 검색 전략 자체보다 그것을 감싸는 하네스의 구성이 성능을
좌우하는 큰 변수라는 것이 이 논문의 중심 주장이다.

논문의 기여는 검색 전략을 단일 변수로 떼어 평가하던 기존 RAG 문헌의
관행을 비판하고, 검색 방식 × 하네스 × 도구 결과 제시 방식이라는
삼자 상호작용을 실증적으로 드러낸 데 있다.
“grep이 벡터보다 낫다”는 단순 결론보다는, 검색 성능을 논할 때
하네스를 통제하지 않으면 비교가 무의미해진다는 메타적 경고가
실질적 메시지로 보인다.

## 분석

### 핵심 기여는 검색 전략이 아니라 “하네스 교란 변수”의 가시화다

표면적으로 이 논문은 grep과 벡터 검색의 대결처럼 읽힌다.
그러나 더 무게 있는 기여는 “동일한 데이터라도 하네스에 따라 점수가
크게 달라진다”는 관찰이다. 이는 RAG 평가에서 흔히 암묵적으로
가정되던 전제, 즉 검색기(retriever)의 품질이 최종 성능을 지배한다는
믿음을 흔든다. 저자들은 검색기를 독립 변수로 고정한 채 하네스를
바꾸면 결과가 출렁인다는 점을 보여줌으로써, 기존 벤치마크들이
교란 변수를 통제하지 못했을 가능성을 제기한다.

이 관점에서 보면 논문의 진짜 주장은 방법론적이다.
검색 전략을 평가하려면 하네스와 도구 호출 스타일을 함께 보고해야
하며, 그렇지 않은 비교는 재현성과 외적 타당성을 결여한다는 것이다.
이는 단순한 성능 수치보다 오래 살아남을 메시지다.

HN의 한 독자는 이 점을 표 차원에서 더 날카롭게 짚는다.
표 2와 표 3을 보면 프로그래밍에 맞춰 튜닝된 하네스(Codex, Claude
Code)에서는 grep이 이기지만, 중립적 하네스에서는 벡터 검색이
이긴다는 것이다[^skypuncher]. 즉 “grep이 낫다”는 결론 자체가
하네스에 종속된 조건부 명제이며, 같은 데이터로도 하네스를 바꾸면
승자가 뒤집힌다는 논문의 핵심 관찰이 표 수준에서 그대로 확인된다.
이 독자는 나아가 지금까지의 grep 대 RAG 논쟁이 대부분 교란 요인을
뭉뚱그렸다고 지적한다. 흔한 사례는 파이프라인을 처음부터 다시
지으면서 여러 문제를 함께 고친 경우이고, 최악은 단발성 RAG를
다단계 grep과 비교하면서 다단계 RAG였다면 비슷한 결과가 나왔을
가능성을 놓치는 경우라는 것이다[^skypuncher].

### 어휘 검색의 부활이라는 흐름 위에 서 있다

grep이 벡터를 이긴다는 결과는 고립된 발견이 아니다.
정보 검색 분야에서 BM25 같은 어휘적 베이스라인이 신경망 검색기를
종종 능가하거나 비등하다는 보고는 오래전부터 있었고,
코드 에이전트 영역에서는 ripgrep 같은 도구가 의미 검색보다
실용적이라는 경험적 합의가 형성되어 왔다.
이 논문은 그 흐름을 LongMemEval 기반의 장기 기억(long-term memory)
질의응답이라는 구체적 과제로 끌어와 재확인한다.

다만 이 연결은 양날의 검이다. 한편으로는 결과가 기존 직관과
정합적이어서 신뢰를 더한다. 다른 한편으로는 “grep이 자주 강하다”는
사실 자체가 이미 알려진 만큼, 논문의 신규성은 검색 전략 결론보다
하네스 상호작용 분석 쪽에 집중되어야 정당화된다.

이 경험적 합의의 한 단면은 Claude Code의 설계 결정에서도 읽힌다.
HN의 한 댓글은 초기 버전이 트리/구조 기반 검색을 쓰다가, grep이
더 낫거나 비등하면서도 복잡성이 적다는 것을 발견해 결국 grep을
탑재하는 쪽으로 갔다고 전한다[^krzyk]. 검색 품질의 우위뿐 아니라
구현·운영 복잡성의 절감이 어휘 검색 선택을 굳혔다는 실무적 정황이다.

### 도구 결과 제시 방식을 1급 변수로 끌어올린 점

인라인 대 파일 기반이라는 도구 결과 제시 축을 명시적 실험 변수로
다룬 것은 실무적으로 가치가 크다. 실제 에이전트 시스템에서는
검색 결과를 프롬프트에 직접 넣을지, 파일로 떨궈 모델이 읽게 할지가
컨텍스트 윈도 사용량, 비용, 그리고 주의 분산에 직결되는 결정이다.
이 차원은 학술 RAG 논문에서 거의 측정되지 않던 부분이다.

이를 통해 논문은 “검색 품질”이라는 단일 척도로는 포착되지 않는,
에이전트 루프 내부의 정보 전달 경로 자체가 성능 인자임을 시사한다.
다만 실험 1에서만 이 축을 다루고 실험 2에서는 검색 전략과
방해 자료에 집중하면서, 두 축이 교차할 때 무슨 일이 벌어지는지는
설계상 분리되어 있다.

### 두 실험의 분업 구조가 드러내는 가정

실험 1은 하네스와 제시 방식이라는 시스템 변수를, 실험 2는 방해
자료라는 데이터 난이도 변수를 각각 담당한다. 이 분업은 변수를
깔끔히 분리하려는 의도지만, 동시에 강한 가정을 깔고 있다.
즉 하네스 효과와 방해 자료에 대한 강건성이 서로 독립적이라는
가정이다. 현실의 에이전트에서는 방해 자료가 많아질수록 하네스의
도구 호출 전략이 더 중요해질 수 있어, 두 효과는 상호작용할
개연성이 높다. 논문 구조는 그 상호작용을 측정 범위 밖에 둔다.

## 비평

### 116개 질문 표본과 단일 벤치마크 의존이 결론의 일반화를 제약한다

가장 먼저 의심해야 할 지점은 표본 크기다. LongMemEval에서
추출한 116개 질문은 하네스 4종 × 검색 전략 2종 × 제시 방식 2종이라는
다수의 조건으로 쪼개지면 각 셀에 할당되는 질문 수가 급격히 줄어든다.
이 경우 셀 간 정확도 차이가 통계적으로 유의한지, 아니면 표본 변동에
불과한지를 구분하기 어렵다. 논문이 신뢰구간이나 유의성 검정을
제시하지 않는다면 “grep이 대체로 낫다”는 서술은 효과 크기 없이
방향성만 말하는 약한 주장에 머문다.

더 근본적으로 LongMemEval 단일 벤치마크에 의존한다는 점이 문제다.
이 벤치마크는 장기 대화 기억 회상에 특화되어 있어, grep 같은
어휘 매칭이 유리한 구조적 편향을 내포할 수 있다.
대화 이력에서 답이 특정 키워드나 표현으로 명시적으로 등장한다면
문자열 매칭이 임베딩 유사도보다 유리한 것은 당연하다.
도메인이 동의어, 의역, 다국어 질의가 많은 코퍼스로 바뀌면
순위가 역전될 여지가 크다. 단일 벤치마크 결과를
“agentic search 전반”으로 일반화하는 제목은 과도하다.

HN에서는 벤치마크 선택 자체가 grep에 유리하게 편향됐다는 지적이
구체적으로 나온다. 한 독자는 LongMemEval이 정확한 날짜, 개수,
선호, 토큰화 후에도 안정적으로 남는 구절 같은 “문자 그대로의 증거”
회수를 보상한다는 논문 문장을 인용하며, 결국 문자열 매칭에 유리한
벤치마크를 골라 grep이 잘했다는 결과를 보여준 셈 아니냐고 꼬집는다.
자전거 얘기 뒤 “bike”를 묻는 질의처럼 공통 토큰이 직접 맞아떨어지는
사례에는 grep이 강하지만, 베토벤 소나타 대화 뒤 “클래식 음악”을
묻는 식의 의미적 비약에는 임베딩이 빛난다는 것이다[^yetanotherjosh].
같은 맥락에서 다른 독자는 이 연구가 코드 검색이 아니라 여러 세션에
걸친 긴 대화에 대한 질의응답을 측정했을 뿐이라는 점을 명확히
짚으며, 프로그래밍 일반의 결론으로 읽지 말라고 경고한다[^quinncom].

### 벡터 검색 구현의 공정성이 결론을 좌우한다

grep과 벡터의 대결에서 결과는 벡터 파이프라인을 얼마나 잘
구성했는가에 극도로 민감하다. 임베딩 모델 선택, 청킹(chunking)
전략, top-k 값, 재순위화(reranking) 유무, 하이브리드 결합 여부가
모두 벡터 측 성능을 좌우한다. 만약 저자들이 기본 설정의 단순
벡터 검색을 grep과 맞붙였다면, 이는 잘 튜닝된 grep 대 덜 튜닝된
벡터의 비대칭 비교일 수 있다.

리뷰어 관점에서는 벡터 베이스라인의 구체적 구성과 튜닝 노력이
grep 측과 대칭적이었는지를 반드시 확인해야 한다.
실무에서 강한 RAG는 거의 항상 어휘 검색과 의미 검색의
하이브리드이며, 벡터 단독을 grep 단독과 비교하는 것은
실제로 쓰이는 시스템을 대표하지 못한다.
“grep만으로 충분한가”라는 질문은 하이브리드라는 명백한
세 번째 선택지를 비교에서 배제할 때만 의미를 갖는다.

### 자체 하네스 Chronos와 제공자 CLI의 비교 가능성이 불분명하다

Chronos는 저자들이 직접 만든 하네스이고, Claude Code, Codex,
Gemini CLI는 외부 제공자의 닫힌 시스템이다.
이 둘을 같은 표에 놓고 비교할 때, 제공자 CLI는 내부 프롬프트,
도구 정의, 컨텍스트 관리 방식이 블랙박스라 통제가 불가능하다.
따라서 “하네스에 따라 점수가 크게 달라진다”는 핵심 관찰이
검색 전략의 본질적 상호작용을 반영하는지, 아니면 단지 제공자별
구현 차이라는 잡음을 반영하는지 분리하기 어렵다.

또한 제공자 CLI는 평가 기간 동안 업데이트되면 결과 재현이
불가능해진다. 모델 버전과 하네스 버전을 고정하지 않은 비교는
시점 의존적 스냅숏일 뿐이다. 논문이 각 CLI의 정확한 버전과
설정을 명시하지 않으면, 표의 수치는 재현 가능한 과학적 결과가
아니라 특정 시점의 일화에 가깝다.

HN에서도 이 통제 불가능성을 정면으로 비판하는 목소리가 있다.
한 독자는 제목이 과대 포장됐다며, Chronos가 정확히 무엇인지,
어떤 임베딩 모델과 재순위기를 썼는지, 재순위가 어떻게 수행됐는지,
그리고 왜 Chronos가 Claude Code보다 훨씬 나은지가 불분명하다고
열거한다[^stephantul]. 이는 자체 하네스와 블랙박스 CLI를 한
표에 놓을 때 빠지는 핵심 정보가 무엇인지를 그대로 보여준다.

### 정확도 단일 지표로는 에이전트 검색의 실질을 평가하기 어렵다

평가가 정확도(accuracy) 중심으로 보이는 점도 약점이다.
에이전트 검색에서 실무적으로 중요한 것은 정답률만이 아니라
지연 시간, 토큰 비용, 도구 호출 횟수, 그리고 컨텍스트 점유량이다.
grep이 정확도에서 약간 앞선다 해도, 대규모 코퍼스에서 grep이
반환하는 매칭 수가 폭증해 컨텍스트를 잠식한다면 비용 효율은
벡터가 우월할 수 있다. 단일 지표 비교는 이 트레이드오프를 가린다.

HN의 실무자들도 같은 트레이드오프를 강조한다. 한 독자는 grep이
대체로 더 높은 정확도를 낸다는 결과에 대해, 그것은 훨씬 더 많은
토큰을 더 느리게 컨텍스트로 빨아들인 대가일 뿐이라고 지적하며,
tree-sitter, PageRank, LSP처럼 의미 지도를 구축해 더 관련성 높은
컨텍스트를 제공하는 방식과 비교돼야 한다고 주장한다[^badcafebee].
관련 연구를 인용한 다른 댓글은 토큰을 신경 쓰지 않고 파일이 10만 개
미만이라면 grep이 괜찮지만 그 규모를 넘으면 무너진다고 정리하며,
grep+에이전트 조합이 BM25 검색 엔진보다 약간 나은 관련성을 주는
대신 토큰을 많이 먹는다고 경험을 덧붙인다. 더 나아가 그는 grep이
잘 통하는 이유의 절반은 사람들이 콘텐츠를 찾기 쉽게 조직하도록
유인된 결과이며, 그렇게 찾을 수 있게 만드는 작업 자체가 검색
구축의 절반이라고 본다[^softwaredoug].

또한 방해 자료를 늘리는 실험 2에서 강건성을 측정한다고 하지만,
강건성을 정확도 하락폭으로만 본다면 그 하락이 검색 실패에서
오는지, 아니면 늘어난 컨텍스트로 인한 모델 추론 저하에서 오는지를
귀속(attribution)하기 어렵다. 검색 단계의 재현율(recall)과
최종 응답 정확도를 분리해 보고하지 않으면, 어느 단계가
병목인지에 대한 인과적 해석이 흐려진다.

## 인사이트

### “검색기가 아니라 하네스가 변수다”는 결론은 RAG 평가의 측정 단위를 바꾼다

이 논문의 가장 오래 살아남을 함의는 검색 전략 순위가 아니라,
RAG 성능을 보고할 때의 분석 단위에 대한 것이다.
지금까지 RAG 논문은 검색기를 단위로 삼아 “이 검색기가 더 좋다”고
말해 왔다. 그러나 동일 검색기가 하네스에 따라 출렁인다면,
적절한 분석 단위는 (검색기 × 하네스 × 제시 방식)이라는 조합이지
검색기 단독이 아니다. 이는 통계학에서 교란 변수를 통제하지
않은 비교가 무효라는 원리의 에이전트 버전이다.

이 시각을 받아들이면 향후 RAG 벤치마크는 검색기 leaderboard가
아니라, 하네스를 명시적으로 고정하거나 무작위화한 요인 설계
(factorial design)로 보고해야 한다. 논문이 직접 이 처방을
내리지는 않더라도, 그 방향을 강하게 시사한다는 점에서 가치가 있다.

### grep의 승리는 “구조화되지 않은 도구가 에이전트에 더 잘 맞는다”는 이차 효과를 드러낸다

grep이 벡터를 이긴 이유를 검색 품질만으로 설명하는 것은 표면적이다.
더 깊은 가설은 grep이 에이전트의 반복적 도구 호출 루프와 궁합이
좋다는 것이다. grep은 결정론적이고 투명해서, 모델이 패턴을 바꿔
재시도하며 결과를 점진적으로 좁혀 갈 수 있다.
반면 벡터 검색은 한 번에 top-k를 던지는 단발성에 가깝고,
유사도 점수가 모델에게 불투명해 재시도 전략을 세우기 어렵다.

이 관점은 도구 설계 원칙으로 일반화된다. 즉 에이전트용 도구는
출력이 높은 정밀도를 갖기보다, 모델이 조합하고 반복하며
스스로 보정할 수 있는 형태여야 유리할 수 있다.
이는 사람이 한 번에 정답을 받기보다 검색을 여러 번 다듬는
방식과 닮았으며, 도구를 “한 방의 정답기”가 아니라
“탐색 루프의 한 스텝”으로 설계해야 한다는 시사를 준다.

HN에는 이 구도를 “둘 다 주면 된다”로 받아치는 시각도 있다.
한 독자는 비터 레슨(bitter lesson)을 진지하게 받아들인다면 grep과
하이브리드 검색(bm25+vector)을 모두 도구로 쥐여 주고 에이전트가
스스로 고르게 하면 되며, 답이 “둘 다”일 수 있는데 X 대 Y로 묻는
것은 흥미롭지 않다고 말한다[^jeffchuber]. 다만 이에 대한 반론도
즉시 따라붙는다. 에이전트가 어느 쪽이 나은지 안다는 보장이 없고,
그 판단을 사후 학습(post-training)에 새겨 넣으려면 바로 이 논문
같은 연구가 먼저 각 방식이 어디서 잘 통하는지를 규명해 줘야
한다는 것이다[^pastel]. 즉 “둘 다 주기”는 선택을 에이전트에
떠넘길 뿐, 선택의 근거를 만드는 일은 여전히 이런 비교 연구의
몫이라는 지적이다.

### 가려진 트레이드오프 — grep의 정확도는 코퍼스 규모에 따라 무너질 수 있다

실험은 LongMemEval의 제한된 대화 이력 규모에서 수행된다.
여기서 간과되기 쉬운 트레이드오프는 grep의 우위가 코퍼스 크기에
강하게 의존한다는 점이다. 수백 건의 대화 안에서는 문자열 매칭이
충분히 좁은 후보 집합을 반환하지만, 코퍼스가 수백만 문서로
커지면 grep은 너무 많은 매칭을 토해내거나, 반대로 정확한
키워드를 모르면 아무것도 못 찾는 양극단으로 치닫는다.

벡터 검색의 진짜 강점은 바로 이 규모에서 나타난다.
임베딩은 명시적 키워드 없이도 의미적으로 가까운 후보를
일정 수로 압축해 주기 때문이다. 따라서 “grep만으로 충분한가”라는
질문의 답은 규모 의존적이며, 소규모 기억 회상에서는 yes,
대규모 의미 검색에서는 no에 가까울 가능성이 높다.
논문의 제목이 던지는 도발은 측정된 영역 밖으로 확장될 때
조심해서 다뤄야 한다.

### 하네스 의존성은 벤치마크 게이밍과 재현성 위기의 새 표면을 연다

동일 데이터에서 하네스만 바꿔도 점수가 출렁인다는 사실은,
역으로 하네스 선택이 결과를 의도적으로 끌어올리는 지렛대가 될 수
있음을 뜻한다. 어떤 검색 전략을 홍보하려는 측은 그 전략에 유리한
하네스를 골라 보고하면 된다. 이는 모델 벤치마크에서 이미 익숙한
게이밍 패턴이 에이전트 검색 평가로 전이됨을 예고한다.

하네스가 결과를 좌우한다는 사실은 모델의 학습 편향 형태로도
나타난다. HN의 한 실무자는 직접 만든 고성능 스트리밍 의미 검색
도구를 붙였지만, Claude는 RL로 굳어진 grep 같은 도구로 자꾸
회귀해 끈질긴 조정 없이는 거의 통제가 불가능했다고 토로한다.
반면 Codex는 지시한 도구를 따라 줬고, 그의 조합형 도구를 쓰게
만들면 도구 호출이 20~50회에서 3~4회로 줄었다는 것이다[^fnordpiglet].
특정 하네스에 최적화된 모델 편향이 외부 도구의 효율을 압도해
버리는 이 현상은, 하네스 선택이 결과를 끌어올리는 지렛대라는
앞선 우려를 모델 내부의 편향 차원으로 한 겹 더 끌고 들어간다.

구조적으로 이는 LLM 평가가 겪어 온 재현성 위기의 다음 단계다.
모델, 프롬프트, 하네스, 도구 버전이라는 변수의 곱이 커질수록
독립적 재현은 사실상 불가능해진다. 이 논문은 그 위험을 드러내는
경고등 역할을 하지만, 동시에 스스로도 제공자 CLI를 통제 불가능한
블랙박스로 포함함으로써 그 위기의 일부가 된다.
앞으로의 에이전트 평가는 하네스를 오픈소스로 고정하고 버전을
박제하는 표준 없이는 신뢰를 얻기 어려울 것이다.

---

[^skypuncher]: HN 사용자 SkyPuncher의 댓글. “Table 2 and 3 tell you
    basically all you need to know. When you use a harness that is tuned
    towards programing (Codex and Claude Code), grep wins. When you use a
    neutral harness, vector search wins.”

[^krzyk]: HN 사용자 krzyk의 댓글. “AFAIR their first versions used some
    kind of treee/structure for easy search, but they found out that grep
    was better/similar but with less complications (they now ship some
    kind of grep).”

[^yetanotherjosh]: HN 사용자 yetanotherjosh의 댓글. “Is this saying they
    chose a benchmark that is biased towards doing well against literal
    string matching, thus works well with grep, and then (gasp) showed
    that grep did well, finally declaring 'grep is all you need'? ... A
    conversation about bikes, then a query about bike(s) where 'bike' is a
    common token hit. But not stuff like a conversation about a Beethoven
    sonata, then a question about classical music, where embedding based
    approach would shine.”

[^quinncom]: HN 사용자 quinncom의 댓글. “Don't presume this study has
    anything to do with programming. They measured an agent's ability to
    search long conversations, not code.”

[^stephantul]: HN 사용자 stephantul의 댓글. “This paper oversells on the
    title. Like, what is chronos, which embedding model was used, which
    reranker, how was the reranking done, why is chronos much better than
    claude code”

[^badcafebee]: HN 사용자 0xbadcafebee의 댓글. “And a lot more tokens, and
    slower speed. Yes you can get more accuracy if you suck tons more data
    into context. But compare this to more advanced code agent methods
    like Tree Sitter, PageRank, LSP, that build semantic maps to provide
    more relevant context. Grep alone can't do that”

[^softwaredoug]: HN 사용자 softwaredoug의 댓글. “In my research grep is
    fine if you don't care about tokens and you have less than 100k files.
    ... If you think grep is great, it's because you've been social
    engineered to organize your content to be findable.”

[^jeffchuber]: HN 사용자 jeffchuber의 댓글. “If you are truly
    bitter-lesson pilled - give the agent all the tools and let it decide
    which to use. - regex (grep) - hybrid search (bm25+vector) this X vs Y
    is uninteresting when the answer can be both.”

[^pastel]: HN 사용자 pastel8739의 댓글. “That assumes that the agent knows
    which one is better. And to bake in which one is better via
    post-training would require a study like this to establish where each
    one works well”

[^fnordpiglet]: HN 사용자 fnordpiglet의 댓글. “I've got a custom ultra
    high performance streaming semantic search I exposed as a tool and the
    RL bias in Claude is almost insurmountable without copious and
    consistent steering. Codex will follow instructions and use the tools
    I ask it to ... When I can get it to use my compositional tools tool
    calls drop from like 20-50 to 3-4, but it's almost impossible to
    steer.”
