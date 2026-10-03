# AI Module Engineering Resources

## Current Slice 2 — Campaign Context + Policy Gate

### Project source — default first choice

- [Project reference: `reference/agents-from-scratch`](https://github.com/Ian010529/agent-module-lab/tree/main/reference/agents-from-scratch)

Pinned in this repository at commit `603fc7a4ac6119004f43894395e504a1fefcc6c0`. For Slice 2, use it to study the boundary between deterministic workflow control and model-selected tools. Do not copy its tool loop mechanically.

- [Pinned source: `src/email_assistant/tools/base.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/tools/base.py)

Use for: seeing that the application code chooses which tools are available before the model sees them.

- [Pinned source: `src/email_assistant/email_assistant_hitl.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/email_assistant_hitl.py)

Use for: `bind_tools`, model-generated `tool_calls`, direct execution of selected tools, and the fact that only some tool calls need HITL.

- [Pinned source: `src/email_assistant/email_assistant.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/email_assistant.py)

Use for: deterministic `if / elif` routing after a model decision is already known.

### Official documentation — verify the tool-calling contract

- [LangChain Reference: `BaseChatOpenAI.bind_tools`](https://reference.langchain.com/python/langchain-openai/chat_models/base/BaseChatOpenAI/bind_tools)

Primary API reference for how tool definitions are bound to a chat model and how `tool_choice` constrains model selection.

- [OpenAI Guide: Function calling](https://developers.openai.com/api/docs/guides/function-calling)

Primary provider documentation for the model/tool interaction: tools expose application functionality to the model; the model can decide when and which tool to call unless the application constrains that choice.

## Previous Slice 1 — Structured Output + Schema Validation

- [Pinned source: `src/email_assistant/schemas.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/schemas.py)
- [Pinned source: `src/email_assistant/email_assistant.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/email_assistant.py)
- [Pinned source: `src/email_assistant/eval/evaluate_triage.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/eval/evaluate_triage.py)
- [LangChain Reference: `BaseChatModel.with_structured_output`](https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel/with_structured_output)
- [OpenAI Guide: Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Pydantic Documentation: Validators](https://docs.pydantic.dev/latest/concepts/validators/)

## Wisdom (Communities)

- [LangChain Forum](https://forum.langchain.com/)

Use only when primary documentation and pinned source do not explain an observed runtime behaviour.

## Gaps

- Slice 2 has not selected a real Campaign API/database; the first implementation should therefore use a thin lookup interface and deterministic fake/in-memory data in tests rather than inventing infrastructure.
- RAG, dynamic Tool Registry, MCP, Memory, Redis and queues remain intentionally out of scope until a concrete requirement appears.
