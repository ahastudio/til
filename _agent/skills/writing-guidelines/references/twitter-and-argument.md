# Twitter Naming and Argument Rules

## Contents

- Twitter Naming: Twitter, never X; tweet URLs use `twitter.com`
- Tweet Terminology: 트윗 unless the user says 스레드
- Argument and Evidence: keep fact, inference and judgment distinguishable

## Twitter Naming (ABSOLUTE PRIORITY — ZERO TOLERANCE)

**The service is called Twitter. Never X. Not in a document, a heading, a
footnote, a table cell, a chat message, or a commit message.** The user
treats every appearance of X as the service name as a severe defect.

Root cause of a repeated failure: the source (a Korean news article, an
English post, the platform's own page) wrote X or 엑스 or X(옛 트위터), and
the writer mirrored the source's wording instead of the repository's rule.
A source's naming never overrides this rule. When a source says X, the
document says Twitter; when a source says X(옛 트위터) or formerly Twitter,
the document says Twitter and drops the parenthetical.

- Every form is covered: 트위터 is allowed and means the same thing, but
  X, 엑스, X에, X 게시물, X 계정, X(옛 트위터), the X platform, and
  compound names such as a Twitter Article are not. Write Twitter 게시물,
  Twitter 계정, Twitter에 올렸다.
- Tweet URLs use `twitter.com`, never `x.com`. The domain `x.com` may appear
  only where the literal domain is the point, such as a rule about which URLs
  to rewrite.
- Quoting is not an exception. A quotation that contains X as the service
  name is paraphrased in prose or the service name inside it is replaced by
  Twitter. Never keep the source's X for fidelity.
- A different thing that is also written X is not this rule's concern: the
  Tesla Model X, a variable named X, Xbox, Xcode. Do not rename those.

**Mandatory check before finishing ANY `.md` write or edit, and before
sending ANY chat message:**

1. Search the text for the capital letter X standing alone, for 엑스, and for
   x.com.
2. For each hit, decide whether it names the service. If it does, rewrite it
   as Twitter now.
3. The format gate of the analyze-article skill fails any document that calls
   the service X in prose. A pass from the gate does not replace this check,
   because the gate recognises only the common phrasings.
4. When the user corrects this once, search every document written in the
   same session for the same failure and fix them all in the same edit.

## Tweet Terminology

Call it a "트윗" unless the user explicitly says "스레드". Long tweets are still
tweets.

## Argument and Evidence

An analytical document must make three layers distinguishable:

- **Reported fact:** what the cited material directly says.
- **Inference:** what follows from those facts, including the assumptions
  needed to connect them.
- **Judgment:** what the writer recommends, doubts, or considers important.

Do not let a sourced fact silently carry a broader conclusion. Name the
bridge between them, and state when it is an assumption rather than a
verified fact.

When a claim is disputed, address its strongest plausible form. A useful
critique identifies the evidence that would support the claim, the evidence
that would weaken it, and the observation that could distinguish between
competing explanations.

For practical notes, end the reasoning with a decision rule, a sequence of
actions, or a failure condition the reader can apply. Avoid adding a
generic summary when the document already states its conclusion.
