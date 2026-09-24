# 服务内部:页面关注,连续批量,零碎预填.
# 服务引擎内部 页面注意,连续批量,零碎预填

> 现代服务引擎的吞吐量依赖于三个合并默认, 网页关注总是开放. 连续批量将新的请求注入解码代之间. 碎片的预填片长时间提示,所以解码代码永远不会饿死. 启动三种,一个H100 SXM5上的Llama 3.3 70B FP8在128次同时下推出2,200-2,400个/秒,大约比VLLM的默认高25%, 是所有三种技术的参考引擎在一个你可以图表的水平上,并结束在玩具连续批量`code/main.py`时间表像VLLM一样预填和解码.

> **【中文解读】**2026年主导地位基于三个复杂优化:PagedAttention(分页注意力)始终开启;连续批量在解码代间注入新请求;分块预填片长提示以防止解码 标志饥饿──三者全开时,Llama 3.3 70B FP8 在单卡H100上以 128并发达2,200-2,400 tok/s比朴素 PyTorch 循环快 3-4倍──

> **【拓展：vLLM → LLM 推理服务标准】**存器是2026年最流行的开源存器. 存器是2026年最流行的开源存器. 存器是2026年最流行的开源存器. 存器是2026年最流行的开源存器.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy continuous batching scheduler) | **语言:** Python（标准库，连续批处理调度器模拟）
**Prerequisites:** Phase 17 · 01 (Model Serving), Phase 11 (LLM Engineering) | **前置知识:** Phase 17 · 01（模型服务）, Phase 11（LLM 工程）
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前请先掌握:阶段11·12(推理优化基础) 、KV缓存概念、连续批处理──vLLM 是2026 开源推理引擎的事实标准──
>  **【类比】**像操作系统虚拟内存分页,碎片率 < 4%);持续批量 = 动态拼单(新请求随时插入运行批量);碎片预填 = 切长快速(长输入切片避免阻塞解码) ――Llama 3.3 70B FP8 在 H100 上 128 并发达 2200-2400 tok/s,比朴素实现快 3-4 倍

## 学习目标

- 解释PagedAttention作为KV缓存分配器:区块,区块表,以及为什么在生产负载时碎片化保持在4%以下.
  中文翻译:将 PagedAttention 解释为 KV 缓存分配器:块、块表,以及为什么在生产负载下碎片率保持在4%以下──
- 在反复级别上进行连续批量图:完成的序列如何离开批量,而新的序列如何在没有排水的情况下加入.
  中文翻译:在代级别绘制连续批处理:已完成的序列如何离开批次,新序列如何加入而无需清空――
- 描述一个句子中的零碎预填,并命名它保护的延迟指标 (提示:这是TTFT尾声,而不是平均吞吐量).
  中文翻译:用一句话描述分块预填充,并说出它保护哪个延迟指标
- 给2026年VLLM v0.18.0的名称来说,它可以同时实现每个优化.
  中文翻译:说出2026年 vLLM v0.18.0 中同时启动所有优化团队会遇到的问题.

## 问题 问题引入

> **【中文解读】**朴素 PyTorch 服务循环一次处理一个请求――静态批量将所有请求填充到最长序列,浪费 GPU资源并让快请求等待慢请求――vLLM 通过三个核心优化解决这个问题:PagedAttention(KV缓存碎片率从60-80% 降至4% 以下) 连续批量处理(在解码代间动态加入新请求) 分块预填充(将长提示切片以防止解码饥饿) ⋅

一个天真的 PyTorch 服务循环一次执行一个请求:代码化,预填,解码到 EOS,返回. 在一个用户上,这就有效了. 百人,是一队耐心的人. 显而易见的解决方案是: 静态批量 将每个请求都将放在窗口中最长的提示,每个解码都将被放在最长的预期输出中,并且将整个批量停滞在最慢的序列中. 你付钱买不用的填充, 快速的请求等待缓慢的请求.

> 朴素 PyTorch 服务循环一次处理一个请求:分词、预填充、解码直到EOS、返回──一个用户时,这行通──一百个用户时,这就是一排耐心等待的人──显然修复静态批处理将每个请求填充到窗口中最长的提示,将每个解码填充到最长的预期输出,整个批次等待最慢的序列──你为未使用的填充单,快速请求等待缓慢请求──

机可以同时解决三个问题. 页面注意力阻止KV缓存碎片化消耗60至80%的GPU内存, 连续批量允许请求在每个解码反复之间加入和离开批量,所以批量总是充满了真正的工作. 碎片预填将32k代码提示分解为512代码切片,与解码交互,因此长时间的提示不会结 GPU上的每个解码代码.

> 继续批量处理让请求在每个解码代代之间加入和离开批次,所以批次总是充满真实工作──分块预填将将32K代币的提示切成512个代币的提示片段,与解码交换进行,所以长提示不会结 GPU 上每个解码代币──

需要了解每个机器的操作,因为失败模式都在调度器上,而不是模型上.

> 2026年生产默认设置是三个.你需要了解每个做什么,因为故障模式都在调节器上,而不是模型上.

## 概念的核心概念

### 页面关注作为虚拟内存系统

> **【中文解读】**页面注意力 借鉴操作系统虚拟内存分页思想管理 KV Cache──传统连续分配为每个序列预分配最大长度(如8192个代币),但平均请求只使用1500个代币,浪费82%的HBM── 页面注意力将 KV Cache 分为固定大小的块(默认16个代币),每个序列有一个块表映射逻辑位置到物理块ID,按需分配,碎片率低于4%──这是vLLM唯一的分配器,通过`--gpu-memory-utilization`控制KV缓存可用HBM比如:

> **【拓展：KV Cache 内存管理演进】**卡存储管理经历了三代演变: 1) 连续预分配简单但浪费60-80%内存; 2) 页面关注(vLLM 2023) 分页管理,碎片率 <4%,成为行业标准; 3) 拉迪克斯关注(SGLang 2024) 在前共享场景下进一步优化,通过雷迪克斯树索引实现跨请求的卡存储重复使用.

一个KV缓存是`num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element`如果您预先预订每次请求的8192个插槽,但平均请求只使用1500个插座,您将浪费约82%的预订的HBM.经典批量支付了这个浪费.

> 每个序列的KV存储量大小为`num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element`拉马 3.3 70B 在 8192 代币中,BF16 下每序列约 1.25 GB. 如果你为每一个请求预留 8192 个槽位,但平均请求只使用 1500 个代币,你浪费了约 82% 预留的 HBM.

页面注意从OS虚拟内存借用这个想法.KV缓存不连续于每个序列.它分为固体尺寸的块 (默认16个代币).每个序列都有一个区块表,将其逻辑代币位置映射到物理区块ID.当一个序列越来越多,其分配的区块被添加了另一个区块.当它完成时,其区块返回池中.

> 借鉴操作系统虚拟内存的思想──KV 缓存不是每个序列连续的──它以固定的大小块的块──默认16个代币) 分布──每个序列有一个块表,将逻辑代币 位置映射到物理块 ID──当序列增长超过已分布的块时,添加一个新的块──完成后,块返回池中──

,它是唯一的分配器vLLM船只. 按是`--gpu-memory-utilization`(默认0.9),该文件告诉vLLM在加载重量和激活后,HBM应为KV块保留多少.

> 碎片率从60到80% (经典) 下降到4% 以下(PagedAttention) ――你不需要标志启动`--gpu-memory-utilization`预备多少HBM.

### 在反复级别的连续批量

> **【中文解读】**连续批量处理在每个解码步骤之间做出接受/释放决策.每个代:(1) 移除已完成的序列;(2) 检查等待队列,如果有空 KV 块则接受新序列;(3) 对运行列中的所有序列进行一次前向传播.批次大小不确定,不同输出位置的序列共享一次融合前向计算.

旧的"动态批量"等待一个窗口 (例如10 ms) 填充批量,然后运行预填+解码+解码+解码+解码直到每个序列完成.快速序列早就离开了,停留在空中,而GPU完成了缓慢的序列.

> 旧的"动态批处理"等待一个窗口 (如10ms) 来填充批次,然后运行预填+解码+解码+解码直到每个序列完成.

连续批量在每个解码步骤之间运行.`RUNNING`在每次代时:

> 连续批处理在每个解码步骤之间操作.将运行中的序列集合称为`RUNNING`列表:每次代

1. 任何序列`RUNNING`现在,我们可以将 EOS 输入到 EOS 输入中,
   翻译: 中文`RUNNING`中刚达到EOS或max_tokens的任何序列都被移除.
2. 编程器看待排队.如果有免费的KV块,它会允许新的序列 (预填或恢复).
   中文翻译:调度器查看等队列. 如果有空 KV 块,它接纳新序列.
3. 进口通行是现在的任何东西.`RUNNING`发出每次一个新的代币.
   中文翻译:前向传播对`RUNNING`现在,每个序列发出一个新代币.

批量尺寸从来没有被到固定数量.在不同位置的序列在输出中共享一个前进的融合.`V1 scheduler`关键不变:调节器每次解码反复运行一次,而不是每次请求.

> 批次大小从不填充到固定数字――输出不同位置的序列共享一次融合前向传播――2026年VLLM中称为`V1 scheduler`△关键不变量:调度器每解码代运行一次,而不是每请求运行一次.

### 碎片预填保护TTFT尾

> **【中文解读】**分块预填充解决了长提示"结结"其他序列解码问题. 一个32K代币提示在70B模型上需要约800ms的纯预填值计算,而所有其他序列的解码代币都在等待. 分块预填充将预填 切成固定大小的块 (默认512代币),每个块之间调度器可以推进其他序列解码.价格是预填延迟增加几毫秒,但P99 ITL从约50ms 降至约15ms.这是用户体验的关键改善.

> **【拓展：vLLM 生产部署最佳实践】**公司的产业部署的关键配置包括:`--gpu-memory-utilization 0.9`预留90%的HBM 给KV缓存;(2) `--max-model-len`根据实际需求设置而非默认最大值;(3) 分块预填充默认开启但不兼容某些推测解码模式;(4)`--enable-prefix-caching`在RAG/代理场景下可大幅减少重复预填;5) 承诺指标端点用于监控队列深度和KV利用率──

在Llama 3.3 70B上使用32k代币提示需要在一个H100上使用800ms的纯预填.在预填运行期间,在批量等待中,对每个其他序列进行代码解码.在服务循环中,一个长时间的提示的第一代币延迟 (TTFT) 成为数十个其他用户的代币间延迟 (ITL) 漏洞.

> 预充是计算密集型的――Llama 3.3 70B 上一个32K代币提示在单卡H100上需要约800ms的纯预充――预充运行时,批次中所有其他序列的解码代币都在等待――在服务循环中,一个长提示的首个代币延迟(TTFT) 变成了几十个其他用户的代币间延迟(ITL) 毛刺――

按零件预填分成固定尺寸的零件 (默认512个代币) 并将每个零件作为单位安排.在零件之间,计程师可以提升一个代码序列.您以较低的解码时间位换取一个小的绝对预填延迟 (每零件数 ms).在发布的基准中,混合负载下 P99 ITL 从 ~ 50 ms 到 ~ 15 ms 降低.

> 分块预填充将预填充分成固定大小的块 (默认512代币),每个块作为调度单元. 在块之间,调度器可以推进解码序列一个代币. 你用少量绝对预填充延误损失. 每块几毫秒) 换取更低的解码时间.

### 三个默认互动

随着时间表的推进,可实现一个新的测量,即将进行测量. 随着时间表的推进,可实现一个新的测量.`RUNNING`                                                                                                                                                                                                                                                              

> 连续批量处理需要这种细分资源,因此接收新序列不需要整局重排. 分块预填充是调度器在同一块.`RUNNING`列表上做出的决策是调整策略,而不是独立系统.

你不需要知道每一个旗,你需要知道调度器优化什么:KV区块预算下,

> 你不需要知道每个标志. 你需要知道调度器优化什么.

### 2026年版本0.18.0得到了你

> **【中文解读】**vLLM v0.18.0 中不能同时启动`--enable-chunked-prefill`和草案模型 推测解码`--speculative-model`) ・ 唯一的例外是V1调度器中的N-gram GPU 推测解码――不读发布说明说明 启动时所有优化标志的团队会遇到运行错误,而不是软性退化―― 如果推测解码的收益值启动分块预填,2026年正确的答案通常是EAGLE-3而不是草案模型――

在vLLM v0.18.0中,不能组合`--enable-chunked-prefill`采用预测式模拟解码 (`--speculative-model`) 文件的例外是V1调度器中的N-gram GPU推测解码. 没有阅读发布说明的团队在启动时会出现运行时间错误,而不是软回归. 如果你的投机收益值得实现零碎预填, 再次选择2026年正确的答案通常是EAGLE-3没有零碎预填,而不是一个不编译的草案模型加上零碎预填.

> 在vLLM v0.18.0中,你不能同时启动`--enable-chunked-prefill`和草案模型 推测解码`--speculative-model`)――文档记录的例外是V1调度器中的N-gram GPU 推测解码――不读发布说明关于启动所有标志的团队在启动时遇到运行时的错误而不是软性退化――如果推测解码的收益值需要启动分块预填,重新审核选择2026年正确的答案通常是EAGLE-3而不是草案模型――

### 你应该记住的数字

- 拉马3.3 70B FP8,H100 SXM5,128同时,所有三种都在: 2,200-2,400 /秒.
  中文翻译:Llama 3.3 70B FP8,H100 SXM5,128 并发,三个优化全开:2,200-2,400 托克/秒──
- 模板相同,默认vLLM (没有碎片预填): ~ 1,800 tok/s.
  中文翻译:同模型,默认 vLLM(无分块预填充):约1,800个单元/秒.
- 模特相同,纯粹的 PyTorch 前进循环: ~600通/秒.
  中文翻译:同模型,朴素 PyTorch 前向循环:约600个/秒.
- 在生产负载下,KV碎片化废物在 PagedAttention下: <4%.
  中文翻译:PagedAttention 在生产负载下 KV碎片浪费:<4%──
- 混合载荷下 P99 ITL: ~15 ms,含有碎片预填,没有含有 ~50 ms.
  中文翻译:混合负载下 P99 ITL:有分块预填充约15ms,无约50ms──

### 时间表表的样子

```
while True:
    finished = [s for s in RUNNING if s.is_done()]
    for s in finished: release_blocks(s); RUNNING.remove(s)

    while WAITING and have_free_blocks_for(WAITING[0]):
        s = WAITING.pop(0)
        allocate_initial_blocks(s)
        RUNNING.append(s)

    # schedule prefill chunks + decode in one batch
    batch = []
    for s in RUNNING:
        if s.in_prefill:
            batch.append(next_prefill_chunk(s))   # e.g. 512 tokens
        else:
            batch.append(decode_one_token(s))     # 1 token

    run_forward(batch)                            # one fused GPU call
```

`code/main.py`运行它显示了如何在长时间的预填中保持解码序列的活力.

> `code/main.py`正是这个循环的纯标准库 Python 实现,使用虚假代币计数和虚假前向延迟.运行它可以看到分块预填充如何保持解码序列在长期预填充期间活跃.

## 用它实现框架
```figure
tensor-parallel
```

## 用它

`code/main.py`模拟一个可转换功能的vLLM类型的调度器.运行它,以查看:

> `code/main.py`模拟一个带有可切换功能的vLLM风格调度器.

- `NAIVE`模式:一次一次要求,无批量.
  翻译: 中文`NAIVE`模式:一次一个请求,无批处理.
- `STATIC`模式: 片和等待,经典的批量.
  翻译: 中文`STATIC`模式:填充并等待,经典批量处理.
- `CONTINUOUS`模式:回复级的接入和释放.
  翻译: 中文`CONTINUOUS`模式: 代级的接收和释放
- `CONTINUOUS + CHUNKED`模式:用解码插入的预填片.
  翻译: 中文`CONTINUOUS + CHUNKED`模式:预填充切片与解码交错.

输出显示了总吞吐量 (每虚拟秒的代币),TTFT平均值和P99ITL.`CONTINUOUS + CHUNKED`排列应在混合交通中占主导地位.

> 输出显示总吞吐量(每虚拟秒代币 数) 、TTFT 平均值和 P99 ITL。`CONTINUOUS + CHUNKED`行在混合流量下应占主导地位.

## 运送它.

> **【拓展：LLM 推理引擎对比】**2026年主流开源 LLM 推理引擎包括:vLLM(通用生产默认,PagedAttention+连续批处理) √SGLang(前共享优化,RadixAttention) √TensorRT-LLM(NVIDIA专属,Blackwell 上吞吐最高) √llama.cpp(CPU/边缘,GGUF 格式) √选择取决于硬件(CPU/GPU/Hopper/Blackwell) √工作负载(通用聊天/代理/RAG) 和合规要求自 √托管/云托管) √vLLM 根据2026年人工智能基础设施调查的生产部署量约60%) √

这一课产生了`outputs/skill-vllm-scheduler-reader.md`鉴于服务配置 (批量大小,KV内存使用,零碎预填尺寸,投机配置),它产生了一个调度器诊断,该诊断列出三个默认缺陷中的哪个是瓶和什么调节.

> 本课产出发 `outputs/skill-vllm-scheduler-reader.md`△给定服务配置 () 量量大小,KV内存利用率,分块预填大小,推测配置),它产生调度器诊断,指出三个默认中哪个是瓶以及如何调优.

## 练习题

1. 跑步`code/main.py`比较`STATIC`为了`CONTINUOUS`预填效率,解码效率或尾延迟的产量差距来自哪里?
   中文翻译:运行 `code/main.py`△在混合长短请求工作负载上比较`STATIC`和 `CONTINUOUS`吞吐量差距 预充效率,解码效率还是尾部延迟从何而来?
2. 修改玩具调节器`--max-num-batched-tokens`运行Llama 3.3 70B FP8的H100的正确值是什么? (提示:它是KV块大小和数量的函数,而不是原始HBM).
   中文翻译:修改模拟调度器添加 `--max-num-batched-tokens`△H100 运行 Llama 3.3 70B FP8 的正确值是多少?提示:是 KV 块大小和空块数的函数,而不是原始的 HBM。)
3. 列出哪些旗组合是相互排斥的?
   中文翻译:重新阅读 vLLM v0.18.0 发布说明──哪些标志组合互斥?列出它们──
4. 计算KV缓存碎片化废物为1000个请求的追踪,平均输出代币为1,500个,STD600代币,根据 (a) 每次请求分配的连续性最高为8192, (b) PagedAttention,含16代币块.
   中文翻译:计算 1,000 个请求的 KV 缓存碎片浪费(平均值 1,500 输出代币,标准差 600),在 (a) 最大 8192 的连续每请求分配和 (b) 16 代币块的 PagedAttention 下。
5. 解释一段落,为什么碎片预填有助于P99ITL,但不单独地提供产量.
   中文翻译:用一段话解释为什么分块预填充帮助P99 ITL但不单独提升吞吐量――实际中吞吐量提升从何而来?

## 关键词 快速查找表

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| PagedAttention | "the KV trick" / "KV 技巧" | Fixed-size block allocator for KV cache; fragmentation <4% / KV 缓存的固定大小块分配器；碎片率 <4% |
| Block table | "the page table" / "页表" | Per-sequence map from logical token position to physical KV block / 每序列的逻辑 token 位置到物理 KV 块的映射 |
| Continuous batching | "dynamic batching, but right" / "正确的动态批处理" | Admit/release decisions made every decode iteration / 每个解码迭代做出接纳/释放决策 |
| Chunked prefill | "prefill splitting" / "预填充切片" | Break long prefill into 512-token slices interleaved with decode / 将长预填充切为 512 token 片段与解码交错 |
| TTFT | "first token time" / "首 token 时间" | Prefill + queue + network; dominated by prefill at long prompts / 预填充+队列+网络；长提示时由预填充主导 |
| ITL | "inter-token latency" / "token 间延迟" | Time between consecutive decode tokens; dominated by batch size / 连续解码 token 之间的时间；由批次大小主导 |
| Goodput | "throughput that meets SLO" / "满足 SLO 的吞吐量" | Tokens/sec where every request still hit TTFT and ITL targets / 每秒 token 数，每个请求仍满足 TTFT 和 ITL 目标 |
| V1 scheduler | "the new scheduler" / "新调度器" | vLLM's 2026 scheduler; N-gram spec decode is the chunked-prefill-compatible path / vLLM 2026 调度器；N-gram 推测解码与分块预填充兼容 |
| `--gpu-memory-utilization` | "the memory knob" / "内存旋钮" | Fraction of HBM reserved for KV blocks after weights and activations / 加载权重和激活后为 KV 块预留的 HBM 比例 |

## 继续阅读 继续阅读

- [vLLM documentation — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode/)关于零碎预填和投机解码兼容性的官方来源.
- [vLLM Release Notes (NVIDIA)](https://docs.nvidia.com/deeplearning/frameworks/vllm-release-notes/index.html) 2026 发布序列和版本特定行为.
- [vLLM Blog — PagedAttention](https://blog.vllm.ai/2023/06/20/vllm.html)原始的写作,仍然定义了如何思考分配器.
- [PagedAttention paper (arXiv:2309.06180)](https://arxiv.org/abs/2309.06180) 分裂分析和规划设计.
- [Aleksa Gordic — Inside vLLM](https://www.aleksagordic.com/blog/vllm)详细的V1调度器通过火焰图.
