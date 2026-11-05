# Korean Clarity and Vocabulary Rules

## Contents

- Every Sentence Must Make Sense: a stranger must be able to say what each sentence means
- Forbidden Vocabulary: the verb stem `박-` is banned
- Forbidden Metaphors: no figurative 내기, 천장, 전장, 주자, 지형, 해자; write the plain claim
- Any Doubt Means English Alongside: write `한국어(English)` whenever a Korean word could be read two ways
- Terminology: standard full names, no clipped or coined terms

## Every Sentence Must Make Sense (ABSOLUTE PRIORITY — ZERO TOLERANCE)

**A sentence is finished only when a reader who has not seen the source can
say plainly what it means. A sentence that parses but says nothing, or says
something other than what was meant, is a defect in every document, heading,
table cell, footnote, and chat message.**

Root cause of repeated failures: the writer compressed or translated while
thinking in another language and never read the result as a stranger would.
The usual forms are these:

- Compressing a source's phrase into a fragment whose referent disappears,
  so the reader cannot tell what the phrase points at.
- Carrying a foreign sentence structure or idiom into Korean word for word.
  Each word is real and the sentence still means nothing to a Korean reader.
- Coining a shorthand name for a source, an idea, or a section, and using it
  as if the reader already knew it.
- Filler sentences that talk about the document itself instead of its
  subject, repeated in the same stock shape across paragraphs.
- Metaphors that only work in the original language.

Rules:

- Before finishing any text, read every sentence cold. For each one ask what
  exactly it claims and what each noun refers to. If the answer cannot be
  given in one plain sentence, rebuild the sentence from its meaning. Do not
  patch it cosmetically.
- Say who did what, which thing is meant, and which source said it. Do not
  leave the reader to infer a subject, an object, or a time.
- When a reader points at one unclear sentence, search the whole document, and
  every other document written in the same session, for the same form of
  failure, and fix them all in the same edit.
- Never explain a source's circumstances (hosting, archiving, mirroring) unless
  they change how the content should be read.

## Forbidden Vocabulary — 박다 계열 (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**NEVER use the verb `박다` or any of its conjugated or compound forms in TIL
prose.** This verb carries a coarse, crude, and unpleasant connotation in
Korean that does not fit the tone of these documents. Its use is a defect, not
a style choice.

Forbidden forms include, but are NOT limited to:

- `박다`, `박는다`, `박지`, `박았다`, `박은`, `박힌`, `박혀`, `박혀 있다`
- `박아 넣다` / `박아넣다`, `박아 두다` / `박아두다`
- `박제`, `박제하다`, `박제되다`

This list is illustrative, not exhaustive. Any word built on the `박-` stem
with this "drive in / nail in / embed" meaning is forbidden, even forms not
spelled out above.

Use a plainer verb that states the actual meaning instead:

- embedding / inserting → `넣다`, `삽입하다`, `포함하다`
- persisting / remaining → `남다`, `남기다`, `유지되다`
- imprinting on memory → `각인시키다`, `각인되다`
- repeating for emphasis → `반복하다`, `강조하다`
- hardcoding → `하드코딩하다`, `고정하다`

**Mandatory check:** Before finishing ANY `.md` write or edit, scan the text
you produced for the `박` character used as this verb. If you find even one
instance, replace it before completing. "It reads fine" is not an excuse —
the verb is banned regardless of how natural it sounds in context.

If you catch yourself typing `박아`, `박힌`, `박제`, or any sibling form:
STOP and rewrite with a neutral verb.

## Forbidden Metaphors — 내기 계열 (ABSOLUTE PRIORITY — ZERO TOLERANCE)

**NEVER carry an English figure of speech into Korean prose.** A noun or verb
from sports, gambling, war, geography, or architecture that stands in for a
plain claim reads as a mistranslation, and a Korean reader stops at it and asks
what it means. The user treats each one as a severe defect, not a style choice.

Root cause of a repeated failure: the English word was chosen first (bet,
ceiling, battlefield, runner, landscape), then mapped to a Korean word with the
same literal meaning. The Korean word has no such figurative use, so the
sentence means nothing, and a table label or heading built on it spreads the
defect through the whole document.

Forbidden when used as a figure of speech, with the plain claim to write
instead:

- `내기`, `내기를 걸다`, `내기를 하다` for a strategic choice (bet on X): say
  what was chosen and what it depends on, such as `X를 택했다`, `X 쪽으로
  방향을 잡았다`, `X를 전제로 만들었다`. In a table, label the column by what it
  holds (`방향`, `접근 방식`, `전제`), never `내기`.
- `천장` for a limit (ceiling): `한도`, `상한`.
- `전장`, `승부`, `싸움` for competition between products: `경쟁 영역`,
  `경쟁`, `갈리는 지점`.
- `주자` for competitors or candidates (runner): name them, or `도구`, `후보`.
- `지형`, `지도`, `사각 구도` for a market or situation (landscape, quadrant):
  `상황`, `구도`, `비교`, or describe what is being compared.
- `도전자`, `챔피언`, `왕좌` and the like for products: `후발 제품`,
  `기존 제품`.
- `해자`, `병목` and similar borrowed images are allowed only when Korean
  practitioners write them in that exact sense; otherwise state the plain claim.

This list is illustrative, not exhaustive. The rule covers every metaphor of
the same kind, including ones not spelled out above.

`내기` stays correct only for an actual wager: a bet between people, or Pascal's
wager as that established name. A company's or a product's choice of direction
is never a wager.

Test before writing any figurative noun or verb: would a Korean news article or
documentation use this exact word in this sense? If you cannot name one that
does, delete the image and write the claim in plain words. Rebuild the
sentence from its meaning; do not swap in a near-synonym metaphor.

**Mandatory check before finishing ANY `.md` write or edit, and before
sending ANY chat message:**

1. Search the text for every word in the list above and for any other figurative
   noun or verb you used.
2. Look in tables first. Column labels, row labels, and headings are where
   such words hide and where they cost the most.
3. Replace each hit with the plain claim.
4. When the user points at one such word, search the whole document and every
   other document written in the same session for the same family of word, and
   fix them all in the same edit.

## Any Doubt Means English Alongside (ABSOLUTE PRIORITY — ZERO TOLERANCE)

**When a Korean word could be read in more than one way, even slightly, write
the original English term next to it in parentheses: `한국어(English)`. This
is the only reliable way to stop ambiguous or mistranslated wording, and it
overrides the writer's confidence that the Korean is clear.**

Root cause of a repeated failure: the writer judged a Korean word to be clear,
the reader could not tell what it meant or which English term it stood for,
and the document lost credibility. The writer's own sense that the word is
fine is exactly the judgment that failed, so it is not allowed to decide
whether the English is needed.

Rules:

- The threshold is any doubt. If a reader could attach a different meaning,
  if more than one Korean rendering of the English exists, if the Korean word
  is a translation rather than the form practitioners write, if it is coined
  or newly combined, or if the same Korean word carries another meaning in the
  field, the English goes next to it. When unsure whether it is ambiguous, it
  is ambiguous.
- Cost is not an argument. An extra parenthesis costs nothing; a wrong or
  unclear term costs the reader's trust. Never skip the English to keep a
  sentence short or smooth.
- Write the English at the first use in the document, and again in every
  heading, table label, table cell, and section a reader may enter on its own,
  because those are read without the earlier text.
- Use the English term exactly as the source or the field writes it, not a
  paraphrase of it. Where there is no settled English term, describe the
  concept in plain English words rather than inventing one.
- The English does not excuse a bad Korean word. Words banned by the
  vocabulary and metaphor rules stay banned with an English gloss attached,
  and a coined Korean shorthand is still replaced, not annotated.
- This applies to documents, headings, footnotes, and chat messages alike.

**Mandatory check before finishing ANY `.md` write or edit, and before
sending ANY chat message in Korean:**

1. List every Korean noun, verb, and label that stands for a foreign or
   technical term, a figure of speech, or a name you shaped yourself.
2. For each one ask only: could a reader take it another way? If yes or not
   sure, add the English in parentheses now.
3. Do not decide that a word is common enough to leave bare. Leave a word bare
   only when it is a proper name or a code identifier already written in its
   original form.
4. When the user points at one ambiguous word, search the whole document and
   every other document written in the same session for the same family of
   word, and add the English in the same edit.

## Terminology (ABSOLUTE PRIORITY — NO EXCEPTIONS — ZERO TOLERANCE)

**Every technical term must be its standard, full, established name.
Clipped, coined, slangy, or loosely translated terms are forbidden in every
document, every heading, every table cell, every footnote, and every chat
message. There is no "it is understandable" exception.**

Root cause of repeated failures: a term was picked because it was quick to
write or sounded close enough, not because it is what the field calls the
thing. The reader pays for that every time: they stop to decode it, they
doubt the writer, and sometimes the sentence now says something else. A
sloppy term in one place poisons trust in the rest of the document.

Forbidden, without exception:

- **Clipped forms** that people say aloud but the field does not write: a
  half-word cut from a longer standard name. Write the whole name.
- **Coined words and ad-hoc shorthand** invented for the document. If the
  field has no settled word, describe the concept in a plain phrase and use
  that same phrase every time.
- **Word-for-word translation** of a technical word. A term that is settled
  in English stays in English. A term that has a settled Korean form uses
  that form. Never pick a Korean word only because a dictionary lists it.
- **Near-synonyms that shift the meaning.** Two words that are loosely
  related are different terms. Use the one that matches the concept.
- **Mixing names for one thing.** One concept gets one term for the whole
  document, headings and footnotes included.
- **Overriding the user's term.** When the user names, corrects, or
  rejects a term, that choice is final for the rest of the conversation and
  for every later document. Apply it everywhere it appears, including
  quotations of code or plans that you reproduce, unless the user says
  otherwise.
- **Unexplained abbreviations.** Write the full name at first use. Never
  invent an abbreviation.

Process, not intention:

1. Before writing a term, ask: is this the name the field writes in its
   documentation? If you are not sure, look it up in the repository's own
   notes or the primary source before using it.
2. When the user corrects one term, search the whole document, and every
   other file you touched this session, for every variant of it. Fix all of
   them in the same edit. Fixing only the sentence the user pointed at is a
   violation.
3. Do not wait to be told twice. A term the user has rejected once must
   never reappear.

**Mandatory check before finishing ANY `.md` write or edit, and before
sending ANY chat message:** list every technical noun and verb you used,
and confirm each is the standard full name. Replace each failure now. This
check runs every time, including for short edits and short replies.
