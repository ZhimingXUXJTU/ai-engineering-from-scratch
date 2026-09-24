# 投机解码与3

> 阶段 7 · 第16课证明了数学:利维亚坦拒绝规则确切保存验证器的分布. 这一课是2026年生产投机解码的训练视角. -3将草案模型从廉价近似转化为一个专门构建的小型网络,训练在验证器自己的隐藏状态,然后添加了一个训练时间测试循环, 结果: 3×到 6.5×端到端加快,在聊天中接受的每代币率高于0.9,没有分配权衡. 根据2026年的每一个生产推断堆,

> **【中文解读】**投机解码:使用小模型猜测接下来 3-5个代币,大模型只需要验证――猜对了就在 5个代币计算一个的价格――EAGLE-3 用目标模型的隐藏状态训练草稿网络,接受率90%+,3-6.5倍加速,输出分布不变――

> **【拓展：投机解码→生产推理】**2026年所有主流推理框架都内置投机解码――DeepSeek-V3的MTP头在推理时也被用作投机解码的草稿机,接受率80%+,实现1.8倍吞吐提升――

>  **【前置】**学本节前请先掌握:第7阶段·16期(投机解码 数学证明);第10阶段·12期(推理优化);变换器 隐藏状态概念――本节是生产部署投机解码的工程视角――

>  **【类比】**投机解码 = 老板让实习生先起草邮件。实习生(草案模型) 秒写 5 段草稿,老板(大模型) 只对一次一次──校对一段比从头写一段快得多──校对时如果某段错了,从那段开始重写──EAGLE-3的关键:实习生看过老板之前写的邮件隐藏思考(隐藏状态),起草更像老板风格,接受率90%+──

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 7 · 16 (speculative decoding math), Phase 10 · 12 (inference optimization)
**Time:** ~75 minutes

## 学习目标

- 单句说明利维亚坦定理,证明投机循环产生对验证者相同分布的样本.
  用一句话陈述利维亚坦定理,证明投机循环产生的样本与验证器直接采样分布相同
- 走过尼拉规格解码 (Leviathan 2023) 两年的进展,通过Eagle,Eagle-2,Eagle-3,并列出每一步的确切限制.
  理从朴素投机解码(Leviathan 2023) 到Eagle、Eagle-2,Eagle-3,说出每一步移动的具体限制
- 计算预期的接受率加速`α`项目与验证人成本比例`c`选择最好的草稿长度`N`对于每一个政权.
  从接受率`α`和草稿验证成本比`c`计算预期加速,为每种情况选择最优草稿长度`N`
- 执行从零开始的全部投机循环:从残余中起草,验证,拒绝-样本,在拒绝时将KV缓存重新滚动,在完全接受时发放奖金代币.
  从零实现完整投机循环:草稿、验证、从残差拒绝采样、拒绝回滚 KV 缓存、全部接受时发送奖励令牌

## 问题 问题引入

在70B模型上,自动降解码速度在H100上运行时可能为每秒35个代币.GPU几乎没有度.内存带宽是天花板:每个代币都载荷70B的重量从HBM,执行一个步骤的算术,产生一个浮动.计算单位大部分都停留无动.

> 70B 模型的自归解码在H100上大约每秒35个代币──GPU 远未和──显存带宽是上限:每个代币从HBM加载70B权重,做一步运算,产出一个浮点数──计算单元大部分时间在置──

实际上,你能解决的吞吐量问题.`N`标记`N`验证器在前上运行一次加上所有`N`核实者在位置上的分布`i`否则,我们会拒绝并从残余分布中采样一个修正.`N+1`接受代币而不是一个.

> 投机解码将其转化为实际解决的吞吐量问题――一个廉价的草稿模型使用N 次小前向传播提出N 个代币――验证器对前加上所有N 个草稿运行一次――如果验证器在位置i的分布与草稿一致,我们接受;否则拒绝并从残差分布中采用一个修正――一次大模型前向传播产生最多的N+1 个被接受的代币,而不是一个――

重要论是利维亚坦,卡尔曼,马蒂亚斯 (ICML 2023):输出分布与验证器直接产生的样本相同.不大致.同样.这就是投机解码在生产中被接受的全部原因.

> 关键定理来自Leviathan、Kalman、Matias(ICML 2023):输出分布与直接从验证器采样产生的分布相同──不是近似──是相同──这是投机解码在生产环境中可接受的全部原因它是纯粹的延迟优化,没有质量折衷──

七阶段16课给你了数学.这课给你了训练堆.一个好的草稿比一个便宜的草稿值得加快两倍.EAGLE,EAGLE-2,EAGLE-3 (Li等, 20242025) 将"草稿 =同样的模型的较小版本"变成了精确的工程学科. 2026 生产推理服务器默认为EAGLE-3.

## 概念的核心概念

> **【中文解读】**投机解码(投机解码) 用小模型快速猜测多个代币,再用大模型并行验证被接受的代币 直接保留,被拒绝的从拒绝点重新生成――EAGLE 系列方法在特征层面而不是代币层面投机,接受率更高――

> **【拓展：投机解码的加速效果】**标准投机解码可实现2-3倍 推理加速不损输出质量――EAGLE-2 和 Medusa 等方法通过多头并行预测达到3-4倍 加速――关键技术指标是接受率 (接受率) 小模型与大模型的分布越接近,接受率越高,加速效果越好――


### 变体:利维亚坦拒绝样本

让我们`p(t)`给出一个前,并`q(t)`检查员的. 取样一个标志草案.`d ~ p`接受一个可能性`min(1, q(d) / p(d))`弃后,从残留分布中取出样本`(q - p)_+ / ||(q - p)_+||_1`结果样本分为`q`这不管是多么糟糕`p`越糟糕,你越经常拒绝,但结果仍然是准确的.

子`N`通过一个验证器传输传输`prefix + d_1 + ... + d_N`验证器回复`q_1, q_2, ..., q_{N+1}`随着第一次拒绝,在位置上,`j`采样`residual(q_j, p_j)`在完全接受时,请从中抽取一个奖金代币.`q_{N+1}`现在,我们要去.

### 什么决定了加速

让我们`α`预期的每项预订代币的接受率.`c = cost(draft) / cost(verifier)`预期的每向验证器接受的代币数量为:

```
E[accepted] = (1 - α^(N+1)) / (1 - α)
```

预期的每个接受的代币的 Wall Time `(N * c + 1) / E[accepted]`减少对`N`你会得到一个好处.`α = 0.8, c = 0.05`优质`N`速度是3.2x.`α = 0.95, c = 0.02`优质`N`速度增长速度是5x.

唯一最大的杆是`α`开始的`α = 0.6`通过"酒草稿"`α = 0.9`鱼-3号`N = 5`通过验证器,您将从每个验证器的预期接受代币 2.2 转到 4.1.

### 两年来的进展

**Vanilla speculative (Leviathan, 2023).**简单的编程, 简单的编程, 简单的编程,`α ≈ 0.6`速度最好是2倍.

**EAGLE-1 (Li et al., 2024).**草案是一个小型变压器,通常是一个或两个层,它将验证器的最后层隐藏状态作为输入,直接预测下一个代币.由于草案看到验证器的特征表示,它的分布更接近验证器的.`α`升至0.70.8.

**EAGLE-2 (Li et al., 2024).**增加一个动态的草图树:而不是提出一个单一的序列`N`通过一个向前传递 (树注意) 给每个选手提出一个小树,并通过一个向前传递 (树注意) 给每个选手提供一个小树.`α`通过路径的代币升至0.85以上.

**EAGLE-3 (Li et al., 2025, NeurIPS).**另有两个变化. 首先,完全放弃功能预测损失 EAGLE-1/2 训练了草案来匹配验证器的隐藏状态,这限制了数据有多大帮助. 3直接在预测代币上训练. 第二,训练时间测试 (TTT):在草案训练期间,将草案的以前预测作为多步骤的输入,就像在推断时一样运作. 这将列车和测试分布均整齐,从而阻止错误积累. 测量速度:在聊天中达到6.5x,在H100上SGLang的64批发中增速38%.

### 转换KV缓存

验证扩大验证器的KV缓存到 `N`如果在位置上发生拒绝`j`缓存内容已过位置`j-1`现在错了.两个常见的实现:写到一个零缩缓冲器,并在接受时提交 (vLLM,TensorRT-LLM),或者保持物理KV缓存加上逻辑长度和断断.无论如何,反弹成本是每层每头的字节,这是除了前进通过成本之外的微不足道.

对于EAGLE-2树搜索,验证器使用不因果性面具来运行注意力,该面具尊重树拓.工程很难,但计算是使用自定义面具的标准闪光注意力调用.

### 2026年建筑草案

| Strategy | Draft type | `α` | Speedup | Training cost |
|----------|-----------|-----|---------|---------------|
| Vanilla | Separate small LLM | 0.55-0.70 | 1.8-2.3× | None (reuse existing small model) |
| Medusa | Extra LM heads on verifier | 0.65-0.75 | 2-3× | ~1B SFT tokens |
| EAGLE-1 | 1-layer transformer on hidden states | 0.70-0.80 | 2.5-3× | ~60B tokens |
| EAGLE-2 | EAGLE-1 + dynamic draft tree | 0.80-0.88 | 3-4× | ~60B tokens |
| EAGLE-3 | Multi-layer feature fusion + TTT | 0.88-0.92 | 3.5-6.5× | ~60-200B tokens |
| Lookahead | No draft (Jacobi iteration) | N/A | 1.3-1.6× | None |

在2026年生产:vLLM和SGLang默认为EAGLE-3,如果有,则EAGLE-2.TensorRT-LLM为Meta和NVIDIA公共模型提供了最快的Medusa路径. llama.cpp为CPU部署提供了草草稿.


> **【拓展：EAGLE 的创新点】**在标志空间中,而不是特征空间中投投机使用前几层的特征预测未来的特征,再从特征解码标志中.


## 建立它,实现它.
```figure
l5-spec-decode-eagle
```

## 建立它

看到`code/main.py`这就是全程的利维亚坦投机循环,所有部分:N的草案,验证器的平行通过,每位的拒绝,残余样本采集,奖金代币,KV回滚,以及经验验验证,输出分布与直接样本采集相匹配`q`现在,我们要去.

### 步骤1:拒绝规则

```python
def accept(q_prob, p_prob, u):
    if p_prob <= 0:
        return True
    return u < min(1.0, q_prob / p_prob)
```

### 步骤2:残余分布

```python
def residual(q, p):
    raw = [max(0.0, qi - pi) for qi, pi in zip(q, p)]
    s = sum(raw)
    if s == 0:
        return list(q)
    return [r / s for r in raw]
```

### 步骤3:一个完全的投机步骤

其他`spec_step`函数草案`N`标记`p`然后在一个平行中验证它们.`q`对于每一个草案的代币,它应用拒绝规则,在第一个拒绝时,它从残余中取样了修正.如果一切都接受,它会发出一个奖金代币.`q_{N+1}`现在,我们要去.

### 步骤4:KV回滚账户

模拟器跟踪了一个逻辑的`kv_length`通过"每名工人"的`k`项目草案`kv_length += k`关于拒绝职位`j`现在,预存器已经被写到过去.`j`按,但逻辑长度设置为`prefix_length + j + 1`一个经过了纠正符号. 后续读取到逻辑长度.

### 步骤5: 利维亚坦检查

运行5万个投机步骤. 计算受理代币的经验分布.`q`定理在实践中通过.

### 步骤 6:加快与 α

通过扰乱扫描质量`p`远离`q`测量`α`按验证器调用的预期代币进行图为 `α`其他`N`编码中印出表表,显示了EAGLE-3类草案质量 (`α ≈ 0.9`) 每次验证者调用时解锁45个代币.

## 用它实现框架

生产水平`vllm serve`3:

```bash
vllm serve meta-llama/Llama-3.3-70B-Instruct \
  --speculative-config '{
    "model": "yuhuili/EAGLE3-LLaMA3.3-Instruct-70B",
    "num_speculative_tokens": 5,
    "method": "eagle3"
  }'
```

轮-3在H100上64批次:大约1.38倍比轮-64的轮解码更高的吞吐量,根据EAGLE-3文件.

什么时候找到投机解码:

- 任何互动聊天工作负载,其中p50延迟比峰值吞吐量更重要.
- 编码生成和结构化输出 (JSON,SQL).`α`由于目标分布很可预测.
- 长期代码 (数千个代币) 抵消速度不断支付.

什么时候不:

- 非常小的模型 (<3B). 草稿不比验证器便宜得多.
- 简单的批量-1 CPU 部署.
- 非常高温的创意采样`α`它们会崩.

## 运送它.

这一课产生了`outputs/skill-eagle3-tuner.md`鉴于推断工作量 (模型,批量大小,目标延迟,任务配置文件),它建议推一个投机式解码策略和调整参数 (草案家族,`N`树深度,温度意识的切换).

> 本课产出发 `outputs/skill-eagle3-tuner.md`△给定推理工作负载(模型、批次大小、目标延迟、任务配置),它推投机解码策略和调优参数(草稿族、`N`树深度,温度感知切换)

## 练习题

1. 跑步`code/main.py`确认在5万个样本中,利维亚坦分布检查的千平方统计数据低于95%的关键值.
   中文翻译:运行 `code/main.py`❖确认,在5万样本上,利维亚松分类检查的卡方统计量低于95%的临界值.

2. 扫描`N`从1到10`α`保持在0.9和`c`查看每次验证器调用预期代币和每次代币的实际墙时间.`N`解释曲线的形状.
   中文翻译:将 `N`从1到10`α`保持0.9`c`保持0.04──绘制每次验证调用期望代币 数和每代币 实际挂钟时间──找到最小化挂钟时间的`N`△解释曲线形状──

3. 修改代码以模拟EAGLE-2树搜索:每一步,草案提出一个形状的树`[2, 2, 2]`验证器运行一次,最有可能接受的路径获胜.计算`α`通过同等计算,比较线性链规格解码.
   中文翻译:修改代码模拟EAGLE-2 树搜索:每步草稿提出 `[2, 2, 2]`形状的树 (?? 条候选路径) △验证器运行一次,最高概率的接受路径胜出──计算每叶`α`和每次调试的总代币数量――与等计算量线性链投机解码比较――

4. 执行两个同时序列的KV滚动模拟器.序列A已接受所有草案;序列B在位置2拒绝.`kv_length`任何工作都不会浪费.
   中文翻译:实现两个并发序列的批量KV 回滚模拟器──序列A 所有草稿被接受;序列B 在位置2被拒绝──展示正确的`kv_length`按序列更新且无浪费.

5. 阅读EAGLE-3论文第4节 (训练时间测试).用两句话解释为什么无线特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特特
   中文翻译:阅读EAGLE-3论文第4节(训练时测试) ――用两句话解释为什么没有TT的简单草稿训练受曝光偏差影响,以及为什么训练时草稿自己的预测能修复它――将其与后2秒中的计划采样文献联系起来――

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Leviathan rule | "min(1, q over p)" | Bernoulli accept/reject with probability `min(1, q(d)/p(d))`, preserves the verifier distribution exactly when you sample from the residual on rejection | Leviathan 规则，精确保持验证器分布的接受/拒绝规则 |
| Residual distribution | "(q minus p) plus, normalized" | `(q - p)_+` clamped at zero and renormalized — the correct distribution to sample from on rejection | 残差分布，拒绝时从中采样的正确分布 |
| Acceptance rate α | "how often the draft is right" | Expected per-token Bernoulli-success probability under the rejection rule; governs all speedup math | 接受率，草稿每 token 的期望成功概率 |
| EAGLE-1 | "hidden-state draft" | Tiny transformer draft conditioned on the verifier's last-layer hidden state (Li et al., 2024) | EAGLE-1，基于验证器隐藏状态的小型草稿 |
| EAGLE-2 | "dynamic draft tree" | EAGLE-1 plus a tree of candidate continuations scored with tree attention in one verifier pass | EAGLE-2，动态草稿树+树注意力 |
| EAGLE-3 | "training-time test" | Drops the feature-prediction loss, trains on direct token prediction with the draft fed its own outputs during training | EAGLE-3，训练时让草稿自回归生成以匹配推理分布 |
| Training-time test (TTT) | "exposure bias fix" | Run the draft autoregressively during training so train and test input distributions match — the direct analog of scheduled sampling | 训练时测试，解决曝光偏差 |
| KV rollback | "undo rejected drafts" | Bookkeeping that resets the verifier's KV cache to the accepted-prefix length after a rejection | KV 回滚，拒绝后重置 KV 缓存到已接受前缀长度 |
| Bonus token | "the free one" | When all `N` drafts accept, sample one extra from `q_{N+1}` at no additional verifier cost | 奖励 token，全部接受时免费多生成一个 |
| Tree attention | "verify many candidates at once" | Attention with a non-causal mask that respects the topology of a draft tree; computes `q_i` for every node in the tree in one forward pass | 树注意力，一次前向传播验证多个候选 |

## 继续阅读 继续阅读

- [Leviathan, Kalman, Matias — Fast Inference from Transformers via Speculative Decoding (arXiv:2211.17192, ICML 2023)](https://arxiv.org/abs/2211.17192)基础论文和等效定理
- [Chen et al. — Accelerating Large Language Model Decoding with Speculative Sampling (arXiv:2302.01318)](https://arxiv.org/abs/2302.01318)同时独立引入,且有清晰的证明
- [Li et al. — EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty (arXiv:2401.15077)](https://arxiv.org/abs/2401.15077)Eagle-1,隐藏状态的草案
- [Li et al. — EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees (arXiv:2406.16858)](https://arxiv.org/abs/2406.16858)动态树木搜索
- [Li et al. — EAGLE-3: Scaling up Inference Acceleration via Training-Time Test (arXiv:2503.01840, NeurIPS 2025)](https://arxiv.org/abs/2503.01840)2026年生产违约
- [Cai et al. — Medusa: Multiple Decoding Heads (arXiv:2401.10774)](https://arxiv.org/abs/2401.10774) 另一个无草案的方法
- [vLLM Speculative Decoding documentation](https://docs.vllm.ai/en/latest/features/spec_decode.html)可信生产参考,所有战略都连接在一起
