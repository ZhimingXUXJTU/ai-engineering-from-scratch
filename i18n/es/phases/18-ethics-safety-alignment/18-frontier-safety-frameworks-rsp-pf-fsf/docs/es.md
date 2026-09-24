# Frontier Safety Frameworks  RSP, PF, FSF  framework  Frontier Safety Frameworks  Frontier Safety Frameworks  Frontier Safety Frameworks  Frontier Safety Frameworks   RSP, PF, FSF   marco RSP

> Tres marcos principales de laboratorio definen la gobernanza de la capacidad fronteriza en la industria para 2026. La Política de Escalación Responsable Antropical v3.0 (febrero 2026) introduce niveles de seguridad de IA (ASL-1 a ASL-5+), basados en niveles de bioseguridad, con ASL-3 activado en mayo de 2025 para modelos relevantes para CBRN. OpenAI Preparedness Framework v2 (abril 2025) define cinco criterios para las capacidades rastreadas y separa los informes de capacidades de los informes de salvaguardias. DeepMind Frontier Safety Framework v3.0 (septiembre 2025) introduce niveles críticos de capacidad incluyendo una nueva CCL de manipulación perjudicial. Los tres ahora incluyen cláusulas de ajuste de competencia que permiten el aplazamiento si los laboratorios de pares envían sin garantías comparables. La alineación entre laboratorios sigue siendo estructural y no terminológica: "Tresos de capacidad", "Tresos de alta capacidad" y "Niveles de capacidad crítica" denotan construcciones análogas.

> **【中文解读】**Este capítulo presenta el marco de seguridad de la vanguardia RSP antropológico OpenAI Preparedness DeepMind FSF 等 Raducción de seguridad en comparación  Tres marcos de laboratorio definen la gestión del sector de la vanguardia de capacidad de 2026 ASL-3 Relacionado a CBRN Relacionado a modelos Case de seguridad Es un caso de escritura, en el que se considera que la seguridad es aceptable bajo la hipótesis de que la mejor situación se pueda encontrar en la prueba de la implementación 

> **【拓展：竞争调整条款 → 竞赛动态】**Todos los tres marcos contienen disposiciones de ajuste de competencia que permiten que los competidores envíen el tiempo de retraso en caso de que no haya garantías comparables. Los críticos consideran que esto crea una base de competencia: si tres laboratorios están en violación de la competencia, el equilibrio se desplaza hacia la violación. Los defensores consideran que los métodos alternativos (la garantía única) producen resultados más pobres cuando la conciencia de seguridad de los laboratorios de violación es menor.

**Type:** Learn | **类型:** 学习
**Languages:** none | **语言:** 无
**Prerequisites:** Phase 18 · 17 (WMDP), Phase 18 · 07-09 (deception failures) | **前置知识:** Phase 18 · 17 (WMDP), Phase 18 · 07-09 (欺骗失败)
**Time:** ~75 minutes | **时间:** ~75 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 18·17(WMDP) ‧Fase 18·07-09(欺骗三角) ・・・三大前沿实验室安全框架横向对比(与Fase 15·19-20 互补) ・・・
> ¿ Qué es esto ?**【类比】**Seguridad marco = "AI 实验室的生物安全等级"―Antropic RSP v3.0(ASL-1 hasta ASL-5+, similar a BSL 生物安全);OpenAI PF v2(5 跟踪能力+能力報告/保障報告分离);DeepMind FSF v3(关键能力等级+操纵 CCL)―ASL-3 已 2025.5 激利用于 CBRN──三家都加"竞争调整"条款若行无类似保障可暂缓──

## Objetivos de aprendizaje

- Describa la estructura de nivel ASL de Anthropic y qué activó ASL-3.

> Descripción de la estructura de nivel ASL de Anthropic y qué activó ASL-3:

- Nombre de los cinco criterios de OpenAI Preparedness Framework v2 para las capacidades rastreadas.

> 列出 OpenAI Preparedness Framework v2  Capacidad de seguimiento de cinco criterios。

- Describa la estructura de nivel de capacidad crítica de DeepMind y el CCL de manipulación dañina.

> Describir las capacidades clave de la Mente Profunda, la estructura y el manejo nocivo de la CCL.

- Explicar las cláusulas de ajuste de competidores y por qué son importantes para la dinámica de la raza.

> 解释竞争调整条款 y su impacto sobre el comportamiento de la competencia¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

- Definir un caso de seguridad y describir la estructura de tres pilares (monitoreo, ilegabilidad, incapacidad).

> 定义安全案例并描述三支柱结构(monitoreo、不可读性、无能)

## El problema es el problema .

Las lecciones 7-17 establecen que el engaño es posible, existe capacidad de doble uso y la evaluación tiene límites.
- Define los umbrales para cuando se requieran nuevas salvaguardias.
- Definir las evaluaciones requeridas antes de escalar.
- Describe cómo es un caso de seguridad.
- Maneja el problema dinámico de la carrera (si los competidores se embarcan sin salvaguardas, ¿qué hace?).

> Lecciones 7-17 establecen que el engaño es posible, que la capacidad de uso doble existe, que la evaluación está limitada, que los laboratorios que poseen modelos de capacidad de vanguardia necesitan una estructura de gobierno interna: definir cuándo se necesita un nuevo valor de garantía, evaluar las necesidades de expansión, diseñar casos de seguridad, problemas de competitividad.

Los tres marcos 2025-2026 son el estado de la técnica  imperfecto, evolucionando y alineado lo suficiente entre los laboratorios que la pregunta de gobernanza es ahora si los marcos son adecuados, no si existen.

> Tres marcos 2025-2026 son las tecnologías más avanzadas  imperfectas  en desarrollo  a través de laboratorios suficientemente preparados, el problema de gobierno ahora es si el marco es suficiente o si no existe 

## El concepto.

> **【中文解读】** ASL  estructura de RSP antropico v3.0:ASL-1 非前沿模型;ASL-2 当前前前沿基线;ASL-3 大幅更高的灾难性滥用风险(CBRN),2025年 5月激活;ASL-4 AI R&D-2 跨越值(可自动化进入级 AI研究);ASL-5+ 高级 AI R&D(公开加速有效扩张)──v3.0 新增前沿安全路线图 (图) 季度风险报告 (图) 部分外部审查) 分分 AI R&D 拆分 R&D-2 和 R&D-4──

### Política de escalación responsable antropófica v3.0 (febrero 2026)

Estructura de las LSA:
- ASL-1: no es un modelo fronterizo (sumo por línea de base más débil que fronteriza).
- ASL-2: línea de base actual de las fronteras; desplegada con las garantías habituales.
- ASL-3: riesgo sustancialmente mayor de abuso catastrófico; capacidades relevantes para el CBRN. Activado mayo de 2025.
- ASL-4: AI R&D-2 cruzando el umbral; modelos que pueden automatizar la investigación de IA de nivel de entrada.
- ASL-5+: modelos avanzados de I+D de IA que aceleran dramáticamente la escalabilidad efectiva.

> ASL 结构:ASL-1 非前沿模型;ASL-2 当前前沿基线;ASL-3 大幅更高的灾难性滥用风险(CBRN),2025 年 5 月激活;ASL-4 AI R&D-2 跨越值;ASL-5+ 高级 AI R&D──

Nuevo en la versión 3.0:
- Mapa de ruta de seguridad fronteriza (publicado en forma redactada).
- Informe de riesgos (trimestralmente, algunos revisados externamente).
- La I+D de la IA se desagrega en I+D-2 y I+D-4.
- Una vez que se cruza la IA R&D-4, se requiere un caso de seguridad afirmativo, identificando los riesgos de desalinamiento de los modelos que persiguen objetivos desalinados.

> v3.0 新增:前沿安全路线图 (图) 公開修订版) 季度风险报告 (季度风险报告) 部分外部审查) 、AI R&D 拆分为R&D-2 和R&D-4、R&D-4 跨越后需要肯定性安全案例──

> **【拓展：OpenAI PF v2 → 五项追踪标准】**Criterio de capacidad de seguimiento de OpenAI: 1) razonable existe un modelo de amenaza razonable; 2) puede evaluarse la experiencia evaluada posible; 3) grave  daño grande; 4) nuevo  neto no tiene riesgo de aumentar; 5) inmediato o irreparable  daño rápidamente ocurrir o no puede ser revocado;.

### Marco de preparación de OpenAI v2 (15 de abril de 2025)

Cinco criterios para las capacidades de seguimiento:
- **Plausible.**Existe un modelo razonable de amenaza.
- **Measurable.**Es posible una evaluación empírica.
- **Severe.**El daño es grande.
- **Net-new.**No es un riesgo preexistente en escala.
- **Instantaneous-or-irremediable.**El daño ocurre rápidamente o no se puede hacer reparar.

>  5 criterios de capacidad de seguimiento: razonable, medible, grave, nuevo, inmediato o irreparable.

Las capacidades que cumplen con los cinco son rastreadas.

> 满足所有五项的能力被追踪,其他不追踪──

Otras estructuras de PF v2:
- Los informes de capacidades (qué puede hacer el modelo) y los informes de salvaguardias (qué controles existen) se separarán.
- Las revisiones del Grupo Asesor de Seguridad.
- El liderazgo aprueba; el Comité de Seguridad y Seguridad de la Junta supervisa.
- "Cláusula de ajuste": OpenAI podrá reducir los requisitos si otro laboratorio no dispone de garantías comparables.

> PF v2 其他 estructuras: informe de capacidad de separación y de garantía, informe de grupo de asesoramiento sobre seguridad, revisión de los miembros de la dirección, aprobación de los miembros de la dirección, control de la comisión de seguridad, "调整条款" (en inglés).

### Marco de seguridad de las fronteras de DeepMind v3.0 (septiembre 2025)

Nivel de capacidad crítica (CCL) por dominio:
- El aumento de las armas biológicas
- El aumento de la seguridad informática
- ML Aceleración de la I+D
- Manipulación dañina (nueva en la versión 3.0): modelos que podrían cambiar sustancialmente las creencias/comportamiento en contextos de alto riesgo.

> 按领域关键能力级别(CCL): desarrollo de armas biológicas, desarrollo de redes, ML I+D, acelerar, manipular peligrosamente las armas de fuego, v3.0 新增)

V2.0 (febrero 2025) añadió una sección de Alineación engañosa y niveles de seguridad más altos para CCL de I+D de ML.

> V2.0 añadió una mayor seguridad de la R&D CCL y la parte de engaño.

### Alineación transversal de laboratorio

- "Trescales de capacidad" antropópica.
- "Niveles críticos de capacidad".
- OpenAI "Trescos de alta capacidad".

> Los "Tresos de Capacidad" Antropicos, la "Mente profunda, los niveles de Capacidad crítica" y la "Tresas de Capacidad"

No hay terminología estándar para la industria. Estructuralizada: tres niveles de capacidad fronteriza con criterios de evaluación publicados.

> 没有行业标准术语──结构上对齐:三层前沿能力、发布评估标准、竞争调整条款──

> **【中文解读】**Seguridad casos tres pilares estructura: 1) control Si ocurre mal comportamiento, ¿podemos detectar? 2) inaudible ¿Está el modelo carente de capacidad para ejecutar un plan de daño continuo? 3) inaudible ¿Está el modelo carente de capacidad para causar daño relacionado?

### Casos de seguridad

Un caso de seguridad es un argumento escrito de que una implementación es aceptablemente segura bajo los peores supuestos.

> El caso de seguridad es el de la escritura, que se despliega en la peor de las hipótesis de seguridad aceptable.

- **Monitoring.**¿Podemos detectar el mal comportamiento si ocurre?
- **Illegibility.**¿El modelo carece de la capacidad de ejecutar un plan coherente para causar daño?
- **Incapability.**¿El modelo carece de la capacidad de causar el daño en cuestión?

> **监控：**Si ocurre mal comportamiento, ¿podemos comprobar?**不可读性：**¿Es que el modelo carece de capacidad para ejecutar un plan de daño continuo?**无能：**¿Es que el modelo carece de capacidad para causar daños?

Los casos de seguridad diferentes tienen como objetivo diferentes pilares. Para un caso de ASL-3 CBRN, la incapacidad (a través del no aprendizaje) es el objetivo principal. Para la alineación engañosa, el monitoreo y la ilegibilidad son objetivos. Para el ciberelevación, los tres son relevantes.

> Los casos de seguridad diferentes se centran en diferentes pilares: ASL-3 CBRN  casos principalmente en el no-aliento                                                                                                                                                                                                                                                 

### El problema de la dinámica de la raza

Las cláusulas de ajuste de competidores son controvertidas. Los críticos argumentan que crean una carrera hacia el fondo: si los tres laboratorios reducen los requisitos cuando un competidor falla, el equilibrio se desplaza hacia la deserción.

> 竞争调整条款有争议── los críticos consideran que crean una competencia: si tres laboratorios están en violación de los requisitos de los competidores, el equilibrio hacia la violación se desplaza.

El Reino Unido, CAISI y la Oficina de Inteligencia Artificial de la UE (lección 24) son sus homólogos de gobernanza externa.

> El marco de los laboratorios es voluntario; el marco de la regulación está surgiendo.

### Donde esto encaja en la Fase 18

Las lecciones 17-18 son la capa de medición y gobierno en la parte superior del engaño y los análisis del equipo rojo. Las lecciones 19-24 cubren el bienestar, el sesgo, la privacidad, el marcado de agua y la estructura regulatoria. La lección 28 mapea el ecosistema de investigación (MATS, Redwood, Apollo, METR) que operacionaliza las evaluaciones.

> Las lecciones 17-18 son las medidas y la gestión de la analítica de la engaño y la red team. Las lecciones 19-24 abarcan la estructura de beneficios, prejuicios, privacidad, marcas y regulación.

> **【拓展：跨实验室对齐 → 结构性而非术语性】**Tres marcos en el término no coinciden pero estructuralmente se encuentran en la misma:Antropic "Capacity Thresholds" = DeepMind "Critical Capacity Levels" = OpenAI "High Capacity Thresholds"── tres niveles de capacidad de vanguardia、 publicar normas de evaluación、 competencia调整条款结构趋同──UK AISI, US CAISI y EU AI Office (Leyción 24) es un marco externo de gestión frente a la respuesta―; el marco de laboratorio es voluntario; está surgiendo un marco de regulación―.

## Usalo.
```figure
al-asl-ladder
```

## Usalo

No hay código para esta lección. Lea las tres fuentes primarias: RSP v3.0, PF v2, FSF v3.0. Mapa de la estructura de niveles de cada laboratorio a los demás y identifique un umbral que cada laboratorio define que los otros no.

> Este curso no tiene código. Lee tres fuentes principales: RSP v3.0 、PF v2 、FSF v3.0 ‧.

## Envíalo .

Esta lección produce`outputs/skill-framework-diff.md`. Dado un marco de seguridad o una nota de liberación, compara las definiciones de umbral del marco, las evaluaciones requeridas y la estructura del caso de seguridad con respecto a RSP v3.0, PF v2, FSF v3.0 y las brechas transversales de laboratorio.

> 本课产 出  `outputs/skill-framework-diff.md` Establecer un marco de seguridad o una declaración de publicación, definir su valor, evaluar y evaluar la estructura de los casos de seguridad con RSP v3.0PF, v2 ̊ FSF v3.0 comparado, marcando las diferencias entre los laboratorios ̊

## Los ejercicios.

1. Lea RSP v3.0, PF v2 y FSF v3.0. Compile una tabla del umbral de CBRN de cada laboratorio, el umbral de I+D de IA de cada uno y la evaluación previa a la implementación requerida de cada uno.

2. La cláusula de ajuste de competidores se encuentra en los tres marcos (2025+). Escriba un párrafo argumentando por ella; escriba un párrafo argumentando en contra. Identifique la suposición de la que depende cada posición.

3. Diseñar un caso de seguridad para un modelo que cruce el umbral de I+D-4 de la IA de Anthropic. Nombre la evidencia que requiere cada uno de los tres pilares (monitoreo, ilegibilidad, incapacidad).

4. La FSF v3.0 de DeepMind introduce una CCL de Manipulación Dañina. Propón tres mediciones empíricas que indicarían que un modelo ha cruzado este umbral.

5. Lea los "Elementos comunes de las políticas de seguridad de la IA fronteriza" (2025) del METR. Nombre las tres convergencias más fuertes entre laboratorios y las dos mayores divergencias.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| RSP | "Anthropic's framework" | Responsible Scaling Policy; ASL tiers; v3.0 February 2026 |
| PF | "OpenAI's framework" | Preparedness Framework; five criteria; v2 April 2025 |
| FSF | "DeepMind's framework" | Frontier Safety Framework; CCLs; v3.0 September 2025 |
| ASL-3 | "biosafety level 3-analog" | Anthropic tier for CBRN-relevant capabilities; activated May 2025 |
| CCL | "critical capability level" | DeepMind's threshold construct; per-domain |
| Safety case | "the formal argument" | Written argument that deployment is acceptably safe under worst-case U |
| Adjustment clause | "competitor defection allowance" | Framework provision for reducing requirements if competitors ship without comparable safeguards |

## Más Leer más Leer más

- [Anthropic — Responsible Scaling Policy v3.0 (February 2026)](https://www.anthropic.com/responsible-scaling-policy) niveles de ASL, mapas de ruta, desagregación de la I+D de la IA
- [OpenAI — Updating the Preparedness Framework (April 15, 2025)](https://openai.com/index/updating-our-preparedness-framework/) cinco criterios, cláusula de ajuste
- [DeepMind — Strengthening our Frontier Safety Framework (September 2025)](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) CCL v3.0, Manipulación perjudicial
- [METR — Common Elements of Frontier AI Safety Policies (2025)](https://metr.org/blog/2025-03-26-common-elements-of-frontier-ai-safety-policies/) Comparación entre laboratorios
