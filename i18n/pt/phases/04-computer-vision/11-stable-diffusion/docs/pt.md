# Estabilidade de difusão  Arquitetura e ajuste perfeito  Estabilidade de difusão  Arquitetura e micro-modução

> A Diffusão Estavel é um DDPM que funciona no espaço latente de um VAE pré-treinado, condicionado ao texto através da atenção cruzada, amostrado com um solvente ODE determinista rápido e orientado por orientação sem classificador.

> **【中文解读】**A difusão estável é um modelo de difusão que opera no espaço potencial do VAE, através de um intercâmbio de atenção (transação) para aceitar condições de texto, usando um ODE de rápida determinação (exemplos de busca de soluções), e através de orientação sem classificador (guia livre de classificadores) para controlar a qualidade de produção.

> **【拓展：Stable Diffusion 生态】**Estabilidade de difusão  Derivado de LoRA ️Light Quantity ️ControlNet ️Control Gestão/Reijo ️IP-Adapter ️Image Tip ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

**Type:** Learn + Use | **类型:** 学习 + 应用
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 10 (Diffusion), Phase 7 Lesson 02 (Self-Attention) | **前置知识:** Phase 4 Lesson 10（扩散模型），Phase 7 Lesson 02（自注意力）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Rastrear as cinco peças de um pipeline de difusão estável: VAE, codificador de texto, U-Net, agendador, verificador de segurança  e o que cada um deles realmente faz
- Explicar a difusão latente e por que o treinamento num espaço latente 4x64x64 (em vez de uma imagem 3x512x512) reduz a computação em 48x sem perda de qualidade
- Utilização`diffusers`gerar imagens, executar imagem-para-imagem, inpainting e geração guiada pelo ControlNet
- Ação de sintonia precisa Difusão estável com LoRA em um pequeno conjunto de dados personalizado e carga o adaptador LoRA na inferência

> **【中文解读】**O objetivo do aprendizado é listar as capacidades centrais que devem ser adquiridas após a conclusão do curso.


## O problema é o problema da introdução

Treinar um DDPM diretamente em imagens RGB 512x512 é caro. Cada passo de treinamento retrocede através de uma U-Net que vê valores de entrada 3x512x512 = 786,432, e a amostragem leva 50+ passes para a frente através dessa mesma U-Net. No nível de qualidade da Stable Diffusion 1.5 (lançado em 2022), a difusão de espaço de pixels precisaria de aproximadamente 256 meses de treinamento de GPU e 10-30 segundos por imagem em uma GPU de consumo.

>  Direta em 512x512 RGB  imagens  treinamento DDPM  muito caro. Cada passo de treinamento deve passar por um ver 3x512x512 = 786,432                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

O truque que fez o texto-imagem de peso aberto prático foi**latent diffusion**(Rombach et al., CVPR 2022). Treinar um VAE que mapeia uma imagem 3x512x512 para um tensor latente 4x64x64 e de volta, então fazer a difusão nesse espaço latente.`(3*512*512)/(4*64*64) = 48x`A amostragem cai de dezenas de segundos para menos de dois segundos na mesma GPU.

> Para tornar o livre poder de gravação de texto para imagens práticas é**潜空间扩散**(Rombach 等,CVPR 2022)  Treinar um VAE vai 3x512x512 图像映射到4x64x64 潜张量并恢复, então fazer dilatação em que potencial espaço 计算量降低 `(3*512*512)/(4*64*64) = 48x`Na mesma GPU, a escala de imagem foi reduzida de 10 segundos para 2 segundos.

Quase todos os modelos modernos de geração de imagens  SDXL, SD3, FLUX, HunyuanDiT, Wan-Video  são um modelo de difusão latente com variações no autoencoder, no denoizador (U-Net ou DiT) e no condicionamento de texto.

> Quase todos os modelos de gerenciamento de imagens modernos são diferentes em sistemas de codificação automática, em redes ou em dispositivos de DiT e em termos de texto.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


### O oleoduto

```mermaid
flowchart LR
    TXT["Text prompt"] --> TE["Text encoder<br/>(CLIP-L or T5)"]
    TE --> CT["Text<br/>embedding"]

    NOISE["Noise<br/>4x64x64"] --> UNET["UNet<br/>(denoiser with<br/>cross-attention<br/>to text)"]
    CT --> UNET

    UNET --> SCHED["Scheduler<br/>(DPM-Solver++,<br/>Euler)"]
    SCHED --> LATENT["Clean latent<br/>4x64x64"]
    LATENT --> VAE["VAE decoder"]
    VAE --> IMG["512x512<br/>RGB image"]

    style TE fill:#dbeafe,stroke:#2563eb
    style UNET fill:#fef3c7,stroke:#d97706
    style SCHED fill:#fecaca,stroke:#dc2626
    style IMG fill:#dcfce7,stroke:#16a34a
```

- **VAE**Encoder transforma imagem em latentes (usado para img2img e treinamento).
  O sistema de codificação de imagens em imagens de imagem em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em imagens em.
- **Text encoder** Encoder de texto CLIP (SD 1.x/2.x), CLIP-L + CLIP-G (SDXL) ou T5-XXL (SD3/FLUX). Produz uma sequência de embeddings de tokens.
  Tradução do inglês: 文本编码器CLIP 文本编码器(SD 1.x/2.x)、CLIP-L + CLIP-G(SDXL) ou T5-XXL(SD3/FLUX)。产生一系列代币 嵌入──
- **U-Net**O denotador possui camadas de atenção cruzada que se insistem desde os latentes até ao texto incorporado em todos os níveis de resolução.
  U-Net去噪器──包含交叉注意力层, em cada nível de resolução, de um nível de variação de potencial关订本嵌入──
- **Scheduler**O algoritmo de amostragem (DDIM, Euler, DPM-Solver++).
  Tradução do inglês para tradução livre:调度器采样算法(DDIM、Euler、DPM-Solver++) ・・・选择 sigma 值,将预测的噪音混合回潜变量──
- **Safety checker** Filtro opcional de conteúdo ilegal NSFW na imagem de saída.
  Tradução do inglês para tradução livre: segurança checkmachiner可选的NSFW / 违规内容过器,作用于输出图像──

### Orientação sem classificador (CFG)

Aprenda a condicionar o texto simples `epsilon_theta(x_t, t, c)`Para cada pedido .`c`O CFG treina a mesma rede com `c`A conclusão é que, em termos de volume, a quantidade de ruído que se produz em um ambiente de alta pressão, em que a quantidade de ruído é reduzida, é de 10% (substituída por uma inserção vazia), dando um único modelo que prevê tanto o ruído condicional quanto o ruído incondicional.

> 纯文本条件化学习 `epsilon_theta(x_t, t, c)`Para cada palavra de sugestão`c` CFG  Treinamento com uma rede  10% do tempo perdido `c`(substituição por embutidos em espaço), obtém um modelo de simultaneamente previsão de ruído condicional e ruído incondicional:

```
eps = eps_uncond + w * (eps_cond - eps_uncond)
```

`w`É a escala de orientação. `w=0`é incondicional,`w=1`é condicional,`w>1`O SD é o padrão de configuração de um sistema de configuração de um sistema de configuração de um sistema de configuração de um sistema de configuração de configuração de um sistema de configuração de configuração de um sistema de configuração de configuração de configuração de um sistema de configuração de configuração de configuração de configuração de configuração de um sistema de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de configuração de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de.`w=7.5`- Não .

> `w`É a medida do que é.`w=0`Não há condições de gerar.`w=1`É normal que as condições sejam geradas.`w>1`Em sacrifício da diversidade em troca de preços, impulsionar a produção mais "conforme a proposta"`w=7.5`- Não.

O CFG é a razão pela qual o texto-a-imagem funciona na qualidade da produção. Sem ele, os pedidos de desvio da saída são fracos; com ele, os pedidos dominam.

> O CFG é a razão pela qual o texto até imagens podem trabalhar em qualidade de produção.

### Geometria do espaço latente

A latença de 4 canais do VAE não é apenas uma imagem comprimida. É um manifold onde a aritmética corresponde aproximadamente a edições semânticas (ingeniería de rapidez + interpolação ambos vivem aqui), e onde a U-Net de difusão foi treinada para gastar todo o seu orçamento de modelagem. A decodificação de uma latente aleatória 4x64x64 não produz uma imagem aleatória.

> O VAE 4 通道潜量量 não é apenas uma imagem compactada. É um fluxo, com o qual o cálculo operacional ocorre aqui, mas também é um lugar de treinamento da U-Net para a construção de um orçamento.

Duas consequências:

> 两个后果:

1. **Img2img**= codificar imagem para latente, adicionar ruído parcial, executar o denoiser, decodificar. A estrutura da imagem sobrevive porque a codificação é quase invertível; o conteúdo muda com base no prompt.
   Tradução:**Img2img**= Codificar imagens para variações, adicionar parte do ruído, executar para o ruído, descodear;
2. **Inpainting**= igual a img2img mas o denotador apenas actualiza regiões mascaradas; as regiões não mascaradas são mantidas no latente codificado.
   Tradução:**Inpainting**= Igual com img2img, mas o dispositivo de ruído apenas atualiza a zona de encoberta; a zona não encoberta mantém-se em constante constante de variação.

### A arquitetura da U-Net

A SD U-Net é uma grande versão da TinyUNet da lição 10 com três adições:

> A U-Net do SD é a 10a versão da TinyUNet, que adiciona três componentes:

- **Transformer blocks**Em cada resolução espacial, contendo auto-atenção + atenção cruzada ao texto incorporado.
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês
- **Time embedding**através de MLP em codificação sinusoidal.
  Tradução do inglês:MLP 处理正弦编码的时间嵌入.
- **Skip connections**entre codificador e decodificador em resoluções correspondentes.
  Tradução do inglês:编码器和码器在匹配分辨率之间跳跃连接──

Parâmetros totais em SD 1,5: ~860M. SDXL: ~2.6B. FLUX: ~12B. O salto em parâmetros é principalmente em camadas de atenção.

> SD 1.5                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

### Ajuste fino do LoRA

O ajuste fino completo da Diffusion estável requer 20+ GB de VRAM e atualiza 860M parâmetros. LoRA (Low-Rank Adaptation) mantém o modelo base congelado e injeta pequenas matrizes de decomposição de nível nas camadas de atenção. Um adaptador LoRA para SD é tipicamente de 10-50 MB, treina em 10-60 minutos em uma única GPU de consumo e carrega no tempo de inferência como uma modificação drop-in.

> O LoRA 适配器 de SD geralmente é de 10 a 50 MB, em um único GPU de consumo de 10 a 60 minutos, quando recomendado como um modo de fazer modificações imediatas.

```
Original: W_q : (d_in, d_out)   frozen
LoRA:     W_q + alpha * (A @ B)   where A : (d_in, r), B : (r, d_out)

r is typically 4-32.
```

A LoRA é a forma como quase todas as comunidades de música é distribuída.

> A LoRA é a forma de distribuição de quase todas as comunidades.

### Os agendamentos que verão

- **DDIM**Determinista, 50 passos, simples.
  Tradução do inglês:DDIM确定性, aproximadamente 50 步,简单――
- **Euler ancestral** Estocástico, 30-50 passos, amostras ligeiramente mais criativas.
  O que é que é o "predecessor" de Euler?
- **DPM-Solver++ 2M Karras** Determinista, 20-30 passos, padrão de produção.
  中文翻译:DPM-Solver++ 2M Karras确定性,20-30 步,生产环境默认选择──
- **LCM / TCD / Turbo** modelos de consistência e variantes destiladas; 1-4 etapas ao custo de alguma qualidade.
  中文翻译:LCM / TCD / Turbo一致性模型和蒸变体;1-4 步,代价是一些质量损失──

A troca de calendários é uma alteração de linha única em `diffusers`E às vezes corrige os problemas de amostra sem qualquer reformulação.

> Em`diffusers`O modificador de câmbio de câmbio requer apenas uma linha de código, às vezes não é necessário re-treinar para poder reparar o problema de amostra.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

> **【拓展：工业部署中的视觉系统】**No implementar industrial real, o modelo visual precisa considerar a possibilidade de atrasos, modelos de tamanho, dispositivos de margem, etc. TensorRT, ONNX Runtime, OpenVINO são ferramentas de aceleração de cálculo de uso comum.

> **【拓展：数据标注与质量】** Visual task's effect highly depends on label data quality──Label Studio、CVAT is the mainstream marking tool──In industrial scenarios, proactive learning(Active Learning) pode reduzir o custo de marcação: modelo contra um pedido de amostra não definido marcação artificial, identidade de amostra auto-marcação──




## Construí-lo e realizei-o.
```figure
cv3-latent-compression
```

## Construí-lo

Esta lição usa`diffusers`As peças que você precisaria reconstruir (VAE, codificador de texto, U-Net, agendador) são tópicos de suas próprias lições; aqui o objetivo é a fluência com a API de produção.

> 本课端到端使用 `diffusers`Em vez de criar uma rede de componentes, você precisa de reconstruir os componentes (VAE, Text Text Text Coder, U-Net,调度器) de cada um dos cursos; o objetivo é ter um conhecimento profundo da produção de API.

### Passo 1: texto para imagem

```python
import torch
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
).to("cuda")

image = pipe(
    prompt="a dog riding a skateboard in tokyo, studio ghibli style",
    guidance_scale=7.5,
    num_inference_steps=25,
    generator=torch.Generator("cuda").manual_seed(42),
).images[0]
image.save("dog.png")
```

`float16`reduz a metade a VRAM sem perda visível de qualidade. `num_inference_steps=25`com a correspondência padrão DPM-Solver++ `num_inference_steps=50`com DDIM.

> `float16`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `num_inference_steps=25`É muito mais eficaz que usar DDIM.`num_inference_steps=50`- Não.

### Passo 2: Troca o cronograma

```python
from diffusers import DPMSolverMultistepScheduler, EulerAncestralDiscreteScheduler

pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
```

O estado do cronograma está descoplado dos pesos da U-Net.

> 调度器状态与 U-Net 权重解── Você pode treinar no DDPM, usando qualquer调度器采样──

### Passo 3: Imagem a imagem

```python
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image

img2img = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
).to("cuda")

init_image = Image.open("dog.png").convert("RGB").resize((512, 512))
out = img2img(
    prompt="a dog riding a skateboard, oil painting",
    image=init_image,
    strength=0.6,
    guidance_scale=7.5,
).images[0]
```

`strength`O nível de ruído é o que deve ser adicionado antes de denosar (0,0 = inalterado, 1,0 = regeneração completa).

> `strength`控制去噪音前添加多少噪音(0.0 = 不变,1.0 = 完全重新生成) ⋅0.5-0.7 é o padrão de escala de mudança

### Passo 4: Pintura

```python
from diffusers import StableDiffusionInpaintPipeline

inpaint = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16,
).to("cuda")

image = Image.open("dog.png").convert("RGB").resize((512, 512))
mask = Image.open("dog_mask.png").convert("L").resize((512, 512))

out = inpaint(
    prompt="a cat",
    image=image,
    mask_image=mask,
    guidance_scale=7.5,
).images[0]
```

Os pixels brancos da máscara são a área para regeneração.

> O quadro branco é uma área que precisa ser reproduzida, o quadro negro é mantido.

### Passo 5: Carregamento de LoRA

```python
pipe.load_lora_weights("sayakpaul/sd-lora-ghibli")
pipe.fuse_lora(lora_scale=0.8)

image = pipe(prompt="a village square in ghibli style").images[0]
```

`lora_scale`- 0,0 = sem efeito, 1,0 = efeito total. `fuse_lora`O adaptador é colocado nos pesos para a velocidade, mas impede a troca.`pipe.unfuse_lora()`antes de carregar um adaptador diferente.

> `lora_scale`Control强度;0.0 = 无效,1.0 = 完全效果──`fuse_lora`A partir de agora, o adaptador será transformado em um peso de peso para aumentar a velocidade, mas impedirá a mudança.`pipe.unfuse_lora()`- Não.

### Passo 6: Formação do LoRA (esquema)

A real formação da LoRA vive em `peft`ou `diffusers.training`O esboço:

> O verdadeiro treinamento de Loura está`peft`Ou `diffusers.training`O que se segue:

```python
# Pseudocode
for step, batch in enumerate(dataloader):
    images, prompts = batch
    latents = vae.encode(images).latent_dist.sample() * 0.18215

    t = torch.randint(0, num_train_timesteps, (batch_size,))
    noise = torch.randn_like(latents)
    noisy_latents = scheduler.add_noise(latents, noise, t)

    text_emb = text_encoder(tokenizer(prompts))

    pred_noise = unet(noisy_latents, t, text_emb)  # LoRA weights injected here

    loss = F.mse_loss(pred_noise, noise)
    loss.backward()
    optimizer.step()
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


Apenas as matrizes LoRA recebem gradiente; a base U-Net, VAE e o codificador de texto são congelados. Com um tamanho de lote de 1 e ponto de verificação de gradiente, isso se encaixa em 8 GB de VRAM.

>                                                                                                                                                                                                                                                               




> **【拓展：视觉模型的持续学习】**Em um ambiente de produção, o modelo visual precisa se adaptar constantemente a novos dados. Isto é especialmente importante na condução automática e no controle de qualidade industrial.

## Use-o com o framework implementado.

Na produção, as decisões que realmente tomas:

- **Model family**: SD 1.5 para as melodias de comunidade de código aberto, SDXL para maior fidelidade, SD3 / FLUX para o estado da arte e requisitos de licenciamento rigorosos.
- **Scheduler**: DPM-Solver++ 2M Karras para 20-30 passos, LCM-LoRA quando a latência é inferior a 1s.
- **Precision**- Não .`float16`em 4080/4090, `bfloat16`na A100 e mais recente, `int8`(via `bitsandbytes`ou `compel`) quando o VRAM estiver apertado.
- **Conditioning**: funciona com texto simples; para um controlo mais forte, adicione o ControlNet (canny, depth, pose) no topo do pipeline base.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


Para a geração de lote, `AUTO1111`- Não .`ComfyUI`são as ferramentas comunitárias; para as APIs de produção, `diffusers`+ `accelerate`ou `optimum-nvidia`com a compilação TensorRT.



## Envia-o . Produto .

Esta lição produz:

- `outputs/prompt-sd-pipeline-planner.md` um prompt que escolhe SD 1.5 / SDXL / SD3 / FLUX mais cronógrafo e precisão dado um orçamento de latência, objetivo de fidelidade e restrição de licenciamento.
- `outputs/skill-lora-training-setup.md` uma habilidade que escreve uma configuração completa de treinamento do LoRA para um conjunto de dados personalizado, incluindo legendas, classificação, tamanho de lote e taxa de aprendizagem.

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 


## Exercícios.

1. **(Easy)**Gerenar o mesmo prompt com `guidance_scale`em `[1, 3, 5, 7.5, 10, 15]`Descreva como a imagem muda.
2. **(Medium)**Tome qualquer fotografia real, passe-a.`StableDiffusionImg2ImgPipeline`- Não .`strength`em `[0.2, 0.4, 0.6, 0.8, 1.0]`Qual força preserva a composição enquanto muda de estilo?
3. **(Hard)**Treinar um LoRA em 10-20 imagens de um único sujeito (um animal de estimação, um logotipo, um personagem) e gerar cenas novas com esse sujeito nelas.

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Latent diffusion | "Diffuse in latents" | Run the entire DDPM in the VAE latent space (4x64x64) instead of pixel space (3x512x512); 48x compute saving |
| VAE scale factor | "0.18215" | Constant that rescales the VAE's raw latent to roughly unit variance; hardcoded in every SD pipeline |
| Classifier-free guidance | "CFG" | Mix conditional and unconditional noise predictions; the single most impactful inference knob |
| Scheduler | "Sampler" | The algorithm that turns noise + model predictions into a denoised latent trajectory |
| LoRA | "Low-rank adapter" | Small rank-decomposition matrices that fine-tune attention layers without touching base weights |
| Cross-attention | "Text-image attention" | Attention from latent tokens to text tokens; injects prompt information at every U-Net level |
| ControlNet | "Structure conditioning" | A separately-trained adapter that steers SD with an extra input (canny, depth, pose, segmentation) |
| DPM-Solver++ | "The default scheduler" | Second-order deterministic ODE solver; best quality at low step counts (20-30) in 2026 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [High-Resolution Image Synthesis with Latent Diffusion (Rombach et al., 2022)](https://arxiv.org/abs/2112.10752) o papel de difusão estável; inclui todas as ablações que justificam o desenho
- [Classifier-Free Diffusion Guidance (Ho & Salimans, 2022)](https://arxiv.org/abs/2207.12598) O papel CFG
- [LoRA: Low-Rank Adaptation of Large Language Models (Hu et al., 2021)](https://arxiv.org/abs/2106.09685)O LoRA foi o primeiro a ser desenvolvido em PNL; foi transferido para SD sem quase nenhuma alteração.
- [diffusers documentation](https://huggingface.co/docs/diffusers) a referência para cada oleoduto SD/SDXL/SD3/FLUX
