# Política de Escalagem Responsável Antropical v3.0

> A RSP v3.0 entrou em vigor em 24 de fevereiro de 2026, substituindo a política de 2023. Mitigamento de dois níveis: o que a Anthropic fará unilateralmente versus o que é enquadrado como uma recomendação para toda a indústria (incluindo os padrões de segurança RAND SL-4). Adiciona mapas de roteiro de segurança de fronteiras e relatórios de riscos como documentos permanentes, em vez de dados de entrega pontuais. Despeja o compromisso de pausa para 2023. Introduz o limiar de I&D-4 da IA: uma vez ultrapassado, a Anthropic deve publicar um caso afirmativo identificando riscos e mitigações de desalinhamento. O Claude Opus 4.6 não atravessa. A Antropic afirma no anúncio da versão 3.0 que "confiar que descartar isso está ficando difícil". A SaferAI classificou o RSP de 2023 em 2.2; eles rebaixaram a versão 3.0 para 1.9, colocando a Anthropic na categoria de RSP "fraca" ao lado da OpenAI e DeepMind. Os limites qualitativos substituíram os compromissos quantitativos de 2023; a eliminação da cláusula de pausa é a regressão mais acentuada.

> **【中文解读】**RSP v3.0 于 2026 年 2 月 24 日生效,替代 2023 政策。两层缓解:Antropic 单边做什么 vs 行业范围建议(incluindo RAND SL-4 安全标准) ・添加边界安全路线图和风险报告 作为常设文档而非一次性交付物品──删除 2023 暂停承诺──引入 AI R&D-4 齐值:一旦跨越,Anthropic 必须发布识别不对风险和缓解的肯定案例──Claude Opus 4.6 未跨越它──Anthropic 在 v3.0 公告中声明"自信地排除这变得困难"──Safer 评价 2023 RSP 为 2.2;将降级 v3.0 至 1.9,将 Anthropic 和 DeepMind 起起一"进入了RSP 类别的弱点和缓解的肯定案──Claude Opus 4.6 未跨越它──Anthropic 在 v3.0 公告中声明"自信地排除这变得困难"──Safer 评价 2023 RSP 为 2.2;将降级 v3.0 和 DeepMind 起一"进入了RSP 类别的弱点的定值; 关键条 项 项 暂停承诺是暂停退款项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项

> **【拓展：v3.0 的核心改动】**Três mudanças fundamentais: 1) adicionar o mapa de segurança da primeira linha, o relatório de risco, o R&D-4 valor da IA; 2) eliminar o compromisso de suspensão de 2023; 3) reestruturação de dois níveis de cronograma de suspensão:

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, RSP threshold decision engine) | **语言:** Python（标准库，RSP 阈值决策引擎）
**Prerequisites:** Phase 15 · 06 (AAR), Phase 15 · 07 (RSI) | **前置知识:** Phase 15 · 06（AAR），Phase 15 · 07（RSI）
**Time:** ~45 minutes | **时间:** ~45 分钟

> - Não .**【前置】**O RSI é um sistema de segurança de expansão de laboratórios.
> - Não .**【类比】**RSP = "AI company's security Constitution"―2023 版 = 严格(定量值+暂停承诺);v3.0 = 灵活(定性值+删暂停)―SaferAI 评分 2.2 降至 1.9("弱"类别)―新增AI R&D-4 值 = Uma vez que a AI 能自动化AI 研发达到某水平, deve forçar divulgação
> 🤔 **【困惑】**P: Por que eliminar o suspiro de um compromisso?  商业压力──暂停 = 竞争对手超越你──OpenAI、Google 都没暂停,Antropic 单方面暂停=自杀──修复:行业协调(RAND SL-4 标准) + 监管干预(EU AI Act) 才能避免囚犯困境──

## O problema é o problema da introdução

Os laboratórios de fronteira publicam políticas de escalagem que são em parte documentos técnicos, em parte documentos de governança e em parte sinais para os reguladores.

> A política de expansão publicada pela primeira vez pelo laboratório é parte do arquivo técnico, parte do arquivo administrativo, parte do sinal para os reguladores.

O RSP v3.0 é o documento atual da Anthropic. Lendo atentamente, importa não porque o cumprimento é vinculativo (não é), mas porque o enquadramento molda como um laboratório concebe o risco catastrófico e como eles comunicam as compensações ao público.

> RSP v3.0 é um dos principais modelos de desenvolvimento de uma estrutura de desenvolvimento de um laboratório de pesquisa e de desenvolvimento de pesquisa.

A diferença entre o v3.0 e o v2.0 é a unidade útil. O que foi adicionado: mapas de segurança de fronteira, relatórios de risco, o limiar de I&D-4 da IA. O que foi removido: o compromisso de pausa de 2023.

> A diferença entre o v3.0 e o v2.0 é útil.

O que foi reformado: um cronograma de mitigação de dois níveis dividido entre Anthropic-unilateral e recomendação da indústria.

> 重构: 分为人类 单边和行业建议的两层缓解时间表──外部审查SaferAI将分数从2.2(v2)降低到1.9(v3.0)──这是扩张政策如何在看起来更精细的同时变得更不严谨的――

> **【中文解读】**A política de expansão da responsabilidade antropológica (RSP, Responsible Scaling Policy) definiu um quadro para manter a segurança no crescimento da capacidade de IA. Compromissos centrais: 1) avaliar se o modelo de avaliação periódica avançou para o novo valor da capacidade de risco; 2) definir a segurança de nível e medidas de segurança correspondentes à capacidade; 3) suspender a promessa se a avaliação falhar, suspender a expansão.

## O conceito central.

### O cronograma de mitigação de dois níveis.

- **Anthropic unilateral actions**O treinamento termina acima de um limiar, medidas de segurança específicas, portas de implantação específicas.
  Tradução:**Anthropic 单边动作**Não importa o que outros laboratórios fazem, o Antropic vai fazer.
- **Industry-wide recommendations**A Anthropic não se compromete a promover a segurança, mas a promover políticas.
  Tradução:**行业范围建议**O que é que o mundo tem de fazer?

A estrutura de dois níveis não estava no v2. Significa que um leitor precisa olhar para a coluna em que cada compromisso vive. Uma medida de segurança na coluna "recomendação para toda a indústria" não é a promessa da Anthropic; é a esperança da Anthropic.

> 两层结构在 v2 中没有── isto significa que o leitor precisa ver cada compromisso em que linha── "As recomendações de segurança no âmbito do setor" não são compromissos antropológicos; são esperanças antropológicas──

### O limiar de I&D-4 da IA  Valor

Este é o nível de capacidade RSP v3.0 nomeia como o próximo limiar importante. Especificamente: um modelo que poderia automatizar uma fração substancial da pesquisa de IA a um custo competitivo. Uma vez que a Anthropic acredita que um modelo o cruza, eles devem publicar um caso afirmativo identificando riscos de desalinhamento e mitigações antes de continuar a escala.

> É o RSP v3.0 que é denominado como importante abaixo de um nível de capacidade de valor.

Claude Opus 4.6 não ultrapassa o limite de risco segundo o anúncio v3.0. O documento acrescenta: "Certamente, descartar isso está ficando difícil". Essa fraseção é importante; admite que o limiar está perto o suficiente para ser uma preocupação real, não um limite especulativo.

> Claude Opus 4.6 根据 v3.0 公告未跨越它──文档添加:"Confiança de excluir isso se torna difícil──" Essa frase é importante; ela reconhece que o valor é suficientemente próximo de uma preocupação real, não de uma restrição de sugestão──

A lição 6 (Automated Alignment Research) e a lição 7 (Recursive Self-Improvement) alimentam diretamente este limiar.

> Sexta - Classe 6 (Automatização para o Capacitamento) e sétima - Classe 7 (Regulamento para a Auto-Reforma) diretamente dentro devalor.

### Mapa de segurança fronteiriça e relatórios de riscos

O v3.0 eleva dois tipos de artefatos a documentos permanentes:

> V3.0 vai melhorar duas categorias de produtos para o arquivo permanente:

- **Frontier Safety Roadmap**O documento apresenta um quadro de orientação para o futuro que descreve os trabalhos de segurança planejados, as expectativas de capacidade e a investigação sobre a mitigação.
  Tradução:**前沿安全路线图**O programa de segurança de trabalho, capacidade de antecipação e de alívio de estudos, foi desenvolvido em
- **Risk Report**O documento retrospectivo sobre modelos específicos após a liberação, que descreve a capacidade observada e o risco residual.
  Tradução:**风险报告**O que é que é o problema?

Ambos são públicos. Ambos são atualizados em uma cadência declarada. A utilidade é: o leitor pode rastrear como o que a Anthropic disse que faria em um Roadmap compara com o que relatam em um Relatório de Risco.

> 两者公开──两者按声明节奏更新──效果: Reader可追踪 Antropic 在路线图中说会做与在风险报告中报告中的报告的如何对比──

### Remover a cláusula de pausa

O RSP de 2023 incluiu um compromisso explícito de pausa: se um modelo ultrapassasse os limiares de capacidade específicos, o treinamento interromperia até que as atenuações fossem implementadas. V3.0 substitui a pausa explícita por uma formulação mais suave (publicar um caso afirmativo, prosseguir se as atenuações forem adequadas). SaferAI e outros analistas chamaram isso diretamente como a regressão mais forte no novo documento.

> 2023 RSP incluem um supressão de supressão de forma clara: se o modelo atravessar um determinado valor, o treinamento será suspensa até a sua redução.

O argumento político para a mudança: os limites quantitativos em 2023 revelaram-se inalcançáveis pelos referências de capacidade da era 2026 porque os referências em si foram re-escalados. O contra-argumento: uma cláusula de pausa numa política de escala é um instrumento de compromisso; a sua eliminação elimina a credibilidade da política.

> 变更的政策论文:2023 时代能力基准 定量值被2026 时代能力基准证明不可达成,因为基准本身被重缩缩而成.

### A redução da classificação de SaferAI.

A SaferAI é uma organização independente que avalia documentos de estilo RSP. Sua classificação pública: 2023 Anthropic RSP obteve 2.2 (de uma escala onde 4.0 é a melhor RSP atual e 1.0 é nominal). v3.0 obteve 1.9.

> SaferAI é uma organização independente que avalia RSP 式文档. Its public rating:2023 Antropic RSP 得 2.2(4.0 é o melhor RSP atual, 1.0 é o melhor RSP nominal.

Os fatores de redução de classificação por SaferAI:

> Fator de redução de SAFERAI 列出的:

- Os limites de qualidade substituíram os de qualidade.
  Chinese: 定性值替代定量──
- A pausa de compromisso foi removida.
  Tradução do inglês:暂停承诺移除──
- As mitigações do limiar de I&D-4 da IA são descritas como "casos afirmativos" em vez de medidas específicas.
  Tradução do inglês para "R&D-4"
- Os mecanismos de revisão dependem do Grupo Consultivo de Segurança da Anthropic, com supervisão independente limitada.
  Tradução em inglês:审查机制依赖 Anthropic的安全咨询组,独立监督有限.

### O que esta lição não é, esta lição não é o que é.

Esta não é uma lição de conformidade. RSP v3.0 não é uma regulamentação; nada obriga a Anthropic a segui-la.

> Não é uma disciplina de regimes. Não é uma regra.

A lição é ler o documento com a especificidade e o ceticismo que merece. As políticas de escalagem são os principais sinais públicos de fronteira que os laboratórios emitem sobre a postura de risco catastrófico.

> O programa é usado para ler o documento sobre as características e suspeitas que ele deve ter. A política de expansão é um dos principais sinais públicos emitidos pelos laboratórios de vanguarda sobre a postura de risco de catástrofe.

## Use-o com o framework implementado.
```figure
a5-rsp-ladder
```

## Usá-lo

`code/main.py`Implementa um pequeno motor de decisão que reflete a forma de avaliação do limiar de RSP: dado um modelo candidato e um conjunto de medições de capacidade, retorne se o limiar de I&D-4 da IA foi ultrapassado, as seções de casos afirmativos necessárias e se a implantação pode continuar. É intencionalmente simples; o ponto é tornar a lógica do documento explícita.

> `code/main.py`                                                                                                                                                                                                                                                              

## Envia-o . Produto .

`outputs/skill-scaling-policy-review.md`Revisar uma política de escalagem (Anthropic, OpenAI, DeepMind ou interna) em relação à referência v3.0: estrutura de dois níveis, limiares, compromissos de pausa, revisão independente.

> `outputs/skill-scaling-policy-review.md`À luz do novo modelo, o novo modelo de desenvolvimento tecnológico é o modelo de desenvolvimento tecnológico.

## Exercícios.

1. Corra .`code/main.py`- Introdução de três modelos sintéticos em diferentes níveis de capacidade.
   Tradução: 运行`code/main.py`

2. Leia RSP v3.0 em sua totalidade (32 páginas). Identifique cada compromisso que vive na categoria "recomendações para toda a indústria". Qual desses compromissos teria sido "antropico unilateral" na v2?
   中文翻译:全文阅读 RSP v3.0(32 页) ――识别"行业范围建议"层中的每个承诺──v2 中哪些会是"Antropic 单边"?

3. Leia a metodologia de classificação RSP da SaferAI. Reproduzir a pontuação 1,9 para a versão 3.0 aplicando sua rubrica ao documento. Qual linha de rubrica levou a rebaixada mais?
   Chinese: 阅读 SaferAI's RSP 评分方法论──通过将评分量表应用于文档复现 v3.0 的 1.9 分── qual é a maior redução de valores?

4. Propõe um compromisso de substituição que preserve a credibilidade da política, reconhecendo o problema da recalculação dos valores de referência de 2026.
   Chinese Translation:2023 暂停承诺被移除──提议保留政策可信度同时承认2026 基准重缩放问题的替代承诺──

5. Compare RSP v3.0 com OpenAI Preparedness Framework v2 (Lessão 20). Escolha uma área onde v3.0 é mais forte. Escolha uma área onde o Framework de Preparedness é mais forte.
   中文翻译:Compare RSP v3.0 com OpenAI Preparedness Framework v2 ((第 20 课) ⋅ Select a v3.0 更强的领域── Select a Preparedness Framework 更强的领域──

## Termos-chave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| RSP | "Anthropic's scaling policy" | Responsible Scaling Policy; v3.0 effective Feb 24, 2026 |
| RSP | "Anthropic 的扩展政策" | Responsible Scaling Policy；v3.0 2026 年 2 月 24 日生效 |
| AI R&D-4 | "Research-automation threshold" | Capability to automate substantial AI research at competitive cost |
| AI R&D-4 | "研究自动化阈值" | 以竞争成本自动化相当部分 AI 研究的能力 |
| Affirmative case | "Safety justification" | Published argument that risks are identified and mitigations adequate |
| 肯定案例 | "安全证明" | 风险已识别缓解充分的已发布论证 |
| Frontier Safety Roadmap | "Forward plan" | Standing document on planned safety work and expected capabilities |
| 前沿安全路线图 | "前瞻计划" | 计划安全工作和预期能力的常设文档 |
| Risk Report | "Retrospective on a model" | Standing document on observed capability and residual risk after release |
| 风险报告 | "模型事后" | 发布后观察能力和剩余风险的常设文档 |
| Two-tier mitigation | "Unilateral vs industry" | Anthropic commitments vs industry recommendations, separated |
| 两层缓解 | "单边 vs 行业" | Anthropic 承诺 vs 行业建议，分开 |
| Pause commitment | "2023 clause" | Explicit promise to pause training; removed in v3.0 |
| 暂停承诺 | "2023 条款" | 暂停训练的显式承诺；v3.0 中移除 |
| SaferAI rating | "Independent RSP grade" | Third-party rubric; v3.0 scored 1.9 (v2 was 2.2) |
| SaferAI 评分 | "独立 RSP 评分" | 第三方量表；v3.0 得 1.9（v2 是 2.2） |

## Mais leitura 延伸阅读

- [Anthropic — Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) a política completa de 32 páginas.
  中文翻译:完整 32 页政策。
- [Anthropic — RSP v3.0 announcement](https://www.anthropic.com/news/responsible-scaling-policy-v3) resumo das alterações a partir de v2.
  Tradução do português:
- [Anthropic — Frontier Safety Roadmap](https://www.anthropic.com/research/frontier-safety) documento permanente ligado a partir do RSP v3.0.
  Tradução do português:RSP v3.0 链接的常设文档──
- [Anthropic — Risk Report: Claude Opus 4.6](https://www.anthropic.com/research/risk-report-claude-opus-4-6) retrospectiva do modelo actual de fronteira.
  O que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) liga a IA R&D-4 à autonomia medida.
  Chinese:将 AI R&D-4 连接到测量的自主性──
