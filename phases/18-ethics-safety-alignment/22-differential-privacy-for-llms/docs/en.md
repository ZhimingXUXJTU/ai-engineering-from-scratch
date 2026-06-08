# Differential Privacy for LLMs | 差分隐私 LLM

> DP-SGD remains the standard — noise-injected gradient updates provide formal (epsilon, delta) guarantees. Overhead in compute, memory, and utility is substantial; parameter-efficient DP fine-tuning (LoRA + DP-SGD) is the common 2025 configuration (ACM 2025). Two bodies of evidence in tension: canary-based membership inference (Duan et al., 2024) reports limited success against language models; training-data extraction (Carlini et al., 2021; Nasr et al., 2025) recovers substantial verbatim memorization. Resolution (arXiv:2503.06808, March 2025): the gap is in what is measured — inserted canaries vs "most extractable" data. New canary designs enable loss-based MIA without shadow models and yield the first nontrivial DP audit of an LLM trained on real data with realistic DP guarantees. Alternatives: PMixED (arXiv:2403.15638) — private prediction at inference time via mixture of experts on next-token distributions; DP synthetic data generation (Google Research 2024). Emerging attack: Differential Privacy Reversal via LLM Feedback — confidence-score leakage.

> **【中文解读】** 本节介绍了 LLM 的差分隐私——在训练和推理中保护用户数据隐私的数学方法。DP-SGD 是标准方法——噪声注入梯度更新提供形式化的 (epsilon, delta) 保证。LoRA + DP-SGD 是 2025 年常见配置——全量 DP-SGD 训练前沿模型成本过高，LoRA 限制梯度更新到小型适配器。

> **【拓展：MIA vs 训练数据提取 → 衡量差距】** 2024-2025 年的两条证据线形成张力：金丝雀 MIA（Duan 等人 2024）报告对语言模型的成功有限；训练数据提取（Carlini 2021, Nasr 等人 2025）恢复大量逐字记忆。2025 年 3 月的解决方案：两者测量不同东西——MIA 问"示例 e 在 D 中吗？"，提取问"我能恢复 D 的什么？"——"最可提取的"示例才是隐私的关键。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, DP-SGD noise-injection and ε-δ accountant demonstration) | **语言:** Python（标准库，DP-SGD 噪声注入和 ε-δ 计数器演示）
**Prerequisites:** Phase 01 · 09 (information theory), Phase 10 · 01 (large-model training) | **前置知识:** Phase 01 · 09 (信息论), Phase 10 · 01 (大模型训练)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Learning Objectives | 学习目标

- Define (epsilon, delta)-differential privacy and state the DP-SGD recipe.
- Explain the 2024-2025 tension: canary MIA vs training-data extraction give different pictures.
- Describe PMixED and why inference-time private prediction is an alternative to DP training.
- Describe the Differential Privacy Reversal via LLM Feedback attack.

## The Problem | 问题

LLMs memorize. Carlini et al. 2021 showed production language models reproduce verbatim training text on demand. DP is the formal defense: train so that the output is provably insensitive to any single training example. The 2024-2025 evidence shows DP-SGD is necessary but the deployed ε values may not match the threat model.

## The Concept | 概念

> **【中文解读】** (epsilon, delta)-差分隐私定义：随机算法 M 是 (epsilon, delta)-DP 的，如果对于任何两个相差一个示例的数据集和任何事件 S：P(M(D) in S) <= e^epsilon * P(M(D') in S) + delta。解释：输出分布足够接近（由 epsilon 参数化），任何单个个体的贡献都不能被可靠推断，除了概率 delta。

### (ε, δ)-differential privacy

A randomized algorithm M is (ε, δ)-DP if for any two datasets differing in one example and any event S:
P(M(D) in S) <= e^ε * P(M(D') in S) + δ.

Interpretation: the output distribution is close enough (parametrized by ε) that the contribution of any single individual cannot be reliably inferred, except with probability δ.

### DP-SGD

Abadi et al. 2016. The standard recipe:
1. Sample a mini-batch.
2. Compute per-example gradients.
3. Clip each per-example gradient to a threshold C.
4. Sum the clipped gradients and add Gaussian noise with std σ * C.
5. Use the noisy sum to update parameters.

Privacy cost is tracked by an accountant (Moments Accountant, Rényi DP accountant). Reported ε values in the LLM literature vary widely by threat model, data sensitivity, and utility target; there is no universally "safe" default ε. Published examples span roughly ε ≈ 1–10 in some LLM training settings, but these are illustrative — not recommended defaults. Lower ε generally requires more noise and can increase utility loss.

### LoRA + DP-SGD

Full DP-SGD of a frontier model is prohibitive. LoRA (Hu et al. 2022) limits gradient updates to a small adapter, reducing per-example gradient storage. LoRA + DP-SGD is the common 2025 configuration. DP guarantees apply to the adapter; the base model is held fixed.

### The 2024-2025 tension

Two lines of evidence:

- **Canary MIA (Duan et al. 2024).** Insert unique canaries into training data, measure whether a membership-inference attacker can identify them. Reports limited success on language models. Suggests MIA is hard.
- **Training-data extraction (Carlini 2021, Nasr et al. 2025).** Prompt the model with a prefix; measure whether it recovers verbatim text from training. Reports substantial memorization. Suggests MIA is easy in the relevant sense.

March 2025 resolution (arXiv:2503.06808): the two measure different things. MIA asks "is example e in D?" on inserted canaries. Extraction asks "what can I recover of D?" The "most extractable" example is what matters for privacy; canaries under-report this because they are not optimized to be extractable.

New canary designs. Loss-based MIA without shadow models. First nontrivial DP audit of an LLM on real data with realistic DP guarantees.

> **【拓展：PMixED → 推理时隐私】** PMixED（arXiv:2403.15638）提供推理时私有预测：在 next-token 分布上的专家混合，每个专家看到训练数据的一个分片，聚合添加噪声以实现 DP。完全避免了 DP 训练。DP 合成数据生成（Google Research 2024）使用 DP-SGD 的 LoRA 微调采样合成数据，然后在合成数据上训练下游分类器。两者以不同的威胁模型为代价规避了全量 DP 训练的效用成本。

### Alternatives to DP training

- **PMixED (arXiv:2403.15638).** Private prediction at inference time. Mixture of experts on next-token distributions; each expert sees a shard of training data; aggregation adds noise for DP. Avoids DP training entirely.
- **DP synthetic data generation (Google Research 2024).** LoRA-fine-tune with DP-SGD, sample synthetic data, train a downstream classifier on the synthetic data.

Both sidestep the utility cost of full DP training at the cost of a different threat model.

> **【中文解读】** 差分隐私逆转攻击（2025）：使用 DP 训练模型的置信分数作为预言机重新识别个体。即使输出不泄露，置信分布也可能泄露。防御：不暴露置信度，或在暴露前截断/量化。这是 (epsilon, delta)-DP 训练之外的额外要求。

### Differential Privacy Reversal via LLM Feedback

Emerging 2025 attack. Use a DP-trained model's confidence scores as an oracle to re-identify individuals. Even when outputs do not leak, confidence distributions can.

The defense: do not expose confidences, or truncate/quantize them before exposure. This is an additional requirement beyond (ε, δ)-DP training.

### Where this fits in Phase 18

Lessons 20-21 are bias/fairness. Lesson 22 is privacy. Lesson 23 is provenance via watermarking. Lesson 27 covers the regulatory data-provenance layer.

> **【拓展：DP-SGD 的实际开销 → LoRA 解决方案】** 全量 DP-SGD 训练前沿模型在计算、内存和效用上代价巨大。LoRA（Hu 等人 2022）限制梯度更新到小型适配器，减少逐例梯度存储。LoRA + DP-SGD 是 2025 年常见配置——DP 保证适用于适配器，基础模型保持固定。这是实用性与隐私之间的工程权衡。

## Use It | 使用方法

`code/main.py` simulates DP-SGD on a toy binary-classification dataset. You can sweep the noise multiplier σ and the clipping norm C and track the (ε, δ) budget and the accuracy cost. A "canary attack" inserts a unique training example and measures whether a log-loss test can detect it before and after DP.

## Ship It | 部署上线

This lesson produces `outputs/skill-dp-audit.md`. Given a DP claim on a language model deployment, it audits: the (ε, δ) values, the accountant used, the MIA evaluation protocol, and whether confidence-exposure vectors have been assessed.

## Exercises | 练习题

1. Run `code/main.py`. Sweep σ in {0.5, 1.0, 2.0} and report the (ε, δ)-accuracy trade-off. Identify the point at which utility collapses.

2. Implement a canary insertion and a log-loss test. Measure detection rate before and after DP-SGD at σ = 1.0.

3. Read Nasr et al. 2025 on training-data extraction. Why does extraction success not collapse under moderate ε? What does this imply about MIA-as-evaluation?

4. Design a deployment using PMixED (arXiv:2403.15638) that operates entirely at inference time. What is the threat model that PMixED addresses that DP-SGD does not?

5. Sketch the DP Reversal via LLM Feedback attack. Design a countermeasure that limits confidence-score leakage and estimate its deployment cost.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| DP | "(ε, δ)-differential privacy" | Formal privacy: output distribution close under neighbouring-dataset change |
| DP-SGD | "noise-injected SGD" | Gradient clipping + Gaussian noise addition; standard DP training |
| LoRA + DP-SGD | "efficient private fine-tune" | DP-SGD on low-rank adapters; standard 2025 configuration |
| MIA | "membership inference" | Attack that determines whether an example was in training data |
| Canary | "inserted watermark example" | Unique training example used to measure DP leakage |
| PMixED | "private inference mixture" | Inference-time DP via mixture-of-experts on next-token distributions |
| DP Reversal | "confidence leakage attack" | Attack that uses a model's confidence as an oracle for re-identification |

## Further Reading | 延伸阅读

- [Abadi et al. — DP-SGD (arXiv:1607.00133)](https://arxiv.org/abs/1607.00133) — the standard DP training algorithm
- [Carlini et al. — Extracting Training Data (arXiv:2012.07805)](https://arxiv.org/abs/2012.07805) — the canonical extraction paper
- [Duan et al. — Canary MIA on LLMs (arXiv:2402.07841, 2024)](https://arxiv.org/abs/2402.07841) — limited-success MIA
- [Kowalczyk et al. — Auditing DP for LLMs (arXiv:2503.06808, March 2025)](https://arxiv.org/abs/2503.06808) — resolution of the tension
- [PMixED (arXiv:2403.15638)](https://arxiv.org/abs/2403.15638) — inference-time private prediction
