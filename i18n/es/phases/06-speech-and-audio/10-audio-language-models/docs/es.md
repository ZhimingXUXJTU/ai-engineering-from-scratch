# Modelos de audio-idioma  Qwen2.5 Omni, Audio Flamingo, GPT-4o Audio 音频语言模型

> Los modelos de audio-idioma 2026 razonan sobre el habla + sonido ambiental + música. Qwen2.5-Omni-7B coincide con GPT-4o Audio en MMAU-Pro. Audio Flamingo Next supera a Gemini 2.5 Pro en LongAudioBench. La brecha entre abierto y cerrado es esencialmente cerrada  excepto en tareas de audio múltiples, donde todos son casi aleatorios.

> **【中文解读】**2026 años de audio频语言模型能理解语音+环境声+音乐──Qwen2.5-Omni-7B 在 MMAU-Pro 上匹配 GPT-4o Audio,Audio Flamingo Next 在 LongAudioBench 上超越 Gemini 2.5 Pro──开源与闭源的差距基本消失──

> **【拓展：音频大模型的新时代】**El modelo de lenguaje de audio ampliará la capacidad de pensamiento del LLM al ámbito de la voz, y podrá comprender al mismo tiempo el contenido de los idiomas, la identificación de los sonidos ambientales, el análisis de la estructura musical.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04 (ASR), Phase 12 · 03 (Vision-Language Models), Phase 7 · 10 (Audio Transformers) | **前置知识:** 阶段 6 · 04（ASR），阶段 12 · 03（视觉语言模型），阶段 7 · 10（音频 Transformer）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## El problema es la introducción del problema

Hay 5 segundos de audio: ladrones de perros, alguien grita "¡para!", luego silencio.

> Tienes 5 segundos de voz: perro grita, alguien grita "parar!", luego está quieto.

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

- **Transcription.**"Qué se dijo?"  Territorio de la RAS.
  **转录。**"¿Dice qué?" en el campo de la Asamblea General.
- **Semantic reasoning.**"¿Está la persona en peligro?"  requiere un entendimiento conjunto del ladrido + grito + silencio.
  **语义推理。**¿Este hombre es peligroso? Necesita un entendimiento conjunto.
- **Music reasoning.**"¿Qué instrumentos tocan la melodía?"
  **音乐推理。**"¿Qué instrumento toca la melodía?"
- **Long-audio retrieval.**"¿Dónde en esta conferencia de 90 minutos explicó el instructor la descensos de gradientes?"
  **长音频检索。**"En esta charla de 90 minutos, ¿dónde explicó el profesor la disminución del nivel?"

Un modelo único que responde a todos estos con un solo aviso es un **audio-language model**Separado de la ASR pura: los LALM producen respuestas de forma libre en lenguaje natural, no sólo transcripciones.

> Con un solo consejo, responder a todas estas preguntas es un único modelo.**音频语言模型**(LALM / ALM) ∼区别于纯 ASR:LALM 生成自由形式的自然语言答案, no sólo es un texto transcript.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![Audio-language model: audio encoder + projector + LLM decoder](../assets/alm-architecture.svg)

### La plantilla de tres componentes

Cada 2026 LALM tiene el mismo esqueleto:

> ### 3 componentes

> Cada LAM de 2026 tiene la misma estructura:

1. **Audio encoder.**Encodrador de susurros · BEATs · CLAP · WavLM · o un codificador personalizado por modelo.
   **音频编码器。**Los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de codificación de susurros, los sistemas de codificación de susurros, los sistemas de codificación de codificación de susurros, los sistemas de codificación de los sistemas de codificación de susurros, los sistemas de codificación de los sistemas de codificación de los sistemas de codificación de susurros, los sistemas de los sistemas de codificación de los sistemas de codificación de los sistemas de los sistemas de codificación de los sistemas de codificación de los sistemas de los sistemas de codificación de los sistemas de los sistemas de los sistemas de codificación de los sistemas de los sistemas de los sistemas de codificación de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de la información de control de la información de control de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la
2. **Projector.**Las funciones de audio-encoder de puente lineal o MLP en el espacio de incorporación de tokens del LLM.
   **投影器。**La tecnología de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de la grabación de grabación de la grabación de la grabación de grabación de la grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de grabación de gración de grabación de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración de gración
3. **LLM.**Descriptor basado en Llama / Qwen / Gemma. Toma texto entrelazado + tokens de audio; genera texto.
   **LLM。**基于 Llama / Qwen / Gemma 的解码器──接收交织的文本 + 音频代币;生成文本──

Formación:

> 训练:

- **Stage 1.**Encoder de congelación + LLM; proyector de tren sólo en datos de ASR / subtítulos.
  **阶段 1。**结编码器 + LLM; sólo en ASR/标注数据上训练投影器──
- **Stage 2.**La perfección de la función de audio (QA, razonamiento, comprensión de la música) que sigue las instrucciones.
  **阶段 2。**En instrucción seguir con la tarea de la audiencia (QA、推理、音乐理解) se realiza el total de los parámetros / LoRA 微调──
- **Stage 3 (optional).**El Voice-in / voice-out añade un decodificador de voz. Qwen2.5-Omni y AF3-Chat hacen esto.
  **阶段 3（可选）。**语音入/语音出添加语音解码器──Qwen2.5-Omni 和 AF3-Chat 实现了这一点──

### El mapa modelo de 2026

> ### Mapa del modelo de 2026

| Model | Backbone | Audio encoder | Output modality | Access |
|-------|----------|---------------|-----------------|--------|
| Qwen2.5-Omni-7B | Qwen2.5-7B | Custom + Whisper | text + speech | Apache-2.0 |
| Qwen3-Omni | Qwen3 | Custom | text + speech | Apache-2.0 |
| Audio Flamingo 3 | Qwen2 | AF-CLAP | text | NVIDIA non-commercial |
| Audio Flamingo Next | Qwen2 | AF-CLAP v2 | text | NVIDIA non-commercial |
| SALMONN | Vicuna | Whisper + BEATs | text | Apache-2.0 |
| LTU / LTU-AS | Llama | CAV-MAE | text | Apache-2.0 |
| GAMA | Llama | AST + Q-Former | text | Apache-2.0 |
| Gemini 2.5 Flash/Pro (closed) | Gemini | proprietary | text + speech | API |
| GPT-4o Audio (closed) | GPT-4o | proprietary | text + speech | API |

| 模型 | 骨干 | 音频编码器 | 输出模态 | 访问方式 |
|------|------|-----------|---------|---------|
| Qwen2.5-Omni-7B | Qwen2.5-7B | 自定义 + Whisper | 文本+语音 | Apache-2.0 |
| Qwen3-Omni | Qwen3 | 自定义 | 文本+语音 | Apache-2.0 |
| Audio Flamingo 3 | Qwen2 | AF-CLAP | 文本 | NVIDIA 非商业 |
| Audio Flamingo Next | Qwen2 | AF-CLAP v2 | 文本 | NVIDIA 非商业 |
| SALMONN | Vicuna | Whisper + BEATs | 文本 | Apache-2.0 |
| LTU / LTU-AS | Llama | CAV-MAE | 文本 | Apache-2.0 |
| GAMA | Llama | AST + Q-Former | 文本 | Apache-2.0 |
| Gemini 2.5 Flash/Pro（闭源） | Gemini | 专有 | 文本+语音 | API |
| GPT-4o Audio（闭源） | GPT-4o | 专有 | 文本+语音 | API |

### Verificación de realidad de referencia (2026)

**MMAU-Pro.**1800 pares de calidad que cubren voz / sonido / música / mezclado.

| Model | Overall | Speech | Sound | Music | Multi-audio |
|-------|---------|--------|-------|-------|-------------|
| Gemini 2.5 Pro | ~60% | 73.4% | 51.9% | 64.9% | ~22% |
| Gemini 2.5 Flash | ~57% | 73.4% | 50.5% | 64.9% | 21.2% |
| GPT-4o Audio | 52.5% | — | — | — | 26.5% |
| Qwen2.5-Omni-7B | 52.2% | 57.4% | 47.6% | 61.5% | ~20% |
| Audio Flamingo 3 | ~54% | — | — | — | — |
| Audio Flamingo Next | SOTA on LongAudioBench | — | — | — | — |

El **multi-audio column is damning for everyone.**La probabilidad aleatoria en la opción de 4 opciones = 25%; la mayoría de los modelos obtienen un puntaje alrededor de ahí.

> **多音频列对所有人都是致命的。**4 選 1 多選題的隨機概率 = 25%; la mayoría de los modelos obtienen puntos en la zona.

### Donde los LALM son útiles en 2026

- **Compliance audit of call-center recordings.**"¿El agente mencionó la divulgación requerida?"
  **合规审计通话录音。**"¿El cliente ha mencionado la declaración de responsabilidad necesaria?"
- **Accessibility.**Describa los eventos sonoros a los usuarios sordos (no sólo la transcripción).
  **无障碍。**Por lo que el usuario describe el evento de voz (((no sólo se transcribe)
- **Content moderation.**Detectar lenguaje violento + tono amenazante + contexto de fondo.
  **内容审核。**检测暴力语言 + 威胁语气 + 背景上下文──
- **Podcast / meeting chaptering.**Resumen semántico, no sólo los giros del orador.
  **播客/会议章节化。**语义摘要, no sólo habla de la gente en su turno.
- **Music catalog analysis.**"Encuentra todas las pistas con un cambio de llave de sección B".
  **音乐目录分析。**"Encuentra todos los temas que han cambiado".

### Cuando no son (todavía) útiles

- Teoría de la música de granos finos (por debajo del nivel de acordes).
  精细音乐理论(和弦级别以下)
- Razonamiento atribuido por el orador durante largas conversaciones (grados pasados 10 minutos).
  长对话中的说话人归因推理 (más de 10 minutos de retrocesión)
- Comparación de audio múltiple (22-26% es apenas más que aleatorio).
  Más de un 22-26%  casi igual a las veces)
- Razonamiento en tiempo real de transmisión (la mayoría son inferencias de lotes fuera de línea).
  实时流式推理 (la mayoría son las propuestas de venta en línea)

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.




## Construye y realiza.
```figure
v4-alm-tokens
```

## Construye el mismo

### Paso 1: consulta Qwen2.5-Omni

```python
from transformers import AutoModelForCausalLM, AutoProcessor

processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-Omni-7B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-Omni-7B", torch_dtype="auto")

audio, sr = load_wav("clip.wav", sr=16000)
messages = [{
    "role": "user",
    "content": [
        {"type": "audio", "audio": audio},
        {"type": "text", "text": "What sounds do you hear, and what's happening?"},
    ],
}]
inputs = processor.apply_chat_template(messages, tokenize=True, return_tensors="pt")
output = model.generate(**inputs, max_new_tokens=200)
print(processor.decode(output[0], skip_special_tokens=True))
```

### Paso 2: el patrón del proyector

```python
import torch.nn as nn

class AudioProjector(nn.Module):
    def __init__(self, audio_dim=1280, llm_dim=4096):
        super().__init__()
        self.down = nn.Linear(audio_dim, llm_dim)
        self.act = nn.GELU()
        self.up = nn.Linear(llm_dim, llm_dim)

    def forward(self, audio_features):
        return self.up(self.act(self.down(audio_features)))
```

El proyector es generalmente de 1-3 capas lineales. Entrenarlo en pares ASR (audio → transcripción) es la tarea de pretexto de la etapa 1.

### Paso 3: evaluación comparativa de MMAU / LongAudioBench

```python
from datasets import load_dataset
mmau = load_dataset("MMAU/MMAU-Pro")

correct = 0
for item in mmau["test"]:
    answer = call_model(item["audio"], item["question"], item["choices"])
    if answer == item["correct_choice"]:
        correct += 1
print(f"Accuracy: {correct / len(mmau['test']):.3f}")
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


Informar por categoría (habla / sonido / música / multi-audio) por separado.




> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

| Task | 2026 pick |
|------|-----------|
| Free-form audio QA (open) | Qwen2.5-Omni-7B |
| Best open on long audio | Audio Flamingo Next |
| Best closed | Gemini 2.5 Pro |
| Voice-in / voice-out agent | Qwen2.5-Omni or GPT-4o Audio |
| Music reasoning | Audio Flamingo 3 or 2 (music-specialized AF-CLAP) |
| Call-center audit | Gemini 2.5 Pro via API, with RAG over your policy docs |

| 任务 | 2026 年选择 |
|------|-----------|
| 自由格式音频 QA（开源） | Qwen2.5-Omni-7B |
| 最佳开源长音频 | Audio Flamingo Next |
| 最佳闭源 | Gemini 2.5 Pro |
| 语音入/语音出智能体 | Qwen2.5-Omni 或 GPT-4o Audio |
| 音乐推理 | Audio Flamingo 3 或 2（音乐专用 AF-CLAP） |
| 呼叫中心审计 | Gemini 2.5 Pro via API，配合策略文档 RAG |



## Las trampas

> 常见陷

- **Over-trust on multi-audio.**Si su tarea necesita "cuál clip tiene X", el rendimiento al azar es real.
  **过度信任多音频。**Si tu tarea necesita "qual es el segmento con X", el rendimiento horizontal es real.
- **Long-audio degradation.**Después de 10 minutos, la mayoría de los modelos rompen la atribución de altavoces.
  **长音频退化。**超过 10 分钟, la mayoría de los modelos de la palabra 归因失效──先做日志化 (第 6 课),再总结──
- **Hallucinations on silence.**El mismo problema de estilo Whisper heredado por los LALM que usan el codificador Whisper.
  **静音上的幻觉。**El problema de susurros es el mismo que el problema de susurros de los editores de Whisper.
- **Benchmark cherry-picking.**Las publicaciones de los vendedores en el blog destacan las categorías de mejor caso. ejecutar el subconjunto multi-audio MMAU-Pro usted mismo.
  **基准挑挑拣拣。**供应商博客文章突出最佳类别──自运行 MMAU-Pro 多音频子集──

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-alm-picker.md`. Seleccione LALM + subconjunto de referencia + modalidad de salida (texto vs habla) para una tarea de comprensión de audio dada.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-alm-picker.md`◊ para un determinado audio frecuencia de comprensión de tareas seleccionar LALM + 基准子集 + 输出模态(文本 vs 语音) ◊

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`para ver un patrón de proyector de juguete + falso enrutamiento LALM de (audio-embedado, tokens de texto) → tokens de salida.
   **简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`查看玩具投影器模式 + 假 LALM 路由(音频嵌入,文本代币)→ 输出代币──
2. **Medium.**Ponte Qwen2.5-Omni-7B en 100 artículos de habla MMAU-Pro. Comparar con el número reportado del periódico.
   **中等。**En 100 MMAU-Pro 语音项评分 Qwen2.5-Omni-7B──与论文报告的数字比较──
3. **Hard.**Construir una línea de base de audio de capción mínima: BEATs codificador + proyector de 2 capas + congelado Llama-3.2-1B. Fine-tune sólo el proyector en AudioCaps. Comparar con SALMONN en Clotho-AQA.
   **困难。**构建最小音频标注基线:BEATs 编码器 + 2层投影器 + 结 Llama-3.2-1B──仅在AudioCaps 上微调投影器──在Clotho-AQA 上与SALMONN比较──

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| LALM | Audio ChatGPT | Audio encoder + projector + LLM decoder. |
| Projector | Adapter | Small MLP mapping audio features into LLM embedding space. |
| MMAU | The benchmark | 10k audio-QA pairs across speech, sound, music. |
| MMAU-Pro | Harder MMAU | 1800 multi-audio / reasoning-heavy questions. |
| LongAudioBench | Long-form eval | Multi-minute clips with semantic queries. |
| Voice-in / voice-out | Speech-native | Model ingests speech and emits speech without text detour. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| LALM | 音频 ChatGPT | 音频编码器 + 投影器 + LLM 解码器。 |
| 投影器 | 适配器 | 将音频特征映射到 LLM 嵌入空间的小型 MLP。 |
| MMAU | 那个基准 | 跨语音、声音、音乐的 1 万音频-QA 对。 |
| MMAU-Pro | 更难的 MMAU | 1800 个多音频/重推理问题。 |
| LongAudioBench | 长音频评估 | 带语义查询的多分钟片段。 |
| 语音入/语音出 | 原生语音 | 模型直接接收和输出语音，不经文本。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Chu et al. (2024). Qwen2-Audio](https://arxiv.org/abs/2407.10759) arquitectura de referencia.
  Chu 等 (2024). Qwen2-Audio 参考架构──
- [Alibaba (2025). Qwen2.5-Omni](https://huggingface.co/Qwen/Qwen2.5-Omni-7B) hablar en hablar.
  Alibaba (2025). Qwen2.5-Omni语音入语音出。
- [NVIDIA (2025). Audio Flamingo 3](https://arxiv.org/abs/2507.08128) el líder de audio largo abierto.
  NVIDIA (2025). Audio Flamingo 3开源长音频领先者
- [NVIDIA (2026). Audio Flamingo Next](https://arxiv.org/abs/2604.10905) LongAudioBench SOTA.
  NVIDIA (2026). Audio Flamingo SiguienteLongAudioBench SOTA──
- [Tang et al. (2023). SALMONN](https://arxiv.org/abs/2310.13289)Pionero en el doble codificación.
  Tang 等 (2023). SALMONN双编码器先驱──
- [MMAU-Pro leaderboard](https://mmaubenchmark.github.io/) ranking en vivo de 2026.
  MMAU-Pro 排行榜 2026 年实时排名──

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

