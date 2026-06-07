# Capstone 17 — Personal AI Tutor (Adaptive, Multimodal, with Memory) | 多模态 结业 个人 记忆 导师

> Khanmigo (Khan Academy), Duolingo Max, Google LearnLM / Gemini for Education, Quizlet Q-Chat, and Synthesis Tutor all shipped adaptive multimodal tutoring at scale in 2026. The common shape is a Socratic policy (never just dump the answer), a learner model that updates after every interaction (Bayesian knowledge tracing style), voice + text + photo-math input, curriculum graph retrieval, spaced-repetition scheduling, and hard safety filters for age-appropriate content. The capstone is to ship a subject-specific tutor (K-12 algebra or intro Python), run a two-week efficacy study with 10 learners, and pass a content-safety audit.

> **【中文解读】** 本节是综合项目——构建个人 AI 导师系统。


**Type:** Capstone | **类型:** Capstone
**Languages:** Python (backend, learner model), TypeScript (web app), SQL (curriculum graph via Postgres + Neo4j) | **语言:** Python (backend, learner model), TypeScript (web app), SQL (curriculum graph via Postgres + Neo4j)
**Prerequisites:** Phase 5 (NLP), Phase 6 (speech), Phase 11 (LLM engineering), Phase 12 (multimodal), Phase 14 (agents), Phase 17 (infrastructure), Phase 18 (safety) | **前置知识:** Phase 5 (NLP), Phase 6 (speech), Phase 11 (LLM engineering), Phase 12 (multimodal), Phase 14 (agents), Phase 17 (infrastructure), Phase 18 (safety)
**Phases exercised:** P5 · P6 · P11 · P12 · P14 · P17 · P18 | **涉及阶段:** P5 · P6 · P11 · P12 · P14 · P17 · P18
**Time:** 30 hours | **时间:** 30 hours

## Problem | 问题引入

> **【中文解读】** 本节描述自适应辅导 AI 的核心挑战。2026 年自适应辅导已从教育技术研究走向消费产品。共同要素：多模态输入（打字/语音/拍照方程式）、苏格拉底教学法（先提问再讲解）、每次交互后更新的学习者模型、严格的年龄适宜安全过滤。核心挑战是有效性验证——需要 10 名学习者的两周前测/后测效果研究。

> **【拓展：AI 教育产品生态】** 2026 年主要 AI 教育产品：Khanmigo（Khan Academy，覆盖美国大部分学区）、Duolingo Max（数千万 MAU）、Google LearnLM/Gemini for Education（集成 Google Classroom）、Quizlet Q-Chat、Synthesis Tutor（面向好奇心儿童）。语音交互复用 LiveKit + Whisper 技术栈（Capstone 03），数学拍照输入使用 dots.ocr 或 PaliGemma 2。COPPA（儿童在线隐私保护法）要求严格的记忆保留策略和内容安全过滤。

Adaptive tutoring used to be an ed-tech research niche. By 2026 it is a consumer product. Khanmigo is deployed across most US school districts. Duolingo Max hit tens of millions of MAUs. Google's LearnLM / Gemini for Education powers tutoring in Google Classroom. Quizlet Q-Chat sits alongside flashcards. Synthesis Tutor hit virality with tutor-for-curious-kids. The common elements: multimodal input (type, speak, photograph equations), Socratic pedagogy (ask first, explain later), a learner model that updates after each interaction, and strict age-appropriate safety.

> Adaptive tutoring used to be an ed-tech research niche.


You will build one of these for a specific cohort. The measurement bar is an actual efficacy study: pre-test and post-test scores over two weeks with 10 learners. The voice loop must feel natural (capstone 03 sub-stack). The memory must be privacy-respecting. The safety filter must pass COPPA-aware red-team for K-12.

> 你will build one of these for a specific cohort. The measurement bar is an actual efficacy study: pre-test and post-test scores over two weeks with 10 learners. The voice loop must feel natural (capstone 03 sub-stack). The memory must be privacy-respecting. The safety filter must pass COPPA-aware red-team for K-12.


## Concept | 核心概念

> **【中文解读】** 四大组件：辅导策略（苏格拉底循环——学习者求答案时反问引导问题，答对后推进下一概念，卡住时提供脚手架提示）、学习者模型（贝叶斯知识追踪，每次交互后更新课程节点的掌握概率）、课程图谱（Neo4j 中概念与先修关系图，策略沿图选择下一概念）、记忆（情节+语义存储，保存交互历史和偏好）。安全使用 Llama Guard 4 + 年龄适宜过滤器 + COPPA 记忆保留策略。

> **【拓展：贝叶斯知识追踪与效果研究】** 贝叶斯知识追踪（BKT）是自适应学习的基础模型，为每个技能节点维护掌握概率 P(L)，根据学习者回答（正确/错误）和猜测/失误参数更新。现代变体包括深度知识追踪（DKT）和自适应知识追踪（AKT）。效果研究设计：10 名学习者，前测→两周自适应辅导→后测，报告学习增益 delta 和置信区间，与非自适应基线（相同内容线性交付）对比。

Four components. **Tutor policy** is a Socratic loop: when the learner asks for the answer, the policy asks a leading question; when they get it right, it moves to the next concept; when they are stuck, it offers a scaffolded hint. **Learner model** is Bayesian knowledge tracing (or a simple variant) that updates mastery probability per curriculum node after each interaction. **Curriculum graph** is a Neo4j of concepts with prerequisite edges; the policy walks the graph to pick the next concept. **Memory** is an episodic + semantic store (agentmemory-style) holding past interactions, mistakes, and preferences.

> Four components.


The UX is multimodal. Text input for typed answers. Voice input via LiveKit + Whisper (reuse capstone 03). Photo input for math problems via dots.ocr or PaliGemma 2. Voice output via Cartesia Sonic-2. Safety uses Llama Guard 4 plus an age-appropriate filter (blocks adult content, violence, self-harm) and a COPPA-aware memory retention policy.

> UX is multimodal. Text input for typed answers. Voice input via LiveKit + Whisper (reuse capstone 03). Photo input for math problems via dots.ocr or PaliGemma 2. Voice output via Cartesia Sonic-2. Safety uses Llama Guard 4 plus an age-appropriate filter (blocks adult content, violence, self-harm) and a COPPA-aware memory retention policy.


The efficacy study is the deliverable. 10 learners, pre-test and post-test, two weeks. Report learning gain delta and confidence interval. Compare against a non-adaptive baseline (the same content delivered linearly without the tutor policy).

> 是交付物。


## Architecture | 架构

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

## Stack | 技术栈

- Subject choice: K-12 algebra or intro Python (pick one for depth)
  中文翻译：Subject choice: K-12 algebra or intro Python (pick one for depth)
- Tutor policy: LangGraph over Claude Sonnet 4.7 (with prompt caching)
  中文翻译：Tutor policy: LangGraph over Claude Sonnet 4.7 (with prompt caching)
- Learner model: Bayesian knowledge tracing (classic) or FSRS for spacing
  中文翻译：Learner model: Bayesian knowledge tracing (classic) or FSRS for spacing
- Curriculum graph: Neo4j of concepts + prerequisite edges + OER content
  中文翻译：Curriculum graph: Neo4j of concepts + prerequisite edges + OER content
- Memory: agentmemory-style persistent vector + episodic + semantic store
  中文翻译：Memory: agentmemory-style persistent vector + episodic + semantic store
- Voice: LiveKit Agents 1.0 + Cartesia Sonic-2 (reuse capstone 03 sub-stack)
  中文翻译：Voice: LiveKit Agents 1.0 + Cartesia Sonic-2 (reuse capstone 03 sub-stack)
- Photo math: dots.ocr or PaliGemma 2 for equation recognition
  中文翻译：Photo math: dots.ocr or PaliGemma 2 for equation recognition
- Safety: Llama Guard 4 + custom age-appropriate filter
  中文翻译：Safety: Llama Guard 4 + custom age-appropriate filter
- Eval: Bloom-level question generation, pre/post test harness, efficacy study tooling
  中文翻译：Eval: Bloom-level question generation, pre/post test harness, efficacy study tooling

## Build It | 动手构建

> **【中文解读】** 构建个人 AI 导师系统：课程知识图谱（50-150 个概念节点 + 前置依赖边）、知识诊断测试（项目反应理论 IRT 模型评估学生水平）、个性化学习路径（基于诊断结果的图遍历）、多模态解释生成（文本+图表+代码示例）、间隔重复调度和 Bloom 分类法问题生成。

> **【拓展：AI 教育在 2026 年的突破】** Khan Academy 的 Khanmigo、Duolingo 的 AI 辅导、Coursera 的 AI 学习助手都采用类似架构。关键创新：1）IRT（Item Response Theory）模型精准定位学生知识盲区；2）Bloom 分类法确保问题覆盖记忆/理解/应用/分析/评价/创造六个层次；3）间隔重复算法（Anki 风格）优化长期记忆保持率。Meta 2025 年的研究显示，AI 辅导将学习效率提升约 30%，但完全自主 AI 导师在情感支持和动机维持方面仍不足。

1. **Curriculum graph.** Build a Neo4j of 50-150 concept nodes (e.g., K-12 algebra from "number line" to "quadratic formula") with prerequisite edges. Attach OER content per node (Open Textbook, OpenStax).
   中文翻译：1. **Curriculum graph.** Build a Neo4j of 50-150 concept nodes (e.g., K-12 algebra from "number line" to "quadratic formula") with prerequisite edges. Attach OER content per node (Open Textbook, OpenStax).

2. **Learner model.** Initialize Bayesian knowledge tracing with priors: guess, slip, learn-rate. Update per-concept mastery after each interaction. Persist per learner.
   中文翻译：2. **Learner model.** Initialize Bayesian knowledge tracing with priors: guess, slip, learn-rate. Update per-concept mastery after each interaction. Persist per learner.

3. **Tutor policy.** LangGraph with nodes: `read_signal` (was the learner's answer correct / partial / stuck?), `select_concept` (walk curriculum graph picking the highest-priority concept), `scaffold` (Socratic prompt), `update_mastery`.
   中文翻译：3. **Tutor policy.** LangGraph with nodes: `read_signal` (was the learner's answer correct / partial / stuck?), `select_concept` (walk curriculum graph picking the highest-priority concept), `scaffold` (Socratic prompt), `update_mastery`.

4. **Memory.** Every interaction writes to an episodic store. Mistakes and preferences promote to semantic memory. COPPA-aware retention policy: auto-delete after 1 year, parent-accessible.
   中文翻译：4. **Memory.** Every interaction writes to an episodic store. Mistakes and preferences promote to semantic memory. COPPA-aware retention policy: auto-delete after 1 year, parent-accessible.

5. **Voice path.** LiveKit Agents worker attached to the tutor policy. ASR via Whisper-v3-turbo. TTS via Cartesia Sonic-2. Barge-in supported (reuse capstone 03 mechanics).
   中文翻译：5. **Voice path.** LiveKit Agents worker attached to the tutor policy. ASR via Whisper-v3-turbo. TTS via Cartesia Sonic-2. Barge-in supported (reuse capstone 03 mechanics).

6. **Photo-math path.** Upload or capture image; run dots.ocr or PaliGemma 2 to recognize the equation; feed to tutor as structured input.
   中文翻译：6. **Photo-math path.** Upload or capture image; run dots.ocr or PaliGemma 2 to recognize the equation; feed to tutor as structured input.

7. **Safety.** Every model output passes Llama Guard 4 + an age-appropriate filter (blocks self-harm, adult content, violence). Memory access scoped by learner ID; parental access surface for deletion.
   中文翻译：7. **Safety.** Every model output passes Llama Guard 4 + an age-appropriate filter (blocks self-harm, adult content, violence). Memory access scoped by learner ID; parental access surface for deletion.

8. **Efficacy study.** 10 learners, pre-test (standardized 30-question baseline), two weeks of tutor interaction (3 sessions/week), post-test. Compare against a non-adaptive baseline cohort of 10 learners on the same content.
   中文翻译：8. **Efficacy study.** 10 learners, pre-test (standardized 30-question baseline), two weeks of tutor interaction (3 sessions/week), post-test. Compare against a non-adaptive baseline cohort of 10 learners on the same content.

9. **Weekly progress reports.** Per learner, auto-generate a PDF summary of topics explored, mastery trajectories, and recommended next steps.
   中文翻译：9. **Weekly progress reports.** Per learner, auto-generate a PDF summary of topics explored, mastery trajectories, and recommended next steps.

## Use It | 使用方法

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

## Ship It | 部署上线

`outputs/skill-ai-tutor.md` is the deliverable. A subject-specific adaptive tutor with multimodal input, a learner model, memory, safety, and measured efficacy.

> `outputs/skill-ai-tutor.md` 是交付物. A subject-specific adaptive tutor with multimodal input, a learner model, memory, safety, and measured efficacy.


| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | Learning gain delta | Pre/post-test delta in a 10-learner two-week study |
| 20 | Socratic fidelity | Rubric score on transcript samples |
| 20 | Multimodal UX | Voice + photo + text coherence end to end |
| 20 | Safety + privacy posture | Llama Guard 4 pass rate + COPPA-aware retention |
| 15 | Curriculum breadth and graph quality | Concept coverage + prerequisite graph consistency |
| **100** | | |

## Exercises | 练习题

1. Run the efficacy study with and without the adaptive learner model (random concept order). Report the delta. Expect adaptive to win, but the size is the interesting number.

2. Add a multimodal probe: the same concept question delivered as text, voice, and photo. Measure whether learners converge faster with the modality they prefer.

3. Build a parent dashboard: topics practiced, mastery trajectories, upcoming concepts, safety events (any guardrail hits). COPPA-aligned.

4. Add a language-switch mode: the tutor accepts Spanish input and teaches in Spanish. Measure X-Guard coverage.

5. Stress the memory privacy: verify that learner A cannot see learner B's data even through a voice-clip re-ingest attack. Log the attempted access and alert.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Socratic policy | "Ask, do not dump" | Tutor asks a leading question rather than giving the answer |
| Bayesian knowledge tracing | "BKT" | Classic learner-model equations for mastery probability per concept |
| FSRS | "Free Spaced Repetition Scheduler" | 2024 spaced-repetition scheduler, better than SM-2 |
| Curriculum graph | "Concept DAG" | Neo4j of concepts with prerequisite edges |
| Episodic memory | "Per-interaction log" | Every interaction stored for later retrieval |
| Semantic memory | "Learned pattern store" | Compacted mistakes and preferences promoted from episodic |
| COPPA | "Kids privacy law" | US law restricting data collection from children under 13 |

## Further Reading | 延伸阅读

- [Khanmigo (Khan Academy)](https://www.khanmigo.ai) — reference consumer K-12 tutor
- [Duolingo Max](https://blog.duolingo.com/duolingo-max/) — reference language-learning tutor
- [Google LearnLM / Gemini for Education](https://blog.google/technology/google-deepmind/learnlm) — hosted reference model
- [Quizlet Q-Chat](https://quizlet.com) — alternate reference
- [Synthesis Tutor](https://www.synthesis.com) — startup reference
- [FSRS algorithm](https://github.com/open-spaced-repetition/fsrs4anki) — spaced-repetition scheduler
- [Bayesian Knowledge Tracing](https://en.wikipedia.org/wiki/Bayesian_knowledge_tracing) — learner-model classic
- [LiveKit Agents](https://github.com/livekit/agents) — voice stack
