# 聊天机器人 规则 基于规则到神经系统到法师事务所代理人

> 卡罗里斯在一个小时内,他发现了一个不错的东西,然后他开始做了一些事情.
> 通过" 互动互动"来解决上一代最严重的失败.

> **【中文解读】**从Eliza到Seq2Seq到GPT代理.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 13 (Question Answering), Phase 5 · 14 (Information Retrieval) | **前置知识:** Phase 5 · 13（问答系统），Phase 5 · 14（信息检索与搜索）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

系统必须弄清楚他们想要什么,缺失什么信息,如何获取它,以及如何完成操作.然后用户说"等,如果我取消?"系统必须记住文本,切换任务,保存状态.

> 用户说"我想改变航班"",系统必须弄清楚他们想要什么"",缺少什么信息"",如何获取"",如何完成操作"",然后用户说"等等等,如果我要取消呢?"系统必须记住下文"",切换任务并保持状态――

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

对于 ML 系统来说,对话很难.输入是无限的.输出必须在多个转折中保持一致.系统可能需要对世界产生影响 (改变飞行,充电卡).用户可以看到每一步错误.

> 对于 ML 系统来说很难.输入是开放式的.输出必须在多轮中保持连贯.系统可能需要对世界采取行动.

聊天机器人架构已经通过四个范式进行了循环,每个范式都被引入,因为前一个太明显失败了.这堂课让它们顺序.2026年生产景观是最后两个混合物.

> 机器架构经历了四种范式,每种都是因为前一种失败太明显而引入的.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

![Chatbot evolution: rule-based → retrieval → neural → agent](../assets/chatbot.svg)

### 剧本写的半个世纪,1950-2001

首先,这个模式不持续五年.它持续了五十年.知道它的弧线是重要的,因为它中的每个系统都是相同的机器匹配输入,发出一个装响应,更新一个小状态,五十年的添加规则到那台机器从来没有产生了一般的情况.这天花板是为什么两到四个范式存在.

**1950.**图灵通过提出一个操作替代方案来回避"机器能思考吗?" 如果一个询问者无法通过电话来区分机器与人,那么哲学问题就会被争论.

**1956.**根据"人工智能"的假设,每个智能特征"原则上可以以如此精确的精度描述,以使一个机器可以模拟它".

**1966.**子在一步中建立了反思技巧:分解规则从输入中抽取碎片,重组规则回声回复它们作为问题.大约200个模式总数,零状态,零理解,用户无论如何都信任它.韦森巴姆在他的职业生涯的余分时间都惊于它需要多少机器.

**1972.**帕里在斯坦福大学建立了一个偏执的模型, 恐惧,愤怒和不信任的数值变量在每一个转折和门上更新, 脚本接下来开启, 在盲目的转录测试中,精神科医生将PARRY与人类患者分开. 它是人格调节的直接祖先, 作为三个浮动系统的系统提示. 同年,这两个机器人通过ARPANET互相指向:一个治疗师采访一个偏执状态机器的脚本,

**1995.**艾利斯用AIML来扩展ELIZA的配方,这是一个用于模式模板对的XML方言.大约有4万个手写类别,赢得了三个洛伯纳奖.它证明了基于规则的系统的扩展法:更多的规则买入覆盖,从来没有通用性.每个规则都是一个责任有人必须保持.

**2001.**智能儿童将该食谱放在3000万即时消息用户面前,并添加后端查询 天气,股票,电影时间 拼接到模板中.

五十年,一个机制,一个规则的增加. 范式结束了,不是因为有人否认它,

```figure
chatbot-lineage
```

**Rule-based (ELIZA, AIML, DialogFlow).**手动编写的模式与用户输入匹配,产生响应.意图分类器向预定义的流程路由.填充机器收集所需信息.它在设计的狭窄范围内工作得很好.它立即失败.仍然在安全关键领域 (银行身份验证,航空公司预订) 里运输,在这些领域不容忍幻觉.

> **基于规则（ELIZA、AIML、DialogFlow）。**手写模式匹配用户输入并产生响应――意图分类器路由到预定义流程――槽位填充状态机收集所需信息――在设计的狭窄范围内表现出色――超出范围立即失败――仍在不容许的安全关键领域――银行认证、航空公司预订) 中使用――

**Retrieval-based.**采用常见问题类型的系统. 编码每一对 (发言,响应). 在运行时,编码用户的消息,并检索最近存储的响应. 想象Zendesk的经典"类似文章"功能. 处理比规则更好. 没有生成,所以没有幻觉.

> **基于检索。**编码时编码用户消息并检索最近的存储响应.

**Neural (seq2seq).**编码解码器训练在对话日志上.从零开始生成响应.流动但容易产生通用输出 ("我不知道") 和事实漂移.从来没有在主题上靠谱. Google,Facebook和微软在2016-2019年都有令人失望的聊天机器人.

> **神经（seq2seq）。**在对话日志上训练的编码器解码器──从零生成响应──流但倾向于通用输出("我不知道") 和事实漂移──从不可靠地保持主题──这就是谷歌、Facebook和微软在2016-2019年有令人失望的聊天机器的原因──

**LLM agents.**语言模型包裹在一个循环中,它计划,调用工具,并验证结果.不是一个长时间提示的聊天机.一个代理循环:计划 →调用工具 →观察结果 →决定下一步.检索-第一地定位 (RAG) 阻止它幻觉.工具调用让它实际上做事情.这是2026年架构.

> **LLM Agent。**包装在循环中的语言模型,规划,调用工具并验证结果――不是带长提示的聊天机器人――一个代理 循环:规划 → 调用工具 → 观察结果 →决定下一步――检索优先定(RAG) 防止幻觉――工具调用让它实际做事――这就是2026年架构――

通过所有四个路线:基于规则的身份验证和破坏性行动,查询常见问题,神经生成自然表达,对模糊的开放式查询的LLM代理.

> 这四种范式不是顺序替代的.2026年生产聊天机器人通过所有四种路径:基于规则用于认证和破坏性操作,检查用于FAQ,神经生成用于自然措辞,LLM代理用于模糊的开放式查询.

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

### 步骤1:基于规则的模式匹配

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

思考技巧 ("我感到悲伤" → "你为什么感到悲伤") 是1966年威森巴姆的常规心理治疗师演示.

> 伊丽莎·反射技巧:"我感到悲伤" →"你为什么感到悲伤") 是威森巴姆1966年的经典心理治疗师演讲.

### 步骤2:基于检索 (FAQ)

这段插图需要`pip install sentence-transformers`火的火.`code/main.py`这一课使用了Stdlib Jaccard相似性,所以课程没有外部依赖.

> 这样一个例子需要代码片段`pip install sentence-transformers`现在,我在读了这篇文章.`code/main.py`使用标准库的Jaccard相似度代替,这样的课程无需外部依赖即可运行.

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

如果最好的匹配不够近,请返回.`None`让系统升级.

> 基于值的拒绝是关键设计选择.`None`让系统升级处理.

### 步骤3:神经生成 (基线)

使用一个小的指示调节的编码器-解码器 (FLAN-T5) 或一个精细调节的对话模型. 产品本身无法使用2026年 (矛盾,非主题漂移,事实无稽之谈),但在混合系统内运输自然表达. 只有DialoGPT式解码器模型需要明确的转分区和EOS处理来产生一致的答案;一个FLAN-T5文本2文本管道作为教学例子是无机的.

> 使用小型指令微调编码器-解码器(FLAN-T5) 或微调的对话模型──2026年单独使用不适合生产(矛盾、跑题、事实错误),但在混合系统中用于自然措辞──DialogGPT风格的仅解码器模型需要显式轮次分隔符和EOS 处理才能产生连贯回复;FLAN-T5文本2文本流水线开箱即可适合教学示例──

```python
from transformers import pipeline

chatbot = pipeline("text2text-generation", model="google/flan-t5-small")

response = chatbot("Respond politely to: Hi there!", max_new_tokens=40)
print(response[0]["generated_text"])
```

### 步骤4:LLM代理循环

2026年生产形状:

> 2026年生产形态:

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

工具是 LLM可以调用的可调用函数. LLM返回最终答案而不是工具调用时循环结束.步骤预算防止无限的循环在模糊任务.

> 三个要点――工具是 LLM 可以调用的函数――当 LLM 返回最终答案而不是工具调用时循环终止――步骤预算防止模糊任务的无限循环――

实际生产增加了:检索-第一地 (在每次LLM电话之前注入相关文件),防护护 (不确认拒绝破坏性行动),可观察性 (每一步都记录),以及评估 (自动检查代理行为保持在规范状态).

> 实际生产还需要:检索优先定(每次 LLM 调用前注入相关文档) 护(未经确认拒绝破坏性操作) 可观测性(记录每步) 和评估(自动检查代理 行为保持规范) 

### 步骤5:混合路由

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

模式:任何破坏性的决定性规则,用于装常见问题,用于其他所有的事情的LLM代理.

> 模式:对任何破坏性操作使用确定性规则,对固定查询,对其他所有使用LLM代理.

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

现在,我们要做什么?

> 2026 年技术:

| Use case / 使用场景 | Architecture / 架构 |
|---------|---------------|
| Booking, payment, authentication / 预订、支付、认证 | Rule-based state machines + slot filling / 基于规则的状态机 + 槽位填充 |
| Customer support FAQs / 客户支持 FAQ | Retrieval over curated answers / 对精选答案的检索 |
| Open-ended help chat / 开放式帮助聊天 | LLM agent with RAG + tool calls / 带 RAG + 工具调用的 LLM Agent |
| Internal tools / IDE assistants / 内部工具 / IDE 助手 | LLM agent with tool calls (search, read, write) / 带工具调用的 LLM Agent（搜索、读写） |
| Companion / character chatbots / 伴侣/角色聊天机器人 | Tuned LLM with persona system prompt, retrieval on knowledge / 微调 LLM 配角色系统提示和知识检索 |

总是使用混合路由在生产中.没有一个架构都能处理每一个请求.路由层本身通常是一个小的意图分类器.

> 在生产中始终使用混合路由.没有单一的架构能处理每种请求.

## 仍然运输的失败模式将进入生产失败模式

- **Confident fabrication.**减轻:验证结果,记录工具的调用,永远不要让LLM声称没有成功的工具返回.
  **自信捏造。**士官声称完成未完成的操作.缓解:验证结果,记录工具调用.永远不让士官在没有成功工具的情况下声称完成某事.
- **Prompt injection.**用户插入了超过系统提示的文本.在OWASP LLM应用程序2025年10大排名中排名的LLM01.两种口味:直接注射 (贴在聊天中) 和间接注射 (隐藏在文件,电子邮件或工具输出中,代理阅读).
  **提示注入。**用户插入覆盖系统提示的文本──在OWASP LLM 应用 2025 中排列十大中排列 LLM01──两种形式:直接注入(粘贴到聊天中) 和间接注入(藏在文档、邮件或代理 读取的工具输出中)──

  攻击率因情况而异. 在一般工具使用和编码基准中,测量成功率在边界模型中为0.5-8.5%. 特定高风险设置 (适应性攻击AI编码代理,脆弱的编排) 达到84%. 产品 CVE包括 EchoLeak (CVE-2025-32711, CVSS 9.3) 微软 365 副驾驶员中零点击数据泄露漏洞是由攻击者控制的电子邮件触发的.
  攻击成功率因场景而异. 在通用工具使用和编码基准中,前沿模型的测量成功率约为0.5-8.5%──特定风险设置.

  减轻措施:将用户输入视为整个循环中不值得信赖;在工具调用之前进行清洁;将工具输出从主提示中隔离;使用计划-验证-执行 (PVE) 模式,该模式首先计划,然后在执行之前验证每个行动与该计划相反 (这阻止工具结果注入新的未计划的行动);要求用户确认破坏性行动;对工具范围应用最小特权.
  缓解措施:在整个循环中将用户输入视为不可信;工具调用前消毒;将工具输出与主提示隔离;使用规划验证-执行 (PVE) 模式,代理先规划,然后对每个操作按计划验证后再执行 (这阻止工具结果注入新的未计划操作);对破坏性操作要求用户确认;对工具范围应用最小权限.

  没有大量的快速工程完全消除了这种风险. 需要外部运行时防护层 (LLM Guard,允许验证,语义异常检测).
  无论多少提示工程都无法完全消除这一风险.
- **Scope creep.**减轻:狭窄工具合约;保持系统的焦点;增加对任务之外的率的评估.
  **范围蔓延。**由于工具调用返回间接相关信息和运行问题.
- **Infinite loops.**减轻:步骤预算,工具调用减倍,法师法官说"我们正在取得进展".
  **无限循环。**缓解:步骤预算、工具调用重量、LLM 判断"是否有进展"――
- **Context window exhaustion.**缓解:总结较早的转折,通过相似性检索相关的过去转折,或使用长文本模型.
  **上下文窗口耗尽。**长对话将最早轮次推出上下文――缓解:摘要旧轮次、根据相似性检查相关历史轮次、或使用长上下文模型――

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

## 运送它.

保存如`outputs/skill-chatbot-architect.md`其他:

> 保存为`outputs/skill-chatbot-architect.md`其他:

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

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## 练习题

1. **Easy.**执行上述基于规则的响应,为咖啡店订购机器人进行10个模式. 测试边缘情况:双订单,修改,取消,不明确的意图.
   **简单。**为咖啡店点单机器人实现上述基于规则的响应,10 个模式――测试边界情况:重复订单、修改、取消、模糊意图――
2. **Medium.**构建一个混合FAQ+LLM回复. 50个包装FAQ输入用于SaaS产品,LLM回复与文件网站检索.测量100个真正的支持问题上的拒绝率和准确性.
   **中等。**构建混合FAQ+LLM 回退──50个SaaS产品的固定FAQ条目,LLM 回退带文档站检索──在100个真实支持问题上测量拒绝率和准确率──
3. **Hard.**执行上述代理循环,使用三个工具 (搜索,阅读用户数据,发送电子邮件).运行50个测试场景的评估,包括即时注射尝试.报告出班率,失败任务率和任何注射成功.
   **困难。**用三个工具 (搜索,读取用户数据,发送邮件) 实现上述代理循环.运行包括50个测试场景的评估,包括提示注入尝试.

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.

## 关键词 快速查找表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Intent（意图） | What the user wants / 用户想要什么 | Categorical label (book_flight, reset_password). Routed to a handler. / 分类标签（book_flight、reset_password）。路由到处理器。 |
| Slot（槽位） | A piece of info / 一条信息 | Parameter the bot needs (date, destination). Slot filling is the sequence of asks. / 机器人需要的参数（日期、目的地）。槽位填充是依次询问的过程。 |
| RAG（检索增强生成） | Retrieval plus generation / 检索加生成 | Retrieve relevant docs, then ground the LLM's response. / 检索相关文档，然后锚定 LLM 的响应。 |
| Tool call（工具调用） | Function invocation / 函数调用 | LLM emits a structured call with name + args. Runtime executes, returns result. / LLM 发出带名称和参数的结构化调用。运行时执行并返回结果。 |
| Agent loop（Agent 循环） | Plan, act, verify / 规划、执行、验证 | Controller that runs LLM calls interleaved with tool calls until task complete. / 运行 LLM 调用与工具调用交错直到任务完成的控制器。 |
| Prompt injection（提示注入） | User attacks prompt / 用户攻击提示 | Malicious input that tries to override the system prompt. / 试图覆盖系统提示的恶意输入。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.

## 继续阅读 继续阅读

- [Weizenbaum (1966). ELIZA — A Computer Program For the Study of Natural Language Communication](https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf)原始基于规则的聊天机器人论文.
- [Thoppilan et al. (2022). LaMDA: Language Models for Dialog Applications](https://arxiv.org/abs/2201.08239)谷歌的晚期神经聊天机器人论文,就在LLM代理接管之前.
- [Yao et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)标记了代理循环模式的论文.
- [Anthropic's guide on building effective agents](https://www.anthropic.com/research/building-effective-agents) 2024年生产指南,2026年仍有效──
- [Greshake et al. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173)即时注射纸. / 提示注入论文。
- [OWASP Top 10 for LLM Applications 2025 — LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)使即时注射成为安全关注的首要排名.
- [AWS — Securing Amazon Bedrock Agents against Indirect Prompt Injections](https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agents-a-guide-to-safeguarding-against-indirect-prompt-injections/)包括计划验证执行和用户确认流程在内的实用编排层防御,包括规划验证执行和用户确认流程.
- [EchoLeak (CVE-2025-32711)](https://www.vectra.ai/topics/prompt-injection)可波及间接提示注射的可波及数据零点击-exfiltration CVE. 写入访问代理需要运行时间防御的参考案例. / 间接提示注入的典型零点击数据泄露 CVE──写入权限 需要运行时防御的参考案例──
| Intent | What the user wants | Categorical label (book_flight, reset_password). Routed to a handler. |
| Slot | A piece of info | Parameter the bot needs (date, destination). Slot filling is the sequence of asks. |
| RAG | Retrieval plus generation | Retrieve relevant docs, then ground the LLM's response. |
| Tool call | Function invocation | LLM emits a structured call with name + args. Runtime executes, returns result. |
| Agent loop | Plan, act, verify | Controller that runs LLM calls interleaved with tool calls until task complete. |
| Prompt injection | User attacks prompt | Malicious input that tries to override the system prompt. |

## 进一步阅读

- [Turing (1950). Computing Machinery and Intelligence](https://academic.oup.com/mind/article/LIX/236/433/986238)使对话成为该领域的基准.
- [Weizenbaum (1966). ELIZA — A Computer Program For the Study of Natural Language Communication](https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf)基于规则的原始聊天机器人论文.
- [Colby, Weber, Hilf (1971). Artificial Paranoia](https://doi.org/10.1016/0004-3702(71)巴里的影响变量架构,是第一台充满状态的聊天机器人.
- [Thoppilan et al. (2022). LaMDA: Language Models for Dialog Applications](https://arxiv.org/abs/2201.08239)谷歌的晚期神经聊天机论文, 就在法学院代理人接管之前.
- [Yao et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)是指指代理循环模式的文件.
- [Anthropic's guide on building effective agents](https://www.anthropic.com/research/building-effective-agents) 2024年生产预测,仍在2026年保持.
- [Greshake et al. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173)即时注射纸.
- [OWASP Top 10 for LLM Applications 2025 — LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)使即时注射成为安全问题.
- [AWS — Securing Amazon Bedrock Agents against Indirect Prompt Injections](https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agents-a-guide-to-safeguarding-against-indirect-prompt-injections/)包括计划-验证-执行和用户确认流程在内的实用调整层防御.
- [EchoLeak (CVE-2025-32711)](https://www.vectra.ai/topics/prompt-injection)可视的零点击数据泄漏CVE从间接提示注射. 为什么写入访问代理需要运行时间防御的参考案例.
