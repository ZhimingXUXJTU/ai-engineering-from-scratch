# El transformador completo  Encoder + Decodificador
# 完整 Transformer  编码器 + 解码器

> La atención es la estrella. Todo lo demás  residuos, normalización, alimentación hacia adelante, atención cruzada  es el andamio que te permite apilarlo profundamente.

> La atención es la principal. Todo lo demás. La conexión, la integración, la red, la intersección.

> **【中文解读】**Colocar la autoatención, la atención múltiple, la FFN, los residuos, la norma de capa, y la transformación completa.

**Type:** Build | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention), Phase 7 · 04 (Positional Encoding) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力），阶段 7 · 04（位置编码）
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

Una capa de atención única es un extractor de características, no un modelo. Un matmul por capa no es suficiente capacidad para el lenguaje. Necesitas profundidad  y breaks de profundidad sin la tubería adecuada.

>                                                                                                                                                                                                                                                               

El documento Vaswani de 2017 empaquetó seis decisiones de diseño que convirtieron una capa de atención en un bloque apilable. Cada transformador desde  codificador-solo (BERT), decodificador-solo (GPT), codificador-decodificador (T5)  hereda el mismo esqueleto.

> En 2017 Vaswani 论文打包了六个设计决策,将一个注意层变成可堆叠的块──此后每个变压器纯编码器(BERT) 纯解码器(GPT) 编码器-解码器(T5) 都继承了相同的骨架──2026年, estos bloques han sido optimizados(RMSNorm、SwiGLU、前归化、RoPE), pero la estructura es completamente la misma──

Esta lección es el esqueleto. Las siguientes lecciones lo especializan  06 para codificadores, 07 para decodificadores, 08 para codificador-decodificador.

> Este curso es un esquema. El siguiente curso se especializa en él.

> **【中文解读】**单个注意层只是一个特征提取器, no es un modelo completo. En el artículo de 2017 se incluyen seis decisiones de diseño en bloques de composición: emplazamiento + codificación de posición, auto-atención, FFN, conexión de residuos, reclutamiento de niveles, interconexión de atención.

## El concepto central.

![Encoder and decoder block internals, wired](../assets/full-transformer.svg)

### Los seis piezas.

1. **Embedding + positional signal.**Tokens → vectores. Posición inyectada a través de RoPE (moderno) o sinusoidal (clásico).
   **嵌入 + 位置信号。**Token → 向量──通过 RoPE(现代) or正弦编码(经典)

2. **Self-attention.**Cada posición se atende a la otra.
   **自注意力。**Cada posición tiene todas las demás ubicaciones.

3. **Feed-forward network (FFN).**MLP de dos capas en función de la posición: `W_2 · activation(W_1 · x)`. Ratio de expansión 4x por defecto.
   **前馈网络 (FFN)。**位置级两层 MLP:`W_2 · activation(W_1 · x)`◊默认扩展比 4×──

4. **Residual connection.** `x + sublayer(x)`Sin esto, los gradientes desaparecen más allá de 6 capas.
   **残差连接。** `x + sublayer(x)`                                                                                                                                                                                                                                                              

5. **Layer normalization.** `LayerNorm`o `RMSNorm`Estabiliza el flujo residual.
   **层归一化。** `LayerNorm`O `RMSNorm`(现代) ∼稳定残差流─

6. **Cross-attention (decoder only).**Las consultas provienen del decodificador, claves y valores de la salida del codificador.
   **交叉注意力（仅解码器）。** Inquiries de descifrador, clave y valor de descifrador de salida

### Bloque de codificación (utilizado por BERT, T5 codificador)
Observe el flujo de un vector a través de un bloque: la atención se mezcla a través de posiciones, el residual lo lleva hacia adelante, el FFN lo transforma y la norma mantiene la corriente estable.

```figure
transformer-block
```

### Bloque de codificación (utilizado por el codificador BERT, T5)

```
x → LN → MHA(self) → + → LN → FFN → + → out
                     ^              ^
                     |              |
                     └── residual ──┘
```

El codificador es bidireccional, no se enmascara, todas las posiciones ven todas las posiciones.

> El codificador es doble. No hay ningún encubrimiento.

### Bloqueo de decodificación (utilizado por GPT, T5 decodificador)

```
x → LN → MHA(masked self) → + → LN → MHA(cross to encoder) → + → LN → FFN → + → out
```

El decodificador tiene tres subcapas por bloque. El medio  atención cruzada  es el único lugar donde la información fluye de un codificador a un decodificador. En una arquitectura pura de decodificador solo (GPT), la atención cruzada se omite y solo tienes la autoatención enmascarada + FFN.

> En la estructura del GPT, la atención de la intersección se omite, sólo se puede ocultar la atención de la misma + FFN。

### Pre-norma vs post-norma. Pre-reintegración vs. reintegración posterior.

Papel original: `x + sublayer(LN(x))`- ¿ Qué ?`LN(x + sublayer(x))`. Después de la norma perdió el favor alrededor de 2019  es más difícil entrenar profundamente sin un calentamiento cuidadoso.`LN`*antes de* subcapas) es el 2026 por defecto: Llama, Qwen, GPT-3+, Mistral todos lo usan.

> El tema original:`x + sublayer(LN(x))`- ¿ Qué ?`LN(x + sublayer(x))`◊ Después de la regeneración en 2019 aproximadamente  no hay un detalle de pre-calentamiento es muy difícil entrenar en profundidad ◊ Antes de la regeneración `LN`En la actualidad, el sistema de control de la energía solar es el más rápido posible para el mundo.

### El bloque 2026 modernizado 2026 el bloque modernizado

| Component / 组件 | 2017 | 2026 |
|-----------|------|------|
| Normalization / 归一化 | LayerNorm | RMSNorm |
| FFN activation / FFN 激活函数 | ReLU | SwiGLU |
| FFN expansion / FFN 扩展比 | 4× | 2.6×（SwiGLU 使用三个矩阵，总参数匹配） |
| Position / 位置编码 | Sinusoidal absolute / 绝对正弦 | RoPE |
| Attention / 注意力 | Full MHA | GQA (or MLA) |
| Bias terms / 偏置项 | Yes / 有 | No / 无 |

RMSNorm elimina la media de centrarse de LayerNorm (una subtracción menos), que ahorra en la computación y es empíricamente al menos tan estable.`Swish(W1 x) ⊙ W3 x`) supera constantemente a la FFN de ReLU/GELU en ~0,5 puntos en los documentos de Llama, PaLM y Qwen.

> RMSNorm eliminó la centralización de la media de LayerNorm (en la actualidad se reduce una vez más), ahorró la cantidad de cálculo, la experiencia al menos igual de estable.`Swish(W1 x) ⊙ W3 x`) en Llama、PaLM 和 Qwen 论文中一致地比 ReLU/GELU FFN 好约0.5 个困惑度点──

> **【中文解读】**2026 现代 Transformer 块与 2017 原版相比:LayerNorm→RMSNorm,ReLU→SwiGLU,后归一化→前归一化,绝对位置编码→RoPE,全多头注意力→GQA。 Cada mejoría es progresiva, pero la combinación mejoró significativamente la estabilidad del entrenamiento y la calidad del modelo。

> **【拓展：为什么 Decoder-only 成为主流】**Aunque la arquitectura de codificadores-des codificadores tiene ventajas naturales en tareas como la traducción, pero el modelo de solo Decoder (GPT、Llama) es más exitoso en expansión y generalidad. Puede utilizar la misma arquitectura para procesar la comprensión y generación de tareas, entrenar objetivos, y la expansión ha sido probada por Chinchilla 定律证── esto es la razón por la cual casi todos los modelos anteriores de 2024-2026 han sido seleccionados como Decoder-only.

### El número de parámetros.

Por un bloque con `d_model = d`y la expansión de FFN `r`¿Qué es esto ?

>  Para una `d_model = d`且 FFN 扩展比为 `r`El bloque:

- MHA: `4 · d²`(Proyecciones Q, K, V, O)
  El MHA:`4 · d²`(Q、K、V、O 投影)
- FFN (SwiGLU): `3 · d · (r · d)`¿ Qué es esto ?`3rd²`
  FFN(SwiGLU):`3 · d · (r · d)`¿ Qué es esto ?`3rd²`
- Normas: insignificantes
  归一化:可忽略

> **【拓展：参数计数与模型规模的实际意义】**Los parámetros de un transformador se centran principalmente en la proyección de atención ([[4d^2) y FFN]] (~8d^2 para SwiGLU) (中。Llama 3 8B Cada nivel es de aproximadamente 1.5B 参数,32 niveles 共约 7B加上嵌入层和输出头―― comprender la distribución de los parámetros ayuda a optimizar:MoE 替换FFN puede aumentar el total de los parámetros sin aumentar el cálculo activo; cuantitativo(como GPTQ、AWQ) principal compresión de FFN 权重──

## Construye y realiza.

### Paso 1: Los bloques de construcción Paso 1: Construir un módulo.

Usando el pequeño`Matrix`clase de la lección 03 (copiada en este archivo para su independencia):

> Uso de la sección 03 课中微型 `Matrix`类(ha sido copiado hasta este documento para mantenerse independiente):

- `layer_norm(x, eps=1e-5)` restar la media, dividir por std.
  `layer_norm(x, eps=1e-5)`  减去平均值,除以标准差──
- `rms_norm(x, eps=1e-6)` dividir por RMS. No hay subtracción media.
  `rms_norm(x, eps=1e-6)` Excepto en RMS──不减平均值──
- `gelu(x)`y `silu(x) * W3 x`- ¿Qué es eso?
  `gelu(x)`Y `silu(x) * W3 x`(SwiGLU)
- `ffn_swiglu(x, W1, W2, W3)`¿ Qué ?
- `encoder_block(x, params)`y `decoder_block(x, enc_out, params)`¿ Qué ?

### Paso 2: Conectar un codificador de 2 capas y un decodificador de 2 capas. Paso 2: conectar un codificador de 2 capas y un decodificador de 2 capas.

Colocalas en apilamiento, pasa la salida del codificador a cada decodificador, añade una LN final antes de la proyección de salida.

> 堆叠它们──将编码器输出传入每个解码器交叉注意力──在输出投影前添加最终 LN──

```python
def encode(tokens, params):
    x = embed(tokens, params.emb) + sinusoidal(len(tokens), params.d)
    for block in params.encoder_blocks:
        x = encoder_block(x, block)
    return x

def decode(target_tokens, encoder_out, params):
    x = embed(target_tokens, params.emb) + sinusoidal(len(target_tokens), params.d)
    for block in params.decoder_blocks:
        x = decoder_block(x, encoder_out, block)
    return x
```

### Paso 3: Avanza en un ejemplo de juguete. Paso 3: En un ejemplo de juguete, se ejecuta hacia adelante y se transmite.

A través de una fuente de 6 tokens y un objetivo de 5 tokens.`(5, vocab)`No hay entrenamiento. Esta lección es sobre la arquitectura, no la pérdida.

> 输入 6 个代币的源和 5 个代币的目标──验证输出形状是 `(5, vocab)` No entrenar  No preocuparse por la estructura, no preocuparse por la pérdida.

### Paso 4: Cambiar en RMSNorm + SwiGLU 步骤 4: sustituir por RMSNorm + SwiGLU

Replace LayerNorm y ReLU-FFN con RMSNorm y SwiGLU. Confirme que las formas siguen coincidiendo. Esta es la modernización 2026 con una sustitución de función.

> Utiliza RMSNorm 和 SwiGLU  sustituir LayerNorm 和 ReLU-FFN── confirmación de forma todavía coincide── es a través de una vez de la función sustitución de la realización de 2026 años de modernización──

## Usalo con el marco de ejecución

Las implementaciones de referencia PyTorch/TF: `nn.TransformerEncoderLayer`¿ Qué ?`nn.TransformerDecoderLayer`Pero la mayoría del código de producción 2026 tiene su propio bloque porque:

> PyTorch/TF 参考实现:`nn.TransformerEncoderLayer`¿Qué es esto?`nn.TransformerDecoderLayer`Pero la mayoría de los códigos de producción de 2026 años se construyen por sí mismos, ya que:

- La atención flash se llama dentro de la atención, no a través de `nn.MultiheadAttention`¿ Qué ?
  Flash Atención en la atención interna, no pasa `nn.MultiheadAttention`¿Qué es eso?
- GQA / MLA no están en la referencia de la STDlib.
  GQA / MLA 不在标准库参考中──
- RoPE, RMSNorm, SwiGLU no son los valores predeterminados de PyTorch.
  RoPE、RMSNorm、SwiGLU no es el valor predeterminado de PyTorch.

**Encoder vs decoder vs encoder-decoder — when to pick:**

> **编码器 vs 解码器 vs 编码器-解码器——何时选择：**

| Need / 需求 | Pick / 选择 | Example / 示例 |
|------|------|---------|
| Classification, embeddings, QA over text / 分类、嵌入、文本 QA | Encoder-only / 纯编码器 | BERT, DeBERTa, ModernBERT |
| Text generation, chat, code, reasoning / 文本生成、聊天、代码、推理 | Decoder-only / 纯解码器 | GPT, Llama, Claude, Qwen |
| Structured input → structured output (translation, summarization) / 结构化转换 | Encoder-decoder / 编码器-解码器 | T5, BART, Whisper |

> **【中文解读】**Tres tipos de arquitectura:Encoder-sólo(BERT) adaptado a la clase y la inserción;Decoder-sólo(GPT/Llama) adaptado a la generación y tareas generales;Encoder-Decoder(T5/BART) adaptado a una clara "solución de origen" de tareas de transformación estructural.

> **【拓展：SwiGLU 为何优于 ReLU】**SwiGLU(Unidad Lineal de Puertas Suecas) a través de un mecanismo de control de puertas hace que la capacidad de expresión de FFN sea más fuerte. Las experiencias de modelos similares de SwiGLU muestran que SwiGLU es aproximadamente 0.5 puntos bajo en comparación con ReLU/GELU en la confusión de construcción de lenguaje. Aunque requiere tres matrices de peso y no dos, la cantidad de parámetros aumenta un 50%), pero generalmente se ampliará de 4x a 2.6x para compensar.

## Envíe el producto .

¿ Qué ?`outputs/skill-transformer-block-reviewer.md`. La habilidad revisa la implementación de un nuevo bloque de transformador en función de los valores predeterminados de 2026 y señala las piezas faltantes (pre-norma, RoPE, RMSNorm, GQA, FFN ratio de expansión).

> 参见 `outputs/skill-transformer-block-reviewer.md` Esta habilidad según el establecimiento de 2026 revisar nuevos bloques de transformadores para realizar, y marcar la falta de parte 

## Los ejercicios.

1. **Easy / 简单。**Cuenta los parámetros en tu bloque de codificación en `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`. Valida mediante la implementación del bloque y el uso de `sum(p.numel() for p in block.parameters())`¿ Qué ?
   计算 `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`时 encoder_block 的参数──通过实现块并使用 `sum(p.numel() for p in block.parameters())`验证。

2. **Medium / 中等。**Cambiar de post-norma a pre-norma. Iniciar ambos y medir la norma de activación después de 12 capas apiladas en entrada aleatoria.
   Desde el posterior regeneración de cambios hasta el anterior regeneración. Los dos iniciaciones y mediciones de 12 niveles de acumulación de activas en las entradas de paso.

3. **Hard / 困难。**Implementar un codificador-decodificador de 4 capas en una tarea de copia de juguete (copiar `x`El tren 100 pasos. informe pérdida. ¿El cambio en RMSNorm + SwiGLU + RoPE  ¿La pérdida disminuye?
   En la tarea de reproducción de juguetes`x`¿Ha disminuido el número de pérdidas en el RMSNorm + SwiGLU + RoPE?

## Términos clave .

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Block / 块 | "One transformer layer" / "一个 Transformer 层" | Stack of norm + attention + norm + FFN, wrapped in residual connections. 归一化 + 注意力 + 归一化 + FFN 的堆叠，包裹在残差连接中。 |
| Residual / 残差连接 | "Skip connection" / "跳跃连接" | `x + f(x)` output; enables gradient flow through deep stacks. `x + f(x)` 输出；使梯度流能穿过深层堆叠。 |
| Pre-norm / 前归一化 | "Normalize before, not after" / "先归一化，不是后归一化" | Modern: `x + sublayer(LN(x))`. Trains deeper without warmup gymnastics. 现代：`x + sublayer(LN(x))`。无需预热技巧即可训练更深的网络。 |
| RMSNorm | "LayerNorm without the mean" / "没有均值的 LayerNorm" | Divide by RMS; one less op, same empirical stability. 除以 RMS；少一次操作，经验上同样稳定。 |
| SwiGLU | "The FFN everyone switched to" / "大家都换成的 FFN" | `Swish(W1 x) ⊙ W3 x → W2`. Beats ReLU/GELU on LM ppl. 在 LM 困惑度上击败 ReLU/GELU。 |
| Cross-attention / 交叉注意力 | "How the decoder sees the encoder" / "解码器如何看到编码器" | MHA with Q from decoder, K/V from encoder outputs. MHA 的 Q 来自解码器，K/V 来自编码器输出。 |
| FFN expansion / FFN 扩展比 | "How wide the middle MLP is" / "中间 MLP 有多宽" | Ratio of hidden-size to d_model, usually 4 or 2.6 (SwiGLU). 隐藏大小与 d_model 的比率，通常为 4 或 2.6（SwiGLU）。 |
| Bias-free / 无偏置 | "Drop the +b terms" / "去掉 +b 项" | Modern stacks omit biases in linear layers; slight ppl improvement, smaller model. 现代堆栈在线性层中省略偏置；轻微的困惑度改善，更小的模型。 |

## Más Leer más Leer más

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762) especificación original del bloque.
  Vaswani 等人(2017)  原始块规范。

- [Xiong et al. (2020). On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745)¿Por qué la pre-norma supera profundamente la post-norma?
  Xiong 等人(2020)  ¿Por qué el pre-reunificación en el nivel profundo después de la victoria en el nivel profundo?

- [Zhang, Sennrich (2019). Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467) RMSNorm.

- [Shazeer (2020). GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202) el papel SwiGLU.
  Shazeer(2020)  SwiGLU 论文。

- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) bloque canónico 2026 solo para decodificadores.
  Abrazando el rostro`modeling_llama.py` 2026                                                                                                                                                                                                                                                             
