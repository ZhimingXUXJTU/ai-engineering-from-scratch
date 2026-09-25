# O Presidente Reconhecimento e Verificação Falar Identificação e Verificação de Pessoas

> A ASR pergunta "o que eles disseram?" O reconhecimento do orador pergunta "quem disse isso?" A matemática parece a mesma  embebimentos mais cosino  mas cada decisão de produção depende de um único número EER.

> **【中文解读】**ASR 问"说了什么",说话人识别问"谁说的"―― matemática parece ser assim embutida em massa +余弦相似度, mas cada decisão de produção depende de um EER等误差率) 值──EER 越低,系统越可靠──

> **【拓展：声纹识别应用】**声纹识别用于银行电话认证、智能音箱用户识别、安防监控──声纹(voz impressão) é uma importante divisão da identificação de características biológicas.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 22 (Embedding Models) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 22（嵌入模型）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## O problema é o problema da introdução

Um usuário diz uma senha. Você quer saber: é essa a pessoa que eles afirmam ser (*verificação*, 1:1), ou é a primeira pessoa no seu banco de inscrição (*identificação*, 1:N)?

> Usagi: Você sabe que é a primeira pessoa que eles afirmam ser? ou é que é a primeira pessoa que você escreveu?

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

Pre-2018: GMM-UBM + i-vectores. EER razoável, mas frágil para mudança de canal (telefone vs laptop) e emoção. 20182022: x-vectores (backbone TDNN treinado com margem angular). 2022+: ECAPA-TDNN e WavLM-embeddings grandes. Em 2026 o campo é dominado por três modelos e uma métrica.

> 2018 前年:GMM-UBM + i-vectores。EER 合理但对信道偏移(电话 vs 笔记本) 和情绪敏感。2018-2022:x-vectors(用角度间隔训练的 TDNN 骨干)。2022+:ECAPA-TDNN 和 WavLM-large 嵌入──到2026年,该领域由三个模型和一个指标主导────

A métrica é**EER** Taxa de erro igual. Defina o seu limite de decisão para que a taxa de aceitação falsa = taxa de rejeição falsa. O crossover é EER.

> Este indicador é**EER**等错误率──设定决策值使假接受率 =假拒绝率──交叉点就是 EER──用于每篇论文、每排行榜、每采购评审──

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![Enrollment + verification pipeline with embedding + cosine + EER](../assets/speaker-verification.svg)

**The pipeline.**Inscrição: registar 530 segundos do alto-falante alvo; calcular uma incorporação de dimensão fixa (192-d para ECAPA-TDNN, 256-d para WavLM-large). Verificação: obter a incorporação da expressão do teste; calcular a semelhança cosínica; comparar com um limiar.

> **流水线。**Registrar: registar objetivo falar pessoa 5-30 segundos语音; calcular dimensão fixa embutida(ECAPA-TDNN 为 192 维,WavLM-large 为 256 维) 

**ECAPA-TDNN (2020, still dominant 2026).**Emfatizada Atenção ao Canal, Propagação e Agregação - Rede Neural de Atraso no Tempo. Blocos de convos 1D com excitação de compressão, concentração de atenção em várias cabeças, seguido por uma camada linear de 192-d. Treinado em VoxCeleb 1+2 (2,700 alto-falantes, 1,1M pronunciamentos) com perda de margem angular aditiva (AAM-softmax).

> **ECAPA-TDNN（2020，2026 年仍占主导）。**Emfoque no tempo de concentração da atenção, da disseminação e da concentração da rede neuronal.

**WavLM-SV (2022+).**Ajuste a espinha dorsal de SSL grande WavLM pré-entrenada com perda de AAM. Qualidade mais alta, mas mais lenta  300+ MB vs 15 MB.

> **WavLM-SV（2022+）。**Usar AAM 损失微调预训练的 WavLM-large SSL 骨干──质量更高但更慢300+ MB vs 15 MB──

**x-vector (baseline).**TDNN + compartilhamento de estatísticas. Clássico; ainda útil em CPU / borda.

> **x-vector（基线）。**TDNN + 统计池化── clásico; ainda útil em dispositivos de CPU/margem

**AAM-softmax.**Softmax padrão com margem adicionada `m`no espaço angular: `cos(θ + m)`Forças de separação angular inter-classe.`m=0.2`, escala `s=30`- Não .

> **AAM-softmax。**Em angular espaço, adicione espaço.`m`                                                                                                                                                                                                                                                              `cos(θ + m)` Força de classe entre ângulos de separação  valor típico `m=0.2`, emagrecer`s=30`- Não.

### Ponto de pontuação

> ### 评分

- **Cosine**A decisão baseada em limiares.
  **余弦**A semelhança, calculada entre inscrição e test emplacamento.
- **PLDA (Probabilistic LDA).**Embedings de projeto em um espaço latente onde o mesmo alto-falante vs. alto-falante diferente tem uma relação de probabilidade de forma fechada. Adicionado em cima do cosino para uma redução de +1020% de EER. padrão pré-2020; agora usado apenas em configurações fechadas.
  **PLDA（概率 LDA）。**O projeto será inserido no espaço potencial, em que os interlocutores com o mesmo discurso contra os interlocutores com o mesmo discurso têm um tipo de comparação fechada.
- **Score normalization.** `S-norm`ou `AS-norm`A normalização de cada pontuação em relação a uma coorte de meios impostores e etc.
  **分数归一化。** `S-norm`Ou `AS-norm`O valor médio e o padrão de diferença dos grupos de iniciantes são necessários para cada divisão.

### Números que você deve saber (2026)

> 2026 ano que você deve saber números

| Model | VoxCeleb1-O EER | Params | Throughput (A100) |
|-------|-----------------|--------|-------------------|
| x-vector (classic) | 3.10% | 5 M | 400× RT |
| ECAPA-TDNN | 0.87% | 15 M | 200× RT |
| WavLM-SV large | 0.42% | 316 M | 20× RT |
| Pyannote 3.1 segmentation + embedding | 0.65% | 6 M | 100× RT |
| ReDimNet (2024) | 0.39% | 24 M | 100× RT |

| 模型 | VoxCeleb1-O EER | 参数量 | 吞吐量（A100） |
|------|-----------------|--------|----------------|
| x-vector（经典） | 3.10% | 500 万 | 400× 实时 |
| ECAPA-TDNN | 0.87% | 1500 万 | 200× 实时 |
| WavLM-SV large | 0.42% | 3.16 亿 | 20× 实时 |
| Pyannote 3.1 分割 + 嵌入 | 0.65% | 600 万 | 100× 实时 |
| ReDimNet（2024） | 0.39% | 2400 万 | 100× 实时 |

### Diarização

> ### 说话人日志 ((谁在何时说话)

"Quem falou quando" em um clip de alto-falantes. Pipeline: VAD → segmento → embebed cada segmento → cluster (aglomerativo ou espectral) → limites suaves.`pyannote.audio`3.1, que agrupa a segmentação de alto-falantes + incorporação + agrupamento por trás de uma chamada.

> 多说话人音频中"谁在何时说话"──流水线:VAD → 分段 → 对每段嵌入 → 聚类(层聚类或谱聚类)→ 平滑边界──现代技术:`pyannote.audio`3.1,将说话人分割 + 嵌入 + 聚类打包为一个调用──2026 ano AMI 上 SOTA DER 约15%(de 2022 ano 23% 下降)──

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.



## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

```figure
sp-eer-crossover
```

## Construí-lo

### Passo 1: inserção de brinquedos a partir das estatísticas da MFCC

```python
def embed_mfcc_stats(signal, sr):
    frames = featurize_mfcc(signal, sr, n_mfcc=13)
    mean = [sum(f[i] for f in frames) / len(frames) for i in range(13)]
    std = [
        math.sqrt(sum((f[i] - mean[i]) ** 2 for f in frames) / len(frames))
        for i in range(13)
    ]
    return mean + std  # 26-d
```

Não é só para ensinar.`code/main.py`utiliza isto como prova de conceito em dados de alto-falantes sintéticos.

> 离 SOTA 差得远仅用于教学──`code/main.py`A partir de então, o sistema de dados de pessoas foi desenvolvido.

### Passo 2: semelhança cosínica + limiar

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0

def verify(enroll, test, threshold=0.75):
    return cosine(enroll, test) >= threshold
```

### Passo 3: EER a partir de pares de semelhanças

```python
def eer(same_scores, diff_scores):
    thresholds = sorted(set(same_scores + diff_scores))
    best = (1.0, 1.0, 0.0)  # (fa, fr, threshold)
    for t in thresholds:
        fr = sum(1 for s in same_scores if s < t) / len(same_scores)
        fa = sum(1 for s in diff_scores if s >= t) / len(diff_scores)
        if abs(fa - fr) < abs(best[0] - best[1]):
            best = (fa, fr, t)
    return (best[0] + best[1]) / 2, best[2]
```

Retorno (eer, threshold_at_eer).

> 返回 (eer, threshold_at_eer) ⋅两者都要报告──

### Passo 4: produção com SpeechBrain

```python
from speechbrain.pretrained import EncoderClassifier

clf = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

# enroll: average the embeddings of 3-5 clean samples
enroll = torch.stack([clf.encode_batch(load(x)) for x in enrollment_clips]).mean(0)
# verify
score = clf.similarity(enroll, clf.encode_batch(load("test.wav"))).item()
verdict = score > 0.25   # ECAPA typical threshold; tune on your data
```

### Passo 5: Diário com pyannote

```python
from pyannote.audio import Pipeline

pipe = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
diarization = pipe("meeting.wav", num_speakers=None)
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"{turn.start:.1f}–{turn.end:.1f}  {speaker}")
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.





> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

A pilha de 2026:

> Tecnologia de 2026:

| Situation | Pick |
|-----------|------|
| Closed-set 1:1 verification, edge | ECAPA-TDNN + cosine threshold |
| Open-set verification, cloud | WavLM-SV + AS-norm |
| Diarization (meetings, podcasts) | `pyannote/speaker-diarization-3.1` |
| Anti-spoofing (replay / deepfake detection) | AASIST or RawNet2 |
| Tiny embedded (KWS + enrollment) | Titanet-Small (NeMo) |

| 场景 | 选择 |
|------|------|
| 封闭集 1:1 验证，边缘设备 | ECAPA-TDNN + 余弦阈值 |
| 开放集验证，云端 | WavLM-SV + AS-norm |
| 说话人日志（会议、播客） | `pyannote/speaker-diarization-3.1` |
| 反欺诈（回放/深度伪造检测） | AASIST 或 RawNet2 |
| 小型嵌入式（关键词检测 + 注册） | Titanet-Small（NeMo） |



## Encurralagens

> 常见陷

- **Channel mismatch.**Modelo treinado em VoxCeleb (vídeo web) ≠ áudio de chamada telefônica.
  **信道不匹配。**O modelo de treinamento no VoxCeleb não é igual ao de telefone.
- **Short utterances.**O EER degrada-se acentuadamente abaixo dos 3 segundos de áudio do ensaio.
  **短语音。**测试音频低于3秒时 EER 剧恶化──
- **Enrollment with noise.**Uma inscrição barulhenta envenena a âncora.
  **带噪注册。**Uma lista de amostras de encomenda em inglês é composta por três amostras de encomenda em inglês.
- **Fixed threshold across conditions.**Sempre ajuste o limiar num conjunto de desenvolvimento de destino.
  **跨条件固定阈值。**始终在目标领域的留出开发集上调整值──
- **Cosine on non-normalized embeddings.**L2-normalizar primeiro; caso contrário, a magnitude domina.
  **未归一化嵌入上的余弦。**Antes de fazer L2 归一化;否则模值会占主导.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-speaker-verifier.md`- Seleção de modelo, protocolo de inscrição, plano de ajuste de limiares e proteção contra fraude.

> 保存为 `outputs/skill-speaker-verifier.md` Seleção de modelos, acordos de inscrição, programas de avaliação e medidas de prevenção da fraude.

## Exercícios.

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


1. **Easy.**Corra .`code/main.py`- Construir "alto-falantes" sintéticos (profis de tom diferentes), inscrever, calcular o EER numa lista de ensaio de 100 pares.
   **简单。**运行 `code/main.py`◊ Construir sintet"说话人" ([[不同音调配置), registrar, calcular EER em 100 para a lista de ensaios ◊
2. **Medium.**Use o SpeechBrain ECAPA em 30 pronunciamentos VoxCeleb1 (5 alto-falantes × 6 cada).
   **中等。**Em 30 条 VoxCeleb1 语音上使用SpeechBrain ECAPA(5 个说话人 × 6 条) ――用余弦和 PLDA 计算 EER。
3. **Hard.**Construir o registro completo → diário → verificar pipeline com `pyannote.audio`Avaliação de DER no set de desenvolvimento de AMI.
   **困难。**- Não .`pyannote.audio`构建完整的注册 → 日志 → 验证流水线──在 AMI 开发集上评估 DER──

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| EER | The headline metric | Threshold where False Accept = False Reject. |
| Verification | 1:1 | "Is this Alice?" |
| Identification | 1:N | "Who is speaking?" |
| Open-set | Unknown possible | Test set can contain unenrolled speakers. |
| Enrollment | Registering | Computing a speaker's reference embedding. |
| AAM-softmax | The loss | Softmax with additive angular margin; forces cluster separation. |
| PLDA | Classic scoring | Probabilistic LDA; likelihood-ratio scoring on top of embeddings. |
| DER | Diarization metric | Diarization Error Rate — miss + false alarm + confusion. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| EER | 头条指标 | 假接受率 = 假拒绝率时的阈值。 |
| 验证 | 1:1 | "这是 Alice 吗？" |
| 识别 | 1:N | "谁在说话？" |
| 开放集 | 可能有未知者 | 测试集可包含未注册的说话人。 |
| 注册 | 登记 | 计算说话人的参考嵌入。 |
| AAM-softmax | 那个损失 | 带加性角度间隔的 softmax；强制聚类分离。 |
| PLDA | 经典评分 | 概率 LDA；嵌入之上的似然比评分。 |
| DER | 日志指标 | 说话人日志错误率——漏检 + 误检 + 混淆。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Snyder et al. (2018). X-Vectors: Robust DNN Embeddings for Speaker Recognition](https://www.danielpovey.com/files/2018_icassp_xvectors.pdf)O papel clássico de inserção profunda.
  Snyder 等 (2018). X-Vectors:说话人识别的鲁棒 DNN 嵌入经典的深度嵌入论文──
- [Desplanques et al. (2020). ECAPA-TDNN](https://arxiv.org/abs/2005.07143)Arquitetura dominante 20202026.
  Desplanques et al. (2020). ECAPA-TDNN2020-2026 anos de ocupação predominante de arquitetura
- [Chen et al. (2022). WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing](https://arxiv.org/abs/2110.13900) Espécie vertebral SSL para SV e diarização.
  Chen 等 (2022). WavLM: Full语音处理大规模自监督预训SV 和日志的SSL 骨干──
- [Bredin et al. (2023). pyannote.audio 3.1](https://github.com/pyannote/pyannote-audio) Diarização da produção + estaca de incorporação.
  Bredin 等 (2023). pyannote.audio 3.1生产级日志 + 嵌入技术。
- [VoxCeleb leaderboard (updated 2026)](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/) classificações actuais das EER em todos os modelos.
  VoxCeleb 排行榜(2026年更新) 各模型当前 EER 排名──

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

