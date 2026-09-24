# ASCII Art y la cárcel visual Breaks .

> Jiang, Xu, Niu, Xiang, Ramasubramanian, Li, Poovendran, "ArtPrompt: ataques de jailbreak basados en arte ASCII contra LLM alineados" (ACL 2024, arXiv:2402.11753). Enmascarar los tokens relevantes para la seguridad en una solicitud perjudicial, reemplazarlos con renderizaciones ASCII-art de las mismas letras, y enviar el aviso enmascarado. GPT-3.5, GPT-4, Gemini, Claude, Llama-2 no pueden reconocer con fuerza los tokens de arte ASCII. El ataque evita los filtros de perplejidad, las defensas de paráfrases y la retokenización. Relacionado: el índice de referencia ViTC mide el reconocimiento de las instrucciones visuales no semánticas; StructuralSleight generaliza a estructuras codificadas con texto poco comunes (árboles, gráficos, JSON anidados) como una familia de ataques de codificación.

> **【中文解读】**Este episodio presenta ASCII 艺术视觉越狱用文本图形绕过安全过器的攻击技术──ArtPrompt(ACL 2024)

> **【拓展：ArtPrompt → 编码攻击家族】**标准防御 (困惑度过、释义、重新分词) en ArtPrompt 上全部失败, porque el sistema de seguridad está en orden牌/语义级操作, mientras que ArtPrompt en el visual recognition级操作。StructuralSleight va a promover esto hasta raros en la estructura de código de texto (UTES) 树、图、嵌套 JSON、CSV-in-JSON Cualquier estructura de seguridad de entrenamiento en datos raros pero de modelos resuelibles puede ocultar contenido nocivo―

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, ArtPrompt token-masking harness) | **语言:** Python（标准库，ArtPrompt token 掩码框架）
**Prerequisites:** Phase 18 · 12 (PAIR), Phase 18 · 13 (MSJ) | **前置知识:** Phase 18 · 12 (PAIR), Phase 18 · 13 (MSJ)
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 18·12-13──视觉越狱 = 用 ASCII 艺术/树状图/JSON 等编码攻击绕过文本过器──
> ¿ Qué es esto ?**【类比】**ASCII 越狱 = "隐形墨水"。安全过器看无害的标点网格,模型视觉理解为一个词──ArtPrompt ACL 2024:GPT-4/Gemini/Claude/Llama-2 全失败,>75% 攻击成功率──绕过PPL 过、改写、重代币 化防御──结构性变种(StructuralSleight) expand to tree/图/嵌套 JSON所有非语义视觉提示都是攻击面──

## Objetivos de aprendizaje

- Describa el ataque ArtPrompt: paso de identificación de palabras, sustitución ASCII-art, último aviso enmascarado.

> 描述 ArtPrompt 攻击:词识别步骤、ASCII 艺术替换、最终伪装提示──

- Explica por qué las defensas estándar (PPL, Paraphrase, Retokenization) fallan en ArtPrompt.

> 解释为什么标准防御(困惑度过、释义、重新分词) en ArtPrompt 上失败──

- Define el VTC y describa lo que mide.

> definición de ViTC并描述其衡量内容──

- Describa StructuralSleight como una generalización a estructuras codificadas con texto poco comunes arbitrarias.

> 描述 StructuralSleight 作为对任意罕见文本编码结构的推广──

## El problema es el problema .

Los ataques a través de la paráfrase y el juego de roles (lección 12) y a través del contexto largo (lección 13) operan en el patrón a nivel de texto. ArtPrompt opera en el nivel de reconocimiento: el modelo no analiza el token prohibido. analiza una imagen renderizada en caracteres. El filtro de seguridad ve puntuación inofensiva. El modelo ve una palabra.

> 通过释义和角色扮演(Leyón 12) 和长上下文(Leyón 13) de ataques en el patrón de texto de nivel operativo。ArtPrompt en el patrón de reconocimiento de nivel operativo: modelo no resuelve órdenes prohibidas, sino resuelve en imágenes de caracteres 染──安全过器看无害的标点符号──模型看一个词──

## El concepto.

> **【中文解读】**ArtPrompt 两步攻击的细节:第一步给定有害请求,使用LLM 识别安全相关词(如"bomba"在"how to make a bomb"中);第二步将每个识别的词换为其ASCII 艺术染(7x5 o 7x7 字符块形成字母形状) ;; el modelo recibe es un señalización y un vuelo en red, el modelo suficientemente fuerte para identificar palabras; seguridad 过器只看网格;;

### ArtPrompt, dos pasos

Paso 1. Identificación de palabras. Dado un pedido dañino, el atacante utiliza un LLM para identificar las palabras relevantes para la seguridad (por ejemplo, "bomba" en "cómo hacer una bomba"). 

Paso 2. Generación de Prompt encubierta. reemplaza cada palabra identificada con su renderización ASCII-art (un bloque de caracteres 7x5 o 7x7 que forman la forma de la letra). El modelo recibe una cuadrícula de puntuación y espacios que un modelo suficientemente capaz puede reconocer como la palabra; un filtro de seguridad sólo ve la cuadrícula.

Resultado: GPT-4, Gemini, Claude, Llama-2, GPT-3.5 todos fallan. tasa de éxito de ataque superior al 75% en su subconjunto de referencia.

> Resultado:GPT-4、Gemini、Claude、Llama-2、GPT-3.5 全部失败── ataque de éxito en el grupo de base de más del 75%──

> **【拓展：防御失败 → 多层安全启示】**困惑度过器失败是因为合法结构化输入也得分高;释义失败是因为释义 LLM 常保留或重建 ASCII 艺术;重新分词失败是因为识别是视觉的而不是令牌级的──安全必须泛化到模型能解析的所有结构化表示

### Por qué las defensas estándar fallan

- **PPL (perplexity filter).**El arte ASCII tiene una alta perplejidad  pero también lo hace toda entrada nueva.

> **困惑度过滤。**ASCII 艺术有高困惑度但所有新输入也是如此──阻止ArtPrompt的值选择也阻止了合法的结构化输入──

- **Paraphrase.**Parafrasear el prompt destruye el arte ASCII. En la práctica, los LLM parafrase a menudo preservan o reconstruyen el arte.

> **释义。**释义提示会破坏 ASCII 艺术── en realidad, 释义 LLM 常常保留或重建艺术──

- **Retokenization.**Dividir los tokens de manera diferente no cambia que la visión del modelo es reconocer las formas de letras.

> **重新分词。**Diferentes números de la letra no cambian el modelo de la visión en el hecho de que la forma de la letra se identifica.

El problema subyacente es que los filtros de seguridad son de nivel token o semántico; ArtPrompt opera en el nivel de reconocimiento visual.

> 根本问题是安全过器在令牌或语义级操作;ArtPrompt在视觉识别级操作;;

> **【中文解读】**ViTC 基准:ArtPrompt's eficacia与模型读取视觉文本的能力相关ViTC 准确率越高,ArtPrompt 越有效。这是一个能力-安全权衡:提升模型的多模态理解能力会同时增加编码攻击的脆弱性──视觉 LLM(GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) amplió el ataque a la superficie de las imágenes reales de ArtPrompt 式攻击比ASCII 艺术更强──

### Indicador de referencia de ViTC

Reconocimiento de las instrucciones visuales no semánticas. Medir la capacidad del modelo para leer ASCII-art, wingdings y otros contenidos visuales no-texto-semánticos. La efectividad de ArtPrompt se correlaciona con la precisión de ViTC: cuanto mejor lee el modelo texto visual, mejor ArtPrompt trabaja en él.

> La eficacia de ArtPrompt se relaciona con el índice de precisión de ViTC: el modelo de lectura de un texto visual es mejor, el efecto de ArtPrompt es mejor.

### EstructuralSleight

ArtPrompt generaliza: estructuras codificadas en texto (UTES) poco comunes. árboles, gráficos, JSON anidados, CSV-en-JSON, bloques de código de estilo diferente. Si una estructura es rara en el entrenamiento de datos de seguridad pero puede ser analizada por el modelo, puede ocultar contenido dañino.

> 推广 ArtPrompt: rare text text text code structure(UTES) ―― tree、图、嵌套 JSON、 JSON en el CSV、diff 风格代码块── Si una estructura es rara en el entrenamiento de datos de seguridad pero el modelo se resuelve, puede ocultar contenido nocivo──

La implicación de la defensa: la seguridad debe generalizarse a través de las representaciones estructuradas que el modelo puede analizar.

> 防御启示: seguridad debe generalizarse a todos los modelos que pueden ser resueltos.

### Análogo de modalidad de imagen

Los LLM visuales (GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) amplían la superficie de ataque. Los ataques de estilo ArtPrompt con imágenes reales son más fuertes que los análogos de arte ASCII porque los codificadores de imágenes producen una señal más rica.

> 视觉 LLM 扩展了攻击面──使用实际图像的ArtPrompt 式攻击比ASCII 艺术更强,因为图像编码器产生更丰富的信号──

### Donde esto encaja en la Fase 18

Las lecciones 12-14 describen tres vectores de ataque ortogonales: refinamiento iterativo (PAIR), longitud de contexto (MSJ) y codificación (ArtPrompt/StructuralSleight). La lección 15 cambia de ataques centrados en el modelo a ataques de los límites del sistema (injección de inmediato indirecto).

> Lecciones 12-14  describir tres formas de ataque: 代改进 (PAIR) 、上下文长度 (MSJ) 和编码 (编码) (ArtPrompt/StructuralSleight) ⋅ Lección 15 描述防御工具响应──

> **【拓展：视觉 LLM → 攻击面扩展】**视觉 LLM(GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) amplió el ataque face.

## Usalo.
```figure
al-ascii-cloak
```

## Usalo

`code/main.py`Puede ocultar palabras específicas en una consulta dañina con glifos de arte ASCII, verificar que la cadena encubierta pasa un filtro de palabras clave y (opcionalmente) descifrar la cadena encubierta de nuevo usando un reconocedor simple.

> `code/main.py`Construir un juego ArtPrompt。 puedes usar ASCII 艺术字形伪装有害查询中的特定词,验证伪装字符串通过关键词过,并(可选地) usando simplemente identificador解码。

## Envíalo .

Esta lección produce`outputs/skill-encoding-audit.md`. Dado un informe de defensa contra jailbreak, enumera las familias de ataques de codificación cubiertas (art ASCII, base64, leet-speak, homoglif UTF-8, UTES) y la capa de defensa que captura cada uno.

> 本课产 出  `outputs/skill-encoding-audit.md` Informar sobre la defensa de la prisión, incluir la capa de código de ataque y cada capa de defensa de la respuesta.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Verifique si la cadena encubierta pasa por un simple filtro de palabras clave.

2. Implemente una segunda codificación: base64 para la misma palabra objetivo. Compara la velocidad de bypass del filtro con ArtPrompt y la dificultad de recuperación.

3. Lea Jiang et al. 2024 Sección 4.3 (resultados de cinco modelos). Propón una razón por la que la resistencia a ArtPrompt de Claude es mayor que la de Géminis en el mismo índice de referencia.

4. Diseñar una defensa de pre-generación que detecte regiones en forma de arte ASCII en el instante. Medir la tasa de falso positivo en código legítimo, tablas y notación matemática.

5. StructuralSleight enumera 10 estructuras de codificación. Esbozar una defensa generalizada que maneje las 10 y estimar el costo de cálculo por instante defendible.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| ArtPrompt | "the ASCII-art attack" | Two-step jailbreak that masks safety words with ASCII-art renderings |
| Cloaking | "hide the word" | Replace a forbidden token with a visual representation the model reads but the filter does not |
| UTES | "uncommon structure" | Uncommon Text-Encoded Structure — tree, graph, nested JSON, etc. used to smuggle content |
| ViTC | "visual-text capability" | Benchmark for model's ability to read non-semantic visual encoding |
| Perplexity filter | "PPL defense" | Reject prompts with high perplexity; fails because legitimate structured input also scores high |
| Retokenization | "tokenizer shift defense" | Pre-process the prompt with a different tokenizer; fails because recognition is visual |
| Homoglyph | "lookalike characters" | Unicode characters that look identical to Latin letters; bypass substring checks |

## Más Leer más Leer más

- [Jiang et al. — ArtPrompt (ACL 2024, arXiv:2402.11753)](https://arxiv.org/abs/2402.11753) el papel de jailbreak de arte ASCII
- [Li et al. — StructuralSleight (arXiv:2406.08754)](https://arxiv.org/abs/2406.08754) Generalización de las UTES
- [Chao et al. — PAIR (Lesson 12, arXiv:2310.08419)](https://arxiv.org/abs/2310.08419) ataque iterativo complementario
- [Anil et al. — Many-shot Jailbreaking (Lesson 13)](https://www.anthropic.com/research/many-shot-jailbreaking) ataque de longitud complementaria
