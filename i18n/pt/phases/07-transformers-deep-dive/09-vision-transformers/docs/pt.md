# Transformadores de visão (ViT)

> Uma imagem é uma grade de parches, uma frase é uma grade de tokens, o mesmo transformador come as duas coisas.

> **【中文解读】**ViT Colocar imagens cortadas em patch 当作符号序列处理──理解 ViT =理解 Transformer Não se limita a NLP──CLIP、DALL-E、Sora 都基于Transformer──

**Type:** Hands-on | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro)
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

Antes de 2020, a visão por computador significava convulsões. Cada SOTA na ImageNet, COCO e benchmarks de detecção usavam uma espinha dorsal da CNN.

> Até 2020, o computador visual significava volútude.

Dosovitskiy et al. (2020)  "Uma imagem vale 16x16 palavras"  mostrou que você pode soltar as convulsões inteiramente. Cortar uma imagem em parches de tamanho fixo, projetar linearmente cada parche em um incorporado, alimentar a sequência para um codificador transformador de vainilha. Em escala suficiente (ImageNet-21k pré-treino ou maior), ViT combina ou supera os modelos baseados em ResNet.

> Dosovitskiy 等人(2020) "一张图像值 16x16 个词"证明可以完全放弃卷积──将图像切成固定大小的补丁,线性投影每补丁为嵌入,将序列送进标准变压器编码器──在足够大的下尺寸(ImageNet-21k 预训或更大),ViT可以匹配或超越基于ResNet的模型──

ViT foi o início de um padrão mais amplo em 2026: uma arquitetura, muitas modalidades. Whisper tokenizes áudio. ViT tokenizes imagens. Tokens de ação para robótica. Tokens de píxeles para vídeo. O transformador não se importa  alimentar uma sequência e ele aprende.

> ViT é o ponto de partida de uma tendência mais ampla de 2026: uma estrutura, vários modelos, um sinal de som, um sinal de som, um sinal de som, um sinal de som, um sinal de som, um sinal de movimento de um dispositivo, um sinal de som, um sinal de imagem, um sinal de som, um sinal de imagem, um sinal de som, um sinal de imagem, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, um sinal de câmbio, que pode ser usado para o computador.

Em 2026, a ViT e seus descendentes (DeiT, Swin, DINOv2, ViT-22B, SAM 3) possuem a maior parte da visão.

> Até 2026, o ViT e seus sucessores (DeiT, Swin, DINOv2, ViT-22B, SAM 3) ocuparam a maior parte do campo visual.

> **【中文解读】**O ViT tem um insight central: imagens podem ser cortadas como texto em sequências "token" e "tôquetas". 224x224 imagens podem ser cortadas em 14x14 个 16x16 parches, cada parche mostra um plano de projeção linear para inserir em um veículo, e depois enviado para o padrão de transformer.

## O conceito central.

![Image → patches → tokens → transformer](../assets/vit.svg)

### Passo 1  Aplicação

Dividir um`H × W × C`imagem em um `N × (P·P·C)`sequência de manchas planas.`224 × 224`imagem, `16 × 16`patches → 196 patches de 768 valores cada.

> - Não .`H × W × C`图像分为 `N × (P·P·C)`序列──tipo de configuração:`224 × 224`Imagens,`16 × 16`Patch → 196 个 768 值的补丁──

```
image (224, 224, 3) → 14 × 14 grid of 16x16x3 patches → 196 vectors of length 768
```

O tamanho do patch é a alavanca. Patches menores = mais tokens, melhor resolução, custo de atenção quadrática. Patches maiores = mais grosseiros, mais baratos.

> Patch: maior é o controle de parametros. Patch menor = mais tokens. melhor resolução.

### Passo 2  incorporação linear

Uma única matriz aprendida projeta cada parcela plana para `d_model`. Equivalente a uma convolução de tamanho do núcleo `P`E passo a passo .`P`Em PyTorch isto é literalmente`nn.Conv2d(C, d_model, kernel_size=P, stride=P)` uma aplicação de duas linhas.

> Uma matriz de aprendizado vai para cada parche plano`d_model`◊ igual preço a nuclear`P`、步长为 `P`É o que se passa na PyTorch.`nn.Conv2d(C, d_model, kernel_size=P, stride=P)`两行实现──

> **【拓展：Swin Transformer 的层级设计】**標準 ViT 使用固定 patch 大小和全局注意力,计算量 O(N^2)。Swin Transformer 引入层次结构:在小补丁上做局部窗口注意力,逐层合并补丁 扩大感受野──这使计算复杂变为O(N),同时保留层次特征提取的能力──Swin 在检测和分任务仍优于标准 ViT──

### Passo 3  prepend `[CLS]`token, adicionar inserções posicionais

- Prepare um aprendizagem .`[CLS]`O seu estado oculto final é a representação de imagem usada para classificação.
  Tradução do inglês:`[CLS]`token── seu estado oculto final para representação de imagens de classe
- Adicionar embutidos posicionais aprendizes (ViT-original) ou sinusoidais 2D (variantes posteriores).
  Chinese: 添加可学习的位置嵌入 ([[ViT 原始版]]) ou 正弦 2D 嵌入 ([[后续变体]])
- Em 2024+ RoPE estendido para 2D para posição, às vezes sem incorporações explícitas.
  Depois de 2024, RoPE  expandir para 2D  posição codificação, às vezes não precisa de um embedamento evidente.

### Passo 4  Encoder padrão de transformador

Estaca de blocos de`LayerNorm → Self-Attention → + → LayerNorm → MLP → +`- Identico ao BERT. Não há camadas específicas de visão.

> - Não .`LayerNorm → Self-Attention → + → LayerNorm → MLP → +`块──与BERT 完全相同──没有视觉特有的层──这是本论文的教学要点──

### Passo 5 - cabeça

Para classificação: tomar `[CLS]`estado oculto → linear → softmax. para DINOv2 ou SAM, descartar `[CLS]`, usar as inserções do parche directamente.

> Categoria: "`[CLS]` Hidden state → 线性层 → softmax── para DINOv2 ou SAM, abandonado `[CLS]`, usar patch diretamente 嵌入──

### Variantes que importaram

| Model | Year | Change |
|-------|------|--------|
| 模型 | 年份 | 变化 |
| ViT | 2020 | The original. Fixed patch size, full global attention. |
| ViT | 2020 | 原始版本。固定 patch 大小，全局注意力。 |
| DeiT | 2021 | Distillation; trainable on ImageNet-1k only. |
| DeiT | 2021 | 蒸馏；仅在 ImageNet-1k 上可训练。 |
| Swin | 2021 | Hierarchical with shifted windows. Fixed sub-quadratic cost. |
| Swin | 2021 | 层级结构，移位窗口。固定的亚二次成本。 |
| DINOv2 | 2023 | Self-supervised (no labels). Best general vision features. |
| DINOv2 | 2023 | 自监督（无标签）。最佳通用视觉特征。 |
| ViT-22B | 2023 | 22B params; scaling laws apply. |
| ViT-22B | 2023 | 22B 参数；缩放定律适用。 |
| SigLIP | 2023 | ViT + language pair, sigmoid contrastive loss. |
| SigLIP | 2023 | ViT + 语言配对，sigmoid 对比损失。 |
| SAM 3 | 2025 | Segment anything; ViT-Large + promptable mask decoder. |
| SAM 3 | 2025 | 分割一切；ViT-Large + 可提示的掩码解码器。 |

### Por que demorou um tempo?

A ViT precisa de *muitos* dados para combinar com as CNNs porque não tem nenhum dos preconceitos indutivos da CNN (invariância de tradução, localidade). Sem >100M de imagens rotuladas ou um forte pré-treino auto-supervisionado, as CNNs ainda ganham em computação combinada.

> A ViT precisa de uma grande quantidade de dados para combinar as performances da CNN, pois não tem preferências de classificação da CNN (平移不变性、局部性) ⋅ sem imagens de marcação ou treinamento de vigilância de mais de 1 bilhão de pessoas, a CNN continua a vencer em comparação com a mesma quantidade de dados. A Deit resolveu o problema em 2021 através de técnicas de vapor; a DINOv2 resolveu o problema em 2023 através de vigilância permanente.

> **【中文解读】**A ViT tem uma preferência de redução fraca: é preciso mais dados para combinar com a performance da CNN, pois a CNN tem preferências de redução de fluxo e de localização.

> **【拓展：ViT 在多模态系统中的角色】**CLIP utiliza ViT 编码图像、Transformer 编码文本, através de comparação de aprendizagem em dois modelos──DALL-E 和 Sora utiliza ViT entender imagens/vídeos, regenerar em novo conteúdo──SAM(Segmento Qualquer coisa) utiliza ViT 作为主干网络实现通用图像分化──ViT 已成为多模态 AI 的视觉基础模块──

## Construí-lo e realizei-o.
```figure
n5-patch-stream
```

## Construí-lo

Veja .`code/main.py`- Pure-stdlib patchify + linear embutida + verificações de sanidade.

> 参见 `code/main.py`◊ Patchfify de pura biblioteca padrão + 线性嵌入 + 合理性检查──无训练 任何实际规模的 ViT 都需要 PyTorch 和数小时的GPU 时间──

### Passo 1: imagem falsa

Uma imagem RGB 24 × 24 como uma lista de linhas de `(R, G, B)`Usamos 6×6 parches → 16 parches, vector de incorporação de 108D cada.

> Uma imagem RGB 24 × 24`(R, G, B)`元组的行列表形式表示──使用 6×6 patch → 16 个 patch, cada 108 维嵌入向量──

### Passo 2: Parchear

```python
def patchify(image, P):
    H = len(image)
    W = len(image[0])
    patches = []
    for i in range(0, H, P):
        for j in range(0, W, P):
            patch = []
            for di in range(P):
                for dj in range(P):
                    patch.extend(image[i + di][j + dj])
            patches.append(patch)
    return patches
```

A ordem de raster: linha-maior através da grade.

> Luz  ordem: Redes de acesso em linha de prioridade através de todas as viaturas utilizam esta ordem.

### Passo 3: inserção linear

Multiplicar cada parcela plana por um aleatório `(patch_flat_size, d_model)`Matrix. Verifique a forma de saída é `(N_patches + 1, d_model)`após a preparação `[CLS]`- Não .

> Vai colocar cada parche em um momento.`(patch_flat_size, d_model)`矩阵──验证在添加 `[CLS]`后输出形为 `(N_patches + 1, d_model)`- Não.

### Passo 4: Parâmetros de contagem para um ViT realista

Imprima a contagem de parâmetros para ViT-Base: 12 camadas, 12 cabeças, d = 768, parche = 16.

> Impressão de parâmetros da base ViT: 12 层、12 头、d=768、patch=16──与 ResNet-50(cerca de 25M)对比──ViT-Base 约86M──ViT-Large 约307M──ViT-Huge 约632M──

## Use-o com o framework implementado.

```python
from transformers import ViTImageProcessor, ViTModel
import torch
from PIL import Image

processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
model = ViTModel.from_pretrained("google/vit-base-patch16-224-in21k")

img = Image.open("cat.jpg")
inputs = processor(img, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, 197, 768): [CLS] + 196 patches
cls_emb = out[:, 0]                       # image representation
```

**DINOv2 embeddings are the 2026 default for image features.**A meta funciona para classificação, recuperação, detecção, subtítulos. Os pontos de controlo DINOv2 do Meta superam o CLIP em todas as tarefas de visão não textual.

> **DINOv2 嵌入是 2026 年图像特征的默认选择。**结骨干网络,训练一个小头── é aplicável para classificar, pesquisar, pesquisar, exibir, descrever imagens── Meta's DINOv2 检查点在每个非文本视觉任务上都优于CLIP──

**Patch-size picking.**Modelos pequenos usam 16×16 (ViT-B/16). A previsão densa (segmentação) usa 8×8 ou 14×14 (SAM, DINOv2).

> **Patch 大小选择。**小模型使用 16×16(ViT-B/16)。密集预测(分割) 使用 8×8 或 14×14(SAM、DINOv2)。 muito grande modelo usar 14×14。

## Envia-o . Produto .

Veja .`outputs/skill-vit-configurator.md`. A habilidade escolhe uma variante ViT e tamanho de parche para uma nova tarefa de visão dada a dimensão do conjunto de dados, resolução e orçamento de computação.

> 参见 `outputs/skill-vit-configurator.md` Esta habilidade  baseada em dados                                                                                                                                                                                                                                                                                                               

## Exercícios.

1. **Easy.**Corra .`code/main.py`Verifique o número de parches igual .`(H/P) * (W/P)`e a dimensão do parche plano é igual `P*P*C`- Não .
   Tradução: 运行`code/main.py` Patch de verificação`(H/P) * (W/P)`,平 patch 维度等于 `P*P*C`- Não.
2. **Medium.**Implementar inserções posicionais sinusoidais 2D  dois códigos sinusoidais independentes para `row`E ...`col`Acompanhe-os num pequeno PyTorch ViT e compare a precisão vs. inserções posicionais aprendíveis no CIFAR-10.
   Tradução do inglês: implementar 2D 正弦位置嵌入每个补丁的`row`和 `col`独立编码后拼接──在小型 PyTorch ViT 上使用,与可学习位置嵌入在CIFAR-10 上对比准确率──
3. **Hard.**Construir um ViT de 3 camadas (PyTorch), treinar em 1.000 imagens MNIST com 4×4 patches. Medir a precisão do teste. Agora adicionar DINOv2 pré-treinamento nas mesmas 1.000 imagens (simplificado: apenas treinar o codificador para prever embutidos de patches de patches mascarados). Melhora a precisão?
   中文翻译:构建 3层 ViT(PyTorch), usando patch 4×4 在 1,000 张 MNIST 图像上训练。测量测试准确率──然后添加 DINOv2 预训练(简化版:训练编码器从掩码 patch 预测 patch 嵌入)──准确率是否提升?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Patch | "The vision-transformer token" | Flat vector of pixel values for a `P × P × C` region of the image. |
| Patch | "视觉 Transformer 的 token" | 图像中 `P × P × C` 区域的像素值扁平向量。 |
| Patchify | "Chop + flatten" | Slice image into non-overlapping patches, flatten each to a vector. |
| Patchify | "切分 + 展平" | 将图像切成不重叠的 patch，每个展平为向量。 |
| `[CLS]` token | "The image summary" | Prepended learnable token; its final embedding is the image representation. |
| `[CLS]` token | "图像摘要" | 预置的可学习 token；其最终嵌入是图像表示。 |
| Inductive bias | "What the model assumes" | ViT has fewer priors than CNNs; needs more data to make up the gap. |
| 归纳偏好 | "模型假设了什么" | ViT 的先验比 CNN 少；需要更多数据来弥补差距。 |
| DINOv2 | "Self-supervised ViT" | Trained without labels using image augmentation + momentum teacher. Best general image features in 2026. |
| DINOv2 | "自监督 ViT" | 使用图像增强 + 动量教师无标签训练。2026 年最佳通用图像特征。 |
| SigLIP | "CLIP's successor" | ViT + text encoder trained with sigmoid contrastive loss; better than CLIP on matched compute. |
| SigLIP | "CLIP 的继承者" | 用 sigmoid 对比损失训练的 ViT + 文本编码器；相同计算量下优于 CLIP。 |
| Swin | "Windowed ViT" | Hierarchical ViT with local attention + shifted windows; sub-quadratic. |
| Swin | "窗口 ViT" | 带局部注意力 + 移位窗口的层级 ViT；亚二次复杂度。 |
| Register tokens | "2023 trick" | A few extra learnable tokens that soak up attention sinks; improves DINOv2 features. |
| Register tokens | "2023 技巧" | 几个额外的可学习 token，吸收注意力汇聚；改善 DINOv2 特征。 |

## Mais leitura 延伸阅读

- [Dosovitskiy et al. (2020). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929)O papel do ViT.
  Tradução do português:ViT 原始论文。
- [Touvron et al. (2021). Training data-efficient image transformers & distillation through attention](https://arxiv.org/abs/2012.12877)- Não.
  Tradução do português:DeiT 论文。
- [Liu et al. (2021). Swin Transformer: Hierarchical Vision Transformer using Shifted Windows](https://arxiv.org/abs/2103.14030)- Esvaziar.
  Tradução do português:Swin Transformer
- [Oquab et al. (2023). DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193)- DINOv2.
  Tradução do português:DINOv2
- [Darcet et al. (2023). Vision Transformers Need Registers](https://arxiv.org/abs/2309.16588) a fixação do símbolo de registro para DINOv2.
  中文翻译:DINOv2 的注册代码 修复论文。
