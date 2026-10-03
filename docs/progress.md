# Current Progress

## Current project

Creator Outreach / Reply Copilot

## Current phase

**Slice 3 — Next Action Recommendation + Safe Reply Draft 已开始。**

当前步骤：

**Technical foundation + reference trace — action routing / draft generation / side-effect boundary**

Slice 1 — Creator Reply Extraction 已完成并收口。

Slice 2 已完成：`CreatorReply + campaign_id → CampaignRules → PolicyDecision`。Slice 3 固定承接 `docs/project-scope.md` 中尚未完成的“建议与草稿”能力：基于已经结构化的 Creator Reply 与 PolicyDecision，形成有依据的下一步建议与安全回复草稿；不自动接受报价、不承诺寄样/预算、不发送真实商务邮件。

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
- 普通函数 vs Agent Tool：已在 Slice 2 实现 known-ID direct lookup，整个 Agent Tool protocol 被移除，并通过测试。
- RAG vs Direct Lookup：known-ID Campaign rules direct lookup 已实现并通过测试；当前没有 RAG 需求。
- Policy Gate：已实现 budget / currency / delivery / missing / ambiguity checks，并通过 deterministic tests，当前为 PRACTICED。

## Next step — Slice 3

严格按 `docs/workspace-guide.md` 从 **Technical foundation** 开始，不跳到 Own Design 或实现。

### Slice 3 business goal

承接已完成的：

`CreatorReply + PolicyDecision`

解决 `docs/project-scope.md` 中的“建议与草稿”能力：

- 给出有现有事实和规则依据的下一步建议；
- 在适合的情况下生成回复草稿；
- 缺信息时应能形成澄清方向，而不是编造事实；
- 涉及越权、业务承诺或无法可靠判断时保留人工处理边界；
- 默认只生成建议/草稿，不执行真实发送或商务承诺。

本 Slice **不预先决定**最终 action schema、draft schema、是否使用 LangGraph、是否用 Tool 来表示 draft 动作；这些留到 learning gate 之后由用户 Own Design。

### Technical foundation

当前只学习足以完成 Own Design 的技术边界：

1. **Decision / routing vs generation**：哪些下一步可以由已有结构化状态确定，哪些内容才需要 LLM 生成自然语言。
2. **Draft vs side effect**：生成文本草稿与真正执行 `write_email` / 外部写操作是不同权限层。
3. **Grounded generation / no-commit boundary**：草稿只能使用已有 CreatorReply / PolicyDecision / 已批准业务事实，不把缺失信息或未授权承诺写成确定事实。
4. **HITL placement**：只理解 reference 中为什么在 side-effectful action 前 interrupt；不在 Technical Foundation 阶段预先决定本项目最终 HITL 架构。

### Pinned reference for this Slice

仍然只使用当前主项目已经指定的：

`reference/agents-from-scratch` @ `603fc7a4ac6119004f43894395e504a1fefcc6c0`

优先追踪：

- `src/email_assistant/prompts.py`：response-agent 如何约束回复行为、已有 context 如何进入生成；
- `src/email_assistant/tools/default/email_tools.py`：`write_email` 是一个真实 side-effectful action，而不只是“生成一段文本”；
- `src/email_assistant/email_assistant_hitl.py`：模型选择 action 后，application 如何在执行 `write_email` 前插入 HITL，以及 accept/edit/ignore/response 如何改变执行；
- 必要时对照 `src/email_assistant/email_assistant.py` 的非 HITL tool loop。

不引入 `gpt-researcher`、`vanna` 或 `tau2-bench`；它们仍按 `docs/references.md` 的既定阶段使用。

### Learning gate before Own Design

新对话应先完成 Slice 3 lesson/reference trace，并确认用户能解释：

- 为什么“决定下一步做什么”和“把回复写成自然语言”不一定应该交给同一层；
- reference 中 `write_email` 为什么属于有 side effect 的 Tool，而“只生成 draft”可以有不同的实现边界；
- HITL 在 reference 中拦截的是哪一层、为什么；
- 如果 PolicyDecision 已经明确是某种状态，哪些 control flow 没必要再让 LLM 猜；
- 什么信息可以进入草稿，什么信息缺失时必须保留未知/澄清而不能编造。

通过 learning gate 后，才进入用户 Own Design；然后依次 tests/eval → vibe coding → verification → understanding check → state update。

## Not decided yet

以下内容仍未做最终技术选择：

- 是否使用 LangGraph 作为最终编排框架
- HITL 在本项目中的具体持久化实现
- 是否需要长期 Memory
- 是否需要 RAG
- 具体模型与模型提供商
- 是否需要动态 Tool Registry / Tool Retrieval

这些内容都必须由实际需求触发，不能因为参考仓库使用或技术上“可以做”就提前引入，也不提前为其创建 lesson。


### Slice 2 closure

Slice 2 已完成 technical foundation、reference trace、learning gate、own design、tests-first、implementation、verification 与 understanding check。
