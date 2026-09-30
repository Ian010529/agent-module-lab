# Learning Mission

## 目标

`learning/` 是 `agent-module-lab` 内的 teach 学习工作区。

学习目标不是完整覆盖 Agent、LangChain、Pydantic 或任何框架知识，而是为了完成当前 AI 提效模块 Slice，逐步形成能够独立负责模块设计、实现、测试与排障的能力。

最终需要能够：

- 理解当前 Slice 必需的技术原理；
- 阅读并解释 pinned reference 中对应的真实实现；
- 根据 Creator Outreach / Reply Copilot 的需求设计自己的版本；
- 审查 AI 生成的关键代码，而不是只接受生成结果；
- 用测试和评测验证行为；
- 解释技术取舍、failure modes 与重新设计条件。

## 课程选择原则

课程由项目驱动，而不是由知识体系驱动。

每次只根据以下文件选择当前课程：

1. `docs/progress.md`
2. `docs/technical-map.md`
3. 当前 Slice 的真实实现需求

只有当某个知识点如果不掌握，会阻碍当前 Slice 的理解、设计、实现或验证时，才进入 lesson。

不提前生成未来课程；标记为 `NOT REQUIRED NOW` 的技术不创建 lesson。

## 学习与项目实践的边界

`learning/` 负责：

- lesson
- retrieval practice / quiz / exercise
- reference cheat sheet
- learning record

`reference/` 负责：

- pinned 外部真实源码

`src/`、`tests/`、`evals/` 负责：

- 自己的实现
- 测试
- 评测

完成 lesson 不等于 `PRACTICED`。只有技术已经在本项目自己的实现中使用并通过对应测试或评测，才更新为 `PRACTICED`。

## 当前课程

**Structured Output + Schema Validation → Creator Reply Extraction**

当前 lesson：

`learning/lessons/01-structured-output.html`
