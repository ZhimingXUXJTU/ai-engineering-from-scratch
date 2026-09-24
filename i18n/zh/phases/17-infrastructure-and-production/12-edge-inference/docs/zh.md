# 边缘传输 果神经引擎,高通六角,WebGPU/WebLLM,Jetson 推理 边缘LLM GPU 欧盟

> 核心边缘限制是内存带宽,而不是计算. 移动DRAM处于50-90GB/s;数据中心HBM3清除2-3TB/s30-50x差距. 解码是记忆的,所以差距是决定性的. 在2026年,这个景观分为四个部分. 果M4/A18神经引擎最高值为38TOPS,具有统一内存 (没有CPUNPU副本). 龙X精英/8代4六合集体达到45. 网络GPU + WebLLM 在M3 Max上运行Llama 3.1 8B (Q4) 速度为 ~ 41 tok/s (约为 70-80%的本土); 17.6k GitHub 星,OpenAI兼容的 API, ~ 70-75%的移动覆盖率. 飞机机的机器人是NVIDIA Jetson Orin Nano Super (8GB) 兼容Llama 3.2 3B / Phi-3; AGX Orin 通过vLLM 运行gpt-oss-20b 速度约为40个通/秒;Jetson T4000 (JetPack 7.1) 是2x AGX Orin. 讯RT Edge-LLM支持EAGLE-3,NVFP4,在2026年CES展览会上由博什,ThunderSoft,MediaTek展示的零碎预填料.

> **【中文解读】**本节介绍了在边缘设备上部署的 LLM 的挑战和方案.
**Type:** Learn
**Languages:** Python (stdlib, toy bandwidth-bound decode simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 09 (Production Quantization)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy bandwidth-bound decode simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 09 (Production Quantization) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 09 (Production Quantization)

>  **【前置】**学本节前请先掌握:阶段17·04(vLLM) 、阶段17·09(量化) ・・・边缘推理核心约束 = 内存带宽(不是算力) ・・・
>  **【类比】**边缘 VS 数据中心 = "手机 VS 超算"――手机 DRAM 50-90 GB/s,数据中心 HBM3 2-3 TB/s30-50 倍差距,解码(内存绑定) 下决定性。2026 四大平台:果 NE(38 TOPS 统一内存) 、Qualcomm Hexagon(45 TOPS)、WebGPU+WebLLM(M3 Max 跑 Llama 3.1 8B 41 tok/s)、Jetson(Orin AGX 跑 gpt-oss-20b 40 tok/s) ――TensorRT Edge-LLM 支持EAGLE-3 + NVFP4 + 切断预填充──
**Time:** ~60 minutes | **时间:** ~60 minutes

## 学习目标

- 解释为什么移动LLM推断是基于存储带宽的,计算是次要的.
  中文翻译:解释为什么移动LLM推理是内存带宽有限的,而计算能力是次要的.
- 列出四个边缘目标 (果ANE,高通六合,WebGPU/WebLLM,NVIDIA Jetson) 并将每个目标匹配一个使用情况.
  中文翻译:列举四个边缘目标(果ANE、Qualcomm六角形、WebGPU/WebLLM、NVIDIA Jetson) 并匹配每个用例──
- 举个2026 WebGPU 覆盖率差距 (Firefox Android 追赶) 和 Safari iOS 26 登陆的名称.
  中文翻译:说出 2026 年 WebGPU 覆盖缺口(Firefox Android 赶追中) 和Safari iOS 26 落地。
- 选择每个目标的量化格式 (ANE的核心ML INT4 + FP16,六角形的QNN INT8/INT4,浏览器的WebGPU Q4,Jetson Thor的NVFP4).
  中文翻译:为每个目标选择量化格式(ANE 用Core ML INT4 + FP16,角用QNN INT8/INT4,浏览器用WebGPU Q4,Jetson Thor用 NVFP4)。

## 问题 问题引入

> **【中文解读】**边缘推理的核心约束是内存带宽而不是计算能力――移动DRAM 带宽50-90GB/s,数据中心HBM3 达2-3TB/s30-50x 差距――由于解码阶段是内存带宽限定的,这个差距是决定性的――7B模型Q4 量化后权重3.5GB,在50GB/s 带宽下不同的读取需要70ms理论上限制约14个托克/s――2026年边缘推广是四个不同的平台――四种解决方案――

> **【拓展：边缘 AI 芯片市场】**2026年边缘AI芯片的竞争格局:(1) 果神经引擎 (M4/A18) 38TOPS,统一内存架构,无需CPUNPU 数据拷贝;(2) 通六角 (Snapdragon X Elite / 8 Gen 4) 45TOPS,QNN SDK 提供转换链路;(3) 智能月球湖 / AMD Ryzen AI 30040-50TOPS,软件生态落后于果/Qualcomm;(4) NVIDIA Jetson Orin/Thor边缘GPU方案,支持vLLM 和TensorRT Edge-LLM──语音代理是边缘推销手机应用的本地推理完全消除网络延迟.

客户想要一个设备上的聊天机器人:语音先,默认私人,在线上工作.在MacBook Pro M3 Max上,Llama 3.1 8B Q4运行在55个通/秒的速度上.在iPhone 16 Pro上,同样的模型运行在3个通/秒的速度上.在中端的Android上,Snapdragon 8 Gen 3,7个通/秒.在浏览器中通过WebGPU在Chrome Android v121+,4-8个通/秒,取决于设备.

输出差异不是一个移植问题.这是带宽差距乘以量化格式乘以NPU是否可访问用户空间.2026年边缘推断是四个不同的解决方案的四个不同的问题.

## 概念的核心概念

### 带宽是真正的天花板

> **【中文解读】**边缘推理的真正天花板是内存带宽―― 解码阶段每生成一个代币 需要读取全部权重――7B Q4 模型 3.5GB,在 50 GB/s 带宽下读取需要 70ms理论上限约 14 tok/s――在 90 GB/s 高端移动DRAM) 下限升至约 25 tok/s――数据中心 HBM3 在不同的 3 TB/s 读取相同模型只需要 1.2ms上限 830 tok/s――同样的模型、同样的权重、内存子系统――

解码读取每个代币的全部权重.Q4中的一个7B模型为3.5GB.在50GB/s时读取3.5GB需要70ms ,理论上限为14tok/s.在90GB/s (高端移动DRAM) 时,限额移动到25tok/s.没有计算量帮助低于这个数量.

数据中心HBM3在3TB/s时清除相同的3.5GB在1.2ms 天花板是830tc/s.同样的模型,相同的重量.不同的内存子系统.

### 果神经引擎 (M4 / A18)

- 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器: 存储器:
- 通过核心ML+ 访问`.mlmodel`通过 PyTorch 进行编译的模型或通过金属性能遮光器 (MPS).
- 金属后端使用MPS,而不是直接使用ANE;本土ANE需要Core ML转换.
- 2026年iOS应用程序的最佳实用途径:核心ML与INT4权重+FP16激活.

### 高通六合 (Snapdragon X Elite / 8 Gen 4)

- 集成到CPU和GPU,但分开存储域.
- 基于QNN (Qualcomm神经网络) SDK和AI Hub, PyTorch/ONNX的转换功能可实现.
- 聊天模板,Llama 3.2,Fhi-3都作为AI中心的第一类文物.

### 智能/AMD NPU (月球湖,瑞森AI300)

- 软件落后于果/电,OpenVINO正在改善,但其实是个位.
- 最适合Windows ARM副驾驶应用程序;本地使用AMD/Intel桌面.

### 网络GPU + 网络LLM

> **【中文解读】**通过WebGPU计算影子运行模型. 在M3 Max 上 Llama 3.1 8B Q4 达到 ~41 个次数,约为原生性能的70 - 80%.2026年覆盖率:Chrome Android v121+、Safari iOS 26 GA、Firefox Android 仍在追赶,总体约70 - 75% 移动浏览器覆盖.

- 通过WebGPU计算模块,在浏览器中运行模型;没有安装.
- 3 Max 的Llama 3.1 8B Q4在M3 Max上以 ~ 41 个时/秒的速度,大约是70~80%的原生通过相同的后端.
- 17.6k GitHub 星星在 WebLLM;OpenAI兼容的JS API;Apache 2.0.
- 2026年覆盖率:Chrome Android v121+,Safari iOS 26 GA,Firefox Android仍在追赶.

### 杰特森家族

- 机 Nano Super (8GB):适合Llama 3.2 3B,Fi-3在好时速.
- AGX Orin:通过vLLM以 ~ 40 个时/秒运行gpt-oss-20b.
- /T4000 (JetPack 7.1): 2x AGX Orin性能,支持EAGLE-3和NVFP4.
- 讯RT Edge-LLM (2026) 支持EAGLE-3推测解码,NVFP4重量,零碎预填数据中心优化移植到边缘.

### 目标量化选择

| Target | Format | Notes |
|--------|--------|-------|
| Apple ANE | INT4 weights + FP16 activations | Core ML conversion path |
| Qualcomm Hexagon | QNN INT8 / INT4 | AI Hub converters |
| WebGPU / WebLLM | Q4 MLC (q4f16_1) | Use `mlc_llm convert_weight` + compiled `.wasm`; GGUF is not supported |
| Jetson Orin Nano | Q4 GGUF or TRT-LLM INT4 | Memory-bound |
| Jetson AGX / Thor | NVFP4 + FP8 KV | Edge-LLM path |

### 长文本陷在边缘

> **【中文解读】**边缘设备上的长上下文陷:Llama 3.1 的 128K 上下文是数据中心特性. 在 8GB RAM 的手机上,4GB 模型 + 2GB KV 缓存(32K 代币) + 系统开销 = OOM。边缘部署通常将上文限制在4K-8K,除非使用激进的 KV 量化(Q4 KV) 。

> **【拓展：边缘推理的隐私优势】**边缘推理在隐私敏感场景中有独特优势: 1) 医疗 患者数据不离开设备; 2) 金融 交易分析在本地完成; 3) 法律 律师-客户通信不上传云端; 4) 军事/政府 完全离线运行.

拉马 3.1 的 128K 语境是一个数据中心功能.在具有 8 GB RAM 的手机上, 4 GB 模型 + 32K 代币的 2 GB KV 缓存 + OS 开销 = OOM. 除非接受积极的 KV 量化 (Q4 KV) 否则,边缘部署保持 4K-8K 语境.

### 声音是杀手的应用程序

> **【拓展：边缘推理的应用场景】**边缘推理的杀手级应用是语音代理语音代理对延迟极度敏感的首代币 <500ms) ⋅本地推理完全消除网络延迟.结合语音转文字. 语变体在边缘运行),边缘推理成为生产质量的语音环路. 其他场景包括:隐私优先医疗/金融分析.

语音代理是延迟敏感的 (第一代标 <500 ms).本地推理完全消除了网络延迟.与语音到文本 (Whisper Turbo变体在边缘运行) 结合,边缘推理成为生产质量的语音循环.

### 你应该记住的数字

- 果M4 / A18 ANE: 38 个顶部.
- 通六合式SDX精英:45TOPS.
- 网络LLM M3 Max:在Llama 3.1 8B Q4上使用的速度为41个时/秒.
- 通过vLLM,在gpt-oss-20b上使用40个通话/秒.
- 数据中心边缘带宽差距:30-50倍.
- 网络GPU移动覆盖率: ~ 70-75% (Firefox Android 滞后).

## 用它实现框架
```figure
edge-bandwidth-pipe
```

## 用它

`code/main.py`计算理论解码吞吐量上限从带宽限制的数学跨边缘目标. 与观察到的基准和突出点相比,带宽而不是计算是瓶.

> `code/main.py`从宽限数学计算各边缘目标的理论解码吞吐量上限――与观察到的基准比较,强调瓶在宽度而不是计算――

## 运送它.

这一课产生了`outputs/skill-edge-target-picker.md`根据平台 (iOS/Android/浏览器/Jetson),模型和延迟/内存预算,选择量化格式和转换管道.

> 本课产出发 `outputs/skill-edge-target-picker.md`◎给定平台 (iOS/Android/浏览器/Jetson) ◎模型和延迟/内存预算,选择量化格式和转换管线.

## 练习题

1. 跑步`code/main.py`对于4Q7B模型,在Snapdragon 8 Gen 3 (~77GB/s带宽) 上,计算解码天花板.
   中文翻译:运行 `code/main.py`△计算Snapdragon 8 Gen 3 ((约77GB/s带宽) 上Q4 7B 模型的解码上限──与观察到的 6-8个/s相比运行时是否高效?
2. 在安卓上,WebGPU需要Chrome v121+.通过相同的OpenAI兼容API设计旧浏览器的服务器侧.
   中文翻译:Android 上的WebGPU 需要Chrome v121+──为旧浏览器设计回归方案通过相同的OpenAI兼容API实现服务端推理──
3. 您的iOS应用程序需要4K文本流媒体. 哪种模式/格式组合允许您在iPhone 16上保持4GB的活跃内存以下?
   中文翻译:你的iOS应用需要4K 上下文流式输出.
4. 如果你的产品是针对两者,你如何统一推断堆?
   中文翻译:杰森 AGX Orin 以40个/s 运行gpt-oss-20b。杰森纳诺只能运行3B模型。如果你的产品同时针对两者,如何统一推理?
5. 讨论"WebLLM是否2026年准备生产". 提及覆盖率,性能和Firefox Android差距.
   中文翻译:论证WebLLM 在2026年是否生产就绪──引用覆盖率、性能和Firefox Android 缺口──

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [On-Device LLMs State of the Union 2026](https://v-chandra.github.io/on-device-llms/)景观和基准
- [NVIDIA Jetson Edge AI](https://developer.nvidia.com/blog/getting-started-with-edge-ai-on-nvidia-jetson-llms-vlms-and-foundation-models-for-robotics/)        
- [NVIDIA TensorRT Edge-LLM](https://developer.nvidia.com/blog/accelerating-llm-and-vlm-inference-for-automotive-and-robotics-with-nvidia-tensorrt-edge-llm/)2026年边缘端口公告.
- [WebLLM (arXiv:2412.15803)](https://arxiv.org/html/2412.15803v2)设计和基准.
- [Apple Core ML](https://developer.apple.com/documentation/coreml)           
- [Qualcomm AI Hub](https://aihub.qualcomm.com/)前转换的六角形模型.
