#!/usr/bin/env bash
# Install the youtube-to-agent skill globally into ~/.claude/skills.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
dest="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/youtube-to-agent"
mkdir -p "$(dirname "$dest")"
rm -rf "$dest"
cp -R "$here/.claude/skills/youtube-to-agent" "$dest"
echo "Installed to $dest"
python3 -c "import google.genai" 2>/dev/null || echo "Next: pip install google-genai"
[ -n "${GEMINI_API_KEY:-}" ] || echo "Next: export GEMINI_API_KEY=... (free key: https://aistudio.google.com/apikey)"
echo "Also install /watch in Claude Code:"
echo "  /plugin marketplace add bradautomates/claude-video"
echo "  /plugin install watch@claude-video"
