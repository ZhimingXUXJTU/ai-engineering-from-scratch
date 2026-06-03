# MIO and Any-to-Any Streaming Multimodal Models | MIO：任意到任意流式多模态模型

> GPT-4o ships a product most open models cannot replicate: an agent that hears voice, sees video, and speaks back in real time. The open-ecosystem answer by late 2024 was MIO (Wang et al., September 2024). MIO tokenizes text, image, speech, and music, trains one causal transformer over the interleaved sequences, and generates any modality to any modality. AnyGPT (Zhan et al., February 2024) was the proof of concept; MIO is the scale-up; Unified-IO 2 (Allen AI, December 2023) is the cousin with vision + action grounding. This lesson reads the any-to-any pattern — four tokenizers, one transformer, streaming-friendly decode.

> **【中文解读】** GPT-4o 展示了一个令人震撼的产品形态：一个能听、能看、能实时语音回复的 Agent。开源社区直到 2024 年底才有了 MIO 这个可行方案。MIO 的核心思路是将文本、图像、语音、音乐全部 tokenize 成整数 token，用一个因果 Transformer 统一处理，实现任意模态到任意模态的生成。

**Type:** Learn
**Languages:** Python (stdlib, four-modality token allocator + streaming decode loop)
**Prerequisites:** Phase 12 · 11 (Chameleon), Phase 6 (Speech and Audio)
**Time:** ~120 minutes

## Learning Objectives

- Design a shared vocabulary that hosts text, image, speech, and music tokens without collisions.
- Compare SEED-Tokenizer (images) and SpeechTokenizer residual-VQ (speech) on compression + reconstruction trade-offs.
- Explain the four-stage curriculum that builds up any-to-any generation.
- Name the three open any-to-any recipes and their main trade-offs: MIO, AnyGPT, Unified-IO 2.

## The Problem

A unified multimodal model is easy to claim and hard to build at scale. Most "any-to-any" systems until 2024 were pipelined: vision model → text representation → speech model → audio. Each hop loses information, adds latency, and complicates training. GPT-4o's demo video showed a single-model alternative with subsecond response; open systems trailed by months.

> **【中文解读】** "任意到任意"多模态系统最大的挑战是：不能再用级联管道（视觉→文本→语音→音频），因为每个阶段都会丢失信息并增加延迟。需要的是一个统一模型，像 GPT-4o 那样用单一 Transformer 直接处理所有模态。

The engineering challenges:

- Tokenizers must exist for every modality, compress losslessly-enough for reconstruction, and produce tokens at rates the transformer can consume.
- A single vocabulary must allocate space for text (32k+), image (16k+), speech (4k+), music (8k+). Forty-thousand-plus entries minimum.
- Training data must cover every input-output pair (text→image, image→speech, speech→image, etc.) or the model must compose.
- Inference must stream output tokens fast enough for conversational latency (<500ms time-to-first-audio-byte).

## The Concept

### Four tokenizers for four modalities

MIO's tokenizer stack:

> **【中文解读】** MIO 为四种模态各配一个专用 tokenizer，输出的 token 都映射到共享词汇表的不重叠 ID 区间。文本用标准 BPE（32000 词），图像用 SEED-Tokenizer（4096 离散码本），语音用 SpeechTokenizer 残差 VQ（8 层分层码本，首层为内容、后续层为韵律和说话人身份），音乐用 Encodec 系列残差 VQ。总词汇量约 48k。

- Text: standard BPE, vocab ~32000.
- Image: SEED-Tokenizer (2023) — quantized VAE with discrete codebook, 4096 entries, 32x32 tokens per image.
- Speech: SpeechTokenizer residual-VQ (2023) — encodes 16kHz waveform into 8 hierarchical codebooks; first level is coarse content, later levels add prosody and speaker identity.
- Music: similar residual-VQ (Meta's MusicGen / Encodec family), 4-8 codebooks.

Each modality produces integer tokens. The tokens get disjoint ID ranges in the shared vocabulary:

```
text:   0..31999
image:  32000..36095  (4096 image tokens)
speech: 36096..40191  (4096 speech base tokens, plus residual layers)
music:  40192..48383  (8192 music tokens)
sep:    48384..48390  (<image>, <speech>, <music>, </...>, etc.)
```

Total: ~48k vocabulary. The input embedding and output projection span all of it.

### Streaming decode

Speech generation uses residual-VQ. The transformer predicts the base (layer 0) speech tokens; a parallel-decoded residual quantizer predicts the subsequent layers. Each layer 0 token is roughly 50ms of audio at 16kHz.

> **【中文解读】** 流式解码的关键是并行处理：Transformer 预测语音基础层 token，残差量化器并行预测后续层。每个基础层 token 对应约 50ms 音频。整个链路从麦克风到首个音频输出约 300-500ms，接近 GPT-4o 的 250ms。

The streaming pattern:

1. User speaks into mic; real-time audio tokenizer emits speech tokens every 50ms.
2. MIO consumes tokens as they arrive (prompt prefill + incremental forward).
3. Output tokens stream out as generated; a parallel speech decoder converts them to audio samples with ~50-150ms latency.
4. Time-to-first-audio-byte: ~300-500ms in MIO paper, approaching GPT-4o's ~250ms.

Mini-Omni (arXiv:2408.16725), GLM-4-Voice (arXiv:2412.02612), and Moshi (arXiv:2410.00037) are complementary streaming speech-LLM designs. Moshi in particular achieves 160ms round-trip on a single GPU.

### Four-stage curriculum

MIO's training curriculum:

1. Stage 1 — alignment. Large-scale modality-pair corpora: text-image, text-speech, text-music. Each pair uses its own token vocabulary segment. Trains the shared vocabulary.
2. Stage 2 — interleaved. Multi-modality interleaved documents (blogs with images + video, podcasts with transcripts, etc.). Trains cross-modality context.
3. Stage 3 — speech-enhanced. Extra audio data to lift speech quality without losing text capability.
4. Stage 4 — SFT. Instruction tuning across modalities: VQA, captioning, narration, speech-to-speech dialogue.

Missing a stage degrades specific capabilities: skip stage 2 and the model loses cross-modality context; skip stage 3 and speech is poor.

> **【中文解读】** MIO 的四阶段训练课程是逐步构建能力的：(1) 模态对齐——大规模图文、文本-语音配对训练共享词汇表；(2) 交错训练——多模态交错文档训练跨模态上下文；(3) 语音增强——额外音频数据提升语音质量；(4) 指令微调——跨模态的 VQA、描述、对话等。跳过任一阶段都会导致特定能力退化。

### Chain-of-visual-thought

MIO introduces chain-of-visual-thought: the model emits intermediate image tokens as a reasoning step. For "is the cat climbing a tree?" the model:

1. Emits `<image>` tokens rendering the scene (from the input image or a sketch).
2. Emits text analyzing the sketch.
3. Emits the final answer.

The rendered intermediate image serves as a scratchpad. Benchmarks improve on spatial-reasoning tasks. The idea mirrors chain-of-thought for text reasoning.

> **【拓展：视觉思维链的应用前景】** Chain-of-visual-thought 是文本思维链 (CoT) 在视觉领域的扩展。在金融场景中，这一技术可用于复杂图表分析：先生成中间可视化（如标注趋势线），再分析。在机器人领域，VLA 模型可以先用视觉思维链规划动作路径，再执行。

### Competitors in any-to-any

- AnyGPT (arXiv:2402.12226): 4 modalities (text, image, speech, music), similar design.
- Unified-IO 2 (arXiv:2312.17172): adds vision action outputs, depth, normals. More task diversity, smaller scale.
- NExT-GPT (arXiv:2309.05519): LLM + modality-specific diffusion decoders. Not a single-model approach.
- CoDi (arXiv:2305.11846): composable diffusion; any-to-any via shared latent.

MIO is the closest to pure-token any-to-any. AnyGPT is its conceptual ancestor.

### Latency budget

For a conversational product, every component's latency matters:

- Mic to audio tokens: ~50ms.
- Prefill (audio tokens + history): ~100ms on an 8B model.
- First output token: ~50ms.
- Parallel residual-VQ + speech decoder: ~100-150ms.

Total time-to-first-audio-byte: ~300ms minimum. GPT-4o claims ~250ms. Moshi claims 160ms. MIO/AnyGPT are in the 400-600ms range per public benchmarks.

> **【中文解读】** 对话产品的延迟预算：麦克风→语音 token（~50ms）→ 预填充（~100ms）→ 首个输出 token（~50ms）→ 残差 VQ + 语音解码（~100-150ms）。总计 TTFAB 约 300ms 起。GPT-4o 约 250ms，Moshi 仅 160ms（单 GPU 上最快的开源方案）。

### Why any-to-any stays hard

Even in 2026, open any-to-any models trail closed ones on two axes:

- Speech quality. The residual-VQ tokenizer is lossy; conversational speech sounds robotic compared to ElevenLabs-class voices.
- Cross-modality reasoning. Asking the model "sing about what you see" still fails more often than pure-vision tasks.

These are open research problems. Qwen3-Omni (Lesson 12.20) is the most advanced open attempt in 2025.

## Use It

`code/main.py`:

- Defines the four-modality vocabulary allocation and prints it.
- Routes a list of multimodal inputs (text, image, audio-clip, music) through the tokenizer router.
- Simulates streaming decode for a text-to-speech response with latency counting.
- Computes the expected time-to-first-audio-byte given encoder, prefill, and decoder latencies.

## Ship It

This lesson produces `outputs/skill-any-to-any-pipeline-auditor.md`. Given a conversational product spec (modalities in, modalities out, latency target), it audits the MIO-family design choices and computes the latency budget.

## Exercises

1. Your product accepts speech input and returns speech output. What's the end-to-end latency budget target? List the components that spend time. 你的产品接受语音输入并返回语音输出。端到端延迟预算目标是多少？列出各组件耗时。

2. SpeechTokenizer residual-VQ uses 8 codebooks. Propose why parallel-decoding the residual levels is necessary (vs sequential) and what latency savings it brings. SpeechTokenizer 残差 VQ 使用 8 个码本。解释为什么需要并行（而非串行）解码残差层，以及节省了多少延迟。

3. Your vocabulary has 32k text + 4k image + 4k speech. Add 8k music and ~10 separators. What is the embedding-matrix parameter cost at hidden dim 4096? 你的词汇表有 32k 文本 + 4k 图像 + 4k 语音。加上 8k 音乐和约 10 个分隔符。在隐藏维度 4096 下，嵌入矩阵的参数量是多少？

4. Chain-of-visual-thought emits an intermediate image. What kinds of questions benefit? What kinds are hurt by the extra tokens? 视觉思维链会生成中间图像。哪些类型的问题受益？哪些类型会受到额外 token 的负面影响？

5. Read Moshi (arXiv:2410.00037). Describe its "inner monologue" technique and compare to MIO's chain-of-visual-thought. 阅读 Moshi 论文，描述其"内心独白"技术并与 MIO 的视觉思维链对比。

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Any-to-any | "Multimodal in/out" 任意模态进出 | A single model that accepts and emits text, image, speech, and music in any direction 单一模型接受并以任意方向输出文本、图像、语音、音乐 |
| Residual-VQ | "Speech tokenizer stack" 语音分词器栈 | Multi-codebook tokenization where each layer adds information; base layer is content, later layers are prosody 多码本分词，每层添加信息；基础层是内容，后续层是韵律 |
| SEED-Tokenizer | "Image codes" 图像编码 | Discrete image tokenizer with 4096-entry codebook used by MIO 离散图像分词器，4096 码本 |
| Chain-of-visual-thought | "Visual scratchpad" 视觉草稿板 | The model generates an intermediate image as a reasoning step before its final answer 模型在最终回答前生成中间图像作为推理步骤 |
| Time-to-first-audio-byte | "TTFAB" 首音频字节延迟 | Latency from user voice to first audio output; <500ms for conversational feel 用户语音到首个音频输出的延迟；<500ms 才有对话感 |
| Four-stage curriculum | "Training recipe" 训练配方 | Alignment -> interleaved -> speech-enhanced -> SFT, in that order 对齐→交错→语音增强→指令微调的四阶段训练流程 |

## Further Reading

- [Wang et al. — MIO (arXiv:2409.17692)](https://arxiv.org/abs/2409.17692)
- [Zhan et al. — AnyGPT (arXiv:2402.12226)](https://arxiv.org/abs/2402.12226)
- [Lu et al. — Unified-IO 2 (arXiv:2312.17172)](https://arxiv.org/abs/2312.17172)
- [Wu et al. — NExT-GPT (arXiv:2309.05519)](https://arxiv.org/abs/2309.05519)
- [Tang et al. — CoDi (arXiv:2305.11846)](https://arxiv.org/abs/2305.11846)
