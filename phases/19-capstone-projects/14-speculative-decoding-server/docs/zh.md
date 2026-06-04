# Capstone 14 — Speculative-Decoding Inference Server | 推测 推理 结业 编码 服务器

> EAGLE-3 in vLLM 0.7 ships 2.5-3x throughput on real traffic. P-EAGLE (AWS 2026) pushed parallel speculation even further. SGLang's SpecForge trained draft heads at scale. Red Hat's Speculators hub published aligned drafts for common open models. TensorRT-LLM made speculative decoding first-class on NVIDIA. The 2026 production serving stack is vLLM or SGLang with EAGLE-family drafts, FP8 or INT4 quantization, and HPA on queue-wait. This capstone is to serve two open models at 2.5x+ baseline throughput with a full tail-latency report.

> **【中文解读】** 本节是综合项目——构建推测解码服务器。


**类型：** 结业项目
**语言：** Python (serving), C++ / CUDA (kernel inspection), YAML (configs)
**前置知识：** Phase 3 (deep learning), Phase 7 (transformers), Phase 10 (LLMs from scratch), Phase 17 (infrastructure)
**涉及的 Phase：** P3 · P7 · P10 · P17
**预计时间：** 30 hours

## Problem

> **【中文解读】** 本节描述推测解码服务器的工程挑战。2026 年推测解码已成为标配——EAGLE-3 草稿头在目标模型隐状态上训练，预测 N 个 token 前瞻，目标模型一次验证。60-80% 的接受率转化为 2-3 倍端到端吞吐提升。关键工艺在服务运维而非模型：接受率随流量分布漂移、拒绝时的尾延迟比无推测更差、$/1M tokens 对比 API 价格是可信度杠杆。

> **【拓展：推测解码技术演进】** EAGLE-3 在 vLLM 0.7 中提供 2.5-3 倍吞吐提升。P-EAGLE（AWS 2026）将并行推测推向更深的草稿树。SGLang 的 SpecForge 提供大规模草稿头训练管道。Red Hat Speculators Hub 发布了 Llama 3.3 70B、Qwen3-Coder-30B MoE 等模型的预对齐草稿。部署使用 K8s HPA 按 queue-wait 而非 CPU 自动扩缩，FP8-Marlin 或 INT4-AWQ 量化控制 GPU 内存。

Speculative decoding became a commodity in 2026. EAGLE-3 draft heads train on the target model's hidden states and predict N tokens ahead; the target model verifies in a single pass. Acceptance rates of 60-80% translate to 2-3x end-to-end throughput. vLLM 0.7 integrates this natively. SGLang + SpecForge gives you the training pipeline. Red Hat's Speculators publishes aligned drafts for Llama 3.3 70B, Qwen3-Coder-30B MoE, GPT-OSS-120B.

The craft is in the serving operations, not the model. Acceptance rate drifts with the traffic distribution (ShareGPT vs code vs domain data). Tail latency under rejection is worse than without speculation — you must report p99 at multiple batch sizes, not just steady-state tokens/sec. Cost per 1M tokens vs Anthropic / OpenAI API is the credibility lever.

## Concept

> **【中文解读】** 推测解码分两层：草稿模型（EAGLE-3 头/ngram/小型对齐模型）每步提出 k 个候选 token，目标模型一次验证全部 k 个——接受的前缀替换贪心路径。接受率取决于草稿-目标对齐度和输入分布。EAGLE-3 在大多数流量上优于 ngram，P-EAGLE 支持并行推测的更深层草稿树。部署使用 vLLM 0.7，每 GPU 一个副本，FP8/INT4 量化控制内存。

> **【拓展：接受率与延迟权衡】** 接受率的分布特性直接影响尾延迟：在拒绝情况下，验证 pass 更大导致 p99 延迟高于无推测基线。因此服务配置必须按批次大小（1/8/32）分桶报告延迟。实测数据：代码领域接受率约 0.65-0.75，通用对话约 0.70-0.80，数学推理约 0.55-0.65。$/1M tokens 是与 Anthropic/OpenAI API 对比的基准——自托管推测解码通常在 8B 模型上实现 $0.10-0.30/1M tokens，70B 模型上 $1-3/1M tokens。

Speculative decoding has two layers. A **draft** model (EAGLE-3 head, ngram, or smaller target-aligned model) proposes k candidate tokens per step. The **target** model verifies all k in one pass; any prefix accepted replaces the greedy path. Acceptance rate depends on draft-target alignment and the input distribution.

EAGLE-3 beats ngram drafts on most traffic. P-EAGLE runs parallel speculation for deeper draft trees. The trade-off: P99 latency on rejection is higher because the verify pass is larger. The serving config must report batch-size-bucketed latency to surface this.

Deployment is Kubernetes. vLLM 0.7 runs one replica per GPU or tensor-parallel shard. HPA autoscales on queue-wait rather than CPU. FP8 (Marlin) and INT4 (AWQ) quants keep GPU memory inside an H100 / H200 envelope. The end-to-end report is throughput, acceptance rate, p50/p99 at batch 1/8/32, and $/1M tokens.

## 架构 | 架构

```
request ingress
    |
    v
vLLM server (0.7) or SGLang (0.4)
    |
    +-- draft: EAGLE-3 heads | P-EAGLE parallel | ngram fallback
    +-- target: Llama 3.3 70B | Qwen3-Coder-30B | GPT-OSS-120B
    |     quantized FP8-Marlin or INT4-AWQ
    |
    v
verify pass: batch k draft tokens through target
    |
    v (accept prefix; resample for rejected suffix)
    v
token stream back to client
    |
    v
Prometheus metrics: throughput, acceptance rate, queue wait, latency p50/p99
    |
    v
HPA on queue-wait metric
```

## Stack

- Serving: vLLM 0.7 or SGLang 0.4
- Speculative methods: EAGLE-3 draft heads, P-EAGLE parallel speculation, ngram fallback
- Draft training: SpecForge (SGLang) or Red Hat Speculators
- Target models: Llama 3.3 70B, Qwen3-Coder-30B MoE, GPT-OSS-120B
- Quantization: FP8 (Marlin), INT4 AWQ
- Deployment: Kubernetes + NVIDIA device plugin; HPA on queue-wait metric
- Eval: ShareGPT, MT-Bench-v2, GSM8K, HumanEval for domain-spread acceptance measurement
- Reference: TensorRT-LLM speculative decoding for a vendor baseline

## 动手实现 | 动手构建

> **【中文解读】** 构建投机解码推理服务器：目标模型（Llama 3.3 70B FP8 量化）部署在 vLLM 上，草稿模型（Llama 3.3 8B 或 EAGLE-3 draft heads）并行预测后续 token，投机调度器验证草稿并接受/拒绝。关键度量是接受率（acceptance rate）——典型值 60-80%，直接决定加速比。

> **【拓展：投机解码在 2026 年推理优化中的地位】** 投机解码（Speculative Decoding）是 LLM 推理延迟优化的核心技术。vLLM 0.7+、TensorRT-LLM、Anthropic 的推理服务都采用此技术。原理：小模型快速生成 K 个候选 token，大模型一次前向传播验证所有候选——接受的 token 免费（无额外延迟），拒绝的 token 被丢弃。EAGLE-3（Red Hat）使用特征级预测而非 token 级，接受率提升到 85%+。实测在 H100 上，70B 模型的 TTFT（首 token 延迟）降低 40-60%。

1. **Target model prep.** Pick Llama 3.3 70B. Quantize to FP8 via Marlin. Deploy under vLLM 0.7 on 1xH100 (or 2x tensor-parallel).

2. **Draft source.** Pull an aligned EAGLE-3 draft head from Red Hat Speculators (or train one via SpecForge). Load into vLLM's speculative-decoding config.

3. **Baseline numbers.** Before speculation: tokens/s at batch 1/8/32, p50/p99 latency, GPU utilization. Publish.

4. **Enable EAGLE-3.** Flip config; rerun the same benchmark. Report speedup, acceptance rate, p99 tail-latency delta.

5. **P-EAGLE.** Enable parallel speculation; measure deeper draft tree vs serial EAGLE-3. Report the inflection where P-EAGLE helps vs hurts.

6. **Domain traffic.** Run ShareGPT vs HumanEval vs domain-specific traffic through the same server. Measure acceptance rate per distribution. Identify when drafts drift.

7. **Second target model.** Run the same pipeline on Qwen3-Coder-30B MoE. Draft is trickier (MoE routing noise). Report.

8. **K8s HPA.** Deploy under K8s with HPA tracking `queue_wait_ms`. Demonstrate scale-out when load triples.

9. **Cost comparison.** Compute $/1M tokens vs Anthropic Claude Sonnet 4.7 and OpenAI GPT-5.4 on the same eval. Publish.

## 用框架实现 | 使用方法

```
$ curl https://infer.example.com/v1/chat/completions -d '{"messages":[...]}'
[serve]     vLLM 0.7, Llama 3.3 70B FP8, EAGLE-3 active
[decode]    bs=8, accepted_tokens_per_step=3.2, acceptance_rate=0.76
[latency]   first-token 42ms, full-response 980ms (620 tokens)
[cost]      $0.34 per 1M output tokens at sustained throughput
```

## 产出物 | 部署上线

`outputs/skill-inference-server.md` describes the deliverable. A measured serving stack with speculative decoding, a full benchmark report, and a K8s deployment.

| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | Measured speedup vs baseline | 2.5x+ throughput at matched quality on two models |
| 20 | Acceptance rate on realistic traffic | Per-distribution acceptance-rate report |
| 20 | P99 tail-latency discipline | p99 at batch 1/8/32 with and without speculation |
| 20 | Ops | K8s deploy, HPA on queue-wait, rollout smooth |
| 15 | Write-up and methodology | Clear explanation of what changed and why |
| **100** | | |

## 练习题 | 练习题

1. Measure acceptance-rate degradation when the draft is one version behind the target (e.g., Llama 3.3 -> 3.4 drift). Build a monitoring alert.

2. Implement ngram-fallback: if EAGLE-3 acceptance drops below a threshold, switch to ngram drafts. Report reliability improvement.

3. Run a controlled MoE experiment: same Qwen3-Coder-30B with routing noise injected vs without. Measure draft acceptance sensitivity.

4. Extend to H200 (141 GB). Report the model-size-per-replica headroom gained and whether you can serve an unquantized Llama 3.3 70B.

5. Benchmark TensorRT-LLM speculative decoding on the same H100 hardware. Report where it wins vs vLLM.

## 术语速查表 | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Draft model | "Speculator" | Small model that proposes N tokens for the target to verify |
| EAGLE-3 | "2026 draft architecture" | Draft head trained on target hidden states; ~75% acceptance |
| P-EAGLE | "Parallel speculation" | Tree of draft branches verified in one target pass |
| Acceptance rate | "Hit rate" | Fraction of drafted tokens accepted without resampling |
| Quantization | "FP8 / INT4" | Lower-precision weights to fit more model in GPU memory |
| Queue wait | "HPA metric" | Time a request waits in the pending queue before inference starts |
| Speculators hub | "Aligned drafts" | Red Hat Neural Magic hub of EAGLE drafts for common open models |

## 延伸阅读 | 延伸阅读

- [vLLM EAGLE and P-EAGLE documentation](https://docs.vllm.ai) — the reference serving stack
- [P-EAGLE (AWS 2026)](https://aws.amazon.com/blogs/machine-learning/p-eagle-faster-llm-inference-with-parallel-speculative-decoding-in-vllm/) — parallel speculative decoding paper + integration
- [SGLang SpecForge](https://github.com/sgl-project/SpecForge) — draft-head training pipeline
- [Red Hat Speculators](https://github.com/neuralmagic/speculators) — aligned draft hub
- [TensorRT-LLM speculative decoding](https://nvidia.github.io/TensorRT-LLM/) — vendor alternative
- [Fireworks.ai serving architecture](https://fireworks.ai/blog) — commercial reference
- [EAGLE-3 paper (arXiv:2503.01840)](https://arxiv.org/abs/2503.01840) — the method paper
- [vLLM repository](https://github.com/vllm-project/vllm) — code and benchmarks
