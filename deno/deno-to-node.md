# Deno와 결별하고 Node로 돌아가다: Node는 따라잡았고 Deno는 멈췄다

원문: [Friendship ended with Deno, now Node is my best friend – David Bushell – Web Dev (UK)](https://dbushell.com/2026/10/03/deno-to-node/)

HN 토론: <https://news.ycombinator.com/item?id=49971719> (322점, 251개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/a9kwzv/friendship_ended_with_deno_now_node_is_my> (59점, 49개 댓글)

GN 토론: <https://news.hada.io/topic?id=34851>

## 요약

영국 웹 개발자 David Bushell이 2026년 10월 3일에 쓴 글이다.
제목은 “Friendship ended with Mudasir” 밈을 빌렸다.
그는 이번 달 SvelteKit 클라이언트 프로젝트에서 Node를 많이 쓰다가
Node가 언제 이렇게 좋아졌느냐고 놀란다.
Deno를 오래 기본 런타임으로 써 온 탓에 Node 쓰는 법을 잊었을 정도인데,
돌아와 보니 최신 ECMAScript 문법이 다 지원되고 예전의 불편한 API는 교체되거나
현대화되어 있었고, 무엇보다 `require()`를 볼 일이 없어졌다고 말한다.

### 패키지 관리

Node 공식 다운로드 페이지는 NVM을 설치하려고 인터넷의 스크립트를 bash로 바로
파이프하라고 권한다.
그는 NVM과 NPM에 대한 오래된 경험이 좋지 않아
버전 전환에는 Fast Node Manager(FNM)를, 패키지 매니저로는 PNPM을 골랐다.
NPM의 “M”은 malware의 약자라고 비꼬면서,
`npm`과 `npx`를 `pnpm`과 `pnpx`의 별칭으로 걸어 두었다.
처음에는 바이너리 이름이 고정된 스크립트 때문이라고 적었다가,
나중에 심볼릭 링크를 썼던 때와 혼동했을 수 있다고 고쳐 적고
설치 안내문의 명령을 복사할 때 도움이 된다고 덧붙였다.

PNPM이 post-install 스크립트를 막는 점도 장점으로 꼽고,
`pnpm-workspace.yaml`에 악성 업데이트를 늦추는 설정 두 줄을 더했다.

```yaml
minimumReleaseAge: 1440
trustPolicy: no-downgrade
```

처음에는 Microsoft가 신고된 악성코드를 지우는 데 적어도 한 달이 걸린다는
이유로 최소 릴리스 경과 시간을 한 달로 잡았지만,
PNPM이 맞는 의존성 버전을 찾지 못해 하루로 줄였다.
다음 Shai-Hulud를 다른 누군가가 먼저 시험해 줄 만큼의 시간이라는 설명이다.

### TypeScript

Node는 이제 TypeScript를 직접 실행하지만 `node_modules` 아래의 파일은 타입을
지우지 않고 `ERR_UNSUPPORTED_NODE_MODULES_TYPE_STRIPPING` 오류를 낸다.
Node.js v26.10.0 문서는 이 제한이 패키지 작성자가 TypeScript로 쓴 패키지를
배포하지 못하게 하려는 것이라고 밝힌다.
저자는 이를 기술이 아니라 철학의 문제로 읽는다.
TypeScript는 Microsoft 제품이고 그 문을 열면 생태계 전체가 오염되며
아무도 Microsoft를 더 원하지 않는다는 것이다.
ECMAScript에 가벼운 네이티브 타입이 들어오길 바라지만
타입 주석 제안은 자신이 은퇴하기 전에는 결실을 맺지 못할 것 같다고 본다.

결국 패키지 번들링에 Tsdown을 썼고 dotfile이 두 개 늘었다.
GitHub을 떠나 자체 호스팅한 Forgejo 인스턴스로 옮긴 탓에 NPM의 제한으로
패키지의 provenance를 잃었고,
자기 패키지를 허용하도록 PNPM 신뢰 정책을 따로 설정해야 했다.

### 사이트 이전

마지막 시험은 Deno로 만든 자신의 정적 사이트 생성기를 Node v26.10.0으로 옮기는
일이었다.
필요한 변경은 Deno의 파일 시스템 API를 `node:fs`로 바꾸고,
`Deno.serve`를 `node:http`를 감싼 Hono의 Node 어댑터로 바꾸는 것뿐이었다.
이 최소한의 이전만으로 빌드가 15% 빨라졌다.
코드는 여전히 Deno식이라 Node 내장 API를 더 쓰면 성능이 더 나올 것이라고
짐작하지만 아직 확인하지는 않았다.
이후 Deno의 `@std/path`도 `node:path`로 import만 바꿨다.

### Deno의 쇠퇴

글 끝에 일부러 묻어 둔 부분이다.
그는 Deno가 실리콘밸리식 성공 기준을 받아들이면서 혁신적인 런타임에서
매력 없는 제품을 파는 지루한 스타트업이 되었다고 말한다.
직원 절반이 해고되었고 남은 사람들은 AI 환상을 트윗하며
“Temu Cloudflare”를 바이브 코딩하고 있다고 쏘아붙인다.
Deno Land Inc.는 수년 전에 런타임 혁신을 멈췄고 Node가 꾸준히 따라와
몇몇 영역에서는 앞질렀으므로 오늘 Deno 런타임을 쓸 이유가 없다는 결론이다.

마지막으로 등을 떠민 것은 세 가지였다.
몇 주 동안 깨져 있던 ZSH 통합, JSR의 공격적인
“429 (Too Many Requests)” 응답, 동시 HTTP 요청에서 Deno가 멈추는 버그다.
그는 JSR 계정 삭제를 요청했고 지원팀은 빠르게 처리했다.
패키지는 더 보이지 않지만 예전 버전은 여전히 설치할 수 있다.
글은 `brew uninstall deno`로 끝난다.

## 분석

### 비교의 단위는 런타임이 아니라 저자의 작업 흐름이다

글은 Node와 Deno를 비교하는 형식을 띠지만 실제로 비교되는 것은 한 사람의
작업 흐름이다.
측정된 수치는 정적 사이트 생성기 빌드가 15% 빨라졌다는 것 하나뿐이고,
Deno를 떠난 이유 세 가지도 재현 조건이 없는 개인 경험이다.
Lobste.rs의 matthiasportzel은 다른 워크로드에서는 Deno가 더 빠르다는 예를
들며, ZSH 통합이 무엇이었는지도 모르겠고 버그를 언급만 해서는
흥미롭지 않다고 지적했다.[^matthiasportzel]
HN의 polatronics도 Node가 Deno를 앞지른 곳이 있다면 예를 들어 달라고
요구했다.[^polatronics]

그래서 이 글이 증명하는 것은 “Node가 Deno보다 낫다”가 아니라
“Deno 전용 API를 조금만 쓴 코드는 이제 Node로 쉽게 옮겨진다”이다.
이전 범위가 `Deno.serve`, 파일 시스템 API, `@std/path` 세 곳이었다는 사실이
이를 보여 준다.
HN의 chrysoprace는 Deno 고유 API를 쓰는 순간 앱이 “Deno 앱”이 되어 생태계가
둘로 나뉘고, 이식성을 원하면 결국 Node API를 써야 해서 Deno의 가치가 깎인다고
썼다.[^chrysoprace]
저자의 이전이 쉬웠던 것은 그가 이미 그 경계 가까이에 서 있었기 때문이다.

### 호환성 전략은 떠나는 비용을 낮춘다

Lobste.rs의 hongminhee는 `npm:` 지정자, `node_modules`, `node:*` 모듈처럼
Node 호환으로 가는 걸음마다 라이브러리 작성자가
Deno를 겨냥할 이유가 하나씩 줄어든다며,
Windows 호환이 OS/2에 그랬던 것과 같다고 비유했다.[^hongminhee]
동시에 Node는 네이티브 TypeScript, 권한 모델, `fetch()` 같은 Deno의 아이디어를
가져갔다고 덧붙였다.

이 글은 그 구조가 사용자 한 명의 차원에서 어떻게 작동하는지 보여 주는 사례다.
들어오는 비용을 낮추는 호환 계층은 나가는 비용도 똑같이 낮춘다.
GN의 click은 Bun을 쓰다 Node로 돌아갔다며,
모든 런타임이 Node 호환을 주장하지만 제논의 역설처럼 100%에는 닿지 못하고
그사이 다른 런타임이 내세운 가치가 Node에 대부분 구현되는 것을 보고
굳이 필요 없다고 느꼈다고 적었다.[^click]
Lobste.rs의 gcollazo도 Bun 프로젝트를 처음부터 “비상시 Node로 이전” 가능하게
설계해 두었다가 실제로 옮겼다고 말했다.[^gcollazo]
대안 런타임의 사용자 상당수가 Node를 탈출구로 계속 쥐고 있다는 뜻이다.

### 공급망 방어가 런타임 선택의 축이 되었다

글에서 가장 구체적인 부분은 성능도 문법도 아닌 패키지 관리다.
FNM, PNPM, 별칭, `minimumReleaseAge`, `trustPolicy`까지
설정의 대부분이 악성 패키지를 피하려는 장치다.
Shai-Hulud 같은 웜이 반복된 npm 생태계에서 런타임을 고르는 일은
곧 설치 시점의 위협 모델을 고르는 일이 되었다는 것이 이 노트의 해석이다.

HN과 Lobste.rs에서 Deno를 변호하는 댓글도 같은 축에 서 있다.
HN의 benburton은 Deno의 네트워크 수준 차단처럼 주소 허용 목록을 기본으로 두는
런타임을 다른 데서 본 적이 없고, 에이전트 시대에는 그게 기본 조건이어야 한다고
썼다.[^benburton]
Lobste.rs의 KevinMGranger는 Node가 Deno의 권한 시스템을 들이지 않는 한
옮길 이유가 없다고 했다.[^KevinMGranger]
런타임 논쟁의 중심이 실행 속도에서 무엇을 막아 주느냐로 옮겨 가고 있다.

### TypeScript 제한을 둘러싼 오독

저자는 `node_modules` 안의 타입 제거 금지를 Microsoft에 대한 거부로 읽었지만,
HN의 Naitronbomb은 이유가 다르다고 반박했다.[^Naitronbomb]
라이브러리가 쓴 tsconfig 설정이 내 프로젝트와 같다는 보장이 없어,
타입 검사를 하면 라이브러리 코드 안에서 오류가 날 수 있다는 것이다.
그는 번들러 없이도 TypeScript 컴파일러의 선언 파일 생성으로 충분하며,
그 방식은 순수 JavaScript 사용자를 배제하지 않는 장점도 있다고 덧붙였다.

HN의 WorldMaker는 Node의 타입 제거 방식이 Deno나 Bun보다 가장 엄격해서
isolated modules와 erasable syntax only를 켜야 하고 enum과 namespace를 쓸 수
없다고 설명했다.[^WorldMaker]
이는 TC39 타입 주석 제안이 요구하는 엄격함과 같은 방향이다.
저자가 바란 “ECMAScript의 가벼운 네이티브 타입”과 Node의 제한은 사실 같은 쪽을
보고 있는 셈이다.

## 비평

### “Deno는 혁신을 멈췄다”는 주장은 석 달 전 릴리스와 부딪힌다

저자는 Deno Land Inc.가 수년 전에 런타임 혁신을 멈췄다고 단정한다.
하지만 2026년 6월 25일에 나온 Deno 2.9는 `deno desktop`으로 데스크톱 앱
빌드를 내놓았고, 콜드 기동 시간을 절반으로 줄였다(`deno/deno-2.9.md`).
HN의 jerleth는 바로 그 데스크톱 앱 지원 때문에 Deno를 쓰기 시작했다고
반문했다.[^jerleth]
혁신의 기준을 무엇으로 잡느냐에 따라 평가는 달라질 수 있지만,
글은 그 기준을 밝히지 않은 채 결론만 내린다.

더 아이러니한 것은 공급망 설정이다.
Deno 2.9 릴리스 노트에 따르면 Deno는 24시간 최소 의존성 나이를 기본으로
켜고, 탈취된 메인테이너 토큰 공격을 막는 no-downgrade 신뢰 정책을 선택 사항으로
더했다.
저자가 PNPM에서 손으로 넣은 `minimumReleaseAge: 1440`과
`trustPolicy: no-downgrade`와 같은 내용이다.
저자는 Deno를 떠나면서 Deno가 이미 주던 방어를 PNPM 설정으로 다시 만든 셈이다.
글에는 이 대응 관계가 한 번도 등장하지 않는다.

같은 맥락에서 HN의 dzonga는 “Temu Cloudflare”라는 조롱이 공정하지 않다며,
Deno 팀이 셀프 호스팅 가능한 오픈소스 워커 플랫폼 cell-d에 들이는 작업을
들었다.[^dzonga]
회사의 방향을 비판하는 것과 엔지니어링 결과물을 깎아내리는 것은 다른 일이다.

### 저자가 Node 쪽에 적용한 기준은 Deno 쪽과 다르다

Deno에 대해서는 몇 주간의 ZSH 버그 하나로도 떠날 이유가 된다.
그런데 Node 쪽에서는 공식 문서가 권하는 NVM 대신 FNM을 고르고,
NPM을 피하려고 PNPM을 깔고, 별칭을 걸고, 공급망 설정 두 줄을
넣고, TypeScript 패키지를 위해 Tsdown과 dotfile 두 개를 더하고,
Forgejo 때문에 신뢰 정책 예외까지 만든다.
글이 나열한 Node의 마찰이 Deno의 마찰보다 적다고 보기는 어렵다.

저자는 이 비대칭을 dotfile 두 개가 늘었어도 `deno.json`을 지웠으니 본전이라는
식으로 넘긴다.
Lobste.rs의 bakkot은 npm 12가 lifecycle 스크립트를 기본으로 끄지만 Node 26에
포함되기에는 늦게 나와 직접 업그레이드해야 한다고 짚었다.[^bakkot]
즉 저자가 PNPM으로 얻은 보호는 Node의 기본값이 아니라 저자가 쌓은 설정이다.
“Node가 좋아졌다”는 결론은 이 설정을 감당할 줄 아는 사람에게만 성립한다.

### 기술 판단과 감정이 같은 글 안에서 섞인다

TypeScript 제한을 “Microsoft 제품이라서”로 설명하는 대목은
글 전체의 신뢰도를 깎는다.
Lobste.rs의 wrs는 NPM 역시 Microsoft 제품이라고 짧게 꼬집었고,[^wrs]
HN의 gwbas1c은 바로 이 대목에서 저자가 신뢰를 잃었다고 적었다.[^gwbas1c]
Node가 TypeScript를 직접 실행하게 된 것 자체가 TypeScript의 영향력을 받아들인
결과라는 점에서, Microsoft를 피하려 Node로 간다는 서사는 앞뒤가 맞지 않는다.

저자는 Deno 쇠퇴 부분을 “죽은 말에 채찍질”이라며 일부러 글 끝에 두었다고
말한다.
그러나 글의 결론인 “Deno 런타임을 쓸 이유가 없다”는 바로 그 부분에서 나온다.
HN의 steve_adams_86은 Deno 팀의 소통 부족은 걱정되지만 이 글은 오히려 Deno가
무엇을 주는지에 대한 저자의 인식 부족을 보여 준다고 평했다.[^steve_adams_86]
기술 비교로 읽히길 원하는 부분과 감정을 정리하는 부분이 분리되지 않아
어느 쪽도 충분히 설득하지 못한다.

### 사소한 설정 설명에도 부정확함이 있다

Lobste.rs의 shdown은 bash 별칭이 대화형 셸이 아닌 스크립트 안에서는 동작하지
않는다고 지적했다.[^shdown]
저자는 댓글로 심볼릭 링크를 쓰던 때와 혼동했을 수 있다고 답했고,[^dbushell]
본문에도 정정 메모를 달았다.
고친 것은 좋지만, 바이너리 이름이 고정된 스크립트를 위해서라는 원래 근거는
틀렸고 남은 이점은 설치 안내문 복사 정도다.

Lobste.rs의 lilac은 curl-bash 비판에 대해, 어차피 인터넷에서 받은 임의 코드를
실행할 것인데 첫 조각이 셸 스크립트인 게 왜 문제냐고 물었다.[^lilac]
보안 서사가 글의 큰 줄기인 만큼 이런 대목의 부정확함은 전체 논지를
약하게 만든다.

## 인사이트

### 런타임의 차별점은 결국 기본값으로 수렴한다

Node가 따라잡은 것은 기능 목록이고, 아직 남은 격차는 기본값이다.
ESM, `fetch`, `node:test`, TypeScript 실행, 권한 모델이 차례로 들어왔고,
Lobste.rs의 bakkot은 `util.parseArgs`, `util.styleText`, `--env-file`, glob,
sqlite까지 들며 대부분의 앱은 의존성이 거의 필요 없다고 했다.[^bakkot]
Deno 쪽에서 남은 차별점은 HN의 notnullorvoid가 꼽은 것처럼
워크스페이스 패키지의 무컴파일 의존, 권한 모델, 네이티브 WebGPU, 내장 린터와
벤치마크 같은 것들이다.[^notnullorvoid]

이 목록의 공통점은 대부분 “설정 없이 켜져 있는 것”이라는 점이다.
Node에도 권한 모델과 테스트 러너는 있지만 켜고 맞추는 일이 사용자 몫이다.
저자의 PNPM 설정이 보여 주듯, 같은 기능이라도 기본으로 켜져 있느냐 아니냐가
실사용 경험을 가른다.
앞으로 대안 런타임이 살아남을 자리는 새 API가 아니라
“아무것도 하지 않았을 때 안전한가”라는 질문에 있을 가능성이 크다.

### 대안 런타임의 진짜 경쟁자는 LLM의 기본 선택이다

HN의 theturtletalks는 Deno가 잘못된 선택은 아니지만 LLM이 Deno를 먼저
고르지 않는다는 점이 지금 큰 타격이라고 썼다.[^theturtletalks]
반론도 많았지만, 코드를 직접 쓰는 비중이 줄어들수록 런타임 선택은
사람의 취향보다 에이전트의 기본값을 따라가게 된다.
학습 데이터에서 압도적인 Node는 이 구도에서 가만히 있어도 유리하다.

이 문단부터는 해석이지만, 저자의 이번 결정도 같은 흐름 위에 있다.
그는 클라이언트 프로젝트에서 Node를 쓰다가 익숙해졌다.
대안 런타임은 개인이 의식적으로 고르는 도구였는데,
팀과 클라이언트와 에이전트가 기본값을 정하는 환경에서는
의식적인 선택의 기회 자체가 줄어든다.
Deno가 2.9에서 npm·pnpm·yarn·Bun 락파일을 그대로 읽는 이주 도구를 낸 것도
이 기본값의 중력을 거스르지 않으려는 시도로 볼 수 있다.

### 회사에 대한 신뢰가 런타임 신뢰를 대신하게 되었다

저자가 Deno를 떠나는 이유의 절반은 기술이 아니라 회사다.
정리해고, AI 중심 메시지, 소통 부재가 그것이다.
Deno 표준 라이브러리 v1 작업에 계약자로 참여했던 HN의 isyouaint도
정리해고 이후 로드맵도 소통도 보이지 않아 서서히 잊혀 가는 것 같다고
안타까워했다.[^isyouaint]
저자는 2025년 9월 노트에서 Bun을 쓰지 않는 이유도 기술이 아니라 창업자의
정치적 연결로 설명한 적이 있다.

벤처 자금으로 만든 런타임은 이제 기술만이 아니라 회사의 지배 구조와
의사소통까지 함께 평가받는다.
이것은 해석이지만, Node가 유리한 것은 더 빨라서가 아니라 특정 회사의 런웨이에
묶여 있지 않기 때문이다.
hongminhee가 제품 결정과 런웨이 결정을 밖에서는 구분할 수 없다고 한 말이
이 불안을 정확히 담는다.
대안 런타임이 신뢰를 되찾으려면 기능보다 로드맵 공개와 거버넌스가 먼저일 수
있다.

### 이전이 쉬웠다는 사실이 가장 중요한 결과다

이 글에서 오래 남을 정보는 Deno에 대한 불만이 아니라
`Deno.serve`와 파일 시스템 API만 바꾸면 사이트 생성기가 Node에서 돌았다는
사실이다.
Lobste.rs의 Johz는 런타임을 바꿀 때의 어려움이 API 차이와 동작 차이 두 가지인데,
표준 Node 모듈을 기준으로 삼고 이상한 일을 하지 않으면 API 문제는 거의 없다고
설명했다.[^Johz]
대신 `setTimeout`과 `process.nextTick` 같은 비동기 함수의 실행 순서처럼
엔진마다 다른 세부 동작이 복잡한 앱에서 문제를 만든다고 덧붙였다.

실무 원칙으로 옮기면, 어떤 런타임을 쓰든 고유 API는 얇은 어댑터 뒤에 두고
웹 표준과 `node:*` 모듈을 기본으로 쓰는 편이 낫다.
저자가 Hono를 써서 서버 부분을 어댑터 교체로 끝낸 것이 좋은 예다.
gcollazo의 “비상시 Node로 이전” 설계와 같은 생각이며,
런타임 회사의 운명이 불확실한 시기에는 이 탈출구 자체가 가장 값싼 보험이다.

---

[^matthiasportzel]: <https://lobste.rs/s/a9kwzv/friendship_ended_with_deno_now_node_is_my#c_jwzniz>

[^polatronics]: <https://news.ycombinator.com/item?id=49980380>

[^chrysoprace]: <https://news.ycombinator.com/item?id=49972856>

[^hongminhee]: <https://lobste.rs/s/a9kwzv/friendship_ended_with_deno_now_node_is_my#c_lzvngk>

[^click]: <https://news.hada.io/topic?id=34851#cid67023>

[^gcollazo]: <https://lobste.rs/s/a9kwzv/friendship_ended_with_deno_now_node_is_my#c_lfeqxh>

[^benburton]: <https://news.ycombinator.com/item?id=49975003>

[^KevinMGranger]: <https://lobste.rs/s/a9kwzv/friendship_ended_with_deno_now_node_is_my#c_wgtd9e>

[^Naitronbomb]: <https://news.ycombinator.com/item?id=49973527>

[^WorldMaker]: <https://news.ycombinator.com/item?id=49983061>

[^jerleth]: <https://news.ycombinator.com/item?id=49974443>

[^dzonga]: <https://news.ycombinator.com/item?id=49977056>

[^bakkot]: <https://lobste.rs/s/a9kwzv/friendship_ended_with_deno_now_node_is_my#c_y14ixs>

[^wrs]: <https://lobste.rs/s/a9kwzv/friendship_ended_with_deno_now_node_is_my#c_ckbytg>

[^gwbas1c]: <https://news.ycombinator.com/item?id=49978535>

[^steve_adams_86]: <https://news.ycombinator.com/item?id=49981915>

[^shdown]: <https://lobste.rs/s/a9kwzv/friendship_ended_with_deno_now_node_is_my#c_9kva70>

[^dbushell]: <https://lobste.rs/s/a9kwzv/friendship_ended_with_deno_now_node_is_my#c_qgsdp0>

[^lilac]: <https://lobste.rs/s/a9kwzv/friendship_ended_with_deno_now_node_is_my#c_ublqv1>

[^notnullorvoid]: <https://news.ycombinator.com/item?id=49977141>

[^theturtletalks]: <https://news.ycombinator.com/item?id=49973419>

[^isyouaint]: <https://news.ycombinator.com/item?id=49973086>

[^Johz]: <https://lobste.rs/s/a9kwzv/friendship_ended_with_deno_now_node_is_my#c_hb7ew6>
