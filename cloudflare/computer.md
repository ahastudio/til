# Cloudflare Computer: 에이전트에게 컨테이너 대신 컴퓨터를 주겠다는 실험

<https://github.com/cloudflare/computer>

HN 토론: <https://news.ycombinator.com/item?id=49155598> (13점, 3개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=49155280> (10점, 0개 댓글)

## 소개

Cloudflare Computer는 Durable Object 안에 사는 가상 파일시스템이다.
Durable Object가 권위 있는 상태를 SQLite에 들고 있고, `workspace.runtime`이라는 하나의 실행 표면을 통해 여러 실행 백엔드를 끼워 쓰게 한다.
npm 패키지 이름은 `@cloudflare/computer`이고, 저장소 설명은 “Give your agent a computer”다.
MIT 라이선스이며 TypeScript로 작성됐고, 2026년 6월 5일에 만들어져 9월 23일 기준 스타 9,254개, 포크 535개다.

README는 첫머리부터 이 패키지가 미리 보기라고 분명히 밝힌다.
피드백을 받기 위한 것이고, API는 불안정하며 설계가 바뀔 수 있고, 실험과 프로토타입에는 적합하지만 프로덕션에는 적합하지 않다는 것이다.
`docs/`의 명세는 앞을 내다보고 쓴 것이라 지금의 코드가 아니라 의도로 읽으라는 단서도 붙어 있다.
외부 기여는 이슈와 토론으로만 받고, 요청하지 않은 풀 리퀘스트는 받지 않는다.

출시는 2026년 8월 3일 Matt Carey와 Aron Carroll이 쓴 블로그 글 [Your agent needs a computer, not a container — introducing @cloudflare/computer](https://blog.cloudflare.com/cloudflare-computer/)로 알려졌다.
글의 논지는 제목 그대로다.
가장 유능한 에이전트들은 공통적으로 자기 컴퓨터를 받는데, 모든 에이전트에게 컨테이너를 하나씩 주는 방식은 수억, 수십억 개의 동시 에이전트로 확장되지 않는다는 것이다.
모든 클라우드와 하이퍼스케일러를 합쳐도 모든 회사가 모든 사용자의 에이전트에게 컨테이너 환경을 줄 만큼의 컴퓨트는 없고, 그래서 업계가 GPU뿐 아니라 CPU 컴퓨트를 절박하게 찾고 있다고 적는다.

Cloudflare의 답은 isolate다.
거의 10년 전 Workers를 내놓을 때, 그리고 거의 6년 전 [[durable-objects]]를 내놓을 때 같은 베팅을 했다고 글은 말한다.
isolate는 수평으로 무한히 확장되고, 빠르게 뜨고 내려가며, 에이전트가 쉴 때 동면하고, 자기 상태를 저장하고, 신뢰할 수 없는 코드를 돌릴 isolate를 스스로 띄울 수 있다는 것이다.
작년에는 isolate가 자기 컨테이너 샌드박스를 띄울 수 있게 했고, 에이전트 하네스는 Durable Object 안에서 돌리고 컨테이너는 도구로 필요할 때만 부르는 구조를 처음부터 권해 왔다.
Computer는 이 두 컴퓨트 원시 요소를 사용자가 직접 조합하던 일을 하나의 추상화로 묶으려는 시도다.

## 구조

### 파일시스템이 중심이고 실행은 끼워 쓴다

모든 것의 중심은 워크스페이스, 곧 SQLite에 저장되는 가상 파일시스템이다.
워크스페이스는 git 저장소, 스토리지 버킷, 그 밖의 파일로 채울 수 있고, R2 버킷을 읽기 전용으로 마운트할 수도 있다.
마운트 아래에 쓰려고 하면 `EROFS`로 거절된다.
`workspace.fs`는 `node:fs/promises`처럼 생겼고 `readFile`, `writeFile`, `mkdir`, `readdir`, `rm`, `grep`을 제공하며, Durable Object가 재시작해도 유지된다.

실행은 `workspace.runtime.exec(source, { backend })` 하나로 들어간다.
`source`가 셸 명령인지 ECMAScript 모듈인지는 고른 백엔드가 정한다.
워크스페이스는 여러 백엔드를 고정 ID로 등록할 수 있고, 백엔드는 처음 쓰일 때 연결된다.
백엔드 없이 만들면 파일시스템만 남는다.
실행 핸들은 라이브 이벤트의 `ReadableStream`이기도 해서, 출력을 Server-Sent Events로 그대로 흘려보낼 수 있다.

### 세 가지 백엔드

지금 들어 있는 백엔드는 세 가지다.

| 백엔드            | 실행하는 것                                    | 필요한 것                                   |
| ----------------- | ---------------------------------------------- | ------------------------------------------- |
| Container         | 완전한 Linux 사용자 공간의 셸 명령             | `computerd`를 돌리는 Cloudflare Container   |
| Worker shell      | Dynamic Worker 안의 just-bash로 돌리는 셸      | Worker Loader 바인딩, `experimental` 플래그 |
| Worker JavaScript | 새 Dynamic Worker에서 평가하는 ECMAScript 모듈 | Worker Loader 바인딩, `experimental` 플래그 |

Container 백엔드는 SQLite 상태를 샌드박스 컨테이너 안에 실제 FUSE 마운트로 투영한다.
컨테이너 쪽 데몬 `computerd`가 상태를 파일시스템으로 마운트하고, 바뀐 내용을 capnweb RPC 채널로 되돌려 동기화한다.
실제 바이너리와 실제 네트워크가 있는 대신 콜드 스타트가 느리다.

Worker shell 백엔드는 Vercel Labs의 [just-bash](https://github.com/vercel-labs/just-bash)를 Dynamic Worker에서 돌린다.
모든 파일시스템 연산이 Workers RPC로 같은 Durable Object에 전달되므로 두 번째 저장소도 동기화 왕복도 없다.
셸은 기능 묶음 단위로 배포되며 `curl`, `html-to-markdown`, `python`, `sqlite`, `js-exec`, `yq`, `file`, `xan`, `jq`가 선택 묶음이다.
가져오지 않은 묶음은 번들러가 떨어뜨린다.

Worker JavaScript 백엔드는 구조화된 입력과 결과, 영속적인 상대 경로 임포트, 설정된 라이브러리, 워크스페이스에 연결된 `node:fs/promises`, 그리고 신뢰된 `ws:git`과 `ws:artifacts` 모듈을 준다.

블로그 글이 나온 8월 3일에는 isolate 셸과 컨테이너 두 가지만 소개됐고, JavaScript 백엔드는 그 뒤에 들어온 것이다.

### 에이전트용 도구와 감사

에이전트용으로는 AI SDK 호환 도구 묶음 `@cloudflare/computer/tools`가 있다.
`read`, `ls`, `find`, `grep`, `write`, `edit`, `delete`, 그리고 선택적인 `exec`다.
`exec`는 `backend` 인자를 받아 여러 런타임에 걸쳐 동작하고, 도구 설명이 에이전트에게 빠르고 싼 워커 백엔드와 기능이 다 갖춰진 컨테이너 중 무엇을 고를지 안내한다.
블로그는 자체 시험에서 프런티어 모델들이 이 선택을 아주 잘하며 필요할 때만 컨테이너로 넘어간다고 적는다.
모든 연산은 통제되고 감사되고 관측되어, 에이전트가 허용된 변경만 하게 하고 무엇을 했는지 기록을 남긴다고도 한다.

## 사용법

가장 작은 쓸모 있는 형태는 실행 백엔드 없는 파일시스템이다.
Durable Object에 `withWorkspace`를 붙이면 영속 파일이 생긴다.

```ts
import { withWorkspace, getWorkspace } from "@cloudflare/computer";
import { DurableObject } from "cloudflare:workers";

export class Agent extends withWorkspace(
  class extends DurableObject<Env> {},
  (self) => ({ storage: self.ctx.storage }),
) {}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const id = env.Agent.idFromName("user-123");
    using ws = await getWorkspace(env.Agent.get(id));

    await ws.fs.writeFile("/notes.md", "- [ ] ship it\n");
    const notes = await ws.fs.readFile("/notes.md", "utf8");

    return new Response(notes);
  },
} satisfies ExportedHandler<Env>;
```

Worker에는 `nodejs_compat` 플래그가 필요하고, Durable Object는 SQLite 클래스로 마이그레이션해야 한다.

```jsonc
{
  "compatibility_flags": ["nodejs_compat"],
  "durable_objects": {
    "bindings": [{ "name": "Agent", "class_name": "Agent" }]
  },
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["Agent"] }
  ]
}
```

명령을 돌리려면 백엔드를 더한다.
컨테이너도 Docker도 필요 없는 Worker shell이 가장 빠른 길이며, 이때는 `experimental` 플래그와 `worker_loaders` 바인딩을 추가해야 한다.

```ts
import { withWorkspace, getWorkspace } from "@cloudflare/computer";
import { WorkerShellBackend } from "@cloudflare/computer/backends/worker-shell";
import curlModules from "@cloudflare/computer/shell/curl";
import { DurableObject } from "cloudflare:workers";

export class Agent extends withWorkspace(
  class extends DurableObject<Env> {},
  (self) => ({
    storage: self.ctx.storage,
    backends: [
      new WorkerShellBackend({
        loader: self.env.LOADER,
        workspace: { binding: "Agent", id: self.ctx.id.toString() },
        ctx: self.ctx,
        commands: [curlModules], // 필요한 명령 묶음만 번들에 넣는다
      }),
    ],
  }),
) {}
```

`fs`로 쓴 파일에 `exec`가 그대로 닿는다.

```ts
using ws = await getWorkspace(env.Agent.get(id));
await ws.fs.writeFile("/hello.txt", "world");
using run = await ws.runtime.exec("cat /hello.txt");
const { stdout, exitCode } = await run.result();
```

저장소의 `examples/`에는 컨테이너, Worker shell, Worker JavaScript, 이그레스 정책(`none`, `all`, 사용자 정의), Code Mode `code` 도구 하나로 된 MCP 서버, `@cloudflare/think` 채팅 에이전트, 두 런타임을 나란히 비교하는 웹 UI, 컨테이너에서 `pandoc`을 돌려 PDF를 만드는 튜토리얼 등이 들어 있다.

## 한계와 성능

패키지 README가 밝히는 한계는 세 가지다.
워크스페이스 하나에 약 10GB이고 Durable Object와 저장 공간을 나눠 쓴다.
컨테이너 쪽 파일시스템은 메모리에 올라가므로 에이전트 규모의 작업 공간을 겨냥해야 하며 모노레포 전체는 대상이 아니다.
컨테이너 접근이 FUSE를 거치므로 큰 `node_modules` 설치나 대용량 tarball 해제 같은 무거운 I/O는 네이티브 디스크보다 느리다.

`docs/19_performance.md`의 수치는 Cloudflare Containers standard-2 인스턴스(vCPU 1개, 메모리 6GiB, 디스크 12GB)에서 `computerd` FUSE 마운트를 메모리 `tmpfs`, 그리고 컨테이너의 ext4 루트 디스크와 비교한 것이다.

| 시나리오                   | computerd | ext4 디스크 | 디스크 대비 |
| -------------------------- | --------- | ----------- | ----------- |
| 파일 1000개 stat           | 1971.9 ms | 2659.3 ms   | 0.91배      |
| 파일 1000개 rm             | 827.7 ms  | 1281.8 ms   | 0.66배      |
| find 트리                  | 1813.6 ms | 4404.2 ms   | 0.72배      |
| git init + 파일 100개 커밋 | 459.2 ms  | 635.4 ms    | 0.72배      |
| 파일 1000개 생성           | 560.6 ms  | 303.2 ms    | 1.85배      |
| 64MiB 읽기                 | 437.5 ms  | 25.6 ms     | 39.72배     |
| 64MiB 복사                 | 1037.2 ms | 39.8 ms     | 40.46배     |

메타데이터가 많은 작업에서는 인메모리 inode 저장소가 실제 디스크보다 빠르고, 큰 순차 I/O에서는 크게 뒤진다.
느린 이유는 쓰기 경로가 512KiB 청크마다 해시를 계산해 내용 주소 방식 블롭 저장소에 넣기 때문이며, 그 덕분에 Durable Object가 바뀐 청크만 동기화하고 같은 내용을 중복 제거할 수 있다.
`cloudflare/sandbox-sdk`의 전체 `npm install`(패키지 854개, 파일 36,675개)은 tmpfs에서 34.3초, ext4 디스크에서 63.9초, `computerd`에서 124.7초가 걸렸다.

저장소를 메모리 대신 디스크에 두는 선택지(`COMPUTERD_DB`)도 있다.
작은 파일 작업이 10~20% 비싸지는 대신, 재시작 뒤 복원이 트리 크기와 무관하게 약 25ms로 고정된다.
파일 3,000개 트리에서 메모리 저장소는 3,749ms 동안 3,002개 항목을 다시 보내야 했고, 파일 저장소는 23ms에 아무것도 보내지 않았다.

## 분석

### 이 설계가 실제로 뒤집는 것은 컴퓨터와 파일의 주종 관계다

블로그 제목은 “컨테이너가 아니라 컴퓨터”지만, 구조를 보면 더 정확한 말은 “컴퓨터가 아니라 파일시스템”이다.
전통적인 샌드박스에서 파일시스템은 컴퓨터에 딸린 것이다.
VM이나 컨테이너가 먼저 있고, 그 디스크에 파일이 있으며, 컨테이너가 죽으면 파일도 함께 사라지거나 따로 백업해야 한다.
Computer는 이 순서를 뒤집는다.
권위 있는 상태는 Durable Object의 SQLite에 있고, 컨테이너는 그 상태를 FUSE로 잠시 빌려 보는 투영에 불과하다.

이렇게 뒤집으면 실행 환경은 일회용이 된다.
에이전트가 파일만 만지는 동안에는 isolate에서 공짜에 가까운 비용으로 돌고, 네이티브 바이너리가 필요한 순간에만 컨테이너가 붙었다가 떨어진다.
두 환경이 같은 파일을 본다는 보장이 이 전환을 가능하게 하며, `computerd`와 capnweb 동기화 계층이 그 보장을 떠맡는다.
블로그가 말한 “두뇌와 손의 분리”, 곧 에이전트 루프와 작업이 일어나는 샌드박스의 분리가 여기서 한 단계 더 나아가 “기억과 손의 분리”가 된다.

### 목표는 기술 문서가 아니라 비용 곡선에 적혀 있다

글의 마지막 문단이 이 프로젝트의 진짜 목표를 밝힌다.
에이전트 작업의 10% 미만에서만 컨테이너가 필요한 런타임을 만들고, 코딩 작업과 오디오·비디오 처리와 문서 작성까지 isolate에서 처리하겠다는 것이다.
이것은 기능 목표가 아니라 원가 목표다.
isolate와 컨테이너의 단위 비용 차이가 크기 때문에, 작업의 90%를 isolate로 옮길 수 있다면 에이전트 한 개당 컴퓨트 비용이 한 자릿수 배로 떨어진다.

그렇게 읽으면 설계 선택들이 한 방향으로 정렬된다.
Worker shell이 just-bash로 셸을 흉내 내는 것, 셸 명령을 기능 묶음으로 쪼개 번들에서 떨어뜨리는 것, `curl`이 `undici` 없이 isolate의 전역 `fetch`로 돌게 한 것은 모두 컨테이너를 부르지 않고 버티는 범위를 넓히려는 조치다.
Cloudflare가 10년 동안 해 온 isolate 베팅을 에이전트 시대의 CPU 부족 담론에 다시 거는 것이고, [[cloudflare-os]]가 그리는 플랫폼의 실행 계층이 이 패키지다.

### 백엔드 선택을 모델에게 맡긴 것이 가장 대담한 결정이다

어느 백엔드로 돌릴지는 사람이 정하지 않는다.
`exec` 도구의 설명문이 “파일 조작 이상이 필요하면 컨테이너를 쓰라”는 식으로 안내하고, 모델이 매 호출마다 고른다.
블로그는 프런티어 모델들이 이 판단을 아주 잘한다고 적는다.

이 결정이 대담한 이유는 스케줄링 정책이 코드가 아니라 자연어 설명으로 표현된다는 데 있다.
전통적인 시스템이라면 워크로드 특성을 보고 스케줄러가 배치를 결정했을 자리에, 이제는 도구 설명 몇 문장이 있다.
설명을 바꾸면 비용 구조가 바뀌고, 모델을 바꾸면 비용 구조가 또 바뀐다.
이 패키지가 “런타임이 효율을 최적화한다”고 말할 때, 그 최적화의 상당 부분은 런타임이 아니라 모델의 판단력에 기대고 있다.

## 비평

### 성능 문서가 스스로의 측정 조건과 모순된다

`docs/19_performance.md`는 첫 문단에서 수치가 Cloudflare Containers standard-2 인스턴스에서 나왔고 `cloudflare/sandbox-sdk`의 전체 `npm install`을 돌렸다고 밝히며, 그 결과로 124.7초라는 숫자까지 표에 싣는다.
그런데 같은 문서의 저장소 비교 절 끝에는, 이 수치들이 Cloudflare Containers 하드웨어가 아니라 Linux 컨테이너 하나에서 나왔고 전체 `npm install`은 돌리지 않았다는 문장이 있다.
맥락상 이 단서는 인메모리 대 디스크 저장소 비교에만 해당하는 것으로 보이지만, 문서는 그 범위를 명시하지 않는다.

읽는 사람 입장에서는 어느 수치가 어느 환경에서 나왔는지 확신할 수 없게 된다.
이 문서는 README가 성능을 판단하라고 직접 가리키는 유일한 근거다.
벤치마크의 가치는 숫자가 아니라 조건의 명확성에서 나오는데, 한 문서 안에서 조건이 두 가지로 서술되면 숫자 전체의 신뢰도가 함께 떨어진다.
미리 보기 단계의 문서라는 사정은 이해할 수 있지만, 성능 주장은 미리 보기에서도 가장 먼저 고쳐야 할 부분이다.

### 모델이 런타임을 잘 고른다는 주장에 수치가 없다

블로그는 자체 시험에서 프런티어 모델들이 올바른 런타임을 아주 잘 고른다고 쓰지만, 몇 번 중 몇 번을 맞혔는지, 틀렸을 때 무슨 일이 생겼는지는 적지 않는다.
앞서 분석했듯 이 판단이 비용 구조 전체를 좌우하므로, 이 문장은 설계의 핵심 가정이다.

틀린 선택의 비용은 비대칭이다.
컨테이너가 필요 없는데 컨테이너를 고르면 돈과 콜드 스타트 시간을 잃는다.
컨테이너가 필요한데 isolate를 고르면, just-bash가 지원하지 않는 명령이나 옵션에서 실패하고 에이전트가 재시도한다.
재시도는 토큰을 쓰고, 토큰 비용이 절약한 CPU 비용을 넘어설 수 있다.
“10% 미만만 컨테이너”라는 목표가 의미 있으려면, 그 10%를 고르느라 치르는 오판의 비용이 함께 측정돼야 한다.

HN에서 noman-land가 “just-bash로 셸 코드를 JavaScript로 번역한다”는 블로그 문장을 인용하며 말을 잇지 못한 것도 같은 지점을 건드린다.[^noman-land]
셸의 의미론은 수십 년 동안 쌓인 예외의 집합이다.
에이전트가 쓰는 셸 한 줄이 실제 bash와 just-bash에서 다르게 동작한다면, 모델은 그 차이를 알지 못한 채 틀린 결과를 믿게 된다.
실패가 오류로 드러나면 다행이지만, 조용히 다른 결과를 내면 모델의 백엔드 선택 능력으로도 막을 수 없다.

### “오픈 소스 라이브러리”는 사실상 한 플랫폼 전용이다

블로그는 이 실험을 오픈 소스 라이브러리로 시작한다고 말하고, 저장소는 MIT 라이선스다.
그러나 핵심 구성 요소인 Durable Object, Dynamic Worker, Worker Loader, Cloudflare Containers는 모두 Cloudflare에만 있다.
`@platformatic/vfs`용 Node 쪽 제공자가 있기는 하지만, 실행 백엔드 세 개 중 어느 것도 다른 클라우드에서 그대로 돌지 않는다.

기여 모델도 이 성격을 드러낸다.
버그 보고와 설계 제안은 받지만 요청하지 않은 풀 리퀘스트는 받지 않고, 승인된 협력자만 개발에 참여한다.
코드를 읽을 수 있고 고쳐 쓸 수 있다는 의미에서 오픈 소스이지만, 공동으로 만드는 프로젝트는 아니다.
HN에서 383toast가 Daytona나 E2B와 어떻게 다르냐고 물었을 때[^383toast], 가장 정직한 답은 기능 비교가 아니라 “Cloudflare 위에서만 돈다”일 것이다.
Alibaba의 [OpenSandbox](../agentic-coding/opensandbox.md)가 Docker와 Kubernetes라는 범용 런타임 위에 규격을 세우려는 것과 정반대 방향이다.

### 블로그의 논지와 실제 구성 사이에 틈이 있다

글은 “컨테이너가 아니라 컴퓨터”라고 선언하지만, 이 패키지에서 완전한 Linux가 필요한 순간은 여전히 컨테이너가 맡는다.
글도 이것을 부정하지 않는다.
그렇다면 주장은 컨테이너를 없애자가 아니라 컨테이너를 덜 쓰자이고, 제목이 약속하는 것보다 훨씬 온건하다.

온건한 주장 쪽이 사실 더 방어하기 쉽다.
문제는 제목이 만든 기대와 문서가 밝힌 한계가 어긋난다는 점이다.
워크스페이스당 약 10GB, 메모리에 올라가는 컨테이너 쪽 파일시스템, 모노레포 비권장, FUSE로 인한 무거운 I/O 저하는 모두 코딩 에이전트가 가장 자주 부딪히는 조건이다.
“컴퓨터”라는 말에서 독자가 떠올리는 것은 이런 제약이 없는 환경이고, 이 패키지가 실제로 주는 것은 에이전트 규모에 맞춘 작은 작업 디렉터리다.

## 인사이트

### 디스크 없는 워크스테이션이 에이전트 인프라로 돌아왔다

1980년대의 디스크 없는 워크스테이션은 파일을 로컬에 두지 않았다.
사용자의 파일은 NFS 서버에 있었고, 워크스테이션은 그것을 마운트해 계산만 했다.
Plan 9는 여기서 더 나아가 모든 자원을 파일로 표현하고 프로세스마다 네임스페이스를 따로 구성하게 했다.
Computer의 구조는 이 계보에 정확히 들어맞는다.
Durable Object가 파일 서버이고, isolate와 컨테이너가 디스크 없는 워크스테이션이며, `computerd`가 NFS 클라이언트 역할을 한다.

이 계보가 알려 주는 것은 성능 특성이다.
NFS 시절에도 메타데이터 연산은 캐시 덕분에 빨랐고 큰 파일의 순차 I/O는 네트워크 대역폭에 묶였다.
Computer의 벤치마크가 메타데이터 작업에서는 디스크보다 빠르고 64MiB 읽기에서는 40배 느린 것은 같은 구조가 같은 결과를 낸 것이다.
그리고 NFS 시절의 교훈도 따라온다.
원격 파일시스템 위에서 무거운 빌드를 돌리면 결국 사람들은 로컬 디스크로 돌아갔다.
에이전트가 `npm install`과 대형 빌드를 자주 돌리는 한, 이 패키지도 같은 압력을 받을 것이다.

AverageYoghurt가 곧 에이전트용 VDI가 생길 것 같다고 쓴 것[^AverageYoghurt]도 같은 계보의 다른 끝을 가리킨다.
VDI는 사용자의 상태를 중앙에 두고 화면만 원격으로 보여 주는 방식이었다.
에이전트에게는 화면이 필요 없으므로, 남는 것은 중앙의 상태와 필요할 때만 붙는 계산이다.

### 도구 설명이 스케줄러가 되면 프롬프트 변경이 인프라 변경이 된다

백엔드 선택을 모델에게 맡기는 구조의 이차 효과는 운영 쪽에서 나타난다.
지금까지 비용을 바꾸는 것은 인스턴스 크기나 오토스케일링 설정 같은 인프라 변수였다.
이 구조에서는 `exec` 도구 설명의 문장 하나, 시스템 프롬프트의 문단 하나, 모델 버전 하나가 컨테이너 호출 비율을 바꾸고, 그것이 곧 청구서를 바꾼다.

그래서 이 패키지를 운영하는 조직에는 새로운 종류의 회귀 테스트가 필요해진다.
기능이 맞게 동작하는지뿐 아니라, 같은 작업 묶음을 돌렸을 때 백엔드 선택 분포가 바뀌지 않았는지를 재야 한다.
모델을 한 버전 올렸는데 컨테이너 비율이 5%에서 30%로 뛰었다면 그것은 성능 문제가 아니라 비용 사고다.
블로그가 강조한 “모든 연산이 감사되고 관측된다”는 성질이 여기서 진짜 가치를 가진다.
감사 기록은 보안 도구이기 이전에, 모델의 스케줄링 판단을 사후에 검증하는 유일한 수단이 된다.

### isolate 베팅이 이기는 조건은 셸 호환성이 아니라 에이전트가 쓰는 도구의 수렴이다

just-bash가 bash를 완벽하게 흉내 낼 수는 없다.
그러나 isolate 쪽이 이기는 데 완벽한 호환이 필요하지는 않다.
필요한 것은 에이전트가 실제로 쓰는 명령의 분포가 좁게 수렴하는 것이다.

에이전트가 쓰는 셸은 사람이 쓰는 셸과 다르다.
`cat`, `ls`, `grep`, `sed`, `jq`, `curl`, 그리고 짧은 파이프라인이 대부분이고, 도구 호출 형식이 표준화될수록 이 분포는 더 좁아진다.
Worker shell이 `jq`, `yq`, `sqlite`, `python`, `html-to-markdown`을 선택 묶음으로 넣어 둔 것은 이 분포를 겨냥한 목록으로 읽힌다.
에이전트의 명령 분포가 수렴하면 isolate가 감당하는 비율은 저절로 올라가고, 10%라는 목표는 셸의 완성도보다 이 수렴 속도에 달려 있게 된다.

이 수렴은 되먹임을 만든다.
isolate에서 잘 도는 명령이 더 싸고 빠르므로, 하네스 설계자들은 에이전트가 그런 명령을 쓰도록 도구와 프롬프트를 다듬는다.
그러면 에이전트의 작업 방식 자체가 isolate에 맞춰 바뀐다.
플랫폼이 사용자의 행동을 자기 원가 구조에 맞게 조형하는 오래된 패턴이며, 서버리스가 애플리케이션 설계를 짧은 무상태 함수 쪽으로 밀었던 것과 같은 힘이다.

### 상태를 가진 쪽이 에이전트 시장의 계산을 가져간다

이 설계에서 가장 오래 남는 것은 실행 백엔드가 아니라 워크스페이스다.
실행은 isolate든 컨테이너든 브라우저든 바꿔 끼울 수 있지만, 권위 있는 상태는 Durable Object의 SQLite에 있다.
에이전트의 파일, git 기록, 작업 산출물이 한 곳에 쌓이면, 그 옆에서 계산을 돌리는 것이 가장 싸고 빠르다.

클라우드 시장에서 데이터 중력이 한 일을 에이전트 시장에서 상태 중력이 하게 된다.
저장된 데이터가 많은 곳으로 분석 작업이 따라갔듯, 에이전트의 작업 상태가 쌓인 곳으로 에이전트의 계산이 따라간다.
Cloudflare가 파일시스템을 먼저 만들고 실행은 끼워 쓰게 한 순서는, 이 중력을 자기 쪽에 두려는 선택으로 읽힌다.
경쟁 샌드박스 제품들이 실행 격리의 품질로 경쟁하는 동안, 이 패키지는 상태를 누가 들고 있느냐로 경쟁의 축을 옮기려 한다.

---

[^noman-land]: <https://news.ycombinator.com/item?id=49162385>

[^383toast]: <https://news.ycombinator.com/item?id=49161042>

[^AverageYoghurt]: <https://news.ycombinator.com/item?id=49172470>
