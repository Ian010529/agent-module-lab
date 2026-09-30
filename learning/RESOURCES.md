# AI Module Engineering Resources

## Knowledge

- [LangChain Reference: `BaseChatModel.with_structured_output`](https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel/with_structured_output)

Primary API reference for the exact wrapper used by the pinned `agents-from-scratch` implementation. Use for: what the wrapper accepts and what it returns.

- [OpenAI Guide: Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

Primary provider documentation explaining schema adherence, the difference from JSON mode, and the important limitation that schema-conforming outputs can still contain semantic mistakes. Use for: separating output-shape guarantees from task correctness.

- [Pydantic Documentation: Validators](https://docs.pydantic.dev/latest/concepts/validators/)

Primary Pydantic documentation for field and model validators. Use for: cross-field constraints once the Creator Reply schema needs relationships such as exact-vs-range pricing.

- [Project reference: `agents-from-scratch` pinned commit](https://github.com/langchain-ai/agents-from-scratch/tree/603fc7a4ac6119004f43894395e504a1fefcc6c0)

The exact code version pinned in this repository. Use for: tracing `RouterSchema → with_structured_output → classification → deterministic routing → eval` without drifting to newer implementations.

- [Project file: RouterSchema](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/schemas.py)

Primary source for the reference schema used in the current lesson. Use for: seeing how a finite classification space is represented with Pydantic and `Literal`.

- [Project file: email assistant routing](https://github.com/langchain-ai/agents-from-scratch/blob/603fc7a4ac6119004f43894395e504a1fefcc6c0/src/email_assistant/email_assistant.py)

Primary source for the reference execution path. Use for: locating `with_structured_output`, reading `result.classification`, and seeing deterministic routing after the LLM decision.

## Wisdom (Communities)

- [LangChain Forum](https://forum.langchain.com/)

Official community support venue referenced by LangChain's own issue templates. Use for: implementation-specific behaviour, provider quirks, or cases where documentation and actual runtime behaviour diverge.

## Gaps

- Provider-specific structured-output differences are intentionally not researched yet because the current slice has not selected a final model/provider.
- Advanced Pydantic features are intentionally not researched until the Creator Reply schema demonstrates a real need for them.
