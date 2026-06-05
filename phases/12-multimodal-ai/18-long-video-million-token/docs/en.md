# Long-Video Understanding at Million-Token Context | 百万 Token 上下文的长视频理解

> A 1-hour 4K video at 24 FPS, patched and embedded, produces on the order of 60 million tokens. A 2-hour podcast episode transcribed is 30,000 tokens. A full Blu-ray feature film, even compressed with aggressive pooling, is hundreds of thousands of tokens. Google's Gemini 1.5 (March 2024) opened this era with a 10-million-token context, doing reliable needle-in-a-haystack recall over hour-long videos. LWM (Liu et al., February 2024) showed ring attention's scaling path. LongVILA and Video-XL scaled ingestion further. VideoAgent swapped raw context for agentic retrieval. Each approach is a different trade-off on compute, recall, and engineering complexity. This lesson reads them side by side.

> **【中文解读】** 1 小时 4K 视频可产生约 6000 万 token，远超任何模型的上下文窗口。处理长视频有三条路径：(1) 暴力上下文（Gemini 1.5 的千万 token 上下文）；(2) Ring Attention 跨设备分布式注意力；(3) Token 压缩（Video-XL 的摘要 token）；(4) Agent 检索（VideoAgent 将视频当数据库查询）。每条路径在计算量、召回率和工程复杂度上有不同取舍。

**Type:** Build
**Languages:** Python (stdlib, needle-in-haystack simulator + agentic-retrieval router)
**Prerequisites:** Phase 12 · 17 (video temporal tokens)
**Time:** ~180 minutes

## Learning Objectives

- Compute total visual-token counts for long-form video at varying FPS and pooling.
  中文翻译：计算不同 FPS 和池化配置下长视频的视觉 token 总数。
- Explain the three scaling paths: brute context (Gemini 1.5), ring attention (LWM), token compression (LongVILA / Video-XL).
  中文翻译：解释三条扩展路径：暴力上下文（Gemini 1.5）、环形注意力（LWM）、token 压缩（LongVILA / Video-XL）。
- Compare raw-context video VLMs vs agentic-retrieval video VLMs (VideoAgent) on accuracy and latency.
  中文翻译：比较原始上下文视频 VLM 和 Agent 检索视频 VLM（VideoAgent）在准确率和延迟上的表现。
- Design a needle-in-a-haystack test for a 30-minute video and measure recall at a specific minute.
  中文翻译：为 30 分钟视频设计大海捞针测试并测量特定分钟的召回率。

## The Problem | 问题引入

A single frame of Qwen2.5-VL-sized patches at 384 native resolution is ~729 tokens. At 3x3 pooling that's 81 tokens per frame. A 30-minute clip at 1 FPS = 1800 frames = 145,800 tokens. Doable by 2025 open VLMs, tight. At 2 FPS, 291,600 tokens — only the biggest contexts fit.

> Qwen2.5-VL 大小的 patch 在 384 原生分辨率下每帧约 729 token。3x3 池化后每帧 81 token。30 分钟片段 1 FPS = 1800 帧 = 145,800 token，2025 年开放 VLM 可以处理但紧张。2 FPS 下 291,600 token——只有最大上下文才能容纳。

A 2-hour movie at 1 FPS is 583k tokens. Beyond most 2026 open models; requires Gemini 2.5 Pro or pooling more aggressively.

> 2 小时电影 1 FPS 是 583k token。超过 2026 年大多数开放模型的能力；需要 Gemini 2.5 Pro 或更激进的池化。

Three scaling paths emerged.

> 出现了三条扩展路径。

## The Concept | 核心概念

> **【中文解读】** 长视频理解（百万 token 级别）是多模态 AI 的前沿挑战。一小时视频约 108,000 帧，即使每帧压缩为 1 个 token 也需要处理 10 万+ token。核心技术：层次化压缩、稀疏采样、状态空间模型（SSM）处理超长序列。

> **【拓展：Gemini 1.5 Pro 的百万 token 上下文** Gemini 1.5 Pro 支持 1M token 输入，可以处理约 1 小时的视频或 1000+ 页文档。通过稀疏注意力（仅关注相关帧）和分块处理实现。在长视频 QA 任务上，Gemini 1.5 Pro 的准确率随视频长度下降较缓慢，但仍与人类有显著差距。


### Path 1: Brute context (Gemini 1.5, Claude Opus)

Throw hardware at the problem. Scale context to millions of tokens, process everything in one forward pass.

> 用硬件暴力解决问题。将上下文扩展到百万 token，一次前向传播处理全部内容。

Gemini 1.5 Pro launched with 1M tokens; Gemini 1.5 Ultra to 10M; Gemini 2.5 Pro in 2026 does hours of video reliably. The paper (arXiv:2403.05530) documents needle-in-a-haystack recall at 99.7% up to ~9.5M tokens.

> Gemini 1.5 Pro 以 1M token 发布；Gemini 1.5 Ultra 扩展到 10M；Gemini 2.5 Pro 在 2026 年可以可靠处理数小时视频。论文记录了在约 9.5M token 范围内 99.7% 的大海捞针召回率。

Engineering: a custom attention implementation with memory hierarchy (local + global + sparse) plus MoE expert routing for long-context efficiency. Not published in full detail. Not open-source.

> 工程实现：自定义注意力机制，带有内存层级（局部+全局+稀疏），加上 MoE 专家路由提升长上下文效率。未完整公开。非开源。

### Path 2: Ring attention (LWM, LongVILA)

Ring attention distributes long sequences across devices in a "ring" where each device holds a chunk. Attention across the full sequence happens by each device sending its chunk to the next in a ring pattern, computing partial attention, and aggregating.

> **【中文解读】** Ring Attention 将长序列分布到多个设备上，每个设备持有序列的一个块，通过环形通信计算全局注意力。计算量随上下文长度线性增长（而非二次方），因为注意力的二次开销被分摊到了环形设备上。LongVILA 用 8 路并行处理 268k token 的视频。

LWM (Liu et al., 2024) trained a 1M-token context model this way. Training compute scales linearly with context, not quadratically — the quadratic hit on attention is amortized across the ring's devices.

> LWM（Liu 等人，2024）用这种方式训练了 1M token 上下文模型。训练计算量随上下文线性增长而非二次方——注意力的二次开销被分摊到环形设备上。

LongVILA (arXiv:2408.10188) adapted the pattern to VLMs. 1400-frame videos at 192 tokens per frame = 268k context, trained with ring attention across 8-way parallelism.

> LongVILA 将该模式适配到 VLM。1400 帧视频，每帧 192 token = 268k 上下文，通过 8 路并行环形注意力训练。

### Path 3: Token compression (Video-XL, LongVA)

Cheaper than brute context: compress aggressively before the LLM sees the sequence.

> 比暴力上下文更便宜：在 LLM 看到序列之前进行激进压缩。

Video-XL (arXiv:2409.14485) uses a visual summary token: each clip of N frames produces a single "summary" token that attends over the N. At inference, the LLM sees one summary token per clip, drastically shrinking the context.

> Video-XL 使用视觉摘要 token：每 N 帧片段生成一个"摘要" token，对该 N 帧做注意力。推理时 LLM 每个片段只看到一个摘要 token，大幅缩减上下文。

LongVA extends LLM context from 200k to 2M with a "long context transfer" technique. Train on long-context text, transfer to long-context video via shared representation.

> LongVA 用"长上下文迁移"技术将 LLM 上下文从 200k 扩展到 2M。在长上下文文本上训练，通过共享表示迁移到长上下文视频。

Token compression trades off recall at specific timestamps for scalability. The model knows generally what happened but sometimes misses exact frames.

> Token 压缩以牺牲特定时间戳的召回率为代价换取可扩展性。模型大致知道发生了什么但有时会错过精确帧。

### Path 4: Agentic retrieval (VideoAgent)

Do not feed the full video to the LLM. Instead, treat the video as a database and use an LLM to query it.

> 不要将完整视频喂给 LLM。而是将视频当作数据库，用 LLM 查询它。

VideoAgent (arXiv:2403.10517):

> VideoAgent：

1. LLM reads the question.
   中文翻译：LLM 读取问题。
2. LLM asks a retrieval tool for relevant clips ("show me segments with a cat").
   中文翻译：LLM 向检索工具请求相关片段（"给我看有猫的片段"）。
3. Tool returns matching clip timestamps.
   中文翻译：工具返回匹配的片段时间戳。
4. LLM reads those clips via a VLM.
   中文翻译：LLM 通过 VLM 阅读那些片段。
5. LLM composes the answer or asks follow-up queries.
   中文翻译：LLM 生成回答或发起后续查询。

This is the LLM-as-agent pattern applied to long video. Cheaper inference (only relevant clips encoded), harder engineering (retrieval quality becomes the bottleneck).

> 这是将 LLM-as-agent 模式应用于长视频。推理更便宜（只编码相关片段），工程更难（检索质量成为瓶颈）。

> **【拓展：生产级长视频管道】** 2026 年生产环境的长视频管道通常是混合方案：(1) 对整个视频进行动态 FPS 采样 + 激进池化（得到约 100k token 的全局表示）；(2) 用 72B VLM 生成全局摘要；(3) 用户提问时，用 Agent 检索定位到相关片段。这结合了暴力上下文的全局理解和检索的局部细节能力。

### Needle-in-a-haystack benchmarks

The standard long-context test: insert a unique visual or textual marker at a random point in the video, then ask a query that requires recalling it.

> 标准长上下文测试：在视频随机位置插入唯一的视觉或文本标记，然后提出需要回忆该标记的查询。

Metric: Recall@k across video length and marker position.

> 指标：跨视频长度和标记位置的 Recall@k。

Gemini 2.5 Pro scores >99% recall at up to 90-minute videos. Open 72B models (Qwen2.5-VL-72B, InternVL3-78B) score ~85-90% at 30 minutes and degrade past 60.

> Gemini 2.5 Pro 在长达 90 分钟的视频上召回率 >99%。开放 72B 模型（Qwen2.5-VL-72B、InternVL3-78B）在 30 分钟时约 85-90%，60 分钟后退化。

VideoAgent can match or beat raw-context models at 2+ hours because retrieval hits the needle if the tool is good.

> VideoAgent 在 2 小时以上的视频中可以匹配或超越原始上下文模型，因为只要工具好，检索就能命中目标。

### Which path to pick

For a 15-minute clip at frontier accuracy: open 72B + native context usually works. Pick Qwen2.5-VL-72B.

> 15 分钟片段追求前沿准确率：开放 72B + 原生上下文通常可行。选 Qwen2.5-VL-72B。

For 30-minute to 1-hour content: LongVILA or Video-XL for open; Gemini 2.5 Pro for closed. The quality bar matters — frontier goes closed.

> 30 分钟到 1 小时内容：开源用 LongVILA 或 Video-XL；闭源用 Gemini 2.5 Pro。质量门槛很重要——前沿水平需要闭源。

For 2+ hour content: VideoAgent or similar retrieval patterns. Alternatively, summarize to smaller chunks and feed hierarchical summaries.

> 2 小时以上内容：VideoAgent 或类似检索模式。或者压缩为更小的块并喂入分层摘要。

### 2026 production pattern

In practice, production long-video pipelines are hybrid:

> 实践中，生产级长视频管道是混合方案：

1. Run dynamic-FPS sampling + aggressive pooling on the entire video (get a 100k-token global representation).
   中文翻译：对整个视频运行动态 FPS 采样 + 激进池化（得到约 100k token 的全局表示）。
2. Pass to a 72B VLM for a global summary.
   中文翻译：传入 72B VLM 生成全局摘要。
3. If user asks detailed questions, run agentic retrieval using the summary as an index.
   中文翻译：如果用户提问详细问题，用摘要作为索引运行 Agent 检索。

This combines brute-context for global understanding and retrieval for local detail.

> 这结合了暴力上下文的全局理解和检索的局部细节能力。

## Use It | 用框架实现

`code/main.py`:

- Computes token budgets for videos from 1 minute to 3 hours at varying FPS + pooling.
  中文翻译：计算 1 分钟到 3 小时视频在不同 FPS + 池化下的 token 预算。
- Simulates a needle-in-a-haystack run: inject a marker at a random timestamp, ask a question, score recall.
  中文翻译：模拟大海捞针测试：在随机时间戳注入标记，提问，评分召回率。
- Includes an agentic-retrieval router simulator that picks specific clips to feed to a downstream VLM.
  中文翻译：包含一个 Agent 检索路由模拟器，选择特定片段喂给下游 VLM。

Run the budget table and feel the scale gap.

> 运行预算表，感受规模差距。

## Ship It | 产出物

This lesson produces `outputs/skill-long-video-strategy-planner.md`. Given a video duration and query complexity, it picks between brute-context, compression, and agentic retrieval, and computes the latency + quality expectations.

> 本课产出 `outputs/skill-long-video-strategy-planner.md`。给定视频时长和查询复杂度，它在暴力上下文、压缩和 Agent 检索之间选择，并计算延迟+质量预期。

## Exercises | 练习题

1. A 45-minute lecture at 1 FPS, 81 tokens per frame. Total tokens? Fits in which models' contexts? 45 分钟讲座，1 FPS，每帧 81 token。总 token 数？能放入哪些模型的上下文？

2. Design a needle-in-a-haystack test: at what minute do you inject the marker, and what is the exact query format? 设计一个大海捞针测试：在哪一分钟注入标记？精确的查询格式是什么？

3. Compare brute-context Qwen2.5-VL-72B (80k context) to VideoAgent (Claude 3.5 + retrieval) on a 1-hour video. Which wins on recall? Which wins on latency? 在 1 小时视频上对比暴力上下文 Qwen2.5-VL-72B 和 VideoAgent。哪个召回率高？哪个延迟低？

4. Ring attention's memory cost scales linearly in sequence length and linearly in device count. Explain why and what fails if you drop the ring-rotation phase. Ring Attention 的内存开销随序列长度和设备数线性增长。解释原因，以及去掉环形轮转阶段会出什么问题。

5. Read Gemini 1.5 Section 5 on needle-in-a-haystack. What did the paper find about recall at the 1M vs 10M token boundary? 阅读 Gemini 1.5 第 5 节关于大海捞针的实验。论文发现 1M 和 10M token 边界的召回率有什么差异？

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Brute context | "Just more tokens" 暴力上下文 | Scale LLM context to millions of tokens; process everything in one pass 将 LLM 上下文扩展到百万 token，一次前向传播处理全部内容 | |
| Ring attention | "LWM-style parallel" 环形注意力 | Distributed attention pattern where each device holds a chunk and rotates 分布式注意力模式，每个设备持有一块并在环中轮转 | |
| Token compression | "Summary tokens" 摘要 token | Reduce per-clip tokens via a learned compressor before the LLM LLM 前通过学习型压缩器减少每片段 token 数 | |
| Needle-in-haystack | "NIH test" 大海捞针测试 | Insert a unique marker at a random point, ask model to recall it at test time 在随机位置插入唯一标记，测试时要求模型回忆 | |
| Agentic retrieval | "LLM as query planner" Agent 检索 | LLM asks a retrieval tool for relevant clips, reads them via a VLM, composes answer LLM 调用检索工具获取相关片段，通过 VLM 阅读并生成回答 | |
| VideoAgent | "Retrieval pattern for video" 视频检索模式 | Canonical agentic-retrieval design: question -> tool -> clip -> answer 经典 Agent 检索设计：问题→工具→片段→回答 | |

## Further Reading | 延伸阅读

- [Gemini Team — Gemini 1.5 (arXiv:2403.05530)](https://arxiv.org/abs/2403.05530)
- [Liu et al. — LWM / RingAttention (arXiv:2402.08268)](https://arxiv.org/abs/2402.08268)
- [Xue et al. — LongVILA (arXiv:2408.10188)](https://arxiv.org/abs/2408.10188)
- [Shu et al. — Video-XL (arXiv:2409.14485)](https://arxiv.org/abs/2409.14485)
- [Wang et al. — VideoAgent (arXiv:2403.10517)](https://arxiv.org/abs/2403.10517)
