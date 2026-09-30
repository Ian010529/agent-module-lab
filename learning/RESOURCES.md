# AI Module Engineering Resources

## Knowledge

### Project source — default first choice for the current slice

- [Project reference: `reference/agents-from-scratch`](https://github.com/Ian010529/agent-module-lab/tree/main/reference/agents-from-scratch)

Pinned in this repository at commit `603fc7a4ac6119004f43894395e504a1fefcc6c0`. Use first for: learning how the reference system actually implements structured output, routing, state transitions, and evaluation.

- [Pinned source: `src/email_assistant/schemas.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/schemas.py)

This is the exact file behind the repository submodule. Use for: `RouterSchema`, `Literal`, and the separation between one LLM call's output schema and workflow state.

- [Pinned source: `src/email_assistant/email_assistant.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/email_assistant.py)

This is the exact file behind the repository submodule. Use for: `with_structured_output(RouterSchema)`, `result.classification`, and deterministic routing after the model decision.

- [Pinned source: `src/email_assistant/eval/evaluate_triage.py`](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/eval/evaluate_triage.py)

This is the exact file behind the repository submodule. Use for: seeing why schema-valid output can still fail task evaluation.

### Official documentation — use to verify contracts and semantics

- [LangChain Reference: `BaseChatModel.with_structured_output`](https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel/with_structured_output)

Primary API reference for the wrapper used by the pinned source. Use for: what the API accepts, how the schema is supplied, and what kind of object is returned.

- [OpenAI Guide: Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

Primary provider documentation on schema adherence and its limits. Use for: verifying that structure conformance does not imply semantic correctness.

- [Pydantic Documentation: Validators](https://docs.pydantic.dev/latest/concepts/validators/)

Primary validation documentation. Use only when the project schema creates a real need for field/model-level constraints such as exact-vs-range pricing.

## Wisdom (Communities)

- [LangChain Forum](https://forum.langchain.com/)

Official community support venue. Use for: runtime behaviour, provider quirks, or cases where documentation and observed implementation behaviour diverge.

## Gaps

- Provider-specific structured-output differences are intentionally not researched yet because the current slice has not selected a final model/provider.
- Advanced Pydantic features are intentionally not researched until the Creator Reply schema demonstrates a real need for them.
