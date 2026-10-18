# AI Tech Consultant (JD4 Capstone)

An integrated, three-tier agentic system that automates repetitive technical consulting workflows for software and service companies. By connecting product documentation, email support, and client meeting scoping into a shared intelligence loop, the system accelerates consultant output by 10x to 20x.

---

## Architecture at a Glance

The application consists of three connected tasks sharing a single knowledge brain:

1. **Task 1: The Knowledge Brain (`task1-knowledge-brain/`)** [Python]
   - Polite, resumable crawler over Brilliant Directories Solution Center sitemap (1,696 pages).
   - Multimodal screenshot understanding extracting UI controls, toggles, and buttons.
   - Hybrid vector retrieval (Dense 384-dim embeddings + BM25 lexical scoring + Reranker).
   - Grounded RAG with source citations, honest abstention, and human escalation feedback loop.
   - REST API: `POST /query`, `POST /ingestion/run`, `POST /escalations/{id}/resolve`, `GET /health`.

2. **Task 2: The Autonomous Inbox Agent (`task2-inbox-agent/`)** [TypeScript — Strict Mode]
   - Consumes Task 1 API over HTTP; never duplicates knowledge code.
   - 7-intent classification with calibrated urgency and commercial risk assessment.
   - Tested on 52 realistic customer support emails covering all edge cases and risks.
   - Enforces the 20-consecutive-approval rule: unlocks autonomous sending upon 20 unmodified sends.
   - Automatic downgrade safety guardrail: instant revocation upon human edit or complaint.

3. **Task 3: Meeting to Scope Studio (`task3-meeting-to-scope/`)** [Python]
   - 5-agent team: Transcript Analyst, Product Feasibility Agent (queries Task 1), Scope Agent, Estimation Agent, Proposal & Review Agent.
   - Tested across 3 realistic role-play transcripts (Meeting A, Meeting B, Meeting C).
   - Scope Diff Engine: Compares Meeting C follow-up against approved baseline, identifying added (+11 hrs), modified (+2 hrs), removed (-3 hrs), and out-of-scope requests (+10.0 hrs net delta = +$1,200).
   - Strict human approval barrier before proposal dispatch.

4. **Executive Command Center Dashboard (`frontend-dashboard/`)**
   - Cyber-modern HUD with animated particle canvas, section transitions, live telemetry, and interactive controls.

---

## Prerequisites

- **Python**: 3.10+ (tested on Python 3.13)
- **Node.js**: v18+ (tested on Node.js v22.15.1)
- **Git**

---

## One-Command Startup

Start all three microservices and the interactive dashboard with a single command:

```bash
# Option A: Python Master Runner
python run_all.py

# Option B: PowerShell
./start.ps1
```

### Live Service Endpoints

| Service | Port | URL | Description |
|---|---|---|---|
| **Executive Dashboard** | `8000` | [http://localhost:8000](http://localhost:8000) | Animated Web Command Center |
| **Task 1: Knowledge Brain** | `8001` | [http://localhost:8001/docs](http://localhost:8001/docs) | Swagger API & RAG Query Service |
| **Task 2: Inbox Agent** | `8002` | [http://localhost:8002/health](http://localhost:8002/health) | TypeScript Express Server |
| **Task 3: Meeting-to-Scope** | `8003` | [http://localhost:8003/docs](http://localhost:8003/docs) | Multi-Agent Scoping Service |

---

## Running the Automated Test Suites (66 Evals Total)

Every task includes 22 automated evaluation benchmarks:

```bash
# 1. Run Task 1 Evaluations (Python — 22 cases)
cd task1-knowledge-brain
python -m evaluation.run_evals

# 2. Run Task 2 Evaluations (TypeScript — 22 cases)
cd ../task2-inbox-agent
npm test

# 3. Run Task 3 Evaluations (Python — 22 cases)
cd ../task3-meeting-to-scope
python -m evaluation.run_evals
```
