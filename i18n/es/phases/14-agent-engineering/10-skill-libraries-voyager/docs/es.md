# Bibliotécas de habilidades y aprendizaje permanente (Voyager)

> Voyager (Wang et al., TMLR 2024) trata el código ejecutable como una habilidad. Las habilidades se nombran, se pueden recuperar, se componen y se refinan por retroalimentación ambiental. Esta es la arquitectura de referencia para las habilidades de Claude Agent SDK, el kit de habilidades y el patrón de biblioteca de habilidades 2026.

> **【中文解读】**Voyager va a poder ejecutar código como habilidades. Habilidades son denominadas, recopilables, compostables, y se pueden combinar a través del entorno contra la refinamiento. Esta es la estructura de referencia de Claude Agent SDK habilidades, habilidades y habilidades y el modelo de la base de habilidades de 2026 .

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta Blocks) | **前置知识:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta 块)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Nombre de los tres componentes de Voyager  currículo automático, biblioteca de habilidades, incitación iterativa  y el papel de cada uno.
  China                                                                                                                                                                                                                                                               
- Explica por qué Voyager hace el código del espacio de acción, no comandos primitivos.
  Traducción: Explica por qué Voyager se movilizará espacio para codificar y no para ordenar.
- Implementar una biblioteca de habilidades stdlib con registro, recuperación, composición y refinamiento impulsado por fallos.
  La lengua china es la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china, la lengua china y la lengua china.
- Mapa el patrón de Voyager en las habilidades de 2026 de Claude Agent SDK y el ecosistema de skillkit.
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión original de la versión de la versión de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 2026 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 2026 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 2026 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de

## El problema es la introducción del problema

Los agentes que reconstruyen todas las capacidades desde cero en cada sesión hacen tres cosas mal:

> Cada reunión de la capacidad de reconstrucción de la propiedad de un agente hará tres cosas equivocadas:

1. **Waste tokens.**Cada tarea re-evoca el mismo razonamiento.
   En inglés:**浪费 token。**Cada tarea reinicia la misma idea.
2. **Lose progress.**Una corrección aprendida en la sesión A no se transfiere a la sesión B.
   En inglés:**丢失进展。**En el curso A, las correcciones no se transfieren al curso B.
3. **Fail on long-horizon composition.**Las tareas complejas requieren jerarquías de capacidad; las instrucciones de un solo tiro no pueden expresarlas.
   En inglés:**在长程组合上失败。**Las tareas complejas requieren niveles de capacidad; las simples propuestas no pueden expresarse.

> **【中文解读】**技能库(Skill Libraries) provino de Voyager (Wang et al., 2023)  un agente de exploración y aprendizaje autónoma en Minecraft.  La innovación central de Voyager es el descubrimiento y almacenamiento automático de habilidades: el agente en la ejecución de tareas encuentra una secuencia de operación efectiva, codificando su función de habilidades de uso repetible en la base de habilidades.

La respuesta de Voyager: tratar cada capacidad reutilizable como un trozo de código almacenado en una biblioteca, recuperable por similitud, composible con otras habilidades, y refinado por retroalimentación de ejecución.

> Respuesta de Voyager: Considerará cada capacidad de repetición como un bloque de código denominado almacenado en la arsenal, puede ser buscado a través de la similitud, puede combinarse con otros conjuntos de habilidades, y puede ser ejecutado a través de la re-refinanciación.

> **【拓展：Voyager 的技能库概念已被 2026 年的编码 Agent 普遍采用】**CLAUDE.md, Cursor, Cursor y el sistema de habilidades del Codex son variantes de esta idea. El modelo de operación válido se codificará como habilidades reproducibles.

> ¿ Qué es esto ?**【前置】**需要先掌握:Fase 14·05(Self-Refine/CRITIC) Voyager's "代提示机制"本质是 Self-Refine + 环境反;Fase 14·07(MemGPT) 技能库的检索机制类似于档案记忆的语义搜索──还需要理解"代码即行动"的概念,区别于"文本即行动"──

## El concepto central.

### Tres componentes

Voyager (arXiv:2305.16291) estructura un agente alrededor de:

> Voyager ((arXiv:2305.16291) alrededor de los siguientes tres componentes

1. **Automatic curriculum.**Un proponente impulsado por la curiosidad elige la siguiente tarea en función del conjunto de habilidades y el estado del entorno del agente.
   En inglés:**自动课程。**Bueno, el experto de la investigación de la ciencia y el desarrollo de la ciencia y el desarrollo de la ciencia y el desarrollo de la ciencia y el desarrollo de la ciencia y la tecnología.
2. **Skill library.**Cada habilidad es un código ejecutable. Nuevas habilidades se añaden cuando una tarea tiene éxito.
   En inglés:**技能库。**Cada habilidad es ejecutiva de código. Cuando se logra una tarea, se añade nuevas habilidades.
3. **Iterative prompting mechanism.**En caso de fallo, el agente recibe errores de ejecución, retroalimentación ambiental y salida de auto-verificación, luego refina la habilidad.
   En inglés:**迭代提示机制。**失败时,Agent 接收执行错误、环境反和自我验证输出,然后精炼技能──

La evaluación de Minecraft (Wang et al., 2024): 3.3 veces más elementos únicos, 8.5 veces más rápidas herramientas de piedra, 6.4 veces más rápidas herramientas de hierro, 2.3 veces más largo cruce de mapas frente a líneas de base.

> Minecraft  evaluación(Wang 等人,2024):3.3 veces más objetos únicos  8,5 veces más rápidos herramientas de piedra  6,4 veces más rápidas herramientas de hierro  2,3 veces más largo mapa de la tierra en comparación con las líneas de base  Número es Minecraft  específico, pero el modelo se puede mover 

### Espacio de acción = código

La mayoría de los agentes emiten comandos primitivos.

> Mayoría de agentes 发发出原始命令──Voyager 发出 JavaScript 函数──一个技能是:

```
async function craftIronPickaxe(bot) {
  await mineIron(bot, 3);
  await mineStick(bot, 2);
  await placeCraftingTable(bot);
  await craft(bot, 'iron_pickaxe');
}
```

Compuesto de subcompetencias, almacenado con teclas en la descripción y la incorporación, recuperado como un programa, no como una solicitud.

> Por el conjunto de habilidades de los niños.

Esta es la habilidad de 2026 Claude Agent SDK: un nombre, un trozo de código extraíble más instrucciones que el agente carga a pedido.

> Esto es 2026 Claude Agente SDK habilidad: un nombre de bloque de código recopilable más Agente de carga por necesidad instrucciones.

> ¿ Qué es esto ?**【类比】**技能库像程序员的"代码片段库" o fragmentos de IDE: no necesitas escribir Python cada vez que lo rediseñas`read_file`函数,调用已有的就行;;Voyager's insight is to let Agent also do It"invented" a once"挖铁矿"s code, stored into the library, next time again to dig铁矿就直接检索调用;;**关键**: habilidad es**代码**En cambio,**提示词**代码可以被环境执行、获得明确反,提示词不行──

### Recuperación de habilidades

La nueva tarea es hacer una piceta de diamante.

> Nueva misión: hacer la piedra.

1. Incluye la descripción de tarea.
   En inglés, "Misión de trabajo" se refiere a una tarea.
2. Hacer consultas en la biblioteca de habilidades para obtener habilidades similares.
   En inglés, "Consultar habilidades" se puede decir de forma diferente.
3. Recuperaciones `craftIronPickaxe`¿ Qué ?`mineDiamond`¿ Qué ?`placeCraftingTable`y otros.
   En inglés:`craftIronPickaxe`¿Qué es esto?`mineDiamond`¿Qué es esto?`placeCraftingTable`Y así.
4. Componen la nueva habilidad de primitivos recuperados + nueva lógica.
   Traducción: de la lengua original hasta el original + nueva lógica 组合新技能──

Este es el patrón de recursos de MCP (fase 13) y de habilidades de SDK de agentes implementados: recuperación sobre una superficie de conocimiento/código, enfocada a la tarea actual.

> Esta es la fase 13) y las habilidades de SDK de los agentes 实现的模式:在知识/代码表面上检索, limitada a las tareas actuales。

### Refinamiento iterable

El bucle de retroalimentación del Voyager:

> El ciclo de la Voyager:

1. El agente escribe una habilidad.
   En inglés: "Agent"
2. La habilidad se opone al medio ambiente.
   Traducción:Habilidad en el ambiente.
3. Una de las tres señales regresa:`success`¿ Qué ?`error`(con rastro de pila), `self-verification failure`¿ Qué ?
   Traducción:三种信号之一返回:`success`¿Qué es esto?`error`(带堆跟踪)`self-verification failure`¿Qué es eso?
4. El agente reescribe la habilidad usando la señal como contexto.
   En inglés, "Agent" significa "agent".
5. Loop hasta el éxito o rondas máximas.
   En inglés, "circuito hasta el éxito o alcanzar la mayor ronda de veces".

Esto es Auto-Refine (Ley 05) aplicado a la generación de código con verificación basada en el entorno. CRITIC (Ley 05) es el mismo patrón con herramientas externas que el verificador.

> ️ **【易错点】**La falta de habilidad se puede cubrir directamente en la base de habilidades.**后果**La versión anterior del trabajo original se perdió, la siguiente búsqueda es la nueva versión de un error.**一行修复**: skills库用版本化 key (casa de desarrollo)`craft_pickaxe_v3`),失败时新增版本,不覆盖旧版本; sólo auto-verificación 通过才标记为`latest`¿Qué es eso?

> Se trata de Auto-Refinación (n.o 5) aplicada a la creación de códigos de la prueba de ambiente (n.o 5) CRITIC (n.o 5) es el mismo modo de utilizar herramientas externas como prueba de la prueba (n.o 5)

### Currículo y exploración

El módulo de currículo de Voyager propone tareas como "construir un refugio cerca del lago" basándose en lo que el agente tiene y lo que aún no ha hecho. El proponente utiliza el estado ambiental + inventario de habilidades para elegir una tarea justo por encima de la capacidad actual  el punto dulce de exploración.

> ¿ Qué es esto ?**【困惑】**P: La "habilidad" de Voyager es JavaScript 代码"¿Por qué no Python? ¿Es Minecraft Mineflayer API 限制? A: 部分是──Mineflayer es Node.js 库, por lo que el código debe ser JavaScript── pero la razón más profunda es:**代码作为动作空间必须可执行** lenguaje no es importante, lo importante es "canjable por medio ambiente ejecutarse directamente y devolver el éxito/fallo señal"― en el navegador Agente 里可能是剧作家 TS 代码, en la base de datos Agente 里可能是 SQL―

> Modulo de curso de Voyager basado en el contenido existente y no completado del agente para presentar tareas, como "Construir un refugio en la costa del lago"  Proponente utilizar el estado ambiental + lista de habilidades para seleccionar un poco superior a la capacidad actual  Explorar los mejores puntos 

Para los agentes de producción esto se traduce en un operador de "lo que falta": dada la biblioteca de habilidades actual y un dominio, ¿qué habilidades aún no estamos cubriendo?

> Para el agente de producción, esto se traduce en un operador "deficiente": dado el actual conocimiento y el campo, ¿qué habilidades aún no hemos cubierto?

### Cuando este patrón va mal

- **Skill library rot.**La misma habilidad se añade 10 veces con descripciones ligeramente diferentes.
  En inglés:**技能库腐化。**La misma habilidad utiliza una descripción diferente añadir 10 veces.
- **Composed-skill drift.**Las habilidades de los padres dependen de un niño que haya sido refinado.
  En inglés:**组合技能漂移。**Las habilidades de los hijos que dependen de la habilidad paterna se refinan.
- **Retrieval quality.**La extracción de vectores sobre las descripciones de habilidades se degrada a medida que la biblioteca crece más allá de unos cientos.`category=tooling`").
  En inglés:**检索质量。**                                                                                                                                                                                                                                                              `category=tooling`"La habilidad" ("

## Construye con movimiento.
```figure
voyager-skills
```

## Construye el mismo

`code/main.py`Implementa una biblioteca de habilidades de STDlib:

> `code/main.py`Utilizando el estándar de la base de habilidades:

- `Skill` nombre, descripción, código (como cadena), versión, etiquetas, dependencias.
  En inglés:`Skill`名称、描述、代码(字符串) 版本、标签、依赖──
- `SkillLibrary` registrar, buscar (superposición de tokens), componer (tipo topológico de deps) y refinar (versión de golpe en actualización).
  En inglés:`SkillLibrary`注册、搜索(token 重叠)、组合(依赖的拓排序) 和精炼(更新时版本递增)
- Un agente con guión que registra tres habilidades primitivas, compone una cuarta, golpea un fracaso y refinará.
  En inglés, el nombre de la persona que ha sido seleccionada para la selección de equipos es el nombre de la persona que ha sido seleccionada para la selección de equipos.

- ¿Qué quieres decir ?

> 运行:

```
python3 code/main.py
```

El rastro muestra escritos de la biblioteca, recuperación, composición, una ejecución fallida y un refinamiento de v2  ciclo de Voyager de extremo a extremo.

> 轨迹显示库写入,检索,组合,一次失败执行和 v2 精炼 Voyager's end to end cycle──

## Usalo con el marco de ejecución

- **Claude Agent SDK skills**(Antropico)  la referencia 2026: cada habilidad tiene una descripción, código e instrucciones; cargado a pedido durante una sesión de agente.
  En inglés:**Claude Agent SDK skills**(Antropico) 2026 años referencia: cada habilidad tiene descripción、代码和指示; en Agence 会话中按需加载──
- **skillkit**(npm: skillkit)  Gestión de habilidades entre agentes para 32+ agentes de codificación de IA.
  En inglés:**skillkit**(npm: skillkit) 32+ AI 编码 Agente de trans-agente 技能管理。
- **Custom skill libraries** Específico de dominio (habilidades SQL para agentes de datos, habilidades Terraform para infra agentes).
  En inglés:**自定义技能库** área específica DATA Agent  SQL 技能、 infraestructura 技能)
- **OpenAI Agents SDK `tools`** en el extremo inferior; cada herramienta es una habilidad ligera.
  En inglés:**OpenAI Agents SDK `tools`**低端; cada herramienta es una habilidad de nivel ligero.

## Envíe el producto .

`outputs/skill-skill-library.md`genera una biblioteca de habilidades en forma de Voyager con registro, recuperación, versión y refinamiento conectados para cualquier tiempo de ejecución objetivo.

> `outputs/skill-skill-library.md`La base de habilidades de forma Voyager, incorporada en registro, búsqueda, versión y refinamiento, para cualquier objetivo de ejecución.

## Los ejercicios.

1. Añadir un detector de ciclo de dependencia a `compose()`¿Qué sucede cuando la habilidad A depende de B que depende de A?
   En español: en`compose()`En adición de dependencias de la prueba de ciclo. Habilidades A Depende B, B Depende A. ¿Qué ocurrirá?
2. Implementar la versión por habilidad. Cuando una habilidad de padre compone a un niño`crafting@1`, un refinamiento a `crafting@2`no debe actualizar silenciosamente al padre.
   Traducción:                                                                                                                                                                                                                                                              `crafting@1`时,`crafting@2`La perfección no puede ser silenciosa.
3. Reemplazar la recuperación de tokens superpuestos con embeddings de transformadores de oraciones (o una impl stdlib BM25).
   En inglés, el nombre de la palabra "título" se traduce en "título" o "título" en inglés.
4. Añadir un agente de "curriculum": dada la biblioteca actual y una descripción de dominio, proponga 5 habilidades faltantes.
   En el caso de los estudiantes de la escuela, el curso de enseñanza superior se realiza en el centro de la escuela.
5. Lea los documentos de habilidades de Claude Agent SDK de Anthropic.
   En inglés, el método de reproducción de juegos de azar es el método de reproducción de juegos de azar.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Skill | "Reusable capability" / "可复用能力" | Named chunk of code + description, retrievable by similarity / 命名的代码块 + 描述，可按相似性检索 |
| Skill library | "Agent memory of how-to" / "Agent 的操作记忆" | Persistent store of skills, searchable and composable / 技能的持久化存储，可搜索可组合 |
| Curriculum | "Task proposer" / "任务提议器" | Bottom-up goal generator driven by current capability gap / 由当前能力差距驱动的自底向上目标生成器 |
| Composition | "Skill DAG" / "技能 DAG" | Skills invoking skills; topologically sorted on execution / 技能调用技能；执行时拓扑排序 |
| Iterative refinement | "Self-correcting loop" / "自我纠错循环" | Env feedback + errors + self-verification fold back into the next version / 环境反馈+错误+自我验证反馈到下一版本 |
| Action-space-as-code | "Programmatic actions" / "编程式动作" | Emit functions, not primitive commands, for temporally extended behavior / 发出函数而非原始命令，用于时间扩展行为 |
| Dedup on write | "Skill collapse" / "技能合并" | Near-duplicate descriptions collapse to one canonical skill / 近似重复描述合并为一个规范技能 |

## Más Leer más Leer más

- [Wang et al., Voyager (arXiv:2305.16291)](https://arxiv.org/abs/2305.16291) el papel original de la biblioteca de habilidades
  Voyageur:Voyager, el primer libro de habilidades.
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) las capacidades de producción para 2026
  En inglés, "Cláude Agent SDK" 概览2026 年产品化技能──
- [Anthropic, Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) habilidades y sub-gentes en la práctica
  En la actualidad, el programa de trabajo de la compañía de la compañía de la tecnología de la información (CLAUD) está disponible en todo el mundo.
- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) el bucle de refinamiento debajo de Voyager
  El viaje es un ciclo de refinamiento de la base.
