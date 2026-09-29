# Project References

本文件记录当前工作区固定的外部参考源码、版本与用途。参考项目用于学习、对照与实验，不代表最终实现必须采用其架构或技术栈。

## 1. agents-from-scratch

- Repository: `langchain-ai/agents-from-scratch`
- Local path: `reference/agents-from-scratch`
- Pinned commit: `603fc7a4ac6119004f43894395e504a1fefcc6c0`
- Current role: 第一主项目的主要参考源码

重点参考：

- workflow 与 agent 的边界
- structured output / routing
- tool calling 与 agent loop
- state
- human-in-the-loop
- interrupt / checkpoint / resume
- evaluation

## 2. GPT Researcher

- Repository: `assafelovic/gpt-researcher`
- Local path: `reference/gpt-researcher`
- Pinned commit: `0957c301ed06c2a5857b834358c7227c739041d4`
- Role: Creator / Competitor Research Copilot 的后续参考源码

重点参考：

- research planning
- search / retrieval
- source tracking
- parallel research
- evidence-backed synthesis

当前不把其 planner、多 Agent 或检索架构默认引入第一主项目。

## 3. Vanna

- Repository: `vanna-ai/vanna`
- Local path: `reference/vanna`
- Pinned commit: `365d0617c1a4567ffee1b19b40c27feb4206bfcf`
- Role: Campaign Performance Analyst 的后续参考源码

重点参考：

- natural language to data query
- SQL / tool execution
- user-aware permissions
- validation
- observability
- analytics agent integration

当前不开发 BI 平台，也不默认把自然语言 SQL 引入第一主项目。

## 4. tau2-bench

- Repository: `sierra-research/tau2-bench`
- Local path: `reference/tau2-bench`
- Pinned commit: `5bfa7e37b36656b37dc6d022156be6563c1007f3`
- Role: Agent evaluation 的参考实现

重点参考：

- policy
- tools
- tasks
- environment
- trajectory / end-state evaluation
- task-level reproducibility

它是评测参考，不是当前业务开发主项目，也不默认要求为本项目重新搭一套 benchmark 平台。

## 使用原则

1. 外部源码与本项目自己的实现分离。
2. 参考实现先理解问题与设计，再决定是否采用；不按仓库结构机械复制。
3. 当前任务已经确定下一步时，优先使用固定 workflow / 普通函数 / 已有业务接口，不为了 Agent 化而强行暴露 Tool。
4. RAG、Memory、Multi-Agent、MCP、Tool Registry、Redis、消息队列等都不是默认依赖。
5. 每个 reference 都固定 commit；需要升级时先说明升级原因及影响，再修改 pinned version。
