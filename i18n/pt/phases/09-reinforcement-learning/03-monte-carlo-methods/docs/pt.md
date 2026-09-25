# Métodos de Monte Carlo  Aprender de Episódios Completos  Método de Monte Carlo  Aprender de um ciclo completo 

> A programação dinâmica precisa de um modelo. Monte Carlo precisa de episódios. Execute a política, observe os retornos, media-los. A ideia mais simples em RL  e a que desbloqueia tudo para baixo.

> **【中文解读】**O desenvolvimento de um ambiente de desenvolvimento é um processo de desenvolvimento de um ambiente de desenvolvimento de um ambiente de desenvolvimento.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划)
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

A programação dinâmica é elegante, mas assume que você pode fazer perguntas.`P(s' | s, a)`O sistema de preços não pode ser integrado em todas as reações dos clientes possíveis. Um LLM não pode enumerar todas as possíveis continuações após um token.

> O planejamento é muito bonito, mas suponha que possa consultar cada estado e movimento.`P(s' | s, a)`◊ na realidade quase nada é assim. ◊ máquinas não podem resolver a distribuição de imagens de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio de câmbio

É preciso um método que só precise da capacidade de "mostrar" do ambiente.`s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`- Usa-o para estimar valores.

> Você precisa de um método que só precise de um ambiente.`s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`Usá-lo para calcular o valor.

A mudança de DP para MC é filosóficamente importante: passamos de *modelo conhecido + backup exato* para *rollouts amostragados + retorno médio*. A variância salta, mas a aplicabilidade explode.

> A transição do DP para o MC é importante na filosofia: nós passamos de * modelo conhecido + reservas precisas * para * rotar * sample rollout + média de retornos *。 a diferença aumentou, mas a sua amplitude de aplicação aumentou explosivamente。 cada algoritmo RL TD、Q-learning、REINFORCE、PPO、GRPO são, em essência, um estimador de monotráfico, às vezes superpõe-se sobre ele próprio。

> **【中文解读】**De DP a MC a transformação central: de "modelo conhecido+ calculação precisa" a "template trajectory+ média de retornos"── a diferença aumentou, mas a amplitude de aplicação explodiu─PPO、RLHF são, em essência, variações do MC estimator─

> **【拓展：LLM中的MC】**No treinamento RLHF do ChatGPT, para cada pedido 采样多个答案、计算平均奖励 é a aplicação direta do MC 思想在大模型训练中──DeepSeek-R1 的GRPO também é baseado em um grupo de MC 估计──

## O conceito central.

![Monte Carlo: rollout, compute returns, average; first-visit vs every-visit](../assets/monte-carlo.svg)

**The core idea, in one line:** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`onde`G^{(i)}(s)`são observados os retornos após as visitas a `s`Política`π`- Não .

> **核心思想，一行概括：** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`, entre os `G^{(i)}(s)`É em estratégia.`π`下访问 `s`时观测到的回报──

> **【中文解读】**MC  avaliação do núcleo: estado = valor médio dos retornos observados durante o estado.`V_new = V_old + α(target - V_old)`É um ponto de partida do MC para o TD para todos os algoritmos modernos de RL.

**First-visit vs every-visit MC.**Dado um episódio que visita o estado`s`Multiplicas vezes, a primeira visita MC só conta o retorno da primeira visita; cada visita MC conta todas as visitas. Ambas são imparciais no limite. A primeira visita é mais fácil de analisar (mostras de ID).

> **首次访问 vs 每次访问 MC。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `s`O primeiro e o segundo período de visitas são:

**Incremental mean.**Em vez de armazenar todos os resultados, atualize a média de execução:

`V_n(s) = V_{n-1}(s) + (1/n) [G_n - V_{n-1}(s)]`

Reorganizar: `V_new = V_old + α · (target - V_old)`com`α = 1/n`- Troca .`1/n`para um passo-dimensional constante `α ∈ (0, 1)`e obtém um estimador de MC não estacionário que acompanha as mudanças em`π`Esse movimento é o salto completo de MC para TD para todos os algoritmos RL modernos.

> **增量均值。**Não armazenar todos os dados, mas actualizar o valor médio de execução.`1/n`替换为常数步长 `α ∈ (0, 1)`- Tenho um rastro.`π`                                                                                                                                                                                                                                                              

**Exploration is now a problem.**O DP tocou todos os estados por enumeração.`π`As regiões inteiras do espaço do estado nunca são amostragadas e as estimativas de valor permanecem em zero para sempre.

> **探索现在成了问题。**DP 通过枚举触及每个状态──MC 只有能看到策略访问的状态──如果`π`É certo que toda a região do espaço de estado nunca será tomada, seu valor estimado será sempre zero.

> **【中文解读】**探索问题:DP 能遍历所有状态,MC 只有能看到策略访问过的状态――如果策略是确定性的,大量状态永远不会被访问──三种解决方案:探索起点 (不实实) ̇ε-贪心 (最常用) ̇离策略MC ̇通过重要性采样从行为策略学习目标策略) ̇

1. **Exploring starts.**Comece cada episódio a partir de um par aleatório (s, a). Garante cobertura; irrealista na prática (você não pode "reset" um robô em um estado arbitrário).
   **探索起点。**Cada ciclo de um (s) arranque (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar (s) para começar) para começar (s) para começar) para começar (s) para começar) para começar (s) para começar) para começar (s) para começar) para começar (s) para começar) para começar (s) para começar) para começar)
2. **ε-greedy.**Ator ganancioso W.R.T. corrente Q, mas com probabilidade `ε`Todos os pares de estado-ação são amostragados assintoticamente.
   **ε-贪心。**Para os actuais Q 贪心行动, mas com probabilidade `ε`随机选动作── Todos os estados-motivos são gradualmente tomados──
3. **Off-policy MC.**Recolher dados sob uma política de comportamento `μ`, aprender sobre a política de alvo `π`É uma grande variância, mas é a ponte para métodos de repetição como o DQN.
   **离策略 MC。**Em estratégias de comportamento`μ`                                                                                                                                                                                                                                                              `π`高方差, mas é o caminho para DQN 等回放缓冲方法的桥梁

**Monte Carlo Control.**Avaliação → melhoria → avaliação, assim como a iteração da política, mas a avaliação é baseada em amostragem:

1. Corra .`π`- Não, não.
2. Atualização `Q(s, a)`de retornos observados.
3. Faça`π`É-avidito W.R.T.`Q`- Não .
4. Repito. - Não.

Converge para `Q*`E ...`π*`com probabilidade 1 em condições leves (cada par visitado com infinita frequência, `α`satisfaz Robbins-Monro).

> **蒙特卡洛控制。**评估 → 改进 → 评估,就像策略代,但评估基于采样――在温和条件下对被无限次访问,`α`满足 Robbins-Monro), em probabilidade 1 收到 `Q*`和 `π*`- Não.

## Construí-lo e realizei-o.
```figure
epsilon-greedy
```

## Construí-lo

### Passo 1: lançamento → lista de (s, a, r)

```python
def rollout(env, policy, max_steps=200):
    trajectory = []
    s = env.reset()
    for _ in range(max_steps):
        a = policy(s)
        s_next, r, done = env.step(s, a)
        trajectory.append((s, a, r))
        s = s_next
        if done:
            break
    return trajectory
```

Não há modelo, só `env.reset()`E ...`env.step(s, a)`A mesma interface que um ambiente de ginásio, mas despojado.

> Não precisa de modelo, só precisa.`env.reset()`和 `env.step(s, a)`                                                                                                                                                                                                                                                              

### Passo 2: Retorno de cálculo (varagem inversa)

```python
def returns_from(trajectory, gamma):
    returns = []
    G = 0.0
    for _, _, r in reversed(trajectory):
        G = r + gamma * G
        returns.append(G)
    return list(reversed(returns))
```

Um passe,`O(T)`A recorrência retrógrada .`G_t = r_{t+1} + γ G_{t+1}`Evita a somação.

> Uma vez,`O(T)` Reverso-transmissão`G_t = r_{t+1} + γ G_{t+1}`避免了重复求和──

### Passo 3: Avaliação do MC na primeira visita

```python
def mc_policy_evaluation(env, policy, episodes, gamma=0.99):
    V = defaultdict(float)
    counts = defaultdict(int)
    for _ in range(episodes):
        trajectory = rollout(env, policy)
        returns = returns_from(trajectory, gamma)
        seen = set()
        for t, ((s, _, _), G) in enumerate(zip(trajectory, returns)):
            if s in seen:
                continue
            seen.add(s)
            counts[s] += 1
            V[s] += (G - V[s]) / counts[s]
    return V
```

Três linhas fazem o trabalho: marcar o estado visto na primeira visita, contar os incrementos, atualizar a média de execução.

> 三行代码完成工作: marcar o estado da primeira visita, aumentar o número de contabilistas, actualizar o valor médio de operações.

### Passo 4: controlo do MC ganancioso (na política)

```python
def mc_control(env, episodes, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    counts = defaultdict(lambda: {a: 0 for a in ACTIONS})

    def policy(s):
        if random() < epsilon:
            return choice(ACTIONS)
        return max(Q[s], key=Q[s].get)

    for _ in range(episodes):
        trajectory = rollout(env, policy)
        returns = returns_from(trajectory, gamma)
        seen = set()
        for (s, a, _), G in zip(trajectory, returns):
            if (s, a) in seen:
                continue
            seen.add((s, a))
            counts[s][a] += 1
            Q[s][a] += (G - Q[s][a]) / counts[s][a]
    return Q, policy
```

### Passo 5: comparação com o padrão de ouro DP

A sua estimativa do MC de`V^π`Devem concordar com o resultado do DP da lição 02 como episódios → ∞. Na prática: 50.000 episódios em 4×4 GridWorld o leva dentro de `~0.1`da resposta DP.

> Tu é que estás ?`V^π`A avaliação de MC em número de reajustes → ∞ 时应与课02 DP 结果一致──实践中:4×4 GridWorld 上 50,000 回合将错误控制在 `~0.1`É dentro.

## Encurralagens

- **Infinite episodes.**MC requer episódios para acabar. Se a sua política pode circular para sempre, cap.`max_steps`GridWorld com uma política aleatória rotineiramente vezes fora  que é normal, só certifique-se de contar corretamente.
  **无限回合。**MC 要求回合*终止*──如果策略可能永远循环,设置 `max_steps`A limitação será vista como um fracasso oculto.
- **Variance.**MC usa retornos completos. Em longos episódios, a variação é enorme  uma recompensa infeliz no final dos turnos `V(s_0)`O método TD (Lessão 04) reduziu isto através do bootstrapping.
  **方差。**MC utiliza um total de reportagens.`V(s_0)`◊TD 方法(Lessão 04) através do auto-resgate para reduzir a diferença de dimensão.
- **State coverage.**O MC ganancioso num Q fresco com laços só vai tentar uma ação.
  **状态覆盖。**Novo Q 上的贪心 MC apenas vai tentar um movimento. Você tem que explorar.
- **Non-stationary policies.**Se`π`A taxa de variação de dados é de uma taxa de variação de dados, mas a taxa de variação de dados é de uma taxa de variação de dados.
  **非平稳策略。**Se `π`变化(如 MC 控制中),旧回报来自不同策略──常数 α MC 处理此问题;样本平均 MC 不能──
- **Off-policy importance sampling.**Os pesos .`π(a|s)/μ(a|s)`A variância explode com o horizonte. O limite com IS ponderado por decisão ou a transição para TD.
  **离策略重要性采样。**权重 `π(a|s)/μ(a|s)`Em seu caminho, a acumulação de fases multiplicadas.

## Use-o com o framework implementado.

O papel dos métodos Monte Carlo em 2026:

> 2026  Монт卡洛方法的角色:

| Use case | Why MC |
|----------|--------|
| Use case / 用例 | Why MC / 为什么用 MC |
| Short-horizon games (blackjack, poker) / 短视野游戏（二十一点、扑克） | Episodes terminate naturally; returns are clean. / 回合自然终止；回报干净。 |
| Offline evaluation of a logged policy / 离线评估已记录的策略 | Average discounted returns over stored trajectories. / 对存储轨迹取折扣回报平均。 |
| Monte Carlo Tree Search (AlphaZero) / 蒙特卡洛树搜索 | MC rollouts from tree leaves guide selection. / 树叶的 MC rollout 指导选择。 |
| LLM RL evaluation / LLM RL 评估 | Compute average reward over sampled completions for a given policy. / 对给定策略的采样完成计算平均奖励。 |
| Baseline estimation in PPO / PPO 中的基线估计 | The advantage target `A_t = G_t - V(s_t)` uses an MC `G_t`. / 优势目标使用 MC 的 `G_t`。 |
| Teaching RL / 教学 RL | Simplest algorithm that actually works — strip bootstrapping to see the core. / 最简单且有效的算法——去掉自举看核心。 |

Os algoritmos modernos de deep-RL (PPO, SAC) interpolam entre MC puro (retorno total) e TD puro (bootstrap de um passo) através de `n`Os dois pontos finais são exemplos do mesmo estimador.

> 现代深度 RL 算法 PPO、SAC) através `n`步回报或 GAE 在纯 MC (M) 完全回报) 和纯 TD (TD) 单步自举) 间插值── ambos os extremos são exemplos do mesmo estimador──

## Envia-o . Produto .

Salva como`outputs/skill-mc-evaluator.md`- Não .

```markdown
---
name: mc-evaluator
description: Evaluate a policy via Monte Carlo rollouts and produce a convergence report with DP-comparison if available.
version: 1.0.0
phase: 9
lesson: 3
tags: [rl, monte-carlo, evaluation]
---

Given an environment (episodic, with reset+step API) and a policy, output:

1. Method. First-visit vs every-visit MC. Reason.
2. Episode budget. Target number, variance diagnostic, expected standard error.
3. Exploration plan. ε schedule (if needed) or exploring starts.
4. Gold-standard comparison. DP-optimal V* if tabular; otherwise a bound from a Q-learning / PPO baseline.
5. Termination check. Max-step cap, timeouts, handling of non-terminating trajectories.

Refuse to run MC on non-episodic tasks without a finite horizon cap. Refuse to report V^π estimates from fewer than 100 episodes per state for tabular tasks. Flag any policy with zero-variance actions as an exploration risk.
```

## Exercícios.

1. **Easy.**Implementar a avaliação de MC de primeira visita da política uniforme-aleatória no 4×4 GridWorld.`V(0,0)`como função da contagem de episódios contra a resposta DP.
   > **练习1：**实现 MC 评估,将 V(0,0) 随回合数的收曲线与 DP 基准对比──
2. **Medium.**Implementar o controlo do MC com `ε ∈ {0.01, 0.1, 0.3}`Comparar o retorno médio após 20.000 episódios.
   > **练习2：**Us Diferente ε 值做 MC 控制, observar explorar-utilizar权衡──
3. **Hard.**Implementar *oft-policy* MC com amostragem de importância: recolher dados sob política uniforme aleatória `μ`, estimativa `V^π`para a política determinista ideal `π`Comparar simples IS vs. por decisão IS vs. ponderado IS. Qual tem menor variância?
   > **练习3：**实现离策略 MC 重要性采样), comparar diferentes IS 方差的差异──

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Monte Carlo | "Random sampling" / 蒙特卡洛 | Estimate expectations by averaging over iid samples from the distribution. |
| Return `G_t` | "Future reward" / 回报 | Sum of discounted rewards from step `t` to episode end: `Σ_{k≥0} γ^k r_{t+k+1}`. |
| First-visit MC | "Count each state once" / 首次访问 MC | Only the first visit in an episode contributes to the value estimate. |
| Every-visit MC | "Use all visits" / 每次访问 MC | Every visit contributes; slightly biased but more sample-efficient. |
| ε-greedy | "Exploration noise" / ε-贪心 | Pick greedy action with prob `1-ε`; random action with prob `ε`. |
| Importance sampling | "Correcting for sampling from the wrong distribution" / 重要性采样 | Reweight returns by `π(a\|s)/μ(a\|s)` products to estimate `V^π` from `μ` data. |
| On-policy | "Learn from my own data" / 在线策略 | Target policy = behavior policy. Vanilla MC, PPO, SARSA. |
| Off-policy | "Learn from someone else's data" / 离线策略 | Target policy ≠ behavior policy. Importance-sampled MC, Q-learning, DQN. |

## Mais leitura 延伸阅读

- [Sutton & Barto (2018). Ch. 5 — Monte Carlo Methods](http://incompleteideas.net/book/RLbook2020.pdf) o tratamento canónico.
- [Singh & Sutton (1996). Reinforcement Learning with Replacing Eligibility Traces](https://link.springer.com/article/10.1007/BF00114726) Análise de primeira visita versus cada visita.
- [Precup, Sutton, Singh (2000). Eligibility Traces for Off-Policy Policy Evaluation](http://incompleteideas.net/papers/PSS-00.pdf) MC e controlo de variações fora da política.
- [Mahmood et al. (2014). Weighted Importance Sampling for Off-Policy Learning](https://arxiv.org/abs/1404.6362) estimadores modernos de IS de baixa variação.
- [Tesauro (1995). TD-Gammon, A Self-Teaching Backgammon Program](https://dl.acm.org/doi/10.1145/203330.203343) a primeira demonstração empírica em larga escala de auto-jogo MC/TD convergindo para o jogo sobre-humano; precursor conceitual de cada lição na segunda metade desta fase.
