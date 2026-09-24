# 谈判和谈判 谈判 讨价还价

> 经纪人谈判资源,价格,任务分配和条款.2026年基准设定很清楚:谈判场 (arXiv:2402.05863) 显示LLM可以通过人格操纵提高收益率20% (绝望);"衡量谈判能力" (arXiv:2402.15813) 显示买家比卖家更难,规模不帮助他们**OG-Narrator**投资率从26.67%提高到88.88%;大规模自主谈判竞赛 (arXiv:2503.06416) 进行了约180000次谈判,发现**chain-of-thought-concealing**通过隐藏对手的推理,代理人获胜;Bhattacharya et al. 2025 在哈佛谈判项目测量中,Llama-3最有效,Claude-3最具侵略性,GPT-4最公平.这个课程实现了合同网协议 (FIPA祖先,课程02),线程LLM类型的买家/卖家,运行了OG-叙述者类型的分解,并测量了交易率如何随着每个结构选择变化.

> **【中文解读】**本节介绍了资源分配和任务分配的多代理商协商策略.

> **【拓展：negotiation bargaining→具体应用】**协商和讨价还价是多代理资源分配的核心机制――三种协商策略: 1) 合作型 代理追求整体利益最大化; 2) 竞争型 代理追求自身利益最大化; 3) 混合型 兼顾个人和整体.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 02 (FIPA-ACL Heritage), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 02（FIPA-ACL 遗产），Phase 16 · 09（并行群体网络）

>  **【前置】**学生节前请先掌握:16期·02期 ((FIPA合同网) ‧16期09期 ((群众) ‧博论基础 ((纳什均衡) ‧代理 协商 = 资源/价格/任务分配的讨价还价──
>  **【类比】**商务员 协商 = "二手市场砍价"――LLM 通过人 操纵(装穷)能多 20%;隐藏推理过程的代理 赢对手看不到你的底线――OG-Narrator 把商务拆为"确定性提议生成"+"LLM 叙述",交易率 26%→89%──模型差异:Llama-3 最有效、Claude-3 强势、GPT-4公平 最选即模型选风格──
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

两家代理商需要达成价格. 由于纯粹的语言提示,2024-2026年,LLCs以惊人的低率 (在 arXiv:2402.15813 中,紧密参数的交易中约27%) 达成交易. 规模并不能解决:GPT-4在谈判中结构上不比GPT-3.5更好;它在谈判的 *语言*上更好.

> 两位代理人需要达成价格一致. 在纯语言提示下,2024-2026年LLM成交率惊人的低. 在 arXiv:2402.15813的紧密参数化议价中约为27%.

根据LLM的基本问题,LLM将两个工作组合在一起,决定报价和叙述报价.OG-Narrator分开了这些:确定性报价生成器计算了数量的动作;LLM只叙述.交易率跳到89%.

> 根本问题是,LLM 混入了两个任务决定报价和叙述报价――OG-Narrator 将两者分开:确定性报价生成器计算数字变动;LLM 仅负责叙述――成交率升到约89%――

这反映了经典的多代理发现:脱离机制与通信层的胜利.合同网协议 (FIPA, 1996;史密斯, 1980) 是参考任务市场机制.将LLM插入叙述槽,你得到一个现代的LLM驱动任务市场.

> 这反映了经典的多代理发现:将机制与通信层解是胜利之道.

## 概念的核心概念

### 合同网,在一段

史密斯1980年合同网协议:**manager**广播**call for proposals (cfp)**其他**bidders**回答**propose**经理选择一个获胜者,并发送**accept-proposal**给获胜者**reject-proposal**获胜者完成工作. 选择性信息:**refuse**国际投资管理局编码这一点为`fipa-contract-net`互动协议.

> 史密斯 1980 年的合同网协议:**管理者**广播**提案请求（cfp）**其他**投标人**回复包含其报价的**提案**消息;管理者选择获胜者并向获胜者发送**接受提案**发送给落选者**拒绝提案**△获胜者执行工作──可选消息:**拒绝**投标人拒绝提案.`fipa-contract-net`交互协议.

### 为什么"OG讲述者"赢了

语言模型的谈判能力测量 (arXiv:2402.15813) 指出:

> 据"衡量语言模型的议价能力" (arXiv:2402.15813) 观察:

- 法律法规经常违反谈判规则 (以无意义的价格提供,忽略对方的ZOPA).
  中文翻译:LLM 经常违反议价规则 ((以无意义的价格报价,忽略对方的ZOPA) 
- 它们扎不好 (接受不好的首次报价;反报价比战略性).
  中文翻译:定效差 ((接受糟糕的首轮报价;以象征性而不是战略性的金额回报价) 
- 规模本身并不能解决这些问题.更大的模型使类似的战略错误更可靠.
  中文翻译:仅靠规模化不能解决这些问题.

关于"OG-Narrator"的解体:

```
           ┌──────────────────┐        ┌──────────────────┐
  state  → │ offer generator  │ price → │  LLM narrator    │ → message
           │  (deterministic) │        │  (writes the     │
           │                  │        │   human-style    │
           └──────────────────┘        │   accompaniment) │
                                       └──────────────────┘
```

报价生成器是一个经典的谈判策略:鲁宾斯坦谈判模型,泽顿策略或简单的价格交换.LLM讲述.信息包含确定性价格和自然语言框架.

交易率上升,因为:
- 价格保持在谈判区.
- 是战略性的,而不是情感的.
- 法律士做出自己的技能:写作.

> 成交率升高因为:
> - 价格保持在议价区间内.
> - 点是战略性的,而不是情绪化的.
> - 士做它擅长的事:写作.

### 谈判Arena的发现

根据"法典"的标准, arXiv:2402.05863提供了标准.

> 提供规范基准──主要发现:

- 通过采用个性化 ("我绝望能在周五之前销售") 个性化操纵是一种真正的策略.
  人操纵是一种真实策略.
- 公平/合作的代理人被敌对的代理人剥削;防御需要明确的反.
  中文翻译:公平/合作的代理被对抗性代理利用;防御需要显而易见的反向姿态──
- 根据标准,在约40%的基准场景中,对称对合结果趋于不公平.
  中文翻译:对称配对在40%的基准场景中得到不公平的结果.

这不是"LLM是坏谈判者". 这就是"LLM谈判太像人类,包括可剥削的部分.

> 这不是"LLM是糟糕的谈判者"......而是"LLM的谈判方式太像人类,包括可利用的部分"......

### 隐藏思想链

大规模自主谈判竞赛 (arXiv:2503.06416) 在许多LLM战略中进行了约180k的谈判.获奖者隐藏了他们的推理:

> 大规模自主协商竞赛 (arXiv:2503.06416) 在许多LLM策略上进行了约18万次协商.

- 如果一个代理打印"我只会去"$75; my reservation price is $任何一个人可以看到的,
  ,如果代理将"我只会出现在$75；我的保留价是 $打印到公开可见的草稿书上,对手会阅读它.
- 获胜者私下计算策略;输出道只包含了报价和最低要求的叙述.
  中文翻译:获胜者私下计算策略;输出通道只包含报价和最低限度的叙述.

对于"游戏理论" (Aumann 1976年关于理性和信息) 的2026年回声:揭示了你私人估值成本的回报.

> 曼 1976 关于理性和信息) 在2026年回应:透露私人估值会损失收益.

工程的提取:将私人抓板的文本与公共信息的文本分开.

> 工程要点:将私人草稿本上下文与公开消息上下文分离.

### 巴塔查里亚等2025年 模型排名

哈佛谈判项目指标 (原则性谈判,BATNA尊重,利益互惠):

> 在哈佛谈判项目目标上:

- **Llama-3**在交易中最有效 (交易率+收益率).
  翻译: 中文**Llama-3**在达成交易方面最有效的成交率+收益)
- **Claude-3**谈判最具侵略性的谈判者 (高,迟到的让步).
  翻译: 中文**Claude-3**很高点,晚让步.
- **GPT-4**配对中最公平 (最小的变化).
  翻译: 中文**GPT-4**最公平的利差距最小的利差距

问题不是2026年4月哪个模型赢得了胜利. 问题是,不同的基模型具有持久的谈判风格.异性集体 (课 15) 将这作为多样性来源.

> 焦点不是哪个模型在2026年4月获胜,而是不同的基础模型具有持久的谈判风格.

### 通过合同网 + LLM分配任务

现代的合同网的重用:

> 合同网在现代 LLM多代理中重用:

1. 管理员将任务分解成单元.
   中文翻译:管理者 代理将任务分解为单元――
2. 广播`cfp`工作人员的任务描述.
   中文翻译:向工作者 广播带任务描述的 `cfp`,我知道.
3. 每个工人都回报了一份报价:`(price, eta, confidence)`价格可能是代币,计算单位或美元.
   中文翻译:每个工作者回归一个报价:`(price, eta, confidence)`价格可以是代币,计算单元或美元.
4. 管理者选择获奖者 (单项或多项,具体取决于任务) 和奖项.
   中文翻译:管理者选择获胜者 (单个或多个,取决于任务)并授标――
5. 拒绝的工人可以自由投标其他任务.
   中文翻译:被拒绝的工作者可以竞标其他任务.

由于协调是播放和响应,而不是同步聊天. 在生产中使用:微软代理框架的编排模式,一些LangGraph实现.

> 由于协调是广播响应模式,而不是同步聊天.

### 合资企业利益相关者互动谈判

果产品https://proceedings.neurips.cc/paper_files/paper/2024/file/984dd3db213db2d1454a163b65b84d08-Paper-Datasets_and_Benchmarks_Track.pdf) 引入多方可得分游戏**secret scores**其他**minimum-acceptance thresholds**任何利益相关者都有私营公用事业;LLM必须从信息中推断这些信息.这是两党谈判的通用化到N党联盟的形成.对于具有异性工人能力的生产任务市场相关.

> 引入了 NeurIPS 2024 具有**秘密分数**和**最低接受阈值**对于各利益相关者来说,每个利益相关者都有私人效果;LLM必须从消息中推断.

### 叙述与机制规则

在2024-2026年所有谈判基准中,一致的工程规则是:

> 让法师讲述,不要让法师计算出报价.

> 让LLM 叙述. 不要让LLM 计算报价.

如果报价需要一个数字 (价格, ETA,数量),从谈判状态中确定性地生成它,并让LLM制作框架.如果报价需要一个提案结构 (任务分解,角色分配),让LLM起草它,但在发送之前根据一个方案和约束检查验证.

> 如果报价需要数字 (价格,ETA,数量),从协商状态确定性生成它,让LLM产生框架.

## 动手构建
```figure
a5-og-narrator
```

## 建立它

`code/main.py`执行:

- `ContractNetManager`现在`ContractNetTask`现在`Bid`经理+投标人,广播公司,收集提案,授予.
  翻译: 中文`ContractNetManager`,我知道.`ContractNetTask`,我知道.`Bid` 管理者 + 投标人,广播 cfp,收集建议,授标──
- `og_narrator_bargain(state, rng)` OG-Narrator买家:决定性的Zeuthen风格让步到中点.
  翻译: 中文`og_narrator_bargain` OG-Narrator 买方:确定性 Zeuthen 风格向中间点让步.
- `seller_response(state, rng)`确定性卖家反报政策 (对两种风格的结构性基础真理).
  翻译: 中文`seller_response` 确定性卖方还价策略 (二种风格的结构基准)
- `naive_llm_bargain(state, rng)`模拟全LLM交易者:选择高差异性价格,通常是超出ZOPA的.
  翻译: 中文`naive_llm_bargain`模拟全 LLM 议价者:以高方差选价,经常超出ZOPA。
- 测量:交易率超过1000个试验,每试验采样新鲜预订价格.
  中文翻译:测量:1000次试验的成交率,每次试验重新采样保留价格.

运行:

```
python3 code/main.py
```

预期产量:天真-LLM交易率~65-75%;OG-Narrator交易率~85-95%;15-25点差距是从叙述中分解产品生成的结构优势.加上一个有三个投标者和一个任务的合同网任务市场分配例子.

> 预期输出:朴素 LLM 成交率约65-75%;OG-Narrator 成交率约85-95%;15-25个百分点的差距是将报价产生与叙述解的结构优势――加上一个三个投标者和一个任务的合同网任务市场分配示例――

## 用它使用方法

`outputs/skill-bargainer-designer.md`设计谈判协议:谁生成报价 (定制性或LLM),谁讲述,私人剪辑板如何与公共信息分开,以及如何监测交易率.

> `outputs/skill-bargainer-designer.md`设计议价协议:谁产生报价 (确定性或LLM),谁叙述,私人草稿本如何与公开消息分离,以及如何监控成交率.

## 发射上线

生产谈判检查列表:

- **Separate scratchpad.**个人国家从来没有达到对方的背景.
  翻译: 中文**分离草稿本。**个人状态永远不会达到对手的下文.
- **Deterministic offer generation.**价格,数量,时间:计算,不要要求.
  翻译: 中文**确定性报价生成。**价格,数量,ETA:计算,不要提示.
- **Validate all incoming offers**拒绝在协议边界的非ZOPA报价.
  翻译: 中文**验证所有传入报价**根据模式. 在协议边界拒绝了ZOPA外的报价.
- **Bound rounds.**极限3-5次,在停滞时升级到中介.
  翻译: 中文**限制轮次。**最多3-5轮;死锁时升级到调解者──
- **Measure deal rate and payoff variance**交易率下降是症状,通常是迅速的漂移或对方攻击.
  翻译: 中文**持续测量成交率和收益方差。**降低成交率是症状,通常是提示漂移或对手攻击.
- **Log all rejected proposals**对于合同网经理来说,输入竞标者需要了解原因.
  翻译: 中文**记录所有被拒绝的提案**及确定性理由──对于合同网管理者,落选投标人需要理解原因──

## 练习题

1. 跑步`code/main.py`确认OG-Narrator比天真LLM在交易率.
   中文翻译:运行 `code/main.py`确认OG讲述者在成交率上优于简单的LLM.
2. 实施**persona-based payoff improvement**买家只在叙述中采用"绝望要买本周"角色,提供发电机不变.交易率或回报率是否改变?
   中文翻译:实现**基于人格的收益改进**买方只采用"本周急需购买"的人格,报价生成器不变.
3. 实现思想链**concealment**假设您不想通过道来模拟它,会发生什么?
   中文翻译:实现思维链**隐藏**维护一个不传递给对手的私人草稿本字符串.
4. 如何决定最低价格和最高质量的价格?你选择哪个奖项规则,为什么?
   中文翻译:将合同网扩大以保留价格为N 投标人拍卖.当所有投标超过保留价格时,管理员如何在最低价格和最高质量之间选择?你选择哪个授权规则,为什么?
5. 阅读Bhattacharya et al. 2025 在哈佛谈判项目指标. 实施两个不同的风格的讨价还价者 (侵略性与公平). 在对称和不对称对称下衡量回报差异.
   中文翻译:阅读Bhattacharya 等人2025年关于哈佛谈判项目目标论文――实现两个不同风格的议价者(攻击性与公平) ⋅测量对称和非对称配对下的收益方差――

## 关键词 关键词

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Contract Net / 合同网 | "Task market" / "任务市场" | Smith 1980, FIPA 1996. cfp + propose + accept/reject. The canonical task-market. / Smith 1980, FIPA 1996。cfp + propose + accept/reject。规范的任务市场。 |
| ZOPA / 可能协议区 | "Zone of possible agreement" / "可能协议区域" | Overlap between buyer's max and seller's min. Offers outside it cannot close. / 买方最大值和卖方最小值的重叠。超出此范围的报价无法成交。 |
| BATNA / 最佳替代方案 | "Best alternative to a negotiated agreement" / "谈判协议的最佳替代方案" | Your fallback if this deal fails. Sets your reservation price. / 如果交易失败的后备方案。设定你的保留价。 |
| OG-Narrator / OG-叙述者 | "Offer generator + narrator" / "报价生成器 + 叙述者" | Decomposition: deterministic offer, LLM narration. / 分解：确定性报价，LLM 叙述。 |
| Zeuthen strategy / Zeuthen 策略 | "Risk-minimizing concession" / "风险最小化让步" | Classical offer-generator that concedes based on risk limits. / 基于风险限制让步的经典报价生成器。 |
| Rubinstein bargaining / Rubinstein 议价 | "Alternating-offer equilibrium" / "交替报价均衡" | Game-theoretic model for infinite-horizon bargaining with discounting. / 带折现的无限期议价博弈论模型。 |
| CoT concealment / CoT 隐藏 | "Hide your reasoning" / "隐藏推理" | Winners in arXiv:2503.06416 kept private scratchpads; public channel shows offer only. / arXiv:2503.06416 的获胜者保持私人草稿本；公开通道只显示报价。 |
| Persona manipulation / 人格操纵 | "Emotional posturing" / "情绪姿态" | arXiv:2402.05863: ~20% payoff gain from desperation/urgency personas. / arXiv:2402.05863：绝望/紧迫人格带来约 20% 的收益增益。 |

## 继续阅读 继续阅读

- [NegotiationArena](https://arxiv.org/abs/2402.05863)基准指标;人格操纵和剥削的发现
- [Measuring Bargaining Abilities of Language Models](https://arxiv.org/abs/2402.15813) OG-Narrator 和买家比卖家更难的结果
- [Large-Scale Autonomous Negotiation Competition](https://arxiv.org/abs/2503.06416) ~ 180k 谈判; 思想链隐获胜
- [LLM-Stakeholders Interactive Negotiation (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/984dd3db213db2d1454a163b65b84d08-Paper-Datasets_and_Benchmarks_Track.pdf)多方可得分游戏,有秘密工具
- [Smith 1980 — The Contract Net Protocol](https://ieeexplore.ieee.org/document/1675516)经典机制,电脑上IEEE交易
