# MARL  MADDPG, QMIX, MAPPO  MADDPG MAPPO MARL QMIX

> O património de aprendizagem reforçada da coordenação multi-agente, que ainda informa os sistemas de LLM-agente em 2026. **MADDPG**(Lowe et al., NeurIPS 2017, arXiv:1706.02275) introduziu Treinamento Centralizado, Execução Descentralizada (CTDE): cada crítico vê todos os estados e ações dos agentes durante o treinamento; no momento do teste apenas atores locais executam.**QMIX**(Rashid et al., ICML 2018, arXiv:1803.11485) é a decomposição de valor com uma rede de mistura monótona; por agente Qs combinam em conjunto Q assim `argmax`distribui limpo  dominante no StarCraft Multi-Agent Challenge (SMAC). **MAPPO**(Yu et al., NeurIPS 2022, arXiv:2103.01955) é um PPO com uma função de valor centralizada; "surpreendentemente eficaz" no mundo das partículas, SMAC, Google Research Football, Hanabi com ajuste mínimo.**default 2026 cooperative-MARL baseline**Esta lição construiu cada um a partir de um pequeno brinquedo de rede-mundo e faz com que as três ideias se encaixem na memória muscular antes de tocar no treinamento de agente LLM.

> **【中文解读】**Este capítulo apresenta o multi-agent 强化学习MADDPG、QMIX、MAPPO etc. Multi-agent RL 算法。

> **【拓展：marl maddpg qmix mappo→具体应用】**Do Agente 强化学习(MARL) algoritmo:(1) MADDPG cada Agente tem um Actor-Critico independente, mas o Crítico pode ver todos os movimentos do Agente;(2) QMIX concentração de treinamento executado de forma dispersa, através de mistura de rede de garantia de união;(3) MAPPOPPO 多 Agent 扩展──2026 MARL avançou no jogo AI、机器人协作与交通控制, mas a aplicação no LLM Agente ainda está no início.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, small NumPy-free implementations) | **语言:** Python（标准库，无 NumPy 的小型实现）
**Prerequisites:** Phase 09 (Reinforcement Learning), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 09（强化学习），Phase 16 · 09（并行群体网络）

> - Não .**【前置】**學本節前 請先掌握:Fase 09 (RL 基礎 PPO/Q-learning) 、Fase 16·09 (Swarm) │MARL = 多 Agent 强化学习,CTDE(集中訓練分散执行) │
> - Não .**【类比】**MARL = "entrenamento da equipa"―MADDPG = 教练看全场训练(集中评论), competição时球员各自决策(分散演员);QMIX = Cada pessoa um Q 值,单调混合保证最优解可分;MAPPO = PPO多 Agent 版本──MAPPO 是 2026 合作 MARL 默认基线("surprisingly effective"),SMAC、Google Football、Hanabi 都能少调参跑通──LLM Agent training 借鉴也借鉴这套范式──
**Time:** ~90 minutes | **时间:** ~90 分钟

## Problema Introdução

Os sistemas de LLM-agentes treinam cada vez mais políticas para a coordenação entre agentes: quando adiar, quando agir, que peer para chamar. A literatura que diz como treinar essas políticas é o Multidimensional Reforço de Aprendizagem (MARL), que antecede a onda de LLM e tem um pequeno conjunto de algoritmos dominantes.

> O programa de treinamento de agentes é muito mais frequente do que o programa de treinamento de agentes, mas é muito mais antigo do que o programa de treinamento de agentes, com um grupo de algoritmos de direção.

A leitura de artigos MARL sem o vocabulário padrão é dolorosa.

> Não há modo de expressão para ler o MARL 论文是痛苦的;;集中训练分散执行;;CTDE) 价值分解和集中式评论家不是流行词它们是特定问题的特定答案:

- A RL independente (cada agente aprende sozinho) não é estacionária, do ponto de vista de cada agente.
  Tradução do inglês para RL (RL) (de língua inglesa: RL)
- A RL centralizada (um agente controla todos) não escala e viola as restrições de execução.
  Tradução do inglês: RL (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL)) (RL) (RL) (RL)) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (RL) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R)
- O CTDE obtém o melhor dos dois: treinar com informações globais, implementar com políticas locais.
  O CTDE 兼得两者之长: Usando o treinamento de informação da área, Usando a estratégia da área.

## Conceptos básicos

### Três ambientes que os artigos usam

- **Particle World (multi-agent particle env).**Física 2D simples com tarefas cooperativas/competitivas.
- **StarCraft Multi-Agent Challenge (SMAC).**Micro-gestão cooperativa, observação parcial, teste de QMIX, ações discretas, estados contínuos.
- **Google Research Football, Hanabi, MPE.**Linhas de base do MAPPO.

Diferentes ambientes têm diferentes tipos de ação/observação.

### MADDPG (2017)  o padrão CTDE

Cada agente .`i`Tem um ator.`mu_i(o_i)`O que é que é o que é preciso para que o Parlamento possa fazer?`Q_i(x, a_1, ..., a_n)`O ator é actualizado por gradiente de política contra a avaliação do crítico.

```
actor update:    grad_theta_i J = E[grad_theta mu_i(o_i) * grad_a_i Q_i(x, a_1..n) at a_i=mu_i(o_i)]
critic update:   TD on Q_i(x, a_1..n) given next-state joint estimate
```

Por que CTDE: no tempo de treinamento, conhecemos as ações de todos; usamos isso para reduzir a variância em cada crítico.`o_i`e chamadas .`mu_i(o_i)`- Não .

Modo de falha: os críticos crescem com N agentes (a entrada inclui todas as ações). Não escala além de ~ 10 agentes sem aproximações.

### QMIX (2018)  decomposição de valor

A recompensa global é a soma de uma função monótona de valores Q por agente:

```
Q_tot(tau, a) = f(Q_1(tau_1, a_1), ..., Q_n(tau_n, a_n)),   df/dQ_i >= 0
```

A monotonia garante `argmax_a Q_tot`Pode ser calculado por cada agente escolhendo`argmax_{a_i} Q_i`Independentemente.**exactly the decentralized execution property**No momento do treino, uma rede de mistura produz`Q_tot`do Qs por agente.

Por que a QMIX vence o SMAC: a micro-gestão cooperativa StarCraft tem agentes homogéneos, obs local, recompensa global  perfeita para a decomposição de valor.

Modo de falha: a restrição de monotonia é restritiva; algumas tarefas têm estruturas de recompensa que não são monotones decomposíveis (um agente sacrificando para a equipe).

### MAPPO (2022)  o padrão negligenciado

Multi-Agent PPO: PPO com uma função de valor centralizada. Cada agente tem sua própria política; todos os agentes compartilham (ou têm por agente) funções de valor que veem o estado completo. Yu et al. 2022 compararam MAPPO contra MADDPG, QMIX e suas extensões em cinco benchmarks e encontraram:

- O MAPPO corresponde ou supera os métodos MARL fora da política no mundo das partículas, SMAC, Google Research Football, Hanabi, MPE.
- Requer-se ajuste mínimo de hiperparâmetros.
- Treinamento estável; reprodutivel entre as sementes.

A comunidade subestimou a MARL política até este artigo. Em 2026, o MAPPO é a linha de base padrão para a MARL cooperativa; qualquer novo método deve vencê-lo.

### Por que os engenheiros de LLM-agentes devem se preocupar

Três usos directos:

1. **Router training.**Um meta-agente escolhe qual sub-agente lida com uma tarefa. Este é um problema MARL com N sub-agentes descentralizados e um roteador centralizado.
2. **Role emergence.**Em simulações de agentes geradores, os agentes de formação para adotar papéis complementares ao longo do tempo é um problema MARL disfarçado.
3. **Multi-agent tool use.**Quando os agentes compartilham ferramentas e competem por orçamento, a formação através do CTDE produz políticas locais implementáveis que respeitam as restrições de recursos.

A advertência prática: em 2026, a maioria dos sistemas de agentes LLM de produção incentiva suas políticas em vez de treiná-los.

### CTDE como padrão de projeto além do RL

Mesmo sem formação, o CTDE é um padrão arquitectónico útil:

- Durante o *design*, assumir a visibilidade total da equipa.
- No * runtime*, aplicar execução descentralizada: cada agente vê apenas `o_i`- Não .

O padrão obriga você a manter o estado por agente explícito e a pensar na observabilidade parcial de antemão.

### O problema da não estacionalidade

Quando vários agentes aprendem simultaneamente, o ambiente de cada agente (que inclui as políticas dos outros) é não estacionário.

- MADDPG: O crítico global vê todas as ações, por isso a sua estimativa de valor é estacionária.
- QMIX: a decomposição de valores move a aprendizagem para um espaço conjunto de Q onde a otimilidade é bem definida.
- MAPPO: a função de valor centralizado diminui a variação das alterações políticas dos outros.

Nos sistemas de agentes LLM, a não estacionalidade manifesta-se como "meu agente trabalhou no mês passado, agora que outro agente upstream mudou, a mina se comporta mal".

### O que esta lição NÃO abrange

A formação de redes reais é um tópico da Fase 9. Esta lição constrói versões de políticas scriptadas que demonstram os padrões de CTDE, decomposição de valor e valor centralizado sem atualizações de gradiente. O objetivo é internalizar os padrões antes de pegar uma biblioteca MARL completa (PyMARL, MARLlib, RLlib multi-agente).

## Construí-lo.
```figure
sw-ctde
```

## Construí-lo

`code/main.py`Implementa três demonstrações de padrão, todas em um pequeno mundo cooperativo de duas pessoas:

- Ambiente: 2 agentes numa grade 4x4, um pellet de recompensa.
  Tradução do inglês: ambiente: 2 个代理在 4x4 网格上,一个奖励颗粒──任何代理到达颗粒则奖励 = 1;任务结束──
- `IndependentAgents`- cada agente trata os outros como ambiente.
  Tradução:`IndependentAgents`Cada agente vai ser outro agente, visto o ambiente.
- `MADDPGStyle` O crítico centralizado calcula um valor comum; as políticas dos atores atualizam-se a partir dele.
  Tradução:`MADDPGStyle` 集中式评论家计算联合值;Actor 策略从中更新──脚本化策略改进──
- `QMIXStyle` decomposição de valor com um misturador monótono.
  Tradução:`QMIXStyle` 带单调混合器的值分解──
- `MAPPOStyle` Função de valor centralizada; atualização das políticas em relação à linha de base compartilhada.
  Tradução:`MAPPOStyle` 集中式值函数;策略对共享基线更新──

Os quatro episódios executam os mesmos episódios e relatam os passos médios para o objetivo.

> Todos os quatro circuitos da mesma linha de rotação e relatam a média de atender aos objetivos.

- Correr .

```
python3 code/main.py
```

A saída esperada: agentes independentes levam ~6 passos em média; as variantes CTDE convergem para ~3.5 passos (ótimo para a grade 4x4 é 3). A diferença de padrão aparece apesar das políticas scripted.

## Usa-o. Usa-o.

`outputs/skill-marl-picker.md`é uma habilidade que seleciona um algoritmo MARL para uma determinada tarefa multi-agente: cooperativa vs competitiva, homogênea vs heterogênea, tipo de espaço de ação, escala, sinal de recompensa.

## Envia-o .

A MARL em produção é rara.

- **Start with MAPPO.**O artigo de 2022 estabeleceu isso como a linha de base; reproduzi-lo primeiro poupa semanas de perseguir métodos mais sofisticados.
  Tradução:**从 MAPPO 开始。**O artigo de 2022 será estabelecido como base; antes de se repetir, pode economizar semanas em busca de métodos mais sofisticados.
- **Log every agent's observation and action stream.**Desembaraçar o MARL sem vestígios de agentes é desesperado.
  Tradução:**记录每个 Agent 的观察和动作流。**Não há nenhum agente que possa fazer o teste de MARL.
- **Separate training code from execution code.**O CTDE é uma disciplina; deixe o caminho de execução realmente ver apenas`o_i`- Não .
  Tradução:**分离训练代码和执行代码。**O CTDE é uma forma de regra; fazer executar o caminho realmente só ver`o_i`- Não.
- **Reward shaping warning.**A MARL é extremamente sensível ao design de recompensas, um erro de coordenação no moldamento e os agentes aprendem a explorá-lo.
  Tradução:**奖励塑形警告。**MARL para o design de prêmio é extremamente sensível. Um bug de coordenação em forma de plástico permite ao agente aprender a usá-lo.
- **For LLM agents**Investi em formação MARL apenas quando os dados de interação + sinal de recompensa + infraestrutura estiverem todos presentes.
  Tradução:**对于 LLM Agent**, primeiro considerar estratégias de nível de informação e de informação.

## Exercícios.

1. Corra .`code/main.py`- Medir a lacuna de passos para metas entre agentes independentes e de tipo MAPPO.
2. Implementar uma variante competitiva: dois agentes, uma pellet, apenas o primeiro a alcançar recebe recompensa.
3. Leia MADDPG (arXiv:1706.02275) Secção 3. Implementar a regra de atualização crítica exata simbólicamente em pseudocódia em suas próprias palavras.
4. Leia MAPPO (arXiv:2103.01955). Por que os autores argumentam que o valor centralizado + PPO supera o MARL fora da política em seus índices de referência?
5. Aplicar CTDE como padrão de projeto para um sistema hipotético de agente LLM (por exemplo, agente de pesquisa + resumidor + codificador).

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MARL / 多 Agent 强化学习 | "Multi-Agent RL" / "多 Agent 强化学习" | Reinforcement learning for multi-agent systems. / 多 Agent 系统的强化学习。 |
| CTDE / 集中训练分散执行 | "Centralized Training, Decentralized Execution" / "集中训练分散执行" | Train with global info; deploy with local policies. / 用全局信息训练；用局部策略部署。 |
| MADDPG | "Multi-Agent DDPG" / "多 Agent DDPG" | CTDE with per-agent critic seeing all observations + actions. / CTDE，每个 Agent 的评论家看到所有观察 + 动作。 |
| QMIX / 值分解 | "Value decomposition" / "值分解" | Monotonic mixing of per-agent Qs. Cooperative. / 每 Agent Q 的单调混合。协作型。 |
| MAPPO / 多 Agent PPO | "Multi-Agent PPO" / "多 Agent PPO" | PPO with centralized value function. 2026 default baseline. / 带集中式值函数的 PPO。2026 默认基线。 |
| Value decomposition / 值分解 | "Sum of individual Qs" / "个体 Q 之和" | Joint Q represented as a monotone function of per-agent Qs. / 联合 Q 表示为每 Agent Q 的单调函数。 |
| Non-stationarity / 非平稳性 | "Moving targets" / "移动目标" | Each agent's env changes as others learn. The core MARL problem. / 每个 Agent 的环境随着其他 Agent 学习而变化。核心 MARL 问题。 |
| On-policy / off-policy / 同策略/离策略 | "Learn from current / replay" / "从当前/回放学习" | PPO is on-policy (MAPPO); DDPG and Q-learning are off-policy. / PPO 是同策略（MAPPO）；DDPG 和 Q-learning 是离策略。 |
| SMAC / 星际争霸多 Agent 挑战 | "StarCraft Multi-Agent Challenge" / "星际争霸多 Agent 挑战" | Cooperative micromanagement benchmark; QMIX's homegrown ground. / 协作微操基准；QMIX 的主战场。 |

## Mais leitura 延伸阅读

- [Lowe et al. — Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments](https://arxiv.org/abs/1706.02275) MADDPG; NeurIPS 2017
- [Rashid et al. — QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning](https://arxiv.org/abs/1803.11485) QMIX; ICML 2018
- [Yu et al. — The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games](https://arxiv.org/abs/2103.01955) MAPPO; NeurIPS 2022
- [BAIR blog post on MAPPO](https://bair.berkeley.edu/blog/2021/07/14/mappo/) Enquadramento legível do resultado do MAPPO
- [SMAC repository](https://github.com/oxwhirl/smac) StarCraft Multi-Agent Challenge
