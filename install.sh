#!/usr/bin/env bash
# Install the interactive-deep-research skills into a Claude Code skills dir
# and symlink the `idr`, `askq`, and `scorecard` drivers onto your PATH.
set -euo pipefail

SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$SKILLS_DIR" "$BIN_DIR"

for skill in integrative-deep-research askq interactive-deep-research deep-research-scorecard; do
  src="$HERE/skills/$skill"
  [ -d "$src" ] || continue
  rm -rf "${SKILLS_DIR:?}/$skill"
  cp -R "$src" "$SKILLS_DIR/$skill"
  echo "installed skill: $skill -> $SKILLS_DIR/$skill"
done

# drivers on PATH
ln -sf "$SKILLS_DIR/integrative-deep-research/scripts/idr.py" "$BIN_DIR/idr"
ln -sf "$SKILLS_DIR/askq/scripts/askq.py" "$BIN_DIR/askq"
ln -sf "$SKILLS_DIR/deep-research-scorecard/scripts/scorecard.py" "$BIN_DIR/scorecard"
chmod +x \
  "$SKILLS_DIR/integrative-deep-research/scripts/idr.py" \
  "$SKILLS_DIR/askq/scripts/askq.py" \
  "$SKILLS_DIR/deep-research-scorecard/scripts/scorecard.py"
echo "linked drivers: $BIN_DIR/idr , $BIN_DIR/askq , $BIN_DIR/scorecard"

echo
echo "Preflight:"
echo "  - NotebookLM CLI:  nlm doctor   (run 'nlm login' if it errors)"
echo "  - Antigravity:     agy --version (optional; pipeline degrades gracefully without it)"
echo "  - Offline smoke:   IDR_MOCK=1 idr plan \"test topic\""
