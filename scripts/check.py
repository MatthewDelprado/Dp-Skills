#!/usr/bin/env python3
"""Repo check. Fails the PR when the layout, frontmatter or sibling links drift."""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAX_SKILL_LINES = 100
STANDALONE = {"grill-me"}  # skills that need no sibling mention

errors = []

def err(msg):
    errors.append(msg)

def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out

market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
listed = {p["name"]: p for p in market.get("plugins", [])}
folders = {p.name for p in (ROOT / "plugins").iterdir() if p.is_dir()}

for name in sorted(folders - set(listed)):
    err(f"plugins/{name} is not listed in marketplace.json")
for name in sorted(set(listed) - folders):
    err(f"marketplace.json lists {name} but plugins/{name} does not exist")

skills = {}  # skill name -> text of SKILL.md plus references
for plugin in sorted(folders):
    pj = ROOT / "plugins" / plugin / ".claude-plugin" / "plugin.json"
    if not pj.exists():
        err(f"plugins/{plugin} has no .claude-plugin/plugin.json")
    else:
        if json.loads(pj.read_text()).get("name") != plugin:
            err(f"plugins/{plugin}/plugin.json name does not match the folder")
    if plugin in listed and listed[plugin].get("source") != f"./plugins/{plugin}":
        err(f"marketplace source for {plugin} should be ./plugins/{plugin}")
    sdir = ROOT / "plugins" / plugin / "skills"
    if not sdir.is_dir():
        err(f"plugins/{plugin} has no skills folder")
        continue
    for skill_dir in sorted(p for p in sdir.iterdir() if p.is_dir()):
        md = skill_dir / "SKILL.md"
        if not md.exists():
            err(f"{skill_dir.relative_to(ROOT)} has no SKILL.md")
            continue
        text = md.read_text()
        fm = frontmatter(text)
        if fm is None:
            err(f"{md.relative_to(ROOT)} has no frontmatter")
            continue
        if not fm.get("name"):
            err(f"{md.relative_to(ROOT)} frontmatter is missing name")
        elif fm["name"] != skill_dir.name:
            err(f"{md.relative_to(ROOT)} name '{fm['name']}' does not match folder '{skill_dir.name}'")
        if not fm.get("description"):
            err(f"{md.relative_to(ROOT)} frontmatter is missing description")
        lines = len(text.splitlines())
        if lines > MAX_SKILL_LINES:
            err(f"{md.relative_to(ROOT)} is {lines} lines, over the {MAX_SKILL_LINES} line cap. Move detail into references/")
        refs = "".join(p.read_text() for p in skill_dir.glob("references/*.md"))
        skills[skill_dir.name] = text + refs

for name in sorted(skills):
    if name in STANDALONE:
        continue
    mentioned = any(re.search(rf"`{re.escape(name)}`|\({re.escape(name)}\)", t) for other, t in skills.items() if other != name)
    if not mentioned:
        err(f"skill '{name}' is not named by any sibling skill. Add a line under Related skills in a related skill")

if errors:
    print("check failed:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(f"check passed: {len(skills)} skills in {len(folders)} plugins")
