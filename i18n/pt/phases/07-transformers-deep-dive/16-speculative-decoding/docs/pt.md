# Descodagem especulativa  Projeto, Verificação, Repetição                                                                                                                                                                                                                                                      

> A descodificação autoregressiva é serial. Cada token espera para o anterior. A descodificação especulativa quebra a cadeia: um modelo barato elabora N tokens, o modelo caro verifica todos os N em uma passagem para frente. Quando o projeto é correto, você pagou um grande avanço para N gerações.

> **【中文解读】**Use pequeno modelo rápido gerar token de candidato, grande modelo de verificação em massa. Pode acelerar a raciocínio 2-3 vezes sem reduzir a qualidade.

**Type:** Hands-on | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 7 · 07 (GPT Causal LM), Phase 7 · 12 (KV Cache & Flash Attention) | **前置知识:** Phase 7 · 07 (GPT Causal LM), Phase 7 · 12 (KV Cache & Flash Attention)
**Time:** ~60 minutes | **时间:** ~60 分钟

## O problema é o problema da introdução

Uma amostragem de 70B LLM um token leva ~30 ms em um H100. Um modelo de projeto 3B leva ~3 ms. Se deixarmos o projeto 3B 5 tokens à frente, então executar o 70B * uma vez * para verificar todos os 5, o total é `5×3 + 30 = 45 ms`para até 5 tokens aceites  versus `5×30 = 150 ms`É o passo completo da descodificação especulativa: troca uma pequena quantidade extra de memória GPU (modelo de projeto) por 24× menor latência de decodificação.

> Uma linha de 70B LLM 采样一个代币 在H100上需要约30 ms──一个3B草案模型需要约3 ms──如果我们让3B提前生成5代币,然后运行70B *一次*验证所有5个,总时间为 `5×3 + 30 = 45 ms`O máximo de 5 tokens aceites são necessários para gerar diretamente.`5×30 = 150 ms`︎ é o ponto de venda total do código: usando uma pequena quantidade extra de GPUs em memória ({{draftmodel}}) em troca de 2-4 vezes mais baixo do código de atraso︎

O truque tem de preservar a distribuição. A amostragem especulativa, introduzida por Leviathan et al. (2023) e por Chen et al. simultaneamente, garante que a sequência de saída é **identically distributed**Não há troca de qualidade, só mais rápido.

> Esta técnica deve manter a distribuição inalterável.**完全相同**Não há perda de qualidade, só mais rápido.

Quatro famílias de pares de verificadores de rascunho dominam a inferência de 2026:

> Quatro tipos de projectos-verificadores assumirão a posição dominante na proposta de 2026:

1. **Vanilla speculative (Leviathan 2023).**Modelo de projeto separado (por exemplo, Llama 3 1B) + verificador (por exemplo, Llama 3 70B).
   Tradução:**朴素推测（Leviathan 2023）。**独立的草案模型(如 Llama 3 1B) + 验证器(如 Llama 3 70B) ⋅
2. **Medusa (Cai 2024).**Múltiples cabeças de decodificação no verificador prevê posições `t+1..t+k`Não há modelo de projeto separado.
   Tradução:**Medusa（Cai 2024）。**Multiple terminal em verificação e posições de previsão`t+1..t+k`Não é necessário um projecto independente.
3. **EAGLE family (Li 2024, 2025).**Draft leve que reutiliza os estados ocultos do verificador; taxa de aceitação mais próxima do que a baunilha; 34× típico.
   Tradução:**EAGLE 系列（Li 2024, 2025）。**复用验证器隐藏状态的轻量草案; 接受率比朴素方案更高; 典型加速3-4倍──
4. **Lookahead decoding (Fu 2024).**Iteração Jacobi, não é necessário nenhum modelo de projeto, auto-especulação, nicho, mas livre de dependência.
   Tradução:**前瞻解码（Fu 2024）。**Jacobi 代;完全不需要草案模型──自推测──小众但无依赖──

Cada estaca de inferências de produção em 2026 vai enviar decodificação especulativa por padrão. vLLM, TensorRT-LLM, SGLang e llama.cpp todos suportam pelo menos baunilha + EAGLE-2.

> Cada produção de 2026 anos 都默认搭载推测解码──vLLM、TensorRT-LLM、SGLang 和 llama.cpp 都至少支持朴素 + EAGLE-2──

> **【中文解读】**推测解码的核心洞察:自归生成是串行瓶──用小模型(3B) 快速生成 N 个候选代币,大模型(70B) 一次前向传播验证所有 N 个──总时间从 N×30ms 降至 5×3+30=45ms,加速 2-4 倍──关键:推测采样保证输出分布与大模型完全一致,无质量损失──

> **【拓展：EAGLE 与 Medusa 的自推测策略】**EAGLE(2024) Reutilize o estado oculto do grande modelo para gerar um projecto, a taxa de aceitação é maior do que o pequeno modelo independente, acelerando tipicamente 3-4 vezes.

## O conceito central.

### O algoritmo central

Dado um verificador `M_q`e um esboço mais barato `M_p`- Não .

> 给定验器 `M_q`E mais barato é o modelo de projeto.`M_p`- Não .

1. Deixe-me .`x_1..x_k`ser o prefixo já decodificado.
   Tradução:设 `x_1..x_k`Por que não se resolveu?
2. **Draft**: utilização `M_p`Proporcionar autoregressivamente `d_{k+1}, d_{k+2}, ..., d_{k+N}`com probabilidades de projeto `p_1..p_N`- Não .
   Tradução:**草案**:用 `M_p`Autorecursos`d_{k+1}, d_{k+2}, ..., d_{k+N}`, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,`p_1..p_N`- Não.
3. **Verify in parallel**- Não .`M_q`Uma vez por todas .`x_1..x_k, d_{k+1}, ..., d_{k+N}`, obtendo probabilidades de verificação `q_1..q_{N+1}`para posições `k+1..k+N+1`- Não .
   Tradução:**并行验证**- Não .`x_1..x_k, d_{k+1}, ..., d_{k+N}`- Não .`M_q`, obter posição`k+1..k+N+1`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `q_1..q_{N+1}`- Não.
4. **Accept/reject each draft token left to right**: para cada `i`, aceitar com probabilidade .`min(1, q_i(d_i) / p_i(d_i))`- Não .
   Tradução:**从左到右接受/拒绝每个草案 token**Para cada um .`i`, em probabilidade`min(1, q_i(d_i) / p_i(d_i))`- Aceitação.
5. Em primeira rejeição na posição `j`: amostra `t_j`da distribuição "residual" `(q_j - p_j)_+`Todos os projetos depois de`j`são descartadas.
   Tradução do português:`j`首次被拒绝时: de "残差" distribuição `(q_j - p_j)_+`归一化后采样 `t_j`- Não.`j`Depois, todos os projectos foram abandonados.
6. Sobre aceitar tudo .`N`: amostra um token extra `t_{N+1}`de`q_{N+1}`(o token de bônus gratuito).
   Tradução do português:当所有`N`个都被接受时: de `q_{N+1}`Como um token extra.`t_{N+1}`(título de recompensa gratuito)

O truque de distribuição residual é a visão matemática que mantém a saída distribuída exatamente como se `M_q`Tinha uma amostra de zero.

> A técnica de distribuição de diferença é manter a distribuição de saída e de saída.`M_q`A partir do princípio, a mesma matemática.

### O que determina a aceleração

Deixe-me .`α`= taxa de aceitação esperada por token de projeto.`c`= relação custo entre o projecto e o verificador.

> 设 `α`= Previsão de aceitação de cada token de projecto.`c`= custo do projecto e do verificador:

- A geração ingênua faz uma chamada de modelo grande por token.
  Tradução do inglês: 朴素生成每个 token 调用一次大模型──
- O especulativo faz uma chamada de modelo grande por dia .`(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)`Tokens quando `α`É alto.
  Tradução do português:`α`较高时,每 `(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)`- O que é isso?

Regra típica de um "`α = 0.75`E ...`N = 5`O custo do projeto é 5x barato. O total do relógio de parede cai cerca de 2,5x.

> `α = 0.75`和 `N = 5`时的典型经验法则:大模型调用减少3倍――草案成本是5倍便宜――实际总时间下降约2.5倍――

> **【中文解读】**A taxa de aceitação da taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa de taxa

**α depends on:**

> **α 取决于：**

- A forma como o projeto se aproxima do verificador.
  Tradução em inglês:Draft to approximate degree of verifier.
- Estratégia de decodificação. Draft ganancioso contra verificador ganancioso: alto α. Amostra de temperatura: mais difícil de combinar; aceitação cai.
  Tradução do inglês para o inglês: ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎  ︎  
- Tipo de tarefa: código e saída estruturada aceitam mais (predicável); escrita criativa em forma livre aceita menos.
  Tradução em inglês: task type──代码和结构化输出接受更多(可预测); 自由形式创意写作接受更少──

### Medusa  projectos sem modelo de projecto

Medusa substitui o modelo de projeto por cabeças de saída extra no verificador.`t`- Não .

> Medusa utilizou o extra-output do teste de teste em seu modelo de troca.`t`- Não .

```
shared trunk → hidden h_t
    ├── head_0: predict token at t+1  (standard LM head)
    ├── head_1: predict token at t+2
    ├── head_2: predict token at t+3
    ├── head_3: predict token at t+4
```

Cada cabeça sai suas próprias logites. Na inferência você amostra de cada cabeça para obter uma sequência candidata, em seguida, verifique com uma passagem para a frente usando um esquema de atenção de árvore que considera todas as continuações candidatas de uma vez.

> Cada cabeça sai sua própria lógica. Quando se faz uma avaliação, cada cabeça recebe uma sequência de candidaturas, e depois, usando o esquema de atenção, uma vez para a divulgação de testes, contempla todas as candidaturas.

Pros: nenhum segundo modelo. Cons: adiciona parâmetros treinables; precisa de uma fase de ajuste fino supervisionado (~ 1B tokens); taxa de aceitação é um pouco menor do que a vanilha especulativa com um bom esboço.

> 优点:无需第二模型──缺点:增加可训练参数;需要监督微调阶段(约1B token); acceptance rate比好的草案模型的朴素推测略低──

> **【拓展：推测解码在 vLLM 中的实现】**VLLM é o mais popular do ano 2026 LLM 推理框架,原生支持推测解码── é usado em batches contínuas (continuous batching) + PagedAttention + 推测解码的组合优化── em produção, o 推测解码 geralmente traz 2-3 vezes mais um atraso reduzido, para o cenário de conversação (user perception delay sensitive)

### A ÁGuila  melhor desenho reutilizando estados ocultos

EAGLE-1/2/3 (Li et al., 20242025) faz do modelo de projeto um pequeno transformador (tipicamente 1 camada) que ingere os estados ocultos da última camada do verificador. Como o projeto vê a representação de características do verificador, suas previsões se correlacionam fortemente com a distribuição de saída do verificador.

> EAGLE-1/2/3 ((Li 等人,2024-2025) vai fazer o modelo do projeto em um transformador de microtipo (((normalmente 1 nível), estado oculto da última camada do verificador de absorção.

A EAGLE-3 (2025) adicionou a busca de árvores sobre as continuações candidatos.

> EAGLE-3(2025) adicionou para o candidato de renovação de árvore buscas.

### A dança do cache KV

Feeds de verificação `N`O projeto de tokens para o verificador em uma passagem avançada.`N`Se alguns rascunhos forem rejeitados, você deve rolar o cache de volta ao comprimento de prefixo aceito.

> 验证在一次前向传播中将 `N`个草案 token 输入验证器── This will be the KV 缓存扩展                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `N`个条目── Se algum projecto for rejeitado, você deve reverter o caixe até ao prazo de duração aceito──

Implementações de produção (vLLM's `--speculative-model`O que é que eu quero dizer é que eu não posso fazer isso, mas eu quero que você faça isso.

> Produção de realização`--speculative-model`、TensorRT-LLM's LookaheadDecoder) usando temporário KV 缓冲区 para tratar este problema──pre-escrito, aceite quando enviado──conceptos não são difíceis, mas implementar é mais difícil ∼

## Construí-lo e realizei-o.
```figure
draft-verify-tokens
```

## Construí-lo

Veja .`code/main.py`Implementamos o algoritmo de amostragem especulativa central (passo de rejeição + distribuição residual) com:

> 参见 `code/main.py`△ Nós utilizamos os seguintes componentes para implementar o algoritmo de análise de dados (Refusal Step + Remain Difference):

- Um "modelo grande" que é um determinístico-softmax sobre uma distribuição codificada à mão (para que possamos verificar a aceitação matemática analíticamente).
  Tradução do inglês para tradução do inglês: "Big Model", é a determinação de uma determinada área de distribuição (de acordo com o inglês: determination softmax) para que a análise de experiências seja feita em matemática.
- Um "modelo de projeto" que é uma perturbação do modelo grande.
  Tradução do inglês para tradução do inglês:
- Um ciclo de aceitação/rejeição que produz a mesma distribuição marginal que a amostragem direta.
  Tradução do inglês para inglês: a) uma distribuição de lado ou de lado, que é feita de forma directa.

### Passo 1: o passo de rejeição

```python
def accept_or_reject(q_prob, p_prob, draft_token, u):
    ratio = q_prob / p_prob if p_prob > 0 else float("inf")
    return u < min(1.0, ratio)
```

`u`é um número aleatório uniforme. `q_prob`é a probabilidade do verificador para o token elaborado. `p_prob`O teorema de Leviathan é que esta decisão de Bernoulli, seguida de amostragem do resíduo na rejeição, preserva a distribuição do verificador exatamente.

> `u`É um número de vezes.`q_prob`É probabilidade de um testador a um token de projecto.`p_prob`O teorema Leviathan indica que, além da rejeição da análise de residuos, a distribuição dos testadores pode ser assegurada.

### Passo 2: distribuição residual

```python
def residual_dist(q, p):
    raw = [max(0.0, qi - pi) for qi, pi in zip(q, p)]
    s = sum(raw)
    return [r / s for r in raw]
```

Subtrair`p`de`q`- A partir de um elemento, apertar os valores negativos para zero, renormalizá-los.

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              `q`减去 `p`, vai cortar o valor negativo para zero, reintegrar.

### Passo 3: um passo especulativo

```python
def spec_step(prefix, q_model, p_model, N, rng):
    drafts = []
    p_probs = []
    ctx = list(prefix)
    for _ in range(N):
        p_dist = p_model(ctx)
        d = sample(p_dist, rng)
        drafts.append(d)
        p_probs.append(p_dist[d])
        ctx.append(d)

    q_dists = [q_model(prefix + drafts[:i]) for i in range(N + 1)]

    for i, d in enumerate(drafts):
        u = rng.random()
        q_prob = q_dists[i][d]
        p_prob = p_probs[i]
        if u < min(1.0, q_prob / p_prob if p_prob > 0 else float("inf")):
            prefix = prefix + [d]
        else:
            res = residual_dist(q_dists[i], p_model(prefix))
            prefix = prefix + [sample(res, rng)]
            return prefix
    prefix = prefix + [sample(q_dists[N], rng)]
    return prefix
```

Cinco aceitos → um bônus → seis tokens produzidos em um passe de verificação.

> 五个被接受 → 一个奖励 → 一次验证器通行产生六个代币──

### Passo 4: medir a taxa de aceitação

Execute 10.000 passos especulativos em diferentes níveis de qualidade do esboço. Taxa de aceitação do esboço versus divergência KL entre distribuições do esboço e verificador. Você deve ver uma relação monótona limpa.

> Em diferentes projectos de qualidade, executar 10.000 vezes.

### Passo 5: verificar a equivalência da distribuição

Empiricamente: o histograma de tokens produzido pelo loop especulativo deve corresponder ao histograma produzido pela amostragem diretamente do verificador. Este é o teorema Leviathan na prática. Um teste de chi-quadrado confirma dentro do erro de amostragem.

> 经验上: O símbolo do ciclo de sugestão deve ser combinado com o mesmo de um testador.

## Use-o com o framework implementado.

Produção:

> Produção:

```bash
# vLLM with EAGLE
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model /models/llama-3.1-eagle-70b \
    --speculative-draft-tensor-parallel-size 1 \
    --num-speculative-tokens 5

# vLLM with vanilla draft model
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model meta-llama/Llama-3.2-1B-Instruct \
    --num-speculative-tokens 5
```

TensorRT-LLM tem a rota mais rápida de Medusa a partir de meados de 2026. `faster-whisper`Envolve a descodificação especulativa para Whisper-large com um pequeno rascunho.

> TensorRT-LLM terá o caminho mais rápido para Medusa em 2026`faster-whisper`Por que não é que eu não sei?

**Picking a draft:**

> **选择草案策略：**

| Strategy | When to pick | Speedup |
|----------|--------------|---------|
| 策略 | 何时选择 | 加速比 |
| Vanilla draft (1B/3B Llama family) | Fast prototype, no training | 1.8–2.3× |
| 朴素草案（1B/3B Llama 系列） | 快速原型，无需训练 | 1.8–2.3× |
| Medusa heads | You can fine-tune the verifier | 2–3× |
| Medusa 头 | 可以微调验证器 | 2–3× |
| EAGLE-2 / 3 | Production, max speed | 3–4× |
| EAGLE-2 / 3 | 生产环境，最大速度 | 3–4× |
| Lookahead | No draft, no training, no extra params | 1.3–1.6× |
| 前瞻 | 无草案，无训练，无额外参数 | 1.3–1.6× |

**When NOT to spec-decode:**

> **何时不使用推测解码：**

- Geração de sequência única de 15 tokens.
  Chinese: 1-5 tokens 单序列生成──开销占主导──
- Amostragem de alta temperatura / extremamente criativa (a)
  Tradução do inglês: altitude (高温采样)
- Deploições com restrições de memória (modelo de projeto adiciona VRAM).
  Tradução do inglês para o inglês:

## Envia-o . Produto .

Veja .`outputs/skill-spec-decode-picker.md`A habilidade escolhe uma estratégia de descodificação especulativa (vanilha / Medusa / EAGLE / lookhead) e parâmetros de sintonia (N, temperatura de rascunho) para uma nova carga de trabalho de inferência.

> 参见 `outputs/skill-spec-decode-picker.md`△ Esta habilidade é utilizada para a criação de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de novas estratégias de desenvolvimento e desenvolvimento de desenvolvimento.

## Exercícios.

1. **Easy.**Corra .`code/main.py`Confirmar que a distribuição especulativa de tokens corresponde à distribuição direta de amostras do verificador em 50.000 tokens dentro de p = 0,05 por quadrado de chi.
   Tradução: 运行`code/main.py` Confirmar em 50 000 tokens, distribuir tokens de sugestão e testes distribuídos em testes de cartão p > 0,05 dentro de correspondência.
2. **Medium.**A aceleração da trama (tokens por modelo grande para frente) como função de `N`Para`α = 0.5, 0.7, 0.85`Identificar o óptimo .`N`para cada α. (Punta: tokens esperados por chamada de verificação = `(1 - α^{N+1}) / (1 - α)`.)
   Tradução: `α = 0.5, 0.7, 0.85`时加速比( por grande modelo de símbolo`N`                                                                                                                                                                                                                                                              `N`◊                                                                                                                                                                                                                                                              `(1 - α^{N+1}) / (1 - α)`◊)
3. **Hard.**Implementar uma pequena Medusa: pegue o GPT da lição 14, adicione 3 cabeças de LM extras que prevejam posições t+2, t+3, t+4. Treine em mini-shakespeare com uma perda conjunta de várias cabeças. Compare as taxas de aceitação versus um esboço de vainilha feito truncando o mesmo modelo.
   Tradução do inglês para tradução do inglês para inglês: implementing a small Medusa: take the 14th 课的 GPT 毕业项目, add 3 额外的 LM 头预测位置 t+2、t+3、t+4──用联合多头损失在小小小小小小小小小中学上训──比较与截断相同模型得到的简单草案的接受率──
4. **Hard.**Implementar o rollback: comece com um prefixo KV de 10 tokens, entre 5 tokens de rascunho, simule uma rejeição na posição 3. Verifique se a leitura do cache corresponde corretamente ao "prefixo + os primeiros 2 rascunhos aceitos" na próxima iteração.
   Chinese:实现回滚:从10 token 的前 KV 缓存开始,输入5 个草案令牌,模拟位置3 的拒绝――验证你的缓存读取在下次代时正确匹配"前 + 前2 个已接受草案"――

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Draft model | "The cheap one" | A smaller model that proposes candidate tokens; usually 10–50× cheaper than the verifier. |
| 草案模型 | "便宜的那个" | 提出候选 token 的较小模型；通常比验证器便宜 10-50 倍。 |
| Verifier | "The big one" | The target model whose distribution we preserve; runs once per speculative step. |
| 验证器 | "大的那个" | 我们要保持其分布的目标模型；每次推测步骤运行一次。 |
| Acceptance rate (α) | "How often the draft is right" | Per-token probability that the verifier accepts the draft. 0.7–0.9 typical. |
| 接受率 (α) | "草案正确的频率" | 验证器接受草案的每 token 概率。典型值 0.7-0.9。 |
| Residual distribution | "The rejection fallback" | `(q - p)_+` normalized; sampling from this on rejection preserves the verifier's distribution. |
| 残差分布 | "拒绝时的后备方案" | `(q - p)_+` 归一化；拒绝时从中采样保持验证器的分布。 |
| Bonus token | "The free one" | When all N drafts accepted, sample one more from the verifier's next-step distribution. |
| 奖励 token | "免费的那个" | 当所有 N 个草案被接受时，从验证器的下一步分布中多采样一个。 |
| Medusa | "Draft-less speculative" | Multiple LM heads on the verifier predict positions t+1..t+k in parallel. |
| Medusa | "无草案推测" | 验证器上的多个 LM 头并行预测位置 t+1..t+k。 |
| EAGLE | "Hidden-state draft" | Tiny transformer draft conditioned on the verifier's last-layer hidden states. |
| EAGLE | "隐藏状态草案" | 以验证器最后一层隐藏状态为条件的小型 Transformer 草案。 |
| Lookahead decoding | "Jacobi iteration" | Self-speculation using a fixed-point iteration; no draft model. |
| 前瞻解码 | "Jacobi 迭代" | 使用不动点迭代的自推测；无需草案模型。 |
| Tree attention | "Verify many candidates at once" | Branching verification that considers several draft continuations simultaneously. |
| 树注意力 | "同时验证多个候选" | 同时考虑多个草案续写的分支验证。 |
| KV rollback | "Undo rejected drafts" | Scratch KV buffer; commit on acceptance, discard on reject. |
| KV 回滚 | "撤销被拒绝的草案" | 临时 KV 缓冲区；接受时提交，拒绝时丢弃。 |

## Mais leitura 延伸阅读

- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) o algoritmo central e o teorema da equivalência.
  Tradução do inglês para o inglês: 推测解码的核心算法和等价定理论文──
- [Chen et al. (2023). Accelerating Large Language Model Decoding with Speculative Sampling](https://arxiv.org/abs/2302.01318) introdução simultânea; prova limpa de rejeição de Bernoulli.
  Tradução do inglês: simultáneamente publicado; claro de Bernúli rejeitar a prova.
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) Papel Medusa; verificação da atenção à árvore.
  O que é que é o "conhecimento" de uma pessoa?
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) EAGLE-1; projecto de estado oculto.
  Tradução do inglês para o inglês:Eagle-1
- [Li et al. (2024). EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees](https://arxiv.org/abs/2406.16858) AGLE-2; profundidade dinâmica da árvore.
  Tradução do português:Eagle-2 论文;动态树深度──
- [Li et al. (2025). EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test](https://arxiv.org/abs/2503.01840)- A Eagle-3.
  Tradução do português:Eagle-3
- [Fu et al. (2024). Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](https://arxiv.org/abs/2402.02057)- Olhe para o lado de fora, não há estratégia.
  Tradução do inglês para tradução livre:
- [vLLM docs — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode.html) referência canónica de produção com as quatro estratégias ligadas.
  O que é que se passa com o sistema de controle de dados?
- [SafeAILab / EAGLE reference implementation](https://github.com/SafeAILab/EAGLE) o código de referência para a EAGLE-1/2/3.
  Tradução do inglês:Eagle-1/2/3
