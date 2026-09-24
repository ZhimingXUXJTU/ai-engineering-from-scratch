# 混沌工程 工程 生产 混沌 工程 生产

> 士专业的混乱工程将在2026年成为自己的学科. 在生产中进行实验之前的先决条件:定义的SLI/SLO,跟踪+计量+日志可观测性,自动回滚,运行簿,调用. 建筑有四个层面:控制 (实验安排器),目标 (服务,基础设施,数据存储),安全 (监护+中断+交通过器),可观察性 (计量+痕迹+日志),反 (SLO调整). 防护轨道是强制性的:如果预计每天错误预算燃烧> 2x,燃烧率警报暂停实验;压制窗户 + 追踪识别相关性减持警报噪音. 时间:每周的小鱼+SLO审查;每月的游戏日+死后测试;每季度的跨团队弹性审计+依赖性映射. 专业化实验:内存过载,网络故障,供应商中断,错误的提示,KV缓存驱逐风暴. 工具:利用混沌工程 (LLM衍生的建议,爆炸射线缩放,MCP工具集成);LitmusChaos (CNCF);混沌网 (CNCF Kubernetes本土).

> **【中文解读】**本节介绍了士的工作实践.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy chaos experiment runner) | **语言:** Python
**Prerequisites:** Phase 17 · 23 (SRE for AI), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 23 (SRE for AI), Phase 17 · 13 (Observability)

>  **【前置】**学本节前请先掌握:阶段17·23(SRE) 、阶段17·13(可观测性) 、SRE 基础(SLI/SLO/错误预算) ・LLM 混沌工程 = 主动注入故障测量性。
>  **【类比】**机械工程 (LLM) 混沌工程 = "消防演习"――前提:SLI/SLO 定义好、可观测、自动回滚、跑本、上调――四平面:控制(实验调度) +目标(服务/数据/基础设施) +安全(守卫/停止/流量过) +可观测――必须护:错误预算燃烧率 > 2x 时暂停实验──节奏:每周小卡纳里度+月度游戏日+季度跨团队审计──LLM 专属实验:内存过载、网络故障、提供商 机机、坏快点、KV缓存 驱逐风暴──
**Time:** ~60 minutes | **时间:** ~60 minutes

## 学习目标

- 举个五个混乱工程前列条件 (SLI/SLO,可观测性,反弹,跑本,通话) 并解释为什么跳过任何情况会破坏实践.
  中文翻译:说出五个混沌工程前置条件 (SLI/SLO、可观测性、回滚、运行手册、待命文化)
- 绘制四个平面 (控制,目标,安全,可观测性) 和反循环成SLO.
  中文翻译:绘制四个平面 (控制,目标,安全,可观测性) 和反循环到SLO仪表板.
- 列出五项专业管理师专业实验 (内存过载,网络故障,供应商停机,错误的提示,KV驱逐风暴).
  中文翻译:列举五个 LLM 特定的混沌实验 (内存过载、网络故障、提供商机、形输入、缓存失效) 
- 选择一个工具                 
  中文翻译:选择工具Harness、LitmusChaos、Chaos Mesh根据技术。

## 问题 问题引入

> **【中文解读】**混沌工程是2026年的独立学科. LLM 增加了新的故障模式:4K-代号的毒化字符使分词器卡住12秒; 上游提供商 429 触发网关重试,重试放大并发导致OOM;突发负载下KV缓存 淘汰风暴引发重新预填级联,耗尽计算资源. 这些都不会出现在单元测试中混沌工程工具用户才发现它们.

> **【拓展：LLM 混沌工程的五类实验】**2026年LLM 特定五类混乱实验:(1) 内存过载发送长上下文高并发请求引发KV缓存 抢占风暴,观察服务是优雅降级还是崩;(2) 网络故障断推理网关与供应商的连接,观察故障是否在SLA内生效;(3) 供应商中断模拟100%OpenAI 429,观察路由是否失败到人类;(4) 形提示注入器具死亡是否负载(分层嵌套 Unicode、UTF-8码点),观察单个请求锁定工作者淘汰;5) KV 淘汰巨大暴风和LLM 块预算强制淘汰, L((还恢复服务MC 降级观察.

在传统堆中建立了混乱测试.LLM堆增加了新的故障模式.一个有毒字符的4K代码提示会停滞12秒.一个上游提供商429;你的网关重新尝试;你的服务OOM在重新加大同时尝试.在爆发负载下KV缓存驱逐风暴导致重新填充布,使计算机和.

混沌工程是你在用户之前发现它们的方式.

## 概念的核心概念

### 条件

> **【中文解读】**在生产中运行混沌测试的五个前提: 1) SLI/SLO 已定义; 2) 可观测性(跟踪+计量+日志) 已部署; 3) 自动回滚机制就绪; 4) 结构化跑本已编写; 5) 有值得的员工响应――缺少任何一项,混沌就会变成真实事件――四个平面:控制面(实验调度器) 目标面服务/基础设施) 安全、面杀开关+抑制窗口+爆炸射线 限制) 、观测面标志+跟踪 关联) ⋅反循环将可回归到 SLO 调整、运行 更新和代码书修复.

没有:

1. **SLI/SLO**确定服务水平指标和目标.
2. **Observability**跟踪,指标,日志,连接到仪表板.
3. **Automated rollback** 17 阶段 · 20 政策旗反弹.
4. **Runbooks**结构化,第17阶段 · 23.
5. **On-call**有人要回应.

没有任何手段,混乱变成了真实的事件.

### 四个飞机+反

**Control plane**实验安排器 (Litmus工作流程,混沌网时间表,利用 UI).

**Target plane**服务,片,节点,负载平衡器,数据存储器.

**Safety plane**杀死开关,压制窗户,爆炸射线限制,错误预算门.

**Observability plane**正常的指标 + 痕迹-ID相关性,以区分导致混乱的故障与自然故障.

**Feedback loop**结果回应SLO调整,运行簿更新,代码修复.

### 护卫是强制性的

> **【拓展：混沌工程的安全护栏】**混沌工程的三个必要安全护理: 1) 燃烧尽可能的报警报警实验期间如果每天的错误预算消耗超过预期的2倍,自动暂停实验; 2) 抑制窗口在实验爆炸半径内静默非实验报警,避免电话噪音; 3) 追踪身份证关联所有实验引起的错误携带标签,使电话可以重复. 这些护理可以确保混沌实验不会变成真实的事件缺少任何一个都意味着混沌失控.

- **Burn-rate alert**假设每天的错误预算损耗超过预期的2倍.
- **Suppression windows**试验期间,在爆炸半径中制非试验警报.
- **Trace-ID correlation**试验引起的错误都包含一个标签,以便在调用时可以推断.

### 五项专业士专业实验

1. **Memory overload**通过发送高同步度的长文本请求,强加KV缓存预先风暴. 注意:服务是否优雅地流失或崩?

2. **Network failure**断断推断网关与提供商之间的连接. 观察:SLA内是否会出现反弹? (阶段17 · 19)

3. **Provider outage simulation** 100% 429 来自OpenAI. 观察:路由向人类转移吗? (阶段 17 · 16, 19)

4. **Malformed prompt**注入标记器安装有效载荷 (例如,深嵌入式单码,巨大的UTF-8代码点).观察:单个请求是否锁定了员工?

5. **KV eviction storm**通过和VLLM区块预算强迫流离失所.

### 率

- **Weekly**小鱼实验,可能是5%的推进.
- **Monthly** 规划的比赛日,具体场景;跨团队出席;死后.
- **Quarterly**跨团队弹性审计;依赖性地图更新.

### 工具

> **【拓展：混沌工程工具选择】**2026年混沌工程工具选择:(1) 运用混沌工程商业,AI 驱动的实验推,爆炸射线自动缩放,MCP 工具集成;(2) 利特姆斯混沌CNCF 毕业,Kubernetes 工作流式;(3) 混沌网CNCF 沙箱,Kubernetes-本土CRD风格;(4) 格林商业,广泛支持;(5) AWS FIS / Azure Chaos Studio托管云服务;;节奏建议:每周可纳里 实验 + SLO 审查,每月游戏日 + 后期,每季度跨团队性审计 + 依赖映射更新;;

- **Harness Chaos Engineering**商业;人工智能衍生的实验建议;爆炸射线缩放;MCP工具集成.
- **LitmusChaos** CNCF毕业;库伯内特工作流程.
- **Chaos Mesh** CNCF沙盒;古伯内特斯原生CRD风格.
- **Gremlin**商业;广泛支持.
- **AWS FIS**现在,**Azure Chaos Studio**管理云服务.

### 开始小

首先,在稳定的流量下,杀死一个解码复制器. 观察转向和恢复. 如果这有效,看起来很安全,则会导致网络混乱.

首先,一个专业专业实验:给一个提供者注射429药物5分钟.观察倒退.大多数团队发现他们的倒退还没有完全测试.

### 你应该记住的数字

- 控制,目标,安全,可观察.
- 预期每日预算的燃烧量是两倍.
- 率:每周的鱼,每月的游戏日,每季度的审计.
- 五次LLM实验:记忆,网络,提供商,错误的提示,KV风暴.

## 用它实现框架
```figure
i4-chaos-guard
```

## 用它

`code/main.py`报告了哪些实验会使燃烧率失效.

> `code/main.py`报告了哪些实验会使燃烧率失效.

> `code/main.py`报告了哪些实验会使燃烧率失效.

## 运送它.

这一课产生了`outputs/skill-chaos-plan.md`鉴于积和成熟度, 选择了第3次实验和工具.

> 本课产出发 `outputs/skill-chaos-plan.md`鉴于积和成熟度, 选择了第3次实验和工具.

## 练习题

1. 跑步`code/main.py`什么实验会打破燃烧率的门,为什么?
   中文翻译:运行 `code/main.py`什么实验触发了燃烧率控制?
2. 设计一个基于vLLM的RAG服务的前五次混乱实验.
   中文翻译:为基于vLLM的RAG 服务设计前五个混沌实验.
3. 你的燃烧率警报暂停了实验.
   中文翻译:你的燃烧率告警暂停了一个实验.
4. 争辩,生产中应该发生混乱还是仅仅是舞台化.
   中文翻译:论证混沌实验应该在生产中还是仅在预发布环境运行中.
5. 举个简单的网络混乱无法复制的三种LLM特定故障模式.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| SLI / SLO | "service targets" | Indicator + objective; required prerequisite |
| Blast radius | "scope" | Set of services / users affected by experiment |
| Burn-rate alert | "budget gate" | Fires when error-budget burn rate > 2x expected |
| Game day | "monthly drill" | Scheduled cross-team chaos exercise |
| LitmusChaos | "CNCF workflow" | Graduated CNCF Kubernetes chaos tool |
| Chaos Mesh | "CNCF CRD" | CNCF sandbox Kubernetes-native chaos |
| Harness CE | "commercial AI-assisted" | Harness chaos with AI recommendations |
| Malformed prompt | "tokenizer bomb" | Input that stalls tokenization |
| KV eviction storm | "preemption cascade" | Mass eviction triggering re-prefills |

## 继续阅读 继续阅读

- [DevSecOps School — Chaos Engineering 2026 Guide](https://devsecopsschool.com/blog/chaos-engineering/)
- [Ankush Sharma — Observability for LLMs (book)](https://www.amazon.com/Observability-Large-Language-Models-Engineering-ebook/dp/B0DJSR65TR)
- [LitmusChaos (CNCF)](https://litmuschaos.io/)
- [Chaos Mesh (CNCF)](https://chaos-mesh.org/)
- [Harness Chaos Engineering](https://www.harness.io/products/chaos-engineering)
- [AWS FIS](https://aws.amazon.com/fis/)
