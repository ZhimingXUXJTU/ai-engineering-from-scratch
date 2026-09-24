# CNN y RNN para texto

> Las convoluciones aprenden n-gramos. las repeticiones recuerdan. ambas son reemplazadas por la atención. ambas siguen siendo importantes en hardware limitado.
> 卷积学习 n-gram──循环负责记忆── ambos fueron reemplazados por el mecanismo de atención── pero siguen siendo importantes en los hardware restringidos──

> **【中文解读】**CNN 捕捉局部 n-gram 特征,RNN 处理长程依赖──Transformer 之前的主流架构──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 11 (PyTorch Intro), Phase 5 · 03 (Word Embeddings), Phase 4 · 02 (Convolutions from Scratch) | **前置知识:** Phase 3 · 11（PyTorch 入门），Phase 5 · 03（词嵌入），Phase 4 · 02（从零实现卷积）
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

TF-IDF y Word2Vec producen vectores planos que ignoran el orden de palabras.`dog bites man`de la`man bites dog`El orden de palabras a veces lleva la señal.

> TF-IDF y Word2Vec  generan 平向量 of word sequences 平向量 .`dog bites man`Y `man bites dog`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊   ◊ ◊ ◊  ◊ ◊    ◊ ◊    ◊ ◊  ◊ ◊            ◊    ◊ ◊                  ◊          ◊                                                                                              

Dos familias de arquitecturas llenaron ese vacío antes de que llegaran los transformadores.

> Antes de que apareciera el Transformer, las dos tribus llenaron este vacío.

**Convolutional nets for text (TextCNN).**Aplicar convulsiones 1D sobre secuencias de incorporaciones de palabras. Un filtro de ancho 3 es un detector de trigramas aprendizable: abarca tres palabras y saca una puntuación. Apila diferentes anchos (2, 3, 4, 5) para detectar patrones de múltiples escalas.

> **文本卷积网络（TextCNN）。**En palabras de inserción en la secuencia de aplicación una dimensión de volumen. La amplitud de 3 波器 es un tres grupos de detectores de aprendizaje: se cruza tres palabras y se produce un número de partículas. Se compone de diferentes amplitudes.

**Recurrent nets (RNN, LSTM, GRU).**Procesar tokens uno a la vez, manteniendo un estado oculto que transporta la información hacia adelante. Secuenciales, con capacidad de memoria, comprimentos de entrada flexibles.

> **循环网络（RNN、LSTM、GRU）。**个个处理代币,维护向前传递信息的隐藏状态――顺序、有记忆、灵活输入长度── de 2014 a 2017 años se construyó la serie dominante, luego apareció el mecanismo de atención―

Esta lección construye ambos, y luego nombra el fracaso que motivó la atención.

> Este curso construye ambos, y luego señala el fracaso del motor de la atención.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

**TextCNN**Los tokens se incorporan.`k`La convolución 1D desliza un filtro en forma consecutiva `k`-gramos de embebidos, que producen un mapa de características. Global max-pooling sobre ese mapa elige la activación más fuerte. Concatenate max-pooled salidas de varios filtros anchos. alimentación a una cabeza de clasificador.

> **TextCNN**(Kim, 2014)  Token 被嵌入──宽度为 `k`de un volumen en continuo.`k`-grama 嵌上滑波器,产生特征图―― para hacer el gráfico de la característica en general, seleccionar la mayor acumulación de la mayor cantidad de activaciones─ de la mayor cantidad de 波器 de amplitud 波器 de la mayor cantidad de acumulación 波器 de la mayor cantidad de la producción 拼接──送入分类器头──

Por qué funciona. Un filtro es un n-gram aprendible. El max-pooling es invariable en posición, por lo que "no bueno" dispara la misma característica al comienzo o a mediados de una revisión. Tres anchos de filtro con 100 filtros cada uno te da 300 detectores de n-gram aprendices. El entrenamiento es paralelo; no hay dependencia secuencial.

> Por qué es efectivo? 波器是可学习的 n-gram──最大池化是位置不变的,所以"no es bueno" en comentarios iniciales o intermedios触发相同特征──三个波器宽度各100 波器给你300 个可学习的 n-gram 检测器── entrenamiento es paralelos; no depende de orden──

**RNN.**En cada paso .`t`, el estado oculto .`h_t = f(W * x_t + U * h_{t-1} + b)`- Compartir .`W`¿ Qué ?`U`¿ Qué ?`b`El estado oculto en el tiempo.`T`Es un resumen de todo el prefijo.`h_1 ... h_T`(máximo, medio o último).

> **RNN。**En cada paso del tiempo`t`, estado oculto`h_t = f(W * x_t + U * h_{t-1} + b)`¿Qué es eso?`W`¿Qué es esto?`U`¿Qué es esto?`b`跨时间共享──时间 `T`El estado oculto es el resumen de todo el anterior.`h_1 ... h_T`La mayor de las veces, el valor medio o el final.

Las RNN simples sufren de desvanecimiento de los gradientes.**LSTM**añade puertas que deciden qué olvidar, qué almacenar y qué sacar, estabilizando los gradientes a través de largas secuencias.**GRU**simplifica el LSTM a dos puertas; funciona de manera similar con menos parámetros.

> Normal RNN  exist gradiente desaparecimiento problema¬**LSTM**Añadir decisiones olvidar lo que ¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿**GRU**Simplificar LSTM en dos puertas; los parámetros son menores pero el efecto es similar.

**Bidirectional RNNs**ejecutar un RNN hacia adelante y otro hacia atrás, concatenando estados ocultos. la representación de cada token ve tanto el contexto izquierdo como el derecho. Es esencial para etiquetar tareas.

> **双向 RNN**运行一个RNN向前、另一个向后,拼接隐藏状态──每个代币的表示看左右两侧的上下文──对标注任务必不可少──

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.
```figure
rnn-unroll
```

## Construye el mismo

### Paso 1: TextCNN en PyTorch

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


class TextCNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, n_classes, filter_widths=(2, 3, 4), n_filters=64, dropout=0.3):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.convs = nn.ModuleList([
            nn.Conv1d(embed_dim, n_filters, kernel_size=k)
            for k in filter_widths
        ])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(n_filters * len(filter_widths), n_classes)

    def forward(self, token_ids):
        x = self.embed(token_ids).transpose(1, 2)
        pooled = []
        for conv in self.convs:
            c = F.relu(conv(x))
            p = F.max_pool1d(c, c.size(2)).squeeze(2)
            pooled.append(p)
        h = torch.cat(pooled, dim=1)
        return self.fc(self.dropout(h))
```

El `transpose(1, 2)`reformulaciones `[batch, seq_len, embed_dim]`¿ Qué ?`[batch, embed_dim, seq_len]`Porque ...`nn.Conv1d`El eje medio se trata de canales.

> `transpose(1, 2)`¿ Qué ?`[batch, seq_len, embed_dim]`La carga de la carga`[batch, embed_dim, seq_len]`, porque `nn.Conv1d`La salida posterior a la acumulación es de tamaño fijo, independientemente de la longitud de la entrada.

### Paso 2: Clasificador LSTM

```python
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_classes, bidirectional=True, dropout=0.3):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=bidirectional)
        factor = 2 if bidirectional else 1
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * factor, n_classes)

    def forward(self, token_ids):
        x = self.embed(token_ids)
        out, _ = self.lstm(x)
        pooled = out.max(dim=1).values
        return self.fc(self.dropout(pooled))
```

Para la clasificación, el max-pooling suele superar el tomar el último estado oculto porque la información al final de una larga secuencia tiende a dominar el último estado.

> En la secuencia se hace la mayor acumulación, en lugar de la acumulación de estado final. Para la clasificación, la mayor acumulación suele ser mejor que la acumulación de estado oculto final, ya que la información del extremo de la secuencia larga tiende a dominar el estado final.

### Paso 3: la demostración de gradiente de desaparición (intucción)

Un RNN simple sin gate no puede aprender dependencias a largo alcance.`A`apareció en cualquier parte de una secuencia.`A`Si el gradiente de la pérdida tiene que fluir de nuevo a través de 99 multiplicidades del peso recurrente. si el peso es menor a 1, el gradiente desaparece. si más de 1, explota.

> 没有门控的普通RNN 无法学习长程依赖――考虑一个玩具任务:预测 token `A`Sí, si está en cualquier lugar de la serie.`A`En la posición 1, la longitud del secuestro es de 100, el grado de pérdida debe pasar por 99 veces el ciclo de multiplicidad del peso de la corriente. Si el peso es menor que 1, el grado desaparece. Si es mayor que 1, el grado de explosión.

```python
def vanishing_gradient_sim(seq_len, recurrent_weight=0.9):
    import math
    return math.pow(recurrent_weight, seq_len)


# At weight=0.9 over 100 steps:
#   0.9 ^ 100 ≈ 2.7e-5
# The gradient from step 100 to step 1 is effectively zero.
```

Los LSTMs arreglan esto con un**cell state**Las GRU hacen algo similar con menos parámetros. Ambos te dan un entrenamiento estable a través de 100+ secuencias de pasos.

> LSTM  por un**细胞状态** solucionó este problema, este estado sólo se ha hecho mediante la adición de la interacción a través de la red  olvidar la reducción de la multiplicación, pero el gradiente sigue fluyendo en la "autopista"  GRU ha hecho cosas similares con menos parámetros  ambos te permiten entrenar en la estabilidad en una secuencia de 100 pasos 

### Paso 4: por qué esto todavía no era suficiente

Tres problemas persistieron incluso con los LSTM.

> Incluso si hay LSTM, tres problemas persisten.

1. **Sequential bottleneck.**El entrenamiento de un RNN en una secuencia de longitud 1000 requiere 1000 pasos en serie hacia adelante/hacia atrás.
   **顺序瓶颈。**En la longitud para 1000 de la secuencia de entrenamiento RNN necesita 1000 de las líneas de pasos hacia / hacia atrás.
2. **Fixed-size context vector in encoder-decoder setups.**El decodificador sólo ve el estado oculto final del codificador, comprimido sobre toda la entrada. Las entradas largas pierden detalles. La lección 09 cubre esto directamente.
   **编码器-解码器中的固定大小上下文向量。**El descifrador sólo ve el estado oculto final del codificador, comprimiendo toda la entrada.
3. **Distant-dependency accuracy ceiling.**Los LSTM superan a los RNNs comunes pero aún luchan por propagar información específica a través de más de 200 pasos.
   **远距离依赖准确率天花板。**LSTM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

La atención resolvió las tres. los transformadores han dejado de recurrir.

> Atención resuelve todos los tres problemas. El transformador ha abandonado por completo el ciclo.

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

El de PyTorch.`nn.LSTM`¿ Qué ?`nn.GRU`, y `nn.Conv1d`El código de entrenamiento es estándar.

> PyTorch de `nn.LSTM`¿Qué es esto?`nn.GRU`Y `nn.Conv1d`Es la producción de la formación.

Embracing Face naves preentrenadas embeddings que se conecta como la capa de entrada:

> Abrazar la cara  proporcionar entrenamiento pre 嵌入作为输入层插入:

```python
from transformers import AutoModel

encoder = AutoModel.from_pretrained("bert-base-uncased")
for param in encoder.parameters():
    param.requires_grad = False


class BertCNN(nn.Module):
    def __init__(self, n_classes, filter_widths=(2, 3, 4), n_filters=64):
        super().__init__()
        self.encoder = encoder
        self.convs = nn.ModuleList([nn.Conv1d(768, n_filters, kernel_size=k) for k in filter_widths])
        self.fc = nn.Linear(n_filters * len(filter_widths), n_classes)

    def forward(self, input_ids, attention_mask):
        with torch.no_grad():
            out = self.encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        x = out.transpose(1, 2)
        pooled = [F.max_pool1d(F.relu(conv(x)), kernel_size=conv(x).size(2)).squeeze(2) for conv in self.convs]
        return self.fc(torch.cat(pooled, dim=1))
```

Lista de control de uso cuando se ajuste a las restricciones.

> 适用约束检查清单──

- **Edge / on-device inference.**TextCNN con GloVe embedded es 10-100 veces más pequeño que un transformador. Si tu objetivo de despliegue es un teléfono, esta es la pila.
  **边缘/设备端推理。**带 GloVe 嵌入的 TextCNN 比变压器 小 10-100 倍──如果部署目标是手机,这就是你的技术──
- **Streaming / online classification.**RNN procesa un token a la vez; los transformadores necesitan la secuencia completa. Para el texto entrante en tiempo real, los LSTMs aún ganan.
  **流式/在线分类。**RNN Cada vez que se procesa un token; Transformer  necesita un proceso completo.
- **Tiny models for baselines.**Una nueva tarea es rápida, entrenar un TextCNN en 5 minutos en una CPU.
  **用于基线的微型模型。**En la nueva tarea, rápido. En la CPU, en 5 minutos, entrenando un texto.
- **Sequence labeling with limited data.**BiLSTM-CRF (lección 06) es todavía una arquitectura NER de grado de producción para oraciones etiquetadas 1k-10k.
  **数据有限的序列标注。**BiLSTM-CRF (第 06 课) para 1k-10k 标注句子 todavía es producción de NER 架构──

Todo lo demás va a un transformador.

> Todo lo demás con el Transformer.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

## Envíe el producto .

Salvo como`outputs/prompt-text-encoder-picker.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/prompt-text-encoder-picker.md`¿Qué es esto ?

```markdown
---
name: text-encoder-picker
description: Pick a text encoder architecture for a given constraint set.
phase: 5
lesson: 08
---

Given constraints (task, data volume, latency budget, deploy target, compute budget), output:

1. Encoder architecture: TextCNN, BiLSTM, BiLSTM-CRF, transformer fine-tune, or "use a pretrained transformer as a frozen encoder + small head".
2. Embedding input: random init, GloVe / fastText frozen, or contextualized transformer embeddings.
3. Training recipe in 5 lines: optimizer, learning rate, batch size, epochs, regularization.
4. One monitoring signal. For RNN/CNN models: attention mechanism absence means they miss long-range deps; check per-length accuracy. For transformers: fine-tuning collapse if LR too high; check train loss.

Refuse to recommend fine-tuning a transformer when data is under ~500 labeled examples without showing that a TextCNN / BiLSTM baseline has plateaued. Flag edge deployment as needing architecture-before-everything.
```

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista

## Los ejercicios.

1. **Easy.**Entrenar a un TextCNN en un conjunto de datos de juguete de 3 clases (inventas los datos). Verifique que los anchos de filtro (2, 3, 4) superen un solo ancho (3) en promedio a F1.
   **简单。**En un conjunto de datos de 3 tipos de juguetes entrenar TextCNN((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
2. **Medium.**Implemente el pool máximo, el pool medio y el pool de último estado para el clasificador LSTM. Compara en un conjunto de datos pequeño; documento que gana el pool y hipotese por qué.
   **中等。**Para LSTM, el grupo de datos puede obtener la mayor acumulación, la media y el estado final de la acumulación.
3. **Hard.**Construye un etiquetado BiLSTM-CRF NER (combina la lección 06 y esta). Entrenar en CoNLL-2003. Compara con la línea de base de CRF sola de la lección 06 y con un ajuste fino de BERT. Informar el tiempo de entrenamiento, la memoria y la F1.
   **困难。**Construir BiLSTM-CRF NER 标标标器(结合第 06 课和本课) ⋅ en CoNLL-2003 上训练──与第 06 课的纯CRF基线和BERT 微调比较──报告训练时间、内存和F1──

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.

## Términos clave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| TextCNN | CNN for text / 文本 CNN | Stack of 1D convolutions over word embeddings with global max-pool. Kim (2014). / 在词嵌入上堆叠一维卷积加全局最大池化。Kim (2014)。 |
| RNN（循环神经网络） | Recurrent net / 循环网络 | Hidden state updated at each time step: `h_t = f(W x_t + U h_{t-1})`. / 每个时间步更新隐藏状态：`h_t = f(W x_t + U h_{t-1})`。 |
| LSTM | Gated RNN / 门控 RNN | Adds input / forget / output gates + a cell state. Trains stably through long sequences. / 添加输入/遗忘/输出门 + 细胞状态。在长序列上稳定训练。 |
| GRU | Simpler LSTM / 更简单的 LSTM | Two gates instead of three. Similar accuracy, fewer parameters. / 两个门代替三个。类似准确率，更少参数。 |
| Bidirectional（双向） | Both directions / 两个方向 | Forward + backward RNN concatenated. Every token sees both sides of its context. / 前向 + 后向 RNN 拼接。每个 token 看到其上下文两侧。 |
| Vanishing gradient（梯度消失） | Training signal dies / 训练信号消失 | Repeated multiplication by <1 weights in plain RNNs makes early-step gradients effectively zero. / 普通 RNN 中对小于 1 的权重反复乘法使早期步骤的梯度实际上为零。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.

## Más Leer más Leer más

- [Kim, Y. (2014). Convolutional Neural Networks for Sentence Classification](https://arxiv.org/abs/1408.5882) el textoCNN papel. Ocho páginas. Leerable. / TextCNN 论文──八页──易读──
- [Hochreiter, S. and Schmidhuber, J. (1997). Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf) el papel de LSTM. Inesperadamente lúcido. / LSTM 论文──出乎意料地清晰──
- [Olah, C. (2015). Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/) los diagramas que hicieron que los LSTMs fueran accesibles a todos. /  Que los LSTM fueran comprensibles para todos.
