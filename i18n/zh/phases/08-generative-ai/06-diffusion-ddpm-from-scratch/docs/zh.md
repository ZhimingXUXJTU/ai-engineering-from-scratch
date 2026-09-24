# 扩散模型 从零实现DDPM

> 霍,贾因,阿贝尔 (2020) 给了该领域一个无法停止的食谱. 用千个小步骤的噪音摧毁数据.训练一个神经网络来预测噪音.在推断时逆转过程.今天每个主流图像,视频,3D和音乐模型都运行在这个循环上,可能是上层上有流量匹配或一致性技巧.

> **【中文解读】**基于此循环,可加上流量匹配或一致性技巧) 通过"DDPM"的核心流程,

> **【拓展：扩散模型是当前 AI 生成的核心】**稳定扩散,DALL-E 3 Midjourney 索拉都基于扩散模型.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 8 · 02 (VAE)
**Time:** ~75 minutes

## 问题 问题引入

你想要一个样本器`p_data(x)`们玩的是一个常常分的最小量游戏.VAE从高斯解码器中产生模糊的样本.你真正想要的是一个训练目标, (a) 只有一个稳定的损失 (没有杆点,没有最小量), (b) 只有一个低边界.`log p(x)`(所以你有可能性),和 (c) 与SOTA质量相匹配的样本.

> 你想要的`p_data(x)`                                                                                                                                                                                                                                                              `log p(x)`样本质量匹配SOTA──

定义一个马科夫链.`q(x_t | x_{t-1})`逐渐增加了高斯噪音,并引发了反向链.`p_θ(x_{t-1} | x_t)`霍,贾因,阿贝尔 (2020) 表明损失可以简化为一行 预测噪音 并清理数学.在2020年,这是一个好奇心.在2021年,它生产了最先进的样本.在2022年,它成为稳定分散.在2026年,它是基板.

> 索尔-迪克斯斯坦 (2015) 给出了理论答案:定义逐步增加噪音的马尔可夫链,训练反向链去噪音.

> **【中文解读】**转向过程从纯噪音开始逐步到噪音,恢复到真实的数据. 损失函数简化为"预测噪音".

> **【拓展：从 DDPM 到实用扩散模型】**根据"中国"的统计数据,在中国的数据库中,有了大量的数据,但在中国的数据库中,数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据库的数据量为数量.

## 概念的核心概念

![DDPM: forward noise, reverse denoise](../assets/ddpm.svg)

**Forward process `q`.**加入高斯噪音`T`关闭形式是数学易于处理的原因是累积步骤也是高斯式的:

> **前向过程 `q`。**在`T`关闭式解答数学可处理的原因是积累式步骤也是高的:

```
q(x_t | x_0) = N( sqrt(α̅_t) · x_0,  (1 - α̅_t) · I )
```

在哪里`α̅_t = ∏_{s=1..t} (1 - β_s)`时间表`β_t`选择`β_t`通过T=1000步骤从1e-4到0.02直线,`x_T`平均值`N(0, I)`现在,我们要去.

> 其中`α̅_t = ∏_{s=1..t} (1 - β_s)`将`β_t`从1e-4到0.02 线性排列 T=1000步,`x_T`接近`N(0, I)`,我知道.

**Reverse process `p_θ`.**学习一个神经网络`ε_θ(x_t, t)`由于声增加,`x_t`标签:

> **反向过程 `p_θ`。**学习一个神经网络`ε_θ(x_t, t)`预测添加的噪音.`x_t`为了:

```
x_{t-1} = (1 / sqrt(α_t)) · ( x_t - (β_t / sqrt(1 - α̅_t)) · ε_θ(x_t, t) )  +  σ_t · z
```

在哪里`σ_t`是否是`sqrt(β_t)`虽然这个表达式很丑,但它只是代数,`x_{t-1}`由于后部`q(x_{t-1} | x_t, x_0)`替代`x_0`预测噪音预测的情况.

> 其中`σ_t`是 `sqrt(β_t)`演示看起来很复杂,但只是一个数量给定后验.`q(x_{t-1} | x_t, x_0)`求解`x_{t-1}`,我知道.

**Training loss.**

```
L_simple = E_{x_0, t, ε} [ || ε - ε_θ( sqrt(α̅_t) · x_0 + sqrt(1 - α̅_t) · ε,  t ) ||² ]
```

样本`x_0`从数据中,选择一个随机的`t`样本`ε ~ N(0, I)`计算噪音`x_t`通过闭式形式,然后退出噪音. 一次输,没有最小值,没有KL,没有重设.

> 从数据采集中`x_0`随机选择`t`采样`ε ~ N(0, I)`通过一个关闭的计算含噪声`x_t`没有最小值,没有KL,没有重量参数化技巧.

**Sampling.**开始`x_T ~ N(0, I)`复制反向步骤`t = T`为了`1`完成了.

> **采样。**从`x_T ~ N(0, I)`开始,从`t = T`到了`1`代反向步骤――完成――

## 为什么它有效?

只有三个直觉:

> 现在,我知道.

1. **Denoising is easy; generating is hard.**在`t=T`网络必须解决一个微不足道的问题.`t=0`网络只需要清理几个像素.`t`网络的度是相同的,从每个噪音水平流动的.
   **去噪容易，生成难。**在`t=T`时,数据是纯噪音网络只需要解决简单的问题.`t=0`时,网络只需要清理少量像素.

2. **Score matching in disguise.**讯 (2011) 证明,预测噪音与估计等等.`∇_x log q(x_t | x_0)`逆SDE使用这个分数来走上密度梯度,向高概率区域进行指导的随机走路.
   **伪装的分数匹配。**预测噪音等价值的估计分数函数`∇_x log q(x_t | x_0)`△反向SDE利用这个分数沿密度梯度上升.

3. **The ELBO reduces to simple MSE.**随着DDPM的参数化,这些KL术语简化为MSE在噪音预测上,具有特定的系数;Ho降低了系数 (称之为"简单"损失) 和质量 *改善*.
   **ELBO 简化为简单 MSE。**完整的变分下界 每个时间步骤都有 KL 项.

## 建立它,实现它.
```figure
diffusion-denoise
```

## 建立它

`code/main.py`网络是一个小的 MLP,它需要一个`(x_t, t)`训练是单线损失. 样本测试反转链.

> `code/main.py`实现一个维 DDPM──数据是双峰混合──"网络"是一个微型的MLP,接收`(x_t, t)`输出预测噪音――训练就是那一行损失――采样代反向链――

### 步骤1:前进时间表 (封闭表格)

```python
betas = [1e-4 + (0.02 - 1e-4) * t / (T - 1) for t in range(T)]
alphas = [1 - b for b in betas]
alpha_bars = []
cum = 1.0
for a in alphas:
    cum *= a
    alpha_bars.append(cum)
```

### 步骤2: 样本`x_t`在一个射击中

```python
def forward_sample(x0, t, alpha_bars, rng):
    a_bar = alpha_bars[t]
    eps = rng.gauss(0, 1)
    x_t = math.sqrt(a_bar) * x0 + math.sqrt(1 - a_bar) * eps
    return x_t, eps
```

### 步骤3:一个训练步骤

```python
def train_step(x0, model, alpha_bars, rng):
    t = rng.randrange(T)
    x_t, eps = forward_sample(x0, t, alpha_bars, rng)
    eps_hat = model_forward(model, x_t, t)
    loss = (eps - eps_hat) ** 2
    return loss, gradient_step(model, ...)
```

### 步骤4:反向采样

```python
def sample(model, alpha_bars, T, rng):
    x = rng.gauss(0, 1)
    for t in range(T - 1, -1, -1):
        eps_hat = model_forward(model, x, t)
        beta_t = 1 - alphas[t]
        x = (x - beta_t / math.sqrt(1 - alpha_bars[t]) * eps_hat) / math.sqrt(alphas[t])
        if t > 0:
            x += math.sqrt(beta_t) * rng.gauss(0, 1)
    return x
```

对于一个40个时间步骤和24个单位的MLP的1D问题,这在200个时代中学习了两种模式的混合物.

> 对于40个时间步骤和24个单元MLP的一维问题,约有200轮即可学会双峰混合.

## 时间定制.

网络需要知道它正在指定的时间步骤.

> 网络需要知道它在哪个时间里进行噪音.

- **Sinusoidal embedding.**像变压器定位编码.`embed(t) = [sin(t/ω_0), cos(t/ω_0), sin(t/ω_1), ...]`通过一个MLP,播出到网络.
  **正弦嵌入。**类似变压器 位置编码――
- **Film / group-norm conditioning.**项目嵌入每个区块的每道尺度/偏差 (FiLM).
  **FiLM / 组归一化条件化。**插入投影为每通道缩放/偏置.

我们的玩具代码使用了突状 → 缩写.

> 我们的玩具代码用正弦→拼接──制作U-Net用FiLM──

## 陷常见的陷

- **Schedule matters a lot.**线性`β`根据DDPM默认的规则,但Cosine时间表 (尼乔尔和达里瓦尔,2021) 为相同的计算提供了更好的FID.
  **调度很重要。**线性 `β`是DDPM默认但余弦调度在相同的计算量下 FID更好.
- **Timestep embedding is fragile.**通过原始`t`像浮动机一样,它适用于玩具1-D,但对于图像来说是失败的;总是使用适当的嵌入.
  **时间步嵌入脆弱。**原始 `t`浮点数在玩具1D可用但图像不行.
- **V-prediction vs ε-prediction.**对于狭窄的制度 (非常小或非常大),`ε`信号噪音差.V预测 (`v = α·ε - σ·x`) 较稳定;SDXL,SD3和Flux使用它.
  **V 预测 vs ε 预测。**在极端时间步骤,V 预测更稳定;SDXL、SD3、Flux 使用它.
- **Classifier-free guidance.**在推断时,计算条件和无条件的两个`ε`现在`ε_cfg = (1 + w) · ε_cond - w · ε_uncond`随着`w ≈ 3-7`课第8课中包括.
  **无分类器引导。**推理时计算条件和无条件预测的差值.
- **1000 steps is a lot.**生产使用DDIM (20-50步骤),DPM-Solver (10-20步骤),或蒸 (1-4步骤).
  **1000 步太多了。**生产用DDIM(20-50步)、DPM-Solver(10-20步) 或蒸(1-4步)。

## 用它实现框架

| Role / 角色 | Typical stack in 2026 / 2026 典型技术栈 |
|------|-----------------------|
| Image pixel-space diffusion (small, toy) / 像素空间扩散 | DDPM + U-Net |
| Image latent diffusion / 潜在扩散 | VAE encoder + U-Net or DiT (Lesson 07) |
| Video latent diffusion / 视频潜在扩散 | Spatiotemporal DiT (Sora, Veo, WAN) |
| Audio latent diffusion / 音频潜在扩散 | Encodec + diffusion transformer |
| Science (molecules, proteins, physics) / 科学 | Equivariant diffusion (EDM, RFdiffusion, AlphaFold3) |

流量匹配 (课3) 是2024-2026年通常以推理速度赢得相同质量的竞争者.

> 扩散是通用生成骨干;;流量匹配第13课) 是2024-2026年的竞争对手,通常在相同质量下推理速度更快.

## 运送它.

保存`outputs/skill-diffusion-trainer.md`技能采用数据集+计算预算和输出:时间表 (线性/可西因/西格莫ид),预测目标 (ε/v/x),步骤数量,指导尺度,样本组和评估协议.

> 保存`outputs/skill-diffusion-trainer.md`◎ 技能 接收数据集+计算预算,输出调度,预测目标,步数,引导缩放,采样器和评估协议.

## 练习题

1. **Easy / 简单.**改变T从40到10`code/main.py`样品质量 (输出视觉历史图) 如何降低?
   如何将T从40变为10?样本质量如何退化?双峰结构在哪个T值塌?
2. **Medium / 中等.**转换从 ε 预测到 v 预测.再推出反向步骤.
   从 ε 预测切换到 v 预测――重新推导反向步骤――比较最终样本质量――
3. **Hard / 困难.**添加无类别指导. 类标签上的条件 `c ∈ {0, 1}`培训期间,并在采样时间使用时,将其降低10%的时间`ε = (1+w)·ε_cond - w·ε_uncond`测量条件模式的击中率`w = 0, 1, 3, 7`现在,我们要去.
   添加无分类器引导――测量`w = 0, 1, 3, 7`时的条件模式命中率

## 关键词 快速查找表

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Forward process | "Adding noise" / "加噪" | Fixed Markov chain `q(x_t \| x_{t-1})` that destroys the data. / 破坏数据的固定马尔可夫链。 |
| Reverse process | "Denoising" / "去噪" | Learned chain `p_θ(x_{t-1} \| x_t)` that reconstructs the data. / 重建数据的学习链。 |
| β schedule | "The noise ladder" / "噪声阶梯" | Per-step variance; linear, cosine, or sigmoid. / 每步方差；线性、余弦或 S 形。 |
| α̅ | "Alpha bar" | Cumulative product `∏(1 - β)`; gives closed-form `x_t` from `x_0`. / 累积乘积，给出闭式 `x_t`。 |
| Simple loss | "MSE on noise" / "噪声 MSE" | `\|\|ε - ε_θ(x_t, t)\|\|²`; all variational derivations collapse to this. / 所有变分推导最终坍塌为此。 |
| ε-prediction | "Predict noise" / "预测噪声" | Output is the noise added; standard DDPM. / 输出是添加的噪声。 |
| V-prediction | "Predict velocity" / "预测速度" | Output is `α·ε - σ·x`; better conditioning across t. / 跨时间步条件化更好。 |
| DDPM | "The paper" / "那篇论文" | Ho et al. 2020; linear β, 1000 steps, U-Net. |
| DDIM | "Deterministic sampler" / "确定性采样器" | Non-Markov sampler, 20-50 steps, same training objective. / 非马尔可夫采样器。 |
| Classifier-free guidance | "CFG" | Mix conditional and unconditional noise predictions to amplify conditioning. / 混合条件和无条件预测以放大条件化。 |

## 产品注释:扩散推理是步数问题

根据DDPM的文件,T=1000反向步骤.在生产中没有人运行.每一个真正的推断堆都选择了三个策略中的一个,每个都清洁地绘制了生产框架的"延迟来自哪里":

> 通过使用T=1000反向步骤.

1. **Faster sampler, same model.**通过换反循环,训练有素的 `ε_θ`减速延迟20-50倍.
   **更快的采样器，相同模型。**插即用替换反向循环,降低延迟20-50倍.
2. **Distillation.**训练学生以更少的步骤与教师匹配:渐进式蒸 (2 → 1),一致性模型 (任意 → 1-4),LCM,SDXL-Turbo,SD3-Turbo. 降低延迟另一个 5-10 ×,需要重新训练.
   **蒸馏。**训练学生模型在更少步骤的匹配教师――再降迟 5-10 倍,需要重训――
3. **Caching and compilation.** `torch.compile(unet, mode="reduce-overhead")`光RT-LLM的扩散后端,`xformers`减速速度为2x,堆积1和2
   **缓存和编译。**火器.组件、光RT、xformers、bf16──降低每步延迟约2倍──

对于生产传播服务器,预算对话与生产文献描述的LLC相同:延迟是`num_steps × step_cost + VAE_decode`通过率是`batch_size × (num_steps × step_cost)^-1`图像生成是从用户的角度来看"一次性"的,因此,TTFT是小的 (一步);TPOT相当于全响应时间.

> 生产扩散服务器的预算对话与LLM 相同:延迟 = `num_steps × step_cost + VAE_decode`△TTFT 很小的步骤;TPOT 等价物是完整的响应时间──

## 继续阅读 继续阅读

- [Sohl-Dickstein et al. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics](https://arxiv.org/abs/1503.03585)                               
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)    
- [Song, Meng, Ermon (2021). Denoising Diffusion Implicit Models](https://arxiv.org/abs/2010.02502) DDIM,少了步骤.
- [Nichol & Dhariwal (2021). Improved DDPM](https://arxiv.org/abs/2102.09672)代数时间表,学习变异.
- [Dhariwal & Nichol (2021). Diffusion Models Beat GANs on Image Synthesis](https://arxiv.org/abs/2105.05233)分类指导
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598)   
- [Karras et al. (2022). Elucidating the Design Space of Diffusion-Based Generative Models (EDM)](https://arxiv.org/abs/2206.00364)统一的标记,最清洁的食谱.
