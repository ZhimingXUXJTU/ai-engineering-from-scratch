# Modelos de difusão  DDPM a partir do zero  Modelo de expansão  Realização de DDPM a partir de zero

> Ho, Jain, Abbeel (2020) deu ao campo uma receita que não podia parar. Destruir os dados com ruído em mil pequenos passos. Treinar uma rede neural para prever o ruído. Reverte o processo à inferência. Hoje todo modelo de imagem, vídeo, 3D e música da corrente dominante funciona neste loop, possivelmente com a combinação de fluxo ou truques de consistência no topo.

> **【中文解读】**O processo central do DDPM: usando 1000 passos para dar dados adicionais ao ruído, danificar dados, treinar um ruído prévio de rede neural, sugerir o tempo de remoção de ruído.

> **【拓展：扩散模型是当前 AI 生成的核心】**Estabilidade de difusão DALL-E 3 Midjourney Sora são baseados em modelos de difusão.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 8 · 02 (VAE)
**Time:** ~75 minutes

## O problema é o problema da introdução

Queres uma amostra para ?`p_data(x)`O que realmente se quer é um objetivo de treinamento que seja (a) uma única perda estável (sem ponto de sela, sem minimax), (b) um limite inferior em `log p(x)`(de modo que tenha probabilidades), e (c) amostras que correspondam à qualidade do SOTA.

> Tu queres`p_data(x)`O que você realmente quer é: (a) 单一稳定的损失, (b) `log p(x)`É um dos principais pontos de interesse da indústria.

Sohl-Dickstein et al. (2015) teve uma resposta teórica: definir uma cadeia de Markov `q(x_t | x_{t-1})`que gradualmente adiciona ruído gaussiano, e treinar uma cadeia inversa`p_θ(x_{t-1} | x_t)`Ho, Jain, Abbeel (2020) mostrou que a perda pode ser simplificada para uma linha  prever o ruído  e limpar a matemática. Em 2020 isso foi uma curiosidade. Em 2021 produziu amostras de última geração. Em 2022 tornou-se Diffusão estável. Em 2026 é o substrato.

> Sohl-Dickstein (2015)  deu a resposta teórica: definir a cadeia de marcófuge de aumento gradual do ruído, treinamento contra a cadeia de ruído. Ho  et al. (2020) vai simplificar o perdimento para uma linha de ruído de previsão.

> **【中文解读】**O DDPM é um processo de três etapas: 1) processo de avanço para aumentar o ruído gradualmente até que os dados se transformem em ruído puro; 2) processo de treinamento para aprender um preâmbulo de rede a cada passo de adição de ruído; 3) processo de reverso para começar a fazer ruído gradualmente, para recuperar dados reais.

> **【拓展：从 DDPM 到实用扩散模型】**DDPM 原始论文在像素空间操作,速度慢(需要1000步去噪音) ・・・三关键改进使它成为实用工具:(1) DDIM(2020) 采样步数将从1000 降到20-50;(2) 潜在扩散(2021,Rombach) 潜空间中操作,大幅降低计算量;(3) CFG(Classifier-Free Guidance,2022) 通过条件/无条件预测的差提升生成质量──

## O conceito central.

![DDPM: forward noise, reverse denoise](../assets/ddpm.svg)

**Forward process `q`.**Adicionar ruído Gaussiano .`T`A forma fechada  a razão pela qual a matemática é tratável  é que o passo acumulativo é também gaussiano:

> **前向过程 `q`。**Em`T`O que é que se pode fazer com que o número de números seja elevado?

```
q(x_t | x_0) = N( sqrt(α̅_t) · x_0,  (1 - α̅_t) · I )
```

onde`α̅_t = ∏_{s=1..t} (1 - β_s)`para um calendário de `β_t`- Escolha .`β_t`de 1e-4 a 0,02 linearmente sobre T=1000 passos e `x_T`é aproximadamente `N(0, I)`- Não .

> Entre eles `α̅_t = ∏_{s=1..t} (1 - β_s)`将 `β_t`De 1e-4 a 0,02 线性排列 T=1000 步,`x_T`Quase assim.`N(0, I)`- Não.

**Reverse process `p_θ`.**Aprenda uma rede neural .`ε_θ(x_t, t)`que prevê o ruído que foi adicionado.`x_t`, denotado por:

> **反向过程 `p_θ`。**Aprender a usar uma rede de neurônios`ε_θ(x_t, t)`Prevé-se o aumento do ruído.`x_t`,去噪音方式为:

```
x_{t-1} = (1 / sqrt(α_t)) · ( x_t - (β_t / sqrt(1 - α̅_t)) · ε_θ(x_t, t) )  +  σ_t · z
```

onde`σ_t`É um dos dois .`sqrt(β_t)`A expressão é feia, mas é apenas álgebra.`x_{t-1}`dada a posterior `q(x_{t-1} | x_t, x_0)`e substituindo`x_0`com a sua estimativa prévia de ruído.

> Entre eles `σ_t`Sim `sqrt(β_t)`Ou aprender a fazer diferença. A expressão parece complicada, mas é apenas um número.`q(x_{t-1} | x_t, x_0)`- Não .`x_{t-1}`- Não.

**Training loss.**

```
L_simple = E_{x_0, t, ε} [ || ε - ε_θ( sqrt(α̅_t) · x_0 + sqrt(1 - α̅_t) · ε,  t ) ||² ]
```

Amostra `x_0`De dados, escolha um aleatório`t`, amostra `ε ~ N(0, I)`, calcular o barulho .`x_t`Uma perda, sem minimos, sem KL, sem truques de reparametrização.

> De dados`x_0`, como escolher`t`, assim`ε ~ N(0, I)`, através de um cálculo de um volume de ruído`x_t`, para o ruído fazer regresso.

**Sampling.**Começa .`x_T ~ N(0, I)`Repita o passo inverso de`t = T`- Não .`1`- Já está.

> **采样。**De`x_T ~ N(0, I)`開始,从 `t = T`Até`1`代反向步骤──完成──

## Porque é que funciona ?

Três intuições:

> Três sentidos:

1. **Denoising is easy; generating is hard.**- Não .`t=T`A rede tem de resolver um problema trivial.`t=0`A rede só tem de limpar alguns pixels.`t`O problema é difícil, mas a rede tem muitos gradientes fluindo através dos mesmos pesos de todos os níveis de ruído.
   **去噪容易，生成难。**Em`t=T`Quando, os dados são ruídos puros, a rede só precisa resolver um simples problema.`t=0`时, a rede só precisa de limpar uma pequena quantidade de imagens.

2. **Score matching in disguise.**Vincent (2011) provou que prever o ruído é equivalente a estimar `∇_x log q(x_t | x_0)`O SDE inverso usa esta pontuação para subir o gradiente de densidade  um caminho aleatório guiado em direção a regiões de alta probabilidade.
   **伪装的分数匹配。**预测 ruído é igual ao valor da função de cálculo`∇_x log q(x_t | x_0)`❖ O SDE de contra-direcção utiliza este percentual de aumento da densidade.

3. **The ELBO reduces to simple MSE.**O limite inferior variável completo tem um termo KL por etapa de tempo. Com a parâmetrizagem do DDPM, esses termos KL simplificam para MSE na previsão de ruído com coeficientes específicos; Ho caiu os coeficientes (chamando-o de perda "simples") e a qualidade *melhorou*.
   **ELBO 简化为简单 MSE。**完整的变分下界 每次步都有 KL 项── Ho 丢弃系数后质量反而升级了──

## Construí-lo e realizei-o.
```figure
diffusion-denoise
```

## Construí-lo

`code/main.py`O "net" é um pequeno MLP que leva`(x_t, t)`O treinamento é a perda de uma linha.

> `code/main.py`实现一维 DDPM──数据是双峰混合──"网络" é um micro tipo de MLP, recepção `(x_t, t)`输出预测噪音──训练就是那一行损失──采样代反向链──

### Passo 1: calendário de execução (formulario fechado)

```python
betas = [1e-4 + (0.02 - 1e-4) * t / (T - 1) for t in range(T)]
alphas = [1 - b for b in betas]
alpha_bars = []
cum = 1.0
for a in alphas:
    cum *= a
    alpha_bars.append(cum)
```

### Passo 2: amostra `x_t`em uma só vez

```python
def forward_sample(x0, t, alpha_bars, rng):
    a_bar = alpha_bars[t]
    eps = rng.gauss(0, 1)
    x_t = math.sqrt(a_bar) * x0 + math.sqrt(1 - a_bar) * eps
    return x_t, eps
```

### Passo 3: um passo de formação

```python
def train_step(x0, model, alpha_bars, rng):
    t = rng.randrange(T)
    x_t, eps = forward_sample(x0, t, alpha_bars, rng)
    eps_hat = model_forward(model, x_t, t)
    loss = (eps - eps_hat) ** 2
    return loss, gradient_step(model, ...)
```

### Passo 4: amostragem inversa

```python
def sample(model, alpha_bars, T, rng):
    x = rng.gauss(0, 1)
    for t in range(T - 1, -1, -1):
        eps_hat = model_forward(model, x, t)
        beta_t = 1 - alphas[t]
        x = (x - beta_t / math.sqrt(1 - alpha_bars[t]) * eps_hat) / math.sqrt(alphas[t])
        if t > 0:
            x += math.sqrt(beta_t) * rng.gauss(0, 1)
    return x
```

Para um problema 1-D com 40 passos de tempo e um MLP de 24 unidades, este aprende a mistura de dois modos em ~ 200 épocas.

> Para 40 个时间步和 24 单元 MLP 的一维问题, cerca de 200 轮即可学会双峰混合──

## Condicionamento de tempo .

A rede precisa saber qual é o passo a seguir.

> A rede precisa saber em que tempo está a fazer ruído.

- **Sinusoidal embedding.**Como codificação posicional do Transformer.`embed(t) = [sin(t/ω_0), cos(t/ω_0), sin(t/ω_1), ...]`Passa por um MLP, transmite-se à rede.
  **正弦嵌入。**类似Transformer 位置编码──
- **Film / group-norm conditioning.**Projecto de inserção em escala/bias por canal (FiLM) em cada bloco.
  **FiLM / 组归一化条件化。**Embaixar projeção para cada canal de encolhimento/defiliação.

Nosso código de brinquedo usa sinusoidal → concat.

> Nós somos os que criamos o nosso jogo.

## Encaixos.

- **Schedule matters a lot.**Linear `β`O programa de cálculo é o DDPM padrão, mas o cronograma cosínico (Nichol & Dhariwal, 2021) dá uma melhor FID para a mesma computação.
  **调度很重要。**线性 `β`É DDPM 默认但余弦调度在相同计算量下 FID 更好──
- **Timestep embedding is fragile.**Passando cru`t`como um float funciona para brinquedo 1-D mas falha para imagens; sempre use um incorporado adequado.
  **时间步嵌入脆弱。**Originário`t`O número de pontos em brinquedo 1D disponível mas imagem não é usada.
- **V-prediction vs ε-prediction.**Para regimes estreitos (t muito pequenos ou muito grandes), `ε`- a previsão de V (`v = α·ε - σ·x`) é mais estável; SDXL, SD3 e Flux utilizam-na.
  **V 预测 vs ε 预测。**Em extremo tempo, V 预测更稳定; SDXL、SD3、Flux usá-lo.
- **Classifier-free guidance.**Na inferência, calcular as condições e as incondições.`ε`, então`ε_cfg = (1 + w) · ε_cond - w · ε_uncond`com`w ≈ 3-7`- Coberto na lição 8.
  **无分类器引导。**推理时计算条件和无条件预测的差值──第 08 课详述──
- **1000 steps is a lot.**A produção utiliza DDIM (20-50 passos), DPM-Solver (10-20 passos) ou destilação (1-4 passos).
  **1000 步太多了。**Produção com DDIM ((20-50 步)、DPM-Solver ((10-20 步)

## Use-o com o framework implementado.

| Role / 角色 | Typical stack in 2026 / 2026 典型技术栈 |
|------|-----------------------|
| Image pixel-space diffusion (small, toy) / 像素空间扩散 | DDPM + U-Net |
| Image latent diffusion / 潜在扩散 | VAE encoder + U-Net or DiT (Lesson 07) |
| Video latent diffusion / 视频潜在扩散 | Spatiotemporal DiT (Sora, Veo, WAN) |
| Audio latent diffusion / 音频潜在扩散 | Encodec + diffusion transformer |
| Science (molecules, proteins, physics) / 科学 | Equivariant diffusion (EDM, RFdiffusion, AlphaFold3) |

A difusão é a espinha dorsal generativa universal. A combinação de fluxos (Lessão 13) é o concorrente 2024-2026, que geralmente ganha na velocidade de inferência pela mesma qualidade.

> 扩散是通用生成骨干;;Flow Matching (第 13 课) é um concorrente de 2024-2026, normalmente, sob a mesma qualidade, a hipótese é mais rápida.

## Envia-o . Produto .

Salvar`outputs/skill-diffusion-trainer.md`. A competência assume um conjunto de dados + orçamento e resultados de cálculo: cronograma (linear/cosino/sigmoide), meta de previsão (ε/v/x), número de etapas, escala de orientação, família de amostragens e um protocolo de avaliação.

> 保存 `outputs/skill-diffusion-trainer.md` Habilidade de recepção de dados + orçamento de cálculo, saída de dados, previsão de objetivos, medidas, orientação de redução, análise e avaliação de dados.

## Exercícios.

1. **Easy / 简单.**Mudança de T de 40 para 10 em `code/main.py`Como a qualidade da amostra (histograma visual das saídas) se degrada?
   A partir de 40 para 10 ⋅ Como é que a qualidade da amostra se degrada?
2. **Medium / 中等.**Passe da previsão ε para a previsão v. Retrai a passagem inversa. Comparar a qualidade final da amostra.
   Desde ε 预测切换到v 预测。 re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re-re
3. **Hard / 困难.**Adicionar orientação sem classificador. Condição em um rótulo de classe `c ∈ {0, 1}`, diminuir 10% do tempo durante o treinamento e no tempo de amostragem de uso `ε = (1+w)·ε_cond - w·ε_uncond`. Medir a taxa de acidentes no modo condicional em `w = 0, 1, 3, 7`- Não .
   添加无分类器引导──测量 `w = 0, 1, 3, 7`时的条件模式命中率──

## Termos-chave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Forward process | "Adding noise" / "加噪" | Fixed Markov chain `q(x_t \| x_{t-1})` that destroys the data. / 破坏数据的固定马尔可夫链。 |
| Reverse process | "Denoising" / "去噪" | Learned chain `p_θ(x_{t-1} \| x_t)` that reconstructs the data. / 重建数据的学习链。 |
| β schedule | "The noise ladder" / "噪声阶梯" | Per-step variance; linear, cosine, or sigmoid. / 每步方差；线性、余弦或 S 形。 |
| α̅ | "Alpha bar" | Cumulative product `∏(1 - β)`; gives closed-form `x_t` from `x_0`. / 累积乘积，给出闭式 `x_t`。 |
| Simple loss | "MSE on noise" / "噪声 MSE" | `\|\|ε - ε_θ(x_t, t)\|\|²`; all variational derivations collapse to this. / 所有变分推导最终坍塌为此。 |
| ε-prediction | "Predict noise" / "预测噪声" | Output is the noise added; standard DDPM. / 输出是添加的噪声。 |
| V-prediction | "Predict velocity" / "预测速度" | Output is `α·ε - σ·x`; better conditioning across t. / 跨时间步条件化更好。 |
| DDPM | "The paper" / "那篇论文" | Ho et al. 2020; linear β, 1000 steps, U-Net. |
| DDIM | "Deterministic sampler" / "确定性采样器" | Non-Markov sampler, 20-50 steps, same training objective. / 非马尔可夫采样器。 |
| Classifier-free guidance | "CFG" | Mix conditional and unconditional noise predictions to amplify conditioning. / 混合条件和无条件预测以放大条件化。 |

## Nota de produção: inferência de difusão é um problema de contagem de etapas.

O documento DDPM executar T=1000 passos reversa. Ninguém envia isso na produção. Cada pilha de inferência real escolhe uma das três estratégias  e cada mapa limpo para enquadramento de produção de "de onde vem a latência":

> DDPM 论文 T=1000 反向步──生产中没有人这样做──每种策略对应生产中"延迟来自哪里":

1. **Faster sampler, same model.**DDIM (20-50 passos), DPM-Solver++ (10-20), UniPC (8-16). Substituição de drop-in do loop inverso; o treinado `ε_θ`Os pesos são intocados, reduz a latência 20 a 50 vezes.
   **更快的采样器，相同模型。**DDIM、DPM-Solver++、UniPC──即插即用替换反向循环,降低延迟 20-50倍──
2. **Distillation.**Treinar um aluno para se adequar ao professor em menos passos: Distilação Progressiva (2 → 1), Modelos de Consistência (arbitrário → 1-4), LCM, SDXL-Turbo, SD3-Turbo. Cortar a latência mais 5-10x, requer reformulação.
   **蒸馏。**訓練学生模型在更少步数匹配教师──再降延迟 5-10 倍,需要重训──
3. **Caching and compilation.** `torch.compile(unet, mode="reduce-overhead")`, os retrospectivos de difusão do TensorRT-LLM,`xformers`/SDPA atenção, bf16 pesos. Cortes por etapa latência ~ 2×.
   **缓存和编译。**Torch.compile、TensorRT、xformers、bf16──降低每步延迟约2倍──

Para um servidor de difusão de produção, a conversação orçamental é a mesma que a literatura de produção descreve para os LLM: a latência é `num_steps × step_cost + VAE_decode`, o volume é `batch_size × (num_steps × step_cost)^-1`. O TTFT é pequeno (um passo); o TPOT é equivalente ao tempo de resposta total porque a geração de imagens é "todo ao mesmo tempo" da perspectiva do utilizador.

> O orçamento do serviço de produção de produtos de produção e de expansão é o mesmo que o programa de gestão de produtos de produção de produtos de produção.`num_steps × step_cost + VAE_decode`△TTFT 很小(一步);TPOT 等价物是完整响应时间──

## Mais leitura 延伸阅读

- [Sohl-Dickstein et al. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics](https://arxiv.org/abs/1503.03585) o papel de difusão, antes do seu tempo.
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) DDPM.
- [Song, Meng, Ermon (2021). Denoising Diffusion Implicit Models](https://arxiv.org/abs/2010.02502)- DDIM, menos passos.
- [Nichol & Dhariwal (2021). Improved DDPM](https://arxiv.org/abs/2102.09672)- Calendário cosínico, variação aprendida.
- [Dhariwal & Nichol (2021). Diffusion Models Beat GANs on Image Synthesis](https://arxiv.org/abs/2105.05233) Orientações para o classificador.
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598)- CFG.
- [Karras et al. (2022). Elucidating the Design Space of Diffusion-Based Generative Models (EDM)](https://arxiv.org/abs/2206.00364)- Notação unificada, receita mais limpa.
