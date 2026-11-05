# Source Footnote Rules

## Contents

- Source Footnotes in Source-Based Documents: each sentence resting on an outside page has its own titled footnote; the analyzed source never takes one
- Social Posts as a Starting Point: build from primary sources, cite the post only where it carries a footnote

## Source Footnotes in Source-Based Documents (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**When a document reports what outside pages say — several articles compiled,
reports, official pages, search results, or pages that a single analyzed
article quotes or that were fetched to check it — every factual claim that
rests on such a page carries a footnote that points to it. Footnotes for
outside pages are complete and exact: every claim has its page, and each
footnote sits where the claim is made — never sparse, never padded.**
A reference list at the end of the document is not a substitute.
A list says what was read; only a footnote says which source supports which
sentence, and that is what a reader needs in order to check a number.

Why this is a defect and not a style choice: a researched document is only
as trustworthy as the reader's ability to trace each claim. When sources
disagree — and in researched topics they routinely do — an unattributed
number cannot be weighed against its rivals, and an error cannot be traced
back to where it entered.

Rules:

- Every number, date, name, quotation, and specific factual claim that came
  from a source gets a footnote reference right after it, in the same
  sentence or table cell.
- Abundance is the default for every page other than the document's own
  analyzed source. Every sentence that rests on such a page — a claim, a
  number, an example, a quotation, a comparison — carries its own footnote
  reference, and a sentence resting on two pages carries two. A paragraph of
  such content with no footnote, or one reference parked at the end of
  several sentences, is a defect. When in doubt, add the footnote.
- A named source gets its own footnote. When the prose says where something
  came from — taken from an encyclopedia entry, quoted from a report, said in
  an interview — the footnote for that page sits at the end of that very
  sentence, not several sentences later and not on a different page. Link the
  page the words actually come from: confirm that the quoted or paraphrased
  words appear there, and use the same language edition or version the source
  drew on. When the exact page cannot be identified, say so in the text
  instead of linking a near match.
- Placement: the reference goes at the end of the sentence it supports, after
  the final punctuation, whenever it can. A reference in the middle of a
  sentence is allowed only when one sentence rests on different pages and the
  clauses cannot be separated; even then, prefer splitting the sentence in two
  so that each reference lands at a sentence end. Never leave a reference in
  the middle of a phrase.
- **The analyzed source never gets a footnote. Not one. (ABSOLUTE
  PRIORITY — ZERO TOLERANCE)** In a document built around one article, post,
  paper, tweet, video, or repository, the source line under the title is the
  only link to that page. No footnote may point at that page: not on the
  first sentence, not on a quotation, not on a figure, not on the publication
  date, not for the author's name, and not in the titled
  `[^label]: <매체>, [<제목>](<URL>), <날짜>` form either. A label such as
  `essay`, `source`, `original`, `post`, or the author's name whose definition
  is the source URL is a defect, and so is the same URL with a trailing slash,
  a tracking parameter, or a different scheme. When a sentence needs the
  author, the date, or the exact wording of the source, say it in the prose;
  the reader already has the source line. Footnotes exist for the pages the
  reader does not already have — never to repeat the page the document is
  about. If you notice this defect in a document you are touching, delete
  every reference and the definition, then reread the sentences to confirm
  they still stand without the mark.
- When the analyzed source quotes or relies on another page and that page was
  also opened and read (an essay quoting an encyclopedia entry, a report citing
  a paper), footnote that page on the sentence that reports the fact. The
  source line covers the essay; the footnote covers the encyclopedia.
- Material the writer fetched to check, extend, or contrast with the source
  is footnoted like any other outside page.
- The footnote points to the page the claim was actually read from.
  If the claim was read in a secondary report that cites a primary source,
  footnote the page that was read, and name the primary source in the prose.
  Never footnote a primary source you did not open.
- A quotation is footnoted to the page where the quoted words appear.
- One footnote label per source page, reused wherever that page supports a
  claim. Choose a short, readable label that identifies the source.
- A table that compiles figures from several sources carries a footnote in
  each row or cell, not one note for the whole table.
- The document's own analysis, comparison, and judgment are not footnoted;
  the facts they rest on are.
- Every footnote definition carries the publisher, the source's own title
  as a link, and the source's publication date. A bare URL is not enough:
  the reader must be able to tell what the source is and how current it is
  without opening it.

  ```markdown
  [^label]: <매체>, [<원문 제목>](<URL>), <YYYY-MM-DD>
  ```

  The title is copied as the source presents it, untranslated. The date is
  the publication date read from the page itself (its byline, metadata, or
  URL), never a guess and never the date it was read. If a page shows no
  publication date, leave the date out; write no placeholder in its place.
- Footnote definitions follow `## Footnote Spacing` and sit at the end of
  the document after a `---` rule.
- This format is for researched sources. Footnotes that cite a community
  comment (Hacker News, Lobste.rs, GeekNews) keep the bare `<URL>` form
  their skills specify.
- A separate reference-list section is not added on top of the footnotes.
- Claims that could not be confirmed are stated as such in the text, never
  footnoted to a source that does not actually say them.

**Mandatory check before finishing a source-based document:**

1. Scan every paragraph, table row, and list item for numbers, dates, names,
   quotations, and any sentence that rests on a page other than the analyzed
   source.
2. For each one, confirm a footnote reference sits next to it. A sentence
   resting on an outside page with none is a violation, including in the
   summary section.
3. For each footnote, confirm the page it points to was actually read and
   says what the sentence claims.
4. Compare every footnote definition's URL with the URL on the source line.
   If any definition points at that same page, it is a violation: delete the
   definition and every reference to it before doing anything else. This
   check runs on every document you write, enhance, or edit, and it runs
   again after the reaction skills have added their footnotes.
5. Wherever the prose names where something came from, confirm the footnote
   sits at the end of that sentence and links that exact page. Look for
   references stranded mid-sentence and move them to a sentence end.
6. Count the references per paragraph. A paragraph resting on outside pages
   with a single reference at its end means footnotes were written too
   thinly: split them out per sentence. Equally, remove footnotes that only
   repeat the analyzed source sentence by sentence.

## Social Posts as a Starting Point (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**When the user brings a social post (a Threads post or thread, a tweet,
and the like) and asks for a document on its subject, the document is
built from facts, and the post is reflected only to the extent that it
can carry a footnote.**

The post is a lead, not the backbone. Root cause of a past failure: the
post's framing, numbers, and claims drove the structure, and the critique
section ended up arguing with the post instead of explaining the subject.

Rules:

- Find and read the primary sources the post points to or relies on
  (original documents, reports, official pages), and build every section
  from them.
- The title, sections, and conclusions describe the subject, not the post.
  Do not organize the document as a claim-by-claim check of the post, and
  do not write a critique section aimed at the post.
- Use the post only where it adds something citable: a fact the primary
  sources lack, a firsthand account, or an interpretation worth noting in
  a sentence or two. Every such use carries a footnote to the exact post.
- The post always appears in at least one footnote.
- When the post disagrees with the sources, state the sourced fact in the
  body and note the discrepancy briefly, with the post footnoted.
- Claims from the post that could not be verified are attributed to the
  person, never stated as fact.
- In prose, attribute to the person, never to the post. Name the platform
  and the handle as a user: `Threads 사용자 <handle>는 ...라고 했다`
  (or `적었다`, `짚었다`). Never call it 게시물, 타래, 글, 작성자, or
  댓글 in the document, and never write that "the post claims" something.
  This applies to the author and to repliers alike.
- Footnote link text is the cited post's own opening words, not a label
  such as 후속 게시물, 타래 3, or 댓글.
