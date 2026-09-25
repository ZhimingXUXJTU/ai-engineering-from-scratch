# "Susperar Arquitetura e Arquitetura e Arquitetura"

> Whisper é um transformer de 30 segundos de janela encoder-decoder, treinado em 680k horas de pares de áudio-texto multilíngue deficiente supervisionado.

> **【中文解读】**Whisper é um transformer de 30 segundos, em 680.000 horas, em mais de 80 idiomas.

> **【拓展：Whisper 的生态】**Whisper 衍生了 Whisper.cpp(本地部署)、Faster-Whisper(CTtranslate2 加速)、WhisperX(词级时间)、Bloomsbury(实时流式)等工具链,是语音识别工业部署的事实标准──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04 (ASR), Phase 5 · 10 (Attention), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 04（ASR），阶段 5 · 10（注意力机制），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## O problema é o problema da introdução

O Whisper, lançado pela OpenAI em setembro de 2022, foi o primeiro modelo ASR a ser enviado como um produto: paste áudio, obter texto, 99 idiomas, robusto ao ruído, funciona em um laptop. Em 2024, a OpenAI havia enviado variantes Large-v3 e Turbo; em 2026, o Whisper é a linha de base padrão para tudo, desde transcrição de podcast a assistentes de voz a subtítulos do YouTube.

> Whisper foi lançado pela OpenAI em setembro de 2022, é o primeiro modelo ASR lançado como produto geral: stickling, obtiver texto, 99 idiomas, anti-ruído, operacional em seu próprio computador. Até 2024, a OpenAI lançou o Large-v3 e Turbo; até 2026, o Whisper foi transferido do usuário para o assistente de voz para o YouTube.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

Mas o Whisper não é um pipeline que você pode tratar como uma caixa negra para sempre.

> Mas o sussurro não é o fluxo de água que pode ser usado na caixa negra.

1. O que é que realmente está lá dentro.
   É o que é a estrutura interior.
2. Como dar corretamente áudio em pedaços, em streaming ou em formato longo.
   Como é que é que é preciso fazer isso?
3. Quando e como ajustar.
   Qual é o tempo e como é o tempo?

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


## O conceito central.

![Whisper encoder-decoder, tasks, chunked inference, fine-tune](../assets/whisper.svg)

**Architecture.**Transformador padrão encoder-decoder.

> **架构。**标准 Transformer 编码器-解码器──

- Entrada: Espectroograma log-mel de 30 segundos, 80 mels, 10 ms hop → 3000 quadros.
  输入30 秒 log-mail 频谱图,80 mels,10 ms 步长 → 3000 ──短片段零填充,长片段分块──
- Encoder: conv-downsample (passo 2) + `N`Para grande V3: 32 camadas, 1280-dim, 20 cabeças.
  编码器:卷积下采样(步幅 2) + `N`个 Transformer 块──Large-v3:32 层,1280 维,20 头──
- Descódigo: `N`Blocos de transformador com auto-atn + cross-attn para saída de codificador.
  解码器:`N`个带因果自注意力 + Transformer 块──与编码器同大小──
- Resultado: Tokens BPE sobre um vocabulário de 51.865 tokens.
  输出:51,865 token 词表上的 BPE token──

O Large-v3 tem parâmetros de 1.55B. Turbo usa um decodificador de 4 camadas (a partir de 32), cortando a latência 8x com um hit WER < 1%.

> Grande-v3 tem 15,5 mil milhões de parâmetros.

**The prompt format.**Whisper é um modelo de multitarefa dirigido por tokens especiais no prompt do decodificador:

> **提示格式。**Whisper é um modelo de várias tarefas, através de um token especial de comando:

```
<|startoftranscript|><|en|><|transcribe|><|notimestamps|> Hello world.<|endoftext|>
```

- `<|en|>` tag de linguagem; força o comportamento tradução versus transcrição.
  `<|en|>` 语言标签; obrigatoriedade tradução ou transcrição
- `<|transcribe|>`ou `<|translate|>` traduzir o resultado em inglês a partir de qualquer entrada de idioma, ou literalmente.
  `<|transcribe|>`Ou `<|translate|>` From any language输入翻译为英文输出,或逐字转录──
- `<|notimestamps|>` Salte os timestamps de nível de palavra (mais rápido).
  `<|notimestamps|>` 跳过词级时间(更快)。

O prompt é o que permite que um modelo faça muitas tarefas.`<|en|>`- Não .`<|fr|>`E transcreve em francês.

> O que é importante é que um modelo faça várias tarefas.`<|en|>`改为 `<|fr|>`Em inglês.

**30-second window.**Tudo é fixado em 30 segundos. Clips mais longos precisam de troca; clips mais curtos são empolgados. Windows não são transmitidos nativamente  é por isso que existem WhisperX, Whisper-Streaming e faster-whisper.

> **30 秒窗口。**Tudo em 30 segundos para basear. O maior volume de som precisa de blocos; o menor volume precisa de preenchimento. A janela não suporta o processo de produção original.

**Log-mel normalization.** `(log_mel - mean) / std`O que é que é o que é o Whisper?`whisper.audio.log_mel_spectrogram`), não `librosa.feature.melspectrogram`- Não .

> **Log-mel 归一化。** `(log_mel - mean) / std`, da qual a estatística vem de Whisper  própria formação语料──你*必须*使用 Whisper 的预处理(`whisper.audio.log_mel_spectrogram`), em vez de `librosa.feature.melspectrogram`- Não.

### Variantes em 2026

> ### 2026 ano de mudanças

| Variant | Params | Latency (A100) | WER (LibriSpeech-clean) |
|---------|--------|----------------|------------------------|
| Tiny | 39M | 1× realtime | 5.4% |
| Base | 74M | 1× | 4.1% |
| Small | 244M | 1× | 3.0% |
| Medium | 769M | 1× | 2.7% |
| Large-v3 | 1.55B | 2× | 1.8% |
| Large-v3-turbo | 809M | 8× | 1.58% |
| Whisper-Streaming (2024) | 1.55B | streaming | 2.0% |

| 变体 | 参数量 | 延迟（A100） | WER（LibriSpeech-clean） |
|------|--------|--------------|-------------------------|
| Tiny | 3900 万 | 1× 实时 | 5.4% |
| Base | 7400 万 | 1× | 4.1% |
| Small | 2.44 亿 | 1× | 3.0% |
| Medium | 7.69 亿 | 1× | 2.7% |
| Large-v3 | 15.5 亿 | 2× | 1.8% |
| Large-v3-turbo | 8.09 亿 | 8× | 1.58% |
| Whisper-Streaming（2024） | 15.5 亿 | 流式 | 2.0% |

### Apontação fina

> ### 微调

Fluxo de trabalho canônico em 2026:

> O padrão de funcionamento para 2026:

1. Recolher 10100 horas de áudio do domínio alvo com transcrições alinhadas.
   收集 10-100 小时目标领域的音频及对应转录文本──
2. Corra .`transformers.Seq2SeqTrainer`com`generate_with_loss`- Voltar a ligar.
   Utilização `transformers.Seq2SeqTrainer`和 `generate_with_loss`O que é isso?
3. Eficiência do parâmetro: LoRA em `q_proj`- Não .`k_proj`- Não .`v_proj`de camadas de atenção reduz a memória da GPU 4× com custo de WER < 0,3.
   参数高效:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `q_proj`- Não.`k_proj`- Não.`v_proj`上使用Lora,GPU内存降低 4 倍,WER 损失 <0.3──
4. Congelhe o codificador se tiver < 10 horas. Apenas sintonize o decodificador.
   Se os dados não forem suficientes, apenas o micro-module o código.
5. Use o próprio tokenizer e formato de prompt do Whisper; nunca troque de tokenizer.
   Use Whisper  seu próprio tokenizer 和提示格式; Nunca substituir o tokenizer。

Resultados comunitários: ajuste fino Medium em 20 horas de ditado médico reduz o WER de 12% para 4,5% no vocabulário médico.

> 社区结果: 在 20 小时医疗口述上微调 Medium,医疗词汇 WER de 12% 降至 4.5%── 在 4 小时冰岛语上微调 Turbo, WER de 18% 降至 6%──

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.



## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

```figure
sp-asr-attention
```

## Construí-lo

### Passo 1: executar Whisper fora da caixa

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe(
    "clip.wav",
    language="en",
    task="transcribe",
    temperature=0.0,
    condition_on_previous_text=False,  # prevents runaway repetition
)
print(result["text"])
for seg in result["segments"]:
    print(f"[{seg['start']:.2f}–{seg['end']:.2f}] {seg['text']}")
```

As principais falhas que deve sempre ser ignorada: `temperature=0.0`(exemplos de defeitos para 0,0 → 0,2 → 0,4 ... cadeia de retorno), `condition_on_previous_text=False`(preventa o problema da alucinação em cascata), e `no_speech_threshold=0.6`(Detecção do silêncio).

> Você deve sempre cobrir os valores-chave:`temperature=0.0`(采样默认为 0.0 → 0.2 → 0.4 ... 回退链)`condition_on_previous_text=False`(prevenir classe associée problem) e `no_speech_threshold=0.6`(静音检测)

### Passo 2: forma longa em pedaços

```python
# whisperx is the 2026 reference for long-form with word-level timestamps
import whisperx
model = whisperx.load_model("large-v3-turbo", device="cuda", compute_type="float16")
segments = model.transcribe("1hour.mp3", batch_size=16, chunk_size=30)
```

O WhisperX adiciona (1) Silero VAD gating, (2) alinhamento de nível de palavras através de wav2vec 2.0, (3) diarização através de `pyannote.audio`O cavalo de trabalho de 2026 para transcrição de produção.

> WhisperX 添加了 (1) Silero VAD 门控,(2) 通过 wav2vec 2.0 实现词级对齐,(3) 通过 `pyannote.audio`实现说话人分离──2026年生产转录的主力工具──

### Passo 3: sintonização com LoRA

```python
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from peft import LoraConfig, get_peft_model

model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3-turbo")
lora = LoraConfig(
    r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1, bias="none", task_type="SEQ_2_SEQ_LM",
)
model = get_peft_model(model, lora)
# model.print_trainable_parameters()  -> ~3M trainable / 809M total
```

Depois, o ciclo padrão do treinador, um ponto de controlo a cada 1000 passos, e uma avaliação com WER.

> Então, o padrão de treinador  treino ciclo ⋅ cada 1000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

### Passo 4: inspecionar o que cada camada aprende

```python
# Grab cross-attention weights during decode to see what the decoder attends to.
with torch.inference_mode():
    out = model.generate(
        input_features=features,
        return_dict_in_generate=True,
        output_attentions=True,
    )
# out.cross_attentions: layer × head × step × src_len
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


Visualize com um heatmap  você verá alinhamento diagonal como os passos do decodificador escanear através de quadros de codificador.

> Usando calorismo visualizando você verá o descifrador passo em passo em busca de codificador                                                                                                                                                                                                                                                   




> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

A pilha de 2026:

> Tecnologia de 2026:

| Situation | Pick |
|-----------|------|
| General English, offline | Large-v3-turbo via `whisperx` |
| Mobile / edge | Whisper-Tiny quantized (int8) or Moonshine |
| Multilingual long-form | Large-v3 via `whisperx` + diarization |
| Low-resource language | Fine-tune Medium or Turbo with LoRA |
| Streaming (2 s latency) | Whisper-Streaming or Parakeet-TDT |
| Word-level timestamps | WhisperX (forced alignment via wav2vec 2.0) |

| 场景 | 选择 |
|------|------|
| 通用英文、离线 | 通过 `whisperx` 使用 Large-v3-turbo |
| 移动端/边缘设备 | 量化 Whisper-Tiny（int8）或 Moonshine |
| 多语言长音频 | 通过 `whisperx` 使用 Large-v3 + 说话人分离 |
| 低资源语言 | 用 LoRA 微调 Medium 或 Turbo |
| 流式（2 秒延迟） | Whisper-Streaming 或 Parakeet-TDT |
| 词级时间戳 | WhisperX（通过 wav2vec 2.0 强制对齐） |

`faster-whisper`(CTranslate2 backend) é o tempo de execução de inferência CPU+GPU mais rápido em 2026  4x mais rápido do que a baunilha com saída idêntica.

> `faster-whisper`(CTranslate2 后端) é o CPU + GPU mais rápido de 2026 推理运行时比原始版本快4倍,输出完全相同──



## Encurralagens que ainda se lançam em 2026

> 2026 ano ainda em vítima de um erro

- **Hallucinated text on silence.**O sussurro treinado em legendas inclui "Obrigado por assistir!", "Subscreva!", letras de canções.
  **静音上的幻觉文本。**Whisper, em seu livro "Whisper" (em inglês), contém um texto que diz: "Obrigado por assistir!"
- **`condition_on_previous_text` cascade.**Uma alucinação contamina as janelas subsequentes.`False`A menos que precise de fluência em pedaços.
  **`condition_on_previous_text` 级联。**Uma visão de contaminação posterior.`False`- Não.
- **Short-clip padding.**Um clip de 2 segundos com 30 segundos pode alucinar no silêncio.`pad=False`ou VAD-gate.
  **短片段填充。**2 segundos de fragmentos de carga até 30 segundos de espera.`pad=False`Ou VAD 过──
- **Wrong mel stats.**Usar os mels da librosa em vez do Whisper produz uma saída quase aleatória.`whisper.audio.log_mel_spectrogram`- Não .
  **错误的 mel 统计量。**Use librosa de mels e não Whisper de irá gerar quase que qualquer saída.`whisper.audio.log_mel_spectrogram`- Não.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-whisper-tuner.md`Desenhar um fluxo de sintonia ou inferência Whisper para um determinado domínio.

> 保存为 `outputs/skill-whisper-tuner.md`❖ para um determinado domínio de design Whisper 微调或推理流水线──

## Exercícios.

1. **Easy.**Corra .`code/main.py`Ele tokeniza um pedido de estilo Whisper, calcula os orçamentos de forma decodificada e imprime o cronograma de pedaços para um clipe de 10 minutos.
   **简单。**运行 `code/main.py`                                                                                                                                                                                                                                                              
2. **Medium.**Instalação`faster-whisper`, transcrever um podcast de 10 minutos, comparar WER com uma transcrição humana.`language="auto"`contra forçado`language="en"`- Não .
   **中等。**Instalação`faster-whisper`, Transcord 10 minutos , em comparação com transcordes artificiais WER `language="auto"`Com obrigação`language="en"`- Não.
3. **Hard.**Usando HF `datasets`, escolher uma língua que o Whisper luta com (por exemplo, Urdu), sintonizar o Médio com o LoRA por 2 épocas em 2 horas, e relatar o delta WER.
   **困难。**Utilizando HF `datasets`,select a Whisper 困难的语言 (如乌尔都语), em 2 小时数据上使用 LoRA 微调 Medium 2 个时代,报告 WER 差值──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 30-sec window | Whisper's limit | Hard input cap; chunk longer audio. |
| SOT | Start-of-transcript | `<\|startoftranscript\|>` kicks off the decoder prompt. |
| Timestamps token | Temporal alignment | Every 0.02 s offset is a special token in the 51k vocab. |
| Turbo | The fast variant | 4-decoder layers, 8× faster, <1% WER regression. |
| WhisperX | The long-form wrapper | VAD + Whisper + wav2vec alignment + diarization. |
| LoRA fine-tune | Efficient tuning | Add low-rank adapters to attention; train ~0.3% of params. |
| Hallucination | The silent failure | Whisper produces fluent English from noise/silence. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 30 秒窗口 | Whisper 的限制 | 硬性输入上限；更长音频需分块。 |
| SOT | 转录开始 | `<\|startoftranscript\|>` 启动解码器提示。 |
| 时间戳 token | 时间对齐 | 每 0.02 秒偏移是 51k 词表中的特殊 token。 |
| Turbo | 快速变体 | 4 层解码器，快 8 倍，WER 回退 <1%。 |
| WhisperX | 长音频封装 | VAD + Whisper + wav2vec 对齐 + 说话人分离。 |
| LoRA 微调 | 高效调优 | 在注意力层添加低秩适配器；仅训练约 0.3% 参数。 |
| 幻觉 | 静默失败 | Whisper 从噪声/静音中产生流畅的英文。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Radford et al. (2022). Whisper paper](https://arxiv.org/abs/2212.04356) a arquitetura original e a receita de formação.
  Radford etc (2022). Whisper 论文原始架构和训练方案──
- [OpenAI (2024). Whisper Large-v3-turbo release](https://github.com/openai/whisper/discussions/2363)- Decodificador de 4 camadas, aceleração 8x.
  OpenAI (2024). Whisper Large-v3-turbo 发布4 层解码器,8 倍加速──
- [Bain et al. (2023). WhisperX](https://arxiv.org/abs/2303.00747)- Forma longa, alinhada com as palavras, diária.
  Bain 等 (2023). WhisperX长音频、词级对齐、说话人分离──
- [Systran — faster-whisper repo](https://github.com/SYSTRAN/faster-whisper) CTranslate2-supportado, 4x mais rápido.
  Sistema de transmissão mais rápida, rápido e rápido.
- [HuggingFace — Whisper fine-tune tutorial](https://huggingface.co/blog/fine-tune-whisper) LoRA canônico / caminhada completa de FT.
  AbraçosFaceSuspar 微调教程标准 LoRA/全参数微调指南。

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

