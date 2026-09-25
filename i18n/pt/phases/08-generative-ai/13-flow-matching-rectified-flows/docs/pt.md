# Flow Matching & Rectified Flow 流匹配与整流

> Os modelos de difusão tomam 20-50 passos de amostragem porque percorrem um caminho curvo do ruído para os dados. A combinação de fluxo (Lipman et al., 2023) e fluxo retificado (Liu et al., 2022) treinaram caminhos retos. Os caminhos mais retos significam menos passos significam inferência mais rápida.

> **【中文解读】**O modelo de expansão requer 20-50 passos de aprendizagem, pois é o caminho de corrida. Flow Matching e Rectified Flow Training Direct Line Pathways  Pior direção significa menos passos e mais rápida conclusão. SD3、FLUX.1、AudioCraft 2 são mudados para Flow Matching em 2024.

> **【拓展：Flow Matching 是 2024-2026 的趋势】**O Flow Matching está substituindo a tradição de regulação de expansão como padrão de um novo modelo de geração. É matematicamente mais elegante, experimentalmente mais eficaz.

**Type:** Build / 构建型 | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 8 · 06 (DDPM), Phase 1 · Calculus / 微积分 | **前置知识:** 阶段 8 · 06（DDPM），阶段 1 · 微积分
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## O problema é o problema da introdução

O processo inverso do DDPM é um passeio estocástico de 1000 passos de `N(0, I)`O DDIM desmoronou-o para 20-50 passos deterministas. Você quer menos passos  idealmente um. O bloqueador é que o ODE resolvendo o processo inverso é rígido; o caminho é curvo.

> O processo de reversão do DDPM é de`N(0, I)`De volta a 1000 passos de distribuição de dados, o DIM reduzirá a compressão para 20 a 50 passos.

Se pudesse treinar o modelo de tal forma que o caminho do ruído para os dados fosse uma *linha reta*, um único passo de Euler de `t=1`- Não .`t=0`A combinação de fluxos constrói isto diretamente: definir uma interpolação reta a partir de`x_1 ∼ N(0, I)`- Não .`x_0 ∼ data`, treinar um campo vetorial `v_θ(x, t)`para combinar a sua derivada do tempo, integrar na inferência.

> Se puder o modelo de treinamento fazer ruído para dados o caminho é *direita*, passo de Euler de `t=1`Até`t=0`Basta. Flow Matching.`x_1 ∼ N(0, I)`Até`x_0 ∼ data`O que é o "training" ?`v_θ(x, t)`匹配时间导数──

O fluxo retificado (Liu 2022) vai mais longe: endireita iterativamente os caminhos com um procedimento de refluxo que produz um ODE progressivo mais próximo a linear. Após duas iterações de refluxo, um amostragem de 2 passos corresponde à qualidade de DDPM de 50 passos.

> Flow rectified (rectified flow) 2022) 更多: 通过 reflow 过程代拉直路径──两次 reflow 代后,2 步采样器匹配 50 步 DDPM 质量──

> **【中文解读】**Flow Matching 定义 x_1(ruído) a x_0(data) 的直线插值,训练向量场 v_theta(x,t) 匹配时间导数――修正 Flow 进一步通过 reflow 代拉直路径,2 步采样即可匹配50 步 DDPM 的质量──

> **【拓展：FLUX.1 的 Flow Matching 实现】**FLUX.1 do Black Forest Labs (em inglês) é criado por Stable Diffusion (em inglês) usando Flow Matching (em inglês) para criar imagens de alta qualidade, que são de grande qualidade em termos de qualidade e velocidade de produção.

## O conceito central.

![Flow matching: straight-line interpolation between noise and data](../assets/flow-matching.svg)

### Fluxo em linha reta

Define:

>  definição:

```
x_t = t · x_1 + (1 - t) · x_0,   t ∈ [0, 1]
```

onde`x_0 ~ data`E ...`x_1 ~ N(0, I)`A derivada temporal ao longo desta reta é constante:

> Entre eles `x_0 ~ data`- Não .`x_1 ~ N(0, I)`  O número de direções de tempo a longo desta linha é constante:

```
dx_t / dt = x_1 - x_0
```

Defina um campo de vetor neural `v_θ(x_t, t)`e treinar para combinar com esta derivada:

> 定義神经向量场 `v_θ(x_t, t)`, treiná-lo para combinar este número:

```
L = E_{x_0, x_1, t} || v_θ(x_t, t) - (x_1 - x_0) ||²
```

É o que eu faço .**conditional flow matching**O programa de formação é gratuito: nunca se desbloqueia o ODE.`(x_0, x_1, t)`e regressão.

> É isso.**条件 Flow Matching**损失(Lipman 2023) ―― training is simulation-free 的:你永远不需要展开 ODE──只需要采样`(x_0, x_1, t)`Não fizemos a volta.

### Amostra de amostra.

Na inferência, integra o campo vetorial aprendido * para trás* no tempo:

> 推理时,将学到的量场沿时间*反向*积分:

```
x_{t-Δt} = x_t - Δt · v_θ(x_t, t)
```

Começa em`x_1 ~ N(0, I)`, Euler-passo para baixo para `t=0`- Não .

> De`x_1 ~ N(0, I)`Começa, com o Euler.`t=0`- Não.

### Fluxo corrigido (Liu 2022) 整流流(Liu 2022)

O fluxo em linha reta funciona, mas os caminhos aprendidos não são realmente retos.`x_0`s pode mapear para o mesmo `x_1`. Passo de refluxo do fluxo corrigido:

> Mesmo que seja eficaz, o caminho aprendido não é realmente direto.`x_0`Pode ser projetado para o mesmo.`x_1`,路径会曲──Reflow of Reflux 步骤:

1. Modelo de fluxo de trem v_1 com acoplamento aleatório.
   Use as suas capacidades de treinamento Flow 模型 v_1──
2. Amostra N pares `(x_1, x_0)`integrando v_1 de `x_1`até ao seu pouso .`x_0`- Não .
   通過將 v_1 从 `x_1`积分到落点 `x_0`采样 N 对 `(x_1, x_0)`- Não.
3. Como os pares agora são "ODE-matched", o interpolante em linha reta entre eles é realmente mais plano.
   Em estas combinações de amostras, o conjunto de dados é "ODE 匹配", e o valor de inserção entre elas é realmente mais plano.
4. Repito. - Não.
   - Não, não.

Na prática, 2 iterações de reflow levam você a quase linear, permitindo inferência de 2-4 passos. SDXL-Turbo, SD3-Turbo, LCM são todos modelos destilados de fluxo-matching.

> Na prática, 2 vezes reflow 代就能使路径接近线性, త తద్వారా apoiar 2-4 步推理──SDXL-Turbo、SD3-Turbo、LCM são baseados em modelos de Flow Matching 蒸出──

### Por que isso ganhou para imagens em 2024 ? Por que 2024 geração de imagens completa para fluxo de correspondência

Três razões:

> Três razões:

1. **Simulation-free training** não haverá ODE que se desenrolem durante a formação, sendo trivial a implementar.
   **无需仿真的训练** treinamento                                                                                                                                                                                                                                                             
2. **Better loss geometry** Os caminhos retos têm um sinal-ruído consistente, enquanto o DDPM ε-loss tem um SNR ruim nas bordas do cronograma.
   **更优的损失几何**直线路径信噪比一致, enquanto a ε- perda do DDPM está em menor nível do SNR.
3. **Faster inference** 4-8 etapas com qualidade SDXL-Turbo; 1 etapa com destilação de consistência.
   **更快的推理**4-8 步即可达到 SDXL-Turbo 质量; 配合一致性蒸可一步生成

## Flow matching vs DDPM  a conexão exata  Flow matching vs DDPM  精确联系

A correspondência de fluxo com um caminho condicional de Gauss é difusão *com um cronograma específico de ruído*.`x_t = α(t) x_0 + σ(t) x_1`O calendário e o fluxo correspondentes recuperam a difusão reformulada por Stratonovich com `v = α'·x_0 - σ'·x_1`Os dois são algébricos equivalentes para os caminhos de Gaussian.

> Utilize High-Condition Pathways Flow Matching                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 `x_t = α(t) x_0 + σ(t) x_1`调度后,Flow Matching ainda está disponível em Stratonovich 形式重写的扩散,其中 `v = α'·x_0 - σ'·x_1` Para os altos padrões, ambos são iguais em valores.

O que o fluxo de correspondência adicionou: a *clarity* do alvo (uma velocidade simples), uma perda mais limpa, e a licença para experimentar com interpolantes não gaussianos.

> A verdadeira contribuição do fluxo de correspondência é: a meta de * claridade *(uma velocidade normal de velocidade) 、 perda de mais puro, bem como a liberdade de tentar não-alto-posição.

## Construí-lo e realizei-o.
```figure
normalizing-flow
```

## Construí-lo

`code/main.py`Implementa a correspondência de fluxo 1-D em uma mistura de Gaussian de dois modos.`v_θ(x, t)`A conclusão é que, ao fazer uma conclusão, integrar 1, 2, 4 e 20 passos de Euler e comparar a qualidade da amostra.

> `code/main.py`Em duas cotas de alta concentração, a distribuição mistura é realizada em 1D Flow Matching.`v_θ(x, t)`É um MLP de pequeno tipo, usando treinamento de objetivos diretos.

### Passo 1: Perda de treinamento.

```python
def train_step(x0, net, rng, lr):
    x1 = rng.gauss(0, 1)
    t = rng.random()
    x_t = t * x1 + (1 - t) * x0
    target = x1 - x0
    pred = net_forward(x_t, t)
    loss = (pred - target) ** 2
    # backprop + update
```

> 訓練損失: 采样噪音                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     `x1`E o tempo`t`, construção de valores`x_t`, objectivo `x1 - x0`, fazer o regresso quadrado.

### Passo 2: inferência em vários passos. Passo 2: mais passos.

```python
def sample(net, num_steps):
    x = rng.gauss(0, 1)
    for i in range(num_steps):
        t = 1.0 - i / num_steps
        dt = 1.0 / num_steps
        x -= dt * net_forward(x, t)
    return x
```

> Do alto do ruído, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em segundo passo, em que em segundo passo, em segundo passo, em que em segundo passo, em segundo passo, em que em segundo passo, em segundo passo, em que o mais preciso e em que é.

### Passo 3: Comparar o número de passos.

Esperem que o amostragem de 4 passos já corresponda à qualidade de 20 passos, um grande problema para a latência.

> 4 步采采器应已匹配 20 步质量 Este é um grande aperfeiçoamento em relação ao atraso

## Encaixos.

- **Time parameterization.**Utilizações de correspondência de fluxo `t ∈ [0, 1]`com`t=0`em dados, `t=1`- a utilização de DDPM`t ∈ [0, T]`com`t=0`em dados, `t=T`O mesmo rumo, em escala diferente, os papéis estão sempre errados.
  时间参数化: Flow Matching Used `t ∈ [0, 1]`- Não .`t=0`Em um dado,`t=1`Em uso de DDPM`t ∈ [0, T]`A direcção é a mesma, mas as dimensões são diferentes.
- **Schedule choice.**A linha reta do fluxo corrigido é "o" cronograma de correspondência de fluxo, mas você pode usar o cosino ou logit-normal t-sampling (SD3 faz isso) para uma melhor cobertura em escala.
  调度选择:Relicted Flow 直线是"标准"的流量匹配调度, mas pode ser usado com cosino ou logit-normal de t 采样 (SD3 é o que se faz) para obter melhor cobertura de escala.
- **Reflow cost.**Gerar o conjunto de dados emparelhados para refluxo é uma passagem completa de inferência por amostra. Só fazer refluxo quando você realmente precisa de inferência de 1-2 passos.
  Reflow 成本: geração de reflow 配对数据集需要每样本一次完整推理──只有真正需要1-2步推理时才做 reflow──
- **Classifier-free guidance still applies.**Basta trocar ε por v na combinação linear: `v_cfg = (1+w) v_cond - w v_uncond`- Não .
  Classificador-Free Guidance  ainda aplica: apenas precisa de colocar em conjunto os elementos de um sistema de ligação`v_cfg = (1+w) v_cond - w v_uncond`- Não.

## Use-o com o framework implementado.

| Use case / 用途 | 2026 stack / 2026 技术栈 |
|----------|-----------|
| Text-to-image, best quality / 最佳质量文生图 | Flow matching: SD3, Flux.1-dev |
| Text-to-image, 1-4 steps / 1-4 步文生图 | Distilled flow matching: Flux.1-schnell, SD3-Turbo, SDXL-Turbo |
| Real-time inference / 实时推理 | Consistency distillation from a flow-matched base (LCM, PCM) |
| Audio generation / 音频生成 | Flow matching: Stable Audio 2.5, AudioCraft 2 |
| Video generation / 视频生成 | Flow matching mixed with diffusion (Sora, Veo, Stable Video) |
| Science / physics / 科学/物理 | Flow matching + equivariant vector field |

Sempre que um artigo diz "mais rápido do que a difusão" em 2025-2026, é quase sempre o fluxo de correspondência + destilação.

> Quando o artigo diz "Bívio expandido mais rápido", quase sempre é Fluxo de Combinação + 蒸──

## Envia-o . Produto .

Salvar`outputs/skill-fm-tuner.md`. A Skill toma uma especificação de modelo de estilo difusão e converte-a em uma configuração de treinamento de correspondência de fluxo: escolha de horário, distribuição de amostragem de tempo (uniforme / logit-normal), optimizador, plano de refluxo, contagem de etapas-alvo, protocolo de avaliação.

> 保存为 `outputs/skill-fm-tuner.md` Esta habilidade recebe um modelo de regulamentação de expansão, transformá-lo em Flow Matching  training config:调度选择、时间采样分布(uniform / logit-normal) 、优化器、reflow 计划、目标步数、评估协议。

## Exercícios.

1. **Easy.**Corra .`code/main.py`e comparar a distribuição de dados real com a MSE de 1 passo versus 20 passos.
   **简单。**运行 `code/main.py`, comparar 1 passo e 20 passo em relação à distribuição de dados reais MSE¬
2. **Medium.**- Desliga-te do uniforme .`t`A amostragem para logit-normal (concentra a amostragem em meados de t).
   **中等。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `t`采样切换为 logit-normal(集中在中间 t 附近采样) ―― modelo质量是否提升?
3. **Hard.**Implementar uma iteração de reflow: gerar emparelhado (x_0, x_1) integrando o primeiro modelo, treinar um segundo modelo nos pares e comparar a qualidade da amostra em 1 passo.
   **困难。**实现一次反流 代: através do primeiro modelo积分生成配对 (x_0, x_1), em treinamento no segundo modelo,并比较 1 步采样质量──

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Flow matching | "Straight-line diffusion" | Train `v_θ(x, t)` to match `x_1 - x_0` along an interpolant. |
| Rectified flow | "Reflow" | Iterative procedure that straightens learned flows. |
| Velocity field | "v_θ" | Output of the model — the direction to move `x_t`. |
| Straight-line interpolant | "The path" | `x_t = (1-t)·x_0 + t·x_1`; trivial target derivative. |
| Euler sampler | "1st order ODE solver" | Simplest integrator; works well when paths are straight. |
| Logit-normal t | "SD3 sampling" | Concentrate `t` sampling toward mid-values where gradients are strongest. |
| Consistency distillation | "1-step sampler" | Train a student to map any `x_t` directly to `x_0`. |
| CFG with velocity | "v-CFG" | `v_cfg = (1+w) v_cond - w v_uncond`; same trick, new variable. |

## Nota de produção: Flux.1-schnell é o fluxo de correspondência em seu mais rápido

A vitória de produção do fluxo de correspondência é Flux.1-schnell  um fluxo-correspondente DiT destilado para 1-4 passos de inferência mantendo a qualidade de grau Flux-dev. O notebook de Niels "Run Flux em uma máquina de 8GB" é a receita de implantação de referência: T5 + código CLIP, denotação quantizada de MMDiT (em 4 passos para rápido vs 50 para dev), decodificação VAE. A contabilidade de custos:

> Flux.1-schnell a vapor até 1-4 步推理、 manter Flux-dev 级质量的Flow-Matched DiT。Niels's "Flux operando em 8GB 机器上运行Flux" notebook é referência de depósito esquema:T5 + CLIP 编码、量化MMDiT 去噪(schnell 4 步 vs dev 50 步)、VAE 解码──成本核算:

| Variant | Steps | Latency at 1024² on L4 | Total FLOPs (relative) |
|---------|-------|------------------------|------------------------|
| Flux.1-dev (raw) | 50 | ~15 s | 1.0× |
| Flux.1-schnell | 4 | ~1.2 s | 0.08× (12× faster) |
| SDXL-base | 30 | ~4 s | 0.25× |
| SDXL-Lightning 2-step | 2 | ~0.3 s | 0.03× |

Regra de produção: **flow-matched base + distillation = the 2026 default for fast text-to-image.**Todos os principais fornecedores enviam esta combinação: SD3-Turbo (SD3 + fluxo + destilação), Flux-schnell (Flux-dev + rectified-flow straightening), CogView-4-Flash.

> Regras de produção:**Flow-Matched 基座 + 蒸馏 = 2026 年快速文生图的默认方案。**Cada fabricante principal lançou esta combinação:SD3-Turbo(SD3 + fluxo + 蒸)、Flux-schnell(Flux-dev + Fluxo Rectified 拉直)、CogView-4-Flash──纯扩散基座只为遗留检查点保留──

## Mais leitura 延伸阅读

- [Liu, Gong, Liu (2022). Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](https://arxiv.org/abs/2209.03003) fluxo rectificado.
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) correspondência de fluxo.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) SD3, fluxo rectificado em escala.
- [Albergo, Vanden-Eijnden (2023). Stochastic Interpolants](https://arxiv.org/abs/2303.08797) quadro geral que abrange a difusão FM+.
- [Song et al. (2023). Consistency Models](https://arxiv.org/abs/2303.01469) Destilação em 1 etapa de difusão/ fluxo.
- [Sauer et al. (2023). Adversarial Diffusion Distillation (SDXL-Turbo)](https://arxiv.org/abs/2311.17042)- Variante turbo.
- [Black Forest Labs (2024). Flux.1 models](https://blackforestlabs.ai/announcing-black-forest-labs/) correspondência de fluxo na produção.
