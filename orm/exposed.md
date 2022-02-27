# Exposed - Kotlin SQL Framework

<https://github.com/JetBrains/Exposed>

## Exposed Spring Boot Starter

<https://github.com/JetBrains/Exposed/tree/master/exposed-spring-boot-starter>

## Transaction

<https://github.com/JetBrains/Exposed/wiki/Transactions>

<https://github.com/JetBrains/Exposed/tree/master/spring-transaction>

## Yun님의 적용 사례 및 정리 글

- <https://cheese10yun.github.io/spring-batch-batch-insert/>
- <https://cheese10yun.github.io/exposed/>

## 아샬의 jOOQ → Exposed 코멘트 (2022년 2월 27일)

> jOOQ의 두 가지 단점을 보완하기 위해 Exposed를 사용하려고 합니다:
>
> 1. jOOQ는 DB 스키마를 직접 표현할 방법이 없습니다.
> 현재는 JPA를 활용하고 있는데, 이렇게 하면
> 도메인 객체를 DB와 강하게 연결하는 경향을 만들게 됩니다.
> Exposed는 object로 테이블 정보를 직접 묘사하기 때문에
> 이런 문제에서 자유롭습니다.
>
> 1. jOOQ는 DSL을 제대로 쓰려면 Code Generation 단계가 필요합니다.
> DB에 대한 접근 문제도 있고,
> 코드 생성에 적지 않은 시간이 소요되는 문제가 있습니다.
> Exposed는 object로 DSL을 위한 코드를 직접 작성하기 때문에
> 이런 문제에서 자유롭습니다.
