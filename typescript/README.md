# TypeScript: JavaScript with syntax for types

<https://www.typescriptlang.org/>

## The TypeScript Handbook

<https://www.typescriptlang.org/ko/docs/handbook/intro.html>

## TypeScript + React

[https://github.com/ahastudio/CodingLife/tree/main/20211004/typescript](https://j.mp/3BlN2mV)

## Developer experience in TypeScript

[It's not JavaScript's ugly cousin. See how Typescript improves Developer Experience](https://tsh.io/blog/typescript-improves-developer-experience/)

## 30 Seconds of Typescript

> Inspired by 30-seconds-of-code

<https://decipher.dev/30-seconds-of-typescript/>

<https://github.com/deepakshrma/30-seconds-of-typescript>

## TypeScript 6.0

[Announcing TypeScript 6.0 Beta](https://devblogs.microsoft.com/typescript/announcing-typescript-6-0-beta/)

JavaScript 기반의 마지막 릴리스.
Go로 작성된 TypeScript 7.0으로의 전환을 준비하는
브릿지 역할.

주요 변경사항:

- `--stableTypeOrdering` 플래그
  (TypeScript 7.0과 타입 순서 동작 일치)
- `es2025` target 및 lib 지원
- Temporal API 타입 지원
- `RegExp.escape` 지원
- `this`를 사용하지 않는 함수의
  컨텍스트 민감도 완화
- Map/WeakMap "Upsert" 메서드 타입 추가
  (`getOrInsert`, `getOrInsertComputed`)
- `lib.dom.iterable`, `lib.dom.asynciterable`을
  `lib.dom`으로 통합
- `#/`로 시작하는 Subpath Imports 지원
- `--moduleResolution bundler`와
  `--module commonjs` 조합 허용

업데이트된 기본값:

- `strict`: `true`
- `module`: `esnext`
- `target`: `es2025`
- `types`: `[]` (빌드 시간 20-50% 개선)

Deprecated 옵션
(`"ignoreDeprecations": "6.0"`으로 우회 가능,
7.0에서 완전 제거 예정):

- `target: es5`, `--outFile`,
  `--downlevelIteration`
- `--moduleResolution node10` / `classic`
- AMD/System/UMD 등 레거시 모듈 포맷

## TypeScript 7 (native)

[A 10x Faster TypeScript](https://devblogs.microsoft.com/typescript/typescript-native-port/)

Staging repo for development of native port of TypeScript:
<https://github.com/microsoft/typescript-go>

## Articles

[Fully Typed Web Apps | Epic Web Dev](https://www.epicweb.dev/fully-typed-web-apps)
\
→ 한국어 번역:
[완전한 타입 안정성을 가진 웹 애플리케이션 | bohyeon.dev](https://ktseo41.github.io/blog/log/fully-typed-web-apps.html)

## tsafe — Leverage the more advanced TypeScript features

<https://www.tsafe.dev/>

<https://docs.tsafe.dev/>

<https://github.com/garronej/tsafe>

---

[TypeScript Done Wrong](https://blog.openreplay.com/typescript-done-wrong)

[How to write a constant in the TypeScript? | by Przemyslaw Jan Beigert](https://medium.com/@przemyslaw.jan.beigert/how-to-write-a-constant-in-the-typescript-64d296c1e003)
