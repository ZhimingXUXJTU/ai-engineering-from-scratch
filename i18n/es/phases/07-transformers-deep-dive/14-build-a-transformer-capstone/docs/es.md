# Construir un transformador desde cero  La piedra angular  Desde cero construir transformador  毕业项目

> Trece lecciones, un modelo, sin atajos.

> **【中文解读】**整合所有知识, desde zero implementar la arquitectura completa de GPT.

**Type:** Hands-on | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 7 · 01 through 13. Don't skip. | **前置知识:** Phase 7 · 01 through 13. Don't skip.
**Time:** ~120 minutes | **时间:** ~120 分钟

## El problema es la introducción del problema

Has leído todos los artículos, has implementado atención, divisiones de múltiples cabezas, codificación posicional, bloqueos de codificación y decodificación, pérdidas de BERT y GPT, MoE, KV caché. Ahora haz que trabajen juntos en una tarea real.

> Ya has leído cada artículo. Ya has logrado la atención, la división, la codificación de posiciones, el codificador y el codificador de bloques, BERT y GPT                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

La piedra angular: entrenar a un pequeño transformador de un solo decodificador de extremo a extremo en una tarea de modelado de lenguaje a nivel de personajes. Lee Shakespeare. Genera un nuevo Shakespeare. Es lo suficientemente pequeño como para entrenar en una computadora portátil en menos de 10 minutos. Es lo suficientemente correcto que intercambiar un conjunto de datos más grande y un entrenamiento más largo te da un LM real.

> 毕业项目: 在字符级语言建模任务上端到端训练一个小型解码器专用变压器──它读取莎士比亚,生成新的莎士比亚──它足够小,可以在笔记本上完成10分钟的训练──它足够正确,转换成更大的数据集和更长的训练时间就能得到真正的语言模型──

Este es el "nanoGPT" del curso. No es original  El tutorial de Karpathy de 2023 nanoGPT es la implementación de referencia que cada estudiante escribe al menos una vez. Levantamos la forma y la retolamos alrededor de lo que hemos cubierto.

> Este es el "nanoGPT" del curso. No es el original. El programa de nanoGPT de Karpathi 2023 es un proyecto de referencia que cada estudiante escriba al menos una vez.

> **【中文解读】**Este programa de estudios se desarrollará en las primeras 13 secciones de la clase para integrar todos los conocimientos: código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de

> **【拓展：从 nanoGPT 到生产级 LLM】**El nanoGPT de Karpathy es el mejor punto de partida para aprender Transformer. La diferencia clave de nanoGPT a nivel de producción del LLM es: tamaño de datos, desde MB hasta TB. La infraestructura de entrenamiento, desde una sola GPU hasta miles de GPU, es el mismo.

## El concepto central.

![Transformer-from-scratch block diagram](../assets/capstone.svg)

La arquitectura, anotado:

> 架构,带注释:

```
input tokens (B, N)
   │
   ▼
token embedding + positional embedding  ◀── Lesson 04 (RoPE option)
   │
   ▼
┌──── block × L ────────────────────┐
│  RMSNorm                          │  ◀── Lesson 05
│  MultiHeadAttention (causal)      │  ◀── Lesson 03 + 07 (causal mask)
│  residual                         │
│  RMSNorm                          │
│  SwiGLU FFN                       │  ◀── Lesson 05
│  residual                         │
└────────────────────────────────── ┘
   │
   ▼
final RMSNorm
   │
   ▼
lm_head (tied to token embedding)
   │
   ▼
logits (B, N, V)
   │
   ▼
shift-by-one cross-entropy            ◀── Lesson 07
```

### Lo que enviamos

> El contenido de nuestro servicio:

- `GPTConfig` un lugar para configurar todos los hiperparámetros.
  En inglés:`GPTConfig` Un lugar donde se encuentran todos los superparámetros.
- `MultiHeadAttention` Causal, en lote, con vía opcional de estilo Flash (PyTorch's `scaled_dot_product_attention`¿Qué es lo que se hace?
  En inglés:`MultiHeadAttention` 因果的、批量,可选闪光 风格路径(PyTorch de `scaled_dot_product_attention`)。
- `SwiGLUFFN` FFN moderno.
  En inglés:`SwiGLUFFN` 现代 FFN。
- `Block` Pre-norma, atención envuelta residual + FFN.
  En inglés:`Block` Pre-regulación, residuo de paquete de atención + FFN。
- `GPT` embebidos, bloques apilados, cabeza LM, generar().
  En inglés:`GPT` 嵌入、堆叠块、LM 头、generar()
- Bucle de entrenamiento con AdamW, cosino LR, recorte de gradiente.
  La formación de los estudiantes en el campo de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación.
- Tokenizer de nivel Char en el texto de Shakespeare.
  En inglés, el nombre de Shakespeare es "Shakespeare".

> **【中文解读】** completa GPT 实现包含:配置类、多头因果注意力(可选 Flash Attention)、SwiGLU FFN、前归归一化残差块、 completa GPT 模型类(嵌入 + 堆叠块 + LM 头 + 生成函数)、AdamW + 余弦学习率训练循环──为了简洁,使用学习式位置嵌入(而不是 RoPE) 并实现KV 缓存,但练习要求你添加这些──

### Lo que no enviamos

> Nosotros no entregamos contenido:

- RoPE  implementado conceptualmente en la Lección 04. Aquí usamos embeddings posicionales aprendidos para la simplicidad.
  En la cuarta clase hay un concepto de realización. Aquí para hacer una práctica de aprendizaje.
- El caché KV durante la generación  cada paso de generación recalcula la atención sobre el prefijo completo.
  Traducción:Casa de producción  Cada paso de generación hacia el completo anterior vuelve a calcular la atención.
- Atención Flash  PyTorch 2.0+ automáticos de envío si las entradas coinciden; usamos `F.scaled_dot_product_attention`¿ Qué ?
  En inglés, el nombre de la plataforma de la plataforma de la plataforma de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet`F.scaled_dot_product_attention`¿Qué es eso?
- MoE  FFN por bloque.
  En el primer capítulo, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de los jóvenes, el libro de la vida de la familia, el libro de la historia de la familia de los jóvenes, el libro de la historia de la historia de la historia de los jóvenes, el libro de la historia de la historia de la historia de la historia de los jóvenes, el libro de la historia de la historia de la historia de la historia de los jóvenes, el libro de la historia de la historia de la historia de la historia de la historia de los jóvenes, el libro de la historia de la historia de la historia de la historia de los jóvenes, la historia de la historia de la historia de la historia de la historia de la historia de los que se trata sobre.

### Metricas de objetivo

En una computadora portátil Mac M2, un 4 capas, 4 cabezas, d_model=128 GPT entrenado para 2.000 pasos en `tinyshakespeare.txt`¿Qué es esto ?

> En Mac M2 笔记本上,4 层、4 头、d_model=128 de GPT en `tinyshakespeare.txt`上训练 2.000 pasos:

- La pérdida de entrenamiento converge de ~ 4,2 (a azar) a ~ 1,5 en aproximadamente 6 minutos.
  Traducción:El entrenamiento perdido de aproximadamente 4.2 (随机) en aproximadamente 6 minutos en aproximadamente 1.5 (en inglés).
- La muestra de producción parece en forma de Shakespeare: aparecen palabras arcaicas, interrupciones de líneas, nombres propios como "ROMEO:" .
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la
- La pérdida de valor (el 10% final del texto retenido) sigue de cerca la pérdida de formación; no se sobreajusta a este tamaño/orden de presupuesto.
  Traducción:El último 10% del texto de la prueba de pérdida de tiempo (Leave Out the Last 10% of the Text)

> **【拓展：从字符级到子词级 Tokenizer】**Este proyecto utiliza un tokenizador de tipo letra (BPE) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en) (en inglés) (en inglés).

## Construye y realiza.
```figure
n5-block-stack
```

## Construye el mismo

Esta lección utiliza PyTorch.`torch`(Construcción de CPU está bien).`code/main.py`El guión se ocupa de:

> 本课使用 PyTorch──安装 `torch`(CPU 版本即可)`code/main.py`❖ El guión de tratamiento:

- Descargar`tinyshakespeare.txt`si falta (o si se lee una copia local).
  Si falta es por aquí`tinyshakespeare.txt`(或读取本地副本)
- Tokenizaje de car de nivel byte.
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de trabajo es el de la persona que se encuentra en el lugar de trabajo.
- Tren / val dividido en 90/10.
  El trabajo de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de
- Bucle de entrenamiento con bf16 autocast en el hardware soportado.
  Traducción:Bf16 en el hardware de apoyo
- Se concluye la toma de muestras después del entrenamiento.
  En español, "la formación después de la finalización"

### Paso 1: datos

```python
text = open("tinyshakespeare.txt").read()
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
encode = lambda s: [stoi[c] for c in s]
decode = lambda xs: "".join(itos[x] for x in xs)
```

65 caracteres únicos, un pequeño vocabulario, un tamaño de 4 bytes, sin BPE, sin drama de tokenizer.

> 65 个唯一字符──微型词表──适配 4 字节 vocab_size──没有 BPE,没有分词器的麻烦──

### Paso 2: modelo

¿ Qué ?`code/main.py`El bloque es un libro de texto de la lección 05  pre-norma, RMSNorm, SwiGLU, MHA causal.

> 参见 `code/main.py`◊ Este bloque es el texto de la clase 05                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

### Paso 3: ciclo de entrenamiento

Obtenga un lote aleatorio de ventanas de 256 tokens de longitud hacia adelante, cambio por entropias cruzadas hacia atrás, paso AdamW, registro, repite.

> 获取随机批量长度为 256 的标记窗口──前向传播──偏移一位的交叉──反向传播──AdamW 步进──记录──重复──

```python
for step in range(max_steps):
    x, y = get_batch("train")
    logits = model(x)
    loss = F.cross_entropy(logits.view(-1, vocab_size), y.view(-1))
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    opt.zero_grad()
```

### Paso 4: muestra

Si se le da una solicitud, repetidamente, muestra de los logits de arriba, añade y continúa.

> 给定一个提示,反复前向传播, de los logitos de arriba p 采样,追加,继续──500 个标志 后停止──

### Paso 5: lee la salida

Después de 2.000 pasos:

> 2.000 pasos después:

```
ROMEO:
Away and mild will not thy friend, that thou shalt wit:
The chief that well shame and hath been his friends,
...
```

No Shakespeare, pero en forma de Shakespeare, una clara victoria por unos 800K parámetros y 6 minutos en una computadora portátil.

> No es Shakespeare, pero como Shakespeare, unos 800.000 puntos en el cuaderno de 6 minutos de victoria.

## Usalo con el marco de ejecución

Esta piedra es una arquitectura de referencia.

> Este proyecto de formación es una estructura de referencia. Tres expansiones pueden convertirlo en un sistema realmente útil:

1. **Swap the tokenizer.**Utilice BPE (por ejemplo `tiktoken.get_encoding("cl100k_base")`El tamaño de la vocab aumentó de 65 a 50.000.
   En inglés:**替换分词器。**Uso de BPE`tiktoken.get_encoding("cl100k_base")`)──词表大小 de 65 跳到约50,000──模型容量需要相应扩展──
2. **Train on a bigger corpus.**Usar`OpenWebText`o `fineweb-edu`Los tokens 10B en un solo A100 tardan alrededor de 24 horas en un GPT de 125M-param.
   En inglés:**在更大的语料上训练。**Uso `OpenWebText`O `fineweb-edu`(HuggingFace) ―― en单张 A100 上用10B token 训练 125M 参数 GPT 约需24小时──
3. **Add RoPE + KV cache + Flash Attention.**Los ejercicios que se presentan a continuación te guiarán a través de cada uno.
   En inglés:**添加 RoPE + KV 缓存 + Flash Attention。**Los siguientes ejercicios te guiarán a completar cada paso.

Esto termina como un GPT de parámetro de 125M que genera inglés fluido. No es un modelo fronterizo. Pero el mismo camino de código  sólo más grande  es lo que Karpathy, EleutherAI y el Instituto Allen utilizan para entrenar los puestos de control de investigación en 2026.

> Finalmente obtuve un que pueda generar un fluido Inglés de 125M parámetro GPT── no es un modelo de vanguardia── pero el mismo código de ruta es simplemente más grande es el Karpathy、EleutherAI 和 Allen Institute en 2026 entrenamiento y investigación de los puntos de inspección utilizados─.

> **【拓展：Karpathy 的 nanoGPT 与教育意义】**El nanoGPT de Andrej Karpathy ((2023) es uno de los más influyentes cursos en la historia de la educación de IA. Prueba un GPT completo y entrenable que se puede implementar con aproximadamente 300 piezas PyTorch. Este método de enseñanza "desde cero construido" te permite comprender realmente el papel de cada componente, en lugar de transformarlo en una caja negra.

## Envíe el producto .

¿ Qué ?`outputs/skill-transformer-review.md`La habilidad revisa una implementación de transformador desde cero para verificar la corrección en las 13 lecciones anteriores.

> 参见 `outputs/skill-transformer-review.md`◊ Esta habilidad  revisar una transformación de la construcción desde cero , comprobar la veracidad de todos los 13 

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Verifique si la pérdida de validación en la etapa final de su modelo entrenado es inferior a 2.0.`max_steps`¿La pérdida de val sigue mejorando?
   Traducción:运行`code/main.py` Verificar que la pérdida final del modelo de entrenamiento es inferior a 2.0 `max_steps`¿Se ha mejorado la pérdida de la certificación de 2000 a 5000?
2. **Medium.**Reemplazar las incorporaciones posicionales aprendidas con RoPE. Aplique la rotación a Q y K dentro `MultiHeadAttention`La pérdida de val es al menos tan baja.
   En inglés, el idioma de la lengua inglesa es el idioma de la lengua inglesa.`MultiHeadAttention`En el caso de los sistemas de control de la velocidad, el valor de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de velocidad de la velocidad de la velocidad de la velocidad de la velocidad de velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de velocidad de la velocidad de la veloc
3. **Medium.**Implemente una caché KV en el bucle de muestreo. Generar 500 tokens con y sin caché. El reloj de pared debería mejorar en 520x en una computadora portátil.
   En el ciclo de la toma de datos, se realiza un KV 缓存──有缓存和无缓存, generando 500 tokens── en el libro de notas debería haber un mejoramiento real de 5-20 veces.
4. **Hard.**Añadir una segunda cabeza al modelo que predice el siguiente token más uno (MTP  Multi-Token Prediction de DeepSeek-V3).
   China: Add Add a second头预测下下一个代币MTP proviene de varios de los tokens de DeepSeek-V3 预测)
5. **Hard.**Reemplazar el FFN único por bloque con un MoE de 4 expertos. Router + top-2 enrutamiento. Ver cómo cambia la pérdida de val en parámetros activos coincidentes.
   China 翻译:将每块的单个FFN 替换为4 专家 MoE──路由器 + top-2 路由──观察在匹配活跃参数下验证损失的变化──

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| nanoGPT | "Karpathy's tutorial repo" | Minimal decoder-only transformer training code, ~300 LOC; the canonical reference. |
| nanoGPT | "Karpathy 的教程仓库" | 最小解码器专用 Transformer 训练代码，约 300 行；经典参考。 |
| tinyshakespeare | "The standard toy corpus" | ~1.1 MB of text; every character-LM tutorial since 2015 uses it. |
| tinyshakespeare | "标准玩具语料库" | 约 1.1 MB 文本；自 2015 年以来每个字符级语言模型教程都用它。 |
| Tied embeddings | "Share input/output matrix" | LM head weight = transpose of token embedding matrix; saves parameters, improves quality. |
| 绑定嵌入 | "共享输入/输出矩阵" | LM 头权重 = token 嵌入矩阵的转置；节省参数，提高质量。 |
| bf16 autocast | "Training precision trick" | Run forward/back in bf16, keep optimizer state in fp32; standard since 2021. |
| bf16 自动混合精度 | "训练精度技巧" | 前向/反向用 bf16，优化器状态用 fp32；2021 年以来的标准。 |
| Gradient clipping | "Stops spikes" | Cap global grad norm at 1.0; prevents training blowups. |
| 梯度裁剪 | "阻止尖峰" | 将全局梯度范数限制在 1.0；防止训练爆炸。 |
| Cosine LR schedule | "The 2020+ default" | LR ramps up linearly (warmup) then decays cosine-shaped to 10% of peak. |
| 余弦学习率调度 | "2020+ 默认" | 学习率线性升温（warmup）然后余弦衰减到峰值的 10%。 |
| MFU | "Model FLOP Utilization" | Achieved FLOPs / theoretical peak; 40% dense, 30% MoE is strong in 2026. |
| MFU | "模型 FLOP 利用率" | 实际 FLOPs / 理论峰值；2026 年稠密 40%、MoE 30% 是好的。 |
| Val loss | "Held-out loss" | Cross-entropy on data the model never saw; overfit detector. |
| 验证损失 | "留出损失" | 模型从未见过的数据上的交叉熵；过拟合检测器。 |

## Más Leer más Leer más

- [The Annotated Transformer (Harvard NLP)](https://nlp.seas.harvard.edu/annotated-transformer/) la aplicación clásica de notas.
  Traducción:Havard NLP's注解版 Transformer, clásico referencia realización。
