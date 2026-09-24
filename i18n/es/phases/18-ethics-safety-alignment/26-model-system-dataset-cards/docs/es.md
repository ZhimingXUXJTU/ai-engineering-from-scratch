# Modelo, sistema y tarjetas de conjunto de datos.

> Tres formatos de documentación estructuran la transparencia de la IA. Carteles modelo (Mitchell et al. En el caso de los modelos de Hugging Face, sólo el 0,3% de las tarjetas de modelos de Hugging Face documentan consideraciones éticas (Oreamuno et al. El año 2023). Fichas de datos para Datasets (Gebru et al. 2018, CACM)  motivación, composición, proceso de recogida, etiquetado, distribución, mantenimiento; analogía electrónica-ficha de datos. Las tarjetas de datos (Pushkarna et al., Google 2022)  detalle en capas modulares (telescópico, periscópico, microscópico) como objetos de frontera para diversos lectores. Desarrollo 2024-2025: generación automatizada a través de los LLM (CardGen, Liu et al. 2024); el detalle de la tarjeta de modelo se correlaciona con un aumento de hasta un 29% en las descargas de HF (Liang et al. Las autoridades competentes de la Unión Europea han informado a los Estados miembros de que la certificación de la calidad de los productos de la industria de la Unión Europea (en lo sucesivo, la certificación de los productos de la industria de la Unión Europea) se cumple con el objetivo de garantizar que los productos de la Unión sean compatibles con el mercado interior. Las medidas de ayuda a la pesca y a la pesca incluyen medidas de ayuda a la pesca y a la pesca. Julio 2025); las tarjetas reguladoras de la UE/ISO emergentes. Cartas de sistema (Sidhpurwala 2024; Transparencia a nivel de meta sistema; "Bluprints of Trust" arXiv:2509.20394)  Documentación de sistema de IA de extremo a extremo que cubre las capacidades de seguridad, protección de inyección rápida, detección de exfiltración de datos, alineamiento con los valores humanos.

> **【中文解读】**Este capítulo presenta los modelos/ sistemas/ datos de los grupos de datos de los archivos DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATASET DATAS DATASET DATASET DATASET DATAS DATASET DATASET DATASET DATASET DATASET DATAS DATASET DATASET DATASET DATAS DATAS DATASET DATASET DATASET 

> **【拓展：采用率 → 0.3% 问题】**Oreamuno 等人 2023  Audit Hugging Face 模型卡发现只有0.3% 记录伦理考量。Liang 等人 2024 发现详细模型卡与高达29%的下载增加相关采用压力现在是市场驱动的,不仅是合规驱动的──自动化生成(CardGen, Liu 等人 2024) 和可验证证明(Laminator, Duddu 等人 2024) 解决长期采用问题──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, model-card + datasheet + system-card generator) | **语言:** Python（标准库，模型卡 + 数据表 + 系统卡生成器）
**Prerequisites:** Phase 18 · 18 (safety frameworks), Phase 18 · 24 (regulatory) | **前置知识:** Phase 18 · 18 (安全框架), Phase 18 · 24 (监管)
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 18·18+24──三种透明度文档:模型卡 + 数据集卡 + 系统卡──
> ¿ Qué es esto ?**【类比】**透明卡 = "protocolo de productos de IA"―Modelo de tarjetas = 营养标签(entrenamiento datos/ análisis/伦理); Datasheets = 电子元件规格书(数据集动机/组成/收集);System Cards = 整机蓝图(端到端系统)―Problema: sólo 0.3% HF 模型卡含伦理考量──
> 🤔 详细卡 → 下载量 29%(HF 2024 数据)  Transparencia tiene valor comercial──2024-2025 Nueva tendencia:LLM 自动生成卡(CardGen)、可验证证明(Laminator)、可持续性报告(碳/水)。

## Objetivos de aprendizaje

- Describa la tarjeta modelo original de Mitchell et al. de 2019 y la hoja de datos de Gebru et al. de 2018.
- Describa la captura telescópica/periscópica/microscópica de las tarjetas de datos.
- Describa las tarjetas de sistema y su cobertura de extremo a extremo.
- En el caso de las empresas de la Unión, el importe de la producción de la producción de la producción de la Unión debe ser de un importe de un millón de euros.

> 描述 Mitchell 等人 2019的原始模型卡和 Gebru 等人 2018的数据表──描述数据卡的望远镜/潜望镜/显微镜分层──描述系统卡 及其端到端覆盖──说明三个 2024-2025年发展──

## El problema es el problema .

Los marcos regulatorios (lección 24) y las políticas de seguridad de laboratorio (lección 18) requieren documentación. Los formatos de documentación evolucionaron de modelos específicos (tarjetas modelo) a conjuntos de datos específicos (fichas de datos) a sistemas específicos (tarjetas de sistema). Cada uno aborda un alcance diferente de transparencia.

> 监管框架和实验室安全政策都要求文档――文档形式从模型特定 (模型卡) 到数据集 (数据集) 特定 (数据表) 到系统特定 (系统卡) 发展――2024-2025 años de automatización y validación de la prueba de trabajo resuelve problemas de adopción a largo plazo――

## El concepto.

> **【中文解读】**Modelo de tarjetas 九大板块:模型详情、预期用途、因素 (relacionados con la población o el medio ambiente) ‧指标、评估数据、训练数据、定量分析 (en función de los factores que se desglosan) ‧伦理考量、注意事项和建议──Data Cards(Google 2022) de tres niveles de acrecentamiento:望远镜级((非专家高层摘要) ‧潜望镜级(ML 从业者中层概览) ‧微镜级(审计员显详细特征级文档) ∼

### Carteles modelo (Mitchell et al. 2019)

Secciones:
- Detalles del modelo.
- Uso previsto.
- Factores (factores demográficos o ambientales relevantes para la evaluación).
- Las métricas.
- Datos de evaluación.
- Datos de entrenamiento.
- Análisis cuantitativos (desagregados por factores).
- Considerancias éticas.
- Las cuevas y las recomendaciones.

Problema de adopción: Oreamuno et al. Auditoría 2023 de las tarjetas de modelo Hugging Face encontró sólo el 0,3% de documentos consideraciones éticas.

### Ficha de datos para conjuntos de datos (Gebru et al. 2018)

Analogía de ficha electrónica.
- Motivación (por qué se creó el conjunto de datos).
- Compuesta (lo que hay en ella).
- Proceso de recogida (cómo se ensambló).
- Etiquetado (si corresponde).
- Utilizaciones (intencionadas, prohibidas, riesgos).
- Distribución.
- - El mantenimiento.

Publicado en CACM 2021. La hoja de datos es la documentación de aguas arriba; la tarjeta modelo depende de que la hoja de datos sea exacta.

### Carteles de datos (Pushkarna et al., Google 2022)

Detalle modular en capas. Tres niveles de zoom:
- **Telescopic.**Resumen de alto nivel para no expertos.
- **Periscopic.**Una visión general de nivel medio para los profesionales de la ML.
- **Microscopic.**Documentación detallada a nivel de características para los auditores.

Enmarcado de límites: diferentes lectores extraen información diferente del mismo documento.

> **【拓展：System Cards → 部署层透明度】**El sistema de tarjetas de seguridad incluye modelos+ seguridad+ implementación en la siguiente sección. El tipo de tarjetas de seguridad  capacidad de seguridad  sugerencias de protección  datos de fuga de datos  declaraciones de valores humanos  respuesta a eventos  "Bluprints of Trust"  arXiv:2509.20394)  Formalización de la tarjeta de sistema  complemento de la capa de implementación de la tarjeta de modelo  GPAI  código de la Ley de la UE  Requisitos de la transparencia 

### Carnetas de sistema

Ámbito de aplicación: sistema de IA de extremo a extremo que incluye modelo + pila de seguridad + contexto de implementación.
- Capacidades de seguridad.
- Protección por inyección rápida.
- Detección de exfiltración de datos.
- Alineación con los valores humanos declarados.
- Respuesta al incidente.

Sidhpurwala 2024 y Meta trabajan en el nivel de transparencia del sistema. "Bluprints of Trust" (arXiv:2509.20394) formaliza la tarjeta del sistema como el complemento de la capa de implementación de las tarjetas modelo.

> **【中文解读】**2024-2025 años de desarrollo:CardGen(Liu 等人 2024) a través de LLM Automatic Generating Model Card, Reporting Than Many Artificial Card higher Objectivity;Laminator(Duddu 等人 2024) a través de hardware TEE/加密签名实现可验证证明 permite que el modelo card lleve declaración de prueba y no sólo declaración; sostenibilidad字段(Jouneaux 等人 2025 7 月) 新增碳、水和计算能足迹,对应新兴 ISO 标准.

### Desarrollo de las actividades 2024-2025

- **CardGen (Liu et al. 2024).**Generación automática de tarjetas de modelo a través de LLM; informa de mayor objetividad que muchas tarjetas de autor humano en los campos estandarizados de Mitchell 2019.
- **Download correlation (Liang et al. 2024).**Las tarjetas de modelo detalladas se correlacionan con tasas de descarga hasta un 29% más altas en la presión de adopción de HF  ahora está impulsada por el mercado, no solo por el cumplimiento.
- **Laminator (Duddu et al. 2024).**Las certificaciones verificables a través de firmas TEE / criptográficas de hardware permiten que la tarjeta modelo lleve una prueba de reclamación, no solo una reclamación.
- **Sustainability (Jouneaux et al. July 2025).**Adiciones para la huella de carbono, agua y energía computacional; estándares ISO emergentes.
- **Regulatory cards.**La Ley de IA de la UE (lección 24) del capítulo de transparencia del Código de Prácticas de la GPAI requiere que las tarjetas modelo sean un artefacto de cumplimiento.

### Donde esto encaja en la Fase 18

Las lecciones 24-25 son las capas reguladoras y CVE. La lección 26 es la capa de documentación. La lección 27 es la gobernanza de datos de capacitación, que es la hoja de datos en aguas al margen. La lección 28 es el ecosistema de investigación que produce evaluaciones referenciadas en tarjetas.

> Las lecciones 24-25 son la supervisión y la CVE 层――Ley 26 es la documentación 层――Ley 27 es el entrenamiento de la gestión de datos――Ley 28 es la producción de tarjetas de referencia para evaluar el estudio de los sistemas vivos―

> **【拓展：可验证证明 → Laminator】**Laminator (Duddu et al. 2024) utiliza hardware TEE / firma de 加密 para lograr la prueba de validación que permite que el modelo de tarjeta lleve una declaración de prueba y no sólo una declaración. Por ejemplo, un modelo de tarjeta puede llevar una prueba de加密 de "la tasa de precisión en el conjunto de datos X es de Y%", el verificador puede revisar la prueba sin necesidad de volver a aplicar la evaluación. Esto es especialmente importante para la regulación de la ley de IA de la UE, lección 24.

## Usalo.
```figure
an-card-scopes
```

## Usalo

`code/main.py`Generar una tarjeta de modelo mínima, una hoja de datos y una tarjeta de sistema para un despliegue de juguete. cada uno sigue la estructura de sección canónica.

> `code/main.py`Para la implementación de los juegos se genera el modelo más pequeño de la tarjeta de juego, el mapa de datos y el sistema de juego. Cada uno sigue la estructura de los capítulos estándar.

## Envíalo .

Esta lección produce`outputs/skill-card-audit.md`. Dado un modelo de tarjeta, hoja de datos o tarjeta de sistema, audita la cobertura de las secciones, la desagregación numérica y la presencia de certificados verificables.

> 本课产 出  `outputs/skill-card-audit.md` una determinada tarjeta de modelo, tabla de datos o tarjeta de sistema, capítulo de auditoría, desglose de valores y si existe una prueba verificable.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`- Inspeccionar las tarjetas generadas. Identificar las secciones débiles (sólo para los titulares de lugar) y especificar qué pruebas las fortalecerían.

2. Extendiendo la tarjeta modelo con un análisis cuantitativo desagregado en dos grupos demográficos (lección 20).

3. Oreamuno et al. 2023 sobre la tasa de adopción del 0,3%. Proponer un cambio estructural en la especificación del modelo de tarjeta que aumentaría la adopción de consideraciones éticas.

4. Laminator (Duddu et al. 2024) utiliza TEEs para certificaciones verificables. Diseñar un campo de tarjeta modelo que lleve una certificación criptográfica de un resultado de evaluación y describa el papel del verificador.

5. Escriba una tarjeta de sistema (tarjeta de sistema, no tarjeta modelo) para uno de sus proyectos anteriores o una implementación hipotética.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Model Card | "the Mitchell card" | Mitchell et al. 2019 standard documentation for ML models |
| Datasheet | "the Gebru datasheet" | Gebru et al. 2018 standard documentation for datasets |
| Data Card | "the Pushkarna card" | Google 2022 modular layered data documentation |
| System Card | "the deployment card" | End-to-end AI system documentation including safety stack |
| Boundary object | "different readers, one doc" | Data Cards framing: same document serves diverse audiences |
| Verifiable attestation | "the Laminator attestation" | Cryptographic or TEE proof attached to a documentation claim |
| Sustainability field | "carbon / water footprint" | Emerging 2025 addition for environmental accounting |

## Más Leer más Leer más

- [Mitchell et al. — Model Cards for Model Reporting (arXiv:1810.03993, FAT* 2019)](https://arxiv.org/abs/1810.03993) la tarjeta modelo canónica
- [Gebru et al. — Datasheets for Datasets (CACM 2021, arXiv:1803.09010)](https://arxiv.org/abs/1803.09010) papel de hoja de datos
- [Pushkarna et al. — Data Cards (Google 2022)](https://arxiv.org/abs/2204.01075) Documentación de datos en capas
- [Sidhpurwala et al. — Blueprints of Trust (arXiv:2509.20394)](https://arxiv.org/abs/2509.20394) Formalización de la tarjeta de sistema
