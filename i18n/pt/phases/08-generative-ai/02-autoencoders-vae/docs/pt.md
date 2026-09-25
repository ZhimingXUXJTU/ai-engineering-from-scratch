# Autoencoders & Variation Autoencoders (VAE) ✓ Autoencoders e variáveis

> Um autoencoder simples comprime e reconstrui. Ele memorizou. Não gera. Adicione um truque  forçar o código para parecer Gaussian  e você obtém um amostragem. Esse truque único, a reparameterization de `z = mu + sigma * epsilon`, é por isso que cada modelo de imagem de difusão latente e de correspondência de fluxo que você usa em 2026 tem um VAE na entrada.

> **【中文解读】**Normalmente, o auto-codificador se compacta, reconstrui, apenas lembranças, não pode gerar.`z = mu + sigma * epsilon`Deixar a escala atravessar a operação de aprendizagem é o chave do treinamento de VAE.

> **【拓展：VAE 是 Stable Diffusion 的基石】**Em 2026 todos os modelos de expansão potencial ((Stable Diffusion、FLUX) estão em funcionamento no espaço potencial do VAE.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 3 · 07 (CNNs / 卷积神经网络), Phase 8 · 01 (Taxonomy / 分类)
**Time:** ~75 minutes

## O problema é o problema da introdução

Compre uma cifra MNIST de 784 pixels para um código de 16 números, e depois reconstruir. Um autoencoder simples irá reconstruir MSE mas o espaço de código é um desastre. Escolha um ponto aleatório no espaço de código, decodifique-o e você obtém ruído. Não tem amostragem. É um modelo de compressão vestido bem.

> Para reduzir o número de imagens de 784 para 16 números, o MNIST pode ser reedificado. O sistema pode ser bem reedificado, mas o espaço de codificação é ruim.

O que você realmente quer é: (a) o espaço de código é uma distribuição limpa e suave que você pode amostrar a partir de  digamos um Gaussian isotrópico `N(0, I)`A descrição de um modelo é uma análise de dados que permite a análise de dados e de dados.

> O que você realmente quer é: a) O espaço de código é limpo, plano, distribuído de forma aceitável, como em todos os lugares.`N(0, I)`• b) O sistema de codificação de qualquer tipo produz números razoáveis; c) O sistema de codificação e codificação ainda estão bem comprimidos.

O VAE 2013 da Kingma resolve isso treinando o codificador para emitir uma *distribuição* `q(z|x) = N(μ(x), σ(x)²)`, puxando essa distribuição para o prior`N(0, I)`através de uma penalidade KL, e depois de amostragem `z`de`q(z|x)`Antes de decodificar. Na hora de inferir, solte o codificador, amostra `z ~ N(0, I)`A penalidade KL é o que obriga o espaço de código a ser estruturado.

> Kingma 2013 ano VAE 通过训练编码器输出*分布* `q(z|x) = N(μ(x), σ(x)²)`Para resolver este problema, através da KL, a punição será distribuída para os primeiros.`N(0, I)`, e depois de`q(z|x)`- Não .`z`Recorrendo a um processo de redação, deixo de usar o programa.`N(0, I)`采样 `z`,解码──KL 惩罚正是使编码空间结构化的关键──

Em 2026 os VAEs raramente enviam independentemente  eles foram superados pela difusão pela qualidade de imagem crua  mas são o codificador de escolha para todos os modelos de difusão latente (SD 1/2/XL/3, Flux, AudioCraft).

> Em 2026 anos, a VAE  Very few Independent Deployment  já foi expandido modelo em qualidade de imagem original ultrapassando mas é o primeiro editor de todas as possíveis expansões modelo (SD 1/2/XL/3、Flux、AudioCraft) .

> **【中文解读】**O VAE tem um conceito central: fazer com que o codificador saia de distribuição e não de pontuação.`z = mu + sigma * epsilon`Use o código de distribuição de forma mais próxima do padrão normal. ELBO  perda = perda de construção mais beta * KL 散度, ambas se pesam entre si.

> **【拓展：beta-VAE 与解耦表示学习】**beta-VAE(2017) através de regulação beta parâmetros control reconstrução com KL de peso;; beta<1 时重建更清晰但潜在空间不规整; beta>1 时潜在空间更规整但图像更模糊;; quando beta 足够大时,VAE pode aprender a "descombinar" a expressão de cada dimensão codificar isolados de significados factores (((como cores, formas, tamanho) ⋅).

## O conceito central.

![Autoencoder vs VAE: the reparameterization trick](../assets/vae.svg)

**Autoencoder.** `z = encoder(x)`- Não .`x̂ = decoder(z)`, perda = `||x - x̂||²`- Espaço de código não estruturado.

> **自编码器。** `z = encoder(x)`- Não .`x̂ = decoder(z)`, perda = `||x - x̂||²`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖

**VAE encoder.**As saídas de dois vetores: `μ(x)`E ...`log σ²(x)`Estes definem`q(z|x) = N(μ, diag(σ²))`- Não .

> **VAE 编码器。**输出两个向量:`μ(x)`和 `log σ²(x)` Eles definiram `q(z|x) = N(μ, diag(σ²))`- Não.

**Reparameterization trick.**Amostragem de `q(z|x)`Não é diferenciável. Reescrever a amostra como `z = μ + σ·ε`onde`ε ~ N(0, I)`Agora .`z`é uma função determinista de `(μ, σ)`+ um ruído não-parâmetro  gradientes fluem através `μ`E ...`σ`- Não .

> **重参数化技巧。**De`q(z|x)`采样不可微──将采样重写为 `z = μ + σ·ε`, entre os `ε ~ N(0, I)`Agora.`z`Sim `(μ, σ)`A função de determinação, adicionada ao ruído não-parametral, pode ser aprovada.`μ`和 `σ`Contrário à propagação.

**Loss.**Evidência Bando inferior (ELBO), dois termos:

```
loss = reconstruction + β · KL[q(z|x) || N(0, I)]
     = ||x - x̂||²  + β · Σ_i ( σ_i² + μ_i² - log σ_i² - 1 ) / 2
```

A reconstrução impulsiona .`x̂`- Para o lado .`x`- KL empurra .`q(z|x)`A primeira é a de uma forma mais simples, mas não é a de uma forma mais simples.

> Pulsão de perda de construção`x̂`趋近 `x` KL 推动 `q(z|x)`趋近先验──两者相互权衡──β 小(<1) = 更利的样本,编码空间不太高斯──β 大(>1) = 更干净的编码空间,更模糊的样本──β-VAE(2017) fez esse giro conhecido,并开启了解表示学习研究──

**Sampling.**Em inferência: desenho `z ~ N(0, I)`Uma passagem avançada, sem amostragem iterativa como a difusão.

> **采样。**推理时: de `N(0, I)`抽取                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `z`, entregue em disseminação e divulgação.

> **【中文解读】**As duas componentes da perda de ELBO são: reconstrução da perda para garantir a qualidade do código, KL 散度 para garantir a regularidade do espaço potencial.

> **【拓展：Stable Diffusion 中的 VAE】**Estabilidade de difusão Usar o VAE de pré-treino vai 512x512  imagem comprimido para 64x64 de potencial espaço(8 vezes abaixo da definição)  O processo de difusão ocorre no espaço potencial, reduzindo significativamente a quantidade de cálculo  SD 3 Usar o VAE mais avançado  Apoio 16 de potencial espaço, imagem de qualidade mais alta  O volume de compressão do VAE afeta diretamente a segurança das informações da geração final da imagem 

## Construí-lo e realizei-o.
```figure
vae-latent-grid
```

## Construí-lo

`code/main.py`Implementa um pequeno VAE sem numpy ou tocha. A entrada é dados sintéticos 8-dimensionais extraídos de uma mistura gaussiana de 2 componentes em 8-D. Encoder e decodificador são MLPs de camada oculta única. Implementamos ativação tanh, passagem para frente, perda e passagem para trás escrita à mão. Não produção  pedagogia.

> `code/main.py` Realizar um VAE de pequeno tipo sem dependência de numpy ou tocha  Introdução é extraído de 8 维 2 分量高斯混合中抽取的 8 维合成数据──编码器和编码器是单隐层 MLP── 实现 tanh 激活、前向传播、损失和手写反向传播── não é produção de código纯教学──

### Passo 1: encode para a frente

```python
def encode(x, enc):
    h = tanh(add(matmul(enc["W1"], x), enc["b1"]))
    mu = add(matmul(enc["W_mu"], h), enc["b_mu"])
    log_sigma2 = add(matmul(enc["W_sig"], h), enc["b_sig"])
    return mu, log_sigma2
```

`log σ²`Em vez de`σ`Assim, a saída da rede é livre (softplus de σ é uma armadilha  gradientes morrem em σ ≈ 0).

> Utilização `log σ²`Não é`σ`O softplus de σ é um tipo de armadilha em σ ≈ 0 时梯度会消失)

### Passo 2: reparametrizar e decodificar

```python
def reparameterize(mu, log_sigma2, rng):
    eps = [rng.gauss(0, 1) for _ in mu]
    sigma = [math.exp(0.5 * lv) for lv in log_sigma2]
    return [m + s * e for m, s, e in zip(mu, sigma, eps)]

def decode(z, dec):
    h = tanh(add(matmul(dec["W1"], z), dec["b1"]))
    return add(matmul(dec["W_out"], h), dec["b_out"])
```

### Passo 3: ELBO

```python
def elbo(x, x_hat, mu, log_sigma2, beta=1.0):
    recon = sum((a - b) ** 2 for a, b in zip(x, x_hat))
    kl = 0.5 * sum(math.exp(lv) + m * m - lv - 1 for m, lv in zip(mu, log_sigma2))
    return recon + beta * kl, recon, kl
```

Exato KL fechado porque ambas as distribuições são gaussianas. Não se integram numericamente. As pessoas ainda enviam código com as estimativas de monte-carlo KL em 2026  é 3x mais lento sem razão.

> 精确的闭式 KL,因为两个分布都是高斯的──不要数值积分──2026年还有人发布蒙特卡洛 KL 估计代码无端慢了3倍──

### Passo 4: gerar

```python
def sample(dec, z_dim, rng):
    z = [rng.gauss(0, 1) for _ in range(z_dim)]
    return decode(z, dec)
```

É o modelo generativo.

> É o que se passa com a produção de modelos.

## Encaixos.

- **Posterior collapse.**- Dispositivos de termo KL`q(z|x) → N(0, I)`tão agressivamente que`z`Não tem informações sobre `x`. Correcção: anulação β (iniciar β=0, rampa a 1), bits livres ou saltar o KL em dimensões inativas.
  **后验坍塌。**KL 项如此强强地将 `q(z|x)`- Não .`N(0, I)`, que conduz`z`Não tenho nada a ver com isso.`x` 0 ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ 
- **Blurry samples.**A probabilidade do decodificador gaussiano implica a reconstrução do MSE, que é Bayes-ótima para L2 (a média)  a média de um conjunto de dígitos plausíveis é um dígito confuso.
  **模糊样本。**高斯解码器似然意味着MSE 重建一组合理数字的平均值是一个模糊的数字──修复:离散解码器(VQ-VAE、NVAE), ou simplesmente usar VAE como um codificador, superimposado em um modelo de expansão em um espaço potencial──
- **β too large, too early.**Veja o colapso posterior.
  **β 太大太早。**见后验塌──从 β≈0.01 开始并逐渐增加──
- **Latent dim too small.**16-D funciona para MNIST, 256-D para ImageNet 2562, 2048-D para ImageNet 10242. O VAE da Diffusão Estavel comprime 512×512×3 → 64×64×4 (32x fator de amostra descendente em área espacial, 32x em canais).
  **潜在维度太小。**MNIST usando 16 维,ImageNet 2562 usando 256 维── VAE de Diffusão Estavel vai 512×512×3  Compressão para 64×64×4──

## Use-o com o framework implementado.

A pilha de 2026 VAE:

> 2026 技术:

| Situation / 场景 | Pick / 选择 |
|-----------|------|
| Image-latent encoder for diffusion / 图像潜在编码器 | Stable Diffusion VAE (`sd-vae-ft-ema`) or Flux VAE |
| Audio-latent encoder / 音频潜在编码器 | Encodec (Meta), SoundStream, or DAC (Descript) |
| Video latents / 视频潜在表示 | Sora's spatiotemporal patches, Latte VAE, WAN VAE |
| Disentangled representation learning / 解耦表示学习 | β-VAE, FactorVAE, TCVAE |
| Discrete latents (for transformer modelling) / 离散潜在表示 | VQ-VAE, RVQ (ResidualVQ) |
| Continuous latents for generation / 连续潜在生成 | Plain VAE, then condition a flow/diffusion model in that latent space |

Um modelo de difusão latente é um VAE com um modelo de difusão que vive entre o codificador e o decodificador. O VAE faz compressão grosseira, o modelo de difusão faz o levantamento pesado. O mesmo padrão para vídeo (VAE + video-difusão DiT) e áudio (Encodec + MusicGen transformador).

> O modelo de expansão potencial é entre o codificador e o codificador, que se juntou ao modelo de expansão VAE──VAE fazer grosso compressão, modelo de expansão fazer revivê──vídeo(VAE + vídeo DiT) e audio频(Encodec + MusicGen transformador)

## Envia-o . Produto .

Salvar`outputs/skill-vae-trainer.md`- Não .

> 保存 `outputs/skill-vae-trainer.md`- Não.

As competências são: perfil do conjunto de dados + meta de diminuição latente + uso a jusante (reconstrução, amostragem ou entrada de difusão latente) e resultados: escolha de arquitetura (planos/β/VQ/RVQ), programação β, diminuição latente, probabilidade de decodificação (Gaussian vs categorical) e plano de avaliação (recon MSE, KL por dim, distância Fréchet entre `q(z|x)`E ...`N(0, I)`)).

> Competências  recepção: dados集概况 + 潜在维度目标 + 下游用途(重建、采样或潜在扩散输入),输出:架构选择(plain/β/VQ/RVQ) 、β 调度、潜在维度、解码器似然(高斯 vs 类别) 和评估计划──

## Exercícios.

1. **Easy / 简单.**Mudança .`β`em `code/main.py`- Não .`0.01`- Não .`0.1`- Não .`1.0`- Não .`5.0`Gravar a reconstrução final do MSE e KL. Qual β é o melhor para os seus dados sintéticos?
   Em`code/main.py`- Não .`β`改为 `0.01`- Não.`0.1`- Não.`1.0`- Não.`5.0` Record final reconstrução MSE e KL. • Qual β para o seu conjunto de dados é o melhor para o seu conjunto?
2. **Medium / 中等.**Substitua a probabilidade de descodificação gaussiana por uma probabilidade de Bernoulli (perda de entropia cruzada). Compare a qualidade da amostra em uma versão binária dos mesmos dados sintéticos.
   O valor de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de um sistema de cálculo de cálculo de um sistema de cálculo de cálculo de um sistema de cálculo de cálculo de um sistema de cálculo de cálculo de um sistema de cálculo de cálculo de um sistema de cálculo de cálculo de um sistema de cálculo de cálculo de um sistema de cálculo de cálculo de cálculo de um sistema de cálculo de cálculo de cálculo de um sistema de cálculo de cálculo de cálculo de um sistema de cálculo de cálculo de cálculo de cálculo de um sistema de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de um sistema de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de cálculo de de de de de cálculo de cálculo de de de de de cálculo de de de de cálculo de cálculo de de de cálculo de cálculo de de de de de cálculo de cálculo de de de de cálculo de cálculo de de de de cálculo de de de de de cálculo de cálculo de de de de cálculo de cálculo de de de de de cálculo de de de de de de cálculo de de de um de cálculo de de de de de de cálculo de cálculo de de de de de cálculo de de de de de de de de um de cálculo de de de um de um de um
3. **Hard / 困难.**Extensão`code/main.py`em um mini VQ-VAE: substituir o contínuo `z`Comparar a reconstrução MSE e relatar quantas entradas de código são utilizadas (o colapso do código é real).
   - Não .`code/main.py`扩展为迷你 VQ-VAE: Usar K=32 的码本近邻查找替换连续 `z`❖ Comparar a reconstrução da MSE e relatar o número de utilizadas neste artigo.

## Termos-chave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Autoencoder | Encode-decode network / 编码-解码网络 | `x → z → x̂`, learn MSE. Not generative. / `x → z → x̂`，学习 MSE。不是生成模型。 |
| VAE | AE with a sampler / 带采样器的 AE | Encoder outputs a distribution, KL penalty shapes code space. / 编码器输出分布，KL 惩罚塑造编码空间。 |
| ELBO | Evidence lower bound / 证据下界 | `log p(x) ≥ recon - KL[q(z\|x) \|\| p(z)]`; tight when `q = p(z\|x)`. |
| Reparameterization | `z = μ + σ·ε` | Rewrites stochastic node as deterministic + pure noise. Enables backprop through sampling. / 将随机节点重写为确定性 + 纯噪声。使采样可反向传播。 |
| Prior | `p(z)` | Target distribution for the latent, typically `N(0, I)`. / 潜在变量的目标分布，通常是 `N(0, I)`。 |
| Posterior collapse | "KL term wins" / "KL 项赢了" | Encoder ignores `x`, outputs the prior; decoder must hallucinate. / 编码器忽略 `x`，输出先验；解码器只能幻觉。 |
| β-VAE | Tunable KL weight / 可调 KL 权重 | `loss = recon + β·KL`. Higher β = more disentangled but blurrier. / β 越高越解耦但越模糊。 |
| VQ-VAE | Discrete latent / 离散潜在变量 | Replace continuous `z` with nearest codebook vector; enables transformer modelling. / 用最近码本向量替换连续 `z`。 |

## Nota de produção: o VAE é o caminho mais quente em um servidor de difusão .

Em um fluxo / fluxo / SD3 de fluxo estável, o VAE é chamado duas vezes por pedido  uma vez para codificar (se fazendo img2img / inpainting) e uma vez para decodificar.`128×128×16`Latentes de volta para `1024×1024×3`Duas consequências práticas:

> Em Stable Diffusion / Flux / SD3 流水线中,VAE Cada vez que o pedido é chamado duas vezes uma vez codificação(img2img/inpainting) uma vez resolver.

- **Slice or tile the decode.** `diffusers`expõe`pipe.vae.enable_slicing()`E ...`pipe.vae.enable_tiling()`O Tiling negocia um pequeno artefato de costura para`O(tile²)`Memória em vez de `O(H·W)`É essencial para 10242+ em GPUs de consumo.
  **切片或分块解码。** `diffusers` fornecer `enable_slicing()`和 `enable_tiling()`分块以轻微接伪影换取 `O(tile²)`- Não.
- **bf16 decoder, fp32 numerics for the final resize.**O SD 1.x VAE foi lançado em fp32 e *produz silenciosamente NaNs* quando lançado para fp16 em 10242+. navios SDXL `madebyollin/sdxl-vae-fp16-fix` sempre prefira a variante fp16-fix ou use bf16.
  **bf16 解码器，fp32 用于最终 resize。**SD 1.x VAE 在 fp16 下 10242+ 会静默产生 NaN──始终使用 fp16-fix 变体或 bf16──

## Mais leitura 延伸阅读

- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) o papel do VAE.
- [Higgins et al. (2017). β-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework](https://openreview.net/forum?id=Sy2fzU9gl) dissociado β- VAE.
- [van den Oord et al. (2017). Neural Discrete Representation Learning](https://arxiv.org/abs/1711.00937) VQ-VAE.
- [Vahdat & Kautz (2021). NVAE: A Deep Hierarchical Variational Autoencoder](https://arxiv.org/abs/2007.03898) imagem de última geração VAE.
- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) Difusão estável; VAE como codificador.
- [Défossez et al. (2022). High Fidelity Neural Audio Compression](https://arxiv.org/abs/2210.13438) Encodec, o padrão de áudio VAE.
