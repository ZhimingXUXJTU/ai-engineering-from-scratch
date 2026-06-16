# Flamingo and Gated Cross-Attention for Few-Shot VLMs | Flamingo 门控交叉注意力与少样本视觉语言模型

> DeepMind's Flamingo (2022) did two things before anyone else. It showed a single model could process arbitrarily interleaved sequences of images, videos, and text. And it showed VLMs could learn in-context — give a few-shot prompt with three example (image, caption) pairs and the model captions a new image without any gradient step. The mechanism: gated cross-attention layers, inserted between the frozen LLM's existing layers, with a learned tanh gate that starts at zero so the LLM's text capability is preserved at initialization. This lesson walks Flamingo's Perceiver resampler and gated cross-attention architecture — the ancestor of Gemini's interleaved inputs and Idefics2's visual tokens.

> **【中文解读】** Flamingo 首次实现图文交织输入和上下文少样本学习。核心是门控交叉注意力——在冻结 LLM 层间插入可学习的 tanh 门控层，初始值为零以保护文本能力。

> **【拓展：Flamingo→Gemini交织输入】** Flamingo 的图文交织处理模式是 Gemini 交织输入和 Idefics2 视觉 token 的原型，开创了多模态上下文学习的先河。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, gated cross-attention + Perceiver resampler demo) | **语言:** Python（标准库，门控交叉注意力 + Perceiver resampler 演示）
**Prerequisites:** Phase 12 · 03 (BLIP-2 Q-Former) | **前置知识:** Phase 12 · 03（BLIP-2 Q-Former）
**Time:** ~120 minutes | **时间:** ~120 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 12·03（BLIP-2 Q-Former，理解交叉注意力和 learnable query）；Phase 7（Transformer 残差结构）；Phase 11·05（In-context Learning 概念）。Flamingo 和 BLIP-2 最大的不同：BLIP-2 在 LLM 输入端桥接一次；Flamingo 在 LLM 每隔几层插入门控层。
> 💡 **【类比】** Flamingo 的门控交叉注意力 = "外科手术式的微创改造"。BLIP-2 = "在 LLM 大门口装一个翻译员"（输入端桥接一次）；Flamingo = "在 LLM 的每一层办公室里安一个窗口"（每 4 层一个门控交叉注意力）。门控初始为 0 = 窗口一开始是关的，模型行为和原 LLM 完全一样；训练慢慢开窗 = 视觉信息逐渐注入但不破坏原有文本能力。

## Learning Objectives | 学习目标

- Explain how gated cross-attention preserves a frozen LLM's text capability at initialization via tanh(gate) = 0.
  中文翻译：解释门控交叉注意力如何通过 tanh(gate) = 0 在初始化时保持冻结 LLM 的文本能力。
- Walk through a Perceiver resampler: N image patches → K fixed "latent" queries via cross-attention.
  中文翻译：梳理 Perceiver resampler：N 个图像 patch → 通过交叉注意力产生 K 个固定"潜在"查询。
- Describe how Flamingo handles interleaved image-text sequences with causal masking that respects image placement.
  中文翻译：描述 Flamingo 如何用尊重图像位置的因果掩码处理交织的图文序列。
- Reproduce a few-shot multimodal prompt structure (3 image-caption examples then a query image).
  中文翻译：复现少样本多模态提示结构（3 个图文示例后跟一个查询图像）。

## The Problem | 问题引入

BLIP-2 feeds 32 visual tokens into a frozen LLM's input layer. Works for one image per prompt. But what if you want to feed *many* images interleaved with text, as in "here is image A, caption it; here is image B, caption it; now here is image C, caption it"? The LLM's self-attention would need to handle image tokens and text tokens in a single stream, and the question of which positions can attend to which images gets fussy.

> BLIP-2 将 32 个视觉 token 喂入冻结 LLM 的输入层。适用于每个提示一张图像。但如果你想喂入与文本交织的*多张*图像呢，比如"这是图像 A，描述它；这是图像 B，描述它；现在这是图像 C，描述它"？LLM 的自注意力需要在单个流中处理图像 token 和文本 token，哪些位置可以关注哪些图像的问题变得棘手。

Flamingo's answer: do not change the LLM's input stream at all. Insert extra cross-attention layers between existing LLM blocks. Text tokens still flow through the LLM's causal self-attention as always. Between every few LLM blocks, text tokens also cross-attend to image features via a new gated layer. The gate (initialized to zero) means at step zero the new layers are no-ops — the model behaves exactly like the pretrained LLM. As training progresses the gate opens and visual information starts flowing.

> Flamingo 的答案：完全不改变 LLM 的输入流。在现有 LLM 块之间插入额外的交叉注意力层。文本 token 像往常一样流过 LLM 的因果自注意力。每隔几个 LLM 块，文本 token 还通过新的门控层交叉关注图像特征。门控（初始化为零）意味着在第零步新层是空操作——模型行为完全像预训练的 LLM。随着训练进行门控逐渐打开，视觉信息开始流入。

The second question Flamingo answered: how do you handle a variable number of images (0, 1, or many) per prompt? A Perceiver resampler — a small cross-attention module that takes whatever number of patches you have and produces a fixed number of visual latent tokens. The LLM cross-attention layer sees the same shape regardless of how many images are in the prompt.

> Flamingo 回答的第二个问题：如何处理每个提示中可变数量的图像（0、1 或多张）？Perceiver resampler——一个小型交叉注意力模块，接收任意数量的 patch 并产生固定数量的视觉潜在 token。无论提示中有多少图像，LLM 交叉注意力层看到的形状都相同。

## The Concept | 核心概念

> **【中文解读】** Flamingo（DeepMind）引入门控交叉注意力（Gated Cross-Attention），在冻结的 LLM 层之间插入可训练的交叉注意力层来注入视觉信息。门控机制控制视觉信息的流入量，初始化时门控值为 0（视觉信息不流入），训练过程中逐渐开放。

> **【拓展：Flamingo 的高效适配】** Flamingo 仅训练约 1% 的参数（门控交叉注意力层），就能在 few-shot 视觉推理任务上达到 SOTA。这种"冻结预训练模型 + 轻量适配层"的范式后来被 LLaVA、Qwen-VL 等模型继承。Flamingo-80B 在 few-shot VQA 上超越了当时全量微调的方法。


> **【拓展：门控机制的数学原理】** 门控交叉注意力的门控值初始化为 0，意味着训练开始时视觉信息完全不流入 LLM。随着训练进行，门控逐渐开放。这防止了训练初期视觉噪声干扰 LLM 的语言能力。这种零初始化门控技巧后来被 LLaVA 等模型借鉴用于投影层。


### The frozen LLM

Flamingo starts with a frozen Chinchilla 70B LLM. All 70B weights untouched. The existing text self-attention and FFN operate normally.

> Flamingo 以冻结的 Chinchilla 70B LLM 为起点。所有 700 亿权重不触碰。现有的文本自注意力和 FFN 正常运行。

### Perceiver resampler

For each image in the prompt, the ViT produces N patch tokens. The Perceiver resampler has K fixed learnable latents (Flamingo uses K=64). Each resampler block is two sub-steps:

> 对于提示中的每张图像，ViT 产生 N 个 patch token。Perceiver resampler 有 K 个固定的可学习潜在向量（Flamingo 使用 K=64）。每个 resampler 块有两个子步骤：

> 🤔 **【困惑】** Q: Perceiver resampler 和 BLIP-2 的 Q-Former 有什么区别？A: 思想几乎一样（learnable query 从 patch 提取信息），但 Flamingo 的 Perceiver resampler 只做视觉特征压缩、不参与对比损失训练；Q-Former 是 transformer 结构且有 ITC/ITM/ITG 三个损失。可以认为 Perceiver resampler 是 Q-Former 的简化版。

1. Cross-attention: the K latents attend over the N patch tokens (Q from latents, K/V from patches).
   中文翻译：交叉注意力：K 个潜在向量关注 N 个 patch token（Q 来自潜在向量，K/V 来自 patch）。
2. Self-attention + FFN within the latents.
   中文翻译：潜在向量内部的自注意力 + FFN。

After 6 resampler blocks, the output is K=64 visual tokens of dim 1024, regardless of how many patches the ViT produced. A 224x224 image (196 patches) and a 480x480 image (900 patches) both exit as 64 resampler tokens.

> 经过 6 个 resampler 块后，输出是 K=64 个维度为 1024 的视觉 token，无论 ViT 产生了多少 patch。224x224 的图像（196 个 patch）和 480x480 的图像（900 个 patch）都输出为 64 个 resampler token。

For video, the resampler is applied temporally: each frame's patches produce 64 latents, and a temporal positional encoding lets the model distinguish t=0 from t=N. The full video becomes T * 64 visual tokens.

> 对于视频，resampler 按时间维度应用：每帧的 patch 产生 64 个潜在向量，时间位置编码让模型区分 t=0 和 t=N。完整视频变成 T * 64 个视觉 token。

### Gated cross-attention

Between every M layers of the frozen LLM (Flamingo uses M=4), insert a new gated cross-attention block:

> 在冻结 LLM 的每 M 层之间（Flamingo 使用 M=4），插入一个新的门控交叉注意力块：

```
x_after_llm_block = llm_block(x_before)
cross = cross_attn(x_after, resampler_output)
gated = tanh(alpha) * cross + x_after
x_before_next_block = gated
```

- `alpha` is a learnable scalar initialized to zero.
  中文翻译：`alpha` 是一个可学习的标量，初始化为零。
- `tanh(0) = 0`, so at init the gated branch contributes zero.
  中文翻译：`tanh(0) = 0`，所以初始化时门控分支贡献为零。
- As `alpha` moves away from zero, the cross-attention contribution grows smoothly.
  中文翻译：随着 `alpha` 远离零，交叉注意力的贡献平滑增长。
- The residual connection means even a fully-open gate does not overwrite the LLM's text representation; it just adds visual information on top.
  中文翻译：残差连接意味着即使门控完全打开，也不会覆盖 LLM 的文本表示；它只是在上面添加视觉信息。

This is the single most important design choice in Flamingo: visual conditioning is additive, gated, and zero at initialization. A Flamingo at step 0 is a perfect Chinchilla 70B on text-only inputs.

> 这是 Flamingo 中最重要的设计选择：视觉条件是可加的、门控的、初始化为零。第 0 步的 Flamingo 在纯文本输入上就是完美的 Chinchilla 70B。

> ⚠️ **【易错点】** 自己实现时忘记初始化 alpha=0，直接随机初始化 → 训练前几步 LLM 文本能力就会崩塌。原因：未训练的交叉注意力输出是噪声，混入 LLM 内部表示会破坏文本知识。修复：alpha 必须初始化为 0，让模型从"完美 LLM"出发，缓慢学习。
> 💡 **【类比】** 零初始化门控 = "新员工入职模式"。新员工（视觉层）第一周只观察、不说话（gate=0）；熟悉业务后逐渐发言（gate 慢慢打开）。直接让新员工主导决策（gate≠0 初始化）会扰乱团队原有节奏（破坏 LLM 文本能力）。

### Masked cross-attention for interleaved inputs

In a prompt like "<image A> caption A <image B> caption B <image C> ?", each text token should only see images that came before it in the sequence. The cross-attention mask enforces: text token at position `t` attends only to image resampler tokens whose image index `i < i_t` where `i_t` is the most recent image before position `t`. "Sees only the last preceding image" or "sees all preceding images" are both valid choices; Flamingo chose the former.

> 在类似"<图像 A> 描述 A <图像 B> 描述 B <图像 C> ?"的提示中，每个文本 token 只应看到序列中位于它之前的图像。交叉注意力掩码强制：位置 `t` 的文本 token 只关注图像索引 `i < i_t` 的图像 resampler token，其中 `i_t` 是位置 `t` 之前最近的图像。"只看最近的图像"或"看所有之前的图像"都是有效选择；Flamingo 选择了前者。

### In-context few-shot learning

A Flamingo prompt looks like:

> Flamingo 提示看起来像这样：

```
<image1> A photo of a cat. <image2> A photo of a dog. <image3> A photo of a
```

The model sees the completion pattern and outputs "bird" (or whatever image3 shows). No gradient steps. The frozen LLM's in-context learning capability carries through the gated cross-attention — this is the punchline of the paper and why it matters.

> 模型看到补全模式并输出"bird"（或 image3 显示的任何内容）。无需梯度步骤。冻结 LLM 的上下文学习能力通过门控交叉注意力传递——这是论文的关键点，也是它重要的原因。

> 🤔 **【困惑】** Q: 为什么 Flamingo 能 in-context learn 而 BLIP-2 不能？A: Flamingo 在 LLM 每隔 4 层注入视觉信息，LLM 内部的 in-context learning（在 Phase 11·05 学过）依然完整工作；BLIP-2 把 32 个视觉 token 直接拼到 prompt 前面，LLM 把它们当普通 token 处理，但训练目标里没有显式的 few-shot 模式，所以能力弱。

### Training data

Flamingo trained on three datasets:

> Flamingo 在三个数据集上训练：

1. MultiModal MassiveWeb (M3W): 43M web pages with interleaved images and text, reconstructing reading order.
   中文翻译：多模态 MassiveWeb（M3W）：4300 万个包含交织图像和文本的网页，重建阅读顺序。
2. Image-Text Pairs (ALIGN + LTIP): 4.4B pairs.
   中文翻译：图文对（ALIGN + LTIP）：44 亿对。
3. Video-Text Pairs (VTP): 27M short video clips.
   中文翻译：视频-文本对（VTP）：2700 万个短视频片段。

OBELICS (2023) is an open reproduction of the interleaved web corpus, which Idefics, Idefics2, and most open "Flamingo-like" models train on.

> OBELICS（2023）是交织网络语料库的开放复现，Idefics、Idefics2 和大多数开放的"类 Flamingo"模型在其上训练。

### OpenFlamingo and Otter

OpenFlamingo (2023) is the open reproduction. Architecture identical (Perceiver resampler + gated cross-attention on frozen LLaMA or MPT). Checkpoints at 3B, 4B, 9B. Quality lags Flamingo due to smaller base LLM and less data.

> OpenFlamingo（2023）是开放复现。架构相同（Perceiver resampler + 冻结 LLaMA 或 MPT 上的门控交叉注意力）。3B、4B、9B 检查点。由于基础 LLM 更小和数据更少，质量落后于 Flamingo。

Otter (2023) builds on OpenFlamingo with instruction tuning on MIMIC-IT (a dataset of multimodal instructions), showing gated cross-attention works for instruction following too.

> Otter（2023）在 OpenFlamingo 基础上用 MIMIC-IT（多模态指令数据集）进行指令微调，证明门控交叉注意力也适用于指令遵循。

### The descendants

- Idefics / Idefics2 / Idefics3: Hugging Face's gated cross-attention lineage, progressively simpler (Idefics2 dropped the resampler in favor of direct patch tokens with adaptive pooling).
  中文翻译：Idefics / Idefics2 / Idefics3：Hugging Face 的门控交叉注意力谱系，逐步简化（Idefics2 去掉了 resampler，改用自适应池化的直接 patch token）。
- Flamingo-to-Chameleon transition: by 2024 many teams moved to early-fusion (Lesson 12.11); Flamingo-style gated cross-attention remains in production where backbone freezing is required.
  中文翻译：Flamingo 到 Chameleon 的过渡：到 2024 年许多团队转向早期融合（第 12.11 课）；Flamingo 风格的门控交叉注意力在需要冻结主干网络的场景仍在生产中使用。
- Gemini's interleaved input: conceptually inherits Flamingo's interleaved-format flexibility, though the exact mechanism is proprietary.
  中文翻译：Gemini 的交织输入：概念上继承了 Flamingo 的交织格式灵活性，尽管具体机制是专有的。

### Comparison to BLIP-2

| | BLIP-2 | Flamingo |
|---|---|---|
| / | BLIP-2 | Flamingo |
| Visual bridge | Q-Former once at input | Gated cross-attention at every M layers |
| 视觉桥接 | 输入层一次 Q-Former | 每 M 层一次门控交叉注意力 |
| Visual tokens | 32 per image | 64 per image per cross-attn layer |
| 视觉 token | 每图 32 个 | 每个交叉注意力层每图 64 个 |
| Frozen LLM | Yes | Yes |
| 冻结 LLM | 是 | 是 |
| Few-shot in-context | Weak | Strong — the paper's centerpiece |
| 少样本上下文学习 | 弱 | 强——论文的核心亮点 |
| Interleaved inputs | No native support | Yes, the design target |
| 交织输入 | 无原生支持 | 是，设计目标 |
| Training data | 130M pairs | 1.3B pairs + 43M interleaved pages |
| 训练数据 | 1.3 亿对 | 13 亿对 + 4300 万交织网页 |
| Parameter count | 188M trained | ~10B trained (cross-attn layers) |
| 参数量 | 训练 1.88 亿 | 训练约 100 亿（交叉注意力层） |
| Compute | Days on 8 A100s | Weeks on thousands of TPUv4 |
| 计算量 | 8 块 A100 数天 | 数千块 TPUv4 数周 |

Pick BLIP-2 for single-image VQA on a budget. Pick Flamingo/Idefics2 for interleaved, few-shot, or multi-image reasoning.

> 预算有限的单图像 VQA 选 BLIP-2。交织、少样本或多图像推理选 Flamingo/Idefics2。

## Use It | 用框架实现

`code/main.py` demonstrates:

> `code/main.py` 演示了：

1. A Perceiver resampler on 36 fake patch tokens with 8 learnable latents (pure Python cross-attention).
   中文翻译：对 36 个假 patch token 的 Perceiver resampler，使用 8 个可学习潜在向量（纯 Python 交叉注意力）。
2. A gated cross-attention step with `alpha = 0` → output equals input (LLM unchanged), then `alpha = 2.0` → visual contribution mixed in.
   中文翻译：门控交叉注意力步骤，`alpha = 0` → 输出等于输入（LLM 不变），然后 `alpha = 2.0` → 视觉贡献混入。
3. An interleaved-mask builder that produces the 2D attention mask for a "(image 1) (text 1) (image 2) (text 2)" sequence.
   中文翻译：交织掩码构建器，为"(图像 1) (文本 1) (图像 2) (文本 2)"序列生成 2D 注意力掩码。

## Ship It | 产出物

This lesson produces `outputs/skill-gated-bridge-diagnostic.md`. Given an open VLM's config (resampler Y/N, cross-attn frequency, gate scheme), it identifies the Flamingo lineage elements and explains the freezing strategy. Useful for debugging why a fine-tune degraded text performance (answer: the gate got too wide too fast).

> 本课产出 `outputs/skill-gated-bridge-diagnostic.md`。给定开放 VLM 的配置（是否有 resampler、交叉注意力频率、门控方案），它识别 Flamingo 血统元素并解释冻结策略。有助于调试为什么微调后文本性能退化（答案：门控开得太快太大）。

## Exercises | 练习题

1. Compute Flamingo-9B's visual parameter count: 9B LLM + 1.4B gated cross-attention layers + 64M resampler. What fraction of total params is trained?
   中文翻译：计算 Flamingo-9B 的视觉参数量：9B LLM + 14 亿门控交叉注意力层 + 6400 万 resampler。训练的参数占总参数的比例是多少？

2. Implement the gated residual `y = tanh(alpha) * cross + x` in PyTorch. Show experimentally that with `alpha=0`, `y==x` exactly at init.
   中文翻译：用 PyTorch 实现门控残差 `y = tanh(alpha) * cross + x`。实验证明 `alpha=0` 时 `y==x` 精确成立。

3. Read OpenFlamingo Section 3.2 (arXiv:2308.01390) on how they handle multiple images in a batch when each prompt has a different image count. Describe the padding strategy.
   中文翻译：阅读 OpenFlamingo 第 3.2 节（arXiv:2308.01390）关于如何处理批次中每个提示图像数量不同的情况。描述填充策略。

4. Why does Flamingo's cross-attention mask let a text token attend to *only the most recent* preceding image rather than all preceding images? Read the Flamingo paper Section 2.4 and explain the tradeoff.
   中文翻译：为什么 Flamingo 的交叉注意力掩码让文本 token 只关注*最近的*前一张图像而非所有前序图像？阅读 Flamingo 论文第 2.4 节并解释权衡。

5. In-context few-shot: construct a prompt with 4 examples of "image → color of main object" for a new Flamingo variant. Describe the expected accuracy pattern as you vary the number of examples from 0 to 8.
   中文翻译：上下文少样本：构建包含 4 个"图像 → 主要对象颜色"示例的提示。描述示例数从 0 变到 8 时预期的准确率模式。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Perceiver resampler | "Fixed-latent cross-attention" | Module that produces K fixed tokens from a variable number of input patches | 从可变数量输入 patch 产生 K 个固定 token 的模块 |
| Gated cross-attention | "Tanh-gated bridge" | Residual layer `y = tanh(alpha)*cross + x`, learnable alpha, init 0 | 残差层 `y = tanh(alpha)*cross + x`，可学习 alpha，初始化为 0 |
| Interleaved input | "Mixed sequence" | Prompt format with images and text mixed freely in reading order | 图像和文本按阅读顺序自由混合的提示格式 |
| Frozen LLM | "No LLM gradients" | The text LLM's weights do not update; only resampler + cross-attn layers train | 文本 LLM 权重不更新；仅 resampler + 交叉注意力层训练 |
| Few-shot | "In-context examples" | Give a few (image, answer) pairs in the prompt; model generalizes without finetuning | 在提示中给几个（图像，答案）对；模型无需微调即可泛化 |
| OBELICS | "Interleaved web corpus" | Open dataset of 141M web pages with images and text in reading order | 1.41 亿网页的开放数据集，包含按阅读顺序排列的图像和文本 |
| Chinchilla | "70B frozen base" | Flamingo's frozen text LLM, from DeepMind's Chinchilla paper | Flamingo 的冻结文本 LLM，来自 DeepMind 的 Chinchilla 论文 |
| Gate schedule | "How alpha moves" | The rate at which the cross-attention gate opens during training | 训练过程中交叉注意力门控打开的速率 |
| Cross-attn frequency | "Every M layers" | How often a gated cross-attention block is inserted; Flamingo uses M=4 | 门控交叉注意力块插入的频率；Flamingo 使用 M=4 |
| OpenFlamingo | "Open reproduction" | MosaicML/LAION open checkpoint at 3-9B; architecture-identical to Flamingo | MosaicML/LAION 的 3-9B 开放检查点；架构与 Flamingo 相同 |

## Further Reading | 延伸阅读

- [Alayrac et al. — Flamingo (arXiv:2204.14198)](https://arxiv.org/abs/2204.14198) — the original paper.
  中文翻译：Flamingo 原始论文。
- [Awadalla et al. — OpenFlamingo (arXiv:2308.01390)](https://arxiv.org/abs/2308.01390) — open reproduction.
  中文翻译：开放复现。
- [Laurençon et al. — OBELICS (arXiv:2306.16527)](https://arxiv.org/abs/2306.16527) — interleaved web corpus.
  中文翻译：交织网络语料库。
- [Jaegle et al. — Perceiver IO (arXiv:2107.14795)](https://arxiv.org/abs/2107.14795) — the general Perceiver architecture.
  中文翻译：通用 Perceiver 架构。
- [Li et al. — Otter (arXiv:2305.03726)](https://arxiv.org/abs/2305.03726) — instruction-tuned Flamingo descendant.
  中文翻译：指令微调的 Flamingo 后代。
- [Laurençon et al. — Idefics2 (arXiv:2405.02246)](https://arxiv.org/abs/2405.02246) — modern simplification of the Flamingo approach.
  中文翻译：Flamingo 方法的现代化简化。
