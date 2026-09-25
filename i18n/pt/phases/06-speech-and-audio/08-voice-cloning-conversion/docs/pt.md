# Clonagem de voz e conversão de voz .

> A clonagem de voz lê o seu texto na voz de outra pessoa. A conversão de voz reescreve a sua voz para a de outra pessoa, preservando o que você disse. Ambos dependem da mesma decomposição: a identidade do alto-falante separada do conteúdo.

> **【中文解读】**语音克隆 usar a voz de outra pessoa para ler suas palavras;语音转换把你的声音变成别人的但保留内容── ambos são fundamentais na mesma decomposição:将说话人身份与内容分离──

> **【拓展：语音克隆的伦理与法律】**语音克隆技术引发严重伦理和法律问题深度伪造语音诈骗、名人声音未经授权使用──2025-2026多年起诉案(如华纳音乐 5 亿美元和解案) impulsionou o desenvolvimento da tecnologia de áudio e contrafalsificação──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 06 (Speaker Recognition), Phase 6 · 07 (TTS) | **前置知识:** 阶段 6 · 06（说话人识别），阶段 6 · 07（TTS）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## O problema é o problema da introdução

Em 2026, um clip de áudio de 5 segundos é suficiente para produzir um clone de alta qualidade da voz de qualquer pessoa com uma GPU de consumo. ElevenLabs, F5-TTS, OpenVoice v2, VoiceBox todos enviam clonagem de zero-shot ou poucos-shot. A tecnologia é uma bênção (acessibilidade TTS, dobramento, vozes de assistência) e uma arma (chamadas de fraude, deepfakes políticos, roubo de IP).

> 2026 年,一段 5 秒音频就足以使用消费级 GPU 高质量克隆任何人的声音──ElevenLabs、F5-TTS、OpenVoice v2、VoiceBox 都提供零样本或少样本克隆── esta tecnologia é uma arma, também é uma arma, também é uma arma, também é uma fraude telefónica, uma falsidade política, um roubo de direitos de propriedade intelectual.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

Duas tarefas estreitamente relacionadas:

> Duas missões estreitamente relacionadas:

- **Voice cloning (TTS-side):**texto + 5 segundos de voz de referência → áudio nessa voz.
  **声音克隆（TTS 侧）：**文本 + 5 秒参考音 → The sound of the audio.
- **Voice conversion (speech-side):**Áudio fonte (pessoal A dizendo X) + voz de referência da pessoa B → áudio de B dizendo X.
  **语音转换（语音侧）：**源音频(说话人 A 说 X) + 说话人 B 的参考声音 → B 说 X 的音频。

Ambos factorizam uma forma de onda em (conteúdo, alto-falantes, prosódias) e recombinam conteúdo de uma fonte com alto-falantes de outra.

> 都将波形分解为(内容、说话人、律) 并从一个来源取内容与另一来源的说话人重新组合──

Uma restrição chave que agora se submeterá em 2026:**watermarking and consent gates are legally required in the EU (AI Act, enforceable August 2026) and in California (AB 2905, effective 2025)**O seu gasoduto deve emitir uma marca de água inaudivel e recusar clones não consensuais.

> 2026 ano que você enfrenta:**水印和同意门在 EU（AI 法案，2026 年 8 月生效）和加利福尼亚州（AB 2905，2025 年生效）是法律要求的**O seu fluxo de água deve emitir impressões inaudibles e rejeitar o seu consentimento.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![Voice cloning vs conversion: factorize, swap speaker, recombine](../assets/voice-cloning.svg)

**Zero-shot cloning.**Passe um clip de 5 segundos para um modelo que foi treinado em milhares de alto-falantes. O codificador de alto-falantes mapeia o clip para um integrador de alto-falantes; o decodificador TTS condiciona essa incorporação mais texto.

> **零样本克隆。**Transmitir 5 segundos de rádio para um modelo treinado por mil pessoas.

Usado por: F5-TTS (2024), YourTTS (2022), XTTS v2 (2024), OpenVoice v2 (2024).

> Utilizador:F5-TTS(2024)、YourTTS(2022)、XTTS v2(2024)、OpenVoice v2(2024)。

**Few-shot fine-tuning.**Gravar 5-30 minutos da voz alvo. LoRA-fine-tune um modelo base por uma hora. Qualidade salta de "okay" para "indistinguible". Coqui e ElevenLabs ambos suportam este padrão; comunidade usa-o com F5-TTS.

> **少样本微调。**录制目标声音 5-30 分钟──LoRA 微调基础模型一小时──质量从"还行"跳到"无法区分"──Coqui 和 ElevenLabs 都支持这种模式;社区用F5-TTS 实现──

**Voice conversion (VC).**Duas famílias:

> **语音转换（VC）。**两个家族:

- **Recognition-synthesis.**Execute um modelo ASR para extrair representação de conteúdo (por exemplo, posteriors fonémicos moles, PPGs), em seguida, resinteze com o incorporamento de alto-falantes alvo. Robusto para a linguagem e o sotaque. usado por KNN-VC (2023), Diff-HierVC (2023).
  **识别-合成。**运行类 ASR 模型提取内容表示 (如软音素后验、PPG), em seguida, usar o objetivo de falar em pessoas para reintroduzir.
- **Disentanglement.**Treinar um autoencoder que separa conteúdo, alto-falantes e prosódias em espaço latente no gargalo de engarrafamento. Swap alto-falantes incorporando na inferência. Baixa qualidade, mas mais rápido. Usado por AutoVC (2019), variantes VITS-VC.
  **解耦。** training self-coder in bottle处的潜在空间中分离内容、讲话人和律──推理时交换说话人嵌入──质量较低但更快──AutoVC(2019)、VITS-VC 变体使用──

**Neural codec-based cloning (2024+).**VALL-E, VALL-E 2, NaturalSpeech 3, VoiceBox  tratar o áudio como tokens discretos do SoundStream / EnCodec, treinar um grande modelo autoregressivo ou de correspondência de fluxo sobre tokens de codec. Qualidade comparável a ElevenLabs em instruções curtas.

> **基于神经编解码器的克隆（2024+）。**VALL-E、VALL-E 2、NaturalSpeech 3、VoiceBox将音频视为 SoundStream/EnCodec's离散代币, 在编解码代币上训练大型自归归或流匹配模型──短提示上质量可与ElevenLabs相当──

### O pouco ético, não um boleto

> ### 伦理问题, não é opcional

**Watermarking.**PerTh (Perth) e SilentCipher (2024) incorporam um ID de ~16-32 bits imperceptiblemente no áudio. Sobrevive ao re-encodificação, streaming e edições comuns.

> **水印。**PerTh 和 SilentCipher(2024) embutidos de cerca de 16 a 32 bits em seu rádio.

**Consent gates.**"Eu, Rohit, em 2026-04-22, autorizo esta voz para propósito X". Guarde num registro de manipulação.

> **同意门。**Cada produto deve ser acompanhado de um registro de consentimento verificável.

**Detection.**AASIST, RawNet2 e Wav2Vec2-AASIST navio como detectores. ASVspoof 2025 desafio publicou EERs de 0,82,3% para os detectores de última geração contra ElevenLabs, VALL-E 2, e Bark saídas.

> **检测。**AASIST、RawNet2 和 Wav2Vec2-AASIST 作为检测器发布──ASVspoof 2025 挑战赛发布了SOTA 检测器对ElevenLabs、VALL-E 2 和 Bark 输出 EER为0.8-2.3%──

### Números (2026)

> Número de anos de 2026

| Model | Zero-shot? | SECS (target sim) | WER (intel.) | Params |
|-------|-----------|--------------------|--------------|--------|
| F5-TTS | Yes | 0.72 | 2.1% | 335M |
| XTTS v2 | Yes | 0.65 | 3.5% | 470M |
| OpenVoice v2 | Yes | 0.70 | 2.8% | 220M |
| VALL-E 2 | Yes | 0.77 | 2.4% | 370M |
| VoiceBox | Yes | 0.78 | 2.1% | 330M |

| 模型 | 零样本？ | SECS（目标相似度） | WER（可懂度） | 参数量 |
|------|---------|-------------------|--------------|--------|
| F5-TTS | 是 | 0.72 | 2.1% | 3.35 亿 |
| XTTS v2 | 是 | 0.65 | 3.5% | 4.7 亿 |
| OpenVoice v2 | 是 | 0.70 | 2.8% | 2.2 亿 |
| VALL-E 2 | 是 | 0.77 | 2.4% | 3.7 亿 |
| VoiceBox | 是 | 0.78 | 2.1% | 3.3 亿 |

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.


SECS > 0,70 é geralmente indistinguível do alvo para a maioria dos ouvintes.

> SECS > 0,70 para a maioria dos ouvintes, normalmente não é possível distinguir entre o objetivo e o objetivo.

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.



## Construí-lo e realizei-o.
```figure
sp-voice-factorize
```

## Construí-lo

### Passo 1: decompõe com reconhecimento-síntese (só código demo em main.py)

```python
def clone_pipeline(ref_audio, text, target_embedder, tts_model):
    speaker_emb = target_embedder.encode(ref_audio)
    mel = tts_model(text, speaker=speaker_emb)
    return vocoder(mel)
```

Conceptualmente simples; massa de implementação é de`tts_model`e um codificador de alto-falantes.

> 概念上简单; realização `tts_model`E o meu amigo está a escrever.

### Passo 2: clone de tiro zero com F5-TTS

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="rohit_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please add milk and bread to my list.",
)
```

A transcrição de referência deve corresponder exatamente ao áudio; a descoincidência rompe o alinhamento.

> 参照转录必须完全匹配与音频;不匹配将破坏对齐──

### Passo 3: conversão de voz com KNN-VC

```python
import torch
from knnvc import KNNVC  # 2023 model, https://github.com/bshall/knn-vc
vc = KNNVC.load("wavlm-base-plus")
out_wav = vc.convert(source="my_voice.wav", target_pool=["alice_1.wav", "alice_2.wav"])
```

KNN-VC executa WavLM para extrair embebimentos por quadro para pool de fonte e alvo, em seguida, substitui cada quadro de origem com o vizinho mais próximo na piscina.

> KNN-VC 运行 WavLM 提取源和目标池的逐嵌入, em seguida, usar o vizinho mais próximo no池 para substituir cada fonte──非参数化,一分钟目标语音即可工作──

### Passo 4: inserir uma marca de água

```python
from silentcipher import SilentCipher
sc = SilentCipher(model="2024-06-01")
payload = b"consent_id:abc123;ts:1745353200"
watermarked = sc.embed(wav, sr=24000, message=payload)
detected = sc.detect(watermarked, sr=24000)   # returns payload bytes
```

~ 32 bits de carga útil, detectável após a recodificação MP3 e ruído leve.

> 约 32 位载荷,MP3 重编码和轻度噪音后仍可检测──

### Passo 5: Portal de consentimento

```python
def cloned_inference(text, ref_audio, consent_record):
    assert verify_signature(consent_record), "Signed consent required"
    assert consent_record["speaker_id"] == hash_speaker(ref_audio)
    wav = tts.infer(ref_file=ref_audio, gen_text=text)
    wav = watermark(wav, payload=consent_record["id"])
    return wav
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.





> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

A pilha de 2026:

> Tecnologia de 2026:

| Situation | Pick |
|-----------|------|
| 5-sec zero-shot clone, open-source | F5-TTS or OpenVoice v2 |
| Commercial production cloning | ElevenLabs Instant Voice Clone v2.5 |
| Voice conversion (rewriting) | KNN-VC or Diff-HierVC |
| Many-speaker fine-tune | StyleTTS 2 + speaker adapter |
| Cross-lingual cloning | XTTS v2 or VALL-E X |
| Deepfake detection | Wav2Vec2-AASIST |

| 场景 | 选择 |
|------|------|
| 5 秒零样本克隆，开源 | F5-TTS 或 OpenVoice v2 |
| 商业生产级克隆 | ElevenLabs Instant Voice Clone v2.5 |
| 语音转换（重写） | KNN-VC 或 Diff-HierVC |
| 多说话人微调 | StyleTTS 2 + 说话人适配器 |
| 跨语言克隆 | XTTS v2 或 VALL-E X |
| 深度伪造检测 | Wav2Vec2-AASIST |



## Encurralagens

> 常见陷

- **Misaligned reference transcript.**F5-TTS e similares exigem que o texto de referência corresponda exatamente ao áudio de referência, incluindo a pontuação.
  **参考转录不对齐。**F5-TTS etc. Requisitos de referência em texto e em rádio de referência
- **Reverberant reference.**O Echo mata o clone.
  **混响参考。**O que é que se passa?
- **Emotional mismatch.**A referência de treinamento "alegre" produz clones alegres de tudo.
  **情感不匹配。**                                                                                                                                                                                                                                                              
- **Language leakage.**Clonar um falante de inglês e depois pedir ao modelo que fale francês geralmente carrega o sotaque de qualquer maneira; use modelos interlinguários (XTTS, VALL-E X).
  **语言泄漏。**克隆英文说话人然后让模型说法语仍将带有口音;使用跨语言模型 (XTTS、VALL-E X) ⋅
- **No watermark.**Não é legalmente enviável na UE a partir de agosto de 2026.
  **没有水印。**A partir de 2026 a partir de agosto de 2026 não será publicado na UE.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-voice-cloner.md`. Desenhar um canal de clonagem ou de conversão com porta de consentimento + marca de água + meta de qualidade.

> 保存为 `outputs/skill-voice-cloner.md`◊ design with consent门 + 水印 + 质量目标的克隆或转换流水线──

## Exercícios.

1. **Easy.**Corra .`code/main.py`. Demonstra a troca de integradores de alto-falantes, calculado o cosino entre dois "falantes" antes e depois da troca.
   **简单。**运行 `code/main.py`◊ através do cálculo de trocas de palavras e palavras, o discurso é introduzido em trocas de palavras.
2. **Medium.**Use o OpenVoice v2 para clonar a sua própria voz. Messa o SECS entre referência e clone. Messa o CER através do Whisper.
   **中等。**Usando OpenVoice v2 克隆你自己的声音──测量参考与克隆之间的SECS──通过Whisper 测量 CER──
3. **Hard.**Aplique a marca de água SilentCipher em 20 clones, execute-os através de 128 kbps MP3 codificação + decodificação, detectar a carga útil.
   **困难。**Para 20 aplicações em SilentCipher, através de 128 kbps MP3 编码+解码,检测载荷――报告比特准确率──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Zero-shot clone | 5 seconds is enough | Pretrained model + speaker embedding; no training. |
| PPG | Phonetic posteriorgram | Per-frame ASR posteriors used as language-agnostic content rep. |
| KNN-VC | Nearest-neighbor conversion | Replace each source frame with nearest target-pool frame. |
| Neural codec TTS | VALL-E style | AR model over EnCodec/SoundStream tokens. |
| Watermark | Inaudible signature | Bits embedded in audio, survive re-encode. |
| SECS | Cloning fidelity | Cosine between target and clone speaker embeddings. |
| AASIST | Deepfake detector | Anti-spoof model; detects synthesized speech. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 零样本克隆 | 5 秒就够了 | 预训练模型 + 说话人嵌入；无需训练。 |
| PPG | 音素后验图 | 逐帧 ASR 后验，用作语言无关的内容表示。 |
| KNN-VC | 最近邻转换 | 用目标池中最近邻替换每个源帧。 |
| 神经编解码 TTS | VALL-E 风格 | 在 EnCodec/SoundStream token 上的 AR 模型。 |
| 水印 | 不可听签名 | 嵌入音频中的比特，经受重编码。 |
| SECS | 克隆保真度 | 目标与克隆说话人嵌入之间的余弦相似度。 |
| AASIST | 深度伪造检测器 | 反欺诈模型；检测合成语音。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885) Clonagem de código aberto SOTA de tiro zero.
  Chen 等 (2024). F5-TTS开源 SOTA 零样本克隆──
- [Baevski et al. / Microsoft (2023). VALL-E](https://arxiv.org/abs/2301.02111)E ...[VALL-E 2 (2024)](https://arxiv.org/abs/2406.05370) TTS de codec neural.
  Baevski 等 / 微软 (2023). VALL-E 和 VALL-E 2(2024)  神经编解码 TTS──
- [Qian et al. (2019). AutoVC](https://arxiv.org/abs/1905.05879) conversão de voz baseada em desembaraço.
  Qian 等 (2019). AutoVC baseado em resolução 的语音转换──
- [Baas, Waubert de Puiseau, Kamper (2023). KNN-VC](https://arxiv.org/abs/2305.18975) VC baseado em recuperação.
  Baas, Waubert de Puiseau, Kamper (2023). KNN-VC Baseada em检索的语音转换──
- [SilentCipher (2024) — Audio Watermarking](https://github.com/sony/silentcipher) Marca de áudio de 32 bits pronta para produção.
  SilentCipher ((2024) 音频水印生产可用 32 位音频水印──
- [ASVspoof 2025 results](https://www.asvspoof.org/) corrida de armamento detector vs. sintetizador, atualizada em 2026.
  ASVspoof 2025 结果检测器 vs 合成器军备竞赛,2026年更新──

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

