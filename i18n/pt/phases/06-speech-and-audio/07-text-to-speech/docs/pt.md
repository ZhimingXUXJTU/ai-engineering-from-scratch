# Text-to-Speech (TTS)  De Tacotron para F5 e Kokoro 语音合成  De Tacotron para F5 e Kokoro

> A ASR inverte fala para texto; TTS inverte texto para fala. A pilha 2026 é de três partes: texto → tokens, tokens → mel, mel → forma de onda. Cada parte tem um modelo padrão que se encaixa em um laptop.

> **【中文解读】**ASR 把语音变文字,TTS 把文字变语音──2026 年的 TTS 技术分三步:文本→token→Mel 频谱→波形──cada passo tem um modelo de execução em seu próprio livro de notas──

> **【拓展：TTS 的应用】**TTS é uma técnica central, que é uma técnica de comunicação e comunicação, que é uma técnica de comunicação e comunicação.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 09 (Seq2Seq), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 09（Seq2Seq），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## O problema é o problema da introdução

Você tem uma corda: "Por favor, lembre-me de regar as plantas às 18h". Você precisa de um vídeo de áudio de 3 segundos que soa natural, tem prosodia correta (pausas, estresse), pronuncia "plantes" com a vogais certas e corre em menos de 300 ms em uma CPU para um assistente de voz ao vivo. Você também precisa trocar vozes, lidar com entradas com código-switched ("lembrem-me às 18h, daijoubu?"), e não se envergonhar em nomes.

> Você tem um字符串:"Por favor, lembre-me de regar as plantas às 18h". Você precisa de um período de 3 segundos de audio, "Legue natural,律正确(停顿、重音), "plantes" de元音发音正确, e em CPU não chega a 300 ms, em que você pode operar para usar em tempo real.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

Os oleodutos modernos TTS parecem assim:

> 现代 TTS 流水线如下:

1. **Text frontend.**Normalize texto (datas, números, e-mails), converta em fonemas ou tokens de subpalavras, prevê recursos de prosodia.
   **文本前端。**归一化文本(日期、数字、邮箱),转换为音素或子词代币,预测律特征──
2. **Acoustic model.**Texto → mel espectrograma. Tacotron 2 (2017), FastSpeech 2 (2020), VITS (2021), F5-TTS (2024), Kokoro (2024).
   **声学模型。**文本 → Mel 频谱图──Tacotron 2(2017)、FastSpeech 2(2020)、VITS(2021)、F5-TTS(2024)、Kokoro(2024)。
3. **Vocoder.**Mel → forma de onda. WaveNet (2016), WaveRNN, HiFi-GAN (2020), BigVGAN (2022), vocoders de codec neural em 2024+.
   **声码器。**Mel → 波形──WaveNet(2016)、WaveRNN、HiFi-GAN(2020)、BigVGAN(2022)、2024+ 的神经编解码声码器──

Em 2026, o vocalista acústico + vocal divide-se com modelos de difusão de ponta a ponta e de correspondência de fluxo.

> Em 2026, com a aparição de um modelo de expansão e de fluxo de correspondência, as fronteiras entre o modelo sonoro e o codificador sonoro ficam obscuras.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![Tacotron, FastSpeech, VITS, F5/Kokoro side-by-side](../assets/tts.svg)

**Tacotron 2 (2017).**Seq2seq: car-embedding → BiLSTM encoder → atenção localização sensível → autoregressivo LSTM decoder emite molduras mel. Lento (AR), vacilante em texto longo. Ainda citado como uma linha de base.

> **Tacotron 2（2017）。**Seq2seq:字符嵌入 → BiLSTM 编码器 → 位置敏感注意力 → 自归 LSTM 解码器输出 mel ──慢(AR),长文本不稳定── ainda são citados为基线──

**FastSpeech 2 (2020).**Não autoregressivo. Preditor de duração emitir quantas molduras mel cada fonema recebe. 1 pass, 10x mais rápido que Tacotron. Perde alguma naturalidade (alinhamento monótono) mas navega em todos os lugares.

> **FastSpeech 2（2020）。**Não-auto-regressão──时长预测器输出每音素获得多少 mel ──单次前向,比塔科特龙快10倍──损失一些自然度(单调对齐)

**VITS (2021).**Juntamente treina codificador + duração baseada em fluxo + vocoder de extremo a extremo HiFi-GAN com inferência variável. Alta qualidade, modelo único. TTS de código aberto dominante 20222024. Variantes: YourTTS (multiplicador zero-shot), XTTS v2 (2024, Coqui).

> **VITS（2021）。**联合训练编码器 + 基流的时长预测 + HiFi-GAN 声码器端到端,使用变分推断。高质量,单模型──2022-2024年主导开源 TTS──变体:YourTTS(多说话人零样本)、XTTS v2(2024,Coqui)──

**F5-TTS (2024).**Transformador de difusão sobre a correspondência de fluxo. Prósodia natural, clonagem de voz de tiro zero com 5 segundos de áudio de referência.

> **F5-TTS（2024）。**Baseada em fluidismo, distribuição e distribuição de dados.

**Kokoro (2024).**Pequeno (82M), executável pela CPU, melhor TTS de inglês para uso em tempo real.

> **Kokoro（2024）。**Por exemplo, o sistema operacional Apache 2.0 pode ser executado em qualquer formato de computador.

**OpenAI TTS-1-HD, ElevenLabs v2.5, Google Chirp-3.**ElevenLabs v2.5 emoção tags ("[suspirado]", "[risos]") e vozes de personagens dominam a produção de livros de áudio em 2026.

> **OpenAI TTS-1-HD、ElevenLabs v2.5、Google Chirp-3。**商业 SOTA──ElevenLabs v2.5 的情感标签("[ sussurrou]"、"[risos]")和角色声音主导 2026 年有声书制作──

### Evolução do vocoder

> ### O que é que é isso?

| Era | Vocoder | Latency | Quality |
|-----|---------|---------|---------|
| 2016 | WaveNet | offline only | SOTA at release |
| 2018 | WaveRNN | ~realtime | good |
| 2020 | HiFi-GAN | 100× realtime | near-human |
| 2022 | BigVGAN | 50× realtime | generalizes across speakers/langs |
| 2024 | SNAC, DAC (neural codecs) | integrated with AR models | discrete tokens, bit-efficient |

| 时代 | 声码器 | 延迟 | 质量 |
|------|--------|------|------|
| 2016 | WaveNet | 仅离线 | 发布时 SOTA |
| 2018 | WaveRNN | 约实时 | 良好 |
| 2020 | HiFi-GAN | 100× 实时 | 接近人类 |
| 2022 | BigVGAN | 50× 实时 | 跨说话人/语言泛化 |
| 2024 | SNAC, DAC（神经编解码器） | 与 AR 模型集成 | 离散 token，比特高效 |

Em 2026, a maioria dos modelos "TTS" são end-to-end de texto para forma de onda; o espectrograma mel é uma representação interna.

> Até 2026, a maioria dos modelos "TTS" é de texto a forma de onda de modelo de extremo a extremo; o gráfico de frequência é o indicado interno.

### Avaliação

> ###  avaliação

- **MOS (Mean Opinion Score).**Escala de 1 a 5, de fontes públicas, ainda o padrão ouro, dolorosamente lento.
  **MOS（平均意见分）。**1-5 分量表,众包── ainda é o padrão de ouro; velocidade dolorosamente lenta──
- **CMOS (Comparative MOS).**Preferência A versus B. Intervalos de confiança mais estreitos por anotação.
  **CMOS（比较 MOS）。**A-vs-B  preferência.
- **UTMOS, DNSMOS.**Predutores neurais de MOS sem referência, usados para rankings.
  **UTMOS、DNSMOS。**无参考神经 MOS 预测器──用于排行榜──
- **CER (Character Error Rate) via ASR.**Execute a saída TTS através do Whisper, computa o CER contra o texto de entrada.
  **CER（字符错误率）通过 ASR。**Para a sua produção, o TTS é um indicador de controle de dados.
- **SECS (Speaker Embedding Cosine Similarity).**Qualidade de clonagem de voz.
  **SECS（说话人嵌入余弦相似度）。**O que é que é que é?

Números 2026 da limpeza de ensaio LibriTTS:

> 2026 ano LibriTTS teste-limpo 上的数字:

| Model | UTMOS | CER (via Whisper) | Size |
|-------|-------|-------------------|------|
| Ground truth | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 335M |
| XTTS v2 | 3.81 | 3.5% | 470M |
| VITS | 3.62 | 3.1% | 25M |
| Kokoro v0.19 | 3.87 | 1.8% | 82M |
| Parler-TTS Large | 3.76 | 2.8% | 2.3B |

| 模型 | UTMOS | CER（通过 Whisper） | 大小 |
|------|-------|---------------------|------|
| 真实音频 | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 3.35 亿 |
| XTTS v2 | 3.81 | 3.5% | 4.7 亿 |
| VITS | 3.62 | 3.1% | 2500 万 |
| Kokoro v0.19 | 3.87 | 1.8% | 8200 万 |
| Parler-TTS Large | 3.76 | 2.8% | 23 亿 |

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.




## Construí-lo e realizei-o.
```figure
sp-tts-stack
```

## Construí-lo

### Passo 1: fonemizar a entrada

```python
from phonemizer import phonemize
ph = phonemize("Hello world", language="en-us", backend="espeak")
# 'həloʊ wɜːld'
```

Os fonemas são a ponte universal. Evite alimentar texto bruto a qualquer coisa abaixo do nível de qualidade do VITS.

> 音素是通用桥梁──避免将原始文本输入到VITS 级别以下的任何模型──

### Passo 2: executar Kokoro (2026 CPU padrão)

```python
from kokoro import KPipeline
tts = KPipeline(lang_code="a")  # "a" = American English
audio, sr = tts("Please remind me to water the plants at 6 pm.", voice="af_bella")
# audio: float32 tensor, sr=24000
```

Funciona offline, único arquivo, 82M params.

> O que é o "Caso de Operação" ?

### Passo 3: executar F5-TTS com clonagem de voz

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="my_voice_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please remind me to water the plants.",
)
```

Passe um clipe de referência de 5 segundos + sua transcrição; F5 clona prosodia e timbre.

> 传入 5 秒参考音频 + 其转录文本;F5 克隆律和音色──

### Passo 4: Vocoder HiFi-GAN a partir do zero

Muito grande para caber num guião de tutorial, mas a forma é:

```python
class HiFiGAN(nn.Module):
    def __init__(self, mel_channels=80, upsample_rates=[8, 8, 2, 2]):
        super().__init__()
        # 4 upsample blocks, total 256x to go from mel-rate to audio-rate
        ...
    def forward(self, mel):
        return self.blocks(mel)  # -> waveform
```

Formação: adversária (discriminador em janelas curtas) + perda de reconstrução do espectrograma mel + perda de correspondência de características.`hifi-gan`repo ou nvidia-neMo.

> 訓練:对抗式(短窗口判别器) + Mel 频谱图重建损失 + 特征匹配损失──已商品化使用 `hifi-gan`倉庫或nvidia-NeMo 的预训练检查点──

### Passo 5: o conjunto completo do gasoduto (pseudo-código)

```python
text = "Please remind me at 6 pm."
phones = phonemize(text)
mel = acoustic_model(phones, speaker=alice)      # [T, 80]
wav = vocoder(mel)                                # [T * 256]
soundfile.write("out.wav", wav, 24000)
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.





> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

A pilha de 2026:

> Tecnologia de 2026:

| Situation | Pick |
|-----------|------|
| Real-time English voice assistant | Kokoro (CPU) or XTTS v2 (GPU) |
| Voice cloning from 5 s reference | F5-TTS |
| Commercial character voices | ElevenLabs v2.5 |
| Audiobook narration | ElevenLabs v2.5 or XTTS v2 + fine-tune |
| Low-resource language | Train VITS on 5–20 h target-lang data |
| Expressive / emotion tags | ElevenLabs v2.5 or StyleTTS 2 fine-tune |

| 场景 | 选择 |
|------|------|
| 实时英文语音助手 | Kokoro（CPU）或 XTTS v2（GPU） |
| 5 秒参考音频声音克隆 | F5-TTS |
| 商业角色声音 | ElevenLabs v2.5 |
| 有声书朗读 | ElevenLabs v2.5 或 XTTS v2 + 微调 |
| 低资源语言 | 在 5-20 小时目标语言数据上训练 VITS |
| 表达性 / 情感标签 | ElevenLabs v2.5 或 StyleTTS 2 微调 |

Líder de código aberto a partir de 2026: **F5-TTS for quality, Kokoro for efficiency**Não busques o Tacotron a menos que seja um historiador.

> 2026                                                                                                                                                                                                                                                              **F5-TTS 追求质量，Kokoro 追求效率**Se não és um historiador, não usem o Tacotron.



## Encurralagens

> 常见陷

- **No text normalizer.**"Dr. Smith" diz "Doutor" ou "Drive"? "2026" diz "vinte e vinte e seis" ou "dois zero dois seis"?
  **没有文本归一化器。**"Dr. Smith" 读成"Doctor"还是"Drive"?"2026"读成"twenty twenty six"还是"two zero two six"?在音素化之前归一化──
- **OOV proper nouns.**"Ghumare" → "ghyu-mair"? Enviar um modelo de fallback grapheme-to-phoneme para tokens desconhecidos.
  **OOV 专有名词。**"Ghumare" → "ghyu-mair"?
- **Clipping.**A saída do vocoder raramente é clipe, mas a descoincidência de escalação mel na inferência pode ultrapassar ±1,0.`np.clip(wav, -1, 1)`- Não .
  **削波。**声码器输出很少削波,但推理时 Mel 缩放不匹配可能超出 ±1.0──始终使用 `np.clip(wav, -1, 1)`- Não.
- **Sample-rate mismatch.**Kokoro produz 24 kHz; o seu pipeline aguardando 16 kHz → re-sampulação ou obter aliasing.
  **采样率不匹配。**Kokoro 输出 24 kHz; 你的下游流水线期望 16 kHz → 重采样否则产生混叠──

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-tts-designer.md`. Desenhar um canal TTS para um determinado alvo de voz, latência e linguagem.

> 保存为 `outputs/skill-tts-designer.md`◊ Para um determinado som、延迟和语言目标设计 TTS 流水线──

## Exercícios.

1. **Easy.**Corra .`code/main.py`Construi um dicionário fonético a partir de um vocabulário de brinquedo, estima a duração por fonema e imprime um cronograma falso de "mel".
   **简单。**运行 `code/main.py` From toy tool word表                                                                                                                                                                                                                                                            
2. **Medium.**Instale Kokoro, sintetize a mesma frase com voz.`af_bella`E ...`am_adam`Comparar a duração do áudio e a qualidade subjetiva.
   **中等。**Anúncio de Kokoro, usá-lo`af_bella`和 `am_adam`音合成同一句话──比较音频时长和主观质量──
3. **Hard.**Grave um clip de referência de 5 segundos de si mesmo, use o F5-TTS para cloná-lo, informe o SECS entre a referência e a saída clonada.
   **困难。**录制一段 5 seconds of自已的参考音频──使用F5-TTS 克隆──报告参考与克隆输出之间的SECS──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Phoneme | Sound unit | Abstract sound class; 39 in English (ARPABet). |
| Duration predictor | How long each phoneme lasts | Non-AR model output; integer frames per phoneme. |
| Vocoder | Mel → waveform | Neural net mapping mel-spec to raw samples. |
| HiFi-GAN | Standard vocoder | GAN-based; dominant 2020–2024. |
| MOS | Subjective quality | 1–5 mean opinion score from human raters. |
| SECS | Voice-clone metric | Cosine similarity between target and output speaker embedding. |
| F5-TTS | 2024 open-source SOTA | Flow-matching diffusion; zero-shot cloning. |
| Kokoro | CPU English leader | 82M-param model, Apache 2.0. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 音素 | 声音单位 | 抽象声音类别；英文有 39 个（ARPABet）。 |
| 时长预测器 | 每个音素持续多久 | 非自回归模型输出；每个音素的整数帧数。 |
| 声码器 | Mel → 波形 | 将 mel 频谱映射为原始采样的神经网络。 |
| HiFi-GAN | 标准声码器 | 基于 GAN；2020-2024 年主导。 |
| MOS | 主观质量 | 人工评分员的 1-5 平均意见分。 |
| SECS | 声音克隆指标 | 目标与输出说话人嵌入之间的余弦相似度。 |
| F5-TTS | 2024 开源 SOTA | 流匹配扩散；零样本克隆。 |
| Kokoro | CPU 英文领导者 | 8200 万参数模型，Apache 2.0。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Shen et al. (2017). Tacotron 2](https://arxiv.org/abs/1712.05884) a linha de base de seguimento.
  Shen 等 (2017). Tacotron 2seq2seq 基线。
- [Kim, Kong, Son (2021). VITS](https://arxiv.org/abs/2106.06103) baseado em fluxos de ponta a ponta.
  Kim, Kong, Son (2021). VITS端到端基于流的模型──
- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885) SOTA de código aberto atual.
  Chen 等 (2024). F5-TTS 当前开源SOTA──
- [Kong, Kim, Bae (2020). HiFi-GAN](https://arxiv.org/abs/2010.05646)O vocoder que ainda vai para 2026.
  Kong, Kim, Bae (2020).
- [Kokoro-82M on HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M) 2024 TTS Inglês com CPU-friendly.
  Kokoro-82M 在 HuggingFace 上2024年 CPU 友好的英文 TTS。

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

