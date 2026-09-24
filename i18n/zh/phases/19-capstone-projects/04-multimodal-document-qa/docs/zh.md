# 卡普斯通 04 多模文件QA (视觉第一PDF,表表,图表) 官网

> 2026年,文件-QA界限从OCR转移到视觉-第一的后期互动.  ColPali, ColQwen2.5 和 ColQwen3-omni将每个 PDF 页面视为图像,将其嵌入多向量迟交互, 在金融10K,科学论文和手写的笔记上, 建立一个终端的管道,在10万页,并将其发布一边对抗OCR-then-text.

> **【中文解读】**本节是综合项目构建多模态文档问答系统,处理文本、图像和表格.


**Type:** Capstone | **类型:** 综合项目
**Languages:** Python (pipeline), TypeScript (viewer UI) | **语言:** Python（管道）, TypeScript（查看器 UI）
**Prerequisites:** Phase 4 (computer vision), Phase 5 (NLP), Phase 7 (transformers), Phase 11 (LLM engineering), Phase 12 (multimodal), Phase 17 (infrastructure)

>  **【前置】**顶点项目 04 = 综合阶段 4/5/7/11/12/17──文档 QA 走视觉优先(ColPali 风格,参考阶段 12·23)──
>  **【类比】**文档 QA = "PDF 直接看"──2026 前沿:从"OCR→文本"转向"视觉优先 + 延迟交互"(ColPali/ColQwen2.5/ColQwen3-omni)──把 PDF 页面当图像,多向量嵌入,查询 直接关注补丁──在金融 10-K、科学论文、手写笔记上大幅胜利 OCR 方案──**前置知识:**工程阶段第1 (多模态) 基础设施
**Phases exercised:**现在,我们在这个世界里,**涉及阶段:**子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子
**Time:** 30 hours | **时间:** 30 小时

## 问题 问题引入

> **【中文解读】**本节阐述文档问答从"先OCR 再文本"到"视觉优先"范式转变――企业PDF中旋转表格、公式、图片、手写批注是OCR管道的梦――2026年答案是ColPali/ColQwen系列的晚期交互多向量检查将将每页 PDF当成图像,让查询直接关注图像块 (图片块) 补丁.

> **【拓展：视觉文档检索前沿】**通过50%的剪枝将存储减半,精度损失 <0.5%──VSim 和 Qespa 干部都支持多向量字段和Max 检索──

企业使用OCR管道破碎的PDF文件:扫描10K的轮换表, 让这些信息成为第一条短信意味着失去一半的信号. 2026年答案是在原始页面图像上进行迟到互动的多向量检索. 科尔帕利 (伊利科技) 推出了它;科尔2.5v0.2和科尔3omni推进了精度. 在 ViDoRe v3 中,视觉首先检索的分数比OCR然后是文字高出了有意义的边缘,图表,表格和手写的差距扩大.

> 企业拥有大量的OCR管道无法正确处理的PDF:带旋转表格扫描 10-K 报告、充满公式的科学论文、只有作为图像才有意义的图像、手写批量──将这些视为文本优先意味着丢失一半信号──2026年答案是对原始页面图像进行晚期交互多向量检查──ColQwen2.5v0.2 和ColQ3-omni 推动精度──在ViDoRe v3上,视觉优先检查显著优势超过OCR手写文字差距图表,表格和内容写作中更大────

交换是存储和延迟.一个 ColQwen 嵌入式是每页的 ~2048个补丁向量,而不是单个1024维度向量.原料存储气球.docPruner (2026) 带来50%的剪裁,没有可测量的精度损失.您将索引10k页面,测量ViDoRe v3 nDCG@5,提供2秒以下的答案,并直接与OCR然后文本基线进行比较.

> 代价是存储和延迟──ColQwen 嵌入式是每页约2048个补丁向量,而不是单个1024个维向量──原始存储膨胀──DocPruner(2026) 在不损失可测量精度的情况下实现50% 剪枝──你将索引1万页,测量ViDoRe v3 nDCG@5,在2秒内提供答案,并直接与OCR-then-text 基线比较──

## 概念的核心概念

> **【中文解读】**晚期交互 (晚间交互) 指每个查询代币与每个页面补丁代币 独立计算相似性,取每个查询代币的最大分数后求和和――这比单单池化向量匹配更精细――多向量索引(Vespa/Qdrant/AstraDB) 存储每个页面的补丁 嵌入和检查时执行MaxSim──答案生成使用视觉语言模型(Qwen3-VL-30B/Gemini 2.5 Pro),带证据区域定位和码引用页面――

> **【拓展：多模态 VLM 选型】**2026年文档问答 主流 VLM 包括:Qwen3-VL-30B(自托管最优) 、Gemini 2.5 Pro(API 调用最优)、InternVL3(开源备选) ・・・对于公式密集页面,Nougat OCR 作为补充文本通道──评估采用二维矩阵:横轴内容类型(文段落/密集表格/图表/手写/公式),纵轴检索方法视觉优先/OCR-then-text/混合),每个单元格计算 nDCG@5 和答案准确率──

晚交互意味着每个查询代币对每个补丁代币进行分数,每个查询代币的最大分数被总和.你得到了细粒度匹配,而不需要单个聚合向量.一个多向量指数 (Vespa,Qdrant多向量,或AstraDB) 存储每个补丁嵌入式,并在检索时运行MaxSim.

> 晚期交互意味着每个查询代币和每个补丁代币 计算分数,每个查询代币最大分数被要求和――你得到精细匹配而不需要单个池化向量――多向量索引(Vespa、Qdrant多向量或AstraDB) 存储每个补丁的嵌入并检查时运行MaxSim――

答案器是一个视觉语言模型,将查询加上上-k获取的页面作为图像,并用证据区域 (边框或页面引用) 写出答案.Qwen3-VL-30B,Gemini 2.5 Pro和InternVL3是2026年边界选择.对于方程和科学符号,OCR倒退 (Nougat,dots.ocr) 是作为可选的文本频道.

> 回答器是一个视觉语言模型,接收查询加上顶-k检索页面作为图像,并写出带证据区域 (图片) 问题答案.

评估是一个二维矩阵.一个轴:内容类型 (平文段,密集表,条/行图,手写笔记,方程).另一个轴:检索方法 (视觉-第一晚交互与OCR-然后-文字对混合).每个细胞得到nDCG@5和答案准确性.报告是可交付的.

> 评估是一个二维矩阵――一个轴:内容类型(纯文本段落、密集表格、条形/折线图、手写笔记、公式) ――另一个轴:检索方法(视觉优先晚期交互 vs OCR-then-text vs 混合) ――每个单元格获得nDCG@5 和答案准确率――报告是交付物物――

## 建筑,建筑

```
PDFs -> page renderer (PyMuPDF, 180 DPI)
           |
           v
  ColQwen2.5-v0.2 embed (multi-vector per page, ~2048 patches)
           |
           +------> DocPruner 50% compression
           |
           v
   multi-vector index (Vespa or Qdrant multi-vector)
           |
query ----+----> retrieve top-k pages (MaxSim)
           |
           v
  VLM answerer: Qwen3-VL-30B | Gemini 2.5 Pro | InternVL3
    inputs: query + top-k page images + optional OCR text
           |
           v
  answer with cited page numbers + evidence regions
           |
           v
  Streamlit / Next.js viewer: highlighted boxes on source page
```

##  技术

- 页面染:PyMuPDF (fitz) 180 DPI,肖像正常化
  中文翻译:页面转载:PyMuPDF (fitz) 180 DPI,肖像正常化
- 后期交互模型:ColQwen2.5-v0.2或ColQwen3-omni (在拥抱面上的视频团队)
  中文翻译:后期互动模型:ColQwen2.5-v0.2或ColQwen3-omni (在拥抱面部的视频团队)

> 中文翻译:后期互动模型:ColQwen2.5-v0.2或ColQwen3-omni (在拥抱面部的视频团队)

- 索引:Vespa与多向量场,或Qdrant多向量,或AstraDB与MaxSim
  中文翻译:索引:Vespa与多向量场,或Qdrant多向量,或AstraDB与MaxSim
- 切割: DocPruner 2026 政策 (保持高变量补丁,50%的压缩在<0.5%的精度损失)
  中文翻译:运行: DocPruner 2026 政策 (保持高变量补丁,50%的压缩在<0.5%的准确性损失)
- 转移 (方程/密集表):dots.ocr或Nougat
  中文翻译:OCR倒退 (方程 / 密集表):点.ocr或Nougat
- 维LM响应器:Qwen3-VL-30B自主托管或双子 2.5 Pro托管;InternVL3作为倒退
  中文翻译:VLM回复器:Qwen3-VL-30B自主托管或双子 2.5 Pro托管;InternVL3作为倒退

> 中文翻译:VLM回复器:Qwen3-VL-30B自主托管或双子 2.5 Pro托管;InternVL3作为倒退(翻译)

- 评估:ViDoRe v3基准,M3DocVQA用于多页推理
  中文翻译:评估:ViDoRe v3基准,M3DocVQA用于多页推理
- 浏览器UI: Next.js 15 具有证据区域的帆布覆盖
  中文翻译:视频用户界面: Next.js 15 面膜覆盖证据区域

## 动手构建

> **【中文解读】**构建步骤分为8个阶段:摄取10k页 PDF并染为PNG、ColQwen2.5 嵌入(每页 ~2048个补丁,dim 128) 并应用DocPruner50%压缩、MaxSim 检查顶-k页、VLM 答案合成带引用、证据区域提取与可视化、OCR 回退通道(公式密集页)、ViDoRe v3 + M3DocVQA 评估、Streamlit/Next.js 查看器──
```figure
ce-late-interaction
```

## 建立它

1. **Ingest.**通过10万页的PDF文件,科学论文和扫描文件进行散步.将每个页面呈现为1536x2048 PNG. 坚持`{doc_id, page_num, image_path}`现在,我们要去.
   中文翻译:1. **Ingest.**通过10万页的PDF文件,科学论文和扫描文件进行散步.将每个页面呈现为1536x2048 PNG. 坚持`{doc_id, page_num, image_path}`现在,我们要去.

2. **Embed.**在每个页面图像上运行ColQwen2.5-v0.2.输出形状 ~2048 补丁嵌入式的低128.应用 DocPruner 保持最高信号半.写到Vespa 多向量场或Qdrant 多向量.
   翻译: 翻译:**Embed.**在每个页面图像上运行ColQwen2.5-v0.2.输出形状 ~2048 补丁嵌入式的低128.应用 DocPruner 保持最高信号半.写到Vespa 多向量场或Qdrant 多向量.

3. **Query.**对于每一个接入查询,嵌入查询塔 (代币级嵌入). 运行MaxSim对索引:对于每一个查询代币,取 max dot-产品在页面补丁嵌入,总和.返回顶级k页面.
   翻译: 翻译:**Query.**对于每一个接入查询,嵌入查询塔 (代币级嵌入). 运行MaxSim对索引:对于每一个查询代币,取 max dot-产品在页面补丁嵌入,总和.返回顶级k页面.

4. **Synthesize.**随着查询和前5页面图像,请调用Qwen3-VL-30B. 提示:"只使用提供的页面回答.以 (doc_id,页面) 引用每个索赔,并命名区域 (图,表,段落)."
   翻译: 翻译:**Synthesize.**随着查询和前5页面图像,请调用Qwen3-VL-30B. 提示:"只使用提供的页面回答.以 (doc_id,页面) 引用每个索赔,并命名区域 (图,表,段落)."

5. **Evidence regions.**如果VLM发射边框 (Qwen3-VL是这样的),将它们作为观众中的叠加.
   翻译: 五.**Evidence regions.**如果VLM发射边框 (Qwen3-VL是这样的),将它们作为观众中的叠加.

6. **OCR fallback.**对于被确定为方程密度 (图像变异的论) 的页面,运行Nougat或dots.ocr,并将OCR文本作为图像旁边的额外频道.
   翻译: 七个字**OCR fallback.**对于被确定为方程密度 (图像变异的论) 的页面,运行Nougat或dots.ocr,并将OCR文本作为图像旁边的额外频道.

7. **Eval.**运行 ViDoRe v3 (检索 nDCG@5) 和 M3DocVQA (多页QA精度).同时运行同一个合成器的OCR-then-text管道.生成内容类型x方法矩阵.
   翻译:7.**Eval.**运行 ViDoRe v3 (检索 nDCG@5) 和 M3DocVQA (多页QA精度).同时运行同一个合成器的OCR-then-text管道.生成内容类型x方法矩阵.

8. **UI.**首先是流光原型; Next.js 15 制作观看器,面对面的证据区域覆盖.
   翻译:8.**UI.**首先是流光原型; Next.js 15 制作观看器,面对面的证据区域覆盖.

## 用它使用方法

```
$ doc-qa ask "what was the 2024 operating margin change for segment EMEA?"
[retrieve]   top-5 pages in 320ms (ColQwen2.5, MaxSim, Vespa)
[synth]      qwen3-vl-30b, 1.4s, cited (form-10k-2024, p. 88) + (..., p. 92)
answer:
  EMEA operating margin moved from 18.2% to 16.8%, a 140bp decline.
  cited: 10-K-2024.pdf p.88 (Table 4, Segment Operating Margin)
         10-K-2024.pdf p.92 (MD&A, Operating Performance)
[viewer]     open with highlighted bounding boxes overlaid on p.88 Table 4
```

## 发射上线

`outputs/skill-doc-qa.md`描述可交付的产品:一个视觉先多模文件QA系统,调整到特定的体积,并与ViDoRe v3的OCR然后文本基线进行评估.

> `outputs/skill-doc-qa.md`描述交付物件:根据特定语料库调优的视觉优先多模态文档QA系统,在 ViDoRe v3 上与OCR-then-text基线对比评估.

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | ViDoRe v3 / M3DocVQA accuracy | Benchmark numbers vs OCR-text baseline and published leaderboard |
| 25 | ViDoRe v3 / M3DocVQA 准确率 | 基准数字 vs OCR-text 基线和已发布排行榜 |
| 20 | Evidence-region grounding | Fraction of cited regions that actually contain the answer span |
| 20 | 证据区域定位 | 引用区域中实际包含答案跨度的比例 |
| 20 | Storage and latency engineering | DocPruner compression ratio, index p95, answer p95 |
| 20 | 存储与延迟工程 | DocPruner 压缩比、索引 p95、答案 p95 |
| 20 | Multi-page reasoning | Accuracy on a hand-labeled 100-question multi-page set |
| 20 | 多页推理 | 手工标注的 100 题多页集合上的准确率 |
| 15 | Source-inspection UX | Viewer clarity, overlay fidelity, side-by-side comparison tools |
| 15 | 源文档查看体验 | 查看器清晰度、覆盖层保真度、并排比较工具 |
| **100** | | |

## 练习题

1. 在同一体积上测量ColQwen2.5-v0.2vsColQwen3-omni.哪些页面一个是正确的,另一个是错误的?添加一个"内容类"标签到索引中以按类型进行路由.
   中文翻译:在同一语料库测量 ColQwen2.5v0.2 vs ColQwen3-omni──哪个在某些页面上正确而另一个遗漏?向索引添加"内容类别"标签按类型路由──

> 中文翻译:在同一语料库上测量 ColQwen2.5v0.2 vs ColQwen3-omni──哪个在某些页面上正确而另一个遗漏?向索引添加"内容类别"标签按类型路由──(翻译)


2. 除嵌的方法 (75%, 90%). 找到压缩悬崖: ViDoRe nDCG@5 落在OCR基线以下的地方.
   中文翻译:激进剪枝嵌入(75%、90%)──找到压缩悬崖:ViDoRe nDCG@5 降至OCR基线以下的点──

3. 构建一个混合动力:并行运行OCR-then-text和ColQwen,并并并并与RRF,再使用一个跨编码器.混合动力单独打败了任何一个?它最有帮助的地方?
   中文翻译:构建混合方案:并行运行 OCR-then-text 和 ColQwen,使用 RRF 融合,使用交叉编码器重排序.混合方案是否胜过单独使用?在哪里帮助最大?

> 中文翻译:构建混合方案:并行运行 OCR-then-text 和 ColQwen,使用 RRF 融合,使用交叉编码器重排序.混合方案是否胜过单独使用?在哪里帮助最大?


4. 换取一个较小的VLM (Qwen2.5-VL-7B) 的Qwen3-VL-30B. 测量每美元的精度曲线.
   中文翻译:将 Qwen3-VL-30B 换为更小的 VLM(Qwen2.5-VL-7B) 』测量每美元准确率曲线──

5. 添加手写笔记支持. 递交手写体,嵌入ColQwen,测量检索. 与手写OCR管道进行比较.
   中文翻译:添加手写笔记支持──染手写语料库,用ColQwen 嵌入,测量检索──与手写 OCR管道对比──

## 关键词 快速查找表

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| Late interaction | "ColPali-style retrieval" | Query tokens score against page patches independently; MaxSim aggregates |
| 晚期交互 | "ColPali 风格检索" | 查询 token 独立于页面 patch 计分；MaxSim 聚合 |
| Multi-vector | "Per-patch embedding" | Each document has many vectors, not one pooled vector |
| 多向量 | "每个 patch 的嵌入" | 每个文档有多个向量，而不是一个池化向量 |
| MaxSim | "Late-interaction scoring" | For every query token, take max similarity over document vectors; sum |
| MaxSim | "晚期交互评分" | 对每个查询 token，取文档向量上的最大相似度；求和 |
| DocPruner | "Patch compression" | 2026 pruning that keeps 50% of patches with negligible accuracy loss |
| DocPruner | "Patch 压缩" | 2026 年剪枝，保留 50% 的 patch，精度损失可忽略 |
| ViDoRe v3 | "Document-retrieval benchmark" | The 2026 standard for measuring visual-document retrieval |
| ViDoRe v3 | "文档检索基准" | 2026 年测量视觉文档检索的标准 |
| Evidence region | "Cited bounding box" | A bbox on the source page that localizes the answer span |
| 证据区域 | "引用边界框" | 源页面上定位答案跨度的边界框 |
| OCR fallback | "Equation channel" | Text pipeline used alongside vision for equation- or table-heavy pages |
| OCR 回退 | "公式通道" | 在公式或表格密集页面与视觉并用的文本管道 |

## 继续阅读 继续阅读

- [ColPali (Illuin Tech) repository](https://github.com/illuin-tech/colpali) 参考后期交互文件检索
  中文翻译:参考晚期交互文档检索
- [ColPali paper (arXiv:2407.01449)](https://arxiv.org/abs/2407.01449)基础方法论文
  中文翻译:基础方法论文
- [ColQwen family on Hugging Face](https://huggingface.co/vidore)生产准备的检查站
  中文翻译:生产就绪的检查点
- [M3DocRAG (Adobe)](https://arxiv.org/abs/2411.04952)多页多模拟RAG基线
  中文翻译:多页多模态 RAG 基线
- [Vespa multi-vector tutorial](https://docs.vespa.ai/en/colpali.html)参考服务堆
  中文翻译:参考服务
- [Qdrant multi-vector support](https://qdrant.tech/documentation/concepts/vectors/#multivectors)替代指数
  中文翻译:备选索引
- [AstraDB multi-vector](https://docs.datastax.com/en/astra-db-serverless/databases/vector-search.html)替代管理指数
  中文翻译:备选托管索引
- [Nougat OCR](https://github.com/facebookresearch/nougat)可方程的OCR倒退
  中文翻译:支持公式的OCR 回退
