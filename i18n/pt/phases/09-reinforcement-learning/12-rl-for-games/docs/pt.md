# RL para jogos  AlphaZero, MuZero, e a era do LLM-Razonamento  game中的强化学习  AlphaZero、 MuZero e LLM 推理时代

> 1992: TD-Gammon venceu campeões humanos no backgammon com TD puro. 2016: AlphaGo venceu Lee Sedol. 2017: AlphaZero dominou xadrez, shogi e Go a partir do zero. 2024: DeepSeek-R1 provou a mesma receita, com o GRPO substituindo o PPO, trabalha no raciocínio.

> **【中文解读】**游戏是 RL 突破的试验场:TD-Gammon (1992) → AlphaGo (2016) → AlphaZero (2017) → DeepSeek-R1 (2025)。DeepSeek-R1 证明了 AlphaZero's"self-blowing+search+strategy improvement" loop can be directly used for large model's mathematical reasoningtoken 就是动作,验证器就是"win/输"信号──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 05 (DQN), Phase 9 · 08 (PPO), Phase 9 · 09 (RLHF), Phase 9 · 10 (MARL) | **前置知识:** Phase 9 · 05 (DQN), Phase 9 · 08 (PPO), Phase 9 · 09 (RLHF), Phase 9 · 10 (多智能体 RL)
**Time:** ~120 minutes | **时间:** ~120 分钟

## O problema é o problema da introdução

Os jogos têm tudo o que RL quer. recompensa limpa (ganho/perda). Episódios infinitos (auto- jogação reset). Simulação perfeita (o jogo *é* o simulador). Espaços de ação contínuos discretos ou pequenos. Estrutura multi-agente que força robustez adversária.

> O jogo tem RL necessário todo o seu tempo. O jogo tem RL necessário todo o seu tempo.

E os jogos são como cada grande avanço RL foi testado. TD-Gammon (backgammon, 1992). Atari-DQN (2013). AlphaGo (2016). AlphaZero (2017). OpenAI Five (Dota 2, 2019). AlphaStar (StarCraft II, 2019). MuZero (modelo aprendido, 2019). AlphaTensor (multiplicação de matriz, 2022). AlphaDev (algoritmos de classificação, 2023). DeepSeek-R1 (razão matemática, 2025)  a mais recente demonstração de que as técnicas de jogo-RL funcionam no texto.

> 游戏是每个 RL 重大突破的试验场──TD-Gammon(西洋双陆棋,1992)、Atari-DQN(2013)、AlphaGo(2016)、AlphaZero(2017)、OpenAI Five(Dota 2,2019)、AlphaStar(星际争 II,2019)、MuZero(学习模型,2019)、AlphaTensor(矩阵乘法,2022)、AlphaDev(排序算法,2023)、DeepSeek-R1(数学推理,2025)最新证据:游戏RL 技术可用于文本──

Esta pedra angular analisa as três arquiteturas emblemáticas  AlphaZero, MuZero e GRPO  através de uma única lente unificadora: **self-play + search + policy improvement**Cada um generaliza o anterior; GRPO em particular é a receita do AlphaZero aplicada ao raciocínio LLM, com tokens como ações e verificação matemática como sinal de vitória.

> Esse é o final através de um único ponto de vista.**自我博弈+搜索+策略改进**审视三个里程碑架构:AlphaZero、MuZero 和 GRPO── cada um é uma promoção anterior; GRPO 特别是将 AlphaZero 配方应用于 LLM 推理,token 是动作,数学验证 是胜信号──

## O conceito central.

![AlphaZero ↔ MuZero ↔ GRPO: same loop, different environments](../assets/rl-games.svg)

**The unifying loop.**

```
while True:
    trajectory = self_play(current_policy, search)     # play game against self
    policy_target = search.improved_policy(trajectory) # search improves raw policy
    policy_net.update(policy_target, value_target)     # supervised on search output
```

**AlphaZero (2017).**Silver et al. Dado um jogo (chaque, shogi, Go) com regras conhecidas:

- Rede de valor político: uma torre `f_θ(s) → (p, v)`- Não .`p`É um antecessor sobre movimentos legais.`v`é o resultado esperado do jogo.
- Monte Carlo Tree Search (MCTS): a cada movimento, expandir uma árvore de possíveis continuas.`(p, v)`como o anterior + bootstrap. Selecione nós por UCB (PUCT): `a* = argmax Q(s, a) + c · p(a|s) · √N(s) / (1 + N(s, a))`- Não .
- Jogar jogos de agente contra agente.`t`, a distribuição das visitas do MCTS `π_t`torna-se o objectivo da formação política.
- Perda: `L = (v - z)² - π · log p + c · ||θ||²`- Não .`z`é o resultado do jogo (+1 / 0 / -1).

Zero conhecimento humano, zero heurísticas artesanais, uma única receita que dominava xadrez, shogi e go depois de algumas dezenas de milhões de jogos de auto-jogo.

> O mundo de jogo de xadrez, de xadrez e de golfe, foi dominado por milhares de milhões de pessoas.

**MuZero (2019).**Schrittwieser et al. Elimina o requisito de que as regras sejam conhecidas.

- Em vez de um ambiente fixo, aprenda um modelo de dinâmica latente.`(h, g, f)`- Não .
  - `h(s)`: codificar a observação em estado latente.
  - `g(s_latent, a)`: prever o próximo estado latente + recompensa.
  - `f(s_latent)`: previsão de prioridade política + valor.
- O MCTS funciona no espaço latente aprendido.
- Funciona no Go, xadrez, shogi e Atari, um algoritmo, sem conhecimento de regras.

> Nação de jogo, jogo, jogo e Atari, é um algoritmo, sem necessidade de regras.

> **【中文解读】**O ciclo central de AlphaZero e MuZero: AutoBlog+ Search+ Strategy Improvement iniciou diretamente o treinamento de raciocínio do DeepSeek-R1 com recompensas verificáveis para substituir o jogo negativo.

> **【拓展：DeepSeek-R1 与 AlphaZero 范式】**DeepSeek-R1(2025) vai aplicar o paradigma do AlphaZero para LLM 推理:token就是动作,推理过程就是"游戏",验证器(Mathematics题对错、代码是否通过测试)就是"胜负信号"──GRPO 替代PPO,组内采样替代自我博──

**Stochastic MuZero (2022).**Adiciona dinâmica estocástica e nós de sorte; se estende aos jogos de classe backgammon.

> **随机 MuZero (2022)。**添加随机动力学和机会节点; expandir para jogos de jogos de azar

**Muesli, Gumbel MuZero (2022-2024).**Melhorias na eficiência da amostra e na procura determinista.

> **Muesli、Gumbel MuZero (2022-2024)。** melhoria da procura de amostras e de determinação

**GRPO (2024-2025).**A mesma faixa em forma de AlphaZero, aplicada ao raciocínio do modelo de linguagem:

- "Game": responder a um problema de matemática / codificação / raciocínio. "Win" = verificador (passagens de teste, correspondências numéricas de respostas) retorna 1.
- Política: o LLM. Ações: tokens. Estado: prompt + response-so far.
- Não há crítico (V_φ estilo PPO).`G`- A política de pagamento é de um valor de R$ 5 milhões.**group-relative advantage** `A_i = (r_i - mean_r) / std_r`como sinal para atualização no estilo REINFORCE.
- A política de referência de KL para evitar a deriva (como a RLHF).
- Perda total:

  `L_GRPO(θ) = -E_{q, {o_i}} [ (1/G) Σ_i A_i · log π_θ(o_i | q) ] + β · KL(π_θ || π_ref)`

Não há modelo de recompensa, não há crítico, não há MCTS. A linha de base relativa ao grupo substitui as três.

> **GRPO (2024-2025)。**DeepSeek-R1 配方── igual AlphaZero 形状循环, aplicado para modelos linguísticos 推理:不需要奖励模型、Critic 或 MCTS──组相对基线替代了三者──在推理基准上匹配或超越 PPO-RLHF 质量,计算量仅为一小部分──

> **【中文解读】**GRPO é a inovação central do DeepSeek-R1: não precisa de crítico 网络(省一半内存), utilizando o valor médio e o diferencial de construção de grupos.

> **【拓展：GRPO→DeepSeek-R1→开源推理革命】**DeepSeek-R1 quatro fases de treinamento: Cold start SFT → 推理导向 GRPO → 拒采样+SFT → 全谱 GRPO──R1-Zero(pure GRPO 无 SFT) provou LLM pode ser do zero学会推理, mas emitir leitura diferença──蒸 Experimento mostra: usar forte RL do professor de sugestão de trilha para fazer SFT, em comparação com um pequeno modelo de fazer RL 效果更好──

**The R1 recipe in full.**DeepSeek-R1 (DeepSeek 2025) é um dos dois modelos de um único documento:

> **R1 完整配方。**DeepSeek-R1 é um dos dois modelos do artigo:

- **R1-Zero.**Comece com o modelo base DeepSeek-V3. Não há SFT. Aplique GRPO diretamente com dois componentes de recompensa: * recompensa de precisão * (baseada em regras  fez a resposta final analisar o número correto / o código passou testes de unidade) e * recompensa de formato * (a conclusão envolveu sua cadeia de pensamento em `<think>…</think>`tags). Ao longo de milhares de passos, o comprimento médio da resposta aumenta de ~100 para ~10,000 tokens e as pontuações de referência matemática subem para níveis de pré-visualização próximos a o1. O modelo aprende a raciocinar a partir do zero. A desvantagem: suas cadeias de pensamento são muitas vezes ilegíveis, misturam línguas e não têm poluição estilística.
- **R1.**Corrigir os problemas de legibilidade do R1-Zero com um gasoduto de quatro etapas:
  1. **Cold-start SFT.**Coletar alguns milhares de demonstrações longas de CoT com formato limpo, supervisionar-finetunar o modelo base sobre eles.
  2. **Reasoning-oriented GRPO.**Aplicar o GRPO com as recompensas de precisão+formato mais uma recompensa de *consistência linguística* para evitar a troca de código.
  3. **Rejection sampling + SFT round 2.**Amostre ~ 600K trajetórias de raciocínio do ponto de controle RL, mantenha apenas aquelas com respostas finais corretas e CoT legível, e combine com ~ 200K exemplos de SFT não raciocínio (escritura, QA, auto-conhecimento).
  4. **Full-spectrum GRPO.**Mais uma rodada de RL que abrange o raciocínio (recompensas baseadas em regras) e o alinhamento geral (recompensas baseadas em preferências de utilidade/inharmonia).

O resultado corresponde ao o1 em AIME e MATH-500 em pesos abertos, e é pequeno o suficiente para destilar. O mesmo artigo também libera seis modelos densos destilados (Qwen-1.5B até Llama-70B) por SFT'ing em rastros de raciocínio de R1  nenhum RL no aluno.

> Resultados em AIME e MATH-500 上匹配 o1,且足足足小可以蒸──蒸强 RL

**Why GRPO instead of PPO for reasoning.**Três razões no artigo DeepSeekMath (Feb 2024): (1) nenhuma rede de valor para treinar, reduzindo a memória pela metade; (2) a linha de base do grupo naturalmente lida com a recompensa de final de trajetória que as tarefas de raciocínio produzem; (3) a normalização por instante torna vantagens comparáveis em problemas de dificuldade muito diferentes, o que o único crítico do PPO não pode.

> **为什么推理用 GRPO 而非 PPO。**Três razões: 1) 无需训练值网络,内存减半; 2) 组基线自然处理推理任务产生的稀疏回合末奖励; 3) Cada dica de reúnização faz com que a vantagem em dificuldade diferença enorme entre problemas entre comparação:

**Search-free vs search-based.**Os jogos se ramificaram:

> **Search-free vs search-based.**

- *Jogos de informação perfeita com horizontes longos* (Go, xadrez): ainda baseados em pesquisas.
- * Raciocínio LLM*: ainda não há MCTS em produção; GRPO em implantações completas, melhor de N para computação de inferência.

## Construí-lo e realizei-o.
```figure
f3-selfplay-ladder
```

## Construí-lo

O código está em `code/main.py`Implementos **GRPO in miniature**O algoritmo é o mesmo que num LLM; apenas a política e o ambiente são mais simples. Ensinam a *perda* e a *vantagem relativa ao grupo*, que é a inovação de 2025.

> `code/main.py`Cód do meio implementado**微型 GRPO** um algoritmo com um grupo de amostras 博机── é o mesmo que o LLM; apenas estratégia e ambiente mais simples── é professor* perda* e* grupo em relação a vantagens*, é uma inovação para 2025──

### Passo 1: um ambiente de verificação pequeno

```python
QUESTIONS = [
    {"prompt": "q1", "correct": 3},
    {"prompt": "q2", "correct": 1},
]

def verify(prompt_idx, answer_token):
    return 1.0 if answer_token == QUESTIONS[prompt_idx]["correct"] else 0.0
```

No GRPO real, o verificador executa testes unitários ou verifica a igualdade matemática.

> Verdadeiro GRPO 中验证器运行单元测试或检查数学等式──

### Passo 2: política: softmax sobre K tokens de resposta por pedido

```python
def policy_probs(theta, p_idx):
    return softmax(theta[p_idx])
```

Equivalente à saída final de uma MLL condicionada a um pedido.

> Para o LLM, é necessário um nível de produção de um nível final.

### Passo 3: amostragem de grupo e vantagem relativa ao grupo

```python
def grpo_step(theta, p_idx, G=8, beta=0.01, lr=0.1, rng=None):
    probs = policy_probs(theta, p_idx)
    samples = [sample(probs, rng) for _ in range(G)]
    rewards = [verify(p_idx, s) for s in samples]
    mean_r = sum(rewards) / G
    std_r = stddev(rewards) + 1e-8
    advs = [(r - mean_r) / std_r for r in rewards]

    for a, A in zip(samples, advs):
        grad = onehot(a) - probs
        for i in range(len(probs)):
            theta[p_idx][i] += lr * A * grad[i]
    # KL penalty: pull theta toward reference
    for i in range(len(probs)):
        theta[p_idx][i] -= beta * (theta[p_idx][i] - reference[p_idx][i])
```

A vantagem relativa ao grupo é o truque DeepSeek 2024. Não é necessário crítico. A "linha de base" é a média do grupo, e a normalização usa o grupo std.

> 组相对优势是2024年DeepSeek的技巧──无需批判──"基线"是组平均值,归结使用组标准差──

### Passo 4: comparação com a linha de base de REINFORCE (sem valor)

A mesma configuração, o mesmo cálculo, simples reforço.

> Paralelamente, a mesma quantidade de cálculo, pura REINFORCE, GRPO, recebendo mais rapidez e estabilidade.

### Passo 5: observar a entropia e KL

Os mesmos diagnósticos que o RLHF: KL para referência, entropia política, recompensa-over-time.

> Compatível com RLHF: diagnóstico: KL médio até referência estratégia, estratégia, recompensa com o tempo de mudança.

## Encurralagens

- **Reward hacking via verifier gaming.**O GRPO herda o risco da RLHF: se o verificador for errado ou explorável, o MLL encontrará o explorador.
  **通过验证器博弈的奖励黑客。**GRPO  herdou o risco de RLHF: se o verificador errar ou ser utilizável, LLM encontrará uma falha.
- **Group size too small.**A variação da linha de base do grupo é a seguinte:`1/√G`- Abaixo .`G = 4`, o sinal de vantagem é barulhento; escolha padrão é `G = 8`- Não .`64`- Não .
  **组大小太小。**组基线的方差与 `1/√G`É verdade.`G = 4`Os seguintes sinais de vantagem são ruídos;`G = 8`Até`64`- Não.
- **Length bias.**Completos LLM de diferentes comprimentos têm diferentes log-probabilidades. Normalize por contagem de tokens, ou use log-prob de nível de sequência, ou truncate para a máxima comprimento.
  **长度偏差。**Diferentes de duração LLM  conclusão com probabilidade de contra-número diferente  por token  numeração ou corte até a maior duração
- **Pure self-play cycles.**O treinamento no estilo AlphaZero pode ficar preso em loops de domínio em jogos de soma geral.
  **纯自我博弈循环。**O treinamento AlphaZero pode ser um ciclo de controle em geral e em geral.
- **Search-policy mismatch.**O AlphaZero treina a política para imitar o resultado da pesquisa.
  **搜索-策略不匹配。**AlphaZero trenagem estratégia em forma de busca de saída.
- **Compute floor.**MuZero / AlphaZero precisa de computação maciça. Uma única ablação costuma ser de centenas de horas de GPU. Existem demos em miniatura (por exemplo, AlphaZero no Connect Four) para aprendizagem.
  **计算下限。**MuZero/AlphaZero  necessita de um grande número de cálculos ∙
- **Verifier coverage.**Os testes de unidade que aprovam uma solução de buggy reforçam o bug.
  **验证器覆盖。**通過有 bug 解決的单元测试会强化 bug;; design能捕获边缘情况的验证器;;

## Use-o com o framework implementado.

O cenário de jogo-RL de 2026, por domínio:

> 2026 年游戏 RL 版图, por domínio:

| Domain | Dominant method |
|--------|-----------------|
| Domain / 领域 | Dominant method / 主导方法 |
| Two-player zero-sum board games (Go, chess, shogi) / 双人零和棋类 | AlphaZero / MuZero / KataGo |
| Imperfect info card games (poker) / 不完全信息纸牌 | CFR + deep learning (DeepStack, Libratus, Pluribus) / CFR + 深度学习 |
| Atari / pixel games / Atari/像素游戏 | Muesli / MuZero / IMPALA-PPO |
| Large multiplayer strategy (Dota, StarCraft) / 大型多人策略 | PPO + self-play + league (OpenAI Five, AlphaStar) |
| LLM math/code reasoning / LLM 数学/代码推理 | GRPO (DeepSeek-R1, Qwen-RL, open replications) |
| LLM alignment / LLM 对齐 | DPO / RLHF-PPO (not GRPO; verifier is preference not verifiable) / DPO/RLHF-PPO |
| Robotics / 机器人 | PPO + DR (not game-RL, but uses same policy-gradient tools) / PPO+DR |
| Combinatorial problems / 组合问题 | AlphaZero variants (AlphaTensor, AlphaDev) / AlphaZero 变体 |

A *receita*  auto-jogo, melhoria aumentada pela pesquisa, destilação de políticas  abrange texto, pixels e controle físico.

> Esta * forma* auto-exploração  busca reforço de melhorias  estratégia  através do texto  imagem e controle físico  GRPO é o último exemplo; mais está chegando 

## Envia-o . Produto .

Salva como`outputs/skill-game-rl-designer.md`- Não .

```markdown
---
name: game-rl-designer
description: Design a game-RL or reasoning-RL training pipeline (AlphaZero / MuZero / GRPO) for a given domain.
version: 1.0.0
phase: 9
lesson: 12
tags: [rl, alphazero, muzero, grpo, self-play]
---

Given a target (perfect-info game / imperfect-info / Atari / LLM reasoning / combinatorial), output:

1. Environment fit. Known rules? Markov? Stochastic? Multi-agent? Informs AlphaZero vs MuZero vs GRPO.
2. Search strategy. MCTS (PUCT with learned prior), Gumbel-sampled, best-of-N, or none.
3. Self-play plan. Symmetric self-play / league / offline data / verifier-generated.
4. Target signal. Game outcome / verifier reward / preference / learned model. Include robustness plan.
5. Diagnostics. Win rate vs baseline, ELO curve, verifier pass rate, KL to reference.

Refuse AlphaZero on imperfect-info games (route to CFR). Refuse GRPO without a trusted verifier. Refuse any game-RL pipeline without a fixed baseline opponent set (self-play ELO is uncalibrated otherwise).
```

## Exercícios.

1. **Easy.**Implementar o bandido do GRPO em `code/main.py`. Treinar em 2 instruções × 4 tokens de resposta cada. Convergir em < 1.000 atualizações com `G=8`- Não .
2. **Medium.**Compare a eficiência da amostra e a variação da recompensa com a GRPO no mesmo bandido.
3. **Hard.**Estender para uma "cadeia de raciocínio" de comprimento-2: o agente emite dois tokens e o verificador recompensa o par. Medir como o GRPO lida com a atribuição de crédito em duas sequências de passos. (Punta: vantagem do grupo de cálculo por *sequência completa*, propagar para ambas as posições de tokens.)

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| MCTS | "Tree search with learned net" / 蒙特卡洛树搜索 | Monte Carlo Tree Search; UCB1/PUCT selection with learned `(p, v)` priors. |
| AlphaZero | "Self-play + MCTS" / AlphaZero | Policy-value net trained to match MCTS visits and game outcome. |
| MuZero | "Learned-model AlphaZero" / MuZero | Same loop but in latent space via learned dynamics. |
| GRPO | "Critic-free PPO" / 组相对策略优化 | Group Relative Policy Optimization; REINFORCE with group-mean baseline + KL. |
| PUCT | "AlphaZero's UCB" / PUCT 选择公式 | `Q + c · p · √N / (1 + N_a)` — balances value estimate with prior. |
| Self-play | "Agent vs past self" / 自我博弈 | Standard for zero-sum; symmetric training signal. |
| League play | "Population-based self-play" / 联盟训练 | Past + current + exploiters sampled as opponents. |
| Verifier reward | "Verifiable RL" / 验证器奖励 | Reward comes from a deterministic checker (tests pass, answer matches). |
| Process reward | "PRM" / 过程奖励模型 | Scores each reasoning step, not just the final answer. |

## Mais leitura 延伸阅读

- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270)- Não .
- [Silver et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play (AlphaZero)](https://www.science.org/doi/10.1126/science.aar6404)- Não .
- [Schrittwieser et al. (2020). Mastering Atari, Go, chess and shogi by planning with a learned model (MuZero)](https://www.nature.com/articles/s41586-020-03051-4)- Não .
- [Vinyals et al. (2019). Grandmaster level in StarCraft II (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z)- Não .
- [DeepSeek-AI (2024). DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO)](https://arxiv.org/abs/2402.03300) o artigo que introduziu o GRPO e a linha de base relativa ao grupo.
- [DeepSeek-AI (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) a receita completa de quatro etapas R1 mais a ablação R1-Zero.
- [Brown et al. (2019). Superhuman AI for multiplayer poker (Pluribus)](https://www.science.org/doi/10.1126/science.aay2400) CFR + aprendizagem profunda em escala.
- [Tesauro (1995). Temporal Difference Learning and TD-Gammon](https://dl.acm.org/doi/10.1145/203330.203343)O jornal que começou tudo.
- [Hugging Face TRL — GRPOTrainer](https://huggingface.co/docs/trl/main/en/grpo_trainer) a referência de produção para a aplicação de GRPO com funções de recompensa personalizadas.
- [Qwen Team (2024). Qwen2.5-Math — GRPO replication](https://github.com/QwenLM/Qwen2.5-Math) replicação aberta da receita R1 em múltiplas escalas.
- [Sutton & Barto (2018). Ch. 17 — Frontiers of Reinforcement Learning](http://incompleteideas.net/book/RLbook2020.pdf) o enquadramento do livro de texto para o auto-joco, a pesquisa e a "recompensa concebida" que R1 representa na escala de LLM.
