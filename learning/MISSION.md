# Mission: Independently own an AI efficiency module

## Why

Use the Creator Outreach / Reply Copilot as a real project to become capable of independently owning an AI efficiency module: define the problem, choose the architecture, review AI-generated code, implement the critical path, test it, and diagnose failures.

## Success looks like

- Explain the module's execution path and major design tradeoffs without relying on a prepared answer.
- Design each project slice from business requirements before asking AI to implement it.
- Review and modify AI-generated critical code instead of treating generated code as authoritative.
- Build reproducible tests and evals that distinguish formatting, semantic, business-rule, and runtime failures.
- Decide when a simpler deterministic solution is better than adding Agent, RAG, Memory, Multi-Agent, MCP, or infrastructure.

## Constraints

- Learning is project-driven and just-in-time: only learn what the current slice requires.
- Keep the teaching workspace inside this repository under `learning/`; no separate learning repo and no local clone is required for reading lessons.
- Use vibe coding for implementation speed, but retain ownership of architecture, failure handling, and verification.
- Lessons should be short, interactive, browser-readable, and based on trusted primary sources.

## Out of scope

- Building a complete general-purpose Agent curriculum before the project needs it.
- Learning RAG, Memory, Multi-Agent, MCP, dynamic Tool Registry, Redis, queues, or other infrastructure only because they are popular.
- Rebuilding a CRM, campaign platform, mailbox client, data warehouse, or benchmark platform.
