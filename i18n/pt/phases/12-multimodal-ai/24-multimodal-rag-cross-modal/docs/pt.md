# Multimodal RAG e Cross-Modal Retrieval .

> O documento RAG é uma fatia. A RAG multimodal de produção vai mais amplo  a recuperação de texto, imagens, áudio e vídeo para fluxos de trabalho como planejamento de viagens ("encontrar-me um brunch vegano tranquilo com luz natural"), triagem médica ("o que a lesão corresponde a esta foto + essas notas"), comércio eletrônico ("vestimentos semelhantes a esta selfie, no meu tamanho"), e serviço de campo ("diagnóstico este som do motor mais foto da parte"). Três pesquisas de 2025  Abootorabi et al., Mei et al., Zhao et al.  codificou os subproblemas: recuperação transmodal, fusão de recuperação, fixação da geração, avaliação multimodal. Esta lição lê as pesquisas e desenha um pipeline de produção.

> **【中文解读】**O RAG ultrapassa o requisito de pesquisa de documentos únicos, necessitando de pesquisas em textos, imagens, áudio, vídeos, para planejamento de viagens, clínicas, e-commerce, serviços em locais de trabalho, etc. Em 2025, três artigos de resumo definem quatro componentes: pesquisa de documentos únicos, pesquisa de dados, análise de dados, análise de dados, análise de dados, análise de dados, análise de dados, análise de dados, análise de dados, etc.

**Type:** Build
**Languages:** Python (stdlib, cross-modal retriever with fusion + grounded generator)
**Prerequisites:** Phase 12 · 23 (ColPali), Phase 11 (RAG basics)
**Time:** ~180 minutes

> - Não .**【前置】**O primeiro é o primeiro, que é o primeiro, que é o primeiro, que é o primeiro, que é o segundo.
> - Não .**【类比】**Doente diz "meu peito dói" (文本) + 给你看心电图 (图像) + 让你听心跳录音 (音频) 医生要同时检索医学文献 (文本) ♡心电图案库 (图像) ♡心跳声纹库 (音频) 融合多源信息后给出诊断 (诊断) 融合策略:分数融合 = 让分分分分分加权;注意力融合 = 专业融合 = 让分分分分加权; 专业融合 = 让分分分分加权; 专业融合 = 让分分分分分加权; 专业融合 = 专业融合 = 不同专业处理不同模态;;

## Objetivos de aprendizagem

- Desenho de recuperação transmodal: texto → imagem, imagem → texto, áudio → vídeo, etc.
  Tradução do inglês: design跨模态检索:文本→图像、图像→文本、音频→视频等──
- Comparar três estratégias de fusão: fusão de pontuação, fusão baseada na atenção, fusão MoE.
  Chinese Language Translation: Comparar três estratégias de integração:
- Explique a base de geração: como é que "citar as suas fontes" se as fontes são uma mistura de modalidades.
  Tradução do inglês para tradução do inglês: "Quando a origem é uma mistura de diferentes formas, a origem é uma mistura de diferentes formas".
- Cite as três pesquisas canônicas multimodal do RAG de 2025 e a sua taxonomia subproblemática.
  中文翻译:列举 2025 年三篇经典多模态 RAG 综述及其子问题分类──

## O problema é o problema da introdução

O RAG de modalidade única é um padrão resolvido: inserir consulta, inserir pedaços, recuperar, coisas em LLM. O RAG multimodal requer:

> 单模态 RAG 是已解决的模式:嵌入查询、嵌入块、检索、塞入 LLM──多模态 RAG 需要:

1. Múltiples cabeças de recuperação (cada modalidade precisa de inserções num espaço compatível).
   Tradução do inglês:                                                                                                                                                                                                                                                            
2. A fusão dos resultados de recuperação em diferentes modalidades.
   Tradução do inglês: transformational.
3. A geração de terra que cita fontes em todas as modalidades.
   Tradução do inglês: trans-modelo
4. Metricas de avaliação que cobrem o sinal transmodal.
   Tradução do inglês para tradução do inglês:

As pesquisas de 2025 chegam todas à mesma taxonomia.

> A análise geral de 2025 foi feita com a mesma classificação.

## O conceito central.

> **【中文解读】**跨模态 RAG  expandido tradicional texto RAG, apoiar vários modelos de pesquisa e geração: pode ser usado para pesquisa de texto imagens, usar imagens de pesquisa de texto, ou mistura de pesquisa de vários modelos de documentos.

> **【拓展：多模态 RAG 的应用**O sistema de regulação dos preços dos produtos de consumo tem um grande valor em áreas como a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde, a saúde e a saúde.


### Recuperação transmodal

Retirar documentos da modalidade B em resposta a uma consulta da modalidade A. Três padrões:

> 给定模态 A 的查询,检索模态 B 的文档──三种模式:

1. Espaço de inserção compartilhado. CLIP e CLAP produzem inserções de texto + imagem / texto + áudio em um espaço compartilhado. A semelhança de cosina entre modalidades funciona diretamente. Limitado a pares treinados CLIP.
   Tradução em inglês:共享嵌入空间──CLIP 和 CLAP 在共享空间产生文本+图像/文本+音频嵌入──跨模态余弦相似度直接有效──限于CLIP 训练过的配对──

2. Encoder de per-modalidade + tradução. Encoder de texto + encoder de imagem + um pequeno módulo de tradução mapeando entre espaços. Sen2Sen por Gupta et al. e outros projetos de 2024.
   Chinese: 每模态独立编码器 + 翻译──文本编码器 + 图像编码器 + 在空间间映射的小翻译模块──Sen2Sen等 2024年设计──灵活但增加复杂度──

3. O VLM como codificador. Use os estados ocultos de um VLM como a representação de recuperação. Qualquer modalidade que o VLM suporta funciona.
   中文翻译:VLM 作为编码器──使用VLM 隐藏状态作为检索表示──VLM 支持的任何模态都可用──质量更高,成本更高──

Opção: CLIP / SigLIP 2 para texto+imagem; CLAP para texto+áudio; VLM-estados ocultos para cross-modal em qualidade de fronteira.

> 选择建议:文本+图像用 CLIP/SigLIP 2;文本+音频用 CLAP;前沿质量跨模态用 VLM 隐藏状态──

### Estratégias de fusão

Você recuperou 10 resultados: 5 imagens, 3 passagens de texto, 2 áudio clips. Como você merge?

> Você procurou 10 resultados: 5 imagens, 3 episódios de texto, 2 episódios de som.

Fusão de pontuação (mais barata). Cada modalidade tem seu próprio retriever, cada um retorna pontuações. Normalize pontuações dentro da modalidade e depois soma.

> O modelo tem seu próprio pesquisador, cada um retorna ao seu próprio modelo.

Fusão baseada na atenção, concatenar todos os itens recuperados, deixar uma pequena rede de atenção pesá-los.

> Atenção concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração, concentração,

Fusão MoE. Gating de rotas de rede para especialistas específicos de modalidade. Diferentes tipos de consulta percorrem de forma diferente  uma pergunta visual pesa imagens mais altas.

> MoE 融合──门控网络路由到模态特定专家── diferentes tipos de consulta

Produzção padrão: pontuação de fusão com um leve viés em direção à modalidade dominante da consulta. Atualização para MoE se A / B mostra vitórias claras em seu domínio.

> O resultado é um resultado positivo, mas não é um resultado positivo.

> **【中文解读】**3 estratégias de integração: 1) Fusion de números  diferentes modelos de pesquisa  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação de números  Segmentação  Segmentação de números  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segmentação  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Segment  Seg

> **【拓展：多模态 RAG 的跨模态检索基础】**跨模态检索有三种模式:(1) 共享嵌入空间(CLIP/SigLIP 2 用图文,CLAP 用文本-音频);(2) 每模态独立编码器 + 翻译模块;(3) 用 VLM 隐藏状态作为检索表示──选择建议:文本+图像用 CLIP/SigLIP 2,文本+音频用 CLAP,跨模态前沿质量用 VLM 隐藏状态──

### Aterrização de geração

A MLL deve indicar qual item recuperado motivou cada reivindicação.

> O LLM 应引用哪个检索项驱动了每个声明.

- Fonte de texto: citação padrão `[1]`- Não .
  Tradução do português:`[1]`- Não.
- Fonte de imagem: `[img 3]`com uma legenda curta.
  Tradução do português:`[img 3]`附简短描述──
- Áudio: `[audio 2 at 0:34]`- Não .
  Tradução do idioma:`[audio 2 at 0:34]`- Não.

Treinar o gerador com dados de base: cada afirmação no alvo de treinamento é marcada com o índice de origem.

> Utilizando o gerador de dados de treinamento de percepção de terra: cada declaração do objetivo de treinamento é marcada por um código de referência.

### Os inquéritos de 2025

Abootorabi et al. (arXiv:2502.08826, "Ask in Any Modality"): taxonomia para RAG multimodal. Abrange recuperação, fusão, geração. Cobertura mais ampla.

> Abootorabi 等人:多模态 RAG 分类法──覆盖检索、融合、生成──覆盖最广──

Mei et al. (arXiv:2504.08748, "A Survey of Multimodal RAG"): concentra-se em benchmarks de sub-tarefa e modos de falha. Útil para o projeto de avaliação.

> Mei 等人: foco em tarefas básicas e modelo de fracasso.

Zhao et al. (arXiv:2503.18016): pesquisa focada na visão.

> Zhao 等人:聚焦视觉的综述──对 ColPali 系列工作覆盖深入──

A leitura de todos os três dá-lhe o estado da arte à primavera de 2025.

> 阅读全部三篇可获得2025年春最前沿状态―― a maioria dos problemas ainda está aberta―

### MuRAG  o documento de fundação

MuRAG (Chen et al., 2022) foi o primeiro RAG multimodal. Retirou imagem + texto de um KB multimodal, gerou respostas. Mostrou viabilidade antes da onda VLM. Sistemas modernos (REACT, VisRAG, M3DocRAG) construíram sobre isso.

> MuRAG é o primeiro multi-modelo RAG. De vários modelos de conhecimento, a base de pesquisa de imagens + texto, gerar respostas.

### Um exemplo de planeador de viagens de produção

Pergunta: "Encontre-me um almoço vegano tranquilo com luz natural".

> Pergunta: "Dê-me um pequeno-almoço tranquilo, com luz natural".

- O canal de condução:

> - O que é isso ?

1. Descompõe a consulta. "quiet" → palavra-chave de áudio/revisão; "vegan brunch" → item do menu; "luz natural" → recurso de imagem.
   中文翻译:分解查询──"安静"→音频/评论关键词;"纯素早午餐"→菜单项;"自然光"→图像特征──
2. Retirada por modalidade:
   Tradução do português:
   - Recuperação de texto em comentários: "brunch vegetariano, ambiente tranquilo".
     Tradução do português: "Pure素早午餐,安静氛围"
   - Retorno de imagem em fotos de restaurantes: "luz natural, ar".
     Tradução do português: "Naturalmente, há um grande número de pessoas que estão no meio da cidade".
   - Recuperação de áudio em clips de som ambiente: "baixo decibel, sem música".
     Tradução do português: ambiente som frequente: "低分贝,无音乐"
3. Cada restaurante tem uma pontuação composta.
   Tradução do inglês:融合分数──每个餐厅有综合分数──
4. Restaurantes Top-k → gerador VLM com todas as evidências → resposta com citações.
   中文翻译:Top-k 餐厅 → VLM 生成器(附所有证据)→ 带引用的回答──

Cada modalidade adiciona um sinal que só o texto perde.

> O que é muito mais do que um RAG? Cada modelo é adicionado apenas por sinais que o texto deixou de lado?

### Agentes de RAG multimodal

Multi-hop: se a primeira recuperação não retorna respostas de alta confiança, o LLM reformula e recupera novamente.

> Do jump: Se a primeira vez que o teste foi feito não retornar a resposta de alta confiança, LLM 重新表述并再次检索──Fase 14 de Agente RAG 模式在此适用── exemplo:

- Retrieve top-10 inicial → LLM pede "muito barulhento, filtro para <40 dB" → retrieve.
  Tradução do inglês para tradução livre:检索初始 top-10 → LLM 提问"太杂,过 <40 分贝" → 重新检索──
- Retrieve imagens → LLM vê que um tem um menu → retrieve o texto do menu → resposta.
  Tradução do inglês para tradução do inglês: 检索图像 → LLM 看到一张有菜单 → 检索菜单文本 → 回答。

Adiciona complexidade, mas lida com consultas que a recuperação de um só tiro não pode.

>  aumentar a complexidade mas pode tratar de uma única consulta não pode tratar de uma consulta

### Avaliação

A avaliação transmodal ainda é imatura.

> 跨模态评估 ainda não está maduro.

- Recall@k por modalidade.
  Tradução do inglês para o português:
- Precuração top-k combinada.
  Tradução do inglês:
- A satisfação de ponta a ponta, julgada pelo homem.
  Tradução do inglês:
- Função específica (reservas completas, compras feitas).
  Tradução do inglês para japonês:任务特定指标 (任务特定指标)

Não existe uma referência padrão que abranja todas as modalidades.

> 没有标准基准覆盖所有模态── a maioria dos artigos é avaliada em tarefas específicas de um domínio──

## Use-o com o framework implementado.
```figure
contrastive-matrix
```

## Usá-lo

`code/main.py`- Não .

- Três retrievers falsos (texto, imagem, áudio) operando em um corpo compartilhado de restaurantes.
  Tradução em inglês: 三模拟检索器 (三模拟检索器)
- Fusão de pontuação que combina pontuações de modalidade com pesos configuráveis.
  Tradução do inglês para tradução do inglês:
- Um botão de gerador que emite uma resposta final com citações.
  Tradução do inglês para tradução livre:
- Um simples ciclo agente que reformula a consulta se a confiança for baixa.
  Tradução do inglês para tradução inglesa:

## Envia-o . Produto .

Esta lição produz`outputs/skill-multimodal-rag-designer.md`- Uma especificação de produto com um fluxo de consulta multimodal, desenhos de retrievers, fusão, gerador e avaliação.

> 本课产 出 `outputs/skill-multimodal-rag-designer.md` Determine os modelos de pesquisa, as especificações dos produtos, os mecanismos de pesquisa de design, as estratégias de integração, os geradores e os programas de avaliação.

## Exercícios.

1. Propõe um RAG multimodal de triagem médica: consulta = foto de lesão + sintomas de texto. Que modalidades extrair de que KB? 设计医疗分诊多模态 RAG:查询 = 伤处照片 + 文字症状── quais modelos extrair de quais knowledgebacks?

2. A fusão de pontuação é uma soma ponderada simples. Que modo de falha tem que a fusão de MoE evita?

3. Leia a taxonomia de Abootorabi et al. (Seção 3). Quais são os três subproblemas canônicos e como eles se mapeam para o produto escolhido?

4. Desenhar uma especificação de avaliação para um RAG multimodal de planejamento de viagens. Que métricas cobrem a recall de imagem, a recall de áudio e a corretão composta?

5. O RAG multi-hop agente tem um imposto de latência por viagem de ida e volta. Em que dificuldade da consulta o ganho de precisão justifica a latência?

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Cross-modal retrieval | "Query one modality, retrieve another" 跨模态检索 | Text query retrieves images; image query retrieves text; requires a shared space or translator 文本查询检索图像；图像查询检索文本；需要共享空间或翻译器 | |
| Score fusion | "Combine scores" 分数融合 | Weighted sum of per-modality retrieval scores; simplest fusion 各模态检索分数的加权和；最简单的融合方式 | |
| MoE fusion | "Modality-routed experts" 混合专家融合 | Gating network picks which modality's scores to trust per query 门控网络按查询选择信任哪个模态的分数 | |
| Grounded generation | "Cite your sources" 接地生成 | Each claim in the answer tagged with the source index 回答中的每个声明都标注来源索引 | |
| MuRAG | "First multimodal RAG" 首个多模态 RAG | 2022 paper that established the multimodal RAG pattern 2022 年建立多模态 RAG 模式的论文 | |
| Agentic multi-hop | "Reformulate and retry" Agent 多跳 | LLM re-queries retrievers when first-pass confidence is low 首次检索置信度低时 LLM 重新查询检索器 | |

## Mais leitura 延伸阅读

- [Abootorabi et al. — Ask in Any Modality (arXiv:2502.08826)](https://arxiv.org/abs/2502.08826)
- [Mei et al. — A Survey of Multimodal RAG (arXiv:2504.08748)](https://arxiv.org/abs/2504.08748)
- [Zhao et al. — Vision RAG Survey (arXiv:2503.18016)](https://arxiv.org/abs/2503.18016)
- [Chen et al. — MuRAG (arXiv:2210.02928)](https://arxiv.org/abs/2210.02928)
- [Liu et al. — REACT (arXiv:2301.10382)](https://arxiv.org/abs/2301.10382)
