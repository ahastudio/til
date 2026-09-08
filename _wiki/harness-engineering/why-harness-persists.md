# 모델이 좋아져도 하네스가 사라지지 않는 이유

[← 하네스 엔지니어링](index.md)

“모델이 이제 똑똑해졌으니 하네스는 배관일 뿐”이라는 주장과 “같은 모델도
하네스에 따라 성능이 극적으로 갈린다”는 반증이 이 저장소 안에 나란히
있다. 결론부터 말하면 둘 다 부분적으로 맞다 — 다만 “하네스”라는 한
단어가 서로 다른 두 종류의 구성 요소를 가리키기 때문에 생기는 착시다.

## 같은 모델, 하네스만 바꿔 45%p 차이

[GPT-6 Astra가 증명한 것은 모델이 아니라
하네스다](../../agentic-coding/gpt-6-astra-harness-is-the-product.md)가
가장 극적인 반증이다. ARC Prize는 동일한 GPT-6 Astra를 공급자 중립
표준 하네스(고강도 추론, 54.8%)와 OpenAI 네이티브 어댑터 하네스(같은
설정, 99.9%)로 각각 시험했다. 모델은 전혀 바뀌지 않았는데 45.1%p가
갈렸고, 심지어 점수가 높은 쪽이 평가 비용도 더 쌌다(18,817달러 대
40,705달러). [Learn Harness Engineering
강의](../../agentic-coding/learn-harness-engineering-lectures.md) 1강이
인용하는 Anthropic 통제 실험도 같은 형태다 — 동일 모델, 동일 프롬프트를
하네스 없이 돌리면 20분 만에 실패하고, 완전한 하네스를 갖추면 6시간
만에 플레이 가능한 게임이 나온다. 이런 사례들의 공통점은 하네스가
“모델이 이미 할 수 있는 것을 조금 더 잘 끌어내는 장치”가 아니라 “모델의
관측 가능한 능력 자체를 결정하는 변수”라는 것이다.

## 그런데 같은 모델 발전이 하네스 구성 요소를 무력화하기도 한다

정반대 증거도 같은 저장소에 있다. [장기 실행 애플리케이션 개발을 위한
하네스
설계](../../agentic-coding/harness-design-long-running-apps.md)는
Anthropic 스스로 Opus 4.6에서 일부 하네스 구성 요소가 “더 이상 하중을
받지 않게(no longer load-bearing)” 됐다고 인정한 사례를 담고 있다. 이
노트의 인사이트는 이를 극단까지 밀어붙인다 — 하네스의 각 구성 요소는
“현재 모델이 못 하는 것”에 대한 베팅이며, 모델이 그것을 할 수 있게 되는
순간 그 베팅은 사장 비용(sunk cost)이 된다. [Learn Harness Engineering
강의](../../agentic-coding/learn-harness-engineering-lectures.md) 12강은
이를 절차로 만든다 — 월별로 하네스 구성 요소 하나를 비활성화하고
벤치마크해, 필요 없으면 제거하거나 더 가벼운 대안으로 교체하라는 것이다.

[earendil의 “하네스란 무엇인가”](../../agentic-coding/what-is-a-harness.md)에
달린 HN 댓글에서 `tosh`는 이 방향을 배낭 비유로 정리한다 — 하네스를
여행에 지고 가는 짐으로 보면 가져가는 모든 것에 비용이 있고, 모델이
좋을수록 하네스는 더 얇아질 수 있다는 것이다. 이 관점에서 하네스는
모델의 보완재이므로, 모델이 나아지는 만큼 하네스의 전략적 가치는
줄어든다.

## 두 증거가 공존하는 이유: “하네스”가 가리키는 것이 두 가지다

이 모순을 푸는 열쇠는 [Claude 5 세대 모델을 위한 컨텍스트 엔지니어링의
새 규칙](../../claude/new-rules-of-context-engineering-for-claude-5.md)의
분석에 있다. Anthropic이 Claude Code 시스템 프롬프트를 80% 이상
걷어냈다는 사례에서, 여섯 가지 전환 중 셋(규칙→판단, 예시→인터페이스
설계, 반복→단일 진술)은 **모델 세대에 종속된 조언**이고, 나머지
셋(점진적 공개, 자동 메모리, 풍부한 참조)은 **컨텍스트 창을 자원으로
관리하는 방법의 개선**이라 모델과 무관하게 유효하다. 즉 하네스에는
“이번 모델 세대의 특정 결함을 메우는 임시 보철물”과 “컨텍스트 예산을
구조적으로 관리하는 영구 인프라”가 섞여 있고, 사라지는 것은 언제나
전자다. GPT-6 Astra 사례에서 45%p를 만든 것도 후자에 가까운
것(추론 상태 보존, 컨텍스트 압축)이지 “이 모델은 아직 못하는 것”에
대한 임시방편이 아니었다.

이 구분을 놓치면 두 가지 반대 방향의 실수를 한다. 사라지는 하네스
구성 요소(모델 세대 종속)를 영구 자산인 것처럼 계속 유지하거나,
사라지지 않는 하네스 구성 요소(컨텍스트 관리 인프라)를 “이제 모델이
좋아졌으니 필요 없다”며 걷어내는 것이다. [결정론적 강제와 텍스트
지침의 경계](deterministic-vs-prompted.md)가 다루는 것이 바로 이
두 번째 실수의 구체적 사례다.

## 하네스로도 못 고치는 것이 있다는 반론

세 번째 각도도 있다. [Why Software Factories
Fail](../../ai/software-factories-fail-coding-agents.md)은 앞의 두
증거와 다른 종류의 주장을 편다 — 코드베이스 유지보수성처럼 강화학습
보상 함수(FAIL_TO_PASS/PASS_TO_PASS)에 애초에 반영되지 않는 능력은,
아무리 정교한 하네스를 쌓아도 모델 훈련의 한계를 우회할 수 없다는
것이다. 이는 “하네스가 필요 없다”는 주장과도, “하네스만 잘 만들면
된다”는 주장과도 다르다 — 하네스가 메울 수 있는 격차와 메울 수 없는
격차가 따로 있다는 것이며, 유지보수성 벤치마크가 없는 한 이 주장은
반증도 확증도 어렵다는 점을 저자 스스로 인정한다. HN에서
`fishtoaster`는 이 글의 핵심 근거(2025년 7월 lights-off 실험 실패)가
Opus 4.5 이후의 도약 이전 경험이라고 반박했는데, 이 반박 자체가 다시
“모델이 좋아지면 특정 하네스 구성 요소가 불필요해진다”는 첫 번째
증거를 재확인하는 셈이다 — 다만 유지보수성이라는 좁은 영역에서는
아직 그 도약이 확인되지 않았다는 유보가 남는다.

## “성격”과 “하네스”를 분리할 수 있다는 주장 자체가 검증되지 않는다

[Boris Cherny의 Fable 5 사용 소감: “big model
smell”](../../claude/fable-5-big-model-smell.md)은 이 논쟁에 방법론적
경고를 더한다. Claude Code 제작자인 저자는 Fable 5가 프롬프트에 없는
방법론적 디버깅을 스스로 한다며 이를 “모델의 성격”이라 부르지만, 비평은
이 관찰이 “같은 하네스에 모델만 바꿨다”는 통제를 가정하고 있을 뿐
증명하지 않는다고 지적한다. 새 모델은 거의 항상 갱신된 프롬프트·도구
정의·컨텍스트 정책과 함께 배포되므로, 관찰된 차이가 “모델의 성격”인지
“모델과 하네스의 공진화”인지 같은 회사가 둘을 함께 발전시키는 한
분리할 수 없다. 이는 하네스와 모델의 기여도를 나누려는 모든 벤치마크
논쟁(위의 GPT-6 Astra 사례 포함)에 적용되는 일반적 경고다.

## 관련

[결정론적 강제와 텍스트 지침의 경계](deterministic-vs-prompted.md) ·
[하네스는 소모품이다: 유지와 가지치기](harness-as-disposable.md)

## 출처

- [agentic-coding/gpt-6-astra-harness-is-the-product.md](../../agentic-coding/gpt-6-astra-harness-is-the-product.md)
- [agentic-coding/harness-design-long-running-apps.md](../../agentic-coding/harness-design-long-running-apps.md)
- [agentic-coding/learn-harness-engineering-lectures.md](../../agentic-coding/learn-harness-engineering-lectures.md)
- [agentic-coding/what-is-a-harness.md](../../agentic-coding/what-is-a-harness.md)
- [claude/new-rules-of-context-engineering-for-claude-5.md](../../claude/new-rules-of-context-engineering-for-claude-5.md)
- [ai/software-factories-fail-coding-agents.md](../../ai/software-factories-fail-coding-agents.md)
- [claude/fable-5-big-model-smell.md](../../claude/fable-5-big-model-smell.md)
