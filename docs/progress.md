# Current Progress

## Current project

Creator Outreach / Reply Copilot

## Current phase

**Slice 1 — Creator Reply Extraction 已完成并收口。**

下一阶段固定为：

**Slice 2 — Campaign Context + Policy Gate**

目标是把已经提取出的 Creator Reply 与已知 `campaign_id` 对应的业务规则连接起来，使用 direct lookup 获取最少必要 Campaign Context，再用 deterministic policy checks 判断是否在规则内、是否缺信息或是否需要人工处理。

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
- 实现过程中发现并修复了 `Delivery.date` 与 Python `datetime.date` 的命名冲突，改为 `normalized_date`。
- 关键 schema 决策记录在 `docs/decisions/0001-reply-extraction-schema.md`。

## Current technical focus

完整状态见 `docs/technical-map.md`。

当前项目状态：

- Schema Validation：已在自己的实现中实践并通过 deterministic tests；关键 range cross-field validator 已完成理解检查。
- Structured Output：已实现 `with_structured_output(CreatorReply)`，并完成真实模型验证。
- Semantic extraction correctness：真实模型验收已通过当前保留测试集；后续仍需在更多真实回复上持续观察。

## Next step — Slice 2

按 `docs/workspace-guide.md` 的 Slice 协议进入 **Campaign Context + Policy Gate**：

1. **Technical foundation**：学习“已知下一步 lookup 时 direct lookup / 普通函数 vs Agent Tool”的边界，只覆盖当前 Slice 真正需要的部分。
2. **Reference implementation**：从 pinned reference 中寻找与 context retrieval、tool boundary、deterministic routing 直接相关的实现；不机械复制架构。
3. **Own design**：
   - 输入：`CreatorReply + campaign_id`；
   - direct lookup：根据 `campaign_id` 获取最少必要 Campaign Policy；
   - deterministic policy gate：判断报价、币种、deliverable / usage 条件等是否满足已知规则；
   - 输出只区分当前需要的状态，例如 `within_policy / missing_information / human_review` 与 reasons。
4. **Tests first**：为正常、缺 policy 信息、超预算、usage 超范围、币种不匹配等案例建立固定测试。
5. **Vibe coding**：实现最薄的 context lookup interface 与 policy gate。
6. **Verification**：优先 deterministic tests；只有需要语义判断的地方才使用 LLM/eval。

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
