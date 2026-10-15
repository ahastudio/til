# hamzafer/claude-code-mods: 바로 설치해 쓰는 Claude Code mod 모음

<https://github.com/hamzafer/claude-code-mods>

## 소개

Claude Code의 함수 훅(function hook) 위에 만든 플러그인,
즉 mod를 모아 둔 저장소다.
README는 목표를
“Claude Code가 하는 일을 보이게 하라(Make Claude Code show what it's doing)”로 내건다.
프롬프트 위에 실시간으로 갱신되는 줄,
위험한 명령을 붙잡는 가드, 대화 옆의 창, 게임까지
mod 25개를 하나의 마켓플레이스로 배포하고, 원하는 것만 골라 설치하게 한다.
라이선스는 MIT이고, 2026년 10월 2일에 만들어져 10월 15일 기준 스타 249개다.

mod가 무엇인지와 직접 만드는 법은
[Claude Code mods 입문](claude-code-mods.md)에 정리되어 있다.
이 저장소는 그 API로 만든 결과물을 실제로 써 보는 쪽의 출발점이다.

## 설치하기

마켓플레이스를 한 번 추가한 뒤 이름으로 설치한다.

```bash
claude plugin marketplace add hamzafer/claude-code-mods
claude plugin install context-bar@claude-code-mods
```

README는 범용 mod 12개를 한 번에 설치하는 반복문도 제공한다.

```bash
for m in context-bar token-weather usage-meter heatmap where-am-i next-steps agent-radar review-watch replay-theater md-preview blast-radius mission-control; do
  claude plugin install "$m@claude-code-mods"
done
```

설치한 뒤에는 Claude Code를 다시 시작한다.
설치하지 않고 한 번 써 보려면 저장소를 받아 `--plugin-dir`로 띄운다.

```bash
git clone https://github.com/hamzafer/claude-code-mods && cd claude-code-mods
claude --plugin-dir mods/context-bar
```

Claude Code 2.1.287 이상이 필요하고,
일부 mod는 Chrome, `gh`, 커넥터 같은 것을 추가로 요구한다.

## 주요 mod

### 보이게 하기

| mod             | 하는 일                                                                               | 명령                 |
| --------------- | ------------------------------------------------------------------------------------- | -------------------- |
| mission-control | 서브에이전트, 도구 호출, 그들이 건드리는 파일을 대화 옆 창에 실시간으로 표시          | `/mission`           |
| context-bar     | 컨텍스트 창 사용량을 범주별 색의 막대 하나로, 압축 지점까지 표시                      | `/context-bar`       |
| token-weather   | 컨텍스트가 찬 정도를 Clear에서 Compact soon까지 날씨로, 프롬프트 캐시 카운트다운 포함 |                      |
| cache-clock     | 프롬프트 캐시 남은 시간, 적중률, 식으면 다시 캐시할 토큰                              | `/cache-clock setup` |
| where-am-i      | 세션 목표, 지금 하는 일, 사용자를 기다리는 것, 다음 단계                              | `/where`             |
| next-steps      | 턴마다 다음 프롬프트 후보 2~3개, 키 하나로 초안 작성                                  | `1` `2` `3`          |
| usage-meter     | 5시간·7일 요금제 사용량, 초기화까지 남은 시간, 세션 비용                              |                      |
| agent-radar     | 실행 중인 서브에이전트마다 한 줄                                                      | `/radar`             |
| review-watch    | 실행 중인 코드 리뷰(Codex 또는 리뷰 서브에이전트)마다 한 줄, 끝나면 결과 알림         |                      |
| replay-theater  | 마지막 턴의 편집을 diff 하나씩 넘겨 보기                                              | `/replay`            |
| md-preview      | Claude가 편집한 Markdown을 GitHub처럼 렌더해 전후를 나란히 표시                       | `/md`                |

### 막기와 아끼기

| mod          | 하는 일                                                                                           | 명령     |
| ------------ | ------------------------------------------------------------------------------------------------- | -------- |
| blast-radius | `rm -r`, 강제 푸시, 마이그레이션을 붙잡아 무엇이 지워지는지 보여 주고, 60초 동안 답이 없으면 취소 |          |
| switchboard  | 모델을 지정하지 않은 서브에이전트의 모델을 짧은 레이블만 보고 고르고, 서브에이전트별 비용 표시    | `/route` |

저자는 이 밖에 자기 도구와 규칙에 맞춘 mod(merge-gate, rulebook-guard 등)를
“포크해서 고쳐 쓰라”고 따로 분류하고,
reels, snake, now-playing 같은 놀이용 mod도 둔다.
mission-control의 코드 지도 화면은 macOS, Chrome, 이미지를 보여 주는 터미널
(Ghostty, kitty, iTerm2)이 있어야 한다.

다른 사람이 만든 mod도 README의 커뮤니티 표에 모은다.
그중 mod-store는 창 안에서 약 2,700개의 커뮤니티 mod를 찾아 설치하게 하고,
설치 전에 각 mod가 무엇에 접근하는지 보여 준다고 소개된다.

## 고르는 기준

### 관찰하는 mod와 개입하는 mod를 나눈다

모음의 mod는 대부분 관찰만 한다.
context-bar, usage-meter,
agent-radar 같은 mod는 세션 이벤트를 읽어 화면에 그릴 뿐
Claude Code의 동작을 바꾸지 않으므로, 실패해도 원래 동작이 남는다.
반면 blast-radius, merge-gate, rulebook-guard, switchboard는
명령을 붙잡거나 고쳐 쓰거나 모델을 바꾼다.
이런 mod는 설치하기 전에 코드를 읽고, 내 작업 방식과 맞는지 확인할 가치가 크다.
특히 rulebook-guard는 저자의 글쓰기·git 규칙을 그대로 강제하므로
그대로 설치하면 내 규칙이 아니라 저자의 규칙이 적용된다.

### 화면 자리는 한정되어 있다

프롬프트 위의 띠와 대화 옆의 창은 여러 mod가 함께 쓰는 공간이다.
줄을 그리는 mod를 여러 개 설치하면 띠가 길어지고,
같은 정보를 두 번 보여 주는 조합(token-weather와 context-bar,
usage-meter와 커뮤니티의 usage-limits)도 생긴다.
한 번에 전부 설치하는 반복문보다,
지금 가장 궁금한 정보 하나부터 설치하는 편이 낫다.

### 외부 서비스에 기대는 mod는 비용과 키가 따른다

switchboard는 OpenAI의 Decisions API나 Jev를 부르고,
openai-balance는 OpenAI 조직 관리자 키를,
glance는 Google Calendar, Linear, Slack 커넥터를 요구한다.
편해지는 만큼 키와 데이터가 그 서비스로 나간다는 점을 감안해야 한다.

## 함정

- mod는 Claude Code와 같은 권한으로 내 컴퓨터에서 돈다. 이 저장소의 mod도 Anthropic이 아니라 저자가 쓴 코드이고, 커뮤니티 표의 mod는 README 스스로 여기서 관리하지 않으니 코드를 읽고 설치하라고 적는다.
- blast-radius 같은 가드는 명령 문자열을 읽는 안전망이다. 확실히 막아야 할 명령은 권한 규칙이나 샌드박스에 둔다.
- 설치 뒤 재시작하지 않으면 mod가 불러와지지 않는다.
- mod API는 Claude Code 릴리스마다 바뀔 수 있으므로, 업데이트 뒤 화면이 이상하면 mod 버전부터 확인한다.
- 일부 mod의 버전 요구는 기본값과 다르다. cache-clock은 Node와 Claude Code 2.1.251 이상을 따로 적는다.

## 기억할 원칙

### 보이게 하는 것이 mod의 첫 번째 쓸모다

이 모음이 가장 많이 담은 것은 무언가를 막거나 자동화하는 mod가 아니라
컨텍스트, 캐시, 사용량, 서브에이전트, 리뷰처럼
지금까지 보이지 않던 상태를 화면에 올리는 mod다.
에이전트에게 일을 많이 맡길수록 사람이 개입할 시점을 아는 것이 중요해지고,
그 판단은 보이는 정보의 양에 기댄다.
mod를 처음 들인다면 개입하는 것보다 보여 주는 것부터 시작하는 편이 위험이 작다.
