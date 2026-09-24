# Escalación de leyes.

> El artículo de Kaplan de 2020 dijo: modelo más grande, pérdida menor. El artículo de Hoffmann de 2022 dijo: estabas bajo entrenamiento. La computación se divide en dos cubos  parámetros y tokens  y la división no es obvia.

> **【中文解读】**La ley de Chinchilla revela el modelo de tamaño, la cantidad de datos, la relación óptima de la cantidad de cálculo.

**Type:** Study | **类型:** 学习
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

Cuando tienes C FLOPs de formación en computación y quieres el mejor modelo, te enfrentas a dos botones:

> Cuando tienes un entrenamiento para calcular la cantidad y quieres el mejor modelo, te enfrentas a dos rotas:

1. **How many parameters (N)?**Un modelo más grande, mayor capacidad.
   En inglés:**多少参数（N）？**模型越大, capacidad越高──
2. **How many training tokens (D)?**Más datos, mejor uso de la capacidad.
   En inglés:**多少训练 token（D）？**Más datos, más capacidad para usar.

Las PLOP se extienden aproximadamente en la misma escala que `6 × N × D`Puedes empujar N hacia arriba y D hacia abajo, o D hacia arriba y N hacia abajo. ¿Cuál es mejor?

> FLOPs aproximadamente`6 × N × D`¿Puedes aumentar N  disminuir D, o aumentar D  disminuir N ⋅ ¿Cuál es mejor?

Antes de 2022, la respuesta era "push N hard". GPT-3 (2020) era 175B parámetros entrenados en tokens ~300B. Una proporción de aproximadamente 1,7 tokens por parámetro.

> Antes de 2022 años, la respuesta es "推大 N"──GPT-3(2020) tiene 175B 参数, en torno a 300B token 上训练──比例约为每参数 1.7  token──Kaplan 缩放定律支持这一观点──

Hoffmann et al. (2022), que formaba una pequeña familia de modelos llamada Chinchilla, encontró algo diferente: la relación óptima está más cerca de **20 tokens per parameter**Sin embargo, el equipo de GPT-3 fue 10 veces menos capacitado. Chinchilla (70B parámetros, 1.4T tokens) superó a GPT-3 (175B, 300B tokens) en cada punto de referencia a un costo de inferencia 2,5 veces menor.

> Hoffmann 等人(2022) entrenó un pequeño grupo llamado modelo de Chinchilla, encontró resultados diferentes:**每个参数 20 个 token** GPT-3 low estimation trained 10 times──Chinchilla(70B 参数,1.4T token) en cada基准测试 todos derrotaron GPT-3(175B,300B token), el costo de la hipótesis es sólo de los últimos 2.5 分之一──

2026 es el mundo de Chinchilla  con un giro importante. Llama 3 8B fue entrenado en 15 billones de tokens, una proporción de 1.875 tokens por parámetro. Noventa y cuatro veces más allá de Chinchilla-óptimo. El costo de inferencia importa más que el costo de entrenamiento para modelos que se utilizarán a escala, por lo que el sobreentrenamiento (pasado de Chinchilla) para una huella desplegable más pequeña es el estándar de 2026.

> 2026 es el año del mundo de Chinchilla pero hay un importante giro. Llama 3 8B utilizó 15 millones de tokens  entrenamiento, proporción para cada elemento 1,875  token ⋅ es Chinchilla óptimo 94 veces ⋅ para el modelo que será utilizado a gran escala, el costo de la raciocinio es más importante que el costo de la formación, por lo que para una menor implementación de su propia marca ⋅ sobre Chinchilla ⋅ es la estrategia predeterminada para el año 2026.

> **【中文解读】**缩放定律的核心洞察:FLOPs ≈ 6 × N × D(参数 × token 数) ;;Kaplan(2020) tiende a aumentar N, pero Chinchilla(2022) prueba la mejor proporción de aproximadamente 20 tokens/parámetros.

> **【拓展：过度训练策略的经济逻辑】**Llama 3 8B utiliza 15T token  entrenamiento(Far sobre Chinchilla maximal 160B token), el costo de la racionalización se redujo considerablemente. Esto se debe a que la cantidad de cálculo de cada token en la racionalización se ha convertido en proporción correcta entre la cantidad y el parámetro de los parámetros,8B parámetros de la racionalización costo de sólo aproximadamente 1/9 de los 70B  modelos.

## El concepto central.

![Chinchilla curves: loss vs compute at various N/D ratios](../assets/scaling-laws.svg)

### La ley Hoffmann

De la publicación de Chinchilla, la pérdida es la siguiente:

> Desde Chinchilla 论文, pérdida sigue:

```
L(N, D) = A / N^α + B / D^β + E
```

- `N`= parámetros (no incorporados).
  En inglés:`N`= 参数量 (en inglés)
- `D`= tokens de entrenamiento.
  En inglés:`D`= 訓練代號 数──
- `α ≈ 0.34`¿ Qué ?`β ≈ 0.28`(aproximadamente simétrica).
  En inglés:`α ≈ 0.34`¿Qué es esto?`β ≈ 0.28`(Gran número de palabras)
- `E ≈ 1.69`, el techo de pérdida irreductible.
  En inglés:`E ≈ 1.69`, no puede perderse en el límite.
- `A ≈ 406`¿ Qué ?`B ≈ 411`¿ Qué ?
  En inglés:`A ≈ 406`¿Qué es esto?`B ≈ 411`¿Qué es eso?

Dos términos se intercambian entre sí a medida que escalas.`N`en cálculo fijo (C = 6ND) y resolver:

> 两项在扩展时相互制衡──在固定计算量 (C = 6ND) 下对 `N`求导并求解:

```
N_opt ≈ 0.6 × (C/6)^0.5
D_opt ≈ 0.6 × (C/6)^0.5
D_opt / N_opt ≈ 20
```

Optimo para el cálculo: 20 tokens por parámetro.

> 計算最优: cada uno de los 20 símbolos.

### ¿Por qué sobreentrenar de todos modos?

Chinchilla-optimal minimiza la pérdida de entrenamiento por entrenamiento FLOP. Pero usted paga el costo de entrenamiento una vez; la inferencia costo para siempre.

> Chinchilla, Optimum Minimizes cada entrenamiento FLOP de entrenamiento pérdida. Pero el costo de entrenamiento sólo paga una vez; el costo de la evaluación es permanente.

Para un chatbot que sirve un billón de tokens por mes, la inferencia domina el costo total. El enfoque de Llama: tren más pequeño, más largo.

> 对于每月服务万亿代币的聊天机器人,推理主导总成本――Llama's method:训练更小,更长――8B 在 15T代币上训是深度推理优化:

- Se ajusta a las GPU de consumo.
  Traducción:GPU de los niveles de consumo.
- La latencia es una fracción de 70B Chinchilla-óptima.
  China: 延迟仅为70B Chinchilla 最优的一小部分──
- La calidad es lo suficientemente cercana para la mayoría de las tareas.
  La calidad es suficiente para la mayoría de las tareas.

El artículo de DeepMind de 2024 ("Over-training es el nuevo óptimo") formalizó esto. Para las cargas de trabajo dominadas por inferencias, la proporción correcta está más cerca de 100500 tokens por parámetro dependiendo del volumen de servicio.

> DeepMind 2024 años de trabajo ((("exceso de entrenamiento es el nuevo mejor") formalizó este punto.

### Emergencia vs suavidad

Afirmación: ciertas habilidades (arítmética, razonamiento en varios pasos, seguimiento de la cadena de pensamiento) "emergen" repentinamente en alguna escala.

> 声称: ciertas capacidades (算术、多步推理、思维链遵循) en cierta escala "surge" (en inglés)

Schaeffer et al. (2023) argumentó que este es un artefacto de medición: las métricas emergentes utilizan puntuaciones discontinuas (combinación exacta, precisión en el umbral) que ocultan una mejora suave en las logitas subyacentes.

> Schaeffer 等人(2023) considera que es la medida de falsedad:涌现指标使用不连续的评分(精确匹配、值准确率), ocultó la mejora de la planificación de los logitos de la base──连续指标(交叉) muestra la planificación de la línea──

En 2026 el consenso es: las predicciones a través de pérdidas continuas son confiables. Los saltos de referencia son a menudo artefactos de puntaje.

> El consenso de 2026 es: el pronóstico de pérdidas continuas es fiable.

> **【中文解读】**"Emergencia" (涌现能力) provocó un gran debate en 2023 sobre algunas capacidades que parecen aparecer de repente en una escala específica. Pero Schaeffer 等人 demostró que esto podría ser una medida falsa: no se mantiene un nivel de evaluación.

> **【拓展：数据质量比数据量更重要】**En 2026 la nueva variación de la ley de acrecentamiento es la calidad de datos. La serie Phi de Microsoft muestra que los tokens de "alta calidad" seleccionados pueden aumentar el volumen de cálculo de forma efectiva 2 veces más. La Llama 3 utiliza la optimización de la distribución de datos y el aumento de datos de la composición. La arquitectura de MoE explica aún más la cantidad de componentes y la cantidad de cálculo activo. Estos factores hacen que la curva tradicional de Chinchilla necesite recalificar.

### La imagen de 2026

Las leyes de escalación todavía funcionan, pero:

> 缩放定律 todavía vigente, pero:

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

> **【拓展：合成数据与缩放定律的未来】**2026 Enfrentamiento de la ley de datos frente a la pared de datos  Alta calidad de datos de texto humano podría consumirse en los próximos años  Datos de formación de modelos generados  Datos de formación de datos) es una solución potencial  La serie Phi de Microsoft utiliza GPT-4 para entrenar los datos de la "clasificación de calidad de libros" de datos de datos de datos de la GPT, Nemotron de NVIDIA utiliza datos de la composición  Si los datos de la composición son válidos, el "calculo válido" de la ley de la ley de cálculo de la consolidación puede continuar creciendo

El optimizador de Muon (Kimi Moonlight, 2024) mostró una ganancia de cálculo efectiva de ~2x sobre AdamW en datos coincidentes. Algunas carreras de entrenamiento de 2026 usan Muon por defecto. Cambia la constante absoluta en la ley de escala, no su forma.

> Muon 优化器(Kimi Moonlight,2024) en los mismos datos mostró un aumento de cálculo efectivo de aproximadamente 2 veces más que AdamW. Algunos entrenamientos de 2026 se ejecutan de forma automática utilizando Muon.

## Construye y realiza.
```figure
scaling-laws
```

## Construye el mismo

¿ Qué ?`code/main.py`Implementamos la ecuación de pérdidas de Chinchilla y resolvemos para el óptimo de cálculo .`(N, D)`en cada uno de los presupuestos informáticos.

> 参见 `code/main.py` Lograr la ecuación de pérdida de Chinchilla y buscar la mejor solución bajo un presupuesto de varios cálculos`(N, D)`¿Qué es eso?

### Paso 1: pérdida de chinchilla

```python
def chinchilla_loss(N, D, A=406.4, B=410.7, alpha=0.34, beta=0.28, E=1.69):
    return A / N ** alpha + B / D ** beta + E
```

El argumento`L`como un contorno sobre `(N, D)`en fijo `C = 6ND`- Encuentra el mínimo.

> ¿ Qué ?`L` como `(N, D)`de la línea, fija`C = 6ND`❖ encontrar el valor mínimo―

### Paso 2: Frontera óptima de cálculo

Para los presupuestos de computación de `1e17`¿ Qué ?`1e25`FLOPs, encontrar `(N, D)`que minimizen las pérdidas sujetas a `6ND = C`Verifique la relación `D/N ≈ 20`¿ Qué ?

>  para el `1e17`¿ Qué ?`1e25`FLOPs de cálculo de presupuesto, encontrar para minimizar las pérdidas `(N, D)`, de la unión`6ND = C` Procentaje de pruebas`D/N ≈ 20`¿Qué es eso?

### Paso 3: Costo de formación excesiva

Calcule la pérdida adicional que paga para entrenar un modelo 10x más pequeño (1/10 de N óptimo, 10x el D óptimo).

> 計算訓練一個 10倍小模型 ((最优 N 的 1/10,最优 D 的 10倍) de los extraños pagados──報告作为交换的推理 FLOP 节约(与 N 成正比)──

### Paso 4: comparación con modelos reales

Entra en conocido`(N, D)`parejas para GPT-3, Chinchilla, Llama 3 8B, DeepSeek-V3 (parámetros activos), y comparar pérdida prevista con la reportada.

> 输入 GPT-3、Chinchilla、Llama 3 8B、DeepSeek-V3(activ参数) de ya conocidos `(N, D)`Para, comparar pérdidas de previsión con pérdidas de informe.

## Usalo con el marco de ejecución

Es poco probable que entrenes a un modelo de frontera, pero las leyes de escalate te dicen:

> Tu no es muy probable que entrenes tu propio modelo, pero la ley de la reducción te dice:

1. **Whether your fine-tune has enough data.**Si sus datos específicos de tareas están por debajo de 20 tokens por parámetro del modelo base, esperen saturación en algún nivel de pérdida.
   En inglés:**你的微调是否有足够数据。**Si tu tarea específica de datos es inferior a 20 tokens por parámetro del modelo básico, la expectativa es que se produzca una pérdida de valor.
2. **Whether to pick a bigger base model.**Si gastas todo tu presupuesto en inferencias, prefieres un modelo más pequeño y más entrenado.
   En inglés:**是否选择更大的基础模型。**Si se gastan todos los presupuestos en la reflexión, priorizar la elección de modelos más pequeños, entrenar más tiempo.
3. **Where the returns diminish.**Más allá de 1000x Chinchilla-óptima, los cambios de pérdida de registro se convierten en ruido.
   En inglés:**收益递减在哪里。**Después de más de 1000 veces el mejor de Chinchilla, el cambio en la pérdida de números se convierte en ruido.

**The research trajectory in 2026:**

> **2026 年的研究方向：**

- **Data-constrained regime.**La web tiene un número finito de tokens de alta calidad (~510 billones de inglés después de filtrar). El preentrenamiento fronterizo se acerca a este techo.
  En inglés:**数据受限时代。**网络上高质量代币 数量有限 ((过后约5-10亿亿英语) ⋅前沿预训练正在接近这个上限──合成数据多语言多模态和RLHF 缩缩的微调是下一个杆──
- **Compute-multiplier tricks.**Optimizador de muones, MoE, mejor curado de datos  cada uno cambia las constantes absolutas, no el asintoto.
  En inglés:**计算倍增技巧。**Muon 优化器, MoE, mejores datos 策展 cada uno cambia el número de frecuencias absolutas, y no la línea de aproximación.
- **Scaling laws for RL.**Las primeras pruebas sugieren la ley de poder en muestras de RL pero con exponentes muy diferentes que el preentrenamiento.
  En inglés:**RL 的缩放定律。**Problema abierta―: Evidencias tempranas indican que el RL sample tiene una relación legal, pero el índice y el pre-training son muy diferentes―:

## Envíe el producto .

¿ Qué ?`outputs/skill-training-budget-estimator.md`La habilidad escoge .`(N, D, hours, GPU)`para una nueva carrera de formación, dado el presupuesto de cálculo, las limitaciones de implementación y la pérdida de objetivos.

> 参见 `outputs/skill-training-budget-estimator.md` Esta habilidad  basándose en el presupuesto de cálculo  la implementación de restricciones y pérdidas de objetivos, para la selección de nuevos entrenamientos y operaciones `(N, D, hours, GPU)`¿Qué es eso?

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Imprimir Chinchilla óptimo`(N, D)`para los presupuestos de computación `1e20`¿ Qué ?`1e22`¿ Qué ?`1e24`Comparar con la mesa de modelos reales.
   Traducción:运行`code/main.py` Impresión de presupuesto`1e20`¿Qué es esto?`1e22`¿Qué es esto?`1e24`时的Chinchilla 最优 `(N, D)`与真实模型表对比──
2. **Medium.**Implemente la curva de pérdida de la función de la computación Hoffmann.`log10(C)`Identificar cuándo la ley predice que necesitaríamos`>10^28`FLOPs para la próxima reducción de 0,1 en entropía cruzada.
   Traducción: 实现 Hoffmann 损失-计算量曲线──绘制计算最优前沿的损失对`log10(C)`◊ determinar la ley de pronóstico ¿qué tiempo necesita `>10^28`Los FLOP 才能使交叉再降低 0.1──
3. **Hard.**Aplica su propia ley de escala en 5 modelos pequeños (100K a 10M parámetros) entrenados en el mismo conjunto de datos.`α`y `E`¿Qué tan bien coinciden tus exponentes con los publicados?
   En el mismo conjunto de datos entrenar 5 个小模型 (en la misma base de datos) 参数 100K ~ 10M) 并适应自己的缩放定律──估计`α`Y `E`¿Cómo es su índice de correlación con el valor de publicación?

## Términos clave .

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

## Más Leer más Leer más

- [Kaplan et al. (2020). Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361) el primer documento de derecho de escala; poco capacitado.
  En el caso de los estudios de la Universidad de San Francisco, el estudio de la ley de la ley de los Estados Unidos, se ha realizado en el año 2000.
- [Hoffmann et al. (2022). Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556)- Chinchilla.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- [Schaeffer et al. (2023). Are Emergent Abilities of Large Language Models a Mirage?](https://arxiv.org/abs/2304.15004) la aparición como artefacto de medición.
  La capacidad de surgir es un fenómeno de la naturaleza.
- [Sardana, Frankle (2024). Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws](https://arxiv.org/abs/2401.00448)¿Por qué la sobreentrenamiento de Llama es adecuado para su carga de trabajo?
  Por qué el exceso de entrenamiento de Llama sobre su carga de trabajo es correcto.
- [Jordan et al. (2024). Muon: An optimizer for hidden layers in neural networks](https://kellerjordan.github.io/posts/muon/) 2x multiplicador de cálculo.
  Muon 优化器,2 倍计算倍增器── también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, también conocido como Muon 优化器, fue creado en el año pasado.
