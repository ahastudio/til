# Web Content Fetching

## Browser Choice (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**When a page must be opened in a real browser, ALWAYS use Claude in Chrome.**

Claude in Chrome drives the user's own Chrome profile, so it carries the
sessions and subscriptions the user already has. That is the only way to reach
pages behind a login or a paywall, and it is also the most faithful rendering of
what the user actually sees. A headless automation browser has neither.

Order of attempts for any URL:

1. `WebFetch` — for plain, server-rendered pages.
2. Direct retrieval (`curl` with a browser User-Agent, or a site's `.md` /
   API / oEmbed endpoint) — for pages that render server-side but block
   `WebFetch`.
3. **Claude in Chrome** — for anything that needs JavaScript, a login, a
   paywall, or a session. This is the required browser.

**Never open a headless automation browser when Claude in Chrome is
available.** `agent-browser` is a fallback for one case only: Claude in Chrome
is not connected to this session. When that happens, say so explicitly in the
report rather than switching silently.

**Checklist before launching any browser:**

1. Is Claude in Chrome available in this session?
2. If YES — use it. Do not use `agent-browser`.
3. If NO — say so in the response, then fall back to `agent-browser`.

## Twitter / X (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**NEVER use WebFetch for twitter.com or x.com URLs.**
**ALWAYS open tweets in a browser, and that browser is Claude in Chrome.**

WebFetch is blocked by X's paywall (HTTP 402). Using it will produce empty or
fabricated content. There are zero cases where WebFetch is acceptable for X.

Procedure for any tweet URL:

1. Open the tweet URL in Claude in Chrome.
2. Read the exact tweet text from the rendered page.
3. Expand any truncated text (`Show more`) before reading.
4. Capture replies too when the document will cite them.

**Never write about a tweet's content without first opening it in a browser.
Writing from memory or inference is forbidden.**

## Paywalled and Logged-In Pages

Subscription news sites (Bloomberg, WSJ, FT, The Information, and similar),
anything behind a member wall, and anything that requires an account are
Claude in Chrome cases by definition. Direct retrieval returns a teaser or a
consent page, and writing a document from a teaser is the failure this rule
exists to prevent.

If the page cannot be read even in Claude in Chrome, STOP. Report which URL
failed and what was tried. Never reconstruct a paywalled article from its
headline, its metadata, or prior knowledge.

## Other JavaScript-Rendered Pages

JavaScript-rendered pages follow the same order: `WebFetch`, then direct
retrieval, then Claude in Chrome. Many sites that appear to need a browser
publish the same content in a fetchable form — a `.md` sibling URL, an oEmbed
endpoint, a JSON API, or an RSS item. Check for those before opening a browser,
because they are faster and quote more exactly.

## An Empty Result Is Not a Result (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**Never conclude that something does not exist from a search that returned
nothing, until you have confirmed the search actually ran.**

Sites increasingly answer automated requests with an interstitial that
carries HTTP 200 — an anti-bot challenge, a consent wall, a rate-limit
notice, or a JavaScript shell with no content. A scraper reading that page
finds zero matches, and zero matches looks exactly like a genuine absence.
This has already produced wrong conclusions in this repository: a Lobste.rs
thread with 170 points and 64 comments was reported as "no thread found"
because `lobste.rs/search` was serving `Making sure you're not a bot!` with
a 200.

Before writing any sentence that asserts absence:

1. **Look at the body, not just the status code.** Check for `not a bot`,
   `challenge`, `captcha`, `Enable JavaScript`, `Access denied`,
   `rate limit`, or a body far shorter than a real page.
2. **Run a control query.** Search for something you know exists through the
   exact same code path. If the control also returns zero, the pipeline is
   broken — fix it before concluding anything.
3. **Try a different transport.** A blocked HTML endpoint often has a working
   JSON, RSS, or per-item sibling. Blocking is usually applied per path, not
   per host.
4. **Distinguish the two outcomes in what you report.** "Searched and found
   nothing" and "could not search" are different findings. Say which one it
   is, and name the endpoints you tried.

Known blocked paths are recorded in the skill that uses them; when you
discover a new one, add it there rather than rediscovering it later.

## agent-browser (fallback only)

Use only when Claude in Chrome is unavailable, and say so when you do.

1. `agent-browser open <URL>` — open a page (add `--headed` when a site
   blocks headless)
2. `agent-browser snapshot -i` — get interactive element tree
3. `agent-browser click @<ref>` — click an element
4. `agent-browser eval "<JS expression>"` — extract text via JavaScript
5. `agent-browser close --all` — close the browser
