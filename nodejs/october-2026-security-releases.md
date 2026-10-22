# Node.js 2026년 10월 보안 릴리스: 호스트 이름 검증 우회와 Brotli 원격 코드 실행을 고친 세 라인

원문: [Node.js — Wednesday, October 21, 2026 Security Releases](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases)

HN 토론: <https://news.ycombinator.com/item?id=50177438> (11점, 0개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/gu7bow/node_js_wednesday_october_21_2026> (7점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=35798>

## 지금 해야 할 일

### 무엇이 위험한가

26.x, 24.x, 22.x를 쓰는 모든 서비스가 대상이다.
공지가 High로 분류한 취약점은 네 건이고, 성격은 두 가지다.

하나는 TLS 호스트 이름 검증 우회다.
IP 주소를 전각 숫자로 쓰거나 느슨하게 해석되는 형태로 쓰면, 인증서가 그 호스트의 것인지 확인하는 단계를 통과할 수 있다는 내용이다.
Node.js 프로세스가 외부 서버를 호출하는 쪽(HTTPS 클라이언트, 서버 간 API 호출)이라면 연결 상대가 진짜인지 믿을 수 없게 된다.
공격자가 통신 경로에 들어갈 수 있어야 하는 것이 이런 우회의 일반적인 조건이지만, 공지는 구체적인 조건을 밝히지 않는다.

다른 하나는 Brotli 디코더의 범위 밖 쓰기다.
공지는 이것이 원격 코드 실행을 허용한다고 적는다.
Brotli로 압축된 데이터를 푸는 코드가 있는 서비스가 우선 점검 대상인데, 어떤 경로로 입력이 도달해야 악용되는지는 공지에 없다.

나머지 High 한 건은 `dns.resolve`가 NUL 문자가 든 이름을 잘라 내는 문제다.
사용자 입력을 그대로 DNS 조회에 넘기는 코드에서 검증을 통과한 이름과 실제로 조회되는 이름이 달라질 수 있다.
이 동작은 수정되지 않은 24.11.0에서 직접 재현했다.

### 오늘 할 일

아래는 우선순위 순서다.
우선순위는 이 글의 판단이며 공지가 정한 것이 아니다.

1. 실행 중인 버전을 확인한다. `node -p "process.version"`의 결과가 아래 표의 수정 버전보다 낮으면 대상이다.
2. 수정 버전으로 올린다. 26.x는 26.12.1, 24.x는 24.22.1, 22.x는 22.23.4다.
3. 올린 뒤 프로세스를 모두 재시작한다. 실행 중인 프로세스는 이전 런타임을 계속 쓴다.
4. 컨테이너로 배포한다면 이미지를 다시 빌드하고, 이미지 안에서 `process.version`을 확인한다.
5. 지원이 끝난 라인을 쓰고 있다면 지원되는 라인으로 올린다. 공지는 지원이 끝난 버전이 보안 릴리스에 항상 영향받는다고 밝힌다.
6. 외부 입력을 받는 서버와 외부 서버를 HTTPS로 호출하는 서비스부터 먼저 올린다.
7. 26.x로 올린다면 ES 모듈 로딩에 의존하는 코드를 배포 전에 테스트한다. 26.12.1에는 보안 수정과 별개로 ES 모듈 로딩 변경을 되돌리는 커밋이 들어 있다.
8. SEA(단일 실행 파일)나 시작 스냅샷을 배포한다면 새 버전으로 다시 만든다.
9. 마지막으로 이 글의 `확인하기` 절 스크립트를 돌려 버전이 맞는지 확인한다.

| 사용 중인 라인 | 올릴 버전 |
| -------------- | --------- |
| 26.x           | 26.12.1   |
| 24.x           | 24.22.1   |
| 22.x           | 22.23.4   |

임시 완화책은 공지에 없다.
공지는 업데이트 외의 방어 수단을 제시하지 않으므로, 당장 올릴 수 없다면 위험을 안은 채 일정을 정해야 한다.

## 요약

Node.js 프로젝트가 2026년 10월 21일에 26.x, 24.x, 22.x 세 릴리스 라인의 보안 릴리스를 냈다.
수정 버전은 26.12.1, 24.22.1, 22.23.4이고, 가장 높은 심각도는 High다.
공지는 취약점 10건을 심각도별로 나열한다.
High가 4건, Medium이 3건, Low가 3건이다.

| CVE               | 심각도 | 영향받는 라인    | 공지의 제목                                                                                               |
| ----------------- | ------ | ---------------- | --------------------------------------------------------------------------------------------------------- |
| `CVE-2026-105482` | High   | 26.x, 24.x, 22.x | `dns.resolve`가 NUL 문자가 든 이름을 잘라 낸다                                                            |
| `CVE-2026-105483` | High   | 26.x, 24.x       | IP가 전각 숫자로 쓰이면 TLS 인증서 호스트 이름 검증을 우회한다                                            |
| `CVE-2026-106069` | High   | 26.x, 24.x, 22.x | 호스트가 느슨하게 IP 주소로 해석되면 TLS 호스트 이름 검증을 우회한다                                      |
| `CVE-2026-111497` | High   | 26.x, 24.x, 22.x | Brotli 디코더의 범위 밖 쓰기가 원격 코드 실행을 허용한다                                                  |
| `CVE-2026-105481` | Medium | 26.x, 24.x, 22.x | keep-alive 소켓이 요청을 보내기 전에 쓰인 응답을 처리한다                                                 |
| `CVE-2026-106072` | Medium | 26.x, 24.x, 22.x | 비정규 IPv4 호스트 이름으로 인해 DNS SAN이 IP 엔드포인트를 인증한다                                       |
| `CVE-2026-106074` | Medium | 26.x, 24.x, 22.x | `crypto.randomUUID()`와 `randomInt()`의 엔트로피 캐시가 스냅샷에 저장되어 프로세스마다 같은 값을 반복한다 |
| `CVE-2026-106070` | Low    | 26.x             | `ZipFile`이 ZIP 헤더 검증에 실패한 뒤 공격자가 통제하는 앞부분 바이트를 반환한다                          |
| `CVE-2026-106071` | Low    | 26.x             | 와일드카드 기수 조회로 Permission Model이 파일 시스템 권한을 과다 부여한다                                |
| `CVE-2026-106073` | Low    | 26.x, 24.x, 22.x | `fs.realpathSync`로 Permission Model을 우회한다                                                           |

공지는 의존성 업데이트도 함께 알린다.
c-ares는 세 라인 모두, OpenSSL은 24.x와 22.x, SQLite는 22.x, Undici는 세 라인 모두 올렸다.
세 라인 모두에 CA 인증서 묶음 업데이트도 들어갔고, 공지는 이를 eMudhra 중간 CA 침해 대응으로 표시한다.
공지는 지원이 끝난 버전이 보안 릴리스에 항상 영향을 받으므로 지원되는 버전을 쓰라고 덧붙인다.

공지 자체는 항목마다 제목, 영향받는 라인, 보고자와 수정자만 적고 취약점의 동작 조건은 설명하지 않는다.
이 글에서는 세 버전의 릴리스 노트에 적힌 수정 커밋 제목으로 각 취약점이 무엇을 고쳤는지 보충한다.

## 동작 방식

### 호스트 이름 검증을 우회하는 세 건

세 건 모두 TLS 인증서가 호스트 이름과 맞는지 따지는 과정에 있다.
`CVE-2026-106069`와 `CVE-2026-106072`는 같은 수정 `tls: reject non-canonical IP addresses`로 묶여 나왔고,
`CVE-2026-105483`에는 `tls: fix ip normalization regression`이라는 별도 수정이 붙었다.[^v24]
공지가 제목으로 밝힌 조건은 각각 IP가 전각 숫자로 쓰인 경우, 호스트가 느슨하게 IP 주소로 해석되는 경우, 비정규 IPv4 호스트 이름이 DNS SAN으로 IP 엔드포인트를 인증하는 경우다.

`CVE-2026-105483`이 22.x에는 해당하지 않는다는 점이 단서가 된다.
수정 커밋 제목에 회귀(regression)라는 말이 들어 있는데, 이는 22.x에는 없고 24.x 이상에서 생긴 정규화 변경의 부작용이었다는 추론과 맞는다.
22.23.4의 릴리스 노트에는 이 수정이 없고,[^v22] 24.22.1과 26.12.1에는 있다.[^v24][^v26]

### dns.resolve가 NUL 문자에서 이름을 자른다

수정은 `dns: validate resolve inputs for null bytes`다.[^v24]
이름에 NUL 문자가 있으면 그 앞까지만 질의되므로, 검증을 통과한 이름과 실제로 조회된 이름이 달라진다.
수정되지 않은 24.11.0에서 직접 실행해 보면 이 동작이 그대로 나온다.

```javascript
import dns from 'node:dns';

// NUL 앞의 example.com만 질의되면 example.com의 주소가 돌아온다.
dns.resolve4('example.com\0.invalid', (err, addresses) => {
  console.log(err?.code ?? 'no error', addresses);
});
```

수정되지 않은 24.11.0에서 이 코드는 오류 없이 `example.com`의 주소 목록을 출력했다.
이 글을 쓸 때 직접 실행한 결과이며, 수정된 버전의 출력은 확인하지 못했다.

### Brotli 디코더의 범위 밖 쓰기

공지는 이 취약점을 `Node.js Brotli decoder out-of-bounds write permits remote code execution`이라는 한 줄로만 설명한다.
수정은 Brotli의 커밋 `0ed4268a4401abcb44720963`을 가져온(cherry-pick) 것이고,
수정 과정에서 `BROTLI_DECODER_ERROR_FORMAT_BLOCK_SWITCH`가 새로 노출되었다.[^v24]
Brotli로 압축된 입력을 푸는 코드가 영향 범위일 수 있다는 것은 추론이며, 어떤 경로로 입력이 도달하는지는 공지에 없다.

### 나머지 중간·낮은 심각도

`CVE-2026-105481`의 수정은 `http: ensure agent data guard works without I/O`다.[^v24]
`CVE-2026-106074`는 `crypto: reset random caches across snapshots`로 고쳤다.[^v24]
공지가 설명하는 증상은 사용자 영역 시작 스냅샷과 SEA(단일 실행 파일 애플리케이션)에 난수 캐시가 저장되어 모든 프로세스가 같은 값을 반복한다는 것이다.
Permission Model의 `CVE-2026-106073`은 `permission: check permission model in realpathSync`로 고쳤다.[^v24]
26.x에만 해당하는 `CVE-2026-106070`과 `CVE-2026-106071`의 수정은 각각 `zlib: avoid caching invalid ZIP local headers`와 `src: fix the fs permission tree node on wildcard nodes`다.[^v26]

### 의존성과 인증서 묶음

세 라인 모두 루트 인증서를 NSS 3.131.1로 올렸고 c-ares를 1.34.9로 올렸다.[^v24][^v22][^v26]
24.22.1과 22.23.4는 OpenSSL 소스를 3.5.9로 올렸고, 타임존 데이터도 2026e로 올렸다.[^v24][^v22]
Undici는 24.x가 7.30.1, 22.x가 6.29.1이고, 26.x가 8.12.2다.[^v24][^v22][^v26]
SQLite는 22.x만 3.53.4로 올렸다.[^v22]

세 라인의 릴리스 노트에는 `tls: reject chains containing blocked public keys`도 있다.[^v24][^v22][^v26]
이 수정이 eMudhra 침해와 직접 이어지는지는 노트에 적혀 있지 않다.
같은 사건을 다룬 `security/eight-bits-of-trust.md`의 내용으로 보면 이유를 짐작할 수 있으나, 짐작일 뿐이다.

## 업데이트하기

사용하는 라인에 맞는 버전으로 올린다.

| 라인 | 올릴 버전 | 비고                     |
| ---- | --------- | ------------------------ |
| 26.x | 26.12.1   | Current 라인이다         |
| 24.x | 24.22.1   | LTS 코드명은 Krypton이다 |
| 22.x | 22.23.4   | LTS 코드명은 Jod이다     |

지원이 끝난 라인은 이 목록에 없다.
공지는 지원이 끝난 버전이 보안 릴리스에 항상 영향받는다고 하므로 지원되는 라인으로 올려야 한다.

설치된 버전을 확인하고, 컨테이너로 배포한다면 이미지 안의 버전도 확인한다.

```bash
node -p "process.version"
# 컨테이너 이미지는 새 버전으로 다시 빌드되었는지 직접 확인한다.
docker run --rm node:24 node -p "process.version"
```

## 확인할 값

업데이트 뒤에 의존성 버전이 릴리스 노트의 값과 같은지 확인할 수 있도록, 라인별 기대 값을 정리하면 다음과 같다.

| 항목      | 22.x    | 24.x    | 26.x    | 출처의 근거                             |
| --------- | ------- | ------- | ------- | --------------------------------------- |
| `node`    | 22.23.4 | 24.22.1 | 26.12.1 | 공지의 수정 버전                        |
| `ares`    | 1.34.9  | 1.34.9  | 1.34.9  | 세 라인의 릴리스 노트                   |
| `openssl` | 3.5.9   | 3.5.9   | 없음    | 공지가 OpenSSL을 24.x와 22.x에만 적었다 |
| `undici`  | 6.29.1  | 7.30.1  | 8.12.2  | 라인별 릴리스 노트                      |
| `sqlite`  | 3.53.4  | 없음    | 없음    | 공지가 SQLite를 22.x에만 적었다         |
| `tz`      | 2026e   | 2026e   | 없음    | 22.x와 24.x의 릴리스 노트에만 있다      |

표에서 없음은 이 릴리스가 해당 의존성을 올리지 않았다는 뜻이며, 해당 값이 비어 있다는 뜻이 아니다.

## 확인하기

다음 스크립트는 현재 실행 중인 Node.js의 버전과 의존성 버전을 위 표와 비교하고,
`CVE-2026-105482`의 NUL 문자 동작을 시험한다.

```javascript
import dns from 'node:dns';

const major = Number(process.versions.node.split('.')[0]);
const expectedByMajor = {
  22: { node: '22.23.4', ares: '1.34.9', openssl: '3.5.9', undici: '6.29.1', sqlite: '3.53.4', tz: '2026e' },
  24: { node: '24.22.1', ares: '1.34.9', openssl: '3.5.9', undici: '7.30.1', tz: '2026e' },
  26: { node: '26.12.1', ares: '1.34.9', undici: '8.12.2' },
};
const expected = expectedByMajor[major];
if (!expected) {
  console.log(`${process.version}: 이 표에 없는 라인이다. 지원되는 라인으로 올려야 한다.`);
  process.exit(1);
}

// 숫자로만 이루어진 버전은 구간별로 비교하고, 2026e 같은 값은 문자열로 비교한다.
function atLeast(actual, wanted) {
  if (!/^[\d.]+$/.test(wanted)) return actual >= wanted;
  const a = actual.split('.').map(Number);
  const w = wanted.split('.').map(Number);
  for (let i = 0; i < w.length; i++) {
    if ((a[i] ?? 0) !== w[i]) return (a[i] ?? 0) > w[i];
  }
  return true;
}

let ok = true;
for (const [key, wanted] of Object.entries(expected)) {
  const actual = key === 'node' ? process.versions.node : process.versions[key];
  const pass = actual !== undefined && atLeast(actual, wanted);
  ok &&= pass;
  console.log(`${pass ? 'OK  ' : 'FAIL'} ${key}: ${actual} (기대 ${wanted} 이상)`);
}

// CVE-2026-105482: NUL 문자 앞까지만 질의되면 취약하다.
await new Promise((resolve) => {
  try {
    dns.resolve4('example.com\0.invalid', (err, addresses) => {
      if (addresses?.length) {
        ok = false;
        console.log('FAIL dns.resolve4: NUL 뒤가 잘려 example.com이 조회되었다');
      } else if (err?.code?.startsWith('ERR_')) {
        console.log(`OK   dns.resolve4: 입력이 거부되었다 (${err.code})`);
      } else {
        console.log(`??   dns.resolve4: 판정 불가 (${err?.code}), 네트워크를 확인한다`);
      }
      resolve();
    });
  } catch (err) {
    console.log(`OK   dns.resolve4: 동기 오류로 거부되었다 (${err.code})`);
    resolve();
  }
});

process.exit(ok ? 0 : 1);
```

수정되지 않은 24.11.0에서 직접 실행하면 모든 줄이 `FAIL`로 나오고 NUL 시험도 실패한다.
`dns.resolve4` 시험에서 판정 불가가 나오면 DNS에 접근할 수 없는 환경이다.
수정된 버전에서 입력을 어떤 오류 코드로 거부하는지는 확인하지 못했고, 코드가 `ERR_`로 시작한다는 것은 Node.js의 일반적인 규칙에 기댄 가정이다.

## 트레이드오프

### 26.x는 취약점 수정 외의 동작 변경도 들어 있다

26.12.1의 커밋 목록에는 `Revert "module: synchronously load most ES modules"`가 있다.[^v26]
보안 수정과 상관없는 되돌림이 같은 릴리스에 섞여 있다.
Current 라인에서 ES 모듈 로딩 방식에 기대는 코드가 있다면 업데이트 뒤에 동작이 달라질 수 있으므로 배포 전에 테스트해야 한다.
보안 수정만 따로 받는 방법은 없고, 그 코드가 문제라면 이전 버전에 머물러야 하는데 그 선택은 취약점을 안고 가는 것이다.

### 공지의 정보가 적어서 영향 판단이 어렵다

공지는 High 네 건 가운데 Brotli 건에만 한 문장 설명을 붙였고, 그것도 제목을 되풀이한 정도다.
호스트 이름 검증 우회가 어떤 클라이언트 설정에서 실제로 악용되는지는 공지에 없다.
그래서 업데이트 여부를 영향 분석으로 정하기 어렵고, 보수적으로 모든 라인을 올리는 것이 현실적인 선택이다.
이 선택의 비용은 테스트와 배포에 드는 시간이며, 영향이 없는 서비스까지 같은 비용을 치른다.

## 함정

### SEA와 스냅샷은 다시 만들어야 한다

`CVE-2026-106074`는 난수 캐시가 사용자 영역 스냅샷과 SEA에 저장되는 문제다.
런타임을 올려도 이미 만들어 둔 SEA 파일에는 이전 바이너리가 들어 있을 것으로 보이는데,
이는 SEA가 실행 파일에 런타임을 포함한다는 구조에서 나온 추론이다.
SEA나 스냅샷을 배포하는 쪽은 새 버전으로 다시 빌드해야 하고, 이미 배포한 파일이 생성한 UUID는 겹칠 수 있다.

### 컨테이너와 배포판 패키지는 늦게 올 수 있다

공식 다운로드는 릴리스 당일에 있어도, 배포판 패키지와 컨테이너 이미지는 그보다 늦을 수 있다.
위의 `docker run` 명령처럼 실제 이미지 안의 버전을 확인해야 한다.
이미지 태그가 `node:24`처럼 움직이는 태그라면 다시 빌드하지 않는 한 이전 버전이 남는다.

### 22.x는 수정 목록이 다르다

22.x에는 `CVE-2026-105483`이 없고 대신 SQLite 업데이트가 있다.
라인별로 목록이 다르므로 한 라인에서 확인한 내용을 다른 라인에 그대로 적용하면 안 된다.

## 체크리스트

- 사용 중인 Node.js 라인이 26.x, 24.x, 22.x 중 하나인가?
- 해당 라인의 수정 버전(26.12.1, 24.22.1, 22.23.4) 이상인가?
- 지원이 끝난 라인을 쓰고 있다면 지원되는 라인으로 올릴 계획이 있는가?
- 컨테이너 이미지 안의 `process.version`이 수정 버전 이상인가?
- 확인 스크립트가 `FAIL` 없이 끝나는가?
- SEA나 시작 스냅샷을 배포한다면 새 버전으로 다시 빌드했는가?
- 26.x로 올렸다면 ES 모듈 로딩에 의존하는 코드를 테스트했는가?

## 기억할 원칙

### 심각도만 있는 공지는 영향 조건을 직접 확인해야 한다

이 공지는 심각도와 영향받는 라인을 알려 주지만 악용 조건은 알려 주지 않는다.
그런 공지에서는 해당 기능을 쓰는지가 아니라 해당 버전인지를 기준으로 판단하는 것이 안전하다.
조건을 직접 분석할 수 있는 시간이 없다면 업데이트 자체를 가장 싼 확인 수단으로 삼아야 한다.

### 업데이트는 확인 절차까지 포함해야 끝난다

패키지 관리자의 버전 번호, 컨테이너 이미지의 버전, 의존성 버전은 서로 다를 수 있다.
업데이트를 마쳤다고 보고하려면 실제로 실행되는 프로세스의 `process.versions`를 근거로 삼아야 한다.

---

[^v24]: Node.js, [Node.js — Node.js 24.22.1 (LTS)](https://nodejs.org/en/blog/release/v24.22.1), 2026-10-21

[^v22]: Node.js, [Node.js — Node.js 22.23.4 (LTS)](https://nodejs.org/en/blog/release/v22.23.4), 2026-10-21

[^v26]: Node.js, [Node.js — Node.js 26.12.1 (Current)](https://nodejs.org/en/blog/release/v26.12.1), 2026-10-21
