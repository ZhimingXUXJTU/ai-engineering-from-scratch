# Geração de Música  Geração de Música, Áudio estável, Suno, e o Terremoto de Licença  Geração de Música  Geração de Música  Áudio estável  Suno e direitos de autor

> A geração musical de 2026: Suno v5 e Udio v4 dominam os comerciais; MusicGen, Stable Audio Open e ACE-Step lideram o código aberto. O problema técnico é principalmente resolvido. O problema legal (Warner Music $ 500M acordo, UMG acordo) remodelaram o campo em 2025-2026.

> **【中文解读】**2026 年音乐生成:Suno v5 和 Udio v4 主导商业产品;MusicGen、Stable Audio Open 和 ACE-Step 领先开源;; problemas técnicos são fundamentalmente resolvidos, mas problemas legais(Warner Music 5 bilhões de dólares e acordo) em 2025-2026 reformula essa área;;

> **【拓展：AI 音乐的法律风暴】**A questão do direito de autor da AI produzir música provocou um terremoto na indústria da música.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 4 · 10 (Diffusion Models) | **前置知识:** 阶段 6 · 02（频谱图），阶段 4 · 10（扩散模型）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## O problema é o problema da introdução

Texto → um clipe musical de 30 segundos a 4 minutos, com letras, vocais e estrutura.

> 文本 → 30 秒到 4 分钟的音乐片段,带歌词、人声和结构──三子问题:

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

1. **Instrumental generation.**Texto como "bateria de hip-hop de lo-fi com teclas quentes" → áudio. MusicGen, Stable Audio, AudioLDM.
   **器乐生成。**Como "bateria de hip-hop com teclas quentes"
2. **Song generation (with vocals + lyrics).**"Canção country sobre noites chuvosas no Texas" → canção completa.
   **歌曲生成（带人声+歌词）。**"Canção country sobre noites chuvosas no Texas" → 完整歌曲──Suno、Udio、YuE、ACE-Step──
3. **Conditional / controllable.**Extender um clip existente, regenerar uma ponte, trocar gênero, separar-estampado ou inpaint.
   **条件/可控生成。**扩展现有片段、重新生成桥段、切换风格、分轨或内画──Udio de内画 + 分轨 é um recurso que deve ser alcançado em 2026―

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![Music generation: token-LM vs diffusion, the 2026 model map](../assets/music-generation.svg)

### Token LM em relação a tokens neurais-codec

> ### Baseado em Módulo de Módulo de Módulo de Módulo

Meta's **MusicGen**(2023, MIT) e muitos derivados: condição em embutidos de texto/melodia, prevê autoregressivamente tokens EnCodec (32 kHz, 4 codebooks), decodifica com EnCodec. Parâmetros 300M - 3.3B. Base forte; luta além de 30 segundos.

> Meta de **MusicGen**(2023, MIT) e muitos derivados: em texto /旋律嵌入为条件, auto-regreso预测 EnCodec token(32 kHz,4 个码本), com EnCodec 解码──3 bilhões a 33 bilhões de参数──强基线; mais de 30 秒效果下降──

**ACE-Step**(open source, 4B XL lançado em abril de 2026) estende isso para geração completa de letras.

> **ACE-Step**(Open Source, 4 de abril de 2026) vai se expandir para a produção de todos os produtos de Suno.

### Diffusão sobre fusões ou latentes

> ###  baseada em mel ou variação potencial

**Stable Audio (2023)**E ...**Stable Audio Open (2024)**É excelente em circuitos, design de som, texturas ambientais, não é ótimo em músicas estruturadas.

> **Stable Audio（2023）**和 **Stable Audio Open（2024）**O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é?

**AudioLDM / AudioLDM2**A comunicação de texto a áudio através de difusão latente de estilo T2I, generalizada para música, efeitos sonoros, fala.

> **AudioLDM / AudioLDM2**Por meio do T2I 风格, a potencial variação se espalha para o texto para a geração de áudio, para a geração de áudio para a música, a produção de áudio e a produção de áudio.

### Híbrido (produção)  Suno, Udio, Lyria

> ### 混合(生产)  Suno、Udio、Lyria

Pesos fechados. Provavelmente, o vocalista baseado em difusão com um codec AR LM + com cabeças de voz / tambor / melodia especializadas. Suno v5 (2026) é o líder de qualidade do ELO 1293.

> 闭源权重──可能是 AR 编解码 LM + 基于扩散的声码器,配有专门语音/鼓/旋律头──Suno v5(2026) é ELO 1293 质量领先者──Udio v4 增加内画 + 分轨(贝斯、鼓、人声分别下载)──

### Avaliação

> ###  avaliação

- **FAD (Fréchet Audio Distance).**Distância de nível de incorporação entre a distribuição de áudio gerada versus real usando recursos VGGish ou PANNs. Baixo é melhor. MusicGen pequeno: 4.5 FAD em MusicCaps; SOTA ~ 3.0.
  **FAD（Fréchet 音频距离）。**Utilize VGGish ou PANNs Features of generation vs 真实音频分布的嵌入级距离──越低越好──MusicGen pequeno:MusicCaps 上 4.5 FAD;SOTA 约 3.0──
- **Musicality (subjective).**Preferência humana. Suno v5 ELO 1293 leva.
  **音乐性（主观）。**O que é que é que é?
- **Text-audio alignment.**CLAP pontuação entre o prompt e saída.
  **文本-音频对齐。**提示与输出之间的 CLAP 分数──
- **Musicality artifacts.**Transições fora do ritmo, deriva vocal, perda de estrutura depois de 30 segundos.
  **音乐性伪影。**跑拍过渡、人声短语漂移、 mais de 30 segundos depois de a estrutura perder-se¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.



## Mapa modelo 2026

> Mapa de modelos de 2026

| Model | Params | Length | Vocals | License |
|-------|--------|--------|--------|---------|
| MusicGen-large | 3.3B | 30 s | no | MIT |
| Stable Audio Open | 1.2B | 47 s | no | Stability non-commercial |
| ACE-Step XL (Apr 2026) | 4B | > 2 min | yes | Apache-2.0 |
| YuE | 7B | > 2 min | yes, multilingual | Apache-2.0 |
| Suno v5 (closed) | ? | 4 min | yes, ELO 1293 | commercial |
| Udio v4 (closed) | ? | 4 min | yes + stems | commercial |
| Google Lyria 3 (closed) | ? | real-time | yes | commercial |
| MiniMax Music 2.5 | ? | 4 min | yes | commercial API |

| 模型 | 参数量 | 时长 | 人声 | 许可 |
|------|--------|------|------|------|
| MusicGen-large | 33 亿 | 30 秒 | 无 | MIT |
| Stable Audio Open | 12 亿 | 47 秒 | 无 | Stability 非商业 |
| ACE-Step XL（2026.04） | 40 亿 | > 2 分钟 | 有 | Apache-2.0 |
| YuE | 70 亿 | > 2 分钟 | 有，多语言 | Apache-2.0 |
| Suno v5（闭源） | ? | 4 分钟 | 有，ELO 1293 | 商业 |
| Udio v4（闭源） | ? | 4 分钟 | 有 + 分轨 | 商业 |
| Google Lyria 3（闭源） | ? | 实时 | 有 | 商业 |
| MiniMax Music 2.5 | ? | 4 分钟 | 有 | 商业 API |

## O cenário jurídico (2025-2026)

> ## 法律环境(2025-2026)

- **Warner Music vs Suno settlement.**$500 milhões. A WMG agora tem supervisão da semelhança com a IA, direitos de música e faixas geradas pelo usuário no Suno.
  **Warner Music 诉 Suno 和解。**500 milhões de dólares. WMG agora tem o direito de supervisionar a similaridade da AI de Suno, direitos de gravação e usuário de conteúdo gerado.
- **EU AI Act**+ **California SB 942**A música gerada pela IA deve ser divulgada.
  **EU AI 法案**+ **加利福尼亚 SB 942**A música que eu faço tem de ser revelada.
- **Riffusion / MusicGen**Não há nenhuma equipa de conformidade no MIT, mas também não há vocais comerciais.
  **Riffusion / MusicGen**Não há nenhuma carga de conformidade, mas também não há voz de empresário.

Padrões de segurança para embarque:

> Modelo de segurança:

1. Gerenar apenas instrumentos (MusicGen, Stable Audio Open, MIT/CC0 de saída).
   仅生成器乐(MusicGen、Stable Audio Open、MIT/CC0 输出)
2. Use APIs comerciais (Suno, Udio, ElevenLabs Music) com licença por geração.
   Utilize带每次生成许可的商业API (Suno, Audio, ElevenLabs Music)
3. Trem em catálogo de propriedade ou licenciado (a maioria das empresas acaba aqui).
   Em formação em catálogo de autodidactação (ou autorizado) a maioria das empresas acaba chegando a este passo.
4. Tag gerações com marcas de água + metadados.
   Usado para imprimir dados e dados.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.


## Construí-lo e realizei-o.
```figure
sp-codec-tokens
```

## Construí-lo

### Passo 1: gerar com MusicGen

```python
from audiocraft.models import MusicGen
import torchaudio

model = MusicGen.get_pretrained("facebook/musicgen-small")
model.set_generation_params(duration=10)
wav = model.generate(["upbeat synthwave with driving drums, 128 BPM"])
torchaudio.save("out.wav", wav[0].cpu(), 32000)
```

Três tamanhos: `small`(300M, rápido),`medium`(1.5B), `large`(3.3B) O pequeno é suficiente para "fazer aterrar a ideia".

> Três grandes:`small`(3 bilhões, rápido)`medium`(15 mil milhões)`large`(33 mil milhões)`small`足以验证"idea é possível?"

### Passo 2: Condicionamento da melodia

```python
melody, sr = torchaudio.load("humming.wav")
wav = model.generate_with_chroma(
    ["jazz piano cover"],
    melody.squeeze(),
    sr,
)
```

MusicGen-melody toma um cromagrama e preserva a melodia enquanto troca timbre. Útil para "dar-me essa melodia como um quarteto de cordas".

> MúsicaGênero-melodia                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

### Passo 3: Avaliação do FAD

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()

fad.get_fad_score("generated_folder/", "reference_folder/")
```

Computa distância de inserção VGGish. Útil para testes de regressão de nível de gênero; não substitui os ouvintes humanos.

> 計算 VGGish 嵌入距離── aplica-se ao teste de regresso de classe de classe; não pode substituir o público humano──

### Passo 4: adição ao fluxo de trabalho de Mestrado em Música

Combine com as ideias das lições 7-8:

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


```python
prompt = "Write a 30-second jazz loop. Describe the drums, bass, and piano voicing."
description = llm.complete(prompt)
music = musicgen.generate([description], duration=30)
```




> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

| Goal | Stack |
|------|-------|
| Instrumental sound design | Stable Audio Open |
| Game / adaptive music | Google Lyria RealTime (closed) |
| Full songs with vocals (commercial) | Suno v5 or Udio v4 with explicit license |
| Full songs with vocals (open) | ACE-Step XL or YuE |
| Short ad jingle | MusicGen melody-conditioned on a hummed reference |
| Music-video background | MusicGen + Stable Video Diffusion |

| 目标 | 技术栈 |
|------|--------|
| 器乐声音设计 | Stable Audio Open |
| 游戏/自适应音乐 | Google Lyria RealTime（闭源） |
| 带人声的完整歌曲（商业） | Suno v5 或 Udio v4 带明确许可 |
| 带人声的完整歌曲（开源） | ACE-Step XL 或 YuE |
| 短广告曲 | MusicGen 在哼唱参考上的旋律条件 |
| 音乐视频背景 | MusicGen + Stable Video Diffusion |



## Encurralagens que ainda se lançam em 2026

> 2026 ano ainda em vítima de um erro

- **Copyright-laundering prompts.**"Canção no estilo de Taylor Swift"  comercial Suno / Áudio filtro estes agora, modelos abertos não. Adicionar sua própria lista de filtros.
  **版权洗钱提示。**"Canção no estilo de Taylor Swift" Comércio Suno/Udio 现在会过这些,开源模型不会──添加你自己的过列表──
- **Repetition / drift past 30 s.**Modelos AR circuito. Crossfade múltiplas gerações, ou usar ACE-Step para a coerência estrutural.
  **超过 30 秒的重复/漂移。**AR 模型会循环──交叉淡进多个生成,或使用 ACE-Step 保持结构一致性──
- **Tempo drift.**Os modelos desviam-se do BPM. Use as etiquetas BPM no prompt e pós-filtro com librosa's `beat_track`- Não .
  **节奏漂移。**模型偏离 BPM──在提示中使用 BPM 标签并使用图书馆 的 `beat_track`- Não, não.
- **Vocal intelligibility.**O Suno é excelente; os modelos abertos são muitas vezes fracos em palavras.
  **人声清晰度。**Suno 表现出色; open source模型的歌词经常模糊──如果歌词重要,使用商业API或微调──
- **Mono output.**Os modelos abertos geram mono ou falso estereo.
  **单声道输出。**Open source model generating single soundway or fake sound.                                                                                                                                                                                                                                                         

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-music-designer.md`. Selecionar modelo, estratégia de licença, plano de comprimento / estrutura e divulgação de metadados para uma implantação de geração musical.

> 保存为 `outputs/skill-music-designer.md` For music generation deployment selection model、 licença estratégia、 duração/ estrutura plano e divulgação de dados。

## Exercícios.

1. **Easy.**Corra .`code/main.py`Ele produz uma progressão de acordes "generacional" + padrão de tambor como símbolos ASCII  um desenho animado de geração musical.
   **简单。**运行 `code/main.py`◊ É executado com um símbolo ASCII gerando "generação" e cordas + 鼓点一个音乐生成的卡通── pode ser jogado com um MIDI 染器──
2. **Medium.**Instalação`audiocraft`, gerar clips de 10 segundos em 4 conjuntos de gêneros com MusicGen-small, medir FAD contra um conjunto de gêneros de referência.
   **中等。**Instalação`audiocraft`, usando MusicGen-small em 4 流派提示上生成10秒片段,对照参考流派集测量 FAD──
3. **Hard.**Usando o ACE-Step (ou MusicGen-melody), gerar três variações da mesma melodia com diferentes pedidos de timbre.
   **困难。**Utilize ACE-Step (ou MusicGen-melody), usando diferentes sons de cores de suporte para gerar três variações da mesma melodia.

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| FAD | Audio FID | Fréchet distance between embedding distributions of real vs generated. |
| Chromagram | Melody as pitches | 12-dim per-frame vector; input to melody conditioning. |
| Stems | Instrument tracks | Separated bass / drums / vocals / melody as WAV. |
| Inpainting | Regen a section | Mask a time window; model regenerates just that. |
| CLAP | Text-audio CLIP | Contrastive audio-text embedding; eval text-audio alignment. |
| EnCodec | Music codec | Meta's neural codec used by MusicGen; 32 kHz, 4 codebooks. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| FAD | 音频 FID | 真实 vs 生成嵌入分布之间的 Fréchet 距离。 |
| 色度图 | 旋律即音高 | 12 维逐帧向量；旋律条件的输入。 |
| 分轨 | 乐器轨道 | 分离的贝斯/鼓/人声/旋律 WAV。 |
| 内画 | 重生成一段 | 遮蔽时间窗口；模型只重生成那部分。 |
| CLAP | 文本-音频 CLIP | 对比音频-文本嵌入；评估文本-音频对齐。 |
| EnCodec | 音乐编解码器 | Meta 的神经编解码器，MusicGen 使用；32 kHz，4 个码本。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Copet et al. (2023). MusicGen](https://arxiv.org/abs/2306.05284) o índice de referência autoregressivo aberto.
  Copet 等 (2023). MusicGen开源自归基准──
- [Evans et al. (2024). Stable Audio Open](https://arxiv.org/abs/2407.14358) o design de som padrão.
  Evans 等 (2024). Stable Audio Open声音设计默认选择──
- [ACE-Step](https://github.com/ace-step/ACE-Step)- Gerador de música completa 4B, abril de 2026.
  ACE-Step开源 40 亿参数全曲生成器,2026 年 4 月。
- [Suno v5 platform docs](https://suno.com) o líder da qualidade comercial.
  Suno v5 平台文档商业质量领先者──
- [AudioLDM2](https://arxiv.org/abs/2308.05734) difusão latente para música + efeitos sonoros.
  AudioLDM2音乐 + 音效的潜变量扩散──
- [WMG-Suno settlement coverage](https://www.musicbusinessworldwide.com/suno-warner-music-settlement/) Novembro 2025 precedente.
  WMG-Suno 和解报道2025 年 11 月判例──

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

