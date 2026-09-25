# Multidistribuição de RL.

> O RL de agente único assume que o ambiente é estacionário. Coloque dois agentes de aprendizagem no mesmo mundo e essa suposição quebra: cada agente é parte do ambiente do outro, e ambos estão mudando.

> **【中文解读】**单智能体 RL 假设环境是平稳的──但放入两个同时学习的智能体后, cada智能体都成为对方环境的一部分环境不再平稳,马尔可夫假设被打破──多智能体 RL 就是处理"todos estão em mudança"的问题──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 04 (Q-learning), Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic) | **前置知识:** Phase 9 · 04 (Q-learning), Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic)
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

Um robô que aprende a navegar em uma sala é um problema de RL de um único agente. Uma equipe de futebol não é.

> O sistema de navegação é um problema único. O sistema de navegação é um problema único. O sistema de navegação é um problema único.

Em cada ambiente multi-agente, a partir da perspectiva de qualquer agente, os outros agentes são parte do ambiente. À medida que aprendem e mudam o comportamento, o ambiente torna-se não-estacionário. A propriedade Markov  "o próximo estado depende apenas do estado atual e da minha ação"  é violada porque o próximo estado também depende do que os outros agentes escolheram, e suas políticas estão movendo alvos.

> Em cada ambiente multi-inteligente, do ponto de vista de cada um, outros inteligentes são parte do ambiente. Quando eles aprendem e mudam de comportamento, o ambiente se torna instável. A capacidade de manejar é violada, porque o estado seguinte também depende da escolha de outros inteligentes, enquanto sua estratégia é o objetivo móvel.

O que é preciso é que os agentes se perseguam uns aos outros em circuitos, nunca convergem para uma política estável.

> Isso destruiu o padrão de receção de prova ([[Q-learning]]s assumptions of assurance assumptions of a stable environment) ∼ também destruiu a simples profundidade RL: os inteligentes se perseguem mutuamente, nunca recebem a estratégia de estabilização ∼ você precisa de vários inteligentes técnicas especiais: concentração de treinamento/ distribuição de execução ∼ antifactos base line ∼ aliança de treinamento ∼ auto-exploração ∼

Aplicações 2026: enxames de robôs, roteamento de tráfego, frotas de veículos autônomos, simuladores de mercado, sistemas LLM multi-agente (fase 16), e qualquer jogo com mais de um jogador inteligente.

> Aplicação 2026: máquinas, grupos de pessoas, transportes, equipes de condução automática, mercados, modelos, sistemas de LLM multi-inteligentes, fase 16), bem como qualquer jogo com vários jogadores inteligentes.

> **【中文解读】**O desafio central do RL do 多智能体:非平稳性 (非平稳性) 其他智能体也在学习) 信用分配 (信用分配) 谁应得到奖励?) 联合动作空间爆炸、部分可观察性──四种主要范式:独立学习 (独立学习) 简单但不保证收) 、CTDE (entrenamento时集中、执行时分布) 、自我博 (AlphaZero) 、联盟 (联盟) 训练 (AlphaStar) ∼

> **【拓展：多智能体→LLM Agent系统】**A aplicação mais popular de MARL em 2026 é o multi-inteligente LLM: Multi Modelo Agent 协作完成复杂任务――Module multi-agent 模式、AutoGen、CrewAI e outros quadros são, em essência, uma extensão do pensamento MARL no domínio da linguagem Agent.

## O conceito central.

![Four MARL regimes: indep, centralized critic, self-play, league](../assets/marl.svg)

**Formalism: Markov Game.**Uma generalização do MDP: estados `S`, uma acção conjunta `a = (a_1, …, a_n)`, transição `P(s' | s, a)`, e recompensas por agente `R_i(s, a, s')`Cada agente .`i`maximiza o seu próprio retorno sob a sua própria política `π_i`Se as recompensas forem idênticas, é o caso.**fully cooperative**Se for zero, é o mesmo.**adversarial**Se misturado, é.**general-sum**- Não .

> **形式化：马尔可夫博弈。**MDP 的推广: estado `S`、                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            `a = (a_1, …, a_n)`、 transferência `P(s'|s,a)`、 recompensa de cada corpo inteligente `R_i`Se as recompensas forem as mesmas,**全合作**Se é zero e, é**对抗**Se misturado, é**一般和**- Não.

**Core challenges:**

- **Non-stationarity.** `P(s' | s, a_i)`do agente .`i`A visão depende de`π_{-i}`, que está a mudar.
  **非平稳性。**De inteligência`i`O transmissão depende da estratégia de outros seres inteligentes em mudança.
- **Credit assignment.**Com uma recompensa compartilhada, qual agente causou isso?
  **信用分配。**Quando a recompensa é compartilhada, qual é o resultado?
- **Exploration coordination.**Os agentes devem explorar estratégias complementares, não explorar redundantemente o mesmo estado.
  **探索协调。**O corpo inteligente deve explorar estratégias complementares, e não explorar excessivo o mesmo estado.
- **Scalability.**O espaço de acção comum cresce exponencialmente em `n`- Não .
  **可扩展性。**联合动作空间随 `n`O número de pessoas que estão a morrer.
- **Partial observability.**Cada agente vê apenas a sua própria observação; o estado global está oculto.
  **部分可观察性。**Cada corpo inteligente só vê sua própria observação; o estado da situação está oculto.

**Four dominant regimes:**

> **四种主导范式：**

**1. Independent Q-learning / independent PPO (IQL, IPPO).**Cada agente aprende sua própria Q ou política, tratando os outros como parte do ambiente. Simples, às vezes funciona (especialmente com repetição de experiência agindo como um truque de modelagem de agente suave). Convergência teórica: nenhuma. Na prática: bom para tarefas soltos, ruim para as fortemente acopladas.

> **1. 独立 Q-learning / 独立 PPO。**Cada corpo inteligente aprende seu próprio Q ou estratégia, para que o outro seja considerado parte do ambiente.

**2. Centralized training, decentralized execution (CTDE).**O paradigma moderno mais comum.`π_i`que as condições da observação local `o_i` execução descentralizada padrão na implantação.`Q(s, a_1, …, a_n)`Condições relativas ao estado global completo e a acção conjunta.
- **MADDPG**(Lowe et al. 2017): DDPG com um crítico centralizado por agente.
- **COMA**(Foerster et al. 2017): base contrafactual  perguntar "qual seria a minha recompensa se eu tivesse tomado medidas `a'`"Em vez disso?"
- **MAPPO**- Não .**IPPO**com crítico compartilhado (Yu et al. 2022): PPO com função de valor centralizada. Dominant em 2026 para a MARL cooperativa.
- **QMIX**(Rashid et al. 2018): decomposição do valor  `Q_tot(s, a) = f(Q_1(s, a_1), …, Q_n(s, a_n))`com mistura monótona.

> **2. 集中训练，分布执行（CTDE）。**O sistema de inteligência tem suas próprias estratégias, dependendo apenas do local de observação.

**3. Self-play.**Duas cópias do mesmo agente jogam um ao outro. A política do adversário é a minha política de um snapshot passado. AlphaGo / AlphaZero / MuZero. OpenAI Five. Funciona melhor para jogos de soma zero; o sinal de treinamento é simétrico.

> **3. 自我博弈。**As duas cópias do mesmo corpo inteligente são para ── as estratégias do outro são para ── os mais adequados para o zero e para o jogo.

**4. League play.**Uma extensão do auto-jogo para ambientes de soma geral / adversária: manter uma população de políticas passadas e atuais, amostrar um adversário da liga, treinar contra eles. Adiciona exploradores (especializados em vencer o melhor atual) e exploradores principais (especializados em vencer exploradores). AlphaStar (StarCraft II). Necessário quando o jogo admite ciclos de estratégia "rock-paper-scissors".

> **4. 联盟训练。**O jogo permite que o "rolamento de pedra" da estratégia circule quando necessário.

**Communication.**Permita que os agentes enviem mensagens aprendidas .`m_i`Foerster et al. (2016) mostrou que a comunicação inter-agente diferenciável pode ser treinada de ponta a ponta. Os sistemas multi-agente baseados em LLM de hoje (Fase 16) comunicam essencialmente em linguagem natural.

> **通信。**允许智能体相互发送学习的消息――有效在合作环境中―― hoje em dia, o Mestrado em Ciências Magistrais em sistemas de inteligência múltiplos é essencialmente utilizado em comunicação em linguagem natural―

## Construí-lo e realizei-o.
```figure
f3-marl-orbit
```

## Construí-lo

Esta lição usa um GridWorld 6×6 com dois agentes cooperativos. Eles começam em cantos opostos e devem alcançar um objetivo compartilhado.`-1`por passo enquanto qualquer um dos agentes ainda está em movimento,`+10`Quando ambos chegarem.`code/main.py`- Não .

> Esta aula usa um GridWorld 6×6 e dois inteligentes colaboradores. Eles são partindo de um canto para outro, devem chegar ao objetivo compartilhado.

### Passo 1: o ambiente multi-agente

```python
class CoopGridWorld:
    def __init__(self):
        self.size = 6
        self.goal = (5, 5)

    def reset(self):
        return ((0, 0), (5, 0))  # two agents

    def step(self, state, actions):
        a1, a2 = state
        new1 = move(a1, actions[0])
        new2 = move(a2, actions[1])
        done = (new1 == self.goal) and (new2 == self.goal)
        reward = 10.0 if done else -1.0
        return (new1, new2), reward, done
```

O espaço de acção comum é`|A|² = 16`O estado global é de duas posições.

> * Unidos* movimento espaço é `|A|² = 16`O estado da totalidade é de duas posições.

### Passo 2: aprendizagem Q independente

Cada agente executa sua própria tabela Q teclada em estado conjunto. Em cada passo: ambos escolhem ações ε-compassivas, coletam transição conjunta, cada um atualiza seu próprio Q com a recompensa compartilhada.

```python
def independent_q(env, episodes, alpha, gamma, epsilon):
    Q1, Q2 = defaultdict(default_q), defaultdict(default_q)
    for _ in range(episodes):
        s = env.reset()
        while not done:
            a1 = epsilon_greedy(Q1, s, epsilon)
            a2 = epsilon_greedy(Q2, s, epsilon)
            s_next, r, done = env.step(s, (a1, a2))
            target1 = r + gamma * max(Q1[s_next].values())
            target2 = r + gamma * max(Q2[s_next].values())
            Q1[s][a1] += alpha * (target1 - Q1[s][a1])
            Q2[s][a2] += alpha * (target2 - Q2[s][a2])
            s = s_next
```

Funciona nessa tarefa porque as recompensas são densas e alinhadas.

> É válido nesta missão, porque a recompensa é intensa e completa.

### Passo 3: Q centralizado com atualização de valor decomposto

Use um Q em vez de acções conjuntas `Q(s, a_1, a_2)`Atualizar a partir de recompensa compartilhada. Descentralize na execução marginalizando: `π_i(s) = argmax_{a_i} max_{a_{-i}} Q(s, a_1, a_2)`. Troca espaço de acção comum exponencial para uma visão global *correcta* .

> Utilize um Q. sobre a unionização.

### Passo 4: simples jogo próprio (adversário 2 agente)

O mesmo agente, dois papéis.`K`O que é que é que é o que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é?

> Com um corpo inteligente, dois papéis.`K`回合后将 A's权重复到B──对称训练,持续进步──AlphaZero 配方的缩影──

## Encurralagens

- **Non-stationary replay.**Repetição de experiências com agentes independentes é pior do que um agente único porque antigas transições foram geradas por oponentes agora obsoletos.
  **非平稳回放。**A experiência de um corpo inteligente independente é pior do que a de um só corpo inteligente, pois a transferência antiga é gerada por oponentes do passado.
- **Credit assignment ambiguity.**Recompensa compartilhada após um longo episódio; não há forma clara de dizer qual agente contribuiu.
  **信用分配模糊。**长回合后的共享奖励; não se sabe qual dos seus contribuintes contribuiu com o que.
- **Policy drift / chasing.**A melhor resposta de cada agente muda com a atualização do outro.
  **策略漂移/追逐。**Cada corpo inteligente responde melhor à atualização e mudança de outros inteligentes.
- **Reward hacking via coordination.**Agentes encontram explorações coordenadas que o designer não antecipou. Agentes de leilão convergem para zero.
  **协调奖励黑客。**智能体发现设计者未预期的协调漏洞──修复:仔细的奖励设计、行为约束──
- **Exploration redundancy.**Os dois agentes exploram os mesmos pares de ações de estado.
  **探索冗余。** Dois seres inteligentes explorar o mesmo estado-moção para──Reprodução:  Recompensa ou condição de papel para cada seres inteligentes──
- **League cycles.**O auto-joco puro pode ficar preso num ciclo de dominação.
  **联盟循环。**O auto-conhecimento pode ser um processo de controle.
- **Sample explosion.** `n`Ações conjuntas: Ações de base de dados:
  **样本爆炸。**n 个智能体 × 状态空间 × 联合动作──用函数近似解决;因子化动作空间──

## Use-o com o framework implementado.

O mapa de aplicação MARL 2026:

> 2026 AN MARL  aplicato mapa:

| Domain | Method | Notes |
|--------|--------|-------|
| Domain / 领域 | Method / 方法 | Notes / 备注 |
| Cooperative navigation / manipulation / 合作导航/操作 | MAPPO / QMIX | CTDE; shared critic + decentralized actors. / CTDE；共享 Critic + 分布式 Actor。 |
| Two-player games (chess, Go, poker) / 双人游戏 | Self-play with MCTS (AlphaZero) | Zero-sum; symmetric training. / 零和；对称训练。 |
| Complex multiplayer (Dota, StarCraft) / 复杂多人游戏 | League play + imitation pretraining | OpenAI Five, AlphaStar. |
| Autonomous-vehicle fleets / 自动驾驶车队 | CTDE MAPPO / PPO with attention | Partial obs; variable team sizes. / 部分可观察；可变团队大小。 |
| Auction markets / 拍卖市场 | Game-theoretic equilibrium + RL | Mean-field RL when `n` → ∞. / n→∞ 时用平均场 RL。 |
| LLM multi-agent systems (Phase 16) / LLM 多智能体系统 | Natural-language comm + role conditioning | RL loop at the agent-planning layer. / Agent 规划层的 RL 循环。 |

Em 2026, a maior área de crescimento da MARL é a base de LLM: enxames de agentes de modelos de linguagem que negociam, debatem, construem software.

> O maior crescimento do MARL em 2026 é baseado no LLM: linguagem modelo inteligente grupo discussão, debate, construção de software.

## Envia-o . Produto .

Salva como`outputs/skill-marl-architect.md`- Não .

```markdown
---
name: marl-architect
description: Pick the right multi-agent RL regime (IPPO, CTDE, self-play, league) for a given task.
version: 1.0.0
phase: 9
lesson: 10
tags: [rl, multi-agent, marl, self-play]
---

Given a task with `n` agents, output:

1. Regime classification. Cooperative / adversarial / general-sum. Justify.
2. Algorithm. IPPO / MAPPO / QMIX / self-play / league. Reason tied to coupling tightness and reward structure.
3. Information access. Centralized training (what global info goes to the critic)? Decentralized execution?
4. Credit assignment. Counterfactual baseline, value decomposition, or reward shaping.
5. Exploration plan. Per-agent entropy, population-based training, or league.

Refuse independent Q-learning on tightly-coupled cooperative tasks. Refuse to recommend self-play for general-sum with cycle risks. Flag any MARL pipeline without a fixed-opponent eval (cherry-picked self-play numbers are common).
```

## Exercícios.

1. **Easy.**Treinar aprendizagem Q independente na cooperativa GridWorld. Quantos episódios até o retorno médio > 0?
2. **Medium.**Adicione uma tarefa de "coordenação": o objetivo é alcançado apenas quando ambos os agentes pisam sobre ele na mesma curva.
3. **Hard.**Implementar um critico centralizado para a formação no estilo MAPPO e comparar a velocidade de convergência com a PPO independente na tarefa de coordenação.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Markov game | "Multi-agent MDP" / 马尔可夫博弈 | `(S, A_1, …, A_n, P, R_1, …, R_n)`; each agent has its own reward. |
| CTDE | "Centralized training, decentralized execution" / 集中训练分布执行 | Joint critic at training time; each agent's policy uses only local obs. |
| IPPO | "Independent PPO" / 独立 PPO | Each agent runs PPO separately. Simple baseline; often underrated. |
| MAPPO | "Multi-agent PPO" / 多智能体 PPO | PPO with a centralized value function conditioned on global state. |
| QMIX | "Monotonic value decomposition" / 单调值分解 | `Q_tot = f_monotone(Q_1, …, Q_n)` allows decentralized argmax. |
| COMA | "Counterfactual multi-agent" / 反事实多智能体 | Advantage = my Q minus expected Q marginalizing over my action. |
| Self-play | "Agent vs past self" / 自我博弈 | Single agent, two roles; standard for zero-sum games. |
| League play | "Population training" / 联盟训练 | Cache past policies, sample opponents from the pool; handles strategy cycles. |

## Mais leitura 延伸阅读

- [Lowe et al. (2017). Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments (MADDPG)](https://arxiv.org/abs/1706.02275) CTDE com um crítico centralizado.
- [Foerster et al. (2017). Counterfactual Multi-Agent Policy Gradients (COMA)](https://arxiv.org/abs/1705.08926) Linhas de base contrafactuais para a atribuição de crédito.
- [Rashid et al. (2018). QMIX: Monotonic Value Function Factorisation](https://arxiv.org/abs/1803.11485) decomposição de valores com monotonia.
- [Yu et al. (2022). The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games (MAPPO)](https://arxiv.org/abs/2103.01955)O PPO é surpreendentemente forte para o MARL.
- [Vinyals et al. (2019). Grandmaster level in StarCraft II using multi-agent reinforcement learning (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z)- Liga de jogo em escala.
- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270) puro auto-jogo em jogos de soma zero.
- [Sutton & Barto (2018). Ch. 15 — Neuroscience & Ch. 17 — Frontiers](http://incompleteideas.net/book/RLbook2020.pdf) inclui o curto tratamento do manual das configurações de agentes múltiplos e o problema de não estacionalidade que o CTDE é concebido para resolver.
- [Zhang, Yang & Başar (2021). Multi-Agent Reinforcement Learning: A Selective Overview](https://arxiv.org/abs/1911.10635) Pesquisa que abrange a LMP cooperativa, competitiva e mista com resultados de convergência.
