# just-bash: Bash for Agents

<https://justbash.dev/>

<https://github.com/vercel-labs/just-bash>

## 한 줄 요약

Bash의 파서, 인터프리터, 77개 이상의 명령어를 TypeScript로 재구현한
가상 쉘 환경이다. AI 에이전트가 안전하게 파일시스템을 탐색하고 데이터를
처리할 수 있도록 설계됐다.

## 배경: "Bash is all you need"

Vercel은 에이전트 도구를 80% 줄이고 bash 하나만 남겼더니 성공률이 80%에서
100%로 올랐다는 블로그를 공개했다. 모델이 이미 Unix 시맨틱에 익숙하므로,
새 API를 가르치는 것보다 `grep`, `find`, `cat` 같은 기존 명령어를
제공하는 편이 낫다는 가설이다. just-bash는 이 가설을 제품화한 결과물이다.

Guillermo Rauch(Vercel CEO)의 표현:

> The primary lesson from the actually successful agents so far
> is the return to Unix fundamentals: file systems, shells,
> processes & CLIs.

## 아키텍처

```
입력 스크립트
  │
  ▼
┌──────────┐    ┌─────────┐    ┌─────────────┐
│  Lexer   │ →  │ Parser  │ →  │ Interpreter │
│(토크나이저)│    │(AST 생성)│    │ (AST 실행)  │
└──────────┘    └─────────┘    └──────┬──────┘
                                      │
                    ┌─────────────────┼──────────────┐
                    │                 │              │
                    ▼                 ▼              ▼
              ┌──────────┐    ┌───────────┐  ┌──────────┐
              │ Builtins │    │ Commands  │  │ Virtual  │
              │(cd, echo,│    │(grep, awk,│  │    FS    │
              │ export)  │    │ sed, jq)  │  │          │
              └──────────┘    └───────────┘  └──────────┘
```

- **Lexer**: 상태 기계 토크나이저. heredoc, 인용문, 명령 치환 처리.
- **Parser**: 재귀 하강 파서. 깊이/반복 제한으로 DoS 방지.
- **Interpreter**: AST 실행 엔진. 변수 확장, 글로브,
  파이프라인, 리디렉션 처리.
- **Commands**: 77개 이상의 명령어를 TypeScript로 구현.
  grep은 re2js(안전한 RE2), awk는 자체 파서 포함.

### 규모

358개의 비테스트 TypeScript 파일, 약 54,130줄.
"Just Bash"라는 이름과 달리 상당한 규모의 구현체다.

## 가상 파일시스템

4가지 구현을 제공하며, 플러그인 인터페이스(`IFileSystem`)로
교체할 수 있다.

| 구현체      | 읽기   | 쓰기     | 용도                 |
|-------------|--------|----------|----------------------|
| InMemoryFs  | 메모리 | 메모리   | 기본값. 완전 격리    |
| OverlayFs   | 디스크 | 메모리   | CLI 기본. CoW 샌드박스|
| ReadWriteFs | 디스크 | 디스크   | 신뢰 환경. 직접 접근 |
| MountableFs | 혼합   | 혼합     | 경로별 다중 마운트   |

```typescript
const fs = new MountableFs();
fs.mount("/mnt/ro", new OverlayFs("/project"));
fs.mount("/home/agent", new ReadWriteFs("/workspace"));
// /mnt/ro는 읽기 전용, /home/agent는 쓰기 가능
```

지연 로딩 파일도 지원한다.
파일 값에 함수를 넘기면 첫 읽기 시에만 호출된다.

```typescript
const bash = new Bash({
  files: {
    "/data/config.json": () =>
      JSON.stringify({ key: "value" }),
    "/data/remote.txt": async () =>
      (await fetch("https://example.com")).text(),
  },
});
```

## 보안 모델: 5계층 방어

```
계층 1: 아키텍처 격리
  ├─ 가상 파일시스템 (실제 시스템 보호)
  ├─ exec() 상태 격리 (각 호출 독립)
  └─ OverlayFS (읽기는 디스크, 쓰기는 메모리)

계층 2: 입력 제한
  ├─ 입력 크기 1MB, 토큰 수 100,000
  └─ 파서 깊이 500, 반복 1,000,000

계층 3: 런타임 제한
  ├─ 함수 재귀 깊이 100
  ├─ 총 명령어 수 10,000
  ├─ 루프 반복 10,000
  └─ 문자열 길이 10MB

계층 4: 네트워크 제어
  ├─ 기본 비활성화
  ├─ URL 접두사 화이트리스트
  └─ HTTP 메서드 제한

계층 5: Defense-in-Depth
  ├─ Function/eval 차단
  ├─ process 차단
  └─ AsyncLocalStorage 기반 컨텍스트 인식
```

### exec() 격리

각 `exec()` 호출은 독립적인 상태 사본을 생성한다.
환경 변수, cwd, 함수, 쉘 옵션은 격리되지만 파일시스템은 공유된다.
환경 변수 저장에 `Map`을 사용해 프로토타입 오염을 방지한다.

### 네트워크 접근 제어

```typescript
const bash = new Bash({
  network: {
    allowedUrlPrefixes: [
      "https://api.github.com/repos/myorg/",
    ],
    allowedMethods: ["GET", "HEAD"],
  },
});
```

기본값은 네트워크 완전 차단이다.
리디렉트 체인도 각 대상을 화이트리스트와 대조한다.

## bash-tool: AI SDK 통합

just-bash를 AI SDK에서 바로 쓸 수 있는 도구로 래핑한 패키지다.
`bash`, `readFile`, `writeFile` 세 가지 도구를 제공한다.

```typescript
import { createBashTool } from "bash-tool";

const bashTool = createBashTool({
  files: {
    "/data/users.json": usersData,
  },
});
```

### 토큰 효율

전체 파일을 컨텍스트에 넣는 방식 대비 95% 이상 토큰을 절감한다.
에이전트가 `grep`, `find`, `jq` 등으로 필요한 부분만 추출하기
때문이다.

## Sandbox API 호환

`@vercel/sandbox`와 API 호환 클래스를 제공한다.
개발 시 just-bash로 시작하고, 프로덕션에서 실제 VM으로 교체할 수
있다.

```typescript
// just-bash의 Sandbox
const sandbox = await Sandbox.create({ cwd: "/app" });
await sandbox.writeFiles({
  "/app/script.sh": 'echo "Hello"',
});
const cmd = await sandbox.runCommand(
  "bash /app/script.sh"
);
const output = await cmd.stdout();

// @vercel/sandbox와 동일한 API
```

## 벤치마크: Bash vs SQL

Vercel이 GitHub 이슈/PR 데이터셋으로 테스트한 결과:

| 방식         | 정확도 | 토큰 사용량 | 비용   |
|--------------|--------|-------------|--------|
| SQL          | 100%   | 1x          | 1x     |
| Bash         | 53%    | 7x          | 6.5x   |
| 파일 검색    | 63%    | -           | -      |
| Bash + SQL   | 100%   | 2x          | 2x     |

구조화된 데이터 쿼리에서는 SQL이 압도적이다.
하지만 코드 탐색, 파일 검색, 비정형 텍스트 처리에서는 bash가 강점을
보인다. Vercel은 **하이브리드 접근(bash + SQL)**이 가장 신뢰할 수
있다고 결론지었다. SQL로 쿼리하고, bash로 결과를 검증하는
이중 확인(double-checking) 패턴이 100% 정확도를 유지한다.

## 코드 분석에서 발견한 흥미로운 설계

### 지연 로딩 레지스트리

78개 명령어를 동적 import로 지연 로딩한다.
사용하지 않는 명령어는 메모리에 올라가지 않는다.

```typescript
const commandLoaders = [
  {
    name: "echo",
    load: () =>
      import("./echo/echo.js").then(
        (m) => m.echoCommand
      ),
  },
  // ... 78개
];
```

### AST 변환 플러그인

스크립트 실행 전에 AST를 변환하는 플러그인 파이프라인을 지원한다.
TeePlugin은 각 파이프라인 단계의 출력을 파일로 캡처한다.

```bash
# 변환 전
echo hello | grep hello

# TeePlugin 적용 후
echo hello \
  | tee /tmp/logs/000-echo.stdout.txt \
  | grep hello \
  | tee /tmp/logs/001-grep.stdout.txt
```

### 조건부 명령어 활성화

curl은 네트워크 설정이 있을 때만 등록된다.
Python은 pyodide(WASM) 기반으로 명시적 opt-in이 필요하다.
기본 상태에서는 위험한 기능이 비활성화되어 있다.

## 인사이트

### Unix 시맨틱의 재발견

AI 에이전트 도구 설계에서 새로운 API를 만드는 대신 Unix 명령어를
그대로 제공하는 전략이 효과적이다. LLM이 이미 학습한 패턴을
활용하므로 별도 도구 사용법을 가르칠 필요가 없다.

### 격리와 기능의 균형

완전한 샌드박스(바이너리 실행 불가)와 실용적 기능(77개 명령어,
SQLite, JSON/YAML/CSV 처리) 사이의 균형점을 잡았다.
"쓸 수 있는 만큼만 열어준다"는 원칙이 일관되게 적용됐다.

### 토큰 경제학

에이전트에게 파일 전체를 주는 대신 bash 명령어로 필요한 부분만
추출하게 하면 토큰을 95% 절감할 수 있다. 이는 비용뿐 아니라
정확도에도 영향을 미친다. 컨텍스트가 작을수록 모델의 집중도가
높아진다.

### "Just Bash"는 만능이 아니다

Vercel 자체 벤치마크에서 bash 단독 정확도는 53%에 그쳤다.
구조화된 데이터에는 SQL이, 비정형 탐색에는 bash가 적합하다.
도구 선택은 데이터 특성에 맞춰야 한다.

### 점진적 마이그레이션 전략

Sandbox API 호환은 단순한 편의 기능이 아니다.
개발 시 가볍게 시작하고(just-bash), 필요할 때 풀 VM으로
교체하는 점진적 마이그레이션 경로를 제공한다.
이런 전략적 API 호환은 도구 채택의 진입 장벽을 낮춘다.

## 참고 자료

- [just-bash GitHub](https://github.com/vercel-labs/just-bash)
- [bash-tool GitHub](https://github.com/vercel-labs/bash-tool)
- [Testing if "bash is all you need" - Vercel Blog](https://vercel.com/blog/testing-if-bash-is-all-you-need)
- [We removed 80% of our agent's tools - Vercel Blog](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools)
- [Introducing bash-tool - Vercel Changelog](https://vercel.com/changelog/introducing-bash-tool-for-filesystem-based-context-retrieval)
