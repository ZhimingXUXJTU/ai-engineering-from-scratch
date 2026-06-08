# Self-Hosted Serving Selection — llama.cpp, Ollama, TGI, vLLM, SGLang | 自托管 选择 服务 SGLang vLLM

> Four engines dominate self-hosted inference in 2026. Pick based on hardware, scale, and ecosystem. **llama.cpp** is fastest on CPU — widest model support, full control over quantization and threading. **Ollama** is the dev-laptop one-command install, ~15-30% slower than llama.cpp (Go + CGo + HTTP serialization), 3x throughput gap under prod-like load. **TGI entered maintenance mode December 11, 2025** — only bug fixes, ~10% slower raw throughput than vLLM but historically top observability and HF-ecosystem integration. That maintenance status makes it a risky long-term bet — SGLang or vLLM are safer defaults for new projects. **vLLM** is the general-purpose production default — v0.15.1 (February 2026) adds PyTorch 2.10, RTX Blackwell SM120, H200 optimization. **SGLang** is the agentic multi-turn / prefix-heavy specialist — 400,000+ GPUs in production (xAI, LinkedIn, Cursor, Oracle, GCP, Azure, AWS). Hardware constraints: CPU-only → llama.cpp only. AMD / non-NVIDIA → vLLM only (TRT-LLM is NVIDIA-locked). 2026 pipeline pattern: dev = Ollama, staging = llama.cpp, prod = vLLM or SGLang. Same GGUF/HF weights throughout.

> **【中文解读】** 本节介绍了自托管推理服务选型——vLLM、TGI、llama.cpp 等框架的对比和选择。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, engine-decision tree walker) | **语言:** Python
**Prerequisites:** All Phase 17 lessons covering engines (04, 06, 07, 09, 18) | **前置知识:** All Phase 17 lessons covering engines (04, 06, 07, 09, 18)
**Time:** ~45 minutes | **时间:** ~45 minutes

## Learning Objectives | 学习目标

- Pick an engine given hardware (CPU / AMD / NVIDIA Hopper / Blackwell), scale (1 user / 100 / 10,000), and workload (general chat / agent / long-context).
  中文翻译：给定硬件（CPU/AMD/NVIDIA Hopper/Blackwell）、规模和工作负载选择引擎。
- Name the 2026 TGI maintenance-mode status (December 11, 2025) and why it biases new projects toward vLLM or SGLang.
  中文翻译：说出 2026 年 TGI 维护模式状态（2025 年 12 月 11 日）以及它为什么影响使用 HuggingFace 默认设置的团队。
- Describe the dev/staging/prod pipeline using the same GGUF or HF weights throughout.
  中文翻译：描述在整个生命周期中使用相同 GGUF 或 HF 权重的开发/预发布/生产流水线。
- Explain why "CPU only" forces llama.cpp and "AMD" excludes TRT-LLM.
  中文翻译：解释为什么"仅 CPU"强制使用 llama.cpp 而"AMD"排除了 TRT-LLM。

## The Problem | 问题引入

> **【中文解读】** 自托管推理引擎的选择取决于三个维度：硬件（CPU / AMD / NVIDIA Hopper / Blackwell）、规模（1 用户 / 100 / 10,000）、工作负载（通用聊天 / Agent / 长上下文）。2025 年 12 月 11 日 HuggingFace TGI 进入维护模式（仅 bug fix），这使得新项目应默认远离 TGI，转向 vLLM 或 SGLang。2026 年的流水线模式是：开发用 Ollama，预发布用 llama.cpp，生产用 vLLM 或 SGLang——全程使用相同的 GGUF/HF 权重。

> **【拓展：2026 年推理引擎选择决策】** 2026 年推理引擎的硬件优先决策树：(1) CPU-only → llama.cpp（唯一有竞争力的选项）；(2) AMD GPU → vLLM（ROCm 支持），TRT-LLM 不支持 AMD；(3) NVIDIA Hopper → vLLM 或 SGLang 或 TRT-LLM（三选一）；(4) NVIDIA Blackwell → TRT-LLM 吞吐最高；(5) Apple Silicon → llama.cpp（Metal 后端）。规模决策：1 用户→Ollama，10-100→vLLM 单 GPU，100-10K→vLLM production-stack 或 SGLang，10K+→production-stack + 分离式 + LMCache。

Your team starts a new self-hosted LLM project. One engineer says Ollama, another says vLLM, a third says "doesn't TGI just work out of the box?" All three are right for different contexts. None is right for all.

In 2026 the choice tree matters: hardware first, scale second, workload third. And one specific 2025 event — TGI entering maintenance mode December 11 — changes the default for new projects.

## The Concept | 核心概念

### The five engines

| Engine | Best for | Notes |
|--------|----------|-------|
| **llama.cpp** | CPU / edge / minimal deps / widest model support | Fastest on CPU, full control |
| **Ollama** | Dev laptops, single user, one-command install | 15-30% slower than llama.cpp; 3x prod throughput gap |
| **TGI** | HF ecosystem, regulated industries | **Maintenance mode Dec 11, 2025** |
| **vLLM** | General-purpose production, 100+ users | Broad production default; v0.15.1 Feb 2026 |
| **SGLang** | Agentic multi-turn, prefix-heavy workloads | 400,000+ GPUs in production |

### Hardware-first decision

**CPU only** → llama.cpp. Ollama works too but is slower. No other engine is competitive on CPU.

**AMD GPU** → vLLM (AMD ROCm support). SGLang also works. TRT-LLM is NVIDIA-locked, so it's out.

**NVIDIA Hopper (H100 / H200)** → vLLM or SGLang or TRT-LLM. All three top-tier.

**NVIDIA Blackwell (B200 / GB200)** → TRT-LLM is the throughput leader (Phase 17 · 07). vLLM and SGLang follow close.

**Apple Silicon (M-series)** → llama.cpp (Metal). Ollama wraps this.

### Scale-second decision

**1 user / local dev** → Ollama. One command, first-token in seconds.

**10-100 users / small team** → vLLM single-GPU.

**100-10k users / production** → vLLM production-stack (Phase 17 · 18) or SGLang.

**10k+ users / enterprise** → vLLM production-stack + disaggregated (Phase 17 · 17) + LMCache (Phase 17 · 18).

### Workload-third decision

**General chat / Q&A** → vLLM wins on broad default.

**Agentic multi-turn (tools, planning, memory)** → SGLang's RadixAttention (Phase 17 · 06) dominates.

**RAG with heavy prefix reuse** → SGLang.

**Code generation** → vLLM fine; SGLang slightly better on cache.

**Long context (128K+)** → vLLM + chunked prefill; SGLang + tiered KV.

### The TGI maintenance trap

> **【中文解读】** TGI 陷阱：HuggingFace TGI 在 2025 年 12 月 11 日进入维护模式——仅 bug fix，不再有功能更新。历史上 TGI 有顶级的可观测性和 HF 生态集成（模型卡、安全工具），原始吞吐略低于 vLLM（约 10%）。对于 2026 年的新项目，应默认远离 TGI。现有 TGI 部署可以继续运行，但应规划迁移。SGLang 和 vLLM 是更安全的默认选择。

> **【拓展：工作负载驱动的引擎选择】** 工作负载维度驱动引擎选择：(1) 通用聊天/问答 → vLLM（广泛默认）；(2) Agent 多轮对话（工具、规划、记忆）→ SGLang RadixAttention 主导；(3) RAG 重前缀复用 → SGLang；(4) 代码生成 → vLLM 足够，SGLang 缓存略好；(5) 长上下文（128K+）→ vLLM + 分块预填充，SGLang + 分层 KV。Ollama 适合开发但不是生产共享服务的理想选择——Go HTTP 序列化增加开销、并发管理比 vLLM 简单、OpenTelemetry 支持滞后。

Hugging Face TGI entered maintenance mode December 11, 2025 — only bug fixes going forward. Historically: top-tier observability, best-in-class HF-ecosystem integration (model cards, safety tools), slightly behind vLLM on raw throughput.

For new projects in 2026: default away from TGI. Existing TGI deployments can continue but should migrate eventually. SGLang and vLLM are the safer defaults.

### The pipeline pattern

Dev (Ollama) → staging (llama.cpp) → prod (vLLM). Same GGUF or HF weights throughout. Engineers iterate quickly on laptops; staging mirrors production quantization; prod is the serving target.

### Ollama caveat

Ollama is great for dev. It is not great for shared production: Go HTTP serialization adds overhead, concurrency management is simpler than vLLM, OpenTelemetry support lags. Use Ollama where it shines — one user, one command — and switch to vLLM for shared.

### Self-hosted vs managed is a separate decision

Phase 17 · 01 (managed hyperscalers), · 02 (inference platforms) cover managed. This lesson assumes you've already decided to self-host. Reasons to self-host: data residency, custom fine-tune, total cost ownership at scale, domain model not available on hosted.

### Numbers you should remember

- TGI maintenance mode: December 11, 2025.
- vLLM v0.15.1: February 2026; PyTorch 2.10; Blackwell SM120 support.
- SGLang production footprint: 400,000+ GPUs.
- Ollama throughput gap vs llama.cpp: 15-30% slower; 3x under prod load.

## Use It | 用框架实现

`code/main.py` is a decision-tree walker: given hardware + scale + workload, picks an engine and explains why.

> `code/main.py` is a decision-tree walker: given hardware + scale + workload, picks an engine and explains why.

## Ship It | 产出物

> **【拓展：自托管 vs 托管的决策】** 自托管 vs 托管是独立的决策。自托管的理由：(1) 数据驻留——数据不能离开组织；(2) 自定义微调——LoRA/QLoRA 适配器需要本地部署；(3) 大规模总拥有成本——年推理支出超过 $5M 时自托管通常更经济；(4) 领域模型不在托管平台上可用。Phase 17·01（托管 hyperscaler）和 ·02（推理平台）覆盖了托管选项。2026 年的混合模式也很常见：实验层用托管（快速迭代），生产层用自托管（成本控制）。

This lesson produces `outputs/skill-engine-picker.md`. Given constraints, picks an engine and writes the migration plan.

> 本课产出 `outputs/skill-engine-picker.md`. Given constraints, picks an engine and writes the migration plan.

## Exercises | 练习题

1. Run `code/main.py` with your hardware / scale / workload. Does the output match your intuition?
   中文翻译：用你的硬件/规模/工作负载运行 `code/main.py`。输出是否符合预期？
2. Your infra is 12 H100s and 8 MI300X AMD. What engine? Why is TRT-LLM off the table?
   中文翻译：你的基础设施是 12 块 H100 和 8 块 MI300X AMD。用什么引擎？为什么 TRT-LLM 不可选？
3. A team wants to use TGI in 2026 because "it's what we know." Argue the migration case.
   中文翻译：一个团队想在 2026 年使用 TGI 因为"这是我们熟悉的"。论证迁移的理由。
4. Ollama dev to vLLM prod: what changes in quantization, configuration, and observability?
   中文翻译：Ollama 开发到 vLLM 生产：量化、配置和可观测性有什么变化？
5. RAG product with P99 prefix length 8K and high reuse across tenants. Pick an engine and stack it with Phase 17 · 11 + 18.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| llama.cpp | "the CPU one" | Widest model support, fastest on CPU |
| Ollama | "the laptop one" | One-command install, dev-grade throughput |
| TGI | "HF's serving" | Maintenance mode since Dec 2025 |
| vLLM | "the default" | Broad production baseline 2026 |
| SGLang | "the agentic one" | Prefix-heavy, RadixAttention |
| TRT-LLM | "NVIDIA-locked" | Blackwell throughput leader, NVIDIA only |
| GGUF | "llama.cpp format" | Bundled K-quant variants |
| Production-stack | "vLLM K8s" | Phase 17 · 18 reference deployment |
| Pipeline pattern | "dev→stage→prod" | Ollama → llama.cpp → vLLM on same weights |

## Further Reading | 延伸阅读

- [AI Made Tools — vLLM vs Ollama vs llama.cpp vs TGI 2026](https://www.aimadetools.com/blog/vllm-vs-ollama-vs-llamacpp-vs-tgi/)
- [Morph — llama.cpp vs Ollama 2026](https://www.morphllm.com/comparisons/llama-cpp-vs-ollama)
- [n1n.ai — Comprehensive LLM Inference Engine Comparison](https://explore.n1n.ai/blog/llm-inference-engine-comparison-vllm-tgi-tensorrt-sglang-2026-03-13)
- [PremAI — 10 Best vLLM Alternatives 2026](https://blog.premai.io/10-best-vllm-alternatives-for-llm-inference-in-production-2026/)
- [TGI maintenance announcement](https://github.com/huggingface/text-generation-inference) — release notes.
- [vLLM v0.15.1 release notes](https://github.com/vllm-project/vllm/releases)
