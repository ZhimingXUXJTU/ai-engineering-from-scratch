# 推理指标 推测指标 推测指标 推测指标

> 根据4个指标,确定推断部署是否有效. 预填加排列加网络. 对于每个代币,TPOT (相当于ITL) 是内存绑定解码成本. 终端到终端延迟是TTFT加上TPOT乘以输出长度. 通过率是每秒的代币, 但对于产品来说,重要的是,  满足每个SLO同时的请求的比例. 低功率的高吞吐量意味着你处理的代币永远不会及时到达用户. 2026年Llama-3.1-8B-Instruct on TRT-LLM的参考号码:平均TTFT162ms,平均TPOT7.33ms,平均E2E1.093ms. 总是报道P50,P90,P99 永远不只是恶意. 并且注意测量陷:GenAI-Perf排除了TTFT从ITL计算中,LLMPerf包括它;两个工具对TPOT不同意.

> **【中文解读】**本节介绍了推理指标和优质衡量LLM推理服务质量的关键指标体系.
**Type:** Learn
**Languages:** Python (stdlib, toy percentile calculator and goodput reporter)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy percentile calculator and goodput reporter) | **语言:** Python（标准库，百分位计算器和 Goodput 报告器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 04（vLLM 服务内部）

>  **【前置】**学本节前请先掌握:阶段17·04(vLLM) 统计基础(百分位) ・・・推理指标四件套:TTFT(首代币 时间) + TPOT(每代币 时间) + 吞吐量 + Goodput。
>  **【类比】**推理指标 = "餐厅 KPI"──TTFT = 客户坐到第一道菜上桌(预填+排列+网络);TPOT = 后续每道菜间隔(解码成本);吞吐量 = 餐厅每小时出餐总数;Goodput = 满足所有SLO的请求比例(关键!)──陷:高吞吐低 Goodput = 做了很多菜,但客户没有按值吃到.──必须报报P50/P90/P99 不能只报报均――GenAI-Perf 和 LLMPerf对TPOT口径不同相同运行结果会冲突.──
**Time:** ~60 minutes | **时间:** ~60 分钟

## 学习目标

- 精确定义TTFT,TPOT,ITL,E2E,吞吐量和put,并命名每个测量的组件.
  中文翻译:精确定义 TTFT、TPOT、ITL、E2E、吞吐量和Goodput,并说出每个指标测量组件──
- 解释为什么平均是 LLM 服务的错误统计数据,以及如何读取P50/P90/P99.
  中文翻译:解释为什么平均值是LLM服务的错误统计量,以及如何阅读P50/P90/P99──
- 构建一个SLO多限制 (例如TTFT<500 ms和TPOT<15 ms和E2E<2 s) 并根据它计算出良好的输出.
  中文翻译:构造SLO 多约束(如TTFT<500ms 且TPOT<15ms 且E2E<2s)并根据此计算Goodput。
- 举个两个同期不同意TPOT的基准工具,并解释为什么.
  中文翻译:说出两个在同一运行中对TPOT产生不同的结果基准测试工具并解释原因.

## 问题 问题引入

> **【中文解读】**推理服务有多个延迟轴,每个轴以不同的方式失败了――预先是计算有限的,随着提示长度增长;解码是内存有限的,随着批量大小增长;排列延迟是运维问题;网络是物理距离问题――需要不同的指标来衡量每个维度,需要百分数,还需要一个综合指标来说"用户是否获得了预期的体验"这就是Goodput――

> **【拓展：LLM 推理指标体系】**2026年LLM推理的完整指标体系包括: 1) TTFT (首代币) 延迟 (首代币) 用户感知到的首次响应时间; 2) TPOT/ITL (每代币) 延迟/间代币) 流式输出平滑度; 3) E2E (端到端延迟) 从请求到完成的总时间; 4) 吞吐量 (吞吐量) 集群效率指标; 5) 优势 (有效吞吐) 同时满足所有SLA的请求比例.

如果40%的请求超过2秒,用户会放弃该会议. 通过量本身并不能告诉你产品是否有效.

> 如果40%的请求端到端超过2秒,用户会放弃会话.

推理具有多个延迟轴,每个轴都不同. 预填是计算的,并且可以按时间进行量度. 解码是记忆的,并且与批量大小的尺度. 排队延迟是一个运营问题. 网络是物理距离问题. 需要每个数据的分别,需要百分比,需要一个单一的复合值,上面写着"用户得到了他们预期的东西吗?"

> 推理有多个延迟轴,每个轴以不同的方式失败了――预填充是计算限制的,随提示长度增长――解码是内存限制的,随批次大小增长――排列延迟是运维问题――网络是物理距离问题――你需要每个维度不同的指标,需要百分数,还需要一个综合指标说"用户是否获得了预期的体验"这是好运气――

## 概念的核心概念

### 时间到第一个代币

> **【中文解读】**排队时间是负载调度器的行为,网络请求包括TLS的线程时间──TTFT是用户在流程中返回任何内容之前感知到的延迟──

`TTFT = queue_time + network_request + prefill_time`

在Llama-3.3-70B FP8上,H100上的32k提示需要 ~800 ms的纯预填.排队时间是载载下的规划器行为.网络请求是电线时间,包括TLS.TTFT是用户在任何东西回流之前看到的延迟.

> 预充在长提示时占主导地位――Llama-3.3-70B FP8 在H100上,32K提示需要约800ms的纯预充――排队时间是负载调节器的行为――网络请求包括TLS的线缆时间――TTFT是用户在任何内容流回之前感知到的延迟――

### 互通代币间延迟

> **【中文解读】**图片:TPOT = (decode_forward_time + scheduler_overhead) /代币_产生的──在Llama 3.3 70B H100 + 分块预填充下,TPOT 平均值约为 7ms;无分块预填充时,在长期预填充 邻居序列期间 TPOT 可升至 50ms──永远监控 P99 而非均值──

许多名称用于一个数量.`TPOT`(输出代币的时间),`ITL`标间延迟`decode latency per token`所有相同. 这是连续流通的代币之后的时间.

> 一个多个名称.`TPOT`时间的每输出标志`ITL`延迟, 延迟, 延迟, 延迟`每 token 解码延迟`都是同一个. 它是第一个标志. 之后连续流式标志 之间的时间.

`TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced`

在同一块Llama-3.3-70B H100堆上,TPOT平均值为7ms.没有块式预填,在邻近序列上长时间预填时,TPOT可以达到50ms.

> 在相同的Llama-3.3-70B H100 上加分块预充,TPOT 平均值约为7ms──无分块预充时,在邻居序列的长预充期间,TPOT 可能升至50ms──关注P99,不是平均值──

### 电源延迟

`E2E = TTFT + TPOT * output_tokens + network_response`

对于长输出 (>500代币),E2E是TPOT主导的.对于长输出,E2E是TTFT主导的.报告输出长度条件E2E.

> 对于长输出 ((>500代币),E2E由TPOT 主导──对于长提示的短输出,E2E由TTFT 主导──报告按输出长度分条件的E2E──

### 吞吐量

`throughput = total_output_tokens / elapsed_time`

总计,告诉你舰队的效率,而不是个人要求的健康.

> 聚合指标――告诉你集群效率――不告诉你单个请求的健康状况――

### 你真正关心的指标

> **【中文解读】**产量是唯一真正重要的综合指标――SLO是多约束的一个要求只有同时满足TTFT <= a、TPOT <= b、E2E <= c 才算"好"――高吞吐量在 60% 产量是失败的;低吞吐量在 99% 产量是目标――2026年MLPerf 推理 v6.0 和 AI 平台提供商内部 SLA 追踪都以 Goodput 为核心指标――

`goodput = fraction of requests meeting (TTFT <= a) AND (TPOT <= b) AND (E2E <= c)`

要求只有当每个限制都被满足时才是"好".好输出是份额.高输出率为60%的好输出是失败.低输出率为99%的好输出是目标.

> 只有当所有约束都满足时,请求才是"好"的.

2026年, goodput 是在MLPerf 推理 v6.0提交和AI平台提供商内部SLA跟踪中使用的指标.

> 2026年,Goodput 是MLPerf推理 v6.0 提交和AI 平台提供商内部SLA 追踪使用的指标──

### 为什么恶意是错误的统计数据

> **【中文解读】**延迟分布是右偏的. 一个包含长预填邻居的解码批量可能发出500个TPOT~7ms的代币和20个TPOT~60ms的代币. 平均值TPOT是9ms,但P99TPOT是65ms. 用户经常遇到P99这是他们离开的原因.

率分布是右向的.一个长预填邻居的解码批量可以发送500个代币,TPOT ~7 ms和20个代币,TPOT ~60 ms.平均TPOT为9 ms.P99 TPOT为65 ms.用户经常打到P99,这就是为什么他们离开.

> 延迟分布是右偏的. 一个包含长预填充邻居的解码批次可以发出500个TPOT约7ms的代币和20个TPOT约60ms的代币.

总是报告三倍 (P50,P90,P99). 用户体验,P99是你优化的.

> 始终报告三元组(P50、P90、P99) 对于用户体验,P99是你需要优化的──

###  拉马-3.1-8B-TRT-LLM指导, 2026

- 平均TTFT: 162 ms
  中文翻译:平均值 TTFT:162ms
- 平均TPOT:7.33 ms
  中文翻译:平均值 TPOT:7.33ms
- 平均E2E: 1,093 ms
  中文翻译:平均值 E2E:1,093ms
- P99 TPOT:根据零碎预填配置,可在10-25ms之间变化.
  中文翻译:P99 TPOT:10-25ms,取决于分块预填充配置.

这些是NVIDIA发布的参考点.它们随着模型尺寸 (70B显示 3-5x),硬件 (H100 vs B200 ~ 3x) 和负载而变化.

> 这些是NVIDIA发布的参考数据.它们随模型大小的70B会显示3-5倍) 硬件 (H100vsB200约3倍) 和负载变化.

### 测量陷

> **【中文解读】**2026年最常用的两个基准测试工具在TPOT上产生不同结果:NVIDIA GenAI-Perf将TTFT从ITL 计算中排除(从代币 2 开始),LLMPerf 包含TTFT(从代币 1 开始) ⋅同一个请求(TTFT 500ms、100 输出代币、700ms解码),GenAI-Perf 报告 ITL=7.07ms,LLMPerf 报告 ITL=12.00ms──永远说明使用哪个工具,永远发布定义──

> **【拓展：LLM 基准测试工具生态】**2026年LLM推理基准测试工具包括:(1) NVIDIA GenAI-PerfTriton 客户端,全面指标覆盖,ITL 不含TTFT;(2) LLMPerf(Anyscale)  靠谱的 分词,流式感知,含TTFT的ITL;(3) LLM-Locust(TrueFoundry)  扩展,修复GIL 问题;4) 导航大规模合成基准测试;5) (((k6 v2026.1.0流式感知,Kubernetes-native──选择工具时要了解其ITL 定义差异.

2026年最常用的两个基准工具对TPOT的不同意见:

- **NVIDIA GenAI-Perf**计算的ITL从代币 2开始.
  翻译: 中文**NVIDIA GenAI-Perf**计算中排除TTFT──ITL 从第2个标志开始──
- **LLMPerf** ITL 从代币 1 开始.
  翻译: 中文**LLMPerf**包含TTFT──ITL 从第1个标志开始──

对于一个使用TTFT 500 ms和100 个输出代币的请求,`ITL = 700/99 = 7.07 ms`据"LLMPerf"报告`ITL = 1200/100 = 12.00 ms`工具选择改变了数字.

> 对于一个TTFT 500ms,1000 输出代币,700ms 总解码的请求,GenAI-Perf 报告`ITL = 700/99 = 7.07ms`报告`ITL = 1200/100 = 12.00ms`‧工具选择改变数字‧

总是说明哪个工具,总是发布定义.

> 始终说明使用哪个工具──始终发布定义──

### 构建SLO

> **【拓展：LLM SLO 设定参考】**2026年推的消费级70B对话模型 SLO:TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s(<300代币输出)、Goodput >= 99%──企业级 SLO 收紧 TTFT(200-400ms) 但放宽 E2E──测量方法:使用真流量或LLMPerf 合成流量(`--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`),目标 2x 峰值并发,运行 30-50 次代取百分位数──

2026年为70B聊天模式提供合理的面向消费者的SLO:

- 光电阻 (TTFT P99) <= 800 ms
  中文翻译:TTFT P99 <= 800ms(首代币 延迟上限) 』
- 光电 (TPOT P99) <= 25 ms.
  中文翻译:TPOT P99 <= 25ms(每代币延迟上限) 』
- 对于<300代币输出,E2E P99 <= 3 s.
  中文翻译:E2E P99 <= 3s(<300代币输出) 』
- 产量目标 >=99%.
  中文翻译:好运 目标 >= 99%──

企业SLO紧缩TTFT (200-400ms) 和放宽E2E. 目的是记录它们,测量所有三个,并作为一个复合物追踪产量.

> 企业级SLO 紧紧 TTFT(200-400ms)并放宽E2E──关键是要写下来,测量全部三个,并将好输出作为单一综合指标追踪──

### 测量方法

- 运行真实流量或实实用合成 (LLMPerf与 `--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`)
  中文翻译:运行真流量或逼真合成流量`--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`
- 目标为基准运行的2倍峰值同步率.
  中文翻译:基准测试运行目标为2倍峰值并发──
- 运行30-50次,取组合样本的百分比.
  中文翻译:运行 30-50 次代,取合并样本的百分位数──
- 发布工具名称,工具版本,模型,硬件,同时,快速发行.
  中文翻译:发布时标注工具名、版本、模型、硬件、并发数、提示分布──

## 用它实现框架
```figure
throughput-latency
```

## 用它

`code/main.py`产品的产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少? 产量是多少?

> `code/main.py`是一个模拟的Goodput 计算器――生成合成延迟分布,应用SLO,计算Goodput──还显示相同的痕迹 上 GenAI-Perf vs LLMPerf 的TPOT 差异──

## 运送它.

> **【拓展：SLO 设定与 Goodput 门控】**2026年推的70B对话模型 SLO:TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s(<300代币 输出)、Goodput 目标 >= 99%。企业级 SLO 收紧 TTFT(200-400ms) 但放宽 E2E──关键实践:(1) 在 CI/CD 中门部署决策于Goodput值而不是吞吐量;(2) 用2x峰并发行基准测试;(((运行30-50次取百分位数;(4) 发布时标工具名,版本,模型,硬件、发行数、代提示分布.

这一课产生了`outputs/skill-slo-goodput-gate.md`鉴于工作负载和SLO,它产生了一个CI/CD准备的基准配方,该配方将门部署在产量相反的产量上.

> 本课产出发 `outputs/skill-slo-goodput-gate.md`△给定工作负载和SLO,它产生了CI/CD就绪基准测试方案,以Goodput而不是吞吐量作为部署门控.

## 练习题

1. 跑步`code/main.py`如何改变值,当你将P99TPOT从30ms到15ms紧缩时?
   中文翻译:运行 `code/main.py`◎生成带有1% 尾部尖刺的分布──当P99 TPOT从30ms 收紧到15ms 时,
2. 一家卖家引用了"Llama 3.3 70B H100"的15,000个/秒.
   中文翻译:供应商报价"拉马3.3 70B H100 上 15,000 托克/s"――在信任之前说出三个要问的问题――
3. 为什么碎片预填保护P99TPOT,而不是TPOT?
   中文翻译:为什么分块预填充保护 P99 TPOT但不保护平均值 TPOT?
4. 构建一个消费者SLO为语音助理 (第一代标语是听到的,而不是读到的).
   中文翻译:为语音助手构建消费级SLO(首代标志是听到而非读到) ――哪个标志对用户最可见?
5. 阅读LLMPerf README和GenAI-Perf文件. 确定其他三项指标,其中工具不同意.
   中文翻译:阅读LLMPerf README 和 GenAI-Perf 文档――找出工具在另外三个标志上的分歧――

## 关键词 快速查找表

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| TTFT | "time to first token" / "首 token 时间" | Queue + network + prefill; dominated by prefill at long prompts / 队列+网络+预填充；长提示时由预填充主导 |
| TPOT | "time per output token" / "每输出 token 时间" | Memory-bound decode cost per token after first / 首个 token 后每 token 的内存受限解码成本 |
| ITL | "inter-token latency" / "inter-token 延迟" | Same as TPOT in most tools (not all — see GenAI-Perf) / 大多数工具中同 TPOT（非所有——见 GenAI-Perf） |
| E2E | "end to end" / "端到端" | TTFT + TPOT * output_len; response-side network on top / TTFT + TPOT * 输出长度；加上响应端网络 |
| Throughput | "tok/s" / "token 每秒" | Fleet efficiency; useless without latency percentiles / 集群效率；无延迟百分位数则无意义 |
| Goodput | "SLO-met rate" / "SLO 达标率" | Fraction of requests meeting every SLO constraint simultaneously / 同时满足所有 SLO 约束的请求比例 |
| P99 | "tail" / "尾部" | 1-in-100 worst-case latency; the user experience metric / 百分之一最差延迟；用户体验指标 |
| SLO multi-constraint | "the joint" / "联合约束" | AND of all three latency bounds; a request fails if any one is violated / 三个延迟界限的 AND；任一违反即失败 |
| GenAI-Perf vs LLMPerf | "the tool trap" / "工具陷阱" | Tools disagree on whether ITL includes TTFT / 工具在 ITL 是否包含 TTFT 上不一致 |

## 继续阅读 继续阅读

- [NVIDIA NIM — LLM Benchmarking Metrics](https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html)TTFT,ITL,TPOT的法典定义.
- [Anyscale — LLM Serving Benchmarking Metrics](https://docs.anyscale.com/llm/serving/benchmarking/metrics)替代定义和测量配方.
- [BentoML — LLM Inference Metrics](https://bentoml.com/llm/inference-optimization/llm-inference-metrics)实用测量实用部署.
- [LLMPerf](https://github.com/ray-project/llmperf)基于光线的开源基准.
- [GenAI-Perf](https://github.com/triton-inference-server/perf_analyzer/blob/main/genai-perf/README.md)NVIDIA的基准工具.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/)行业接受的基于产品质量的基准指标.
