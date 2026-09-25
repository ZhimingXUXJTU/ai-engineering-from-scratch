# Avaliação  FID, CLIP Score, Preferência Humana   avaliação indicador  FID  CLIP Score e preferências humanas

> Cada quadro de classificação de modelos geracionais cita o FID, a pontuação CLIP e uma taxa de vitória de uma arena de preferência humana. Cada número tem um modo de falha que um pesquisador determinado pode jogar.

> **【中文解读】**Cada classificação de modelos gerados cita a FID (Fréchet Inception Distance) ✓ CLIP Score 和人类偏好胜率── cada indicador tem falhas que podem ser apagadas── não compreendendo estas falhas, é impossível distinguir entre melhorias reais e a lista de actualização──

> **【拓展：FID 的局限性】**FID mede a distância de distribuição entre imagens geradas e imagens reais, mas pode ser otimizada (como a produção selecionária de alta porcentagem de amostras) e avalia as preferências humanas (como o Chatbot Arena) como uma alternativa mais confiável, mas mais cara.

**Type:** Build / 构建型 | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 8 · 01 (Taxonomy / 分类), Phase 2 · 04 (Evaluation Metrics / 评估指标) | **前置知识:** 阶段 8 · 01（分类），阶段 2 · 04（评估指标）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## O problema é o problema da introdução

Um modelo gerativo é julgado em * qualidade de amostra * e * adesão de condicionamento *. Nem tem uma medida de forma fechada. Seu modelo tem que renderizar 10.000 imagens; algo tem que atribuí-las números; você tem que confiar nos números em todas as famílias de modelos, em todas as resoluções, em todas as arquiteturas. Três métricas sobreviveram ao guante 2014-2026.

> O modelo de produção é feito em * qualidade de amostra * e * condições seguindo a avaliação * avaliação── ambas não têm uma medida fechada── seu modelo deve ter 10 mil imagens; deve ter algo para dar-lhes a classificação── três indicadores passaram por exames de 2014-2026:

- **FID (Fréchet Inception Distance).**Distância entre duas distribuições  reais e geradas  no espaço de recursos de uma rede de iniciação.
  **FID。**A verdade e a produção distribuídos em Inception 网络特征空间中的距离──越低越好──
- **CLIP score.**A semelhança cosínea entre a incorporação de imagem CLIP de uma imagem gerada e a incorporação de texto CLIP de um prompt. Mais alto é melhor. Medidas de adesão de prompt.
  **CLIP Score。**生成图像与文本提示的 CLIP 嵌入余弦相似度──越高越好──
- **Human preference.**Coloque dois modelos frente a frente no mesmo prompt, faça com que os humanos (ou um modelo de classe GPT-4) escolham o melhor, agregando para uma pontuação Elo.
  **人类偏好。** 2 modelos em relação aos modelos humanos ou GPT-4                                                                                                                                                                                                                                                         

Você também verá: IS (pontuação inicial, em grande parte aposentado), KID, CMMD, ImageReward, PickScore, HPSv2, MJHQ-30k. Cada corrigir para um fracasso do anterior.

> Você também verá: IS( já está no jogo) 、KID、CMMD、ImageReward、PickScore、HPSv2 etc.

> **【中文解读】**Os três principais indicadores de avaliação de modelos de produção: 1) FID na Inception 网络特征空间, medir a distância entre a distribuição gerada e a distribuição real, cada vez menor; 2) CLIP Score gerar imagens e texto em seguida, cada vez maior; 3) Preferências de pessoas dois modelos são melhores em comparação com a escolha, aglomerados em Elo por cento.

> **【拓展：生成模型评估的"刷榜"问题】**O FID pode ser optimizado através da seleção de gerar alta porcentagem de amostra, ajuste de nível de características do modelo de iniciação ou adaptação à distribuição de referência. O CLIP Score também tem preconceito. O modelo CLIP é mais sensível a certos conceitos. A avaliação das preferências humanas (como a Arena de Análise Artificial) é a mais confiável, mas a mais cara. A tendência de 2026 é a utilização de modelos de nível GPT-4 como "juiz automático" para se aproximar das preferências humanas.

## O conceito central.

![FID, CLIP, and preference: three axes, different failure modes](../assets/evaluation.svg)

### Qualidade de amostra

Heusel et al. (2017). Passo:

> Heusel 等人(2017)。步骤:

1. Extrair recursos Inception-v3 (2048-D) para N imagens reais e N geradas.
   Por isso, não é possível que o seu nome seja o nome de um dos seus membros.
2. Aplique um Gaussian a cada piscina: média de cálculo `μ_r, μ_g`e covariância `Σ_r, Σ_g`- Não .
   Para cada PQ: valor médio calculado`μ_r, μ_g`和协方差 `Σ_r, Σ_g`- Não.
3. FID = `||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`- Não .
   FID = `||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`- Não.

Interpretação: Distância de Fréchet entre dois Gaussianos multivariados no espaço de características.

> 解读:Trategy space                                                                                                                                                                                                                                                           

Modos de falha:

> 失败模式:

- **Biased on small N.**O FID é o quadrado médio sobre a distribuição de características  pequena N subestima a covariância, dá falsamente baixo FID.
  小 N 偏差:FID é o erro de média de distribuição de características, 小 N 会低估协方差, dá falsos FIDs baixos──necessário usar N ≥ 10.000──
- **Inception-dependent.**Inception-v3 foi treinado na ImageNet. Domínios longe da ImageNet (faces, arte, imagens de texto) produzem FID sem sentido. Use um extractor de recursos específico de domínio.
  Dependendo da Incepção:Incepção-v3 em ImageNet 上訓練──远离 ImageNet's domain ([[人脸]],艺术、文字图像) ]]) irá gerar FID sem sentido── utilizando áreas específicas de características ‧提取器──
- **Gaming.**O excesso de montagem ao prévio de iniciação dá uma baixa FID sem melhoria da qualidade visual.
  刷分: para Inception pre-testado pode dar baixo FID, mas a qualidade visual não melhorou.

### Ponto de inscrição  adesão rápida  Ponto de inscrição  Seguimento rápido

Radford et al. (2021). Para uma imagem gerada + prompt:

> Radford 等人(2021)。

```
clip_score = cos_sim( CLIP_image(x_gen), CLIP_text(prompt) )
```

Uma média de 30k imagens geradas → um escala comparável entre os modelos.

> Para 30k 张 生成图像求平均 → 1 模型间比较的标量──

Modos de falha:

> 失败模式:

- **CLIP's own blind spots.**O CLIP tem um raciocínio composto fraco ("um cubo vermelho em uma esfera azul" muitas vezes falha). Os modelos podem classificar bem no resultado do CLIP sem realmente seguir instruções complexas.
  CLIP  própria cego: CLIP 组合推理能力弱 (com frequência falha o "quadrado vermelho em bola azul")
- **Short prompt bias.**As instruções curtas têm mais coincidências de imagem CLIP na natureza.
  短 prompt 偏差:短 prompt 在野外有更多 CLIP-image 匹配──长 prompt 在 CLIP Score 上机械性地更低──
- **Prompt gaming.**Incluindo "alta qualidade, 4k, obra-prima" no prompt infla a pontuação CLIP sem melhorar a ligação imagem-texto.
  Instant 刷分: 在 prompt 中加入 "alta qualidade, 4k, obra-prima" 能升高 CLIP Score而不改善图文绑定──

CMMD (Jayasumana et al., 2024) corrige algumas destas: utiliza recursos CLIP em vez de Inception, discrepância máxima-média em vez de Fréchet. Melhor na detecção de diferenças de qualidade sutis.

> CMMD(Jayasumana 等人 2024) corrigido alguns dos problemas: usar CLIP características em vez de Inception, usar MMD(maximum mean value difference) em vez de Frechet 距离──更善于检测细微的质量差异──

### Preferências humanas  a verdade da terra  Preferências humanas  Valor real da terra

Escolha um conjunto de instruções. Gerencie com o modelo A e o modelo B. Mostre pares para os seres humanos (ou um forte juiz de LLM).

> 選一批提示──用模型 A 和模型 B 生成──把成对结果展示给人类 (), 把胜场聚聚为 Elo, 或 Bradley-Terry 分数──基准:

- **PartiPrompts (Google)**1.600 indicações diversas, 12 categorias.
  **PartiPrompts（Google）**:1600 个多样化 prompt,12 个类别──
- **HPSv2**: 107 mil anotações humanas, amplamente utilizadas como proxy automatizado.
  **HPSv2**10,7 mil artigos de marcação humana, amplamente utilizados como agente automático.
- **ImageReward**137K pares de preferências de imagem rápida, licenciados pelo MIT.
  **ImageReward**13,7 mil dólares em favor de imagens de vídeo, MIT.
- **PickScore**- formação em preferências de Pick-a-Pic 2.6M.
  **PickScore**- Não, não. - Não, não.
- **Chatbot-Arena-style image arenas**- Não .https://imagearena.ai/E outros.
  **Chatbot-Arena 风格的图像竞技场**- Não .https://imagearena.ai/E assim...

Modos de falha:

> 失败模式:

- **Judge variance.**Os não-especialistas têm preferências diferentes das dos especialistas.
  评判者方差: não especialistas e especialistas têm preferências diferentes.
- **Prompt distribution.**As instruções escolhidas favorem uma família.
  Rapido distribuição:精心挑选的快速会偏向某一家族──务必记录──
- **LLM-judge reward hacking.**O juiz GPT-4 é enganado por resultados bonitos, mas errados.
  LLM 评判被刷分:GPT-4 评判会被"好看但错"的输出欺骗──与人类三角验证──

## Usar juntos

Um relatório de avaliação da produção deve incluir:

> Um relatório de avaliação de nível de produção deve incluir:

1. FID em amostras de 10 a 30 mil em relação a uma distribuição real prolongada (qualidade da amostra).
   Em 10-30k amostras em relação à FID de distribuição real (quantidade de amostras)
2. Ponto CLIP / CMMD nas mesmas amostras versus as suas indicações (adherença).
   Como também, a sua pontuação de CLIP / CMMD (seguiência)
3. Taxa de vitória em uma arena cegar em relação ao modelo anterior (preferência geral).
   Com um modelo anterior, a taxa de vitória em câmbio de jogo (Bundespreferenças)
4. Análise do modo de falha: 50 saídas randomizadas, marcadas por problemas conhecidos (anatomia da mão, renderização de texto, contagem consistente de objetos).
   失败模式分析:随机采样 50 输出,标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已知问题 (), 标记已已已已已已问题 (), 标记已已已问题 (), 标记已已一致性 (), 标记已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已已

Qualquer métrica é uma mentira. Três métricas corroboradoras + revisão qualitativa são uma alegação.

> Qualquer indicador único é mentira. Três indicadores mutuamente comprovados.

## Construí-lo e realizei-o.
```figure
gx-fid-distributions
```

## Construí-lo

`code/main.py`Implementa a agregação de FID, CLIP-score-like e Elo em "vectores de características" sintéticos (usamos vectores 4D como substitutos para características de Inception).

> `code/main.py`Em sintetização "trademarks" para realizar FID、类 CLIP Score 和 Elo 聚合( utilizamos 4 维向量 em vez de Trademarks Inception) ;; você verá:

- Calculação FID em um pequeno N e em um grande N  o viés.
  小 N 和 大 N 上 的 FID 计算偏差──
- "Colocação CLIP" como similaridade cosínea entre as pools de características.
  Como característica de similaridade entre os fios de corda
- Regra de atualização de Elo a partir de um fluxo de preferências sintéticas.
  De composto preferencial fluxo de Elo 更新规则──

### Passo 1: FID em quatro linhas.

```python
def fid(real_features, gen_features):
    mu_r, cov_r = mean_and_cov(real_features)
    mu_g, cov_g = mean_and_cov(gen_features)
    mean_diff = sum((a - b) ** 2 for a, b in zip(mu_r, mu_g))
    trace_term = trace(cov_r) + trace(cov_g) - 2 * sqrt_cov_product(cov_r, cov_g)
    return mean_diff + trace_term
```

> Quatro linhas FID: divisão entre o real e o gerado caracteres de cálculo média e diferença de coesão, recalculação média diferença de quadrado + diferença de coesão.

### Passo 2: Similaridade cosínica de estilo CLIP.

```python
def clip_like(image_feat, text_feat):
    dot = sum(a * b for a, b in zip(image_feat, text_feat))
    norm = math.sqrt(dot_self(image_feat) * dot_self(text_feat))
    return dot / max(norm, 1e-8)
```

> CLIP 风格余弦相似度: ponto积除以两个向量范数乘积,加epsilon 防止除零──

### Passo 3: A agregação de Elo.

```python
def elo_update(r_a, r_b, winner, k=32):
    expected_a = 1 / (1 + 10 ** ((r_b - r_a) / 400))
    actual_a = 1.0 if winner == "a" else 0.0
    r_a_new = r_a + k * (actual_a - expected_a)
    r_b_new = r_b - k * (actual_a - expected_a)
    return r_a_new, r_b_new
```

> Elo 更新: Baseado na expectativa de vitória e resultados reais, K=32 é o padrão internacional de xadrez.

## Encaixos.

- **FID at N=1000.**Os documentos que relatam baixa N FID estão a jogar.
  N=1000 时的FID:在N<10k 时不可靠──报告低N FID 的论文在刷分──
- **Comparing FID across resolutions.**O tamanho de 299×299 da Inception altera a distribuição de recursos.
  跨分辨率比较 FID:Inception's 299×299 缩放会改变特征分布――只在匹配分辨率下比较――
- **Reporting one seed.**Faça 3 sementes no mínimo.
  Apenas relatar uma semente: pelo menos 3 sementes foram executadas.
- **CLIP score inflation via negative prompts.**Alguns canais aumentam o CLIP, ajustando o sinal de sinal.
  通过负向快速 抬高 CLIP Score:有些流水线通过过拟合快速 抬高 CLIP──检查视觉和──
- **Elo bias from prompt overlap.**Se ambos os modelos viram um prompt de referência durante o treinamento, o Elo não tem sentido.
  Rapido 重叠导致的 Elo 偏差: Se dois modelos treinados quando se viu um prompt de base, Elo 无意义──使用留出的 prompt 集──
- **Human eval paid-crowd skew.**Prolíficos, os anotadores MTurk tendem a ser mais jovens / amigáveis à tecnologia.
  O que é um dos principais aspectos da política de desenvolvimento tecnológico?

## Use-o com o framework implementado.

Protocolo de avaliação da produção em 2026:

> Acordo de Avaliação de Classe de Produção de 2026:

| Pillar / 支柱 | Minimum / 最低要求 | Recommended / 推荐 |
|--------|---------|-------------|
| Sample quality / 样本质量 | FID on 10k vs held-out real | + CMMD on 5k + FID on subset per category |
| Prompt adherence / Prompt 遵循 | CLIP score on 30k | + HPSv2 + ImageReward + VQA-style question answering |
| Preference / 偏好 | 200 blinded pairs vs baseline | + 2000 paired human + LLM-judge + Chatbot Arena |
| Failure analysis / 失败分析 | 50 hand-flagged | 500 hand-flagged + automated safety classifier |

Os quatro pilares num relatório = reivindicação.

> Quatro pilares são uma declaração. Qualquer um só é apenas uma propaganda.

## Envia-o . Produto .

Salvar`outputs/skill-eval-report.md`. A Skill toma um novo ponto de controlo modelo + linha de base e elabora um plano de avaliação completo: tamanhos de amostra, métricas, sondas de modo de falha, critérios de assinatura.

> 保存为 `outputs/skill-eval-report.md` Esta habilidade recebe um novo ponto de controlo de modelo + 基线, produz um plano de avaliação completo: sample numbers, indicators, fail patterns, signature standards.

## Exercícios.

1. **Easy.**Corra .`code/main.py`. Comparar FID em N=100 vs N=1000 nas mesmas distribuições sintéticas.
2. **Medium.**Implementar CMMD a partir de características sintéticas de estilo CLIP (ver Jayasumana et al., 2024 para a fórmula).
3. **Hard.**Replicar a configuração HPSv2: pegue 1000 pares de imagens de um subconjunto de Pick-a-Pic, ajuste o pequeno marcador baseado em CLIP nas preferências e mensure sua concordância com um conjunto mantido.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| FID | "Fréchet Inception Distance" | Fréchet distance of Gaussian fits to real vs gen Inception features. |
| CLIP score | "Text-image similarity" | Cosine similarity between CLIP image and text embeddings. |
| CMMD | "FID's replacement" | CLIP-feature MMD; less biased, no Gaussian assumption. |
| IS | "Inception score" | Exp KL(p(y|x) || p(y)); correlates poorly on modern models, retired. |
| HPSv2 / ImageReward / PickScore | "Learned preference proxies" | Small models trained on human preferences; used as automatic judges. |
| Elo | "Chess rating" | Bradley-Terry aggregation of pairwise wins. |
| PartiPrompts | "The benchmark prompt set" | 1,600 Google-curated prompts across 12 categories. |
| FD-DINO | "Self-sup replacement" | FD using DINOv2 features; better for out-of-ImageNet domains. |

## Nota de produção: avaliação é uma carga de trabalho de inferência também

Para uma base SDXL de 50 passos em 10242 em um único L4, isto é ~ 11 horas de inferência de pedido único. Os orçamentos de avaliação são reais, e o enquadramento é exatamente o cenário de inferência offline (máxima o throughput, ignore o TTFT):

- **Batch hard, forget latency.**Avaliação offline = batch estático no maior tamanho que se encaixa na memória. `pipe(...).images`com`num_images_per_prompt=8`num H100 de 80 GB funciona 4 a 6 vezes mais rápido do que um único pedido.
- **Cache the real features.**A extracção da função Inception (FID) ou CLIP (CLIP-score, CMMD) sobre o conjunto de referência real é executada *once*, armazenada como um`.npz`Não recomputem por avaliação.

Para os portões de CI / regressão: executar o FID + CLIP em um subconjunto de 500 amostras por PR (~ 30 min); executar o FID + HPSv2 + Elo completo por noite.

## Mais leitura 延伸阅读

- [Heusel et al. (2017). GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium (FID)](https://arxiv.org/abs/1706.08500)Papel da FID.
- [Jayasumana et al. (2024). Rethinking FID: Towards a Better Evaluation Metric for Image Generation (CMMD)](https://arxiv.org/abs/2401.09603) CMMD.
- [Radford et al. (2021). Learning Transferable Visual Models from Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020)- O que é isso?
- [Wu et al. (2023). HPSv2: A Comprehensive Human Preference Score](https://arxiv.org/abs/2306.09341) HPSv2.
- [Xu et al. (2023). ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation](https://arxiv.org/abs/2304.05977) ImageReward.
- [Yu et al. (2023). Scaling Autoregressive Models for Content-Rich Text-to-Image Generation (Parti + PartiPrompts)](https://arxiv.org/abs/2206.10789) PartiPrompts.
- [Stein et al. (2023). Exposing flaws of generative model evaluation metrics](https://arxiv.org/abs/2306.04675) Pesquisa de modo de falha.
