# Docker Sandboxes: YOLO 모드를 기본값으로 만드는 microVM 격리

> Sandboxes for Coding Agents
>
> Run AI agents safely in local sandboxes.

<https://www.docker.com/products/docker-sandboxes/>

공식 문서: <https://docs.docker.com/ai/sandboxes/>

## 소개

Docker Sandboxes는 AI 코딩 에이전트를 microVM 안에서 격리해 실행하는 도구다.
제품 페이지의 첫 문장은 “AI 에이전트를 로컬 샌드박스에서 안전하게 실행하라”이고, 그 아래 부제가 대상을 명시한다.
Claude Code, Copilot CLI, Codex, OpenCode, Kiro처럼 안전한 무인 실행이 필요한 에이전트를 위한 일회용 격리 샌드박스라는 것이다.

CLI 이름은 `sbx`이며 설치는 세 플랫폼 모두 패키지 관리자로 끝난다.

```bash
# macOS
brew trust docker/tap && brew install docker/tap/sbx

# Windows
winget install Docker.sbx

# Linux (Ubuntu)
curl -fsSL https://get.docker.com | sudo REPO_ONLY=1 sh
sudo apt-get install docker-sbx
```

기본 사용은 프로젝트 디렉터리에서 `sbx run claude`를 실행하는 것이고, 그 전에 `sbx login`이 필요하다.
작업 공간을 여러 개 지정할 수 있으며 읽기 전용 표시도 붙는다.

```bash
sbx run claude ~/project-a ~/shared-libs:ro ~/docs:ro
```

### 제품 페이지가 내세우는 것

핵심 주장은 자율성과 안전이 더는 상충하지 않는다는 것이다.
“에이전트는 자유를 가질 때 가장 잘 일한다”고 적고, 샌드박스가 에이전트를 빠르게 달리게 하되 통제 밖으로 벗어나지는 않게 한다고 말한다.
통제 대상으로 파일 시스템, 네트워크, 자격 증명 세 가지를 든다.

역량 절의 제목은 “YOLO 모드를, 안전하게”다.
각 에이전트가 전용 microVM 안에서 실행되고 그 안에 개발 환경과 프로젝트 작업 공간만 마운트되며, 에이전트는 패키지를 설치하고 설정을 바꾸고 자체 Docker 컨테이너를 띄울 수 있고, 호스트는 그대로 남는다는 설명이다.
그리고 결론이 세 개의 부정문으로 이어진다.
수동 검토도, 권한 프롬프트도, 감독도 필요 없다는 것이다.

기능 목록 일곱 개 중 마지막 항목이 이 제품의 성격을 가장 잘 드러낸다.
`--dangerously-skip-permissions`가 기본값이라고 적혀 있다.
관대한 모드를 자신 있게 쓰라는 것이며, 실제로 그것이 기본값이라고 덧붙인다.

FAQ는 VM과의 차이를 이렇게 정리한다.
샌드박스는 microVM에서 완전히 격리되어 실행되므로 VM을 온전히 돌리는 비용을 치르지 않고도 더 많은 격리를 얻으며, 그래서 추가 Docker 컨테이너 실행처럼 더 많은 권한이 필요한 일을 안전하게 할 수 있다는 것이다.
Docker Desktop이 필요하냐는 질문에는 아니라고 답한다.

### 문서가 밝히는 구조

아키텍처 문서는 이 도구가 하이퍼바이저 기반 격리라고 명시하고 그 대가도 함께 적는다.
샌드박스는 완전한 격리를 얻는 대신 VM 하나와 그 자체 데몬이라는 더 높은 자원 부담을 치른다는 것이다.

작업 공간은 파일 시스템 패스스루로 직접 마운트되며 절대 경로가 보존되어 디버깅 시 경로가 호스트와 일치한다.
virtiofs 캐싱이 기본으로 켜져 있고 환경 변수로 끌 수 있다.
네트워크 아웃바운드는 전부 호스트 쪽 HTTP/HTTPS 프록시를 지나며, 이 프록시가 접근 정책을 강제하고 자격 증명을 주입한다.
`HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY`를 존중하고 `DOCKER_SANDBOXES_PROXY`로 경로를 바꿀 수 있으나 `proxy.pac` 같은 자동 설정 파일은 지원하지 않는다.
샌드박스마다 자체 Docker 데몬 상태와 이미지 캐시를 가지므로 이미지나 레이어를 공유하지 않으며, 호스트 쪽 에이전트 스킬 저장소만 선택적으로 공유한다.
상태는 `sbx rm`으로 지울 때까지 유지된다.

보안 문서는 신뢰 경계가 microVM이라고 분명히 밝힌다.
에이전트는 sudo를 포함해 VM 안에서 완전한 통제권을 가지며, VM 경계가 명시적으로 공유된 것 외에는 호스트의 무엇에도 닿지 못하게 막는다는 것이다.
격리 계층으로 다섯 가지를 든다.
하이퍼바이저 격리(샌드박스마다 별도 커널, 호스트와 메모리나 프로세스를 공유하지 않음), 네트워크 격리(호스트 프록시를 통한 기본 거부 정책, 비 HTTP 프로토콜은 전면 차단), Docker 엔진 격리, 선택적 작업 공간 격리(`--clone` 사용 시 저장소를 읽기 전용으로 마운트), 자격 증명 격리(API 키를 호스트 쪽 프록시가 HTTP 헤더에 주입하므로 원본 값이 VM에 들어오지 않음)다.

같은 문서가 막지 못하는 것도 명시한다.
직접 모드에서는 작업 공간 변경이 호스트에 그대로 반영되며, 에이전트가 Git 훅이나 CI 설정이나 `package.json` 스크립트처럼 암묵적으로 실행되는 파일을 고칠 수 있다.
기본 허용 도메인에 `*.googleapis.com` 같은 넓은 와일드카드가 들어 있다.
스킬을 공유하는 샌드박스들 사이에는 교차 격리의 좁은 예외가 생겨 한 샌드박스가 다른 샌드박스의 지시문을 바꿀 수 있다.
그리고 로컬 stdio MCP 서버는 샌드박스 VM 바깥에서 호스트 권한으로 실행된다.

## 분석

### 이 제품이 파는 것은 격리가 아니라 승인 프롬프트의 제거다

기술적으로 microVM 격리는 새롭지 않다.
Firecracker는 2018년부터 있었고 HN에서도 여러 사람이 그렇게 지적했다[^hn-rvz].
그런데도 이 페이지가 팔리는 이유는 격리 기술이 아니라 그 위에 얹힌 한 문장 때문이다.
`--dangerously-skip-permissions`가 기본값이라는 문장이다.

에이전트 도구를 쓰는 사람이 매일 지불하는 비용은 커널 탈출 위험이 아니라 권한 프롬프트다.
파일을 쓸 때마다, 명령을 실행할 때마다 확인을 요구받으면 무인 실행이 성립하지 않고, 그래서 사람들은 위험 표시가 이름에 그대로 들어 있는 플래그를 매일 쓴다.
이 제품은 그 플래그를 지우려 하지 않는다.
반대로 그것을 기본값으로 승격시키고, 대신 그 플래그가 위험하지 않은 환경을 판다.

이 배치가 마케팅 문구의 세 부정문으로 이어진다.
수동 검토도, 권한 프롬프트도, 감독도 필요 없다는 것인데, 이 셋은 모두 사람의 시간이다.
곧 이 제품이 실제로 파는 단위는 보안이 아니라 사람의 주의력이며, microVM은 그 주의력을 회수하기 위해 치르는 인프라 비용이다.
[Agent Safehouse](../security/agent-safehouse.md)가 “Go full `--yolo`. We've got you”라는 슬로건으로 같은 자리를 겨냥한 것도 우연이 아니다.

### 로그인 요구가 무엇을 드러내는가

HN 스레드에서 가장 반복된 반응은 기술적 반박이 아니라 로그인 요구였다.
“로그인 필요. 쓰레기”[^hn-laserlight]로 시작해, 로컬 개발 도구를 쓰는 데 로그인을 요구한다며 버즈워드로 된 이유는 됐다는 반응[^hn-pixard], 락인이 싫은 사람을 위해 자기 오픈 소스 대안을 내놓겠다는 글[^hn-binsquare]이 이어졌다.
호의적인 사용자들도 같은 지점에서 멈춘다.
Docker가 무게를 실으면 업계 전반의 채택과 통합이 좋아지리라 기대했다가 로그인 요구에서 실망했다는 반응[^hn-karakanb], 로그인 문제만 빼면 괜찮은 선택지라는 반응[^hn-aborsy], 오픈 소스 대안이 없어서 매일 쓰고 있다는 반응[^hn-rusch]이 모두 그렇다.

로그인이 왜 필요한지는 페이지 자체가 답한다.
FAQ와 각 절 끝마다 Docker AI Governance로 가는 링크가 붙어 있고, 그 제품이 파는 것이 네트워크 정책과 파일 시스템 규칙과 조직 전역 MCP 거버넌스를 한 번 정의해 어디서나 강제하는 능력이다.
정책은 직접 만들 수 있지만 그것을 강제하려면 구독이 필요하다는 설명이 스레드 안에도 나온다[^hn-dsebastien].

여기서 무료 제품과 유료 제품의 경계가 정확히 어디인지가 드러난다.
격리는 무료다.
강제는 유료다.
그리고 그 경계는 기술의 경계가 아니라 조직의 경계이며, 개발자 개인의 계정을 필요로 하는 이유도 강제할 대상을 세어야 하기 때문이다.

### 격리와 강제는 다른 문제라는 것을 스레드가 먼저 짚었다

스레드에서 가장 정확한 구분은 Docker가 아니라 독자에게서 나왔다.
샌드박스는 에이전트가 무엇을 할 수 있는지를 제한하지만 에이전트가 반드시 샌드박스 안에서 실행되어야 한다는 것을 강제하지는 않으며, 그 경계를 강제하려면 별도의 통제 계층이 필요하다는 지적이다[^hn-runtime].
같은 질문이 다른 형태로도 나왔다.
샌드박스를 쓰지 않고 호스트에서 바로 에이전트를 돌리는 것을 어떻게 막느냐, 머신에서 바이너리를 스캔하는 것 말고 방법이 있느냐는 것이다[^hn-dsebastien-enforce].

이 질문에 제품 페이지는 답하지 않는다.
답하는 것은 Docker AI Governance이고, 그래서 이 두 제품의 관계는 보완이 아니라 완성이다.
Sandboxes 혼자서는 규율이 있는 개인에게만 작동하며, 규율이 없는 개인이 있는 조직에서는 아무것도 보장하지 못한다.

이 구조가 보안 제품에서는 흔하다.
안티바이러스도, 디스크 암호화도, MDM도 같은 모양이다.
도구는 무료로 뿌리고 강제와 감사와 보고를 판다.
Docker가 컨테이너로 한 번 겪은 일이기도 하다.
런타임은 상품이 되었고 돈은 레지스트리와 데스크톱 라이선스와 조직 관리에서 나왔다.

### Linux를 제품 페이지에서 지운 선택

제품 페이지의 설치 절에는 macOS와 Windows와 Linux가 모두 있지만, “왜 샌드박스인가” 이후의 서술과 FAQ는 Linux를 사실상 언급하지 않는다.
HN에서 이 점이 여러 번 지적됐다.
페이지만 보면 Linux 지원이 없는 것처럼 읽힌다는 지적[^hn-cryptoz], 언젠가 Linux도 이 macOS/Windows 전용 기술을 지원하기를 바란다는 비꼼[^hn-hokkos], Docker에 대해 아는 모든 것에 비추어 그 누락이 이상하다는 반응[^hn-ethagnawl]이 그것이다.
답은 매번 같았다.
문서에는 있고, 마케팅 페이지가 그럴 뿐이라는 것이다[^hn-etoxin].

이 누락이 사소해 보이지만 대상 고객을 알려 준다.
Linux 개발자는 이미 `bubblewrap`이나 Incus나 QEMU로 같은 일을 하고 있고, 실제로 스레드의 상당 부분이 그 사람들의 자작 설정 자랑이다.
반대로 macOS와 Windows에서는 Docker가 이미 VM을 돌리고 있으므로 microVM 하나를 더 얹는 심리적 비용이 낮다.

곧 이 제품이 겨냥하는 사람은 격리를 직접 만들 수 없거나 만들고 싶지 않은 사람이며, 그 집단은 Linux보다 macOS와 Windows에 몰려 있다.
Linux 지원을 문서에만 둔 것은 실수가 아니라 그 판단의 반영으로 읽힌다.

## 비평

### “감독이 필요 없다”는 문장과 문서가 밝힌 구멍이 같은 제품 안에 있다

제품 페이지는 수동 검토도 권한 프롬프트도 감독도 필요 없다고 적는다.
그런데 같은 회사의 보안 문서가 감독이 필요한 자리를 네 군데 명시한다.

가장 큰 것은 로컬 stdio MCP 서버가 샌드박스 VM 바깥에서 호스트 권한으로 실행된다는 사실이다.
이것은 주변부 예외가 아니다.
MCP는 지금 에이전트에게 실제 능력을 주는 주된 통로이고, 파일 시스템 서버나 데이터베이스 서버나 브라우저 서버를 붙이는 순간 에이전트가 조종하는 실행 주체가 VM 밖에 생긴다.
VM 안의 에이전트가 VM 밖의 프로세스에 명령을 보낼 수 있다면 하이퍼바이저 경계는 그 통로에 대해 아무 의미가 없다.

두 번째는 직접 모드에서 작업 공간 변경이 호스트에 그대로 반영된다는 점이다.
문서는 Git 훅과 CI 설정과 `package.json` 스크립트를 예로 든다.
이것들의 공통점은 나중에 호스트에서 사람이 실행한다는 것이며, 곧 샌드박스는 즉시 실행을 막지만 지연 실행은 막지 못한다.
`--clone`을 쓰면 읽기 전용이 되지만 그것은 기본값이 아니고, 기본값이 아닌 안전 장치는 없는 것과 크게 다르지 않다.

세 번째가 기본 허용 도메인의 넓은 와일드카드다.
문서는 기본 거부 정책이라고 적고 바로 다음에 `*.googleapis.com` 같은 항목이 기본으로 들어 있다고 적는다.
`*.googleapis.com` 하나면 Google Cloud Storage 버킷에 데이터를 올릴 수 있고, 그러면 유출 경로로는 충분하다.
기본 거부라는 표현은 정책의 형식을 말할 뿐 실제 표면적을 말하지 않는다.

이 셋을 합치면 마케팅 페이지의 세 부정문은 유지되지 않는다.
정확한 문장은 감독이 필요 없다가 아니라, 설정을 검토할 감독이 한 번 필요하고 MCP를 붙일 때마다 다시 필요하다는 것이다.

### 자격 증명 격리는 네트워크가 열려 있는 한 성립하지 않는다

다섯 번째 격리 계층으로 제시된 자격 증명 주입은 이 제품에서 기술적으로 가장 정교한 부분이다.
호스트 프록시가 아웃바운드 요청의 헤더에 실제 키를 넣으므로 원본 값이 VM 안으로 들어오지 않고, VM 안에는 자리 표시자만 있다.
Docker DevRel 소속 참여자가 스레드에서 직접 확인했듯 주입은 호스트명이 규칙에 맞을 때만 일어난다[^hn-mikesir87].

그런데 같은 스레드에서 이 설계가 어디까지 버티는지가 공개적으로 시험됐고, 결론은 그리 멀지 않다는 것이었다.
자리 표시자가 헤더에서만 치환된다면 파일에 쓴 값은 그대로라는 반박이 나오자[^hn-llimllib], 요청 헤더만 건드리므로 파일은 안전하다는 답이 돌아왔고[^hn-skinfaxi], 다시 요청 헤더를 그대로 공개 로그에 찍어 주는 서비스로 요청을 보내고 그 로그를 읽으면 된다는 지적이 나왔다[^hn-stavros].
결국 에이전트에게 GitHub 푸시 권한이든 gist 생성 권한이든 남아 있으면 유출 경로가 생기며, 네트워크 접근이 조금이라도 있으면 키가 되돌아오도록 요청을 구성하는 방법을 찾아낸다는 정리[^hn-llimllib2]가 이 논쟁의 요약이다.

여기서 짚어야 할 것은 이 설계가 틀렸다는 것이 아니다.
토큰화 프록시는 실제로 유용하고, 최소한 에이전트가 실수로 키를 로그에 남기거나 커밋하는 사고는 확실히 막는다.
문제는 그것이 다섯 개의 격리 계층 중 하나로 나란히 제시된다는 배치다.
하이퍼바이저 격리는 공격자가 커널 취약점을 찾아야 뚫리지만 자격 증명 격리는 에이전트가 허용된 도메인 하나로 요청을 보내면 뚫린다.
난이도가 몇 자릿수 다른 두 방어를 같은 목록에 놓으면 독자는 목록 전체를 가장 강한 항목의 강도로 읽는다.

### 프록시 기반 통제가 감당하지 못하는 트래픽이 남는다

네트워크 정책이 호스트 프록시에서 강제된다는 설계는 비 HTTP 프로토콜을 전면 차단한다는 문장과 짝을 이룬다.
이 조합이 정책 강제를 가능하게 하는 동시에 이 도구의 실질적 사용 범위를 정한다.

HTTPS 트래픽에 정책을 걸려면 프록시가 내용을 봐야 하고, 그러려면 VM 안에 프록시의 인증서를 심어야 한다.
스레드에서 이 지점이 정확히 문제로 제기됐다.
인증서 치환을 지원하지 않는 프로그램이 있으면 그 경우에는 작동하지 않으며, 이것이 생각만큼 사소한 문제가 아니고 인증서를 바꾸면 아예 동작하지 않는 서비스가 실제로 존재한다는 지적이다[^hn-ruszki].
문서가 특정 도메인에 대해 우회를 허용한다고 밝힌 것이 그 대응인데, 우회는 그 도메인에 대해 정책이 없다는 뜻이다.

비 HTTP 전면 차단도 마찬가지로 양날이다.
데이터베이스 클라이언트, SSH, 커스텀 프로토콜을 쓰는 개발 작업은 그대로는 돌아가지 않는다.
이 도구가 잘 맞는 작업은 패키지를 내려받고 API를 호출하고 코드를 고치는, 아웃바운드가 전부 HTTPS인 작업이다.
그것이 코딩 에이전트 작업의 다수이기는 하지만 전부는 아니며, 페이지의 “진짜 개발 환경”이라는 표현은 그 경계를 말하지 않는다.

세 번째로, 허용 도메인 목록을 유지하는 비용이 이 방식의 숨은 세금이다.
스레드에서 Claude Code의 devcontainer 방화벽을 두고 나온 지적이 그것을 잘 보여 준다.
도메인이 CDN 뒤에 있어 IP가 예측 불가능한데 스크립트 실행 시점에 해석된 IP만 허용한다면 나중에 다른 IP로 해석될 때 어떻게 되느냐, 그리고 목록이 짧아서 Go나 Rust 도구 체인에 손대는 순간 아무것도 동작하지 않으므로 결국 시행착오로 목록을 손으로 관리해야 한다는 것이다[^hn-fg137].
Docker의 구현은 IP가 아니라 도메인 단위 프록시이므로 첫 번째 문제는 피하지만 두 번째 문제는 그대로 남는다.
`*.googleapis.com` 같은 넓은 기본값이 들어간 이유도 바로 그 유지 비용일 것이며, 그렇다면 앞 절에서 지적한 표면적 문제와 이 절의 운영 비용 문제는 같은 문제의 두 얼굴이다.

### 스레드의 절반이 자작 대안이라는 사실이 제품 자체에 대한 평가다

HN 353개 댓글에서 가장 눈에 띄는 것은 반대 논거가 아니라 목록이다.
`smolvm`[^hn-binsquare], Nix 기반 재현 가능한 에이전트 이미지[^hn-nicoty], `virtdev`라는 QEMU VM 오케스트레이션[^hn-matheus], `opencode-docker`[^hn-pkhamre], `vibepod-cli`[^hn-nezhar], `flar`라는 bubblewrap 래퍼[^hn-swelljoe], 자작 devcontainer 여러 개[^hn-navigate][^hn-cvak], Incus/LXC 조합[^hn-distepoch], Eclipse Enclave[^hn-segmenttree]가 한 스레드 안에 나온다.

이 밀도는 두 가지를 동시에 말한다.
하나는 문제가 진짜라는 것이다.
사람들이 각자 시간을 들여 같은 것을 만들었다면 수요는 의심할 여지가 없다.

다른 하나는 진입 장벽이 낮다는 것이다.
자기 필요에 맞는 에이전트 샌드박스를 Claude로 직접 짰고 이제 독점 제품에 시간을 투자하기는 어렵다는 반응[^hn-outof]이 그 상태를 요약한다.
격리 자체가 상품화된 영역이므로 Docker가 팔 수 있는 것은 격리가 아니라 통합과 기본값이며, 실제로 매일 쓰는 사용자들이 꼽은 이유도 그것이었다.
아웃바운드 방화벽과 자리 표시자 기반 비밀 주입이 기본으로 되어 있어서라는 것이다[^hn-rusch].

그런데 바로 그 두 기능이 앞의 두 절에서 본 대로 가장 약한 고리다.
그리고 그 위에 로그인 요구가 얹혀 있으므로, 스레드가 도달한 자리는 예측 가능하다.
지금은 이것이 가장 완성도 높은 선택지이지만 오픈 소스가 같은 기본값을 갖추는 순간 갈아탈 준비가 되어 있다는 것이다.

## 인사이트

### 격리 강도가 아니라 격리 경계의 개수가 실제 위험을 정한다

이 제품에 대한 논쟁의 대부분은 강도에 대한 것이다.
컨테이너로 충분한가 VM이어야 하는가, microVM은 진짜 VM인가, gVisor의 시스템 호출 오버헤드와 Firecracker의 시작 시간 중 무엇이 나은가 같은 이야기가 스레드를 채운다[^hn-angry][^hn-cognitive][^hn-masklinn].

그런데 이 문서에서 실제로 위험한 항목들은 강도 문제가 아니었다.
호스트 권한으로 도는 MCP 서버, 나중에 호스트에서 실행되는 Git 훅, 넓은 와일드카드로 열린 도메인은 전부 경계를 뚫는 이야기가 아니라 경계를 우회하는 통로가 몇 개인지의 이야기다.
하이퍼바이저를 아무리 단단히 만들어도 그 옆에 난 문의 개수는 줄지 않는다.

이 구분이 중요한 이유는 투자 방향이 갈리기 때문이다.
강도를 믿는 조직은 더 나은 하이퍼바이저를 고르는 데 시간을 쓰고, 경계 개수를 세는 조직은 무엇이 VM 밖에서 도는지 목록을 만드는 데 시간을 쓴다.
후자가 훨씬 지루하고 훨씬 효과적이다.

그리고 이 지루한 작업은 자동화되지 않는다.
MCP 서버 하나를 새로 붙일 때마다 그것이 안에서 도는지 밖에서 도는지 사람이 확인해야 하며, 그것이 이 제품이 없애 준다고 말한 바로 그 감독이다.

### 에이전트 샌드박스의 진짜 경쟁 축은 보안이 아니라 개발 환경 복제 비용이다

스레드에서 자작 대안을 쓰는 사람들이 공통으로 겪는 문제는 격리가 아니라 환경이다.
Firecracker에서는 `apt install postgres`를 그냥 할 수 없고 이미지에 미리 넣어야 한다는 불만[^hn-grimburger], 에이전트 최신 버전이 이미지에 반영되는지 묻는 질문[^hn-zingar], 커스텀 볼륨 마운트를 여러 개 걸 수 없어 복잡한 설정이 불가능했다는 보고[^hn-meffmadd]가 모두 같은 축에 있다.

이것이 왜 결정적인가 하면, 격리의 강도는 한 번 정해 놓으면 끝나지만 환경의 충실도는 매일 마찰을 만들기 때문이다.
샌드박스가 아무리 안전해도 그 안에서 프로젝트가 빌드되지 않으면 사람은 호스트로 돌아간다.
그리고 호스트로 돌아간 순간 격리의 강도는 0이 된다.

그래서 이 시장의 승부는 “얼마나 단단한가”가 아니라 “내 개발 환경이 그 안에서 얼마나 그대로 도는가”에서 갈릴 가능성이 크다.
Docker가 유리한 자리에 있는 이유도 여기다.
샌드박스 안에서 Docker를 다시 쓸 수 있다는 기능은 보안 기능이 아니라 환경 충실도 기능이며, 이미 Docker로 개발 환경을 만들어 둔 사람에게는 이식 비용이 거의 0이라는 뜻이다.
절대 경로를 보존하는 파일 시스템 패스스루도 같은 성격의 결정이다.

역사적으로 같은 패턴이 있었다.
Vagrant와 devcontainer가 이긴 이유는 격리가 더 좋아서가 아니라 환경 재현이 더 쉬워서였고, Docker 자신이 LXC 위에서 이긴 이유도 정확히 그것이었다.
격리는 커널이 제공했고 Docker가 판 것은 이미지 형식과 배포 경로였다.

### 사람의 승인을 없애면 검토 부채가 설정 파일로 옮겨 갈 뿐 사라지지 않는다

권한 프롬프트가 하는 일은 두 가지다.
하나는 위험한 동작을 막는 것이고, 다른 하나는 사람에게 에이전트가 무엇을 하고 있는지 계속 알려 주는 것이다.
샌드박스는 첫 번째를 인프라로 대체하지만 두 번째는 대체하지 않는다.

그 결과 검토의 대상이 이동한다.
전에는 개별 동작을 그 자리에서 검토했다면, 이제는 허용 도메인 목록과 마운트 목록과 MCP 서버 목록을 미리 검토해야 한다.
문제는 이 이동이 검토를 더 어렵게 만든다는 것이다.
개별 동작 검토는 맥락이 눈앞에 있어서 판단이 쉽지만, 설정 파일 검토는 그 설정이 나중에 어떤 동작을 허용하게 될지를 상상해야 하는 일이다.
`*.googleapis.com`을 허용 목록에서 보고 데이터 유출 경로를 떠올리는 사람은 그 목록을 읽는 사람 중 소수다.

그리고 이 검토는 잘 부패한다.
목록은 한 번 만들고 나면 무언가 동작하지 않을 때만 손대며, 그때마다 항목이 추가되지 삭제되지는 않는다.
방화벽 규칙이 그랬고 IAM 정책이 그랬고 CORS 설정이 그랬다.
허용 목록은 시간이 지나면서 단조 증가하는 것이 기본 동작이다.

그렇다면 이 제품의 실질적 안전은 초기 기본값이 얼마나 좁은지와, 그 목록을 주기적으로 줄이는 사람이 조직에 있는지에 달린다.
전자에 대해서는 문서 스스로 넓다고 인정했고, 후자는 Docker AI Governance가 파는 것이다.
[Core Web Vitals 프로그램에 대해 적었던 것](../performance/core-web-vitals.md)과 같은 결론에 도달한다.
담당자가 없는 정책은 장식이며, 도구가 파는 것은 정책이 아니라 담당자를 세울 근거다.

### 이 범주는 오픈 소스가 기본값을 따라잡는 순간 상품화된다

Docker가 이 제품에 붙인 차별점은 세 가지다.
여러 에이전트를 한 샌드박스로 다루는 통합, 아웃바운드 방화벽, 자리 표시자 기반 비밀 주입이다.
그리고 매일 쓰는 사용자들이 꼽은 이유도 정확히 그 세 가지였다.

그런데 이 셋은 모두 코드로 복제 가능한 기능이다.
스레드에서 이미 아웃바운드 방화벽과 비밀 주입을 둘 다 갖춘 오픈 소스가 이름으로 제시됐고[^hn-segmenttree], 여러 에이전트를 다루는 템플릿과 킷 개념도 개인이 만든 이미지로 복제되고 있다[^hn-alexfortin].
격리 자체는 Firecracker와 libkrun과 bubblewrap이 이미 무료로 제공하며, Apple은 `container` CLI를, Linux는 Incus를 기본 제공한다[^hn-woadwarrior][^hn-crabmusket].

복제되지 않는 것은 하나다.
조직 전역 강제와 감사인데, 그것이 유료 제품의 이름이 AI Governance인 이유이며 무료 제품이 로그인을 요구하는 이유이기도 하다.
그러니 로그인 요구는 실수나 탐욕이 아니라 이 범주의 유일한 방어 가능한 자리로 미리 이동해 둔 것이다.

문제는 그 이동이 무료 제품의 채택을 깎는다는 점이다.
조직 전역 강제를 팔려면 개발자들이 이미 그 도구를 쓰고 있어야 하는데, 로그인 요구가 정확히 그 채택을 막는다.
Docker Desktop 라이선스 변경 때와 같은 긴장이며, 그때도 개발자는 대안으로 흩어졌고 조직은 남았다.
이번에도 같은 결과가 나올 것 같다면, 이 제품의 성공 여부는 오픈 소스보다 얼마나 나은가가 아니라 조직 구매 결정이 개발자 선호보다 얼마나 빨리 내려지는가에 달려 있다.

## 참고

- HN 토론: <https://news.ycombinator.com/item?id=49239751> (640점, 353개 댓글)
- Lobste.rs와 GeekNews에서는 이 페이지에 대한 스레드를 찾지 못했다.
- 관련 문서: [Agent Safehouse](../security/agent-safehouse.md), [Sandboxd](sandboxd.md)

---

[^hn-rvz]: HN 사용자 `rvz`: “microVMs (firecracker) have existed for years. This is not new.”
[^hn-laserlight]: HN 사용자 `laserlight`: “Requires login. Garbage.”
[^hn-pixard]: HN 사용자 `pixard`: “do they still want you to LOGIN, in order to use a local dev tool? Yes, yes they do. No thanks Docker. You can keep your buzzword reasoning as to why this is needed.”
[^hn-binsquare]: HN 사용자 `binsquare`: “I build a OSS lightweight, portable VM for those that don't want lock ins: `smol-machines/smolvm`”. Firecracker 대신 만든 이유로 “batteries included” 대안이라는 점과 단일 파일로 구워 어디서나 되살리는 이식성을 든다.
[^hn-karakanb]: HN 사용자 `karakanb`: “I got excited for this not because this didn't exist before, but because Docker putting their weight on this would imply a broader adoption and better integration in the industry. I am sad that they are asking for a login here though, which doesn't make any sense to me.”
[^hn-aborsy]: HN 사용자 `aborsy`: “Other than the login problem, it's a decent option.” 에이전트는 미리 설치되어 있고 업데이트가 있으면 첫 실행 시 알리고 승인하면 갱신한다고 덧붙인다.
[^hn-rusch]: HN 사용자 `rusch`: “The login is annoying but, lacking an open source alternative, this has been my daily driver for a while now because it works great out of the box with two key features: outbound firewall and secret injection with placeholders.”
[^hn-dsebastien]: HN 사용자 `dSebastien`: “You can create those manually but if you want to enforce those then you need the subscription”
[^hn-runtime]: HN 사용자 `runtime_lens`: “sandboxing limits what the agent can do but it doesn't necessarily enforce that the agent must run inside the sandbox. You need a separate control layer to enforce that boundary.”
[^hn-dsebastien-enforce]: HN 사용자 `dSebastien`: “The one thing I wonder about is how you enforce the usage of Docker Sandboxes vs running the agent on the host directly, apart from scanning machines for binaries”
[^hn-cryptoz]: HN 사용자 `cryptoz`: “The linked page implies there is no linux support, I wonder why. It's there in the docs if you hunt for it.”
[^hn-hokkos]: HN 사용자 `hokkos`: “Wow, I hope one day Linux will be able to support the exclusive MacOs/Windows technology of Docker Sandboxes.”
[^hn-ethagnawl]: HN 사용자 `ethagnawl`: “That omission didn't smell right based on everything I know about Docker. Curious choice, indeed, not to show Linux install instructions.”
[^hn-etoxin]: HN 사용자 `etoxin`: “The docs are here... The other url is their marketing page. Yes, Linux is supported.”
[^hn-mikesir87]: Docker DevRel 팀 소속이라고 밝힌 HN 사용자 `mikesir87`: “On the Docker DevRel team... yes! This is it. The secret is injected only into headers in which the hostname matches.”
[^hn-llimllib]: HN 사용자 `llimllib`: “Your agent writes secret.txt with the placeholder, and the tokenizing proxy replaces it with the token, then the agent reads secret.txt”
[^hn-skinfaxi]: HN 사용자 `skinfaxi`: “It only replaces the token in the HTTP header that is sent to the server. Whatever you wrote in your files isn't touched by the proxy.”
[^hn-stavros]: HN 사용자 `stavros`: “It sends a request to requestb.in and reads the public log of the headers. There are ways.”
[^hn-llimllib2]: HN 사용자 `llimllib`: “really if it has any network access at all it can come up with a clever way to route a request through the network such that the key comes back somewhere in the request. If you scan for it inbound too, the machine can obfuscate it.”
[^hn-ruszki]: HN 사용자 `ruszki`: “That means that it doesn't work in those cases... It's not as trivial as it seems at all. There are websites which simply doesn't work if you replace certificates, regardless of browser or CA for example.”
[^hn-fg137]: HN 사용자 `fg137`: “presumably those domains are behind CDNs, and IP addresses are unpredictable... And even if that works, this is a very short list. As soon as you reach for Go, Rust tooling etc nothing works. So you need to manually maintain this list which is nothing but painful trial and error.”
[^hn-nicoty]: HN 사용자 `nicoty`: “I have a solution based on Nix that can be used to generate reproducible container images... It lets you customise which agents, harnesses, or any other packages you want included in the VM”
[^hn-matheus]: HN 사용자 `matheusmoreira`: “Just the general knowledge that sharing a kernel with untrusted software is too dangerous, that hardware virtualization is an infinitely smaller attack surface... Initial threat model was supply chain attacks but eventually grew to include AI harnesses as well. Not very worried about them hacking me, more about accident prevention.”
[^hn-pkhamre]: HN 사용자 `pkhamre`: “I started building my own isolated and security-hardened docker image for OpenCode about half a year ago. Been using it daily.”
[^hn-nezhar]: HN 사용자 `nezhar`가 podman 지원과 로컬 텔레메트리 수집을 갖춘 오픈 소스 대안 `VibePod/vibepod-cli`를 제시했다.
[^hn-swelljoe]: HN 사용자 `SwellJoe`: “bubblewrap is superior to Docker for this. I wrote a tool to use bubblewrap for the purpose. It needs a tool to start it... because you need to take your session/auth data into the container, and if you want the agent to be able to start containers (agents love containers) within the container, you need some config magic mounted inside.”
[^hn-navigate]: HN 사용자 `navigate8310`: “I just made my own devcontainer that I copy on any project and load whatever harness I want in that repo. Harnesss' config and auth are simply mounted from the host, so no setup required at all.”
[^hn-cvak]: HN 사용자 `cvak`: “I actually just re-use claude-code .devcontainer... I especially like the firewall it has.”
[^hn-distepoch]: HN 사용자 `dist-epoch`: “An Ubuntu Server VM, like the ones started by Incus, use at least 512 MB of RAM per instance. If you spawn 10 sandbox VMs, you already pay 5 GB RAM just to sit there idle... I use something in between - a single Ubuntu VM, into which I spawn multiple Incus LXC containers for the agents. The containers only use 50 MB or so per instance.”
[^hn-segmenttree]: HN 사용자 `SegmentTree`: “Eclipse Enclave does exactly that: There is an outbound firewall and secret injections, so that the agent never sees a real key. And it's fully open source.”
[^hn-angry]: HN 사용자 `angry_octet`: “LLMs are great at finding 0-day, and people are rubbish at updating their containers and hosts to patch b-day. Containers have access to the kernel ABI, and as shown in the latest kernel exploits, all the memory handling surface that exposes. The virtualisation interface, offering fewer services, is significantly harder.”
[^hn-cognitive]: HN 사용자 `cognitiveinline`: “Unless we're talking 0-day/CVE, running an unprivileged container is as trustable as a VM. The only difference is how strictly you want to hold the memory/CPU bar.”
[^hn-masklinn]: HN 사용자 `masklinn`: “'microvms' are real vms but the hypervisor and vm (guest kernel) shed most of the hardware / device emulation, support, and discovery... Firecracker is designed to start a VM in under 125ms and 5MB.”
[^hn-grimburger]: HN 사용자 `Grimburger`: “you can't just `apt install postgres` on firecracker, it needs to get baked into the image first. That's my experience anyway, there's a lot of restrictions once you need to do some real basic things.”
[^hn-zingar]: HN 사용자 `zingar`: “Do the agents come preinstalled in the images? Or do they somehow use whatever I've installed locally?... I'm wondering whether the sandbox images stay up to date with new releases of each image.”
[^hn-meffmadd]: HN 사용자 `meffmadd`: “last time I checked you could not configure custom volume mounts, making more complex setups impossible.” 이후 `sbx run claude ~/project-a ~/shared-libs:ro` 형태의 다중 작업 공간 지원이 추가됐다는 답이 이어졌다.
[^hn-outof]: HN 사용자 `outof`: “Like many people, I suspect, I used Claude to write my own agent sandbox that suits my needs very well. Investing my time in a propietary product has become a hard sell.”
[^hn-alexfortin]: HN 사용자 `alexfortin`이 Pi 미지원을 우회하려고 만든 `sbx-template-pi` 이미지를 소개하며 “the 'kit/mixin' concepts are neat and I make use of them too”라고 적었다.
[^hn-woadwarrior]: HN 사용자 `woadwarrior01`: “Better yet, use Apple's container CLI if you're on a Mac, instead of the docker bloatware.”
[^hn-crabmusket]: HN 사용자 `crabmusket`가 Incus 기반 대안 `code-on-incus`를 제시했다.
