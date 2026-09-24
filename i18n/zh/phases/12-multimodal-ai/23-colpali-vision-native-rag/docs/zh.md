# 专业技术和视觉原生文档

> 传统的RAG将PDF解析成文本,分成块,嵌入块,存储向量. 每一步都会失去信号:OCR丢掉图表数据,碎碎表行,文字嵌入式忽略数字. 科尔帕利 (Faysse等,2024年7月) 提出了一个更简单的问题:为什么要提取文本? 直接通过PaliGemma嵌入页面图像,使用ColBERT式的晚间交互来检索,并保留文件所载的所有布局,数字,字体和格式化信号. 发表的基准标准:视觉丰富的文档的端到端准确度比文本RAG要高20-40%.  ColQwen2, ColSmol 和 VisRAG 扩大了这种模式. 这一课读出了视觉原生RAG论文,

> **【中文解读】**传统的RAG在PDF上表现不佳,因为每一步都在丢失信号:OCR 丢图表、分块破坏表格行行、文本嵌入忽略图片。ColPali 问了一个更简单的问题:为什么要提取文本?直接使用PaliGemma 嵌入页面图像,使用ColBERT风格的MaxSim 延迟交互进行检索,保留文档的全部布局、图表、字体和格式信号。在视觉丰富文档上,RAG 准确率高于20-40%──

> **【拓展：ColPali 在金融 RAG 中的应用】**金融报告是最典型的视觉丰富文档Q3 营收增长通常在图表中,合同签名块是布局事实而不是文本事实. ColPali 直接嵌入页面图像,保留完整的视觉信号,非常适合金融报告,合同,发票等场景. 储备开销约为文本RAG的5-10倍,但在准确率上升通常会带来这个成本.

**Type:** Build
**Languages:** Python (stdlib, multi-vector indexer + MaxSim scorer)
**Prerequisites:** Phase 11 (LLM Engineering — RAG basics), Phase 12 · 05 (LLaVA)
**Time:** ~180 minutes

>  **【前置】**开始学习,然后开始学习:阶段11·14-16(RAG 基础:嵌入/切割/恢复) 阶段11·13(ColBERT 延迟交互检索,ColPali 直接借鉴)
>  **【类比】**传统RAG vs ColPali = "看书先扫描成纯文本" vs "直接看图找答案"──传统 = OCR 提取文字→分块→嵌入式(图表数据全部丢失);ColPali = 直接对页面图像做补丁嵌入式(图表、表格、布局全保留)──在金融报告中,ColPali准确率高20%-40%.

## 学习目标

- 解释双编码检索 (每文档一个向量) 和晚交互检索 (每文档许多向量) 的区别.
  中文翻译:解释双编码器检查 (每文档一个向量) 和延迟交互检查 (每文档多个向量) 的区别.
- 描述ColBERT的MaxSim操作以及ColPali如何将其从文字代币到图像补丁来概括.
  中文翻译:描述ColBERT的MaxSim操作以及ColPali如何将其从文本代币推广到图像补丁.
- 建立一个像 ColPali 的小索引:页面 →补丁嵌入 → 查询术语嵌入 → top-k页面.
  中文翻译:构建一个微型 ColPali 式索引器:页面→补丁 嵌入→对查询词嵌入做MaxSim→top-k 页面。
- 在发票/财务报告使用情况上,比较ColPali + Qwen2.5VL发电机与文字RAG + GPT-4.
  中文翻译:在发票/金融报告用例上比较ColPali + Qwen2.5-VL 生成器 vs 文本RAG + GPT-4──

## 问题 问题引入

文件中的文字-RAG会丢弃大部分文件.财务报告的第三季度收入增长通常是在图表中;医疗报告的发现在注释图像中;法律合同的签名区块是布局事实,而不是文本事实.

> 财务报告第三季度营收增长通常在图表中;医疗报告的发现标记在图像上;法律合同的签署块是布局事实,不是文本事实――

文字-RAG管道:

> 文本 拉格 管道:

1. 通过OCR/pdftotext来使用PDF →文本.
   中文翻译:PDF → 通过OCR/pdf到文字提取文本──
2. 文字 → 300-500个代币.
   中文翻译:文本 → 300-500个代币的块──
3. 部分 → 双编码嵌入 (一个向量).
   中文翻译:块 → 双编码器嵌入(一个向量) 』
4. 用户查询 →嵌入 → 合数相似 → 顶级k块.
   中文翻译:用户查询 → 嵌入 → 余弦相似度 → 顶-k块──
5. 士+查询 →法学士.
   中文翻译:块 + 查询 → LLM。

五个失败步骤,图表未被捕获,表格被分成块,多列布局平坦化,图形注释消失.

> 五个有损步骤――图表未获取――图表被块截截了.多布局被展平――图表注释消失――

 ColPali 的解决方案:跳过 OCR,直接嵌入页面图像. 使用 ColBERT 式的晚间交互来检索,以便模型可以在查询时处理细粒度的补丁.

> 修复:跳过OCR,直接嵌入页面图像――使用ColBERT风格的延迟交互进行检查,使模型能够在查询时关注细粒度补丁――

## 概念的核心概念

> **【中文解读】**通过OCR,直接将文档页面作为图像编码为向量,使用视觉相似性检查. ColPali的核心创新是 MaxSim 模式查询的每个代币嵌入文档页面的每个补丁嵌入最大相似性匹配,然后求和.

> **【拓展：视觉原生 RAG 的优势**传统RAG管线(OCR -> 文本 -> 嵌入 -> 检索) 在复杂版面上(表格、图表、公式) 上经常失败──ColPali 直接在视觉层次匹配,无需OCR,在包含图表和表格的文档检索上比传统方法提升 30-50%──缺点是需要更多存储的(每页向量)──


> **【拓展：ColPali 的效率分析】**查询延迟与传统方法相等 (约50ms/查询),但在包含图表和表格的文档上,准确率提高了30-50%.缺点是索引存储成本更高.每页需要一个1280维向量而不是传统方法的768维.


### 科尔伯特 (2020)

科尔伯特 (Khattab & Zaharia, arXiv:2004.12832) 是一个文本检索方法.它每文档的向量不是一个,而是每代币产生一个向量.

> 科尔伯特是文本检查方法,不是每文档一个向量,而是每代币一个向量.

- 查询代币得到自己的嵌入 (N_q向量).
  中文翻译:查询代币 获得自己的嵌入
- 文件代币得到嵌入 (N_d向量,通常缓存).
  中文翻译:文档代币 获得嵌入
- 积分 = 查询代币的总数max对文件代币的共数相似性: Σ_i max_j cos(q_i, d_j).
  中文翻译:分数 = 对查询代币 求和,每个查询代币 取文档代币 中最大余弦相似度:Σ_i max_j cos(q_i,d_j) 』

现在,我们要做什么?

> 这就是MaxSim操作. 每个查询代币"挑选"其最佳匹配的文档代币.

优点:强大的回忆,处理术语级语义. 缺点:每文档的N_d向量,存储成本昂贵.

> 优势:强召回率,处理词级语义――劣势:每文档 N_d 个向量,储存昂贵――

### 鱼

科尔帕利 (Faysse等人, arXiv:2407.01449) 应用了科尔伯特模式到图像.

> 利将ColBERT模式应用于图像.

- 每页面都通过PaliGemma (ViT+语言) 编码成补丁嵌入式:每页的N_p向量.
  中文翻译:每页由PaliGemma(ViT + 语言)编码为补丁 嵌入:每页 N_p 个向量。
- 每个用户查询 (文本) 都被编码成查询标志嵌入式:N_q向量.
  中文翻译:每个用户查询(文本)编码为查询代币 嵌入:N_q 个向量。
- 评分 = Σ_i max_j cos(q_i, p_j),即 MaxSim对查询文本标记和页面图像补丁.
  中文翻译:分数 = Σ_i max_j cos(q_i, p_j),即查询文本代币 和页面图像补丁的 MaxSim。
- 根据总分数,查看最好的页面.
  中文翻译:按总分检索上面.

在文件吞时:将每页都使用PaliGemma嵌入,存储所有补丁嵌入.在查询时:嵌入查询代码,计算MaxSim与所有存储的页面嵌入,返回顶级k页面.

> 文档摄取时:使用PaliGemma 嵌入每页,存储所有补丁 嵌入――查询时:嵌入查询代币,对所有存储的页面嵌入计算MaxSim,返回顶级页面――

优点:在视觉丰富的文档上,端到端比文字RAG20-40%更好.每个补丁向量捕捉到本地布局和内容.

> 优势:端到端在视觉丰富文档上文本RAG高20-40%──每个补丁向量捕获局部布局和内容──

缺点:每页的N_p补丁 × 4 字节浮动 × D dim 矢量 = 存储速度增长快.

> 劣势:N_p 个补丁 × 4 字节浮点 × D 维向量每页 = 储存快速增长――可通过 PQ/OPQ 量化缓解――

### 素2和素

文2 (伊利科技, 2024-2025) 换了PaliGemma为Qwen2-VL. 更好的基底编码器,更好的检索.

> 文2将替换PaliGemma为文2VL.

 ColSmol 是用于本地/边缘使用的较小规模变体.

> 模是面向本地/边缘使用的较小规模变体.

### 皮

维斯RAG (Yu et al., arXiv:2410.10594) 是一个不同的变体:取而代之的是MaxSim在补丁上,将每个页面集成成一个单个向量,然后使用VLM检索双码码.更快的索引 +更小的存储,更弱的回忆.

> 维斯拉格是不同的变体:不是在补丁上做MaxSim,而是用VLM将每个页面池化为单向量重复编码器检查.

质量与成本的折衷:质量是ColPali,规模是VISRAG.

> 质量与成本的权衡:ColPali 追求质量,VisRAG 追求规模――

### 其他类型

M3DocRAG (Cho et al., arXiv:2411.04952) 将多模索取扩展到多页多文档推理.

> 通过M3DocRAG将多模态检查扩展到多页多文档推理――跨文档检查页面,为VLM组合多页上下文――

### 基准指数

视觉文件检索评估.任务包括财务报告,科学论文,行政文件,医疗记录,手册.

> 科普利的配套基准──视觉文档检查评估──任务包括金融报告、科学论文、行政文件、医疗记录、手册──指标:nDCG@5──

在 ViDoRe 上, ColPali-v1 获得了80%的 nDCG@5;在相同文件上,文本-RAG 获得了50%-60%.

> 据报道,该公司的数据显示,该公司的数据量为55%

### 终端到终端的RAG管道

对于视力原生RAG:

> 视觉原生RAG管道:

1. 摄入: PDF → 页面图像 → PaliGemma编码 → 存储所有补丁嵌入式.
   中文翻译:摄取:PDF → 页面图像 → PaliGemma 编码 → 存储所有补丁 嵌入──
2. 查询:用户文本 →查询标志嵌入 → MaxSim对所有索引页面 → top-k页面.
   中文翻译:查询:用户文本 → 查询代币 嵌入 → 对所有索引页面做MaxSim → top-k 页面。
3. 生成:顶级页面图像+查询 → VLM (Qwen2.5-VL或Claude) →答案.
   中文翻译:生成:top-k 页面图像 + 查询 → VLM(Qwen2.5-VL 或 Claude)→ 回答。

没有任何OCR,图形,图形,字体,布局都流入答案.

> 图表,图表,字体,布局全部流入答案.

### 存储数量

财务报告50页,每页有729个补丁,并包含128个维度的嵌入式:

> 金融报告,每页729个补丁,128个维嵌入:

-  ColPali: 50 * 729 * 128 * 4 字节 = ~ 18 MB 原始, PQ 后的 ~ 4 MB.
  中文翻译:ColPali:50 * 729 * 128 * 4 字节 = 约18 MB 原始,PQ 后约4 MB。
- 文字-RAG:50块 * 768-dim * 4字节 = ~150kB.
  中文翻译:文本 RAG:50块 * 768维 * 4字节 = 约150kB。

文件存储量为每份文件的30倍.在规模上,OPQ/PQ将其降至5-10倍,通常是可以容忍的.

> 总体积大约30倍,OPQ/PQ将降至5-10倍,通常可接受.

### 当短信RAG仍然赢得

- 文本文本是简单的,存储成本更低.
  中文翻译:无布局信号的纯文本文档(维基文章、聊天记录) ――文本 RAG 更简单且存储更便宜──
- 存储占据成本的数百万页档案.
  中文翻译:数百万页档案,存储成本占主导地位.
- 严格的监管要求除了检索之外,还需要提取可转录的文本.
  中文翻译:严格要求可提取 OCR 文本与检索并存的监管要求.

其他2026年 财务报告,科学论文,法律合同,医疗记录,UX文档 视觉原生RAG获胜.

> 其他所有场景2026年 金融报告,科学论文,法律合同,医疗记录,UX 文档 视觉原生RAG 胜出.

## 用它实现框架
```figure
mm-maxsim
```

## 用它

`code/main.py`其他:

- 玩具补丁编码器:将"页面" (特征向量小格式) 映射到一个组补丁嵌入式.
  中文翻译:玩具补丁编码器:将"页面" (特征向量小网格)映射为补丁嵌入数组.
-  MaxSim 评分器:计算查询代币嵌入集和页面补丁集之间的ColBERT式评分.
  中文翻译:MaxSim 评分器:计算查询代币 嵌入集和页面补丁集之间的 ColBERT 风格分数──
- 索引5页玩具,执行3个查询,返回最高的K,
  中文翻译:索引 5个玩具页面,运行 3个查询,返回带分数的顶部k――

## 运送它.

这一课产生了`outputs/skill-vision-rag-designer.md`根据文件RAG项目,选择 ColPali / ColQwen2 / VisRAG / text-RAG,并将存储量量量缩小.

> 本课产出发 `outputs/skill-vision-rag-designer.md`△给定文档 RAG 项目,选择 ColPali / ColQwen2 / VisRAG / 文本 RAG 并估算储备──

## 练习题

1. 根据"图库"的数据,每页的数据量为729个补丁,128维的嵌入式,4字节的浮动.计算原始存储和PQ压缩的 (8x) 存储.

2. 马克西姆是 Σ_i max_j cos(q_i, p_j). 这个总和捕捉到什么,而一个简单的平均相似性没有?

3. 利将页面索引为补丁集.如果我们以词级级索引 (如ColBERT) 索引,会怎样改变?有什么取舍?

4. 设计一个1M页的管道,每次查询的延迟预算为500ms. 选择 ColQwen2 / VisRAG,并证明. 设计100万页语料库的端到端管道,每查询延迟预算500ms──选择 ColQwen2 / VisRAG 并论证──

5. 阅读M3DocRAG (arXiv:2411.04952). 描述多页关注模式以及它与单页ColPali检索的区别是如何不同.

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Late interaction | "ColBERT-style" 延迟交互 | Retrieval using per-token or per-patch embeddings + MaxSim, not a single doc vector 使用逐 token/patch 嵌入 + MaxSim 的检索，非单向量 | |
| MaxSim | "Max-over-patches" 最大相似度 | For each query token, pick the highest-similarity document token; sum across query 对每个查询 token 选最高相似度的文档 token；跨查询求和 | |
| Bi-encoder | "Single-vector" 双编码器 | One vector per document; faster but loses granularity 每文档一个向量；更快但丢失粒度 | |
| Multi-vector | "Many-vectors-per-doc" 多向量索引 | Store N_p vectors per document / page; storage cost grows but recall improves 每文档/页存储 N_p 个向量；存储增长但召回提升 | |
| Patch embedding | "Page feature" 图像块嵌入 | One vector per image patch from a VLM encoder, cached per page VLM 编码器输出的每 patch 一个向量，按页缓存 | |
| ViDoRe | "Vision doc bench" 视觉文档检索基准 | ColPali's benchmark suite for visual document retrieval ColPali 的视觉文档检索基准套件 | |
| PQ quantization | "Product quantization" 乘积量化 | Compression that maintains vector similarity while shrinking storage ~8x 保持向量相似度的同时压缩存储约 8 倍 | |

## 继续阅读 继续阅读

- [Faysse et al. — ColPali (arXiv:2407.01449)](https://arxiv.org/abs/2407.01449)
- [Khattab & Zaharia — ColBERT (arXiv:2004.12832)](https://arxiv.org/abs/2004.12832)
- [Yu et al. — VisRAG (arXiv:2410.10594)](https://arxiv.org/abs/2410.10594)
- [Cho et al. — M3DocRAG (arXiv:2411.04952)](https://arxiv.org/abs/2411.04952)
- [illuin-tech/colpali GitHub](https://github.com/illuin-tech/colpali)
