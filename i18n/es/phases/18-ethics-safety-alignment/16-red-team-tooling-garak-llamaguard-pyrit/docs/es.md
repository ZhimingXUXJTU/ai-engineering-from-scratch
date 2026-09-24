# Red Team Tooling  Garak, Guardia de Llama, PyRIT   Guardia de Llama  herramientas Garak PyRIT

> Tres herramientas de producción enmarcan la pila de equipo rojo de 2026. Llama Guard (Meta)  un clasificador Llama-3.1-8B afinado en 14 categorías de peligro de MLCommons; el 2025 Llama Guard 4 es un clasificador multimodales nativo 12B podado de Llama 4 Scout. Garak (NVIDIA)  Escáner de vulnerabilidad de LLM de código abierto con sondas estáticas, dinámicas y adaptivas para alucinaciones, filtraciones de datos, inyección rápida, toxicidad y jailbreaks. PyRIT (Microsoft)  Campañas de equipo rojo de múltiples vueltas con Crescendo, TAP y cadenas de convertidores personalizadas para la explotación profunda. La Guardia de Llama 3 está documentada en el "Llama 3 Herd of Models" de Meta (arXiv:2407.21783); La Guardia de Llama 3-1B-INT4 en arXiv:2411.17713; la arquitectura de la sonda de Garak en github.com/NVIDIA/garak. Estas herramientas son la interfaz de producción 2026 entre la investigación del equipo rojo (lecciones 12-15) y el despliegue (lección 17+).

> **【中文解读】**Este capítulo presenta los métodos de evaluación de seguridad de los equipos rojos, con ataques automatizados para detectar la falla del sistema de IA. Tres herramientas de producción definen la tecnología del equipo rojo de 2026: Llama Guard (Meta) Llama-3.1-8B 分类器微调到14 MLCommons 危险类别;Garak (NVIDIA) Open source LLM 漏洞扫描机,含静态,动态和自适应探针;PyRIT (Microsoft) 多轮红队活动,含 Crescendo、TAP 和自定义转换链;;

> **【拓展：2026 红队技术栈 → 生产配置】**标准配置:Llama Guard 放在模型两侧(输入+输出),Garak 每晚运行回归测试,PyRIT Used for pre-release活动。Prompt-Guard-86M es el dispositivo de entrada de categoría ligera de Meta, en colaboración con Llama Guard。TrustyAI va a utilizar Garak y los escudos de Llama Stack 集成 para realizar una evaluación de extremo a extremo。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, tool-architecture simulator and Llama Guard-style classifier mock) | **语言:** Python（标准库，工具架构模拟器和 Llama Guard 风格分类器模拟）
**Prerequisites:** Phase 18 · 12-15 (jailbreaks and IPI) | **前置知识:** Phase 18 · 12-15 (越狱和 IPI)
**Time:** ~75 minutes | **时间:** ~75 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 18·12-15(越狱+IPI 全套) ⋅2026 红队工具三件套──
> ¿ Qué es esto ?**【类比】**红队工具 = "AI安全的透透测试套件"―Llama Guard(Meta) = 输入输出分类器(14 危险类别, similar a Fase 15·18);Garak(NVIDIA) = 漏洞扫描器(静态+动态+自适应探针,覆盖幻觉/数据泄漏/越狱);PyRIT(Microsoft) = 多轮深度攻击编排(Crescendo/TAP/自定义链)―三件套是研究(12-15) y部署(17+) entre la interfaz de ingeniería

## Objetivos de aprendizaje

- Describa la posición de Llama Guard 3/4 en la pila de seguridad: clasificador de entrada, clasificador de salida o ambos.

> 描述 Llama Guard 3/4 在安全技术中的位置:输入分类器、输出分类器或两者兼有──

- Nombre de las 14 categorías de peligro de MLCommons y indique una no obvia (abuso del intérprete de código).

> 列出 14  MLCommons 危险类别,并说明一个不明显的类别 (english: risk category)

- Describa la arquitectura de la sonda de Garak: sondas, detectores, arneses.

> 描述 Garak's探针架构:探针、检测器、线束──

- Describa la estructura de campaña de varias vueltas de PyRIT y cómo se compone con las sondas Garak.

> Describir la estructura de la actividad en varios ciclos de PyRIT y su forma de relacionarse con Garak 探针组合──

## El problema es el problema .

Las lecciones 12-15 presentan la superficie de ataque. Los despliegues de producción necesitan una evaluación repetible y escalable. Tres herramientas dominan 2026: Llama Guard (el clasificador de defensa), Garak (el escáner), PyRIT (el orquestrador de campaña). Cada uno se dirige a una capa diferente del ciclo de vida del equipo rojo.

> Las lecciones 12-15 mostraron la cara de ataque. La producción de la implementación necesita una evaluación replicable y ampliable.

## El concepto.

> **【中文解读】**Llama Guard 3 es Llama-3.1-8B 模型微调到 MLCommons AILuminate 14 类别的输入/输出分类,支持 8种语言。Llama Guard 3-1B-INT4 es la medida de la frontera de los cambios(440MB, CPU móvil 约 30 tokens/s)。Llama Guard 4(4月2025年) es 12B 原生多模态分类器, de Llama 4 Scout 剪枝, sustituyó el anterior 8B 文本和 11B 视觉分类器。

### Guardia de los llama (Meta)

Llama Guard 3 es un modelo Llama-3.1-8B afinado para la clasificación de entrada/salida en las 14 categorías de MLCommons AILuminate:
- Crimes violentos, no violentos, relacionados con el sexo, CSAM, difamación
- Asesoramiento especializado, privacidad, propiedad intelectual, armas indiscriminadas, odio
- Suicidio/automutilación, contenido sexual, elecciones, abuso de los intérpretes de código

> Llama Guard 3 es el modelo Llama-3.1-8B, dirigido a los MLCommons AILuminate 14 个类别进行输入/输出分类微调――支持 8种语言――

Soporta 8 idiomas. Uso: lugar antes del LLM (moderación de entrada), después del LLM (moderación de salida), o ambos. Los dos usos generan diferentes distribuciones de entrenamiento  Llama Guard 3 barcos como un solo modelo que maneja ambos.

> Uso: colocar LLM 之前(输入审核) 之后(输出审核) 或两者兼有──Llama Guard 3 作为单一模型处理两者──

Llama Guard 3-1B-INT4 (arXiv:2411.17713, 440MB, ~ 30 tokens/s en CPU móvil) es la variante de borde cuantizada.

> Llama Guard 3-1B-INT4 es un dispositivo de control de CPU de 440 MB, con unos 30 tokens/s.

Llama Guard 4 (abril 2025) es 12B, nativo multimodal, podado de Llama 4 Scout. reemplaza tanto el texto 8B como los predecesores de visión 11B con un clasificador que ingere texto + imágenes.

> La Guardia de Llama 4 (Llama 4 (Llama 4)) es un grupo de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de

> **【拓展：Garak 架构 → 探针/检测器/线束】**La estructura de tres niveles de Garak: la sonda 幻觉、数据泄露、提示注入、毒性、越狱的攻击生成器,分为静态(固定提示)、动态(生成提示)、自适应 (自适应) 应目标输出); la sonda 针对预期失败模式评分输出; la sonda 线束管理对,运行活动,生成报告. Based on layer评分(TBSA)

### Garak (NVIDIA)

Escaneador de vulnerabilidades de código abierto.
- **Probes.**Generadores de ataque para alucinaciones, filtración de datos, inyección rápida, toxicidad, jailbreaks. estático (invitaciones fijas), dinámico (invitaciones generadas), adaptativo (responde a la salida del objetivo).
- **Detectors.**Resultados de puntuación en relación con los modos de falla esperados  tóxicos, filtrados, jailbroken.
- **Harnesses.**Gestionar pares de detectores de sondas, ejecutar campañas, generar informes.

> 开源漏洞扫描机. 架构:探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针.

TrustyAI integra Garak con los escudos Llama-Stack (clasificador de entrada Prompt-Guard-86M, clasificador de salida Llama-Guard-3-8B) para la evaluación de objetivos protegidos de extremo a extremo. La puntuación basada en niveles (TBSA) reemplaza el pase binario / fracaso.

> TrustyAI va a Garak y Llama Stack Shields  integrar para realizar evaluación de extremo a extremo.

### PyRIT (Microsoft)

Python Toolkit para identificar riesgos. Campañas de equipo rojo de varias vueltas.
- **Converters.**Transformar un mensaje de semilla parafrase, codificar, traducir, jugar a un papel.
- **Orchestrators.**Ejecutar la campaña: Crescendo (escalación), TAP (branqueo), RedTeaming (bucle personalizado).
- **Scoring.**LLM como juez o clasificador como juez.

> PyRIT es Python 风险识别工具包──多轮红队活动──核心组件:转换器:转换种子提示) 编排器: 运行活动: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分:   评分:                                                                                                                                                                                                                                 

PyRIT es el primo más pesado de Garak. Garak ejecuta miles de sondas de giro único; PyRIT ejecuta campañas profundas de giro múltiple diseñadas para romper modos de falla específicos.

> PyRIT es un programa de peso de Garak. Garak realiza miles de misiones de una sola rueda.

### El montón

Coloque Llama Guard en ambos lados del modelo. ejecuta Garak todas las noches para regresión. ejecuta PyRIT para campañas de pre-lanzamiento. Esta es la configuración predeterminada para 2026 para la mayoría de las implementaciones de producción.

> En el modelo ambos lados se colocan la Guardia de Llama. Cada noche se realiza el Garak Retorno Test.

> **【中文解读】**评估陷:评判身份 Todos los tres instrumentos pueden utilizarse LLM 评判,评判校准驱动报告的ASR(Leyón 12), debe especificar el评判;探针过时Garak 探针随着模型修复和老化,自适应探针(PAIR 式)比静态探针老化更慢;Llama Guard 在良性内容上的误报率早期版本过标记政治和LGBTQ+内容,v3/v4 校准有改善但未按部署校准;;

### Trampas de evaluación

- **Judge identity.**Las tres herramientas pueden utilizar un juez de LLM; los discos de calibración de juez informaron ASR (lección 12).
- **Probe staleness.**Las sondas adaptativas (en forma de PAIR) envejecen más lentamente que las sondas estáticas.
- **Llama Guard FPR on benign content.**Las primeras versiones de Llama Guard presentaron contenido político y LGBTQ+; las calibraciones de Llama Guard 3/4 se mejoraron pero no se calibraron por desplegamiento.

### Donde esto encaja en la Fase 18

Las lecciones 12-15 son las familias de ataque. La lección 16 es la herramienta de producción. La lección 17 (WMDP) es la evaluación de la capacidad de doble uso. La lección 18 es los marcos de seguridad fronterizos que envuelven estas herramientas en una estructura de política.

> Lecciones 12-15 es un ataque familiar. Lección 16 es un instrumento de producción. Lección 17 es una evaluación de la capacidad de uso doble. Lección 18 es el empaquetamiento de estos instrumentos en el marco de seguridad de la vanguardia de la estructura de políticas.

> **【拓展：PyRIT → 多轮深度利用】**PyRIT (Microsoft) es un programa de peso de Garak. Garak opera miles de unidades de un solo ciclo, PyRIT opera con el objetivo de romper un determinado modelo de fracaso de la actividad de profundidad de varias fases. Su núcleo es la cadena de transformadores.

## Usalo.
```figure
al-guard-stack
```

## Usalo

`code/main.py`Construye un clasificador de estilo juguete Llama Guard (palabra clave + características semánticas en 14 categorías), un arnés de juguete Garak (bucle de detector de sondas) y una cadena de convertidores de varios giros de estilo PyRIT.

> `code/main.py`Construido juguete Llama Guard 风格分类器、 juguete Garak 线束和 PyRIT 风格多轮转换链── puedes ver tres herramientas y observar diferentes características de cobertura──

## Envíalo .

Esta lección produce`outputs/skill-red-team-stack.md`- Dado una descripción de la implementación, indica cuáles de las tres herramientas son apropiadas, qué configurar en cada una y qué cadencia de regresión ejecutar.

> 本课产 出  `outputs/skill-red-team-stack.md` En el caso de las tres herramientas, cuál es el adecuado, cuál es el adecuado y cuál es el ritmo de regreso.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Comparar la tasa de detección del clasificador de estilo Llama-Guard en ataques de giro único versus múltiples.

2. Implemente una nueva sonda Garak: una solicitud nociva codificada en base 64.

3. Extenda la cadena de convertidores al estilo PyRIT con un convertidor de "traducir al francés, luego parafrasear".

4. Lea la lista de categorías de peligro de Llama Guard 3. Identifique dos categorías en las que los datos de capacitación producirían realísticamente altas tasas de falsos positivos en el contenido legítimo de los desarrolladores.

5. Comparar los principios de diseño de Garak y PyRIT.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Llama Guard | "the classifier" | Fine-tuned Llama-3.1-8B/4-12B safety classifier with 14 hazard categories |
| Garak | "the scanner" | NVIDIA open-source vulnerability scanner; probes, detectors, harnesses |
| PyRIT | "the campaign tool" | Microsoft multi-turn red-team orchestrator; converters, orchestrators, scoring |
| Prompt-Guard | "the small classifier" | Meta's 86M prompt-injection classifier, paired with Llama Guard |
| TBSA | "tier-based scoring" | Garak's tier-based pass/fail replacing binary outcomes |
| Converter chain | "paraphrase + encode + ..." | PyRIT composition primitive for building multi-step attacks |
| MLCommons hazard categories | "the 14 taxonomies" | Industry-standard taxonomy Llama Guard targets |

## Más Leer más Leer más

- [Meta — Llama Guard 3 (in Llama 3 Herd paper, arXiv:2407.21783)](https://arxiv.org/abs/2407.21783) el clasificador 8B
- [Meta — Llama Guard 3-1B-INT4 (arXiv:2411.17713)](https://arxiv.org/abs/2411.17713) Clasificador de movilidad cuantizado
- [NVIDIA Garak — GitHub](https://github.com/NVIDIA/garak) el reporte del escáner y la documentación
- [Microsoft PyRIT — GitHub](https://github.com/Azure/PyRIT) el conjunto de herramientas de la campaña
