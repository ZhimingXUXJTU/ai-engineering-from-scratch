# CLIP y la formación de lenguaje de visión contrastable

> CLIP (2021) de OpenAI demostró ser una idea lo suficientemente grande como para impulsar los próximos cinco años: alinear un codificador de imágenes y un codificador de texto en el mismo espacio vectorial utilizando solo pares ruidosos de captura de imágenes web y una pérdida de contraste. Cero etiquetas supervisadas. 400 millones de pares. El espacio de incorporación resultante hace una clasificación de tiro cero, recuperación de imágenes y texto y se conecta a cada VLM 2026 como su torre de visión. SigLIP 2 (2025) sustituyó a softmax por sigmoid y se amplió más allá de CLIP a menor costo. Esta lección recorre las matemáticas de InfoNCE a sigmoid loss pairwise y construye el paso de entrenamiento en stdlib Python.

> **【中文解读】**CLIP utilizó 400 millones de imágenes en la red, a través de la pérdida de comparación, para codificar imágenes y texto en el mismo espacio de volumen.

> **【拓展：CLIP→多模态大模型】**El gráfico de CLIP en comparación con el aprendizaje es la base de LLaVA, BLIP-2 etc.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, InfoNCE + sigmoid loss implementations) | **语言:** Python（标准库，InfoNCE + sigmoid 损失实现）
**Prerequisites:** Phase 12 · 01 (ViT patches), Phase 7 (Transformers) | **前置知识:** Phase 12 · 01（ViT patch），Phase 7（Transformer）
**Time:** ~180 minutes | **时间:** ~180 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·01(ViT Colocar imágenes cortadas en parche);Fase 11·04(Embeddings 向量空间概念);Fase 7(Transformer 自注意力)。本节核心数学是软max + 交叉,Fase 7·04 有详推导──
> ¿ Qué es esto ?**【类比】**CLIP  entrenamiento = "中外文词典配对游戏"── dar 32k a la imagen, la descripción), que el modelo de la escuela de dibujo traiga cada imagen y su propia descripción a la misma posición del espacio de velocidad, lanzar la descripción de otros 31999 张图片. Después de la formación, el modelo se puede poner "una foto de un gato" y el gato real dibujo juntos incluso cuando el entrenamiento no ha visto este gato──

## Objetivos de aprendizaje

- Derivar la pérdida de InfoNCE de la información mutua e implementar una versión vectorizada numéricamente estable.
  Traducción:En el caso de los datos de la información, el valor de la información se puede calcular en un cuadro de datos.
- Explica por qué la pérdida en pares sigmoide (SigLIP) se escala a lote 32768+ sin las exigencias de la máxima baja de carga total.
  China: explica por qué sigmoid 成对损失 (sigLIP) puede extenderse a 32768+ 批次大小,而无需软max 开销――
- ejecutar la clasificación de ImageNet de tiro cero mediante la construcción de plantillas de texto (`a photo of a {class}`) y tomar argmax sobre similitud cosina.
  Por ejemplo, el texto de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de los Estados Unidos de Israel.`a photo of a {class}`)并对余弦相似度取 argmax 来运行零样本 ImageNet 分类──
- Nombre de las cuatro palancas que le da el CLIP / SigLIP pre-entrenamiento: tamaño de lote, temperatura, plantilla de solicitud, calidad de datos.
  En inglés, el nombre de la forma en que se utiliza la palabra "Clip" se puede añadir a la forma en que se utiliza la palabra "Clip".

## El problema es la introducción del problema

La visión pre-CLIP fue supervisada. Recoger conjuntos de datos etiquetados (ImageNet: 1.2M imágenes, 1000 clases), entrenar una CNN, enviar. Las etiquetas son caras, las etiquetas son sesgadas con lo que los etiquetadores pueden acordar, y las etiquetas no se transfieren a nuevas tareas sin ajuste fino.

> CLIP  previa visión es de supervisión.  Recolección de datos de marcas.  ImageNet:120.000张图像,1000 个类别), entrenamiento CNN, deposición  Marcas costosas, marcas orientadas al marcador pueden alcanzar el consenso de contenido, y marcas no pueden ser transferidas a través de micro-modular a nuevas tareas 

La red de captura de imágenes tiene más de mil millones de pares de etiquetados libremente. Una foto de un retriever dorado con texto alternativo "mi perro Max en el parque" lleva una señal de supervisión  el texto describe la imagen.

>  Hay más de mil millones de imágenes de marcas en la red disponibles para uso gratuito                                                                                                                                                                                                                                                    

La respuesta de CLIP: trate los pares de imágenes-capción como una tarea de coincidencia. Dado un lote de N imágenes y N capciones, aprenda a combinar cada imagen con su propia capción contra los distractores N-1. La supervisión es "estas dos cosas pertenecen juntas; estas N-1 no lo hacen".

> Respuesta de CLIP: Dar un conjunto de N 张图像和 N 条描述, aprender en N-1 干扰项目将每图像匹配自己的描述――监督信号是"Estas dos cosas pertenecen a una sola cosa; este N-1 个不属于"―― no hay etiquetas de clase, no hay etiquetas artificiales, sólo pérdidas de comparación―

El espacio de incorporación resultante hace más de lo que CLIP fue entrenado para. ImageNet funciona de tiro cero porque "una foto de un gato" se incrusta cerca de imágenes de gatos que nunca fueron etiquetados explícitamente gatos. Esta es la apuesta que generó cada 2026 VLM.

> 得到的嵌入空间超越了CLIP's training goal──ImageNet 零样本分类有效,因为"una foto de un gato" está emplazada hasta que nunca ha sido claramente etiquetada para una foto de gato en la cercana── esto es lo que ocasionó todos los 2026 años de VLM 注──

## El concepto central.

> **【中文解读】**CLIP(Contrastivo lenguaje-imagen Pre-entrenamiento) a través de comparación de aprendizaje las imágenes y el texto se proyectan en el mismo espacio de volumen: imágenes compatibles con la distancia cercana, no compatibles con la propuesta. CLIP en 4 mil millones de imágenes con el entrenamiento superior, sin necesidad de micro-modular, es posible lograr cero-shot 图像分类, es la base de la capacidad de OpenAI de múltiples modelos.

> **【拓展：CLIP 的应用生态】**El modelo de CLIP para el aprendizaje comparativo ha generado una gran aplicación: DALL-E 2/3 con CLIP para generar imágenes, Difusión estable con OpenCLIP como filtro de seguridad, LLaVA con CLIP para conectar a un programa de programación de imágenes y comprensión de imágenes.


> **【拓展：CLIP 的 zero-shot 能力】**La capacidad más sorprendente de CLIP es la de cero disparos 分类不需要任何下游任务的训练数据, sólo tiene que darse un nombre de clase就能分类图像── en ImageNet, la tasa de cero disparos 准确率 (CCLIP ViT-L/14 ) del 76,2%) se acerca a la tasa de control total de ResNet-50 (CCLIP )  76,7%)── esta capacidad proviene de 4 mil millones de imágenes en comparación con el aprendizaje.


### El doble codificador

CLIP tiene dos torres:

> CLIP tiene dos torres:

- Código de imagen `f`: ViT o ResNet, saca un vector D-dim por imagen.
  En inglés: 图像编码器`f`:ViT o ResNet, cada imagen de salida de una D 维向量──
- Código de texto`g`: transformador pequeño, que emite un vector D-dim por subtítulo.
  En inglés: 文本编码器`g`: pequeño transformador, cada artículo describe la producción de un D 维向量──

Ambas torres normalizan sus salidas a la longitud de la unidad.`cos(f(x), g(y)) = f(x)^T g(y)`ya que ambos son la norma de unidad.

> Dos torres se producen en unidad de longitud.`cos(f(x), g(y)) = f(x)^T g(y)`, porque ambas son unidades de velocidad.

> ️ **【易错点】**忘归一化 (L2) normaliza) 关于计算相似度 → 向量模长大的样本天然有更大的点积,模型会偏向"长向量"而不是"语义匹配"──修复:每次前进 后必须`f = f / ||f||`, y luego sólo ...`cos`¿Qué es eso?
> ¿ Qué es esto ?**【困惑】**P: ¿Por qué el resemblancia de los cuerpos no utiliza la distancia de O? A: El resemblancia sólo ve la dirección no ve la longitud, a la imagen de "luz diferente pero el mismo contenido" es el rojo; la distancia de O se dirige a la longitud de la longitud.

Para un lote de pares N (imagen, leyenda) construye la similitud矩阵 `S`de forma`(N, N)`¿Qué es esto ?

> 对于一批 N 个 图像,描述) 对, construcción de forma`(N, N)`La comparación de la estructura`S`¿Qué es esto ?

```
S[i, j] = cos(f(x_i), g(y_j)) / tau
```

donde`tau`es una temperatura aprendida (CLIP inicializa a 0.07; aprendida en el espacio log).

> Entre ellos `tau`Es un parámetro de temperatura que se puede aprender.

### Perdida de información sobre la NCE

CLIP utiliza una entropía cruzada simétrica sobre filas y columnas:

> CLIP para la línea y la línea de uso para la línea de trabajo:

```
loss_i2t = CE(S, labels=identity)     # each image's positive is its own caption
loss_t2i = CE(S^T, labels=identity)   # each caption's positive is its own image
loss = (loss_i2t + loss_t2i) / 2
```

Esto es InfoNCE. La máxima suave en CE obliga a cada imagen a coincidir con su título más que con cualquier otro título en el lote. Los "negativos" son todos los otros artículos del lote. Los lotes más grandes = más negativos = señal más fuerte. CLIP entrenado en lote 32k; la escala importa.

> Éste es el softmax de InfoNCE──CE  Forza cada imagen con su propia descripción de la compatibilidad superior a todas las demás descripciones del lote──"muestreo negativo" es el resto del lote──批次越大 = 负样本越多 = 信号越强──CLIP en 32k 批次下训练;规模很重要──

> ️ **【易错点】** batch_size 太小(如 64) 训不出好 CLIP负样本太少,模型学不到"什么算真正的相似"──CLIP 原文 batch_size=32768 才有效果──如果你只能跑批=256,要么要用SigLIP(不需要大批),要么要用梯度累积模拟大批(但不等价)──
> ¿ Qué es esto ?**【类比】**InfoNCE 像"找卧底游戏":32k 张图片对应 32k 个描述, cada imagen debe encontrar su propio verdadero parecido en una pila de descripciones.

### Temperatura

`tau`Controló la nitidez de la suavidad. La distribución de tau baja → nitidez, efecto minero negativo duro. La temperatura de tau alta → suavidad, todas las muestras contribuyen. CLIP aprende log(1/tau), recortado para evitar el colapso. SigLIP 2 fija el tau inicial y utiliza un sesgo aprendido en su lugar.

> `tau`控制softmax 的度──低 tau → 尖分布,具有难负例挖掘效果──高 tau → 平滑,所有样本都有贡献──CLIP 学习 log(1/tau),并剪剪以防止崩──SigLIP 2 固定初始 tau 并使用可学习的偏置替补──

### ¿Por qué la sigmoide se mide mejor (SigLIP)

Softmax necesita toda la matriz de similitud en sincronización. En el entrenamiento distribuido debes reunir todas las incorporaciones a cada réplica, luego hacer el softmax. Esto es cuadrático en tamaño mundial para la comunicación.

> Softmax  necesita toda la matriz de similitud con el mismo ritmo. En el entrenamiento distribuido, debes incorporar cada uno a cada lado, y luego hacer softmax.

SigLIP sustituye softmax por sigmoide con base en elementos: para cada par `(i, j)`, la pérdida es una clasificación binaria de "es que estos son el par de coincidencia?" las etiquetas de clase positiva son la diagonal, todo lo demás es negativo.

> SigLIP Usado por elemento sigmoide  sustitución de suavemax: para cada por `(i, j)`, la pérdida es para "¿son compatibles?" de las categorías dos.

> ¿ Qué es esto ?**【困惑】**P: ¿Por qué softmax  necesita todo reunido y sigmoid  不需要?A: softmax 的分母是"todos los N2 个配对的相似度之和", cada GPU 必须看到全部;sigmoid 只看每个 (i,j) 配对独立判断是/否匹配,不依赖全局信息──多 GPU 训练时 sigmoid 损失可以在本地计算后减少──
> ¿ Qué es esto ?**【类比】**InfoNCE = "32k 选 1 选择题", must看完整张卷子才能做;SigLIP = "32k 个判断题(这对配对吗?)", cada respuesta independiente.

```
L = -1/N sum over (i, j) [ y_ij log sigmoid(S[i,j]) + (1-y_ij) log sigmoid(-S[i,j]) ]
```

`y_ij = 1`si`i == j`Cada GPU calcula su bloque local y sumas. SigLIP 2 escala para lotes de 32k-512k a bajo costo donde CLIP necesitaría proporcionalmente más comunicación.

> `y_ij = 1`Si es que`i == j`, en caso contrario para 0── por par de pérdidas es independiente── no necesita todo reunido── cada GPU  calcular su propio bloque 并求和──SigLIP 2 puede expandirse a bajo costo a 32k-512k 批次, mientras que CLIP 需要相应更多通信──

### Clasificación de tiro cero

Dados N nombres de clases, para cada clase crear una plantilla de texto:

> 给定 N 个类别名称,为每个类别构建文本模板:

```
"a photo of a {class}"
```

Embed cada plantilla con el codificador de texto. Embed su imagen con el codificador de imagen. Argmax cosino similaridad = clase prevista. No se ha entrenado en las clases objetivo.

> Use text editor emplazado en cada modelo. Use image editor emplazado en imagen. Argmax 余弦相似度 = 预测类别.

> ️ **【易错点】** directamente `"cat"`作为提示 → 比 `"a photo of a cat"`差 10+ 个百分点──CLIP 训练时文本端看的描述大多是完整句子,单词作为提示会让分布偏移──修复:始终使用模板 单词作为提示会让分布偏移──修复:始终使用模板`"a photo of a {class}"`,多模板集成更好──
> ¿ Qué es esto ?**【困惑】**P: ImageNet 1000 类全算一遍文嵌入 不是很慢吗?A: Sólo算一次然后缓存──1000 个提示 在文本编码器里跑一遍(毫秒级),后面每张新图片只需要1次图像嵌入+1000 次余弦相似度(向量化矩阵乘)──

Las plantillas rápidas son importantes. El papel original de CLIP utilizaba 80 plantillas por clase (planas, artísticas, fotos, pinturas, etc.) y promedió los embebidos. +3 puntos de ImageNet. El uso moderno típicamente elige una o dos plantillas.

> 提示模板很重要──CLIP 始文每类使用80模板(普通、艺术、照片、绘画等)并对嵌取平均──ImageNet 上提升3个百分点──现代用法通常选择一个两个模板──

### Las sondas lineales y la regulación de la finalidad

Una sonda lineal (traen una capa lineal sobre las características CLIP congeladas para sus clases objetivo) supera la sonda lineal en tareas dentro del dominio.

> 零样本是基线――线性探测(在结的 CLIP特征之上为目标类训练一线性层) en la tarea de dominio dentro de la que se encuentra más allá de 0样本―― total de la pequeña modificación en la zona dentro de la que se encuentra más allá de la línea, pero puede dañar la migración de 0样本――三种模式,三种权衡――

### SigLIP 2: NaFlex y características densas

SigLIP 2 (2025) añade:

> SigLIP 2(2025) Añadió:

- NaFlex: un modelo único maneja proporciones de aspecto y resoluciones variables.
  NaFlex: un modelo único para procesar la capacidad de resolución y la capacidad de distribución.
- Mejor características densas para la segmentación y la estimación de profundidad, dirigidas al uso como columna vertebral congelada en VLM.
  China: mejor densidad de características para la división y la estimación de profundidad, el objetivo es en VLM como la red principal de la red.
- Multilingüe: formado en más de 100 idiomas donde CLIP era sólo en inglés.
  En el caso de los estudiantes de más de 100 idiomas, el CLIP es sólo en inglés.
- 1B escala paramétrica donde CLIP alcanzó el máximo de 400M.
  La escala de los parámetros es de 10 mil millones, mientras que el máximo de CLIP es de 4 mil millones.

En 2026 VLM abiertos, SigLIP 2 SO400m/14 es la torre de visión predeterminada. CLIP sigue siendo la opción predeterminada para la recuperación de texto de imagen pura donde la distribución específica de entrenamiento LAION-2B coincide con el patrón de consulta.

> En el VLM abierto en 2026, SigLIP 2 SO400m/14 es una opción de visión por defecto.

### El objetivo de la presente Decisión es garantizar que los Estados miembros puedan adoptar medidas de seguridad en el marco de la aplicación de la presente Directiva.

ALIGN (Google, 2021): la misma idea que CLIP, escala de pares 1.8B, 90% ruidoso. Escales de datos ruidosas probadas. OpenCLIP (LAION): reproducción abierta de CLIP en LAION-400M / 2B, escalas múltiples, el punto de control de acceso a la apertura. EVA-CLIP: inicializa desde el modelado de imágenes enmascaradas; fuerte columna vertebral para VLMs. Básico: CLIP+ALIGN híbrido de Google. Todas las mismas familias, datos diferentes y sintonización.

> ALIGN(Google,2021): ideas similares a CLIP, 18.000 millones a escala, 90% de datos de ruido.

### El techo de tiro cero

Los modelos de clase CLIP tienen una cobertura de 76% de imagen de imagen de cero-shot (CLIP-G, OpenCLIP-G). Más allá requiere datos mucho más grandes (SigLIP 2 obtiene 80% +) o cambios de arquitectura ( cabezas supervisadas, más parámetros).

> CLIP 类模型 en ImageNet 零样本分类上限约为76%(CLIP-G、OpenCLIP-G) ・・・ Más allá de este nivel se necesita más datos(SigLIP 2 达到80%+) o la estructura cambia 监督头、更多参数) ;;基准测试正在和; el verdadero valor está en el espacio de inserción de los VLM 消费的下游.

> ¿ Qué es esto ?**【困惑】**¿Por qué CLIP no tiene un plano cero como GPT-4 para entender "qué hacen las dos personas en el cuadro"?

## Usalo con el marco de ejecución
```figure
multimodal-fusion
```

## Usalo

`code/main.py`los instrumentos:

> `code/main.py`实现:

1. Un codificador dual de juguete (carácter de imagen basado en hash, características de gráfico de texto) para que pueda ver la forma de InfoNCE sin numpy.
   Un juego de doble codificador (en inglés: a························) es un juego de cartas de la información.
2. Perdida de InfoNCE en Python puro (estabilidad numérica a través de log-sum-exp).
   En español, el nombre de la base de datos de la base de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de
3. Perdida sigmóide en pareja para comparación.
   Sinopsis: El amor de los sigmoides
4. Una rutina de clasificación de tiro cero: computa la similitud cosina contra un conjunto de instrucciones de texto, argmax para predicción.
   En el caso de los ejemplos de la letra, el número de ejemplos de la letra se puede calcular con un conjunto de ejemplos de la letra.

Los números absolutos son juguetes, la forma coincide con lo que emite un entrenador de CLIP real.

> 运行它并观察损失曲线──绝对数值是玩具级的; pero la forma coincide con la salida de la verdadera CLIP 训练机──

## Envíe el producto .

Esta lección produce`outputs/skill-clip-zero-shot.md`. Dado un conjunto de imágenes (a través de la ruta) y una lista de clases objetivo, se construyen instrucciones de texto con la plantilla CLIP, se incorporan ambos lados con un punto de control indicado (por ejemplo, `openai/clip-vit-large-patch14`), y devuelve las predicciones top-1 / top-5 con puntuaciones de similitud. La habilidad se niega a hacer afirmaciones sobre clases que no están en la lista de instrucciones.

> 本课产 出  `outputs/skill-clip-zero-shot.md`△ dado un grupo de imágenes (por vía) y un grupo de objetivos (por ejemplo, un grupo de objetos)`openai/clip-vit-large-patch14`) se incrustó en ambos lados, y regresó con un número de similitudes entre los primeros 1 y los primeros 5 预测── esta habilidad 绝对拒绝在提示列表中的类别做判断──

## Los ejercicios.

1. Implemente InfoNCE para un lote de 4 pares a mano. Construye la matriz de similitud 4x4, ejecute softmax, seleccione la diagonal, computa entropía cruzada. Verifique su implementación de Python con este cálculo manual.
   China: manual implement 4 para muestras de InfoNCE. Construir 4x4 Similaridad matriz, ejecutar softmax,提取对角线,计算交叉──验证你的Python 实现与手算一致──

2. SigLIP utiliza un parámetro de sesgo `b`Además de la temperatura: `S'[i,j] = S[i,j]/tau + b`¿ Qué papel tiene ?`b`¿Cuándo se puede jugar cuando el lote tiene un gran desequilibrio de clases (mucho más negativos que positivos por fila)?
   SigLIP además de temperatura también utiliza parámetros de parámetro`b`¿Qué es esto ?`S'[i,j] = S[i,j]/tau + b`◊ Cuando hay grandes categorías de desequilibrio (por cada tipo negativo, mucho más que el actual),`b`¿Qué hay de nuevo?

3. Construye un clasificador de disparos cero para gatos vs perros. Prueba dos plantillas rápidas: `a photo of a {class}`y `a picture of a {class}`¿El conjunto de plantillas bate solo?
   En el caso de los animales, el animal puede ser usado como un animal.`a photo of a {class}`Y `a picture of a {class}`◊ Precisión de la medición en 100 张测试图像. ¿Es la integración de modelos superior a una sola?

4. Calcule el costo de comunicación de softmax InfoNCE vs sigmoid en pareja para una carrera de 512 GPU en lote 32k. ¿Qué escalas como O(N), que como O(N^2)? Cite SigLIP Sección 4.
   En el caso de los sistemas de datos de datos, el número de datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los cuentas de los datos de los datos de los datos de los cuentas de los datos de los datos de los datos de los cuentas de los datos de los cuentas de los datos de los cuentas de los datos de los datos de los datos de los cuentas de los datos de los datos de los cuentas de los datos de los cuentas de los datos de los datos de los cuentas de datos de los cuentas de datos de los cuentas

5. Leer el documento de OpenCLIP sobre las leyes de escala (arXiv:2212.07143, Cherti et al.). Reproduce su conclusión para la escala de datos a partir de las cifras: en el tamaño fijo del modelo, ¿cuál es la relación log-lineal entre la precisión de captura cero de ImageNet y el tamaño de los datos de entrenamiento?
   China Translation: read OpenCLIP 缩放定律论文(arXiv:2212.07143,Cherti 等人)  Conclusión de la gráfica de la reconstrucción de ellos acerca de la expansión de datos: en el modelo fijo en tamaño, ¿Cuál es la relación entre la tasa de precisión de muestras de ImageNet 零 y la capacidad de datos de tamaño?

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| InfoNCE | "Contrastive loss" | Cross-entropy over a batch's similarity matrix; each item's positive is its paired item, negatives are everything else | 批次相似度矩阵上的交叉熵；每项的正样本是其配对项，负样本是所有其他项 |
| Sigmoid loss | "SigLIP loss" | Per-pair binary cross-entropy; no softmax, no all-gather, scales cheaply in distributed training | 逐对二分类交叉熵；无 softmax，无 all-gather，分布式训练中扩展成本低 |
| Temperature | "tau" | Scalar that scales logits before softmax/sigmoid; controls sharpness of the distribution | softmax/sigmoid 前缩放 logits 的标量；控制分布的锐度 |
| Zero-shot | "no-finetune classification" | Use text prompts to construct class embeddings and classify by cosine similarity; no training on target classes | 用文本提示构建类别嵌入，通过余弦相似度分类；无需在目标类别上训练 |
| Prompt template | "a photo of a ..." | Text scaffold around a class name; affects zero-shot accuracy by 1-5 points | 类别名周围的文本支架；影响零样本准确率 1-5 个百分点 |
| Dual encoder | "Two-tower" | One image encoder + one text encoder, outputs in shared D-dim space | 一个图像编码器 + 一个文本编码器，输出在共享的 D 维空间 |
| Hard negative | "Tough distractor" | A negative similar enough to the positive that the model has to work to separate them | 与正样本足够相似的负样本，模型需要努力区分它们 |
| Linear probe | "Frozen + one layer" | Train only a linear classifier on top of frozen features; measures feature quality | 仅在冻结特征之上训练线性分类器；衡量特征质量 |
| NaFlex | "Native flexible resolution" | SigLIP 2 capability to ingest images at any aspect ratio and resolution without resizing | SigLIP 2 以任意宽高比和分辨率输入图像的能力，无需调整大小 |
| Temperature scaling | "log-parametrized tau" | CLIP parametrizes `log(1/tau)` so gradients behave; clips to prevent collapse to near-zero tau | CLIP 参数化 `log(1/tau)` 使梯度行为正常；裁剪防止 tau 崩溃到接近零 |

## Más Leer más Leer más

- [Radford et al. — Learning Transferable Visual Models From Natural Language Supervision (arXiv:2103.00020)](https://arxiv.org/abs/2103.00020) el documento CLIP.
  En el caso de los países de la Unión Soviética, el gobierno de los Estados Unidos ha adoptado una política de libre comercio.
- [Zhai et al. — Sigmoid Loss for Language Image Pre-Training (arXiv:2303.15343)](https://arxiv.org/abs/2303.15343) Siglip.
  En el caso de los países de la Unión Europea, el número de países de la Unión Europea es de 1.
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) multilingüe + NaFlex.
  En inglés, el nombre de la palabra "naflex" se traduce en inglés como "naflex".
- [Jia et al. — ALIGN (arXiv:2102.05918)](https://arxiv.org/abs/2102.05918) escalar con datos ruidosos de la web.
  En español: con ruido en la red de datos.
- [Cherti et al. — Reproducible scaling laws for contrastive language-image learning (arXiv:2212.07143)](https://arxiv.org/abs/2212.07143) Ley de escalación de OpenCLIP.
  En inglés, "OpenCLIP" se abre para "OpenCLIP" y "OpenCLIP" se abre para "OpenCLIP" en inglés.
