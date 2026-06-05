# Chatbots — Rule-Based to Neural to LLM Agents | 聊天机器人 — 规则到神经网络到 LLM Agent

> ELIZA replied with pattern matches. DialogFlow mapped intents. GPT answered from weights. Claude runs tools and verifies. Each era solved the previous one's worst failure.
> ELIZA 用模式匹配回复。DialogFlow 映射意图。GPT 从权重中回答。Claude 运行工具并验证。每个时代解决了上一个时代的最严重失败。

> **【中文解读】** 从 ELIZA 到 Seq2Seq 到 GPT Agent。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 13 (Question Answering), Phase 5 · 14 (Information Retrieval) | **前置知识:** Phase 5 · 13（问答系统），Phase 5 · 14（信息检索与搜索）
**Time:** ~75 minutes | **时间:** ~75 分钟

## The Problem | 问题引入

A user says "I want to change my flight." The system has to figure out what they want, what information is missing, how to get it, and how to complete the action. Then the user says "wait, what if I cancel instead?" and the system has to remember the context, switch tasks, and preserve state.

> 用户说 "我想改签航班。" 系统必须弄清楚他们想要什么、缺少什么信息、如何获取、如何完成操作。然后用户说 "等等，如果我要取消呢？" 系统必须记住上下文、切换任务并保持状态。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

Conversation is hard for an ML system. The input is open-ended. The output has to be coherent over many turns. The system may need to act on the world (change a flight, charge a card). Every wrong step is visible to the user.

> 对话对 ML 系统来说很难。输入是开放式的。输出必须在多轮中保持连贯。系统可能需要对世界采取行动（改签航班、扣款）。每个错误步骤对用户都是可见的。

Chatbot architectures have cycled through four paradigms, each introduced because the previous one failed too visibly. This lesson walks them in order. The 2026 production landscape is a hybrid of the last two.

> 聊天机器人架构经历了四种范式，每种都是因为前一种失败太明显而引入的。本课按顺序讲解。2026 年的生产环境是后两者的混合。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![Chatbot evolution: rule-based → retrieval → neural → agent](../assets/chatbot.svg)

**Rule-based (ELIZA, AIML, DialogFlow).** Hand-authored patterns match user input and produce responses. Intent classifiers route to predefined flows. Slot-filling state machines collect required info. Works brilliantly inside the narrow scope it was designed for. Fails immediately outside it. Still ships in safety-critical domains (banking authentication, airline booking) where hallucination is not tolerated.

> **基于规则（ELIZA、AIML、DialogFlow）。** 手写模式匹配用户输入并产生响应。意图分类器路由到预定义流程。槽位填充状态机收集所需信息。在设计的狭窄范围内表现出色。超出范围立即失败。仍在不容许幻觉的安全关键领域（银行认证、航空公司预订）中使用。

**Retrieval-based.** A FAQ-style system. Encode every pair of (utterance, response). At runtime, encode the user's message and retrieve the nearest stored response. Think Zendesk's classic "similar articles" feature. Handles paraphrases better than rules. No generation, so no hallucination.

> **基于检索。** FAQ 式系统。编码每对（话语、响应）。运行时编码用户消息并检索最近的存储响应。类似 Zendesk 的经典 "相似文章" 功能。比规则更好地处理释义。无生成，所以无幻觉。

**Neural (seq2seq).** Encoder-decoder trained on conversation logs. Generates responses from scratch. Fluent but prone to generic outputs ("I don't know") and factual drift. Never reliably on topic. The reason Google, Facebook, and Microsoft all had disappointing chatbots in 2016-2019.

> **神经（seq2seq）。** 在对话日志上训练的编码器-解码器。从零生成响应。流畅但倾向通用输出（"我不知道"）和事实漂移。从不可靠地保持主题。这就是 Google、Facebook 和 Microsoft 在 2016-2019 年都有令人失望的聊天机器人的原因。

**LLM agents.** A language model wrapped in a loop that plans, calls tools, and verifies outcomes. Not a chatbot with a long prompt. An agent loop: plan → call tool → observe result → decide next step. Retrieval-first grounding (RAG) keeps it from hallucinating. Tool calls let it actually do things. This is the 2026 architecture.

> **LLM Agent。** 包装在循环中的语言模型，规划、调用工具并验证结果。不是带长提示的聊天机器人。一个 Agent 循环：规划 → 调用工具 → 观察结果 → 决定下一步。检索优先的锚定（RAG）防止幻觉。工具调用让它实际做事。这就是 2026 年的架构。

The four paradigms are not sequential replacements. A 2026 production chatbot routes through all four: rule-based for authentication and destructive actions, retrieval for FAQ, neural generation for natural phrasing, LLM agent for ambiguous open-ended queries.

> 这四种范式不是顺序替代。2026 年生产聊天机器人通过所有四种路由：基于规则用于认证和破坏性操作，检索用于 FAQ，神经生成用于自然措辞，LLM Agent 用于模糊的开放式查询。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### Step 1: rule-based pattern matching

```python
import re


class RulePattern:
    def __init__(self, pattern, response_template):
        self.regex = re.compile(pattern, re.IGNORECASE)
        self.template = response_template


PATTERNS = [
    RulePattern(r"my name is (\w+)", "Nice to meet you, {0}."),
    RulePattern(r"i (need|want) (.+)", "Why do you {0} {1}?"),
    RulePattern(r"i feel (.+)", "Why do you feel {0}?"),
    RulePattern(r"(.*)", "Tell me more about that."),
]


def rule_based_respond(user_input):
    for pattern in PATTERNS:
        m = pattern.regex.match(user_input.strip())
        if m:
            return pattern.template.format(*m.groups())
    return "I don't understand."
```

ELIZA in 20 lines. The reflection trick ("I feel sad" → "Why do you feel sad") is the canonical psychotherapist demo from Weizenbaum 1966. Still instructive.

> 20 行 ELIZA。反射技巧（"I feel sad" → "Why do you feel sad"）是 Weizenbaum 1966 年的经典心理治疗师演示。仍然有启发意义。

### Step 2: retrieval-based (FAQ)

This illustrative snippet requires `pip install sentence-transformers` (which pulls in torch). The runnable `code/main.py` for this lesson uses a stdlib Jaccard similarity instead, so the lesson runs without external dependencies.

> 这个示例代码片段需要 `pip install sentence-transformers`（会拉取 torch）。本课的可运行 `code/main.py` 使用标准库的 Jaccard 相似度代替，这样课程无需外部依赖即可运行。

```python
from sentence_transformers import SentenceTransformer
import numpy as np


FAQ = [
    ("how do i reset my password", "Go to Settings > Security > Reset Password."),
    ("how do i cancel my order", "Go to Orders, find the order, click Cancel."),
    ("what is your return policy", "30-day returns on unused items, original packaging."),
]


encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
faq_questions = [q for q, _ in FAQ]
faq_embeddings = encoder.encode(faq_questions, normalize_embeddings=True)


def faq_respond(user_input, threshold=0.5):
    q_emb = encoder.encode([user_input], normalize_embeddings=True)[0]
    sims = faq_embeddings @ q_emb
    best = int(np.argmax(sims))
    if sims[best] < threshold:
        return None
    return FAQ[best][1]
```

Threshold-based refusal is the key design choice. If the best match is not close enough, return `None` and let the system escalate.

> 基于阈值的拒绝是关键设计选择。如果最佳匹配不够接近，返回 `None` 让系统升级处理。

### Step 3: neural generation (baseline)

Use a small instruction-tuned encoder-decoder (FLAN-T5) or a fine-tuned conversational model. Production-unusable on its own in 2026 (contradiction, off-topic drift, factual nonsense), but ships inside hybrid systems for natural phrasing. DialoGPT-style decoder-only models need explicit turn separators and EOS handling to produce coherent replies; a FLAN-T5 text2text pipeline works out of the box for a teaching example.

> 使用小型指令微调编码器-解码器（FLAN-T5）或微调的对话模型。2026 年单独使用不适合生产（矛盾、跑题、事实错误），但在混合系统中用于自然措辞。DialoGPT 风格的仅解码器模型需要显式轮次分隔符和 EOS 处理才能产生连贯回复；FLAN-T5 text2text 流水线开箱即用适合教学示例。

```python
from transformers import pipeline

chatbot = pipeline("text2text-generation", model="google/flan-t5-small")

response = chatbot("Respond politely to: Hi there!", max_new_tokens=40)
print(response[0]["generated_text"])
```

### Step 4: LLM agent loop

The 2026 production shape:

> 2026 年的生产形态：

```python
def agent_loop(user_message, tools, llm, max_steps=5):
    history = [{"role": "user", "content": user_message}]
    for _ in range(max_steps):
        response = llm(history, tools=tools)
        tool_call = response.get("tool_call")
        if tool_call:
            tool_name = tool_call.get("name")
            args = tool_call.get("arguments")
            if not isinstance(tool_name, str) or tool_name not in tools:
                history.append({"role": "assistant", "tool_call": tool_call})
                history.append({"role": "tool", "name": str(tool_name), "content": f"error: unknown tool {tool_name!r}"})
                continue
            if not isinstance(args, dict):
                history.append({"role": "assistant", "tool_call": tool_call})
                history.append({"role": "tool", "name": tool_name, "content": f"error: arguments must be a dict, got {type(args).__name__}"})
                continue
            fn = tools[tool_name]
            result = fn(**args)
            history.append({"role": "assistant", "tool_call": tool_call})
            history.append({"role": "tool", "name": tool_name, "content": result})
        else:
            return response["content"]
    return "I could not complete the task in the step budget."
```

Three things to name. Tools are callable functions the LLM can invoke. The loop terminates when the LLM returns a final answer instead of a tool call. The step budget prevents infinite loops on ambiguous tasks.

> 三个要点。工具是 LLM 可以调用的函数。当 LLM 返回最终答案而非工具调用时循环终止。步骤预算防止模糊任务上的无限循环。

Real production adds: retrieval-first grounding (inject relevant docs before each LLM call), guardrails (refuse destructive actions without confirmation), observability (log every step), and evaluations (automated checks that agent behavior stays on-spec).

> 实际生产还需：检索优先锚定（每次 LLM 调用前注入相关文档）、护栏（未经确认拒绝破坏性操作）、可观测性（记录每步）和评估（自动检查 Agent 行为保持规范）。

### Step 5: hybrid routing

```python
def hybrid_chat(user_input):
    if is_destructive_action(user_input):
        return structured_flow(user_input)

    faq_answer = faq_respond(user_input, threshold=0.6)
    if faq_answer:
        return faq_answer

    return agent_loop(user_input, tools, llm)


def is_destructive_action(text):
    danger_words = ["delete", "cancel", "charge", "refund", "transfer"]
    return any(w in text.lower() for w in danger_words)
```

The pattern: deterministic rules for anything destructive, retrieval for canned FAQs, LLM agents for everything else. This is what ships in 2026 customer-support systems.

> 模式：对任何破坏性操作使用确定性规则，对固定 FAQ 使用检索，对其他一切使用 LLM Agent。这就是 2026 年客户支持系统的做法。

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Use It | 用框架实现

The 2026 stack:

> 2026 年的技术栈：

| Use case / 使用场景 | Architecture / 架构 |
|---------|---------------|
| Booking, payment, authentication / 预订、支付、认证 | Rule-based state machines + slot filling / 基于规则的状态机 + 槽位填充 |
| Customer support FAQs / 客户支持 FAQ | Retrieval over curated answers / 对精选答案的检索 |
| Open-ended help chat / 开放式帮助聊天 | LLM agent with RAG + tool calls / 带 RAG + 工具调用的 LLM Agent |
| Internal tools / IDE assistants / 内部工具 / IDE 助手 | LLM agent with tool calls (search, read, write) / 带工具调用的 LLM Agent（搜索、读写） |
| Companion / character chatbots / 伴侣/角色聊天机器人 | Tuned LLM with persona system prompt, retrieval on knowledge / 微调 LLM 配角色系统提示和知识检索 |

Always use hybrid routing in production. No single architecture handles every request well. The routing layer itself is typically a small intent classifier.

> 在生产中始终使用混合路由。没有单一架构能处理好每种请求。路由层本身通常是一个小型意图分类器。

## Failure modes that still ship | 仍会进入生产的失败模式

- **Confident fabrication.** LLM agent claims it completed an action it did not. Mitigation: verify outcomes, log tool calls, never let the LLM claim to have done something without a successful tool return.
  **自信捏造。** LLM Agent 声称完成了未完成的操作。缓解：验证结果、记录工具调用、永远不让 LLM 在没有成功工具返回的情况下声称完成了某事。
- **Prompt injection.** User inserts text that overrides the system prompt. Ranked LLM01 in the OWASP Top 10 for LLM Applications 2025. Two flavors: direct injection (pasted into the chat) and indirect injection (hidden in documents, emails, or tool outputs the agent reads).
  **提示注入。** 用户插入覆盖系统提示的文本。在 OWASP LLM 应用 2025 Top 10 中排 LLM01。两种形式：直接注入（粘贴到聊天中）和间接注入（隐藏在文档、邮件或 Agent 读取的工具输出中）。

  Attack rates vary by scenario. Measured success rates range ~0.5-8.5% across frontier models in general tool-use and coding benchmarks. Specific high-risk setups (adaptive attacks against AI coding agents, vulnerable orchestration) have reached ~84%. Production CVEs include EchoLeak (CVE-2025-32711, CVSS 9.3) — a zero-click data-exfiltration flaw in Microsoft 365 Copilot triggered by an attacker-controlled email.
  攻击成功率因场景而异。在通用工具使用和编码基准中，前沿模型的测量成功率约 0.5-8.5%。特定高风险设置（对 AI 编码 Agent 的自适应攻击、脆弱编排）已达约 84%。生产 CVE 包括 EchoLeak（CVE-2025-32711，CVSS 9.3）—— Microsoft 365 Copilot 中的零点击数据泄露漏洞，由攻击者控制的邮件触发。

  Mitigations: treat user input as untrusted throughout the loop; sanitize before tool calls; isolate tool outputs from the main prompt; use the Plan-Verify-Execute (PVE) pattern where the agent plans first, then verifies each action against that plan before executing (this stops tool results from injecting new unplanned actions); require user confirmation for destructive actions; apply least-privilege to tool scopes.
  缓解措施：在整个循环中将用户输入视为不可信；工具调用前消毒；将工具输出与主提示隔离；使用规划-验证-执行（PVE）模式，Agent 先规划，然后对每个操作按计划验证后再执行（这阻止工具结果注入新的未计划操作）；对破坏性操作要求用户确认；对工具范围应用最小权限。

  No amount of prompt engineering fully eliminates this risk. External runtime defense layers (LLM Guard, allowlist validation, semantic anomaly detection) are required.
  无论多少提示工程都无法完全消除这个风险。需要外部运行时防御层（LLM Guard、白名单验证、语义异常检测）。
- **Scope creep.** Agent goes off-task because a tool call returned tangentially related info. Mitigation: narrow tool contracts; keep the system prompt focused; add evaluations for off-task rate.
  **范围蔓延。** Agent 因为工具调用返回了间接相关信息而跑题。缓解：缩小工具契约；保持系统提示聚焦；添加跑题率评估。
- **Infinite loops.** Agent keeps calling the same tool. Mitigation: step budget, tool-call deduplication, LLM judge on "are we making progress."
  **无限循环。** Agent 持续调用相同工具。缓解：步骤预算、工具调用去重、LLM 判断 "是否有进展"。
- **Context window exhaustion.** Long conversations push the earliest turns out of context. Mitigation: summarize older turns, retrieve relevant past turns by similarity, or use a long-context model.
  **上下文窗口耗尽。** 长对话将最早轮次推出上下文。缓解：摘要旧轮次、按相似度检索相关历史轮次、或使用长上下文模型。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## Ship It | 产出物

Save as `outputs/skill-chatbot-architect.md`:

> 保存为 `outputs/skill-chatbot-architect.md`：

```markdown
---
name: chatbot-architect
description: Design a chatbot stack for a given use case.
version: 1.0.0
phase: 5
lesson: 17
tags: [nlp, agents, chatbot]
---

Given a product context (user need, compliance constraints, available tools, data volume), output:

1. Architecture. Rule-based, retrieval, neural, LLM agent, or hybrid (specify which paths go where).
2. LLM choice if applicable. Name the model family (Claude, GPT-4, Llama-3.1, Mixtral). Match to tool-use quality and cost.
3. Grounding strategy. RAG sources, retrieval method (see lesson 14), tool contracts.
4. Evaluation plan. Task success rate, tool-call correctness, off-task rate, hallucination rate on held-out dialogs.

Refuse to recommend a pure-LLM agent for any destructive action (payments, account deletion, data modification) without a structured confirmation flow. Refuse to skip the prompt-injection audit if the agent has write access to anything.
```

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

## Exercises | 练习题

1. **Easy.** Implement the rule-based respond above with 10 patterns for a coffee-shop ordering bot. Test edge cases: double orders, modifications, cancellation, unclear intent.
   **简单。** 为咖啡店点单机器人实现上述基于规则的响应，10 个模式。测试边界情况：重复订单、修改、取消、模糊意图。
2. **Medium.** Build a hybrid FAQ + LLM fallback. 50 canned FAQ entries for a SaaS product, LLM fallback with retrieval over the docs site. Measure refusal rate and accuracy on 100 real support questions.
   **中等。** 构建混合 FAQ + LLM 回退。50 个 SaaS 产品的固定 FAQ 条目，LLM 回退带文档站检索。在 100 个真实支持问题上测量拒绝率和准确率。
3. **Hard.** Implement the agent loop above with three tools (search, read-user-data, send-email). Run an evaluation with 50 test scenarios including prompt injection attempts. Report off-task rate, failed task rate, and any injection success.
   **困难。** 用三个工具（搜索、读取用户数据、发送邮件）实现上述 Agent 循环。运行包含 50 个测试场景的评估，包括提示注入尝试。报告跑题率、失败任务率和任何注入成功。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Intent（意图） | What the user wants / 用户想要什么 | Categorical label (book_flight, reset_password). Routed to a handler. / 分类标签（book_flight、reset_password）。路由到处理器。 |
| Slot（槽位） | A piece of info / 一条信息 | Parameter the bot needs (date, destination). Slot filling is the sequence of asks. / 机器人需要的参数（日期、目的地）。槽位填充是依次询问的过程。 |
| RAG（检索增强生成） | Retrieval plus generation / 检索加生成 | Retrieve relevant docs, then ground the LLM's response. / 检索相关文档，然后锚定 LLM 的响应。 |
| Tool call（工具调用） | Function invocation / 函数调用 | LLM emits a structured call with name + args. Runtime executes, returns result. / LLM 发出带名称和参数的结构化调用。运行时执行并返回结果。 |
| Agent loop（Agent 循环） | Plan, act, verify / 规划、执行、验证 | Controller that runs LLM calls interleaved with tool calls until task complete. / 运行 LLM 调用与工具调用交错直到任务完成的控制器。 |
| Prompt injection（提示注入） | User attacks prompt / 用户攻击提示 | Malicious input that tries to override the system prompt. / 试图覆盖系统提示的恶意输入。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## Further Reading | 延伸阅读

- [Weizenbaum (1966). ELIZA — A Computer Program For the Study of Natural Language Communication](https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf) — the original rule-based chatbot paper. / 原始基于规则的聊天机器人论文。
- [Thoppilan et al. (2022). LaMDA: Language Models for Dialog Applications](https://arxiv.org/abs/2201.08239) — Google's late neural-chatbot paper, just before LLM agents took over. / Google 后期神经聊天机器人论文，就在 LLM Agent 接管之前。
- [Yao et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — the paper that named the agent loop pattern. / 命名 Agent 循环模式的论文。
- [Anthropic's guide on building effective agents](https://www.anthropic.com/research/building-effective-agents) — 2024 production guidance that still holds in 2026. / 2024 年生产指南，2026 年仍然有效。
- [Greshake et al. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) — the prompt-injection paper. / 提示注入论文。
- [OWASP Top 10 for LLM Applications 2025 — LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — the ranking that made prompt injection the top security concern. / 使提示注入成为首要安全关注的排名。
- [AWS — Securing Amazon Bedrock Agents against Indirect Prompt Injections](https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agents-a-guide-to-safeguarding-against-indirect-prompt-injections/) — practical orchestration-layer defenses including Plan-Verify-Execute and user-confirmation flows. / 实用编排层防御，包括规划-验证-执行和用户确认流程。
- [EchoLeak (CVE-2025-32711)](https://www.vectra.ai/topics/prompt-injection) — the canonical zero-click data-exfiltration CVE from indirect prompt injection. Reference case for why write-access agents need runtime defenses. / 间接提示注入的典型零点击数据泄露 CVE。写入权限 Agent 需要运行时防御的参考案例。
