# ASCII Arte e Prisões Visuais

> Jiang, Xu, Niu, Xiang, Ramasubramanian, Li, Poovendran, "ArtPrompt: Ataques de Jailbreak baseados em arte ASCII contra LLM alinhados" (ACL 2024, arXiv:2402.11753). Mascarar os tokens relevantes para a segurança em um pedido prejudicial, substituí-los por renderização ASCII-art das mesmas letras, e enviar o aviso disfarçado. GPT-3.5, GPT-4, Gemini, Claude, Llama-2 todos falham em reconhecer robustamente os tokens de arte ASCII. O ataque contorna PPL (filtros de perplexidade), defesas de paráfrase e retokenization. Relacionado: o ViTC benchmark mede o reconhecimento de pedidos visuais não semânticos; StructuralSleight generaliza para estruturas incomuns codificadas por texto (árvores, gráficos, JSON aninhados) como uma família de ataques de codificação.

> **【中文解读】**Este capítulo introduziu ASCII 艺术视觉越狱文本图形绕过安全过器的攻击技术──ArtPrompt(ACL 2024) 两步攻击:识别安全相关词,使用 ASCII 艺术染替换──安全过器看无害的标点符号网格,模型看一个词──GPT-4、Gemini、Claude、Llama-2 全部失败,攻击成功率超过75%──

> **【拓展：ArtPrompt → 编码攻击家族】**标准防御 (困惑度过、释义、重新分词) é um erro completo no ArtPrompt, pois a segurança de um sistema é uma operação de nível de instrução/linguagem, enquanto a segurança de um sistema é uma operação de nível de reconhecimento visual.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, ArtPrompt token-masking harness) | **语言:** Python（标准库，ArtPrompt token 掩码框架）
**Prerequisites:** Phase 18 · 12 (PAIR), Phase 18 · 13 (MSJ) | **前置知识:** Phase 18 · 12 (PAIR), Phase 18 · 13 (MSJ)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**學本節前 請先掌握:Fase 18·12-13──視觉越狱 = 用 ASCII 艺术/树状图/JSON 等编码攻击绕过文本过器──
> - Não .**【类比】**ASCII 越狱 = "隐形墨水"。安全过器看无害的标点网格,模型视觉理解为一个词──ArtPrompt ACL 2024:GPT-4/Gemini/Claude/Llama-2 全失败,>75% 攻击成功率──绕过PPL 过、改写、重代币 化防御──结构性变种(StructuralSleight) expand to tree/图/嵌套 JSON所有非语义视觉提示都是攻击面──

## Objetivos de aprendizagem

- Descreva o ataque ArtPrompt: passo de identificação de palavras, substituição ASCII-art, final de encoberta de prompt.

> 描述 ArtPrompt 攻击:词识别步骤、ASCII 艺术替换、最终伪装提示──

- Explique por que as defesas padrão (PPL, Paraphrase, Retokenization) falham no ArtPrompt.

> 解释为什么标准防御(困惑度过、释义、重新分词) em ArtPrompt 上失败──

- Defina o ViTC e descreva o que ele mede.

> definição ViTC并描述其衡量内容──

- Descreva StructuralSleight como uma generalização para estruturas arbitrárias incomuns codificadas por texto.

> Descrição de StructuralSleight como uma promoção para qualquer rara textbook codificação de estrutura.

## O problema é o problema .

Os ataques por meio de parafrase e jogo de roteiro (Lessão 12) e por meio de longo contexto (Lessão 13) operam no padrão de nível de texto. ArtPrompt opera no nível de reconhecimento: o modelo não analisa o token proibido. Ele analisa uma imagem renderizada em caracteres. O filtro de segurança vê pontuação inofensiva. O modelo vê uma palavra.

> 通过释义和角色扮演(Lessão 12) 和长上下文(Lessão 13) de ataques em padrão de texto operação。ArtPrompt 在识别级操作:模型不解析禁止令牌,而是解析以字符染的图像──安全过器看无害的标点符号──模型看一个词──

## O conceito .

> **【中文解读】**ArtPrompt 两步攻击的细节:第一步给定有害请求,使用LLM 识别安全相关词(如"bomba"在"how to make a bomb"中);第二步将每个识别的词换为其ASCII 艺术染(7x5或7x7 字符块形成字母形状) ;; o modelo recebe é de sinais e空格网格, modelo suficientemente forte para poder identificar palavras; segurança 过器只看网格;;

### ArtPrompt, dois passos

Passo 1. Identificação de palavras. Dado um pedido prejudicial, o atacante usa um LLM para identificar as palavras relevantes para a segurança (por exemplo, "bomba" em "como fazer uma bomba"). 

Passo 2. Geração de Prompt encoberta. Substitua cada palavra identificada com sua representação de arte ASCII (um bloco de caracteres 7x5 ou 7x7 formando a forma da letra). O modelo recebe uma grade de pontuação e espaços que um modelo suficientemente capaz pode reconhecer como a palavra; um filtro de segurança vê apenas a grade.

Resultado: GPT-4, Gemini, Claude, Llama-2, GPT-3.5 todos falham. Taxa de sucesso de ataque acima de 75% em seu subconjunto de referência.

> Resultado: GPT-4、Gemini、Claude、Llama-2、GPT-3.5 全部失败──ataque de sucesso em grupos de base superior a 75%──

> **【拓展：防御失败 → 多层安全启示】**困惑度过器失败是因为合法结构化输入也得分高;释义失败是因为释义 LLM 常保留或重建 ASCII 艺术;重新分词失败是因为识别是视觉的而不是令牌级的──安全必须泛化到模型能解析的所有结构化表示

### Por que as defesas padrão falham

- **PPL (perplexity filter).**A arte ASCII tem uma alta perplexidade  mas também todas as entradas novas.

> **困惑度过滤。**ASCII 艺术有高困惑度但所有新输入也是如此──阻止ArtPrompt的值选择也阻止了合法的结构化输入──

- **Paraphrase.**Parafrasear o prompt destrói a arte ASCII. Na prática, parafrase LLM muitas vezes preservam ou reconstruem a arte.

> **释义。**释义提示会破坏 ASCII 艺术── na prática, 释义 LLM 常常保留或重建艺术──

- **Retokenization.**Dividir os tokens de forma diferente não muda que a visão do modelo esteja reconhecendo formas de letras.

> **重新分词。**Diferentes divisões não alteram o modelo de visão em reconhecimento de letras forma facto.

O problema subjacente é que os filtros de segurança são de nível token ou semântico; o ArtPrompt opera no nível de reconhecimento visual.

> 根本问题是安全过器在令牌或语义级操作; ArtPrompt在视觉识别级操作.

> **【中文解读】**ViTC 基准:ArtPrompt's efficacité与模型读取视觉文本的能力相关ViTC 准确率越高,ArtPrompt 越有效。 é uma capacidade-segurança: aumentar a capacidade de compreensão de vários modos do modelo ao mesmo tempo que aumenta a vulnerabilidade do código de ataque。

### Indicador de referência ViTC

Reconhecimento de pedidos visuais não semânticos. Medem a capacidade do modelo de ler ASCII-art, wingdings e outros conteúdos visuais não-texto-semânticos. A eficácia do ArtPrompt correlaciona com a precisão ViTC: quanto melhor o modelo lê texto visual, melhor o ArtPrompt trabalha nele.

> Não-linguística                                                                                                                                                                                                                                                             

### EstruturaSleight

Generaliza ArtPrompt: Estruturas incomuns codificadas por texto (UTES). Árvores, gráficos, JSON aninhado, CSV-in-JSON, blocos de código de estilo diferente. Se uma estrutura é rara no treinamento de dados de segurança, mas pode ser analisada pelo modelo, ela pode esconder conteúdo prejudicial.

> 推广 ArtPrompt: Raramente observado em textos de código de estrutura (UTES) ⋅ tree、图、嵌套 JSON、 JSON CSV、diff 风格代码块── Se uma estrutura é rara em dados de segurança treinados, mas o modelo é resolutivo, pode ocultar conteúdo nocivo──

A implicação da defesa: a segurança deve generalizar-se através das representações estruturadas que o modelo pode analisar.

> 防御启示: segurança deve generalizar-se para todos os modelos que podem ser resolvidos.

### Análogo de modalidade de imagem

Os LLM visuais (GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) ampliam a superfície de ataque. Ataques de estilo ArtPrompt com imagens reais são mais fortes do que os análogos de arte ASCII porque os codificadores de imagens produzem um sinal mais rico.

> 视觉 LLM 扩展了攻击面──使用实际图像的ArtPrompt 式攻击比ASCII 艺术更强,因为图像编码器产生更丰富的信号──

### Onde isto encaixa na Fase 18

As lições 12-14 descrevem três vetores de ataque ortogonais: refinamento iterativo (PAIR), comprimento de contexto (MSJ) e codificação (ArtPrompt/StructuralSleight). A lição 15 muda de ataques centrados no modelo para ataques de fronteira do sistema (injeção de prompt indireta).

> Lições 12-14  Descrição de três formas de ataque: 代改进 (PAIR) 、上下文长度 (MSJ) 和编码 (ArtPrompt/StructuralSleight) ⋅ Lição 15   模型中心攻击转向系统边界攻击── Lição 16 描述防御工具响应──

> **【拓展：视觉 LLM → 攻击面扩展】**视觉 LLM(GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) expandiram a face de ataque.

## Usa-o. Usa-o.
```figure
al-ascii-cloak
```

## Usá-lo

`code/main.py`Você pode encobrir palavras específicas em uma consulta prejudicial com glifos de arte ASCII, verificar que a cadeia encoberta passa por um filtro de palavra-chave e (opcionalmente) decodificar a cadeia encoberta de volta usando um reconhecedor simples.

> `code/main.py`Construir um brinquedo ArtPrompt。 você pode usar ASCII 艺术字形伪装有害查询中的特定词,验证伪装字符串通过关键词过,并(可选地) usando simples identificadores解码。

## Envia-o .

Esta lição produz`outputs/skill-encoding-audit.md`. Dado um relatório de defesa contra jailbreak, ele enumera as famílias de ataques de codificação cobertas (arte ASCII, base64, leet-speak, homoglifos UTF-8, UTES) e a camada de defesa que capta cada um.

> 本课产 出 `outputs/skill-encoding-audit.md` Foram fornecidos relatórios de defesa da prisão, lista de codificação abrangente das famílias de ataques e cada nível de defesa de resposta.

## Exercícios.

1. Corra .`code/main.py`Verifique se a cadeia encoberta passa por um simples filtro de palavras-chave.

2. Implementar uma segunda codificação: base64 para a mesma palavra-alvo. Compare a taxa de ultrapassagem do filtro com o ArtPrompt e a dificuldade de recuperação.

3. Leia Jiang et al. 2024 Seção 4.3 (resultados de cinco modelos). Propõe uma razão pela qual a resistência ArtPrompt de Claude é maior do que a de Gémeos no mesmo índice de referência.

4. Desenhar uma defesa de pré-geração que detecte regiões em forma de arte ASCII no prompt. Medir a taxa de falso positivo em código legítimo, tabelas e notação matemática.

5. StructuralSleight lista 10 estruturas de codificação. Esboce uma defesa generalizada que lida com todas as 10 e estimar o custo de computação por prompt defendido.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| ArtPrompt | "the ASCII-art attack" | Two-step jailbreak that masks safety words with ASCII-art renderings |
| Cloaking | "hide the word" | Replace a forbidden token with a visual representation the model reads but the filter does not |
| UTES | "uncommon structure" | Uncommon Text-Encoded Structure — tree, graph, nested JSON, etc. used to smuggle content |
| ViTC | "visual-text capability" | Benchmark for model's ability to read non-semantic visual encoding |
| Perplexity filter | "PPL defense" | Reject prompts with high perplexity; fails because legitimate structured input also scores high |
| Retokenization | "tokenizer shift defense" | Pre-process the prompt with a different tokenizer; fails because recognition is visual |
| Homoglyph | "lookalike characters" | Unicode characters that look identical to Latin letters; bypass substring checks |

## Mais leitura 延伸阅读

- [Jiang et al. — ArtPrompt (ACL 2024, arXiv:2402.11753)](https://arxiv.org/abs/2402.11753)O papel de jailbreak da ASCII-art
- [Li et al. — StructuralSleight (arXiv:2406.08754)](https://arxiv.org/abs/2406.08754) Generalização de UTES
- [Chao et al. — PAIR (Lesson 12, arXiv:2310.08419)](https://arxiv.org/abs/2310.08419) ataque iterativo complementar
- [Anil et al. — Many-shot Jailbreaking (Lesson 13)](https://www.anthropic.com/research/many-shot-jailbreaking) Ataque de comprimento complementar
