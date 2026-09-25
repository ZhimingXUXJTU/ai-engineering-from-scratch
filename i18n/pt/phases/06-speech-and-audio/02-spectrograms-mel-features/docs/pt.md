# Espectogramas, Mel Scale & Audio Features.

> As redes neurais não consomem bem as formas de onda crudas. Consomem espectrogramas. Consomem espectrogramas mel ainda melhor. Cada classificador de áudio ASR, TTS e em 2026 vive ou morre por esta única escolha de pré-processamento.

> **【中文解读】**O processamento de ondas de rede de neurônios não é bom, mas o processamento de frequências de frequência é bom, o processamento de frequências de frequência de Mel é melhor.

> **【拓展：Mel 频谱图是音频 AI 的 "图像"】**Mel 频谱图将音频转换为 2D 图像(时间×频率), pode ser usado para o tratamento de CNN/ViT──Whisper、MusicGen、Stable Audio 都使用 Mel 频谱图作为中间表示──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 01 (Audio Fundamentals) | **前置知识:** 阶段 6 · 01（音频基础）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## O problema é o problema da introdução

Tome um clip de 10 segundos a 16 kHz, isto é 160.000 floats, tudo em`[-1, 1]`A forma de onda crua possui as informações, mas em uma forma que o modelo não pode extrair facilmente.

> 16 kHz de 10 segundos. Era 160.000.`[-1, 1]`范围内, quase não está completamente relacionado com o rótulo "dog calling" ou "单词 cat" △.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

Um espectrograma corrige isso. Ele desmorona o detalhe temporal onde a percepção humana ignora (microsecondiário jitter) e preserva a estrutura onde a percepção atende (que frequências são energéticas, sobre janelas de tempo de ~ 1025 ms).

> O gráfico de frequência resolveu este problema. Ele comprimiu os detalhes do tempo ignorado pelo sentimento humano (microssegundos) e manteve a estrutura de atenção do sentimento (em cerca de 1025 ms, quais as frequências têm energia)

Os espectrogramas mel empurram mais longe. Os seres humanos percebem o pitch logaritmicamente: 100 Hz vs 200 Hz soam "a mesma distância entre si" que 1000 Hz vs 2000 Hz. A escala mel distorce o eixo de frequência para corresponder. Um espectrograma mel-escalado é a característica mais importante do discurso ML de 2010 a 2026.

> Mel 频谱图进一步──人类对音高的感知是对数的: 100 Hz 与 200 Hz 听起来和 1000 Hz 与 2000 Hz "distância é igual"──Mel scale will frequency axis torsion to match this perception──Mel 频谱图是2010-2026年语音机学习中最重要的单一特征──

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![Waveform to STFT to mel spectrogram to MFCC ladder](../assets/mel-features.svg)

**STFT (Short-Time Fourier Transform).**Corte a forma de onda em quadros sobrepostos (típico: 25 ms janela, 10 ms hop = 400 amostras / 160 amostras em 16 kHz). Multiplicar cada quadro por uma função de janela (Hann é o padrão; Hamming com troca ligeiramente diferente). FFT cada quadro. Apila os espectros de magnitude em uma matriz de forma `(n_frames, n_freq_bins)`É o teu espectrograma.

> **STFT（短时傅里叶变换）。**A forma de um movimento é diferente, mas não é o mesmo que o tempo de um movimento.`(n_frames, n_freq_bins)`É a sua forma de reprodução.

**Log-magnitude.**Grandes dimensões cruas variam entre 5 e 6 ordens de magnitude.`log(|X| + 1e-6)`ou `20 * log10(|X|)`Cada linha de produção usa magnitude de log, não magnitude bruta.

> **对数幅度。**A amplitude original atravessa 5-6 classes numéricas.`log(|X| + 1e-6)`Ou `20 * log10(|X|)`Para comprimir a gama de movimentos, cada linha de produção é utilizada para a amplitude numérica e não para a amplitude original.

**Mel scale.**Frequência`f`em mapas Hz para mel `m`Por`m = 2595 * log10(1 + f / 700)`O mapeamento é aproximadamente linear abaixo de 1 kHz e aproximadamente logarítmico acima. 80 melbins cobrindo 08 kHz é a entrada ASR padrão.

> **Mel 尺度。**Frequência`f`(Hz) Meteragem até mel`m` 的公式为 `m = 2595 * log10(1 + f / 700)`◊ O que é o que se passa em 1 kHz:

**Mel filterbank.**Um conjunto de filtros triangulares espaçados igualmente na escala mel. Cada filtro é uma soma ponderada de contenedores FFT adjacentes. Multiplicando a magnitude STFT pela matriz filterbank dá o espectrograma mel em um matmul.

> **Mel 滤波器组。**Um grupo em escala mel igual a uma distância entre as três partes do conjunto. Cada um dos grupos é o aumento de peso do bin FFT em relação ao outro.

**Log-mel spectrogram.** `log(mel_spec + 1e-10)`A entrada do Whisper, a entrada do Parakeet, a entrada do SeamlessM4T, a entrada do frontend de áudio universal de 2026.

> **对数 Mel 频谱图。** `log(mel_spec + 1e-10)`❖ Whisper 的输入──Parakeet 的输入──SeamlessM4T 的输入──2026 年通用音频前端──

**MFCCs.**Pegue o espectrograma log-mel, aplique um DCT (tipo II), mantenha os primeiros 13 coeficientes. Decorrela as características e comprime mais. Figura dominante até cerca de 2015, quando as CNNs/Transformers em log-mels crues foram capturadas. Ainda é usada no reconhecimento de alto-falantes (vectores x, ECAPA).

> **MFCC。**取对数 Mel 频谱图,应用 DCT(类 II),保留前 13 个系数──除特征间相关性并进一步压缩──2015年之前的主流特征,之后CNN/Transformer 在原始 log-mel 上追上──仍然用于说话人识别(x-vectors、ECAPA)──

**Resolution trade.**Maior FFT = melhor resolução de frequência, mas pior resolução de tempo. 25 ms / 10 ms é o padrão de áudio-ML; 50 ms / 12,5 ms para música; 5 ms / 2 ms para detecção transitória (bateria, plosivos).

> **分辨率权衡。**FFT maior = melhor frequência de resolução mas menor de tempo de resolução.

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.



## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

```figure
spectrogram-window
```

## Construí-lo

### Passo 1: enquadrar a forma de onda

```python
def frame(signal, frame_len, hop):
    n = 1 + (len(signal) - frame_len) // hop
    return [signal[i * hop : i * hop + frame_len] for i in range(n)]
```

Um clip de 10 segundos de 16 kHz com `frame_len=400, hop=160`- E dá 998 quadros.

> 1 段 10 秒 16 kHz 的音频,使用 `frame_len=400, hop=160`- Sim, eu tenho 998.

### Passo 2: Janela Hann

```python
import math

def hann(N):
    return [0.5 * (1 - math.cos(2 * math.pi * n / (N - 1))) for n in range(N)]
```

Multiplicar com elementos antes do FFT. Elimina vazamento espectral causado por truncar em pontos finais não-zero.

> Antes da FFT, a fissão de frequência de elementos é eliminada devido à interrupção de pontos não-zero.

### Passo 3: Magnitude STFT

```python
def stft_magnitude(signal, frame_len=400, hop=160):
    win = hann(frame_len)
    frames = frame(signal, frame_len, hop)
    return [magnitudes(dft([w * s for w, s in zip(win, f)])) for f in frames]
```

Utilizações de produção `torch.stft`ou `librosa.stft`O ciclo aqui é pedagógico; ele é executado em clips curtos em`code/main.py`- Não .

> Produção ambiental`torch.stft`Ou `librosa.stft`(Baseado em FFT ∼ em quantificação) ∼ Este ciclo é de ensino; está em`code/main.py`中处理短音频片段──

### Passo 4: Mel filterbank

```python
def hz_to_mel(f):
    return 2595.0 * math.log10(1.0 + f / 700.0)

def mel_to_hz(m):
    return 700.0 * (10 ** (m / 2595.0) - 1)

def mel_filterbank(n_mels, n_fft, sr, fmin=0, fmax=None):
    fmax = fmax or sr / 2
    mels = [hz_to_mel(fmin) + (hz_to_mel(fmax) - hz_to_mel(fmin)) * i / (n_mels + 1)
            for i in range(n_mels + 2)]
    hzs = [mel_to_hz(m) for m in mels]
    bins = [int(h * n_fft / sr) for h in hzs]
    fb = [[0.0] * (n_fft // 2 + 1) for _ in range(n_mels)]
    for m in range(n_mels):
        for k in range(bins[m], bins[m + 1]):
            fb[m][k] = (k - bins[m]) / max(1, bins[m + 1] - bins[m])
        for k in range(bins[m + 1], bins[m + 2]):
            fb[m][k] = (bins[m + 2] - k) / max(1, bins[m + 2] - bins[m + 1])
    return fb
```

80 mels cobrindo 08 kHz com `n_fft=400`dá um `(80, 201)`Matriz. Multiplica o `(n_frames, 201)`A magnitude da STFT pela transposição para obter `(n_frames, 80)`Espectograma de mel.

> 80 milhas de 08 kHz,`n_fft=400`- Não .`(80, 201)`- Não, não.`(n_frames, 201)`A amplitude do STFT multiplicada por transformação`(n_frames, 80)`De mel 频谱图──

### Passo 5: log-mail

```python
def log_mel(mel_spec, eps=1e-10):
    return [[math.log(max(v, eps)) for v in frame] for frame in mel_spec]
```

Alternativas comuns: `librosa.power_to_db`(dB normalizado em referência), `10 * log10(power + eps)`O Whisper usa um clip mais envolvido + normaliza a rotina (ver Whisper's `log_mel_spectrogram`)).

> 常见替代方案:`librosa.power_to_db`(Reflexão em dB)`10 * log10(power + eps)`❖ Suspirar  使用更复杂的剪裁 + 归一化流程 ◎参见 ◎`log_mel_spectrogram`)。

### Passo 6: CFPM

```python
def dct_ii(x, n_coeffs):
    N = len(x)
    return [
        sum(x[n] * math.cos(math.pi * k * (2 * n + 1) / (2 * N)) for n in range(N))
        for k in range(n_coeffs)
    ]
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


Aplique DCT a cada quadro log-mel, mantenha os primeiros 13 coeficientes. Essa é a sua matriz MFCC. O primeiro coeficiente é geralmente caído (ela codifica a energia total).

> Para cada log-mail  aplica DCT, reter anterior 13 系数── é o seu MFCC 矩阵── o primeiro系数 é geralmente abandonado.




> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

A pilha de 2026:

> Tecnologia de 2026:

| Task | Features |
|------|----------|
| ASR (Whisper, Parakeet, SeamlessM4T) | 80 log-mels, 10 ms hop, 25 ms window |
| TTS acoustic model (VITS, F5-TTS, Kokoro) | 80 mels, 5–12 ms hop for fine temporal control |
| Audio classification (AST, PANNs, BEATs) | 128 log-mels, 10 ms hop |
| Speaker embedding (ECAPA-TDNN, WavLM) | 80 log-mels or raw-waveform SSL |
| Music (MusicGen, Stable Audio 2) | EnCodec discrete tokens (not mels) |
| Keyword spotting | 40 MFCCs for tiny devices |

| 任务 | 特征配置 |
|------|----------|
| ASR（Whisper、Parakeet、SeamlessM4T） | 80 log-mels，10 ms 步长，25 ms 窗口 |
| TTS 声学模型（VITS、F5-TTS、Kokoro） | 80 mels，5–12 ms 步长，精细时间控制 |
| 音频分类（AST、PANNs、BEATs） | 128 log-mels，10 ms 步长 |
| 说话人嵌入（ECAPA-TDNN、WavLM） | 80 log-mels 或原始波形 SSL |
| 音乐（MusicGen、Stable Audio 2） | EnCodec 离散 token（非 mels） |
| 关键词检测 | 40 MFCCs，用于小型设备 |

Regra geral: **if you are not working on music, start with 80 log-mels.**O fardo da prova está em qualquer desvio.

> 经验法则:**如果你不是在做音乐，就从 80 log-mels 开始。**Qualquer desvio precisa provar a sua racionalidade.



## Encurralagens que ainda se lançam em 2026

> 2026 ano ainda em vítima de um erro

- **Mel count mismatch.**Treinamento com 80 mels, inferência com 128 mels, falha silenciosa, registro da forma de característica em ambas as extremidades.
  **Mel 数量不匹配。**Treinar com 80 mels, pensar com 128 mels.
- **Sample-rate mismatch upstream.**Mels computados a 22,05 kHz parecem diferentes de 16 kHz.
  **上游采样率不匹配。**22,05 kHz 计算的 mels与16 kHz的不同──在特征化*之前*修正采样率──
- **dB vs log.**O Whisper espera o log-mel, não o dB-mel.
  **dB 与 log。**Whisper 期望 log-mel e não dB-mel。 certos HF 流水线会自动检测; seu código de auto-definição não será。
- **Normalization drift.**Normalização de per-utterance durante o treinamento, normalização global durante a inferência.
  **归一化漂移。**                                                                                                                                                                                                                                                              
- **Leakage from padding.**O pad zero na extremidade de um clip produz um espectro plano nos quadros traseiros.
  **填充泄漏。**Para os episódios de som final, o número de preenchimentos é de um número de vezes mais elevado.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-feature-extractor.md`A habilidade seleciona o tipo de característica, a contagem de mel, o quadro/sopa e a normalização para um determinado alvo modelo.

> 保存为 `outputs/skill-feature-extractor.md` Esta habilidade é utilizada para determinar o modelo de objetivo de seleção de características tipo, número de milhas,

## Exercícios.

1. **Easy.**Corra .`code/main.py`- Sintetiza um chirp (frequência varrida 200 → 4000 Hz) e imprime o argmax mel bin por quadro.
   **简单。**运行 `code/main.py`◊ é sintetizado um sinal  freqüência de 200 扫到 4000 Hz)  é impresso em cada  de argmax mel bin── desenho 可选) 并确认与扫频匹配──
2. **Medium.**Repete com `n_mels`em `{40, 80, 128}`E ...`frame_len`em `{200, 400, 800}`- Medir a largura de banda de pico acentuado através do eixo do tempo.
   **中等。**- Não .`n_mels`Por`{40, 80, 128}`和 `frame_len`Por`{200, 400, 800}`重新运行. Qual é a melhor combinação para identificar sinais?
3. **Hard.**Implementação `power_to_db`e comparar a precisão ASR de um pequeno classificador CNN no AudioMNIST usando (a) log-mel bruto, (b) dB-mel com `ref=max`, (c) MFCC-13 + delta + delta-delta.
   **困难。** realização `power_to_db`, em AudioMNIST 上用微型 CNN 分类器比较 (a) 原始 log-mel、(b)`ref=max`准确率──报告 top-1 准确率── MFCC-13 + delta + delta-delta 准确率──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Frame | A slice | 25 ms chunk of waveform fed to one FFT. |
| Hop | Stride | Samples between consecutive frames; 10 ms is ASR default. |
| Window | Hann/Hamming thing | Point-wise multiplier that tapers the frame edges to zero. |
| STFT | Spectrogram generator | Framed + windowed FFT; yields time × frequency matrix. |
| Mel | Warped frequency | Log-perception scale; `m = 2595·log10(1 + f/700)`. |
| Filterbank | The matrix | Triangular filters that project STFT onto mel bins. |
| Log-mel | Whisper's input | `log(mel_spec + eps)`; standardized in 2026. |
| MFCC | Old-school feature | DCT of log-mel; 13 coeffs, decorrelated. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 帧 | 一段切片 | 送入一次 FFT 的 25 ms 波形片段。 |
| 步长 | 步幅 | 连续帧之间的采样点数；10 ms 是 ASR 默认值。 |
| 窗函数 | Hann/Hamming 那个东西 | 将帧边缘逐渐缩减为零的逐点乘数。 |
| STFT | 频谱图生成器 | 分帧 + 加窗的 FFT；产生时间 × 频率矩阵。 |
| Mel | 扭曲的频率 | 对数感知尺度；`m = 2595·log10(1 + f/700)`。 |
| 滤波器组 | 那个矩阵 | 将 STFT 投影到 mel bin 的三角滤波器。 |
| Log-mel | Whisper 的输入 | `log(mel_spec + eps)`；2026 年标准化。 |
| MFCC | 老派特征 | log-mel 的 DCT；13 个系数，去相关。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Davis, Mermelstein (1980). Comparison of parametric representations for monosyllabic word recognition](https://ieeexplore.ieee.org/document/1163420) o documento do MFCC.
  Davis、Mermelstein (1980) 单音节词识别的参数化表示比较MFCC 论文──
- [Stevens, Volkmann, Newman (1937). A Scale for the Measurement of the Psychological Magnitude Pitch](https://pubs.aip.org/asa/jasa/article-abstract/8/3/185/735757/)- A escala mel original.
  Stevens, Volkmann, Newman (1937) 心理音高量级的尺度尺度 原始 mel 尺度──
- [OpenAI — Whisper source, log_mel_spectrogram](https://github.com/openai/whisper/blob/main/whisper/audio.py) ler a aplicação de referência.
  OpenAIWhisper 源码,log_mel_spectrogram阅读参考实现──
- [librosa feature extraction docs](https://librosa.org/doc/main/feature.html) referência para `mfcc`- Não .`melspectrogram`, e salto/janela.
  Biblioteca Features提取文档`mfcc`- Não.`melspectrogram`O que é que se passa?
- [NVIDIA NeMo — audio preprocessing](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/asr_all.html#featurizers) Pipeline em escala de produção para os modelos Parakeet + Canary.
  NVIDIA NeMo音频预处理Parakeet + Canary 模型的生产级流水线──

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

