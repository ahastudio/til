# Output, file name, post-processing and the format gate (steps 8a, 8b, 8c)

## 8a. File name — STRICT RULE (NO EXCEPTIONS)

**The file name is the subject. Nothing else.**

Use lowercase English kebab-case. Include only words that identify which
subject this is. Never include words that state what category, medium, or
kind of artifact the subject is, and never describe what this document does
to the subject.

Name a named thing by its name. Name an argument by its claim. Name a
specific release or incident by its identifier. Add words only to
disambiguate, and only words that narrow the subject.

Keep it short. Do not transliterate Korean; the name stays English even
though the H1 is Korean (step 3a).

**Mandatory check before writing the file:**

1. Read the file name back without the extension.
2. Ask of each word: does it answer *which* thing this is, or *what kind of*
   thing this is?
3. Delete every word that answers the second question.

## 8b. Post-processing and the format gate — MANDATORY SEQUENCE

**Run these four commands, in this order, every time, on every file this
skill writes or enhances. The document is not written until they pass.**

```bash
# 1. straight quotes → curly, outside fenced code
python3 .claude/skills/quotes-curly/scripts/convert_quotes.py <file>

# 2. restore straight quotes inside inline `code spans`
#    (convert_quotes.py skips fenced blocks but not spans)
python3 .claude/skills/analyze-article/scripts/fix_code_spans.py <file>

# 3. pad table cells so the pipes line up (CJK counts as two)
python3 .claude/skills/analyze-article/scripts/align_tables.py <file>

# 4. the format gate
python3 .claude/skills/analyze-article/scripts/check_format.py <file>
```

`check_format.py` enforces the mechanical half of this skill: the H1, the
closed header block of step 7a, the source-line form of step 4, the ban on
`## 요약` in a non-article, the completeness and order of the analytical body
from step 5a, code-fence language identifiers,
CJK table alignment, standalone bold lines, indentation that would render as
a code block, the `박다` vocabulary ban, quote direction inside and outside
code, and footnote integrity from step 7b.

It prints `OK` or `FAIL` with a line number for each defect. **A `FAIL` is
not advisory.** Fix the file and run it again until it prints `OK`. Never
report a document as finished, and never move to the next URL in a queue,
while the gate is failing. Do not edit the gate to make a document pass.

If you believe the gate is wrong about a specific rule, say so to the user
and stop; do not route around it silently.

## 8c. What the gate cannot check

The script checks shape. These remain your judgment, and are checked by
reading the file you just wrote:

1. Is the H1 Korean prose that carries the source's claim, rather than a
   transliteration or a flattened topic label?
2. Does the body structure match step 5a's choice — analytical for a source
   that argues, practical for one that teaches?
3. Do the sections do different work, or do two of them restate each other?
4. Is every number, name, and quoted phrase traceable to the fetched text
   rather than to memory?
5. Does every footnote point at a comment you actually observed?
6. Is the file name the subject and nothing else (step 8a)?
