# Project References

本文件只记录当前项目实际使用或准备使用的外部参考源码及其用途。

## agents-from-scratch

- Repository: `langchain-ai/agents-from-scratch`
- Local path: `reference/agents-from-scratch`
- Pinned commit: `603fc7a4ac6119004f43894395e504a1fefcc6c0`
- Role: 第一阶段主要参考源码

当前关注内容：

- Agent 与固定 workflow 的边界
- Tool calling
- State 与执行循环
- Human-in-the-loop
- Memory 的实现边界
- Agent evaluation

使用原则：

- 参考其实现和设计，不默认照搬架构。
- 项目自己的代码与参考源码分离。
- 只有在真实需求出现时才引入相应组件。

## Later candidates

以下项目目前只保留为后续候选，不加入仓库：

- `assafelovic/gpt-researcher`：达人 / 竞品研究模块参考
- `vanna-ai/vanna`：活动数据分析模块参考
- `sierra-research/tau2-bench`：Agent 评测设计参考

只有进入对应项目阶段时，再决定是否固定具体版本并加入 `reference/`。
