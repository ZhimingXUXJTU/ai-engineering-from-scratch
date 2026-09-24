# 现在,我们可以在线观看,看看,看看,看看,看看,看看,看看,看看看,看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看看,看看,看看,看看,看看,看看,看看,看看,看看,看看,看看,看看,看看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,看,

> 训练是平行的,FLOP的. 推理是序列的,记忆的. 不同的瓶,不同的技巧.

> **【中文解读】**缓存已计算的关键/值 避免重复计算,是 LLM 推理加速的核心.

**Type:** Hands-on | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

一个天真的自动降解器可以`O(N²)`工作要产生`N`代币:在每一步上,它重新计算注意力在完整的预先代币上.对于4K代币响应,这是16M注意力操作,其中大多数是冗余的.一个预先代币的每个隐藏状态是确定性的,一旦计算了,你只需要运行新的代币的查询与之前所有东西的缓存键和值.

> 一个简单的自归解码器生成器`N`个标志需要`O(N²)`工作量:每一步都对完整的前重新计算注意力.对于4K代币的响应,那就是16M次的注意力操作,其中大部分是冗余的.

另外,注意力本身移动了大量数据.标准注意力实现了N×N分数矩阵,N×d软max输出,N×d最终输出 读写太多.对于N≥2K,注意力在成为FLOP之前会被绑定到内存.经典注意力内核使用现代GPU不足410×.

> 除此之外,注意力本身需要移动大量数据――标准注意力会产生N×N 分数矩阵、N×d软max 输出、N×d 最终输出对HBM的读写次数过多――当N≥2K时,注意力在成为FLOP瓶之前,首先成为内存瓶──经典注意力内核对现代GPU的利用率仅为4-10倍差异――

两种优化,来自达和其他,将边界推断从"慢"转化为"快":

> 两种优化都来自道人等.

1. **KV cache.**存储每个预सर्ग代币的K和V向量.每个新代币的注意力是一个查询对缓存键. 推理减少了`O(N²)`为了`O(N)`对于每一代的步骤.
   翻译: 中文**KV 缓存。**存储每个前代币的K 和 V 向量――每个新代币的注意力是对缓存键的一次查询――推理从每一步`O(N²)`降低到`O(N)`,我知道.
2. **Flash Attention.**切注意计算,使N×N矩阵永远不会达到HBM.所有软max + matmul都发生在SRAM中.A100上24×墙钟速度加快;FP8上H100上510×.
   翻译: 中文**Flash Attention。**将注意力计算分块,使完整的N×N矩阵永远不写入HBM──所有软max+矩阵乘法都在SRAM中完成──A100上 2-4倍加速;H100上 FP8可达 5-10倍──

到2026年,这两种模型都将成为通用的.每个生产推理堆 (vLLM,TensorRT-LLM,SGLang, llama.cpp) 都会假设它们.每个边境模型船只都能使用Flash Attention.

> 到2026年,两者都已经普及了.每个生产推系统都假设使用它们.

> **【中文解读】**推理优化两大核心技术:KV缓存 已计算的关键/值向量,避免重复计算,将每步推理从O(N^2) 降至O(N);Flash 注意 通过分块计算避免N×N矩阵写入HBM,在SRAM完成所有计算,速度提升2-10倍.

## 概念的核心概念

![KV cache growth and Flash Attention tiling](../assets/kv-cache-flash-attn.svg)

### 预存计算

每个解码器层,每个代币,每个头:

> 每个解码器层,每一个代币,每一个头:

```
bytes_per_token_per_layer = 2 * d_head * dtype_size
                          ^
                          K and V
```

对于7B型号,有32层,32头,d_head=128,fp16:

> 对于7B模型 ((32层、32头、d_head=128、fp16):

```
per token per layer = 2 * 128 * 2 = 512 bytes
per token (32 layers) = 16 KB
per 32K context = 512 MB
```

> **【拓展：GQA 对 KV 缓存的影响】**查头/8KV头配置,将KV缓存压缩8倍. 在128K上下文中,这将从约4GB下降到0.5GB的KV缓存,是长上下文推理的关键优化.

对于Llama 3 70B (80层,d_head=128,GQA 8 KV头):

> 对于拉马370B ((80层、d_head=128、GQA 8个KV头):

```
per token per layer = 2 * 8 * 128 * 2 = 4096 bytes (4 KB)
per 32K context = 10.4 GB
```

这10GB是为什么Llama370B在128K环境中需要大部分40GBA100只为KV缓存在批量1.

> 这就是为什么10GB的Llama370B在128K上下文下仅KV缓存 (批量大小1)

**GQA is the KV-cache win.**只有64个头的MHA将是32GB.

> **GQA 是 KV 缓存的胜利。**需要32GB的MHA.
拉取尺寸,看缓存尺寸移动. 按下序列长度或批量,看它在单个GPU上爆炸的速度:

```figure
kv-cache-sizer
```

###  片技巧

标准注意力:

> 标准注意力:

```
S = Q @ K^T          (HBM read, N×N, HBM write)
P = softmax(S)       (HBM read, HBM write)
O = P @ V            (HBM read, HBM write)
```

在H100上,HBM带宽为3TB/s;SRAM为30TB/s.每次HBM旅行都是10倍的减速相比,保持一切在芯片上.

> 在H100上,HBM带宽为3TB/s;SRAM为30TB/s. 每次HBM访问比在片上保持所有数据慢10倍.

闪光注意:

```
for each block of Q (tile size ~128 × 128):
    load Q_tile into SRAM
    for each block of K, V:
        load K_tile, V_tile into SRAM
        compute S_tile = Q_tile @ K_tile^T     (SRAM)
        running softmax aggregation             (SRAM)
        accumulate into O_tile                  (SRAM)
    write O_tile to HBM
```

每每次一次HBM旅行,总记忆足迹从`O(N²)`为了`O(N)`后传输将从前传输中重新计算一些值,而不是存储它们另一个记忆获取.

> 每个,一次HBM访问.`O(N²)`降到`O(N)`△反向传播 从前向传播中重新计算某些值而不是存储它们另一个内存优势.

**Numerical trick.**运行软max保持`(max, sum)`闪光注意力计算的比特相同输出标准注意力 (模块fp16非关联性).

> **数值技巧。**运行时软max 跨 维护 `(max, sum)`对,确保最终归结是精确的. 不近似的.

> **【中文解读】**闪光注意的核心技巧:将注意力计算分块 () 在 GPU 的快速 SRAM 中完成软max 和矩阵乘法,避免将 N×N 的中间矩阵写入慢速 HBM。关键数值技巧是"运行时软max"跨 维护 (最大,总量),确保最终结果与标准注意力数学完全一致,不是近似──

> **【拓展：vLLM 的 PagedAttention】**页面注意(vLLM) 将将KV缓存组织为固定大小的"页",类似操作系统的虚拟内存. 这消除了内存碎片问题,使多个并发请求能够高效共享GPU显存.

**Version evolution:**

| Version | Year | Key change | Speedup on reference hardware |
|---------|------|-----------|-------------------------------|
| 版本 | 年份 | 关键变化 | 参考硬件上的加速 |
| Flash 1 | 2022 | Tiled SRAM kernel | 2× on A100 |
| Flash 2 | 2023 | Better parallelism, causal-first ordering | 3× on A100 |
| Flash 3 | 2024 | Hopper asynchrony, FP8 | 1.5–2× on H100 (~740 TFLOPs FP16) |
| Flash 4 | 2026 | Blackwell 5-stage pipeline, software exp2 | Inference-first (forward only initially) |

4仅在发射时才会通过.训练仍然使用Flash 3.GQA和varlen支持Flash 4正在等待 (2026年中期).

> 发行时仅支持前向传播;;训练仍使用Flash 3;;Flash 4的GQA 和变长支持待定(2026年中)。

### 其他延迟获胜

廉价模型提出N代币.大模型并行验证所有N代币.如果验证接受k代币,则你为k代代币支付1个大模型前行通行.典型的k=35在代码和散文中.

> 廉价模型提出了N 个代币――大模型并行验证所有N 个――如果验证接受了K 个代币,你用一次大模型前向传播获得了K 个生成――代码和散文的典型K=3-5――

2026 违约:
- **EAGLE 2 / Medusa.**通过互联网,我们可以实现快速化,
  翻译: 中文**EAGLE 2 / Medusa。**集成草案头,共享验证器的隐藏状态──2-3倍加速,无质量损失──
- **Speculative decoding with draft model.**消费者硬件的速度增加了24倍.
  翻译: 中文**带草案模型的推测解码。**消费级硬件上 2-4 倍加速.
- **Lookahead decoding.**没有草稿模型,但是免费的.
  翻译: 中文**前瞻解码。**代·不需要草案模型──小众但免费──

### 连续批发

典型的批量推断:等待最慢的序列完成,然后开始新的批量.

> 经典批量推理:等待最慢的序列完成,然后开始新批次――短响应提前完成时浪费GPU――

连续批发 (首先出货在Orca,现在在vLLM,TensorRT-LLM,SGLang):在旧批发完成后,将新请求交换到批发中.

> 连续批处理(首次在Orca中发布,现在在vLLM、TensorRT-LLM、SGLang 中):旧请求完成后立即将新请求换入批次――典型聊天工作负载的吞吐量提升5-10倍――

### 页面注意  KV缓存作为虚拟内存

维LLM的主题功能.KV缓存分为16个代币块;一个页面表将逻辑位置映射到物理块.允许您共享KV在并行样本中 (光束搜索,并行样本采集),热交换预先设用于快速缓存,以及消碎内存.

> 基于此,KV 缓存将逻辑位置映射到物理块. 允许跨并行样本.

## 建立它,实现它.
```figure
flash-attention-memory
```

## 建立它

看到`code/main.py`我们实施:

> 参见`code/main.py`我们实现了:

1. 一个天真的人.`O(N²)`增量解码器.
   中文翻译:一个朴素的`O(N²)`增量解码器――
2. `O(N)`设置了KV缓存解码器.
   中文翻译:一个`O(N)`缓存解码器――
3. 模拟闪光注意力运行最大算法的软max.
   中文翻译:一个模拟闪光注意力 运行时最大值的分块软max──

### 步骤1:KV缓存

```python
class KVCache:
    def __init__(self, n_layers, n_heads, d_head):
        self.K = [[[] for _ in range(n_heads)] for _ in range(n_layers)]
        self.V = [[[] for _ in range(n_heads)] for _ in range(n_layers)]

    def append(self, layer, head, k, v):
        self.K[layer][head].append(k)
        self.V[layer][head].append(v)

    def read(self, layer, head):
        return self.K[layer][head], self.V[layer][head]
```

简单:继续在每个层,每个头条列表中增长每代币K,V向量.

> 简单:在逐层的列表中持续增加每个代币的 K、V 向量──

### 步骤2: 软max

```python
def tiled_softmax_dot(q, K, V, tile=4):
    """Flash-attention-style softmax(qK^T)V with running max/sum."""
    m = float("-inf")
    s = 0.0
    out = [0.0] * len(V[0])
    for start in range(0, len(K), tile):
        k_block = K[start:start + tile]
        v_block = V[start:start + tile]
        scores = [sum(qi * ki for qi, ki in zip(q, k)) for k in k_block]
        new_m = max(m, *scores)
        exp_old = math.exp(m - new_m) if m != float("-inf") else 0.0
        exp_new = [math.exp(sc - new_m) for sc in scores]
        s = s * exp_old + sum(exp_new)
        for j in range(len(out)):
            out[j] = out[j] * exp_old + sum(e * v[j] for e, v in zip(exp_new, v_block))
        m = new_m
    return [o / s for o in out]
```

比特相同输出`softmax(qK) V`任何时候工作组是一个`tile × d_head`区块,不是全部`N × d_head`现在,我们要去.

> 一次性`softmax(qK) V`逐步相同的输出,但任何时候工作集只是`tile × d_head`块,而不是完整的`N × d_head`,我知道.

### 步骤3:在100代币生成中比较简单与缓存解码

计算注意力操作.`O(N²)`预示:`O(N)`代码打印了两者.

> 计算注意力操作次数──朴素:`O(N²)`存储:`O(N)`现在,我已经开始了.

## 用它实现框架

```python
# HuggingFace transformers auto-enables KV cache on decoder-only generate().
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",
    attn_implementation="flash_attention_2",  # use FA3 if Hopper
    torch_dtype="bfloat16",
)
# generate() uses KV cache automatically
```

机生产:

> 产业部署:

```bash
pip install vllm
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --tensor-parallel-size 4 \
    --max-model-len 32768 \
    --enable-prefix-caching \
    --kv-cache-dtype fp8
```

预先文件缓存在请求中是2026年大胜利. 相同的系统提示,少数拍摄示例或长文本文档在调用中重复使用KV. 对于重复工具提示的代理工作负载,预先文件缓存通常是5x吞吐量增长.

> 跨请求的前缓存是2026年最大的胜利. 相同的系统提示、少样本示例或长上下文文档在调用间重复使用 KV.

## 运送它.

看到`outputs/skill-inference-optimizer.md`技能选择注意力实现,KV缓存策略,量化和推测解码来实现新的推理部署.

> 参见`outputs/skill-inference-optimizer.md`△ 应对新推理部选注意力实现 KV 缓存策略 量化和推测解码方案

## 练习题

1. **Easy.**跑步`code/main.py`确认无和缓存解码器的输出相同;注意选数差异.
   中文翻译:运行 `code/main.py`△确认简单和缓存解码器产生相同输出;注意操作次数差异──
2. **Medium.**实现前置缓存:给出提示P和几个完成,运行一个前进通过P填写KV缓存,然后分支每完成.
   中文翻译:实现前缓存:给定提示 P 和多个补充,对 P 运行一次前向传播填充 KV 缓存,然后每个补充分支――测量与每次重新编码 P 相比的速度提升――
3. **Hard.**实现玩具页面注意:在固定16个代币区块中实现KV缓存.一旦一个序列完成,将其区块返回池中.模拟1000个不同长度的聊天完成.比较内存碎片化与连接分配.
   中文翻译:实现玩具版 页面注意:KV 缓存使用固定16个代币块加空列表――序列完成时归还块――模拟1000个变长聊天补全――比较连续分配的内存碎片化差异――

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| KV cache | "The trick that makes decoding fast" | Stored K and V from every prefix token; new queries attend to them instead of recomputing. |
| KV 缓存 | "让解码变快的技巧" | 存储每个前缀 token 的 K 和 V；新查询对它们做注意力而非重新计算。 |
| HBM | "GPU main memory" | High Bandwidth Memory; 80 GB on H100, 192 GB on B200. ~3 TB/s bandwidth. |
| HBM | "GPU 主内存" | 高带宽内存；H100 上 80 GB，B200 上 192 GB。约 3 TB/s 带宽。 |
| SRAM | "On-chip memory" | Per-SM fast memory, ~256 KB per SM on H100. ~30 TB/s bandwidth. |
| SRAM | "片上内存" | 每 SM 的快速内存，H100 上每 SM 约 256 KB。约 30 TB/s 带宽。 |
| Flash Attention | "Tiled attention kernel" | Computes attention without materializing N×N in HBM. |
| Flash Attention | "分块注意力内核" | 不在 HBM 中生成 N×N 矩阵即完成注意力计算。 |
| Continuous batching | "No-wait batching" | Swap finished sequences out, new ones in, without draining the batch. |
| 连续批处理 | "无等待批处理" | 完成的序列换出，新的换入，无需排空批次。 |
| PagedAttention | "vLLM's headline" | KV cache allocated in fixed blocks with a page table; eliminates fragmentation. |
| PagedAttention | "vLLM 的核心特性" | KV 缓存以固定块分配加页表；消除碎片化。 |
| Prefix caching | "Reuse long prompts" | Cache KV for a shared prefix across requests; major cost cut for agents. |
| 前缀缓存 | "复用长提示" | 跨请求缓存共享前缀的 KV；代理场景大幅降低成本。 |
| Speculative decoding | "Draft + verify" | Cheap draft model proposes tokens; big model verifies k in one pass. |
| 推测解码 | "草案 + 验证" | 廉价草案模型提出 token；大模型一次验证 k 个。 |

## 继续阅读 继续阅读

- [Dao et al. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135)闪电1.
  中文翻译:闪光注意 1 论文。
- [Dao (2023). FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://arxiv.org/abs/2307.08691)闪光2.
  中文翻译:闪光注意 2 论文。
- [Shah et al. (2024). FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](https://arxiv.org/abs/2407.08608)闪电3.
  中文翻译:闪光注意 3 论文。
- [FlashAttention-4 release notes (Dao-AILab, 2026)](https://github.com/Dao-AILab/flash-attention)黑5阶段管道和软件-exp2技巧;阅读REPREVIEREPREVIE,了解本课程所提到的仅向前发射警告.
  中文翻译:闪光注意4 发布说明;黑 5 阶段管道和软件 exp2 技巧。
- [Kwon et al. (2023). Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180)   纸
  中文翻译:vLLM 页面关注 论文。
- [Leviathan et al. (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192)规格解码.
  中文翻译:推测解码论文──
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077)课程中引用的综合草案方法的EAGLE-1/2论文.
  中文翻译:EAGLE-1/2 论文,集成草案方法──
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774)在Eagle旁边引用了Medusa方法.
  中文翻译:Medusa 论文,多解码头方法──
- [vLLM docs — PagedAttention](https://docs.vllm.ai/en/latest/design/kernel/paged_attention.html)在16个代币区块和页面表设计上进行了正规深入潜水.
  中文翻译:vLLM 页面关注 文档,16个代币块和页面设计的深入解析──
