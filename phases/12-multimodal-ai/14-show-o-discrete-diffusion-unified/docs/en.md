# Show-o and Discrete-Diffusion Unified Models | Show-o 离散扩散统一模型

> Transfusion mixes continuous and discrete representations. Show-o (Xie et al., August 2024) goes the other way: text tokens use causal next-token prediction, image tokens use masked discrete diffusion in the spirit of MaskGIT. Both sit inside one transformer with a hybrid attention mask. The result unifies VQA, text-to-image, inpainting, and mixed-modality generation on one backbone, one tokenizer per modality, one loss formulation (next-token extended to masked prediction). This lesson walks the Show-o design — why masked discrete diffusion is a parallel, few-step image generator — and contrasts with Transfusion and Emu3.

> **【中文解读】** Show-o（2024年8月）走另一条路：文本 token 用因果下一 token 预测，图像 token 用掩码离散扩散（MaskGIT 风格）。两者共用一个 Transformer，用混合注意力掩码。结果是一个 checkpoint 同时支持 VQA、文本生成图像和图像修复。

> **【拓展：并行解码的速度优势】** Show-o 生成图像只需约 16 步（每步并行预测所有掩码 token），而 Chameleon/Emu3 需要 1024-4096 步（逐 token 自回归）。这使得 Show-o 在统一生成模型中速度最快，但图像质量受限于 VQ tokenizer 的重建天花板。

**Type:** Learn  | **类型:** 学习
**Languages:** Python (stdlib, masked-discrete-diffusion sampler) | **语言:** Python（标准库，掩码离散扩散采样器）
**Prerequisites:** Phase 12 · 13 (Transfusion) | **前置知识:** Phase 12 · 13（Transfusion）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Learning Objectives  | 学习目标

- Explain masked discrete diffusion: the schedule that masks tokens uniformly then asks the transformer to recover them.
  > 解释掩码离散扩散：均匀掩码 token 然后让 Transformer 恢复它们的调度。
- Compare parallel image decoding (Show-o, MaskGIT) to autoregressive image decoding (Chameleon, Emu3) on speed and quality.
  > 比较并行图像解码（Show-o、MaskGIT）与自回归图像解码（Chameleon、Emu3）在速度和质量上的差异。
- Name the three tasks Show-o handles in one checkpoint: T2I, VQA, image inpainting.
  > 列举 Show-o 在一个 checkpoint 中支持的三种任务：T2I、VQA、图像修复。
- Pick a masking schedule (cosine, linear, truncated) and reason about its effect on sample quality.
  > 选择掩码调度（余弦、线性、截断）并分析其对采样质量的影响。

## The Problem  | 问题背景

Transfusion's two-loss training works but has trickier dynamics — the continuous diffusion loss lives on a different numerical scale from the discrete NTP loss. Balancing loss weights is a hyperparameter search. The architecture is effective but complex.

> Transfusion 的双损失训练可行但动态更复杂——连续扩散损失与离散 NTP 损失在数值尺度上不同。平衡损失权重是一个超参数搜索。架构有效但复杂。

Show-o's answer: keep both modalities discrete (like Chameleon), but generate images in parallel via masked discrete diffusion instead of sequentially. The training objective becomes a single masked-token-prediction that generalizes next-token-prediction naturally.

> Show-o 的答案：保持两种模态都是离散的（像 Chameleon），但通过掩码离散扩散并行生成图像，而非顺序生成。训练目标变成单一的掩码 token 预测，自然泛化了下一 token 预测。

## The Concept  | 核心概念

> **【中文解读】** Show-o 统一多模态理解和生成，使用离散扩散替代传统连续扩散。离散扩散直接在 token 级别操作，将遮罩预测（理解任务）和去噪（生成任务）统一在同一框架下。

> **【拓展：离散扩散的统一优势】** 离散扩散将文本生成和图像生成统一到同一个数学框架（掩码 token 预测），使多模态联合训练更简单。这是 2025 年多模态 AI 的趋势方向。


### Masked discrete diffusion (MaskGIT)

The original Chang et al. (2022) MaskGIT trick is elegant. Start from a fully-masked image (every token is the special `<MASK>` id). At each step, predict all masked tokens in parallel, then keep the top-K most confident predictions and re-mask the rest. After ~8-16 iterations, all tokens are filled in. The schedule of how many tokens to unmask per step is tuned — cosine schedules work well.

> 原始的 Chang 等人（2022）MaskGIT 技巧很优雅。从完全掩码的图像开始（每个 token 都是特殊的 `<MASK>` ID）。每步并行预测所有掩码 token，然后保留 top-K 最有信心的预测并重新掩码其余的。经过约 8-16 次迭代，所有 token 都被填充。每步解掩码多少 token 的调度需要调优——余弦调度效果好。

Training is simple: sample a masking ratio uniformly from [0, 1], apply it to the image's VQ tokens, train the transformer to recover the masked ones. Exactly what BERT did for text, scaled to image generation.

> 训练很简单：从 [0, 1] 均匀采样掩码比例，应用到图像的 VQ token，训练 Transformer 恢复被掩码的 token。就是 BERT 对文本做的，扩展到图像生成。

### Show-o: one transformer, hybrid mask

Show-o puts MaskGIT inside a causal-language-model transformer. The attention mask is:

> Show-o 将 MaskGIT 放入因果语言模型 Transformer 中。注意力掩码是：

- Text tokens: causal (standard LLM).
  中文翻译：文本 token：因果（标准 LLM）。
- Image tokens: full bidirectional within the image block (so the masked tokens can see every other image token during prediction).
  中文翻译：图像 token：图像块内全双向（掩码 token 可以在预测时看到其他所有图像 token）。
- Text-to-image: text attends to prior images, image attends to prior text.
  中文翻译：文本到图像：文本关注之前的图像，图像关注之前的文本。

Training alternates between:
1. Standard NTP on text sequences.
   中文翻译：文本序列上的标准 NTP。
2. T2I samples: text → image with masked image tokens, masked-token-prediction loss.
   中文翻译：T2I 样本：文本→带掩码图像 token 的图像，掩码 token 预测损失。
3. VQA samples: image → text with masked text tokens (really just NTP).
   中文翻译：VQA 样本：图像→带掩码文本 token 的文本（实际上就是 NTP）。

The unified loss is cross-entropy on `<MASK>` tokens, which covers both text NTP (only the last token is "masked") and image masked-diffusion (random subset is masked).

> 统一损失是 `<MASK>` token 上的交叉熵，同时覆盖文本 NTP（只有最后一个 token 是"掩码"的）和图像掩码扩散（随机子集被掩码）。

### Parallel sampling

Show-o generates an image in ~16 steps instead of ~1000 (autoregressive per token) or ~20 (diffusion). At each step, predict all masked tokens in parallel; commit the top-K confident; repeat.

> Show-o 在约 16 步内生成图像，而非约 1000 步（逐 token 自回归）或约 20 步（扩散）。每步并行预测所有掩码 token；提交 top-K 有信心的；重复。

Compare:
- Chameleon / Emu3 (autoregressive over tokens): N_tokens forward passes, typically 1024-4096 per image.
  中文翻译：Chameleon / Emu3（逐 token 自回归）：N_tokens 次前向传播，通常每张图像 1024-4096。
- Transfusion (continuous diffusion): ~20 steps, each a full transformer pass.
  中文翻译：Transfusion（连续扩散）：约 20 步，每步一次完整 Transformer 传播。
- Show-o (masked discrete diffusion): ~16 steps, each a full transformer pass.
  中文翻译：Show-o（掩码离散扩散）：约 16 步，每步一次完整 Transformer 传播。

Show-o is faster than Chameleon at similar-scale models, roughly matches Transfusion step count with lower per-step cost (discrete vocab logits vs continuous MSE loss).

> Show-o 在相似规模模型上比 Chameleon 更快，步数大致匹配 Transfusion，但每步成本更低（离散词汇表 logits vs 连续 MSE 损失）。

### Tasks in one checkpoint

Show-o supports four tasks at inference, selected by prompt format:

> Show-o 在推理时支持四个任务，通过提示格式选择：

- Text generation: standard autoregressive text output.
  中文翻译：文本生成：标准自回归文本输出。
- VQA: image in, text out.
  中文翻译：VQA：图像输入，文本输出。
- T2I: text in, image out via masked discrete diffusion.
  中文翻译：T2I：文本输入，通过掩码离散扩散输出图像。
- Inpainting: image with some tokens masked, fill in.
  中文翻译：图像修复：带部分掩码 token 的图像，填充缺失部分。

The inpainting capability comes for free from the masked-prediction training. Mask a region of the VQ-token grid, feed the rest plus a text prompt, predict the masked tokens.

> 图像修复能力从掩码预测训练中免费获得。掩码 VQ token 网格的一个区域，喂入其余部分加上文本提示，预测被掩码的 token。

### Masking schedule

The schedule of how many tokens to unmask per step shapes quality. Show-o recommends cosine:

> 每步解掩码多少 token 的调度影响质量。Show-o 推荐余弦调度：

```
mask_ratio(t) = cos(pi * t / (2 * T))   # t = 0..T
```

At step 0, all tokens masked (ratio 1.0). At step T, none masked. Cosine concentrates mass on mid-range ratios where prediction is most informative. Linear schedules also work but plateau faster.

> 第 0 步，所有 token 被掩码（比例 1.0）。第 T 步，无掩码。余弦调度将质量集中在中程比例上，此时预测信息量最大。线性调度也可用但更早饱和。

### Show-o2

Show-o2 (2025 follow-up, arXiv 2506.15564) scales Show-o: larger LLM base, better tokenizer, improved mask schedule. Same architectural pattern.

### Where Show-o sits

In the 2026 taxonomy:

> 在 2026 年的分类中：

- Discrete tokens + NTP: Chameleon, Emu3. Simple but slow inference.
  中文翻译：离散 token + NTP：Chameleon、Emu3。简单但推理慢。
- Discrete tokens + masked diffusion: Show-o, MaskGIT, LlamaGen, Muse. Parallel sampling, still lossy by tokenizer.
  中文翻译：离散 token + 掩码扩散：Show-o、MaskGIT、LlamaGen、Muse。并行采样，仍受分词器损失限制。
- Continuous + diffusion: Transfusion, MMDiT, DiT. Highest quality, more complex training.
  中文翻译：连续 + 扩散：Transfusion、MMDiT、DiT。最高质量，训练更复杂。
- Continuous + flow matching in a VLM: JanusFlow, InternVL-U. Newest.
  中文翻译：VLM 中连续 + 流匹配：JanusFlow、InternVL-U。最新。

Pick by task: Show-o when you want T2I + inpainting + VQA in one open model with reasonable speed; Transfusion when quality is paramount and you can afford the two-loss plumbing.

> 按任务选择：需要一个开放模型同时做 T2I + 修复 + VQA 且速度合理时选 Show-o；质量至上且能承担双损失复杂性时选 Transfusion。


> **【拓展：Show-o 的离散扩散方法】** Show-o 的离散扩散使用掩码预测：随机遮盖部分 token，模型预测被遮盖的 token。理解任务遮盖答案部分，生成任务从全遮盖开始逐步去噪。数学上等价于多项式扩散。


## Use It  | 动手实践

`code/main.py` simulates Show-o sampling:

> `code/main.py` 模拟 Show-o 采样：

- A toy grid of 16 VQ tokens.
  中文翻译：一个 16 个 VQ token 的玩具网格。
- A mock "transformer" that predicts logits based on a prompt and the currently-unmasked tokens.
  中文翻译：一个模拟"Transformer"，基于提示和当前未掩码 token 预测 logits。
- Parallel masked sampling over 8 steps with cosine schedule.
  中文翻译：余弦调度下的 8 步并行掩码采样。
- Prints the intermediate states (mask pattern evolution) and the final tokens.
  中文翻译：打印中间状态（掩码模式演化）和最终 token。

Run it, watch the mask dissolve step by step.

> 运行它，观察掩码逐步消解。

## Ship It  | 部署上线

This lesson produces `outputs/skill-unified-gen-model-picker.md`. Given a product that needs both understanding (VQA, captioning) and generation (T2I, inpainting) with an open-weights constraint, picks between Show-o family, Transfusion/MMDiT family, and Emu3 / Chameleon family with concrete trade-offs.

> 本课产出 `outputs/skill-unified-gen-model-picker.md`。给定需要理解（VQA、描述）和生成（T2I、修复）且受限开放权重的产品，在 Show-o、Transfusion/MMDiT 和 Emu3/Chameleon 家族之间选择，附具体权衡。

## Exercises  | 练习题

1. Masked discrete diffusion samples in ~16 steps. Why not 1? What breaks if you unmask everything at step 0?
   中文翻译：掩码离散扩散在约 16 步内采样。为什么不是 1 步？如果在第 0 步解掩码所有 token 会怎样？

2. Inpainting is free with masked diffusion. Propose a product use case (real or hypothetical) where Show-o's inpainting beats a specialist model.
   中文翻译：掩码扩散的图像修复是免费的。提出一个 Show-o 修复能力胜过专业模型的产品用例。

3. Cosine schedule vs linear schedule: trace the number of unmasked tokens per step for T=8. Which is more balanced?
   中文翻译：余弦调度 vs 线性调度：追踪 T=8 时每步解掩码的 token 数。哪个更均衡？

4. A 512x512 Show-o image is 1024 tokens. At vocab K=16384, the model emits 1024 * log2(16384) = 14,336 bits (~1.75 KiB) of data. Stable Diffusion outputs 512*512*24 bits = 6,291,456 bits (~768 KiB) of raw pixels. What is the compression ratio and what quality does it buy?
   中文翻译：512x512 Show-o 图像是 1024 个 token。词汇表 K=16384 下，模型输出约 1.75 KiB 数据。SD 输出约 768 KiB 原始像素。压缩比是多少？换来什么质量？

5. Read LlamaGen (arXiv:2406.06525). How is LlamaGen's class-conditional autoregressive image model different from Show-o's masked approach?
   中文翻译：阅读 LlamaGen（arXiv:2406.06525）。LlamaGen 的类别条件自回归图像模型与 Show-o 的掩码方法有何不同？

## Key Terms  | 关键术语

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Masked discrete diffusion | "MaskGIT-style" | Training to predict masked tokens; at inference, iteratively unmask the most-confident predictions | 训练预测掩码 token；推理时迭代解掩码最有信心的预测 |
| Cosine schedule | "Unmask schedule" | Decay of mask ratio over inference steps; concentrates confidence growth at mid-range | 推理步骤中掩码比例的衰减；将信心增长集中在中程 |
| Parallel decoding | "All tokens at once" | Every step predicts the full sequence of masked tokens in one forward pass, then commits top-K | 每步在一次前向传播中预测所有掩码 token，然后提交 top-K |
| Hybrid attention | "Causal + bidirectional" | Mask that is causal over text tokens and bidirectional within image blocks | 文本 token 因果、图像块内双向的掩码 |
| Inpainting | "Fill-in generation" | Condition on an image with some tokens masked, predict the missing ones; free from the training objective | 以部分掩码图像为条件，预测缺失 token；从训练目标免费获得 |
| Commitment rate | "Top-K per step" | How many tokens are declared "done" per iteration; controls inference vs quality trade-off | 每次迭代声明"完成"的 token 数；控制推理与质量的权衡 |

## Further Reading  | 延伸阅读

- [Xie et al. — Show-o (arXiv:2408.12528)](https://arxiv.org/abs/2408.12528)
  中文翻译：Show-o 论文。
- [Show-o2 (arXiv:2506.15564)](https://arxiv.org/abs/2506.15564)
  中文翻译：Show-o2 后续论文。
- [Chang et al. — MaskGIT (arXiv:2202.04200)](https://arxiv.org/abs/2202.04200)
  中文翻译：MaskGIT 论文，掩码离散扩散的原始工作。
- [Sun et al. — LlamaGen (arXiv:2406.06525)](https://arxiv.org/abs/2406.06525)
  中文翻译：LlamaGen 自回归图像生成。
- [Chang et al. — Muse (arXiv:2301.00704)](https://arxiv.org/abs/2301.00704)
  中文翻译：Muse 掩码图像生成。
