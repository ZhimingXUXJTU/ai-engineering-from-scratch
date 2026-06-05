# MIO and Any-to-Any Streaming Multimodal Models | MIO：任意到任意流式多模态模型

> GPT-4o ships a product most open models cannot replicate: an agent that hears voice, sees video, and speaks back in real time. The open-ecosystem answer by late 2024 was MIO (Wang et al., September 2024). MIO tokenizes text, image, speech, and music, trains one causal transformer over the interleaved sequences, and generates any modality to any modality. AnyGPT (Zhan et al., February 2024) was the proof of concept; MIO is the scale-up; Unified-IO 2 (Allen AI, December 2023) is the cousin with vision + action grounding. This lesson reads the any-to-any pattern — four tokenizers, one transformer, streaming-friendly decode.

> **【中文解读】** GPT-4o 展示了一个令人震撼的产品形态：一个能听、能看、能实时语音回复的 Agent。开源社区直到 2024 年底才有了 MIO 这个可行方案。MIO 的核心思路是将文本、图像、语音、音乐全部 tokenize 成整数 token，用一个因果 Transformer 统一处理，实现任意模态到任意模态的生成。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-modality token allocator + streaming decode loop) | **语言:** Python（标准库，四模态 token 分配器 + 流式解码循环）
**Prerequisites:** Phase 12 · 11 (Chameleon), Phase 6 (Speech and Audio) | **前置知识:** Phase 12 · 11（Chameleon），Phase 6（语音与音频）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Learning Objectives | 学习目标

- Design a shared vocabulary that hosts text, image, speech, and music tokens without collisions.
  中文翻译：设计一个共享词汇表，容纳文本、图像、语音和音乐 token 而不冲突。
- Compare SEED-Tokenizer (images) and SpeechTokenizer residual-VQ (speech) on compression + reconstruction trade-offs.
  中文翻译：比较 SEED-Tokenizer（图像）和 SpeechTokenizer 残差 VQ（语音）在压缩+重建方面的权衡。
- Explain the four-stage curriculum that builds up any-to-any generation.
  中文翻译：解释构建任意到任意生成的四阶段课程学习。
- Name the three open any-to-any recipes and their main trade-offs: MIO, AnyGPT, Unified-IO 2.
  中文翻译：列举三个开放的任意到任意方案及其主要权衡：MIO、AnyGPT、Unified-IO 2。

## The Problem | 问题引入

A unified multimodal model is easy to claim and hard to build at scale. Most "any-to-any" systems until 2024 were pipelined: vision model → text representation → speech model → audio. Each hop loses information, adds latency, and complicates training. GPT-4o's demo video showed a single-model alternative with subsecond response; open systems trailed by months.

> 统一多模态模型容易声称但难以大规模构建。2024 年之前大多数"任意到任意"系统都是管道式的：视觉模型→文本表示→语音模型→音频。每跳都会丢失信息、增加延迟、复杂化训练。GPT-4o 的演示视频展示了单模型替代方案，响应时间在秒级以下；开放系统落后了数月。

> **【中文解读】** "任意到任意"多模态系统最大的挑战是：不能再用级联管道（视觉→文本→语音→音频），因为每个阶段都会丢失信息并增加延迟。需要的是一个统一模型，像 GPT-4o 那样用单一 Transformer 直接处理所有模态。

The engineering challenges:

> 工程挑战：

- Tokenizers must exist for every modality, compress losslessly-enough for reconstruction, and produce tokens at rates the transformer can consume.
  中文翻译：每种模态都必须有分词器，压缩损失足够小以便重建，并以 Transformer 可消费的速率产生 token。
- A single vocabulary must allocate space for text (32k+), image (16k+), speech (4k+), music (8k+). Forty-thousand-plus entries minimum.
  中文翻译：单一词汇表必须为文本（32k+）、图像（16k+）、语音（4k+）、音乐（8k+）分配空间。至少四万条以上。
- Training data must cover every input-output pair (text→image, image→speech, speech→image, etc.) or the model must compose.
  中文翻译：训练数据必须覆盖每个输入-输出对（文本→图像、图像→语音、语音→图像等），或模型必须能组合。
- Inference must stream output tokens fast enough for conversational latency (<500ms time-to-first-audio-byte).
  中文翻译：推理必须以足够快的速度流式输出 token，以满足对话延迟（<500ms 首个音频字节时间）。

## The Concept | 核心概念

> **【中文解读】** MIO 实现任意到任意的多模态流式处理：文本、图像、音频、视频之间可以任意组合输入和输出。核心是统一的离散 token 化——所有模态都被编码为 token 序列，用一个 Transformer 统一处理。

> **【拓展：全模态模型的趋势】** 2025 年的趋势是从"视觉+语言"走向"全模态"：GPT-4o 原生支持语音输入输出，Gemini 支持视频实时流，Meta 的 Spirit LM 统一语音和文本。全模态模型需要解决的核心问题是不同模态的信息密度差异——1 秒视频约 30 帧，1 秒语音约 16K 样本，需要高效压缩。


### Four tokenizers for four modalities

MIO's tokenizer stack:

> **【中文解读】** MIO 为四种模态各配一个专用 tokenizer，输出的 token 都映射到共享词汇表的不重叠 ID 区间。文本用标准 BPE（32000 词），图像用 SEED-Tokenizer（4096 离散码本），语音用 SpeechTokenizer 残差 VQ（8 层分层码本，首层为内容、后续层为韵律和说话人身份），音乐用 Encodec 系列残差 VQ。总词汇量约 48k。

- Text: standard BPE, vocab ~32000.
  中文翻译：文本：标准 BPE，词汇量约 32000。
- Image: SEED-Tokenizer (2023) — quantized VAE with discrete codebook, 4096 entries, 32x32 tokens per image.
  中文翻译：图像：SEED-Tokenizer（2023）——带离散码本的量化 VAE，4096 个条目，每张图 32x32 个 token。
- Speech: SpeechTokenizer residual-VQ (2023) — encodes 16kHz waveform into 8 hierarchical codebooks; first level is coarse content, later levels add prosody and speaker identity.
  中文翻译：语音：SpeechTokenizer 残差 VQ（2023）——将 16kHz 波形编码为 8 层层级码本；第一层是粗粒度内容，后续层添加韵律和说话人身份。
- Music: similar residual-VQ (Meta's MusicGen / Encodec family), 4-8 codebooks.
  中文翻译：音乐：类似残差 VQ（Meta 的 MusicGen / Encodec 系列），4-8 个码本。

Each modality produces integer tokens. The tokens get disjoint ID ranges in the shared vocabulary:

> 每种模态产生整数 token。Token 在共享词汇表中获得不重叠的 ID 区间：

```
text:   0..31999
image:  32000..36095  (4096 image tokens)
speech: 36096..40191  (4096 speech base tokens, plus residual layers)
music:  40192..48383  (8192 music tokens)
sep:    48384..48390  (<image>, <speech>, <music>, </...>, etc.)
```

Total: ~48k vocabulary. The input embedding and output projection span all of it.

> 总计约 48k 词汇量。输入嵌入和输出投影覆盖全部词汇。

### Streaming decode

Speech generation uses residual-VQ. The transformer predicts the base (layer 0) speech tokens; a parallel-decoded residual quantizer predicts the subsequent layers. Each layer 0 token is roughly 50ms of audio at 16kHz.

> 语音生成使用残差 VQ。Transformer 预测基础层（第 0 层）语音 token；并行解码的残差量化器预测后续层。每个第 0 层 token 大约对应 16kHz 下的 50ms 音频。

> **【中文解读】** 流式解码的关键是并行处理：Transformer 预测语音基础层 token，残差量化器并行预测后续层。每个基础层 token 对应约 50ms 音频。整个链路从麦克风到首个音频输出约 300-500ms，接近 GPT-4o 的 250ms。

The streaming pattern:

> 流式模式：

1. User speaks into mic; real-time audio tokenizer emits speech tokens every 50ms.
   中文翻译：用户对着麦克风说话；实时音频分词器每 50ms 输出语音 token。
2. MIO consumes tokens as they arrive (prompt prefill + incremental forward).
   中文翻译：MIO 在 token 到达时即时消费（prompt 预填充 + 增量前向传播）。
3. Output tokens stream out as generated; a parallel speech decoder converts them to audio samples with ~50-150ms latency.
   中文翻译：输出 token 在生成时流式输出；并行语音解码器以约 50-150ms 延迟将其转换为音频样本。
4. Time-to-first-audio-byte: ~300-500ms in MIO paper, approaching GPT-4o's ~250ms.
   中文翻译：首音频字节时间（TTFAB）：MIO 论文约 300-500ms，接近 GPT-4o 的约 250ms。

Mini-Omni (arXiv:2408.16725), GLM-4-Voice (arXiv:2412.02612), and Moshi (arXiv:2410.00037) are complementary streaming speech-LLM designs. Moshi in particular achieves 160ms round-trip on a single GPU.

> Mini-Omni、GLM-4-Voice 和 Moshi 是互补的流式语音 LLM 设计。Moshi 在单 GPU 上实现了 160ms 往返延迟。

### Four-stage curriculum

MIO's training curriculum:

> MIO 的训练课程：

1. Stage 1 — alignment. Large-scale modality-pair corpora: text-image, text-speech, text-music. Each pair uses its own token vocabulary segment. Trains the shared vocabulary.
   中文翻译：阶段 1 —— 对齐。大规模模态对语料：文本-图像、文本-语音、文本-音乐。每对使用自己的 token 词汇段。训练共享词汇表。
2. Stage 2 — interleaved. Multi-modality interleaved documents (blogs with images + video, podcasts with transcripts, etc.). Trains cross-modality context.
   中文翻译：阶段 2 —— 交错。多模态交错文档（带图片+视频的博客、带文字稿的播客等）。训练跨模态上下文。
3. Stage 3 — speech-enhanced. Extra audio data to lift speech quality without losing text capability.
   中文翻译：阶段 3 —— 语音增强。额外音频数据提升语音质量，不损失文本能力。
4. Stage 4 — SFT. Instruction tuning across modalities: VQA, captioning, narration, speech-to-speech dialogue.
   中文翻译：阶段 4 —— 指令微调（SFT）。跨模态指令调优：VQA、描述、旁白、语音对话。

Missing a stage degrades specific capabilities: skip stage 2 and the model loses cross-modality context; skip stage 3 and speech is poor.

> 跳过某一阶段会导致特定能力退化：跳过阶段 2 模型失去跨模态上下文；跳过阶段 3 语音质量差。

> **【中文解读】** MIO 的四阶段训练课程是逐步构建能力的：(1) 模态对齐——大规模图文、文本-语音配对训练共享词汇表；(2) 交错训练——多模态交错文档训练跨模态上下文；(3) 语音增强——额外音频数据提升语音质量；(4) 指令微调——跨模态的 VQA、描述、对话等。跳过任一阶段都会导致特定能力退化。

### Chain-of-visual-thought

MIO introduces chain-of-visual-thought: the model emits intermediate image tokens as a reasoning step. For "is the cat climbing a tree?" the model:

> MIO 引入了视觉思维链（chain-of-visual-thought）：模型在推理过程中生成中间图像 token。例如"猫在爬树吗？"模型会：

1. Emits `<image>` tokens rendering the scene (from the input image or a sketch).
   中文翻译：输出 `<image>` token 渲染场景（来自输入图像或草图）。
2. Emits text analyzing the sketch.
   中文翻译：输出文本分析草图。
3. Emits the final answer.
   中文翻译：输出最终答案。

The rendered intermediate image serves as a scratchpad. Benchmarks improve on spatial-reasoning tasks. The idea mirrors chain-of-thought for text reasoning.

> 渲染的中间图像充当草稿板。在空间推理任务上基准测试有所改善。这一思路映射了文本推理中的思维链。

> **【拓展：视觉思维链的应用前景】** Chain-of-visual-thought 是文本思维链 (CoT) 在视觉领域的扩展。在金融场景中，这一技术可用于复杂图表分析：先生成中间可视化（如标注趋势线），再分析。在机器人领域，VLA 模型可以先用视觉思维链规划动作路径，再执行。

### Competitors in any-to-any

- AnyGPT (arXiv:2402.12226): 4 modalities (text, image, speech, music), similar design.
  中文翻译：AnyGPT：4 种模态（文本、图像、语音、音乐），类似设计。
- Unified-IO 2 (arXiv:2312.17172): adds vision action outputs, depth, normals. More task diversity, smaller scale.
  中文翻译：Unified-IO 2：添加视觉动作输出、深度、法线。任务更多样，规模更小。
- NExT-GPT (arXiv:2309.05519): LLM + modality-specific diffusion decoders. Not a single-model approach.
  中文翻译：NExT-GPT：LLM + 模态特定扩散解码器。非单模型方案。
- CoDi (arXiv:2305.11846): composable diffusion; any-to-any via shared latent.
  中文翻译：CoDi：可组合扩散；通过共享隐空间实现任意到任意。

MIO is the closest to pure-token any-to-any. AnyGPT is its conceptual ancestor.

> MIO 最接近纯 token 的任意到任意方案。AnyGPT 是其概念前身。

### Latency budget

For a conversational product, every component's latency matters:

> 对于对话产品，每个组件的延迟都很重要：

- Mic to audio tokens: ~50ms.
  中文翻译：麦克风到音频 token：约 50ms。
- Prefill (audio tokens + history): ~100ms on an 8B model.
  中文翻译：预填充（音频 token + 历史）：8B 模型约 100ms。
- First output token: ~50ms.
  中文翻译：首个输出 token：约 50ms。
- Parallel residual-VQ + speech decoder: ~100-150ms.
  中文翻译：并行残差 VQ + 语音解码器：约 100-150ms。

Total time-to-first-audio-byte: ~300ms minimum. GPT-4o claims ~250ms. Moshi claims 160ms. MIO/AnyGPT are in the 400-600ms range per public benchmarks.

> 首音频字节时间总计至少约 300ms。GPT-4o 声称约 250ms。Moshi 声称 160ms。MIO/AnyGPT 在公开基准测试中约 400-600ms。

> **【中文解读】** 对话产品的延迟预算：麦克风→语音 token（~50ms）→ 预填充（~100ms）→ 首个输出 token（~50ms）→ 残差 VQ + 语音解码（~100-150ms）。总计 TTFAB 约 300ms 起。GPT-4o 约 250ms，Moshi 仅 160ms（单 GPU 上最快的开源方案）。

### Why any-to-any stays hard

Even in 2026, open any-to-any models trail closed ones on two axes:

> 即使在 2026 年，开放的任意到任意模型在两个维度上仍落后于闭源模型：

- Speech quality. The residual-VQ tokenizer is lossy; conversational speech sounds robotic compared to ElevenLabs-class voices.
  中文翻译：语音质量。残差 VQ 分词器是有损的；与 ElevenLabs 级别的语音相比，对话语音听起来机械。
- Cross-modality reasoning. Asking the model "sing about what you see" still fails more often than pure-vision tasks.
  中文翻译：跨模态推理。让模型"唱出你看到的"仍然比纯视觉任务更频繁地失败。

These are open research problems. Qwen3-Omni (Lesson 12.20) is the most advanced open attempt in 2025.

> 这些都是开放的研究问题。Qwen3-Omni（第 12.20 课）是 2025 年最先进的开源尝试。

## Use It | 用框架实现

`code/main.py`:

> `code/main.py`：

- Defines the four-modality vocabulary allocation and prints it.
  中文翻译：定义四模态词汇分配并打印。
- Routes a list of multimodal inputs (text, image, audio-clip, music) through the tokenizer router.
  中文翻译：通过分词器路由器路由多模态输入（文本、图像、音频片段、音乐）。
- Simulates streaming decode for a text-to-speech response with latency counting.
  中文翻译：模拟文本转语音响应的流式解码并计算延迟。
- Computes the expected time-to-first-audio-byte given encoder, prefill, and decoder latencies.
  中文翻译：根据编码器、预填充和解码器延迟计算预期的首音频字节时间。

## Ship It | 产出物

This lesson produces `outputs/skill-any-to-any-pipeline-auditor.md`. Given a conversational product spec (modalities in, modalities out, latency target), it audits the MIO-family design choices and computes the latency budget.

> 本课产出 `outputs/skill-any-to-any-pipeline-auditor.md`。给定对话产品规格（输入模态、输出模态、延迟目标），它审计 MIO 系列的设计选择并计算延迟预算。

## Exercises | 练习题

1. Your product accepts speech input and returns speech output. What's the end-to-end latency budget target? List the components that spend time. 你的产品接受语音输入并返回语音输出。端到端延迟预算目标是多少？列出各组件耗时。

2. SpeechTokenizer residual-VQ uses 8 codebooks. Propose why parallel-decoding the residual levels is necessary (vs sequential) and what latency savings it brings. SpeechTokenizer 残差 VQ 使用 8 个码本。解释为什么需要并行（而非串行）解码残差层，以及节省了多少延迟。

3. Your vocabulary has 32k text + 4k image + 4k speech. Add 8k music and ~10 separators. What is the embedding-matrix parameter cost at hidden dim 4096? 你的词汇表有 32k 文本 + 4k 图像 + 4k 语音。加上 8k 音乐和约 10 个分隔符。在隐藏维度 4096 下，嵌入矩阵的参数量是多少？

4. Chain-of-visual-thought emits an intermediate image. What kinds of questions benefit? What kinds are hurt by the extra tokens? 视觉思维链会生成中间图像。哪些类型的问题受益？哪些类型会受到额外 token 的负面影响？

5. Read Moshi (arXiv:2410.00037). Describe its "inner monologue" technique and compare to MIO's chain-of-visual-thought. 阅读 Moshi 论文，描述其"内心独白"技术并与 MIO 的视觉思维链对比。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Any-to-any | "Multimodal in/out" 任意模态进出 | A single model that accepts and emits text, image, speech, and music in any direction 单一模型接受并以任意方向输出文本、图像、语音、音乐 | |
| Residual-VQ | "Speech tokenizer stack" 语音分词器栈 | Multi-codebook tokenization where each layer adds information; base layer is content, later layers are prosody 多码本分词，每层添加信息；基础层是内容，后续层是韵律 | |
| SEED-Tokenizer | "Image codes" 图像编码 | Discrete image tokenizer with 4096-entry codebook used by MIO 离散图像分词器，4096 码本 | |
| Chain-of-visual-thought | "Visual scratchpad" 视觉草稿板 | The model generates an intermediate image as a reasoning step before its final answer 模型在最终回答前生成中间图像作为推理步骤 | |
| Time-to-first-audio-byte | "TTFAB" 首音频字节延迟 | Latency from user voice to first audio output; <500ms for conversational feel 用户语音到首个音频输出的延迟；<500ms 才有对话感 | |
| Four-stage curriculum | "Training recipe" 训练配方 | Alignment -> interleaved -> speech-enhanced -> SFT, in that order 对齐→交错→语音增强→指令微调的四阶段训练流程 | |

## Further Reading | 延伸阅读

- [Wang et al. — MIO (arXiv:2409.17692)](https://arxiv.org/abs/2409.17692)
- [Zhan et al. — AnyGPT (arXiv:2402.12226)](https://arxiv.org/abs/2402.12226)
- [Lu et al. — Unified-IO 2 (arXiv:2312.17172)](https://arxiv.org/abs/2312.17172)
- [Wu et al. — NExT-GPT (arXiv:2309.05519)](https://arxiv.org/abs/2309.05519)
- [Tang et al. — CoDi (arXiv:2305.11846)](https://arxiv.org/abs/2305.11846)
