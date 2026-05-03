# pnpm v11

<https://pnpm.io/blog/releases/11.0>

## 요약

pnpm 11.0이 2026년 4월 28일에 출시됐다.
주요 방향은 보안 기본값 강화, 성능 향상, 아키텍처 정리다.
Node.js 22 이상을 요구하고(18–21 지원 종료), 순수 ESM으로 배포된다.

보안 기본값이 대폭 강화됐다.
`minimumReleaseAge`가 기본값 0에서 1440분(24시간)으로 변경돼
새로 등록된 패키지는 최소 하루가 지나야 해석된다.
`blockExoticSubdeps`와 `strictDepBuilds`도 기본값 true가 됐다.
공급망 공격(supply-chain attack)을 사전에 차단하는 기본값 설계다.

성능에서는 스토어 인덱스를 수백만 개의 JSON 파일 대신
단일 SQLite 데이터베이스로 전환했다(Store v11).
시스템 콜 수가 줄고 설치 속도가 크게 향상된다.
HTTP 클라이언트도 `node-fetch`에서 `undici`로 교체해 keep-alive와
Happy Eyeballs 듀얼스택 지원을 개선했다.

설정 구조도 재편됐다.
`.npmrc` 파일은 인증과 레지스트리 설정만 처리하고,
pnpm 전용 설정은 `pnpm-workspace.yaml` 또는 `~/.config/pnpm/config.yaml`로 이동한다.
환경 변수 접두사가 `npm_config_*`에서 `pnpm_config_*`로 바뀐다.

## 분析

### 빌드 설정 통합: `allowBuilds`

다섯 개 설정이 하나로 통합됐다.
`onlyBuiltDependencies`, `neverBuiltDependencies`, `ignoredBuiltDependencies`,
`ignoreDepScripts`, `onlyBuiltDependenciesFile`이 모두 제거되고
`allowBuilds` 맵으로 대체된다.
패키지 이름 패턴에 불리언 값을 매핑하는 방식으로 어떤 패키지의 빌드를
허용·차단할지 한 곳에서 관리한다.
이전 버전에서 여러 설정이 겹치거나 충돌하던 문제를 해소하는 정리다.

### 글로벌 패키지 격리

글로벌 패키지가 이제 독립 디렉터리에 분리된 `package.json`, `node_modules`,
락파일을 가진다.
이전 버전에서는 글로벌로 설치한 패키지들이 공유 `node_modules`에 섞여
의존성 충돌이 발생하는 경우가 있었다.
바이너리는 `PNPM_HOME` 안의 `bin` 하위 디렉터리로 이동했으므로
업그레이드 후 `pnpm setup`을 실행해 셸 설정을 갱신해야 한다.

### publish 워크플로우 독립

`publish`, `login`, `logout`, `view`, `deprecate`, `unpublish`, `dist-tag`,
`version` 명령이 npm CLI에 위임하는 대신 pnpm 네이티브로 구현됐다.
npm에 의존하지 않고 pnpm만으로 패키지를 배포할 수 있게 됐다.
반면 `access`, `team`, `token` 명령은 “not implemented” 오류를 반환한다.

보안 취약점 추적도 CVE 기반에서 GHSA 기반으로 전환됐다.
`ignoreCves`를 쓰던 설정은 `ignoreGhsas`로 마이그레이션해야 한다.

### 새 명령

눈에 띄는 추가 명령들이 있다.
`pnpm ci`(클린 인스톨), `pnpm clean`(`node_modules` 제거),
`pnpm sbom`(소프트웨어 자재 명세 생성), `pnpm runtime set`(`env use` 대체),
`pnpm with`(특정 pnpm 버전으로 실행).
단축 별칭으로 `pn`(pnpm), `pnx`(pnpx)도 추가됐다.

## 비평

### 강점: 공급망 보안을 기본값으로

`minimumReleaseAge` 기본값 1440분은 타이포스쿼팅(typosquatting)과
악성 패키지 즉시 배포 공격을 방어하는 실용적 선택이다.
신규 등록 패키지가 24시간 안에 설치되지 않으므로, 공격자가 패키지를 등록하고
피해자가 설치하기까지의 시간 창이 좁아진다.
`security/minimum-release-age.md`에서 다뤘던 이 기능이 이제 기본값이 됐다는 것은
업계 표준으로 수렴하는 신호다.

### 약점: 마이그레이션 비용이 높다

v10에서 v11로의 마이그레이션은 기계적 변경 사항이 많다.
환경 변수 접두사 변경, `.npmrc` 역할 축소, `allowBuilds` 전환, GHSA 전환 —
이 변경들이 모두 동시에 일어나므로 대형 모노레포에서 마이그레이션 부담이 크다.
자동화 codemod(`pnpm-v10-to-v11`)가 제공되지만,
수동 검토가 필요한 부분이 남는다.

## 인사이트

### SQLite 스토어: 파일 시스템의 한계를 인정한 설계 전환

수백만 개의 작은 JSON 파일에서 단일 SQLite로의 전환은
파일 시스템이 수백만 개 소파일 I/O에 부적합하다는 오래된 관찰을 실천한 것이다.
특히 inode 수가 제한된 일부 파일 시스템이나, 많은 소파일이 디렉터리 캐시를
오염시키는 macOS에서 성능 개선이 두드러질 것이다.
SQLite는 단순한 “더 빠른 저장소”가 아니라 트랜잭션과 인덱스를 갖춘
구조화된 데이터 접근을 가능하게 한다.
pnpm store 정보를 쿼리하거나 분석하는 도구 생태계도 기대할 수 있다.

### 패키지 매니저가 보안 게이트키퍼가 되는 흐름

v11의 보안 기본값 강화 — `minimumReleaseAge`, `blockExoticSubdeps`,
`strictDepBuilds` — 는 패키지 매니저가 단순한 의존성 설치 도구를 넘어
공급망 보안의 첫 번째 방어선이 되겠다는 선언이다.
Sigstore 서명 검증, SBOM 생성(`pnpm sbom`), 최소 패키지 나이 요건이 모두
같은 방향을 가리킨다.

이 흐름은 `npm audit`이 취약점 정보를 제공하는 데서 출발했지만,
이제는 인스톨 단계 자체에서 의심스러운 패키지를 차단하는 방향으로 발전했다.
패키지 매니저가 보안 정책의 집행 지점이 되면, 조직은 중앙 정책 파일
(`pnpm-workspace.yaml`)에 보안 규칙을 명시하고 모든 CI/CD 파이프라인에
자동 적용할 수 있다.
이것은 개발자 개개인의 보안 의식 교육보다 훨씬 효과적인 보안 강화 경로다.

### `.npmrc` 역할 축소와 설정 파편화 종식

pnpm이 `.npmrc`를 인증·레지스트리 전용으로 제한하고
자체 설정을 `pnpm-workspace.yaml`로 분리한 것은
오랫동안 이어진 “어디에 무슨 설정을 두어야 하는가” 혼란에 대한 답이다.
`.npmrc`는 원래 npm 전용 파일이지만, pnpm을 포함한 여러 도구가 이 파일을
읽으면서 “npm 설정인지 pnpm 설정인지” 경계가 불분명해졌다.

명확한 분리는 모노레포에서 특히 의미 있다.
루트 `.npmrc`가 레지스트리 인증만 담고, `pnpm-workspace.yaml`이 워크스페이스
동작을 정의하면, 각 파일의 역할이 명확하다.
이것은 단일 책임 원칙을 설정 파일 수준에서 실천한 것이다.
