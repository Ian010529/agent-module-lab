# Technical Map

本文件记录为了能够独立负责 AI 提效模块，需要真正掌握并在项目中验证的技术主干。

状态定义：

- `NOT STARTED`：尚未正式学习或实践
- `UNDERSTANDING`：已能解释基本机制，但还未在自己的实现中完成验证
- `PRACTICED`：已经在本项目中实际实现、测试或评测
- `CAN EXPLAIN`：能够脱离参考答案解释设计、取舍和失败模式
- `NOT REQUIRED NOW`：当前项目没有需求，不为了学习技术而强行引入

| 技术 | 当前状态 | 当前/计划中的项目落点 |
|---|---|---|
| Workflow vs Agent | UNDERSTANDING | 已通过参考源码与报价处理案例分析边界 |
| LLM Messages / Prompt | UNDERSTANDING | 已为 Reply Extraction 编写 no-guess extraction prompt；真实模型效果待持续观察 |
| Structured Output | PRACTICED | 已实现 `with_structured_output(CreatorReply)` 并完成真实模型验收 |
| Schema Validation | PRACTICED | 已实现 Quote / Delivery cross-field validation；deterministic tests 通过 |
| Tool Calling | UNDERSTANDING | 已追踪参考项目 tool loop；后续开放式 action 选择场景再实践 |
| 普通函数 vs Agent Tool | UNDERSTANDING | Lesson 0002 gate 已通过；已迁移到 Campaign lookup 的 direct-call 边界，待项目实现验证 |
| Agent Loop | UNDERSTANDING | 已追踪 llm → tool → observation → llm |
| Stop Condition | UNDERSTANDING | 已分析 Done termination signal |
| State | UNDERSTANDING | 已分析参考项目 State / MessagesState |
| State Machine / Graph | UNDERSTANDING | 已追踪 StateGraph 主链 |
| LangGraph | UNDERSTANDING | 只理解当前参考实现；是否用于最终实现尚未决定 |
| HITL | UNDERSTANDING | 已分析业务判断与执行审批两类 HITL |
| Interrupt / Checkpoint / Resume | UNDERSTANDING | 已追踪参考项目暂停恢复机制 |
| Context Minimization | UNDERSTANDING | 已确定按当前 decision 获取最少必要上下文 |
| Business Data vs Context | UNDERSTANDING | 已通过 campaign policy / creator history 案例区分 |
| State vs Memory | NOT STARTED | 后续在确有长期偏好需求时学习 |
| RAG vs Direct Lookup | UNDERSTANDING | known-ID Campaign 规则采用 direct lookup；待 Slice 2 实现与测试后再评估 PRACTICED |
| Tool Permission / Least Privilege | UNDERSTANDING | 已分析最小 Tool 暴露与只返回必要字段 |
| Policy Gate | UNDERSTANDING | 已能识别 threshold / missing / allowed-set 等 deterministic checks；现进入 own design |
| Deterministic Evaluation | PRACTICED | Reply Extraction schema / failure tests 已通过 |
| Tool-call Evaluation | UNDERSTANDING | 已追踪参考测试 |
| Trajectory Evaluation | NOT STARTED | 后续完整 agent eval |
| LLM-as-a-Judge | UNDERSTANDING | 已了解适用范围；尚未在本项目实践 |
| Business Metrics | NOT STARTED | 模块完成后做提效对比 |
| Timeout | NOT STARTED | Reliability slice |
| Retry vs Replan | NOT STARTED | Reliability slice |
| Idempotency | NOT STARTED | 外部写操作 / resume failure 场景 |
| Duplicate Event Handling | NOT STARTED | Reliability slice |
| Failure Recovery | NOT STARTED | HITL / tool execution slice |
| Observability / Tracing | NOT STARTED | 集成后补充 |
| Cost / Latency | NOT STARTED | Eval / optimization 阶段 |
| Tool Registry / Dynamic Tool Loading | NOT REQUIRED NOW | 仅在工具规模和动态选择需求真实出现时重新评估 |
| Multi-Agent | NOT REQUIRED NOW | 第一主项目不预设 |
| MCP | NOT REQUIRED NOW | 第一主项目不预设 |
| Redis / Queue | NOT REQUIRED NOW | 只有持久化、并发或异步需求证明必要时再评估 |

## 当前技术单元

Learning gate 已通过，当前进入设计：

**Campaign Context direct lookup + deterministic Policy Gate → Own Design**

对应 teach lesson：

`learning/lessons/0002-known-next-step-is-not-a-tool.html`

当前 reference trace：

- `reference/agents-from-scratch/src/email_assistant/tools/base.py`
- `reference/agents-from-scratch/src/email_assistant/email_assistant_hitl.py`
- `reference/agents-from-scratch/src/email_assistant/email_assistant.py`

当前结论：

- 已知 `campaign_id` 且下一步固定为查询 Campaign Policy 时，优先 direct lookup / 普通函数，而不是让 LLM 重新选择 Tool。
- 外部 I/O 与 Agent Tool 不是同一个概念；普通函数也可以访问 API / DB。
- Campaign Policy 与 Creator Reply 的明确规则比较应由 deterministic code 完成。
- Lesson 0002 transfer gate 已通过：对于 `CreatorReply + campaign_id` 且 lookup 为固定 next step 的场景，整个 Agent Tool protocol 删除，直接调用 application function / API。
- 用户已能列举适合 deterministic gate 的规则类型（allowed currency、required missingness、numeric threshold、enum/allowed-set membership）；`Policy Gate` 仍只有在自己的实现中落地并通过测试后才能进入 `PRACTICED`。

## 技术状态更新原则

技术状态跟随真实学习与项目实践更新：

- 仅阅读资料或第一次接触：保持 `NOT STARTED` 或进入正式学习后标记 `UNDERSTANDING`。
- 能用自己的话解释机制和边界：可标记 `UNDERSTANDING`。
- 已在本项目自己的实现中使用，并通过对应测试或评测：可标记 `PRACTICED`。
- 能脱离源码、提示和现成答案解释设计、替代方案、failure modes，并能迁移到新模块：可标记 `CAN EXPLAIN`。
- 当前需求没有必要使用：标记 `NOT REQUIRED NOW`，不为了学习而强行引入。

完成 teach lesson 或看过 reference 本身不等于 `PRACTICED`。每个 Slice 结束时都检查本表，但只有状态真实变化时才修改。
