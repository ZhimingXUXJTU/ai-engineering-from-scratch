# AI Scientist v2 — Workshop-Level Autonomous Research | AI Scientist v2 — 工作坊级自主研究

> Sakana's AI Scientist v2 (Yamada et al., arXiv:2504.08066) runs the full research loop: hypothesis, code, experiments, figures, writeup, submission. It is the first system to have a generated paper pass peer review at an ICLR 2025 workshop. Independent evaluation (Beel et al.) found 42% of experiments failed from coding errors and literature review frequently mislabeled established concepts as novel. Sakana's own docs warn that the codebase executes LLM-written code and recommend Docker isolation. Both halves of that picture are the point.

> **【中文解读】** Sakana 的 AI Scientist v2（Yamada 等人，arXiv:2504.08066）运行完整的研究循环：假设、编码、实验、图表、撰写、提交。它是第一个有生成论文通过 ICLR 2025 工作坊同行评审的系统。独立评估（Beel 等人）发现 42% 的实验因编码错误失败，文献综述频繁将已建立的概念错误标记为新颖。Sakana 自己的文档警告代码库执行 LLM 编写的代码并建议 Docker 隔离。这两面都是本课重点。

> **【拓展：开放式研究的代价】** AlphaEvolve 和 DGM 都有"机器可检查的评估器"——单元测试或基准。研究没有：论文由审稿人评判，而非单元测试。这让闭环更难，但价值也更高（研究是复利增长的来源）。AI Scientist v2 用同行评审（弱信号）作为评估器，这意味着它的安全模型与 AlphaEvolve 根本不同——必须依赖沙箱、人工审查和披露。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, research-loop state-machine toy) | **语言:** Python（标准库，研究循环状态机玩具）
**Prerequisites:** Phase 15 · 03 (AlphaEvolve), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 03（AlphaEvolve），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 15·03-04（AlphaEvolve/DGM）、Phase 14·30+（工作台 Agent 实践）、学术论文写作基础。AI Scientist = 开放式研究任务，评估器是"同行评审"（弱信号），所以安全模型完全不同。
> 💡 **【类比】** AI Scientist = "AI 博士生"。AlphaEvolve/DGM = 工程师（评估器=单元测试，强信号）；AI Scientist = 博士生（评估器=审稿人，弱信号）。同样跑实验-评估-迭代循环，但弱信号评估让 Agent 容易自欺——42% 的实验代码有 bug，文献综述把已知概念当新发现。修复：(1) Docker 隔离（执行 LLM 代码必须沙箱化）；(2) 人类复核（披露 AI 生成）；(3) 引入强信号检查（如复现性测试）。

## The Problem | 问题引入

Research is an open-ended task.

> 研究是开放式任务。

Unlike AlphaEvolve's algorithmic search or DGM's benchmark-bounded self-modification, a research result does not have a machine-checkable correctness criterion. A paper is judged by reviewers, not unit tests. That makes the loop harder to close — and more valuable if closed, because research is where compounding progress lives.

> 与 AlphaEvolve 的算法搜索或 DGM 的基准约束自修改不同，研究结果没有机器可检查的正确性标准。论文由审稿人评判，而非单元测试。这让闭环更难——但若闭合则更有价值，因为研究是复利进展的所在。

AI Scientist v1 (Sakana, 2024) closed the loop by starting from human-authored templates. The LLM filled in experiments within a fixed scaffolding. AI Scientist v2 (Yamada et al., 2025) removes the template requirement by using agentic tree search with a vision-language model critique loop. The system generates ideas, implements experiments, produces figures, writes a paper, and iterates on reviewer feedback.

> AI Scientist v1（Sakana，2024）通过从人类编写的模板开始闭合循环。LLM 在固定脚手架中填充实验。AI Scientist v2（Yamada 等人，2025）通过使用带有视觉语言模型评审循环的 Agent 式树搜索移除了模板要求。系统生成想法、实现实验、生成图表、撰写论文并迭代审稿反馈。

> **【中文解读】** AI Scientist v2 (Sakana, 2025) 运行完整的研究循环：假设、编码、实验、图表、论文撰写和提交。它是第一个有生成论文通过 ICLR 2025 工作坊同行评审的系统。但独立评估发现 42% 的实验因编码错误失败，文献综述经常将已建立的概念标记为新颖。两面都是事实。

Peer review verdict: one v2-generated paper was accepted at an ICLR 2025 workshop (with disclosure). Independent evaluation verdict: the system is far from reliable. Both are true.

> 同行评审结论：一篇 v2 生成的论文被 ICLR 2025 工作坊接受（附带披露）。独立评估结论：系统远非可靠。两者都是事实。

## The Concept | 核心概念

### The architecture | 架构

1. **Idea generation.** The LLM proposes research ideas conditioned on a topic and prior literature. v1 used templates; v2 uses agentic search over a space of hypotheses.
   中文翻译：**想法生成。** LLM 基于主题和先前文献提出研究想法。v1 使用模板；v2 在假设空间上使用 Agent 式搜索。
2. **Novelty check.** A literature retrieval step checks whether the idea has been published. This is the step where Beel et al.'s evaluation found mislabeling — established methods frequently classified as novel.
   中文翻译：**新颖性检查。** 文献检索步骤检查想法是否已发表。这是 Beel 等人评估发现错误标记的步骤——已建立的方法频繁被分类为新颖。
3. **Experiment plan.** The agent drafts an experimental protocol and writes code.
   中文翻译：**实验计划。** Agent 起草实验协议并编写代码。
4. **Execution.** Code runs in a sandbox. Failures are fed back into a retry loop. In Beel et al.'s measurements, 42% of experiments failed from coding errors at this stage.
   中文翻译：**执行。** 代码在沙箱中运行。失败反馈到重试循环。在 Beel 等人的测量中，42% 的实验在此阶段因编码错误失败。
5. **Figure generation.** A vision-language model reads generated figures and rewrites them for clarity. This was v2's key technical addition.
   中文翻译：**图表生成。** 视觉语言模型读取生成的图表并为清晰性重写它们。这是 v2 的关键技术添加。
6. **Writeup.** The LLM drafts a paper, iterates with an internal reviewer.
   中文翻译：**撰写。** LLM 起草论文，与内部审稿人迭代。
7. **Optional: submission.** The paper is submitted to a venue.
   中文翻译：**可选：提交。** 论文提交到会议。

### What the workshop-acceptance result means | 工作坊接受结果意味着什么

One v2-generated paper passed peer review at an ICLR 2025 workshop. The authors disclosed the paper's origin to the program committee. The acceptance is a data point; it is not a license to claim the system "does research."

> 一篇 v2 生成的论文在 ICLR 2025 工作坊通过同行评审。作者向程序委员会披露了论文的来源。接受是一个数据点；不是声称系统"做研究"的许可。

Important context: workshop papers are a lower bar than main-conference papers. Peer review is noisy; a small fraction of submissions are accepted on any given day. One success is a proof of concept, not a reliability claim. The Nature 2026 paper documents the end-to-end loop and was itself co-authored by human researchers; it is not "the system wrote a Nature paper."

> 重要背景：工作坊论文的门槛低于主会议论文。同行评审有噪声；任何一天都有一小部分提交被接受。一次成功是概念证明，不是可靠性声明。Nature 2026 论文记录了端到端循环，本身由人类研究者合著；不是"系统写了一篇 Nature 论文"。

### What the independent evaluation found | 独立评估发现

Beel et al. (arXiv:2502.14297) ran an external evaluation. Headline findings:

> Beel 等人（arXiv:2502.14297）运行了外部评估。标题性发现：

- **Experiment failures.** 42% of experiments failed from coding errors (bad imports, shape mismatches, undefined variables). The retry loop caught some, not all.
  中文翻译：**实验失败。** 42% 的实验因编码错误失败（坏导入、形状不匹配、未定义变量）。重试循环捕获了一些，但不是全部。
- **Novelty mislabeling.** The literature-retrieval step frequently flagged established concepts as novel. This is the research equivalent of hallucination.
  中文翻译：**新颖性错误标记。** 文献检索步骤频繁将已建立的概念标记为新颖。这是研究界的幻觉等效物。
- **Presentation-quality gap.** The vision-language figure critique produced publication-grade visuals, masking underlying experimental weaknesses.
  中文翻译：**呈现质量差距。** 视觉语言图表评审产生出版级视觉效果，掩盖了底层实验弱点。

The last finding is the important one for this phase. A system that produces convincing outputs without doing convincing research is more dangerous, not safer, than one that fails obviously.

> 最后一个发现对本阶段很重要。产生令人信服的输出但未做令人信服的研究的系统，比明显失败的系统更危险而非更安全。

Evaluation must reach the underlying claims, not stop at the figure.

> 评估必须触及底层声明，而不是停在图表。

### The sandbox-escape concern | 沙箱逃逸担忧

Sakana's own repository README warns:

> Sakana 自己的仓库 README 警告：

> Due to the nature of this software, which executes LLM-generated code, we cannot guarantee safety. There are risks of dangerous packages, uncontrolled web access, and spawning of unintended processes. Use at your own risk and consider Docker isolation.

> 由于本软件执行 LLM 生成的代码，我们无法保证安全。存在危险包、不受控网络访问和生成意外进程的风险。自行承担风险并考虑 Docker 隔离。

This is the operational shape of autonomy in an unverified domain. The LLM writes code; the code runs; the code can do anything the process is allowed to do. Without a sandbox that hard-limits filesystem, network, and process actions, any self-directed research agent can exfiltrate data, burn compute, or rewrite itself.

> 这是未验证领域自主性的操作形态。LLM 写代码；代码运行；代码可以做进程被允许的任何事。没有硬限制文件系统、网络和进程操作的沙箱，任何自主研究 Agent 都可泄露数据、烧毁计算或重写自己。

AlphaEvolve's sandbox story is easier because its evaluator is tight. AI Scientist v2's loop runs open-ended code with open-ended goals. That is why it needs stronger isolation (Docker minimum; seccomp / gVisor preferred) and a manual review of every submission before it leaves the system.

> AlphaEvolve 的沙箱叙述更容易，因为其评估器严密。AI Scientist v2 的循环用开放目标运行开放代码。这就是它需要更强隔离（最低 Docker；首选 seccomp / gVisor）和每次提交离开系统前人工审查的原因。

### Where v2 sits in the frontier stack | v2 在前沿栈中的位置

| System | Target | Output kind | Evaluator | Known failure |
|---|---|---|---|---|
| 系统 | 目标 | 输出类型 | 评估器 | 已知失败 |
| AlphaEvolve | algorithms | code | unit + benchmark | bounded by evaluator rigor |
| AlphaEvolve | 算法 | 代码 | 单元 + 基准 | 受评估器严谨性约束 |
| DGM | agent scaffolding | code | SWE-bench | reward hacking |
| DGM | Agent 脚手架 | 代码 | SWE-bench | 奖励篡改 |
| AI Scientist v2 | research papers | text + code + figures | peer review (weak) | experiment failures, mislabeling, polish masking weakness |
| AI Scientist v2 | 研究论文 | 文本 + 代码 + 图表 | 同行评审（弱） | 实验失败、错误标记、修饰掩盖弱点 |

v2 has the weakest automatic evaluator of the three, the widest output surface, and the shortest path to public artifacts.

> v2 在三者中拥有最弱的自动评估器、最广的输出面和最短的公开制品路径。

The operational controls (sandbox, review, disclosure) are doing most of the safety work.

> 操作控制（沙箱、审查、披露）承担了大部分安全工作。

## Use It | 用框架实现

`code/main.py` simulates the v2 loop as a state machine: idea → novelty check → experiment → figure → writeup → review → accept-or-iterate. Each state has a configurable failure probability pulled from the Beel et al. findings. Run the simulator for N loops and count:

> `code/main.py` 将 v2 循环模拟为状态机：想法 → 新颖性检查 → 实验 → 图表 → 撰写 → 审稿 → 接受或迭代。每个状态有从 Beel 等人发现中提取的可配置失败概率。运行模拟器 N 个循环并计数：

- How many ideas reach submission.
  中文翻译：多少想法到达提交。
- How many submissions would have a critical experimental flaw the polished paper hides.
  中文翻译：多少提交会有修饰论文隐藏的关键实验缺陷。
- How retry budgets trade off quality vs yield.
  中文翻译：重试预算如何在质量与产量之间权衡。

## Ship It | 产出物

`outputs/skill-ai-scientist-sandbox-review.md` is a two-gate review checklist for anything produced by a research-loop agent before it leaves the sandbox.

> `outputs/skill-ai-scientist-sandbox-review.md` 是研究循环 Agent 产生的任何制品离开沙箱前的双门审查清单。

## Exercises | 练习题

1. Run `code/main.py` with default parameters. What fraction of loop runs produce a "clean" paper? What fraction produce a paper with an experiment-failure flaw the figure critique polished over?
   中文翻译：使用默认参数运行 `code/main.py`。多少比例的循环运行产生"干净"论文？多少比例的论文有图表评审修饰过的实验失败缺陷？

2. The defaults already use Beel et al.'s 42% / 25%. Re-run with `--experiment-failure 0.20 --novelty-mislabel 0.10` and then with `--experiment-failure 0.60 --novelty-mislabel 0.40`. How does the polished-but-flawed share shift between the two runs?
   中文翻译：默认已使用 Beel 等人的 42% / 25%。用 `--experiment-failure 0.20 --novelty-mislabel 0.10` 重跑，然后用 `--experiment-failure 0.60 --novelty-mislabel 0.40`。两次运行之间修饰但有缺陷的比例如何变化？

3. Read Sakana's AI Scientist v2 repo README on sandbox requirements. Name two additional restrictions (beyond Docker) you would apply for a multi-day autonomous run.
   中文翻译：阅读 Sakana AI Scientist v2 仓库 README 关于沙箱要求。命名你会为多日自主运行添加的两项额外限制（除 Docker 外）。

4. Read Beel et al. Section 4 on presentation-quality gap. Design one additional evaluator that would catch polished-looking but experimentally flawed papers.
   中文翻译：阅读 Beel 等人第 4 节关于呈现质量差距。设计一个会捕获修饰但实验有缺陷论文的额外评估器。

5. Propose a human-review protocol for research-agent outputs that scales better than "a PhD reads every paper." Identify the bottleneck and design around it.
   中文翻译：为研究 Agent 输出提议比"博士读每篇论文"扩展更好的人工审查协议。识别瓶颈并据此设计。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AI Scientist v1 | "Sakana's templated research agent" | Filled experiments into a fixed scaffold |
| AI Scientist v1 | "Sakana 的模板研究 Agent" | 在固定脚手架中填充实验 |
| AI Scientist v2 | "Template-free research agent" | Agentic tree search with VLM figure critique |
| AI Scientist v2 | "无模板研究 Agent" | 带有 VLM 图表评审的 Agent 式树搜索 |
| Agentic tree search | "Branching research agent" | Expands multiple experiment plans in parallel; prunes by internal critic |
| Agent 式树搜索 | "分支研究 Agent" | 并行展开多个实验计划；由内部评论者修剪 |
| Vision-language critique | "VLM polish on figures" | Multimodal model reads figures and rewrites them for clarity |
| 视觉语言评审 | "VLM 修饰图表" | 多模态模型读取图表并为清晰性重写 |
| Literature retrieval | "Novelty check" | Searches prior work to confirm idea novelty — documented to mislabel |
| 文献检索 | "新颖性检查" | 搜索先前工作以确认想法新颖性——文档记录会错误标记 |
| Polish masking | "Pretty paper, broken research" | Presentation quality exceeds experimental quality; hides weaknesses |
| 修饰掩盖 | "漂亮论文，破碎研究" | 呈现质量超过实验质量；隐藏弱点 |
| Sandbox escape | "LLM code breaks out" | Agent-executed code does things the loop designer did not intend |
| 沙箱逃逸 | "LLM 代码逃逸" | Agent 执行的代码做循环设计者未预期的事 |

## Further Reading | 延伸阅读

- [Yamada et al. (2025). The AI Scientist-v2](https://arxiv.org/abs/2504.08066) — paper.
  中文翻译：论文。
- [Sakana blog on the Nature 2026 publication](https://sakana.ai/ai-scientist-nature/) — vendor summary with peer-review context.
  中文翻译：厂商摘要，含同行评审背景。
- [Beel et al. (2025). Independent evaluation of The AI Scientist](https://arxiv.org/abs/2502.14297) — external evaluation numbers.
  中文翻译：外部评估数字。
- [Sakana AI Scientist v1 paper](https://arxiv.org/abs/2408.06292) — the templated predecessor.
  中文翻译：模板化前身。
- [Anthropic — Measuring AI agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) — broader framing of open-ended research agents.
  中文翻译：开放式研究 Agent 的更宽框架。
