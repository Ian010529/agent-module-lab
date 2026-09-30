# Workspace Guide

## 这个仓库是什么

`agent-module-lab` 是 AI 提效模块的学习与开发工作区。

它包含三类内容：

1. 本项目自己的目标、进度、技术地图、代码、测试与评测。
2. `learning/` 中的 teach 学习工作区，用于当前 Slice 的 lesson、练习、reference cheat sheet 与 learning record。
3. 固定版本的外部参考源码，用于阅读、运行、对照和实验。

外部参考项目不是本项目最终架构，也不直接等于未来实际业务系统的实现。learning 也不替代项目实现；lesson 完成不等于技术已经 `PRACTICED`。

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
├── learning/
│   ├── MISSION.md           # teach 的长期目标与课程选择原则
│   ├── RESOURCES.md         # 当前项目与 reference 学习资源
│   ├── NOTES.md             # 稳定的教学规则与学习备注
│   ├── lessons/             # 当前真正开展的 lesson；不提前批量生成
│   ├── reference/           # 学完后用于复习的 cheat sheet
│   ├── learning-records/    # 已经通过回答/练习证明的能力
│   └── assets/              # lesson 共用样式或组件
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
4. `learning/MISSION.md`
5. 当前技术单元对应的最新 `learning/learning-records/`
6. 当前 `learning/lessons/` 与 `learning/RESOURCES.md`
7. 当前阶段需要的 `docs/references.md` 条目
8. 对应 reference 源码与本项目相关代码

这样可以同时恢复：

- 项目为什么做
- 当前做到哪里
- 技术学到哪里
- 已经真正证明掌握什么
- 当前 lesson 的 gate 是什么
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
- 学习由当前 Slice 驱动，不为了“知识完整”提前扩展课程。
- `NOT REQUIRED NOW` 的技术不创建 lesson。
- 能由 deterministic code 可靠解决的，不默认交给 LLM。
- 已知下一步必须调用哪个业务接口时，不默认把它包装成让 Agent 自主选择的 Tool。
- 当前 Slice 有对应 pinned reference 源码时，教学默认先从仓库中的真实源码出发，再用官方文档校验 API 契约与技术边界。
- 外部源码用于理解和比较，不机械复制。
- 每个功能至少要有对应测试或评测依据。
- 重要架构决策记录原因与重新评估条件。

## 每个开发 Slice 的固定推进协议

每个 Slice 都按下面的顺序推进，不跳步：

1. **Technical foundation**
   - 由 `docs/progress.md` 与 `docs/technical-map.md` 决定当前真正需要学习的技术。
   - 在 `learning/lessons/` 中只开展当前 lesson。
   - 通过预测、练习、quiz、迁移题证明理解，而不是只阅读解释。
   - 不允许直接跳到让 AI 生成实现。

2. **Reference implementation**
   - 阅读 pinned reference 中与当前技术直接相关的真实源码。
   - 追踪输入、关键对象、控制流和失败路径。
   - lesson 可以给追踪任务，但真实 source of truth 始终是 `reference/`。
   - 理解参考实现为什么这样设计，而不是只记 API。

3. **Learning gate**
   - 当前 lesson 的 Final Gate 通过后，更新对应 `learning/learning-records/`。
   - learning record 只记录已经通过回答、练习或迁移任务证明的能力。
   - 通过 learning gate 只代表达到设计/实现前的理解要求，不等于 `PRACTICED`。

4. **Own design**
   - 根据本项目需求自己定义输入、输出、状态、边界和技术选择。
   - 不机械复制参考项目的 schema、workflow、tool 或目录结构。
   - 明确哪些步骤属于 LLM、deterministic code、已有业务接口、Tool 或 HITL。

5. **Implementation**
   - 使用 vibe coding 加速实现。
   - 关键架构、关键代码路径、权限边界和失败处理必须能够解释。
   - 不因为 AI 建议就自动引入新框架、中间件或基础设施。

6. **Verification**
   - 建立正常案例、边界案例和 failure cases。
   - 能确定性判断的行为优先使用程序测试。
   - Agent 行为再使用适合的 eval 方法验证。

7. **Understanding check**
   - 完成 Slice 前，需要能够脱离参考答案解释：
     - 它怎么工作；
     - 为什么这样设计；
     - 为什么不用更简单或其他替代方案；
     - 哪些 failure 需要在哪一层处理；
     - 什么条件出现时应该重新设计。

8. **State update**
   - 根据真实完成情况更新 `docs/progress.md`。
   - 根据实际掌握程度更新 `docs/technical-map.md`。
   - 需要时更新 learning record。
   - 只有产生真实、非显然且需要长期保留的架构决策时，才新增 `docs/decisions/`。

## 学习范围控制

新 lesson 只能由当前项目需求触发。

判断一个知识点是否进入当前 lesson，只问：

> 如果不掌握它，会不会阻碍当前 Slice 的理解、设计、实现或验证？

如果不会，就暂不学习。

因此不提前创建完整的 Agent 课程树，也不因为 reference 使用某项技术就自动学习或引入它。

## 进度更新规则

项目进度会随着真实学习和实现持续更新，但不为了“有更新”而机械改文档。

以下情况应更新 `docs/progress.md`：

- 当前 Slice 开始或结束；
- 当前 lesson / learning gate 对项目下一步产生实质变化；
- 实现、测试或评测状态发生实质变化；
- 当前 blocker、下一步或项目边界发生变化；
- 发现参考实现的重要限制或需要调整项目方案。

以下情况应更新 `docs/technical-map.md`：

- 一个技术从 `NOT STARTED` 进入正式学习；
- 已能解释基本机制，进入 `UNDERSTANDING`；
- 已在自己的项目中实现并通过测试/评测，进入 `PRACTICED`；
- 能脱离源码与提示解释设计、取舍和 failure modes，进入 `CAN EXPLAIN`；
- 需求证明当前不需要某项技术，标记 `NOT REQUIRED NOW`。

“讨论过”“看过源码”或“完成 lesson”本身都不等于 `PRACTICED` 或 `CAN EXPLAIN`。


## Teach artifact conventions

The `learning/` directory is treated as the teach workspace root.

- Lessons use `0001-<dash-case-name>.html`, `0002-...` numbering.
- Learning records use the same four-digit sequential convention.
- A lesson teaches one tightly-scoped skill and must cite vetted resources from `learning/RESOURCES.md`.
- Reusable quiz, diagram, simulator, and style code belongs in `learning/assets/`, not duplicated inside lesson files.
- Learning records capture demonstrated non-obvious learning, not session activity or unfinished checklists.
