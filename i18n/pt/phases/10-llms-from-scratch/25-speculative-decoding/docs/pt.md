# Descodagem especulativa e Eagle.

> Um LLM de fronteira que gera um token requer uma passagem completa para a frente em bilhões de parâmetros. Esse passado para a frente é massively superprovisionado: na maioria das vezes um modelo muito menor pode adivinhar os próximos 3-5 tokens corretamente, e o modelo grande só precisa *verificar* a adivinhação. Quando a suposição for certa, você tem 5 tokens pelo preço de um. Descodagem especulativa (Leviathan et al. 2023) fez isso exatamente, e EAGLE-3 (2025) empurrou as taxas de aceitação para ~ 4,5 tokens por verificação  um aumento de 4-5x na distribuição de saída correspondente.

> **【中文解读】**O Mestrado em Ciências Magistrais (LLM) produz um token  necessita de uma vez completa de bilhões de parâmetros                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

> **【拓展：投机解码→推理加速】**投机解码是 2025-2026年推理加速的标准技术──DeepSeek-V3  MTP                                                                                                                                                                                                                                                 

> - Não .**【前置】**学本节前请先掌握:Fase 07·16(投机解码数学证明);Fase 10·12(推理优化基础)。本节是Fase 10·15(EAGLE-3) 的更早版本(基础+EAGLE),Fase 10·15 是 V3 升级版。

**Type:** Build
**Languages:** Python (with numpy)
**Prerequisites:** Phase 10 Lesson 12 (Inference Optimization), Phase 10 Lesson 04 (Pre-training Mini-GPT)
**Time:** ~75 minutes

## O problema é o problema da introdução

O decodificador de um modelo de classe 70B no H100 é tipicamente de 40-80 tokens / segundo. Cada token requer uma passagem completa para frente que lê todos os pesos do modelo do HBM. Você não pode tornar o modelo menor sem alterar sua saída. Você não pode aumentar o tamanho do lote além da memória. Você está preso  a menos que você possa deixar o modelo produzir mais de um token por passagem para frente.

A geração autoregressiva parece inerentemente seria:`x_{t+1} = sample(p(· | x_{1:t}))`Mas há uma oportunidade de simultânea. Se você tivesse um preditor barato que diz "os próximos 4 tokens são provavelmente [a, b, c, d]" você poderia verificar todas as 5 posições em um **single forward pass of the big model**e aceitar o prefixo mais longo correspondente.

Leviathan, Kalai, Matias (2023, "Inferência Rápida dos Transformadores através da Descodagem Especulativa") fez isso exatamente através de uma regra inteligente de aceitação / rejeição que preserva a distribuição de amostragem do modelo alvo. A mesma distribuição de saída, 2-4 vezes mais rápida.

## O conceito central.

> **【中文解读】**投机解码的核心思想: usando um pequeno esquema modelo de rápida geração de k 个候选符号, reutilizar o objetivo grande modelo并行验证这 k 个符号── 接受的符号 直接保留(零额外延迟),被拒绝的从第一错处重新生成──数学证明:输出分布与直接使用大模型生成完全相同──

> **【拓展：投机解码的工程实践】**A taxa de aceleração do desenho de projetos depende da distribuição e da eficiência de batch de distribuição do modelo de esboço e do modelo-alvo. Na prática, a utilização de uma versão menor da mesma série de projetos (como Llama-3-8B para Llama-3-70B) é a melhor.


### A configuração de dois modelos

- **Target model** `M_p`O modelo grande, lento e de alta qualidade do qual realmente se querem amostras.`p(x)`- Não .
- **Draft model** `M_q`O modelo é pequeno, rápido e de baixa qualidade.`q(x)`5 a 30 vezes menor.

Por etapa:

1. Propõe-se um projecto de modelo `K`Tokens autoregressivamente: `x_1, x_2, ..., x_K ~ q`- Não .
2. O modelo-alvo é um passe para frente sobre todos .`K+1`posições paralelas, produzindo`p(x_k)`para cada token proposto.
3. Aceitar/rejectar cada token de esquerda para direita através da regra de rejeição modificada abaixo.
4. Se qualquer token for rejeitado, mostre o substituto da distribuição corrigida e pare.`p(· | x_1...x_K)`- Não .

Se o projeto coincide perfeitamente com o objetivo, você recebe tokens K + 1 por objetivo-ahead. Se o projeto estiver errado na posição 1, você recebe apenas 1 token.

### A Regra da Exactitude

A descodificação especulativa é **provably equivalent in distribution to sampling from p**A regra de rejeição:

```
For each drafted token x_t:
    r ~ Uniform(0, 1)
    if r < p(x_t) / q(x_t):
        accept x_t
    else:
        sample replacement from residual: (p - q)+ / ||(p - q)+||_1
        stop
```

onde`(p - q)+`Quando o projecto e o objectivo são de acordo (`p ≈ q`Quando os dois grupos discordam, a distribuição residual é construída de modo a que a amostra geral seja ainda exata.`p`- Não .

**Greedy case.**Para a amostragem de temperatura=0 basta verificar `argmax(p) == x_t`Se sim, aceita; se não, saída.`argmax(p)`E pára.

### A expectativa de aceleração

Se a taxa de aceitação a nível de tokens do modelo de projeto for `α`, os tokens esperados produzidos por passagem de destino é:

```
E[tokens] = (1 - α^{K+1}) / (1 - α)        # K = draft length, α in [0, 1]
```

- Não .`α = 0.8, K = 4`- Não .`(1 - 0.8^5)/(1 - 0.8) = 3.36`Os preços de um único destino a prazo são aproximadamente`cost_q * K + cost_p`(K passo-figura mais uma verificação de objectivo).`cost_p >> cost_q * K`O índice de aceleração é `3.36× / 1 = 3.36×`- O que é?

O único parâmetro real é`α`O que é preciso é um bom projecto.

### Formação do projecto: Destilação

Um modelo aleatório faz um esboço ruim.

1. Escolha uma pequena arquitetura (~ 1B para um alvo 70B, ~ 500M para um alvo 7B).
2. Execute o modelo-alvo em um grande corpus de texto; armazenar suas distribuições de tokens seguintes.
3. Treinar o rascunho com divergência KL contra a distribuição do alvo (não contra tokens de verdade base).

O resultado: `α`Normalmente 0,6-0,8 na codificação, 0,7-0,85 no chat em linguagem natural.

### ÁGLA: Arvore de desenho + Reutilização de recursos

Li, Wei, Zhang, Zhang (2024, "AEGLE: Especulative Sampling Requires Rethinking Feature Uncertainty") observaram duas ineficiências na descodificação especulativa padrão:

1. O projeto faz K série passos, cada pilha completa. Mas o projeto poderia reutilizar as características do alvo (estados ocultos) do mais recente verificar  o alvo já computado representações ricas que o projeto está re-derivado do zero.
2. O projeto produz uma cadeia linear. Se o projeto pudesse produzir uma árvore de candidatos (cada nó adivinha múltiplas), a passagem para frente única do alvo poderia verificar múltiplos caminhos de candidatos em paralelo através de uma máscara de atenção para a árvore e escolher o ramo mais longo aceito.

Mudanças da EAGLE-1:
- Introdução de projeto = estado oculto final do alvo na posição t, não tokens brutos.
- Arquitetura de projeto = 1 camada de decodificador de transformador (não um modelo pequeno separado).
- Output = árvore de K = 4-8 candidatos por profundidade, profundidade 4-6.

A AGLE-2 (2024) adiciona uma topologia dinâmica de árvores: a árvore cresce mais larga onde o rasto é incerto e permanece estreita onde é confiante.`α_effective`sem aumentar o custo de verificação.

AEGLE-3 (Li et al. 2025, "EAGLE-3: Aumenta a aceleração da inferência de grandes modelos de linguagem através do teste de tempo de treinamento") elimina a dependência fixa de recursos de camada superior e treina o projeto com uma nova perda de "simulação de tempo de teste"  o projeto é treinado em resultados que correspondem à distribuição de tempo de teste do alvo, em vez de distribuição de treinamento forçado do professor. A taxa de aceitação aumenta de 0,75 (EAGLE-2) para 0,82 (EAGLE-3), e a média de tokens/verificação de 3,0 para 4,5.

### Verificação da Atenção à Árvore

Quando o rascunho produz uma árvore, o modelo-alvo verifica-a num único passo para frente usando um **tree attention mask** uma máscara causal que codifica a topologia da árvore em vez de uma linha pura. Cada token atende apenas aos seus antepassados na árvore. A passagem de verificação ainda é uma frente, uma matmul; a máscara topológica custa apenas algumas entradas KV extras.

```
        root
       /    \
      a      b
     / \    / \
    c  d   e   f
```

Se`a, b`estão a competir candidatos com primeiro token e `c, d, e, f`são candidatos a segundo token, todas as seis posições são verificadas em uma passagem para a frente.

### Quando ganha, quando não ganha

**Wins:**
- Chat / conclusão com texto previsível (código, inglês comum, saída estruturada). `α`É alto.
- Configurações com computação de GPU não utilizada durante a decodificação (fase de memória).

**Loses / no win:**
- Resultados altamente estocásticos (escritura criativa a alta temperatura). `α`Cai em direcção a`1/|vocab|`- Não .
- O lote que serve com uma concurrencia muito elevada  o lote já enche os FLOPs, pouco espaço para verificação de árvores.
- Modelos de alvo muito pequenos onde o projecto não é muito menor.

Lojas de produção normalmente relatam 2-3x de velocidade no chat, 3-5x na geração de código e quase zero na escrita criativa.


> **【拓展：投机解码的数学保证】**A distribuição de saída do jogo não é totalmente compatível com o modelo-alvo, mas sim com a rigor matemática.


## Construí-lo e realizei-o.
```figure
speculative-decoding
```

## Construí-lo

`code/main.py`- Não .

- Uma referência`speculative_decode(target, draft, prompt, K, temperature)`que implemente a regra exata de rejeição e verifica que preserva a distribuição do alvo (emprogramação empírica KL < 0,01 vs. amostragem de alvo comum).
- Um desenhador de árvores de estilo AGLE que constrói uma árvore de profundidade K com ramificação de p.
- Um construtor de máscara de atenção para árvores que produz o padrão causal certo para um verificador.
- Um arame de taxa de aceitação que funciona em ambos os dois em um pequeno LM (destila um GPT-2- pequeno de um alvo GPT-2-médio).

```python
def speculative_step(p_target, q_draft, K, temperature=1.0):
    """One round of speculative decoding. Returns list of accepted tokens."""
    # 1. Draft K tokens
    draft_tokens = []
    q_probs = []
    state = draft_state_init()
    for _ in range(K):
        probs = softmax(q_draft(state) / temperature)
        t = np.random.choice(len(probs), p=probs)
        draft_tokens.append(t)
        q_probs.append(probs[t])
        state = draft_step(state, t)

    # 2. Target computes p at every drafted position + 1 extra
    p_probs_all = target_forward_batched(p_target, draft_tokens, temperature)

    # 3. Accept/reject left-to-right
    accepted = []
    for k, tok in enumerate(draft_tokens):
        r = np.random.uniform()
        if r < p_probs_all[k][tok] / q_probs[k]:
            accepted.append(tok)
        else:
            residual = np.maximum(p_probs_all[k] - q_probs[k], 0)
            residual /= residual.sum()
            accepted.append(np.random.choice(len(residual), p=residual))
            return accepted
    # 4. All K accepted → sample bonus token from target
    accepted.append(np.random.choice(len(p_probs_all[-1]), p=p_probs_all[-1]))
    return accepted
```

## Use-o com o framework implementado.

- **vLLM**E ...**SGLang**Navio de primeira classe de descodificação especulativa.`--speculative_model`- Não .`--num_speculative_tokens`. Apoio EAGLE-2/3 através do `--spec_decoding_algorithm eagle`- Não.
- **NVIDIA TensorRT-LLM**Apoia as árvores Medusa e Eagle nativo.
- **Reference draft models**- Não .`Qwen/Qwen3-0.6B-spec`(projetos para o Qwen3-32B), `meta-llama/Llama-3.2-1B-Instruct-spec`(projetos para o 70B).
- **Medusa heads**(Cai et al. 2024, "Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads"): em vez de um modelo de projeto, adicione heads de previsão paralelo K ao próprio alvo.

## Envia-o . Produto .

Esta lição produz`outputs/skill-speculative-tuning.md` uma habilidade que perfila a carga de trabalho de um modelo-alvo e escolhe: modelo de projeto, K (longo de projeto), largura da árvore, temperatura e quando voltar para a decodificação simples.

> 本课产 出 `outputs/skill-speculative-tuning.md` Análise objetivo modelo trabalho carga e seleção de desenho modelo  K(Duração do desenho)  Largura de árvore  Temperatura  Como voltar para o normal

## Exercícios.

1. Implementar a regra exata de rejeição e verificá-la empiricamente.`speculative_decode`e através de amostragem de alvo simples; calcular a distância TV entre as duas distribuições de saída. Deve ser < 0,01.
   Tradução do inglês: implement precisamente rejeitar regras e experiência.`speculative_decode`和普通目标采样各运行 10K 样本; calcular a distância entre duas distribuições de TV △应 < 0.01──

2. Calcule a fórmula de aceleração.`α`E ...`K`, gráfico de tokens esperados por meta-ahead. Encontre o K ideal para α ∈ {0,5, 0,7, 0,9}.
   Tradução do inglês: calcular a fórmula de aceleração.`α`和 `K`, desenhar cada objetivo de espera para a divulgação num¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

3. Treinar um pequeno rascunho, tomar um alvo de 124 milhões de GPT-2 e destilar um rascunho de 30 milhões de GPT-2 em tokens de 100 milhões com perda KL.`α`- O número de dados de texto não divulgados.
   Tradução do inglês para tradução do inglês: train microtype drafts模型──以 124M GPT-2 为目标,在 100M token 上用 KL 损失蒸 30M GPT-2 草稿──在保留文本上测量 `α` Previsão: 0,6-0,7

4. Implemente o desenho de árvore no estilo EAGLE. Em vez de uma cadeia, tenha o desenho de saída em três ramos em cada profundidade. Construa a máscara de atenção da árvore. Verifique se o alvo aceita o ramo correto mais longo.
   Não é uma cadeia, mas sim um projecto que saiba o que é o primeiro.

5. Meter modos de falha. Execute decodificação especulativa em temperatura = 1,5 (alto estocástico). Mostre α colapsos e o algoritmo é mais lento do que decodificação simples devido a troca de custos.
   Em inglês, o algoritmo é mais lento do que o normal.

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Target model | "The big model" | The slow, high-quality model you want samples from (p distribution) | 目标模型，慢速高质量的大模型 |
| Draft model | "The speculator" | The small, fast predictor (q distribution); 5-30x smaller | 草稿模型，小而快的预测器 |
| K / draft length | "Look-ahead" | Number of speculated tokens per verify pass | 草稿长度，每次验证的投机 token 数 |
| α / acceptance rate | "Hit rate" | Per-token probability that the draft's proposal is accepted | 接受率，草稿每 token 被接受的概率 |
| Exact rejection rule | "The accept test" | r < p/q compare that preserves target's distribution | 精确拒绝规则，保持目标分布不变的接受测试 |
| Residual distribution | "Corrected p-q" | (p - q)+ / ||(p - q)+||_1, the distribution to sample from on rejection | 残差分布，拒绝时从中采样的校正分布 |
| Tree drafting | "Branching speculation" | Draft outputs a tree of candidates, verified in one pass with tree-structured attention mask | 树形草稿，一次验证多个分支候选 |
| Tree attention mask | "Topological mask" | Causal mask encoding the tree topology so each node attends only to its ancestors | 树注意力掩码，按拓扑结构编码因果掩码 |
| Medusa heads | "Parallel heads" | K extra prediction heads on the target itself; no separate draft model | Medusa 头，目标模型上的多个并行预测头 |
| EAGLE feature reuse | "Hidden-state draft" | Draft input is target's last hidden state, not raw tokens, shrinking the draft | EAGLE 特征复用，用目标模型隐藏状态作草稿输入 |
| Test-time simulation loss | "EAGLE-3 training" | Train draft on outputs matching target's test-time distribution, not teacher forcing | 测试时模拟损失，EAGLE-3 训练方法 |

## Mais leitura 延伸阅读

- [Leviathan, Kalai, Matias, 2023 — "Fast Inference from Transformers via Speculative Decoding"](https://arxiv.org/abs/2211.17192) a regra exata de rejeição e a análise teórica de aceleração
- [Chen, Borgeaud, Irving et al., 2023 — "Accelerating Large Language Model Decoding with Speculative Sampling"](https://arxiv.org/abs/2302.01318) papel de amostragem especulativa simultânea na DeepMind
- [Cai, Li, Geng, Wang, Wang, Zhu, Dao, 2024 — "Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads"](https://arxiv.org/abs/2401.10774) cabeças paralelas alternativas a um modelo de projecto
- [Li, Wei, Zhang, Zhang, 2024 — "EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty"](https://arxiv.org/abs/2401.15077) Reutilização das características e elaboração de árvores
- [Li et al., 2024 — "EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees"](https://arxiv.org/abs/2406.16858) Topologia dinâmica de árvores
- [Li et al., 2025 — "EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test"](https://arxiv.org/abs/2503.01840) correspondência entre o tempo de ensaio e o tempo de trem
- [Fu, Haotian, Peng et al., 2024 — "Break the Sequential Dependency of LLM Inference Using Lookahead Decoding"](https://arxiv.org/abs/2402.02057) A descodificação Jacobi/lookahead, uma alternativa livre de especuladores
