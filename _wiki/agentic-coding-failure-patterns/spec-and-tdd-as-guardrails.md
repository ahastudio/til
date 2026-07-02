# 스펙/TDD가 하는 일과 못 하는 일

[← 에이전트형 코딩의 실패/함정 패턴](index.md)

[자율성이 검증을 잠식하는 구조](autonomy-erodes-verification.md)에서 확인한
병목(검증 속도)에 대해, 이 저장소의 노트들은 스펙 기반 개발(SDD)과
TDD를 유력한 처방으로 반복해서 다룬다. 하지만 두 처방 모두 만능이
아니며, 처방 자체가 새로운 한계를 낳는다는 점도 함께 기록되어 있다.

## SDD가 실제로 해결하는 문제: 맥락 손실

[spec-driven-development.md](../../agentic-coding/spec-driven-development.md)에
따르면 SDD는 "vibe-coding" 문제(겉보기엔 괜찮지만 실제로는 작동하지
않는 코드)에 대응하기 위해 등장했다. 명세를 임시 문서가 아니라 코드를
직접 생성하는 "실행 가능한" 문서로 취급하고,
constitution → specify → plan → tasks → implement의 단계로 구조화한다.

[kakaopay-spec-kit-practice.md](../../agentic-coding/kakaopay-spec-kit-practice.md)의
실전 보고가 이 처방이 왜 필요한지를 구체적으로 보여준다. 카카오페이
팀은 프로젝트 초반에는 에이전틱 코딩으로 속도를 냈지만, 후반으로
갈수록 AI가 이전 대화에서 합의한 코드 패턴을 잊고 다른 스타일을
적용하는 문제를 겪었다. 이는 컨텍스트 윈도우의 구조적 한계다 — 대화가
길어지면 초기 합의가 창 밖으로 밀려난다. Spec-kit은 맥락을 대화가
아닌 파일(constitution.md, spec, tasks.md)로 외부화해 이 문제를
해결한다. **파일은 대화와 달리 잘리지 않는다.**

바이브 코딩의 실패가 항상 "후반부"에 나타난다는 관찰이 중요하다. 초반의
빠른 진행이 "이 방식이 맞다"는 착각을 심어주고, 실패는 항상 나중에
온다. SDD의 여러 단계는 초반부터 의도적으로 마찰을 만들어 후반부
붕괴를 막는 일종의 보험료로 기능한다.

## SDD가 해결하지 못하는 것: 스펙도 결국 코드다

[sufficiently-detailed-spec-is-code.md](../../agentic-coding/sufficiently-detailed-spec-is-code.md)의
지적이 SDD 전체에 대한 가장 근본적인 반론이다. 구현을 신뢰성 있게
생성할 만큼 상세한 스펙은, 그 상세함 자체가 이미 코드의 정밀성을
요구한다는 것이다. `verification-debt.md`에 인용된 HN 댓글(dwb)도 같은
말을 한다 — "프로그램을 설명할 만큼 상세한 스펙은 실행 불가능한
언어로 쓰인 프로그램이나 마찬가지다." 즉 SDD는 "명세가 코드를
대체한다"는 약속이 아니라 "명세와 구현 사이의 의존성 방향을
강제한다"는 약속으로 읽어야 한다 — 코딩의 어려움을 없애는 것이 아니라
다른 곳으로 옮기는 것에 가깝다.

[ai-orchestrator-illusion.md](../../agentic-coding/ai-orchestrator-illusion.md)는
더 근본적으로 반박한다. 언어는 의도를 완전히 표현하지 못하고, AI는 그
빈틈을 확률적으로 채운다. 스펙을 쓰는 행위가 구현을 통해서만 축적되는
컨텍스트를 대체할 수 없다는 것이다. "스펙을 잘 쓰는 능력" 자체가
구현 경험을 통해 길러진 컨텍스트를 전제한다면, SDD는 그 전제를
해소하지 않은 채 도구화한 것일 뿐이다.

[bottleneck-was-never-the-code.md](../../agentic-coding/bottleneck-was-never-the-code.md)에
인용된 반론(trjordan)도 이 편에 선다 — "코드 작성은 항상 무언가를
가르쳐준다." 명세 단계에서는 보이지 않던 것들이 구현을 통해 드러나며,
작동하는 소프트웨어를 만들어봐야 비로소 무언가 가치 있는 것을 만들고
있는지 알 수 있다.

## TDD의 역할 재분배: Red는 인간, Green은 AI

[tdd-in-ai-era.md](../../agentic-coding/tdd-in-ai-era.md)는 TDD를 검증
병목에 대한 가장 구체적인 실천법으로 제시한다. Red-Green-Refactor
루프에서 주도권이 재분배된다. **Red(실패 테스트 작성)는 인간의
몫**이다 — 정상 입력, 경계 조건, 예외 상황을 테스트로 명시하는 것은
도메인 이해와 의도 파악을 요구하며 AI가 대신할 수 없다. **Green(테스트
통과)은 AI가 담당**한다 — 테스트라는 명확한 제약이 주어지면 AI는 그
안에서 정확한 구현을 만든다. 테스트가 정밀할수록 AI 코드의 정확성도
올라간다는 것이 핵심이다: 차이는 모델의 지능이 아니라 명세의
명확성이다.

이 관점에서 테스트는 프롬프트보다 정확한 명세다. "로그인 실패 시
적절히 처리해줘"는 수십 가지로 해석되지만,
`expect(login('wrong-password')).toThrow(AuthError)`는 해석의 여지가
없다. `sufficiently-detailed-spec-is-code.md`의 논리를 빌리면, 테스트는
"정밀해진 명세가 코드로 수렴한 형태" 그 자체다 — 이미 실행 가능한
형식 언어이기 때문에 자연어 스펙이 겪는 모호성 문제를 겪지 않는다.

## Constitution: 거버넌스를 프롬프트가 아니라 문서 아키텍처로

`kakaopay-spec-kit-practice.md`가 짚는 실무적 통찰: 많은 팀이 AI 출력을
제어하려고 프롬프트를 다듬는 데 집중하지만, 프롬프트는 매 요청마다
다시 써야 하고 대화가 끊기면 사라진다. Spec-kit의 constitution.md는
거버넌스 규칙을 파일로 문서화하고 모든 AI 작업이 그 파일을 참조하도록
강제한다 — "정책을 코드로 표현하라(Policy as Code)"는 원칙의 AI
버전이다. 단, 실전에서는 AI가 constitution보다 더 가까운 컨텍스트인
tasks 파일에 더 집중하는 경향이 관찰되어, constitution의 원칙이
tasks에 실제로 반영됐는지 별도로 확인해야 하는 문제가 남는다.

## 스펙과 TDD로도 해소되지 않는 것: 의도 부채

[intent-debt.md](../../agentic-coding/intent-debt.md)는 스펙/TDD 처방의
한계를 가장 정교하게 짚는다. 저자는 부채를 세 유형으로 나눈다 — 기술
부채(코드 안), 인지 부채(사람 안), 의도 부채(외재화된 산출물 안,
"왜 이렇게 설계했는가"). AI는 기술 부채(리팩터링)와 인지 부채(코드
설명)를 효과적으로 낮추지만, **의도 부채는 해소하지 못한다.** 에이전트는
코드로부터 그럴듯한 근거를 추론할 수는 있지만, 추론된 근거는 의도가
아니다 — 확신에 찬 설명을 날조할 뿐이며, 이것은 "모른다"고 인정하는
것보다 더 나쁘다.

이 한계는 에이전트 수가 늘어날수록 초선형으로 증폭된다. 인간 팀원은
경험을 축적하며 온보딩 비용이 팀원 수에 비례(선형)해 발생하지만,
에이전트는 매 세션마다 제로 컨텍스트로 시작한다. 10개의 에이전트가
하루 50개 세션을 실행하면 의도 전달 비용은 하루 500회 청구된다 —
스펙과 테스트를 아무리 잘 갖춰도, "이 선택을 왜 했는가"라는 배경
지식 자체를 기록해두지 않으면 그 부분만은 반복해서 새로 설명해야
한다.

## 정리: 처방은 유효하지만 새 병목을 만든다

스펙과 TDD는 검증 부채라는 병목에 대한 실질적 대응이지만, 둘 다
"검증 자체를 없애는 것"이 아니라 "검증을 명시적이고 반복 가능한
형태로 옮기는 것"에 가깝다. 그 결과 병목은 사라지지 않고
명세 작성 능력, 테스트 설계 능력, 의도 기록 규율이라는 새로운
장소로 이동한다 — 이는
[어디까지 자율을 주고 어디서 개입해야 하는가](where-to-draw-the-line.md)에서
다루는 "판단이 상류로 이동한다"는 관찰과 정확히 같은 결이다.

## 출처

- [agentic-coding/spec-driven-development.md](../../agentic-coding/spec-driven-development.md)
- [agentic-coding/sufficiently-detailed-spec-is-code.md](../../agentic-coding/sufficiently-detailed-spec-is-code.md)
- [agentic-coding/kakaopay-spec-kit-practice.md](../../agentic-coding/kakaopay-spec-kit-practice.md)
- [agentic-coding/tdd-in-ai-era.md](../../agentic-coding/tdd-in-ai-era.md)
- [agentic-coding/ai-orchestrator-illusion.md](../../agentic-coding/ai-orchestrator-illusion.md)
- [agentic-coding/bottleneck-was-never-the-code.md](../../agentic-coding/bottleneck-was-never-the-code.md)
- [agentic-coding/intent-debt.md](../../agentic-coding/intent-debt.md)
- [agentic-coding/verification-debt.md](../../agentic-coding/verification-debt.md)
