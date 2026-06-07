# Capstone 08 — Production RAG Chatbot for a Regulated Vertical | 生产 结业 聊天机器人 RAG

> Harvey, Glean, Mendable, and LlamaCloud all run the same production shape in 2026. Ingest with docling or Unstructured and ColPali for visuals. Hybrid search. Re-rank with bge-reranker-v2-gemma. Synthesize with Claude Sonnet 4.7 using prompt caching at 60-80% hit rate. Guard with Llama Guard 4 and NeMo Guardrails. Watch with Langfuse and Phoenix. Grade with RAGAS on a 200-question golden set. Build one in a regulated domain (legal, clinical, insurance), and the capstone is passing the golden set, the red team, and the drift dashboard.

> **【中文解读】** 本节是综合项目——构建生产级 RAG 聊天机器人，包含缓存、安全和监控。


**Type:** Capstone | **类型:** 综合项目
**Languages:** Python (pipeline + API), TypeScript (chat UI) | **语言:** Python（管道 + API）, TypeScript（聊天 UI）
**Prerequisites:** Phase 5 (NLP), Phase 7 (transformers), Phase 11 (LLM engineering), Phase 12 (multimodal), Phase 17 (infrastructure), Phase 18 (safety) | **前置知识:** Phase 5（NLP）, Phase 7（Transformer）, Phase 11（LLM 工程）, Phase 12（多模态）, Phase 17（基础设施）, Phase 18（安全）
**Phases exercised:** P5 · P7 · P11 · P12 · P17 · P18 | **涉及阶段:** P5 · P7 · P11 · P12 · P17 · P18
**Time:** 30 hours | **时间:** 30 小时

## Problem | 问题引入

> **【中文解读】** 本节描述受监管领域 RAG 的生产挑战。法律合同、临床试验方案、保险条款——这些场景 ROI 明确且风险具体。难点不在模型，而在合规（HIPAA/GDPR/SOC2）、引用级审计、成本控制（Prompt Caching 可降低 60-90%）、幻觉检测（RAGAS 忠实度）和漂移监控（源文档更新时索引未同步）。

> **【拓展：受监管领域 RAG 产品】** 2026 年主要玩家：Harvey（法律，Allen & Overy 合作）、Glean（企业搜索）、Mendable（开发者文档）。共同架构：docling/Unstructured 摄取 + ColPali 处理视觉内容 + 混合检索 + 重排序 + Prompt Caching + Llama Guard 4 安全防护 + NeMo Guardrails 策略护栏。Prompt Caching 的关键是将稳定前缀（系统提示 + 检索上下文）放在缓存头部，60-80% 命中率下每查询成本降低 3-5 倍。

Regulated-domain RAG (legal contracts, clinical trial protocols, insurance policies) is the most-shipped production shape of 2026 because the ROI is obvious and the stakes are concrete. Harvey (Allen & Overy) built it for legal. Mendable ships the developer-docs flavor. Glean covers enterprise search. The pattern is: ingest high-fidelity, retrieve hybrid with rerank, synthesize with citation enforcement and prompt caching, guard with multiple safety layers, and monitor drift continuously.

> 受监管领域的 RAG（法律合同、临床试验方案、保险条款）是 2026 年出货量最大的生产形态，因为 ROI 明确且风险具体。Harvey（Allen & Overy）为法律领域构建了它。Mendable 发布了开发者文档版本。Glean 覆盖企业搜索。模式是：高保真摄取、混合检索加重排序、带引用强制和 prompt caching 的合成、多层安全防护和持续漂移监控。

The hard parts are not the model. They are jurisdiction-aware compliance (HIPAA, GDPR, SOC2), citation-level auditability, cost control (prompt caching buys 60-90% discount when hit rate is high), hallucination detection via RAGAS faithfulness, and drift detection when the source documents get updated without the index catching up. This capstone asks you to ship all of it on a 200-question golden set with a red-team suite alongside.

> 难点不在模型。它们是司法管辖感知合规（HIPAA、GDPR、SOC2）、引用级可审计性、成本控制（prompt caching 在命中率高时获得 60-90% 折扣）、通过 RAGAS 忠实度进行幻觉检测，以及源文档更新但索引未跟上时的漂移检测。本结业项目要求你在 200 题黄金集上发布所有内容，并附带红队测试套件。

## Concept | 核心概念

> **【中文解读】** 管道分两侧：摄取侧（docling/Unstructured 解析 + ColPali 视觉处理 + 分块摘要/角色标签/司法管辖区标签 + pgvector/Qdrant 稠密索引 + Tantivy BM25 稀疏索引）和对话侧（LangGraph 记忆管理 + 混合检索 + 重排序 + Claude Sonnet 4.7 合成 + Llama Guard 4 + NeMo Guardrails 安全过滤）。评估栈四层：200 题黄金集（正确性）、红队测试（安全性）、RAGAS 在线评估（忠实度/相关性）、Arize Phoenix 漂移仪表盘（周监控）。

> **【拓展：RAGAS 评估框架】** RAGAS 0.2 是 RAG 系统的标准化评估框架，核心指标：faithfulness（答案是否完全基于检索上下文）、answer relevance（答案是否切题）、context precision（检索结果是否精准）。配合 DeepEval 做幻觉检测和越狱测试。生产环境建议在线 RAGAS（采样 5-10% 的查询自动评分）+ 每周漂移监控（nDCG 或引用分数下降 > 5% 时告警）+ 发布前红队测试（50 个对抗性提示）。

The pipeline has two sides. **Ingestion**: docling or Unstructured parses structured documents; ColPali handles visually rich ones; chunks get summaries, tags, and role-based access labels. Vectors go into pgvector + pgvectorscale (under 50M vectors) or Qdrant Cloud; sparse BM25 runs alongside. **Conversation**: LangGraph handles memory and multi-turn; each query runs hybrid retrieval, reranks with bge-reranker-v2-gemma-2b, synthesizes with Claude Sonnet 4.7 (prompt-cached), passes output through Llama Guard 4 and NeMo Guardrails, and emits a citation-anchored response.

> 管道有两侧。**摄取**：docling 或 Unstructured 解析结构化文档；ColPali 处理视觉丰富的文档；分块获得摘要、标签和基于角色的访问标签。向量进入 pgvector + pgvectorscale（5000 万向量以下）或 Qdrant Cloud；稀疏 BM25 并行运行。**对话**：LangGraph 处理记忆和多轮；每个查询运行混合检索，用 bge-reranker-v2-gemma-2b 重排序，用 Claude Sonnet 4.7（prompt 缓存）合成，通过 Llama Guard 4 和 NeMo Guardrails 传递输出，并发出引用锚定的响应。

The eval stack has four layers. **Golden set** (200 labeled Q/A with citations) for correctness. **Red team** (jailbreaks, PII extraction attempts, off-domain questions) for safety. **RAGAS** for faithfulness / answer relevance / context precision automatically per-turn. **Drift dashboard** (Arize Phoenix) watching retrieval quality and hallucination score weekly.

> 评估栈有四层。**黄金集**（200 个带引用的标注 Q/A）用于正确性。**红队**（越狱、PII 提取尝试、域外问题）用于安全性。**RAGAS** 用于每轮自动评分忠实度/答案相关性/上下文精度。**漂移仪表盘**（Arize Phoenix）每周监控检索质量和幻觉分数。

Prompt caching is the cost lever. Claude 4.5+ and GPT-5+ support caching system prompts + retrieved context. At 60-80% hit rate, per-query cost drops 3-5x. The pipeline must be designed for stable prefixes (system prompt + reranked context first) to achieve high cache hit rates.

> Prompt caching 是成本杠杆。Claude 4.5+ 和 GPT-5+ 支持缓存系统提示 + 检索上下文。在 60-80% 命中率下，每查询成本降低 3-5 倍。管道必须为稳定前缀（系统提示 + 重排序上下文在前）设计以实现高缓存命中率。

## Architecture | 架构

```
documents (contracts, protocols, policies)
      |
      v
docling / Unstructured parse + ColPali for visuals
      |
      v
chunks + summaries + role-labels + jurisdiction tags
      |
      v
pgvector + pgvectorscale  +  BM25 (Tantivy)
      |
query + role + jurisdiction
      |
      v
LangGraph conversational agent
   +--- retrieve (hybrid)
   +--- filter by role + jurisdiction
   +--- rerank (bge-reranker-v2-gemma-2b or Voyage rerank-2)
   +--- synthesize (Claude Sonnet 4.7, prompt cached)
   +--- guard (Llama Guard 4 + NeMo Guardrails + Presidio output PII scrub)
   +--- cite + return
      |
      v
eval:
  RAGAS faithfulness / answer_relevance / context_precision (online)
  Langfuse annotation queue (sampled)
  Arize Phoenix drift (weekly)
  red team suite (pre-release)
```

## Stack | 技术栈

- Ingestion: Unstructured.io or docling for structured documents; ColPali for visually-rich PDFs
  中文翻译：Ingestion: Unstructured.io or docling for structured documents; ColPali for visually-rich PDFs

> 中文翻译：Ingestion: Unstructured.io or docling for structured documents; ColPali for visually-rich PDFs（翻译）

- Vector DB: pgvector + pgvectorscale under 50M vectors; Qdrant Cloud otherwise
  中文翻译：Vector DB: pgvector + pgvectorscale under 50M vectors; Qdrant Cloud otherwise

> 中文翻译：Vector DB: pgvector + pgvectorscale under 50M vectors; Qdrant Cloud otherwise（翻译）

- Sparse: Tantivy BM25 with field weights
  中文翻译：Sparse: Tantivy BM25 with field weights
- Orchestration: LlamaIndex Workflows (ingestion) + LangGraph (conversation)
  中文翻译：Orchestration: LlamaIndex Workflows (ingestion) + LangGraph (conversation)
- Re-ranker: bge-reranker-v2-gemma-2b self-hosted or Voyage rerank-2 hosted
  中文翻译：Re-ranker: bge-reranker-v2-gemma-2b self-hosted or Voyage rerank-2 hosted
- LLM: Claude Sonnet 4.7 with prompt caching; fallback Llama 3.3 70B self-hosted
  中文翻译：LLM: Claude Sonnet 4.7 with prompt caching; fallback Llama 3.3 70B self-hosted
- Eval: RAGAS 0.2 online, DeepEval for hallucination and jailbreak suites
  中文翻译：Eval: RAGAS 0.2 online, DeepEval for hallucination and jailbreak suites
- Observability: Langfuse self-hosted with annotation queue; Arize Phoenix for drift
  中文翻译：Observability: Langfuse self-hosted with annotation queue; Arize Phoenix for drift
- Guardrails: Llama Guard 4 input/output classifier, NeMo Guardrails v0.12 policy, Presidio PII scrub
  中文翻译：Guardrails: Llama Guard 4 input/output classifier, NeMo Guardrails v0.12 policy, Presidio PII scrub

> 中文翻译：Guardrails: Llama Guard 4 input/output classifier, NeMo Guardrails v0.12 policy, Presidio PII scrub（翻译）

- Compliance: role-based access labels on chunks; jurisdiction tags for GDPR/HIPAA
  中文翻译：Compliance: role-based access labels on chunks; jurisdiction tags for GDPR/HIPAA

## Build It | 动手构建

> **【中文解读】** 构建 8 个阶段：语料摄入（Unstructured/docling 解析 + ColPali 视觉页面）、索引（pgvector 密集向量 + Tantivy BM25）、混合检索（RRF 融合 + 角色过滤）、重排序（Cohere Rerank 3）、上下文压缩、对话记忆、RAG 评估（RAGAS 框架）和合规审计（GDPR/HIPAA 标签）。

> **【拓展：生产 RAG 系统在 2026 年的最佳实践】** Airbnb、Notion、Dropbox 的 AI 搜索都基于 RAG 架构。2026 年的关键改进：1）混合检索（dense + sparse）比纯向量搜索准确率高 10-15%；2）ColPali 视觉检索直接在文档截图上做检索，跳过 OCR；3）chunk 级别的角色标签和权限过滤确保合规；4）RAGAS 评估框架提供 faithfulness、relevancy、context recall 等维度。

1. **Ingestion.** Parse your corpus (1000-10000 documents for a serious build) with Unstructured or docling. For scanned / visual-heavy pages, route through ColPali. Produce chunks with summaries, role-labels, jurisdiction tags.
   中文翻译：1. **Ingestion.** Parse your corpus (1000-10000 documents for a serious build) with Unstructured or docling. For scanned / visual-heavy pages, route through ColPali. Produce chunks with summaries, role-labels, jurisdiction tags.

2. **Index.** Dense embeddings (Voyage-3 or Nomic-embed-v2) into pgvector + pgvectorscale. BM25 side-index via Tantivy. Role and jurisdiction filters as payload.
   中文翻译：2. **Index.** Dense embeddings (Voyage-3 or Nomic-embed-v2) into pgvector + pgvectorscale. BM25 side-index via Tantivy. Role and jurisdiction filters as payload.

3. **Hybrid retrieve.** Filter by role+jurisdiction first; then parallel dense + BM25; merge with reciprocal rank fusion; top-20 to reranker; top-5 to synth.
   中文翻译：3. **Hybrid retrieve.** Filter by role+jurisdiction first; then parallel dense + BM25; merge with reciprocal rank fusion; top-20 to reranker; top-5 to synth.

4. **Synthesize with prompt caching.** System prompt + static policies in cache header; reranked context as cache extension; user question as uncached suffix. Target 60-80% cache hit rate in steady state.
   中文翻译：4. **Synthesize with prompt caching.** System prompt + static policies in cache header; reranked context as cache extension; user question as uncached suffix. Target 60-80% cache hit rate in steady state.

5. **Guardrails.** Llama Guard 4 on input; NeMo Guardrails rails block off-domain questions or policy-forbidden topics; Presidio scrubs accidental PII in the output; citation enforcement post-filter.
   中文翻译：5. **Guardrails.** Llama Guard 4 on input; NeMo Guardrails rails block off-domain questions or policy-forbidden topics; Presidio scrubs accidental PII in the output; citation enforcement post-filter.

6. **Golden set.** 200 Q/A pairs labeled by a domain expert with (answer, citations). Score agent on exact-citation match, answer correctness, faithfulness (RAGAS).
   中文翻译：6. **Golden set.** 200 Q/A pairs labeled by a domain expert with (answer, citations). Score agent on exact-citation match, answer correctness, faithfulness (RAGAS).

7. **Red team.** 50 adversarial prompts: jailbreaks (PAIR, TAP), PII exfiltration attempts, off-domain, cross-jurisdiction leaks. Score with pass/fail and severity.
   中文翻译：7. **Red team.** 50 adversarial prompts: jailbreaks (PAIR, TAP), PII exfiltration attempts, off-domain, cross-jurisdiction leaks. Score with pass/fail and severity.

8. **Drift dashboard.** Arize Phoenix tracks retrieval quality (nDCG, citation faithfulness) weekly. Alert on 5% drop.
   中文翻译：8. **Drift dashboard.** Arize Phoenix tracks retrieval quality (nDCG, citation faithfulness) weekly. Alert on 5% drop.

9. **Cost report.** Langfuse: prompt-caching hit rate, tokens per query, $/query breakdown by stage.
   中文翻译：9. **Cost report.** Langfuse: prompt-caching hit rate, tokens per query, $/query breakdown by stage.

> 中文翻译：9. **Cost report.** Langfuse: prompt-caching hit rate, tokens per query, $/query breakdown by stage.（翻译）


## Use It | 使用方法

```
$ chat --role=analyst --jurisdiction=GDPR
> what is the data-retention obligation for EU user profiles under our contract?
[retrieve]  hybrid top-20 filtered to GDPR + analyst-role
[rerank]    top-5 kept
[synth]     claude-sonnet-4.7, cache hit 74%, 0.8s
answer:
  The contract (Section 12.4, Master Services Agreement dated 2024-03-11)
  obligates EU user profile deletion within 30 days of termination per GDPR
  Article 17. The DPA amendment (DPA-v2.1, Section 5) extends this to 14 days
  for "restricted" category data.
  citations: [MSA-2024-03-11 s12.4, DPA-v2.1 s5]
```

## Ship It | 部署上线

`outputs/skill-production-rag.md` describes the deliverable. A regulated-domain chatbot deployed with compliance labels, passed through the rubric, observed with live drift monitoring.

> `outputs/skill-production-rag.md` 描述了交付物。一个部署了合规标签、通过评分标准、带实时漂移监控的受监管领域聊天机器人。

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | RAGAS faithfulness + answer relevance | Online scores on the golden set (200 Q/A) |
| 25 | RAGAS 忠实度 + 答案相关性 | 黄金集（200 Q/A）上的在线分数 |
| 20 | Citation correctness | Fraction of answers with verifiable source anchors |
| 20 | 引用正确性 | 有可验证源锚点的答案比例 |
| 20 | Guardrail coverage | Llama Guard 4 pass rate + jailbreak suite results |
| 20 | 护栏覆盖 | Llama Guard 4 通过率 + 越狱套件结果 |
| 20 | Cost / latency engineering | Prompt-cache hit rate, p95 latency, $/query |
| 20 | 成本/延迟工程 | Prompt 缓存命中率、p95 延迟、$/query |
| 15 | Drift monitoring dashboard | Phoenix live dashboard with weekly retrieval-quality trend |
| 15 | 漂移监控仪表盘 | Phoenix 实时仪表盘带每周检索质量趋势 |
| **100** | | |

## Exercises | 练习题

1. Build a second corpus slice under a different jurisdiction (e.g., HIPAA alongside GDPR). Demonstrate role+jurisdiction filtering preventing cross-leak on a 20-question cross-jurisdiction probe.
   中文翻译：在不同司法管辖区下构建第二个语料库切片（如 HIPAA 与 GDPR 并行）。演示角色+司法管辖区过滤在 20 题跨司法管辖区探测中防止交叉泄漏。

> 中文翻译：在不同司法管辖区下构建第二个语料库切片（如 HIPAA 与 GDPR 并行）。演示角色+司法管辖区过滤在 20 题跨司法管辖区探测中防止交叉泄漏。（翻译）


2. Measure prompt-cache hit rate over a week of production traffic. Identify which queries break the cache prefix. Restructure.
   中文翻译：测量一周生产流量中的 prompt 缓存命中率。识别哪些查询破坏缓存前缀。重构。

3. Add multi-turn memory with a 10k-token summary buffer. Measure whether faithfulness drops as the conversation grows.
   中文翻译：添加带 10k token 摘要缓冲区的多轮记忆。测量随着对话增长忠实度是否下降。

4. Swap Claude Sonnet 4.7 for Llama 3.3 70B self-hosted. Measure $/query and faithfulness delta.
   中文翻译：将 Claude Sonnet 4.7 换为自托管的 Llama 3.3 70B。测量 $/query 和忠实度差异。

> 中文翻译：将 Claude Sonnet 4.7 换为自托管的 Llama 3.3 70B。测量 $/query 和忠实度差异。（翻译）


5. Add an "unsure" mode: if top reranked scores are below a threshold, the agent says "I do not have confident citations" instead of answering. Measure false-confidence reduction.
   中文翻译：添加"不确定"模式：如果 top 重排序分数低于阈值，Agent 说"我没有确信的引用"而非回答。测量虚假置信度减少。

> 中文翻译：添加"不确定"模式：如果 top 重排序分数低于阈值，Agent 说"我没有确信的引用"而非回答。测量虚假置信度减少。（翻译）


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| Prompt caching | "Cached system + context" | Claude/OpenAI feature: cached prefix tokens discounted 60-90% on hit |
| Prompt 缓存 | "缓存系统 + 上下文" | Claude/OpenAI 功能：缓存前缀 token 命中时折扣 60-90% |
| RAGAS | "RAG evaluator" | Automated scoring of faithfulness, answer relevance, context precision |
| RAGAS | "RAG 评估器" | 忠实度、答案相关性、上下文精度的自动评分 |
| Golden set | "Labeled eval" | 200+ expert-labeled Q/A with citations; the ground truth |
| 黄金集 | "标注评估" | 200+ 专家标注的带引用 Q/A；基准真相 |
| Jurisdiction tag | "Compliance label" | GDPR/HIPAA/SOC2 scope attached to chunks; enforced by retrieval filter |
| 司法管辖区标签 | "合规标签" | 附加到分块的 GDPR/HIPAA/SOC2 范围；由检索过滤器强制 |
| Citation faithfulness | "Grounded answer rate" | Fraction of claims backed by retrievable source spans |
| 引用忠实度 | "有据答案率" | 有可检索源跨度支持的声明比例 |
| Drift | "Retrieval quality decay" | Weekly change in nDCG or citation score; alert threshold 5% |
| 漂移 | "检索质量衰减" | nDCG 或引用分数的周变化；告警阈值 5% |
| Red team | "Adversarial eval" | Pre-release jailbreak, PII extraction, off-domain probes |
| 红队 | "对抗性评估" | 发布前越狱、PII 提取、域外探测 |

## Further Reading | 延伸阅读

- [Harvey AI](https://www.harvey.ai) — reference legal production stack
  中文翻译：参考法律生产栈
- [Glean enterprise search](https://www.glean.com) — reference RAG at enterprise scale
  中文翻译：企业级 RAG 参考
- [Mendable documentation](https://mendable.ai) — developer-docs RAG reference
  中文翻译：开发者文档 RAG 参考
- [LlamaCloud Parse + Index](https://docs.llamaindex.ai/en/stable/examples/llama_cloud/llama_parse/) — managed ingestion
  中文翻译：托管摄取
- [Anthropic prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) — the cost-lever reference
  中文翻译：成本杠杆参考
- [RAGAS 0.2 documentation](https://docs.ragas.io/) — the canonical RAG eval framework
  中文翻译：规范 RAG 评估框架
- [Arize Phoenix](https://github.com/Arize-ai/phoenix) — reference drift observability
  中文翻译：参考漂移可观测性
- [Llama Guard 4](https://ai.meta.com/research/publications/llama-guard-4/) — 2026 safety classifier
  中文翻译：2026 安全分类器
- [NeMo Guardrails v0.12](https://docs.nvidia.com/nemo-guardrails/) — policy rail framework
  中文翻译：策略护栏框架
