# Mistura de Especialistas (MoE) 混合专家模型 (MoE)

> Um transformador 70B denso ativa todos os parâmetros para cada token. Um 671B MoE ativa apenas 37B por token e o supera em todos os benchmarks.

> **【中文解读】**MoE apenas ativa parte especialista de rede processando cada token, aumentando significativamente o número de parâmetros sem aumentar a quantidade de cálculo.

**Type:** Hands-on | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

A FLOP de um transformador denso na inferência é igual ao seu número de parâmetros ( vezes 2 para passar para frente). Escala um modelo denso e cada token paga a conta completa. Em 2024 a fronteira estava atingindo uma parede de computação: para ser significativamente mais inteligente, você precisava exponencialmente mais FLOPs por token.

> 密变压器 推理时的FLOPs等于其参数(前向传播乘以2);;扩大密模型意味着每个代币都应支付全部代价;; Até 2024, o modelo da vanguarda encontrou-se com a parede de cálculo: para se tornar mais inteligente, precisa de um índice de crescimento de cada token FLOPs;;

A mistura de especialistas rompe este vínculo.`E`Especialistas independentes + um roteador que escolha `k`- os parâmetros totais = `E × FFN_size`Parâmetros ativos por token = `k × FFN_size`. Configuração típica de 2026: `E=256`- Não .`k=8`- Escalas de armazenamento com `E`, calcular escalas com `k`- Não .

> O modelo de especialização mistura rompeu este vínculo.`E`个独立专家 + 一个路由器, cada token 选择 `k`个专家──总参数 = `E × FFN_size`◊ Número de elementos activos de cada token = `k × FFN_size`❖ Configuração típica de 2026:`E=256`- Não.`k=8` armazenamento`E`扩展,计算随 `k`扩展──

A fronteira de 2026 é quase inteiramente MoE: DeepSeek-V3 (671B total / 37B ativo), Mixtral 8×22B, Qwen2.5-MoE, Llama 4, Kimi K2, gpt-oss.

> A linha de frente do ano de 2026 é quase totalmente MoE:DeepSeek-V3(671B 总参数 / 37B 活跃) 、Mixtral 8×22B、Qwen2.5-MoE、Llama 4、Kimi K2、gpt-oss── em Artificial Analysis's Independent排行榜,排名前 10 开源模型都是 MoE──

> **【中文解读】**MoE  rompeu a equação de "parameto = 计算量" ⋅ cada FFN 层替换为 E 个独立专家 + 路由器, cada token apenas activa k 个专家──总参数随 E 增长,但每个 token 的计算量只随 k 增长── típico配置 E=256, k=8,存储随 E 缩缩,计算随 k 缩缩──这是2020s最重要的扩展思路──

> **【拓展：DeepSeek-V3 的 MoE 创新】**O DeepSeek-V3  possui 671B  parâmetros gerais, mas por token apenas ativa 37B através de 256 especialistas em roteiros + 1 especialista em partilha de implementação. Também introduziu uma estratégia de equilíbrio de carga sem perda de suporte, evitando o problema de colapso de roteiros tradicionais do MoE.

## O conceito central.

![MoE layer: router selects k of E experts per token](../assets/moe.svg)

### O swap FFN

Bloco de transformador denso:

> 密 Transformador 块:

```
h = x + attn(norm(x))
h = h + FFN(norm(h))
```

Bloco de MoE:

```
h = x + attn(norm(x))
scores = router(norm(h))              # (N_tokens, E)
top_k = argmax_k(scores)              # pick k of E per token
h = h + sum_{e in top_k}(
        gate(scores[e]) * Expert_e(norm(h))
    )
```

Cada especialista é um FFN independente (tipicamente SwiGLU). O roteador é uma única camada linear.`k`Expertos e obtém uma mistura fechada de suas saídas.

> Cada especialista é um FFN independente (normalmente SwiGLU) ⋅ routers é uma camada única ⋅ cada token  escolher o seu ⋅`k`个专家, obter os seus resultados em um mix control.

### O problema do equilíbrio de carga

Se o roteador colocar 90% dos tokens através do especialista 3, os outros especialistas morrem de fome.

> Se o routers distribuir 90% dos tokens para especialistas 3, outros especialistas vão "fome"

1. **Auxiliary load-balancing loss**Adicione uma penalidade proporcional à variação no uso especialista. Funciona, mas adiciona um hiperparâmetro e um segundo sinal de gradiente.
   Tradução:**辅助负载均衡损失**(Switch Transformer、Mixtral) ∼ Adição com especialistas de uso de diferença proporcional de punição── válida, mas aumentou o superparâmetro e o segundo grau de sinal──
2. **Expert capacity + token dropping**Cada perito é o máximo processado.`C × N/E`Tokens, tokens de sobreflow saltam a camada.
   Tradução:**专家容量 + token 丢弃**(Switch) ⋅ Cada especialista mais tratamento `C × N/E`O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é.
3. **Auxiliary-loss-free balancing**(DeepSeek-V3). Adicione um viés aprendido por perito especialista que muda a seleção top-k do roteador. Viés é atualizado fora da perda de treinamento.
   Tradução:**辅助损失无关均衡**(DeepSeek-V3)──Add a learning to of individual specialists bias, adjust the top-k choice of the router──paradoj em training loss, além de update── não contra o principal objetivo de施加惩罚──2024 anos grandes avanços──

A abordagem do DeepSeek-V3: após cada etapa de formação, para cada especialista, verifique se a sua utilização está acima ou abaixo do objetivo.`±γ`. Utilizações de selecção `scores + bias`As probabilidades de expertos usadas para gating são as principais .`scores`Desacoplamento do encaminhamento da expressão.

> Método de Profundos Buscadores: após cada etapa de treinamento, cada especialista verifica se o seu uso é superior ou inferior ao objetivo.`±γ`△ escolher usar `scores + bias` A probabilidade de especialistas em controle de entrada é original.`scores`将路由与表达解──

### Especialistas partilhados

O DeepSeek-V2/V3 também divide os especialistas em *shared* e *routed*. Cada token passa por todos os especialistas compartilhados. Os especialistas de roteamento são escolhidos através de top-k. Os especialistas compartilhados capturam conhecimento comum; os especialistas de roteamento se especializam. O V3 executa 1 especialista compartilhado mais o top-8 de 256 roteados.

> DeepSeek-V2/V3 também vai dividir os especialistas em duas categorias: *compartilhar* e *rourouway*.

### Especialistas em grãos finos

MoE clássico (GShard, Switch): cada especialista é tão largo quanto um FFN completo. `E`é pequeno (864), `k`é pequena (12).

> 经典 MoE(GShard、Switch): Cada especialista com FFN completo 一样宽──`E`较小(8-64),`k`较小(1-2)。

MoE moderno de grãos finos (DeepSeek-V3, Qwen-MoE): cada especialista é mais estreito (1/8 de tamanho FFN). `E`é grande (256+), `k`Os mesmos parâmetros totais, mas as combinações escalam muito mais rapidamente. `C(256, 8) = 400 trillion`A qualidade aumenta, a latência permanece estável.

> 现代细粒度 MoE(DeepSeek-V3、Qwen-MoE): cada especialista é mais estreito(1/8 FFN`E`较大(256+),`k`Também é maior (8+) ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅                                                                                                                                                                                                                                                       `C(256, 8) = 400 万亿`种可能的"专家"组合──质量提升,延迟不变──

> **【拓展：MoE 的路由崩塌问题】**O desafio central no treinamento do MoE é o colapso do roteiro (routeiro) rouuters poderão distribuir a maior parte dos tokens para uma pequena quantidade de especialistas, levando outros especialistas a não conseguirem treinar.

### Profil de custos

Por token, por camada:

> Cada token, cada camada:

| Config | Active params / token | Total params |
|--------|-----------------------|--------------|
| 配置 | 每个 token 活跃参数 | 总参数量 |
| Mixtral 8×22B | ~39B | 141B |
| Llama 3 70B (dense) | 70B | 70B |
| DeepSeek-V3 | 37B | 671B |
| Kimi K2 (MoE) | ~32B | 1T |

DeepSeek-V3 supera o Llama 3 70B (denso) em quase todos os índices de referência enquanto faz **fewer active FLOPs per token**Mais parâmetros = mais conhecimento. FLOPs mais ativos = mais computação por token.

> DeepSeek-V3 derrotou Llama 3 em quase todos os testes de base, ao mesmo tempo.**每个 token 的活跃 FLOPs 更少**△ Mais参数 = 更多知识──更多活跃 FLOPs = Cada token 更多计算──MoE 将两者解──

### A captura: memória

Todos os especialistas vivem em GPUs independentemente de qual deles disparar. Um modelo 671B precisa de ~1,3 TB de VRAM para pesos fp16.

> Todos os especialistas, independentemente de serem ativados, estão localizados no GPU. Um modelo 671B precisa de cerca de 1,3 TB de fp16 de peso de armazenamento.

> **【中文解读】**O peso central do MoE: com o cálculo de câmbio de memória. O DeepSeek-V3 alcança o desempenho de um modelo de 37B com um parâmetro ativo superior a 70B, mas requer 1,3TB de armazenamento de armazenamento de dados.

> **【拓展：细粒度专家 vs 粗粒度专家】**传统 MoE(Switch Transformer) utiliza minúsculas grandes especialidades(E=8-64)。现代细粒度 MoE(DeepSeek-V3) utiliza um grande número de pequenos especialistas(E=256+), cada especialista apenas 1/8 de FFN 宽度──组合数 C(256,8) 约为40000000000种,远超粗粒度的组合空间──质量提升显著,延迟基本不变──

## Construí-lo e realizei-o.
```figure
expert-routing
```

## Construí-lo

Veja .`code/main.py`Uma camada compacta de MoE em stdlib puro com:

> 参见 `code/main.py`                                                                                                                                                                                                                                                              

- `n_experts=8`Especialistas em SWIGU (um linear cada, para ilustração)
  Tradução:`n_experts=8`个类 SwiGLU 专家( cada uma linha de nível, para demonstração)
- Top-k=2 roteamento
  Tradução do português: top-k=2 路由
- Peso de abertura normalizado de softmax
  Tradução do inglês: softmax
- Equilíbrio sem perdas auxiliares através de preconceito por perito
  Tradução do inglês:                                                                                                                                                                                                                                                            

### Passo 1: roteador

```python
def route(hidden, W_router, top_k, bias):
    scores = [sum(h * w for h, w in zip(hidden, W_router[e])) for e in range(len(W_router))]
    biased = [s + b for s, b in zip(scores, bias)]
    top_idx = sorted(range(len(biased)), key=lambda i: -biased[i])[:top_k]
    # softmax over ORIGINAL scores of the chosen experts
    chosen = [scores[i] for i in top_idx]
    m = max(chosen)
    exps = [math.exp(c - m) for c in chosen]
    s = sum(exps)
    gates = [e / s for e in exps]
    return top_idx, gates
```

O preconceito afeta a seleção, não o peso da porta. É o truque DeepSeek-V3  o preconceito corrige o desequilíbrio de carga sem dirigir as previsões do modelo.

> 偏置影响选择,不影响门控制权重――这是DeepSeek-V3技巧偏置纠正负载不平衡,但不干预模型的预测――

### Passo 2: executar 100 tokens através do roteador

A utilização de um sistema de informação de informação de informação de informação é distorcida.`-γ`para especialistas excessivamente utilizados, `+γ`Para o uso de dados de dados, a utilização converge numa distribuição uniforme em algumas iterações.

> Seguir quais especialistas foram ativados quantas vezes. Não há qualquer tipo de utilização, o volume de utilização é constante.`-γ`, utilizando insuficientes especialistas `+γ`), a utilização foi distribuída em média em várias gerações.

### Passo 3: Comparação de contagem de parâmetros

Imprima o "equivalente denso" de uma configuração de MoE. DeepSeek-V3-formado: 256 encaminhado + 1 compartilhado, 8 ativo, d_model = 7168.

> 印印 MoE 配置的"密等价"──DeepSeek-V3 形状:256 个路由 + 1 个共享,8 个活跃,d_model=7168──总参数令人惊叹──活跃参数数只有密 Llama 3 70B 的七分之一──

## Use-o com o framework implementado.

EmbracamentoFace Carregamento:

> Abraços Face

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-8x22B-v0.1")
```

2026 Inferência de produção: vLLM suporta roteamento MoE nativo. SGLang tem o caminho paralelo de peritos mais rápido. Ambos processam automaticamente a seleção top-k e o paralelismo de peritos.

> 2026 anos de produção: vLLM 原生支持 MoE 路由──SGLang 拥有最快专家并行路径──都自动处理 top-k 选择和专家并行──

**When to pick MoE:**
- Quer qualidade de fronteira a um custo de inferência mais baixo por token.
  Tradução do inglês:You Wanna in lower per token 推理成本获得前沿质量──
- Tem a infraestrutura VRAM / especialista paralela.
  Tradução do inglês para tradução do inglês:
- A sua carga de trabalho é pesada em tokens (chat, código) e não em contexto (longos documentos).
  Tradução do inglês: Your work load is token 密集型(聊天、代码) e não 上下文密集型(长文档)

**When NOT to pick MoE:**
- Deploição de bordo  pagas o armazenamento completo por qualquer FLOP ativo.
  Tradução do inglês: 边缘部署你要为任何活跃 FLOP 支付全部储存──
- O serviço de roteamento especialista de um único usuário crítico para a latência adiciona custos gerais.
  Chinese Language Translation:延迟敏感的单用户服务专家路由增加开销──
- Modelos pequenos (<7B)  A vantagem de qualidade do MoE só aparece acima de um limiar de cálculo (~ 6B parâmetros ativos).
  O MoE é um modelo de desenvolvimento de uma economia de mercado que tem uma economia de mercado.

## Envia-o . Produto .

Veja .`outputs/skill-moe-configurator.md`A habilidade seleciona o layout de E, k e compartilhado de especialistas para um novo orçamento de parâmetros do MEE, tokens de treinamento e objetivo de implantação.

> 参见 `outputs/skill-moe-configurator.md` Esta habilidade  baseada em parâmetros orçamento ✓ token de treinamento ✓ número e objetivo de implantação, ✓ escolha de novos MoE ✓ e ✓ distribuição de especialistas ✓

## Exercícios.

1. **Easy.**Corra .`code/main.py`Veja como a atualização de preconceito sem perda auxiliar compensa o uso de especialistas em mais de 50 iterações.
   Tradução: 运行`code/main.py`◊ observar auxiliar perdas não relacionadas
2. **Medium.**Substitua o roteador aprendido por um roteador baseado em hash (determinista, sem aprendizado). Compare qualidade e equilíbrio. Por que o roteador aprendido é melhor?
   Tradução do inglês para o inglês:                                                                                                                                                                                                                                                          
3. **Hard.**Implementar "routing de parceria de implantação" de estilo GRPO (tructo DeepSeek-V3.2): registro que os especialistas disparam durante a inferência, forçar o mesmo roteamento durante o cálculo de gradientes. Medir o efeito sobre uma configuração de política de gradiente de brinquedo.
   Tradução do inglês para inglês: GRPO 风格的"推演匹配路由" (DeepSeek-V3.2 技巧): registro de quais especialistas foram ativados, em escala calculada, forçando o mesmo caminho.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Expert | "One FFN among many" | An independent feed-forward network; parameters dedicated to a sparse slice of the FFN computation. |
| 专家 | "众多 FFN 之一" | 独立的前馈网络；专用于 FFN 计算的稀疏切片的参数。 |
| Router | "The gate" | A tiny linear layer that scores each token against each expert; top-k selection. |
| 路由器 | "门控" | 一个小线性层，对每个 token 与每个专家打分；top-k 选择。 |
| Top-k routing | "k active experts per token" | Each token's FFN computation goes through exactly k experts, weighted by gate. |
| Top-k 路由 | "每个 token 激活 k 个专家" | 每个 token 的 FFN 计算经过恰好 k 个专家，按门控加权。 |
| Auxiliary loss | "Load-balance penalty" | Extra loss term that penalizes skewed expert usage. |
| 辅助损失 | "负载均衡惩罚" | 惩罚专家使用不均衡的额外损失项。 |
| Auxiliary-loss-free | "DeepSeek-V3's trick" | Balance via per-expert bias on the router's selection only; no extra gradient. |
| 辅助损失无关 | "DeepSeek-V3 的技巧" | 仅通过路由器选择上的逐专家偏置实现均衡；无额外梯度。 |
| Shared expert | "Always on" | Extra expert through which every token passes; captures common knowledge. |
| 共享专家 | "始终开启" | 每个 token 都通过的额外专家；捕获通用知识。 |
| Expert parallelism | "Shard by expert" | Distribute different experts to different GPUs; route tokens across the network. |
| 专家并行 | "按专家分片" | 将不同专家分配到不同 GPU；通过网络路由 token。 |
| Sparsity | "Active params < total params" | The ratio `k × expert_size / (E × expert_size)`; 37/671 ≈ 5.5% for DeepSeek-V3. |
| 稀疏性 | "活跃参数 < 总参数" | 比率 `k × expert_size / (E × expert_size)`；DeepSeek-V3 为 37/671 ≈ 5.5%。 |

## Mais leitura 延伸阅读

- [Shazeer et al. (2017). Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://arxiv.org/abs/1701.06538)- A ideia.
  O primeiro livro foi publicado em 17 de janeiro de 2012.
- [Fedus, Zoph, Shazeer (2022). Switch Transformer: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://arxiv.org/abs/2101.03961)- Switch, o MoE clássico.
  Tradução do português:Switch Transformer, clásico de MoE 论文。
- [Jiang et al. (2024). Mixtral of Experts](https://arxiv.org/abs/2401.04088) Mixtral 8×7B.
  Tradução do português:Mixtral 8×7B 论文。
- [DeepSeek-AI (2024). DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437) MLA + MoE sem perda auxiliar + MTP.
  Tradução do inglês:DeepSeek-V3 技术报告,MLA + 辅助损失无关 MoE + MTP。
- [Wang et al. (2024). Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts](https://arxiv.org/abs/2408.15664) o papel de balanço baseado em preconceitos.
  Tradução do inglês para "Equilibrio de estratégias baseadas em desvio"
- [Dai et al. (2024). DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models](https://arxiv.org/abs/2401.06066) o especialista de graus finos + compartilhado dividem os usos do roteador desta aula.
  中文翻译:DeepSeekMoE 论文,细粒度 + 共享专家拆分──
- [Kim et al. (2022). DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training](https://arxiv.org/abs/2201.05596) artigo original de especialistas compartilhados.
  中文翻译:DeepSpeed-MoE 原始共享专家论文──
