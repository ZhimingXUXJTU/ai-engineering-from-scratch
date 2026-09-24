# Sociedad de la Mente y el debate multi-agente .

> La premisa de Minsky de 1986  inteligencia es una sociedad de especialistas  se redescubre cada década. En 2023 Du et al. la convirtieron en un algoritmo concreto: múltiples instancias de LLM proponen respuestas, leen las respuestas de cada uno, critican y actualizan. Durante N rondas convergen en un consenso que supera la CoT de tiro cero y la reflexión sobre seis tareas de razonamiento y factualidad. Dos hallazgos importan: ambos **multiple agents**y **multiple rounds**La sociedad supera el monólogo de un solo agente; el intercambio de múltiples rondas supera el voto de una sola vez.

> **【中文解读】**Este capítulo presenta el debate social sobre el espíritu de Marvin Minsky sobre la aplicación de la teoría social en el sistema de múltiples agentes.

> **【拓展：society of mind debate→具体应用】**Marvin Minsky 心智社会 (心智社会, 1986) propone que el inteligencia es el producto de la colaboración de muchos simplistas. Esta idea se aplica a los múltiples agentes en el sistema de debate de 2026 para lograr que los múltiples agentes logren un mejor resultado a través del debate.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (Primitive Model)
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 16·04(原语模型)、Fase 13·01-03(CoT 推理)。Minsky 心智社会理论 + LLM 辩论算法。
> ¿ Qué es esto ?**【类比】**Más agente 辩论 = "学术同行评审"──单 agent = 一个作者写论文(易自但片面);多 agent 辩论 = 多位审稿人 + 作者多轮回应,最终共识更稳健──Du et al. 2023 证明:多 agent + 多轮独立贡献提升不是简单加法,是协同效应──3-5 个代理 最优(多多多了反而成一团)──

## # El problema # # El problema #

La autoconstancia  muestra un modelo muchas veces y toma la respuesta mayoritaria  es la mejoría de razonamiento más barata que puedes seguir. Funciona, pero se satura rápidamente. Puedes duplicar tus muestras y no ver otro salto significativo.

> La autoconformidad  a un modelo varias veces muestran y obtienen la mayoría de las respuestas  es la mejoría de la hipótesis más económica que puedes añadir .

La saturación proviene de errores correlacionados: el mismo modelo tiende a fallar de la misma manera.

>  y de errores relacionados: el mismo modelo tiende a fracasar de la misma manera.

El debate rompe la saturación. En lugar de N muestras independientes de un modelo, N agentes leen el razonamiento y revisión de los demás. La correlación entre muestras disminuye (ya no son i.i.d.), y el punto de convergencia es a menudo correcto donde la votación i.i.d. estaba confidentemente equivocada.

> El debate rompe 和── no se obtiene N 个独立样本从一个模型, sino que se deja N 个代理阅读彼此的推理和修改── los ejemplos ya no son independientes y distribuidos, los puntos de recepción suelen ser correctos, mientras que los votos independientes y distribuidos se cometen errores con confianza.

La relación decorrectiva es el mecanismo.Cuando los agentes ven el razonamiento de otros agentes, no pueden evitar interactuar con él  ya sea para defender su posición o actualizarla.

> Cuando el agente ve las recomendaciones de otros agentes, ellos tienen que participar o defender su posición, o actualizarla. Esta participación forzada no puede generar información independiente y distribuida de cualquier manera.

## Concepto de la esencia de la concepción

### El algoritmo de Du et al. 2023

En el caso de las medidas de seguridad, el fabricante deberá tener en cuenta el valor de la información obtenida.

> De arXiv:2305.14325 (ICML 2024):

El algoritmo es intencionalmente simple: no hay papeles especiales, no hay juez, no hay moderador. Cada agente es simétrico. La única asimetría es el orden de quién habla primero, e incluso eso se desvanece en múltiples rondas.

> 算法有意简单: no hay un papel especial, no hay un juez, no hay un presentador. Cada agente es un homónimo.

1. Cada uno de los agentes N produce una respuesta inicial a la pregunta.
   En inglés, "Agent" es el nombre de un agente.
2. Para la ronda r = 2..R: a cada agente se le muestran las respuestas de la ronda r-1 de los otros agentes y se le pide "considerando estas, dé su respuesta actualizada".
   Para la segunda ronda: cada agente ve otras respuestas del segundo turno y se le pregunta: "Considera esto, da tu respuesta actualizada"".
3. Después de las rondas R, la mayoría vota las respuestas finales.
   Después de la ronda, se votó la mayoría sobre la respuesta final.

Las pruebas en papel sobre MMLU, GSM8K, biografías, MATH y puntos de referencia de la realidad.

> 论文在 MMLU、GSM8K、传记、MATH 和事实性基准上测试──辩论持续优于CoT 和自我反思──

La suite de benchmarks abarca tanto el razonamiento (MATH, GSM8K  problemas con respuestas correctas verificables) como la realidad (biografías  afirmaciones verificables frente a Wikipedia).

> 基准套件涵盖推理(MATH、GSM8K有可验证正确答案问题) y事实性(传记可对照维基百科 检查的声明) ⋅ Factualidad increment is the title result:

### Dos botones independientes

Ablaciones del mismo documento:

> Como se dice en el artículo:

- **Agent count alone**En la mayoría de las tareas, el único agente es el mejor, pero en la mayoría de las tasas, el plateau.
  En inglés:**仅 Agent 数量**(1 ronde, mayoría de votos) En la mayoría de las tareas es mejor que un solo agente, pero alcanzará la plataforma.
- **Round count alone**(1 agente que ve su propio razonamiento previo) apenas ayuda a la debilidad conocida de la reflexión.
  En inglés:**仅轮数**(1 Agente ver sus propias conclusiones) casi no ayudó.
- **Both together**El intercambio de múltiples rondas entre múltiples agentes impulsa la ganancia.
  En inglés:**两者结合** producido un aumento considerable                                                                                                                                                                                                                                                           

### Por qué funciona

Dos mecanismos:

>  Dos mecanismos:

Los dos mecanismos se componen: la exposición a los desacuerdos proporciona nueva información; los errores descorrelados impiden que la nueva información sea media en la respuesta incorrecta.

> 两个 mecanismos complejos: exponerse a las diferencias para proporcionar nueva información; ir a correlaciones de errores para evitar que la nueva información sea media a la respuesta errónea.

1. **Exposure to disagreement.**Cuando un agente ve la cadena de razonamiento de otro agente con una conclusión diferente, tiene que justificar o actualizar.
   En inglés:**暴露于分歧。**Cuando un agente ve a otro agente con una cadena de discusión diferente, debe demostrar o actualizarse. De cualquier manera, la primera ronda de r+1 tiene un contenido más rico que la segunda ronda.
2. **Correlated error reduction.**En autoconsistencia, todas las muestras provienen del mismo modelo, por lo que los errores se correlacionan  promedio en una respuesta confidentemente incorrecta. Diferentes modelos o semillas diferentes se descorrela. Diferentes * puntos de vista debatidos * se descorrela más adelante.
   En inglés:**相关错误减少。**En la autoconformidad, todas las muestras provienen del mismo modelo, por lo que errores relacionados  obtienes una respuesta errónea segura  Diferente modelo o diferentes semillas se relacionan  Diferente* punto de vista de debate  Más en relación 

### El debate es heterogéneo

El debate sobre Llama + Claude + GPT reduce el colapso de la monocultura (lección 26) porque los errores correlacionados de una familia de modelos no son compartidos por los demás.

> A-HMAD 和相关后续工作为不同 Agent 使用*不同的基础模型*──Llama + Claude + GPT 辩论减少单一文化崩(Leyón 26), porque un modelo de la familia de errores relacionados no se comparten con otros modelos de la familia.

El argumento de la correlación de errores es el mismo detrás de los métodos de conjunto en el ML clásico: los modelos diversos fallan de manera diferente, por lo que la votación es más confiable.

> 错误去相关论点与经典ML中集成方法背后的相同: los modelos de diversificación fracasan de manera diferente, por lo que votar es más fiable.

Desventaja: un modelo débil que participa en un debate puede arrastrar el consenso hacia su respuesta equivocada (ver "¿Deberíamos estar volviéndonos locos?", arXiv:2311.17371).

> 缺点: un modelo débil de debate participativo puede llegar a un consenso arrastrándolo hacia su respuesta errónea.

El debate heterogéneo no es la diversidad libre. Un modelo débil (digamos, un parámetro Llama 7B) puede superar a un modelo fuerte (GPT-4) si el modelo fuerte se actualiza demasiado agresivamente hacia las respuestas equivocadas del modelo débil. Calibra qué modelos participan.

> 异构辩论不是免费多样性──弱模型(如7B 参数 Llama) puede rechazar el fuerte模型(GPT-4), si el fuerte modelo es demasiado agresivo hacia el débil modelo de confianza error答案更新──校准哪些模型参与──

### NLSOM  la extensión de 129-agente

Zhuge et al. ("Mindstorms in Natural Language-Based Societies of Mind", arXiv:2305.17066) escalaron esta idea a 129 sociedades miembros. El resultado: la especialización y la autoorganización surgen con la escala, y el sistema supera al agente único en tareas como la respuesta a preguntas visuales.

> Zhuge 等人("Based on natural language的心智社会中的思维风暴",arXiv:2305.17066) extenderá esta idea a 129 miembros de la sociedad── resultado: especialización y autoorganización a medida que surgen las tasas, sistemas en la visión y las respuestas, y así sucesivamente.

El resultado de la escala es sorprendente: después de ~ 50 agentes, los roles individuales comienzan a especializarse sin que se les diga. Algunos se convierten en "investigadores", "otros" en críticos, "otros" en "sintetizadores". Esta es una diferenciación de roles emergente  el mismo fenómeno observado en las organizaciones humanas, que ahora ocurre en las sociedades de LLM.

>  El resultado es notable: después de más de 50 agentes, los roles individuales comienzan a especializarse en condiciones sin ser acusados. Algunos se convierten en "investigadores", otros en "criticos" o "complejos".

### Modo de falla

- **Sycophancy cascade.**Todos los agentes se aplazan a quien suene más seguro. El debate se derrumba con la voz más alta.
  En inglés:**谄媚级联。**Todos los agentes se someten a la voz más segura de sí mismos.
- **Topic drift.**Los debates en muchas rondas se derivan de la pregunta original.
  En inglés:**主题漂移。**Muchos debates se han ido haciendo en el debate original.
- **Compute blowup.**N agentes x R rondas = N*R LLM llamadas, cada una con un contexto que crece. Un debate de 5 agentes, 5 rondas es de 25 llamadas en contexto creciente. El costo por pregunta puede exceder 10 veces una sola llamada CoT.
  En inglés:**计算爆炸。**N 个代理 x R 轮 = N*R 次 LLM 调用, cada vez de arriba abajo都在增长──5 个代理、5 轮辩论是25 次调用,上下文不断增长──每问题成本可能超过单次CoT 调用的10倍──

## Construye y realiza.
```figure
multi-agent-debate
```

## Construye el mismo

`code/main.py`La respuesta de los agentes es una respuesta de 3 agentes x 3 rondas en una pregunta matemática en la que cada agente comienza con una respuesta diferente (posiblemente incorrecta).

> `code/main.py`En un problema matemático se ejecuta 3 Agente x 3 Radas de debate, cada Agente comienza con una respuesta diferente (puede ser un error).

La demostración muestra dos efectos clave:

> La demostración muestra dos efectos clave:

- Una sola ronda de intercambio acerca a los agentes a la respuesta correcta.
  China: 单轮交流将 Agent 移向正确答案.
- Las rondas adicionales anteriores a la segunda ronda muestran rendimientos disminuyentes (combina con la meseta de Du et al.).
  China 翻译: Más de la segunda ronda de la cantidad de rotas extra muestra ingresos en aumento 匹配 Du等人的平台) 

- ¿Qué quieres decir ?

```
python3 code/main.py
```

## Usalo con el marco de ejecución

`outputs/skill-debate-configurator.md`Configura un debate para una nueva tarea: número de agentes, número de rondas, heterogeneidad (modelo mismo vs mixto), asignación de roles (simétrica vs una adversarial).

> `outputs/skill-debate-configurator.md`Por el contrario, el nombre de la persona que se encuentra en el grupo de trabajo es el nombre de la persona que se encuentra en el grupo de trabajo.

## Envíe el producto .

Si usted navega el debate:

> Si lo haces:

- **Cap rounds at 3.**Du et al. muestran que 3 rondas capturan la mayor parte de la ganancia.
  En inglés:**将轮数限制在 3。**Du 等人 indican que las tres rutas capturaron la mayor parte de los beneficios.
- **Cap agents at 5.**Más allá de 5, el contexto y el costo dominan.
  En inglés:**将 Agent 限制在 5。** Más de 5 , sobre la inflación y el coste de la producción.
- **Heterogeneous by default.**Al menos dos modelos de base diferentes en la piscina.
  En inglés:**默认异构。**Hay al menos dos modelos básicos diferentes en la piscina.
- **Adversarial slot.**Un agente le hizo discrepar sin importar.
  En inglés:**对抗角色。**Un agente es advertido de cualquier manera.
- **Log every round.**Los sistemas de debate que ocultan rondas intermedias no pueden ser desactivados ni auditados.
  En inglés:**记录每轮。**El sistema de debate oculto en el medio de las rondas no puede ser revisado o revisado.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`, luego fijar el recuento de las rondas a 5 y ver los retornos decrecientes. ¿En qué ronda se detiene la convergencia adicional?
   Traducción:运行`code/main.py`¿Y qué ronda de extracontactos se detiene?
2. Si se añade un cuarto agente con un papel adversario: siempre no está de acuerdo con la mayoría actual. ¿Rotará o mejorará la convergencia?
   China: Añadir un cuarto agente que tiene un papel de oposición:总是与当前多数不同意. ¿Esto va a dañar o mejorar el ingreso?
3. En el gráfico (impresión) el puntaje de acuerdo por ronda (fracción de agentes en la respuesta mayoritaria). ¿Cuándo alcanza 1,0 y es eso equivalente a "correcto"?
   ChinaX traducción: dibujo (印打) por rueda de la unidad de la cantidad de puntos de la mayoría de las respuestas (Agent de la mayoría de las respuestas)
4. Leer las ablaciones de la sección 4. Replicar el resultado "sólo para agentes" vs "sólo para rondas" vs "ambos" usando este código.
   China 翻译:阅读 Du 等人第 4 节消融实验──使用此代码复现"仅代理"vs"仅轮数"vs"两者结合"的结果──
5. Lea "¿Deberíamos estar volviéndonos locos?" (arXiv:2311.17371) y enumere dos variantes del debate más allá de la ronda de rotura  por ejemplo, dirigido por un juez, cadena de debate, adversarial.
   La traducción del texto original de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la lengua inglesa de la lengua inglesa de la lengua inglesa de la lengua inglesa de la lengua inglesa de la lengua inglesa de la lengua inglesa de la lengua inglesa de la lengua inglesa de la lengua inglesa de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Society of Mind / 心智社会 | "Minsky's idea" / "Minsky 的想法" | Intelligence as interacting specialists; 1986 framing now operationalized via LLM debate. / 智能作为交互的专家；1986 年的框架现在通过 LLM 辩论实现。 |
| Multi-agent debate / 多 Agent 辩论 | "Agents argue" / "Agent 争论" | N agents propose, critique each other, revise over R rounds, majority-vote. / N 个 Agent 提议、批评彼此、在 R 轮中修改、多数投票。 |
| Consensus / 共识 | "They agree" / "他们一致" | Not epistemic truth — just fraction-on-majority-answer. Can be confidently wrong. / 不是认识论真理——只是多数答案上的比例。可能自信地犯错。 |
| Rounds / 轮次 | "Exchange steps" / "交换步骤" | One round = each agent reads the others and updates once. / 一轮 = 每个 Agent 阅读其他 Agent 并更新一次。 |
| Heterogeneous debate / 异构辩论 | "Mix model families" / "混合模型族" | Using different base models to decorrelate errors. / 使用不同的基础模型来去相关错误。 |
| Sycophancy cascade / 谄媚级联 | "Everyone agrees with the loud one" / "每个人都同意最大声的" | Debate failure where agents defer to the most confident agent regardless of correctness. / 辩论失败，Agent 不顾正确性屈从于最自信的 Agent。 |
| NLSOM | "129-agent society" / "129 Agent 社会" | Natural-language society of mind; Zhuge et al.'s scaled version. / 自然语言心智社会；Zhuge 等人的扩展版本。 |
| Correlated error / 相关错误 | "Same model, same bug" / "相同模型，相同 bug" | Why self-consistency saturates; debate across different views decorrelates. / 自我一致性为什么饱和；不同观点的辩论去相关。 |

## Más Leer más Leer más

- [Du et al. — Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325) el documento de referencia, ICML 2024
    通过多 Agent 辩论改进语言模型的事实性和推理  参考论文, ICML 2024 辩论改进语言模型  论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论文, 论
- [Zhuge et al. — Mindstorms in Natural Language-Based Societies of Mind](https://arxiv.org/abs/2305.17066) 129-agente NLSOM
  China                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
- [Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs](https://arxiv.org/abs/2311.17371) Variancias de debate de valores de referencia
  Traducción: ¿Deberíamos ir hacia la locura?
- [Debate project page](https://composable-models.github.io/llm_debate/) El código, los demos y los detalles de ablación de Du et al.
  China 文翻译:辩论项目页面  Tu y otros 代码、演示和消融细节
