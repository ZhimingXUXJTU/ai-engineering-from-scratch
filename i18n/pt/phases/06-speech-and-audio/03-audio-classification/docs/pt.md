# Classificação de áudio  De k-NN em MFCC para AST e BEATs  音频分类  De MFCCs+KNN para AST 和 BEATs

> Tudo, desde "barbão de cão vs sirena" até "que idioma é este" é classificação de áudio. As características são mels. A arquitetura muda a cada década. A avaliação permanece AUC, F1, e recall por classe.

> **【中文解读】**De "dog calling还是警笛" a "这是什么语言", são todas as audi频分类──特征用 Mel,架构每个时代都在变化(MFCC+kNN → CNN → Transformer), avaliação de índice始终是 AUC、F1 和每类召回率──AST(Audio Spectrogram Transformer) e BEATs são atuais SOTA──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 3 · 06 (CNNs), Phase 5 · 08 (CNNs & RNNs for Text) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 3 · 06（CNN），阶段 5 · 08（文本的 CNN 与 RNN）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## O problema é o problema da introdução

Você recebe um clipe de 10 segundos. Você quer saber: "o que é isso?" Som urbano (sirena, perfuração, cão), comando de fala (sim/não/stop), ID de idioma (en/es/ar), emoção do alto-falante (nervosos/neutros), ou som ambiental (interior/exterior, babble). Todos estes são *audioclassificação*, e em 2026 a arquitetura de base está madura: log-mel → CNN ou Transformer → softmax.

> Você consegue um parágrafo de 10 segundos de rádio. Você sabe: "O que é isso?"

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

O problema principal não é a rede. São dados. Os conjuntos de dados de áudio têm desequilíbrio de classe brutal, forte mudança de domínio (limpo vs barulhento) e ruído de rótulo (quem decidiu "barulho urbano" vs "ruído de restaurante"?).

> O problema principal não está na rede, mas no dados. O grupo de dados tem uma série de tipos de desequilíbrio, de deslocamento de áreas fortes e de ruído de etiqueta. Quem definia "ruído de cidade" contra ruído de restaurante?

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![Audio classification ladder: k-NN on MFCCs to AST to BEATs](../assets/audio-classification.svg)

**k-NN on MFCCs (the 1990s baseline).**MFCCs planos por clipe, computa a semelhança cosina com um banco rotulado, devolve a maioria do voto do topo K. Surpreendentemente forte em conjuntos de dados limpos e pequenos (Comandos de fala, ESC-50).

> **MFCC 上的 k-NN（1990 年代基线）。**Para calcular a similaridade de cada segmento do MFCC, a maioria dos votos de K 个 retornará ao seu volume de dados.

**2D CNN on log-mels (2015-2019).**Tratar o`(T, n_mels)`O sistema de log-mail é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de log-mail, que é um sistema de-mail, ou de-mail, ou de-mail, ou de-mail, e que é um sistema de-mail, e-mail, e-mail, e-mail, e-mail, e-mail, e-mail, e-mail, e-mail, e-mail.

> **log-mel 上的 2D CNN（2015-2019）。**- Não .`(T, n_mels)`O sistema de log-mail é usado para processar imagens. Utiliza o ResNet-18 ou o VGG.

**Audio Spectrogram Transformer, AST (2021-2024).**Parchear o log-mail (por exemplo, 16×16 parches), adicionar inserções de posição, alimentar um ViT. O estado da técnica no AudioSet (mAP 0.485) para aprendizagem supervisionada.

> **音频频谱图 Transformer，AST（2021-2024）。**将 log-mail 分块(如 16×16 块),添加位置嵌入,送入 ViT──AudioSet 上监督学习的 SOTA(mAP 0.485)──

**BEATs and WavLM-base (2024-2026).**Pre-treinamento auto-supervisionado em milhões de horas. Ajuste a sua tarefa com 1-10% dos dados supervisionados que você precisaria. Em 2026 este é o ponto de partida padrão para áudio não- fala. BEATs-iter3 bate o AST em 1-2 mAP no AudioSet enquanto usa 1/4 da computação.

> **BEATs 和 WavLM-base（2024-2026）。**Em milhões de horas de dados, a supervisão de pré-treino. Usando 1-10% dos dados de supervisão que você deveria precisar, é um ponto de partida padrão para o uso de um sistema de rádio.

**Whisper-encoder as a frozen backbone (2024).**Pegue o codificador do Whisper, deixe cair o decodificador, anexe um classificador linear.

> **Whisper 编码器作为冻结骨干（2024）。**取 Whisper 的编码器,丢弃解码器,接一个线性分类器──在语言ID 和简单事件分类上接近SOTA,无需任何音频增强──"免费午餐"基线──

### O desequilíbrio de classes é o verdadeiro desafio

> ### O desequilíbrio é o verdadeiro desafio .

ESC-50: 50 classes, 40 clips cada  equilibrado, fácil. UrbanSound8K: 10 classes, desequilibrado 10:1. AudioSet: 632 classes com uma cauda longa de 100.000:1. Técnicas que funcionam:

> ESC-50:50 个类, por classe 40 个片段平衡、简单。UrbanSound8K:10 个类,10:1 不平衡。AudioSet:632 个类,长尾比例 100,000:1──有效的技术:

- Amostragem equilibrada durante a formação (não na avaliação).
  訓練時平衡采样 () 
- Mistura: interpolar linearmente dois clips (e as suas etiquetas) como aumento.
  Mixup: 线性插值两段音频 (→ "Mixagem de texto") e seu 标签 (→ "Mixagem de texto")
- SpecAugment: mascarar as bandas de tempo e frequência aleatórias.
  EspecAugment: escuridão com tempo e frequência.

### Avaliação

> ###  avaliação

- Exclusividade multiclasse (Comando de fala): precisão superior a 1, precisão superior a 5.
  Talvez os comandos de fala: top-1 准确率、top-5 准确率。
- Multiclasse multi-etiqueta (AudioSet, UrbanSound-style): média de precisão média (mAP).
  Talvez tipo de tags:
- Gravemente desequilibrado: recall por classe + macro F1.
  严重不平衡: cada classe de recrutamento + 宏观 F1──

Números 2026 que você deve saber:

> 2026 ano que você deve saber números:

| Benchmark | Baseline | SOTA 2026 | Source |
|-----------|----------|-----------|--------|
| ESC-50 | 82% (AST) | 97.0% (BEATs-iter3) | BEATs paper (2024) |
| AudioSet mAP | 0.485 (AST) | 0.548 (BEATs-iter3) | HEAR leaderboard 2026 |
| Speech Commands v2 | 98% (CNN) | 99.0% (Audio-MAE) | HEAR v2 results |

| 基准测试 | 基线 | 2026 SOTA | 来源 |
|----------|------|-----------|------|
| ESC-50 | 82%（AST） | 97.0%（BEATs-iter3） | BEATs 论文（2024） |
| AudioSet mAP | 0.485（AST） | 0.548（BEATs-iter3） | HEAR 排行榜 2026 |
| Speech Commands v2 | 98%（CNN） | 99.0%（Audio-MAE） | HEAR v2 结果 |

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.

> **【拓展：语音隐私与安全】**语音数据 contém uma grande quantidade de informações pessoais de privacidade (→ "faixas") 语音数据包含大量个人隐私信息 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音数据 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音音音水印 (→ "Audio Watermarking") 音纹反欺诈 (→ "Anti-faixas") 音纹) 音反欺诈 (→ "Anti-faixas") 音) 音) 音音是当前研究热点点.





## Construí-lo e realizei-o.
```figure
mfcc-pipeline
```

## Construí-lo

### Passo 1: featurizar

```python
def featurize_mfcc(signal, sr, n_mfcc=13, n_mels=40, frame_len=400, hop=160):
    mag = stft_magnitude(signal, frame_len, hop)
    fb = mel_filterbank(n_mels, frame_len, sr)
    mels = apply_filterbank(mag, fb)
    log = log_transform(mels)
    return [dct_ii(frame, n_mfcc) for frame in log]
```

### Passo 2: resumo de duração fixa

```python
def summarize(mfcc_frames):
    n = len(mfcc_frames[0])
    mean = [sum(f[i] for f in mfcc_frames) / len(mfcc_frames) for i in range(n)]
    var = [
        sum((f[i] - mean[i]) ** 2 for f in mfcc_frames) / len(mfcc_frames) for i in range(n)
    ]
    return mean + var
```

Simples mas fortes: média + variância através do tempo dá uma incorporação fixa de 26 dimensões para um MFCC de 13 covas. Funciona instantaneamente.

>  Simple mas eficaz: valor médio no eixo do tempo + 方差 é 13 números MFCC  deu 26 维固定嵌入──运行瞬间── em ESC-50  até 2017 ainda pode vencer o SOTA então

### Passo 3: k-NN

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1e-12
    nb = math.sqrt(sum(x * x for x in b)) or 1e-12
    return dot / (na * nb)

def knn_classify(q, bank, labels, k=5):
    sims = sorted(range(len(bank)), key=lambda i: -cosine(q, bank[i]))[:k]
    votes = Counter(labels[i] for i in sims)
    return votes.most_common(1)[0][0]
```

### Passo 4: atualização para a CNN em log-mels

Em PyTorch:

```python
import torch.nn as nn

class AudioCNN(nn.Module):
    def __init__(self, n_mels=80, n_classes=50):
        super().__init__()
        self.body = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.head = nn.Linear(128, n_classes)

    def forward(self, x):  # x: (B, 1, T, n_mels)
        return self.head(self.body(x).flatten(1))
```

Parâmetros 3M. Trens em ~ 10 min no ESC-50 com uma única RTX 4090.

> 300 milhões de parâmetros.

### Passo 5: os 2026 padrão  de ajuste fino BEATs

```python
from transformers import ASTFeatureExtractor, ASTForAudioClassification

ext = ASTFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
model = ASTForAudioClassification.from_pretrained(
    "MIT/ast-finetuned-audioset-10-10-0.4593",
    num_labels=50,
    ignore_mismatched_sizes=True,
)

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


inputs = ext(audio, sampling_rate=16000, return_tensors="pt")
logits = model(**inputs).logits
```

Para BEATs, use `microsoft/BEATs-base`através do `beats`biblioteca; a API dos transformadores é da mesma forma.

> Para os batidos, através`beats`库使用 `microsoft/BEATs-base`;transformers API de forma igual:




> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

A pilha de 2026:

> Tecnologia de 2026:

| Situation | Start with |
|-----------|-----------|
| Tiny dataset (<1000 clips) | k-NN on MFCC means (your baseline) + audio augmentation |
| Medium dataset (1K–100K) | BEATs or AST fine-tune |
| Large dataset (>100K) | Train from scratch or fine-tune Whisper-encoder |
| Real-time, edge | 40-MFCC CNN, quantized to int8 (KWS-style) |
| Multi-label (AudioSet) | BEATs-iter3 with BCE loss + mixup + SpecAugment |
| Language ID | MMS-LID, SpeechBrain VoxLingua107 baseline |

| 场景 | 起始方案 |
|------|----------|
| 小数据集（<1000 段） | MFCC 均值上的 k-NN（基线）+ 音频增强 |
| 中等数据集（1K–100K） | BEATs 或 AST 微调 |
| 大数据集（>100K） | 从零训练或微调 Whisper 编码器 |
| 实时、边缘设备 | 40-MFCC CNN，量化为 int8（关键词检测风格） |
| 多标签（AudioSet） | BEATs-iter3 + BCE 损失 + mixup + SpecAugment |
| 语言识别 | MMS-LID，SpeechBrain VoxLingua107 基线 |

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


Regra de decisão: **start with a frozen backbone, not a fresh model**A ponta de uma cabeça da BEATs dá-lhe 95% de SOTA em horas, não semanas.

>  决策规则:**从冻结骨干开始，而不是从头训练模型**❖ A classificação dos BEATs pode atingir 95% da SOTA em algumas horas, em vez de algumas semanas.



## Envia-o . Produto .

Salva como`outputs/skill-classifier-designer.md`Selecionar arquitetura, aumentos, estratégia de equilíbrio de classes e métricas de avaliação para uma determinada tarefa de classificação de áudio.

> 保存为 `outputs/skill-classifier-designer.md`◊ para uma determinada categoria de tarefas de escolha de estrutura, estratégias de reforço, estratégias de equilíbrio e indicadores de avaliação.

## Exercícios.

1. **Easy.**Corra .`code/main.py`. Ele treina a linha de base do K-NN MFCC em um conjunto de dados sintéticos de 4 classes (tons puros em diferentes tons).
   **简单。**运行 `code/main.py`◊ É em 4 tipos de dados sintetizados ([[ diferentes sons de alta pureza]])
2. **Medium.**Substitui`summarize`A agregação de 4 momentos bate a média + var no mesmo conjunto de dados sintéticos?
   **中等。**- Não .`summarize`替换为 [média, var, skew, kurtosis]──四矩池化是否在相同合成数据集上优于平均值+方差?
3. **Hard.**Usando`torchaudio`, treinar uma CNN 2D no ESC-50 de dobrar 1. relatar a precisão de validação cruzada 5 vezes. Adicionar SpecAugment (mascaras de tempo = 20, mascaras de freqüência = 10) e relatar o delta.
   **困难。**Utilização `torchaudio`, em ESC-50 dobra 1 上訓練 2D CNN── relatório 5 折交叉验证准确率──添加 具体Augment(时间掩码 = 20,频率掩码 = 10)并报告差值──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| AudioSet | The ImageNet of audio | Google's 2M-clip, 632-class weakly-labeled YouTube dataset. |
| ESC-50 | Small classification benchmark | 50 classes × 40 clips of environmental sounds. |
| AST | Audio Spectrogram Transformer | ViT on log-mel patches; 2021 SOTA. |
| BEATs | Self-supervised audio | Microsoft model, iter3 leads AudioSet as of 2026. |
| Mixup | Pair augmentation | `x = λ·x1 + (1-λ)·x2; y = λ·y1 + (1-λ)·y2`. |
| SpecAugment | Mask-based augmentation | Zero-out random time and frequency bands of the spectrogram. |
| mAP | Main multi-label metric | Mean average precision across classes and thresholds. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| AudioSet | 音频界的 ImageNet | Google 的 200 万片段、632 类弱标注 YouTube 数据集。 |
| ESC-50 | 小型分类基准 | 50 类 × 40 个环境声音片段。 |
| AST | 音频频谱图 Transformer | log-mel 块上的 ViT；2021 SOTA。 |
| BEATs | 自监督音频 | 微软模型，iter3 截至 2026 年领先 AudioSet。 |
| Mixup | 配对增强 | `x = λ·x1 + (1-λ)·x2; y = λ·y1 + (1-λ)·y2`。 |
| SpecAugment | 掩码增强 | 将频谱图的随机时间和频率带置零。 |
| mAP | 主要多标签指标 | 各类别和阈值的平均精度均值。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Gong, Chung, Glass (2021). AST: Audio Spectrogram Transformer](https://arxiv.org/abs/2104.01778) a arquitetura de registro de 20212024.
  Gong, Chung, Glass (2021). AST:音频频谱图 Transformer2021-2024 年的记录架构──
- [Chen et al. (2022, rev. 2024). BEATs: Audio Pre-Training with Acoustic Tokenizers](https://arxiv.org/abs/2212.09058) o padrão de 2024+.
  Chen 等 (2022, 修订 2024). BEATs:声学 tokenizer 的音频预训练2024+ 的默认选择──
- [Park et al. (2019). SpecAugment](https://arxiv.org/abs/1904.08779) o aumento de áudio dominante.
  Park 等 (2019). SpecAugmentMainstream音频增强方法──
- [Piczak (2015). ESC-50 dataset](https://github.com/karolpiczak/ESC-50) 50 classes de referência que vive.
  Piczak (2015). ESC-50 dados → continuamente utilizados 50 类基准──
- [Gemmeke et al. (2017). AudioSet](https://research.google.com/audioset/)Taxonomia do YouTube de classe 632; ainda o padrão de ouro.
  Gemmeke 等 (2017). AudioSet632 类 YouTube 分类体系; ainda é um padrão de ouro.

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

