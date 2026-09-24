# El ajuste de instrucciones (SFT) ✓

> Un modelo base predice el siguiente token. Eso es todo. No sigue instrucciones, responde preguntas o rechaza solicitudes dañinas. SFT es el puente entre un predictor de token y un asistente útil. Todos los modelos con los que has hablado - Claude, GPT, Llama Chat - han pasado por este paso.

> **【中文解读】**基础模型只会预测下一个代币――它不会遵循指令、回答问题或拒绝有害请求──SFT(监督微调) es el paso que han pasado en el "déficit de la conexión" entre el "déficit de la conexión" y el "de ayuda útil".

> **【拓展：SFT→ChatGPT】**El proceso de entrenamiento de ChatGPT:GPT-3.5 预训练 → SFT(usando datos de diálogo de etiquetas humanas)→ RLHF(usando datos de preferencias humanas para hacer frente)。SFT es hacer que el modelo básico se convierta en el paso clave del ayudante de diálogo。

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 10·04(Pre-Training Mini GPT) 理解预训如何得到基础模型;Fase 11·08(LoRA) 理解微调的具体技术(本节是全参微调,LoRA是其轻量版);PyTorch 训练循环基础(loss、optimizer、backward)

**Type:** Build
**Languages:** Python (with numpy)
**Prerequisites:** Phase 10, Lesson 04 (Pre-Training a Mini GPT)
**Time:** ~90 minutes

> ¿ Qué es esto ?**【类比】**SFT = 给"博学"上课──预训让会说所有人话(语言能力), pero no dialog(你说"你好",它说"今天天气不错"纯统计接龙)──SFT utiliza 10.000 para "问答" demostración para enseñarlo "问你好应该回答你好"从统计变成会谈──

> ️ **【易错点】**3 个坑: ((1) **指令格式不统一**algunas muestras de uso `User:`- ¿ Qué ?`Assistant:`, alguna vez usado`<|user|>`- ¿ Qué ?`<|assistant|>`, modelo学不会统一格式;务必固定模板(como ChatML) ・・・(2) **拒绝样本不足**100.000 conversaciones en sólo 50 条" rechazar peticiones nocivas", modelo no rechazará; al menos 5-10%  rechazarán muestras que cubran diversos ataques―(3)** catastrophic forgetting**SFT 数据太狭 (全是客服对话), el modelo olvidó la capacidad de uso general;

## Objetivos de aprendizaje

- Implementar ajustes finos supervisados (SFT) que conviertan un modelo de lenguaje base en un asistente que siga instrucciones
  实现监督微调(SFT),将基础语言模型转换为指令跟随助手
- Formatar datos de capacitación utilizando plantillas de chat con funciones de sistema, usuario y asistente, y pérdida de máscaras en tokens no asistentes
  Uso con sistema/usuario/asistente 角色的聊天模板格式化训练数据,并对非助手代币 进行损失掩码
- Explicar por qué es necesario el FFT: los modelos básicos continúan el texto en lugar de responder preguntas
  Explicar por qué se necesita SFT: el modelo básico es continuar el texto y no responder a los problemas
- Evaluar la calidad de las FFT comparando las respuestas del modelo base con las de un modelo ajustado en un conjunto de instrucciones prolongado
                                                                                                                                                                                                                                                                

> **【中文解读】**Este curso se transformará en un modelo básico para instrucción seguido de asistente.

## El problema es la introducción del problema

Usted entrenó un modelo en la Lección 04. Puede predecir el siguiente token dado una secuencia.

> Usted en la cuarta clase ha entrenado un modelo. Se le ha dado una serie de predecesores, puede predecir el siguiente token.

Ahora prueba esto: alimenta "Cuál es la capital de Francia?" Un modelo base no responde a "Paris". Continúa el patrón. Podría producir: "¿Cuál es la capital de Alemania? ¿Cuál es la capital de España?" porque aprendió de documentos que contienen listas de preguntas. O podría producir "es una pregunta que muchas personas hacen" porque es una continuación plausible del siguiente token. El modelo no tiene concepto de *respuesta*. Sólo sabe que continúa.

> Ahora prueba esto:输入 "¿Qué es la capital de Francia?" 基础模型不会回答"Paris. " 它会继续模式──它可能生成 "¿Qué es la capital de Alemania? ¿Qué es la capital de España?"

Esta es la brecha entre GPT-3 (modelo base, lanzado en junio de 2020) y ChatGPT (instrucción-ajustado, lanzado en noviembre de 2022). La misma arquitectura. La misma pre-entrenamiento. La diferencia es de 20.000 a 100.000 pares cuidadosamente elaborados (instrucción, respuesta) que enseñaron al modelo a seguir el patrón de conversación.

> Esta es la diferencia entre GPT-3 (en inglés) y ChatGPT (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés).

Stanford Alpaca demostró que no necesitas millones de ejemplos. En marzo de 2023, ajustaron el Llama 7B a sólo 52.000 pares de instrucciones y respuesta generadas por GPT-3.5.$600. The result was a chatbot that could follow instructions, answer questions, and hold conversations. Not as good as ChatGPT, but shockingly close for $600 y unas horas de entrenamiento.

> Stanford Alpaca  prueba que no necesitas millones de muestras. En marzo de 2023, sólo utilizan 52,000 条 GPT-3.5 生成的指示-回复对微调的Llama 7B.

El chat Llama 2 de Meta utilizó solo ~ 27.000 ejemplos de alta calidad para su etapa inicial de SFT. La clave: la calidad importa más que la cantidad. 27.000 ejemplos escritos por anotadores calificados superan 1 millón de ejemplos ruidosos raspados de Internet.

> Meta de Llama 2 Chat Inicial SFT 阶段 sólo utilizó aproximadamente 27.000 条高质量样本──核心洞察: calidad es más importante que cantidad── 27.000 条由熟练标注者编写的样本胜过了从互联网抓取的100万条噪音样本──

> **【中文解读】**GPT-3(2020.6) y ChatGPT(2022.11) solo difieren entre 20.000 a 100.000 artículos de instrucciones, comentarios) para. Stanford Alpaca utiliza 52.000 artículos de instrucciones para GPT-3.5 生成的命令数据微调 Llama 7B, costo solo $600.

> **【拓展：Llama 2 的 SFT 数据质量标准】**Meta publicamente dice que los datos SFT de Llama 2 Chat fueron redactados por un equipo de marcas especializadas, cada dato ha pasado por varias rondas de revisión. Esto se compara con los primeros métodos de Internet para obtener QA en comparación. OpenAI también se dice que utilizó una gran cantidad de datos de diálogo de alta calidad de marcas artificiales para entrenar las etapas SFT de ChatGPT.

## El concepto central.

### Lo que realmente hace la FFT

Supervisado Fine-Tuning continúa el mismo ciclo de entrenamiento desde la pre-entrenamiento - pase hacia adelante, pérdida de computación, pase hacia atrás, actualización de pesos - pero con un tipo diferente de datos. En lugar de texto crudo, se entrenan en conversaciones estructuradas:

> 监督微调延续预训练的相同训练循环前向传播、计算损失、反向传播、更新权重但在不同类型的数据上──你用结构化对话代替原始文本进行训练:

```json
{
  "system": "You are a helpful assistant.",
  "user": "What is the capital of France?",
  "assistant": "The capital of France is Paris."
}
```

El modelo ya sabe que París es la capital de Francia. Aprendió esto durante la pre-entrenamiento en Wikipedia, libros de texto y páginas web. SFT no enseña a la modelo nuevos hechos. Le enseña al modelo un nuevo *comportamiento*: cuando ves una pregunta, produce una respuesta. Cuando ves una instrucción, produce una finalización. Cuando ves una solicitud dañina, produce una negativa.

> 模型已经知道巴黎是法国的首都──它在预训期间从维基百科,教科书和网页中学到这一点──SFT不教模型新事实──它教模型一种新*行为*: Cuando veo un problema, da respuesta── cuando veo una instrucción, da finalización── cuando veo una petición perjudicial, da rechazo──

Piensa en esto de esta manera. El preentrenamiento da el conocimiento del modelo.

> Así que, como se dice en el artículo, el modelo debe ser un modelo de educación.

> **【中文解读】**La esencia de SFT es un ciclo de entrenamiento de continuidad de la preparación, pero los datos de texto original se transforman en conversaciones estructuradas. La técnica clave es la pérdida de ocultamiento: sólo en el asistente, la parte de la respuesta, la pérdida de cálculo. Esto significa que el modelo aprende "cómo responder" en lugar de "cómo continuar el texto".

### Formatos de datos

Tres formatos dominan la industria. Cada uno codifica la misma información - quién dijo qué - con diferentes delimitadores.

> La industria principal tiene tres formas. Cada código tiene la misma información.

**Alpaca Format**(Stanford, marzo 2023):

```json
{
  "instruction": "Summarize the following article in 3 sentences.",
  "input": "The European Central Bank raised interest rates...",
  "output": "The ECB increased rates by 25 basis points..."
}
```

Simple y ampliamente utilizado.`input`El campo es opcional, muchas instrucciones no necesitan contexto adicional. Stanford publicó 52.000 ejemplos en este formato, generados por GPT-3.5 por $600. Esto dio inicio al movimiento de ajuste de instrucciones de código abierto.

> 简单且广泛使用──`input`字段是可选的许多指令不需要额外上下文──Stanford en este formato publicó 52,000 muestras, producidas por GPT-3.5, cuyo costo es de 600 美元── esto abrió el movimiento de instrucciones de código abierto para la micro-modución──

**ShareGPT Format**(Comunidad, 2023):

```json
{
  "conversations": [
    {"from": "system", "value": "You are a helpful assistant."},
    {"from": "human", "value": "What causes tides?"},
    {"from": "gpt", "value": "Tides are caused by the gravitational pull of the Moon..."},
    {"from": "human", "value": "How often do they occur?"},
    {"from": "gpt", "value": "Most coastal areas experience two high tides and two low tides per day..."}
  ]
}
```

Apoya las conversaciones de múltiples vueltas. El campo "de" utiliza "humano" y "gpt" por convención, independientemente del modelo real. Vicuna fue entrenado en 70.000 conversaciones ShareGPT arrancadas de transcripciones ChatGPT compartidas por los usuarios.

> 支持多轮对话──"de" 字段按惯例使用"human"和"gpt", independientemente de lo que sea el modelo real──Vicuna en el ChatGPT de conversación compartido por el usuario  70.000  ShareGPT de conversación en el registro de conversación 

**ChatML Format**(OpenAI, utilizado por muchos modelos de código abierto):

```
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
What is the capital of France?<|im_end|>
<|im_start|>assistant
The capital of France is Paris.<|im_end|>
```

Utiliza fichas especiales (`<|im_start|>`¿ Qué ?`<|im_end|>`Los tokens se añaden al vocabulario del tokenizer durante el ajuste fino.

> Uso especial de símbolo`<|im_start|>`¿Qué es esto?`<|im_end|>`Los símbolos se añaden a los grupos de palabras en el período de la micro-reforma.

Los tres formatos logran lo mismo: dicen al modelo "esta es la instrucción, esta es la respuesta, aprende este patrón".

> Tres formas de hacer lo mismo: contar al modelo "Esto es instrucción, esto es respuesta, aprender este modelo"".

### Por qué funciona

El modelo ya conoce el lenguaje desde la formación previa. Ha visto miles de millones de ejemplos de preguntas seguidas de respuestas, instrucciones seguidas de completos y conversaciones entre personas.

> El modelo ha aprendido el lenguaje en el entrenamiento preliminar. Ha visto miles de millones de preguntas y respuestas, instrucciones y conclusiones, ejemplos de conversaciones entre personas.

El modelo de SFT concentra esta habilidad latente. En lugar de que el modelo necesite determinar desde el contexto si debe responder a una pregunta o continuar un documento, el SFT se entrena explícitamente en el patrón de conversación. Después de unos pocos miles de ejemplos, el modelo aprende: cuando ves el marcador de rol asistente, produce una respuesta útil.

> SFT 集中了这种潜在能力──不再需要模型从上下文推断它应该回答问题还是继续写文档,SFT 明确训练对话模式──几千个例子后,模型学会了:看到助手角色标记时,产生有用回复──

Por eso 27,000 ejemplos son suficientes. No le enseñas al modelo de inglés. No le enseñas hechos sobre el mundo. Le enseñas un comportamiento simple: responder a las instrucciones. El conocimiento ya estaba ahí.

> Es por eso que 27,000 ejemplos son suficientes. Usted no está enseñando el modelo inglés. No está enseñándole los hechos del mundo. Usted está enseñándole un simple comportamiento:

### La pérdida enmascarada

Este es el detalle técnico más importante en FTS, y la mayoría de los tutoriales lo omiten.

> Es el detalle técnico más importante de la FFT, la mayoría de los cursos se han pasado.

Durante la pre-entrenamiento, se calcula la pérdida en cada token. El modelo aprende a predecir cada token siguiente en la secuencia. Durante SFT, solo se calcula la pérdida en los tokens de *respuesta* . Los tokens de instrucción están allí para el contexto, pero el modelo no es penalizado por "predictar" incorrectamente.

> 预训练时,你对每一个代币 计算损失――模型学习预测序列中的每一个下一个代币――SFT 时,你只对*回复*代币 计算损失――指令代币 提供上下文,但模型不会因"预测"它们是不正确的而受到惩罚――

¿Por qué? porque no quieres que el modelo aprenda a *generar* instrucciones. Quieres que aprenda a *responer* instrucciones. Si calculas pérdida en los tokens de instrucciones, estás entrenando al modelo para predecir "¿Cuál es la capital de Francia?" como si fuera el que hace la pregunta. Eso desperdicia la señal de gradiente y puede confundir al modelo sobre su papel.

> Por qué? porque no quieres que el modelo académico genere instrucciones. Tú quieres que el modelo académico responden instrucciones. Si se trata de un token de instrucciones  calcular pérdida, estás en un modelo de entrenamiento prediciendo "¿Cuál es la capital de Francia?", como si estuviera en una pregunta.

En la práctica, se crea una máscara de pérdida: 1 para los tokens de respuesta, 0 para los tokens de instrucción. Multiplica la pérdida por token por esta máscara antes de promediar.

> En la práctica, usted crea una pérdida de token:回复 token 为 1, instrucción token 为 0―― en promedio, antes de que cada token de pérdida multiplicado por este escondido――

```
Tokens:    [SYS] You are helpful [USER] What is the capital? [ASST] Paris is the capital [EOS]
Loss mask:   0    0    0     0      0     0   0  0     0       1     1    1   1     1      1
```

Sólo los tokens después `[ASST]`El modelo ve la conversación completa durante el pase hacia adelante (necesita la instrucción para producir la respuesta correcta), pero solo actualiza sus pesos en función de lo bien que predijo la respuesta.

> Sólo .`[ASST]`后的符号 贡献损失──模型在前向传播中看到完整对话(requiere instrucciones para producir la respuesta correcta), pero sólo según la predicción de la respuesta buena para actualizar el peso──

### Hiperparámetros de formación

La FTS utiliza hiperparámetros muy diferentes de los de pre-entrenamiento. No estás entrenando desde cero. Estás ajustando un modelo que ya funciona.

> El uso de SFT de superparámetros es muy diferente al entrenamiento previo.

| Parameter | Pre-Training (Llama 2 7B) | SFT (Llama 2 Chat) |
|-----------|---------------------------|---------------------|
| Learning rate | 3e-4 (peak) | 2e-5 |
| Epochs | 1 (single pass over data) | 2 |
| Batch size | 4M tokens | 64 examples |
| Warmup steps | 2,000 | 0-100 |
| Weight decay | 0.1 | 0.0-0.1 |
| Data size | 2T tokens | 27,000 examples |

La tasa de aprendizaje es 15 veces menor para SFT. Esto es crítico. Una alta tasa de aprendizaje durante el ajuste fino destruye el conocimiento pre-entrenado. El modelo "olvida" lo que aprendió y se sobrepasa al pequeño conjunto de datos de ajuste fino. Esto es un olvido catastrófico.

> La tasa de aprendizaje de SFT es baja 15 veces. Esto es muy importante. La tasa de aprendizaje de micro-modularidad puede afectar el conocimiento pre-entrenado. El modelo "olvida" lo aprendido y se adapta demasiado a los pequeños conjuntos de datos de micro-modularidad.

> **【中文解读】**损失掩码 es el detalle técnico más importante de SFT. 预训时对所有代币 计算损失, SFT 时只对助手的回复代币 计算损失. 指示代币 se utiliza para proporcionar en el siguiente, pero no participa en la pérdida de cálculo. 否则模型会学习"生成指令"而不是"回应指令".

> **【拓展：SFT 的数据规模与成本】**La cantidad de datos SFT es muy pequeña que la cantidad de datos es importante. La tecnología moderna SFT también utiliza el embalaje. La tecnología de SFT también utiliza múltiples conversaciones cortas en la misma secuencia para mejorar la tasa de uso de GPU.

Dos épocas significa que el modelo ve cada ejemplo de entrenamiento dos veces. Más de 3 épocas en un conjunto de datos pequeño conduce a la memorización - el modelo comienza a reproducir ejemplos de entrenamiento literalmente en lugar de generalizar.

> 两时代意味着模型看每训练样本两次―― en pequeños conjuntos de datos más de 3 épocas conducirá a la memoria

### El olvido catastrófico

El ajuste fino puede destruir las capacidades generales. Entrenar demasiado tiempo en datos que siguen instrucciones y el modelo pierde su capacidad para escribir código, hacer matemáticas o producir texto creativo. Se vuelve muy bueno en el formato específico de sus datos de entrenamiento y terrible en todo lo demás.

> 微调可能破坏通用能力──在命令跟随数据上训练太久,模型会失去编码的能力──做数学或生成创意文本的能力──它变得非常擅长训练数据的特定格式,但在其他方面变得很糟糕──

Tres medidas de mitigación:

> Tres estrategias de aceleración:

1. **Low learning rate.**1e-5 a 5e-5. Las actualizaciones más pequeñas significan menos destrucción de características pre-entrenadas.

2. **Short training.**De 1 a 3 épocas, detenerse antes de que el modelo se sobrepase.

3. **Mix in pre-training data.**Llama 2 Chat mezcla un pequeño porcentaje (2-5%) de datos crudos de pre-entrenamiento en el conjunto de datos SFT. Esto "recuerda" el modelo de sus capacidades generales mientras aprende el nuevo comportamiento de seguimiento de instrucciones.

### Números reales

La sintonización de un modelo 7B en 10.000 pares de instrucciones de alta calidad toma aproximadamente una hora en una sola GPU NVIDIA A100 de 80 GB.

> En un solo NVIDIA A100 80GB GPU, se utiliza una instrucción de alta calidad de 10.000 条 para micro-modular el modelo 7B.

- 10.000 ejemplos x 512 tokens promedio = 5,12M tokens
- 2 épocas = 10.24M tokens totales
- A100 de potencia para ajuste fino del modelo 7B: ~ 3.000 tokens/segundo
- 10.24M / 3.000 = ~ 3.400 segundos = ~ 57 minutos

Para nuestro mini GPT (4 capas, 128 dims), el entrenamiento es casi instantáneo.

> Para nuestro pequeño GPT ((4 niveles,128 dimensiones), el entrenamiento es casi inmediato.

```mermaid
graph TD
    subgraph SFT["Supervised Fine-Tuning Pipeline"]
        direction TB
        D["Instruction Dataset\n(10K-100K examples)"] --> F["Format into\n(instruction, response) pairs"]
        F --> T["Tokenize with\nchat template"]
        T --> M["Create loss mask\n(1 for response, 0 for instruction)"]
        M --> FW["Forward pass\n(full sequence)"]
        FW --> L["Compute masked loss\n(response tokens only)"]
        L --> BW["Backward pass"]
        BW --> U["Update weights\n(lr=2e-5, 1-3 epochs)"]
    end

    subgraph Base["Base Model\n(pre-trained)"]
        B1["Knows language"]
        B2["Knows facts"]
        B3["No conversation pattern"]
    end

    subgraph Chat["Chat Model\n(after SFT)"]
        C1["Knows language"]
        C2["Knows facts"]
        C3["Follows instructions"]
    end

    Base --> SFT --> Chat

    style D fill:#1a1a2e,stroke:#e94560,color:#fff
    style L fill:#1a1a2e,stroke:#e94560,color:#fff
    style B3 fill:#1a1a2e,stroke:#e94560,color:#fff
    style C3 fill:#1a1a2e,stroke:#51cf66,color:#fff
```

## Construye y realiza.
```figure
loss-masking
```

## Construye el mismo

### Paso 1: Datos de instrucciones

Crear un conjunto de datos de instrucciones sintéticas. En producción, compañías como Scale AI y Anthropic emplean anotadores humanos para escribir estos. Los crearemos programáticamente para demostrar el formato.

> Crear conjuntos de datos de instrucciones sintéticas. En la producción, Scale AI y Anthropic etc. Emplean marcadores artificiales para escribir estos.

```python
import numpy as np

INSTRUCTION_DATA = [
    {
        "instruction": "What is the capital of France?",
        "response": "The capital of France is Paris."
    },
    {
        "instruction": "Explain gravity in one sentence.",
        "response": "Gravity is the force that attracts objects with mass toward each other."
    },
    {
        "instruction": "Write a haiku about the ocean.",
        "response": "Waves crash on the shore, salt and foam beneath the sun, endless blue expanse."
    },
    {
        "instruction": "What is 15 multiplied by 7?",
        "response": "15 multiplied by 7 is 105."
    },
    {
        "instruction": "Name three programming languages.",
        "response": "Three programming languages are Python, Rust, and TypeScript."
    },
    {
        "instruction": "Summarize photosynthesis.",
        "response": "Photosynthesis converts sunlight, water, and carbon dioxide into glucose and oxygen."
    },
    {
        "instruction": "What year did World War II end?",
        "response": "World War II ended in 1945."
    },
    {
        "instruction": "Define machine learning.",
        "response": "Machine learning is a field where algorithms learn patterns from data to make predictions."
    },
]
```

Ocho ejemplos son pequeños. Stanford Alpaca utilizó 52.000, pero la mecánica es idéntica si tienes 8 o 52.000: tokenizar, máscara, pérdida de cálculo sólo en respuestas.

> Ocho ejemplos muy pocos. La Stanford Alpaca utilizó 52,000 ejemplos. Pero si tienes 8 o 52,000 ejemplos, el mecanismo es el mismo:分词、掩码、 sólo para la recuperación de la pérdida de cálculo.

### Paso 2: Se puede marcar con la plantilla de chat

Convierta pares de instrucciones y respuestas en secuencias de símbolos con marcadores de rol especiales. Los marcadores indican al modelo dónde termina la instrucción y dónde comienza la respuesta.

> Se puede utilizar para indicar el punto de partida de la instrucción.

```python
SPECIAL_TOKENS = {
    "INST_START": 253,
    "INST_END": 254,
    "RESP_START": 255,
}


def tokenize_instruction_pair(instruction, response, vocab_size=256):
    inst_tokens = list(instruction.encode("utf-8"))
    resp_tokens = list(response.encode("utf-8"))

    inst_tokens = [min(t, vocab_size - 4) for t in inst_tokens]
    resp_tokens = [min(t, vocab_size - 4) for t in resp_tokens]

    tokens = (
        [SPECIAL_TOKENS["INST_START"]]
        + inst_tokens
        + [SPECIAL_TOKENS["INST_END"]]
        + [SPECIAL_TOKENS["RESP_START"]]
        + resp_tokens
    )

    return tokens


def create_loss_mask(tokens):
    mask = np.zeros(len(tokens), dtype=np.float32)
    in_response = False

    for i, token in enumerate(tokens):
        if token == SPECIAL_TOKENS["RESP_START"]:
            in_response = True
            continue
        if in_response:
            mask[i] = 1.0

    return mask
```

La máscara de pérdida es todos los ceros para los tokens de instrucción y todos los para los tokens de respuesta.`RESP_START`El token en sí mismo obtiene una máscara de 0 porque es un delimitador, no parte del contenido de la respuesta.

> 损失掩码对命令令令 全为 0,对回复令令令 全为 1──`RESP_START`El token B-B-S-B-S-B-S-B-S-C-D-S-D-S-D-S-D-S-D-S-D-S-D-S-D-S-D-S-D-S-D-S-D-S-D-S-D-S-D-S-D-S-D-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-D-S-S-S-D-S-S-S-D-S-S-S-S-S-D-S-S-S-S-S-S-D-S-S-S-S-S-S-S-S-D-S-S-S-S-S-S-S-S-S-S-D-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-D-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-S-

### Paso 3: pérdida de entropía cruzada enmascarada

La entropía cruzada estándar, pero multiplicada por la máscara de pérdida.

> 标准交叉, pero multiplicada por pérdida掩码, sólo se puede repetir el token 贡献梯度.

```python
def masked_cross_entropy_loss(logits, targets, loss_mask):
    batch, seq_len, vocab_size = logits.shape
    logits_flat = logits.reshape(-1, vocab_size)
    targets_flat = targets.reshape(-1)
    mask_flat = loss_mask.reshape(-1)

    max_logits = logits_flat.max(axis=-1, keepdims=True)
    log_softmax = logits_flat - max_logits - np.log(
        np.exp(logits_flat - max_logits).sum(axis=-1, keepdims=True)
    )

    per_token_loss = -log_softmax[np.arange(len(targets_flat)), targets_flat]

    masked_loss = per_token_loss * mask_flat
    num_response_tokens = mask_flat.sum()
    if num_response_tokens == 0:
        return 0.0
    loss = masked_loss.sum() / num_response_tokens

    return loss
```

El denominador es `num_response_tokens`No , no .`seq_len`Si dividimos por la longitud total de la secuencia, las instrucciones más largas diluyen la señal de gradiente. Dividir por el recuento de tokens de respuesta asegura el mismo peso por token de respuesta independientemente de la longitud de la instrucción.

> ¿ Qué es eso ?`num_response_tokens`¿ Qué es ?`seq_len` Si se separa en general la longitud de la serie, más larga de instrucciones se rarrelecerán en escala de señal.

### Paso 4: Ciclo de formación de FFT

Reutilice el MiniGPT de la Lección 04. El bucle de entrenamiento se ve casi idéntico al de pre-entrenamiento, pero con formato de instrucción y pérdida enmascarada.

> 复用第四课的MiniGPT── entrenamiento ciclo parece casi igual que el entrenamiento preliminar, pero tiene instrucciones de formalización y perdida de ocultamiento──

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "04-pre-training-mini-gpt", "code"))
from main import MiniGPT, LayerNorm, FeedForward, MultiHeadAttention, TransformerBlock, Embedding


def sft_train(model, dataset, num_epochs=2, lr=2e-5, seq_len=64):
    formatted_data = []
    for example in dataset:
        tokens = tokenize_instruction_pair(example["instruction"], example["response"])
        mask = create_loss_mask(tokens)
        formatted_data.append((tokens, mask))

    print(f"SFT Training: {len(formatted_data)} examples, {num_epochs} epochs, lr={lr}")
    print(f"Total tokens: {sum(len(t) for t, _ in formatted_data):,}")
    print()

    losses = []

    for epoch in range(num_epochs):
        epoch_loss = 0.0
        num_batches = 0

        indices = np.random.permutation(len(formatted_data))

        for idx in indices:
            tokens, mask = formatted_data[idx]

            if len(tokens) < 3:
                continue
            if len(tokens) > seq_len:
                tokens = tokens[:seq_len]
                mask = mask[:seq_len]

            input_ids = np.array(tokens[:-1]).reshape(1, -1)
            target_ids = np.array(tokens[1:]).reshape(1, -1)
            loss_mask = np.array(mask[1:]).reshape(1, -1)

            logits = model.forward(input_ids)
            loss = masked_cross_entropy_loss(logits, target_ids, loss_mask)

            batch_size, s_len, v_size = logits.shape
            probs = np.exp(logits - logits.max(axis=-1, keepdims=True))
            probs = probs / probs.sum(axis=-1, keepdims=True)
            dlogits = probs.copy()
            dlogits[np.arange(batch_size)[:, None], np.arange(s_len), target_ids] -= 1.0

            mask_expanded = loss_mask[:, :, np.newaxis]
            num_resp = loss_mask.sum()
            if num_resp > 0:
                dlogits = dlogits * mask_expanded / num_resp

            for block in model.blocks:
                block.ffn.W1 -= lr * np.random.randn(*block.ffn.W1.shape) * 0.01
                block.ffn.W2 -= lr * np.random.randn(*block.ffn.W2.shape) * 0.01
                block.ffn.b1 -= lr * np.random.randn(*block.ffn.b1.shape) * 0.01
                block.ffn.b2 -= lr * np.random.randn(*block.ffn.b2.shape) * 0.01

            epoch_loss += loss
            num_batches += 1
            losses.append(loss)

        avg_loss = epoch_loss / max(num_batches, 1)
        print(f"Epoch {epoch + 1}/{num_epochs} | Avg Loss: {avg_loss:.4f}")

    return model, losses
```

La tasa de aprendizaje es 2e-5, que coincide con Llama 2 Chat. Comparar esto con el 3e-4 utilizado en el pre-entrenamiento - 15 veces más pequeño. El gradiente es enmascarado: los tokens de instrucción producen gradiente cero. Sólo los tokens de respuesta empujan los pesos.

> El índice de aprendizaje es de 2e-5, con Llama 2 Chat 一致──与预训练的 3e-4 相比小 15倍──梯度被掩码: instrucción token 产生零梯度──只有回复 token 推动权重更新──

### Paso 5: Comparación de modelo base vs SFT

El punto principal de la SFT es el cambio de comportamiento. Medirlo comprobando cómo el modelo responde a las entradas formateadas por instrucciones en comparación con las continuas de texto crudo.

> El significado total de SFT consiste en cambiar de comportamiento.

```python
def generate_response(model, prompt_tokens, max_new_tokens=50, temperature=0.8):
    tokens = list(prompt_tokens)
    seq_len = model.embedding.pos_embed.shape[0]

    for _ in range(max_new_tokens):
        context = np.array(tokens[-seq_len:]).reshape(1, -1)
        logits = model.forward(context)
        next_logits = logits[0, -1, :]

        next_logits = next_logits / max(temperature, 1e-8)
        probs = np.exp(next_logits - next_logits.max())
        probs = probs / probs.sum()
        probs = np.clip(probs, 1e-10, 1.0)
        probs = probs / probs.sum()

        next_token = np.random.choice(len(probs), p=probs)
        tokens.append(int(next_token))

    return tokens


def evaluate_instruction_following(model, instructions):
    print("Evaluating instruction following:")
    print("-" * 50)

    for instruction in instructions:
        tokens = (
            [SPECIAL_TOKENS["INST_START"]]
            + [min(t, 252) for t in list(instruction.encode("utf-8"))]
            + [SPECIAL_TOKENS["INST_END"]]
            + [SPECIAL_TOKENS["RESP_START"]]
        )

        output = generate_response(model, tokens, max_new_tokens=30, temperature=0.6)
        response_start = len(tokens)
        response_tokens = output[response_start:]
        response_bytes = bytes([t for t in response_tokens if t < 128])
        response_text = response_bytes.decode("utf-8", errors="replace")

        print(f"  Q: {instruction}")
        print(f"  A: {response_text[:80]}")
        print()
```

En un modelo pequeño con 8 ejemplos, las respuestas no serán significativas. Eso es esperado. Lo importante es la *estructura*: el modelo aprende a producir salida después del marcador de respuesta en lugar de continuar generando más instrucciones.

> En sólo 8 ejemplos de modelos de microtipo, la respuesta no tiene sentido. Esto es de esperado.

### Paso 6: Cuida el olvido catastrófico

Comparar la capacidad de predicción de los tokens siguientes del modelo antes y después de SFT. Si SFT daña las capacidades generales, la pérdida en el texto bruto aumentará.

> Comparar la capacidad de predicción de los SFT en el modelo anterior y posterior. Si los SFT pierden la capacidad de uso general, las pérdidas en el texto original aumentarán.

```python
def measure_forgetting(model, test_text, seq_len=64):
    tokens = np.array(list(test_text.encode("utf-8")[:512]))

    total_loss = 0.0
    num_windows = 0

    for start in range(0, len(tokens) - seq_len - 1, seq_len):
        input_ids = tokens[start:start + seq_len].reshape(1, -1)
        target_ids = tokens[start + 1:start + seq_len + 1].reshape(1, -1)

        logits = model.forward(input_ids)

        batch, s_len, vocab_size = logits.shape
        logits_flat = logits.reshape(-1, vocab_size)
        targets_flat = target_ids.reshape(-1)

        max_logits = logits_flat.max(axis=-1, keepdims=True)
        log_softmax = logits_flat - max_logits - np.log(
            np.exp(logits_flat - max_logits).sum(axis=-1, keepdims=True)
        )

        loss = -log_softmax[np.arange(len(targets_flat)), targets_flat].mean()
        total_loss += loss
        num_windows += 1

    return total_loss / max(num_windows, 1)
```

En el ajuste real, se rastrearía esta métrica durante todo el entrenamiento. Si la pérdida de texto bruto aumenta en más de 10-15%, su SFT es demasiado agresivo. Baja la tasa de aprendizaje o reduce el número de épocas.

> En la actualidad, debes seguir este indicador durante todo el proceso de entrenamiento. Si la pérdida de texto original aumenta más del 10-15%, significa que el SFT ha aumentado demasiado.

## Usalo con el marco de ejecución

### Demo de la línea de tuberías SFT completa

```python
if __name__ == "__main__":
    np.random.seed(42)

    test_text = """The transformer architecture processes sequences through self-attention.
Each layer applies multi-head attention followed by a feedforward network.
Residual connections and layer normalization stabilize deep networks.
The model learns to predict the next token given all previous tokens."""

    print("=" * 70)
    print("INSTRUCTION TUNING (SFT) DEMO")
    print("=" * 70)
    print()

    model = MiniGPT(
        vocab_size=256, embed_dim=128, num_heads=4,
        num_layers=4, max_seq_len=128, ff_dim=512
    )
    print(f"Model: {model.count_parameters():,} parameters")
    print(f"Config: 4 layers, 4 heads, 128 dims (mini GPT from Lesson 04)")
    print()

    print("PRE-SFT: Measuring base model loss on raw text")
    base_loss = measure_forgetting(model, test_text)
    print(f"  Base model loss: {base_loss:.4f}")
    print()

    print("=" * 70)
    print("SFT TRAINING")
    print("=" * 70)

    model, losses = sft_train(
        model, INSTRUCTION_DATA, num_epochs=3, lr=2e-5, seq_len=128
    )

    print()
    print("POST-SFT: Measuring fine-tuned model loss on raw text")
    sft_loss = measure_forgetting(model, test_text)
    print(f"  SFT model loss: {sft_loss:.4f}")
    print(f"  Change: {((sft_loss - base_loss) / base_loss * 100):+.1f}%")
    if abs(sft_loss - base_loss) / base_loss < 0.15:
        print("  Minimal forgetting (< 15% change)")
    else:
        print("  Significant forgetting detected")
    print()

    print("=" * 70)
    print("INSTRUCTION FOLLOWING EVALUATION")
    print("=" * 70)
    print()

    test_instructions = [
        "What is the capital of France?",
        "Name a programming language.",
        "Define gravity.",
    ]
    evaluate_instruction_following(model, test_instructions)

    print("=" * 70)
    print("DATA FORMAT EXAMPLES")
    print("=" * 70)
    print()

    for i, example in enumerate(INSTRUCTION_DATA[:3]):
        tokens = tokenize_instruction_pair(example["instruction"], example["response"])
        mask = create_loss_mask(tokens)
        resp_count = int(mask.sum())
        total_count = len(tokens)
        print(f"  Example {i + 1}: {total_count} tokens, {resp_count} response tokens ({resp_count/total_count:.0%} of sequence)")
        print(f"    Instruction: {example['instruction']}")
        print(f"    Response: {example['response']}")
        print()

    print("=" * 70)
    print("TRAINING LOSS CURVE")
    print("=" * 70)
    print()

    if losses:
        window = max(1, len(losses) // 5)
        for i in range(0, len(losses), window):
            chunk = losses[i:i + window]
            avg = sum(chunk) / len(chunk)
            print(f"  Steps {i:3d}-{i + len(chunk) - 1:3d}: avg loss = {avg:.4f}")
```

## Envíe el producto .

Esta lección produce`outputs/prompt-sft-data-curator.md`-- un prompt que le ayuda a diseñar y curar conjuntos de datos de instrucciones para SFT. Dado una capacidad objetivo (generación de código, matemáticas, conversación), produce un plan de recopilación de datos con especificaciones de formato, criterios de calidad y requisitos de diversidad.

## Los ejercicios.

1. Añadir soporte de sistema rápido. Modificar `tokenize_instruction_pair`Crear 5 ejemplos con diferentes instrucciones de sistema ("Eres un poeta", "Eres un tutor de matemáticas") y verificar que el modelo ve diferentes instrucciones de sistema durante el entrenamiento.

2. Implementar la mezcla de datos. Crear una función que toma un conjunto de datos SFT y un corpus de texto crudo, luego produce lotes de entrenamiento donde el 5% de los ejemplos son texto crudo (sin enmascaramiento) y el 95% son pares de instrucciones (mascarados). ejecutar 3 épocas y comparar métricas de olvido con el entrenamiento puro SFT.

3. Construir un puntuación de calidad de datos. Para cada par de instrucciones y respuestas, calcular: (a) longitud de respuesta en tokens, (b) relación instrucción-respuesta, (c) diversidad de vocabulario (tokens únicos / tokens totales). Filtrar ejemplos con longitud de respuesta < 10 tokens o diversidad < 0,3. Muestre cómo el filtrado afecta la pérdida final.

4. Implemente entrenamiento de conversación en múltiples vueltas. Extenda la tokenización para manejar conversaciones de 3 vueltas (usuario-asistente-usuario-asistente-usuario-asistente). La máscara de pérdida debe cubrir los tres vueltas de asistente. Verifique si la máscara es correcta imprimiendo la alineación de token-máscara para un ejemplo.

5. Compare las tasas de aprendizaje. Entrenar el mismo modelo tres veces con lr=1e-4, lr=2e-5, y lr=1e-6. trazar las curvas de pérdida. La carrera 1e-4 debe mostrar un descenso inicial rápido pero una pérdida final más alta (overfitting). La carrera 1e-6 apenas debe moverse. La carrera 2e-5 debe ser el punto dulce.

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| SFT | "Fine-tuning on conversations" | Supervised Fine-Tuning: continuing training on (instruction, response) pairs with loss computed only on response tokens | 监督微调，在指令-回复对上继续训练，仅对回复 token 计算损失 |
| Instruction tuning | "Teaching the model to follow instructions" | Training on explicit instruction-response pairs so the base model learns the conversation pattern, not new knowledge | 指令微调，训练基础模型学会对话模式而非新知识 |
| Loss masking | "Ignoring the prompt" | Setting loss to zero for instruction tokens so gradients only flow from response token predictions | 损失掩码，指令 token 损失设为零，梯度仅来自回复预测 |
| ChatML | "Chat Markup Language" | A token format using `<\|im_start\|>` and `<\|im_end\|>` delimiters to mark speaker roles in conversation data | 聊天标记语言，用特殊 token 标记对话角色 |
| Alpaca format | "Stanford's format" | A JSON format with instruction/input/output fields, used for 52K GPT-3.5-generated examples that cost $600 | Alpaca 格式，Stanford 的 JSON 指令格式，52K 样本成本 $600 |
| Catastrophic forgetting | "The model gets dumber" | Fine-tuning destroys pre-trained capabilities because gradient updates overwrite general knowledge with task-specific patterns | 灾难性遗忘，微调破坏预训练能力 |
| Weight tying | "Shared embeddings" | Using the same matrix for input token embeddings and output prediction head, saving parameters and improving coherence | 权重共享，输入输出共用嵌入矩阵 |
| Chat template | "How you format the prompt" | The specific token sequence (role markers, delimiters) that structures a conversation for the model | 聊天模板，格式化对话的 token 序列 |

## Más Leer más Leer más

- [Ouyang et al., 2022 -- "Training language models to follow instructions with human feedback" (InstructGPT)](https://arxiv.org/abs/2203.02155)-- el documento que introdujo el ajuste de instrucciones + RLHF en OpenAI
- [Taori et al., 2023 -- "Stanford Alpaca: An Instruction-following LLaMA Model"](https://github.com/tatsu-lab/stanford_alpaca)-- 52K ejemplos de instrucciones por $ 600, que demuestran que SFT funciona en pequeños conjuntos de datos
- [Touvron et al., 2023 -- "Llama 2: Open Foundation and Fine-Tuned Chat Models"](https://arxiv.org/abs/2307.09288)-- El oleoducto SFT + RLHF de Meta con ejemplos de alta calidad de 27K
- [Chiang et al., 2023 -- "Vicuna: An Open-Source Chatbot Impressing GPT-4"](https://lmsys.org/blog/2023-03-30-vicuna/)-- formación en 70K conversaciones ShareGPT
- [Zhou et al., 2023 -- "LIMA: Less Is More for Alignment"](https://arxiv.org/abs/2305.11206)-- demostrando que 1.000 ejemplos cuidadosamente seleccionados pueden coincidir con SFT en conjuntos de datos mucho más grandes
