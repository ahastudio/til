# Skills

## Skill Location (ABSOLUTE PRIORITY)

**Always create and search for skills in the project-local directory.**

- Local (correct): `.claude/skills/<skill-name>/SKILL.md`
- Global (forbidden): `~/.claude/skills/`

Skills are project-specific artifacts and must live with the project.

## Writing a Skill

- The description says what the skill does and when to use it, in the third
  person. A vague description ("helps with documents") does not let the agent
  choose the skill.
- Write only what the agent cannot find on its own: team procedures and
  non-obvious constraints, never a description of the code layout.
- A skill with side effects (publishing, deleting, spending, writing outside
  the project) runs only when the user invokes it. Mark it user-invoked in the
  frontmatter where the agent supports that.
- Keep SKILL.md under 500 lines and its essentials within the first 100.
  Detail goes in reference files one level below it, and a reference file
  longer than 100 lines starts with a contents block.
- Give the skill a check that comes back pass or fail, such as a script or a
  gate, and make the final report quote its result.
- A rule that must hold on every run does not live only in a skill: also
  enforce it in the agent's enforcement settings (see Rule Writing Guidelines
  in `AGENTS.md`).
- No time-sensitive statements, one term per concept, forward slashes in
  paths.

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
