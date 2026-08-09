#!/usr/bin/env bash
set -e

# ==============================================================================
# Antigravity MacBook Pro <-> iMac Synchronization Script
# ==============================================================================

WORKSPACE_ROOT="/Users/gdone/dev/codyssey"
GLOBAL_CONFIG="/Users/gdone/.gemini/config"

echo "🔄 [1/4] Starting Antigravity Cross-Device Synchronization..."
echo "📍 Machine: $(hostname) | Date: $(date)"

# 1. Sync Global Skills to Workspace
mkdir -p "$GLOBAL_CONFIG/skills/antigravity-sync"
if [ -f "$WORKSPACE_ROOT/.agents/skills/antigravity-sync/SKILL.md" ]; then
    cp -R "$WORKSPACE_ROOT/.agents/skills/antigravity-sync/"* "$GLOBAL_CONFIG/skills/antigravity-sync/"
    echo "✅ Global Skill (~/.gemini/config/skills/antigravity-sync) updated."
fi

# 2. Pull latest main workspace repository
echo "📥 [2/4] Pulling main repository ($WORKSPACE_ROOT)..."
git -C "$WORKSPACE_ROOT" pull --rebase origin main || echo "⚠️ Warning: git pull on main repo failed or already clean."

# 3. Pull all sub-repositories
echo "📥 [3/4] Pulling sub-repositories..."
for dir in "$WORKSPACE_ROOT"/*/; do
    if [ -d "$dir/.git" ]; then
        repo_name=$(basename "$dir")
        echo "   - Syncing $repo_name..."
        git -C "$dir" pull --rebase origin main 2>/dev/null || git -C "$dir" pull --rebase 2>/dev/null || echo "     ⚠️ Pull skipped for $repo_name"
    fi
done

# 4. Check for uncommitted changes & push
echo "📤 [4/4] Checking workspace status and pushing changes..."
if git -C "$WORKSPACE_ROOT" diff --quiet && git -C "$WORKSPACE_ROOT" diff --cached --quiet; then
    echo "✅ Workspace is clean."
else
    echo "📦 Committing updated workspace pointers..."
    git -C "$WORKSPACE_ROOT" add .
    git -C "$WORKSPACE_ROOT" commit -m "chore(sync): auto-sync Antigravity skills and workspace state between devices [$(date '+%Y-%m-%d %H:%M')]"
fi

git -C "$WORKSPACE_ROOT" push origin main 2>/dev/null || echo "⚠️ Push failed or up-to-date."

echo "🎉 Antigravity Synchronization Completed Successfully!"
