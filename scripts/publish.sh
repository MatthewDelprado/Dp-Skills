#!/usr/bin/env bash
# One-time: create a private repo under the GitHub account you are signed into, and push.
# Usage: ./scripts/publish.sh [repo-name]   (default: claude-skills)
set -euo pipefail
cd "$(dirname "$0")/.."
command -v gh >/dev/null || { echo "Install the GitHub CLI first: https://cli.github.com"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Run: gh auth login"; exit 1; }
REPO="${1:-claude-skills}"
OWNER="$(gh api user -q .login)"
# Fill the owner placeholder (works with both GNU and BSD sed)
grep -rl "__OWNER__" . --exclude-dir=.git --exclude=publish.sh | while read -r f; do sed -i.bak "s/__OWNER__/$OWNER/g" "$f"; rm -f "$f.bak"; done
if [ "$REPO" != "claude-skills" ]; then
  grep -rl "$OWNER/claude-skills" . --exclude-dir=.git --exclude=publish.sh | while read -r f; do sed -i.bak "s#$OWNER/claude-skills#$OWNER/$REPO#g" "$f"; rm -f "$f.bak"; done
fi
python3 scripts/check.py
[ -d .git ] || git init -b main
git add -A
git commit -m "Initial skills: show-me, mock-up, skill-feedback, skill-review, grill-me"
gh repo create "$OWNER/$REPO" --private --source . --push
echo "Done: https://github.com/$OWNER/$REPO"
echo "Install: /plugin marketplace add $OWNER/$REPO"
