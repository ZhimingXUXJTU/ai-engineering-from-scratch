# 卡普斯通17 个人人工智能导师 (适应性,多模态,具有记忆力) 更多模态 结业 个人 记忆 导师

> 米戈 (汗学院),杜林戈马克斯,教育谷歌学习LM/双胞胎,奇威letQ-聊天,和合成导师都在2026年提供了适应性多模式导师. 常见的形式是苏格拉底政策 (永远不要只是抛弃答案),学习者模型每次交互后都会更新 (贝叶斯知识追踪风格),语音+文字+照片数学输入,课程图图检索,间隔重复计划和适合年龄的安全过器. 终点是向专科的导师 (K-12代数或Python引入),与10名学习者进行两周的有效性研究,并通过内容安全审计.

> **【中文解读】**本节是综合项目 构建个人人工智能导师系统.


**Type:** Capstone | **类型:** Capstone
**Languages:** Python (backend, learner model), TypeScript (web app), SQL (curriculum graph via Postgres + Neo4j) | **语言:** Python (backend, learner model), TypeScript (web app), SQL (curriculum graph via Postgres + Neo4j)
**Prerequisites:** Phase 5 (NLP), Phase 6 (speech), Phase 11 (LLM engineering), Phase 12 (multimodal), Phase 14 (agents), Phase 17 (infrastructure), Phase 18 (safety)

>  **【前置】**顶点项目 17 = 综合阶段 5/6/11/12/14/17/18──个人人工智能导师 = 汉米戈 / 杜灵戈马克斯 / 学习LM / 问卷 Q-Chat / 合成导师──
>  **【类比】**导师: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 专题: 题: 专题: 题: 题: 题: 题: 题:**前置知识:**五阶段 (NLP),六阶段 (演讲),十一阶段 (LLM工程),十二阶段 (多元),十四阶段 (代理人),十七阶段 (基础设施),十八阶段 (安全)
**Phases exercised:**现在,我们在这个世界里,**涉及阶段:**五·六·十一·十二·十四·十七·十八
**Time:** 30 hours | **时间:** 30 hours

## 问题 问题引入

> **【中文解读】**本节描述自适应辅导AI的核心挑战――2026年自适应辅导已从教育技术研究走向消费产品――共同要素:多模态输入 (打字/语音/拍照方程式) 苏格兰教学法 (先提问再讲解) ‧每次交互后更新的学习者模型、严格的年龄适宜安全过──核心挑战是有效性验证需要10名学习者两周前测/后测效研究――

> **【拓展：AI 教育产品生态】**2026年主要人工智能教育产品:Khanmigo(Khan Academy,覆盖美国大部分学区) 杜灵戈马克斯 (Duolingo Max) 几千万MAU) 谷歌学习LM/双胞胎教育 (集成谷歌课堂) 查询Q聊天、合成导师 (面向好奇心儿童) 语音交互复复用LiveKit + 微笑 技术(Capstone 03),数学拍照输入使用dots.ocr或PaliGemma 2――COPPA (儿童在线隐私保护法) 要求严格的记忆保留策略和内容安全过.

适应教学曾经是科技研究领域的位. 到2026年,它将成为消费品. 美国大多数学校都部署了Khanmigo. 杜灵戈马克斯打了数亿的MAU. 谷歌的学习LM/双子座教育功能在谷歌课堂教学. 问卷Q-Chat坐在卡片旁边. 导师与导师为好奇的孩子们的传播. 共同的元素:多模式输入 (类型,讲话,摄影方程),苏格拉底教学 (先问,后解释),每次互动后更新的学习模型,以及严格的适合年龄的安全.

> 适应教学曾经是科技研究领域的位.


测量是实际有效性研究:测试前和测试后两周的成绩,包括10名学习者.语音循环必须感觉自然 (Capstone 03子堆).记忆必须尊重隐私.安全过器必须通过Coppa意识的红队K-12.

> 你将为特定群体构建一个.测量是实际的有效性研究:测试前和测试后两周的成绩与10名学习者.语音循环必须感觉自然 (Capstone 03子堆).记忆必须尊重隐私.安全过器必须通过COPA意识的红队K-12.


## 概念的核心概念

> **【中文解读】**四大组件:辅导策略(苏格兰底循环学习者求答时反问引导问题,答对后推进下一概念,卡住时提供脚手架提示) 学习者模型(贝叶斯知识追踪,每次交互后更新课节的掌握概率) 课程图谱(Neo4j 中概念与先修关系图,策略沿图选择下一概念) 记忆节+语义存储,保存互联历史和偏好) 安全使用Llama Guard 4 + 年龄适合过器 + COPPA 记忆保留策略──

> **【拓展：贝叶斯知识追踪与效果研究】**贝叶斯知识追踪(BKT) 是自适应学习的基础模型,为每个技能节点维护掌握概率 P(L),根据学习者回答(正确/错误) 和猜测/失误参数更新。现代变体包括深度知识追踪(DKT) 和自适应知识追踪(AKT) ――效果研究设计:10 名学习者,前测→两周自适应辅导→后测,报告学习增长和置信区应应间, delta与非自适基线间(同样的内容线性交付) 对比.

它们有四个组成部分.**Tutor policy**学生问答时,政策提出一个主要问题;当他们正确地理解时,它转向下一个概念;当他们陷入困境时,它提供了一个架的提示. **Learner model**是贝叶斯知识追踪 (或简单的变体) 每次交互后更新每一个课程节点的掌握概率. **Curriculum graph**对于一个概念的定义,该概念的定义是:**Memory**是一个节目式+语义存储 (代理记忆式) 包含过去的互动,错误和偏好.

> 它们有四个组成部分.


通过Dots.ocr或PaliGemma进行数学问题的照片输入.通过Cartesia Sonic-2进行语音输出.安全使用Llama Guard 4加上年龄适当的过器 (阻止成人内容,暴力,自伤) 和COPPA意识的记忆保留政策.

> 通过Dots.ocr或PaliGemma进行图像输入.通过Cartesia Sonic-2进行语音输出.安全使用Llama Guard 4加上年龄适当的过器 (阻止成人内容,暴力,自伤) 和COPPA意识的记忆保留政策.


效率研究是可交付的. 10名学习者,试验前和试验后,两周.报告学习增长的特拉和信心间隔.与非适应的基线 (不需要导师政策的线性内容) 进行比较.

> 是交付物品.


## 建筑,建筑

```
learner device
  |
  +-- text         -> web app
  +-- voice        -> LiveKit Agents (ASR + TTS)
  +-- photo math   -> dots.ocr / PaliGemma 2
       |
       v
  tutor policy (LangGraph)
       - Socratic decision head
       - next-concept chooser (curriculum graph walk)
       - hint scaffolder
       - mastery update
       |
       v
  learner model (BKT / item-response theory)
       - per-concept mastery probability
       - spaced-repetition scheduler (SM-2 or FSRS)
       |
       v
  memory (agentmemory-style)
       - episodic: every interaction
       - semantic: learned mistakes, preferences
       - retention policy: COPPA / GDPR aware
       |
       v
  curriculum graph (Neo4j)
       - prerequisite edges
       - OER content attached
       |
       v
  safety:
    Llama Guard 4 + age-appropriate filter
    memory access guarded by learner ID scope
```

##  技术

- 选择主题:K-12代数或Python介绍 (选择一个深度)
  中文翻译:主题选择:K-12代数或介绍Python (选择一个为深度)
- 导师政策:LangGraph与Claude Sonnet 4.7 (即时缓存)
  中文翻译:教师政策: 长图对克劳德·索尼特4.7 (随即缓存)
- 学习者模型:贝耶斯知识追踪 (经典) 或FSRS用于间隔
  中文翻译:学习者模型:贝叶斯知识追踪 (经典) 或FSRS用于间隔
- 课程图:概念的新4j+先决条件边缘+OER内容
  中文翻译:课程图:概念的Neo4j+先决条件边缘+OER内容
- 记忆:代理记忆式持久向量+剧情+语义存储
  中文翻译:记忆:代理记忆式持久向量 + 剧情 + 语义存储
- 声音:LiveKit代理 1.0 +卡特西亚索尼克-2 (重复使用的底石03子堆)
  中文翻译:声音:LiveKit代理 1.0 +卡特西亚索尼克-2 (重复使用底石03子堆)
- 图形数学:dots.ocr或PaliGemma 2用于识别方程
  中文翻译:图片数学:dots.ocr或PaliGemma 2用于识别方程
- 安全:Llama Guard 4+适合年龄的定制过器
  中文翻译:安全:拉马卫队4+适合年龄的自定义过器
- 率:率问题生成,测试前/后使用,有效性研究工具
  中文翻译:Eval: 芽级问题生成,前/后测试使用,有效性研究工具

## 动手构建

> **【中文解读】**构建个人 AI 导师系统:课程知识图谱(50-150个概念节点 + 前置依边) 知识诊断测试(项目反应理论IRT 模型评估学生水平) 个人化学习路径(基于诊断结果图遍历) 多模态解释生成(文本+图表+代码示例) 间隔重调度和 Bloom 分类法问题生成――

> **【拓展：AI 教育在 2026 年的突破】**汉学院的汉密戈、杜林戈的AI辅导员、课程的AI学习助手都采用类似架构──关键创新:1)IRT(物件响应理论) 模型精准定位学生知识盲区;2) 芽 分类法确保问题覆盖记忆/理解/应用/分析/评价/创造六层次;3) 间隔重复算法(Anki风格) 优化长期记忆保持率――Meta 2025年研究显示,AI辅导员将提高学习效率约30%,但完全自主 AI 导师在情绪支持和动机维护方面仍然不足.
```figure
cf-tutor-loop
```

## 建立它

1. **Curriculum graph.**构建一个由50-150个概念节点组成的Neo4j (例如,从"数线"到"方程公式"的K-12代数) 具有先决条件边缘. 附加每个节点的OER内容 (Open Textbook, OpenStax).
   中文翻译:1. **Curriculum graph.**构建一个由50-150个概念节点组成的Neo4j (例如,从"数线"到"方程公式"的K-12代数) 具有先决条件边缘. 附加每个节点的OER内容 (Open Textbook, OpenStax).

2. **Learner model.**开始使用先例来追踪贝耶斯知识:猜测,滑动,学习速度. 每次交互后更新每个概念的掌握. 持续每个学习者.
   翻译: 翻译:**Learner model.**开始使用先例来追踪贝耶斯知识:猜测,滑动,学习速度. 每次交互后更新每个概念的掌握. 持续每个学习者.

3. **Tutor policy.**带节点的长图: `read_signal`(学习者的答案是否正确/部分/固?),`select_concept`(步行课程图选择最优先概念),`scaffold`现在,我们需要一个人来帮助我们.`update_mastery`现在,我们要去.
   翻译: 翻译:**Tutor policy.**带节点的长图: `read_signal`(学习者的答案是否正确/部分/固?),`select_concept`(步行课程图选择最优先概念),`scaffold`现在,我们需要一个人来帮助我们.`update_mastery`现在,我们要去.

4. **Memory.**任何交互都会写到一个剧情商店. 错误和偏好促进语义记忆. COPPA 意识到保留政策:自动删除1年后,可以访问父母.
   翻译: 翻译:**Memory.**任何交互都会写到一个剧情商店. 错误和偏好促进语义记忆. COPPA 意识到保留政策:自动删除1年后,可以访问父母.

5. **Voice path.**通过Whisper-v3-turbo.TTS通过Cartesia Sonic-2. 支持轮 (重复使用 capstone 03 机械).
   翻译: 五.**Voice path.**通过Whisper-v3-turbo.TTS通过Cartesia Sonic-2. 支持轮 (重复使用 capstone 03 机械).

6. **Photo-math path.**运行dots.ocr或PaliGemma 2以识别方程; 输送给导师作为结构化输入.
   翻译: 七个字**Photo-math path.**运行dots.ocr或PaliGemma 2以识别方程; 输送给导师作为结构化输入.

7. **Safety.**每个模型输出都通过了Llama Guard 4 + 适合年龄的过器 (阻止自伤,成人内容,暴力).学习者ID的内存访问范围;删除的父母访问表面.
   翻译:7.**Safety.**每个模型输出都通过了Llama Guard 4 + 适合年龄的过器 (阻止自伤,成人内容,暴力).学习者ID的内存访问范围;删除的父母访问表面.

8. **Efficacy study.**10名学习者,预测 (30个标准问题基础),两周的导师互动 (3个会议/周),测试后.
   翻译:8.**Efficacy study.**10名学习者,预测 (30个标准问题基础),两周的导师互动 (3个会议/周),测试后.

9. **Weekly progress reports.**根据学习者,自动生成已探讨的主题,掌握轨迹和建议的下一步的PDF总结.
   翻译:9.**Weekly progress reports.**根据学习者,自动生成已探讨的主题,掌握轨迹和建议的下一步的PDF总结.

## 用它使用方法

```
learner: "I don't understand why 3x + 6 = 12 means x = 2"
[signal]   stuck
[concept]  'isolating variables' (prerequisite: addition-subtraction-equality)
[scaffold] "what number would you subtract from both sides to start?"
learner: "6"
[signal]   correct
[mastery]  addition-subtraction-equality: 0.62 -> 0.77
[concept]  continue 'isolating variables'
[scaffold] "great. now what is 3x / 3 equal to?"
```

## 发射上线

`outputs/skill-ai-tutor.md`具有多模式输入,学习模型,记忆,安全性和测量效率的专科特定适应教师.

> `outputs/skill-ai-tutor.md`是交付物. 一个专科特定的适应教师,具有多模式输入,学习模型,记忆,安全性和测量效率.


| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | Learning gain delta | Pre/post-test delta in a 10-learner two-week study |
| 20 | Socratic fidelity | Rubric score on transcript samples |
| 20 | Multimodal UX | Voice + photo + text coherence end to end |
| 20 | Safety + privacy posture | Llama Guard 4 pass rate + COPPA-aware retention |
| 15 | Curriculum breadth and graph quality | Concept coverage + prerequisite graph consistency |
| **100** | | |

## 练习题

1. 运行有效性研究,无论是没有适应性学习者模型 (随机概念顺序).报告 delta. 预计适应性赢得,但大小是有趣的数字.

2. 添加多模特探测器:相同的概念问题作为文字,声音和照片. 测量学习者是否更快地与他们喜欢的模式相结合.

3. 建立一个主题仪表板:练习的主题,掌握轨迹,即将推出的概念,安全事件 (任何防护车道.

4. 增加语言交换模式:导师接受西班牙语输入,并以西班牙语教学.

5. 强调记忆隐私:验证学习者A即使通过语音录像重新摄入攻击,也无法看到学习者B的数据.记录访问尝试和警报.

## 关键词 关键词

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Socratic policy | "Ask, do not dump" | Tutor asks a leading question rather than giving the answer |
| Bayesian knowledge tracing | "BKT" | Classic learner-model equations for mastery probability per concept |
| FSRS | "Free Spaced Repetition Scheduler" | 2024 spaced-repetition scheduler, better than SM-2 |
| Curriculum graph | "Concept DAG" | Neo4j of concepts with prerequisite edges |
| Episodic memory | "Per-interaction log" | Every interaction stored for later retrieval |
| Semantic memory | "Learned pattern store" | Compacted mistakes and preferences promoted from episodic |
| COPPA | "Kids privacy law" | US law restricting data collection from children under 13 |

## 继续阅读 继续阅读

- [Khanmigo (Khan Academy)](https://www.khanmigo.ai)参考消费者K-12教师
- [Duolingo Max](https://blog.duolingo.com/duolingo-max/)参考语言学习教师
- [Google LearnLM / Gemini for Education](https://blog.google/technology/google-deepmind/learnlm)托管的参考模型
- [Quizlet Q-Chat](https://quizlet.com)替代参考
- [Synthesis Tutor](https://www.synthesis.com)创业参考
- [FSRS algorithm](https://github.com/open-spaced-repetition/fsrs4anki)间隔重复时间表
- [Bayesian Knowledge Tracing](https://en.wikipedia.org/wiki/Bayesian_knowledge_tracing)学习者模型经典
- [LiveKit Agents](https://github.com/livekit/agents)语音堆
