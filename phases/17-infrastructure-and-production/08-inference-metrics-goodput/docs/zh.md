# Inference Metrics — TTFT, TPOT, ITL, Goodput, P99 | 推理 指标 Goodput

> Four metrics decide whether an inference deployment is working. TTFT is prefill plus queue plus network. TPOT (equivalently ITL) is the memory-bound decode cost per token. End-to-end latency is TTFT plus TPOT times output length. Throughput is tokens per second aggregated across the fleet. But the one that matters for product is goodput — the fraction of requests that met every SLO simultaneously. High throughput at low goodput means you are processing tokens that never reach users on time. Reference numbers for Llama-3.1-8B-Instruct on TRT-LLM in 2026: mean TTFT 162 ms, mean TPOT 7.33 ms, mean E2E 1,093 ms. Always report P50, P90, P99 — never just mean. And watch the measurement trap: GenAI-Perf excludes TTFT from ITL calculation, LLMPerf includes it; two tools disagree on TPOT for the same run.

> **【中文解读】** 本节介绍了推理指标和 Goodput——衡量 LLM 推理服务质量的关键指标体系。


**类型：** 学习
**语言：** Python (stdlib, toy percentile calculator and goodput reporter)
**前置条件：** Phase 17 · 04 (vLLM Serving Internals)
**时间：** ~60 minutes

## 学习目标 | 学习目标

- Define TTFT, TPOT, ITL, E2E, throughput, and goodput precisely and name the component each one measures.
- Explain why mean is the wrong statistic for LLM serving and how to read P50/P90/P99.
- Construct an SLO multi-constraint (e.g. TTFT<500 ms AND TPOT<15 ms AND E2E<2 s) and compute goodput against it.
- Name two benchmark tools that disagree on TPOT for the same run and explain why.

## 问题引入 | 问题

> **【中文解读】** 推理服务有多个延迟轴，每个轴以不同方式失败。Prefill 是计算受限的，随提示长度增长；Decode 是内存受限的，随 batch size 增长；排队延迟是运维问题；网络是物理距离问题。需要不同的指标来衡量每个维度，需要百分位数，还需要一个综合指标说"用户是否得到了期望的体验"——这就是 Goodput。

> **【拓展：LLM 推理指标体系】** 2026 年 LLM 推理的完整指标体系包括：(1) TTFT（首 token 延迟）——用户感知到的首次响应时间；(2) TPOT/ITL（每 token 延迟/inter-token 延迟）——流式输出的平滑度；(3) E2E（端到端延迟）——从请求到完成的总时间；(4) Throughput（吞吐量）——集群效率指标；(5) Goodput（有效吞吐）——同时满足所有 SLA 的请求比例。MLPerf Inference v6.0 已将 Goodput 作为官方提交指标。

"Our throughput is 15,000 tokens per second." So what? If 40% of requests blew past 2 seconds end-to-end, users abandoned the session. Throughput alone does not tell you whether the product works.

Inference has multiple axes of latency and each one fails differently. Prefill is compute-bound and scales with prompt length. Decode is memory-bound and scales with batch size. Queuing delay is an operational problem. Network is a physical-distance problem. You need distinct metrics for each, and you need percentiles, and you need a single composite that says "did the user get what they expected" — that is goodput.

## 核心概念 | 概念

### TTFT — time to first token

> **【中文解读】** TTFT = queue_time + network_request + prefill_time。Prefill 在长提示时占主导——32K prompt 在 Llama 3.3 70B FP8 H100 上需要约 800ms 的纯 prefill。排队时间是负载下的调度器行为，网络请求包括 TLS 的线缆时间。TTFT 是用户在流式返回任何内容之前感知到的延迟。

`TTFT = queue_time + network_request + prefill_time`

Prefill dominates when prompts are long. On Llama-3.3-70B FP8 on H100, a 32k prompt takes ~800 ms of pure prefill. Queue time is scheduler behavior under load. Network request is wire time including TLS. TTFT is the latency the user sees before anything streams back.

### TPOT / ITL — inter-token latency

> **【中文解读】** TPOT（time per output token）= ITL（inter-token latency）= decode latency per token。公式：TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced。在 Llama 3.3 70B H100 + 分块预填充下，TPOT 均值约 7ms；无分块预填充时，在长 prefill 邻居序列期间 TPOT 可飙升至 50ms。永远监控 P99 而非均值。

Many names for one quantity. `TPOT` (time per output token), `ITL` (inter-token latency), `decode latency per token` — all the same. It is the time between consecutive streamed tokens after the first.

`TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced`

On the same Llama-3.3-70B H100 stack with chunked prefill, TPOT mean ~7 ms. Without chunked prefill, during a long prefill on a neighboring sequence, TPOT can spike to 50 ms. Watch P99, not mean.

### E2E latency

`E2E = TTFT + TPOT * output_tokens + network_response`

For long outputs (>500 tokens), E2E is TPOT-dominated. For short outputs with long prompts, E2E is TTFT-dominated. Report output-length-conditioned E2E.

### Throughput

`throughput = total_output_tokens / elapsed_time`

Aggregate metric. Tells you fleet efficiency. Does not tell you individual-request health.

### Goodput — the metric you actually care about

> **【中文解读】** Goodput 是唯一真正重要的综合指标。SLO 是多约束的——一个请求只有同时满足 TTFT <= a、TPOT <= b、E2E <= c 才算"好"。高吞吐量在 60% Goodput 时是失败；低吞吐量在 99% Goodput 时才是目标。2026 年 MLPerf Inference v6.0 和 AI 平台提供商的内部 SLA 追踪都以 Goodput 为核心指标。

`goodput = fraction of requests meeting (TTFT <= a) AND (TPOT <= b) AND (E2E <= c)`

The SLO is a multi-constraint. A request is "good" only if every constraint held. Goodput is the share. High throughput at 60% goodput is failure. Lower throughput at 99% goodput is the target.

In 2026, goodput is the metric used in MLPerf Inference v6.0 submissions and in internal SLA tracking at AI platform providers.

### Why mean is the wrong statistic

> **【中文解读】** LLM 延迟分布是右偏的。一个包含长 prefill 邻居的 decode batch 可能发出 500 个 TPOT ~7ms 的 token 和 20 个 TPOT ~60ms 的 token。均值 TPOT 是 9ms，但 P99 TPOT 是 65ms。用户经常遇到 P99——这就是他们离开的原因。永远报告三元组（P50, P90, P99），对于用户体验，P99 是需要优化的目标。

LLM latency distributions are right-skewed. A decode batch with one long-prefill neighbor can ship 500 tokens with TPOT ~7 ms and 20 tokens with TPOT ~60 ms. Mean TPOT is 9 ms. P99 TPOT is 65 ms. Users hit the P99 regularly — that is why they leave.

Always report the triple (P50, P90, P99). For user experience, P99 is the one you optimize.

### Reference numbers — Llama-3.1-8B-Instruct on TRT-LLM, 2026

- mean TTFT: 162 ms
- mean TPOT: 7.33 ms
- mean E2E: 1,093 ms
- P99 TPOT: varies 10-25 ms depending on chunked-prefill configuration.

These are the published NVIDIA reference points. They change with model size (70B would show 3-5x), hardware (H100 vs B200 ~3x), and load.

### The measurement trap

> **【中文解读】** 2026 年最常用的两个基准测试工具在 TPOT 上产生不同结果：NVIDIA GenAI-Perf 将 TTFT 从 ITL 计算中排除（从 token 2 开始），LLMPerf 包含 TTFT（从 token 1 开始）。同一个请求（TTFT 500ms、100 输出 token、700ms decode），GenAI-Perf 报告 ITL=7.07ms，LLMPerf 报告 ITL=12.00ms。永远说明使用哪个工具，永远发布定义。

> **【拓展：LLM 基准测试工具生态】** 2026 年 LLM 推理基准测试工具包括：(1) NVIDIA GenAI-Perf——Triton 客户端，全面指标覆盖，ITL 不含 TTFT；(2) LLMPerf（Anyscale）——Rust-backed 分词，流式感知，含 TTFT 的 ITL；(3) LLM-Locust（TrueFoundry）——Locust 扩展，修复了 GIL 问题；(4) guidellm——大规模合成基准测试；(5) k6 v2026.1.0——流式感知，Kubernetes-native。选择工具时要了解其 ITL 定义差异。

Two of the most-used 2026 benchmark tools disagree on TPOT for the same run:

- **NVIDIA GenAI-Perf**: excludes TTFT from the ITL calculation. ITL starts from token 2.
- **LLMPerf**: includes TTFT. ITL starts from token 1.

For a request with TTFT 500 ms and 100 output tokens in 700 ms total decode, GenAI-Perf reports `ITL = 700/99 = 7.07 ms`, LLMPerf reports `ITL = 1200/100 = 12.00 ms`. Tool choice changes the number.

Always state which tool. Always publish the definition.

### Constructing an SLO

> **【拓展：LLM SLO 设定参考】** 2026 年推荐的消费级 70B 对话模型 SLO：TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s（<300 token 输出）、Goodput >= 99%。企业级 SLO 收紧 TTFT（200-400ms）但放宽 E2E。测量方法：使用真实流量或 LLMPerf 合成流量（`--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`），目标 2x 峰值并发，运行 30-50 次迭代取百分位数。

A reasonable consumer-facing SLO for a 70B chat model in 2026:

- TTFT P99 <= 800 ms.
- TPOT P99 <= 25 ms.
- E2E P99 <= 3 s for <300-token outputs.
- Goodput target >= 99%.

Enterprise SLOs tighten TTFT (200-400 ms) and loosen E2E. The point is to write them down, measure all three, and track goodput as a single composite.

### How to measure

- Run real traffic or realistic synthetic (LLMPerf with `--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`).
- Target 2x peak concurrency for the benchmark run.
- Run 30-50 iterations, take percentiles of the combined sample.
- Publish with tool name, tool version, model, hardware, concurrency, prompt distribution.

## 用框架实现 | 使用方法

`code/main.py` is a toy goodput calculator. Generate a synthetic latency distribution, apply an SLO, and compute goodput. Also shows the GenAI-Perf vs LLMPerf TPOT difference on the same trace.

## 产出物 | 部署上线

> **【拓展：SLO 设定与 Goodput 门控】** 2026 年推荐的 70B 对话模型 SLO：TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s（<300 token 输出）、Goodput 目标 >= 99%。企业级 SLO 收紧 TTFT（200-400ms）但放宽 E2E。关键实践：(1) 在 CI/CD 中 gate 部署决策于 Goodput 而非吞吐量；(2) 用 2x 峰值并发运行基准测试；(3) 运行 30-50 次迭代取百分位数；(4) 发布时标注工具名、版本、模型、硬件、并发数、提示分布。

This lesson produces `outputs/skill-slo-goodput-gate.md`. Given a workload and SLO, it produces a CI/CD-ready benchmark recipe that gates deploys on goodput rather than throughput.

## 练习题 | 练习题

1. Run `code/main.py`. Generate a distribution with 1% tail spike. How does goodput change when you tighten P99 TPOT from 30 ms to 15 ms?
2. A vendor quotes "15,000 tok/s on Llama 3.3 70B H100". Name three questions to ask before trusting it.
3. Why does chunked prefill protect P99 TPOT but not mean TPOT?
4. Construct a consumer SLO for a voice assistant (first token is heard, not read). Which metric is most user-visible?
5. Read the LLMPerf README and the GenAI-Perf docs. Identify three other metrics where the tools disagree.

## 术语速查表 | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| TTFT | "time to first token" | Queue + network + prefill; dominated by prefill at long prompts |
| TPOT | "time per output token" | Memory-bound decode cost per token after first |
| ITL | "inter-token latency" | Same as TPOT in most tools (not all — see GenAI-Perf) |
| E2E | "end to end" | TTFT + TPOT * output_len; response-side network on top |
| Throughput | "tok/s" | Fleet efficiency; useless without latency percentiles |
| Goodput | "SLO-met rate" | Fraction of requests meeting every SLO constraint simultaneously |
| P99 | "tail" | 1-in-100 worst-case latency; the user experience metric |
| SLO multi-constraint | "the joint" | AND of all three latency bounds; a request fails if any one is violated |
| GenAI-Perf vs LLMPerf | "the tool trap" | Tools disagree on whether ITL includes TTFT |

## 延伸阅读 | 延伸阅读

- [NVIDIA NIM — LLM Benchmarking Metrics](https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html) — canonical definition of TTFT, ITL, TPOT.
- [Anyscale — LLM Serving Benchmarking Metrics](https://docs.anyscale.com/llm/serving/benchmarking/metrics) — alternative definitions and measurement recipe.
- [BentoML — LLM Inference Metrics](https://bentoml.com/llm/inference-optimization/llm-inference-metrics) — applied measurement on real deployments.
- [LLMPerf](https://github.com/ray-project/llmperf) — Ray-based open-source benchmark.
- [GenAI-Perf](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/client/src/c++/perf_analyzer/genai-perf/README.html) — NVIDIA's benchmark tool.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/) — the industry-accepted goodput-based benchmark.
