# Documentos e Diagramas Compreensão  arquivo e gráfico Compreensão

> Os documentos não são fotos. Um PDF, documento científico, faturamento ou formulário manuscrito tem um layout, tabelas, diagramas, notas de rodapé, cabeçalhos e estrutura semântica que a compreensão de imagens simples não pode capturar. A pilha pré-VLM era um pipeline: Tesseract OCR + LayoutLMv3 + heurísticas de extracção de tabela. A onda VLM substituiu os modelos sem OCR  Donut (2022), Nougat (2023), DocLLM (2023)  que emitem marcas estruturadas diretamente. Em 2026, a fronteira é apenas "alimentar a imagem da página para Claude Opus 4.7 em 2576px nativo", e a saída de marcação estruturada vem gratuitamente. Esta lição lê o arco de três eras da IA de documentos.

> **【中文解读】**文档不是照片──PDF、论文、发票、手写表单有布局、表格、图表、脚注、标题等语义结构,普通图像理解无法捕捉──文档 AI 经历了三个时代:(1) OCR 管道(Tesseract + LayoutLMv3);(2) OCR-free(Donut、Nougat 直接从图像生成结构化输出);(3) VLM 原生(2026年直接将页面图像给Claude Opus 4.7 即可)

> **【拓展：文档理解在金融领域的应用】**金融场景是文档 AI最重要的应用领域之一:发票解析(自动提取供应商、金额、税率) 、合同审查(条款比对、风险标记) 、财务报表提取(资产负债表、利表的结构化数据抽取) 、KYC 文档处理身份(证券、营业执照的自动识别) ⋅ 2026 年推方案:纯印发票用 LayoutLMv3 ◎成本低),混合文档用手写VLM 原生(PaliGemma 2 或 Qwen2.5-VL),监管场景用OCR + VLM 交叉验证──

**Type:** Build
**Languages:** Python (stdlib, layout-aware document parser skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 5 (NLP)
**Time:** ~180 minutes

> - Não .**【前置】**O primeiro é o primeiro, que é o primeiro, que é o primeiro, que é o primeiro, que é o segundo.
> - Não .**【类比】**O OCR é um sistema de análise de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados
> ️ **【易错点】**简单 OCR 任务用VLM = 杀用牛刀(成本10倍) ;;例如纯文本发票用Tesseract + LayoutLMv3 只需几分钱,使用GPT-4V 要几毛钱──修复:先评估任务复杂度,简单的OCR管道,复杂的(手写、混合布局、多语言)才上VLM──

## Objetivos de aprendizagem

- Explique as três eras da IA de documentos: OCR pipeline, OCR-free, VLM-native.
  Tradução do inglês para tradução livre: OCR 管道、无 OCR、VLM 原生──
- Descreva os três fluxos de entrada do LayoutLMv3: texto, layout (bbox), patches de imagem, com mascaragem unificada.
  中文翻译:描述 LayoutLMv3 的三个输入流:文本、布局(bbox)、图像补丁,配合统一掩码──
- Compare Donut (livre de OCR, imagem → marcação), Nougat (papel científico → LaTeX), DocLLM (generativo de layout), PaliGemma 2 (nativo VLM).
  Não há nenhuma informação sobre o que é um "dout" ou um "dout"
- Escolha um modelo de documento para uma nova tarefa (facturas, trabalhos científicos, formulários manuscritos, recibos chineses).
  Tradução em chinês:为新任务选择文档模型 (新任务选择文档模型)

## O problema é o problema da introdução

"Entender este PDF" é enganosamente difícil.

> "Compreender este PDF" parece simplesmente difícil.

- Conteúdo de texto (90% do sinal).
  Tradução do idioma:文本内容 (90% das informações)
- Layout (títulos, notas de rodapé, barras laterais, formato de duas colunas).
  Tradução do inglês: 布局 (→ "Bíbricas")
- Tablas (linhas, colunas, células combinadas).
  Tradução do inglês para o inglês:
- Figuras e diagramas.
  Tradução do inglês:
- Anotativas manuscritas.
  Tradução do português:
- Fontes e tipografia (título vs corpo).
  Tradução em inglês:字体和排版

O OCR bruto descarta o texto e perde o resto. Um sistema que se importa com as faturas precisa saber "Total: $1.245" veio da parte inferior à direita, não de uma nota de rodapé.

> O OCR original apenas tira o texto, perde o resto das informações.

## O conceito central.

> **【中文解读】**文档和图表理解是多模态 AI 重要应用场景:OCR、表格提取、流程图解读、公式识别等──关键技术:高分辨率输入 (Reserving Script Clarity) 版面分析 (Reserving Script Clarity) 版面分析 (Reserving Text) 版面分析 (Reserving Text) 版面分析 (Reserving Text) 版面分析 (Reserving Text) 版面分析 (Reserving Text) 版面分析 (Reserving Text) 版) 版面分析 (Reserving Text) 版面分析 (Reserving Text) 版面分析 (Reserving Text) 版) 版面分析 (Reserving Text) 版面分析 (Reserving Text) 版 (Reserving Text) 版 (Reserving Text) 版 (Reserving Text) 版 (Reserving Text) 版 (Reserving Text) 版 (Reserving Text) 版 (Reserving Text) 版 (Reserving Text) 版 (Reserving Text) 版 (Reserving) 版 (Reserving) 版) 版 (Reserving) 版 (Reserving) 版 (Reserving) 版) 版 (Reserving) 版 (Reserving) 版 (Reserving) 版) 版 (Reserving) 版 (R) 版 (R) 版 (R) 版 (R) 版 (R) 版 (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R)

> **【拓展：文档 AI 的工业应用**文档 AI 市场巨大:合同审核、发票处理、学术论文分析等──GPT-4o no DocVQA alcançou 92,8%,InternVL2-26B alcançou 92,7%(open source optimum)──MarkItDown (Microsoft) vai transformar o seu documento em Markdown,ColPali usando o método de visão para substituir o tradicional OCR 管线──


> **【拓展：文档理解的技术路线】**文档理解有两条路线:(1) OCR-first(先用 OCR 提取文本,再用 LLM 处理)适合纯文文文文档;(2) Vision-first(直接用 VLM 处理文档图像)适合包含图表、表格的复杂版面──GPT-4o 和 InternVL2 走 Vision-first 路线,在复杂文档理解上表现更好──


### Era 1  OCR (antes de 2021)

A pilha clássica:

> 经典技术:

1. PDF → imagem por página.
   Tradução do português:PDF → Cada página
2. O Tesseract (ou OCR comercial) extrai texto com caixas de limite por palavra.
   Chinese:Tesseract (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tess) (Tesseract) (Tesseract) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess)
3. O analisador de layout identifica blocos (título, tabela, parágrafo).
   Tradução do inglês para o português: 布局分析器识别块
4. Reconhecedor de estrutura de tabela paralisa tabelas.
   Tradução do inglês para tradução inglesa:表格结构识别器解析表格──
5. Regras de domínio + campos de extração de regex.
   Tradução do inglês: 字段提取.

Funciona para texto impresso limpo. Fugas na escrita, digitalização distorcida, tabelas complexas, scripts não-inglês.

> 适用于清洁印刷文本──在手写、倾斜扫描、复杂表格、非英语文字上失败──每种失败模式都需要自定义异常处理──

### TrOCR (2021)

TrOCR (Li et al., arXiv:2109.10282) substituiu o clássico CNN-CTC da Tesseract por um transformador encoder-decoder treinado em imagens de texto sintéticas + reais.

> TrOCR utilizado em sintetizar + real text images on training de Transformer 编码器-解码器 substituiu o clássico CNN-CTC de Tesseract.

### Era 2  Livre de OCR (2022-2023)

Os primeiros modelos sem OCR disseram: "Salte a detecção inteiramente, mapeie os pixels de imagem para a saída estruturada diretamente".

> Primeiro modelo de OCR não apresentado: totalmente saltando de inspecção, diretamente irá mapear imagens para o estruturado de saída.

Donut (Kim et al., arXiv:2111.15664):
- Transformador de codificador-decodificador, codificador é Swin-B.
- A saída é JSON para compreensão de formulários, marcação para resumo ou qualquer esquema específico de tarefa.
- Sem OCR, sem layout, sem detecção.

> Donut:编码器-解码器 Transformer,编码器为Swin-B──输出是 JSON(表单理解)、markingdown(摘要) 或任务特定方案──无需 OCR、无需布局、无需检测──

Nougat (Blecher et al., arXiv:2308.13418):
- Formada especificamente em artigos científicos.
- A saída é LaTeX / markdown.
- Manuseia equações, layout de colunas múltiplas, figuras.
- O modelo que cada arXiv-parser chama.

> Nougat: especializado em treinos em artigos científicos.

São especialistas, não generalistas. O donut num artigo científico falha; o nougat numa fatura falha.

> Estes são modelos de especialistas, não são de talento.

### LayoutLMv3 (2022)

Uma faixa diferente. LayoutLMv3 (Huang et al., arXiv:2204.08387) mantém OCR mas adiciona compreensão de layout:

> Não é igual. LayoutLMv3 Mantém OCR, mas adicione o layout compreender:

- Três fluxos de entrada: tokens de texto OCR, caixas de limite 2D por token, parches de imagem.
  中文翻译:三个输入流:OCR 文本代币、 cada token de 2D 边界框、图像补丁──
- Objectivo de formação mascarada em todas as três modalidades (texto mascarado, parches mascarados, layout mascarado).
  Tradução do inglês: 藏语语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏: 藏: 藏语: 藏: 藏语: 藏: 藏: 藏: 藏: 藏: 藏: 藏语: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏:
- A seguir: classificação, extração de entidades, tabela QA.
  Tradução do inglês para o inglês:

LayoutLMv3 é o auge da compreensão de documentos baseados em OCR. Forte em formulários e faturas. Requer OCR upstream. Melhor precisão pré-VLM em referências padronizadas de documentos.

> LayoutLMv3 é o pico de compreensão de documentos baseados em OCR.

### DocLLM (2023)

DocLLM (Wang et al., arXiv:2401.00908) é o irmão gerador do LayoutLM. Gera respostas de forma livre condicionadas a tokens de layout. Melhor para QA em documentos; ainda depende da entrada de OCR.

> O DocLLM é um LayoutLM de gerado de dados.

### Era 3  VLM-nativo (2024+)

2024 VLMs tornou-se bom o suficiente para substituir o gasoduto inteiramente.

> Em 2024, o VLM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

- LLaVA- NEXT 336-tile AnyRes funciona para pequenos documentos.
  中文翻译:LLaVA-NeXT 336-tile AnyRes 适用于小文档。
- Qwen2.5VL de resolução dinâmica lida com 2048+ pixels nativo.
  Tradução do inglês:Qwen2.5-VL 动态分辨率原生处理 2048+ 像素。
- Claude Opus 4.7 suporta documentos de 2576px.
  中文翻译:Claude Opus 4.7 支持 2576px 文档。
- PaliGemma 2 (abril de 2025) treina especificamente para documentos + escrita à mão.
  中文翻译:PaliGemma 2(2025 年 4 月) especializada em treino de arquivos + escrita em mão.

A lacuna entre o VLM-nativo e o OCR-pipeline foi rapidamente encerrada.

> A diferença entre o VLM original e o OCR se reduz rapidamente. Até 2026, o VLM original está em:

- Texto de cena (escrito à mão + impresso, scripts mistos).
  中文翻译:场景文本(手写+印刷,混合文字)
- Tablas complexas com células fundidas.
  Tradução do inglês: 带合并单元格的复杂表格.
- Equações matemáticas incorporadas no texto.
  Tradução do inglês: 嵌入文本的数学公式──
- Figuras com anotações de texto.
  Tradução do inglês:

Os gasodutos OCR continuam a ganhar:

> O OCR 管道 ainda está em vantagem nos seguintes aspectos:

- Cargas de trabalho de escaneamento puro em escala maciça onde a latência por página importa.
  Tradução do inglês: Masselha puro扫描工作负载,每页延迟很重要──
- Confiabilidade do gasoduto (falhas deterministas versus alucinações VLM).
  Tradução do português: "Beixa" (Beixa)
- Ambientes regulamentados que exigem uma saída de OCR auditável.
  Tradução do inglês para tradução do inglês: needs可审计 OCR 输出监管环境──

### A fronteira Claude 4.7 / GPT-5

Com entrada nativa de 2576 pixels, os VLMs de fronteira documentam a compreensão com precisão quase humana.

> Em 2576 像素原生输入下, VLM de frente para aproximar a taxa de precisão do ser humano fazer o documento de compreensão.

- DocVQA: Claude 4.7 ~ 95,1, PaliGemma 2 ~ 88,4, Nougat ~ 77,3, Layout em tubulaçãoLMv3 ~ 83.
  Noutros países, a produção de produtos de qualidade é muito mais alta do que a produção de produtos de qualidade.
- ChartQA: Claude 4.7 ~ 92,2, GPT-4V ~ 78.
  中文翻译:ChartQA:Claude 4.7 约 92.2,GPT-4V 约 78。
- VisualMRC: Claude 4.7 ~ 94.
  Tradução do português:MRC visual:Claude 4.7 约 94。

O espaço entre os modelos fechados é principalmente de resolução e escala LLM base. Os modelos abertos em 7B estão alguns pontos atrás, mas conseguem alcançar.

> A diferença entre o modelo de código aberto e o modelo de código aberto está a ser alcançada.

### Equações matemáticas e saída de LaTeX

Os trabalhos científicos precisam de exata saída de LaTeX para equações. Nougat foi treinado sobre isso. VLMs treinados com metas LaTeX (Qwen2.5-VL-Math, derivados de Nougat) produzem LaTeX utilizável. Sem treinamento explícito LaTeX, VLMs produzem transcrições legíveis, mas imprecisas.

> O estudo científico precisa de um formulário de LATEX 公式输出──Nougat 在此上训练──使用LATEX 目标训练的VLM(Qwen2.5-VL-Math、Nougat 衍生物) para produzir um LATEX (LATEX) disponível──没有明显LATEX 训练的VLM 产生可读但不精确的转录──

Para os canais de papel científico em 2026: cadeia Nougat no PDF, depois um VLM em páginas complicadas.

> 2026 年科学论文管道建议:先用Nougat 处理 PDF,再用VLM 处理棘手页面──

### Escrita à mão

Ainda é a sub-tarefa mais difícil. A impressão mista + escrita à mão (notificações de médicos, formulários preenchidos) é onde os canais de OCR ainda superam os VLM em custo.

> 依然是最难的子任务──印刷+手写混合(医生笔记、填写的表单) 依然是 OCR管道在成本上仍然胜胜了VLM的场景──纯手写VLM 正在改进(Claude 4.7、PaliGemma 2)──

### 2026 receita

Para um novo projecto de IA documental:

>  para novos projetos de IA:

- Faturas impressas em escala: LayoutLMv3 + regras, custo-eficiente.
  Tradução do inglês: LayoutLMv3 + 规则,成本高效──
- Documentos mistos (científicos + manuscritos + formulários): nativos do VLM (PaliGemma 2 ou Qwen2.5-VL).
  中文翻译:混合文档(科学+手写+表单):VLM 原生(PaliGemma 2 或 Qwen2.5-VL) 』
- Ingestão completa do arXiv: Nougat para matemática, VLM para números.
  Tradução do português:完整 arXiv 处理:Nougat 处理数学,VLM 处理图表。
- Regulatório: OCR pipeline + VLM validador para verificação cruzada.
  Tradução do inglês: 监管场景: OCR 管道 + VLM 验证器交叉检查──

## Use-o com o framework implementado.
```figure
mm-doc-layout
```

## Usá-lo

`code/main.py`- Não .

- Um tokenizer de brinquedo consciente de layout: dado (texto, bbox) pares, produz a entrada de estilo LayoutLMv3.
  Tradução do inglês para inglês: LayoutLmv3 风格的输入──
- Um gerador de esquema de tarefa de estilo Donut: modelo JSON para formulários.
  Não há nenhum tipo de programa de missão.
- Uma comparação de orçamentos de tokens por página em toda a pipeline OCR, Donut, Nougat e VLM-native.
  OCR 管道、Donut、Nougat 和 VLM 原生之间每页代币 预算的比较──

## Envia-o . Produto .

Esta lição produz`outputs/skill-document-ai-stack-picker.md`- Tendo em conta um projecto de IA de documentos (domínio, escala, qualidade, regulamentação), escolha entre o pipeline de OCR, o especialista livre de OCR e o VLM nativo.

> 本课产 出 `outputs/skill-document-ai-stack-picker.md` fornecer documentos sobre os projetos de IA (à escala, à escala, à qualidade e à supervisão), entre os canais de OCR e os VLM.

## Exercícios.

1. O seu projeto é de 10 milhões de faturas por dia. Qual pilha minimiza o custo por página sem perder precisão?

2. Por que o LayoutLMv3 supera os CLIP-VLMs puros no formulário QA, mas tem um desempenho inferior no texto de cena? O que o stream bbox desiste? Por que o LayoutLMv3 em expressão única QA 上优于纯 CLIP VLM, mas em cena?

3. Nougat gera LaTeX. Propõe um caso de teste onde a saída nativa de VLM vence a Nougat na fidelidade de LaTeX, e um caso onde a Nougat vence. Nougat 生成 LaTeX.

4. Leia o artigo PaliGemma 2 (Google, 2024). Qual foi a adição de dados-treinamento chave que levantou a precisão do documento versus PaliGemma 1?

5. Desenhar um híbrido regulatório-seguro: OCR pipeline como primário, VLM como secundário cross-check. Como você resolver o desacordo?

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| OCR pipeline | "Tesseract-style" OCR 管道 | Stage-wise stack: detect -> OCR -> layout -> rules; deterministic, fragile 分阶段栈：检测→OCR→布局→规则；确定但脆弱 | |
| OCR-free | "Donut-style" 无 OCR | Image-to-output transformer that skips explicit OCR; single model 图像到输出的 Transformer，跳过显式 OCR；单一模型 | |
| Layout-aware | "LayoutLM" 布局感知 | Input includes per-token bbox coordinates; unified masking across modalities 输入包含逐 token 的 bbox 坐标；跨模态统一掩码 | |
| VLM-native | "Frontier VLM" VLM 原生 | Feed page image directly to Claude/GPT/Qwen VLM at high resolution; no pipeline 直接将页面图像输入高分辨率 VLM；无需管道 | |
| DocVQA | "Doc benchmark" 文档 VQA 基准 | Document VQA standard; most-cited score 文档 VQA 标准评测；被引用最多的评分 | |
| Markup output | "LaTeX / MD" 标记输出 | Structured output format instead of free-form text; enables downstream automation 结构化输出格式而非自由文本；支撑下游自动化 | |

## Mais leitura 延伸阅读

- [Li et al. — TrOCR (arXiv:2109.10282)](https://arxiv.org/abs/2109.10282)
- [Blecher et al. — Nougat (arXiv:2308.13418)](https://arxiv.org/abs/2308.13418)
- [Huang et al. — LayoutLMv3 (arXiv:2204.08387)](https://arxiv.org/abs/2204.08387)
- [Kim et al. — Donut (arXiv:2111.15664)](https://arxiv.org/abs/2111.15664)
- [Wang et al. — DocLLM (arXiv:2401.00908)](https://arxiv.org/abs/2401.00908)
