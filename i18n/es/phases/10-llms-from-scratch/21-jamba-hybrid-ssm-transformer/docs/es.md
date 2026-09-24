# Jamba  Transformador SSM híbrido  Jamba  Transformador SSM mezclado

> Los modelos espaciales de estado (SSM) y transformadores quieren cosas diferentes. Los transformadores compran calidad a través de la atención a un costo cuadrático. Los SSM compran inferencia en tiempo lineal y memoria constante a través de una recurrencia pero calidad de retraso. Jamba (marzo 2024) y Jamba 1.5 (agosto 2024) de AI21 los ponen en el mismo modelo: 1 capa transformadora por cada 7 capas de Mamba, MoE en cada otro bloque, y una ventana de contexto de 256k que se ajusta a una sola GPU de 80 GB. Mamba-3 (ICLR 2026) aprueba el lado de SSM con espacios de estado de valor complejo y proyecciones MIMO. Esta lección lee ambas arquitecturas de extremo a extremo y explica por qué la receta híbrida ha sobrevivido tres años de escalado cuando los intentos de largo contexto de pure-SSM y pure-Transformer no lo han hecho.

> **【中文解读】**Transformador Usando la segunda complejidad de la atención de cambio de calidad, SSM Usando el tiempo lineal de la teoría y los números constantes de la existencia de cambios de eficiencia pero el calidad de un poco de diferencia.

> **【拓展：SSM+Transformer→未来架构】**純SSM 和純變壓器 在长上下文任务上各有局限性──混合架构──Jamba、Mamba-3) combina las ventajas de ambos, posiblemente es la principal dirección del modelo 2026-2027 长上下文.

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 07(Transformers); estado espacial模型(SSM, Mamba) concepto;MoE(Mixura de Expertos)。本节是SSM 和 Transformer 混合架构的代表作──
> ¿ Qué es esto ?**【类比】**Jamba = "长短记忆组合"──Transformer = 短期记忆(精确但贵,每件事都需要注意力);Mamba = 长期记忆(粗略但便宜,用状态压缩历史)──1:7 比例 = 偶尔做精确记忆,大多数时候用快速压缩记忆──两者结合在 256K 上下文下既精确又便宜──

**Type:** Learn
**Languages:** Python (stdlib, layer-mix calculator)
**Prerequisites:** Phase 10 · 14 (open-model architectures), Phase 10 · 17 (native sparse attention)
**Time:** ~60 minutes

## Objetivos de aprendizaje

- Explica las tres primitivas en un bloque Jamba  capas de transformador, capas de Mamba, MoE  y la receta 1:7: incluso interdependiendo.
  解释 Jamba 块中的三个基元Transformer 层、Mamba 层、MoE及 1:7:偶数层交织方案
- En el caso de los sistemas de memoria de base, el sistema de memoria de base debe tener una función de referencia.
  Explicar cómo es la recurrencia de SSM en el macro y por qué puede lograr la teoría de la existencia de números constantes
- Computa la huella de caché KV de un modelo Jamba en un contexto de 256k y compara con lo que un modelo puro-transformer necesitaría.
  计算 Jamba 模型在 256K 上下文中的 KV 缓存占用,并与纯变压器 模型对比
- Nombrar las tres innovaciones de Mamba-3 (discretizamiento exponencial-trapezoidal, actualización de estado de valor complejo, MIMO) y el problema que cada uno tiene como objetivo.
  Explicar tres innovaciones de Mamba-3 y sus problemas específicos

## El problema es la introducción del problema

La atención es cuadrada en longitud de la secuencia. Los modelos de espacio de estado son lineales. Esa diferencia es compuesta: en 256k tokens, un mapa de atención de transformador es de 65B entradas por cabeza; el estado recurrente de un SSM es de tamaño fijo independientemente de la longitud de la secuencia.

> La diferencia en la acumulación es muy significativa: 256k de tokens, el gráfico de la concentración de transformador tiene 650 mil millones de artículos por cabeza; el estado de ciclo de SSM, independientemente de la longitud de la secuencia, es de tamaño fijo.

Los modelos de SSM puros (Mamba, Mamba-2) coinciden con la perplejidad de los transformadores a pequeñas escalas, pero se retrasan en las tareas de seguimiento de estado y fallan en algunas categorías de recuperación dentro del contexto.

> 純SSM 模型(Mamba、Mamba-2) en pequeña escala Aparece Transformer 困惑度, pero en estado de seguimiento de tareas, pero atrasado, en ciertos niveles de la siguiente revisión de clases fracasa.

La solución obvia: usar ambas. Ponga las capas de Transformer donde importa el recuerdo exacto. Usa las capas de SSM en otro lugar. Ajusta la relación. Jamba es el primer modelo de producción en enviar esta receta híbrida a escala (52B total, 12B activo, contexto de 256k, GPU de 80GB). Jamba 1.5 extiende la familia a 398B total / 94B activo. Mamba-3 (ICLR 2026) es la mejor línea de base de SSM pura actual en la que los híbridos pueden ser reconstruidos.

> 显而易见的修复:两者都用──在需要精确回忆的地方放 Transformer层──其他地方使用SSM层──调整比例──Jamba es el primer modelo de producción de este esquema de mezcla entregado a gran escala. 52B 总参数,12B 活跃,256k 上下文,单张 80GB GPU)──Jamba 1.5 将家族扩展到398B 总参数 / 94B 活跃参数──Mamba-3ICLR 2026) es la mejor línea de base pura de SSM, la estructura mezclable puede reconstruirse en torno a ella──

Esta lección lee los tres artículos y produce el modelo mental para "garanse la relación correcta".

## El concepto central.

> **【中文解读】**Jamba es un proyecto de AI21 Labs  propuesta por el MITS-Transformer  arquitectura, que Mamba  estado 空间 模型) capa con Transformer                                                                                                                                                                                                                                             

> **【拓展：SSM 与 Transformer 的融合趋势】**Mamba 等 SSM de la complejidad de la raciocinio es O(1)(estado fijo), mientras que Transformer es O(n)(KV-cache 随序列增长) ・・・ Jamba 将两者结合:SSM 处理长程依赖(高效), atención de procesamiento necesita preciso regreso de la tarea (准确) ・・・ Esta estructura mezclable puede ser el futuro de la raciocinio de la raciocinio de la longitud abajo ∼


### Un SSM en una página

Un modelo espacial de estado procesa una secuencia `x_1, ..., x_N`a través de un estado de tamaño fijo `h`¿Qué es esto ?

```
h_t = A h_{t-1} + B x_t
y_t = C h_t
```

En cada paso el estado evoluciona a través de una dinámica lineal `A`, toma información `B x_t`, y emite la salida `C h_t`- ¿ Qué ?`A, B, C`No se puede aprender.`y_t`sólo necesita`h_{t-1}`y `x_t`, no antes .`x`La memoria es constante. La inferencia es O  1 por token.

El truco para la calidad de la modelación es la estructura de`A`. S4 (Gu 2021) utilizó una matriz altamente estructurada que podía evaluarse de manera eficiente como una larga convolución durante el entrenamiento.`A, B, C`Mamba-2 (2024) simplificó aún más la estructura. Mamba-3 (2026) reaparece la complejidad en lugares específicos.

La propiedad clave: para un decodificador LLM, una capa SSM es un reemplazo drop-in para una capa de atención, con estado de tamaño fijo por capa en lugar de un caché KV creciente.

### El bloque de Jamba

Un bloque de Jamba interlea capas de acuerdo con dos números:

- `l`El uso de Jamba en el estudio de la relación entre la atención y la Mamba`l = 8`, es decir, 1 capa de transformador por cada 7 capas de Mamba (7 Mamba + 1 Atención = 8 capas por grupo).
- `e`La frecuencia de la MoE.`e = 2`, lo que significa que cada otra capa aplica MoE.

La secuencia de capas dentro de un bloque:

```
M  M  M  M  M  M  M  A    (7 Mamba + 1 Attention)
|  M  |  M  |  M  |  M    (where | marks MoE applied)
```

Cada bloque Jamba tiene 8 capas. A 4 bloques de profundidad (32 capas en total), obtienes 28 Mamba y 4 capas de atención. 16 de ellas utilizan MoE.

### ¿Por qué la proporción 1:7

AI21 ejecutó ablaciones: ¿qué relación de atención a mamba da la mejor perplejidad por parámetro Y recuerdo en contexto en sus evaluaciones de largo contexto?

- Demasiada atención (1:1): la calidad aumenta pero la memoria y la velocidad se degradan.
- Demasiada poca atención (1:15): la memoria es grande pero la recuperación en contexto falla.
- Lugar dulce: 1:7 o 1:8.

La intuición: las capas del Transformer manejan el retorno exacto y el seguimiento del estado.

### Codificación de posición

Las capas de Mamba son ellas mismas conscientes de la posición (a través de la recurrencia). Las capas de atención en los híbridos originales basados en Mamba no utilizaron RoPE  las capas SSM proporcionaron información de posición. Jamba 1.5 agrega RoPE a las capas de atención para generalización de contexto más largo, una refinación post-hoc basada en la evaluación empírica de contexto largo.

### El presupuesto de memoria

Para una forma Jamba-1 (32 capas: 28 Mamba + 4 Atención, oculta 4096, 32 cabezas de atención):

- Caché KV (sólo capas de atención): `2 * 4 * 32 * 128 * 256k * 2 = 8.4 GB`En 256k BF16 sólo las 4 capas de atención contribuyen.
- Estado del MSS: `28 * hidden * state_size`El estado típico de Mamba es de 16 por característica, oculto 4096: `28 * 4096 * 16 * 2 = 3.7 MB`- ¿Qué?

Comparar con un transformador puro en 32 capas, la misma oculta, MHA completo en 32 cabezas: `2 * 32 * 32 * 128 * 256k * 2 = 128 GB`La reducción de 8 veces en el caché de KV.`2 * 32 * 8 * 128 * 256k * 2 = 32 GB`), el híbrido 1:7 de Jamba con 16 GB es todavía 2 veces más pequeño.

Eso es lo que AI21 significa por "contexto de 256k en una GPU de 80 GB". El caché KV de un transformador puro de MHA completo no encajaría; incluso una línea de base GQA no deja espacio para pesos y activaciones; Jamba sí.

### Mamba-3: el límite de referencia de la MSS pura en 2026

Mamba-3 (ICLR 2026, arXiv:2603.15569) introduce tres innovaciones en el lado del SSM puro:

1. **Exponential-trapezoidal discretization.**Replace la discretization del método de Euler en Mamba-2 con una recurrencia más expressiva.`x_t`¿ Qué ?

2. **Complex-valued state update.**Mamba-3 re-agrega valores complejos  equivalentes a una incorporación rotativa dependiente de datos en el estado. Esto restaura las capacidades de seguimiento de estado que costaron las simplificaciones anteriores de valor real.

3. **Multi-input multi-output (MIMO) projections.**En lugar de proyecciones escalares por característica, utilice proyecciones con valor de matriz. Mejora el poder de modelado y la utilización del hardware de tiempo de inferencia sin aumentar la latencia de decodificación.

En parámetros 1.5B, Mamba-3 mejora la precisión media en el torrente inferior en 0,6 puntos sobre el Gated DeltaNet; la variante MIMO agrega 1,2 más para una ganancia total de 1,8 puntos.

Mamba-3 aún no está enviando en un híbrido de producción a escala  pero es el candidato obvio para el lado SSM del próximo modelo de la clase Jamba.

### Cuando se busca un híbrido

Los híbridos ganan cuando:

- El contexto es lo suficientemente largo como para que el caché KV de Transformer puro se vuelva doloroso (64k +).
- Las tareas mezclan la estructura de corto alcance (buena para el SSM) con el retiro a largo alcance (necesidades de Transformer).
- Quieres desplegar en presupuestos de memoria de un solo GPU donde la caché KV del Transformer por sí solo no encajaría.

Los híbridos pierden cuando:

- El contexto es corto (menos de 16k). La carga de SSM es desperdiciada; el transformador puro está bien.
- Las tareas requieren atención en todas partes (razón profundo, referencia cruzada de varios documentos).
- Se está escalado a modelos fronterizos de billones de parámetros. Pure-Transformer + MLA + MoE (estilo DeepSeek-V3) está ganando actualmente la carrera de capacidad.

### El panorama competitivo

| Model | Family | Scale | Unique claim |
|-------|--------|------|-------------|
| Mamba-2 | pure SSM | 3B | linear time, constant memory |
| Jamba | hybrid | 52B/12B | 256k on 80GB |
| Jamba 1.5 Large | hybrid | 398B/94B | enterprise-grade long-context |
| Mamba-3 | pure SSM | 1.5B (paper) | state-tracking restored |
| DeepSeek-V3 | pure Transformer + MoE | 671B/37B | frontier capability |

El panorama de 2026: el MoE de transformador puro domina la frontera, pero los híbridos poseen el nicho de contexto de 256k más.


> **【拓展：Mamba/SSM 的优势与局限】**Mamba 推理复杂度 O(1),远优于Transformer的 O(n) ・・・ pero SSM en la tarea de exacta retroceso es débil en la atención。


## Usalo con el marco de ejecución
```figure
swiglu-ffn
```

## Usalo

`code/main.py`Es una calculadora de memoria para arquitecturas híbridas. Dada una relación SSM-Transformer y una configuración de tamaño oculto / recuento de capas, calcula:

- El caché KV en el contexto objetivo.
- Memoria de estado de SSM.
- Memoria total en contexto N para una gama de formas de modelo.

La calculadora admite:

- Línea de base de Pure-Transformer (la caché de KV crece con N).
- El estilo Jamba 1: 7 híbrido.
- Pure-SSM (no hay caché KV en absoluto).

Los números son directamente de los documentos Jamba-1 y Jamba-1.5 para formas publicadas y extrapolados para variantes hipotéticas.

Considerancias de integración para un despliegue real:

- La mayoría de los servidores de inferencia de producción (vLLM, SGLang) admiten Jamba y Mamba.
- En el contexto de 256k, la ventaja de la memoria de Jamba se muestra en el rendimiento de solicitud simultánea.
- Mamba-3 como modelo independiente aún no está en producción  investigación preview en 1.5B.

## Envíe el producto .

Esta lección produce`outputs/skill-hybrid-picker.md`. Dado un perfil de longitud de contexto, mezcla de tareas, presupuesto de memoria, el documento recomienda una combinación entre un transformador puro, un híbrido de estilo Jamba y un SSM puro, con razonamiento explícito sobre las diferencias de memoria y calidad.

> 本课产 出  `outputs/skill-hybrid-picker.md` La definición de la carga de trabajo (en inglés) se basa en la definición de la duración de la configuración, el conjunto de tareas, el presupuesto de memoria, y se propone entre la combinación de la forma de transformador y la forma de SSM, y se da una idea clara sobre la ponderación de la memoria y la calidad.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Para calcular la caché KV en un contexto de 256k para un transformador puro de 32 capas (oculto 4096, 32 cabezas) y para un híbrido Jamba-1 de la misma forma.
   Traducción:运行`code/main.py`計算 32 層純變壓器 (Hidden 4096.32 头) y Jamba-1 混合模型在 256K 上下文下 KV 缓存──验证 AI21 论文声称的约8倍内存减少──

2. Modificar la calculadora para modelar un híbrido 1:3 (4 Mamba: 1 Atención) y un híbrido 1:15 (14 Mamba: 1 Atención).
   China: Modificación de calculador 建模 1:3 混合(4 Mamba: 1 Atención) y 1:15 混合(14 Mamba: 1 Atención) ―― dibujar KV 缓存与比率的关系──在什么比率下 KV 缓存等于 SSM 状态内存?

3. Leer la sección 3 del documento Jamba (arXiv:2403.19887). Explica por qué AI21 utiliza Mamba-1 en lugar de Mamba-2 a pesar de que Mamba-2 es más rápido.
   China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China

4. Compute el parámetro de la carga de MoE-cada otra capa en Jamba 1.5 Large (398B total, 94B activo). Compara la relación activa con DeepSeek-V3 (37B/671B) y explique por qué la arquitectura de Jamba empuja la relación activa más alto.
   En el caso de la construcción de Jamba, el porcentaje de activación de la plataforma de búsqueda de datos de la plataforma de datos de la plataforma de datos de Jamba es de 37B/671B.

5. Lea la sección 3 del documento Mamba-3 (arXiv:2603.15569). Explique en tres frases por qué una actualización de estado de valor complejo es equivalente a una incorporación rotativa dependiente de datos.
   China Translation: read Mamba-3 论文第 3 节──用三句话解释为什么复数值状态更新等价格与数据依赖的旋转嵌入──将答案与第7阶段第04课的RoPE推导联系起来──

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| State space model (SSM) | "Recurrence with a fixed state" | A layer with a learned recurrence `h_t = A h_{t-1} + B x_t`; constant memory per token | 状态空间模型，固定状态的递归层 |
| Selective SSM | "Mamba's trick" | Data-dependent A, B, C parameters that give the model gating-like selectivity at linear time | 选择性 SSM，数据依赖的参数实现门控 |
| Attention-to-Mamba ratio | "How many attention layers" | In Jamba, `l = 8` means 1 attention layer per 7 Mamba layers | 注意力与 Mamba 层比例，Jamba 用 1:7 |
| Jamba block | "The 8-layer group" | One attention + seven Mamba + MoE on alternate positions | Jamba 块，1 层注意力 + 7 层 Mamba + MoE |
| SSM state | "The hidden buffer" | Fixed-size per-layer state that replaces the KV cache for Mamba layers | SSM 状态，替代 Mamba 层 KV 缓存的固定大小状态 |
| 256k context | "Jamba's flagship number" | The sequence length Jamba-1 fits on a single 80GB GPU; pure Transformer cannot at that size | 256K 上下文，Jamba-1 在单张 80GB GPU 上的最大序列长度 |
| Mamba-3 | "2026 pure SSM" | Current-best pure-SSM architecture with complex state + MIMO; the baseline hybrids rebuild around | Mamba-3，2026 年最优纯 SSM 架构 |
| MIMO | "Multi-input multi-output" | Mamba-3 innovation using matrix-valued projections instead of scalar per-feature | MIMO，矩阵值投影替代标量投影 |
| Exponential-trapezoidal discretization | "Mamba-3's recurrence" | More expressive recurrence that subsumes Mamba-2's Euler-method discretization | 指数梯形离散化，更高效的递归表达 |
| Hybrid architecture | "Mix attention and SSM" | Any model that interleaves Transformer and SSM layers; Jamba is the production archetype | 混合架构，交替使用 Transformer 和 SSM 层 |

## Más Leer más Leer más

- [Lieber et al. — Jamba: A Hybrid Transformer-Mamba Language Model (arXiv:2403.19887)](https://arxiv.org/abs/2403.19887) el papel original de Jamba, ablaciones de ratio, reclamo de contexto de 256k
- [AI21 — Jamba 1.5: Hybrid Transformer-Mamba at Scale (arXiv:2408.12570)](https://arxiv.org/abs/2408.12570) la familia ampliada, 398B/94B y 12B/52B publicaciones
- [Gu, Dao — Mamba: Linear-Time Sequence Modeling with Selective State Spaces (arXiv:2312.00752)](https://arxiv.org/abs/2312.00752) el papel selectivo del MSS sobre el que se basa Jamba
- [Dao, Gu — Mamba-2 (arXiv:2405.21060)](https://arxiv.org/abs/2405.21060) el sucesor del espacio estructurado-estado-espacio simplificado
- [Lahoti et al. — Mamba-3 (arXiv:2603.15569, ICLR 2026)](https://arxiv.org/abs/2603.15569) Estado de valor complejo, MIMO, la frontera de 2026 con SSM puro
- [Gu et al. — Efficiently Modeling Long Sequences with Structured State Spaces (arXiv:2111.00396)](https://arxiv.org/abs/2111.00396) el documento S4, punto de partida de la genealogía del MSS para los LLM
