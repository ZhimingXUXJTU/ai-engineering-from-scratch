# 图像检索和测量学习

> 测量学习是塑造空间的学科,使距离意味着你想要的.

> **【中文解读】**检索系统通过嵌入空间中的距离对候选图像排序进行了测量学习就是塑造这个空间,使距离反映你想要的语义关系相似图像靠近,不相似图像离远.

> **【拓展：检索系统的应用】**以图搜图(Google图片、淘宝拍照搜索)、人脸识别(FaceNet)、推系统(Pinterest) 都依赖于量度学习──CLIP对比预训本质上也是量度学习──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 14 (ViT), Phase 4 Lesson 18 (CLIP) | **前置知识:** Phase 4 Lesson 14（ViT），Phase 4 Lesson 18（CLIP）
**Time:** ~45 minutes | **时间:** ~45 分钟

## 学习目标

- 解释三小部分,对比和代理的指标学习损失,并选择给定的数据集的正确数据
- 执行L2规范化和共数相似性正确,并审核"同类"和"同类"检索之间的差异
- 建立一个 FAISS 指数,通过文字和图像查询,并报告回忆@K 对于一个已保留的查询集
- 使用DINOv2,Clip和SigLIP作为现货嵌入骨,并知道每一个赢得什么时候

> **【中文解读】**学习目标列出了课程完成后应掌握的核心能力.建议在开始学习前先浏览目标,学习完后对照检查是否已实现.


## 问题 问题引入

检索在生产视觉中无处不在:重复检测,反向图像搜索,视觉搜索 ("找到类似的产品"),面部重新识别,监控的人身份,电子商务的实例级匹配.

> 检索在生产视觉中无处不在:重复检测、反向图像搜索、视觉搜索("寻找相似产品")、人脸重识别、监控人员重识别、电商实例级匹配──产品问题总是相同:"给定这张查询图像,对我的目录排序──"

两个设计决定塑造整个系统.嵌入式 产生向量模型.索引 如何在尺度上找到最近的邻居.这两种都是2026年的商品 (嵌入式 DINOv2 ,索引式 FAISS),这提高了条:最难的部分是定义 *什么是类似的* 对于您的应用,然后塑造嵌入式空间,使距离匹配.

> 两个设计决策塑造整个系统――嵌入式什么模型产生量量――索引式如何大规模找到最近的邻居――两者在2026年都是商品――DINOv2用于嵌入式,FAISS用于索引式),这提高了标准:困难的部分是为你的应用定义*什么算相似*,然后塑造嵌入式空间使距离匹配――

塑造是一种微小但高杆性的学科.

> 塑造就是量度学习.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


### 一眼发现

```mermaid
flowchart LR
    Q["Query image<br/>or text"] --> ENC["Encoder"]
    ENC --> EMB["Query embedding"]
    EMB --> IDX["FAISS index"]
    CAT["Catalogue images"] --> ENC2["Encoder (same)"] --> IDX_BUILD["Build index"]
    IDX_BUILD --> IDX
    IDX --> RANK["Top-k nearest<br/>by cosine / L2"]
    RANK --> OUT["Ranked results"]

    style ENC fill:#dbeafe,stroke:#2563eb
    style IDX fill:#fef3c7,stroke:#d97706
    style OUT fill:#dcfce7,stroke:#16a34a
```

### 失去的四个家庭

| Loss | Requires | Pros | Cons |
|------|----------|------|------|
| **Contrastive** | (anchor, positive) + negatives | Simple, works with any pair label | Slow to converge without many negatives |
| **Triplet** | (anchor, positive, negative) | Intuitive; direct margin control | Hard-triplet mining is expensive |
| **NT-Xent / InfoNCE** | Pairs + batch-mined negatives | Scales to large batches | Needs big batch or momentum queue |
| **Proxy-based (ProxyNCA)** | Class labels only | Fast, stable, no mining | Can overfit to proxies on small datasets |

在大多数生产使用案例中,从预训练的脊椎开始,只需在测试组上使用的嵌入式性能低,才能添加测量学习细节调整.

> 对于大多数生产场景,从预训练骨干网络开始,只有当现成的嵌入在你的测试集中表现不佳时才会增加学习量微调.

### 官方的三分之一损失

```
L = max(0, ||f(a) - f(p)||^2 - ||f(a) - f(n)||^2 + margin)
```

拉`a`接近正面`p`让它远离负面`n`通过`margin`对于任何类似性来说,这将使得图像结构普遍化.

> 将点`a`拉近正样本`p`推远负样本`n`用`margin`确保间隔──三图像结构可推广到任何相似度排序──

矿业问题:轻松三重 (`n`现在还不太久了`a`只有硬三分之一教网络.`n`超过`p`虽然这项技术是最重要的,但在边缘范围内) 是2016年FaceNet的配方,

> 挖掘很重要:简单三元组`n`已经远离了`a`贡献零损失;只有困难三元组能教网络――半困难挖掘`n`比比`p`远但在边缘内) 是2016年FaceNet的方案,至今仍占主导地位.

### 子相似性与L2

两个指标,两个公约:

> 两种量,两种约定:

- **Cosine**需要L2标准化嵌入式.
  翻译: 中文**余弦**需要 L2 归结嵌入式
- **L2**工作在原始或正常嵌入式上,但通常与L2正常化 +2L2相对.
  翻译: 中文**L2**适用于原始或归化嵌入,但通常与L2归化+平方L2配对使用.

对于大多数现代网络来说,这两种网络是相当的:`||a - b||^2 = 2 - 2 cos(a, b)`什么时候`||a|| = ||b|| = 1`选择与你的嵌入训练相匹配的会议; 默默地混合它们改变了"最接近"的意思.

> 对于大多数现代网络,两者等价:当 `||a|| = ||b|| = 1`时,`||a - b||^2 = 2 - 2 cos(a, b)`选择与嵌入训练匹配的约定;混用会静默改变"最近"的含义

### 提醒@K

标准检索指标:

```
recall@K = fraction of queries where at least one correct match is in the top K results
```

报告 recall@1, @5, @10 旁边. recall@10 在 0.95 之上, recall@1 在 0.5 之下,意味着嵌入空间有正确的结构,但排名很尝试更长的细节调节或重新排名步骤.

> 并排报告回忆@1、@5、@10──回忆@10 超过0.95 但回忆@1 低于0.5 意思是嵌入空间结构正确但排序有噪音尝试更长的微调或重排序步骤──

对于重复检测,精度@K更重要,因为每一个假正是用户可见的错误.

> 对于重复检测,精确性更重要,因为每个假阳性都是用户可见的错误.

### 单一段落中的 FAISS

根据"Facebook AI相似性搜索"的实际图书馆,

> 搜索结果: 搜索结果: 搜索结果: 搜索结果:

- `IndexFlatIP`现在,`IndexFlatL2`粗力,精确,没有训练. 运用到1M向量.
  翻译: 中文`IndexFlatIP`现在,`IndexFlatL2`暴力搜索,精确,无需训练――适用于约100万向量内――
- `IndexIVFFlat`分成K细胞,只搜索最近的几个细胞. 接近,快速,需要训练数据.
  翻译: 中文`IndexIVFFlat`分为K个单元,只搜索最近几个单元――近似、快速,需要训练数据――
- `IndexHNSW`基于图表,最快于许多查询,大指数尺寸.
  翻译: 中文`IndexHNSW`基于图,多查询时最快,索引大小较大.

对于100万个向量,你可能想要`IndexFlatIP`对于10万,你想要的`IndexIVFFlat`对于100万+与产品量化相结合 (`IndexIVFPQ`)

> 百万向量使用`IndexFlatIP`余弦相似度即可.`IndexIVFFlat`△1亿以上的配合乘积量化`IndexIVFPQ`

### 实例级别与类别级别检索

两个完全不同的问题,

> 两个名字相同,但非常不同的问题:

- **Category-level**"在我的目录中找到猫".类条件相似性;现货CLIP/DINOv2嵌入式工作良好.
  翻译: 中文**类别级**"在我的目录中找猫"──类别条件相似度;现成的 CLIP / DINOv2 嵌入即可──
- **Instance-level**"在我的目录中找到*这个精确的产品*".需要细微的区分相同类别的视觉相似物体;现货嵌入式性能低;对测量学习问题进行细微调整.
  翻译: 中文**实例级**"在我的目录中找到*这个特定产品*"──需要与类视觉相似物体之间的细分分辨率;现成嵌入表现不佳;度量学习微调很重要──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

在选择模型之前,你总是问你要解决哪个问题.

> 在选择模型之前,务必问清楚你在解决哪个问题.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：工业部署中的视觉系统】**在实际工业部署中,视觉模型需要考虑推迟模型大小的边缘设备适应等问题.

> **【拓展：数据标注与质量】**视觉任务的效果高度依赖标签数据质量――标签工作室、CVAT是主流标签工具――在工业场景中,主动学习(主动学习) 可以减少标签成本:模型对不确定的样本请求人工标签,确定性的样本自动标签――




## 建立它,实现它.
```figure
metric-embedding
```

## 建立它

### 步骤1:三分钟损失

```python
import torch
import torch.nn.functional as F

def triplet_loss(anchor, positive, negative, margin=0.2):
    d_ap = F.pairwise_distance(anchor, positive, p=2)
    d_an = F.pairwise_distance(anchor, negative, p=2)
    return F.relu(d_ap - d_an + margin).mean()
```

能在L2标准化或原始嵌入式上使用.

> 一行代码――适用于L2归结或原始嵌入式――

### 步骤2:半硬的采矿

根据嵌入式和标签的批量, 找出每个的最难的半硬负值.

> 给定一批嵌入和标签,为每一个点找到最难的半困难负面样本.

```python
def semi_hard_negatives(emb, labels, margin=0.2):
    dist = torch.cdist(emb, emb)
    same_class = labels[:, None] == labels[None, :]
    diff_class = ~same_class
    N = emb.size(0)

    positives = dist.clone()
    positives[~same_class] = float("-inf")
    positives.fill_diagonal_(float("-inf"))
    pos_idx = positives.argmax(dim=1)

    semi_hard = dist.clone()
    semi_hard[same_class] = float("inf")
    d_ap = dist[torch.arange(N), pos_idx].unsqueeze(1)
    semi_hard[dist <= d_ap] = float("inf")
    neg_idx = semi_hard.argmin(dim=1)

    fallback_mask = semi_hard[torch.arange(N), neg_idx] == float("inf")
    if fallback_mask.any():
        hardest = dist.clone()
        hardest[same_class] = float("inf")
        neg_idx = torch.where(fallback_mask, hardest.argmin(dim=1), neg_idx)
    return pos_idx, neg_idx
```

每个都有最硬的正值,半硬的负值,远于正值,但在边缘范围内.

> 每个点都能获得同类中最难的正品样本和比较正品样本的远,但在边缘内半难负品样本.

### 步骤3:回忆@K

```python
def recall_at_k(query_emb, gallery_emb, query_labels, gallery_labels, k=1):
    sim = query_emb @ gallery_emb.T
    _, top_k = sim.topk(k, dim=-1)
    matches = (gallery_labels[top_k] == query_labels[:, None]).any(dim=-1)
    return matches.float().mean().item()
```

在L2标准化嵌入式上,内产量上-k等于kosine上-k.报告至少一个正确邻居的平均查询比例.

> 报告至少有一个正确的邻居查询的平均比例.

### 步骤4: 组合

```python
import torch
import torch.nn as nn
from torch.optim import Adam

class Encoder(nn.Module):
    def __init__(self, in_dim=128, emb_dim=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 128), nn.ReLU(),
            nn.Linear(128, emb_dim),
        )

    def forward(self, x):
        return F.normalize(self.net(x), dim=-1)

torch.manual_seed(0)
num_classes = 6
protos = F.normalize(torch.randn(num_classes, 128), dim=-1)

def sample_batch(bs=32):
    labels = torch.randint(0, num_classes, (bs,))
    x = protos[labels] + 0.15 * torch.randn(bs, 128)
    return x, labels

enc = Encoder()
opt = Adam(enc.parameters(), lr=3e-3)

for step in range(200):
    x, y = sample_batch(32)
    emb = enc(x)
    pos_idx, neg_idx = semi_hard_negatives(emb, y)
    loss = triplet_loss(emb, emb[pos_idx], emb[neg_idx])
    opt.zero_grad(); loss.backward(); opt.step()
```

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


后几百步,嵌入集群形成一个集群每个类.

> 几百步后,嵌入集成形成每个类别一个──




> **【拓展：视觉模型的持续学习】**在生产环境中,视觉模型需要不断适应新数据. 持续学习. 持续学习. 技术可以防止模型在适应新数据时忘记旧知识.

## 用它实现框架

2026年生产堆:

- **DINOv2 + FAISS**一般用途的视觉检索.
- **CLIP + FAISS**当查询是短信时.
- **Fine-tuned DINOv2 + FAISS**实例级检索,面部重新识别,时尚,电子商务.
- **Milvus / Weaviate / Qdrant**管理在 FAISS 或 HNSW 周围的向量 DB 包装.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


对于SOTA实例检索,配方是:DINOv2脊柱,添加嵌入头,通过三小组调整或InfoNCE损失在实例标记的对,索引在FAISS中.



## 运送它.

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


这一课产生了:

- `outputs/prompt-retrieval-loss-picker.md`一个提示,选择给定的检索问题的三小部分 / InfoNCE / ProxyNCA.
- `outputs/skill-recall-at-k-runner.md`写一个清洁的评估带,以火车//图库分区和适当的数据合同.

## 练习题

1. **(Easy)**在训练前和后,用PCA绘制嵌入式图,看看六个集群形成.
2. **(Medium)**添加ProxyNCA损失实现:每个类学习一个"代理",在可西因相似度上标准交叉.在玩具数据上比较缩速度与三分钟损失.
3. **(Hard)**通过 HuggingFace 嵌入DINOv2的1000个ImageNet验证图像,构建一个 FAISS平面索引,并报告回忆@{1, 5, 10}与查询相同的图像 (应该是1.0) 和与ImageNet标签的持久分离作为基础真相.

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Metric learning | "Shape the space" | Training an encoder so distances in its output space reflect a target similarity |
| Triplet loss | "Pull and push" | L = max(0, d(a, p) - d(a, n) + margin); the canonical metric-learning loss |
| Semi-hard mining | "Useful negatives" | Negatives further from the anchor than the positive but within margin; empirically the most informative |
| Proxy-based loss | "Class prototypes" | One learned proxy per class; cross-entropy over similarity-to-proxies; no pair mining |
| Recall@K | "Top-K hit rate" | Fraction of queries with at least one correct result in the top K |
| Instance retrieval | "Find this exact thing" | Fine-grained matching; off-the-shelf features usually underperform |
| FAISS | "The NN library" | Facebook's nearest-neighbour library; supports exact and approximate indexes |
| HNSW | "Graph index" | Hierarchical navigable small world; fast approximate NN with small memory overhead |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [FaceNet: A Unified Embedding for Face Recognition (Schroff et al., 2015)](https://arxiv.org/abs/1503.03832)三片损失/半硬的矿山纸
- [In Defense of the Triplet Loss for Person Re-Identification (Hermans et al., 2017)](https://arxiv.org/abs/1703.07737)三重小组细调的实用指南
- [FAISS documentation](https://github.com/facebookresearch/faiss/wiki)每一个指数,每一个交易
- [SMoT: Metric Learning Taxonomy (Kim et al., 2021)](https://arxiv.org/abs/2010.06927)现代损失及其联系的调查
