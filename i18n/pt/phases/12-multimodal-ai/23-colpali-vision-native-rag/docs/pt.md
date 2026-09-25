# ColPali e Visão-Nativo Document RAG  ColPali 视觉原生文档 RAG

> O RAG tradicional paralisa PDFs em texto, divide em pedaços, incorpora pedaços, armazena vetores. Cada passo perde o sinal: OCR deixa cair os dados do gráfico, o fragmentação rompe as linhas da tabela, os incorporados de texto ignoram os números. ColPali (Faysse et al., Julho 2024) fez a pergunta mais simples: por que extrair texto? Embed a imagem da página diretamente através do PaliGemma, use a interação tardia de estilo ColBERT para recuperação e mantenha todos os layout, figuras, fontes e sinal de formatação que o documento carrega. Referências publicadas: 20-40% melhor precisão de ponta a ponta do que o texto-RAG em documentos ricos em visão. O ColQwen2, o ColSmol e o VisRAG alargaram o padrão. Esta lição lê a tese RAG visual nativa e constrói um pequeno índice ColPali-like.

> **【中文解读】**Tradicional RAG em PDF desempenho ruim, porque cada passo está em perda de sinal: OCR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

> **【拓展：ColPali 在金融 RAG 中的应用】**O relatório financeiro é o mais típico de vídeo rico documentárioQ3  O aumento de receita geralmente ocorre em gráficos, os blocos de assinatura de contratos são fatos de estrutura e não fatos de texto. ColPali  diretamente embutidos em imagens de página, mantendo um sinal visual completo, muito adequado a relatórios financeiros, contratos, emissão, etc. Casoes─O estoque de distribuição é de cerca de 5-10 vezes o texto RAG, mas a elevação na taxa de precisão geralmente atinge esse custo.

**Type:** Build
**Languages:** Python (stdlib, multi-vector indexer + MaxSim scorer)
**Prerequisites:** Phase 11 (LLM Engineering — RAG basics), Phase 12 · 05 (LLaVA)
**Time:** ~180 minutes

> - Não .**【前置】**學本节前请先掌握:Fase 11·14-16(RAG 基础:embedding/chunking/retrieval) 、Fase 11·13(ColBERT 延迟交互检索,ColPali 直接借鉴) 、Fase 12·05(LLaVA 视觉编码器) ――ColPali = "ColBERT para imagens"―
> - Não .**【类比】**传统 RAG vs ColPali = "看书先扫描成纯文本" vs "直接看图找答案"──传统 = OCR 提取文字→分块→embedding(图表数据全部丢失);ColPali = 直接对页面图像做补丁嵌入(图表、表格、布局全保留)── em documentos de "图表为王" em relatório financeiro, ColPali 准确率高 20-40%──

## Objetivos de aprendizagem

- Explique a diferença entre a recuperação de bi-encoder (um vetor por documento) e a recuperação de interação tardia (muitos vetores por documento).
  Tradução do inglês para tradução do inglês: 文文翻译:解释双编码器检查((每文档一个向量) 和延迟交互检查(每文档多个向量) 的区别──
- Descreva a operação MaxSim do ColBERT e como o ColPali a generaliza de tokens de texto para correções de imagem.
  中文翻译:描述 ColBERT's MaxSim 操作以及 ColPali 如何将其从文本代币 推广到图像补丁──
- Construa um pequeno índice ColPali: página → inserções de patch → MaxSim sobre inserções de query term → top-k páginas.
  中文翻译:构建一个微型 ColPali 式索引器:页面→patch 嵌入→对查询词嵌入做MaxSim→top-k 页面。
- Compare o gerador ColPali + Qwen2.5VL versus texto-RAG + GPT-4 em um caso de uso de faturas / relatórios financeiros.
  中文翻译:在发票/金融报告用例上比较 ColPali + Qwen2.5-VL 生成器 vs 文本 RAG + GPT-4──

## O problema é o problema da introdução

O texto-RAG em PDFs descarta a maior parte do documento. O crescimento de receita do terceiro trimestre de um relatório financeiro é geralmente em um gráfico; as conclusões de um relatório médico são em imagens anotadas; o bloco de assinatura de um contrato legal é um fato de layout, não um fato de texto.

> O texto do PDF acima RAG  desistiu da maior parte das informações do arquivo. O aumento de receita do Q3 do relatório financeiro geralmente está no gráfico; as descobertas do relatório médico são marcadas em imagem; o bloco de assinatura do contrato legal é um fato de estrutura, não um fato de texto.

O canal de texto-RAG:

> 文本 RAG 管道:

1. PDF → texto através de OCR / pdftotext.
   中文翻译:PDF → 通过 OCR/pdftotext 提取文本。
2. Texto → 300-500 pedaços de tokens.
   Chinese: 中文翻译:文本 → 300-500 tokens 的块──
3. Chunk → bi-encoder embutida (um vetor).
   中文翻译:块 → 双编码器嵌入(一个向量) 』
4. Pergunta de usuário → inserção → semelhança cosínica → pedaços top-k.
   中文翻译: user quer quer quer → 嵌入 → 余弦相似度 → top-k 块──
5. Câncer + consulta → Mestrado em Direito.
   中文翻译:块 + 查询 → LLM。

Cinco passos perdidos, gráficos não capturados, tabelas divididas em pedaços, layout de várias colunas aplanado, anotações de figuras desaparecem.

> 五有损步骤──图表未捕获──图表被块截截切──多布局被展平──图表注释消失──

Corrigir com o ColPali: pular o OCR, incorporar a imagem da página diretamente. Use interação tardia no estilo ColBERT para recuperação para que o modelo possa atender a correções de grãos finos no momento da consulta.

> ColPali Modification: Salta OCR, directamente embutida em imagem de página. Utilize ColBERT 风格的延迟交互进行检查, para que o modelo possa concentrar-se no parche de menor dimensão durante a consulta.

## O conceito central.

> **【中文解读】**ColPali usa o método de visão pura para implementar RAG: não através de OCR, diretamente embaixar a página do arquivo como imagem codificada para a quantidade, com visão de semelhança de pesquisa.

> **【拓展：视觉原生 RAG 的优势**传统RAG管线(OCR -> 文本 -> 嵌入 -> 检索) 在复杂版面面(表格、图表、公式) 上经常失败──ColPali 直接在视觉层次匹配,无需OCR,在包含图表和表格的文档检索上上上传统方法提升 30-50%──缺点是需要更多存储(每页一个向量)──


> **【拓展：ColPali 的效率分析】**ColPali em retardo de pesquisa é equivalente ao método tradicional (cerca de 50ms/questão), mas a taxa de precisão em arquivos que contêm gráficos e modelos aumentou 30-50%. O fator é que o custo de armazenamento de índices é maior.


### Colbert (2020)

ColBERT (Khattab & Zaharia, arXiv:2004.12832) é um método de recuperação de texto. Em vez de um vetor por documento, ele produz um vetor por token.

> Colbert é um método de pesquisa de texto não é um dos seus movimentos, mas sim um dos seus movimentos.

- Os tokens de consulta têm as suas próprias incorporações (vectores N_q).
  Tradução do inglês: quer query token  get your own嵌入 (N_q 个向量)
- Os tokens de documento recebem embutidos (vectores N_d, normalmente armazenados em cache).
  O símbolo de arquivo é um símbolo de arquivo de arquivo.
- Score = soma sobre os tokens de consulta de max sobre os tokens de documento de similaridade cosínea: Σ_i max_j cos(q_i, d_j).
  Por exemplo, a palavra "question token" significa "question token" ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question token) ou "question token" (question) ou "question token" (question) ou "question token" (question) ou "question) ou "question token" (question) ou "question "question" (question) " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "

Esta é a operação MaxSim. Cada token de consulta "põe" o seu melhor correspondente documento token.

> É o que MaxSim faz. Cada token de consulta seleciona o seu melhor correspondente.

Pros: forte recall, lida com semântica de nível de termo. Cons: N_d vetores por documento, armazenamento caro.

> 优势:强召回率,处理词级语义――劣势:每文档 N_d 个向量,存储昂贵――

### ColPali

ColPali (Faysse et al., arXiv:2407.01449) aplica o padrão ColBERT às imagens.

> ColPali vai usar o modelo ColBERT para imagens.

- Cada página é codificada pelo PaliGemma (linguagem ViT +) em embutidos de correio: N_p vetores por página.
  中文翻译:每页由 PaliGemma(ViT + 语言)编码为补丁 嵌入: 每页 N_p 个向量──
- Cada consulta de usuário (texto) é codificada em embutidos de query-token: vetores N_q.
  Tradução do inglês para o inglês:
- Score = Σ_i max_j cos(q_i, p_j), ou seja, MaxSim sobre query-text-tokens e page-image-patches.
  中文翻译:分数 = Σ_i max_j cos(q_i, p_j),即查询文本代币 和页面图像补丁的 MaxSim。
- Retirando as páginas de topo por pontuação total.
  Tradução do inglês:

No momento da ingestão de documentos: embebebedar cada página com PaliGemma, armazenar todas as incorporações de patch. No momento da consulta: embebedar os tokens de consulta, calcular MaxSim contra todas as incorporações de página armazenadas, retornar páginas top-k.

> 文档摄取时: Use PaliGemma 嵌入每页,存储所有补丁 嵌入――查询时:嵌入查询代币,对所有存储的页面嵌入计算MaxSim,返回顶-k页面──

Pros: end-to-end supera o texto-RAG em 20-40% em documentos visualmente ricos. Cada patch-vector capta o layout e o conteúdo local.

> 优势:端到端在视觉丰富文档上文 RAG 高 20-40%──每补丁 向量捕获局部布局和内容──

Desvantagens: N_p patches × 4 bytes flutuantes × D-dim vectores por página = armazenamento cresce rapidamente. Mitigado pela quantização PQ / OPQ.

> 劣势:N_p 个补丁 × 4 字节浮点 × D 维向量每页 = 储存快速增长──可通过 PQ/OPQ 量化缓解──

### ColQwen2 e ColSmol

ColQwen2 (illuin-tech, 2024-2025) troca PaliGemma por Qwen2-VL. Melhor codificador base, melhor recuperação.

> O ColQwen2 vai substituir o PaliGemma por o Qwen2-VL.

O ColSmol é a variante de menor escala para uso local / borda. Um retriever ColSmol com parâmetros ~ 1B é executado em GPU de consumo.

> ColSmol é um variante de menor escala de uso em locais/margens.

### VisRAG

VisRAG (Yu et al., arXiv:2410.10594) é uma variante diferente: em vez de MaxSim em patches, agrupar cada página em um único vetor com um VLM e, em seguida, recuperar bi-encoder.

> VisRAG é uma variação diferente: não em patch, mas com VLM, cada página será reformulada em um único veículo re-dobrar o código de busca.

A compensação qualidade/custo: ColPali para qualidade, VisRAG para escala.

> O valor da produção e do custo: ColPali  buscam a qualidade, VisRAG  buscam a dimensão¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

### M3DocRAG

M3DocRAG (Cho et al., arXiv:2411.04952) estende a recuperação multimodal para o raciocínio multimodal de várias páginas.

> M3DocRAG vai ampliar o multimodelo de pesquisa para várias páginas de documentos.

### ViDoRe  o índice de referência

O ColPali é um banco de referência para a avaliação visual de recuperação de documentos. As tarefas incluem relatórios financeiros, artigos científicos, documentos administrativos, registros médicos, manuais.

> O ColPali é um dos principais organismos de investigação e de investigação da área da saúde.

ColPali-v1 marca ~80% nDCG@5 no ViDoRe; texto-RAG nos mesmos documentos marca ~50-60%.

> ColPali-v1 em ViDoRe 上約80% nDCG@5;文本RAG 在同一文档上約50%-60%──

### O gasoduto RAG de ponta a ponta

Para um RAG nativo de visão:

> 视觉原生 RAG 管道:

1. Ingest: PDF → imagens de página → codificação PaliGemma → armazenar todos os incorporados de correio.
   中文翻译:摄取:PDF → 页面图像 → PaliGemma 编码 → 存储所有补丁 嵌入──
2. Query: texto de usuário → embutidos de tokens de consulta → MaxSim contra todas as páginas indexadas → páginas top-k.
   Chinese: 查询: user文本 → 查询 token 嵌入 → 对所有索引页面做MaxSim → top-k 页面──
3. Gerar: imagens de página top-k + consulta → VLM (Qwen2.5-VL ou Claude) → resposta.
   中文翻译:生成:top-k 页面图像 + 查询 → VLM(Qwen2.5-VL 或 Claude)→ 回答。

Não há OCR em nenhum lugar, figuras, gráficos, fontes, layout tudo fluem para a resposta.

> O programa de trabalho é um programa de trabalho de trabalho de todos os Estados Unidos.

### Matemática de armazenamento

Um relatório financeiro de 50 páginas com 729 patches por página e embutidos em 128 dimensões:

> 50 páginas relatório financeiro, por página 729 patch, 128 dimensões:

- ColPali: 50 * 729 * 128 * 4 bytes = ~ 18 MB crus, ~ 4 MB após PQ.
  中文翻译:ColPali:50 * 729 * 128 * 4 字节 = 约18 MB 原始,PQ 后约4 MB。
- Text-RAG: 50 pedaços * 768-dim * 4 bytes = ~ 150 kB.
  中文翻译:文本 RAG:50 块 * 768 维 * 4 字节 = 约150 kB。

O ColPali é ~ 30x mais armazenamento por documento. Em escala, o OPQ / PQ reduz-o para ~ 5-10x, geralmente tolerável.

> ColPali Cada arquivo de armazenamento é de cerca de 30 vezes.

### Quando o texto-RAG ainda vence

- Documentos de texto puro sem sinal de layout (articles wiki, logs de chat).
  Não há nenhuma forma de fazer isso.
- Arquivos de milhões de páginas onde o armazenamento domina o custo.
  Tradução do inglês:
- Requisitos regulamentares rigorosos que exigem texto extraível de OCR ao lado da recuperação.
  OCR 文本与检索并存的监管要求.

Para tudo o mais em 2026  relatórios financeiros, artigos científicos, contratos legais, registros médicos, documentação UX  RAG vision-native ganha.

> 2026 ano todos os outros cenários 金融報告、科学论文、法律合同、医疗记录、UX 文档视觉原生 RAG 胜出──

## Use-o com o framework implementado.
```figure
mm-maxsim
```

## Usá-lo

`code/main.py`- Não .

- Encoder de patch de brinquedo: mapeia uma "página" (pequena grade de vetores de características) para uma série de inserções de patch.
  Tradução do inglês: 编码器:将"页面" (tr征向量小网格)映射为补丁 (emparelhamento) 嵌入数组 (emparelhamento)
- Scorer MaxSim: calcula a pontuação de estilo ColBERT entre um conjunto de inserção de token de consulta e um conjunto de patches de página.
  Tradução do inglês:MaxSim 评分器:计算查询 token 嵌入集和页面补丁集 集之间 ColBERT 风格分数──
- Indica 5 páginas de brinquedos, faz 3 consultas, retorna o top-k com pontuações.
  Tradução do inglês:Index 5 个玩具页面,运行 3 个查询,返回带分数的顶-k――

## Envia-o . Produto .

Esta lição produz`outputs/skill-vision-rag-designer.md`. Tendo em conta um projecto de documento-RAG, escolhe ColPali / ColQwen2 / VisRAG / text-RAG e dimensionar o armazenamento.

> 本课产 出 `outputs/skill-vision-rag-designer.md` 给定文档 RAG 项目,选择 ColPali / ColQwen2 / VisRAG / 文本 RAG 并估算存储──

## Exercícios.

1. Um relatório anual de 200 páginas em 729 parches por página, 128-dim emb, 4 bytes flutuantes. Computa armazenamento bruto e armazenamento com compressão PQ (8x). 200 páginas anual.

2. MaxSim é Σ_i max_j cos(q_i, p_j). O que esta soma captura que uma semelhança média simples não? MaxSim é Σ_i max_j cos(q_i, p_j) ⋅

3. ColPali indexa páginas como conjuntos de patches. Que mudanças se nós, em vez de indexar no nível da palavra (como ColBERT faz)? trade-offs? ColPali 以 patch 集索引页面──如果改为词级索引(如 ColBERT),会怎么?有什么取舍?

4. Desenhar o pipeline de ponta a ponta para um corpus de 1M de página com um orçamento de latência de 500ms por consulta. Escolher ColQwen2 / VisRAG e justificar.

5. Leia M3DocRAG (arXiv:2411.04952). Descreva o padrão de atenção de várias páginas e como ele difere da recuperação de ColPali de uma única página.

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Late interaction | "ColBERT-style" 延迟交互 | Retrieval using per-token or per-patch embeddings + MaxSim, not a single doc vector 使用逐 token/patch 嵌入 + MaxSim 的检索，非单向量 | |
| MaxSim | "Max-over-patches" 最大相似度 | For each query token, pick the highest-similarity document token; sum across query 对每个查询 token 选最高相似度的文档 token；跨查询求和 | |
| Bi-encoder | "Single-vector" 双编码器 | One vector per document; faster but loses granularity 每文档一个向量；更快但丢失粒度 | |
| Multi-vector | "Many-vectors-per-doc" 多向量索引 | Store N_p vectors per document / page; storage cost grows but recall improves 每文档/页存储 N_p 个向量；存储增长但召回提升 | |
| Patch embedding | "Page feature" 图像块嵌入 | One vector per image patch from a VLM encoder, cached per page VLM 编码器输出的每 patch 一个向量，按页缓存 | |
| ViDoRe | "Vision doc bench" 视觉文档检索基准 | ColPali's benchmark suite for visual document retrieval ColPali 的视觉文档检索基准套件 | |
| PQ quantization | "Product quantization" 乘积量化 | Compression that maintains vector similarity while shrinking storage ~8x 保持向量相似度的同时压缩存储约 8 倍 | |

## Mais leitura 延伸阅读

- [Faysse et al. — ColPali (arXiv:2407.01449)](https://arxiv.org/abs/2407.01449)
- [Khattab & Zaharia — ColBERT (arXiv:2004.12832)](https://arxiv.org/abs/2004.12832)
- [Yu et al. — VisRAG (arXiv:2410.10594)](https://arxiv.org/abs/2410.10594)
- [Cho et al. — M3DocRAG (arXiv:2411.04952)](https://arxiv.org/abs/2411.04952)
- [illuin-tech/colpali GitHub](https://github.com/illuin-tech/colpali)
