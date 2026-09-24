# 现在,我们在这个问题上,我们需要一个问题.

> 关于HITL的2026年共识是具体的. 它不是"代理要求,用户点击批准". 它是提出-然后承诺:建议的行动是继续使用无权密钥的持久存储器;向审查者显示了意图,数据谱系,触摸的权限,爆炸半径和反弹计划;只有在积极的确认后进行;执行后验证以确认副作用实际发生. 长格拉夫的`interrupt()`另外,我们还可以使用微软代理框架的 PostgreSQL 检查点.`RequestInfoEvent`云的`waitForApproval()`标准的标准是: 通过"通过"的,没有审查的. 文件的减轻是挑战和反应,有明确的检查列表.

> **【中文解读】**2026年HITL 共识是具体的──不是"代理问,用户点击批准"──是提出-然后承诺:提议动作以等键持久化到持久存储;向审查者呈现意图,数据谱系、触及权限、爆炸半径、回滚计划;仅在正面确认后提交;执行后验证确认副作用实际发生──长图的`interrupt()`加 PostgreSQL 检查点、微软代理框架的 `RequestInfoEvent`云的`waitForApproval()`规范失败模式是没有审查的地点批准.

> **【拓展：四个状态机步骤】**提出,然后承诺是四步状态机:(1) 提议代理产生动作,以等键持久化带意图/数据谱系/触及权限/爆炸半径/回滚计划;(2) 呈现审查员(人类,非代理自审) 看到所有元数据;(3) 提交正面确认,动作执行;(4) 验证执行后回读副作用确认──这是数据库`RETURNING`句、AWS `PutObject`后`GetObject`◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, propose-then-commit state machine with idempotency) | **语言:** Python（标准库，带幂等的提议-提交状态机）
**Prerequisites:** Phase 15 · 12 (Durable execution), Phase 15 · 14 (Tripwires) | **前置知识:** Phase 15 · 12（持久执行），Phase 15 · 14（触发器）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:阶段15·12(可持续执行) 阶段15·14(杀死开关) 阶段14·15(HITL代理模式) ◎本节是HITL的工程化标准四步状态机──
>  **【类比】**提交转账申请 (含收款人,金额,用途,回滚预案) 审查员看到元数据 → 批准 → 执行 → 验证到账――每一步都不能省省――这是人类计算机使用、Claude Code Plan 模式、Stripe API 等的关键统一模式――
> ️ **【易错点】**通过? 弹窗被用户惯性点"是" → 皮章失效──修复:(1) 多选清单(每个动作独立确认);(2) 强制延迟(3秒倒计时);(3) 关键动作双确认(输入金额数字);(4) 显示"爆炸半径"(影响N 个文件、M 个用户) ⋅

## 问题 问题引入

> **【中文解读】**建议后提交 (Propose-then-Commit) 模式要求代理先生成修改方案,但不会立即执行,而是向用户或其他代理展示,审查通过后提交.

> **【拓展：propose then commit】**提出后提交模式是2026年编码代理的标准安全实践. 克劳德代码默认使用这种模式生成修改建议并等待用户确认. 吉特的PR/MR机制也是该模式的应用.

代理人采取行动.用户必须决定:批准或不批准. 如果决定是即时的,那么它可能不是审查.

> 代理人采取行动.用户必须决定:批准还是不批准.

工程问题是如何使结构化审查成为最少阻力的道路.

> 如果决定是结构化,它会慢慢但可信.

2023年HITL模式是一个同步提示:"代理想发送电子邮件给X,体 Y 批准?"用户点击批准.每个人都觉得系统安全.实际上,这个表面很大程度上是纹:用户快速批准,批准预测很少,当代理错误时,审计轨迹显示了用户无法回忆的长期批准历史.

> 2023时代HITL模式是同步提示:"代理要发邮件给X,正文Y批准?"用户点击批准──每个人都感觉系统安全──实践中这个界面被严重章化:用户快速批准,批准预测性低,当代理出错时审计追踪显示用户无法记住长期批准历史──

> **【中文解读】**本节介绍了AI代理的核心概念和实现方法. 代理是由LLM驱动的自主系统,能够观察环境,思考决策,执行行动和循环代直到完成目标.

2026 模式 提出然后承诺 将HITL移动到一个持久的基板上,附加结构化元数据,并需要积极的承诺.

> 2026年模式 提出后承诺 将HITL 移至持久基板上,附加结构化元数据,要求正面提交.

每个管理代理SDK都发送一个版本:`interrupt()`微软代理框架`RequestInfoEvent`云`waitForApproval()` API名称不同,形状不同.

> 每个托管代理 SDK 出货一版:长图`interrupt()`、微软代理框架`RequestInfoEvent`云`waitForApproval()`△API 名称不同;形态不。

## 概念的核心概念

### 提出,然后承诺的状态机.

1. **Propose.**代理生成一个拟议的操作. 持续到一个持久的存储器 (PostgreSQL, Redis,持久的对象). 包括:
   翻译: 中文**提议。**代理 产生提议动作──持久化到持久存储(PostgreSQL、Redis、Durable Object) 包括:
   - 意图 (为什么代理人这样做)
     中文翻译:意图(代理为什么要这样做)
   - 数据系 (该提案的来源)
     中文翻译:数据谱系 (什么源导致此提议)
   - 触及的权限 (哪些范围 / 文件 / 终点)
     中文翻译:触及的权限 (哪些范围/文件/端点)
   - 爆炸半径 (最坏情况是什么)
     中文翻译:爆炸半径 (最坏情况是什么)
   - 倒退计划 (如果已实施,我们如何撤销它)
     中文翻译:回滚计划 (如提交,如何撤销)
   - 无效关键 (每项提案均为独一无二;重新提交的记录相同)
     中文翻译:等键(每提议唯一;重提交返回同样的记录)
2. **Surface.**审查者看到所有元数据的提案. 审查者是一个人 (而不是审查自己的代理人).
   翻译: 中文**呈现。**审查员看到带所有元数据的提议――审查员是个人――不是代理自审――
3. **Commit.**确认了,行动执行了.
   翻译: 中文**提交。**正面确认――动作执行――
4. **Verify.**执行后,副作用被检查并确认. 如果验证步骤失败,系统处于已知坏状态,并启动警报.
   翻译: 中文**验证。**执行后副作用被重新确认. 如果验证步骤失败,系统处于已知坏状态并启动警报.

### 无权的关键

没有无效的关键,经过过过渡性失败的重试可以双重执行批准的行动.

> 没有等键,瞬态失败后的重试可能双倍执行已批准动作.

具体例子:用户批准"从A转移100美元到B".网络闪. 工作流再次尝试.用户批准了一次,但转移执行两次. 异能关键将批准联系到单一,独特的副作用; 第二次执行是无操作.

> 具体例:用户批准"从A 转 $100到B"――网络闪断――工作流重试――用户批准一次但转账执行两次――等键将批准绑定到单一唯一副作用;第二次执行是无-op――

对于代理批准,它被明确使用在微软代理框架文件中.

> 微软代理框架 文档明确将其复用于代理批准.

### 持久性:为什么批准比进程寿命长

通过等待室是一个代理人不拥有的状态.工作流程被暂停 (课12).`interrupt()`通过 PostgreSQL 检查点,而不是仅仅在内存状态, 两天后的批准仍然发现工作流程完整.

> 批准等候室是代理不拥有的状态――工作流暂停了――第12课)――批准到达时,工作流从该精确点恢复了――这就是为什么LangGraph将`interrupt()`两天后的批准仍在找到完整的工作流.

### 轮邮票批准和挑战和反应缓解.

默认的HITLUI ("批准" / "拒绝"按) 产生了快速的批准,没有真正的审查. 文档减轻:需要在批准按启用之前对特定问题作出积极答案的挑战和响应检查清单.

> 已记录缓解:在 批准按启动前要求对特定问题正面回答的挑战-响应清单――具体形状:

- "你知道这是什么资源吗?"
  中文翻译:"你了解这触及什么资源吗?[ ]"
- "你是否确定爆炸半径是可接受的?"
  中文翻译:"你验证了爆炸半径可接受吗?[ ]"
- "如果这失败,你有没有反弹计划吗?"
  中文翻译:"如果失败你有回滚计划吗?[ ]"

没有官僚主义本身是一个强制性功能.不能点击框的评论员要么要求澄清 (升级) 或拒绝 (安全默认).人类代理安全研究明确引用了检查清单驱动的HITL作为印批准模式的减轻.

> 不为官僚而官僚是强制函数――不能勾选框的审查员要么要求澄清,升级,拒绝,安全默认,人类特工安全研究明确引用清单驱动HITL作为缓解的皮章批准模式――

### 什么是后果的?

没有任何行动都需要提出,然后承诺.

> 没有任何动作都需要提出,然后承诺.

- **Consequential actions**无可逆的文件,金融交易,出口通信,生产数据库的变化,破坏性文件系统操作.
  翻译: 中文**后果性动作**金融交易,外发通信,生产数据库变更,破坏性文件系统操作.
- **Reversible actions**(有时HITL):编辑本地文件,阶段化变化,可逆的写作,清晰的反转.
  翻译: 中文**可逆动作**编辑:本地文件编辑,舞台 环境变更,带清晰回滚的可逆写.
- **Reads and inspections**读取文件,列出资源,调用只读取API.
  翻译: 中文**读和检查**读文件列资源调用只读API。

### 行动后验证

"提交运行"与"副作用发生"不同.网络分区和比赛条件可以产生一个认为成功的工作流程,而后端没有持续.验证步骤在提交确认后重新阅读目标资源.这是与数据库交易相同的模式.`RETURNING`条款或 AWS `GetObject`之后`PutObject`现在,我们要去.

> 网络分区和竞争条件可产生工作流以成功而后端未持续化.`RETURNING`关键词的数据库事务`PutObject`后`GetObject` AWS 的模式与此相似.

### 欧盟人工智能法第14条

根据第14条,在欧盟高风险人工智能系统的有效监督."有效"并非装饰性的.监管语言特别排除了印模式.提出,然后承诺,挑战和回应是微软代理管理工具包合规文件中保存的第14条审查的形状.

> 第14条强制欧盟高风险人工智能系统有效的人类监督――"有效"不是装饰性――监管语言明确排除皮章模式――带挑战应对的建议-然后-承诺是通过了微软代理治理工具包 合规文档中第14条审查的形式――

## 用它实现框架
```figure
mx-propose-then-commit
```

## 用它

`code/main.py`执行一个建议然后执行状态机在 stdlib Python. 持久存储是一个 JSON 文件. 无效密钥是 (thread_id, action_signature) 的哈希. 驱动程序模拟了三个情况:清洁的批准流,过渡失败后的重试 (不得执行双重),以及印默认对挑战和响应流.

> `code/main.py`用标准库 Python 实现建议然后承诺 状态机――持久存储是 JSON 文件――等键是 (thread_id, action_signature) 的哈希――驱动器模拟三例:干净批准流、瞬态失败后重试(必须不双重执行)

## 运送它.

`outputs/skill-hitl-design.md`审查拟议的HITL工作流程,以提出后承诺的形式和缺少元数据,无权,验证或挑战和响应层的标志.

> `outputs/skill-hitl-design.md`审查提议 HITL 工作流的建议-然后-承诺 形态并标记缺失的元数据、等、验证或挑战-响应层──

## 练习题

1. 跑步`code/main.py`确认批准的提案的重试使用了持久记录,而不是重复执行. 现在更改无效键,包括时间印,并显示重试双重执行.
   中文翻译:运行 `code/main.py`△确认已批准的提议重试使用持久记录且未再执行.

2. 延长提案记录`rollback`执行执行过程中验证步骤失败. 显示自动反弹.
   中文翻译:用`rollback`字段扩展提议记录──模拟验证步骤失败的执行──展示回滚自动触发──

3. 阅读微软代理框架的文章`RequestInfoEvent`文件. 识别一个元数据领域,API包括玩具机器缺失. 添加它并解释它保护什么.
   中文翻译:阅读微软代理框架的`RequestInfoEvent`文档――识别API 包含了玩具引擎缺失的一个元数据字段――添加它并解释它防止什么――

4. 设计一个特定行动的挑战和答案检查清单 (例如"发布到公共Twitter帐户").评论员必须回答哪些三个问题?为什么这三个问题?
   中文翻译:为特定动作 (例如"发到公共Twitter账号") 设计挑战-响应清单――审查员必须回答哪三个问题?为什么这三个?

5. 选择一个同步的"批准"提示 (不需要持久的存储) 足够的情况.解释原因,并列出你接受的风险类别.
   中文翻译:选一个同步"批准?"提示就足够了(不需要持久存储) 的案例──解释为什么,并命名你接受的风险类──

## 关键词 快速查找表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Propose-then-commit | "Two-phase approval" | Persisted proposal + positive commit + verify |
| Propose-then-commit | "两阶段批准" | 持久提议 + 正面提交 + 验证 |
| Idempotency key | "Retry-safe token" | Unique per proposal; second execution no-ops |
| 幂等键 | "重试安全 token" | 每提议唯一；第二次执行 no-op |
| Data lineage | "Where it came from" | The specific source content that led to the proposal |
| 数据谱系 | "它从哪来" | 导致提议的特定源内容 |
| Blast radius | "Worst case" | Scope of effect if the action goes wrong |
| 爆炸半径 | "最坏情况" | 动作出错时的影响范围 |
| Rubber-stamp | "Fast approval" | "Approve" clicked without genuine review |
| 橡皮章 | "快速批准" | 无真实审查地点击"Approve" |
| Challenge-and-response | "Forcing checklist" | Reviewer must positively acknowledge specific questions |
| 挑战-响应 | "强制清单" | 审查者必须正面确认特定问题 |
| RequestInfoEvent | "MS Agent Framework primitive" | Durable HITL request with structured metadata |
| RequestInfoEvent | "MS Agent Framework 原语" | 带结构化元数据的持久 HITL 请求 |
| `interrupt()` / `waitForApproval()` | "Framework primitives" | LangGraph / Cloudflare equivalents of the same shape |
| `interrupt()` / `waitForApproval()` | "框架原语" | 相同形态的 LangGraph / Cloudflare 等价物 |

## 继续阅读 继续阅读

- [Microsoft Agent Framework — Human in the loop](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) `RequestInfoEvent`经过长期的批准.
  翻译: 中文`RequestInfoEvent`持久批准.
- [Cloudflare Agents — Human in the loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/) `waitForApproval()`它们是可靠的.
  翻译: 中文`waitForApproval()`和耐用物体――
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy)HITL作为缓解长远风险.
  中文翻译:HITL 作为长程风险缓解.
- [EU AI Act — Article 14: Human oversight](https://artificialintelligenceact.eu/article/14/)高风险系统的监管基准.
  中文翻译:高风险系统的监管基线――
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) 关于监督的宪法框架.
  中文翻译:监督的宪法框架.
