---
name: git-sync
description: Commit changes and push to the remote repository
---

Sync local changes to the remote repository:

1. Check changes with `git status` and `git diff`
2. Stage modified and new files
3. Write a concise commit message summarizing the changes and commit
4. Pull from remote with rebase to update to the latest state (always run,
   even if there are no changes)
5. Push to the remote branch (if there are commits)

## Commit message rules

- No prefix (do not use `sync:`, `feat:`, `fix:`, etc.)
- Always write both a subject and a body
- In the body, explain specifically why the change was made and what changed
- Always include a Co-Authored-By trailer at the end (based on the model in
  use)

On conflicts or push failures, explain the cause.
