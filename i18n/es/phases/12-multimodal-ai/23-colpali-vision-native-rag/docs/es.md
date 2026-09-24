# ColPali y el documento nativo de visión RAG  ColPali 视觉原生文档 RAG

> RAG tradicional analiza los PDF en texto, se divide en trozos, incrusta trozos, almacena vectores. Cada paso pierde la señal: OCR deja caer los datos de los gráficos, la fragmentación rompe las filas de tablas, los embebidos de texto ignoran las cifras. ColPali (Faysse et al., julio 2024) hizo la pregunta más simple: ¿por qué extraer texto en absoluto? Embed la imagen de la página directamente a través de PaliGemma, utilice la interacción tardía de estilo ColBERT para la recuperación, y guarde toda la disposición, las figuras, las fuentes y la señal de formato que lleva el documento. Indicadores de referencia publicados: 20-40% mejor precisión de extremo a extremo que el texto-RAG en documentos ricos en imágenes. ColQwen2, ColSmol y VisRAG ampliaron el patrón. Esta lección lee la tesis de RAG nativo de la visión y construye un pequeño índice similar a ColPali.

> **【中文解读】**传统RAG en PDF es un poco peor, porque cada paso está en el error de señal:OCR 丢图表、分块破坏表格行、文本嵌入忽略图片。ColPali 问了一个更简单的问题:为什么要提取文本?直接使用PaliGemma 嵌入页面图像,使用ColBERT 风格的MaxSim 延迟交互进行检查,保留文档的全部布局、图表、字体和格式信号──在视觉丰富文档上,RAG 准确率高于文本 20-40%──

> **【拓展：ColPali 在金融 RAG 中的应用】**财报是最典型的视觉丰富文档Q3 营收增长通常在图表中, los bloques de firmas de contratos son hechos de diseño y no hechos de texto。ColPali 直接嵌入页面图像,保留完整的视觉信号,非常适合金融报告、合同、发票等场景──存储开销约为文本RAG的5-10 veces ((经PQ压缩后), pero en la tasa de precisión de la elevación de la valor suele obtener este costo。

**Type:** Build
**Languages:** Python (stdlib, multi-vector indexer + MaxSim scorer)
**Prerequisites:** Phase 11 (LLM Engineering — RAG basics), Phase 12 · 05 (LLaVA)
**Time:** ~180 minutes

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 11·14-16(RAG 基础:embedding/chunking/retrieval) Fase 11·13(ColBERT 延迟交互检索,ColPali 直接借鉴) Fase 12·05(LLaVA 视觉编码器) ――ColPali = "ColBERT para imágenes"―
> ¿ Qué es esto ?**【类比】**传统RAG vs ColPali = "看书先扫描成纯文本" vs "直接看图找答案"──传统 = OCR 提取文字→分块→embedding(图表数据全部丢失);ColPali = 直接对页面图像做补丁嵌入(图表、表格、布局全保留)──En los informes financieros, en los documentos de este tipo, ColPali 准确率高 20-40%──

## Objetivos de aprendizaje

- Explica la diferencia entre la recuperación de biencoder (un vector por documento) y la recuperación de interacción tardía (muchos vectores por documento).
  Traducción:Explanar dos codificadores de búsqueda de datos (en inglés) y diferencias entre los dos tipos de búsqueda de datos (en inglés) y los dos tipos de búsqueda de datos (en inglés).
- Describa la operación MaxSim de ColBERT y cómo ColPali la generaliza desde tokens de texto hasta parches de imagen.
  中文翻译: describe ColBERT's MaxSim 操作以及 ColPali 如何将其从文本代币 推广到图像补丁──
- Construir un pequeño índice similar a ColPali: página → embebedidos de parches → MaxSim sobre embebedidos de query term → páginas top-k.
  Construir un pequeño ColPali 式索引器:页面→patch 嵌入→对查询词嵌入做MaxSim→top-k 页面。
- Compare el generador ColPali + Qwen2.5VL con el texto-RAG + GPT-4 en un caso de uso de facturas / informes financieros.
  En el caso de los informes financieros, el sistema de gestión de los recursos humanos se utiliza para el desarrollo de la economía.

## El problema es la introducción del problema

El texto-RAG en los PDFs arroja la mayor parte del documento. El crecimiento de los ingresos del tercer trimestre de un informe financiero suele estar en un gráfico; los hallazgos de un informe médico están en imágenes anotadas; el bloque de firma de un contrato legal es un hecho de diseño, no un hecho de texto.

> El texto de los documentos de la RAG se deshace de la mayor parte de la información del archivo. El aumento de ingresos del tercer trimestre de los informes financieros se encuentra normalmente en el gráfico.

El sistema de texto-RAG:

> 文本 RAG 管道:

1. PDF → texto a través de OCR / pdftotext.
   En el texto de la página web se encuentra el texto de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web.
2. Texto → 300-500 trozos de tokens.
   En el caso de los ejemplos de la moneda, el valor de la moneda es de 300-500 euros.
3. Embedado de bi-encoder → Chunk (un vector).
   En el caso de los sistemas de codificación, el código de codificación es el código de codificación.
4. Encuesta de usuario → incrustado → cosino similaridad → top-k trozos.
   中文翻译: usuario查询 → 嵌入 → 余弦相似度 → top-k 块──
5. Unidad de trabajo + consulta → LLM.
   En inglés, el lenguaje de la lengua inglesa es el idioma de la lengua inglesa.

Cinco pasos perdidos, gráficos no capturados, tablas rotas en pedazos, diseño de múltiples columnas aplanadas, anotaciones de figuras desaparecen.

> 五有损步骤──图表未捕获──图表被块截截切──多布局被展平──图表注释消失──

Corrección de ColPali: omite OCR, embebegue la imagen de la página directamente. Utilice la interacción tardía de estilo ColBERT para la recuperación para que el modelo pueda atender a los parches de granos finos en el momento de la consulta.

> ColPali Modification: saltó OCR, directamente en la imagen de la página.

## El concepto central.

> **【中文解读】**ColPali utiliza un método de visión pura para implementar RAG: sin pasar por OCR, directamente enmarcar la página de archivo como un ímbolo codificado para la dimensión, con la búsqueda de similitud visual. La innovación central de ColPali es que cada token de la búsqueda de MaxSim se inserta en cada parche de la página de archivo para hacer la mayor similitud, y luego se busca y se aplica.

> **【拓展：视觉原生 RAG 的优势**传统RAG管线(OCR -> 文本 -> 嵌入 -> 检索) 在复杂版面(表格、图表、公式) 上经常失败──ColPali 直接在视觉层次匹配,无需OCR,在包含图表和表格的文档检索上上比传统方法提升 30-50%──缺点是需要更多存储(每页一个向量)──


> **【拓展：ColPali 的效率分析】**ColPali en la búsqueda tardía es equivalente al método tradicional (aproximadamente 50ms/cuestión), pero en los archivos que contienen gráficos y formularios la precisión aumentó del 30-50%. La falta es que el costo de almacenamiento de índices es más alto.


### El proyecto de ley

ColBERT (Khattab & Zaharia, arXiv:2004.12832) es un método de recuperación de texto. En lugar de un vector por documento, produce un vector por token.

> Colbert es un método de búsqueda de texto. No es un espectro de cada documento, sino un espectro de cada token.

- Los tokens de consulta obtienen sus propios embeddings (vectores N_q).
  En el caso de los ejemplos de la serie, el nombre de la serie se puede añadir a la serie de ejemplos de la serie.
- Los tokens de documentos obtienen embebidos (vectores N_d, típicamente almacenados en caché).
  En el caso de los archivos de archivo, el token de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archivo de archi
- Score = suma sobre las fichas de consulta de max sobre las fichas de documento de similitud cosina: Σ_i max_j cos(q_i, d_j).
  En el caso de los ejemplos de la serie de ejemplos de la serie de ejemplos de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de serie de la serie de serie de la serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de

Esta es la operación MaxSim. Cada token de consulta "escoge" su mejor token de documento.

> Es la operación de MaxSim. Cada token de consulta "Pick" su mejor correspondiente en el archivo.

Pros: fuerte recuerdo, maneja la semántica a nivel de términos.

> 优势:强召回率,处理词级语义――劣势:每文档 N_d 个向量, almacenamiento costoso――

### ColPali

ColPali (Faysse et al., arXiv:2407.01449) aplica el patrón ColBERT a las imágenes.

> ColPali va a utilizar el modelo ColBERT para imágenes.

- Cada página está codificada por PaliGemma (idioma ViT +) en embebedidos de parches: N_p vectores por página.
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la
- Cada consulta de usuario (texto) se codifica en embeddings de marcas de consulta: N_q vectores.
  En el texto original, el nombre de la página web se encuentra en el código de usuario.
- Score = Σ_i max_j cos(q_i, p_j), es decir, MaxSim sobre los tokens de texto de consulta y parches de imagen de página.
  En el texto original, el texto se encuentra en el código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de en en en en en en en en en en en en en en en en en en en en en en en en en en en en en en en en en en en en en.
- Recupera las páginas de primer nivel por puntaje total.
  Traducción:按总分检索 top-k 页面──

En el momento de ingestión de documentos: embebar cada página con PaliGemma, almacenar todas las incorporaciones de parches. En el momento de la consulta: embebar los tokens de consulta, calcular MaxSim contra todas las incorporaciones de página almacenadas, devolver páginas top-k.

> 文档摄取时: Usando PaliGemma 嵌入每页, almacenamiento todos los parches 嵌入──查询时:嵌入查询代币,对所有存储的页面嵌入计算MaxSim,返回顶-k页面──

Pros: de extremo a extremo supera el texto-RAG en un 20-40% en documentos ricos en visualización.

> 优势:端到端在视觉丰富文档上文 RAG Alto 20-40%── cada parche 向量捕获局部布局和内容──

Los inconvenientes: parches N_p × 4 bytes flotantes × vectores D-dim por página = almacenamiento crece rápidamente. Mitigado por la cuantización PQ / OPQ.

> 劣势:N_p 个补丁 × 4 字节浮点 × D 维向量每页 = 储存快速增长──可通过 PQ/OPQ 量化缓解──

### ColQwen2 y ColSmol

ColQwen2 (illuin-tech, 2024-2025) sustituye PaliGemma por Qwen2-VL. Mejor codificador de base, mejor recuperación.

> ColQwen2 reemplazará a PaliGemma por Qwen2-VL.

ColSmol es la variante a menor escala para uso local / borde. Un retriever ColSmol con ~1B parámetros se ejecuta en GPU de consumo.

> ColSmol es un variable de menor tamaño de uso en el uso local/margenal.

### VisRAG

VisRAG (Yu et al., arXiv:2410.10594) es una variante diferente: en lugar de MaxSim en parches, agrupar cada página en un solo vector con un VLM y luego recuperar el bi-encoder.

> VisRAG es una variación diferente: no en parche, sino con VLM, se va a organizar cada página en un solo eje re-doble de codificación.

El compromiso calidad-precio: ColPali para la calidad, VisRAG para la escala.

> 质量与成本的权衡:ColPali 追求质量,VisRAG 追求规模──

### M3DocRAG

M3DocRAG (Cho et al., arXiv:2411.04952) extiende la recuperación multimodal al razonamiento multicapa de documentos.

> M3DocRAG extenderá la búsqueda de múltiples modelos a varias páginas de archivos de investigación.

### ViDoRe  el índice de referencia

El punto de referencia de ColPali. Evaluación de recuperación de documentos visuales. Las tareas incluyen informes financieros, documentos científicos, documentos administrativos, registros médicos, manuales.

> El proyecto de investigación de ColPali se basa en la investigación de la investigación y la investigación de la investigación de la investigación y la investigación de la investigación de la investigación y la investigación de la investigación.

ColPali-v1 obtiene un puntaje de ~80% nDCG@5 en ViDoRe; el texto-RAG en los mismos documentos obtiene un puntaje de ~50-60%.

> ColPali-v1 en ViDoRe arriba aproximadamente 80% nDCG@5; texto RAG en el mismo archivo sobre aproximadamente 50-60%。

### El gasoducto de RAG de extremo a extremo

Para un RAG nativo de la visión:

> 视觉原生 RAG 管道:

1. Ingesta: PDF → imágenes de página → codificación PaliGemma → almacenar todos los embebedidos de parches.
   En el texto original, el texto se utiliza para la traducción de la traducción de la lengua inglesa.
2. Consultas: texto de usuario → embeddings de token de consulta → MaxSim contra todas las páginas indexadas → páginas top-k.
   Encuesta: usuario文本 → 查询 token 嵌入 → 对所有索引页面做MaxSim → top-k 页面──
3. Generar: imágenes de la página superior + consulta → VLM (Qwen2.5-VL o Claude) → respuesta.
   En el caso de los que se encuentran en la zona de la ciudad, el número de personas que se encuentran en la zona de la ciudad es de aproximadamente un millón de personas.

No hay OCR en ninguna parte. Las figuras, gráficos, fuentes, diseño todo fluye en la respuesta.

> Todo el proceso sin OCR.

### Matemáticas de almacenamiento

Un informe financiero de 50 páginas con 729 parches por página y embebidos de 128 dimensiones:

> 50 páginas de informe financiero, por página 729 parches,128 dimensiones:

- ColPali: 50 * 729 * 128 * 4 bytes = ~ 18 MB crudo, ~ 4 MB después de PQ.
  中文翻译:ColPali:50 * 729 * 128 * 4 字节 = 约18 MB 原始,PQ 后约4 MB。
- Text-RAG: 50 trozos * 768-dim * 4 bytes = ~ 150 kB.
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de

ColPali es ~ 30 veces más almacenamiento por documento. En escala, OPQ / PQ lo reduce a ~ 5-10x, generalmente tolerable.

> ColPali Cada archivo de almacenamiento de aproximadamente 30 veces. Bajo una gran escala, OPQ/PQ se reducirá a aproximadamente 5-10 veces, normalmente aceptable.

### Cuando el texto-RAG todavía gana

- Documentación de texto puro sin señal de diseño (artículos wiki, registros de chat).
  En el caso de los archivos de archivo, el contenido de los archivos de archivo es más sencillo y más barato.
- Archivos de varios millones de páginas donde el almacenamiento domina el costo.
  El costo de almacenamiento es de más de un millón de páginas.
- Se aplican requisitos regulatorios estrictos que exigen que el texto OCR extraíble se extraiga junto con la recuperación.
  China: 严格要求可提取 OCR 文本与检索并存的监管要求.

Para todo lo demás en 2026  informes financieros, artículos científicos, contratos legales, registros médicos, documentación UX  RAG nativo de visión gana.

> 2026 años todos los demás escenarios 金融報告、科学论文、法律合同、医疗记录、UX 文档视觉原生 RAG 胜出──

## Usalo con el marco de ejecución
```figure
mm-maxsim
```

## Usalo

`code/main.py`¿Qué es esto ?

- Encodrador de parches de juguete: mapea una "página" (pequeña cuadrícula de vectores de características) a una matriz de embebedidos de parches.
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión original de la versión de la versión de la versión de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de
- MaxSim puntuación: calcula la puntuación de estilo ColBERT entre un conjunto de embedding de token de consulta y un conjunto de parches de página.
  评分器:计算查询代币 嵌入集和页面补丁集 集之间 ColBERT 风格分数──
- Indexa 5 páginas de juguete, ejecuta 3 consultas, devuelve el top-k con puntajes.
  Enlace 5 páginas de juegos, 3 consultas, regreso con el máximo de la cantidad de juegos.

## Envíe el producto .

Esta lección produce`outputs/skill-vision-rag-designer.md`. Dado un proyecto de documento-RAG, elige ColPali / ColQwen2 / VisRAG / texto-RAG y mide el almacenamiento.

> 本课产 出  `outputs/skill-vision-rag-designer.md` dar un documento RAG 项目,选择 ColPali / ColQwen2 / VisRAG / 文本 RAG 并估算存储──

## Los ejercicios.

1. Un informe anual de 200 páginas en 729 parches por página, 128-dim Emb, floats de 4 bytes. Computa almacenamiento crudo y almacenamiento comprimido PQ (8x). 200 páginas anual.

2. MaxSim es Σ_i max_j cos(q_i, p_j). ¿Qué captura esta suma que una similitud media simple no? MaxSim es Σ_i max_j cos(q_i, p_j) ⋅

3. ColPali indexa páginas como conjuntos de parches. ¿Qué cambios si en su lugar indexamos a nivel de palabras (como ColBERT hace)?

4. Diseñar el pipeline de extremo a extremo para un corpus de 1M páginas con un presupuesto de latencia de 500ms por consulta. Elegir ColQwen2 / VisRAG y justificar.

5. Lea M3DocRAG (arXiv:2411.04952). Describa el patrón de atención de varias páginas y cómo difiere de la recuperación de ColPali de una sola página.

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Late interaction | "ColBERT-style" 延迟交互 | Retrieval using per-token or per-patch embeddings + MaxSim, not a single doc vector 使用逐 token/patch 嵌入 + MaxSim 的检索，非单向量 | |
| MaxSim | "Max-over-patches" 最大相似度 | For each query token, pick the highest-similarity document token; sum across query 对每个查询 token 选最高相似度的文档 token；跨查询求和 | |
| Bi-encoder | "Single-vector" 双编码器 | One vector per document; faster but loses granularity 每文档一个向量；更快但丢失粒度 | |
| Multi-vector | "Many-vectors-per-doc" 多向量索引 | Store N_p vectors per document / page; storage cost grows but recall improves 每文档/页存储 N_p 个向量；存储增长但召回提升 | |
| Patch embedding | "Page feature" 图像块嵌入 | One vector per image patch from a VLM encoder, cached per page VLM 编码器输出的每 patch 一个向量，按页缓存 | |
| ViDoRe | "Vision doc bench" 视觉文档检索基准 | ColPali's benchmark suite for visual document retrieval ColPali 的视觉文档检索基准套件 | |
| PQ quantization | "Product quantization" 乘积量化 | Compression that maintains vector similarity while shrinking storage ~8x 保持向量相似度的同时压缩存储约 8 倍 | |

## Más Leer más Leer más

- [Faysse et al. — ColPali (arXiv:2407.01449)](https://arxiv.org/abs/2407.01449)
- [Khattab & Zaharia — ColBERT (arXiv:2004.12832)](https://arxiv.org/abs/2004.12832)
- [Yu et al. — VisRAG (arXiv:2410.10594)](https://arxiv.org/abs/2410.10594)
- [Cho et al. — M3DocRAG (arXiv:2411.04952)](https://arxiv.org/abs/2411.04952)
- [illuin-tech/colpali GitHub](https://github.com/illuin-tech/colpali)
