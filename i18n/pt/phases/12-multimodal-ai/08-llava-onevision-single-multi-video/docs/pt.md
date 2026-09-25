# LLaVA-OneVision: Single-Image, Multi-Image, Video em Um Modelo

> Antes de LLaVA-OneVision (Li et al., agosto de 2024) o mundo de VLM aberto tinha linhagens separadas: LLaVA-1.5 para imagens individuais, modelos de imagens múltiplas como Mantis e VILA, modelos de vídeo como Video-LLaVA e Video-LLaMA. Cada um ganhou o seu valor de referência e falhou nos outros. A LLaVA-OneVision argumentou que um único currículo poderia treinar um modelo para dominar os três cenários, e que os efeitos emergentes de transferência de tarefas (habilidades de imagem única exportadas para vídeo, raciocínio de imagem múltipla exportado para imagem única) superaram a soma de especialistas. A receita é deceptivamente simples: um orçamento visual-token que permanece constante em todos os cenários, além de um currículo explícito que passa de uma imagem única para OneVision (multi-imagem) para vídeo. Esta lição lê o orçamento, o currículo e os comportamentos emergentes.

> **【中文解读】**Contribuição central de LLaVA-OneVision: com um único token visual  orçamento (cerca de 3000-4000 tokens) e um programa de três fases de aprendizagem (单图→多图→视频), treinamento de um modelo de três cenários de aprendizagem que traz a capacidade de surgir em habilidades de aprendizagem em um único gráfico que podem ser transferidas para o vídeo.

> **【拓展：统一多模态模型的产业价值】**No produto real, o usuário pode simultaneamente enviar imagens únicas, imagens e vídeos.

**Type:** Build  | **类型：构建**
**Languages:** Python (stdlib, token budget solver + curriculum planner)  | **语言：Python（标准库，token预算求解器 + 课程规划器）**
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 12 · 06 (any-resolution)  | **前置：阶段12第05课（LLaVA）、阶段12第06课（任意分辨率）**
**Time:** ~180 minutes  | **时长：约180分钟**

> - Não .**【前置】**O curso de aprendizagem é um curso de aprendizagem de aprendizagem de aprendizagem de aprendizagem.
> - Não .**【类比】**LLaVA-OneVision = "Onde todo o poder é usado"── outros VLM = 专门的单功能刀(单图刀、多图刀、视频刀)──Reixa militar cada um dos seus recursos não é especial, mas pode lidar com cenários desconhecidos; mantenha um único token 预算(3000-4000) = 子和刀片的总长度恒定,根据场景切换主功能──

## Objetivos de aprendizagem

- Desenhar um orçamento de tokens visuais que mantenha constante em entrada de imagem única, imagem múltipla e vídeo.
- Ordenar um currículo de treinamento que transfere habilidades de uma única imagem para o vídeo sem esquecimento catastrófico.
- Explicar por que um único modelo supera especialistas na mesma contagem de parâmetros quando o currículo é feito corretamente.
- Nomear as três capacidades emergentes relatadas pela LLaVA-OneVision: raciocínio multi-câmera, set-of-mark prompting, agente de captura de tela do iPhone.

## O problema é o contexto do problema .

Imagem, multi-imagem e vídeo cada um enfatizam um modelo de forma diferente.

A imagem única requer tokens de alta resolução (AnyRes, ~ 2880 tokens visuais) para capturar OCR e detalhes finos. Orçamento por amostra: uma imagem, 2880 tokens.

Multi-imagem quer várias imagens com resolução moderada (~ 576 tokens cada) para que o raciocínio entre imagens se encaixa no contexto. Orçamento por amostra: 4-8 imagens, 576 cada, 2300-4600 tokens.

O vídeo precisa de muitos quadros com baixa resolução (~ 196 tokens por quadro após a agregação) para capturar a dinâmica temporal. Orçamento por amostra: 8-32 quadros, 196 cada, 1600-6200 tokens.

> **【中文解读】**Três cenários para token  orçamento de demanda diferentes: single picture for high resolution (((cerca de 2880 tokens), multi picture for medium resolution (((cerca de 576 tokens), video video for low resolution but more(cerca de 196 tokens) ⋅ desafio em: como atender a três cenários simultaneamente com um orçamento fixo

Se treinarmos modelos separados, escolheremos um orçamento. Se treinarmos um modelo, precisamos do orçamento para escalar sensatamente em todos os cenários sem estragar o contexto.

Antes da OneVision, a resposta padrão era "treinar um cenário, ignorar os outros". Video-LLaVA retrofittado vídeo em um modelo de imagem com etapas de treinamento extra. LLaVA-NeXT adicionou suporte a imagem múltipla com azulejos. Nenhum manuseou as três limpos.

## O conceito central.

### O orçamento do token OneVision.

A LLaVA-OneVision escolhe um orçamento unificado de tokens visuais de aproximadamente 3000-4000 tokens por amostra, atribuídos de forma diferente por cenário:

- Imagem única / 单图: AnyRes-9 (3x3 azulejos + miniatura), cada azulejo em 384 com 729 parches, bilinear agressível de aglutinamento 2x2 → 182 por azulejo. Total: 9 * 182 + 182 = 1820 tokens.
- Multi-imagem / 多图: cada imagem em resolução moderada (384, sem telas), 729 tokens sem pooling. Orçamento 6 imagens → 4374 tokens.
- Video / 视频: 32 quadros com resolução 384 com pool bilinear agressivo 3x3 → 81 tokens por quadro. Total: 32 * 81 = 2592 tokens.

A alocação mantém tokens totais praticamente constantes. O LLM nunca vê um lote que sopra seu contexto. O codificador produz geometria diferente por cenário, mas o LLM consome o mesmo orçamento.

> **【中文解读】**核心思想:总代币 预算保持恒定(约3000-4000), mas o modo de distribuição é diferente de cenário.

### O currículo de três etapas.

Os trens LLaVA-OneVision são divididos em três fases:

1. SFT de imagem única (estado SI) / 单图指令微调. Todos os dados são de imagem única e texto. Treinar com entrada AnyRes de alta resolução. Isso ensina percepção, OCR e compreensão de grãos finos. Utiliza dados LLaVA-NeXT mais dados de imagem única específicos da OneVision.
2. OneVision SFT (estadio OV) / 统一指令微调. Misture imagem única + imagem múltipla + vídeo (quadros de amostra uniformemente). Treine no orçamento de token unificado. Isso ensina o modelo a lidar com formas de lote heterogêneas.
3. Transferência de tarefas (fase TT) / 任务迁移. Continuar com um mix de tarefas alvo, normalmente mais pesado em imagem ou vídeo múltipla dependendo do produto. Opcional de ajuste fino para implantação.

O estudo também mostra que a formação de vídeo primeiro ou de imagem múltipla primeiro produz um desempenho de imagem pior do que a imagem única primeiro, mesmo com os mesmos dados.

> ️ **【易错点】**Auto-treinamento unificado VLM 时课程顺序搞反了(先训视频再训单图)→ 单图性能大幅下降──原因:视频低分辨率输入让模型先学到"模糊是正常的",再训高分辨率单图时模型适应不过来──修复:必须单图 → 多图 → 视频的顺序,先学精细再学粗──
> 🤔 **【困惑】**P: Por que é que o token fixo  orçamento é tão importante? Porque a janela de lógica do LLM é fixa, o único plano de repente ocupa 5000 tokens、 vídeo 10000 tokens, vai destruir batching 和推理预算── orçamento fixo = custo de cálculo previsível, é o chave para a implantação do produto──

> **【中文解读】** sequência de curso é essencial: primeiro single-toto、再多图+vídeo、最后任务迁移──如果先训练视频或多图,单图性能会下降──这是因为单图训练建立感知基础,多图和视频的时序/空间推理需要基于此──

### Porque é que o currículo funciona ?

O treinamento de imagem única constrói a base perceptiva. Os tokens de patch carregam características visuais de grãos finos; o LLM aprende a integrá-los com o texto. A imagem e o vídeo multi-introduem desafios estruturais (que imagem é qual, o que aconteceu primeiro) que são difíceis de aprender sem uma base perceptiva forte.

Se você treinar todos os cenários a partir do zero juntos, o modelo não se encaixa na percepção (data limitada de imagem única por lote) e na estrutura de sobre-excesso (muitos dados de imagem / vídeo).

A ordem do currículo dá-lhe força de percepção a partir da fase SI, depois raciocínio composto/temporal a partir da fase OV, sem perder nenhum.

> **【中文解读】**Se ao mesmo tempo treinar todas as cenas, o modelo ficará sem capacidade de percepção adequada (construção adequada) e não será capaz de fazer uma grande quantidade de imagens/vidéos/dados), o que levará ao modelo a fazer uma percepção transversal (construção de imagens/vidéos/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dados/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/dos/

### Habilidades emergentes de transcêntricos em cenários

O artigo LLaVA-OneVision relata três capacidades emergentes:

1. Raciocínio com várias câmeras / 多摄像头推理. Treinado em múltiplas imagens + vídeo separadamente; em inferência, solicitado a raciocínio sobre uma cena de condução com várias câmeras. O modelo integra corretamente as visões apesar de nunca ver esse formato exato no treinamento.
2. Instrução de conjunto de marcas / 标记提示. O usuário anota objetos em uma imagem com marcas numeradas; o modelo argumenta sobre "o que a marca 3 faz em relação à marca 7." Treinado em nem marcas nem anotações; aprendido a partir da combinação de aterragem espacial + referência de imagem múltipla.
3. Agente de captura de tela do iPhone / 手机截图代理. O usuário fornece uma captura de tela de uma tela do iPhone e pede para planejar o próximo clique. Formada em captura de tela da UI, vídeo dos fluxos de trabalho do usuário e multi-imagem antes / depois de pares. Generaliza para o caso de uso do agente.

Estas não são tarefas formadas; emergem da estrutura composta do currículo.

> **【拓展：涌现能力的工程启示】**A capacidade de surgir significa que o valor do modelo unificado excede os diferentes especialistas. A capacidade de raciocínio de várias câmeras pode ser usada para controle de segurança, condução automática; a capacidade de sinalização de pontas pode ser usada para ferramentas de sinalização de imagem; o agente de interceptação pode ser usado para testes de automação de UI.

### Compartilhamento de tokens visuais

O orçamento de tokens requer pooling. OneVision usa interpolação bilinear na grade de parches 2D: 24x24 = 576 parches torna-se 12x12 = 144 (2x factor) ou 8x8 = 64 (3x factor).

A escolha de um fator de pooling por cenário é em si um hiperparâmetro. Menos pooling = mais tokens = representação mais rica.

> **【中文解读】**池化在2D 补丁网格空间进行(而不是 token 空间),以保留空间局部性──池化因子是每个场景的超参数:少池化=更多 token=更丰富表示;多池化=更少 token=可容纳更多/图像──

### LLaVA-OneVision-1.5

O seguimento de 2025 (LLaVA-OneVision-1.5, arXiv 2509.23661) é "totalmente aberto" em dados de treinamento, pesos de modelo e código.

### Contraste com Qwen2.5VL em relação a Qwen2.5VL

Qwen2.5-VL (Lessão 12.09) faz escolhas diferentes. Utiliza M-RoPE e FPS dinâmico em vez de pooling fixo. Suas escalas de orçamento com entrada  um vídeo de 1 minuto usa mais tokens do que um vídeo de 5 segundos. LLaVA-OneVision fixa o orçamento e escala o pooling. Ambos funcionam; eles trocam configurabilidade por previsibilidade.

> **【中文解读】**Qwen2.5VL Utilizando M-RoPE 和动态率,token 预算随输入缩放;LLaVA-OneVision 固定预算、调整池化── duas estratégias têm todos os seus vantagens: o primeiro é rápido, mas o custo é imprevisível, o segundo é custo controlado, mas pode ser desperdiçado ou insuficiente──
```figure
l5-onevision-budget
```

## Usá-lo

## Use-o em prática.

`code/main.py`É um planejador curricular e orçamental para um VLM de estilo OneVision. Dada uma quantidade de tokens por amostra e uma mistura de cenários-alvo (por exemplo, 40% de imagem única, 30% de imagem múltipla, 30% de vídeo), ele:

- Aloca resolução, fator de agregação e quadros por cenário.
- Verifica se cada cenário se encaixa no orçamento compartilhado.
- Relatórios de número de tokens esperados, FLOPs LLM, e quais cenários são sub-tokenized.
- Imprime um programa de treinamento passo a passo.

## Envia-o .

Esta lição produz`outputs/skill-onevision-budget-planner.md`. Dada uma distribuição de tarefas-alvo e um orçamento por amostra, ele emite o fator AnyRes, o pooling por quadro, a contagem de quadros de vídeo e os pesos de estágios do currículo.

> **【中文解读】**Este curso é produzido por OneVision  orçamento de planejamento de ferramentas.

## Exercícios.

1. O seu produto suporta 80% de imagem única, 10% de imagem multi (2-4 imagens), 10% de vídeo (8-16 quadros).
   | 产品支持 80% 单图、10% 多图（2-4张）、10% 视频（8-16帧）。设计 token 预算。从轻量多图中省下的预算放在哪？

2. Leia a Seção 4.3 (Capacidades emergentes) do LLaVA-OneVision. Propõe uma quarta habilidade emergente que o currículo provavelmente desbloquearia, mas o artigo não relatou.
   | 阅读 LLaVA-OneVision 第 4.3 节（涌现能力）。提出课程学习可能解锁但论文未报告的第四种涌现技能。

3. Troque a ordem do currículo  treine a imagem múltipla primeiro, depois a imagem única, depois o vídeo.
   | 交换课程顺序——先多图，再单图，最后视频。预测哪些基准会下降以及原因。

4. O artigo relata que os benchmarks de vídeo treinados em apenas 8 quadros por amostra. Isso se generaliza para vídeos de 30 segundos na inferência?
   | 论文报告视频基准只用每样本8帧训练。这对推理时的30秒视频泛化吗？先崩溃的是 token 预算还是时序推理？

5. A combinação bilinear de 24x24 patches para 12x12 é uma redução de 4x por dim. Implementar a combinação em stdlib Python e verificar que a média sobre cada bloco 2x2 corresponde à saída bilinear.
   | 将 24x24 补丁双线性池化为 12x12 是每维 4 倍缩减。用标准库 Python 实现池化，验证每个 2x2 块的均值与双线性输出一致。

## Termos-chave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| OneVision scenario | "Single-image, multi-image, or video" | One of three input shapes the unified VLM handles; the budget stays constant across | 统一 VLM 处理的三种输入形态之一，预算在场景间保持恒定 | |
| Token budget | "How many tokens per sample" | Total visual tokens the LLM sees per training / inference sample, typically 3000-4000 | LLM 每样本看到的总视觉 token 数，通常 3000-4000 | |
| Curriculum | "Training order" | Stage ordering (single-image → multi-image → video) chosen for emergent transfer | 课程学习：按单图→多图→视频顺序训练，促进技能迁移 | |
| Bilinear pooling | "Token shrink" | Applying bilinear interpolation to the patch grid (2D) to reduce token count while preserving locality | 在补丁网格上做双线性插值，减少 token 数并保留空间局部性 | |
| Emergent skill | "Not trained, still works" | Capability that appears at inference without matching training data, due to curriculum composition | 课程学习组合带来的未训练即涌现的能力 | |
| AnyRes-k | "k-tile setup" | k sub-tiles of fixed resolution plus one thumbnail, typical k ∈ {4, 9} | k 个固定分辨率子切片加一个缩略图 | |
| Task transfer | "Cross-scenario generalization" | Skills learned on single-image that apply to video (and vice versa) via shared backbone | 通过共享骨干网络，单图技能迁移到视频（反之亦然） | |

## Mais leitura 延伸阅读

- [Li et al. — LLaVA-OneVision (arXiv:2408.03326)](https://arxiv.org/abs/2408.03326)O que é que é que é o que é que é?
- [LLaVA-OneVision-1.5: Fully Open Framework (arXiv:2509.23661)](https://arxiv.org/abs/2509.23661)- É uma versão totalmente aberta.
- [Lin et al. — Video-LLaVA (arXiv:2311.10122)](https://arxiv.org/abs/2311.10122)♬ Video-LLAVA                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
- [Lin et al. — VILA (arXiv:2312.07533)](https://arxiv.org/abs/2312.07533)O que é que é isso?
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191)Qwen2-VL em relação à referência
