# Current Progress

## Current project

Creator Outreach / Reply Copilot

## Current phase

**Slice 2 — Campaign Context + Policy Gate 已开始。**

当前步骤：

**Technical foundation + reference trace — Lesson 0002: Tool Calling execution chain + direct-control boundary**

Slice 1 — Creator Reply Extraction 已完成并收口。

Slice 2 的目标是把已经提取出的 Creator Reply 与已知 `campaign_id` 对应的业务规则连接起来，使用 direct lookup 获取最少必要 Campaign Context，再用 deterministic policy checks 判断是否在规则内、是否缺信息或是否需要人工处理。

## Completed

- 已确定项目目标与开发边界，见 `docs/project-scope.md`。
- 已将 4 个外部项目以 pinned Git submodule 形式加入 `reference/`，具体版本见 `docs/references.md`。
- 已追踪 `agents-from-scratch` HITL 版本的完整主链：输入 → triage → response agent → tool decision → HITL / direct tool execution → resume → completion。
- 已通过 Lesson 0001 retrieval gate，能够区分 semantic error、schema/type error 与 deterministic business-rule check。
- 已完成 Creator Reply Extraction 第一版业务边界设计：
  - 顶层只保留 `interest / quotes / delivery`；
  - Quote 分离 `quote_basis`、`amount_type` 与 `conditions`；
  - `quotes=None` 明确表示邮件没有报价信息；
  - currency 缺失保持 `None`，明确货币标准化为三字母代码；
  - approximate delivery 保留 `raw_text`，禁止制造假日期。
- 已完成第一版实现：
  - `src/creator_reply/schemas.py`：Pydantic schema 与 cross-field validation；
  - `src/creator_reply/extractor.py`：使用 `with_structured_output(CreatorReply)` 的薄适配层，不锁定具体模型提供商；
  - `tests/reply_extraction_cases.json`：7 个保留验收案例。
- 已在隔离环境运行 pytest：**15 passed**。
- 已完成真实模型验收。
- 实现过程中发现并修复了 `Delivery.date` 与 Python `datetime.date` 的命名冲突，改为 `normalized_date`。
- 关键 schema 决策记录在 `docs/decisions/0001-reply-extraction-schema.md`。
- Slice 2 已完成开场 reference 定位：
  - `tools/base.py`：应用代码先决定允许暴露哪些 Tools；
  - `email_assistant_hitl.py`：LLM 在受控 Tool 集合中产生 `tool_calls`，程序执行或进入 HITL；
  - `email_assistant.py`：模型结果已知后由 deterministic `if / elif` 决定路由。
- 已按 Slice 1 的 source-first 方式重做 `learning/lessons/0002-known-next-step-is-not-a-tool.html`：从 pinned `agents-from-scratch` 追踪 `@tool → get_tools → bind_tools → AIMessage.tool_calls → dispatch → invoke → observation → llm_call`，并与 deterministic triage routing 对照；对应 quick reference 为 `learning/reference/tool-calling-boundary.html`。

## Current technical focus

完整状态见 `docs/technical-map.md`。

当前项目状态：

- Schema Validation：已在自己的实现中实践并通过 deterministic tests。
- Structured Output：已实现 `with_structured_output(CreatorReply)`，并完成真实模型验证。
- 普通函数 vs Agent Tool：已有基础理解；当前通过 Lesson 0002 验证能否把边界迁移到 Campaign Context。
- RAG vs Direct Lookup：当前边界是 known-ID 结构化 Campaign Policy 优先 direct lookup。
- Policy Gate：尚未进入 own design / implementation。

## Next step — Slice 2 learning gate

严格按 `docs/workspace-guide.md` 推进：

1. 完成 `learning/lessons/0002-known-next-step-is-not-a-tool.html`，能够解释 reference 的完整 Tool Calling execution chain。
2. 在对话中完成 lesson 最后的 transfer：
   - 从 `@tool` 到 observation 回到 `llm_call` 的完整链路；
   - 对 `CreatorReply + campaign_id` 场景说明 Tool Loop 哪些部分需要保留、哪些应去掉以及原因；
   - 区分适合 deterministic policy gate 与仍需语义判断的条件。
3. 通过 learning gate 后，新增对应 `learning/learning-records/`；没有通过前不提前写 Slice 2 实现。
4. **Own design**：定义最小 Campaign Policy 输入/输出、lookup interface、policy gate 状态和边界。
5. **Tests first**：正常、缺 policy 信息、超预算、usage 超范围、币种不匹配。
6. **Implementation + verification**：实现最薄 direct lookup interface 与 deterministic policy gate，并运行测试。

当前不引入 RAG、Memory、Multi-Agent、MCP、Tool Registry、Redis 或 Queue，除非 Slice 2 的实际需求证明必要。

## Not decided yet

以下内容仍未做最终技术选择：

- 是否使用 LangGraph 作为最终编排框架
- HITL 在本项目中的具体持久化实现
- 是否需要长期 Memory
- 是否需要 RAG
- 具体模型与模型提供商
- 是否需要动态 Tool Registry / Tool Retrieval

这些内容都必须由实际需求触发，不能因为参考仓库使用或技术上“可以做”就提前引入，也不提前为其创建 lesson。
