# GAN condicional e Pix2Pix .

> A primeira grande desbloqueio de 2014-2017 foi controlar o que um GAN faz. Anexe um rótulo, ou uma imagem, ou uma frase. Pix2Pix fez a versão de imagem e ainda vence todos os modelos genéricos de texto para imagem em tarefas estreitas de imagem para imagem.

> **【中文解读】**O primeiro grande avanço de 2014-2017 foi o controle do GAN. O GAN produziu: tags adicionais, imagens ou textos. O Pix2Pix produziu uma versão de imagens, que ainda venceu o modelo de imagem gerado em texto geral em tarefas de tradução de imagens de domínio restrito.

> **【拓展：Pix2Pix 的应用】**Pix2Pix 开创了"图像到图像翻译"范式:素描→照片、白天→夜晚、线稿→彩色图── essa范式 foi posteriormente adquirida e desenvolvida pelo ControlNet──

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 03 (GANs), Phase 4 · 06 (U-Net), Phase 3 · 07 (CNNs / 卷积神经网络)
**Time:** ~75 minutes

## O problema é o problema da introdução

Uma GAN incondicional mostra rostos arbitrários. Útil para uma demonstração, inútil na produção. Você quer: *mapear um esboço para uma foto*, *mapear um mapa para uma foto aérea*, *mapear uma cena diurna para a noite*, *colorizar uma imagem em escala de cinza*. Em todos eles, você recebe uma imagem de entrada`x`e deve ser emitido`y`Há muitas hipóteses plausíveis.`y`S por`x`O erro médio quadrado aplania-os em massa, mas a perda adversária não, porque "parece real" é acentuada.

> 无条件 GAN 采样任意人脸──适合演示,不适合生产──你想要的是:*将素描映射为照片*、*将地图映射为航拍图*、*将白天映射为夜*、*给灰度图上色*──在所有这些场景中,给定输入图像 `x`, deve produzir relações de resposta significativas.`y`Todos.`x`Há muitas razões .`y`                                                                                                                                                                                                                                                              

GAN condicional (Mirza & Osindero, 2014) adiciona uma condição `c`como uma entrada para ambos `G`E ...`D`. Pix2Pix (Isola et al., 2017) especializou-se nisso: condição é uma imagem de entrada completa, gerador é uma U-Net, discriminador é um classificador baseado em patch (PatchGAN), e perda é adversária + L1. Essa receita supera modelos de texto a imagem de zero em domínios de imagem a imagem estreitos mesmo em 2026 porque é treinado em * dados em pares *  você tem exatamente o sinal que precisa.

> 条件 GAN(2014) `G`和 `D`Of entrada em condições adicionais`c` Pix2Pix(2017) especializou-se neste: condição é entrada completa de imagem, gerador é U-Net, divisor é PatchGAN, perda = oposição + L1♦ Este programa ainda é melhor do que o modelo de imagem de teste em 2026 em tarefas de tradução de imagem de domínio restrito, pois está em * par com dados * em treinamento de sinais que você precisa ter.

> **【中文解读】**Condições Mudanças centrais do GAN: para gerador e gerador de dados adicionadas Condições de entrada c⋅Pix2Pix as condições são completa entrada de imagem, gerador U-Net ([[Reservation Space Details]]), gerador de dados com PatchGAN ([[Local Image Block]]) ⋅ Perda = para resistência a perda + L1 ⋅ Perda.

> **【拓展：从 Pix2Pix 到 ControlNet 的演进】**A ideia de "generação de imagens condicionais" da Pix2Pix foi gerada pela ControlNet (em 2023) e desenvolvida.

## O conceito central.

![Pix2Pix: U-Net generator, PatchGAN discriminator](../assets/pix2pix.svg)

**Conditional G.** `G(x, z) → y`- Na Pix2Pix,`z`é descontinuado dentro de G (sem ruído de entrada  Isola encontrou ruído explícito foi ignorado).

> **条件生成器 G。** `G(x, z) → y` Em Pix2Pix,`z`Não há ruído de entrada.

**Conditional D.** `D(x, y) → [0, 1]`. A entrada é o *par* (condição, saída). Esta é a diferença chave: D deve julgar se `y`é consistente com `x`Não só se`y`Parece real.

> **条件判别器 D。** `D(x, y) → [0, 1]`◊输入是*配对*(条件,输出) ー关键区别:D 必须判断 `y`Sim ou não`x`Uma致, não apenas `y`Não parece real.

**U-Net generator.**Encoder-decodificador com conexões de saltar através do gargalo de engarrafamento. É crítico para tarefas onde entrada e saída compartilham estrutura de baixo nível (borda, silueta). Sem os saltos, detalhes de alta frequência desaparecem.

> **U-Net 生成器。**带有跳跃连接的编码器-解码器――对于输入输出共享低级结构的任务至关重要――没有跳跃连接,高频细节会消失――

**PatchGAN discriminator.**Em vez de emitir uma única pontuação real/falsa, D emitirá uma`N×N`Grade onde cada célula julga um campo receptivo de ~70×70 pixels. média. Esta é uma suposição de campo aleatório de Markov: realismo é local. muito mais rápido para treinar, menos parâmetros, saída mais nítida.

> **PatchGAN 判别器。**D 输出 `N×N`网格而不是单一真/假分数, cada unidade julga cerca de 70×70 像素的感受野──这是马尔可夫随机场假设:真实感是局部的──训练更快,参数更少,输出更利──

**Loss.**

```
loss_G = -log D(x, G(x)) + λ · ||y - G(x)||_1
loss_D = -log D(x, y) - log (1 - D(x, G(x)))
```

O termo L1 estabiliza o treinamento e empurra G para o alvo conhecido.`λ = 100`Era o Pix2Pix padrão.

> L1 项稳定训练并推动 G 趋向已知目标──L1 比 L2 产生更利的边缘(中位数 vs 平均值)──`λ = 100`É o valor de configuração do Pix2Pix.

## CycleGAN  quando não tens pares  CycleGAN   não há par de dados 

Pix2Pix precisa de paragem `(x, y)`Os dados. CycleGAN (Zhu et al., 2017) reduz esta exigência ao custo de uma perda extra: a perda de *consistência do ciclo*.`G: X → Y`E ...`F: Y → X`Treinar-lhes assim .`F(G(x)) ≈ x`E ...`G(F(y)) ≈ y`Isto permite que se traduza cavalos em zebras, verão em inverno, sem exemplos emparelhados.

> Pix2Pix 需要配对 `(x, y)`Data: CycleGAN (em 2017) abandonou esta exigência, o preço é extra ciclo de concordança perdida.`G: X → Y`和 `F: Y → X`, treinamento `F(G(x)) ≈ x`和 `G(F(y)) ≈ y`O que te deixa sem par de amostra para poder transformar o cavalo em zebra, o verão em inverno.

Em 2026, a imagem-para-imagem não-parejada é feita principalmente através da difusão (ControlNet, IP-Adapter) em vez do CycleGAN, mas a ideia de consistência de ciclo sobrevive em quase todos os documentos de adaptação de domínio não-parejado.

> Em 2026, não se completa a ideia de concordança de ciclo em cada um dos artigos de adaptação de domínio não-combustible.

## Construí-lo e realizei-o.
```figure
gx-patchgan
```

## Construí-lo

`code/main.py`Implementa uma pequena GAN condicional em dados 1-D.`c`é um rótulo de classe (0 ou 1). A tarefa: produzir uma amostra da distribuição condicional para a classe dada.

> `code/main.py`Em um nível de dados, é possível realizar uma condição GAN.`c`É uma categoria de tags ((0 ou 1);; tarefa: para uma determinada categoria de padrões gerados em uma distribuição de condições;;

### Passo 1: apenda condição tanto às entradas G como D

```python
def G(z, c, params):
    return mlp(concat([z, one_hot(c)]), params)

def D(x, c, params):
    return mlp(concat([x, one_hot(c)]), params)
```

A codificação de um só-quente é a maneira mais simples. Os modelos maiores usam incorporados aprendidos, modulação FiLM ou atenção cruzada.

> One-hot 编码是最简单的方式――更大的模型使用学习嵌入、FiLM 调制或交叉注意力──

### Passo 2: com condição de trem

```python
for step in range(steps):
    x, c = sample_real_conditional()
    noise = sample_noise()
    update_D(x_real=x, x_fake=G(noise, c), c=c)
    update_G(noise, c)
```

O gerador deve corresponder à distribuição real * para a dada condição *, não à marginalidade.

> O gerador deve corresponder à distribuição real sob determinadas condições, e não à distribuição marginal.

### Passo 3: Verificação de saída por classe

```python
for c in [0, 1]:
    samples = [G(noise, c) for noise in batch]
    mean_c = mean(samples)
    assert_near(mean_c, real_mean_for_class_c)
```

## Encaixos.

- **Condition ignored.**G aprende a marginalizar, D nunca penaliza porque o sinal de condição é fraco.
  **条件被忽略。**G aprenderam a marginalizar, D 从不惩罚因为条件信号弱――修复:更积极地条件化 D, usando projeção判别器――
- **L1 weight too low.**G deriva para saídas arbitrárias de aparência real, não fiéis. Comece λ≈100 para tarefas de estilo Pix2Pix.
  **L1 权重太低。**G 偏移到任意看起来真实输出──Pix2Pix 任务从 λ≈100 开始──
- **L1 weight too high.**O G produz resultados borrosos porque o L1 continua a ser uma norma de L_p.
  **L1 权重太高。**G  产生模糊输出── treino estabilizado depois gradualmente diminuir──
- **Ground-truth leakage in D.**Concatenato `(x, y)`como entrada D, não apenas `y`Sem este D não podemos verificar a consistência.
  **D 中的真值泄漏。**- Não .`(x, y)`拼接为 D 的输入,而非仅仅 `y`- Não.
- **Mode collapse per class.**Cada classe pode colapsar de forma independente.
  **每类模式坍塌。**Cada categoria pode ser separada.

## Use-o com o framework implementado.

2026 estado das tarefas de imagem em imagem:

> 2026 ano imagem para imagem missão estado:

| Task / 任务 | Best approach / 最佳方案 |
|------|---------------|
| Sketch → photo, same domain, paired data / 素描→照片，配对数据 | Pix2Pix / Pix2PixHD (still fast, still sharp) |
| Sketch → photo, unpaired / 素描→照片，非配对 | ControlNet with a Scribble conditioning model |
| Semantic seg → photo / 语义分割→照片 | SPADE / GauGAN2 or SD + ControlNet-Seg |
| Style transfer / 风格迁移 | Diffusion with IP-Adapter or LoRA; GAN methods are legacy |
| Depth → photo / 深度→照片 | ControlNet-Depth over Stable Diffusion |
| Super-resolution / 超分辨率 | Real-ESRGAN (GAN), ESRGAN-Plus, or SD-Upscale (diffusion) |
| Colorization / 上色 | ColTran, diffusion-based colorizers, or Pix2Pix-color |
| Daytime → nighttime, seasons, weather / 白天→夜晚 | CycleGAN or ControlNet-based |

Pix2Pix continua a ser a ferramenta certa quando (a) você tem milhares de exemplos emparelhados, (b) a tarefa é estreita e repetível e (c) você precisa de inferência rápida. Em tarefas genéricas de domínio aberto, a difusão ganha.

> Pix2Pix está em situação de: a) Há milhares de modelos de partilha, b) As tarefas são estreitas e repetíveis, c) Precisam de uma rápida avaliação.

## Envia-o . Produto .

Salvar`outputs/skill-img2img-chooser.md`. A competência assume uma descrição da tarefa, a disponibilidade de dados (pareados vs. não-pareados, amostras N) e o orçamento de latência/qualidade, e em seguida, as saídas: abordagem (Pix2Pix, CycleGAN, variante ControlNet, SDXL + IP-Adapter), requisitos de dados de treinamento, custo de inferência e protocolo de avaliação (LPIPS, FID, específico de tarefa).

> 保存 `outputs/skill-img2img-chooser.md` Descrição de tarefas de recepção de habilidades, disponibilidade e orçamento de atraso/qualidade de dados, programa de saída, necessidade de formação de dados, acordo de avaliação e avaliação de custos.

## Exercícios.

1. **Easy / 简单.**Modificar`code/main.py`Confirme que o G ainda mapeia o ruído de cada classe para o modo correto.
   修改 `code/main.py`Adicionar 3o Categoria: Confirmar que cada tipo de ruído será mapeado para o padrão correto
2. **Medium / 中等.**Substituir o L1 por uma perda de estilo perceptivo na configuração 1-D (por exemplo, um pequeno D congelado que atua como extractor de características).
   Em 1D, substituir a perda sensorial por L1... mudou a condição de distribuição?
3. **Hard / 困难.**Esboçar um CycleGAN na configuração 1-D: duas distribuições, dois geradores, perda de ciclo. Mostrar que ele aprende a mapear entre eles sem dados emparelhados.
   Em 1D  desenho em configuração CycleGAN: duas distribuições ▌dois geradores ▌ciclo de perda ▌prova que não é necessário comparar dados para aprender a mapear ▌

## Termos-chave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Conditional GAN | "GAN with labels" / "带标签的 GAN" | G(z, c), D(x, c). Both networks see the condition. / 两个网络都看到条件。 |
| Pix2Pix | "Image-to-image GAN" / "图像到图像 GAN" | Paired cGAN with U-Net G and PatchGAN D + L1 loss. / 配对 cGAN + U-Net + PatchGAN + L1。 |
| U-Net | "Encoder-decoder with skips" / "带跳跃的编解码器" | Symmetric conv network; skips preserve high-freq. / 对称卷积网络；跳跃连接保留高频。 |
| PatchGAN | "Local-realism classifier" / "局部真实分类器" | D outputs per-patch score instead of global score. / D 输出逐块分数。 |
| CycleGAN | "Unpaired image translation" / "非配对图像翻译" | Two G's + cycle-consistency loss; no paired data. / 两个 G + 循环一致性损失。 |
| SPADE | "GauGAN" | Normalizes intermediate activations with the semantic map; segmentation-to-image. / 用语义图归一化中间激活。 |
| FiLM | "Feature-wise linear modulation" / "特征级线性调制" | Per-feature affine transform from the condition; cheap conditioning. / 廉价的条件化方式。 |

## Nota de produção: Pix2Pix como uma linha de base limitada à latência

Quando você combina dados e uma tarefa estreita (esquisa → renderização, mapa semântica → foto, dia → noite), a inferência de uma só vez da Pix2Pix supera a difusão em uma ordem de magnitude na latência.

> Quando você tem um parâmetro de dados e tarefas de domínio estreito, a única hipótese do Pix2Pix é que o modelo de expansão é rápido em uma escala quantitativa.

| Path / 方案 | Steps / 步数 | Typical latency at 512² on a single L4 / 典型延迟 |
|------|-------|----------------------------------------|
| Pix2Pix (U-Net forward) | 1 | ~30 ms |
| SD-Inpaint or SD-Img2Img | 20 | ~1.2 s |
| SDXL-Turbo Img2Img | 1-4 | ~0.15-0.35 s |
| ControlNet + SDXL base | 20-30 | ~3-5 s |

Pix2Pix ganha em throughput em lotes estáticos (cada solicitação é a mesma FLOPs). Diffusão ganha na qualidade e generalização. O jogo moderno é muitas vezes enviar um modelo destilado estilo Pix2Pix para a tarefa estreita e uma falha de difusão para entradas de cauda.

> Pix2Pix em estado estático de volume de produção em volume de produção (FLOPs) = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

## Mais leitura 延伸阅读

- [Mirza & Osindero (2014). Conditional Generative Adversarial Nets](https://arxiv.org/abs/1411.1784)- o papel do CGAN.
- [Isola et al. (2017). Image-to-Image Translation with Conditional Adversarial Networks](https://arxiv.org/abs/1611.07004)- Pix2Pix.
- [Zhu et al. (2017). Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks](https://arxiv.org/abs/1703.10593) CycleGAN.
- [Wang et al. (2018). High-Resolution Image Synthesis with Conditional GANs](https://arxiv.org/abs/1711.11585)- Pix2PixHD.
- [Park et al. (2019). Semantic Image Synthesis with Spatially-Adaptive Normalization](https://arxiv.org/abs/1903.07291)- SPADE / Gaugan.
- [Miyato & Koyama (2018). cGANs with Projection Discriminator](https://arxiv.org/abs/1802.05637) a projecção D.
