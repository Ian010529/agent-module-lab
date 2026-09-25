# Current Progress

## Current project

Creator Outreach / Reply Copilot

## Current phase

项目初始化与参考源码准备。

## Completed

- 已确定项目目标与开发边界，见 `docs/project-scope.md`。
- 已将 `langchain-ai/agents-from-scratch` 作为第一阶段参考项目。
- 参考项目以 Git submodule 形式固定在 `reference/agents-from-scratch`。
- 当前固定版本：`603fc7a4ac6119004f43894395e504a1fefcc6c0`。

## Current focus

先理解参考项目中一条完整的执行链，包括：

- 输入如何进入系统
- triage / workflow 如何分流
- Agent 如何调用工具
- state 如何变化
- human-in-the-loop 如何暂停和恢复
- evaluation 如何验证行为

## Next step

从 `reference/agents-from-scratch` 的真实源码出发，追踪一条完整请求链，确定哪些设计可以用于 Creator Outreach / Reply Copilot，哪些不需要保留。

## Not decided yet

以下内容尚未做技术选择，不应预设：

- 是否直接使用 LangGraph 作为最终编排框架
- 是否需要持久化状态
- HITL 的具体实现方式
- 是否需要 Memory
- 是否需要 RAG
- 具体模型与模型提供商
