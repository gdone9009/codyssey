# 🚀 Codyssey Task Orchestrator Dashboard

구글 드라이브(`AI올인원_AISW기본_미션목록`) 및 로컬 워크스페이스 내 10개 코디세이(Codyssey) 미션과제를 개별 대화 맥락(Subagent Context)에서 오케스트레이션하기 위한 중앙 상태 대시보드입니다.

---

## 📊 Mission Task Registry & Real-Time Status

| ID | Mission Directory | Full Mission Title | Stack / Topic | Status | Conversation ID | Commit | Test |
|---|---|---|---|---|---|---|---|
| 01 | [Prompt-Engineering](./Prompt-Engineering) | 🚀 LLM Prompt Engineering & Automation Package | LLM, Prompting | 🟢 Pending | - | bed4912 | N/A |
| 02 | [cli-docker-git](./cli-docker-git) | 💻 AI/SW 개발 워크스테이션 구축 프로젝트 | Shell, Docker, Git | 🟢 Pending | - | 299d567 | N/A |
| 03 | [cloud-infra-aws](./cloud-infra-aws) | 🛡️ VPC 사설 격리 네트워크 기반 인프라 구축 | AWS, Cloud Infra | ❇️ Completed | - | 102be9d | Passed |
| 04 | [linux-system-monitor](./linux-system-monitor) | 🛡️ 시스템 관제 자동화 및 보안 구축 프로젝트 | C, Linux Sys, Shell | ❇️ Completed | 52b943ac-f000 | 47b4772 | Passed |
| 05 | [mini-npu-simulator](./mini-npu-simulator) | 🧠 Mini NPU Simulator v1.5 | Python, AI NPU | ❇️ Completed | 52b943ac-f000 | 8967ebd | Passed |
| 06 | [mini-redis](./mini-redis) | 🛡️ 순수 자료구조 기반 인메모리 Key-Value 저장소 | C/Python, Networking | ❇️ Completed | dda1a018-5436 | d0930e3 | 22/22 Passed |
| 07 | [python-budget-app](./python-budget-app) | 💰 파일 기반 가계부 콘솔 프로그램 | Python, OOP, Test | ❇️ Completed | 52b943ac-f000 | 7c08987 | Passed |
| 08 | [python-quiz-game](./python-quiz-game) | 🎯 CLI 퀴즈 게임 프로그램 | Python, JSON, CLI | ❇️ Completed | 52b943ac-f000 | 845bf6d | Passed |
| 09 | [sql-db](./sql-db) | 📊 도서 관리 시스템 SQL 데이터베이스 구축 | SQLite, SQL Query | ❇️ Completed | 0d4021e9-92f8 | 0df8c76 | Passed |
| 10 | [vanilla-js-portfolio](./vanilla-js-portfolio) | 🛡️ 단방향 상태 관리 기반 반응형 포트폴리오 | JS, HTML/CSS Web | ❇️ Completed | - | ef053c0 | Passed |

---

## 🔄 Status Legend

- 🟢 **Pending**: 과제 수행 대기 중
- 🟡 **In Progress**: 전담 서브에이전트(`codyssey_task_executor`) 대화 수행 중
- 🔵 **Verification Pending**: 구현 완료 후 매니저 검증 및 QA 진행 중
- ❇️ **Completed**: 유닛 테스트 통과 및 매니저 최종 승인 완료
- 🔴 **Failed / Error**: 구현 또는 테스트 실패, 수정 조치 필요
