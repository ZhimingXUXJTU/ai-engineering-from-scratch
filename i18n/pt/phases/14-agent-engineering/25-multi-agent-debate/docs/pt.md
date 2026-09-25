# Multidívidas e Colaboração Multidívidas

> Du et al. (ICML 2024, "Sociedade de Mentes") executam instâncias de modelo N que propõem respostas de forma independente, depois se criticam iterativamente em torno de rodadas R para convergir. Melhora a factualidade, seguimento de regras, raciocínio.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 12 (Workflow Patterns), Phase 14 · 05 (Self-Refine and CRITIC) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objetivos de aprendizagem

- Explicar o protocolo de debate: N propostas, R rodadas, convergem numa resposta compartilhada.
- Descreva por que o debate melhora a faculdade, a regra e o raciocínio.
- Explique a topologia escassa: nem todos os debatedores precisam de se ver.
- Implementar um debate sobre um LLM com roteiro com variantes completas e escassas; medir o custo do token versus precisão.

## O problema é o problema da introdução

Auto-refinamento (Lessão 05) é um modelo que se critica  risco de grupo pensamento. CRITIC (Lessão 05) baseia a crítica em ferramentas externas  nem sempre disponíveis.

> Auto-refinamento (第 5 课) é um modelo de autocrítica que existe no grupo de pensamentos.

> - Não .**【前置】**O estudo foi realizado em um estudo de estudos sobre a auto-refinamento e a auto-refinamento, que foi publicado em 18 de janeiro de 2007.


> **【中文解读】**Diversos agentes debatem através de vários exemplos de LLM para discutir a mesma questão de diferentes perspectivas para melhorar a qualidade da raciocínio.

> **{【拓展：多 Agent 辩论是 2023-2025 年的研究热点。Du et al. (2023) 证明两个...】}**Du et al. (2023) provam que dois exemplos de ChatGPT podem melhorar significativamente a taxa de precisão de raciocínio. A prática de 2026 mostra que os 3-5 efeitos do debate de um agente são melhores.
## O conceito central.

### Sociedade das Mentes (Du et al., ICML 2024)

> - Não .**【类比】**Dois agentes 辩论像学术同行评审: 你写论文(N=3 个独立作者各写一版)→ 投稿后 3 个审稿人读对方的版本写评审(R 轮交叉批评)→ Autor Based on review 修改 → 几轮后论文收──关键洞察:单个作者会自信写错(Self-Refine的群体思维),3 个独立作者挑错彼此更容易出现象──但全连接──每个读者) 评审成本是O(N2) 所以会议 "area chair + reviewers" 的星形拓(hub-and-spoke),审稿人只使用和沟通,成本降到O(N) 

- N exemplos modelo propõem independentemente respostas à mesma pergunta.
- Durante as rodadas R, cada modelo lê as propostas dos outros e as critica.
- Os modelos atualizam as suas respostas com base nas críticas.
- Após as rodadas R, devolva a resposta convergente.

Os experimentos originais usaram N=3, R=2 devido ao custo. A precisão melhora com mais agentes e mais rodadas em problemas difíceis (MMLU, GSM8K, Valididade de Movimento de Xadrez, geração de biografia).

> Multidívidas de agentes, permitindo que vários agentes apresentem diferentes pontos de vista sobre a mesma questão e argumentem para melhorar a qualidade da raciocínio.

As combinações de modelos cruzados superam os debates de modelos únicos: ChatGPT + Bard juntos > ou sozinhos.

> 跨模型组合胜过单一模型辩论:ChatGPT + Bard 一起比单独任何一个都好──

> Multidívidas de agentes, permitindo que vários agentes apresentem diferentes pontos de vista sobre a mesma questão e argumentem para melhorar a qualidade da raciocínio.

### Topologia de escassez

"Melhorar o debate multi-agente com a topologia de comunicação Sparse" (arXiv:2406.11776, 2024-2025) mostrou que o debate de rede completa nem sempre é o ideal. As topologias de Sparse (estrela, anel, hub-and-spoke) podem corresponder à precisão a um menor custo de token. Cada debatedor vê apenas um subconjunto de pares.

> "Melhorar o debate multi-agente com a topologia da comunicação de Sparse" (arXiv:2406.11776, 2024-2025) mostra que o debate de ligação total não é sempre o melhor.

> Multidívidas de agentes, permitindo que vários agentes apresentem diferentes pontos de vista sobre a mesma questão e argumentem para melhorar a qualidade da raciocínio.

Implicações:

- N=5, R=3 = 5 × 3 = 15 propostas, cada leitura de 4 pares = 60 críticas.
- Estrela N=5, R=3 (um hub + 4 vozes) = 15 propostas, vozes ler apenas o hub = 12 opções de crítica.

### Quando o debate ajuda

- **Factuality.**N propostas independentes, o controlo cruzado reduz as alucinações.
- **Rule-following.**Validade de movimento de xadrez  Um modelo perde uma regra, outros pegam-na.
- **Open-ended reasoning.**Múltiples enquadramentos limitam-se à resposta certa.

### Quando o debate dói

- **Latency-sensitive UX.**As rodadas de série N × R são latência que talvez não tenha.
- **Cost-sensitive scale.**Tokens N × R por pergunta.
- **Simple factual lookups.**Uma pesquisa é mais barata que cinco debates.

### 2026 instâncias práticas

- **Anthropic orchestrator-workers**(Lessão 12)  uma variante do debate com um passo de síntese.
- **LangGraph supervisor**(Lessão 13)  Roteador central + agentes especializados podem implementar o debate como um nó.
- **OpenAI Agents SDK**(Lessão 16)  Agentes de transferência para frente e para trás para a crítica iterativa.
- **Multi-agent evals** debate em pares + avaliador-optimizador para o sinal de avaliação.

### Onde este padrão vai mal

> 🤔 **【困惑】**Q: 辩论到底什么时候值得使用?N×R 延迟和成本看起来很高―― A: Apenas usados em cenários de "modelo único err erroneously costs far far higher than the cost of debate"―― Jury formula:辩论 cost = N×R× 推理 cost; 错误的单模型错误的预期损失 = 错误率 × 错误的单次损失――当代码生成(一次 bug 进生产 = 几十万损失) 法律文书事实检查、医疗诊断这些场景,单模型哪怕是 95% 准确率也得到N=3,R=2 辩论准确率推推到99%.

- **Convergence collapse.**Todos os agentes convergem na primeira resposta errada, e reduzem a falta de discordância.
- **Hub failure.**Em uma topologia estelar, um núcleo ruim corrompe todos.
- **Prompt homogenization.**Todos os agentes usam o mesmo prompt; produzem as mesmas respostas.

> **收敛崩溃。**Todos os agentes recebem a primeira resposta errada.
> **中心故障。**Em um cenário de estrela, um centro de maldade contaminará todos os habitantes.
> **提示同质化。**Todos os agentes utilizam as mesmas dicas; produzem as mesmas respostas.

## Construí-lo e realizei-o.

> ️ **【易错点】**场景: desenvolvedor usando o mesmo prompt 起起了5辩论者 实例期待"多样化观点" → 后果:5 个实例给出几乎相同的答案 (甚至相同的错误),辩论沦为N 倍成本的自我精炼,这叫"快速同化" → 修复:要么用不同模型 (GPT-4o + Claude + Gemini,异构带来真分歧),要么给每个辩论者不同角色 (你是怀疑论者""你是乐观派""你是细节核查员"),要么至少随机化温度.
```figure
debate-converge
```

## Construí-lo

`code/main.py`Implementa o debate sobre o STDlib:

- `Debater`A classe (Mestrado em Direito Jurídico com derivação de opinião por debatedor).
- `FullMeshDebate`E ...`SparseDebate`Corredores.
- Três perguntas: uma factual, uma baseada em regras, uma raciocínio.
- Metricas: resposta convergente, rodadas para convergência, operações de crítica total.

- É o que é ?

```
python3 code/main.py
```

Resultados: precisão e custo por protocolo; correspondências escassas em 2/3 de perguntas a um custo menor.

> 输出: precisão e custo de cada acordo; raridade de expansão em 2/3 de problemas para menor custo de correspondência total.

> Multidívidas de agentes, permitindo que vários agentes apresentem diferentes pontos de vista sobre a mesma questão e argumentem para melhorar a qualidade da raciocínio.

## Use-o com o framework implementado.

- **Anthropic orchestrator-workers**Para debates simples de dois a três trabalhadores.
- **LangGraph**O Conselho Europeu de Ministros dos Negócios Estrangeiros, em nome da Comissão, tem de apresentar um relatório sobre a proposta de directiva.
- **Custom**para investigação ou garantias de correcção especializadas.

## Envia-o . Produto .

`outputs/skill-debate.md`Estabelece um debate multi-agente com topologia configurável, N, R e uma regra de convergência.

> `outputs/skill-debate.md`construir um multi-agente que pode ser configurado  N  R 和收 规则的多代理 辩

> Multidívidas de agentes, permitindo que vários agentes apresentem diferentes pontos de vista sobre a mesma questão e argumentem para melhorar a qualidade da raciocínio.

## Exercícios.

1. Implementar uma regra de "desacordo forçado": na primeira rodada, cada debatente deve apresentar uma proposta distinta.
  Tradução do inglês para tradução do inglês:
2. Adicionar uma agregação ponderada pela confiança: os debatedores retornam (resposta, confiança); o agregador pesa pela confiança.
  Tradução do inglês para tradução do inglês:
3. Troca um "agente" por um LLM diferente com diferentes opiniões.
  Tradução do inglês para tradução do inglês:
4. Mita o custo do token para rede completa vs. escassa em suas 3 perguntas.
  Tradução do inglês para tradução do inglês:
5. Leia o artigo da Sociedade das Mentes.
  Tradução do inglês para tradução do inglês:

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Debate | "Multi-agent critique" | N proposers, R rounds of cross-critique, converge |  |
| Full mesh | "Everyone reads everyone" | Every debater reads every peer each round |  |
| Sparse topology | "Limited peer view" | Debaters read only a subset of peers |  |
| Hub-and-spoke | "Star topology" | One central debater, N-1 spokes read only the hub |  |
| Convergence | "Agreement" | Debaters converge on a shared answer |  |
| Society of Minds | "Du et al. debate paper" | ICML 2024 multi-agent debate method |  |

## Mais leitura 延伸阅读

- [Du et al., Society of Minds (arXiv:2305.14325)](https://arxiv.org/abs/2305.14325) debate canônico multi-agente
  Tradução do português:
- [Sparse Communication Topology (arXiv:2406.11776)](https://arxiv.org/abs/2406.11776) resultados de topologia escassos
  Tradução do português:
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) trabalhadores-orquestrais como variante de debate
  Tradução do português:
- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) Contralor de autocrítica de modelo único
  Tradução do português:
