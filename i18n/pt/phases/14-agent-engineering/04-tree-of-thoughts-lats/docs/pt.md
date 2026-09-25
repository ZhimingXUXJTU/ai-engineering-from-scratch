# Árvore dos Pensamentos e LATS: Busca deliberada

> Uma única trajetória de cadeia de pensamento não tem espaço para retroceder. ToT (Yao et al., 2023) transforma o raciocínio em uma árvore com auto-avaliação em cada nó. LATS (Zhou et al., 2024) unifica ToT com ReAct e Reflexion sob a Pesquisa de Árvore de Monte Carlo.

> **【中文解读】**单条思维链没有回归空间――ToT将推理变为带有自评树结构,Game of 24 4% 升升至74%──LATS 统一了ToT、ReAct 和 Reflection,使用蒙特卡洛树搜索实现,HumanEval 达到92.7% pass@1──

> **【拓展：ToT/LATS → OpenAI o1/o3 的推理搜索】**O "penso profundo" do modelo da série OpenAI o1/o3 é, em essência, pesquisa em um espaço de pensamento para explorar várias rotas, avaliar e escolher o melhor.

> - Não .**【前置】**本节硬核,前置必须扎实:Fase 14·01(ReAct) LATS 内部就是 ReAct;Fase 14·03(Reflexão) LATS  Self-Reflector 复用 Reflexion 机制; bem como MCTS(蒙特卡洛树搜索)`Q(s,a) + c*sqrt(lnN/N)`Os dois elementos representam o que, primeiro, veja o artigo ou o curso AlphaGo.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 03 (Reflexion) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 03 (Reflexion)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Raciocínio de quadro como pesquisa: nós são "pensamentos", bordas são "expansions", valor é "quão promissor".
  O que é que é um quadro de reflexão?
- Implementar uma pesquisa de árvore BFS no estilo stdlib ToT com pontuação de autoavaliação.
  Tradução do inglês para tradução livre: using standard library implement ToT 风格的 BFS 树搜索,带自评估评分──
- Estender para um circuito LATS MCTS de brinquedo com selecção / expansão / simulação / retropropagação.
  Tradução do inglês para tradução do inglês: expand expand expand for play LATS MCTS 循环,包含选择/扩展/模拟/反向传播──
- Decida quando a pesquisa vale o multiplicador de tokens (Game of 24, geração de código) e quando uma única trajetória é suficiente (questionamento e resposta simples).
  Chinese:                                                                                                                                                                                                                                                              

## O problema é o problema da introdução

A cadeia de pensamento é uma caminhada linear. Se o primeiro passo for errado, cada passo subsequente funciona com uma premissa ruim. No jogo de 24 (use quatro dígitos com + − × ÷ para fazer 24), o GPT-4 CoT atinge uma precisão de 4%. O modelo escolhe a subexpressão errada cedo e não pode recuperar.

> Se o primeiro passo estiver errado, cada passo posterior será baseado em um erro. No jogo de 24 (com quatro números e + − × ÷  obtém 24) o GPT-4 CoT tem uma taxa de precisão de apenas 4% e não pode ser recuperado após a expressão do erro inicial.

O que o raciocínio precisa é da capacidade de propor vários candidatos, avaliá-los, escolher os promissores e recuar quando surgem terminações estancadas.

> Túbulos necessários são: apresentar vários programas de candidatura, avaliá-los, selecionar perspectivas, retroceder ao mesmo tempo.

> **【中文解读】**O pensamento é linear de avanço Se o primeiro passo estiver errado, cada passo posterior é baseado em um pressuposto errado.

## O conceito central.

### Árvore dos Pensamentos (Yao et al., NeurIPS 2023)

Cada nó é um passo intermediário coerente ("um pensamento"). Cada nó pode se expandir para pensamentos de K. O LLM auto-avalia cada nó com um prompt de pontuação.

> Cada ponto é um passo intermediário de uma linha de pensamento. Cada ponto pode ser expandido para um ponto de pensamento.

```
                     (root: "find 24 from 4 6 4 1")
                    /               |            \
           ("6 - 4 = 2")    ("4 + 1 = 5")    ("4 * 6 = 24")  <- Score: HIGH
              /   \              |                  |
          ...    ...          ...                finish
```

A autoavaliação é a peça de carga.`sure / likely / impossible`classificação, `1..10`Os três venceram a CoT substancialmente no jogo de 24 (4% -> 74% com GPT-4).

> - Não .**【类比】**Para o "calculador" do jogo de xadrez: cada passo antes de calcular 3-5 variações no cérebro (expandir), auto-avalia qual variação é mais favorável (auto-avaliação), corta uma variação claramente inferior (impossível), aprofunda o cálculo de mudanças favoráveis (CoT é "com a intuição de que o próximo passo" é o "calculador" do erro de um passo na sua totalidade.

> O artigo apresenta três variações:`sure / likely / impossible`- Não.`1..10`Número de avaliações e votação de candidatos.

### LATS (Zhou et al., ICML 2024)

O LATS unifica ToT, ReAct e Reflexion sob o MCTS.

> LATS em MCTS, reúne-se a TOT, ReAct e Reflexion, e LLM desempenha três papéis:

- **Policy**: propõe candidato a próximas acções (estilo ReAct).
  Tradução:**策略**O Conselho Europeu de Administração e de Desenvolvimento Económico e Social (CEPA)
- **Value function**: pontuação de uma trajetória parcial (auto-evaluação ao estilo ToT).
  Tradução:**价值函数**O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é?
- **Self-reflector**No caso de falhas, escreva uma reflexão em linguagem natural (estilo de reflexão) e usa-a para reanalisar futuras implementações.
  Tradução:**自我反思器**Refleção (Reflexão) é usado para re-emprender o futuro.

Os resultados em tempo de papel: HumanEval pass@1 92,7% com GPT-4 (SOTA), WebShop média de 75.9 com GPT-3.5 (aproximando-se de ajuste fino baseado em gradiente).

> 环境反(观察)混入价值函数,使搜索由真实工具结果而非仅仅模型观点驱动──论文发表时的结果:GPT-4 上 HumanEval pass@1 92.7%(SOTA),GPT-3.5 上 WebShop 平均 75.9(接近基于梯度的微调) ⋅

### MCTS, mínimo

Quatro fases por iteração:

> Cada vez que vierem quatro fases:

1. **Select** caminhar de raiz a folha utilizando UCT (confiança superior ligada às árvores).
   Tradução:**选择**User UCT((são de cima da árvore) da raiz até ao ponto de folha.
2. **Expand** gerar filhos K através da política.
   Tradução:**扩展**Use estratégia gerar K 个子节点──
3. **Simulate** lançamento de uma criança usando a política, pontuação da folha com a função de valor (ou recompensa ambiental).
   Tradução:**模拟**从子节点用策略展开,用价值函数 (从子节点用策略展,用价值函数,或环境奖励) 评分叶节点──
4. **Backpropagate** actualizar os números de visitas e as estimativas de valor do caminho.
   Tradução:**反向传播** A seguir ao caminho, actualizar a contabilidade de visitas e a estimativa de valor.

Formulha da TCC: `Q(s, a) + c * sqrt(ln N(s) / N(s, a))`O primeiro termo é exploração, o segundo exploração.`c`por tarefa.

> UCT 公式:`Q(s, a) + c * sqrt(ln N(s) / N(s, a))`O primeiro é o uso; o segundo é a exploração.`c`- Não.

### A realidade dos custos

A pesquisa explode tokens. ToT em Game of 24 usa 1001000x os tokens de CoT. LATS é semelhante.

> ️ **【易错点】**Veja o ToT em Jogo de 24 上 +70 个点就以为是"银弹",套到所有任务上.**后果**Em simples perguntas e respostas, consome 1000 vezes mais token, em troca de 0% de aumento, o balanço explode.**一行修复**A primeira é a de 10 amostras em relação ao COT vs TOT, e a de 5 pontos é a de apenas "uma trajetória evidente de insuficiência".

> O jogo de 24 horas é 100-1000 vezes mais rápido do que o jogo de 24 horas.

- Tarefas em que uma única trajetória é demonstravelmente insuficiente (Game of 24, código complexo).
  Tradução do inglês:单轨迹明显不足的任务
- Tarefas onde o relógio de parede é menos importante do que a corretão.
  Tradução do inglês:正确性比耗时更重要任务──
- Tarefas com uma função de valor barata e confiável (testes unitários para código, alvo explícito para matemática).
  Tradução do inglês para o inglês: Código de valores (Chinese: 有廉价可靠价值函数的任务)

Se a sua tarefa tem uma única resposta correta e um avaliador barulhento, a pesquisa muitas vezes piora as coisas  encontra uma resposta errada "bom pontuação".

> 🤔 **【困惑】**P: LATS Colocar TOT/ReAct/Reflection 三個都"統一"已經,那不是學了LATS就夠了嗎 A: 不夠──LATS é "重型武器"一次完整搜索要展开上百节点,单任务代币 成本可达百万级── 95% do ambiente de produção 任务使用ReAct + 简单 Reflexion 已够了──LATS apenas em "valor função barata e confiável" como 代码任务的单元测试)

> Se a sua missão tiver apenas uma resposta correta, mas o avaliador tiver ruído, a pesquisa geralmente piora a situação.

> **【中文解读】**搜尋会爆炸 TokenToT em jogo de 24 上消耗 CoT 100-1000 倍. 搜尋:单轨迹明显不足、正确性比速度重要、有廉价可靠的价值函数──搜索可能找到"高分但错误"的答案── Se o avaliador tiver ruído, a pesquisa poderá encontrar a resposta para "高分但错误".

### 2026 posicionamento

A maioria dos agentes de produção não executa LATS. Eles executam ReAct com verificação baseada em ferramentas (CRITIC, lição 05).

> A maioria produz Agente não opera LATS¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

- Agentes de codificação que executam testes como função de valor (estilo HumanEval).
  Em inglês, o código de um valor é o código de um valor.
- Agentes de pesquisa profunda que exploram vários caminhos de consulta.
  Tradução do inglês para tradução do inglês: explorar múltiples quer quer querying pathways' depth study agent.
- Fluxos de trabalho pesados de planejamento dentro dos subgrafos de LangGraph.
  中文翻译:LangGraph 子图内重规划工作流──

AlphaEvolve (Lessão 11) é o extremo de 2025: busca evolutiva sobre código, aptidão verificável por máquina, ganhos de fronteira (primeira melhoria de matmul 4x4 em 56 anos).

> AlphaEvolve (第 11 课) é um exemplo extremista de 2025: desenvolvimento de pesquisa em código, máquina de controle de adaptação, avanço de rotação, em 56 anos, a primeira vez que a quadruplox quadruplox quadruplox é melhorada)

## Construí-lo e realizei-o.
```figure
tree-of-thoughts
```

## Construí-lo

`code/main.py`Implementos:

> `code/main.py`实现:

- Um pequeno ToT BFS numa tarefa estilizada "pick arithmetic ops".
  Tradução do inglês para inglês:
- Um brinquedo LATS MCTS loop na mesma tarefa (Select / Expand / Simulate / Backpropagate) com seleção UCT.
  Tradução do inglês para tradução livre: LATS MCTS 循环 ([[pt:[[pt:[[pt:[[pt:[[pt:[[pt:[[pt:[[pt:[[pt:[[pt:[[pt:[[pt:[[pt:[[pt:[[pt:[[pt:[[pt:[[pt:[[pt:[[pt:pt:[[pt:pt:[[pt:pt:[[pt:pt:pt:[[pt:pt:pt:[[pt:pt:pt:pt:[[pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt:pt
- Uma função de valor que compõe uma pontuação simbólica mais uma pontuação auto-equa.
  Tradução do inglês para o inglês: a···················································································································································································································································································································································

- É o que é ?

> 运行:

```
python3 code/main.py
```

O rastro mostra o ToT expandindo três candidatos por nó com BFS, em comparação com o LATS convergindo no melhor lançamento através do MCTS.

> 轨迹显示 ToT Used BFS Cada um dos pontos é expandido três candidatos, com LATS 通过 MCTS 收到最佳展开对比── ambos imprimidos token 计数──

## Use-o com o framework implementado.

LangGraph envia exploração de estilo ToT como padrões de subgrafos; o blog da equipe LangChain no LATS (maio de 2024) é o tutorial de referência.`TreeOfThoughts`Para a maioria dos agentes de produção de 2026 este padrão vive por trás de um`if task_complexity > threshold: use_search()`gate  ver o padrão de avaliador-optimizador na lição 05.

> LangGraph irá explorar o ToT 风格 como um modelo de gráfico fornecido; LangChain 团队关于 LATS 的博客(2024 年 5 月) é um tutorial de referência.`TreeOfThoughts`Para a maioria dos agentes de produção de 2026, este modelo existe em`if task_complexity > threshold: use_search()`门控后参见第 5 课的评估器-优化器模式──

## Envia-o . Produto .

`outputs/skill-search-policy.md`seleciona entre ReAct linear, ToT, LATS e pesquisa evolutiva dada forma da tarefa, orçamento e fidelidade do avaliador.

> `outputs/skill-search-policy.md`De acordo com a forma de tarefa, orçamento e avaliação, segurança, em linha ReAct, ToT, LATS e desenvolvimento entre pesquisas escolher.

## Exercícios.

1. Execute o LATS com UCT c=0.1 vs c=2.0.
   Tradução do português: Usando UCT c=0.1 和 c=2.0 分别运行 LATS──轨迹有什么变化?
2. A função de valor é substituída por um marcador mais ruidoso (aditar um jitter aleatório).
   Chinese Translation:将价值函数替换为更杂的评分器──MCTS ainda pode encontrar o melhor eije节点?
3. Implementar o ToT de busca de feixe (manter o top-k em cada nível) e comparar com o BFS. Qual é melhor com um orçamento de token apertado?
   Tradução do inglês: implementar beam-search ToT(per layer retain top-k), em comparação com BFS.
4. Leia a secção 5.1. Reproduzir a contagem de trajetória HumanEval: quantas lançamentos é necessário para atingir o pass@1 relatado?
   Chinese Translation: read LATS 第 5.1 节──重现 HumanEval's轨迹数量:达到报告的 pass@1 需要多少次展开?
5. Leia a discussão do artigo LATS sobre "quando o LATS ajuda menos". Escreva uma regra de decisão de um parágrafo mapeando a forma da tarefa para a estratégia de pesquisa.
   Chinese Language Translation: read LATS 论文关于"何时 LATS 帮助不大"的讨论──写一段决策规则映射任务形状到搜索策略──

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Tree of Thoughts | "Branching CoT" / "分支思维链" | Yao et al. — tree of thought nodes with self-evaluation / Yao 等人——带自评估的思维节点树 |
| LATS | "MCTS for LLMs" / "LLM 的 MCTS" | Zhou et al. — unifies ToT + ReAct + Reflexion under MCTS / Zhou 等人——在 MCTS 下统一 ToT+ReAct+Reflexion |
| UCT | "Upper confidence bound" / "上置信界" | Select formula balancing exploitation (Q) and exploration (ln N / n) / 平衡利用(Q)和探索(ln N/n)的选择公式 |
| Value function | "How good is this state" / "状态有多好" | Prompted LLM score or environment reward; feeds backprop / 提示的 LLM 评分或环境奖励；驱动反向传播 |
| Policy | "Action proposer" / "行动提议器" | ReAct-style generator; emits candidate next thoughts/actions / ReAct 风格生成器；发出候选下一步思考/行动 |
| Rollout | "Simulated trajectory" / "模拟轨迹" | Walk from a node to a leaf using policy, score with value / 用策略从节点走到叶节点，用价值函数评分 |
| Backpropagate | "Update ancestors" / "更新祖先" | Push the leaf's reward up the path, updating visit counts and Q / 将叶节点的奖励沿路径上推，更新访问计数和 Q 值 |
| Search cost | "Token explosion" / "Token 爆炸" | 100-1000x CoT on Game of 24; budget before you adopt / Game of 24 上是 CoT 的 100-1000 倍；采用前先做预算 |

## Mais leitura 延伸阅读

- [Yao et al., Tree of Thoughts (arXiv:2305.10601)](https://arxiv.org/abs/2305.10601) o papel canônico
  Tradução do português:
- [Zhou et al., LATS (arXiv:2310.04406)](https://arxiv.org/abs/2310.04406) MCTS com feedback Reflexão
  Tradução do português:LATS带 Reflexion 反的蒙特卡洛树搜索──
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) Padrões de subgráficos para pesquisa
  中文翻译:LangGraph 概览搜索的子图模式──
- [AlphaEvolve (arXiv:2506.13131)](https://arxiv.org/abs/2506.13131) Pesquisa evolutiva com avaliadores programáticos
  Tradução do inglês para tradução livre:AlphaEvolve带程序化评估器的进化搜索──
