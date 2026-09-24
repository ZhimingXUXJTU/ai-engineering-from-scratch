# 卡普斯通16  GitHub 发行至公关 独立代理人

> 标签一个问题,获得一个PR  2026自主编码代理产品形状:运行一个代理在云沙箱,验证测试通过,并发布一个准备备好审查的PR, 它们都在运输中,包括 AWS 远程SWE 代理,Cursor 背景代理,OpenAI Codex 云和Google Jules. 硬部分是自动复制 repo 的构建环境, 防止凭证泄露, 执行每次 repo 预算, 这块顶石构建了自主托管版本,并将其比较在成本和通过率上与托管的替代品.

> **【中文解读】**本节是综合项目,构建GitHub版到公关的自动化代理.


**Type:** Capstone | **类型:** Capstone
**Languages:** Python (agent), TypeScript (GitHub App), YAML (Actions) | **语言:** Python (agent), TypeScript (GitHub App), YAML (Actions)
**Prerequisites:** Phase 11 (LLM engineering), Phase 13 (tools), Phase 14 (agents), Phase 15 (autonomous), Phase 17 (infrastructure)

>  **【前置】**顶点项目 16 = 综合阶段 11/13/14/15/17。GitHub 问题→PR 代理 = AWS 远程SWE / 课程背景 / OpenAI Codex云 / Google Jules 共识产品形态。
>  **【类比】**问题→PR代理 = "AI 修 bug 工程师"――流程:标题→云端沙箱跑代理→测试通过→发可审 PR(带理性) ――难点:(1) 自动重现仓库构建环境;(2) 防凭证泄漏;(3) 强制每次回应 预算;(4) 禁止强迫推――要求:自建+与托管方案对比成本+通过率――**前置知识:**项目项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目:
**Phases exercised:**现在,我们在这个世界里,**涉及阶段:**子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子
**Time:** 30 hours | **时间:** 30 hours

## 问题 问题引入

> **【中文解读】**本节描述异步云端编码代理的核心挑战. 与交互式编码代理不同,这里UX是GitHub标签标签`@agent fix this`后,工作器在云沙箱中启动,克隆仓库、运行测试、编辑文件、验证并开 PR──工程挑战包括:环境复现(从零构建无缓存开发镜像) 测试动、证书范围控制、每天每仓库预算强制和禁止强迫――

> **【拓展：异步编码 Agent 产品】**2026年异步云端编码代理 已成为独立品类──AWS远程SWE代理、Cursor背景代理、OpenAI Codex Cloud、Google Jules、Factory Droids 都采用相同的架构:标签触发 →云沙箱 →自动构建 →代理 循环 → CI 验证 → PR 提交──关键安全措施:GitHub App 使用短期安装代币,分支保护禁止直接写主要 和强力推,每天每仓库预算上限如(5 PR/天,$20/PR）。自托管版本与托管方案对比时，主要看 pass rate 和 $关于 公共事务

无同步云编码代理是与互动编码代理 (capstone 01) 独立的产品类别.UX是一个GitHub标签.你标签一个问题`@agent fix this`工作者在云沙箱中旋转,克隆备忘录,运行测试,编辑文件,验证,并打开一个与代理的逻辑在身体中的 PR.没有交互循环,没有终端. AWS 远程SWE 代理,Cursor 背景代理,OpenAI Codex 云,谷歌 Jules 和工厂 Droid 都会汇聚在这里.

> 无机云编码代理是与互动编码代理 (capstone 01) 单独的产品类别.UX是一个GitHub标签.你标签一个问题`@agent fix this`工作者在云沙箱中旋转,克隆备忘录,运行测试,编辑文件,验证,并打开一个与代理的逻辑在身体中的 PR.没有交互循环,没有终端. AWS 远程SWE 代理,Cursor 背景代理,OpenAI Codex 云,谷歌 Jules 和工厂 Droid 都会汇聚在这里.


工程挑战是具体的:环境复制 (代理必须从零开始建立 repo,而无需缓存开发图像),碎片测试 (必须重新运行或孤立),凭证范围 (一个拥有最小的微粒许可的 GitHub 应用程序),每天每次 repo 的预算执行,以及无力推政策.

> 工程挑战是具体的:环境复制 (代理必须从零开始建立 repo,而无需缓存开发图像),碎片测试 (必须重新运行或孤立),凭证范围 (一个拥有最小的微粒权限的 GitHub 应用程序),每天每次 repo 的预算执行,以及无力推政策.


## 概念的核心概念

> **【中文解读】**触发通过 GitHub webhook(问题标签或 PR 评论),调度器将任务进入队伍到 ECS Fargate 或 Lambda。工作器将仓库拉入Daytona/E2B 沙箱,使用从仓库推断的通用Dockerfile。代理运行迷你自动代理循环(读代码→提议修复→打补丁→运行测试) ・完整的CI 通过后开才PR,覆盖率下降超过值时标记`needs-review`◎安全通过GitHub应用程序 短期代币 + 分支保护 + 工作器级文件编辑白名单实现──

> **【拓展：沙箱环境复现】**环境复现是不同步 代理的核心难点 代理必须从零构建仓库的开发环境――自动推断策略包括:检测语言/框架(package.json/pom.xml/Cargo.toml/requirements.txt) 、选择基础镜像、安装依赖――Daytona 和 E2B 都提供预构建的开发容器模板――测试动处理策略:失败测试重跑3次,一致失败才看为真失败――预算强制在调度器层面实现(每天/每仓库/每PR三层上限) ⋅

引发器是GitHub网络连接器 (问题标签或公关评论).一个发送器将工作列到ECSFargate或Lambda. 工作者将 repo 拉入一个Daytona或E2B沙箱中,使用从 repo (语言,框架) 推出的通用Dockerfile. 代理运行一个小型Swe-agent或SWE-agent v2循环对Claude Opus 4.7或GPT-5.4代码进行反复. 它反复:阅读代码,提出修复,应用补丁,运行测试.

> 发射器是GitHub网络连接器 (问题标签或公关评论).一个发送器将工作列到ECSFargate或Lambda. 工作者将 repo 拉入一个Daytona或E2B沙箱中,使用从 repo (语言,框架) 推导的通用Docker文件. 代理运行一个小型Swe-agent或SWE-agent v2循环对Claude Opus 4.7或GPT-5.4代码进行反复. 它反复:阅读代码,提出修复,应用补丁,运行测试.


验证是关门步骤. 在公关开放之前,完整的公关必须通过沙箱. 覆盖率的三角形计算;如果超过门,公关开放,但标签.`needs-review`代理人将理由列为 PR 描述加上一个`@agent`审查员可以寻求后续.

> 验证是关门的步骤.


应用程序提供了一个短暂的安装代币.`workflows: read`应用程序的权限 (而不是应用程序权限) 强制"没有直接写到`main`没有强迫推, 应用程序从来没有被添加到绕过列表.`.github/workflows`作为一个真正的GitHub应用程序原始,所以代理的文件编辑允许列表必须在工作者身上执行.每天每次备用程序的预算上限在发送器上执行 (例如,每天每次备用程序最多5次,每次备用程序为20美元).

> 应用程序提供了一个短暂的安装代币.`workflows: read`应用程序的权限 (而不是应用程序权限) 强制"没有直接写到`main`应用程序从来没有被添加到绕过列表中.


## 建筑,建筑

```
GitHub issue labeled `@agent fix` or PR comment
            |
            v
    GitHub App webhook -> AWS Lambda dispatcher
            |
            v
    ECS Fargate task (or GitHub Actions self-hosted runner)
       - pull repo
       - infer Dockerfile (language, package manager)
       - Daytona / E2B sandbox with target runtime
       - clone -> git worktree -> agent branch
            |
            v
    mini-swe-agent / SWE-agent v2 loop
       Claude Opus 4.7 or GPT-5.4-Codex
       tools: ripgrep, tree-sitter, read/edit, run_tests, git
            |
            v
    verify CI passes in-sandbox + coverage delta check
            |
            v (verified)
    git push + open PR via GitHub App
       PR body = rationale + diff summary + trace URL
       label: needs-review
            |
            v
    operator reviews; can @-mention agent for follow-ups
```

##  技术

- 触发器:GitHub应用程序,有微粒代币;通过Lambda或Fly.io接收器
  中文翻译:触发器:GitHub应用程序,有细粒度的代币;通过Lambda或Fly.io接收器
- 工作者:ECS Fargate任务 (或 GitHub 行动自主托管的运行器)
  中文翻译:Worker:ECS Fargate任务 (或 GitHub 行动自主托管的运行器)
- 沙箱:每项任务的Daytona开发集装箱或E2B沙箱
  中文翻译:沙箱:每项任务的Daytona devcontainer或E2B沙箱
- 代理循环:迷你Swe-agent基线或SWE-agent v2 通过Claude Opus 4.7 / GPT-5.4-Codex
  中文翻译:代理循环:小自代理基线或SWE代理v2对Claude Opus 4.7 / GPT-5.4-Codex
- 获取:树木监护者复核地图 + 撕裂
  中文翻译:恢复:树守备备地图 + 撕裂
- 验证:全CI在沙箱+覆盖地达尔塔门
  中文翻译:验证:全CI在沙箱+覆盖地达尔塔门
- 可观察性:与每个人关系的痕迹档案由公关机构链接
  中文翻译:可观察性:与每个人信息记录档案的长相,从公共信息机构链接
- 预算:每期每日美元上限;每期每日每期每日公交
  中文翻译:预算:每期每日美元上限;每期每日最大公交

## 动手构建

> **【中文解读】**构建GitHub问题到 PR的自动化代理:GitHub App权限管理) 细粒度安装代币) 问题 分类器 (类别) 实现代理 (SWE-bench 级别问题解决)  PR 创建和审查――安全设计强调:不允许直接推送到主,不允许强迫推力,不允许修改.github/工作流程――

> **【拓展：GitHub Copilot Autofix 和 SWE-Agent 的自动化 PR 实践】**基特哈布的副驾驶自动修复了安全漏洞生成修复了PR──SWE-代理) 在SWE-台上达到50%+通过率──OpenHands(原 OpenDevin) 的CodeAct代理将将问题到 PR流程完全自动化──关键挑战是分支策略和CI 集成创建代理的PR 目的必须通过项目CI检查,但CI 本人可能依赖于Code修改的代理──本人分支保护和工作流程限制设计解决了这个问题.
```figure
cf-issue-to-pr
```

## 建立它

1. **GitHub App.**细节的安装代币:问题阅读+写,拉_请求写,内容阅读+写,工作流读.`main`"和"没有强迫推",应用程序不在绕行列表. 工人强制"没有写下`.github/workflows`由于GitHub应用程序权限没有路径范围.
   中文翻译:1. **GitHub App.**细节的安装代币:问题阅读+写,拉_请求写,内容阅读+写,工作流读.`main`"和"没有强迫推",应用程序不在绕行列表. 工人强制"没有写下`.github/workflows`由于GitHub应用程序权限没有路径范围.

2. **Webhook receiver.**通过 Lambda 函数接受问题标签 / PR 评论网页.`@agent fix this`查询到SQS.
   翻译: 翻译:**Webhook receiver.**通过 Lambda 函数接受问题标签 / PR 评论网页.`@agent fix this`查询到SQS.

3. **Dispatcher.**执行每日预算,用 repo URL,发行机器和新鲜的Daytona沙箱,
   翻译: 翻译:**Dispatcher.**执行每日预算,用 repo URL,发行机器和新鲜的Daytona沙箱,

4. **Environment inference.**检测语言 (Python, Node, Go, Rust) 和包管理器 (uv, pnpm, go mod, cargo).如果没有,则在飞行中生成Docker文件.
   翻译: 翻译:**Environment inference.**检测语言 (Python, Node, Go, Rust) 和包管理器 (uv, pnpm, go mod, cargo).如果没有,则在飞行中生成Docker文件.

5. **Agent loop.**工具: ripgrep,树座 repo-map, read_file, edit_file, run_tests, git. 硬限制:20美元的成本,30分钟的墙钟,30个代理转.
   翻译: 五.**Agent loop.**工具: ripgrep,树座 repo-map, read_file, edit_file, run_tests, git. 硬限制:20美元的成本,30分钟的墙钟,30个代理转.

6. **Verification.**循环结束后,在沙盒中运行整个测试套件.通过 jacoco / coverage.py计算覆盖率德尔塔.如果CI红色:停止,不要打开PR.如果覆盖率下降超过2%:打开PR与 `needs-review`标签
   翻译: 七个字**Verification.**循环结束后,在沙盒中运行整个测试套件.通过 jacoco / coverage.py计算覆盖率德尔塔.如果CI红色:停止,不要打开PR.如果覆盖率下降超过2%:打开PR与 `needs-review`标签

7. **PR posting.**通过 GitHub API 打开 PR 内容,标题,理由,差异概要,追踪URL,成本,转折.
   翻译:7.**PR posting.**通过 GitHub API 打开 PR 内容,标题,理由,差异概要,追踪URL,成本,转折.

8. **Credential hygiene.**工作者使用了短暂的GitHub应用程序安装代币.
   翻译:8.**Credential hygiene.**工作者使用了短暂的GitHub应用程序安装代币.

9. **Eval.**30种种植的内部问题具有不同难度.测量通过率,公关质量 (不同尺寸,风格,覆盖率),成本,延迟.对相同问题进行比较.
   翻译:9.**Eval.**30种种植的内部问题具有不同难度.测量通过率,公关质量 (不同尺寸,风格,覆盖率),成本,延迟.对相同问题进行比较.

## 用它使用方法

```
# on github.com
  - user labels issue #842 with `@agent fix this`
  - PR #1903 appears 14 minutes later
  - body:
    > Fixed NPE in widget.dedupe() caused by null comparator entry.
    > Added regression test widget_test.go::TestDedupeNullComparator.
    > Coverage delta: +0.12%
    > Turns: 7  Cost: $1.80  Trace: langfuse:...
    > Label: needs-review
```

## 发射上线

`outputs/skill-issue-to-pr.md`作为一个 GitHub App + 无同步云工作者,将标记的问题转化为准备的 PR,具有限额成本和范围的凭证.

> `outputs/skill-issue-to-pr.md`是交付物.一个GitHub App +异步云工作者,将标记的问题转化为准备审查的公关,具有限额成本和范围的凭证.


| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | Pass rate on 30 issues | End-to-end success (CI green + coverage OK) |
| 20 | PR quality | Diff size, coverage delta, style conformance |
| 20 | Cost and latency per resolved issue | $ and wall-clock per PR |
| 20 | Safety | Scoped token, per-repo budget, no force-push, credential hygiene |
| 15 | Operator UX | Rationale comments, retry affordance, @-mention follow-up |
| **100** | | |

## 练习题

1. 添加"固定片测试"模式:标签 `@agent stabilize-flake TestX`测试50次在沙盒中进行,并提出一个最小的变化,

2. 根据三项共同问题,比较成本与代背景代理. 报告哪些工具在哪里获胜.

3. 实施预算仪表板:每次报复每天成本,每用户成本.

4. 建立一个"干跑"模式, 打开一个 PR 草案, 没有运行 CI,

5. 加入保留政策:未合并的7天以上的公关分公司将自动删除.

## 关键词 关键词

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| GitHub App | "Scoped bot identity" | App with fine-grained permissions + short-lived installation token |
| Async cloud agent | "Background agent" | Non-interactive worker that runs in a cloud sandbox, not a terminal |
| Environment inference | "Dockerfile synthesis" | Detect language + package manager, generate a Dockerfile if absent |
| Verification | "CI-in-sandbox" | Run the full test suite inside the worker before opening a PR |
| Coverage delta | "Coverage preservation" | Change in test coverage % from base to agent branch |
| Per-repo budget | "Daily ceiling" | Dollar and PR-count cap enforced at the dispatcher |
| Rationale | "PR body explanation" | Agent's summary of what changed and why; required in the PR body |

## 继续阅读 继续阅读

- [AWS Remote SWE Agents](https://github.com/aws-samples/remote-swe-agents)可нони化异步云代理参考
- [SWE-agent](https://github.com/SWE-agent/SWE-agent) CLI 参考
- [Cursor Background Agents](https://docs.cursor.com/background-agent)商业替代品
- [OpenAI Codex (cloud)](https://openai.com/codex)主办的竞争对手
- [Google Jules](https://jules.google)谷歌的托管版本
- [Factory Droids](https://www.factory.ai)替代商业参考
- [GitHub App documentation](https://docs.github.com/en/apps) 范围的机器人身份
- [Daytona cloud sandboxes](https://daytona.io)参考沙盒
