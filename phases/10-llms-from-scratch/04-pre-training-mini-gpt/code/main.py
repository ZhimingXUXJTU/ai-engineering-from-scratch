"""Mini GPT —— 从零实现一个完整的 GPT 模型并训练

核心概念：
  - Transformer 架构：Embedding + 多层 Transformer Block + LayerNorm + 线性头
  - 每个 Block 包含：Multi-Head Self-Attention + Feed-Forward Network + 残差连接 + LayerNorm
  - 因果注意力掩码：确保模型只能看到当前位置之前的 token（自回归生成）
  - 手动实现反向传播：逐层计算梯度，理解 Transformer 训练的每个细节

AI 对应：
  - GPT-2 Small 就是这个架构：12 层、12 头、768 维、124M 参数
  - GPT-4 的核心架构也是 Transformer decoder，只是更深更宽并加入了 MoE 等优化
  - 本实现约 0.5M 参数，用纯 NumPy 训练，完整展示预训练过程
"""

import numpy as np


class Embedding:
    """词嵌入 + 位置嵌入层：将 token ID 转换为稠密向量表示

    token_embed：每个 token ID 对应一个 learnable 向量（词表大小 x 嵌入维度）
    pos_embed：每个位置对应一个 learnable 向量（最大序列长度 x 嵌入维度）
    最终嵌入 = 词嵌入 + 位置嵌入，让模型同时知道"是什么词"和"在哪个位置"
    """

    def __init__(self, vocab_size, embed_dim, max_seq_len):
        self.token_embed = np.random.randn(vocab_size, embed_dim) * 0.02
        self.pos_embed = np.random.randn(max_seq_len, embed_dim) * 0.02

    def forward(self, token_ids):
        seq_len = token_ids.shape[-1]
        tok_emb = self.token_embed[token_ids]  # 查表获取每个 token 的嵌入向量
        pos_emb = self.pos_embed[:seq_len]      # 获取前 seq_len 个位置嵌入
        return tok_emb + pos_emb                # 相加得到最终的输入表示


class LayerNorm:
    """层归一化：在每个位置对特征维度做均值=0、方差=1 的标准化

    稳定训练过程中的梯度流，是 Transformer 训练成功的关键组件。
    gamma 和 beta 是可学习参数，允许模型恢复任意的均值和方差。
    """

    def __init__(self, dim, eps=1e-5):
        self.gamma = np.ones(dim)
        self.beta = np.zeros(dim)
        self.eps = eps

    def forward(self, x):
        mean = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True)
        return self.gamma * (x - mean) / np.sqrt(var + self.eps) + self.beta  # 标准化 + 缩放 + 偏移


class MultiHeadAttention:
    """多头自注意力机制：Transformer 的核心组件

    计算 Q*K^T/sqrt(d) 得到注意力分数，再用因果掩码屏蔽未来位置。
    多头让模型能同时关注不同子空间的不同类型关系。
    """
    def __init__(self, embed_dim, num_heads):
        assert embed_dim % num_heads == 0, f"embed_dim {embed_dim} not divisible by num_heads {num_heads}"
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.W_q = np.random.randn(embed_dim, embed_dim) * 0.02
        self.W_k = np.random.randn(embed_dim, embed_dim) * 0.02
        self.W_v = np.random.randn(embed_dim, embed_dim) * 0.02
        self.W_out = np.random.randn(embed_dim, embed_dim) * 0.02

    def forward(self, x, mask=None):
        batch, seq_len, d = x.shape
        Q = (x @ self.W_q).reshape(batch, seq_len, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)  # 线性投影并分头
        K = (x @ self.W_k).reshape(batch, seq_len, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)
        V = (x @ self.W_v).reshape(batch, seq_len, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)

        scores = Q @ K.transpose(0, 1, 3, 2) / np.sqrt(self.head_dim)  # 计算注意力分数: QK^T / sqrt(d_k)
        if mask is not None:
            scores = scores + mask  # 因果掩码：将未来位置的分数设为 -1e9
        weights = np.exp(scores - scores.max(axis=-1, keepdims=True))  # 数值稳定的 softmax
        weights = weights / weights.sum(axis=-1, keepdims=True)
        attn_out = weights @ V  # 加权求和：用注意力权重聚合 Value

        attn_out = attn_out.transpose(0, 2, 1, 3).reshape(batch, seq_len, d)  # 合并多头
        return attn_out @ self.W_out  # 输出投影


class FeedForward:
    """前馈网络 (FFN)：两层线性变换 + ReLU 激活

    这是 Transformer Block 中的"思考"部分，注意力负责收集信息，FFN 负责处理信息。
    中间维度通常是嵌入维度的 4 倍（如 768 -> 3072 -> 768）。
    """
    def __init__(self, embed_dim, ff_dim):
        self.W1 = np.random.randn(embed_dim, ff_dim) * 0.02
        self.b1 = np.zeros(ff_dim)
        self.W2 = np.random.randn(ff_dim, embed_dim) * 0.02
        self.b2 = np.zeros(embed_dim)

    def forward(self, x):
        h = x @ self.W1 + self.b1  # 第一层线性变换
        h = np.maximum(0, h)        # ReLU 激活：max(0, x)
        return h @ self.W2 + self.b2  # 第二层线性变换


class TransformerBlock:
    """Transformer Block：Pre-Norm 架构（先归一化，再注意力/FFN）

    结构：x + Attention(LayerNorm(x))  ->  x + FFN(LayerNorm(x))
    残差连接 (+) 让梯度可以直接流过深层网络，是训练 100+ 层模型的关键。
    """
    def __init__(self, embed_dim, num_heads, ff_dim):
        self.ln1 = LayerNorm(embed_dim)
        self.attn = MultiHeadAttention(embed_dim, num_heads)
        self.ln2 = LayerNorm(embed_dim)
        self.ffn = FeedForward(embed_dim, ff_dim)

    def forward(self, x, mask=None):
        x = x + self.attn.forward(self.ln1.forward(x), mask)  # 残差连接 + 注意力
        x = x + self.ffn.forward(self.ln2.forward(x))          # 残差连接 + FFN
        return x


class MiniGPT:
    """Mini GPT 模型：完整的 GPT-2 风格语言模型

    架构：Embedding -> N x TransformerBlock -> LayerNorm -> 线性头（映射回词表）
    训练目标：预测下一个 token（给定前 k 个 token，预测第 k+1 个）
    """
    def __init__(self, vocab_size=50257, embed_dim=768, num_heads=12,
                 num_layers=12, max_seq_len=1024, ff_dim=3072):
        self.embedding = Embedding(vocab_size, embed_dim, max_seq_len)
        self.blocks = [
            TransformerBlock(embed_dim, num_heads, ff_dim)
            for _ in range(num_layers)
        ]
        self.ln_f = LayerNorm(embed_dim)
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim

    def forward(self, token_ids):
        seq_len = token_ids.shape[-1]
        mask = np.triu(np.full((seq_len, seq_len), -1e9), k=1)  # 因果掩码：上三角为 -1e9

        x = self.embedding.forward(token_ids)  # 词嵌入 + 位置嵌入
        for block in self.blocks:
            x = block.forward(x, mask)           # 通过 N 层 Transformer Block
        x = self.ln_f.forward(x)                # 最终 LayerNorm

        # 权重共享：输出投影复用 token embedding 矩阵（GPT-2 的做法）
        logits = x @ self.embedding.token_embed.T
        return logits

    def count_parameters(self):
        total = 0
        total += self.embedding.token_embed.size
        total += self.embedding.pos_embed.size
        for block in self.blocks:
            total += block.attn.W_q.size + block.attn.W_k.size
            total += block.attn.W_v.size + block.attn.W_out.size
            total += block.ffn.W1.size + block.ffn.b1.size
            total += block.ffn.W2.size + block.ffn.b2.size
            total += block.ln1.gamma.size + block.ln1.beta.size
            total += block.ln2.gamma.size + block.ln2.beta.size
        total += self.ln_f.gamma.size + self.ln_f.beta.size
        return total


def cross_entropy_loss(logits, targets):
    """交叉熵损失：衡量模型预测的 token 分布与真实下一个 token 的差距"""
    batch, seq_len, vocab_size = logits.shape
    logits_flat = logits.reshape(-1, vocab_size)
    targets_flat = targets.reshape(-1)

    max_logits = logits_flat.max(axis=-1, keepdims=True)
    log_softmax = logits_flat - max_logits - np.log(
        np.exp(logits_flat - max_logits).sum(axis=-1, keepdims=True)
    )

    loss = -log_softmax[np.arange(len(targets_flat)), targets_flat].mean()
    return loss


def generate(model, prompt_tokens, max_new_tokens=100, temperature=0.8):
    """自回归生成：每次预测下一个 token，逐步拼接生成完整序列

    temperature 控制生成的随机性：越高越随机（更有创意），越低越确定（更保守）。
    【拓展】GPT-4 的 top-p (nucleus) 采样在此基础上还限制了概率累积阈值，
    而 beam search 则同时追踪多条候选路径。
    """
    tokens = list(prompt_tokens)
    seq_len = model.embedding.pos_embed.shape[0]

    for _ in range(max_new_tokens):
        context = np.array(tokens[-seq_len:]).reshape(1, -1)
        logits = model.forward(context)
        next_logits = logits[0, -1, :]  # 取最后一个位置的 logits（预测下一个 token）

        next_logits = next_logits / temperature  # temperature 缩放
        probs = np.exp(next_logits - next_logits.max())
        probs = probs / probs.sum()  # softmax 得到概率分布

        next_token = np.random.choice(len(probs), p=probs)
        tokens.append(next_token)

    return tokens


def layernorm_backward(dy, x, ln):
    """LayerNorm 反向传播：计算对输入 x、gamma、beta 的梯度"""
    mean = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    std_inv = 1.0 / np.sqrt(var + ln.eps)
    x_hat = (x - mean) * std_inv
    n = x.shape[-1]

    grad_gamma = (dy * x_hat).sum(axis=(0, 1))
    grad_beta = dy.sum(axis=(0, 1))

    dx_hat = dy * ln.gamma
    dvar = (dx_hat * (x - mean) * -0.5 * std_inv ** 3).sum(axis=-1, keepdims=True)
    dmean = (-dx_hat * std_inv).sum(axis=-1, keepdims=True)
    dmean += dvar * (-2.0 / n) * (x - mean).sum(axis=-1, keepdims=True)
    dx = dx_hat * std_inv + dvar * 2.0 * (x - mean) / n + dmean / n

    return dx, grad_gamma, grad_beta


def ffn_backward(dy, x_in, ffn):
    """FFN 反向传播：计算对权重、偏置和输入的梯度"""
    h = x_in @ ffn.W1 + ffn.b1
    h_relu = np.maximum(0, h)

    grad_W2 = h_relu.reshape(-1, h_relu.shape[-1]).T @ dy.reshape(-1, dy.shape[-1])
    grad_b2 = dy.reshape(-1, dy.shape[-1]).sum(axis=0)

    dh_relu = dy @ ffn.W2.T
    dh = dh_relu * (h > 0).astype(float)

    grad_W1 = x_in.reshape(-1, x_in.shape[-1]).T @ dh.reshape(-1, dh.shape[-1])
    grad_b1 = dh.reshape(-1, dh.shape[-1]).sum(axis=0)

    dx = dh @ ffn.W1.T

    return dx, grad_W1, grad_b1, grad_W2, grad_b2


def train_mini_gpt(text, vocab_size=256, embed_dim=128, num_heads=4,
                   num_layers=4, seq_len=64, num_steps=200, lr=3e-4):
    """训练 Mini GPT：手动实现前向传播 + 反向传播 + SGD 更新

    这是 GPT 预训练的核心循环：采样序列 -> 前向计算 loss -> 反向计算梯度 -> 更新权重。
    真实训练使用 PyTorch 自动微分和 AdamW 优化器，但手动实现帮助理解每一步。
    """
    tokens = np.array(list(text.encode("utf-8")[:2048]))
    model = MiniGPT(
        vocab_size=vocab_size, embed_dim=embed_dim, num_heads=num_heads,
        num_layers=num_layers, max_seq_len=seq_len, ff_dim=embed_dim * 4
    )

    print(f"Model parameters: {model.count_parameters():,}")
    print(f"Training tokens: {len(tokens):,}")
    print(f"Config: {num_layers} layers, {num_heads} heads, {embed_dim} dims")
    print()

    for step in range(num_steps):
        start_idx = np.random.randint(0, max(1, len(tokens) - seq_len - 1))
        batch_tokens = tokens[start_idx:start_idx + seq_len + 1]

        input_ids = batch_tokens[:-1].reshape(1, -1)
        target_ids = batch_tokens[1:].reshape(1, -1)

        mask = np.triu(np.full((seq_len, seq_len), -1e9), k=1)
        x = model.embedding.forward(input_ids)
        block_inputs = [x]
        for block in model.blocks:
            x = block.forward(x, mask)
            block_inputs.append(x)
        x_pre_ln = x
        x_normed = model.ln_f.forward(x_pre_ln)
        logits = x_normed @ model.embedding.token_embed.T

        loss = cross_entropy_loss(logits, target_ids)

        batch_size, s_len, v_size = logits.shape
        probs = np.exp(logits - logits.max(axis=-1, keepdims=True))
        probs = probs / probs.sum(axis=-1, keepdims=True)
        dlogits = probs.copy()
        dlogits[np.arange(batch_size)[:, None], np.arange(s_len), target_ids] -= 1.0
        dlogits /= (batch_size * s_len)

        grad_token_embed = np.zeros_like(model.embedding.token_embed)
        for b in range(batch_size):
            grad_token_embed += dlogits[b].T @ x_normed[b]

        dx_normed = dlogits @ model.embedding.token_embed

        dx_pre_ln, grad_ln_gamma, grad_ln_beta = layernorm_backward(
            dx_normed, x_pre_ln, model.ln_f
        )

        dx = dx_pre_ln
        for i in range(len(model.blocks) - 1, -1, -1):
            block = model.blocks[i]
            block_in = block_inputs[i]

            ln2_in = block_in + block.attn.forward(block.ln1.forward(block_in), mask)
            ln2_out = block.ln2.forward(ln2_in)

            dffn, gW1, gb1, gW2, gb2 = ffn_backward(dx, ln2_out, block.ffn)

            dln2_out = dffn
            dln2_in, g_ln2_gamma, g_ln2_beta = layernorm_backward(
                dln2_out, ln2_in, block.ln2
            )

            dx = dx + dln2_in

            block.ffn.W1 -= lr * gW1
            block.ffn.b1 -= lr * gb1
            block.ffn.W2 -= lr * gW2
            block.ffn.b2 -= lr * gb2
            block.ln2.gamma -= lr * g_ln2_gamma
            block.ln2.beta -= lr * g_ln2_beta

        model.ln_f.gamma -= lr * grad_ln_gamma
        model.ln_f.beta -= lr * grad_ln_beta
        model.embedding.token_embed -= lr * grad_token_embed

        if step % 20 == 0:
            print(f"Step {step:4d} | Loss: {loss:.4f}")

    return model


def parameter_breakdown():
    """GPT-2 系列模型的参数量分解：展示各组件如何贡献总参数量"""
    configs = [
        ("GPT-2 Small", 50257, 768, 12, 12, 1024, 3072),
        ("GPT-2 Medium", 50257, 1024, 16, 24, 1024, 4096),
        ("GPT-2 Large", 50257, 1280, 20, 36, 1024, 5120),
        ("GPT-2 XL", 50257, 1600, 25, 48, 1024, 6400),
    ]

    print("GPT-2 Family Parameter Counts")
    print("=" * 65)
    print(f"{'Model':<16} {'Layers':>6} {'Heads':>6} {'Dims':>6} {'Params':>14}")
    print("-" * 65)

    for name, vocab, dim, heads, layers, seq_len, ff in configs:
        token_emb = vocab * dim
        pos_emb = seq_len * dim
        per_block_attn = 4 * dim * dim
        per_block_ff = 2 * dim * ff + dim + ff
        per_block_ln = 4 * dim
        per_block = per_block_attn + per_block_ff + per_block_ln
        final_ln = 2 * dim
        total = token_emb + pos_emb + layers * per_block + final_ln
        print(f"{name:<16} {layers:>6} {heads:>6} {dim:>6} {total:>14,}")

    print()


def memory_estimate():
    """推理时的显存估算：模型权重 + KV Cache

    【拓展】Llama 3 70B 的 KV Cache 在 8K 上下文时约占 32GB，
    这是为什么推理服务需要多卡或使用 GQA/MQA 来减少 KV Cache。
    """
    print("Memory Requirements for Inference (FP16)")
    print("=" * 65)

    models = [
        ("GPT-2 Small (124M)", 124e6, 12, 12, 64, 1024),
        ("Llama 3 8B", 8e9, 32, 32, 128, 8192),
        ("Llama 3 70B", 70e9, 80, 64, 128, 8192),
        ("Llama 3 405B", 405e9, 126, 128, 128, 131072),
    ]

    print(f"{'Model':<24} {'Weights':>10} {'KV Cache':>12} {'Total':>10}")
    print("-" * 65)

    for name, params, layers, heads, head_dim, max_seq in models:
        weight_bytes = params * 2
        kv_per_token = 2 * layers * heads * head_dim * 2
        kv_full = kv_per_token * max_seq
        total = weight_bytes + kv_full

        def fmt(b):
            if b >= 1e9:
                return f"{b / 1e9:.1f} GB"
            return f"{b / 1e6:.0f} MB"

        print(f"{name:<24} {fmt(weight_bytes):>10} {fmt(kv_full):>12} {fmt(total):>10}")

    print()


if __name__ == "__main__":
    np.random.seed(42)

    parameter_breakdown()
    memory_estimate()

    corpus = """The transformer architecture has revolutionized natural language processing.
Attention mechanisms allow the model to focus on relevant parts of the input.
Self-attention computes relationships between all pairs of positions in a sequence.
Multi-head attention splits the representation into multiple subspaces.
Each attention head can learn different types of relationships.
The feedforward network provides nonlinear transformations at each position.
Residual connections enable gradient flow through deep networks.
Layer normalization stabilizes training by normalizing activations.
Position embeddings give the model information about token ordering.
The causal mask ensures autoregressive generation during training.
Pre-training on large text corpora teaches the model general language understanding.
Fine-tuning adapts the pre-trained model to specific downstream tasks."""

    print("Training Mini GPT")
    print("=" * 65)
    model = train_mini_gpt(corpus, num_steps=200)

    prompt = list("The transformer".encode("utf-8"))
    print(f"\nPrompt: 'The transformer'")
    print("Generating...")
    output_tokens = generate(model, prompt, max_new_tokens=100, temperature=0.8)
    generated_text = bytes(output_tokens).decode("utf-8", errors="replace")
    print(f"Generated: {generated_text}")
