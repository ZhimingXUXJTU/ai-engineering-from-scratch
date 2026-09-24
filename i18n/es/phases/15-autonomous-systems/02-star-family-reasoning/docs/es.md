# STAR, V-STAR, Quiet-STAR  Razonamiento autodidacta  STAR Series auto-título método

> El más pequeño bucle de auto-mejora posible se encuentra dentro de la lógica. Un modelo genera una cadena de pensamientos, mantiene los que aterrizan en las respuestas correctas, y los ajusta a la perfección. Eso es STAR. V-STaR añade un verificador para que la selección de tiempo de inferencia sea mejor. Quiet-STaR empuja la razón a cada token. Los tres trabajan. Ninguno de ellos es mágico. El bucle conserva cualquier atajo que sucedió para llegar a la respuesta correcta.

> **【中文解读】**El último ciclo de auto-reforma oculto en el proceso de la reflexión: el modelo genera una cadena de pensamiento, mantiene un proceso de reflexión de la respuesta correcta, se modifica en estos datos.

> **【拓展：STaR → OpenAI o1/o3 的自我改进】**La serie STaR es el modelo central de la formación de "auto-exploración" para entrenarse con su propia racionalización. La serie OpenAI o1/o3 de modelos adopta un entrenamiento de la fuerza química similar: generar varios caminos de racionalización, elegir los correctos, utilizarlos para mejorar el modelo.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, bootstrap-loop simulator) | **语言:** Python (标准库，bootstrap 循环模拟器)
**Prerequisites:** Phase 13 · 01-03 (Reasoning and CoT), Phase 15 · 01 (long-horizon framing) | **前置知识:** Phase 13 · 01-03（推理与 CoT），Phase 15 · 01（长程框架）
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 13·01-03(CoT 思维链) Fase 11·08(SFT 监督微调) Fase 15·01(长程 Agent 框架) STaR es el círculo más pequeño de "自蒸 + 推理增强"
> ¿ Qué es esto ?**【类比】**STaR = "estudiante auto-aprobación"―普通学习 = 老师改作业学生订正(人工标注推理过程);STaR = 学生写推理→对答案→对对的推理保留并自我再练一遍(自我生成训练数据)―problema es: a veces el proceso de推理 es incorrecto pero la respuesta resulta ser la respuesta a la respuesta,STaR se va a reforzar este tipo de "蒙对" V-STaR加加一个法官验证器) 掉错推理──
> ️ **【易错点】**STaR  entrenamiento                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

## El problema es introducción introducción

La forma más sencilla de enseñar a un modelo a razonar es recopilar rastros de razonamiento escritos por el hombre.

> El método directo de la teoría del modelo es recopilar el trayecto de la teoría de los libros humanos. Esto es costoso y lento, y también está limitado a la voluntad humana de escribir una cadena de pensamiento de alta calidad.

STaR (Self-Teught Reasoner, Zelikman et al., 2022) pregunta: ¿qué pasa si el modelo escribe sus propias racionalidades y las califica en función de las respuestas conocidas?

> STaR(auto-education推理器, Zelikman 等人,2022) propone: si el modelo redacta el proceso de推理 de sí mismo y se relaciona con el conocido respuesta对照评分会怎么样?


> **【中文解读】**Star 家族推理技术 (STAR、Quiet-STaR、ReST、ReST-EM) a través de la formación de sí mismo de generaciones para mejorar la capacidad de pensar en el LLM, la idea central es: hacer que el modelo genere un modelo de ideas, un modelo de alta calidad, un modelo de movimiento, un ciclo de ideas.

1. Muestre un rasgo de razonamiento más respuesta.
2. Si la respuesta final es correcta, mantenga el rastro.
3. - En sintonía con los rastros guardados.
4. Repito, ¿qué quieres?

GSM8K y CommonsenseQA mejoraron sin nuevas anotaciones humanas. Pero el bucle tiene un sesgo incorporado: cualquier razonamiento que produjo la respuesta correcta se conserva, independientemente de si el razonamiento en sí era sólido. V-STaR (Hosseini et al., 2024) corregir esto con un verificador aprendido; Quiet-STaR (Zelikman et al., 2024) generaliza la idea a per-token racionales internos.

> Es válido. GSM8K y CommonsenseQA se han mejorado sin la marca de nuevos humanos. Pero el ciclo tiene una diferencia interna: cualquier proceso de reflexión que genere una respuesta correcta se mantiene, independientemente de si la reflexión en sí misma es razonable.

## El concepto central.

### STaR: arranque en lo que funcionó

Comience con un modelo base con alguna capacidad de razonamiento débil. En cada problema de entrenamiento, muestre una razón más una respuesta. Si la respuesta coincide con la etiqueta, mantenga el (problema, razón, respuesta) triple. Ajuste el modelo en el conjunto mantenido. Repita.

> Comienza con un modelo básico con una capacidad de raciocinio más débil. En cada problema de entrenamiento, toma un proceso de raciocinio para agregar respuesta. Si la respuesta coincide con la etiqueta, retenga el problema.

Si el modelo nunca puede resolver un problema, el bucle no puede aprender de él.**rationalization**En el caso de problemas que el modelo no logre, inyectar la respuesta correcta como una pista y volver a impulsar el modelo para producir una justificación que lo lleve.

> Un cambio clave: Si el modelo nunca puede responder correctamente a un problema, el ciclo no puede aprender de él.**合理化**Para el problema del fracaso del modelo, se inyecta la respuesta correcta como una sugerencia, se produce una nueva sugerencia del modelo que se orienta hacia la respuesta.

Resultado en el documento original (Zelikman et al., 2022): un modelo base GPT-J mejoró en GSM8K del 5.8% al 10.7% a través de rondas repetidas de STaR con racionalización  aproximadamente 5 puntos porcentuales absolutos. En CommonsenseQA, el GPT-J 6B entrenado en STaR alcanzó el 72.5%, comparable con un GPT-3 175B (~73%)

> El resultado del primer ensayo fue que el modelo de base de GPT-J, a través de la racionalización de la repetición de STaR, aumentó de 5.8% en GSM8K a 10.7% en torno a 5 puntos de porcentaje. En CommonsenseQA, el modelo de GPT-J 6B de la formación de GPT-J alcanzó el 72,5%, con GPT-3 175B de la formación de TaR, que se puede ajustar a la GPT-175B, aproximadamente 73%, en comparación con el modelo de la formación de la evaluación de marcas de mano de aproximadamente 30 veces mayor.

### V-STaR: entrenar a un verificador con DPO

Los datos de la serie de racionalidades de los usuarios de STaR son los datos de los usuarios de los datos de los usuarios de STaR. Hosseini et al. (2024) observan que estos son también datos: cada par de (racional, "es correcto esto") puede entrenar a un verificador. Utilizan la optimización de preferencias directas sobre soluciones correctas e incorrectas para construir un ranker.

> STaR  abandonando las hipótesis incorrectas―Hosseini 等人2024) observan estas también datos: por cada proceso de hipótesis, "es correcto o no") pueden ser entrenados en verificadores.

Delta reportada: +4 a +17 puntos porcentuales respecto a las líneas de referencia anteriores de auto-mejora en GSM8K y MATH, la mayor parte de la ganancia proviene del uso del verificador para la selección del tiempo de inferencia en lugar de para el ajuste fino adicional del generador.

> 报告的提升: en GSM8K 和 MATH 上比前的自我改进基线提升 +4至 +17 百分点, la mayor parte de la mejoría proviene de la evaluación de la selección de verificadores y no de los extra generadores de micro调

### Quiet-STaR: racionalidades internas por token

Zelikman et al. (2024) preguntó: ¿qué pasa si el modelo aprende a generar una racionalidad interna corta en cada posición de token, no solo entre el problema y la respuesta? Quiet-STaR entrena a un modelo para emitir un "pensamiento" oculto antes de cada token predicho, luego mezcla la predicción consciente del pensamiento con la predicción de línea de base a través de un peso aprendido.

> Zelikman 等人 2024) propone: si el modelo se encuentra en cada posición de un token  generando una breve reflexión interna, no sólo entre el problema y la respuesta? Quiet-STaR Training model Emitir un "pensamiento" oculto antes de cada token , luego a través del aprendizaje el peso del pensamiento se mezclará entre el pronóstico perceptivo y el pronóstico de base .

Resultado: Mistral 7B obtuvo mejoras absolutas de cero disparos en GSM8K del 5.9% al 10.9% y CommonsenseQA del 36.3% al 47.2% sin ajuste específico de tarea. El modelo aprendió "cuándo pensar"  los tokens duros obtienen racionales internos más largos; los fáciles casi no obtienen ninguno.

> Resultado:Mistral 7B en GSM8K arriba de la muestra absolutamente aumentó de 5.9% a 10.9%, en CommonsenseQA desde 36.3% a 47.2%, sin necesidad de tareas específicas de la micro-modución.

### ¿Por qué los tres comparten una preocupación por la seguridad?

Los tres métodos utilizan la respuesta final como la señal de gradiente. Una razón que llega a la respuesta correcta a través de razonamiento defectuoso  explotando un atajo, adivinando o utilizando un patrón no generalizador  se refuerza positivamente. En los problemas de distribución el atajo funciona. En los problemas fuera de distribución rompe silenciosamente.

> Tres métodos utilizan la respuesta final como señal de gradiente. A través de la raciocinio de deficiencias para alcanzar la respuesta correcta. El proceso de raciocinio de la respuesta correcta se fortalece de forma positiva. En los problemas distribuidos, el raciocinio es válido. En los problemas extra-distrusidos, el raciocinio fracasa silenciosamente.

El verificador de V-STaR mitigará al aprender a clasificar las racionalidades, pero el verificador está entrenado en el mismo conjunto de etiquetas. Puede aprender a preferir el razonamiento incorrecto bien formado a la incertidumbre honesta. El diseño más seguro es combinar datos de estilo STaR con (a) modelos de recompensa supervisados por el proceso (recompensar pasos intermedios, no solo respuestas) y (b) evaluación OOD prolongada que rompe atajos simples.

> El verificador de V-STaR se ha capacitado en el mismo conjunto de etiquetas, pero puede aprender a preferir el formato de la hipótesis buena pero errónea y no la incertidumbre de la realidad.

### Comparación

| Method | Training signal | Inference cost | Data waste | Known failure mode |
|---|---|---|---|---|
| 方法 | 训练信号 | 推理成本 | 数据浪费 | 已知失败模式 |
| STaR | keep (rationale, answer) if correct | 1x | discards all incorrect rationales | shortcut rationales |
| STaR | 正确时保留（推理，答案） | 1x | 丢弃所有不正确的推理 | 捷径推理 |
| STaR + rationalization | above + correct-answer hinted retries | 1x | less | rationalized rationales may be implausible |
| STaR + 合理化 | 上述 + 正确答案提示重试 | 1x | 较少 | 合理化的推理可能不可信 |
| V-STaR | STaR + DPO verifier from both classes | Nx (best-of-N) | minimal | verifier can reinforce confident wrongness |
| V-STaR | STaR + 两类 DPO 验证器 | Nx（N 中选优） | 最少 | 验证器可能强化自信的错误 |
| Quiet-STaR | per-token rationale + mixing weight | 1.5-3x | minimal | still answer-conditioned gradient |
| Quiet-STaR | 每 token 推理 + 混合权重 | 1.5-3x | 最少 | 仍是答案条件梯度 |

### Donde esto se encuentra en la pila de 2026

El STAR es viejo. Pero el patrón reaparece en todas partes en 2025-2026. RL en problemas matemáticos verificables (DeepSeek-R1, Kimi-k1.5, o1) es la señal de gradiente de respuesta de STaR, ampliada. Los modelos de recompensas de procesos (Lightman et al., 2023; "Verifiquemos paso a paso" de OpenAI) son la alternativa supervisada por el proceso. AlphaEvolve (Lección 3) es STaR para código, con un evaluador de programa en lugar de una etiqueta. La Máquina Darwin Godel (Ley 4) es STaR para el propio andamio del agente.

> STaR  está muy viejo. Pero este modelo surge en 2025-2026 años de edad. RL (en inglés) en el problema matemático de validación DeepSeek-R1  Kimi-k1.5  o1) es la respuesta de STaR                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

Comprender STaR hace que todos estos clics. Es el ciclo de auto-mejora mínimo viable.

> Comprender que STaR 让所有这些都说通―― es el ciclo de auto-reforma más pequeño posible―

## Usalo con el marco de ejecución
```figure
reflection-loop
```

## Usalo

`code/main.py`ejecuta un ciclo STaR simulado en una tarea aritmética de juguete.

- Cómo la precisión se eleva sobre las balas de arranque.
  La tasa de recaudación de los datos de la empresa se ha incrementado en un período de tiempo de tres años.
- Cómo se introducen los atajos: el simulador incluye una clase de racionalización "perezosa" que obtiene la respuesta correcta el 40% de las veces pero generaliza mal.
  En el caso de los modelos de la forma en que se utilizan, el 40% de las veces se obtiene la respuesta correcta, pero la generalización es muy baja.
- Cómo un verificador (estilo V-STaR) ayuda a la inferencia pero no puede recortar completamente los atajos introducidos durante el entrenamiento.
  Traducción:V-STaR 风格) ¿Cómo ayudar en la meditación pero no puede completamente modificar la introducción de los métodos durante el entrenamiento。

## Envíe el producto .

`outputs/skill-star-loop-reviewer.md`ayuda a auditar una propuesta de diseño de razonamiento autodidacta antes de entrenar en ella.

> `outputs/skill-star-loop-reviewer.md` ayudarle a evaluar la auto-aprendizaje de la propuesta antes del entrenamiento 

## Los ejercicios.

1. Ejecutar el simulador. Establecer la frecuencia de acceso directo a cero, luego a 0.4. ¿Cuánto difiere la precisión final entre las dos carreras, aunque ambas alcancen >90% en la distribución de entrenamiento?
   Traducción: ¿Cuánto diferencia la tasa de precisión final entre dos operaciones, incluso si ambas alcanzan > 90% en la distribución de entrenamiento?

2. Añadir una prueba de OOD prolongada al simulador. Dibujar problemas de una distribución diferente y evaluar el modelo arrancado tanto en los conjuntos de distribución como en los conjuntos de OOD. Cuantificar la brecha.
   En inglés: 量化差距.

3. Lea el documento Quiet-STaR (arXiv:2403.09629) Sección 3. Explica el símbolo "fin de pensamiento" y la cabeza de peso mezclado en tres frases cada una.
   En el caso de los ejemplos de la palabra "todo" y "todo" en el caso de los ejemplos de la palabra "todo" en inglés, el significado de "todo" en inglés es "todo".

4. Comparar el filtro de mantenimiento si es correcto de STaR con una alternativa supervisada por el proceso que recompensa cada paso racional de forma independiente.
   China: 识别标注成本差异和质量差异.

5. Diseñar una evaluación que capture racionales de atajos en un modelo implementado. No tiene que ser perfecto  tiene que romper los atajos más simples que un bucle STaR reforzaría.
   China: sólo necesita romper el más simple camino de fortalecer el ciclo de STaR.

## Términos clave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| STaR | "Self-Taught Reasoner" | Fine-tune on model-generated rationales that land correct answers; repeat |
| STaR | "自我教学推理器" | 在模型生成的正确推理上微调；重复 |
| Rationalization | "Hinted retry" | Inject the correct answer and re-prompt for a rationale |
| 合理化 | "提示重试" | 注入正确答案重新提示推理 |
| V-STaR | "Verifier STaR" | DPO-train a verifier on both correct and incorrect rationales |
| V-STaR | "验证器 STaR" | DPO 训练验证器用于推理时选择 |
| Quiet-STaR | "Per-token rationales" | Generate hidden thoughts at every token position; mix with baseline |
| Quiet-STaR | "每 token 推理" | 在每个 token 位置生成隐藏思考；与基线预测混合 |
| Answer-conditioned gradient | "Outcome-based signal" | The training loop rewards final answers, not reasoning steps |
| 答案条件梯度 | "基于结果的信号" | 训练循环奖励最终答案，而非推理步骤 |
| Process reward model | "Step-level verifier" | Reward model trained on per-step correctness, not outcome |
| 过程奖励模型 | "步骤级验证器" | 在每步正确性上训练的奖励模型 |
| Shortcut rationale | "Right answer, wrong reasoning" | A rationale that reaches the label via a non-generalizing pattern |
| 捷径推理 | "正确答案，错误推理" | 通过不可泛化模式达到标签的推理 |

## Más Leer más Leer más

- [Zelikman et al. (2022). STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/abs/2203.14465) el papel original.
  El texto original de la traducción de la traducción de la lengua inglesa es:
- [Hosseini et al. (2024). V-STaR: Training Verifiers for Self-Taught Reasoners](https://arxiv.org/abs/2402.06457) añade un verificador de DPO para la selección del tiempo de inferencia.
  China: 添加 DPO 验证器用于推理时选择.
- [Zelikman et al. (2024). Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking](https://arxiv.org/abs/2403.09629) rationales internos por token.
  En inglés, "Todo el mundo está en el camino".
- [Lightman et al. (2023). Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) modelos de recompensas de proceso, la señal de gradiente alternativa.
  En inglés, el proceso de recompensa es un proceso de recompensa.
- [DeepSeek-R1 paper (arXiv:2501.12948)](https://arxiv.org/abs/2501.12948) RL en tareas verificables, STaR escalado a la formación fronteriza.
  RL,STaR 扩展到前沿训练──
