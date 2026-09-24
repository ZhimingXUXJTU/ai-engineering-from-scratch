# Desde CLIP a BLIP-2  Q-Former como puente de modalidad  desde CLIP a BLIP-2:Q-Former 模态桥接

> CLIP alinea imágenes y texto, pero no puede generar captulos, responder preguntas o mantener una conversación. BLIP-2 (Salesforce, 2023) resolvió que con un pequeño puente entrenable: 32 vectores de consulta aprendizables asisten a las características de un ViT congelado a través de la atención cruzada, luego se inserten directamente en el flujo de entrada de un LLM congelado. 188M parámetros de puente conectaron un LLM 11B a un ViT-g/14. Cada VLM basado en un adaptador hasta 2026  MiniGPT-4, InstructBLIP, primos de LLaVA  es un descendiente. Esta lección lee la arquitectura del Q-Former, explica su entrenamiento en dos etapas y construye una versión de juguete que alimenta tokens visuales en un decodificador de texto congelado.

> **【中文解读】**CLIP sólo puede ver el texto pero no puede generarse. BLIP-2 utiliza 32 volúmenes de consulta que pueden aprender a través de la intersección de atención.

> **【拓展：Q-Former→多模态架构演进】**Q-Former es el fundador de la modalidad de "结视觉编码器+结LLM+轻量桥接", MiniGPT-4、InstructBLIP、LLaVA 都是其思想的后代──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, cross-attention + learnable-query demo) | **语言:** Python（标准库，交叉注意力 + 可学习查询演示）
**Prerequisites:** Phase 12 · 02 (CLIP), Phase 7 (Transformers) | **前置知识:** Phase 12 · 02（CLIP），Phase 7（Transformer）
**Time:** ~180 minutes | **时间:** ~180 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·02(CLIP对比学习);Fase 7(Transformer自注意力和交叉注意力);Fase 11·04(Embeddings)。
> ¿ Qué es esto ?**【类比】**Pregunta: Previo = "Reporter interview"──32 个记者(question) Standing ViT 出来的 256 补丁 前面,每个人都提问自己的问题,听完回答后写下 32 条新闻摘要──这32 条摘要就是给LLM 的"新闻简报",LLM 不用看完整 256 张原始图片──

## Objetivos de aprendizaje

- Explica por qué un cuello de botella manejable entre un codificador de visión congelado y un LLM congelado supera el ajuste de costos y estabilidad de extremo a extremo.
  Traducción:Explica por qué el proceso de formación entre el programa de programación visual y el programa de formación LLM es mejor que el de costos y estabilidad.
- Implementar un bloque de atención cruzada donde un conjunto fijo de consultas de aprendizaje atienden las características de la imagen externa.
  China: implementar un bloque de atención de intercambio, en el que un grupo de preguntas fijas y aprendizables se centran en las características de imágenes externas.
- Caminar a través de la preparación de dos etapas de BLIP-2: representación (ITC + ITM + ITG) y luego generativa (perdida de LM con decodificador congelado).
  En el caso de los sistemas de aprendizaje, el sistema de aprendizaje de la lengua inglesa (ITC + ITM + ITG) se utiliza para generar aprendizaje.
- Compara Q-Former con el proyector MLP más simple utilizado en LLaVA y discuta cuándo gana cada elección.
  China Translation: Comparar Q-Former 和 LLaVA utilizaciones más sencillas de MLP 投影器,论证各自优势场景──

## El problema es la introducción del problema

Tiene un ViT congelado que produce 256 tokens de parches de dim 1408 por imagen. Tiene un LLM congelado 7B que espera embeddings de tokens de dim 4096. El puente obvio  una capa lineal de 1408 a 4096  funciona, pero alimentar a todos los 256 tokens de parches en el contexto del LLM cuesta 256 tokens adicionales por imagen.

> Tienes una conexión de viT, cada imagen genera 256 dimensiones para 1408 parches tokens. Tienes una conexión de 7B LLM, espera que la dimensión de 4096 token 嵌入. Obviamente, el puente de la línea de 1408 a 4096 está disponible, pero se va a todos los 256 parches tokens  en LLM.

La pregunta del BLIP-2: ¿puedes comprimir la representación de la imagen de 256 tokens en mucho menos tokens (digamos 32) mientras conservas suficiente información para que el LLM pueda escribir, responder preguntas y razonar sobre la imagen? ¿Puedes entrenar este puente sin tocar las espinas congeladas, manteniendo el costo de entrenamiento en los parámetros del puente?

> ¿Puedes comprimir las imágenes de 256 tokens para representarlas a menos de 32 tokens, al tiempo que conservas suficiente información para que el LLM pueda describir imágenes, responder preguntas y reflexiones? ¿Puedes entrenar esta capa de puente sin tocar la red principal, y el costo de entrenamiento se limitará a los parámetros de la capa de puente?

La respuesta: un Q-Former. 32 vectores "queri" aprendibles que atenden cruzados a los tokens de parches de ViT, produciendo un resumen visual de 32 tokens que el LLM consume. 188M parámetros totales.

> La respuesta es: Q-Former──32 个可学习的"查询"量通过交叉注意关注 ViT的补丁代币,产生LLM 消费的32代币 视觉摘要──总共188M参数──在接触LLM 之前进行对比与匹配和生成目标的训练──

## El concepto central.

> **【中文解读】**BLIP-2  Introducción de Q-Former  como 结视觉编码器和结 LLM 之间的轻量桥接层。Q-Former Utiliza un conjunto de fichas de consulta que se pueden aprender de la edición de vídeo 提取与文本最相关的视觉特征, redujo significativamente el número de entrenamientos  仅训练 Q-Former), logró un alto rendimiento de la lenguaje visual 齐──

> **【拓展：BLIP-2 的高效训练】**BLIP-2 puede completarse en un solo A100 en 12 horas, solo en Q-Former 参数), comparado con el método anterior, 10-100 veces más rápido. El diseño de Q-Former influyó en los modelos posteriores de LLaVA、InternVL, etc.


> **【拓展：Q-Former 的影响】**La idea de diseño de Q-Former (con una consulta que se puede aprender de la base de datos) es ampliamente utilizada.


### Las preguntas que se pueden aprender

El truco principal del Q-Former: en lugar de dejar que los tokens de texto del LLM atiendan a los parches de imagen, introduzca un nuevo conjunto de 32 vectores de consulta aprendizables `Q`Las consultas son parámetros del modelo  se aprenden durante el entrenamiento y se utilizan las mismas 32 consultas para cada imagen.

> Técnicas centrales de Q-Former: no dejar que el texto de LLM sea un token  enfocarse en el parche de imágenes, sino introducir un nuevo grupo de 32 `Q`, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , y , , , , , , , , , , , , , , , , , , y , , , , , , y , , , , , , y , , , , , , , , , , , y , , , , , , , , , , , , , , , , , y , , , , , , , , , , y , , , , , , , , , y , , , , , , , , , y , , , , , , , , , , y , , , , , , , , y , , , , , , , , , , y , , , , , y , y , , , , , y , , , , , , , y , , , y , y , , , y , y , y , , , , , ,

> ️ **【易错点】**Es decir, "32 preguntas son 32 preguntas de diferentes imágenes". err!32 preguntas son fijas, son las mismas para todas las imágenes.
> ¿ Qué es esto ?**【困惑】**P: 32 个查询 怎么知道每一个该看什么?A: 训练时三个损失(ITC/ITM/ITG) 会反向传播梯度告诉每一个查询 该专精什么;;最终学到的 32 维编码是"损失下降最快的那个方向",并不是为人定"颜色/物体/背景"――

Después de la atención cruzada, cada consulta contiene un resumen comprimido de la imagen  "describir el objeto principal", "describir el fondo", "contar los objetos", etc. Las consultas no se especializan literalmente en etiquetas semánticas; aprenden lo que sea la codificación que hace caer las pérdidas en el torrente descendente.

> Después de la atención de intercambio, cada consulta tiene resumen de la imagen comprimida" descripción de los objetos principales""", descripción de contexto""", número de objetos calculados" etc.

### Arquitectura

El Q-Former es un pequeño transformador (12 capas, ~ 100M parámetros) con dos caminos:

> Q-Former es un pequeño transformador (~12 niveles, ~100M de parámetros), tiene dos rutas:

1. Camino de consulta: 32 vectores de consulta fluyen a través de la autoatención (entre sí), luego la atención cruzada sobre las fichas de parche de ViT congeladas, luego FFN.
   En la actualidad, el sistema de control de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de datos de la red de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de
2. Ruta de texto: un codificador de texto similar a BERT comparte la autoatención y los pesos FFN con la ruta de consulta.
   Traducción:documentos de texto: clases de codificadores de textos de BERT y de consultas de texto de la red de mensajes de texto de la red de mensajes de texto de la red de mensajes de texto de la red de mensajes de texto de la red de mensajes de texto de la red de mensajes de texto de la red de mensajes de texto de la red de mensajes de texto de la red de mensajes de texto de la red de mensajes de texto de la red de mensajes de texto de la red de mensajes de texto de texto de la red de texto de la red de mensajes de texto de texto de la red de texto de la red de mensajes de texto de texto de la red de texto de texto de la red de texto de texto de la red de texto de texto de la red de texto de texto de la red de texto de texto de la red de texto de texto de la red de texto de texto de la red de texto de texto de la red de texto de texto de la red de texto de texto de texto de la red de texto de texto de texto de la red de texto de texto de la red de texto de texto de texto de la red de texto de texto de la red de texto de texto de la red de texto de texto de la red de texto de la red de texto de la red de texto de texto de la red de texto de la red de texto de la red de texto de la red de texto de texto de la red de texto de la red de texto de texto de la red de texto de la red de texto de la red de texto de la red de texto de la red de texto de la red de la red de texto de texto de la red de texto de texto de la red de texto de la red de texto de la red de la red de texto de la red de texto de la red de texto de texto de la red de la red de texto de la red de la red de texto de la red de la red de texto de la red de la red de texto de la red de la red de texto de la red de texto de texto de la red de la red de la red de la red de la red de texto de la red de la red de la red de la red de la red de la red de texto de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la

En el tiempo de entrenamiento, ambas vías se ejecutan. Las consultas y el texto interactúan a través de la autoatención compartida, lo que significa que las consultas pueden condicionar el texto para tareas que lo necesitan (ITM, ITG).

>                                                                                                                                                                                                                                                               

### Formación en dos etapas

El BLIP-2 se prepara en dos etapas:

> BLIP-2 分两阶段预训练:

Fase 1: aprendizaje representativo (sin LLM). Tres pérdidas:
- ITC (contraste de imagen-texto): contraste de estilo CLIP entre los tokens de consulta combinados y el token CLS de texto.
  China 文翻译:ITC(图文对比): entre el token de consulta y el token CLS 类 CLIP对比损失──
- ITM (imagen-texto coincidiendo): clasificador binario  ¿Es este par de imagen-texto coincidente?
  En el caso de los ejemplos de la lengua inglesa, el uso de la lengua inglesa es un problema.
- ITG (generación de texto basado en imágenes): LM causal en texto, condicionado a las consultas.
  En la actualidad, el contenido de la publicación se encuentra en el contenido de la publicación.

> ¿ Qué es esto ?**【类比】**Tres pérdidas de trabajo:ITC = "ver la letra" ([[gros graciosidad]]);ITM = " juzgar que la letra es realmente escrita" ([[gros graciosidad]]);ITG = "ver la letra escrita" ([[capacidad de generación]])

Sólo los trenes de Q-Former, el ViT está congelado, no hay LLM involucrado.

> 仅训练 Q-Former──ViT 结──不涉及 LLM──

Etapa 2: aprendizaje generativo. adjunta un LLM congelado (OPT-2.7B o Flan-T5-XL, etc.). proyecta los 32 resultados de la consulta a la inclusión de la LLM a través de una pequeña capa lineal. prepárelos para el texto de la solicitud. Entrena sólo la proyección lineal y el Q-Former en la pérdida de LM sobre la secuencia de solicitud + imagen + título concatenada.

> Segunda fase: generación de aprendizaje. Conexión a un LLM de finalización.

Después de la etapa 2, la proyección Q-Former + es el adaptador visual completo. En la inferencia: imagen → ViT → Q-Former → proyecto lineal → prependido a texto → congelado LLM emite salida.

> En el segundo período, Q-Former + 投影就是完整的视觉适配器──推理时:图像 → ViT → Q-Former → 线性投影 → 前置到文本 → 结 LLM 生成输出──

### Economía de parámetros

BLIP-2 con ViT-g/14 (1.1B, congelado) + OPT-6.7B (6.7B, congelado) + Q-Former (188M, entrenado) = 8B total, 188M entrenado. El Q-Former solo es ~2.4% de los parámetros de la pila completa. El costo de entrenamiento refleja esto: días en un puñado de A100s vs semanas para el final a final.

> BLIP-2 Utiliza ViT-g/14(11 mil millones,结) + OPT-6.7B(67 mil millones,结) + Q-Former(1.88 mil millones, entrenamiento) = 共 80 mil millones, entrenamiento 1.88 mil millones, Q-Former 仅占全参数约2.4%──

Calidad: BLIP-2 coincide o supera al Flamingo-80B en VQA de tiro cero mientras es 50 veces más pequeño.

> 质量:BLIP-2 在零样本 VQA 上匹配或超越 Flamingo-80B, simultáneamente menor de 50 veces.

### InstructBLIP y el Q-Former que tiene conocimiento de las instrucciones

InstructBLIP (2023) extiende el Q-Former con una entrada adicional: el texto de instrucción en sí. En el tiempo de atención cruzada, las consultas ahora tienen acceso tanto a los parches de imagen como a la instrucción. Las consultas pueden especializarse por instrucción ("contar los coches", "describir el estado de ánimo") en lugar de aprender un solo resumen fijo.

> En el caso de la instrucción de instrucción, la instrucción puede ser consultada simultáneamente en el parche de imágenes y instrucción, en lugar de aprender un resumen fijo en un solo trabajo, en la tarea de reserva hay un test de base para mejorar.

### MiniGPT-4 y el enfoque solo con proyector

MiniGPT-4 mantuvo el Q-Former pero entrenó sólo la proyección lineal de salida mientras congelaba todo lo demás. Barato, pero el costo es calidad  las consultas eran de BLIP-2, no las tuyas. Buenas para la iteración rápida, no la mejor arquitectura.

> MiniGPT-4 guarda Q-Former, pero sólo entrenar para sacar proyecciones linearias,结其他一切──便宜, pero el precio es de calidad查询 es BLIP-2, no es tuyo── adaptado a la rápida代, no es la mejor arquitectura──

### ¿Por qué LLaVA fue más simple?

LLaVA (2023, Lección 12.05) reemplazó al Q-Former con un MLP de 2 capas que proyecta cada token de parche ViT en espacio LLM  576 tokens por imagen para una cuadrícula 24x24, todos alimentados al LLM. Peor compresión pero deja que el LLM asista sobre parches crudos. En ese momento esto era controvertido; a finales de 2023 era dominante porque los datos de instrucción visual (LLaVA-Instruct-150k) demostraron que el MLP podía ser entrenado para preservar suficiente señal. El compromiso: El contexto de LLaVA se llena más rápido, pero se escala naturalmente a imágenes y videos múltiples.

> LLaVA(2023, § 12.05 课) sustituye a Q-Former con un simple MLP de 2 niveles, proyectando cada token de parche ViT en el espacio LLM 24x24 网格下 cada token de 576 imágenes, todo  a LLM.

> ¿ Qué es esto ?**【困惑】**学完本节还会问:Q-Former vs LLaVA MLP 该选哪个? 短上下文 + 高质量 → Q-Former(压缩32代币 精心训练);长上下文 + 多图/视频 → LLaVA MLP(por token 信息量大但灵活) ⋅ 2026 años la mayoría de VLM utiliza MLP, ya que los datos de instrucciones visuales son suficientes, MLP aprenderá de suficientemente bueno y más fácil de expandir―

Para 2026, el campo se divide: Q-Former sobrevive donde el presupuesto de los tokens importa (vídeo largo, muchas imágenes); el proyector MLP domina donde la calidad bruta por token es la prioridad.

> Para 2026, el campo de distribución: Q-Former en token  presupuesto importante cuando; Long video 多图像) sobrevivir; MLP 投影器 en la calidad original de cada token prioridad ocupa la principal dirección.

### La atención cruzada por la puerta: Flamingo, el antepasado

Flamingo (Ley 12.04) precedió a BLIP-2 y utilizó la misma idea de atención cruzada pero en cada capa de LLM congelada, no como un solo puente. BLIP-2 mostró que se puede comprimir a la capa de entrada solo y aún funcionar. Gemini e Idefics combinan ambos: tokens de entrada entrelazados más atención cruzada cerrada opcional para pocos disparos en contexto.

> Flamingo (第 12.04 课) Antes de BLIP-2, utiliza el mismo pensamiento de transferencia de atención pero en cada una de las capas de LLM, y no en un solo puente.

### Los descendientes de 2026

- Previo: BLIP-2, InstructBLIP, MiniGPT-4, y la mayoría de los modelos de lenguaje de vídeo por razones de presupuesto token.
  La mayoría de las películas de la televisión se han convertido en un programa de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de televisión de Estados Unidos.
- Re-sampler de percepción: variante de Flamingo (lección 12.04); familia Idefics, Eagle, OmniMAE.
  El modelo de percepción de flamenco es el siguiente:
- Proyector MLP: LLaVA, LLaVA-NeXT, LLaVA-OneVision, Cambrian-1.
  El proyecto de la película fue lanzado en el año 2000 por el director de la compañía de televisión de la compañía.
- La piscina de atención: VILA, PaliGemma.
  En el caso de los niños, el problema es que no hay nada que hacer.

Las cuatro son válidas. La pregunta decisiva es si usted está limitado en el presupuesto de token o en la calidad por token.

> Cuatro esquemas son válidos. La cuestión de la determinación es si tu límite es el token.

## Usalo con el marco de ejecución
```figure
modality-projection
```

## Usalo

`code/main.py`construye una atención cruzada al estilo de Q-Former:

> `code/main.py`Construir una biblioteca de estándares Q-Former 风格的交叉注意力:

1. Simula 256 fichas de parche de imagen (dim 128).
   En el caso de los parches de imágenes, el parche de imágenes se puede ver en el mapa de imágenes.
2. Instantánea 32 consultas de aprendizaje (dim 128).
   En la actualidad, el número de personas que han recibido una ayuda de la Universidad de Nueva York es de aproximadamente un millón de personas.
3. Ejecutar la atención cruzada de producto de punto a punto (Q de consultas, K/V de parches).
   En el caso de los que se encuentran en el centro de la ciudad, el número de personas que se encuentran en el centro de la ciudad es de aproximadamente un millón de personas.
4. Proyecto a LLM-dim (512) a través de una capa lineal.
   China:                                                                                                                                                                                                                                                              
5. Saque los 32 tokens visuales listos para LLM.
   Traducción: 输出 32 个 LLM 就绪的视觉代号.

Todo matemática en Python puro (bucles anidados sobre vectores). juguete pero forma correcta. La matriz de peso de atención se imprime para que pueda ver de qué parches se extrae cada consulta.

> Todos los cálculos matemáticos con Python puro (~) ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅                                                                                                                                                                                            

## Envíe el producto .

Esta lección produce`outputs/skill-modality-bridge-picker.md`. Dado una configuración VLM objetivo (conto de tokens del codificador de visión, presupuesto de contexto de LLM, restricciones de implementación, objetivo de calidad), recomienda el nuevo muestreo Q-Former vs MLP vs Perceiver con una justificación corta y una estimación del número de parámetros para cada puente.

> 本课产 出  `outputs/skill-modality-bridge-picker.md`△ dado un objetivo VLM 配置(vidéo编码器代币 数、LLM 上下文预算、部署约束、质量目标), que sugiere Q-Former vs MLP vs Perceiver resampler, junto con un argumento y una estimación de los parámetros de cada nivel de puente.

## Los ejercicios.

1. Implemente el bloque de atención cruzada en PyTorch. Verifique que con 32 consultas y 256 claves/valores, la matriz de peso de atención es de 32 x 256 y cada fila suma a 1 después de softmax.
   En el caso de las piezas de la pieza, el eje de la pieza es el eje de la pieza de la pieza.

2. En la etapa 1 de BLIP-2, el Q-Former ejecuta tres pérdidas simultáneamente: ITC, ITM, ITG. Escriba la firma hacia adelante para cada uno en pseudo-código. ¿Cuál de ellas requiere que la ruta del codificador de texto esté activa?
   En el primer período, Q-Former simultáneamente opera con tres perdidas: ITC, ITM, ITG.

3. Comparar los recuentos de parámetros: Q-Former (12 capas, 768 ocultas) vs un proyector MLP de 2 capas (1408 → 4096, dos capas).
   En la actualidad, el número de estudiantes de la Universidad de California en la región de California es de 1,486 estudiantes.

4. Lea la sección 3.2 del documento BLIP-2 (arXiv:2301.12597) sobre cómo se inicializa el Q-Former.
   La primera parte de la primera fase de la formación de la base de la base de la base de la formación de la base de la base de la formación de la base de la formación de la base de la formación de la formación de la base de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la

5. Para un video de 10 minutos a 1 FPS muestrado a 60 cuadros, calcular el costo de los tokens por cuadro en (Q-Former → 32 tokens/frame) vs (proyector MLP → 576 tokens/frame). ¿Cuál encaja en una ventana de contexto de LLM de 128k-token?
   Para 10 minutos de vídeo en 1 FPS 采样为60 ,计算每代币 成本:(Q-Former → 32 token/) vs.

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Q-Former | "Querying transformer" | Small transformer with 32 learnable query vectors that cross-attend to frozen ViT features | 带有 32 个可学习查询向量的小型 Transformer，交叉关注冻结的 ViT 特征 |
| Learnable queries | "Soft prompt for vision" | A fixed set of parameters that serve as the query side of cross-attention; learned per model, shared across all inputs | 作为交叉注意力查询侧的固定参数集；按模型学习，所有输入共享 |
| Cross-attention | "Q from here, K/V from there" | Attention where query, key, and value come from different sources; how the queries pull from ViT patches | 查询、键和值来自不同来源的注意力；查询如何从 ViT patch 提取信息 |
| ITC | "Image-text contrastive" | CLIP-style loss applied to Q-Former pooled queries vs text CLS | 应用于 Q-Former 池化查询与文本 CLS 的类 CLIP 对比损失 |
| ITM | "Image-text matching" | Binary classifier on hard-negative-mined pairs; forces the queries to discriminate fine-grained mismatches | 难负例挖掘对上的二分类器；强制查询区分细粒度不匹配 |
| ITG | "Image-grounded text generation" | Causal LM loss where text is generated conditioned on queries; forces queries to encode text-decodable content | 以查询为条件生成文本的因果 LM 损失；强制查询编码可解码为文本的内容 |
| Two-stage pretraining | "Representation then generative" | Stage 1 trains Q-Former alone (ITC/ITM/ITG); Stage 2 attaches frozen LLM and trains only the projection + Q-Former | 第一阶段仅训练 Q-Former；第二阶段连接冻结 LLM，仅训练投影 + Q-Former |
| Frozen backbone | "Do not finetune" | The vision encoder and LLM weights are fixed; only the bridge trains | 视觉编码器和 LLM 权重固定；仅训练桥接层 |
| Projection head | "Linear to LLM dim" | Final linear layer mapping Q-Former output to the LLM's embedding dimension | 将 Q-Former 输出映射到 LLM 嵌入维度的最终线性层 |
| Perceiver resampler | "Flamingo's version" | Similar learnable-query cross-attention, used by Flamingo at every layer rather than as a single bridge | 类似的可学习查询交叉注意力，Flamingo 在每层使用而非单一桥接 |

## Más Leer más Leer más

- [Li et al. — BLIP-2 (arXiv:2301.12597)](https://arxiv.org/abs/2301.12597) el papel central.
  El texto original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original.
- [Li et al. — BLIP (arXiv:2201.12086)](https://arxiv.org/abs/2201.12086) el predecesor con el trío ITC/ITM/ITG.
  En el texto original, se incluye el texto de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la de la de la de la página de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la
- [Li et al. — ALBEF (arXiv:2107.07651)](https://arxiv.org/abs/2107.07651) "align antes de fusión"  el ancestro conceptual del entrenamiento de la etapa 1.
  Traducción: "Prederecordar la formación"
- [Dai et al. — InstructBLIP (arXiv:2305.06500)](https://arxiv.org/abs/2305.06500) Q-Former, consciente de las instrucciones.
  En inglés, el nombre de la persona que se encuentra en el idioma chino es Q-Former.
- [Zhu et al. — MiniGPT-4 (arXiv:2304.10592)](https://arxiv.org/abs/2304.10592) enfoque solo con proyector.
  En inglés, sólo se puede interpretar el tema.
- [Jaegle et al. — Perceiver IO (arXiv:2107.14795)](https://arxiv.org/abs/2107.14795) arquitectura general para la atención cruzada entre las preguntas y las enseñanzas.
  La estructura general de la atención es la de la atención.
