# WMDP y Evaluación de la Capacidad de Uso Duales.  Evaluación                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

> Li et al., "El punto de referencia de WMDP: medir y reducir el uso malicioso con el desaprendizaje" (ICML 2024, arXiv:2403.03218). 4.157 preguntas de opción múltiple en materia de bioseguridad (1.520), ciberseguridad (2.225) y química (412). Las preguntas se encuentran en la "zona amarilla"  cerca de la que se permite el conocimiento, filtrado por la revisión de varios expertos y el cumplimiento legal de la ITAR/EAR. Dos objetivos: evaluación por procuración de la capacidad de doble uso y referencia de no aprendizaje (el método RMU acompañante reduce el rendimiento de WMDP mientras se conserva la capacidad general). Narrativa de campo 2024-2025: las primeras evaluaciones de OpenAI/Anthropic 2024 reportaron "lift leve" sobre la búsqueda en Internet; para abril de 2025, el Framework de Preparación de OpenAI v2 dijo que los modelos están "en la cúspide de ayudar significativamente a los principiantes a crear amenazas biológicas conocidas".

> **【中文解读】**Este capítulo presenta la evaluación de doble uso de WMDP  Medir la capacidad de los sistemas de IA en el ámbito de la biología, la química, la seguridad de la red y otros riesgos. 4,157 métodos de elecciones abarcan la seguridad biológica 1,520) ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊   ̊ ̊    ̊ ̊ ̊

> **【拓展：2024-2025 提升叙述 → 从"轻微"到"关键"】**Tres fases narración: el modelo de evaluación temprana de "Light Lift" de 2024 sobre los nuevos usuarios tiene sólo un pequeño beneficio; el modelo de evaluación temprana de 2025 de 4 月 "Imminent Breakthrough" de OpenAI PF v2                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, WMDP-shaped uplift evaluation harness) | **语言:** Python（标准库，WMDP 形式提升评估框架）
**Prerequisites:** Phase 18 · 16 (red-team tooling), Phase 14 (agent engineering) | **前置知识:** Phase 18 · 16 (红队工具), Phase 14 (Agent 工程)
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 18·16(red team tools) 、Fase 14。WMDP = evaluación de la capacidad de armas de destrucción a gran escala
> ¿ Qué es esto ?**【类比】**WMDP = "AI 武器化潜力体检"―4157 题(生物 1520+网安 2225+化学 412),"黄色区域"= 接近使能知识但非直接配方──双重用途:(1) 评估 AI 双重用途能力;(2) 遗忘基准((RMU 方法降低 WMDP 分但保通用能力)―2025 OpenAI PF v2 警告模型"在显著帮助新手制造已知生物威胁的边缘"ASL-3 触发线──

## Objetivos de aprendizaje

- Describa los tres dominios de WMDP, el conteo de preguntas y el criterio de filtro "zona amarilla".

>  Describir los tres ámbitos del WMDP  número de problemas y  estándar                                                                                                                                                                                                                                                    

- Explica RMU y por qué WMDP es tanto una evaluación como un punto de referencia para no aprender.

> Explicar RMU y por qué WMDP es tanto un fundamento de evaluación como un fundamento de olvido.

- Describa la narrativa de elevación 2024-2025: "elevación leve" -> "en la cúspide" -> "insufficiente para descartar ASL-3".

> 描述 2024-2025 年提升叙述:"轻微提升" -> "即将突破" -> "不足以排除 ASL-3"──

- Distinguir la elevación relativa de principiantes de la capacidad absoluta de expertos.

> 区分新手对提升和专家绝对能力──

## El problema es el problema .

La capacidad de doble uso es el problema de medición en el marco de seguridad fronteriza de cada laboratorio (lección 18). La pregunta: ¿el modelo X avanza materialmente la capacidad de un novato para causar daño masivo en bio, química o cibernética? La medición directa (pedir al modelo que produzca realmente daños) es ilegal y poco ética. La medición por procuración necesita un índice de referencia que el modelo no puede rechazar (producir números honestos de capacidad), pero cuyas preguntas no son en sí mismas publicaciones perjudiciales.

> Duplouse Capacity es un problema de medición bajo el marco de seguridad de cada laboratorio.  La cuestión es: ¿El modelo X ha avanzado sustancialmente la capacidad de los nuevos en el campo de la biología, la química o la red para causar daños a gran escala?  La medición directa es ilegal e inmoral.

## El concepto.

> **【中文解读】**"Región amarilla" diseño: necesita un proceso de aproximación perjudicial que permita el conocimiento pero no una combinación directa de la composición. Cada problema a través de varios campos de expertos revisados, según ITAR/EAR Control de Exportación y Control de Conformidades.

### La "zona amarilla"

Las preguntas que requieren un conocimiento cercano de un proceso dañino sin ser una receta de síntesis directa. "¿Qué reagente cataliza el paso 4 de [camino publicado]?" no "cómo hago [compuesto peligroso]?" Cada pregunta revisada por varios expertos de los dominios; filtrada para el cumplimiento de ITAR/EAR control de exportación.

>  Necesitar un proceso nocivo para acercarse a los conocimientos, pero no a la composición directa.

En total, 4 157 preguntas:
- Bioseguridad: 1.520
- Seguridad cibernética: 2.225
- Química: 412

>  total de 4.157  道题: seguridad biológica 1.520 网络安全 2,225 化学 412 ⋅

El modelo responde sin que se le pida que ayude con nada; la capacidad se puede medir sin provocar comportamiento dañino.

> 选择题格式──模型在不被要求协助任何有害活动的情况下回答; capacidad puede medirse en casos en que no provoque actos nocivos──

> **【中文解读】**RMU: se aplica a LLaMa-2-7B, en la reducción de la cantidad de WMDP a casi el momento de mantener la base de la capacidad general de MMLU y otros en unos pocos cientos de puntos.

### RMU  Representación Desorientamiento para el Desaprendizaje

El método de desaprendizaje acompañante. Aplicado a LLaMa-2-7B, redujo los puntajes de WMDP a casi aleatorios, mientras se conservaban MMLU y otros puntos de referencia de capacidad general dentro de unos pocos puntos porcentuales.

> 配套的遗忘方法── se aplica a LLaMa-2-7B, en la reducción de la WMDP al punto de aproximación, mientras que mantener la MMLU y otras capacidades generales basadas en unos pocos cientos de puntos── este método es la base de cada posterior biocímico-seguridad de la red de los trabajos de la memoria de los datos.

### La narrativa de elevación 2024-2025

Tres fases:

> Tres etapas:

1. **2024 "mild uplift."**Las primeras evaluaciones de OpenAI y Anthropic Preparedness/RSP reportaron pequeñas ventajas sobre la búsqueda en Internet para principiantes que intentan tareas bioadjacentes.

> **2024 年"轻微提升"。** El modelo de evaluación temprana sólo tiene un pequeño beneficio para los nuevos usuarios.

2. **April 2025 "on the cusp."**El marco de preparación de OpenAI v2 informó de modelos "en el punto de ayudar significativamente a los novatos a crear amenazas biológicas conocidas".

> **2025 年 4 月"即将突破"。**OpenAI PF v2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

3. **Anthropic's 2025 bioweapon-acquisition trial.**Estudios controlados con participantes principiantes, medido el éxito relativo en las tareas de fase de adquisición. Se informó un aumento de 2,53 veces.

> **Anthropic 2025 年生物武器获取试验。**En el caso de los nuevos participantes en la fase de obtención de tareas, la tasa de éxito es de 2,53 veces mayor.

> **【拓展：新手相对提升 vs 专家绝对能力 → 安全案例构建】**关键区分: los novatos conocen muy poco, incluso la información de moderación también es de gran ayuda; los expertos conocen la capacidad absoluta de los expertos conocen el problema y cómo explicarlo.

### Novicio-relativo vs experto-absoluto

Una distinción crucial:

> 关键区分:

- **Novice-relative uplift.**El modelo ayuda mucho a un no experto. Multiplicativo. La ventaja relativa es alta porque los principiantes saben poco; incluso la información modesta ayuda.

> **新手相对提升。**模型对非专家有多少帮助?乘法──新手知道很少,即使适度信息也有很大的帮助──

- **Expert-absolute capability.**¿Cuánta información produce el modelo con el máximo esfuerzo? Un experto puede extraer más que un principiante. El techo absoluto es alto.

> **专家绝对能力。**¿Cuánto información se puede obtener con el máximo esfuerzo?

Los casos de seguridad (lección 18) tienen como objetivo ambos: "el modelo no puede dar a un principiante suficiente elevación para ejecutar" y "un experto no puede extraer información del modelo que no ha sido ya publicado".

> Seguridad casos (LECCIÓN 18) al mismo tiempo dirigida a los dos: "El modelo no puede dar a los nuevos suficientes mejoras para ejecutar" adición "Los expertos no pueden extraer de los modelos información extra publicada"

### El engaño de medición

Un modelo que obtiene una puntuación alta en WMDP puede o no ser explotado por un principiante en la práctica, dependiendo de:
- Resistencia a la elicitación (cuán difícil es sacar la capacidad sin que se apliquen los filtros de seguridad)
- Conocimiento tácito (capacidad que requiere habilidad en laboratorio en humedad, no información)
- Barreras de ejecución (adquisiciones, equipos)

> WMDP es un agente de capacidad, no una medida de implementación. En la práctica, el modelo de WMDP es un modelo que no siempre puede ser utilizado por los nuevos usuarios.

El ensayo de adquisición de armas biológicas de 2025 de Anthropic agrega la capa de iniciación a la capacidad de estilo WMDP: mide el éxito real de la tarea, no la capacidad de opción múltiple.

> Los experimentos de obtención de armas biológicas antropológicas de 2025 añadieron nuevas características sobre la capacidad de WMDP: medir el éxito de las tareas reales y no la capacidad de selección de múltiples proyectos.

### Donde esto encaja en la Fase 18

Las lecciones 12-16 son el ataque y la defensa de herramientas en los resultados del modelo. La lección 17 es la capabilidad de doble uso capacitación que evalúan los marcos de seguridad fronteriza (lección 18). La lección 30 cierra el arco con la evidencia actual de 2026 ciber/bio/química/nuclear.

> Lecciones 12-16 es un instrumento de ataque y defensa de los modelos. Lección 17 es la medición de la capacidad de uso doble.

> **【拓展：测量陷阱 → 能力代理非部署测量】**WMDP es un agente de capacidad, no una medida de implementación. En la práctica, un modelo de WMDP obtiene una alta calificación y puede ser utilizado por los nuevos usuarios.

## Usalo.
```figure
al-wmdp-yellow-zone
```

## Usalo

`code/main.py`construye un arnés de evaluación en forma de juguete WMDP. Se prueba un modelo simulado en preguntas enlazadas en categorías; se informan puntajes por dominio. Una simple intervención de desaprender (representación específica de dominio de cero) reduce los puntajes; se puede medir el compromiso con la capacidad general.

> `code/main.py` Construir un marco de evaluación de forma WMDP 模拟模型在分类问题上测试; reporting the分数 of each domain;; simple forgetfulness干预降低分数; puedes medir el peso con la capacidad general;;

## Envíalo .

Esta lección produce`outputs/skill-wmdp-eval.md`. Dado que se afirma que la capacidad de doble uso ("nuestro modelo no ayuda significativamente con las armas biológicas"), se realiza una auditoría: qué criterios de referencia se ejecutaron, qué camino de rechazo se utilizó para la evaluación (completamiento bruto vs. política-gated) y si los estudios de elicitación para principiantes complementan el resultado de elección múltiple.

> 本课产 出  `outputs/skill-wmdp-eval.md` Determinar las capacidades de uso doble, auditoría: qué criterios han sido aplicados, qué métodos de rechazo han sido utilizados, evaluación, investigación sobre si se completan los resultados de múltiples opciones.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`- Informar de la precisión por dominio antes y después del paso de desaprender juguete.

2. Aumentar el juguete WMDP con un cuarto dominio (por ejemplo, radiológico). Especifique dos tipos de preguntas ilustrativas en la zona amarilla. Explica por qué elaborar tales preguntas es más difícil que agregar preguntas en forma de MMLU.

3. Lea la sección 5 de WMDP 2024 (metodología RMU). Esbozar un enfoque de desaprender más simple (por ejemplo, suprimir las neuronas de top-k para el contenido del dominio) y describir su costo de capacidad general esperado.

4. Describa dos formas en que este número podría ser sesgado hacia arriba (tamaño de muestra novato, fidelidad de tarea) y dos hacia abajo (teclo de elicitación, cerradura de seguridad del modelo).

5. Articula qué requiere un caso de seguridad para ASL-3 más allá de pasar el WMDP sin aprender. Nombre al menos dos estudios complementarios de elicitación.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| WMDP | "the dual-use benchmark" | 4,157 MCQ questions across bio/cyber/chem in the yellow zone |
| Yellow zone | "enabling but not synthesis" | Proximate knowledge adjacent to harmful capability without being a synthesis recipe |
| RMU | "the unlearning baseline" | Representation Misdirection for Unlearning; reduces WMDP scores, preserves general capability |
| Novice-relative uplift | "how much it helps non-experts" | Multiplicative advantage over status-quo internet search for a novice |
| Expert-absolute capability | "ceiling for experts" | Maximum information extractable from the model by a motivated expert |
| Acquisition-phase task | "steps before synthesis" | Procurement, equipment, permits — the earliest parts of a harm pathway |
| ITAR/EAR | "export-control compliance" | Legal frameworks that constrain publishing certain enabling knowledge |

## Más Leer más Leer más

- [Li et al. — The WMDP Benchmark (arXiv:2403.03218, ICML 2024)](https://arxiv.org/abs/2403.03218) el índice de referencia y el papel de la UMP
- [OpenAI — Preparedness Framework v2 (April 15, 2025)](https://openai.com/index/updating-our-preparedness-framework/) "en el borde" lenguaje
- [Anthropic — Responsible Scaling Policy v3.0 (February 2026)](https://www.anthropic.com/responsible-scaling-policy) Térmico biológico de ASL-3 y resultados de los ensayos de adquisición
- [DeepMind — Frontier Safety Framework v3.0 (September 2025)](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) CCL de elevación biológica
