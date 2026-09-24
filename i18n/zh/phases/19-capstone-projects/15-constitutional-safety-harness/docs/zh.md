# 宪法规则 结业 线束安全

> 对于多语言覆盖,Anthropic的宪法分类器,Meta的Llama Guard4,谷歌的ShieldGemma-2,NVIDIA的Nemotron 3内容安全,以及X-Guard定义了2026年安全分类器堆. 格拉克,Pyrit,NVIDIA Aegis和 promptfoo成为标准的对抗评估工具. 尼莫防护车的0.12将它们连接到生产管道. 这块顶石将所有这些东西结合在一起:一个围绕目标应用程序的层次安全带,一个自主的红团队代理运行6多个攻击家庭,

> **【中文解读】**本节是综合项目,构建宪法安全线束.


**Type:** Capstone | **类型:** Capstone
**Languages:** Python (safety pipeline, red team), YAML (policy configs) | **语言:** Python (safety pipeline, red team), YAML (policy configs)
**Prerequisites:** Phase 10 (LLMs from scratch), Phase 11 (LLM engineering), Phase 13 (tools), Phase 14 (agents), Phase 18 (ethics, safety, alignment)

>  **【前置】**顶点项目 15 = 综合阶段 10/11/13/14/18──宪法安全线束+红队场 = 综合阶段 18 所有安全工具的实战──
>  **【类比】**安全线束 = "AI 应用的安全带+气囊"──2026 分类器:人类宪法分类器+Llama Guard 4+Google ShieldGemma-2+NVIDIA Nemotron 3+X-Guard(多语言)──红队工具:garak/PyRIT/NVIDIA Aegis/promptfoo──NeMo Guardrails v0.12 串起来──要求:分层守护+主红队(6+家族攻击) +宪法自评产生可测无害性三角洲──**前置知识:**阶段10 (从零开始的LLM),阶段11 (LLM工程),阶段13 (工具),阶段14 (代理人),阶段18 (道德,安全,配合)
**Phases exercised:**现在,我们在这个世界里,**涉及阶段:**子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子
**Time:** 25 hours | **时间:** 25 hours

## 问题 问题引入

> **【中文解读】**本节描述了LLM安全防护的核心挑战.2026年前沿的问题不是分类器是否有效,而是如何正确组合它们不过拒绝也不留下明显漏洞.

> **【拓展：对抗性攻击工具生态】**2026年标准化攻击工具:garak(LLM安全扫描器) ‧PyRIT(微软红队框架) ‧快foo(提示注入测试) ‧NVIDIA Aegis(企业安全评估) ‧攻击家族包括:PAIR/TAP(自动越狱发现) ‧GCG(梯度后攻击) ‧ASCII/base64/rot13 编码攻击、多轮攻击(人格采纳/记忆利用) ‧语码转换攻击(混合英语与斯瓦希里语或泰语) ‧每次红队运行产出CVSS 评分的结构化发现文件.

2026年LLM安全的边界不是分类器是否工作 (大概是这样做的),而是如何在生产应用程序周围正确地编译它们, 拉马卫队4处理英国政策违规行为. 据悉,在此期间, 根据图像,ShieldGemma-2可以捕获即时注射. 公司的内容安全性 类的宪法分类器是训练而不是服务期间使用的单独方法.

> 2026年LLM安全的最重要问题不是分类器是否能工作 (大概是这样做的),而是如何在生产应用程序周围正确地编译它们, 拉马卫队4处理英国政策违规行为. 据悉,在此期间, 根据图像,ShieldGemma-2可以捕获即时注射. 公司的内容安全性 类的宪法分类器是训练而不是服务期间使用的单独方法.


攻击进化也很重要. PAIR 和 TAP 自动化了 jailbreak 发现. GCG 运行基于梯度的后音攻击.多转和代码交换攻击利用了代理记忆.任何部署的LLM 需要红队范围.

> 进化攻击也是重要的.


您将硬化目标应用程序 (要么是8B指令调整的模型,要么是其他顶点的RAG聊天机器人之一),对此运行6+攻击家庭,并进行前后无害度测量.

> 你将硬化目标应用程序 (要么是8B指令调整的模型,要么是其他顶点的RAG聊天机器人之一),对其进行6+攻击家庭,并进行前/后的无害性测量.


## 概念的核心概念

> **【中文解读】**安全管道分五层:输入净化(去零宽字符、解码基础64/rot13、Unicode 规范化)→ 策略层(NeMo Guardrails v0.12 策略护)→ 分类器门控(Llama Guard 4 输入/X-Guard 非英文/ShieldGemma-2 图像)→ 目标模型 → 输出过(Llama Guard 4 输出/Presidio PII 脱敏/引用强制) ――高风险输出进入 Slack 人工队列列。宪法自审是训练时 →干干:1000 条 有害尝试 → 模型起草 根据宪法自审预训 重量,测量前后无害性差异──

> **【拓展：Constitutional AI 方法】**人类的宪法人工智能方法在训练中嵌入安全原则 (无害规则),而不是仅仅在推理时过──红队测试发现,多层组合防护输入净化+策略护+分类器门控+输出过) 与单层防护效果提高了40-60%.

安全管道是五层.**Input sanitize**解码的基本64/rot13字符,规范 Unicode.**Policy layer**:NeMo Guardrails v0.12轨道 (域外,毒性,PII提取). **Classifier gate**,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,**Model**目标法定士**Output filter**关4号号, 检查, 报名执行, 应有的情况.**HITL tier**标记高风险的输出进入 Slack 队列.

> 安全管道是五层.**Input sanitize**解码的基本64/rot13字符,规范 Unicode.**Policy layer**:NeMo Guardrails v0.12轨道 (域外,毒性,PII提取). **Classifier gate**,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,**Model**目标法定士**Output filter**关4号号, 检查, 报名执行, 应有的情况.**HITL tier**标记高风险的输出进入 Slack 队列.


红队范围运行在一个调度器上. PAIR 和 TAP 自主地发现 jailbreaks. GCG运行基于梯度的后音攻击. ASCII / base64 / rot13编码攻击.多转攻击 (个人采用,内存利用).代码交换攻击 (混合英语和斯瓦希利或泰语).每个运行产生一个结构化的发现文件,CVSS得分和披露时间表.

> 红团队范围在调度器上运行. PAIR 和 TAP 自主地发现 jailbreaks. GCG运行基于梯度的后音攻击. ASCII / base64 / rot13编码攻击.多转攻击 (个人采用,内存利用).代码交换攻击 (混合英语和斯瓦希利或泰语).每个运行产生一个结构化的发现文件,CVSS得分和披露时间表.


宪法自我批评是训练时间干预. 采取1k的有害尝试提示,让模型起草答案,对书面宪法 (不要伤害规则) 进行批评,并在批评循环上重新训练. 在持久的评估中测量之前/后的无害性三角形.

> 宪法自我批评是训练时间干预. 采取1k的有害尝试提示,让模型草案作出反应,对书面宪法 (不要伤害规则) 进行批评,并在批评循环上重新训练. 在持久的评估中测量前/后无害性三角形.


## 建筑,建筑

```
request (text / image / multilingual)
      |
      v
input sanitize (strip zero-width, decode, normalize)
      |
      v
NeMo Guardrails v0.12 rails (off-domain, policy)
      |
      v
classifier gate:
  Llama Guard 4 (English)
  X-Guard (multilingual, 132 langs)
  ShieldGemma-2 (image prompts)
  Nemotron 3 Content Safety (enterprise)
      |
      v (allowed)
target LLM
      |
      v
output filter: Llama Guard 4 + Presidio PII + citation check
      |
      v
HITL tier for flagged outputs

parallel:
  red-team scheduler
    -> garak (classic attacks)
    -> PyRIT (orchestrated red team)
    -> autonomous jailbreak agent (PAIR + TAP)
    -> GCG suffix attacks
    -> multilingual / code-switch
    -> multi-turn persona adoption

output: CVSS-scored findings + disclosure timeline + before/after harmlessness delta
```

##  技术

- 安全分类:Llama Guard 4,ShieldGemma-2,NVIDIA Nemotron 3 内容安全,X-Guard
  中文翻译:安全分类:拉马卫队4,盾牌Gemma-2,NVIDIANemotron3内容安全,X-Guard
- 防护轨道框架:NeMo防护轨道 v0.12 + OPA
  中文翻译:护卫框架:NeMo Guardrails v0.12 + OPA
- 红团队驱动程序:garak (NVIDIA),PyrIT (Microsoft Azure),NVIDIA Aegis, promptfoo
  中文翻译:红团队驱动程序:garak (NVIDIA),PyrIT (Microsoft Azure),NVIDIA Aegis, promptfoo
- 监狱突破剂:PAIR (Chao等人, 2023),攻击树 (TAP),GCG后
  中文翻译:入狱代理:PAIR (Chao等, 2023),攻击树 (TAP),GCG后
- 宪法培训:人类式的自我批评循环 + 批评的SFT
  中文翻译:宪法训练:人类风格的自我批评循环 + 批评的SFT
- 标签: 总统
  中文翻译:PII 清除: 普雷西迪奥
- 目标:一个8B指令调整的模型或其他顶点石的RAG聊天机器人
  中文翻译:目标:一个8B指令调整的模型或其他顶点的RAG聊天机器人之一

## 动手构建

> **【中文解读】**构建宪法安全测试线束:对待测试模型 (?? 八B 指令微调模型或RAG 聊天机器人) 运行 10 类攻击 (?? 狱,提示注入,数据泄露,幻觉,偏见,毒性,版权,隐私,拒绝合法请求和可用性退化),每类 20 个测试用例,共 200 个测试. 通过 6 个指标评估:拒绝率,误拒率,泄露率,毒性分数,偏见分数和可用性退化.

> **【拓展：AI 安全评估在 2026 年的标准化进展】**根据"人类自残等级"的标准测试集,人工智能 (AI) 应对自残等级的标准测试集. 基于预设原则,人工智能 (AI) 应对自评和修改输出.
```figure
cf-safety-stack
```

## 建立它

1. **Target setup.**在vLLM上建立一个8B指令调整模型 (或从另一个顶石中重新使用RAG聊天机器人).这是正在测试的应用程序.
   中文翻译:1. **Target setup.**在vLLM上建立一个8B指令调整模型 (或从另一个顶石中重新使用RAG聊天机器人).这是正在测试的应用程序.

2. **Safety pipeline wrap.**导线在目标周围的五层管道. 检查每个层是个别可观测的 (在Langfuse中每个层的跨度).
   翻译: 翻译:**Safety pipeline wrap.**导线在目标周围的五层管道. 检查每个层是个别可观测的 (在Langfuse中每个层的跨度).

3. **Classifier coverage.**装载Llama Guard 4,X-Guard (多语言),ShieldGemma-2 (图片). 运行每个小标记的集,以建立基线.
   翻译: 翻译:**Classifier coverage.**装载Llama Guard 4,X-Guard (多语言),ShieldGemma-2 (图片). 运行每个小标记的集,以建立基线.

4. **Red-team scheduler.**计划加拉克,Pyrit,一个PAIR代理,一个TAP代理,一个GCG运行者,一个多轮攻击者,一个代码交换者攻击者.
   翻译: 翻译:**Red-team scheduler.**计划加拉克,Pyrit,一个PAIR代理,一个TAP代理,一个GCG运行者,一个多轮攻击者,一个代码交换者攻击者.

5. **Attack suite.**攻击家族: (1) PAIR自动 jailbreak, (2) TAP tree-of-attacks, (3) GCG梯度后, (4) ASCII/base64/rot13编码, (5) 多转型人格, (6) 多语言代码交换. 每个家庭报告成功率.
   翻译: 五.**Attack suite.**攻击家族: (1) PAIR自动 jailbreak, (2) TAP tree-of-attacks, (3) GCG梯度后, (4) ASCII/base64/rot13编码, (5) 多转型人格, (6) 多语言代码交换. 每个家庭报告成功率.

6. **Constitutional self-critique.**监督1k的危害试图提示.每个目标都起草了一个反应.一个批评者LLM评价一个书面宪法 ("不要伤害","引用证据","拒绝非法请求").指导评论对象被重写;目标对批评改善的对进行细节调整.在进行的评估中测量之前/之后无害性.
   翻译: 七个字**Constitutional self-critique.**监督1k的危害试图提示.每个目标都起草了一个反应.一个批评者LLM评价一个书面宪法 ("不要伤害","引用证据","拒绝非法请求").指导评论对象被重写;目标对批评改善的对进行细节调整.在进行的评估中测量之前/之后无害性.

7. **Over-refusal measurement.**检测良性提示套件 (例如XSTest) 上的错误阳性率. 目标必须在良性问题上保持有用.
   翻译:7.**Over-refusal measurement.**检测良性提示套件 (例如XSTest) 上的错误阳性率. 目标必须在良性问题上保持有用.

8. **CVSS scoring.**对于每次成功的 jailbreak,评分 CVSS 4.0 (攻击向量,复杂性,影响). 制作披露时间表和缓解计划.
   翻译:8.**CVSS scoring.**对于每次成功的 jailbreak,评分 CVSS 4.0 (攻击向量,复杂性,影响). 制作披露时间表和缓解计划.

9. **Range automation.**上面的一切都运行在 cron 上; 结果写到队列上; 过度拒绝回归警告到 Slack 上.
   翻译:9.**Range automation.**上面的一切都运行在 cron 上; 结果写到队列上; 过度拒绝回归警告到 Slack 上.

## 用它使用方法

```
$ safety probe --model=target --family=PAIR --budget=50
[attacker]   PAIR agent running on target
[attack]     attempt 1/50: disguise query as academic research ... blocked
[attack]     attempt 2/50: appeal to roleplay ... blocked
[attack]     attempt 3/50: chain-of-thought coax ... SUCCEEDED
[finding]    CVSS 4.8 medium: roleplay bypass on target
[range]      7 successes out of 50 (14% success rate)
```

## 发射上线

`outputs/skill-safety-harness.md`产品可交付.生产级层级的安全管道加上可复制的红色车队范围,具有前/后无害度.

> `outputs/skill-safety-harness.md`是交付物品.生产级层级的安全管道加上可复制的红色车队范围,具有前/后无害度.


| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | Attack-surface coverage | 6+ attack families exercised, 2+ languages |
| 20 | True-positive / false-positive trade-off | Attack block rate vs XSTest benign pass rate |
| 20 | Self-critique delta | Before/after harmlessness on held-out eval |
| 20 | Documentation and disclosure | CVSS-scored findings with timeline |
| 15 | Automation and repeatability | Everything runs on cron with alerts |
| **100** | | |

## 练习题

1. 运行garak的插件,即将在RAG聊天机器人中注射,并与输出过层和没有输出过器层进行攻击成功率的比较.

2. 增加第七次攻击家族:通过检索文件间接即时注射.

3. 执行"拒绝与帮助"模式:当防护堵塞时,目标提供更安全的相关答案,而不是平坦的拒绝.

4. 多语言覆盖率差距:找到X-Guard低性能的语言. 提出针对它进行细节调整的数据集.

5. 根据30B模型进行宪法自我批评,

## 关键词 关键词

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Layered safety | "Defense in depth" | Multiple guardrails at input, gate, output, HITL |
| Llama Guard 4 | "Meta's safety classifier" | The 2026 reference input/output content classifier |
| PAIR | "Jailbreak agent" | Paper (Chao et al.) on LLM-driven jailbreak discovery |
| TAP | "Tree-of-Attacks" | Tree-search variant of PAIR |
| GCG | "Greedy coordinate gradient" | Gradient-based adversarial suffix attack |
| Constitutional self-critique | "Anthropic-style training" | Target drafts -> critic scores -> rewrite -> retrain |
| XSTest | "Benign probe set" | Benchmark for over-refusal regression |
| CVSS 4.0 | "Severity score" | Standard vulnerability scoring for safety findings |

## 继续阅读 继续阅读

- [Anthropic Constitutional Classifiers](https://www.anthropic.com/research/constitutional-classifiers)培训时间参考
- [Meta Llama Guard 4](https://www.llama.com/docs/model-cards-and-prompt-formats/llama-guard-4/)2026年输出输入分类器
- [Google ShieldGemma-2](https://huggingface.co/google/shieldgemma-2b)图像+多模安全
- [NVIDIA Nemotron 3 Content Safety](https://developer.nvidia.com/blog/building-nvidia-nemotron-3-agents-for-reasoning-multimodal-rag-voice-and-safety/)企业参考
- [X-Guard (arXiv:2504.08848)](https://arxiv.org/abs/2504.08848) 132 种语言的多语言安全
- [garak](https://github.com/NVIDIA/garak)NVIDIA红队工具包
- [PyRIT](https://github.com/Azure/PyRIT)微软红团框架
- [NeMo Guardrails v0.12](https://docs.nvidia.com/nemo-guardrails/)铁路框架
- [PAIR (arXiv:2310.08419)](https://arxiv.org/abs/2310.08419) 监狱突破代理文件
