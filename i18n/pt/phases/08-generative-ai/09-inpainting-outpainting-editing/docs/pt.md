# Imagem, pintura e edição de imagem

> O texto-à-imagem cria coisas novas. A pintura consome coisas antigas. Na produção, 70% do trabalho de imagem que pode ser cobrado é a edição.

> **【中文解读】**文本生成图像创建新东西,图像修复(inpainting) Modificar o já existente;; 70% da produção de pagamento de imagem trabalha é editando 换背景、去 logo、扩展画布、重画手;;Inpainting é o lugar onde se espalha o modelo real钱;;

> **【拓展：Photoshop 生成式填充】**O Adobe Photoshop é baseado em tecnologia de pintura. Também permite que os usuários não profissionais possam transferir ou substituir qualquer conteúdo da imagem.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 8 · 08 (ControlNet & LoRA)
**Time:** ~75 minutes

## O problema é o problema da introdução

Um cliente envia uma foto perfeita do produto com um sinal distraente no fundo. Você quer apagar o sinal e deixar tudo o resto idêntico a pixels. Você não pode executar texto-a-imagem a partir do zero. O resultado terá uma cor diferente, iluminação diferente, ângulo de produto diferente. Você quer regenerar * somente * a região mascarada, e você quer que a regeneração respeite o contexto circundante.

> 客户发来一张完美的产品照片,背景有分散注意的标志――你想抹去标志并保持其他像素完全一致――你不能从头发运行文生图结果将有不同的颜色、光照和产品角度――你想只重生*被遮蔽区域*,并让重生内容尊重周围上下文――

Isso é pintar.

> É o que eu faço.

- **Inpainting.**Regenerar dentro de uma máscara, manter fora de pixels.
  **图像修复。**Em um escuro, reproduzir, manter imagens externas.
- **Outpainting.**Regenerar fora da máscara (ou além da tela), manter dentro.
  **图像扩展。**Em um escuro exterior, reproduzido, mantém-se dentro.
- **Image editing.**Regenerar toda a imagem, mas manter a fidelidade semântica ou estrutural ao original (SDEdit, InstructPix2Pix).
  **图像编辑。**Re-generar toda a imagem, mas manter a concordança linguística ou estrutura.

Cada pipeline de difusão em 2026 vai enviar um modo de pintura. Flux.1-Fill, Stable Diffusion Inpaint, SDXL-Inpaint, DALL-E 3 Edit. Eles funcionam com o mesmo princípio.

> 2026 Ano Cada corrente de água tem um padrão de pintura 模式──Flux.1-Fill、SD-Inpaint、SDXL-Inpaint、DALL-E 3 Edit──原理相同──

> **【中文解读】**Inpainting ([[Imagem Refação]]) é a necessidade de edição de imagens mais comum no ambiente de produção. O desafio central: apenas reproduzir a área coberta, mantendo simultaneamente a coerência com a área ao redor.

> **【拓展：Photoshop 生成式填充与商业 Inpainting】**A Adobe Photoshop é uma aplicação de pintura, que combina modelos de expansão e tecnologia de integração de margens, permitindo que os usuários possam, através de instruções de linguagem natural, remover/substituir qualquer conteúdo das imagens. Aplicações comerciais semelhantes também incluem Canva Magic Edit, AI Image Edit, etc.

## O conceito central.

![Inpainting: mask-aware denoising with context-preserving reinjection](../assets/inpainting.svg)

### A abordagem ingênua (e por que é errada)

> ### 朴素方法 (e por que não é assim)

Em cada passo de amostragem, substitua a região desmascarada do latente barulhento pela imagem limpa difundida para a frente.

> Usando um sistema de sombreamento, o modelo não sabe o que há em um sistema de sombreamento.

### O modelo de pintura adequado

> ### O que é o " Inpainting " ?

Treinar uma rede U-Modificada que toma 9 canais de entrada em vez de 4:

```
input = concat([ noisy_latent (4ch), encoded_image (4ch), mask (1ch) ], dim=channel)
```

Os canais extras são uma cópia da imagem fonte codificada por VAE e uma máscara de um único canal. No tempo de treinamento, você mascara aleatoriamente regiões da imagem e treina o modelo para denotar apenas a região mascarada, enquanto a região desmascarada é dada como um sinal de condicionamento limpo.

SD-Inpaint, SDXL-Inpaint, Flux-Fill todos usam esta entrada de 9 canais (ou analógicos).`StableDiffusionInpaintPipeline`- Não .`FluxFillPipeline`- Não .

> SD-Inpaint、SDXL-Inpaint、Flux-Fill 都使用这种9通道(或类似)输入。

### SDEdit (Meng et al., 2022)  edição gratuita

> ### SDEdit  免费编辑

Adicionar ruído à imagem fonte até um certo intermediário `t`, então, corre a cadeia inversa de `t`Não há reformulação, a escolha de começar.`t`negocia fidelidade pela liberdade criativa:

> - Dá-lhe imagens e aumenta o ruído.`t`Depois, com um novo impulso, revertem-se ao ruído.`t`O que é a liberdade de escolha?

- `t/T = 0.3`→ quase idêntico à fonte, pequenas mudanças estilísticas / 几乎与源相同,小风格变化
- `t/T = 0.6`→ edições moderadas, conserva estrutura grosseira / 中等编辑,保留粗结构
- `t/T = 0.9`→ gerado a partir de ruído próximo, preservação da fonte mínima / 从近噪声生成,最小源保留

### InstructPix2Pix (Brooks et al., 2023)

> ### InstructPix2Pix

Ajustar um modelo de difusão em`(input_image, instruction, output_image)`Em inferência, condição tanto na imagem de entrada quanto em uma instrução de texto ("fazer o pôr do sol", "add a dragon").

> Em`(输入图像, 指令, 输出图像)`O modelo de expansão é o modelo de expansão de três grupos.

### RePaint (Lugmayr et al., 2022)

> ### Recoloração

Manter um modelo de difusão incondicional padrão. Em cada passo inverso, reanalisar  saltar de volta para um estado mais barulhento ocasionalmente e regenerar. Evite artefatos de fronteira. usado quando você não tem um modelo de pintura treinado.

> 保持标准无条件扩散模型──在每反向步骤偶尔重采样跳回更噪的状态重生成──避免边界伪影──

## Construí-lo e realizei-o.
```figure
inpaint-mask-reinject
```

## Construí-lo

`code/main.py`A partir da análise de dados de 5D, cada amostra é de 5 flutuantes de um dos dois aglomerados. Na inferência, "mascaramos" 2 das 5 dimensões, injetamos a versão barulhenta para a frente dos três desenmascarados em cada passo e regeneramos apenas as dimensões enmascaradas.

### Passo 1: Dados de DDPM 5D

```python
def sample_data(rng):
    cluster = rng.choice([0, 1])
    center = [-1.0] * 5 if cluster == 0 else [1.0] * 5
    return [c + rng.gauss(0, 0.2) for c in center], cluster
```

### Passo 2: Denoiser de trem sobre os 5 dims

DDPM padrão. Saídas de rede previsão de ruído 5D para entrada de ruído 5D.

### Passo 3: na inferência, reverso consciente da máscara

```python
def inpaint_step(x_t, mask, clean_image, alpha_bars, t, rng):
    # replace unmasked dims with a freshly noised version of the clean source
    a_bar = alpha_bars[t]
    for i in range(len(x_t)):
        if not mask[i]:
            x_t[i] = math.sqrt(a_bar) * clean_image[i] + math.sqrt(1 - a_bar) * rng.gauss(0, 1)
    # ...then run the normal reverse step on x_t
```

Esta é a abordagem ingênua e funciona com dados 1D de brinquedos.

### Passo 4: pintura

O desenho exterior é o desenho com a máscara invertida: mascarar a tela nova (previamente inexistente), preencher o resto com o original.

## Encaixos.

- **Seams.**A abordagem ingênua deixa limites visíveis porque a informação de gradiente não flui através da máscara.
- **Mask leakage.**Se a região não mascarada da imagem de condicionamento for de baixa qualidade ou ruidosa, ela contamina a geração dentro da máscara.
- **CFG interacts with mask size.**Alta CFG em uma máscara pequena = parche saturado. Reduzir CFG para pequenas edições.
- **SDEdit fidelity cliff.**A partir de`t/T = 0.5`- Não .`t/T = 0.6`Pode perder a identidade do sujeito.
- **Prompt mismatch.**O aviso deve descrever a imagem inteira, não apenas o novo conteúdo. "Um gato sentado numa cadeira" não "um gato".

## Use-o com o framework implementado.

| Task / 任务 | Pipeline / 方案 |
|------|----------|
| Remove object, small mask / 移除物体 | SD-Inpaint or Flux-Fill, standard prompt |
| Replace sky / 替换天空 | SD-Inpaint + "blue sky at sunset" |
| Extend canvas / 扩展画布 | SDXL outpaint mode (8px feather) or Flux-Fill with outpaint mask |
| Regenerate hand / face / 重画手/脸 | SD-Inpaint with prompt re-describing the subject + ControlNet-Openpose |
| Change style of one region / 改变区域风格 | SDEdit at `t/T=0.5` on masked region |
| "Make it sunset" / "变成日落" | InstructPix2Pix or Flux-Kontext |
| Background replacement / 背景替换 | SAM mask → SD-Inpaint |
| Ultra-high-fidelity / 超高保真 | Flux-Fill or GPT-Image (hosted) for hardest cases |

SAM (Meta's Segment Anything, 2023) + difusão de tinta é o 2026 de remoção de fundo. SAM 2 (2024) funciona em vídeo.

> SAM(Meta's Segment Anything) + 扩散 inpaint is 2026 年的背景移除流水线──SAM 2(2024)支持视频──

## Envia-o . Produto .

Salvar`outputs/skill-editing-pipeline.md`. A Skill toma uma imagem original + descrição de edição + máscara opcional (ou prompt SAM) e as saídas: abordagem de geração de máscara, modelo base, escalas CFG (imagem + texto), modo SDEdit-t ou inpainting e lista de verificação de QA.

## Exercícios.

1. **Easy.**- Não .`code/main.py`A fracção de dimensões mascaradas varia de 0,2 a 0,8.
2. **Medium.**Implementar RePaint: a cada décima etapa inversa, salte 5 passos para trás (agrega ruído) e re-denota.
3. **Hard.**Use difusores de Face Hugging para comparar: SD 1.5 Inpaint + ControlNet-Openpose vs Flux.1-Encha em 20 tarefas de regeneração facial.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Inpainting | "Fill the hole" | Regenerate inside a mask; keep outside pixels. |
| Outpainting | "Extend the canvas" | Regenerate outside the canvas; keep inside. |
| 9-channel U-Net | "Proper inpainting model" | U-Net with `noisy \| encoded-source \| mask` as input. |
| SDEdit | "Img2img with noise level" | Noise to time `t`, denoise with new prompt. |
| InstructPix2Pix | "Text-only edits" | Fine-tuned diffusion on (image, instruction, output) triples. |
| RePaint | "No retraining" | Re-noise periodically during reverse to reduce seams. |
| SAM | "Segment Anything" | Mask generator by clicks or boxes; pairs with inpaint. |
| Flux-Kontext | "Edit with context" | Flux variant that accepts a reference image + instruction for edits. |

## Nota de produção: edit pipelines são sensíveis à latência

Os usuários que editam uma imagem esperam viagens de ida e volta de menos de 5 segundos. Uma SDXL-Inpaint de 30 passos em 10242 é de 3-4 segundos em um L4, além de geração de máscara SAM (~ 200 ms) e codificação / decodificação VAE (~ 500 ms combinados).

- **SAM-H is the slow one.**SAM-H em 10242 é ~ 200 ms; SAM-ViT-B é ~ 40 ms com perda de qualidade menor. SAM 2 (vídeo) adiciona sobrecarga temporal; não o use para edições de imagem única.
- **Skip the encode when possible.** `pipe.image_processor.preprocess(img)`Se você tiver os latentes da geração anterior (típico em UI de edição iterativa), passe-os diretamente através de `latents=...`para saltar um código de VAE.
- **Mask dilation matters for throughput too.**Uma pequena máscara significa que a maior parte do pass U-Net para a frente é desperdiçada (os pixels não mascarados são apertados de qualquer maneira). `diffusers`" `StableDiffusionInpaintPipeline`funciona a rede U-Net completa independentemente; apenas as variantes de 9 canais de tinta adequada exploram computação mascarada.
- **Flux-Kontext is the 2025 answer.**Passagem para frente única .`(source_image, instruction)`Não há máscara separada, não há barulho SDEdit. Em um H100 ele envia uma edição em ~ 1,5 s. A lição de arquitetura: derrubar os estágios.

## Mais leitura 延伸阅读

- [Lugmayr et al. (2022). RePaint: Inpainting using Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2201.09865)- pintura sem formação.
- [Meng et al. (2022). SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations](https://arxiv.org/abs/2108.01073)- SDEdit.
- [Brooks, Holynski, Efros (2023). InstructPix2Pix](https://arxiv.org/abs/2211.09800) Edição de instruções de texto.
- [Kirillov et al. (2023). Segment Anything](https://arxiv.org/abs/2304.02643)SAM, a fonte da máscara.
- [Ravi et al. (2024). SAM 2: Segment Anything in Images and Videos](https://arxiv.org/abs/2408.00714)- Vídeo SAM.
- [Hertz et al. (2022). Prompt-to-Prompt Image Editing with Cross-Attention Control](https://arxiv.org/abs/2208.01626) Edição de nível de atenção.
- [Black Forest Labs (2024). Flux.1-Fill and Flux.1-Kontext](https://blackforestlabs.ai/flux-1-tools/) 2024 ferramentas.
