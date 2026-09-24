# Flamingo y Gated Cross-Attention para VLMs de pocos disparos

> DeepMind's Flamingo (2022) hizo dos cosas antes que nadie. Mostró que un solo modelo podía procesar secuencias arbitrariamente entrelazadas de imágenes, videos y texto. Y mostró que los VLM podrían aprender en contexto  dar un prompt de algunas tomas con tres pares de ejemplos (imagen, leyenda) y el modelo subtítulos una nueva imagen sin ningún paso de gradiente. El mecanismo: capas de atención cruzada cerradas, insertadas entre las capas existentes del LLM congelado, con una puerta tanh aprendida que comienza a cero para que la capacidad de texto del LLM se preserve en la inicialización. Esta lección recorre el nuevo modelo Perceptor de Flamingo y la arquitectura de atención cruzada cerrada, el ancestro de las entradas entrelazadas de Gemini y los tokens visuales de Idefics2.

> **【中文解读】**Flamingo  Primera implementación de la escritura                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

> **【拓展：Flamingo→Gemini交织输入】**El modelo de procesamiento de imágenes de Flamingo es el modelo original de los símbolos de imágenes de Gemini y Idefics2, que se desarrolló en varios modos.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, gated cross-attention + Perceiver resampler demo) | **语言:** Python（标准库，门控交叉注意力 + Perceiver resampler 演示）
**Prerequisites:** Phase 12 · 03 (BLIP-2 Q-Former) | **前置知识:** Phase 12 · 03（BLIP-2 Q-Former）
**Time:** ~120 minutes | **时间:** ~120 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·03(BLIP-2 Q-Former,理解交叉注意力和学习可取查询);Fase 7(Transformer残差结构);Fase 11·05(In-context Learning 概念)。Flamingo 和 BLIP-2 最大的不同:BLIP-2 在 LLM 输入端桥接一次;Flamingo 在 LLM 每隔几层插入门控制层──
> ¿ Qué es esto ?**【类比】**Flamingo's Gate Control Intersection Attention = "Michie innovador de la cirugía externa"。BLIP-2 = "en el LLM grandes puertas instal un traductor"(输入端桥接一次);Flamingo = "en cada nivel de la oficina del LLM se instala una ventana"(cada 4 niveles de una puerta control intersección Attention)。门控初始为0 = 窗一开始是关闭的,模型行为和原LLM 完全一样;训练慢慢开窗 = 视觉信息逐渐注入但不破坏原文能力──

## Objetivos de aprendizaje

- Explica cómo la atención cruzada cerrada preserva la capacidad de texto de un LLM congelado en la inicialización a través de tanh(gate) = 0.
  En inglés, el título de LLM es el título de la titulación de LLM.
- Caminar a través de un nuevo modelo de perceptor: N parches de imagen → K fijas consultas "latentes" a través de la atención cruzada.
  En el caso de los usuarios de la plataforma, el usuario puede utilizar la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la ley.
- Describa cómo Flamingo maneja secuencias de texto-imagen entrelazadas con enmascaramiento causal que respete la colocación de la imagen.
  En español, el nombre de la persona que representa la imagen es Flamingo.
- Reproduce una estructura de instancias multimodal de algunas tomas (3 ejemplos de captura de imagen y luego una imagen de consulta).
  En el caso de la estructura de la muestra, el ejemplar de la muestra se muestra en el siguiente cuadro.

## El problema es la introducción del problema

BLIP-2 alimenta 32 tokens visuales en la capa de entrada de un LLM congelado. Funciona para una imagen por pedido. Pero ¿qué pasa si quieres alimentar *muchas* imágenes entrelazadas con texto, como en "aquí está la imagen A, subtítalo; aquí está la imagen B, subtítalo; ahora aquí está la imagen C, subtítalo"? La autoatención del LLM tendría que manejar tokens de imagen y tokens de texto en un solo flujo, y la pregunta de qué posiciones pueden asistir a qué imágenes se vuelve agitada.

> BLIP-2 se aplicará a cada una de las 32 fichas visuales de LLM. Pero si quieres incorporar imágenes de texto en una serie de diferentes formas, por ejemplo, "Este es un cuadro A, describirlo; este es un cuadro B, describirlo; ahora es un cuadro C, describirlo"?

La respuesta de Flamingo: no cambies en absoluto el flujo de entrada del LLM. Insertar capas de atención cruzada adicionales entre los bloques de LLM existentes. Los tokens de texto siguen fluyendo a través de la autoatención causal del LLM como siempre. Entre cada pocos bloques de LLM, los tokens de texto también atenden a las características de la imagen a través de una nueva capa cerrada. La puerta (iniciada a cero) significa que en el paso cero las nuevas capas no funcionan  el modelo se comporta exactamente como el LLM pre-entrenado. A medida que avanza el entrenamiento, la puerta se abre y la información visual comienza a fluir.

> Respuesta de Flamingo: totalmente no cambia el flujo de entrada de LLM. En los bloques existentes de LLM se insertan niveles de atención adicional entre los bloques de LLM. En el caso de los bloques de LLM, el texto se ejecuta como siempre. Cada uno de los bloques de LLM, el texto se ejecuta a través de un nuevo nivel de control.

La segunda pregunta Flamingo respondió: ¿cómo manejar un número variable de imágenes (0, 1 o muchas) por pedido? Un re-sampler Perceptor  un pequeño módulo de atención cruzada que toma cualquier número de parches que tenga y produce un número fijo de fijos tokens visuales latentes. La capa de atención cruzada LLM ve la misma forma independientemente de cuántas imágenes estén en el pedido.

> Flamingo 回答的第二个问题:如何处理每个提示中可变数量的图像(0、1或多张)?El reampler del perceptor es un pequeño módulo de atención de intercambio, que recibe un parche de cualquier cantidad y genera una cantidad fija de puntos de vista potenciales.

## El concepto central.

> **【中文解读】**Flamingo(Mente profundo) introducción de control de la información visual, inicialización de tiempo de control de la información visual, 0 (((La información visual no entra), gradualmente abierto en el proceso de entrenamiento.

> **【拓展：Flamingo 的高效适配】**Flamingo 


> **【拓展：门控机制的数学原理】**El valor de inicialización de la atención de control de entrada es 0, lo que significa que la información visual no fluye completamente en el LLM cuando comienza el entrenamiento.


### El LLM congelado

Flamingo comienza con un LLM congelado de Chinchilla 70B. Todos los pesos de 70B no se han tocado.

> Flamingo 以结的Chinchilla 70B LLM 为起点──所有700亿权重不触碰──现有文本自注意力和FFN 正常运行──

### Re-muestreo del receptor

Para cada imagen en el prompt, el ViT produce N parches de tokens. El resampler Perceptor tiene K fijas latencias de aprendizaje (Flamingo utiliza K=64).

> 对于提示中的每张图像,ViT 产生 N 个补丁代币──感知器复制器 有 K 个固定的可学习潜在向量(Flamingo 使用 K=64)──每个复制器块有两个步骤:

> ¿ Qué es esto ?**【困惑】**P: El modelo de percepción y BLIP-2 de Q-Former ¿hay alguna diferencia?A: 思想几乎一样(la consulta de aprendizaje desde el parche 提取信息), pero el modelo de percepción de Flamingo sólo hace características de compresión visual、 no participa en el entrenamiento de pérdida; Q-Former es un transformador 结构且有ITC/ITM/ITG 三个损失── se puede pensar que el modelo de percepción es la versión simplificada de Q-Former──

1. Atención cruzada: los latences K se presentan sobre los tokens de parches N (Q de los latences, K/V de los parches).
   En el caso de los parches, el parche de parches es el parche de parches.
2. Autoatención + FFN dentro de los latences.
   En inglés, el tiempo de la concentración de energía es el tiempo de la concentración de energía.

Después de 6 bloques de resampler, la salida es K = 64 tokens visuales de dim 1024, independientemente de cuántos parches haya producido el ViT. Una imagen de 224x224 (196 parches) y una imagen de 480x480 (900 parches) salen como 64 tokens de resampler.

> Después de pasar por 6 bloques de muestra, la salida es K=64 个维度为 1024的视觉代币, independientemente de cuántos parches ViT 产生了── 224x224 图像(196 个补丁) y 480x480 图像(900 个补丁) todos salen por 64 个补丁代币──

Para el vídeo, el resampler se aplica temporalmente: los parches de cada marco producen 64 latencias, y una codificación posicional temporal permite que el modelo distinga t=0 de t=N. El video completo se convierte en tokens visuales T * 64.

> 对于视频,resampler 按时间维度应用:每的补丁 产生 64 潜在向量,时间位置编码让模型区分 t=0 和 t=N──完整视频变成T * 64 视频代币──

### La atención cruzada

Entre cada capa M del LLM congelado (Flamingo utiliza M=4), insertar un nuevo bloque de atención cruzada cerrado:

> En el final de LLM de cada M 层之间(Flamingo usando M=4), insertado un nuevo bloque de atención:

```
x_after_llm_block = llm_block(x_before)
cross = cross_attn(x_after, resampler_output)
gated = tanh(alpha) * cross + x_after
x_before_next_block = gated
```

- `alpha`es un escalar aprendible iniciado a cero.
  En inglés:`alpha`Es una cantidad de aprendizaje, inicialización para cero.
- `tanh(0) = 0`, por lo que en init la rama cerrada contribuye cero.
  En inglés:`tanh(0) = 0`, por lo que la contribución inicial del tiempo de control de la división es de 0.
- Como`alpha`Si se aleja de cero, la contribución de atención cruzada crece sin problemas.
  En español: con`alpha`远离零,交叉注意力贡献平滑增长──
- La conexión residual significa que incluso una puerta completamente abierta no sobrescribe la representación de texto del LLM; solo añade información visual en la parte superior.
  El texto del LLM se muestra en el texto de la LLM, aunque el control esté completamente abierto, simplemente añade información visual.

Esta es la elección de diseño más importante en Flamingo: el acondicionamiento visual es aditivo, cerrado y cero al iniciar.

> Es la elección de diseño más importante de Flamingo: las condiciones de visión son de adición, control, inicialización para cero.

> ️ **【易错点】**Auto-realización cuando olvidar inicialización alfa=0, directamente随机初始化 → 训练前几步 LLM 文本能力就会崩塌──原因:未训练的交叉注意力输出是噪音,混入 LLM 内部表示会破坏文本知识──修复:alpha 必须初始化为0,让模型从"完美 LLM"出发,缓慢学习──
> ¿ Qué es esto ?**【类比】**零初始化门控 = "nuevos empleados ingresan a la tarea"──新员工 (新员工) 视觉层) 第一周只观察、不说话(gate=0);熟悉业务后逐渐发言(gate 慢慢打开)──直接让新员工主导决策(gate≠0初始化) 会扰乱团队原奏(破坏 LLM 文本能力)──

### Atención cruzada enmascarada para entradas entrelazadas

En un mensaje de respuesta como "<imagen A> subtítulo A <imagen B> subtítulo B <imagen C> ?", cada token de texto solo debe ver imágenes que se presentaron antes que él en la secuencia. La máscara de atención cruzada aplica: token de texto en posición `t`sólo se atiende a las fichas de resampler de imagen cuyo índice de imagen `i < i_t`donde`i_t`es la imagen más reciente antes de la posición `t`"Vea sólo la última imagen anterior" o "ve todas las imágenes anteriores" son ambas opciones válidas; Flamingo eligió la primera.

> En similar a "<imagen A> describir A <imagen B> describir B <imagen C> ?" en la sugerencia, cada símbolo de texto sólo debe ver la secuencia de imágenes que se encuentran antes de ella.`t`Sólo mira la indicación de imágenes `i < i_t`De la imagen de muestra de token, entre ellos `i_t`Es la posición`t`之前最近的图像──" Sólo mira la imagen más reciente" o "Vea todas las imágenes anteriores" son todas válidas opciones; Flamingo 选择前者──

### Aprendizaje en pocos disparos en contexto

Un mensaje de Flamingo parece:

> Flamingo 提示 se ve así:

```
<image1> A photo of a cat. <image2> A photo of a dog. <image3> A photo of a
```

El modelo ve el patrón de finalización y las salidas "pájaro" (o lo que sea que la imagen3 muestra). No hay pasos de gradiente. La capacidad de aprendizaje en el contexto congelado del LLM lleva a través de la atención cruzada cerrada.

> 模型看补全模式并输出"bird" (en inglés) 或图3 显示的任何内容) ⋅无需梯度步骤──结 LLM 上下文学习能力通过门控交叉注意力传递 es el punto clave del trabajo, también es importante por ello―

> ¿ Qué es esto ?**【困惑】**P: ¿Por qué Flamingo puede aprender en contexto y BLIP-2 no puede? A: Flamingo en LLM Cada 4 niveles injectado en información visual, LLM  interno de aprendizaje en contexto(en la Fase 11·05 aprendiz) sigue siendo un trabajo completo; BLIP-2 Colocar 32 tokens de vídeo  directamente escrito a la primera vista, LLM ponerlos como un token normal  procesar, pero el objetivo de entrenamiento no tiene un modelo de pocos disparos de forma evidente, por lo que la capacidad es débil;.

### Datos de formación

Flamingo entrenado en tres conjuntos de datos:

> Flamingo en tres grupos de datos entrenamiento:

1. MultiModal MassiveWeb (M3W): 43 millones de páginas web con imágenes y texto entrelazados, reconstruyendo el orden de lectura.
   En el contexto de la nueva versión de la web, el sitio web de la red de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de la red de Internet de la red de Internet de la red de Internet de la red de la red de Internet de la red de la red de Internet de la red de la red de Internet de la red de la red de Internet de la red de la red de la red de Internet de la red de la red de la red de Internet de la red de la red de la red de la red de Internet de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de.
2. Parejas de imagen y texto (ALIGN + LTIP): 4.4B.
   El texto original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión original de la versión de la versión original.
3. Parejas de vídeo-texto (VTP): 27 millones de cortos clips de vídeo.
   El video fue publicado en el sitio web de la revista People's Daily.

OBELICS (2023) es una reproducción abierta del corpus web entrelazado, en el que entrenan Idefics, Idefics2 y los modelos más abiertos "como Flamingo".

> Obélicos (en inglés: OBELICS) es un modelo de "classes Flamingo" abierto en el mundo de la lenguaje de la red.

### OpenFlamingo y Otter

OpenFlamingo (2023) es la reproducción abierta. La arquitectura es idéntica (re-sampler del receptor + atención cruzada cerrada en LLaMA congelada o MPT).

> OpenFlamingo(2023) ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓    ↓ ↓                                                             

Otter (2023) se basa en OpenFlamingo con la sintonización de instrucciones en MIMIC-IT (un conjunto de datos de instrucciones multimodal), mostrando trabajos de atención cruzada cerrada para instrucciones que siguen también.

> Otter(2023) para realizar instrucciones de micro-modo en OpenFlamingo  base con MIMIC-IT (MIMIC-IT) 多模态指令数据集), prueba que el control de la atención de la intersección también se aplica a las instrucciones de seguimiento.

### Los descendientes

- Idefics / Idefics2 / Idefics3: El linaje de atención cruzada cerrado de Hugging Face, progresivamente más simple (Idefics2 dejó caer el resampler a favor de tokens de parches directos con pooling adaptativo).
  La idea es que el usuario debe tener un control de la memoria de la persona.
- Transición de Flamingo a Camelio: para 2024 muchos equipos se trasladaron a la fusión temprana (lección 12.11); la atención cruzada cerrada al estilo Flamingo sigue en producción donde se requiere congelamiento de la columna vertebral.
  Traducción:Flamingo a Chameleon: hasta 2024 muchos equipos se dirigen hacia la primera integración (§ 12.11 课);
- La entrada entrelazada de Géminis: conceptualmente hereda la flexibilidad de formato entrelazado de Flamingo, aunque el mecanismo exacto es propietario.
  Ingresos de la tela de los Gemini: el concepto heredó la flexibilidad de la tela de los Flamingos, aunque el mecanismo concreto es propio.

### Comparación con BLIP-2

| | BLIP-2 | Flamingo |
|---|---|---|
| / | BLIP-2 | Flamingo |
| Visual bridge | Q-Former once at input | Gated cross-attention at every M layers |
| 视觉桥接 | 输入层一次 Q-Former | 每 M 层一次门控交叉注意力 |
| Visual tokens | 32 per image | 64 per image per cross-attn layer |
| 视觉 token | 每图 32 个 | 每个交叉注意力层每图 64 个 |
| Frozen LLM | Yes | Yes |
| 冻结 LLM | 是 | 是 |
| Few-shot in-context | Weak | Strong — the paper's centerpiece |
| 少样本上下文学习 | 弱 | 强——论文的核心亮点 |
| Interleaved inputs | No native support | Yes, the design target |
| 交织输入 | 无原生支持 | 是，设计目标 |
| Training data | 130M pairs | 1.3B pairs + 43M interleaved pages |
| 训练数据 | 1.3 亿对 | 13 亿对 + 4300 万交织网页 |
| Parameter count | 188M trained | ~10B trained (cross-attn layers) |
| 参数量 | 训练 1.88 亿 | 训练约 100 亿（交叉注意力层） |
| Compute | Days on 8 A100s | Weeks on thousands of TPUv4 |
| 计算量 | 8 块 A100 数天 | 数千块 TPUv4 数周 |

Elija BLIP-2 para una imagen única VQA en un presupuesto. Elija Flamingo/Idefics2 para el razonamiento intercalados, pocos disparos o múltiples imágenes.

> 预算有限的单图像 VQA 选 BLIP-2──交织、少样本或多图像推理选 Flamingo/Idefics2──

## Usalo con el marco de ejecución
```figure
cross-attention-fusion
```

## Usalo

`code/main.py`demuestra:

> `code/main.py`¿Qué es eso ?

1. Un nuevo modelo de Perceptor en 36 tokens de parches falsos con 8 latencias aprendizables (pura atención cruzada de Python).
   Por ejemplo, el usuario puede utilizar un modelo de parche de 36 parches falsos.
2. Un paso de atención cruzada cerrado con `alpha = 0`→ salida es igual a entrada (LLM sin cambios), entonces `alpha = 2.0`→ contribución visual mezclado.
   En inglés, el nombre de la persona que está en el centro de la vida es el nombre de la persona que está en el centro de la vida.`alpha = 0`→ 输出等于输入 (LLM 不变), entonces `alpha = 2.0`→ 视觉贡献混入──
3. Un constructor de máscaras entrelazadas que produce la máscara de atención 2D para una secuencia "(imagen 1) (texto 1) (imagen 2) (texto 2)".
   Se trata de un sistema de construcción de imágenes de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen.

## Envíe el producto .

Esta lección produce`outputs/skill-gated-bridge-diagnostic.md`. Dado la configuración de un VLM abierto (resampler Y/N, frecuencia de acceso cruzado, esquema de puertas), identifica los elementos del linaje Flamingo y explica la estrategia de congelación.

> 本课产 出  `outputs/skill-gated-bridge-diagnostic.md` Dado que el VLM está configurado para la configuración de la aplicación de un modelo, el sistema de control de la frecuencia de atención de la toma de datos, el sistema de control de datos, el sistema de control de datos y la información de la información, y el sistema de control de datos, el sistema de control de datos y la información de la información de la persona que está en el sistema de control de datos, el sistema de control de datos y la información de la persona que está en el sistema de control de datos, el sistema de control de datos y la información de datos de la persona que está en el sistema de control de datos.

## Los ejercicios.

1. Computa el número de parámetros visuales de Flamingo-9B: 9B LLM + 1.4B capas de atención cruzada cerradas + 64M resampler. ¿Qué fracción de los parámetros totales se entrenan?
   Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clásico: Clá

2. Implementar el residuo cerrado `y = tanh(alpha) * cross + x`En PyTorch. Muestre experimentalmente que con`alpha=0`¿ Qué ?`y==x`exactamente en el inicio.
   中文翻译:用 PyTorch 实现门控残差 `y = tanh(alpha) * cross + x` Prueba de experimentación`alpha=0`时    tiempo`y==x`精确成立── es una verdadera verdad.

3. Lea la sección 3.2 de OpenFlamingo (arXiv:2308.01390) sobre cómo manejan múltiples imágenes en un lote cuando cada mensaje tiene un conteo de imágenes diferente.
   En el caso de los ejemplos de la imagen, el contenido de la imagen se puede ver en el archivo de la imagen.

4. ¿Por qué la máscara de atención cruzada de Flamingo permite que un token de texto atenda a *sólo a la imagen anterior más reciente* en lugar de todas las imágenes anteriores?
   Por qué Flamingo tiene que preocuparse sólo de las imágenes más recientes y no de todas las imágenes anteriores?

5. En el contexto de pocas fotos: construye un prompt con 4 ejemplos de "imagen → color del objeto principal" para una nueva variante de Flamingo. Describa el patrón de precisión esperado a medida que varía el número de ejemplos de 0 a 8.
   La estructura contiene 4 "imágenes → Principales objetos de color" ejemplos de sugerencias.

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Perceiver resampler | "Fixed-latent cross-attention" | Module that produces K fixed tokens from a variable number of input patches | 从可变数量输入 patch 产生 K 个固定 token 的模块 |
| Gated cross-attention | "Tanh-gated bridge" | Residual layer `y = tanh(alpha)*cross + x`, learnable alpha, init 0 | 残差层 `y = tanh(alpha)*cross + x`，可学习 alpha，初始化为 0 |
| Interleaved input | "Mixed sequence" | Prompt format with images and text mixed freely in reading order | 图像和文本按阅读顺序自由混合的提示格式 |
| Frozen LLM | "No LLM gradients" | The text LLM's weights do not update; only resampler + cross-attn layers train | 文本 LLM 权重不更新；仅 resampler + 交叉注意力层训练 |
| Few-shot | "In-context examples" | Give a few (image, answer) pairs in the prompt; model generalizes without finetuning | 在提示中给几个（图像，答案）对；模型无需微调即可泛化 |
| OBELICS | "Interleaved web corpus" | Open dataset of 141M web pages with images and text in reading order | 1.41 亿网页的开放数据集，包含按阅读顺序排列的图像和文本 |
| Chinchilla | "70B frozen base" | Flamingo's frozen text LLM, from DeepMind's Chinchilla paper | Flamingo 的冻结文本 LLM，来自 DeepMind 的 Chinchilla 论文 |
| Gate schedule | "How alpha moves" | The rate at which the cross-attention gate opens during training | 训练过程中交叉注意力门控打开的速率 |
| Cross-attn frequency | "Every M layers" | How often a gated cross-attention block is inserted; Flamingo uses M=4 | 门控交叉注意力块插入的频率；Flamingo 使用 M=4 |
| OpenFlamingo | "Open reproduction" | MosaicML/LAION open checkpoint at 3-9B; architecture-identical to Flamingo | MosaicML/LAION 的 3-9B 开放检查点；架构与 Flamingo 相同 |

## Más Leer más Leer más

- [Alayrac et al. — Flamingo (arXiv:2204.14198)](https://arxiv.org/abs/2204.14198) el papel original.
  El tema es el tema de la película.
- [Awadalla et al. — OpenFlamingo (arXiv:2308.01390)](https://arxiv.org/abs/2308.01390) reproducción abierta.
  En español: "Creo que el mundo está en paz".
- [Laurençon et al. — OBELICS (arXiv:2306.16527)](https://arxiv.org/abs/2306.16527) corpus de la red entrelazado.
  En el lenguaje chino, el lenguaje es el lenguaje de la lengua.
- [Jaegle et al. — Perceiver IO (arXiv:2107.14795)](https://arxiv.org/abs/2107.14795) la arquitectura general del Perceptor.
  En inglés, el lenguaje de la lengua inglesa es el lenguaje de la lengua inglesa.
- [Li et al. — Otter (arXiv:2305.03726)](https://arxiv.org/abs/2305.03726)Descendiente flamingo con instrucciones.
  En español, el nombre de la familia de los flamencos es "Flamingo".
- [Laurençon et al. — Idefics2 (arXiv:2405.02246)](https://arxiv.org/abs/2405.02246) simplificación moderna del enfoque Flamingo.
  En inglés, el método flamingo es un método de la lengua inglesa.
