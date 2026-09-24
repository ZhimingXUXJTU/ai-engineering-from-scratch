# Cameleón y early-fusion tokens-only multimodal modelos

> Cada VLM que hemos visto hasta ahora mantiene imágenes y texto separados. Los tokens visuales vienen de un codificador de visión, fluyen a un proyector, luego se encuentran con texto dentro del LLM. La visión y el vocabulario del texto nunca se superponen. El camaleón (Meta, mayo 2024) preguntó: ¿y si lo hicieran? Entrenar un VQ-VAE que convierte una imagen en una secuencia de tokens discretos de un vocabulario compartido. Cada documento multimodal es ahora una secuencia de tokens de texto y tokens de imagen entrelazados, una sola pérdida autoregressiva. Efecto secundario: el modelo puede generar salidas de modalidad mixta  tokens de texto e imagen alternados en una sola llamada de inferencia. Esta lección lee la tesis de la fusión temprana y construye una versión de juguete de extremo a extremo.

> **【中文解读】**Chameleon (Meta,2024年5月) propuso un método de múltiples modelos: con VQ-VAE convertir imágenes en tokens de separación, compartir con tokens de texto, con un solo entrenamiento de pérdida de auto-regreso.

> **【拓展：早期融合 vs 后期融合】**Antes de todos los VLM(LLaVA、BLIP-2、Qwen-VL) todos mantienen imágenes y textos separados. La "fusión temprana" de Camelio significa que las imágenes y textos se procesan desde el principio en el mismo espacio, el modelo puede intercambiarse naturalmente para producir textos e imágenes.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, VQ-VAE tokenizer + interleaved decoder) | **语言:** Python（标准库，VQ-VAE tokenizer + 交织解码器）
**Prerequisites:** Phase 12 · 05, Phase 8 (Generative AI) | **前置知识:** Phase 12 · 05，Phase 8（生成式 AI）
**Time:** ~180 minutes | **时间:** ~180 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·05(LLaVA 后期融合方案) 、Fase 8(VQ-VAE 离散表示) 、Fase 7(Transformer next-token 训练) ⋅Chameleon es el otro extremo de "反 LLaVA": todos los modelos están usando la próxima token de pérdida。
> ¿ Qué es esto ?**【类比】**Caméleo = "el mundo"―LLaVA = 翻译机;;Visual编码器把图片翻译成LLM 能懂的语言);Chaméleo = el mundo语(图片和文本都用同样的人造语言,模型不用翻译)―Las ventajas del mundo语 son que el modelo puede generar texto y imágenes sin cambios;坏处是每种模态必须分离化(VQ-VAE 给图片"造词"), información pérdida大──

## Objetivos de aprendizaje

- Explica por qué un vocabulario compartido + pérdida única cambia lo que el modelo puede hacer.
  > 解释为什么共享词汇表 + 单一损失能改变模型能力──
- Describa cómo un VQ-VAE tokeniza una imagen en una secuencia discreta compatible con el objetivo de token siguiente de un transformador.
  > 描述 VQ-VAE 如何将图像分词为与变压器 下一代标题 目标兼容的分散序列──
- Nombre de los trucos de entrenamiento-estabilidad de Chameleon: QK-Norm, colocación de abandono, LayerNorm ordenando.
  > 列举 Chameleon's training稳定性技巧:QK-Norm、Dropout 位置、LayerNorm 顺序──
- Compara el enfoque de Q-Former de Chameleon vs BLIP-2 y describa cuándo cada uno es la opción correcta.
  > Comparar el esquema Q-Former de Chameleon con BLIP-2, describir sus escenarios adecuados.

## El problema es el contexto del problema

Los VLM basados en adaptadores (LLaVA, BLIP-2, Qwen-VL) tratan el texto e imagen como dos cosas diferentes.`embed(text_token)`Una imagen pasa por`visual_encoder(image) → projector → ... pseudo_tokens`El modelo tiene dos vías de entrada que se funden en parte.

> 适配器式 VLM(LLaVA、BLIP-2、Qwen-VL) va a ser el texto y la imagen vivido como dos cosas diferentes.`embed(text_token)`; imágenes a través de `visual_encoder(image) → projector → ... pseudo_tokens`◊ Modelo tiene dos vías de entrada en medio de la combinación.

Tres consecuencias:

> Tres resultados:

1. El LLM sólo puede consumir imágenes, no emitirlas.
   En el caso de los modelos de la imagen, el modelo de la imagen es el modelo de la imagen.
2. Los documentos de modalidad mixta (apartados y imágenes alternativas, como en un artículo) son incómodos  o analizar la entrada multimodal fuera del modelo o generaciones de cadena.
   En el caso de los modelos, el modelo de entrada de un modelo de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de diseño de
3. Desajuste distribucional. Tokens visuales y tokens de texto viven en diferentes regiones del espacio oculto, creando problemas sutiles de alineación.
   Se trata de un símbolo de la imagen y el símbolo de la escritura que se encuentra en diferentes regiones del espacio oculto, causando un problema de equilibrio.

Cameleon rechaza la premisa: las imágenes son solo secuencias de tokens discretos de un vocabulario compartido. Entrenar el modelo en documentos entrelazados, una pérdida, un decodificador autoregresivista, y desbloquear la generación de modalidad mixta de forma gratuita.

> Camelón rechazó este supuesto: imágenes son sólo un conjunto de tokens de distribución compartida.

## El concepto central.

> **【中文解读】**Chameleon (Meta) adoptó una estrategia de fusión temprana: imágenes y textos se desprenden en un solo token 序列, con el mismo Transformer 处理── imágenes a través de VQGAN 编码为离散 token,与文本 token 在同一词表中── esto es la máxima realización de la comprensión de los diferentes modelos de la unidad.

> **【拓展：早期融合 vs 晚期融合】**早期融合 (Chameleon) 将多模态统一到同一代号空间,理论上优雅但训练成本高──晚期融合 (LLaVA) 保持视觉和语言模型独立性通过桥接层连接,训练更高效──


### VQ-VAE como tokenizador de imágenes

El tokenizer es un autoencoder de variación cuantizado por vectores.

> 分词器 es un mecanismo de codificación de la misma forma.

- Encoder: CNN + ViT que mapea la imagen a un mapa de características espaciales, digamos 32x32 características de dim 256.
  China:编码器:CNN + ViT se proyecta la imagen como un espacio de características, como 32x32 dimensiones de 256 características.
- Libro de códigos: un vocabulario aprendido de vectores K (Chameleon utiliza 8192), también dim 256.
  La lengua de la lengua chino es la lengua de la lengua china.
- Cuantización: para cada característica espacial, busque la entrada de código más cercana por distancia L2.
  En inglés, el número de indices de la serie de datos se puede añadir a cada una de las características de la serie de datos.
- Decodificador: CNN que lleva las características cuantizadas de vuelta a píxeles.
  China: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CNN: CN

Formación: pérdida de reconstrucción de la AEV + pérdida de compromiso + pérdida de código de código.

> 訓練:VAE 重建损失 + 承诺损失 + 码本损失──码本索引构成图像的离散字母表──

Para el camaleón: una imagen se convierte en 32*32 = 1024 tokens extraídos de un vocabulario de 8192. Concatenate con tokens de texto (del vocabulario BPE del LLM, digamos 32000).

> 对于Chameleon:一张图像变成32*32 = 1024 个标记, 来自8192 的词汇表――与文本标记( 来自LLM 的 BPE 词汇表,如32000)拼接──最终词汇表:40192──Transformer 见一个序列,一个损失──

### El vocabulario compartido

El vocabulario de Chameleon combina tokens de texto, tokens de imagen y separadores de modalidad. Cada token tiene un solo ID. La capa de incorporación de entrada mapea cada ID a un vector oculto D-dim.

> El ejemplar de palabras de Chameleon combina los símbolos de texto, símbolos de imágenes y símbolos de forma separada. Cada símbolo tiene un único ID.

Los separadores son importantes: `<image>`y `</image>`las etiquetas se encuentran en el bracket de la secuencia de la imagen-token. en el momento de generación, si el modelo emite `<image>`, el software de aguas abajo sabe que los próximos 1024 tokens son índices VQ para enviar al decodificador para la representación de píxeles.

> Es muy importante .`<image>`Y `</image>`标签包裹图像代币 序列──生成时,如果模型输出 `<image>`, el software ya sabe que los siguientes 1024 tokens son VQ index, necesita enviar a un descifrador para hacer la imagen 染.

### Generación de modalidad mixta

La inferencia es la predicción de la próxima señal en el vocabulario compartido. Ejemplo de solicitud: "Diseña un gato y describa".

> 推理是共享词汇表中的下一代币 预测。 ejemplos提示:"画一只猫并描述它──"Chameleon 输出:

```
<image> 4821 1029 2891 ... (1024 image tokens) </image>
The cat is orange, sitting on a windowsill...
```

El modelo selecciona el orden de forma autónoma. Puede producir imagen luego texto, texto luego imagen o interlea.

> El modelo puede seleccionar por sí mismo el orden de la imagen, el texto, el texto, o el resultado de la imagen.

Comparar con los VLM adaptadores donde la generación es sólo de texto.

> Con el adaptador VLM (en inglés) sólo puede generar texto)

### Estabilidad de entrenamiento  QK-Norm, abandono, orden de LayerNorm

El entrenamiento de fusión temprana es inestable en escala.

> El ensayo de la formación temprana de la fusión en gran escala no está estable.

- QK-Norm. Aplicar LayerNorm a la consulta y proyecciones clave dentro de la atención, antes del producto punto. Previene la explosión de magnitud logit en la profundidad.
  La norma se aplica a la aplicación de la norma en la búsqueda y la clave de la proyección.
- La colocación de abandono. abandono después de cada adición residual, no sólo después de la atención y MLP. Se requiere más regularización cuando los gradientes de los tokens de imagen pueden dominar.
  En el caso de los símbolos de imagen, el nivel de la imagen puede ser mayor.
- LayerNorm ordenando. Pre-LN en la rama residual (estándar), más un LN adicional en la conexión de salto del último bloque. Estabiliza el flujo de gradiente de la capa final.
  La norma de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de la línea de trabajo de trabajo de la línea de trabajo de trabajo de la línea de trabajo de trabajo de la línea de trabajo de trabajo de la línea de trabajo de trabajo de la línea de trabajo de trabajo de la línea de trabajo de trabajo de trabajo de la línea de trabajo de trabajo de trabajo de la línea de trabajo de trabajo de trabajo de la línea de trabajo de trabajo de trabajo de trabajo de la línea de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de la línea de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de

Sin estos trucos, el entrenamiento del 34B-param Camelón divergió en múltiples puestos de control. Con ellos, converge.

>  sin estas habilidades, el Camelio de 340 mil millones de parámetros  entrenamiento en varios puntos de inspección  dispone de ellos, entrenamiento                                                                                                                                                                                                                                            

### El techo de reconstrucción del tokenizer

VQ-VAE es pérdida. En 8192 entradas de código y 1024 tokens por 512x512 imagen, la reconstrucción PSNR limita alrededor de 26-28 dB. Esto es suficiente para la gen de imagen reconocible, pero visiblemente peor que la difusión en el espacio continuo (Stable Diffusion 3 alcanza 32+ dB).

> VQ-VAE es un error de 8192 个码本条目和每张 512x512 图像 1024 个代币, reconstruye PSNR hasta el límite de 26-28 dB, pero claramente difiere de la expansión del espacio continuo.

El tokenizer es el cuello de botella. Los mejores tokenizadores (MAGVIT-v2, IBQ, SBER-MoVQGAN) elevan el techo. Emu3 (Lección 12.12) logra la generación de calidad SDXL solo a través de un mejor tokenizer.

> Por lo tanto, el sistema de clasificación de los valores de la SDXL es un sistema de clasificación de valores de la SDXL.

### Cameleón vs BLIP-2 / LLaVA

Camelion (fusión temprana, vocabulario compartido):
- Una pérdida, un decodificador.
  Un perdimiento, un desmantelamiento.
- Generar una salida de modalidad mixta.
  Se trata de un sistema de producción de productos de la industria.
- El tokenizer es el techo de calidad.
  El lenguaje de la lengua chino es el lenguaje de la lengua chino.
- Costo: Decodificador VQ-VAE por imagen generada en el camino de inferencia.
  Por ejemplo, el sistema de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen.

BLIP-2 / LLaVA (fusión tardía, torres separadas):
- La visión en, sólo mensajes de texto.
  En el caso de los medios de comunicación, el contenido de la información es el contenido de la información.
- Reutiliza el LLM pre-entrenado.
  En inglés, el inglés se traduce en inglés como "LL.L.M".
- No hay cuello de botella para el entendimiento.
  En inglés, el significado de "concierto" es "concierto".
- Barata: pase único hacia adelante.
  En el caso de la lengua inglesa, el nombre de la lengua es "Casa de la Información".

Si necesitas generación de imágenes, familia Chameleon, si sólo necesitas comprensión, el adaptador VLM es más simple y reutiliza más computación pre-entrenada.

> 按任务选择──如果需要图像生成,选择Chameleon 系列──如果只需要理解,适配器 VLM更简单且复用更多预训计算──

### Fuyu y AnyGPT

Fuyu (Adept, 2023) es un enfoque relacionado: omite el codificador de visión separado por completo, alimenta los parches de imagen crudas a través de la proyección de entrada de la LLM como si fueran tokens, sin tokenizer.

> Fuyu(Adept,2023) es un método relacionado: completamente saltando por encima del codificador de imágenes independiente, se va a parche de imagen original a través de LLM de entrada e inyección, tal como ellos son símbolos, sin distinción de palabras.

AnyGPT (Zhan et al., 2024) extiende Chameleon a cuatro modalidades: texto, imagen, habla, música. El mismo truco VQ-VAE para cada uno, transformador compartido. Cualquier generación.

> En el año 2024, el Camelón se extenderá a cuatro modalidades: texto, imágenes, voz, música, etc.


> **【拓展：早期融合的训练挑战】**La primera integración necesita una descentralización de imágenes y textos, el requisito de calidad de un tokenizador de imágenes es muy alto.


## Usalo en práctica.
```figure
vq-codebook
```

## Usalo

`code/main.py`construye un modelo de fusión temprana de juguete de extremo a extremo:

> `code/main.py`Construir un modelo de integración temprana de los juguetes de extremo a extremo:

- Un pequeño cuantificador de estilo VQ-VAE que mapea parches 8x8 a índices de código (K=16).
  Un pequeño VQ-VAE 风格的量化器,将 8x8 parche 映射到码本索引(K=16)。
- Un vocabulario compartido de (id de texto 0..31) + (id de imagen 32..47) + (separadores 48, 49).
  En el texto original, el texto se traduce como "la palabra de Dios" en la lengua árabe.
- Un decodificador autoregresor de juguete (tabla de bigramas) entrenado en subtítulos sintéticos + secuencias de tokens de imagen.
  Un juego de la forma de un símbolo de la imagen en la serie de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo de la forma de un símbolo.
- Un bucle de muestreo que emite tokens de texto + imagen alternados dado un aviso.
  En la actualidad, el sistema de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de

El código mantiene intencionalmente el transformador pequeño (bigramas) para que pueda rastrear el flujo de señal de extremo a extremo.

> 代码故意将 Transformer 保持得非常小(二元组), para que puedas de un extremo a otro rastrear el flujo de señales.

## Envíalo .

Esta lección produce`outputs/skill-tokenizer-vs-adapter-picker.md`. Dado un producto específico (entender sólo vs entender + generar, calidad de imagen requerida, presupuesto de costes), elige entre familia de camaleones (fusión temprana) y familia de LLaVA (fusión tardía) y se justifica con reglas cuantitativas.

> 本课产 出  `outputs/skill-tokenizer-vs-adapter-picker.md` Se ha elegido entre la serie Chameleon                                                                                                                                                                                                                                                         

## Los ejercicios.

1. Chameleon utiliza K=8192 entradas de código y 1024 tokens por 512x512 imagen. Estima la relación de compresión frente a una imagen RGB de 24 bits. ¿Es pérdida? ¿Qué tan pérdida?
   Camelio utiliza K=8192 个码本条目和每张 512x512 图像 1024 个代币――estimulación en relación con 24 bits RGB 图像的压缩比──有损吗?

2. ¿Puede un modelo al estilo Chameleon generar una imagen 4K en una llamada de inferencia? ¿Qué rompe primero el contexto, la calidad del tokenizer o el caché KV?
   ¿Cuántos tokens de imágenes se producen bajo la misma densidad VQ-VAE? ¿El modelo de estilo chameleón puede una vez razonar para la modificación de la generación de imágenes 4K? ¿Qué precluye la desintegración de la siguiente?

3. Implemente QK-Norm en Python puro. Dado una consulta y clave de 64 dimensiones, muestre el producto de puntos antes y después de LayerNorm. ¿Por qué es importante el control de magnitud en profundidad?
   China Translation: Usar Python para implementar la norma QK-Norm. ¿Por qué es importante el control de la amplitud en la red de profundidad?

4. Leer la sección 2.3 de Chameleon sobre estabilidad de entrenamiento. Describa el modo exacto de falla del papel observado en 34B sin QK-Norm. ¿Cuál fue la firma de "explosión normal"?
   China Translation: read Chameleon 第 2.3 节关于训练稳定性――描述论文在 340 亿参数下不使用QK-Norm 观察到的确失败模式――¿Cuál es la característica de la "范数爆炸"?

5. Extenda el decodificador de juguete para emitir una respuesta de modalidad mixta dada una solicitud de texto solo. Medir la frecuencia con la que el modelo elige la imagen primero vs texto primero dada la distribución de datos de entrenamiento 60% texto primero / 40% imagen primero.
   En el entrenamiento, los datos se distribuyen en un 60% de la prioridad del texto / 40% de la prioridad de la imagen, el modelo de medición selecciona la prioridad de la imagen frente a la frecuencia de la prioridad del texto.

## Términos clave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Early fusion | "Unified tokens" | Images converted to discrete tokens sharing the transformer's vocabulary from step one | 图像从第一步就转换为与 Transformer 共享词汇表的离散 token |
| VQ-VAE | "Image tokenizer" | CNN + ViT + codebook that maps images to integer indices the transformer can predict | CNN + ViT + 码本，将图像映射为 Transformer 可预测的整数索引 |
| Shared vocabulary | "One dictionary" | A single token ID space covering text + image + modality separators | 覆盖文本 + 图像 + 模态分隔符的单一 token ID 空间 |
| QK-Norm | "Attention stabilizer" | LayerNorm applied to query and key before their dot product, prevents norm blowup | 在 query 和 key 点积前应用 LayerNorm，防止范数爆炸 |
| Mixed-modality generation | "Text + image output" | Inference that autonomously produces interleaved text and image tokens in one pass | 推理时自主产生交替的文本和图像 token |
| Codebook size | "K entries" | Number of discrete vectors the VQ-VAE can quantize to; trades compression for fidelity | VQ-VAE 可量化到的离散向量数；压缩与保真度的权衡 |
| Tokenizer ceiling | "Reconstruction limit" | Best PSNR achievable by decoding VQ tokens; bounds the model's image quality | 解码 VQ token 可达到的最佳 PSNR；限制模型的图像质量上限 |

## Más Leer más Leer más

- [Chameleon Team — Chameleon: Mixed-Modal Early-Fusion Foundation Models (arXiv:2405.09818)](https://arxiv.org/abs/2405.09818)
  El modelo de base de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación.
- [Aghajanyan et al. — CM3 (arXiv:2201.07520)](https://arxiv.org/abs/2201.07520)
  El primer día de la muerte de Camilo, el primer día de la muerte de Camilo.
- [Yu et al. — CM3Leon (arXiv:2309.02591)](https://arxiv.org/abs/2309.02591)
  Sinopsis: El hombre es un hombre de la familia de los tres.
- [Zhan et al. — AnyGPT (arXiv:2402.12226)](https://arxiv.org/abs/2402.12226)
  En el caso de la lengua inglesa, el nombre de la lengua es "GPT".
- [Adept — Fuyu-8B blog (adept.ai)](https://www.adept.ai/blog/fuyu-8b)
  Fuyu-8B 博客,跳过视觉编码器的方案──
