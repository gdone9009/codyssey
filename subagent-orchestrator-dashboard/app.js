// Subagent Orchestrator Frontend Engine

let subagentData = [];
let logEntries = [];
let currentSubagentFilter = 'ALL';
let currentLogFilter = 'ALL';
let resourceChart = null;

// Initial state fallback
const defaultState = {
  subagents: [
    {
      id: "subagent-01",
      name: "Code Auditor Agent",
      type: "code_auditor",
      role: "Static Code Analysis & AST Parsing",
      model: "Gemini 3.6 Flash",
      status: "RUNNING",
      progress: 78,
      task: "Scanning /dev/codyssey AST tree & dependencies",
      cpu: "14%",
      memory: "142 MB",
      logs_count: 42
    },
    {
      id: "subagent-02",
      name: "Security Audit Agent",
      type: "sec_audit",
      role: "Vulnerability & Credentials Verification",
      model: "Gemini 3.6 Flash",
      status: "RUNNING",
      progress: 62,
      task: "Auditing open ports, env secrets, and SQL injections",
      cpu: "22%",
      memory: "188 MB",
      logs_count: 31
    },
    {
      id: "subagent-03",
      name: "Performance Profiler",
      type: "perf_profiler",
      role: "Event Loop & IO Bottleneck Optimization",
      model: "Gemini 3.6 Flash",
      status: "COMPLETED",
      progress: 100,
      task: "Benchmarking async throughput and latency",
      cpu: "2%",
      memory: "94 MB",
      logs_count: 55
    },
    {
      id: "subagent-04",
      name: "Test Generator Agent",
      type: "test_synth",
      role: "Automated Unit & Integration Test Generation",
      model: "Gemini 3.6 Flash",
      status: "IN_PROGRESS",
      progress: 45,
      task: "Generating Jest test suites for backend modules",
      cpu: "18%",
      memory: "165 MB",
      logs_count: 19
    }
  ]
};

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
  initChart();
  subagentData = defaultState.subagents;
  renderTopology();
  renderSubagentCards();
  
  // Start polling or fallback simulation
  fetchTelemetry();
  setInterval(fetchTelemetry, 2500);
});

// Fetch live telemetry from orchestrator server
async function fetchTelemetry() {
  try {
    const res = await fetch('http://localhost:3456/api/status');
    if (res.ok) {
      const data = await res.json();
      if (data.config && data.config.subagents) {
        subagentData = data.config.subagents;
      }
      if (data.logs) {
        logEntries = data.logs;
      }
    } else {
      simulateLocalStep();
    }
  } catch (e) {
    // If backend server isn't running, run client-side simulation
    simulateLocalStep();
  }

  updateMetrics();
  renderTopology();
  renderSubagentCards();
  renderLogs();
  updateChartData();
}

// Client-side simulation step fallback
function simulateLocalStep() {
  subagentData.forEach(agent => {
    if (agent.status === 'RUNNING' || agent.status === 'IN_PROGRESS') {
      agent.progress = Math.min(100, agent.progress + Math.floor(Math.random() * 4) + 1);
      agent.cpu = (Math.floor(Math.random() * 15) + 10) + '%';
      agent.memory = (Math.floor(Math.random() * 20) + 130) + ' MB';
      
      if (agent.progress >= 100) {
        agent.status = 'COMPLETED';
        addLocalLog('SUCCESS', agent.id, `${agent.name} finished task!`);
      }
    }
  });

  if (Math.random() > 0.4) {
    const msgs = [
      { id: 'subagent-01', msg: 'AST Parser: Processed 1,200 lines of JavaScript.' },
      { id: 'subagent-02', msg: 'Security Audit: Scanned dependency tree for known CVEs.' },
      { id: 'subagent-04', msg: 'Test Synth: Generated test fixture for user controller.' },
      { id: 'master', msg: 'Master Orchestrator: Verified subagent health heartbeats.' }
    ];
    const pick = msgs[Math.floor(Math.random() * msgs.length)];
    addLocalLog('AGENT_MSG', pick.id, pick.msg);
  }
}

function addLocalLog(level, agentId, message) {
  logEntries.unshift({
    timestamp: new Date().toLocaleTimeString(),
    level,
    agentId,
    message
  });
  if (logEntries.length > 80) logEntries.pop();
}

// Update Top Metrics Strip
function updateMetrics() {
  document.getElementById('metric-agents-count').innerText = `${subagentData.length} Worker Nodes`;
  
  const totalCpu = subagentData.reduce((acc, a) => acc + parseInt(a.cpu || 0), 0);
  const avgCpu = Math.round(totalCpu / (subagentData.length || 1));
  document.getElementById('metric-cpu').innerText = `${avgCpu}%`;

  const throughput = (1.2 + Math.random() * 0.4).toFixed(2);
  document.getElementById('metric-throughput').innerText = `${throughput}k tok/s`;
}

// Render Topology Graph Nodes
function renderTopology() {
  const container = document.getElementById('subagents-topology-nodes');
  container.innerHTML = subagentData.map(agent => `
    <div class="topo-node">
      <i class="fa-solid ${getAgentIcon(agent.type)}"></i>
      <h4>${agent.name}</h4>
      <span>${agent.status} (${agent.progress}%)</span>
    </div>
  `).join('');
}

function getAgentIcon(type) {
  switch (type) {
    case 'code_auditor': return 'fa-code';
    case 'sec_audit': return 'fa-shield-halved';
    case 'perf_profiler': return 'fa-gauge-high';
    case 'test_synth': return 'fa-vial';
    default: return 'fa-robot';
  }
}

// Render Subagent Cards
function renderSubagentCards() {
  const container = document.getElementById('subagent-cards-container');
  
  const filtered = subagentData.filter(agent => {
    if (currentSubagentFilter === 'ALL') return true;
    return agent.status === currentSubagentFilter;
  });

  container.innerHTML = filtered.map(agent => `
    <div class="subagent-card">
      <div class="subagent-header">
        <div class="subagent-title">
          <h3><i class="fa-solid ${getAgentIcon(agent.type)}"></i> ${agent.name}</h3>
          <span class="subagent-id">${agent.id} &bull; ${agent.model}</span>
        </div>
        <span class="badge-status badge-${agent.status.toLowerCase()}">${agent.status}</span>
      </div>

      <div class="task-box">
        <label>Current Subagent Task Focus</label>
        <p title="${agent.task}">${agent.task}</p>
      </div>

      <div class="progress-container">
        <div class="progress-info">
          <span>Task Execution Progress</span>
          <span>${agent.progress}%</span>
        </div>
        <div class="progress-bar-bg">
          <div class="progress-bar-fill" style="width: ${agent.progress}%"></div>
        </div>
      </div>

      <div class="subagent-footer">
        <span><i class="fa-solid fa-microchip"></i> ${agent.cpu}</span>
        <span><i class="fa-solid fa-memory"></i> ${agent.memory}</span>
        <span><i class="fa-solid fa-list-check"></i> ${agent.logs_count} Events</span>
      </div>
    </div>
  `).join('');
}

function filterSubagents(status) {
  currentSubagentFilter = status;
  const pills = document.querySelectorAll('.subagents-card .pill');
  pills.forEach(p => p.classList.remove('active'));
  event.target.classList.add('active');
  renderSubagentCards();
}

// Terminal Log Rendering
function renderLogs() {
  const container = document.getElementById('terminal-logs');
  const query = document.getElementById('log-search').value.toLowerCase();

  const filtered = logEntries.filter(log => {
    if (currentLogFilter !== 'ALL' && log.level !== currentLogFilter) return false;
    if (query && !log.message.toLowerCase().includes(query) && !log.agentId.toLowerCase().includes(query)) return false;
    return true;
  });

  container.innerHTML = filtered.map(log => `
    <div class="log-line">
      <span class="log-time">[${log.timestamp}]</span>
      <span class="log-agent">&lt;${log.agentId}&gt;</span>
      <span class="log-lvl-${log.level}">${log.message}</span>
    </div>
  `).join('');
}

function setLogFilter(level) {
  currentLogFilter = level;
  const btns = document.querySelectorAll('.terminal-controls .pill-btn');
  btns.forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  renderLogs();
}

function clearLogs() {
  logEntries = [];
  renderLogs();
}

// Resource Telemetry Chart (Chart.js)
function initChart() {
  const ctx = document.getElementById('resourceChart').getContext('2d');
  
  const labels = Array.from({length: 10}, (_, i) => `${(10-i)*2.5}s ago`);
  
  resourceChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Cluster Avg CPU %',
          data: [12, 18, 15, 22, 19, 25, 21, 18, 20, 18],
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          fill: true,
          tension: 0.4
        },
        {
          label: 'Active Subagent Memory (x10 MB)',
          data: [14, 15, 14, 16, 17, 18, 17, 16, 17, 18],
          borderColor: '#8b5cf6',
          backgroundColor: 'rgba(139, 92, 246, 0.1)',
          fill: true,
          tension: 0.4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#64748b' } },
        y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#64748b' } }
      },
      plugins: {
        legend: { labels: { color: '#94a3b8', font: { family: 'Inter' } } }
      }
    }
  });
}

function updateChartData() {
  if (!resourceChart) return;
  
  const totalCpu = subagentData.reduce((acc, a) => acc + parseInt(a.cpu || 0), 0);
  const avgCpu = Math.round(totalCpu / (subagentData.length || 1));
  
  resourceChart.data.datasets[0].data.shift();
  resourceChart.data.datasets[0].data.push(avgCpu);

  resourceChart.data.datasets[1].data.shift();
  resourceChart.data.datasets[1].data.push(Math.floor(14 + Math.random() * 5));

  resourceChart.update();
}

// Modal & Workload Controls
function openDispatchModal() {
  document.getElementById('dispatch-modal').classList.add('active');
}

function closeDispatchModal() {
  document.getElementById('dispatch-modal').classList.remove('active');
}

async function submitDispatchSubagent() {
  const name = document.getElementById('agent-name-input').value || 'Dynamic Subagent Worker';
  const role = document.getElementById('agent-role-input').value || 'Custom Task Execution';
  const task = document.getElementById('agent-task-input').value || 'Executing custom user-defined subagent workflow.';

  try {
    const res = await fetch('http://localhost:3456/api/dispatch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, role, task })
    });
    if (res.ok) {
      fetchTelemetry();
    } else {
      dispatchLocalSubagent(name, role, task);
    }
  } catch (e) {
    dispatchLocalSubagent(name, role, task);
  }

  closeDispatchModal();
}

function dispatchLocalSubagent(name, role, task) {
  const newId = `subagent-0${subagentData.length + 1}`;
  subagentData.push({
    id: newId,
    name: name,
    type: "custom_worker",
    role: role,
    model: "Gemini 3.6 Flash",
    status: "RUNNING",
    progress: 15,
    task: task,
    cpu: "16%",
    memory: "135 MB",
    logs_count: 1
  });
  addLocalLog('INFO', 'master', `Launched dynamic subagent: ${name} [${newId}]`);
  renderTopology();
  renderSubagentCards();
}

function triggerWorkload() {
  subagentData.forEach(agent => {
    agent.status = 'RUNNING';
    agent.progress = 20;
    agent.cpu = (Math.floor(Math.random() * 20) + 30) + '%';
  });
  addLocalLog('WARN', 'master', 'Heavy Audit Workload dispatched to all subagent nodes.');
  renderSubagentCards();
}

function exportTelemetry() {
  const report = {
    exportTime: new Date().toISOString(),
    system: "Antigravity Multi-Agent Cluster 2.0",
    subagents: subagentData,
    logs: logEntries
  };
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(report, null, 2));
  const downloadAnchor = document.createElement('a');
  downloadAnchor.setAttribute("href", dataStr);
  downloadAnchor.setAttribute("download", `subagent_telemetry_${Date.now()}.json`);
  document.body.appendChild(downloadAnchor);
  downloadAnchor.click();
  downloadAnchor.remove();
}
