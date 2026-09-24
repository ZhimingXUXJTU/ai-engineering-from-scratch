# 服务选择  llama.cpp, Ollama, TGI, vLLM, SGLang
# 选择自主托管服务 机器与硬件和规模相匹配

> 引擎选择是硬件,规模和生态系统的函数,而不是排名表的读数. 2026年,四个引擎主导自主主设置推理: llama.cpp, Ollama, vLLM, SGLang,TGI在维护模式下落后.**llama.cpp**支持最广泛的模型,对量化和线程进行全面控制.**Ollama**是 dev 笔记本电脑单命令安装,比 llama.cpp (Go + CGo + HTTP 序列化) ~15-30%慢,在像 prod 负载下输出差距3x. **TGI entered maintenance mode December 11, 2025**只修复错误,原始吞吐量比vLLM慢10%但历史上具有最高可观测性和HF生态系统集成性.这种维护状态使其成为一个风险的长期投注.**vLLM**是一般用途的生产默认 v0.15.1 (二月2026年) 添加 PyTorch 2.10, RTX Blackwell SM120, H200优化. **SGLang**是生产的多转/前重型专家的400,000+GPU (xAI,LinkedIn,Cursor,Oracle,GCP,Azure,AWS). 硬件限制:CPU-first → llama.cpp. AMD/非NVIDIA → vLLM是最强有支持的路径 (TRT-LLM是NVIDIA锁定). 2026 管道模式: dev = Ollama,阶段 = llama.cpp, prod = vLLM或 SGLang. 发动机采用不同的重量格式, GGUF用于 llama.cpp家族,HF安全传感器用于GPU发动机,因此格式转换可以在阶段之间进行.

> **【中文解读】**本节介绍了自托管推理服务选择类型vLLM、TGI、llama.cpp等框架的对比和选择.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, engine-decision tree walker) | **语言:** Python
**Prerequisites:** All Phase 17 lessons covering engines (04, 06, 07, 09, 18) | **前置知识:** All Phase 17 lessons covering engines (04, 06, 07, 09, 18)

>  **【前置】**本节是第17阶段的机器知识.
>  **【类比】**自托管引擎 = "AI 服务器品牌"──llama.cpp = CPU 王者(最广模型支持、量化全控制);Ollama = 笔记本一键安装(比 llama.cpp 慢15-30%);TGI 已进入维护模式(2025.12.11) 只修改bug,新项目别选;vLLM = 通用生产默认(v0.15.1+ PyTorch 2.10+Blackwell);SGLang = 代理多轮+前密集专家(40万+ GPU 在 xAI/LinkedIn/Cursor) ⋅
>  **【困惑】**问: 我的场景该选哪个?仅供CPU→llama.cpp;AMD/非NVIDIA→vLLM(TRT-LLM 锁NVIDIA);代理多轮→SGLang;通用→vLLM。2026 流水线:dev=Ollama、舞台=llama.cpp、prod=vLLM/SGLang,全用GGUF/HF权重一致。
**Time:** ~45 minutes | **时间:** ~45 minutes

## 学习目标

- 选择一个引擎 (CPU/AMD/NVIDIA Hopper/Blackwell),规模 (1用户/100/10,000),和工作负载 (通用聊天/代理/长文).
  中文翻译:给定硬件 ((CPU/AMD/NVIDIA Hopper/Blackwell) 尺寸和工作负载选择引擎──
- 举个2026年TGI维护模式状态 (2025年12月11日) 的名称,以及为什么它偏向新项目向vLLM或SGLang.
  中文翻译:说出2026年TGI 维护模式状态(2025年12月11日) 以及它为什么影响使用 HuggingFace 默认设置的团队──
- 描述整个开发/阶段/生产管道,使用相同的GGUF或HF重量.
  中文翻译:描述在整个生命周期中使用相同的GGUF或HF权重的开发/预发布/生产流水线――
- 解释为什么"只有CPU"强迫 llama.cpp,而"AMD"排除TRT-LLM.
  中文翻译:解释为什么"仅CPU"强制使用 llama.cpp而"AMD"排除了TRT-LLM──

## 问题 问题引入

> **【中文解读】**自托管推理引擎的选择取决于三个维度:硬件(CPU / AMD / NVIDIA Hopper / Blackwell) √规模(1用户 / 100 / 10,000) √工作负载(通用聊天 / 代理 / 长上下文) √2025年 12 月 11 日 HuggingFace TGI 进入维护模式(仅修改错误),这使新项目应默认远离 TGI,转向vLLM或 SGLang.
- 描述开发/阶段化/生产管道,包括在阶段之间设置GGUF到安全感应器格式转换的地方.
- 解释为什么"CPU-first"指 llama.cpp,而"AMD"排除TRT-LLM.

> **【拓展：2026 年推理引擎选择决策】**2026年推理引擎的硬件优先决策树:(1) 只有CPU → llama.cpp(唯一有竞争力的选项);(2) AMD GPU → vLLM(ROCm 支持),TRT-LLM 不支持 AMD;(3) NVIDIA Hopper → vLLM 或 SGLang 或 TRT-LLM(三选一);(4) NVIDIA Blackwell → TRT-LLM 吞吐最高;(5) Apple Silicon → llama.cpppp(金属 GPU 后端) △规模决策:1 用户→Ollama,10-100→LLvM 单,100-10K→LLM 生产堆或 SangGL,10K+→生产堆 + 分离式 + LMC。

你的团队开始了新的自主主办的LLM项目. 一个工程师说Ollama,另一个说vLLM,第三个说"TGI不只是出局吗?"这三个适合不同环境.

2026年,选择树是重要的:硬件第一,规模第二,工作负载第三. 2025年一个特定事件  TGI进入维护模式 12月11日 改变了新项目默认.

## 概念的核心概念

### 五个发动机

| Engine | Best for | Notes |
|--------|----------|-------|
| **llama.cpp** | CPU / edge / minimal deps / widest model support | Fastest on CPU, full control |
| **Ollama** | Dev laptops, single user, one-command install | 15-30% slower than llama.cpp; 3x prod throughput gap |
| **TGI** | HF ecosystem, regulated industries | **Maintenance mode Dec 11, 2025** |
| **vLLM** | General-purpose production, 100+ users | Broad production default; v0.15.1 Feb 2026 |
| **SGLang** | Agentic multi-turn, prefix-heavy workloads | 400,000+ GPUs in production |

### 硬件首次决定

**CPU-first**拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉

**AMD GPU**是最强的支持路径 (AMD ROCm支持).SGLang也可以.TRT-LLM是NVIDIA锁定,所以它是关闭的.

**NVIDIA Hopper (H100 / H200)**,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

**NVIDIA Blackwell (B200 / GB200)** TRT-LLM是吞吐量领先者 (阶段17 · 07). vLLM和SGLang紧接着.

**Apple Silicon (M-series)**拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉拉

### 规模二次决定

**1 user / local dev**一个命令,在几秒钟内发出.

**10-100 users / small team**接器的使用率

**100-10k users / production**→ vLLM生产阶段 (阶段17 · 18) 或SGLang.

**10k+ users / enterprise**→ vLLM生产堆+分类 (阶段17 · 17) + LMCache (阶段17 · 18).

### 工作负担第三决定

**General chat / Q&A**在宽泛的默认情况下,

**Agentic multi-turn (tools, planning, memory)**→ SGLang 的RadixAttention (阶段17 · 06) 主导.

**RAG with heavy prefix reuse**子子

**Code generation**,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

**Long context (128K+)**→ vLLM + 碎片预填; SGLang + 层级KV.

### 维护TGI陷

> **【中文解读】**图像卡,安全工具),原始吞吐略低于VLLM (约10%). 对2026年的新项目,应默认远离TGI.现有TGI部署可以继续运行,但应规划迁移.

> **【拓展：工作负载驱动的引擎选择】**工作负载维度驱动引擎选择:(1) 通用聊天/问答 → vLLM(广泛默认);(2) 代理多轮对话(工具、规划、记忆)→ SGLang RadixAttention 主导;(3) RAG 重前复用 → SGLang;(4) 代码生成 → vLLM 足够,SGLang 缓存略好;(5) 长上下文(128K+)→ vLLM + 分块预填充,SGLang + 分层 KV── Ollama 适合开发但不是生产共享服务的理想选择Go HTTP 序列化增加开销并管理发送比 vLLM 简单、Openmetry 支持滞后.

抱脸TGI进入维护模式2025年12月11日 仅在未来修复了错误.历史上:顶级可观测性,最好的HF生态系统整合 (模型卡,安全工具),在原始吞吐量上略落后于vLLM.

2026年新项目:默认退出TGI.现有的TGI部署可以继续,但最终应该迁移.SGLang和vLLM是安全的默认.

### 管道模式

发动机采用不同的重量格式.  GGUF为 llama.cpp 家庭,HF安全传感器为 GPU ,因此格式转换可以在阶段之间坐落. 工程师在笔记本电脑上快速演变; 阶段镜子生产量化; 是服务目标.

### 奥拉马警示

欧拉马是 dev 很好的.它不适合共享生产:Go HTTP 序列化增加了上费用,同时管理比vLLM更简单,OpenTelemetry 支持延迟.使用Ollama 闪耀的一个用户,一个命令,然后切换到vLLM.

### 自主主主机与管理机是个独立的决定

阶段17 · 01 (管理过度计算器), · 02 (推理平台) 覆盖管理.本课程假设您已经决定自主托管.自主托管的原因:数据居住,定制细节调整,规模总成本所有权,主机模型不提供在托管.

### 你应该记住的数字

- 维护模式:2025年12月11日
- 支持PyTorch 2.10;支持Blackwell SM120
- 产量足迹:400,000+GPU.
- 拉马输出差距与拉马.cpp:15-30%慢;

## 用它实现框架
```figure
data-parallel
```

## 用它

`code/main.py`根据硬件+规模+工作负载,选择引擎并解释原因.

> `code/main.py`根据硬件+规模+工作负载,选择引擎并解释原因.

## 运送它.

> **【拓展：自托管 vs 托管的决策】**自托管与托管是独立的决策.自托管的理由: 1) 数据留留数据不能离开组织; 2) 自定义微调LoRA/QLoRA 适配器需要本地部署; 3) 大规模总拥有成本年推理支出超过5亿美元 时自托管通常更经济; 4) 领域模型不在托管平台上可用.

这一课产生了`outputs/skill-engine-picker.md`由于限制,他选择了引擎,并写出了迁徙计划.

> 本课产出发 `outputs/skill-engine-picker.md`由于限制,他选择了引擎,并写出了迁徙计划.

## 练习题

1. 跑步`code/main.py`输出与你的直觉相符吗?
   中文翻译:用你的硬件/规模/工作负载运行 `code/main.py`◎输出是否符合预期?
2. 你的红外线是12个H100和8个MI300XAMD. 什么发动机?为什么TRT-LLM没有上桌?
   中文翻译:你的基础设施是12块H100和8块MI300XAMD──用什么引擎?为什么TRT-LLM不可选?
3. 据了解, 移民案例是"我们所知道的"
   中文翻译:一个团队想在2026年使用TGI 因为"这是我们熟悉的"......论证迁移的理由.
4. 拉马开发到vLLM推广:量子化,配置和可观测性有哪些变化?
   中文翻译:Ollama 开发到vLLM 生产:量化,配置和可观测性有什么变化?
5. 采用P99预写长度8K和租户中重复使用的RAG产品.

## 关键词 快速查找表

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
| Pipeline pattern | "dev→stage→prod" | Ollama → llama.cpp → vLLM; weight formats differ per engine |

## 继续阅读 继续阅读

- [AI Made Tools — vLLM vs Ollama vs llama.cpp vs TGI 2026](https://www.aimadetools.com/blog/vllm-vs-ollama-vs-llamacpp-vs-tgi/)
- [Morph — llama.cpp vs Ollama 2026](https://www.morphllm.com/comparisons/llama-cpp-vs-ollama)
- [n1n.ai — Comprehensive LLM Inference Engine Comparison](https://explore.n1n.ai/blog/llm-inference-engine-comparison-vllm-tgi-tensorrt-sglang-2026-03-13)
- [PremAI — 10 Best vLLM Alternatives 2026](https://blog.premai.io/10-best-vllm-alternatives-for-llm-inference-in-production-2026/)
- [TGI maintenance announcement](https://github.com/huggingface/text-generation-inference)发布的说明.
- [vLLM v0.15.1 release notes](https://github.com/vllm-project/vllm/releases)
