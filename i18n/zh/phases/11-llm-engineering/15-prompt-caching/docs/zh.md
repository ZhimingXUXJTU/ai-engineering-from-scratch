# 提示缓存与上下文缓存

> 您的系统提示是4000个代币.您的RAG文本是20,000个代币.您每次请求都会发送两种代币.您每次都会支付两种代币.快速缓存允许提供商将该预先端放在其侧面,并将正常使用率的10%收费.如果正确使用,它将推断成本减少5090%和第一次代币延迟4085%.

> **【中文解读】**系统提示4000代币 + RAG 上下文20000代币,每次请求都必须付费.提示缓存让供应商保留前,重用时只收取10%费用.

> **【拓展：提示缓存→RAG生产优化】**人类的快速缓存和OpenAI的缓存响应是RAG产品系统降低成本的关键技术,特别是有固定系统提示和大量检查下面的场景.

>  **【前置】**节前请先掌握:阶段11·01(即时工程)、阶段11·05(文本工程)、阶段11·11(缓存成本)。本节是其延伸,讲提供商层(人类缓存_控制、OpenAI自动缓存、双胞胎缓存内容)。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 01 (Prompt Engineering), Phase 11 · 05 (Context Engineering), Phase 11 · 11 (Caching and Cost) | **前置知识:** Phase 11 · 01 (提示工程)、05 (上下文工程)、11 (缓存与成本)
**Time:** ~60 minutes | **时间:** ~60 分钟

## 问题 问题引入

编码代理在每次对话中都会向克劳德发送相同的15000代币系统提示.$3/M input tokens is $只有 0.90 美元的输入成本, 之前用户的任何实际消息.乘以每天的10,000次对话,账单达到9,000美元/天,

> 一个编程代理在每次对话中发送相同的15000个代币给克劳德.$3/M 输入 token，仅输入成本就是 $账单每天达到9000美元.

您不能减少提示,而不会损害质量.您不能避免发送它. 模型需要它在每一个转折.唯一的举动是停止支付完整的价格为供应商已经看到的预写.

> 你不能缩小提示,不损坏质量. 你不能避免发送它.

>  **【类比】**快递公司记住您常用的地址"第一次发货要详细说明"北京市朝阳区...",之后每次发货只需说"老地方",快递公司自动调出地址。技术上:供应商把前的KV缓存 存在自己的服务器,下次请求来直接复用,不需要重新计算注意的K/V矩阵。对用户透明你只需要在API调用加个`cache_control`标记:

> ️ **【易错点】**快速缓存的3个坑:(1) **prefix 顺序敏感** cache 命中要求前 完全相同(包括空格、换行),系统提示 末尾多一个空格就错过;务必把可变部分(用户输入) 放最后。(2) **cache TTL 5 分钟**人类默认 5 分钟过期,没流量时缓存 失效;用延长的TTL(1 小时) 保住冷启动场景――(3) **没监控命中率**不知道命中率就无法判断收益;人类API响应 里有`cache_creation_input_tokens`和 `cache_read_input_tokens`记录到监控板.

这一举动是快速缓存.安特罗皮克在2024年8月发布 (在2025年推出1小时的延长TTL变体),OpenAI自动化了该年晚些时候,谷歌在双子座1.5号的同时发布了明确的语境缓存,现在这三个都将其作为其边界模型的一流功能.

> 这种方法就是提示缓存. 人类在2024年8月推出它.


> **【中文解读】**快速缓存的价值在系统快速通常很长 ((5K+代币) 并在所有请求中不变──每次请求都重新计算这些代币的KV缓存是巨大的浪费──缓存后,这些代币的计算成本从100%降至接近0%──


## 概念的核心概念

> **【中文解读】**快速缓存利用LLM推理的特性如果多个请求共享相同的快速前,可以缓存该前的KV缓存计算结果,避免重复计算.

> **【拓展：Prompt Caching 的成本节省】**化快速缓存将重复前的输入 成本降低约90%──OpenAI的类似功能将缓存输入 价格降低至$0.50/M tokens（原价 $5,对系统即时5K代币 + 平均10次复用场景,月成本可降低约75%


![Prompt caching: write once, read cheap](../assets/prompt-caching.svg)

**The mechanic.**当请求的前与最近请求的前相匹配时,提供商将从前运行中提供KV缓存,而不是重新编码代币.你第一次支付小写费,每次都会收取大阅读折扣.

> **机制。**当请求的前与最近请求的前匹配时,供应商从上次运行中提供KV缓存,而不是重新编码代币――你第一次支付少量的写入溢价,然后每次享受大量阅读折扣――

**Three provider flavors in 2026.**

| Provider | API style | Hit discount | Write premium | Default TTL | Min cacheable |
|---------|-----------|--------------|---------------|-------------|---------------|
| Anthropic | Explicit `cache_control` markers on content blocks | 90% off input | 25% surcharge | 5 min (extendable to 1 hour) | 1,024 tokens (Sonnet/Opus), 2,048 (Haiku) |
| OpenAI | Automatic prefix detection | 50% off input | none | Up to 1 hour (best-effort) | 1,024 tokens |
| Google (Gemini) | Explicit `CachedContent` API | Storage-billed; read at ~25% of normal | Storage fee per token·hour | User-set (default 1 hour) | 4,096 tokens (Flash), 32,768 (Pro) |

**The invariant.**如果任何代币在请求之间不同,则在第一个不同代币之后的一切都是错误. 放在顶部的 *稳定* 部分,下面的 *变量* 部分.

> **不变量。**三者都只缓存前──如果请求之间有任何符号不同,第一个不同符号后的所有内容都是未定.将*稳定*部分放在顶部,可变*部分放在底部──

### 缓存友好的布局

```
[system prompt]          <-- cache this
[tool definitions]       <-- cache this
[few-shot examples]      <-- cache this
[retrieved documents]    <-- cache if reused, else don't
[conversation history]   <-- cache up to last turn
[current user message]   <-- never cache (different every time)
```

违反命令 将用户消息放在系统提示上面, 间接几次截图之间动态检索 和缓存永远不会打.

> 违反顺序将用户信息放在系统提示上,在少量样本之间插动态检查缓存永远不会被命中.

### 破产平衡计算

为了节省净资金,预存区块必须至少读到两次. 1 写 + 1 读平均每次请求成本 0.675x (节省 32%); 1 写 + 10 读平均 0.205x (节省 80%). 指规则:预计在 TTL 中至少 3 次重复使用任何预存.

> 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测: 预测:

## 建立它,实现它.
```figure
prompt-cache-hit
```

## 建立它

### 步骤1: 通过明确标记进行人类提示缓存

```python
import anthropic

client = anthropic.Anthropic()

SYSTEM = [
    {
        "type": "text",
        "text": "You are a senior Python reviewer. Follow the rubric exactly.\n\n" + RUBRIC_15K_TOKENS,
        "cache_control": {"type": "ephemeral"},
    }
]

def review(code: str):
    return client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": code}],
    )
```

其他`cache_control`标记告诉人类存储区块5分钟. 在窗口中重复使用; 过期后重复使用,然后再写.

> `cache_control`标记告诉人类将该块存储5分钟.

**Response usage fields:**

```python
response = review(code_a)
response.usage
# InputTokensUsage(
#     input_tokens=120,
#     cache_creation_input_tokens=15023,   # paid at 1.25x
#     cache_read_input_tokens=0,
#     output_tokens=340,
# )

response_b = review(code_b)
response_b.usage
# cache_creation_input_tokens=0
# cache_read_input_tokens=15023           # paid at 0.1x
```

检查IC 中的两个字段,如果 `cache_read_input_tokens`在请求中保持零,你的缓存密钥漂移.

> 在IC中检查这两个字段如果`cache_read_input_tokens`在多次请求中保持为零,你的缓存键正在漂移.

### 步骤2:延长1小时的TTL

对于长期的批次工作,工作间的5分钟违约期会到期.`ttl`其他:

```python
{"type": "text", "text": RUBRIC, "cache_control": {"type": "ephemeral", "ttl": "1h"}}
```

一小时的TTL成本是写费的两倍 (50%比基线而不是25%),但在任何批次中重复使用前的时间超过5次时,会很快回报.

> 报价为1小时的TTL,是基准的2倍,而不是25%),但在任何重用前超过5次批量处理中很快回本.

### 步骤3:OpenAI自动缓存

任何与最近的请求相匹配的1024个代币以上的预写符都会自动获得50%折扣.

```python
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},   # long and stable
        {"role": "user", "content": user_msg},
    ],
)
resp.usage.prompt_tokens_details.cached_tokens  # the discounted portion
```

两个因素会杀死OpenAI的缓存,而不是杀死Anthropic的:改变 `user`字段 (作为缓存密钥组件使用) 和重新排序工具.

> 两件事会杀死OpenAI的缓存而不会杀死人类的:更改`user`字段和重新排序工具──

### 步骤4:双子座明确的语境缓存

双子座将缓存视为你创建的第一类对象,

```python
from google import genai
from google.genai import types

client = genai.Client()

cache = client.caches.create(
    model="gemini-3-pro",
    config=types.CreateCachedContentConfig(
        display_name="rubric-v3",
        system_instruction=RUBRIC,
        contents=[FEW_SHOT_EXAMPLES],
        ttl="3600s",
    ),
)

resp = client.models.generate_content(
    model="gemini-3-pro",
    contents=["Review this code:\n" + code],
    config=types.GenerateContentConfig(cached_content=cache.name),
)
```

双子座每一个代币·小时的存储费用是缓存存存储存存存存存存存存存存存存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存存储存存存存存存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存储存存存储存存储存存储存存储存存存存储存存存储存存储存存存存存储存储存存存存存储存存存存存储存存存存存存储存存存存存储存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存存

> 双子座按缓存存活期间每代币·小时收取存储费,读取费率约为正常输入的25%──当你在多次会议中跨天重复使用相同的大型提示时,这是正确的选择──

### 步骤5:测量生产中撞击率

看到`code/main.py`对于一个模拟的三供应商会计师,该会追踪写/阅读/错过计算和计算每1K请求的混合成本. 门部署在目标的成功率大多数生产的人类设置应看到>80%的读数分数在加热后.

> 见`code/main.py`获取模拟的三供应商会计师,跟踪写入/读取/未预期计数并计算每千请求的混合成本.

## 陷在2026年仍存在

> 2026年仍在线陷:

- **Dynamic timestamps at the top.** `"Current time: 2026-04-22 15:30:02"`系统提示的顶部,每个请求都错过了. 移动时间标签在缓存破点以下.
  **顶部的动态时间戳。**系统提示顶部放 `"Current time: 2026-04-22 15:30:02"`,每次请求都未定.
- **Tool reordering.**系统化工具稳定顺序 部署之间的命令调整,
  **工具重排序。**以稳定序列序列化工具部署间的字典重排破坏每次命中──
- **Free-text near-duplicates.**"你是有帮助的. "vs"你是有帮助的助手. "一个字节差异 = 完全错过.
  **自由文本近似重复。**"你是个有帮助的助手".
- **Too-small blocks.**哈伊库的小块默默不存储.
  **过小的块。**强制1024代币 下限(海库为2,048)。更小的块静默不缓存。
- **Blind cost dashboards.**输入代码分为缓存与未缓存.否则流量下降看起来像缓存获利.
  **盲目的成本仪表板。**输入代币将拆成缓存与未缓存.

## 用它实现框架

预备备库2026:

> 2026 缓存技术:

| Situation | Pick |
|-----------|------|
| Agent with stable 10k+ system prompt, many turns | Anthropic `cache_control` with 5-min TTL |
| Batch job reusing a prefix for 30+ minutes | Anthropic with `ttl: "1h"` |
| Serverless endpoints on GPT-5, no custom infra | OpenAI automatic (just make your prefix stable and long) |
| Multi-day reuse of a giant code/doc corpus | Gemini explicit `CachedContent` |
| Cross-provider fallback | Keep the cacheable prefix layout identical across providers so any hit works |

| 场景 | 选择 |
|------|------|
| Agent 有稳定 10k+ 系统提示、多轮 | Anthropic `cache_control` 配 5 分钟 TTL |
| 批处理重用前缀 30+ 分钟 | Anthropic 配 `ttl: "1h"` |
| GPT-5 上的无服务器端点、无定制基建 | OpenAI 自动（让前缀稳定且够长） |
| 多天重用大型代码/文档语料 | Gemini 显式 `CachedContent` |
| 跨提供商回退 | 跨提供商保持可缓存前缀布局一致，任何命中都工作 |

结合用户信息层的语义缓存 (阶段11 · 11):提示缓存处理 *代币相同*重复使用,语义缓存处理 *意义相同*重复使用.

> 与语义缓存(Phase 11 · 11)结合用于用户消息层:提示缓存处理*代码 完全相同*的重用,语义缓存处理*语义相同*的重用──

## 运送它.

保存`outputs/skill-prompt-caching-planner.md`其他:

```markdown
---
name: prompt-caching-planner
description: Design a cache-friendly prompt layout and pick the right provider caching mode.
version: 1.0.0
phase: 11
lesson: 15
tags: [llm-engineering, caching, cost]
---

Given a prompt (system + tools + few-shot + retrieval + history + user) and a usage profile (requests per hour, TTL needed, provider), output:

1. Layout. Reordered sections with a single cache breakpoint marked; explain which sections are stable, which are volatile.
2. Provider mode. Anthropic cache_control, OpenAI automatic, or Gemini CachedContent. Justify from TTL and reuse pattern.
3. Break-even. Expected reads per write within TTL; net cost vs no-cache with math.
4. Verification plan. CI assertion that cache_read_input_tokens > 0 on the second identical request; dashboard split by cached vs uncached tokens.
5. Failure modes. List the three most likely reasons the cache will miss in this setup (dynamic timestamp, tool reorder, near-duplicate text) and how you will prevent each.

Refuse to ship a cache plan that places a dynamic field above the breakpoint. Refuse to enable 1h TTL without a reuse count that makes the 2x write premium pay back.
```

## 练习题

1. **Easy.**通过5000个代币系统来对抗克劳德进行10轮对话.`cache_control`报告每个输入代码的账单.
   取一个10轮对话和5000个代币 系统提示,不使用和使用 `cache_control`分别运行,报告输入代币费用.
2. **Medium.**写一个测试,根据提示模板和请求日志,计算每个提供商的预期成功率和美元节省 (Anthropic 5m,Anthropic 1h,OpenAI自动,Twin explicit).
   编写测试工具,给定提示模板和请求日志,计算每个提供商预期命运率和节省金额.
3. **Hard.**创建布局优化器:给出提示和标记的字段列表 `stable=True/False`通过一个简单的缓存,将一个缓存破解点放在最大的缓存友好的位置,而不输掉信息.
   构建布局优化器:重写提示将缓存断点放在最大缓存友好位置.

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Prompt caching | "Makes long prompts cheap" / "让长提示变便宜" | Reusing a provider-side KV-cache for matching prefixes; 50-90% discount on repeated input tokens. | 提示缓存：重用供应商端的 KV-cache，对重复输入 token 提供 50-90% 折扣 |
| `cache_control` | "The Anthropic marker" / "Anthropic 标记" | Content-block attribute that declares "everything up to here is cacheable"; `{"type": "ephemeral"}`. | cache_control：内容块属性，声明"到这里为止的内容可缓存" |
| Cache write | "Paying the premium" / "付溢价" | The first request that populates the cache; billed at ~1.25x input rate on Anthropic, free on OpenAI. | 缓存写入：第一次填充缓存的请求 |
| Cache read | "The discount" / "折扣" | Subsequent requests matching the prefix; billed at 10% (Anthropic), 50% (OpenAI), ~25% (Gemini). | 缓存读取：匹配前缀的后续请求 |
| TTL | "How long it lives" / "存活时间" | Seconds the cache stays warm; Anthropic 5m default (extendable 1h), OpenAI best-effort up to 1h, Gemini user-set. | TTL：缓存保持活跃的秒数 |
| Extended TTL | "1-hour Anthropic cache" / "1小时缓存" | `{"type": "ephemeral", "ttl": "1h"}`; 2x write premium but worth it for batch reuse. | 扩展 TTL：1 小时缓存，2 倍写入溢价 |
| Prefix match | "Why my cache missed" / "为什么缓存未命中" | Caches only hit when every token from the start up to the breakpoint is byte-identical. | 前缀匹配：缓存只在从开头到断点的每个 token 完全相同时才命中 |
| Context caching (Gemini) | "The explicit one" / "显式缓存" | Google's named, storage-billed cache object; best for multi-day reuse of large corpora. | 上下文缓存 (Gemini)：命名、按存储计费的缓存对象 |

## 继续阅读 继续阅读

- [Anthropic — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) `cache_control`时间1小时,平衡表.
  预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览 预览
- [OpenAI — Prompt caching](https://platform.openai.com/docs/guides/prompt-caching)自动前匹配.
  开放AI提示缓存文档 自动前匹配
- [Google — Context caching](https://ai.google.dev/gemini-api/docs/caching) `CachedContent`存储器和存储器的价格.
  谷歌上下文缓存文档CachedContent API 和存储定价
- [Anthropic engineering — Prompt caching for long-context workloads](https://www.anthropic.com/news/prompt-caching)原始发射站,延迟号码.
  汉化工程博客长上下文工作负载的提示缓存,含延迟数据──
- 阶段11 · 05 (文本工程)  如何切断提示器,以便缓存可登陆.
  第11阶段 · 05                                                                                                                                                                                                                                                            
- 对应缓存与用户消息的语义缓存.
  第11阶段 · 11(缓存与成本) 将提示缓存与用户消息的语义缓存配对.
- [Pope et al., "Efficiently Scaling Transformer Inference" (2022)](https://arxiv.org/abs/2211.05102) KV缓存存储器模型,提示缓存将用户暴露在缓存中;解释为什么缓存前置器的重读比重新计算便宜10x.
  解释为什么缓存前比重计算便宜约10倍的KV缓存内存模型论文.
- [Agrawal et al., "SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills" (2023)](https://arxiv.org/abs/2308.16369)预填是阶段提示缓存快捷方式;本文解释了为什么TTFT在缓存中大幅下降,而TPOT不受影响.
  解释为什么缓存命中时TTFT大幅下降而TPOT不受影响的论文.
- [Leviathan et al., "Fast Inference from Transformers via Speculative Decoding" (2023)](https://arxiv.org/abs/2211.17192)快速缓存与投机解码,闪光注意力和MQA/GQA作为曲线的杆,
  提示缓存与投机解码、Flash Attention 和 MQA/GQA 并列的推理成本曲线杆──
