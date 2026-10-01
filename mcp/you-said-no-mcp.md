# MCP를 거부하던 Pi가 MCP를 코어에 넣은 이유: Codemode라는 조건

원문: [“You Said No MCP!” | Earendil](https://earendil.com/posts/you-said-no-mcp/)

HN 토론: <https://news.ycombinator.com/item?id=49906637> (617점, 344개 댓글)

GN 토론: <https://news.hada.io/topic?id=34545>

## 요약

Earendil Engineering이 2026년 9월 29일 공개한 글이다.
Pi는 한때 pi.dev에서 MCP를 지원하지 않는다고 자랑스럽게 밝혔고, 팟캐스트에서도 MCP를 깎아내리는 말을 여러 번 했으며, Mario가 MCP가 필요 없다면 어떨까라는 글까지 썼다.
그런데 지금 Pi를 업그레이드하면 MCP가 지원된다.
글은 무엇이 바뀌었는지를 설명한다.

첫째 이유는 세상이 정적이지 않다는 것이며, 글은 Armin Ronacher의 2016년 글로 이를 연결한다.
지난 1년 사이 MCP는 예전의 MCP가 아니게 되었다.
하지만 그것만으로 코어에 넣을 이유는 되지 않았고, 실제로 MCP는 이미 `pi-mcp-adapter`라는 확장으로 쓸 수 있었다.
코어에 넣은 진짜 이유는 MCP에 필요한 변경이 일반적으로도 쓸모 있었기 때문이다.
예를 들어 그 변경은 Pi 안에서 Jev를 더 쉽게 쓰게 해 주며, 결국 Pi에 필요한 것과 MCP에 필요한 것은 같았다.
인터프리터 형태의 샌드박스다.

MCP의 가장 큰 문제는 여전히 조합하기 어렵다는 점이다.
글은 이것을 MCP 자체보다 MCP 서버들과 하네스들의 접근 방식 문제로 본다.
많은 MCP 서버가 도구를 문맥에 쏟아붓는 하네스에 맞춰, 토큰을 아끼려고 텍스트를 반환한다.
Earendil은 MCP가 지능적인 도구 발견을 갖춘 OpenAPI에 가까워야 한다고 본다.
도구는 구조화된 데이터를 반환하고, 문서와 설명으로 발견될 수 있어야 한다.
CLI가 잘 동작하는 이유는 에이전트가 효율적인 셸 관용구로 도구를 엮기 때문인데, MCP도 그렇게 못할 이유가 없으며, Pi의 MCP는 Codex처럼 도구를 JavaScript 샌드박스에 노출하는 방식으로 만들었다.

왜 MCP 없이 Codemode만 하지 않았느냐는 질문에는 Pi의 도구 구성 방식이 답이다.
최근 Pi는 지연 도구 로딩, 대화 중 시스템 메시지, 추론 수준 변경을 지원하는 모델에 맞게 손봤지만, 도구 구성은 아직 그 능력에 맞게 확장하지 않았다.
Codemode에서는 도구가 LLM에게 직접 보일지, Codemode 안에서만 쓰일지 정해야 하는데, 일반 MCP 확장은 그 판단에 필요한 메타데이터를 Pi의 도구 구성에서 얻을 수 없었다.
그래서 도구를 지연 로딩하거나 Codemode 전용으로 설정할 수 있게 했다.
글은 무언가에 긍정적으로 영향을 주는 가장 좋은 방법은 그것을 받아들이는 것이라며, 작은 하네스에서도 잘 동작하도록 대화에 참여하겠다고 말한다.

Codemode는 하네스가 도구를 실행하는 두 위치 중 bash가 도는 쪽이 아니라 에이전트 루프가 도는 쪽에서 실행된다.
하네스 루프는 대개 신뢰할 수 있는 환경에서 돌고, 그것이 실행하는 도구는 신뢰가 낮은 샌드박스에서 돈다.
Codemode는 도구 호출을 조율하는 장치로, 에이전트가 JavaScript로 호출 순서를 정하고 결과를 엮게 하며, 상태는 파일 시스템이 아니라 세션 기록에 남는다.
JavaScript를 고른 이유는 작은 구현을 WASM 바이너리로 배포해 적당한 보호를 줄 수 있기 때문이다.
MCP를 설정하면 Codemode가 자동으로 로드되고, 기본 도구로 켤 수도 있다.
글은 Linear MCP로 열린 이슈 167개를 가져와 Jev로 댓글의 짜증 정도를 분류하는 세션을 예로 보여 준다.
결과는 중립 156개, 약간 짜증 11개, 매우 짜증 0개였고, 판정 결과는 Codemode 안에 저장되어 이슈를 다시 가져오지 않고도 이어서 살펴볼 수 있다.

## 분석

### 확장으로 충분했던 것을 코어로 올린 진짜 이유는 MCP가 아니다

글의 구조는 제목과 반대 방향으로 움직인다.
제목은 MCP를 받아들인 이유를 묻지만, 본문의 답은 MCP가 아니라 Codemode다.
MCP는 이미 확장으로 쓸 수 있었고, 글 스스로 MCP가 여전히 조합하기 어렵다고 인정한다.
코어로 올라간 것은 도구를 지연 로딩하거나 Codemode 전용으로 표시하는 메타데이터, 그리고 하네스 쪽에서 도는 JavaScript 샌드박스다.

HN에서 Armin Ronacher(the_mitsuhiko)는 Codemode가 bash와 다른 문제를 푼다고 설명했다[^the_mitsuhiko-codemode].
bash는 에이전트가 bash라는 도구 하나를 실행하는 방법이고, Codemode는 LLM이 하네스 수준의 도구들을 조율하는 방법이라는 것이다.
그리고 지금 이 일이 벌어지는 이유로, 연구소들의 모델이 점점 이 방식으로 학습되고 있으며 Codex의 한 API는 병렬 도구 호출에 Codemode를 요구한다고 덧붙였다.
즉 MCP 지원은 결과이고, 원인은 모델이 도구를 쓰는 방식의 변화다.

### 신뢰 경계가 bash와 Codemode를 가른다

글에서 가장 중요한 문장은 도구를 실행하는 두 위치의 신뢰 수준이 다르다는 설명이다.
bash는 신뢰가 낮은 샌드박스에서 돌고, Codemode는 신뢰할 수 있는 하네스 쪽에서 돈다.
이 차이가 왜 MCP와 Codemode가 함께 와야 하는지를 설명한다.
MCP 서버의 OAuth 토큰과 자격 증명은 하네스가 가지고 있으므로, 그 도구를 엮는 스크립트도 하네스 쪽에서 돌아야 한다.

HN의 mijoharas는 이 경계를 자기 운영 방식으로 설명했다[^mijoharas].
bash 도구는 네트워크에 닿지 못하는 제한된 샌드박스에서 돌리고, 자격 증명은 에이전트가 아니라 하네스만 만지게 한다는 것이다.
CLI를 선호하지만 일부 CLI는 비밀을 써야 접근할 수 있고, 그 비밀을 하네스에만 두면 문제가 풀린다.
nextaccountic은 같은 점을 권한 모델 쪽에서 짚었다[^nextaccountic].
bash는 셸이 가진 권한을 그대로 물려받으므로 CLI로 MCP를 쓰면 에이전트가 키에 접근하게 되기 쉽고, 흔히 쓰는 명령어 정규식 매칭 방식의 허용 목록은 에이전트가 인터프리터에 접근하는 순간 쉽게 뚫린다.
Python이나 JavaScript로 도구를 호출하게 하면 그 대신 실제 권한 체계를 둘 수 있다는 것이다.
magnio는 Codemode를 JSON 도구 호출과 bash 사이의 중간 지점으로 정리했다[^magnio].
직접 도구 호출은 오류를 일찍 잡고 출력을 통제하며 격리되지만 힘이 약하고, bash는 강하지만 오류가 실행 시에야 드러나고 출력이 문맥을 어지럽히며 기본 보안이 없다.

### 1년 사이 바뀐 것은 MCP의 기본 전송과 인증이다

글은 오늘의 MCP가 예전의 MCP가 아니라고만 쓰고, 무엇이 바뀌었는지는 구체적으로 적지 않는다.
HN의 댓글들이 그 공백을 채웠다.
bmurphy1976은 8개월 전 MCP는 헤더, `.env` 파일, 로컬 npm 프록시를 만져야 했지만, 지금은 완전히 원격이고 상태가 없으며 OAuth가 되고 버튼 하나로 연결된다고 썼다[^bmurphy1976].
CharlieDigital은 상태 없는 HTTP 모드가 3월에도 있었고, 2026-07-28 개정판 스펙이 그것을 주된 방향으로 삼았을 뿐이라고 짚었다[^CharlieDigital].

이 변화의 의미는 MCP가 누구의 도구인가에 있다.
로컬 stdio 서버 시절의 MCP는 개발자가 직접 띄우는 프로세스였고, 그렇다면 CLI가 더 단순했다.
원격, 상태 없음, OAuth가 기본이 되면 MCP는 SaaS가 자기 데이터에 들어오는 공식 문이 된다.
rcarmo가 기업 통합의 90%가 MCP 기반이고 MCP가 제3자 에이전트에게 사실상 필수인 보안과 인증 경계가 되었다고 한 것도 같은 이야기다[^rcarmo-enterprise].

## 비평

### OpenAPI에 가까워야 한다는 결론은 MCP의 존재 이유를 되묻게 한다

글은 MCP가 지능적인 도구 발견을 갖춘 OpenAPI에 가까워야 하며, 구조화된 데이터를 반환하고 문서로 발견되어야 한다고 말한다.
HN에서 abtinf는 OpenAPI가 바로 구조화된 데이터를 반환하고 문서와 설명으로 발견되는 것이라며 이 문장을 정면으로 비판했다[^abtinf].
mikeocool은 OAuth2를 지원하는 API의 OpenAPI 명세만 있으면, 하네스가 인증 흐름을 처리하고 토큰을 저장하고 요청 도구를 문맥에 넣는 세계가 가능했다고 썼다[^mikeocool].

물론 반론도 있다.
crooked-v는 데스크톱 클라이언트 전반에서 동작하는 하나의 잘 정의된 OAuth 흐름, 그 흐름을 쓰는 임베디드 위젯, 모델 통제 밖의 사용자 결정 지점 같은 것은 단순한 API 왕복으로 처리되지 않는다고 답했다[^crooked-v].
그러나 글은 이 반론을 스스로 하지 않는다.
MCP가 OpenAPI와 무엇이 다르기에 받아들일 가치가 있는지 설명하지 않고, 차라리 OpenAPI처럼 되어야 한다고 말하면, 독자는 왜 MCP를 받아들이는지가 아니라 왜 MCP가 필요한지를 묻게 된다.

### 조합의 어려움을 진단하고 그 내용을 비워 둔다

글은 MCP의 가장 큰 문제가 조합하기 어렵다는 점이며, Codemode로도 완전히 해결되지 않는다고 쓴다.
그런데 무엇이 조합되지 않는지는 말하지 않는다.
HN의 andrewingram은 지난주 Twitter에서 MCP가 조합되지 않는다는 말을 많이 봤지만 누구도 그것이 구체적으로 무슨 뜻인지 설명하지 않는다며, Codemode에서 남은 틈이 무엇이냐고 물었다[^andrewingram].

추론할 수 있는 단서는 있다.
Guillaume86은 MCP 서버마다 자기 Codemode 샌드박스를 두면 서로 다른 서버의 도구를 한 스크립트에서 부를 수 없고, Pi는 하네스가 샌드박스를 가져 그 문제를 우회한다고 봤다[^Guillaume86].
글이 말하는 서버들이 텍스트를 반환한다는 문제도 같은 방향이다.
텍스트를 반환하는 도구는 스크립트가 다음 도구의 입력으로 넘길 수 없다.
이 두 가지가 글이 말한 조합의 실제 내용이라면, 글은 문제의 대부분을 MCP 서버 작성자에게 넘긴 셈이고, Pi가 그것을 어떻게 바꾸려는지는 대화에 참여하겠다는 말 외에는 없다.

### 최소주의 하네스라는 약속이 조용히 바뀐다

Pi의 정체성은 작고 확장 가능한 하네스였다.
글은 MCP가 확장으로 충분했다고 인정하면서도, 필요한 메타데이터 때문에 코어로 올렸다고 설명한다.
HN에서 skohan은 Codemode를 코어 편집기에 넣는 것이 Pi의 최소주의라는 장점과 맞지 않는다고 했고[^skohan], spence-s는 Pi가 이 하네스는 당신의 것이라는 말에서 Armin과 Mario의 좋은 하네스에 대한 의견으로 바뀌고 있다고 비판했다[^spence-s].

Armin은 기본으로 새로 로드되는 것은 없으며 군살을 늘리는 것은 전혀 계획이 아니라고 답했다[^the_mitsuhiko-cruft].
하지만 핵심은 기본값이 아니라 구조다.
하네스를 만드는 dpc_01234는 Codemode가 하네스 내부 동작을 완전히 바꾸고 다른 모든 것으로 번지므로, 요즘 잘 동작하는 수준의 통합은 이 하네스는 당신의 것이라는 철학과 맞지 않는다고 썼다[^dpc_01234].
ricericerice는 Earendil이 자체 추론 공급자를 만들고 있다는 점까지 더해, 프로젝트가 사람들이 기대한 최소 플랫폼에서 멀어질 위험이 있다고 지적했다[^ricericerice].
글은 이 정체성 변화를 다루지 않고, 세상은 정적이지 않다는 문장 하나로 넘어간다.

## 인사이트

### 강한 반대 의견은 근거가 낡은 뒤에도 정체성으로 남는다

글이 인용한 Armin Ronacher의 2016년 글은 무언가를 싫어할 때 조심하라는 내용이다.
HN의 gk1은 그 글에서, 강한 의견을 마주하면 그 논의의 근거가 이미 오래전에 낡았거나 더는 관련이 없는 경우가 많다는 대목을 인용했다[^gk1].
Pi의 MCP 반대는 정확히 그런 궤적을 밟았다.
MCP가 로컬 프로세스와 도구 덤프였던 시절의 반대는 합리적이었지만, 원격과 OAuth와 지연 로딩이 기본이 된 뒤에도 pi.dev 첫 화면의 아이콘으로 남아 있었다.

이 사례가 흥미로운 것은 반대가 제품 정체성의 일부였다는 점이다.
NichoPaolucci는 MCP 미지원이 Pi 첫 화면의 첫 아이콘이었다고 짚었다[^NichoPaolucci].
기술적 판단이 마케팅 문구가 되면, 근거가 바뀌어도 판단을 바꾸는 비용이 커진다.
Earendil이 이 비용을 공개적으로 치렀다는 점은 높이 살 만하지만, 같은 함정은 CLI 대 MCP 논쟁의 반대편에도 있다.
`mcp/mcp-is-dead-long-live-the-cli.md`가 정리한 3월의 MCP 사망론도 몇 달 만에 같은 질문 앞에 선다.

### 하네스의 경쟁 축이 도구 수에서 도구 조율로 옮겨 간다

Codemode가 코어 기능이 되는 흐름은 하네스 경쟁의 축이 바뀌고 있다는 신호다.
초기 하네스는 얼마나 많은 도구를 붙일 수 있느냐로 경쟁했고, 그다음은 문맥을 아끼기 위한 지연 로딩과 도구 검색이었다.
이제는 모델이 스크립트로 여러 도구를 엮어, 중간 결과를 문맥에 올리지 않고 처리하는 방식이 표준이 되어 간다.
글의 예시에서 이슈 167개와 댓글 수백 건이 문맥에 한 줄도 들어가지 않고 요약 결과만 돌아온 것이 그 효과다.

이는 데이터베이스가 걸어온 길과 닮았다.
초기에는 애플리케이션이 행을 하나씩 가져와 처리했고, 저장 프로시저와 서버 측 질의가 나온 뒤에야 데이터를 움직이지 않고 계산을 데이터 쪽으로 보내는 것이 표준이 되었다.
Codemode는 계산을 모델의 문맥에서 하네스의 샌드박스로 보내는 같은 전환이다.
그러면 하네스의 가치는 도구 목록이 아니라, 그 샌드박스가 얼마나 안전하고 얼마나 많은 도구를 하나의 스크립트에서 부를 수 있게 하느냐로 측정된다.

### 하네스 쪽 샌드박스는 새로운 신뢰 경계를 만든다

Codemode가 신뢰할 수 있는 하네스 쪽에서 돈다는 설계는 자격 증명 문제를 푼다.
동시에 새로운 질문을 만든다.
HN의 coder-pm은 그 JavaScript 샌드박스가 컨테이너인지, 별도 프로세스인지, 같은 Node 프로세스인지, MCP 토큰과 하네스 자격 증명에 접근할 수 있는지 물었다[^coder-pm].
Pxtl은 Codemode의 주된 가치가 높은 권한으로 MCP를 부르는 격리된 언어라는 보안이라면, 보안 모델이 없는 Pi에서 그 계획이 무엇이냐고 물었다[^Pxtl].

이 질문은 Pi만의 것이 아니다.
모델이 쓴 스크립트가 신뢰 영역에서 실행되고, 그 스크립트가 자격 증명을 가진 도구를 부를 수 있다면, 프롬프트 인젝션의 목표는 bash 샌드박스 탈출이 아니라 Codemode 스크립트에 원하는 도구 호출을 끼워 넣는 것이 된다.
WASM 격리는 스크립트가 호스트를 건드리지 못하게 막지만, 허용된 도구를 원치 않는 방식으로 부르는 것은 막지 못한다.
Codemode가 표준이 될수록, 하네스는 샌드박스 격리와 별개로 스크립트가 부르는 도구 호출 하나하나에 대한 권한 정책을 가져야 한다.

---

[^the_mitsuhiko-codemode]: <https://news.ycombinator.com/item?id=49907603>

[^mijoharas]: <https://news.ycombinator.com/item?id=49909465>

[^magnio]: <https://news.ycombinator.com/item?id=49907715>

[^bmurphy1976]: <https://news.ycombinator.com/item?id=49909949>

[^CharlieDigital]: <https://news.ycombinator.com/item?id=49907780>

[^rcarmo-enterprise]: <https://news.ycombinator.com/item?id=49907300>

[^abtinf]: <https://news.ycombinator.com/item?id=49908820>

[^mikeocool]: <https://news.ycombinator.com/item?id=49909373>

[^crooked-v]: <https://news.ycombinator.com/item?id=49910900>

[^andrewingram]: <https://news.ycombinator.com/item?id=49907846>

[^Guillaume86]: <https://news.ycombinator.com/item?id=49908143>

[^skohan]: <https://news.ycombinator.com/item?id=49908893>

[^spence-s]: <https://news.ycombinator.com/item?id=49908812>

[^the_mitsuhiko-cruft]: <https://news.ycombinator.com/item?id=49907562>

[^dpc_01234]: <https://news.ycombinator.com/item?id=49914907>

[^ricericerice]: <https://news.ycombinator.com/item?id=49911741>

[^gk1]: <https://news.ycombinator.com/item?id=49910371>

[^NichoPaolucci]: <https://news.ycombinator.com/item?id=49907054>

[^coder-pm]: <https://news.ycombinator.com/item?id=49908068>

[^Pxtl]: <https://news.ycombinator.com/item?id=49907798>

[^nextaccountic]: <https://news.ycombinator.com/item?id=49916646>
