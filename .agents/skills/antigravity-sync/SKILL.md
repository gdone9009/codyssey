---
name: antigravity-sync
description: >-
  Synchronize Google Antigravity configurations, skills, rules, MCP servers, and workspace repositories
  between devices (MacBook Pro and iMac). Use when the user asks to sync Antigravity setup, share skills between
  MacBook Pro and iMac, or synchronize local and remote Git state across machines.
---

# 🔄 Antigravity Cross-Device Synchronization Skill (MacBook Pro ↔ iMac)

This skill provides a standardized, automated workflow to synchronize Google Antigravity (AGY) agent configurations, global settings, skills, rules, and workspace git repositories between **MacBook Pro** and **iMac**.

---

## 🎯 1. Overview & Synchronization Architecture

Antigravity operates across two primary state layers:

1. **Workspace Layer (`.agents/`)**:
   - Location: `<workspace_root>/.agents/` (e.g., `/Users/gdone/dev/codyssey/.agents/`)
   - Contents: Project rules (`AGENTS.md`), project skills (`.agents/skills/`), MCP configs (`mcp_config.json`), submodules.
   - Sync Mechanism: Tracked via Git (`git@github.com:gdone9009/codyssey.git`).

2. **Global System Layer (`~/.gemini/config/`)**:
   - Location: `/Users/gdone/.gemini/config/`
   - Contents: Global rules, global plugins/skills, MCP configurations (`mcp_config.json`), project metadata.
   - Sync Mechanism: Automated sync script or Git tracking.

---

## 🛠️ 2. Step-by-Step Synchronization Protocol

### Step 1: Workspace & Repository Sync (Git Automation)

Execute the automated synchronization script to pull remote changes from iMac/MacBook Pro and push local commits:

```bash
/Users/gdone/dev/codyssey/.agents/skills/antigravity-sync/scripts/sync_antigravity.sh
```

### Step 2: Manual / CLI Verification Commands

If running manually via terminal:

```bash
# 1. Main Repository Pull & Rebase
git -C /Users/gdone/dev/codyssey pull --rebase origin main

# 2. Sub-repositories & Submodules Sync
for d in /Users/gdone/dev/codyssey/*/; do
  if [ -d "$d/.git" ]; then
    echo "=== Syncing $d ==="
    git -C "$d" pull --rebase
  fi
done

# 3. Push local changes
git -C /Users/gdone/dev/codyssey push origin main
```

### Step 3: Global Config Verification

Ensure `~/.gemini/config/skills/antigravity-sync` and `.agents/skills/antigravity-sync` are aligned across both machines.

---

## 🧪 3. Verification Checklist

- [ ] All sub-repositories cleaned and committed (`git status`).
- [ ] Remote `origin/main` pulled and up to date without conflicts.
- [ ] Local commits pushed to GitHub.
- [ ] Custom skills and rules reflected in both MacBook Pro and iMac environments.
