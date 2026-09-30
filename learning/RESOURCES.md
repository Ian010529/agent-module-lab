# Learning Resources

## Project source of truth

学习前先以项目文件恢复边界：

- `docs/project-scope.md` — 项目目标与边界
- `docs/progress.md` — 当前 Slice 与下一步
- `docs/technical-map.md` — 技术掌握状态
- `docs/workspace-guide.md` — 工作与学习推进协议
- `docs/references.md` — pinned reference 版本

## Current lesson

### Structured Output + Schema Validation

项目落点：

**Creator Reply → structured extraction**

当前 reference：

`reference/agents-from-scratch`

Pinned commit：

`603fc7a4ac6119004f43894395e504a1fefcc6c0`

当前需要阅读的源码：

- `src/email_assistant/schemas.py`
  - `RouterSchema`
  - `StateInput`
  - `State`
- `src/email_assistant/email_assistant.py`
  - `llm.with_structured_output(RouterSchema)`
  - `triage_router()`
  - `result.classification`
  - deterministic routing
- `src/email_assistant/prompts.py`
  - triage classification semantics
- `src/email_assistant/eval/evaluate_triage.py`
  - classification exact-match evaluation

## Scope boundary for this lesson

需要掌握：

- structured output 与普通 prompt JSON 的区别
- schema 作为数据契约
- Pydantic `BaseModel`
- `Literal`、可空字段、nested model
- missing vs ambiguous
- raw vs normalized value
- schema/type validation
- cross-field validation 的概念
- semantic correctness 与 schema validity 的区别
- deterministic validation 与 LLM semantic extraction 的边界
- reference 中 structured output 的真实执行链

当前不展开：

- Pydantic 高级 API 全集
- JSON Schema 标准细节
- provider-specific structured output 差异
- RAG
- Memory
- MCP
- Multi-Agent
- dynamic Tool Registry
- Redis / Queue
