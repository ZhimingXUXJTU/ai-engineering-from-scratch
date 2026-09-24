# La generación de música  MusicGen, Audio estable, Suno, y el terremoto de licencia  音乐生成  MusicGen、Stable Audio、Suno y derechos de terremoto

> 2026 generación de música: Suno v5 y Udio v4 dominan comercial; MusicGen, Stable Audio Open y ACE-Step lideran el código abierto. El problema técnico se resuelve en su mayoría. El problema legal (Warner Music $ 500M acuerdo, UMG acuerdo) remodela el campo en 2025-2026.

> **【中文解读】**2026 años de música generación:Suno v5 y Udio v4 主导商业产品;MusicGen、Stable Audio Open 和 ACE-Step 领先开源;; problemas técnicos básicos resueltos, pero problemas de ley(Warner Music 5 mil millones de dólares y acuerdo) en 2025-2026 años reformula esta área;;

> **【拓展：AI 音乐的法律风暴】**El problema de derechos de autor de la música de AI produce un terremoto en la industria de la música. ¿Constituye el derecho de autor de la música en los datos de entrenamiento? ¿A quién pertenece el derecho de autor de la música de AI de la música de AI?

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 4 · 10 (Diffusion Models) | **前置知识:** 阶段 6 · 02（频谱图），阶段 4 · 10（扩散模型）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## El problema es la introducción del problema

Text → un clip musical de 30 segundos a 4 minutos, con letras, voces y estructura.

> 文本 → 30 segundos a 4 minutos de música,带歌词、人声和结构──三子问题:

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

1. **Instrumental generation.**Texto como "batería de hip-hop lo-fi con teclas calientes" → audio. MusicGen, Audio Stable, AudioLDM.
   **器乐生成。**Como "batería de hip-hop lo-fi con teclas calientes" así de texto → 音频──MusicGen、Stable Audio、AudioLDM──
2. **Song generation (with vocals + lyrics).**"Canción country sobre las noches lluviosas de Texas" → canción completa.
   **歌曲生成（带人声+歌词）。**"Cantada de país sobre las noches lluviosas de Texas" → 完整歌曲──Suno、Udio、YuE、ACE-Step──
3. **Conditional / controllable.**Extender un clip existente, regenerar un puente, cambiar género, separar el tallo o pintar.
   **条件/可控生成。**扩展现有片段、重新生成桥段、切换风格、分轨或内画──Udio de interior画 + 分轨 es la función que debe alcanzar en 2026 años──

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![Music generation: token-LM vs diffusion, the 2026 model map](../assets/music-generation.svg)

### Token LM sobre los tokens de codec neuronal

> ### Token LM basado en el código de código

Meta's **MusicGen**(2023, MIT) y muchos derivados: condición en las incorporaciones de texto/melodía, predecir autoregresivamente tokens EnCodec (32 kHz, 4 libros de código), decodificar con EnCodec. 300M - 3.3B parámetros.

> Meta de **MusicGen**(2023, MIT) y muchas derivadas: en texto /旋律嵌入为条件, auto-regreso预测 EnCodec token(32 kHz,4 个码本), con EnCodec 解码──3 亿到33 亿参数──强基线; más de 30 秒效果下降──

**ACE-Step**(open source, 4B XL lanzado en abril de 2026) extiende esto a la generación de canciones completas con letra.

> **ACE-Step**(Open Source, 4 de abril de 2026) se extenderá a la producción de todo el mundo.

### Difusión sobre fundimientos o latencias

> ### basado en la expansión de la variabilidad mel/potencial

**Stable Audio (2023)**y **Stable Audio Open (2024)**La difusión latente en audio comprimido. Excelente en circuitos, diseño de sonido, texturas ambientales. No es excelente en canciones completas estructuradas.

> **Stable Audio（2023）**Y **Stable Audio Open（2024）**La música de la canción es muy buena en su estructura.

**AudioLDM / AudioLDM2**: texto a audio a través de la difusión latente de estilo T2I, generalizada a la música, efectos sonoros, habla.

> **AudioLDM / AudioLDM2**A través de T2I 风格的潜变量扩散进行文本到音频生成,泛化到音乐、音效、语音──

### Hybrid (producción)  Suno, Udio, Lyria

> ### 混合(生产)  Suno、Udio、Lyria

Peso cerrado. Probablemente un códec AR LM + vocoder basado en difusión con cabezas de voz / batería / melodía especializadas. Suno v5 (2026) es el líder de calidad de ELO 1293. Udio v4 añade inpainting + separación de tronco (bajo, batería, vocales descargas separadas).

> 闭源权重──可能是 AR 编解码 LM + 基于扩散的声码器,配有专门语音/鼓/旋律头──Suno v5(2026) es ELO 1293 质量领先者──Udio v4 增加内画 + 分轨(贝斯、鼓、人声分别下载)──

### Evaluación

> ###  evaluación

- **FAD (Fréchet Audio Distance).**Distancia de nivel de incorporación entre la distribución de audio generada y la real utilizando funciones VGGish o PANNs. Más bajo es mejor. MusicGen pequeño: 4.5 FAD en MusicCaps; SOTA ~ 3.0.
  **FAD（Fréchet 音频距离）。**Utiliza VGGish o PANNs Tr征的生成对真实音频分布的嵌入级距离──越低越好──MusicGen pequeño:MusicCaps 上 4.5 FAD;SOTA 约 3.0──
- **Musicality (subjective).**La preferencia humana. Suno v5 ELO 1293 conduce.
  **音乐性（主观）。**El hombre está en el camino.
- **Text-audio alignment.**CLAP puntaje entre la respuesta y la salida.
  **文本-音频对齐。**提示与输出之间的 CLAP 分数──
- **Musicality artifacts.**Transiciones fuera de ritmo, deriva de la frase vocal, pérdida de estructura después de 30 segundos.
  **音乐性伪影。**跑拍过渡、人声短语漂移、 más de 30 segundos después de la pérdida de la estructura。

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.



## Mapa modelo 2026

> Mapa del modelo de 2026

| Model | Params | Length | Vocals | License |
|-------|--------|--------|--------|---------|
| MusicGen-large | 3.3B | 30 s | no | MIT |
| Stable Audio Open | 1.2B | 47 s | no | Stability non-commercial |
| ACE-Step XL (Apr 2026) | 4B | > 2 min | yes | Apache-2.0 |
| YuE | 7B | > 2 min | yes, multilingual | Apache-2.0 |
| Suno v5 (closed) | ? | 4 min | yes, ELO 1293 | commercial |
| Udio v4 (closed) | ? | 4 min | yes + stems | commercial |
| Google Lyria 3 (closed) | ? | real-time | yes | commercial |
| MiniMax Music 2.5 | ? | 4 min | yes | commercial API |

| 模型 | 参数量 | 时长 | 人声 | 许可 |
|------|--------|------|------|------|
| MusicGen-large | 33 亿 | 30 秒 | 无 | MIT |
| Stable Audio Open | 12 亿 | 47 秒 | 无 | Stability 非商业 |
| ACE-Step XL（2026.04） | 40 亿 | > 2 分钟 | 有 | Apache-2.0 |
| YuE | 70 亿 | > 2 分钟 | 有，多语言 | Apache-2.0 |
| Suno v5（闭源） | ? | 4 分钟 | 有，ELO 1293 | 商业 |
| Udio v4（闭源） | ? | 4 分钟 | 有 + 分轨 | 商业 |
| Google Lyria 3（闭源） | ? | 实时 | 有 | 商业 |
| MiniMax Music 2.5 | ? | 4 分钟 | 有 | 商业 API |

## El panorama legal (2025-2026)

> ## 法律环境(2025-2026)

- **Warner Music vs Suno settlement.**$500M. WMG ahora tiene supervisión de la similitud de IA, derechos de música y pistas generadas por el usuario en Suno.
  **Warner Music 诉 Suno 和解。**500 millones de dólares. WMG ahora tiene el control de la similaridad de la IA de Suno, derechos de autor y contenido de generación de usuarios.
- **EU AI Act**¿ Qué es eso ?**California SB 942**: La música generada por IA debe ser revelada.
  **EU AI 法案**¿ Qué es eso ?**加利福尼亚 SB 942**La música que se produce debe ser revelada.
- **Riffusion / MusicGen**En el MIT no tienen equipaje de cumplimiento pero tampoco voces comerciales.
  **Riffusion / MusicGen**En MIT no hay ninguna carga de acuerdo con la normativa, pero tampoco hay voz de empresario.

Modelos de seguridad para el buque:

> Modelo de seguridad:

1. Generar sólo instrumental (MusicGen, Stable Audio Open, MIT/CC0 salidas).
   仅生成器乐(MusicGen、Stable Audio Open、MIT/CC0 输出)
2. Utilice APIs comerciales (Suno, Udio, ElevenLabs Music) con licencia por generación.
   Utiliza con cada vez que se produce permiso de API comercial (Suno, Audio, ElevenLabs Music)
3. El tren en catálogo de propiedad o con licencia (la mayoría de las empresas terminan aquí).
   En el catálogo de auto-o autorizados entrenamiento (la mayoría de las empresas finalmente llegan a este paso)
4. Etiquetar generaciones con marcas de agua + metadatos.
   Usado para imprimir datos y obtener contenido.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.


## Construye y realiza.
```figure
sp-codec-tokens
```

## Construye el mismo

### Paso 1: genera con MusicGen

```python
from audiocraft.models import MusicGen
import torchaudio

model = MusicGen.get_pretrained("facebook/musicgen-small")
model.set_generation_params(duration=10)
wav = model.generate(["upbeat synthwave with driving drums, 128 BPM"])
torchaudio.save("out.wav", wav[0].cpu(), 32000)
```

Tres tamaños: `small`(300M, rápido),`medium`(1.5B), `large`(3.3B) Lo pequeño es suficiente para "hace que la idea aterrice".

> Tres grandes:`small`(Millones, rápido)`medium`(15 mil millones)`large`(33 mil millones)`small`足以验证"¿¿la idea es posible?"

### Paso 2: Condicionamiento de la melodía

```python
melody, sr = torchaudio.load("humming.wav")
wav = model.generate_with_chroma(
    ["jazz piano cover"],
    melody.squeeze(),
    sr,
)
```

MusicGen-melody toma un cromagrama y conserva la melodía mientras cambia de timbre.

> MúsicaGen-melodia  acepta la nota y cambia la voz cuando se conserva la melodía.

### Paso 3: Evaluación del FAD

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()

fad.get_fad_score("generated_folder/", "reference_folder/")
```

Computa distancia de incorporación VGGish. Útil para pruebas de regresión a nivel de género; no es un sustituto para los oyentes humanos.

> 計算 VGGish 嵌入距離── se aplica a la prueba de regreso de clase de la corriente; no puede sustituir a la audiencia humana──

### Paso 4: añadir al flujo de trabajo de LLM-música

Combina con las ideas de las lecciones 7-8:

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


```python
prompt = "Write a 30-second jazz loop. Describe the drums, bass, and piano voicing."
description = llm.complete(prompt)
music = musicgen.generate([description], duration=30)
```




> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

| Goal | Stack |
|------|-------|
| Instrumental sound design | Stable Audio Open |
| Game / adaptive music | Google Lyria RealTime (closed) |
| Full songs with vocals (commercial) | Suno v5 or Udio v4 with explicit license |
| Full songs with vocals (open) | ACE-Step XL or YuE |
| Short ad jingle | MusicGen melody-conditioned on a hummed reference |
| Music-video background | MusicGen + Stable Video Diffusion |

| 目标 | 技术栈 |
|------|--------|
| 器乐声音设计 | Stable Audio Open |
| 游戏/自适应音乐 | Google Lyria RealTime（闭源） |
| 带人声的完整歌曲（商业） | Suno v5 或 Udio v4 带明确许可 |
| 带人声的完整歌曲（开源） | ACE-Step XL 或 YuE |
| 短广告曲 | MusicGen 在哼唱参考上的旋律条件 |
| 音乐视频背景 | MusicGen + Stable Video Diffusion |



## Las trampas que todavía se envían en 2026

> 2026 año todavía en la trampa de los culpables

- **Copyright-laundering prompts.**"Cantando al estilo de Taylor Swift"  comercial Suno / Audio filtro estos ahora, modelos abiertos no. Agregue su propia lista de filtros.
  **版权洗钱提示。**"Cantando al estilo de Taylor Swift" Comercio Suno/Udio 现在会过这些,开源模型不会──添加你自己的过列表──
- **Repetition / drift past 30 s.**Modelos de AR en bucle. Crossfade múltiples generaciones, o usar ACE-Step para la coherencia estructural.
  **超过 30 秒的重复/漂移。**AR 模型会循环──交叉淡进多个生成,或使用 ACE-Step 保持结构一致性──
- **Tempo drift.**Los modelos se alejan del BPM. Utilice las etiquetas BPM en el prompt y post-filter con librosa's `beat_track`¿ Qué ?
  **节奏漂移。**模型偏离 BPM──在提示中使用 BPM 标签并使用图书馆的 `beat_track`Después de todo.
- **Vocal intelligibility.**El Suno es excelente; los modelos abiertos a menudo son suaves en palabras.
  **人声清晰度。**Suno 表现出色; open source模型的歌词经常模糊──如果歌词重要,使用商业API或微调──
- **Mono output.**Los modelos abiertos generan estereo mono o falso.
  **单声道输出。**Open source model generar una sola voz o una falsa voz.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-music-designer.md`. Seleccionar el modelo, la estrategia de licencia, el plan de longitud / estructura y los metadatos de divulgación para una implementación de la generación musical.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-music-designer.md` para la producción de música, la implementación de modelos de selección, la estrategia de autorización, la duración/plan de estructura y la presentación de datos.

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Produce una progresión de acordes "generacional" + patrón de tambor como símbolos ASCII  una caricatura de la generación musical.
   **简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`◊ se realiza con símbolos ASCII generando "generación" y cuerda + 鼓点一个音乐生成的卡通── se puede reproducir con un colorador MIDI──
2. **Medium.**Instalar`audiocraft`, generar clips de 10 segundos en 4 generaciones con MusicGen-small, medir FAD contra un conjunto de géneros de referencia.
   **中等。**Instalación`audiocraft`, con MusicGen-small en 4 流派提示上生成10秒片段,对照参考流派集测量 FAD──
3. **Hard.**Utilizando ACE-Step (o MusicGen-melody), genera tres variaciones de la misma melodía con diferentes instrucciones de timbre.
   **困难。**Utilización de ACE-Step (o MusicGen-melodia), con diferentes sonidos de la música, para generar tres variaciones de la misma melodía.

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| FAD | Audio FID | Fréchet distance between embedding distributions of real vs generated. |
| Chromagram | Melody as pitches | 12-dim per-frame vector; input to melody conditioning. |
| Stems | Instrument tracks | Separated bass / drums / vocals / melody as WAV. |
| Inpainting | Regen a section | Mask a time window; model regenerates just that. |
| CLAP | Text-audio CLIP | Contrastive audio-text embedding; eval text-audio alignment. |
| EnCodec | Music codec | Meta's neural codec used by MusicGen; 32 kHz, 4 codebooks. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| FAD | 音频 FID | 真实 vs 生成嵌入分布之间的 Fréchet 距离。 |
| 色度图 | 旋律即音高 | 12 维逐帧向量；旋律条件的输入。 |
| 分轨 | 乐器轨道 | 分离的贝斯/鼓/人声/旋律 WAV。 |
| 内画 | 重生成一段 | 遮蔽时间窗口；模型只重生成那部分。 |
| CLAP | 文本-音频 CLIP | 对比音频-文本嵌入；评估文本-音频对齐。 |
| EnCodec | 音乐编解码器 | Meta 的神经编解码器，MusicGen 使用；32 kHz，4 个码本。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Copet et al. (2023). MusicGen](https://arxiv.org/abs/2306.05284) el índice de referencia autorregresor abierto.
  Copet等 (2023). MusicGen开源自归基准──
- [Evans et al. (2024). Stable Audio Open](https://arxiv.org/abs/2407.14358) el diseño de sonido por defecto.
  Evans 等 (2024). Estatal Audio Open声音设计默认选择──
- [ACE-Step](https://github.com/ace-step/ACE-Step) generador de 4B de canciones completas abierto, abril 2026.
  ACE-Step开源 40 亿参数全曲生成器,2026 年 4 月。
- [Suno v5 platform docs](https://suno.com) el líder en calidad comercial.
  Suno v5 商业质量领先者──
- [AudioLDM2](https://arxiv.org/abs/2308.05734) difusión latente para la música + efectos sonoros.
  AudioLDM2音乐 + 音效的潜变量扩散──
- [WMG-Suno settlement coverage](https://www.musicbusinessworldwide.com/suno-warner-music-settlement/) Novembre 2025 precedente.
  WMG-Suno 和解报道2025 年 11 月判例──

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

