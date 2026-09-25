# Current Progress

## Current project

Creator Outreach / Reply Copilot

## Current phase

参考源码执行链梳理。

## Completed

- 已确定项目目标与开发边界，见 `docs/project-scope.md`。
- 已将 `langchain-ai/agents-from-scratch` 作为第一阶段参考项目。
- 参考项目以 Git submodule 形式固定在 `reference/agents-from-scratch`。
- 当前固定版本：`603fc7a4ac6119004f43894395e504a1fefcc6c0`。
- 已追踪 HITL 版本的完整主链：输入 → triage → response agent → tool decision → HITL / direct tool execution → resume → completion。
- 已确认状态由 `email_input`、`classification_decision` 和消息历史构成；HITL 的暂停/恢复依赖 checkpointer 与 thread id。
- 已确认原仓库自动化评测覆盖 triage、tool calling 和 response quality，但现有测试脚本没有完整覆盖 HITL 版本。

## Current focus

把参考实现映射到 Creator Outreach / Reply Copilot，区分：

- 哪些步骤应该保留为固定 workflow
- 哪些步骤需要 LLM 判断
- 哪些能力应该暴露为 tools
- 哪些动作必须进入 HITL
- 哪些参考实现不应该照搬

## Next step

用一个具体达人回复案例设计第一版执行链，再据此确定我们自己的 workflow / agent / tool / HITL 边界。设计确认后才开始写 `src/`。

## Not decided yet

以下内容尚未做技术选择，不应预设：

- 是否直接使用 LangGraph 作为最终编排框架
- 是否需要持久化状态
- HITL 的具体实现方式
- 是否需要 Memory
- 是否需要 RAG
- 具体模型与模型提供商
