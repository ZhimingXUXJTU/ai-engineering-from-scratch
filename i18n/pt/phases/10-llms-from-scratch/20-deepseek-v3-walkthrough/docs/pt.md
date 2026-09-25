# Processo de Arquitetura de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Processo de Pro

> Fase 10 · Lição 14 nomeou os seis botões arquitetônicos que cada modelo aberto vira. DeepSeek-V3 (dezembro de 2024, 671B parâmetros totais, 37B ativo) vira todos os seis e adiciona mais quatro: Atenção Latente Multi-Head, equilíbrio de carga auxiliar sem perda, Predicção Multi-Token e treinamento DualPipe. Esta lição lê a arquitetura do DeepSeek-V3 de cima para baixo e deriva cada contagem de parâmetros da configuração publicada. No final, você pode explicar por que a taxa 671B/37B é a aposta certa e por que MLA + MoE juntos vencem sozinhos na fronteira.

> **【中文解读】**DeepSeek-V3(2024年12月,671B 总参数,37B 激活) transformou todas as seis estruturas 旋并新增四个:MLA(多头潜在注意力) 无辅助负载均衡、MTP(多代币 预测) 双管训练──671B/37B Proporção significa que cada sugestão só activa 5,5% de parâmetros──

> **【拓展：DeepSeek架构→开源大模型】**DeepSeek-V3 é uma das principais grandes estruturas de modelos de 2024-2025. MLA vai comprimir o cache KV para 1/10, MoE 让671B 模型只耗耗37B的推理成本―― compreender esta estrutura é a chave para entender a China AI 实验室在大模型领域突破――

> - Não .**【前置】**學本節前请先掌握:Fase 10·14(Open Models Architecture) 6 个架构旋概览;Fase 10·15-19 全部(EGLE、Diff Attention、NSA、MTP、DualPipe) DeepSeek-V3 de cada inovação。本节把它们组装在一起,是Fase 10 后半段的综合──
> - Não .**【类比】**DeepSeek-V3 = "六边形战士"把 2024 年所有前沿优化全堆上:MLA(省 KV cache) 、MoE(省推理算力) 、MTP(送投机解码) 、DualPipe(省训练通信) 、NSA(省长上下文算力) ∼671B 总参数但每次只激活37B(5.5%), equivale a "funcional rica em armas suíças, mas apenas usando uma faca"―

**Type:** Learn
**Languages:** Python (stdlib, parameter calculator)
**Prerequisites:** Phase 10 · 14 (open-model walkthroughs), Phase 10 · 17 (NSA), Phase 10 · 18 (MTP), Phase 10 · 19 (DualPipe)
**Time:** ~75 minutes

## Objetivos de aprendizagem

- Leia a configuração DeepSeek-V3 de cima para baixo e explique cada campo em termos dos seis botões GPT-2 mais quatro adições específicas do DeepSeek.
  De início a fim ler Configuração do DeepSeek-V3, usando os seis giros do GPT-2 e quatro DeepSeek especiais para cada parágrafo
- Derivar a contagem total de parâmetros (671B), a contagem de parâmetros ativos (37B) e os componentes que contribuem para cada um.
  推导总参数(671B)、激活参数(37B) e sua composição
- Calcule a pegada de cache KV do MLA em contexto de 128k e compare com o que um modelo denso de paramétricos com GQA paga.
   calcular MLA em 128K  KV  cache ocupação, em relação ao modelo GQA  intenso de parâmetros de ativação iguais
- Indique as quatro inovações específicas do DeepSeek (MLA, MTP, roteamento auxiliar sem perda, DualPipe) e nomear qual parte da pilha de arquitetura/formação é alvo de cada uma delas.
  Explicar quatro elementos: DeepSeek, MLA, MTP, não-assistido, DualPipe) e suas respectivas estruturas/treinamento

## O problema é o problema da introdução

DeepSeek-V3 é o primeiro modelo aberto de fronteira cuja arquitetura é significativamente diferente da família Llama. Llama 3 405B é "GPT-2 com seis botões girados". DeepSeek-V3 é GPT-2 com todos os seis botões mais quatro. Ler a configuração Llama 3 é um aquecimento para ler a configuração DeepSeek, mas a estrutura profunda  a forma do bloco de atenção, a lógica de roteamento, o objetivo de treinamento  é diferente o suficiente para que você precise de uma passagem separada.

> DeepSeek-V3 é a primeira estrutura com a família Llama que tem diferenças substanciais de modelo. Llama 3 405B é "GPT-2 调整六旋"──DeepSeek-V3 é GPT-2 六旋 全调整再加四四个──阅读 Llama 3 configuração é a configuração de DeepSeek 配置热身, mas estrutura profunda 关注块的形状、路由逻辑训练时目标差异足够大,需要单独解读──

A rede de treinamento de 2026 está copiando a arquitetura. Entender que é uma mesa de apostas para qualquer papel que toque treinamento de LLM de fronteira ou inferência.

> Aprender os benefícios: a publicação do OpenWay de DeepSeek-V3 mudou o significado do modelo open source "frontfront ability". Sua estrutura é a duplicação de muitos planos de treinamento de 2026 em curso.

## O conceito central.

> **【中文解读】**DeepSeek-V3 é um dos modelos de código aberto mais influentes de 2024: 671B 总参数(37B 激活参数) de MoE 架构, com MLA(多头潜在注意力) comprimir KV-cache, com DualPipe 优化流水线并行, com cerca de 5600000 USD de custo de treinamento alcançando um desempenho de nível GPT-4.

> **【拓展：DeepSeek-V3 的经济性突破】**O custo de treinamento do DeepSeek-V3 é de apenas 560 milhões de dólares, aproximadamente 2.788M H800 GPU 小时, cerca de 1/18 do custo de treinamento do Llama 3 405B.


### O núcleo invariante, novamente

DeepSeek-V3 ainda é autoregressivo. Ele ainda apila blocos de decodificador. Cada bloco ainda tem atenção mais MLP mais dois RMSNorms. Ele ainda usa SwiGLU no MLP. Ele ainda usa RoPE. Pre-norma. Embedings ligados ao peso. A mesma linha de base como todos os Llama ou Mistral.

### A mudança: MLA em vez de GQA

A partir da fase 10 · 14 você sabe que o GQA reduz o cache KV dividindo K e V entre grupos de cabeças Q. A atenção latente multi-cabeça (MLA) vai mais longe: K e V são comprimidos em uma representação latente de baixo nível compartilhada (a `kv_lora_rank`O cache KV armazena apenas o latente  normalmente 512 flutuantes por token por camada, não 8 x 128 = 1024 flutuantes.

Em contexto de 128k, DeepSeek-V3 com MLA (um latente compartilhado `c^{KV}`por token por camada; K e V são ambos derivados deste latente através de projeções ascendentes que podem ser absorvidas no matmul subsequente):

```
kv_cache = num_layers * kv_lora_rank * max_seq_len * bytes_per_element
         = 61 * 512 * 131072 * 2
         = 7.6 GB
```

Uma linha de base hipotética de GQA (forma de Llama 3 70B, cabeças de 8 KV, cabeças de 128) pagaria:

```
kv_cache = 2 * 61 * 8 * 128 * 131072 * 2
         = 30.5 GB
```

O MLA é 4 vezes menor do que um cache GQA de estilo Llama-3-70B em contexto de 128k.

O tradeoff: MLA adiciona um passo de descompressão por computação de atenção (por cabeça). O cálculo extra é pequeno em comparação com a largura de banda salvada.

### A rota: equilíbrio de carga sem perda auxiliar

Os roteadores MoE decidem quais especialistas top-k processam cada token. Um roteador ingênuo concentra muito trabalho em alguns especialistas, deixando outros inativos.

O DeepSeek-V3 introduz um esquema auxiliar sem perdas.`e`- O que é o problema?`bias_e`Se estiver subcarregado, aumenta-o. Sem perdas adicionais. O treino permanece limpo.

Efeito sobre a perda principal: nenhuma medível. Efeito sobre a arquitetura do MoE: limpar, sem hiperparâmetro auxiliar de perda para ajustar.

### O MTP: formação mais densa + projecto livre

A partir da fase 10 · 18 você sabe que DeepSeek-V3 adiciona o módulo D=1 MTP que prevê o token duas posições à frente. Na inferência, o módulo treinado é reutilizado como um rascunho de decodificação especulativa com aceitação de 80%+.

Parâmetros: 14B em cima do 671B principal.

### O treinamento: DualPipe

A partir da fase 10 · 19 você sabe que DualPipe é um pipeline bidirecional que se sobrepõe para frente e para trás com pedaços de comunicações transversais. Na escala 2,048-H800 do DeepSeek-V3, ele recupera aproximadamente 245k horas de GPU que 1F1B teria perdido para bolhas de pipeline.

### A configuração, campo por campo

Aqui está a configuração DeepSeek-V3 (simplificada):

```
hidden_size: 7168
intermediate_size: 18432   (dense MLP hidden size, used on first few layers)
moe_intermediate_size: 2048 (expert MLP hidden size)
num_hidden_layers: 61
first_k_dense_layers: 3    (first 3 layers use dense MLP)
num_attention_heads: 128
num_key_value_heads: 128   (formally equal to num_heads under MLA, but
                           the real compression is in kv_lora_rank)
kv_lora_rank: 512          (MLA latent dimension)
num_experts: 256            (MoE expert count per block)
num_experts_per_tok: 8      (top-8 routing)
shared_experts: 1           (always-on shared expert per block)
max_position_embeddings: 163840
rope_theta: 10000.0
vocab_size: 129280
mtp_module: 1               (1 MTP module at depth 1)
```

Partilha:

- `hidden_size=7168`: dimensão de inserção.
- `num_hidden_layers=61`: profundidade total do bloco.
- `first_k_dense_layers=3`Os primeiros 3 blocos utilizam um MLP denso de tamanho 18432.
- `num_attention_heads=128`: 128 cabeças de consulta.
- `kv_lora_rank=512`: K e V são comprimidos para esta dimensão latente e descomprimidos por cabeça.
- `num_experts=256, num_experts_per_tok=8`Cada bloco do MoE tem 256 especialistas, rotas no topo-8.
- `shared_experts=1`Para além dos 256 especialistas enrutados, um especialista sempre presente contribui para cada token.
- `moe_intermediate_size=2048`A maior parte dos casos de PMA é de um tipo de PMA, mas o maior número de PMA é de um tipo de PMA.

### Contabilidade de parâmetros

O cálculo completo está em`code/main.py`O título:

- Incorporar: `vocab * hidden = 129280 * 7168 = ~0.93B`- Não .
- Os primeiros 3 blocos densos: atenção com MLA (~144M por bloco) + MLP denso (~260M por bloco) + normas.
- 58 blocos de MoE: atenção com MLA (~144M) + 256 especialistas cada um (30M cada) + 1 especialista compartilhado (30M) + norma. Total ~ 7,95B por bloco, incluindo todos os especialistas. 461B total para os 58 blocos de MoE.
- MTP: 14B.

O número de dados de DeepSeek é de 3 a 5% do valor publicado. O delta vem dos documentos de relatórios de contabilidade finos da DeepSeek no anexo 2 da Secção 2.

Parâmetros ativos por forward:

- Atenção: 144 M por camada * 61 = 8,8 B (todas as camadas de fogo).
- MLP ativo: as primeiras 3 camadas densas (3 * 260M = 780M), 58 camadas MoE cada ativo com 8 encaminhadas + 1 compartilhada + carga aérea de encaminhamento.
- Incorporar + normas: 1.2B.
- Total ativo: aproximadamente 26B núcleo + 14B MTP (treinado mas não sempre executado em inferência) ≈ 37B.

### A relação 671B / 37B

O DeepSeek-V3 é o modelo de MoE de fronteira mais escassa que tenha enviado pesos abertos. Mixtral 8x7B com a proporção 13/47 (28%) é muito mais denso. Llama 4 Maverick com a proporção 17B/400B (4.25%) é comparável. A aposta do DeepSeek: em escala de fronteira, mais especialistas com menor taxa de ativação produzem melhor qualidade por FLOP ativo.

### Onde fica o DeepSeek-V3

| Model | Total | Active | Ratio | Attention | Novel ideas |
|-------|------|-------|-------|-----------|-------------|
| Llama 3 70B | 70B | 70B | 100% | GQA 64/8 | — |
| Llama 4 Maverick | 400B | 17B | 4.25% | GQA | — |
| Mixtral 8x22B | 141B | 39B | 27% | GQA | — |
| DeepSeek V3 | 671B | 37B | 5.5% | MLA 512 | MLA + MTP + aux-free + DualPipe |
| Qwen 2.5 72B | 72B | 72B | 100% | GQA 64/8 | YaRN extension |

### A seguir: R1, V4

DeepSeek-R1 (2025) é uma corrida de treinamento de raciocínio na espinha dorsal V3. R1 usa a mesma arquitetura. O que mudou é a receita pós-treino (RL em grande escala em tarefas verificáveis), não a arquitetura pré-treino.

O DeepSeek-V4 (se for enviado) deve manter MLA + MoE + MTP e adicionar DSA (DeepSeek Sparse Attention), o sucessor da NSA da Fase 10 · 17.


> **【拓展：DeepSeek-V3 的 MoE 架构细节】**DeepSeek-V3 tem 256 routes de especialistas, ativando 8 por vez, mais 1 especialista em compartilhamento.


## Use-o com o framework implementado.
```figure
moe-routing
```

## Usá-lo

`code/main.py`É a calculadora de parâmetros especializada na forma do DeepSeek-V3.

O que ver:

- Contagem total de parâmetros vs. 671B publicado.
- Contagem de parâmetros ativos vs. publicado 37B.
- O cache KV em contexto de 128k  a comparação MLA vs GQA.
- Desagregação por camada para ver onde o orçamento de parâmetros realmente vai.

## Envia-o . Produto .

Esta lição produz`outputs/skill-deepseek-v3-reader.md`. Dado um modelo da família DeepSeek (V3, R1 ou qualquer variante futura), ele produz uma leitura de arquitetura componente por componente que nomeia cada campo da configuração, deriva os números de parâmetros por componente e identifica quais das quatro inovações específicas do DeepSeek o modelo usa.

> 本课产 出 `outputs/skill-deepseek-v3-reader.md`△ dado DeepSeek 系列模型 ((V3、R1 或任何未来变体), ele produz por componentes de estrutura de interpretação, nomeação de cada parágrafo, por componentes de indução de parâmetros,并识别模型 utilizou quatro DeepSeek 特定创新中的哪些──

## Exercícios.

1. Corra .`code/main.py`- Compare a estimativa do parâmetro total da calculadora com a 671B publicada e identifique a origem do delta.
   Tradução: 运行`code/main.py` A avaliação dos parâmetros gerais do calculador com a comparação publicada com 671B, encontrando a origem da diferença.

2. Modifique a configuração para usar MLA rank 256 em vez de 512. Calcule o tamanho do cache KV resultante em contexto de 128k. Que redução percentual compra e a que custo para a expressividade por cabeça?
   Modificação de configuração usando MLA 秩 256 em vez de 512──计算 128K 上下文下 KV 缓存大小──节省了多少百分比,代价是什么?

3. Compare o roteamento do DeepSeek-V3 (256 especialistas, top-8) com uma variante hipotética (512 especialistas, top-8). Os parâmetros totais crescem; os parâmetros ativos permanecem iguais. O que a capacidade de especialistas extra compra em teoria, e quanto custa na inferência?
   Chinese translation: comparar DeepSeek-V3 de(256 专家,top-8) 路由与假设的(512 专家,top-8) 变体──总参数增长;激活参数不变──额外专家容量理论上买到了什么,推理时代价是什么?

4. Leia a Seção 2.1 do relatório técnico DeepSeek-V3 (arXiv:2412.19437) sobre MLA. Explique em três frases por que as matrizes de descompressão K e V podem ser "absorvidas" no matmul subsequente para a eficiência de tempo de inferência.
   Tradução em chinês:read DeepSeek-V3 技术报告第 2.1 节关于MLA的内容.

5. DeepSeek-V3 usa treinamento FP8 para a maioria das operações. Calcule a economia de memória de FP8 vs BF16 para armazenar os pesos 671B. Como isso se cruza com o orçamento de treinamento de tokens 14.8T?

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| MLA | "Multi-Head Latent Attention" | Compress K and V into a shared low-rank latent (kv_lora_rank, typically 512), decompress per head on-the-fly; KV cache stores only the latent | 多头潜在注意力，将 K/V 压缩为共享低秩潜在向量 |
| kv_lora_rank | "MLA compression dim" | The size of the shared latent for K and V; DeepSeek-V3 uses 512 | MLA 压缩维度，DeepSeek-V3 使用 512 |
| First k dense layers | "Early layers stay dense" | The first few MoE-model layers skip the MoE router and run a dense MLP for stability | 前 k 层保持密集，跳过 MoE 路由保证稳定性 |
| num_experts_per_tok | "Top-k routing" | How many routed experts fire per token; DeepSeek-V3 uses 8 | 每 token 激活专家数，DeepSeek-V3 使用 8 |
| Shared experts | "Always-on experts" | Experts that process every token regardless of routing; DeepSeek-V3 uses 1 | 共享专家，每个 token 都经过的专家 |
| Auxiliary-loss-free routing | "Bias-adjusted load balance" | Per-expert bias terms adjusted during training to keep expert load balanced without adding a loss term | 无辅助损失路由，用偏置项替代辅助损失做负载均衡 |
| MTP module | "Extra prediction head" | Transformer block predicting t+2 from h^(1) and E(t+1); denser training, free speculative-decoding draft | MTP 模块，多 token 预测头 |
| DualPipe | "Bidirectional pipeline" | Training schedule that overlaps forward/backward compute with cross-node all-to-all | DualPipe，双向流水线调度 |
| Active parameter ratio | "Sparsity" | active_params / total_params; DeepSeek-V3 hits 5.5% | 激活参数比，DeepSeek-V3 仅 5.5% |
| FP8 training | "8-bit training" | Training storage and many compute ops in FP8; roughly halves memory vs BF16 at a small quality cost | FP8 训练，8 位训练节省约一半显存 |

## Mais leitura 延伸阅读

- [DeepSeek-AI — DeepSeek-V3 Technical Report (arXiv:2412.19437)](https://arxiv.org/abs/2412.19437) o documento completo de arquitetura, formação e resultados
- [DeepSeek-V3 model card on Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V3) arquivos de configuração e notas de implantação
- [DeepSeek-V2 paper (arXiv:2405.04434)](https://arxiv.org/abs/2405.04434) o antecessor que introduziu MLA
- [DeepSeek-R1 paper (arXiv:2501.12948)](https://arxiv.org/abs/2501.12948) o sucessor de formação de raciocínio na arquitetura do V3
- [Native Sparse Attention (arXiv:2502.11089)](https://arxiv.org/abs/2502.11089) a direcção futura da atenção da família DeepSeek
- [DualPipe repository](https://github.com/deepseek-ai/DualPipe) a referência ao calendário de formação
