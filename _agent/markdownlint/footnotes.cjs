// Custom markdownlint rule: footnote integrity.
// - undefined reference: [^x] used but no "[^x]:" definition
// - duplicate definition: "[^x]:" defined more than once
// - stacked definitions: definitions on consecutive lines
// Unused definitions are already reported by MD053.

const DEF = /^\[\^([^\]\s]+)\]:/;
const REF = /\[\^([^\]\s]+)\](?!:)/g;

module.exports = {
  names: ["FN001", "footnote-integrity"],
  description: "Footnotes must be defined once, separated, and referenced",
  tags: ["footnotes"],
  parser: "none",
  function: (params, onError) => {
    const defs = new Map();
    let inFence = false;
    let prevWasDef = false;

    params.lines.forEach((line, i) => {
      const lineNumber = i + 1;
      if (/^\s*(```|~~~)/.test(line)) {
        inFence = !inFence;
        prevWasDef = false;
        return;
      }
      if (inFence) return;

      const m = DEF.exec(line);
      if (m) {
        if (defs.has(m[1])) {
          onError({
            lineNumber,
            detail: `Duplicate footnote definition: "^${m[1]}"`,
            context: line.slice(0, 40),
          });
        }
        defs.set(m[1], lineNumber);
        if (prevWasDef) {
          onError({
            lineNumber,
            detail: "Footnote definitions must be separated by a blank line",
            context: line.slice(0, 40),
          });
        }
        prevWasDef = true;
      } else {
        prevWasDef = false;
      }
    });

    inFence = false;
    params.lines.forEach((line, i) => {
      if (/^\s*(```|~~~)/.test(line)) {
        inFence = !inFence;
        return;
      }
      if (inFence || DEF.test(line)) return;
      const text = line.replace(/`[^`]*`/g, (s) => " ".repeat(s.length));
      for (const m of text.matchAll(REF)) {
        if (!defs.has(m[1])) {
          onError({
            lineNumber: i + 1,
            detail: `Footnote reference without definition: "^${m[1]}"`,
            context: m[0],
          });
        }
      }
    });
  },
};
