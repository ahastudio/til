# Next.js Kubernetes OOM 토론 (2023)

원문: [OOM issue with Next.js on Kubernetes](https://github.com/vercel/next.js/discussions/46873)

## 요약

2023년 3월 7일 vercel/next.js의 Help 범주에 erkand-imeri가 올린 토론 #46873이다.
원 글의 추천은 2이다.

질문자는 Kubernetes에서 파드 메모리가 계속 오르고 내려가지 않다가 한도에서 파드가 재시작된다고 쓴다.
앱 코드, 순환 임포트, GC를 의심했고 정적 텍스트만 그리는 두 번째 Next.js 앱도 같게 동작했다고 한다.
환경은 `node:16.15.0-alpine`, yarn 1.22.19, 다단계 빌드와 `.next/standalone` 출력, 비루트 사용자, 3005 포트이다. 시작 명령은 `node --max-old-space-size=360 server.js`이며 512MB 파드 한도의 약 75%로 온라인 조언을 따랐다고 한다.
Istio 경로 기반 라우팅으로 한 도메인에서 `basePath`가 `/plain-nextjs`이다. `next.config.js`에는 SVG용 사용자 지정 webpack 규칙, `reactStrictMode: false`, `output: "standalone"`, `swcMinify: true`, `compress: true`가 있고 의존성은 Next 13.1.5와 React 18.2.0이다.

대화는 다음과 같이 흘렀다.

- 3월 9일 질문자가 재현 저장소와 스테이징의 Grafana 화면(부하가 낮은데 메모리가 오르고 처음 수준으로 돌아오지 않음)을 올렸다. 협력자 icyJoseph는 파드 수준의 동작을 배제했는지 묻고 파드가 부하 뒤 메모리를 반환하지 않는 스택오버플로 질문과 AWS ECS 에이전트의 누수 이슈를 링크했으며, 힙 덤프를 받는 엔드포인트(토론 #26801)와 힙 덤프를 요청했다.
- 질문자는 `experimental.isrMemoryCacheSize: 0`을 시도해도 변화가 없었고 누수가 아니라 느긋한 GC로 의심된다고 했다. Helm 설정은 요청 CPU 50m와 메모리 128Mi, 한도 CPU 300m와 메모리 512Mi이다. `--max-old-space-size`가 Kubernetes 한도와 관련이 있는지, Node가 한도를 무시하고 파드가 재시작될 때까지 느긋하게 GC하는지 물었다. icyJoseph는 두 한도가 충돌할 수 있으니 조사해 보겠다고 답했다.
- 질문자는 구글 클라우드 블로그를 인용해 512MB 한도를 파드마다 나눠야 하는지(최소 파드 2개, 각 1컨테이너로 파드당 약 256MB)를 물었다. 답은 없었다.
- 3월 23일 질문자가 결론을 적었다. 핵심은 앱 누수가 아니라 느긋한 GC일 가능성이 크고, Istio의 `istio-proxy` 사이드카가 파드마다 약 150Mi를 써 앱이 쓸 메모리를 줄였다는 것이다. `--max-old-space-size`를 쿠버네티스 한도에서 사이드카를 뺀 값의 약 80%로 잡으라고 권하며 예로 `node --max-old-space-size=200 --optimize_for_size --gc_interval=100 server.js`를 든다. Istio `Sidecar` 객체로 송신을 제한하고 파드 템플릿의 `sidecar.istio.io/inject: "false"`로 주입을 끄는 방법도 적는다. 이 글의 추천은 2이다.

## 분석

### 쟁점은 누수가 아니라 한도의 구성이다

질문자의 최종 진단은 앱 누수가 아니라 컨테이너 한도, V8 힙 한도, 사이드카의 메모리가 서로 맞지 않았다는 것이다.
앞서 정리한 `nodejs/docker-memory-limit.md`가 말하는 두 한도의 관계가 실제 사례로 나타난 셈이다. 이는 이 문서의 해석이다.

### 진단이 질문자 스스로에게서 나왔다

협력자는 힙 덤프와 파드 수준의 동작을 확인하라고 안내했을 뿐이고 결론은 질문자가 두 주 뒤에 적었다.
토론은 닫혔지만 답으로 표시된 것이 없다.

## 비평

### 결론의 근거가 측정으로 제시되지 않았다

질문자의 결론은 느긋한 GC이고 사이드카가 약 150Mi를 쓴다는 서술인데, 수정 뒤의 메모리 그래프나 재현 결과가 이 토론에 없다.
권고한 80%와 GC 플래그 값(`gc_interval=100`)의 근거도 적혀 있지 않다.

### 재현이 단순하지만 환경이 오래되었다

환경은 2023년의 Next 13.1.5와 Node 16이다. 지금 버전의 동작과 같다고 볼 수 없다.
같은 증상이 2026년 Next.js 16 토론에서도 나온다. 이는 `nextjs/memory-leak-oom-discussion.md`에 정리했다.

### 외부 반응

GeekNews에서는 `Next.js OOM Kubernetes`가 결과 없음이었고 대조 쿼리는 정상이었다.

## 인사이트

### 가져갈 것은 힙 한도를 컨테이너 한도에서 사이드카를 뺀 값으로 잡는 순서이다

파드 한도에서 사이드카와 힙 밖 메모리를 뺀 값을 기준으로 V8 한도를 정한다는 순서는 서비스 메시를 쓰는 어느 Node.js 앱에도 적용된다. 이는 이 문서의 적용이다.

### 증상이 같아도 원인은 구성일 수 있다

메모리가 오르고 내려가지 않는 것은 누수의 증상이지만 GC 시점과 한도 구성으로도 같게 보인다.
힙 덤프로 누수 여부를 가린 뒤에 한도를 조정하는 순서가 낫다.

### 확인할 관찰

이 토론의 주장을 가를 관찰은 세 가지이다.
사이드카 제거나 한도 조정 뒤의 메모리 그래프,
권고한 GC 플래그의 효과,
현재 Next.js와 Node 버전에서의 재현이다.
