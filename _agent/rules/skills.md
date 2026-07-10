# Skills

## Skill Location (ABSOLUTE PRIORITY)

**Always create and search for skills in the project-local directory.**

- Local (correct): `.claude/skills/<skill-name>/SKILL.md`
- Global (forbidden): `~/.claude/skills/`

Skills are project-specific artifacts and must live with the project.

## Skill Lookup (ABSOLUTE PRIORITY)

**When the user invokes a slash command (e.g. `/some-skill`), ALWAYS check
the project-local `.claude/skills/` directory BEFORE concluding it does not
exist.** The system's built-in skill list is NOT exhaustive — project-local
skills may not appear there. The local directory is the authoritative source.

Procedure:

1. Check `.claude/skills/<skill-name>/SKILL.md` with Read.
2. If not found, try Glob with `.claude/skills/**/*`.
3. If not found, try `ls .claude/skills/`.
4. Only after all three fail, ask the user for the correct path.
5. NEVER say a skill does not exist without completing steps 1-3.
