# Mixture of Experts (MoE) | 混合专家模型 (MoE)

> 一个稠密 70B Transformer 为每个 token 激活所有参数。一个 671B MoE 每个 token 只激活 37B，在每个基准测试上击败它。稀疏是这个十年最重要的扩展思路。

> **【中文解读】** MoE 只激活部分专家网络处理每个 token，大幅增加参数量而不增加计算量。DeepSeek、Mixtral 都用 MoE 架构。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 7 · 05（完整 Transformer），阶段 7 · 07（GPT）
**时长：** 约 45 分钟

## 问题引入

稠密 Transformer 推理时的 FLOP 等于其参数量（前向传播乘以 2）。扩展稠密模型，每个 token 都要付全款。到 2024 年，前沿正在触及计算墙：要有意义地更聪明，你需要呈指数增长的每 token FLOP。

混合专家打破了这种联系。将每个 FFN 替换为 `E` 个独立专家 + 一个路由器，每个 token 选择 `k` 个专家。总参数 = `E × FFN_size`。每个 token 的活跃参数 = `k × FFN_size`。典型的 2026 年配置：`E=256`，`k=8`。存储随 `E` 缩放，计算随 `k` 缩放。

2026 年的前沿几乎全是 MoE：DeepSeek-V3（671B 总 / 37B 活跃），Mixtral 8×22B，Qwen2.5-MoE，Llama 4，Kimi K2，gpt-oss。在 Artificial Analysis 的独立排行榜上，前 10 名开源模型都是 MoE。

> **【中文解读】** MoE 打破了"参数量 = 计算量"的等式。每个 FFN 层替换为 E 个独立专家 + 路由器，每 token 只激活 k 个专家。总参数量随 E 增长，但每个 token 的计算量只随 k 增长。典型配置 E=256, k=8，存储随 E 缩放，计算随 k 缩放。这是 2020 年代最重要的扩展思路。

> **【拓展：DeepSeek-V3 的 MoE 创新】** DeepSeek-V3 拥有 671B 总参数但每 token 只激活 37B——通过 256 个路由专家 + 1 个共享专家实现。它还引入了辅助损失无关的负载均衡策略，避免了传统 MoE 的路由崩塌问题。在 Artificial Analysis 排行榜上，DeepSeek-V3 以不到 GPT-4 十分之一的推理成本达到了可比的性能。

## 核心概念

![MoE 层：路由器每 token 选择 E 个专家中的 k 个](../assets/moe.svg)

### FFN 替换

稠密 Transformer 块：

```
h = x + attn(norm(x))
h = h + FFN(norm(h))
```

MoE 块：

```
h = x + attn(norm(x))
scores = router(norm(h))              # (N_tokens, E)
top_k = argmax_k(scores)              # 每 token 选择 k/E
h = h + sum_{e in top_k}(
        gate(scores[e]) * Expert_e(norm(h))
    )
```

每个专家是一个独立的 FFN（通常是 SwiGLU）。路由器是单个线性层。每个 token 选择自己的 `k` 个专家，并获得它们输出的门控混合。

### 负载均衡问题

如果路由器将 90% 的 token 送到专家 3，其他专家就会挨饿。已尝试三种修复：

1. **辅助负载均衡损失**（Switch Transformer、Mixtral）。添加与专家使用方差成正比的惩罚。有效，但增加了超参数和第二个梯度信号。
2. **专家容量 + token 丢弃**（早期 Switch）。每个专家最多处理 `C × N/E` 个 token；溢出的 token 跳过该层。损害质量。
3. **辅助损失无关均衡**（DeepSeek-V3）。添加学习的每专家偏置，移动路由器的 top-k 选择。偏置在训练损失之外更新。不对主目标施加惩罚。2024 年的重大突破。

DeepSeek-V3 的方法：每个训练步骤后，对每个专家检查其使用量是高于还是低于目标。以 `±γ` 微调偏置。选择使用 `scores + bias`。用于门控的专家概率是未改变的原始 `scores`。将路由与表达解耦。

### 共享专家

DeepSeek-V2/V3 还将专家分为*共享的*和*被路由的*。每个 token 通过所有共享专家。被路由的专家通过 top-k 选择。共享专家捕获通用知识；被路由的专家专门化。V3 运行 1 个共享专家加上 256 个被路由专家中的 top-8。

### 细粒度专家

经典 MoE（GShard、Switch）：每个专家和完整 FFN 一样宽。`E` 很小（8-64），`k` 很小（1-2）。

现代细粒度 MoE（DeepSeek-V3、Qwen-MoE）：每个专家更窄（1/8 FFN 大小）。`E` 很大（256+），`k` 更大（8+）。总参数相同，但组合增长快得多。`C(256, 8) = 400 万亿`种可能的"专家"每 token。质量上升，延迟持平。

> **【拓展：MoE 的路由崩塌问题】** MoE 训练中的核心挑战是路由崩塌（router collapse）——路由器可能将大部分 token 分配给少数几个专家，导致其他专家得不到训练。解决方案包括：辅助损失（auxiliary loss）鼓励均匀分配、噪声注入（在路由决策前加随机扰动）、DeepSeek-V3 的辅助损失无关负载均衡策略。

### 成本概况

每 token，每层：

| 配置 | 每 token 活跃参数 | 总参数 |
|------|-------------------|--------|
| Mixtral 8×22B | 约 39B | 141B |
| Llama 3 70B（稠密） | 70B | 70B |
| DeepSeek-V3 | 37B | 671B |
| Kimi K2（MoE） | 约 32B | 1T |

DeepSeek-V3 在几乎每个基准测试上击败 Llama 3 70B（稠密），同时每 token 的**活跃 FLOP 更少**。更多参数 = 更多知识。更多活跃 FLOP = 每 token 更多计算。MoE 解耦了它们。

### 代价：内存

所有专家都在 GPU 上，无论哪些被激活。671B 模型在 fp16 权重下需要约 1.3 TB 显存。前沿 MoE 部署需要专家并行——将专家分片到多个 GPU 上，跨网络路由 token。延迟主要由 all-to-all 通信决定，而非矩阵乘法。

> **【中文解读】** MoE 的核心权衡：用内存换计算。DeepSeek-V3 以 37B 活跃参数达到超越 70B 稠密模型的性能，但需要 1.3TB 显存存储所有专家。这推动了专家并行（expert parallelism）技术的发展——将专家分散到多个 GPU 上，通过网络路由 token。

> **【拓展：细粒度专家 vs 粗粒度专家】** 传统 MoE（Switch Transformer）使用少量大型专家（E=8-64）。现代细粒度 MoE（DeepSeek-V3）使用大量小型专家（E=256+），每个专家只有 1/8 的 FFN 宽度。组合数 C(256,8) 约为 400 万亿种，远超粗粒度的组合空间。质量提升显著，延迟基本不变。

## 动手实现

参见 `code/main.py`。纯标准库的紧凑 MoE 层，包含：

- `n_experts=8` 个类 SwiGLU 专家（各一个线性层，用于示意）
- top-k=2 路由
- softmax 归一化的门控权重
- 通过每专家偏置实现辅助损失无关均衡

### 步骤 1：路由器

```python
def route(hidden, W_router, top_k, bias):
    scores = [sum(h * w for h, w in zip(hidden, W_router[e])) for e in range(len(W_router))]
    biased = [s + b for s, b in zip(scores, bias)]
    top_idx = sorted(range(len(biased)), key=lambda i: -biased[i])[:top_k]
    # 对选中专家的原始分数做 softmax
    chosen = [scores[i] for i in top_idx]
    m = max(chosen)
    exps = [math.exp(c - m) for c in chosen]
    s = sum(exps)
    gates = [e / s for e in exps]
    return top_idx, gates
```

偏置影响选择，不影响门控权重。这就是 DeepSeek-V3 的技巧——偏置纠正负载不均衡而不引导模型的预测。

### 步骤 2：通过路由器运行 100 个 token

跟踪哪些专家被激活多少次。没有偏置时，使用量是偏斜的。通过偏置更新循环（过度使用的专家 `-γ`，使用不足的 `+γ`），使用量在几次迭代后收敛到均匀分布。

### 步骤 3：参数量比较

打印 MoE 配置的"稠密等价"。DeepSeek-V3 形状：256 个被路由 + 1 个共享，8 个活跃，d_model=7168。总参数量令人瞠目。活跃数量是稠密 Llama 3 70B 的七分之一。

## 用框架实现

HuggingFace 加载：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-8x22B-v0.1")
```

2026 年生产推理：vLLM 原生支持 MoE 路由。SGLang 拥有最快的专家并行路径。两者都自动处理 top-k 选择和专家并行。

**何时选择 MoE：**
- 你想要更低推理成本下的前沿质量。
- 你有显存/专家并行基础设施。
- 你的工作负载是 token 密集型（聊天、代码）而非上下文密集型（长文档）。

**何时不选 MoE：**
- 边缘部署——你为任何活跃 FLOP 付全部存储代价。
- 延迟敏感的单用户服务——专家路由增加开销。
- 小型模型（<7B）——MoE 的质量优势只在计算阈值以上（约 6B 活跃参数）才出现。

## 产出物

参见 `outputs/skill-moe-configurator.md`。该技能为新 MoE 选择 E、k 和共享专家布局，给定参数预算、训练 token 和部署目标。

## 练习题

1. **简单。** 运行 `code/main.py`。观察辅助损失无关偏置更新如何在 50 次迭代中均匀化专家使用。
2. **中等。** 用基于哈希的路由器（确定性，无学习）替换学习路由器。比较质量和均衡性。为什么学习路由器更好？
3. **困难。** 实现 GRPO 风格的"rollout-matched routing"（DeepSeek-V3.2 技巧）：记录推理时哪些专家被激活，在梯度计算时强制相同路由。在玩具策略梯度设置上测量效果。

## 术语速查表

| 术语 | 人们的说法 | 实际含义 |
|------|-----------|---------|
| 专家 (Expert) | "众多 FFN 之一" | 独立的前馈网络；专用于 FFN 计算稀疏切片的参数。 |
| 路由器 (Router) | "门" | 一个微型线性层，将每个 token 与每个专家评分；top-k 选择。 |
| Top-k 路由 | "每 token k 个活跃专家" | 每个 token 的 FFN 计算恰好通过 k 个专家，按门控加权。 |
| 辅助损失 | "负载均衡惩罚" | 惩罚偏斜专家使用的额外损失项。 |
| 辅助损失无关 | "DeepSeek-V3 的技巧" | 仅通过路由器选择上的每专家偏置均衡；无额外梯度。 |
| 共享专家 | "始终开启" | 每个 token 都通过的额外专家；捕获通用知识。 |
| 专家并行 | "按专家分片" | 将不同专家分配到不同 GPU；跨网络路由 token。 |
| 稀疏度 | "活跃参数 < 总参数" | 比率 `k × expert_size / (E × expert_size)`；DeepSeek-V3 为 37/671 ≈ 5.5%。 |

## 延伸阅读

- [Shazeer 等人（2017）。Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://arxiv.org/abs/1701.06538) —— 这个想法。
- [Fedus, Zoph, Shazeer（2022）。Switch Transformer: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://arxiv.org/abs/2101.03961) —— Switch，经典 MoE。
- [Jiang 等人（2024）。Mixtral of Experts](https://arxiv.org/abs/2401.04088) —— Mixtral 8×7B。
- [DeepSeek-AI（2024）。DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437) —— MLA + 辅助损失无关 MoE + MTP。
- [Wang 等人（2024）。Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts](https://arxiv.org/abs/2408.15664) —— 基于偏置的均衡论文。
- [Dai 等人（2024）。DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models](https://arxiv.org/abs/2401.06066) —— 本课路由器使用的细粒度 + 共享专家拆分。
- [Kim 等人（2022）。DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training](https://arxiv.org/abs/2201.05596) —— 原始共享专家论文。
