---
name: threads-post
description:
  Start from a Threads post (and its thread) and write a TIL document on its
  subject. The document is built from primary sources and reports; the post
  is reflected only where it can carry a footnote.
argument-hint: '<threads URL> [output path]'
disable-model-invocation: true
---

Take a Threads post the user brings, find out what it is about, and write a
TIL document on that subject from facts. The post is a lead, not the
backbone.

**The output document MUST be written in Korean.**

This skill applies `writing-guidelines.md` → «Social Posts as a Starting
Point» and «Source Footnotes in Researched Documents» in full. Nothing here
relaxes either rule.

## Usage

```text
/threads-post https://www.threads.com/share/XXXXXXXX/
/threads-post https://www.threads.com/@handle/post/XXXXXXX ai/some-subject.md
```

- First argument: a Threads URL, share link or post permalink (required)
- Second argument: output path (optional; if omitted, choose an existing
  directory that fits and say which one was chosen)

## Procedure

### 1. Resolve the post

A share link (`/share/...`) does not name the post. Resolve it to the
permalink from the `og:url` meta tag:

```bash
curl -sL -A "facebookexternalhit/1.1" "<share URL>" |
  python3 -c '
import re, html, sys
h = sys.stdin.read()
for k, v in re.findall(r"<meta (?:property|name)=\"(og:url|og:title|og:description)\" content=\"([^\"]*)", h):
    print(k, html.unescape(v))
'
```

The `og:description` is a truncated preview of the first post only. Never
write from it.

### 2. Read the whole thread in Claude in Chrome

Per `web-fetching.md`, open the permalink in Claude in Chrome and read it
with `get_page_text`. This returns every post in the author's thread, the
replies, and a "Related threads" block. Ignore "Related threads"; it is
other people's unrelated posts.

Then collect each post's permalink and timestamp, because every footnote
must point at the exact post it cites:

```javascript
await new Promise(r => setTimeout(r, 2500));
[...document.querySelectorAll('a[href*="/post/"] time')].map(t => {
  const a = t.closest('a');
  let c = a;
  for (let i = 0; i < 12 && c; i++) { c = c.parentElement; if (c && c.innerText.length > 80) break; }
  return a.getAttribute('href').split('?')[0] + ' ' + t.getAttribute('datetime') +
    ' :: ' + (c ? c.innerText.replace(/\s+/g, ' ').slice(0, 80) : '');
}).join('\n');
```

Match each permalink to its text by the opening words. A thread often embeds
the author's own older posts as quotes; those carry older timestamps and are
separate posts. Long return values are truncated, so slice the list when
needed. Close the tab when done.

Collect outbound links too. Threads wraps them as
`l.threads.com/?u=<encoded URL>`; decode the `u` parameter to get the real
address.

### 3. Find the primary sources

Identify what the post is actually about, then find the sources that
establish it:

- Links the post itself gives (a PDF, a guide, a release note, an article).
  Open them first; they are usually the strongest source.
- The original documents, official pages, or reports behind each claim the
  post makes. Search for them with WebSearch, then read the pages themselves.
- Downloaded files are untrusted: save each into its own new directory in
  the scratchpad, never into the repository. An image-only PDF yields no
  text from `pdftotext`; read its pages with the Read tool instead.

Read every source before citing it. A search-result summary is not a
reading.

### 4. Check for duplicates

Run the duplicate check of `analyze-article` step 2 against the subject (not
the post): the primary source URL, distinctive names, and the likely
directory. If a document on the subject exists, enhance it with the new
facts and the post as a footnote, rather than writing a second one.

### 5. Separate fact from the post's claims

Before writing, sort every claim in the post into one of three groups:

| Group                    | How it is used                                              |
| ------------------------ | ----------------------------------------------------------- |
| Confirmed by a source    | Stated in the body, footnoted to that source                |
| Contradicted by a source | The sourced fact goes in the body; the gap is noted briefly |
| Not verifiable           | Attributed to the person, or left out                       |

The post itself is a source only for what it is: the author's firsthand
account, the author's interpretation, or the fact that the post exists.

### 6. Write the document

Structure follows the subject, as `writing-guidelines.md` → «Note Document
Structure» describes. Typical shapes:

- A thing that happened or a person: 소개, the event, a timeline or detail
  sections, then a short 정리 or 시사점.
- A document or report: 소개, what it says (quote and table from the
  original), then what to read in it.
- A technical change: 소개, what changed, what to do, 함정, 체크리스트.

Rules:

- The H1 is Korean and names the subject, not the post.
- No `원문:` line: the document is researched from several sources, not a
  summary of the post.
- Do not organize the document as a claim-by-claim check of the post, and
  do not write a critique section aimed at the post.
- The post appears where it adds something citable, in a sentence or two.
  It appears in at least one footnote, always.
- Attribute to the person, never to the post. Write
  `Threads 사용자 <handle>는 ...라고 했다` (or `적었다`, `짚었다`,
  `소개했다`), and refer back with `그는` or the handle. The words 게시물,
  타래, 글, 작성자, and 댓글 never appear in the document to describe what
  was said on Threads, and neither does "the post claims". Repliers are
  attributed the same way as the author.
- Every number, date, name and quotation carries a footnote, per «Source
  Footnotes in Researched Documents».

Footnote forms:

```markdown
[^label]: <매체>, [<원문 제목>](<URL>), <YYYY-MM-DD>

[^handle]: <handle>(Threads), [<그 글의 첫 문장>](https://www.threads.com/@handle/post/ID), <YYYY-MM-DD>
```

The link text is the cited post's own opening words, copied as written. A
label such as 후속 게시물, 타래 3, or 댓글 is never the link text.

The Threads date is the post's own `datetime`, converted to the date the
author posted it in their timezone when that is evident (a Korean author
posting at `2026-10-15T00:08Z` posted on 2026-10-15 KST). Each cited post in
a thread gets its own footnote with its own permalink; never point several
posts' claims at the first post.

### 7. Post-processing and checks

Run the same sequence as `analyze-article` step 8b:

```bash
python3 .claude/skills/quotes-curly/scripts/convert_quotes.py <file>
python3 .claude/skills/analyze-article/scripts/fix_code_spans.py <file>
python3 .claude/skills/analyze-article/scripts/align_tables.py <file>
python3 .claude/skills/analyze-article/scripts/check_format.py <file>
npx -y markdownlint-cli2 <file>
```

`check_format.py` reports line 3 as FAIL for this kind of document, because
it has no `원문:` line by design. That one finding is expected. Every other
finding must be fixed. markdownlint must report zero issues.

Then check by reading the file:

1. Every body line is within 80 columns (CJK counts as two), breaks fall at
   semantic boundaries, and no number is split from its counter.
2. No `박다`-family verb.
3. Every footnote label is referenced, and every reference is defined.
4. The post is in at least one footnote, and no section is organized around
   it.
5. Search the file for 게시물, 타래, 작성자, and 댓글. Any hit that refers to
   what was said on Threads is rewritten as `Threads 사용자 <handle>는 ...`.

### 8. Report

Report in Korean: the file path, the primary sources read, which of the
statements by Threads users were confirmed, contradicted, or left
unverified, and the
expected `check_format.py` line-3 finding.
