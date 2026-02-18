codex exec "
  다음 소스에서 최근 48시간 이내에 올라온 개발자 트렌드 주제 10개를 찾아줘:
  - Hacker News (top/new)
  - dev.to 트렌딩

  선정 기준:
  - 조회수/댓글/스타 수 등 실제 반응이 많은 것 우선
  - 실용적으로 바로 써먹을 수 있는 것 우선
  - 단순 뉴스보다 기술적 깊이가 있는 것 우선

  sandbox.md 파일에 오늘 날짜(YYYY-MM-DD)와 트렌드 주제를 조합한
  '## YYYY-MM-DD 개발자 트렌드' 형식의 h2 섹션을 새로 추가하고,
  그 아래에 각 항목을 다음 형식으로 작성해 줘:

  ### {번호}. {제목}

  - **출처**: {사이트명} — <{URL}>
  - **한 줄 요약**: {핵심 내용을 한 문장으로}
  - **왜 주목받나**: {커뮤니티 반응과 인기 이유}
  - **개발자 관점 인사이트**:
    - 이 기술/이슈가 실무에 어떤 영향을 주는지
    - 지금 당장 써먹을 수 있다면 어떻게 활용할 수 있는지
    - 앞으로 어떤 방향으로 흘러갈 것 같은지 (트렌드 예측)
    - 놓치면 안 되는 핵심 포인트나 주의사항
"

npx prettier --write sandbox.md

git add sandbox.md

codex exec '
  git diff --staged 내용을 기반으로 Git Commit Message를 작성하고,
  /tmp/til-update-sandbox-commit-message.txt 파일에 저장해줘.
'

git commit -F /tmp/til-update-sandbox-commit-message.txt

git fetch origin --prune

git pull --rebase

git push
