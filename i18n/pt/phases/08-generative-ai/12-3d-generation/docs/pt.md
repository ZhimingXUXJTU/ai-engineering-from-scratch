# Geração 3D.

> A 3D é a modalidade em que a alavancagem 2D-to-3D é mais forte. O avanço de 2023 foi 3D Gaussian Splating. A 2024-2026 gerativa empurra camadas de difusão multi-visão + reconstrução 3D em cima para produzir objetos e cenas a partir de um único prompt ou foto.

> **【中文解读】**3D é o modelo mais forte de 2D a 3D 桥接. Em 2023, a descoberta é 3D Gaussian Splatting. Em 2024-2026, a tendência de geração é a expansão de vários pontos de vista + 3D reconstrução sobrepostas, a partir de palavras ou fotos individuais para geração de objetos e cenários 3D.

> **【拓展：3D 生成的应用】**3D 生成用于游戏资产创建、VR/AR 内容、建筑设计、电商产品展示──DreamGaussian、TripoSR 等模型可以在秒级从文字/图片生成 3D模型──

**Type:** Learn / 学习型
**Languages:** Python
**Prerequisites:** Phase 4 (Vision / 视觉), Phase 8 · 07 (Latent Diffusion / 潜在扩散)
**Time:** ~45 minutes

## O problema é o problema da introdução

O conteúdo 3D é doloroso:

> 3D content é difícil:

- **Representation.**Mestres, nuvens pontuais, grades de voxel, campos de distância assinados (SDFs), campos de radiação neural (NeRFs), Gaussians 3D. Cada um tem trade-offs.
  **表示方式。**O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é?
- **Data scarcity.**A ImageNet tem 14 milhões de imagens. O maior conjunto de dados 3D limpo (Objaverse-XL, 2023) tem ~ 10 milhões de objetos, a qualidade mais baixa.
  **数据稀缺。**ImageNet tem 14 milhões de imagens.
- **Memory.**Uma grade de 5123 voxel é de 128M voxels; uma cena útil NeRF precisa de 1M amostras / raios.
  **内存。**5123 corpo de corpo é de 1.28 bilhões de corpo de corpo.
- **Supervision.**Para uma imagem 2D, temos os pixels. Para 3D, normalmente temos um punhado de visualizações 2D e temos que subir para 3D.
  **监督。**2D imagens têm imagens. 3D geralmente apenas uma pequena quantidade de 2D imagens.

A pilha 2026 separa os dois problemas. Primeiro, gerar * 2D imagens de visualização múltipla * com um modelo de difusão. segundo, encaixar uma representação * 3D * (geralmente Gaussian splatting) para essas imagens.

> O programa de 2026 é dividido em dois passos: primeiro usar um modelo de expansão para gerar imagens de 2D, mais visões de imagens, mais uma vez usar 3D para mostrar a sua capacidade de expansão.

> **【中文解读】**Desafio central da produção 3D: mostrar o modo de produção de diferentes formas de produção de imagens em 2D. O principal esquema de 2026 é de duas fases: primeiro usar um modelo de expansão para gerar imagens em 2D, reutilizar 3D.

> **【拓展：3D Gaussian Splatting 的革命性影响】**3DGS(2023) substituir NeRF  tornar-se o principal método de reconstrução 3D. Ele usa milhões de 3D High 球体 para expressar cenários, 染速度快 100 倍以上,质量相当或更优──结合多视角扩散模型,3DGS fazer "produção de textos/imágenes de interagem 3D 场景" tornar-se possível, em jogos、VR/AR、 construção visualização tem uma enorme aplicação.

## O conceito central.

![3D generation: multi-view diffusion + 3D reconstruction](../assets/3d-generation.svg)

### Representação: 3D Gaussian Splatting (Kerbl et al., 2023)

Representa uma cena como uma nuvem de Gaussianos 3D ~ 1M. Cada um tem 59 parâmetros: posição (3), covariância (6, ou quaternion 4 + escala 3), opacidade (1), cor esférica-harmónica (48 em grau 3, 3 em grau 0).

Rendering = projeção + composição alfa. Rapido (~ 100 fps em 1080p em um 4090). Diferenciável. Adaptação por descida de gradiente contra fotos de verdade no solo. Uma cena se encaixa em 5-30 minutos em uma GPU de consumo.

Dois inovações para 2023-2024:
- **Generative Gaussian splats.**Modelos como LGM, LRM, InstantMesh prevêem uma nuvem gaussiana diretamente a partir de uma ou algumas imagens.
- **4D Gaussian Splatting.**Gaussians com ofertas por quadro para cenas dinâmicas.

### Difusão de visualização múltipla

Tune-se em forma uma imagem pré-treinada modelo de difusão para gerar múltiplas visualizações consistentes do mesmo objeto a partir de um texto de prompt ou de uma única imagem. Zero123 (Liu et al., 2023), MVDream (Shi et al., 2023), SV3D (Estabilidade, 2024), CAT3D (Google, 2024). Geralmente emitir 4-16 visualizações ao redor do objeto, elevado para 3D através de Gaussian splatting ou NeRF.

### Tubos de texto para 3D

| Model | Input | Output | Time |
|-------|-------|--------|------|
| DreamFusion (2022) | text | NeRF via SDS | ~1 hour per asset |
| Magic3D | text | mesh + texture | ~40 min |
| Shap-E (OpenAI, 2023) | text | implicit 3D | ~1 min |
| SJC / ProlificDreamer | text | NeRF / mesh | ~30 min |
| LRM (Meta, 2023) | image | triplane | ~5 s |
| InstantMesh (2024) | image | mesh | ~10 s |
| SV3D (Stability, 2024) | image | novel views | ~2 min |
| CAT3D (Google, 2024) | 1-64 images | 3D NeRF | ~1 min |
| TripoSR (2024) | image | mesh | ~1 s |
| Meshy 4 (2025) | text + image | PBR mesh | ~30 s |
| Rodin Gen-1.5 (2025) | text + image | PBR mesh | ~60 s |
| Tencent Hunyuan3D 2.0 (2025) | image | mesh | ~30 s |

2025-2026 direção: modelos diretos de texto para rede com materiais PBR adequados para motores de jogo.

### NeRF (para contexto)

Campo de Radiância Neural (Mildenhall et al., 2020).`(x, y, z, view direction)`e de saída `(color, density)`- Render através da integração ao longo dos raios. Superou a síntese de visão nova baseada em malha em qualidade, mas é 100-1000 vezes mais lenta de render.

## Construí-lo e realizei-o.
```figure
v4-3d-multiview
```

## Construí-lo

`code/main.py`Implementa um jogo 2D "splating gaussiano" fit: representar uma imagem de alvo sintética (um gradiente liso) como uma soma de espaços gaussianos 2D. Otimizar posições, cores e covarianças por descida de gradiente para combinar com o alvo. Você vê as duas operações principais: render para frente (splat + alfa-composto) e fit por descida de gradiente.

### Passo 1: 2D Gaussian splat

```python
def gaussian_at(x, y, gaussian):
    px, py = gaussian["pos"]
    sigma = gaussian["sigma"]
    d2 = (x - px) ** 2 + (y - py) ** 2
    return math.exp(-d2 / (2 * sigma * sigma))
```

### Passo 2: renderização por soma de pontos

```python
def render(image_size, gaussians):
    img = [[0.0] * image_size for _ in range(image_size)]
    for g in gaussians:
        for y in range(image_size):
            for x in range(image_size):
                img[y][x] += g["color"] * gaussian_at(x, y, g)
    return img
```

A real espalhação gaussiana 3D classifica gaussianos por profundidade e por compostos alfa em ordem.

### Passo 3: ajustamento por descida de gradiente

```python
for step in range(steps):
    pred = render(size, gaussians)
    loss = mse(pred, target)
    gradients = compute_grads(pred, target, gaussians)
    update(gaussians, gradients, lr)
```

## Encaixos.

- **View inconsistency.**Se você gerar 4 visualizações de forma independente e eles discordam sobre a estrutura do objeto, o ajuste 3D é borroso.
- **Back-side hallucination.**A imagem única → 3D tem que inventar o lado invisível.
- **Gaussian splat explosion.**O treinamento sem restrições cresce para 10 milhões de espaços e superpontos.
- **Topology issues.**As malhas de campos implícitos (SDFs) têm muitas vezes buracos ou auto-interseções.
- **License of training data.**O Objaverse tem licenças mistas; uso comercial varia por modelo.

## Use-o com o framework implementado.

| Task / 任务 | 2026 pick / 2026 选择 |
|------|-----------|
| Scene reconstruction from photos / 照片场景重建 | Gaussian splatting (3DGS, Gsplat, Scaniverse) |
| Text-to-3D object for games / 文本生成游戏 3D | Meshy 4 or Rodin Gen-1.5 (PBR output) |
| Image-to-3D / 图像生成 3D | Hunyuan3D 2.0, TripoSR, InstantMesh |
| Novel-view synthesis from few images / 少样本新视角 | CAT3D, SV3D |
| Dynamic scene reconstruction / 动态场景重建 | 4D Gaussian Splatting |
| Avatar / clothed human / 虚拟人/穿衣人体 | Gaussian Avatar, HUGS |
| Research / SOTA / 研究 | Whatever dropped last week / 上周发布的任何模型 |

Para a produção de transporte 3D em um jogo ou pipeline de comércio eletrônico: Meshy 4 ou Rodin Gen-1.5 de saída de malhas PBR que vão diretamente para Unity / Unreal.

> Em jogo ou em linha de câmbio, 3D: Meshy 4 ou Rodin Gen-1.5 输出可直接用于 Unity/Unreal 的 PBR 网格──

## Envia-o . Produto .

Salvar`outputs/skill-3d-pipeline.md`. A competência assume um resumo 3D (entrada: texto / uma imagem / poucas imagens; saída: malha / espartilha / NeRF; uso: renderização / jogo / VR) e saídas: pipeline (difusão de múltiplas visualizações + ajuste ou modelo de malha direta), modelo base, orçamento de iteração, pós-processamento de topologia, canais de material necessários.

## Exercícios.

1. **Easy.**Corra .`code/main.py`Relatório final MSE vs. alvo.
2. **Medium.**Extender para Gaussianos de cor (RGB). Confirmar reconstrução coincide com o padrão de cor alvo.
3. **Hard.**Usando gsplat ou Nerfstudio, reconstruir um objeto real a partir de uma captura de 50 fotos.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 3D Gaussian Splatting | "3DGS" | Scene as a cloud of 3D Gaussians; differentiable alpha-composite render. |
| NeRF | "Neural radiance field" | MLP that outputs color + density at a 3D point; render by ray integration. |
| Triplane | "Three 2-D planes" | Factor 3D into three 2-D axis-aligned feature grids; cheaper than volumetric. |
| SDS | "Score distillation sampling" | Train 3D model by using 2D-diffusion score as pseudo-gradient. |
| Multi-view diffusion | "Many views at once" | Diffusion model that outputs a batch of consistent camera views. |
| PBR | "Physically-based rendering" | Material with albedo, roughness, metallic, normal channels. |
| Densification | "Grow splats" | 3DGS training heuristic: split / clone splats in high-gradient regions. |

## Nota de produção: 3D ainda não tem substrato compartilhado

Ao contrário da imagem (difusão latente + DiT) e do vídeo (diT espacial-temporal), a 3D não tem um único tempo de execução dominante em 2026.

- **NeRF / triplane.**A inferência é a marcação de raios + um MLP para a frente por amostra. Um renderização 5122 requer milhões de MLP para a frente. Batch as amostras de raios agressivamente; SDPA/xformers aplica.
- **Multi-view diffusion + LRM reconstruction.**O estágio 1 (difuso de visualização múltipla) é um servidor de difusão, assim como a lição 07. O estágio 2 (transformador LRM) é um passo para frente de um tiro sobre as visualizações.
- **SDS / DreamFusion.**Otimizar por ativo, não inferir, criar empregos, não pedir manipuladores.

Para a maioria dos produtos de 2026, a resposta correta é "exercer um modelo de difusão de visualização múltipla a pedido, reconstruir para 3DGS de forma assíncrona, servir o 3DGS para visualização em tempo real". Isso divide a carga de trabalho limpa entre um servidor de interferência GPU (rápido) e um optimizador offline (lento).

## Mais leitura 延伸阅读

- [Mildenhall et al. (2020). NeRF: Representing Scenes as Neural Radiance Fields](https://arxiv.org/abs/2003.08934)- NeRF.
- [Kerbl et al. (2023). 3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://arxiv.org/abs/2308.04079)- 3DGS.
- [Poole et al. (2022). DreamFusion: Text-to-3D using 2D Diffusion](https://arxiv.org/abs/2209.14988) SDS.
- [Liu et al. (2023). Zero-1-to-3: Zero-shot One Image to 3D Object](https://arxiv.org/abs/2303.11328)- Zero123.
- [Shi et al. (2023). MVDream](https://arxiv.org/abs/2308.16512) Difusão de visualização múltipla.
- [Hong et al. (2023). LRM: Large Reconstruction Model for Single Image to 3D](https://arxiv.org/abs/2311.04400) LRM.
- [Gao et al. (2024). CAT3D: Create Anything in 3D with Multi-View Diffusion Models](https://arxiv.org/abs/2405.10314)- CAT3D.
- [Stability AI (2024). Stable Video 3D (SV3D)](https://stability.ai/research/sv3d)- SV3D.
