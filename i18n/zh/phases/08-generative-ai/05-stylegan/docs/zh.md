# 风格GAN 风格GAN 风格生成对抗网络

> 大多数发电机都会动`z`时刻将它们分开.`z`通过中间`w`接着*注射*`w`通过AdaIN,每一个分辨率级别. 这一变化解开了隐藏的空间,

> **【中文解读】**通过AdaIN在每个分辨率层级注入w,实现了对生成图像不同层次的独立控制.

> **【拓展：StyleGAN 的应用】**风格GAN 广泛用于人脸生成 (thispersondoesnotexist.com) 虚拟人物创建,艺术创作,其风格混合技术可以混合不同的人脸的粗略特征.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 03 (GANs), Phase 4 · 08 (Normalization / 归一化), Phase 3 · 07 (CNNs)
**Time:** ~45 minutes

## 问题 问题引入

一个DCGAN地图`z`问题是: 通过一堆转换的转变来将图像转换成图像.`z`控制一切 姿势,照明,身份,背景  结合在一起.`z`模型不能问"同一个人,不同的姿势",因为表现不以这种方式考虑.

> 通过转置卷积堆将`z`映射为图像──问题是:`z`控制一切姿态,光照,身份,背景,`z`你不能要求模型"同一个人,不同姿态",因为表示没有这样的分解.

卡拉斯等人 (2019,NVIDIA) 提出:停止养`z`直接进入层.`4×4×512`了解一个8层MLP,它将图表绘制`z ∈ Z → w ∈ W`注射`w`在每个分辨率通过 *适应实例正常化* (AdaIN):将每个 conv 特性地图正常化,然后通过相似的投影来扩展和移动`w`增加每层噪音以确保体细节 (皮肤孔孔,头发线).

> 卡拉斯 等人 (NVIDIA) 提出:停止将`z`直接送入卷积层.`4×4×512`张量作为网络输入.学习一个8层MLP将.`z ∈ Z → w ∈ W`通过*自适应实例归纳*(AdaIN) 在每个分辨率注入`w`△添加每层随机噪音用于随机细节孔、发丝)

结果是:`W`图像的位置和形状是相对的. 图像的位置和形状是相对的.`w`对于低分辨率的水平和B图像`w`对于高层,这个开放的编辑,跨域风格化,以及整个"StyleGAN-inversion"的研究线.

> 结果:`W`空间对"高级风格" (姿态,身份) 和"精细风格" (光照,颜色) 有大致正交的轴.`w`根据低分辨率层的图像B`w`这解锁了编辑,跨域风格化和整个"StyleGAN反演"研究方向.

> **【中文解读】**格AN的关键创新:(1) 映射网络 z→w 解开纠的隐藏空间;(2) AdaIN 在每个分辨率层级注入风格低分辨率层控制粗粒度(姿势、身份),高分辨率层控制细粒度(颜色、纹理);(3) 每层随机噪音添加细节(毛孔、发丝) ――风格混合技术可以混合不同的图像的粗粒特征──

> **【拓展：StyleGAN 3 的平移等变性】**通过连续信号处理解这个问题,使生成结果对平移和旋转具有等变性. 这对视频生成和3D应用尤为重要.

## 概念的核心概念

![StyleGAN: mapping network + AdaIN + per-layer noise](../assets/stylegan.svg)

**Mapping network.** `f: Z → W`只有一个8层的MLP.`Z = N(0, I)^512`现在,我们要去.`W`没有被迫成为高斯人,它学习了数据适应的形状.

> **映射网络。** `f: Z → W`八层的MLP.`W`不被强迫高斯它学习数据适应的形状.

**Synthesis network.**从一个学习的常数开始`4×4×512`每个分辨率块:`upsample → conv → AdaIN(w_i) → noise → conv → AdaIN(w_i) → noise`两次决议: 4, 8, 16, 32, 64, 128, 256, 512, 1024.

> **合成网络。**从学习到学习的常数`4×4×512`开始──每个分辨率块:上采样→卷积→AdaIN→噪声→卷积→AdaIN→噪声──分辨率翻倍:4到1024──

**AdaIN.**

```
AdaIN(x, y) = y_scale · (x - mean(x)) / std(x) + y_bias
```

在哪里`y_scale`其他`y_bias`来自于 `w`按特征地图进行正常化,然后重新样式化. "样式"是特征地图的第一和第二级统计数据.

> 其中`y_scale`和 `y_bias`现在`w`模拟投影――逐个特征图归结,然后重新施加风格――"风格"即特征图的一阶段和二阶段统计量――

**Per-layer noise.**单通道高斯噪音加上每个特征地图,以每通道的学习因素进行扩展.

> **每层噪声。**单通道高噪音加到每个特征图,由可学习的单通道因子缩小.

**Truncation trick.**在推断时,样本`z`计算`w = mapping(z)`现在`w' = ŵ + ψ·(w - ŵ)`在哪里`ŵ`是平均值`w`通过许多样本.`ψ < 1`几乎所有的Stylagan演示都使用了`ψ ≈ 0.7`现在,我们要去.

> **截断技巧。**推理时,`w' = ŵ + ψ·(w - ŵ)`在其中`ŵ`是 `w`在多个样本中平均值.`ψ < 1`以多样性换质量――几乎所有的StylagAN演示都使用`ψ ≈ 0.7`,我知道.

## 风格GAN 1 → 2 → 3 风格GAN 版本演进

| Version | Year | Innovation / 创新 |
|---------|------|------------|
| StyleGAN | 2019 | Mapping network + AdaIN + noise + progressive growing. / 映射网络 + AdaIN + 噪声 + 渐进增长。 |
| StyleGAN2 | 2020 | Weight demodulation replaces AdaIN (fixes droplet artifacts); skip/residual architecture; path-length regularization. / 权重解调替代 AdaIN。 |
| StyleGAN3 | 2021 | Alias-free convolution + equivariant kernels; eliminates texture sticking to pixel grid. / 无混叠卷积，消除纹理粘附。 |
| StyleGAN-XL | 2022 | Class-conditional, 1024², ImageNet. / 类别条件，1024²。 |
| R3GAN | 2024 | Rebrands with stronger reg; closes gap to diffusion on FFHQ-1024 with 20x fewer params. / 更强正则化，20 倍更少参数。 |

在2026年,StyleGAN3仍然是 (a) 狭域光现实主义的默认标准,高FPS, (b) 短拍的域调整 (在100图片的新数据集上进行训练,结地图), (c) 基于逆转的编辑 (查看 `w`修改一个真实照片,然后编辑它.`w`对于开放域的文字到图像,它不是工具传播是.

> 2026年 StyleGAN3 仍是以下场景的默认选择: (a) 高FPS 狭域照片级真实感, (b) 少样本域适应, (c) 基于反演的编辑.

## 建立它,实现它.
```figure
gx-stylegan-mapping
```

## 建立它

`code/main.py`实现1D中的玩具"风格-GAN 莱特":一个绘图MLP,一个合成函数,它采用学习的常量向量并通过`w`射的效果是可观的.`w`通过结调节匹配或结结`z`它们可以在发电机的输入中输入.

> `code/main.py`在1D中实现了一个"StyleGAN lite":映射MLP、合成函数和每层噪音――它通过仿射调制注入展示了`w`与将`z`拼接到输入相比效果相当或更好.

### 步骤1:地图网络

```python
def mapping(z, M):
    h = z
    for i in range(num_layers):
        h = leaky_relu(add(matmul(M[f"W{i}"], h), M[f"b{i}"]))
    return h
```

### 步骤2:适应实例正常化

```python
def adain(x, w_scale, w_bias):
    mu = mean(x)
    sd = std(x)
    x_norm = [(xi - mu) / (sd + 1e-8) for xi in x]
    return [w_scale * xi + w_bias for xi in x_norm]
```

性能图的尺度和偏差来自`w`通过线性投影.

> 个性图的缩放和偏移来自`w`线性投影

### 步骤3:每层噪音

```python
def add_noise(x, sigma, rng):
    return [xi + sigma * rng.gauss(0, 1) for xi in x]
```

通过道学习可以.

> 每个通道的西格马是可学习的.

## 陷常见的陷

- **Droplet artifacts.**由于AdaIN 零了平均值,StyleGAN 1 在功能地图中产生了滴.StyleGAN 2 的权重解调通过缩小卷积权重来修复它.
  **液滴伪影。**风格GAN 1 因 AdaIN 归零平均值产生液滴──StyleGAN 2 的权重调调通过缩放卷积权重修复──
- **Texture sticking.**模拟器1和2的纹理遵循像素坐标,而不是对象坐标 (在插曲时可见).StyleGAN3的无形曲线通过窗口的sinc过器来解决这一问题.
  **纹理粘附。**风格GAN 1/2 的纹理跟随像素坐标而不是物体坐标──StyleGAN 3 的无混卷积用窗户 波器修复──
- **Mode coverage.**切割`ψ < 0.7`表面清洁,但来自狭角的样本;使用`ψ = 1.0`如果需要多样性.
  **模式覆盖。**截断`ψ < 0.7`长得很干净,但从狭采样;需要多样性.`ψ = 1.0`,我知道.
- **Inversion is lossy.**转换一个真实照片成`W`结果通常通过优化或编码器 (e4e,ReStyle,HyperStyle) 进行.
  **反演有损。**将真实照片反演到`W`通常通过优化或编码器完成,结果在多次代后会漂移.

## 用它实现框架

| Use case / 用途 | Approach / 方案 |
|----------|----------|
| Photoreal human faces (anime, product, narrow) / 照片级人脸 | StyleGAN3 FFHQ / custom fine-tune |
| Face editing from a photo / 从照片编辑人脸 | e4e inversion + StyleSpace / InterFaceGAN directions |
| Face swap / reenactment / 换脸/重演 | StyleGAN + encoder + blending |
| Avatar pipelines / 虚拟形象 | StyleGAN3 w/ ADA for low-data fine-tune |
| Domain adaptation from a few images / 少样本域适应 | Freeze mapping network, fine-tune synthesis |
| Multi-modal or text-conditioned generation / 多模态生成 | Don't — use diffusion / 不要用——用扩散模型 |

对于产品级演示,答案是"人的脸照片",StyleGAN比推断成本 (单向传递,4090ms <10ms) 的扩散率和相同质量条的敏度更高.

> 对于"人物面部照片"级别的产品展示,StyleGAN在推测成本中,

## 运送它.

保存`outputs/skill-stylegan-inversion.md`技能拍摄真实照片和输出:逆转方法 (e4e / ReStyle / HyperStyle),预期隐藏损失,编辑预算 (到底在`W`您可以在文物之前移动),以及已知编辑指南 (年龄,表情,姿势) 的列表.

> 保存`outputs/skill-stylegan-inversion.md`◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎

## 练习题

1. **Easy / 简单.**跑步`code/main.py`随着`adain_on=True`其他`adain_on=False`对于固定隐形与扰乱隐形的输出分布进行比较.
   分别使用`adain_on=True`和 `adain_on=False`运行――与固定隐变量和动隐变量输出分布相比――
2. **Medium / 中等.**实施混合规律化:对于训练批次,计算`w_a`现在`w_b`应用`w_a`对于合成的第一半年`w_b`解码器能学到没有任何分歧的风格吗?
   实现混合正则化――解码器是否学到了解的风格?
3. **Hard / 困难.**采用预训练的StyleGAN3 FFHQ模型 (ffhq-1024.pkl).`w`通过在标记样品上训练SVM来控制"微笑"的方向;报告在身份漂移之前,您可以推向多远.
   使用预训练 StyleGAN3 FFHQ 模型,通过SVM 找到控制"微笑"的`w`方向:

## 关键词 快速查找表

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Mapping network | "The MLP" / "那个 MLP" | `f: Z → W`, 8 layers, decouples latent geometry from data statistics. / 解耦隐变量几何与数据统计。 |
| W space | "The style space" / "风格空间" | Output of the mapping network; roughly disentangled. / 映射网络的输出；大致解耦。 |
| AdaIN | "Adaptive instance norm" / "自适应实例归一化" | Normalize feature map, then scale + shift by `w`-projection. / 归一化后用 `w` 投影缩放偏移。 |
| Truncation trick | "Psi" | `w = mean + ψ·(w - mean)`, ψ<1 trades diversity for quality. / ψ<1 以多样性换质量。 |
| Path-length regularization | "PL reg" | Penalizes large changes in image per unit change in `w`; makes `W` smoother. / 惩罚 `w` 单位变化引起的大图像变化。 |
| Weight demodulation | "The StyleGAN2 fix" / "StyleGAN2 修复" | Normalize conv weights instead of activations; kills droplet artifacts. / 归一化卷积权重而非激活。 |
| Alias-free | "StyleGAN3's trick" / "StyleGAN3 技巧" | Windowed sinc filters; eliminates texture sticking to the pixel grid. / 窗口 sinc 滤波器消除纹理粘附。 |
| Inversion | "Find w for a real image" / "找 w" | Optimize or encode `x → w` so `G(w) ≈ x`. / 优化或编码使 `G(w) ≈ x`。 |

## 产品说明:为什么StileGAN仍在2026年出货

在4090上,StyleGAN3在10ms内产生10242 FFHQ面孔`num_steps = 1`没有VAE解码,没有跨度注意力通过.在生产方面,这是任何图像生成器的地板延迟.一个50步的SDXL +VAE解码管道在相同分辨率是 ~3秒.**300× gap**对于狭域产品 (avatar服务,身份证件管道,股票面孔生成)

> 风格GAN3 在4090上不到10ms 生成10242 人脸`num_steps = 1`没有VAE解码,没有交叉注意力.**300 倍差距**收获中标产品的收获

两种操作后果:

> 两运营后果:

- **No scheduler, no batcher.**目标占用量最佳的静态批量.持续批量 (对于LLM和传播至关重要) 提供零效益,因为每个请求都采用相同的FLOP.
  **无需调度器或批处理器。**静态批量最优──连续批处理对 LLM 和扩散模型至关重要)零收益──
- **Truncation `ψ` is the safety knob.** `ψ < 0.7`图测网络范围的狭窄角角的样本.这是服务层对样本变异的唯一杆.`ψ`在高负载时,将其提高为优质用户.
  **截断 `ψ` 是安全旋钮。** `ψ < 0.7`从映射网络范围的狭采样.`ψ`高级用户时提高.

## 继续阅读 继续阅读

- [Karras et al. (2019). A Style-Based Generator Architecture for GANs](https://arxiv.org/abs/1812.04948) 风格GAN
- [Karras et al. (2020). Analyzing and Improving the Image Quality of StyleGAN](https://arxiv.org/abs/1912.04958)    
- [Karras et al. (2021). Alias-Free Generative Adversarial Networks](https://arxiv.org/abs/2106.12423)    
- [Tov et al. (2021). Designing an Encoder for StyleGAN Image Manipulation](https://arxiv.org/abs/2102.02766)e4e逆转
- [Sauer et al. (2022). StyleGAN-XL: Scaling StyleGAN to Large Diverse Datasets](https://arxiv.org/abs/2202.00273)     
- [Huang et al. (2024). R3GAN: The GAN is dead; long live the GAN!](https://arxiv.org/abs/2501.05441)现代的最小GAN食谱.
