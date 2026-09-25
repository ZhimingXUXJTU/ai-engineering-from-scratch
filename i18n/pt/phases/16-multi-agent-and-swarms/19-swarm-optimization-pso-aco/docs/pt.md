# Otimizar o grupo para LLM (PSO, ACO) 优化群体 PSO ACO LLM

> A otimização bio-inspirada está a fazer um retorno de LLM. **LMPSO**(arXiv:2504.09247) usa PSO onde a velocidade de cada partícula é um prompt e o LLM gera o próximo candidato; funciona bem em saídas de sequência estruturada (expressões matemáticas, programas). **Model Swarms**(arXiv:2410.11163) trata cada especialista em LLM como uma partícula de PSO num variável de peso de modelo e apresenta relatórios **13.3% average gain**mais de 12 linhas de base em 9 conjuntos de dados com apenas 200 instâncias. **SwarmPrompt**(ICAART 2025) hibrida PSO + Grey Wolf para otimização rápida. **AMRO-S**(arXiv:2603.12933) é especialista em feromônios inspirado em ACO para roteamento de LLM multi-agente  **4.7x speedup**Esta lição implementa o PSO no espaço de parâmetros rápidos e o ACO no roteamento de agentes, mede por que esses algoritmos clássicos se encaixam na era do LLM e quando não.

> **【中文解读】**Esta secção apresenta o algoritmo de otimização de grupos de partículas (PSO) e ACO (ACO) e a aplicação de organismos como a otimização em vários agentes (Multi-Agent).

> **【拓展：swarm optimization pso aco→具体应用】**群体优化算法在多代理中的应用:(1) 粒子群优化(PSO) Agent 根据自身最佳位置和全局最佳位置调整搜索方向;(2) 群群优化(ACO) Agent 通过信息素标记好的路径,后者倾向于遵循强信息素路径──这些算法适合大规模搜索空间中的优化问题,如 Agent 任务分配和路径规划──


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 09 (Parallel Swarm Networks), Phase 16 · 14 (Consensus and BFT) | **前置知识:** Phase 16 · 09（并行群体网络），Phase 16 · 14（共识与 BFT）

> - Não .**【前置】**O que é que você tem a ver com o seu computador?
> - Não .**【类比】**LLM + PSO/ACO = "群找最佳快点"──PSO = Cada Agente é uma partícula, velocidade=prompto, para toda a área;ACO = Agente em tempo rápido 空间留下信息素,后者跟随强信息素──LMPSO 适合结构化输出(matemática expressão、代码);Model Swarms Colocar cada LLM 专家当粒子,比 12 个基线平均高13.3%;AMRO-S usando ACO fazer agente 路由,4.7 倍加速──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problema Introdução

Você tem um prompt que marca 62% em sua avaliação de tarefa. Você quer melhorar. O movimento ingênuo é ajustar manual sem gradiente, o que escala mal. A aprendizagem de reforço precisa de sinais de recompensa e implementações suficientes para treinar. Backprop através de prompts não é realmente possível  o prompt é uma cadeia discreta, não um parâmetro diferenciável.

> Você tem uma dica em avaliação de tarefa que tem 62% de pontuação. Você quer melhorá-la. O método simples é o ajuste manual sem gradiente, a expansão de diferença.

Otimizar bio-inspirado clássico  PSO para espaços de pesquisa contínua, ACO para seleção de caminho  foi projetado exatamente para este regime: livre de gradientes, baseado na população, barato por avaliação.

> O PSO é usado para o espaço de pesquisa contínua, o ACO é usado para a seleção de caminhos que são concebidos para esse cenário: sem gradiente, baseado em grupos, baixo custo de avaliação por avaliação.

Os mesmos padrões se aplicam ao agente *routing* em sistemas multi-agentes. Um feromônio de estilo ACO registra o agente que mais funcionou em que tipo de tarefa, permite que o roteador explore o rastro e decompõe feromônios para que as rotas possam ser redescobertas.

> O mesmo modelo é aplicável ao Agente em sistemas multi-agente *rouagem*。 ACO 风格的信息素轨迹记录哪个Agente melhor se apresenta em que tipo de missão,让路由器利用轨迹,并衰减信息素以便重新发现路径──

## Conceptos básicos

### Refrescador do PSO (Kennedy & Eberhart 1995)

Otimizar o enxame de partículas: população de partículas num espaço de busca contínua.`x_i`e velocidade.`v_i`- Cada iteração:

```
v_i <- w * v_i + c1 * r1 * (p_best_i - x_i) + c2 * r2 * (g_best - x_i)
x_i <- x_i + v_i
evaluate fitness(x_i)
update p_best_i if improved
update g_best if global best
```

Onde ?`p_best`é o melhor da partícula,`g_best`É o melhor do enxame.`w, c1, c2`são a inercia + o cognitivo + os pesos sociais, `r1, r2`são fatores aleatórios.

### OPS sobre resultados de LLM  LMPSO

ArXiv:2504.09247 adapta PSO para saídas estruturadas geradas pela LLM (expressões matemáticas, programas). Cada partícula é uma saída candidata. Velocidade é um *prompt* que descreve como modificar a saída atual para o melhor pessoal / global. O LLM gera a nova saída a partir do prompt de velocidade. A "inertia" da velocidade é um prompt como "fazer pequenas mudanças incrementais".

Isto funciona bem quando:
- A saída é estruturada (percebível, avaliável).
  Tradução do inglês para tradução livre:
- A forma é automática (teste de corridas, avaliação aritmética).
  Tradução do inglês para o inglês:                                                                                                                                                                                                                                                          
- A população é pequena (~ 10-30 partículas), por isso as chamadas de LLM totais permanecem gerenciáveis.
  Tradução em inglês: 种群小(约10-30 个粒子),总 LLM 调用可控。

Não funciona bem quando a forma física precisa de revisão humana  o custo da per-iteration torna-se proibitivo.

> Quando a adaptação requer revisão artificial, o efeito é ruim.

### Modelo de Enxames

O arXiv:2410.11163 tira o PSO da camada de saída para a camada de modelo. Cada "partícula" é um LLM especialista (parâmetros). O enxame move os parâmetros para o melhor coletivo através de uma atualização sem gradiente.

A principal ideia é que os modelos de especialistas em LLM já estão próximos num variável parâmetro compartilhado (pesos de adaptadores, deltas de LoRA).

### Acondicionamento de água (Dorigo 1992)

A melhor forma de fazer uma colônia de formigas é através de um gráfico; cada caminho tem uma trilha de feromônios. As formigas movem as probabilidades de peso por força de feromônios. As formigas que completam a tarefa depositam feromônios proporcionais à qualidade da solução.

### AMRO-S  ACO para encaminhamento de agentes

ArXiv:2603.12933 usa ACO para roteamento multi-agente. Cada tipo de tarefa é um "destino"; cada agente é uma rota possível. Feromônios fortalecem rotas que produzem bons resultados. Contribuições principais:

- **Interpretable routing evidence.**A força feromônica é um sinal legível ao homem.
  Tradução:**可解释的路由证据。**A intensidade da informação é um sinal que é lido pelo homem.
- **Quality-gated asynchronous update.**As feromônios atualizam-se apenas após a aprovação dos controlos de qualidade, desacoplando a inferência da aprendizagem.
  Tradução:**质量门控异步更新。**O material só será atualizado após o teste de qualidade, será analisado e aprendido.
- **4.7x speedup**sobre o indicador de referência de roteamento para vários agentes.
  Tradução do inglês:**4.7 倍加速**- Não.

A porta de qualidade importa: sem ela, agentes rápidos mas errados acumulam feromônio, e o sistema bloqueia rotas ruins.

> 質量門很重要: sem ele, Rapid but erroneous Agent 会积累信息素, sistema bloqueado em um caminho ruim.

### Quando utilizar PSO/ACO para LLM

**Use PSO when:**
- O espaço de pesquisa é contínuo ou mapeia para parâmetros contínuos (embeddings de prompt, pesos de LoRA, parâmetros de geração numérica).
  Chinese: 搜索空间是连续的或映射到连续参数 (se busca espaço é continuado ou mapeado até a continuação de parametros)
- A forma física é barata e automática.
  Tradução do inglês:适应度评估廉价且自动.
- A população pode ser pequena (10-30).
  Tradução do inglês: 种群可以很小 ((10-30) ⋅

**Use ACO when:**
- Tem um problema de roteamento ou de selecção de caminho.
  Tradução do inglês:You have a pathway or pathway choice problem.
- As decisões reforçam-se ao longo do tempo (os mesmos tipos de tarefas voltam).
  Chinese:                                                                                                                                                                                                                                                              
- Precisas de provas interpretáveis para as decisões de roteamento.
  Tradução do inglês:You need route by decision

**Do not use either when:**
- A aptidão física requer revisão humana (demasiada por iteração).
  Tradução do inglês: 适应度需要人工审查 (适应度需要人工审查)
- O espaço de pesquisa é discreto e combinatório de uma forma que o PSO não cobre (use algoritmos genéticos em vez disso).
  O PSO 无法覆盖 (PSO 无法覆盖) é um sistema de pesquisa de dados.
- As decisões em tempo real necessitam de uma latença rigorosa (PSO/ACO convergem lentamente em relação às heurísticas de passagem única).
  O processo de decisão precisa ser muito lento.

### Por que a bio-inspiração ainda vence

Os métodos baseados em gradientes precisam de sinais diferenciáveis. As saídas do LLM e as decisões de roteamento não são triviais. Os métodos pseudo-gradientes (routers de reforço, sintonizadores de prompt no estilo DPO) funcionam, mas precisam de treinamento caro.

PSO e ACO precisam apenas de uma função de *evaluador* . Se você pode marcar uma saída candidata ou uma decisão de roteamento, você pode otimizar o espaço. Isso torna a barra de aplicabilidade muito menor.

### Limite prático

- **Population budget.**N partículas × T iterações × custo por eval. Para avaliações LLM em ~$0.02 / call, a 20-particle PSO running 50 iterations costs ~$20. Planeje em conformidade.
- **Exploration vs exploitation.**A taxa de decomposição feromônica e a inércia do PSO trocam-se; decomposição demasiado rápida → esqueça soluções; muito lenta → pegou em ótimas locais iniciais.
- **Catastrophic drift.**Os dois algoritmos podem convergir e depois divergir se a paisagem de fitness mudar (nova distribuição de dados).

## Construí-lo.
```figure
swarm-stigmergy
```

## Construí-lo

`code/main.py`Implementos:

- `LMPSO` PSO sobre parâmetros de prompt numérico (temperatura, pesos top_k). A "geração LLM" de cada partícula é simulada como uma função de fitness scripted.
- `AMRO_S` Routing de estilo ACO. 3 agentes, 4 tipos de tarefas, matriz feromônica, 100 tarefas enrutadas. Impressões (task_type → opções de agentes) distribuição ao longo do tempo para mostrar a formação de trilha.
- Comparação: roteamento aleatório vs roteamento ACO no mesmo fluxo de tarefas.

- Correr .

```
python3 code/main.py
```

Produção esperada:
- LMPSO: g_best fitness melhora de aleatório para quase ótimo em mais de 30 iterações.
- AMRO-S: a tabela de feromonas estabiliza-se no agente certo por tipo de tarefa; o roteamento ACO bate aleatoriamente em ~ 30-40% na qualidade e também reduz a latência (menos retrospectivas).

## Usa-o. Usa-o.

`outputs/skill-swarm-optimizer.md`ajuda a escolher entre PSO, ACO, algoritmos genéticos e optimizadores baseados em gradientes para problemas de otimização de LLM / agente.

## Envia-o .

- **Start small.**10-20 partículas, 20 a 50 iterações.
  Tradução:**从小开始。**10-20 partículas, 20-50 vezes 代── apenas na curva de recepção mostram um aumento evidente quando é expandido──
- **Log pheromones or g_best per iteration.**Desembaraçar os optimizadores sem rastro é doloroso.
  Tradução:**每次迭代记录信息素或 g_best。**Não há nenhum caminho para o mundo.
- **Quality-gate updates.**Especialmente para o encaminhamento ACO: agentes rápidos e errados não devem acumular feromona.
  Tradução:**质量门控更新。**Especialmente ACO 路由: Rapid, mas errôneo Agente não consegue acumular informação.
- **Reset decay on distribution shift.**Quando a distribuição da avaliação muda, as feromônios envelhecidos ficam obsoletas; restabeleça ou duplique temporariamente a taxa de decomposição.
  Tradução:**分布偏移时重置衰减。**Quando a avaliação da variação da distribuição, a taxa de envelhecimento da informação é ultrapassada;
- **Cap the per-iteration cost.**Emite uma métrica de custo por iteração. O PSO que custa $500 / iteração e ganha 0,5% não é enviável.
  Tradução:**限制每次迭代成本。**发发每次代成本指标──每次代耗费$500 且只增加0.5% 的PSO不可发行──

## Exercícios.

1. Corra .`code/main.py`Observe a convergência do LMPSO. Dimensão populacional variar 5, 10, 20, 50.
2. Implementar um experimento de "drift catastrófico": após a iteração 30, alterar a função de fitness.`p_best`- Ajuda?
3. Adicionar um gate de qualidade para AMRO-S: depósito de feromônio apenas em corridas com pontuação de avaliação > 0,7. Como isso muda a convergência versus a versão não-gated?
4. Leia LMPSO (arXiv:2504.09247). Mapeia da "velocidade do papel como um prompt" de volta à sua velocidade numérica. O que é perdido na simulação e o que é preservado?
5. Leia AMRO-S (arXiv:2603.12933). Implementar o "caminho rápido de inferência" descoplado com atualização feromônica assíncrona. Como isso muda a latência do sistema sob carga sustentada?

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| PSO / 粒子群优化 | "Particle Swarm Optimization" / "粒子群优化" | Kennedy-Eberhart 1995. Population-based gradient-free optimizer. / Kennedy-Eberhart 1995。基于种群的无梯度优化器。 |
| ACO / 蚁群优化 | "Ant Colony Optimization" / "蚁群优化" | Dorigo 1992. Path/route optimization via pheromone trails. / Dorigo 1992。通过信息素轨迹的路径/路由优化。 |
| LMPSO / LLM 粒子群 | "PSO with LLM generation" / "LLM 生成的 PSO" | arXiv:2504.09247. Velocity is a prompt; LLM produces candidates. / arXiv:2504.09247。速度是提示；LLM 生成候选。 |
| Model Swarms / 模型群体 | "PSO on expert weights" / "专家权重的 PSO" | arXiv:2410.11163. Gradient-free update on model parameter subspace. / arXiv:2410.11163。模型参数子空间上的无梯度更新。 |
| AMRO-S / ACO Agent 路由 | "ACO for agent routing" / "Agent 路由的 ACO" | arXiv:2603.12933. Pheromone matrix over task-type × agent. / arXiv:2603.12933。任务类型 × Agent 的信息素矩阵。 |
| p_best / g_best / 个体最优/全局最优 | "Personal / global best" / "个人/全局最优" | Per-particle and swarm-wide best solutions found so far. / 每个粒子和群体目前找到的最优解。 |
| Pheromone / 信息素 | "Routing memory" / "路由记忆" | Strength on an edge; decays over time; deposits on quality. / 边上的强度；随时间衰减；按质量沉积。 |
| Quality-gated update / 质量门控更新 | "Only learn from good runs" / "只从好的运行学习" | Pheromone deposit conditioned on quality check. / 以质量检查为条件的信息素沉积。 |
| Catastrophic drift / 灾难性漂移 | "Distribution shift" / "分布偏移" | Fitness landscape changes; old p_best and pheromones become stale. / 适应度景观变化；旧的 p_best 和信息素变得过时。 |

## Mais leitura 延伸阅读

- [Kennedy & Eberhart — Particle Swarm Optimization](https://ieeexplore.ieee.org/document/488968) O documento da OPS de 1995
- [Dorigo — Ant Colony Optimization](https://www.aco-metaheuristic.org/about.html) 1992 Fundações da ACO
- [LMPSO — Language Model Particle Swarm Optimization](https://arxiv.org/abs/2504.09247) OPS para resultados estruturados de MLL
- [Model Swarms — gradient-free LLM expert optimization](https://arxiv.org/abs/2410.11163) PSO no subespaço de peso do modelo
- [AMRO-S — ant-colony multi-agent routing](https://arxiv.org/abs/2603.12933) Roteamento a base de feromonas com porta de qualidade
