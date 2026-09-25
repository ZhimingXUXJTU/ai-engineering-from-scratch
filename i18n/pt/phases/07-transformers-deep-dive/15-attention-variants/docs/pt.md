# Atenção Variantes  Janela deslizante, Sparse, Diferencial  Atenção  Janela deslizante 稀疏 差分注意力

> A atenção total é um círculo. Cada token vê cada token, e a memória paga o preço.

> **【中文解读】**O método de redução da complexidade é o método de redução da complexidade.

**Type:** Hands-on | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head), Phase 7 · 12 (KV Cache / Flash Attention) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head), Phase 7 · 12 (KV Cache / Flash Attention)
**Time:** ~60 minutes | **时间:** ~60 分钟

## O problema é o problema da introdução

Custos de atenção total `O(N²)`Memória e `O(N²)`Para um Llama 3 70B de 128K de contexto que é 16 bilhões de entradas de atenção por camada, vezes 80 camadas.`O(N²)`Memória de ativação, mas não altera o custo aritmético  cada token ainda atende a cada outro token.

> A atenção total é para a memória e o custo de cálculo na duração da sequência.`O(N²)`Para 128K, é o Llama 3 70B, é 160 bilhões de notas de atenção por camada, multiplicadas por 80 camadas.`O(N²)`De ativar a memória, mas não alterar o custo de cálculo cada token  ainda se preocupar em cada outro token 

Três classes de variantes mudam a topologia da própria matriz de atenção:

> Três tipos de variação alteraram a estrutura da própria matriz de atenção:

1. **Sliding window attention (SWA).**Cada token atende a uma janela fixa de vizinhos, não o prefixo completo.`O(N · W)`onde`W`Gemma 2/3, as primeiras camadas do Mistral 7B, Phi-3-Long.
   Tradução:**滑动窗口注意力 (SWA)。**Cada token se concentra apenas no domínio vizinho da janela fixa, e não no anterior completo.`O(N · W)`, entre os `W`É uma grande janela. Gemma 2/3
2. **Sparse / block attention.**Apenas pares selecionados `(i, j)`O resto é forçado a zero peso. Longformer, BigBird, OpenAI transformador esparso.
   Tradução:**稀疏/块注意力。**只有选定的 `(i, j)`À avaliação; o restante é forçado a zero peso.
3. **Differential attention.**Compute dois mapas de atenção com projeções Q/K separadas, subtraia um do outro. Mata o "sink de atenção" que sangra o peso dos primeiros tokens.
   Tradução:**差分注意力。**Utilizando Q/K independente 投影计算两个注意力图,将一个从另一个减去―― eliminar将权重汇聚到前几个代币的"注意力汇聚"现象――Microsoft's DIFF Transformer(2024)。

Estes coexistem. Um modelo de fronteira de 2026 muitas vezes os mistura: a maioria das camadas são SWA-1024, cada quinta é atenção global completa, e um punhado são cabeças diferenciais que limpam a recuperação.

> Eles podem coexistir. Um modelo de vanguarda de 2026 é geralmente usado em combinação: a maioria das camadas é SWA-1024, cada cinco camadas é a atenção total do ensino, uma pequena parte é a diferença entre as pesquisas de limpeza e a atenção geral.

> **【中文解读】**三种降低注意力复杂度的方法:(1) 滑窗口(SWA) 只关注局部邻域,O(N*W) 复杂度;(2) 稀疏/块注意力只计算选的代币对;(3) 差分注意力两组 Q/K 注意力相减,消除"注意力汇聚"现象──2026年模型通常混合使用这些变体──

## O conceito central.

### Atenção à janela deslizante (SWA)

Cada consulta em posição `i`Assegura apenas posições em `[i - W, i]`(SWA causal) ou `[i - W/2, i + W/2]`Os tokens fora da janela vão ficar`-inf`na matriz de pontuação.

> - O que é ?`i`Todas as consultas são apenas preocupadas.`[i - W, i]`(因果 SWA) ou `[i - W/2, i + W/2]`(双向) posição dentro do âmbito.`-inf`- Não.

```
full causal:           sliding window (W=4):
positions 0-7          positions 0-7, W=4
    0 1 2 3 4 5 6 7        0 1 2 3 4 5 6 7
0 | x                0 |  x
1 | x x              1 |  x x
2 | x x x            2 |  x x x
3 | x x x x          3 |  x x x x
4 | x x x x x        4 |    x x x x
5 | x x x x x x      5 |      x x x x
6 | x x x x x x x    6 |        x x x x
7 | x x x x x x x x  7 |          x x x x
```

Para o`N = 8192`E ...`W = 1024`, a matriz de pontuação tem 1024 × 8192 linhas não-zero na expectativa  uma redução de 8 ×.

> Para o`N = 8192`和 `W = 1024`O número de rotas de divisão de 1024 × 8192 não-zero-lines foi reduzido 8 vezes.

**KV cache shrinks with SWA.**Só o último .`W`Para uma configuração Gemma-3-ish (1024 janela, contexto 128K), o cache KV cai 128x.

> **KV 缓存随 SWA 缩小。**Cada camada só precisa de manter o final do K e V.`W`个 token──对于类 Gemma-3 的配置(1024 窗口,128K 上下文),KV 缓存减少 128 倍──

**Quality cost.**Os transformadores SWA-somente lutam com a recuperação de longo alcance. A solução: intercalar camadas SWA com camadas de atenção plena. Gemma 3 usa 5:1 SWA: global. Mistral 7B usou uma pilha de SWA causal onde a informação "flui para a frente" através de janelas sobrepostas  cada camada estende o campo receptivo efetivo por `W`, e depois`L`camadas que o modelo pode participar `L × W`- Os tokens de volta.

> **质量代价。**純 SWA Transformer 在长距离检索上表现不佳──修复方案:将 SWA 层与全注意层交换使用──Gemma 3 使用 5:1 的 SWA:全局比例──Mistral 7B 使用因果 SWA 堆,信息通过重叠窗口"向前流动"每层将有效感受野扩展`W`- Não .`L`层后模型可以追溯 `L × W`- Não.

### Atenção de pouca / bloqueio

Escolha um .`N × N`Patrão de esparcia antecipado.

> 预先选择 `N × N`O que é um tipo de "classical"

- **Local + strided (OpenAI sparse transformer).**Atender ao último .`W`Tokens mais cada `stride`- O símbolo anterior, capta tanto local como de longo alcance.`O(N · sqrt(N))`Computação.
  Tradução:**局部 + 步进（OpenAI 稀疏 Transformer）。**关注最后 `W`- Sim , sim . - Sim , sim .`stride`- Não, não.`O(N · sqrt(N))`de calcular quantidade de informação local e de longa distância.
- **Longformer / BigBird.**Janela local + um pequeno conjunto de tokens globais (por exemplo `[CLS]`O conteúdo empírico 2x com qualidade correspondente.
  Tradução:**Longformer / BigBird。**局部窗口 + 少量全局 token (também conhecido como`[CLS]`O estudo mostrou que a produção de todos os tokens se expandiu 2 vezes sob a mesma qualidade.
- **Native Sparse Attention (DeepSeek, 2025).**Saiba quais blocos de `(Q, K)`- Não há bloqueio zero no núcleo.
  Tradução:**原生稀疏注意力（DeepSeek，2025）。**Aprender o que é que é?`(Q, K)`块重要;在内核级别跳过零块──与 FlashAttention 兼容──

A atenção escassa é uma história de engenharia de kernel. A matemática é simples (mascarar a matriz de pontuação); a vitória vem de nunca carregar as entradas zero no SRAM. FlashAttention-3 e a API 2026 FlexAttention fazem padrões escassos personalizados de primeira classe no PyTorch.

> 稀疏注意力 (RAR) é uma história de engenharia nuclear. A matemática é muito simples.

> **【拓展：滑动窗口的信息传递机制】**滑窗注意力看似只能捕获局部信息,但通过多层堆叠,信息可以"透透"到更远的位置──W 窗窗的L 层注意力,有效感受野为L×W──例如 W=1024、L=32 的模型有效感受野为32K token──Mistral 7B 正正是利用这个特性在保持O(N*W) 计算复杂性同时实现长上下文建模──

### Atenção Diferencial (Transformador DIFF, 2024)

A atenção regular tem um problema de "desintoxicação da atenção": softmax força cada linha a somar a 1, então os tokens que não querem atender a nada em particular despejam peso no primeiro token (ou os primeiros).

> 標準注意力有"注意力汇聚"問題:softmax 强制每行总和为 1,所以不想关注任何特定内容的代币会重权倾倾倒到第一代币(或前几个) ;; Isso roubou a capacidade de contenção que deveria ser usada para o conteúdo real。

A atenção diferencial corrige isto computacional .**two**mapas de atenção e subtração:

> 差分注意力 através do cálculo**两个**Nota:

```
A1 = softmax(Q1 K1^T / √d)
A2 = softmax(Q2 K2^T / √d)
DiffAttn = (A1 - λ · A2) V
```

onde`λ`A1 capta pesos reais de conteúdo; A2 capta o lavatório. A subtração cancela o lavatório, realoca o peso para tokens relevantes.

> Entre eles `λ`A1 捕获真实内容权重; A2 捕获汇聚──相减消除汇聚,将权重重新分配到相关代币──

Resultados relatados (Microsoft 2024): 510% menor perplexidade, contexto eficaz 1,52× mais longo no mesmo comprimento treinado, recuperação mais nítida de agulha em palha de feno.

> 報告結果(Microsoft 2024):困惑度降低 5-10%,同训长度下有效上下文长度增加1.5-2倍,agulha-em-haystack 检索更精确──

> **【中文解读】**差分注意力创新之处: 标准注意力因软max 归归化导致"注意力汇聚" (Attenção sumida) 不相关的代币 把重重集中在序列开头的代币上。差分注意力计算两组注意力并相减,A1 捕获真实内容权重,A2 捕获汇聚噪音,相减后消除汇聚现象──困惑度降低 5-10%──

> **【拓展：Gemma 3 的混合注意力策略】**O Google Gemma 3 usa 5:1 de deslizante janela com proporção de atenção global para cada 5 níveis de atenção local para 1 nível de atenção global para 1 nível de atenção global para Google. Isto mantém a capacidade de construção do longo e baixo nível de dados, além de reduzir significativamente o custo de cálculo.

### Comparação variável

| Variant | Compute | KV cache | Quality vs full | Production use |
|---------|---------|----------|-----------------|----------------|
| 变体 | 计算量 | KV 缓存 | 相对全注意力的质量 | 生产使用 |
| Full attention | O(N²) | O(N) per layer | baseline | every model's default layer |
| 全注意力 | O(N²) | 每层 O(N) | 基线 | 每个模型的默认层 |
| SWA (window 1024) | O(N·W) | O(W) per layer | -0.1 ppl, good with global layers | Gemma 2/3, Phi-3-Long |
| 滑动窗口 (窗口 1024) | O(N·W) | 每层 O(W) | -0.1 ppl，配合全局层效果好 | Gemma 2/3, Phi-3-Long |
| Local + strided sparse | O(N·√N) | mixed | similar to SWA | OpenAI sparse transformer, Longformer |
| 局部+步进稀疏 | O(N·√N) | 混合 | 类似 SWA | OpenAI 稀疏 Transformer, Longformer |
| BigBird (local + global + random) | O(N) approx | mixed | matches full at 2× context | early long-context BERT |
| BigBird (局部+全局+随机) | O(N) 近似 | 混合 | 2 倍上下文下匹配全注意力 | 早期长上下文 BERT |
| Native Sparse (DeepSeek-V3.2) | O(N · active fraction) | O(N) | within 0.05 ppl | DeepSeek-V3.2, 2025 |
| 原生稀疏 (DeepSeek-V3.2) | O(N · 活跃比例) | O(N) | 0.05 ppl 以内 | DeepSeek-V3.2, 2025 |
| Differential | O(2·N²) | O(2N) | -5 to -10% ppl | DIFF Transformer, early 2026 models |
| 差分 | O(2·N²) | O(2N) | 困惑度降低 5-10% | DIFF Transformer, 2026 早期模型 |

## Construí-lo e realizei-o.
```figure
gqa-kv-sharing
```

## Construí-lo

Veja .`code/main.py`Implementamos um comparador de máscaras causais que mostra atenção completa, SWA, local+strided e diferencial lado a lado numa sequência de brinquedos.

> 参见 `code/main.py` Nós realizamos um comparador de ocultação de efeitos, que mostra a atenção total SWA local + progresso e diferença 

### Passo 1: máscara causal completa (linha de base)

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

Linha de base da lição 07. Triangular inferior; peso zero acima da diagonal.

> 第 07 课的基线──下三角;对角线上权重为零──

### Passo 2: Máquina de deslizar a janela

```python
def swa_mask(n, window):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
    return M
```

Um parâmetro  `window`- Para o ...`window >= n`Recuperamos a atenção causal completa.`window = 1`Cada token serve apenas a si mesmo.

> Um parâmetro`window`- Não.`window >= n`时, recuperação para todo o efeito atenção.`window = 1`Cada um só se preocupa com si mesmo.

### Passo 3: local + mascarinha esporádica

```python
def strided_mask(n, window, stride):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
        for j in range(0, i + 1, stride):
            M[i][j] = 0.0
    return M
```

Janela local densa mais cada `stride`O campo receptor cresce em etapas de registro com camadas adicionais.

> O espaço é limitado a partir da linha de entrada.`stride`个标志──感受野随着层次的增长以对数步长的增长──

### Passo 4: atenção diferenciada

```python
def diff_attention(Q1, K1, Q2, K2, V, lam):
    A1 = softmax_causal(Q1 @ K1.T / sqrt_d)
    A2 = softmax_causal(Q2 @ K2.T / sqrt_d)
    return (A1 - lam * A2) @ V
```

Em dois passos de atenção, subtrair com um coeficiente de mistura aprendido. No código comparamos o mapa de calor de atenção-sincação de único versus diferencial e observamos o colapso do sinca.

>  2o cálculo da atenção, usando a combinação de fatores de redução aprendidos.

### Passo 5: Tamanhos do cache KV

Imprimir o tamanho do cache por camada em `N = 131072`A diferença é de 10 a 100 vezes, o que significa que a diferença é de 2 a 5 vezes, e que a diferença é de 2 a 5 vezes.

> - Não .`N = 131072`时每种变体每层缓存大小──SWA 和稀疏变体减少10-100 倍──差分变体翻倍──要有意识地管理你的内存开销──

## Use-o com o framework implementado.

Padrões de produção de 2026:

> Modelo de produção de 2026:

```python
from transformers import AutoModelForCausalLM
# Gemma 3 mixes SWA (window=1024) and global layers at 5:1.
model = AutoModelForCausalLM.from_pretrained("google/gemma-3-27b-it")
# print(model.config.sliding_window, model.config.layer_types)
```

FlexAttention em PyTorch 2.5+ aceita uma função de máscara:

> PyTorch 2.5+ 中的 FlexAttention  aceitar função de masquerado:

```python
from torch.nn.attention.flex_attention import flex_attention, create_block_mask

def swa_pattern(b, h, q_idx, kv_idx):
    return (q_idx - kv_idx < 1024) & (q_idx >= kv_idx)

mask = create_block_mask(swa_pattern, B=batch, H=heads, Q_LEN=n, KV_LEN=n)
out = flex_attention(q, k, v, block_mask=mask)
```

Isso se compilou para um kernel Triton personalizado. Dentro de 10% da velocidade FlashAttention-3 para padrões comuns, e a função de máscara é um Python chamada.

> Esta se traduzirá para auto-definir Triton 内核── para o modo comum, a velocidade está dentro de 10% do FlashAttention-3, e a função de masquerade é um Python objeto ajustavel──

**When to pick each:**

> **何时选择每种变体：**

- **Pure full attention** cada camada até ~ 16K contexto, ou quando a qualidade de recuperação é primordial.
  Tradução:**纯全注意力** Cada camada é usada até cerca de 16K em cima e baixo, ou inspeção de qualidade.
- **SWA + global mix** longo contexto (> 32K), formação e inferência ligada à memória.
  Tradução:**SWA + 全局混合** 长上下文(>32K), treinamento e sugestão 內存约束──32K acima de 2026 anos默认配置──
- **Sparse block attention** kernel personalizado, padrão personalizado. Reservado para cargas de trabalho especializadas (recuperar, áudio).
  Tradução:**稀疏块注意力** 自定义内核,自定义模式──专用于特殊工作负载(检索、音频)──
- **Differential attention** qualquer carga de trabalho em que a contaminação do sumidouro de atenção dói (RAG de longo contexto, agulha em manto de feno).
  Tradução:**差分注意力** Atenção ao nível da população em que se encontra a contaminação (controle de dados)

## Envia-o . Produto .

Veja .`outputs/skill-attention-variant-picker.md`A competência seleciona uma topologia de atenção para um novo modelo, dada a extensão do contexto-alvo, as exigências de recuperação e o perfil de computação de formação/inferência.

> 参见 `outputs/skill-attention-variant-picker.md` Esta habilidade  baseada no objetivo  a procura de necessidades e treinamento / cálculo de configuração, para o novo modelo escolher atenção 

## Exercícios.

1. **Easy.**Corra .`code/main.py`Verificar o SWA em`window=4`- Verifica tudo fora dos últimos 4 tokens por linha.`window=n`Reproduz a atenção causal completa de forma bit-identical.
   Tradução: 运行`code/main.py`❖ O teste `window=4`A SWA vai colocar todo o conteúdo fora dos últimos 4 tokens para cada linha.`window=n`能逐位复现全因果注意力──
2. **Medium.**Implementar a SWA causal com `window=1024`Treinar por 1000 passos no Tinyshakespeare, quanto é a perda de valor contra a atenção plena?
   Tradução do inglês: 文中译:在第07 课毕业项目上实现`window=1024`O resultado é SWA. Em minisshakespeare, 1000 passos.
3. **Hard.**Implemente uma mistura de camadas 5:1 de estilo Gemma-3 (5 SWA, 1 global) no modelo de pedra angular. Comparar perda, memória e qualidade de geração contra linhas de base de SWA pura e global pura em parâmetros correspondentes.
   Tradução do inglês para inglês: In the implementation of the class Gemma-3's 5:1-layer mix (in the final version of the class Gemma-3), em tradução livre:
4. **Hard.**Implementar a atenção diferenciada com um aprendiz `λ`A formação de um trabalho de recuperação sintética (uma agulha, 2.000 distractores).
   Tradução do inglês: implementar cada um tem aprendizagem`λ`A diferença de atenção em uma tarefa de pesquisa sintética (a) é de aproximadamente 2.000 pontos (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a pesquisa de dados (a) para a) para a pesquisa de dados (a) para o que se comparar.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Sliding window attention (SWA) | "Local attention" | Each query attends to its last `W` tokens; KV cache shrinks to `O(W)`. |
| 滑动窗口注意力 (SWA) | "局部注意力" | 每个查询关注其最后 `W` 个 token；KV 缓存缩小到 `O(W)`。 |
| Effective receptive field | "How far back the model sees" | In an `L`-layer SWA stack with window `W`, up to `L × W` tokens. |
| 有效感受野 | "模型能看多远" | 在 `L` 层 SWA 堆栈中，窗口 `W`，最多 `L × W` 个 token。 |
| Longformer / BigBird | "Local + global + random" | Sparse patterns with a few always-attending global tokens; early long-context approach. |
| Longformer / BigBird | "局部+全局+随机" | 带少量始终关注的全局 token 的稀疏模式；早期长上下文方案。 |
| Native Sparse Attention | "DeepSeek's kernel trick" | Learn block-level sparsity; skip zero blocks at the kernel level while keeping quality. |
| 原生稀疏注意力 | "DeepSeek 的内核技巧" | 学习块级稀疏性；在内核级别跳过零块同时保持质量。 |
| Differential attention | "Two maps, one subtracts" | DIFF Transformer: subtract a learned `λ` times a second attention map from the first to cancel attention sinks. |
| 差分注意力 | "两个图，一个相减" | DIFF Transformer：用第一个注意力图减去学习 `λ` 倍的第二个注意力图，消除注意力汇聚。 |
| Attention sink | "Weight bleeds to token 0" | Softmax normalization forces rows to sum to 1; uninformative queries dump weight on position 0. |
| 注意力汇聚 | "权重流向 token 0" | Softmax 归一化迫使每行总和为 1；无信息查询将权重倾倒到位置 0。 |
| FlexAttention | "Mask-as-Python" | PyTorch 2.5+ API that compiles arbitrary mask functions into FlashAttention-shape kernels. |
| FlexAttention | "掩码即 Python" | PyTorch 2.5+ API，将任意掩码函数编译为 FlashAttention 形式的内核。 |
| Layer type mix | "5:1 SWA-to-global" | Interleave sparse and full attention layers in a stack to keep quality at lower memory. |
| 层类型混合 | "5:1 SWA 与全局" | 在堆栈中交替使用稀疏和全注意力层，以较低内存保持质量。 |

## Mais leitura 延伸阅读

- [Beltagy, Peters, Cohan (2020). Longformer: The Long-Document Transformer](https://arxiv.org/abs/2004.05150) o papel de janela de deslizamento canônico + global-token.
  Tradução do inglês:Longformer 论文,经典的滑动窗口 + 全局 token 方案──
- [Zaheer et al. (2020). Big Bird: Transformers for Longer Sequences](https://arxiv.org/abs/2007.14062)Local + global + aleatório.
  Tradução do inglês: BigBird 论文,局部 + 全局 + 随机模式──
- [Child et al. (2019). Generating Long Sequences with Sparse Transformers](https://arxiv.org/abs/1904.10509) Modelo local+passo do OpenAI.
  Tradução do inglês para Chinês:OpenAI 稀疏 Transformer 论文,局部+步进模式──
- [Gemma Team (2024). Gemma 2: Improving Open Language Models at a Practical Size](https://arxiv.org/abs/2408.00118) a combinação global de 1:1 SWA.
  中文翻译:Gemma 2 论文,1:1 SWA 与全局混合──
- [Gemma Team (2025). Gemma 3 technical report](https://arxiv.org/abs/2503.19786) a mistura de 5:1 com a janela =1024 que é agora o manual padrão.
  中文翻译:Gemma 3 技术报告,5:1 混合,窗口=1024,现已成为教科书默认──
- [Ye et al. (2024). Differential Transformer](https://arxiv.org/abs/2410.05258) papel transformador DIFF.
  Tradução do português:DIFF Transformer
- [Yuan et al. (2025). Native Sparse Attention](https://arxiv.org/abs/2502.11089) A atenção de disparidade aprendida do DeepSeek-V3.2.
  O que é o "desenvolvimento" de um sistema de controle de dados?
- [PyTorch — FlexAttention blog and docs](https://pytorch.org/blog/flexattention/) Referência API para o padrão de mascaras como chamáveis em Use It.
  O que é um sistema de controle de dados?
