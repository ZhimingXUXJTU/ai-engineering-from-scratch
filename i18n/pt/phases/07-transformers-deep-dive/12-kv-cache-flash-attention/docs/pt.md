# KV Cache, Flash Attention & Inference Optimization.

> O treinamento é paralelo e ligado ao FLOP. A inferência é serial e ligada à memória.

> **【中文解读】**KV Cache 缓存已计算的钥匙/值 避免重复计算,是LLM 推理加速的核心──Flash Attention 优化显存访问模式,减少显存使用──

**Type:** Hands-on | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

Um descodificador autoregressivo ingênuo faz .`O(N²)`trabalho para gerar `N`Tokens: em cada passo recalcula a atenção sobre o prefixo completo. Para uma resposta de token 4K que é 16M operações de atenção, a maioria delas redundantes. Cada estado oculto de um token prefixo é determinista uma vez calculado.

> Um simples gerador de código de auto-regresso.`N`- Não .`O(N²)`Para a resposta do token 4K, é 16M vezes de atenção operação, a maior parte dos quais é redundante. Cada estado oculto do token anterior uma vez que o cálculo é de certeza, você só precisa usar as perguntas do novo token e todos os valores e chaves do cache anterior para prestar atenção.

Além disso, a atenção em si move muitos dados. A atenção padrão materializa uma matriz de pontuação N×N, saída N×d softmax, saída final N×d  muita leitura e escrita para HBM. Para N≥2K, a atenção se torna limitada à memória antes de se tornar FLOP-bound.

> Além disso, a atenção em si deve mover uma grande quantidade de dados. A atenção padrão gerará N×N divisão de matrizes, N×d softmax, saída, N×d, saída final, quando o número de vezes de leitura de HBM é excessivo. Quando o N≥2K, a atenção se torna um flap antes de se tornar um flap.

Duas otimizações, ambas de Dao et al., empurraram a inferência de fronteira de "lento" para "rápido":

> 两个优化 ((都来自道 等人) 将前沿推理从"慢"推向"快":

1. **KV cache.**Armazenar os vetores K e V de cada token pré-fix. A atenção de cada novo token é uma consulta contra as chaves armazenadas em cache.`O(N²)`- Não .`O(N)`por fase de geração.
   Tradução:**KV 缓存。**存储每个前代币的K 和 V 向量──每个新代币的注意是对缓存键的一个查询──推理从每步 `O(N²)`降低到 `O(N)`- Não.
2. **Flash Attention.**Tire a computação de atenção para que a matriz completa N×N nunca atinja HBM. Todo softmax + matmul acontece na SRAM. 24× velocidade do relógio de parede em A100; 510× em H100 com FP8.
   Tradução:**Flash Attention。**Para calcular o cálculo de blocos, fazer com que a N×N 矩阵 completa nunca seja escrita em HBM。 todos os softmax + 矩阵乘法都在SRAM中完成──A100 上 2-4 倍加速;H100 上 FP8 可达 5-10 倍──

Em 2026, ambos são universais. Todas as pilhas de inferência de produção (vLLM, TensorRT-LLM, SGLang, llama.cpp) assumem-nos.

> Até 2026, ambos já foram utilizados em todos os modelos de produção.

> **【中文解读】**推理优化两大核心技术:KV Cache 存储已计算的钥匙/值向量,避免重复计算,将每步推理从O(N^2) 降至O(N);Flash Attention 通过分块计算避免 N×N矩阵写入HBM,完成所有计算在SRAM,速度提升2-10倍――

## O conceito central.

![KV cache growth and Flash Attention tiling](../assets/kv-cache-flash-attn.svg)

### Matemática do cache KV

Por camada de decodificador, por token, por cabeça:

> Cada nível de código, cada token, cada cabeça:

```
bytes_per_token_per_layer = 2 * d_head * dtype_size
                          ^
                          K and V
```

Para um modelo 7B com 32 camadas, 32 cabeças, d_head=128, fp16:

> Para o modelo 7B ((32 层、32 头、d_head=128、fp16):

```
per token per layer = 2 * 128 * 2 = 512 bytes
per token (32 layers) = 16 KB
per 32K context = 512 MB
```

> **【拓展：GQA 对 KV 缓存的影响】**GQA(Grouped-Query Attention) reduzirá o KV 头从n_heads 减少到n_kv_heads,直接等比例缩小 KV 缓存.

Para Llama 3 70B (80 camadas, d_head=128, GQA com 8 cabeças de KV):

> Para Llama 3 70B ((80 层、d_head=128、GQA 8 个 KV 头):

```
per token per layer = 2 * 8 * 128 * 2 = 4096 bytes (4 KB)
per 32K context = 10.4 GB
```

Esse 10 GB é o motivo pelo qual o Llama 3 70B em contexto 128K precisa da maioria de um A100 de 40 GB apenas para cache KV no tamanho de lote 1.

> Este 10 GB é o que faz com que o Llama 3 70B em 128K em baixo abaixo apenas KV 缓存( tamanho de lote 1) é necessário a maior parte de 40 GB A100 显存――

**GQA is the KV-cache win.**A MHA com 64 cabeças seria de 32 GB.

> **GQA 是 KV 缓存的胜利。**64 cabeças de MHA  necessita de 32 GB¬MLA  comprimir ainda mais¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬
Arraste as dimensões e observe o movimento do tamanho do cache. Empurre o comprimento da sequência ou batch para cima e veja a velocidade com que ele sopra além de uma única GPU:

```figure
kv-cache-sizer
```

### Atenção flash  o truque de tecelagem

Atenção padrão:

> 标准注意力:

```
S = Q @ K^T          (HBM read, N×N, HBM write)
P = softmax(S)       (HBM read, HBM write)
O = P @ V            (HBM read, HBM write)
```

Três viagens de ida e volta de HBM. Em H100, a largura de banda de HBM é de 3 TB/s; SRAM é de 30 TB/s. Cada viagem de HBM é um fator de 10 desaceleração versus manter tudo no chip.

> Três vezes HBM 往返── em H100 上, HBM 带宽是3TB/s;SRAM é 30TB/s── cada vez HBM 访问比在片保持所有数据慢10倍──

Atenção flash:

```
for each block of Q (tile size ~128 × 128):
    load Q_tile into SRAM
    for each block of K, V:
        load K_tile, V_tile into SRAM
        compute S_tile = Q_tile @ K_tile^T     (SRAM)
        running softmax aggregation             (SRAM)
        accumulate into O_tile                  (SRAM)
    write O_tile to HBM
```

Uma viagem de HBM por telha.`O(N²)`- Não .`O(N)`Passada para trás recalcula alguns valores da passada para frente em vez de armazená-los  outra vitória de memória.

> Cada telha, uma visita de HBM, o total de reservas.`O(N²)`- Desce para aqui .`O(N)`反向传播 从前向传播中重新计算某些价值而不是存储它们另一个内存优势

**Numerical trick.**Funcionamento de softmax mantém `(max, sum)`A atenção flash calcula a saída bit-identical para atenção padrão (modulo fp16 não-asociatividade).

> **数值技巧。**运行时 softmax 跨 tile 维护 `(max, sum)`Para, garantir que a integração final é precisa. Não é similar.

> **【中文解读】**Técnicas centrais da atenção flash: calcular a atenção em blocos de cálculo, completar softmax e matrizes multiplicadas em GPUs de rápida SRAM, evitar escrever a média de N×N em HBMs de baixa velocidade.

> **【拓展：vLLM 的 PagedAttention】**PagedAttention(vLLM) organizará KV 缓存 para "paginas" fixas de tamanho grande, semelhantes à "invasão" virtual de sistemas operacionais. Isto eliminou o problema de fragmentos de memória, permitindo que várias solicitações de desenvolvimento possam ser compartilhadas com GPU 显存――配合连续批处理(continuous batching), vLLM aumentará o volume de leitura do LLM 推理 2-4 vezes, tornando-se o quadro de leitura mais popular de 2024-2026.

**Version evolution:**

| Version | Year | Key change | Speedup on reference hardware |
|---------|------|-----------|-------------------------------|
| 版本 | 年份 | 关键变化 | 参考硬件上的加速 |
| Flash 1 | 2022 | Tiled SRAM kernel | 2× on A100 |
| Flash 2 | 2023 | Better parallelism, causal-first ordering | 3× on A100 |
| Flash 3 | 2024 | Hopper asynchrony, FP8 | 1.5–2× on H100 (~740 TFLOPs FP16) |
| Flash 4 | 2026 | Blackwell 5-stage pipeline, software exp2 | Inference-first (forward only initially) |

Flash 4 é avançado apenas no lançamento. O treinamento ainda usa Flash 3.

> Flash 4 发布时仅支持前向传播;;训练仍使用 Flash 3;; Flash 4 的 GQA 和变长支持待定(2026年中)。

### Descodagem especulativa  a outra vitória de latência

O modelo barato propõe N tokens. O modelo grande verifica todos os N em paralelo. Se a verificação aceita k tokens, você pagou 1 grande modelo pass para frente para k gerações.

> O modelo barato propõe N 个 token──大模型并行验证所有 N 个── Se a verificação aceita k 个 token, você obtém k 个生成──代码和散文的典型 k=3-5──

2026 padrões:
- **EAGLE 2 / Medusa.**cabeças de rascunho integradas que compartilham os estados ocultos do verificador. 23x aceleração sem perda de qualidade.
  Tradução:**EAGLE 2 / Medusa。**集成草案头, condição oculta do verificador.
- **Speculative decoding with draft model.**2×4x de aceleração no hardware do consumidor.
  Tradução:**带草案模型的推测解码。**O consumo de hardware aumenta de 2 a 4 vezes.
- **Lookahead decoding.**Iteração Jacobi, não é necessário um modelo de projeto.
  Tradução:**前瞻解码。**Jacobi 代;不需要草案模型──小众但免费──

### Batchagem contínua

Inferência em lote clássica: esperar a sequência mais lenta para terminar, e depois iniciar um novo lote.

> 经典批量推理: esperar pela sequência mais lenta terminar, então começar uma nova bateria.

Batchamento contínuo (primeiro enviado em Orca, agora em vLLM, TensorRT-LLM, SGLang): troca de novas solicitações no lote assim que os antigos terminam. 510x ganho de throughput para cargas de trabalho típicas de chat.

> 连续批处理(首次在Orca中发布,现在在vLLM、TensorRT-LLM、SGLang 中): antigo pedido concluído logo após o novo pedido de mudança em lote次;; típico chat chat 工作负载的吞吐量提升 5-10 倍;;

### PagedAttention  cache KV como memória virtual

O cache KV é alocado em blocos de 16 tokens; uma tabela de página mapeia posições lógicas para blocos físicos. Permite compartilhar KV em amostras paralelas (pesquisa de feixe, amostragem paralela), prefixos de troca de calor para cache rápida e memória de defragmentação. Melhoria de 4x de throughput em relação à alocação contígua ingênua.

> Características essenciais do vLLM: KV 缓存 distribuição de 16 blocos de tokens; página de mapa irá mapear a posição lógica para blocos físicos. Permitir trans-paradas de padrões.

## Construí-lo e realizei-o.
```figure
flash-attention-memory
```

## Construí-lo

Veja .`code/main.py`Implementamos:

> 参见 `code/main.py`❖ Nós realizamos:

1. Um ingênuo .`O(N²)`Decodificador incremental.
   Tradução do português:`O(N²)`- Não, não.
2. A.`O(N)`Descóderas em cache KV.
   Tradução: um`O(N)`KV 缓存解码器──
3. Um softmax de azulejos que simula o algoritmo de execução máxima da Flash Attention.
   Tradução do inglês: 模拟 Flash Attention 运行时最大值的分块软max──

### Passo 1: cache KV

```python
class KVCache:
    def __init__(self, n_layers, n_heads, d_head):
        self.K = [[[] for _ in range(n_heads)] for _ in range(n_layers)]
        self.V = [[[] for _ in range(n_heads)] for _ in range(n_layers)]

    def append(self, layer, head, k, v):
        self.K[layer][head].append(k)
        self.V[layer][head].append(v)

    def read(self, layer, head):
        return self.K[layer][head], self.V[layer][head]
```

Simples: continuar a crescer vetores por token K, V em listas por camada, por cabeça.

> 简单: continuamente adicionar cada token de K、V 向量─ na lista de cada nível.

### Passo 2: softmax de azulejos

```python
def tiled_softmax_dot(q, K, V, tile=4):
    """Flash-attention-style softmax(qK^T)V with running max/sum."""
    m = float("-inf")
    s = 0.0
    out = [0.0] * len(V[0])
    for start in range(0, len(K), tile):
        k_block = K[start:start + tile]
        v_block = V[start:start + tile]
        scores = [sum(qi * ki for qi, ki in zip(q, k)) for k in k_block]
        new_m = max(m, *scores)
        exp_old = math.exp(m - new_m) if m != float("-inf") else 0.0
        exp_new = [math.exp(sc - new_m) for sc in scores]
        s = s * exp_old + sum(exp_new)
        for j in range(len(out)):
            out[j] = out[j] * exp_old + sum(e * v[j] for e, v in zip(exp_new, v_block))
        m = new_m
    return [o / s for o in out]
```

Saída de bits idêntica a `softmax(qK) V`em um tiro, mas a qualquer momento o conjunto de trabalho é um `tile × d_head`Bloco, não o completo.`N × d_head`- Não .

> Com uma única vez`softmax(qK) V`O mesmo tipo de saída, mas qualquer momento, o trabalho é apenas um`tile × d_head`块, em vez de completo `N × d_head`- Não.

### Passo 3: Compare naívo versus decodificação em cache na geração de 100 tokens

Contar operações de atenção.`O(N²)`= 5050. em cache: `O(N)`O código imprime as duas.

> 計算注意力操作次数──朴素:`O(N²)`= 5050──缓存:`O(N)`= 100...

## Use-o com o framework implementado.

```python
# HuggingFace transformers auto-enables KV cache on decoder-only generate().
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",
    attn_implementation="flash_attention_2",  # use FA3 if Hopper
    torch_dtype="bfloat16",
)
# generate() uses KV cache automatically
```

Produção de VLLM:

> VLLM 生产部署:

```bash
pip install vllm
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --tensor-parallel-size 4 \
    --max-model-len 32768 \
    --enable-prefix-caching \
    --kv-cache-dtype fp8
```

O pré-acessamento de pré-contexto em todas as solicitações é um grande ganho de 2026  o mesmo sistema de prompt, alguns exemplos de tiros ou documento de contexto longo reutiliza KV em todas as chamadas. Para cargas de trabalho de agente com repetidas solicitações de ferramentas, o pré-acessamento de pré-contexto é rotineiramente ganho de throughput de 5x.

> 跨请求的前缓存是2026年重大胜利相同系统提示、少样本示例或长上下文文档在调用间重复使用 KV──对于有重复工具提示的代理工作负载,前缓存通常带来5倍吞吐量提升──

## Envia-o . Produto .

Veja .`outputs/skill-inference-optimizer.md`A habilidade escolhe implementação de atenção, estratégia de cache KV, quantização e decodificação especulativa para uma nova implantação de inferências.

> 参见 `outputs/skill-inference-optimizer.md` Esta habilidade é utilizada para a nova estratégia de avaliação do desenvolvimento de sistemas de gestão de dados, de gestão de dados, de gestão de dados e de avaliação de dados.

## Exercícios.

1. **Easy.**Corra .`code/main.py`- Confirmar que os decodificadores ingênuos e armazenados em cache produzem a mesma saída; observar a diferença de op-count.
   Tradução: 运行`code/main.py` Confirmar que o simples e o caché-descodificador produzem a mesma saída;
2. **Medium.**Implementar o caching de prefixos: dado um prompt P e várias conclusões, executar uma passagem para frente sobre P para preencher o cache KV, em seguida, ramificar por conclusão.
   Tradução do inglês para tradução do inglês: implementing pre缓存:给定提示 P 和多个补充,对P 运行一次前向传播填充 KV 缓存,然后每个补充分支――测量与每次重编码 P 相比的速度提升――
3. **Hard.**Implementar um brinquedo PagedAttention: KV cache em blocos fixos de 16 tokens com uma lista livre. Quando uma sequência terminar, devolva seus blocos ao pool. Simula 1000 conclusões de bate-papo com comprimentos variados. Compare fragmentação de memória versus alocação contígua.
   Chinese: 实现玩具版 PagedAttention:KV 缓存使用固定 16 token 块加空列表──序列完成时归归块──模拟 1,000 个变长聊天补全──相比较连续分配的内存碎片化差异──

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| KV cache | "The trick that makes decoding fast" | Stored K and V from every prefix token; new queries attend to them instead of recomputing. |
| KV 缓存 | "让解码变快的技巧" | 存储每个前缀 token 的 K 和 V；新查询对它们做注意力而非重新计算。 |
| HBM | "GPU main memory" | High Bandwidth Memory; 80 GB on H100, 192 GB on B200. ~3 TB/s bandwidth. |
| HBM | "GPU 主内存" | 高带宽内存；H100 上 80 GB，B200 上 192 GB。约 3 TB/s 带宽。 |
| SRAM | "On-chip memory" | Per-SM fast memory, ~256 KB per SM on H100. ~30 TB/s bandwidth. |
| SRAM | "片上内存" | 每 SM 的快速内存，H100 上每 SM 约 256 KB。约 30 TB/s 带宽。 |
| Flash Attention | "Tiled attention kernel" | Computes attention without materializing N×N in HBM. |
| Flash Attention | "分块注意力内核" | 不在 HBM 中生成 N×N 矩阵即完成注意力计算。 |
| Continuous batching | "No-wait batching" | Swap finished sequences out, new ones in, without draining the batch. |
| 连续批处理 | "无等待批处理" | 完成的序列换出，新的换入，无需排空批次。 |
| PagedAttention | "vLLM's headline" | KV cache allocated in fixed blocks with a page table; eliminates fragmentation. |
| PagedAttention | "vLLM 的核心特性" | KV 缓存以固定块分配加页表；消除碎片化。 |
| Prefix caching | "Reuse long prompts" | Cache KV for a shared prefix across requests; major cost cut for agents. |
| 前缀缓存 | "复用长提示" | 跨请求缓存共享前缀的 KV；代理场景大幅降低成本。 |
| Speculative decoding | "Draft + verify" | Cheap draft model proposes tokens; big model verifies k in one pass. |
| 推测解码 | "草案 + 验证" | 廉价草案模型提出 token；大模型一次验证 k 个。 |

## Mais leitura 延伸阅读

- [Dao et al. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135)Flash 1.
  Tradução do português:Flash Attention 1 论文。
- [Dao (2023). FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://arxiv.org/abs/2307.08691)Flash 2.
  Tradução do Novo Mundo:Flash Attention 2
- [Shah et al. (2024). FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](https://arxiv.org/abs/2407.08608)Flash 3.
  Tradução do Novo Mundo:Flash Attention 3
- [FlashAttention-4 release notes (Dao-AILab, 2026)](https://github.com/Dao-AILab/flash-attention) O pipeline de 5 etapas Blackwell e o truque de software-exp2; leia o repo README para as advertências de lançamento apenas para o futuro mencionadas nesta lição.
  Tradução do Novo Mundo:Flash Attention 4 发布说明;Blackwell 5 阶段管道和软件 exp2 技巧。
- [Kwon et al. (2023). Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180)- Papel de trabalho.
  中文翻译:vLLM PagedAttention 论文。
- [Leviathan et al. (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192)- Descodagem de especificações.
  Tradução do português:
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) O documento EAGLE-1/2 para a abordagem de projecto integrado que cita a lição.
  Tradução do inglês para o inglês:Eagle-1/2 论文,集成草案方法──
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) a abordagem Medusa referenciada ao lado da AGLE.
  Tradução do português: Medusa 论文,多解码头方法──
- [vLLM docs — PagedAttention](https://docs.vllm.ai/en/latest/design/kernel/paged_attention.html) o mergulho profundo canônico no bloco de 16 tokens e no design da tabela de páginas.
  中文翻译:vLLM PagedAttention 文档,16 token 块和页表设计的深入解析──
