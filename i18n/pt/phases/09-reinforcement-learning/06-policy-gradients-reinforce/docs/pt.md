# Política Gradiente  REINFORCE do zero  estratégia                                                                                                                                                                                                                                                       

> Para de estimar o valor. Parametrizar a política diretamente, calcular o gradiente do retorno esperado, passo para cima. Williams (1992) escreveu em um teorema. É por isso que PPO, GRPO e cada ciclo LLM RL existem.

> **【中文解读】**Não reavaliação da função, estratégia de parametrização directa π_θ(a)), cálculo de expectativa de retorno de escala ou escala de aumento.`∇J(θ) = E[G · ∇log π_θ(a|s)]` É por isso que existe o PPO ̊GRPO ̊ e todos os grandes ciclos de treinamento RL ̊.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 03 (Monte Carlo), Phase 9 · 04 (TD Learning) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 03 (蒙特卡洛), Phase 9 · 04 (TD 学习)
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

Q-learning e DQN paramétricos da função *valor*.`argmax Q`O que é bom para ações discretas e estados discretos.`argmax`sobre um torque de 10 dimensões?) ou quando você quer uma política estocástica (`argmax`É determinista por construção).

> Q-learning 和 DQN 参数化*值*函数──通过 `argmax Q`选择动作── Isso é um problema para o movimento separado e o estado separado não é problema── mas quando o movimento continua10 维力矩上取哪个`argmax`• ou necessitar de estratégias`argmax`Naturalmente é certo, já está em ruínas.

Os gradientes de política parametrizam a *política* em vez disso. `π_θ(a | s)`A rede neural é uma rede neural que produz uma distribuição sobre ações.`θ`- Passa para cima.`argmax`Não há recursão de Bellman, só ascensão de gradiente.`J(θ) = E_{π_θ}[G]`- Não .

> 策略梯度改为参数化*策略*──`π_θ(a | s)`É uma rede de distribuição de movimentos de saída.`θ`É preciso que o meu pai me diga que não é preciso.`argmax`Não preciso de Bellman.`J(θ) = E_{π_θ}[G]`A escala de elevação...

O teorema de REINFORCE (Williams 1992) diz que este gradiente é computavel: `∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`- Exerça um episódio, calcula o retorno, multiplica por`∇ log π_θ(a | s)`- A média, a ascensão gradual, pronto.

> Reforça-nos, diz-nos que esta escala é calculavel.`∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`◊运行一个回合――计算回报―― cada passo multiplicado `∇ log π_θ(a | s)`△取平均──梯度上升──完成──

Cada algoritmo LLM-RL em 2026  PPO, DPO, GRPO  é um aperfeiçoamento da REINFORCE.

> Em 2026 cada LLM-RL 算法PPO、DPO、GRPO são refinamentos de REINFORCE.

> **【中文解读】** estratégia gradiente  estratégia gradiente  estratégia                                                                                                                                                                                                                                                      `∇log π`É o "direção de estratégia", multiplicado por "G" é "em direção certa".

> **【拓展：PPO→ChatGPT对齐】**O algoritmo de PPO  que é usado pelo ChatGPT  RLHF   treinamento                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `loss = -advantage * log_prob`Esta linha de código, aparecendo em quase todos os grandes modelos RL 2026 anos  formação de guião.

## O conceito central.

![Policy gradient: softmax policy, log-π gradient, return-weighted update](../assets/policy-gradient.svg)

**The policy gradient theorem.**Para qualquer política`π_θ`Parametrizado por `θ`- Não .

`∇J(θ) = E_{τ ~ π_θ}[ Σ_{t=0}^{T} G_t · ∇_θ log π_θ(a_t | s_t) ]`

onde`G_t = Σ_{k=t}^{T} γ^{k-t} r_{k+1}`é o retorno descontado do passo `t`A expectativa é de que as trajetórias sejam completas .`τ`amostragem de `π_θ`- Não .

> **策略梯度定理。**Para qualquer coisa.`θ`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `π_θ`, a expectativa de retorno é igual a: desconto de retorno e multiplicação da expectativa de retorno para a expectativa de retorno de estratégias numéricas.`π_θ`O que é que é que é?

**The proof is short.**Diferenciar `J(θ) = Σ_τ P(τ; θ) G(τ)`- Não é o que se espera.`∇P(τ; θ) = P(τ; θ) ∇ log P(τ; θ)`Factor `log P(τ; θ) = Σ log π_θ(a_t | s_t) + environment terms that do not depend on θ`Os termos de ambiente desaparecem. Duas linhas de álgebra dão-lhe o teorema.

> **证明很短。**Em espera de`J(θ)`求导――使用对数导数技巧――将 `log P(τ; θ)`O que é o que se passa com o ambiente?

**Variance reduction tricks.**A Vanilla ReINFORCE tem uma variância homicida. Os retornos são ruidosos.`∇ log π`O produto é muito barulhento.

> **方差降低技巧。**A primeira força de reabastecimento tem uma grande diferença de volume.`∇ log π`Há ruído, a sua multiplicidade é maior.

1. **Baseline subtraction.**Substitui`G_t`com`G_t - b(s_t)`para qualquer linha de base `b(s_t)`que não depende de `a_t`- Imparcial porque`E[b(s_t) · ∇ log π(a_t | s_t)] = 0`. Escolha típica: `b(s_t) = V̂(s_t)`aprendizado por um crítico → ator-crítico (Lessão 07).
   **基线减法。**- Não .`G_t - b(s_t)`替换 `G_t`❖ típico seleccion:`b(s_t) = V̂(s_t)`Por crítico 学习 → Actor-Critic (Lessão 07)
2. **Reward-to-go.**Substitui`Σ_t G_t · ∇ log π_θ(a_t | s_t)`com`Σ_t G_t^{from t} · ∇ log π_θ(a_t | s_t)`. Apenas os retornos futuros são importantes para uma determinada ação  Os retornos passados contribuem com ruído zero-médio.
   **未来回报。** Apenas o retorno futuro para determinadas acções é significativocontribuição de recompensas do passado  0 volume de ruído médio

Combinados, obtém:

`∇J ≈ (1/N) Σ_{i=1}^{N} Σ_{t=0}^{T_i} [ G_t^{(i)} - V̂(s_t^{(i)}) ] · ∇_θ log π_θ(a_t^{(i)} | s_t^{(i)})`

que é REINFORCE com uma linha de base  o ancestral directo do A2C (Lessão 07) e do PPO (Lessão 08).

**Softmax policy parameterization.**Para ações discretas, a escolha padrão:

`π_θ(a | s) = exp(f_θ(s, a)) / Σ_{a'} exp(f_θ(s, a'))`

onde`f_θ`É qualquer rede neural que produz uma pontuação por ação.

`∇_θ log π_θ(a | s) = ∇_θ f_θ(s, a) - Σ_{a'} π_θ(a' | s) ∇_θ f_θ(s, a')`

Por exemplo, o resultado da acção tomada menos o seu valor esperado no âmbito da política.

> **Softmax 策略参数化。**Para a separação de movimentos, gradiente forma simplificar:

**Gaussian policy for continuous actions.** `π_θ(a | s) = N(μ_θ(s), σ_θ(s))`- Não .`∇ log N(a; μ, σ)`A fase 9 · 07 é a fase de SAC.

> **连续动作的高斯策略。** `∇ log N(a; μ, σ)`Há uma solução completa. É tudo o que é necessário para a Fase 9 · 07 do SAC.

## Construí-lo e realizei-o.
```figure
policy-gradient-landscape
```

## Construí-lo

### Passo 1: rede de políticas softmax

```python
def policy_logits(theta, state_features):
    return [dot(theta[a], state_features) for a in range(N_ACTIONS)]

def softmax(logits):
    m = max(logits)
    exps = [exp(l - m) for l in logits]
    Z = sum(exps)
    return [e / Z for e in exps]
```

Use uma política linear (um vetor de peso por ação) para um envelope tabuleiro. Para Atari, troque em uma CNN e mantenha a cabeça softmax.

> A Atari, mudou para a CNN e manteve suavidade máxima.

### Passo 2: amostragem e probabilidade de registro

```python
def sample_action(probs, rng):
    x = rng.random()
    cum = 0
    for a, p in enumerate(probs):
        cum += p
        if x <= cum:
            return a
    return len(probs) - 1

def log_prob(probs, a):
    return log(probs[a] + 1e-12)
```

### Passo 3: lançamento com log-probes capturados

```python
def rollout(theta, env, rng, gamma):
    trajectory = []
    s = env.reset()
    while not done:
        logits = policy_logits(theta, s)
        probs = softmax(logits)
        a = sample_action(probs, rng)
        s_next, r, done = env.step(s, a)
        trajectory.append((s, a, r, probs))
        s = s_next
    return trajectory
```

### Passo 4: Atualização da REINFORCE

```python
def reinforce_step(theta, trajectory, gamma, lr, baseline=0.0):
    returns = compute_returns(trajectory, gamma)
    for (s, a, _, probs), G in zip(trajectory, returns):
        advantage = G - baseline
        grad_log_pi_a = [-p for p in probs]
        grad_log_pi_a[a] += 1.0
        for i in range(N_ACTIONS):
            for j in range(len(s)):
                theta[i][j] += lr * advantage * grad_log_pi_a[i] * s[j]
```

O gradiente`∇ log π(a|s) = e_a - π(·|s)`(exceto em`a`- probabilidades) é o coração dos gradientes de política softmax.

> 梯度 `∇ log π(a|s) = e_a - π(·|s)`(`a`O que é um dos principais fatores que podem ser observados em um estudo de um grupo de pacientes com diabetes mellitus?

### Passo 5: Linhas de base

Uma média corrente de `G`Em relação aos episódios recentes, a redução de variância é suficiente para que um GridWorld 4×4 seja executado; é preciso ~ 500 episódios para convergir.`V̂(s)`E você tem crítico de ator.

> Recentemente reunido`G`O valor médio de operação é suficiente para permitir que 4×4 GridWorld trabalhe; cerca de 500 回合收──将基线升级为学习的`V̂(s)`É um ator crítico.

## Encurralagens

- **Exploding gradients.**Os rendimentos podem ser enormes.`G`- Não .`~N(0, 1)`através do lote antes de multiplicar por `∇ log π`- Não .
  **梯度爆炸。**O relatório pode ser muito grande.`∇ log π`之前始终将 `G`归一化到 `~N(0, 1)`- Não.
- **Entropy collapse.**A política converge para uma ação quase determinista muito cedo, deixa de explorar, fica presa.`β · H(π(·|s))`Para o objectivo.
  **熵坍缩。**策略过早收到近确定性动作,停止探索,陷入困境──修复:向目标添加奖励 `β · H(π(·|s))`- Não.
- **High variance.**A Vanilla REINFORCE precisa de milhares de episódios.
  **高方差。**O primeiro é o "Critical 基线" (Lessão 07) ou "Trusted Domain" (Lessão 08) (Lessão 08) é "standard修复").
- **Sample inefficiency.**A correcção extra-política através da amostragem de importância traz dados, ao custo da variação (a taxa da OPP é um peso de IS reduzido).
  **样本效率低。**O estratégico online significa que todos os transferências são abandonadas após cada atualização.
- **Non-stationary gradients.**O mesmo gradiente de há 100 episódios usa o antigo .`π`Os métodos de política atualizam cada algumas implementações por este motivo.
  **非平稳梯度。**100 回合前的梯度使用旧的 `π`                                                                                                                                                                                                                                                              
- **Credit assignment.**Sem recompensa, recompensas passadas contribuem com ruído.
  **信用分配。**没有未来回报,过去的奖励贡献噪声──始终使用未来回报──

## Use-o com o framework implementado.

Em 2026, o REINFORCE raramente é executado diretamente, mas a sua fórmula de gradiente está em toda parte:

> 2026 anos, REINFORCE  muito poucas operações diretas, mas sua gradiência fórmula não está presente:

| Use case | Derived method |
|----------|---------------|
| Use case / 用例 | Derived method / 派生方法 |
| Continuous control / 连续控制 | PPO / SAC with Gaussian policy / 高斯策略的 PPO/SAC |
| LLM RLHF / LLM RLHF | PPO with KL penalty, running on token-level policy / 带 KL 惩罚的 PPO，token 级策略 |
| LLM reasoning (DeepSeek) / LLM 推理 | GRPO — REINFORCE with group-relative baseline, no critic / 组相对基线的 REINFORCE，无 critic |
| Multi-agent / 多智能体 | Centralized-critic REINFORCE (MADDPG, COMA) / 集中 critic 的 REINFORCE |
| Discrete action robotics / 离散动作机器人 | A2C, A3C, PPO |
| Preference-only settings / 仅偏好设置 | DPO — REINFORCE rewritten as a preference-likelihood loss, no sampling / 重写为偏好似然损失的 REINFORCE |

Quando você lê`loss = -advantage * log_prob`Os trabalhos completos (DPO, GRPO, RLOO) são truques de redução de variância no topo desta linha.

> Quando você estiver lendo o livro de treinamento de 2026`loss = -advantage * log_prob`, é o reforço da linha de base.

## Envia-o . Produto .

Salva como`outputs/skill-policy-gradient-trainer.md`- Não .

```markdown
---
name: policy-gradient-trainer
description: Produce a REINFORCE / actor-critic / PPO training config for a given task and diagnose variance issues.
version: 1.0.0
phase: 9
lesson: 6
tags: [rl, policy-gradient, reinforce]
---

Given an environment (discrete / continuous actions, horizon, reward stats), output:

1. Policy head. Softmax (discrete) or Gaussian (continuous) with parameter counts.
2. Baseline. None (vanilla), running mean, learned `V̂(s)`, or A2C critic.
3. Variance controls. Reward-to-go on by default, return normalization, gradient clip value.
4. Entropy bonus. Coefficient β and decay schedule.
5. Batch size. Episodes per update; on-policy data freshness contract.

Refuse REINFORCE-no-baseline on horizons > 500 steps. Refuse continuous-action control with a softmax head. Flag any run with `β = 0` and observed policy entropy < 0.1 as entropy-collapsed.
```

## Exercícios.

1. **Easy.**Implementar REINFORCE no 4×4 GridWorld com uma política de softmax linear. Treinar por 1.000 episódios sem uma linha de base. Planejar a curva de aprendizagem; medir a variância (std de retornos).
2. **Medium.**Adicione uma linha de base de corrida média. Treine novamente. Compare a eficiência da amostra e a variância com a corrida de baunilha. Em quanto a linha de base reduz os passos para a convergência?
3. **Hard.**Adicionar um bônus de entropia `β · H(π)`- Esvaziar .`β ∈ {0, 0.01, 0.1, 1.0}`O que é que é o ponto de encontro desta tarefa?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Policy gradient | "Train the policy directly" / 策略梯度 | `∇J(θ) = E[G · ∇ log π_θ(a\|s)]`; derived from the log-derivative trick. |
| REINFORCE | "The original PG algorithm" / REINFORCE算法 | Williams (1992); Monte Carlo returns multiplied by log-policy gradient. |
| Log-derivative trick | "Score function estimator" / 对数导数技巧 | `∇P(τ;θ) = P(τ;θ) · ∇ log P(τ;θ)`; makes gradients of expectations tractable. |
| Baseline | "Variance reduction" / 基线 | Any `b(s)` subtracted from `G`; unbiased because `E[b · ∇ log π] = 0`. |
| Reward-to-go | "Only future returns count" / 未来回报 | `G_t^{from t}` instead of the full `G_0`; correct and lower-variance. |
| Entropy bonus | "Encourage exploration" / 熵正则化 | `+β · H(π(·\|s))` term keeps the policy from collapsing. |
| On-policy | "Train on what you just saw" / 在线策略 | Gradient expectation is w.r.t. the current policy — cannot reuse old data directly. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = G(s, a) - V(s)`; the signed quantity REINFORCE-with-baseline multiplies. |

## Mais leitura 延伸阅读

- [Williams (1992). Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning](https://link.springer.com/article/10.1007/BF00992696) o papel original do REINFORCE.
- [Sutton et al. (2000). Policy Gradient Methods for Reinforcement Learning with Function Approximation](https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html) o teorema moderno da política-gradiente com aproximação de funções.
- [Sutton & Barto (2018). Ch. 13 — Policy Gradient Methods](http://incompleteideas.net/book/RLbook2020.pdf) apresentação de livros didáticos.
- [OpenAI Spinning Up — VPG / REINFORCE](https://spinningup.openai.com/en/latest/algorithms/vpg.html) Exposição pedagógica clara com código PyTorch.
- [Peters & Schaal (2008). Reinforcement Learning of Motor Skills with Policy Gradients](https://homes.cs.washington.edu/~todorov/courses/amath579/reading/PolicyGradient.pdf) A redução da variância e a visão natural-gradiente que liga a REINFORCE à família da região de confiança (TRPO, PPO).
