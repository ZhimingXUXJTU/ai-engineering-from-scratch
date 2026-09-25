# Avaliação de áudio  WER, MOS, UTMOS, MMAU, FAD e as tabela de liderança aberta 音频评估指标

> Esta lição nomeia as métricas 2026 para cada tarefa de áudio: ASR (WER, CER, RTFx), TTS (MOS, UTMOS, SECS, WER-on-ASR-round-trip), áudio-linguagem (MMAU, LongAudioBench), música (FAD, CLAP) e alto-falantes (EER).

> **【中文解读】**无法度量就无法交付──本课列出 2026年所有音频任务的评估指标:ASR 用 WER (WER) 词错率)  TTS 用 MOS (MOS) 平均意见分) 音频语言模型用 MMAU、音乐用 FAD、说话人识别用 EER──还有对比排列榜──

> **【拓展：WER 是语音识别的黄金指标】**WER(Word Error Rate,词错率) = (替换+删除+插入) / 总词数──Whisper Grande v3 在英文上达到 ~5% WER,接近人类水平──中文用 CER(字错率)──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 06, 07, 09, 10; Phase 2 · 09 (Model Evaluation) | **前置知识:** 阶段 6 · 04、06、07、09、10；阶段 2 · 09（模型评估）
**Time:** ~60 minutes | **预计用时:** ~60 分钟

## O problema é o problema da introdução

Cada tarefa de áudio tem múltiplas métricas, cada uma medindo um eixo diferente. Usando a métrica errada é como você envia um modelo que parece ótimo no seu painel de controle e terrível em produção.

> Cada tarefa de som tem vários indicadores, cada indicador mede diferentes dimensões. O indicador de uso errado é como um modelo de 2026 em linha parece ótimo no painel de instrumentos, mas que se apresenta mal na produção.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.


| Task | Primary | Secondary |
|------|---------|-----------|
| ASR | WER | CER · RTFx · first-token latency |
| TTS | MOS / UTMOS | SECS · WER-on-ASR-round-trip · CER · TTFA |
| Voice cloning | SECS (ECAPA cosine) | MOS · CER |
| Speaker verification | EER | minDCF · FAR / FRR at operating point |
| Diarization | DER | JER · speaker confusion |
| Audio classification | top-1 · mAP | macro F1 · per-class recall |
| Music generation | FAD | CLAP · listening panel MOS |
| Audio language model | MMAU-Pro | LongAudioBench · AudioCaps FENSE |
| Streaming S2S | latency P50/P95 | WER · MOS |

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


## O conceito central.

![Audio evaluation matrix — metrics vs tasks vs 2026 leaderboards](../assets/eval-landscape.svg)

### Metricas de RAS

> Indicador de avaliação de RAS

**WER (Word Error Rate).** `(S + D + I) / N`- Baixa letra, pontuação de strip, normalização de números antes de marcar.`jiwer`ou da OpenAI `whisper_normalizer`. &lt;5% = leitura de fala em paridade humana.

> **WER（词错率）。** `(替换 + 删除 + 插入) / 总词数`◊评分前需转小写、除标点、标准化数字──使用 `jiwer`Ou OpenAI `whisper_normalizer`❖ Menos de 5% = 朗读语音的人类水平──

**CER (Character Error Rate).**A mesma fórmula, nível de caracteres. Usado para línguas de tom (mandarim, cantonês) onde a segmentação de palavras é ambígua.

> **CER（字错率）。**相同公式,字符级别──用于声调语言(普通话、语),因为词细分 不明──

**RTFx (inverse real-time factor).**Segundo de áudio processado por segundo de relógio de parede. Mais alto é melhor. Parakeet-TDT atinge 3380x.

> **RTFx（逆实时因子）。**Cada segundo real de processamento de número de segundos de som.

**First-token latency.**O relógio de parede da entrada de áudio para o primeiro token de transcrição.

> **首 token 延迟。**Desde o audio input até o primeiro transcrição token.

### Metricas de TTS

> TTS  avaliação indicador

**MOS (Mean Opinion Score).**1-5 de classificação humana. Padrão de ouro, mas lento. Coletar mais de 20 ouvintes por amostra, 100+ amostras por modelo.

> **MOS（平均意见分）。**1-5 分人工评分──黄金标准但速度慢──每样本收集20+听者,每模型100+样本──

**UTMOS (2022-2026).**Aprendi predictor MOS. Correlação de ~ 0,9 com MOS humano em padrões de referência. F5-TTS: UTMOS 3,95; verdade fundamental: 4,08.

> **UTMOS（2022-2026）。**O MOS é um sistema de previsão de dados que é um sistema de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de

**SECS (Speaker Encoder Cosine Similarity).**Para clonagem de voz. ECAPA incorporando cosino entre referência e saída clonada. &gt; 0,75 = clone reconhecível.

> **SECS（说话人编码器余弦相似度）。**Utilizado em语音克隆──参考音频和克隆输出之间的 ECAPA 嵌入余弦相似度──大于0.75 = 可识别的克隆──

**WER-on-ASR-round-trip.**Execute Whisper sobre a saída TTS, computa WER contra o texto de entrada. Capta regressões de inteligibilidade. 2026 SOTA: &lt; 2% CER.

> **WER-on-ASR-round-trip（ASR 回环 WER）。**Para TTS 输出运行 Whisper,计算对输入文本的 WER──捕获可理解度退化──2026 SOTA:CER 低于2%──

**TTFA (time-to-first-audio).**Latência de relógio de parede. Kokoro-82M: ~ 100 ms; F5-TTS: ~ 1 s.

> **TTFA（首个音频时间）。**实际延迟──Kokoro-82M: cerca de 100 ms; F5-TTS: cerca de 1 s──

### Específico para clonagem vocal

> 语音克隆专用标标签

**SECS + MOS + CER**Cloning que tem um alto SECS mas baixo MOS significa timbre-direito-mas-naturalmente; o oposto significa voz natural mas falhante.

> **SECS + MOS + CER**Como três indicadores: Klon score high SECS Mas Low MOS significa som certo mas não natural;

### Verificação de alto-falantes

> 说话人验证指标

**EER (Equal Error Rate).**O limite em que a taxa de rejeição falsa é igual à taxa de rejeição falsa.

> **EER（等错误率）。** erro aceitação taxa é igual ao erro rejeição taxa valor。 ECAPA em VoxCeleb1-O 上: 0.87%。

**minDCF (min Detection Cost).**Custo ponderado num ponto de exploração escolhido (frequentemente FAR=0,01).

> **minDCF（最小检测代价）。**Em pontos de trabalho definidos (normalmente FAR=0.01) o aumento do preço de produção é mais próximo do que o da EER.

### Diarização

> 说话人日志标签

**DER (Diarization Error Rate).** `(FA + Miss + Confusion) / total_speaker_time`. Falsa fala + fala de falsa alarme + confusão de alto-falantes, cada uma como uma fração. Reuniões AMI: DER ~ 10-20% é realista. pyannote 3.1 + Precision-2 comercial: &lt;10% DER em áudio bem gravado.

> **DER（说话人日志错误率）。** `(虚警 + 漏检 + 混淆) / 总说话时间`◊漏检语音 + 虚警语音 + 说话人混,各占比例──AMI 会议:DER 约 10-20% 是现实水平──piannote 3.1 + Precision-2 商业版:在良好录音上 DER 低于10%──

**JER (Jaccard Error Rate).**Alternativa à DER, robusta para o viés de segmentos curtos.

> **JER（Jaccard 错误率）。**O DER é um sistema alternativo, para um pequeno diferencial de tempo.

### Classificação de áudio

> 音频分类标标

Multi-etiqueta: **mAP (mean Average Precision)**AudioSet: 0,548 mAP para BEATs-iter3.

> Dois marcos:**mAP（平均精度均值）**, cobre todas as categorias。AudioSet:BEATs-iter3 为 0.548 mAP。

Exclusivos para várias classes: **top-1, top-5 accuracy**Comando de fala v2: 99,0% top-1 (Audio-MAE).

> Dois tipos de interação:**top-1、top-5 准确率**❖ Comando de fala v2:99.0% top-1 (Audio-MAE) ❖

Desbalançado: **macro F1**+ **per-class recall**. Relatório por classe  A precisão agregada oculta quais classes falham.

> Não equilibrados:**macro F1**+ **每类召回率** O relatório de classificação 汇总准确率将掩盖哪些类别失败──

### Geração de música

> 音乐生成指标

**FAD (Fréchet Audio Distance).**Distância entre distribuições de áudio real em VGGish versus gerado. MusicGen-small em MusicCaps: 4.5. MusicLM: 4.0. Baixo melhor.

> **FAD（Fréchet 音频距离）。**O que é o que acontece com o VGGish?

**CLAP Score.**Pontuação de alinhamento de texto-áudio usando embalagens CLAP. &gt; 0,3 = alinhamento razoável.

> **CLAP 分数。**Utilize CLAP 嵌入文本-音频对齐分数──大于0.3 = 合理对齐──

**Listening panel MOS.**Ainda a última palavra para música de nível de consumo. Suno v5 ELO 1293 no TTS Arena (de preferências humanas emparelhadas).

> **听音评审团 MOS。**O ELO de Suno v5 no TTS Arena é 1293 ((provém de uma comparação com a preferência humana) ").

### Indicadores de referência de áudio

> 音频语言基准测试

**MMAU (Massive Multi-Audio Understanding).**10 mil pares de áudio-QA.

> **MMAU（大规模多音频理解）。**10 mil.

**MMAU-Pro.**1800 itens rígidos, quatro categorias: fala / som / música / multi-audio. 25% acaso em quatro vias. Gemini 2.5 Pro em geral ~ 60%; multi-audio ~ 22% em todos os modelos.

> **MMAU-Pro。**1800 个难题,四个类别:语音/声音/音乐/多音频──4 选 1 随机猜测 25%──Gemini 2.5 Pro 整体约60%;所有模型在多音频上约22%──

**LongAudioBench.**Clips de vários minutos com consultas semânticas.

> **LongAudioBench。**Talvez钟音频片段 + 语义查询──Audio Flamingo Next 超过 Gemini 2.5 Pro──

**AudioCaps / Clotho.**Captioning benchmarks. SPICE, CIDER, FENSE métricas.

> **AudioCaps / Clotho。**音频描述基准测试──SPICE、CIDER、FENSE 指标──

### Transmissão de fala para fala

> 流式语音到语音指标

**Latency P50 / P95 / P99.**O relógio de parede do end-of-user-speech para a primeira resposta audível.

> **延迟 P50 / P95 / P99。**Desde o usuário de voz terminar até o primeiro som de resposta real.

**WER / MOS**- A saída.

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              **WER / MOS**- Não.

**Barge-in responsiveness.**Tempo de interrupção do usuário para assistente mudo.

> **打断响应时间。**Desde o tempo de interrupção do usuário até o tempo de assistência silenciosa.

### As tabela de liderança de 2026

| Leaderboard | Tracks | URL |
|------------|--------|-----|
| Open ASR Leaderboard (HF) / 开源 ASR 排行榜（HF） | English + multilingual + long-form / 英语 + 多语言 + 长音频 | `huggingface.co/spaces/hf-audio/open_asr_leaderboard` |
| TTS Arena (HF) / TTS 竞技场（HF） | English TTS / 英语 TTS | `huggingface.co/spaces/TTS-AGI/TTS-Arena` |
| Artificial Analysis Speech / Artificial Analysis 语音 | TTS + STT, ELO from paired votes / TTS + STT，配对投票 ELO | `artificialanalysis.ai/speech` |
| MMAU-Pro / MMAU-Pro | LALM reasoning / LALM 推理 | `mmaubenchmark.github.io` |
| SpeakerBench / VoxSRC / 说话人基准 / VoxSRC | Speaker recognition / 说话人识别 | `voxsrc.github.io` |
| MMAU music subset / MMAU 音乐子集 | Music LALM / 音乐 LALM | （在 MMAU 内） |
| HEAR benchmark / HEAR 基准 | Self-supervised audio / 自监督音频 | `hearbenchmark.com` |

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.




## Construí-lo e realizei-o.
```figure
sp-wer-align
```

## Construí-lo

### Passo 1: REM com normalização

> 步骤 1: levar a WER padronizada

```python
from jiwer import wer, Compose, ToLowerCase, RemovePunctuation, Strip

transform = Compose([ToLowerCase(), RemovePunctuation(), Strip()])
score = wer(
    truth="Please turn on the lights.",
    hypothesis="please turn on the light",
    truth_transform=transform,
    hypothesis_transform=transform,
)
# ~0.17
```

### Passo 2: TTS WER de ida e volta

> 步骤 2: TTS 回环 WER

```python
def ttr_wer(tts_model, asr_model, texts):
    errors = []
    for txt in texts:
        audio = tts_model.synthesize(txt)
        recog = asr_model.transcribe(audio)
        errors.append(wer(truth=txt, hypothesis=recog))
    return sum(errors) / len(errors)
```

### Passo 3: SECS para clonagem de voz

> 步骤 3:语音克隆的SECS

```python
from speechbrain.inference.speaker import EncoderClassifier
sv = EncoderClassifier.from_hparams("speechbrain/spkrec-ecapa-voxceleb")

emb_ref = sv.encode_batch(load_wav("reference.wav"))
emb_clone = sv.encode_batch(load_wav("cloned.wav"))
secs = torch.nn.functional.cosine_similarity(emb_ref, emb_clone, dim=-1).item()
```

### Passo 4: FAD para geração de música

> 步骤 4: FAD do gerador de música

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()
score = fad.get_fad_score("generated_folder/", "reference_folder/")
```

### Passo 5: EER para a verificação dos alto-falantes (o mesmo código que a lição 6)

> 步骤 5: 话话人验证的 EER(与第六课相同的代码)

```python
def eer(same_scores, diff_scores):
    thresholds = sorted(set(same_scores + diff_scores))
    best = (1.0, 0.0)
    for t in thresholds:
        far = sum(1 for s in diff_scores if s >= t) / len(diff_scores)
        frr = sum(1 for s in same_scores if s < t) / len(same_scores)
        if abs(far - frr) < best[0]:
            best = (abs(far - frr), (far + frr) / 2)
    return best[1]
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.





> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

Aparar cada implantação com um arnes de avaliação fixo que é executado em cada atualização do modelo.

> Cada implantação é equipada com um instrumento de avaliação fixo, em cada modelo atualizado.

1. **Normalize before scoring.**Baixa letra, linha de pontuação, número expandido, informe a regra de normalização.
   Tradução:**评分前标准化。**转小写、去标点、数字展开―― relatório normas de padronização―
2. **Report distributions, not averages.**P50/P95/P99 para latência. Recall por classe para classificação.
   Tradução:**报告分布而非均值。**延迟用P50/P95/P99──分类用每类召回率──MMAU用每类──
3. **Run one canonical public benchmark.**Mesmo que os seus dados de produção sejam diferentes, relatar no Open ASR / TTS Arena / MMAU permite que os revisores comparem maçãs a maçãs.
   Tradução:**运行一个权威公共基准。**Mesmo que os seus dados de produção sejam diferentes, o relatório do Open ASR / TTS Arena / MMAU pode permitir que os avaliadores façam uma comparação justa.



## Encurralagens

> 常见陷

- **UTMOS extrapolation.**Treinado em discurso limpo no estilo VCTK; pontuação ruidosa / clonado / áudio emocional mal.
  Tradução:**UTMOS 外推问题。**Em VCTK 风格的纯净语音上训练;对杂/克隆/情感语音评分效果差──
- **MOS panel bias.**20 trabalhadores da Amazon Mechanical Turk ≠ 20 usuários alvo. Pague por um painel de domínio se as apostas forem altas.
  Tradução:**MOS 评审团偏差。**20 个 Amazon Mechanical Turk 工作者不等于 20 个目标用户──如果风险高,花钱请领域专家评审团──
- **FAD depends on reference set.**Comparar com a mesma distribuição de referência entre os modelos.
  Tradução:**FAD 依赖参考集。**跨模型比较时使用相同的参考分布──
- **Aggregate WER.**Uma REM de 5% em geral pode ocultar 30% da REM em discurso acentuado.
  Tradução:**汇总 WER。**O total de 5% de WER pode ocultar 30% de WER, segundo o relatório do grupo de pesquisa populacional.
- **Public benchmark saturation.**A maioria dos modelos de fronteira está perto do teto em referência padrão.
  Tradução:**公共基准饱和。**A maioria dos modelos de vanguarda na base padrão já se aproxima do telhado.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-audio-evaluator.md`Selecionar métricas, referências e formato de relatório para qualquer lançamento de modelo de áudio.

> 保存为 `outputs/skill-audio-evaluator.md`◊ Para qualquer modelo de rádio publicar um indicador de seleção, um modelo de base e um modelo de relatório.

## Exercícios.

1. **Easy.**Corra .`code/main.py`- Calcular WER / CER / EER / SECS / FAD-ish / MMAU-ish em entradas de brinquedos.
   Tradução:**简单。**运行 `code/main.py` Em jogo                                                                                                                                                                                                                                                             
2. **Medium.**Construir um arame WER de ida e volta TTS. Exibir sua saída Kokoro ou F5-TTS através de Whisper. Compute WER acima de 50 instruções. Flag instruções com WER &gt; 10%.
   Tradução:**中等。**Construir TTS 回环 WER 评估工具──用 Whisper 处理你的 Kokoro 或 F5-TTS 输出──在 50 个提示上计算 WER──标记 WER 大于10% 的提示──
3. **Hard.**Marque a sua escolha de aula 10 LALM em discurso MMAU-Pro + subconjuntos de áudio múltiplos (50 itens cada).
   Tradução:**困难。**Em MMAU-Pro's语音 + 多音频子集上 ([[50 条各) 项目) 评价您第十 课选择的 LALM──报告每类准确率并与发表数据对比──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| WER | ASR score | `(S+D+I)/N` at word level after normalization. / 标准化后的词级 `(S+D+I)/N` |
| CER | Character WER | For tone languages or char-level systems. / 用于声调语言或字符级系统 |
| MOS | Human opinion | 1-5 rating; 20+ listeners × 100 samples. / 1-5 分评分；20+ 听者 × 100 样本 |
| UTMOS | ML MOS predictor | Learned model; correlates ~0.9 with human MOS. / 学习型模型；与人类 MOS 相关性约 0.9 |
| SECS | Voice-clone similarity | ECAPA cosine between reference and clone. / 参考与克隆之间的 ECAPA 余弦相似度 |
| EER | Speaker verif score | Threshold where FAR = FRR. / FAR = FRR 的阈值 |
| DER | Diarization score | (FA + Miss + Confusion) / total. / (虚警 + 漏检 + 混淆) / 总时间 |
| FAD | Music-gen quality | Fréchet distance on VGGish embeddings. / VGGish 嵌入上的 Fréchet 距离 |
| RTFx | Throughput | Audio seconds per wall-clock second. / 每实际秒处理的音频秒数 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [jiwer](https://github.com/jitsi/jiwer) Biblioteca WER/CER com utilitários de normalização.
  O WER/CER 库
- [UTMOS (Saeki et al. 2022)](https://arxiv.org/abs/2204.02152)Aprendi a prever o MOS.
  UTMOS(Saeki 等 2022) 学习型 MOS 预测器。
- [Fréchet Audio Distance (Kilgour et al. 2019)](https://arxiv.org/abs/1812.08466)- O padrão da geração musical.
  Frechet Audio Distance(Kilgour 等 2019) 音乐生成的标准指标──
- [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) 2026 rankings ao vivo.
  Open ASR 排行榜2026 实时排名──
- [TTS Arena](https://huggingface.co/spaces/TTS-AGI/TTS-Arena) TTS líder de votos humanos.
  TTS Arena humanos votando 排行榜
- [MMAU-Pro benchmark](https://mmaubenchmark.github.io/) Lista de resultados de raciocínio da LALM.
  MMAU-Pro 基准LALM 推理排行榜──
- [HEAR benchmark](https://hearbenchmark.com/) Referências de SSL de áudio.
  OUR 基准音频 SSL 评估基准。

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

