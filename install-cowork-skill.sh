#!/bin/bash
# Install JobReforgerAI skill for Claude Cowork
# Run this from the JobReforgerAI project root directory

set -e

SKILL_SOURCE=".claude/skills/jobreforger"
SKILL_DEST="$HOME/.claude/skills/jobreforger"

if [ ! -f "$SKILL_SOURCE/SKILL.md" ]; then
    echo "Error: Run this script from the JobReforgerAI project root directory."
    echo "Usage: cd /path/to/JobReforgerAI && bash install-cowork-skill.sh"
    exit 1
fi

echo "Installing JobReforgerAI skill for Claude Cowork..."

# Create destination directory
mkdir -p "$SKILL_DEST"

# Copy skill files
cp -r "$SKILL_SOURCE/"* "$SKILL_DEST/"

echo "Installed to: $SKILL_DEST"
echo ""
echo "The 'jobreforger' skill is now available in Claude Cowork."
echo "Open a new Cowork session and try: 'Help me apply to this job: [paste a JD]'"
