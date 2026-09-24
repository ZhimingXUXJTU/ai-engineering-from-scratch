# 卡普斯通2 RAG 通过代码基础 (跨度回应语义搜索)

> 每一个认真的工程机构在2026年都会进行内部代码搜索, 源图扩展器,Cursor的代码基础答案, Augment的企业图,Aider的重绘图,Pinterest的内部MCP 相同的形状. 取许多回复,用树分析,嵌入函数和类级分类,混合搜索,重新排名,回答引用. 这块顶石要求你构建一个处理2万行代码的代码,

> **【中文解读】**本节是综合项目构建代码库RAG系统,实现代码语义搜索和检索增强生成


**Type:** Capstone | **类型:** 综合项目
**Languages:** Python (ingestion), TypeScript (API + UI) | **语言:** Python（摄取）, TypeScript（API + UI）
**Prerequisites:** Phase 5 (NLP foundations), Phase 7 (transformers), Phase 11 (LLM engineering), Phase 13 (tools), Phase 17 (infrastructure)

>  **【前置】**顶点项目 02 = 综合阶段 5/7/11/13/17──代码库 RAG = 2026 工程组织标配(Sourcegraph/Cursor/Augment/Aider/Pinterest 都在做)──
>  **【类比】**代码 RAG = "Google for 你的代码"――流程:tree-sitter 解析→函数/类级块→embedding→混合搜索→rerank→带引用答案。本课要求处理2M 行/10 仓库,且每次按点 增量重索引。难点:大型单元的块 边界(按 AST而非行号) 、增量索引的版本一致性。**前置知识:**基础), 转型器, 11 阶段, 13 阶段,工具, 17 阶段
**Phases exercised:**五,七,十一,十三,十七**涉及阶段:**五·七·十一·十三·十七
**Time:** 30 hours | **时间:** 30 小时

## 问题 问题引入

> **【中文解读】**本节阐述代码检索增强生成 (RAG) 的核心痛点――即使克劳德拥有100万代币的上下文窗口,也无法解决跨仓库语义搜索问题需要排序检索――朴素弦搜索在生成代码、monorepo 重复和长尾符号上效果极差――生产级方案是混合搜索(密向量 + BM25),基于AST 感知的分块和重排序,并依赖符号引用图――

> **【拓展：代码搜索的产业实践】**源图 Amp、Cursor Codebase答案、增强企业图等产品在2026年都采用类似架构──Pinterest 内部构建了MCP 搜索服务,助手使用重建地图做树座视图──关键指标包括MRR@10 ((前10 结果的倒数排名平均值) 引用忠诚度 (答案中可验证声明比例) 和增量索引延迟 ((万从推到可搜索时间) ⋅对于200行代码的仓库舰队,增量重量索引需要60秒内完成──

到2026年,每个边境编码代理都将运输一个代码基础检索层,因为单独的语境窗口无法解决跨度问题. 克劳德的1M代币背景有助于;它并没有消除排名检索的需要. 简单的搜索原始的毒品, 结果是生成代码, 单体复制, 生产答案是通过重新排名的AST意识的块进行混合 (密度+BM25) 搜索,支持符号引用图.

> 到2026年,每个前沿编码代理都带着代码库检查层,因为单独的上下文窗口无法解决跨仓库问题――克劳德的上下文100万代币有帮助;但它不能消除对排序检查的需求――在原始分块上的简单弦搜索将在生成代码、monorepo 重复和很少导入的符号长尾上污染的结果――生产答案是混合的密 + BM25) 搜索,基于AST 感知的分块和重排器,由符号引用支持――

通过索引一个真正的机队,而不是一个教程 repo,测量MRR@10,引用忠诚度和增量新鲜度来学习这一点. 失败模式是基础设施的:一个100k文件单元 repo,一个重复一半文件的推力,一个需要跨越四个 repos才能正确回答.

> 你通过索引真实仓库舰队来学习而不是一个教程仓库并测量MRR@10、引用忠诚度和增量新鲜度──失败模式是基础设施层面的:一个10万文件的单独,一个重新触及一半文件的推动──一个需要跨越四个仓库才能正确回答查询──

## 概念的核心概念

> **【中文解读】**核心概念是AST 感知的摄取管道:用树座器解析代码,在函数/类边界分块中 (而不是固定代币窗口中) 设置.每个分块生成三种表示:密嵌入 (密嵌入) 旅行代码-3)  BM25 稀疏索引,自然语言摘要.检索采用混合搜索+交叉编码器重排,最终由长上下文模型生成带引用的答案.增量索引只重嵌变分块,保持索引用于大仓库的实时性.

> **【拓展：向量数据库选型】**2026年主流选择:Qdrant 1.12 支持原生混合搜索,适合中等规模(<5000万向量);pgvector + pgvector scale 适合已有的 PostgreSQL 基础设施团队;Vespa 支持多向量字段和 MaxSim,适合文档级检索――嵌入模型方面,Voyage-code-3 在代码检索上领先,名字嵌入码-v1.5 是自托管首选――重排序模型 Cohere rerank-3 或 bge-reranker-v2-ma-2b 可提升 10-20%──

基于AST的摄入管道通过树座仪分析每个文件,提取函数和类节点,并将节点的块放在节点边界而不是固定的代币窗口. 每个部分都得到了三个表示:密集嵌入 (旅行代码-3或名字嵌入代码),稀缺的BM25术语,以及简短的自然语言摘要. 总结中添加了第三种可检索的模式用户问"X是如何授权的"总结中提到"authz",即使代码只有`check_permission`现在,我们要去.

> 感知摄取管道使用树座器解析每个文件,提取函数和类节点,并节点边界而不是固定代币 窗口处分块。每个分块获得三种表示:密嵌入(旅行代码-3或名字嵌入代码) 稀疏 BM25 术语和简短的自然语言摘要──摘要增加了第三种可检查模态用户"X 如何授权",摘要提到"authz",即使代码只有`check_permission`,我知道.

复苏是混合物. 一个查询会发射密集和BM25搜索,并合并top-k,并将联盟交给一个跨编码重新排名器 (Cohere重排-3或bge-重排-v2-gemma-2b). 重新排名的列表将被转移到长文本合成器 (Claude Sonnet 4.7 与快速缓存,或Llama 3.3 70B自主托管) 没有引用的答案被后过所拒绝.

> 检索是混合的. 查询同时触发密和BM25 搜索,合并 top-k,并将并集交交交交叉编码器重排器.

增长新鲜性是基础设施问题. Git 推进会引发差异:哪些文件改变,哪些符号改变.只有受影响的块重新嵌入.受影响的跨文件符号边缘 (进口,方法调用) 重新计算.索引保持一致,不需要重新处理2M行.

> 增量新鲜度是基础设施问题. 推进 触发差异:哪些文件变化,哪些符号变化.

## 建筑,建筑

```
git push --> webhook --> ingest worker (LlamaIndex Workflow)
                           |
                           v
             tree-sitter parse + AST chunk
                           |
            +--------------+----------------+
            v              v                v
          dense        BM25 index       summary (LLM)
        (Voyage / bge)  (Tantivy)        (Haiku 4.5)
            |              |                |
            +------> Qdrant / pgvector <----+
                            |
                            v
                      symbol graph (Neo4j / kuzu)
                            |
  query --> LangGraph agent (retrieve -> rerank -> synth)
                            |
                            v
                 Claude Sonnet 4.7 1M context
                            |
                            v
                 answer + file:line citations
```

##  技术

- 解析:有17种语言语法的树守 (Python,TS,Rust,Go,Java,C++等)
  中文翻译:Parsing:有17种语言语法的树守 (Python,TS,Rust,Go,Java,C++,等)

> 中文翻译:Parsing:有17种语言语法的树守 (Python,TS,Rust,Go,Java,C++,等)

- 密集嵌入式: Voyage-code-3 (托管) 或名式嵌入式代码-v1.5 (自主托管), bge-code-v1倒退
  中文翻译:密集嵌入:旅行代码-3 (托管) 或名字嵌入代码-v1.5 (自主托管),bge代码-v1倒退

> 中文翻译:密集嵌入式: Voyage-code-3 (托管) 或名字嵌入式代码-v1.5 (自主托管), bge-code-v1 fallback(翻译)

- 率指数:与BM25F的性 (性),按符号名称与体格进行田径权重
  中文翻译:率指数:与BM25F的率 (Rust),按符号名字和体格进行字段权重
- 矢量DB:Qdrant 1.12 混合搜索,或pgvector + pgvector尺度为50M以下的团队
  中文翻译:向量DB:Qdrant 1.12与混合搜索,或pgvector + pgvector尺度为50M向量以下的团队

> 中文翻译:向量DB:Qdrant 1.12与混合搜索,或pgvector + pgvector尺度为50M向量以下的团队(翻译)

- 零件总结模型:克劳德海库4.5或双子 2.5 闪存,即时缓存
  中文翻译:零件总结模型:克劳德海库4.5或双子 2.5闪存,快速缓存
- 排名重:Cohere排名-3或bge排名重-v2-gemma-2b自主托管
  中文翻译:重排:Cohere重排-3或bge-重排-v2-gemma-2b自主主托管
- 调整:LlamaIndex 摄入工作流程,查询代理的LangGraph
  中文翻译:管弦乐:LlamaIndex 工作流程用于摄入,LangGraph用于查询代理
- 合成器:Claude Sonnet 4.7 (1M语境) 随时缓存
  中文翻译:合成器:Claude Sonnet 4.7 (1M语境) 与快速缓存
- 符号图:进口和调用边缘 Neo4j (管理) 或 kuzu (嵌入式)
  中文翻译:符号图:Neo4j (管理) 或 kuzu (嵌入) 对于进口和调用边缘
- 观察性:每次检索+合成步骤的长跨度
  中文翻译:可观察性:每次检索+合成步骤的长跨度

## 动手构建

> **【中文解读】**构建分为9个阶段:摄取遍历器(git push 触发 diff) 分块摘要器(海库 4.5 批处理) 嵌入池(旅行代码-3 批量 128) ‧BM25 索引(字段加权) 符号图片(Neo4j/kuzu 存储导入/调用/继承关系) 查询代理(LangGraph 三节点:检索-重排-合成) 引用(强制无点声明被过) ‧增量重索引(50 文件推送 60 秒) 评估(100 个标签问题测 MRR@10) ⋅

> **【拓展：tree-sitter 在代码分析中的核心地位】**树座是代码解析的实验标准,由Neovim、Helix、Zed 编辑器和 GitHub 代码搜索使用. 它提供增量解析.
```figure
ce-hybrid-retrieval
```

## 建立它

1. **Ingestion walker.**按每一个按上重复 Git 历史记录.收集已更改的文件.每个文件,用树监管器分析,提取函数和类节点,以其全部源跨度. 发送分类记录.`{repo, path, start_line, end_line, symbol, body}`现在,我们要去.
   中文翻译:1. **Ingestion walker.**按每一个按上重复 Git 历史记录.收集已更改的文件.每个文件,用树监管器分析,提取函数和类节点,以其全部源跨度. 发送分类记录.`{repo, path, start_line, end_line, symbol, body}`现在,我们要去.

2. **Chunk summarizer.**按组分分为Haiku 4.5调用,即时缓存系统序言. 提示:"将这个函数总结成一个句子,命名其公开合约和副作用". 随着部分存储总结.
   翻译: 翻译:**Chunk summarizer.**按组分分为Haiku 4.5调用,即时缓存系统序言. 提示:"将这个函数总结成一个句子,命名其公开合约和副作用". 随着部分存储总结.

3. **Embedding pool.**两条平行队列:密集 (旅行代码-3批量128) 和总结 (相同的模型,但在总结字符串上).`{repo, path, start_line, end_line, symbol, kind}`现在,我们要去.
   翻译: 翻译:**Embedding pool.**两条平行队列:密集 (旅行代码-3批量128) 和总结 (相同的模型,但在总结字符串上).`{repo, path, start_line, end_line, symbol, kind}`现在,我们要去.

4. **BM25 index.**字段权重的Tantivy指数:符号名称重量4,符号体重量1,总结重量2. 启用"找到名为X的函数"查询,并加上"找到X的函数".
   翻译: 翻译:**BM25 index.**字段权重的Tantivy指数:符号名称重量4,符号体重量1,总结重量2. 启用"找到名为X的函数"查询,并加上"找到X的函数".

5. **Symbol graph.**对于每个部分,记录边缘:进口 (本文件使用 repo Z 的符号 Y),调用 (本函数在 C 类上调用方法 M),继承.存储在 kuzu 中.在查询时用于扩大回收跨 repo 边界.
   翻译: 五.**Symbol graph.**对于每个部分,记录边缘:进口 (本文件使用 repo Z 的符号 Y),调用 (本函数在 C 类上调用方法 M),继承.存储在 kuzu 中.在查询时用于扩大回收跨 repo 边界.

6. **Query agent.**具有三个节点的兰格格拉夫.`retrieve`密度火 + BM25平行,乘以 (repo,路径,符号) 倍增.`rerank`运行跨码器在50上,保持10上.`synth`调用Claude Sonnet 4.7在文本中重新排名的部分,缓存系统提示,需要文件:行引用.
   翻译: 七个字**Query agent.**具有三个节点的兰格格拉夫.`retrieve`密度火 + BM25平行,乘以 (repo,路径,符号) 倍增.`rerank`运行跨码器在50上,保持10上.`synth`调用Claude Sonnet 4.7在文本中重新排名的部分,缓存系统提示,需要文件:行引用.

7. **Citation enforcement.**分析模型输出; 任何没有 `(repo/path:start-end)`给用户返回只引用答案.
   翻译:7.**Citation enforcement.**分析模型输出; 任何没有 `(repo/path:start-end)`给用户返回只引用答案.

8. **Incremental re-index.**在每个网关上,计算符号级别差异. 只有重新嵌入的部分,其文字发生了变化. 重新计算进口发生了变化的部分的符号边缘. 测量:为2M-LOC舰队,50文件推重索引在60秒内.
   翻译:8.**Incremental re-index.**在每个网关上,计算符号级别差异. 只有重新嵌入的部分,其文字发生了变化. 重新计算进口发生了变化的部分的符号边缘. 测量:为2M-LOC舰队,50文件推重索引在60秒内.

9. **Eval.**标签100个跨度问题,以黄金文件:线答. 测量MRR@10,nDCG@10,引用忠实性 (有可验证的杆的索赔的部分) 和p50/p99延迟.
   翻译:9.**Eval.**标签100个跨度问题,以黄金文件:线答. 测量MRR@10,nDCG@10,引用忠实性 (有可验证的杆的索赔的部分) 和p50/p99延迟.

## 用它使用方法

```
$ code-rag ask "how is S3 multipart abort wired into our retry budget?"
[retrieve]  12 chunks dense + 7 chunks bm25, 16 unique after dedup
[rerank]    top-5 kept (cohere rerank-3)
[synth]     claude-sonnet-4.7, cache hit rate 68%, 2.1s
answer:
  Multipart aborts are triggered by `AbortMultipartOnFail` in
  services/uploader/retry.go:122-148, which decrements the per-bucket
  retry budget defined in config/budgets.yaml:34-51 ...
  citations: [services/uploader/retry.go:122-148, config/budgets.yaml:34-51,
              libs/s3client/multipart.ts:44-61]
```

## 发射上线

能提供的技能`outputs/skill-codebase-rag.md`鉴于复制文件,它会查询摄入量管道,混合指数和查询代理,并返回任何复制问题上引用的答案.

> 交付物品技能 为`outputs/skill-codebase-rag.md`△给定仓库语料库,它建立了摄取管道,混合索引和查询代理,并回应任何跨仓库问题.

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | Retrieval quality | MRR@10 and nDCG@10 on a 100-question held-out set |
| 25 | 检索质量 | 100 问题保留集上的 MRR@10 和 nDCG@10 |
| 20 | Citation faithfulness | Fraction of answer claims with verifiable file:line anchors |
| 20 | 引用忠实度 | 有可验证 file:line 锚点的答案声明比例 |
| 20 | Latency and scale | p95 query latency at 10k QPS on the indexed corpus size |
| 20 | 延迟与规模 | 索引语料库规模下 10k QPS 的 p95 查询延迟 |
| 20 | Incremental indexing correctness | Time from git push to searchable on a 50-file commit |
| 20 | 增量索引正确性 | 50 文件提交从 git push 到可搜索的时间 |
| 15 | UX and answer formatting | Citation clickability, snippet previews, follow-up affordance |
| 15 | 用户体验与答案格式 | 引用可点击性、代码片段预览、后续追问支持 |
| **100** | | |

## 练习题

1. 换取自主托管的名字嵌入式代码.测量MRR@10三角形.报告是否在重新排名启用时关闭差距.
   中文翻译:将旅行代码-3 换为自托管的名字嵌入代码――测量MRR@10 差异――报告启用重排序后差距是否缩小――

> 中文翻译:将旅行代码-3 换为自托管的名字嵌入代码――测量MRR@10 差异――报告启用重排序后差距是否缩小――(翻译)


2. 注入20%生成代码 (LLM生产的炉板) 进入体内,重新评估.观察检索中毒.添加"生成"旗到有效载荷中,减轻这些击中.
   中文翻译:向语料库注入20% 生成代码(LLM 生成的样板代码)并重新评估──观察检索污染──向负载添加"生成"标志并降低这些命中权重──

> 中文翻译:向语料库注入20% 生成代码(LLM 生成的样板代码)并重新评估──观察检索污染──向负载添加"生成"标志并降低这些命中的权重──(翻译)


3. 基准测量Qdrant混合搜索与pgvector +pgvectorscale在您的体积. 报告p99在批量1.
   中文翻译: 在你的语料库规模下基准测试 Qdrant 混合搜索与pgvector +pgvector规模――报告批量大小为 1 时的p99──

> 中文翻译: 在你的语料库规模下基准测试 Qdrant 混合搜索 vs pgvector + pgvectorskala──报告批量大小为 1 时的 p99──(翻译)


4. 增加基于样本的漂移检查:每周,重复100个问题评估.
   中文翻译:添加基于采样漂移检查:每周重新运行 100题评估──MRR@10 下降 > 5% 时告警──

5. 扩展到跨语言符号分辨率:一个Python函数,通过gRPC调用Go服务.使用符号图来链接它们.
   中文翻译:扩展到跨语言符号解析:一个通过gRPC调用Go 服务的Python函数――使用符号图将它们链接――

## 关键词 关键词

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| AST-aware chunking | "Function-level splits" | Cutting code at tree-sitter node boundaries instead of fixed token windows |
| AST 感知分块 | "函数级拆分" | 在 tree-sitter 节点边界而非固定 token 窗口处切割代码 |
| Hybrid search | "Dense + sparse" | Run BM25 and vector search in parallel, merge top-k, rerank |
| 混合搜索 | "稠密 + 稀疏" | 并行运行 BM25 和向量搜索，合并 top-k，重排序 |
| Cross-encoder rerank | "Second-stage rank" | Model that scores each (query, candidate) pair together, more accurate than cosine |
| 交叉编码器重排序 | "二阶段排序" | 对每个（查询，候选）对一起评分的模型，比余弦更准确 |
| Prompt caching | "Cached system prompt" | 2026 Claude / OpenAI feature that discounts repeat prefix tokens up to 90% |
| Prompt 缓存 | "缓存系统提示" | 2026 Claude/OpenAI 功能，对重复前缀 token 折扣高达 90% |
| Symbol graph | "Code graph" | Edges for imports, calls, inheritance across files and repos |
| 符号图 | "代码图" | 跨文件和仓库的导入、调用、继承边 |
| Citation faithfulness | "Grounded answer rate" | Fraction of claims a user can verify by clicking the anchor and reading the referenced span |
| 引用忠实度 | "有据答案率" | 用户可通过点击锚点并阅读引用范围来验证的声明比例 |
| Incremental re-index | "Push-to-search time" | Wall-clock from git push to the changed symbols being queryable |
| 增量重索引 | "推送至搜索时间" | 从 git push 到变更符号可查询的挂钟时间 |

## 继续阅读 继续阅读

- [Sourcegraph Amp](https://ampcode.com)生产跨度报告代码信息
  中文翻译:生产级跨仓库代码智能
- [Sourcegraph Cody RAG architecture](https://sourcegraph.com/blog/how-cody-understands-your-codebase)这个顶石的参考深度潜水
  中文翻译:本结业项目的深度分析参考
- [Aider repo-map](https://aider.chat/docs/repomap.html)树排名的回复视图
  中文翻译:树座 排序的仓库视图
- [Augment Code enterprise graph](https://www.augmentcode.com)商业象征图RAG
  中文翻译:商业符号图 RAG
- [Qdrant hybrid search docs](https://qdrant.tech/documentation/concepts/hybrid-queries/)参考实施
  中文翻译:参考实现
- [Voyage AI code embeddings](https://docs.voyageai.com/docs/embeddings)旅行代码-3详细信息
  中文翻译:旅行代码-3 详情
- [Cohere rerank-3](https://docs.cohere.com/reference/rerank)跨编码器参考
  中文翻译:交叉编码器参考
- [Pinterest MCP internal search](https://medium.com/pinterest-engineering)内部平台参考
  中文翻译:内部平台参考
