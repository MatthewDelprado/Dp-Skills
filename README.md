# claude-skills

Personal Claude skills, installed as a plugin marketplace.

| Skill | What it does |
| --- | --- |
| `show-me` | Explains code, flows and changes in chat with the smallest useful view: pseudocode, call tree, component tree, file tree, Mermaid or diff |
| `mock-up` | Builds a throwaway HTML preview of a UI idea in the current repo's own look and feel |
| `skill-feedback` | Logs feedback on a skill as a GitHub issue. Drafts it, you confirm |
| `skill-review` | Reads open feedback issues for a skill and opens a PR with proposed edits. You merge |
| `grill-me` | Interviews you about a plan, one question at a time, with a live decision-tree page |

## Install

```
/plugin marketplace add MatthewDelprado/Dp-Skills
/plugin install show-me@claude-skills
/plugin install mock-up@claude-skills
/plugin install skill-feedback@claude-skills
```

Or with the skills CLI: `npx skills add MatthewDelprado/Dp-Skills --skill show-me`.

## How they fit together

`show-me` and `mock-up` are model-routed. Say "diagram this" or "mock this up" and the right one runs. Each names the other, so a UI question reaches `mock-up` and a logic question reaches `show-me`. `skill-review` is slash-only (`/skill-review show-me`).

When a skill gets it wrong (you asked for a different view, trimmed the output, or it had to guess), it ends with one line offering to log it, at most once per session. Say yes and `skill-feedback` drafts a GitHub issue for you to confirm. Run `/skill-review <skill>` now and then. It groups the open issues, changes a skill only where two or more agree, and opens a PR that must not grow the skill. You review and merge.

## Adding things

New view in `show-me`: add one bullet with a 3 to 4 line example to its `SKILL.md`. If it needs more than about 10 lines, put it in `references/<view>.md` and link it with one line. Keep each `SKILL.md` at 100 lines or fewer.

New skill:

1. Create `plugins/<name>/skills/<name>/SKILL.md` with `name` and `description` frontmatter.
2. Add `plugins/<name>/.claude-plugin/plugin.json`.
3. Add the plugin to `.claude-plugin/marketplace.json`.
4. Add a line under Related skills in at least one sibling that names it. A skill that stands alone goes in `STANDALONE` in `scripts/check.py`.
5. Run `python3 scripts/check.py`. CI runs the same check on every PR.

## Layout

```
.claude-plugin/marketplace.json
plugins/<name>/.claude-plugin/plugin.json
plugins/<name>/skills/<name>/SKILL.md
plugins/<name>/skills/<name>/references/
scripts/check.py        # layout, frontmatter, size cap, sibling links
scripts/publish.sh      # one-time: create the GitHub repo and push
.github/workflows/check.yml
```

`show-me` started from humanlayer's skill of the same name (MIT), trimmed and extended.
