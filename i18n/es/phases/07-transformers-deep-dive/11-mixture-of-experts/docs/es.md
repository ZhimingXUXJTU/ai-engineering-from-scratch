# Mixtura de expertos (MoE) 混合专家模型 (MoE)

> Un transformador 70B denso activa todos los parámetros para cada token. Un 671B MoE activa solo 37B por token y lo supera en cada punto de referencia.

> **【中文解读】**MoE sólo activa parte de la red de expertos para procesar cada token, aumentando considerablemente la cantidad de componentes sin aumentar la cantidad de cálculo.

**Type:** Hands-on | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

Los FLOPs de un transformador denso a la inferencia son iguales al número de parámetros (de 2 veces para el pase hacia adelante). Escala un modelo denso y cada token paga la cuenta completa. Para 2024 la frontera estaba golpeando una pared de cálculo: para ser significativamente más inteligente, se necesitaban exponencialmente más FLOPs por token.

> 密变压器 推理时的FLOPs等于其参数(前向传播乘以2);;扩大密模型意味着每个代币都必须支付全部代价;; En el año 2024, el modelo de vanguardia se encontró con el cálculo: para ser más inteligente, necesita un índice de crecimiento de cada token FLOPs;;

La mezcla de expertos rompe este vínculo.`E`expertos independientes + un router que seleccione `k`Expertos por token. Parámetros totales = `E × FFN_size`. Parámetros activos por token = `k × FFN_size`. Configuración típica para 2026: `E=256`¿ Qué ?`k=8`. Escales de almacenamiento con `E`, calcular escalas con `k`¿ Qué ?

> 混合专家模型打破了这个联系.`E`个独立专家 + 一个路由器, cada token 选择 `k`个专家──总参数 = `E × FFN_size`◊ cantidad activa de cada token = `k × FFN_size`❖ Configuración típica para el año 2026:`E=256`¿Qué es esto?`k=8` Almacenamiento`E`扩展,计算随 `k`扩展──

La frontera de 2026 es casi completamente MoE: DeepSeek-V3 (671B total / 37B activo), Mixtral 8×22B, Qwen2.5-MoE, Llama 4, Kimi K2, gpt-oss. En el tablero de clasificación independiente de Análisis Artificial, los 10 modelos de código abierto más importantes son todos MoE.

> La primera línea de 2026 es casi completamente MoE:DeepSeek-V3(671B 总参数 / 37B 活跃) 、Mixtral 8×22B、Qwen2.5-MoE、Llama 4、Kimi K2、gpt-oss── en la lista de clasificación independiente de Análisis Artificial,排名前 10 de los modelos de origen abiertos son MoE──

> **【中文解读】**MoE rompió la ecuación de "parámetro = 计算量"― cada FFN 层替换为E 个独立专家 + 路由器, cada token sólo activa k 个专家―总参数随着E 增长, pero la cantidad de cálculo de cada token sólo con k 增长―典型配置 E=256, k=8,存储随着E 缩缩,计算随着k 缩缩――这是2020s's most important expansion thinking―

> **【拓展：DeepSeek-V3 的 MoE 创新】**DeepSeek-V3  posee 671B   Parámetros totales pero por token sólo activa 37B a través de 256 perímetros expertos + 1 perímetros de uso compartido implementar. También introdujo una estrategia de equilibrio de carga sin pérdida de ayuda, evitando el problema de colapsos de perímetros tradicionales MoE. En el ranking de Análisis Artificial, DeepSeek-V3 alcanzó un rendimiento comparable con menos de un diezmo del costo de la investigación de GPT-4.

## El concepto central.

![MoE layer: router selects k of E experts per token](../assets/moe.svg)

### El intercambio de FFN

Bloqueo de transformador denso:

> 密 块 de transformador:

```
h = x + attn(norm(x))
h = h + FFN(norm(h))
```

Bloqueo de la MOE:

```
h = x + attn(norm(x))
scores = router(norm(h))              # (N_tokens, E)
top_k = argmax_k(scores)              # pick k of E per token
h = h + sum_{e in top_k}(
        gate(scores[e]) * Expert_e(norm(h))
    )
```

Cada experto es un FFN independiente (típicamente SwiGLU). El router es una sola capa lineal.`k`expertos y obtiene una mezcla cerrada de sus resultados.

> Cada especialista es un FFN independiente (normalmente SwiGLU) ⋅ router es una capa única ⋅ cada token                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    `k`个专家, obtener su salida y control de la mezcla.

### El problema de equilibrio de carga

Si el router pone el 90% de los tokens a través del experto 3, los otros expertos pasan hambre.

> Si el router distribuye el 90% de los tokens a los expertos 3, otros expertos se "envejecerán"

1. **Auxiliary load-balancing loss**Añade una penalidad proporcional a la variación en el uso experto. Funciona, pero añade un hiperparámetro y una segunda señal de gradiente.
   En inglés:**辅助负载均衡损失**(Switch Transformer、Mixtral) ∼ Añadir con especialistas el uso de la diferencia de proporción de castigo── efectivo, pero aumentó las superparámetros y la segunda graduación de señal──
2. **Expert capacity + token dropping**Cada experto procesa como máximo`C × N/E`Los tokens de sobreflujo saltan la capa.
   En inglés:**专家容量 + token 丢弃**(Epiquio temprano) ◊ Cada especialista más`C × N/E`个 token;溢出的 token 跳过这个层――损害质量――
3. **Auxiliary-loss-free balancing**(DeepSeek-V3). Agregar un sesgo aprendido por experto que cambia la selección de la parte superior del router.
   En inglés:**辅助损失无关均衡**(DeepSeek-V3)── Añadir un aprendizaje hasta el momento de cada especialista, ajustar la selección de los principales módulos de ruta── modificar la situación de los módulos de entrenamiento.

El enfoque de DeepSeek-V3: después de cada paso de formación, para cada experto, compruebe si su uso está por encima o por debajo del objetivo.`±γ`. Utilizaciones de selección `scores + bias`Las probabilidades expertas utilizadas para el gating son las primas .`scores`Desacopla el enrutamiento de la expresión.

> Método de Profundo-V3: Después de cada paso de entrenamiento, cada experto comprueba si su uso es mayor o menor al objetivo.`±γ`△ seleccionar `scores + bias` La probabilidad de que los expertos sean controlados por el portal es original.`scores`将路由与表达解──

### Expertos compartidos

DeepSeek-V2/V3 también divide a los expertos en *compartido* y *routed*. Cada token pasa a través de todos los expertos compartidos. Los expertos enrutados se seleccionan a través de top-k. Los expertos compartidos capturan el conocimiento común; los expertos enrutados se especializan. V3 ejecuta 1 experto compartido más el top-8 de 256 enrutados.

> DeepSeek-V2/V3 también dividirá los especialistas en dos clases: * compartido* y * ruta*. Cada token está dividido en dos categorías:

### Expertos de granos finos

MoE clásico (GShard, Switch): cada experto tiene la anchura de un FFN completo. `E`es pequeño (864), `k`es pequeño (12).

> 经典 MoE(GShard、Switch): Cada especialista con FFN completo 一样宽──`E`较小(8-64),`k`较小(1-2)。

MoE moderno de granos finos (DeepSeek-V3, Qwen-MoE): cada experto es más estrecho (1/8 de FFN). `E`es grande (256+), `k`Es más grande (8+). Los mismos parámetros totales, pero las combinaciones escalar mucho más rápido. `C(256, 8) = 400 trillion`La calidad aumenta y la latencia se mantiene estable.

> 现代细粒度 MoE(DeepSeek-V3、Qwen-MoE): cada especialista más estrecho(1/8 FFN`E`较大(256+),`k`También más grande ((8+) ⋅总参数 igual, pero组合增长更快──`C(256, 8) = 400 万亿`种可能的"专家"组合──质量提升,延迟不变──

> **【拓展：MoE 的路由崩塌问题】**El reto central en el entrenamiento de MoE es el desplome del router) 路由器可能將大部分的代幣分配給少数專家,导致其他專家得不到訓練──:

### El perfil de costes

Por símbolo, por capa:

> Cada símbolo, cada capa:

| Config | Active params / token | Total params |
|--------|-----------------------|--------------|
| 配置 | 每个 token 活跃参数 | 总参数量 |
| Mixtral 8×22B | ~39B | 141B |
| Llama 3 70B (dense) | 70B | 70B |
| DeepSeek-V3 | 37B | 671B |
| Kimi K2 (MoE) | ~32B | 1T |

DeepSeek-V3 supera a Llama 3 70B (denso) en casi todos los puntos de referencia mientras hace **fewer active FLOPs per token**Más parámetros = más conocimiento. más FLOPs activos = más cálculo por token.

> DeepSeek-V3 en casi todos los test de base ha derrotado a Llama 3 70B, al mismo tiempo.**每个 token 的活跃 FLOPs 更少**△ Más parametros = 更多知识── Más FLOPs activos = Cada token 更多计算──MoE 将两者解──

### El problema: la memoria

Todos los expertos viven en GPU independientemente de cuál uno dispare. Un modelo 671B necesita ~ 1.3 TB de VRAM para pesos de fp16.

> Todos los expertos, independientemente de si están activados, se encuentran en la GPU. Un modelo 671B requiere alrededor de 1.3TB de fp16 权重显存.

> **【中文解读】**El peso central de MoE: con el cálculo de cambio de memoria. El DeepSeek-V3 alcanzó un parámetro activo de 37B con un rendimiento de más de 70B, pero requiere 1.3TB de almacenamiento de datos. Esto impulsó el desarrollo de la tecnología de paralelismo de expertos.

> **【拓展：细粒度专家 vs 粗粒度专家】**传统 MoE(Switch Transformer) utilizaba una pequeña cantidad de grandes especialistas(E=8-64)。现代细粒度 MoE(DeepSeek-V3) utilizaba una gran cantidad de pequeños especialistas(E=256+), cada especialista tenía sólo 1/8 de FFN 宽度──组合数 C(256,8) 约为40000000000种,远超粗粒度的组合空间──质量提升显著,延迟基本不变──

## Construye y realiza.
```figure
expert-routing
```

## Construye el mismo

¿ Qué ?`code/main.py`. Una capa compacta de MoE en stdlib puro con:

> 参见 `code/main.py` Una capa de implementación de normas de la UE, que incluye:

- `n_experts=8`Expertos de SWIGU (una línea cada uno, para ilustración)
  En inglés:`n_experts=8`个类 SwiGLU 专家( cada una de las líneas de la capa, para la demostración)
- Top-k=2 enrutamiento
  En inglés, "Centro de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de la Cumbre de Cumbre de la Cumbre de Cumbre de Cumbre de Cumbre"
- Peso de puertas normalizado de la máxima suave
  Traducción:softmax 归一化门控权重
- equilibrio sin pérdidas auxiliares por sesgo de expertos
  Por el contrario, el cambio de posición de los trabajadores es un problema de la salud.

### Paso 1: el router

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

El sesgo afecta la selección, no el peso de la puerta. Ese es el truco de DeepSeek-V3  sesgo corrige el desequilibrio de carga sin dirigir las predicciones del modelo.

> 偏置影响选择,不影响门控制权重――这是DeepSeek-V3的技巧偏置纠正负载不平衡,但不干预模型的预测――

### Paso 2: ejecuta 100 tokens a través del router

El uso de los datos de los datos de los usuarios es distorsionado.`-γ`para expertos sobreutilizados, `+γ`En el caso de las aplicaciones de la aplicación de la norma de uso (en el caso de las aplicaciones de uso insuficiente), el uso converge a una distribución uniforme en varias iteraciones.

> Seguir cuáles expertos han sido activados varias veces.`-γ`, uso insuficiente de expertos `+γ`), el uso en varias generaciones recibida a la distribución media.

### Paso 3: Comparación de parámetros

Imprima el "equivalente denso" de una configuración de MoE. DeepSeek-V3-forma: 256 enrutado + 1 compartido, 8 activo, d_model=7168. El conteo total de parámetros es impresionante. El conteo activo es una séptima de un Llama 3 70B denso.

> 印印 MOE 配置的"密等价"──DeepSeek-V3 形状:256 个路由 + 1 个共享,8 个活跃,d_model=7168──总参数数令人惊叹──活跃参数数只有密 Llama 3 70B 的七分之一──

## Usalo con el marco de ejecución

Embarcación de la cara:

> Acogida cara

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-8x22B-v0.1")
```

2026 Inferencia de producción: vLLM admite el enrutamiento de MoE de forma nativa. SGLang tiene el camino paralelo experto más rápido. Ambos manejan automáticamente la selección top-k y el paralelismo experto.

> 2026 años de producción: vLLM 原生支持 MoE 路由──SGLang 拥有最快专家并行路径──两都自动处理顶级 选择和专家并行──

**When to pick MoE:**
- Quieres una calidad de frontera con un menor costo de inferencia por token.
  China: 您想以低的每 token 推理成本获得前沿质量──
- Tiene la infraestructura paralela VRAM / experto.
  Traducción:Tu tienes suficiente evidencia de la infraestructura.
- Su carga de trabajo es token-pesado (chat, código) no contexto-pesado (docs largos).
  Su trabajo está en el tipo de token 密集型(聊天、代码) y no en el tipo de texto de abajo.

**When NOT to pick MoE:**
- Despliegue de borde  usted paga el almacenamiento completo para cualquier FLOP activo.
  China 译文:边缘部署你要为任何活跃FLOP 支付全部储备──
- El servicio de un solo usuario de servicio  de enrutamiento experto de latencia crítica añade gastos generales.
  China: 延迟敏感的单用户服务专家路由增加开销──
- Los modelos pequeños (<7B)  La ventaja de calidad de MoE sólo aparece por encima de un umbral de cálculo (~6B parámetros activos).
  En el caso de los modelos de la MOE, el valor de la MOE es de aproximadamente 6B.

## Envíe el producto .

¿ Qué ?`outputs/skill-moe-configurator.md`. La habilidad elige E, k y diseño compartido de expertos para un nuevo presupuesto de parámetros del Ministerio de Economía, tokens de capacitación y objetivo de implementación.

> 参见 `outputs/skill-moe-configurator.md` Esta habilidad  De acuerdo con el presupuesto  token de entrenamiento  Número y objetivo de implementación,  para el nuevo Ministerio de Educación  E  k 和 compartir los diseños de expertos 

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Observe cómo la actualización de sesgo sin pérdidas auxiliares equilibra el uso de expertos en más de 50 iteraciones.
   Traducción:运行`code/main.py`◊ observar el uso de los expertos en equilibrio en 50 vecesgeneration
2. **Medium.**Reemplazar el router aprendido con un router basado en hash (determinístico, sin aprendizaje). Comparar calidad y equilibrio. ¿Por qué el router aprendido es mejor?
   Traducción:Por qué es mejor el aprendizaje en un módulo de ruta?
3. **Hard.**Implementar el tipo GRPO "routing de despliegue" (tructo DeepSeek-V3.2): registro que los expertos disparan durante la inferencia, forzar el mismo enrutamiento durante el cálculo de gradientes. Medir el efecto en una configuración de política de gradientes de juguete.
                                                                                                                                                                                                                                                                 

## Términos clave .

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

## Más Leer más Leer más

- [Shazeer et al. (2017). Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://arxiv.org/abs/1701.06538)¿La idea?
  El texto original de MoE fue traducido en inglés en chino en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés.
- [Fedus, Zoph, Shazeer (2022). Switch Transformer: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://arxiv.org/abs/2101.03961) Switch, el clásico MoE.
  El cambio de velocidad de la máquina de cambio de velocidad de la máquina de cambio de velocidad de la máquina de cambio de velocidad de la máquina de cambio de velocidad de velocidad de la máquina de cambio de velocidad de velocidad de la máquina de cambio de velocidad de velocidad de la máquina de cambio de velocidad de velocidad de velocidad de la máquina de cambio de velocidad de velocidad de velocidad de velocidad de la máquina de cambio de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de velocidad de
- [Jiang et al. (2024). Mixtral of Experts](https://arxiv.org/abs/2401.04088) Mixtral 8×7B.
  Traducción:Mixtral 8×7B 论文。
- [DeepSeek-AI (2024). DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437) MLA + MoE sin pérdidas auxiliares + MTP.
  La información de la empresa se encuentra en el área de la información de la empresa.
- [Wang et al. (2024). Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts](https://arxiv.org/abs/2408.15664) el papel de balance basado en sesgos.
  La estrategia de equilibrio basada en la orientación.
- [Dai et al. (2024). DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models](https://arxiv.org/abs/2401.06066) el experto de granos finos + compartido dividido de este curso de los usos del router.
  En el caso de los grupos de la población, el número de personas que han sido objeto de una investigación en la investigación es de aproximadamente un millón de personas.
- [Kim et al. (2022). DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training](https://arxiv.org/abs/2201.05596) documento original compartido de expertos.
  El trabajo de la empresa de la industria de la información (MQM) fue realizado en el año 2000.
