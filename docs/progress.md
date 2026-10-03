# Current Progress

## Current project

Creator Outreach / Reply Copilot

## Current phase

**Slice 2 — Campaign Context + Policy Gate 已开始。**

当前步骤：

**Implementation + verification complete — Understanding Check pending**

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
- Slice 2 的 direct lookup / minimal CampaignRules / PolicyDecision 关键边界记录在 `docs/decisions/0002-campaign-rules-policy-gate.md`。

## Current technical focus

完整状态见 `docs/technical-map.md`。

当前项目状态：

- Schema Validation：已在自己的实现中实践并通过 deterministic tests。
- Structured Output：已实现 `with_structured_output(CreatorReply)`，并完成真实模型验证。
- 普通函数 vs Agent Tool：Lesson 0002 learning gate 已通过；已能把 reference 的 Tool Loop 迁移到 Campaign Context，并判断已知 next step 应直接调用普通函数。
- RAG vs Direct Lookup：当前边界是 known-ID 结构化 Campaign Policy 优先 direct lookup。
- Policy Gate：已理解 deterministic rule boundary，现进入 own design；尚未实现，因此仍未达到 PRACTICED。

## Next step — Slice 2 Own Design

Lesson 0002 learning gate 已通过，记录见 `learning/learning-records/0005-known-next-step-removes-tool-loop.md`。

严格按 `docs/workspace-guide.md` 继续：

1. **Own design**：由项目需求定义最小 Campaign Rules / Policy Context，而不是从 reference 机械复制：
   - 输入：`CreatorReply + campaign_id`；
   - direct lookup interface：已知 next step，整个 Agent Tool protocol 删除；
   - 最小 Campaign rules/context：只保留下游 gate 真正需要的业务规则；
   - policy gate 输出：`within_policy / outside_policy / missing_information / human_review` + `reasons`；
   - 明确 deterministic rules 与仍需 semantic judgment 的边界。
   - 当前 v1 已锁定：`CampaignRules = campaign_id + max_budget + currency + latest_delivery_date`；Campaign 配置缺失在 lookup 层失败，不进入 Policy Gate；`missing_information` 仅表示 CreatorReply 一侧缺少判断所需事实。
   - Quote v1 规则已锁定：`current_quote + exact` 直接比预算；range 全部在预算内/外可确定判断，跨预算走 `human_review`；`starting_from > budget` 为 `outside_policy`，否则 `human_review`；`usual_rate` 为 `missing_information`；`quote_basis=unclear` 或存在自然语言 `conditions` 时不强行确定化，走 `human_review`。
   - Delivery v1 规则已锁定：`delivery=None → missing_information`；exact/deadline 直接与 `latest_delivery_date` 比较；date range 全部在 deadline 内/外可确定判断，跨 deadline 走 `human_review`；approximate delivery 走 `human_review`。
   - Multi-quote v1 规则已锁定：`quotes=None → missing_information`；单个 quote 按 Quote v1 规则判断；多个 quotes 不自动选价或猜适用条件，直接 `human_review`。
2. **Tests first**：已完成 lookup failure、预算/币种、Quote amount types、delivery、multiple quotes、状态优先级和 boundary cases。
3. **Implementation**：已完成 `src/campaign_policy/`：
   - `schemas.py`：`CampaignRules / PolicyDecision`；
   - `lookup.py`：已知 `campaign_id` 的 direct lookup + validation；
   - `gate.py`：deterministic policy checks + `evaluate_campaign_policy` 主入口。
4. **Verification**：从当前 GitHub 文件内容在隔离环境复现并运行 pytest，**46 passed**（Slice 2 新测试 + Slice 1 regressions）。
5. **Understanding check**：当前唯一剩余步骤。需要能够解释当前设计、为什么不用 Agent Tool、status priority、lookup/gate failure boundary，以及什么条件出现时应重新设计。

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
