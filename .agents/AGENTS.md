# Workspace Rules & Turbo Mode Configuration

## ⚡ Turbo Mode & Maximum Autonomy Directives
1. **Full Autonomous Execution**: Execute tasks, implement features, run commands, and invoke subagents proactively without stopping for intermediate permission requests.
2. **End-to-End Verification**: Always build, test, and verify code changes automatically before declaring task completion.
3. **Multi-Agent Orchestration**: Utilize parallel subagents (`invoke_subagent`) whenever tasks can be split across audit, development, security, or testing roles.
4. **Git Operations**: Automatically handle git commits, branching, and repository synchronizations as needed.
5. **GitHub & MCP Integration**: Operate using authenticated SSH (`git@github.com:gdone9009`) and GitHub MCP Server integration for repository actions.
