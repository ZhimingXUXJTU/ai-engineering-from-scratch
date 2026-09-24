# 混合专家模型 (MoE)

> 密集的70B变压器会激活每个代币的每个参数. 671B MoE 激活每代币只有37B,并且在每个基准上都超过它.

> **【中文解读】**通过使用MoE架构进行深度搜索,混合的使用.

**Type:** Hands-on | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

密集变压器的FLOP在推断时等于其参数数数量 (前进传输的2倍). 扩展密集模型,每个代币都支付了全部账单.到2024年,边界正在撞击计算墙:要更聪明,你需要每代币的FLOP数量呈指数.

> 密变压器 推理时的FLOPs等于其参数量(前向传播乘以2);;扩大密模型意味着每个代币都必须支付全部代价;;到2024年,前沿模型遇到了计算墙:要变得更聪明,需要指数级增长的每个代币FLOPs;;

专家组合打破了这个联系.`E`独立专家 + 选择路由器`k`标记的专家.`E × FFN_size`每代币的活跃参数 = `k × FFN_size`典型的2026配置:`E=256`现在`k=8`存储量量`E`计算规模`k`现在,我们要去.

> 混合专家模型打破了这个联系.`E`个独立专家 + 一个路由器,每个代币 选择 `k`个专家――总参数 = `E × FFN_size`△每个代币的活跃参数数 = `k × FFN_size`△典型的2026年配置:`E=256`,我知道.`k=8`│ 存储随`E`扩展,计算随`k`扩展.

2026年边界几乎完全是MoE:DeepSeek-V3 (671B总量 / 37B活跃),Mixtral 8×22B,Qwen2.5-MoE,Llama 4,Kimi K2,gpt-oss.在人工分析的独立领先榜单上,前10个开源模型都是MoE.

> 2026年前沿几乎完全是MoE:DeepSeek-V3(671B 总参数 / 37B 活跃) 、混合8×22B、Qwen2.5-MoE、Llama 4、Kimi K2、gpt-oss──在人工分析的独立排行榜上,排名第10的开源模型都是MoE──

> **【中文解读】**摩伊打破了"参数 = 计算量"等式. 每个FFN层被替换为E个独立专家 +路由器,每一个代币只激活 k个专家.总参数随着E的增长而成长,但每个代币的计算量只随着E的增长而成长.典型配置E=256,k=8,存储随着E的缩小,计算随着k的缩小.这是2020年代最重要的扩展思路.

> **【拓展：DeepSeek-V3 的 MoE 创新】**果V3 拥有671B 总参数,但每代币只通过256个路由专家+1个共享专家实现了37B. 它还引入了无损辅助负载平衡策略,避免了传统的MOE路由崩问题. 在人工分析排行榜中,DeepSeek-V3以不到GPT-4的推理成本的十分之一实现了可比性性能.

## 概念的核心概念

![MoE layer: router selects k of E experts per token](../assets/moe.svg)

### 转换的FFN

密集变压器块:

> 密变压器块:

```
h = x + attn(norm(x))
h = h + FFN(norm(h))
```

门:

```
h = x + attn(norm(x))
scores = router(norm(h))              # (N_tokens, E)
top_k = argmax_k(scores)              # pick k of E per token
h = h + sum_{e in top_k}(
        gate(scores[e]) * Expert_e(norm(h))
    )
```

每个专家都是一个独立的FFN (通常是SwiGLU).路由器是一个单一的线性层.每个代币都选择了自己的代币.`k`专家们可以通过他们的输出来进行封闭的混合.

> 每个专家是一个独立的FFN (通常是SwiGLU) 路由器是一个单线性层.`k`专家,获得它们的输出门控混合.

### 负载平衡问题

如果路由器通过专家3将90%的代币,其他专家就会饿死.

> 如果路由器将90%的代币分配给专家3,其他专家就会"饿了"――已经尝试了三种修复方案:

1. **Auxiliary load-balancing loss**根据专家使用的差异,加一个惩罚. 工作,但增加了一个超参数和第二个梯度信号.
   翻译: 中文**辅助负载均衡损失**增加与专家使用差比例的惩罚──有效,但增加了超参数和第二梯度信号──
2. **Expert capacity + token dropping**每个专家最多处理`C × N/E`标记,过度标记跳过层. 损害质量.
   翻译: 中文**专家容量 + token 丢弃**专家最多处理 `C × N/E`个标志;溢出的标志 跳过这个层面――损害质量――
3. **Auxiliary-loss-free balancing**通过"深度搜索" (DeepSeek-V3) 增加一个学习的专家偏见,改变路由器的顶级k选择.偏见在训练损失之外更新.没有罚款在主要目标.2024年大解锁.
   翻译: 中文**辅助损失无关均衡**调整路由器的顶部选择――偏置在训练损失之外更新――不对主目标施加惩罚――2024年重大突破――

对于每位专家,在每一步培训后,检查其使用是否超越目标或低于目标.`±γ`选择用途`scores + bias`专家使用的概率是原料`scores`没有变化. 脱离路由与表达.

> 查V3的方法:每次训练步骤后,每个专家都检查使用量是否高于或低于目标.`±γ`△选择使用`scores + bias`△用于门控专家概率是未改的原始`scores`将路由与表达解.

### 共同的专家

根据 DeepSeek-V2/V3 的规定,专家分为 *共享*和 *路由*.每个代币都通过所有共享专家.路由专家通过顶级k 选出.共享专家捕获了共同知识;路由专家专业化. V3运行 1 个共享专家加上 256 个路由专家中最前8个.

> 通过所有共享专家――通过顶级专家选择――共享专家获取通用知识;通过专家负责专业化――V3 运行 1 个共享专家加上 256 个路由专家中选择 8 个顶级专家――

### 精细粮食专家

经典MoE (GShard,Switch):每个专家的宽度就像一个完整的FFN. `E`只有小的 (864),`k`是小的 (12).

> 经典的Moe:GShard、Switch:每个专家与完整的FFN 一样宽.`E`较小(8-64),`k`较小(1-2) 』

现代细粒度的MoE (DeepSeek-V3,Qwen-MoE):每个专家的尺寸较窄 (1/8FFN). `E`是大 (256+),`k`总参数相同,但组合规模更快. `C(256, 8) = 400 trillion`质量上升,延迟保持平稳.

> 现代细粒度 MoE(DeepSeek-V3、Qwen-MoE):每个专家更窄(1/8FFN 大小) ⋅`E`较大(256+),`k`也更大(8+) △总参数相同,但组合增长更快──`C(256, 8) = 400 万亿`种可能的"专家"组合――质量提升,延迟不变――

> **【拓展：MoE 的路由崩塌问题】**导航训练中的核心挑战是路由崩 (路由崩) 路由器可能将大部分的代币分配给少数专家,导致其他专家无法接受训练.

### 成本概况

按标记,按层:

> 每个代币,每一个层次:

| Config | Active params / token | Total params |
|--------|-----------------------|--------------|
| 配置 | 每个 token 活跃参数 | 总参数量 |
| Mixtral 8×22B | ~39B | 141B |
| Llama 3 70B (dense) | 70B | 70B |
| DeepSeek-V3 | 37B | 671B |
| Kimi K2 (MoE) | ~32B | 1T |

在执行过程中,DeepSeek-V3几乎在每个基准上击败了Llama 3 70B (密集).**fewer active FLOPs per token**更多参数 = 更多知识. 更多的活跃FLOPs = 更多的计算每代币.

> 密的Llama3在几乎所有基准测试中击败了Llama370B.**每个 token 的活跃 FLOPs 更少**更多参数 = 更多知识. 更多活跃FLOP.

### 捕获:记忆

所有专家都使用GPU,不管哪个是射击的.671B模型需要1.3TB的VRAM用于fp16权重.边界MoE部署需要专家平行性.

> 所有专家无论是否活跃都驻留在GPU上. 一个671B模型需要约1.3TB的fp16权重显存. 前沿MoE部署需要专家并行.

> **【中文解读】**核心权衡:使用内存换计算――DeepSeek-V3 以37B 活跃参数达到超过70B 密模型的性能,但需要1.3TB 显存储所有专家――这推动了专家并行 (专家并行) 技术的发展专家将分散到多个GPU上,通过网络路由代币――

> **【拓展：细粒度专家 vs 粗粒度专家】**传统的MOE(Switch Transformer) 使用少量大型专家(E=8-64)。现代细粒度MOE(DeepSeek-V3) 使用大量小型专家(E=256+),每个专家只有1/8的FFN宽度──组合数 C(256,8) 约为400亿种,远超粗粒度的组合空间──质量提升显著,延迟基本不变──

## 建立它,实现它.
```figure
expert-routing
```

## 建立它

看到`code/main.py`纯的紧的MoE层,含有:

> 参见`code/main.py` 简单标准的实现紧密的MoE层,包括:

- `n_experts=8`光 (SwiGLU) 的专家 (每一个线性,说明)
  翻译: 中文`n_experts=8`个类SwiGLU 专家(每个一条线性层,用于演示)
- 顶级k=2路由
  中文翻译:上-k=2 路由
- 软max正常化的门重量
  中文翻译:软最大重量
- 通过专家偏见进行无损辅助平衡
  中文翻译:通过逐专家偏置实现辅助损失无关平衡

### 步骤1:路由器

```python
def route(hidden, W_router, top_k, bias):
    scores = [sum(h * w for h, w in zip(hidden, W_router[e])) for e in range(len(W_router))]
    biased = [s + b for s, b in zip(scores, bias)]
    top_idx = sorted(range(len(biased)), key=lambda i: -biased[i])[:top_k]
    # softmax over ORIGINAL scores of the chosen experts
    chosen = [scores[i] for i in top_idx]
    m = max(chosen)
    exps = [math.exp(c - m) for c in chosen]
    s = sum(exps)
    gates = [e / s for e in exps]
    return top_idx, gates
```

偏差影响选择,而不是门权重.这是DeepSeek-V3技巧.

> 偏置影响选择,不影响门控制权重――这就是DeepSeek-V3的技巧偏置纠正负载不平衡,但不干预模型的预测――

### 步骤2:通过路由器运行100个代币

随着专家的射击频率的追踪.`-γ`对于过度使用的专家,`+γ`对于未使用的使用量),使用量在几次代中趋于均分布.

> 随着这些专家被激活了多少次.`-γ`缺乏使用的专家`+γ`),使用量在几次代后收到平均分布.

### 步骤3:参数数量比较

打印MoE配置的"密度相当" .深度搜索V3形: 256路由 + 1共享, 8 活跃,d_model=7168. 总参数数是眼睛. 活跃数量是密度Llama 3 70B的第七个.

> 打印MoE配置的"密等价"──DeepSeek-V3 形状:256 个路由 + 1 个共享,8 个活跃,d_model=7168──总参数数令人惊叹──活跃参数数只有密 Llama 3 70B 的七分之一──

## 用它实现框架

拥抱面部加载:

> 拥抱脸 加载:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-8x22B-v0.1")
```

2026 产量推断:vLLM 支持MoE路由本地.SGLang 具有最快的专家平行路径.两者都自动处理顶级选项和专家平行.

> 2026年生产推理:vLLM 原生支持MoE 路由──SGLang 拥有最快的专家并行路径──都自动处理顶级的专家并行──

**When to pick MoE:**
- 你想要以低的推断成本的标准质量.
  中文翻译:你想以更低的每代币 推理成本获得前沿质量.
- 你有VRAM/专家并行基础设施.
  中文翻译:你有足够的显存/专家并行基础设施.
- 你的工作量是代币重 (聊天,代码) 而不是文本重 (长文档).
  中文翻译:你的工作负载是标志密集型 (图片) 而不是上下文密集型 (图片) 长文档 (图片) .

**When NOT to pick MoE:**
-  边缘部署 您为任何活跃的FLOP付出了全部存储费.
  中文翻译:边缘部署你要为任何活跃的FLOP支付全部储备.
- 专家路由增加了总费用.
  中文翻译:延迟敏感的单用户服务专家路由增加开销――
- 小型型号 (<7B) MoE的质量优势仅在计算门 (~6B活性参数) 以上.
  中文翻译:小模型(<7B) MoE的质量优势只在计算值以上(约6B 活跃参数) 才会出现──

## 运送它.

看到`outputs/skill-moe-configurator.md`技能选择E,k和共享专家布局,以实现新的MoE参数预算,培训代币和部署目标.

> 参见`outputs/skill-moe-configurator.md`△ 根据参数预算,训练标志数和部署目标,为新能源部 选择E、k 和共享专家布局.

## 练习题

1. **Easy.**跑步`code/main.py`观察如何辅助免损失偏见更新平衡专家使用超过50次.
   中文翻译:运行 `code/main.py`〔观察辅助损失无关偏置更新如何在50次代中平衡专家使用〕
2. **Medium.**换取学习路由器以基于哈希的路由器 (确定性,没有学习). 进行质量和平衡比较.
   中文翻译:使用哈希的路由器取代学习式路由器 (定性,无需学习) ――比较质量和平衡性――为什么学习式路由器更好?
3. **Hard.**实现GRPO类型的"推广匹配路由" (DeepSeek-V3.2技巧):记录专家在推断过程中发射的,在梯度计算过程中强迫相同的路由.测量玩具政策梯度设置的影响.
   中文翻译:实现GRPO风格的"推演匹配路由" (DeepSeek-V3.2技巧):记录推理时哪些专家被激活,在梯度计算时强制相同路由.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Expert | "One FFN among many" | An independent feed-forward network; parameters dedicated to a sparse slice of the FFN computation. |
| 专家 | "众多 FFN 之一" | 独立的前馈网络；专用于 FFN 计算的稀疏切片的参数。 |
| Router | "The gate" | A tiny linear layer that scores each token against each expert; top-k selection. |
| 路由器 | "门控" | 一个小线性层，对每个 token 与每个专家打分；top-k 选择。 |
| Top-k routing | "k active experts per token" | Each token's FFN computation goes through exactly k experts, weighted by gate. |
| Top-k 路由 | "每个 token 激活 k 个专家" | 每个 token 的 FFN 计算经过恰好 k 个专家，按门控加权。 |
| Auxiliary loss | "Load-balance penalty" | Extra loss term that penalizes skewed expert usage. |
| 辅助损失 | "负载均衡惩罚" | 惩罚专家使用不均衡的额外损失项。 |
| Auxiliary-loss-free | "DeepSeek-V3's trick" | Balance via per-expert bias on the router's selection only; no extra gradient. |
| 辅助损失无关 | "DeepSeek-V3 的技巧" | 仅通过路由器选择上的逐专家偏置实现均衡；无额外梯度。 |
| Shared expert | "Always on" | Extra expert through which every token passes; captures common knowledge. |
| 共享专家 | "始终开启" | 每个 token 都通过的额外专家；捕获通用知识。 |
| Expert parallelism | "Shard by expert" | Distribute different experts to different GPUs; route tokens across the network. |
| 专家并行 | "按专家分片" | 将不同专家分配到不同 GPU；通过网络路由 token。 |
| Sparsity | "Active params < total params" | The ratio `k × expert_size / (E × expert_size)`; 37/671 ≈ 5.5% for DeepSeek-V3. |
| 稀疏性 | "活跃参数 < 总参数" | 比率 `k × expert_size / (E × expert_size)`；DeepSeek-V3 为 37/671 ≈ 5.5%。 |

## 继续阅读 继续阅读

- [Shazeer et al. (2017). Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://arxiv.org/abs/1701.06538)这个想法.
  中文翻译:MoE的原始论文──
- [Fedus, Zoph, Shazeer (2022). Switch Transformer: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://arxiv.org/abs/2101.03961)开关,经典的MoE.
  中文翻译:转换器,经典的MOE论文。
- [Jiang et al. (2024). Mixtral of Experts](https://arxiv.org/abs/2401.04088)混合物8×7B.
  中文翻译:混合8×7B论文。
- [DeepSeek-AI (2024). DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437) MLA + 无损辅助MoE + MTP.
  中文翻译:DeepSeek-V3 技术报告,MLA + 辅助损失无关 MoE + MTP。
- [Wang et al. (2024). Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts](https://arxiv.org/abs/2408.15664)基于偏差的平衡纸.
  中文翻译:基于偏置的均衡策略论文.
- [Dai et al. (2024). DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models](https://arxiv.org/abs/2401.06066)精细的+共享专家 分开本课的路由器使用.
  中文翻译:深度搜索论文,细粒度 + 共享专家拆分――
- [Kim et al. (2022). DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training](https://arxiv.org/abs/2201.05596)原始共享专家论文.
  中文翻译:DeepSpeed-MoE 原始共享专家论文──
