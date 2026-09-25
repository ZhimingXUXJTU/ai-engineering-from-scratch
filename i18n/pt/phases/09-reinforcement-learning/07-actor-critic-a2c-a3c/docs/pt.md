# Ator-Critico  A2C e A3C  Ator-Comentarista  A2C e A3C

> A ReINFORCE é barulhenta, adicione um crítico que aprenda.`V̂(s)`A 2C executa sincronicamente; A 3C executa através de fios. Ambos são o modelo mental para cada método moderno de RL profundo.

> **【中文解读】**REINFORCE 方差太大──加入一个"评论家"(Critical)学习 V̂(s), usá-lo como base para construir vantagem função A = G - V̂(s), expectativa não mudar, mas a diferença é muito menor── é o que Actor-CriticalPPO、SAC 等 todos os modernos profundidade RL 方法的架构原型──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 04 (TD Learning), Phase 9 · 06 (REINFORCE) | **前置知识:** Phase 9 · 04 (TD 学习), Phase 9 · 06 (REINFORCE)
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

A Vanilla ReINFORCE funciona, mas a sua variação é terrível.`G_t`O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é.`∇ log π`e a média produz um estimador de gradiente que leva milhares de episódios para mover a política a mesma distância que você poderia mover com muito menos atualizações DQN.

> O primeiro reforço é eficaz, mas a diferença é muito ruim.`G_t`Em um período de tempo, o ruído pode aumentar 10 vezes.`∇ log π`A partir de agora, a média de estimadores de gradientes resultantes requer milhares de reatempos para que a estratégia de movimentação seja alcançada com menos DQN.

A variação vem do uso de retornos brutos. Se subtrair uma linha de base `b(s_t)` qualquer função de estado, incluindo um valor aprendido  a expectativa é inalterada e a variância cai.`V̂(s_t)`Agora a quantidade se multiplica .`∇ log π`é a *vantagem*:

`A(s, a) = G - V̂(s)`

> 方差来自使用原始回报──如果减去基线 `b(s_t)` Qualquer função de estado, incluindo o valor do aprendizado  expectativa não mudar mas a diferença reduzir.`V̂(s_t)`Agora, vamos para o outro lado.`∇ log π`É o que eu quero dizer.

Uma ação é boa se produzir retornos acima da média; ruim se abaixo. REINFORCE com um crítico erudito é *actor-crítica*. O crítico dá ao ator um professor de baixa variação. Este é todo método de política profunda após 2015 (A2C, A3C, PPO, SAC, IMPALA).

> 动作好如果产生高于平均的回报;差如果低于──带学习批评的 REINFORCE 就是 *Actor-Critic*──Critic 给 Actor一个低方差的老师──这是2015年后每深度策略方法(A2C、A3C、PPO、SAC、IMPALA)──

## O conceito central.

![Actor-critic: policy net plus value net, TD residual as advantage](../assets/actor-critic.svg)

**Two networks, one shared loss:**

> **两个网络，一个共享损失：**

- **Actor** `π_θ(a | s)`A política: a política.
  **Actor** `π_θ(a | s)`• estratégia.
- **Critic** `V_φ(s)`As estimativas de retorno esperado do estado.`(V_φ(s) - target)²`- Não .
  **Critic** `V_φ(s)`O resultado da avaliação é o resultado da avaliação do estado.`(V_φ(s) - target)²`- Não.

**The advantage.**Dois formulários padrão:

> **优势函数。**两种标准形式:

- *Vantagem MC:* `A_t = G_t - V_φ(s_t)`Imparcial, maior variância.
  *MC 优势:* 无偏,方差较高──
- *Vantagem TD:* `A_t = r_{t+1} + γ V_φ(s_{t+1}) - V_φ(s_t)`. Preciados (utilizos `V_φ`O valor de variação é muito menor.`δ_t`- Não .
  *TD 优势:* 有偏差(使用 `V_φ`),方差远低── também chamado *TD残差* `δ_t`- Não.

**n-step advantage.**Interpolar entre os dois:

`A_t^{(n)} = r_{t+1} + γ r_{t+2} + … + γ^{n-1} r_{t+n} + γ^n V_φ(s_{t+n}) - V_φ(s_t)`

`n = 1`é TD puro. `n = ∞`A maioria das implementações utiliza`n = 5`para a Atari, `n = 2048`Para o PPO no MuJoCo.

> **n 步优势。**Entre os dois, entre os dois.`n = 1`É pura TD.`n = ∞`É MC. A maioria realiza Atari.`n = 5`MuJoCo, o PPO do topo.`n = 2048`- Não.

**Generalized Advantage Estimation (GAE).**Schulman et al. (2016) propôs uma média ponderada exponencialmente sobre todas as vantagens do n-passo:

`A_t^{GAE} = Σ_{l=0}^{∞} (γλ)^l δ_{t+l}`

com`λ ∈ [0, 1]`- Não .`λ = 0`é TD (baixa variância, alto viés). `λ = 1`é MC (alta variância, imparcial). `λ = 0.95`é o 2026 de acordo com o padrão  tune até que o dial de desvio/variância esteja onde você quer.

> **【中文解读】**GAE(广义优势估算) é uma das principais melhorias do Actor-Critic: através do índice de aumento de peso média de todos os n 步优势, entre o prejuízo e o prejuízo, encontrar o melhor equilíbrio.

> **【拓展：GAE 在 RLHF 中的应用】**O PPO de ChatGPT  treino usando GAE  calcular vantagem função。 em LLM 场景, "status" é uma sequência de tokens gerada, "动作" é o próximo token, "premiação" é proveniente do modelo de recompensa。 GAE 让 PPO 能在长文本生成(100 tokens)

**A2C: synchronous advantage actor-critic.**Coletar`T`Passo de cruzamento .`N`Paralelas de ambiente. Compute vantagens para cada passo. Atualize ator e crítico no lote combinado. Repita. O irmão mais simples e mais escalavel do A3C.

> **A2C：同步优势 Actor-Critic。**Em`N`个并行环境中收集                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `T`步──计算每步优势──在合并批次上更新 Actor 和 Critic──重复──A3C's 更多简单,更多可扩展的兄弟──

**A3C: asynchronous advantage actor-critic.**Mnih et al. (2016). Spawn `N`As funções de trabalho são de um tipo de processador, cada um executando um env. Cada trabalhador calcula gradientes localmente em sua própria implementação, em seguida, assincronicamente os aplica a um servidor de parâmetros compartilhado.

> **A3C：异步优势 Actor-Critic。**Mnih 等人 (2016)。 iniciação `N`个工作线程, cada um executando um ambiente. Cada trabalho线程 está em um gradiente de cálculo local, então é aplicado em diferentes fases para servidores de parâmetros compartilhados.

**The combined loss.**

`L(θ, φ) = -E[ A_t · log π_θ(a_t | s_t) ]  +  c_v · E[(V_φ(s_t) - G_t)²]  -  c_e · E[H(π_θ(·|s_t))]`

Três termos: perda de grau de política, regressão de valor, bônus de entropia. `c_v ~ 0.5`- Não .`c_e ~ 0.01`são pontos de partida canônicos.

> **组合损失。**Três: estratégia de perda de valor, retorno de valor, recompensa.`c_v ~ 0.5`- Não.`c_e ~ 0.01`É o típico valor inicial.

> **【中文解读】**Actor-Critic's composite loss = estratégia gradiente loss + 值函数归归 + 正则化── these three distinctly对应:

> **【拓展：GAE→PPO→RLHF】**GAE (广义优势估算) é um componente central do PPO, enquanto PPO é o algoritmo padrão do treinamento ChatGPT RLHF ∙∙λ=0.95 é o valor padrão de 2026, para obter um equilíbrio entre o preconceito e o preconceito ∙

## Construí-lo e realizei-o.
```figure
actor-critic
```

## Construí-lo

### Passo 1: um crítico

Crítico linear `V_φ(s) = w · features(s)`Atualizado com a MSE:

```python
def critic_update(w, x, target, lr):
    v_hat = dot(w, x)
    err = target - v_hat
    for j in range(len(w)):
        w[j] += lr * err * x[j]
    return v_hat
```

Em um ambiente tabular o crítico converge em algumas centenas de episódios.

> 线性批判 `V_φ(s) = w · features(s)`Usar MSE 更新──在表格环境中几百回合就收──在 Atari 上, substituindo por compartilhar CNN 主干 + 值头──

### Passo 2: vantagem de n-passo

Dado o seu comprimento .`T`E uma final de arranque .`V(s_T)`- Não .

```python
def compute_advantages(rewards, values, gamma=0.99, lam=0.95, last_value=0.0):
    advantages = [0.0] * len(rewards)
    gae = 0.0
    for t in reversed(range(len(rewards))):
        next_v = values[t + 1] if t + 1 < len(values) else last_value
        delta = rewards[t] + gamma * next_v - values[t]
        gae = delta + gamma * lam * gae
        advantages[t] = gae
    returns = [a + v for a, v in zip(advantages, values)]
    return advantages, returns
```

`returns`É o alvo crítico.`advantages`é o que se multiplica.`∇ log π`- Não .

> `returns`É crítico.`advantages`É o que se passa .`∇ log π`- Não.

### Passo 3: atualização combinada

```python
for step_i, (x, a, _r, probs) in enumerate(traj):
    adv = advantages[step_i]
    target_v = returns[step_i]

    # critic
    critic_update(w, x, target_v, lr_v)

    # actor
    for i in range(N_ACTIONS):
        grad_logpi = (1.0 if i == a else 0.0) - probs[i]
        for j in range(N_FEAT):
            theta[i][j] += lr_a * adv * grad_logpi * x[j]
```

Na política, uma implementação por atualização, taxas de aprendizagem separadas para ator e crítico.

> Em linha estratégia, cada vez mais um rollout, Ator e crítico usando diferentes taxas de aprendizagem.

### Passo 4: paralelação (A3C vs. A2C)

- **A3C:**- Não .`N`Cada um corre seu próprio env e seu próprio pass para a frente. Periodicamente empurrar atualizações de gradiente para um mestre compartilhado.
- **A2C:**- Correr .`N`Env instâncias num único processo, empilhar observações em um `[N, obs_dim]`Batch, batch forward pass, batch backward pass. Maior utilização de GPU, determinista, mais fácil de raciocinar.

O nosso código de brinquedo é de um único fio para a clareza; reescrever para A2C em lote é três linhas de numpy.

> O nosso código de brinquedos é de linha única para manter a clareza; reescrever para o volume A2C só precisa de três linhas de numpy.

## Encurralagens

- **Critic bias before actor gradient.**Se o crítico é aleatório, a sua linha de base é desinformativa e você está treinando em ruído puro. aqueça o crítico por algumas centenas de passos antes de ativar o gradiente de política, ou use uma taxa lenta de aprendizagem de atores.
  **Actor 梯度之前的 Critic 偏差。**Se o crítico é aleatório, a sua linha de base não tem quantidade de informação, você treina em puro ruído.
- **Advantage normalization.**Normaliza as vantagens para zero média/unit-std por lote. Estabiliza o treinamento em massa a um custo próximo a zero.
  **优势归一化。**Cada lote será reintegrado em um valor médio/unidade de diferença.
- **Shared trunk.**Use um extractor de recursos compartilhado para ator e crítico em entradas de imagem. cabeças separadas. Os recursos compartilhados de livre-mover em ambas as perdas.
  **共享主干。**图像输入时使用共享特征提取器──分开的头──共享特征同时从两个损失中获益──
- **On-policy contract.**A A2C reutiliza dados para exatamente uma atualização. Mais e o seu gradiente é tendencioso (a correção de amostragem de importância é o que a PPO adiciona).
  **在线策略约束。**A A2C 恰好用数据做一次更新.
- **Entropy collapse.**Sem .`c_e > 0`A política se torna quase determinista em algumas centenas de atualizações e deixa de explorar.
  **熵坍缩。**Não há nada .`c_e > 0`A estratégia, após centenas de atualizações, se tornou quase definida e deixou de ser explorada.
- **Reward scale.**Grandes vantagens dependem da escala de recompensa. Normalize recompensas (por exemplo, divisão run-std) para magnitudes de gradiente consistentes em tarefas.
  **奖励尺度。**Classe de vantagem depende da medida de recompensa

## Use-o com o framework implementado.

A2C/A3C raramente são a escolha final em 2026, mas são a arquitetura que tudo mais tarde refinará:

> A2C/A3C em 2026 é raramente a escolha final, mas são mais tarde uma estrutura refinada:

| Method | Relation to A2C |
|--------|----------------|
| Method / 方法 | Relation to A2C / 与 A2C 的关系 |
| PPO | A2C + clipped importance ratio for multi-epoch updates / A2C + 裁剪重要性比率用于多轮更新 |
| IMPALA | A3C + V-trace off-policy correction / A3C + V-trace 离策略修正 |
| SAC (Phase 9 · 07) | Off-policy A2C with a soft-value critic (next lesson) / 离策略 A2C + 软值 Critic |
| GRPO (Phase 9 · 12) | A2C without the critic — group-relative advantage / 无 Critic 的 A2C——组相对优势 |
| DPO | A2C collapsed into a preference-ranking loss, no sampling / 折叠为偏好排名损失的 A2C |
| AlphaStar / OpenAI Five | A2C with league training + imitation pre-training / A2C + 联盟训练 + 模仿预训练 |

Se virem "vantagem" num artigo de 2026, pensem em crítico de actores.

> Se você ver "Unexity" em seu artigo de 2026 ano, pense no Actor-Critic.

## Envia-o . Produto .

Salva como`outputs/skill-actor-critic-trainer.md`- Não .

```markdown
---
name: actor-critic-trainer
description: Produce an A2C / A3C / GAE configuration for a given environment, with advantage estimation and loss weights specified.
version: 1.0.0
phase: 9
lesson: 7
tags: [rl, actor-critic, gae]
---

Given an environment and compute budget, output:

1. Parallelism. A2C (GPU batched) vs A3C (CPU async) and the number of workers.
2. Rollout length T. Steps per env per update.
3. Advantage estimator. n-step or GAE(λ); specify λ.
4. Loss weights. `c_v` (value), `c_e` (entropy), gradient clip.
5. Learning rates. Actor and critic (separate if using).

Refuse single-worker A2C on environments with horizon > 1000 (too on-policy, too slow). Refuse to ship without advantage normalization. Flag any run with `c_e = 0` and observed entropy < 0.1 as entropy-collapsed.
```

## Exercícios.

1. **Easy.**Treinar actor-crítica com vantagem MC (`G_t - V(s_t)`Compare a eficiência da amostra com a linha de base da REINFORCE-with-running-median de lição 06.
2. **Medium.**A transição para a vantagem residual TD (`r + γ V(s') - V(s)`A diferença entre os lotes de vantagem é medida.
3. **Hard.**Implementar o GAE ((λ).`λ ∈ {0, 0.5, 0.9, 0.95, 1.0}`O que é o ponto de preferência para esta tarefa?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Actor | "The policy net" / 演员（策略网络） | `π_θ(a\|s)`, updated by policy gradient. |
| Critic | "The value net" / 评论家（值网络） | `V_φ(s)`, updated by MSE regression to returns / TD targets. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = Q(s, a) - V(s)` or its estimators. Multiplier for `∇ log π`. |
| TD residual | "δ" / TD 残差 | `δ_t = r + γ V(s') - V(s)`; one-step advantage estimate. |
| GAE | "The interpolation knob" / 广义优势估计 | Exponentially weighted sum of n-step advantages, parameterized by `λ`. |
| A2C | "Synchronous actor-critic" / 同步演员-评论家 | Batched across envs; one gradient step per rollout. |
| A3C | "Async actor-critic" / 异步演员-评论家 | Worker threads push gradients to a shared param server. Original paper; less common in 2026. |
| Bootstrap | "Use V at the horizon" / 自举截断 | Truncate the rollout, add `γ^n V(s_{t+n})` to close the sum. |

## Mais leitura 延伸阅读

- [Mnih et al. (2016). Asynchronous Methods for Deep Reinforcement Learning](https://arxiv.org/abs/1602.01783) A3C, o papel crítico-actor asíncrono original.
- [Schulman et al. (2016). High-Dimensional Continuous Control Using Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438) GAE.
- [Sutton & Barto (2018). Ch. 13 — Actor-Critic Methods](http://incompleteideas.net/book/RLbook2020.pdf) fundamentos; combinar isto com o capítulo 9 sobre aproximação de funções quando o crítico é uma rede neural.
- [Espeholt et al. (2018). IMPALA](https://arxiv.org/abs/1802.01561) Escalabilidade distribuída de actor-crítica com correcção de fora de política de rastreamento V.
- [OpenAI Baselines / Stable-Baselines3](https://stable-baselines3.readthedocs.io/) implementações de produção A2C/PPO que valham a pena ler.
- [Konda & Tsitsiklis (2000). Actor-Critic Algorithms](https://papers.nips.cc/paper/1786-actor-critic-algorithms) o resultado de convergência fundamental para a decomposição actor-crítica em duas escalas.
