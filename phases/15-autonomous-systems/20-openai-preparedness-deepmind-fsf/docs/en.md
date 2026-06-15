# OpenAI Preparedness Framework and DeepMind Frontier Safety Framework | 准备度 前沿 OpenAI 安全

> OpenAI Preparedness Framework v2 (April 2025) introduces Research Categories — Long-range Autonomy, Sandbagging, Autonomous Replication and Adaptation, Undermining Safeguards — distinct from Tracked Categories. Tracked Categories trigger Capabilities Reports plus Safeguards Reports reviewed by the Safety Advisory Group. DeepMind's FSF v3 (September 2025, with Tracked Capability Levels added April 17, 2026) folds autonomy into ML R&D and Cyber domains (ML R&D autonomy level 1 = fully automate the AI R&D pipeline at competitive cost vs human + AI tools). FSF v3 explicitly addresses deceptive alignment via automated monitoring for instrumental-reasoning misuse. The honest note: Research Categories in PF v2 (including Long-range Autonomy) do not automatically trigger mitigations; the policy language is "potential." DeepMind itself says automated monitoring "will not remain sufficient long-term" if instrumental reasoning strengthens.

> **【中文解读】** 本节介绍了各前沿 AI 实验室的安全框架——Anthropic RSP、OpenAI Preparedness、DeepMind FSF。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-framework decision-table diff tool) | **语言:** Python（标准库，三框架决策表差异工具）
**Prerequisites:** Phase 15 · 19 (Anthropic RSP) | **前置知识:** Phase 15 · 19（Anthropic RSP）
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

Lesson 19 read Anthropic's scaling policy closely. This lesson completes the picture by reading OpenAI's and DeepMind's. The three documents are cousin artifacts addressing the same question — when should a frontier lab pause or gate a model — and they converge on a small set of categories and diverge in specific places that matter.

> 第 19 课仔细阅读了 Anthropic 的扩展政策。本课通过阅读 OpenAI 和 DeepMind 的政策来完成全景。这三份文档是同源工件，回答同一问题——前沿实验室何时应暂停或门控模型——它们在一小组类别上收敛，在关键具体点分歧。

The convergence: all three label long-range autonomy as a capability class worth tracking. All three acknowledge deceptive behavior as a specific class of risk. All three have an internal review body. The divergence: OpenAI splits categories into "Tracked" (mandatory mitigation) and "Research" (no automatic trigger). DeepMind folds autonomy into two domains rather than naming it separately. The lab names Tracked vs Research, or Critical vs Moderate, or Tier-1 vs Tier-2; the operational consequence of which bucket a capability lives in is different across labs.

> 收敛点：三者都将长程自主标记为值得跟踪的能力类别。三者都承认欺骗行为（对齐伪装、sandbagging）是特定风险类别。三者都有内部审查机构。分歧点：OpenAI 将类别分为"Tracked"（强制缓解）和"Research"（无自动触发）。DeepMind 将自主性折叠到两个领域而非单独命名。实验室命名 Tracked vs Research、Critical vs Moderate、Tier-1 vs Tier-2；能力所在桶的运营后果在实验室间不同。

Reading them together is the useful exercise. The same capability can be "mandatory mitigation" at Anthropic, "monitored but not triggering" at OpenAI, and "tracked in a specific domain" at DeepMind. The policy posture matters.

> 将三者一起阅读是有用的练习。同一能力在 Anthropic 是"强制缓解"、在 OpenAI 是"监控但不触发"、在 DeepMind 是"在特定领域跟踪"。政策姿态很重要。

## The Concept | 核心概念

### OpenAI Preparedness Framework v2 (April 2025)

Structure:

> 结构：

- **Tracked Categories**: trigger Capabilities Reports (what the model can do) plus Safeguards Reports (what mitigations are in place). Reviewed by the Safety Advisory Group before deployment.
  中文翻译：**Tracked Categories（跟踪类别）**：触发能力报告（模型能做什么）加防护报告（已有哪些缓解）。部署前由安全咨询组（Safety Advisory Group）审查。
- **Research Categories**: model capabilities the lab is tracking but not yet committing to specific mitigations. Includes Long-range Autonomy, Sandbagging, Autonomous Replication and Adaptation, Undermining Safeguards.
  中文翻译：**Research Categories（研究类别）**：实验室正在跟踪但尚未承诺特定缓解的模型能力。包括长程自主、Sandbagging、自主复制与适应、破坏防护。

Key framing in v2: Research Categories do not automatically trigger mitigations. The policy language is "potential" mitigations. This is the specific delta to watch: a category's location in Tracked vs Research is the hinge between "gated" and "observed."

> v2 的关键框架：Research Categories 不自动触发缓解。政策语言是"潜在"缓解。这是要关注的具体差异：一个类别在 Tracked 还是 Research 的位置是"门控"和"观察"之间的铰链。

### DeepMind Frontier Safety Framework v3 (September 2025; Tracked Capability Levels added April 17, 2026)

Structure:

> 结构：

- **Critical Capability Levels (CCLs)**: capability thresholds across five domains: Cyber, Bio, ML R&D, CBRN, Autonomy (folded into ML R&D and Cyber).
  中文翻译：**Critical Capability Levels（CCL，关键能力等级）**：跨五个领域的能力阈值：网络、生物、机器学习研发、CBRN、自主性（折叠到机器学习研发和网络中）。
- **Tracked Capability Levels**: additional granularity added in April 2026. Concrete example: ML R&D autonomy level 1 = fully automate the AI R&D pipeline at competitive cost vs human + AI tools.
  中文翻译：**Tracked Capability Levels（跟踪能力等级）**：2026 年 4 月添加的额外粒度。具体例子：机器学习研发自主等级 1 = 以与人类+AI 工具竞争的成本完全自动化 AI 研发管道。
- **Deceptive alignment monitoring**: explicit commitment to automated monitoring for instrumental-reasoning misuse.
  中文翻译：**欺骗对齐监控**：明确承诺对工具性推理滥用进行自动化监控。

The autonomy framing differs from OpenAI's. DeepMind does not keep "Autonomy" as a top-level domain; it is folded into the domains where autonomy would cause harm (ML R&D and Cyber). The argument is that autonomy without a domain is capability without risk; the counter-argument is that autonomy across domains is a meta-risk the framework should name.

> 自主性框架与 OpenAI 不同。DeepMind 不将"自主性"保留为顶级领域；它被折叠到自主性会造成损害的领域（机器学习研发和网络）。论点是：无领域的自主性是无风险的能力；反论是：跨领域的自主性是框架应命名的元风险。

### What all three converge on

- Internal Safety Advisory Group (named Anthropic SAG, OpenAI SAG, DeepMind internal committee). Review before deployment for high-capability models.
  中文翻译：内部安全咨询组（名为 Anthropic SAG、OpenAI SAG、DeepMind 内部委员会）。高能力模型部署前审查。
- Explicit mention of deceptive alignment / alignment faking as a risk class.
  中文翻译：明确提及欺骗对齐/对齐伪装作为风险类别。
- Standing artifacts on a declared cadence (Anthropic: Frontier Safety Roadmap, Risk Report; OpenAI: Capabilities and Safeguards Reports; DeepMind: FSF update cycle).
  中文翻译：按声明节奏发布的常设工件（Anthropic：前沿安全路线图、风险报告；OpenAI：能力和防护报告；DeepMind：FSF 更新周期）。
- Acknowledgement that monitoring-only defenses have a ceiling. DeepMind is explicit: "automated monitoring will not remain sufficient long-term."
  中文翻译：承认仅监控防御有上限。DeepMind 明确说："自动化监控长期不会保持足够。"

### Where they diverge

- **Anthropic**: pause commitment removed in v3.0; AI R&D-4 threshold is the named next gate.
  中文翻译：**Anthropic**：v3.0 移除暂停承诺；AI R&D-4 阈值是命名的下一个门控。
- **OpenAI**: Tracked vs Research split; Research Categories (including Long-range Autonomy) do not automatically gate.
  中文翻译：**OpenAI**：Tracked vs Research 分割；Research Categories（包括长程自主）不自动门控。
- **DeepMind**: autonomy folded into other domains; Tracked Capability Levels add granularity in April 2026.
  中文翻译：**DeepMind**：自主性折叠到其他领域；Tracked Capability Levels 在 2026 年 4 月增加粒度。

### Sandbagging: a specific capability that complicates all three

Sandbagging (a model strategically underperforming on evaluations) is in OpenAI's Research Categories. Anthropic's RSP v3.0 addresses it via the evaluation-context gap (Lesson 1). DeepMind addresses it via deceptive alignment monitoring in FSF v3.

> Sandbagging（模型在评估中战略性表现不佳）在 OpenAI 的 Research Categories 中。Anthropic RSP v3.0 通过评估上下文差距（第 1 课）处理。DeepMind 通过 FSF v3 的欺骗对齐监控处理。

If a model sandbags on evaluations, every framework's capability thresholds are underestimated. The framework works only if the measurement works. This is why external measurement (Lesson 21, METR) and adversarial evaluation are necessary in addition to lab self-assessment.

> 如果模型在评估中装傻，每个框架的能力阈值都被低估。框架只在测量有效时才有效。这就是为什么除了实验室自评估外，外部测量（第 21 课 METR）和对抗评估是必要的。

### The policy-reading skill

- Locate: every capability you care about should be findable in the policy. If not findable, the policy does not cover it.
  中文翻译：**定位**：你关心的每个能力应在政策中可找到。如不可找到，政策不覆盖它。
- Classify: is it Tracked (triggers mitigation) or Research (tracked but not triggering)? OpenAI names this; Anthropic and DeepMind have their own equivalents.
  中文翻译：**分类**：是 Tracked（触发缓解）还是 Research（跟踪但不触发）？OpenAI 命名此；Anthropic 和 DeepMind 有各自的等价物。
- Cadence: is the policy updated on a declared schedule, or only after specific events? Declared cadence is stronger.
  中文翻译：**节奏**：政策按声明计划更新，还是仅在特定事件后？声明节奏更强。
- Independence: is external review mandatory or optional? Anthropic partners with Apollo and US AI Safety Institute; OpenAI with METR; DeepMind with internal SAG primarily.
  中文翻译：**独立性**：外部审查是强制还是可选？Anthropic 与 Apollo 和美国 AI 安全研究所合作；OpenAI 与 METR 合作；DeepMind 主要与内部 SAG。

## Use It | 用框架实现

`code/main.py` implements a small decision-table diff tool. Given a capability (autonomy, deceptive alignment, R&D automation, cyber uplift, etc.), it outputs how each of the three policies classifies the capability, and what mitigations trigger. It's a reading aid, not a policy tool.

> `code/main.py` 实现小型决策表差异工具。给定一个能力（自主性、欺骗对齐、研发自动化、网络增强等），输出三个政策各自如何分类该能力，以及触发哪些缓解。这是阅读辅助，不是政策工具。

## Ship It | 产出物

`outputs/skill-cross-policy-diff.md` produces a cross-policy comparison for a specific capability, using the three frameworks as reference.

> `outputs/skill-cross-policy-diff.md` 为特定能力生成跨政策比较，使用三个框架作为参考。

## Exercises | 练习题

1. Run `code/main.py`. Confirm the diff tool's output matches the policies for at least two capabilities you can verify against the source documents.
   中文翻译：运行 `code/main.py`。确认差异工具输出与你可在源文档验证的至少两个能力匹配。

2. Read OpenAI Preparedness Framework v2 in full. Identify each Research Category. For each, write one sentence on why it is in Research rather than Tracked.
   中文翻译：完整阅读 OpenAI Preparedness Framework v2。识别每个 Research Category。为每个写一句话说明为何在 Research 而非 Tracked。

3. Read DeepMind FSF v3 in full, plus the April 2026 Tracked Capability Levels update. Identify ML R&D autonomy level 1's specific evaluation criteria. How would you measure it externally?
   中文翻译：完整阅读 DeepMind FSF v3 加 2026 年 4 月 Tracked Capability Levels 更新。识别机器学习研发自主等级 1 的具体评估标准。你会如何外部测量？

4. Sandbagging is in OpenAI's Research Categories. Design an evaluation that would force a sandbagging model to reveal its actual capability. Reference the Lesson 1 eval-context-gaming discussion.
   中文翻译：Sandbagging 在 OpenAI Research Categories 中。设计一个评估迫使 sandbagging 模型揭示其真实能力。参考第 1 课 eval-context-gaming 讨论。

5. Compare the three policies on a specific capability (your choice). Name which policy's classification you find most rigorous and which least. Justify with source text.
   中文翻译：比较三个政策在特定能力（你选）上的分类。命名你认为最严格和最不严格的分类。用源文本论证。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| Preparedness Framework | "OpenAI's scaling policy" | PF v2 (April 2025); Tracked vs Research categories | OpenAI 准备度框架：PF v2，Tracked vs Research |
| Tracked Category | "Mandatory mitigation" | Triggers Capabilities + Safeguards Reports; SAG review | 跟踪类别：触发能力+防护报告，SAG 审查 |
| Research Category | "Monitored only" | Tracked but no automatic mitigation; includes Long-range Autonomy | 研究类别：跟踪但不自动缓解，含长程自主 |
| Frontier Safety Framework | "DeepMind's scaling policy" | FSF v3 (Sept 2025) + Tracked Capability Levels (Apr 2026) | DeepMind 前沿安全框架 |
| CCL | "Critical Capability Level" | DeepMind threshold per domain (Cyber, Bio, ML R&D, CBRN) | 关键能力等级：DeepMind 各领域阈值 |
| ML R&D autonomy level 1 | "R&D automation" | Fully automate AI R&D pipeline at competitive cost | 机器学习研发自主等级 1：完全自动化研发管道 |
| Sandbagging | "Strategic underperformance" | Model underperforms on evals; in OpenAI Research Categories | Sandbagging：模型战略性表现不佳 |
| Instrumental reasoning | "Means-ends reasoning" | Reasoning about how to achieve goals; target of DeepMind monitoring | 工具性推理：DeepMind 监控目标 |

## Further Reading | 延伸阅读

- [OpenAI — Updating our Preparedness Framework](https://openai.com/index/updating-our-preparedness-framework/) — v2 announcement.
  中文翻译：v2 公告
- [OpenAI — Preparedness Framework v2 PDF](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf) — full document.
  中文翻译：完整文档
- [DeepMind — Strengthening our Frontier Safety Framework](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) — FSF v3 announcement.
  中文翻译：FSF v3 公告
- [DeepMind — Updating the Frontier Safety Framework (April 2026)](https://deepmind.google/blog/updating-the-frontier-safety-framework/) — Tracked Capability Levels addition.
  中文翻译：Tracked Capability Levels 添加
- [Gemini 3 Pro FSF Report](https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_fsf_report.pdf) — example of an FSF-format Risk Report.
  中文翻译：FSF 格式风险报告示例
