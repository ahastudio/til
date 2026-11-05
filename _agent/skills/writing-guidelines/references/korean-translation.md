# Korean Translation Rules

## Contents

- Natural Korean, including Collocation: no literal translation; a noun must take the predicate Korean actually pairs with it
- Never Force an English Term Into Korean: a term the field writes in English stays in English
- Translation Is Understanding First: keep the author's intent; one source term, one Korean term; footnote ambiguous terms

## Natural Korean — No Literal Translation (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**Never translate English words or expressions literally into Korean prose.**
Literal translation is the most common cause of unnatural-sounding Korean.

**Forbidden pattern — mechanically mapping an English verb to a Korean verb:**

| English concept | Literal (forbidden) | Natural Korean       |
| --------------- | ------------------- | -------------------- |
| twist (mockery) | 비틀다              | 꼬집다, 비꼬다       |
| cut (dismiss)   | 자르다              | 단정하다, 정리하다   |
| capture         | 포착하다            | 담다, 잡아내다       |
| highlight       | 하이라이트하다      | 강조하다, 부각하다   |
| navigate        | 내비게이트하다      | 탐색하다, 다루다     |

This table is illustrative, not exhaustive.
Whenever you thought of the English word first and then translated it,
stop and rethink.

**Test:** Before writing a verb, ask "Would a native Korean speaker say this
naturally?" If you reached for the English word first, that is a warning sign.
In that case, express the intended meaning in Korean from scratch.

**Verb selection:** Prefer pure Korean verbs that express the meaning directly.
Sino-Korean verbs are acceptable when they are more natural and precise.
Foreign-origin `-하다` verbs are only allowed when they are established
industry-standard terms.

### Collocation Is Part of Correctness (ABSOLUTE PRIORITY — ZERO TOLERANCE)

**A Korean sentence is wrong when its noun and predicate do not belong
together, even if every word in it is a real word.**
Root cause of a repeated failure: an English collocation was carried over
word for word, so the sentence pairs a noun with a verb that Korean writers
never pair with it. A reader stops at it, and the whole document loses
credibility. The user treats this as a severe defect, not a style issue.

- Each noun takes the predicate that Korean writing actually uses with it.
  Abstract nouns such as a definition, a standard, a consensus, or a
  meaning take the predicates established in Korean prose for that noun,
  never a physical or sensory verb borrowed from an English idiom.
- Never render an English idiom or metaphor by its literal words. Find the
  plain Korean predicate for what it means, or drop the metaphor.
- If you cannot name a common Korean phrase that uses this exact noun and
  predicate pair, the pair is suspect. Rewrite it with a plainer predicate.
- Sentences translated from a source deserve the most suspicion: you wrote
  them with the English still in mind.
- This applies equally to documents, headings, table cells, footnotes, and
  chat messages.

**Mandatory check before finishing ANY `.md` write or edit, and before
sending ANY chat message in Korean:**

1. Read every sentence you produced as a Korean reader would, without the
   source in mind.
2. For each noun and predicate pair, ask whether a Korean writer would
   naturally write that pair. Any doubt means rewrite.
3. For each sentence that came from an English source, rebuild it from the
   meaning instead of adjusting the translated words.
4. Do this for the whole text you produced, not just the sentence a
   previous correction pointed at. A correction to one sentence means the
   same failure may exist elsewhere; search for it.

## Never Force an English Term Into Korean (ABSOLUTE PRIORITY — ZERO TOLERANCE)

**A word that the field uses in English stays in English. Inventing a Korean
word for it, or picking a dictionary equivalent that readers have never
seen in that role, is forbidden in every document, heading, table cell,
footnote, and chat message.**

Root cause of a repeated failure: an English term was swapped for a Korean
word that is not what Korean practitioners write, and the swap also collides
with another established meaning. A reader then asks what the word refers to,
and the document loses credibility. The user treats this as a severe defect.

- Before writing a Korean word for a foreign term, ask whether Korean
  practitioners actually write that word for that concept. If you cannot name
  a document, product, or standard that does, keep the original term.
- Design, graphics, and platform vocabulary is the highest-risk area. Terms
  such as material, surface, backdrop, layer, shader, and sample belong to
  their field in English. Do not turn them into coined Korean nouns or
  common-noun look-alikes.
- A Korean word that already carries another established meaning in the same
  field is never reused for the English term. If the reader could mistake it
  for that other thing, the word is wrong.
- When no settled Korean form exists, write the original term, or describe the
  concept in a plain phrase once and then keep using the original term. Do not
  create a shorthand.
- Do not translate a product's own vocabulary (API names, parameter names, the
  names of styles or modes). Keep it exactly as the product writes it.
- Never force a sentence structure, metaphor, or compound noun from the
  source into Korean word for word. If the Korean reads as a translation, the
  sentence is rebuilt from its meaning.

**Mandatory check before finishing ANY `.md` write or edit, and before
sending ANY chat message:** list every Korean noun that stands in for a
foreign technical term, and for each one confirm that practitioners write it
that way. Replace every failure with the original term or a plain description.
When the user points at one such word, search the whole document and every
other document written in the same session for the same family of word and fix
them all in the same edit.

## Translation Is Understanding First, Then Writing (ABSOLUTE PRIORITY — ZERO TOLERANCE)

**Every sentence that comes from an English source is a translation, whether
it is a summary, a paraphrase, a woven-in comment, or a table cell. Keep the
author's intent exactly, and write Korean that a Korean reader reads without
stopping.**

Principles:

- Understanding and writing are both required. Writing fluent Korean without
  having understood the source, or understanding the source and writing Korean
  that reads as a translation, are both failures. Making the Korean smoother by
  changing what the author meant is also a failure.
- Different source terms stay different. Two English terms in the same source
  never become one Korean word. Rendering both `client` and `customer` as the
  same Korean word makes a reader who connects the two read the opposite of
  what the author wrote. For every pair of English terms that sit near each
  other, confirm the two Korean words differ and each can be told apart.
- One source term stays one Korean term. The same English phrase gets the same
  Korean wording across the whole document. Rendering one phrase three different
  ways hides that it is one concept. Fix the choice at first use and reuse it.
- The field decides the word, not the dictionary. Choose the word that
  practitioners of that field write for that sense, and read the sense from the
  context: `action` in a sentence about a team's work is closer to 업무 than to
  행동, and `client` in a sentence about objects and systems is a technical
  term, not a customer. If you do not know the field's word, keep the English
  and describe the sense once in plain Korean. A guess from the dictionary is
  the typical failure of translators who are not experts in the field.
- Connectives and small words carry the logic. Read what each connective
  relates (contrast, addition, cause, sequence) before choosing the Korean.
  Rendering `meanwhile` with a contrast word reverses the relation between two
  sentences, while the field's usual rendering for that sense is closer to 한편.
  A wrong connective changes what the paragraph claims.
- A term can bring a foreign practice with it. When the usual Korean rendering
  of a term encodes a different concept (design rendered as 설계 or 기획 carries
  the engineering split of design and build, and a custom from another country),
  do not use that rendering silently. Keep the English and explain the sense in
  a footnote.
- Check the Korean against the English. When a sentence matters, set the
  English beside the Korean and compare in both directions. A Korean sentence
  that cannot be matched back to the English sentence is rebuilt from the
  meaning.
- Reviewing someone else's translation is done with the original in hand.
  Quote the page, the translated sentence, and the original sentence, and say
  what meaning changed. Calling a sentence awkward is not a review.

### Ambiguous Translated Terms Get an Explanatory Footnote

**When a translated term is ambiguous, or the choice among its Korean renderings
is not obvious, attach a footnote that explains it.** The footnote is a note
written in Korean prose. It does not translate anything and it does not cite a
page.

- Put the footnote reference at the end of the sentence that first uses the
  term, and define it at the bottom of the document under the `---` rule like
  every other footnote.
- The note gives the English original, the sense that is meant, and why this
  rendering was chosen over the others. When the usual rendering would mislead,
  the note says so.
- The note comes in addition to the English in parentheses from the rule on
  English alongside, never instead of it.
- An explanatory note carries no URL, because it is the writer's explanation
  and not a citation. It therefore never points at the analyzed source, and the
  rule that the analyzed source takes no footnote stays intact.
- Do not decide that a term is clear enough to go without the note. When in
  doubt, write it.

A sentence translated from an outside page still carries the footnote for that
page under the source footnote rules, and the two kinds of footnote are
separate: a citation points at a page, an explanation explains a term.

These principles work together with the rules on English terms: keep the
English next to any Korean word that could be read another way, so the reader
can check the translation too.

**Mandatory check before finishing ANY `.md` write or edit, and before
sending ANY chat message in Korean:**

1. For each sentence taken from an English source, state what the author meant
   in one plain sentence, then confirm the Korean says exactly that.
2. List the English terms that sit near each other and confirm each has its
   own Korean word. List the terms that repeat and confirm each keeps one
   Korean word.
3. Read every connective for the relation it expresses.
4. List every translated term that is ambiguous or whose rendering is not
   obvious, and confirm each has an explanatory footnote and the English in
   parentheses.
5. Check the footnote definitions of the finished text: every sentence resting
   on an outside page has its own citation footnote, and no definition points
   at the analyzed source.
6. When the user points at one translation error, search the whole document and
   every other document written in the same session for the same kind of error
   and fix them all in the same edit.
