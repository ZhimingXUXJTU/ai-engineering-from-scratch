# Voz Antivitamento e Áudio Marcação de Água  ASVspoof 5, AudioSeal, WaveVerify 语音防伪与音频水印

> A clonagem de voz foi enviada mais rápido do que as defesas. Os sistemas de voz de produção de 2026 precisam de duas coisas: um detector (AASIST, RawNet2) que classifica fala real vs falsa, e uma marca de água (AudioSeal) que sobrevive à compressão e edição.

> **【中文解读】**O sistema de produção de voz de 2026 anos precisa de duas coisas: um testeiro (AASIST, RawNet2) e um sistema de gravação (AudioSeal) para manter a sua vida após a compressão e a edição.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 06 (Speaker Recognition), Phase 6 · 08 (Voice Cloning) | **前置知识:** 阶段 6 · 06（说话人识别），阶段 6 · 08（语音克隆）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## O problema é o problema da introdução

Três defesas relacionadas:

> Três meios de defesa:

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.


1. **Anti-spoofing / deepfake detection.**Dado um vídeo de áudio, é sintético ou real? ASVspoof benchmarks (ASVspoof 2019 → 2021 → 5) são o padrão de ouro.
   Tradução:**反欺骗/深度伪造检测。**给定一段音频,判断它是合成的还是真实的?ASVspoof 基准测试(ASVspoof 2019 → 2021 → 5) é o padrão ouro。
2. **Audio watermarking.**Embed um sinal imperceptível em áudio gerado que um detector pode extrair mais tarde.
   Tradução:**音频水印。**Em embutidos em um sinal incompreensível, depois de um testeiro, pode-se extrair.
3. **Authenticated provenance.**Assinatura criptográfica de arquivos de áudio + metadados.
   Tradução:**认证来源。**音频文件 + 元数据的加密签名──C2PA / 内容真实性倡议──

A detecção lida com adversários que não cooperam. A marca de água lida com o cumprimento.

> 检测应对不配合的攻击者──水印应对合规性AI 生成的音频应被识别──2026 ano são necessários──

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![Anti-spoofing vs watermarking vs provenance — three defense layers](../assets/spoofing-watermark.svg)

### ASVspoof 5  o índice de referência 2024-2025

> ASVspoof 5  2024-2025 年基准测试

A maior mudança das edições anteriores:

> A maior variação em relação à versão anterior:

- **Crowdsourced data**- Não é um estúdio limpo.
  Tradução:**众包数据**(Non-registrado棚纯净数据)
- **~2000 speakers**(versus ~ 100 antes).
  Tradução:**约 2000 名说话人**(até 100 nomes)
- **32 attack algorithms.**TTS + conversão de voz + perturbação adversária.
  Tradução:**32 种攻击算法。**TTS + 语音转换 + 对抗性扰动──
- **Two tracks.**Contro-medida (CM) detecção independente; ASV (SASV) robusto em falsificação para sistemas biométricos.
  Tradução:**两个赛道。**Anti-fraude (SSAV)

Estado da arte em ASVspoof 5: ~ 7,23% EER. No ASVspoof mais antigo 2019 LA: 0,42% EER. Desplojamento no mundo real: espere 5-10% EER em clips no meio selvagem.

> ASVspoof 5 上的SOTA:约7.23% EER──在较旧 ASVspoof 2019 LA 上:0.42% EER──实际部署:预期在野外音频上 EER为5-10%──

### Famílias de modelos de detecção AASIST e RawNet2 

> AASIST 和 RawNet2  检测模型家族

**AASIST**(2021, atualizado até 2026). Atenção gráfica às características espectrais. SOTA atual sobre a tarefa de contra-medida ASVspoof 5.

> **AASIST**(Ao final de 2021, continuará a ser atualizado até 2026) ⋅ baseado em mecanismos de atenção para os dados da frequência de dados e das características da sua rede de dados.

**RawNet2.**Convolução frontal sobre forma de onda bruta + espinha dorsal TDNN. Linha de base mais simples; ainda competitiva com ajuste fino.

> **RawNet2。**O primeiro é o primeiro, o segundo é o segundo.

**NeXt-TDNN + SSL features.**Variante 2025: ECAPA-style + WavLM recursos + perda focal. Atinge a 0,42% EER em ASVspoof 2019 LA.

> **NeXt-TDNN + SSL 特征。**2025 年变体:ECAPA 风格 + WavLM 特征 + focal loss──在 ASVspoof 2019 LA 上达到0.42% EER──

### AudioSeal  o 2024 marca de água padrão

> AudioSeal  2024 ano de água

Meta's **AudioSeal**(Jan 2024, v0.2 Dec 2024).

> Meta de **AudioSeal**(2024 年 1 月,v0.2 于 2024 年 12 月) ⋅

- **Localized.**Detecta a marca de água por quadro em resolução de amostra de 16 kHz (1/16000 s).
  Tradução:**局部化。**E 16 kHz 采样分辨率逐检测水印 ((1/16000 秒) ⋅
- **Generator + detector jointly trained.**O gerador aprende a incorporar um sinal inaudible; o detector aprende a encontrá-lo através de aumentos.
  Tradução:**生成器 + 检测器联合训练。**O sistema de aprendizagem é um sistema de aprendizagem de aprendizagem de aprendizagem de aprendizagem de aprendizagem.
- **Robust.**Sobrevive à compressão MP3 / AAC, EQ, velocidade de mudança ±10%, mistura de ruído +10 dB SNR.
  Tradução:**鲁棒。**能经受 MP3/AAC 压缩,均衡, ±10% 变速, +10 dB SNR 噪声混合,
- **Fast.**O detector funciona a 485x em tempo real, 1000x mais rápido do que o WavMark.
  Tradução:**快速。**O testeiro funciona 485 vezes na velocidade real; Comparado com o WavMark 快 1000 vezes.
- **Capacity.**Carga útil de 16 bits (pode codificar ID de modelo, timestamp de geração, ID de usuário) incorporável em cada expressão.
  Tradução:**容量。**16 位载荷(可编码模型 ID、生成时间、用户 ID) pode ser inserido em cada段语音──

### WavMark

A linha de base aberta pré-AudioSeal. Rede neural invertível, 32 bits/seg.

> AudioSeal 之前的开源基线──可逆神经网络,32 位/秒──问题:

- A sincronização da força bruta é lenta.
  O que é que é violência?
- Pode ser removido por ruído gaussiano ou compressão MP3.
  Tradução do inglês: Canção de alto ruído ou MP3
- Não é amigável em tempo real.
  Não se adapta ao cenário real.

### WaveVerify (julho de 2025)

Resolve as fraquezas do AudioSeal  especificamente manipulações temporais (inversion, velocidade). Utiliza gerador baseado em FiLM + detector de mistura de especialistas. Competitivo com o AudioSeal em ataques padrão; lida com edições temporais.

> WaveVerify(2025 年 7 月) ・ resolver os pontos fracos do AudioSeal 特别是时间操作(反转、变速) ・ usar baseado em FiLM 的生成器 + MoE 检测器──在标准攻击上与 AudioSeal 相当;能处理时间编辑──

### Os adversários exploram a lacuna

De AudioMarkBench: "em baixo da mudança de pitch, todas as marcas de água mostram Bit Recovery Accuracy abaixo de 0,6, indicando remoção quase completa". **Pitch-shift is the universal attack.**A marca de água no 2026 é totalmente robusta para modificações agressivas de tom. É por isso que você precisa de detecção (AASIST) ao lado da marca de água.

> 攻击者利用的漏洞──来自 AudioMarkBench:"Em baixa frequência de baixa frequência, a taxa de recuperação de todos os sinais de água é inferior a 0,6, o que indica que foram quase completamente eliminados".""**音高偏移是通用攻击。**Não há nenhum tipo de água em 2026 que possa resistir ao aumento da alta de volume.

### C2PA / Iniciativa de Autenticidade de Conteúdo

Não é uma técnica de ML  um formato manifesto. Os arquivos de áudio carregam metadados criptograficamente assinados sobre a ferramenta de criação, autor, data. Audobox / Seamless usá-lo. Bom para a proveniência; não faz nada se um mau ator recodificar e strip metadados.

> C2PA / 内容真实性倡议──不是机器学习技术 é uma forma simples──音频文件携带关于创建工具、作者、日期的加密签名元数据──Audobox / Seamless 使用它── é favorável à traçabilidade; mas se os malintencionados re-códigos e desprestigiarem os dados são ineficazes──

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.

> **【拓展：语音隐私与安全】**语音数据 contém uma grande quantidade de informações pessoais de privacidade (→ "faixas") 语音数据包含大量个人隐私信息 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音数据 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音音音水印 (→ "Audio Watermarking") 音纹反欺诈 (→ "Anti-faixas") 音纹) 音反欺诈 (→ "Anti-faixas") 音) 音) 音音是当前研究热点点.




## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

```figure
v4-audio-watermark
```

## Construí-lo

### Passo 1: um simples detector de características espectrais (joguete)

> 步骤 1: simples de frequência de testes de características

```python
def spectral_rolloff(spec, percentile=0.85):
    cum = 0
    total = sum(spec)
    if total == 0:
        return 0
    threshold = total * percentile
    for k, v in enumerate(spec):
        cum += v
        if cum >= threshold:
            return k
    return len(spec) - 1

def is_suspicious(audio):
    spec = magnitude_spectrum(audio)
    rolloff = spectral_rolloff(spec)
    return rolloff / len(spec) > 0.92
```

A fala sintética tem frequência de alta frequência, mas a intuição é válida.

> O sintetizador de voz geralmente tem alta frequência de energia anormalmente plana.

### Passo 2: AudioSeal embutida + detectada

> 步骤 2:AudioSeal 嵌入 + 检测

```python
from audioseal import AudioSeal
import torch

generator = AudioSeal.load_generator("audioseal_wm_16bits")
detector = AudioSeal.load_detector("audioseal_detector_16bits")

audio = load_wav("generated.wav", sr=16000)[None, None, :]
payload = torch.tensor([[1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0]])
watermark = generator.get_watermark(audio, sample_rate=16000, message=payload)
watermarked = audio + watermark

result, decoded_payload = detector.detect_watermark(watermarked, sample_rate=16000)
# result: float in [0, 1] — probability of watermark presence
# decoded_payload: 16 bits; match against embedded payload
```

### Passo 3: avaliação  EER

> 步骤 3: avaliar  EER(等 err err err err err err rate)

```python
def eer(real_scores, fake_scores):
    thresholds = sorted(set(real_scores + fake_scores))
    best = (1.0, 0.0)
    for t in thresholds:
        far = sum(1 for s in fake_scores if s >= t) / len(fake_scores)
        frr = sum(1 for s in real_scores if s < t) / len(real_scores)
        if abs(far - frr) < best[0]:
            best = (abs(far - frr), (far + frr) / 2)
    return best[1]
```

### Passo 4: integração da produção

> 步骤 4: produção, nível de integração

```python
def safe_tts(text, voice, clone_reference=None):
    if clone_reference is not None:
        verify_consent(user_id, clone_reference)
    audio = tts_model.synthesize(text, voice)
    audio_with_wm = audioseal_embed(audio, payload=build_payload(user_id, model_id))
    manifest = c2pa_sign(audio_with_wm, user_id, timestamp=now())
    return audio_with_wm, manifest
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


Cada navio de geração: (1) marca de água, (2) manifesto assinado, (3) registro de auditoria conforme às políticas de retenção.

> Cada geração de output são incluídos: 1) água, 2) assinatura, 3) conformidade com a estratégia de retenção.




> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

| Use case | Defense |
|----------|---------|
| Shipping TTS / voice cloning / 上线 TTS/语音克隆 | AudioSeal embed on every output (non-negotiable) / 每次输出嵌入 AudioSeal（不可妥协） |
| Biometric voice unlock / 生物识别语音解锁 | AASIST + ECAPA ensemble; liveness challenge / AASIST + ECAPA 集成；活体挑战 |
| Call-center fraud detection / 呼叫中心欺诈检测 | AASIST on 20% sample of incoming calls / 对 20% 的来电做 AASIST 检测 |
| Podcast authenticity / 播客真实性 | C2PA signing on upload, AudioSeal if AI-generated / 上传时 C2PA 签名，AI 生成则加 AudioSeal |
| Research / training detectors / 研究/训练检测器 | ASVspoof 5 train/dev/eval sets / ASVspoof 5 训练/开发/评估集 |



## Encurralagens

> 常见陷

- **Watermark without detector ever running.**Envia o detector para o teu informador.
  Tradução:**嵌入水印但从未运行检测器。**Não há sentido.
- **Detection without calibration.**AASIST treinado em sobre-exames de LA, redução de precisão no mundo real.
  Tradução:**检测未校准。**A AASIST irá ser treinado em ASVspoof LA; a taxa de precisão real vai diminuir.
- **Pitch-shift gap.**A mudança de pitch agressiva remove a maioria das marcas de água.
  Tradução:**音高偏移漏洞。**激进的音高偏移能去除大多数水印──preparar检测作为后备──
- **Metadata strip-and-rehost.**C2PA é trivialmente evitável por recodificação. Sempre adicione a defesa criptográfica + perceptual (marca de água) juntas.
  Tradução:**元数据剥离重新托管。**C2PA 通過重新编码即可輕易绕過──始终同时使用加密 + 感知(水印) defenção──
- **Liveness as detection.**Peça ao usuário para dizer uma frase aleatória.
  Tradução:**活体检测作为检测手段。**Deixe o usuário dizer um "razão curta": pode prevenir ataques reinstalados, mas não pode prevenir o real-time clonão:

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-spoof-defender.md`Selecionar o modelo de detecção, a marca de água, o manifesto de proveniência e o manual operacional para a implantação de uma geração de voz.

> 保存为 `outputs/skill-spoof-defender.md`◊ Para um programa de produção de idiomas, um modelo de pesquisa de águas, um código de origem e um manual de operação.

## Exercícios.

1. **Easy.**Corra .`code/main.py`- Detector de brinquedos + marca de água de brinquedos embutida/detectada em áudio sintético.
   Tradução:**简单。**运行 `code/main.py`                                                                                                                                                                                                                                                              
2. **Medium.**Instalação`audioseal`, incorporar uma carga útil de 16 bits numa saída TTS, recodificar, corromper o áudio com ruído e medir a precisão de recuperação de bits.
   Tradução:**中等。**Instalação`audioseal`, em TTS 输出中嵌入 16位载荷,重新解码──用噪音损坏音频并测量位恢复准确率──
3. **Hard.**Tune-se em linha reta um RawNet2 ou AASIST em ASVspoof 2019 LA. Mese a EER. Teste em um conjunto de clips gerados por F5-TTS  ver como a detecção de OOD se degrada.
   Tradução:**困难。**Em ASVspoof 2019 LA 上微调 RawNet2 或 AASIST──测 EER──在留出的F5-TTS 生成音频集上测试观察 OOD 检测的退化程度──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| ASVspoof | The benchmark | Biennial challenge; 2024 = ASVspoof 5. / 双年挑战赛；2024 = ASVspoof 5 |
| CM (countermeasure) | Detector | Classifier: real speech vs synthetic / converted. / 分类器：真实语音 vs 合成/转换语音 |
| SASV | Speaker verif + CM | Integrated biometric + spoof detection. / 集成生物识别 + 欺骗检测 |
| AudioSeal | Meta watermark | Localized, 16-bit payload, 485× faster than WavMark. / 局部化，16 位载荷，比 WavMark 快 485 倍 |
| Bit Recovery Accuracy | Watermark survival | Fraction of payload bits recovered after attack. / 攻击后恢复的载荷位比例 |
| C2PA | Provenance manifest | Cryptographic metadata about creation / authorship. / 关于创建/作者身份的加密元数据 |
| AASIST | Detector family | Graph-attention-based anti-spoofing SOTA. / 基于图注意力的反欺骗 SOTA |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Todisco et al. (2024). ASVspoof 5](https://dl.acm.org/doi/10.1016/j.csl.2025.101825) o indicador de referência actual.
  O que é que se passa com o novo modelo?
- [Defossez et al. (2024). AudioSeal](https://arxiv.org/abs/2401.17264) o signo de água padrão.
  Defossez 等(2024).
- [Chen et al. (2025). WaveVerify](https://arxiv.org/abs/2507.21150)Detetor de MoE para ataques temporais.
  Chen 等(2025). WaveVerify  em relação ao tempo de ataque de MoE 检测器──
- [Jung et al. (2022). AASIST](https://arxiv.org/abs/2110.01200) a espinha dorsal de detecção de SOTA.
  Jung 等(2022). AASISTSOTA 检测骨干──
- [AudioMarkBench (2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d9b7775296a641a1913ab6b4425d5e8-Paper-Datasets_and_Benchmarks_Track.pdf) Avaliação da robustez.
  AudioMarkBench ((2024) 鲁棒性评估──
- [C2PA specification](https://c2pa.org/specifications/specifications/) formato do manifesto de proveniência.
  C2PA 规范来源清单格式──

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

