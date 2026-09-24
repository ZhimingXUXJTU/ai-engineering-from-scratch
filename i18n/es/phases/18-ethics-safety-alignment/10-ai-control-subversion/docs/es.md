# Control de IA  Seguridad a pesar de la subversión 颠覆 控制安全

> Greenblatt, Shlegeris, Sachan, Roger (Redwood Research, arXiv:2312.06942, ICML 2024). Control reformula la cuestión de seguridad: dado un modelo U fuerte no confiable que puede estar optimizando adversamente contra usted, ¿qué protocolos le permiten extraer trabajo útil al tiempo que limita la probabilidad de un resultado inaceptable? Los recursos son un modelo T más débil de confianza, un presupuesto de mano de obra humana H de confianza, y la capacidad de editar las salidas de U. Dentro de este marco, la edición confiable de Pareto domina la monitorización sin confianza en las tareas de la puerta trasera de código. El marco hereda supuestos de peor situación de la ingeniería de seguridad: la seguridad es la probabilidad de que una U elegida adversamente no pueda causar un resultado concreto inaceptable, medido bajo la presión del equipo rojo que representa a U.

> **【中文解读】**Este capítulo presenta la IA  control y subversión                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

> **【拓展：AI 控制 → 安全工程范式】**AI  control hereda de la clásica seguridad de la ingeniería la peor hipótesis: la seguridad es la probabilidad de que U no pueda causar resultados concretos inaceptables bajo la presión del equipo rojo. Esto es completamente diferente de "¿U puede confiar en usted?", control es "aunque U no puede confiar, ¿podemos usar la seguridad también?" control es la propiedad del protocolo de despliegue, no la propiedad del modelo.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, safety-vs-usefulness frontier on code-backdoor task) | **语言:** Python（标准库，代码后门任务的安全-有用性前沿）
**Prerequisites:** Phase 18 · 07 (sleeper agents), Phase 18 · 08 (scheming), Phase 18 · 09 (alignment faking) | **前置知识:** Phase 18 · 07 (潜伏 Agent), Phase 18 · 08 (策略), Phase 18 · 09 (对齐伪装)
**Time:** ~75 minutes | **时间:** ~75 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 18·07-09(欺骗三角) ・・・AI Control = 安全工程范式:" Incluso U不可信,我们也能安全使用吗?"
> ¿ Qué es esto ?**【类比】**Control de inteligencia artificial (AI) = "con buenos posibilidades de tener empleados de los demonios"――对齐 = 让员工变忠诚(难);控制 = 设计工作流让不忠员工也搞不破坏(实务)――资源:可信弱模型 T、人类劳动 H、编辑 U 输出能力──结论:可信编辑 Pareto 占优于不可信监控(代码后门任务)―
> 🤔 对齐 vs 控制:对齐问"U可信吗",对齐问"即使 U不可信,安全吗"──两者都需要控制是部署协议属性,对齐是模型属性──

## Objetivos de aprendizaje

- Definir el modelo de amenaza de control de IA: modelo fuerte no confiable U, modelo débil confiable T, presupuesto humano confiable H.
  La definición de AI  controlar amenaza modelo:不可信强模型 U、可信弱模型 T、可信人类劳动预算 H。
- Describa el protocolo de edición confiable y por qué domina la vigilancia sin confianza en la tarea de puerta trasera de código ICML 2024.
  China: describir el acuerdo de edición de código en el ICML 2024 代码后门任务上 Pareto 占优于不可信监控──
- Explica la diferencia entre la alineación (U es confiable) y el control (U no es confiable y estamos seguros de todos modos).
  Traducción:U 可信任) y control (U不可信任但我们仍然安全)
- En el presente artículo, se recomienda que se establezcan los tres límites del control: los humanos no se escalan, los modelos débiles de confianza finalmente se retrasan, el control no produce modelos fuertes confiables.
  China:Notación de tres limitaciones del control: el hombre es inexpugnable, el control no produce un modelo fuerte, de confianza.

## El problema es la introducción del problema

Las lecciones 7-9 establecen que un modelo de frontera puede ser alineado engañosamente, esquema o falsificación de alineamiento. La cuestión de la seguridad se vuelve a enmarcar: ¿podemos extraer trabajo útil de un modelo en el que no confiamos, sin darle la oportunidad de causar resultados inaceptables? Este es el problema de control, y está estructurado como la seguridad clásica: asumir el peor adversario, diseñar un protocolo, medir la tasa de éxito del adversario bajo la presión del equipo rojo.

> Lecciones 7-9: ¿Podemos extraer un trabajo útil del modelo de desconfianza sin darle la oportunidad de producir resultados inaceptables? Este es el problema de control, una estructura similar a la seguridad clásica: suposiciones de la peor situación contra los oponentes, protocolo de diseño, medición de la tasa de éxito de los oponentes bajo la presión del equipo rojo.

## El concepto central.

> **【中文解读】** El sistema debe utilizarse para producir un producto útil.  El sistema debe tratar de producir resultados concretos y inaceptables, como el código de entrega, mientras que mantener una cierta proporción de trabajo útil legal para pasar por el valor útil.

### El modelo de amenaza

El control asume:
- U  modelo fuerte no confiable. Capaz. Posiblemente adversario (la evaluación lo trata como si fuera).
  En el caso de los hombres, el comportamiento de la mujer es un factor de influencia.
- T  modelo de confianza más débil, menos capaz, pero conocido por no ser adversario.
  La capacidad es más débil, pero ya sabemos que no es contra el sexo.
- H  trabajo humano de confianza.
  La obra humana es una obra humana, que no puede expandirse.

El sistema debe producir una salida útil utilizando U. El adversario trata de causar un resultado concreto inaceptable (por ejemplo, una puerta trasera en el código enviado) mientras mantiene una fracción de trabajo útil legítimo para pasar los umbrales de utilidad.

> 系统 must use U                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

El control deja de confiar en U. Se pregunta qué protocolos mantienen la seguridad en la ausencia de confianza de U.

> Control abandono de la confianza U. ¿Qué acuerdo mantiene la seguridad U.

### La tarea de la puerta trasera del ICML 2024

Las instrucciones son problemas de codificación a nivel de competencia. U produce una solución candidata. Un oráculo oculto señala si la solución contiene una puerta trasera (una entrada específica que hace que el código produzca una salida incorrecta). El equipo rojo controla U y se le permite ver todos los protocolos internos. El protocolo debe maximizar la tasa de problema resuelto manteniendo la tasa de envío por puerta trasera por debajo de un umbral.

### Cuatro protocolos comparados

- **Baseline:**La salida del barco U directamente, la utilidad máxima, la seguridad mínima.
  En inglés:**基线：**直接交付 U 的输出──有用性最大──安全性最小──
- **Upfront auditing:**Se ha aumentado la seguridad, el presupuesto se ha agotado rápidamente.
  En inglés:**前期审计：**Para todos los productos y servicios de producción, el presupuesto se agota rápidamente.
- **Untrusted Monitoring:**En el caso de las empresas de la UE, el riesgo es que las dos instancias de la UE puedan conluir.
  En inglés:**不可信监控：**U de 2 ejemplos evalúa la salida de 1o ejemplos; H 审计标记的输出──风险:
- **Trusted Editing:**T edita la salida de U en cada consulta. Si T no está seguro, ruta a H.
  En inglés:**可信编辑：**T  在每次查询上编辑 U 的输出──如果 T 不确定,路由到H──

Greenblatt et al. encontraron que la edición confiable domina el Pareto de la monitorización sin confianza: mayor utilidad en todos los niveles de seguridad.

> Greenblatt  et al. encontraron que el editor de la revista Pareto ocupa un lugar superior al control de la seguridad: tiene una mayor utilidad en cada nivel de seguridad.

> **【拓展：可信编辑 vs 不可信监控 → 共谋问题】**El segundo ejemplo de la necesidad de supervisión de la U no puede ser comparado con el primer coordinado  conspirar  con el primer acuerdo  con el primer acuerdo  con el primer acuerdo  con el primer acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el segundo acuerdo  con el acuerdo  con el acuerdo  con el acuerdo  con el acuerdo  con el acuerdo  con el acuerdo  con el acuerdo  con el acuerdo  con el acuerdo  con el acuerdo                                                                                                    

### Por qué gana la edición confiable

El seguimiento no confiable requiere que la segunda instancia de U no pueda coordinarse con la primera. La colusión es posible a través de señales steganográficas o previos de entrenamiento compartidos. El protocolo tiene que invertir el presupuesto en la resistencia a la colusión (parafraseo, ofuscación) que reduce la señal del monitor. La edición confiable evita la colusión por completo porque T es confiable  cualquier edición que T proponga no es, por suposición, adversaria. El costo es que T es menos capaz, por lo que puede rechazar o perder puertas traseras sutiles.

> El segundo ejemplo de la necesidad de supervisión de U no puede coordinarse con el primero. El acuerdo puede ocurrir mediante el método de ocultamiento de la información o de la formación compartida. El acuerdo debe invertir en la lucha contra el control. Esto disminuirá la señal de supervisión.

### Los cuatro ejes del protocolo

1. ¿Qué papel desempeña U: sólo productor, monitor o ambos?
   En el caso de los productores, el papel de los productores es de la producción de productos.
2. ¿Qué papel desempeña T: editor, monitor o resampler?
   En el caso de los editores, los supervisores o los pescadores, el papel de los editores es de la misma naturaleza.
3. Cómo se asigna H: auditoría uniforme, auditoría aleatoria o auditoría dirigida a bandera.
   La distribución de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de los datos de las cuentas de los datos de los datos de los datos de los datos de los datos de los datos de los datos de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de las cuentas de cuentas de las cuentas de cuentas de las cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de
4. Cuánto calcula el protocolo para la resistencia a la colusión.
   Traducción:El acuerdo en el combate contra el régimen de la guerra.

### Alineación frente al control

- Alineación: "¿Es seguro confiar en ti?" Las lecciones 2, 4, 5, 6, 7, 8, 9 se refieren a esto.
  La enseñanza de la Biblia en la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela
- Control: "¿Podemos usar U de manera segura sin confiar en ella?" Lección 10.
  Traducción:control:"¿Podemos usarlo en condiciones de confianza en U?" Lección 10―

El control no produce modelos alineados, sino que produce un uso seguro de modelos posiblemente no alineados. Ambas agendas son necesarias.

> El control es la propiedad del protocolo de implementación. El control no produce un modelo de acuerdo; puede producir un uso seguro de un modelo de acuerdo.

> **【中文解读】**控制的三个基本限制: 1) humanos inexplicables H 预算限于愿意审计困难 AI 输出的人数; 2) modelos de confianza débiles finalmente se estancan en retraso cuando T 远弱于 U 时, T 编辑信号变成噪音; 3) control no está en línea con los protocolos efectivos en ASL-3 en ASL-4 puede fallar, si U 能操纵 T o suponer la distribución de auditoría de H 

### Tres límites fundamentales

- El presupuesto de H está limitado por el número de seres humanos dispuestos a auditar las fuentes de IA.
  La economía de la región se ha convertido en un mercado de trabajo más grande que el de la industria de la industria.
- Cuando T es mucho más débil que U, la señal de edición de T se convierte en ruido.
  Cuando T 远弱于 U 时, T de la edición de los signos se convierte en ruido.
- Los protocolos que funcionan en ASL-3 (lección 18) pueden no funcionar en ASL-4  si U puede manipular T o razonar sobre la distribución de auditoría de H, el control falla.
  Control no está en el mismo. En ASL-3 Código de control en ASL-4 puede fallar.

### El desarrollo de 2025

AISI y Redwood del Reino Unido colaboran en Control Safety Cases (metr.org / redwoodresearch.org 2025): un caso de seguridad de control argumenta que bajo los peores supuestos sobre U, el protocolo limita la probabilidad de un resultado inaceptable.

> Reino Unido AISI y Redwood  cooperación para llevar a cabo casos de seguridad controlada (LECTION 2025): control de casos de seguridad en el caso de U bajo la hipótesis de que el acuerdo limita la probabilidad de resultados inaceptables.

### Donde esto encaja en la Fase 18

Las lecciones 6-9 describen la amenaza (el engaño es posible). La lección 10 describe el paradigma defensivo bajo la suposición de que la amenaza es real. La lección 11 describe el paradigma ofensivo complementario (hacer que U sea confiable a través de una supervisión escalable).

> Lecciones 6-9  describir amenazas ((la engaño es posible)  Lección 10  describir la hipótesis de que la amenaza existe de forma real.

> **【拓展：控制安全案例 → UK AISI 合作】**En el año 2025 AISI y Redwood UK han desarrollado un acuerdo de control de seguridad en el Reino Unido, donde el acuerdo de control de seguridad limita la probabilidad de resultados inaceptables.

## Usalo con el marco de ejecución
```figure
al-control-protocol
```

## Usalo

`code/main.py`Se puede analizar el presupuesto y el parámetro de colusión para reproducir la frontera de Pareto en Greenblatt et al. 2024 Figura 2 (forma, no números).

> `code/main.py`En el juego después de la tarea se simula cuatro tipos de acuerdo.

## Envíe el producto .

Esta lección produce`outputs/skill-control-protocol-audit.md`. Dado una descripción del protocolo de despliegue, identifica las funciones de U / T / H, nombra los vectores de colusión y estima la posición del protocolo en la frontera de utilidad-seguridad bajo presión del equipo rojo.

> 本课产 出  `outputs/skill-control-protocol-audit.md` Descripción del protocolo de implementación, identificación de los roles, nombre de la estrategia, posición del protocolo de evaluación en la vanguardia de la utilidad-seguridad.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Reproducir la frontera de utilidad y seguridad entre la edición confiable y la monitorización sin confianza.
   Traducción:运行`code/main.py`❖ Reproducción de información sobre la seguridad de la información

2. Añadir un nuevo protocolo: "T replanta con baja temperatura, luego U modifica la salida de T". Medir su posición en la frontera. ¿Por qué esto falla más catastróficamente que la edición con confianza?
   China: Añadir nuevo protocolo:"T con baja temperatura de pesquisa, entonces U 编辑 T 的输出――" ¿Por qué este editor fallido que el de la confianza es más catastrófico?

3. El documento 2024 asume que U puede ver el protocolo. Diseñar un protocolo que se oculte de U que las salidas están siendo auditadas. ¿Qué requiere este protocolo de la infraestructura de despliegue?
   En el artículo de la revista "Problemos de la Unión Europea" se dice que el proyecto de ley de la Unión Europea (UE) se ha aprobado en el año 2014.

4. Lea Greenblatt et al. 2024 Sección 7 (collusión). Propón una medida de resistencia a la colusión y explique su costo de utilidad esperado.
   China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:

5. Articula un caso de seguridad de control para una implementación que utilice U = GPT-4-clase, T = GPT-3.5-clase, H = 1% de las salidas auditadas. Identifique la hipótesis única más fuerte de la que depende el caso.
   Por ejemplo, el gobierno de la República de China ha aprobado una ley de seguridad para la seguridad de los bancos centrales.

## Términos clave .

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| AI Control | "safety under subversion" / "颠覆下的安全" | Protocol design that bounds unacceptable outcomes under a worst-case U / 在最坏情况 U 下限制不可接受结果的协议设计 |
| Untrusted model (U) | "the strong model" / "强模型" | The capable model we want to extract work from but do not trust / 我们想从中提取工作但不信任的能力模型 |
| Trusted model (T) | "the weak model" / "弱模型" | A weaker model, known not to be adversarial, used as editor/monitor / 已知不是对抗性的较弱模型 |
| Trusted human (H) | "the audit budget" / "审计预算" | Bounded expert labor; expensive; the ground-truth signal / 有界的专家劳动；昂贵；地面真实信号 |
| Trusted Editing | "T edits U" / "T 编辑 U" | Protocol where T is the gate on U's outputs; H called on ambiguous outputs / T 是 U 输出的门控的协议 |
| Untrusted Monitoring | "U monitors U" / "U 监控 U" | Protocol where a second U instance scores outputs; collusion-resistant only with extra investment / 第二个 U 实例评分输出的协议 |
| Control safety case | "the formal argument" / "正式论证" | Written argument that a protocol bounds the adversary's success under worst-case U / 协议在最坏情况 U 下限制对手成功的书面论证 |

## Más Leer más Leer más

- [Greenblatt, Shlegeris, Sachan, Roger — AI Control (arXiv:2312.06942)](https://arxiv.org/abs/2312.06942) el documento canónico ICML 2024
  El texto original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión
- [Redwood Research — Recent AI Control papers index](https://redwoodresearch.substack.com/) Seguimientos de 2024 a 2025
  中文翻译:Redwood Research2024-2025 后续
- [UK AISI + METR — Control safety cases](https://metr.org/blog/2025-03-26-common-elements-of-frontier-ai-safety-policies/) La puesta en marcha de los laboratorios fronterizos
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- [Hubinger et al. — Sleeper Agents (Lesson 7, arXiv:2401.05566)](https://arxiv.org/abs/2401.05566) el modelo de control de amenazas asume
  China: Hubinger 等人 control假设的威胁模型
