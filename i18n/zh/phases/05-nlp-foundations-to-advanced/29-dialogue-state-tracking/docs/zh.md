# 对话状态跟踪

> "我想要一个北方的廉价餐厅... 让它适度... 加入意大利语". 三轮,三次状态更新.
> "我要北边一家便宜的餐厅......改成中等价位......加意大利菜――" 三轮对话,三次状态更新――DST 保持槽位-值字典同步,让预订成功――

> **【中文解读】**随着对话中的状态变化,确保多轮对话一致.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 17 (Chatbots), Phase 5 · 07 (POS & Parsing) | **前置知识:** Phase 5 · 17（聊天机器人），Phase 5 · 07（POS 与解析）
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

系统会预订错误的餐厅,收费错误的卡或安排错误的日期. DST是感觉像数据库查询和感觉像对话的聊天机器人之间的区别.

> 一个槽位搞错,系统就预订错餐厅、扣错卡或排错日期――DST是让聊天机器人感觉像数据库查询还是像对话区别――

> **【中文解读】**本节提出的问题是:如何正确理解和应用这一技术在实际工程中.

尽管在2026年还重要,但在2026年仍然有重要意义:尽管在2026年还存在重要意义,但在复杂的多槽更新中,LLC仍然无法实现复杂的更新,修正次 ("等,让它成为第7个,而不是第8个,并将时间更改为下午3点"),以及长时间的会议中持续状态.明确的DST仍然是任务导向系统的生产答案.

> 2026年为什么仍然重要:LLM 隐式处理简单状态但在复杂多槽更新,纠正级联"等等,改成7号不是8号,时间改成下午3点") 和长会话的持久状态失败了――显然DST 仍然是任务导向系统的生产答案――

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.

**Dialogue state.**一组 (插槽,值) 对,捕获系统在每个转折时知道用户目标的信息.

> **对话状态。**每轮对话中一组 (槽位, 值) 对,捕获系统对用户目标的理解──例如:{厨房:意大利菜,价格:中等,区域:北方}──

**State update.**在每次更新时,根据用户的新发言更新状态.

> **状态更新。**每轮对话根据新用户话语更新状态.

**Belief state.**对于可能的插槽值来说,概率分布. 当用户不清楚时有用 ("餐厅" →厨房=没有,但相信意大利=0.3,中国=0.2,...).

> **信念状态。**可能槽位值的概率分布──当用户模糊时有用量("一家餐厅" →厨房=没有,但信仰显示意大利=0.3、中国=0.2、......) ⋅

> **【拓展：大语言模型的工程实践】**通过GPT到ChatGPT,NLP 领域经历了范式转变.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构.
```figure
n5-slot-tracker
```

## 建立它

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.

## 建立它,实现它.

> **【中文解读】**本节通过代码从零实现核心算法.

### 步骤1:插槽值状态跟踪器

```python
class DialogueStateTracker:
    def __init__(self, slots):
        self.state = {slot: None for slot in slots}
        self.history = []

    def update(self, slot_values):
        for slot, value in slot_values.items():
            if slot in self.state:
                self.state[slot] = value
        self.history.append(dict(self.state))

    def get_missing_slots(self):
        return [s for s, v in self.state.items() if v is None]

    def is_complete(self):
        return all(v is not None for v in self.state.values())


tracker = DialogueStateTracker(["cuisine", "price", "area", "party_size"])
tracker.update({"cuisine": "Italian", "area": "north"})
print(tracker.get_missing_slots())  # ['price', 'party_size']
print(tracker.is_complete())  # False
```

### 步骤2:基于LLM的状态更新

```python
def llm_state_update(dialogue_history, current_state, llm):
    prompt = f"""Given the dialogue history and current state, extract slot updates.

Current state: {current_state}
Dialogue: {dialogue_history[-1]}

Output JSON of updated slots."""
    return llm(prompt)
```

> **【中文解读】**本节展示了如何使用成熟框架快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能.

## 用它实现框架

> **【中文解读】**本节关注如何将模型部署为可用产品.

- **Rule-based DST.**快速,可预测. / 基于规则的DST──正则+实体提取──快速、可预测──
- **Neural DST.**训练在多WOZ或类似的数据集. 更好的通用化. / 神经 DST──在多WOZ 上训练──更好泛化──
- **LLM-based DST.**根据法学学学的DST──灵活──昂贵──
- **Hybrid.**取的LLM + 基于规则的验证. 生产建议. / 混合──LLM 提取 + 规则验证──生产推──

## 运送它.

保存如`outputs/skill-dst-builder.md`其他:

> 保存为`outputs/skill-dst-builder.md`其他:

```markdown
Given a task-oriented dialogue system, design DST.
1. Slots to track.
2. State update method (rule, neural, LLM).
3. Confirmation and correction handling.
```

## 练习题

1. **Easy.**建立一个基于规则的餐厅预订系统.**简单。**为餐厅预订系统建立基于规则的DST.
2. **Medium.**加入基于LLM的状态提取. 进行规则的比较. / **中等。**添加基于LLM的状态提取.
3. **Hard.**评估多WOZ的DST. 报告共同目标准确性. / **困难。**在多WOZ上评估DST──

## 关键词 快速查找表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Dialogue state（对话状态） | Current (slot, value) pairs. / 当前槽位-值对。 |
| Slot filling（槽位填充） | Extracting values for predefined slots. / 为预定义槽位提取值。 |
| Belief state（信念状态） | Probability distribution over slot values. / 槽位值的概率分布。 |
| MultiWOZ | Multi-domain dialogue dataset. / 多领域对话数据集。 |

## 继续阅读 继续阅读

- [MultiWOZ](https://arxiv.org/abs/1810.00278)标准DST数据集. / 标准DST 数据集──
- [TRADE](https://arxiv.org/abs/1810.00278)可转移对话状态跟踪器. / 可迁移对话状态跟踪器──
- [SimpleTOD](https://arxiv.org/abs/2005.00796)简单端到端 DST──
