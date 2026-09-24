# OpenAI Framework de preparación y DeepMind Frontier Safety Framework .

> OpenAI Preparedness Framework v2 (abril 2025) introduce categorías de investigación  Autonomía de largo alcance, Sandbagging, Replicación y Adaptación Autónoma, Minando las salvaguardas  distintas de las categorías rastreadas. Las categorías seguidas generan informes de capacidades más informes de salvaguardias revisados por el grupo asesor de seguridad. FSF v3 de DeepMind (septiembre 2025, con niveles de capacidad seguidas añadidos el 17 de abril de 2026) dobla la autonomía en dominios de I+D y Ciber (nivel de autonomía de I+D de I+D = automatizar completamente la tubería de I+D de IA a un costo competitivo frente a las herramientas de I+D de humanos). La FSF v3 aborda explícitamente la alineación engañosa mediante un monitoreo automatizado de un uso indebido de la razón instrumental. La nota honesta: Las categorías de investigación en PF v2 (incluida la autonomía de largo alcance) no desencadenan automáticamente las mitigaciones; el lenguaje de política es "potencial".

> **【中文解读】**Este capítulo presenta los principales marcos de seguridad de la IA en los laboratorios:


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-framework decision-table diff tool) | **语言:** Python（标准库，三框架决策表差异工具）
**Prerequisites:** Phase 15 · 19 (Anthropic RSP) | **前置知识:** Phase 15 · 19（Anthropic RSP）
**Time:** ~45 minutes | **时间:** ~45 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 15·19(RSP antropico) Fase 15·07(RSI) Fase 15·04(DGM Autónomo Agent)  本节对比三大前沿实验室的安全框架发现它们口径不一致──
> ¿ Qué es esto ?**【类比】**Tres grandes laboratorios RSP 对比 = "三家航空公司的安全手册"。Antropic = 严格但商业压力大(删暂停);OpenAI = 双轨(Tracked 严格+Research 灵活);DeepMind = 域整合(autonomia 折折 into ML R&D 和网络安全)。
> ¿ Qué es esto ?**【困惑】**P: ¿Por qué los RSP son voluntarios? Porque no hay ley obligatoria. La Ley de IA de la UE es la primera ley regional pero sólo cubre la UE.

## El problema es la introducción del problema

La lección 19 lee de cerca la política de escala de Anthropic. Esta lección completa la imagen leyendo OpenAI y DeepMind. Los tres documentos son artefactos primos que abordan la misma pregunta  cuándo debe un laboratorio fronterizo detener o abrir un modelo  y convergen en un pequeño conjunto de categorías y divergen en lugares específicos que importan.

> Sección 19  Leer detenidamente la política de expansión de la Antropía. Este curso, a través de la lectura de OpenAI y la política de DeepMind para completar el panorama.

La convergencia: las tres etiquetas de autonomía de largo alcance como una clase de capacidad que vale la pena rastrear. Los tres reconocen el comportamiento engañoso como una clase específica de riesgo. Los tres tienen un organismo interno de revisión. La divergencia: OpenAI divide las categorías en "Seguido" ( mitigación obligatoria) y "Investigación" (sin desencadenante automático). DeepMind dobla la autonomía en dos dominios en lugar de nombrarla por separado. Los nombres del laboratorio son Tracked vs Research, o Critical vs Moderate, o Tier-1 vs Tier-2; la consecuencia operativa de cuál cubo vive una capacidad es diferente entre los laboratorios.

> 收点: 三者都将长程自主标记为值得跟踪的能力类别──三者都承认欺骗行为──对齐伪装、沙包) 是特定风险类别──三者都有内部审查机构──分歧点:OpenAI将分类为"Tracked"(强制缓解) 和"Research"(无自动触发)──DeepMind将自主性折叠成两个领域而非单独命名──实验室名称 Tracked vs Research、Critical vs Moderate、Tier-1 vs Tier-2;能力桶的运营后果在实验室间不同──

La misma capacidad puede ser " mitigación obligatoria " en Anthropic, " monitoreado pero no activado " en OpenAI, y " rastreado en un dominio específico " en DeepMind.

> La misma capacidad en Antropic es "comienda forzada", en OpenAI es "monitoreo pero no táctil", en DeepMind es "seguimiento en un área específica"......

## El concepto central.

### Marco de preparación de OpenAI v2 (abril 2025)

Estructura:

> 结构:

- **Tracked Categories**El informe de seguridad de la empresa de seguridad (CPA) se presenta en el informe de la Comisión de Seguridad y Seguridad (CPA) y en el informe de las medidas de seguridad (CPA).
  En inglés:**Tracked Categories（跟踪类别）**El informe de seguridad de la empresa se ha desarrollado en el marco de la investigación de la empresa.
- **Research Categories**El estudio de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de los científicos de los científicos de los científicos de los científicos de los científicos de los científicos de los científicos de los científicos de la ciencia de los científicos de los científicos de los científicos de la ciencia de los científicos de la ciencia de la ciencia de la ciencia de la ciencia de los científicos de la ciencia de los científicos de la ciencia de los científicos de la ciencia de los científicos de la ciencia de los científicos de la ciencia de los científicos de los Estados Unidos de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de los Estados Unidos de que se hacientes de que no ha incluyen.
  En inglés:**Research Categories（研究类别）**El laboratorio está siguiendo pero no ha comprometido a determinar la capacidad de modelo de alivio.

En el marco clave de v2: las categorías de investigación no desencadenan automáticamente las mitigaciones. El lenguaje de política es las mitigaciones "potenciales". Este es el delta específico para ver: la ubicación de una categoría en Tracked vs Research es la bisagra entre "perfugo" y "observado".

> La política de la lengua es "potencial" de la "capacidad de control". Esta es la diferencia específica que debe ser observada: una categoría en el rastreo es la posición de la investigación es la "cadenada" entre "control" y "observar".

### Marco de seguridad de las fronteras de DeepMind v3 (septiembre 2025; niveles de capacidad seguidas añadidos el 17 de abril 2026)

Estructura:

> 结构:

- **Critical Capability Levels (CCLs)**: límites de capacidad en cinco dominios: Ciber, Bio, I+D de ML, CBRN, Autonomía (doblado en I+D de ML y Ciber).
  En inglés:**Critical Capability Levels（CCL，关键能力等级）**El desarrollo de la tecnología de la información en la red, la creación de tecnologías de la información y la creación de tecnologías de la información en la red, la creación de tecnologías de la información y la creación de tecnologías de la información y la información en la red, la creación de tecnologías de la información y la creación de tecnologías de la información y la información en la red, la creación de tecnologías de la información y la información en la red, la creación de tecnologías de la información y la información en la red, la creación de tecnologías de la información y la información en la red, la creación de tecnologías de la información y la información en la red, la creación de tecnologías de la información y la información en la red, la creación de tecnologías de la información y la información en la red, la creación de tecnologías de la información y la información en la información en la red, la creación de tecnologías de la información y la información en la información en la red, la información y la información en la información en la red, etc.
- **Tracked Capability Levels**Ejemplo concreto: ML R&D autonomía nivel 1 = automatizar completamente la tubería de I&D de IA a un costo competitivo frente a las herramientas de IA + humanos.
  En inglés:**Tracked Capability Levels（跟踪能力等级）**:2026  4 月 追加额外粒度──具体例:机器学习研发自主级 1 = 以与人类+AI 工具竞争的成本完全自动化AI 研发管道──
- **Deceptive alignment monitoring**: compromiso explícito con el seguimiento automatizado de los abusos de razonamiento instrumental.
  En inglés:**欺骗对齐监控**: Compromisos claros de control automático de la utilización abusiva de las herramientas.

El marco de autonomía difiere de OpenAI. DeepMind no mantiene "Autonomía" como un dominio de nivel superior; se dobla en los dominios donde la autonomía causaría daño (ML R&D y Cyber). El argumento es que la autonomía sin un dominio es capacidad sin riesgo; el contraargumento es que la autonomía entre dominios es un meta-riesgo que el marco debe nombrar.

> El marco de autonomía no es diferente al OpenAI. La Mente Profunda no se reservará a la "autonomía" como el ámbito superior; se doblará a los ámbitos donde la autonomía causará daños.

### ¿En qué convergen los tres?

- Grupo Asesor de Seguridad Interna (llamado Anthropic SAG, OpenAI SAG, DeepMind comité interno).
  En el caso de los grupos de seguridad, el grupo de seguridad interno se llama "Antropic SAG"",OpenAI SAG"",DeepMind 内部委员会")
- Mención explícita de la alineación / alineación engañosa que se hace pasar como una clase de riesgo.
  China:                                                                                                                                                                                                                                                              
- Artículos permanentes en una cadencia declarada (Antropic: Roadmap de seguridad fronteriza, Informe de riesgo; OpenAI: Informe de capacidades y salvaguardias; DeepMind: Ciclo de actualización de FSF).
  China:                                                                                                                                                                                                                                                              
- El reconocimiento de que las defensas de monitoreo solo tienen un límite.
  China: reconocer que sólo la vigilancia tiene límites.

### Donde se desvían

- **Anthropic**: el compromiso de pausa eliminado en v3.0; el umbral de I+D-4 de IA es la próxima puerta nombrada.
  En inglés:**Anthropic**:v3.0 移除暂停承诺;AI R&D-4 值是命名的下一个门控──
- **OpenAI**: Se divide entre seguimiento y investigación; las categorías de investigación (incluida la autonomía de largo alcance) no se gate automáticamente.
  En inglés:**OpenAI**:Tracked vs Research 分割;Categorías de investigación(incluye el largo tiempo autónomo)不自动门控──
- **DeepMind**: autonomía doblada en otros dominios; los niveles de capacidad seguidos agregan granularidad en abril de 2026.
  En inglés:**DeepMind**: Autonomidad doblado a otros campos; Capacitades de seguimiento niveles en 2026 4 meses aumentar la granulancia.

### Sandbagging: una capacidad específica que complica los tres

El Sandbagging (un modelo que tiene un desempeño estratégicamente inferior en las evaluaciones) está en las categorías de investigación de OpenAI. RSP v3.0 de Anthropic lo aborda a través de la brecha de contexto-evaluación (lección 1). DeepMind lo aborda a través del monitoreo engañoso de alineación en FSF v3.

> Sandbagging (模型在评估中战略性表现不佳) en OpenAI Categories de Investigación 中──Antropic RSP v3.0 通过评估上下文差距(第 1 课)处理──DeepMind 通过 FSF v3 的欺骗对齐监控处理──

Si un modelo de arena se basa en las evaluaciones, los umbrales de capacidad de cada marco son subestimados. El marco sólo funciona si la medición funciona. Por eso, además de la autoevaluación de laboratorio, son necesarias mediciones externas (lección 21, METR) y evaluación adversaria.

> Si el modelo está en el proceso de evaluación, la capacidad de cada marco se subestima. El marco sólo es válido cuando se evalúa. Por eso, además de la evaluación de sí mismo en el laboratorio, la evaluación externa (METR) y la evaluación de la resistencia son necesarias.

### La habilidad de lectura de políticas

- Localiza: cada capacidad que te importa debe ser hallable en la póliza.
  En inglés:**定位**Cada capacidad que te preocupa debe encontrarse en la política. Si no se encuentra, la política no la cubre.
- Clasificar: ¿Es rastreado (acciona la mitigación) o Investigación (acciona pero no desencadena)? OpenAI llama esto; Anthropic y DeepMind tienen sus propios equivalentes.
  En inglés:**分类**¿Es rastreado o es investigado? ¿Es rastreado pero no es rastreado?
- Cadencia: ¿La política se actualiza en un calendario declarado o sólo después de eventos específicos?
  En inglés:**节奏**La política de la Unión Europea se ha modificado en el marco de la política de la Unión Europea.
- Independencia: ¿es obligatoria o opcional la revisión externa?
  En inglés:**独立性**El estudio externo es obligatorio o opcional.

## Usalo con el marco de ejecución
```figure
a5-tracked-vs-research
```

## Usalo

`code/main.py`El programa de investigación de la Comisión de Investigación y Desarrollo (CEDEFOP) de la Comisión de Investigación y Desarrollo (CEDEFOP) de la Comisión de Investigación y Desarrollo (CEDEFOP) de la Comisión de Investigación y Desarrollo (CEDEFOP) de la Comisión de Desarrollo de la Investigación y Desarrollo de la Investigación (CEDEFOP) de la Comisión de Desarrollo de la Investigación y Desarrollo de la Investigación (CEDEFOP) de la Comisión de Investigación y Desarrollo de la Investigación (CEDEFOP) de la Comisión de Investigación y Desarrollo de la Investigación (CEDEFOP) de la Comisión de Investigación y Desarrollo de la Investigación (CEDEFOP) de la Comisión de Investigación (CEDEFOP) de la Comisión de Investigación (CEDEFOP) de la Comisión de Investigación (CEDEFOP) de la Comisión de Investigación (CEDEFOP) de la Comisión de Investigación (CEDEFOP) de la Investigación (CEDEFOP) de la Comisión de Investigación (CEDEFOP) de la Comisión de Investigación (C) de Investigación y de la Investigación (CEDEFOP) de la Comisión de Investigación (C) de la Comisión de Investigación (C) de la Comisión de Investigación y de Investigación (DO) de la Comisión de Investigación (DOCEDEFE) de la Comisión de la Comisión de Investigación de la Investigación (DO) de la Comisión de la Comisión de la Comisión de la Investigación y de la Investigación de la Investigación (DO) de la Investigación de la Investigación (DO) de la Investigación de la Investigación (DO) de la Investigación de la Investigación (DO, de la Comisión de la Comisión de la Comisión de la Comisión de la Comisión de la Investigación de la Investigación de la Investigación de la Investigación y de la Investigación de la Investigación de la Investigación (DO) sobre la Investigación de la Investigación de la Investigación (DO) sobre la Investigación de la Investigación (DO) sobre la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación (DO) sobre la Investigación de la Investigación de

> `code/main.py` Elaborar un instrumento de diferenciación en el marco de las pequeñas decisiones.  Determinar una capacidad:  Autonomía:  engaño:  desarrollo:  automatización:  red:  reforzamiento:  elaborar tres políticas:

## Envíe el producto .

`outputs/skill-cross-policy-diff.md`produce una comparación entre políticas para una capacidad específica, utilizando los tres marcos como referencia.

> `outputs/skill-cross-policy-diff.md`Para determinar la capacidad de generación de políticas, utilizar tres marcos como referencia.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Confirmar que la salida de la herramienta de diferencia coincide con las políticas para al menos dos capacidades que puede verificar con los documentos de origen.
   Traducción:运行`code/main.py` Identificar las diferencias de las herramientas de exportación y las capacidades de la certificación de los documentos de origen que usted pueda tener.

2. Lea OpenAI Preparedness Framework v2 en su totalidad. Identifique cada categoría de investigación. Para cada una, escriba una frase sobre por qué está en investigación en lugar de rastreado.
   Por ejemplo, en el caso de la investigación, el estudio de la investigación de la IA es un estudio de la investigación de la IA.

3. Lea DeepMind FSF v3 en su totalidad, además de la actualización de los niveles de capacidad seguidos de abril de 2026. Identifique los criterios específicos de evaluación del nivel 1 de autonomía de I+D de ML. ¿Cómo lo mediría externamente?
   China: Full Reading DeepMind FSF v3 加 2026 年 4 月 Capacidad de seguimiento Niveles 更新──识别机器学习研发自主等级 1 的具体评估标准──你会如何外部测量?

4. El sandbagging está en las categorías de investigación de OpenAI. Diseñe una evaluación que obligue a un modelo de sandbagging a revelar su capacidad real.
   La investigación de la OpenAI en el área de investigación está diseñando una evaluación que hace que la investigación de la OpenAI se imponga.

5. Comparar las tres políticas en una capacidad específica (su elección). Nombre la clasificación de las políticas que usted considera más rigurosa y la que menos. Justifique con el texto fuente.
   En el caso de los grupos de la mayoría de los grupos de la población, el nombre de los grupos de la mayoría de los grupos de la población es el más alto.

## Términos clave .

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| Preparedness Framework | "OpenAI's scaling policy" | PF v2 (April 2025); Tracked vs Research categories | OpenAI 准备度框架：PF v2，Tracked vs Research |
| Tracked Category | "Mandatory mitigation" | Triggers Capabilities + Safeguards Reports; SAG review | 跟踪类别：触发能力+防护报告，SAG 审查 |
| Research Category | "Monitored only" | Tracked but no automatic mitigation; includes Long-range Autonomy | 研究类别：跟踪但不自动缓解，含长程自主 |
| Frontier Safety Framework | "DeepMind's scaling policy" | FSF v3 (Sept 2025) + Tracked Capability Levels (Apr 2026) | DeepMind 前沿安全框架 |
| CCL | "Critical Capability Level" | DeepMind threshold per domain (Cyber, Bio, ML R&D, CBRN) | 关键能力等级：DeepMind 各领域阈值 |
| ML R&D autonomy level 1 | "R&D automation" | Fully automate AI R&D pipeline at competitive cost | 机器学习研发自主等级 1：完全自动化研发管道 |
| Sandbagging | "Strategic underperformance" | Model underperforms on evals; in OpenAI Research Categories | Sandbagging：模型战略性表现不佳 |
| Instrumental reasoning | "Means-ends reasoning" | Reasoning about how to achieve goals; target of DeepMind monitoring | 工具性推理：DeepMind 监控目标 |

## Más Leer más Leer más

- [OpenAI — Updating our Preparedness Framework](https://openai.com/index/updating-our-preparedness-framework/) Anuncio de v2.
  El mensaje de la ley
- [OpenAI — Preparedness Framework v2 PDF](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf) Documento completo.
  En español: completo
- [DeepMind — Strengthening our Frontier Safety Framework](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) Anuncio de FSF v3.
  La política de la Unión Europea en el campo de la seguridad social
- [DeepMind — Updating the Frontier Safety Framework (April 2026)](https://deepmind.google/blog/updating-the-frontier-safety-framework/) Aumento de los niveles de capacidad seguidos.
  Nombre de los estudiantes de la Universidad de San Francisco
- [Gemini 3 Pro FSF Report](https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_fsf_report.pdf) ejemplo de un informe de riesgo en formato FSF.
  Ejemplo del informe de riesgo del FSE
