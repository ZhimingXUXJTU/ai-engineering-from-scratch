# Long-Video Understanding at Million-Token Context | 百万 Token 上下文的长视频理解

> A 1-hour 4K video at 24 FPS, patched and embedded, produces on the order of 60 million tokens. A 2-hour podcast episode transcribed is 30,000 tokens. A full Blu-ray feature film, even compressed with aggressive pooling, is hundreds of thousands of tokens. Google's Gemini 1.5 (March 2024) opened this era with a 10-million-token context, doing reliable needle-in-a-haystack recall over hour-long videos. LWM (Liu et al., February 2024) showed ring attention's scaling path. LongVILA and Video-XL scaled ingestion further. VideoAgent swapped raw context for agentic retrieval. Each approach is a different trade-off on compute, recall, and engineering complexity. This lesson reads them side by side.

> **【中文解读】** 1 小时 4K 视频可产生约 6000 万 token，远超任何模型的上下文窗口。处理长视频有三条路径：(1) 暴力上下文（Gemini 1.5 的千万 token 上下文）；(2) Ring Attention 跨设备分布式注意力；(3) Token 压缩（Video-XL 的摘要 token）；(4) Agent 检索（VideoAgent 将视频当数据库查询）。每条路径在计算量、召回率和工程复杂度上有不同取舍。

**Type:** Build
**Languages:** Python (stdlib, needle-in-haystack simulator + agentic-retrieval router)
**Prerequisites:** Phase 12 · 17 (video temporal tokens)
**Time:** ~180 minutes

## 学习目标

- Compute total visual-token counts for long-form video at varying FPS and pooling.
- Explain the three scaling paths: brute context (Gemini 1.5), ring attention (LWM), token compression (LongVILA / Video-XL).
- Compare raw-context video VLMs vs agentic-retrieval video VLMs (VideoAgent) on accuracy and latency.
- Design a needle-in-a-haystack test for a 30-minute video and measure recall at a specific minute.

## 问题引入

A single frame of Qwen2.5-VL-sized patches at 384 native resolution is ~729 tokens. At 3x3 pooling that's 81 tokens per frame. A 30-minute clip at 1 FPS = 1800 frames = 145,800 tokens. Doable by 2025 open VLMs, tight. At 2 FPS, 291,600 tokens — only the biggest contexts fit.

A 2-hour movie at 1 FPS is 583k tokens. Beyond most 2026 open models; requires Gemini 2.5 Pro or pooling more aggressively.

Three scaling paths emerged.

## 核心概念

> **【中文解读】** 长视频理解（百万 token 级别）是多模态 AI 的前沿挑战。一小时视频约 108,000 帧，即使每帧压缩为 1 个 token 也需要处理 10 万+ token。核心技术：层次化压缩、稀疏采样、状态空间模型（SSM）处理超长序列。

> **【拓展：Gemini 1.5 Pro 的百万 token 上下文** Gemini 1.5 Pro 支持 1M token 输入，可以处理约 1 小时的视频或 1000+ 页文档。通过稀疏注意力（仅关注相关帧）和分块处理实现。在长视频 QA 任务上，Gemini 1.5 Pro 的准确率随视频长度下降较缓慢，但仍与人类有显著差距。


### Path 1: Brute context (Gemini 1.5, Claude Opus)

Throw hardware at the problem. Scale context to millions of tokens, process everything in one forward pass.

Gemini 1.5 Pro launched with 1M tokens; Gemini 1.5 Ultra to 10M; Gemini 2.5 Pro in 2026 does hours of video reliably. The paper (arXiv:2403.05530) documents needle-in-a-haystack recall at 99.7% up to ~9.5M tokens.

Engineering: a custom attention implementation with memory hierarchy (local + global + sparse) plus MoE expert routing for long-context efficiency. Not published in full detail. Not open-source.

### Path 2: Ring attention (LWM, LongVILA)

Ring attention distributes long sequences across devices in a "ring" where each device holds a chunk. Attention across the full sequence happens by each device sending its chunk to the next in a ring pattern, computing partial attention, and aggregating.

> **【中文解读】** Ring Attention 将长序列分布到多个设备上，每个设备持有序列的一个块，通过环形通信计算全局注意力。计算量随上下文长度线性增长（而非二次方），因为注意力的二次开销被分摊到了环形设备上。LongVILA 用 8 路并行处理 268k token 的视频。

LWM (Liu et al., 2024) trained a 1M-token context model this way. Training compute scales linearly with context, not quadratically — the quadratic hit on attention is amortized across the ring's devices.

LongVILA (arXiv:2408.10188) adapted the pattern to VLMs. 1400-frame videos at 192 tokens per frame = 268k context, trained with ring attention across 8-way parallelism.

### Path 3: Token compression (Video-XL, LongVA)

Cheaper than brute context: compress aggressively before the LLM sees the sequence.

Video-XL (arXiv:2409.14485) uses a visual summary token: each clip of N frames produces a single "summary" token that attends over the N. At inference, the LLM sees one summary token per clip, drastically shrinking the context.

LongVA extends LLM context from 200k to 2M with a "long context transfer" technique. Train on long-context text, transfer to long-context video via shared representation.

Token compression trades off recall at specific timestamps for scalability. The model knows generally what happened but sometimes misses exact frames.

### Path 4: Agentic retrieval (VideoAgent)

Do not feed the full video to the LLM. Instead, treat the video as a database and use an LLM to query it.

VideoAgent (arXiv:2403.10517):

1. LLM reads the question.
2. LLM asks a retrieval tool for relevant clips ("show me segments with a cat").
3. Tool returns matching clip timestamps.
4. LLM reads those clips via a VLM.
5. LLM composes the answer or asks follow-up queries.

This is the LLM-as-agent pattern applied to long video. Cheaper inference (only relevant clips encoded), harder engineering (retrieval quality becomes the bottleneck).

> **【拓展：生产级长视频管道】** 2026 年生产环境的长视频管道通常是混合方案：(1) 对整个视频进行动态 FPS 采样 + 激进池化（得到约 100k token 的全局表示）；(2) 用 72B VLM 生成全局摘要；(3) 用户提问时，用 Agent 检索定位到相关片段。这结合了暴力上下文的全局理解和检索的局部细节能力。

### Needle-in-a-haystack benchmarks

The standard long-context test: insert a unique visual or textual marker at a random point in the video, then ask a query that requires recalling it.

Metric: Recall@k across video length and marker position.

Gemini 2.5 Pro scores >99% recall at up to 90-minute videos. Open 72B models (Qwen2.5-VL-72B, InternVL3-78B) score ~85-90% at 30 minutes and degrade past 60.

VideoAgent can match or beat raw-context models at 2+ hours because retrieval hits the needle if the tool is good.

### Which path to pick

For a 15-minute clip at frontier accuracy: open 72B + native context usually works. Pick Qwen2.5-VL-72B.

For 30-minute to 1-hour content: LongVILA or Video-XL for open; Gemini 2.5 Pro for closed. The quality bar matters — frontier goes closed.

For 2+ hour content: VideoAgent or similar retrieval patterns. Alternatively, summarize to smaller chunks and feed hierarchical summaries.

### 2026 production pattern

In practice, production long-video pipelines are hybrid:

1. Run dynamic-FPS sampling + aggressive pooling on the entire video (get a 100k-token global representation).
2. Pass to a 72B VLM for a global summary.
3. If user asks detailed questions, run agentic retrieval using the summary as an index.

This combines brute-context for global understanding and retrieval for local detail.

## 用框架实现

`code/main.py`:

- Computes token budgets for videos from 1 minute to 3 hours at varying FPS + pooling.
- Simulates a needle-in-a-haystack run: inject a marker at a random timestamp, ask a question, score recall.
- Includes an agentic-retrieval router simulator that picks specific clips to feed to a downstream VLM.

Run the budget table and feel the scale gap.

## 产出物

This lesson produces `outputs/skill-long-video-strategy-planner.md`. Given a video duration and query complexity, it picks between brute-context, compression, and agentic retrieval, and computes the latency + quality expectations.

## 练习题

1. A 45-minute lecture at 1 FPS, 81 tokens per frame. Total tokens? Fits in which models' contexts? 45 分钟讲座，1 FPS，每帧 81 token。总 token 数？能放入哪些模型的上下文？

2. Design a needle-in-a-haystack test: at what minute do you inject the marker, and what is the exact query format? 设计一个大海捞针测试：在哪一分钟注入标记？精确的查询格式是什么？

3. Compare brute-context Qwen2.5-VL-72B (80k context) to VideoAgent (Claude 3.5 + retrieval) on a 1-hour video. Which wins on recall? Which wins on latency? 在 1 小时视频上对比暴力上下文 Qwen2.5-VL-72B 和 VideoAgent。哪个召回率高？哪个延迟低？

4. Ring attention's memory cost scales linearly in sequence length and linearly in device count. Explain why and what fails if you drop the ring-rotation phase. Ring Attention 的内存开销随序列长度和设备数线性增长。解释原因，以及去掉环形轮转阶段会出什么问题。

5. Read Gemini 1.5 Section 5 on needle-in-a-haystack. What did the paper find about recall at the 1M vs 10M token boundary? 阅读 Gemini 1.5 第 5 节关于大海捞针的实验。论文发现 1M 和 10M token 边界的召回率有什么差异？

## 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Brute context | "Just more tokens" 暴力上下文 | Scale LLM context to millions of tokens; process everything in one pass 将 LLM 上下文扩展到百万 token，一次前向传播处理全部内容 | |
| Ring attention | "LWM-style parallel" 环形注意力 | Distributed attention pattern where each device holds a chunk and rotates 分布式注意力模式，每个设备持有一块并在环中轮转 | |
| Token compression | "Summary tokens" 摘要 token | Reduce per-clip tokens via a learned compressor before the LLM LLM 前通过学习型压缩器减少每片段 token 数 | |
| Needle-in-haystack | "NIH test" 大海捞针测试 | Insert a unique marker at a random point, ask model to recall it at test time 在随机位置插入唯一标记，测试时要求模型回忆 | |
| Agentic retrieval | "LLM as query planner" Agent 检索 | LLM asks a retrieval tool for relevant clips, reads them via a VLM, composes answer LLM 调用检索工具获取相关片段，通过 VLM 阅读并生成回答 | |
| VideoAgent | "Retrieval pattern for video" 视频检索模式 | Canonical agentic-retrieval design: question -> tool -> clip -> answer 经典 Agent 检索设计：问题→工具→片段→回答 | |

## 延伸阅读

- [Gemini Team — Gemini 1.5 (arXiv:2403.05530)](https://arxiv.org/abs/2403.05530)
- [Liu et al. — LWM / RingAttention (arXiv:2402.08268)](https://arxiv.org/abs/2402.08268)
- [Xue et al. — LongVILA (arXiv:2408.10188)](https://arxiv.org/abs/2408.10188)
- [Shu et al. — Video-XL (arXiv:2409.14485)](https://arxiv.org/abs/2409.14485)
- [Wang et al. — VideoAgent (arXiv:2403.10517)](https://arxiv.org/abs/2403.10517)
