# Layered Architecture

> One of the powerful features of the layered architecture pattern
> is the **separation of concerns** among components.
>
> (from <https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/ch01.html>)

## 전통적인 3계층

<https://martinfowler.com/bliki/PresentationDomainDataLayering.html>

1. Presentation
1. Domain
1. Data

[N-tier Architecture](./n-tier-architecture.md)
참고.

## 에릭 에반스의 “DDD”에 나온 4계층

<https://wikibook.co.kr/article/layered-architecture/>

1. UI Layer
1. Application Layer
1. Domain Layer
1. Infrastructure Layer

상위 레이어는 하위 레이어에 의존,
하위 레이어는 상위 레이어를 모름.

애플리케이션 레이어가 모든 기능 목록을 드러내고,
도메인 객체들이 협력할 수 있는 진입점을 마련.

### DIP를 적용한 4계층

[Vaughn Vernon on Advanced Architecture Styles with DDD](https://www.infoq.com/news/2013/04/DDD-Architecture-Styles/)

인프라스트럭처 레이어를 UI 레이어와 마찬가지로
의존성 체인의 가장 밖으로 꺼내기 위해
의존성 역전 원칙(DIP; Dependency Inversion Principle)을 적용.

### 구체적인 사례

1. UI Layer - `POST /transactions to=Jane amount=1300` `TransactionController`
1. Application Layer - `TransferService`
1. Domain Layer - `Account`, `AccountId`, `Money`, `Transaction`, Interface of `AccountRepository` and `TransactionRepository`
1. Infrastructure Layer - Implements of `AccountRepository` and `TransactionRepository`
