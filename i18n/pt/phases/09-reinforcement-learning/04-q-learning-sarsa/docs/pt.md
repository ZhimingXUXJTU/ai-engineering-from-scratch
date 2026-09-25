# Diferença temporal  Q-Learning & SARSA  时序差分  Q学习 vs SARSA

> Monte Carlo espera até o final do episódio. TD atualiza após cada passo, iniciando a próxima estimativa de valor. Q-learning é fora de política e otimista; SARSA é política e cauteloso. Ambos são uma linha de código. Ambos sustentam cada método de RL profundo nesta fase.

> **【中文解读】**MC tem que esperar até o ciclo terminar para atualizar, TD`r + γ V(s')`Como objetivo para orientar a avaliação actual. O aprendizado Q é o melhor aprendizado estratégico, o SARSA é o melhor aprendizado estratégico online.`max`Mas é a base de toda a RL profunda.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming), Phase 9 · 03 (Monte Carlo) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划), Phase 9 · 03 (蒙特卡洛)
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

Monte Carlo funciona, mas tem duas exigências caras. Ele precisa de episódios que terminem, e ele só atualiza depois que o retorno final está dentro. Se o seu episódio é de 1.000 passos, MC espera 1.000 passos para atualizar qualquer coisa. É de alta variância, baixa viés, e lento na prática.

> O Monte Carlo é válido, mas tem dois requisitos caros. Ele precisa de encerrar o ciclo, e só é atualizado após o final de retornos. Se o ciclo tiver 1.000 passos, MC deve esperar 1.000 passos para atualizar qualquer coisa.

A programação dinâmica tem o perfil oposto  backup bootstrapped de variância zero  mas requer um modelo conhecido.

> O desenvolvimento de um sistema de gestão de dados e de dados é um processo de desenvolvimento de dados e de dados.

A diferença temporal (TD) divide a diferença.`(s, a, r, s')`, formam um alvo de um passo .`r + γ V(s')`e empurrar .`V(s)`Não há modelo, não há episódios completos, há preconceitos em usar uma aproximação.`V`A variância é muito menor do que a MC e as atualizações online a partir do primeiro passo.

> 时序差分(TD) aprendizagem entre os dois.`(s, a, r, s')`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `r + γ V(s')`,将 `V(s)`Não precisa de um modelo. Não precisa de um ciclo completo.`V`Há uma diferença, mas a diferença é muito menor que a MC, e pode ser atualizada desde o primeiro passo.

Este é o pivô em que todas as modernas RL  DQN, A2C, PPO, SAC  gira. O resto da Fase 9 são camadas de aproximação de funções e truques construídos em cima da atualização TD de um passo que você vai escrever nesta lição.

> É o resto da fase 9 que você vai escrever neste curso é sobre a aproximação e a técnica do nível de função construída sobre a actualização.

> **【中文解读】**TD aprendizagem é DP e MC: usando um único passo de transferência `(s,a,r,s')`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `r + γV(s')`Não é necessário um modelo, nem um ciclo completo. Há uma variação (porque é usado um V similar), mas a variação é muito inferior ao MC, e pode ser atualizado online.

> **【拓展：游戏AI→LLM对齐】**Q-learning é o núcleo do Atari DQN de 2013, iniciou a profunda RL 时代。PPO é o algoritmo central do treinamento ChatGPT RLHF  ambos baseados em TD 误差的思想──compreender Q-learning 和 SARSA é a base do grande modelo para o treinamento齐──

## O conceito central.

![Q-learning vs SARSA: off-policy max vs on-policy Q(s', a')](../assets/td.svg)

**The TD(0) update for V:**

`V(s) ← V(s) + α [r + γ V(s') - V(s)]`

A quantidade em brackets é o erro TD `δ = r + γ V(s') - V(s)`É o analogo online de `G_t - V(s_t)`Em MC. A convergência exige `α`A satisfação de Robbins-Monro (`Σ α = ∞`- Não .`Σ α² < ∞`O Governo da República, em especial, foi o primeiro a visitar os Estados-Membros.

> **V 的 TD(0) 更新：**括号中量是 TD 误差 `δ = r + γ V(s') - V(s)`É o MC Central.`G_t - V(s_t)`O que é que é o que é preciso para isso?`α`满足 Robbins-Monro 条件且所有状态被无限次访问──

**Q-learning.**Um método de controlo TD fora da política:

`Q(s, a) ← Q(s, a) + α [r + γ max_{a'} Q(s', a') - Q(s, a)]`

O `max`Assume que a política *comprometida* será seguida a partir de`s'`O desacoplamento faz com que o aprendizado Q aprenda.`Q*`Mnih et al. (2015) converteram isso em aprendizado Q profundo na Atari (Lesson 05).

> **Q-learning。**Uma estratégia de controle TD`max`假设从 `s'`開始將遵循*貪心*策略, independentemente do que o corpo inteligente realmente tome.`Q*`❖Mnih 等人 (2015) vai transformar isto em Atari 上的深度 Q-learning (Lessão 05) ❖

**SARSA.**Um método de TD sobre a política:

`Q(s, a) ← Q(s, a) + α [r + γ Q(s', a') - Q(s, a)]`

O nome é o tuple .`(s, a, r, s', a')`A SARSA utiliza a acção .`a'`O agente é o que vai seguir, não o ganancioso.`argmax`Converge para`Q^π`Para o que quer que seja avaro .`π`Está a correr, que no limite `ε → 0`torna-se`Q*`- Não .

> **SARSA。**Uma estratégia on-line TD 方法──名称是元组 `(s, a, r, s', a')`◊ SARSA 使用智能体*实际*采取的下一个动作 `a'`Não é ganância .`argmax`◊ Recebendo até agora`π`de `Q^π`, em `ε → 0`De limite para baixo.`Q*`- Não.

**The cliff-walking difference.**Na tarefa clássica de caminhada em penhasco (caída-desde-penhasco = recompensa -100), a aprendizagem Q aprende o caminho ideal ao longo da borda do penhasco, mas ocasionalmente assume a penalidade durante a exploração. A SARSA aprende um caminho mais seguro a um passo da falésia porque faz com que o ruído da exploração seja incluído em seu valor Q. Com o treinamento, ambos atingem o ponto ideal.`ε → 0`Na prática, importa: quando a exploração está realmente a acontecer na implantação, o comportamento da SARSA é mais conservador.

> **【中文解读】**A experiência clássica de caminhada no escalão revela a diferença fundamental entre Q-learning e SARSA: Q-learning aprender a seguir o melhor caminho para um escalão, mas explorar quando cai), SARSA aprender a percorrer um caminho seguro para um escalão distante, pois considera o ruído explorado.

**Expected SARSA.**Substitui`Q(s', a')`com o seu valor esperado inferior a `π`- Não .

`Q(s, a) ← Q(s, a) + α [r + γ Σ_{a'} π(a'|s') Q(s', a') - Q(s, a)]`

Variância menor do que a SARSA (não há amostra de `a'`O objetivo é o mesmo em matéria de política, muitas vezes o padrão dos livros didáticos modernos.

> **期望 SARSA。**- Não .`π`O valor de espera substitui`Q(s', a')`◊ Em comparação com a SARSA 方差更低`a'`), o mesmo em linha estratégico objetivo.

**n-step TD and TD(λ).**Interpolar entre TD(0) e MC, esperando `n`Passo antes de arrancar. `n=1`é TD, `n=∞`é MC. TD(λ) médias sobre todos `n`com pesos geométricos `(1-λ)λ^{n-1}`A maioria dos usos de RL profundo`n`Entre 3 e 20.

> **n 步 TD 和 TD(λ)。**Em TD(0) e MC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `n`步再自举──`n=1`É TD,`n=∞`É MC―TD (L) Us几何权重对所有 `n`取平均── maioria profundidade RL `n`Entre 3 e 20 anos.

> **【拓展：TD 误差在 LLM RLHF 中的对应】**TD 误差 δ = r + γV(s') - V(s) na formação RLHF do LLM                                                                                                                                                                                                                                                  

## Construí-lo e realizei-o.
```figure
qlearning-gridworld
```

## Construí-lo

### Passo 1: SARSA sobre a política de avareza

```python
def sarsa(env, episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})

    def choose(s):
        if random() < epsilon:
            return choice(ACTIONS)
        return max(Q[s], key=Q[s].get)

    for _ in range(episodes):
        s = env.reset()
        a = choose(s)
        while True:
            s_next, r, done = env.step(s, a)
            a_next = choose(s_next) if not done else None
            target = r + (gamma * Q[s_next][a_next] if not done else 0.0)
            Q[s][a] += alpha * (target - Q[s][a])
            if done:
                break
            s, a = s_next, a_next
    return Q
```

A única diferença com a aprendizagem Q é a linha-alvo.

> O único que distingue o aprendizado de Q é o objetivo de aprendizagem.

### Passo 2: Aprendizagem Q

```python
def q_learning(env, episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    for _ in range(episodes):
        s = env.reset()
        while True:
            a = choose(s, Q, epsilon)
            s_next, r, done = env.step(s, a)
            target = r + (gamma * max(Q[s_next].values()) if not done else 0.0)
            Q[s][a] += alpha * (target - Q[s][a])
            if done:
                break
            s = s_next
    return Q
```

O `max`O símbolo é a diferença entre dentro da política e fora da política.

> `max`O símbolo é a diferença entre estratégias online e estratégias offline.

### Passo 3: Curvas de aprendizagem

A média de retorno de pista por 100 episódios. Q-learning converge mais rápido no GridWorld determinista simples; SARSA é mais conservador no caminhão em penhasco.`code/main.py`, ambos são quase ótimos depois de cerca de 2.000 episódios com`α=0.1, ε=0.1`- Não .

> Seguir cada 100 volumes de retorno médio. Q-learning em simples determinação GridWorld 上收快; SARSA em cliff walk walk 上保守.`code/main.py`O 4x4 GridWorld é um dos principais.`α=0.1, ε=0.1`Cerca de 2.000 volumes, quase o melhor.

### Passo 4: comparação com a verdade DP

Iteração de valor de execução (Lessão 02) para obter `Q*`- Cheque .`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`Um agente TD tabuleiro saudável atinge o interior .`~0.5`no 4x4 GridWorld depois de 10.000 episódios.

> 运行值代(Lessão 02) 获得`Q*` Inspecção`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`◊ Um quadro saudável TD 智能体在 10,000 回合后在 4×4 GridWorld 上误差在 `~0.5`É dentro.

## Encurralagens

- **Initial Q values matter.**Optimismo inicial (`Q = 0`A política de ganância pode ser atrapada para sempre.
  **初始 Q 值很重要。**乐观初始化 负奖励任务中                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  `Q = 0`O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é?
- **α schedule.**Constantemente .`α`É bom para problemas não estacionários.`α_n = 1/n`dá convergência em teoria mas é muito lento na prática  pin `α`em `[0.05, 0.3]`e monitorar a curva de aprendizagem.
  **α 调度。**常数 `α`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `α_n = 1/n`                                                                                                                                                                                                                                                              `α`Fixa-se`[0.05, 0.3]`Não monitorizar a aprendizagem.
- **ε schedule.**Começar alto (`ε=1.0`), decadência a `ε=0.05`. "GLIE" (avididade no limite com exploração infinita) é a condição de convergência.
  **ε 调度。**Desde o alto da sua posição`ε=1.0`), decadência`ε=0.05` "GLIE"极极贪心且无限探索) 是收条件
- **Max bias in Q-learning.**O `max`O operador é tendencioso para cima quando `Q`O método de aprendizagem dupla de Hasselt (usado pelo DDQN na lição 05) corrige isto com duas tabelas de Q.
  **Q-learning 的最大化偏差。** `max`- Não .`Q`Há ruído quando há uma grande variação.
- **Non-terminating episodes.**TD pode aprender sem terminais, mas você precisa de captar os passos ou lidar com a banda de arranque corretamente na banda. padrão: tratar a banda como não terminal, continuar a arrancar.
  **非终止回合。**O TD pode ser aprendido em um estado infinito, mas precisa de definir um número de passos acima do limite ou de um processo de auto-processamento de um limite.
- **State hashing.**Se os estados forem tuples/tensores, use uma chave hashável (tuple, não lista; tuple de flotas arredondadas, não cruas).
  **状态哈希。**Se o estado é um grupo de unidades/quantidade de unidades, use o valor original do grupo de unidades (ou um grupo de unidades) e não o valor inicial do grupo de unidades.

## Use-o com o framework implementado.

O panorama da TD de 2026:

> Edição de 2026 ano TD 学习:

| Task | Method | Reason |
|------|--------|--------|
| Task / 任务 | Method / 方法 | Reason / 原因 |
| Small tabular environments / 小型表格环境 | Q-learning | Learns optimal policy directly. / 直接学习最优策略。 |
| On-policy safety-critical / 在线策略安全关键 | SARSA / Expected SARSA | Conservative during exploration. / 探索期间保守。 |
| High-dimensional state / 高维状态 | DQN (Phase 9 · 05) | Neural-net Q-function with replay and target net. / 神经网络 Q 函数+回放+目标网络。 |
| Continuous actions / 连续动作 | SAC / TD3 (Phase 9 · 07) | TD update on a Q-network; policy net emits actions. / Q 网络上的 TD 更新；策略网络输出动作。 |
| LLM RL (reward-model-based) / LLM RL（基于奖励模型） | PPO / GRPO (Phase 9 · 08, 12) | Actor-critic with TD-style advantage via GAE. / Actor-Critic + GAE 的 TD 式优势。 |
| Offline RL / 离线 RL | CQL / IQL (Phase 9 · 08) | Q-learning with conservative regularization. / 带保守正则化的 Q-learning。 |

90% do "RL" que você lê sobre em 2026 artigos é alguma elaboração de Q-learning ou SARSA. Entender a atualização tabuleira em seus dedos antes de ler mais fundo.

> No artigo 2026 ano, você leu "RL", 90% é uma variante de Q-learning ou SARSA. Antes de ler em profundidade, primeiro, actualize o padrão de aprendizagem para a memória muscular.

## Envia-o . Produto .

Salva como`outputs/skill-td-agent.md`- Não .

```markdown
---
name: td-agent
description: Pick between Q-learning, SARSA, Expected SARSA for a tabular or small-feature RL task.
version: 1.0.0
phase: 9
lesson: 4
tags: [rl, td-learning, q-learning, sarsa]
---

Given a tabular or small-feature environment, output:

1. Algorithm. Q-learning / SARSA / Expected SARSA / n-step variant. One-sentence reason tied to on-policy vs off-policy and variance.
2. Hyperparameters. α, γ, ε, decay schedule.
3. Initialization. Q_0 value (optimistic vs zero) and justification.
4. Convergence diagnostic. Target learning curve, `|Q - Q*|` check if DP is possible.
5. Deployment caveat. How will exploration behave at inference? Is SARSA's conservatism needed?

Refuse to apply tabular TD to state spaces > 10⁶. Refuse to ship a Q-learning agent without a max-bias caveat. Flag any agent trained with ε held at 1.0 throughout (no exploitation phase).
```

## Exercícios.

1. **Easy.**Implementar Q-learning e SARSA no GridWorld 4×4. Planejar curvas de aprendizagem (retorno médio por 100 episódios) para 2.000 episódios. Quem converge mais rápido?
   > **练习1：**Em GridWorld, a curva de aprendizagem de Q-learning e SARSA é comparada.
2. **Medium.**Construa um ambiente de caminhada em penhasco (4×12, a última linha é o penhasco com recompensa -100 e reinicie para começar). Compare as políticas finais de Q-learning e SARSA.
   > **练习2：** realçar o ambiente, observar as diferenças de estratégia de Q-learning (CCL) vs SARSA (CCL)
3. **Hard.**Implementar o duplo aprendizado Q. Em um GridWorld com recompensas ruidosas (ruído gaussiano σ=5 adicionado à recompensa por passo), mostrar sobreestimações de aprendizado Q `V*(0,0)`A aprendizagem dupla de Q não faz isso.
   > **练习3：**实现双重Q-learning,验证它能消除最大化偏差在Q-learning中.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| TD error | "The update signal" / TD 误差 | `δ = r + γ V(s') - V(s)`, the bootstrapped residual. |
| TD(0) | "One-step TD" / 单步 TD | Update after every transition using only the next state's estimate. |
| Q-learning | "Off-policy RL 101" / Q 学习 | TD update with `max` over next-state actions; learns `Q*` regardless of behavior policy. |
| SARSA | "On-policy Q-learning" / SARSA | TD update using the actual next action; learns `Q^π` for current ε-greedy π. |
| Expected SARSA | "The low-variance SARSA" / 期望 SARSA | Replace sampled `a'` with its expectation under π. |
| GLIE | "Correct exploration schedule" / 无限探索极限贪心 | Greedy in the Limit with Infinite Exploration; needed for Q-learning convergence. |
| Bootstrapping | "Using current estimate in the target" / 自举 | What distinguishes TD from MC. Source of bias but massive variance reduction. |
| Maximization bias | "Q-learning overestimates" / 最大化偏差 | `max` over noisy estimates is upward-biased; fixed by Double Q-learning. |

## Mais leitura 延伸阅读

- [Watkins & Dayan (1992). Q-learning](https://link.springer.com/article/10.1007/BF00992698) o papel original e a prova de convergência.
- [Sutton & Barto (2018). Ch. 6 — Temporal-Difference Learning](http://incompleteideas.net/book/RLbook2020.pdf) TD(0), SARSA, Q-learning, Esperado SARSA.
- [Hasselt (2010). Double Q-learning](https://papers.nips.cc/paper_files/paper/2010/hash/091d584fced301b442654dd8c23b3fc9-Abstract.html) fixação do preconceito de maximização.
- [Seijen, Hasselt, Whiteson, Wiering (2009). A Theoretical and Empirical Analysis of Expected SARSA](https://ieeexplore.ieee.org/document/4927542) motivação esperada para a SARSA.
- [Rummery & Niranjan (1994). On-line Q-learning using connectionist systems](https://www.researchgate.net/publication/2500611_On-Line_Q-Learning_Using_Connectionist_Systems) o artigo que contou o SARSA (então chamado de "Q-learning de conexão modificada").
- [Sutton & Barto (2018). Ch. 7 — n-step Bootstrapping](http://incompleteideas.net/book/RLbook2020.pdf) generaliza TD(0) para TD(n), o caminho da aprendizagem Q para os traços de elegibilidade e, mais tarde, GAE em PPO.
