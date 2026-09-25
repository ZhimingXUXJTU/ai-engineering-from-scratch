# GANs  Generador vs Discriminador  GAN  Produtor e Jurispriminador

> O truque de Goodfellow em 2014 foi ignorar a densidade inteiramente. Duas redes. Uma faz falsas. Uma as apanha. Eles lutam até que as falsas sejam indistinguíveis do real. Não deveria funcionar. Muitas vezes não funciona. Quando acontece, as amostras ainda são as mais nítidas na literatura para domínios estreitos.

> **【中文解读】**A técnica de Goodfellow 2014 foi totalmente saltar a estimativa de densidade. Duas redes: uma falsificação, uma crença, se compartilham entre si até que a falsa amostra e a verdadeira amostra não sejam distinguidas.

> **【拓展：GAN 的遗产】**StyleGAN(人脸生成)、CycleGAN(风格迁移)、Pix2Pix(图像翻译) é uma aplicação clássica do GAN。 Embora o modelo de expansão se torne dominante em 2022 depois, a ideia de treinamento de resistência do GAN ainda é usada para melhorar a qualidade de outros modelos。

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 3 · 08 (Optimizers / 优化器), Phase 8 · 02 (VAE)
**Time:** ~75 minutes

## O problema é o problema da introdução

Os VAEs produzem amostras borrosas porque a perda do decodificador MSE é Bayes-óptima para a imagem * média *  e a média de muitos dígitos plausíveis é um dígito confuso. Você quer uma perda que recompensa * plausibilidade*, não proximidade de pixel para um alvo. Não há forma fechada para plausibilidade. Você tem que aprender.

> O VAE  produz uma amostra confusa, porque a perda do MSE 解码器 (descodificador) em relação ao valor médio da imagem é a melhor de Bayes  e a média de muitos números razoáveis é um número confuso. Você precisa de uma perda de recompensa* realidade* em vez de uma proximidade com qualquer objetivo.

A ideia do Goodfellow: treinar um classificador.`D(x)`Para distinguir imagens reais de falsas.`G(z)`Para enganar .`D`O sinal de perda para o`G`É o que quer que seja.`D`O sinal atualiza-se como:`G`Se as duas redes convergem,`G`Aprendeu a distribuição de dados sem escrever.`log p(x)`- Não .

> O bom amigo é um tipo de máquina .`D(x)`区分真假图像, treinar um gerador `G(z)`Para enganar .`D`- Não.`G`O sinal de perda é:`D`Quando pensamos que "parece real" algo... este sinal acompanha-nos.`G`O melhoramento e a atualização são para alcançar um objetivo móvel.`G`Aprendi a distribuir os dados, sem precisar escrever.`log p(x)`- Não.

Isto é treinamento adversário.

```
min_G max_D  E_real[log D(x)] + E_fake[log(1 - D(G(z)))]
```

Em 2026 os GANs não são mais o gerador de SOTA (difusão e fluxo de correspondência cometeu essa coroa). Mas o StyleGAN 2/3 continua sendo os modelos de rosto mais nítidos já enviados, os discriminadores GAN são usados como *perdas perceptivas* no treinamento de difusão, e o treinamento adversário alimenta as destilações rápidas em 1 passo (SDXL-Turbo, SD3-Turbo, LCM) que permitem enviar difusão em tempo real.

> 2026 ano GAN  不再是最先进的生成器 (GAN 扩散模型和流量匹配) 夺走了冠) ──但 StyleGAN 2/3 仍然是历史上最利的人脸模型,GAN 判斷器被用于扩散训练中*感觉损失*,对抗训练驱动快速的1步蒸(SDXL-Turbo、SD3-Turbo、LCM) ──

> **【中文解读】**GAN 尝试生成逼真图像,判别器 D(x) 尝试区分真假──两者在最小x 博中共同进化──VAE  MSE 损失导致模糊──因为它最优化是平均值图像),而GAN 抗损失奖励"逼真度"──GAN 生成速度快 ,但训练不稳──

> **【拓展：GAN 在扩散模型蒸馏中的新角色】**Embora o GAN não seja mais um método de produção dominante, o anti-trainamento ideológico desenvolve-se em um modelo de dispersão. O modelo de rápido uso de anti-perdidas será mais rápido em 1 a 4 etapas, para a realização da produção em tempo real.

## O conceito central.

![GAN training: generator and discriminator in minimax](../assets/gan.svg)

**Generator `G(z)`.**Mapas de um vetor de ruído `z ~ N(0, I)`para uma amostra `x̂`- Uma rede em forma de decodificador (conventes densos ou transpostos).

> **生成器 `G(z)`。**- Não .`z ~ N(0, I)`映射为样本 `x̂`△ Uma rede de forma de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede

**Discriminator `D(x)`.**Mapas de uma amostra para uma probabilidade escalar (ou pontuação).

> **判别器 `D(x)`。**将样本映射为标量概率 (或分数) ⋅真实 → 1,伪造 → 0⋅

**Loss.**Duas atualizações alternativas:

- **Train `D`:** `loss_D = -[ log D(x) + log(1 - D(G(z))) ]`Entropia binária cruzada em real=1, falso=0.
- **Train `G`:** `loss_G = -log D(G(z))`Esta é a forma * não saturante * usada por Goodfellow (original `log(1 - D(G(z)))`satura e mata os gradientes quando `D`- Não é um problema.

> **损失。**两个交替更新:训练 D 用二元交叉(真实=1,伪造=0);训练 G 用非和形式 `-log D(G(z))`(original forma em D 自信时梯度 desaparecer)

**Training loop.**Um passo de `D`, um passo de `G`Repito.

> **训练循环。**Um passo D, um passo G, um passo G, um passo G.

**Why it works.**Se`G`- Sim . - Sim .`p_data`, então`D`Não pode fazer melhor do que o acaso e as saídas 0,5 em todos os lugares; `G`Não há mais gradiente.

> **为什么有效。**Se `G`完美匹配 `p_data`, , ,`D`Não posso imaginar melhor, em qualquer saída.`G`Não tenho mais gradiente.

**Why it breaks.**Colapso de modo (`G`encontra um modo `D`Não podemos classificar e minar para sempre), desvanecendo gradiente (`D`Aprende muito rápido e `log D`A Comissão propõe que os programas de formação sejam desenvolvidos em todos os Estados-Membros.

> **为什么会失败。**模式塌(`G`找到 `D`Não podemos classificar um tipo de padrão que nunca se produzir.`D`Aprendi muito depressa.`log D`和) 、 training is unstable (和)                                                                                                                                                                                                                                                        

## Variantes que fizeram o GAN funcionar.

| Year / 年份 | Innovation / 创新 | Fix / 解决的问题 |
|------|------------|-----|
| 2015 | DCGAN | Conv/deconv, batch norm, LeakyReLU — the first stable architecture. / 首个稳定架构。 |
| 2017 | WGAN, WGAN-GP | Replace BCE with Wasserstein distance + gradient penalty. Fixes vanishing gradient. / 用 Wasserstein 距离替换 BCE，修复梯度消失。 |
| 2017 | Spectral normalization | Lipschitz-bound the discriminator. Still used in 2026 discriminators. / 约束判别器 Lipschitz 常数。 |
| 2018 | Progressive GAN | Train low-res first, add layers. First megapixel results. / 先训练低分辨率，再加层。 |
| 2019 | StyleGAN / StyleGAN2 | Mapping network + adaptive instance norm. State of the art for fixed-domain photorealism. / 映射网络 + AdaIN。 |
| 2021 | StyleGAN3 | Alias-free, translation-equivariant — still the face gold standard in 2026. / 无混叠，平移等变。 |
| 2022 | StyleGAN-XL | Conditional, class-aware, larger scale. / 条件生成，类别感知。 |
| 2024 | R3GAN | Rebrands with stronger regularization; works on 1024² without tricks. / 更强的正则化。 |

## Construí-lo e realizei-o.
```figure
gan-minimax
```

## Construí-lo

`code/main.py`O gerador e o discriminador são MLPs de camada única oculta. Implementamos o loop avançado, retroativo e mínimox à mão. O objetivo é ver os dois modos de falha chave (collapso de modo + gradiente de desaparecimento) à medida que acontecem.

> `code/main.py`Em uma dimensão de dados, treinar um GAN de pequeno tipo: GAN:双峰高斯混合── generator e判辨器 são um único nível de MLP── 我们手动实现前向、反向和最小x循环──目标是看到两种关键失败模式 (模式塌 + 梯度消失) 的发生过程──

### Passo 1: perda não saturante

A perda do Vanilla Goodfellow .`log(1 - D(G(z)))`O gradiente para G é basicamente zero  G não pode melhorar. A forma não saturante `-log D(G(z))`tem a asintóte oposta: explode quando D está confiante, dando a G um sinal forte.

> Bom companheiro                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `log(1 - D(G(z)))`Em D alta confiança, a classificação de G em falso se aproxima de 0, neste momento a gradiência de G é essencialmente zero.`-log D(G(z))`Há um comportamento gradual contrário: em D auto-confiança quando se desencadeia, dá um forte sinal G.

```python
def g_loss(d_fake):
    # maximize log D(G(z))  <=>  minimize -log D(G(z))
    return -sum(math.log(max(p, 1e-8)) for p in d_fake) / len(d_fake)
```

### Passo 2: um passo discriminador por passo gerador

```python
for step in range(steps):
    # train D
    real_batch = sample_real(batch_size)
    fake_batch = [G(z) for z in sample_noise(batch_size)]
    update_D(real_batch, fake_batch)

    # train G
    fake_batch = [G(z) for z in sample_noise(batch_size)]  # fresh fakes
    update_G(fake_batch)
```

Falsas frescas para o G, caso contrário, os gradientes são velhos.

> Para criar novas falsiões, ou então estávamos passando o tempo.

### Passo 3: vigilância para o colapso do modo

```python
if step % 200 == 0:
    samples = [G(z) for z in sample_noise(500)]
    mode_a = sum(1 for s in samples if s < 0)
    mode_b = 500 - mode_a
    if min(mode_a, mode_b) < 50:
        print("  [!] mode collapse: one mode is starved")
```

O sintoma canônico: um dos dois modos reais deixa de ser gerado. O discriminador deixa de corrigi-lo porque nunca é visto como falso.

> 典型症状: dos dois modelos reais não mais é gerado.

## Encaixos.

- **Discriminator too strong.**Reduzir a taxa de aprendizagem de D em 2-5x, ou adicionar ruído de instância/camada.
  **判别器太强。**A taxa de aprendizagem de D é reduzida 2-5 vezes, ou adicionada por exemplo/ruído de camada.
- **Generator memorizes a mode.**Adicionar ruído às entradas D, usar uma camada de minibatch-discriminator, ou mudar para WGAN-GP.
  **生成器记住了一种模式。**给 D 输入添加噪音, use小批量判辨器层,或切换到WGAN-GP──
- **Batch norm leaking statistics.**Batch real + batch falso fluindo através da mesma camada BN mistura suas estatísticas.
  **批归一化泄漏统计量。**Batas reais e falsas foram aprovadas pela mesma BN 层混合统计量――改用例归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归
- **Inception-score gaming.**FID e IS são barulhentos em baixas quantidades de amostras.
  **Inception Score 作弊。**FID 和 IS em baixa quantidade de amostras em volume de ruído.
- **One-shot sampling is a lie for conditional tasks.**Ainda precisas de escalas CFG, truques de truncamento e re-muitas para obter resultados utilizáveis.
  **条件任务中"单次采样"是个谎言。**Você ainda precisa de técnicas de CFG 缩缩,截断和重采样才能获得可用输出.

## Use-o com o framework implementado.

A pilha de GAN 2026:

> 2026 技术:

| Situation / 场景 | Pick / 选择 |
|-----------|------|
| Photoreal human faces, fixed pose / 照片级人脸，固定姿势 | StyleGAN3 (sharpest, smallest) |
| Anime / stylized faces / 动漫/风格化人脸 | StyleGAN-XL or Stable Diffusion LoRA |
| Image-to-image translation / 图像翻译 | Pix2Pix / CycleGAN (Phase 8 · 04) or ControlNet (Phase 8 · 08) |
| Fast 1-step text-to-image / 快速单步文生图 | Adversarial distillation of diffusion (SDXL-Turbo, SD3-Turbo) |
| Perceptual loss inside a diffusion trainer / 扩散训练中的感知损失 | Small GAN discriminator on image crops |
| Anything multi-modal, open-ended / 多模态开放域 | Don't — use diffusion or flow matching / 不要用 GAN——用扩散或 Flow Matching |

O GAN é agudo, mas estreito. Uma vez que o seu domínio abre fotos, instruções de texto arbitrárias, vídeo, comuta para difusão.

> GAN 利但狭域──一旦领域开放照片、任意文本提示、视频就就换到扩散模型──对抗技巧作为组件存活(感知损失、蒸),而不是独立生成器──

## Envia-o . Produto .

Salvar`outputs/skill-gan-debugger.md`. A Skill toma uma execução GAN falha (curvas de perda, rede de amostragem, tamanho do conjunto de dados) e produz uma lista classificada de causas prováveis, correções de uma linha e um protocolo de reiniciação.

> 保存 `outputs/skill-gan-debugger.md`◊ Habilidade de receber um GAN falhado 运行(损失曲线、样本网格、数据集大小),输出可能原因排序列、一行修复和重跑方案──

## Exercícios.

1. **Easy / 简单.**Corra .`code/main.py`com as configurações de ações.`D_LR = 5 * G_LR`A perda do G desmorona-se rapidamente para uma constante.
   Usado por definição`code/main.py`。 Então, configuração `D_LR = 5 * G_LR`Perdas de peso em G são constantes?
2. **Medium / 中等.**Substituir a perda do Goodfellow BCE pela perda do WGAN: `loss_D = E[D(fake)] - E[D(real)]`- Não .`loss_G = -E[D(fake)]`, e clip D pesos para `[-0.01, 0.01]`Comparar a convergência entre o relógio de parede.
   Para trocar perdas do Goodfellow BCE por perdas do WGAN , cortar o peso do D`[-0.01, 0.01]`O que é que é mais forte?
3. **Hard / 困难.**Extenda o exemplo 1-D para dados 2-D (mistura de 8 Gaussians em um anel).
   Para ampliar o exemplo 1D para dados 2D ((\ rings 个高斯混合) ⋅ tracking generator capturou em 1k、5k、10k 步骤多少模式;; realizar pequeno batch

## Termos-chave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Generator | "G" | Noise-to-sample network, `G: z → x̂`. / 噪声到样本的网络。 |
| Discriminator | "D" | Classifier `D: x → [0, 1]`, real vs fake. / 真假分类器。 |
| Minimax | "The game" / "博弈" | `min_G max_D` of a joint objective. / 联合目标的极小极大。 |
| Non-saturating loss | "The fix" / "修复" | Use `-log D(G(z))` for G instead of `log(1 - D(G(z)))`. / 用非饱和形式替代原始损失。 |
| Mode collapse | "G memorized one thing" / "G 记住了一种" | Generator produces few distinct outputs despite diverse data. / 生成器产生少量不同输出。 |
| WGAN | "Wasserstein" | Replace BCE with Earth-Mover distance + gradient penalty; smoother gradient. / 用 Wasserstein 距离替代 BCE。 |
| Spectral norm | "Lipschitz trick" / "Lipschitz 技巧" | Constrain D's weight norms to bound its slope; stabilizes training. / 约束 D 的权重范数以稳定训练。 |
| StyleGAN | "The one that works" / "能用的那个" | Mapping network + AdaIN; best-in-class for faces, still in 2026. / 映射网络 + AdaIN，人脸最佳。 |

## Nota de produção: inferência de um tiro é a vantagem duradoura de GAN

Os GANs não ganham mais a qualidade da amostra para a geração de domínio aberto, mas ainda ganham o custo de inferência.

> O GAN não vence mais a qualidade das amostras geradas em áreas abertas, mas ainda vence no custo de cálculo.

- **No prefill, no decode stages.**Um único .`G(z)`Passagem para a frente. TTFT ≈ latência total.
  **无 prefill，无 decode 阶段。**单次 `G(z)`Antes de chegar ao mundo, o mundo não está mais a ser visto.
- **No KV-cache pressure.**O tamanho do lote é limitado pela memória de ativação, não pelo cache.
  **无 KV 缓存压力。**O único estado é o peso. O volume é limitado a armazenamento ativado e não a armazenamento.
- **Trivial continuous batching.**Uma vez que cada solicitação recebe os mesmos FLOPs fixos, um lote estático na ocupação alvo do servidor é geralmente ideal.
  **简单的连续批处理。**Cada pedido consome o mesmo FLOP, o volume estático geralmente é o melhor.

É por isso que a destilação GAN (SDXL-Turbo, SD3-Turbo, ADD, LCM) é a técnica dominante para a rápida transmissão de texto para imagem em 2026: desintegra um tubo de difusão de 20 a 50 passos em passes avançadas de 1 a 4 GAN ao mesmo tempo que mantém a distribuição de uma base de difusão.

> É por isso que o GAN 蒸(SDXL-Turbo、SD3-Turbo、LCM) é a principal tecnologia de 2026: ele irá expandir o fluxo de água em 2050 passos para 1-4 vezes a direção da GAN 风格, mantendo a distribuição do modelo de expansão.

## Mais leitura 延伸阅读

- [Goodfellow et al. (2014). Generative Adversarial Nets](https://arxiv.org/abs/1406.2661) o papel original do GAN.
- [Radford et al. (2015). Unsupervised Representation Learning with DCGAN](https://arxiv.org/abs/1511.06434)A primeira arquitetura estável.
- [Arjovsky, Chintala, Bottou (2017). Wasserstein GAN](https://arxiv.org/abs/1701.07875) WGAN.
- [Miyato et al. (2018). Spectral Normalization for GANs](https://arxiv.org/abs/1802.05957) SN.
- [Karras et al. (2020). Analyzing and Improving the Image Quality of StyleGAN](https://arxiv.org/abs/1912.04958)- StyleGAN2.
- [Karras et al. (2021). Alias-Free Generative Adversarial Networks](https://arxiv.org/abs/2106.12423)- StyleGAN3.
- [Sauer et al. (2023). Adversarial Diffusion Distillation](https://arxiv.org/abs/2311.17042)- SDXL-Turbo.
