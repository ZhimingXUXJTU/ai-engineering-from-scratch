# Documento y Diagrama Comprensión  Archivo y gráfico Comprensión

> Los documentos no son fotos. Un PDF, un documento científico, una factura o un formulario escrito a mano tiene un diseño, tablas, diagramas, notas a pie de página, encabezados y estructura semántica que la comprensión de la imagen simple no puede captar. La pila pre-VLM era una tubería: Tesseract OCR + LayoutLMv3 + heurísticas de extracción de tablas. La ola VLM reemplazó a la de modelos libres de OCR  Donut (2022), Nougat (2023), DocLLM (2023)  que emiten marcado estructurado directamente. Para 2026, la frontera es simplemente "alimentar la imagen de página a Claude Opus 4.7 en nativo de 2576px", y la salida de marcado estructurado viene de forma gratuita. Esta lección lee el arco de tres épocas de la IA de documentos.

> **【中文解读】**文档不是照片──PDF、论文、发票、手写表单有布局、表格、图表、脚注、标题等语义结构,普通图像理解无法捕捉──文档 AI 经历了三个时代:(1) OCR管道(Tesseract + LayoutLMv3);(2) OCR-free(Donut、Nougat 直接从图像生成结构化输出);(3) VLM 原生(2026年直接将页面图像给Claude Opus 4.7 即可)

> **【拓展：文档理解在金融领域的应用】**金融场景是文档 AI 最重要应用领域之一:发票解析(自动提取供应商、金额、税率) 、合同审查(条款比对、风险标记) 、财务报表提取(资产负债表、利表的结构化数据抽取) 、KYC 文档处理身份(证券、营业执照的自动识别) ∼2026年推方案:纯印发票用 LayoutLMv3 ◎成本低),混合文档用手写VLM 原生(PaliGemma 2或Qwen2.5-VL),监管场景用OCR + VLM 交叉验证──

**Type:** Build
**Languages:** Python (stdlib, layout-aware document parser skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 5 (NLP)
**Time:** ~180 minutes

> ¿ Qué es esto ?**【前置】**La fase 12 de la serie de proyectos de investigación de la VLM es un proyecto de investigación de gran alcance y de gran importancia.
> ¿ Qué es esto ?**【类比】**文档理解三时代 = "evolución de los informes de contabilidad"。OCR 管道 = 人工核对+表格软件(先识别文字再解析布局);OCR-free(Donut) = software integrado(看图直接生成结构化数据);VLM 原生(Claude) = 全能AI(看图就能理解,回答,推理,无需专门训练)。 Cada generación deja pasar el tiempo de la primera generación de métodos, pero las tres generaciones de 2026 todavía están utilizando el esquema más barato para seleccionar en el escenario―
> ️ **【易错点】**简单 OCR 任务用VLM = 杀用牛刀(成本10倍) ・・・例如纯文本发票用Tesseract + LayoutLMv3 只需几分钱,使用GPT-4V 要几毛钱──修复:先评估任务复杂度,简单的OCR管道,复杂的(手写、混合布局、多语言)才上VLM──

## Objetivos de aprendizaje

- Explica las tres eras de la IA de documentos: OCR pipeline, OCR libre, VLM nativo.
  La inteligencia artificial tiene tres tiempos: OCR 管道、无 OCR、VLM 原生──
- Describa las tres corrientes de entrada de LayoutLMv3: texto, diseño (bbox), parches de imagen, con enmascaramiento unificado.
  La versión original de LayoutLMv3 fue publicada en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web de LayoutLMv3 en el sitio web.
- Compare Donut (sin OCR, imagen → marcado), Nougat (papel científico → LaTeX), DocLLM (generativo consciente del diseño), PaliGemma 2 (nativo de VLM).
  En el caso de los donuts, el nombre de los donuts es el de los donuts.
- Seleccione un modelo de documento para una nueva tarea (facturas, documentos científicos, formularios escritos a mano, recibos chinos).
  En el texto original, el texto se traduce en la lengua inglesa como "el lenguaje de la lengua".

## El problema es la introducción del problema

"Entender este PDF" es engañosamente difícil. La información se encuentra en:

> "Comprender este PDF" parece simple en realidad difícil.

- Contenido de texto (90% de la señal).
  En el texto original, el texto se traduce como "la palabra de Dios".
- Layout (títulos, notas de pie, barras laterales, formato de dos columnas).
  En el lenguaje chino, el lenguaje de la lengua se traduce en lengua inglesa como lengua de la lengua inglesa.
- Tablas (fila, columna, células fusionadas).
  En el caso de los ejemplos de la lengua inglesa, el nombre de la lengua inglesa es "Latin".
- Las figuras y diagramas.
  En español: gráfico y ilustración.
- Anotadas escritas a mano.
  En inglés, "Here's the way".
- Fuentes y tipografía (título vs cuerpo).
  En el idioma chino, el idioma se traduce en inglés como "el idioma" (en inglés).

Un sistema que se preocupa por las facturas necesita saber que "Total: $1,245" proviene de la parte inferior derecha, no de una nota a pie de página.

> El sistema de corrección de votos necesita saber "total: $1,245" de la esquina derecha, y no de la esquina abajo.

## El concepto central.

> **【中文解读】**文档和图表理解是多模态 AI:OCR,表格提取,流程图解读,公式识别等. 关键技术: alta resolución de entrada, conservación de la claridad de los textos, edición de la superficie, análisis de la estructura de los archivos, producción estructurada, transformación de la información visual en un formato procesable.

> **【拓展：文档 AI 的工业应用**文档 AI 市場巨型:合同审核、发票处理、学术论文分析等──GPT-4o en DocVQA alcanzó el 92.8%,InternVL2-26B alcanzó el 92.7% MarkItDown (Microsoft) convertirá el documento en Markdown,ColPali con métodos de visión para reemplazar a las tradicionales OCR 管线──


> **【拓展：文档理解的技术路线】**文档理解有两条路线:(1) OCR-first(先用OCR 提取文本,再用LLM 处理) 适合纯文文文文档;(2) Vision-first(直接用VLM 处理文档图像)适合包含图表、表格的复杂版面── GPT-4o 和 InternVL2 走 Vision-first 路线,在复杂文档理解上表现更好──


### ERA 1  OCR (antes de 2021)

La pila clásica:

> 经典技术:

1. PDF → imagen por página.
   En el texto original, el texto se traduce en inglés como "PDF".
2. Tesseract (o OCR comercial) extrae texto con cuadro de límite por palabra.
   China: Tesseract (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tess) (Tesseract) (Tesseract) (Tesseract) (Tess) (Tesseract) (Tess) (Tess) (Tesseract) (Tess) (Tess) (Tess) (Tesseract) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (Tess) (T) (T) (T) (T) (T) (T) (T) (T)
3. El analizador de diseño identifica los bloques (título, tabla, párrafo).
   En inglés, el lenguaje de la lengua inglesa se traduce en inglés como "el lenguaje de la lengua".
4. El reconocedor de estructura de la tabla analiza las tablas.
   En inglés, el lenguaje de la lengua inglesa se traduce en inglés como "el lenguaje de la lengua".
5. Reglas de dominio + campos de extracto de regex.
   En español: "Región de la lengua"

Funciona para texto impreso limpio. Se rompe la letra, escaneos sesgados, tablas complejas, guiones no en inglés. Cada modo de falla requiere un camino de excepción personalizado.

> 适用于清洁印刷文本──在手写、倾斜扫描、复杂表格、非英语文字上失败──每种失败模式都需要自定义异常处理──

### El importe de la ayuda se calcula en el plazo de cinco meses.

TrOCR (Li et al., arXiv:2109.10282) reemplazó al clásico CNN-CTC de Tesseract por un transformer encoder-decoder entrenado en imágenes de texto sintéticas + reales.

> TrOCR utilizó en la formación de sintetizadores de imágenes de texto real 编码器-解码器 sustituyó a los clásicos CNN-CTC de Tesseract.

### Era 2  libre de OCR (2022-2023)

Los primeros modelos libres de OCR dijeron: omite la detección por completo, mapa de los píxeles de imagen a la salida estructurada directamente.

> Primera generación sin OCR 模型 propuesto: completamente saltar de inspección, directamente se proyecta imagen imagen para la salida estructurada.

Donut (Kim et al., arXiv:2111.15664):
- Transformador de codificación y decodificación, codificador es Swin-B.
- La salida es JSON para la comprensión de las formas, marcado para la resumen, o cualquier esquema específico de tarea.
- No hay OCR, no hay diseño, no detección.

> Donut:编码器-解码器 Transformer,编码器为Swin-B──输出是 JSON(表单理解)、标记down(摘要) 或任务特定方案──无需 OCR、无需布局、无需检测──

Nougat (Blecher et al., arXiv:2308.13418):
- Formado específicamente en artículos científicos.
- La salida es LaTeX / marcado.
- Maneja ecuaciones, diseño de varias columnas, figuras.
- El modelo que llama cada parser de archivo.

> Nougat: especializado en el trabajo científico.

Esos son especialistas, no generalistas.

> Estos son modelos expertos, no son de talento.

### LayoutLMv3 (2022)

La distribuciónLMv3 (Huang et al., arXiv:2204.08387) mantiene la OCR pero añade la comprensión del diseño:

> No es igual. Mantenga el OCR, pero añade el diseño.

- Tres flujos de entrada: tokens de texto OCR, cuadros de límite 2D por token, parches de imagen.
  En inglés, el código de acceso de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de red.
- Objetivo de formación enmascarada en las tres modalidades (texto enmascarado, parches enmascarados, diseño enmascarado).
  En el caso de los niños, el uso de la palabra "escuro" es un método de aprendizaje de la lengua.
- A continuación: clasificación, extracción de entidades, cuadro de calificación.
  En el caso de los grupos de trabajo, el grupo de trabajo de los trabajadores de la empresa es el grupo de trabajo de los trabajadores de la empresa.

LayoutLMv3 es el máximo de comprensión de documentos basados en OCR. Fuerte en formularios y facturas. Requiere OCR en el río arriba. Mejor precisión previo a VLM en referentes de documentos estandarizados.

> LayoutLMv3 es el punto más alto de la comprensión de los documentos basados en OCR.

### DocLLM (2023)

DocLLM (Wang et al., arXiv:2401.00908) es el hermano generativo de LayoutLM. Genera respuestas de forma libre condicionadas a tokens de diseño. Mejor para QA en documentos; todavía depende de la entrada de OCR.

> DocLLM es la generación de LayoutLM.

### Era 3  nativo de VLM (2024+)

2024 VLMs se hicieron lo suficientemente buenos para reemplazar el oleoducto por completo.

> 2024 VLM  become good enough, can completely replace pipeline― will complete page image with high resolution give VLM, questions, get answers―

- El AnyRes de lápiz LLaVA-NeXT 336 funciona para documentos pequeños.
  En el caso de los archivos de la revista, el texto de la revista se basa en el texto de la revista.
- Qwen2.5VL de resolución dinámica maneja 2048+ píxeles de forma nativa.
  China 动态分辨率原生处理 2048+ 像素──
- Claude Opus 4.7 admite documentos de 2576px.
  El texto de la obra de Claude Opus 4.7 支持 2576px 文档。
- PaliGemma 2 (abril 2025) se entrena específicamente para documentos + escritura a mano.
  En el caso de la lengua portuguesa, el idioma oficial de la lengua portuguesa es el idioma de la lengua portuguesa.

La brecha entre el tubo de VLM-nativo y el OCR se cerró rápidamente.

> La diferencia entre el VLM original y el OCR se reducirá rápidamente.

- Texto de escena (escrito a mano + impreso, guiones mixtos).
  La traducción de la lengua inglesa es "creo" (en inglés).
- Tablas complejas con células fusionadas.
  La forma de la obra es la de la obra.
- Ecuaciones matemáticas incrustadas en el texto.
  En español: "Enlazar en el texto"
- Figuras con anotaciones de texto.
  La obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra.

Los oleoductos de OCR siguen ganando:

> El sistema de OCR sigue siendo exitoso en los siguientes aspectos:

- Cargas de trabajo de escaneo puro a gran escala donde la latencia por página importa.
  La obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de Jesús.
- Confiabilidad de la tubería (fallas deterministas frente a alucinaciones de VLM).
  La situación de la seguridad de los trabajadores en el sector de la seguridad social es muy difícil.
- Entidades reguladas que requieren una salida de OCR auditable.
  China                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

### La frontera de Claude 4.7 / GPT-5

A 2576 píxeles de entrada nativa, los VLM fronterizos documentan la comprensión con una precisión casi humana.

> En 2576 像素原生输入下, VLM de primera línea para acercarse a la precisión humana en el estudio de la comprensión de documentos.

- DocVQA: Claude 4.7 ~ 95.1, PaliGemma 2 ~ 88.4, Nougat ~ 77.3, Layout en tuberíaLMv3 ~ 83.
  En el texto original, el texto se basa en el texto de la carta de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista de la revista.
- CÁRTO: Claude 4.7 ~ 92,2, GPT-4V ~ 78.
  En el caso de los países de la Unión Europea, el número de países de la UE es de aproximadamente un millón de personas.
- VisualMRC: Claude 4.7 ~ 94.
  El texto original de la película fue publicado en el periódico de la revista The Guardian.

La brecha en el modelo cerrado es principalmente de resolución y escala LLM base.

> La diferencia entre los modelos de código abierto y los modelos de código abierto está en la escala de la LLM.

### Ecuaciones matemáticas y salida de LaTeX

Los trabajos científicos necesitan una salida exacta de LaTeX para las ecuaciones. Nougat fue entrenado en esto. VLM entrenados con objetivos LaTeX (Qwen2.5-VL-Math, derivados de Nougat) producen LaTeX utilizable.

> El trabajo científico necesita un método de formación de la lengua latina. No hay una forma de formación de la lengua latina.

Para las tuberías de papel científico en 2026: cadena Nougat en el PDF, luego un VLM en páginas complicadas.

> 2026 年科学论文管道建议:先用 Nougat 处理 PDF,再用 VLM 处理棘手页面──

### Escritura de mano

La tarea más difícil es la de imprimir mezclado + escrito a mano (noticias de médicos, formularios llenos) donde las tuberías de OCR siguen superando a las VLM en cuanto a costo.

> 仍然是最难的子任务──印刷+手写混合(医生笔记、填写的表单) es que el OCR 管道 sigue superando el VLM en el costo.

### Recepta de 2026

Para un nuevo proyecto de IA documental:

>  para nuevos proyectos de IA:

- Las facturas impresas en escala: LayoutLMv3 + reglas, rentables.
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de LMv3 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la
- Documentación mixta (científica + manuscrito + formularios): nativo de VLM (PaliGemma 2 o Qwen2.5-VL).
  En el caso de los primeros tiempos, el sistema de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información.
- Ingestión completa de archivo: Nougat para matemáticas, VLM para cifras.
  En el texto original, el texto se basa en el texto de la traducción de la lengua inglesa.
- Regulación: tubería de OCR + validador VLM para la verificación cruzada.
  La información de la empresa se encuentra en el área de control de la empresa.

## Usalo con el marco de ejecución
```figure
mm-doc-layout
```

## Usalo

`code/main.py`¿Qué es esto ?

- Un tokenizer de juguete consciente de la disposición: dado (texto, bbox) pares, produce la entrada de estilo LayoutLMv3.
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original.
- Generador de esquemas de tareas de estilo Donut: plantilla JSON para formularios.
  Sin embargo, el proyecto de trabajo de la empresa es un proyecto de investigación.
- Una comparación de los presupuestos de tokens por página en OCR-pipeline, Donut, Nougat y VLM-native.
  En inglés, el código de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de datos de la red de datos de datos de la red de datos de datos de la red de datos de datos de la red de datos de datos de la red de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos

## Envíe el producto .

Esta lección produce`outputs/skill-document-ai-stack-picker.md`. Dado un proyecto de IA de documentos (dominio, escala, calidad, regulación), escoge entre el oleoducto de OCR, el especialista libre de OCR y el nativo de VLM.

> 本课产 出  `outputs/skill-document-ai-stack-picker.md` proporcionar documentación sobre proyectos de IA  ámbito  tamaño  calidad  supervisión), entre los OCR 管道  no OCR 专家 y VLM

## Los ejercicios.

1. ¿Cuál pila minimiza el costo por página sin perder precisión? ¿Cuál es el proyecto que maneja 1.000 millones de dólares diarios? ¿Cuál es el programa que puede minimizar el costo por página sin pérdida de precisión?

2. ¿Por qué LayoutLMv3 supera a los puros CLIP-VLM en el formulario QA pero tiene un rendimiento inferior en el texto de escena? ¿Qué es lo que el stream bbox abandona? ¿Por qué LayoutLMv3 en el solo QA 上优于纯 CLIP VLM, pero en el escenario文本上表现不佳? bbox 流放弃了什么?

3. Nougat genera LaTeX. Proponga un caso de prueba en el que la salida nativa de VLM vence a Nougat en fidelidad de LaTeX, y un caso en el que Nougat gane. Nougat 生成 LaTeX.

4. ¿Cuál fue la adición clave de datos de entrenamiento que levantó la exactitud del documento frente a PaliGemma 1? 阅读 PaliGemma 2 论文──相比 PaliGemma 1, ¿qué clave ha aumentado el índice de precisión de documentos?

5. Diseñar un híbrido regulador-seguro: OCR como tubería principal, VLM como control cruzado secundario. ¿Cómo resolver el desacuerdo?

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| OCR pipeline | "Tesseract-style" OCR 管道 | Stage-wise stack: detect -> OCR -> layout -> rules; deterministic, fragile 分阶段栈：检测→OCR→布局→规则；确定但脆弱 | |
| OCR-free | "Donut-style" 无 OCR | Image-to-output transformer that skips explicit OCR; single model 图像到输出的 Transformer，跳过显式 OCR；单一模型 | |
| Layout-aware | "LayoutLM" 布局感知 | Input includes per-token bbox coordinates; unified masking across modalities 输入包含逐 token 的 bbox 坐标；跨模态统一掩码 | |
| VLM-native | "Frontier VLM" VLM 原生 | Feed page image directly to Claude/GPT/Qwen VLM at high resolution; no pipeline 直接将页面图像输入高分辨率 VLM；无需管道 | |
| DocVQA | "Doc benchmark" 文档 VQA 基准 | Document VQA standard; most-cited score 文档 VQA 标准评测；被引用最多的评分 | |
| Markup output | "LaTeX / MD" 标记输出 | Structured output format instead of free-form text; enables downstream automation 结构化输出格式而非自由文本；支撑下游自动化 | |

## Más Leer más Leer más

- [Li et al. — TrOCR (arXiv:2109.10282)](https://arxiv.org/abs/2109.10282)
- [Blecher et al. — Nougat (arXiv:2308.13418)](https://arxiv.org/abs/2308.13418)
- [Huang et al. — LayoutLMv3 (arXiv:2204.08387)](https://arxiv.org/abs/2204.08387)
- [Kim et al. — Donut (arXiv:2111.15664)](https://arxiv.org/abs/2111.15664)
- [Wang et al. — DocLLM (arXiv:2401.00908)](https://arxiv.org/abs/2401.00908)
