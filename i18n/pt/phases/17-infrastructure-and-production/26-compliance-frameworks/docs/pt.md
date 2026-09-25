# Compliance  SOC 2, HIPAA, GDPR, PCI-DSS, EU AI Act, ISO 42001 合规 行动 欧盟 PR

> A cobertura multi-quadro é a participação de mesa em 2026 acordos empresariais. **EU AI Act**A maioria dos requisitos de alto risco são aplicados em 2 de agosto de 2026. Impelas de até 15 milhões de euros ou 3% do volume de negócios global por obrigações de sistemas de alto risco (artigo 99(4); até 35 milhões de euros ou 7% por práticas proibidas de IA (artigo 99(3)).**Colorado AI Act**A Comissão propõe que a Comissão adopte um novo regulamento que estabelece as regras de aplicação do artigo 107.o, n.o 1, do Regulamento (CE) n.o 1083/2008.**SOC 2 Type II**: exigência de facto de IA B2B (tipo II, não tipo I, para fintech). **GDPR**A maior multa documentada específica de IA é de € 30,5 milhões contra a Clearview AI (DPA holandesa, setembro 2024); Garante da Itália emitiu € 15 milhões contra a OpenAI em dezembro de 2024 (mais tarde revogada em recurso em março de 2026).**HIPAA**: saúde obrigada  não pode enviar PHI para serviços externos de IA sem BAA. **PCI-DSS**: A cobertura de camadas de interação com IA requer configuração + acordos contratuais, não automática. **ISO 42001**O perfil de referência: OpenAI mantém SOC 2 Tipo 2, ISO/IEC 27001:2022, ISO/IEC 27701:2019, GDPR/CCPA/HIPAA (BAA) / FERPA, PCI-DSS para componentes de pagamento ChatGPT. O mapeamento cruzado reduz a fadiga de auditoria: controle de acesso mapa em toda a ISO 27001 A.5.15-5.18, GDPR Art. 32, HIPAA §164.312(a).

> **【中文解读】**Esta secção apresenta o quadro de conformidade LLM  serviços necessários para satisfazer as normas e requisitos de conformidade 


**Type:** Learn | **类型:** 学习
**Languages:** (Python optional — compliance is policy + process, not code) | **语言:** Python
**Prerequisites:** Phase 17 · 25 (Security), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 25 (Security), Phase 17 · 13 (Observability)

> - Não .**【前置】**O que é o que acontece com o seu negócio?
> - Não .**【类比】**合规框架 = "AI 公司的驾照"――EU AI Act(2024.8 生效,2026.8 高风险全执行) = 欧盟驾照,罚款最高营业额 7%;SOC 2 Type II = B2B必备(fintech 必须 Type II);GDPR = 隐私(Clearview AI 被罚 €30.5M);HIPAA = 医疗(无A 不能传 PHI);BAPCI-DSS = 支付;ISO 42001 = 新AI 治理──跨框架映射减审负担(访问控制在ISO/GDPR/HIPAA通用) ‧OpenAI 是参考画像:HIPAC 2 Type 2 + ISO 27001/27701 + GDPR/CCPA/PAABAA) /PCI-SSD-((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
> ️ **【易错点】**实时 PII 脱敏是底线,后处理清洗不够( já foi sancionado pelo GDPR)
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizagem

- Enumerar os sete quadros de 2026 relevantes para os produtos LLM e combinar cada um com um segmento de clientes.
  Chinese Translation: 列举 2026 年与LLM 产品相关的七个框架,并将每个匹配到客户细分――
- Citar o calendário de aplicação da Lei da IA da UE (em vigor em agosto de 2024; aplicação de riscos elevados em agosto de 2026) e o limite máximo de multa de dois níveis (€ 15 milhões / 3% para obrigações de alto risco, € 35 milhões / 7% para práticas proibidas).
  Chinese:                                                                                                                                                                                                                                                              
- Explique por que a limpeza de PII pós-processamento não é suficiente para o GDPR e nomee a redação em tempo real da camada de inferência como o padrão defensivel.
  Tradução do inglês para o português: explica por que o tratamento posterior de PII  limpeza do RGPD não é suficiente, e diz que é um substituto do tratamento de nível de dados.
- Descrever o mapeamento de controle transframe (por exemplo, mapas de controle de acesso para a ISO 27001 A.5.15-5.18 + GDPR Art. 32 + HIPAA §164.312 ((a)).
  中文翻译:描述跨框架控制映射 (如访问控制映射到 ISO 27001 A.5.15-5.18 + SOC 2 CC6 + HIPAA 安全规则)

## O problema é o problema da introdução

> **【中文解读】**O multi framework coverage é o ingresso de bolsa de 2026 para negócios. Os clientes de empresas exigem a compra de SOC 2 Tipo II, GDPR, HIPAA BAA, ISO 27001 e "EU AI Act 合规声明" (Lei de conformidade da UE).

> **【拓展：EU AI Act 关键时间线】**A lei da UE sobre IA 关键时间线:(1) 2024 年 8 月 1 日生效;(2) 2025 年 2 月 2 日禁止 AI 实践条款执行;(3) 2026 年 8 月 2 日高风险系统条款执行(合规评估、文档、日志);(4) 2027 年 8 月受协调立法约束产品中的高风险系统;;

A aquisição de um cliente empresarial pede SOC 2 Tipo II, GDPR, HIPAA BAA, ISO 27001, e "Declaração de conformidade com a Lei de IA da UE". Sua equipe tem SOC 2 Tipo I. Você tem seis meses do Tipo II e não iniciou os registros do Artigo 30 do GDPR.

A cobertura multi-quadro não é um problema de LLM  é um problema de Enterprise-SaaS, com sobreposições específicas de LLM. As equipes de aquisição em 2026 querem uma matriz com uma linha por framework e uma coluna por controle, não um PDF.

## O conceito central.

### Os sete quadros

> **【拓展：2026 年 LLM 合规框架全景】**Os produtos LLM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

| Framework | Scope | LLM-specific requirement |
|-----------|-------|--------------------------|
| SOC 2 Type II | B2B SaaS baseline | Process controls audited over 6-12 months |
| HIPAA | US healthcare | BAA required; PHI cannot leave infrastructure without signed agreement |
| GDPR | EU users | Real-time PII redaction; data subject rights; Article 30 records |
| PCI-DSS | Payment data | Configuration + contracts for AI touching payment |
| EU AI Act | Serving EU users | Risk tier classification; high-risk systems: conformity assessment, documentation, logging |
| Colorado AI Act | Serving CO residents | Impact assessments; right to appeal |
| ISO 42001 | AI governance | Emerging; pairs with ISO 27001 |

### Linha de tempo do Ato da IA da UE

- 1 de agosto de 2024: em vigor.
- 2 de fevereiro de 2025: aplicadas as práticas proibidas de IA.
- 2 de agosto de 2026: aplicação de sistemas de alto risco (avaliação da conformidade, documentação, registos).
- Agosto 2027: sistemas de alto risco em produtos, sob legislação harmonizada.

Níveis de risco: Inaceitável (proibido), Alto risco (conformidade + registros), Risco limitado (transparência), Risco mínimo (sem restrições). A maioria dos B2B LLM SaaS é de risco limitado; lançamentos de alto risco para emprego, crédito, educação, aplicação da lei, migração, serviços essenciais.

As multas (artigo 99): até 15 milhões de euros ou 3% do volume de negócios global anual por violação de obrigações de sistema de alto risco (artigo 99 ((4)); até 35 milhões de euros ou 7% para práticas proibidas de IA (artigo 99 ((3)); consoante o montante mais elevado.

### GDPR  Redigir em tempo real é o padrão

> **【中文解读】**O RGPD é um sistema de gestão de dados que permite a utilização de dados e de dados para a gestão de dados. O RGPD é um sistema de gestão de dados e de dados para a gestão de dados e de dados.

A limpeza pós-processamento (redigir PII depois que o LLM vê) não é uma postura defensiva  o modelo já viu os dados.

- Reconhecimento da entidade antes da convocatória de LLM.
- A tokenização consistente (abordagem Mesh) preserva a semântica.
- Armazenar apenas as instruções editadas + consentimento opt-in crudo.

Recentemente aplicada: € 30,5 milhões contra a Clearview AI (DPA holandesa, setembro 2024) é a maior multa GDPR documentada específica da IA até à data; € 15 milhões contra a OpenAI (Garante da Itália, dezembro 2024) é a maior multa específica da LLM, embora tenha sido revogada em recurso em março de 2026 e a decisão permanece sob revisão adicional.

### HIPAA  BAA não é opcional

Você não pode enviar PHI para serviços externos de IA sem um Acordo de Asociado de Negócios assinado. Todas as três plataformas de LLM hipercaler (Bedrock, Azure OpenAI, Vertex) oferecem BAAs. OpenAI diretamente API oferece BAA. Antropic diretamente API oferece BAA. Confirme antes de enviar PHI.

### SOC 2 Tipo II

Tipo I: controles concebidos e documentados.
Tipo II: os controles funcionam eficazmente durante 6 a 12 meses.

As compras B2B em 2026 são padrões para o tipo II. O tipo I é um iniciador; o tipo II é o portão.

Os principais factores de auditoria: registos de acesso (quem viu o quê), gestão de alterações (como foi implementada), avaliações de riscos (quarta-feira), resposta a incidentes (testada)?

### Mapeamento transversal

> **【拓展：跨框架映射降低审计疲劳】**跨框架控制映射是减少审计疲劳的关键―― Uma estratégia de controle de visitas pode simultaneamente satisfazer os requisitos de controle de vários frameworks: 32 + HIPAA §164.312 ((a);变更管理 → ISO 27001 A.8.32 + PCI DSS Req. 6 + HIPAA  违规通知范围;传输加密 → ISO 27001 A.8.24 + GDPR Art. 32 + HIPAA §164.312 ((e);密钥管理 → ISO 27001 A.8.19 + PCI DSS Req. 8 + SOC 2 CC6.1── Conformidade ferramenta de automação (Drata、Vanta、Secureframe) pode automatizar esta mapeamento Massal deployment 时值投资──OpenAI's reference conformities档案(SOC 2 Type 2 + ISO 27001 + ISO 27701 + GDPR/CCPA/HIPAA/FERPA + PCI-DSS) 大致是 2026 年的企业入场标准──

Uma política de controlo de acesso satisfaz vários controlos-quadro:

| Control | Frameworks |
|---------|-----------|
| Access logging | ISO 27001 A.5.15-5.18, GDPR Art. 32, HIPAA §164.312(a) |
| Change management | ISO 27001 A.8.32, PCI DSS Req. 6, HIPAA breach-notification scope |
| Encryption in transit | ISO 27001 A.8.24, GDPR Art. 32, HIPAA §164.312(e) |
| Secrets management | ISO 27001 A.8.19, PCI DSS Req. 8, SOC 2 CC6.1 |

As ferramentas de conformidade (Drata, Vanta, Secureframe) automatizam este mapeamento.

### ISO 42001  emergente

Publicado no final de 2023. Requisitos crescentes de aquisição junto com a ISO 27001.

### Profil de referência da OpenAI

A OpenAI mantém SOC 2 Tipo 2, ISO/IEC 27001:2022, ISO/IEC 27701:2019, GDPR/CCPA/HIPAA (BAA) / FERPA, PCI-DSS para componentes de pagamento ChatGPT. Isso é aproximadamente a mesa da empresa em 2026.

### Números que você deve lembrar

- As multas previstas na Lei da IA da UE: até 15 milhões de euros / 3% (obrigações de alto risco, artigo 99? 4)); até 35 milhões de euros / 7% (práticas proibidas, artigo 99? 3)).
- A aplicação da Lei da UE sobre IA em risco elevado: 2 de agosto de 2026.
- A maior multa do GDPR documentada específica da IA: € 30,5 milhões, Clearview AI (DPA holandês, setembro 2024).
- A maior multa do RGPD específica do LLM: 15 milhões de euros, OpenAI (Garante da Itália, de dezembro de 2024; revogada em recurso em março de 2026).
- O sistema SOC 2 Tipo II: 6 a 12 meses de controlo operacional.
- Data de entrada em vigor da Lei de IA do Colorado: 30 de junho de 2026 (retrasado a partir de fevereiro de 2026 pela SB25B-004).

## Use-o com o framework implementado.
```figure
i4-control-matrix
```

## Usá-lo

`code/main.py`é uma planilha de mapeamento de conformidade em Python  dado um controle, lista os quadros que satisfaz.

> `code/main.py`é uma planilha de mapeamento de conformidade em Python  dado um controle, lista os quadros que satisfaz.

## Envia-o . Produto .

Esta lição produz`outputs/skill-compliance-matrix.md`- Especifica os quadros e os controles necessários, tendo em conta o segmento de clientes e a sua geografia.

> 本课产 出 `outputs/skill-compliance-matrix.md`- Especifica os quadros e os controles necessários, tendo em conta o segmento de clientes e a sua geografia.

## Exercícios.

1. O seu primeiro cliente empresarial requer SOC 2 Tipo II, HIPAA BAA, declaração da Lei de IA da UE. Qual é a postura mínima viável de conformidade para ganhar o negócio?
   Chinese: Your first enterprise customer needs SOC 2 Type II, HIPAA BAA, EU AI Act, 合规, 按优先级排序实现路线图, 合规, 按优先级排序实现路线图, 按优先级排序实现路线图, 按优先级排序实现路线图, 按优先级排序实现路线图, 按优先级排序实现路线图, 按优先级排序实现路线图, 按优先级排序实现路线图, 按优先级排序实现路线图, 按优先级排序实现路线图, 按优先级排序实现路线图, 按优先级排序实现路线图, 按优先级排序实现路线图, 按优先级排序实现路线图, 按优先级排序实现路线图, 按
2. Classificar três produtos hipotéticos de LLM sob os níveis de risco da Lei da IA da UE.
   Tradução em inglês: What's changed in the EU AI Act 风险等级下分类三个假设的 LLM 产品──高风险等级有什么变化?
3. Enviaste o PHI acidentalmente a um provedor sem BAA.
   Não é o caso de um agente de saúde que não tenha recebido um pagamento de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de R$ de
4. Argumentar se a ISO 42001 é "necessária em 2026" para um fornecedor de IA de mercado médio.
   Tradução do inglês para o inglês: essay ISO 42001 ⇒ 2026 
5. Mapear os campos de registro de auditoria do Mestrado em Direito (Fase 17 · 25) para pelo menos três controles estruturais.

## Termos-chave .

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

## Mais leitura 延伸阅读

- [OpenAI Security and Privacy](https://openai.com/security-and-privacy/) perfil de referência de conformidade.
- [GuardionAI — LLM Compliance 2026: ISO 42001, EU AI Act, SOC 2, GDPR](https://guardion.ai/blog/llm-compliance-guide-iso-42001-eu-ai-act-soc2-gdpr-2026)
- [Dsalta — SOC 2 Type 2 Audit Guide 2026: 10 AI Controls](https://www.dsalta.com/resources/ai-compliance/soc-2-type-2-audit-guide-2026-10-ai-powered-controls-every-saas-team-needs)
- [EU AI Act official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) fonte primária.
- [Colorado AI Act](https://leg.colorado.gov/bills/sb24-205) fonte primária.
- [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html) Padrão de sistema de gestão de IA.
