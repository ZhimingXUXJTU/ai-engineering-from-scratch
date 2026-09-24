# RAG multimodal y recuperación transmodal .

> El documento RAG de visión nativa es una sola rebanada. La producción multimodal RAG se expande  la recuperación de texto, imágenes, audio y video para flujos de trabajo como la planificación de viajes ("encontradme un brunch vegano tranquilo con luz natural"), triaje médico ("qué lesión coincide con esta foto + estas notas"), comercio electrónico ("trajes similares a este selfie, en mi tamaño") y servicio de campo ("diagnóstico este sonido del motor más foto de la parte"). Tres encuestas de 2025  Abootorabi et al., Mei et al., Zhao et al.  codificó los subproblemas: recuperación transmodal, fusión de recuperación, generación de tierra, evaluación multimodal. Esta lección lee las encuestas y diseña una línea de producción.

> **【中文解读】**RAG                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

**Type:** Build
**Languages:** Python (stdlib, cross-modal retriever with fusion + grounded generator)
**Prerequisites:** Phase 12 · 23 (ColPali), Phase 11 (RAG basics)
**Time:** ~180 minutes

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·23(ColPali 视觉文档 RAG) 、Fase 11·14-17(RAG 检索/融合/重排) 、Fase 12·02(CLIP 跨模态对齐) ⋅本节是ColPali 扩展多种模态一起检索+融合──
> ¿ Qué es esto ?**【类比】**Más información sobre la formación de los médicos en el campo de la salud y la salud del paciente: ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

## Objetivos de aprendizaje

- Diseño de recuperación transmódica: texto → imagen, imagen → texto, audio → video, etc.
  En español, el nombre de la ciudad de Nueva York es "Casa de la ciudad de Nueva York".
- Comparar tres estrategias de fusión: fusión de puntaje, fusión basada en la atención, fusión de MoE.
  En el caso de los grupos de la sociedad, el grupo de la sociedad de la sociedad de la sociedad de la sociedad de la sociedad civil, la sociedad de la sociedad civil, la sociedad civil y la sociedad civil, la sociedad civil, la sociedad civil y la sociedad civil, la sociedad civil, la sociedad civil y la sociedad civil, la sociedad civil, la sociedad civil y la sociedad civil.
- Explica la generación de tierra: cómo se ve "citar sus fuentes" cuando las fuentes son una mezcla de modalidades.
  Traducción:Cuando la fuente es una mezcla de diferentes formas, la fuente de la referencia es un tipo de forma.
- Nombre de las tres encuestas multimodales canónicas de RAG de 2025 y su taxonomía de subproblemas.
  中文翻译:列举 2025 年三篇经典多模态 RAG 综述及其子问题分类──

## El problema es la introducción del problema

RAG de modalidad única es un patrón resuelto: incrustar consulta, incrustar trozos, recuperar, cosas en LLM. RAG multimodal requiere:

> 单模态 RAG 是已解决的模式:嵌入查询,,嵌入块、检索、塞入 LLM──多模态 RAG 需要:

1. Capaces de extracción múltiples (cada modalidad necesita incorporaciones en un espacio compatible).
   Traducción:Muchos controles de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los modelos de los
2. Fusión de resultados de recuperación en diferentes modalidades.
   En la actualidad, el proceso de integración de los resultados de la investigación está en desarrollo.
3. La generación de tierra que cita fuentes en todas las modalidades.
   Traducción:Modo de referencia de origen de la generación.
4. Metricas de evaluación que cubren la señal transmódica.
   En inglés, "Cámara de evaluación de los signos de un modelo de trabajo".

Las encuestas de 2025 llegan todas a la misma taxonomía.

> El año 2025 se ha desarrollado una misma clasificación.

## El concepto central.

> **【中文解读】**跨模态 RAG  expandió el RAG de texto tradicional, apoyando la búsqueda y generación de múltiples modelos: puede utilizarse la búsqueda de imágenes en texto, la búsqueda de imágenes en texto, o la búsqueda de múltiples modelos en documentos mixtos.

> **【拓展：多模态 RAG 的应用**El número de casos de recesos de los que se trata es el de los casos de recesos de los que se trata la mayoría de los casos.


### Recuperación transmódica

Recoger documentos de modalidad B en una consulta de modalidad A. Tres patrones:

> 给定模态 A 的查询,检索模态 B 的文档──三种模式:

1. Espacio de incorporación compartido. CLIP y CLAP producen embedidos de texto + imagen / texto + audio en un espacio compartido. La similitud de cosinos entre modalidades funciona directamente.
   China Translation: compartido emplazado espacio;. CLIP 和 CLAP en el espacio compartido se produce texto+imagen/texttext+audio emplazado;.

2. Encodrador de modalidad + traducción. Encodrador de texto + encodrador de imagen + un pequeño módulo de traducción que mapea entre espacios. Sen2Sen de Gupta et al. y otros diseños de 2024. Flexible pero añade complejidad.
   En el lenguaje chino, el lenguaje chino es el idioma de la lengua china.

3. VLM como codificador. Utilice los estados ocultos de un VLM como la representación de recuperación. Cualquier modalidad que el VLM admita funciona.
   China 文翻译:VLM 作为编码器──使用VLM 隐藏状态作为检索表示──VLM 支持的任何模态都可用──质量更高,成本更高──

Opción: CLIP / SigLIP 2 para texto + imagen; CLAP para texto + audio; VLM-estados ocultos para trans-modal en calidad fronteriza.

> 选择建议:文本+图像用 CLIP/SigLIP 2;文本+音频用 CLAP;前沿质量跨模态用 VLM 隐藏状态──

### Estrategias de fusión

Recuperaste 10 resultados: 5 imágenes, 3 pasajes de texto, 2 clips de audio. ¿Cómo se fusiona?

> Usted ha buscado 10 resultados: 5 imágenes, 3 fragmentos de texto, 2 fragmentos de audio, ¿cómo se combina?

Fusión de puntajes (más barato). Cada modalidad tiene su propio retriever, cada uno devuelve puntajes. Normaliza las puntuaciones dentro de la modalidad y luego suma.

> Por ejemplo, el modelo de un sistema de búsqueda de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos

Fusión basada en la atención. Concatenar todos los objetos recuperados, dejar que una pequeña red de atención los pese.

> Atención: ¿Cómo se puede hacer una pequeña concentración de la red?

Fusión de MoE. Gating de rutas de red a expertos específicos de modalidad. Diferentes tipos de consultas rutas de manera diferente  una pregunta visual pesa imágenes más alto.

> MoE 融合──门控网络路由到模态特定专家── diferentes tipos de consultas 路由不同的视觉问题给图像更高权重──

Producción por defecto: puntuación de fusión con un ligero sesgo hacia la modalidad dominante de la consulta. actualizar a MoE si A / B muestra claras victorias en su dominio.

> Si el A/B test muestra un claro beneficio en tu área, actualiza a MoE。

> **【中文解读】**Tres estrategias de fusión: 1) Fusión de números  diferentes modelos de investigación  segmentación de números  después de la fusión  y más simple; 2) Fusión de atención  pequeño red de aprendizaje  peso, necesidad de entrenamiento; 3) Fusión de datos  control de la red  por tipo de consulta de los diferentes especialistas.

> **【拓展：多模态 RAG 的跨模态检索基础】**跨模态检索有三种模式:(1) 共享嵌入空间(CLIP/SigLIP 2 用于图文,CLAP 用于文本-音频);(2) 每模态独立编码器 + 翻译模块;(3) 用于VLM 隐藏状态作为检索表示──选择建议:文本+图像用CLIP/SigLIP 2,文本+音频用CLAP,跨模态前沿质量用VLM 隐藏状态──

### Aterrizaje de generación

La MLL debe citar qué elemento recuperado impulsó cada reclamo.

> El LLM 应引用哪个检索项驱动了每个声明.

- Fuente de texto: citación estándar `[1]`¿ Qué ?
  Sin embargo, el gobierno de la República de China no ha sido capaz de hacer nada.`[1]`¿Qué es eso?
- Fuente de imagen: `[img 3]`con una breve leyenda.
  En el caso de los niños, el nombre de la persona que se encuentra en el centro de la ciudad es el de la ciudad.`[img 3]`附简短描述── también
- Audio: `[audio 2 at 0:34]`¿ Qué ?
  El idioma de la lengua china es el idioma de la lengua china.`[audio 2 at 0:34]`¿Qué es eso?

Entrenando al generador con datos conocedores de la base: cada afirmación en el objetivo de entrenamiento está etiquetada con el índice de origen.

> Utilizando el proceso de aprendizaje de datos: cada uno de los objetivos de la formación se marca en el código fuente.

### Las encuestas de 2025

Abootorabi et al. (arXiv:2502.08826, "Ask in Any Modality"): taxonomía para RAG multimodal. Cubre la recuperación, fusión, generación. Cobertura más amplia.

> Abootorabi 等人:多模态 RAG 分类法──覆盖检索、融合、生成──覆盖最广──

Mei et al. (arXiv:2504.08748, "Una encuesta de RAG multimodal"): se centra en los puntos de referencia de subtareas y modos de falla.

> Mei 等人: enfoque en las tareas básicas y el modelo de fracaso.

Zhao et al. (arXiv:2503.18016): encuesta centrada en la visión.

> Zhao 等人:聚焦视觉的综述──对 ColPali 系列工作覆盖深入──

Leer los tres te da el estado del arte a partir de la primavera de 2025.

> 阅读全部三篇可获得2025年春最前沿状态―― la mayoría de los problemas todavía están abiertos―

### MuRAG  el documento de base

MuRAG (Chen et al., 2022) fue el primer RAG multimodal. Recuperó imagen + texto de un KB multimodal, generó respuestas.

> MuRAG es el primer RAG multimodelo. Desde la biblioteca de conocimientos de varios modelos, se ha demostrado la viabilidad de la VLM antes de la ola.

### Un ejemplo de planificador de viajes de producción

Pregunta: "Encuentra un brunch vegano tranquilo con luz natural".

> Pregunta: "Dame encontrar un tranquilo y puro almuerzo, hay luz natural"".

El gasoducto:

> 管道:

1. Descompone la consulta. "quiet" → palabra clave de audio/revisión; "vegan brunch" → elemento del menú; "luz natural" → función de imagen.
   En el lenguaje chino, el lenguaje de la lengua china es "solo" y "solo" se refiere a la lengua inglesa.
2. Recuperación por modalidad:
   En el caso de los niños, el número de niños en edad avanzada es de aproximadamente un millón.
   - Recuperación de texto en las reseñas: "brunch vegano, ambiente tranquilo".
     El texto de la carta de la revista "Puramente en la mañana" se traduce en "Puramente en la mañana".
   - Recuperación de imágenes en fotos de restaurantes: "luz natural, aireada".
     El nombre de la ciudad de Nueva York se encuentra en el centro de la ciudad.
   - Recuperación de audio en clips de sonido ambiente: "bajo decibel, sin música".
     El lenguaje de la lengua china es el idioma de la lengua china.
3. Cada restaurante tiene una puntuación compuesta.
   En el resto de la sala hay un número de entradas.
4. Restaurantes Top-k → Generador VLM con toda la evidencia → respuesta con citas.
   En el caso de los viajeros, el número de pasajeros en el mercado de transporte es de aproximadamente un millón de personas.

Esto va mucho más allá del texto-RAG. Cada modalidad añade una señal que el texto solo pierde.

> Este es un gran número de RAG. Cada modelo se agrega sólo por las señales que el texto deja.

### Agentes de RAG multimodal

Multi-hop: si la primera recuperación no devuelve respuestas de alta confianza, el LLM reformula y recupera de nuevo.

> Más saltos: Si la primera vez que se le solicita no se le devuelve una respuesta de alta confianza, LLM 重新表述并再次检索──Fase 14 de Agente RAG 模式在此适用── Ejemplo:

- Recuperar el top-10 inicial → LLM pide "demasiado ruidoso, filtro para <40 dB" → recuperar de nuevo.
  En el caso de los estudiantes de la Universidad de Nueva York, el número de estudiantes de la Universidad de Nueva York es de 40 a 40 años.
- Recuperar imágenes → LLM ve que uno tiene un menú → recuperar el texto del menú → respuesta.
  En inglés, el texto de la ley de educación superior se traduce en inglés como "Legislación de educación superior".

Agrega complejidad pero maneja consultas que la recuperación de un solo disparo no puede.

>  aumento de complejidad pero puede tratar una sola consulta  consulta imposible de tratar

### Evaluación

La evaluación transmodal es aún inmadura.

> 跨模态评估 todavía no está maduro.

- Recall@k por modalidad.
  En español, el nombre de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona.
- Precisión top-k fusionada.
  La tasa de acceleración de la convergencia después de la convergencia es de 1.
- La satisfacción de extremo a extremo, según el juicio humano.
  Traducción:Artificial de la evaluación de la conclusión de la conclusión.
- Específico de tarea (reservas completadas, compras realizadas).
  En español, "completar" significa "completar" o "completar".

No hay un índice de referencia estándar que abarque todas las modalidades.

> 没有标准基准覆盖所有模态──la mayoría de los trabajos se evalúan en tareas específicas del ámbito──

## Usalo con el marco de ejecución
```figure
contrastive-matrix
```

## Usalo

`code/main.py`¿Qué es esto ?

- Tres simuladores de retriever (texto, imagen, audio) que operan en un conjunto compartido de restaurantes.
  Traducción:Nuevo idioma: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español:
- Fusión de puntuaciones que combina puntuaciones de modalidad con pesos configurables.
  Traducción:Conformidad de la configuración de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de los números de la combinación de la combinación de los números de la combinación de los números de la combinación de la combinación de los números de la combinación de los números.
- Un generador que emite una respuesta final con citas.
  Traducción: 输出带引用最终回答的生成器──
- Un simple bucle agente que reformula la consulta si la confianza es baja.
  Traducción:De la confianza en el tiempo, re-expresar la consulta de simple agente ciclo.

## Envíe el producto .

Esta lección produce`outputs/skill-multimodal-rag-designer.md`. Dado un producto específico con un flujo de consulta multimodal, diseña retrievers, fusión, generador y evaluación.

> 本课产 出  `outputs/skill-multimodal-rag-designer.md` Determinar los modelos de productos, especificaciones, diseño de los investigadores, estrategias de integración, generadores y programas de evaluación de los flujos de consulta.

## Los ejercicios.

1. Proponer una RAG multimodal de triaje médico: consulta = foto de lesión + síntomas de texto. ¿Qué modalidades se extraen de qué KB? 设计医疗分诊多模态 RAG:查询 = 伤处照片 + 文字症状── ¿qué modelos se extraen de qué conocimientos?

2. La fusión de puntajes es una suma ponderada simple. ¿Qué modo de fracaso tiene que la fusión de MoE evita?

3. Lea la taxonomía de Abootorabi et al. (Sección 3). ¿Cuáles son los tres subproblemas canónicos y cómo se mapean a su producto elegido? 阅读 Abootorabi 等人的分类法(第 3 节)。三个标准子问题是什么?

4. Diseñar una especificación de evaluación para un RAG multimodal de planeador de viajes. ¿Qué métricas cubren el recuerdo de imágenes, el recuerdo de audio y la corrección compuesta? 设计旅行规划多模态 RAG 的评估规格──.

5. Agente multi-hop RAG tiene un impuesto de latencia por ida y vuelta. ¿En qué dificultad de consulta la precisión aumenta justifica la latencia?

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Cross-modal retrieval | "Query one modality, retrieve another" 跨模态检索 | Text query retrieves images; image query retrieves text; requires a shared space or translator 文本查询检索图像；图像查询检索文本；需要共享空间或翻译器 | |
| Score fusion | "Combine scores" 分数融合 | Weighted sum of per-modality retrieval scores; simplest fusion 各模态检索分数的加权和；最简单的融合方式 | |
| MoE fusion | "Modality-routed experts" 混合专家融合 | Gating network picks which modality's scores to trust per query 门控网络按查询选择信任哪个模态的分数 | |
| Grounded generation | "Cite your sources" 接地生成 | Each claim in the answer tagged with the source index 回答中的每个声明都标注来源索引 | |
| MuRAG | "First multimodal RAG" 首个多模态 RAG | 2022 paper that established the multimodal RAG pattern 2022 年建立多模态 RAG 模式的论文 | |
| Agentic multi-hop | "Reformulate and retry" Agent 多跳 | LLM re-queries retrievers when first-pass confidence is low 首次检索置信度低时 LLM 重新查询检索器 | |

## Más Leer más Leer más

- [Abootorabi et al. — Ask in Any Modality (arXiv:2502.08826)](https://arxiv.org/abs/2502.08826)
- [Mei et al. — A Survey of Multimodal RAG (arXiv:2504.08748)](https://arxiv.org/abs/2504.08748)
- [Zhao et al. — Vision RAG Survey (arXiv:2503.18016)](https://arxiv.org/abs/2503.18016)
- [Chen et al. — MuRAG (arXiv:2210.02928)](https://arxiv.org/abs/2210.02928)
- [Liu et al. — REACT (arXiv:2301.10382)](https://arxiv.org/abs/2301.10382)
