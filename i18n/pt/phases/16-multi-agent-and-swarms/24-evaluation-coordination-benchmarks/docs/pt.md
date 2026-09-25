# Avaliação e Coordenação Benchmarks .

> Cinco critérios de referência para 2025-2026 abrangem o espaço de avaliação multiagente. **MultiAgentBench / MARBLE**(ACL 2025, arXiv:2503.01935) avalia as topologias de estrelas/cadeias/árvores/grafos com KPI de marcas; **graph is best for research**O planejamento cognitivo adiciona ~3% de realização de metas. **COMMA**Avalia a coordenação multimodal de informação asimétrica; modelos de ponta, incluindo o GPT-4o, lutam para superar uma linha de base aleatória. **MedAgentBoard**(arXiv:2505.12371) abrange quatro categorias de tarefas médicas e muitas vezes encontra multi-agente não domina o single-LLM. **AgentArch**(arXiv:2509.10769) referências de arquiteturas de agentes empresariais combinando utilização de ferramentas + memória + orquestração. **SWE-bench Pro**([arXiv:2509.16941](https://arxiv.org/abs/2509.16941)O modelo de fronteira tem uma pontuação de ~23% no Pro vs 70% + no Verified  uma verificação de realidade sobre a contaminação.**64.3%**Pro com coordenação explícita de agentes-equipas (nenhuma fonte primária antropópica publicada ainda  tratar como preliminar); Verdent (establo de agentes) hits **76.1% pass@1**sobre Verificado ([Verdent technical report](https://www.verdent.ai/blog/swe-bench-verified-technical-report) ).**AAAI 2026 Bridge Program WMAC**(https://multiagents.org/2026/Esta lição baseia-se nas métricas da MARBLE, faz uma varredura topologia-versus-metrica e fixa a regra "apenas passar o banco SWE Verificado não é evidência de generalização".

> **【中文解读】**Esta secção apresenta um método de avaliação da capacidade de coordenação do sistema para medir a coordenação de vários agentes.

> **【拓展：evaluation coordination benchmarks→具体应用】**Do agente  coordenação avaliar基准:(1) AgenteBenchdo Agente  task completude assessment;(2) CLEVALLM Agente  assessment framework;(3) SWE-benchdo Agente 协作修复 bug──关键评估维度: task completion rate、协调效率(步数/成本)、鲁棒性(Agente 故障时的表现) 和可扩展性(Agente 数量增加时的性能变化)──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 15 (Voting and Debate Topology), Phase 16 · 23 (Failure Modes) | **前置知识:** Phase 16 · 15（投票与辩论拓扑），Phase 16 · 23（失败模式）

> - Não .**【前置】**學本節前請先掌握:Fase 16·15(voting拓) ‧Fase 16·23(失败模式) ‧SWE-bench 概念──5 个 2026 主流多 Agent 基准横向对比──
> - Não .**【类比】**多 Agent 基准 = "AI 团队的标准化考试"――MARBLE 测拓(图最佳做研究);COMMA 测多模态不对称信息协调(GPT-4o 都难超随机基线);MedAgentBoard 测医疗(多 Agent 常不胜单 LLM);SWE-bench Pro 测真码(1865 题/41 仓库,前沿模型仅23%,对比 Verified 70%+,揭露污染问题) ―Claude Opus 4.7 多 Agent 协调达 64.3%──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problema Introdução

Quando um artigo afirma que "nosso sistema multi-agente é melhor", a questão é: melhor do que, em que, medida como? A era de avaliação multi-agente de 2023-2024 foi caos.

> Quando o artigo afirma que "nosso multi-agente  sistema melhor", a questão é: do que é melhor, do que é melhor, com que medidas?

Sem benchmarks compartilhados, não se pode comparar significativamente dois sistemas multi-agentes. Pior, sem benchmarks de retenção, os modelos de fronteira podem contaminar. SWE-bench Verified tornou-se parcialmente contaminado nos corpora de treinamento em meados de 2025; pontuações de fronteira inflacionadas; Pro foi projetado como um controle de realidade não contaminado.

>  sem partilha de bases, você não pode significativamente comparar dois mais agentes  sistemas.  pior, não tem reservas de bases, modelo de fronteira pode ser contaminado.

Esta lição enumera os cinco critérios de referência canônicos de 2026, nomeia o que cada uma mede e ensina-o a ler as afirmações de referência de forma cética.

> Esta aula apresenta cinco regras para o teste de base de 2026 e, assim, nomea cada medida do que você tem de fazer.

## Conceptos básicos

### MultiAgentBench (MARBLE)  ACL 2025

ArXiv:2503.01935. Avalia quatro topologias de coordenação (estrela, cadeia, árvore, gráfico) em tarefas de pesquisa, codificação e planejamento.

Resultados medidos:

- **Graph**A melhor topologia para cenários de investigação; apoia qualquer crítica.
- **Chain**melhor para codificação de refinamento gradual.
- **Star**melhor para uma consolidação rápida de facto.
- **Coordination tax**aparece depois de ~4 agentes no gráfico.
- **Cognitive planning**Adiciona ~3% de logros em todas as topologias.

Utilize quando: quer comparar topologias de coordenação maçãs- maçãs.https://github.com/ulab-uiuc/MARBLE) é o avaliador.

### COMMA  Informações asimétricas multimodal

O resultado relatado é desconfortável: os modelos de fronteira, incluindo o GPT-4o, lutam para vencer um grupo de**random baseline**O relatório da Comissão sobre a cooperação entre agentes no COMMA indica que as modalidades de multi-agentes são pouco treinadas e sub-avaliações.

Utilize quando: o seu sistema tem coordenação multimodal ou asimetrica de informação.

### MedAgentBoard  Teste de estresse de domínio

ArXiv:2505.12371. Quatro categorias de tarefas médicas: diagnóstico, planejamento de tratamento, geração de relatórios, comunicação com os pacientes. Comparar sistemas baseados em regras convencionais com sistemas multi-agente versus single-LLM.

A vantagem do multi-agente é estreita  A decomposição das tarefas ajuda quando as subtarefas são claramente separáveis (diagnóstico + tratamento); dói quando a coordenação de gastos gerais excede o ganho de especialização (geração de relatórios).

Use quando: seu domínio tem linhas de base claras de um único LLM. Se a lição do MedAgentBoard generaliza, muitos sistemas multi-agentes propostos são sobre-engenheirados.

### AgenteArch  Arquiteturas empresariais

ArXiv:2509.10769. Configurações empresariais com uso de ferramentas, memória e orquestração em camadas juntas. Benchmark isola a contribuição de cada camada: quanto ajuda adicionar ferramentas? adicionar memória? adicionar orquestração multi-agente?

Utilize quando: você está a projetar uma pilha de agentes empresariais e precisa justificar cada camada.

### SWE-bench Pro  a verificação da realidade

ArXiv:2509.16941. 1865 problemas em 41 repositórios abrangendo aplicativos de negócios, serviços B2B e ferramentas de desenvolvimento.**uncontaminated**Os modelos Frontier têm uma pontuação de ~23% no Pro versus 70%+ no Verified.

Resultados de abril de 2026:
- Claude Opus 4.7 no Pro: **64.3%**(relatado com coordenação explícita entre agentes e equipes; nenhuma fonte primária Anthropic publicada ainda  tratada como preliminar).
- Verdent (establo de agentes) em Verificado: **76.1% pass@1**([technical report](https://www.verdent.ai/blog/swe-bench-verified-technical-report))).
- Resultados brutos de fronteira em Pro sem andamio de agente: ~23-35% ([SWE-bench Pro paper](https://arxiv.org/abs/2509.16941))).

O resultado: "vemos vencer o banco SWE Verified" não é mais uma prova de capacidade. Pro é o teste atual de gating.

### AAAI 2026 WMAC

Programa de ponte 2026 da AAAI  Talento sobre coordenação multi-agente (https://multiagents.org/2026/O artigo 107.o, n.o 1, do Tratado de Maastricht, estabelece um quadro de cooperação entre a Comunidade Europeia e a Comunidade Europeia para a investigação sobre a IA.

### Leia as alegações de referência de forma cética  a lista de verificação de 2026

Quando alguém reclama um resultado multi-agente:

1. **Which benchmark, which split?**Verificado vs Pro é muito importante, um número relatado na divisão errada não vale nada.
   Tradução:**哪个基准，哪个分割？**O SWE-bench Verificado vs Pro  diferença é grande.
2. **Contamination check.**O índice de referência foi lançado após o corte de treino do modelo?
   Tradução:**污染检查。**基准是否在模型训练截止日期后发布?
3. **Baseline comparison.**Contra a linha de base de um único LLM, contra o aleatório, contra o trabalho anterior de vários agentes.
   Tradução:**基线比较。**Comparado com um único Mestrado em Direito Civil, não é "uma versão não modificada do mesmo sistema"".
4. **Statistical significance.**Os modelos de fronteira são de alta variação; as corridas individuais enganam.
   Tradução:**统计显著性。**N 次试验、p 值、置信区间──前沿模型是高方差的;单次运行误导──
5. **Task diversity.**Uma tarefa ou muitas? A generalização é importante para a produção.
   Tradução:**任务多样性。**Uma tarefa ou várias?
6. **Cost disclosure.**Uma solução de 90% a um custo de 20 vezes é uma decisão de negócios, não uma reivindicação de capacidade.
   Tradução:**成本披露。**Cada tarefa é um token  20 % do custo  90%                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

### O que nenhum dos índices de referência mede bem

- **Long-horizon coordination.**Dias de interação entre o relógio de parede.
- **Adversarial resilience.**O que acontece quando um agente é malicioso ou comprometido?
- **Drift under deployment.**Os índices de referência são estáticos; as distribuições de produção mudam.
- **Cost-normalized performance.**A maioria dos índices de referência relata precisão bruta, não precisão por dólar.

Construir o seu próprio índice de referência interno para o eixo que realmente lhe interessa é muitas vezes o movimento certo.

## Construí-lo.
```figure
a5-bench-gap
```

## Construí-lo

`code/main.py`é um passeio não interativo:

- Simula 3 sistemas multi-agentes numa tarefa de brinquedo.
- Computa métricas de margem de estilo MARBLE para cada um.
- Realiza um controlo de contaminação retendo tarefas de um conjunto de "formação".
- Comparado a uma linha de base aleatória explicitamente.
- Imprime um cartão de pontuação de reivindicações de referência.

- Correr .

```bash
python3 code/main.py
```

Resultados esperados: cartão de pontuação do sistema com precisão bruta, realização de metas, custo por tarefa, delta da linha de base versus aleatório e nota de verificação da contaminação.

## Usa-o. Usa-o.

`outputs/skill-benchmark-reader.md`Leia qualquer pedido de referência de vários agentes e aplica a lista de controlo de controlo.

## Envia-o .

Disciplina da avaliação da produção:

- **Build an internal benchmark**Os índices de referência públicos informam, mas não substituem.
  Tradução:**构建内部基准**Reflectar a sua distribuição de produção real.
- **Include a random baseline**Se não conseguirem vencer o acaso por uma grande margem numa tarefa de coordenação, a tarefa pode ser mal colocada.
  Tradução:**在每个比较中包含随机基线。**Se não conseguires superar o tempo em coordenação, a tarefa pode não ser definida.
- **Report cost alongside accuracy.**O custo dos tokens e o relógio de parede.
  Tradução:**同时报告成本和准确率。**Token 成本和挂钟时间──运维团队都需要──
- **Rebuild the benchmark quarterly.**Mudanças na distribuição da produção; valores de referência obsoletos enganam.
  Tradução:**每季度重建基准。**A distribuição de produção é desviada; o passado é um erro de orientação.
- **Avoid published-benchmark overfitting.**Se a sua equipa está a optimizar especificamente para os números de SWE-bench Pro, você regressará à produção.
  Tradução:**避免公开基准过拟合。**Se a sua equipa se especializasse em optimizar os números de SWE-bench Pro, você estará na produção.

## Exercícios.

1. Corra .`code/main.py`Identificar qual dos três sistemas simulados tem o melhor custo por marco.
2. Leia MultiAgentBench (arXiv:2503.01935). Para o seu próprio domínio de tarefas, decida qual das quatro topologias que a MARBLE recomendaria.
3. Leia o artigo do SWE-bench Pro. O que é que o torna especificamente resistente à contaminação?
4. Leia a conclusão da COMMA sobre a coordenação multimodal.
5. Aplique a lista de verificação das reivindicações de referência ao resultado principal de um recente artigo sobre vários agentes.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MARBLE | "MultiAgentBench" / "多 Agent 基准" | ACL 2025; star/chain/tree/graph topologies with milestone KPIs. / ACL 2025；星形/链形/树形/图形拓扑，带里程碑 KPI。 |
| COMMA | "Multimodal benchmark" / "多模态基准" | Multimodal asymmetric-info coordination; frontier models struggle vs random. / 多模态不对称信息协调；前沿模型难以超越随机基线。 |
| MedAgentBoard | "Domain stress test" / "领域压力测试" | Four medical categories; often finds multi-agent does not dominate single-LLM. / 四个医疗类别；常发现多 Agent 不优于单 LLM。 |
| AgentArch | "Enterprise benchmark" / "企业基准" | Tools + memory + orchestration layered. / 工具 + 记忆 + 编排分层。 |
| SWE-bench Pro | "Contamination-resistant" / "抗污染" | 1865 problems, 41 repos; ~23% vs 70%+ on Verified (the contamination signal). / 1865 个问题，41 个仓库；~23% vs Verified 上 70%+（污染信号）。 |
| Milestone achievement / 里程碑达成 | "Partial credit" / "部分积分" | Benchmarks that reward progress, not only final success. / 奖励进展而非仅最终成功的基准。 |
| Contamination / 污染 | "Benchmark leaked into training" / "基准泄露到训练" | Post-release, benchmarks drift into training corpora; scores inflate. / 发布后，基准渗入训练语料；分数膨胀。 |
| WMAC | "AAAI 2026 Bridge Program" / "AAAI 2026 桥接项目" | Workshop on Multi-Agent Coordination; community focal point. / 多 Agent 协调研讨会；社区焦点。 |

## Mais leitura 延伸阅读

- [MultiAgentBench / MARBLE](https://arxiv.org/abs/2503.01935) índice de referência de topologia com indicadores indicadores de referência
- [MARBLE repository](https://github.com/ulab-uiuc/MARBLE) Implementação de referência
- [MedAgentBoard](https://arxiv.org/abs/2505.12371) Teste de tensão de domínio; muitas vezes não domina o multi-agente
- [AgentArch](https://arxiv.org/abs/2509.10769)Arquiteturas de agentes empresariais
- [SWE-bench leaderboards](https://www.swebench.com/) Resultados verificados e pro para modelos de fronteira
- [AAAI 2026 WMAC](https://multiagents.org/2026/) o ponto focal comunitário de 2026
