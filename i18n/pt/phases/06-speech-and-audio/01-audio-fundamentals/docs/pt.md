# Fundamentos de áudio  Ondas, amostragem, Fourier Transform  音频基础  波形、采样与里叶变换

> As ondas são o sinal bruto. Os espectrogramas são a representação. As características Mel são a forma amigável ao ML. Cada moderno ASR e TTS caminha nesta escada, e o primeiro passo é entender a amostragem e Fourier.

> **【中文解读】**波形是原始信号,频谱图是表示形式,Mel特征是机器学习友好的形式──每个现代语音识别(ASR) 和语音合成(TTS) sistemas são ao longo desta escala:波形 → 频谱图 → Mel特征──第一阶段就是理解采样和里叶变之──

> **【拓展：音频 AI 的基础】**采样率 (como 16kHz) determina a freqüência máxima que pode ser expressa (Náquioes específicos) 里叶变化将时域信号分解为频域成分──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 1 · 06 (Vectors & Matrices), Phase 1 · 14 (Probability Distributions) | **前置知识:** 阶段 1 · 06（向量与矩阵），阶段 1 · 14（概率分布）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## O problema é o problema da introdução

Um microfone produz um sinal de pressão contra tempo. Sua rede neural consome tensores. Entre eles fica uma pilha de convenções que, quando violadas, produz bugs silenciosos: o modelo se prepara bem, mas o WER duplica, ou o TTS envia um silbido, ou um sistema de clonagem de voz memoriza o microfone em vez do alto-falante.

> O seu consumo de rede neural é de volume. Entre os dois, um monte de convenções contra estas convenções produzem bugs de ocultação: o modelo de treinamento é normal, mas é duplicado, ou o TTS produz o som, ou o sistema de conversão relembra o seu comportamento.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

Cada bug nos sistemas de fala remonta a uma das três perguntas:

> Cada bug no sistema de voz pode ser traçado a um dos três seguintes problemas:

1. Em que taxa de amostragem foram registados os dados, e o que o modelo espera?
   Qual é a taxa de amostragem de gravação de dados, qual é a taxa de amostragem de modelos esperados?
2. O sinal é alias?
   O sinal é que há confusão?
3. Está a operar com amostras brutas ou com uma representação de frequência?
   Você está a tratar o ponto de amostra original ou a frequência de expressão?

Se as fizerem bem, o resto da Fase 6 é fácil de tratar, e até o Whisper-Large-v4 produz lixo.

> Para resolver estes três problemas, o resto da fase 6 é fácil de entender.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![Waveform, sampling, DFT, and frequency bins visualized](../assets/audio-fundamentals.svg)

**Waveform.**Uma matriz unidimensional de flutuantes em `[-1.0, 1.0]`Para converter em segundos, divide pela taxa de amostragem:`t = n / sr`Um clip de 10 segundos a 16 kHz é uma matriz de 160.000 floats.

> **波形（Waveform）。**Um valor de compra`[-1.0, 1.0]`间一维浮点数组──以采样编为索引──转换为秒数,除以采样率:`t = n / sr`◊ 1 段 10 segundos de 16 kHz 音频 é um número de 160.000 个浮点数.

**Sampling rate (sr).**Quantas amostras por segundo.

> **采样率（sr）。**Número de pontos de amostragem por segundo.

| Rate | Use |
|------|-----|
| 8 kHz | Telephony, legacy VOIP. Nyquist at 4 kHz kills consonants. Avoid for ASR. |
| 16 kHz | ASR standard. Whisper, Parakeet, SeamlessM4T v2 all consume 16 kHz. |
| 22.05 kHz | TTS vocoder training for older models. |
| 24 kHz | Modern TTS (Kokoro, F5-TTS, xTTS v2). |
| 44.1 kHz | CD audio, music. |
| 48 kHz | Film, pro audio, high-fidelity TTS (VALL-E 2, NaturalSpeech 3). |

| 采样率 | 用途 |
|--------|------|
| 8 kHz | 电话、传统 VOIP。奈奎斯特频率 4 kHz 会丢失辅音。ASR 应避免使用。 |
| 16 kHz | ASR 标准。Whisper、Parakeet、SeamlessM4T v2 均使用 16 kHz。 |
| 22.05 kHz | 旧模型 TTS 声码器训练。 |
| 24 kHz | 现代 TTS（Kokoro、F5-TTS、xTTS v2）。 |
| 44.1 kHz | CD 音质、音乐。 |
| 48 kHz | 电影、专业音频、高保真 TTS（VALL-E 2、NaturalSpeech 3）。 |

**Nyquist-Shannon.**Uma taxa de amostragem de `sr`pode representar de forma inequívoca frequências de até `sr/2`- O .`sr/2`O limite é a frequência de Nyquist. A energia acima de Nyquist fica * alias *  dobrado para baixo em frequências mais baixas  e corrompe o sinal.

> **奈奎斯特-香农定理。**采样率 `sr`Pode sem diferença significar o máximo até `sr/2`A frequência:`sr/2`边界就是奈奎斯特频率 (····························) ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞      ∞                                                                

**Bit depth.**O PCM de 16 bits (assinado int16, intervalo ±32.767) é o formato de troca universal.`soundfile`ler int16 mas expor float32 matrizes em `[-1, 1]`- Não .

> **位深度。**16 位 PCM(有符号 int16,范围 ±32,767) é um formato de câmbio geral.`soundfile`Esperar para ler o artigo 16 mas voltar.`[-1, 1]`范围的 float32 数组──

**Fourier Transform.**Qualquer sinal finito é uma soma de sinusoides em diferentes frequências.`N`amostras, `N`coeficientes complexos  um por caixa de frequências. `bin k`mapas de frequência `k · sr / N`Magnitude é amplitude nessa frequência, ângulo é fase.

> **傅里叶变换。**Qualquer sinal limitado pode ser dividido em diferentes frequências de ondas de cordas e de ondas.`N`个采样点计算                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `N`个复数系数每个频率 bin 一个──`bin k`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `k · sr / N`Hz── amplitude é a amplitude da frequência, ângulo é fase──

**FFT.**Transformação rápida de Fourier: um `O(N log N)`Algoritmo para o DFT quando `N`Uma FFT de 1024-sampla em 16 kHz dá 512 canhões de frequência utilizáveis que abrangem 08 kHz em resolução de 15,6 Hz.

> **FFT。**快速里叶变换:当 `N`Por 2 de 时,DFT de `O(N log N)`算法── cada nível de base de rádio utiliza FFT──16 kHz 下 1024 采样点的 FFT 产生 512 个可用频率bin,覆盖08 kHz,分辨率为15.6 Hz──

**Framing + window.**Não FFT um clip inteiro. Nós o cortamos em *frames* sobrepostos (normalmente 25 ms com 10 ms hop), multiplicamos cada quadro por uma função de janela (Hann, Hamming) para matar discontinuidades de borda, então FFT cada quadro.

> **分帧 + 加窗。**Nós não fazemos FFT em todo o tempo, mas fazemos isso em 25 ms, 10 ms, cada vez mais em função de janela.

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.



## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

```figure
mel-scale
```

## Construí-lo

### Passo 1: ler um clip e traçar a forma de onda

`code/main.py`utiliza apenas o stdlib `wave`O módulo para manter a demonstração livre de dependência.`soundfile`ou `torchaudio.load`(ambos retornam `(waveform, sr)`- Tópicos:

> `code/main.py`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `wave`Modulo para manter a apresentação independente.`soundfile`Ou `torchaudio.load`(两者都回归 `(waveform, sr)`- O que é isso?

```python
import soundfile as sf
waveform, sr = sf.read("clip.wav", dtype="float32")  # shape (T,), sr=int
```

### Passo 2: sintetizar uma onda sinusal a partir dos primeiros princípios

```python
import math

def sine(freq_hz, sr, seconds, amp=0.5):
    n = int(sr * seconds)
    return [amp * math.sin(2 * math.pi * freq_hz * i / sr) for i in range(n)]
```

Um sinusoide de 440 Hz (concerto A) a 16 kHz por 1 segundo é 16 000 flutuantes.`wave.open(..., "wb")`usando codificação PCM de 16 bits.

> 16 kHz 采样率下 440 Hz 正弦波(标准音 A) dura 1 秒是 16,000 个浮点数──使用 `wave.open(..., "wb")`E 16 de PCM 编码写入──

### Passo 3: calcular a DFT à mão

```python
def dft(x):
    N = len(x)
    out = []
    for k in range(N):
        re = sum(x[n] * math.cos(-2 * math.pi * k * n / N) for n in range(N))
        im = sum(x[n] * math.sin(-2 * math.pi * k * n / N) for n in range(N))
        out.append((re, im))
    return out
```

`O(N²)`- Muito bem.`N=256`Para confirmar a corretão, inútil para áudio real.`numpy.fft.rfft`ou `torch.fft.rfft`- Não .

> `O(N²)`complicidade 对 `N=256`验证正确性还行,对真实音频没有用──实际代码调用 `numpy.fft.rfft`Ou `torch.fft.rfft`- Não.

### Passo 4: encontrar a frequência dominante

Indice de pico de magnitude `k_star`mapas de frequência `k_star * sr / N`Se executarmos isto no seno de 440 Hz , devemos retornar um pico no bin .`440 * N / sr`- Não .

> 幅度 peak value índice `k_star`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `k_star * sr / N`△ para 440 Hz 正弦波运行`440 * N / sr`处返峰值──

### Passo 5: demonstrar o aliasing

Amostra de um sinusoide de 7 kHz a 10 kHz (Nyquist = 5 kHz).`10 − 7 = 3 kHz`O pico da FFT aparece em 3 kHz. Esta é a demonstração clássica de alias e a razão de todos os navios DAC/ADC terem um filtro de baixa passagem de parede de tijolo.

> 以 10 kHz 采样 7 kHz 正弦波(奈奎斯特频率 = 5 kHz) ・7 kHz 音调高于奈奎斯特频率,会折叠到 `10 − 7 = 3 kHz`O pico de FFT aparece em 3 kHz. É um clássico show de contagem, e é também a razão de cada DAC/ADC estar equipado com um dispositivo de câmbio de câmbio.

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.





> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

A pilha que enviará em 2026:

> 2026 anos você realmente vai usar as técnicas:

| Task | Library | Why |
|------|---------|-----|
| Read/write WAV/FLAC/OGG | `soundfile` (libsndfile wrapper) | Fastest, stable, returns float32. |
| Resample | `torchaudio.transforms.Resample` or `librosa.resample` | Correct anti-aliasing built in. |
| STFT / Mel | `torchaudio` or `librosa` | GPU-friendly; PyTorch ecosystem. |
| Real-time streaming | `sounddevice` or `pyaudio` | Cross-platform PortAudio bindings. |
| Inspect a file | `ffprobe` or `soxi` | CLI, fast, reports sr/channels/codec. |

| 任务 | 库 | 原因 |
|------|----|------|
| 读写 WAV/FLAC/OGG | `soundfile`（libsndfile 封装） | 最快、最稳定，返回 float32。 |
| 重采样 | `torchaudio.transforms.Resample` 或 `librosa.resample` | 内置正确的抗混叠滤波。 |
| STFT / Mel | `torchaudio` 或 `librosa` | GPU 友好；PyTorch 生态。 |
| 实时流 | `sounddevice` 或 `pyaudio` | 跨平台 PortAudio 绑定。 |
| 检查文件 | `ffprobe` 或 `soxi` | 命令行工具，快速报告采样率/声道/编码。 |

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


Regra de decisão: **match sample rate before you match anything else**O Whisper espera 16 kHz mono float32. Passa-o com um estéreo de 44,1 kHz e vai ter lixo que parece um bug modelo.

>  决策规则:**在匹配其他任何东西之前先匹配采样率**❖ Suspirar  expectativa 16 kHz 单声道 float32──传入 44.1 kHz 立体声, você vai ficar parecendo um modelo de bug de lixo de saída──

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 




## Envia-o . Produto .

Salva como`outputs/skill-audio-loader.md`A habilidade ajuda a verificar se a entrada de áudio corresponde às expectativas do modelo a jusante e a repetição correta quando não o faz.

> 保存为 `outputs/skill-audio-loader.md`◊ Esta habilidade ajuda a verificar se as entradas de som correspondem às expectativas do modelo de som e se elas não correspondem.

## Exercícios.

1. **Easy.**Sintetize uma mistura de 1 segundo de 220 Hz + 440 Hz + 880 Hz a 16 kHz. Execute DFT. Confirme três picos nos contentores esperados.
   **简单。**合成一 220 Hz + 440 Hz + 880 Hz de 1 秒混合信号,采样率 16 kHz──运行 DFT──确认在预期bin 位置有三个峰值──
2. **Medium.**Grave um WAV de 3 segundos da sua voz a 48 kHz.`torchaudio.transforms.Resample`(com anti-aliasing), em seguida, para 16 kHz usando uma decimação ingênua (cada terceira amostra).
   **中等。**录制一段 3 秒 48 kHz 的语音 WAV──使用 `torchaudio.transforms.Resample`(带抗混叠) Baixa a 16 kHz, então, usando simplesmente extrair (((每隔三个样本取一个) Baixa a 16 kHz;;
3. **Hard.**Construir o STFT a partir do zero usando apenas `math`E o DFT do passo 3. tamanho do quadro 400, hop 160, janela Hann.`matplotlib.pyplot.imshow`Este é o espectrograma da lição 02.
   **困难。** apenas usados `math`和步骤 3 的 DFT 从零构建 STFT──大小 400,步长 160,Hann 窗──用 `matplotlib.pyplot.imshow`Escrever um quadro de amplitude.

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Sample rate | How many samples per second | Frequency in Hz at which the ADC measures the signal. |
| Nyquist | The max frequency you can represent | `sr/2`; energy above it aliases back down. |
| Bit depth | Resolution of each sample | `int16` = 65,536 levels; `float32` = 24-bit precision in `[-1, 1]`. |
| DFT | The Fourier transform for sequences | `N` samples → `N` complex frequency coefficients. |
| FFT | The fast DFT | `O(N log N)` algorithm requiring `N` = power of 2. |
| Bin | Frequency column | `k · sr / N` Hz; resolution = `sr / N`. |
| STFT | Spectrogram under the hood | Framed + windowed FFT over time. |
| Aliasing | Weird frequency ghosts | Energy above Nyquist mirroring down to lower bins. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 采样率 | 每秒多少个采样点 | ADC 测量信号的频率（Hz）。 |
| 奈奎斯特 | 能表示的最大频率 | `sr/2`；超过它的能量会混叠回来。 |
| 位深度 | 每个采样点的精度 | `int16` = 65,536 级；`float32` = `[-1, 1]` 中 24 位精度。 |
| DFT | 序列的傅里叶变换 | `N` 个采样 → `N` 个复数频率系数。 |
| FFT | 快速 DFT | `O(N log N)` 算法，要求 `N` 为 2 的幂。 |
| Bin | 频率列 | `k · sr / N` Hz；分辨率 = `sr / N`。 |
| STFT | 频谱图的底层实现 | 分帧 + 加窗的 FFT 随时间推移。 |
| 混叠 | 奇怪的频率鬼影 | 超过奈奎斯特的能量镜像到更低的 bin。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Shannon (1949). Communication in the Presence of Noise](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf) o papel por trás do teorema de amostragem.
  Shannon (1949) 带噪音条件下的通信采样定理后背的论文──
- [Smith — The Scientist and Engineer's Guide to Digital Signal Processing](https://www.dspguide.com/ch8.htm)Livro de texto livre e canônico de DSP.
  Smith  Cientistas e Engenheiros de Gestão de Sinais Digitais Guia  Clásico DSP
- [librosa docs — audio primer](https://librosa.org/doc/latest/tutorial.html) Passagem prática com código.
  Biblioteca 文档音频入门带代码的实践教程──
- [Heinrich Kuttruff — Room Acoustics (6th ed.)](https://www.routledge.com/Room-Acoustics/Kuttruff/p/book/9781482260434) referência para o motivo pelo qual o áudio do mundo real não é um sinusoide limpo.
  Heinrich Kuttruff房间声学(第 6 版) 解释为什么真世界音频不是干净正弦波的参考书──
- [Steve Eddins — FFT Interpretation notebook](https://blogs.mathworks.com/steve/2020/03/30/fft-spectrum-and-spectral-densities/)Intuição do bin de frequência resolvido em 10 minutos.
  Steve Eddins FFT 解读笔记10 分钟搞清频率 bin 的直觉──

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

