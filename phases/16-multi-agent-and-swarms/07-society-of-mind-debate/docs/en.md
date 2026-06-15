# Society of Mind and Multi-Agent Debate | 心智社会 多 Agent 辩论

> Minsky's 1986 premise — intelligence is a society of specialists — gets rediscovered every decade. In 2023 Du et al. turned it into a concrete algorithm: multiple LLM instances propose answers, read each other's answers, critique, and update. Over N rounds they converge on a consensus that beats zero-shot CoT and reflection on six reasoning and factuality tasks. Two findings matter: both **multiple agents** and **multiple rounds** contribute independently. The society beats a single-agent monologue; the multi-round exchange beats one-shot voting.

> **【中文解读】** 本节介绍了心智社会辩论——Marvin Minsky 的心智社会理论在多 Agent 系统中的应用。

> **【拓展：society of mind debate→具体应用】** Marvin Minsky 的《心智社会》（1986）提出智能是许多简单心智的协作产物。这一思想在 2026 年的多 Agent 辩论系统中实现——多个 Agent 从不同角度讨论问题，通过辩论达成更好的结论。研究表明，3-5 个 Agent 的辩论效果最佳。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (Primitive Model)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Problem | 问题引入

Self-consistency — sample one model many times and take the majority answer — is the cheapest reasoning improvement you can bolt on. It works, but it saturates fast. You can double your samples and not see another meaningful jump.

> 自我一致性——对一个模型多次采样并取多数答案——是你可以添加的最便宜的推理改进。它有效，但很快饱和。你可以把样本量翻倍却看不到有意义的提升。

The saturation comes from correlated errors: the same model tends to fail the same way. Sampling more does not help if every sample shares the same blind spot. Debate breaks the correlation by forcing agents to confront disagreement.

> 饱和来自相关错误：相同模型倾向于以相同方式失败。如果每个样本共享相同盲点，更多采样没有帮助。辩论通过强制 Agent 面对分歧打破相关性。

Debate breaks the saturation. Instead of N independent samples from one model, N agents read each other's reasoning and revise. The correlation between samples drops (they are no longer i.i.d.), and the convergence point is often correct where i.i.d. voting was confidently wrong.

> 辩论打破了饱和。不是从一个模型中获取 N 个独立样本，而是让 N 个 Agent 阅读彼此的推理并修改。样本之间的相关性下降（它们不再是独立同分布的），收敛点通常是正确的，而独立同分布投票则在自信地犯错。

The decorrelation is the mechanism. When agents see other agents' reasoning, they cannot help but engage with it — either to defend their position or update it. This forced engagement produces information that no amount of i.i.d. sampling can.

> 去相关是机制。当 Agent 看到其他 Agent 的推理时，它们不得不参与——要么捍卫自己的立场，要么更新它。这种强制参与产生任何数量的独立同分布采样都不能产生的信息。

## Concept | 核心概念

### The Du et al. 2023 algorithm

From arXiv:2305.14325 (ICML 2024):

> 来自 arXiv:2305.14325 (ICML 2024)：

The algorithm is intentionally simple: no special roles, no judge, no moderator. Every agent is symmetric. The only asymmetry is the order of who speaks first, and even that washes out over multiple rounds.

> 算法有意简单：没有特殊角色、没有裁判、没有主持人。每个 Agent 是对称的。唯一的不对称是谁先发言的顺序，即使这也在多轮中淡化。

1. Each of N agents produces an initial answer to the question.
   中文翻译：N 个 Agent 各自产生问题的初始答案。
2. For round r = 2..R: each agent is shown the other agents' round r-1 answers and asked "considering these, give your updated answer."
   中文翻译：对于第 r = 2..R 轮：每个 Agent 看到其他 Agent 第 r-1 轮的答案并被问"考虑这些，给出你的更新答案。"
3. After R rounds, majority-vote the final answers.
   中文翻译：R 轮之后，对最终答案进行多数投票。

The paper tests on MMLU, GSM8K, biographies, MATH, and factuality benchmarks. Debate consistently beats CoT and Self-Reflection.

> 论文在 MMLU、GSM8K、传记、MATH 和事实性基准上测试。辩论持续优于 CoT 和自我反思。

The benchmark suite spans both reasoning (MATH, GSM8K — problems with verifiable correct answers) and factuality (biographies — claims checkable against Wikipedia). The factuality gains are the headline result: debate is the cheapest known method to reduce hallucination on factual questions.

> 基准套件涵盖推理（MATH、GSM8K——有可验证正确答案的问题）和事实性（传记——可对照 Wikipedia 检查的声明）。事实性增益是标题结果：辩论是减少事实性问题幻觉的已知最廉价方法。

### Two independent knobs

Ablations from the same paper:

> 同一篇论文的消融实验：

- **Agent count alone** (1 round, majority vote of N) beats single-agent on most tasks, but plateaus.
  中文翻译：**仅 Agent 数量**（1 轮，N 的多数投票）在大多数任务上优于单 Agent，但会达到平台。
- **Round count alone** (1 agent seeing its own prior reasoning) barely helps — reflection's known weakness.
  中文翻译：**仅轮数**（1 个 Agent 看到自己先前的推理）几乎没有帮助——这是反思的已知弱点。
- **Both together** produces the big jumps. The multi-round exchange between multiple agents drives the gain.
  中文翻译：**两者结合**产生大幅提升。多个 Agent 之间的多轮交流驱动了收益。

### Why it works

Two mechanisms:

> 两个机制：

The two mechanisms compound: exposure to disagreement provides new information; decorrelated errors prevent the new information from being averaged into the wrong answer. Either alone is weaker than both together.

> 两个机制复合：暴露于分歧提供新信息；去相关错误防止新信息被平均到错误答案中。单独任一比两者结合弱。

1. **Exposure to disagreement.** When an agent sees another agent's reasoning chain with a different conclusion, it has to either justify or update. Either way, the context for round r+1 is richer than round r.
   中文翻译：**暴露于分歧。** 当一个 Agent 看到另一个 Agent 具有不同结论的推理链时，它必须要么证明要么更新。无论哪种方式，第 r+1 轮的上下文都比第 r 轮更丰富。
2. **Correlated error reduction.** In self-consistency, all samples come from the same model, so the errors correlate — you average into a confidently wrong answer. Different models or different seeds decorrelate. Different *debated views* decorrelate further.
   中文翻译：**相关错误减少。** 在自我一致性中，所有样本来自同一个模型，所以错误相关——你平均得到一个自信的错误答案。不同的模型或不同的种子去相关。不同的*辩论观点*进一步去相关。

### Heterogeneous debate

A-HMAD and related follow-ups use *different base models* for different agents. Llama + Claude + GPT debating reduces monoculture collapse (Lesson 26) because the correlated errors of one model family are not shared by the others.

> A-HMAD 和相关后续工作为不同的 Agent 使用*不同的基础模型*。Llama + Claude + GPT 辩论减少了单一文化崩溃（Lesson 26），因为一个模型族的相关错误不被其他模型族共享。

The error-decorrelation argument is the same one behind ensemble methods in classical ML: diverse models fail differently, so voting is more reliable. The catch is that diversity is expensive (three API bills instead of one) and the gain saturates quickly past 3-4 model families.

> 错误去相关论点与经典 ML 中集成方法背后的相同：多样化模型以不同方式失败，因此投票更可靠。问题是多样性昂贵（三份 API 账单而不是一份）且收益在 3-4 个模型族之后快速饱和。

Downside: a weak model participating in a debate can drag the consensus toward its wrong answer (see "Should we be going MAD?", arXiv:2311.17371).

> 缺点：一个参与辩论的弱模型可以将共识拖向其错误答案（参见"我们应该走向 MAD 吗？"，arXiv:2311.17371）。

Heterogeneous debate is not free diversity. A weak model (say, a 7B parameter Llama) can outvote a strong model (GPT-4) if the strong model updates too aggressively toward the weak model's confident wrong answers. Calibrate which models participate.

> 异构辩论不是免费多样性。弱模型（如 7B 参数 Llama）可以否决强模型（GPT-4），如果强模型过于激进地向弱模型的自信错误答案更新。校准哪些模型参与。

### NLSOM — the 129-agent extension

Zhuge et al. ("Mindstorms in Natural Language-Based Societies of Mind," arXiv:2305.17066) scaled this idea to 129-member societies. The result: specialization and self-organization emerge with scale, and the system outperforms single-agent on tasks like visual question answering.

> Zhuge 等人（"基于自然语言的心智社会中的思维风暴"，arXiv:2305.17066）将这个想法扩展到 129 成员社会。结果：专业化和自组织随规模涌现，系统在视觉问答等任务上优于单 Agent。

The scaling result is striking: past ~50 agents, individual roles start specializing without being told to. Some become "researchers," others "critics," others "synthesizers." This is emergent role differentiation — the same phenomenon observed in human organizations, now happening in LLM societies.

> 扩展结果引人注目：超过约 50 个 Agent 后，个体角色开始在没有被告知的情况下专业化。一些变成"研究员"、其他"批评者"、其他"综合者"。这是涌现的角色分化——在人类组织中观察到的相同现象，现在发生在 LLM 社会中。

### Failure modes

- **Sycophancy cascade.** All agents defer to whichever agent sounds most confident. The debate collapses to the loudest voice. Prompting for adversarial roles ("one agent must argue the counter-position") helps.
  中文翻译：**谄媚级联。** 所有 Agent 屈从于听起来最自信的 Agent。辩论崩溃为最大的声音。对抗角色的提示（"一个 Agent 必须论证反方立场"）有帮助。
- **Topic drift.** Debates over many rounds drift from the original question. Mitigation: re-inject the question every round.
  中文翻译：**主题漂移。** 多轮辩论偏离原始问题。缓解措施：每轮重新注入问题。
- **Compute blowup.** N agents x R rounds = N*R LLM calls, each with a context that grows. A 5-agent, 5-round debate is 25 calls at growing context. Cost per question can exceed 10x a single CoT call.
  中文翻译：**计算爆炸。** N 个 Agent x R 轮 = N*R 次 LLM 调用，每次的上下文都在增长。5 个 Agent、5 轮的辩论是 25 次调用，上下文不断增长。每个问题的成本可能超过单次 CoT 调用的 10 倍。

## Build It | 动手实现

`code/main.py` runs a 3-agent x 3-round debate on a math question where each agent starts with a different (possibly wrong) answer. Agents are scripted — each "updates" by averaging the neighbors' answers weighted by a scripted confidence. Convergence is visible in the round-by-round log.

> `code/main.py` 在一个数学问题上运行 3 Agent x 3 轮辩论，每个 Agent 从一个不同（可能错误）的答案开始。Agent 是脚本化的——每个"更新"通过按脚本化置信度加权平均邻居答案。收敛在逐轮日志中可见。

The demo shows two key effects:

> 演示展示了两个关键效果：

- A single round of exchange moves agents closer to the correct answer.
  中文翻译：单轮交流将 Agent 移向正确答案。
- Extra rounds past round 2 show diminishing returns (matches Du et al.'s plateau).
  中文翻译：超过第 2 轮的额外轮数显示收益递减（匹配 Du 等人的平台）。

Run:

```
python3 code/main.py
```

## Use It | 用框架实现

`outputs/skill-debate-configurator.md` configures a debate for a new task: number of agents, number of rounds, heterogeneity (same model vs mixed), role assignment (symmetric vs one-adversarial). It also estimates the token cost before you run.

> `outputs/skill-debate-configurator.md` 为新任务配置辩论：Agent 数量、轮数、异构性（相同模型 vs 混合）、角色分配（对称 vs 一个对抗者）。它还在运行前估算 token 成本。

## Ship It | 产出物

If you ship debate:

> 如果你部署辩论系统：

- **Cap rounds at 3.** Du et al. show 3 rounds capture most of the gain. More is cost, not quality.
  中文翻译：**将轮数限制在 3。** Du 等人表明 3 轮捕获了大部分收益。更多是成本，不是质量。
- **Cap agents at 5.** Beyond 5, context bloat and cost dominate.
  中文翻译：**将 Agent 限制在 5。** 超过 5 个，上下文膨胀和成本占主导。
- **Heterogeneous by default.** At least two different base models in the pool.
  中文翻译：**默认异构。** 池中至少有两个不同的基础模型。
- **Adversarial slot.** One agent prompted to disagree regardless. Breaks sycophancy.
  中文翻译：**对抗角色。** 一个 Agent 被提示无论如何都要反对。打破谄媚。
- **Log every round.** Debate systems that hide intermediate rounds cannot be debugged or audited.
  中文翻译：**记录每轮。** 隐藏中间轮次的辩论系统无法调试或审计。

## Exercises | 练习题

1. Run `code/main.py`, then set the round count to 5 and watch diminishing returns. At which round does additional convergence stop?
   中文翻译：运行 `code/main.py`，然后将轮数设为 5 并观察收益递减。在哪一轮额外收敛停止？
2. Add a fourth agent with an adversarial role: always disagree with the current majority. Does this break or improve convergence?
   中文翻译：添加第四个具有对抗角色的 Agent：总是与当前多数不同意。这会破坏还是改善收敛？
3. Plot (print) the agreement score per round (fraction of agents on the majority answer). When does it hit 1.0 and is that equivalent to "correct"?
   中文翻译：绘制（打印）每轮的一致性分数（多数答案上的 Agent 比例）。它何时达到 1.0，这是否等同于"正确"？
4. Read Du et al. Section 4 ablations. Replicate the "agents-only" vs "rounds-only" vs "both" result using this code.
   中文翻译：阅读 Du 等人第 4 节消融实验。使用此代码复现"仅 Agent"vs"仅轮数"vs"两者结合"的结果。
5. Read "Should we be going MAD?" (arXiv:2311.17371) and list two debate variants beyond round-robin — e.g., judge-led, chain-of-debate, adversarial.
   中文翻译：阅读"我们应该走向 MAD 吗？"（arXiv:2311.17371）并列出两种轮询之外的辩论变体——例如，裁判主导、辩论链、对抗式。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Society of Mind / 心智社会 | "Minsky's idea" / "Minsky 的想法" | Intelligence as interacting specialists; 1986 framing now operationalized via LLM debate. / 智能作为交互的专家；1986 年的框架现在通过 LLM 辩论实现。 |
| Multi-agent debate / 多 Agent 辩论 | "Agents argue" / "Agent 争论" | N agents propose, critique each other, revise over R rounds, majority-vote. / N 个 Agent 提议、批评彼此、在 R 轮中修改、多数投票。 |
| Consensus / 共识 | "They agree" / "他们一致" | Not epistemic truth — just fraction-on-majority-answer. Can be confidently wrong. / 不是认识论真理——只是多数答案上的比例。可能自信地犯错。 |
| Rounds / 轮次 | "Exchange steps" / "交换步骤" | One round = each agent reads the others and updates once. / 一轮 = 每个 Agent 阅读其他 Agent 并更新一次。 |
| Heterogeneous debate / 异构辩论 | "Mix model families" / "混合模型族" | Using different base models to decorrelate errors. / 使用不同的基础模型来去相关错误。 |
| Sycophancy cascade / 谄媚级联 | "Everyone agrees with the loud one" / "每个人都同意最大声的" | Debate failure where agents defer to the most confident agent regardless of correctness. / 辩论失败，Agent 不顾正确性屈从于最自信的 Agent。 |
| NLSOM | "129-agent society" / "129 Agent 社会" | Natural-language society of mind; Zhuge et al.'s scaled version. / 自然语言心智社会；Zhuge 等人的扩展版本。 |
| Correlated error / 相关错误 | "Same model, same bug" / "相同模型，相同 bug" | Why self-consistency saturates; debate across different views decorrelates. / 自我一致性为什么饱和；不同观点的辩论去相关。 |

## Further Reading | 延伸阅读

- [Du et al. — Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325) — the reference paper, ICML 2024
  中文翻译：Du 等人 — 通过多 Agent 辩论改进语言模型的事实性和推理 — 参考论文，ICML 2024
- [Zhuge et al. — Mindstorms in Natural Language-Based Societies of Mind](https://arxiv.org/abs/2305.17066) — 129-agent NLSOM
  中文翻译：Zhuge 等人 — 基于自然语言的心智社会中的思维风暴 — 129 Agent NLSOM
- [Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs](https://arxiv.org/abs/2311.17371) — benchmarks debate variants
  中文翻译：我们应该走向 MAD 吗？多 Agent 辩论策略研究 — 辩论变体基准测试
- [Debate project page](https://composable-models.github.io/llm_debate/) — Du et al.'s code, demos, and ablation details
  中文翻译：辩论项目页面 — Du 等人的代码、演示和消融细节
