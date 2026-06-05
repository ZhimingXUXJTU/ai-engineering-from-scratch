# Dialogue State Tracking | 对话状态跟踪

> "I want a cheap restaurant in the north... actually make it moderate... and add Italian." Three turns, three state updates. DST keeps the slot-value dict in sync so the booking works.
> "我要北边一家便宜的餐厅……改成中等价位……加意大利菜。" 三轮对话，三次状态更新。DST 保持槽位-值字典同步，让预订成功。

> **【中文解读】** 跟踪对话中的状态变化（槽位-值对），确保多轮对话一致。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 17 (Chatbots), Phase 5 · 07 (POS & Parsing) | **前置知识:** Phase 5 · 17（聊天机器人），Phase 5 · 07（POS 与解析）
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

Get a single slot wrong and the system books the wrong restaurant, charges the wrong card, or schedules the wrong date. DST is the difference between a chatbot that feels like a database query and one that feels like a conversation.

> 一个槽位搞错，系统就预订错餐厅、扣错卡或排错日期。DST 是让聊天机器人感觉像数据库查询还是像对话的区别。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。

Why it still matters in 2026 despite LLMs: LLMs handle simple state implicitly but fail on complex multi-slot updates, correction cascades ("wait, make it the 7th not the 8th, and change the time to 3pm"), and persistent state across long sessions. Explicit DST is still the production answer for task-oriented systems.

> 2026 年为什么仍然重要：LLM 隐式处理简单状态但在复杂多槽更新、纠正级联（"等等，改成 7 号不是 8 号，时间改成下午 3 点"）和长会话的持久状态上失败。显式 DST 仍是任务导向系统的生产答案。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。

**Dialogue state.** A set of (slot, value) pairs that captures what the system knows about the user's goal at each turn. Example: {cuisine: Italian, price: moderate, area: north}.

> **对话状态。** 每轮对话中一组 (槽位, 值) 对，捕获系统对用户目标的理解。例如：{cuisine: Italian, price: moderate, area: north}。

**State update.** At each turn, update the state based on the new user utterance. Three operations: set, update, delete.

> **状态更新。** 每轮对话根据新的用户话语更新状态。三种操作：设置、更新、删除。

**Belief state.** Probability distribution over possible slot values. Useful when the user is ambiguous ("a restaurant" → cuisine=None, but belief shows Italian=0.3, Chinese=0.2, ...).

> **信念状态。** 可能槽位值的概率分布。当用户模糊时有用量（"一家餐厅" → cuisine=None，但信念显示 Italian=0.3、Chinese=0.2、……）。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了范式转变。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。

### Step 1: slot-value state tracker

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

### Step 2: LLM-based state update

```python
def llm_state_update(dialogue_history, current_state, llm):
    prompt = f"""Given the dialogue history and current state, extract slot updates.

Current state: {current_state}
Dialogue: {dialogue_history[-1]}

Output JSON of updated slots."""
    return llm(prompt)
```

> **【中文解读】** 本节展示如何用成熟框架快速应用该技术。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。

## Use It | 用框架实现

> **【中文解读】** 本节关注如何将模型部署为可用的产品。

- **Rule-based DST.** Slot filling with regex + entity extraction. Fast, predictable. / 基于规则的 DST。正则 + 实体提取。快速、可预测。
- **Neural DST.** Train on MultiWOZ or similar dataset. Better generalization. / 神经 DST。在 MultiWOZ 上训练。更好泛化。
- **LLM-based DST.** Prompt the LLM to extract state updates. Flexible, expensive. / 基于 LLM 的 DST。灵活、昂贵。
- **Hybrid.** LLM for extraction + rule-based for validation. Production recommendation. / 混合。LLM 提取 + 规则验证。生产推荐。

## Ship It | 产出物

Save as `outputs/skill-dst-builder.md`:

> 保存为 `outputs/skill-dst-builder.md`：

```markdown
Given a task-oriented dialogue system, design DST.
1. Slots to track.
2. State update method (rule, neural, LLM).
3. Confirmation and correction handling.
```

## Exercises | 练习题

1. **Easy.** Build a rule-based DST for a restaurant booking system. / **简单。** 为餐厅预订系统构建基于规则的 DST。
2. **Medium.** Add LLM-based state extraction. Compare to rule-based. / **中等。** 添加基于 LLM 的状态提取。
3. **Hard.** Evaluate DST on MultiWOZ. Report joint goal accuracy. / **困难。** 在 MultiWOZ 上评估 DST。

## Key Terms | 术语速查表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Dialogue state（对话状态） | Current (slot, value) pairs. / 当前槽位-值对。 |
| Slot filling（槽位填充） | Extracting values for predefined slots. / 为预定义槽位提取值。 |
| Belief state（信念状态） | Probability distribution over slot values. / 槽位值的概率分布。 |
| MultiWOZ | Multi-domain dialogue dataset. / 多领域对话数据集。 |

## Further Reading | 延伸阅读

- [MultiWOZ](https://arxiv.org/abs/1810.00278) — standard DST dataset. / 标准 DST 数据集。
- [TRADE](https://arxiv.org/abs/1810.00278) — transferable dialogue state tracker. / 可迁移对话状态跟踪器。
- [SimpleTOD](https://arxiv.org/abs/2005.00796) — simple end-to-end DST. / 简单端到端 DST。
