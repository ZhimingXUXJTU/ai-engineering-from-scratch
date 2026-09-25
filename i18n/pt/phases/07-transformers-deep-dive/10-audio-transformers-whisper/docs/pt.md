# Transformadores de áudio  Arquitetura de sussurros  Transformador de áudio  Arquitetura de sussurros 

> O áudio é uma imagem de frequência ao longo do tempo.

> **【中文解读】**Whisper Using Transformer fazer语音识别和翻译──理解音频如何变成符号序列送进 Transformer──

**Type:** Study | **类型:** 学习
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 08 (Encoder-Decoder), Phase 7 · 09 (ViT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 08 (Encoder-Decoder), Phase 7 · 09 (ViT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

Antes do Whisper (OpenAI, Radford et al. 2022), o reconhecimento automático de voz (ASR) de última geração significava wav2vec 2.0 e HuBERT  extractores de recursos auto-supervisionados além de uma cabeça afinada.

> Em Whisper, Radford, etc. (2022), antes de 2022, os mais avançados de reconhecimento automático de idiomas (ASR) usaram a onda 2.0 e o HuBERT, mas os dados são caros, sensíveis ao domínio.

O Whisper fez três apostas:

> O sussurro fez três notas:

1. **Train on everything.**680.000 horas de áudio com etiqueta fraca, arrancadas da Internet em 97 idiomas, sem corpus acadêmico limpo, sem etiquetas fonéticas.
   Tradução:**用一切数据训练。**680.000 horas de transmissão da Internet, abrangendo 97 idiomas.
2. **Multi-task single model.**Um decodificador treinado em conjunto em transcrição, tradução, detecção de atividade de voz, ID de idioma e timestamping através de tokens de tarefa.
   Tradução:**单模型多任务。**Um descifrador através de um token de tarefa 联合 training转录、翻译、语音活动检测、语言识别和时间──
3. **Standard encoder-decoder transformer.**O codificador consome espectrogramas log-mail. O decodificador produz tokens de texto autoregressivamente.
   Tradução:**标准编码器-解码器 Transformer。**编码器消费 log-mail 频谱图──解码器自归生成文本代币──没有声码器,没有CTC,没有HMM──

O resultado: Whisper big-v3 é robusto em acentos, ruído e linguagens que têm dados com rótulo limpo zero. É o front-end de fala padrão para todos os assistentes de voz de código aberto e a maioria dos comerciais em 2026.

> Resultado:Whisper big-v3 para a fala, ruído e dados de zero marcas linguísticas são todos com um robustez.

> **【中文解读】**Whisper's Three Big Innovations: 1) Used 680.000 hours weak标注音频训练,覆盖 97 种语言; 2) 单模型多任务(转录、翻译、语种识别、时间); 3) 标准编码器-解码器 Transformer 架。音频被转构为 log-mail 频谱图(类似图像),编码器处理频谱特征,解码器生成文本。

## O conceito central.

![Whisper pipeline: audio → mel → encoder → decoder → text](../assets/whisper.svg)

### Passo 1  Re-sampula + janela

Áudio em 16 kHz. Clip/pad para 30 segundos. Computação log-mel espectrograma: 80 mel bin, 10 ms passo → ~ 3.000 quadros × 80 recursos. Esta é a "imagem de entrada" que Whisper vê.

> 音频采样率 16 kHz──剪剪/填充到30秒──计算 log-mel 频谱图:80 个梅尔频率 bin,10 ms 步长 → 约 3,000  × 80特征──这是Whisper 看到的"输入图像"──

### Passo 2  tronco convolucional

Duas camadas Conv1D com kernel 3 e passo 2 reduzem os 3.000 quadros para 1.500.

> 两层 Conv1D(核大小 3,步长 2) reduzirá 3.000  para 1.500── reduzirá a duração do processo à metade sem aumentar muito mais parâmetros──

> **【拓展：Whisper 的多语言能力来源】**Whisper em 97 种语言、68万小时音频上训练, multilingual ability comes from two factors: 1) 超大规模的弱标注数据覆盖绝大多数语言; 2) 统一的BPE词表是GPT-2词表的超集,天然支持多语言──decoder prompt 中的语言代码符号如`<|zh|>`) controlar a linguagem de saída, para que o mesmo modelo possa executar a tarefa de transcrição ou tradução.

### Passo 3  codificador

Um codificador de transformador de 24 camadas (para grandes) em 1.500 etapas de tempo. codificação posicional sinusoidal, auto-atenção, GELU FFN. Produz estados ocultos de 1.500 × 1.280 .

> Uma 24 层(grande 版本) Transformador 编码器处理 1,500 个时间步──正弦位置编码、自注意力、GELU FFN── produzir 1.500 × 1,280 de estado oculto──

### Passo 4  decodificador

Um decodificador de transformador de 24 camadas. Ele produz automaticamente tokens a partir de um vocabulário BPE que é um superconjunto de GPT-2s com alguns tokens especiais específicos de áudio.

> Uma 24 Layer Transformer 解码器──自归地从 BPE 词表生成代币,该词表是GPT-2 词表的超集,外加几个音频专用特殊代币──

### Passo 5  Tokens de tarefa

O prompt do decodificador começa com tokens de controle que dizem ao modelo o que fazer:

> Para controlar o token, diga ao modelo o que fazer:

```
<|startoftranscript|>  <|en|>  <|transcribe|>  <|0.00|>
```

ou

```
<|startoftranscript|>  <|fr|>  <|translate|>   <|0.00|>
```

O modelo foi treinado nesta convenção. Você controla tarefa por prefixo. O equivalente a 2026 instrução-ajuste, mas aplicado à fala.

> 模型按这种约定训练──你通过前控制任务──这是语音领域的指令微调等价──

> **【中文解读】**O mecanismo de controle de missões do Whisper é muito bom: através de um token especial como`<|transcribe|>`Ou `<|translate|>`O "instrução de micro-modução" é aplicado no campo do som através de diferentes tokens de execução.

> **【拓展：Whisper 在语音助手中的应用】**O sussurro é um componente básico da AI de 2026 em idiomas. Desde o assistente de idiomas de tempo real até o gerenciamento de vídeos, o sussurro forneceu um primeiro nível de idiomas de um único nível.

### Passo 6  saída

Busca de feixe (largura 5) com um limiar de log-prob.`<|notimestamps|>`O token está ausente.

> 束搜索(宽度 5)加对数概率值──当没有 `<|notimestamps|>`- Não, não. - Não, não.

### Dimensões de sussurros

| Model | Params | Layers | d_model | Heads | VRAM (fp16) |
|-------|--------|--------|---------|-------|-------------|
| 模型 | 参数量 | 层数 | d_model | 头数 | 显存 (fp16) |
| Tiny | 39M | 4 | 384 | 6 | ~1 GB |
| Base | 74M | 6 | 512 | 8 | ~1 GB |
| Small | 244M | 12 | 768 | 12 | ~2 GB |
| Medium | 769M | 24 | 1024 | 16 | ~5 GB |
| Large | 1550M | 32 | 1280 | 20 | ~10 GB |
| Large-v3 | 1550M | 32 | 1280 | 20 | ~10 GB |
| Large-v3-turbo | 809M | 32 | 1280 | 20 | ~6 GB (4-layer decoder) |

O Large-v3-turbo (2024) cortou o decodificador de 32 camadas para 4.8× mais rápido decodificando com regressão de <1 ponto WER. Essa velocidade de desbloqueio de decodificação é a razão pela qual o Whisper-turbo é o padrão para agentes de voz em tempo real em 2026.

> Large-v3-turbo(2024) vai reduzir o decodificador de 32 níveis para 4 níveis;; a velocidade de decodificação aumentou 8 vezes, WER 退化不到 1个百分点;; essa ruptura da velocidade de decodificação é o motivo do Whisper-turbo 成为 2026年实时语音代理默认选择;;

> **【拓展：音频 Transformer 的统一趋势】**语音识别(Whisper)、语音合成(VALL-E, Kokoro)、音乐生成(MusicGen) 都在转向 Transformer 架构──核心思路相同:将音频转换为频谱图或离散代币 序列,然后使用标准 Transformer 处理──这验证了 Transformer 作为通用序列建模器的地位──

### O que o sussurro não faz

- Não há diário, para isso, é um par com o pyannote.
  Não há ninguém que possa falar com alguém.
- Não há transmissão em tempo real em modo nativo  a janela de 30 segundos está fixa.`faster-whisper`- Não .`WhisperX`) para o streaming através de superposições VAD +.
  Não há nenhuma solução para o processo de processamento.`faster-whisper`- Não.`WhisperX`) através de VAD + 重叠实现流式处理──
- Não há contexto de longa forma além de 30 segundos sem fragmentação externa. Funciona bem na prática porque a fala humana raramente precisa de contexto de longo alcance para transcrição.
  Não há blocos de parte externa que não suportem o formato de longa data superior a 30 segundos.

### 2026 paisagem

| Task | Model | Notes |
|------|-------|-------|
| 任务 | 模型 | 备注 |
| English ASR | Whisper-turbo, Moonshine | Moonshine is 4× faster on edge |
| 英语 ASR | Whisper-turbo, Moonshine | Moonshine 在边缘设备上快 4 倍 |
| Multilingual ASR | Whisper-large-v3 | 97 languages |
| 多语言 ASR | Whisper-large-v3 | 97 种语言 |
| Streaming ASR | faster-whisper + VAD | 150 ms latency targets achievable |
| 流式 ASR | faster-whisper + VAD | 可实现 150ms 延迟目标 |
| TTS | Piper, XTTS-v2, Kokoro | Encoder-decoder pattern, but Whisper-shaped |
| TTS | Piper, XTTS-v2, Kokoro | 编码器-解码器模式，但类似 Whisper |
| Audio + language | AudioLM, SeamlessM4T | Text tokens + audio tokens in one transformer |
| 音频 + 语言 | AudioLM, SeamlessM4T | 文本 token + 音频 token 在一个 Transformer 中 |

## Construí-lo e realizei-o.
```figure
n5-mel-decode
```

## Construí-lo

Veja .`code/main.py`Não treinamos o Whisper, construímos o log-mail espectrogram pipeline + task-token prompt formator.

> 参见 `code/main.py` Nós não treinamos Whisper  Nós construímos log-mail 频谱图管道 + 任务代码 提示格式化器──这些是你在生产中的实际接触的部分──

### Passo 1: sintetizar áudio

Gerar uma onda sinusal de 1 segundo a 440 Hz, amostragem a 16 kHz. 16.000 amostras.

> A onda de 440 Hz de 1 segundo, taxa de tomada de 16 kHz, 16.000 pontos de tomada.

### Passo 2: Espectograma log-mel (simplificado)

O espectro mel completo precisa de FFT. Fazemos uma estrutura simplificada + versão de energia por quadro que mostra o oleoduto sem exigir `librosa`- Não .

> O que é que é que é o que é que é que é?`librosa`Indicações de produção:

```python
def frame_signal(x, frame_size=400, hop=160):
    frames = []
    for start in range(0, len(x) - frame_size + 1, hop):
        frames.append(x[start:start + frame_size])
    return frames
```

O quadro = 25 ms, o hop = 10 ms. Correspondem à janela do Whisper.

>  = 25 ms,步长 = 10 ms──与 Whisper 的窗口匹配──逐能量用于教学演示,替代梅尔频率 bin──

### Passo 3: pad para 30 s

O Whisper sempre processa pedaços de 30 segundos. Pad (ou clip) o espectrograma para 3.000 quadros.

> Fosse 总是处理 30 秒分块──将频谱图填充或剪) até 3.000 ──

### Passo 4: criar os tokens de prompt

```python
def whisper_prompt(lang="en", task="transcribe", timestamps=True):
    tokens = ["<|startoftranscript|>", f"<|{lang}|>", f"<|{task}|>"]
    if not timestamps:
        tokens.append("<|notimestamps|>")
    return tokens
```

É toda a superfície de controlo de tarefas.

> É o que acontece com o controle de todos os tokens.

## Use-o com o framework implementado.

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("meeting.wav", language="en", task="transcribe")
print(result["text"])
print(result["segments"][0]["start"], result["segments"][0]["end"])
```

Mais rápido, compatível com o OpenAI:

> O programa mais rápido e compatível com o OpenAI:

```python
from faster_whisper import WhisperModel
model = WhisperModel("large-v3-turbo", compute_type="int8_float16")
segments, info = model.transcribe("meeting.wav", vad_filter=True)
for s in segments:
    print(f"{s.start:.2f} - {s.end:.2f}: {s.text}")
```

**When to pick Whisper in 2026:**

> **2026 年何时选择 Whisper：**

- ASR multilingue com um modelo.
  Tradução do inglês: using a model to do multi-lingual ASR.
- Uma transcrição robusta de áudio barulhento e diversificado.
  Tradução do idioma:                                                                                                                                                                                                                                                             
- Pesquisa / protótipo ASR  ponto de partida mais rápido.
  Tradução do inglês para tradução do inglês:研究/原型 ASR最快的起点──

**When to pick something else:**

> **何时选择其他方案：**

- Ultra-baixo streaming de latência em borda  Moonshine bate Whisper em qualidade correspondente.
  Tradução do inglês em japonês:  Moonshine 在相同质量下比 Whisper 更快──
- IA de conversação em tempo real que precisa de < 200 ms  ASR de streaming dedicado.
  Tradução do inglês para inglês: needs <200ms of real time dialogue AI专用流式 ASR。
- Diário de alto-falantes  Whisper não faz isso; paralelo em pyannote.
  Chinese:                                                                                                                                                                                                                                                              

## Envia-o . Produto .

Veja .`outputs/skill-asr-configurator.md`A habilidade escolhe um modelo ASR, parâmetros de decodificação e pipeline de pré-processamento para uma nova aplicação de fala.

> 参见 `outputs/skill-asr-configurator.md`◊ Esta habilidade é utilizada para novas aplicações de linguagem, escolha de modelos ASR, desciframento de parâmetros e de processos de pré-processamento.

## Exercícios.

1. **Easy.**Corra .`code/main.py`Confirme a contagem de quadros para um sinal de 1 segundo em 16 kHz com 10 ms salt é ~ 100 quadros.
   Tradução: 运行`code/main.py` Confirmar 1 秒 sinal em 16 kHz、10 ms 步长下约100 ──30 秒:约3,000 ──
2. **Medium.**Construir o espectro completo do log-mail usando `numpy.fft`Verifique 80 millatos de correspondência .`librosa.feature.melspectrogram(n_mels=80)`dentro do erro numérico.
   Tradução:`numpy.fft`构建完整的 log-mail 频谱图――验证 80 个梅尔频率 bin 与 `librosa.feature.melspectrogram(n_mels=80)`Em termos de diferença numérica de valores, coincidência.
3. **Hard.**Implemente inferência de streaming: fragmento de áudio em janelas de 10 segundos com sobreposição de 2 segundos, execute Whisper em cada fragmento, misture transcrições. Messa a taxa de erro de palavra versus passagem única em uma amostra de podcast de 5 minutos.
   Tradução do inglês em japonês:                                                                                                                                                                                                                                                           

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Mel spectrogram | "Audio image" | 2D representation: frequency bins on one axis, time frames on the other; log-scaled energy per cell. |
| 梅尔频谱图 | "音频图像" | 2D 表示：一个轴是频率 bin，另一个是时间帧；每个单元是对数缩放的能量。 |
| Log-mel | "What Whisper sees" | Mel spectrogram passed through log; approximates human perception of loudness. |
| Log-mel | "Whisper 看到的" | 梅尔频谱图取对数；近似人类对响度的感知。 |
| Frame | "One time slice" | A 25 ms window of samples; overlapping at 10 ms stride. |
| 帧 | "一个时间切片" | 25 ms 的采样窗口；10 ms 步长重叠。 |
| Task token | "Prompt prefix for speech" | Special tokens like `<\|transcribe\|>` / `<\|translate\|>` in the decoder prompt. |
| 任务 token | "语音的提示前缀" | 解码器提示中的特殊 token，如 `<\|transcribe\|>` / `<\|translate\|>`。 |
| Voice activity detection (VAD) | "Find the speech" | Gate that removes silence before ASR; cuts cost massively. |
| 语音活动检测 (VAD) | "找到语音" | 在 ASR 之前去除静音的门控；大幅降低成本。 |
| CTC | "Connectionist Temporal Classification" | Classic ASR loss for alignment-free training; Whisper does NOT use it. |
| CTC | "连接主义时间分类" | 经典的 ASR 对齐无关训练损失；Whisper 不使用它。 |
| Whisper-turbo | "Small decoder, full encoder" | large-v3 encoder + 4-layer decoder; 8× faster decoding. |
| Whisper-turbo | "小解码器，全编码器" | large-v3 编码器 + 4 层解码器；解码速度提高 8 倍。 |
| Faster-whisper | "The production wrapper" | CTranslate2 reimplementation; int8 quantization; 4× faster than OpenAI's reference. |
| Faster-whisper | "生产封装器" | CTranslate2 重新实现；int8 量化；比 OpenAI 参考实现快 4 倍。 |

## Mais leitura 延伸阅读

- [Radford et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356)Papel de sussurro.
  Tradução do português:Whisper 论文。
- [OpenAI Whisper repo](https://github.com/openai/whisper) código de referência + peso do modelo.`whisper/model.py`Para ver o código de base Conv1D + codificador + decodificador de cima para baixo em ~ 400 linhas.
  Chinese: OpenAI Whisper 代码仓库, cerca de 400 行代码展示 Conv1D stem + 编码器 + 解码器──
- [OpenAI Whisper — `whisper/decoding.py`](https://github.com/openai/whisper/blob/main/whisper/decoding.py) a lógica de busca de feixe + sinal de tarefa descrita nas etapas 56 está aqui; 500 linhas, totalmente legíveis.
  Tradução do inglês:束搜索 + 任务 token 逻辑的实现,500 行代码,完全可读──
- [Baevski et al. (2020). wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477) precursor; ainda funcionalidades SOTA em algumas configurações.
  O que é que é o "Whisper" é um dos principais traços do "Whisper" em alguns cenários.
- [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) embalagem de produção, 4x mais rápida do que a de referência.
  O que é que é o "sobre-terrorismo"?
- [Jia et al. (2024). Moonshine: Speech Recognition for Live Transcription and Voice Commands](https://arxiv.org/abs/2410.15608) 2024 ASR amigável para bordas, em forma de sussurro, mas menor.
  Chinese: 论文, 2021 年面向边缘的 ASR,类  sussurro, mas更小──
- [HuggingFace blog — "Fine-Tune Whisper For Multilingual ASR with 🤗 Transformers"](https://huggingface.co/blog/fine-tune-whisper) receita de ajuste fino canônico, incluindo pré-processador do espectrograma mel e manuseio de timestamps de tokens.
  Chinese:                                                                                                                                                                                                                                                              
- [HuggingFace `modeling_whisper.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/whisper/modeling_whisper.py) implementação completa (encodeador, decodeador, atenção cruzada, geração) que reflita o diagrama de arquitetura da lição.
  Tradução do inglês para o inglês: HuggingFace Whisper 完整实现(编码器、解码器、交叉注意力、生成),与课程架构图对应──
