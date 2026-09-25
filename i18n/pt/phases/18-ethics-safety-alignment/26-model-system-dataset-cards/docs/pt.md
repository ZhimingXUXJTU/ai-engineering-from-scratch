# Modelo, Sistema e Cartões de Dados.

> Três formatos de documentação estruturam a transparência da IA. Modelo de cartão (Mitchell et al. 2019),  Rótulos nutricionais para modelos: dados de formação, análises desagregadas quantitativas, considerações éticas, avisos; apenas 0,3% dos cartões de modelo Hugging Face documentam considerações éticas (Oreamuno et al. 2023). Fichas de dados para conjuntos de dados (Gebru et al. 2018, CACM)  motivação, composição, processo de coleta, rotulagem, distribuição, manutenção; analogia electrónica-folha de dados. Cartões de dados (Pushkarna et al., Google 2022)  detalhes em camadas modulares (telescópica, periscópico, microscópica) como objetos de fronteira para leitores diversos. Desenvolvimento 2024-2025: geração automatizada através de LLM (CardGen, Liu et al. O número de downloads de HF (Liang et al. A Comissão deve apresentar as suas observações sobre o impacto da utilização de um sistema de controlo de dados. A Comissão deve apresentar um relatório sobre a sustentabilidade (Jouneaux et al. Julho 2025); emergentes cartões reguladores da UE/ISO. Cartões de sistema (Sidhpurwala 2024; Transparência a nível do sistema Meta; "Bluprints of Trust" arXiv:2509.20394)  Documentação de sistema de IA de ponta a ponta que abrange capacidades de segurança, proteção de injeção rápida, detecção de exfiltração de dados, alinhamento com valores humanos.

> **【中文解读】**Este capítulo apresenta o modelo/sistema/data集卡片AI 系统透明度的标准化文档──三种文档格式各有不同的透明度范围:Model Cards(Mitchell 等人 2019)模型的营养标签;Data Sheets for Datasets(Gebruar 等人 2018)数据集的电子规格书;System Cards端到端 AI 系统文档──

> **【拓展：采用率 → 0.3% 问题】**Oreamuno 等人 2023  Audit Hugging Face 模型卡发现只有0.3% 记录伦理考量。Liang 等人 2024 发现详细模型卡与高达29%的下载增加相关采用压力现在是市场驱动的,不仅是合规驱动的──自动化生成(CardGen, Liu 等人 2024) 和可验证证明(Laminator, Duddu 等人 2024) 解决长期采用问题──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, model-card + datasheet + system-card generator) | **语言:** Python（标准库，模型卡 + 数据表 + 系统卡生成器）
**Prerequisites:** Phase 18 · 18 (safety frameworks), Phase 18 · 24 (regulatory) | **前置知识:** Phase 18 · 18 (安全框架), Phase 18 · 24 (监管)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**学本节前请先掌握:Fase 18·18+24──三种透明度文档:模型卡 + 数据集卡 + 系统卡──
> - Não .**【类比】**透明卡 = "protocolo de produtos da IA"―Model Cards = nutrição 标签(entrenamento dados/ análise/伦理); Datasheets = 电子元件规格书(数据集动机/组成/收集);System Cards = 整机蓝图(端到端系统)―问题:仅0.3% HF 模型卡含伦理考量──
> 🤔 详细卡 → 下载量 29%(HF 2024 数据) 透明度有商业价值──2024-2025 新趋势:LLM 自动生成卡(CardGen)、可验证证明(Laminator)、可持续性报告(碳/水)。

## Objetivos de aprendizagem

- Descreva o modelo original de Mitchell et al. de 2019 e a folha de dados de Gebru et al. de 2018.
- Descreva a camada telescópica/periscópica/microscópica dos dados de cartão.
- Descreva os cartões de sistema e a sua cobertura de ponta a ponta.
- Indicar três desenvolvimentos de 2024 a 2025 (geração automatizada, certificações verificáveis, relatórios de sustentabilidade).

> 描述 Mitchell 等人 2019 年的原始模型卡和 Gebru 等人 2018 年的数据表──描述 Data Cards 的望远镜/潜望镜/显微镜分层──描述 System Cards 及其端到端覆盖──说明三个 2024-2025 年发展──

## O problema é o problema .

Os quadros regulatórios (Lessão 24) e as políticas de segurança de laboratório (Lessão 18) exigem documentação. Os formatos de documentação evoluíram de modelos específicos (chartes modelo) para conjuntos de dados específicos (folhas de dados) para sistemas específicos (chartes de sistema). Cada um aborda um escopo diferente de transparência.

> 监管框架和实验室安全政策都要求文档――文档形式从模型特定 (模型卡) 到数据集特定 (数据表) 到系统特定 (系统) 系统卡) 演进――2024-2025 年代自动化和可验证证明工作解决了长期采用问题――

## O conceito .

> **【中文解读】**Modelo de cartões 九大板块:模型详情、预期用途、因素) 、指标、评估数据、训练数据、定量分析(按因素分解) 、伦理考量、注意事项和建议──Data Cards(Google 2022) 三层缩写:望远镜级(非专家高层摘要) 、潜望镜级(ML 从业者中层概览) 、微镜级(审计员显详细特征级文档) ⋅

### Cartões modelo (Mitchell et al. 2019)

Seções:
- Detalhes do modelo.
- Uso previsto.
- Factores (factores demográficos ou ambientais relevantes para avaliação).
- Metricas.
- Dados de avaliação.
- Dados de treinamento.
- Análises quantitativas (desagregadas por fatores).
- Considerações éticas.
- Cavernas e recomendações.

Problema de adoção: Oreamuno et al. Audit 2023 de cartões de modelo Hugging Face encontrou apenas 0,3% de documentos considerações éticas.

### Fichas de dados para conjuntos de dados (Gebru et al. 2018)

Analogia de folha de dados eletrônicos.
- Motivação (por que foi criado o conjunto de dados).
- Composição (o que está nele).
- Processo de recolha (como foi montado).
- Retificação (se aplicável).
- Utilizações (intencionadas, proibidas, riscos).
- Distribuição.
- - A manutenção.

Publicado no CACM 2021. A ficha de dados é a documentação upstream; o modelo de cartão depende da precisão da ficha de dados.

### Cartões de dados (Pushkarna et al., Google 2022)

Detalhes em camadas modulares.
- **Telescopic.**Resumo de alto nível para não peritos.
- **Periscopic.**Visão geral de nível médio para os profissionais de ML.
- **Microscopic.**Documentação pormenorizada de nível de características para auditores.

Enquadramento de limites de objetos: leitores diferentes extraem informações diferentes do mesmo documento.

> **【拓展：System Cards → 部署层透明度】**O sistema de cartões de crédito é um sistema de crédito que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito de crédito, que é um sistema de crédito, que é um sistema de crédito, que é um sistema de crédito, que é um sistema de crédito, que é um sistema de crédito, que é um sistema de crédito, ou seja um sistema de crédito, ou seja, ou seja, um sistema de crédito de crédito, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, um sistema de crédito, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja, ou seja

### Cartões de sistema

Espetáculo: sistema de IA de ponta a ponta, incluindo modelo + pilha de segurança + contexto de implantação.
- Capacidades de segurança.
- Proteção contra injecção rápida.
- Detecção de exfiltração de dados.
- Alignamento com os valores humanos declarados.
- Resposta ao incidente.

Sidhpurwala 2024 e Meta trabalho de transparência a nível do sistema. "Bluprints of Trust" (arXiv:2509.20394) formaliza o Sistema de Cartão como o complemento de nível de implantação para os Modelos de Cartões.

> **【中文解读】**2024-2025 anos de desenvolvimento:CardGen(Liu 等人 2024) através de LLM Automatic Generating Model Card, Reporting Than Many Artificial Card higher Objectivity;Laminator(Duddu 等人 2024) através de hardware TEE/加密签名实现可验证证明允许模型卡携带声明证明而不是仅仅声明;可持续性字段(Jouneaux 等人 2025 年 7 月) 新增碳、水和计算能足迹,对应新兴 ISO 标准.

### Desenvolvimento de 2024 a 2025

- **CardGen (Liu et al. 2024).**Geração automática de cartões de modelo através de LLM; relata maior objetividade do que muitos cartões de autoria humana nos campos padronizados Mitchell 2019.
- **Download correlation (Liang et al. 2024).**Os modelos de cartões detalhados correlacionam com taxas de downloads até 29% mais altas sobre a pressão de adoção de HF  é agora orientada pelo mercado, não apenas pela conformidade.
- **Laminator (Duddu et al. 2024).**As certificações verificáveis através de assinaturas TEE / criptográficas de hardware permitem que o modelo de cartão contenha uma prova de reivindicação, não apenas uma reivindicação.
- **Sustainability (Jouneaux et al. July 2025).**Adições para a pegada de carbono, água e energia computacional; padrões ISO emergentes.
- **Regulatory cards.**O capítulo do Código de Prática da GPAI sobre Transparência exige que os modelos de cartões sejam um artefato de conformidade.

### Onde isto encaixa na Fase 18

As lições 24-25 são as camadas regulatórias e CVE. A lição 26 é a camada de documentação. A lição 27 é a governação de dados de treinamento, que é a ficha de dados a montante. A lição 28 é o ecossistema de pesquisa que produz avaliações referenciadas em cartões.

> Lições 24-25 é a supervisão e a CVE 层――Lessão 26 é o documentário 层――Lessão 27 é o treinamento de dados governamentais――Lessão 28 é a produção de cartões de referência para avaliação de estudos e sistemas de dados――

> **【拓展：可验证证明 → Laminator】**Laminator (Duddu et al. 2024) utiliza hardware TEE / assinatura de armazenamento para realizar prova de validação que permite que o modelo carregem declarações de prova e não apenas declarações. Por exemplo, um modelo carregem um segmento de armazenamento de prova de "acerto de Y% em conjunto de dados X", o verificador pode verificar a prova sem precisar de re-avaliação.

## Usa-o. Usa-o.
```figure
an-card-scopes
```

## Usá-lo

`code/main.py`O sistema de distribuição de dados é um sistema de distribuição de dados, que geram um modelo mínimo de cartão, um arquivo de dados e um sistema de cartão para uma implantação de brinquedo.

> `code/main.py`Para a implantação de jogos, gerar o menor modelo de cartão, data table e sistema de cartão. Cada um segue a estrutura do capítulo padrão.

## Envia-o .

Esta lição produz`outputs/skill-card-audit.md`- Com base num modelo de cartão, numa ficha de dados ou numa ficha de sistema, verifica a cobertura das secções, a desagregação numérica e a presença de atestados verificáveis.

> 本课产 出 `outputs/skill-card-audit.md` dados, modelos, modelos, modelos ou sistemas, contas, divisões de valores e prova de existência de prova de

## Exercícios.

1. Corra .`code/main.py`- Inspeccionar os cartões gerados. Identificar as secções que são fracas (apenas para os titulares de lugares) e especificar quais são as evidências que as fortalecerão.

2. Extender o modelo de cartão com uma análise quantitativa desagregada em dois grupos demográficos (Lessão 20).

3. Leia Oreamuno et al. 2023 sobre a taxa de adoção de 0,3%. Propõe uma alteração estrutural na especificação do modelo de cartão que aumentaria a adoção de considerações éticas.

4. Laminator (Duddu et al. 2024) utiliza TEEs para atestados verificáveis.

5. Escreva um cartão de sistema (Cartão de sistema, não cartão modelo) para um dos seus projetos anteriores ou uma implantação hipotética.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Model Card | "the Mitchell card" | Mitchell et al. 2019 standard documentation for ML models |
| Datasheet | "the Gebru datasheet" | Gebru et al. 2018 standard documentation for datasets |
| Data Card | "the Pushkarna card" | Google 2022 modular layered data documentation |
| System Card | "the deployment card" | End-to-end AI system documentation including safety stack |
| Boundary object | "different readers, one doc" | Data Cards framing: same document serves diverse audiences |
| Verifiable attestation | "the Laminator attestation" | Cryptographic or TEE proof attached to a documentation claim |
| Sustainability field | "carbon / water footprint" | Emerging 2025 addition for environmental accounting |

## Mais leitura 延伸阅读

- [Mitchell et al. — Model Cards for Model Reporting (arXiv:1810.03993, FAT* 2019)](https://arxiv.org/abs/1810.03993) o modelo canônico de cartão
- [Gebru et al. — Datasheets for Datasets (CACM 2021, arXiv:1803.09010)](https://arxiv.org/abs/1803.09010) papel de folha de dados
- [Pushkarna et al. — Data Cards (Google 2022)](https://arxiv.org/abs/2204.01075) Documentação de dados em camadas
- [Sidhpurwala et al. — Blueprints of Trust (arXiv:2509.20394)](https://arxiv.org/abs/2509.20394) Formalização do Cartão de Sistema
