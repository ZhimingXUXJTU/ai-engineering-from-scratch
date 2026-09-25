# Escalação das leis.

> O artigo de 2020 Kaplan disse: modelo maior, menor perda. O artigo de 2022 Hoffmann disse: você estava sob treinamento.

> **【中文解读】**O teorema de Chinchilla revela o modelo de grandeza, quantidade de dados, quantidade de cálculos.

**Type:** Study | **类型:** 学习
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

Quando temos C FLOPs de computação de treinamento e queremos o melhor modelo, enfrentamos dois botões:

> Quando você tem C FLOPs de treinamento para calcular quantidade e quer o melhor modelo, você enfrenta dois rotos:

1. **How many parameters (N)?**Um modelo maior, maior capacidade.
   Tradução:**多少参数（N）？**模型越大, capacidade越高──
2. **How many training tokens (D)?**Mais dados, melhor utilização da capacidade.
   Tradução:**多少训练 token（D）？**O número de dados aumenta, a capacidade de utilização aumenta.

As FLOPs são de uma escala aproximada de `6 × N × D`Pode empurrar N para cima e D para baixo, ou D para cima e N para baixo.

> FLOPs aproximadamente`6 × N × D`扩展── você pode aumentar N 减小 D, ou aumentar D 减小 N── qual é melhor?

Antes de 2022, a resposta era "empurrar N duro". GPT-3 (2020) era 175B parâmetros treinados em tokens ~ 300B. Uma proporção de cerca de 1,7 tokens por parâmetro. As leis de escalagem de Kaplan apoiaram isso.

> Antes de 2022, a resposta é "推大 N"──GPT-3(2020) há 175B 参数, em cerca de 300B token 上训──比例约为每参数 1.7  token──Kaplan 缩放定律支持这一观点──

Hoffmann et al. (2022), que treinavam uma pequena família de modelos chamada Chinchilla, encontraram algo diferente: a relação ideal está mais próxima de **20 tokens per parameter**O Chinchilla (70B params, 1,4T tokens) venceu o GPT-3 (175B, 300B tokens) em cada referência a 2,5x menos custo de inferência.

> Hoffmann 等人(2022) treinou um grupo chamado Chinchilla's Model, descobriu resultados diferentes:**每个参数 20 个 token** GPT-3 low estimation trained 10 times── Chinchilla(70B 参数,1.4T token) em cada teste de base venceu GPT-3(175B,300B token), o custo de cálculo é apenas de 2,5 por cento do último.

2026 é o mundo de Chinchilla  com uma reviravolta importante. Llama 3 8B foi treinado em 15 trilhões de tokens, uma proporção de 1.875 tokens por parâmetro. Noventa e quatro vezes acima de Chinchilla-ótimo.

> 2026 é o mundo de Chinchilla mas há uma importante reviravolta Llama 3 8B usou 15 milhões de milhões de tokens  treinamento, proporção para cada elemento 1,875 tokens É Chinchilla o melhor 94 vezes Para um modelo que será usado em grande escala, o custo de raciocínio é mais importante do que o custo de treinamento, portanto, para menor implantação e excesso de treinamento (mais do que Chinchilla) é a estratégia padrão de 2026

> **【中文解读】**缩放定律的核心洞察:FLOPs ≈ 6 × N × D 参数 × token 数) ;;Kaplan(2020) tende a aumentar N, mas Chinchilla(2022) prova a melhor proporção de cerca de 20 tokens/paramontes.

> **【拓展：过度训练策略的经济逻辑】**Llama 3 8B utilizou 15T token  training(远超Chinchilla 最优的160B token), o custo de raciocínio foi reduzido drasticamente. Isto é porque a quantidade de cálculo de cada token e o parâmetro da raciocínio foram em proporção correta, sendo que o custo de raciocínio de cada token 8B parâmetro é de apenas cerca de 1/9 do modelo 70B.

## O conceito central.

![Chinchilla curves: loss vs compute at various N/D ratios](../assets/scaling-laws.svg)

### A lei Hoffmann

Do jornal Chinchilla, a perda é a seguinte:

> De Chinchilla 论文, perdas segue:

```
L(N, D) = A / N^α + B / D^β + E
```

- `N`= parâmetros (não incorporados).
  Tradução:`N`= 参数量 (não inserido)
- `D`= tokens de formação.
  Tradução:`D`= 訓練符号 数──
- `α ≈ 0.34`- Não .`β ≈ 0.28`(aproximadamente simétrica).
  Tradução:`α ≈ 0.34`- Não.`β ≈ 0.28`(大致对称)
- `E ≈ 1.69`O limite de perda irredutível.
  Tradução:`E ≈ 1.69`Não há limite de perdas.
- `A ≈ 406`- Não .`B ≈ 411`- Não .
  Tradução:`A ≈ 406`- Não.`B ≈ 411`- Não.

Dois termos negociam uns contra os outros à medida que escalam.`N`em cálculo fixo (C = 6ND) e resolver:

> 两项在扩展时相互制衡──在固定计算量 (C = 6ND) 下对 `N`求导并求解:

```
N_opt ≈ 0.6 × (C/6)^0.5
D_opt ≈ 0.6 × (C/6)^0.5
D_opt / N_opt ≈ 20
```

Computação-ótima: 20 tokens por parâmetro.

> 計算最优: cada paraméter 20 tokens.

### Por que se exercitar demais ?

O Chinchilla-Optimo minimiza a perda de treino por treino FLOP. Mas você paga o custo de treino uma vez;

> Chinchilla, o máximo mínimo de cada treinamento FLOP perda de treinamento. Mas o custo de treinamento só paga uma vez; custo de cálculo é permanente.

Para um chatbot que serve um trilhão de tokens por mês, a inferência domina o custo total. A abordagem de Llama: treinar menor, mais tempo.

> Para o serviço mensal de milhões de tokens, o método de Llama: treinamento de menor, maior, maior.

- Fica na GPU do consumidor.
  Tradução do inglês:
- A latência é uma fração de 70B Chinchilla-ótimo.
  Chinese:延迟仅为70B Chinchilla 最优的一小部分──
- A qualidade é suficientemente próxima para a maioria das tarefas.
  Tradução do inglês para tradução do inglês:

O artigo de DeepMind de 2024 ("Over-training is the new optimal") formalizou isso. Para cargas de trabalho dominadas pela inferência, a relação certa é mais próxima de 100500 tokens por parâmetro dependendo do volume de serviço.

> O DeepMind 2024 é um artigo sobre "excesso de treinamento é o novo melhor") formalizou este ponto.

### Emergência vs suavidade

Alegamento: certas habilidades (arítmética, raciocínio em vários passos, seguimento de cadeia de pensamento) "emergem" de repente em alguma escala.

> 声称: certos poderes (算术、多步推理、思维链遵循) em certa escala "emerge" (em inglês)

Schaeffer et al. (2023) argumentou que este é um artefato de medição: métricas emergentes usam pontuação descontínua (paralelas exatas, precisão no limiar) que escondem uma melhora suave nas logitas subjacentes.

> Schaeffer 等人(2023) considera que é a medida falsa:涌现指标使用不连续的评分(精确匹配、值准确率), ocultava a melhoria de planeamento dos logits de nível inferior。连续指标(交叉) mostra a linha de planeamento──

Em 2026, o consenso é: as previsões por perda contínua são confiáveis. Os saltos de referência são muitas vezes artefatos de pontuação.

> O conselho de 2026 é: a previsão de perdas continuas é confiável.

> **【中文解读】**"Emergência" (emergência) provocou uma grande discussão em 2023 Algumas capacidades parecem surgir de repente em uma escala específica Mas Schaeffer  et al. provaram que isso pode ser uma medida de falsidade: não contínuo de avaliação (como precisamente correspondido) oculta a melhoria de sua lógica de nível inferior.

> **【拓展：数据质量比数据量更重要】**Em 2026 a nova variação da lei de envelhecimento é a qualidade de dados. A série Phi da Microsoft demonstra que o token "de alta qualidade" selecionado pode aumentar a quantidade de cálculo de 2 vezes ou mais. A Llama 3 usa o aumento da partilha de dados e o aumento da quantidade de dados sintéticos.

### A imagem de 2026

As leis de escala ainda funcionam, mas:

> 缩放定律 ainda é válido, mas:

| Factor | Changed how |
|--------|-------------|
| 因素 | 变化方式 |
| Data quality | Curating "good" tokens (Phi-style) shifts curves by >2× effective compute |
| 数据质量 | 筛选"优质" token（Phi 风格）使曲线偏移超过 2 倍有效计算 |
| MoE | Total params decouple from active FLOPs; scaling laws per-active-FLOP |
| MoE | 总参数量与活跃 FLOPs 解耦；按活跃 FLOPs 的缩放定律 |
| Post-training | Some capabilities (instruction following, code) shift with SFT+RLHF more than pretraining |
| 后训练 | 某些能力（指令遵循、代码）通过 SFT+RLHF 的提升大于预训练 |
| Multimodality | Image + text tokens scale together; separate curves per modality |
| 多模态 | 图像 + 文本 token 一起扩展；每种模态有独立曲线 |
| Synthetic data | Models generate training data; effective compute can compound |
| 合成数据 | 模型生成训练数据；有效计算可复合增长 |

> **【拓展：合成数据与缩放定律的未来】**2026 ano de redução de teoremas enfrentando o problema de parede de dados Alta qualidade de dados do texto humano pode consumir em alguns anos a futuro. Dados sintéticos(Modelo gerado de dados de treinamento) é uma solução potencial.

O optimizador Muon (Kimi Moonlight, 2024) mostrou um ganho de computação efetiva de ~2x sobre AdamW em dados correspondentes. Algumas corridas de treinamento de 2026 usam Muon por padrão. Mudança a constante absoluta na lei de escala, não sua forma.

> Muon 优化器(Kimi Moonlight,2024) mostrou, nos mesmos dados, um aumento de cálculo válido de cerca de 2 vezes maior que o AdamW. Alguns treinos de 2026 executaram-se de forma padrão usando Muon.

## Construí-lo e realizei-o.
```figure
scaling-laws
```

## Construí-lo

Veja .`code/main.py`Implementamos a equação de perda Chinchilla e resolvemos para o computador-óptimo .`(N, D)`Em cada um dos vários orçamentos de computação.

> 参见 `code/main.py` Realizar a Equivalência de Perda de Chinchilla e buscar a melhor solução sob vários orçamentos de cálculo `(N, D)`- Não.

### Passo 1: Perda de chinchilla

```python
def chinchilla_loss(N, D, A=406.4, B=410.7, alpha=0.34, beta=0.28, E=1.69):
    return A / N ** alpha + B / D ** beta + E
```

Plot `L`Como um contorno sobre `(N, D)`em fixa `C = 6ND`- Encontre o mínimo.

> - Não .`L` como `(N, D)`É um tipo de "controle"`C = 6ND`❖ encontrar o valor mínimo.

### Passo 2: Fronteira óptima de computação

Para os orçamentos de computação de `1e17`- Não .`1e25`FLOPs, encontrar `(N, D)`que minimizem as perdas sujeitas a `6ND = C`Verificar a relação `D/N ≈ 20`- Não .

>  para `1e17`Até`1e25`FLOPs de cálculo orçamento, encontrar para minimizar perdas `(N, D)`,约束 `6ND = C` Processo de verificação`D/N ≈ 20`- Não.

### Passo 3: custo de formação excessiva

Calcule a perda extra que você paga para treinar um modelo 10x menor (1/10 do N ideal, 10x o D ideal).

> 計算訓練一個 10倍小模型 ((最优 N 的 1/10,最优 D 的 10倍) 付出的额外损失──報告作为交换的推理 FLOP 节约(与 N 成正比)──

### Passo 4: comparação com modelos reais

Chega conhecido .`(N, D)`par para GPT-3, Chinchilla, Llama 3 8B, DeepSeek- V3 (param activos), e comparar a perda prevista versus relatada.

> 输入 GPT-3、Chinchilla、Llama 3 8B、DeepSeek-V3(`(N, D)`Para, comparar perdas de previsão com perdas de relatório.

## Use-o com o framework implementado.

É improvável que treines um modelo de fronteira, mas as leis de escalagem dizem:

> Não é muito possível treinar o seu próprio modelo, mas a lei em questão diz-te:

1. **Whether your fine-tune has enough data.**Se os dados específicos da tarefa forem abaixo de 20 tokens por parâmetro do modelo base, espere saturação em algum nível de perda.
   Tradução:**你的微调是否有足够数据。**Se a sua missão específica for inferior a 20 tokens por parâmetro do modelo base, a expectativa será de alguma perda.
2. **Whether to pick a bigger base model.**Se gastas todo o teu orçamento em inferências, prefires um modelo menor e mais treinado.
   Tradução:**是否选择更大的基础模型。**Se você gastar todo o orçamento em pensar, priorizar a escolha de modelos menores, treinamento mais longo.
3. **Where the returns diminish.**Além de 1000x Chinchilla-óptima, as mudanças de perda de registro tornam-se ruído.
   Tradução:**收益递减在哪里。**Depois de 1000 vezes o melhor de Chinchilla, a alteração da perda numérica se transforma em ruído.

**The research trajectory in 2026:**

> **2026 年的研究方向：**

- **Data-constrained regime.**A web tem um número finito de tokens de alta qualidade (~ 510 trilhões de inglês após a filtragem). O pré-treino de fronteira está se aproximando deste teto. Dados sintéticos, multilíngues, multimodal e afinamento em escala RLHF são as próximas alavancas.
  Tradução:**数据受限时代。**网络上高质量代币 数量有限 ((过后约5-10亿英语) ⋅前沿预训练正在接近这个上限──合成数据多语言多模态和RLHF 缩缩微调是下一个杆──
- **Compute-multiplier tricks.**Otimizador de muons, MoE, melhor curatividade de dados  cada um muda as constantes absolutas, não o asintoto.
  Tradução:**计算倍增技巧。**Muon 优化器、MoE、更好的数据策展 cada um altera o número de constantes, não o número de frequências.
- **Scaling laws for RL.**A primeira evidência sugere a lei do poder em amostras de RL, mas com exponentes muito diferentes do que o pré-treino.
  Tradução:**RL 的缩放定律。**Open Question: Evidências iniciais indicam que o modelo de RL tem uma relação legal, mas os índices e o treinamento prévio são muito diferentes.

## Envia-o . Produto .

Veja .`outputs/skill-training-budget-estimator.md`A habilidade escolhe .`(N, D, hours, GPU)`Para uma nova fase de formação, dado o orçamento de cálculo, as restrições de implantação e a perda de objetivos.

> 参见 `outputs/skill-training-budget-estimator.md` Esta habilidade  baseado no orçamento de cálculo  Deploição de restrições e perda de objetivos, para novos treinamentos  Seleção de operações `(N, D, hours, GPU)`- Não.

## Exercícios.

1. **Easy.**Corra .`code/main.py`Imprimir Chinchilla-optimo .`(N, D)`para orçamentos de computação `1e20`- Não .`1e22`- Não .`1e24`Comparar com a mesa de modelos reais.
   Tradução: 运行`code/main.py` Impressão de orçamento`1e20`- Não.`1e22`- Não.`1e24`时的Chinchilla 最优 `(N, D)`与真实模型表对比──
2. **Medium.**Implementar a curva de perda de Hoffmann como função de computador.`log10(C)`Identificar quando a lei prevê que precisamos de um sistema de controle de dados.`>10^28`FLOPs para a próxima redução de 0,1 na entropia cruzada.
   Tradução do inglês: realização Hoffmann 损失-计算量曲线──绘制计算最优前沿的损失对`log10(C)` Determinar o que é necessário`>10^28`FLOPs 才能使交叉再降低 0.1──
3. **Hard.**Aplique a sua própria lei de escala em 5 modelos minúsculos (100K a 10M parâmetros) treinados no mesmo conjunto de dados.`α`E ...`E`Quão bem os seus exponentes correspondem aos publicados?
   Tradução do inglês:                                                                                                                                                                                                                                                            `α`和 `E`Como é que o seu índice se corresponde ao valor de publicação?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Parameters (N) | "Model size" | Non-embedding weight count; determines capacity. |
| 参数 (N) | "模型大小" | 非嵌入权重数量；决定容量。 |
| Tokens (D) | "Training data" | Number of training tokens seen; determines how well the parameters get used. |
| Token (D) | "训练数据" | 看到的训练 token 数量；决定参数被利用的程度。 |
| Compute (C) | "FLOPs spent" | Approximately `6 × N × D` for a standard transformer. |
| 计算量 (C) | "FLOPs 花费" | 标准 Transformer 约为 `6 × N × D`。 |
| Chinchilla-optimal | "D/N ≈ 20" | Ratio that minimizes loss per FLOP of pretraining. |
| Chinchilla 最优 | "D/N ≈ 20" | 最小化每个预训练 FLOP 损失的比例。 |
| Over-training | "Past Chinchilla" | Spend extra training FLOPs to save inference FLOPs; D/N >> 20. |
| 过度训练 | "超过 Chinchilla" | 额外训练 FLOPs 以节省推理 FLOPs；D/N >> 20。 |
| Irreducible loss | "The floor" | The `E` term in the scaling law; the entropy of the data itself. |
| 不可约损失 | "底线" | 缩放定律中的 `E` 项；数据本身的熵。 |
| Emergent capability | "Sudden jumps at scale" | Often a scorer artifact; continuous loss is smooth. |
| 涌现能力 | "规模上的突然跳变" | 通常是评分伪影；连续损失是平滑的。 |
| Effective compute | "Training-efficiency multiplier" | Better data / optimizer / architecture multiplies how far a FLOP goes. |
| 有效计算 | "训练效率倍增器" | 更好的数据/优化器/架构使每个 FLOP 走得更远。 |

## Mais leitura 延伸阅读

- [Kaplan et al. (2020). Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361) o primeiro artigo sobre a legislação em escala;
  Tradução do inglês: First Edition
- [Hoffmann et al. (2022). Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556)- Chinchilla.
  Chinchilla 论文──
- [Schaeffer et al. (2023). Are Emergent Abilities of Large Language Models a Mirage?](https://arxiv.org/abs/2304.15004) surgimento como artefacto de medição.
  Tradução do inglês para O que é um "humor"
- [Sardana, Frankle (2024). Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws](https://arxiv.org/abs/2401.00448)Por que o treinamento excessivo de Llama é adequado para a sua carga de trabalho.
  Por que o excesso de treinamento de Llama para o seu trabalho é correto?
- [Jordan et al. (2024). Muon: An optimizer for hidden layers in neural networks](https://kellerjordan.github.io/posts/muon/)Multiplicador de cálculo 2x.
  Muon 优化器,2 倍计算倍增器── tradução livre
