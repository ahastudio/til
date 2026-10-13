---
name: hackernews-hot
description:
  Pick hot stories from the Hacker News front page and write a TIL document
  for each with the analyze-article skill. Select top stories by points and
  only process stories that do not duplicate existing documents.
argument-hint: '[count (default 5)]'
disable-model-invocation: true
---

Pick popular Hacker News stories and, for each one, write a TIL document by
running the `analyze-article` skill on it.

**Every story is processed through the full `analyze-article` procedure,
one at a time, in point order. This skill only selects; `analyze-article`
writes. Nothing in this file relaxes any rule of `analyze-article`.**

## Usage

```text
/hackernews-hot
/hackernews-hot 3
```

- Argument: number of documents to write (default: 5)

## Procedure

### 1. Collect the front page

Fetch the current front page from the Algolia HN API. It is plain JSON and
carries points, comment counts, and the submitted URL in one request:

```bash
curl -s 'https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=60' |
  python3 -c '
import json, sys
hits = json.load(sys.stdin)["hits"]
for h in sorted(hits, key=lambda h: -(h.get("points") or 0)):
    print(h["points"], h["num_comments"], h["objectID"], h["title"], h.get("url") or "")
'
```

For each story keep: title, points, comment count, the HN item id, and the
submitted URL.

**Confirm the list is real before using it.** An empty or very short `hits`
array means the request failed, not that the front page is empty. Retry, or
fall back to `https://hacker-news.firebaseio.com/v0/topstories.json` and
fetch each item from `/v0/item/<id>.json`. Say which endpoint the list came
from when reporting the selection.

### 2. Filter

Drop these before ranking:

- Job postings (`tags` contains `job`, or the title starts with a company
  name followed by `is hiring`).
- Stories whose URL cannot be read as a source by `analyze-article` — for
  example a bare PDF behind a login, or a dead link. If unsure, keep it and
  let `analyze-article` step 1 decide; a fetch failure there is reported and
  the next story takes its place.

`Ask HN` and `Show HN` threads stay in. `analyze-article` step 4a already
defines how they are written: a `Show HN` that presents a thing with its own
address uses that address as the source and the thread as the `Show HN:` line;
an `Ask HN` without a URL uses the thread itself as the source.

### 3. Remove duplicates

For each candidate, run the duplicate check of `analyze-article` step 2 — the
source URL, its slug, the distinctive proper nouns, and the likely directory.

- A story whose source already has a document is **not** written again. It is
  excluded from the new-document count and listed in the report as a
  duplicate, with the existing path.
- A near-miss (a document that only mentions the subject) is not a
  duplicate; say so and keep the story.

After excluding duplicates, take the requested number of stories by point
order.

### 4. Report the selection

Show the selected list before writing anything. Format:

```text
1. Title (points, comments) — expected path
2. Title (points, comments) — expected path
...
```

List every excluded story with its reason (job post, duplicate of `<path>`,
unreadable). Then start writing immediately; the selection report is not a
request for approval.

### 5. Write each document with `analyze-article`

For each selected story, in point order, invoke the `analyze-article` skill
with the source URL and the chosen output path.

- Process stories one at a time, finishing each — document, format gate,
  reactions, final gate — before starting the next, exactly as the queue rules
  of `analyze-article` require.
- The HN thread this skill started from is a known reaction source. When
  `hackernews-reactions` runs inside `analyze-article` step 9, it must still
  search Algolia as its own procedure says, but it will find this thread; use
  it, fetch every top-level comment and the replies, and record the
  `HN 토론:` line with the counts the API reports at that moment.
- `lobsters-reactions` and `geeknews-reactions` run as well. Starting from HN
  says nothing about whether a Lobste.rs or GeekNews thread exists; each is
  searched independently.
- **Document title:** do not reuse the HN title as the H1. HN titles are the
  submitter's wording and are often shortened or editorialized. Write the
  Korean H1 from what the source itself says, per `analyze-article` step 3a.
- **Directory:** choose an existing directory that fits the topic. If none
  fits, do not create one — ask the user, and continue with the next story
  while waiting.
- **File name:** follow `analyze-article` step 8a exactly.

### 6. Final report

Report as a table, one row per selected story:

| Column | Content                                                    |
| ------ | ---------------------------------------------------------- |
| 순위   | Point rank on the front page                               |
| 제목   | The HN title                                               |
| 결과   | Path written, or the reason it was skipped                 |
| 반응   | HN / Lobste.rs / GN outcome, each as woven-in or not found |

Report a document as finished only after its final format gate printed `OK`.
Then list the excluded stories and their reasons.
