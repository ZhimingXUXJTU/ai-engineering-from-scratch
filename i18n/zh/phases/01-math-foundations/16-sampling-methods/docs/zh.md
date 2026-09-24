# 采样方法

> 采样是人工智能如何探索可能性的空间.
> 采样是AI探索空间的方法.

**Type:** Build | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 1, Lessons 06-07 (Probability, Bayes' Theorem) | **前置知识:** Phase 1, 第 06-07 课（概率、贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## 学习目标

- 通过单一随机数量从零开始实施反向CDF,拒绝和重点样本
  使用均随机数从零实现反CDF(反CDF) 拒绝采样(拒绝采样) 和重要性采样(重要性采样)
- 构建温度,顶-k和顶-p (核心) 样本,用于语言模型代币生成
  构建用于语言模型代币 生成温度、顶-k 和顶-p(核)采样
- 解释重构化技巧以及为什么它通过AVE样本采集使反扩散成为可能
  解释重参数化技巧 (重参数化技巧) 和为什么它能使AE中采样操作支持反向传播
- 运行Metropoolis-Hastings MCMC从一个不正常化的目标分布中采样
  运行 都市-哈斯廷斯 MCMC 从未归化目标分布中采样


> **【中文解读】**
> 采样是AI 探索可能性的方法――LLM 用温度/顶-k/顶-p 控制文本生成多样性――VAE 用重参数化技巧让采样可微――扩散模型的前向过程是采样 (加噪),反向过程是去噪音 (生成) ――

## 问题 问题引入

语言模型完成了处理提示,产生了5万个标记的向量.一个用于其词汇中的每个代币.现在它必须选择一个.

> 语言模型处理你的提示后,会产生一个包含50,000个逻辑的向量,对应词汇表中的每个代币.

如果它总是选择最高概率的代币,每个反应都是相同的. 确定性. 无聊. 如果它随机选择均,输出是的. 答案在这些极端之间某个地方生活,在某个地方由样本控制.

> 如果每次都选出最高概率的代币,每次回答都一样确定性、无聊的. 如果均随机选出,输出就是胡言乱语.

采样不仅限于文本生成. 强化学习通过采样轨迹估计政策梯度. 通过从学习分布中抽样并通过随机性传播,VAE学习隐藏的表示. 扩散模型通过采样噪音和反复测试生成图像. 蒙特卡罗方法估计没有封闭形式的整体.  MCMC算法探索不可能编译的高维后部分布.

> 采样不仅限于文本生成――强化学习通过采样轨迹 (轨迹) 来估计策略梯度――VAE 通过从学习到分布中采样并反向传播来学习隐藏表示――扩散模型通过采样噪声并代噪声来生成图像――蒙特卡洛方法估计没有解析的积分――MCMC算法探索无法枚举的高维后验分布――

每个生成人工智能系统都是采样系统.采样策略决定了输出的质量,多样性和可控制性.这个课程从零开始构建了每种主要采样方法,从统一的随机数开始,并以支持现代LLM和生成模型的技术结束.

> 每个生成式AI系统本质上都是采样系统.采样策略决定了输出质量,多样性和可控性.本课程从零构建所有主要采样方法,从平均随机数量开始,直到驱动现代 LLM和生成模型的技术.

## 概念的核心概念

> **【中文解读】**
> 采样问题无处不在:语言模型需要从5万个代币中选一个,VAE需要从隐空间采样,扩散模型需要从噪音逐步到噪音.核心挑战是,你只能直接从简单分布 (均分布、正态分布) 采样,必须通过巧妙的变化来获得复杂的目标分布样本.

### 为什么样本采样是重要的

采样表现出在人工智能和机器学习中四个基本角色:

> 采样在人工智能和机器学习中扮演四个基本角色:

**Generation.**语言模型,扩散模型和GAN都通过采样产生输出.采样算法直接控制创造力,一致性和多样性.温度,顶级k和核采样是工程师每天转换的按.

> **生成。**采样算法直接控制创造力连贯性和多样性.

**Training.**缩梯度下降样本小批. 脱节样本神经元去关闭. 数据增强样本随机转变. 重要样本重量样本以减少增强学习的梯度差异 (PPO,TRPO).

> **训练。**随机梯度下降(SGD) 采样迷你批量――推出 采样要禁用神经元――数据增强采样随机变化――重要性采样重新加权样本以降低强化学习――PPO、TRPO) 中的梯度方差――

**Estimation.**许多数量在ML中没有封闭形式的解决方案.数据分布的预期损失,基于能量的模型的分区函数,贝叶斯推理中的证据.蒙特卡罗估计通过对样本进行平均估算来近似所有这些.

> **估计。**许多ML中数量没有解析. 数据分布上的预期损失.基于能量模型的配分函数.贝叶斯推断中的证据.

**Exploration.**马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克思马克斯马克斯马克斯马克斯马克斯马克斯马克斯马克斯马克斯

> **探索。**普森 采样在多臂老虎机问题中平衡探索与利用――

基本挑战是:只能直接从简单分布中取样 (均,正常).

> 核心挑战:你只能直接从简单分布 (简单分布) 中采样.

> **【拓展：LLM 采样策略的工程实践】**
> 在GPT-4等模型推理时,温度通常设为0.0-1.0,顶-p设为0.9-1.0──OpenAI API默认温度=1.0、top_p=1.0──研究表明顶-p (核) 采样在大多数任务上优于顶-k,因为它可以根据模型依赖自适应调整候选集大小──对于代码生成,温度=0.2 + top_p=0.95 是常见配置──

### 统一的随机抽样

每种采样方法都从这里开始. 一个统一的随机数生成器在 [0, 1) 中产生值,每个相同长度的子间隔都有相同的概率.

> 所有采样方法都从这里开始. 均随机数生成器产生[0, 1) 中值,其中等长的子区间具有相等的概率.

```
U ~ Uniform(0, 1)

P(a <= U <= b) = b - a    for 0 <= a <= b <= 1

Properties:
  E[U] = 0.5
  Var(U) = 1/12
```

为了从一个单独的集合 n 项中均地采样,生成 U,返回地板(n * U.

> 要从 n 个元素的离散集合中均采样,生成 U 并返回地板(n * U) ⋅要从连续区间 [a, b] 中采样,计算 a + (b - a) * U。

基本的见解是:一个统一的随机数量包含了正确的随机数量,

> 关键洞察:单个均随机数包含恰好足够的随机性,可以从任何分布中产生一个样本.

> **【中文解读】**
> 均分布是所有采用基石的. 计算机中的伪随机数生成器 (如Mersenne Twister) 产生的就是 [0,1) 上的均分布. 采用方法本质上是把均随机数"变换"成目标分布的样本,就像用一个万能钥匙打开不同的锁.

### 逆转CDF方法 (逆转转换样本采样)

累积分布函数 (CDF) 将值映射到概率:

```
F(x) = P(X <= x)

Properties:
  F is non-decreasing
  F(-inf) = 0
  F(+inf) = 1
  F maps the real line to [0, 1]
```

如果 U ~ 均(0, 1),那么X = F_inverse(U) 遵循目标分布.

> 如果 U ~ 均的(0, 1),那么X = F_inverse(U) 服从目标分布──

```
Algorithm:
  1. Generate u ~ Uniform(0, 1)
  2. Return F_inverse(u)

Why it works:
  P(X <= x) = P(F_inverse(U) <= x) = P(U <= F(x)) = F(x)
```

**Exponential distribution example:**

```
PDF: f(x) = lambda * exp(-lambda * x),   x >= 0
CDF: F(x) = 1 - exp(-lambda * x)

Solve F(x) = u for x:
  u = 1 - exp(-lambda * x)
  exp(-lambda * x) = 1 - u
  x = -ln(1 - u) / lambda

Since (1 - U) and U have the same distribution:
  x = -ln(u) / lambda
```

对于正常分布来说,没有封闭形式的反向CDF,所以我们使用其他方法 (Box-Muller或数值近似).

> 当你能写出F_inverse的解析表达式时,这个方法完美运作──对于正态分布,没有解析形式的反CDF,所以我们使用其他方法(Box-Muller或数值近似)──

**Discrete version:**对于分离分布,将CDF构建为累计数量,生成U,并找到第一个指数,当累计数量超过U.`sample_categorical`在第06课中工作.

> **离散版本：**对于离散分布,将CDF构建为累积和,生成U,找到累积和第一次超过U的索引.`sample_categorical`的工作方式.

> **【中文解读】**
> 逆 CDF 方法的核心思想:CDF 函数 F(x) 将随机变量的值映射到 [0,1] 上的概率,而它的逆函数 F_inverse 正好反过来把 [0,1] 上的均随机数映射回目标分布值──这个方法精确、高效,但前提是你能写出逆函数的解析表达式──

### 拒绝样本

当你不能逆转CDF,但可以评估目标PDF到一个常态,拒绝样本工作.

> 当你无法求逆CDF,但可以计算目标 PDF (至多差一个常数因子) 当,拒绝采样 (拒绝采样) 否则可以派上场用.

```
Target distribution: p(x)  (can evaluate, possibly unnormalized)
Proposal distribution: q(x)  (can sample from)
Bound: M such that p(x) <= M * q(x) for all x

Algorithm:
  1. Sample x ~ q(x)
  2. Sample u ~ Uniform(0, 1)
  3. If u < p(x) / (M * q(x)), accept x
  4. Otherwise, reject and go to step 1

Acceptance rate = 1/M
```

通过测试,测试结果的结果会变得更为明显,因为测试结果的大部分量都会被拒绝.

> 包络 M 越紧,接受率越高――在低维空间 (在低维空间) 1-3维),拒绝采样效果很好――在高维空间,接受率呈指数下降,因为大部分的提议体积都被拒绝了――这就是拒绝采样维数灾难――

**Example: sampling from a truncated normal.**采用一个统一的建议在缩短范围. 包裹M是该范围内的正常PDF的最大.

> **示例：从截断正态分布采样。**在截止范围内使用均提议分布──包网 M 是正态 PDF 在该范围内的最大值──

**Example: sampling from a semicircle.**通过一个直角的直角,在直角的边缘上均地提出.如果点落在半圆中,则接受.

> **示例：从半圆采样。**在外接矩形中均提议. 如果点落在半圆内就接受. 这就是蒙特卡洛计算的方法:接受率等于面积比 pi/4.

> **【拓展：拒绝采样在粒子滤波中的应用】**
> 粒子波 (粒子波) 是目标跟踪和机器定位的核心算法. 它本质上是一种拒绝采样的方法.

### 重要性样本

有时你不需要从目标分布 p(x) 样本,你需要在 p(x) 下估计预期,并且你有来自不同的分布 q(x) 的样本.

> 有时你不需要从目标分布 p  中采样,而是需要在 p  下估计一个期望,而你手上有来自另一个分布 q  x) 的样本.

```
Goal: estimate E_p[f(x)] = integral of f(x) * p(x) dx

Rewrite:
  E_p[f(x)] = integral of f(x) * (p(x)/q(x)) * q(x) dx
            = E_q[f(x) * w(x)]

where w(x) = p(x) / q(x)  are the importance weights.

Estimator:
  E_p[f(x)] ~ (1/N) * sum(f(x_i) * w(x_i))    where x_i ~ q(x)
```

在强化学习中,这是关键的.在PPO (近距离政策优化) 中,你收集了旧政策 pi_old的轨迹,但想优化新政策 pi_new.重要重量是 pi_new                                                                                                                                                                                                                                     

> 在强化学习中至关重要. 在PPO中,你在旧策略中收集轨迹,但想优化新策略 pi_new.

> **【拓展：PPO 中的重要性采样】**
> 普普是ChatGPT RLHF 训练的核心算法――它用重要意义来修改新旧策略之间的分布差异――PPO 的关键创新是剪切 (剪切) 剪切:当重要意义权重比率 = pi_new/pi_old 超出 [1-epsilon, 1+epsilon] 范围时(epsilon 通常为0.2),截梯度防止策略更新过大――这使训练比TRPO更稳定高效.

重要性采样估计器的差异取决于q与p有多相似.如果q与p非常不同,几种样本会获得巨大的重量,占据估计的地位.自我正常化的重要性采样将由重量的总和划分以减少这个问题:

> 重要性采样估计器的差异取决于q与p的相似程度. 如果q与p的差异很大,少数样本会获得巨大的权重并主导估计.

```
E_p[f(x)] ~ sum(w_i * f(x_i)) / sum(w_i)
```

### 蒙特卡罗估计

蒙特卡罗估计通过平均随机样本来接近整体. 大数法保证了融合.

> 蒙特卡洛估计通过随机样本的平均取近积分.

```
Goal: estimate I = integral of g(x) dx over domain D

Method:
  1. Sample x_1, ..., x_N uniformly from D
  2. I ~ (Volume of D / N) * sum(g(x_i))

Error: O(1 / sqrt(N))   regardless of dimension
```

错误率是不依赖维度的,这就是为什么蒙特卡罗方法在高维度中占主导地位,而在网格基础上的整合是不可能的.

> 误差率与维度无关.这就是为什么蒙特卡洛方法在高维空间中占据主导地位.

> **【中文解读】**
> 卡洛方法的精髓:使用随机样本的平均值来近似预期. 大数定律保证收,而且误差率O(1/sqrt(N)) 与维度无关.

**Estimating pi:**

```
Sample (x, y) uniformly from [-1, 1] x [-1, 1]
Count how many fall inside the unit circle: x^2 + y^2 <= 1
pi ~ 4 * (count inside) / (total count)
```

**Estimating expectations:**

```
E[f(X)] ~ (1/N) * sum(f(x_i))    where x_i ~ p(x)

The sample mean converges to the true expectation.
Variance of the estimator = Var(f(X)) / N
```

### 马科夫链蒙特卡罗 (MCMC):大都会-哈斯廷斯

 MCMC构建一个马科夫链,其静止分布是目标分布 p(x).经过足够的步骤,链中的样本是 (约) p(x 的样本.

>  MCMC 构建一个马尔可夫链 (Markov Chain),其平稳分布 (Stationary Distribution) 就是目标分布 (p(x) ⋅经过足够多的步数后,链上的样本 (近似地) 是p(x) 的样本.

```
Target: p(x)  (known up to a normalizing constant)
Proposal: q(x'|x)  (how to propose the next state given the current state)

Metropolis-Hastings algorithm:
  1. Start at some x_0
  2. For t = 1, 2, ..., T:
     a. Propose x' ~ q(x'|x_t)
     b. Compute acceptance ratio:
        alpha = [p(x') * q(x_t|x')] / [p(x_t) * q(x'|x_t)]
     c. Accept with probability min(1, alpha):
        - If u < alpha (u ~ Uniform(0,1)): x_{t+1} = x'
        - Otherwise: x_{t+1} = x_t
  3. Discard first B samples (burn-in)
  4. Return remaining samples
```

对于对称式提案 (q(x'的说法x) = q(x的说法x') 则比率简化为p(x')/p(x. 这就是原来的Metrolis算法.

> 对于对称提议 (q) = q) ),比率简化为 p) ') /p)  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  () )  ()  ()  ()  ()  () )  ()  ()  () )  ()  ()  ()  ()  ()  ()  ()  ()  ()  () 

**Why it works.**接受规则确保了详细的平衡:在 x 处的概率和移动到 x 处的概率等于在 x 处的概率和移动到 x. 详细的平衡意味着 p x) 是链的静止分布.

> **为什么有效。**接受规则确保细致平衡条件:在 x 转移到 x 的概率等于在 x 转移到 x 的概率.

> **【拓展：MCMC 在贝叶斯深度学习中的应用】**
> 在药物发现中,研究人员使用MCMC采样分子构造后验分布,处理数千维参数空间――Stan语言 (统计学家斯坦尼斯拉夫·乌拉姆命名) 让研究人员无需手写MCMC就能进行贝叶斯推理――

**Practical considerations:**
- 燃烧:在链达到平衡之前,丢弃早期样本
  预热期(燃烧): 抛弃链达到平衡前的早期样本
- 稀释:保持每一个k-th样本以减少自动相关性
  稀释:每隔一小时保持一个以减少自相关
- 提案规模:太小,链路缓慢 (接受度高,探索度慢);太大,大多数提案被拒绝 (接受度低,不适用)
  提议尺度(提议规模):太小则链移动缓慢(接受率高但探索慢);太大则大多数提议被拒绝(接受率低,原地不动)
- 高尺寸高的高斯提案的最佳接受率是约0.234
  高维空间中高斯提议的最佳接受率约为0.234

### 吉布斯样本

吉布斯样本采集是 MCMC的多变量分布的一个特殊例.它不是一次地提出所有维度的移动,而是一次更新一个变量从其条件分布.

> 吉布斯采样是MCMC在多变量分布中的特例. 它不是同时在所有维度上提议移动,而是每次从条件分布中更新一个变量.

```
Target: p(x_1, x_2, ..., x_d)

Algorithm:
  For each iteration t:
    Sample x_1^{t+1} ~ p(x_1 | x_2^t, x_3^t, ..., x_d^t)
    Sample x_2^{t+1} ~ p(x_2 | x_1^{t+1}, x_3^t, ..., x_d^t)
    ...
    Sample x_d^{t+1} ~ p(x_d | x_1^{t+1}, x_2^{t+1}, ..., x_{d-1}^{t+1})
```

基布斯样本需要你可以从每个条件分布中样本 p  x 
- 贝叶斯网络:从图形结构中得到条件
  贝叶斯网络:条件分布由图结构决定
- 盖斯混合物:条件是盖斯混合物
  高斯混合模型:条件分布是高斯的
- 异性模型:每个旋转的条件只取决于其邻居
  模型:每个自旋的条件分布只依赖于其邻居

接受率总是1 (每一个提案都被接受),因为从具体条件中抽样自动满足详细的平衡.

> 接受率永远是1 (每一个提议都被接受),因为从精确的条件分布中采样自动满足细致平衡条件.

**Limitation.**当变量高度相关时,吉布斯采样会缓慢混合,因为一次更新一个变量不能通过分布进行大角形移动.

> **局限性。**当变量之间高度相关时,吉布斯采样很慢地混合,因为每次更新一个变量无法在分布中产生很大的对角移动.

> **【中文解读】**
> 吉布斯采样是MCMC的特例:每次只更新一个变量,从条件分布中采样. 因为每次采样都来自精确的条件分布,所以接受率永远是100%.

### 温度样本 (用于LLM)

语言模型输出语文库中的每个代币的 logits z_1, ..., z_V. Softmax 将这些转换为概率.

> 语言模型为词汇表中的每个代币输出 logits z_1, ..., z_V──软max 将它们转换为概率──温度(温度) 在软max 之前对 logits 进行缩放:

```
p_i = exp(z_i / T) / sum(exp(z_j / T))

T = 1.0: standard softmax (original distribution)
T -> 0:  argmax (deterministic, always picks highest logit)
T -> inf: uniform (all tokens equally likely)
T < 1.0: sharpens the distribution (more confident, less diverse)
T > 1.0: flattens the distribution (less confident, more diverse)
```

**Why it works.**通过将分数为T < 1 放大分数之间的差异.如果z_1 = 2 和z_2 = 1,除以T = 0.5 给出z_1/T = 4 和z_2/T = 2,使得差距更大.软max后,最高分数的代币获得更大的份额.

> **为什么有效。**将分数除以T < 1 会加大分数之间的差异.如果z_1 = 2、z_2 = 1,除以T = 0.5 得到z_1/T = 4、z_2/T = 2,差距更大了.经过软max 之后,最高分数的分数得到更大的份额.

**In practice:**
- 率为0.0:贪的解码,最适合事实质疑问答
  贪心解码,最适合事实性问答
- 微小创意,适合代码生成
  略有创意,适合代码生成
- 率为0.7-1.0:平衡,适合一般对话
  均衡,适合一般对话
- 创意写作,脑风暴
  创意写作、头脑风暴
-  > 1.5:越来越随机,很少有用
  越来越随时,很少有用

温度不会改变哪些代币可能,而是改变每个代币分配的概率量.

> 温度不会改变哪些代币可能被选中.

> **【中文解读】**
> 温度是 LLM 输出多样性的"旋"──T < 1 让分布更尖(更像贪心),T > 1 让分布更平坦(更随机)──T → 0 退化为 argmax,T → ∞ 退化为均分布──实际中T=0.7 是最常用的平衡点──注意:温度不改变哪些符号有可能被选中,只改变概率分配──

### 顶部样本

顶k样本限制了候选集合到具有最高概率的 k代币,然后重新正常化和从该限制集合中样本.

> 顶级采样将限制选项集为概率最高的 k 个代币,然后重新归纳并从该受限集合中采样.

```
Algorithm:
  1. Compute softmax probabilities for all V tokens
  2. Sort tokens by probability (descending)
  3. Keep only the top k tokens
  4. Renormalize: p_i' = p_i / sum(p_j for j in top-k)
  5. Sample from the renormalized distribution

k = 1:  greedy decoding
k = V:  no filtering (standard sampling)
k = 40: typical setting, removes long tail of unlikely tokens
```

顶k 阻止模型在词汇分布的长尾中选择极其不可能的代币 (typos, nonsense).问题:k 无论文本如何都固定.当模型自信 (一个代币有95%的概率),k = 40仍然允许39种替代方案.当模型不确定 (概率分布在1000个代币),k = 40 切断了可行的选择.

> 问题在于:k 是固定的,不随下文变化而下面. 当模型非常有信心时,一个代币占比95%的概率),k = 40 仍然允许39个替代选项.

### 顶部 (核) 样本

顶p样本调整了候选集体大小.它不保留固定数量的代币,而是保留了超过p的最小的代币集.

> 顶点p 采样动态调整候选人集大小──它不保留固定数量的代币,而是保留积累概率超过p的最小代币集合──

```
Algorithm:
  1. Compute softmax probabilities for all V tokens
  2. Sort tokens by probability (descending)
  3. Find smallest k such that sum of top-k probabilities >= p
  4. Keep only those k tokens
  5. Renormalize and sample

p = 0.9:  keeps tokens covering 90% of probability mass
p = 1.0:  no filtering
p = 0.1:  very restrictive, nearly greedy
```

当模型自信时,核样本采集保持少量的代币 (可能是2-3).当模型不确定时,它保留许多代币 (可能是200).这种适应性行为是为什么核样本采集通常产生比顶级k更好的文本.

> 当模型有信心时,核心采样只保留少量标记 (可能2-3个) ⋅当模型不确定时,它保留很多 (可能200个) ⋅这种自适应行为是核心采样通常比顶级产生更好的文本原因──

**Common combinations:**
- 温度0.7 +上层p0.9:一般用途的设置良好
  很好的通用设置
- 温度0.0 (贪):最适合确定性任务
  最适合确定性任务
- 温度1.0+顶-k50:Fan et al. (2018) 原始纸设置
  粉丝等 (2018) 原论文设置

首先应用top-k,然后在剩余的集合上应用top-p.

> 顶-k 和顶-p 可以组合使用――先应用 top-k,再在剩余集合上应用 top-p――

### 修复尺寸化技巧 (在 VAEs 中使用)

变化自动编码器 (VAE) 通过编码输入到隐藏空间中的分布中,从该分布中取样,并重新解码样本学习.问题是:通过采样操作无法反传播.

> 变分自编码器(VAE) 通过将编码输入为隐藏空间分布、从该分布采样、然后将样本解码回来学习──问题是:你无法通过采样操作进行反向传播──

```
Standard sampling (not differentiable):
  z ~ N(mu, sigma^2)

  The randomness blocks gradient flow.
  d/d_mu [sample from N(mu, sigma^2)] = ???
```

复制化技巧将随机性与参数分开:

> 重参数化技巧将随机与参数分开:

```
Reparameterized sampling:
  epsilon ~ N(0, 1)          (fixed random noise, no parameters)
  z = mu + sigma * epsilon   (deterministic function of parameters)

  Now z is a deterministic, differentiable function of mu and sigma.
  d(z)/d(mu) = 1
  d(z)/d(sigma) = epsilon

  Gradients flow through mu and sigma.
```

这就像在 N                                                                                                                                                                                                                                                             

> 这之所以有效,是因为N(mu,sigma^2) 与mu +sigma *N(0,1) 具有相同的分布.

**In the VAE training loop:**
1. 编码器输出mu和 log(sigma^2) 每次输入
2. 样本 (N(0,1)
3. 计算 z = mu + sigma * epsilon
4. 解码z来重建输入
5. 通过步骤4,3,2,1 (可能因为步骤3是可分化的)

没有重构化技巧,无线电传输器无法通过标准的背扩散训练.

> 没有重参数化技巧,VAE就无法使用标准反向传播训练.

> **【拓展：重参数化技巧的广泛应用】**
> 重参数化技巧不限于VAE──扩散模型(稳定扩散、DALL-E) 的每一步都使用重参数化:z = mu + sigma * epsilon──强化学习中,SAC (软演员-批判) 用重参数化计算策略梯度──可以说,只要涉及"从可学习分布中采样+反向传播",就不开开这一技巧──

### 贝尔-软max (可分类的类型样本)

复制分量方法对连续分布 (高斯式) 有效.对于分离的分类分布,我们需要不同的方法.Gumbel-Softmax为分类采样提供了可差距的近似方法.

> 对于分散分类分布,我们需要不同的方法.

**The Gumbel-Max trick (non-differentiable):**

```
To sample from a categorical distribution with log-probabilities log(p_1), ..., log(p_k):
  1. Sample g_i ~ Gumbel(0, 1) for each category
     (g = -log(-log(u)), where u ~ Uniform(0, 1))
  2. Return argmax(log(p_i) + g_i)

This produces exact categorical samples.
```

**Gumbel-Softmax (differentiable approximation):**

```
Replace the hard argmax with a soft softmax:
  y_i = exp((log(p_i) + g_i) / tau) / sum(exp((log(p_j) + g_j) / tau))

tau (temperature) controls the approximation:
  tau -> 0:  approaches a one-hot vector (hard categorical)
  tau -> inf: approaches uniform (1/k, 1/k, ..., 1/k)
  tau = 1.0: soft approximation
```

贝尔-软max产生一个离散样本的连续放松.输出是概率向量 (软一个热) 而不是硬一个热.渐变体通过软max流.在训练中前进通过时,你可以使用"直径"估计器:使用硬 argmax 进行前进通过,但软的贝尔-软max 渐变体用于后退通过.

> 贝尔-软max 产生离散样本的连续松(连续放松) ――输出是一个概率向量(软一个热) 而不是硬一个热――梯度可以流过软max──在训练的前向传播中,你可以使用"直通估计器" ((直通过估计器):前向传播使用硬 argmax,反向传播使用软 Gumbel-软max 梯度──

**Applications:**
- 隐形变量在 VAEs中
  中离散隐藏变量
- 神经架构搜索 (选择分离操作)
  神经架构搜索 (选择离散操作)
- 硬注意力机制
  硬注意力机制
- 通过单独行动加强学习
  离散动作的强化学习

### 层次采样

标准蒙特卡罗样本采集可以随机在样本空间中留下空隙. 层次采集通过将空间分为层次并从每个层中采样来进行覆盖.

> 标准蒙特卡洛采样可能偶然在样本空间中留下空隙――分层采样―― 通过将空间分为层 (Strata) 并从每个层中采样来强制均覆盖――

```
Standard Monte Carlo:
  Sample N points uniformly from [0, 1]
  Some regions may have clusters, others gaps

Stratified sampling:
  Divide [0, 1] into N equal strata: [0, 1/N), [1/N, 2/N), ..., [(N-1)/N, 1)
  Sample one point uniformly within each stratum
  x_i = (i + u_i) / N   where u_i ~ Uniform(0, 1),  i = 0, ..., N-1
```

与标准蒙特卡罗相比,层样本总是具有较低或相同的差异:

> 层面的差距总是低于或等于标准卡洛:

```
Var(stratified) <= Var(standard Monte Carlo)

The improvement is largest when f(x) varies smoothly.
For piecewise-constant functions, stratified sampling is exact.
```

**Applications:**
- 数字整合 (近蒙特卡洛)
  数值积分(准蒙特卡洛)
- 培训数据分类 (确保每个阶段的类平衡)
  训练数据划分 (确保每折的类别平衡)
- 具有重要性的采样与分层 (结合两种技术)
  结合分层的重要性采样
- 通过NeRF (神经辐射场) 采用相机射线沿线的层次采样
  通过相机光线使用分层采样

### 连接到扩散模型

扩散模型通过采样过程生成图像.前进过程将高斯噪音添加到图像中,直到它变成纯噪音.反向过程学习了指代,逐步恢复原始图像.

> 扩散模型通过采样过程生成图像. 前向过程在T 步骤内逐渐向图像增加高噪音,直到变成纯噪音. 反向过程学习去噪音,逐步恢复原始图像.

```
Forward process (known):
  x_t = sqrt(alpha_t) * x_{t-1} + sqrt(1 - alpha_t) * epsilon
  where epsilon ~ N(0, I)

  After T steps: x_T ~ N(0, I)  (pure noise)

Reverse process (learned):
  x_{t-1} = (1/sqrt(alpha_t)) * (x_t - (1 - alpha_t)/sqrt(1 - alpha_bar_t) * epsilon_theta(x_t, t)) + sigma_t * z
  where z ~ N(0, I)

  Each denoising step is a sampling step.
```

在本课程中使用的方法的联系:
- 每个测试步骤都使用了重设设法 (样本噪音,应用定性转换)
  每个去噪音步骤都使用重参数化技巧 (采样噪音,应用确定性变化)
- 噪音时间表控制一种温度调节
  噪声调度 {alpha_t} 控制一种形式的温度退火(温度调节)
- 训练使用蒙特卡罗估计接近ELBO (证据下限)
  训练使用蒙特卡洛估计来接近ELBO(证据下限,证据下界)
- 在扩散模型中,祖先采样是马科夫链 (每个步骤只取决于当前状态)
  扩散模型中的祖先采样 (代样本) 是一个马尔可夫链 (每一步只依赖于当前状态)

整个图像生成过程都是反复采样:从噪音开始,并在每一步都采样一个稍微不那么噪音的版本,根据学习的化模型.

> 整个图像生成过程都是代采样:从噪音开始,在每一步,基于学习到去噪音模型采样一个稍微不那么杂的版本.

## 建立它,实现它.
```figure
monte-carlo-pi
```

## 建立它

### 步骤1:均和反向的CDF采样

```python
import math
import random

def sample_uniform(a, b):
    return a + (b - a) * random.random()  # 线性变换：把 [0,1) 映射到 [a,b)

def sample_exponential_inverse_cdf(lam):
    u = random.random()                   # 生成均匀随机数
    return -math.log(u) / lam             # 逆 CDF：x = -ln(u) / lambda
```

生成1万个指数样本,验证平均值为1/lambda.

> 生成 10,000 个指数分布样本,验证平均值是否为 1/lambda──

### 步骤2:拒绝采样

```python
def rejection_sample(target_pdf, proposal_sample, proposal_pdf, M):
    while True:                           # 持续采样直到被接受
        x = proposal_sample()             # 从提议分布采样
        u = random.random()               # 均匀随机数用于决定接受/拒绝
        if u < target_pdf(x) / (M * proposal_pdf(x)):  # 接受条件
            return x
```

使用拒绝样本从一个缩小的正常分布中抽取.通过对样本进行 histogramming来验证形状.

> 使用拒绝采样从截断正态分布中抽样――通过绘制直方图验证形状――

### 步骤3:重要性样本

```python
def importance_sampling_estimate(f, target_pdf, proposal_pdf, proposal_sample, n):
    total = 0
    for _ in range(n):
        x = proposal_sample()
        w = target_pdf(x) / proposal_pdf(x)
        total += f(x) * w
    return total / n
```

根据统一的建议,在正常分布下估计E[X^2]. 与已知答案 (mu^2 + sigma^2) 进行比较.

> 使用均提议分布估计正态分布下 E[X^2]──与已知答案 (mu^2 + sigma^2) 比较──

### 步骤4:蒙特卡罗估计 pi

```python
def monte_carlo_pi(n):
    inside = 0
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x*x + y*y <= 1:
            inside += 1
    return 4 * inside / n
```

### 步骤5: 城市-哈斯廷斯 MCMC

```python
def metropolis_hastings(target_log_pdf, proposal_sample, proposal_log_pdf, x0, n_samples, burn_in):
    samples = []
    x = x0                                # 初始状态
    for i in range(n_samples + burn_in):
        x_new = proposal_sample(x)        # 从提议分布生成新候选
        log_alpha = (target_log_pdf(x_new) + proposal_log_pdf(x, x_new)  # 计算接受比的对数
                     - target_log_pdf(x) - proposal_log_pdf(x_new, x))
        if math.log(random.random()) < log_alpha:  # 以 min(1, alpha) 的概率接受
            x = x_new
        if i >= burn_in:                  # 丢弃 burn-in 阶段的样本
            samples.append(x)
    return samples
```

采用双模分布 (两个高斯人的混合物) 的样本.

> 从双峰分布 (双高的混合) 中采样――可视化链的轨迹――

### 第六步:吉布斯样本

```python
def gibbs_sampling_2d(conditional_x_given_y, conditional_y_given_x, x0, y0, n_samples, burn_in):
    x, y = x0, y0
    samples = []
    for i in range(n_samples + burn_in):
        x = conditional_x_given_y(y)
        y = conditional_y_given_x(x)
        if i >= burn_in:
            samples.append((x, y))
    return samples
```

### 步骤7:温度采样

```python
def softmax(logits):
    max_l = max(logits)
    exps = [math.exp(z - max_l) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

def temperature_sample(logits, temperature):
    scaled = [z / temperature for z in logits]  # 温度缩放：除以 T
    probs = softmax(scaled)                      # 计算缩放后的概率分布
    return sample_from_probs(probs)
```

显示温度如何改变一个符号 logit 的输出分布.

> 展示温度如何改变一组代币记录的输出分布――

### 步骤8:顶部k和顶部p样本

```python
def top_k_sample(logits, k):
    indexed = sorted(enumerate(logits), key=lambda x: -x[1])
    top = indexed[:k]
    top_logits = [l for _, l in top]
    probs = softmax(top_logits)
    idx = sample_from_probs(probs)
    return top[idx][0]

def top_p_sample(logits, p):
    probs = softmax(logits)
    indexed = sorted(enumerate(probs), key=lambda x: -x[1])
    cumsum = 0
    selected = []
    for token_idx, prob in indexed:
        cumsum += prob
        selected.append((token_idx, prob))
        if cumsum >= p:
            break
    sel_probs = [pr for _, pr in selected]
    total = sum(sel_probs)
    sel_probs = [pr / total for pr in sel_probs]
    idx = sample_from_probs(sel_probs)
    return selected[idx][0]
```

### 步骤9: 修复尺寸化技巧

```python
def reparam_sample(mu, sigma):
    epsilon = random.gauss(0, 1)          # 标准正态噪声，不含可学习参数
    return mu + sigma * epsilon            # 确定性变换，梯度可流过

def reparam_gradient(mu, sigma, epsilon):
    dz_dmu = 1.0                          # z 对 mu 的梯度恒为 1
    dz_dsigma = epsilon                   # z 对 sigma 的梯度是 epsilon
    return dz_dmu, dz_dsigma
```

证明梯度通过重构样本流动,但不是通过直接样本采集.

> 演示梯度可以通过重参数化样本流,但不能通过直接采样.

### 第十步:Gumbel-Softmax

```python
def gumbel_sample():
    u = random.random()
    return -math.log(-math.log(u))

def gumbel_softmax(logits, temperature):
    gumbels = [math.log(p) + gumbel_sample() for p in logits]
    return softmax([g / temperature for g in gumbels])
```

显示温度下降使输出接近单热向量.

> 展示降温如何使输出趋近一个热向量

完整的实现,所有可视化都在`code/sampling.py`现在,我们要去.

> 所有可视化的完整实现`code/sampling.py`在中.

## 用它实现框架

> **【拓展：扩散模型中的采样工程】**
> 从2022年发布以来,采样方法从DDPM的1000步代进化到DDIM、DPM-Solver++等只需要20-50步的方法.核心思想是把扩散ODE分散,使用高阶数值方法 (如Runge-Kutta) 加速采样.

通过NumPy和SciPy,生产版本:

> 使用NumPy 和 SciPy 的生产版本:

```python
import numpy as np

rng = np.random.default_rng(42)

exponential_samples = rng.exponential(scale=2.0, size=10000)
print(f"Exponential mean: {exponential_samples.mean():.4f} (expected 2.0)")

from scipy import stats
normal = stats.norm(loc=0, scale=1)
print(f"CDF at 1.96: {normal.cdf(1.96):.4f}")
print(f"Inverse CDF at 0.975: {normal.ppf(0.975):.4f}")

logits = np.array([2.0, 1.0, 0.5, 0.1, -1.0])
temperature = 0.7
scaled = logits / temperature
probs = np.exp(scaled - scaled.max()) / np.exp(scaled - scaled.max()).sum()
token = rng.choice(len(logits), p=probs)
print(f"Sampled token index: {token}")
```

对于 MCMC 规模,使用专用图书馆:
- PyMC:全方位贝耶斯模型与NUTS (适应性HMC)
  完整的贝叶斯建模,使用 NUTS(自适应 HMC)
- 机组:集体MCMC样品仪
  集成 MCMC采样器
- 编码: 编码: 编码: 编码:
   GPU 加速的 MCMC

你从头开始了,现在你知道图书馆的电话是什么.

> 你从零开始构建了这些方法.

## 练习题

1. 执行反向CDF样本测试.CDF为F(x) =0.5 + arctan(x) /pi.生成10,000个样本,与真实的PDF绘制历史图.注意重尾 (极端值远离中心).
   实现柯西分布 (Cauchy Distribution) 的逆CDF采样──CDF 为 F(x) = 0.5 + 极端 (x) /pi──生成10,000个样本并绘制直方图与真实的 PDF 对比──注意重尾(远离中心极端值)──

2. 使用拒绝样本生成Beta(2,5) 分布的样本,使用Uniform(0,1) 提案.将接受的样本与真实Beta PDF进行图谱.理论接受率是多少?
   使用拒绝采样从Beta(2, 5) 分布中生成样本,提议分布使用统一(0, 1)─绘制接受样本与真实Beta PDF的比较图──理论接受率是多少?

3. 通过1000,10,000和100,000个样本使用蒙特卡罗估算 sin(x) 的整体从0到pi. 根据每个级别的错误进行比较. 检查错误的规模为O(1/sqrt(N)).
   使用蒙特卡洛方法估计罪 (x) 在 0 到 pi 上积分,分别使用 1,000、10,000 和 100,000 个样本──比较各级的误差──验证误差按 O(1/sqrt(N)) 缩放──

4. 实施Metropoles-Hastings以以x,y) 比例于x,x2 * y2 + x2 + y2 - 8*x - 8*y) /2) 的二维分布进行样本.
   实现大都会-哈斯廷斯 从2D 分布 p(x,y) ~ exp(-(x^2*y^2 + x^2 + y^2 - 8x - 8y) /2) 中采样――绘制样本和链的轨迹――尝试不同的提议标准差──

5. 构建一个完整的文本生成演示:给出一个10个词汇和logits,使用 (a) 贪, (b) 温度=0.7, (c) 顶-k=3, (d) 顶-p=0.9生成20个代币的序列.
   构建一个完整的文本生成演示:给定 10 个词的词汇表和逻辑,使用 (a) 贪心、(b) 温度=0.7、(c) 顶-k=3、((d) 顶-p=0.9 生成 20 个代币的序列──比较 5 次运行的输出多样性──

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Sampling | "Drawing random values" | Generating values according to a probability distribution. The mechanism behind all generative AI |
| Uniform distribution | "All equally likely" | Every value in [a, b] has equal probability density 1/(b-a). The starting point for all sampling methods |
| Inverse CDF | "Probability transform" | F_inverse(U) converts a uniform sample into a sample from any distribution with known CDF. Exact and efficient |
| Rejection sampling | "Propose and accept/reject" | Generate from a simple proposal, accept with probability proportional to target/proposal ratio. Exact but wastes samples |
| Importance sampling | "Reweight samples" | Estimate expectations under p(x) using samples from q(x) by weighting each sample by p(x)/q(x). Core to PPO in RL |
| Monte Carlo | "Average random samples" | Approximate integrals as sample averages. Error O(1/sqrt(N)) regardless of dimension |
| MCMC | "Random walk that converges" | Construct a Markov chain whose stationary distribution is the target. Metropolis-Hastings is the foundational algorithm |
| Metropolis-Hastings | "Accept uphill, sometimes downhill" | Propose moves, accept based on density ratio. Detailed balance ensures convergence to target distribution |
| Gibbs sampling | "One variable at a time" | Update each variable from its conditional distribution holding others fixed. 100% acceptance rate |
| Temperature | "Confidence knob" | Divides logits by T before softmax. T<1 sharpens (more confident), T>1 flattens (more diverse) |
| Top-k sampling | "Keep the k best" | Zero out all but the k highest-probability tokens, renormalize, sample. Fixed candidate set size |
| Nucleus sampling (top-p) | "Keep the probable ones" | Keep the smallest set of tokens whose cumulative probability exceeds p. Adaptive candidate set size |
| Reparameterization trick | "Move randomness outside" | Write z = mu + sigma * epsilon where epsilon ~ N(0,1). Makes sampling differentiable. Essential for VAE training |
| Gumbel-Softmax | "Soft categorical sampling" | Differentiable approximation to categorical sampling using Gumbel noise + softmax with temperature |
| Stratified sampling | "Forced coverage" | Divide sample space into strata, sample from each. Always lower variance than naive Monte Carlo |
| Burn-in | "Warm-up period" | Initial MCMC samples discarded before the chain reaches its stationary distribution |
| Detailed balance | "Reversibility condition" | p(x) * T(x->y) = p(y) * T(y->x). Sufficient condition for p to be the stationary distribution of a Markov chain |
| Diffusion sampling | "Iterative denoising" | Generate data by starting from noise and applying learned denoising steps. Each step is a conditional sampling operation |

## 继续阅读 继续阅读

- [Holbrook (2023): The Metropolis-Hastings Algorithm](https://arxiv.org/abs/2304.07010)- 详细教程关于MCMC基础
- [Jang, Gu, Poole (2017): Categorical Reparameterization with Gumbel-Softmax](https://arxiv.org/abs/1611.01144)- 原始的Gumbel-Softmax纸
- [Holtzman et al. (2020): The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751)- 核 (上) 样本纸
- [Kingma & Welling (2014): Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)- 引入重构方法的VAE论文
- [Ho, Jain, Abbeel (2020): Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)- DDPM将采样与图像生成连接
