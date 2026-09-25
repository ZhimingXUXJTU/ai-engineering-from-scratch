# Otimizar a política próxima (PPO)

> A A2C descarta cada implementação após uma atualização. O PPO envolve o gradiente da política em uma relação de importância reduzida para que você possa fazer 10+ épocas nos mesmos dados sem a política explodir. Schulman et al. (2017). Ainda o algoritmo padrão de gradiente da política em 2026.

> **【中文解读】**O PPO utilizou a taxa de importância de corte para envolver a gradiência da estratégia, permitindo que os mesmos dados possam ser atualizados em mais de 10 rotas e a estratégia não explode.

> **【拓展：PPO 与 ChatGPT】**O PPO é o algoritmo central do treinamento do ChatGPT RLHF. InstruGPT(2022) Usando o PPO para fazer preferências humanas ao GPT-3, é a tecnologia por trás do ChatGPT. A estabilidade e simplicidade do PPO tornou-se a primeira escolha do setor.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic) | **前置知识:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic)
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

A2C (Lessão 07) é sobre política: o gradiente `E_{π_θ}[A · ∇ log π_θ]`requer dados recolhidos a partir da * corrente* `π_θ`- Faça uma atualização e...`π_θ`Os dados que usou agora estão fora da política.

> A2C ((Lessão 07) é a linha estratégica de:梯度 `E_{π_θ}[A · ∇ log π_θ]`要求从*当前* `π_θ`采样数据──一次更新后 `π_θ`改变; os dados que usaste se tornaram estratégias.

As implementações são caras. Na Atari, uma implementação em 8 envs × 128 passos = 1024 transições e uma dúzia de segundos de tempo ambiental.

> Rollout  muito caro. Em Atari, 8 环境 × 128 步 = 1024 vezes transferência e 10 segundos de tempo ambiental.

A Primeira solução foi a otimização das políticas de região de confiança (TRPO, Schulman 2015): restringir cada atualização para que a divergência entre as políticas antigas e novas permaneça abaixo `δ`Teoricamente limpo, mas requer uma solução conjugada-gradiente por atualização.

> O TRPO, Schulman 2015) é o primeiro revisão:`δ`A teoria é que a tecnologia é muito boa, mas cada atualização precisa de uma solução mais rápida.

O PPO (Schulman et al. 2017) substitui a restrição de região de confiança dura por um objetivo simples. Uma linha extra de código. Dez épocas por implantação. Nenhum gradiente conjugado. Garantias teóricas boas o suficiente. Nove anos depois, ainda é o algoritmo padrão de política-gradiente para tudo, desde MuJoCo até RLHF.

> PPO(Schulman 等人 2017) usando simples cortes de objetivos substituir o hard faith domain.

> **【中文解读】**Inovação central do PPO: Usar o corte objetivo substituir o TRPO de dura约束―― importância percentuale r_t(theta) = pi_theta / pi_old 被剪到 [1-epsilon, 1+epsilon] 范围内── quando o benefício A_t>0 时,不将好动作的概率推得太高; quando A_t<0 时,不将坏动作的概率降低太低──需要一行代码,就能安全地多次复制同一批数据──

> **【拓展：PPO 之外的选择——DPO 与 GRPO】**Embora o PPO ainda seja uma escolha padrão em 2026, o seu alternativo está a surgir.

## O conceito central.

![PPO clipped surrogate objective: ratio clipping at 1 ± ε](../assets/ppo.svg)

**The importance ratio.**

`r_t(θ) = π_θ(a_t | s_t) / π_{θ_old}(a_t | s_t)`

Esta é a relação de probabilidade entre a nova política e a política que recolheu os dados. `r_t = 1`Não significa nenhuma mudança.`r_t = 2`significa que a nova política é duas vezes mais provável que`a_t`Como os antigos.

> **重要性比率。**A nova estratégia e a estratégia de coleta de dados são muito parecidas.`r_t = 1`Não há mudança.`r_t = 2`Expressão de novas estratégias`a_t`A probabilidade é duas vezes maior do que a estratégia antiga.

**The clipped surrogate.**

`L^{CLIP}(θ) = E_t [ min( r_t(θ) A_t, clip(r_t(θ), 1-ε, 1+ε) A_t ) ]`

Dois termos:

- Se a vantagem `A_t > 0`E a proporção tenta crescer para além.`1 + ε`, o clip aplania a gradiente  não empurrar uma boa ação mais longe do que `+ε`acima da velha probabilidade.
- Se a vantagem `A_t < 0`E a proporção tenta crescer para além.`1 - ε`(o que significa que faríamos uma ação ruim mais provável em comparação com a sua redução cortada), o clip caps a gradiente  não empurrar uma ação ruim abaixo `-ε`- Não .

O `min`O que é que se passa? - Não, não.

Tipico .`ε = 0.2`. Descrever o objectivo como uma função de `r_t`A função linear de pedaço com um telhado plano no "lado bom" e um piso plano no "lado ruim".

> **裁剪代理。**两项: Se a vantagem for positiva e a taxa exceder `1 + ε`Não faça o melhor que a probabilidade anterior .`+ε`更多── se a vantagem for negativa e a taxa é inferior a `1 - ε`Não reduzir a má conduta.`-ε`更多── típico `ε = 0.2`- Não.

> **【中文解读】**Intuição do mecanismo de corte de PPO:epsilon=0.2 significa que a estratégia muda o máximo de 20% por atualização. Se um movimento for bom, a probabilidade aumentará o máximo de 20%; se um movimento for ruim, a probabilidade diminuirá o máximo de 20%. Isso evita que o "negligência catastrófica" não mude muito.

**The full PPO loss.**

`L(θ, φ) = L^{CLIP}(θ) - c_v · (V_φ(s_t) - V_t^{target})² + c_e · H(π_θ(·|s_t))`

A mesma estrutura de actores-críticos que A2C. Três coeficientes, geralmente `c_v = 0.5`- Não .`c_e = 0.01`- Não .`ε = 0.2`- Não .

> **完整的 PPO 损失。**Comparado com A2C, Actor-Critic 結構──三系数, normalmente `c_v = 0.5`- Não.`c_e = 0.01`- Não.`ε = 0.2`- Não.

**The training loop.**

1. Coletar`N × T`Transições transversais `N`Envistas paralelas para `T`Cada passo.
2. Calcule vantagens (GAE), congelem-nas como constantes.
3. Congelando .`π_{θ_old}`como um instantâneo de corrente `π_θ`- Não .
4. Para o`K`Epoca, para cada minipartida de `(s, a, A, V_target, log π_old(a|s))`- Não .
   - Computação`r_t(θ) = exp(log π_θ(a|s) - log π_old(a|s))`- Não .
   - Aplicar`L^{CLIP}`+ perda de valor + entropia.
   - Passo gradual.
5. Descarte o lançamento, volte ao primeiro passo.

`K = 10`O PPO é robusto: os números exatos raramente importam dentro de ±50%.

> **训练循环。**收集 → 计算 GAE 优势 → 结旧策略 → K 轮更新 → 丢弃数据──`K = 10`O número de unidades de 64 é muito grande.

**KL-penalty variant.**O artigo original propôs uma alternativa que utilizasse uma penalidade KL adaptativa: `L = L^{PG} - β · KL(π_θ || π_old)`com`β`A versão de corte tornou-se dominante; a variante KL sobrevive no RLHF (onde KL à política de referência é uma restrição separada que você sempre quer de qualquer maneira).

> **KL 惩罚变体。**O artigo original propôs uma alternativa ao uso de auto-adaptação KL 惩罚.

## Construí-lo e realizei-o.
```figure
ppo-clip
```

## Construí-lo

### Passo 1: Captura`log π_old(a | s)`no momento da implantação

```python
for step in range(T):
    probs = softmax(logits(theta, state_features(s)))
    a = sample(probs, rng)
    s_next, r, done = env.step(s, a)
    buffer.append({
        "s": s, "a": a, "r": r, "done": done,
        "v_old": value(w, state_features(s)),
        "log_pi_old": log(probs[a] + 1e-12),
    })
    s = s_next
```

A imagem é tirada uma vez, no momento da implantação.

> 快照在 rollout 时拍摄一次──在更新时代 期间不变──

### Passo 2: calcular as vantagens do GAE (Lessão 07)

A mesma coisa que o A2C. Normaliza-se ao longo do lote.

> Com A2C, comparativamente.

### Passo 3: atualização de substituição cortada

```python
for _ in range(K_EPOCHS):
    for mb in minibatches(buffer, size=64):
        for rec in mb:
            x = state_features(rec["s"])
            probs = softmax(logits(theta, x))
            logp = log(probs[rec["a"]] + 1e-12)
            ratio = exp(logp - rec["log_pi_old"])
            adv = rec["advantage"]
            surrogate = min(
                ratio * adv,
                clamp(ratio, 1 - EPS, 1 + EPS) * adv,
            )
            # backprop -surrogate, add value loss, subtract entropy
            grad_logpi = onehot(rec["a"]) - probs
            if (adv > 0 and ratio >= 1 + EPS) or (adv < 0 and ratio <= 1 - EPS):
                pg_grad = 0.0  # clipped
            else:
                pg_grad = ratio * adv
            for i in range(N_ACTIONS):
                for j in range(N_FEAT):
                    theta[i][j] += LR * pg_grad * grad_logpi[i] * x[j]
```

O padrão de "gradiente de corte → zero" é o coração da PPO. Se a nova política já se desviou muito longe na direcção benéfica, a atualização pára.

> O modelo "corte → 零梯度" é o núcleo do PPO. Se uma nova estratégia se desviou muito longe na direção favorável, a actualização acaba.

### Passo 4: valor e entropia

Adicionar MSE padrão ao alvo crítico e um bônus de entropia no ator, igual ao A2C.

> Para o crítico objectivo adicionar padrão MSE, para o ator 添加奖励, com A2C

### Passo 5: diagnóstico

Três coisas para ver em cada atualização:

> Cada atualização tem três coisas a monitorar:

- **Mean KL** `E[log π_old - log π_θ]`Devia ficar dentro .`[0, 0.02]`Se passar por aí .`0.1`, reduzir`K_EPOCHS`ou `LR`- Não .
  **平均 KL。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `[0, 0.02]`Se exceder`0.1`, reduzir `K_EPOCHS`Ou `LR`- Não.
- **Clip fraction** a fracção das amostras cuja proporção se encontra fora `[1-ε, 1+ε]`Devia ser .`~0.1-0.3`Se ...`~0`, o clip nunca desencadeia → aumento `LR`ou `K_EPOCHS`Se ...`~0.5+`, você está super-ajustando a implantação → baixá-los.
  **裁剪比例。**Preço de exclusão`[1-ε, 1+ε]`de proporção de`~0.1-0.3`- Não.
- **Explained variance** `1 - Var(V_target - V_pred) / Var(V_target)`Metrica de qualidade crítica. Deve subir para 1.
  **解释方差。**Critical Quality Index── deve acompanhar a tendência de aprendizagem crítica 1──

## Encurralagens

- **Clip coefficient mistuned.** `ε = 0.2`É o padrão de facto.`0.1`torna as atualizações demasiado tímidas; `0.3+`Invita a instabilidade.
  **裁剪系数调错。** `ε = 0.2`É um facto.`0.1`太保守;`0.3+`导致不稳定──
- **Too many epochs.** `K > 20`O sistema de segurança social é um dos principais factores de destabilização da política social.`π_old`- Epoca de limite, especialmente para grandes redes.
  **太多 epoch。** `K > 20` Sempre está instável, porque a estratégia está desviada `π_old`Muito longe. Limitar a época, especialmente a grande rede.
- **No reward normalization.**Grandes escalas de recompensa se alimentam na faixa de clip. Normalize recompensas (exercício std) antes de vantagens computacionais.
  **没有奖励归一化。**Grande recompensa medida erosion corte alcance.
- **Forgetting advantage normalization.**A normalização de média zero/unit-std por lote é padrão.
  **忘记优势归一化。**Cada lote de valores mínimos/unidades de padrão é padrão.
- **Learning rate not decayed.**O PPO beneficia da decadência do LR linear para zero.
  **学习率未衰减。**PPO de LR linear  decadência a zero                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
- **Importance ratio math errors.**Sempre .`exp(log_new - log_old)`para estabilidade numérica, não `new / old`- Não .
  **重要性比率数学错误。**始终使用 `exp(log_new - log_old)`Garantia de estabilidade numérica, e não `new / old`- Não.
- **Wrong gradient sign.**Maximizar a substitutória = *minimizar* `-L^{CLIP}`Um sinal invertido é o bug mais comum de PPO.
  **梯度符号错误。**Máximação de agente = * minimizar* `-L^{CLIP}`◊ 符号反转为 PPO 最常见 bug──

## Use-o com o framework implementado.

O PPO é o algoritmo RL padrão de 2026 em um número surpreendente de domínios:

> O PPO é um algoritmo de RL de 2026 em muitos domínios:

| Use case | PPO variant |
|----------|-------------|
| Use case / 用例 | PPO variant / PPO 变体 |
| MuJoCo / robotics control / MuJoCo/机器人控制 | PPO with Gaussian policy, GAE(0.95) / 高斯策略的 PPO，GAE(0.95) |
| Atari / discrete games / Atari/离散游戏 | PPO with categorical policy, rolling 128-step rollouts / 分类策略的 PPO |
| RLHF for LLMs / LLM 的 RLHF | PPO with KL penalty to reference model, reward from RM at end of response / 带 KL 惩罚的 PPO |
| Large-scale game agents / 大规模游戏 Agent | IMPALA + PPO (AlphaStar, OpenAI Five) |
| Reasoning LLMs / 推理 LLM | GRPO (Lesson 12) — PPO variant without critic / 无 Critic 的 PPO 变体 |
| Preference-only data / 仅偏好数据 | DPO — closed-form collapsing of PPO+KL, no online sampling / 闭式 PPO+KL 折叠 |

A forma de perda de PPO *  substituto cortado + valor + entropia  é o andamio para DPO, GRPO e quase todos os oleodutos RLHF.

> O PPO de forma de perda é o DPO, o GRPO e quase todos os RLHF 流水线的脚手架──

## Envia-o . Produto .

Salva como`outputs/skill-ppo-trainer.md`- Não .

```markdown
---
name: ppo-trainer
description: Produce a PPO training config and a diagnostic plan for a given environment.
version: 1.0.0
phase: 9
lesson: 8
tags: [rl, ppo, policy-gradient]
---

Given an environment and training budget, output:

1. Rollout size. `N` envs × `T` steps.
2. Update schedule. `K` epochs, minibatch size, LR schedule.
3. Surrogate params. `ε` (clip), `c_v`, `c_e`, advantage normalization on.
4. Advantage. GAE(`λ`) with explicit `γ` and `λ`.
5. Diagnostics plan. KL, clip fraction, explained variance thresholds with alerts.

Refuse `K > 30` or `ε > 0.3` (unsafe trust region). Refuse any PPO run without advantage normalization or KL/clip monitoring. Flag clip fraction sustained above 0.4 as drift.
```

## Exercícios.

1. **Easy.**Execute PPO em 4×4 GridWorld com `ε=0.2, K=4`- Compare a eficiência da amostra com A2C (uma época por implantação) em etapas de ambiente correspondentes.
2. **Medium.**Esvaziar`K ∈ {1, 4, 10, 30}`- Retorno de trama versus passos de env e seguimento média KL por atualização.`K`O KL explode nesta tarefa?
3. **Hard.**Substitua a substitutora cortada por uma penalidade KL adaptativa (`β`duplicado se `KL > 2·target`, reduzida à metade se `KL < target/2`) Compare o retorno final, estabilidade e livre de clipes.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Importance ratio | "r_t(θ)" | `π_θ(a\|s) / π_old(a\|s)`; deviation from the policy that collected the data. |
| Clipped surrogate | "PPO's main trick" | `min(r·A, clip(r, 1-ε, 1+ε)·A)`; flat gradient past the clip on beneficial side. |
| Trust region | "TRPO / PPO intent" | Limit each update's KL to guarantee monotone improvement. |
| KL penalty | "Soft trust region" | Alternative PPO: `L - β · KL(π_θ \|\| π_old)`. Adaptive `β`. |
| Clip fraction | "How often clipping triggers" | Diagnostic — should be 0.1-0.3; outside means mistuned. |
| Multi-epoch training | "Data reuse" | K epochs on each rollout; variance cost traded for sample efficiency. |
| On-policy-ish | "Mostly on-policy" | PPO is nominally on-policy but K>1 epochs uses slightly-off-policy data safely. |
| PPO-KL | "The other PPO" | KL-penalty variant; used in RLHF where KL-to-reference is already a constraint. |

## Mais leitura 延伸阅读

- [Schulman et al. (2017). Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)- O jornal.
- [Schulman et al. (2015). Trust Region Policy Optimization](https://arxiv.org/abs/1502.05477)TRPO, o antecessor da PPO.
- [Andrychowicz et al. (2021). What Matters In On-Policy RL? A Large-Scale Empirical Study](https://arxiv.org/abs/2006.05990) todos os hiperparâmetros de PPO foram eliminados.
- [Ouyang et al. (2022). Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) InstructGPT; a receita de PPO-in-RLHF.
- [OpenAI Spinning Up — PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html)- Exposição moderna limpa com PyTorch.
- [CleanRL PPO implementation](https://github.com/vwxyzjn/cleanrl) Referência de PPO de um único arquivo utilizado por muitos documentos.
- [Hugging Face TRL — PPOTrainer](https://huggingface.co/docs/trl/main/en/ppo_trainer) a receita de produção para o PPO em modelos de linguagem; ler junto à lição 09 (RLHF).
- [Engstrom et al. (2020). Implementation Matters in Deep Policy Gradients](https://arxiv.org/abs/2005.12729) o artigo "37 optimizações de nível de código"; quais os truques de PPO são carregáveis e quais são folclores.
