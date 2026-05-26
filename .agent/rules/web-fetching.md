# Web Content Fetching

## Twitter / X (ABSOLUTE PRIORITY — NO EXCEPTIONS)

**NEVER use WebFetch for twitter.com or x.com URLs.**
**ALWAYS use `agent-browser` for any tweet or X post.**

WebFetch is blocked by X's paywall (HTTP 402). Using it will produce empty or
fabricated content. There are zero cases where WebFetch is acceptable for X.

Procedure for any tweet URL:

1. `agent-browser open <tweet-url>`
2. `agent-browser snapshot -i`
3. Read the exact tweet text from the snapshot
4. `agent-browser close`

**Never write about a tweet's content without first fetching it with
`agent-browser`. Writing from memory or inference is forbidden.**

## Other JavaScript-Rendered Pages

When WebFetch fails to retrieve web content (e.g., JavaScript-rendered pages),
use `agent-browser` as a fallback. It is a CLI browser automation tool designed
for AI agents.

Basic usage:

1. `agent-browser open <URL>` — open a page
2. `agent-browser snapshot -i` — get interactive element tree
3. `agent-browser click @<ref>` — click an element
4. `agent-browser eval "<JS expression>"` — extract text via JavaScript
5. `agent-browser close` — close the browser
