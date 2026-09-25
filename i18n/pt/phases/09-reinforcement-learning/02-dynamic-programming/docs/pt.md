# Programação Dinâmica Iteração de Política e Iteração de Valor                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

> A programação dinâmica é RL com a fraude. Você já sabe as funções de transição e recompensa; você apenas itera a equação Bellman até que`V`ou `π`O método de referência é o que todos os métodos baseados em amostragem tentam abordar.

> **【中文解读】**动态规划是强化学习的"作弊版"你已知环境的转移概率和奖励函数,只需反复代 Bellman 方程直到收──它是所有采样方法的"金标准" (Q-learning、PPO, etc.) referir-se:

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs) | **前置知识:** Phase 9 · 01 (MDP)
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

Você tem um MDP com um modelo conhecido: você pode consultar `P(s' | s, a)`E ...`R(s, a, s')`Um gerente de estoque conhece a distribuição da demanda. um jogo de tabuleiro tem transições deterministas. um mundo de grade é quatro linhas de Python. você tem um *modelo*.

> Você tem um modelo conhecido MDP: você pode consultar qualquer estado-moção para o `P(s' | s, a)`和 `R(s, a, s')` O gerente de estoque sabe a necessidade de distribuição‬  O jogo de tela tem transferência certa‬  O GridWorld é uma linha Python‬  Você tem um modelo ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬

O RL livre de modelos (Q-learning, PPO, REINFORCE) foi inventado para o caso em que você não tem um modelo  você só pode sampler do ambiente. Mas quando você tem um, há métodos mais rápidos e melhores: programação dinâmica. Bellman os projetou em 1957. Eles ainda definem a corretão: quando as pessoas dizem "política ideal para este MDP", eles querem dizer que a política DP retornaria.

> 无模型 RL(Q-learning、PPO、REINFORCE) é uma situação desenvolvida por não ter modelos. Você só pode tomar de um ambiente. Mas quando você tem modelos, há métodos mais rápidos e melhores:

> **【中文解读】**Quando você conhece o modelo ambiental ([[transferência probabilidade e função de recompensa]]), o planejamento de atividades pode ser preciso para obter a melhor estratégia.

> **【拓展：AlphaZero/MCTS】**A busca de Monte Carlo em AlphaZero (MCTS) é, em essência, uma versão diferente da reserva de Bellman.

Os dados são necessários para 2026 por três razões: primeiro, cada ambiente tabular na pesquisa RL (GridWorld, FrozenLake, CliffWalking) é resolvido com DP para produzir a política padrão de ouro.`V*(s_0)`Terceiro, os modernos métodos de RL offline e planejamento (MCTS, pesquisa do AlphaZero, RL baseado em modelo na Fase 9 · 10) todos iteram um backup Bellman sobre um modelo aprendido ou dado.

> Você precisa deles em 2026 , por que há três. Primeiro, o RL em cada um dos estudos (GridWorld, FrozenLake, CliffWalking) usa DP para obter soluções para produzir estratégias de padrão de ouro.`V*(s_0)`A avaliação com a DP 答案差 30%, seu Q-learning já tem um bug.

## O conceito central.

![Policy iteration and value iteration, side by side](../assets/dp.svg)

**Two algorithms, both fixed-point iteration on Bellman.**

> **两种算法，都是对 Bellman 方程做不动点迭代。**

> **【中文解读】**两种算法都是对贝尔曼方程做不动点代――策略代:交替执行"策略评估"和"策略改进"直到策略不变;值代:将两者合并为一步,直接取 max――两者最终收到同一最佳值函数 V*──

**Policy iteration.**Alterna duas etapas até que a política pare de mudar.

> **策略迭代。**交替执行两个步骤直到策略不再改变──

1. *Evaluation:* dada política `π`, computação `V^π`através da aplicação repetida `V(s) ← Σ_a π(a|s) Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`Até que converja.
   * avaliar:* 给定策略 `π`, Repeat Apply Bellman 方程直到 `V^π`- Não.
2. * Melhoria:* dada `V^π`, fazer`π`ganancioso W.R.T.`V^π`- Não .`π(s) ← argmax_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`- Não .
   *改进:* 给定 `V^π`,让 `π`Para o`V^π`- Não.

A convergência é garantida porque (a) cada etapa de melhoria mantém `π`Aumento do número de pessoas em situação de risco`V^π`Para alguns estados, (b) o espaço das políticas deterministas é finito. geralmente converge em ~ 520 iterações externas mesmo para grandes espaços de estado.

> A receita é garantida, pois a) Cada vez que se aprimora ou se mantém`π`Não mudam, ou aumentam drasticamente um estado.`V^π`,(b) O espaço de estratégia de determinação é limitado.

**Value iteration.**Colapsa a avaliação e melhoria em uma única varredura. Aplique a equação Bellman *optimalidade*:

`V(s) ← max_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`

Repita até `max_s |V_{new}(s) - V(s)| < ε`. Extrair a política no final tomando a ação gananciosa. Estritamente mais rápido por iteração  nenhum loop de avaliação interna  mas normalmente precisa de mais iterações para convergir.

> **值迭代。**A avaliação e melhoria serão combinadas para uma análise única. Aplicação de Bellman *o melhor método *o melhor método.

**Generalized policy iteration (GPI).**A estrutura unificadora. Função de valor e política estão bloqueadas em um loop de melhoria bidirecional; qualquer método que conduza ambos para a consistência mútua (iteração de valor assíncrona, iteração de política modificada, Q-learning, ator-crítica, PPO) é uma instância de GPI.

> **【拓展：GPI→PPO/RLHF】**广义策略代 (GPI) 是统一框架:Q-learning、Actor-Critic、PPO Bessessess are examples of GPI── Comprendiu o GPI do DP, você já entendeu o ChatGPT 背后 RLHF 训练循环的设计哲学──

**Why `γ < 1` matters.**O operador Bellman é um`γ`- contracção na norma-sup: `||T V - T V'||_∞ ≤ γ ||V - V'||_∞`A contração implica um ponto fixo único e uma convergência geométrica.`γ < 1`E se perder a garantia, precisa de um horizonte finito ou um estado terminal de absorção.

> **为什么 `γ < 1` 很重要。**Bellman está a fazer o seu trabalho .`γ`- compressão de mapas. compressão significa único inmobiliário e geometria.`γ < 1`Perdeu a garantia de que precisava de um visual limitado ou de um estado de absorção terminado.

## Construí-lo e realizei-o.
```figure
value-iteration-gamma
```

## Construí-lo

### Passo 1: construir o modelo GridWorld MDP

Usar o mesmo 4x4 GridWorld da lição 01. Adicionamos uma variante estocástica: com probabilidade `0.1`O agente desliza numa direcção perpendicular aleatória.

> Utilize Lesson 01 In the Same 4×4 GridWorld... nós adicionamos um variante: em probabilidade`0.1`智能体会滑向随机垂直方向──

```python
SLIP = 0.1

def transitions(state, action):
    if state == TERMINAL:
        return [(state, 0.0, 1.0)]
    outcomes = []
    for direction, prob in action_probs(action):
        outcomes.append((apply_move(state, direction), -1.0, prob))
    return outcomes
```

`transitions(s, a)`Retorna uma lista de `(s', r, p)`Este é o modelo inteiro.

> `transitions(s, a)` Retorno `(s', r, p)`É o que se passa.

### Passo 2: Avaliação das políticas

Dado uma política `π(s) = {action: prob}`, iterar a equação de Bellman até `V`Parou de se mover:

> 给定策略 `π(s) = {action: prob}`, 代 Bellman 方程直到 `V`Não se alteram:

```python
def policy_evaluation(policy, gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in states()}
    while True:
        delta = 0.0
        for s in states():
            v = sum(pi_a * sum(p * (r + gamma * V[s_prime])
                              for s_prime, r, p in transitions(s, a))
                   for a, pi_a in policy(s).items())
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            return V
```

### Passo 3: Melhoria das políticas

Substitui`π`Com a política gananciosa W.R.T.`V`Se ...`π`Não mudou, retorno  estamos no óptimo.

> - Não .`π`替换为对 `V`贪心的策略──如果 `π`Não há mudança, voltamos já ao melhor.

```python
def policy_improvement(V, gamma=0.99):
    new_policy = {}
    for s in states():
        best_a = max(
            ACTIONS,
            key=lambda a: sum(p * (r + gamma * V[s_prime])
                              for s_prime, r, p in transitions(s, a)),
        )
        new_policy[s] = best_a
    return new_policy
```

### Passo 4: Conectar-os

```python
def policy_iteration(gamma=0.99):
    policy = {s: "up" for s in states()}   # arbitrary start
    for _ in range(100):
        V = policy_evaluation(lambda s: {policy[s]: 1.0}, gamma)
        new_policy = policy_improvement(V, gamma)
        if new_policy == policy:
            return V, policy
        policy = new_policy
```

Convergência típica em 4×4: 46 iterações externas.`V*(0,0) ≈ -6`E uma política que reduz rigorosamente a contagem de passos.

> 4×4 上的典型收:4-6 次外层代──输出 `V*(0,0) ≈ -6`E uma estratégia de redução rigorosa de número de passos.

### Passo 5: Iteração de valor (versão de um ciclo)

```python
def value_iteration(gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in states()}
    while True:
        delta = 0.0
        for s in states():
            v = max(sum(p * (r + gamma * V[s_prime])
                       for s_prime, r, p in transitions(s, a))
                   for a in ACTIONS)
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            break
    policy = policy_improvement(V, gamma)
    return V, policy
```

O mesmo ponto fixo, menos linhas de código.

> O mesmo incêndio, menor número de código-fonte.

## Encurralagens

- **Forgetting to handle terminals.**Se aplicarmos o Bellman a um estado de absorção, ele ainda capta uma "melhor ação" que não muda nada.`if s == terminal: V[s] = 0`- Não .
  **忘记处理终止状态。**Se o estado de absorção for aplicado, Bellman, ele ainda escolherá um "melhor movimento", mas nada mudará.`if s == terminal: V[s] = 0`Proteção
- **Sup-norm vs L2 convergence.**Utilização`max |V_new - V|`A garantia teórica está na sup-norma.
  **Sup 范数 vs L2 收敛。**Utilização `max |V_new - V|`, e não o valor médio.
- **In-place vs synchronous updates.**Atualização`V[s]`O sistema de concentração de gases em local (Gauss-Seidel) converge mais rapidamente do que um sistema de concentração separado.`V_new`O código de produção usa o local.
  **原地更新 vs 同步更新。**Originally actualizada `V[s]`(Gauss-Seidel) Comparado com o único.`V_new`字典(Jacobi)收更快──生产代码使用原地更新──
- **Policy ties.**Se duas ações tiverem o mesmo valor Q,`argmax`A primeira ação em ordem fixa é a de uma relação de separação estável.
  **策略平局。**Se dois movimentos tiverem um valor Q,`argmax`Cada vez que se pode romper a linha de jogo de forma diferente, resulta em "stratégies estabilizadas" de verificação.
- **State-space explosion.**DP é`O(|S| · |A|)`Para a análise, a função é estimada em cerca de 107.
  **状态空间爆炸。**DP , cada uma das análises é`O(|S| · |A|)`△ é adequado para cerca de 107 estados.

## Use-o com o framework implementado.

Em 2026, o DP é a linha de base de correcção e o ciclo interno dos planejadores:

> O programa de desenvolvimento de um sistema de desenvolvimento de sistemas de gestão de recursos humanos (PDP) é um ciclo interno de base e planeador de sistemas de gestão de recursos humanos.

| Use case | Method |
|----------|--------|
| Use case / 用例 | Method / 方法 |
| Solve a small tabular MDP exactly / 精确求解小型表格 MDP | Value iteration (simpler) or policy iteration (fewer outer steps) / 值迭代（更简单）或策略迭代（更少外层步数） |
| Verify a Q-learning / PPO implementation / 验证 Q-learning/PPO 实现 | Compare to DP-optimal V* on a toy environment / 在玩具环境上与 DP 最优 V* 比较 |
| Model-based RL (Phase 9 · 10) / 基于模型的 RL | Bellman backup on a learned transition model / 在学习的转移模型上做 Bellman 备份 |
| Planning in AlphaZero / MuZero / AlphaZero/MuZero 中的规划 | Monte Carlo Tree Search = async Bellman backup / MCTS = 异步 Bellman 备份 |
| Offline RL (CQL, IQL) / 离线 RL | Conservative Q-iteration — DP with a penalty on OOD actions / 保守 Q 迭代——对 OOD 动作加惩罚的 DP |

Sempre que alguém diz "a função de valor ideal", eles querem dizer "o ponto fixo DP".`V*`ou `Q*`num jornal, imaginem este ciclo.

> Cada vez que alguém diz "função de valor máximo", eles se referem a "DP não move"`V*`Ou `Q*`Imagina este ciclo.

## Envia-o . Produto .

Salva como`outputs/skill-dp-solver.md`- Não .

```markdown
---
name: dp-solver
description: Solve a small tabular MDP exactly via policy iteration or value iteration. Report convergence behavior.
version: 1.0.0
phase: 9
lesson: 2
tags: [rl, dynamic-programming, bellman]
---

Given an MDP with a known model, output:

1. Choice. Policy iteration vs value iteration. Reason tied to |S|, |A|, γ.
2. Initialization. V_0, starting policy. Convergence sensitivity.
3. Stopping. Sup-norm tolerance ε. Expected number of sweeps.
4. Verification. V*(s_0) computed exactly. Greedy policy extracted.
5. Use. How this baseline will be used to debug/evaluate sampling-based methods.

Refuse to run DP on state spaces > 10⁷. Refuse to claim convergence without a sup-norm check. Flag any γ ≥ 1 on an infinite-horizon task as a guarantee violation.
```

## Exercícios.

1. **Easy.**Execute iteração de valor no 4×4 GridWorld com `γ ∈ {0.9, 0.99}`Quantos baralhos até`max |ΔV| < 1e-6`Impressão`V*`como uma grade 4x4.
   > **练习1：**Usar diferentes fatores de desconto para ver como a taxa de receção varia.
2. **Medium.**Compare iteração de política vs iteração de valor no GridWorld *stochastic* (probabilidade de deslize `0.1`Contar: varreduras, tempo de relógio de parede, final `V*(0,0)`O que converge mais rápido em iterações?
   > **练习2：**Comparar estratégias 代和值 代在随机网格世界中的收速度 ((代次数和运行时间) 代
3. **Hard.**Construir iteração de política modificada: na fase de avaliação, executar apenas `k`- Esvaziam em vez de convergirem.`V*(0,0)`erro vs `k`Para`k ∈ {1, 2, 5, 10, 50}`O que diz a curva sobre a compensação entre avaliação e melhoria?
   > **练习3：**                                                                                                                                                                                                                                                              

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Policy iteration | "DP algorithm" / 策略迭代 | Alternating evaluation (`V^π`) and improvement (greedy `π` w.r.t. `V^π`) until the policy stops changing. |
| Value iteration | "Faster DP" / 值迭代 | Bellman optimality backup applied in one sweep; converges to `V*` geometrically. |
| Bellman operator | "The recursion" / Bellman 算子 | `(T V)(s) = max_a Σ P (r + γ V(s'))`; a `γ`-contraction in sup-norm. |
| Contraction | "Why DP converges" / 压缩映射 | Any operator `T` with `\|\|T x - T y\|\| ≤ γ \|\|x - y\|\|` has a unique fixed point. |
| GPI | "Everything is DP" / 广义策略迭代 | Generalized Policy Iteration: any method driving `V` and `π` to mutual consistency. |
| Synchronous update | "Jacobi-style" / 同步更新 | Use old `V` throughout a sweep; cleanly analyzable but slower. |
| In-place update | "Gauss-Seidel-style" / 原地更新 | Use `V` as it's being updated; converges faster in practice. |

## Mais leitura 延伸阅读

- [Sutton & Barto (2018). Ch. 4 — Dynamic Programming](http://incompleteideas.net/book/RLbook2020.pdf) a apresentação canónica da iteração de políticas e da iteração de valores.
- [Bertsekas (2019). Reinforcement Learning and Optimal Control](http://www.athenasc.com/rlbook.html) tratamento rigoroso dos argumentos de mapeamento de contracção.
- [Puterman (2005). Markov Decision Processes](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887) a iteração da política modificada e a sua análise de convergência.
- [Howard (1960). Dynamic Programming and Markov Processes](https://mitpress.mit.edu/9780262582300/dynamic-programming-and-markov-processes/) o documento original de iteração da política.
- [Bertsekas & Tsitsiklis (1996). Neuro-Dynamic Programming](http://www.athenasc.com/ndpbook.html) a ponte de DP a aproximadamente-DP / profunda RL utilizada em cada aula subsequente.
