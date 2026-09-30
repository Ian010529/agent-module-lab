# Current Progress

## Current project

Creator Outreach / Reply Copilot

## Current phase

第一段实际 Slice 已完成当前 teach learning gate，进入 Own Design。

当前正在学习：

**Structured Output + Schema Validation → Creator Reply Extraction**

teach 学习工作区已经建立在 `learning/`；当前 lesson 为：

`learning/lessons/0001-schema-is-a-contract.html`

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
- Structured Output / Schema Validation 已进入正式学习：
  - 已讨论 structured output、schema、Literal、可空字段、nested model；
  - 已讨论 missing / ambiguous / false precision；
  - 已区分 semantic extraction 与 deterministic validation；
  - 已读取 reference 中 RouterSchema → with_structured_output → classification → deterministic routing → eval 的主链。
- 已建立单仓库 teach 工作区，并创建当前 lesson、reference cheat sheet 和进行中的 learning record。

## Current technical focus

完整状态见 `docs/technical-map.md`。

当前技术单元：

**Structured Output + Schema Validation**

当前状态：

**UNDERSTANDING，Lesson 0001 gate passed；尚未 PRACTICED**

项目落点：

**Creator Reply → structured extraction**

## Next step

当前 Slice 按 `docs/workspace-guide.md` 执行：

1. **Own Design**：根据 Creator Reply 的真实需求定义 extraction 输入、输出 schema 与 failure handling，不复制 RouterSchema。
2. **建立测试案例**：正常、缺字段、模糊报价、多个报价条件、格式异常等固定案例。
3. **Implementation**：使用 vibe coding 完成 Reply Extraction slice。
4. **Verification**：运行正常与 failure cases，区分 schema validity 与 extraction correctness。
5. 完成理解检查后，再判断 Structured Output / Schema Validation 是否可更新为 `PRACTICED`，并进入下一 Slice。

## Not decided yet

以下内容仍未做最终技术选择：

- 是否使用 LangGraph 作为最终编排框架
- 是否需要持久化 workflow state
- HITL 在本项目中的具体持久化实现
- 是否需要长期 Memory
- 是否需要 RAG
- 具体模型与模型提供商
- 是否需要动态 Tool Registry / Tool Retrieval

这些内容都必须由实际需求触发，不能因为参考仓库使用或技术上“可以做”就提前引入，也不提前为其创建 lesson。
