# Fairness Criteria — Group, Individual, Counterfactual | 反事实 公平 准则

> Three families structure the fairness literature. Group fairness: demographic parity, equalized odds, conditional use accuracy equality — equal rates across protected groups on average. Individual fairness (Dwork et al. 2012): similar individuals receive similar decisions; Lipschitz condition on the decision map. Counterfactual fairness (Kusner et al. 2017): a decision is fair to an individual if it is unchanged when sensitive attributes are counterfactually altered. 2024 theoretical result (NeurIPS 2024): there is an inherent CF-vs-accuracy trade-off; a model-agnostic method converts an optimal-but-unfair predictor into a CF one with bounded accuracy loss. Backtracking counterfactuals (arXiv:2401.13935, January 2024): new paradigm that avoids requiring interventions on legally protected attributes. Philosophical reconciliation (ICLR Blogposts 2024): with causal graphs, satisfying certain group fairness measures entails counterfactual fairness.

> **【中文解读】** 本节介绍了公平性准则——群体公平、个体公平和反事实公平的定义和度量。三个家族给出结构不同的标准——一个模型可以群体公平但个体不公平，反事实公平但群体不公平。选择标准是政策决定，没有标准是普遍最优的。

> **【拓展：不可能定理 → 公平性冲突】** Chouldechova / Kleinberg-Mullainathan-Raghavan（2017）不可能定理：人口平权、均等化赔率和条件使用准确率均等在不平等基础率下不能同时满足。这是一个数学结果，不是工程限制——任何涉及不平等群体的系统都必须选择牺牲哪个公平标准。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-criteria comparison) | **语言:** Python（标准库，三标准比较）
**Prerequisites:** Phase 18 · 20 (bias), Phase 02 (classical ML) | **前置知识:** Phase 18 · 20 (偏见), Phase 02 (经典 ML)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Learning Objectives | 学习目标

- State the three group-fairness criteria (demographic parity, equalized odds, conditional use accuracy equality) and one impossibility result.

> 说明三个群体公平标准（人口平权、均等化赔率、条件使用准确率均等）和一个不可能结果。

- Describe individual fairness via the Dwork et al. 2012 Lipschitz formulation.

> 描述通过 Dwork 等人 2012 年 Lipschitz 公式定义的个体公平。

- Describe counterfactual fairness and its causal-graph dependency.

> 描述反事实公平及其因果图依赖。

- Explain backtracking counterfactuals and why they sidestep the intervention-on-protected-attribute problem.

> 解释回溯反事实以及为什么它们避开了在受保护属性上干预的问题。

## The Problem | 问题

Lesson 20 was about measuring bias. Lesson 21 is about defining the fairness standard the measurement should serve. The three families give structurally different standards — a model can be group-fair and individual-unfair, counterfactually fair and group-unfair. Choosing a standard is a policy decision; no standard is universally optimal.

> Lesson 20 是关于测量偏见。Lesson 21 是关于定义测量应服务的公平标准。三个家族给出结构不同的标准——选择标准是政策决定，没有标准是普遍最优的。

## The Concept | 概念

> **【中文解读】** 群体公平三大标准：人口平权——P(Y=1|A=a) = P(Y=1|A=a')，各组接受率相等；均等化赔率——P(Y=1|Y*=y,A=a) = P(Y=1|Y*=y,A=a')，各组真阳性率和假阳性率相等；条件使用准确率均等——P(Y*=y|Y=y,A=a) = P(Y*=y|Y=y,A=a')，各组预测值相等。

### Group fairness

- **Demographic parity.** P(Y=1 | A=a) = P(Y=1 | A=a') for all groups. Equal acceptance rates.
- **Equalized odds.** P(Y=1 | Y*=y, A=a) = P(Y=1 | Y*=y, A=a'). Equal TPR and FPR across groups.
- **Conditional use accuracy equality.** P(Y*=y | Y=y, A=a) = P(Y*=y | Y=y, A=a'). Equal predictive value across groups.

> 人口平权——各组接受率相等；均等化赔率——各组真阳性率和假阳性率相等；条件使用准确率均等——各组预测值相等。

Impossibility (Chouldechova, Kleinberg-Mullainathan-Raghavan 2017): these three cannot be satisfied simultaneously under unequal base rates.

> 不可能定理：在不平等基础率下这三个不能同时满足。

### Individual fairness

Dwork et al. 2012. A decision map f is individually fair with respect to a task-specific similarity metric d if |f(x) - f(x')| <= L * d(x, x') for some Lipschitz constant L. Similar individuals get similar decisions.

> Dwork 等人 2012。决策映射 f 如果对某个 Lipschitz 常数 L 满足 |f(x) - f(x')| <= L * d(x, x')，则对任务特定相似度度量 d 是个体公平的。相似个体得到相似决策。

Requires defining d. Policy question, not statistical.

> 需要定义 d。这是政策问题，不是统计问题。

> **【拓展：反事实公平 → 因果图依赖】** Kusner 等人（2017）的反事实公平：在因果模型下，如果将个体敏感属性反事实改变后决策不变，则该决策对该个体是公平的。这需要因果 DAG——DAG 是建模选择，反事实公平的合理性取决于 DAG 的合理性。2024 年的回溯反事实（arXiv:2401.13935）避免了在法律保护属性上进行干预的困境——不是从属性干预，而是从结果反向推理。

### Counterfactual fairness

Kusner et al. 2017. A decision is counterfactually fair to individual i if, under a causal model of the population, the decision is unchanged when i's sensitive attributes are counterfactually altered.

> Kusner 等人 2017。在因果模型下，如果将个体敏感属性反事实改变后决策不变，则该决策对该个体是反事实公平的。

Requires a causal DAG. The DAG is a modeling choice. Counterfactual fairness is only as justified as the DAG.

> 需要因果 DAG。DAG 是建模选择。反事实公平的合理性取决于 DAG 的合理性。

### The CF-vs-accuracy trade-off

NeurIPS 2024 theoretical: there is an inherent trade-off between counterfactual fairness and predictive accuracy. A model-agnostic method can convert an optimal-but-unfair predictor into a CF one, at a bounded accuracy cost. The accuracy cost depends on the magnitude of the sensitive-attribute coefficient in the optimal unfair predictor.

> NeurIPS 2024 理论结果：反事实公平和预测准确性之间存在固有权衡。模型不可知方法可以将最优但不公平的预测器转换为 CF 公平的，但准确度损失有界。

### Backtracking counterfactuals

arXiv:2401.13935 (January 2024). Traditional counterfactuals require interventions on the sensitive attribute — "would the decision change if this person had been a different gender." Legally, this is problematic: protected attributes cannot be intervened on in classification law.

> 传统反事实需要在敏感属性上干预——法律上这有问题。回溯反事实翻转方向：不是从属性干预，而是从结果反向推理。这避开了法律异议。

Backtracking counterfactuals flip the direction: instead of intervening on the attribute, ask what combination of the individual's actual features would have produced the counterfactual outcome. This sidesteps the legal objection.

> 回溯反事实不是干预属性，而是询问个体实际特征的什么组合会产生反事实结果。

> **【中文解读】** 哲学调和（ICLR Blogposts 2024）：有了因果图后，满足某些群体公平度量就蕴含了反事实公平。三个家族不是正交的，而是相同底层因果结构的不同面向。这没有解决不可能定理（不平等基础率仍阻止同时的群体公平），但表明"群体"和"个体/反事实"之间的表面对立部分是因为没有明确因果模型造成的假象。

### Philosophical reconciliation

ICLR Blogposts 2024. With a causal graph in hand, satisfying certain group-fairness measures entails counterfactual fairness. The three families are not orthogonal; they are different facets of the same underlying causal structure.

> ICLR 2024：有了因果图后，满足某些群体公平度量就蕴含了反事实公平。三个家族不是正交的，而是相同底层因果结构的不同面向。

This does not resolve the impossibility theorems (unequal base rates still prevent simultaneous group fairness). But it shows the apparent opposition between "group" and "individual / counterfactual" is partially an artifact of not being explicit about the causal model.

> 这没有解决不可能定理，但表明"群体"和"个体/反事实"之间的表面对立部分是因为没有明确因果模型造成的假象。

### Where this fits in Phase 18

Lesson 20 is bias measurement. Lesson 21 is fairness definition. Lesson 22 is privacy (differential privacy). Lesson 23 is watermarking. These are the allocation-adjacent lessons complementing the deception-adjacent Lessons 7-11.

> Lesson 20 是偏见测量。Lesson 21 是公平定义。Lesson 22 是隐私。Lesson 23 是水印。这些是分配相关课程，补充欺骗相关课程。

> **【拓展：CF vs 准确性权衡 → 实际影响】** NeurIPS 2024 理论结果：反事实公平和预测准确性之间存在固有权衡。模型不可知论方法可以将最优但不公平的预测器转换为 CF 公平的，但准确度损失有界取决于不公平预测器中敏感属性系数的大小。这意味着选择公平标准有实际代价——更多公平意味着更少预测准确。

## Use It | 使用方法

`code/main.py` builds a toy binary-classification dataset with a sensitive attribute and unequal base rates. Compute demographic parity, equalized odds, and conditional use accuracy equality on a simple classifier. Observe the three metrics disagreeing. Apply a re-weighting for demographic parity and observe its cost on the other two.

> `code/main.py` 构建了带敏感属性和不平等基础率的玩具二分类数据集。计算三个群体公平指标，观察它们不一致。应用人口平权重加权并观察对其他两个的代价。

## Ship It | 部署上线

This lesson produces `outputs/skill-fairness-criterion.md`. Given a fairness claim or policy, identifies which criterion is being claimed, whether the model can satisfy the remaining criteria under the claimed unequal base rates, and what causal DAG the claim depends on.

> 本课产出 `outputs/skill-fairness-criterion.md`。给定公平性声明或政策，识别声称的是哪个标准、在不平等基础率下是否满足其余标准、以及声明依赖的因果 DAG。

## Exercises | 练习题

1. Run `code/main.py`. Report the three group metrics on the default data. Apply the demographic-parity-targeted re-weighting and re-report.

2. Implement the Dwork et al. 2012 individual-fairness metric using L2 on non-sensitive features. Report how many pairs violate Lipschitz with constant L=1.

3. Read Kusner et al. 2017. Construct a simple two-feature causal DAG for resume scoring and identify the counterfactual-fairness condition it implies.

4. The 2024 backtracking-counterfactuals paper avoids intervention on protected attributes. Describe a scenario where this matters for legal compliance.

5. The ICLR 2024 reconciliation argues group and counterfactual fairness are facets of the same structure. Pick two of the three criteria in `code/main.py` and state the causal assumption that would make them equivalent.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Demographic parity | "equal rates" | P(Y=1 | A=a) equal across groups |
| Equalized odds | "equal TPR/FPR" | Equal true-positive and false-positive rates across groups |
| Conditional use accuracy | "equal PPV/NPV" | Equal predictive values across groups |
| Individual fairness | "Lipschitz condition" | Similar individuals get similar decisions |
| Counterfactual fairness | "causal alteration invariance" | Decision unchanged under counterfactual attribute alteration |
| Backtracking counterfactual | "explain via actuals" | Counterfactual reasoned backward from outcome, not forward from attribute |
| Impossibility theorem | "the three conflict" | Chouldechova / KMR 2017: group criteria mutually exclusive under unequal base rates |

## Further Reading | 延伸阅读

- [Dwork et al. — Fairness through Awareness (arXiv:1104.3913)](https://arxiv.org/abs/1104.3913) — individual fairness
- [Kusner, Loftus, Russell, Silva — Counterfactual Fairness (arXiv:1703.06856)](https://arxiv.org/abs/1703.06856) — counterfactual fairness
- [Chouldechova — Fair prediction with disparate impact (arXiv:1703.00056)](https://arxiv.org/abs/1703.00056) — impossibility
- [Backtracking Counterfactuals (arXiv:2401.13935)](https://arxiv.org/abs/2401.13935) — new paradigm for protected-attribute interventions
