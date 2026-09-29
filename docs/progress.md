# Current Progress

## Current project

Creator Outreach / Reply Copilot

## Current phase

参考源码执行链已梳理，准备从架构边界进入第一段实际实现。

## Completed

- 已确定项目目标与开发边界，见 `docs/project-scope.md`。
- 已将 4 个外部项目以 pinned Git submodule 形式加入 `reference/`，具体版本见 `docs/references.md`。
- 已追踪 `agents-from-scratch` HITL 版本的完整主链：输入 → triage → response agent → tool decision → HITL / direct tool execution → resume → completion。
- 已确认参考实现的 State 由业务输入、classification decision 与消息轨迹组成。
- 已确认 HITL 暂停/恢复依赖 checkpoint 与 execution identity（thread id）。
- 已确认参考仓库自动化评测覆盖 triage、tool calling 和 response quality，但现有测试并没有完整覆盖 HITL 版本。
- 已通过达人报价案例初步形成设计边界：
  - 语义理解 / 报价提取适合 LLM；
  - 确定性金额比较适合 CODE；
  - 已知 campaign policy 优先通过现有业务接口获取；
  - 只取得当前 decision 需要的最少上下文；
  - 商务判断与对外执行审批可以是不同的 HITL；
  - 已知下一步必须调用哪个接口时，不需要为了 Agent 化而让模型选择 Tool。

## Current technical focus

技术学习与项目实现并行，完整状态见 `docs/technical-map.md`。

下一正式技术单元：

**Structured Output + Schema Validation**

项目落点：

**Creator Reply → structured extraction**

## Next step

1. 读取 `agents-from-scratch` 中与 structured output / schema 有关的真实实现。
2. 定义第一版 Creator Reply extraction 的输入与输出 schema。
3. 建立最小固定测试案例。
4. 实现 extraction slice。
5. 用正常与失败案例验证，再决定下一 slice。

## Not decided yet

以下内容仍未做最终技术选择：

- 是否使用 LangGraph 作为最终编排框架
- 是否需要持久化 workflow state
- HITL 在本项目中的具体持久化实现
- 是否需要长期 Memory
- 是否需要 RAG
- 具体模型与模型提供商
- 是否需要动态 Tool Registry / Tool Retrieval

这些内容都必须由实际需求触发，不能因为参考仓库使用或技术上“可以做”就提前引入。
