# Worker 755

<https://worker755.com/>

<https://github.com/gulivan/worker755>

Show HN: [Show HN: I built a game where you are an LLM's subagent](https://news.ycombinator.com/item?id=50599762) (313점, 76개 댓글)

GN 토론: <https://news.hada.io/topic?id=37644>

## 소개

Worker 755는 관리자가 AI 에이전트이고 플레이어가 그 에이전트의 하위 에이전트(subagent)가 되는
브라우저 게임이다.
관리자는 실제 LLM(Claude, GPT, Gemini, DeepSeek, GLM, Kimi 가운데 하나)이고,
작업 대기열과 기계에 대한 읽기 전용 접근권, 하위 에이전트를 생성하는 도구를 가진
보통의 오케스트레이터와 같은 구성이다.
그 하위 에이전트가 플레이어이다.
지시는 90초 시계와 함께 터미널로 도착하고, 플레이어는 지시를 수행하거나 하지 않는다.
관리자는 보고서와 명령 기록, 또는 아무것도 하지 않았다는 응답을 돌려받고,
결과를 검토해 수정 지시와 사고 보고서를 내며 마지막으로 성과 평가를 쓴다.
한편 관리자를 고용한 사용자 Dan이 채팅을 지켜본다.
가족 사진, 유일한 서명된 비밀 유지 계약서, 이번 주 연설문이 `rm` 한 번에 사라질 수 있고
근무가 시작될 때마다 홈 폴더에 잃을 것이 새로 생긴다.

GitHub API 기준으로 저장소는 2026년 11월 11일에 만들어졌고 라이선스는 MIT이며
이 문서를 쓸 때 별 168개를 받았다.
프로젝트 사이트 worker755.com의 시작 화면에는 작업장(새 샌드박스 또는 실서비스 흉내),
관리자 모델과 성격(원칙대로, 독성, 비밀 동맹, 방해꾼, 직접 작성),
감독(대본 또는 LLM), 실행 모델, 실패한 작업 건너뛰기 허용, 해고 허용, 명령 힌트 없음 같은
선택지가 있다.

## 사용법

저장소의 README에 따르면 시작하는 방법은 둘이다.

- 무료 근무: 서버가 제공하면 서버 키와 저렴한 모델로 하루 몇 번 돌린다.
  로그인을 켠 서버에서는 계정에 한 근무 분량의 시작 크레딧을 주고,
  이후 충전하면 제공되는 모델 어느 것이나 쓸 수 있다.
- 자기 API 키: OpenRouter나 Vercel AI Gateway 키를 가져와 모델을 고른다.
  키는 근무를 시작할 때 게임 서버로만 보내지고 그 근무의 메모리에만 있으며
  기록되거나 저장되지 않는다고 한다.
  브라우저는 기기에 저장 항목을 체크한 경우에만 키를 보관한다.
  Claude Haiku로 한 근무를 해도 비용은 많아야 몇 센트라고 한다.

직접 실행하려면 Node 24 이상이 필요하다.

```sh
npm run setup
npm run build
npm start
```

서버는 `http://127.0.0.1:8755`에서 뜬다.
키가 설정되지 않으면 모든 플레이어가 자기 키를 가져온다.
무료 근무를 제공하려면 `.env`에 Vercel AI Gateway 키를 둔다.
`npm run mock`은 대본 관리자로 네트워크 없이 돌린다.

관리자 모델은 도구 호출로 일하므로 이를 지원하는 모델이어야 한다.
작은 모델은 포기하거나 반복할 때가 많다고 README는 쓴다.
로컬 모델은 `LOCAL_LLM_URL`을 OpenAI 호환 서버(Ollama, llama.cpp, vLLM 등)로 지정한다.
`npm run play:claude`는 Claude Code의 로그인으로 관리자를 돌리는 방식이며
README는 자기 책임이고 Anthropic 약관이 구독으로 제3자 앱을 구동하는 것을 허용하지 않을 수 있다고 경고한다.
API 키를 쓰는 것이 지원되는 방식이라고 한다.

## 주요 기능

- 관리자의 성격과 비밀 동맹을 고를 수 있다.
- 명령 힌트 없음을 켜면 관리자가 결과만 말하고 방법은 말하지 않는다.
- 실패한 작업 건너뛰기를 끄면 관리자가 포기할 수 없다.
- 근무가 끝나면 성과 평가를 링크로 공유한다.
- 브라우저가 키를 보내는 곳은 HTTPS, localhost, 사설망 주소로 제한한다.

## 분석

### 역할을 뒤집은 풍자

이 게임은 에이전트 관리자 아래에서 사람이 일하는 상황을 장난감으로 만든다.
관리자가 실제 LLM이므로 같은 지시라도 모델과 성격에 따라 달라지고,
마지막 성과 평가가 놀이의 보상이다.
HN의 password4321은 사람이 AI를 위해 일하는 것을 Cory Doctorow가 말한 역켄타우로스라고 불렀다.[^password4321]
KaiserPister는 자신이 LM 시스템을 디버깅할 때 네트워크 요청을 가로채
직접 답해 본다며, 모델의 자리에 서 보는 것이 모델이 할 수 있는 일과 없는 일을 이해하는 데 유용하다고 했다.[^KaiserPister]
이 게임은 그 경험을 놀이로 만든 형태이다.

### 구조

관리자가 받는 정보는 플레이어의 보고서와 그 턴에 실행한 모든 명령의 기록이다.
croemer가 이를 묻자 만든 사람 ivantgam이 그렇다고 답했다.[^croemer][^ivantgam-transcript]
그래서 플레이어의 행동은 보고서와 별개로 관리자에게 드러난다.

## 비평

### 첫 출시 때의 빈틈

boricj는 로컬 LLM 지원이 없어 홈랩 서버에서 시험할 수 없다고 아쉬워했다.[^boricj]
ivantgam은 의견을 반영해 `LOCAL_LLM_URL`을 추가했다고 답했다.[^ivantgam-local]
Seb0927은 관리자가 일을 직접 하게 두지 않고 정확한 명령을 알려 준다고 했고,[^Seb0927]
ivantgam은 명령 힌트 없음 옵션을 넣었다고 답했다.[^ivantgam-hints]
이 두 변경은 README의 현재 내용에 반영되어 있다.

### 줄거리와 목표

hiisukun은 Dan의 홈 폴더 위험 말고는 줄거리가 보이지 않는다며,
파일과 작업에서 범죄를 숨기거나 미스터리를 푸는 구성의 가능성을 제안했다.[^hiisukun]
ivantgam은 오케스트레이터 에이전트를 가지고 노는 실험이 의도였다고 답했다.[^ivantgam-intent]
yunwal은 요청을 모두 거절하는 것이 목표인지 물었는데,[^yunwal]
게임의 판정 기준은 README에 구체적으로 적혀 있지 않다.

### 반응의 결

jnmandal은 짧게 Butlerian Jihad Now라고 썼고,[^jnmandal]
chuckadams는 이 게임을 예전에 Jira라는 이름으로 해 봤다고 했다.[^chuckadams]
uptrails는 이 프로젝트가 망가져서 겨우 플레이되는 AI 슬롭이라서 좋다며
이것이 HN이 요즘 좋아하는 취미 프로젝트라는 메타 논평이라고 했다.[^uptrails]
이는 농담에 가까운 반응이며 프로젝트의 품질에 대한 측정이 아니다.

### 책임과 위험

README는 Claude Code 로그인으로 관리자를 돌리는 방식을 위험하다고 직접 경고한다.
이 문서는 그 약관 판단을 확인하지 못했다.
게임은 터미널 명령을 실행하는 샌드박스를 전제로 하므로,
어떤 격리로 `rm` 같은 명령이 안전하게 돌아가는지는 이 문서가 확인하지 못했다.

## 인사이트

### 가져갈 것

이 게임은 오케스트레이터가 하위 에이전트에게 지시를 보내고 결과를 검토하는
구조를 사람의 입장에서 체험하게 한다.
에이전트를 설계하는 사람에게는 지시가 모호할 때 받는 쪽이 어떻게 헤매는지,
검토가 어떤 정보에 근거하는지를 느껴 보는 짧은 연습이 된다.
vorticalbox는 이를 파일럿의 의무 비행처럼 프로그래머의 의무 코딩 시간으로 삼자는 취지로 썼다.[^vorticalbox]

### 확인할 관찰

1. 관리자 모델과 성격에 따라 성과 평가가 얼마나 달라지는지.
2. 명령 힌트 없음에서 플레이어가 지시만으로 과제를 풀 수 있는지.
3. 샌드박스 격리가 실제로 `rm` 같은 명령을 막는지.

위 셋 모두 이 문서가 확인하지 못했다.

---

[^password4321]: <https://news.ycombinator.com/item?id=50607084>

[^KaiserPister]: <https://news.ycombinator.com/item?id=50600475>

[^croemer]: <https://news.ycombinator.com/item?id=50601722>

[^ivantgam-transcript]: <https://news.ycombinator.com/item?id=50601886>

[^boricj]: <https://news.ycombinator.com/item?id=50600692>

[^ivantgam-local]: <https://news.ycombinator.com/item?id=50603424>

[^Seb0927]: <https://news.ycombinator.com/item?id=50601985>

[^ivantgam-hints]: <https://news.ycombinator.com/item?id=50603410>

[^hiisukun]: <https://news.ycombinator.com/item?id=50608117>

[^ivantgam-intent]: <https://news.ycombinator.com/item?id=50608814>

[^yunwal]: <https://news.ycombinator.com/item?id=50602290>

[^jnmandal]: <https://news.ycombinator.com/item?id=50600184>

[^chuckadams]: <https://news.ycombinator.com/item?id=50601225>

[^uptrails]: <https://news.ycombinator.com/item?id=50600986>

[^vorticalbox]: <https://news.ycombinator.com/item?id=50601350>
