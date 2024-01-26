# ULID (Universally Unique Lexicographically Sortable Identifier)

<https://github.com/ulid/spec>

두 개의 값을 결합해서 ID를 생성. ID의 상위 비트에 Timestamp가 들어가기 때문에, ID를 생성 시각에 따라 정렬할 수 있다.

- Timestamp (48bits)
- Randomness (80bits)

## Node.js `ulid` package

<https://github.com/ulid/javascript>
