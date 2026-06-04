# Speculative Decoding — Draft, Verify, Repeat | 推测解码 — 草案、验证、重复

> 自回归解码是串行的。每个 token 等待前一个。推测解码打破链条：廉价模型起草 N 个 token，昂贵模型一次前向传播验证所有 N 个。当草案正确时，你为 N 次生成付了一次大模型前向传播。

> **【中文解读】** 用小模型快速生成候选 token，大模型批量验证。可以加速推理 2-3 倍而不降低质量。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 7 · 07（GPT 因果 LM），阶段 7 · 12（KV Cache & Flash Attention）
**时长：** 约 60 分钟

## 问题引入

一个 70B LLM 采样一个 token 在 H100 上约需 30 ms。一个 3B 草案模型约需 3 ms。如果我们让 3B 模型提前起草 5 个 token，然后运行 70B *一次*验证所有 5 个，总计 `5×3 + 30 = 45 ms` 最多可以接受 5 个 token——而直接生成是 `5×30 = 150 ms`。这就是推测解码的全部推销：用少量额外的 GPU 内存（草案模型）换取 2-4 倍更低的解码延迟。

这个技巧必须保持分布不变。推测采样，由 Leviathan 等人（2023）和 Chen 等人同时引入，保证输出序列与大模型自己产生的分布**完全相同**。没有质量权衡。只是更快。

四族草案-验证器对主导 2026 年推理：

1. **朴素推测（Leviathan 2023）。** 独立的草案模型（例如 Llama 3 1B）+ 验证器（例如 Llama 3 70B）。
2. **Medusa（Cai 2024）。** 验证器上的多个解码头并行预测位置 `t+1..t+k`。无独立草案模型。
3. **EAGLE 家族（Li 2024, 2025）。** 轻量草案复用验证器的隐藏状态；比朴素更高的接受率；典型 3-4 倍。
4. **Lookahead 解码（Fu 2024）。** Jacobi 迭代；完全不需要草案模型。自推测。小众但无依赖。

2026 年每个生产推理栈默认发布推测解码。vLLM、TensorRT-LLM、SGLang 和 llama.cpp 都至少支持朴素 + EAGLE-2。

> **【中文解读】** 推测解码的核心洞察：自回归生成是串行的瓶颈。用小模型（3B）快速生成 N 个候选 token，大模型（70B）一次前向传播验证所有 N 个。总时间从 N×30ms 降到 5×3+30=45ms，加速 2-4 倍。关键：推测采样保证输出分布与大模型完全一致，无质量损失。

> **【拓展：EAGLE 与 Medusa 的自推测策略】** EAGLE（2024）复用大模型的隐藏状态来生成草案，接受率比独立小模型更高，典型加速 3-4 倍。Medusa 在大模型上添加多个解码头，并行预测多个未来位置，无需额外模型。这两种"自推测"策略避免了维护独立草案模型的开销，成为 2026 年的主流选择。

## 核心概念

### 核心算法

给定验证器 `M_q` 和更便宜的草案 `M_p`：

1. 设 `x_1..x_k` 为已解码的前缀。
2. **草案**：用 `M_p` 自回归地提出 `d_{k+1}, d_{k+2}, ..., d_{k+N}`，带草案概率 `p_1..p_N`。
3. **并行验证**：在 `x_1..x_k, d_{k+1}, ..., d_{k+N}` 上运行 `M_q` 一次，获得位置 `k+1..k+N+1` 的验证器概率 `q_1..q_{N+1}`。
4. **从左到右接受/拒绝每个草案 token**：对每个 `i`，以概率 `min(1, q_i(d_i) / p_i(d_i))` 接受。
5. 在位置 `j` 首次拒绝时：从"残差"分布 `(q_j - p_j)_+` 归一化后采样 `t_j`。`j` 之后的所有草案被丢弃。
6. 接受所有 `N` 个时：从 `q_{N+1}` 采样一个额外 token `t_{N+1}`（免费奖励 token）。

残差分布技巧是保持输出分布与 `M_q` 从头采样完全相同的数学洞察。

### 什么决定加速

设 `α` = 每个草案 token 的预期接受率。设 `c` = 草案与验证器的成本比。每步：

- 朴素生成每 token 做 1 次大模型调用。
- 推测在 `α` 较高时每 `(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)` 个 token 做 1 次大模型调用。

`α = 0.75` 和 `N = 5` 时的典型经验法则：大模型调用减少约 3 倍。草案成本是 5 倍廉价。总时间下降约 2.5 倍。

> **【中文解读】** 加速效果取决于接受率 alpha。当 alpha=0.75、草案长度 N=5 时，大约 3 倍减少大模型调用。残差分布（residual distribution）是保持分布一致性的数学关键——拒绝时从 (q-p)+ 归一化分布中采样，确保最终输出与大模型直接采样的分布完全一致。

**α 取决于：**

- 草案对验证器的近似程度。同家族/同训练数据显著提升 α。
- 解码策略。贪心草案对贪心验证器：高 α。温度采样：更难匹配；接受率下降。
- 任务类型。代码和结构化输出接受更多（可预测）；自由创意写作接受较少。

### Medusa——无草案模型的草案

Medusa 用验证器上的额外输出头替换草案模型。在位置 `t`：

```
共享主干 → 隐藏状态 h_t
    ├── head_0：预测 t+1 位置的 token（标准 LM 头）
    ├── head_1：预测 t+2 位置的 token
    ├── head_2：预测 t+3 位置的 token
    ├── head_3：预测 t+4 位置的 token
```

每个头输出自己的 logits。推理时从每个头采样得到候选序列，然后用树注意力方案一次前向验证所有候选延续。

优点：不需要第二个模型。缺点：增加可训练参数；需要监督微调阶段（约 1B token）；接受率比有良好草案模型的朴素推测略低。

> **【拓展：推测解码在 vLLM 中的实现】** vLLM 是 2026 年最流行的 LLM 推理框架，原生支持推测解码。它使用 continuous批处理（continuous batching）+ PagedAttention + 推测解码的组合优化。在生产部署中，推测解码通常带来 2-3 倍的延迟降低，对于聊天场景（用户感知延迟敏感）尤为关键。结合量化（AWQ/GPTQ），可以在单张 GPU 上实现高性能推理。

### EAGLE——通过复用隐藏状态获得更好的草案

EAGLE-1/2/3（Li 等人，2024-2025）使草案模型成为一个小型 Transformer（通常 1 层），摄入验证器的最后一层隐藏状态。因为草案看到了验证器的特征表示，其预测与验证器的输出分布强相关。接受率从约 0.6（朴素）攀升到 0.85+。

EAGLE-3（2025）添加了候选延续上的树搜索。vLLM 和 SGLang 将 EAGLE-2/3 作为 Llama 3/4 和 Qwen 3 的默认推测路径。

### KV 缓存舞蹈

验证在单次前向传播中将 `N` 个草案 token 送入验证器。这将验证器的 KV 缓存扩展了 `N` 个条目。如果一些草案被拒绝，你必须将缓存回滚到接受的前缀长度。

生产实现（vLLM 的 `--speculative-model`，TensorRT-LLM 的 LookaheadDecoder）用临时 KV 缓冲区处理这个问题。先写，接受时提交。概念上不难，但细节繁琐。

## 动手实现

参见 `code/main.py`。我们用以下内容实现核心的推测采样算法（拒绝步骤 + 残差分布）：

- 一个"大模型"，是手工编码分布上的确定性 softmax（这样我们可以解析地验证接受数学）。
- 一个"草案模型"，是大模型的扰动。
- 一个接受/拒绝循环，产生与直接采样相同的边际分布。

### 步骤 1：拒绝步骤

```python
def accept_or_reject(q_prob, p_prob, draft_token, u):
    ratio = q_prob / p_prob if p_prob > 0 else float("inf")
    return u < min(1.0, ratio)
```

`u` 是均匀随机数。`q_prob` 是验证器对草案 token 的概率。`p_prob` 是草案模型的概率。Leviathan 定理是，这个伯努利决策后接拒绝时从残差采样，精确保持验证器的分布。

### 步骤 2：残差分布

```python
def residual_dist(q, p):
    raw = [max(0.0, qi - pi) for qi, pi in zip(q, p)]
    s = sum(raw)
    return [r / s for r in raw]
```

从 `q` 逐元素减去 `p`，将负值钳位为零，重新归一化。在任何拒绝时从该分布采样。

### 步骤 3：一个推测步骤

```python
def spec_step(prefix, q_model, p_model, N, rng):
    drafts = []
    p_probs = []
    ctx = list(prefix)
    for _ in range(N):
        p_dist = p_model(ctx)
        d = sample(p_dist, rng)
        drafts.append(d)
        p_probs.append(p_dist[d])
        ctx.append(d)

    q_dists = [q_model(prefix + drafts[:i]) for i in range(N + 1)]

    for i, d in enumerate(drafts):
        u = rng.random()
        q_prob = q_dists[i][d]
        p_prob = p_probs[i]
        if u < min(1.0, q_prob / p_prob if p_prob > 0 else float("inf")):
            prefix = prefix + [d]
        else:
            res = residual_dist(q_dists[i], p_model(prefix))
            prefix = prefix + [sample(res, rng)]
            return prefix
    prefix = prefix + [sample(q_dists[N], rng)]
    return prefix
```

五个被接受 → 一个奖励 → 一次验证器传递产生六个 token。

### 步骤 4：测量接受率

在不同草案质量水平下运行 10,000 个推测步骤。绘制接受率 vs 草案和验证器分布之间的 KL 散度。你应该看到清晰的单调关系。

### 步骤 5：验证分布等价性

经验上：推测循环产生的 token 直方图应该与直接从验证器采样产生的直方图匹配。这是实践中的 Leviathan 定理。卡方检验在采样误差内确认。

## 用框架实现

生产环境：

```bash
# vLLM 带 EAGLE
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model /models/llama-3.1-eagle-70b \
    --speculative-draft-tensor-parallel-size 1 \
    --num-speculative-tokens 5

# vLLM 带朴素草案模型
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model meta-llama/Llama-3.2-1B-Instruct \
    --num-speculative-tokens 5
```

TensorRT-LLM 截至 2026 年中期有最快的 Medusa 路径。`faster-whisper` 用小型草案为 Whisper-large 包装了推测解码。

**选择草案：**

| 策略 | 何时选择 | 加速 |
|------|---------|------|
| 朴素草案（1B/3B Llama 家族） | 快速原型，无需训练 | 1.8-2.3× |
| Medusa 头 | 你可以微调验证器 | 2-3× |
| EAGLE-2 / 3 | 生产环境，最大速度 | 3-4× |
| Lookahead | 无草案，无训练，无额外参数 | 1.3-1.6× |

**何时不使用推测解码：**

- 1-5 个 token 的单序列生成。开销占主导。
- 高度创意/高温度采样（α 下降）。
- 内存受限的部署（草案模型增加显存）。

## 产出物

参见 `outputs/skill-spec-decode-picker.md`。该技能为新的推理工作负载选择推测解码策略（朴素 / Medusa / EAGLE / lookahead）和调优参数（N，草案温度）。

## 练习题

1. **简单。** 运行 `code/main.py`。确认 50,000 个 token 上的推测 token 分布在卡方 p > 0.05 范围内匹配验证器的直接采样分布。
2. **中等。** 绘制加速（每大模型前向传播的 token 数）作为 `N` 的函数，`α = 0.5, 0.7, 0.85`。确定每个 α 的最优 `N`。（提示：每验证调用的预期 token = `(1 - α^{N+1}) / (1 - α)`。）
3. **困难。** 实现微型 Medusa：取第 14 课的毕业 GPT，添加 3 个预测位置 t+2、t+3、t+4 的额外 LM 头。在 tinyshakespeare 上用联合多头损失训练。与截断同一模型制作的朴素草案比较接受率。
4. **困难。** 实现回滚：从一个 10-token 前缀 KV 缓存开始，送入 5 个草案 token，模拟位置 3 的拒绝。验证你的缓存在下一次迭代时正确读取"前缀 + 前 2 个被接受的草案"。

## 术语速查表

| 术语 | 人们的说法 | 实际含义 |
|------|-----------|---------|
| 草案模型 | "便宜的那个" | 提出候选 token 的更小模型；通常比验证器便宜 10-50 倍。 |
| 验证器 | "大的那个" | 我们保持其分布的目标模型；每次推测步骤运行一次。 |
| 接受率 (α) | "草案多久正确一次" | 验证器接受草案的每 token 概率。0.7-0.9 为典型。 |
| 残差分布 | "拒绝的回退" | `(q - p)_+` 归一化；拒绝时从此采样保持验证器的分布。 |
| 奖励 token | "免费的那个" | 当所有 N 个草案被接受时，从验证器的下一步分布多采样一个。 |
| Medusa | "无草案的推测" | 验证器上的多个 LM 头并行预测位置 t+1..t+k。 |
| EAGLE | "隐藏状态草案" | 以验证器最后一层隐藏状态为条件的小型 Transformer 草案。 |
| Lookahead 解码 | "Jacobi 迭代" | 使用不动点迭代的自推测；无草案模型。 |
| 树注意力 | "一次验证多个候选" | 同时考虑多个草案延续的分支验证。 |
| KV 回滚 | "撤销被拒绝的草案" | 临时 KV 缓冲区；接受时提交，拒绝时丢弃。 |

## 延伸阅读

- [Leviathan, Kalman, Matias（2023）。Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) —— 核心算法和等价定理。
- [Chen 等人（2023）。Accelerating Large Language Model Decoding with Speculative Sampling](https://arxiv.org/abs/2302.01318) —— 同时引入；干净的伯努利拒绝证明。
- [Cai 等人（2024）。Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) —— Medusa 论文；树注意力验证。
- [Li 等人（2024）。EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) —— EAGLE-1；隐藏状态条件草案。
- [Li 等人（2024）。EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees](https://arxiv.org/abs/2406.16858) —— EAGLE-2；动态树深度。
- [Li 等人（2025）。EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test](https://arxiv.org/abs/2503.01840) —— EAGLE-3。
- [Fu 等人（2024）。Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](https://arxiv.org/abs/2402.02057) —— lookahead，无草案方法。
- [vLLM 文档 — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode.html) —— 规范的生产参考，接入了所有四种策略。
- [SafeAILab / EAGLE 参考实现](https://github.com/SafeAILab/EAGLE) —— EAGLE-1/2/3 的参考代码。
