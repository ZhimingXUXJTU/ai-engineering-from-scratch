# Voz Antifamación y marcado de agua de audio  ASVspoof 5, AudioSeal, WaveVerify 语音防伪与音频水印

> El clonamiento de voz se envió más rápido que las defensas. En 2026 los sistemas de voz de producción necesitan dos cosas: un detector (AASIST, RawNet2) que clasifique el habla real vs falsa, y una marca de agua (AudioSeal) que sobreviva a la compresión y edición.

> **【中文解读】**语音克隆技术跑在防防前面──2026年生产级语音系统需要两样东西:检测器(AASIST、RawNet2)区分真假语音,水印(AudioSeal) aún puede sobrevivir después de comprimir y editar──no hacer estos dos cosas no es necesario en línea语音克隆功能──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 06 (Speaker Recognition), Phase 6 · 08 (Voice Cloning) | **前置知识:** 阶段 6 · 06（说话人识别），阶段 6 · 08（语音克隆）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## El problema es la introducción del problema

Tres defensas relacionadas:

> Tres tipos de medios de defensa:

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.


1. **Anti-spoofing / deepfake detection.**Dado un clip de audio, ¿es sintético o real? Los puntos de referencia ASVspoof (ASVspoof 2019 → 2021 → 5) son el estándar de oro.
   En inglés:**反欺骗/深度伪造检测。**给定一段音频, juzgar si es sintético o real?ASVspoof 基准测试(ASVspoof 2019 → 2021 → 5) es el estándar de oro。
2. **Audio watermarking.**Embed una señal imperceptible en el audio generado que un detector puede extraer más tarde. AudioSeal (Meta) y WavMark son las opciones abiertas.
   En inglés:**音频水印。**En el generado de sonido se enchuflan señales insensibles, después de un inspector puede extraer.
3. **Authenticated provenance.**Firmar criptográficamente archivos de audio + metadatos. Iniciativa de autenticidad de contenido.
   En inglés:**认证来源。**音频文件 + 元数据的加密签名──C2PA / 内容真实性倡议──

La detección maneja a los adversarios que no cooperan. Watermarking maneja el cumplimiento.

> 检测应对不配合的攻击者──水印应对合规性AI 生成的音频应被识别──2026 años son los dos necesarios──

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![Anti-spoofing vs watermarking vs provenance — three defense layers](../assets/spoofing-watermark.svg)

### ASVspoof 5  el índice de referencia 2024-2025

> ASVspoof 5  2024-2025 年基准测试

El mayor cambio de las ediciones anteriores:

> El mayor cambio en comparación con la versión anterior:

- **Crowdsourced data**No está limpio.
  En inglés:**众包数据**(No está en el registro)
- **~2000 speakers**(vs ~ 100 antes).
  En inglés:**约 2000 名说话人**(Behere ca 100 名)
- **32 attack algorithms.**TTS + conversión de voz + perturbación adversaria.
  En inglés:**32 种攻击算法。**TTS + 语音转换 + 对抗性扰动──
- **Two tracks.**Contramedida (CM) detección independiente; ASV (SASV) de seguridad para sistemas biométricos.
  En inglés:**两个赛道。**La Comisión Europea ha aprobado el proyecto de ley de la Unión Europea (UE) de la Unión Europea (UE) de la Unión Europea (UE) de la que se trata.

El estado de la técnica en ASVspoof 5: ~ 7.23% EER. En el ASVspoof más viejo 2019 LA: 0.42% EER. Despliegue en el mundo real: espere 5-10% EER en clips en el medio ambiente.

> ASVspoof 5 上的 SOTA: aproximadamente 7.23% EER──在较旧 ASVspoof 2019 LA 上:0.42% EER──实际部署:预期在野外音频上 EER为 5-10%──

### Famílias de modelos de detección de AASIST y RawNet2 

> AASIST y RawNet2  检测模型家族

**AASIST**(en el caso de los Estados Unidos, el número de Estados miembros que han adoptado las medidas de contraposición es de 2021 a 2026).

> **AASIST**Las medidas de prevención y prevención de la contaminación por el VIH/SIDA se aplican en el sistema de prevención y prevención de enfermedades y enfermedades.

**RawNet2.**Convolución delantera sobre la forma de onda bruta + espina dorsal TDNN. Línea de base más simple; todavía competitivo con ajuste fino.

> **RawNet2。**La red de la base de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de

**NeXt-TDNN + SSL features.**Variante 2025: ECAPA-style + WavLM características + pérdida focal. Lleva el 0,42% EER en ASVspoof 2019 LA.

> **NeXt-TDNN + SSL 特征。**2025 年变体:ECAPA 风格 + WavLM 特征 + focal loss──在 ASVspoof 2019 LA 上达到0.42% EER──

### AudioSeal  el 2024 marca de agua por defecto

> AudioSeal  2024 años de agua

Meta's **AudioSeal**(Jan 2024, v0.2 de diciembre de 2024).

> Meta de **AudioSeal**(2024 年 1 月,v0.2 于 2024 年 12 月) ⋅

- **Localized.**Detecta la marca de agua por fotograma a 16 kHz (1/16000 s) de resolución de muestra.
  En inglés:**局部化。**Es decir, el tiempo de la prueba de agua es de 16 kHz.
- **Generator + detector jointly trained.**El generador aprende a incorporar una señal inaudible; el detector aprende a encontrarla a través de aumentos.
  En inglés:**生成器 + 检测器联合训练。**El aprendizaje de los detectores se puede ver en el sistema de detección de señales de detección.
- **Robust.**Sobrevive a la compresión MP3 / AAC, EQ, cambio de velocidad ±10%, mezcla de ruido +10 dB SNR.
  En inglés:**鲁棒。**能经受 MP3/AAC 压缩,均衡, ±10% 变速, +10 dB SNR 噪声混合,
- **Fast.**El detector funciona en tiempo real 485 veces; 1000 veces más rápido que WavMark.
  En inglés:**快速。**El detector funciona a 485 veces la velocidad real; comparable a WavMark 快 1000 veces.
- **Capacity.**Carga útil de 16 bits (puede codificar el ID del modelo, timestamp de generación, ID del usuario) incrustable en cada declaración.
  En inglés:**容量。**16 位载荷(可编码模型 ID、生成时间、用户 ID) puede ser emplazado en cada段语音──

### WavMark

La línea de base de apertura pre-AudioSeal. red neuronal invertible, 32 bits/sec. Problemas:

> AudioSeal 之前的开源基线──可逆神经网络,32 位/秒──问题:

- La sincronización de la fuerza bruta es lenta.
  Sin embargo, el gobierno de China no ha permitido que la violencia se desvanezca.
- Puede ser eliminado por ruido gaussiano o compresión MP3.
  China 翻译:可被高斯噪声或 MP3 压缩删除──
- No es amigable en tiempo real.
  En español: no se adapta a la realidad.

### WaveVerify (julio 2025)

Adresa las debilidades de AudioSeal  específicamente manipulaciones temporales (inversión, velocidad). Utiliza generador basado en FiLM + detector de mezcla de expertos. Competitivo con AudioSeal en ataques estándar; maneja modificaciones temporales.

> WaveVerify(2025年7月) ―― resolver las debilidades de AudioSeal 特别是时间操作(反转、变速) ―― utilizar basado en FiLM 的生成器 + MoE 检测器──在标准攻击上与 AudioSeal 相当;能处理时间编辑──

### Los adversarios explotan la brecha

De AudioMarkBench: "bajo cambio de tono, todas las marcas de agua muestran la precisión de recuperación de bits por debajo de 0.6, lo que indica una eliminación casi completa". **Pitch-shift is the universal attack.**No 2026 marca de agua es totalmente robusta para la modificación agresiva de tono.

> Leave a comment on the error of the attackers utilization: : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : **音高偏移是通用攻击。**没有任何2026年水印能完全抵御激进的音高修改──这就是为什么你需要检测(AASIST)与水印配合使用──

### C2PA / Iniciativa de autenticidad de contenidos

No es una técnica de ML  un formato manifiesto. Los archivos de audio contienen metadatos firmados criptográficamente sobre la herramienta de creación, autor, fecha. Audobox / Seamless lo utiliza.

> C2PA / 内容真实性倡议──不是机器学习技术 es un formato claro──音频文件携带关于创建工具、作者、日期的加密签名元数据──Audobox / Seamless 使用它── es útil para la retroceso; pero si los malintencionados vuelven a codificar y desprender los datos es ineficaz──

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.

> **【拓展：语音隐私与安全】**语音数据 contiene una gran cantidad de información personal privada ([[音纹]], diálogo contenido) ◦ profundidad falsificación (Deepfake) 语音技术 (语音技术) puede ser utilizada para fraude (音频水印) 音频水印 (音频水印) 音纹水标 (音符标) 声纹反欺诈 (音纹反欺诈) ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]]




## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

```figure
v4-audio-watermark
```

## Construye el mismo

### Paso 1: un detector de características espectrales simple (juego)

> Paso 1: Simple de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la frecuencia de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de prueba de la prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba

```python
def spectral_rolloff(spec, percentile=0.85):
    cum = 0
    total = sum(spec)
    if total == 0:
        return 0
    threshold = total * percentile
    for k, v in enumerate(spec):
        cum += v
        if cum >= threshold:
            return k
    return len(spec) - 1

def is_suspicious(audio):
    spec = magnitude_spectrum(audio)
    rolloff = spectral_rolloff(spec)
    return rolloff / len(spec) > 0.92
```

El habla sintética a menudo tiene una energía de alta frecuencia inusualmente plana.

> El lenguaje sintético suele tener una alta frecuencia de energía anormalmente plana.

### Paso 2: AudioSeal embebed + detecta

> Paso 2: AudioSeal 嵌入 + 检测

```python
from audioseal import AudioSeal
import torch

generator = AudioSeal.load_generator("audioseal_wm_16bits")
detector = AudioSeal.load_detector("audioseal_detector_16bits")

audio = load_wav("generated.wav", sr=16000)[None, None, :]
payload = torch.tensor([[1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0]])
watermark = generator.get_watermark(audio, sample_rate=16000, message=payload)
watermarked = audio + watermark

result, decoded_payload = detector.detect_watermark(watermarked, sample_rate=16000)
# result: float in [0, 1] — probability of watermark presence
# decoded_payload: 16 bits; match against embedded payload
```

### Paso 3: evaluación  EER

> 步骤 3: evaluar  EER(等 error rate)

```python
def eer(real_scores, fake_scores):
    thresholds = sorted(set(real_scores + fake_scores))
    best = (1.0, 0.0)
    for t in thresholds:
        far = sum(1 for s in fake_scores if s >= t) / len(fake_scores)
        frr = sum(1 for s in real_scores if s < t) / len(real_scores)
        if abs(far - frr) < best[0]:
            best = (abs(far - frr), (far + frr) / 2)
    return best[1]
```

### Paso 4: la integración de la producción

> Paso 4: Clasificación de producción

```python
def safe_tts(text, voice, clone_reference=None):
    if clone_reference is not None:
        verify_consent(user_id, clone_reference)
    audio = tts_model.synthesize(text, voice)
    audio_with_wm = audioseal_embed(audio, payload=build_payload(user_id, model_id))
    manifest = c2pa_sign(audio_with_wm, user_id, timestamp=now())
    return audio_with_wm, manifest
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


Cada generación de buques: (1) marca de agua, (2) manifiesto firmado, (3) registro de auditoría conforme a las políticas de retención.

> Cada generación de resultados incluye: 1) agua, 2) lista de firmas, 3) acuerdo con la estrategia de retención de la auditoría.




> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

| Use case | Defense |
|----------|---------|
| Shipping TTS / voice cloning / 上线 TTS/语音克隆 | AudioSeal embed on every output (non-negotiable) / 每次输出嵌入 AudioSeal（不可妥协） |
| Biometric voice unlock / 生物识别语音解锁 | AASIST + ECAPA ensemble; liveness challenge / AASIST + ECAPA 集成；活体挑战 |
| Call-center fraud detection / 呼叫中心欺诈检测 | AASIST on 20% sample of incoming calls / 对 20% 的来电做 AASIST 检测 |
| Podcast authenticity / 播客真实性 | C2PA signing on upload, AudioSeal if AI-generated / 上传时 C2PA 签名，AI 生成则加 AudioSeal |
| Research / training detectors / 研究/训练检测器 | ASVspoof 5 train/dev/eval sets / ASVspoof 5 训练/开发/评估集 |



## Las trampas

> 常见陷

- **Watermark without detector ever running.**Envía el detector en tu informador.
  En inglés:**嵌入水印但从未运行检测器。**No tiene sentido.
- **Detection without calibration.**AASIST entrenado en los sobresaltos de los EE.UU. y la precisión en el mundo real.
  En inglés:**检测未校准。**En los Estados Unidos, los entrenamientos de los asistentes de la AASIST han sido adaptados; la tasa de precisión real ha disminuido.
- **Pitch-shift gap.**El cambio de tono agresivo elimina la mayoría de las marcas de agua.
  En inglés:**音高偏移漏洞。**激进的音高偏移能去除大多数水印──准备检测作为后备──
- **Metadata strip-and-rehost.**C2PA es trivialmente evitable mediante el re-encodificación. Siempre añadir criptografía + perceptual (marca de agua) defensa juntos.
  En inglés:**元数据剥离重新托管。**C2PA 通过重新编码即可轻松绕过──始终同时使用加密 + 感知(水印) defensa──
- **Liveness as detection.**Pida al usuario que diga una frase aleatoria. Previene los ataques de repetición pero no la clonación en tiempo real.
  En inglés:**活体检测作为检测手段。**让用户说一个随机短语──能防止重发攻击,但不能防止实时克隆──

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-spoof-defender.md`. Seleccionar el modelo de detección, la marca de agua, el manifiesto de procedencia y el manual de juego operativo para un despliegue de la generación de voz.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-spoof-defender.md`◊ para un lenguaje generador de la aplicación de selección de análisis de modelos、 agua印、 origen清单和运营手册。

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`. Detector de juguetes + marca de agua de juguetes incorporada/detectada en audio sintético.
   En inglés:**简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`◊ en sintetizado audio频上测试玩具检测器 + 玩具水印嵌入/检测──
2. **Medium.**Instalar`audioseal`, embebebedar una carga útil de 16 bits en una salida TTS, volver a decodificar, corromper el audio con ruido y medir la precisión de recuperación de bits.
   En inglés:**中等。**Instalación`audioseal`, en TTS 输出中嵌入 16 位载荷,重新解码──用噪音损坏音频并测量位恢复准确率──
3. **Hard.**Tune a la perfección un RawNet2 o AASIST en ASVspoof 2019 LA. Medir EER. Prueba en un conjunto prolongado de clips generados por F5-TTS  ver cómo se degrada la detección de OOD.
   En inglés:**困难。**En ASVspoof 2019 LA 上微调 RawNet2 或 AASIST──测量 EER──在留出的 F5-TTS 生成音频集上测试观察 OOD 检测的退化程度──

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| ASVspoof | The benchmark | Biennial challenge; 2024 = ASVspoof 5. / 双年挑战赛；2024 = ASVspoof 5 |
| CM (countermeasure) | Detector | Classifier: real speech vs synthetic / converted. / 分类器：真实语音 vs 合成/转换语音 |
| SASV | Speaker verif + CM | Integrated biometric + spoof detection. / 集成生物识别 + 欺骗检测 |
| AudioSeal | Meta watermark | Localized, 16-bit payload, 485× faster than WavMark. / 局部化，16 位载荷，比 WavMark 快 485 倍 |
| Bit Recovery Accuracy | Watermark survival | Fraction of payload bits recovered after attack. / 攻击后恢复的载荷位比例 |
| C2PA | Provenance manifest | Cryptographic metadata about creation / authorship. / 关于创建/作者身份的加密元数据 |
| AASIST | Detector family | Graph-attention-based anti-spoofing SOTA. / 基于图注意力的反欺骗 SOTA |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Todisco et al. (2024). ASVspoof 5](https://dl.acm.org/doi/10.1016/j.csl.2025.101825) el índice de referencia actual.
  Los Estados Unidos están en la lista de los primeros países en el mundo.
- [Defossez et al. (2024). AudioSeal](https://arxiv.org/abs/2401.17264) el signo de agua por defecto.
  Defossez 等(2024).
- [Chen et al. (2025). WaveVerify](https://arxiv.org/abs/2507.21150)Detector de EMO para ataques temporales.
  Chen 等(2025). WaveVerify  en contra del ataque de tiempo MoE 检测器──
- [Jung et al. (2022). AASIST](https://arxiv.org/abs/2110.01200) la columna vertebral de detección de SOTA.
  Jung 等(2022). AASISTSOTA 检测骨干──
- [AudioMarkBench (2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d9b7775296a641a1913ab6b4425d5e8-Paper-Datasets_and_Benchmarks_Track.pdf) Evaluación de la robustez.
  AudioMarkBench (en inglés) 鲁棒性评估──
- [C2PA specification](https://c2pa.org/specifications/specifications/) formato del manifiesto de procedencia.
  C2PA 规范来源清单格式──

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

