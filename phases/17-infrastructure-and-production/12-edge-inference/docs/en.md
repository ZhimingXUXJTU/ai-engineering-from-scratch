# Edge Inference — Apple Neural Engine, Qualcomm Hexagon, WebGPU/WebLLM, Jetson | 推理 边缘 LLM GPU 欧盟

> The core edge constraint is memory bandwidth, not compute. Mobile DRAM sits at 50-90 GB/s; datacenter HBM3 clears 2-3 TB/s — a 30-50x gap. Decode is memory-bound so the gap is decisive. In 2026 the landscape splits four ways. Apple M4/A18 Neural Engine peaks at 38 TOPS with unified memory (no CPU↔NPU copy). Qualcomm Snapdragon X Elite / 8 Gen 4 Hexagon hits 45 TOPS. WebGPU + WebLLM runs Llama 3.1 8B (Q4) at ~41 tok/s on M3 Max (roughly 70-80% of native); 17.6k GitHub stars, OpenAI-compatible API, ~70-75% mobile coverage. NVIDIA Jetson Orin Nano Super (8GB) fits Llama 3.2 3B / Phi-3; AGX Orin runs gpt-oss-20b via vLLM at ~40 tok/s; Jetson T4000 (JetPack 7.1) is 2x AGX Orin. TensorRT Edge-LLM supports EAGLE-3, NVFP4, chunked prefill — shown at CES 2026 by Bosch, ThunderSoft, MediaTek.

> **【中文解读】** 本节介绍了边缘推理——在边缘设备上部署 LLM 的挑战和方案。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy bandwidth-bound decode simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 09 (Production Quantization) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 09 (Production Quantization)

> 🔗 **【前置】** 学本节前请先掌握：Phase 17·04（vLLM）、Phase 17·09（量化）。边缘推理核心约束 = 内存带宽（不是算力）。
> 💡 **【类比】** 边缘 vs 数据中心 = "手机 vs 超算"。手机 DRAM 50-90 GB/s，数据中心 HBM3 2-3 TB/s——30-50 倍差距，解码（内存绑定）下决定性。2026 四大平台：Apple NE（38 TOPS 统一内存）、Qualcomm Hexagon（45 TOPS）、WebGPU+WebLLM（M3 Max 跑 Llama 3.1 8B 41 tok/s）、Jetson（Orin AGX 跑 gpt-oss-20b 40 tok/s）。TensorRT Edge-LLM 支持 EAGLE-3 + NVFP4 + chunked prefill。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Learning Objectives | 学习目标

- Explain why mobile LLM inference is memory-bandwidth-bound and compute is secondary.
  中文翻译：解释为什么移动 LLM 推理是内存带宽受限的，而计算能力是次要的。
- Enumerate the four edge targets (Apple ANE, Qualcomm Hexagon, WebGPU/WebLLM, NVIDIA Jetson) and match each to a use case.
  中文翻译：列举四个边缘目标（Apple ANE、Qualcomm Hexagon、WebGPU/WebLLM、NVIDIA Jetson）并匹配每个的用例。
- Name the 2026 WebGPU coverage gap (Firefox Android catching up) and the Safari iOS 26 landing.
  中文翻译：说出 2026 年 WebGPU 覆盖缺口（Firefox Android 赶追中）和 Safari iOS 26 落地。
- Pick a quantization format per target (Core ML INT4 + FP16 for ANE, QNN INT8/INT4 for Hexagon, WebGPU Q4 for browser, NVFP4 for Jetson Thor).
  中文翻译：为每个目标选择量化格式（ANE 用 Core ML INT4 + FP16，Hexagon 用 QNN INT8/INT4，浏览器用 WebGPU Q4，Jetson Thor 用 NVFP4）。

## The Problem | 问题引入

> **【中文解读】** 边缘推理的核心约束是内存带宽而非计算能力。移动 DRAM 带宽 50-90 GB/s，数据中心 HBM3 达 2-3 TB/s——30-50x 差距。由于 decode 阶段是内存带宽受限的，这个差距是决定性的。7B 模型 Q4 量化后权重 3.5GB，在 50 GB/s 带宽下读取需要 70ms——理论上限仅约 14 tok/s。2026 年边缘推理是四个不同的平台、四种不同的解决方案。

> **【拓展：边缘 AI 芯片市场】** 2026 年边缘 AI 芯片的竞争格局：(1) Apple Neural Engine (M4/A18)——38 TOPS，统一内存架构，无需 CPU↔NPU 数据拷贝；(2) Qualcomm Hexagon (Snapdragon X Elite / 8 Gen 4)——45 TOPS，QNN SDK 提供转换链路；(3) Intel Lunar Lake / AMD Ryzen AI 300——40-50 TOPS，软件生态落后于 Apple/Qualcomm；(4) NVIDIA Jetson Orin/Thor——边缘 GPU 方案，支持 vLLM 和 TensorRT Edge-LLM。语音代理是边缘推理的杀手级应用——本地推理完全消除网络延迟。

A customer wants an on-device chatbot: voice-first, private-by-default, works offline. On a MacBook Pro M3 Max, Llama 3.1 8B Q4 runs at ~55 tok/s — fine. On an iPhone 16 Pro, the same model runs at 3 tok/s — not fine. On a mid-range Android with Snapdragon 8 Gen 3, 7 tok/s. In the browser via WebGPU on Chrome Android v121+, 4-8 tok/s depending on the device.

The throughput variance is not a porting issue. It is the bandwidth gap times the quantization format times whether the NPU is accessible from user-space. Edge inference in 2026 is four different problems with four different solutions.

## The Concept | 核心概念

### Bandwidth is the real ceiling

> **【中文解读】** 边缘推理的真正天花板是内存带宽。Decode 阶段每生成一个 token 需要读取全部权重。7B Q4 模型 3.5GB，在 50 GB/s 带宽下读取需 70ms——理论上限仅约 14 tok/s。在 90 GB/s（高端移动 DRAM）下上限升至约 25 tok/s。数据中心 HBM3 在 3 TB/s 下读取同一模型仅需 1.2ms——上限 830 tok/s。同样的模型、同样的权重、不同的内存子系统。

Decode reads the full set of weights for every token. One 7B model in Q4 is 3.5 GB. Reading 3.5 GB at 50 GB/s takes 70 ms — a theoretical ceiling of ~14 tok/s. At 90 GB/s (high-end mobile DRAM) the ceiling moves to ~25 tok/s. No amount of compute helps below this number.

Datacenter HBM3 at 3 TB/s clears the same 3.5 GB in 1.2 ms — ceiling is 830 tok/s. Same model, same weights. Different memory subsystem.

### Apple Neural Engine (M4 / A18)

- Up to 38 TOPS. Unified memory (CPU and ANE share the same pool) — no copy overhead.
- Access via Core ML + `.mlmodel` compiled models, or via Metal Performance Shaders (MPS) through PyTorch.
- Llama.cpp Metal backend uses MPS, not ANE directly; native ANE requires Core ML conversion.
- Best practical path for iOS apps in 2026: Core ML with INT4 weights + FP16 activations.

### Qualcomm Hexagon (Snapdragon X Elite / 8 Gen 4)

- Up to 45 TOPS. Integrated with CPU and GPU in the SoC but separate memory domain.
- QNN (Qualcomm Neural Network) SDK and AI Hub provide conversion from PyTorch/ONNX.
- Chat templates, Llama 3.2, Phi-3 all ship as first-class artifacts on AI Hub.

### Intel / AMD NPUs (Lunar Lake, Ryzen AI 300)

- 40-50 TOPS. Software lags behind Apple/Qualcomm; OpenVINO is improving but niche.
- Best for Windows ARM copilot apps; native on AMD/Intel desktops for local-first.

### WebGPU + WebLLM

> **【中文解读】** WebGPU + WebLLM 是浏览器内 LLM 推理的方案——无需安装，通过 WebGPU compute shader 运行模型。在 M3 Max 上 Llama 3.1 8B Q4 达到 ~41 tok/s，约为原生性能的 70-80%。2026 年覆盖率：Chrome Android v121+、Safari iOS 26 GA、Firefox Android 仍在追赶，总体约 70-75% 移动浏览器覆盖。17.6k GitHub stars，OpenAI 兼容的 JavaScript API。

- Run models in the browser via WebGPU compute shaders; no install.
- Llama 3.1 8B Q4 at ~41 tok/s on M3 Max — roughly 70-80% of native via same backend.
- 17.6k GitHub stars on WebLLM; OpenAI-compatible JS API; Apache 2.0.
- 2026 coverage: Chrome Android v121+, Safari iOS 26 GA, Firefox Android still catching up. Overall ~70-75% mobile coverage.

### NVIDIA Jetson family

- Orin Nano Super (8GB): fits Llama 3.2 3B, Phi-3 at good tok/s.
- AGX Orin: runs gpt-oss-20b via vLLM at ~40 tok/s.
- Thor / T4000 (JetPack 7.1): 2x AGX Orin performance, EAGLE-3 and NVFP4 supported.
- TensorRT Edge-LLM (2026) supports EAGLE-3 speculative decoding, NVFP4 weights, chunked prefill — the datacenter optimizations ported to edge.

### Quantization choice per target

| Target | Format | Notes |
|--------|--------|-------|
| Apple ANE | INT4 weights + FP16 activations | Core ML conversion path |
| Qualcomm Hexagon | QNN INT8 / INT4 | AI Hub converters |
| WebGPU / WebLLM | Q4 MLC (q4f16_1) | Use `mlc_llm convert_weight` + compiled `.wasm`; GGUF is not supported |
| Jetson Orin Nano | Q4 GGUF or TRT-LLM INT4 | Memory-bound |
| Jetson AGX / Thor | NVFP4 + FP8 KV | Edge-LLM path |

### The long-context trap on edge

> **【中文解读】** 边缘设备上的长上下文陷阱：Llama 3.1 的 128K 上下文是数据中心特性。在 8GB RAM 的手机上，4GB 模型 + 2GB KV Cache（32K tokens）+ 系统开销 = OOM。边缘部署通常将上下文限制在 4K-8K，除非使用激进的 KV 量化（Q4 KV）。

> **【拓展：边缘推理的隐私优势】** 边缘推理在隐私敏感场景中有独特优势：(1) 医疗——患者数据不离开设备；(2) 金融——交易分析在本地完成；(3) 法律——律师-客户通信不上传云端；(4) 军事/政府——完全离线运行。2026 年 Apple Intelligence 的"Private Cloud Compute"是一个折中方案——简单任务在设备上完成，复杂任务在 Apple 专有云上处理但承诺不存储数据。这种"设备优先、云端后备"的模式正在成为行业标准。

Llama 3.1's 128K context is a datacenter feature. On a phone with 8 GB RAM, 4 GB model + 2 GB KV cache for 32K tokens + OS overhead = OOM. Edge deployments keep context at 4K-8K unless aggressive KV quantization (Q4 KV) is accepted.

### Voice is the killer app

> **【拓展：边缘推理的应用场景】** 边缘推理的杀手级应用是语音代理——语音 Agent 对延迟极度敏感（首 token < 500ms）。本地推理完全消除网络延迟。结合语音转文字（Whisper Turbo 变体在边缘运行），边缘推理成为生产质量的语音环路。其他场景包括：隐私优先的医疗/金融分析、离线代码补全、实时翻译。Apple 的"Private Cloud Compute"是一种折中——简单任务设备端完成，复杂任务在 Apple 专有云处理但承诺不存储数据。

Voice agents are latency-sensitive (first token < 500 ms). Local inference eliminates network latency entirely. Combine with speech-to-text (Whisper Turbo variants run on edge) and edge inference becomes the production-quality voice loop.

### Numbers you should remember

- Apple M4 / A18 ANE: 38 TOPS.
- Qualcomm Hexagon SD X Elite: 45 TOPS.
- WebLLM M3 Max: ~41 tok/s on Llama 3.1 8B Q4.
- AGX Orin: ~40 tok/s on gpt-oss-20b via vLLM.
- Datacenter-edge bandwidth gap: 30-50x.
- WebGPU mobile coverage: ~70-75% (Firefox Android lagging).

## Use It | 用框架实现

`code/main.py` computes theoretical decode throughput ceilings from bandwidth-bound math across edge targets. Compares to observed benchmarks and highlights where bandwidth, not compute, is the bottleneck.

> `code/main.py` 从带宽受限数学计算各边缘目标的理论解码吞吐量上限。与观察到的基准比较，强调瓶颈在带宽而非计算。

## Ship It | 产出物

This lesson produces `outputs/skill-edge-target-picker.md`. Given platform (iOS/Android/browser/Jetson), model, and latency/memory budget, picks a quantization format and conversion pipeline.

> 本课产出 `outputs/skill-edge-target-picker.md`。给定平台（iOS/Android/浏览器/Jetson）、模型和延迟/内存预算，选择量化格式和转换管线。

## Exercises | 练习题

1. Run `code/main.py`. For a 7B model in Q4 on a Snapdragon 8 Gen 3 (~77 GB/s bandwidth), compute the decode ceiling. Compare to observed 6-8 tok/s — is the runtime efficient?
   中文翻译：运行 `code/main.py`。计算 Snapdragon 8 Gen 3（约 77 GB/s 带宽）上 Q4 7B 模型的解码上限。与观察到的 6-8 tok/s 比较——运行时是否高效？
2. WebGPU on Android requires Chrome v121+. Design a fallback for older browsers — server-side via the same OpenAI-compatible API.
   中文翻译：Android 上的 WebGPU 需要 Chrome v121+。为旧浏览器设计回退方案——通过相同的 OpenAI 兼容 API 实现服务端推理。
3. Your iOS app needs 4K-context streaming. Which model/format combination lets you stay under 4 GB active memory on an iPhone 16?
   中文翻译：你的 iOS 应用需要 4K 上下文流式输出。哪种模型/格式组合可以在 iPhone 16 上保持在 4GB 活跃内存以内？
4. Jetson AGX Orin runs gpt-oss-20b at 40 tok/s. Jetson Nano fits only a 3B. If your product targets both, how do you unify the inference stack?
   中文翻译：Jetson AGX Orin 以 40 tok/s 运行 gpt-oss-20b。Jetson Nano 只能运行 3B 模型。如果你的产品同时针对两者，如何统一推理栈？
5. Argue whether "WebLLM is production-ready in 2026." Cite the coverage, performance, and the Firefox Android gap.
   中文翻译：论证“WebLLM 在 2026 年是否生产就绪”。引用覆盖率、性能和 Firefox Android 缺口。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| ANE | "Apple neural engine" | On-device NPU in M-series and A-series; unified memory |
| Hexagon | "Qualcomm NPU" | Snapdragon NPU; QNN SDK for access |
| WebGPU | "browser GPU" | W3C-standardized browser GPU API; Chrome/Safari 2026 |
| WebLLM | "browser LLM runtime" | MLC-LLM project; Apache 2.0; OpenAI-compatible JS |
| Jetson | "NVIDIA edge" | Orin Nano / AGX / Thor / T4000 family |
| TRT Edge-LLM | "edge TensorRT" | 2026 edge port of TensorRT-LLM; EAGLE-3 + NVFP4 |
| Unified memory | "shared pool" | CPU and NPU see same RAM; no copy overhead |
| Bandwidth-bound | "memory limited" | Decode gated by bytes/sec reading weights |
| Core ML | "Apple conversion" | Apple framework for ANE-native models |
| QNN | "Qualcomm stack" | Qualcomm Neural Network SDK |

## Further Reading | 延伸阅读

- [On-Device LLMs State of the Union 2026](https://v-chandra.github.io/on-device-llms/) — landscape and benchmarks.
- [NVIDIA Jetson Edge AI](https://developer.nvidia.com/blog/getting-started-with-edge-ai-on-nvidia-jetson-llms-vlms-and-foundation-models-for-robotics/) — Orin / AGX / Thor.
- [NVIDIA TensorRT Edge-LLM](https://developer.nvidia.com/blog/accelerating-llm-and-vlm-inference-for-automotive-and-robotics-with-nvidia-tensorrt-edge-llm/) — 2026 edge port announcement.
- [WebLLM (arXiv:2412.15803)](https://arxiv.org/html/2412.15803v2) — design and benchmarks.
- [Apple Core ML](https://developer.apple.com/documentation/coreml) — ANE-native conversion.
- [Qualcomm AI Hub](https://aihub.qualcomm.com/) — pre-converted models for Hexagon.
