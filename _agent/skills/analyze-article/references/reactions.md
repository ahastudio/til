# Community reactions and the final gate (steps 9, 10)

## 9. Community reactions

After the gate in step 8b has printed `OK`, automatically invoke the
following three skills in sequence via the Skill tool, passing the output file path as the argument to
each:

1. `hackernews-reactions` — finds the Hacker News thread and weaves key
   comments into the document.
2. `lobsters-reactions` — finds the Lobste.rs thread and weaves key comments
   into the document.
3. `geeknews-reactions` — finds the GeekNews (news.hada.io) thread and weaves
   key native GN comments into the document.

Run them regardless of whether the user asked. If a skill reports that no
thread was found, that is a normal result — note it briefly and continue to
the next skill.

**Mandatory verification (NO EXCEPTIONS):** A document is not done — and
must NOT be reported to the user as done — until all three reaction skills
have been explicitly run against it in this turn, each with a concrete
outcome (comments woven in, or "no thread found"). This applies with equal
force whether you are processing one URL or a long queue of many; a long
queue is not a reason to compress or skip this step for any individual
file.

Before reporting ANY file as complete (including in a queue's final summary
table), run this checklist for that file:

1. Was `hackernews-reactions` invoked for this exact file this turn? What
   was the outcome?
2. Was `lobsters-reactions` invoked for this exact file this turn? What was
   the outcome?
3. Was `geeknews-reactions` invoked for this exact file this turn? What was
   the outcome?

If the answer to any question is "not yet" or "unsure," STOP and run it
before moving on — do not proceed to the next file or to the summary table
with any of the three unresolved. GeekNews is the one most often skipped
(it requires a browser, not a simple API call) — do not let that extra
friction be a reason to defer or drop it. "I already checked HN and that
was thin, so GN is probably thin too" is not a valid basis for skipping the
GN check — each source must be searched independently regardless of what
the others returned.

## 10. Run the format gate again — FINAL STEP

The reaction skills in step 9 edit the document: they insert discussion lines
into the header block, weave sentences into body sections, and append footnote
definitions. Every one of those edits can break the shape that step 8b just
certified — a discussion line in the wrong order or missing its counts, a
footnote defined but never referenced, a handle colliding with an existing
label, curly quotes landing inside a code span in a quoted comment.

So the gate runs a second time, after the last reaction skill has finished:

```bash
python3 .claude/skills/analyze-article/scripts/check_format.py <file>
```

**A document is finished when this second run prints `OK`.** Not when the
prose is good, not when the reactions are woven in, not when the queue is
long and the next URL is waiting. Report the file as complete only after
you have seen `OK` from this run, and in a queue report only files that
reached it.
