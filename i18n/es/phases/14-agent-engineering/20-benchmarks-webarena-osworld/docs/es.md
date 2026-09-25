# Las marcas de referencia: WebArena y OSWorld

> WebArena prueba la capacidad de agente web en cuatro aplicaciones auto-hostadas. OSWorld prueba la capacidad de agente de escritorio en Ubuntu, Windows, macOS. En el lanzamiento (20232024) ambos mostraron una gran brecha entre los mejores agentes de su clase y los humanos. La brecha se está reduciendo; los modos de falla no han cambiado.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 19 (SWE-bench, GAIA) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objetivos de aprendizaje

- Describa las cuatro aplicaciones auto-hospedadas de WebArena y por qué es importante la evaluación basada en la ejecución.
- Explica por qué OSWorld utiliza capturas de pantalla reales del sistema operativo en lugar de API de accesibilidad.
- Nombre de los dos modos principales de falla de OSWorld: conexión a tierra de la interfaz gráfica y conocimiento operativo.
- Resumen lo que OSWorld-G y OSWorld-Human añaden a la referencia básica.

## El problema es la introducción del problema

Los agentes generalistas pueden llamar a herramientas. ¿Pueden manejar un navegador a través de 20 clics para completar un checkout de compras? ¿Pueden configurar una caja Linux usando solo teclado y ratón? Estas son las preguntas que WebArena y OSWorld responden.

> ¿Pueden utilizar las herramientas de un agente de negocios? ¿Pero pueden mover un navegador para completar 20 clics para completar la compra? ¿Pueden configurar solo un equipo de Linux con un teclado y un ratón?


> **【中文解读】**WebArena y OSWorld  evaluación de los agentes en el ambiente de cálculo real  WebArena 测试 Web 浏览器操作(购物、论坛、CMS)  OSWorld 测试桌面操作系统操作(文件管理、应用操作)  ambas son evaluar de extremo a extremo 不看中间步骤, sólo ver si el resultado final es correcto 

> **{【拓展：WebArena (CMU, 2023) 创建了真实的 Web 环境（电商、论坛、GitLab），A...】}**WebArena (CMU, 2023) 创建了真实的 Web 环境(电商、论坛、GitLab),Agent 需要像人类一样浏览和操作。2026年 SOTA 约 35% éxito,人类约 80%。OSWorld (HKU, 2024) 提供真实的 Ubuntu/Windows/macOS 桌面环境,Agent 需要操作 GUI 完成任务。

> ¿ Qué es esto ?**【前置】**建议先过:Phase 14·19 (SWE-bench/GAIA) 本节是其姐妹篇,专门评估"GUI 操作"能力;以及Phase 14·21 (Computer Use Agents) 本节是评估那些 Agent 的"考试题"──了解GUI 操作和工具调用区别──GUI 是像素+点击,工具调用是API+JSON) 本节是关键──

## El concepto central.

### WebArena (Zhou et al., ICLR 2024)

- 812 tareas de largo horizonte en cuatro aplicaciones web auto-hospedadas: un sitio de compras, un foro, una herramienta de desarrollo similar a GitLab, un CMS empresarial.
- Además de utilidades: mapa, calculadora, raspad.
- La evaluación se basa en la ejecución a través de API de gimnasio ¿se realizó el pedido, se cerró el problema, se actualizó la página del CMS?
- Al lanzarse: el mejor agente GPT-4 alcanzó el 14,41% de éxito frente al humano 78,24%.

La configuración de los marcos de auto-hosting es importante  el índice de referencia no es escatimista porque las aplicaciones objetivo están fijadas y reproducibles.

> El marco de la autogestión es importante porque la base de la aplicación de los objetivos no es fija y puede ser reproducida de forma inestable.

> ¿ Qué es esto ?**【类比】**WebArena y OSWorld: WebArena es una versión de un sistema operativo de Ubuntu/Windows/macOS, cada versión de la misma puede ser diferente, también puede ser reproducido en ventanas, carteles, anuncios.**关键**: WebArena 测 es "Agencia 能不能使用Web", OSWorld 测 es "Agencia 能不能使用电脑"后者难一个量级──

> WebArena y OSWorld es un entorno de evaluación de un agente con uso de computadora.

### Extensiones

- **VisualWebArena** tareas basadas en la visión en las que el éxito depende de la interpretación de las imágenes (retratos de pantalla como observaciones de primera clase).
- **TheAgentCompany**(Dec 2024)  añade terminal + codificación; más como un ambiente de trabajo remoto real.

### OSWorld (Xie et al., NeurIPS 2024)

- 369 tareas reales en computadoras en Ubuntu, Windows, macOS.
- Control de teclado y ratón de forma libre de aplicaciones reales.
- 1920×1080 capturas de pantalla como la observación.
- En el momento de su liberación: mejor modelo 12,24% vs humano 72,36%.

### Modo de falla primaria

1. **GUI grounding.**Los modelos luchan por localizar los elementos de la interfaz de usuario de manera confiable en 1920×1080.
2. **Operational knowledge.**¿Qué menú tiene la configuración, qué acceso directo del teclado, qué panel de preferencias.

> ️ **【易错点】**Utilice DOM o API de accesibilidad para correr OSWorld y luego reportar "高分"**后果**Por ejemplo, el número de ejemplares de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie.**视觉 grounding**(Mapping de los elementos a los átomos), con DOM API, se puede superar el reto central.**一行修复**: en OSWorld 上 sólo puede utilizar el agente de captura de pantalla como entrada, si no se cuenta "en OSWorld 上评估"― Si desea evaluar el agente basado en DOM, por favor use WebArena o Mind2Web―

### Seguimiento

- **OSWorld-G** 564 muestras de la suite de tierra + Jedi entrenamiento.
- **OSWorld-Human** trayectorias de acción de oro seleccionadas manualmente.

### ¿Por qué esto importa?

Claude uso de computadoras, OpenAI CUA, Gemini 2.5 Uso de computadoras (lección 21) todos entrenan en cargas de trabajo moldeadas por WebArena y OSWorld.

> Claude 计算机使用、OpenAI CUA、Gemini 2.5 计算机使用(第 21 课) todos en WebArena y OSWorld 塑造 塑造的工作负载上训练──基准是目标;生产模型是交付的答案──

> WebArena y OSWorld es un entorno de evaluación de un agente con uso de computadora.

### Cuando el benchmarking sale mal

- **Screenshot-only evals.**OSWorld se dirige a capturas de pantalla; evaluar un agente que utiliza DOM o API de accesibilidad en OSWorld se pierde el reto de aterrizaje.
- **Ignoring trajectory length.**El puntaje de sólo la tasa de éxito pierde la ineficiencia de 1,4-2,7 veces de los pasos OSWorld-human superficies.
- **Stale self-hosted apps.**Las aplicaciones de WebArena pin versiones específicas; actualización sin re-curar rompe la comparabilidad.

> ¿ Qué es esto ?**【困惑】**P: WebArena 上 SOTA 才 35%,OSWorld 才 12%, esto no es una explicación de que el agente de uso de computadoras ahora no puede ser usado?**针对性优化**de: fijación de varias páginas web 清晰的任务流, en el proceso 底.**结论**El método de evaluación es "capacidad superior", "producción" y "optimización especial", ambos no pueden ser intercambiados directamente.

> **仅截图评估。**OSWorld es un proyecto de investigación; en OSWorld se evalúa el uso de DOM o API sin obstáculos de Agente de la Organización para el Desarrollo de la Tierra.
> **忽略轨迹长度。**                                                                                                                                                                                                                                                              
> **过时的自托管应用。**La aplicación de WebArena fijó una versión específica; no se reorganizó la actualización para destruir la comparabilidad.

## Construye y realiza.
```figure
ae-agent-human-gap
```

## Construye el mismo

`code/main.py`Implementa un arnés de agente web de juguete:

> `code/main.py`实现 un juego Web Agent 测试工具:

> WebArena y OSWorld es un entorno de evaluación de un agente con uso de computadora.

- Una máquina de estado de "aplicación de compras" mínima: list_items, add_to_cart, checkout.
- Trayectorias de oro para 3 tareas.
- Un agente con guión que intenta cada tarea.
- Evaluación basada en la ejecución (control de estado) y métrica de eficiencia de trayectoria (pasos frente al oro).

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Resultado: tasa de éxito por tarea y eficiencia de trayectoria, que reflejan la metodología de OSWorld-Human.

> 输出: por tasas de éxito y eficiencia de trayectoria, refleja el método de OSWorld-Human.

> WebArena y OSWorld es un entorno de evaluación de un agente con uso de computadora.

## Usalo con el marco de ejecución

- **WebArena Verified**auto-hosted en un grupo interno para evaluación continua.
- **OSWorld**en una flota de máquinas virtuales para agentes de escritorio.
- **Computer-use agents**(Lección 21) Claude, OpenAI CUA, Gemini, todos entrenados en cargas de trabajo como estas.
- **Your own product flows** captar trayectorias de oro para tus 20 principales tareas; ejecutar agentes contra ellos semanalmente.

## Envíe el producto .

`outputs/skill-web-desktop-harness.md`construye un arnés de agente web/de escritorio con una métrica de evaluación y eficiencia de trayectoria basada en ejecución.

> `outputs/skill-web-desktop-harness.md`Construir una herramienta de prueba de agente web/de mesa, con un indicador de evaluación y eficiencia de trayectoria basado en la ejecución.

> WebArena y OSWorld es un entorno de evaluación de un agente con uso de computadora.

## Los ejercicios.

1. Extenda el arnés de juguete con una segunda aplicación (un foro). Escriba 3 tareas más trayectorias de oro.
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Añadir informes de eficiencia de trayectoria por tarea. ¿En tu juguete, el agente es 1x, 2x, o 3x sobre el oro?
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. Implementar una herramienta "distractor" que la trayectoria de oro nunca usa. ¿Se siente tentado el agente scripted?
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. Lee OSWorld-G. ¿Cómo separarías los fallos de tierra de los fallos de planificación en tus propias evaluaciones?
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. ¿Qué se rompe cuando se actualiza una de las versiones de la aplicación fijada?
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| WebArena | "Web agent benchmark" | 812 tasks across 4 self-hosted apps; gym-style evaluation |  |
| VisualWebArena | "Visual WebArena" | Visually grounded WebArena; screenshots are observations |  |
| OSWorld | "Desktop agent benchmark" | 369 tasks on real Ubuntu/Windows/macOS |  |
| GUI grounding | "Pixel-to-element mapping" | Model localizing UI elements in 1920x1080 |  |
| Operational knowledge | "OS know-how" | Which menu, which shortcut, which preference pane |  |
| OSWorld-G | "Grounding suite" | 564 grounding-only samples + training set |  |
| OSWorld-Human | "Gold trajectories" | Manual expert action sequences to measure efficiency |  |
| Trajectory efficiency | "Steps over gold" | Agent step count divided by human minimum |  |

## Más Leer más Leer más

- [Zhou et al., WebArena (arXiv:2307.13854)](https://arxiv.org/abs/2307.13854) Referencia web de cuatro aplicaciones
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Xie et al., OSWorld (arXiv:2404.07972)](https://arxiv.org/abs/2404.07972) Referencia de escritorio de sistema operativo transversal
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Anthropic, Introducing computer use](https://www.anthropic.com/news/3-5-models-and-computer-use) La capacidad de Claude en forma de referencia
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [OpenAI, Computer-Using Agent](https://openai.com/index/computer-using-agent/) Números de OSWorld y WebArena
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
