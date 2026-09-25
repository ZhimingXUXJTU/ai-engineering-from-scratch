# Desarrollo de agentes Eval-Driven  desarrollo  evaluación

> La guía de Anthropic: "comience con instrucciones simples, optimicelas con una evaluación integral, y añada sistemas agenciales de múltiples pasos solo cuando sea necesario". La evaluación no es el último paso. Es el bucle externo que impulsa todas las demás opciones en la Fase 14.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** All of Phase 14. | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

> ¿ Qué es esto ?**【前置】**Se trata de una serie de métodos de evaluación de la fase 14 de la evaluación de la evaluación de la evaluación de la fase 14.

## Objetivos de aprendizaje

- Nombre de las tres capas de evaluación  referentes estáticos, personalizado fuera de línea, producción en línea  y para qué sirve cada uno.
- Explica el bucle cerrado de evaluador-optimizador.
- Describa las mejores prácticas para 2026: evaluaciones en directo junto al código, ejecutadas en CI, relaciones públicas de puertas.
- Conecta cada lección de la Fase 14 al caso de evaluación que genera.

## El problema es la introducción del problema

Los agentes pasan demos. Ellos fallan en la producción de maneras que las demos no pueden predecir. Los puntos de referencia responden "¿este modelo es amplio en capacidad?" no "este agente está enviando los parches adecuados para mi producto?" La respuesta: evaluación en tres capas, funcionando continuamente, con cada baranda de seguridad y regla aprendida mapeada a un caso de evaluación.

> ¿ Qué es esto ?**【类比】**El agente evalúa como a los deportistas hacerse un examen físico.**静态基准**(SWE-bench、BFCL) =国家体能测试,比平均水平;**定制离线 eval**= para el diseño de tu proyecto (por ejemplo, "la tasa de éxito de la modificación de este error") = entrenamiento en equipo;**在线生产 eval**= verdadero usuario =A/B 测试──三层缺一不可只看基准会过适应,只看生产反周期太长──

> ️ **【易错点】**El agente eval de 3 个坑:(1) **只测 happy path**eval 集全是简单查询, compleja situación no se cubre;务必构建对抗性 测试(模糊指令、攻击、边界值)**eval 不进 CI** desarrollo时手工跑一次就过,上线后没人跑;eval 必须进 GitHub Actions,PR 不过 eval 不能合并──(3) **eval 集污染**Muchos ejemplos de datos de la actualidad se mezclan rápidamente, por ejemplo,

> El agente ha pasado por la demostración. Ellos han fracasado de una manera impredecible en la producción. El principio de respuesta es "¿Tiene este modelo una capacidad amplia?" en lugar de "¿Este agente está entregando correctos suplementos para mi producto?" La respuesta es: tres niveles de evaluación, funcionamiento continuo, cada cuidado y las reglas de aprendizaje se proyectan en un caso de evaluación.


> **【中文解读】**评估驱动的代理 开发(Eval-Driven Development) se aplicará a la TDD en el diseño de software tradicional 应用于代理:先定义评估标准,再实现代理.

> **{【拓展：Eval-Driven Agent Development 是 2025-2026 年的最佳实践。核...】}**El desarrollo de agentes Eval-Driven es la mejor práctica de 2025-2026 años. Herramientas centrales: 1) AgentOpsAgent Tracking and Evaluation Platform; 2) LangSmithLangChain's assessment suite; 3) BraintrustAI Evaluation Framework。 Key Insight:Agent Evaluation should be based on complete trajectory (trajectory) rather than final output Dos agentes pueden obtener el mismo resultado, pero uno ha ido a través de 5 pasos, el otro a través de 50 pasos, la calidad y el costo son enormes diferencias.
## El concepto central.

### Tres capas de evaluación

1. **Static benchmarks** SWE-bench Verificado para código (lección 19), WebArena/OSWorld para navegación / escritorio (lección 20), GAIA para generalista (lección 19), BFCL V4 para uso de herramientas (lección 06). Uso para comparación entre modelos y puertas de regresión. Contaminación es real: SWE-bench+ encontró una fuga de solución del 32,67%. Siempre informe de puntajes verificados / + auditados.

2. **Custom offline evals** la forma de su producto:
   - LLM como juez (Langfuse, Phoenix, Opik  Lección 24).
   - Basado en la ejecución (execute el parche, verifique las pruebas).
   - Basado en la trayectoria (compara secuencias de acción con el oro; OSWorld-Human muestra agentes superiores 1.4-2.7x sobre el oro).

3. **Online evals** Producción:
   - Repeticiones de la sesión (Langfuse).
   - Alertas activadas por la vigilancia (lección 16, 21).
   - El seguimiento de costes / latencia por paso (lección 23 OTel abarca).

### Evaluación-optimización (antrópica)

El bucle apretado:

1. El proponente genera la salida.
2. Los jueces de evaluación.
3. Refinar hasta que el evaluador pase.

Este es el auto-refinado (lección 05) generalizado. Cualquier flujo de agentes que te importa puede envolver en evaluador-optimizador para la confiabilidad.

> Es la generalización de Auto-Refinación (§5) ◊ cualquier proceso de agente que te interese puede ser empaquetado con un evaluador-optimizador para mejorar la fiabilidad.

> 评估驱动的代理 开发(Eval-Driven Development) se evaluará como el núcleo del desarrollo de un agente  Pre-definir los criterios de evaluación, reconstruir un agente, utilizar la orientación de evaluación y mejorar──

### 2026 mejores prácticas

- Los Evals viven junto al código.
- Haga informativos en cada PR.
- La combinación de puertas en las puntuaciones de evaluación (por ejemplo, "sin regresión > 5% vs principal").
- Cada baranda de vigilancia hace un mapa de un caso de evaluación.
- Cada regla aprendida (Reflexión, pro-flujo de trabajo-regla de aprendizaje) mapas a un caso de fracaso.

### Enlazación de la fase 14

Cada lección en la Fase 14 genera casos de evaluación:

| Lesson | Eval case it generates |
|--------|------------------------|
| 01 Agent Loop | Budget-exhausted, infinite-loop guard |
| 02 ReWOO | Planner replans correctly when a tool fails |
| 03 Reflexion | Learned reflections apply on retry |
| 05 Self-Refine/CRITIC | Judge passes refined output |
| 06 Tool Use | Argument coercion works; unknown tools rejected |
| 07-10 Memory | Retrieval citations match sources; stale facts invalidate |
| 12 Workflow Patterns | Each pattern produces correct output |
| 13 LangGraph | Resume reproduces state exactly |
| 14 AutoGen Actors | DLQ catches crashed handlers |
| 16 OpenAI Agents SDK | Guardrail trips on the right inputs |
| 17 Claude Agent SDK | Subagent results return to orchestrator |
| 19-20 Benchmarks | SWE-bench Verified score, WebArena success rate, OSWorld efficiency |
| 21 Computer Use | Per-step safety catches injected DOM |
| 23 OTel | Spans emit required attributes |
| 26 Failure Modes | Detectors tag known failures |
| 27 Prompt Injection | PVE refuses poisoned retrievals |
| 28 Orchestration | Supervisor routes to the right specialist |
| 29 Runtime Shapes | DLQ handles N% failure |

Si su suite de evaluación tiene casos para cada uno, ha cubierto la Fase 14.

> Si tu equipo de evaluación tiene casos de uso de cada curso, ya cubres la Fase 14.

> 评估驱动的代理 开发(Eval-Driven Development) se evaluará como el núcleo del desarrollo de un agente  Pre-definir los criterios de evaluación, reconstruir un agente, utilizar la orientación de evaluación y mejorar──

### Cuando el desarrollo basado en la evaluación no funciona

- **No baseline.**Los Evals sin un último bien conocido son ilegibles.
- **LLM-judge without grounding.**Los jueces también alucinan. patrón crítico (lección 05)  juicios basados en herramientas externas.
- **Over-fitting to evals.**La optimización para la evaluación se desvía de la utilidad de producción.
- **Flaky evals.**Los casos no deterministas causan falsas alarmas.

> **没有基线。** no hay evaluación de un estado de buen estado conocido es legible                                                                                                                                                                                                                                                        
> **LLM 评审器没有基础。**评审器也会幻觉──CRITIC 模式(第 5 课) 评审器基于外部工具──
> **过拟合评估。**Para evaluar la optimización de la producción en uso práctico, se pueden utilizar ejemplos de cambio.
> **不稳定的评估。**El uso de casos no definidos provoca un error de información.

## Construye y realiza.
```figure
ae-eval-three-layers
```

## Construye el mismo

`code/main.py`es un arnés de evaluación stdlib:

- Registro de casos con categorías (marca de referencia, personalizado, en línea).
- Un agente con guión bajo prueba.
- El ciclo de evaluador-optimizador: proponer, juzgar, refinar hasta el paso o rondas máximas.
- Puerta de CI: tasa de aprobación agregada + regresión frente al nivel de referencia.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Resultado: por caso, la aprobación/fallo, la bandera de regresión, el veredicto de la puerta de CI.

> 输出: cada caso de uso pasa/ fracaso 归标志 CI 门控裁定

> 评估驱动的代理 开发(Eval-Driven Development) se evaluará como el núcleo del desarrollo de un agente  Pre-definir los criterios de evaluación, reconstruir un agente, utilizar la orientación de evaluación y mejorar──

## Usalo con el marco de ejecución

- Escriba casos de evaluación en el mismo repo que su código de agente.
- Controlarlos en todas las relaciones públicas a través de CI.
- No se construye en regresión.
- Rate de paso de seguimiento a lo largo del tiempo.
- Atájate cada fallo de producción a un nuevo caso.

## Envíe el producto .

`outputs/skill-eval-suite.md`construye una suite de evaluación de tres capas para un producto agente con puertas de CI y seguimiento de regresión.

> `outputs/skill-eval-suite.md`Para la construcción de productos de agentes, tres niveles de evaluación, incluidos los controles de CI y el seguimiento de regreso.

> 评估驱动的代理 开发(Eval-Driven Development) se evaluará como el núcleo del desarrollo de un agente  Pre-definir los criterios de evaluación, reconstruir un agente, utilizar la orientación de evaluación y mejorar──

## Los ejercicios.

1. Toma uno de tus fallos de producción, escribe un caso de evaluación que lo reproduzca. ¿Tu agente lo pasa ahora?
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Construye una rúbrica de jueces de LLM para su dominio con tres dimensiones (factual, tono, alcance).
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. Enviar la suite de eval en CI. Fallar en la construcción de >=5% regresión.
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. Añadir una métrica de eficiencia de trayectoria: ¿cuántos pasos tomó el agente frente a una trayectoria de oro?
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. Mapa cada lección de la Fase 14 a un caso de evaluación en su suite. ¿Hay algo que falta?
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Static benchmark | "Off-the-shelf eval" | SWE-bench, GAIA, AgentBench, WebArena, OSWorld |  |
| Custom offline eval | "Domain eval" | LLM-as-judge / exec / trajectory on your product shape |  |
| Online eval | "Production eval" | Session replay, guardrail alerts, cost/latency tracking |  |
| Evaluator-optimizer | "Propose-judge-refine" | Iterate until judge passes |  |
| CI gate | "Merge blocker" | Fail the build on eval regression |  |
| Baseline | "Last-known-good" | Reference score to detect regression |  |
| Trajectory efficiency | "Steps over gold" | Agent step count divided by human expert minimum |  |

## Más Leer más Leer más

- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) "comenzar simple, optimizar con evals"
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [OpenAI, SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) el índice de referencia seleccionado
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) Indicador de referencia de uso de herramientas
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Langfuse docs](https://langfuse.com/) evaluaciones + repetición de sesiones en la práctica
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
