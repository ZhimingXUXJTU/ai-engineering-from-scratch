# Reconhecimento de fala (ASR)  CTC, RNN-T, atenção  语音识别  CTC、RNN-T

> O reconhecimento da fala é classificação de áudio em cada passo do tempo, colada por um modelo de sequência que conhece o inglês e o silêncio. CTC, RNN-T e atenção são as três maneiras de fazer isso. Escolha uma e entenda por quê.

> **【中文解读】**语音识别 é cada tempo fazer 音频分类, reutilizar sequências de modelos ((知道语言和静音规律) para agrupá-las.

> **【拓展：ASR 的应用】**语音识别是语音助手(Siri、小爱同学) 会议记录(飞书/钉钉实时字幕) 视频字幕自动生成的核心──Whisper is the open source ASR 标杆──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 08 (CNNs & RNNs for Text), Phase 5 · 10 (Attention) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 08（文本的 CNN 与 RNN），阶段 5 · 10（注意力机制）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## O problema é o problema da introdução

Você tem um clip de 10 segundos de 16 kHz. Você quer uma corda: "acende as luzes da cozinha". O desafio é estrutural: os quadros de áudio não se alinham um a um com os caracteres. A palavra "okay" pode levar 200 ms ou 1200 ms. O silêncio pontua a pronunciação. Alguns fonemas são mais longos do que outros. O número de tokens de saída não é conhecido com antecedência.

> Você tem um episódio de 10 segundos 16 kHz de som. Você quer um string: "acende as luzes da cozinha". O desafio é estrutural:

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

Três formulações resolvem isto:

> Três soluções para resolver este problema:

1. **CTC (Connectionist Temporal Classification).**Emite probabilidades de token por quadro, incluindo um *blank* especial. Repetências de colapso e espaços em tempo de decodificação. Não autoregressivo, rápido. usado por wav2vec 2.0, MMS.
   **CTC（连接时序分类）。**逐发射代币 概率, incluindo especial *blank*──解码时折重复和空白──非自归,快速──wav2vec 2.0、MMS 使用──
2. **RNN-T (Recurrent Neural Network Transducer).**A rede conjunta prevê o próximo token dado quadro de codificação e tokens anteriores. Streamable. usado pelo ASR do Google no dispositivo, NVIDIA Parakeet.
   **RNN-T（递归神经网络转换器）。**联合网络根据编码器和之前的代币 预测下一个代币──可流式处理──Google 端侧 ASR、NVIDIA Parakeet 使用──
3. **Attention encoder-decoder.**O encoder comprime áudio para estados ocultos, o decodificador atende cruzando para gerar tokens autoregressivamente.
   **注意力编码器-解码器。**编码器将音频压缩为隐藏状态,解码器通过交叉注意力自归归地生成代币──Whisper、SeamlessM4T 使用──

Em 2026, a SOTA WER no LibriSpeech test-clean é de 1,4% (Parakeet-TDT-1.1B, NVIDIA) e 1,58% (Whisper-Large-v3-turbo). As diferenças são pequenas; as diferenças de implantação são enormes.

> 2026 anos, LibriSpeech test-clean 上的 SOTA WER为1.4% (Parakeet-TDT-1.1B,NVIDIA)和1.58% (Whisper-Large-v3-turbo)

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![Three ASR formulations: CTC, RNN-T, attention-encoder-decoder](../assets/asr-formulations.svg)

**CTC intuition.**Deixe o codificador sair `T`distribuições de nível de quadro sobre `V+1`Tokens (caráter V + em branco). Para uma cadeia-alvo `y`de comprimento `U < T`, qualquer alinhamento de quadro que colapse para `y`As diferenças entre os valores de um sistema de correção de dados e os valores de um sistema de correção de dados são:

> **CTC 直觉。**让编码器输出 `T`个级分布, cada distribuição cobre `V+1`个 token ((V 个字符 + em branco) ⋅对于长度为 `U < T`Do que é que é que é?`y`, qualquer dobra posterior é igual a `y`O valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de valor de um valor de um valor de valor de um valor de um valor de valor de um valor de um valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor

Vantagens: não autoregressivo, streamable, zero lookahead. Desvantagem: *assunção de independência condicional*  cada previsão de quadro é independente dos outros, por isso não há um modelo de linguagem interna.

> 优势:非自归、可流式处理、零前──缺点:*条件独立性假设*每预测彼此独立,因此没有内部语言模型──通过束搜索或浅融合的外部LM 来修复──

**RNN-T intuition.**Adiciona uma rede de * predictor * que incorpora o histórico do token e um * joiner * que combina o estado do predictor com o quadro de codificador em uma distribuição conjunta sobre `V+1`(o `+1`é um zero / não emitente). Modela explicitamente a dependência condicional CTC ignorado. Streamable porque cada passo condições apenas em quadros passados e tokens passados.

> **RNN-T 直觉。**Adicionar um token embuxado  Historial * Predictor * 网络和一个将预测器 状态与编码器结合为 `V+1`联合分布的 *joiner*(`+1`É null/不发射) ――显式建模 CTC 忽略的条件依赖──可流式处理,因为 cada passo depende apenas do passado和过去的代币──

Vantagens: streaming + LM interno. Desvantagem: o treinamento é mais complexo e com fome de memória (3D reticula de perda); os núcleos de perda RNN-T são uma categoria inteira de biblioteca por si só.

> 优势:可流式 + 内部 LM。缺点:训练更复杂、更耗内存(3D 损失格);RNN-T 损失核本身就是一个完整的库类──

**Attention encoder-decoder.**Encoder (6-32 camadas de transformador) sobre quadros log-mail. Decoder (6-32 camadas de transformador) atende cruzada para encoder saídas para gerar tokens autoregressivamente. Nenhuma restrição de alinhamento  atenção pode olhar em qualquer lugar no áudio. Não pode ser transmitido a menos que você restrinja a atenção (Whisper-Streaming, 2024).

> **注意力编码器-解码器。**编码器(6-32 层变压器) 处理 log-mel ──解码器(6-32 层变压器) 通过交叉注意力自归归生成代币──无对齐约束注意力可以看向音频的任何位置──除非限制注意力(分块 微笑流,2024),否则不可流式处理──

Vantagens: alta qualidade em ASR offline, fácil de treinar com ferramentas seq2seq padrão.

> 优势:离线 ASR 质量最高,用标准seq2seq 工具易训练──缺点:自归延迟与输出长度成正比;不做工程优化无法流式处理──

### WER: o número único

> ### WER: único indicador

**Word Error Rate**- Não .`(S + D + I) / N`, onde S=substituições, D=eliminações, I=inserções, N=conto de palavras de referência. Correspondem à distância de edição Levenshtein no nível de palavras. Baixo é melhor. Um WER acima de 20% é geralmente inutilizável; abaixo de 5% é a paridade humana para a fala de leitura. Números 2026 em benchmarks padrão:

> **词错误率**- Não .`(S + D + I) / N`, em que S = substituir, D = eliminar, I = inserir, N = número de palavras de referência.

| Model | LibriSpeech test-clean | LibriSpeech test-other | Size |
|-------|------------------------|------------------------|------|
| Parakeet-TDT-1.1B | 1.40% | 2.78% | 1.1B params |
| Whisper-Large-v3-turbo | 1.58% | 3.03% | 809M |
| Canary-1B Flash | 1.48% | 2.87% | 1B |
| Seamless M4T v2 | 1.7% | 3.5% | 2.3B |

| 模型 | LibriSpeech test-clean | LibriSpeech test-other | 大小 |
|------|------------------------|------------------------|------|
| Parakeet-TDT-1.1B | 1.40% | 2.78% | 11 亿参数 |
| Whisper-Large-v3-turbo | 1.58% | 3.03% | 8.09 亿 |
| Canary-1B Flash | 1.48% | 2.87% | 10 亿 |
| Seamless M4T v2 | 1.7% | 3.5% | 23 亿 |

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.


Todos estes sistemas são baseados em codificadores-decodificadores ou RNN-T. Os sistemas de CTC puros (wav2vec 2.0) são de cerca de 1,82,1% em teste-limpo.

> Estes são todos os codificadores-descodificadores ou RNN-T 架构──纯 CTC 系统(wav2vec 2.0) em teste-limpo acima de 1,82.1%──

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.



## Construí-lo e realizei-o.
```figure
ctc-collapse
```

## Construí-lo

### Passo 1: codificação codificada de CTC

```python
def ctc_greedy(frame_logits, blank=0, vocab=None):
    # frame_logits: list of per-frame probability vectors
    preds = [max(range(len(p)), key=lambda i: p[i]) for p in frame_logits]
    out = []
    prev = -1
    for p in preds:
        if p != prev and p != blank:
            out.append(p)
        prev = p
    return "".join(vocab[i] for i in out) if vocab else out
```

Duas regras: colapso repetidas consecutivas, soltar espaços em branco.`a a _ _ a b b _ c`→ `a a b c`- Não .

> 两条规则: folhação连续重复,丢弃空白── exemplos:`a a _ _ a b b _ c`→ `a a b c`- Não.

### Passo 2: CTC de busca de feixe

```python
def ctc_beam(frame_logits, beam=8, blank=0):
    import math
    beams = [([], 0.0)]  # (tokens, log_prob)
    for p in frame_logits:
        log_p = [math.log(max(pi, 1e-10)) for pi in p]
        candidates = []
        for seq, lp in beams:
            for t, lpt in enumerate(log_p):
                new = seq[:] if t == blank else (seq + [t] if not seq or seq[-1] != t else seq)
                candidates.append((new, lp + lpt))
        candidates.sort(key=lambda x: -x[1])
        beams = candidates[:beam]
    return beams[0][0]
```

A produção usa a busca de feixe de árvore de prefixos com fusão LM; este é o esqueleto conceitual.

> O desenvolvimento de um ambiente de produção é um processo de desenvolvimento de um ambiente de produção.

### Passo 3: WER

```python
def wer(ref, hyp):
    r, h = ref.split(), hyp.split()
    dp = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1):
        dp[i][0] = i
    for j in range(len(h) + 1):
        dp[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            cost = 0 if r[i - 1] == h[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )
    return dp[len(r)][len(h)] / max(1, len(r))
```

### Passo 4: inferência contra o sussurro

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("clip.wav")
print(result["text"])
```

Um linheiro para o ASR geral mais forte em 2026.

> A linha de código de ASR mais forte de 2026 foi executada em 24 GB de GPU com cerca de 20 vezes a velocidade real.

### Passo 5: streaming com Parakeet ou wav2vec 2.0

```python
from transformers import pipeline
asr = pipeline("automatic-speech-recognition", model="nvidia/parakeet-tdt-1.1b")
for chunk in streaming_audio():
    print(asr(chunk, return_timestamps=True))
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


Streaming ASR requer atenção de codificador em pedaços e estado de carregamento; use uma biblioteca que o suporta (NeMo para Parakeet, `transformers`O gasoduto com `chunk_length_s`)).

> 流式 ASR 需要分块编码器注意力和转移状态;使用支持它的库(NeMo 用于Parakeet,`transformers`gasodutos`chunk_length_s`)。




> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

A pilha de 2026:

> Tecnologia de 2026:

| Situation | Pick |
|-----------|------|
| English, offline, max quality | Whisper-large-v3-turbo |
| Multilingual, robust | SeamlessM4T v2 |
| Streaming, low latency | Parakeet-TDT-1.1B or Riva |
| Edge, mobile, <500 ms latency | Whisper-Tiny quantized or Moonshine (2024) |
| Long-form | Whisper with VAD-based chunking (WhisperX) |
| Domain-specific (medical, legal) | Fine-tune wav2vec 2.0 + domain LM fusion |

| 场景 | 选择 |
|------|------|
| 英文、离线、最高质量 | Whisper-large-v3-turbo |
| 多语言、鲁棒 | SeamlessM4T v2 |
| 流式、低延迟 | Parakeet-TDT-1.1B 或 Riva |
| 边缘/移动、<500 ms 延迟 | 量化 Whisper-Tiny 或 Moonshine（2024） |
| 长音频 | Whisper + VAD 分块（WhisperX） |
| 特定领域（医疗、法律） | 微调 wav2vec 2.0 + 领域 LM 融合 |



## Encurralagens que ainda se lançam em 2026

> 2026 ano ainda em vítima de um erro

- **No VAD.**Correr Whisper em silêncio produz alucinações ("Obrigado por assistir!").
  **没有 VAD。**"Obrigado por assistir!")
- **Character vs word vs subword WER.**Relatório de WER de nível de palavra *após* normalização (minúscula, pontuação despojada).
  **字符 vs 词 vs 子词 WER。**報告归一化后 (小写、去标点) 词级 WER──
- **Language ID drift.**O LID automático do Whisper encaminha erroneamente os clips barulhentos para o japonês ou galês; força `language="en"`Quando você sabe.
  **语言识别漂移。**Whisper's automatic language recognition will mistake 杂片段 for Japanese or Welsh; conhecido idioma quando forçado `language="en"`- Não.
- **Long clips without chunking.**O Whisper tem uma janela de 30 segundos.`chunk_length_s=30, stride=5`Para qualquer coisa mais longa.
  **长音频不分块。**Fosseira tem 30 segundos de espaço.`chunk_length_s=30, stride=5`- Não.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-asr-picker.md`Selecionar modelo, estratégia de decodificação, fragmentação e fusão LM para um determinado alvo de implantação.

> 保存为 `outputs/skill-asr-picker.md` para uma determinada implantação de objectivos, modelos de selecção, estratégias de decodificação, blocos e LM 融合方案.

## Exercícios.

1. **Easy.**Corra .`code/main.py`- Descifrar com ganância uma saída CTC feita à mão e calcular o WER em relação a uma referência.
   **简单。**运行 `code/main.py` Ele é responsável pela produção manual de CTC 输出进行贪解码并计算 WER
2. **Medium.**Implementar a busca de feixe de árvore de prefixo na etapa 2 corretamente (conta a regra de fusão em branco). Compare com a ganância em um conjunto de dados sintéticos de 10 exemplos.
   **中等。**O que é o que acontece com o uso de um arbusto?
3. **Hard.**Utilização`whisper-large-v3-turbo`- Não .[LibriSpeech test-clean](https://www.openslr.org/12)- Calcular o WER das primeiras 100 declarações.
   **困难。**Em[LibriSpeech test-clean](https://www.openslr.org/12)上使用 `whisper-large-v3-turbo`◊ calcular ‡ 100 条语音的 WER──与发表的数据比较──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| CTC | The blank-token loss | Marginal over all frame-to-token alignments; non-AR. |
| RNN-T | The streaming loss | CTC + next-token predictor; handles word-order. |
| Attention enc-dec | Whisper-style | Encoder + cross-attending decoder; best offline quality. |
| WER | The number you report | `(S+D+I)/N` at word level. |
| Blank | The emptiness | Special token in CTC signalling "no emission this frame". |
| LM fusion | External language model | Add weighted LM log-probs during beam search. |
| VAD | The silence gate | Voice activity detector; trims non-speech. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| CTC | blank token 损失 | 所有帧到 token 对齐的边际概率；非自回归。 |
| RNN-T | 流式损失 | CTC + 下一 token 预测器；处理词序。 |
| 注意力编解码 | Whisper 风格 | 编码器 + 交叉注意力解码器；最佳离线质量。 |
| WER | 你报告的数字 | 词级别的 `(S+D+I)/N`。 |
| Blank | 空白 | CTC 中表示"本帧不发射"的特殊 token。 |
| LM 融合 | 外部语言模型 | beam search 中加入加权的 LM 对数概率。 |
| VAD | 静音门 | 语音活动检测器；裁剪非语音部分。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Graves et al. (2006). Connectionist Temporal Classification](https://www.cs.toronto.edu/~graves/icml_2006.pdf) o papel do CTC.
  Graves 等 (2006). 连接时序分类CTC 论文。
- [Graves (2012). Sequence Transduction with RNNs](https://arxiv.org/abs/1211.3711)O papel RNN-T.
  Graves (2012). Usar RNN  para realizar sequência de transformação RNN-T 论文。
- [Radford et al. / OpenAI (2022). Whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) o papel canônico de 2022; extensão v3-turbo em 2024.
  Radford 等 / OpenAI (2022). Whisper: Masselha weak监督的鲁棒语音识别2022 年经典论文;2024 年 v3-turbo 扩展──
- [NVIDIA NeMo — Parakeet-TDT card](https://huggingface.co/nvidia/parakeet-tdt-1.1b) Líder do quadro de liderança de RAS abertos de 2026.
  NVIDIA NeMoParakeet-TDT 模型卡2026 年 Open ASR 排行榜领先者──
- [Hugging Face — Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) referência ao vivo em mais de 25 modelos.
  Abraçando o rostoOpen ASR 排行榜25+ 模型的实时基准测试──

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

