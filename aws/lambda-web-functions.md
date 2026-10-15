# AWS Lambda Web Functions: 어댑터 없이 표준 HTTP 서버를 Lambda에서 돌리기

원문: [AWS Lambda Web Functions 정식 출시 | Amazon Web Services 한국 블로그](https://aws.amazon.com/ko/blogs/korea/announcing-aws-lambda-web-functions-for-fast-consistent-web-app-performance-anywhere/)

HN 토론: <https://news.ycombinator.com/item?id=50069318> (109점, 102개 댓글)

## 소개

AWS의 Micah Walter가 2026년 10월 14일 발표한 글로,
Lambda의 새 폼 팩터인 Web Functions의 정식 출시를 알린다.
핵심은 Express, Hono, Fastify, Next.js 같은 Node.js 프레임워크로 만든
포트 리스닝 서버를 이벤트 핸들러로 고치지 않고
명령 하나로 Lambda에 배포한다는 것이다.
확장, 다중 리전 배포, 활성 CPU 기준 과금은 Lambda가 맡는다.

이 출시로 Lambda는 같은 Firecracker 격리 기술 위에
프로그래밍 모델이 다른 세 가지 폼 팩터를 갖게 되었다.

| 폼 팩터         | 프로그래밍 모델                            | 과금 기준       | 맞는 작업                                |
| --------------- | ------------------------------------------ | --------------- | ---------------------------------------- |
| Event Functions | 이벤트 핸들러, 환경당 동시 실행 1개        | 실제 경과 시간  | AWS 서비스 이벤트, 큐 소비자, 간접 호출  |
| Web Functions   | 포트에서 HTTP 수신, 다중 동시 실행         | 활성 CPU 사용량 | 웹 앱, API 백엔드, 대화형 HTTP           |
| MicroVM         | 고객 관리형 수명 주기의 상태 저장 샌드박스 | 원문에 없음     | 신뢰할 수 없거나 사용자가 만든 코드 실행 |

기존 Lambda 함수에는 Event Functions라는 이름이 새로 붙었다.
글은 세 가지를 한 애플리케이션 안에서 섞어 쓰라고 권한다.
비동기 백엔드는 Event Functions,
사용자 대면 API와 서버 측 렌더링은 Web Functions,
코드 실행 기능은 MicroVM에 맡기는 식이다.

출시 시점 지원 리전은 미국 동부(버지니아 북부, 오하이오), 미국 서부(오리건),
아시아 태평양(도쿄), 유럽(아일랜드)이다.
런타임은 Arm64 기반 Node.js 24(`nodejs24.x`) 하나이며 VPC 연결을 지원한다.
서울 리전은 목록에 없다.

## 동작 방식

### 한 실행 환경이 여러 요청을 받는다

기존 Lambda는 실행 환경 하나가 한 번에 요청 하나만 처리했다.
트래픽이 몰리면 요청마다 새 환경이 필요했고, 그만큼 콜드 스타트가 늘었다.
Web Functions는 환경당 최대 128건의 동시 요청을 처리한다.
트래픽이 급증해도 이미 준비된 환경을 여러 요청이 나눠 쓴다.

그렇다고 콜드 스타트가 사라지는 것은 아니다.
HN에서 jazzypants가 인용한 설명서에 따르면
트래픽이 없으면 환경이 0개로 줄고, 그다음 요청은 새 환경을 띄운다.[^jazzypants]
128이라는 숫자도 함수 전체가 아니라 환경 하나의 상한이다.
AWS의 julianwood는 HN에서 Lambda가 이 환경 자체를
아주 많이 늘릴 수 있다고 설명했다.[^julianwood]

### CPU는 쓴 만큼, 메모리는 살아 있는 동안

과금은 두 갈래다.
CPU는 코드가 실제로 CPU를 쓰는 시간만 측정하므로
데이터베이스 쿼리나 외부 API 응답을 기다리는 동안에는 거의 청구되지 않는다.
메모리는 실행 환경이 존재하는 동안 계속 측정된다.
글은 서버 측 렌더링, API 백엔드, AI 추론 토큰 스트리밍처럼
I/O 대기가 긴 워크로드에서 비용이 줄어든다고 설명한다.

### 수정 버전과 엔드포인트

배포하면 코드의 변경 불가능한 스냅숏인 수정 버전(revision)이 생긴다.
엔드포인트는 HTTPS URL이며 트래픽을 한 수정 버전으로 보내거나
여러 수정 버전에 나눠 보낸다.
같은 배포 명령을 다시 실행하면 CLI가 기존 함수를 찾아
새 수정 버전을 올리고 엔드포인트를 옮긴다.
여러 리전에 배포하면 코드를 복제하고 지연 시간 기반 라우팅을 자동으로 구성해
`<domain-id>.lambda-web.global.on.aws` 형태의 글로벌 URL 하나로 받는다.

## 구현하기

### 서버 코드

로컬에서 `node index.js`로 돌리는 Express 서버와 같다.
다른 점은 수신할 호스트와 포트를
`AWS_LAMBDA_HTTP_ENDPOINT` 환경 변수에서 읽는 것뿐이다.

```javascript
import express from 'express';

const app = express();
// Lambda가 host:port 형태로 넣어 준다. 고정 포트를 쓰면 요청을 받지 못한다.
const [host, port] = process.env.AWS_LAMBDA_HTTP_ENDPOINT.split(':');

app.get('/', (req, res) => {
  res.json({ message: 'Hello from Lambda Web Functions!' });
});

app.listen(port, host, () => {
  console.log(`Server running on port ${port}`);
});
```

로컬에서는 변수를 직접 지정해 실행한다.

```bash
AWS_LAMBDA_HTTP_ENDPOINT=127.0.0.1:3000 node index.js
```

### 배포

```bash
# 첫 배포: 번들링, 함수 생성, 첫 수정 버전 게시, 엔드포인트 연결까지 한 번에
aws lambda-web deploy --name my-web-app --code ./my-app

# 다중 리전 배포: 지연 시간 기반 라우팅이 자동 구성된다
aws lambda-web deploy --name my-web-app --code ./my-app \
  --regions us-east-1,eu-west-1,ap-northeast-1

# 예제 함수로 바로 시험해 보기
aws lambda-web deploy --name hello-world --hello-world
```

저자는 첫 배포 후 1분 안에 HTTPS URL을 받았고,
코드를 고쳐 다시 배포하는 데는 몇 초가 걸렸다고 적었다.

### 카나리 배포

자동 배포를 끄고 수정 버전별 가중치를 지정한다.

```bash
aws lambda-web update-web-function-endpoint \
  --function-name my-web-app \
  --endpoint-name dev \
  --auto-deployment-mode Disabled \
  --revision-weights '[{"revisionId": "<current-revision-id>", "weight": 90}, {"revisionId": "<new-revision-id>", "weight": 10}]'
```

### CloudFront 앞단

정적 자산과 동적 요청이 섞인 앱이라면 웹 함수 엔드포인트를
CloudFront 배포의 오리진으로 둔다.
CloudFront 오리진 액세스 제어(OAC)를 엔드포인트에 연결하면
CloudFront가 오리진 요청에 서명하고 엔드포인트는 그 배포의 호출만 받는다.
S3 버킷을 CloudFront 뒤에 숨기던 것과 같은 패턴을
별도 인증 코드 없이 쓸 수 있다.

## 트레이드오프

### 동시 실행은 콜드 스타트를 줄이고 격리를 가져간다

기존 Lambda의 “환경당 요청 하나”는 비효율이었지만 장점도 있었다.
요청 사이에 전역 상태가 섞이지 않았고,
한 요청이 메모리를 터뜨려도 다른 요청은 영향을 받지 않았다.
환경당 128건을 받는 순간 이 보장은 사라진다.
모듈 전역에 요청별 값을 넣어 두던 코드,
요청마다 커넥션을 열고 닫던 코드는 일반 서버와 똑같은 동시성 버그를 만난다.

반대로 이것이 Web Functions의 장점이기도 하다.
일반 Node.js 서버처럼 동작하므로 커넥션 풀을 환경 단위로 공유할 수 있고,
기존 Express 앱을 고치지 않고 올릴 수 있다.
얻는 것은 이식성과 효율, 잃는 것은 Lambda가 대신 해 주던 요청 격리다.

### 활성 CPU 과금은 I/O 대기에 유리하고 메모리에는 중립이다

I/O 대기 시간 동안 CPU가 청구되지 않는다는 것은
LLM API를 호출하고 토큰을 흘려보내는 엔드포인트에 특히 유리하다.
경과 시간 과금에서는 모델이 응답을 생성하는 수십 초가 모두 비용이었다.

다만 메모리는 환경이 살아 있는 동안 계속 청구된다.
요청이 적은 시간대에도 환경이 유지되면 메모리 비용은 쌓인다.
글은 구체적인 요금을 AWS Lambda 요금 페이지로 넘기고 있어,
어떤 트래픽 패턴에서 기존 Lambda나 Fargate보다 싼지는
요금표를 놓고 직접 계산해야 한다.

HN에서는 이 과금 방식이 Cloudflare Workers를 겨냥했다는 해석이 많았다.
mikeocool은 업스트림 응답을 기다리는 동안 처리 시간을 내지 않는 것이
Workers의 진짜 강점이며
그동안 이것을 제공한 FaaS는 Cloudflare뿐이었다고 했다.[^mikeocool]
TheJCDenton은 같은 활성 CPU 과금이지만 메모리는 함수가 떠 있는 내내 내고,
데이터 전송과 요청 수도 따로 따져야 한다며
Cloudflare의 요금이 훨씬 읽기 쉽다고 지적했다.[^TheJCDenton]
dzonga는 Workers가 V8 isolate 위에서,
Web Functions는 Firecracker VM 위에서 돌기 때문에
시작 시간이 어떻게 나올지가 관건이라고 했다.[^dzonga]

### 이식성은 높아졌지만 플랫폼은 여전히 Lambda다

어댑터가 사라졌으니 같은 코드를 컨테이너나 다른 서버리스 플랫폼으로
옮기기 쉬워졌다는 점은 분명한 진전이다.
그러나 `aws lambda-web` CLI, 수정 버전과 엔드포인트 모델,
글로벌 URL과 OAC 연결은 모두 AWS 고유의 운영 체계다.
코드는 프레임워크에 묶이지 않지만 배포와 트래픽 관리는 여전히 Lambda에 묶인다.

비교 대상도 이미 있다.
CharlieDigital은 Google Cloud Run과 Azure Container Apps가 가장 가까운 상대라며,
둘 다 어댑터 없이 웹 앱을 배포하고,
0까지 줄어들고, 동시성을 조절할 수 있다고 했다.[^CharlieDigital]
deepsun은 Google은 코드 업로드형인 Cloud Functions보다
컨테이너형인 Cloud Run을 권하는데
AWS는 왜 코드 업로드 방식으로 되돌아갔는지 의문을 표했다.[^deepsun]

### 어댑터와 무엇이 다른가

joshstrange는 Hono나 Express를 어댑터와 함께 Lambda에 넣는 방식을
이미 많은 사람이 쓰고 있는데 무엇이 더 나으냐고 물었다.[^joshstrange]
어댑터 방식은 요청 하나를 이벤트로 바꿔 서버에 흘려 넣을 뿐,
환경당 요청 하나와 경과 시간 과금이라는 Lambda의 모델은 그대로다.
Lord_Zero가 답했듯 Web Functions의 차이는 어댑터가 사라진 것이 아니라
동시 연결과 CPU 과금이라는 실행 모델이 바뀐 데 있다.[^Lord_Zero]

## 도입 여부를 가르는 시험

비용 비교는 같은 요청 분포를 재생해 해야 한다.
Web Functions의 청구액은 활성 CPU 사용량만으로 결정되지 않고,
실행 환경이 살아 있는 동안의 메모리와 요청·전송 비용도 함께 움직인다.
따라서 평균 응답 시간만 비교하지 말고
환경이 0으로 줄어드는 시간, 순간 동시성,
외부 I/O 대기 비율을 포함한 부하 기록을 사용한다.

기능 적합성도 별도로 확인한다.
요청 간 상태를 전역 변수에 보관하지 않는지,
128건 동시 처리에서 커넥션 풀이 버티는지,
CPU를 오래 쓰는 요청이 이벤트 루프를 막지 않는지 시험한다.
실패 시 재시도와 수정 버전 되돌리기가 가능한지도
실제 배포 환경에서 확인해야 한다.

이 시험에서 I/O 대기가 길고 서버 코드를 거의 바꾸지 않아도 된다면
Web Functions가 유력한 후보가 된다.
상태가 요청 사이에 강하게 이어지거나,
고정된 용량과 일관된 장기 실행이 더 중요하다면
컨테이너 기반 대안도 같은 조건으로 비교해야 한다.

## 함정

- 고정 포트로 `listen`하면 동작하지 않는다.
  `AWS_LAMBDA_HTTP_ENDPOINT`에서 호스트와 포트를 읽어야 한다.
- 출시 시점 런타임은 Arm64의 Node.js 24뿐이다.
  x86 전용 네이티브 모듈이나 다른 언어의 서버는 아직 올릴 수 없다.
  solatic은 Node.js 전용이라는 점에 실망하며 에이전트에게 Rust나 Go로 쓰게 해
  정적 바이너리 하나를 올리고 싶다고 했고,[^solatic]
  julianwood는 Web Functions 로드맵을 공개된 GitHub 프로젝트로 안내했다.[^julianwood-roadmap]
- 서울 리전이 지원 목록에 없다.
  다중 리전 배포 예시도 도쿄(`ap-northeast-1`)를 쓴다.
  국내 사용자 대상 서비스라면 지연 시간과 데이터 위치 요건을 먼저 확인해야 한다.
- 다중 리전 복제는 코드만 복제한다.
  데이터베이스가 한 리전에 있다면 다른 리전의 함수는
  결국 그 리전까지 왕복하므로 지연 시간 이득이 사라진다.
- 128건 동시 처리 환경에서 CPU를 오래 쓰는 요청 하나는
  같은 환경의 다른 요청을 지연시킨다.
  Node.js의 이벤트 루프 블로킹 문제가 그대로 따라온다.
- 원문은 실행 시간 제한, 요청 크기 제한, 웹소켓 지원 여부를 다루지 않는다.
  배포 전에 설명서에서 확인해야 한다.

## 체크리스트

- [ ] 서버가 `AWS_LAMBDA_HTTP_ENDPOINT`의 호스트와 포트로 수신하는가
- [ ] 요청별 상태를 모듈 전역 변수에 저장하는 코드가 없는가
- [ ] 데이터베이스 커넥션을 요청마다 열지 않고 환경 단위 풀로 공유하는가
- [ ] 네이티브 의존성이 Arm64에서 빌드되는가
- [ ] 대상 사용자와 데이터 위치에 맞는 리전이 지원 목록에 있는가
- [ ] 다중 리전 배포 시 데이터 계층도 리전별로 가까이 있는가
- [ ] CloudFront를 앞에 둔다면 OAC를 연결해 엔드포인트 직접 호출을 막았는가
- [ ] 새 수정 버전을 가중치 라우팅으로 먼저 일부 트래픽에 시험했는가

## 기억할 원칙

### 서버리스가 서버의 모양으로 돌아왔다

Lambda는 처음에 “서버를 생각하지 말라”며
코드를 이벤트 핸들러라는 고유한 모양으로 바꾸게 했다.
그 대가로 개발자들은 어댑터를 쓰고, 프레임워크를 고치고,
로컬과 운영의 차이를 감수했다.
Web Functions는 그 모양을 포기하고 평범한 HTTP 서버를 받아들인다.
Cloud Run과 Fargate가 컨테이너를 받아들인 방향과 같다.

플랫폼이 개발자에게 고유한 프로그래밍 모델을 요구할수록
진입 장벽이 높아지고, 결국 플랫폼이 표준 쪽으로 다가온다.
새로운 플랫폼을 고를 때는 그 플랫폼이 요구하는 모양이
나중에 사라질 가능성까지 고려해,
코드는 가능한 한 표준의 모양으로 두는 편이 낫다.

---

[^jazzypants]: <https://news.ycombinator.com/item?id=50064967>

[^julianwood]: <https://news.ycombinator.com/item?id=50079338>

[^mikeocool]: <https://news.ycombinator.com/item?id=50070583>

[^TheJCDenton]: <https://news.ycombinator.com/item?id=50071603>

[^dzonga]: <https://news.ycombinator.com/item?id=50070915>

[^CharlieDigital]: <https://news.ycombinator.com/item?id=50070579>

[^deepsun]: <https://news.ycombinator.com/item?id=50081167>

[^joshstrange]: <https://news.ycombinator.com/item?id=50071082>

[^Lord_Zero]: <https://news.ycombinator.com/item?id=50081906>

[^solatic]: <https://news.ycombinator.com/item?id=50077138>

[^julianwood-roadmap]: <https://news.ycombinator.com/item?id=50079328>
