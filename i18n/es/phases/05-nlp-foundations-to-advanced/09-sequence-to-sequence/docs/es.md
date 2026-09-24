# Secuencia a secuencia de modelos.

> Dos RNNs que pretenden ser traductores, el cuello de botella que se encuentran es la razón por la que existe la atención.
> Dos RNN 假装是翻译器──它们 se encuentran en botellas正是注意力机械的存在原因──

> **【中文解读】**编码器解码器架构──注意力机制就是为了解决它的瓶而发明的──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 08 (CNNs + RNNs for Text), Phase 3 · 11 (PyTorch Intro) | **前置知识:** Phase 5 · 08（CNN 和 RNN 文本处理），Phase 3 · 11（PyTorch 入门）
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

La clasificación mapea una secuencia de longitud variable a una sola etiqueta. La traducción mapea una secuencia de longitud variable a otra secuencia de longitud variable. La entrada y salida viven en diferentes vocabularios, posiblemente en diferentes idiomas, sin garantía de paridad de longitud.

> La clasificación de los cambios en la secuencia se asigna a un solo etiquetado. La clasificación de los cambios en la secuencia se asigna a otro cambio en la secuencia.

La arquitectura seq2seq (Sutskever, Vinyals, Le, 2014) rompió esto con una receta deliberadamente simple. Dos RNNs. Uno lee la oración fuente y produce un vector de contexto de tamaño fijo. El otro lee ese vector y genera el token de la oración objetivo por token.

> Seq2seq 架构(Sutskever, Vinyals, Le, 2014) resolvió este problema con un esquema de diseño simple. Dos RNN.

Esto vale la pena estudiar por dos razones. Primero, el cuello de botella del vector contextual es el fracaso pedagógicamente más útil en la PNL. Motiva todo lo que la atención y los transformadores son buenos en. Segundo, la receta de entrenamiento (el profesor forzado, muestreo programado, búsqueda de haces a la inferencia) todavía se aplica a todos los sistemas modernos de generación, incluidos los LLM.

> Esto vale la pena aprender por dos razones. Primero, el fracaso de la más importante enseñanza de valor en la PNL.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

**Encoder.**Un RNN que lee la frase fuente.**context vector** un resumen de tamaño fijo de toda la entrada.

> **编码器（Encoder）。**Un texto de la RNN. Su estado oculto final es:**上下文向量**                                                                                                                                                                                                                                                              

**Decoder.**Otro RNN iniciado desde el vector de contexto. En cada paso toma el token generado previamente como entrada y produce una distribución sobre el vocabulario objetivo. muestra o argmax para elegir el siguiente token.`<EOS>`se produce el token o se alcanza la longitud máxima.

> **解码器（Decoder）。**另一从上下文向量初始化的 RNN──在每一步,它将先生成的代币作为输入,产生目标词表上的分布──采样或取 argmax 选择下一个代币──将其反进去──重复直到产生`<EOS>`El símbolo o alcanzar la máxima longitud.

**Training:**Perdida de entropía cruzada en cada paso del decodificador, sumada a través de la secuencia.

> **训练：**Cada paso de la red de descifradores se pierde, se busca y se pierde en la secuencia.

**Teacher forcing.**Durante el entrenamiento, la entrada del decodificador en paso `t`es el símbolo de la verdad de la base en posición`t-1`En el caso de los modelos de los sistemas de cálculo, el método de cálculo de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los cuentas de los valores de los cuentas**exposure bias**¿ Qué ?

> **教师强制（Teacher Forcing）。**                                                                                                                                                                                                                                                              `t`La entrada es la posición.`t-1`El modelo siempre aprenderá a hacerse a la perfección. Cuando se hace una teoría, se debe usar la propia predicción del modelo, por lo que siempre existe una diferencia de distribución de la teoría.**暴露偏差（Exposure Bias）**¿Qué es eso?

**The bottleneck.**Todo lo que el codificador aprendió sobre la fuente debe ser comprimido en ese vector de contexto. Las oraciones largas pierden detalles. Las palabras raras se borran.

> **瓶颈。**Todo lo que el codificador ha aprendido sobre la fuente debe comprimirse a la que se encuentra en el siguiente volumen.

La atención (lección 10) corrige esto dejando que el decodificador vea * cada * estado oculto del codificador, no sólo el último.

> Atención(第 10 课) 通过让解码器查看* cada*编码器隐藏状态(不仅仅是最后一个) 来修复这个问题――这是全部的关键点――

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.
```figure
lstm-gates
```

## Construye el mismo

### Paso 1: un codificador

```python
import torch
import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, src_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(src_vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)

    def forward(self, src):
        e = self.embed(src)
        outputs, hidden = self.gru(e)
        return outputs, hidden
```

`outputs`tiene forma`[batch, seq_len, hidden_dim]` un estado oculto por posición de entrada. `hidden`tiene forma`[1, batch, hidden_dim]` el paso final. La lección 08 dijo "reunir las salidas para la clasificación". Aquí mantenemos el último estado oculto como el vector de contexto, e ignoramos las salidas por paso.

> `outputs`形状为            `[batch, seq_len, hidden_dim]` Cada entrada de posición es un estado oculto `hidden`形状为            `[1, batch, hidden_dim]` Ultimo paso.  Se dice "En los resultados 上池化做分类"── Aquí conservamos el último estado oculto como en la siguiente secuencia, ignorando el paso a paso de salida.

### Paso 2: un decodificador

```python
class Decoder(nn.Module):
    def __init__(self, tgt_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(tgt_vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, tgt_vocab_size)

    def forward(self, token, hidden):
        e = self.embed(token)
        out, hidden = self.gru(e, hidden)
        logits = self.fc(out)
        return logits, hidden
```

El decodificador se llama un paso a la vez. Entrada: un lote de tokens individuales y el estado oculto actual. salida: logs vocabulario para el siguiente token y el estado oculto actualizado.

> 解码器每次调用一步──输入: una serie de tokens y el estado oculto actual──输出: next tokens of word表 logits 和更新后的隐藏状态──

### Paso 3: ciclo de formación con el profesor forzador

```python
def train_batch(encoder, decoder, src, tgt, bos_id, optimizer, teacher_forcing_ratio=0.9):
    optimizer.zero_grad()
    _, hidden = encoder(src)
    batch_size, tgt_len = tgt.shape
    input_token = torch.full((batch_size, 1), bos_id, dtype=torch.long)
    loss = 0.0
    loss_fn = nn.CrossEntropyLoss(ignore_index=0)

    for t in range(tgt_len):
        logits, hidden = decoder(input_token, hidden)
        step_loss = loss_fn(logits.squeeze(1), tgt[:, t])
        loss += step_loss
        use_teacher = torch.rand(1).item() < teacher_forcing_ratio
        if use_teacher:
            input_token = tgt[:, t].unsqueeze(1)
        else:
            input_token = logits.argmax(dim=-1)

    loss.backward()
    optimizer.step()
    return loss.item() / tgt_len
```

Dos botones que vale la pena nombrar.`ignore_index=0`Salta pérdida en tokens de relleno. `teacher_forcing_ratio`Es la probabilidad de usar el token verdadero frente a la predicción del modelo en cada paso. Comience en 1.0 (forzar al maestro completo) y aneal hacia abajo a ~0.5 durante el entrenamiento para cerrar la brecha de vicio de exposición.

>  Dos elementos que merecen atención:`ignore_index=0`跳过填充代币 上的损失──`teacher_forcing_ratio`Es probable que cada paso de uso de tokens reales y de modelos previos (de 1.0 a la obligación del profesor completo) comience, el proceso de entrenamiento regresa a aproximadamente 0.5 a la reducción de la diferencia de exposición.

### Paso 4: bucle de inferencia (compulsivo)

```python
@torch.no_grad()
def greedy_decode(encoder, decoder, src, bos_id, eos_id, max_len=50):
    _, hidden = encoder(src)
    batch_size = src.shape[0]
    input_token = torch.full((batch_size, 1), bos_id, dtype=torch.long)
    output_ids = []
    for _ in range(max_len):
        logits, hidden = decoder(input_token, hidden)
        next_token = logits.argmax(dim=-1)
        output_ids.append(next_token)
        input_token = next_token
        if (next_token == eos_id).all():
            break
    return torch.cat(output_ids, dim=1)
```

La codificación codificada elige el token de mayor probabilidad en cada paso. Puede alejarse: una vez que se compromete a un token, no se puede desactivar. **Beam search**Mantendrá el primer...`k`Sequencias parciales vivas y elige el más alto puntaje completo al final.

> 贪心解码每步选择最高概率的代币――它可能走偏: una vez que usted ha enviado un token, no se puede retirar――**束搜索（Beam Search）**保持排名前                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `k`La secuencia de partes sobrevive, en la última selección de la secuencia completa de la mayor parte. La amplitud de los grupos de 3-5 es el estándar.

### Paso 5: el cuello de botella, demostrado

Entrenamiento del modelo en una tarea de copia de juguete: fuente `[a, b, c, d, e]`, objetivo`[a, b, c, d, e]`Aumentar la longitud de la secuencia.

> En el juego de la copia de tareas entrenamiento modelo: fuente `[a, b, c, d, e]`, objetivo `[a, b, c, d, e]`                                                                                                                                                                                                                                                              

```
seq_len=5   copy accuracy: 98%
seq_len=10  copy accuracy: 91%
seq_len=20  copy accuracy: 62%
seq_len=40  copy accuracy: 23%
```

Un solo estado oculto de GRU no puede memorizar sin pérdidas una entrada de 40 tokens. La información está allí en cada paso del codificador, pero el decodificador solo ve el último estado.

> 单个GRU 隐藏状态无法无损记忆 40 代币的输入――信息存在于每一个编码器步骤,但解码器只看到最后状态――注意力直接修复了这个问题――

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

PyTorch tiene `nn.Transformer`y `nn.LSTM`- basado en plantillas de seguimiento.`transformers`La biblioteca de los barcos de modelos de codificación y decodificación completos (BART, T5, mBART, NLLB) entrenados en miles de millones de tokens.

> Hay torcha .`nn.Transformer`Y basado en`nn.LSTM`模板──Cabos de la cara `transformers`库提供在数十亿代币上训练的完整编码器-解码器模型(BART、T5、mBART、NLLB) 

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tok = AutoTokenizer.from_pretrained("facebook/bart-base")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

src = tok("Translate this to French: Hello, how are you?", return_tensors="pt")
out = model.generate(**src, max_new_tokens=50, num_beams=4)
print(tok.decode(out[0], skip_special_tokens=True))
```

Los codificadores modernos descodificadores dejaron caer RNN para transformadores. La forma de alto nivel (encodificador, decodificador, generar-token-por-token) es idéntica al papel de 2014 seq2seq. El mecanismo dentro de cada bloque es diferente.

> 现代编码器-解码器用变压器 替换了RNN──高层结构(编码器、解码器、个代币 生成) con el artículo de 2014 seq2seq 完全相同── cada bloque interno es diferente en el mecanismo.

### Cuando todavía se puede alcanzar el seq2seq basado en RNN

Casi nunca, para nuevos proyectos.

> Para los nuevos proyectos casi no hay excepciones específicas:

- Traducción de transmisión donde consumes entrada un token a la vez con memoria limitada.
  流式翻译, por token 消耗输入,内存有界──
- Generación de texto en el dispositivo donde el costo de la memoria del transformador es prohibitivo.
  设备端文本生成,Transformer 内存成本过高──
- Comprender el cuello de botella del codificador y el decodificador es el camino más rápido para entender por qué ganaron los transformadores.
  Enseñanza... Comprender el codificador-descodificador... es entender el transformador por qué es el camino más rápido de la victoria...

### El sesgo de exposición y sus mitigantes

- **Scheduled sampling.**La proporción de fuerza del profesor durante la formación para que el modelo aprenda a recuperarse de sus propios errores.
  **计划采样（Scheduled Sampling）。**En el entrenamiento, el profesor regresa a la escuela para que el profesor se recupere de sus errores
- **Minimum risk training.**Entrenando en la puntuación BLEU de nivel de oración en lugar de la entropía cruzada de nivel de token.
  **最小风险训练（Minimum Risk Training）。**En la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea de línea
- **Reinforcement learning fine-tuning.**Recompensar el generador de secuencias con una métrica.
  **强化学习微调。**Utilizando la tecnología de la información y la información de los usuarios.

Los tres todavía se aplican a la generación basada en transformadores.

> Este último sigue siendo aplicable para la generación basada en el Transformer.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

## Envíe el producto .

Salvo como`outputs/prompt-seq2seq-design.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/prompt-seq2seq-design.md`¿Qué es esto ?

```markdown
---
name: seq2seq-design
description: Design a sequence-to-sequence pipeline for a given task.
phase: 5
lesson: 09
---

Given a task (translation, summarization, paraphrase, question rewrite), output:

1. Architecture. Pretrained transformer encoder-decoder (BART, T5, mBART, NLLB) is the default. RNN-based seq2seq only for specific constraints.
2. Starting checkpoint. Name it (`facebook/bart-base`, `google/flan-t5-base`, `facebook/nllb-200-distilled-600M`). Match the checkpoint to task and language coverage.
3. Decoding strategy. Greedy for deterministic output, beam search (width 4-5) for quality, sampling with temperature for diversity. One sentence justification.
4. One failure mode to verify before shipping. Exposure bias manifests as generation drift on longer outputs; sample 20 outputs at the 90th-percentile length and eyeball.

Refuse to recommend training a seq2seq from scratch for under a million parallel examples. Flag any pipeline that uses greedy decoding for user-facing content as fragile (greedy repeats and loops).
```

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista

## Los ejercicios.

1. **Easy.**Implemente la tarea de copia de juguete. Entrenar un GRU seq2seq en pares de entrada y salida donde el objetivo es igual a la fuente. Medir la precisión en longitudes 5, 10, 20. Reproduce el cuello de botella.
   **简单。**实现玩具复制任务──训练 GRU seq2seq 在目标等于源的输入输出对上──测量长度 5、10、20 的准确率──复现瓶──
2. **Medium.**Añadir la decodificación de búsqueda de haces con ancho de haces 3. Medir el color azul en un corpus paralelo pequeño contra la codicia.
   **中等。**添加束宽度为 3 的束搜索解码──在小平行语料上测量对贪心的 BLEU──记录束搜索在哪里胜出(usualmente son los últimos pocos tokens) así como en donde no hay diferencia──
3. **Hard.**- No . - ¿ Qué ?`facebook/bart-base`comparar la salida de haz-4 del modelo ajustado con la del modelo base en entradas retenidas.
   **困难。**En el conjunto de datos de 10 000 para la liberación`facebook/bart-base`◊ en el grupo de modelos de baja calidad en la entrada de salida 4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.

## Términos clave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Encoder（编码器） | Input RNN / 输入 RNN | Reads source. Produces per-step hidden states and a final context vector. / 读取源。产生逐步隐藏状态和最终上下文向量。 |
| Decoder（解码器） | Output RNN / 输出 RNN | Initialized from context vector. Generates target tokens one at a time. / 从上下文向量初始化。逐个生成目标 token。 |
| Context vector（上下文向量） | The summary / 摘要 | Final encoder hidden state. Fixed size. The bottleneck attention solves. / 最终编码器隐藏状态。固定大小。注意力解决的瓶颈。 |
| Teacher forcing（教师强制） | Use true tokens / 使用真实 token | Feed the ground-truth previous token at training time. Stabilizes learning. / 训练时馈入真实的前一个 token。稳定学习。 |
| Exposure bias（暴露偏差） | Train/test gap / 训练/测试差距 | Model trained on true tokens never practiced recovering from its own mistakes. / 在真实 token 上训练的模型从未练习从自己的错误中恢复。 |
| Beam search（束搜索） | Better decoding / 更好的解码 | Keep top-k partial sequences alive at each step instead of committing greedily. / 每步保持排名前 k 的部分序列存活，而非贪心提交。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.

## Más Leer más Leer más

- [Sutskever, Vinyals, Le (2014). Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215) el papel original de la secuencia. Cuatro páginas. / 原始 seq2seq 论文──四页──
- [Cho et al. (2014). Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078) introdujo el GRU y el marco de codificación y decodificación. / 引入了 GRU 和编码器-解码器框架──
- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) el papel de atención. Lea inmediatamente después de esta lección. / 注意力论文──在本课后立即阅读──
- [PyTorch NLP from Scratch tutorial](https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html) Seq2seq + código de atención. / 可构建的 seq2seq + 注意力代码──
