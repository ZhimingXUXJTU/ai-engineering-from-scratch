# Geração de vídeos

> Uma imagem é um tensor 2D. Um vídeo é um 3D. A teoria é a mesma; a computação é 10-100 vezes mais difícil. Sora da OpenAI (Feb 2024) provou que era possível. Em 2026 Veo 2, Kling 1.5, Runway Gen-3, Pika 2.0, e WAN 2.2 vídeo de produção de navio a partir de texto em 1080p  e o open-weights stack (CogVideoX, HunyuanVideo, Mochi-1, WAN 2.2) está 12 meses atrás.

> **【中文解读】**图像是2D 张量,视频是3D 张量,理论相同但计算量高 10-100 倍──Sora 证明可行,到2026年多个商业产品(Veo 2、Kling、Runway) já pode gerar 1080p 视频──

> **【拓展：Sora 的影响】**A Sora de OpenAI (OpenAI) é um dos mais populares circuitos de produção de vídeo de 2024-2026.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 7 · 09 (ViT), Phase 8 · 06 (DDPM)
**Time:** ~45 minutes

## O problema é o problema da introdução

Um vídeo 1080p de 10 segundos a 24 fps é de 240 quadros de 1920×1080×3 pixels. Isso é cerca de 1,5 GB de dados brutos por clip. A difusão no espaço de pixels é impossível. Você precisa:

> 10 segundos 1080p 24fps  vídeo é 240  1920×1080×3 像素, cerca de 1,5 GB de dados primitivos──像素空间扩散不可行──你需要:

1. **Spatiotemporal compression.**Um VAE que codifica vídeos, não quadros, em uma sequência de parches espaciais-temporais.
   **时空压缩。**将视频(而非) codificar para o tempo空补丁序列的 VAE──
2. **Temporal coherence.**Os quadros precisam compartilhar conteúdo, iluminação e identidade de objeto em segundos.
   **时间连贯性。** entre os dois precisam de partilha de conteúdo 、 luz e identidade de objeto 
3. **Compute budget.**O treinamento por vídeo é 10-100 vezes mais caro do que a imagem para o mesmo tamanho do modelo.
   **计算预算。**视频训练比图像贵 10-100 倍──
4. **Conditioning.**Texto, imagem (primeira tela), áudio ou outro vídeo.
   **条件化。**文本、图像(首)、音频或其他视频──

A arquitetura que resolveu isto é a**Diffusion Transformer (DiT)**A primeira é a de um grupo de dados de um grupo de dados, que é aplicado a parches espaciotemporais, treinados em grandes conjuntos de dados (impressão, legenda, vídeo).

>  resolver estas arquiteturas é**Diffusion Transformer (DiT)**應用時空補貼, training on large-scale dataset── 應用時空補貼, training on large-scale dataset── 應用時空補貼, training on large-scale dataset── 應用時空補貼, training on large-scale dataset── 應用時空補貼, training on large-scale dataset── 應用時空補貼, training on large-scale dataset── 應用時空補貼, training on large-scale dataset── 應用時空補貼, training on large-scale dataset── 應用時空補貼, training on large-scale dataset── 應用時空補貼, training on large-scale dataset── 應用時空補貼, training on large-scale data set── 應用時空補貼, training on the same spread loss, training on the same spread loss, with section 06 課6.

## O conceito central.

![Video diffusion: patchify, DiT, decode](../assets/video-generation.svg)

### Paragem

> ### Parcheamento

O vídeo é codificado com um VAE 3D (compressão espaciotemporal aprendida).`[T_latent, H_latent, W_latent, C_latent]`Dividido em pedaços de tamanho .`[t_p, h_p, w_p]`Para modelos de estilo Sora,`t_p = 1`(parches por quadro) ou `t_p = 2`Um vídeo 1080p de 10 segundos comprime para cerca de 20.000 a 100.000 parches.

> Usar 3D VAE 编码视频──潜在表示形状为 `[T, H, W, C]`│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │`[t_p, h_p, w_p]`10 segundos 1080p  vídeo comprimido para cerca de 2-100.000 parches 

### Dieta de espaço-tempo

> ### 时空 DiT

Um transformador processa a sequência plana de patches. Cada patch tem uma inserção posicional 3D (tempo + y + x).

> Transformador 处理展平的补丁序列──每个补丁有3D 位置编码(时间 + y + x)──注意力通常分解为:

- **Spatial attention**dentro dos parches de cada quadro.
  **空间注意力**Em cada um dos parches dentro.
- **Temporal attention**através de quadros no mesmo local espacial.
  **时间注意力**A mesma posição espacial do espaço.
- **Full 3D attention**É 16-100 vezes mais caro; só é utilizado em baixa resolução ou em investigação.
  **完整 3D 注意力**贵 16-100 倍; apenas em baixa resolução ou estudo.

> **【中文解读】**视频生成的核心技术:(1) 3D VAE 将视频压缩为时空潜在表示;(2) 将潜在表示切分为时空补丁;(3) DiT(Diffusion Transformer) processar sequência de parches, usando 3D 位置编码;(4) Atenção normalmente se divide em espaço atenção e tempo atenção para reduzir a quantidade de cálculo.

> **【拓展：Sora 架构与 DiT 在视频中的应用】**O núcleo de Sora é a expansão do pensamento de patchamento da ViT para o campo de vídeo. O vídeo será chamado de "Time Space Patch 序列" (série de patchamento de tempo em espaço). DiT (Diffusion Transformer) usará o Transformer (substituição de U-Net) como rede de ruído, mostrando uma melhor expansão na produção de vídeos.

### Condicionamento de texto

> ### 文本条件化

Atensão cruzada com um grande codificador de texto (T5-XXL para Sora, CogVideoX-5B usa T5-XXL).

> Usar um grande editor de texto para fazer um intercâmbio de atenção.

### Formação

> ### 訓練

Perda de difusão padrão (ε ou v previsão) sobre latentes espaciotemporais. Dados: vídeo web + ~ 100M clips curados + legendas de texto sintéticas. Computação: 10.000+ horas de GPU para mesmo uma pequena pesquisa; escala Sora é 100.000+.

> 时空潜在表示上的标准扩散损失──数据:网络视频 + 约1亿精选片段 + 合成文本标注──计算:小规模研究需要1万+ GPU 小时;Sora 规模是10万+──

## A paisagem de produção de 2026

| Model / 模型 | Date | Max duration / 最长时长 | Max res / 最高分辨率 | Open weights? / 开源？ | Notable / 亮点 |
|-------|------|--------------|---------|---------------|---------|
| Sora (OpenAI) | 2024-02 | 60s | 1080p | No | First model to show world simulator properties at scale / 首个展示世界模拟器属性的模型 |
| Sora Turbo | 2024-12 | 20s | 1080p | No | Production Sora at 5x faster inference / 5 倍推理加速 |
| Veo 2 (Google) | 2024-12 | 8s | 4K | No | Highest quality + physics in 2025 / 2025 年最高质量 |
| Veo 3 | 2025 Q3 | 15s | 4K | No | Native audio and stronger camera control / 原生音频 |
| Kling 1.5 / 2.1 (Kuaishou) | 2024-2025 | 10s | 1080p | No | Best human motion in 2025 Q1 / 最佳人体运动 |
| Runway Gen-3 Alpha | 2024-06 | 10s | 768p | No | Professional video tools on top / 专业视频工具 |
| Pika 2.0 | 2024-10 | 5s | 1080p | No | Strongest character consistency / 最强角色一致性 |
| CogVideoX (THUDM) | 2024 | 10s | 720p | Yes (2B, 5B) | First open 5B-scale video / 首个开源 5B 视频 |
| HunyuanVideo (Tencent) | 2024-12 | 5s | 720p | Yes (13B) | Open SOTA late 2024 / 2024 年末开源 SOTA |
| Mochi-1 (Genmo) | 2024-10 | 5.4s | 480p | Yes (10B) | Most permissively licensed / 最宽松许可 |
| WAN 2.2 (Alibaba) | 2025-07 | 5s | 720p | Yes | Strongest open model mid-2025 / 2025 年中最强开源 |

Os pesos abertos estão a fechar a lacuna mais rapidamente do que no espaço de imagem: HunyuanVideo + WAN 2.2 LoRAs já alimentam a maioria dos fluxos de trabalho de código aberto até meados de 2026.

> O peso da fonte aberta está a diminuir a diferença mais rapidamente do que no campo da imagem.

## Construí-lo e realizei-o.
```figure
video-diffusion-denoise
```

## Construí-lo

`code/main.py`Simula a ideia principal de DiT espacial-temporal: parchear um pequeno vídeo sintético, adicionar um inserimento de posição por parche e denotar toda a sequência com uma atenção de estilo transformador sobre os parches.

### Passo 1: parche um "vídeo" sintético 1D

```python
def make_video(T_frames=8, rng=None):
    # a "video" is a sequence of 1-D values following a smooth trajectory
    base = rng.gauss(0, 1)
    return [base + 0.3 * t + rng.gauss(0, 0.1) for t in range(T_frames)]
```

### Passo 2: inserção de posição por quadro

```python
def pos_embed(t, dim):
    return sinusoidal(t, dim)
```

### Passo 3: Denoiser vê toda a sequência

Em vez de denotar cada quadro de forma independente, nossa pequena rede concatenar todos os valores do quadro + suas inserções de posição e prever o ruído para todos os quadros em conjunto.

### Passo 4: Teste de coerência temporal

Após o treino, mostre um vídeo. Messe o delta frame-to-frame. Se o modelo tiver aprendido a estrutura temporal, os deltas permanecem menores do que a amostragem de cada quadro de forma independente.

## Encaixos.

- **Independent per-frame sampling = flicker.**Se executar a difusão de imagem em cada quadro separadamente, a saída de flash porque o ruído de cada quadro é independente.
- **Naive 3D attention = OOM.**A atenção 3D completa em uma 1080p latente de 10 segundos é centenas de bilhões de operações. Factorizem em espacial + temporal.
- **Data captioning matters more than size.**A principal atualização de Sora em relação ao trabalho anterior foi a formação em legendas mais detalhadas (clipes reetiquetados GPT-4).
- **First-frame conditioning.**A maioria dos modelos de produção também aceita uma imagem como a primeira tela.
- **Physics drift.**Os clips longos (> 10s) acumulam subtis inconsistências.

## Use-o com o framework implementado.

| Use case / 用途 | 2026 pick / 2026 选择 |
|----------|-----------|
| Highest-quality text-to-video, hosted / 最高质量托管 | Veo 3 or Sora |
| Camera-controlled cinematic / 相机控制电影感 | Runway Gen-3 with motion brushes |
| Character consistency across clips / 跨片段角色一致 | Pika 2.0 or Kling 2.1 |
| Open weights, fast fine-tune / 开源快速微调 | WAN 2.2 + LoRA |
| Image-to-video / 图生视频 | WAN 2.2-I2V, Kling 2.1 I2V, or Runway |
| Audio-to-video lip sync / 音频对口型 | Veo 3 (native audio) or a dedicated lip-sync model |
| Video editing / 视频编辑 | Runway Act-Two, Kling Motion Brush, Flux-Kontext (still-frame) |

O custo por segundo de vídeo na paridade de qualidade caiu 20 vezes entre 2024 e 2026.

> O custo de vídeo por segundo diminuiu 20 vezes entre 2024 e 2026.

## Envia-o . Produto .

Salvar`outputs/skill-video-brief.md`. A competência assume um vídeo breve (durada, relação de aspecto, estilo, plano da câmera, consistência do assunto, áudio) e as saídas: modelo + hospedagem, esquadrão de execução (linguagem da câmera, descrição do assunto, descrição de movimento), protocolo de semente + reprodução e uma lista de verificação de qualidade a nível de quadro.

## Exercícios.

1. **Easy.**- Não .`code/main.py`, comparar delta de quadro a quadro para a) amostragem independente por quadro, b) amostragem conjunta de sequência.
2. **Medium.**Adicione uma condição de primeiro quadro: quadro de pin 0 a um determinado valor e amostre o resto.
3. **Hard.**Use os difusores HuggingFace para executar o CogVideoX-2B em uma GPU local. Tempo 20 de inferência passa a 720p para um clipe de 6 segundos. Profila a atenção espaciotemporal para identificar o gargalo de engarrafamento.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Video VAE | "3-D VAE" | Encoder that compresses `(T, H, W, C)` → spatiotemporal latent. |
| Patches | "The tokens" | Fixed-size 3-D blocks of the latent; input to the DiT. |
| Factorized attention | "Spatial + temporal" | Run attention over space, then over time; skip full 3-D attention. |
| Image-to-video (I2V) | "Animate this photo" | Model takes an image + text, outputs a video that starts from it. |
| Keyframe conditioning | "Anchor frames" | Pin specific frames to control the video's arc. |
| Motion brush | "Directional hint" | UI input where the user paints motion vectors onto the image. |
| Re-captioning | "Dense captions" | Using an LLM to re-label training clips with detailed prompts. |
| Flicker | "Temporal artifact" | Frame-to-frame inconsistency; fixed with coupled denoising. |

## Nota de produção: vídeo latente é um problema de largura de banda de memória.

Um clip de 10 segundos em 1080p a 24 fps é de 240 quadros × 1920 × 1080 × 3 ≈ 1,5 GB de pixels brutos.`2 × spatial × 2 × temporal`O que é o problema é que o tempo de transmissão é de aproximadamente 100 MB por pedido.

Três botões de produção, todos diretamente do capítulo de inferência da literatura de produção-inferência:

- **TP across the DiT.**Os modelos de texto a vídeo são rotineiramente ≥10B parâmetros. TP = 4 em 4 H100s é padrão; PP = 2 × TP = 2 para modelos da classe 405B. A latência por passo cai aproximadamente linearmente com TP até a parede totalmente reduzida.
- **Frame batching = continuous batching.**No momento da geração, o vídeo é conceitualmente um lote de quadros ligados pela atenção.`t+1`enquanto enquadram`t-1`está a ser devolvido, se a arquitetura do modelo permitir a geração de janelas deslizantes.
- **Clip-level prefill cache.**Para imagem-a-vídeo, o condicionamento de primeira tela é análogo ao preenchimento de um LLM: compute-o uma vez, reutilize-o através dos passes do decodificador temporal.

## Mais leitura 延伸阅读

- [Brooks et al. (2024). Video generation models as world simulators](https://openai.com/index/video-generation-models-as-world-simulators/) Relatório técnico da Sora.
- [Yang et al. (2024). CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer](https://arxiv.org/abs/2408.06072) CogVideoX.
- [Kong et al. (2024). HunyuanVideo: A Systematic Framework for Large Video Generative Models](https://arxiv.org/abs/2412.03603) HunyuanVideo.
- [Genmo (2024). Mochi-1 Technical Report](https://www.genmo.ai/blog/mochi)Mochi-1.
- [Alibaba (2025). WAN 2.2](https://wanvideo.io/) abertura da SOTA em meados de 2025.
- [Ho, Salimans, Gritsenko et al. (2022). Video Diffusion Models](https://arxiv.org/abs/2204.03458) o papel de difusão de vídeo seminal.
- [Blattmann et al. (2023). Align your Latents (Video LDM)](https://arxiv.org/abs/2304.08818) Ancestral da Difusão de Vídeo Estabilizada.
