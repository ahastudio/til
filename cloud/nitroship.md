# Nitroship: 한국에서 시작해 Vercel 사용자를 겨냥한 웹 배포 플랫폼

<https://nitroship.co/>

<https://beta.nitroship.co/>

## 소개

Nitroship(나이트로쉽)은 코드를 올리면 빌드, 배포, 도메인 연결,
HTTPS 인증서까지 처리해 주는 웹 배포 플랫폼이다.
홈페이지 제목은 Web deployment from Korea이고,
한국어 페이지(`/ko`)는 한국에서 시작하는 웹 배포 플랫폼이라고 소개한다.
CLI 이름은 `ntro`이며, 프로젝트 폴더에서 `ntro deploy` 한 줄로 빌드와 배포가
끝난다는 것이 첫 화면의 약속이다.
배포마다 미리보기 주소가 따로 생기고, 확인한 뒤 프로덕션으로 올리는 Push,
Preview, Live 흐름을 내세운다.

지금은 Private Beta 단계다.
홈페이지의 신청 버튼은 `https://beta.nitroship.co`로 연결되는데,
이 주소는 Nitroship 서버가 HTTP `307`로 응답하며 Tally 설문 폼
<https://tally.so/r/44g9Xo>로 넘긴다.
즉 베타 사이트라는 별도 서비스가 있는 것이 아니라,
베타 주소 자체가 신청서의 짧은 입구 역할을 한다.
신청서를 내고 선정되면 개인 초대 링크를 이메일로 받아 가입하는 구조이며,
베타 기간에는 무료로 쓰고 기능이 자주 바뀔 수 있다고 안내한다.

운영 주체는 홈페이지 하단과 이용약관에 나온다.
상호는 삼삼오오, 대표는 엄다니엘, 사업자등록번호는 820-19-00672,
통신판매업 신고번호는 2023-서울강남-05840이고,
주소는 충청북도 청주시 청원구 향군로53번길 19다.
이용약관과 개인정보처리방침, 공정 이용 정책은 모두 2026년 10월 1일 시행이며,
영문판은 번역본이고 한국어판이 우선한다고 적혀 있다.
GitHub에는 같은 이름의 조직 `samsam-oo`가 있고,
2026년 9월 27일에 만든 공개 저장소 `samsam-oo/nitroship-examples`에 프레임워크별
예제 앱 40여 개와 Deploy on Nitroship 버튼이 정리되어 있다.

## 동작 방식

### 원격 빌더가 빌드 경로를 고른다

`ntro deploy`는 소스를 Nitroship의 원격 빌더로 올리고,
빌드가 끝나면 앱이 `https://<앱 이름>.ntro.run`에 뜬다.
홈페이지가 설정 파일 없이 배포된다고 말하는 근거는 문서의 감지 순서다.

| 순서 | 경로                | 고르는 조건                                                        | 배포되는 것                                    |
| ---- | ------------------- | ------------------------------------------------------------------ | ---------------------------------------------- |
| 1    | Dockerfile 컨테이너 | `build.dockerfile` 설정, 또는 `Dockerfile.nitroship`, `Dockerfile` | 컨테이너의 HTTP 서버와 CDN 정적 자산           |
| 2    | 관리형 Next.js      | `package.json`이 `next` 16.2 이상에 의존                           | 정적 페이지, SSR, ISR, API 라우트, 미들웨어 등 |
| 3    | 관리형 프레임워크   | 의존성이나 소스 파일로 프레임워크 식별                             | 프리셋이 빌드하고 패키징                       |
| 4    | 일반 정적 파일      | 루트 `index.html`, 또는 빌드 후 `dist`, `build`, `out` 폴더        | HTML, JS, CSS, 이미지와 리다이렉트, 헤더       |

`nitroship.json`에 `build.framework`를 적으면 자동 감지를 건너뛰고,
루트에 Dockerfile이 있어도 그 프리셋이 이긴다.
`build.framework`와 `build.dockerfile`을 함께 적으면 오류다.
프리셋의 결과물은 `static`, `node-server`, `container`,
`container-static` 네 가지 형태 중 하나다.
`container`는 프레임워크 언어에 맞는 Dockerfile을 생성해
비루트 OCI 이미지로 돌리고,
`container-static`은 Hugo, Jekyll, MkDocs처럼
컨테이너 도구로 정적 파일만 뽑아 CDN에 올린다.

지원 목록은 홈페이지에 적힌 16개보다 넓다.
문서의 `build.framework` 허용값에는 Next.js, Nuxt, SvelteKit, Astro, Remix,
React Router, SolidStart, TanStack Start, Analog, Angular, Qwik,
Gatsby, Docusaurus, VitePress, Eleventy, Hugo, Jekyll, MkDocs,
NestJS, Express, Fastify, Hono, Koa, Vite, Create React App,
Laravel, Symfony, WordPress, Rails, Django, Phoenix, FastAPI, Flask,
Spring Boot, .NET, Go, Rust, PHP가 들어 있다.
서버는 `0.0.0.0:$PORT`(기본 `3000`)에서 받아야 하고,
Go와 Rust는 `PORT`를 직접 읽어 바인딩해야 한다.

### 배포는 바뀌지 않고 주소가 움직인다

배포 하나는 한 시점의 빌드 결과이고, 만들어진 뒤에는 바뀌지 않는다.
프로덕션 주소는 지금 보여 줄 배포를 가리키는 화살표처럼 동작하며,
promote는 확인한 프리뷰로 화살표를 옮기고 rollback은 이전 배포로 되돌린다.
둘 다 다시 빌드하지 않는다.

| 주소          | 형식                               | 가리키는 대상                     |
| ------------- | ---------------------------------- | --------------------------------- |
| 프로덕션 URL  | `my-app.ntro.run`                  | 현재 프로덕션 배포                |
| 리비전 URL    | `my-app-<short-id>.rev.ntro.run`   | 그 배포 하나에 영구 고정          |
| 브랜치 URL    | `my-app-git-<branch>.rev.ntro.run` | 그 Git 브랜치의 최신 `ready` 배포 |
| 커스텀 도메인 | `www.example.com`                  | 현재 프로덕션 배포                |

앱의 첫 배포만 자동으로 프로덕션이 되고, 그 뒤의 기본값은 프리뷰다.
실수로 운영 사이트를 바꾸지 않게 하려는 설계다.
현재 프로덕션 배포와 최근 `ready` 배포 10개,
활성 브랜치 URL이 가리키는 배포는 항상 남고,
그보다 오래된 배포는 `pruned` 상태가 되어 열거나 되돌릴 수 없게 될 수 있다.

### 엣지와 컴퓨트, 그리고 인프라 파트너

홈페이지는 SSG, ISR, 정적 파일은 엣지에서,
SSR과 API는 한국과 미국 컴퓨트 리전에서 실행된다고 설명한다.
또 나라마다 현지 인프라 파트너와 함께하며 성능, 안정성,
비용을 하나하나 비교해 정했다고 하지만,
홈페이지에는 파트너 이름이 없다.
이름은 개인정보처리방침의 위탁과 국외 이전 항목에 나온다.

| 제공자                        | 맡은 일                                                  |
| ----------------------------- | -------------------------------------------------------- |
| 주식회사 디지털레이어         | 한국 리전 엣지 운영                                      |
| 프로젝트 엘리브(PROJECT ELIV) | 일본 리전 엣지 운영(국내 사업자, 서버는 일본)            |
| OVH US                        | 미국 리전 엣지 운영, 중앙 Control 클러스터 PostgreSQL DB |
| Backblaze B2(미국 서부)       | 배포 파일과 빌드 소스 객체 저장                          |
| Cloudflare                    | B2 객체를 읽고 캐시하는 CDN(앱의 일반 공개 진입점 아님)  |
| Amazon SES(서울 리전)         | 계정 인증, 초대, 청구 이메일 발송                        |
| Stripe, NicePay               | 해외 결제, 국내(KRW) 빌링키 결제                         |

처리방침은 엣지를 미국(OVH), 일본(PROJECT ELIV),
한국(Digital Layer)에서 운영하고 컴퓨트는 한국에서만 운영한다고 적는다.
한국 리전을 쓰더라도 계정과 서비스 기록은 미국의 중앙 Control DB에 저장되며,
이 이전을 거부하면 계정과 서비스 이용이 제한된다고 명시한다.
홈페이지의 한국·미국 컴퓨트 리전 문구,
베타 신청서의 현재 한국, 미국 서빙 제공 중이라는 문구와
처리방침의 컴퓨트는 한국에서만이라는 문구가 서로 다르다.
문서의 예시 리전 코드도 `kr-icn`(서울)이 대부분이고,
`us-pdx`(오리건)와 `de-fra`(프랑크푸르트)는
청구 단가를 설명하는 대목에 사이트 코드의 형식 예로만 나온다.
실제로 고를 수 있는 리전 목록은 `GET /v1/compute/options`가 알려 주지만,
이메일 인증을 마친 사용자만 호출할 수 있어 확인하지 못했다.

### Next.js는 스냅숏에서 깨어난다

관리형 Next.js는 `output: 'standalone'` 없이 정적 페이지, 프리렌더와 ISR,
서버 라우트, 미들웨어, 이미지 최적화가 동작한다고 한다.
트래픽이 늘 때 새 인스턴스를 빨리 띄우려고,
앱을 한 번 부팅한 상태를 시드 스냅숏으로 저장하고 거기서 복원한다.
새로 빌드한 Next.js 앱에는 `/__nitroship/health` 라우트가 붙는데,
`NextServer.prepare()`와 라우트 파일 사전 `import`가 끝날 때까지
`503`을 돌려준다.
스냅숏 직전에는 `User-Agent: nitroship-seed-warmup`,
`x-nitroship-warmup: 1` 헤더를 단 `GET /` 요청으로
홈페이지를 한 번 실제로 렌더링한다.
그래서 모듈 최상위에서 DB 연결을 여는 코드나,
미들웨어의 분석 기록 같은 부작용은 스냅숏 전에 실행된다.
Dockerfile 문서는 인스턴스가 0개까지 줄어들 수 있다고 적는다.

## 사용하기

### 설치와 첫 배포

CLI는 Linux와 macOS의 amd64, arm64만 지원한다.
설치 스크립트는 `https://nitroship.co/dl/`에서 `VERSION`, 아카이브,
`SHA256SUMS`를 받아 체크섬을 확인하고,
`/usr/local/bin`이 쓰기 가능하면 거기에,
아니면 `~/.local/bin`에 단일 실행 파일을 둔다.
이 문서를 쓰는 시점의 버전은 `v0.3.26`이었다.
아래 명령은 문서에서 옮긴 것이며, 가입이 초대제라 직접 실행해 보지는 않았다.

```bash
curl -fsSL https://nitroship.co/install.sh | bash
ntro login                      # 브라우저에서 일회용 코드를 승인
cd my-project
ntro apps create hello-site     # 앱 생성, 현재 폴더를 .nitroship/app.json으로 연결
ntro deploy . --prod            # 첫 배포는 어차피 프로덕션
ntro deploy                     # 두 번째부터는 기본이 프리뷰
ntro promote <short-id> --yes   # 확인한 프리뷰를 프로덕션으로
ntro rollback <short-id> --yes  # 이전 배포로 되돌리기
```

서버가 있는 앱은 컴퓨트 리전에 기본값이 없어서,
콘솔의 App Settings > Compute에서 고르거나 `nitroship.json`에 적어야 한다.
정적 사이트는 리전이 필요 없다.

```json
{
  "build": { "framework": "nuxt" },
  "compute": {
    "regions": ["kr-icn"],
    "tier": "standard",
    "minInstances": 0,
    "maxInstances": 4,
    "port": 3000
  },
  "crons": [
    { "path": "/api/cron?source=scheduled", "schedule": "0 5 * * *" }
  ]
}
```

컴퓨트 값은 필드마다 CLI 플래그(직접 업로드일 때만), `nitroship.json`,
콘솔 설정, 기본값 순으로 정해지고 빌드가 시작될 때 고정된다.
콘솔에서 값을 바꿔도 기존 배포는 그대로이며,
Apply now를 누르면 다시 빌드하지 않고 현재 프로덕션을 새 값으로 재배포한다.
다음 일반 배포에서는 `nitroship.json`의 값이 다시 콘솔 값을 덮는다.

빌드를 직접 하고 싶다면 `--local`(정적과 Node 서버 프리셋, Next.js만),
`--image sha256:<digest>`(직접 만든 OCI 이미지),
`--bundle-dir`과 `--entrypoint`(Node.js 번들) 경로가 있다.
`ntro registry login`은 Nitroship 레지스트리에 이미지를 올리는
Docker 로그인 명령을 출력만 한다.

### 환경 변수

환경 변수는 앱마다 `production`과 `preview` 두 대상에만 저장되고,
`development` 대상은 없다.
`ntro env add`는 값을 터미널에서 물어보며 기본이 비밀 값이고,
저장된 비밀 값은 다시 읽을 수 없다.
`ntro env pull`과 `ntro env run`은 평문 값만 가져온다.
배포는 만들어지는 순간의 환경 변수를 복사해 고정하므로,
값을 바꾸면 다시 배포해야 한다.
API의 `PUT /v1/apps/{appId}/env`는 목록 전체를 교체하므로 빠진 항목은 지워진다.
처리방침에 따르면 비밀 환경 변수는 OpenBao Transit으로 암호화해 저장하지만,
일반 환경 변수는 같은 수준의 암호화가 아닐 수 있다.

### Cron

Cron은 정해진 시간에 앱의 경로로 `GET` 요청을 보내는 기능이다.
시간대는 항상 UTC이고 다섯 필드 형식만 받으며,
`@daily` 같은 별칭과 `MON` 같은 이름은 지원하지 않는다.
앱당 최대 100개이고 현재 `ready` 프로덕션 배포에만 실행된다.
예정 시간에 실행하지 못한 회차는 건너뛰고 자동으로 재시도하지 않는다.
Cron 경로는 누구나 부를 수 있는 공개 주소이므로,
프로덕션 환경 변수에 `CRON_SECRET`을 넣고
`Authorization: Bearer` 헤더를 검사하라고 안내한다.
`nitroship.json`이나 `vercel.json`에 `crons`를 선언한 배포가 프로덕션이 되면,
콘솔에서 고친 목록을 다시 덮는다.

### 캐시 무효화

홈페이지의 캐시 관리는 두 층이다.
ISR과 프리렌더 페이지는 `ntro purge`가 세대 값을 올려,
다음 요청이 새 결과를 쓰게 한다.
공개 SSR 응답을 엣지에 저장하는 응답 캐시는 선택 기능이며,
운영자가 켜 주어야 동작한다고 문서가 적는다.
켜지면 `Nitroship-CDN-Cache-Control`, `CDN-Cache-Control`,
`Cache-Control` 중 먼저 있는 헤더 하나만 정책으로 쓰고,
`Nitroship-Cache-Tag`로 응답당 최대 128개의 태그를 붙일 수 있다.
`Set-Cookie`가 있거나 `Vary: Cookie`인 응답은 저장하지 않으며,
보존은 생성 후 최대 30일의 최선 노력이다.

```bash
ntro purge /docs/page --app my-app --wait          # 정확한 경로 하나
ntro purge --tag articles --tag article:42 --wait  # 태그(요청당 최대 16개)
ntro purge --tag article:42 --delete --wait        # 낡은 응답도 내보내지 않음
```

기본 모드인 invalidate는 해당 항목을 stale로 만들어,
백그라운드에서 다시 그리는 동안 옛 응답을 보낼 수 있고,
`--delete`는 다음 요청을 동기 렌더링하게 만든다.
어느 쪽도 저장된 정적 파일이나 CDN 파일을 실제로 지우지는 않으므로,
정적 파일을 바꾸려면 새로 배포해야 한다.

### 팀, API 토큰, Git 연동

모든 앱은 팀 하나에 속하고, 권한과 청구도 팀 단위다.
역할은 `owner`, `member`, `billing`, `viewer` 네 가지이며 `admin`은 없다.
초대는 `owner`만 보낼 수 있고 7일 뒤 만료된다.

CI에서는 콘솔에서 만든 `ntro_`로 시작하는 API 토큰을
`NITROSHIP_TOKEN` 환경 변수로 넘긴다.
토큰은 만들 때 한 번만 보이고, 만료는 없음 또는 1일에서 365일 사이로 고른다.
CLI는 API 토큰을 5분짜리 액세스 토큰으로 바꿔 쓰기 때문에,
토큰을 폐기해도 이미 받은 액세스 토큰은 최대 5분 동안 더 동작한다.

```yaml
- run: ntro deploy . --app my-app --prod
  env:
    NITROSHIP_TOKEN: ${{ secrets.NITROSHIP_TOKEN }}
```

GitHub App을 설치하면 비공개 저장소도 연결되고,
프로덕션 브랜치에 push하면 자동 배포된다.
다른 브랜치의 프리뷰 자동 배포는 기본으로 꺼져 있으며,
포함·제외 패턴으로 고를 수 있다.
GitHub App 없이 공개 저장소 주소만 연결하면 콘솔에서 수동으로만 배포한다.
모노레포는 루트 디렉터리를 `apps/web`처럼 지정한다.

### Vercel에서 옮기기

사이트에서 경쟁사를 직접 이름으로 부르는 대상은 Vercel뿐이다.
요금 페이지 FAQ는 Vercel 프로젝트를 옮길 수 있느냐는 질문에
Next.js 16.2 이상 프로젝트는 `ntro`로 배포할 수 있다고 답하고,
문서에는 Migrate from Vercel 가이드가 따로 있다.

`ntro`는 배포 루트의 `vercel.json`에서 `cleanUrls`, `trailingSlash`,
`redirects`, `rewrites`, `headers`, `routes`, `crons`, `version` 키만 읽는다.
`buildCommand`, `outputDirectory`, `framework`, `functions`, `regions`,
`images` 같은 Vercel 전용 키가 있으면 배포가 거부된다.
이런 설정은 `nitroship.json`의 `build`, `compute`, `images`로 옮겨야 하고,
두 파일이 다 있으면 `nitroship.json`만 읽는다.
명령은 `vercel deploy`가 `ntro deploy`, `vercel ls`가 `ntro ls`,
`vercel env pull`이 `ntro env pull`처럼 거의 일대일로 대응한다.
가이드 스스로도 동작이 Vercel과 똑같다고 가정하지 말고,
배포 뒤 주요 주소와 리다이렉트, API를 직접 열어 확인하라고 끝맺는다.

## 요금

요금 페이지의 제목은 요금은 모두 공개합니다이고, 1크레딧은 1달러로 정의된다.
원화 표시에서는 1크레딧이 ₩1,400이며, 문서는 이것이 실시간 환율이 아니라
운영자가 날짜별로 공시하는 고정 가격이라고 설명한다.
페이지에 실제로 보이는 요금제는 Free와 Enterprise(문의) 두 개다.

| 항목                 | Free 포함량 | 측정 대상                                |
| -------------------- | ----------- | ---------------------------------------- |
| Fast Data Transfer   | 100 GB      | 클라이언트와 엣지 사이의 양방향 트래픽   |
| Edge Requests        | 1,000,000건 | 앱에 귀속되는 공개 요청                  |
| Fast Origin Transfer | 10 GB       | 엣지와 컴퓨트, 외부 오리진 사이의 트래픽 |
| Active CPU           | 4 CPU-hr    | 실제로 쓴 CPU 시간                       |
| Provisioned Memory   | 360 GiB-hr  | 할당 메모리 곱하기 과금 시간             |
| Invocations          | 1,000,000회 | 컴퓨트로 들어간 호출 수                  |

Free는 팀원 추가 비용이 없고 동시 빌드는 1개다.
청구서가 없는 요금제라 초과분을 청구하지 않는 대신,
포함량을 넘으면 프로덕션 앱이 일시 중지될 수 있다.
공정 이용 정책은 상업용 앱도 Free에서 돌릴 수 있고,
상업적 용도라는 이유만으로 Pro가 필요하지는 않다고 적는다.

Pro는 아직 페이지 표에 나오지 않는다.
다만 요금 페이지에 실린 가격 데이터와 인증 없이 열리는 `GET /v1/pricing`
응답에는 2026년 10월 7일부터 유효한 `pro` 단가가 들어 있다.

| 지표(USD)                  | 한국(`kr`) | 일본(`jp`) | 그 밖(`*`) |
| -------------------------- | ---------- | ---------- | ---------- |
| Fast Data Transfer, GB     | 0.08       | 0.06       | 0.05       |
| Edge Requests, 1M          | 0.8        | 0.7        | 0.06       |
| Fast Origin Transfer, GB   | 0.06       | 0.05       | 0.02       |
| Active CPU, CPU-hr         | 0.16       | 0.16       | 0.128      |
| Provisioned Memory, GiB-hr | 0.015      | 0.015      | 0.01       |
| Invocations, 1M            | 0.6        | 0.6        | 0.6        |

한국과 일본의 단가가 기본 단가보다 비싸고, 특히 엣지 요청은 10배를 넘는다.
같은 데이터에는 정액 CDN 단계로 기본 제공(요청 100만 건, 1 TB)과
Tier 20($20, 요청 1,000만 건, 50 TB)이 있다.
문서 기준 Pro의 소스 업로드 한도는 1 GB로 Free의 100 MB보다 크고,
함수 요청과 응답 본문 4.5 MB, 함수 번들 250 MB는 같다.
베타 신청서에는 Nitroship Pro가 정식 출시 후 월 19,900원이고
그만큼의 사용 크레딧이 포함된다는 안내가 있지만,
요금 페이지에는 아직 그 숫자가 없다.

요금 페이지 아래에는 월 방문자 수에 따라
예상 Vercel 청구액과 예상 Nitroship 청구액을 나란히 보여 주는 계산기가 있다.
주석에 따르면 Vercel 가격은 2026년 9월 25일 기준 공식 가격표이고,
Pro 요금제는 Flat Rate CDN과 사용량 과금 중 싼 쪽을 쓰며,
데이터 전송과 요청만 비교하고 Fast Origin Transfer와 컴퓨트 요금은 뺐다.
방문자 1명당 요청 25건을 가정한다.
이 글을 쓰는 시점에는 계산기 영역에 요금 정보를 불러오지 못했다는 메시지만 보여,
실제 수치는 확인하지 못했다.

결제는 해외는 Stripe, 원화는 NicePay로 한다.
예산은 월 크레딧을 뺀 트래픽과 컴퓨트 사용액 기준이고, 50%, 75%,
100%에서 서명된 HTTPS 웹훅, Slack, Discord로 알림을 보낸다.
`pause_on_budget`을 켜면 100%에서 프로덕션을 멈추도록 요청하지만,
약관과 문서 모두 예산이 청구 총액의 하드캡은 아니라고 적는다.
이용약관은 유료 요금제의 프로덕션 호스트에 한해 월간 가용성 99%를 보장하고,
미달하면 플랫폼 요금의 10% 또는 25%를 서비스 크레딧으로 준다.
무료 요금제, 프리뷰 호스트, 베타 기능과 베타 API `/v1`은 보장 대상이 아니다.

## 베타 참여

베타 신청은 홈페이지의 Private Beta 신청하기 버튼,
또는 `https://beta.nitroship.co`를 열면 리다이렉트되는 Tally 폼
<https://tally.so/r/44g9Xo>에서 한다.
폼 제목은 Nitroship Closed Beta이고, 홈페이지는 3분 정도 걸린다고 안내한다.
폼은 다섯 쪽이다.

| 쪽            | 묻는 것                                                                                      |
| ------------- | -------------------------------------------------------------------------------------------- |
| About you     | 이름 또는 닉네임, 초대받을 이메일, GitHub ID(선택), 자기 소개(최대 3개), 소속(선택)          |
| How you build | 코딩 경험, 주로 쓰는 AI 코딩 도구, 주로 쓰는 기술, 지금 배포하는 곳, 배포에서 가장 불편한 점 |
| Your Project  | 배포할 앱, 프로젝트 단계, 예상 방문자 규모, 주요 사용자 국가, 기대 기능, 현재 월 배포 비용   |
| Feedback      | 베타 사용 빈도, 참여 방법(문제 제보, 설문, 30분 화상 인터뷰, 커뮤니티), 바라는 점            |
| Consent       | 만 14세 이상 확인, 개인정보 수집·이용 동의                                                   |

자기 소개 선택지는 개인 메이커와 사이드 프로젝트, 스타트업,
프리랜서와 에이전시, 기획자·디자이너·마케터, 학생이다.
코딩 경험은 AI와 함께 만드는 코딩 입문자부터 5년 이상까지 고르게 하고,
AI 코딩 도구로 Replit, Cursor, Bolt, Claude Code, ChatGPT Codex, v0, Windsurf,
GitHub Copilot을 나열한다.
현재 배포처 선택지는 Vercel, Netlify, Cloudflare Workers, Fly.io, Render,
Railway, Cloudtype, 직접 서버 운영이다.
정식 출시 후 월 19,900원이라면 계속 쓸 의향이 있는지도 묻는다.
수집한 정보는 베타 테스터 선정, 초대 링크 발송,
베타 관련 안내에 쓰고 베타 종료 후 3개월 이내에 파기한다고 적혀 있다.

선정 기준은 어디에도 명시되어 있지 않다.
폼은 신청 내용을 바탕으로 순차적으로 초대하고,
사이드 프로젝트로 먼저 시작해 보길 권한다고만 말한다.
질문 구성으로 보면 AI 코딩 도구로 만든 웹앱을 Vercel 같은 곳에 올려 본
한국 사용자, 그리고 피드백에 시간을 낼 수 있는 사람을 찾는 것으로 읽히지만,
이것은 해석이다.
폼 안내의 혜택 목록은 베타 기간 무료라고 하면서 괄호에 일부 유료라고 덧붙여,
홈페이지의 베타 기간 무료 이용 문구와 조금 다르다.
가입과 로그인은 초대 링크가 있어야 해서 콘솔 화면은 확인하지 못했다.

## 트레이드오프

### 한국에서 시작한다는 말이 가리키는 범위

Nitroship의 차별점은 한국에 가까운 배포다.
한국 엣지는 국내 회사인 디지털레이어가 운영하고,
원화 고정 크레딧 가격과 NicePay 결제, 한국어 문서와 약관이 갖추어져 있다.
국내 결제로 환율 걱정이 없다는 베타 폼의 문구도 같은 방향이다.

하지만 데이터가 한국에 머무는 정도는 경로마다 다르다.
요청을 받는 엣지와 처리방침상 컴퓨트는 한국에 있지만, 계정, 팀, 청구,
배포 메타데이터를 담는 중앙 Control DB는 미국 OVH에 있고,
배포 파일과 빌드 소스는 미국 서부의 Backblaze B2에 저장되어
Cloudflare를 거쳐 읽힌다.
한국 리전만 쓴다고 해서 소스 코드와 빌드 산출물이 국내에만 머무르는 것은 아니다.
국내 데이터 위치 요건이 있는 서비스라면 앞의 위탁 표를 먼저 보고 판단해야 한다.

반대로 미국 사용자를 위해 쓰려는 경우에는 컴퓨트 위치가 문제다.
홈페이지는 미국 컴퓨트 리전을 말하지만,
처리방침은 컴퓨트가 한국에서만 운영된다고 적는다.
처리방침을 기준으로 하면 미국 방문자의 SSR과 API 요청이
한국 컴퓨트까지 왕복할 수 있다는 해석이 가능하며,
어느 쪽이 현재 상태인지는 콘솔의 리전 목록으로 확인해야 한다.

### Vercel 호환은 주소 규칙까지다

Vercel에서 넘어오는 비용을 낮추는 장치는
명령 이름과 `vercel.json`의 라우팅 키 호환이다.
그러나 Vercel 함수 설정이나 Vercel 런타임 출력은 변환하지 않고,
알 수 없는 키가 있으면 배포 자체가 거부된다.
관리형 Next.js는 16.2 이상만 받으므로,
그보다 오래된 Next.js 앱은 먼저 업그레이드하거나 Dockerfile 경로로 가야 한다.
Next.js의 `i18n.domains`도 지원하지 않는다.
결국 호환은 옮기는 첫걸음을 줄여 줄 뿐이고,
가이드가 말하듯 동작 확인은 사용자 몫이다.

Netlify, Cloudflare Pages와의 비교는 사이트에 없다.
베타 폼이 현재 배포처로 Netlify와 Cloudflare Workers,
국내 PaaS인 Cloudtype을 선택지로 둔 것이 전부다.
Vercel과 같은 미리보기·프로모트 모델에 한국 엣지와 원화 결제를 얹은 것이
Nitroship의 자리라는 정리는 해석이다.
국내 PaaS 사례는 `cloud/cloudtype.md`,
끌어다 놓는 정적 배포는 `cloud/netlify-drop.md`,
Cloudflare의 정적 호스팅 진입은 `cloudflare/pages.md`,
지역에 묶인 정적 호스팅은 `cloud/statichost.md`,
직접 운영형 배포 플랫폼은 `devops/openship.md`에서 다룬다.

### 컴퓨트는 상태를 들고 있지 않는다

관리형 컨테이너 문서들은 모두 인스턴스 파일 시스템이 휘발성이고,
`/tmp`만 쓸 수 있다고 적는다.
업로드는 S3 같은 객체 저장소에, 데이터는 외부 DB에 두라고 하며,
마이그레이션, 큐 워커, 스케줄러는 자동으로 띄우지 않는다.
Nitroship 문서에는 관리형 DB나 저장소, 워커 기능이 없다.
그래서 Laravel이나 Rails, WordPress 같은 전통적인 앱을 올리려면,
DB와 세션 저장소, 업로드 저장소를 다른 곳에서 따로 마련해야 한다.
스케줄 작업은 Cron이 HTTP 경로를 부르는 방식으로만 대신할 수 있고,
실패한 회차는 재시도되지 않는다.

### 무료 포함량은 상한이기도 하다

Free는 초과 과금이 없는 대신 포함량을 넘으면 프로덕션이 멈출 수 있다.
갑자기 트래픽이 몰렸을 때 청구서 걱정은 없지만,
가장 방문자가 많은 순간에 사이트가 내려갈 수 있다는 뜻이다.
유료 요금제의 예산 정지도 집계 지연 때문에 하드캡이 아니므로,
비용 상한과 가용성 사이의 선택은 어느 요금제에서도 사라지지 않는다.

## 함정

- `ntro deploy`의 기본값은 첫 배포 뒤 프리뷰다. CI에서 프로덕션에 올리려면 매번 `--prod`를 붙여야 한다.
- 서버가 있는 앱은 컴퓨트 리전에 기본값이 없다. `nitroship.json`에 `compute.regions`가 없으면 콘솔에서 따로 정해야 한다.
- `ntro deploy ./dist`는 `./dist` 폴더의 앱 연결을 읽으므로, 프로젝트 루트에서 하위 폴더를 배포할 때는 `--app`이 필요하다.
- 환경 변수와 컴퓨트 설정은 배포 시점에 고정된다. 값을 바꾼 뒤 다시 배포하지 않으면 운영에 반영되지 않는다.
- 앱 슬러그를 바꾸면 이전 `ntro.run` 주소와 리비전, 브랜치 URL이 즉시 끊긴다.
- Cron 시간대는 UTC다. 한국 시간 오전 5시는 `0 20 * * *`이다.
- 응답 캐시는 운영자가 켜야 동작한다. 헤더만 넣고 캐시가 된다고 가정하면 안 된다.
- 문서의 `ntro logs`는 빌드와 배포 이벤트이지 앱의 요청 로그가 아니다. 공개 문서에서 런타임 로그 조회 기능은 찾지 못했다.
- npm의 `ntro` 패키지는 Nitroship과 무관한 TypeScript 설정 도구다. CLI는 npm이 아니라 `nitroship.co/dl`의 Go 바이너리로 배포된다.
- CLI 바이너리 메타데이터는 모듈 경로를 `github.com/samsam-oo/nitroship/apps/cli`로 적고 있지만, 이 저장소는 GitHub API에서 404를 돌려주어 공개되어 있지 않다.
- 설치 스크립트의 체크섬은 바이너리와 같은 서버에서 받는다. 전송 중 손상은 잡지만, 서버 자체가 바뀐 경우까지 막는 서명은 아니다(해석).
- `/v1` API는 베타라 호환 별칭 없이 바뀔 수 있다고 약관과 문서가 모두 밝힌다. 이 API로 자동화를 짜면 변경 공지를 따라가야 한다.

## 기억할 원칙

### 지역 서비스의 로컬은 데이터 경로마다 따로 확인한다

어떤 클라우드 서비스가 한국 리전을 내세울 때,
그 말은 대개 방문자 요청이 처리되는 곳을 가리킨다.
Nitroship도 엣지와 컴퓨트는 한국에 두었지만,
계정 DB와 배포 파일 저장소는 미국에 둔다.
작은 팀이 검증된 저장소와 DB 호스팅을 빌려 쓰는 합리적인 구성으로 보이지만,
사용자 입장에서 한국 서비스라는 인상과 실제 데이터 위치는 다를 수 있다.
배포 플랫폼을 고를 때는 홈페이지 문구보다
개인정보처리방침의 위탁과 국외 이전 표를 먼저 읽는 편이 정확하다.
