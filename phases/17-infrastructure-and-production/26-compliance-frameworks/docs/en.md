# Compliance — SOC 2, HIPAA, GDPR, PCI-DSS, EU AI Act, ISO 42001 | 合规 行动 欧盟 PR

> Multi-framework coverage is table stakes for 2026 enterprise deals. **EU AI Act**: in force since August 1, 2024. Most high-risk requirements enforce August 2, 2026. Fines up to €15M or 3% global annual turnover for high-risk-system obligations (Art. 99(4)); up to €35M or 7% for prohibited AI practices (Art. 99(3)). Applies globally if serving EU users. **Colorado AI Act**: effective June 30, 2026 (delayed from February 2026 by SB25B-004) — impact assessments for high-risk systems, right to appeal AI decisions. Virginia similar for credit/employment/housing/education. **SOC 2 Type II**: de facto B2B AI requirement (Type II, not Type I, for fintech). **GDPR**: largest documented AI-specific fine is €30.5M against Clearview AI (Dutch DPA, Sept 2024); Italy's Garante issued €15M against OpenAI in Dec 2024 (later overturned on appeal in March 2026). Real-time PII redaction at inference is the defensible standard; post-processing cleanup is not enough. **HIPAA**: healthcare bound — cannot send PHI to external AI services without BAA. **PCI-DSS**: AI-interaction-layer coverage requires configuration + contractual agreements, not automatic. **ISO 42001**: emerging AI governance standard, growing procurement requirement alongside ISO 27001. Reference profile: OpenAI maintains SOC 2 Type 2, ISO/IEC 27001:2022, ISO/IEC 27701:2019, GDPR/CCPA/HIPAA (BAA)/FERPA, PCI-DSS for ChatGPT payment components. Cross-framework mapping reduces audit fatigue: access controls map across ISO 27001 A.5.15-5.18, GDPR Art. 32, HIPAA §164.312(a).

> **【中文解读】** 本节介绍了合规框架——LLM 服务需要满足的法规和合规要求。


**Type:** Learn | **类型:** 学习
**Languages:** (Python optional — compliance is policy + process, not code) | **语言:** Python
**Prerequisites:** Phase 17 · 25 (Security), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 25 (Security), Phase 17 · 13 (Observability)

> 🔗 **【前置】** 学本节前请先掌握：Phase 17·25（安全）、Phase 17·13（可观测性）。多框架合规 = 2026 企业单的桌面赌注。
> 💡 **【类比】** 合规框架 = "AI 公司的驾照"。EU AI Act（2024.8 生效，2026.8 高风险全执行）= 欧盟驾照，罚款最高营业额 7%；SOC 2 Type II = B2B 必备（fintech 必须 Type II）；GDPR = 隐私（Clearview AI 被罚 €30.5M）；HIPAA = 医疗（无 BAA 不能传 PHI）；PCI-DSS = 支付；ISO 42001 = 新兴 AI 治理。跨框架映射减审计负担（访问控制在 ISO/GDPR/HIPAA 通用）。OpenAI 是参考画像：SOC 2 Type 2 + ISO 27001/27701 + GDPR/CCPA/HIPAA(BAA)/FERPA + PCI-DSS。
> ⚠️ **【易错点】** 实时 PII 脱敏是底线，后处理清洗不够（已被 GDPR 罚款）。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Learning Objectives | 学习目标

- Enumerate the seven 2026 frameworks relevant to LLM products and match each to a customer segment.
  中文翻译：列举 2026 年与 LLM 产品相关的七个框架，并将每个匹配到客户细分。
- Cite the EU AI Act enforcement timeline (in force August 2024; high-risk enforcement August 2026) and the two-tier fine ceiling (€15M / 3% for high-risk obligations, €35M / 7% for prohibited practices).
  中文翻译：引用 EU AI Act 执法时间表（2024 年 8 月生效；高风险执法 2026 年 8 月）。
- Explain why post-processing PII cleanup is not enough for GDPR and name real-time inference-layer redaction as the defensible standard.
  中文翻译：解释为什么后处理 PII 清理对 GDPR 不够，并说出实时推理层的替代方案。
- Describe cross-framework control mapping (e.g., access control maps to ISO 27001 A.5.15-5.18 + GDPR Art. 32 + HIPAA §164.312(a)).
  中文翻译：描述跨框架控制映射（如访问控制映射到 ISO 27001 A.5.15-5.18 + SOC 2 CC6 + HIPAA 安全规则）。

## The Problem | 问题引入

> **【中文解读】** 多框架覆盖是 2026 年企业交易的入场券。企业客户的采购要求 SOC 2 Type II、GDPR、HIPAA BAA、ISO 27001 和"EU AI Act 合规声明"。这不是 LLM 特有问题——是企业 SaaS 问题加上 LLM 特定的叠加层。采购团队 2026 年想要的是一个矩阵（框架×控制），而不是一个 PDF。

> **【拓展：EU AI Act 关键时间线】** EU AI Act 关键时间线：(1) 2024 年 8 月 1 日生效；(2) 2025 年 2 月 2 日——禁止 AI 实践条款执行；(3) 2026 年 8 月 2 日——高风险系统条款执行（合规评估、文档、日志）；(4) 2027 年 8 月——受协调立法约束产品中的高风险系统。罚款：高风险系统违规最高 €15M 或全球年营业额 3%（Art. 99(4)）；禁止 AI 实践最高 €35M 或 7%（Art. 99(3)）。大多数 B2B LLM SaaS 属于"有限风险"；高风险涉及就业、信贷、教育、执法、移民、基本服务。

An enterprise customer's procurement asks for SOC 2 Type II, GDPR, HIPAA BAA, ISO 27001, and "EU AI Act compliance statement." Your team has SOC 2 Type I. You're six months from Type II and haven't started GDPR Article 30 records.

Multi-framework coverage is not an LLM problem — it's an enterprise-SaaS problem, with LLM-specific overlays. Procurement teams in 2026 want a matrix with a row per framework and a column per control, not a PDF.

## The Concept | 核心概念

### The seven frameworks

> **【拓展：2026 年 LLM 合规框架全景】** 2026 年 LLM 产品需要关注的七大合规框架：(1) SOC 2 Type II——B2B SaaS 基线，Type II 要求 6-12 个月的操作控制审计；(2) HIPAA——美国医疗，BAA 不可选，PHI 不能发送到无 BAA 的外部 AI；(3) GDPR——EU 用户，实时推理层脱敏是 2026 年防御性标准，最大 AI 相关罚款 €30.5M；(4) PCI-DSS——支付数据，AI 触及支付需要配置+合同；(5) EU AI Act——服务 EU 用户，高风险系统 2026 年 8 月执行，罚款最高 €35M/7%；(6) Colorado AI Act——2026 年 6 月 30 日生效，影响评估+上诉权；(7) ISO 42001——AI 治理新兴标准，与 ISO 27001 配套。

| Framework | Scope | LLM-specific requirement |
|-----------|-------|--------------------------|
| SOC 2 Type II | B2B SaaS baseline | Process controls audited over 6-12 months |
| HIPAA | US healthcare | BAA required; PHI cannot leave infrastructure without signed agreement |
| GDPR | EU users | Real-time PII redaction; data subject rights; Article 30 records |
| PCI-DSS | Payment data | Configuration + contracts for AI touching payment |
| EU AI Act | Serving EU users | Risk tier classification; high-risk systems: conformity assessment, documentation, logging |
| Colorado AI Act | Serving CO residents | Impact assessments; right to appeal |
| ISO 42001 | AI governance | Emerging; pairs with ISO 27001 |

### EU AI Act timeline

- August 1, 2024: in force.
- February 2, 2025: prohibited-AI practices enforced.
- August 2, 2026: high-risk systems enforced (conformity assessment, documentation, logging).
- August 2027: high-risk systems in products under harmonized legislation.

Risk tiers: Unacceptable (banned), High-risk (conformity + logging), Limited-risk (transparency), Minimal-risk (no constraint). Most B2B LLM SaaS is limited-risk; high-risk kicks in for employment, credit, education, law enforcement, migration, essential services.

Fines (Article 99): up to €15M or 3% global annual turnover for breaches of high-risk-system obligations (Art. 99(4)); up to €35M or 7% for prohibited AI practices (Art. 99(3)); whichever higher applies.

### GDPR — real-time redaction is the standard

> **【中文解读】** GDPR 的推理层实时脱敏是 2026 年的防御性标准。后处理清理（LLM 看到数据后再脱敏）不可防御——模型已经看到了数据。正确做法：LLM 调用前的实体识别 + 一致性标记化（Mesh 方法）保持语义 + 仅存储脱敏提示 + 用户同意的 opt-in 原始数据。最大 AI 相关 GDPR 罚款：Clearview AI €30.5M（荷兰 DPA，2024 年 9 月）；最大 LLM 相关罚款：OpenAI €15M（意大利 Garante，2024 年 12 月，2026 年 3 月上诉后推翻）。

Post-processing cleanup (redact PII after the LLM sees it) is not a defensible posture — the model already saw the data. Real-time inference-layer redaction is the 2026 standard:

- Entity recognition before the LLM call.
- Consistent tokenization (Mesh approach) preserves semantics.
- Store only redacted prompts + consented opt-in raw.

Recent enforcement: €30.5M against Clearview AI (Dutch DPA, Sept 2024) is the largest documented AI-specific GDPR fine to date; €15M against OpenAI (Italy's Garante, Dec 2024) is the largest LLM-specific fine, though it was overturned on appeal in March 2026 and the ruling remains under further review. Post-processing claims have failed at audit.

### HIPAA — BAA is not optional

You cannot send PHI to external AI services without a signed Business Associate Agreement. All three hyperscaler LLM platforms (Bedrock, Azure OpenAI, Vertex) offer BAAs. OpenAI direct API offers BAA. Anthropic direct API offers BAA. Confirm before sending PHI.

### SOC 2 Type II

Type I: controls designed and documented.
Type II: controls operate effectively over 6-12 months.

B2B procurement in 2026 defaults to Type II. Type I is a starter; Type II is the gate.

Common audit drivers: access logs (who saw what), change management (how was it deployed), risk assessments (quarterly), incident response (tested?). Audit log from Phase 17 · 25 is directly reusable.

### Cross-framework mapping

> **【拓展：跨框架映射降低审计疲劳】** 跨框架控制映射是减少审计疲劳的关键。一个访问控制策略可以同时满足多个框架的控制要求：访问日志 → ISO 27001 A.5.15-5.18 + GDPR Art. 32 + HIPAA §164.312(a)；变更管理 → ISO 27001 A.8.32 + PCI DSS Req. 6 + HIPAA 违规通知范围；传输加密 → ISO 27001 A.8.24 + GDPR Art. 32 + HIPAA §164.312(e)；密钥管理 → ISO 27001 A.8.19 + PCI DSS Req. 8 + SOC 2 CC6.1。合规自动化工具（Drata、Vanta、Secureframe）可以自动化这个映射——大规模部署时值得投资。OpenAI 的参考合规档案（SOC 2 Type 2 + ISO 27001 + ISO 27701 + GDPR/CCPA/HIPAA/FERPA + PCI-DSS）大致是 2026 年的企业入场标准。

One access control policy satisfies multiple framework controls:

| Control | Frameworks |
|---------|-----------|
| Access logging | ISO 27001 A.5.15-5.18, GDPR Art. 32, HIPAA §164.312(a) |
| Change management | ISO 27001 A.8.32, PCI DSS Req. 6, HIPAA breach-notification scope |
| Encryption in transit | ISO 27001 A.8.24, GDPR Art. 32, HIPAA §164.312(e) |
| Secrets management | ISO 27001 A.8.19, PCI DSS Req. 8, SOC 2 CC6.1 |

Compliance tools (Drata, Vanta, Secureframe) automate this mapping. Worth the cost at scale.

### ISO 42001 — emerging

Published late 2023. Growing procurement requirement alongside ISO 27001. Framework for AI governance including risk management, data quality, transparency, human oversight.

### OpenAI's reference profile

OpenAI maintains SOC 2 Type 2, ISO/IEC 27001:2022, ISO/IEC 27701:2019, GDPR/CCPA/HIPAA (BAA)/FERPA, PCI-DSS for ChatGPT payment components. That is roughly the enterprise table stakes in 2026.

### Numbers you should remember

- EU AI Act fines: up to €15M / 3% (high-risk obligations, Art. 99(4)); up to €35M / 7% (prohibited practices, Art. 99(3)).
- EU AI Act high-risk enforcement: August 2, 2026.
- Largest documented AI-specific GDPR fine: €30.5M, Clearview AI (Dutch DPA, Sept 2024).
- Largest LLM-specific GDPR fine: €15M, OpenAI (Italy's Garante, Dec 2024; overturned on appeal March 2026).
- SOC 2 Type II window: 6-12 months of operated controls.
- Colorado AI Act effective date: June 30, 2026 (delayed from February 2026 by SB25B-004).

## Use It | 用框架实现

`code/main.py` is a compliance-mapping spreadsheet in Python — given a control, lists frameworks it satisfies.

> `code/main.py` is a compliance-mapping spreadsheet in Python — given a control, lists frameworks it satisfies.

## Ship It | 产出物

This lesson produces `outputs/skill-compliance-matrix.md`. Given customer segment and geography, specifies required frameworks and controls.

> 本课产出 `outputs/skill-compliance-matrix.md`. Given customer segment and geography, specifies required frameworks and controls.

## Exercises | 练习题

1. Your first enterprise customer requires SOC 2 Type II, HIPAA BAA, EU AI Act statement. What is the minimum viable compliance posture to win the deal?
   中文翻译：你的第一个企业客户需要 SOC 2 Type II、HIPAA BAA、EU AI Act 合规。按优先级排序实现路线图。
2. Classify three hypothetical LLM products under EU AI Act risk tiers. What changes at high-risk?
   中文翻译：在 EU AI Act 风险等级下分类三个假设的 LLM 产品。高风险等级有什么变化？
3. You accidentally sent PHI to a provider without BAA. Walk through the incident response.
   中文翻译：你不小心将 PHI 发送给了没有 BAA 的提供商。走一遍事件响应流程。
4. Argue whether ISO 42001 is "necessary in 2026" for a mid-market AI vendor.
   中文翻译：论证 ISO 42001 在 2026 年对中等市场 AI 供应商是否"必要"。
5. Map your LLM audit log fields (Phase 17 · 25) to at least three framework controls.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| SOC 2 Type II | "audited controls" | Controls operating over 6-12 months, independently attested |
| HIPAA BAA | "healthcare contract" | Business Associate Agreement; required for PHI |
| GDPR | "EU privacy" | Real-time PII redaction is the defensible 2026 standard |
| EU AI Act | "EU AI rules" | High-risk enforcement August 2026; €15M / 3% (high-risk obligations) — €35M / 7% (prohibited practices) |
| Colorado AI Act | "US AI state law" | June 30, 2026 effective (delayed by SB25B-004); impact assessments |
| ISO 42001 | "AI governance" | Emerging framework for AI risk + transparency |
| ISO 27001 | "security ISMS" | Information Security Management System baseline |
| Conformity assessment | "EU AI doc package" | High-risk requirement: docs, testing, logging |
| Cross-framework mapping | "one control, many frames" | Single policy satisfies multiple framework controls |

## Further Reading | 延伸阅读

- [OpenAI Security and Privacy](https://openai.com/security-and-privacy/) — reference compliance profile.
- [GuardionAI — LLM Compliance 2026: ISO 42001, EU AI Act, SOC 2, GDPR](https://guardion.ai/blog/llm-compliance-guide-iso-42001-eu-ai-act-soc2-gdpr-2026)
- [Dsalta — SOC 2 Type 2 Audit Guide 2026: 10 AI Controls](https://www.dsalta.com/resources/ai-compliance/soc-2-type-2-audit-guide-2026-10-ai-powered-controls-every-saas-team-needs)
- [EU AI Act official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) — primary source.
- [Colorado AI Act](https://leg.colorado.gov/bills/sb24-205) — primary source.
- [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html) — AI management system standard.
