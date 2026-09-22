# Cloudflare Python Workers 정식 출시: WebAssembly 위에서 Python이 1급 언어가 되기까지

원문: [Python Workers are now generally available](https://blog.cloudflare.com/python-workers-ga/)

HN 토론: <https://news.ycombinator.com/item?id=49787142> (216점, 36개 댓글)

GN 토론: <https://news.hada.io/topic?id=34087>

## 소개

2년 전에 도입한 Python Workers가 정식 출시되었다는 Cloudflare의 발표다.
원래 목표는 TypeScript로 Worker를 쓰는 것만큼 Python으로 쓰는 것도 간단하게 만들고,
Python 패키지와 프레임워크 생태계가 그냥 작동하게 만드는 것이었다.

정식 출시가 무엇을 뜻하는지가 명시되어 있다.
Python이 Cloudflare 개발자 플랫폼에서 1급이며 완전히 지원되는 언어가 되었다는 것이다.
이미 아는 Python 코드와 라이브러리와 설계 방식을 가져와
Workers AI, R2, D1, Hyperdrive, Durable Objects, Queues, Workflows를 비롯한 플랫폼 전반에 매끄럽게 연결할 수 있고,
FastAPI와 Django와 Flask 같은 인기 프레임워크를 Python Worker 안에서 돌릴 수 있으며,
Dynamic Workers로 Worker 안에서 또 다른 Python Worker를 만들 수도 있다.

기반은 WebAssembly다.
Workers가 2018년부터 WebAssembly를 지원해 왔기 때문에
Wasm으로 컴파일한 Python 인터프리터를 돌릴 환경이 이미 있었고,
Pyodide를 써서 넓은 범위의 Python 응용을 빠르게 지원할 수 있었다는 설명이다.

이 글은 발표문이지만 내용의 대부분이 어떻게 쓰는지에 대한 안내다.
그래서 아래는 그 안내를 실제로 쓸 수 있는 형태로 정리한 것이다.

## 바인딩을 파이썬답게 쓰기

이번 출시에서 가장 실질적인 변화는 여기다.
전에는 Cloudflare 바인딩을 쓰려면 RPC 경계에서 Python 객체를 TypeScript 객체로 명시적으로 변환해야 했다.
Python 사전을 Queue에 보내려면 이런 접착 코드가 필요했다.

```python
from pyodide.ffi import to_js
import js

self.env.QUEUE.send(to_js({"key": "value"}, dict_converter=js.Object.fromEntries))
```

발표문이 이 코드의 문제를 정확히 서술한다.
Python Worker를 쓰면서도 JavaScript 환경과 코드를 계속 염두에 두어야 했고,
사람에게도 AI 에이전트에게도 흔한 오류의 원인이었다는 것이다.
그래서 타입 변환 전체를 Workers 런타임과 Python SDK 안으로 넣었고, 이제는 이렇게 쓴다.

```python
self.env.QUEUE.send({"key": "value"})
```

이 변화의 값어치는 줄 수가 아니라 알아야 할 것의 수에 있다.
앞의 코드를 쓰려면 `to_js`가 무엇이고 `dict_converter`가 왜 필요하며
`js.Object.fromEntries`가 어떤 모양을 만드는지 알아야 한다.
뒤의 코드는 Python만 알면 된다.

## 웹 프레임워크 올리기

FastAPI 같은 비동기 응용은 `workers.asgi`로 연결한다.

```python
from fastapi import FastAPI
from workers import WorkerEntrypoint, asgi

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)

# 위와 같은 뜻
Default = asgi.entrypoint(app)
```

Django 같은 동기 응용은 `workers.wsgi`를 쓴다.

```python
from workers import WorkerEntrypoint, wsgi
from your_django_app.wsgi import app

Default = wsgi.entrypoint(app)
```

작동 방식에 대한 설명이 이 절에서 가장 배울 만한 부분이다.
Python에는 웹 응용이 웹 서버와 어떻게 통신할지에 대한 표준 규약이 있고,
그것이 WSGI와 그 비동기 판본인 ASGI다.
이 표준 덕에 응용은 서버에 완전히 독립적으로 만들어질 수 있다.
전통적인 배포에서는 Uvicorn이나 Gunicorn 같은 웹 서버가 동시 연결과 스레드를 다루며 트래픽을 감당하고,
FastAPI 같은 프레임워크는 응용 논리에만 집중한다.

Cloudflare Workers에서는 플랫폼 자체가 웹 서버다.
전역 네트워크가 이미 부하 분산과 무한 확장을 처리하므로 Python Worker 안에서 서버를 또 돌릴 이유가 없다.
그래서 `workers.asgi`와 `workers.wsgi` 연결기는 얇고 최적화된 다리 역할만 한다.
들어온 네이티브 JavaScript 요청을 Python 응용이 기대하는 표준 WSGI 및 ASGI 구조로 번역하고,
응답을 최소 오버헤드로 다시 내보낸다.

여기서 알아 둘 실무적 함의가 있다.
이 연결기는 WSGI나 ASGI 인터페이스를 쓰는 어떤 Python 웹 프레임워크에도 쓸 수 있다.
프레임워크별 지원이 아니라 규약에 대한 지원이므로,
목록에 없는 프레임워크를 쓴다면 그것이 ASGI나 WSGI를 따르는지만 확인하면 된다.

## 관계형 데이터베이스 붙이기

Hyperdrive 연동이 이번 출시에서 기술적으로 가장 깊은 부분이다.

문제부터 보면 이유가 분명하다.
전에는 Python Workers가 TCP 소켓을 지원하지 않아 데이터베이스 드라이버를 쓸 수 없었다.
`aiomysql`이나 `asyncpg` 같은 드라이버는 표준 라이브러리의 `socket` 모듈에 기대고,
그 모듈은 보통 환경에서 운영체제에 POSIX 시스템 호출을 한다.
WebAssembly 샌드박스 안에서 그 POSIX 네트워킹 시스템 호출은 대개 언제나 실패하는 빈 껍데기이므로,
표준 소켓을 열려는 어떤 시도도 즉시 실패했다.

해법은 Workers의 `connect` API로 소켓 시스템 호출을 구현한 것이다.
드라이버가 TCP 연결을 열려고 하면 이 맞춤 소켓 시스템 호출 구현을 거치고,
그것이 연결 열기나 바이트 읽기 같은 표준 Python 소켓 연산을
Workers 런타임이 쓰는 JavaScript 호출로 번역한다.
번역이 시스템 호출 수준에서 일어나므로 드라이버는 아래 구현을 전혀 알 필요가 없다.

이 설계가 좋은 이유는 번역 지점이 아래쪽에 있기 때문이다.
드라이버마다 고치는 대신 모든 드라이버가 공유하는 계층 하나를 고쳤다.

쓰는 법은 이렇다.
먼저 Wrangler 설정에 바인딩을 넣는다.

```json
"hyperdrive": [
  {
    "binding": "HYPERDRIVE_MYSQL",
    "id": "57b7076f58be42419276f058a8968187"
  }
]
```

그다음 익숙한 드라이버로 연결한다.

```python
import aiomysql
from workers import WorkerEntrypoint

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        hd = self.env.HYPERDRIVE_MYSQL
        conn = await aiomysql.connect(
            host=hd.host,
            port=int(hd.port),
            user=hd.user,
            password=hd.password,
            db=hd.database,
            ssl=None,
        )
        cur = await conn.cursor()
        await cur.execute("SELECT username FROM user")
        r = await cur.fetchall()
        await cur.close()
        conn.close()
```

바인딩이 호스트와 포트와 자격 증명을 속성으로 넘겨주므로 연결 문자열을 따로 관리하지 않는다.

## 패키지 생태계와 PEP 783

Python Workers가 WebAssembly 샌드박스 안에서 돌기 때문에,
C나 C++이나 Rust 네이티브 확장을 가진 패키지는 WebAssembly로 교차 컴파일되어야 한다.
그런데 Python 패키지를 WebAssembly로 교차 컴파일하는 표준 방법이 없었고,
그래서 Cloudflare 팀이 직접 컴파일해 호스팅해야 했으며 쓸 수 있는 패키지 수가 크게 제한되었다.

이 문제를 푸는 방식이 이 발표에서 가장 눈여겨볼 선택이다.
Python Workers에서만 쓸 수 있는 패키지를 만드는 것은 공동체에 도움이 되지 않으므로,
Pyodide와 Python의 WebAssembly 공동체 전체에 이득이 되는 방향으로 생태계가 자라기를 원했다는 것이다.
그래서 브라우저 런타임에서 Python을 돌리는 플랫폼을 표준화하는 PEP 783을 제안했고,
1년 넘는 논의와 다듬기 끝에 받아들여졌다.
이름이 PyEmscripten이며, 패키지 관리자들이 이 플랫폼용으로 빌드하고 배포하면
PyEmscripten을 구현하는 모든 환경에서 쓸 수 있게 된다.

함께 한 일이 셋 더 있다.
기존 Pyodide 빌드 도구 사슬을 안정화해 모든 패키지 관리자가 접근할 수 있는 형태로 발전시킨 것,
`cibuildwheel`에 PyEmscripten 플랫폼 지원을 더한 것,
그리고 주요 패키지 관리자들과 직접 협력해 PyEmscripten 빌드를 추가하는 것이다.
지원되지 않는 패키지를 만나면 알려 달라고 적혀 있다.

## HTTP 클라이언트와 AI 라이브러리

`openai`와 `langchain` 같은 라이브러리는 `requests`나 `httpx` 같은 HTTP 클라이언트로 외부 API와 통신하는데,
저수준 소켓 연산 지원이 없어 이 클라이언트들이 제대로 작동하지 않았다.
발표문은 이 클라이언트들이 WebAssembly 환경에서 JavaScript `fetch` API로 요청을 직접 보내도록
상류에 기여했다고 적는다.
그것과 앞 절의 저수준 소켓 지원을 합쳐 네트워킹 스택 전체가 Python Workers 안에서 매끄럽게 작동하게 되었다는 것이다.

결과로 `openai`와 `langchain`과 `mcp`를 Python Workers에서 그대로 쓸 수 있고,
Workers AI와 결합해 Cloudflare 네트워크의 GPU에서 서버리스 추론을 돌리거나 AI Gateway로 요청을 보낼 수 있다.

```python
from langchain_cloudflare import ChatCloudflareWorkersAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from workers import Response, WorkerEntrypoint

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        prompt = PromptTemplate.from_template(
            "In one sentence, describe a great day in the life of an {profession}."
        )
        llm = ChatCloudflareWorkersAI(
            model_name="@cf/meta/llama-3.3-70b-instruct-fp8-fast",
            binding=self.env.AI,
            max_tokens=64,
        )
        chain = prompt | llm | StrOutputParser()
        result = await chain.ainvoke({"profession": "electrician"})
        return Response.json({"result": result})
```

이 절의 상류 기여에 대한 서술이 뒤에서 가장 크게 반박받는 대목이다.

## 무엇을 만들 수 있는가

발표문이 든 사례들이 조합의 형태를 보여 준다.
이미지 대 이미지 생성기를 순수 Python Workers로 만드는 예에서는
사용자 요청을 받아 Queue에 넣고 Workflows가 Workers AI로 생성 단계를 조율한 뒤 R2 버킷에 저장한다.
Bluesky Jetstream WebSocket에 연결해 실시간 사건 흐름을 소비하는 예에서는
Durable Object로 그 연결을 뒷받침해 오래 사는 상태를 유지하고 WebSocket 연결이 끊기지 않게 한다.
그 밖에 공식 Python MCP 패키지로 MCP 서버를 만드는 예와
Workers AI와 Vectorize로 검색 증강 생성 체계를 만드는 예가 있다.

문서 쪽 변화도 함께 적혀 있다.
TypeScript로 무언가를 하는 방법을 보여 주는 코드 예제가 있는 거의 모든 곳에 Python 예제도 함께 넣었고,
개발자 문서 전반에서 JavaScript와 TypeScript와 Python 사이를 전환할 수 있다는 것이다.

## 함정

이 발표문이 말하지 않은 것들이 반응에서 채워졌다.

찬 시작 시간이 발표에 없다.
WebAssembly 기반 런타임에서 가장 먼저 묻게 되는 값인데 정식 출시 발표에 수치가 없다.
stefan_lec가 정확히 그것을 물었다.
WebAssembly를 Workers에 쓸 때의 단점 중 하나가 더 긴 기동 시간이었던 것으로 기억하는데
그것을 우회할 방법을 찾아냈는지 궁금하다는 것이다.[^stefan_lec]

Pyodide 판본이 고정된다.
쓸 수 있는 Python 판본이 workerd가 내장한 Pyodide 판본 하나로 정해지며 사용자가 고를 수 없다.
appveyor가 지금 어느 판본인지 물었고, 자기가 마지막으로 확인했을 때는 0.28.x였다고 적는다.[^appveyor]
장기 운영에서 이 제약은 의존성 계획에 직접 영향을 준다.

네트워킹과 이벤트 루프의 의미론이 원본과 다르다.
HTTP 요청이 실제 네트워크 스택이 아니라 JavaScript `fetch`로 내려가고, 비동기 이벤트 루프도 JavaScript 것으로 대체된다.
실무적으로는 같은 코드가 로컬에서와 Workers에서 다르게 동작할 수 있다는 뜻이며, 비평 절에서 다룬다.

문서 링크가 깨져 있었다.
pastrami_panda가 예제 페이지가 전부 404를 돌려준다고 적었다.[^pastrami_panda]
발표 직후의 일시적 문제일 수 있지만, 예제 저장소를 주요 근거로 제시하는 발표에서는 확인해 볼 값이다.

## 비평

### 상류에 기여했다는 서술과 유지보수를 떠안은 쪽의 설명이 다르다

발표문은 HTTP 클라이언트가 WebAssembly 환경에서 `fetch`로 요청을 보내도록 상류에 기여했다고 한 줄로 적는다.
그 문장에 대해 urllib3 유지보수자가 직접 맥락을 덧붙였다.

illia-v는 urllib3가 몇 년 전 Pyodide 및 Emscripten 지원을 더하는 큰 기여를 받아 병합했고
이후 JSPI 지원도 들어와 그것이 Requests에서 이 기능이 작동하게 만든 것이라고 설명한다.[^illia-v]
그리고 핵심 문장이 이어진다.
자기가 아는 한 이 작업에 대한 자금은 그것을 구현한 외부 기여자에게 갔고 urllib3 유지보수자들에게 가지 않았다는 것이다.
자기들은 변경을 검토하고 병합했으며, 이제 그 결과물인 백엔드의 유지보수는 프로젝트의 책임이 되었다.

왜 이것이 중요한지도 구체적으로 적는다.
Emscripten 백엔드는 urllib3에서 아직 실험적으로 간주되며 보안 정책의 적용 범위에서 명시적으로 빠져 있다.
그리고 실제로 겪은 문제의 예로 CVE-2025-50182를 든다.
요청이 `fetch`를 통해 흐를 때 urllib3의 리디렉션 통제가 기대한 대로 동작하지 않았다는 것이다.
브라우저와 `fetch`의 네트워킹 의미론이 urllib3의 일반 백엔드와 꽤 다르므로
이런 차이가 더 많이 있을 수 있다고 덧붙인다.
그리고 맺는 문장이 이 지적의 요지다.
그 작업이 상류에 기여되어 Pyodide와 Cloudflare에 유용한 것은 기쁘지만,
상류 프로젝트에 대한 기여에 자금을 대는 것과
그것을 나중에 지원해야 하는 상류 유지보수자들에게 자금을 대는 것 사이에는 의미 있는 차이가 있다는 것이다.

이 지적은 발표문이 거짓이라고 말하지 않는다.
상류에 기여한 것은 사실이다.
문제는 그 문장이 감추는 회계다.
기여의 비용은 일회성이고 유지보수의 비용은 계속되며, 후자가 받는 쪽으로 옮겨졌다.
그리고 그 결과물이 받는 쪽의 보안 정책 밖에 놓였다는 것은,
그 코드로 문제가 생겼을 때 책임질 주체가 정해지지 않은 상태라는 뜻이다.

[오픈소스에 아무도 돈을 내지 않는다는 글](../open-source/nobody-pays-for-open-source.md)에 대한 논의에서
상류로 가는 돈이 얼마냐는 물음이 나왔는데, 이 사례가 그 물음의 구체적인 형태다.
돈이 상류로 가긴 갔고, 유지보수자가 아니라 기여자에게 갔다.

같은 글타래에서 두 갈래 제안이 나왔다.
simonw는 Pyodide가 Python 생태계에서 아주 멋진 조각이라며
Cloudflare가 그쪽으로 돈을 좀 보내는 것을 고려하기를 바란다고 적고 후원 링크를 붙인다.[^simonw]
meagher는 다른 각도를 제시한다.
상류 유지보수자 중 누가 Cloudflare가 지원 계약에 서명하지 않으면 병합을 막는 것을 고려해 본 적이 있느냐는 것이다.[^meagher]
헤쳐 나가기 쉬운 절차는 아니지만 사내에서 밀어 줄 사람을 찾으면 유지보수 자금을 받을 수 있으며,
중요한 의존성에 대해서는 기업들이 대체로 재정 지원 예산을 잡을 의사가 있고
다만 요청하는 방법과 절차를 알아야 한다는 조언이다.

### 의미론을 바꿔 호환성을 얻은 구조가 새로운 비호환을 만든다

이 발표의 기술적 성취는 모두 같은 형태다.
Python이 기대하는 인터페이스를 유지한 채 그 아래를 JavaScript 세계로 연결한 것이다.
소켓 시스템 호출을 `connect` API로 구현하고, HTTP 클라이언트를 `fetch`로 내려보내고,
WSGI와 ASGI 구조로 요청을 번역한다.

syrusakbary는 이 방식의 대가를 짚는다.[^syrusakbary-loop]
Pyodide와 Cloudflare가 HTTP 요청에 실제 네트워크 스택을 쓰지 않고 함수를 고쳐 JavaScript `fetch`를 쓰게 했으며,
Python의 비동기 이벤트 루프도 JavaScript 이벤트 루프를 쓰도록 고쳤다는 것이다.
그리고 그 결과가 호환성 문제라고 적는다.
JavaScript 이벤트 루프는 선점적이어서 비동기 함수가 기다리지 않아도 호출되는 반면,
Python은 게을러서 비동기 함수가 기다릴 때만 실행된다는 것이다.
자기 생각으로는 네트워크 의미론이 보존되어야 하며, 동작이 달라지면 문제가 생기기 시작한다고 맺는다.

이 지적이 urllib3 유지보수자의 취약점 사례와 정확히 같은 지점을 가리킨다.
리디렉션 통제가 기대대로 동작하지 않은 이유가 바로 `fetch`의 네트워킹 의미론이 다르기 때문이다.
즉 두 사람이 서로 다른 계층에서 같은 문제를 보고했다.
인터페이스를 유지한 채 구현을 바꾸면 인터페이스가 약속하던 성질 중 일부가 조용히 사라지고,
그 사라짐은 평상시에는 드러나지 않다가 경계 조건에서 드러난다.
그리고 보안 통제는 대부분 경계 조건에 있다.

이 문제는 설계 실수가 아니라 이 접근의 내재적 비용이다.
샌드박스 안에서 POSIX 소켓이 없는 이상 무언가로 대체해야 하고, 대체하면 의미론이 달라진다.
발표문이 이 비용을 한 번도 언급하지 않는다는 것이 비평의 대상이고,
특히 드라이버가 아래 구현을 전혀 알 필요가 없다는 서술은 그 비용을 정확히 반대로 표현한 것이다.
드라이버가 알 필요가 없다는 것이 장점인 동시에, 드라이버가 차이를 다룰 기회가 없다는 뜻이기도 하다.

### 정식 출시 발표에 찬 시작 수치가 없다

syrusakbary는 Wasmer에서 경쟁 제품을 만들고 있다고 먼저 밝힌 뒤,
2년 전 최초 출시 당시 자기가 남긴 피드백으로 돌아가 보았다고 적는다.[^syrusakbary]
패키지 지원 쪽에서 의미 있는 진전이 있었고 PyEmscripten이 PEP 783으로 표준화된 것이 특히 좋다고 인정한다.
그러면서 당시 제기한 주요 구조적 우려가 여전히 남아 있다고 말한다.
workerd가 내장한 Python 및 Pyodide 판본 하나에만 묶인다는 것,
그리고 구조적으로 JavaScript와 V8 세계에 묶여 있어 찬 시작 시간을 줄이려 할 때 어려움이 있을 수 있다는 것이다.

그리고 수치를 제시한다.
자기들이 올해 초 발표한 벤치마크에서 최소한의 Python 응용이
Wasmer Edge에서 약 60밀리초, Cloudflare Workers에서 약 900밀리초에 시작했다는 것이며,
그것이 2024년에 자기가 제기한 우려를 뒷받침한다고 적는다.
이 수치가 이제 몇 달 된 것이므로 그동안 Cloudflare가 크게 개선했기를 바란다고 덧붙인 뒤,
정식 출시 발표에 갱신된 찬 시작 수치가 들어 있지 않은 것 같다고 지적한다.
그리고 요청한다.
현재 p50과 p95 찬 시작 시간을 공유해 줄 수 있느냐,
가능하면 네이티브 사용자 패키지가 있는 경우와 없는 경우 둘 다,
예컨대 FastAPI를 쓰는 경우와 의존성이 전혀 없는 경우로 나눠 달라는 것이다.

경쟁사 사람의 요청이라는 점을 감안하더라도 이 지적은 타당하다.
정식 출시는 실험 단계가 끝났다는 선언이고, 실험과 운영을 가르는 값 중 하나가 찬 시작이다.
그리고 이 발표문은 앞으로의 계획에서 성능과 메모리 효율 개선을 언급하므로,
현재 값이 개선의 여지가 있는 상태라는 것을 스스로 인정하고 있다.
그렇다면 현재 값을 밝히는 것이 순서다.

## 기억할 원칙

### 상류에 기여했다는 진술은 누가 이후를 책임지는지까지 말해야 완결된다

기업이 오픈소스에 기여했다고 발표할 때 그 문장이 가리킬 수 있는 것은 여럿이다.
코드를 썼을 수도, 코드를 쓸 사람에게 돈을 냈을 수도, 유지보수 조직에 돈을 냈을 수도 있다.
세 가지의 비용과 효과가 크게 다른데 발표문에서는 대개 한 단어로 뭉뚱그려진다.

그리고 셋 중 마지막만이 받는 쪽의 부담을 늘리지 않는다.
앞의 둘은 코드를 늘리고, 코드가 늘면 유지보수 부담이 늘며, 그 부담은 기여자가 떠난 뒤에도 남는다.
urllib3 사례가 그 구조를 정확히 보여 준다.
기여는 병합되었고, 유지보수는 프로젝트의 책임이 되었고, 결과물은 그 프로젝트의 보안 정책 범위 밖에 놓였다.

여기서 나오는 규칙은 읽는 쪽과 쓰는 쪽 모두에 적용된다.
읽는 쪽은 기여했다는 문장을 보면 그 코드를 지금 누가 유지보수하는지,
그 유지보수에 자금이 붙어 있는지, 그리고 그것이 프로젝트의 지원 범위 안인지를 물어야 한다.
특히 마지막 항목은 그 기능을 운영에 쓰려는 사람에게 직접적인 정보다.
실험적이고 보안 정책 밖이라면, 그 경로로 들어온 요청의 보안 통제를 스스로 검증해야 한다.

쓰는 쪽에서는 문장을 나누는 것만으로 정직해진다.
구현에 자금을 댔다고 쓰고, 유지보수에 대해서는 별도로 쓰는 것이다.
둘 중 하나만 했다면 그것도 그대로 쓰면 된다.
뭉뚱그린 문장은 짧은 기간 좋게 읽히고, 유지보수자가 같은 글타래에 나타나면 그 반대가 된다.

### 인터페이스를 유지한 채 구현을 갈아 끼우면 경계 조건이 계약에서 빠진다

이 발표의 기술적 내용은 거의 전부 같은 형태의 성취다.
Python이 기대하는 인터페이스를 그대로 두고 그 아래 구현을 JavaScript 세계의 것으로 바꾼 것이다.
소켓과 HTTP와 이벤트 루프와 타입 변환이 모두 그렇다.
이 방식의 장점은 명확하다.
기존 코드와 기존 라이브러리가 고치지 않고 작동한다.

그런데 인터페이스가 약속하는 것은 함수 이름과 인자 모양만이 아니다.
호출 순서, 오류가 나는 조건, 재시도와 리디렉션의 처리, 동시성의 의미론도 계약의 일부다.
이런 것들은 문서에 적혀 있지 않고 구현에 들어 있는 경우가 많으며,
그래서 구현을 갈아 끼울 때 함께 갈아 끼워지지 않는다.

urllib3의 리디렉션 통제가 `fetch` 경로에서 기대대로 동작하지 않은 것,
그리고 Python의 게으른 비동기와 JavaScript의 선점적 이벤트 루프가 다르다는 지적이 각각 그 사례다.
두 경우 모두 평상적인 호출에서는 아무 문제가 없다.
차이는 경계에서만 드러나고, 보안 통제와 동시성 버그는 경계에 산다.

그래서 이런 이식을 쓸 때 해야 할 일이 정해진다.
잘 작동한다는 것을 확인하는 시험이 아니라, 잘 작동하지 않아야 할 때 제대로 실패하는지를 확인하는 시험이다.
리디렉션을 따라가면 안 되는 경우, 시간 초과가 나야 하는 경우,
동시 요청이 서로를 간섭하면 안 되는 경우를 자기 환경에서 직접 확인해야 한다.
이식 계층의 문서가 그 목록을 주지 않으므로 목록을 스스로 만들어야 하고,
만들지 않으면 원본 구현의 안전 성질을 그대로 물려받았다고 가정하게 된다.

### 정식 출시라는 선언은 실험과 운영을 가르는 수치를 함께 내놓을 때 의미를 갖는다

정식 출시 발표가 실제로 바꾸는 것은 기능이 아니라 기대다.
읽는 사람은 이제 이것을 운영에 써도 된다는 뜻으로 받아들인다.
그렇다면 운영 판단에 필요한 값이 그 발표에 있어야 한다.

이 발표에는 기능 목록과 예제 코드가 풍부하고 운영 값이 없다.
찬 시작 시간, 메모리 사용량, 동시 실행 한도, 고정된 Pyodide 판본과 그 갱신 주기가 그 목록이다.
앞으로의 계획에서 성능과 메모리 효율 개선을 언급하므로 현재 값이 개선 대상이라는 것은 알 수 있는데,
그 값이 얼마인지는 알 수 없다.

이 공백이 특히 눈에 띄는 이유는 이 발표가 놓인 경쟁 구도 때문이다.
같은 작업을 다른 방식으로 하는 제품들이 있고, 그들이 내세우는 지표가 정확히 찬 시작 시간이다.
경쟁사 사람이 자기 벤치마크 수치를 들고 나타나 p50과 p95를 요청한 것이 그 결과다.
자기 수치를 내놓지 않으면 남의 수치가 그 자리를 차지한다.

일반적으로, 어떤 것을 운영 준비 완료라고 선언할 때 함께 적어야 할 것은 그 판단의 근거가 된 측정이다.
근거 없이 선언하면 그 선언은 홍보가 되고,
근거와 함께 선언하면 읽는 사람이 자기 조건에서 그 판단을 다시 할 수 있다.
그리고 후자만이 도입 결정을 실제로 돕는다.

---

[^illia-v]: <https://news.ycombinator.com/item?id=49792257>

[^simonw]: <https://news.ycombinator.com/item?id=49791438>

[^meagher]: <https://news.ycombinator.com/item?id=49796855>

[^syrusakbary]: <https://news.ycombinator.com/item?id=49792380>

[^syrusakbary-loop]: <https://news.ycombinator.com/item?id=49794605>

[^stefan_lec]: <https://news.ycombinator.com/item?id=49789663>

[^appveyor]: <https://news.ycombinator.com/item?id=49794487>

[^pastrami_panda]: <https://news.ycombinator.com/item?id=49791444>
