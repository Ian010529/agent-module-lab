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
| Workflow vs Agent | UNDERSTANDING | Slice 3 将继续验证：已有 PolicyDecision 的 routing 与需要 LLM generation 的边界 |
| LLM Messages / Prompt | UNDERSTANDING | Slice 3 将学习 grounded reply drafting / no-commit prompt boundary |
| Structured Output | PRACTICED | 已实现 `with_structured_output(CreatorReply)` 并完成真实模型验收 |
| Schema Validation | PRACTICED | 已实现 Quote / Delivery cross-field validation；deterministic tests 通过 |
| Tool Calling | UNDERSTANDING | 已追踪参考项目 tool loop；后续开放式 action 选择场景再实践 |
| 普通函数 vs Agent Tool | CAN EXPLAIN | 已实现 known-ID Campaign direct lookup，并能解释何时应重新引入模型 action selection |
| Agent Loop | UNDERSTANDING | 已追踪 llm → tool → observation → llm |
| Stop Condition | UNDERSTANDING | 已分析 Done termination signal |
| State | UNDERSTANDING | 已分析参考项目 State / MessagesState |
| State Machine / Graph | UNDERSTANDING | 已追踪 StateGraph 主链 |
| LangGraph | UNDERSTANDING | 只理解当前参考实现；是否用于最终实现尚未决定 |
| HITL | UNDERSTANDING | Slice 3 将从 reference 追踪 write_email 前的 interrupt；是否用于本项目留到 Own Design |
| Interrupt / Checkpoint / Resume | UNDERSTANDING | 已追踪参考项目暂停恢复机制 |
| Context Minimization | PRACTICED | CampaignRules 仅保留 budget / currency / delivery deadline 等 gate 所需规则 |
| Business Data vs Context | PRACTICED | 已将 Campaign business data 经 lookup boundary 收敛为最小 CampaignRules |
| State vs Memory | NOT STARTED | 后续在确有长期偏好需求时学习 |
| RAG vs Direct Lookup | PRACTICED | known-ID Campaign rules direct lookup 已实现并测试；未引入 RAG |
| Tool Permission / Least Privilege | UNDERSTANDING | Slice 3 将对照 draft generation 与 side-effectful write_email 的权限边界 |
| Policy Gate | CAN EXPLAIN | 已实现并测试，能够解释状态优先级、failure boundary 与 redesign triggers |
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

**Slice 3 — Next Action Recommendation + Safe Reply Draft**

当前阶段：**Technical Foundation + pinned reference trace**

当前还没有 Slice 3 lesson 文件。新对话的第一动作是创建/开展：

`learning/lessons/0003-route-before-you-write.html`

### 当前要学的技术边界

只学习足以让用户进入 Own Design 的内容：

- **Decision / routing vs generation**：已有结构化状态能确定的 control flow，不默认再让 LLM 猜；需要自然语言表达的部分才进入 generation。
- **Draft vs side effect**：生成回复文本与执行 `write_email` / 真实发送是不同权限层。
- **Grounded / no-commit drafting**：只使用已有事实和授权信息；缺失事实必须保持未知、请求澄清或转人工，不能由模型补全。
- **HITL placement**：理解 reference 为什么在 side-effectful action 执行前 interrupt；本项目最终是否以及如何采用 HITL，留到 Own Design。

### 当前 pinned reference trace

仍只使用 `reference/agents-from-scratch` @ `603fc7a4ac6119004f43894395e504a1fefcc6c0`：

- `src/email_assistant/prompts.py`
- `src/email_assistant/tools/default/email_tools.py`
- `src/email_assistant/email_assistant_hitl.py`
- 必要时对照 `src/email_assistant/email_assistant.py`

当前不引入 `gpt-researcher`、`vanna` 或 `tau2-bench`。

### Learning gate

进入 Own Design 前，用户需要能脱离答案解释：

- 为什么 routing 与 language generation 可以分层；
- reference 的 `write_email` 为什么是 side-effectful Tool，而“只生成 draft”不是同一件事；
- HITL 在 reference 中具体拦截哪一层；
- 已有 PolicyDecision 时，哪些 next-step control 不需要 LLM 再猜；
- grounded draft 中哪些事实可以写、哪些未知必须保留未知/澄清；
- 什么条件出现时需要重新考虑 Tool / HITL / workflow 设计。

通过 gate 后才进入用户 Own Design → tests/eval → vibe coding → verification → understanding check → state update。

### Previous completed unit

Slice 2 的 Campaign Rules direct lookup + deterministic Policy Gate 已完成并收口；对应 Lesson 0002、decision 0002 与 learning records 0005/0006 保留为历史记录。

## 技术状态更新原则

技术状态跟随真实学习与项目实践更新：

- 仅阅读资料或第一次接触：保持 `NOT STARTED` 或进入正式学习后标记 `UNDERSTANDING`。
- 能用自己的话解释机制和边界：可标记 `UNDERSTANDING`。
- 已在本项目自己的实现中使用，并通过对应测试或评测：可标记 `PRACTICED`。
- 能脱离源码、提示和现成答案解释设计、替代方案、failure modes，并能迁移到新模块：可标记 `CAN EXPLAIN`。
- 当前需求没有必要使用：标记 `NOT REQUIRED NOW`，不为了学习而强行引入。

完成 teach lesson 或看过 reference 本身不等于 `PRACTICED`。每个 Slice 结束时都检查本表，但只有状态真实变化时才修改。


### Slice 3 focus

当前不把任何新技术提前标记为 PRACTICED。

本 Slice 的 Technical Foundation 只聚焦：

- deterministic next-action routing vs LLM natural-language generation；
- draft generation vs side-effectful external action；
- grounded/no-commit drafting boundary；
- reference HITL placement around side effects。

Pinned reference 仍为 `agents-from-scratch`；不跨阶段引入其他 reference。Own Design 必须在 learning gate 之后由用户完成。
