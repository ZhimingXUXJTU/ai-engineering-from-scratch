# 预测解码 草案验证重复

> 推迟解码是序列的.每个代币等待上一个. 投机解码打破链条:一个廉价的模型在一个前进通行中验证所有N代币,而昂贵的模型在一个前进通行中验证所有N代币. 当草案正确时,你为N代代付出了一个大额的前进.

> **【中文解读】**用小模型快速生成候选标记,大模型批量验证――可以加速推理2-3倍而不降低质量――

**Type:** Hands-on | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 7 · 07 (GPT Causal LM), Phase 7 · 12 (KV Cache & Flash Attention) | **前置知识:** Phase 7 · 07 (GPT Causal LM), Phase 7 · 12 (KV Cache & Flash Attention)
**Time:** ~60 minutes | **时间:** ~60 分钟

## 问题 问题引入

如果我们让3B草案5个代币前进,然后运行70B *一次*验证所有5,总数是`5×3 + 30 = 45 ms`对于最多5个被接受的代币`5×30 = 150 ms`这就是完全的投机解码比率:换取少量的额外的GPU内存 (草案模型) 为24x较低的解码延迟.

> 一个70B LLM 采集一个代币 在H100上需要约30ms──一个3B草案模型需要约3ms──如果我们让3B提前生成5个代币,然后运行70B*一次*验证所有5个,总时间为`5×3 + 30 = 45 ms`最多获得5个被接受的代币,`5×30 = 150 ms`◎这是推测解码的全部卖点:使用少额外的GPU内存 (图案模型) 换取 2-4 倍较低的解码延迟──

投机性样本采集,由Leviathan等 (2023) 和陈等同时引入,确保输出序列是**identically distributed**没有质量妥协,只是更快.

> 这种技巧必须保持分布不变. 推测采样由Leviathan等等 (在2023年) 和 Chen等同时引入,保证输出序列与大模型自动生成的分布.**完全相同**没有质量损失.

根据2026年推断,四个设计验证器对的家庭占据主导地位:

> 根据2026年推,四类草案验证器将占主导地位:

1. **Vanilla speculative (Leviathan 2023).**单独的草案模型 (例如,Llama 3 1B) +验证器 (例如,Llama 3 70B).
   翻译: 中文**朴素推测（Leviathan 2023）。**独立的草案模型(如Llama 3 1B) + 验证器(如Llama 3 70B) 👇
2. **Medusa (Cai 2024).**验证器上的多个解码头预测位置`t+1..t+k`没有单独的模型草案.
   翻译: 中文**Medusa（Cai 2024）。**验证器上的多个解码头并行预测位置`t+1..t+k`无需独立草案模型
3. **EAGLE family (Li 2024, 2025).**轻量级的草稿,重复验证器隐藏状态;比尼拉更接近接受率;典型的34×.
   翻译: 中文**EAGLE 系列（Li 2024, 2025）。**复用验证器隐藏状态的轻量草案;接受率比简单方案更高;典型加速3-4倍──
4. **Lookahead decoding (Fu 2024).**简单的,但没有依赖.
   翻译: 中文**前瞻解码（Fu 2024）。**杰科比 代;完全不需要草案模型──自推测──小众但无依赖──

在2026年,每一个生产推断堆都会默认地发送投机解码. vLLM,TensorRT-LLM,SGLang和 llama.cpp都支持至少尼 + EAGLE-2.

> 2026年每一个生产推理都默认搭载推测解码──vLLM、TensorRT-LLM、SGLang 和 llama.cpp 都至少支持朴素+EAGLE-2──

> **【中文解读】**推测解码的核心洞察:自归生成是串行瓶──用小模型(3B)快速生成N个候选代币,大模型(70B)一次前向传播验证所有N个──总时间从N×30ms 降至5×3+30=45ms,加速 2-4倍──关键:推测采样保证输出分布与大模型完全一致,无质量损失──

> **【拓展：EAGLE 与 Medusa 的自推测策略】**果 (Eagle) 通过2024年重复大模型的隐藏状态来生成草案,接受率比独立小模型更高,典型加速3~4倍.

## 概念的核心概念

### 核心算法

鉴于验证器`M_q`并且更便宜的草稿`M_p`其他:

> 给定验器`M_q`和更便宜的草案模型`M_p`其他:

1. 让我们`x_1..x_k`已解码的前.
   中文翻译:设 `x_1..x_k`为已解码的前──
2. **Draft**:使用 `M_p`推出自动推移`d_{k+1}, d_{k+2}, ..., d_{k+N}`具有草案概率`p_1..p_N`现在,我们要去.
   翻译: 中文**草案**使用`M_p`自归地提出`d_{k+1}, d_{k+2}, ..., d_{k+N}`附带草案概率`p_1..p_N`,我知道.
3. **Verify in parallel**运行`M_q`一次就这样了`x_1..x_k, d_{k+1}, ..., d_{k+N}`获得验证器概率`q_1..q_{N+1}`对于职位`k+1..k+N+1`现在,我们要去.
   翻译: 中文**并行验证**对`x_1..x_k, d_{k+1}, ..., d_{k+N}`运行一次`M_q`获得位置`k+1..k+N+1`证证器概率`q_1..q_{N+1}`,我知道.
4. **Accept/reject each draft token left to right**对于每一个`i`接受一个可能的`min(1, q_i(d_i) / p_i(d_i))`现在,我们要去.
   翻译: 中文**从左到右接受/拒绝每个草案 token**对于每个人都`i`概率`min(1, q_i(d_i) / p_i(d_i))`接受
5. 在第一次拒绝位置`j`: 样本`t_j`由于"残留"分布而导致的`(q_j - p_j)_+`之后的所有草案都正常化了.`j`它们被丢弃.
   中文翻译:在位置`j`首次被拒绝时:从"残差"分布`(q_j - p_j)_+`归化后采样`t_j`,我知道.`j`之后所有草案都被抛弃.
6. 接受一切`N`: 样本一个额外的代币`t_{N+1}`其他`q_{N+1}`(免费奖金代币)
   中文翻译:当所有 `N`个都被接受时:从 `q_{N+1}`作为额外的标志`t_{N+1}`为了获得奖励,

剩余分布技巧是保持输出分布的数学洞察力`M_q`没有任何东西.

> 差距分布技巧是保持输出分布与`M_q`从头样式完全相同的数学洞见.

### 什么决定了加速

让我们`α`预期的每项项目代币的接受率.`c`项目/验证人成本比例.

> 设 `α`= 每个草案标志的预期接受率设`c`项目与验证器的成本比比:

- 无辜的世代每代币都会做一个大型号.
  中文翻译:朴素生成每个代币调用一次大模型――
- 投机者每次打一个大型号电话`(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)`什么时候的代币`α`了.
  中文翻译:推测解码在 `α`较高时,每`(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)`个标志调用一次大模型.

典型的指南`α = 0.75`其他`N = 5`现在,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看.

> `α = 0.75`和 `N = 5`时的典型经验法则:大模型调用减少3倍.

> **【中文解读】**加速效果取决于接受率 alfa──当 alfa=0.75、草案长度 N=5 时,大约3倍减少大模型调用──残差分布残差分布) 是保持分布一致的数学关键拒绝时从 (q-p) + 归结分布中采样,确保最终输出与大模型直接采样的分布完全一致──

**α depends on:**

> **α 取决于：**

- 如何接近验证器的草案.同一个家庭/同一个培训数据显著增强α.
  中文翻译:草案对验证器的近似程度.
- 解码策略:贪的草案与贪的验证器:高 α.温度采样:难以匹配;接受度下降.
  中文翻译:解码策略──贪心草案对贪心验证器:高 α──温度采样:更难匹配;接受率下降──
- 任务类型:代码和结构化输出接受更多 (可预测);自由形式的创意写作接受少.
  中文翻译:任务类型──代码和结构化输出接受更多(可预测);自由形式创意写作接受更少──

### 梅杜萨  草案没有草案模型

梅杜萨将草案模型取代,在验证器上加上输出头.`t`其他:

> 梅杜萨使用验证器上的额外输出头换稿模型.`t`其他:

```
shared trunk → hidden h_t
    ├── head_0: predict token at t+1  (standard LM head)
    ├── head_1: predict token at t+2
    ├── head_2: predict token at t+3
    ├── head_3: predict token at t+4
```

每个头都输出了自己的 logits. 在推断时,你从每个头进行样本来获得候选人序列,然后通过使用树注意方案验证一个前进通过,同时考虑所有候选人延续.

> 每个头发出自己的逻辑. 推时从每个头样得到候选序列,然后使用树注意方案一次前向传播验证,同时考虑所有候选写作.

优势:没有第二个模型. 缺点:添加可训练的参数;需要监督的细节调整阶段 (~1B代币);接受率略低于良好的草稿的尼拉投机.

> 优点:无需第二个模型──缺点:增加可训练参数;需要监督微调阶段(约1B代币);接受率比好的草案模型的简单推测略低──

> **【拓展：推测解码在 vLLM 中的实现】**2026年最流行的LLM推理框架,原生支持推测解码――它使用连续批量处理 (连续批量处理) + PagedAttention + 推测解码的组合优化――在生产部署中,推测解码通常带来2-3倍的延迟降低,对于聊天场景 (用户感知延迟敏感) 尤为关键――结合量化 (AWQ/GPTQ),可以在单张GPU上实现高性能推进――

### 通过重复使用隐藏状态来更好地绘制

由于该草案看到验证器的特征表示,它的预测与验证器的输出分布密切相关.接受率从0.6 (瓦尼拉) 升至0.85+.

> 由于草案看到验证器的特征表示,其预测与验证器的输出分布高度相关.接受率从0.6程度 (简单) 升至0.85以上.

3 (2025) 增加了对候选延续的树搜索. vLLM和SGLang 作为Llama 3/4和Qwen 3的默认规范路径,将Eagle-2/3作为3/3的预定规范路径.

> 作为Llama 3/4 和 Qwen 3 的默认推测路径,Eagle-2 (Eagle-3) 增加了候选续写的树搜索.

### 的舞蹈

验证数据`N`通过一个前进传输,将验证器的KV缓存扩大到 `N`如果一些草案被拒绝,则必须将缓存重新滚动到接受的预写长度.

> 验证在一次前向传播中将`N`个草案标志 输入验证器.`N`个条目. 如果一些草案被拒绝,你必须将缓存回滚到已接受的前长度.

生产实施 (vLLM 项目)`--speculative-model`首先写一下,承诺接受.这不是概念上很难,但它很难.

> 生产实现`--speculative-model`、TensorRT-LLM的LookaheadDecoder) 使用临时KV缓冲区处理这个问题──先写入,接受时提交──概念上不难,但实现上比较繁──

## 建立它,实现它.
```figure
draft-verify-tokens
```

## 建立它

看到`code/main.py`我们实施了核心投机性样本采集算法 (拒绝步骤+残余分布)

> 参见`code/main.py`△我们使用以下组件实现核心推测采样算法 ((拒绝步骤 + 残差分布):

- 一个"大模型",是指指数定性软最大值,而不是指数编码的分布 (所以我们可以分析验证接受数学的结果).
  中文翻译:一个"大模型",是手动编码分布式确定性软max (以便分析性验证接受数学) 〔
- 它们是对大模型的颠覆.
  中文翻译:一个"草案模型",是大模型的扰动版本.
- 接受/拒绝循环,产生与直接采样相同的边际分布.
  中文翻译:一个接受/拒绝循环,产生与直接采样相同的边际分布.

### 步骤1:拒绝步骤

```python
def accept_or_reject(q_prob, p_prob, draft_token, u):
    ratio = q_prob / p_prob if p_prob > 0 else float("inf")
    return u < min(1.0, ratio)
```

`u`是一个统一的随机数字.`q_prob`是验证者对拟定的代币的概率. `p_prob`利维雅坦定理是,这个伯诺利决定,然后是从废弃的残留样本中抽取样本,

> `u`是平均随机数量.`q_prob`是验证器对草案代币的概率.`p_prob`利维亚坦定理表明,除了拒绝残差采样,可以确定持有证件的分布.

### 步骤2:残余分布

```python
def residual_dist(q, p):
    raw = [max(0.0, qi - pi) for qi, pi in zip(q, p)]
    s = sum(raw)
    return [r / s for r in raw]
```

减去`p`其他`q`根据元素,将负值压缩到零,重新正常化.

> 个元素从`q`减去`p`总体而言,将负值切断为零,重新归纳为零.

### 步骤3:一个投机步骤

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

五个接受的 → 一个奖金 → 一个验证器通行中产生的六个代币.

> 五个被接受 → 一个奖励 → 一次验证器通行产生六个代币――

### 步骤4:测量接受率

运行1万个投机步骤,在不同的草案质量水平.图片接受率与草案和验证器分布之间的KL差异.你应该看到一个清洁的单调关系.

> 在不同草案质量水平上运行10,000次推测步骤――绘制接受率与草案与验证器分布之间的 KL 散度――你应该看到一个清晰的单调关系――

### 步骤5:验证分布等效

经验:投机循环产生的代币的历史图应与直接从验证器中采样生成的历史图相匹配.这是实践中的利维亚坦定理.一个奇方体测试在采样错误中确认.

> 经验上:推测循环产生的符号直方图应与直接从验证器采集的直方图匹配.

## 用它实现框架

产量:

> 生产部署:

```bash
# vLLM with EAGLE
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model /models/llama-3.1-eagle-70b \
    --speculative-draft-tensor-parallel-size 1 \
    --num-speculative-tokens 5

# vLLM with vanilla draft model
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model meta-llama/Llama-3.2-1B-Instruct \
    --num-speculative-tokens 5
```

据悉,在2026年中旬,TensorRT-LLM将拥有最快的梅杜萨路径.`faster-whisper`语大的猜测解码用一个小的草稿.

> 在2026年中期拥有最快的梅杜萨路径.`faster-whisper`为语大封装了推测解码,使用小草案模型.

**Picking a draft:**

> **选择草案策略：**

| Strategy | When to pick | Speedup |
|----------|--------------|---------|
| 策略 | 何时选择 | 加速比 |
| Vanilla draft (1B/3B Llama family) | Fast prototype, no training | 1.8–2.3× |
| 朴素草案（1B/3B Llama 系列） | 快速原型，无需训练 | 1.8–2.3× |
| Medusa heads | You can fine-tune the verifier | 2–3× |
| Medusa 头 | 可以微调验证器 | 2–3× |
| EAGLE-2 / 3 | Production, max speed | 3–4× |
| EAGLE-2 / 3 | 生产环境，最大速度 | 3–4× |
| Lookahead | No draft, no training, no extra params | 1.3–1.6× |
| 前瞻 | 无草案，无训练，无额外参数 | 1.3–1.6× |

**When NOT to spec-decode:**

> **何时不使用推测解码：**

- 单次序列生成15个代币.
  中文翻译:1-5代币的单序列生成──开销占主导──
- 极具创意/高温采样 (α滴).
  中文翻译:高度创意/高温采样(α下降) 〔
- 存储量限制的部署 (草案模型添加VRAM).
  中文翻译:内存受限的部署 (内存受限的部署)

## 运送它.

看到`outputs/skill-spec-decode-picker.md`技能选择一个投机式解码策略 (尼拉/梅杜萨/鱼/头) 和调节参数 (N,草稿温度) 进行新的推断工作负载.

> 参见`outputs/skill-spec-decode-picker.md`◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎

## 练习题

1. **Easy.**跑步`code/main.py`确认投机代币分布与验证人在50万代币中直接样本分布相匹配,在平平面 p >0.05内.
   中文翻译:运行 `code/main.py`△确认在5万个标志上,推测标志分布与验证器的直接采样分布在卡方检查 p > 0.05 内匹配──
2. **Medium.**作为一个函数的图片加速 (每大模型前进的代币)`N`为了`α = 0.5, 0.7, 0.85`确定最佳的方法`N`对于每一个 α. (提示:每次验证调用预期的代币 = `(1 - α^{N+1}) / (1 - α)`)
   中文翻译:绘制`α = 0.5, 0.7, 0.85`时加速比(每次大模型前向的符号数) 与 `N`关系――确定每个 α 的最佳`N`〔(提示:每次验证调用预期代币 数 = `(1 - α^{N+1}) / (1 - α)`〔一〕
3. **Hard.**执行一个小的梅杜萨:从14课中取下顶石GPT,添加3个额外的LM头,预测位置t+2,t+3,t+4. 训练小克斯佩尔,并进行多头损失.比较接受率与尼拉草图,通过缩小相同模型.
   中文翻译:实现一个小型梅杜萨:取第14课的GPT毕业项目,添加3个额外的LM头预测位置 t+2、t+3、t+4──使用联合多头损失在小小小的培训──与截断相同模型得到的简单草案的接受率──
4. **Hard.**实现反弹:从10代标前标KV缓存开始,输入5个草案代标,模拟在3位的拒绝.在下一次回复时,检查缓存读数正确匹配"前标+第2个接受草案".
   中文翻译:实现回滚:从10个代币的前 KV 缓存开始,输入5个草案代币,模拟位置3的拒绝――验证你的缓存读取在下一代时正确匹配"前 + 前2个已接受草案"――

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Draft model | "The cheap one" | A smaller model that proposes candidate tokens; usually 10–50× cheaper than the verifier. |
| 草案模型 | "便宜的那个" | 提出候选 token 的较小模型；通常比验证器便宜 10-50 倍。 |
| Verifier | "The big one" | The target model whose distribution we preserve; runs once per speculative step. |
| 验证器 | "大的那个" | 我们要保持其分布的目标模型；每次推测步骤运行一次。 |
| Acceptance rate (α) | "How often the draft is right" | Per-token probability that the verifier accepts the draft. 0.7–0.9 typical. |
| 接受率 (α) | "草案正确的频率" | 验证器接受草案的每 token 概率。典型值 0.7-0.9。 |
| Residual distribution | "The rejection fallback" | `(q - p)_+` normalized; sampling from this on rejection preserves the verifier's distribution. |
| 残差分布 | "拒绝时的后备方案" | `(q - p)_+` 归一化；拒绝时从中采样保持验证器的分布。 |
| Bonus token | "The free one" | When all N drafts accepted, sample one more from the verifier's next-step distribution. |
| 奖励 token | "免费的那个" | 当所有 N 个草案被接受时，从验证器的下一步分布中多采样一个。 |
| Medusa | "Draft-less speculative" | Multiple LM heads on the verifier predict positions t+1..t+k in parallel. |
| Medusa | "无草案推测" | 验证器上的多个 LM 头并行预测位置 t+1..t+k。 |
| EAGLE | "Hidden-state draft" | Tiny transformer draft conditioned on the verifier's last-layer hidden states. |
| EAGLE | "隐藏状态草案" | 以验证器最后一层隐藏状态为条件的小型 Transformer 草案。 |
| Lookahead decoding | "Jacobi iteration" | Self-speculation using a fixed-point iteration; no draft model. |
| 前瞻解码 | "Jacobi 迭代" | 使用不动点迭代的自推测；无需草案模型。 |
| Tree attention | "Verify many candidates at once" | Branching verification that considers several draft continuations simultaneously. |
| 树注意力 | "同时验证多个候选" | 同时考虑多个草案续写的分支验证。 |
| KV rollback | "Undo rejected drafts" | Scratch KV buffer; commit on acceptance, discard on reject. |
| KV 回滚 | "撤销被拒绝的草案" | 临时 KV 缓冲区；接受时提交，拒绝时丢弃。 |

## 继续阅读 继续阅读

- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192)核心算法和等效定理.
  中文翻译:推测解码的核心算法和等价定定理论文文──
- [Chen et al. (2023). Accelerating Large Language Model Decoding with Speculative Sampling](https://arxiv.org/abs/2302.01318)同时引入;清洁的伯诺利拒绝证明.
  中文翻译:同时期发表的推测采样论文;清晰的伯努利拒绝证明──
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774)梅杜萨纸;树木注意力验证.
  中文翻译:Medusa 论文;树注意力验证。
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077)-1;隐藏状态的预案.
  中文翻译:EAGLE-1论文;隐藏状态条件草案.
- [Li et al. (2024). EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees](https://arxiv.org/abs/2406.16858)-2;动态树深度.
  中文翻译:EAGLE-2论文;动态树深度──
- [Li et al. (2025). EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test](https://arxiv.org/abs/2503.01840)3号.
  中文翻译:EAGLE-3论文──
- [Fu et al. (2024). Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](https://arxiv.org/abs/2402.02057)看着,没有草稿的方法.
  中文翻译:前解码论文,无草案方案──
- [vLLM docs — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode.html)可信生产参考,四个战略都连接在一起.
  中文翻译:vLLM 推测解码文档,四种策略的生产参考.
- [SafeAILab / EAGLE reference implementation](https://github.com/SafeAILab/EAGLE) EAGLE-1/2/3的参考代码.
  中文翻译:EAGLE-1/2/3 参考实现代码──
