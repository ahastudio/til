# Special source types: Twitter, YouTube, papers, forum threads (step 4a)

## Contents

- [4a. Special source types](#4a-special-source-types)

## 4a. Special source types

Some sources need a fetch strategy or a link form of their own. Handle these
explicitly rather than improvising.

| Source type        | Fetch method                              | Source line                        |
| ------------------ | ----------------------------------------- | ---------------------------------- |
| Twitter            | Claude in Chrome (see the `web-fetching` skill)  | `트윗: [<제목 또는 첫 문장>](URL)` |
| YouTube            | `yt-dlp` info JSON + captions (see below) | `영상: [<영상 제목>](URL)`         |
| Paper (PDF/arXiv)  | WebFetch, or Read the PDF                 | `논문: [<논문 제목>](URL)`         |
| Press release      | WebFetch                                  | `원문: [<제목>](URL)`              |
| Forum post (GN/HN) | WebFetch, or the site's JSON API          | `Ask GN: [<제목>](URL)` 등         |
| GeekNews Article   | WebFetch, or curl the article page        | `GeekNews Article: [<제목>](URL)`  |

A `Show GN` / `Ask GN` / `Show HN` / `Ask HN` thread is written as a
titled link labeled with the thread's own prefix: `Show GN: [<제목>](URL)`.
Where that line goes depends on what the subject is:

- **The thread presents a thing that has its own address** (a product
  homepage, a GitHub repository, an app page). The subject is the thing, so
  the source line stays the bare `<URL>` of the thing (homepage first, then
  repo). The `Show GN:` line goes in the discussion block **in place of** the
  `GN 토론:` line (and `Show HN:` in place of `HN 토론:`). It never replaces
  or removes the bare source URL.
- **The thread itself is the only source** (an `Ask GN` question, or a post
  with no separate address). Then the labeled line is the source line.

Either way, never add both a `Show GN:` line and a `GN 토론:` line for the
same thread.

For Twitter, the service is always called Twitter in prose, never X, even
when the source writes X or 엑스; the format gate fails prose that calls it X.
For Twitter, `twitter.com` is used instead of `x.com` per
the `writing-guidelines` skill. For a long tweet, call it a `트윗`, not a `스레드`,
unless the user says otherwise.

A tweet that links to a Twitter Article (long-form post) shows only a `t.co`
link in its text; the article body renders on the same status page.
`get_page_text` cuts off around 50,000 characters, which an article with
embedded quote tweets and code blocks can exceed. Read the rest with
`javascript_tool` on `document.querySelector('article').innerText`, sliced
into chunks of under 1,000 characters, because longer return values are
truncated. Strip URLs and `?`/`&`/`=` from the text first: a return value
that contains query-string data is replaced wholesale with
`[BLOCKED: Cookie/query string data]`.

For YouTube, the first section is `## 요약` only if the video advances an
argument (a talk, an essay video). For a demo or a walkthrough, choose a
heading that fits — e.g. `## 내용`, `## 데모`.

### YouTube: fetch with `yt-dlp`, never with WebFetch

**WebFetch cannot read a YouTube video.** It returns the page title and the
site footer, with no description, no chapters and no transcript. A document
written from that is written from the title alone,
which step 4a forbids. Use `yt-dlp` instead. YouTube extraction needs a
JavaScript runtime (Deno) installed; see `cli/yt-dlp.md`.

Fetch in two calls, into a scratch directory, never into the repository:

```bash
D=<scratchpad>/yt-<video-id>
mkdir -p "$D"

# 1. metadata: title, channel, upload date, duration, description, chapters,
#    and the spoken language (`language`) plus which caption tracks exist
yt-dlp --skip-download --write-info-json -o "$D/v.%(ext)s" "<URL>"

# 2. one caption track, in the spoken language
yt-dlp --skip-download --write-auto-subs --write-subs \
  --sub-langs "<lang>-orig" --sub-format vtt --sleep-subtitles 5 \
  -o "$D/v.%(ext)s" "<URL>"
```

Rules for what comes back:

- **The source line uses `title` from the info JSON, verbatim**, including
  prefixes like `[한글자막]`.
- **Read the spoken-language track, not a translation.** Pick `<lang>` from
  the info JSON `language` field (`en-US` → `en`). The `-orig` auto track is
  speech recognition in that language; other language tracks are machine
  translations of it. Quote and paraphrase from the original-language track.
- **Request one track per call.** Asking for several languages at once is the
  usual way to hit `HTTP Error 429: Too Many Requests` on captions. On a 429,
  wait, then retry a single track once with `--sleep-subtitles`. Do not loop.
- **Auto captions repeat and misspell.** Rolling captions emit each line
  several times; de-duplicate and group by minute so you can cite timestamps.
  Speech recognition mangles proper nouns (handles, product names, company
  names). Check every name against the description, the chapters, the
  uploader's links, or another source before writing it. Never copy a name
  from the transcript unverified.
- **A re-upload is not the speaker's own channel.** Translation channels
  (`[한글자막]` and the like) re-post someone else's talk. Name the speaker,
  not the uploader, as the author, and follow the description's links to find
  the original post or event. The source line still links the URL the user
  gave.
- **No caption track at all** means the source cannot be read as text. STOP
  and report it; do not transcribe the audio unless the user asks for that.

If the source cannot be fetched at all, STOP and tell the user which URL
failed and what was tried. Never write a document from the title alone or
from prior knowledge of the subject.
