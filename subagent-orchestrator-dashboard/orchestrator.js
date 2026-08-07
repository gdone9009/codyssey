const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3456;

// Load subagent configuration
let config = JSON.parse(fs.readFileSync(path.join(__dirname, 'subagent_config.json'), 'utf8'));

// Live logs buffer
const logs = [
  { timestamp: new Date().toLocaleTimeString(), level: 'INFO', agentId: 'master', message: 'Antigravity Multi-Agent Orchestrator 2.0 initialized.' },
  { timestamp: new Date().toLocaleTimeString(), level: 'INFO', agentId: 'master', message: 'Spawning subagent cluster: [subagent-01, subagent-02, subagent-03, subagent-04]' },
  { timestamp: new Date().toLocaleTimeString(), level: 'SUCCESS', agentId: 'subagent-03', message: 'Performance Profiler completed IO benchmark in 240ms.' },
  { timestamp: new Date().toLocaleTimeString(), level: 'AGENT_MSG', agentId: 'subagent-01', message: 'Discovered 42 source files. Parsing abstract syntax trees...' },
  { timestamp: new Date().toLocaleTimeString(), level: 'AGENT_MSG', agentId: 'subagent-02', message: 'Scanning environment configurations. Zero unencrypted secrets exposed.' }
];

const sampleLogMessages = [
  { level: 'AGENT_MSG', agentId: 'subagent-01', message: 'Code Auditor: AST traversal completed for src/components.' },
  { level: 'AGENT_MSG', agentId: 'subagent-02', message: 'Security Agent: Verified TLS 1.3 policy & CORS headers.' },
  { level: 'AGENT_MSG', agentId: 'subagent-04', message: 'Test Generator: Created 14 unit test specs for API handlers.' },
  { level: 'SUCCESS', agentId: 'master', message: 'Subagent pulse sync: all 4 workers healthy (Latency: 12ms).' },
  { level: 'INFO', agentId: 'subagent-01', message: 'Refactoring suggestion: Split heavy function in orchestrator.js.' },
  { level: 'AGENT_MSG', agentId: 'subagent-02', message: 'Static Analysis: No high severity vulnerabilities detected.' }
];

// Live telemetry loop
setInterval(() => {
  // Update subagent metrics
  config.subagents.forEach(agent => {
    if (agent.status === 'RUNNING' || agent.status === 'IN_PROGRESS') {
      agent.progress = Math.min(100, agent.progress + Math.floor(Math.random() * 4) + 1);
      agent.cpu = (Math.floor(Math.random() * 15) + 10) + '%';
      agent.memory = (Math.floor(Math.random() * 30) + 120) + ' MB';
      agent.logs_count += 1;

      if (agent.progress >= 100) {
        agent.status = 'COMPLETED';
        logs.unshift({
          timestamp: new Date().toLocaleTimeString(),
          level: 'SUCCESS',
          agentId: agent.id,
          message: `${agent.name} (${agent.id}) successfully completed assigned task!`
        });
      }
    }
  });

  // Push random agent log
  if (Math.random() > 0.4) {
    const randomMsg = sampleLogMessages[Math.floor(Math.random() * sampleLogMessages.length)];
    logs.unshift({
      timestamp: new Date().toLocaleTimeString(),
      level: randomMsg.level,
      agentId: randomMsg.agentId,
      message: randomMsg.message
    });
    if (logs.length > 100) logs.pop();
  }
}, 2500);

// HTTP Server
const server = http.createServer((req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  if (req.url === '/api/status') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ config, logs }));
  } else if (req.url === '/api/dispatch' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const data = JSON.parse(body || '{}');
        const newId = `subagent-0${config.subagents.length + 1}`;
        const newAgent = {
          id: newId,
          name: data.name || `Task Agent ${config.subagents.length + 1}`,
          type: 'custom_worker',
          role: data.role || 'Dynamic Subagent Task',
          model: 'Gemini 3.6 Flash',
          status: 'RUNNING',
          progress: 10,
          task: data.task || 'Processing dynamic subagent workload',
          cpu: '15%',
          memory: '130 MB',
          logs_count: 1
        };
        config.subagents.push(newAgent);
        logs.unshift({
          timestamp: new Date().toLocaleTimeString(),
          level: 'INFO',
          agentId: 'master',
          message: `Dynamically spawned subagent: ${newAgent.name} [${newId}]`
        });
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, agent: newAgent }));
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
  } else {
    // Serve static files
    let filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
    const ext = path.extname(filePath);
    let contentType = 'text/html';
    if (ext === '.css') contentType = 'text/css';
    if (ext === '.js') contentType = 'text/javascript';
    if (ext === '.json') contentType = 'application/json';

    fs.readFile(filePath, (err, content) => {
      if (err) {
        res.writeHead(404);
        res.end('File not found');
      } else {
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(content);
      }
    });
  }
});

server.listen(PORT, () => {
  console.log(`[Antigravity Orchestrator] Server running at http://localhost:${PORT}`);
});
