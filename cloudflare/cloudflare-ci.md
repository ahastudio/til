# Cloudflare CI: Workflows와 Sandbox로 만든 Cloudflare 안의 CI 엔진

> Cloudflare-native continuous integration powered by Workflows and Sandbox

<https://github.com/cloudflare/ci>

HN 토론: <https://news.ycombinator.com/item?id=49168483> (3점, 0개 댓글)

## 소개

Cloudflare CI는 Cloudflare Workflows와 Sandbox 위에 만든
지속적 통합(CI) 엔진이다.
저장소의 최상위가 그대로 `@cloudflare/ci` 패키지이고,
실제로 배포하는 Worker는 `examples/` 아래에 있다.
TypeScript로 쓰였고 Apache-2.0 라이선스이며,
저장소는 2026년 7월 30일에 만들어졌다.
이 문서를 쓴 2026년 10월 4일 기준으로 별은 495개,
포크는 13개이고 마지막 공개 버전은 9월 14일의 0.2.0이다.

이 패키지는 Node.js용 빌드를 내지 않는다.
Cloudflare Workers 런타임을 직접 겨냥하며, TypeScript 소스를 그대로 배포해
Wrangler 같은 Workers 인식 번들러가 처리하게 한다.
`@cloudflare/ci/worker`를 가져오는 Worker는 `nodejs_compat`
호환성 플래그를 켜야 한다.

현재 지원하는 소스 저장소는 Cloudflare Artifacts 하나다.
타입 정의에서 `CiProvider`가 `CloudflareArtifacts`로만 정의되어 있고, 두 예제
모두 Artifacts 저장소에 푸시가 들어올 때 실행된다.
GitHub이나 GitLab 저장소를 직접 연결하는 방법은 저장소에서 찾을 수 없다.

이 문서는 README, 예제, 타입 정의를 읽고 정리한 것이며 직접
배포해서 확인하지는 않았다.

이 패키지는 2026년 8월 4일 Cloudflare 블로그 글 [Run CI/CD for millions of
repos — on your platform, on Cloudflare](ci-workflows.md)에서
CI SDK라는 이름으로 소개되었다.
André Venceslau, Mia Malden, Tomáš Hobza가 쓴 이 글은 코드 저장, 빌드,
테스트, 배포를 모두 Cloudflare 안에서 하는 방향의 첫 조각으로 버전 관리 저장소
Artifacts를 들고, CI SDK가 저장과 빌드와 배포를 잇는다고 설명한다.
글이 겨냥하는 사용자는 플랫폼이다.
플랫폼은 자기 코드와 고객의 코드를 Artifacts의 수백만 저장소에 두고,
고객 대신 CI/CD 파이프라인을 한 번 써서 공유하거나,
원하는 고객에게는 자기 저장소만의 Workflow를 따로 돌리게 할 수 있다고 한다.
글은 CI/CD 파이프라인이 결국 Workflow이며, YAML
대신 TypeScript로 각 단계를 `step.do()`처럼 정의할 수 있다고 주장한다.
푸시 이벤트로 바로 실행되므로 이벤트 구독, 큐, 큐 소비자를 따로 설정하지 않아도
된다는 점도 강조한다.

## 동작 방식

### 파이프라인은 Workflow 클래스 하나다

사용자는 `CIWorkflow`를 상속한 클래스의 `pipeline()` 메서드에 파이프라인을 쓴다.
`ci.runner()`는 이전 스냅샷 없이 새 러너를 시작하고, 반환된 결과의
`runner()`는 그 러너의 작업 공간 스냅샷을 이어받는 연쇄 러너를 시작한다.
각 러너는 Sandbox 안에서 명령을 실행하고,
성공하면 작업 공간을 백업한 스냅샷 핸들을 돌려준다.
연쇄 러너는 이 스냅샷을 복원한 뒤 현재 소스를 덮어씌우고 명령을 실행한다.
별도의 `runner()` 호출은 병렬로 실행할 수 있다.

### 러너는 다시 시도될 수 있다

러너의 명령은 재시도 가능한 Workflow 단계 안에서 실행된다.
README는 그래서 외부 부작용이 있는 명령은 멱등이어야 한다고 분명히 적는다.
명령 실행 제한 시간의 기본값은 지속형 Workflow 단계의 제한 시간보다 10초 짧다.
러너 이름은 지속형 Workflow 단계를 식별하므로 결정적이어야 한다.

### 캐시는 내용 주소 포인터로 찾는다

Sandbox SDK는 작업 공간 백업을 임의의 ID로 저장하므로 다음 실행이 이 백업을
찾을 방법이 원래는 없다.
러너가 `cache: { inputs: [...] }`로 캐시를 켜면,
지정한 경로들의 git blob SHA로 내용 주소 키를 만들고 그 키 위치에 백업의 임의
ID를 가리키는 작은 R2 객체를 쓴다.
다음 실행에서 키가 같으면 이전 스냅샷을 복원하고 현재 소스를 덮어씌운 뒤
명령 실행을 건너뛴다.
타입 정의의 주석에는 캐시 적중 때 `node_modules/`처럼 선언한 경로만 복원하는
`outputs`를 추가할 계획이 할 일로 남아 있다.

### 비밀 값은 단계마다 주입한다

Cloudflare 배포 계정과 API 토큰은 `cloudflareCredentials`를 켠
단계에만 주입된다.
주석은 이렇게 해야 빌드, 테스트, 린트 명령이 그 값을 보지 못한다고 설명한다.
소스 저장소 자격 증명(`sourceControlCredentials`)과 Worker의 비밀
값(`secrets`)도 단계별로 지정한다.

## 파이프라인 쓰기

`examples/cloudflare-artifacts/cloudflare.ci.ts`의 파이프라인은 설치,
병렬 검사, 배포의 세 단계다.

```ts
import { CIWorkflow } from '@cloudflare/ci';
import type { CiContext, CiParams, CloudflareArtifacts } from '@cloudflare/ci';
import type { WorkflowEvent, WorkflowStep } from 'cloudflare:workers';
import type { Bindings } from './env';

export class CI extends CIWorkflow<CloudflareArtifacts, Bindings> {
  protected async pipeline(
    _event: WorkflowEvent<CiParams<CloudflareArtifacts>>,
    _step: WorkflowStep,
    ci: CiContext
  ): Promise<void> {
    // 잠금 파일이 같으면 설치 결과 스냅샷을 다시 쓴다
    const deps = await ci.runner({
      name: 'install',
      command: 'npm ci',
      cache: { inputs: ['package.json', 'package-lock.json'] },
    });

    // 설치 스냅샷에서 이어지는 네 러너를 병렬로 실행한다
    await Promise.all([
      deps.runner({ name: 'lint', command: 'npm run lint' }),
      deps.runner({ name: 'test', command: 'npm run test' }),
      deps.runner({ name: 'typecheck', command: 'npm run typecheck' }),
      deps.runner({ name: 'build', command: 'npm run build' }),
    ]);

    // 배포 단계에만 Cloudflare 자격 증명을 준다
    await deps.runner({
      name: 'deploy',
      command: 'npm exec wrangler deploy',
      cloudflareCredentials: {
        accountId: this.env.CLOUDFLARE_DEPLOY_ACCOUNT_ID,
      },
    });
  }
}
```

### 배포하기

예제는 소스 저장소를 만들어 주지 않는다.
먼저 Cloudflare Artifacts 저장소를 만들고 빌드할 소스를 넣어 두어야 하며, 그
저장소에 푸시가 들어와야 파이프라인이 시작된다.

설정할 것은 이렇다.

- `wrangler.jsonc`의 `artifacts[].namespace`와 `triggers.events[].filter.namespace`에 같은 Artifacts 네임스페이스를 넣는다.
- `triggers.events[].filter.repo_name`에 저장소 이름을 넣는다.
- `CLOUDFLARE_ACCOUNT_ID`와 `CLOUDFLARE_DEPLOY_ACCOUNT_ID`를 넣고, `BACKUP_BUCKET_NAME`을 설정한 `BACKUP_BUCKET` 이름과 같게 둔다.
- 비밀 값은 `wrangler secret put`으로 넣는다.

```sh
pnpm exec wrangler secret put CF_TOKEN
pnpm exec wrangler secret put R2_ACCESS_KEY_ID
pnpm exec wrangler secret put R2_SECRET_ACCESS_KEY
pnpm run deploy
```

최상위 이벤트 트리거가 `cf.artifacts.repo.pushed` 이벤트를 Workflow로 바로
보내므로 큐는 필요 없다.
`cloudflare.ci.ts`를 바꾸면 Worker를 다시 배포해야 반영된다.

## 자가 치유 예제

`examples/self-healing`은 같은 파이프라인에 실패를 고치는
Healing Agent를 붙인다.
에이전트, 도구, 안전장치, AI 의존성은 모두 예제 쪽 코드이고 `@cloudflare/ci`
패키지에는 들어 있지 않다.
패키지는 중립적인 러너 실패 진단만 내보내고,
예제가 이를 Workflow 이벤트와 합쳐 에이전트에게 넘긴다.

동작 순서는 이렇다.

1. 설치나 검사 러너가 실패하면 `isCiRunnerFailure`로 러너 실패인지 확인한다.
2. 기준 브랜치가 없으면 고치지 않고 오류를 낸다.
3. `heal` 단계를 재시도 없이 최대 5시간 제한으로 실행해 에이전트에게 검증을 약하게 하지 말고 관찰된 모든 실패를 고치라고 요청한다.
4. 검증된 수정은 `ci-autofix/<run-id>` 브랜치에 푸시된다.
5. 원래 실행은 여전히 실패로 끝나는데, 원래 리비전은 깨진 채로 남기 때문이다.

예제의 기본 모델은 `@cf/moonshotai/kimi-k2.7-code`이며
`Healer.getModel()`에서 바꾼다.

## 트레이드오프

### 플랫폼 안에서 끝나는 대신 플랫폼에 묶인다

Workflows, Sandbox, R2, Artifacts를 모두 Cloudflare 안에서 쓰므로 별도의 CI
서비스나 러너 서버가 필요 없다.
대가는 소스 저장소까지 Cloudflare Artifacts여야 한다는 점이다.
현재 코드에서 다른 소스 저장소를 연결하려면 제공자 정의를 직접 구현해야 하며, 그
경로는 문서화되어 있지 않다.

### 지속형 단계는 재개를 주지만 멱등성을 요구한다

Workflow 단계가 지속형이어서 실패한 단계만 다시 시도할 수 있다.
그 대신 배포나 외부 API 호출처럼 부작용이 있는 명령은 여러 번
실행되어도 안전해야 한다.
이 요구를 지키지 않으면 재시도가 중복 배포나 중복 알림으로 이어질 수 있다.

### 전체 작업 공간 스냅샷은 단순하지만 무겁다

캐시 적중은 선언한 경로가 아니라 작업 공간 전체 스냅샷을 복원한다.
설정은 간단하지만 작업 공간이 크면 복원 비용도 커진다.
타입 정의에 남은 `outputs` 계획이 이 비용을 줄이려는 다음 단계로 보인다.

## 함정

- **트리거 필터가 틀려도 오류가 나지 않는다.**
  README는 네임스페이스나 저장소 이름이 맞지 않으면
  트리거가 조용히 발화하지 않는다고 두 번 경고한다.
- **로그는 비밀 값을 가리지 않는다.**
  `CiRunnerResult.logs`는 원본 명령 출력이며,
  비밀을 가리는 것은 알림 미리보기와 실패 메시지뿐이다.
  명령이 비밀 값을 출력하면 로그에 그대로 남는다.
- **러너 이름을 실행마다 바꾸면 안 된다.**
  이름이 지속형 단계를 식별하므로 날짜나 무작위 값을 넣으면 재개가 깨질 수 있다.
- **예제끼리 자원 이름이 겹치면 안 된다.**
  자가 치유 예제는 Workflow, Worker, 백업 버킷 이름이
  다른 배포 예제와 겹치지 않게 하라고 안내한다.
- **자가 치유가 성공해도 실행은 실패로 남는다.**
  수정은 별도 브랜치에 있으므로 사람이 검토하고 병합해야 한다.

## 기억할 원칙

### CI의 상태를 지속형 실행에 맡기면 명령의 성질이 바뀐다

전통적인 CI 러너는 명령을 한 번 실행하고 결과를 보고한다.
Cloudflare CI는 명령을 재시도 가능한 지속형 단계로 감싸서,
중간에 실패해도 앞 단계의 스냅샷에서 다시 시작할 수 있게 한다.
이 구조에서 파이프라인 작성자는 각 명령이 여러 번 실행될 수
있다는 전제로 써야 한다.
배포를 마지막 단계에 두고, 그 단계만 자격 증명을 받도록 나누는 예제의 구성이
이 전제에 맞춘 모양이다.

### 자동 수정은 실패를 지우지 않고 제안으로 남긴다

자가 치유 예제는 고친 결과를 별도 브랜치에 올리고 원래 실행은 실패로 둔다.
수정이 맞는지는 사람이 판단하게 하고,
깨진 리비전이 성공으로 기록되지 않게 하는 선택이다.
에이전트에게 맡기는 범위를 정할 때 이 경계, 곧 고치는 일은 맡기되 통과 여부를
바꾸는 일은 맡기지 않는다는 원칙이 유용하다.
