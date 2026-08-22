# NEXUS — AI-Native Business Intelligence & Autonomous Operations Platform

NEXUS is a multi-agent AI system that investigates business questions the way a
human analyst team would — by routing the question to domain-specific agents
(Finance, Sales, Marketing, ...), having each agent pull real numbers using real
tools against real data, and then synthesizing their findings into one grounded,
evidence-backed answer.

> Example: ask "Our sales conversion dropped this month — did that affect our
> revenue growth too?" and NEXUS calls both the Sales and Finance agents,
> then explains how the two findings connect.

## Why this exists

Most "AI dashboards" just let an LLM guess numbers from a prompt. NEXUS is built
around one non-negotiable rule: **the LLM never does the math.** Every number
comes from a deterministic tool call against real data. The LLM's job is to
decide *what* to investigate and *explain* the result — not to invent it.

## Status

🟢 **V1 (in progress)**

- [x] Finance tools (`calculate_growth_rate`) — tested
- [x] Sales tools (`calculate_conversion_rate`, `compare_conversion_rates`) — tested
- [x] Finance Agent — LLM + tool calling via Groq
- [x] Sales Agent — LLM + multi-tool chaining via Groq
- [x] Orchestrator — routes questions to one or more agents, synthesizes combined answers
- [ ] Real database (Postgres) — currently using hardcoded context data
- [ ] FastAPI backend routes
- [ ] React frontend
- [ ] Deployment

## Architecture (current)

Each agent is: an LLM (via Groq) + a specific job + access to specific tools.
Tools are plain, deterministic Python functions — no AI involved, fully unit
tested. The LLM decides *when* to call a tool and *how* to explain the result;
it never calculates anything itself.

The Orchestrator reads the user's question, decides which agent(s) are
relevant (it can call more than one), collects their findings, and synthesizes
one combined answer.

## Tech stack

- **Backend:** Python, FastAPI (coming), SQLAlchemy (coming), Postgres (coming)
- **AI:** Groq (Llama-based models via tool calling / structured outputs)
- **Frontend:** React + TypeScript, Tailwind (coming)
- **Infra (later):** Docker, GitHub Actions

## Project structure

- `backend/app/agents/` — Finance Agent, Sales Agent (LLM + tool calling logic)
- `backend/app/tools/` — Deterministic functions agents call (math, DB queries)
- `backend/app/orchestrator/` — Routes questions to agent(s), synthesizes combined results
- `backend/app/models/` — Pydantic schemas + DB table definitions (coming)
- `backend/app/db/` — DB connection + seed data scripts (coming)
- `backend/app/api/` — FastAPI routes (coming)
- `backend/app/core/` — config, settings (Groq API key handling)
- `frontend/` — React app (coming)
- `docs/` — architecture notes, roadmap, decisions log

## Running locally

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install groq python-dotenv pytest
```

Create a `.env` file in `backend/` with:

```
GROQ_API_KEY=your_key_here
```

Run tests:

```bash
pytest
```

Run a manual agent/orchestrator test:

```bash
python -m app.agents.manual_test
```

## Roadmap

- [x] V1 core — tools, agents, orchestrator (multi-agent loop proven working)
- [ ] V1 remaining — real database, FastAPI, frontend, deployment
- [ ] V2 — RAG for documents, ML forecasting, churn prediction, agent permissions
- [ ] V3 — Human approval layer, audit logs, observability, evaluation framework, CI/CD
