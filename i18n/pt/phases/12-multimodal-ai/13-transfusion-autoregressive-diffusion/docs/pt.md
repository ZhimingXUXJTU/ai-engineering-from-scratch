# Transfusão: Texto autoregressivo + Imagem de difusão em um transformador . Transfusão: um transformador e fazer auto-regressão

> O Camelão e o Emu3 apostaram tudo em tokens discretos. Funcionam, mas o gargalhão de quantização é visível  os planícies de qualidade de imagem abaixo dos modelos de difusão no espaço contínuo. A transfusão (Meta, Zhou et al., agosto 2024) faz a aposta oposta: manter imagens contínuas, soltar o VQ-VAE inteiramente e treinar um transformador com duas perdas. Os tokens de texto recebem a previsão do próximo token. Os parches de imagem têm uma perda de fluxo de correspondência / difusão. Ambos os objetivos otimizam os mesmos pesos. A arquitetura subjacente à Stable Diffusion 3 (MMDiT) é uma prima próxima. Esta lição lê a tese da Transfusão, constrói um treinador de brinquedos de duas perdas e rastreia a máscara de atenção que permite que um transformador faça ambos os trabalhos.

> **【中文解读】**Transfusão(Meta,2024年8月) escolheu o caminho oposto com Chameleon/Emu3: manter imagens para continuidade, sem usar VQ-VAE, com um Transformador, simultaneamente executar dois perdas texto token usando o seguinte token 预测, imagens adicionadas com流匹配/扩散损失──Stable Diffusion 3 MMDiT arquitetura é próximo.

> **【拓展：双损失训练的工程挑战】**O ponto central de dificuldade da transfusão está em equilibrar duas funções de perda diferentes de uma escala numérica.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, two-loss trainer on MNIST-scale toy) | **语言:** Python（标准库，MNIST 规模玩具的双损失训练器）
**Prerequisites:** Phase 12 · 11 (Chameleon), Phase 8 (Generative AI) | **前置知识:** Phase 12 · 11（Chameleon），Phase 8（生成式 AI）
**Time:** ~180 minutes | **时间:** ~180 分钟

> - Não .**【前置】**O primeiro é o primeiro, o segundo é o segundo, o segundo é o segundo. O segundo é o segundo.
> - Não .**【类比】**Transfusão = "双拼户型"──Chameleon = 一居室(todo o conteúdo com o mesmo token);LLaVA = 联排别(视觉和文本完全分开,靠桥接连接);Transfusão = 双拼(一边文本 下一个代号损失,一边图像扩散损失,共享承重墙 = 同一个变压器骨干)── dois perdas juntos optimization 组参数, preservar as suas próprias vantagens de modelo.
> ️ **【易错点】**两个损失直接相加而不调权重 → 一个损失主导训练(normalmente dilatar MSE 数值大,文本 NTP被淹没) ――修复:Use loss weighting(如 λ_text=1.0, λ_image=0.1) 或 GradNorm 自适应平衡──

## Objetivos de aprendizagem

- Enviar um transformador que corre duas perdas (NTP em tokens de texto, MSE de difusão em parches de imagem) em uma espinha dorsal.
  > Construir um transformador que possa correr em dois perdas no mesmo tronco (NTP + Image Patch)
- Explique por que a atenção bidirecional entre os patches de imagem mais a atenção causal sobre os tokens de texto é a escolha certa da máscara.
  > Explicação de porquê "imagem de parche 双向 + 文本代币因果" é a escolha de ocultar a imagem.
- Compare o estilo Transfusão (imagem contínua, perda de difusão) com o estilo Camelão (imagem discreta, NTP) em computação, qualidade e complexidade de código.
  > Comparar Transfusão 风格 (连续图像、扩散损失) com Camelão 风格 (离散图像、NTP) em diferença em capacidade de cálculo、 qualidade e complexidade do código.
- Nomear a contribuição da MMDiT: pesos específicos de modalidade em cada bloco, atenção conjunta no fluxo residual.
  > 列举 MMDiT's contributions: Modelo de cada bloco específico de peso, o que é o seu valor.

## O problema é o contexto do problema .

O debate entre tokens de imagem discretos e contínuos é mais antigo do que os LLM. As representações contínuas (pixels brutos, VAE latentes) preservam detalhes.

> 离散与连续图像代币的争论比 LLM 更早──连续表示(原始像素、VAE 潜变量)保留细节──离散代币(VQ索引) Adaptação ao cronograma original do Transformer, mas em quantização

O Chameleon / Emu3 foi discreto: uma perda, uma arquitetura, mas a fidelidade da imagem foi limitada pela qualidade do tokenizer.

> Camelão / Emu3 选择离散: uma perda, uma estrutura, mas a fidelidade da imagem é limitada à qualidade dos seus componentes.

Os modelos de difusão foram contínuos: qualidade de imagem excepcional, mas um modelo separado do LLM, engenharia complexa de programação de ruído e nenhuma integração limpa com a geração de texto.

> 扩散模型选择连续:卓越的图像质量, mas com LLM é um modelo independente, requer engenharia de ajuste de ruído complexa, incapaz de gerar uma integração pura com o texto.

A transfusão pergunta: podemos ter ambas? Mantém as imagens contínuas, ainda treine um modelo, use duas perdas costuradas em um passo de gradiente.

> Transfusão 问:能否兼得两者? manter imagem连续, ainda treinar um modelo, usar dois perdas para juntar um gradiente de passo em passo.

## O conceito central.

> **【中文解读】**TransFusion(Meta) será auto-regregulado texto gerar e espalhar modelo imagem gerar融合 em um mesmo Transformer 中: texto token Usar a próxima marca de previsão perda, imagem token Usar perda de expansão──两种模态共享相同模型参数但使用不同训练目标──

> **【拓展：多模态训练目标的融合】**Transfuso  prova de auto-regulação e expansão pode existir no mesmo modelo e  comunhão.


### A arquitetura de duas perdas

Um único transformador de decodificador só processa uma sequência que contém:

> 单一解码器 Transformer 处理 contém o seguinte sequência de conteúdo:

- Tokens de texto (discreto, do vocabulário BPE).
  O que é que você tem a ver com o seu nome?
- Patches de imagem (contínuos, blocos de pixels 16x16 projetados em dim oculto através de incorporação linear  igual à entrada de um codificador ViT).
  Chinese:图像补丁 (图像补丁) 连续,16x16 像素块通过线性嵌入投影到隐藏维度与ViT 编码器输入相同) 
- `<image>`E ...`</image>`Tags que marcam onde os parches contínuos vivem.
  Tradução:`<image>`和 `</image>`标签标记连续补丁的位置──

O passante avançado corre uma vez.

> Antes de divulgar, perdemos por cada token.

- Para tokens de texto: entropia cruzada padrão na cabeça do vocabulário-logits.
  O símbolo do texto é o símbolo do texto.
- Para os parches de imagem: perda de difusão em parches contínuos  prevê o ruído que foi adicionado a cada parche.
  Tradução do inglês: image patch:连续 patch 上的扩散损失预测 每个补丁 添加的噪音──

O gradiente flui através do corpo do transformador compartilhado.

> 梯度通过共享的变压器 体回流――两损同时改进共享权重――

### Mascara de atenção: texto causal + imagem bidirecional

Os tokens de texto devem ser causais  você não pode deixar um token de texto atender a texto futuro, ou professor forçando pausas.

> O texto token 必須是因果的不能让文本 token 关注未来文本,否则教师强制会失败―― mas o parche de imagem 代表一个快照; eles devem estar em um mesmo bloco de imagem dois para se preocuparem uns com os outros――

A máscara:

> 掩码:

```
M[i, j] = 1 if:
  (i is text and j is text and j <= i)   # causal for text
  OR (i is image and j is image and same_image_block(i, j))   # bidirectional within image
  OR (i is text and j is image and j < i_image_end)   # text attends to previous images
  OR (i is image and j is text and j < i_image_start)   # image attends to preceding text
```

Implementado como uma máscara triangular de bloco no treinamento e inferência.

> Em treino e meditação, realização para bloco

### Perda de difusão dentro do transformador

A perda de difusão é padrão: adicione ruído a um parche de imagem, peça ao modelo para prever o ruído (ou o parche limpo, equivalentemente).

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

Durante a formação:
1. Para cada parche de imagem x0, amostre um passo temporal aleatório t.
   Chinese:                                                                                                                                                                                                                                                              
2. Escolha ruído ε, calcula xt = (1-t) * x0 + t * ε (interpolação linear para a correspondência de fluxo).
   Tradução em inglês: 采样噪声 ε,计算 xt = (1-t) * x0 + t * ε(流匹配的线性插值)
3. O transformador prevê v_theta(xt, t); perda = MSE(v_theta(xt, t), ε - x0).
   Tradução do português:Transformer 预测 v_theta(xt, t);损失 = MSE(v_theta(xt, t), ε - x0)。
4. O backprop ao lado de perdas de texto NTP da mesma sequência.
   Tradução do inglês: NTP 损失一起反向传播──

Na inferência, a geração é:
- Tokens de texto: amostragem autoregressiva padrão.
  O que é o "título" do livro?
- Parches de imagem: ciclo de amostragem de difusão (10-30 passos típicos) condicionado aos tokens de texto anteriores.
  O padrão de imagem é um padrão de imagem de um padrão de imagem de um padrão de imagem.

### MMDiT: Variante da Stable Diffusion 3

Estabilidade Diffusion 3 (Esser et al., março 2024) enviou MMDiT (Multimodal Diffusion Transformer) em torno do mesmo tempo que Transfusion.

> Estabilidade de difusão 3 (Esser 等人,2024 年 3 月) lançou MMDiT (多模态扩散变压器),与 转变差不多同时──两者架构是兄弟──

Principais diferenças do MMDiT:

> MMDiT's principais diferenças:

- Pesos específicos de modalidade por bloco. Cada bloco transformador tem pesos Q, K, V e MLP separados para tokens de texto versus parches de imagem.
  Tradução do inglês: Each block's mode mode specific weight── cada bloco transformador 块 has independent text token vs 图像 patch's Q、K、V 和 MLP 权重──注意力是联合的(跨模态); restantes são mode specific──
- Formação de fluxo corrigida. Uma variante específica de correspondência de fluxo com amostragem conhecida e matemática mais simples do que a DDPM.
  Tradução do inglês para o inglês: 整流流训练──一种特定流匹配变体,采样已知,数学比DDPM更简单──
- Escala. MMDiT é a espinha dorsal para SD3 (2B e 8B variantes param).
  Tradução do inglês:                                                                                                                                                                                                                                                            

Ambos convergem na mesma ideia central: um transformador executa NTP em texto e difusão em representações contínuas de imagem.

> 两者收到同一核心理念: 一 Transformer 在文本上运行NTP, 在连续图像表示上运行扩散──

### Por que é melhor que o estilo de camaleão

A diferença de qualidade entre a difusão contínua e a NTP discreta na geração de imagens é mensurável.

>  Continual expansão e dispersão NTP na produção de imagens diferença de massa é quantificável.

- Nos parâmetros 7B, supera um modelo de estilo camaleão do mesmo tamanho na FID por 3-5 pontos.
  O FID venceu o Camelão de tamanho 3 a 5 minutos.
- Não é necessário treinamento de tokenizer  o codificador de imagem é mais simples (projeção linear para oculta, igual à camada de entrada de um ViT).
  Não é necessário fazer um treino de um sistema de imagens.
- A inferência pode paralelalizar a denotação de patch de imagem, ao contrário dos tokens de imagem autoregressivos.
  Não é diferente do token de imagem auto-regressado.

Desvantagem: A transfusão é um modelo de dupla perda, tornando a dinâmica de treinamento mais complicada. Pesos de perda precisam ser ajustados.

> 缺点:Transfusão é um modelo de perda dupla, treinamento está mais complexo.

### O que fica ao fundo do rio

Janus-Pro (Lessão 12.15) aperfeiçoou a ideia da Transfusion descouplando o codificador de visão para compreensão e geração  SigLIP para um, VQ para o outro  enquanto compartilha o corpo do transformador. Show-o (Lessão 12.14) troca difusão por difusão discreta (previsão mascarada).

> Janus-Pro (→ 12.15) 课) 通过解视觉编码器改进了Transfusion的思想SigLIP 用于理解,VQ 用于生成同时共享Transformer 主体──Show-o (→ 12.14) 课) 将扩散换换为离散扩散掩码预测──统一生成家族在Transfusion 后迅速分化──

2026 produção VLMs que emitem imagens  Gemini 3 Pro, GPT-5, Claude Opus 4.7 caminho de geração de imagens  quase certamente usar algum descendente desta família.

> 2026 Anos de produção de imagens VLMGemini 3 Pro、GPT-5、Claude Opus 4.7 imagens de produção de caminho Quase se pode determinar que usou algum tipo de geração posterior desta família.


> **【拓展：TransFusion 的推理过程】**Transfuso                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           


## Use-o em prática.
```figure
cfg-guidance-scale
```

## Usá-lo

`code/main.py`Construiu um brinquedo Transfusion sobre um pequeno problema parecido com o MNIST:

> `code/main.py`Em questão de construção de brinquedos em MNIST

- Capções de texto são curtas sequências de números inteiros que descrevem um dígito (0-9).
  O texto descrito é a descrição de um número (0-9) de um número curto.
- As imagens são redes de 4x4 bytes.
  中文翻译:图像是4x4 字节网格──
- Um par de projeções lineares de peso compartilhado atua como o substitutor do transformador; perda de NTP no texto, perda de MSE em parches barulhentos.
  Tradução do inglês para tradução do inglês: One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One One
- O ciclo de treinamento alternou as duas perdas, a máscara de atenção é explícita.
  Tradução do inglês: Training cycle exchange for two losses, attentionfulness mask码 is manifest.
- A geração produz uma legenda de texto e uma imagem 4x4 em uma passagem para a frente.
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para inglês para tradução do inglês para inglês para inglês para inglês para o inglês para o inglês para o inglês para inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe: ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา ภาษา    ภาษา ภาษา        ภาษา  ภาษา                                                                                                                                                                                                                               

A canalização de duas perdas, a construção da máscara de atenção e o ciclo de inferência são os verdadeiros artefatos.

> O transformador é de classe de brinquedo.

## Envia-o .

Esta lição produz`outputs/skill-two-loss-trainer-designer.md`. Tendo em conta uma nova tarefa de formação multimodal (texto + imagem, texto + áudio, texto + vídeo), elabora o cronograma de duas perdas (pesos de perda, forma de máscara, blocos compartilhados versus blocos específicos de modalidade) e sinaliza os riscos de implementação.

> 本课产 出 `outputs/skill-two-loss-trainer-designer.md`◊ Foi dada uma nova tarefa de treinamento de vários modos (文本+图像、文本+音频、文本+视频), que desenhou duas perdas de peso (重量损失、掩码形、共享 vs. 模态特定块) e marcou a realização do risco。

## Exercícios.

1. Um modelo de estilo Transfusion treina 70% de tokens de texto e 30% de parches de imagem. A perda de difusão de imagem é ~10x a perda de NTP de texto em magnitude. Que pesos de perda os equilibrar?
   Tradução do idioma japonês:Transfusão 风格模型训练 70% 文本代币 和 30% 图像补丁──图像扩散损失在量级上约为文本NTP损失的10倍──什么损失权重能平衡它们?

2. Implementar a máscara triangular de bloco para uma sequência: `[T, T, <image>, P, P, P, P, </image>, T]`Marque cada entrada 0 ou 1.
   Tradução do português:`[T, T, <image>, P, P, P, P, </image>, T]`实现块三角掩码──标记每个条目为0或1──

3. MMDiT tem pesos QKV específicos para modalidade. Que parâmetro contagem sobrecarga adiciona esta versus o transformador totalmente compartilhado da Transfusion?
   Em comparação com Transfusion, o Transformer total compartilhado aumentou quantos parâmetros?

4. Geração: dado um prompt de texto, o modelo executa NTP para 50 tokens, em seguida, atinge `<image>`, então corre difusão em 256 parches sobre 20 passos denoise.
   Não é um sinal de segurança, mas é um sinal de segurança.`<image>`Depois, em 256 parches, 20 passos para a expansão do ruído.

5. Leia o artigo SD3 Secção 3. Descreva o fluxo rectificado e por que converge em menos etapas de inferência do que o DDPM.
   Tradução do idioma: Lire o artigo 3o do artigo 3o.

## Termos-chave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Two-loss training | "NTP + diffusion" | A single transformer optimizes both cross-entropy on text tokens and MSE on continuous image patches in the same gradient step | 单一 Transformer 在同一梯度步中优化文本 token 交叉熵和连续图像 patch MSE |
| Flow matching | "Rectified flow" | Diffusion variant that predicts a velocity field from noise to clean data; simpler math than DDPM | 预测从噪声到干净数据速度场的扩散变体；数学比 DDPM 更简单 |
| MMDiT | "Multimodal DiT" | Stable Diffusion 3's architecture: joint attention, modality-specific MLPs and norms | SD3 架构：联合注意力、模态特定 MLP 和归一化 |
| Block-triangular mask | "Causal text + bidirectional image" | Attention mask that is causal across text but bidirectional within image regions | 文本因果、图像区域内双向的注意力掩码 |
| Continuous image representation | "No VQ" | Image patches as real-valued vectors, not integer codebook indices | 图像 patch 为实值向量，非整数码本索引 |
| Velocity prediction | "v-parameterization" | Network output is the velocity field between noise and data, not the noise itself | 网络输出为噪声和数据之间的速度场，非噪声本身 |

## Mais leitura 延伸阅读

- [Zhou et al. — Transfusion (arXiv:2408.11039)](https://arxiv.org/abs/2408.11039)
  Tradução do português:Transfusion
- [Esser et al. — Stable Diffusion 3 / MMDiT (arXiv:2403.03206)](https://arxiv.org/abs/2403.03206)
  中文翻译:Stable Diffusion 3 / MMDiT 论文。
- [Peebles & Xie — DiT (arXiv:2212.09748)](https://arxiv.org/abs/2212.09748)
  Tradução do inglês: Transformer
- [Zhao et al. — MonoFormer (arXiv:2409.16280)](https://arxiv.org/abs/2409.16280)
  中文翻译:MonoFormer 论文。
- [Xie et al. — Show-o (arXiv:2408.12528)](https://arxiv.org/abs/2408.12528)
  O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é?
