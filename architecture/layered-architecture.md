# Layered Architecture

## DDD의 구분

1. UI Layer - `POST /transactions to=Jane amount=1300` `TransactionController`
2. Application Layer - `TransferService`
3. Domain Layer - `Account`, `AccountId`, `Money`, `Transaction`, Interface of `AccountRepository` and `TransactionRepository`
4. Infrastructure Layer - Implements of `AccountRepository` and `TransactionRepository`
