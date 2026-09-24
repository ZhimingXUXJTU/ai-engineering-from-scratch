# 符合SOC 2,HIPAA,GDPR,PCI-DSS,欧盟人工智能法,ISO 42001

> 跨框架覆盖率是2026年企业交易的桌面投资. **EU AI Act**根据"高风险"规定,在2026年8月2日实施了最高罚款,最高罚款为1500万欧元或全球高风险系统义务的3%. (第99条)**Colorado AI Act**根据SB25B-004 (SB25B-004) 推迟到2026年2月30日起,**SOC 2 Type II**:实际上 B2B AI 要求 (类型II,而不是类型I,用于金融技术). **GDPR**据证据,最大的针对AI的罚款为3050万欧元 (荷兰DPA,2024年9月);意大利的Garante在2024年12月针对OpenAI发出了1500万欧元 (后来在2026年3月上诉时被撤销).**HIPAA**没有BAA,无法向外部AI服务发送PHI. **PCI-DSS**:人工智能互动层覆盖需要配置+合同协议,而不是自动. **ISO 42001**参考资料:OpenAI维持SOC 2类型 2,ISO/IEC 27001:2022,ISO/IEC 27701:2019,GDPR/CCPA/HIPAA (BAA) /FERPA,PCI-DSS用于ChatGPT支付组件.跨框架映射减少了审计疲劳:通过ISO 27001 A.5.15-5.18,GDPR第32条,HIPAA §164.312(a.

> **【中文解读】**本节介绍了合规框架LLM 服务需要满足法规和合规要求.


**Type:** Learn | **类型:** 学习
**Languages:** (Python optional — compliance is policy + process, not code) | **语言:** Python
**Prerequisites:** Phase 17 · 25 (Security), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 25 (Security), Phase 17 · 13 (Observability)

>  **【前置】**学本节前请先掌握:阶段17·25(安全) 、阶段17·13(可观测性) 多框架合规 = 2026 企业单单的桌面注。
>  **【类比】**合规框架 = "AI 公司的驾照"――欧盟AI法(2024.8 生效,2026.8 高风险全执行) = 欧盟驾照,罚款最高营业额7%;SOC 2类型 II = B2B必备(fintech 必须类型 II);GDPR = 隐私(Clearview AI 被罚款30.5M;HIPAA = 医疗(无A 不能传 PHI);BAPCI-DSS = 支付;ISO 42001 = 新AI 治理――跨框架映射减审负担(访问控制在ISO/GDPR/HIPAA通用) ‧OpenAI 是参考图像:HIPAC 2类型 +ISO 27001/27701 +GDPR/CCPA/PAABAA) /PCI-SSD-(((
> ️ **【易错点】**实时 PII 脱敏是底线,后处理清洗不够(已被GDPR 罚款) 。
**Time:** ~60 minutes | **时间:** ~60 minutes

## 学习目标

- 列出有关LLM产品的7个2026年框架,并将每个框架与客户细分组相匹配.
  中文翻译:列举2026年与LLM产品相关的七个框架,并将每个框架与客户细分相匹配.
- 引用欧盟人工智能法执行时间表 (2024年8月生效;2026年8月高风险执行) 和两层罚款上限 (15M/3%高风险义务,35M/7%禁止实践).
  中文翻译:引用欧盟人工智能法 执法时间表(2024年8月生效;高风险执法 2026年8月) ⋅
- 解释为什么处理后 PII 清理不够用于GDPR,并将实时推断层编辑作为可辩护的标准.
  中文翻译:解释为什么处理后 PII 清理对GDPR不够,并说出实时推理层的替代方案.
- 描述跨框架控制映射 (例如,访问控制地图到ISO 27001 A.5.15-5.18 + GDPR 32 条 + HIPAA §164.312 ((a)).
  中文翻译:描述跨框架控制映射 (如访问控制映射到ISO 27001 A.5.15-5.18 + SOC 2 CC6 + HIPAA 安全规则) ⋅

## 问题 问题引入

> **【中文解读】**多框架覆盖是2026年企业交易的入场券――企业客户的采购要求SOC 2类 II、GDPR、HIPAA BAA、ISO 27001 和"欧盟AI法规声明"――这不是LLM特有问题是企业SaaS问题加上LLM特定的叠加层――采购团队2026年想要一个矩阵(框架×控制),而不是一个PDF――

> **【拓展：EU AI Act 关键时间线】**关键时间线:(1) 2024年8月1日生效;(2) 2025年2月2日禁止执行人工智能实践条款;(3) 2026年8月2日高风险系统条款执行(合规评估,文档、日志);(4) 2027年8月协调立法约束产品中的高风险系统.

企业客户采购要求SOC 2类 II,GDPR,HIPAA BAA,ISO 27001和"EU AI法合规声明".你的团队有SOC 2类 I.你已经从类 II大了六个月,并且还没有开始GDPR第30条记录.

跨框架覆盖不是一个LLM问题,这是一个企业SaaS问题,具有LLM特定的覆盖.2026年采购团队希望有一个矩阵,每个框架都有一行,每个控制都有一列,而不是PDF.

## 概念的核心概念

### 七个框架

> **【拓展：2026 年 LLM 合规框架全景】**2026年LLM 产品需要关注的七大合规框架: 1) SOC 2类型 IIB2B SaaS 基线,类型 II 要求 6-12 个月的操作控制审计; 2) HIPAA美国医疗,BAA不可选,PHI 不能发送到没有BAA的外部AI; 3) GDPREU用户,实时推理层脱敏是 2026年防御性标准,最大AI 相关罚款 €30.5M; 4) PCI-DSS支付数据,AI 触及支付需求配置+合同;(5) EUAI法服务 EU用户,高风险系统 2026年8月执行,罚款 €35M/7%; 6) 科罗拉多法案26年6月30日生效,影响+诉权评估;

| Framework | Scope | LLM-specific requirement |
|-----------|-------|--------------------------|
| SOC 2 Type II | B2B SaaS baseline | Process controls audited over 6-12 months |
| HIPAA | US healthcare | BAA required; PHI cannot leave infrastructure without signed agreement |
| GDPR | EU users | Real-time PII redaction; data subject rights; Article 30 records |
| PCI-DSS | Payment data | Configuration + contracts for AI touching payment |
| EU AI Act | Serving EU users | Risk tier classification; high-risk systems: conformity assessment, documentation, logging |
| Colorado AI Act | Serving CO residents | Impact assessments; right to appeal |
| ISO 42001 | AI governance | Emerging; pairs with ISO 27001 |

### 欧盟人工智能法时间表

- 2024年8月1日:生效.
- 2025年2月2日:实施禁止AI实践.
- 2026年8月2日:高风险系统实施 (符合性评估,文档化,伐木).
- 2027年8月:根据协调立法,产品中的高风险系统.

风险级别:不可接受 (禁止),高风险 (合规性+记录),有限风险 (透明度),最小风险 (没有限制).大多数B2B LLM SaaS是有限风险的;就业,信用,教育,执法,移民,基本服务的高风险推进.

罚款 (第99条):高风险系统义务违规行为最高额达1500万欧元或全球年营业额3% (第99条 4);禁止人工智能行为最高额达3500万欧元或7% (第99条 3));具体取决于更高的情况.

###  GDPR 实时编辑是标准

> **【中文解读】**根据GDPR的推理层实时脱敏是2026年的防御性标准. 后处理清理. LLM 看到数据后再脱敏) 不可防御模型已经看到了数据. 正确做法:LLM 调用前的实体识别 + 一致性标记化.

后处理清理 (在 LLM 看到后编写 PII) 不是可辩护的姿态模型已经看到数据.实时推断层编辑是2026标准:

- 在 LLM 招聘之前的实体认可.
- 保持语义的连贯标记 (Mesh方法).
- 保存仅删除提示+同意的选择原始.

最近的执行:对Clearview AI (荷兰DPA,2024年9月) 的3050万欧元是迄今为止最大的记录的人工智能特定GDPR罚款;对OpenAI (意大利的Garante,2024年12月) 的1500万欧元是最大的LLM特定罚款,尽管该罚款在2026年3月上诉时被撤销,但裁决仍在进一步审查下.

###  HIPAA  BAA不是可选的

没有签署的商业合作伙伴协议,您不能向外部AI服务发送PHI.三个超级级级LLM平台 (Bedrock,Azure OpenAI,Vertex) 都提供BAA.OpenAI直接API提供BAA.人类直接API提供BAA.在发送PHI之前确认.

### 类型II的SOC2

类型I:设计和记录的控制装置.
类型II:控制在6-12个月内有效运行.

2026年B2B采购不符合II类型.I类型是启动器;II类型是门户.

常见的审计驱动因素:访问日志 (谁看到什么),变化管理 (如何部署),风险评估 (季度),事件响应 (测试).

### 跨框架映射

> **【拓展：跨框架映射降低审计疲劳】**跨框架控制映射是减少审计疲劳的关键. 一个访问控制策略可以同时满足多个框架的控制要求:访问日志 → ISO 27001 A.5.15-5.18 + GDPR Art. 变更管理 → ISO 27001 A.8.32 + PCI DSS Req. 违规通知范围;传输加密 → ISO 27001 A.8.24 + GDPR 艺术. 密钥管理 → ISO 27001 A.8.19 + PCI DSS Req. 根据"中国"的标准,该技术的发展将在全球范围内实现.

一项访问控制政策满足多个框架控制:

| Control | Frameworks |
|---------|-----------|
| Access logging | ISO 27001 A.5.15-5.18, GDPR Art. 32, HIPAA §164.312(a) |
| Change management | ISO 27001 A.8.32, PCI DSS Req. 6, HIPAA breach-notification scope |
| Encryption in transit | ISO 27001 A.8.24, GDPR Art. 32, HIPAA §164.312(e) |
| Secrets management | ISO 27001 A.8.19, PCI DSS Req. 8, SOC 2 CC6.1 |

根据标准的要求, 根据标准的要求,

### 新兴的ISO 42001

发布于2023年底.与ISO 27001相结合的采购需求不断增长.包括风险管理,数据质量,透明度,人力监督等AI治理框架.

### 开通AI的参考资料

开通AI维持了SOC 2类型 2,ISO/IEC 27001:2022,ISO/IEC 27701:2019,GDPR/CCPA/HIPAA (BAA) /FERPA,PCI-DSS用于ChatGPT支付组件.

### 你应该记住的数字

- 欧盟人工智能法罚款:最高1500万欧元/3% (高风险义务,第99条 (4));最高3500万欧元/7% (禁止行为,第99条 (3)).
- 欧盟人工智能法高风险执行:2026年8月2日.
- 根据"全球智能技术"的数据,
- 法律法规规规范:第1条第1条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第2条第
- SOC 2型II窗口:6-12个月的操作控制.
- 科罗拉多人工智能法案生效日期:2026年6月30日 (由SB25B-004推迟到2026年2月).

## 用它实现框架
```figure
i4-control-matrix
```

## 用它

`code/main.py`是一个Python中的合规绘图表, 给出一个控制,列出了它满足的框架.

> `code/main.py`是一个Python中的合规绘图表, 给出一个控制,列出了它满足的框架.

## 运送它.

这一课产生了`outputs/skill-compliance-matrix.md`根据客户细分和地理位置,规定所需的框架和控制.

> 本课产出发 `outputs/skill-compliance-matrix.md`根据客户细分和地理位置,规定所需的框架和控制.

## 练习题

1. 您的第一个企业客户需要SOC2类型II,HIPAABAA,EUAI法声明.
   中文翻译:你的第一企业客户需要SOC 2类 II、HIPAA BAA、EU AI法 合规──按优先级排序实现路线图──
2. 根据欧盟人工智能法的风险级别,将三个假设的LLM产品分类.
   中文翻译:在欧盟人工智能法中风险等级下分类三个假设的LLM产品.高风险等级有什么变化?
3. 你不小心地送PHI给一个没有BAA的提供商.
   中文翻译:你不小心将PHI发送给没有BAA的提供商――走一遍事件响应流程――
4. 争辩是否ISO 42001是"2026年必需"的中产市场人工智能供应商.
   中文翻译:论证ISO 42001在2026年对中等市场的AI供应商是否"必要"――
5. 绘制您的LLM审计日志领域 (阶段17 · 25) 至少在三个框架控制.

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [OpenAI Security and Privacy](https://openai.com/security-and-privacy/)参考合规性资料.
- [GuardionAI — LLM Compliance 2026: ISO 42001, EU AI Act, SOC 2, GDPR](https://guardion.ai/blog/llm-compliance-guide-iso-42001-eu-ai-act-soc2-gdpr-2026)
- [Dsalta — SOC 2 Type 2 Audit Guide 2026: 10 AI Controls](https://www.dsalta.com/resources/ai-compliance/soc-2-type-2-audit-guide-2026-10-ai-powered-controls-every-saas-team-needs)
- [EU AI Act official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)主要来源
- [Colorado AI Act](https://leg.colorado.gov/bills/sb24-205)主要来源
- [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html)人工智能管理系统标准.
