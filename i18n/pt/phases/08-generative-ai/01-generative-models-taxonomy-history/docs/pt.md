# Modelos geracionais  Taxonomia e História  生成模型  类与历史

> Cada modelo de imagem, modelo de texto, modelo de vídeo e modelo 3D cabe em um dos cinco baldes. Escolha o balde errado e você lutará com a matemática por semanas. Escolha o certo e os últimos 12 anos de progresso do campo se acumula limpo em sua cabeça.

> **【中文解读】**Todos os modelos de imagens, textos, vídeos e 3D podem ser classificados em cinco categorias: VAE, GAN, modelo de expansão, modelo de fluxo e modelo de auto-regressão.

> **【拓展：生成式 AI 的五大路线】**(1) VAE变分自编码器,Stable Diffusion 的编码器;(2) GAN生成对抗网络,StyleGAN 的核心;(3) 扩散模型DDPM/DDIM,当前图像生成主流;(4) 流模型Flow Matching,SD3/FLUX 的新方向;(5) 自归归GPT 模式,VAR 应用于图像──

**Type:** Learn / 学习型
**Languages:** Python
**Prerequisites:** Phase 2 (ML Fundamentals / 机器学习基础), Phase 3 (Deep Learning Core / 深度学习核心), Phase 7 · 14 (Transformers / Transformer)
**Time:** ~45 minutes

## O problema é o problema da introdução

Um modelo gerativo faz um trabalho: fornece amostras de formação extraídas de uma distribuição desconhecida `p_data(x)`As faces, frases, arquivos MIDI, estruturas de proteínas, todos os mesmos problemas se você piscar.

> O modelo de produção só faz uma coisa: é determinado por uma distribuição desconhecida.`p_data(x)`A produção de um modelo de treinamento extraído parece ser de uma nova amostra de distribuição igual.

O problema é que ...`p_data`A maioria dos modelos de geradores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de computadores de comput

> O problema está em`p_data`Existem em um espaço de milhões de dimensões ([[1张 512x512 RGB 图像约78.6万维]]), o modelo ocupa apenas uma forma fina no espaço, enquanto você pode ter apenas 1000 milhões de amostras. A densidade de cálculo violenta é desesperada.

Cinco famílias sobreviveram nos últimos doze anos. Saber que compromisso cada família faz nos diz por que ganha em algumas tarefas e desmorona em outras.

> Em 12 anos, cinco famílias modelo sobreviveram. Saber o que cada família fez de acordo, é saber por que ela venceu em certas tarefas e desmoronou em outras.

> **【中文解读】**O trabalho central do modelo é aprender a partir de um modelo de treinamento a partir de uma distribuição desconhecida p_data ((x), para gerar um novo modelo de distribuição igual. O desafio é o de um pequeno volume de dados em um espaço elevado.

> **【拓展：从扩散模型到 Flow Matching 的范式转移】**A tendência mais importante de 2024-2026 é a transferência do modelo de expansão (DDPM) para o fluxo de correspondência (Flow Matching) (Flow Matching) (Training Flow Matching) (Training Flow Matching) (Training Flow Matching) (Training Flow Matching) (Trening Flow Matching) (Trening Flow Matching) (Trening Flow Matching) (Trening Flow Matching) (Trening Flow Matching) (Trening Flow Matching) (Trening Flow Matching) (Trening Flow Matching) (Trening Flow Matching) (Trening Flow Matching) (Trening Flow Matching) (Trening Flow Matching) (Trening Flow Matching) (Trening Flow Matching) (Trening Flow Matching) ) (Trening Flow Matching Flow Matching) (Trenning Flow Matching) Flow Matching) (Trenning Flow Matching) Flow Matching Flow Matching (Trenning Flow Matching) Flow Matching) Flow Matching (Flow Matching) Flow Matching) Flow Matching) (Flow Matching) (Flow Matching) (Flow Matching) (Flow Matching) (Flow Matching) (Flow Matching) (Flow Matching) (Flow Matching) (Flow Matching) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (DDPM) (F) (D) (D) (D) (F) (D) (D) (F) (D) (D) (F) (D) (D) (D

## O conceito central.

![Five families of generative models — taxonomy by what they model](../assets/taxonomy.svg)

**1. Explicit density, tractable.**Escreva .`log p(x)`Os modelos autoregressivos (PixelCNN, WaveNet, GPT) factorizam`p(x) = ∏ p(x_i | x_<i)`- Construção de fluxos normalizados (RealNVP, Glow) `p(x)`Pro: probabilidade exata, perda de treinamento limpa. Con: inferência autoregressiva é sequencial (lento para sequências longas), fluxos precisam de arquiteturas invertíveis (arquiteturicamente restritivas).

> **1. 显式密度，可处理。**- Não .`log p(x)`写成可以实际求值的求和──自归归模型(PixelCNN、WaveNet、GPT) será distribuído em conjunto e dividido em conditionais distribuídos乘积──标准化流(RealNVP、Glow) através de simples distribuição de transformação de construção`p(x)`△优点:精确似然,训练损失清晰──缺点:自归推理是顺序的(长序列慢),流需要可逆架构(架构受限)。

**2. Explicit density, approximate.**- Não .`log p(x)`Os modelos de difusão (DDPM, Ho 2020) treinam um denoizador que otimiza implícitamente um ELBO ponderado. A difusão é a espinha dorsal dominante de imagem, vídeo e 3D em 2026.

> **2. 显式密度，近似。**De baixo ao baixo`log p(x)`(ELBO)并优化该下界──VAE Utilize编码器-解码器和变分后验──扩散模型训练去噪机,隐式优化加权 ELBO──扩散模型是2026年图像、视频和3D 的主导骨干──

**3. Implicit density.**Salte a densidade inteiramente; aprenda um gerador `G(z)`que produz amostras e um discriminador `D(x)`GANs (Goodfellow 2014). Rapidos na inferência (uma passagem para frente) mas notoriamente instáveis durante o treinamento. StyleGAN 1/2/3 permanece o estado da arte para fotorealismo de domínio fixo (faces, quartos) mesmo em 2026.

> **3. 隐式密度。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `G(z)` produzir um modelo, um juiz `D(x)`区分真假──GAN 推理快(单次前向传播), mas o treinamento é muito pouco estável──StyleGAN 1/2/3 mesmo em 2026 ainda é o modelo mais avançado de real-sense em nível de domínio fixo──

**4. Score-based / continuous-time.**Aprenda a gradiente da densidade de tronco.`∇_x log p(x)`Song & Ermon (2019) mostrou que a correspondência de pontuação generaliza a difusão para um SDE. A correspondência de fluxo (Lipman 2023) é a temperatura de 2024-2026: treinamento sem simulação, caminhos mais retos, amostragem 4-10 vezes mais rápida do que o DDPM.

> **4. 基于分数/连续时间。**直接学习对数密度的梯度(分数函数) ――Song & Ermon (2019) 证明分数匹配将扩散推广到SDE──Flow Matching(2023) é um curso de treinamento de fluxo de 2024-2026, mais direto do que o DDPM 快 4-10 倍──Stable Diffusion 3、Flux、AudioCraft 2 都使用Flow Matching──

> **【中文解读】**O parâmetro de combinação e fluxo é uma generalização e melhoria do modelo de expansão. O parâmetro de combinação simplifica ainda mais o processo de treinamento. Não é necessário simular o SDE, aprendendo diretamente a partir do ruído para o dados.

**5. Token-based autoregressive over discrete codes.**Comprime dados de alta dim com um VQ-VAE ou quantificador residual em uma curta sequência de tokens discretos, em seguida, use um transformador para modelar a sequência de tokens. Parti, MuseNet, AudioLM, VALL-E, o tokenizer de patch de Sora todos usam isso. Este é um balde 1 mais um tokenizer aprendido.

> **5. 基于离散 token 的自回归。**Usando VQ-VAE ou residuo quantificador irá comprimir alta dimensão de dados para a sequência curta de tokens de separação, e depois usar o transformador 建模 token 序列──Parti、MuseNet、AudioLM、VALL-E、Sora para o tokenizer de parcheiros são usados dessa forma── este é, em sua natureza, o primeiro tipo de tokenizer a ser aprendido──

## Uma breve história.

| Year / 年份 | Model / 模型 | Why it mattered / 重要意义 |
|------|-------|-----------------|
| 2013 | VAE (Kingma) | First deep generative model with a usable training loss. / 首个具有可用训练损失的深度生成模型。 |
| 2014 | GAN (Goodfellow) | Implicit density, no likelihood — shockingly sharp samples. / 隐式密度，无需似然——惊人的锐利样本。 |
| 2015 | DRAW, PixelCNN | Sequential image generation. / 顺序图像生成。 |
| 2017 | Glow, RealNVP | Invertible flows; exact likelihood with depth. / 可逆流；深度带来精确似然。 |
| 2017 | Progressive GAN | First megapixel faces. / 首个百万像素人脸。 |
| 2019 | StyleGAN / StyleGAN2 | Photorealistic faces still hard to beat for that one domain. / 照片级真实人脸，该领域至今难以超越。 |
| 2020 | DDPM (Ho) | Diffusion becomes practical. / 扩散模型变得实用。 |
| 2021 | CLIP, DALL-E 1, VQGAN | Text-to-image goes mainstream. / 文本生成图像走向主流。 |
| 2022 | Imagen, Stable Diffusion 1, DALL-E 2 | Latent diffusion + text conditioning = commodity. / 潜在扩散 + 文本条件 = 大众化。 |
| 2022 | ControlNet, LoRA | Fine control over pretrained diffusion. / 对预训练扩散模型的精细控制。 |
| 2023 | SDXL, Midjourney v5, Flow matching | Scale + better training dynamics. / 规模化 + 更好的训练动态。 |
| 2024 | Sora, Stable Diffusion 3, Flux.1 | Video diffusion; flow matching wins. / 视频扩散；Flow Matching 胜出。 |
| 2025 | Veo 2, Kling 1.5, Runway Gen-3, Nano Banana | Production-grade video. / 生产级视频。 |
| 2026 | Consistency + Rectified Flow | One-step sampling from diffusion backbones. / 从扩散骨干实现单步采样。 |

## A triagem de cinco perguntas.

Quando um novo modelo gerativo cair, responda a estas cinco perguntas antes de ler a seção de métodos.

> Quando um novo artigo sobre o modelo de geração for publicado, antes de ler a parte do método, responda a estas cinco questões.

1. **What is being modeled?**Pixels, latentes, tokens discretos, Gaussians 3D, malhas, formas de onda?
   **正在建模什么？**Como é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é?
2. **Is the density explicit or implicit?**Eles escrevem .`log p(x)`- Não .
   **密度是显式还是隐式的？**Eles escreveram?`log p(x)`- Não .
3. **Sampling: one-shot or iterative?**Iterativo significa inferência mais lenta; um tiro geralmente significa adversário ou destilado.
   **采样：单次还是迭代？**代 significa pensar mais devagar;单次 normalmente significa oposição ou disti──
4. **Conditioning: unconditional, class, text, image, pose?**Isto determina a perda e o andaime de arquitetura.
   **条件：无条件、类别、文本、图像、姿态？**Isso determina a estrutura de funções e de estrutura de perda.
5. **Evaluation: FID, CLIP score, IS, human preference, task accuracy?**Cada um tem modos de falha conhecidos (ver Lição 14).
   **评估：FID、CLIP Score、IS、人类偏好、任务准确率？**Cada um tem um padrão de insuficiência conhecido (cf. § 14).

Responde-lhes-á estas cinco lições para cada aula nesta fase.

> Você vai responder novamente a estas cinco perguntas em cada sessão desta fase. Até que, finalmente, elas se tornam sua instinção.

> **【中文解读】**Estas cinco questões ([[Construção de Objetos de Modelação]], [[Desensação de Objetos de Modelação]], [[Desensação de Objetos de Modelação]], [[Desensação de Objetos de Modelação]], [[Desensação de Objetos de Modelação]], [[Desensação de Objetos de Modelação]], [[Desensação de Objetos de Modelação]], [[Desensação de Objetos de Modelação]], [[Desensação de Objetos de Modelação]], [[Desensação de Objetos de Modelação]], [[Desensação de Objetos de Modelação]], [[Desensação de Objetos de Modelação]], [[Desensação de Objetos de Modelação]], [[Desensação de Objetos de Modelação]], [[Desensação de Modelação]], [[Desensação de Condições]], [[Desensação de Avaliação]]) são os principais elementos de análise de qualquer modelo gerado.

## Construí-lo e realizei-o.
```figure
autoencoder-bottleneck
```

## Construí-lo

O código para esta lição é uma visualização leve: ajuste uma mistura de Gauss de 1D de amostras usando três abordagens de brinquedo (densidade do núcleo, histograma discreto e gerador de "GAN-ish" da amostra mais próxima) para que você possa ver a diferença entre densidade explícita vs implícita em um problema que você pode imprimir em uma tela.

> O código desta aula é uma visualização de nível leve: usar três métodos simples: (estimativa de densidade nuclear, separada quadrada, gerador de "GAN estilo" próximo) para se adequar a uma distribuição misturada de dimensões em um modelo, permitindo que você veja a distinção entre densidade clara e densidade oculta dentro de uma tela.

Corra .`code/main.py`Extrai 2000 amostras de uma mistura gaussiana de dois modos, e depois imprime:

> 运行 `code/main.py`❖ Extraiu 2000 amostras de dois picos de mistura e imprimiu:

```
explicit density (histogram): p(x in [-0.5, 0.5]) ≈ 0.38
approximate density (KDE):     p(x in [-0.5, 0.5]) ≈ 0.41
implicit (nearest-sample gen): 20 new samples printed, no p(x)
```

Observe: as duas primeiras deixam você perguntar "quão provável é este ponto?" A terceira não pode. Esta é a distinção *explicita vs implícita* que será importante para cada lição futura.

> Nota: Os dois primeiros métodos podem responder "Qual é a probabilidade de que esse ponto tenha uma grande probabilidade?" O terceiro não pode.

## Use-o com o framework implementado.

Que família, para que tarefa, em 2026?

> 2026 ano, qual família se adapta a qual missão?

| Task / 任务 | Best family / 最佳家族 | Why / 原因 |
|------|-------------|-----|
| Photoreal faces, narrow domain / 照片级人脸，窄域 | StyleGAN 2/3 | Still sharpest, fastest inference. / 仍然最锐利，推理最快。 |
| General text-to-image / 通用文本生成图像 | Latent diffusion + flow matching | SD3, Flux.1, DALL-E 3. |
| Fast text-to-image / 快速文本生成图像 | Rectified flow + distillation | SDXL-Turbo, SD3-Turbo, LCM. |
| Text-to-video / 文本生成视频 | Diffusion Transformer + flow matching | Sora, Veo 2, Kling. |
| Speech + music / 语音+音乐 | Token-based AR (AudioLM, VALL-E, MusicGen) or flow matching (AudioCraft 2) | Discrete tokens scale cheaply. / 离散 token 扩展成本低。 |
| 3D scenes / 3D 场景 | Gaussian Splatting fit, diffusion prior | 3D-GS for reconstruction, diffusion for novel-view. / 3D-GS 用于重建，扩散用于新视角。 |
| Density estimation (no sampling) / 密度估计（不采样） | Flows | Only family with exact `log p(x)`. / 唯一有精确 `log p(x)` 的家族。 |
| Simulation / physics / 模拟/物理 | Flow matching, score SDE | Straight-line paths, smooth vector fields. / 直线路径，平滑向量场。 |

## Envia-o . Produto .

Salva como`outputs/skill-model-chooser.md`- Não .

> 保存为 `outputs/skill-model-chooser.md`- Não.

A habilidade requer uma descrição da tarefa e resultados: (1) qual família usar, (2) uma lista classificada de três opções abertas e três hospedadas, (3) o modo de falha provável que você deve procurar, e (4) um orçamento computacional/temporal.

> A competência                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

## Exercícios.

1. **Easy / 简单.**Para cada um destes cinco produtos, identifique a família e a espinha dorsal: imagem ChatGPT, Midjourney v7, Sora, Runway Gen-3, ElevenLabs.
   对于这五个产品,识别其家族和骨干:ChatGPT image、Midjourney v7、Sora、Runway Gen-3、ElevenLabs──证据应来自公开技术报告──
2. **Medium / 中等.**O artigo que você está prestes a ler amanhã afirma que a amostragem é 100 vezes mais rápida do que a difusão.
   Você vai ler amanhã o artigo que afirma que a expansão é mais rápida do que 100 vezes mais rápido.
3. **Hard / 困难.**Tome um domínio que lhe interessa (por exemplo, estrutura de proteínas, CAD, moléculas, trajetórias). Responda à triagem de cinco perguntas para o modelo SOTA atual nesse domínio e esboce o que um modelo melhor mudaria.
   选择一个你关心的领域 (如蛋白质结构,CAD,分子,轨迹) ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅     ⋅                                                                                                                               

## Termos-chave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Generative model | "It makes new stuff" / "它生成新东西" | Learns a sampler for `p_data(x)`, optionally exposes `log p(x)`. / 学习 `p_data(x)` 的采样器，可选暴露 `log p(x)`。 |
| Explicit density | "You can evaluate it" / "可以计算" | Model provides a closed-form or tractable `log p(x)`. / 模型提供闭式或可处理的 `log p(x)`。 |
| Implicit density | "GAN-style" / "GAN 风格" | Only a sampler — no way to evaluate `p(x)` of a given point. / 只有采样器——无法计算给定点的 `p(x)`。 |
| ELBO | "Evidence lower bound" / "证据下界" | A tractable lower bound on `log p(x)`; VAEs and diffusion optimize it. / `log p(x)` 的可处理下界；VAE 和扩散模型优化它。 |
| Score | "Gradient of log-density" / "对数密度梯度" | `∇_x log p(x)`; diffusion and SDE models learn this field. / 扩散和 SDE 模型学习这个场。 |
| Manifold hypothesis | "Data lives on a surface" / "数据在曲面上" | High-dim data concentrates on a low-dim manifold; why dimensionality reduction works. / 高维数据集中在低维流形上；降维有效的原因。 |
| Autoregressive | "Predict the next piece" / "预测下一个" | Factorize joint as product of conditionals. / 将联合分布分解为条件分布的乘积。 |
| Latent | "Compressed code" / "压缩编码" | Low-dim representation from which a decoder can reconstruct the input. / 解码器可从中重建输入的低维表示。 |

## Nota de produção: cinco famílias, cinco formas de inferência

Cada família mapeia uma curva de custo inferência-servidor diferente. literatura de produção-inferação enquadra inferência LLM como prefill + decode; a mesma decomposição aplica-se aqui:

> Cada família deve responder a diferentes tipos de cálculo de custo de servidor.

- **Autoregressive (bucket 1 and 5).**O decodificação sequencial domina a latência; o cache KV, o batch contínuo e a decodificação especulativa aplicam-se diretamente.
  **自回归（第 1 和 5 类）。**顺序解码主导延迟;KV 缓存、连续批处理和推测解码直接适用──
- **VAE / diffusion / flow-matching (buckets 2 and 4).**Não há decodificação no sentido de LLM.`num_steps × step_cost`, e o `step_cost`O botão de produção é de contagem de etapas (DDIM / DPM-Solver / destilação), tamanho de lote e precisão (bf16 / fp8 / int4).
  **VAE / 扩散 / Flow Matching（第 2 和 4 类）。**LLM 意义上没有解码──成本 = `num_steps × step_cost`, produção de regulação de rotação é o número de etapas, grandeza e precisão do lote.
- **GAN (bucket 3).**Não há cronograma, não há cache KV, TTFT ≈ latência total, é por isso que o StyleGAN ainda vence no UX de domínio estreito.
  **GAN（第 3 类）。**单次前向传播──没有调度,没有 KV 缓存──TTFT ≈ 总延迟──这就是StayGAN在狭域UX上仍然胜出的原因──

Quando você vê "mais rápido que a difusão" em um resumo de papel, traduza-o para "menos passos × o mesmo custo de passos" ou "os mesmos passos × mais barato custo de passos".

> Quando o resumo do artigo diz "quando é mais rápido do que o que é mais rápido", traduzido para "menos custos de passo × custos de passo" ou "o mesmo custo de passo × custos de passo mais baratos" (→ "o restante é o custo de vendas").

## Mais leitura 延伸阅读

- [Goodfellow et al. (2014). Generative Adversarial Nets](https://arxiv.org/abs/1406.2661)O papel GAN.
- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) o papel do VAE.
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) o documento do DDPM.
- [Song et al. (2021). Score-Based Generative Modeling through SDEs](https://arxiv.org/abs/2011.13456) difusão como SDE.
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) papel de correspondência de fluxo.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) Difusão estável 3.
