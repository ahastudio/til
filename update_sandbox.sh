#!/usr/bin/env bash
#
# sandbox.md에 오늘의 개발자 트렌드 섹션을 추가하고 커밋·푸시한다.
#
# 중복 방지는 프롬프트가 아니라 이 스크립트가 책임진다.
# sandbox.md는 3MB가 넘어서 모델이 전체를 읽고 중복을 판단할 수 없기 때문에,
# 기존 URL 목록을 여기서 뽑아 프롬프트에 직접 넣는다.

set -euo pipefail

cd "$(dirname "$0")"

SANDBOX_FILE="sandbox.md"
TODAY="$(date +%Y-%m-%d)"
COMMIT_MESSAGE_FILE="$(mktemp -t til-update-sandbox-commit-message)"

trap 'rm -f "$COMMIT_MESSAGE_FILE"' EXIT

if [ ! -f "$SANDBOX_FILE" ]; then
  echo "error: $SANDBOX_FILE 파일이 없습니다." >&2
  exit 1
fi

# 오늘 섹션이 이미 있으면 중복 실행이므로 멈춘다.
if grep -q "^## ${TODAY} 개발자 트렌드" "$SANDBOX_FILE"; then
  echo "error: ${TODAY} 섹션이 이미 있습니다. 중복 실행으로 보입니다." >&2
  exit 1
fi

# 작업 트리가 깨끗한지 확인한다.
# 관계없는 변경이 섞인 채로 자동 커밋·푸시되는 것을 막는다.
if ! git diff --quiet || ! git diff --staged --quiet; then
  echo "error: 커밋하지 않은 변경이 있습니다. 정리한 뒤 다시 실행하세요." >&2
  git status --short >&2
  exit 1
fi

# 기존에 등장한 URL을 모두 뽑는다. 이 목록이 중복 방지의 근거가 된다.
EXISTING_URLS="$(grep -oE '<https?://[^>]+>' "$SANDBOX_FILE" \
  | tr -d '<>' \
  | sort -u)"

echo "기존 URL $(echo "$EXISTING_URLS" | wc -l | tr -d ' ')개를 중복 제외 목록으로 전달합니다."

codex exec "
이 저장소의 규칙 파일은 '_agent/rules/' 에 있다. '.agent/' 가 아니다.
마크다운 작성 규칙은 '_agent/rules/writing-guidelines.md' 를 읽고 따른다.

다음 소스에서 최근 48시간 이내에 올라온 개발자 트렌드 주제 10개를 찾아줘:
- Hacker News (top/new)
- GitHub Trending (오늘 기준)

선정 기준:
- 조회수/댓글/스타 수 등 실제 반응이 많은 것 우선
- 실용적으로 바로 써먹을 수 있는 것 우선
- 단순 뉴스보다 기술적 깊이가 있는 것 우선

중복 방지 규칙 (반드시 준수):
아래는 ${SANDBOX_FILE}에 이미 등장한 URL 전체 목록이다.
이 목록에 있는 URL은 절대 추가하지 마.
목록에 없더라도 같은 프로젝트나 같은 기사를 가리키는 항목은 추가하지 마.
후보가 10개에 못 미치면 억지로 채우지 말고 새로운 항목만 써.
${SANDBOX_FILE} 파일 자체는 3MB가 넘으니 통째로 읽지 마.

--- 이미 등장한 URL 목록 시작 ---
${EXISTING_URLS}
--- 이미 등장한 URL 목록 끝 ---

${SANDBOX_FILE} 파일 맨 끝에 아래 형식의 h2 섹션을 새로 추가해:

## ${TODAY} 개발자 트렌드

그 아래에 각 항목을 다음 형식으로 작성해 줘:

### {번호}. {제목}

- **출처**: {사이트명} — <{URL}>
- **한 줄 요약**: {핵심 내용을 한 문장으로}
- **왜 주목받나**: {커뮤니티 반응과 인기 이유}
- **개발자 관점 인사이트**:

출력 형식 강제 규칙 (반드시 준수):
- '- **개발자 관점 인사이트**:' 뒤에는 반드시 하위 불릿 4개를 줄바꿈으로 작성해.
- 네 개의 하위 불릿은 반드시 다음 라벨로 시작해:
  1) '이 기술/이슈가 실무에 어떤 영향을 주는지:'
  2) '지금 당장 써먹을 수 있다면 어떻게 활용할 수 있는지:'
  3) '앞으로 어떤 방향으로 흘러갈 것 같은지 (트렌드 예측):'
  4) '놓치면 안 되는 핵심 포인트나 주의사항:'
- '실무 영향: ... 즉시 활용: ... 방향: ... 주의: ...'처럼 한 줄 문단으로 합치지 마.
- 각 하위 불릿은 한 문장 이상으로 구체적으로 작성해.
"

# 모델이 실제로 오늘 섹션을 추가했는지 확인한다.
# 확인하지 않으면 빈 커밋이나 엉뚱한 커밋으로 이어진다.
if ! grep -q "^## ${TODAY} 개발자 트렌드" "$SANDBOX_FILE"; then
  echo "error: ${TODAY} 섹션이 추가되지 않았습니다." >&2
  exit 1
fi

npx prettier --write "$SANDBOX_FILE"

# prettier 실행 후에도 변경이 남아 있는지 본다.
if git diff --quiet -- "$SANDBOX_FILE"; then
  echo "error: ${SANDBOX_FILE}에 변경이 없습니다." >&2
  exit 1
fi

# 새로 추가된 URL이 기존 목록과 겹치지 않는지 스크립트가 직접 검증한다.
NEW_URLS="$(git diff -- "$SANDBOX_FILE" \
  | grep -E '^\+' \
  | grep -oE '<https?://[^>]+>' \
  | tr -d '<>' \
  | sort -u)"

DUPLICATED="$(comm -12 \
  <(echo "$EXISTING_URLS") \
  <(echo "$NEW_URLS"))"

if [ -n "$DUPLICATED" ]; then
  echo "error: 이미 등장한 URL이 다시 추가되었습니다:" >&2
  echo "$DUPLICATED" >&2
  exit 1
fi

echo "새 URL $(echo "$NEW_URLS" | wc -l | tr -d ' ')개를 추가했습니다."

git add "$SANDBOX_FILE"

codex exec "
이 저장소의 규칙 파일은 '_agent/rules/' 에 있다. '.agent/' 가 아니다.
커밋 메시지 규칙은 '_agent/rules/git-commit-message.md' 를 읽고 그대로 따른다.

git diff --staged 내용을 기반으로 Git Commit Message를 작성하고,
${COMMIT_MESSAGE_FILE} 파일에 저장해줘.
"

if [ ! -s "$COMMIT_MESSAGE_FILE" ]; then
  echo "error: 커밋 메시지가 비어 있습니다." >&2
  exit 1
fi

git commit -F "$COMMIT_MESSAGE_FILE"

git fetch origin --prune
git pull --rebase
git push
