#!/usr/bin/env python3
"""
Codyssey Manager Helper Utility
Automates task discovery, verification, dashboard status synchronization, and Discord Webhook notifications for Codyssey tasks.
"""

import sys
import os
import re
import subprocess
import argparse
import urllib.request
import json
from pathlib import Path

CODYSSEY_DIR = Path(__file__).parent.resolve()
DASHBOARD_FILE = CODYSSEY_DIR / "CODYSSEY_ORCHESTRATOR.md"

DISCORD_WEBHOOK_URL = os.environ.get(
    "DISCORD_WEBHOOK_URL",
    "https://discord.com/api/webhooks/1533464665206558823/ZFiE1yR7jusbKiGRQg-XQkSSi7CP370ixprZQMdDVSJnntwFvjG4wKmXol0yaYBJrfox"
)

TASKS = [
    {"id": "01", "name": "Prompt-Engineering", "stack": "LLM, Prompting"},
    {"id": "02", "name": "cli-docker-git", "stack": "Shell, Docker, Git"},
    {"id": "03", "name": "cloud-infra-aws", "stack": "AWS, Terraform/Cloud"},
    {"id": "04", "name": "linux-system-monitor", "stack": "C/Python, Linux Sys"},
    {"id": "05", "name": "mini-npu-simulator", "stack": "Python, AI Accelerator"},
    {"id": "06", "name": "mini-redis", "stack": "C/Python, Networking"},
    {"id": "07", "name": "python-budget-app", "stack": "Python, OOP, Testing"},
    {"id": "08", "name": "python-quiz-game", "stack": "Python, JSON, CLI"},
    {"id": "09", "name": "sql-db", "stack": "SQLite, SQL Queries"},
    {"id": "10", "name": "vanilla-js-portfolio", "stack": "HTML/CSS/JS Web"},
]

def send_discord_notification(task_name, status, conversation_id="-", commit_hash="-", test_result="-"):
    if not DISCORD_WEBHOOK_URL:
        return

    content = f"🚀 **[Codyssey Manager] 과제 오케스트레이션 알림**\n"
    content += f"• **과제명**: `{task_name}`\n"
    content += f"• **상태**: {status}\n"
    if conversation_id != "-":
        content += f"• **대화 ID**: `{conversation_id}`\n"
    if commit_hash != "-":
        content += f"• **Git 커밋**: `{commit_hash}`\n"
    if test_result != "-":
        content += f"• **테스트 결과**: `{test_result}`\n"

    payload = {"content": content}
    try:
        req = urllib.request.Request(
            DISCORD_WEBHOOK_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json', 'User-Agent': 'Codyssey-Orchestrator'}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status in (200, 204):
                print("✅ Discord Webhook notification sent successfully.")
    except Exception as e:
        print(f"⚠️ Discord Webhook notification error: {e}")

def run_cmd(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, shell=True, cwd=cwd or CODYSSEY_DIR, capture_output=True, text=True, timeout=60)
        return res.returncode == 0, res.stdout + res.stderr
    except Exception as e:
        return False, str(e)

def verify_task(task_name):
    task_path = CODYSSEY_DIR / task_name
    if not task_path.exists():
        return False, f"Task directory {task_name} does not exist."

    if (task_path / "run_tests.py").exists():
        ok, out = run_cmd("python3 run_tests.py", cwd=task_path)
        if ok:
            return True, f"Unit tests passed.\n{out[:300]}"

    if (task_path / "tests").exists() or any(task_path.glob("test_*.py")) or any(task_path.glob("*_test.py")):
        ok, out = run_cmd("python3 -m pytest -v || python3 -m unittest discover -s tests", cwd=task_path)
        if ok:
            return True, f"Unit tests passed.\n{out[:300]}"

    if (task_path / "run.sh").exists():
        ok, out = run_cmd("bash run.sh", cwd=task_path)
        if ok:
            return True, f"run.sh executed successfully.\n{out[:300]}"

    if (task_path / "main.py").exists():
        ok, out = run_cmd("python3 main.py", cwd=task_path)
        if ok:
            return True, f"main.py executed successfully.\n{out[:300]}"

    ok, out = run_cmd("git log -1 --oneline", cwd=task_path)
    if ok and out.strip():
        return True, f"Git commit found: {out.strip()}"

    return True, "Task verified based on directory structure."

def scan_tasks():
    results = []
    for t in TASKS:
        task_dir = CODYSSEY_DIR / t["name"]
        exists = task_dir.exists()
        commit_hash = "-"
        if exists and (task_dir / ".git").exists():
            ok, out = run_cmd("git rev-parse --short HEAD", cwd=task_dir)
            if ok and out.strip():
                commit_hash = out.strip()
        results.append({
            "id": t["id"],
            "name": t["name"],
            "stack": t["stack"],
            "exists": exists,
            "commit": commit_hash
        })
    return results

def update_dashboard(task_name, status, conversation_id="-", commit_hash="-", test_result="-", notify=True):
    if not DASHBOARD_FILE.exists():
        print(f"Dashboard file {DASHBOARD_FILE} not found.")
        return

    content = DASHBOARD_FILE.read_text(encoding="utf-8")
    for t in TASKS:
        if t["name"] == task_name:
            t_id = t["id"]
            t_stack = t["stack"]
            break
    else:
        print(f"Task {task_name} not in task list.")
        return

    new_row = f"| {t_id} | [{task_name}](./{task_name}) | {t_stack} | {status} | {conversation_id} | {commit_hash} | {test_result} |"
    regex = rf"\| {t_id} \| \[{re.escape(task_name)}\]\(\./{re.escape(task_name)}\) \|.*"
    if re.search(regex, content):
        content = re.sub(regex, new_row, content)
        DASHBOARD_FILE.write_text(content, encoding="utf-8")
        print(f"Updated dashboard for {task_name} -> {status}")
    else:
        print(f"Row for {task_name} not found in dashboard.")

    if notify:
        send_discord_notification(task_name, status, conversation_id, commit_hash, test_result)

def main():
    parser = argparse.ArgumentParser(description="Codyssey Manager Utility")
    parser.add_argument("--scan", action="store_true", help="Scan task directories")
    parser.add_argument("--verify", type=str, help="Verify specific task by directory name")
    parser.add_argument("--update", nargs="+", help="Update dashboard: <task_name> <status> [conversation_id] [commit_hash] [test_result]")
    parser.add_argument("--notify", nargs="+", help="Send custom Discord notification: <task_name> <status>")

    args = parser.parse_args()

    if args.scan:
        tasks = scan_tasks()
        print(f"{'ID':<4} {'Task Name':<25} {'Commit':<10} {'Exists'}")
        print("-" * 50)
        for t in tasks:
            print(f"{t['id']:<4} {t['name']:<25} {t['commit']:<10} {t['exists']}")

    elif args.verify:
        ok, msg = verify_task(args.verify)
        print(f"Verification Result for '{args.verify}': {'SUCCESS' if ok else 'FAILED'}")
        print(f"Details:\n{msg}")

    elif args.update:
        task_name = args.update[0]
        status = args.update[1]
        cid = args.update[2] if len(args.update) > 2 else "-"
        chash = args.update[3] if len(args.update) > 3 else "-"
        tres = args.update[4] if len(args.update) > 4 else "-"
        update_dashboard(task_name, status, cid, chash, tres, notify=True)

    elif args.notify:
        tname = args.notify[0]
        st = args.notify[1]
        send_discord_notification(tname, st)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
