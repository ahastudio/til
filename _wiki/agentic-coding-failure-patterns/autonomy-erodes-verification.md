# 자율성이 검증을 잠식하는 구조

[← 에이전트형 코딩의 실패/함정 패턴](index.md)

[돌이킬 수 없는 사고들](irreversible-incidents.md)이 눈에 보이는 사건이라면,
이 주제는 사고가 터지기 전까지 조용히 쌓이는 부채를 다룬다. 이 저장소의
여러 노트가 서로 다른 이름으로 같은 현상을 가리킨다.

## 검증 부채: 산출물은 싸졌지만 검증은 비싸졌다

[verification-debt.md](../../agentic-coding/verification-debt.md)가 제시하는
핵심 개념이다. 에이전트가 몇 분 만에 그럴듯한 diff를 만들어내지만, 그것을
검증하는 속도는 그만큼 빨라지지 않는다. 기술 부채는 마찰(느려지는 빌드,
꼬인 의존성)로 스스로를 드러내지만, 검증 부채는 **거짓 자신감**을 낳는다 —
테스트는 통과하고 코드는 깔끔해 보이지만, 스펙에 적힌 것만 구현했을 뿐
사용자가 실제로 원한 것은 아닐 수 있다. 이 비대칭이 위험한 이유는 명확한
역방향 피드백 루프 때문이다. 깔끔한 코드 → 승인 → 지표 개선 → 더 많은
승인 → 검증 부채 기하급수적 누적 → 장애 발생 후에야 원인이 몇 달 전
승인된 PR로 드러난다.

## 감독의 역설: 감독하려면 잃어가는 바로 그 능력이 필요하다

[agentic-coding-is-a-trap.md](../../agentic-coding/agentic-coding-is-a-trap.md)와
[ai-orchestrator-illusion.md](../../agentic-coding/ai-orchestrator-illusion.md)가
같은 역설을 다른 각도에서 짚는다. Anthropic 자체 연구에서 에이전트 집중
사용 후 디버깅 능력이 47% 하락했다는 수치가 인용된다. 문제는 이 능력
저하가 “감독을 위해 필요한 바로 그 능력”이라는 점이다. AI를 감독하려면
코드를 읽고 판단할 수 있어야 하는데, 그 판단력 자체가 AI 사용으로
위축된다. 이는 자기강화적 하락 나선이다 — 더 많이 위임할수록 감독
능력이 떨어지고, 감독 능력이 떨어질수록 검증 없이 더 많이 위임하게
된다.

`ai-orchestrator-illusion.md`는 여기에 중요한 구분을 더한다. “AI가
코딩하고 인간은 오케스트레이터가 된다”는 서사는 **더 높은 추상화가
아니라 더 높은 모호성으로의 이동**이라는 것이다. C++에서 Java로, 서버에서
AWS로 옮겨갈 때는 하위 레이어가 여전히 이해 가능했다. AI 위임은 이
연속성을 끊는다 — 결과물은 있지만 왜 그렇게 나왔는지 설명할 수 있는
사람이 사라진다.

## 도박으로서의 AI 코딩: 간헐적 강화가 만드는 중독 구조

[ai-coding-is-gambling.md](../../agentic-coding/ai-coding-is-gambling.md)는
같은 현상을 행동심리학으로 설명한다. 슬롯머신이 중독적인 이유는 매번
이기기 때문이 아니라 언제 이길지 예측할 수 없기 때문이다. 프롬프트를
넣으면 때로는 완벽한 코드가, 때로는 그럴듯하지만 틀린 코드가 나오는
불확실성이 같은 신경 회로를 자극한다. 이 비유가 유용한 이유는 “왜
검증을 건너뛰고 싶은 유혹이 이토록 강한가”를 설명하기 때문이다 — 결과가
빨리 나올수록 확인 없이 다음 프롬프트로 넘어가려는 압력이 커진다.

## 검증 부채가 조직 규모에서 나타나는 형태

`verification-debt.md`는 개인 차원을 넘어 조직 차원의 구조도 짚는다. AI가
모든 엔지니어를 50% 더 생산적으로 만들면, 조직은 50% 더 많은 산출물을
받는 것이 아니라 50% 더 많은 리뷰 부담을 받는다. 병목은 사라지지 않고
“무엇을 만들지 결정하는 것”, “완료를 정의하는 것” 같은 환원 불가능하게
인간적인 판단으로 상류 이동한다. 이 병목 이동은
[bottleneck-was-never-the-code.md](../../agentic-coding/bottleneck-was-never-the-code.md)와
[tdd-in-ai-era.md](../../agentic-coding/tdd-in-ai-era.md)에서도 반복
확인된다 — 세 노트 모두 “코드 생성 속도”가 아니라 “코드 신뢰성 검증
속도”가 새 병목이라는 데 수렴한다.

## AI 코드의 표면 품질이 검증을 더 어렵게 만든다

`verification-debt.md`가 짚는 미묘한 지점: AI 생성 코드는 표면적으로
인간 코드보다 깔끔하다. 일관된 네이밍, 적절한 주석, 정렬된 임포트. 인간이
쓴 코드에는 “냄새”(급하게 쓴 변수명, 임시 주석)가 있어 리뷰어에게 “주의
깊게 봐라”는 신호를 보내지만, AI 코드에는 이 냄새가 없다. 깔끔함 자체가
위장이 되어 유창성 효과(fluency effect) — 읽기 쉬운 텍스트를 더 정확하다고
착각하는 인지 편향 — 를 유발한다.

## 이것은 자동화 전반의 오래된 패턴이다

`agentic-coding-is-a-trap.md`는 이 역설이 AI 코딩에 국한되지 않는다고
지적한다. 항공 자동조종 장치 보급 이후 파일럿의 수동 비행 능력이
퇴화해 자동화 장애 시 오히려 더 위험해진 “자동화 편향(automation
bias)”이 1990년대부터 연구되어 왔다. 소프트웨어 개발이 다른 점은 이
자동화의 속도와 범위가 전례 없이 빠르고 넓다는 것이다. 항공 산업은
수십 년에 걸쳐 시뮬레이터 훈련 의무화 같은 제도적 대응을 발전시켰지만,
AI 코딩 에이전트는 1~2년 만에 표준 워크플로가 되었고 이에 상응하는
대응 메커니즘은 아직 없다.

관련: [스펙/TDD가 하는 일과 못 하는 일](spec-and-tdd-as-guardrails.md)은
바로 이 병목(검증 속도)에 대한 구체적 대응책을 다룬다. 검증 부채라는
진단에 대한 처방이 얼마나 실효성 있는지가 다음 주제다.

## 검증 도구 자체가 검증 대상과 같은 편향을 공유할 수 있다

[swe-bench-pro-signal-noise.md](../../agentic-coding/swe-bench-pro-signal-noise.md)는
검증 부채 문제가 코드 작성 단계를 넘어 “무엇이 옳은 결과인가”를 판정하는
평가 단계 자체에서도 반복된다는 것을 보여준다. OpenAI는 자사 코딩 벤치마크
SWE-Bench Pro의 결함을 감사하면서 Codex 기반 조사 에이전트를 동원했는데,
이는 “모델의 코딩 능력을 측정하는 벤치마크의 결함을, 그 모델과 같은
계열의 에이전트로 찾아낸다”는 재귀적 구조다. 실제로 이 구조의 한계도
함께 드러났다. 에이전트 파이프라인은 결함 후보의 27.4%를 결함으로
판정했지만, 독립적인 인간 검토자 5명은 34.1%를 결함으로 판정했다 —
특히 “테스트는 통과하지만 충분히 검증하지 못하는” 낮은 커버리지 범주에서
두 배 이상 차이가 났다. 에이전트가 인간보다 체계적으로 더 관대하게
판정했다는 사실은, 자동화된 검증이 인간 검증을 대체하기보다는 사전
필터 역할에 머물러 있다는 것을 수치로 보여준다.

[rewriting-bun-in-rust.md](../../rust/rewriting-bun-in-rust.md)는 같은
문제를 코드 작성 단계에서 재확인한다. Bun 팀은 53만 줄 규모의 Zig
코드베이스를 Rust로 이식하면서 구현자 1명과 적대적 리뷰어(adversarial
reviewer) 2명, 수정자 1명으로 구성된 태스크 단위를 64개 동시에
운용했다. 이는 작성자와 검토자를 분리하는 오래된 거버넌스 원칙을
에이전트 단위로 자동화한 설계다. 하지만 이 구조에도 같은 맹점이
있다. 리뷰어 역시 구현자와 같은 모델이 생성한 에이전트라면, 둘이
공유하는 모델 특유의 편향까지는 걸러내지 못한다. 실제로 이 프로젝트에서
발생한 19개의 의미론적 회귀 버그 중 상당수는 “두 언어의 문법이 비슷해
보이지만 런타임 동작이 다른” 지점, 즉 사람이든 AI든 겉보기 대응에
의존하면 놓치기 쉬운 지점에서 나왔다.

두 사례를 겹쳐 보면 하나의 패턴이 드러난다. 검증 주체를 사람에서
에이전트로 옮기는 것은 검증 속도의 병목을 완화하지만, “같은 종류의
실수를 반복하는 편향”이라는 새로운 취약점을 끌어들인다. 구조적으로
독립된 것처럼 보이는 다자간 리뷰(구현자/리뷰어, 벤치마크/감사 에이전트)도
그 구성원들이 결국 같은 세대의 모델이라면, 완전히 독립적인 검증이라고
보기 어렵다. 이는 [멀티 에이전트 오케스트레이션 특유의
실패](multi-agent-orchestration-failures.md)에서 다루는 조율 실패와는
다른 종류의 위험이다 — 에이전트들이 서로 잘 조율되어 있어도, 그
조율의 결과물 자체가 공유된 맹점을 통과시킬 수 있다는 뜻이다.

## 출처

- [agentic-coding/verification-debt.md](../../agentic-coding/verification-debt.md)
- [agentic-coding/agentic-coding-is-a-trap.md](../../agentic-coding/agentic-coding-is-a-trap.md)
- [agentic-coding/ai-orchestrator-illusion.md](../../agentic-coding/ai-orchestrator-illusion.md)
- [agentic-coding/ai-coding-is-gambling.md](../../agentic-coding/ai-coding-is-gambling.md)
- [agentic-coding/bottleneck-was-never-the-code.md](../../agentic-coding/bottleneck-was-never-the-code.md)
- [agentic-coding/tdd-in-ai-era.md](../../agentic-coding/tdd-in-ai-era.md)
- [agentic-coding/swe-bench-pro-signal-noise.md](../../agentic-coding/swe-bench-pro-signal-noise.md)
- [rust/rewriting-bun-in-rust.md](../../rust/rewriting-bun-in-rust.md)
