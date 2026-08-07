# Antigravity 2.0 Subagent Orchestrator & Live Monitoring Dashboard

이 프로젝트는 **Google Antigravity 2.0 Multi-Agent Orchestration Architecture**를 시연하고 실시간으로 관리 및 모니터링하기 위한 웹 대시보드 애플리케이션입니다.

---

## 🌟 주요 기능 (Key Features)

1. **Multi-Agent Topology Visualizer**:
   - Master Orchestrator (Parent Agent)와 각각의 서브에이전트(Subagents) 간의 실시간 통신 및 태스크 분발 구조를 시각화합니다.
2. **Subagent Pool Status Management**:
   - 코드 아키텍처 감사 에이전트, 보안 취약점 점검 에이전트, 성능 프로파일러 에이전트, 통합 테스트 생성 에이전트 등 복수의 전문화된 서브에이전트 상태(RUNNING, COMPLETED, IN_PROGRESS)와 CPU/메모리 사용량을 실시간 추적합니다.
3. **Live Activity & Event Stream (Terminal)**:
   - 각 서브에이전트가 처리하는 작업 로그, 메시지 교환, 경고 및 완료 이벤트를 색상별 및 태그별로 필터링하고 검색할 수 있는 터미널 스트림을 제공합니다.
4. **Real-time Telemetry Analytics**:
   - Chart.js 기반으로 클러스터의 토큰 처리 속도(Throughput), 평균 CPU 사용률, 각 서브에이전트 메모리 사용량을 가시화합니다.
5. **Interactive Dispatch & Controls**:
   - 새로운 서브에이전트를 동적으로 추가(Dispatch), 고부하 작업(Heavy Workload) 일괄 지시, 텔레메트리 보고서 JSON 추출(Export)을 지원합니다.

---

## 🚀 실행 방법 (Getting Started)

### Option 1: Node.js Orchestrator 백엔드 및 실시간 서버 실행
```bash
cd subagent-orchestrator-dashboard
npm start
```
* 서버 실행 후 웹 브라우저에서 `http://localhost:3456`으로 접속합니다.

### Option 2: 정적 웹 서버 실행
```bash
cd subagent-orchestrator-dashboard
npx serve -l 3000 .
```
* 또는 `index.html` 파일을 직접 웹 브라우저에서 열 수 있습니다. (자체 클라이언트 시뮬레이션 엔진 포함)

---

## 🛠 서브에이전트 구성 (Subagent Roles)

- `subagent-01` (**Code Auditor Agent**): 정적 코드 분석, AST 트어 스캐닝 및 리팩토링 제안
- `subagent-02` (**Security Audit Agent**): 보안점검, 환경변수 시크릿 유출 및 OWASP 취약점 스캔
- `subagent-03` (**Performance Profiler**): Event Loop 처리 시간 및 병목 구간 벤치마킹
- `subagent-04` (**Test Generator Agent**): 단위 테스트(Unit/Integration Test) 자동 생성
