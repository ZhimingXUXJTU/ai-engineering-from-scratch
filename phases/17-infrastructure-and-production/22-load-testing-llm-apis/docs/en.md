# Load Testing LLM APIs — Why k6 and Locust Lie | 负载测试 API 为什么 LLM 美国

> Traditional load testers were not designed for streaming responses, variable output lengths, token-level metrics, or GPU saturation. Two traps bite most teams. The GIL trap: Locust's token-level measurement runs tokenization under the Python GIL, which competes with request generation under heavy concurrency; tokenization backlog then inflates reported inter-token latency — your client is the bottleneck, not the server. The prompt-uniformity trap: identical prompts in a loop test one point on the token distribution; real traffic has variable length and diverse prefix matches. LLMPerf fixes this with `--mean-input-tokens` + `--stddev-input-tokens`. Tool mapping in 2026: LLM-specialized (GenAI-Perf, LLMPerf, LLM-Locust, guidellm) for token-level accuracy; **k6 v2026.1.0** + **k6 Operator 1.0 GA (Sept 2025)** — streaming-aware, Kubernetes-native distributed via TestRun/PrivateLoadZone CRDs, best for CI/CD gates; Vegeta for Go constant-rate saturation; Locust 2.43.3 only with LLM-Locust extension for streaming. Load patterns: steady-state, ramp, spike (autoscaling test), soak (memory leaks).

> **【中文解读】** 本节介绍了 LLM API 负载测试——评估推理服务在高负载下表现的测试方法。


**Type:** Build | **类型:** 学习
**Languages:** Python (stdlib, toy realistic-prompt generator + latency collector) | **语言:** Python
**Prerequisites:** Phase 17 · 08 (Inference Metrics), Phase 17 · 03 (GPU Autoscaling) | **前置知识:** Phase 17 · 08 (Inference Metrics), Phase 17 · 03 (GPU Autoscaling)
**Time:** ~75 minutes | **时间:** ~75 minutes

## Learning Objectives | 学习目标

- Explain the two anti-patterns (GIL trap, prompt-uniformity trap) that make generic load testers lie for LLM APIs.
  中文翻译：解释两个反模式（GIL 陷阱、提示均匀性陷阱），它们使通用负载测试工具产生误导。
- Pick a tool for a given purpose: LLMPerf (benchmark run), k6 + streaming extension (CI gate), guidellm (large-scale synthetic), GenAI-Perf (NVIDIA reference).
  中文翻译：选择工具——Harness、LitmusChaos、Chaos Mesh——根据技术栈。
- Design four load patterns (steady, ramp, spike, soak) and name the failure mode each catches.
  中文翻译：设计四种负载模式（稳态、递增、尖峰、浸泡）并说出每种捕获的故障模式。
- Build a realistic prompt distribution using mean + stddev of input tokens rather than fixed length.
  中文翻译：使用输入 token 的均值 + 标准差构建真实提示分布，而非固定长度。

## The Problem | 问题引入

> **【中文解读】** 传统负载测试工具不是为 LLM 设计的——它们不支持流式响应、可变输出长度、token 级指标或 GPU 饱和度。两个常见陷阱：(1) GIL 陷阱——Locust 的 token 级测量在 Python GIL 下运行分词，高并发时 tokenization 队列膨胀，虚报 inter-token 延迟（你的客户端是瓶颈，不是服务器）；(2) 提示均匀性陷阱——循环测试中使用相同提示，前缀缓存命中率接近 100%，吞吐量看起来很好但完全不反映真实流量。

> **【拓展：LLM 负载测试的四种模式】** 2026 年 LLM 负载测试的四种模式：(1) 稳态（steady-state）——恒定 RPS 持续 30-60 分钟，捕获基线性能退化；(2) 渐增（ramp）——从 0 线性增加到目标 RPS，捕获容量断点和预热异常；(3) 突发（spike）——突然 3-10x RPS 持续 2 分钟然后回落，测试自动扩缩响应、队列饱和和冷启动影响；(4) 长时间（soak）——稳态持续 4-8 小时，捕获内存泄漏、连接池漂移和可观测性溢出。

You k6-tested your LLM endpoint at 500 concurrent users. It held. You shipped. In production at 200 actual users the service fell over — P99 TTFT exploded, GPUs pinned.

Two things happened. First, k6 sent 500 identical prompts — your request-coalescing and prefix caching made it look like you were handling 500 concurrent decodes when you were actually handling one. Second, k6 doesn't track inter-token latency on streaming responses the way the eye experiences it; it sees one HTTP connection, not 500 tokens arriving at varying intervals.

Load testing for LLMs is its own discipline.

## The Concept | 核心概念

### The GIL trap (Locust)

> **【拓展：Python GIL 对 LLM 负载测试的影响】** Python GIL（全局解释器锁）对 LLM 负载测试的影响：Locust 使用 Python 运行客户端分词，在高并发时 tokenization 队列排在请求生成后面。报告的 inter-token 延迟包含客户端 tokenization 积压——你以为是服务器慢，其实是测试工具的瓶颈。解决方案：(1) LLM-Locust 扩展将 tokenization 移到独立进程；(2) 使用编译语言工具——k6（Go）、LLMPerf（Rust-backed tokenizers.rs）。这是 LLM 负载测试中最常见的陷阱之一。

Locust uses Python and runs tokenization client-side under the GIL. Under high concurrency the tokenizer queues behind request generation. Reported inter-token latency includes client-side tokenization backlog. You think the server is slow; it's the test harness.

Fix: LLM-Locust extension moves tokenization to separate processes, or use a compiled-language harness (k6, LLMPerf using tokenizers.rs).

### The prompt-uniformity trap

All known load testers let you configure one prompt. In a loop test of 10,000 iterations the exact same prompt sends each time. Server sees the same prefix every time — prefix cache hits approach 100%, throughput looks great.

Fix: sample from a prompt distribution. LLMPerf uses `--mean-input-tokens 500 --stddev-input-tokens 150` — diverse lengths, diverse content.

### Four load patterns

1. **Steady-state** — constant RPS for 30-60 min. Catches: baseline performance regressions.
2. **Ramp** — linearly increase RPS from 0 to target over 15 min. Catches: capacity breakpoint, warm-up anomalies.
3. **Spike** — sudden 3-10x RPS for 2 min then back. Catches: autoscaling latency, queue saturation, cold-start impact.
4. **Soak** — steady-state for 4-8 hours. Catches: memory leaks, connection-pool drift, observability overflow.

### 2026 tool mapping

> **【中文解读】** 2026 年 LLM 负载测试工具选择：(1) LLMPerf（Anyscale）——Rust-backed 分词 + 流式感知，性能测试的默认选择；(2) NVIDIA GenAI-Perf——NVIDIA 参考工具，注意其 ITL 不含 TTFT；(3) LLM-Locust（TrueFoundry）——Locust 扩展，修复 GIL 问题；(4) k6 v2026.1.0 + k6 Operator 1.0 GA（2025 年 9 月）——Go 编译、无 GIL、流式感知、Kubernetes-native 分布式测试，CI/CD gate 最佳选择。

> **【拓展：CI/CD 中的 SLA Gate】** 在 CI 中使用 k6 的 SLA gate 配置：每次 PR 运行 30-50 次迭代，gate 指标包括 P50/P95 TTFT、5xx < 5%、TPOT 在阈值以下。违规则构建失败。使用真实提示分布（mean + stddev of input tokens）而非固定长度——LLMPerf 使用 `--mean-input-tokens 500 --stddev-input-tokens 150` 生成多样化提示。

**LLMPerf** (Anyscale) — Python but Rust-backed tokenization. Mean/stddev prompts. Streaming-aware. Best default for performance runs.

**NVIDIA GenAI-Perf** — NVIDIA's reference. Uses Triton client; comprehensive metric coverage. Note its ITL excludes TTFT; LLMPerf's includes it. Two tools produce different TPOT for the same server.

**LLM-Locust** (TrueFoundry) — Locust extension that fixes the GIL trap. Familiar Locust DSL + streaming metrics.

**guidellm** — large-scale synthetic benchmarking.

**k6 v2026.1.0** + **k6 Operator 1.0 GA (Sept 2025)**:
- k6 itself (Go, compiled, no GIL) added streaming-aware metrics.
- k6 Operator uses TestRun / PrivateLoadZone CRDs for Kubernetes-native distributed testing.
- Best for CI/CD gates and SLA testing.

**Vegeta** — Go, simpler than k6. Constant-rate HTTP saturation. Not LLM-aware but good for gateway / rate-limit testing.

**Locust 2.43.3 stock** — has the GIL trap for LLM. Only with LLM-Locust extension.

### SLA gate in CI

Run k6 on the PR with:

- 30-50 iterations each at baseline RPS.
- Gate: P50/P95 TTFT, 5xx < 5%, TPOT under threshold.
- Break the build on breach.

### Realistic prompt distribution

Build from real traffic samples (if you have them) or from published distributions (e.g., ShareGPT prompts for chat, HumanEval for code). Feed the mean + stddev to LLMPerf. Avoid loop-with-one-prompt at all costs.

### Numbers you should remember

- k6 Operator 1.0 GA: September 2025.
- k6 v2026.1.0: streaming-aware metrics.
- Typical LLMPerf run: 100-1000 requests at concurrency X.
- Typical CI gate: 30-50 iterations per PR.
- Four patterns: steady, ramp, spike, soak.

## Use It | 用框架实现

`code/main.py` simulates a load test with realistic prompt distribution, measures effective TPOT, and demonstrates the uniform-prompt trap.

> `code/main.py` simulates a load test with realistic prompt distribution, measures effective TPOT, and demonstrates the uniform-prompt trap.

> `code/main.py` simulates a load test with realistic prompt distribution, measures effective TPOT, and demonstrates the uniform-prompt trap.

## Ship It | 产出物

This lesson produces `outputs/skill-load-test-plan.md`. Given workload and SLA, picks tool and designs the four load patterns.

> 本课产出 `outputs/skill-load-test-plan.md`. Given workload and SLA, picks tool and designs the four load patterns.

## Exercises | 练习题

1. Run `code/main.py`. Compare uniform vs realistic distribution — where is the gap?
   中文翻译：运行 `code/main.py`。比较均匀 vs 真实分布——P99 TTFT 差异在哪里？
2. Write the k6 script for a CI gate: TTFT P95 < 800 ms at 100 concurrent, runtime 5 minutes.
   中文翻译：编写 CI 门控的 k6 脚本：100 并发下 TTFT P95 < 800ms，运行 5 分钟。
3. Your soak test shows memory growing 50 MB/hour. Name three causes and the instrumentation to pick between them.
   中文翻译：你的浸泡测试显示内存每小时增长 50MB。说出三个原因和每个的调查方法。
4. Spike test from 10 RPS to 100 RPS. What's the expected recovery time if Karpenter + vLLM production-stack are in place (Phase 17 · 03 + 18)?
   中文翻译：从 10 RPS 尖峰测试到 100 RPS。如果 Karpenter 需要 45 秒供给，预期恢复时间是多少？
5. GenAI-Perf reports TPOT=6ms; LLMPerf reports TPOT=11ms on the same server. Explain.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| LLMPerf | "the LLM harness" | Anyscale benchmark tool, streaming-aware |
| GenAI-Perf | "NVIDIA tool" | NVIDIA reference harness |
| LLM-Locust | "Locust for LLMs" | Locust extension fixing GIL trap |
| guidellm | "synthetic benchmark" | Large-scale synthetic tool |
| k6 Operator | "K8s k6" | CRD-based distributed k6 |
| GIL trap | "Python client overhead" | Tokenization backlog inflates reported latency |
| Prompt-uniformity trap | "single-prompt lie" | Loop with same prompt hits cache, inflates throughput |
| Steady-state | "constant load" | Flat RPS for N minutes |
| Ramp | "linear up" | 0 to target over duration |
| Spike | "burst test" | Sudden multiplier then revert |
| Soak | "long test" | Hours for leak detection |

## Further Reading | 延伸阅读

- [TianPan — Load Testing LLM Applications](https://tianpan.co/blog/2026-03-19-load-testing-llm-applications)
- [PremAI — Load Testing LLMs 2026](https://blog.premai.io/load-testing-llms-tools-metrics-realistic-traffic-simulation-2026/)
- [NVIDIA NIM — Introduction to LLM Inference Benchmarking](https://docs.nvidia.com/nim/large-language-models/1.0.0/benchmarking.html)
- [TrueFoundry — LLM-Locust](https://www.truefoundry.com/blog/llm-locust-a-tool-for-benchmarking-llm-performance)
- [LLMPerf](https://github.com/ray-project/llmperf)
- [k6 Operator](https://github.com/grafana/k6-operator)
