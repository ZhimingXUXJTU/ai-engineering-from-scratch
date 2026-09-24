# 图像生成 产生对抗网络

> 两种神经网络在一个固定游戏中,一个抽奖,一个批评. 他们一起变得更好,直到图纸欺骗了批评者.

> **【中文解读】**产生对抗网络) 是两个神经网络的博:生成器画画,判别器挑毛病,两者共同进步直到生成器能骗过判别器;;GAN 是图像生成三大路线之一,曾统治 AI 图像生成领域多年;;

> **【拓展：GAN 的遗产】**虽然扩散模型在2022年后成为图像生成的主流,但GAN的反抗训练思想仍然被用来提高其他生成模型的质量.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 03 (CNNs), Phase 3 Lesson 06 (Optimizers), Phase 3 Lesson 07 (Regularization) | **前置知识:** Phase 4 Lesson 03（CNN），Phase 3 Lesson 06（优化器），Phase 3 Lesson 07（正则化）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 解释生成器和分辨器之间的最小数游戏,以及为什么平衡与p_model =p_data相符
- 在 PyTorch 中实现DCGAN,并使它在60行以下生成一致的32x32合成图像
- 通过三个标准技巧稳定GAN训练:不和损失,光谱规范,TTUR (两次更新规则)
- 阅读训练曲线,将健康的融合与模式崩,振荡和歧视者完全区分

> **【中文解读】**学习目标列出了课程完成后应掌握的核心能力.建议在开始学习前先浏览目标,学习完后对照检查是否已实现.


## 问题 问题引入

类别教导网络将图像映射到标签上. 生成逆转问题:样本新图像看起来像来自同一分布. 没有"正确"输出,你可以不同;只有一个你想模仿的分布.

> 分类教学网络将图像映射到标签中. 产生反转了这个问题:样本看起来来自相同分布的新图像.

标准损失函数 (MSE,跨进) 无法测量"这个样本是否来自真实分布".减少每像素错误会产生模糊的平均值,而不是现实样本.突破是学习损失:训练第二个网络,其工作是区分真实与假,并使用其判断力推出发电机.

> 标准损失函数 (MSE、交叉) 不能衡量"这个样本是否来自真实分布"――最小化成像素差异产生模糊的平均值,而不是真实样本――突破是学习损失:训练第二网络,其工作是区分真假,并使用它判断推动生成器――

截至2018年,StyleGAN正在生产1024x1024面,无法与照片区分.从那以后,扩散模型已经在质量和可控制性方面占据了王位,但使扩散实用化的每一个技巧都是GAN上第一次理解的.

> 据GAN的研究,GAN的发展模式已经在质量和可控性上取得了王位,但使扩散的实际应用的每一个技巧都归纳于选择,潜空间,特征损失,都是首先在GAN上理解的.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


### 两家网络

```mermaid
flowchart LR
    Z["z ~ N(0, I)<br/>noise"] --> G["Generator<br/>transposed convs"]
    G --> FAKE["Fake image"]
    REAL["Real image"] --> D["Discriminator<br/>conv classifier"]
    FAKE --> D
    D --> OUT["P(real)"]

    style G fill:#dbeafe,stroke:#2563eb
    style D fill:#fef3c7,stroke:#d97706
    style OUT fill:#dcfce7,stroke:#16a34a
```

其他**generator** G 取出噪音向量`z`它们可以通过一个图像来输出.**discriminator**图像的概率是真实的.

> **生成器**接收噪音向量`z`并输出一张图像.**判别器**接收一张图像并输出一个标志量:该图像为真实图像的概率.

### 游戏

格希望D错误,D想要正确.

> 希望判断错误,希望判断正确――形式化地:

```
min_G max_D  E_x[log D(x)] + E_z[log(1 - D(G(z)))]
```

读到右到左:D是最大化真实 (`log D(real)`) 和假 (`log (1 - D(fake))`图像. G 正在尽量减少D的虚假信息准确性.`D(G(z))`为了高兴.

> 从右往左读:D 在最大化对真实图像`log D(real)`假图像`log(1 - D(fake))`对于假图像的分类准确率,它希望`D(G(z))`尽可能高.

士证明这个最小值有一个全球平衡`p_G = p_data`并且在生成和实际分布之间的森-申农分歧是零.

> 善良的朋友证明了这个极小极大博存在全局平衡点,现在`p_G = p_data`在所有位置输出0.5,生成分布与真实分布之间的詹森-尚农散率为零.

### 无化的损失

早期训练, 早期训练,`D(G(z))`对于每一个假冒,几乎是零,所以`log(1 - D(G(z)))`解决方案是翻转G的损失.

> 上述形式在数值上不稳定.`D(G(z))`对于每一个假样子都接近零,因此`log(1 - D(G(z)))`对 G 的梯度趋于消失──修复方法:翻转 G 的损失函数──

```
L_D = -E_x[log D(x)] - E_z[log(1 - D(G(z)))]
L_G = -E_z[log D(G(z))]                          # non-saturating
```

现在什么时候?`D(G(z))`现在,每一个现代GAN列车都用这种变体.

> 现在,当`D(G(z))`接近零时,G的损失很大,梯度信息充足.

### DCGAN架构规则

拉德福德,梅茨,辛塔拉 (2015) 将多年的失败实验分成五项规则,使得GAN训练稳定:

> 雷德福德·梅茨·辛塔拉 (Radford、Metz、Chintala(2015) 将多年失败实验的经验提炼为五条使GAN 训练稳定规则:

1. 换成双脚 (两个网) 的聚合器.
   中文翻译:用步幅卷积替代池化层(两个网络都适用) 』
2. 在发电机和分辨器中使用批量标准,除了G输出和D输入.
   中文翻译:在生成器和判别器中都使用批归结,但G的输出层和D的输入层除外.
3. 移除更深层的结构上完全连接的层次.
   中文翻译:在更深层次的架构中移除全连接层.
4. G 在所有层上使用ReLU,除了输出 (在 [-1, 1] 中输出的tanh).
   中文翻译:G 在所有层使用 ReLU,输出层除外(输出层使用 tanh 将值域限制在 [-1, 1])。
5. D 在所有层上使用LeakyReLU (负_斜率=0.2).
   中文翻译:D 在所有层使用LeakyReLU(负斜率=0.2)。

现在,每一个基于的GAN (StyleGAN,BigGAN,GigaGAN) 都从这些规则开始,

> 每个现代基于卷积的GAN (StyleGAN,BigGAN,GigaGAN) 仍然从这些规则中发出,逐渐替换其中的组件.

### 失败模式及其签名

```mermaid
flowchart LR
    M1["Mode collapse<br/>G produces a narrow<br/>set of outputs"] --> S1["D loss low,<br/>G loss oscillating,<br/>sample variety drops"]
    M2["Vanishing gradients<br/>D wins completely"] --> S2["D accuracy ~100%,<br/>G loss huge and static"]
    M3["Oscillation<br/>G and D keep trading<br/>wins forever"] --> S3["Both losses swing<br/>wildly with no downward trend"]

    style M1 fill:#fecaca,stroke:#dc2626
    style M2 fill:#fecaca,stroke:#dc2626
    style M3 fill:#fecaca,stroke:#dc2626
```

- **Mode collapse**修复:添加微批次分辨率,光谱规范或标签条件.
  中文翻译:模式塌G 找到一张能骗过D的图像,然后只生成那张──修复:添加小批量判别、谱归结或标签条件化──
- **Discriminator wins**修复:D较小,D学习率较低,或将标签滑滑在真实标签上.
  中文翻译:判别器完胜D 变得太强太快,G 的梯度消失──修复:缩小D、降低D 学习率或对真实标签进行平滑──
- **Oscillation**修复:TTUR (D学习比G快2倍2倍),或转向Wasserstein损失.
  中文翻译:振荡两个网络交换占优,永远无法接近平衡──修复:TTUR(D比 G 快 2-4倍) 或切换到Wasserstein 损失──

### 评估

没有实在的GAN,你怎么知道它们是有效的?

> 没有标准答案,那么如何判断它们是否正常工作?

- **Sample inspection**每一个时代结束时,只要看看64个样本.
  中文翻译:样本检查每个时代 结束时看64个样本──这是不可省略的步骤──
- **FID (Fréchet Inception Distance)** 距离在实体和生成集合的分类中.较低更好.
  中文翻译:FID(Fréchet 开始距离) 真实集和生成集在开始-v3特征分布之间的距离──越低越好──社区标准──
- **Inception Score**年龄较大,较脆弱;更喜欢FID.
  中文翻译:初始分数较老,较脆弱;优先使用FID──
- **Precision/Recall for generative models** 单独测量质量 (精度) 和覆盖性 (召回).
  中文翻译:生成模型的精确率/召回率分别衡量质量 (精确率) 和覆盖率 (覆盖率) ◎比单独的FID更有信息量──

对于小型合成数据运行,样本检查就足够了.

> 对于小规模的合成数据实验,样本检查就足够了.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：工业部署中的视觉系统】**在实际工业部署中,视觉模型需要考虑推迟模型大小的边缘设备适应等问题.

> **【拓展：数据标注与质量】**视觉任务的效果高度依赖标签数据质量――标签工作室、CVAT是主流标签工具――在工业场景中,主动学习(主动学习) 可以减少标签成本:模型对不确定的样本请求人工标签,确定性的样本自动标签――




## 建立它,实现它.
```figure
cv-gan-image
```

## 建立它

### 步骤1:发电机

通过 64 维噪音生成32x32图像的小型DCGAN发电机.

> 一个小型DCGAN 生成器,接收64维噪音并生成32x32图像.

```python
import torch
import torch.nn as nn

class Generator(nn.Module):
    def __init__(self, z_dim=64, img_channels=3, feat=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.ConvTranspose2d(z_dim, feat * 4, kernel_size=4, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(feat * 4),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(feat * 4, feat * 2, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(feat * 2),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(feat * 2, feat, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(feat),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(feat, img_channels, kernel_size=4, stride=2, padding=1, bias=False),
            nn.Tanh(),
        )

    def forward(self, z):
        return self.net(z.view(z.size(0), -1, 1, 1))
```

转换了四个车辆,每个车辆都有`kernel_size=4, stride=2, padding=1`通过TANH,输出激活在 [-1, 1] 中.

> 转置卷,每使用`kernel_size=4, stride=2, padding=1`以便干净地将空间尺寸翻倍――通过h将输出激活值限制在 [-1, 1]――

### 第二步: 歧视者

漏的雷卢,步骤的电梯,以一个尺度的逻辑结束.

> 发射器的镜像──LeakyReLU、步幅卷积,最终输出一个标量逻辑──

```python
class Discriminator(nn.Module):
    def __init__(self, img_channels=3, feat=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(img_channels, feat, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(feat, feat * 2, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(feat * 2),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(feat * 2, feat * 4, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(feat * 4),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(feat * 4, 1, kernel_size=4, stride=1, padding=0),
        )

    def forward(self, x):
        return self.net(x).view(-1)
```

最后一个缩一个`4x4`功能地图`1x1`输出是每张图像的单个 skalar;仅在损失计算过程中应用 sigmoid.

> 最后一个卷积将`4x4`缩减的特征`1x1`△每张图像输出一个标量;仅在损失计算时应用标量.

### 步骤3:培训步骤

换个方式:一次更新D,然后一次更新G,每批次.

> 交替进行:每批先更新 D 一次,再更新 G 一次。

```python
import torch.nn.functional as F

def train_step(G, D, real, z, opt_g, opt_d, device):
    real = real.to(device)
    bs = real.size(0)

    # D step
    opt_d.zero_grad()
    d_real = D(real)
    d_fake = D(G(z).detach())
    loss_d = (F.binary_cross_entropy_with_logits(d_real, torch.ones_like(d_real))
              + F.binary_cross_entropy_with_logits(d_fake, torch.zeros_like(d_fake)))
    loss_d.backward()
    opt_d.step()

    # G step
    opt_g.zero_grad()
    d_fake = D(G(z))
    loss_g = F.binary_cross_entropy_with_logits(d_fake, torch.ones_like(d_fake))
    loss_g.backward()
    opt_g.step()

    return loss_d.item(), loss_g.item()
```

`G(z).detach()`在D步骤中,关键是:我们不希望更新时渐变流入G.忘记这是经典的初学者错误.

> 步骤中的`G(z).detach()`至关重要:我们不希望在D更新过程中梯度流回G.

### 步骤4:合成形状的全训练循环

```python
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

def synthetic_images(num=2000, size=32, seed=0):
    rng = np.random.default_rng(seed)
    imgs = np.zeros((num, 3, size, size), dtype=np.float32) - 1.0
    for i in range(num):
        r = rng.uniform(6, 12)
        cx, cy = rng.uniform(r, size - r, size=2)
        yy, xx = np.meshgrid(np.arange(size), np.arange(size), indexing="ij")
        mask = (xx - cx) ** 2 + (yy - cy) ** 2 < r ** 2
        color = rng.uniform(-0.5, 1.0, size=3)
        for c in range(3):
            imgs[i, c][mask] = color[c]
    return torch.from_numpy(imgs)

device = "cuda" if torch.cuda.is_available() else "cpu"
data = synthetic_images()
loader = DataLoader(TensorDataset(data), batch_size=64, shuffle=True)

G = Generator(z_dim=64, img_channels=3, feat=32).to(device)
D = Discriminator(img_channels=3, feat=32).to(device)
opt_g = torch.optim.Adam(G.parameters(), lr=2e-4, betas=(0.5, 0.999))
opt_d = torch.optim.Adam(D.parameters(), lr=2e-4, betas=(0.5, 0.999))

for epoch in range(10):
    for (batch,) in loader:
        z = torch.randn(batch.size(0), 64, device=device)
        ld, lg = train_step(G, D, batch, z, opt_g, opt_d, device)
    print(f"epoch {epoch}  D {ld:.3f}  G {lg:.3f}")
```

`Adam(lr=2e-4, betas=(0.5, 0.999))`低的beta1 阻碍动力期来稳定对手的游戏.

> `Adam(lr=2e-4, betas=(0.5, 0.999))`是DCGAN默认配置低的beta1 防止动量项过度稳定对抗博

### 步骤5:采样

```python
@torch.no_grad()
def sample(G, n=16, z_dim=64, device="cpu"):
    G.eval()
    z = torch.randn(n, z_dim, device=device)
    imgs = G(z)
    imgs = (imgs + 1) / 2
    return imgs.clamp(0, 1)
```

在采样之前,总是切换到评估模式.对于DCGAN来说,这是重要的,因为使用批量规范运行统计数据而不是批量统计数据.

> 采样前务必切换到评估模式. 对DCGAN来说,这是很重要的,因为批量归纳将使用运行时统计量而不是当前批量统计量.

### 步骤 6: 频谱规范化

网络保证的区别器中,BN的替代器是1-Lipschitz.

> 谱归结是判定器中批归结的即插即用替代方案,保证网络是1-Lipschitz的――能修复大多数"D 赢得太彻底"的问题――

```python
from torch.nn.utils import spectral_norm

def build_sn_discriminator(img_channels=3, feat=64):
    return nn.Sequential(
        spectral_norm(nn.Conv2d(img_channels, feat, 4, 2, 1)),
        nn.LeakyReLU(0.2, inplace=True),
        spectral_norm(nn.Conv2d(feat, feat * 2, 4, 2, 1)),
        nn.LeakyReLU(0.2, inplace=True),
        spectral_norm(nn.Conv2d(feat * 2, feat * 4, 4, 2, 1)),
        nn.LeakyReLU(0.2, inplace=True),
        spectral_norm(nn.Conv2d(feat * 4, 1, 4, 1, 0)),
    )
```

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


换换`Discriminator`为了`build_sn_discriminator()`频谱规范是你能应用的最简单的单一强度升级.

> 将`Discriminator`替换为`build_sn_discriminator()`后通常不需要TTUR技巧.谱归化是你能应用的最简单的单一棒性升级.




> **【拓展：视觉模型的持续学习】**在生产环境中,视觉模型需要不断适应新数据. 持续学习. 持续学习. 技术可以防止模型在适应新数据时忘记旧知识.

## 用它实现框架

对于严格的生成,使用预训练的权重或转换为扩散.

- `torch_fidelity`在你的发电机上计算FID/IS,而不需要编写定制的评估代码.
- `pytorch-gan-zoo`其他国家`StudioGAN`试验的DCGAN,WGAN-GP,SN-GAN,StayGAN和BigGAN的实施方案.

在2026年,GAN仍然是最好的选择:实时图像生成 (延迟 <10 ms),风格转移,精确控制的图像到图像翻译 (Pix2Pix,CycleGAN).

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.




## 运送它.

这一课产生了:

- `outputs/prompt-gan-training-triage.md`一个提示,读取训练曲线描述,选择失败模式 (模式崩,D-win,振荡) 加上单个建议的修复.
- `outputs/skill-dcgan-scaffold.md`写一个DCGAN架子的技能`z_dim`目标`image_size`其他`num_channels`包括训练循环和样本节省器.

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


## 练习题

1. **(Easy)**在每个时代结束时,将DCGAN训练在合成圈数据集上,并保存16个样本的网格.
2. **(Medium)**换取分辨器的批量标准,用光谱标准. 训练两种版本一边. 哪个版本更快地融合?哪个种子之间的差异较低?
3. **(Hard)**实施条件的DCGAN:将类标签输入到G和D (在G中对噪音进行一次性缩,在D中缩放类嵌入道).从第7课中训练合成"圆与平方"数据集,并通过采用特定标签进行样本测试来证明类调节工作.

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Generator (G) | "The draws-stuff net" | Maps noise to images; trained to fool the discriminator |
| Discriminator (D) | "The critic" | Binary classifier; trained to distinguish real from generated images |
| Minimax | "The game" | min over G, max over D of an adversarial loss; equilibrium is p_G = p_data |
| Non-saturating loss | "The numerically sane version" | G's loss is -log(D(G(z))) instead of log(1 - D(G(z))) to avoid vanishing gradients early in training |
| Mode collapse | "Generator makes one thing" | G produces only a small subset of the data distribution; fix with SN, minibatch discrimination, or larger batch |
| TTUR | "Two learning rates" | D learns faster than G, typically by a factor of 2-4; stabilises training |
| Spectral norm | "1-Lipschitz layer" | A weight-normalisation that bounds each layer's Lipschitz constant; stops D from becoming arbitrarily steep |
| FID | "Fréchet Inception Distance" | Distance between Inception-v3 feature distributions of real and generated sets; the standard evaluation metric |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Generative Adversarial Networks (Goodfellow et al., 2014)](https://arxiv.org/abs/1406.2661)报纸是这一切的起始.
- [DCGAN (Radford, Metz, Chintala, 2015)](https://arxiv.org/abs/1511.06434)使GAN可培训的建筑规则
- [Spectral Normalization for GANs (Miyato et al., 2018)](https://arxiv.org/abs/1802.05957)最有用的稳定技巧
- [StyleGAN3 (Karras et al., 2021)](https://arxiv.org/abs/2106.12423)苏塔甘;读起来像一个最伟大的成功专辑,
