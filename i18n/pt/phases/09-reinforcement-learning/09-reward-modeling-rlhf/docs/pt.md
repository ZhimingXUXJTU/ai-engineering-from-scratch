# Reward Modeling & RLHF   Rewarding Construction & RLHF

> Os seres humanos não podem escrever uma função de recompensa para "boa resposta de assistente", mas eles podem comparar duas respostas e escolher a melhor. Ajuste um modelo de recompensa a essas comparações, então RL o modelo de linguagem contra ele.

> **【中文解读】**O grupo de pessoas não pode escrever funções de recompensa para um "bom assistente de resposta", mas pode comparar duas respostas de resposta melhores.

> **【拓展：RLHF 是大模型对齐的关键】**RLHF( baseado em humanos反的强化学习) 是ChatGPT成功的核心技术──三步流程:(1) 监督微调 SFT;(2) 训练奖励模型 RM;(3) 用PPO 优化 LM──DPO 简化第2-3步,但本质相同──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 05 (Sentiment), Phase 9 · 08 (PPO) | **前置知识:** Phase 5 · 05 (情感分析), Phase 9 · 08 (PPO)
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

Você treinou um modelo de linguagem no objetivo de previsão do próximo token. Ele escreve inglês gramatical. Também mente, vagueia e se recusa a recusar. Você não pode resolver isso com mais pré-treino.

> Você treinou o modelo de linguagem no próximo token 预测目标. Ele escreveu um gramática correta de Inglês. Mas também mentiria, correu questões, recusou, não recusou. Você não pode passar por mais treinamento para corrigir o texto da rede.

Você quer uma * recompensa escalária* que diga "resposta A é melhor do que resposta B para instrução X". Escrever essa função de recompensa à mão é impossível. "Helpfulness" não é uma expressão fechada sobre tokens. Mas os seres humanos podem comparar duas saídas e marcar uma preferência. Isso é barato para coletar em escala.

> Você quer um * valor de recompensa*, diz "para instrução X, responder A em comparação com B é melhor"―handwriting Esta função de recompensa é impossível―"utilidade" não é um token de expressão fechada , mas o ser humano pode comparar dois resultados e marcar preferências―, o que pode ser uma coleta em grande escala de baixo custo―.

RLHF (Christiano et al. 2017; Ouyang et al. 2022) converte as preferências em um modelo de recompensa, e então otimiza o LM através de PPO em relação a essa recompensa. Em três passos: SFT → RM → PPO. É a receita que enviou ChatGPT, Claude, Gemini e todos os outros alinhados-LLM em 20232025.

> RLHF vai se transformar em um modelo de recompensa, e depois passar por PPO para o LM para otimizar.

Em 2026, o passo PPO é substituído principalmente por DPO (Fase 10 · 08) porque é mais barato e quase tão bom para ajustar o alinhamento. Mas a peça do modelo de recompensa ainda está em base a cada amostragem Best-of-N, cada pipeline de recompensas RL-from-verifiable, e cada modelo de raciocínio usando um modelo de recompensa de processo.

> Em 2026 o PPO 步骤大多被DPO 替代,因为更便宜且对齐效果几乎相同――但*奖励模型* ainda é o melhor de N 采样器、可验证奖励 RL 管道和过程奖励模型的基础――理解RLHF 就理解整个对齐技术──

> **【中文解读】**RLHF 三阶段流程:(1) SFT supervisionar os modelos básicos em dados de demonstração humana;(2) RM utilizam a preferência humana para treinar Bradley-Terry 奖励模型;(3) PPO utilizam o modelo de recompensa para melhorar o seu sinal de linguagem, ao mesmo tempo que KL 惩罚 prevent deviance from SFT 太远── embora em 2026 os passos do PPO 多被 DPO 替代, mas o modelo de recompensa ainda é amplamente utilizado em cenários como o Best-of-N 采样、可验证奖励 RL、过程奖励模型等等──

> **【拓展：DPO 与 RLHF 的对比】**DPO(Direct Preference Optimization) vai transformar RM+PPO do RLHF 两步合并为一步 diretamente de preferência para estratégias de treinamento, sem necessidade de um modelo de recompensa de treinamento manifesto. Matematicamente, o valor é equivalente a estratégias de otimização sob o modelo Bradley-Terry.

## O conceito central.

![Three-stage RLHF: SFT, RM training on pairwise prefs, PPO with KL penalty](../assets/rlhf.svg)

**Stage 1: Supervised Fine-Tuning (SFT).**Comece a partir de um modelo base pré-treinado.`π_SFT`que é *biased towards good behavior* mas ainda tem um espaço de ação ilimitado.

> **阶段 1：监督微调（SFT）。**O modelo de comportamento é um modelo de comportamento orientado para o bom comportamento, mas ainda há um espaço de movimento ilimitado.`π_SFT`- Não.

**Stage 2: Reward Model training.**

- Coletar pares de respostas `(y_+, y_-)`- Não .`x`, etiquetado pelos seres humanos como "y_+ é preferido a y_-."
- Treinar um modelo de recompensa`R_φ(x, y)`para atribuir pontuações mais altas a `y_+`- Não .
- Perda: o **Bradley-Terry pairwise logistic**- Não .

  `L(φ) = -E[ log σ(R_φ(x, y_+) - R_φ(x, y_-)) ]`

  A diferença de recompensa implica um log-odds de preferência. BT tem sido o padrão desde 1952 (Bradley-Terry) e é a escolha dominante no RLHF moderno.

- `R_φ`O sistema de transformação é geralmente iniciado a partir do modelo SFT com uma cabeça escalar na parte superior.

> **阶段 2：奖励模型训练。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `(y_+, y_-)`, treinamento de recompensas`y_+`Mais alta... perdas são Bradley-Terry...`R_φ`Normalmente, a partir do modelo inicial SFT, adicione um padrão de saída.

**Stage 3: PPO against the RM with KL penalty.**

- Iniciar a política de formação `π_θ`de`π_SFT`Mantenha um "referência" congelada.`π_ref = π_SFT`- Não .
- Recompensa no final de uma resposta `y`- Não .

  `r_total(x, y) = R_φ(x, y) - β · KL(π_θ(·|x) || π_ref(·|x))`

  A penalidade do KL impede .`π_θ`de desviar arbitrariamente de `π_SFT` é um *regularizador*, não uma região de confiança difícil. `β`Normalmente`0.01`- Não .`0.05`- Não .
- Execute PPO (Lessão 08) com esta recompensa.

> **阶段 3：对 RM 做 PPO + KL 惩罚。**De`π_SFT`Iniciação de estratégias de treinamento. Recompensa = RM 分数 - β × KL 到参考策略.

**Why the KL?**Sem ele, o PPO encontrará com alegria estratégias de hacking de recompensas  o RM foi treinado apenas em conclusões dentro da distribuição.`π_θ`É o botão mais importante do RLHF.

> **为什么需要 KL？**Sem ele, a PPO encontraria estratégias de recompensa para os negros.`π_θ`保持在 RM 训练的流形附近── é a rotação mais importante no RLHF.

**2026 status:**

- **DPO**(Rafailov 2023): álgebra de forma fechada desintegra a Fase 2 + 3 em uma única perda supervisionada sobre dados de preferência. Não RM, não PPO. A mesma qualidade em benchmarks de alinhamento para uma fração da computação. Coberto na Fase 10 · 08.
- **GRPO**(DeepSeek 20242025): PPO com uma linha de base relativa ao grupo em vez de um crítico, recompensa de um *verificador* (codificação / correspondências matemáticas) em vez de um RM treinado pelo homem. Dominant para modelos de raciocínio.
- **Process reward models (PRMs):**soluções parciais de pontuação (cada etapa de raciocínio), utilizadas tanto nas variantes RLHF como GRPO para raciocínio.
- **Constitutional AI / RLAIF:**O programa de gestão de recursos humanos é um programa de gestão de recursos humanos que permite a criação de preferências em vez de de humanos.

> **2026 年状态：**DPO 将阶段 2+3 折叠为单一监督损失──GRPO 用组对基线替代评论,用验证器替代人类训练的 RM──PRM 评分部分解决方案──Constitutional AI / RLAIF 用对齐的 LLM 生成偏好──

## Construí-lo e realizei-o.
```figure
reward-model
```

## Construí-lo

Esta lição usa minúsculos "prompts" e "respostas" sintéticas representadas como cordas. O RM é um marcador linear sobre uma representação de saco de tokens.`code/main.py`- Não .

> Este curso usa sintetizados pequenos "pontos" e "repetências" de letras.

### Passo 1: dados de preferência sintéticos

```python
PROMPTS = ["help me", "answer me", "explain this"]
GOOD_WORDS = {"clear", "specific", "kind", "thorough"}
BAD_WORDS = {"vague", "rude", "wrong", "short"}

def make_pair(rng):
    x = rng.choice(PROMPTS)
    y_good = rng.choice(list(GOOD_WORDS)) + " " + rng.choice(list(GOOD_WORDS))
    y_bad = rng.choice(list(BAD_WORDS)) + " " + rng.choice(list(BAD_WORDS))
    return (x, y_good, y_bad)
```

Em RLHF real, esta é substituída por rotuladores humanos.`(prompt, preferred_response, rejected_response)` é idêntico.

> RLHF 中由人类标注者替代──形状`(提示, 偏好回复, 拒绝回复)`- É o mesmo.

### Passo 2: Modelo de recompensa Bradley-Terry

Resultados lineares: `R(x, y) = w · bag(y)`- Treinamento para minimizar a perda de log de BT em pares:

```python
def rm_train_step(w, x, y_pos, y_neg, lr):
    r_pos = dot(w, bag(y_pos))
    r_neg = dot(w, bag(y_neg))
    p = sigmoid(r_pos - r_neg)
    for tok, cnt in bag(y_pos).items():
        w[tok] += lr * (1 - p) * cnt
    for tok, cnt in bag(y_neg).items():
        w[tok] -= lr * (1 - p) * cnt
```

Depois de algumas centenas de atualizações,`w`atribui pesos positivos aos tokens de boas palavras e negativos aos maus.

> Depois de algumas centenas de atualizações,`w`给好词 token 分配正权重,坏词 分配负权重──

### Passo 3: Política de PPO em cima da RM

A nossa política de brinquedos produz um único token a partir de um vocabulário.`log π_θ(token | prompt)`, adicionar uma penalidade KL-to-referência, e aplicar o substituto de PPO cortado.

> Nossa estratégia de brinquedo gera um único token de uma palavra.`log π_θ(token | prompt)`Adicionar KL para a aplicação de medidas de punição, e aplicar cortes de PPO.

```python
def rlhf_step(theta, ref, w, prompt, rng, eps=0.2, beta=0.1, lr=0.05):
    logits_theta = policy_logits(theta, prompt)
    probs = softmax(logits_theta)
    token = sample(probs, rng)
    logits_ref = policy_logits(ref, prompt)
    probs_ref = softmax(logits_ref)
    reward = dot(w, bag([token])) - beta * kl(probs, probs_ref)
    # ppo-style update on theta, treating reward as the return
    ...
```

> 关键:奖励 = RM 分数 - β × KL(π_θ 1920 π_ref) ――β é controle estratégia漂移程度的关键超参数太大策略几乎不变,太小则奖励黑客开始──

### Passo 4: monitorar o KL

Mediana de pista`KL(π_θ || π_ref)`Se passar,`~5-10`A política tem desviado muito de `π_SFT` mais baixo `β`Este é o diagnóstico mais alto em real RLHF.

> Cada atualização segue a média.`KL(π_θ || π_ref)`Se exceder`~5-10`, estratégia já está longe`π_SFT`可能 β 正在降低或奖励黑客正在开始── é a mais importante diagnóstico na verdadeira RLHF──

### Passo 5: receita de produção com TRL

Uma vez que compreendemos o pipeline de brinquedos, aqui está o mesmo ciclo que um usuário de biblioteca real escreve.[TRL](https://huggingface.co/docs/trl)é a aplicação de referência  `RewardTrainer`para a fase 2 e `PPOTrainer`(com um KL-to-reference incorporado) para a fase 3.

> Uma vez que você entende o fluxo de água de brinquedo, aqui é o verdadeiro usuário da biblioteca escrever o mesmo ciclo de forma.`RewardTrainer`, fase 3 Utilizando`PPOTrainer`- Não.

```python
# Stage 2: reward model from pairwise preferences
from trl import RewardTrainer, RewardConfig
from transformers import AutoModelForSequenceClassification, AutoTokenizer

tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
rm = AutoModelForSequenceClassification.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct", num_labels=1
)

# dataset rows: {"prompt", "chosen", "rejected"} — Bradley-Terry format
trainer = RewardTrainer(
    model=rm,
    tokenizer=tok,
    train_dataset=preference_data,
    args=RewardConfig(output_dir="./rm", num_train_epochs=1, learning_rate=1e-5),
)
trainer.train()
```

```python
# Stage 3: PPO against the RM with KL penalty to the SFT reference
from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead

policy = AutoModelForCausalLMWithValueHead.from_pretrained("./sft-checkpoint")
ref    = AutoModelForCausalLMWithValueHead.from_pretrained("./sft-checkpoint")  # frozen

ppo = PPOTrainer(
    config=PPOConfig(learning_rate=1.41e-5, batch_size=64, init_kl_coef=0.05,
                     target_kl=6.0, adap_kl_ctrl=True),
    model=policy, ref_model=ref, tokenizer=tok,
)

for batch in dataloader:
    responses = ppo.generate(batch["query_ids"], max_new_tokens=128)
    rewards   = rm(torch.cat([batch["query_ids"], responses], dim=-1)).logits[:, 0]
    stats     = ppo.step(batch["query_ids"], responses, rewards)
    # stats includes: mean_kl, clip_frac, value_loss — the three PPO diagnostics
```

Três coisas que a biblioteca faz por ti.`adap_kl_ctrl=True`implementa o cronograma de adaptação-β: se a KL observada exceder `target_kl`O modelo de referência é congelado por convenção  não se podem compartilhar acidentalmente os parâmetros com `policy`E a cabeça de valor vive na mesma espinha dorsal que a política (`AutoModelForCausalLMWithValueHead`O TRL informa que o TRL não pode ser utilizado para a produção de produtos de qualidade.`policy/kl`E ...`value/loss`separadamente.

> Há três coisas que eu faço para ti.`adap_kl_ctrl=True`实现自适应 β 调度: se KL 超目标则 β 翻倍, se inferior a metade则 β 减半―― referência modelo de acordo com o acordo 结──值头和策略在同一主干上──

## Encurralagens

- **Over-optimization / reward hacking.**O RM é imperfeito .`π_θ`Os sintomas: recompensa sobe indefinidamente enquanto a avaliação humana pontuação planícies ou descontos.`β`, ampliar os dados de formação RM.
  **过度优化/奖励黑客。**RM não está perfeito;`π_θ`找到对抗性补全分高但质量差──症状: recompensa continua a subir mas o índice de avaliação humana está parado ou a cair──修复:早停、提高 β、扩展 RM 训练数据──
- **Length hacking.**Os RMs treinados em respostas úteis muitas vezes recompensam implícitamente a duração. A política aprende a encher as respostas. Remediação: recompensa normalizada em comprimento, ou RLAIF com uma RM consciente de comprimento.
  **长度黑客。**Em útil reapreciação no treinamento RM 常隐式奖励长度──策略学会填充回复──缓解:长度归归化奖励或长度感知 RM──
- **Too-small RM.**O RM tem de ser pelo menos tão grande quanto a política.
  **RM 太小。**RM pelo menos deve ser tão grande quanto a estratégia.
- **KL tuning.**O método de manipulação é um método de manipulação de dados que é utilizado para determinar o valor de um sistema de transferência de dados.
  **KL 调优。**β 太低→漂移和奖励黑客──β 太高→ estratégia quase não muda──标准技巧是*自适应* β 目标为固定 KL──
- **Preference-data noise.**- 30% das etiquetas humanas são barulhentas ou ambíguas.
  **偏好数据噪声。**Cerca de 30% dos rótulos humanos têm ruído ou confusão.
- **Off-policy problems.**Os dados de PPO são ligeiramente fora da política após a primeira época.
  **离策略问题。**O PPO dados na primeira época 后略离策略──像课08 那样监控裁剪比例──

## Use-o com o framework implementado.

O RLHF em 2026 é revestido:

> O RLHF de 2026 é de:

| Layer | Target | Method |
|-------|--------|--------|
| Layer / 层级 | Target / 目标 | Method / 方法 |
| Instruction following, helpfulness, harmlessness / 指令遵循、有用性、无害性 | Alignment / 对齐 | DPO (Phase 10 · 08) preferred over RLHF-PPO. |
| Reasoning correctness (math, code) / 推理正确性（数学、代码） | Capability / 能力 | GRPO with verifier reward (Phase 9 · 12). |
| Long-horizon multi-step tasks / 长视野多步任务 | Agentic / 代理 | PPO / GRPO with process reward models over steps. |
| Safety / refusal behavior / 安全/拒绝行为 | Safety / 安全 | RLHF-PPO with separate safety RM, or Constitutional AI. |
| Best-of-N at inference / 推理时 Best-of-N | Fast alignment / 快速对齐 | Use RM at decode time; no policy training needed. |
| Reward distillation / 奖励蒸馏 | Inference compute / 推理计算 | Train a small "reward head" on top of a frozen LM. |

O RLHF foi o método em 2022-2024. Em 2026, os canais de alinhamento de produção são DPO-primeiro, PPO-apenas para as etapas de RM-intensiva ou de segurança crítica.

> RLHF em 2022-2024 é um método central. Em 2026, a produção de linhas de fluxo de água em DPO é feita principalmente para a utilização de linhas de fluxo de água em RM.

## Envia-o . Produto .

Salva como`outputs/skill-rlhf-architect.md`- Não .

```markdown
---
name: rlhf-architect
description: Design an RLHF / DPO / GRPO alignment pipeline for a language model, including RM, KL, and data strategy.
version: 1.0.0
phase: 9
lesson: 9
tags: [rl, rlhf, alignment, llm]
---

Given a base LM, a target behavior (alignment / reasoning / refusal / agent), and a preference or verifier budget, output:

1. Stage. SFT? RM? DPO? GRPO? With justification.
2. Preference or verifier source. Humans, AI feedback, rule-based, unit-test-pass, or reward distillation.
3. KL strategy. Fixed β, adaptive β, or DPO (implicit KL).
4. Diagnostics. Mean KL, reward stability, over-optimization guard (holdout human eval).
5. Safety gate. Red-team set, refusal rate, safety RM separate from helpfulness RM.

Refuse to ship RLHF-PPO without a KL monitor. Refuse to use an RM smaller than the target policy. Refuse length-only rewards. Flag any pipeline that does not hold back a blind human-eval set as lacking over-optimization protection.
```

## Exercícios.

1. **Easy.**Treinar o modelo de recompensa Bradley-Terry em`code/main.py`Em 500 pares sintéticos de preferência, medir a precisão em pares em 100 pares de mão. Deve exceder 90%.
2. **Medium.**Execute o loop de brinquedo PPO-RLHF com `β ∈ {0.0, 0.1, 1.0}`Para cada um, o resultado da RM vs. KL-to-referência sobre as atualizações.
3. **Hard.**Implementar DPO (perda de probabilidade de preferência de forma fechada) sobre os mesmos dados de preferência e comparar com o pipeline RLHF-PPO em cálculo utilizado e pontuação final RM alcançada.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| RLHF | "Alignment RL" | Three-stage SFT + RM + PPO pipeline (Christiano 2017, Ouyang 2022). |
| Reward Model (RM) | "The scoring net" | Learned scalar function fit to pairwise preferences via Bradley-Terry. |
| Bradley-Terry | "Pairwise logistic loss" | `P(y_+ ≻ y_-) = σ(R(y_+) - R(y_-))`; the standard RM objective. |
| KL penalty | "Stay near the reference" | `β · KL(π_θ \|\| π_ref)` in the reward; the anti-reward-hacking regularizer. |
| Reward hacking | "Goodhart's law" | Policy exploits RM flaws; symptoms: reward up, human eval flat. |
| RLAIF | "AI-labeled preferences" | RLHF where labels come from another LM instead of humans. |
| PRM | "Process Reward Model" | Scores partial reasoning steps; used in reasoning pipelines. |
| Constitutional AI | "Anthropic's method" | AI-generated preferences guided by explicit rules. |

## Mais leitura 延伸阅读

- [Christiano et al. (2017). Deep Reinforcement Learning from Human Preferences](https://arxiv.org/abs/1706.03741)O jornal que iniciou a RLHF.
- [Ouyang et al. (2022). InstructGPT — Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) a receita por trás do ChatGPT.
- [Stiennon et al. (2020). Learning to summarize with human feedback](https://arxiv.org/abs/2009.01325) RLHF anterior para resumo.
- [Rafailov et al. (2023). Direct Preference Optimization](https://arxiv.org/abs/2305.18290) DPO; o padrão pós-RLHF em 2026.
- [Bai et al. (2022). Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) RLAIF e ciclo de autocrítica.
- [Anthropic RLHF paper (Bai et al. 2022). Training a Helpful and Harmless Assistant](https://arxiv.org/abs/2204.05862)O papel da HH.
- [Hugging Face TRL library](https://huggingface.co/docs/trl) produção `RewardTrainer`E ...`PPOTrainer`Leia a fonte do treinador para os detalhes de KL adaptativo e de valor.
- [Hugging Face — Illustrating Reinforcement Learning from Human Feedback](https://huggingface.co/blog/rlhf)por Lambert, Castricato, von Werra, Havrilla  o caminhão canônico do oleoduto de três etapas com diagramas.
- [von Werra et al. (2020). TRL: Transformer Reinforcement Learning](https://github.com/huggingface/trl) a biblioteca; `examples/`tem end-to-end RLHF scripts para Llama, Mistral e Qwen.
- [Sutton & Barto (2018). Ch. 17.4 — Designing Reward Signals](http://incompleteideas.net/book/RLbook2020.pdf) a visão da hipótese de recompensa; pré-requisito essencial para pensar no hacking de recompensa.
