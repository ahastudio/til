# LaunchVideo: Opus 5.5가 코드로 쓰고 브라우저가 찍는 제품 소개 영상

<https://launchvideo.io/>

<https://github.com/diggerhq/shipvideo>

HN 토론: <https://news.ycombinator.com/item?id=49836374> (422점, 221개 댓글)

GN 토론: <https://news.hada.io/topic?id=34253>

## 소개

LaunchVideo는 URL을 붙여 넣거나 제품을 설명하면 제품 출시 영상을 만들어 주는 웹 페이지다.
페이지는 Opus 5.5가 영상을 쓰고 서버리스 에이전트가 렌더링하며, 영상 하나에 약 4분과 약 10만 토큰이 든다고 소개한다.
HN에는 “Opus 5.5 is good at explainer videos”라는 제목으로 올라왔다.

페이지에는 편집 없이 한 번 실행한 결과라는 예시 다섯 편이 실려 있다.
NVIDIA, TypeSafe AI의 Jev, OpenComputer, Linear의 홈페이지를 입력한 것과, “추론을 다루는 현대 스타트업을 위한 세련되고 힘 있는 영상”이라는 프롬프트로 만든 가상의 Infera로, 길이는 모두 31초에서 34초 사이다.
무료 생성 횟수를 다 쓰면 자기 OpenComputer 계정에 에이전트를 배포해 제한 없이 돌리라는 안내가 뜬다.
전체 코드는 `diggerhq/shipvideo` 저장소에 있고, `npx opencomputer template deploy`로 한 번에 배포할 수 있다.
페이지 끝에는 이 아이디어가 Opus 5.5와 교육용 영상에 대한 Deedy의 게시물에서 왔다고, 곧 모델이 영상을 코드로 쓰면 코드는 매번 같게 렌더링된다는 발상이라고 적혀 있다.

## 동작 방식

### 에이전트 파일 하나와 도구 세 개

제품 전체는 에이전트 파일 하나, 도구 세 개, 그리고 입력 양식이다.
에이전트는 TypeScript로 정의하고 `opencomputer deploy`로 배포하는 OpenComputer 서버리스 에이전트이며, 프레임워크나 큐나 자체 서버가 없다.
모델은 OpenComputer의 모델 게이트웨이를 거친 `anthropic/claude-opus-5.5`이고, 영상 하나에 입력 약 9만 토큰과 출력 약 1만 5천 토큰을 쓰는데 대부분이 HTML 자체다.

```typescript
// opencomputer/agents/director/agent.ts
import { useInput, useModel, useTool } from "@opencomputer/agent";
import { checkScene, renderVideo } from "./tools/scene.js";
import { webFetch } from "./tools/web.js";

export default function Agent() {
  const input = useInput();           // 양식에서 온 JOB 블록
  useModel("anthropic/claude-opus-5.5");
  useTool(webFetch);                  // 제품 사이트를 읽는다
  useTool(checkScene);                // HTML을 불러 오류와 보이는 글자를 보고한다
  useTool(renderVideo);               // 헤드리스 Chromium → ffmpeg → Blob
  return `You are a motion designer who writes code. ...`;
}
```

세 도구의 역할은 다음과 같다.

| 도구           | 하는 일                                                                        |
| -------------- | ------------------------------------------------------------------------------ |
| `web_fetch`    | 페이지 텍스트와 제목, 헤딩, 가장 많이 쓰인 16진 색상, Google Fonts를 돌려준다  |
| `check_scene`  | 영상 HTML을 불러 JavaScript 오류와 표본 시각마다 화면에 보이는 글자를 보고한다 |
| `render_video` | 렌더링하고 업로드한다                                                          |

### 영상 모델 없이 가상 시계로 찍는다

렌더링에는 영상 생성 모델을 쓰지 않는다.
페이지의 시계, 곧 `requestAnimationFrame`, 타이머, `Date`, CSS와 Web Animations를 가상 시계로 바꿔서, 모든 프레임을 결정적인 시각 이동으로 만든다.
1920x1080, 30fps로 찍은 JPEG 프레임을 `libx264`에 흘려 넣고 `crf 18`로 인코딩한다.

작업마다 새 마이크로VM에서 세션 하나가 돈다.
Amazon Linux 2023 arm64에 vCPU 4개, RAM 8GB, Node 22이며, 첫 도구 호출이 Playwright의 헤드리스 Chromium과 정적 ffmpeg를 설치하는 데 약 1분이 걸리고, 작업이 끝나면 VM은 버린다.

### 비밀을 갖지 않는 에이전트

에이전트는 비밀을 갖지 않는다.
양식이 한 경로에만 3시간 동안 쓸 수 있는 Vercel Blob 업로드 토큰을 발급해 작업별 매니페스트에 두고, 도구는 작업 ID로 그 토큰을 가져온다.
완성된 MP4는 공개 Blob URL이다.
페이지는 CLI와 같은 API를 써서 세션을 만들고, 한 턴을 보내고, `tool.started`, `tool.completed`, `turn.completed` 이벤트 스트림을 폴링해 진행 상황을 보여 주며, MP4가 Blob에 나타나면 완료로 본다.

## 분석

### 영상을 픽셀이 아니라 코드로 만든다는 점이 핵심이다

LaunchVideo가 흔한 AI 영상과 다른 점은 영상 생성 모델을 쓰지 않는다는 것이다.
HN의 minimaxir가 짚은 대로, Opus 5.5는 영상 생성 모델이 아니라 코드를 생성하고 반복해 고친 뒤 렌더링하며, 그 방법은 여러 가지다.[^minimaxir]
그는 유명한 “p(doom)을 올린다” 영상의 코드가 Processing으로 공개돼 있다는 예를 든다.

코드로 만든 영상은 세 가지 성질을 얻는다.
결정적이어서 같은 HTML은 매번 같은 영상을 낸다.
수정할 수 있어서 글자 하나를 바꾸려고 영상을 다시 생성할 필요가 없다.
검사할 수 있어서 `check_scene`처럼 특정 시각에 화면에 무엇이 보이는지를 텍스트로 확인할 수 있다.
이 저장소의 [HyperFrames](./hyperframes.md)가 HTML을 쓰면 영상으로 렌더링되는 에이전트용 프레임워크를 내세운 것과 같은 방향이다.
gAI는 이 방식의 확장을 보여 준다.[^gAI]
Opus 5.5에게 JavaScript 애니메이션을 만들게 하다가 After Effects용 JSX 스크립트로도 내보낼 수 있다는 것을 알게 됐고, 모델이 첫 시도를 하면 실제로 쓰는 도구로 가져가 다듬는다는 것이다.

### 모델의 공은 어디까지인가

cush는 영리하지만 이것이 Opus 5.5와 무슨 상관이냐고 묻는다.[^cush]
전환 애니메이션이 있는 HTML 프레젠테이션을 만드는 것은 Opus 4.6 때부터 가능했고, Playwright와 ffmpeg로 녹화하는 것은 모델의 일이 아니라는 것이다.
bilsbie도 Opus가 대본을 쓰면 영상은 무엇이 만들고, 왜 Opus가 모든 공을 가져가느냐고 묻는다.[^bilsbie]

이 질문에 대한 답은 구조 안에 있다.
렌더링 파이프라인은 결정적이고 단순하며, 가상 시계와 ffmpeg는 새로운 것이 아니다.
영상의 품질을 가르는 것은 HTML 한 편을 얼마나 잘 쓰느냐, 곧 장면의 구성, 타이밍, 색과 글꼴의 선택이며, 이것이 토큰의 대부분을 차지한다.
그래서 이 제품은 사실상 “모델이 모션 디자이너로서 코드를 얼마나 잘 쓰는가”에 대한 시연이고, 파이프라인은 그 결과를 보여 주는 무대일 뿐이다.
prathje가 Motion Canvas 기반 서비스를 만들며 가장 중요한 것은 무엇이 좋아 보이고 좋게 느껴지는지에 대한 모델의 감각이었고, 모델이 명백히 잘못된 배치를 여러 번 놓쳤다고 말한 것도 같은 지점이다.[^prathje-sense]

### 제품의 절반은 인프라 광고다

페이지의 “how it runs” 절은 제품 설명보다 OpenComputer 설명에 가깝다.
에이전트, 마이크로VM, 모델 게이트웨이, 세션 API가 모두 OpenComputer이고, 무료 횟수가 끝나면 OpenComputer 계정에 배포하라는 안내가 뜬다.
amelius는 “예상대로”라고 짧게 반응한다.[^amelius]

이것은 요즘 에이전트 인프라 회사가 쓰는 전형적인 방식이다.
눈길을 끄는 데모 하나를 만들고, 그 데모 전체를 한 번에 복제할 수 있는 템플릿으로 공개해, 데모를 본 사람이 자기 계정에서 인프라를 쓰게 만든다.
ndom91이 곧바로 `claude-code -p`와 로컬 ffmpeg로 같은 일을 하는 포크를 만든 것은, 이 구조의 핵심이 인프라가 아니라 프롬프트와 렌더러라는 것을 보여 준다.[^ndom91]

## 비평

### 설명 영상이라 부르기에는 설명이 없다

HN 제목은 설명 영상이지만, 예시 영상은 설명보다 인상을 남긴다.
remywang은 설명 영상은 설명에 집중해야 하는데 이 영상들은 거의 내용이 없다며, 최고의 설명 영상을 만드는 Kurzgesagt는 애니메이션이 아니라 대본을 쓰는 데 대부분의 시간을 쓴다고 말한다.[^remywang]
lern_too_spel은 기존 프레젠테이션 슬라이드 스킬로 영상을 만든 것일 뿐, 실제 개념을 설명하는 그림이나 애니메이션은 없다고 한다.[^lern_too_spel]

armchairhacker는 구체적인 예를 든다.[^armchairhacker]
Jev 영상은 Jev가 TypeSafe AI의 것이고 더 빠르고 싸다는 같은 말을 되풀이해서 슬라이드 네 장으로 줄일 수 있을 것 같았고, Linear 영상은 이슈를 만들어 에이전트에게 할당하고 간트 차트를 만든다는 것인지 분명하지 않았다는 것이다.
jhiggins777는 LLM 특유의 짧고 경구 같은 문장이 자연스럽게 펼쳐지는 대신 개념적으로만 연결된 채 이어진다며, 좋은 설명 영상에는 서사와 설명을 다듬는 인간 교사가 필요하다고 말한다.[^jhiggins777]
페이지 이름이 LaunchVideo, 곧 출시 영상이라는 점을 보면 제품 자체는 설명이 아니라 홍보를 목표로 한다.
문제는 HN 제목과 반응이 이것을 설명 영상의 성공으로 받아들였다는 데 있다.

### 속도와 화려함이 이해를 대신한다

freedomben은 영상이 너무 빨라서 주제를 모르는 사람은 각 슬라이드를 읽을 시간이 없다고 말한다.[^freedomben]
Tsarp도 이런 데모는 가능한 한 많은 애니메이션과 전환을 밀어 넣어 영상이 끝나면 무엇을 가져가야 할지 알기 어렵고, 더 많은 사람이 얼마나 화려해 보이느냐보다 배움을 최적화하기를 바란다고 한다.[^Tsarp]
sznio는 이런 영상들이 모두 비슷한 분위기를 갖고 있어서 몇 주 안에 누구나 알아보게 되고, 그러면 좋은 영상이 아니게 될 것이라고 말한다.[^sznio]

이 비판들은 도구의 구조와 연결된다.
에이전트가 스스로 확인할 수 있는 것은 `check_scene`이 보고하는 JavaScript 오류와 화면에 보이는 글자뿐이다.
글자가 화면에 떴는지는 확인할 수 있지만, 사람이 그 글자를 읽을 시간이 있었는지, 장면의 흐름이 이해를 쌓는지는 확인할 수 없다.
검증 도구가 확인할 수 있는 것만 최적화되면, 영상은 오류 없이 빽빽하고 빠른 방향으로 기운다.

### 제품을 모르면 영상도 모른다

etchalon은 자기 보드게임 참고 자료 사이트를 넣었더니, 데이터를 중앙화한다는 모호한 목표를 가진 AI 스타트업에 대한 영상이 나왔다고 말한다.[^etchalon]
이 사례는 도구의 전제가 무엇인지 드러낸다.
`web_fetch`는 페이지 텍스트, 헤딩, 색상, 글꼴을 가져오지만, 제품이 무엇인지 이해하려면 그 이상의 맥락이 필요하다.
예시로 고른 NVIDIA, Linear, Jev는 모델이 이미 학습 데이터에서 아는 회사이고, 홈페이지가 전형적인 스타트업 소개 형식을 따른다.

모델이 모르는 제품, 전형적이지 않은 사이트에서는 모델이 빈자리를 가장 흔한 이야기, 곧 AI 스타트업의 서사로 채운다.
편집 없이 한 번 실행한 결과라는 문구는 공정해 보이지만, 어떤 입력을 예시로 골랐는지가 이미 편집이다.
v64가 모델 출시 때의 데모는 처음에 회의적으로 봐야 한다고 말한 것도 이런 선택 효과를 겨냥한다.[^v64]

## 인사이트

### 애니메이션 라이브러리의 가치가 “사람이 쓰기 좋은 API”에서 “모델이 쓰기 좋은 표면”으로 옮겨 간다

prathje는 Remotion과 Motion Canvas 같은 애니메이션 라이브러리가 오래 있었는데, 에이전트가 유능해질수록 라이브러리의 가치가 점점 줄어드는 것 같다고 말한다.[^prathje-libs]
nutanc도 이제 Remotion 같은 것이 필요 없어지느냐고 묻는다.[^nutanc]
LaunchVideo가 보여 주는 것은 라이브러리 없이 평범한 HTML, CSS, JavaScript만으로도 모델이 영상을 쓸 수 있다는 점이다.

그러나 이것은 라이브러리가 사라진다는 뜻이라기보다 라이브러리의 역할이 바뀐다는 뜻이다.
사람을 위한 라이브러리는 애니메이션을 쉽게 쓰게 해 주는 추상화를 판다.
모델은 추상화 없이도 긴 코드를 쓸 수 있으므로, 모델에게 필요한 것은 쓰기 쉬운 API보다 결과를 확인할 수 있는 표면, 곧 결정적 렌더링, 특정 시각의 상태 조회, 오류 보고다.
LaunchVideo에서 실제로 새로운 부분이 가상 시계와 `check_scene`인 것도 그래서다.
앞으로의 영상 도구는 모델이 쓰기 좋은 문법보다 모델이 자기 결과를 볼 수 있는 눈을 파는 쪽으로 갈 것이다.

### 80%는 자동화되고 나머지 20%가 제품이 된다

기업 마케팅 영상 서비스를 만드는 neebz는 고객과 일해 보니 80 대 20 법칙이 그대로라고 말한다.[^neebz]
80%는 AI가 몇 초 만에 하고, 고객이 원하는 것을 정확히 얻기 위한 20%는 몇 분의 수작업이라는 것이다.
LaunchVideo는 편집 없이 한 번 실행하는 것을 자랑하지만, 실제 사업이 되는 지점은 그 한 번 실행 뒤다.

코드로 만든 영상은 이 20%를 다루는 데 유리하다.
영상 생성 모델의 결과는 고치려면 다시 생성해야 하지만, HTML 영상은 대사 한 줄, 색 하나, 장면 길이 하나를 바로 고칠 수 있다.
gAI가 After Effects 스크립트로 내보내 기존 도구에서 다듬는 방식도 같은 이야기다.
그래서 이런 도구의 경쟁력은 첫 결과의 화려함이 아니라, 첫 결과를 사람이 얼마나 쉽게 고칠 수 있느냐에서 나온다.
편집 없음을 자랑하는 데모는 정작 제품이 될 부분을 보여 주지 않는다.

### 설명 영상이 싸지면 설명 영상의 신호 가치가 사라진다

GN에 실린 요약에도 소개된 LastTrain의 댓글은 설명 영상이 광고를 보여 주려고 글로 된 사용법을 대체한 다크 패턴이었다고 말한다.[^LastTrain]
Google이 AI 우선 검색으로 바뀐 뒤 이런 영상이 검색 결과에 덜 뜨는 것이 몇 안 되는 좋은 변화라는 것이다.
hypfer도 이런 콘텐츠는 AI 이전에도 이미 쓰레기였으니 잃은 것은 없다고 말한다.[^hypfer]

출시 영상은 오랫동안 회사가 제품에 돈과 시간을 들였다는 신호였다.
모션 디자이너를 고용하고 몇 주를 들여 만든 영상은, 그 회사가 진지하다는 것을 간접적으로 보여 줬다.
영상 하나에 4분과 10만 토큰이 들면 이 신호는 사라진다.
slawton3가 이 형식의 영상을 이제 어디서나 보게 될 것이라고 한 대로,[^slawton3] 출시 영상이 모든 스타트업의 기본 장비가 되면 사람들은 영상을 보고 제품의 진지함을 판단하지 않게 된다.
그때 다시 가치를 얻는 것은 remywang이 말한 대본, 곧 누군가 시간을 들여 무엇을 어떤 순서로 설명할지 고민한 흔적일 것이다.

---

[^minimaxir]: <https://news.ycombinator.com/item?id=49837044>

[^gAI]: <https://news.ycombinator.com/item?id=49837443>

[^cush]: <https://news.ycombinator.com/item?id=49838377>

[^bilsbie]: <https://news.ycombinator.com/item?id=49843468>

[^prathje-sense]: <https://news.ycombinator.com/item?id=49841151>

[^amelius]: <https://news.ycombinator.com/item?id=49837287>

[^ndom91]: <https://news.ycombinator.com/item?id=49843094>

[^remywang]: <https://news.ycombinator.com/item?id=49847759>

[^lern_too_spel]: <https://news.ycombinator.com/item?id=49836834>

[^armchairhacker]: <https://news.ycombinator.com/item?id=49841648>

[^jhiggins777]: <https://news.ycombinator.com/item?id=49845121>

[^freedomben]: <https://news.ycombinator.com/item?id=49843799>

[^Tsarp]: <https://news.ycombinator.com/item?id=49839356>

[^sznio]: <https://news.ycombinator.com/item?id=49837570>

[^etchalon]: <https://news.ycombinator.com/item?id=49836988>

[^v64]: <https://news.ycombinator.com/item?id=49840171>

[^prathje-libs]: <https://news.ycombinator.com/item?id=49841226>

[^nutanc]: <https://news.ycombinator.com/item?id=49843857>

[^neebz]: <https://news.ycombinator.com/item?id=49840977>

[^LastTrain]: <https://news.ycombinator.com/item?id=49842630>

[^hypfer]: <https://news.ycombinator.com/item?id=49836735>

[^slawton3]: <https://news.ycombinator.com/item?id=49848110>
