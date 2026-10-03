# AI Module Engineering Resources

## Current Slice 2 — Campaign Context + Policy Gate

### Project source — default first choice

- [Project reference: `reference/agents-from-scratch`](https://github.com/Ian010529/agent-module-lab/tree/main/reference/agents-from-scratch)

Pinned at commit `603fc7a4ac6119004f43894395e504a1fefcc6c0`. Slice 2 stays inside this reference. The purpose is to trace the real Tool Calling mechanics and deterministic workflow boundary before designing our own Campaign Context flow.

- [Pinned source: `src/email_assistant/tools/default/email_tools.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/tools/default/email_tools.py)

Use for: `@tool` on functions and Pydantic classes; tool name, docstring and argument shape.

- [Pinned source: `src/email_assistant/tools/default/calendar_tools.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/tools/default/calendar_tools.py)

Use for: another concrete function-tool example with typed arguments.

- [Pinned source: `src/email_assistant/tools/base.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/tools/base.py)

Use for: application-controlled Tool exposure via `get_tools(...)` and runtime dispatch map via `get_tools_by_name(...)`.

- [Pinned source: `src/email_assistant/email_assistant.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/email_assistant.py)

Use for: `bind_tools`, `AIMessage.tool_calls`, `name / args / id`, `tool.invoke(args)`, returning a `role="tool"` observation, the Agent loop, Done stop condition, and deterministic triage routing.

- [Pinned source: `src/email_assistant/email_assistant_hitl.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/email_assistant_hitl.py)

Use only for the current boundary: application can intercept a model-selected Tool before execution and decide whether to execute directly or route through HITL. Do not expand into HITL persistence in this Slice.

### Official documentation — verify contracts after reading the pinned code

- [LangChain Reference: `BaseChatOpenAI.bind_tools`](https://reference.langchain.com/python/langchain-openai/chat_models/base/BaseChatOpenAI/bind_tools)

Verify: accepted tool definitions, returned AIMessage runnable, and `tool_choice` semantics. `required` / `any` forces at least one tool call; `auto` permits the model to choose zero or more.

- [OpenAI Guide: Function calling](https://developers.openai.com/api/docs/guides/function-calling)

Verify: function calling exposes application functions/data to the model, while the application executes custom functions and returns their outputs to the model.

## Previous Slice 1 — Structured Output + Schema Validation

- [Pinned source: `src/email_assistant/schemas.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/schemas.py)
- [Pinned source: `src/email_assistant/email_assistant.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/email_assistant.py)
- [Pinned source: `src/email_assistant/eval/evaluate_triage.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/eval/evaluate_triage.py)
- [LangChain Reference: `BaseChatModel.with_structured_output`](https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel/with_structured_output)
- [OpenAI Guide: Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Pydantic Documentation: Validators](https://docs.pydantic.dev/latest/concepts/validators/)

## Reference staging

The repository's existing staging remains authoritative:

- `agents-from-scratch`: current Creator Outreach / Reply Copilot.
- `gpt-researcher`: later Creator / Competitor Research Copilot.
- `vanna`: later Campaign Performance Analyst.
- `tau2-bench`: evaluation reference, introduced when the project reaches the relevant eval work.

Do not pull a later reference into the current Slice merely because a filename or concept sounds similar.

## Gaps

- Slice 2 has not selected a real Campaign API/database. That decision is intentionally deferred to Own Design; learning only establishes the interface/control boundary needed to make that decision.
- RAG, Memory, MCP, dynamic Tool Registry, Multi-Agent, Redis and queues remain out of scope until a concrete project requirement appears.
