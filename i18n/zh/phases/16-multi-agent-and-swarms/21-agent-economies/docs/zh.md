# 代理经济,代币激励,声誉

> 长远自主代理 (METR的1小时到8小时工作曲线) 需要经济代理.**5-layer stack**是: **DePIN**物理计算**Identity**其他类型的资本**Cognition**子,子,子,子,子,子**Settlement**总结:**Governance**生产代理激励网络包括:**Bittensor**(TAO子网络奖励任务特定模型),**Fetch.ai / ASI Alliance**(ASI-1 Mini LLM + FET代币),以及**Gonka**学术工作:AAMAS 2025的分散式LAMAS使用 **Shapley-value credit attribution**为了公平地奖励贡献者;谷歌研究提出"大型语言模型机制设计"**token auctions**这一课程建立了一个最小的代理市场,将Shapley值的信用归因应应用于多代理管道,并进行了第二价格代币拍卖,以便游戏理论机器具体地落地.

> **【中文解读】**本节介绍了代理商经济多代理系统中的资源交易,定价和市场机制.

> **【拓展：agent economies→具体应用】**代理 经济探讨多 代理 系统中的资源分配和激励机制――核心概念:(1) 代币经济 代理使用代币支付服务;(2) 声誉系统 代理的服务质量影响其选择概率;(3) 拍卖机制 资源通过竞价分配――OpenAI的x402支付协议和MCP的范围 模型是代理经济的初步实现――


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 16 (Negotiation and Bargaining), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 16（协商与讨价还价），Phase 16 · 09（并行群体网络）

>  **【前置】**学本节前请先掌握:阶段16·16(协商) 、阶段16·09(群众) 、机制设计基础(肖普利 值、拍卖理论) ⋅代理 经济 = 多 代理 系统的市场层。
>  **【类比】**经纪人 经济 = "AI 自由市场"──5层:DePIN(算力) + 身份(DID+声誉) + 认知(RAG+MCP) + 结算(账户抽象) + 治理(Agentic DAO) ─ 发言人 子网奖励专门模型,Fetch.ai 用ASI-1 Mini + FET代币,Gonka 用变压器 PoW 把算力导向生产任务――学术价值:Shapley 给多个代币 公平分、二价 拍卖防操纵──
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

经纪人共同创造价值,但需要单独奖励时,多代理系统变得复杂. 经典机制 平等的分开,最后的贡献者取一切 是不公平的或可玩的. 通过Shapley价值观,基于联盟的奖励是公平的, 根据"中国经济发展"的指导,

> 多代理 系统在代理 共同产生价值,但需要单独奖励时变得复杂了.经典机制平分,最后贡献者全拿不公平或可操纵.基于联盟的Shapley价值奖励在构建上是公平但计算昂贵的.2025-2026年文献推动了有用的近似:Shapley采样"",单调聚合拍卖和从确认贡献中积累的链上声誉.

超越信用归因,该领域转向了实际的经济代理:Bittensor TAO奖励挖矿计算来调整子网特定模型,Fetch.ai/ASI奖励ASI-1迷你LLM使用FET代币,Gonka重新分配转former证明工作到生产人工智能任务.

> 超越信用归因,该领域转向了真正的经济代理:Bittensor TAO 奖励挖掘计算来微调网特定模型,Fetch.ai/ASI使用FET代币 奖励ASI-1迷你LLM使用,Gonka将转型 工作量证明重新分配给生产性AI任务――自主交易代理今天已经存在;问题是如何对齐激励――

这一课将代理经济作为一个特定的问题家庭 信用归因,机制设计和声誉 ,并构建每个与最小的数学,

> 本课程将经济体作为一个特定的问题, 信用归因,机制设计和声誉, 并使用最小的数学构建,使概念真正理解.

## 概念的核心概念

### 五层的代理经济堆

1. **DePIN (physical compute).**分散的基础设施,租用GPU,存储,带宽,比特ensor子网络,Render网络,Akash. 不是特征者,特征者使用它.
   翻译: 中文**DePIN（物理计算）。**租GPU、存储、带宽的去中心化基础设施──Bittensor 子网、Render Network、Akash──非代理 专用;代理使用它──
2. **Identity.**据W3C分离式识别器 (DID) 显示,每个代理都具有独立于任何平台的持久身份. 声誉来自于DID. 代理网络协议 (ANP) 使用DID作为发现层.
   翻译: 中文**身份。**据W3C去中心化标识符(DID) 给每个代理一个独立于平台的持久ID──声誉积累到DID──代理网络协议(ANP) 使用DID作为发现层──
3. **Cognition.**其他阶段的构建就是这样.
   翻译: 中文**认知。**代理的推理循环:LLM+RAG+MCP──这是其他阶段的构建──
4. **Settlement.**账户抽象 (ERC-4337) 允许代理人从自己的余额支付天然气,而无需持有ETH. 代理人可以为服务支付,相互支付或计算.
   翻译: 中文**结算。**账户抽象(ERC-4337) 让代理人从自己的余额支付天然气而无需持有ETH──代理人可以支付服务、相互支付或支付计算──
5. **Governance.**代理DAO:由人类和代理人投票对协议变更的治理结构,投票权与声誉有关.
   翻译: 中文**治理。**代理人:人类*和*代理对协议变更投票的治理结构,投票权和声誉绑定.

不是每个生产系统都使用五个.Bittensor使用1,2,部分3,部分4,没有一个.OpenAI代理除了3个,都没有使用.

### ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

**Bittensor (TAO).**矿工提交模型输出.验证器将它们排名;权重分数分配了TAO奖励.每个子网都有自己的评估.经济课程:为特定任务的输出质量付费,而不是使用的计算.

**Fetch.ai / ASI Alliance.**作为一个"FET"的代理,FET.ai的代理可以在FET中调用另一个任务,并支付FET.

**Gonka.**变压器证明工作:"工作"是变压器的前进通行.矿工通过运行已知正确输出 (从训练数据) 的推断任务来获得收入.资源生产的PoW而不是基于哈希的PoW.

截至2026年4月,所有三种产品均为生产级. 付款分布不同. 比特器对子网验证器的质量进行了奖励; 通过付费用户测量的Fetch奖励实用性; Gonka奖励可验证的推断工作.

### 石灰值信用归因

现在,我们有三位代理人合作, 输出率为0.8.

石普利值:满足四个定理 (效率,对称性,线性,零) 的独特信用分配.`i`其他:

```
shapley(i) = (1/N!) * sum over all orderings O of (v(S_i_O ∪ {i}) - v(S_i_O))
```

在哪里`S_i_O`是之前的代理群`i`在顺序中`O`实际上:列出所有变量,记录每个变量中的每个代理的边际贡献,平均.

对于N=3的代理,有6个变量.对于N=10,3.6M ,所以实际上你采样排序而不是编写.

### 集成二价拍卖

谷歌研究 ("大型语言模型机制设计") 为集成LLM产品提出了二价代币拍卖. 设置:N代理人每一个提出完成;每个有个别的值被选中. 拍卖商选择了最高价值的提案,并支付了第二最高价值. 在单调的聚合下 (价值取决于选择哪个提案,而不是多少投标),这是真实的 代理投标他们的真实价值.

为什么这对LLM系统很重要:你可以将完成任务外包给多个代理商,价格不同;拍卖会选择最好的 + 公平的报酬,代理商没有动机报告错误.

### 声誉资本

根据证实贡献,获得了DID相关的声誉分数.

```
rep(i, t+1) = alpha * rep(i, t) + (1 - alpha) * contribution_quality(i, t)
```

具有衰变因素`alpha`接近 1. 声誉:

- 对于路由决策来说,阅读便宜 ("将艰难任务发送给高代表代理").
- 造成本高昂 (随着时间的推移积累,与DID相关).
- 可减小:未能验证的贡献减小.

### 亚马斯2025分散式拉马斯

拉马斯提案 (AAMAS 2025) 结合了:DID身份,Shapley值信用归因和简单的拍卖机制.关键要求:分散信用归因步骤使系统可审计并不受单点操纵的影响.

### 经济在哪里崩

- **Price oracle manipulation.**如果可以玩信用函数,代理人会玩它.
- **Sybil attacks.**一个运营商把N个假代理起来,以膨胀自己的贡献.
- **Verification cost.**如果验证是便宜的 (小型的法定律师),它可以被玩弄;如果昂贵 (人群),系统不会扩展.
- **Regulatory overhang.**代理经济与金融监管交叉. 比特森索,费奇和冈卡都在2026年开始在某些司法管辖区的法律灰色区域运营.

### 当代理经济有意义时

- **Open networks with heterogeneous operators.**没有一个团队控制所有的代理人.
- **Verifiable outputs.**没有验证,信贷归因是猜测.
- **Long-horizon workflows.**一次任务不会从声誉积累中受益.
- **Tokenized payments are legally viable**在您的管辖范围内.

在封闭的企业系统中,经济学更容易分配 (管理人员分配工作,指标是内部的).经济学文献主要适用于开放网络.

## 动手构建
```figure
swarm-auction
```

## 建立它

`code/main.py`执行:

- `shapley(value_fn, agents)`精确的Shapley计算通过小N的编号.
- `second_price_auction(bids)`真实机制; 获奖者是第二位最高的.
- `Reputation`                                                                                                                                                                                                                                                              
- 演示1:三名代理合作,恰恰是莎普利的信用.
- 五个代理人投标一个任务槽;第二价拍卖选中赢家 + 付款.
- 演示 3:100轮任务分配给异质代表的代理人; 代表权重的路由跳动随机.

运行:

```
python3 code/main.py
```

预期产量:每个代理的Shapley值;拍卖结果显示出真实报价平衡;重复路由显示在加热后随机增长10%到20%的质量.

## 用它使用方法

`outputs/skill-economy-designer.md`设计一个最小代理经济:身份层的选择,信用归因机制,支付机制,声誉规则.

## 发射上线

管理2026年的代理经济:

- **Start with reputation, not tokens.**凭借代币,人们的声誉便宜,而且仅仅是有价值的.
  翻译: 中文**从声誉开始，不是 token。**声誉实现廉价且独有价值;令法律和经济复杂性增加.
- **Verify before you reward.**没有独立的验证步骤,永远不要分配信用.
  翻译: 中文**先验证再奖励。**没有独立验证步骤永远不要分配信用.
- **Shapley-sample, not Shapley-exact.**样本100-1000次;精确的清单不计量.
  翻译: 中文**Shapley 采样，而非 Shapley 精确。**采样 100-1000 个排序;精确枚举不可扩展.
- **Cap decay factor and floor reputation.**无限的腐蚀会抹去合法贡献者;过度缓慢的腐蚀会奖励过时的高反应剂.
  翻译: 中文**限制衰减因子和最低声誉。**无界衰减抹抹合法贡献者;太慢的衰减奖励过往的高声誉代理人.
- **Audit mechanisms adversarially.**在打开网络之前,运行红队场景. 每个机制都有游戏理论;你想找到洞穴,而不是攻击者.
  翻译: 中文**对抗性审计机制。**开放网络前运行红队场景――每个机制都有博论;你想找到漏洞,而不是攻击者――

## 练习题

1. 跑步`code/main.py`确认Shapley值总值到总值 (效率定理).改变值函数;Shapley分配是否改变预期方向?
2. 运用Shapley *样本* (Monte Carlo对K序列).K如何影响近似准确性?比较为精确为N=4.
3. 在拍卖之前,实施联盟形成步骤:代理人可以合并成团队并作为一个单位进行竞标.哪些联盟形成?结果比个人竞标更好吗?
4. 读一读Google研究机制设计文章. 确定一个假设,如果被违反,会破坏真相.在LLM设置中,失败模式是什么样子?
5. 阅读AAMAS 2025分散的LAMAS论文. 执行他们的Shapley步骤超过10个代理人在合成任务. 精确计算需要多长时间? 抽样得到了多近100抽奖?

## 关键词 关键词

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| DePIN / 去中心化物理基础设施 | "Decentralized physical infrastructure" / "去中心化物理基础设施" | Token-incentivized compute/storage/bandwidth. Bittensor, Akash, Render. / Token 激励的计算/存储/带宽。Bittensor、Akash、Render。 |
| DID / 去中心化标识符 | "Decentralized identifier" / "去中心化标识符" | W3C spec for portable IDs. Agent reputation binds to DID, not to a platform. / W3C 便携 ID 规范。Agent 声誉绑定到 DID，而非平台。 |
| ERC-4337 / 账户抽象 | "Account abstraction" / "账户抽象" | Contract accounts that can sponsor gas, enabling agent payments. / 可以赞助 gas 的合约账户，使 Agent 支付成为可能。 |
| Shapley value / Shapley 值 | "Fair credit attribution" / "公平信用归因" | Unique allocation satisfying efficiency, symmetry, linearity, null. / 满足效率、对称、线性、零贡献者的唯一分配。 |
| Second-price auction / 二价拍卖 | "Vickrey auction" / "Vickrey 拍卖" | Truthful mechanism: winner pays second-highest bid. Monotone aggregation compatible. / 诚实机制：获胜者支付第二高出价。兼容单调聚合。 |
| Reputation capital / 声誉资本 | "Accumulated quality score" / "累积质量分数" | DID-bound score from confirmed contributions; decays over time. / DID 绑定的来自确认贡献的分数；随时间衰减。 |
| Agentic DAO / Agent DAO | "Agents + humans govern" / "Agent + 人类治理" | DAO with agent voters as first-class, voting power tied to reputation. / Agent 投票者作为一等公民的 DAO，投票权与声誉绑定。 |
| TAO / FET / GPU credits / Token 面额 | "Token denominations" / "Token 面额" | Bittensor TAO, Fetch.ai FET, various DePIN tokens. / Bittensor TAO、Fetch.ai FET、各种 DePIN token。 |

## 继续阅读 继续阅读

- [The Agent Economy](https://arxiv.org/abs/2602.14219) 2026年5层代理经济堆调查
- [Google Research — Mechanism design for large language models](https://research.google/blog/mechanism-design-for-large-language-models/)单调聚合的代币拍卖
- [AAMAS 2025 — decentralized LaMAS](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2896.pdf) 石灰值信用归类
- [Bittensor TAO documentation](https://docs.bittensor.com/)子网结构和奖励分配
- [Fetch.ai / ASI Alliance](https://fetch.ai/)ASI-1迷你法学和FET代币
- [W3C Decentralized Identifiers (DIDs) spec](https://www.w3.org/TR/did-core/)身份基础
