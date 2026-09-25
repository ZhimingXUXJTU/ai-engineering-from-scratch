# ControlNet, LoRA & Conditionação .

> O texto sozinho é um sinal de controle desajeitado. ControlNet permite que você clone um modelo de difusão pré-treinado e guiá-lo com um mapa de profundidade, esqueleto de pose, rabisco ou imagem de borda. LoRA permite que você ajuste um modelo de parâmetro 2B treinando 10 milhões de parâmetros. Juntos eles transformaram a Diffusão estável de um brinquedo no pipeline de imagem 2026 que é enviado para todas as agências.

> **【中文解读】**純文本控制太粗──ControlNet usou profundidade gráficos, gestos esqueletos,涂 ou bord bordes gráficos para gerar controle preciso; LoRA apenas treina 1000 milhões de parâmetros em um modelo de 20 bilhões de parâmetros.

> **【拓展：LoRA 是大模型时代的微调标准】**LoRA (Low Range Adaptation) não é apenas usado na geração de imagens, mas também é amplamente utilizado em LLM (LMA-LoRA) .

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 10 (LLMs from Scratch — for LoRA foundation / LoRA 基础)
**Time:** ~75 minutes

## O problema é o problema da introdução

Um prompt como "uma mulher de vestido vermelho caminhando com um cão numa rua movimentada" não dá ao modelo informações sobre *onde* o cão está, *qual é a posição* da mulher ou *a perspectiva* da rua.

>  Como "uma mulher em vermelho está num cão ocupado na rua" tal dica não diz o modelo cão está em * onde * , mulher é * que postura * , a * vista de rua * como;; texto só pode determinar cerca de 10% da informação de imagem;; o resto é visual, não pode ser descrito com letras altamente eficazes;;

O treinamento de um novo modelo condicional a partir do zero para cada sinal (posição, profundidade, inteligência, segmentação) é proibitivo. Você quer manter a espinha dorsal SDXL de 2.6B parâmetro congelada, anexar uma pequena rede lateral que lê o condicionamento e fazer com que ele empurra as características intermediárias da espinha dorsal.

> Para cada sinal (~gestão, profundidade, margem, divisão) de cabeça, o custo do novo modelo de condições é muito alto.

Você também quer ensinar o modelo novos conceitos (sua cara, seu produto, seu estilo) sem reestruturação do modelo completo. Você quer um delta 100x menor.

> Você também quer ensinar um novo conceito de modelo ((sua cara, seu produto, seu estilo) sem reestruturação do modelo inteiro. Você precisa de um aumento de 100 vezes menor.

ControlNet + LoRA + texto = kit de ferramentas do profissional de 2026. A maioria dos canais de imagem de produção de camada 2-5 LoRAs, 1-3 ControlNets e um IP-Adapter em cima de uma base SDXL / SD3 / Flux.

> ControlNet + LoRA + texto = 2026 anos do praticante toolbox。 a maioria da produção de imagens fluem em linha em SDXL/SD3/Flux  baseada em 2-5 个 LoRA、1-3 个 ControlNet 和一个 IP-Adapter。

## O conceito central.

![ControlNet clones the encoder; LoRA adds low-rank deltas](../assets/controlnet-lora.svg)

### ControlNet (Zhang et al., 2023)

*Clon* a metade do codificador da U-Net. Congelhe o original. Treine o clone para aceitar uma entrada de condicionamento extra (borda, profundidade, pose). Conecte o clone de volta ao decodificador metade do original com *convolução zero* ligações de saltos (1×1 convs iniciados em zero  começa como um no-op, aprenda um delta).

```
SD U-Net decoder:   ... ← orig_enc_features + zero_conv(controlnet_enc(condition))
```

O treinamento em 1M (prompto, condição, imagem) triplica a perda de difusão padrão.

ControlNets por modalidade são enviados como pequenos modelos laterais (~ 360 M para SDXL, ~ 70 M para SD 1.5).

```
features += weight_a * control_a(depth) + weight_b * control_b(pose)
```

### LoRA (Hu et al., 2021)

Para qualquer camada linear `W ∈ R^{d×d}`no modelo, congelar `W`e adicionar um delta de baixo grau:

```
W' = W + ΔW,  ΔW = B @ A,  A ∈ R^{r×d},  B ∈ R^{d×r}
```

com`r << d`. O ranking 4-16 é padrão para atenção, o ranking 64-128 para tons finas pesados.`2 · d · r`Em vez de`d²`. Para a atenção da SDXL com `d=640`- Não .`r=16`Por exemplo, o modelo de um adaptador de 20k em vez de 410k  uma redução de 20x.

Em inferência , pode escalar a LoRA:`W' = W + α · B @ A`- Não .`α = 0.5-1.5`Os LoRAs múltiplos se empilham adicionalmente (com a habitual advertença de que interagem de forma não linear).

### Adaptador IP (Ye et al., 2023)

Um pequeno adaptador que aceita uma *imagem* como condição (junto ao texto). Utiliza o codificador de imagem CLIP para produzir tokens de imagem, injetá-los em atenção cruzada ao lado de tokens de texto. ~ 20 MB por modelo base. Permite "gerar uma imagem no estilo desta referência" sem um LoRA.

## Matriz de composibilidade.

| Tool / 工具 | What it controls / 控制内容 | Size / 大小 | When to use / 使用时机 |
|------|------------------|------|-------------|
| ControlNet | Spatial structure (pose, depth, edges) / 空间结构 | 70-360MB | Exact layout, composition / 精确布局 |
| LoRA | Style, subject, concept / 风格、主题、概念 | 20-200MB | Personalization, style / 个性化、风格 |
| IP-Adapter | Style or subject from reference image / 参考图像风格 | 20MB | No text can describe the look / 文字无法描述 |
| Textual Inversion | Single concept as a new token / 单概念新 token | 10KB | Legacy, mostly replaced by LoRA / 旧方案 |
| DreamBooth | Full fine-tune on a subject / 完整微调 | 2-5GB | Strong identity, high compute / 强身份 |
| T2I-Adapter | Lighter ControlNet alternative / 轻量 ControlNet | 70MB | Edge devices, inference budget / 边缘设备 |

ControlNet ≈ espacial, LoRA ≈ semântico, use os dois.

> ControlNet ≈ 空间控制──LoRA ≈ 语义控制──两者配合使用──

> **【中文解读】**Método central do ControlNet: Klon SD U-Net 编码器,结原始部分,训练克隆部分接受额外条件输入(边缘、深度、姿态)。零卷积(零-convolution) inicialização assegurar o treinamento quando o ControlNet não afeta o modelo original。LoRA 在线性层上添加低排矩阵 B@A, training极少量参数(20-200MB vs 基础模型 5GB)。

> **【拓展：ControlNet + LoRA 的组合控制】**实际生产中,ControlNet(空间控制) 和 LoRA(风格/主题控制) são normalmente combinados. Por exemplo:ControlNet 控制人物姿态,LoRA 注入特定艺术风格,文本提示 描述场景内容. Este mecanismo de controle de três níveis é o padrão de configuração de serviços de imagem de 2026 de IA comercial.

## Construí-lo e realizei-o.
```figure
v4-controlnet-zero
```

## Construí-lo

`code/main.py`Simula os dois mecanismos em 1-D:

1. **LoRA.**Uma camada linear pré-treinada .`W`- Congelar. Treinar um de baixo grau.`B @ A`Tal como isso .`W + BA`- O que é que ele faz?`r = 1`É suficiente para aprender uma correcção de grau 1 perfeitamente.

2. **ControlNet-lite.**Um preditor de "base congelada" e uma "rede lateral" que lê um sinal extra. A saída da rede lateral é bloqueada por um escalar aprendizagem iniciada para zero (nossa versão de zero-conv).

### Passo 1: Matemática de LoRA

```python
def lora(W, A, B, x, alpha=1.0):
    # W is frozen; A, B are the trainable low-rank factors.
    return [W[i][j] * x[j] for i, j in ...] + alpha * (B @ (A @ x))
```

### Passo 2: Rede lateral de zero-init

```python
side_out = control_net(x, condition)
gated = gate * side_out  # gate initialized to 0
h = base(x) + gated
```

No passo 0 a saída é idêntica à base.`gate`lentamente, sem uma deriva catastrófica.

> Em primeiro passo, a saída é a mesma que o modelo básico.`gate`更新缓慢没有灾难性偏移──

## Encaixos.

- **Over-scaling LoRAs.** `α = 2`ou `α = 3`É um hack comum "faça-o mais forte" que produz resultados excessivamente estilizados / quebrados.`α ≤ 1.5`- Não .
  **LoRA 过度缩放。** `α = 2`Ou `α = 3`É comum que a prática de "fortalecer" produzir excesso de produção/perda.`α ≤ 1.5`- Não.
- **ControlNet weight conflict.**Usando uma Pose ControlNet com peso 1.0 e uma Depth ControlNet com peso 1.0 geralmente ultrapassam.
  **ControlNet 权重冲突。**权重之和 ≈ 1.0 é o valor em default da segurança.
- **LoRA on the wrong base.**Os SDXL LoRAs silenciosamente não operam no SD 1.5 porque as dimensões de atenção não coincidem.
  **LoRA 用错基础模型。**SDXL LoRA em SD 1.5 上会静默无效──
- **Textual Inversion drift.**Os tokens treinados num ponto de controlo desviam mal em outro.
  **Textual Inversion 漂移。**Em um ponto de inspecção, um sinal de treinamento se move gravemente em outro.
- **LoRA weight-merging and storage.**Você pode fazer um LoRA em pesos do modelo base para inferência mais rápida (sem adição de tempo de execução), mas você perde a capacidade de escalar `α`Mantém as duas versões.
  **LoRA 权重合并。**Pode acelerar a análise no modelo básico, mas perder a execução.`α`- A capacidade.

## Use-o com o framework implementado.

| Goal / 目标 | 2026 pipeline / 方案 |
|------|---------------|
| Reproduce a brand's art style / 复刻品牌艺术风格 | LoRA trained on ~30 curated images at rank 32 |
| Put my face in a generated image / 把我的脸放入生成图像 | DreamBooth or LoRA + IP-Adapter-FaceID |
| Specific pose + prompt / 特定姿态+提示 | ControlNet-Openpose + SDXL + text |
| Depth-aware composition / 深度感知构图 | ControlNet-Depth + SD3 |
| Reference + prompt / 参考+提示 | IP-Adapter + text |
| Exact layout / 精确布局 | ControlNet-Scribble or ControlNet-Canny |
| Background replace / 背景替换 | ControlNet-Seg + Inpainting (Lesson 09) |
| Fast 1-step style / 快速单步风格 | LCM-LoRA on SDXL-Turbo |

## Envia-o . Produto .

Salvar`outputs/skill-sd-toolkit-composer.md`. A competência assume uma tarefa (asset de entrada: prompt, imagem de referência opcional, posição opcional, profundidade opcional, rabisco opcional) e produz a pilha de ferramentas, pesos e um protocolo de semente reprodutivel.

## Exercícios.

1. **Easy / 简单.**- Não .`code/main.py`, variar o grau de LoRA `r`Em que nível o LoRA corresponde exactamente a um delta-alvo de nível 2?
   Em`code/main.py`- Não , não .`r`De 1 a 4... em que ranking é que a LoRA se encaixa em 2 objetivos?
2. **Medium / 中等.**Treinar dois LoRAs separados em duas transformações alvo. carregar-los juntos e mostrar a sua interação aditiva. Quando a interação quebra a linearidade?
   Em dois objetivos de mudança, em diferentes treinamentos, LoRA...
3. **Hard / 困难.**Use difusores para apilar: SDXL-base + Canny-ControlNet (peso 0,8) + um estilo LoRA (α 0,8) + IP-Adaptor (peso 0,6).
   Us difusores 堆叠组合, medida FID 及快速 遵循的权衡──

## Termos-chave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| ControlNet | "Spatial control" / "空间控制" | Cloned encoder + zero-conv skips; reads a conditioning image. / 克隆编码器 + 零卷积跳跃。 |
| Zero convolution | "Starts as identity" / "起始为恒等" | 1×1 conv initialized to zero; ControlNet starts as no-op. / 1×1 卷积初始化为零。 |
| LoRA | "Low-rank adapter" / "低秩适配器" | `W + B @ A`, `r << d`; 100x fewer params than a full fine-tune. / 比完整微调少 100 倍参数。 |
| rank r | "The knob" / "那个旋钮" | LoRA compression; 4-16 typical, 64+ for heavy personalization. / LoRA 压缩；典型 4-16。 |
| α | "LoRA strength" / "LoRA 强度" | Runtime scaling of the LoRA delta. / LoRA 增量的运行时缩放。 |
| IP-Adapter | "Reference image" / "参考图像" | Small image-conditioning adapter via CLIP-image tokens. / 通过 CLIP 图像 token 的小型适配器。 |
| DreamBooth | "Full subject fine-tune" / "完整主题微调" | Train the full model on ~30 images of a subject. / 在约 30 张主题图像上训练完整模型。 |
| Textual Inversion | "New token" / "新 token" | Learn a new word embedding only; legacy, mostly replaced. / 仅学习新词嵌入；旧方案。 |

## Nota de produção: LoRA swaps, ControlNet lanes, serviço multi-arrendatário

Um SaaS de texto a imagem real serve centenas de LoRAs e uma dúzia de ControlNets sobre o mesmo ponto de controle base. O problema de serviço parece muito com a LLM multi-pensionamento (a literatura de produção abrange o caso LLM sob batch contínuo e LoRAX / S-LoRA):

- **Hot-swap LoRAs, do not merge.**Fusão`W' = W + α·B·A`na base dá ~ 3-5% mais rápido por etapa de inferência, mas congela `α`Mantém os LoRAs quentes no VRAM como delta de rango; os difusores expõem`pipe.load_lora_weights()`+ `pipe.set_adapters([...], adapter_weights=[...])`O custo de troca é o `2 · d · r · num_layers`Pesos  em escala de MB, subsegundo.
- **ControlNet as a second attention lane.**O codificador clonado funciona em paralelo com a base. Dois ControlNets com peso de 1.0 cada = dois passes adicionais adicionais por passo, não um passes combinados.
- **Quantized LoRAs too.**Se você quantizar a base (ver Lição 07, Flux em 8GB), o delta LoRA também quantiza limpo para 8-bit ou 4-bit.

Flux-specific: o notebook Flux-on-8GB de Niels quantifica a base para 4 bits; empilhando um estilo LoRA (`pipe.load_lora_weights("user/style-lora")`) sobre essa base quantizada em `weight_name="pytorch_lora_weights.safetensors"`Esta é a receita que a maioria das agências SaaS vai enviar em 2026.

## Mais leitura 延伸阅读

- [Zhang, Rao, Agrawala (2023). Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543) ControlNet.
- [Hu et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) LoRA (originalmente para LLM; portos para difusão).
- [Ye et al. (2023). IP-Adapter: Text Compatible Image Prompt Adapter](https://arxiv.org/abs/2308.06721) Adaptador IP.
- [Mou et al. (2023). T2I-Adapter: Learning Adapters to Dig Out More Controllable Ability](https://arxiv.org/abs/2302.08453) alternativa mais leve ao ControlNet.
- [Ruiz et al. (2023). DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](https://arxiv.org/abs/2208.12242)- DreamBooth.
- [HuggingFace Diffusers — ControlNet / LoRA / IP-Adapter docs](https://huggingface.co/docs/diffusers/training/controlnet)- canais de referência.
