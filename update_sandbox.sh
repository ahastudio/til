#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

SANDBOX_FILE="sandbox.md"
TODAY="$(date +%Y-%m-%d)"
COMMIT_MESSAGE_FILE="$(mktemp -t til-update-sandbox-commit-message)"
CODEX_MODEL="gpt-5.6-sol"
CODEX_REASONING_EFFORT="high"
CO_AUTHOR="Codex GPT-5.6-Sol <noreply@openai.com>"

trap 'rm -f "$COMMIT_MESSAGE_FILE"' EXIT

if [ ! -f "$SANDBOX_FILE" ]; then
  echo "error: $SANDBOX_FILE 파일이 없습니다." >&2
  exit 1
fi

run_codex() {
  codex exec \
    -m "$CODEX_MODEL" \
    -c model_reasoning_effort="$CODEX_REASONING_EFFORT" \
    "$1"
}

commit_sandbox() {
  git add "$SANDBOX_FILE"

  run_codex "
  이 저장소의 규칙 파일은 '_agent/rules/' 에 있다. '.agent/' 가 아니다.
  커밋 메시지 규칙은 '_agent/rules/git-commit-message.md' 를 읽고 그대로 따른다.

  git diff --staged 내용을 기반으로 Git Commit Message를 작성하고,
  ${COMMIT_MESSAGE_FILE} 파일에 저장해줘.
  " || echo "warning: 커밋 메시지 생성이 실패했습니다." >&2

  if [ ! -s "$COMMIT_MESSAGE_FILE" ]; then
    echo "warning: 커밋 메시지가 비어 있어 기본 메시지를 사용합니다." >&2
    cat > "$COMMIT_MESSAGE_FILE" <<EOF
Add ${TODAY} developer trends

Record today's developer trends from Hacker News and GitHub Trending.
The commit message generator returned nothing, so this default is used.
EOF
  fi

  # 모델은 자기 이름을 모르고 추측해서 쓰므로 트레일러는 스크립트가 붙인다.
  { grep -iv '^Co-Authored-By:' "$COMMIT_MESSAGE_FILE" || true; } \
    | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}' \
    > "$COMMIT_MESSAGE_FILE.tmp"
  printf '\nCo-Authored-By: %s\n' "$CO_AUTHOR" >> "$COMMIT_MESSAGE_FILE.tmp"
  mv "$COMMIT_MESSAGE_FILE.tmp" "$COMMIT_MESSAGE_FILE"

  git commit -F "$COMMIT_MESSAGE_FILE"
}

add_today_section() {
  local existing_urls new_urls duplicated

  existing_urls="$(grep -oE '<https?://[^>]+>' "$SANDBOX_FILE" \
    | tr -d '<>' \
    | sort -u)"

  echo "기존 URL $(echo "$existing_urls" | wc -l | tr -d ' ')개를 중복 제외 목록으로 전달합니다."

  run_codex "
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
${existing_urls}
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
" || echo "warning: 트렌드 생성이 실패했습니다." >&2

  if ! grep -q "^## ${TODAY} 개발자 트렌드" "$SANDBOX_FILE"; then
    echo "warning: ${TODAY} 섹션이 추가되지 않았습니다." >&2
    return
  fi

  # git diff에서 뽑으면 prettier가 다시 감싼 옛 줄의 URL까지 잡힌다.
  new_urls="$(awk -v header="## ${TODAY} 개발자 트렌드" \
    'index($0, header) == 1 { found = 1 } found' "$SANDBOX_FILE" \
    | grep -oE '<https?://[^>]+>' \
    | tr -d '<>' \
    | sort -u || true)"

  duplicated="$(comm -12 \
    <(echo "$existing_urls") \
    <(echo "$new_urls"))"

  if [ -n "$duplicated" ]; then
    echo "warning: 이미 등장한 URL이 다시 추가되었습니다:" >&2
    echo "$duplicated" >&2
  fi

  echo "새 URL $(echo "$new_urls" | wc -l | tr -d ' ')개를 추가했습니다."
}

if grep -q "^## ${TODAY} 개발자 트렌드" "$SANDBOX_FILE"; then
  echo "${TODAY} 섹션이 이미 있어서 가져오기를 건너뜁니다."
else
  add_today_section
fi

npx prettier --write "$SANDBOX_FILE"

if git diff --quiet -- "$SANDBOX_FILE"; then
  echo "${SANDBOX_FILE}에 커밋할 변경이 없습니다."
else
  commit_sandbox
fi

git fetch origin --prune
git pull --rebase --autostash
git push
