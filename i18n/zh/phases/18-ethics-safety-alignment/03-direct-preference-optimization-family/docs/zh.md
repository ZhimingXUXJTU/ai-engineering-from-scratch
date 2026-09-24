# 直接偏好优化家庭

> 拉斐洛夫等人 根据RLHF的优势在偏好数据方面具有封闭形式,因此您可以跳过明确的奖励模式并直接优化政策. 这种洞察力产生了一家IPO,KTO,SimPO,ORPO,BPO,每个都解决了DPO失败模式. 2026年,直线配列算法将比PPO更多的边境训练后运行. 但第二课的过度优化曲线仍然适用:DAA不逃离Goodhart,

> **【中文解读】**本节介绍了直接偏好优化 (DPO) 家庭绕奖励模型直接从偏好数据训练的RLHF 替代方案.

> **【拓展：DPO 家族 → 现代 AI 训练】**2026年,直接对齐算法 (DAA) 进行了更多前沿后训练中部署比PPO.但第二课的过度优化曲线仍然适用.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, six-variant preference-loss comparator) | **语言:** Python（标准库，六种变体偏好损失比较器）
**Prerequisites:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (Reward hacking), Phase 10 · 08 (DPO basics) | **前置知识:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (奖励黑客), Phase 10 · 08 (DPO 基础)

>  **【前置】**学本节前请先掌握:阶段18·01-02(InstructGPT+古德哈特) 、阶段10·08(DPO基础) ――DPO 家族 = 绕过明显奖励模型直接从偏好数据训练――
>  **【类比】**竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果: 竞赛的结果:
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 取出DPO封闭形式从RLHF-with-KL最佳.
  中文翻译:从带 KL 的 RLHF 最优解推导 DPO 闭式解。
- 说明IPO,KTO,SimPO,ORPO,BPO的每个故障模式.
  中文翻译:说明IPO、KTO、SimPO、ORPO、BPO 分别修复了DPO的哪个失败模式――
- 区分"隐含的奖励差距"与"偏好强度",并解释为什么IPO的身份映射是重要的.
  中文翻译:区分"隐式奖励差距"和"偏好强度",解释为什么IPO的恒等映射很重要.
- 解释为什么Rafailov等人 (NeurIPS 2024) 证明尽管没有明确的RM,但DAA过度优化.
  中文翻译:解释为什么拉斐洛夫等(NeurIPS 2024)证明DAA 尽管没有显而易见的RM 仍然会过度优化。

## 问题 问题引入

关于RLHF的目标 (课 1)

> 目标:

```
max_pi E_{x,y~pi} [ r(x, y) ] - beta * KL(pi || pi_ref)
```

已知最佳值:

> 有所知最优解:

```
pi*(y|x) = (1/Z(x)) * pi_ref(y|x) * exp(r(x, y) / beta)
```

因此,奖励被隐含地定义为最佳政策与参考的比例:

> 因此,奖励率由最佳策略与参考策略定义为:

```
r(x, y) = beta * log(pi*(y|x) / pi_ref(y|x)) + beta * log Z(x)
```

取代这个为布拉德利-特里偏好概率和分区函数`Z(x)`取消,因为它只取决于`x`只有政策参数的损失 没有奖励模型需要.

> 为了把它变成布拉德利-特利的分数函数`Z(x)`由于依赖`x`而抵消. 剩下的只是纯策略参数的损失函数.

纹:衍生假设最佳可达,偏好数据是分布式的,参考政策是真实模式.这些都不完全适用.每个家庭成员都会修复不同的违反假设.

> 问题在于:推导假设最优可达,偏好数据分布内,参考策略是真正的点.

## 概念的核心概念

> **【中文解读】**推PO的推:RLF 目标有已知最优解 pi*((DH 于x) = (1((x)) * pi_ref(y 于x) * exp((r(x,y) /beta) 将奖励表示最佳策略与参考策略比率对数,代入布拉德利-特里 偏好,配分函数 Z(x) 因为仅依赖于x而抵消剩余的只是纯策略参数的损失函数,无需奖励模型――但推假设最优可达、偏好数据分布、内参考策略是真正点这些假设在实践中都不完全成立.

### 果 (Rafailov等, 2023)

```
L_DPO = -log sigmoid(
  beta * log(pi(y_w | x) / pi_ref(y_w | x))
  - beta * log(pi(y_l | x) / pi_ref(y_l | x))
)
```

什么可能会发生错误:

> 问题可能是什么?

- 隐含的奖励差距`beta * (log(pi/pi_ref)_w - log(pi/pi_ref)_l)`只有一个小的偏好,就会产生一个任意大的差距.
  中文翻译:隐式奖励差距无限――微小偏好可以产生任意大的差距――
- 输出驱动选择和拒绝的日志探测器在相反的方向.只要拒绝的日志探测器更快地下降,它可以推倒所选的绝对日志探测器.这是降级的选择反应现象.
  中文翻译:损失驱动选择和拒绝对数概率朝相反方向. 只要拒绝的下降更快,它可以推低选择的绝对对数概率.
- 分布外偏好 (罕见罕见对与罕见罕见对) 产生了任意的隐含奖励.
  中文翻译:分布外偏好产生任意隐式奖励.

> **【拓展：IPO → DPO 的边界控制】**通过恒等映射取代日志-标志,偏好差距被1/(2*beta) 封顶.

### 投资者:

身份偏好优化取代了日志-sigmoid 通过身份映射在偏好概率.损失成为一个有限的目标的二方误差:

> 通过恒等映射替换日志-sigmoid,偏好差距被1/(2*beta) 封顶.

```
L_IPO = (log(pi(y_w | x) / pi_ref(y_w | x)) - log(pi(y_l | x) / pi_ref(y_l | x)) - 1/(2 beta))^2
```

边缘由`1/(2 beta)`偏好强度和隐含奖励差距均为比例.

> 边界被被`1/(2 beta)`封顶――偏好强度和隐式奖励差距成正比――不会爆炸――

> **【拓展：KTO → 无配对数据训练】**卡内曼-特弗斯基优化) 的关键创新是完全放弃配对结构,只需要单个标记为"理想"或"不理想"的输出.

### 技术技术技术 (Ethayarajh等,2024年)

由于单个标记输出和二进制"可"或"不可"信号,它将映射到一个前景理论实用性:

>  KTO 完全放弃配对结构. 给定单个标记输出和二元"理想"或"不理想"信号,它映射到前景理论效果:

```
v(x, y) = sigma(beta * log(pi(y|x) / pi_ref(y|x)) - z_ref)
```

优势:可以使用未配对数据,这更丰富.

> 对于收益和损失使用权力不同.

> **【中文解读】**简单的方法是通过长度归化对数似然的替代,加上边际马稳定训练. 这直接解决了DPO的长度偏见失败模式长的 y_w 构造性产生更大的对数概率差距. ORPO 更激进:将偏好项增加到标准SFT的 NLL 损失,单阶段从失基础模型训练到齐模型. BPO 则识别了"退化选择反应"问题.

### 博 (Meng等, 2024)

简单的偏好优化将训练信号与生成进行一致化. 完全删除参考政策,并根据长度正常化日志概率:

> 简单的训练信号与生成对齐.

```
L_SimPO = -log sigmoid(
  (beta / |y_w|) * log pi(y_w | x)
  - (beta / |y_l|) * log pi(y_l | x)
  - gamma
)
```

具有一个边缘`gamma`长度正常化消除了利用DPO的长度偏差失败模式的激励 (更长时间`y_w`根据建筑物,它提供了更大的日志检测差距.

> 边际`gamma`稳定训练――长度归结消除了利用长度偏见失败模式的激励`y_w`构造性地产生较大的对数概率差距)

### 欧罗波 (Hong等, 2024)

优化偏好率增加一个偏好术语,

> 欧罗波将偏好项加到标准的 SFT 负对数似之上:

```
L_ORPO = L_NLL(y_w) + lambda * L_OR
L_OR = -log sigmoid(log(odds(y_w) / odds(y_l)))
```

没有参考政策 SFT术语是调节剂.从基模型到对齐模型的单一阶段训练.没有单独的SFT检查点.

> 无参考策略SFT项就是正则化器――单阶段从基础模型训练到对齐模型――无需单独的SFT检查点――

### 报告的内容:

确定级选择答案问题:DPO保留排名`y_w > y_l`但绝对的记录测试`y_w`报告在Llama-3.1-8B-Instruct上对数学推理而言.

>  BPO 识别了"退化选择响应"问题:DPO 保持`y_w > y_l`排序但`y_w`报告在Llama-3.1-8B-Instruct 数学推理上显示,比DPO提升了10.1%的准确率.

> **【拓展：DAA 过度优化 → 通用防御】**拉斐洛夫等(NeurIPS 2024) 在多个数据集和KL 预算上训练DPO、IPO、SLiC 策略──真实奖励与KL的曲线呈现出与高等相同的前进后降形状──DAA的隐藏奖励在训练期间查询分布外样本,KL 正则化无法稳定这一点──通用修复更好的数据、集成、早停对PPO和DPO家族同样适用──

### 普遍结果:DAA仍然过度优化

拉斐洛夫等人"直接调整算法中奖励模型过度优化的扩展法则" (NeurIPS 2024) 与DPO,IPO,SLiC在KL预算中多个数据集上培训政策.金-奖励-KL曲线具有相同的Gao等.峰值和崩形状.暗示奖励在培训期间询问出分布样本;KL规范化并没有稳定这一点.

> 拉斐洛夫等在多个数据集和KL 预算中训练了DPO、IPO、SLiC 策略──真实奖励与KL的曲线呈现出与高等相同的前进后降形状──DAA的隐藏奖励在训练期间查询分布外样本,KL 正常无法稳定这一点──

报价分析系统 (DAA) 没有逃离Goodhart.它们从"奖励模型过度优化"到"参考政策比率过度优化"的表面变化.

> 它们只是将表面的攻击从"奖励模型过度优化"转化为"参考策略比率过度优化"......通用修复更好的数据,集成,早停对这两者都适用.

> **【中文解读】**2026年方法选择指南:有大量配对偏好数据 → DPO(保守beta) 或 SimPO(如有长度偏见);有非配对二元反 → KTO;想要单阶段管线 → ORPO;DPO 日志显示选择概率下降 → BPO;偏好强度变化大且 DPO 和 → IPO──每个实验室在所有方法上运行再按任务选择优数学推理和安全的最佳方法可能不同.

### 选择他们中的 (2026)

- 如果您有大量的对取决数据:DPO与保守的beta,SimPO如果长度偏差明显.
  中文翻译:有大量配对偏好数据 → DPO(保守beta),如有长度偏见使用 SimPO。
- 如果您有双重反:KTO.
  中文翻译:有非配对二元反 → KTO。
- 如果您想要从基模型中获得单阶段管道:ORPO.
  中文翻译:想要从基础模型的单阶段管线 → ORPO。
- 如果您看到DPO日志中被选择的记录检查器,
  中文翻译:DPO 日志中看选择概率下降 → BPO。
- 如果偏好强度很大,且DPO和:IPO.
  中文翻译:偏好强度变化大且DPO 和 →IPO。

每个实验室都用电池运行五个任务,每项任务都会选择胜利者.

> 每个实验室都在所有方法上运行完善的任务选择优.

> **【拓展：DPO 家族实践 → 方法选择】**2026年每一个前沿实验室在所有方法上都运行完毕再按任务选优.没有理由认为数学推理和安全的最佳方法是相同的.

## 用它实现框架
```figure
dpo-margin
```

## 用它

`code/main.py`根据玩具偏好数据集,对比六次损失 (DPO,IPO,KTO,SimPO,ORPO,BPO) 进行了比较.每次损失都以小的软最大政策优化于相同的500对样本.每种方法的最终胜率,选项日志-试验漂移和隐含奖励差距.

> `code/main.py`在偏好强度变化的玩具数据集中,比较六种损失:DPO,IPO,KTO,SimPO,ORPO,BPO) .每种损失在相同的500个样本上使用小型软max策略优化.

## 运送它.

这一课产生了`outputs/skill-preference-loss-selector.md`鉴于数据集统计数据 (对对对对对对对对对对对对对变量对均偏好强度,长度分布) 和目标 (单阶段或SFT-then-preference),建议对偏好损失进行报告,并报告它保护的故障模式.

> 本课产出发 `outputs/skill-preference-loss-selector.md`△给定数据集统计 (配对与非配对,可变与均偏好强度,长度分布) 和目标 (单阶段或SFT后偏好),推偏好损失并报告保护的失败模式.

## 练习题

1. 跑步`code/main.py`报告DPO和BPO的最后选择日志检查下降.BPO应该保持更高的选择绝对概率验证这一点.
   中文翻译:运行 `code/main.py`报告 DPO 和 BPO 的最终选择对数率概率下降.

2. 修改偏好数据,使所有对具有相同的强度. 在六种方法中,哪种方法最强大?哪种降低?
   中文翻译:修改偏好数据使所有配对强度相等.

3. 没有改变任何其他东西,数字显示DPO的长度利用和SIMPO的修正.
   中文翻译:使拒绝响应平均比选择响应长2倍――不改变其他东西,数值显示DPO的长度利用和SimpO的修复――

4. 拉斐洛夫等人 (NeurIPS 2024) 声称DAA过度优化. 复制一个点版本:图 chosen-minus-rejected KL divergence,并观察大型beta中的DPO过度优化.
   中文翻译:拉斐洛夫等(NeurIPS 2024) 声称DAA过度优化──复现单点版本:绘制选择减拒的 KL 散度,观察 DPO 在大beta 时的过度优化──

5. 阅读BPO论文摘要 (OpenReview b97EwMUWu7). 写下BPO在DPO添加的一行纠正. 确认在`code/main.py`现在,我们要去.
   中文翻译:阅读BPO论文摘要(OpenReview b97EwMUWu7) 』写下BPO对DPO 添加单行修正──对照`code/main.py`中实现确认.

## 关键词 关键词

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| DPO | "RLHF without a reward model" / "没有奖励模型的 RLHF" | Loss derived from the closed-form RLHF optimum; policy parameters only / 从闭式 RLHF 最优解推导的损失；仅策略参数 |
| Implicit reward | "the log-ratio" / "对数比率" | `beta * log(pi(y\|x) / pi_ref(y\|x))` — the DPO-implied reward / DPO 隐含的奖励 |
| IPO | "bounded DPO" / "有界 DPO" | Replaces log-sigmoid with identity; implicit reward gap capped by `1/(2 beta)` / 用恒等映射替换 log-sigmoid；隐式奖励差距被 `1/(2 beta)` 封顶 |
| KTO | "unpaired DPO" / "非配对 DPO" | Prospect-theory utility over single labels with loss aversion / 带损失厌恶的单标签前景理论效用 |
| SimPO | "reference-free DPO" / "无参考 DPO" | Length-normalized log-likelihood + margin; no reference policy / 长度归一化对数似然 + 边际；无参考策略 |
| ORPO | "one-stage DPO" / "单阶段 DPO" | NLL + odds-ratio preference term; trains from base model in one pass / NLL + 胜率比偏好项；单阶段从基础模型训练 |
| BPO | "chosen-preserving DPO" / "保留选择的 DPO" | DPO plus a penalty for decreasing the chosen response's absolute log-prob / DPO 加上降低选择响应绝对对数概率的惩罚 |
| Degraded Chosen | "chosen goes down" / "选择概率下降" | DPO decreases chosen log-prob so long as rejected falls faster / DPO 降低选择对数概率只要拒绝下降更快 |
| DAA | "direct alignment algorithm" / "直接对齐算法" | Any preference-loss method that skips an explicit RM / 任何跳过显式 RM 的偏好损失方法 |

## 继续阅读 继续阅读

- [Rafailov et al. — Direct Preference Optimization (NeurIPS 2023, arXiv:2305.18290)](https://arxiv.org/abs/2305.18290)
  中文翻译:拉菲洛夫等DPO 原始论文
- [Azar et al. — A General Theoretical Paradigm to Understand Learning from Human Preferences (AISTATS 2024, arXiv:2310.12036)](https://arxiv.org/abs/2310.12036)IPO
  中文翻译:Azar 等人IPO论文
- [Ethayarajh et al. — KTO: Model Alignment as Prospect Theoretic Optimization (arXiv:2402.01306)](https://arxiv.org/abs/2402.01306)
  中文翻译:Ethayarajh 等人KTO 论文
- [Meng, Xia, Chen — SimPO (NeurIPS 2024, arXiv:2405.14734)](https://arxiv.org/abs/2405.14734)
  中文翻译:孟等 辛普论文
- [Hong, Lee, Thorne — ORPO (EMNLP 2024, arXiv:2403.07691)](https://arxiv.org/abs/2403.07691)
  中文翻译:香港等ORPO论文
- [BPO — Behavior Preservation Optimization (ICLR 2026 OpenReview b97EwMUWu7)](https://openreview.net/forum?id=b97EwMUWu7)
  中文翻译:BPO行为保持优化
- [Rafailov et al. — Scaling Laws for RM Overoptimization in DAAs (NeurIPS 2024, arXiv:2406.02900)](https://arxiv.org/abs/2406.02900)
  中文翻译:拉斐洛夫等人DAA 过度优化缩放定律
