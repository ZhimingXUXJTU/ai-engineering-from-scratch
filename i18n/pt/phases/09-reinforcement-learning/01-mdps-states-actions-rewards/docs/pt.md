# MDPs, Estados, Ações e Recompensas

> Um processo de decisão Markov é de cinco coisas: estados, ações, transições, recompensas, um desconto. Tudo no RL  Q-learning, PPO, DPO, GRPO  otimiza sobre esta forma. Aprenda uma vez, leia o resto do aprendizado de reforço gratuitamente.

> **【中文解读】**O processo de decisão de Marco Polo (MDP) contém cinco elementos: estado, movimento, transferência, probabilidade, função de recompensa, fator de desconto, RL, tudo o que está dentro do processo de aprendizagem Q, PO, DPO, GRPO está melhorado neste quadro.

> **【拓展：MDP 是 AI 对齐的基础】**O treinamento RLHF do ChatGPT é, em essência, também um MDP: estado = diálogo sobre o diálogo,动作 = geração de tokens, recompensa = preferência humana.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 1 · 06 (Probability & Distributions), Phase 2 · 01 (ML Taxonomy) | **前置知识:** Phase 1 · 06 (概率与分布), Phase 2 · 01 (ML 分类)
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

Você está escrevendo um bot de xadrez, ou um planejador de estoque, ou um agente de negociação, ou o loop PPO que treina um modelo de raciocínio, quatro domínios diferentes, um fato surpreendente: todos os quatro colapso para o mesmo objeto matemático.

> Você está escrevendo um máquina de xadrez internacional, ou um planejador de estoque, ou um agente de negociação, ou treinando o modelo de PPO. Em quatro áreas diferentes, um fato surpreendente é que todas elas podem ser resumidas ao mesmo objeto matemático.

A aprendizagem supervisionada dá-lhe`(x, y)`O aprendizado de reforço não dá rótulos, apenas um fluxo de estados, as ações que você fez e uma recompensa escalar. A mudança ganhou o jogo? A decisão de reabastecimento economizou dinheiro? O comércio fez lucro? O token que o LLM acabou de produzir levou a uma recompensa maior do juiz?

> 监督学习给你 `(x, y)`Sim, deixe-o se adequar a uma função. A aprendizagem de potência não lhe dá uma etiqueta. Apenas o fluxo de estado.

Você não pode aprender com este fluxo até que você formalize. "O que eu vi", "o que eu fiz", "o que aconteceu depois", "o quão bom foi"  cada um tem que se tornar um objeto sobre o qual você pode raciocinar. Essa formalização é um processo de decisão de Markov. Todo algoritmo RL nesta fase, incluindo os ciclos RLHF e GRPO no final, otimiza sobre esta forma.

> Você não pode aprender com este fluxo de dados até que você o forme. "Eu vi o que""",Eu fiz o que""",O que aconteceu depois""",Isso tem muito bom" Cada um deles deve ser um objeto que você possa raciocinar. Esta formalização é o processo de decisão de Markov.

## O conceito central.

![Markov decision process: states, actions, transitions, rewards, discount](../assets/mdp.svg)

**The five objects.**- Não .**五个核心要素。**

- **States** `S`Tudo o que o agente precisa decidir, no GridWorld, a célula, no xadrez, o tabuleiro, no LLM, a janela de contexto, mais qualquer memória.
  **状态** `S` Informações necessárias para decisões inteligentes.
- **Actions** `A`As escolhas, move-se para cima/para baixo/para esquerda/direita, joga um movimento, emite um token.
  **动作** `A`△可选的操作──上/下/左/右移动──下一步棋──生成一个代币──
- **Transitions** `P(s' | s, a)`- Dado o estado .`s`e ação `a`Determinista no xadrez, estocástico no inventário, quase determinista na decodificação LLM.
  **转移概率** `P(s' | s, a)`                                                                                                                                                                                                                                                              `s`E movimentos`a`, distribuição do seguinte estado. Em Chess, a certeza é, no Management de estoques, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, a certeza é, na LLM, e na LLM, a mesma, a mesma, na LLM, e na LLM, e na LLM, e na LLM, e na JL, em que é, em que é, em
- **Rewards** `R(s, a, s')`O sinal escalar. Ganho = +1, perda = -1. receita menos custo. O termo da relação log-probabilidade em GRPO.
  **奖励** `R(s, a, s')`                                                                                                                                                                                                                                                              
- **Discount** `γ ∈ [0, 1)`Quanto é que a recompensa futura conta contra o presente?`γ = 0.99`compra um horizonte de ~ 100 passos; `γ = 0.9`- Compre 10 dólares.
  **折扣因子** `γ ∈ [0, 1)`■ o valor do futuro em relação ao valor do presente■`γ = 0.99`Para um visual válido de aproximadamente 100 passos;`γ = 0.9`Para a resposta, cerca de 10 passos.

**The Markov property** `P(s_{t+1} | s_t, a_t) = P(s_{t+1} | s_0, a_0, …, s_t, a_t)`O futuro depende apenas do estado presente. Se não o fizer, a representação do estado é incompleta.

> **马尔可夫性质**O futuro depende apenas do estado atual. Se não existir, o estado significa imperfeito.

**Policies and returns.**Uma política`π(a | s)`Mapa de estados para distribuições de ação.`G_t = r_t + γ r_{t+1} + γ² r_{t+2} + …`O valor do valor de uma remuneração é a soma descontada das recompensas futuras.`V^π(s) = E[G_t | s_t = s]`é o rendimento esperado a partir de `s`Política`π`O valor Q.`Q^π(s, a) = E[G_t | s_t = s, a_t = a]`O algoritmo RL estimou um destes dois, e depois melhorou `π`- De acordo com isso.

> **策略与回报。**策略  estratégia`π(a|s)`将状态映射到动作分布──回报 `G_t`É um valor de desconto e um valor de recompensa no futuro.`V^π(s)`É do estado.`s`O resultado da avaliação foi o resultado da avaliação de resultados.`Q^π(s,a)`Cada algoritmo RL está em uma estimativa de uma dessas duas quantidades, e, em seguida, a estratégia é melhorada.

**The Bellman equations.**As equações de ponto fixo que tudo nesta fase usa:

`V^π(s) = Σ_a π(a|s) Σ_{s', r} P(s', r | s, a) [r + γ V^π(s')]`

> **【中文解读】**A fórmula Bellman é a relação de passagem central da RL: o valor do estado atual = recompensa instantânea + valor do estado seguinte após o desconto. É a base comum do planejamento, aprendizado Q e TD. No treinamento RLHF do LLM, isso corresponde à "contribuição do token atual = porcentagem de preferências de pessoas + contribuição esperada do token futuro".

> **【拓展：从 MDP 到 POMDP】**现实中很多问题不满足马尔可夫性 (actual status cannot fully determine the future), needs to use POMDP (POMDP) 部分可观察 MDP) 建模──对话系统就是 POMDP模型只能看到上下文窗口内的内容,而不是完整的用户意图──LLM的长上下文能力本质是缓解 POMDP的信息不完整问题──
`Q^π(s, a) = Σ_{s', r} P(s', r | s, a) [r + γ Σ_{a'} π(a'|s') Q^π(s', a')]`

Estes divididos esperados retornam para "a recompensa deste passo" mais "valor descontado do lugar onde você aterrissa". Recursivo. Todo algoritmo na Fase 9 ou itera esta equação para convergência (programação dinâmica), amostras dele (Monte Carlo), ou inicializa um passo (diferência temporal).

> Estes métodos serão esperados para que o retorno seja dividido em "recompensação do passo atual" adicionada ao "valor de desconto para o estado de chegada"―.

## Construí-lo e realizei-o.
```figure
discount-horizon
```

## Construí-lo

### Passo 1: um pequeno MDP determinista

Um GridWorld 4x4. Agente começa em cima à esquerda, terminal em baixo à direita, recompensa de -1 por passo, ações.`{up, down, left, right}`- Veja .`code/main.py`- Não .

> Um mundo de 4×4 de rede. O corpo inteligente sai da esquina esquerda, termina no esquina inferior direita, cada passo é recompensado -1, movido como `{上, 下, 左, 右}`- Não.

```python
GRID = 4
TERMINAL = (3, 3)
ACTIONS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

def step(state, action):
    if state == TERMINAL:
        return state, 0.0, True
    dr, dc = ACTIONS[action]
    r, c = state
    nr = min(max(r + dr, 0), GRID - 1)
    nc = min(max(c + dc, 0), GRID - 1)
    return (nr, nc), -1.0, (nr, nc) == TERMINAL
```

Cinco linhas, é o ambiente inteiro, transições deterministas, penaltis constante, estado terminal absorvente.

> 五行代码── é o ambiente inteiro── determinação de transferência、恒定步惩罚、 absorção de estado de terminação──

### Passo 2: elaboração de uma política

Uma política é uma função da distribuição do estado para a ação.

> 策略是从状态到动作分布的函数――最简单的:均随机―― é uma função de distribuição do estado até a ação.

```python
def uniform_policy(state):
    return {a: 0.25 for a in ACTIONS}

def rollout(policy, max_steps=200):
    s, total, steps = (0, 0), 0.0, 0
    for _ in range(max_steps):
        a = sample(policy(s))
        s, r, done = step(s, a)
        total += r
        steps += 1
        if done:
            break
    return total, steps
```

Execute a política aleatória 1000 vezes. Retorno médio é de cerca de -60 a -80 para esta placa 4×4. Retorno ideal é -6 (caminho de linha reta para baixo para a direita). Fechar essa lacuna é tudo na Fase 9.

> 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 1000 次── 运行随机策略 运行随机策略 运行随机策略 运行随机策略 运行随机策略 运行随机策略 运行随机策略 运行 运行随机策略 运行 运行 运行随机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机机

### Passo 3: computação `V^π`exatamente através da equação de Bellman

Para pequenos MDPs, a equação de Bellman é um sistema linear.

> Para um pequeno MDP, a equação Bellman é um sistema linear.

```python
def policy_evaluation(policy, gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in all_states()}
    while True:
        delta = 0.0
        for s in all_states():
            if s == TERMINAL:
                continue
            v = 0.0
            for a, pi_a in policy(s).items():
                s_next, r, _ = step(s, a)
                v += pi_a * (r + gamma * V[s_next])
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            return V
```

Este é o primeiro algoritmo em Sutton & Barto e a base teórica de cada método RL que segue.

> É o primeiro algoritmo no livro de Sutton & Barto, e também a base teórica de todos os métodos RL posteriores.

### Passo 4:`γ`é um hiperparâmetro com significado físico

O horizonte eficaz é aproximadamente `1 / (1 - γ)`- Não .`γ = 0.9`→ 10 passos. `γ = 0.99`→ 100 passos. `γ = 0.999`→ 1000 passos.

> É muito bom.`1 / (1 - γ)`- Não.`γ = 0.9`Para 10 passos.`γ = 0.99`Para 100 步.`γ = 0.999`Para 1000 passos.

O agente atua de forma miope, muito baixo e a atribuição de crédito torna-se ruidosa, porque muitos passos iniciais compartilham a responsabilidade pela recompensa de futuro.`γ = 1`Os controles utilizam os seguintes métodos:`0.95–0.99`. Jogos de estratégia de longo horizonte usam`0.999`- Não .

> 折扣因子太低,智能体会目光短浅──太高,信用分配会变杂,因为 muitas etapas iniciais assumem em comum a responsabilidade de recompensa de longo prazo──LLM RLHF normalmente usa `γ = 1`, , porque o 回合短且有界── controle uso de tarefas `0.95-0.99`△长视野策略游戏使用 `0.999`- Não.

## Encurralagens

- **Non-Markovian state.**Se você precisar das últimas três observações para decidir, o "estado" não é apenas a observação atual.
  **非马尔可夫状态。**Se você precisar de três observações para tomar uma decisão, "estado" não é apenas o actual observação.
- **Sparse rewards.**Os recompensas apenas para vencer tornam a aprendizagem quase impossível em grandes espaços de estado.
  **稀疏奖励。**                                                                                                                                                                                                                                                              
- **Reward hacking.**Otimizar uma recompensa por proxy geralmente produz comportamento patológico. O agente de corrida de barcos da OpenAI gira em círculos coletando powerups para sempre em vez de terminar a corrida. Sempre defina a recompensa do resultado alvo, não do proxy.
  **奖励黑客。**优化代理奖励常产生病态行为――OpenAI's赛船代理原地转圈收集道具,永远不完成比赛――始终从目标结果定义奖励,而不是代理――
- **Discount mis-spec.** `γ = 1`Em uma tarefa de horizonte infinito, cada valor é infinito.`γ < 1`- Não .
  **折扣因子设定错误。**无限视野任务上 `γ = 1`Vai fazer tudo valer para o infinito.`γ < 1`Vamos lá.
- **Reward scale.**Os valores de {+100, -100} vs {+1, -1} dão políticas ótimas idênticas, mas magnitudes de gradiente muito diferentes.`[-1, 1]`- antes de ligar ao PPO/DQN.
  **奖励尺度。**Os prêmios de {+100, -100} e {+1, -1} fornecem as mesmas estratégias de melhor qualidade, mas as diferenças de nível de gradiência são enormes.`[-1, 1]`- Não.

## Use-o com o framework implementado.

A pilha 2026 reduz cada oleoduto RL a um MDP antes de tocar o código:

> Antes de escrever o código, cada linha de fluxo de água RL será redigida para um MDP:

| Situation | State | Action | Reward | γ |
|-----------|-------|--------|--------|---|
| Situation / 场景 | State / 状态 | Action / 动作 | Reward / 奖励 | γ |
| Control (locomotion, manipulation) / 控制（运动、操作） | Joint angles + velocities / 关节角度+速度 | Continuous torques / 连续力矩 | Task-specific shaped / 任务特定塑形 | 0.99 |
| Games (chess, Go, poker) / 游戏（象棋、围棋、扑克） | Board + history / 棋盘+历史 | Legal move / 合法走法 | Win=+1 / loss=-1 / 胜=+1/负=-1 | 1.0 (finite) |
| Inventory / pricing / 库存/定价 | Stock + demand / 库存+需求 | Order qty / 订购量 | Revenue - cost / 收入-成本 | 0.95 |
| RLHF for LLMs / LLM 的 RLHF | Context tokens / 上下文 token | Next token / 下一个 token | Reward-model score at end / 末尾奖励模型分数 | 1.0 (episode ~200 tokens) |
| GRPO for reasoning / 推理的 GRPO | Prompt + partial response / 提示+部分回复 | Next token / 下一个 token | Verifier 0/1 at end / 末尾验证器 0/1 | 1.0 |

Escreva os cinco tuples antes de escrever qualquer loop de treinamento. A maioria dos relatórios de bugs "RL não funciona" remonta a uma formulação MDP que foi quebrada no papel.

> Antes de escrever qualquer ciclo de treinamento, escreva-se o seguinte:

## Envia-o . Produto .

Salva como`outputs/skill-mdp-modeler.md`- Não .

```markdown
---
name: mdp-modeler
description: Given a task description, produce a Markov Decision Process spec and flag formulation risks before training.
version: 1.0.0
phase: 9
lesson: 1
tags: [rl, mdp, modeling]
---

Given a task (control / game / recommendation / LLM fine-tuning), output:

1. State. Exact feature vector or tensor spec. Justify Markov property.
2. Action. Discrete set or continuous range. Dimensionality.
3. Transition. Deterministic, stochastic-with-known-model, or sample-only.
4. Reward. Function and source. Sparse vs shaped. Terminal vs per-step.
5. Discount. Value and horizon justification.

Refuse to ship any MDP where the state is non-Markovian without explicit mention of frame-stacking or recurrent state. Refuse any reward that was not defined in terms of the target outcome. Flag any `γ ≥ 1.0` on an infinite-horizon task. Flag any reward range >100x the typical step reward as a likely gradient-explosion source.
```

## Exercícios.

1. **Easy.**Implementar o 4x4 GridWorld e a implementação de políticas aleatórias em `code/main.py`- Exercer 10.000 episódios. Relatar média e STD de retorno. Comparar com o retorno ideal (-6).
   > **练习1（简单）：**实现 4×4 GridWorld 和随机策略 rollout──运行 10,000 回合──报告回报的平均值和标准差,与最优回报 (-6) 比较──
2. **Medium.**Corra .`policy_evaluation`com`γ ∈ {0.5, 0.9, 0.99}`Para a política uniforme aleatória.`V`Explique por que os valores de estado perto do terminal crescem mais rápido com a maior`γ`- Não .
   > **练习2（中等）：**- Não .`γ ∈ {0.5, 0.9, 0.99}`运行策略评估──印每 γ 的 4×4 值网格──解释为什么接近终止状态的状态值在更大的 γ 下增长更快──
3. **Hard.**Virar a GridWorld estocástica: cada ação desliza para uma direção adjacente com probabilidade `p = 0.1`Reevaluar a política de uniforme.`V[start]`- Melhor ou pior?
   > **练习3（困难）：**Vai transformar o GridWorld em "quase"`p = 0.1`滑向相邻方向── reevaluar estratégias de avaliação`V[start]`- É melhor ou pior?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
| MDP | "Reinforcement learning setup" | Tuple `(S, A, P, R, γ)` satisfying the Markov property. |
| State / 状态 | "What the agent sees" / "智能体看到什么" | Sufficient statistic for future dynamics under the chosen policy class. |
| Policy / 策略 | "Agent's behavior" / "智能体的行为" | Conditional distribution `π(a \| s)` or deterministic map `s → a`. |
| Return / 回报 | "Total reward" / "总奖励" | Discounted sum `Σ γ^t r_t` from the current step. |
| Value / 值函数 | "How good a state is" / "状态有多好" | Expected return under `π` starting from `s`. |
| Q-value / Q值 | "How good an action is" / "动作有多好" | Expected return under `π` starting from `s` with first action `a`. |
| Bellman equation / Bellman方程 | "Dynamic programming recursion" / "动态规划递推" | Fixed-point decomposition of value / Q into one-step reward plus discounted successor value. |
| Discount `γ` / 折扣因子 | "Future vs present" / "未来vs当前" | Geometric weight on far-future reward; effective horizon `~1/(1-γ)`. |

## Mais leitura 延伸阅读

- [Sutton & Barto (2018). Reinforcement Learning: An Introduction, 2nd ed.](http://incompleteideas.net/book/RLbook2020.pdf)O capítulo 3 abrange as MDPs e as equações de Bellman; o capítulo 1 motiva a hipótese de recompensa que subjacente a cada lição subsequente.
- [Bellman (1957). Dynamic Programming](https://press.princeton.edu/books/paperback/9780691146683/dynamic-programming) a origem da equação de Bellman.
- [OpenAI Spinning Up — Part 1: Key Concepts](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html) Primer MDP conciso a partir de um ângulo de RL profundo.
- [Puterman (2005). Markov Decision Processes](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887) a referência de investigação operacional sobre os MDP e os métodos de solução exatas.
- [Littman (1996). Algorithms for Sequential Decision Making (PhD thesis)](https://www.cs.rutgers.edu/~mlittman/papers/thesis-main.pdf) a mais limpa derivação dos MDPs como especialização em programação dinâmica.
