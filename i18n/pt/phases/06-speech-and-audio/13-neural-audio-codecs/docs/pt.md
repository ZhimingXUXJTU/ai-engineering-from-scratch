# Neural Audio Codecs  EnCodec, SNAC, Mimi, DAC e a separação semântica-acústica

> A geração de áudio 2026 é quase todos os tokens. EnCodec, SNAC, Mimi e DAC transformam formas de onda contínuas em sequências discretas que um transformador pode prever.

> **【中文解读】**A geração de tóquos de som em 2026 é baseada em tokens. EnCodec, SNAC, Mimi, DAC irá continuar a transformar-se em sequências de separação, permitindo que o transformador possa prever.

> **【拓展：音频 token 化】**Assim, o texto tem um tokenizer BPE, o texto se transforma em token, o audio tem um EnCodec, etc.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 10 · 11 (Quantization), Phase 5 · 19 (Subword Tokenization) | **前置知识:** 阶段 6 · 02（频谱图），阶段 10 · 11（量化），阶段 5 · 19（子词分词）
**Time:** ~60 minutes | **预计用时:** ~60 分钟

## O problema é o problema da introdução

Os modelos de linguagem funcionam em tokens discretos. O áudio é contínuo. Se você quiser um modelo de estilo LLM para fala / música  MusicGen, Moshi, Sesame CSM, VibeVoice, Orpheus  primeiro precisa de um **neural audio codec**: um codificador aprendido que discretece o áudio em um pequeno vocabulário de tokens, e um decodificador correspondente que reconstrui a forma de onda.

> 语言模型处理离散 token──音频是连续的── Se você quiser construir um modelo de Mestrado em Música 音乐Gen、Moshi、Sesame CSM、VibeVoice、Orpheus你首先需要一个**神经音频编解码器**Um codificador de aprendizagem irá disseminar o seu som em um token de pequeno valor, adicionando o seu código de aprendizagem ao seu formato.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

Duas famílias surgiram:

> Já surgiram duas famílias:

1. **Reconstruction-first codecs** EnCodec, DAC. Optimize a qualidade de áudio perceptual. Tokens são "acousticos"  eles capturam tudo, incluindo a identidade do alto-falante, timbre, ruído de fundo.
   **重建优先编解码器**EnCodec、DAC──优化感知音频质量──Token é "aosênico"它们捕获一切, incluindo a fala de alguém身份、音色、背景噪声──
2. **Semantic-first codecs**Mimi (Kyutai), SpeechTokenizer. Forçar o primeiro código-book a codificar conteúdo linguístico / fonético (muitas vezes destilar a partir de WavLM).
   **语义优先编解码器**Mimi(Kyutai)、SpeechTokenizer。强制第一码本编码语言/语音内容(normalmente através do WavLM 蒸)。后续码本是声学细节。

A perspectiva de 2024-2026: **a pure reconstruction codec gives you blurry speech when you try to generate from text.**O LLM sobre tokens de codec tem que aprender tanto a estrutura de linguagem quanto a estrutura acústica no mesmo livro de código, o que não é escalado.

> Intuição de 2024-2026:**纯重建编解码器在从文本生成时给你模糊的语音。**O Mestrado em Língua e Língua (LLM) deve ser desenvolvido simultaneamente no mesmo código, o que não pode ser expandido.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![Four codec landscape: EnCodec, DAC, SNAC (multi-scale), Mimi (semantic+acoustic)](../assets/codec-comparison.svg)

### O truque principal: Quantização de VECTORES RESIDUALES (RVQ)

Em vez de um grande livro de códigos (que precisaria de milhões de códigos para uma boa qualidade), todos os códigos de áudio modernos usam **RVQ**O primeiro livro quantiza a saída do codificador; o segundo quantiza o residual; etc. Cada livro de códigos é de 1024 códigos.

> Em vez de usar um código grande, todos os modernos usuários usam**RVQ**O primeiro código é o de um código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código

No momento da inferência, o decodificador soma todos os códigos escolhidos por quadro para reconstruir.

>  Quando se propõe, o descifrador irá buscar todos os códigos de cada seleção e reedificar os seus volumes.

### Os quatro codecs que importam em 2026

**EnCodec (Meta, 2022).**A linha de base. Encoder-decoder sobre a forma de onda, garganta de engarrafamento RVQ. 24 kHz, 32 codesbooks possíveis, padrão 4 codesbooks @ 1,5 kbps. Utilizações `1D conv + transformer + 1D conv`- Usado pela MusicGen.

> **EnCodec（Meta，2022）。**基线──波形上的编码器-解码器,RVQ 瓶──24 kHz, máximo 32 个码本,默认 4 个码本 @ 1.5 kbps──使用 `1D conv + transformer + 1D conv`架构──MusicGen Uso──

**DAC (Descript, 2023).**RVQ com livros de código L2-normalizados, funções de ativação periódica, perdas melhoradas. A maior fidelidade de reconstrução de qualquer codec aberto  às vezes indistinguível do discurso original com 12 livros de código. 44,1 kHz banda completa.

> **DAC（Descript，2023）。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

**SNAC (Hubert Siuzdak, 2024).**Os livros de código grosseiros operam a uma taxa de quadros mais baixa do que os finos. Modelagem eficazmente o áudio hierárquicamente: um "esquiz" grosseiro a ~ 12 Hz mais detalhes a 50 Hz. Usado por Orpheus-3B porque a estrutura hierárquica mapeia bem a geração baseada em LM.

> **SNAC（Hubert Siuzdak，2024）。**Multi-dimensional RVQ grosso código foi usado em comparação com o pequeno código foi usado em uma taxa de operação menor.

**Mimi (Kyutai, 2024).**O 2026 game-changer. 12,5 Hz freqüência de quadros (extremamente baixo), 8 codes @ 4,4 kbps.**distilled from WavLM**Os livros de código 1-7 são resíduos acústicos. Esta divisão alimenta Moshi (Lessão 15) e Sesame CSM.

> **Mimi（Kyutai，2024）。**2026 年代 变更者──12.5 Hz 率(极低),8 个码本 @ 4.4 kbps──码本 0 **从 WavLM 蒸馏** treinamento para prever os caracteres do som da onda. 码本 1-7 é o resíduo da voz.

### As frequências de quadros são importantes para a modelagem de linguagem

Taxa de quadros mais baixa = sequência mais curta = LM mais rápido.

> 率对语言建模很重要: 率越低 = 序列越短 = LM 越快──

| Codec | Frame rate | 1 s = N frames | Good for |
|-------|-----------|----------------|---------|
| EnCodec-24k | 75 Hz | 75 | music, general audio |
| DAC-44.1k | 86 Hz | 86 | high-fidelity music |
| SNAC-24k (coarse) | ~12 Hz | 12 | AR-LM efficient |
| Mimi | 12.5 Hz | 12.5 | streaming speech |

| 编解码器 | 帧率 | 1 秒 = N 帧 | 适用场景 |
|---------|------|------------|---------|
| EnCodec-24k | 75 Hz | 75 | 音乐、通用音频 |
| DAC-44.1k | 86 Hz | 86 | 高保真音乐 |
| SNAC-24k（粗） | ~12 Hz | 12 | AR-LM 高效 |
| Mimi | 12.5 Hz | 12.5 | 流式语音 |

A 12,5 Hz, uma declaração de 10 segundos é apenas 125 quadros de codec  um transformador pode facilmente predizê-los.

> Em 12,5 Hz, apenas 125 palavras são faciais.

### Tokens semânticos versus acústicos

> 语义 vs 声学 token

```
frame_t → [semantic_token_t, acoustic_token_0_t, acoustic_token_1_t, ..., acoustic_token_6_t]
```

- **Semantic token (codebook 0 in Mimi).**Encode o que foi dito  fonemas, palavras, conteúdo. Distilado a partir de WavLM através de uma perda de previsão auxiliar.
  **语义 token（Mimi 中的码本 0）。**编码说了什么音素、单词、内容──通过辅助预测损失从波LM 蒸──
- **Acoustic tokens (codebooks 1-7).**Timbre de encódigo, identidade do alto-falante, prosodia, ruído de fundo, detalhes finos.
  **声学 token（码本 1-7）。**编码音色、说话人身份、律、背景噪音、精细细节──

Um LM AR prevê o token semântico primeiro (condicionado em texto), em seguida, prevê tokens acústicos (condicionado em referência semântica + alto-falantes). Esta fatorização é por que o TTS moderno pode clonar vozes de tiro zero: o modelo semântico lida com conteúdo; o modelo acústico lida com timbre.

> Autorecordando LM, previo previo previo语义 token ((以文本为条件),再预测声学 token ((以语义 + 说话人参考为条件) ・・・ esse desintegração é o moderno TTS 能够零样本克隆声音的原因:语义模型处理内容,声学模型处理音色。

### 2026 Qualidade de reconstrução (bits por segundo, menor bitrate é melhor)

| Codec | Bitrate | PESQ | ViSQOL |
|-------|---------|------|--------|
| Opus-20kbps | 20 kbps | 4.0 | 4.3 |
| EnCodec-6kbps | 6 kbps | 3.2 | 3.8 |
| DAC-6kbps | 6 kbps | 3.5 | 4.0 |
| SNAC-3kbps | 3 kbps | 3.3 | 3.8 |
| Mimi-4.4kbps | 4.4 kbps | 3.1 | 3.7 |

| 编解码器 | 比特率 | PESQ | ViSQOL |
|---------|--------|------|--------|
| Opus-20kbps | 20 kbps | 4.0 | 4.3 |
| EnCodec-6kbps | 6 kbps | 3.2 | 3.8 |
| DAC-6kbps | 6 kbps | 3.5 | 4.0 |
| SNAC-3kbps | 3 kbps | 3.3 | 3.8 |
| Mimi-4.4kbps | 4.4 kbps | 3.1 | 3.7 |

Os codecs tradicionais como o Opus ainda ganham por bit na qualidade perceptiva.**discrete tokens**(que a Opus não produz) e **generative-model quality**(o que o LM pode fazer com esses tokens).

> 傳統編解碼器 (Opus) em cada bits de perceção qualidade ainda venceu.**离散 token**(Opus não produz)**生成模型质量**(LM 能用这些符号做什么) 上胜出.

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.



## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

```figure
rvq-codec-cascade
```

## Construí-lo

### Passo 1: codificar com EnCodec

```python
from encodec import EncodecModel
import torch

model = EncodecModel.encodec_model_24khz()
model.set_target_bandwidth(6.0)  # kbps

wav = torch.randn(1, 1, 24000)
with torch.no_grad():
    encoded = model.encode(wav)
codes, scale = encoded[0]
# codes: (1, n_codebooks, n_frames), dtype=int64
```

`n_codebooks=8`Cada código é 0-1023 (10 bits).

> 6 kbps`n_codebooks=8` Cada código de valor 0-1023  10 比特) 

### Passo 2: decodificação e medida da reconstrução

```python
with torch.no_grad():
    wav_recon = model.decode([(codes, scale)])

from torchaudio.functional import compute_deltas
import torch.nn.functional as F

mse = F.mse_loss(wav_recon[:, :, :wav.shape[-1]], wav).item()
```

### Passo 3: a divisão semântica-acústica (estilo Mimi)

```python
from moshi.models import loaders
mimi = loaders.get_mimi()

with torch.no_grad():
    codes = mimi.encode(wav)  # shape (1, 8, frames@12.5Hz)

semantic = codes[:, 0]
acoustic = codes[:, 1:]
```

O livro de código semântico 0 é alinhado com o WavLM. Você pode treinar um transformador de texto para semântica  vocabulário muito menor do que ir diretamente para áudio.

> 语义码本 0 与 WavLM 对齐──你可以训练一个文本→语义 Transformer词表比直接到音频小得多──然后一个独立的声学→波形解码器以说话人参考为条件──

### Passo 4: por que o AR LM sobre tokens de codec funciona

Para um clip de fala de 10 segundos nos livros de códigos de Mimi de 12,5 Hz × 8:

```
N_tokens = 10 * 12.5 * 8 = 1000 tokens
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


1000 tokens é um contexto trivial para um transformador. Um transformador de parâmetro de 256M pode gerar 10 segundos de fala em milissegundos em uma GPU moderna.

> 1000 tokens para o Transformer são insignificantes para cima e para baixo. Um Transformer de 2,56 bilhões de parâmetros em GPUs modernos pode gerar 10 segundos de voz em poucos segundos.




> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

Problema de mapa → codec:

| Task | Codec |
|------|-------|
| General music generation | EnCodec-24k |
| Highest-fidelity reconstruction | DAC-44.1k |
| AR LM over speech (TTS) | SNAC or Mimi |
| Streaming full-duplex speech | Mimi (12.5 Hz) |
| Sound-effect library with text | EnCodec + T5 condition |
| Fine-grained audio editing | DAC + inpainting |

| 任务 | 编解码器 |
|------|---------|
| 通用音乐生成 | EnCodec-24k |
| 最高保真重建 | DAC-44.1k |
| 语音上的 AR LM（TTS） | SNAC 或 Mimi |
| 流式全双工语音 | Mimi（12.5 Hz） |
| 文本驱动的音效库 | EnCodec + T5 条件 |
| 细粒度音频编辑 | DAC + 内画 |

Regra geral: **if you're building a generative model, start with Mimi or SNAC. If you're building a compression pipeline, use Opus.**

> 经验法则:**如果你在构建生成模型，从 Mimi 或 SNAC 开始。如果在构建压缩流水线，使用 Opus。**



## Encurralagens

- **Too many codebooks.**Adicionar cédulos aumenta a fidelidade linearmente mas o comprimento da sequência LM também linearmente.
  **码本过多。**A maior parte dos números de um grupo de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos
- **Frame-rate mismatch.**O treinamento LM em 12,5 Hz Mimi, depois o ajuste fino em 50 Hz EnCodec falha silenciosamente.
  **帧率不匹配。**Em 12,5 Hz Mimi 上訓練 LM, então em 50 Hz EnCodec 上微调会静默失败.
- **Assuming all codebooks equal.**No Mimi, o código 0 carrega conteúdo; perdê-lo destrói a inteligibilidade.
  **假设所有码本同等重要。**Em Mimi, código-fonte 0 carrega o conteúdo; perder-se-á destruindo a compreensão.
- **Using reconstruction quality as the only metric.**Um codec pode ter uma grande reconstrução, mas não é útil para a geração baseada em LM se a estrutura semântica for ruim.
  **仅用重建质量作为唯一指标。**Um codificador pode reconstruir a qualidade muito boa, mas se a estrutura de linguagem for diferente, não há necessidade de gerar baseada em LM.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-codec-picker.md`Escolha um codec para uma determinada tarefa de geração ou compressão.

> 保存为 `outputs/skill-codec-picker.md` para uma determinada tarefa de produção ou compressão

## Exercícios.

1. **Easy.**Corra .`code/main.py`Implementa um quantificador de brinquedo escalar + residual e mede o erro de reconstrução ao adicionar livros de código.
   **简单。**运行 `code/main.py` Realizou um marcador de brinquedos + restar diferencial, medindo com o aumento do código de erro de reconstrução
2. **Medium.**Instalação`encodec`Comparar 1, 4, 8, 32 codesbook em um clip de fala prolongado.
   **中等。**Instalação`encodec`, em deixarem um vídeo em que comparem 1⁄4, 8⁄32 个码本── desenhar PESQ ou MSE vs 比特率──
3. **Hard.**Carregar Mimi. Encode um clip. Substitua o código 0 por números inteiros aleatórios; decode. Então substitua o código 7 de forma semelhante. Compare as duas corrupções  Corrupção do código 0 deve destruir a inteligibilidade; Corrupção do código 7 deve apenas mudar nada.
   **困难。**Caso não seja possível, o número de usuários deve ser alterado.

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| RVQ | Residual quantization | Cascade of small codebooks; each quantizes the previous residual. |
| Frame rate | Codec speed | How many token-frames per second. Lower = faster LM. |
| Semantic codebook | Codebook 0 (Mimi) | Codebook distilled from SSL features; encodes content. |
| Acoustic codebooks | Everything else | Timbre, prosody, noise, fine detail. |
| PESQ / ViSQOL | Perceptual quality | Objective metrics correlating with MOS. |
| EnCodec | Meta codec | The RVQ baseline; used by MusicGen. |
| Mimi | Kyutai codec | 12.5 Hz frame rate; semantic-acoustic split; powers Moshi. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| RVQ | 残差量化 | 小码本级联；每个量化前一个残差。 |
| 帧率 | 编解码器速度 | 每秒多少 token 帧。越低 = LM 越快。 |
| 语义码本 | 码本 0（Mimi） | 从 SSL 特征蒸馏的码本；编码内容。 |
| 声学码本 | 其余所有 | 音色、韵律、噪声、精细细节。 |
| PESQ / ViSQOL | 感知质量 | 与 MOS 相关的客观指标。 |
| EnCodec | Meta 编解码器 | RVQ 基线；MusicGen 使用。 |
| Mimi | Kyutai 编解码器 | 12.5 Hz 帧率；语义-声学分离；驱动 Moshi。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Défossez et al. (2023). EnCodec](https://arxiv.org/abs/2210.13438) a linha de base do RVQ.
  Défossez 等 (2023). EnCodecRVQ 基线。
- [Kumar et al. (2023). Descript Audio Codec (DAC)](https://arxiv.org/abs/2306.06546)- A mais alta fidelidade aberta.
  Kumar 等 (2023). DAC最高保真开源编解码器
- [Siuzdak (2024). SNAC](https://arxiv.org/abs/2410.14411) RVQ em larga escala.
  Siuzdak (2024). SNAC多尺度 RVQ──
- [Kyutai (2024). Mimi codec](https://kyutai.org/codec-explainer) separação semântica-acústica, destilação WavLM.
  Kyutai (2024). Mimi 编解码器语义-声学分离,WavLM 蒸──
- [Borsos et al. (2023). AudioLM](https://arxiv.org/abs/2209.03143) o paradigma semântico/acústico de dois estágios.
  Borsos 等 (2023). AudioLM两阶段语义/声学范式──
- [Zeghidour et al. (2021). SoundStream](https://arxiv.org/abs/2107.03312) o código RVQ original streamable.
  Zeghidour etc (2021). SoundStream原始可流式 RVQ 编解码器──

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

