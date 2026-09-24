# 3 投机解码 产品

> 投机解码将快速的草案模型与目标模型结合起来. 草案提出K代币;目标在单个前期中验证;接受的代币是免费的. 2026年,EAGLE-3是生产级变体,它训练了一个预稿头,在目标模型的隐藏状态而不是原始代币,在一般聊天中推进接受率alpha到0.6-0.8带. 如果阿尔法下降到0.55以下,投机解码在高同步率下是净负的,因为每一个被拒绝的草案都需要第二个目标前进. 这课教你先测量阿尔法,然后翻旗.

> **【中文解读】**本节介绍推测解码使用小模型预测大模型输出加速推理技术
**Type:** Learn
**Languages:** Python (stdlib, toy acceptance-rate simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 10 · 18 (Multi-Token Prediction)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy acceptance-rate simulator) | **语言:** Python（标准库，接受率模拟器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 18 (Multi-Token Prediction) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 10 · 18（多 Token 预测）

>  **【前置】**学本节前请先掌握:阶段17·04(vLLM) 、阶段10·18(MTP多代币预测) 、阶段10·25(投机解码原理) ⋅本节是生产版EAGLE-3。
>  **【类比】**简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简介: 简
**Time:** ~60 minutes | **时间:** ~60 分钟

## 学习目标

- 举个猜测解码的三个代,并解释EAGLE-3与EAGLE-2以及经典的草案模型所发生的变化.
  中文翻译:说出推测解码的三代,并解释Eagle-3 相比Eagle-2 和经典草案模型改变了什么――
- 定义接受率alpha,从alpha和K (草案长度) 计算预期加速,并确定目标同步率的破解式alpha.
  中文翻译:定义接受率alpha,从alpha 和 K(草案长度) 计算预期加速比,并确定目标并发下亏平衡alpha──
- 解释为什么在vLLM 2026中投机解码是选择式 (不是默认的) 以及为什么在没有测量alpha的情况下启动它是生产反模式的原因.
  中文翻译:解释为什么推测解码在2026年 vLLM 中是选择的(非默认),以及为什么不测量阿尔法就开始它是生产反模式――
- 写出测量计划:哪个基准,哪个提示分布,哪个同步点,哪个指标要进入.
  中文翻译:写出测量计划:哪个基准测试,哪个快速 分布,哪个并发点,哪个指标作为门控.

## 问题 问题引入

> **【中文解读】**推理的解码阶段是内存带宽限制的 每个解码一个代币需要读取约140GB/s的权重,GPU 计算几乎空──推测解码利用这个空:使用廉价的小模型生成K个候选代币,然后让目标模型在一次前向传播中验证所有K个体──接受率alpha是唯一重要的指标低于0.55时推测解码在高并发下反而有害──

> **【拓展：推测解码的产业应用】**谷歌将在2025年推测解码部署到AI概述 (搜索引擎摘要生成),在不损失质量的情况下显著加快响应速度.`speculative_config`作为官方接口──在生产中,推测解码特别适合实时对话(TTFT 敏感) 和代码补充全(延迟敏感)场景──但需要注意:高并发(256+) 当,解码批量已经足够大,内存带宽差距缩小,推测解码收益降低──

解码是内存的.在运行Llama 3.3 70B FP8的H100上,每个解码的代币都读取了140GB/s的权重,并发出了一个代币.在解码期间,GPU计算几乎是无效的.

> 解码是内存限制的. 在H100上运行的Llama 3.3 70B FP8 时,每个解码的代币 读取约140GB/s的权重并输出一个代币.

投机解码利用差距.使用廉价的草案模型生成K候选代币,然后要求目标模型在单次前进传递中验证所有K.每个验证的代币实际上是免费的 (将其抵免成一批K前进的代币,目标无论如何都必须做).

> 推测解码利用这个差距――使用廉价的草案 模型生成K个候选标记,然后让目标模型在一次前向传播中验证所有K个.每个验证通过的标记实际上是免费的(分摊到目标模型应该做的K批前向中) ⋅

经典的草案模型方法采用相同家族的较小模型 (Llama 3.2 1B 草案为Llama 3.3 70B). 虽然它有效,但接受率是中等的, ,然后-2,然后-3将轻微的导弹头直接放在目标模型的内部状态上, 这就是为什么阿尔法从0.4的草案模型到0.6-0.8的EAGLE-3.

> 经典的草案 模型方法使用同系列的更小模型(Llama 3.2 1B 为Llama 3.3 70B做草案) ⋅它可行但接受率平更小模型的分布偏离目标──EAGLE、EAGLE-2、EAGLE-3 直接在目标模型的内部状态上训练轻量级的草案头,所以草案的分布更接近目标──这就是为什么从草案的模型的0.4 升至EAGLE-3 的0.6-0.8──

鱼:EAGLE-3将加入VLLM2026年.`speculative_config`没有标志,没有加速. 没有测量Alpha的团队通常会看到尾声延迟变得更糟,而不是更好.

> 关键点:EAGLE-3 在2026年中是选择.`speculative_config`必须显式设置――没有标志,就没有加速――不测量真实流量阿尔法就开始的团队经常看到尾部延迟变差而不是改善――

## 概念的核心概念

### 什么是投机解码实际上买

> **【中文解读】**推测解码的加速比公式为`S = (1 + K*alpha) / (1 + verify_overhead)`△对于K=5,alpha=0.7,理论加速4.1x. 但实际生产通常只达到2-3x,因为alpha在实际流量上很少达到0.7以上,并且验证开销在高批量大时增长.

没有规范解码,每代币成本是一个目标前. 通过草案长度K和接受alpha的规范解码,每个目标前的预期代币是`1 + K * alpha`速度是`(1 + K * alpha) / (1 + epsilon)`对于K=5,alpha=0.7: `(1 + 5*0.7) / (1 + 0.1) = 4.5 / 1.1 = 4.1x`实际数字的集群大约2到3倍,因为Alpha在生产流量上很少高,而epsilon在高批量量上生长.

> 没有推测解码时,每个代币 成本是一个目标前向传播时,有推测解码时,草案长度 K 和接受率 alpha 下,每一个目标前向的预期代币数为 `1 + K * alpha`△加速比为`(1 + K * alpha) / (1 + epsilon)`对于K=5,alpha=0.7而言,`(1 + 5*0.7) / (1 + 0.1) = 4.5 / 1.1 = 4.1x`△实际数据集中在2-3倍,因为alpha在生产流量上很少,而epsilon在高批量量中增加.

### 为什么阿尔法是唯一重要的指标

拒绝的代币不会消失 它们强迫第二个目标向前,以获得第一个拒绝的代币. 在一个工作负载上,Alpha下降到0.4,你支付的草案总费加上验证加上重新滚动. 在高同步率 (例如 256 同步) 上,解码批量已经足够大,以至于"仅仅目标"和"仅仅验证目标"之间的内存带宽差距缩小. 在2026年大部分硬件上,

> 被拒绝的代币不会消失它们强制对第一个被拒绝的代币进行第二次目标前向传播. 在阿尔法下降到0.4的工作负载上,你付出了草案开销 +验证 + 重新生成. 在高并发的期内,解码批量已经足够大,"单独目标"和"带验证目标"之间的内存宽度差距缩小. 在2026年,在大多数硬件上,阿尔法低于0.55 时推测解码是净负面的.

在ShareGPT类型的通用聊天中,EAGLE-3在ShareGPT上训练达到0.6-0.8.在域特定流量 (代码,医疗,法律) 上,对一般数据训练的草案头下降到0.4-0.6.训练一个域特定的草案头恢复了alpha .

> 在 ShareGPT 风格的通用聊天天中,使用 ShareGPT 训练的 EAGLE-3 达到 0.6-0.8──在特定领域流量下,使用通用数据训练的草案头降至 0.4-0.6──在训练领域的具体草案头可以恢复 Alpha 与目标微调相比,这是一个轻量化、快速的训练任务──

### 子一眼的几代人

> **【中文解读】**推测解码经历了三代演进: 1) 经典草案模型(同一系列小模型,alpha 0.3-0.5) 简单但接受率低; 2) EAGLE-1/2(在目标模型隐藏状态上训练草案头,alpha 0.5-0.7) 更高的接受率; 3) EAGLE-3(在多层隐藏状态上训练,alpha 0.6-0.8) 2025-2026年生产阶段方案.

> **【拓展：推测解码 vs 其他加速技术】**士师推理加速技术对比:(1) 推测解码(EAGLE-3) 2-3x 加速,需要额外的草案头;(2) 量化(INT8/FP8) 推理加速 1.5-2x,有轻微质量损失;(3) 分块预填降低ITL尾巴但不直接提升吞吐量;(4) 分离式预填/解码消除资源浪费,30-40% 成本节省;(5) 自研芯片(Groq/Cerebras) 5-10x 解码速度但单价更高──这些技术可叠加使用:EAGLE-3 + FP8 + 分离式部署的综合效果可达10x──

- **Classic draft model**基础设施简单 两个型号加载,每一个目标向前运行K.
  翻译: 中文**经典 draft 模型**基础设施简单 载载两个模型,草案 每次目标前向运行 K 次前向.
- **EAGLE-1 (2024)**目标上面的小参数上层.
  翻译: 中文**EAGLE-1 (2024)**目标隐藏状态 (上) 训练单一草案头――Alpha 约0.5-0.6――目标上的小参数开销――
- **EAGLE-2 (2025)**根据图文的定义,该图文的长度可适应,基于树木的图文 (在一个目标传输中检查多个分支).
  翻译: 中文**EAGLE-2 (2025)**根据"长度和树"的草案,
- **EAGLE-3 (2025-2026)**预备主机训练多个目标层 (不仅仅是最后),更好的排列.
  翻译: 中文**EAGLE-3 (2025-2026)**们在们的们中,我们都在们的们中,

### 2026年生产配方

> **【中文解读】**生产环境 EAGLE-3 部署的五步流程: 1) 先以基础模型上线,建立TTFT/ITL/吞吐量基线; 2) 启动EAGLE-3草案配置; 3) 监控接受率 alphavLLM V1 通过`spec_decode_metrics.accepted_tokens_per_request`暴露此指标;(4) 如果阿尔法 < 0.55,禁用推测解码或训练领域特定的草案头;(5) 在生产并发水平重新测试,确认P99 ITL 没有恶化──

1. 测量基线TTFT,ITL,在目标同步时的吞吐量.
   中文翻译:先以基础模型上线――在目标并发下测量基线 TTFT、ITL、吞吐量――
2. 通过vLLM启用EAGLE-3草案`speculative_config`检查一个标准.
   中文翻译:通过vLLM `speculative_config`启动EAGLE-3草案.
3. 记录接受率 alfa. vLLM V1 报告`spec_decode_metrics.accepted_tokens_per_request`按要求的草稿长度划分,得到阿尔法.
   中文翻译:记录接受率 alpha──vLLM V1 通过 `spec_decode_metrics.accepted_tokens_per_request`报告――除了请求的草案 长度得到了阿尔法――
4. 如果生产流量分布的alpha <0.55 值,则禁用规格解码或训练一个特定领域的EAGLE-3草案.
   中文翻译:如果生产流量分布在alpha <0.55,禁用推测解码或训练领域特定的EAGLE-3草案.
5. 在生产同时,再运行.确认P99ITL没有变得更糟.
   中文翻译:在生产并发下重新测试──确认P99 ITL 没有恶化──

### 产量陷:P99尾

平均ITL下降了,如果不调节,P99可能会变得更糟.拒绝的草案会引发两次通过序列 (草案+验证失败+重滚).在全批次下,这些两个通过会串行.看P99 ITL,而不是P50.

> 平均ITL 随推测解码下降――如果不调优,P99可能恶化――被拒绝的草案 触发两次传递序列(草案+验证失败+重新生成)――在满批次下,这两次传递串行化――关注P99ITL,而不是P50――

### 已经部署EagLE-3的地区

谷歌在2025年部署了AI概述中的投机解码 (相同质量,更快的响应).`speculative_config`作为文档化界面;N-gram GPU 投机解码在V1中是与碎片预填充兼容的变体.SGLang 支持EAGLE-3作为预写重工作负载的建议草案路径.

> 谷歌将在2025年推测解码部署到AI概述.`speculative_config`作为文档化接口;V1 中的N-gram GPU 推测解码是与分块预填充兼容的变体――SGLang 支持EAGLE-3 作为前密集工作负载的推草案路径――

### 在一行中打破平数

预期加速:`S(alpha, K) = (1 + K*alpha) / (1 + verify_overhead)`设置`S = 1`解决了alpha: `alpha_breakeven = verify_overhead / K`对于典型的verify_overhead ~0.15和K=5: `alpha_breakeven = 0.03`但这是原始解码数学. 在高同步时,验证上空费用增加,并且解码批量已经 amortizes 连续性内存读数,所以有效的alpha_breakeven 实际上上上升到0.45-0.55.

> 预期加速比:`S(alpha, K) = (1 + K*alpha) / (1 + verify_overhead)`设 设`S = 1`求解阿尔法:`alpha_breakeven = verify_overhead / K`典型的验证额度约为0.15,K=5:`alpha_breakeven = 0.03`△但那是原始解码数学――在高并发下,验证开销增长,解码批次已经在序列间分摊内存读取,所以实际有效的阿尔法_破解平衡上升到约0.45-0.55─

### 什么时候不使用推测解码

> **【拓展：推测解码的适用场景】**推测解码在以下场景有效:(1) 实时对话(TTFT < 200ms 要求) 2-3x 加速显著改善用户体验;(2) 代码补充(实时性要求高);(3) 低并发场景(< 50 同时) 内存带宽差距大,收益明显.

> **【拓展：vLLM 推测解码配置】**支持三种推测解码模式:(1) 草案模型传统小模型作为草案,与零碎预填不兼容;(2) EAGLE在隐形状态训练的草案头,推用于通用场景;(3) N-gram GPU基于提示 中 N-gram 查找的 GPU端草案,是唯一与零碎预填兼容的模式.`speculative_config`必须显然设置,vLLM默认不开任何推测解码.

- 批发-1的离线生成,延迟不重要.
  中文翻译:延迟无关紧要的批量为1个离线生成――使用普通目标模型――
- 非常短的输出 (低于50个代币). 草案总费和验证成本占主导地位.
  中文翻译:非常短的输出(50个代币以下) ・草案 开销和验证成本占主导地位。
- 专业域没有专业训练的招聘负责人.
  中文翻译:没有领域训练草案负责人 的专业领域――Alpha 太低――
- 附加于草案模型规格解码`--enable-chunked-prefill`文件的例外是V1中的N-gram GPU规格解码.
  中文翻译:vLLM v0.18.0 + 草案模型 推测解码 + `--enable-chunked-prefill`◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎

## 用它实现框架
```figure
mx-speculative-tree
```

## 用它

`code/main.py`模拟一个在一系列alpha值和草案长度K中进行解码循环,并且没有猜测解码.它打印了破解式alpha,测量速度和尾声行为.在几种 (alpha,K) 组合上运行它,以查看猜测解码在哪里停止付费.

> `code/main.py`模拟有/无推测解码的解码循环,覆盖一系列的阿尔法值和草案长度 K――它印发了亏平衡阿尔法、测量加速比和尾部行为――在多个 (阿尔法,K) 组合上运行,精确看推测解码在哪里停止收益――

## 运送它.

这一课产生了`outputs/skill-eagle3-rollout.md`鉴于目标模型,流量分布描述和同步目标,它产生了一个阶段化的EAGLE-3部署计划基准线,启用配置,测量alpha,关键在alpha >=0.55,看P99ITL.

> 本课产出发 `outputs/skill-eagle3-rollout.md`△给定目标模型、流量分布描述和发发目标,它产生分阶段 EAGLE-3 推出计划基准基线、启动配置、测量阿尔法、以阿尔法 >= 0.55 作为门控、关注 P99 ITL──

## 练习题

1. 跑步`code/main.py`在K=5时,你需要什么alpha来加速2x? 3x?
   中文翻译:运行 `code/main.py`,这对验证过度有什么敏感性?
2. 想象一下,生产流量分为70%的通用聊天,30%的代码.通用聊天达到0.7的阿尔法, EAGLE-3在ShareGPT上训练;代码达到0.4的阿尔法.
   中文翻译:假设生产流量70% 通用聊天,30% 代码――通用聊天 亚尔法 0.7,代码 亚尔法 0.4――混合 亚尔法 是多少,推测解码是否净正向?
3. 阅读全文`speculative_config`列出三个模式 (草案模型,EAGLE,N-gram) 以及哪一种模式与碎片预填充兼容.
   中文翻译:阅读vLLM `speculative_config`文档――说出三种模式 (图案模型,EAGLE、N-gram) 和哪个与分块预填兼容――
4. 3启用后,平均ITL下降了25%,但P99ITL上升了15%.
   中文翻译:启用EAGLE-3后平均ITL下降25%,但P99ITL上升15%──诊断并提出缓解方案──
5. 计算Eagle-3预备头的内存成本. 如何与经典预备机运行Llama 3.2 1B相比?
   中文翻译:计算 Llama 3.3 70B 的 EAGLE-3 草案头 内存成本──与运行 Llama 3.2 1B 作为经典草案 相比怎么?

## 关键词 快速查找表

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| Speculative decoding | "draft plus verify" / "draft 加验证" | Propose K tokens with a cheap model, verify all K in one target forward / 用廉价模型提议 K 个 token，一次目标前向验证所有 K 个 |
| Acceptance rate alpha | "spec accept rate" / "推测接受率" | Fraction of draft tokens accepted by the target; the only metric that matters / 被 target 接受的 draft token 比例；唯一重要的指标 |
| Draft length K | "spec k" / "推测 K" | How many tokens the draft proposes per target forward; typical 4-8 / 每次 target 前向 draft 提议多少 token；通常 4-8 |
| Verify overhead epsilon | "spec overhead" / "推测开销" | Extra cost to verify-and-reroll vs a plain target forward; grows with batch / 验证+重新生成 vs 普通 target 前向的额外成本；随 batch 增长 |
| EAGLE-3 | "latest EAGLE" / "最新 EAGLE" | 2025-2026 variant; trains draft head on multiple target layers; alpha 0.6-0.8 / 2025-2026 变体；在多个 target 层上训练 draft head |
| `speculative_config` | "vLLM spec config" / "vLLM 推测配置" | The explicit opt-in in vLLM V1; no default means no acceleration / vLLM V1 中的显式 opt-in；无默认即无加速 |
| N-gram spec decode | "N-gram draft" / "N-gram draft" | GPU-side draft using N-gram lookups in the prompt; chunked-prefill-compatible / GPU 端使用 prompt 中 N-gram 查找的 draft；与分块预填充兼容 |
| Break-even alpha | "no-op alpha" / "无效果 alpha" | Alpha at which spec decode gives zero speedup; watch this at production concurrency / 推测解码零加速的 alpha；在生产并发下关注 |
| Rejected-draft two-pass | "reroll cost" / "重新生成成本" | Two target forwards when drafts reject; drives P99 tail / draft 被拒绝时的两次 target 前向；驱动 P99 尾部 |

## 继续阅读 继续阅读

- [vLLM — Speculative Decoding docs](https://docs.vllm.ai/en/latest/features/spec_decode/) 权威来源`speculative_config`并且在V1中兼容零碎预填充.
- [vLLM Speculative Config API](https://docs.vllm.ai/en/latest/api/vllm/config/speculative/)准确的场所.
- [EAGLE paper (arXiv:2401.15077)](https://arxiv.org/abs/2401.15077)原始的EagLE草案头格式.
- [EAGLE-2 paper (arXiv:2406.16858)](https://arxiv.org/abs/2406.16858)适应性草图和树木.
- [UC Berkeley EECS-2025-224](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-224.html)具有投机解码的高效LLM系统.
- [BentoML — Speculative Decoding](https://bentoml.com/llm/inference-optimization/speculative-decoding)生产部署检查清单.
