# StyleGAN  StyleGAN  风格生成对抗网络

> A maioria dos geradores agita .`z`O StyleGAN divide-o: primeiro mapa`z`para um intermediário `w`, depois * injectar * `w`Essa única mudança desenroou o espaço latente e fez com que os rostos fotorrealistas fossem um problema resolvido durante sete anos consecutivos.

> **【中文解读】**O StyleGAN irá ocultar a variação z antes de ser mapeada para o espaço intermediário w, repassando AdaIN em cada nível de resolução injectado w, alcançando o controle independente sobre a geração de imagens em diferentes níveis de graus grosseiros/pecílios. Essa mudança abriu o espaço oculto, tornando a geração de faces realistas um problema resolvido por até sete anos.

> **【拓展：StyleGAN 的应用】**StyleGAN  amplamente utilizado para gerar rostos humanos (thispersondoesnotexist.com) 、虚拟人物创建、艺术创作──其 技术可以混合不同人脸的粗细特征──

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 03 (GANs), Phase 4 · 08 (Normalization / 归一化), Phase 3 · 07 (CNNs)
**Time:** ~45 minutes

## O problema é o problema da introdução

Um mapa DCGAN `z`A questão é:`z`Controlar tudo  pose, iluminação, identidade, fundo  entrelaçados.`z`Não se pode perguntar ao modelo "a mesma pessoa, diferentes posturas" porque a representação não faz tal factor.

> DCGAN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `z`映射为图像──`z`Controlar tudo, a forma, a luz, a identidade, o contexto, tudo em conjunto.`z`Não podes exigir um modelo "a mesma pessoa, diferentes posturas", porque não há assim a desintegração.

Karras et al. (2019, NVIDIA) propôs: parar de alimentar `z`- Alimentação constante.`4×4×512`Aprenda um MLP de 8 camadas que mapeia `z ∈ Z → w ∈ W`Injecção`w`em cada resolução através da * normalização de instância adaptativa* (AdaIN): normalizar cada mapa de características conv, em seguida, escalar e deslocar por projeções afínas de `w`Adicionar ruído por camada para obter detalhes estocásticos (poros da pele, fios de cabelo).

> Karras 等人(2019,NVIDIA) propôs:停止将 `z`直接送入卷积层──Use a constante `4×4×512`张量作为网络输入──学习一个8层 MLP将 `z ∈ Z → w ∈ W`◊ através de * auto-adaptation exemplo de regeneração * * AdaIN) em cada resolução injectada `w`◊ Adicionar cada camada de ruído para usar em cada detalhe

O resultado: `W`Tem eixos ortogonais para "estilo de alto nível" (posição, identidade) vs "estilo fino" (iluminação, cor).`w`para os níveis de baixa resolução e imagens B `w`Esta edição desbloqueada, estilização de domínio cruzado e toda a linha de pesquisa "StyleGAN-inversion".

> 结果:`W`空间对"高级风格" (gestão, status) e"精细风格" (luz, cores)`w`Usando níveis de baixa resolução de imagem B.`w`Usado em níveis de alta resolução para trocar estilos. Isto desbloqueou a edição, a transdomainering e toda a direção de estudo de "StyleGAN Ant-evento".

> **【中文解读】**O estiloGAN é um dos principais inovadores: 1) mapeamento de redes z→w 解开纠的隐空间; 2) AdaIN em cada nível de resolução injectar estilo低分辨率层控制粗粒度(姿势、身份), alta resolução层控制细粒度(颜色、纹理); 3) Cada nível随机噪音添加细节(毛孔、发丝) ――Style Mixing 技术可以混合不同图像的粗细特征──

> **【拓展：StyleGAN 3 的平移等变性】**StyleGAN 2 Produção de imagens com "títulos de adesão" problema características(como cabeçalhos) vai "pejar" em posição específica de imagem e não na superfície do objeto.

## O conceito central.

![StyleGAN: mapping network + AdaIN + per-layer noise](../assets/stylegan.svg)

**Mapping network.** `f: Z → W`, um MLP de 8 camadas.`Z = N(0, I)^512`- Não .`W`Não é forçado a ser gaussiano.

> **映射网络。** `f: Z → W`8 níveis de MLP.`W`Não é forçado a aprender a adaptar-se a forma de dados.

**Synthesis network.**Começa com uma constante aprendida .`4×4×512`. Cada bloco de resolução: `upsample → conv → AdaIN(w_i) → noise → conv → AdaIN(w_i) → noise`Resoluções duplas: 4, 8, 16, 32, 64, 128, 256, 512, 1024.

> **合成网络。**De aprendizagem a de constantes`4×4×512`开始──每个分辨率块:上采样→卷积→AdaIN→噪声→卷积→AdaIN→噪声──分辨率翻倍:4 到1024──

**AdaIN.**

```
AdaIN(x, y) = y_scale · (x - mean(x)) / std(x) + y_bias
```

onde`y_scale`E ...`y_bias`vêm de projecções afínas de `w`Normalize por mapa de características, depois restyle. "Style" aqui é a estatística de primeira e segunda ordem do mapa de características.

> Entre eles `y_scale`和 `y_bias`- Não .`w`O "风格" é o "título de um gráfico" e "título de um gráfico".

**Per-layer noise.**Som Gaussian de canal único adicionado a cada mapa de características, escalado por um fator por canal aprendido. Controla detalhes estocásticos sem afetar a estrutura global.

> **每层噪声。**                                                                                                                                                                                                                                                              

**Truncation trick.**Na inferência, amostra `z`, computação `w = mapping(z)`, então`w' = ŵ + ψ·(w - ŵ)`onde`ŵ`é a média`w`sobre muitas amostras. `ψ < 1`O estiloGAN é um modelo de estilo que é usado por todos os usuários.`ψ ≈ 0.7`- Não .

> **截断技巧。**推理时,`w' = ŵ + ψ·(w - ŵ)`, entre os `ŵ`Sim `w`Em vários exemplos, o valor médio é:`ψ < 1`É muito diferente de qualidade.`ψ ≈ 0.7`- Não.

## StyleGAN 1 → 2 → 3 .

| Version | Year | Innovation / 创新 |
|---------|------|------------|
| StyleGAN | 2019 | Mapping network + AdaIN + noise + progressive growing. / 映射网络 + AdaIN + 噪声 + 渐进增长。 |
| StyleGAN2 | 2020 | Weight demodulation replaces AdaIN (fixes droplet artifacts); skip/residual architecture; path-length regularization. / 权重解调替代 AdaIN。 |
| StyleGAN3 | 2021 | Alias-free convolution + equivariant kernels; eliminates texture sticking to pixel grid. / 无混叠卷积，消除纹理粘附。 |
| StyleGAN-XL | 2022 | Class-conditional, 1024², ImageNet. / 类别条件，1024²。 |
| R3GAN | 2024 | Rebrands with stronger reg; closes gap to diffusion on FFHQ-1024 with 20x fewer params. / 更强正则化，20 倍更少参数。 |

Em 2026, o StyleGAN3 continua a ser o padrão para (a) fotorrealismo de domínio estreito com FPS elevado, (b) adaptação de domínio de poucas fotografias (train em um novo conjunto de dados com 100 imagens, mapeamento de congelamento), (c) edição baseada em inversão (encontre o `w`que reconstruir uma foto real, e depois editar isso.`w`Para o domínio aberto, texto-imagem, não é a ferramenta  difusão é.

> 2026 ano StyleGAN3  ainda é a seguinte escolha em termos de cenário: a) Alta FPS 狭域照片级真感, b) Pouco padrão de domínio adaptado, c) Baseado em reversões editadas.

## Construí-lo e realizei-o.
```figure
gx-stylegan-mapping
```

## Construí-lo

`code/main.py`Implementa um brinquedo "style-GAN lite" em 1-D: um MLP de mapeamento, uma função de síntese que toma um vetor constante aprendido e o modula com `w`- a escala/bias derivadas e o ruído por camada.`w`através de correspondências de modulação afina ou batimentos concatenando `z`- O que é que é?

> `code/main.py`Em 1D, foi implementado um "StyleGAN lite": mapeamento MLP, função sintética e cada nível de ruído.`w`Com o`z`拼接到输入相比效果相当或更好──

### Passo 1: rede de mapeamento

```python
def mapping(z, M):
    h = z
    for i in range(num_layers):
        h = leaky_relu(add(matmul(M[f"W{i}"], h), M[f"b{i}"]))
    return h
```

### Passo 2: Normalização de instância adaptativa

```python
def adain(x, w_scale, w_bias):
    mu = mean(x)
    sd = std(x)
    x_norm = [(xi - mu) / (sd + 1e-8) for xi in x]
    return [w_scale * xi + w_bias for xi in x_norm]
```

A escala e o viés de mapas de características vêm de `w`através de projecção linear.

>                                                                                                                                                                                                                                                               `w`De projeção linear.

### Passo 3: ruído por camada

```python
def add_noise(x, sigma, rng):
    return [xi + sigma * rng.gauss(0, 1) for xi in x]
```

Sigma por canal é apropriado.

> Cada caminho é um sigma que se pode aprender.

## Encaixos.

- **Droplet artifacts.**O StyleGAN 1 produziu uma gota de manchas nos mapas de recursos porque o AdaIN zeroou o meio. A desmodulação de peso do StyleGAN 2 corrige-o escalando os pesos de convolução em vez disso.
  **液滴伪影。**StyleGAN 1 因 AdaIN 归零均值产生液滴──StyleGAN 2 的权重解调通过缩放卷积权重修复──
- **Texture sticking.**As texturas StyleGAN 1 e 2 seguiram as coordenadas de pixel, não as coordenadas de objeto (visíveis quando interpoladas).
  **纹理粘附。**O estiloGAN 1/2 segue a estrutura de um quadro em vez de um quadro em vez de um objeto em vez de um quadro.
- **Mode coverage.**Truncation `ψ < 0.7`Parece limpo mas amostras de um cone estreito; uso `ψ = 1.0`Se precisarem de diversidade.
  **模式覆盖。**截断 `ψ < 0.7`Parece limpo, mas de uma forma muito estreita.`ψ = 1.0`- Não.
- **Inversion is lossy.**Inverter uma foto real em `W`O resultado é geralmente feito através de otimização ou um codificador (e4e, ReStyle, HyperStyle).
  **反演有损。**Vai fazer fotos reais .`W`Normalmente, através de otimização ou codificador, o resultado vai mudar de várias gerações para outras.

## Use-o com o framework implementado.

| Use case / 用途 | Approach / 方案 |
|----------|----------|
| Photoreal human faces (anime, product, narrow) / 照片级人脸 | StyleGAN3 FFHQ / custom fine-tune |
| Face editing from a photo / 从照片编辑人脸 | e4e inversion + StyleSpace / InterFaceGAN directions |
| Face swap / reenactment / 换脸/重演 | StyleGAN + encoder + blending |
| Avatar pipelines / 虚拟形象 | StyleGAN3 w/ ADA for low-data fine-tune |
| Domain adaptation from a few images / 少样本域适应 | Freeze mapping network, fine-tune synthesis |
| Multi-modal or text-conditioned generation / 多模态生成 | Don't — use diffusion / 不要用——用扩散模型 |

Para demonstrações de qualidade de produto onde a resposta é "foto do rosto de uma pessoa", o StyleGAN supera a difusão em custo de inferência (passante único para frente, <10ms em um 4090) e nitidez para a mesma barra de qualidade.

> Para a apresentação de produtos de categoria "foto de cara de pessoa", StyleGAN é considerado um modelo de expansão de 4090 m de altura e de igual qualidade.

## Envia-o . Produto .

Salvar`outputs/skill-stylegan-inversion.md`. A competência toma uma foto real e as saídas: método de inversão (e4e / ReStyle / HyperStyle), perda latente esperada, orçamento de edição (quão longe é o tempo de `W`O artigo 1.o do Tratado de Maastricht, que estabelece a política de política comum, é o seguinte:

> 保存 `outputs/skill-stylegan-inversion.md`◊ Habilidade de receber fotos reais, de fazer resultados, de prever perdas potenciais, orçamento de edição e direções de edição conhecidas.

## Exercícios.

1. **Easy / 简单.**Corra .`code/main.py`com`adain_on=True`E ...`adain_on=False`Comparar a distribuição das saídas de um latente fixo com um latente perturbado.
   - Não .`adain_on=True`和 `adain_on=False`运行―― Comparar a distribuição de saída de variações fixas e de variações perturbadoras――
2. **Medium / 中等.**Implementar regularização de mistura: para um lote de formação, computação `w_a`- Não .`w_b`, e aplicar `w_a`para a primeira metade da síntese e `w_b`O decodificador aprende estilos desenrolados?
   实现混合正则化──解码器 ¿学到了解的风格?
3. **Hard / 困难.**Tome um modelo pré-treinado StyleGAN3 FFHQ (ffhq-1024.pkl).`w`Direcção que controla o "sorriso" através da formação de um SVM em amostras rotuladas; informe o que pode fazer antes de se desviar da identidade.
   Utilize Pre-Training StyleGAN3 FFHQ 模型, através do SVM 找到控制"微笑"的`w`Direcção:

## Termos-chave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Mapping network | "The MLP" / "那个 MLP" | `f: Z → W`, 8 layers, decouples latent geometry from data statistics. / 解耦隐变量几何与数据统计。 |
| W space | "The style space" / "风格空间" | Output of the mapping network; roughly disentangled. / 映射网络的输出；大致解耦。 |
| AdaIN | "Adaptive instance norm" / "自适应实例归一化" | Normalize feature map, then scale + shift by `w`-projection. / 归一化后用 `w` 投影缩放偏移。 |
| Truncation trick | "Psi" | `w = mean + ψ·(w - mean)`, ψ<1 trades diversity for quality. / ψ<1 以多样性换质量。 |
| Path-length regularization | "PL reg" | Penalizes large changes in image per unit change in `w`; makes `W` smoother. / 惩罚 `w` 单位变化引起的大图像变化。 |
| Weight demodulation | "The StyleGAN2 fix" / "StyleGAN2 修复" | Normalize conv weights instead of activations; kills droplet artifacts. / 归一化卷积权重而非激活。 |
| Alias-free | "StyleGAN3's trick" / "StyleGAN3 技巧" | Windowed sinc filters; eliminates texture sticking to the pixel grid. / 窗口 sinc 滤波器消除纹理粘附。 |
| Inversion | "Find w for a real image" / "找 w" | Optimize or encode `x → w` so `G(w) ≈ x`. / 优化或编码使 `G(w) ≈ x`。 |

## Nota de produção: por que o StyleGAN ainda está sendo enviado em 2026

O StyleGAN3 num 4090 gera uma face de 10242 FFHQ em menos de 10 ms  `num_steps = 1`Em termos de produção, esta é a latência de piso para qualquer gerador de imagem. Um tubo de decodificação SDXL + VAE de 50 passos com a mesma resolução é de ~ 3 segundos.**300× gap**, e para produtos de domínio restrito (serviços de avatares, canais de documentos de identificação, geração de imagens de estoque) ganha com o TCO.

> StyleGAN3 em 4090 acima de 10ms 生成 10242 人脸`num_steps = 1`, sem VAE 解码, sem交叉注意力──50 步 SDXL em sua mesma resolução cerca de 3 segundos── é **300 倍差距**, em produtos de estreito domínio TCO 获胜──

Duas consequências operacionais:

> 两个运营后果:

- **No scheduler, no batcher.**O lote estático na ocupação alvo é otimizado. O lote contínuo (essencial para os LLM e a difusão) proporciona benefícios zero porque cada pedido recebe os mesmos FLOPs.
  **无需调度器或批处理器。**静态批量最优──连续批处理(对 LLM 和扩散模型至关重要)零收益──
- **Truncation `ψ` is the safety knob.** `ψ < 0.7`A diferença entre a variância de amostra e a variância de um nível de variação de um nível de variação de um nível de variação de um nível de variação de um nível de variação de um nível de variação de um nível de variação de um nível de variação de um nível de variação de um nível de variação de um nível de variação de um nível de variação de uma variedade de variação de um nível de variação de um nível de variação de um nível de variação de um nível de variação de um nível de variação de uma variedade de variação de um nível de variação de um nível de variação de variação de um nível de variação de um nível de variação de variação de um nível de variação de variação de uma variedade de variação de um nível de variação de variação de uma variedade de variação de um nível de variação de variação de uma variedade de variação de um nível de variação de variação de uma variedade de variação de um nível de variação de variação de uma variedade de variação de uma variedade de variação de um nível de variação de variação de uma variedade de variação de uma variedade de variação de um nível de variação de uma variedade de uma variedade de variação de uma variedade de variação de uma variedade de variação de uma variedade de variação de uma variedade de variação de um nível de uma variedade de uma variedade de variação de uma variedade de variação de uma variedade de variação de uma variedade de variação de uma variedade de uma variedade de variação de uma variedade de variação de um nível de uma variedade de uma variedade de variação de uma variedade de variação de uma variedade de uma variedade de uma variedade de variação de uma variedade de um nível de uma variedade de uma variedade de uma variedade de uma variedade de uma variedade de variação de uma variedade de uma variedade de variação de um nível de uma variedade de uma variedade de uma variedade de uma variedade de uma variedade de uma variedade de um nível de uma variedade de uma variedade de um nível de uma variedade de uma variedade de uma variedade de um nível de uma variedade de uma variedade de`ψ`No pico de carga, eleva-o para os utilizadores premium.
  **截断 `ψ` 是安全旋钮。** `ψ < 0.7`A partir do mapa de rede de extensão estreita, é o único nível de diferença entre os padrões de controle de nível de serviço.`ψ`, usuário superior aumentou-se.

## Mais leitura 延伸阅读

- [Karras et al. (2019). A Style-Based Generator Architecture for GANs](https://arxiv.org/abs/1812.04948)- StyleGAN.
- [Karras et al. (2020). Analyzing and Improving the Image Quality of StyleGAN](https://arxiv.org/abs/1912.04958)- StyleGAN2.
- [Karras et al. (2021). Alias-Free Generative Adversarial Networks](https://arxiv.org/abs/2106.12423)- StyleGAN3.
- [Tov et al. (2021). Designing an Encoder for StyleGAN Image Manipulation](https://arxiv.org/abs/2102.02766) inversão e4e.
- [Sauer et al. (2022). StyleGAN-XL: Scaling StyleGAN to Large Diverse Datasets](https://arxiv.org/abs/2202.00273)- StyleGAN-XL.
- [Huang et al. (2024). R3GAN: The GAN is dead; long live the GAN!](https://arxiv.org/abs/2501.05441) Recepta moderna de GAN mínimo.
