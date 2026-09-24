# 专注于前重量工作负载
# 预写缓存服务  激素注意力和KV重复使用

> 处理KV缓存作为一个在基层树中存储的第一类,可重复使用的资源,并与它一起进行调度变化:而不是FCFS (首次来,首次服务) 作为vLLM时间表,一个缓存知性调度器优先考虑使用更长的共享前置器的请求. 轮是引擎,它围绕着这个想法构建. 在Llama 3.1 8B上,SGLang达到16,200个/秒,达到vLLM的12,500个,占比29%. 在前重的RAG工作负载上,优势达到6.4倍. 在语音克隆式工作负载上,缓存击中率已清除了86%. 在2026年将部署在xAI,LinkedIn,Cursor,Oracle,GCP,Azure,AWS等400,000+个GPU上. 序列是工程师的杆.

> **【中文解读】**本节介绍了SGLang 和 Radix注意力 通过前共享优化推理效率.
**Type:** Learn
**Languages:** Python (stdlib, toy radix-tree cache + cache-aware scheduler)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 14 (Agentic RAG)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy radix-tree cache + cache-aware scheduler) | **语言:** Python（标准库，radix tree 缓存 + 缓存感知调度器模拟）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 14 (Agentic RAG) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 14（Agentic RAG）

>  **【前置】**学本节前请先掌握:阶段17·04(vLLM) 、阶段14(Agentic RAG) ・SGLang 用基因树 复用KV缓存比vLLMFCFS 更智能的调度。
>  **【类比】**拉马 3.1 8B 在 ShareGPT 上比 拉马 快 29%;RAG 工作负载快 6.4 倍;语音克隆场景缓存命中 86%──2026 部署在 40 万+ GPU(xAI、LinkedIn、Cursor) 关键:前必须稳定排序才有效──
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 图表Radix注意:如何在一个基因树中存储前置,以及如何在同一分支根基的序列中共享KV块.
  中文翻译:绘制Radix注意:前如何在Radix树中存储,KV块如何在同分支的序列间共享──
- 解释缓存预示的时间表以及为什么FCFS对预写量较高的流量是错误的.
  中文翻译:解释缓存感知调度以及为什么FCFS对前密集流量是错误的.
- 计算预期工作负载加快,以预先缓存击率和快速长度分布为基础.
  中文翻译:给定前缓存命中率和快速长度分布,计算工作负载的预期加速──
- 给出一个即时订单的纪律,使6.4x数量是真实的,而不是丢失的上.
  中文翻译:说出使6.4x 加速成为现实而非流失的快速排序纪律.

## 问题 问题引入

> **【中文解读】**传统推理服务将每个请求的提示视为不透明 即使5000个RAG请求共享相同的2000代币 系统提示,vLLM也将执行5000次完整的预填.

> **【拓展：前缀共享在 Agent 场景的价值】**工作负载天然具有前共享特征:系统提示、工具方案、少数拍摄示例、对话历史跨请求重复──Cursor(AI代码编辑器) 在2026年报告其 代理调用中系统提示 + 工具定义占即时的80%,仅用户查询部分不同──使用SGLang的RadixAttention 后,这些共享前只需要计算一次,后续请求重复使用KV缓存,将推理成本降低60-80%.──

经典服务处理每个请求的提示是不透明的.即使5000个RAG请求都以相同的2000个代币系统提示加上相同的检索序言开始,vLLM将2000个代币前填写5000次.GPU一遍又一遍.

> 经典服务将每一个请求的快速 视为不透明的.即使有5000个RAG请求都用相同的2000个代币.系统提示加相同的检查前开始,vLLM也会预填充那个2000个代币前5000次.

观察:代理和RAG工作负载中的提示几乎总是共享长个预写.系统提示,工具方案,几次示例,检索标题,对话历史记录 所有请求都重复.如果你一次存储了该预写的KV缓存,然后再使用它,你不会再预写.

> 观察:代理和RAG 工作负载中的提示 几乎总是共享长前──系统提示、工具方案、少数拍照示例、检索头、对话历史都在请求间重复──如果你存储一次前的KV缓存并重复使用,就不需要再次预填──

根源注意力执行了这一点.代币在根源树中被索引;每个节点拥有从根开始的代币序列的KV块.一个新的请求通过树:任何与代币匹配的节点都会重复使用该节点的KV块.预填成本变得与"新"后音相比例,而不是完整提示.

> 基因注意 正是这样做的──在基因树中索引;每个节点拥有从根到路径的符号序列的KV块──新请求遍历树:任何符号匹配的节点复用该节点的KV块──预填成本与"新"后成正比,而不是完整的提示──

挑战是安排.如果两个请求共享2000个代币前,而第三个只共享200个代币,你想将两个长共享的请求一起服务,以便长前保持在HBM中.FCFS做相反的它服务了谁来第一,可能在下一个长前请求碰到之前驱逐热分支.

> 挑战在调度中. 如果两个请求共享2000个代币前,第三只共享200个代币,你希望同时服务两个长共享请求以保持长前在HBM中.

## 概念的核心概念

### 作为KV指数的基底树

> **【中文解读】**基因树 (Radix tree) 是SGLang的核心数据结构.每个节点拥有一个代号. 范围和应对的KV块. 新请求进入时沿树匹配:系统提示匹配节点复用124个KV块,文档分支匹配复用31个块,只需要为新问题分配4-6个块.

基底树 (紧的三角形) 存储代币序列.每个节点拥有代币范围,KV区块为该范围计算.孩子们将序列扩展到一个或多个代币.

> 基因树 (Radix tree) 紧前树) 存储代币序列――每个节点拥有一个代币 范围和为该范围计算的KV块――子节点扩展序列一个或多个代币――

```
root
 |- "You are a helpful assistant..."  (2,000 tokens, 124 KV blocks)
      |- "Context: <doc A>..."        (500 tokens, 31 blocks)
           |- "Question: Alice..."    (80 tokens, 5 blocks)
           |- "Question: Bob..."      (95 tokens, 6 blocks)
      |- "Context: <doc B>..."        (520 tokens, 33 blocks)
```

系统提示+"文本: <doc A>"+"问题: Carol"的新请求. 编程程序运行:系统前匹配 (124个块重复使用),doc-A分支匹配 (31个块重复使用),然后仅为"问题: Carol" (4个块) 分配新块.预填成本: 4个块新代币.没有树: 160 块. ~40倍的预填节省.

> 一个新请求带着系统提示 + "文本: <doc A>" + "问题: Carol" 进入──调度器遍历:系统前匹配(复用124块),doc-A 分支匹配(复用31块),然后只为 "问题: Carol" 分配新块(4块)──预填成本:4块新代币──没有树:160块──预填节省约40倍──

### 缓存预定时间

> **【中文解读】**缓存感知调度的两个关键策略: 1) 深度优先调度优先服务与当前运行集共享分支的请求,保持热点分支常驻HBM; 2) 分支级 LRU 淘汰以整棵分支为单位淘汰从最少使用的叶子开始),而不是单个块.

假如缓存出现故障,Radix树支持的重复使用是无意义的.

> 如果缓存不断动,根树支持的复用毫无意义.

1. **Depth-first dispatch**在排列中选择下一个请求时, 优先选择与当前运行集相同的分支的请求. 这将保持热分支的固定.
   翻译: 中文**深度优先调度**△ 在队列中选择下一个请求时,优先选择与当前运行集和分支的请求.
2. **LRU at branch level, not block level**消除整个分支 (从最短使用的叶子开始),而不是单个块,以便缓存形状与基底形状相匹配.
   翻译: 中文**分支级 LRU**淘汰整个分支 (从最少使用的叶子开始),而不是单个块,使缓存形状匹配根形状

要求共享2000个代币,是50个代币的请求背后,然后2000个代币的分支被驱逐出境,

> 后面,2000个代币分支被淘汰,以接受50个代币的请求.

### 您应该记住的基准号码

- 拉马 3.1 8B,H100,ShareGPT 1K提示:SGLang ~16,200个时/秒对VLLM ~12,500 (~29%的边缘).
  中文翻译:Llama 3.1 8B,H100,ShareGPT 1K提示:SGLang 约 16,200 /秒对 vLLM 约 12,500(约 29% 优势) 。
- 预写重的RAG (相同的系统 +相同的文件,不同的问题):在SGLang上高达6.4x.
  中文翻译:前密集 RAG(同系统 + 相同文档,不同问题):SGLang 上最高6.4倍。
- 语音克隆工作量:前置缓存击中率为86.4%.
  中文翻译:语音克隆工作负载:86.4% 前缓存命中中率──
- 产量打击率在SGLang客户中:50-99%取决于迅速的纪律.
  中文翻译:SGLang 客户的生产命中率:50-99%,取决于快速排序纪律.
- 在2026年将部署在400,000+的GPU上.
  中文翻译:2026年部署在400,000+GPU上.

### 订单给你了

> **【中文解读】**6.4x 速度依赖于一致的提示模板排序.`[system, tools, context, history, question]`有时构建`[system, context, tools, history, question]`根树 无法找到共享前 对人类看起来相同的提示,对根树是两个不同的序列.工程师的关键杆是:将提示模板视为缓存键.将不可变内容.

> **【拓展：SGLang 在生产中的采用】**2026年,SGLang已经部署了超过40万块GPU,用户包括xAI (Grok) 、LinkedIn、Cursor、Oracle,以及GCP/Azure/AWS的托管服务――核心优势场景是代理和RAG工作负载 这些场景中系统提示和工具定义重复率极高――SGLang 团队由UC Berkeley LMSYS (Chatbot Arena的创始人) 组成,与vLLM 团队密切合作――两者不是严格的竞争关系vLLM也在2026年增加了预写缓存功能――

如果您的客户端构建提示如`[system, tools, context, history, question]`在某些请求中,`[system, context, tools, history, question]`树木不能找到一个共同的前. 树木的两个不同的序列,

> 6.4x 数字依赖于一致的提示 模板排序.`[system, tools, context, history, question]`在其他请求中构建`[system, context, tools, history, question]`树不能找到共享前──对人类看起来是共享前的,对树根则是两条不同的序列──

工程师的杆:您的提示模板是一个缓存键. 修复顺序. 首先把不可变的东西 (系统,工具,方案) 放在第一位. 接下来放回文本. 排名用户问题. 不要把动态内容插入预写中.

> 工程师的杆:你的提示 模板是缓存键――固定序列――将所有不可变内容――系统、工具、方案) 放最前――检索上下文放中间――用户问题放最后――不要在可缓存前中交错动态内容――

实际情况:从可缓存的前中移动动动态内容,在一个变化中,从7%到74%的缓存击中率.

> 研究中的真实案例:将动态内容移动到可缓存前,一次部署缓存预期率从7%升至74%

### 雷迪克斯注意力赢得和输掉的地方

> **【拓展：RadixAttention vs Prefix Caching 性能对比】**在Llama 3.1 8B H100上,通用ShareGPT工作负载中,SGLang 达到~16,200 tok/s vs vLLM ~12,500 tok/s;;29%的优势;在重度前重复使用RAG工作负载中优势可达6.4x;语音克隆工作负载缓存命中率为86%的.但 vLLM 在2026年也将添加预设缓存和缓存意识路由器.

获奖:
- 总结:
  中文翻译:RAG(同样的检索前,不同问题) 』
- 代理 (相同的工具方案,不同的查询).
  中文翻译:代理 (同样工具方案,不同查询) 』
- 聊天长系统提示.
  中文翻译:长系统提示的聊天.
- 语音/视觉工作负载,重复序言.
  中文翻译:重复前的语音/视觉工作负载。

输出 (返回vLLM级输出):
- 单次生成,具有独特的提示 (编码完成,无系统提示的开放式聊天).
  中文翻译:独立提示的单次生成 ((代码补全、无系统提示的开放聊天) ⋅
- 动态提示,每个请求都将独特的内容插入预सर्ग中.
  中文翻译:每个请求在可缓存前中交错独特内容的动态提示──

### 为什么这是一个调度器问题,而不是一个核心问题

您可以将KV重复使用作为一个内核技巧.SGLang的见解是,重复使用只会付出,如果调节器保持热分支居民.一个天真的"如果可用"政策将在混合负载下乱缓存. 基因树索引调度器是使内核技巧成为29%的生产边缘.

> 简单的"有则复用"策略在混合负载下会动缓存――根树索引的调度器将内核技术转化为29%的生产优势――

### 与vLLM相互作用

两种系统并非严格的竞争对手.`--enable-prefix-caching`                                                                                                                                                                                                                                                              

> 两系统不是严格竞争者.`--enable-prefix-caching`对于前复用主导工作负载,SGLang 仍然是默认选择.对于没有强前模式的通用服务,vLLM 仍然相当或更好.

## 用它实现框架
```figure
roofline
```

## 用它

`code/main.py`运行相同的工作负载通过两个,报告预先缓存击率和吞吐量德尔塔.然后运行一个"缩订"工作负载显示6.4x崩.

> `code/main.py`实现模拟基因树 KV 缓存加两个策略调度器:FCFS 和缓存感知――用两者运行相同工作负载,报告前缓存命中率和吞吐量差异――然后运行"乱序排序"工作负载展示 6.4x 崩――

## 运送它.

> **【拓展：前缀缓存策略选择】**2026年前缓存有三个层次: 1) 应用级语义缓存(17·14期) 在调用LLM前用嵌入相似度匹配历史响应,命中率10%-70%; 2) 服务端前缓存(SGLang RadixAttention / vLLM前缓存) 重用KV缓存,10x 延迟降低; 3) 跨节点缓存路由(17·11期) 通过缓存意识路由器将请求路由通过缓存保持前的副本.

这一课产生了`outputs/skill-radix-scheduler-advisor.md`鉴于工作负载描述 (即时模板形状,检索模式,同时租户数量),它产生了即时订单的处方和SGLang采用的无需处方.

> 本课产出发 `outputs/skill-radix-scheduler-advisor.md`△给定工作负载描述(快速 模板形状、检索模式、并发租户数),它生成快速 排序处方和SGLang 采用的走/不走建议。

## 练习题

1. 跑步`code/main.py`根据FCFS和缓存意识的相同工作负载进行比较. 预填储蓄,解码储蓄或排队延迟的达尔塔来自哪里?
   中文翻译:运行 `code/main.py`△在相同工作负载上与FCFS和缓存感知相比.
2. 修改工作负载,让提示随机转移`[system, tools, context]`什么会发生在撞击率?
   中文翻译:修改工作负载使快速随机排列`[system, tools, context]`运行 命运率发生了什么变化?为什么?
3. 计算HBM的成本,以将2000个代币系统提示居民作为一个基底分支在Llama 3.1 8B上. 与没有预写重复使用的16个序列批次的成本进行比较.
   中文翻译:计算在Llama 3.1 8B 上保持2000个代币 系统提示作为一个根分支常驻的HBM 成本──与无前复用16个序列批次成本比较──
4. 阅读SGLang RadixAttention论文. 用三句话解释为什么树状LRU驱逐器在前重负载下比块状LRU更好.
   中文翻译:阅读 SGLang RadixAttention 论文──用三句话解释为什么树形LRU 淘汰在前密集负载下优于块形LRU──
5. 给出三个可能的原因和你会为每一个用户进行的诊断.
   中文翻译:客户报告只有8% 缓存命中率.

## 关键词 快速查找表

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| RadixAttention | "the SGLang thing" / "SGLang 的那个" | KV cache indexed as a radix tree so shared prefixes reuse blocks / KV 缓存以 radix tree 索引，共享前缀复用块 |
| Radix tree | "compact trie" / "紧凑前缀树" | Tree where each node owns a token range and its KV blocks / 每个节点拥有 token 范围和 KV 块的树 |
| Cache-aware scheduler | "hot-branch-first" / "热分支优先" | Scheduler that prefers requests sharing the resident branch / 优先服务共享常驻分支请求的调度器 |
| Prefix-cache hit rate | "how much of your prompt was free" / "prompt 多少是免费的" | Fraction of prompt tokens served from reused KV blocks / 从复用 KV 块服务的 prompt token 比例 |
| FCFS | "first-come first-served" / "先来先服务" | Default scheduling that breaks prefix locality / 破坏前缀局部性的默认调度 |
| Branch-level LRU | "evict the leaf" / "淘汰叶子" | Eviction policy matched to radix shape / 匹配 radix 形状的淘汰策略 |
| Prompt template ordering | "the cache key" / "缓存键" | The prompt's component order determines what the tree can share / prompt 组件顺序决定树能共享什么 |
| System prompt pinning | "resident prefix" / "常驻前缀" | Keep the immutable system portion pinned to avoid eviction thrash / 保持不可变系统部分固定避免淘汰抖动 |

## 继续阅读 继续阅读

- [SGLang GitHub](https://github.com/sgl-project/sglang)来源和文件.
- [SGLang documentation](https://sgl-project.github.io/)                                                                                                                                                                                                                                                              
- [SGLang paper — Efficiently Programming Large Language Models (arXiv:2312.07104)](https://arxiv.org/abs/2312.07104)设计参考.
- [LMSYS blog — SGLang with RadixAttention](https://www.lmsys.org/blog/2024-01-17-sglang/)基准数字和时间表理性.
- [vLLM — Prefix Caching](https://docs.vllm.ai/en/latest/features/prefix_caching.html) vLLM自己的基像实施,比较.
