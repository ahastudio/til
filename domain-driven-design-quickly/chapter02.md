# Chapter 2 - The Ubiquitous Language

## 인용

> **도메인 주도 설계의 핵심 원칙**은 **모델 기반의 언어**를 사용하는 것이다.
> 모델은 **소프트웨어와 도메인이 서로 교차하는 지점**이기 때문에
> 모델 기반 언어를 사용하는 것이 가장 적절하다.
> (p.33)

---

> 팀에서 이루어지는 모든 **의사소통** 순간과 **코드**에서도 이 언어를
> 최대한 끊임없이 사용하도록 요구하라.
> (p.34)

---

> 언어는 하룻밤에 만들어지지 않는다.
> 언어가 지녀야 할 핵심 요소들을 골라내는 것은 어렵고 집중을 요하는 일이다.
> 우리는 도메인과 설계를 정의할 **핵심 개념**을 찾아 거기에 해당하는
> **적절한 단어**를 찾고 사용할 필요가 있다.
> 일부는 쉽게 발견할 수도 있지만 어떤 것들은 **발견하기 매우 어려울 수 있다**.
> (p.34)

---

> 하지만 실제로는 위와 같은 대화가 훨씬 장황하게 이루어지고,
> 종종 어떤 사실을 돌려서 얘기하거나 너무 상세하게 설명하려고도 하며
> 혹은 잘못된 개념을 가지고 접근하기도 한다.
> (p.38)

---

> 개발자가 모델의 주요 개념을 **코드로 구현**해 보기를 강력히 권한다.
> (p.39)

---

> 프로젝트 후반부에 이르면, 모델이 커지고, 잘 된 설계를 바탕으로 하지 않은
> 코드 때문에 수정 하나로도 의도하지 않는 결과를 낳게 되는데,
> 이때 비로소 모델을 코드로 표현한 것의 가치가 나타난다.
> (p.40)

---

UML 다이어그램의 한계 #1

> UML 다이어그램들은 관련된 요소의 수가 적을 때 매우 유용하다.
> (p.41)

---

UML 다이어그램의 한계 #2

> UML은 클래스와, 내부 속성 및 그 사이의 관계를 표현하는 데에는 매우
> 적합하지만, 클래스의 **행동**이나 **제약 사항**을 표현하기는 그리 쉽지 않다.
> (p.41)

---

대안: 문서 & 작은 다이어그램

> 우리는 문서를 사용할 수 있다.
> 모델의 작은 부분 부분을 작은 다이어그램으로 구성하는 것도 권할 만한
> 의사소통 방법이다.
> (p.41)

---

> 모델 전체를 다루는 한 장의 커다란 다이어그램을 작성해 보고 싶을지 모른다.
> 하지만 대개 모든 것을 포함하는 다이어그램을 작성하기란 불가능하다.
> (p.42)

---

> 문서란 모델과 동일한 내용이어야 한다.
> 잘못된 언어를 사용하고 모델을 반영하지 못하는 오래된 문서는 전혀 소용이 없다.
> (p.42)

---

코드의 한계 (현실?)

> 기능적으로 맞는 일을 수행하는 코드라 할지라도,
> 늘 적절하게 코딩되는 것은 아니다.
> (p.43)

---

> **소프트웨어 아키텍트, 개발자, 도메인 전문가로 구성된 설계팀**은
> 자신들의 행동을 통합하고, 모델 작성과 작성된 모델의 코드화를 도와줄 언어가
> 필요하다
> (p.43)

원서의 문장

> the design team, made up of software architects, developers, and domain
> experts, needs a **language** that *unifies their actions*,
> and helps them *create a model* and *express that model with code*.

“action”은 “행동”보다는 “업무”로 번역하는 게 좀 더 자연스럽다.
