# Transformadores de visión (ViT)

> Una imagen es una cuadrícula de parches. Una oración es una cuadrícula de tokens. El mismo transformador se come a ambos.

> **【中文解读】**ViT Colocar imágenes cortadas en parche 当作 token 序列处理──理解 ViT = comprensión Transformer no se limita a la NLP──CLIP、DALL-E、Sora 都基于Transformer──

**Type:** Hands-on | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro)
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

Antes de 2020, la visión por ordenador significaba convulsiones. Cada SOTA en ImageNet, COCO y puntos de referencia de detección utilizaban una columna vertebral de CNN.

> Antes de 2020, la visión de computadoras significaba volúmenes. Todas las SOTA de la imagen de la red, COCO y la base de análisis utilizaban la red de ADN de CNN.

Dosovitskiy et al. (2020)  "Una imagen vale 16x16 palabras"  mostró que se pueden soltar las convulsiones por completo. Cortar una imagen en parches de tamaño fijo, proyectar linealmente cada parche en un embebedido, alimentar la secuencia a un codificador transformador de vainilla. A escala suficiente (ImageNet-21k pre-entrenamiento o mayor), ViT coincide o supera a los modelos basados en ResNet.

> Dosovitskiy 等人(2020) "一张图像值 16x16 个词"证明可以完全放弃卷积──将图像切成固定大小的补丁,线性投影每补丁为嵌入,将序列送入标准变压器编码器──在足够大的下规模(ImageNet-21k 预训练或更大),ViT可以匹配或超越基于ResNet的模型──

ViT fue el comienzo de un patrón más amplio en 2026: una arquitectura, muchas modalidades. Whisper tokeniza el audio. ViT tokeniza las imágenes. Tokens de acción para robótica. Tokens de píxeles para video.

> ViT es el punto de partida de una tendencia más amplia de 2026: una estructura, varios modelos, etc.

Para 2026, ViT y sus descendientes (DeiT, Swin, DINOv2, ViT-22B, SAM 3) poseen la mayor parte de la visión.

> Para 2026, el ViT y sus sucesores (DeiT, Swin, DINOv2, ViT-22B, SAM 3) ocuparon la mayor parte del campo visual.

> **【中文解读】**La imagen puede ser cortada como un texto en una serie de "tokens" ⋅ 224x224                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

## El concepto central.

![Image → patches → tokens → transformer](../assets/vit.svg)

### Paso 1  Aplicar

Dividiendo una`H × W × C`imagen en una`N × (P·P·C)`Secuencia de parches planos.`224 × 224`imagen, `16 × 16`parches → 196 parches de 768 valores cada uno.

> ¿ Qué ?`H × W × C`图像分为 `N × (P·P·C)`序列──tipo de configuración:`224 × 224`Las imágenes,`16 × 16`Parche → 196 个 768 值的 parche──

```
image (224, 224, 3) → 14 × 14 grid of 16x16x3 patches → 196 vectors of length 768
```

El tamaño del parche es la palanca. Parches más pequeños = más tokens, mejor resolución, costo de atención cuadrática. Parches más grandes = más gruesos, más baratos.

> Parche: mayor tamaño es control de parametros. Parche más pequeño = más tokens.

### Paso 2  incorporación lineal

Una matriz única aprendida proyecta cada parche plano a `d_model`. Equivalente a una convolución del tamaño del núcleo `P`y paso .`P`En PyTorch esto es literalmente`nn.Conv2d(C, d_model, kernel_size=P, stride=P)` una aplicación de dos líneas.

> Una matriz de aprendizaje se va a cada parche plano proyectar`d_model`◊ igual precio a la energía nuclear`P`、步长为 `P`En PyTorch en el centro es`nn.Conv2d(C, d_model, kernel_size=P, stride=P)`两行实现──

> **【拓展：Swin Transformer 的层级设计】**标准 ViT 使用固定补丁 大小和全局注意力,计算量 O(N^2)。Swin Transformer 引入层级结构:在小补丁上做局部窗口注意力,逐层合并补丁 扩大感受野。 Esto hace que la complejidad de cálculo sea O(N), mientras que se conserva la capacidad de extraer características de nivel。Swin en tareas de inspección y división sigue siendo superior a la estándar ViT。

### Paso 3  Prepend `[CLS]`token, añadir inserciones posicionales

- Prepara un aprendizaje .`[CLS]`Su estado oculto final es la representación de imagen utilizada para la clasificación.
  En la actualidad, el programa está disponible para todos los estudiantes.`[CLS]`token── su estado oculto final se utiliza para la representación de imágenes de la clase
- Añadir embebidos posicionales aprendibles (original ViT) o sinusoidales 2D (variantes posteriores).
  China: 添加可学习的位置嵌入 (en inglés)
- En 2024+ RoPE se amplió a 2D para la posición, a veces sin incorporaciones explícitas.
  Después de 2024 años, RoPE se expandió a 2D  ubicación codificación, a veces no necesita un emplazamiento evidente.

### Paso 4  codificador estándar de transformador

La pila de bloques de`LayerNorm → Self-Attention → + → LayerNorm → MLP → +`No hay capas específicas de visión. Este es el punto de inflexión pedagógico del documento.

> 堆叠 L 个 `LayerNorm → Self-Attention → + → LayerNorm → MLP → +`块──与BERT 完全相同──没有视觉特有的层──这是本文的教学要点──

### Paso 5  cabeza

Para su clasificación: tomar `[CLS]`estado oculto → lineal → softmax. para DINOv2 o SAM, descartar `[CLS]`, usar los embebidos de parches directamente.

>  分类: 取`[CLS]`隐藏状态 → 线性层 → softmax──对 DINOv2或 SAM,丢弃 `[CLS]`, directamente usar parche 嵌入──

### Las variantes que importaron

| Model | Year | Change |
|-------|------|--------|
| 模型 | 年份 | 变化 |
| ViT | 2020 | The original. Fixed patch size, full global attention. |
| ViT | 2020 | 原始版本。固定 patch 大小，全局注意力。 |
| DeiT | 2021 | Distillation; trainable on ImageNet-1k only. |
| DeiT | 2021 | 蒸馏；仅在 ImageNet-1k 上可训练。 |
| Swin | 2021 | Hierarchical with shifted windows. Fixed sub-quadratic cost. |
| Swin | 2021 | 层级结构，移位窗口。固定的亚二次成本。 |
| DINOv2 | 2023 | Self-supervised (no labels). Best general vision features. |
| DINOv2 | 2023 | 自监督（无标签）。最佳通用视觉特征。 |
| ViT-22B | 2023 | 22B params; scaling laws apply. |
| ViT-22B | 2023 | 22B 参数；缩放定律适用。 |
| SigLIP | 2023 | ViT + language pair, sigmoid contrastive loss. |
| SigLIP | 2023 | ViT + 语言配对，sigmoid 对比损失。 |
| SAM 3 | 2025 | Segment anything; ViT-Large + promptable mask decoder. |
| SAM 3 | 2025 | 分割一切；ViT-Large + 可提示的掩码解码器。 |

### ¿Por qué tardó un tiempo?

ViT necesita *muchos* datos para coincidir con las CNN porque no tiene ninguno de los sesgos inductivos de CNN (invarianza de traducción, localidad). Sin imágenes etiquetadas >100M o una fuerte pre-entrenamiento auto supervisado, las CNN todavía ganan en la computación coincidente. DeiT lo solucionó en 2021 con trucos de destilación; DINOv2 lo solucionó permanentemente en 2023 con auto-supervisión.

> ViT necesita una gran cantidad de datos para igualar el rendimiento de CNN, ya que no tiene preferencias de clasificación de CNN (平移不变性、局部性) ⋅ sin imágenes de marcado o entrenamiento previo de vigilancia de más de 1 mil millones de张, CNN sigue ganando en la misma cantidad de cálculos.

> **【中文解读】**La vulnerabilidad de la red de datos de ViT es de doble espada: se necesita más datos para igualar los resultados de CNN, ya que CNN tiene preferencias de red de datos de la naturaleza y de la localización. Pero cuando la cantidad de datos es lo suficientemente grande, la expansión de ViT es mucho mayor que la de CNN.

> **【拓展：ViT 在多模态系统中的角色】**CLIP utiliza ViT 编码图像、Transformer 编码文本, mediante comparación de aprendizaje a los dos modelos──DALL-E 和 Sora utiliza ViT comprensión de imágenes/vídeos, regenerar en nuevo contenido──SAM(Segmento Cualquier cosa) utiliza ViT 作为主干网络实现通用图像分化──ViT 已成为多模态 AI's visual base模块──

## Construye y realiza.
```figure
n5-patch-stream
```

## Construye el mismo

¿ Qué ?`code/main.py`.Pure-stdlib patchify + linear embedding + controles de cordura. No entrenamiento  ViT a cualquier escala realista necesita PyTorch y horas de tiempo de GPU.

> 参见 `code/main.py`◊ Patchfifi + 线性嵌入 + 合理性检查──无训 任何实际规模的 ViT 都需要 PyTorch 和数小时的GPU 时间──

### Paso 1: Imagen falsa

Una imagen RGB 24 × 24 como una lista de filas de `(R, G, B)`Usamos 6×6 parches → 16 parches, 108-d incorporando vector cada uno.

> Una imagen RGB 24 × 24 , en`(R, G, B)`Se utiliza un parche de 6×6 → 16 parches, cada uno de 108 dimensiones de inserción en el parche.

### Paso 2: Aparecer

```python
def patchify(image, P):
    H = len(image)
    W = len(image[0])
    patches = []
    for i in range(0, H, P):
        for j in range(0, W, P):
            patch = []
            for di in range(P):
                for dj in range(P):
                    patch.extend(image[i + di][j + dj])
            patches.append(patch)
    return patches
```

Cada VT utiliza este orden.

> Luz  orden: red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de.

### Paso 3: incrustado lineal

Multiplica cada parche plano por un aleatorio `(patch_flat_size, d_model)`Matrix. Verifique que la forma de salida es `(N_patches + 1, d_model)`después de la preposición `[CLS]`¿ Qué ?

> Cada parche se multiplicará por un parche`(patch_flat_size, d_model)`矩阵──验证在添加 `[CLS]`后输出形状为 `(N_patches + 1, d_model)`¿Qué es eso?

### Paso 4: Parámetros de conteo para un ViT realista

Imprima el parámetro para ViT-Base: 12 capas, 12 capas, d=768, parche=16. Compara con ResNet-50 (~25M). ViT-Base aterriza en ~86M. ViT-Large ~307M. ViT-Huge ~632M.

> 打印 ViT-Base 参数:12 层、12 头、d=768、patch=16──与ResNet-50(约25M)对比──ViT-Base 约86M──ViT-Large 约307M──ViT-Huge 约632M──

## Usalo con el marco de ejecución

```python
from transformers import ViTImageProcessor, ViTModel
import torch
from PIL import Image

processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
model = ViTModel.from_pretrained("google/vit-base-patch16-224-in21k")

img = Image.open("cat.jpg")
inputs = processor(img, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, 197, 768): [CLS] + 196 patches
cls_emb = out[:, 0]                       # image representation
```

**DINOv2 embeddings are the 2026 default for image features.**Congelar la columna vertebral, entrenar una cabeza pequeña funciona para la clasificación, recuperación, detección, subtítulos los puntos de control DINOv2 de Meta superan a CLIP en todas las tareas de visión no textual

> **DINOv2 嵌入是 2026 年图像特征的默认选择。**结骨干网络,训练一个小头──适用于分类,检查,检测,图像描述──Meta's DINOv2 检查点在每个非文本视觉任务上都优于CLIP──

**Patch-size picking.**Los modelos pequeños usan 16×16 (ViT-B/16). la predicción densa (segmentación) utiliza 8×8 o 14×14 (SAM, DINOv2).

> **Patch 大小选择。**小模型使用 16×16(ViT-B/16)。密集预测(分割) utilizar 8×8 o 14×14(SAM、DINOv2)。 muy grande modelo utilizar 14×14。

## Envíe el producto .

¿ Qué ?`outputs/skill-vit-configurator.md`. La habilidad elige una variante de ViT y un tamaño de parche para una nueva tarea de visión dada el tamaño del conjunto de datos, la resolución y el presupuesto de cálculo.

> 参见 `outputs/skill-vit-configurator.md` Esta habilidad  Basado en el conjunto de datos de tamaño ̊ resolución y presupuesto de cálculo, para nuevas tareas de visión seleccionar ViT 变体和补丁 大小──

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Verifique el número de parches igual .`(H/P) * (W/P)`y la dimensión del parche plano es igual `P*P*C`¿ Qué ?
   Traducción:运行`code/main.py` Verificación de parches`(H/P) * (W/P)`, 平 parche 维度等于 `P*P*C`¿Qué es eso?
2. **Medium.**Implementar inserciones posicionales sinusoidales 2D  dos códigos sinusoidales independientes para `row`y `col`Los alimentamos en un pequeño PyTorch ViT y comparamos la precisión con las incorporaciones posicionales que se pueden aprender en CIFAR-10.
   En español: implementar 2D 正弦位置嵌入每个补丁的`row`Y `col`独立编码后拼接──在小型 PyTorch ViT 上使用,与可学习位置嵌入在CIFAR-10 上对比准确率──
3. **Hard.**Construir un ViT de 3 capas (PyTorch), entrenar en 1.000 imágenes MNIST con parches 4×4. Medir la precisión de la prueba. Ahora añadir DINOv2 pre-entrenamiento en las mismas 1.000 imágenes (simplificado: simplemente entrenar el codificador para predecir los embebidos de parches de parches enmascarados). ¿ Mejora la precisión?
   La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Patch | "The vision-transformer token" | Flat vector of pixel values for a `P × P × C` region of the image. |
| Patch | "视觉 Transformer 的 token" | 图像中 `P × P × C` 区域的像素值扁平向量。 |
| Patchify | "Chop + flatten" | Slice image into non-overlapping patches, flatten each to a vector. |
| Patchify | "切分 + 展平" | 将图像切成不重叠的 patch，每个展平为向量。 |
| `[CLS]` token | "The image summary" | Prepended learnable token; its final embedding is the image representation. |
| `[CLS]` token | "图像摘要" | 预置的可学习 token；其最终嵌入是图像表示。 |
| Inductive bias | "What the model assumes" | ViT has fewer priors than CNNs; needs more data to make up the gap. |
| 归纳偏好 | "模型假设了什么" | ViT 的先验比 CNN 少；需要更多数据来弥补差距。 |
| DINOv2 | "Self-supervised ViT" | Trained without labels using image augmentation + momentum teacher. Best general image features in 2026. |
| DINOv2 | "自监督 ViT" | 使用图像增强 + 动量教师无标签训练。2026 年最佳通用图像特征。 |
| SigLIP | "CLIP's successor" | ViT + text encoder trained with sigmoid contrastive loss; better than CLIP on matched compute. |
| SigLIP | "CLIP 的继承者" | 用 sigmoid 对比损失训练的 ViT + 文本编码器；相同计算量下优于 CLIP。 |
| Swin | "Windowed ViT" | Hierarchical ViT with local attention + shifted windows; sub-quadratic. |
| Swin | "窗口 ViT" | 带局部注意力 + 移位窗口的层级 ViT；亚二次复杂度。 |
| Register tokens | "2023 trick" | A few extra learnable tokens that soak up attention sinks; improves DINOv2 features. |
| Register tokens | "2023 技巧" | 几个额外的可学习 token，吸收注意力汇聚；改善 DINOv2 特征。 |

## Más Leer más Leer más

- [Dosovitskiy et al. (2020). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929) el papel de ViT.
  El texto original de la traducción de la lengua inglesa es ViT.
- [Touvron et al. (2021). Training data-efficient image transformers & distillation through attention](https://arxiv.org/abs/2012.12877) DeiT.
  En el texto original, el texto se traduce en inglés como "DeiT".
- [Liu et al. (2021). Swin Transformer: Hierarchical Vision Transformer using Shifted Windows](https://arxiv.org/abs/2103.14030)- ¡Swin!
  El cambio de la línea de trabajo de la empresa es el resultado de la investigación.
- [Oquab et al. (2023). DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193)¿Qué es esto?
  En el caso de los niños, el problema es que no hay nada que hacer.
- [Darcet et al. (2023). Vision Transformers Need Registers](https://arxiv.org/abs/2309.16588) la fijación de la ficha de registro para DINOv2.
  En el caso de los registros de DINOv2, el nombre de la empresa es DINOv2.
