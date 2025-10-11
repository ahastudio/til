# 익스트림 프로그래밍 실천방법

- [아듀 2020!](https://adieu2020.ahastudio.com/)
- 이전 글: [똑같이 “P”가 들어가지만 뜻이 다른 용어](https://github.com/ahastudio/til/blob/main/management/20201210-product.md)
- 다음 글: [Gradle로 프로젝트 빌드하고 실행하기](https://github.com/ahastudio/til/blob/main/gradle/20201212-build-and-run.md)

---

저는 주로 익스트림 프로그래밍(XP)을 따르고 있습니다.
여기선 XP의 실천방법을 거칠게 요약하겠습니다.

<img src="./images/xp-circles.jpg" alt="XP Practices" width="360" />

## Business Practices

1. Whole Team

    기능에 따라 나눠지는 낡은 조직 구조를 따르지 않고,
    하나의 제품/프로젝트를 하나의 팀이 책임지게 합니다.
    개발자는 프로그래머만 지칭하는 게 아니라
    제품을 만드는데 직접적으로 관여하는 모두를 의미합니다.
    여기에는 디자이너, 테스터 등이 당연히 포함됩니다.
    전체 팀은 제품을 직접 사용하거나 사용자를 대표하는
    고객(Product Owner)까지 포함합니다.

1. Planning Game

    프로젝트는 작은 단위로 반복 진행됩니다.
    저는 주로 1주 단위를 사용합니다.
    [사용자 스토리](https://github.com/ahastudio/til/blob/main/agile/user-story.md)로
    사용자의 가치와 기능을 모두 표현하려고 노력하고,
    이를 작은 작업으로 분해해 진행합니다.
    가치를 전달하는 대상은 최종 사용자가 아니라
    다른 팀원일 수도 있습니다.
    예를 들어 시장 조사 결과는 팀에게 가치를 전달합니다.

1. Small Release

    매 반복마다 제품이 업데이트 됩니다.
    소프트웨어가 패키지 형태로 전달되던 시절에는
    비교적 어려운 항목이었겠지만,
    지금은 상대적으로 많이 쉬워졌습니다.
    그래서 이제는 단순히 작게 릴리즈하는 걸 넘어서,
    가설-검증 사이클을 잘 돌릴 수 있도록 지원하냐가 관건입니다.

1. Acceptance Test

    제품의 완성도, 작업 완료 여부는
    모두 고객 중심의 테스트를 통해 결정됩니다.
    고객의 관점에서 제품/서비스를 바라볼 기회를 갖고,
    고객 입장에서 올바르게 사용할 수 있는지 확인합니다.

## Team Practices

1. [Continuous Integration](https://github.com/ahastudio/til/blob/main/agile/continuous-integration.md)

    각 작업은 작게 진행하지만 모두 제품에 바로 반영됩니다.
    단 하나의 `main` 브랜치를 중심으로 관리하고,
    [`develop` 등 다른 꼼수를 사용하지 않습니다](https://github.com/ahastudio/til/blob/main/git/github-flow.md).
    자동화된 테스트를 통해 최대한 미리 검증하려고 노력하고,
    [그 결과는 손쉽게 실제 제품/서비스에 반영돼야 합니다](https://github.com/ahastudio/til/tree/main/devops).

1. Collective Ownership

    프로젝트에 투입 되는 모든 자원(코드, 이미지, 문서 등)은
    팀의 공동 소유물입니다.
    즉, 팀원이라면 누구든 접근할 수 있고 제안할 수 있고
    수정할 수 있습니다.
    우리는 프로젝트가 성공하기 위해서라면 모든 것을 할 것입니다.

1. Coding Standard

    가능하면 모든 자원은 일관된 형태를 띄게 합니다.
    너무 다른 양식을 사용해서 작성하거나 읽을 때마다
    불필요하게 인지자원을 낭비하지 않도록 합니다.
    소스 코드의 경우엔 정적분석도구를 최대한 활용해
    일관된 형식을 지키는 걸 손쉽게 합니다.

1. Metaphor

    도메인에 대한 이해와 코드가 일치할 수 있도록
    팀원 모두가 동일한 멘탈모델을 가질 수 있는
    좋은 비유/모델을 만들고 사용합니다.
    구체적으로는 도메인 주도 설계(DDD)를 따릅니다.

1. Sustainable Pace

    프로젝트는 마라톤임을 잊지 않습니다.
    프로젝트는 팀 활동임을 잊지 않습니다.
    헌신적으로 일하는 상황 속에서도
    자신의 상태를 올바르게 파악하고
    팀에 해를 끼치지 않도록 충분히 휴식을 갖습니다.

## Technical Practices

1. Simple Design

    미래를 대비한다고 생각하면서 하는 일 중 상당수는
    미래에 오히려 짐이 되는 경우가 많습니다.
    지금 필요한 걸 만족시키는 가장 단순한 일을 하려고 노력합니다.
    [Xper:SimpleDesign](https://j.mp/37MLvK8) 참고.

1. [Pair Programming](https://github.com/ahastudio/til/blob/main/agile/pair-programming.md)

    혼자 하기 어려운 일은 둘이 함께합니다.
    혼자서 하는 게 더 효율적이라고 생각될 때는
    실제로 어떤 성과를 내고 있는지 측정하고 객관적으로 평가합니다.
    협업은 어렵지만, 그 결과는 대단합니다.
    등을 맡길 수 있는 든든한 팀원들인지 항상 자문합니다.

1. [Test-Driven Development](https://github.com/ahastudio/til/blob/main/agile/test-driven-development.md)

    모든 일을 하기 전에 어떻게 사용할지 먼저 고민합니다.
    어떤 걸 바꿀 때는 무슨 일이 벌어질지 생각합니다.
    우리가 하는 일은 미래를 상상하는 것입니다.
    미래를 상상할 수 없다면 일을 시작하지 않습니다.
    지금은 생각이 더 필요할 겁니다.
    혼자서 어렵다면? 동료와 함께 합니다.

    참고: [TDD FAQ](https://github.com/ahastudio/til/blob/main/blog/2016/12-03-tdd-faq.md)

1. Refactoring

    나쁜 조직은 시간이 지날수록 모든 게 복잡해집니다.
    좋은 조직은 시간이 지날수록 모든 게 분명해집니다.
    항상 고객과 제품, 도메인에 대해 배우고
    이렇게 배운 점을 제품에 다시 적용합니다.
    어제와 같은 오늘이 아니라 어제보다 나은 오늘을 만듭니다.

## 참고

- 이미지 출처: [What is Extreme Programming?](https://j.mp/3aIsHNZ)
- [Wikipedia:Extreme_programming_practices](https://j.mp/2Kulu9I)

---

- [아듀 2020!](https://adieu2020.ahastudio.com/)
- 이전 글: [똑같이 “P”가 들어가지만 뜻이 다른 용어](https://github.com/ahastudio/til/blob/main/management/20201210-product.md)
- 다음 글: [Gradle로 프로젝트 빌드하고 실행하기](https://github.com/ahastudio/til/blob/main/gradle/20201212-build-and-run.md)
