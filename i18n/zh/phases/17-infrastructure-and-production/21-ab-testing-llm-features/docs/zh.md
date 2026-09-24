#  增长书,Statsig,和动问题

> 传统的A/B测试并没有为非确定性 LLM而建立. 重要区别:评估答案是"模型能做好工作吗?"A/B测试答案是"用户是否关心?" 2026年要测试什么:快速工程 (表达式),模型选择 (GPT-4 vs GPT-3.5 vs OSS;准确性 vs 成本 vs 延迟),生成参数 (温度,顶级). 实例:聊天机器人奖励模型变体提供了+70%的对话长度和+30%的保留;接下来AI主题线实验提供了+1%的CTR后奖励功能的完善;Khan Academy Khanmigo在延迟与数学准确性轴上进行了代. 平台分开:**Statsig**测试序列,CUPED,全共一. **GrowthBook**开源,仓库本土,贝叶斯式+频率化+序列引擎,CUPED,SRM检查,Benjamin-Hochberg+Bonferroni修正.您根据仓库SQL偏好选择,以及"OpenAI收购"是否对您的组织重要.

> **【中文解读】**本节介绍了LLM特性的AB测试科学评估LLM功能变更效果的方法.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy sequential test simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 20 (Progressive Deployment) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 20 (Progressive Deployment)

>  **【前置】**学本节前请先掌握:阶段17·13(可观测性) ‧阶段17·20(渐进部署) ‧统计基础(CUPED、序贯测试) ‧传统A/B 不为不确定性LLM设计──
>  **【类比】**测试: 测试: 快速措辞,模型选择,生成参数,温度/顶部p) 测试: 聊天机器人变体+70% 对话长度+30% 留存; 下门AI标题+1% CTR; 延迟与 数学准确率间舍.
**Time:** ~60 minutes | **时间:** ~60 minutes

## 学习目标

- 区分评估 ("模型能做好工作吗") 和A/B测试 ("用户关心").
  中文翻译:区分评估("模型能做这个工作吗")和A/B 测试("用户在乎吗")。
- 列出三个可测试轴 (提示,模型,参数) 并为每个轴选择指标.
  中文翻译:列举三个可测试轴 (提示、模型、参数)并为每个选择指标──
- 解释CUPED,序列测试和Benin-Hochberg多次比较纠正.
  中文翻译:解释CUPED、序贯检验和本杰明尼-霍奇伯格 多重比较校正──
- 根据库存SQL姿势和企业收购态度,选择Statsig或 GrowthBook.
  中文翻译:根据仓库-SQL 态势和企业收购立场选择 状态或增长书──

## 问题 问题引入

> **【中文解读】**传统A/B测试不是为不确定性 LLM 构建的. 关键区分:评估(evals) 回答"模型能做这个事吗?",A/B测试回答"用户在乎吗?"两者都是必需的凭感觉上线(vibes检查) 的时代已经结束.

> **【拓展：LLM A/B 测试的真实案例】**2026年LLM A/B测试的生产案例:(1) 聊天机器人奖励模型变体+70% 对话长度、+30% 留存率;(2) 下门AI主题行实验奖励函数优化后+1% CTR;(3) 汗学院 汗敏在延迟对数学准确率轴上代.

你手动调整了系统提示.它感觉更好.你运送它.转换变化是通过噪音.你责怪的指标.或者你运送一个新模型,转换没有移动?

标准答案是模型是否可以在标记的集合上完成任务.它们没有回答用户是否更喜欢输出.只有一个受控的在线实验才能回答这个问题,只有实验有足够的权力,控制非确定性,并对多个比较进行纠正.

## 概念的核心概念

### 平均值与A/B测试

**Evals**离线,标签集,法官 (标签或法官或人). 回答:"这个固定分布的输出是否正确/有用/安全?"

**A/B test**在线,现场用户,随机. 回答:"新变体是否移动了重要的是用户水平的指标?"

既需要,Evals在暴露前捕获回归;A/B后确认产品影响.

### 测试什么

1. **Prompt engineering**语法,系统提示结构,例子. 计量:任务成功,用户保留,成本/请求.
2. **Model selection** GPT-4 vs GPT-3.5-Turbo vs Llama-OSS. 计量:准确性 (任务) +成本/请求 + 延迟 P99. 多目标.
3. **Generation parameters**温度,顶部p,max_tokens. 计量:任务特定 (输出多样性与确定性).

###         

> **【中文解读】**根据CUPED的原则,在比较后期之前,返回前期的差异――典型差异降低了30-70%,等效于免费增加有效样本量――Statsig和GrowthBook都实现了CUPED――

试验前数据. 在比较后期之前,退出前期差异.典型差异减少: 30-70%.有效的样本大小免费增加.

实施: Statsig 和 GrowthBook 两者都实施.

### 序列测试

经典A/B假设样本大小是固定的. 序列测试 ("望和决定") 在重复的看法下控制虚假阳性率. 始终有效的序列程序 (mSPRT,霍华德的信心序列) 让你早点停止清晰的获胜者.

### 复杂比较纠正

运行20次A/B测试, 95%的信心,随机产生一个假阳性. 波恩弗罗尼纠正每次测试加紧 α; 布尼亚米尼-霍奇伯格控制了假发现率. 增长书实现了两者.

###  SRM 样本比率不匹配

分配哈希将用户随机分为变体.如果50/50分分为47/53,则有东西被打破.

### 经济与增长

> **【拓展：Statsig vs GrowthBook 选型】**据悉,在该公司的数据库中,有了大量的数据库,但它还没有被开发出,因为它已经被开发出了,但它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发出了,它已经被开发了,它已经被开发出了,它已经被开发出了,它已经被开发了.

**Statsig**其他:
- 收购于OpenAI为1.1亿美元 (2025年9月). 主机,SaaS.
- 测试,CUPED,持续的群体.
- 一个全合:特征标志+实验+可观测性.
- 团队已经想要一个捆绑的产品, 不关心OpenAI的所有权.

**GrowthBook**其他:
- 开源 (MIT);仓库本土 (直接从Snowflake/BigQuery/Redshift中读取).
- 机器的数量:贝叶斯式,频率式,序列式.
- ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.
- 提供自主托管或管理云.
- 数据团队控制了测量层,想要OSS.

### 不确定性使权力复杂

根据标准,在测试中,测试结果的结果是不同的. 传统的功率计算假设是IID观测. 在LLM非确定性学中,有效样本大小低于名义. 乘以安全边缘的1.3-1.5x所需的样本大小.

### 实际案件结果

- 聊天机器人奖励模式变异: +70%的对话长度,+30%的保留.
- 接下来的主题线: 奖励函数完善后的+1%的CTR.
- 学院:反复延迟与数学准确度交易.

### 反模式:在振动上运输

> **【拓展：LLM 非确定性对 A/B 测试的影响】**在LLM不确定性下,有效样本量低于名义值需要将所需样本量乘以1.3-1.5x 作为安全边际. 序列测试) 允许在明确的获胜者出现时提前停止,比固定样本量测试节省20%-40%的实验时间.

任何高级工程师都能命名出出货的功能,因为"感觉更好",没有A/B. 大多数产品的指标退后,团队几个月没有注意到.A/B是强迫函数.

### 你应该记住的数字

- 美国国家航空公司收购的Statsig:2025年9月11亿美元.
- 增长书:开源MIT;贝叶斯语+频率主义+序列.
- 减轻CUPED变异率:30-70%.
- 专业学历非确定性 → +30-50%的样本尺寸缓冲.

## 用它实现框架
```figure
mx-sequential-test
```

## 用它

`code/main.py`模拟一个连续A/B测试,有固定和连续边界.

> `code/main.py`模拟一个连续A/B测试,有固定和连续边界.

> `code/main.py`模拟一个连续A/B测试,有固定和连续边界.

## 运送它.

这一课产生了`outputs/skill-ab-plan.md`鉴于功能变化,工作量,基线,平台选择,门口,样本大小.

> 本课产出发 `outputs/skill-ab-plan.md`鉴于功能变化,工作量,基线,平台选择,门口,样本大小.

## 练习题

1. 跑步`code/main.py`预计5%升降,基线转换3%的样本大小为80%功率?
   中文翻译:运行 `code/main.py`△预期5% 提升,基线3% 转换率,需要多少样本?
2. 选择Statsig或 GrowthBook,以供医疗保健监管的本地客户.
   中文翻译:为医疗保健监管的本地部署客户选择Statsig或增长书.
3. 设计一个A/B测试GPT-4与GPT-3.5的价格.
   中文翻译:设计一个在每解决工单成本上测试 GPT-4 VS GPT-3.5 的A/B──主要指标是什么?
4. 你的鱼通过了,但A/B显示了 -1.2%的转换.你发货吗?写下升级标准.
   中文翻译:你的金丝雀通过但A/B 显示 -1.2% 转换率──你上线吗?写出解释──
5. 应对前期使用CUPED,以60%的差距.计算有效样本大小增长.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Eval | "offline test" | Labeled-set evaluation of model capability |
| A/B test | "experiment" | Live randomized comparison on users |
| CUPED | "variance reduction" | Pre-period regression to reduce variance |
| Sequential test | "peek-ok test" | Always-valid procedure allowing early stop |
| Multiple comparison | "the family error" | Running many tests inflates false positives |
| Bonferroni | "tight correction" | Divide α by number of tests |
| Benjamini-Hochberg | "BH FDR" | False-discovery-rate control, less conservative |
| SRM | "bad split" | Sample ratio mismatch; assignment bug |
| Statsig | "OpenAI owned" | Commercial all-in-one, acquired 2025 |
| GrowthBook | "the OSS one" | MIT warehouse-native platform |
| mSPRT | "sequential probability ratio test" | Classical sequential procedure |

## 继续阅读 继续阅读

- [GrowthBook — How to A/B Test AI](https://blog.growthbook.io/how-to-a-b-test-ai-a-practical-guide/)
- [Statsig — Beyond Prompts: Data-Driven LLM Optimization](https://www.statsig.com/blog/llm-optimization-online-experimentation)
- [Statsig vs GrowthBook comparison](https://www.statsig.com/perspectives/ab-testing-feature-flags-comparison-tools)
- [Deng et al. — CUPED](https://www.exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf)
- [Howard — Confidence Sequences](https://arxiv.org/abs/1810.08240)
