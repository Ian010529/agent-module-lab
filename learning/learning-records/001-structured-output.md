# Learning Record 001 — Structured Output + Schema Validation

## Status

**IN PROGRESS**

当前已经进入正式学习，但尚未完成 Final Gate，也尚未在本项目自己的 `src/` 中实现并通过测试。

## Evidence already demonstrated

在当前学习过程中，已经通过回答或设计判断表现出：

- 能从 Creator Reply 中识别明确合作意愿。
- 能区分 “usual fee” 与针对当前合作的确定报价，不把所有金额都当作同一种 quote。
- 能识别原文没有给出 currency，并接受 missing/unknown，而不是默认猜测。
- 能识别 paid usage 会改变价格条件。
- 能把 “报价是否超过已知 budget” 归到 deterministic comparison，而不是继续交给 LLM。
- 能发现单一 `price_amount` 会丢失多个价格及其对应条件之间的关系。
- 在简单 schema 对比中选择 nested quote 方向，而不是单一价格字段。

## Reference exposure completed

已阅读并讨论 pinned `agents-from-scratch` 中：

- `RouterSchema`
- `llm.with_structured_output(RouterSchema)`
- `triage_router()`
- `result.classification`
- classification 后的 deterministic routing
- triage exact-match evaluation

“阅读过”不等于已经通过 mastery gate。

## Not yet demonstrated

仍需要独立证明：

- 能不依赖提示解释 structured output 与 prompt-only JSON 的边界。
- 能独立解释 schema validity 与 semantic correctness 为什么不同。
- 能自己写出 Creator Reply 的最小 Pydantic schema。
- 能处理 exact / range / missing / ambiguous 等报价情况而不制造 false precision。
- 能说明并设计 cross-field validation。
- 能针对新 Creator Reply 完成 extraction schema 迁移。
- 能建立正常、缺字段、模糊报价、格式异常等固定测试案例。
- 能在项目自己的实现中通过测试。

## Next evidence required

完成：

`learning/lessons/01-structured-output.html`

中的 **Final Gate**。

通过后：

1. 更新本 learning record；
2. 进入 Creator Reply Extraction 的 Own Design；
3. 在 `src/` 与 `tests/` 中完成实现和验证；
4. 再判断 `docs/technical-map.md` 是否可从 `UNDERSTANDING` 更新为 `PRACTICED`。
