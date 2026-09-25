# Difusão latente e difusão estável .

> A difusão de espaço de pixels em imagens 512x512 é um crime de guerra computacional. Rombach et al. (2022) notou que você não precisa de todas as dimensões 786k para gerar uma imagem  você precisa de suficiente para capturar estrutura semântica, e um decodificador separado para o resto.

> **【中文解读】**Em 512x512 像素空间做扩散是计算灾难──Rombach 等人发现不需要全部 78.6万维度只需要捕获语义结构,剩余用解码器补充──

> **【拓展：Stable Diffusion 的革命】**A Diffusão Estabilizada irá promover o processo de expansão do espaço de imagem para o espaço potencial, reduzindo a quantidade de cálculo dezenas de vezes, permitindo que a GPU de nível de consumo possa ser operada. Após a liberação do código aberto, ocasionou o LoRA, o ControlNet, etc.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 02 (VAE), Phase 8 · 06 (DDPM), Phase 7 · 09 (ViT)
**Time:** ~75 minutes

## O problema é o problema da introdução

A difusão no espaço-pixel no 5122 significa que a U-Net funciona em tensores de forma .`[B, 3, 512, 512]`Cada passo de amostragem é de ~100 GFLOPS para uma rede U-Net de 500M. Cinquenta passos são 5 TFLOPS por imagem.

> 5122 像素空间扩散 significa U-Net em `[B, 3, 512, 512]`张量上运行──每采样步约100 GFLOPS──50 步就是5 TFLOPS──在十亿图像上训练计算成本荒谬──

A maioria desses FLOPs vai empurrar detalhes perceptivamente não importantes através da rede  a textura de alta frequência que um VAE perdedor poderia comprimir. A ideia de Rombach: treinar um VAE uma vez (o * primeiro estágio *), congelar-o e executar a difusão inteiramente no espaço latente de 4 canais 64×64 (o * segundo estágio *).

> A grande parte dos FLOPs é usada para promover o intuito sobre detalhes não importantes.

Esta é a receita da Estabilidade de Difusão.`64×64×4`Os dados dos dados de dados dos sistemas de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados`128×128×4`O SD3 trocou a U-Net por um Transformador de Difusão (DiT) com correspondência de fluxo. Flux.1-dev (Black Forest Labs, 2024) envia um DiT-MMDiT de 12B-param. Todos funcionam no mesmo substrato de dois estágios.

> É o que é o sistema de difusão estável. SD 1.x/2.x usando 860M U-Net em 64×64×4 em cima, SDXL usando 2.6B U-Net em 128×128×4 em cima, SD3 usando DiT + Flow Matching substituindo U-Net.

> **【中文解读】**A estrutura central da difusão está em duas fases: 1) Primeiro estágio VAE 编码器将512x512 图像压缩到64x64x4 潜在空间(16 倍压缩); 2) Segundo estágio 运行在潜在空间中运行扩散过程――U-Net 在 64x64 张量上运行,计算量降低约64 倍――Desde SD 1.x até SD3 演变:U-Net → DiT(Diffusion Transformer),DDPM → Flow Matching――

> **【拓展：从 U-Net 到 DiT 的架构变迁】**SD 1.x/2.x Utilize U-Net  como rede de desvio de ruído。SD3(2024) e FLUX  转向 DiT(Diffusion Transformer)  Use Transformer 替代 U-Net。DiT 优势在于扩展性更好(Transformer 的缩放定律适用) 支持更高分辨率、可以更好地融合文本条件── essa estrutura está em conformidade com a transformação 统一趋势在NLP 领域.

## O conceito central.

![Latent diffusion: VAE compression + diffusion in latent space](../assets/latent-diffusion.svg)

**Two stages, separately trained.**

> **两个阶段，分别训练。**

1. **Stage 1 — VAE.**Encoder `E(x) → z`, decodificador`D(z) → x`. Compressão alvo: 8x amostra descendente em cada eixo espacial + ajuste de canais para que o tamanho total latente seja ~1/16 da contagem de pixels. perda = reconstrução (L1 + LPIPS perceptivo) + KL (pequeno peso, portanto `z`Não é forçado Gaussian, porque não precisamos de amostragem exata de`z`O que é que é uma forma de fazer isso?

   **阶段 1 — VAE。**编码器 `E(x) → z`, descifrador `D(z) → x`△ objetivo compressão: △ 8 倍下采样──损失 = 重建(L1 + LPIPS) + KL(小权重)。

2. **Stage 2 — diffusion on `z`.**Tratar`z = E(x_real)`- A formação de uma rede U-Net (ou DiT) para denúncia`z_t`- Em inferência: amostra`z_0`através da difusão, então `x = D(z_0)`- Não .

   **阶段 2 — 在 `z` 上扩散。**- Não .`z = E(x_real)`视为数据──训练 U-Net(或 DiT)去噪音──推理时:采样 `z_0`, então`x = D(z_0)`- Não.

**Text conditioning.**Dois componentes adicionais: um codificador de texto congelado (CLIP-L para SD 1.x, CLIP-L+OpenCLIP-G para SD 2/XL, T5-XXL para SD3 e Flux).`[Q = image features, K = V = text tokens]`Os tokens são a única forma de texto influenciar a imagem.

> **文本条件化。**结的文本编码器和交叉注意注入── cada bloco U-Net é usado 结的文本编码器和交叉注意注入──`[Q = 图像特征, K = V = 文本 token]`Fazer um esforço de atenção: o toque é a única maneira de influenciar o texto.

**The loss function is identical to Lesson 06.**O mesmo DDPM / fluxo de correspondência MSE no ruído.

> **损失函数与第 06 课完全相同。**Apenas trocámos os dados.

## Arquitetura variante

| Model / 模型 | Year | Backbone / 骨干 | Latent shape / 潜在形状 | Text encoder / 文本编码器 | Params / 参数量 |
|-------|------|----------|--------------|--------------|--------|
| SD 1.5 | 2022 | U-Net | 64×64×4 | CLIP-L (77 tokens) | 860M |
| SD 2.1 | 2022 | U-Net | 64×64×4 | OpenCLIP-H | 865M |
| SDXL | 2023 | U-Net + refiner | 128×128×4 | CLIP-L + OpenCLIP-G | 2.6B + 6.6B |
| SDXL-Turbo | 2023 | Distilled | 128×128×4 | same | 1-4 step sampling / 1-4 步采样 |
| SD3 | 2024 | MMDiT (multimodal DiT) | 128×128×16 | T5-XXL + CLIP-L + CLIP-G | 2B / 8B |
| Flux.1-dev | 2024 | MMDiT | 128×128×16 | T5-XXL + CLIP-L | 12B |
| Flux.1-schnell | 2024 | MMDiT distilled | 128×128×16 | T5-XXL + CLIP-L | 12B, 1-4 step |

A tendência: substituir a U-Net por DiT (transformador sobre patches latentes), escalar o codificador de texto (T5 supera o CLIP para adesão rápida), aumentar os canais latentes (4 → 16 dá mais espaço de detalhe).

> 趋势: Usar DiT 替代U-Net, ampliar文本编码器(T5 在 prompt 遵循上优于CLIP), aumentar os potenciais passagens(4→16 给更多细节余量) 

## Construí-lo e realizei-o.
```figure
noise-schedule
```

## Construí-lo

`code/main.py`Estabelece um brinquedo 1-D "VAE" (encodeador de identidade + decodeador, para demonstração; um verdadeiro VAE seria uma rede de conexão) em cima do DDPM da lição 06 e adiciona condicionamento de classe com orientação sem classificador.

> `code/main.py`Na 6a aula, sobre o DDPM  superpõe-se um brinquedo 1D "VAE" e adiciona um guia de classe condicionada sem classificação.

### Passo 1: codificador/decodificador

```python
def encode(x):    return x * 0.5          # toy "compression" to smaller scale
def decode(z):    return z * 2.0
```

Para a pedagogia, este mapa linear é suficiente para mostrar que a difusão opera em`z`sem se preocupar com o espaço de dados original.

> A verdadeira VAE tem um bom peso treinado. Na educação, este mapa linear é suficiente para mostrar a expansão.`z`Não se preocupem com o espaço de dados original.

### Passo 2: difusão em`z`- Espaço

A mesma DDPM que a lição 06.`z = E(x)`Após a amostragem`z_0`, decodificar com `D(z_0)`- Não .

> O mesmo que o DDPM do curso 06 ⋅ dados vistos na rede são `z = E(x)`- Sim, sim.`z_0`后用 `D(z_0)`- Não.

### Passo 3: Orientação sem classificador

Durante o treino, deixe de lado a etiqueta de classe 10% do tempo (substitua-a por um token zero).`ε_cond`E ...`ε_uncond`, então:

```python
eps_cfg = (1 + w) * eps_cond - w * eps_uncond
```

`w = 0`= não há orientação (plena diversidade), `w = 3`= padrão, `w = 7+`= saturado / demasiado nítido.

> `w = 0`= 无引导(完全多样性),`w = 3`= 默认,`w = 7+`= 和/过度利。

### Passo 4: condicionamento de texto (conceito, não código)

Substitua o rótulo de classe com uma saída de codificador de texto congelado. Alimenta o texto incorporado para a U-Net através da atenção cruzada:

> Utilize o código de texto para o seu conteúdo.

```python
h = h + CrossAttention(Q=h, K=text_embed, V=text_embed)
```

Esta é a única diferença substancial entre um modelo de difusão condicional de classe e a difusão estável.

> Esta é a única diferença substancial entre o modelo de expansão de condições de classe e a difusão estável.

## Encaixos.

- **VAE-scale mismatch.**SD 1.x VAEs têm uma constante de escala (`scaling_factor ≈ 0.18215`O que é que é o problema é que a rede U-Net está em latência com variação muito errada.
  **VAE 尺度不匹配。**SD 1.x VAE  codificação depois de um número regular de comprimento.
- **Text encoder silently wrong.**SD3 precisa de T5-XXL com >=128 tokens, e o regresso para CLIP-só é perdedor.`use_t5=True`ou crateras de fidelidade.
  **文本编码器静默错误。**SD3 需要 T5-XXL 且 >=128 token──
- **Mixing latent spaces.**SDXL, SD3, Flux todos usam diferentes VAEs. Um LoRA treinado em latentes SDXL não funcionará em SD3.
  **混合潜在空间。**SDXL、SD3、Flux Usar diferentes VAE──SDXL de LoRA não pode usar em SD3 │
- **CFG too high.** `w > 10`O ponto mais interessante é que a sua qualidade de vida é muito mais elevada.`w = 3-7`- Não .
  **CFG 太高。** `w > 10`产生和、油的图像──
- **Negative prompts leaking.**Um prompt negativo vazio torna-se o token zero; um prompt negativo preenchido torna-se o `ε_uncond`Não são os mesmos; alguns oleodutos silenciosamente param para o zero.
  **负向 prompt 泄漏。**空负向 prompt 变为零代币; preenchimento de变为 `ε_uncond`                                                                                                                                                                                                                                                              

## Use-o com o framework implementado.

Estacas de produção em 2026:

> 2026       

| Target / 目标 | Recommended backbone / 推荐骨干 |
|--------|----------------------|
| Narrow domain, paired data, from scratch / 窄域配对从零训练 | SDXL fine-tune (LoRA / full) — fastest to ship |
| Open-domain text-to-image, open weights / 开放域开放权重 | Flux.1-dev (12B, Apache / non-commercial) or SD3.5-Large |
| Fastest inference, open weights / 最快推理开放权重 | Flux.1-schnell (1-4 step, Apache) or SDXL-Lightning |
| Best prompt adherence, hosted / 最佳 prompt 遵循，托管 | GPT-Image / DALL-E 3, Midjourney v7, Imagen 4 |
| Edit workflows / 编辑工作流 | Flux.1-Kontext (Dec 2024) — natively accepts image + text |
| Research, baseline / 研究基线 | SD 1.5 — ancient but well-studied |

## Envia-o . Produto .

Salvar`outputs/skill-sd-prompter.md`. A Skill assume um prompt de texto + estilo de destino e as saídas: modelo + ponto de verificação, escala CFG, amostragem, prompt negativo, resolução, combinação opcional de ControlNet/IP-Adapter e uma lista de verificação de qualidade por etapa.

> 保存 `outputs/skill-sd-prompter.md` Habilidade de receber texto + objetivo, modelo + de saída, ponto de verificação, CFG, máquina de recolha, negativo para o prompt, etc.

## Exercícios.

1. **Easy / 简单.**Corra .`code/main.py`com orientação.`w ∈ {0, 1, 3, 7, 15}`- Registrar a amostra média por classe.`w`Os meios de classe divergem além dos meios de dados reais?
   - Não .`w ∈ {0, 1, 3, 7, 15}`- Não, não.`w`Valor da classe média em relação ao valor médio dos dados reais?
2. **Medium / 中等.**Troque o codificador linear do brinquedo por um par de codificador/decodificador tanh-MLP com perda de reconstrução. Retrain difusão nos novos latentes.
   O que é o novo sistema de código de brinquedos?
3. **Hard / 困难.**Configurar uma verdadeira inferência de difusão estável com difusores: carga `sdxl-base`, executar 30 passos de Euler com CFG=7, tempo. Agora, desligue para `sdxl-turbo`O mesmo assunto, qualidade diferente descreve o que mudou e porquê.
   Utilize difusores 搭建真实SD 推理, comparar SDXL-base 和 SDXL-Turbo──

## Termos-chave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| First stage | "The VAE" | Trained encoder/decoder pair; compresses 512² to 64². / 训练好的编码/解码器对；将 512² 压缩到 64²。 |
| Second stage | "The U-Net" | Diffusion model over the latent space. / 潜在空间上的扩散模型。 |
| CFG | "Guidance scale" / "引导缩放" | `(1+w)·ε_cond - w·ε_uncond`; tunes conditioning strength. / 调节条件化强度。 |
| Null token | "Empty prompt embed" / "空 prompt 嵌入" | Unconditional embed used for `ε_uncond`. / 用于无条件预测的嵌入。 |
| Cross-attention | "How text gets in" / "文本如何进入" | Each U-Net block attends to text tokens as K and V. / 每个 U-Net 块对文本 token 做注意力。 |
| DiT | "Diffusion Transformer" | Replace U-Net with a transformer over latent patches; scales better. / 用 Transformer 替代 U-Net。 |
| MMDiT | "Multi-modal DiT" / "多模态 DiT" | SD3's architecture: text and image streams with joint attention. / SD3 架构：文本和图像流的联合注意力。 |
| VAE scaling factor | "Magic number" / "魔数" | Divides latents by ~5.4 so diffusion operates in unit-variance space. / 除以约 5.4 使扩散在单位方差空间操作。 |

## Nota de produção: executar Flux-12B em uma GPU de consumo de 8GB

A integração de Flux de referência é a receita canônica "Eu tenho uma GPU de consumo, posso enviar isso?" O truque é o mesmo de três botões de receita de produção de inferência de literatura de listas aplicadas a uma difusão DiT:

> Referência Flux 集成是经典的"Eu só tenho GPU de consumo,能部署吗?"方案──三旋方案:

1. **Staggered loading.**Flux tem três redes que nunca precisam coexistir na VRAM: T5-XXL codificador de texto (~ 10 GB em fp32), CLIP-L (pequeno), o 12B MMDiT e o VAE. Encode o prompt primeiro, * excluir* os codificadores, carregar o DiT, denoise, * excluir* o DiT, carregar o VAE, decodificar. GPUs de consumo de 8 GB apenas cabem em uma etapa por vez.
   **交错加载。**Flux tem três não precisa permanecer simultaneamente na rede de VRAM.
2. **4-bit quantization via bitsandbytes.** `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16)`No codificador T5 e no DiT. Cortando a memória 8x, a queda de qualidade é imperceptível para o texto-à-imagem por referências do Aritra (linkado no notebook).
   **4 位量化。**A quantificação de T5 e DiT para 4 bits, a memória reduzida 8 vezes, a perda de qualidade é mínima.
3. **CPU offload.** `pipe.enable_model_cpu_offload()`Auto-swaps módulos entre CPU e GPU como cada passo avança. Adiciona 10-20% de latência, mas faz o pipeline funcionar em tudo.
   **CPU 卸载。**Automática de troca de módulos entre CPU e GPU.

A contabilidade da memória é: `10 GB T5 / 8 = 1.25 GB`quantizada, `12 B params × 0.5 bytes = ~6 GB`DiT quantizado, mais ativações. Em termos de stas00 esta é a extremidade da inferência TP=1  sem paralelismo de modelo, quantização máxima. Para produção você executaria TP=2 ou TP=4 em H100s; para um único laptop de desenvolvimento, esta é a receita.

## Mais leitura 延伸阅读

- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) Difusão estável.
- [Podell et al. (2023). SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis](https://arxiv.org/abs/2307.01952) SDXL.
- [Peebles & Xie (2023). Scalable Diffusion Models with Transformers (DiT)](https://arxiv.org/abs/2212.09748)- Não.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) SD3, MMDiT.
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598)- CFG.
- [Labs (2024). Flux.1 — Black Forest Labs announcement](https://blackforestlabs.ai/announcing-black-forest-labs/) Família Flux.1.
- [Hugging Face Diffusers docs](https://huggingface.co/docs/diffusers/index) Implementação de referência para cada ponto de controlo acima.
