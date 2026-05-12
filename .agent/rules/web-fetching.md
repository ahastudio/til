# Web Content Fetching

When WebFetch fails to retrieve web content (e.g., JavaScript-rendered pages),
use `agent-browser` as a fallback. It is a CLI browser automation tool designed
for AI agents.

Basic usage:

1. `agent-browser open <URL>` — open a page
2. `agent-browser snapshot -i` — get interactive element tree
3. `agent-browser click @<ref>` — click an element
4. `agent-browser eval "<JS expression>"` — extract text via JavaScript
5. `agent-browser close` — close the browser
