# Deep Q-Networks (DQN)

> 2013: Mnih treinou uma rede de aprendizado Q em pixels brutos, venceu todos os agentes RL clássicos em sete jogos Atari. 2015: estendido para 49 jogos, publicado na Nature, desencadeou a era do aprendizado profundo.

> **【中文解读】**DQN = Q-learning + Neural Network + 三个稳定化技巧 (三个稳定化技巧) △experience回放、目标网络、奖励剪) △2013-2015 anos em Atari 游戏 , derrotou todos os clássicos RL 方法, inaugurou a época do RL profundo ⋅ Estes três técnicas ainda são usadas em todos os métodos de RL profundo ⋅

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 04 (Q-learning, SARSA) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 04 (Q-learning, SARSA)
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

O tabular Q-learning precisa de um valor Q separado para cada par (estado, ação). Uma tabela de xadrez tem ~1043 estados. Um quadro Atari é 210×160×3 = 100.800 recursos.

> O modelo de aprendizagem Q  precisa para cada estado, movimento) para o armazenamento individual um valor Q ⋅ um internacional de xadrez tem cerca de 1043 estados ⋅ um Atari  tem 210×160×3 = 100,800 características ⋅ o modelo RL em mil estados já está perdido, não preciso dizer bilhões ⋅

A solução é óbvia em retrospectiva: substituir a tabela Q por uma rede neural.`Q(s, a; θ)`Mas a aproximação das funções naívas com a aprendizagem Q diverge sob a "triade mortal"  aproximação das funções + bootstrapping + aprendizagem fora da política. Mnih et al. (2013, 2015) identificou três truques de engenharia que estabilizam a aprendizagem:

> A solução é simples: usar a rede neural.`Q(s, a; θ)`替换Q 表――但这个"简单"花了几十年――简单的函数近似与Q-learning 在"致命三要素"下会发散函数近似 +自举 + 离策略学习――Mnih 等人(2013、2015) identificou três técnicas de engenharia de aprendizagem estável:

1. **Experience replay**descorrela as transições.
   **经验回放**打破转移的时间相关性──
2. **Target network**congela o alvo da banda de arranque.
   **目标网络**结自举目标──
3. **Reward clipping**normaliza as magnitudes de gradiente.
   **奖励裁剪**归一化梯度级级──

A DQN no Atari foi a primeira vez que uma única arquitetura com um único conjunto de hiperparâmetros resolveu dezenas de problemas de controle a partir de pixels brutos. Tudo o "deep-RL" construído desde DDQN, Rainbow, Dueling, Distribucional, R2D2, Agent57  é empilhado em cima desta base de três truques.

> O DQN do Atari é o primeiro a usar uma única estrutura e um único superparâmetro conjunto para resolver dezenas de problemas de controle desde o primeiro plano.

> **【中文解读】**"Tres fatores fatais": função aproxima + auto-receita + estratégia de saída → Treinamento estável ou mesmo disperso.

> **【拓展：经验回放→RLHF】**O pensamento de experience re放 (Experience Replay) está presente no treinamento do LLM: buffer do treinamento do PPO RLHF  preferência do DPO DATACET 

## O conceito central.

![DQN training loop: env, replay buffer, online net, target net, Bellman TD loss](../assets/dqn.svg)

**The objective.**DQN minimiza a perda TD de um passo em uma função Q neural:

`L(θ) = E_{(s,a,r,s')~D} [ (r + γ max_{a'} Q(s', a'; θ^-) - Q(s, a; θ))² ]`

`θ`= rede online, atualizada a cada passo por descida de gradiente. `θ^-`= rede-alvo, copiada periodicamente a partir de `θ`(a cada ~ 10.000 passos). `D`= Buffer de repetição de transições passadas.

> **目标。**DQN 最小化神经 Q 函数 单步 TD 损失──`θ`= On-line network, cada passo através da gradiência abaixo atualização.`θ^-`= 目标网络, periodicamente `θ`复制(约每 10,000 步) ⋅`D`= 过去转移的回放缓冲区──

**The three tricks, in order of importance:**

> **三个技巧，按重要性排序：**

**Experience replay.**Um tampão de anel de `~10⁶`Transmissões. Cada etapa de treinamento mostra um minibatch uniformemente aleatório. Isso quebra a correlação temporal (quadros sucessivos são quase idênticos), permite que a rede aprenda de raras transições gratificantes muitas vezes e descorrela atualizações de gradiente consecutivas. Sem ele, a TD na política com uma rede neural diverge na Atari.

> **经验回放。**Uma área de transição de cerca de 106 vezes. Cada fase de treinamento é feita de forma média, como um pequeno lote. Isso rompe a correlação de tempo.

**Target network.**Usando a mesma rede `Q(·; θ)`Em ambos os lados da equação Bellman faz com que o alvo se mova a cada atualização  "perseguindo sua própria cauda".`Q(·; θ^-)`com pesos congelados.`C`Passo, cópia.`θ → θ^-`Estabiliza o alvo de regressão para milhares de passos de gradiente de uma vez.`θ^- ← τ θ + (1-τ) θ^-`(usados em DDPG, SAC) são uma variante mais suave.

> **目标网络。**Em Bellman 方程 ambos os lados de uso da mesma rede irá fazer com que o objetivo de cada atualização está em movimento" perseguir seu próprio尾巴"──修复方法:`C`步复制 `θ → θ^-`◊ soft update(DDPG、SAC 中使用) é um tipo de variação mais simples.

**Reward clipping.**As magnitudes da recompensa Atari variam de 1 a 1000+.`{-1, 0, +1}`Não é certo quando a magnitude da recompensa é importante, bem para a Atari, onde só a assinatura é importante.

> **奖励裁剪。**Atari  Graduação de prêmios de 1 a 1000+ não é o mesmo.`{-1, 0, +1}`Prevenir qualquer tipo de jogo.

**Double DQN.**Hasselt (2016) corrige o viés de maximização: use a rede online para *selecionar* a ação, a rede alvo para * avaliá-la*.

`target = r + γ Q(s', argmax_{a'} Q(s', a'; θ); θ^-)`

Substituição de drop-in, consistentemente melhor.

> **双重 DQN。**Hasselt (2016) 修复最大化偏差:用在线网络*选择*动作,用目标网络*评估*它──直接替换,始终更好──默认使用──

**Other improvements (Rainbow, 2017):**Reprodução prioritária (muitas transições de alto TD-erro), arquitetura de duelo (separada `V(s)`A primeira é a de um sistema de gestão de dados, que é o sistema de gestão de dados e de dados, que é o sistema de gestão de dados e de dados, que é o sistema de gestão de dados e de dados, que é o sistema de gestão de dados e de dados e que é o sistema de gestão de dados e de dados.

> **其他改进（Rainbow, 2017）：**优先回放、决斗架构、噪声网络、n 步回报、分布式 Q、多步自举── cada tipo de melhoria contribuiu com vários pontos;收益大致可叠加──

> **【拓展：Rainbow DQN 与集成改进】**Rainbow DQN(2017) irá integrar 6 tipos de DQN  melhoramento juntos: prioridade experiência re-lação Dueling 架构、 noise network exploration、n 步回报、 distribuído Q 学习、多步自举── cada tipo de melhoramento contribui para uma melhoria de desempenho de vários centos de pontos, o efeito do conjunto é significativo── este tipo de "integração de volume" também se manifesta na formação do LLM  qualidade de dados、 estratégias de treinamento、 efeito da melhoria da estrutura geralmente é superimposto.

## Construí-lo e realizei-o.
```figure
f3-dqn-stability
```

## Construí-lo

O código aqui é stdlib-only numpy-free  usamos um MLP de camada oculta única rolado à mão em um pequeno GridWorld contínuo, então cada passo de treinamento é executado em microsecondas. O algoritmo é idêntico ao Atari DQN em escala.

> O código aqui é apenas usado em uma biblioteca de padrões em um microcontrole GridWorld.

### Passo 1: Buffer de repetição

```python
class ReplayBuffer:
    def __init__(self, capacity):
        self.buf = []
        self.capacity = capacity
    def push(self, s, a, r, s_next, done):
        if len(self.buf) == self.capacity:
            self.buf.pop(0)
        self.buf.append((s, a, r, s_next, done))
    def sample(self, batch, rng):
        return rng.sample(self.buf, batch)
```

- 50.000 para a Atari. 5.000 são suficientes para o nosso ambiente de brinquedos.

> A Atari precisa de 50.000 unidades, o nosso ambiente de jogos é de 5.000.

### Passo 2: uma pequena rede Q (MLP manual)

```python
class QNet:
    def __init__(self, n_in, n_hidden, n_actions, rng):
        self.W1 = [[rng.gauss(0, 0.3) for _ in range(n_in)] for _ in range(n_hidden)]
        self.b1 = [0.0] * n_hidden
        self.W2 = [[rng.gauss(0, 0.3) for _ in range(n_hidden)] for _ in range(n_actions)]
        self.b2 = [0.0] * n_actions
    def forward(self, x):
        h = [max(0.0, sum(w * xi for w, xi in zip(row, x)) + b) for row, b in zip(self.W1, self.b1)]
        q = [sum(w * hi for w, hi in zip(row, h)) + b for row, b in zip(self.W2, self.b2)]
        return q, h
```

Passagem para a frente: linear → ReLU → linear.

> 前向传播:线性 → ReLU → 线性──这就是整个网络──

### Passo 3: atualização do DQN

```python
def train_step(online, target, batch, gamma, lr):
    grads = zeros_like(online)
    for s, a, r, s_next, done in batch:
        q, h = online.forward(s)
        if done:
            y = r
        else:
            q_next, _ = target.forward(s_next)
            y = r + gamma * max(q_next)
        td_error = q[a] - y
        accumulate_grads(grads, online, s, h, a, td_error)
    apply_sgd(online, grads, lr / len(batch))
```

A forma é Q-learning da lição 04 com duas diferenças: (a) nós retro-prop através de um diferenciável `Q(·; θ)`Em vez de indexar uma tabela, (b) as utilizações-alvo `Q(·; θ^-)`- Não .

> Forma Q-learning é semelhante à lição 04 mas tem duas diferenças:`Q(·; θ)`Controvertido e não indicativo, b) objetivou uso `Q(·; θ^-)`- Não.

### Passo 4: o circuito externo

Para cada episódio, agem com ganância.`Q(·; θ)`, empurrar transições para o tampão, amostrar um minibatch, dar um passo de gradiente, sincronizar periodicamente `θ^- ← θ`O padrão:

```python
for episode in range(N):
    s = env.reset()
    while not done:
        a = epsilon_greedy(online, s, epsilon)
        s_next, r, done = env.step(s, a)
        buffer.push(s, a, r, s_next, done)
        if len(buffer) >= batch:
            train_step(online, target, buffer.sample(batch), gamma, lr)
        if steps % sync_every == 0:
            target = copy(online)
        s = s_next
```

No nosso pequeno GridWorld com um estado de 16 dimensões, o agente aprende uma política quase ótima em cerca de 500 episódios.

> Em nosso uso de 16 dimensional um-hot  estado de micro GridWorld, o corpo inteligente está em cerca de 500 reúne-se para aprender a aproximar-se da melhor estratégia.

## Encurralagens

- **Deadly triad.**A aproximação de função + off-policy + bootstrapping pode divergir. DQN mitiga com rede de alvo + replay; não remova nenhum.
  **致命三要素。**函数近似+离策略+自举可能发散──DQN 通过目标网络+回放缓解; não mover qualquer um──
- **Exploration.**A rede Q-net converge para uma bacia local sem exploração precoce suficiente.
  **探索。**É necessário diminuir, geralmente de 1.0 a 0.01, cobrir cerca de 10% do treinamento anterior.
- **Overestimation.** `max`Em relação ao Q barulhento, a taxa de aumento é parcial.
  **过估计。**Para Q                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            `max`会上偏倚──生产中始终使用双重 DQN──
- **Reward scale.**Clip ou normalizar recompensas; a magnitude do gradiente é proporcional à magnitude da recompensa.
  **奖励尺度。** redução ou redução de remuneração; graduação de nível e graduação de remuneração em relação à
- **Replay buffer coldstart.**Não treine até o tampão ter alguns milhares de transições.
  **回放缓冲区冷启动。**缓冲区有几千次转移后再训练――早期约20样本上梯度过适应――
- **Target sync frequency.**O Atari DQN usa 10.000 passos de env. Regra geral: sincronizar cada 1/100 do horizonte de treinamento.
  **目标同步频率。**太频繁≈没有目标网络;太不频繁≈过时目标――experience law: 每约1/100 训练视野同步一次――
- **Observation preprocessing.**A Atari DQN apila 4 quadros para fazer estado Markov. Qualquer env com informações de velocidade precisa de estado de quadros ou recorrente.
  **观测预处理。**Atari DQN 堆叠 4 使状态满足马尔可性──任何有速度信息的环境都需要堆叠或循环状态──

## Use-o com o framework implementado.

Em 2026, o DQN raramente é o estado da arte, mas continua a ser o algoritmo de referência fora da política:

> 2026 anos, DQN  muito pouco é o mais avançado, mas ainda está fora do algoritmo estratégico:

| Task | Method of choice | Why not DQN? |
|------|------------------|--------------|
| Task / 任务 | Method of choice / 首选方法 | Why not DQN? / 为什么不用 DQN？ |
| Discrete-action Atari-like / 离散动作类 Atari | Rainbow DQN or Muesli | Same framework, more tricks. / 相同框架，更多技巧。 |
| Continuous control / 连续控制 | SAC / TD3 (Phase 9 · 07) | DQN has no policy network. / DQN 没有策略网络。 |
| On-policy / high-throughput / 在线策略/高吞吐 | PPO (Phase 9 · 08) | No replay buffer; easier to scale. / 无回放缓冲区；更易扩展。 |
| Offline RL / 离线 RL | CQL / IQL / Decision Transformer | Conservative Q targets, no bootstrapping blowups. / 保守 Q 目标，无自举爆炸。 |
| Large discrete action spaces (recommender) / 大离散动作空间（推荐） | DQN with action embedding, or IMPALA | Fine; decoration matters. / 可行；细节很重要。 |
| LLM RL / LLM RL | PPO / GRPO | Sequence-level, not step-level; different loss. / 序列级而非步级；不同损失。 |

As lições ainda viajam. Replay e redes alvo aparecem em SAC, TD3, DDPG, SAC-X, buffer de auto-replay do AlphaZero e em todos os métodos offline de RL. O recorte de recompensas continua a ser uma normalização de vantagem no PPO. A arquitetura é o projeto.

> Estas experiências ainda são válidas. O regresso e a rede de objetivos aparecem na SAC, TD3, DDPG, SAC-X, AlphaZero, em sua própria área de amortização e em cada linha de RL.

## Envia-o . Produto .

Salva como`outputs/skill-dqn-trainer.md`- Não .

```markdown
---
name: dqn-trainer
description: Produce a DQN training config (buffer, target sync, ε schedule, reward clipping) for a discrete-action RL task.
version: 1.0.0
phase: 9
lesson: 5
tags: [rl, dqn, deep-rl]
---

Given a discrete-action environment (observation shape, action count, horizon, reward scale), output:

1. Network. Architecture (MLP / CNN / Transformer), feature dim, depth.
2. Replay buffer. Capacity, minibatch size, warmup size.
3. Target network. Sync strategy (hard every C steps or soft τ).
4. Exploration. ε start / end / schedule length.
5. Loss. Huber vs MSE, gradient clip value, reward clipping rule.
6. Double DQN. On by default unless explicit reason to disable.

Refuse to ship a DQN with no target network, no replay buffer, or ε held at 1. Refuse continuous-action tasks (route to SAC / TD3). Flag any reward range > 10× per-step mean as needing clipping or scale normalization.
```

## Exercícios.

1. **Easy.**Corra .`code/main.py`Quantos episódios até que a média de execução exceda -10?
2. **Medium.**Desativar a rede-alvo (utilizar a rede online para ambos os lados do alvo Bellman).
3. **Hard.**Adicionar DQN duplo: usar a rede online para escolher `argmax a'`, meta rede para avaliar.`Q(s_0, best_a)`contra verdade`V*(s_0)`Depois de 1.000 episódios com vs. sem Double DQN em um GridWorld de prêmios barulhentos.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| DQN | "Deep Q-learning" / 深度Q网络 | Q-learning with a neural Q-function, replay buffer, and target network. |
| Experience replay | "Shuffled transitions" / 经验回放 | Ring buffer sampled uniformly each gradient step; decorrelates data. |
| Target network | "Frozen bootstrap" / 目标网络 | Periodic copy of Q used in the Bellman target; stabilizes training. |
| Deadly triad | "Why RL diverges" / 致命三要素 | Function approximation + bootstrapping + off-policy = no convergence guarantee. |
| Double DQN | "Fix for maximization bias" / 双重DQN | Online net selects action, target net evaluates it. |
| Dueling DQN | "V and A heads" / 决斗DQN | Decompose Q = V + A - mean(A); same output, better gradient flow. |
| Rainbow | "All the tricks" / Rainbow | DDQN + PER + dueling + n-step + noisy + distributional in one. |
| PER | "Prioritized Replay" / 优先经验回放 | Sample transitions proportional to TD-error magnitude. |

## Mais leitura 延伸阅读

- [Mnih et al. (2013). Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602) o artigo de workshop de 2013 do NeurIPS que deu início à RL profunda.
- [Mnih et al. (2015). Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236)O artigo Nature, 49 jogos DQN.
- [Hasselt, Guez, Silver (2016). Deep Reinforcement Learning with Double Q-learning](https://arxiv.org/abs/1509.06461) DDQN.
- [Wang et al. (2016). Dueling Network Architectures](https://arxiv.org/abs/1511.06581)Duelos com DQN.
- [Hessel et al. (2018). Rainbow: Combining Improvements in Deep RL](https://arxiv.org/abs/1710.02298)O papel de truques empilhados.
- [OpenAI Spinning Up — DQN](https://spinningup.openai.com/en/latest/algorithms/dqn.html)- Exposição moderna clara.
- [Sutton & Barto (2018). Ch. 9 — On-policy Prediction with Approximation](http://incompleteideas.net/book/RLbook2020.pdf) o tratamento manual da "triada mortal" (aproximativa de funções + bootstrapping + off-policy) que a rede-alvo e o buffer de repetição da DQN são concebidos para domar.
- [CleanRL DQN implementation](https://docs.cleanrl.dev/rl-algorithms/dqn/) DQN de referência de ficheiro único utilizado em estudos de ablação; bom para ler ao lado da versão do zero desta lição.
