# Workspace Guide

## 这个仓库是什么

`agent-module-lab` 是 AI 提效模块的学习与开发工作区。

它包含两类内容：

1. 本项目自己的目标、进度、技术地图、代码、测试与评测。
2. 固定版本的外部参考源码，用于阅读、运行、对照和实验。

外部参考项目不是本项目最终架构，也不直接等于未来实际业务系统的实现。

## 目录职责

```text
agent-module-lab/
├── docs/
│   ├── project-scope.md     # 项目目标、边界与交付
│   ├── progress.md          # 当前做到哪里、下一步是什么
│   ├── references.md        # 参考源码版本与用途
│   ├── technical-map.md     # 技术主干与掌握状态
│   └── workspace-guide.md   # 本文件
│
├── reference/
│   ├── agents-from-scratch/
│   ├── gpt-researcher/
│   ├── vanna/
│   └── tau2-bench/
│
├── src/                     # 本项目自己的实现；开始编码后创建
├── tests/                   # deterministic / integration tests
└── evals/                   # agent / task evaluation
```

`docs/decisions/` 只在产生真实、需要长期保留的架构决策后创建，不提前制造文档。

## 新对话或重新开始工作时

按以下顺序读取：

1. `docs/project-scope.md`
2. `docs/progress.md`
3. `docs/technical-map.md`
4. 当前阶段需要的 `docs/references.md` 条目
5. 对应 reference 源码与本项目相关代码

这样可以同时恢复：

- 项目为什么做
- 当前做到哪里
- 技术学到哪里
- 参考哪一版源码
- 下一步应该做什么

## Clone

首次 clone：

```bash
git clone --recurse-submodules https://github.com/Ian010529/agent-module-lab.git
```

如果仓库已经 clone：

```bash
git pull
git submodule update --init --recursive
```

## 更新 reference 的原则

reference 默认保持 pinned。

需要升级某个外部项目时：

1. 先确认为什么需要升级；
2. 查看新旧 commit 的相关变化；
3. 判断是否影响当前理解、实现或评测；
4. 再更新 submodule pointer 与 `docs/references.md`。

## 工作原则

- 先解决模块问题，再选择技术。
- 能由 deterministic code 可靠解决的，不默认交给 LLM。
- 已知下一步必须调用哪个业务接口时，不默认把它包装成让 Agent 自主选择的 Tool。
- 外部源码用于理解和比较，不机械复制。
- 每个功能至少要有对应测试或评测依据。
- 重要架构决策记录原因与重新评估条件。
