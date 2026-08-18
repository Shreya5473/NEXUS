# NEXUS — AI-Native Business Intelligence & Autonomous Operations Platform

NEXUS is a multi-agent AI system that investigates business questions the way a
human analyst team would — by routing the question to domain-specific agents
(Finance, Sales, Marketing, ...), having each agent pull real numbers using real
tools against real data, and then synthesizing their findings into one grounded,
evidence-backed answer.

> Example: ask "Why did revenue drop this month?" and NEXUS investigates across
> Finance, Sales, and Marketing data, then explains the *why* — with evidence.

## Why this exists

Most "AI dashboards" just let an LLM guess numbers from a prompt. NEXUS is built
around one non-negotiable rule: **the LLM never does the math.** Every number
comes from a deterministic tool call against real data. The LLM's job is to
decide *what* to investigate and *explain* the result — not to invent it.

## Status

🟢 **V1 (in progress)** — MVP: Finance + Sales + Marketing agents, simple
orchestrator, seeded Postgres data, minimal frontend.

