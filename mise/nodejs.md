# Node.js

## Node.js 설치

```bash
mise use --global node@24.11.0

mise install node@22.21.1

mise list node

node -v
# → .nvmrc 파일 인식
# 만약 .nvmrc 파일에 명시된 버전이 없다면 자동으로 설치된다.

# 명시적으로 설치할 수도 있다.
mise install
```

## Node.js 쿡북

<https://mise.jdx.dev/mise-cookbook/nodejs.html>

mise로 Node.js와 패키지 매니저를 고르고,
프로젝트가 선언한 스크립트와 의존성을 실행하는 방법을 정리한 공식 쿡북이다.

### 디렉터리에 Node.js 설치하기

```bash
mise use node
```

최신 버전의 Node.js를 설치하고 `mise.toml` 파일을 만든다.

```toml
[tools]
node = "latest"
```

전역으로 설치하려면 `-g`를 붙이고 버전을 지정한다.

```bash
mise use -g node@26
```

### node_modules 바이너리를 PATH에 추가하기

`package.json`에 있는 패키지의 바이너리는 보통 `npx`나 전체
경로로 실행해야 한다.

```bash
mise exec -- npm install --save-dev eslint
eslint --version # 동작하지 않는다.
npx eslint --version # 동작한다.
```

`mise.toml`에 `node_modules/.bin`을 PATH로 추가하면 `npx` 없이 CLI를 쓸 수 있다.

```toml
[env]
_.path = ['{{config_root}}/node_modules/.bin']
```

```bash
mise exec -- npm install --save-dev eslint
mise exec -- eslint --version # 셸 활성화 없이도 동작한다.
```

셸 활성화(`mise activate`)를 해 두었다면
`eslint --version`을 바로 실행해도 된다.

### 프로젝트 예시: npm과 태스크

이 예시는 `start`, `lint`, `test`, `build` 스크립트가 있는 `package.json`과
커밋된 `package-lock.json`을 전제로 한다.
ESLint, TypeScript, 테스트 러너는 프로젝트의 `devDependencies`에 두어 npm의 잠금
파일이 패키지와 함께 버전을 통제하게 한다.

```toml
[tools]
node = "24"

[env]
NODE_ENV = { default = "development" }

[tasks.install]
description = "Install the locked npm dependency tree"
alias = "i"
run = "npm ci"

[tasks.start]
description = "Start the development server"
alias = "s"
run = "npm run start"

[tasks.lint]
description = "Run the project's lint script"
alias = "l"
run = "npm run lint"

[tasks.test]
description = "Run the project's tests"
alias = "t"
run = "npm test"

[tasks.build]
description = "Build the project"
alias = "b"
run = "npm run build"
```

저장소를 클론한 뒤 `mise run install`을 실행하고,
이어서 `mise run test`나 `mise run start`를 실행한다.
npm 스크립트는 이미 `node_modules/.bin`을 PATH에 올려 주므로,
이 태스크들에는 별도의 PATH 지시문이 필요 없다.
잠금 파일이 없는 새 프로젝트에서는 `mise exec -- npm install`을 한 번 실행하고
만들어진 잠금 파일을 커밋한다.

### pnpm 예시

패키지 매니저로 pnpm을 쓰는 예시다.
기존 `package.json`에 다음 필드를 합치고, `dev` 스크립트도 정의되어 있어야 한다.

```json
{
  "devEngines": {
    "packageManager": {
      "name": "pnpm",
      "version": "10.15.0"
    }
  }
}
```

```toml
[tools]
node = '24'

[settings]
# package.json에서 pnpm 버전을 읽는다.
idiomatic_version_file_enable_tools = ['pnpm']

[env]
_.path = ['{{config_root}}/node_modules/.bin']

[tasks.pnpm-install]
description = 'Installs dependencies with pnpm'
run = 'pnpm install'
sources = ['package.json', 'pnpm-lock.yaml', 'mise.toml']
outputs = ['node_modules/.pnpm/lock.yaml']

[tasks.dev]
description = 'Calls your dev script in `package.json`'
run = 'node --run dev'
depends = ['pnpm-install']
```

`mise run dev`를 실행하면 선택한 도구를 설치하고 의존성을 준비한 뒤 기존
애플리케이션을 시작한다.

- 올바른 버전의 Node.js를 설치한다.
- `package.json`에 선언된 버전의 pnpm을 설치한다.
- `sources`나 `outputs`가 오래됐을 때만 `pnpm install`이 `node --run dev`보다 먼저 실행된다.

`pnpm-install` 태스크는 `package.json`, `pnpm-lock.yaml`, `mise.toml`이 바뀌지
않았고 `node_modules/.pnpm/lock.yaml`이 있으며 최신이면 건너뛴다.
이 타임스탬프 검사는 `node_modules`의 모든 파일을 확인하지 않는다.
의존성이 없거나 손상됐다면 `mise run --force pnpm-install`을 실행한다.

### Corepack 대체하기

mise는 Corepack 없이 npm, pnpm, Yarn을 설치하고 선택할 수 있다.
가장 단순한 방법은 `mise.toml`에 Node.js와 패키지 매니저를 함께 선언하는 것이다.

```toml
[tools]
node = '24'
pnpm = '10.15.0'
```

패키지 매니저 버전의 출처를 `package.json`으로 유지하려면
idiomatic version file 지원을 켠다.

```json
{
  "packageManager": "pnpm@10.15.0+sha224.88208eb7c2e7de6ed534fa298248dee656723116995eda4b508fd0c9"
}
```

```toml
[tools]
node = '24'

[settings]
idiomatic_version_file_enable_tools = ['pnpm']
```

`mise install`로 선언된 버전을 설치한다.
셸 활성화를 했다면 설정된 패키지 매니저가 없을 때 shim이 처음
호출되는 시점에 설치해 주기도 한다.
이는 기본으로 켜져 있는 `not_found_auto_install` 설정을 쓴다.

Corepack 방식의 `+sha1`, `+sha224`, `+sha256`, `+sha384`, `+sha512`
접미사는 설치 전에 정확한 패키지 매니저 산출물에 대해 검증된다.
npm, pnpm, Yarn Classic은 레지스트리 tarball이고,
최신 Yarn은 Yarn이 공개한 CLI 파일이 대상이다.
체크섬이 없으면 패키지 매니저가 선호하는 레지스트리 백엔드(보통
Aqua)와 그 백엔드의 일반 검증을 쓴다.

저장소가 선언할 수 있는 패키지 매니저마다 설정을 켜야 한다.

```toml
[settings]
idiomatic_version_file_enable_tools = ['npm', 'pnpm', 'yarn']
```

Corepack과 달리 mise는 프로젝트가 아무것도 선언하지 않았을 때 쓸 검증된 기본
패키지 매니저 버전을 제공하지 않는다.
`mise.toml`, `package.json`, 전역 mise 설정 중 한 곳에서 버전을 지정해야 한다.
