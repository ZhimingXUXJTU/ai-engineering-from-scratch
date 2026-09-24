# 条件GAN与Pix2Pix

> 2014-2017年第一场大解锁是控制GAN的产品. 添加标签,图像或句子.Pix2Pix完成了图像版本,并且在狭窄的图像到图像任务上仍然击败了每个通用文本到图像模型.

> **【中文解读】**2014-2017年第一大突破是控制GAN 生成什么:附加标签、图像或文本──Pix2Pix制作了图像版本,至今仍在狭域图像翻译任务中胜过通用文本生成图像模型──

> **【拓展：Pix2Pix 的应用】**皮克斯2皮克斯创建了"图像到图像翻译"的范式:素描→照片、白天→夜晚、线稿→彩色图──这个范式后来被控制网继承和发展──

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 03 (GANs), Phase 4 · 06 (U-Net), Phase 3 · 07 (CNNs / 卷积神经网络)
**Time:** ~75 minutes

## 问题 问题引入

无条件的GAN采样任意的面孔. 用于演示,无用在生产中.你想要: *将草图映射到照片中*, *将地图映射到空中照片中*, *日间场景映射到夜间*, *将灰色图像染色.在所有这些中,你得到一个输入图像`x`必须输出`y`许多可行的方法`y`个性`x`平均平方错误会使它们平坦成.

> 无条件 GAN 采样任意人脸――适合演示,不适合生产――你想要的是:*将素描映射为照片*、*将地图映射为航拍图*、*将白天映射为夜晚*、*给灰度图上色*──在所有这些场景中,给定输入图像`x`必须输出具有意义的应对关系`y`每个人都`x`有很多合理的方法.`y`△平均差异将它们压成一团糊,而对抗损失不会,因为"看起来真实"是利的.

条件GAN (Mirza & Osindero, 2014) 增加了一个条件`c`作为两者都的输入`G`其他`D`皮克斯2皮克斯 (伊索拉等人,2017) 专业化了这一点:条件是一个完整的输入图像,生成器是U-Net,歧视器是一个基于补丁的*分类器 (PatchGAN),损失是对立的+L1.该配方甚至在2026年也超过了从零开始的文本到图像模型,因为它是训练在 *对数据* 你有了你需要的信号.

> 条件 ️2014年`G`和 `D`的输入中添加条件`c`△Pix2Pix(2017) 专为此:条件是完整输入图像,生成器是U-Net,判别器是PatchGAN,损失 =对抗 + L1――这个方案在狭域图像翻译任务上甚至在2026年仍然优于从头上训练的文生图像模型,因为它在*配对数据*上训练你恰好有所需的信号――

> **【中文解读】**条件 GAN 的核心改进:给生成器和判别器都添加条件输入 c。Pix2Pix 的条件是完整输入图像,生成器使用U-Net(保留空间细节),判别器使用PatchGAN(对局部图像块分类) ・损失 = 对抗损失 + L1 损失――这种配对数据训练方式在狭域图像翻译任务中至今仍然优于通用文本生成图像模型――

> **【拓展：从 Pix2Pix 到 ControlNet 的演进】**皮克斯2Pix的"图像条件生成"思想被控制网 (ControlNet) 继承和发展. 控制网将控制条件 (边缘,深度图,姿态等) 注入预训练的稳定扩散模型,实现了更普遍的可控生成. 从皮克斯2Pix到CycleGAN再到控制网,这是一个清晰的"可控生成"技术发展路径.

## 概念的核心概念

![Pix2Pix: U-Net generator, PatchGAN discriminator](../assets/pix2pix.svg)

**Conditional G.** `G(x, z) → y`在Pix2Pix中,`z`在G内出现 (没有输入噪音 发现明确的噪音被忽略).

> **条件生成器 G。** `G(x, z) → y`在Pix2Pix中,`z`是 G 内部的落 (无输入噪音)  发现显式噪音会被忽略) 

**Conditional D.** `D(x, y) → [0, 1]`输入是*对* (条件,输出).这是关键的区别:D必须判断是否`y`符合`x`不仅仅是`y`看起来是真的.

> **条件判别器 D。** `D(x, y) → [0, 1]`◎输入是*配对*(条件,输出) ・关键区别:D 必须判断`y`是否与`x`一致,不仅仅是`y`是否看起来真实.

**U-Net generator.**编码器-解码器,通过瓶跳转连接.输入和输出共享低层次结构 (边缘,外形).没有跳转,高频细节消失.

> **U-Net 生成器。**带有跳跃连接编码器-解码器――对于输入输出共享低级结构的任务至关重要――没有跳跃连接,高频细节会消失――

**PatchGAN discriminator.**结果是: 结果是:`N×N`平均值.这是一个马科夫随机场假设:现实主义是本地.训练速度更快,参数更少,输出更敏捷.

> **PatchGAN 判别器。**输出`N×N`网格而不是单一真/假分数,每个单元判断约70×70 像素的感受野──这是马尔可夫随机场假设:真感是局部的──训练更快,参数更少,输出更利──

**Loss.**

```
loss_G = -log D(x, G(x)) + λ · ||y - G(x)||_1
loss_D = -log D(x, y) - log (1 - D(x, G(x)))
```

术语L1稳定了训练,并将G推向已知目标.L1比L2 (中介,而不是中介) 提供了更尖的边缘.`λ = 100`现在,我们在使用Pix2Pix的默认版本.

> 稳定训练并推动G 趋向已知目标──L1比L2 产生更利的边缘(中位数对平均值)──`λ = 100`是Pix2Pix的默认值.

##  没有对子的时候, 没有配对数据时

Pix2Pix需要配对`(x, y)`循环GAN (Zhu等人,2017) 通过额外的损失降低了这一要求: *循环一致性损失.`G: X → Y`其他`F: Y → X`训练他们.`F(G(x)) ≈ x`其他`G(F(y)) ≈ y`这让你把马转换为斑马,夏天转换为冬天,没有双双的例子.

> 需要配对`(x, y)`据悉,CycleGAN (CycleGAN) 2017年放弃了这一要求,代价是额外的循环一致性损失.`G: X → Y`和 `F: Y → X`训练使`F(G(x)) ≈ x`和 `G(F(y)) ≈ y`这让你无需配对样本就能把马变成斑马,夏天变成冬天.

2026年,未对成的图像到图像主要通过扩散 (ControlNet,IP-Adapter) 而不是CycleGAN进行,但循环一致性概念几乎在每一个未对成的域调整论文中都存活下来.

> 2026年,非配对图像翻译主要通过扩散模型 (ControlNet、IP-Adapter) 而不是CycleGAN完成,但循环一致性思想几乎存在于每篇非配对域适应论文中.

## 建立它,实现它.
```figure
gx-patchgan
```

## 建立它

`code/main.py`根据1D数据的条件,`c`任务:为给定的类型从条件分布中制造样本.

> `code/main.py`在一维数据上实现一个微型条件 GAN――条件`c`是类别标签(0 或 1)。任务:为给定类别从条件分布中生成样本──

### 步骤1:将条件添加到G和D输入

```python
def G(z, c, params):
    return mlp(concat([z, one_hot(c)]), params)

def D(x, c, params):
    return mlp(concat([x, one_hot(c)]), params)
```

单热编码是最简单的方法.较大的模型使用学习嵌入,FiLM调节或交叉注意.

> 单热编码是最简单的方式.

### 步骤2:火车条件

```python
for step in range(steps):
    x, c = sample_real_conditional()
    noise = sample_noise()
    update_D(x_real=x, x_fake=G(noise, c), c=c)
    update_G(noise, c)
```

发电机必须与给定的条件的实际分布相匹配,而不是边缘分布.

> 生成器必须符合*给定条件*下的真实分布,而不是边际分布.

### 步骤3:验证每个类输出

```python
for c in [0, 1]:
    samples = [G(noise, c) for noise in batch]
    mean_c = mean(samples)
    assert_near(mean_c, real_mean_for_class_c)
```

## 陷常见的陷

- **Condition ignored.**修复:条件D更积极 (早期层,不仅仅是晚期),使用投影歧视器 (Miyato & Koyama 2018).
  **条件被忽略。**修复:更积极地条件化 D,使用投影判定器――
- **L1 weight too low.**开始 λ≈100为Pix2Pix类型的任务.
  **L1 权重太低。**偏移到任意看起来真实输出──Pix2Pix 任务从 λ≈100 开始──
- **L1 weight too high.**部下降,训练稳定.
  **L1 权重太高。**产生模糊输出――训练稳定后逐渐降低――
- **Ground-truth leakage in D.**酸`(x, y)`作为D输入,不仅仅是`y`没有这个D,不能检查一致性.
  **D 中的真值泄漏。**将`(x, y)`拼接为 D 的输入,而不是仅仅`y`,我知道.
- **Mode collapse per class.**每个类都可以独立崩. 进行类条件的多样性检查.
  **每类模式坍塌。**每个类可能独立塌.

## 用它实现框架

2026 图像到图像任务状态:

> 图像到图像任务的状态:2026年:

| Task / 任务 | Best approach / 最佳方案 |
|------|---------------|
| Sketch → photo, same domain, paired data / 素描→照片，配对数据 | Pix2Pix / Pix2PixHD (still fast, still sharp) |
| Sketch → photo, unpaired / 素描→照片，非配对 | ControlNet with a Scribble conditioning model |
| Semantic seg → photo / 语义分割→照片 | SPADE / GauGAN2 or SD + ControlNet-Seg |
| Style transfer / 风格迁移 | Diffusion with IP-Adapter or LoRA; GAN methods are legacy |
| Depth → photo / 深度→照片 | ControlNet-Depth over Stable Diffusion |
| Super-resolution / 超分辨率 | Real-ESRGAN (GAN), ESRGAN-Plus, or SD-Upscale (diffusion) |
| Colorization / 上色 | ColTran, diffusion-based colorizers, or Pix2Pix-color |
| Daytime → nighttime, seasons, weather / 白天→夜晚 | CycleGAN or ControlNet-based |

在 (a) 拥有数千个对式示例时, (b) 任务是狭窄的,可重复的, (c) 需要快速推断时,Pix2Pix仍然是正确的工具.在通用开放域任务上,扩散获胜.

> 2Pix 在以下情况下仍然是正确的工具: (a) 有数千个配对样本, (b) 任务是狭窄的,可重复的, (c) 需要快速推理,

## 运送它.

保存`outputs/skill-img2img-chooser.md`技能采用任务描述,数据可用性 (对与对的,N样本),延迟/质量预算,然后输出:方法 (Pix2Pix,CycleGAN,ControlNet变体,SDXL+IP-Adapter),培训数据要求,推断成本和评估协议 (LPIPS,FID,任务特定).

> 保存`outputs/skill-img2img-chooser.md`技能 接收任务描述,数据可用性和延迟/质量预算,输出方案,训练数据需求,推理成本和评估协议.

## 练习题

1. **Easy / 简单.**修改`code/main.py`确认G仍然将每个类的噪音映射到正确的模式.
   修改`code/main.py`添加第三类. 确认G 仍将每个类的噪音映射到正确的模式.
2. **Medium / 中等.**在1D设置中,取代L1以感知式损失 (例如作为特征提取器的小结D).它是否改变条件分布的敏度?
   在1D设置中,用感觉损失取代L1――它改变了分布的条件度吗?
3. **Hard / 困难.**在1D设置中绘制一个CycleGAN:两个分布,两个发电机,周期损失. 显示它学习在没有对数据之间映射.
   在1D设置中勾勒CycleGAN:两个分布,两个生成器,循环损失.证明它不需要配对数据,就能学习映射.

## 关键词 快速查找表

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Conditional GAN | "GAN with labels" / "带标签的 GAN" | G(z, c), D(x, c). Both networks see the condition. / 两个网络都看到条件。 |
| Pix2Pix | "Image-to-image GAN" / "图像到图像 GAN" | Paired cGAN with U-Net G and PatchGAN D + L1 loss. / 配对 cGAN + U-Net + PatchGAN + L1。 |
| U-Net | "Encoder-decoder with skips" / "带跳跃的编解码器" | Symmetric conv network; skips preserve high-freq. / 对称卷积网络；跳跃连接保留高频。 |
| PatchGAN | "Local-realism classifier" / "局部真实分类器" | D outputs per-patch score instead of global score. / D 输出逐块分数。 |
| CycleGAN | "Unpaired image translation" / "非配对图像翻译" | Two G's + cycle-consistency loss; no paired data. / 两个 G + 循环一致性损失。 |
| SPADE | "GauGAN" | Normalizes intermediate activations with the semantic map; segmentation-to-image. / 用语义图归一化中间激活。 |
| FiLM | "Feature-wise linear modulation" / "特征级线性调制" | Per-feature affine transform from the condition; cheap conditioning. / 廉价的条件化方式。 |

## 产品注释:Pix2Pix作为延迟基线

当你对数据和狭窄任务 (sketch → render,语义地图 →照片,白天 →夜) 时,Pix2Pix的一次性推断比延迟扩散量更高.

> 当你有数据和狭域任务的配对时,Pix2Pix的单次推理在延迟上比扩散模型快速的数量级.

| Path / 方案 | Steps / 步数 | Typical latency at 512² on a single L4 / 典型延迟 |
|------|-------|----------------------------------------|
| Pix2Pix (U-Net forward) | 1 | ~30 ms |
| SD-Inpaint or SD-Img2Img | 20 | ~1.2 s |
| SDXL-Turbo Img2Img | 1-4 | ~0.15-0.35 s |
| ControlNet + SDXL base | 20-30 | ~3-5 s |

二皮克斯在静态批量中获胜于吞吐量 (每个请求都是相同的FLOP).二皮克斯在质量和通用化上获胜.现代游戏通常是为狭窄任务运送Pix2Pix式蒸模型,而尾入输出则为二皮克斯式蒸模型.

> 现代的做法通常是为狭域任务部署Pix2Pix风格蒸模型,为尾部输入提供扩散回退.

## 继续阅读 继续阅读

- [Mirza & Osindero (2014). Conditional Generative Adversarial Nets](https://arxiv.org/abs/1411.1784) 关于该公司的文件.
- [Isola et al. (2017). Image-to-Image Translation with Conditional Adversarial Networks](https://arxiv.org/abs/1611.07004)   
- [Zhu et al. (2017). Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks](https://arxiv.org/abs/1703.10593)     
- [Wang et al. (2018). High-Resolution Image Synthesis with Conditional GANs](https://arxiv.org/abs/1711.11585)    
- [Park et al. (2019). Semantic Image Synthesis with Spatially-Adaptive Normalization](https://arxiv.org/abs/1903.07291)   / 
- [Miyato & Koyama (2018). cGANs with Projection Discriminator](https://arxiv.org/abs/1802.05637)投影D
