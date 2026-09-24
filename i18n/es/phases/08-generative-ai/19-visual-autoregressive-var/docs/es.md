# Modelado autoregreso visual (VAR): predicción a la siguiente escala.

> Los modelos de difusión muestran iterativamente en el tiempo (denociando pasos). Muestras VAR iterativamente en escala  predice un token 1x1, luego 2x2, luego 4x4, hasta la resolución final, cada escala condicionando en la anterior. El documento de 2024 mostró que VAR coincide con las leyes de escalación de estilo GPT para la generación de imágenes y supera a DiT en el mismo presupuesto computacional. Esta lección construye el mecanismo principal.

> **【中文解读】**扩散模型在时间维度上代采样 (代采样) 去噪步骤), VAR 在尺度维度上代先预测 1x1 token,再2x2,再4x4,直到目标分辨率──2024年论文证明 VAR 展现了GPT 风格的规模法,在相同计算预算下超越DiT──

> **【拓展：VAR 是生成模型的新范式】**VAR volverá a regresar a la idea de que se expanda desde la " siguiente señal " hasta la " siguiente dimensión ", abriendo nuevas direcciones para la generación de imágenes.

**Type:** Build / 构建型
**Languages:** Python (with PyTorch)
**Prerequisites:** Phase 7 Lesson 03 (Multi-Head Attention / 多头注意力), Phase 8 Lesson 06 (DDPM)
**Time:** ~90 minutes

## El problema es la introducción del problema

La generación autoregresista dominó el modelado de lenguaje porque escala de manera predecible: más computación, más parámetros, menor perplejidad, mejores resultados. La generación de imágenes tuvo dos intentos principales de AR antes de 2024: PixelRNN/PixelCNN (pixel-by-pixel) y DALL-E 1 / Parti / MuseGAN (token-by-token en códigos VQ-VAE).

> La producción de imágenes de 2024 tiene dos tipos principales de AR: PixelRNN/PixelCNN (por imagen) y DALL-E 1 / Parti / MuseGAN (por token) ⋅

Los pixel y tokens se organizan en una cuadrícula 2D, pero el modelo AR tiene que visitarlos en un orden raster 1D. Un pixel de esquina temprano no tiene idea de lo que la imagen eventualmente se convierte. La calidad de generación se escalaba peor que GPT-on-text y nunca alcanzó la calidad del modelo de difusión en el cálculo coincidente.

> 两者都困难在生成顺序问题──像素和代币 排列在2D网格中,但AR 模型必须以1D光顺序访问──早期角落像素不知道图像最终将变成什么──生成质量扩展不像GPT,在相同计算量下从未达到扩散模型质量──

VAR corrige el problema de orden de generación cambiando lo que se está generando. En lugar de predecir tokens de imagen uno por uno en el espacio, VAR predice una imagen entera con mayores resoluciones. Paso 1: predice un token 1x1 (la imagen general "resumen"). Paso 2: predice una cuadrícula de tokens 2x2 (funciones más gruesas). Paso 3: predice una cuadrícula de 4x4. Paso K: predice la cuadrícula final (H/8) x ((W/8)).

> VAR 通过改变生成对象来修复生成顺序问题──不再逐空间预测图像代币, VAR 以增分辨率预测整个图像──步骤 1:预测 1x1代币(全局摘要)──步骤 2:预测 2x2代币 网格──步骤 K:预测最终网格──

Cada escala se ocupa de todas las escalas anteriores (causalmente en "orden de escala") y paralela dentro de su propia escala.

> Cada medida se concentra en todas las medidas anteriores (en la "ordenada de la medida"), y en su propia medida se corre.

> **【中文解读】**La innovación central de VAR(Visual Autoregressive) es: la generación de imágenes en orden de regreso de "por imagen/por token" a "por medida"―previo pronóstico resumen general de 1x1, de 2x2, de 4x4 hasta la resolución de objetivos―, eliminando la "preocupación de generación" de las imágenes tradicionales AR―.

> **【拓展：VAR 与扩散模型的对比】**VAR es el modelo de posterior expansión más potencial para generar imágenes nuevas.

## El concepto central.

### El tokenizador de múltiples escalas VQ-VAE

> ### VQ-VAE Tokenizer de muchas dimensiones

El VAR necesita una**multi-scale discrete tokenizer**Para una imagen x, produce una secuencia de redes de tokens de resolución cada vez mayor:

> VAR  necesita uno**多尺度离散 tokenizer** Para la imagen x, produce una serie de símbolos de resolución creciente:

```
x -> encoder -> latent f
f -> tokenize at 1x1: token grid z_1 of shape (1, 1)
f -> tokenize at 2x2: token grid z_2 of shape (2, 2)
...
f -> tokenize at (H/p)x(W/p): token grid z_K of shape (H/p, W/p)
```

Cada z_k utiliza el mismo libro de código (tamaño típico 4096-16384). La tokenización en cada escala no es independiente  se entrena de modo que la suma de los residuos en cada escala reconstruye f:

```
f ≈ upsample(embed(z_1), target_size) + ... + upsample(embed(z_K), target_size)
```

Esto es un**residual VQ**La escala k capta lo que las escalas 1..k-1 perdieron.

> Esto es un**残差 VQ**变体──尺度 k 捕获尺度 1..k-1 遗漏的内容──解码器将所有尺度嵌入并产生图像──

El tokenizer VQ a múltiples escalas se entrena una vez (como VQGAN) y luego se congela.

> Multi-dimensiones VQ tokenizer  entrenar una vez (como VQGAN) y luego 结── todos los trabajos de generación completados por el modelo de auto-regreso de la capa superior.

### Una predicción de la siguiente escala

> ### Siguiente Previsión

El modelo generativo es un transformador que ve los tokens de todas las escalas anteriores y predice los tokens en la siguiente escala.

> El modelo de producción es un transformador, ver todos los tokens de la medida anterior y predecir los de la medida siguiente.

Estructura de la secuencia de entrada:
```
[START, z_1 tokens, z_2 tokens, z_3 tokens, ..., z_K tokens]
```

Las incorporaciones de posición codifican tanto el índice de escala como la posición espacial dentro de la escala. La atención es causal en orden de escala: el token en escala k, la posición (i, j) puede atender a todos los tokens en escalas 1..k y a los tokens en escala k que vienen antes en cualquier orden intraescala que se utilice (VAR utiliza la atención posicional fija sin causalidad intraescala  todas las posiciones dentro de una escala se predicen en paralelo).

Perdida de entrenamiento: en cada escala k, predecir los tokens z_k dados todos los tokens de escala anterior. pérdida de entropía cruzada en los códigos VQ discretos. La misma estructura que GPT excepto la "secuencia" ahora está estructurada en escala.

### Generación

En la inferencia:
```
generate z_1 = sample from p(z_1)                    # 1 token
generate z_2 = sample from p(z_2 | z_1)              # 4 tokens in parallel
generate z_3 = sample from p(z_3 | z_1, z_2)         # 16 tokens in parallel
...
decode: f = sum of embed-and-upsample scales 1..K
image = VAE_decoder(f)
```

Para K = 10 escalas, la generación es de 10 pases de transformador hacia adelante. Cada pase produce toda su escala en paralelo  sin autorregressión por token dentro de una escala. Para una imagen de 256x256 esto es aproximadamente 10 pases frente a 28-50 de DiT.

> 对于 K = 10 个尺度,生成是10次变压器 前向传播──每次产生整个尺度尺度内无个别代币自归──256x256 图像约10次传播 vs DiT 的 28-50次──

### Por qué la siguiente escala gana a la siguiente

> ### ¿Por qué la siguiente medida gana la siguiente señal?

Tres victorias estructurales:

> Tres ventajas estructurales:

1. **Coarse-to-fine aligns with natural image statistics.**La percepción visual humana y los conjuntos de datos de imágenes presentan regularidades dependientes de la escala: la estructura de baja frecuencia es estable y predecible; el detalle de alta frecuencia depende del contenido de baja frecuencia.
   **从粗到细与自然图像统计一致。**低频结构稳定可预测;高频细节依赖低频内容──
2. **Parallel generation within scale.**A diferencia de los tokens AR de estilo GPT, VAR produce todos los tokens en una escala en un solo paso.
   **尺度内并行生成。**Diferente de los tokens de GPT 风格 AR, VAR un paso para generar todo el tamaño de los tokens.
3. **No generation order bias.**Los tokens en la escala k ven toda la escala k-1; no hay un sesgo "izquierda" o "por encima" que obligue a los tokens tempranos a comprometerse antes de que el contexto tardío esté disponible.
   **无生成顺序偏差。**El símbolo de la medida k 见 la medida k-1 全部──

### Ley de escala

> ### Ley de escala / 缩放定律

Tian y otros. demostró que VAR sigue una curva de escala de la ley de poder para FID en ImageNet  al igual que GPT hace para la perplejidad. El duplicar los parámetros o calcular de manera fiable reduce a la mitad el error. Este fue el primer modelo generador de imágenes en mostrar este tipo de comportamiento de escalación tan limpio como los modelos de lenguaje. El resultado es que las predicciones a escala VAR se vuelven predecibles a partir de la computación, no de suposiciones empíricas por arquitectura.

> Tian 等人 demostró que VAR en ImageNet sigue la FID de la ley de reducción de curvatura  tal como GPT a la confusión .

### Relación con la difusión

> ### Relación con el modelo de expansión

VAR y difusión comparten la misma historia de compresión de datos: ambos dividen el problema de generación en una secuencia de subproblemas más fáciles.

> VAR y la expansión comparten la misma historia de compresión de datos: todo generará problemas que se dividen en una serie de problemas más simples.

- Difusión: añadir gradualmente ruido, aprender a deshacer un paso.
  扩散: paso a paso aumentar el ruido, aprender a retirar paso a paso.
- VAR: gradualmente añadir resolución, aprender a predecir la siguiente escala.
  VAR: gradualmente aumenta la resolución, aprendizaje de la predicción de la siguiente medida.

Los dos resultados son distribuciones condicionales tratables. Empiricamente VAR es más rápido en la inferencia (menos pasa, todos paralelos dentro de una escala) y coincide o supera a DiT en la imagen de clase condicional.

> 它们 son diferentes en los diferentes ejes de los problemas. Ambas producen condiciones de distribución de tratamiento. En la experimentación, VAR  sugiere más rápido, menos se propaga, mide más o menos, y se compone de forma completa.

## Construye y realiza.
```figure
gx-var-next-scale
```

## Construye el mismo

En el`code/main.py`Usted:
1. Construye un pequeño .**multi-scale VQ tokenizer**en datos de "imagen" sintéticos (2 anillos gaussianos en dimensión).
2. Entrenamiento a **VAR-style transformer**para predecir las fichas de la siguiente escala.
3. Muestra llamando al transformador 4 veces (4 escalas) y decodificando.
4. Verificar que la formación ordenada en escala hace que la generación sea paralela dentro de una escala.

El punto es ver la máscara de atención estructurada en escala y la generación paralela dentro de la escala realmente funcionando.

> Este es un juego de realización. El objetivo es ver la estructuración de la escala y la concentración de la escala en la producción de trabajo real.

## Envíe el producto .

Esta lección produce`outputs/skill-var-tokenizer-designer.md` habilidad para diseñar un tokenizer a múltiples escalas: número de escalas, proporciones de escala, tamaño del libro de código, compartimiento residual, arquitectura de decodificadores.

> 本课产生 `outputs/skill-var-tokenizer-designer.md` diseño de tokenizador de múltiples dimensiones habilidad: tamaño número, proporción de dimensiones, tamaño de tamaño, diferencia de compartición, estructura de código.

## Los ejercicios.

1. **Scale count ablation.**Entrenar VAR con 4, 6, 8, 10 escalas. Medir la calidad de la reconstrucción frente al número de pases autoregresivos. Más escalas = residuos más finos = mejor calidad pero más pases.

2. **Codebook size.**Entrenamos a los tokenizadores con el tamaño de los códigos 512, 4096, 16384.

3. **Parallel-within-scale check.**Para un VAR entrenado, mide el patrón de atención explícitamente.

4. **VAR vs DiT scaling.**Para la misma tarea condicional de clase de ImageNet, entrenar VAR y DiT en presupuestos de parámetros iguales (por ejemplo, 33M, 130M, 458M).

5. **Text conditioning.**Extensión de VAR para tomar una incorporación de texto (CLIP agrupado) como una entrada de condicionamiento adicional a través de adaLN. Esta es la receta HART. ¿Cuánto mejora FID en la muestreo alineado con texto?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| VAR | "Visual AutoRegressive" | Image generation by next-scale prediction over a pyramid of VQ token grids |
| Next-scale prediction | "Predict coarser, then finer" | The model predicts tokens at increasing resolution scales, conditioning on all previous scales |
| Multi-scale VQ tokenizer | "Residual VQ" | VQ-VAE that produces K token grids of increasing resolution, with decoder summing all scales |
| Scale k | "Pyramid level k" | One of K resolution levels, from 1x1 at k=1 up to (H/p)x(W/p) at k=K |
| Parallel-within-scale | "One forward per scale" | All tokens at scale k are predicted in one transformer pass, not autoregressively |
| Causal-across-scales | "Scale-ordered attention" | Token at scale k can attend to all of scales 1..k but not scales k+1..K |
| Residual VQ | "Additive tokenization" | Each scale's tokens encode the residual left by lower scales; decoder sums all scale embeddings |
| VAR scaling law | "Image GPT scaling" | FID follows a predictable power law in compute, like language models' perplexity |
| HART | "Hybrid VAR + text" | Text-conditional VAR variant combining MaskGIT-style iterative decoding with VAR's scale structure |
| Scale position embedding | "(scale, row, col) triple" | Positional encoding carries both the scale index and spatial coordinates within the scale |

## Más Leer más Leer más

- [Tian et al., 2024 — "Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction"](https://arxiv.org/abs/2404.02905) el documento VAR, referencia canónica
- [Peebles and Xie, 2022 — "Scalable Diffusion Models with Transformers"](https://arxiv.org/abs/2212.09748) DiT, línea de referencia de comparación de difusión
- [Esser et al., 2021 — "Taming Transformers for High-Resolution Image Synthesis"](https://arxiv.org/abs/2012.09841) VQGAN, el tokenizer de la familia VAR se extiende
- [van den Oord et al., 2017 — "Neural Discrete Representation Learning"](https://arxiv.org/abs/1711.00937) VQ-VAE, la base de la tokenización de imágenes discretas
- [Tang et al., 2024 — "HART: Efficient Visual Generation with Hybrid Autoregressive Transformer"](https://arxiv.org/abs/2410.10812) VAR con texto condicional
