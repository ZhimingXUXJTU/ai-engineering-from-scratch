#  发电机与分辨器

> 2014年,Goodfellow的技巧是完全跳过密度.两个网络.一个制造假冒.一个抓住他们.他们战斗直到假冒是无法区分的真实.它不应该工作.它经常不会.当它做的时候,样本仍然是最尖的文学中,对于狭窄域.

> **【中文解读】**善良的朋友2014年的技巧是完全跳过密度估计.两个网络:一个假,一个抓假,彼此博直到假样本与真样本不可分.理论上不应该工作,实践中常常不工作,但一旦成功,在狭域生成上仍然是文献中最利的结果.

> **【拓展：GAN 的遗产】**虽然扩散模型在2022年后成为主流,但GAN的反抗训练思想仍然被用来提升其他模型质量.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 3 · 08 (Optimizers / 优化器), Phase 8 · 02 (VAE)
**Time:** ~75 minutes

## 问题 问题引入

由于它们的MSE解码器损失是*平均*图像的最佳,而许多可信数字的平均值是模糊的数字.你想要一个损失,以奖励*可信性*,而不是像素智能接近任何一个目标.可信性没有封闭形式.你必须学习它.

> 由于MSE 解码器损失对*平均值*图像是贝叶斯最优的而许多合理数字的平均值是一个模糊的数字.你需要一个奖励*逼真性*的损失,而不是与任何目标的像素级接近.

善良的想法:训练一个分类器`D(x)`让一个发电机训练一个发电机.`G(z)`愚蠢`D`输出信号`G`是什么都不一样`D`现在的信号是:`G`如果两个网络融合,`G`没有写下数据的分布.`log p(x)`现在,我们要去.

> 善良的朋友的想法:训练一个分类器`D(x)`区分真假图像,训练一个生成器`G(z)`欺骗`D`,我知道.`G`损失信号是`D`当前认为"看起来真实"的东西.`G`改进和更新追逐一个移动目标.`G`没有需要写出来的数据分布.`log p(x)`,我知道.

这是一场对抗训练.数学是一场最小级游戏:

```
min_G max_D  E_real[log D(x)] + E_fake[log(1 - D(G(z)))]
```

2026年,GAN不再是SOTA生成器 (扩散和流量匹配吞了那冠).但StyleGAN 2/3仍然是有史以来出货的最尖的面型,GAN歧视器被用于扩散训练中的感知损失,而对抗训练支持快速的1步蒸 (SDXL-Turbo,SD3-Turbo,LCM) 允许您出货实时扩散.

> 2026年,GAN 不再是最先进的生成器.但StyleGAN 2/3 仍然是历史上最利的人脸模型.GAN 判定器被用于扩散训练中*感觉损失*,对抗训练驱动快速1步蒸 (SDXL-Turbo、SD3-Turbo、LCM) ⋅

> **【中文解读】**甘南的核心思想:不建模密度,通过对抗训练学习生成――生成器 G(z) 尝试生成逼真图像,判别器 D(x) 尝试区分真假――两者在最小的博中共同进化――VAE的MSE损失导致模糊――因为它最优化的是平均值图像),而甘南的对抗损失奖励"逼真性"――GAN 生成速度快,但训练不稳定――

> **【拓展：GAN 在扩散模型蒸馏中的新角色】**虽然GAN 不再是主流的生成方法,但对抗训练思想在扩散模型蒸中发新生.SDXL-Turbo、SD3-Turbo、LCM等快速模型使用对抗损失将多步扩散蒸为1-4步,实现实时生成.

## 概念的核心概念

![GAN training: generator and discriminator in minimax](../assets/gan.svg)

**Generator `G(z)`.**绘制一个噪音向量`z ~ N(0, I)`给一个样本`x̂`电脑系统的电脑系统.

> **生成器 `G(z)`。**将噪音量`z ~ N(0, I)`映射为样本`x̂`△一个解码器形状的网络全连接或转置卷积)

**Discriminator `D(x)`.**绘制一个样本的échar概率 (或分数).真 → 1,假 → 0.

> **判别器 `D(x)`。**将样本映射为标量概率 (或分数) 〔真实 → 1,伪造 → 0〕

**Loss.**两次交替更新:

- **Train `D`:** `loss_D = -[ log D(x) + log(1 - D(G(z))) ]`双向交叉值在真=1,假=0.
- **Train `G`:** `loss_G = -log D(G(z))`这是Goodfellow使用的 *不和的*形式 (原始`log(1 - D(G(z)))`化和杀死梯度时`D`对于其他国家,

> **损失。**两个交替更新:训练 D 用二元交叉(真实=1,伪造=0);训练 G 用非和形式 `-log D(G(z))`(原始形式在 D 自信时梯度消失)

**Training loop.**一步走`D`现在,我们要做一个好事.`G`复制.

> **训练循环。**一步D,一步G,交替进行.

**Why it works.**如果`G`非常合适`p_data`现在`D`没有机会, 没有机会, 没有机会.`G`没有任何梯度,平衡.

> **为什么有效。**如果`G`完美匹配`p_data`则`D`无法比随机猜测更好,处处输出0.5;`G`没有再获得梯度.

**Why it breaks.**模式崩 (`G`找到一个模式`D`它们的度变化,`D`学习得太快,`log D`培训不稳定性 (学习率,批量,任何东西).

> **为什么会失败。**模式塌`G`找到`D`无法分类一种模式并永远产生它) 梯度消失(`D`学得太快导致`log D`和) 、训练不稳定(学习率、批大小等)

## 让GAN工作的变体

| Year / 年份 | Innovation / 创新 | Fix / 解决的问题 |
|------|------------|-----|
| 2015 | DCGAN | Conv/deconv, batch norm, LeakyReLU — the first stable architecture. / 首个稳定架构。 |
| 2017 | WGAN, WGAN-GP | Replace BCE with Wasserstein distance + gradient penalty. Fixes vanishing gradient. / 用 Wasserstein 距离替换 BCE，修复梯度消失。 |
| 2017 | Spectral normalization | Lipschitz-bound the discriminator. Still used in 2026 discriminators. / 约束判别器 Lipschitz 常数。 |
| 2018 | Progressive GAN | Train low-res first, add layers. First megapixel results. / 先训练低分辨率，再加层。 |
| 2019 | StyleGAN / StyleGAN2 | Mapping network + adaptive instance norm. State of the art for fixed-domain photorealism. / 映射网络 + AdaIN。 |
| 2021 | StyleGAN3 | Alias-free, translation-equivariant — still the face gold standard in 2026. / 无混叠，平移等变。 |
| 2022 | StyleGAN-XL | Conditional, class-aware, larger scale. / 条件生成，类别感知。 |
| 2024 | R3GAN | Rebrands with stronger regularization; works on 1024² without tricks. / 更强的正则化。 |

## 建立它,实现它.
```figure
gan-minimax
```

## 建立它

`code/main.py`导电和分辨器是单层隐藏MLP.我们手动执行前进,后退和最小x循环.目标是看到两个关键故障模式 (模式崩 +消失梯度) 发生.

> `code/main.py`在一维数据上训练一个微型GAN:双峰高斯混合――生成器和判定器是单隐层MLP――我们手动实现前向、反向和最小循环――目标是看到两种关键失败模式的发生过程――模式塌 + 梯度消失).

### 步骤1:不和损失

瓦尼莉的好友失去了`log(1 - D(G(z)))`在这个时候,G的梯度基本上是零  G不能改善.非和形式`-log D(G(z))`它们在D自信时爆炸,给G一个强烈的信号.

> 原始善良的朋友 损失`log(1 - D(G(z)))`在 D 高置信度地将 G 的伪造分类为假时趋近 0,此时 G 的梯度基本为零――非和形式`-log D(G(z))`们在们的眼前,

```python
def g_loss(d_fake):
    # maximize log D(G(z))  <=>  minimize -log D(G(z))
    return -sum(math.log(max(p, 1e-8)) for p in d_fake) / len(d_fake)
```

### 步骤2:每一个生成器步骤的一个歧视步骤

```python
for step in range(steps):
    # train D
    real_batch = sample_real(batch_size)
    fake_batch = [G(z) for z in sample_noise(batch_size)]
    update_D(real_batch, fake_batch)

    # train G
    fake_batch = [G(z) for z in sample_noise(batch_size)]  # fresh fakes
    update_G(fake_batch)
```

对于G来说,新鲜的假冒,否则梯度是陈旧的.

> 为了生出新的假样本,否则梯度过时.

### 步骤3: 警模式崩

```python
if step % 200 == 0:
    samples = [G(z) for z in sample_noise(500)]
    mode_a = sum(1 for s in samples if s < 0)
    mode_b = 500 - mode_a
    if min(mode_a, mode_b) < 50:
        print("  [!] mode collapse: one mode is starved")
```

法症状:两个真正的模式中的一个停止生成. 歧视者停止纠正它,因为它从来没有被视为假的.

> 典型症状:两个真实模式之一不再被生成.

## 陷常见的陷

- **Discriminator too strong.**如果D达到95%以上的准确度,G就死了.
  **判别器太强。**如果D的准确率超过95%,G就死了――
- **Generator memorizes a mode.**加入噪音到D输入,使用微批量区分器层,或切换到WGAN-GP.
  **生成器记住了一种模式。**给D输入添加噪音,使用小批量判定器层,或切换到WGAN-GP。
- **Batch norm leaking statistics.**实际批量+假批量通过同一BN层流动混合他们的统计数据.
  **批归一化泄漏统计量。**真实批次和伪造批次通过同一BN层混合统计量――改用例归结或谱归结――
- **Inception-score gaming.**在低样本数量时,FID和IS有噪音.在 eval时使用≥10k样本.
  **Inception Score 作弊。**低样本量时噪声大――评估时使用 ≥10k样本――
- **One-shot sampling is a lie for conditional tasks.**你仍然需要CFG尺度,切割技巧,再采样才能得到可用的输出.
  **条件任务中"单次采样"是个谎言。**您仍然需要 CFG 缩放,截断技巧和重采样才能获得可用的输出.

## 用它实现框架

根据"2026年"的GAN堆:

> 2026 年 技术:

| Situation / 场景 | Pick / 选择 |
|-----------|------|
| Photoreal human faces, fixed pose / 照片级人脸，固定姿势 | StyleGAN3 (sharpest, smallest) |
| Anime / stylized faces / 动漫/风格化人脸 | StyleGAN-XL or Stable Diffusion LoRA |
| Image-to-image translation / 图像翻译 | Pix2Pix / CycleGAN (Phase 8 · 04) or ControlNet (Phase 8 · 08) |
| Fast 1-step text-to-image / 快速单步文生图 | Adversarial distillation of diffusion (SDXL-Turbo, SD3-Turbo) |
| Perceptual loss inside a diffusion trainer / 扩散训练中的感知损失 | Small GAN discriminator on image crops |
| Anything multi-modal, open-ended / 多模态开放域 | Don't — use diffusion or flow matching / 不要用 GAN——用扩散或 Flow Matching |

网页的数据源是很简单的,但很窄的.一旦您的域名打开了照片,任意的文本提示,视频转向扩散.

> 利但狭域──一旦领域开放照片、任意文本提示、视频就转换为扩散模型──对抗技巧作为组件存活感知损失、蒸),而不是独立生成器──

## 运送它.

保存`outputs/skill-gan-debugger.md`技能采用一个失败的GAN运行 (损失曲线,样本格格,数据集大小) 并输出了排列可能原因列表,一线修复和重复运行协议.

> 保存`outputs/skill-gan-debugger.md`△ 技能 接收失败的GAN 运行(损失曲线、样本网格、数据集大小),输出可能原因排列表、一行修复和重跑方案──

## 练习题

1. **Easy / 简单.**跑步`code/main.py`根据股票设置.`D_LR = 5 * G_LR`几快G的损失会崩到恒定?
   用默认设置运行`code/main.py`然后设置`D_LR = 5 * G_LR`重跑.G的损失多快塌为常数?
2. **Medium / 中等.**取代Goodfellow BCE损失的WGAN损失: `loss_D = E[D(fake)] - E[D(real)]`现在`loss_G = -E[D(fake)]`子 D 的重量到`[-0.01, 0.01]`训练是否更稳定?
   为了换取GAN损失,切断D的权重.`[-0.01, 0.01]`训练更稳定吗?
3. **Hard / 困难.**扩展1D示例到2D数据 (环上混合8个高西安).追踪发电机在1k,5k,10k步骤中捕获了8种模式中的多少种.实施微批次差异和重新测量.
   追踪生成器在1k,5k,10k步骤捕获了多少模式.实现小批量判别并重新测量.

## 关键词 快速查找表

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Generator | "G" | Noise-to-sample network, `G: z → x̂`. / 噪声到样本的网络。 |
| Discriminator | "D" | Classifier `D: x → [0, 1]`, real vs fake. / 真假分类器。 |
| Minimax | "The game" / "博弈" | `min_G max_D` of a joint objective. / 联合目标的极小极大。 |
| Non-saturating loss | "The fix" / "修复" | Use `-log D(G(z))` for G instead of `log(1 - D(G(z)))`. / 用非饱和形式替代原始损失。 |
| Mode collapse | "G memorized one thing" / "G 记住了一种" | Generator produces few distinct outputs despite diverse data. / 生成器产生少量不同输出。 |
| WGAN | "Wasserstein" | Replace BCE with Earth-Mover distance + gradient penalty; smoother gradient. / 用 Wasserstein 距离替代 BCE。 |
| Spectral norm | "Lipschitz trick" / "Lipschitz 技巧" | Constrain D's weight norms to bound its slope; stabilizes training. / 约束 D 的权重范数以稳定训练。 |
| StyleGAN | "The one that works" / "能用的那个" | Mapping network + AdaIN; best-in-class for faces, still in 2026. / 映射网络 + AdaIN，人脸最佳。 |

## 产品注释: 一次推断是GAN的持久优势

在生产-推理文献词汇中,一个GAN有:

> 由于这种情况,我们可以说,在生产推理术语中,

- **No prefill, no decode stages.**一个单身的`G(z)`预测时间:
  **无 prefill，无 decode 阶段。**单次`G(z)`前向传播──TTFT ≈ 总延迟──
- **No KV-cache pressure.**只有重量,批量量由激活内存限制,而不是缓存.
  **无 KV 缓存压力。**唯一的状态是权重. 批量大小仅限于激活内存而不是缓存.
- **Trivial continuous batching.**由于每个请求都采用相同的固定FLOP,因此在服务器的目标占用量上静态批量通常是最佳的.
  **简单的连续批处理。**每个请求都消耗相同的FLOP,静态批量通常最优.

这就是为什么GAN蒸 (SDXL-Turbo,SD3-Turbo,ADD,LCM) 是2026年快速文字到图像的主导技术:它将20-50步的扩散管道分解成1-4步GAN式前进通道,同时保持了扩散基的分布.对抗损失作为将慢发电器转化为快速发电器的训练时间.

> 这就是为什么GAN蒸(SDXL-Turbo、SD3-Turbo、LCM) 是2026年快速文生图的主导技术:它将在2050步扩散流水线压缩为1-4次GAN风格的前向传播,同时保持扩散模型的分布.

## 继续阅读 继续阅读

- [Goodfellow et al. (2014). Generative Adversarial Nets](https://arxiv.org/abs/1406.2661)原始的GAN纸.
- [Radford et al. (2015). Unsupervised Representation Learning with DCGAN](https://arxiv.org/abs/1511.06434)第一种稳定的建筑.
- [Arjovsky, Chintala, Bottou (2017). Wasserstein GAN](https://arxiv.org/abs/1701.07875)  
- [Miyato et al. (2018). Spectral Normalization for GANs](https://arxiv.org/abs/1802.05957) SN
- [Karras et al. (2020). Analyzing and Improving the Image Quality of StyleGAN](https://arxiv.org/abs/1912.04958)    
- [Karras et al. (2021). Alias-Free Generative Adversarial Networks](https://arxiv.org/abs/2106.12423)    
- [Sauer et al. (2023). Adversarial Diffusion Distillation](https://arxiv.org/abs/2311.17042)SDXL-Turbo.
