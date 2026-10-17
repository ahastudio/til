# NVIDIA Run:ai: 쿠버네티스 GPU 오케스트레이션 플랫폼의 오픈소스 공개

<https://docs.nvidia.com/run-ai/>

<https://github.com/dsx-ai-factory/run-ai>

HN 토론: <https://news.ycombinator.com/item?id=50101962> (1점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=35507>

## 소개

NVIDIA Run:ai는 쿠버네티스 위에서 여러 팀이 공유하는 GPU를
스케줄링하고 관리하는 플랫폼이다.
NVIDIA는 2024년 말 Run:ai를 인수했고,
2026년 10월 플랫폼 전체를 오픈소스로 공개했다.[^techstrong]
저장소는 `dsx-ai-factory/run-ai`이고 라이선스는 Apache 2.0, 주 언어는 Go다.
저장소는 2026년 8월 25일에 만들어졌고,
2026년 10월 17일 확인 기준으로 스타 438개, 포크 62개다.[^gh-api]

README는 이 프로젝트를 쿠버네티스를 대체하는 것이 아니라
그 위에 얹는 스케줄링과 오케스트레이션 계층이라고 소개한다.
개발, 학습, 추론 작업을 온프레미스, 클라우드, 하이브리드 어디서든
같은 방식으로 돌리게 하고, GPU 스케줄링, 자원 관리, 거버넌스,
관측성을 묶어 여러 팀과 클러스터가 GPU를 효율적으로 나눠 쓰게 한다는
것이다.[^readme]

## 구성

플랫폼은 두 부분으로 나뉜다.[^readme]

| 구성 요소     | 역할                                                                         |
| ------------- | ---------------------------------------------------------------------------- |
| 컨트롤 플레인 | 작업 제출, 조직 자원과 정책 관리, 여러 클러스터의 모니터링과 분석            |
| 클러스터      | 각 쿠버네티스 클러스터에 설치되어 기본 스케줄링을 GPU 인식 스케줄링으로 확장 |

사용자는 웹 UI, CLI, REST API로 컨트롤 플레인에 작업을 넘긴다.
컨트롤 플레인은 요청을 해당 클러스터에 동기화하고,
클러스터 서비스가 스케줄링과 자원 정책을 적용해 작업이 어디서 어떻게
돌지 정한다.
상태는 다시 컨트롤 플레인으로 올라온다.

README가 꼽는 핵심 기능은 다음과 같다.

- 공정 분배(fair-share), 선점, 빈 패킹, 우선순위, 토폴로지 인식 배치를 쓰는
  GPU 스케줄링
- GPU를 쪼개 여러 작업에 나눠 주는 분할 할당
- 부서와 프로젝트 단위의 GPU 할당량과 정책
- 여러 클러스터의 중앙 관리
- 워크스페이스, 학습, 분산 학습, 추론 작업 관리
- 역할 기반 접근 제어와 관측성

모노레포에는 컨트롤 플레인(`control-plane/`), 클러스터 서비스(`runai-cluster/`),
설치 도구(`runai-installer/`), MCP 서버(`runai-mcp-server/`),
생성된 API 클라이언트와 공유 Go 라이브러리, 부하 테스트 도구,
문서가 함께 들어 있다.[^readme]
`skills/` 디렉터리에는 실패한 작업 진단, 할당량 감사,
클러스터 상태 요약 같은 AI 에이전트용 스킬이 있다.[^gh-api]

## 다른 도구와의 관계

README는 주변 도구와의 관계를 표로 정리한다.[^readme]
스케줄러 자리에서는 기본 `kube-scheduler`, Volcano, Kueue와 겹치며,
Run:ai는 KAI Scheduler를 함께 배포하고 그 위에 공정 분배, 선점,
분할 GPU, 부서와 프로젝트의 할당량 계층을 더한다.
NVIDIA GPU Operator는 노드에 GPU를 노출하고 설정하는 쪽이라 보완 관계이고,
Kubeflow, Ray, Argo Workflows처럼 작업을 제출하는 도구와도 보완 관계다.
Slurm은 베어메탈 HPC 배치의 대안으로 분류한다.

README는 적용 범위도 스스로 밝힌다.
한 쿠버네티스 GPU 자원을 여러 팀이 나눠 쓰며 할당량과 멀티 테넌트
거버넌스가 필요하다면 Run:ai가 그 빈자리를 채우지만,
한 팀이 전용 GPU에서 작업을 돌리는 정도라면
쿠버네티스 기본 스케줄링으로 충분할 수 있다는 것이다.[^readme]

## 사용법

로컬 개발 환경은 `local-dev.sh` 하나로 만든다.
컨트롤 플레인과 클러스터 서비스를 소스에서 빌드해
로컬 이미지 레지스트리가 딸린 Kind 클러스터에 배포한다.[^readme]

```bash
./local-dev.sh                                  # 전체 빌드, 클러스터 생성, 배포
./local-dev.sh --skip-build --skip-cluster      # 재배포만
./local-dev.sh --teardown                       # 환경 제거
```

빌드는 모두 컨테이너 안에서 돌아서 호스트에 Go, Node, Java가 없어도 된다.
`--gpu-operator`를 주면 가짜 GPU 오퍼레이터 대신 실제 NVIDIA GPU를
쓴다.[^claude-md]
운영 설치는 `runai-installer` CLI와 설정 YAML을 쓰는 안내형 설치가 권장이고,
Argo CD 같은 자체 도구로 관리한다면 Helm 차트를 직접 배포한다.
릴리스된 이미지와 차트는 NGC 레지스트리 `nvcr.io/nvidia/runai`에서
받는다.[^readme]

## 거버넌스와 지원 범위

GOVERNANCE.md는 이 프로젝트를 NVIDIA 오픈소스 프로젝트로 규정하고,
로드맵과 릴리스 일정은 NVIDIA가 정한다고 적는다.[^governance]
여러 PR에 걸친 결정은 게으른 합의(lazy consensus)로 내린다.
메인테이너가 이슈로 제안하고 5영업일 안에 반대가 없으면 통과하며,
반대가 10영업일 안에 풀리지 않으면 메인테이너 과반 투표로 정한다.
메인테이너끼리 합의하지 못하면 프로젝트를 맡은 NVIDIA 엔지니어링
리더십이 정한다.

외부 기여에는 커밋마다 DCO 서명이 필요하다.
PR을 열면 빠른 검사는 바로 돌지만,
전체 빌드와 종단 간 파이프라인은 메인테이너가 `/ok-to-test`를 입력해야 시작되고,
이 파이프라인이 병합에 필요한 `Validate Successful Run` 검사를
만든다.[^contributing]
지원 버전은 `release-3.0` 브랜치 하나뿐이며,
지원하지 않는 브랜치에 대한 버그 리포트와 PR은 받지 않는다.[^support]
릴리스는 3.0.16(9월 30일)부터 3.0.20(10월 11일)까지
2주 사이에 다섯 번 나왔다.[^releases]

## 분석

### 오픈소스화는 플랫폼 판매에서 GPU 판매로 무게가 옮겨 간 결과다

Run:ai는 원래 GPU 활용률을 높여 주는 유료 소프트웨어를 파는 회사였다.
NVIDIA에게 이 소프트웨어의 가치는 라이선스 수익보다
자사 GPU를 사는 이유를 늘리는 데 있다.
Techstrong은 공개의 배경으로 GPU 저활용 문제를 들며,
평균 활용률이 5% 안팎이라는 Cast AI 조사와
기업의 86%가 활용률 50% 이하라고 답했다는 수치를 인용했다.[^techstrong]
GPU가 놀고 있다는 사실은 GPU를 더 사지 않을 이유가 되므로,
활용률을 올리는 도구를 무료로 푸는 것은 판매사 입장에서 합리적이다.

저장소가 `dsx-ai-factory` 조직 아래 있다는 점도 같은 방향을 가리킨다.
Run:ai는 독립 제품이 아니라 NVIDIA DSX AI Factory 플랫폼의 기초로
자리 잡았다.[^techstrong]
소프트웨어를 무료로 하고 하드웨어와 통합 플랫폼에서 돈을 버는 구조는
CUDA가 걸어온 길과 같다.

### README가 범위를 스스로 좁히는 것은 드문 정직함이다

README는 Run:ai가 필요 없는 경우를 명시한다.
한 팀이 전용 GPU를 쓰는 정도라면 쿠버네티스 기본 스케줄링으로 충분하다는
문장이다.[^readme]
제품 README가 자기 제품이 불필요한 조건을 적는 일은 흔하지 않다.

이 문장은 Run:ai가 푸는 문제가 기술 문제라기보다 조직 문제임을 드러낸다.
공정 분배, 할당량 계층, 부서와 프로젝트, 역할 기반 접근 제어는
모두 GPU를 놓고 여러 팀이 다투는 상황을 전제로 한다.
GPU 한 장을 여러 작업에 쪼개 주는 분할 할당도
결국 비싼 자원을 여러 사람이 나눠 쓰게 하려는 장치다.

### 저장소 자체가 AI 에이전트를 기여자로 상정한다

루트에 `AGENTS.md`와 `CLAUDE.md`가 있고,
`CLAUDE.md`는 `AGENTS.md`를 불러와 문서 규칙을 따르게 한다.[^claude-md]
`skills/` 디렉터리는 운영자가 쓰는 에이전트 스킬을,
`runai-mcp-server/`는 Run:ai 조작을 AI 도구에 노출하는 MCP 서버를
담는다.[^readme]
CONTRIBUTING.md는 기여 준비 과정에서 독점, 기밀, 수출 통제 자료를
제3자 AI 도구에 붙여 넣지 말라고 경고한다.[^contributing]

2026년에 공개되는 엔터프라이즈 저장소가
사람 기여자와 AI 에이전트 기여자를 함께 염두에 두고 꾸려진다는 신호다.
`.coderabbit.yaml`로 AI 코드 리뷰까지 설정해 두었으니,
에이전트가 쓰고 에이전트가 1차 리뷰하는 흐름을 처음부터 받아들인 셈이다.

## 비평

### 오픈소스이지만 하드웨어 중립은 아니다

README와 문서는 NVIDIA GPU를 전제로 한다.
`--gpu-operator` 옵션은 실제 NVIDIA GPU를 쓰는 선택지이고,
GPU 활성화 계층으로 언급되는 것도 NVIDIA GPU Operator와 Network
Operator다.[^readme]
AMD나 다른 가속기를 같은 수준으로 지원한다는 언급은 README에 없다.

Futurum Group의 Mitch Ashley는 오픈소스가 하드웨어 중립을 뜻하지는 않으며,
구매자는 바로 그 기준으로 이번 공개를 평가해야 한다고 했다.[^techstrong]
Apache 2.0이라 포크해서 다른 가속기를 붙이는 일은 법적으로 가능하다.
그러나 스케줄러의 분할 GPU나 토폴로지 인식 배치가
NVIDIA 드라이버와 하드웨어 특성에 얼마나 묶여 있는지는
README만으로는 알 수 없다.

### 거버넌스는 열려 있지만 결정권은 NVIDIA에 있다

GOVERNANCE.md는 게으른 합의와 과반 투표라는 공개 절차를 두지만,
로드맵과 릴리스 일정은 NVIDIA가 정하고
교착 상태는 NVIDIA 엔지니어링 리더십이 푼다.[^governance]
README도 장기 기능 로드맵은 이 저장소에 공개하지 않는다고 밝힌다.[^readme]
메인테이너 목록이 사실상 NVIDIA 직원이라면,
공개 절차는 외부 기여자에게 발언권을 주되 결정권은 주지 않는다.

전체 CI가 메인테이너의 `/ok-to-test` 뒤에만 돈다는 점도 같은
구조다.[^contributing]
비용과 보안을 생각하면 합리적인 장치지만,
외부 기여자는 병합에 필요한 검사를 스스로 돌릴 수 없다.
KAI Scheduler는 CNCF 샌드박스에 기여되었지만,
플랫폼 전체는 중립 재단이 아니라 NVIDIA 조직 아래 남아 있다.[^techstrong]

### 공개 직전의 흔적이 저장소에 남아 있다

`local-dev.md`는 `GITHUB_TOKEN`이 저장소가 비공개인 동안에만 필요하며,
Go 빌드가 `github.com/run-ai/*` 모듈을 받아 오기 때문이라고 적는다.[^local-dev]
`CLAUDE.md`에는 여전히 비공개 Go 모듈
때문에 토큰이 필요하다는 안내가 그대로 있다.[^claude-md]
README도 루트 `Makefile` 타깃이 자리표시자일 뿐이라고 알려진 한계로
적는다.[^readme]

이 흔적은 저장소가 처음부터 공개용으로 설계된 것이 아니라,
내부 모노레포를 내보내기 위해 정리된 것임을 보여 준다.
루트의 `.oss-export-id` 파일도 그런 내보내기 과정을 짐작하게 한다.
이런 구조에서는 실제 개발이 내부에서 일어나고
공개 저장소는 그 결과를 받는 쪽이 되기 쉽다.
외부 기여가 의미 있게 들어갈 수 있는지는
앞으로 병합되는 외부 PR의 비율로 판단해야 한다.

## 인사이트

### GPU 스케줄러의 표준을 누가 쥐느냐가 다음 경쟁이다

쿠버네티스 배치 스케줄링에는 이미 Volcano와 Kueue가 있다.
Run:ai는 KAI Scheduler를 CNCF에 기여하고 플랫폼 전체를 공개하면서
이 자리에서 사실상의 표준이 되려 한다.
Techstrong에 따르면 Crusoe, Mirantis, Nebius, Rafay, Spectro Cloud,
vCluster 같은 파트너가 이미 이를 자기 제품에 통합하고 있다.[^techstrong]

스케줄러가 표준이 되면, 그 스케줄러가 가장 잘 이해하는 하드웨어가
유리해진다.
분할 GPU와 토폴로지 인식 배치가 NVIDIA 하드웨어에서 가장 잘 동작한다면,
중립처럼 보이는 오픈소스 계층이 하드웨어 선택을 조용히 끌고 간다.
CUDA가 언어와 라이브러리 계층에서 했던 일을
Run:ai가 클러스터 운영 계층에서 반복하는 셈이다.

### GPU 활용률 문제는 기술보다 조직 설계에서 풀린다

활용률이 낮은 이유는 스케줄러가 없어서만이 아니다.
팀마다 GPU를 확보해 두고 놓지 않으려는 행동이 더 큰 원인이다.
Run:ai의 할당량 계층과 선점은 이 행동을 정책으로 다루려는 장치이고,
README가 단일 팀에는 필요 없다고 말하는 이유도 여기 있다.

따라서 도입을 검토하는 조직은 스케줄러 성능보다
부서별 할당량과 선점 규칙을 누가 정하고 어떻게 합의할지를 먼저 정해야 한다.
도구는 무료가 되었지만,
GPU를 빌려주고 돌려받는 규칙을 만드는 비용은 그대로 남는다.

### 무료 오픈소스 플랫폼의 운영 비용은 지원 기간에서 드러난다

지원 브랜치가 `release-3.0` 하나뿐이고
지원하지 않는 브랜치의 버그 리포트는 받지 않는다.[^support]
2주 사이에 패치 릴리스가 다섯 번 나왔다는 것은 활발하다는 뜻이기도 하지만,
운영자가 그 속도를 따라 업그레이드해야 한다는 뜻이기도 하다.[^releases]
장기 지원 브랜치가 필요한 조직은 결국 NVIDIA의 상용 지원으로 가게 된다.
SUPPORT.md가 상용 지원을 도움 채널로 안내하는 것도 그 경로를 보여 준다.[^readme]

---

[^techstrong]: Techstrong.ai, [NVIDIA Hands Run:ai to the Open Source Community](https://techstrong.ai/articles/nvidia-hands-runai-to-the-open-source-community/), 2026-10-14

[^gh-api]: GitHub API, [dsx-ai-factory/run-ai](https://api.github.com/repos/dsx-ai-factory/run-ai), 2026-10-17 확인

[^readme]: dsx-ai-factory/run-ai, [README.md](https://github.com/dsx-ai-factory/run-ai/blob/main/README.md), 2026-10-17 확인

[^claude-md]: dsx-ai-factory/run-ai, [CLAUDE.md](https://github.com/dsx-ai-factory/run-ai/blob/main/CLAUDE.md), 2026-10-17 확인

[^governance]: dsx-ai-factory/run-ai, [GOVERNANCE.md](https://github.com/dsx-ai-factory/run-ai/blob/main/GOVERNANCE.md), 2026-10-17 확인

[^contributing]: dsx-ai-factory/run-ai, [CONTRIBUTING.md](https://github.com/dsx-ai-factory/run-ai/blob/main/CONTRIBUTING.md), 2026-10-17 확인

[^support]: dsx-ai-factory/run-ai, [SUPPORT.md](https://github.com/dsx-ai-factory/run-ai/blob/main/SUPPORT.md), 2026-10-17 확인

[^local-dev]: dsx-ai-factory/run-ai, [local-dev.md](https://github.com/dsx-ai-factory/run-ai/blob/main/local-dev.md), 2026-10-17 확인

[^releases]: dsx-ai-factory/run-ai, [Releases](https://github.com/dsx-ai-factory/run-ai/releases), 2026-10-17 확인
