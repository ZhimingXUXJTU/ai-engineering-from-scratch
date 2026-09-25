# GPT  Modelagem de Língua Causal  GPT  因果语言模型

> O BERT vê ambos os lados. O GPT vê apenas o passado. A máscara triangular é a linha única mais consequente de código na IA moderna.

> **【中文解读】**GPT é um Transformador de apenas Decodificador, usando o factor mask码 (因果掩码) para evitar ver o futuro de tokens.

**Type:** Hands-on | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

Um modelo de linguagem responde a uma pergunta: dada a primeira `t-1`Tokens, qual é a distribuição de probabilidade sobre token `t`Treinar nesse sinal  previsão de tokens próximos  e você obtém um modelo que pode gerar texto arbitrário um token por vez.

> 语言模型回答一个问题:给定前 `t-1`- Não, não.`t`Em este sinal 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测

Para treiná-lo de ponta a ponta em uma sequência inteira em paralelo, você precisa que a previsão de cada posição dependa apenas de posições anteriores.

> Para treinar em toda a sequência de ponta a ponta, você precisa prever cada posição dependendo apenas da posição anterior.

A máscara causal faz isto. É uma única matriz triangular superior de`-inf`Os valores adicionados às pontuações de atenção antes do softmax. Depois do softmax, essas posições se tornam 0. Cada posição pode atender apenas a si mesma e posições anteriores.

> O resultado ocorre. É uma rectangular de três ângulos.`-inf`值), adicionado ao softmax 之前的注意分数上──softmax 后, estas posições se alteram para 0── cada posição só pode se concentrar em si mesma及之前的位置──因为 só é aplicada uma vez a toda a sequência, então uma vez para frente se pode transmitir para obter o próximo token 预测── N 个并行的下一个代号.

GPT-1 (2018), GPT-2 (2019), GPT-3 (2020), GPT-4 (2023), GPT-5 (2024), Claude, Llama, Qwen, Mistral, DeepSeek, Kimi  são todos transformadores causais apenas de decodificação com o mesmo ciclo central. Apenas maiores, melhores dados e melhor RLHF.
GPT-1 (2018), GPT-2 (2019), GPT-3 (2020), GPT-4 (2023), GPT-5 (2025), Claude, Llama, Qwen, Mistral, DeepSeek, Kimi  são todos transformadores causais apenas de decodificação com o mesmo ciclo central. O que os separa são a qualidade de dados, escala e refinamentos arquitetônicos, e pós-treinamento (SFT, RLHF, DPO e seus sucessores).

> GPT-1(2018)、GPT-2(2019)、GPT-3(2020)、GPT-4(2023)、GPT-5(2024)、Claude、Llama、Qwen、Mistral、DeepSeek、Kimi

> **【中文解读】**O efeito oculto é a linha mais importante de código da IA moderna. Em uma linha de três esquinas, o valor inf ), adicionado ao número de pontos de atenção, o softmax é o ponto de ocultação de 0 para cada posição.

## O conceito central.

![Causal mask creates a triangular attention matrix](../assets/causal-attention.svg)

### A máscara .

Dada uma sequência de comprimento `N`, construir um`N × N`Matriz:

> 给定长度为 `N`De acordo com o artigo, a`N × N`- Não .

```
M[i, j] = 0       if j <= i
M[i, j] = -inf    if j > i
```

Adicionar`M`para os resultados de atenção antes do softmax. `exp(-inf) = 0`Cada linha da matriz de atenção é uma distribuição de probabilidade sobre posições anteriores apenas.

> - Não .`M`Adição ao softmax  anterior                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `exp(-inf) = 0`, portanto, o peso da posição oculta é zero. Cada linha da matriz de atenção é apenas uma distribuição de probabilidade na posição anterior.

Custos de execução: 1 `torch.tril()`Tempo de cálculo: nanossegundos. Impacto no campo: tudo.

> 实现成本:一行 `torch.tril()`调用――计算时间:纳秒级―― impacto sobre todo o campo: mudaram tudo――
### De onde vem o triângulo

A máscara é geralmente apresentada como um parche embulado na atenção. Execute a derivação na outra direção e ela deixa de ser misteriosa: a atenção é o terceiro refinamento de uma média de prefixo, e o triângulo é os limites de ciclo dessa média, escrito como uma matriz.

**Stage 1 — prefix average.**O resumo causal mais estúpido de uma sequência: posição .`i`torna-se o meio das posições `0…i`Como um ciclo, isto é.`out[i] = X[:i+1].mean(0)`O mesmo cálculo é uma matriz multiplicar. Tome uma matriz triangular inferior de um, divide cada linha pelo seu conteúdo, multiplicar:

```python
import numpy as np

A = np.tril(np.ones((n, n)))
A = A / A.sum(axis=1, keepdims=True)
out = A @ X
```

- Em linha .`i`de`A`É o que é`[1/(i+1), …, 1/(i+1), 0, …, 0]`Os zeros acima da diagonal são a causalidade. Nada sobre o futuro foi mascarado; o futuro nunca foi na soma.

**Stage 2 — learned weights.**Uma média uniforme trata cada token passado como igualmente relevante.`S`. Agora as linhas não mais somam a uma por construção, então normalizar cada linha com softmax em vez de dividir pelo conteúdo. Softmax nunca sai um zero exato, o que quebra a causalidade  a menos que as pontuações futuras entrem como `-inf`, porque`exp(-inf) = 0`- Não .

```python
def softmax(x, axis):
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)

S = S + np.triu(np.full((n, n), -np.inf), k=1)
A = softmax(S, axis=1)
out = A @ X
```

O mesmo triângulo, a mesma matriz de fila-estocástica, o mesmo matmul.`-inf`Mas masque não é uma nova máquina. é zero entradas de estágio 1, traduzido para o domínio de entrada de softmax.

**Stage 3 — content-dependent weights.**Na fase 2, `S`O resultado é fixado após o treino: a posição 7 pesa sempre a mesma posição 3, independentemente do que os tokens digam.`S = Q @ K.T / sqrt(d_k)`Mascara, softmax, matmul  são idênticos.

Três estágios, uma invariante: uma matriz de fila-estocástica triangular inferior vezes a sequência. média uniforme, pesos estáticos aprendidos, pesos dependentes do conteúdo. A máscara nunca foi adicionada à atenção.

```figure
mask-derivation
```

### Formação paralela, inferência em série

Formação: avançar o conjunto `(N, d_model)`Sequência uma vez, calcular N perdas de entropia cruzada (um por posição), soma, backprop. Paralelas ao longo da sequência. É por isso que as escalas de treinamento GPT  você processar 1M tokens em um lote em uma passagem de GPU.

> 訓練:对整体 `(N, d_model)`序列做一次前向传播,计算 N 个交叉损失(每个位置一个),求和,反向传播──沿序列并行──这是GPT 训练可扩展的原因一次GPU通行就能处理批量中的1M 个代币──

Inferência: você gera token por token.`[t1, t2, t3]`- Não .`t4`- Alimentação .`[t1, t2, t3, t4]`- Não .`t5`- Alimentação .`[t1, t2, t3, t4, t5]`- Não .`t6`O cache KV (Lessão 12) salva os estados ocultos de `t1…tn`Então, você não os recompõe a cada passo. Mas profundidade serial na inferência = comprimento de saída. Isso é o imposto autoregressivo e por que a decodificação é o gargalo de latência de cada LLM.

> 推理: cada token 生成──输入 `[t1, t2, t3]`- Não .`t4` Introdução`[t1, t2, t3, t4]`- Não .`t5` Introdução`[t1, t2, t3, t4, t5]`- Não .`t6`;;KV 缓存;;第 12 课) guardado `t1…tn`O estado oculto, evitar cada passo repetindo o cálculo. Mas, ao fazer o cálculo, a profundidade da linha = a saída de longo prazo.

### A perda  mudança por uma

Dados tokens `[t1, t2, t3, t4]`- Não .

> - Não .`[t1, t2, t3, t4]`- Não .

- - Introdução:`[t1, t2, t3]`
  Tradução:`[t1, t2, t3]`
- Objetivos: `[t2, t3, t4]`
  Tradução do português:`[t2, t3, t4]`

Para cada posição .`i`, computação `-log P(target_i | inputs[:i+1])`Esta é a entropia cruzada para toda a sequência.

> Para cada posição .`i`, calcular `-log P(target_i | inputs[:i+1])`求和── é o ponto de intersecção de toda a sequência──

Todos os transformadores LM que já ouviram falar de trens nesta perda.

> Todos os modelos de linguagem transformadores que você já ouviu estão treinados nesta perda.

> **【拓展：Teacher Forcing 与暴露偏差】**GPT trenagem usando professor forçando cada passo para inserir o verdadeiro  primeiro token, e não o próprio modelo.

### Estratégias de decodificação

Após o treino, as escolhas de amostragem são mais importantes do que as pessoas pensam.

> Depois de concluído o treino, a escolha de estratégias de seleção é mais importante do que as pessoas imaginam.

| Method | What it does | When to use |
|--------|--------------|-------------|
| 方法 | 功能 | 适用场景 |
| Greedy | Argmax every step | Deterministic tasks, code completion |
| 贪心 | 每步取最大值 | 确定性任务、代码补全 |
| Temperature | Divide logits by T, sample | Creative tasks, higher T = more diversity |
| 温度 | 将 logits 除以 T 后采样 | 创意任务，T 越高多样性越大 |
| Top-k | Sample from top-k tokens only | Kills low-probability tails |
| Top-k | 只从概率最高的 k 个 token 采样 | 消除低概率尾部 |
| Top-p (nucleus) | Sample from smallest set with cumulative prob ≥ p | 2020+ default; adapts to distribution shape |
| Top-p（核采样） | 从累积概率 ≥ p 的最小集合中采样 | 2020+ 默认策略；自适应分布形状 |
| Min-p | Keep tokens with `p > min_p * max_p` | 2024+; better at rejecting long tails than top-p |
| Min-p | 保留 `p > min_p * max_p` 的 token | 2024+；比 top-p 更好地拒绝长尾 |
| Speculative decoding | Draft model proposes N tokens, big model verifies | 2–3× latency reduction at same quality |
| 推测解码 | 草案模型提出 N 个 token，大模型验证 | 相同质量下延迟降低 2-3 倍 |

Em 2026, min-p + temperatura 0,7 é um padrão razoável para modelos de pesos abertos.

> Em 2026, a temperatura min-p + 0,7 é a configuração racional do modelo de código aberto.

> **【中文解读】**解码策略的选择直接影响生成质量──贪心搜索(argmax) Adaptação à tarefa de determinação, temperatura采样增加多样性,top-p/min-p 截断低概率尾部──2026 年的推默认:min-p + temperatura 0,7,比传统的top-p 能更好地处理分布的度变化──

> **【拓展：从 GPT-2 到 GPT-4 的规模跳跃】**GPT-2(1.5B 参数)→ GPT-3(175B)→ GPT-4(A estimativa de 1,8T MoE) na escala salta, a estrutura muda muito pequena, mas a melhoria dos dados e métodos de treinamento é enorme.

### O que fez com que a "receita GPT" funcionasse

1. **Decoder-only.**Sem codificador, uma passagem de atenção + FFN por camada.
   Tradução:**解码器专用。**Não há código de vendas.
2. **Scaling.**124M → 1.5B → 175B → trilhões. As leis da escala Chinchilla (Lessão 13) dizem-lhe como gastar computação.
   Tradução:**规模扩展。**De 124M a 1,5B a 175B, novamente a mil milhões de parametros.
3. **In-context learning.**Surgiu em torno de 6B13B. O modelo pode seguir alguns exemplos de tiros sem ajuste fino.
   Tradução:**上下文学习。**约在 6B-13B 参数时涌现――模型无需微调就能遵循少样本示例――
4. **RLHF.**O pós-treinamento sobre preferências humanas transformou texto bruto pré-treinado em assistentes de chat.
   Tradução:**RLHF。**O texto do treinamento preliminar original será traduzido em assistente de diálogo.
5. **Pre-norm + RoPE + SwiGLU.**Treinamento estável em escala.
   Tradução:**Pre-norm + RoPE + SwiGLU。**Massas de treinamento de estabilidade.

A arquitetura do núcleo não mudou muito desde o GPT-2. Tudo o interessante aconteceu em dados, escala e pós-treino.

> Desde o GPT-2, a estrutura central não mudou muito. Todas as coisas interessantes acontecem em termos de dados, escala e treinamento posterior.

> **【中文解读】**Elemento de sucesso do GPT: Simplicidade e escala de arquitetura apenas em decodificador (de 124M a milhões de parâmetros)                                                                                                                                                                                                                                             

> **【拓展：自回归生成的推理瓶颈】**O GPT é um sistema de produção que é geralmente mais complexo e mais eficaz em termos de desenvolvimento.

## Construí-lo e realizei-o.
```figure
causal-mask
```

## Construí-lo

### Passo 1: a máscara causal

Veja .`code/main.py`Um único liner:

> 参见 `code/main.py`一行代码:

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

Adicione-o aos resultados de atenção antes do Softmax.

> Aumentar a suavidade máxima                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

### Passo 2: modelo de GPT de duas camadas

Aponta dois blocos de decodificador (auto-atenção mascarada + FFN, sem atenção cruzada). Adicione um embedding token, uma codificação posicional e um unembedding (ligado à matriz de embedding token  um truque padrão desde GPT-2).

> 堆叠两个解码器块(掩码自注意力 + FFN,无交叉注意力) ・・・添加代币 嵌入、位置编码和反嵌入(与代币 嵌入矩阵绑定GPT-2 以来标准技巧) ・・・

### Passo 3: previsão do próximo token, de ponta a ponta

Em um vocabulário de brinquedo de 20 tokens, produzir logits em cada posição. Calcule a perda de entropia cruzada contra o alvo de deslocamento por um.

> Em 20 tokens de jogo, em cada posição gerar logits.

### Passo 4: amostragem

Implementar ganância, temperatura, top-k, top-p, min-p. Execute cada um em um prompt fixo e compare as saídas. Uma função de amostragem é de 10 linhas.

> 实现贪心、温度、top-k、top-p、min-p 采样──在固定提示上分别运行并比较输出──一采样函数只需要10 行代码──

## Use-o com o framework implementado.

PyTorch, 2026 Idioma:

> PyTorch, 2026 ano de uso habitual

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")

prompt = "Attention is all you need because"
inputs = tok(prompt, return_tensors="pt")
out = model.generate(
    **inputs,
    max_new_tokens=64,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
)
print(tok.decode(out[0]))
```

Sob o capô,`generate()`executa o passado para a frente, puxa os logits da posição final, amostra o token seguinte, anexa-o e repete. Cada stack de inferência LLM de produção (vLLM, TensorRT-LLM, llama.cpp, Ollama, MLX) implementa o mesmo loop com otimização pesada  preenchimento em lote, batch contínuo, pagamento em cache KV, decodificação especulativa.

> No fundo,`generate()`运行前向传播,取出最后位置的logits,采样下一个代币,追加到序列中,重复──每个生产 LLM 推理(vLLM、TensorRT-LLM、llama.cpp、Ollama、MLX) são usados em grande quantidade de otimização para realizar o mesmo ciclo批量预填、连续批处理、KV 缓存分页、推测解码──

**GPT vs BERT, one line each:**Previsões do GPT `P(x_t | x_{<t})`- O BERT prevê .`P(x_masked | x_unmasked)`A perda determina se o modelo pode gerar.

> **GPT 与 BERT 各一句话：**GPT 预测 `P(x_t | x_{<t})`BERT 预测 `P(x_masked | x_unmasked)`                                                                                                                                                                                                                                                              

## Envia-o . Produto .

Veja .`outputs/skill-sampling-tuner.md`A habilidade seleciona parâmetros de amostragem para uma tarefa de nova geração e indica quando é necessária a decodificação determinista.

> 参见 `outputs/skill-sampling-tuner.md` Esta habilidade é utilizada para a seleção de parâmetros de novas tarefas de geração, e marca quando é necessário determinar a sua solução.

## Exercícios.

1. **Easy.**Corra .`code/main.py`Verificar que a matriz de atenção causal é triangular inferior após softmax.
   Tradução: 运行`code/main.py`, verificação de factor de atenção em suavemax 后是下三角的──抽查:
2. **Medium.**Compare perplexidade de beam-4 vs avarice em 10 instruções curtas.
   Em 10 短提示上比较束搜索和贪心搜索的困惑度──束搜索一定要好些吗?
3. **Hard.**Implementar decodificação especulativa: usar um modelo de 2 camadas minúsculas como rascunho e um modelo de 6 camadas como verificador.
   Tradução do inglês para tradução do inglês: implementing推测解码: using 2 层小模型作为草案模型,6 层模型作为验证器──在 100 长度为 64 的补充上测量实际加速比──确认输出与验证器的贪心解码一致──

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Causal mask | "The triangle" | Upper-triangular `-inf` matrix added to attention scores so position `i` only sees positions `≤ i`. |
| 因果掩码 | "三角矩阵" | 加到注意力分数上的上三角 `-inf` 矩阵，使位置 `i` 只能看到位置 `≤ i`。 |
| Next-token prediction | "The loss" | Cross-entropy of the model's distribution against the true next token at every position. |
| 下一个 token 预测 | "损失函数" | 模型分布与每个位置真实下一个 token 之间的交叉熵。 |
| Autoregressive | "Generate one at a time" | Feed output back as input; parallelism only during training, not during generation. |
| 自回归 | "逐个生成" | 将输出反馈为输入；仅在训练时并行，生成时不并行。 |
| Logits | "Pre-softmax scores" | Raw output of the LM head before softmax; sampling happens on these. |
| Logits | "softmax 前的分数" | LM 头在 softmax 之前的原始输出；采样基于这些值。 |
| Temperature | "Creativity knob" | Divide logits by T; T→0 = greedy, T→∞ = uniform. |
| 温度 | "创造力旋钮" | 将 logits 除以 T；T→0 为贪心，T→∞ 为均匀分布。 |
| Top-p | "Nucleus sampling" | Truncate distribution to smallest set summing to ≥p; sample from what remains. |
| Top-p | "核采样" | 将分布截断为累积概率 ≥ p 的最小集合；从剩余部分采样。 |
| Min-p | "Better than top-p" | Keep tokens where `p ≥ min_p × max_p`; adapts cutoff to sharpness of distribution. |
| Min-p | "比 top-p 更好" | 保留 `p ≥ min_p × max_p` 的 token；根据分布锐度自适应调整截断。 |
| Speculative decoding | "Draft + verify" | Cheap model proposes N tokens; big model verifies in parallel. |
| 推测解码 | "草案+验证" | 廉价模型提出 N 个 token；大模型并行验证。 |
| Teacher forcing | "Training trick" | During training, feed the true previous token, not the model's prediction. Standard for every seq2seq LM. |
| Teacher forcing | "训练技巧" | 训练时输入真实的前一个 token，而非模型的预测。所有 seq2seq 语言模型的标准做法。 |

## Mais leitura 延伸阅读

- [Radford et al. (2018). Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)GPT-1.
  Tradução do português:GPT-1
- [Radford et al. (2019). Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)GPT-2.
  Tradução do português:GPT-2
- [Brown et al. (2020). Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) GPT-3 e aprendizagem no contexto.
  Tradução do inglês para o português:GPT-3 和上下文学习论文──
- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192)Papel de descodificação de especificações.
  Tradução do português:
- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) código de referência canônico causal-LM.
  中文翻译:HuggingFace Llama 因果语言模型参考代码──
