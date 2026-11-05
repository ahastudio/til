# Writing rules (step 7)

## 7. Writing rules

Most of the rules below are enforced mechanically by the format gate in step
8b. They are written out here so you produce a conforming document the first
time, rather than writing freely and patching afterwards.

- Follow `_agent/skills/writing-guidelines/SKILL.md` in full: heading spacing, CJK
  table alignment, inline code, fenced-block language identifiers, the `박다`
  vocabulary ban, and the rule that structure belongs to headings and never to
  bold text.
- Write in Korean. Technical terms may be written alongside their original
  English form.
- Break body text at sentence boundaries and keep every line within 80
  columns: each sentence starts a new line, no line exceeds 80 columns
  (CJK characters count as 2), and a sentence that does not fit breaks at
  natural semantic boundaries (after a comma, before 이며/하지만/그러나/
  그리고/하면/때문에, between clauses) as many times as needed. Never split
  a title, a name, a number with its counter, or a footnote reference across
  lines, never leave a one-syllable tail on its own line, and never indent a
  continuation line, because an indented line renders as a code block. This
  applies to prose only; tables, code blocks, headings, and footnote/URL
  lines are exempt from both the sentence-break rule and the 80-column
  limit, so never wrap or shorten them to fit. The full rule is in the `writing-guidelines` skill. Check this
  before invoking the post-processing of step 8b, not after, and verify the
  80-column limit on the finished file.
- Every fenced code block carries a language identifier (`python`, `bash`,
  `text`, …). A bare fence is always wrong.
- Code in a teaching note must be runnable, not illustrative. Prefer a complete
  function over an ellipsis. Comment the lines that encode a decision, not the
  lines that restate the syntax.
- The H1 is Korean (step 3a). Every `##` and `###` heading is Korean too.
- Sections are marked with headings, never with bold text. When the first
  section runs long enough to need internal divisions, give those divisions
  real sub-headings at the right level. A bold line standing alone above body
  text is a structural defect, not a formatting choice.
- Each section must do different work: 요약/소개 reports, 분석 explains,
  비평 challenges, 인사이트 extends. Do not let sections overlap.
- The document should read as if written by someone who disagrees with
  parts of the source and has thought carefully about why.
- Maintain the same tone and depth as existing TIL documents.
- Read the finished document once as a reader who has not seen the source.
  A sentence whose meaning cannot be stated plainly is rebuilt from its
  meaning, not patched. The rule is `Every Sentence Must Make Sense` in
  the `writing-guidelines` skill.
