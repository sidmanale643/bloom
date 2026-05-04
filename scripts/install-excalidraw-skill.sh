#!/bin/bash
# Install the Excalidraw diagram skill for Claude Code / OpenCode
# This enables Bloom to generate Excalidraw diagrams from natural language descriptions

set -e

SKILL_REPO="https://github.com/coleam00/excalidraw-diagram-skill.git"
SKILL_NAME="excalidraw-diagram"
TMP_DIR="/tmp/excalidraw-diagram-skill-$$"

# Detect available agent skill directories
CLAUDE_DIR="$HOME/.claude/skills"
OPENCODE_DIR="$HOME/.config/opencode/skills"

DIRS=()
[ -d "$CLAUDE_DIR" ] && DIRS+=("$CLAUDE_DIR")
[ -d "$OPENCODE_DIR" ] && DIRS+=("$OPENCODE_DIR")

if [ ${#DIRS[@]} -eq 0 ]; then
    echo "Error: No agent skills directory found."
    echo "Expected one of:"
    echo "  - $CLAUDE_DIR   (for Claude Code)"
    echo "  - $OPENCODE_DIR (for OpenCode)"
    echo ""
    echo "Please ensure your coding agent is installed, then rerun this script."
    exit 1
fi

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "Error: 'uv' is required but not installed."
    echo "Install it from: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

# Clone the skill repo
echo "Cloning excalidraw-diagram-skill..."
git clone --depth 1 "$SKILL_REPO" "$TMP_DIR" > /dev/null 2>&1

# Install into each detected directory
for DIR in "${DIRS[@]}"; do
    SKILL_PATH="$DIR/$SKILL_NAME"
    
    if [ -d "$SKILL_PATH" ]; then
        echo "Skill already exists at $SKILL_PATH — skipping copy"
    else
        echo "Installing to $SKILL_PATH..."
        cp -r "$TMP_DIR" "$SKILL_PATH"
    fi
    
    # Setup render pipeline
    echo "Setting up render pipeline in $SKILL_PATH/references..."
    cd "$SKILL_PATH/references"
    uv sync
    uv run playwright install chromium
    echo "Render pipeline ready."
done

# Cleanup
rm -rf "$TMP_DIR"

echo ""
echo "Excalidraw diagram skill installed successfully."
echo "Restart your coding agent to use it."
echo ""
echo "Usage example:"
echo '  "Draw the three-layer architecture of this vault"'
