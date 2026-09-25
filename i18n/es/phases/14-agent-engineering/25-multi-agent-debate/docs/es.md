# Debate y colaboración multi-agente

> Du et al. (ICML 2024, "Sociedad de Mentes") ejecuta instâncias de modelo N que proponen respuestas independientemente, luego se critican iterativamente entre sí en rondas R para converger. Mejora la factualidad, el seguimiento de reglas, el razonamiento.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 12 (Workflow Patterns), Phase 14 · 05 (Self-Refine and CRITIC) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objetivos de aprendizaje

- Explicar el protocolo de debate: N propuestas, R rondas, convergen en una respuesta compartida.
- Describa por qué el debate mejora la realidad, el cumplimiento de las reglas y el razonamiento.
- Explica una topología escasa: no todos los debatedores necesitan verse entre sí.
- Implementar un debate sobre un LLM con guión con variantes de red completa y escasas; medir el costo de los tokens frente a la precisión.

## El problema es la introducción del problema

El auto-refinamiento (lección 05) es un modelo que se critica a sí mismo  riesgo de pensamiento grupal. CRITIC (lección 05) justifica la crítica en herramientas externas  no siempre disponibles. El debate introduce un tercer modo: múltiples instancias, crítica cruzada, convergencia por desacuerdo.

> Auto-refinado (第 5 课) es un modelo de autocrítica que existe en el grupo de pensamiento.

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 14·05(Self-Refine / CRITIC) 辩论是自炼的多实例扩展,不理解"一个模型自我批评为什么会陷入群体思维"就看不出辩论为什么要 N个实例;Fase 14·12(Workflow Patterns) 理解主管-trabajadores 和监督员 模式,本节的中心和讲话拓就是监督员的具体实现.


> **【中文解读】**El debate de múltiples agentes permite que varios ejemplos de LLM discutan el mismo problema desde diferentes perspectivas para mejorar la calidad de la racionalización.

> **{【拓展：多 Agent 辩论是 2023-2025 年的研究热点。Du et al. (2023) 证明两个...】}**El debate sobre los agentes múltiples es un punto de investigación de 2023-2025. Du et al. (2023) demostró que dos ejemplos de debate ChatGPT pueden mejorar significativamente la tasa de precisión de la hipótesis. La práctica de 2026 demostró que los 3-5 ejemplos de debate sobre los agentes tienen un mejor resultado.
## El concepto central.

### Sociedad de las Mentes (Du et al., ICML 2024)

> ¿ Qué es esto ?**【类比】**Más Agente 辩论像学术同行评审:你写论文(N=3 个独立作者各写一版)→ 投稿后 3 个审稿人读对方的版本写评审(R 轮交叉批评)→ 作者根据评审 修改 → 几轮后论文收──关键洞察:单个作者会自信写错(Self-Refine的群体思维),3 个独立作者挑错彼此更容易出现象──但全连接(每读者所有人) 评审成本是O(N2) 所以会议"area chair + reviewers"的星形拓(hub-and-spoke),审稿人只用和沟通,成本降到O(N) 

- N ejemplos modelo proponen de forma independiente respuestas a la misma pregunta.
- Durante las rondas R, cada modelo lee las propuestas de los demás y las critica.
- Los modelos actualizan sus respuestas basándose en las críticas.
- Después de las rondas R, devuelva la respuesta convergente.

Los experimentos originales utilizaron N=3, R=2 debido al costo. La precisión mejora con más agentes y más rondas en problemas difíciles (MMLU, GSM8K, Valididad de movimiento de ajedrez, generación de biografía).

> El debate de múltiples agentes permite que varios agentes presenten diferentes puntos de vista sobre el mismo problema y el argumento para mejorar la calidad de la racionalización. Este método se desempeña mejor en tareas de racionalización complejas que un solo agente.

Las combinaciones de modelos cruzados superan los debates de modelos únicos: ChatGPT + Bard juntos > cualquiera solo.

> 跨模型组合胜过单一模型辩论:ChatGPT + Bard uní de un solo uno es mejor que cualquier otro.

> El debate de múltiples agentes permite que varios agentes presenten diferentes puntos de vista sobre el mismo problema y el argumento para mejorar la calidad de la racionalización. Este método se desempeña mejor en tareas de racionalización complejas que un solo agente.

### Topología de la escasa

"Mejorar el debate multi-agente con la topología de comunicación de Sparse" (arXiv:2406.11776, 2024-2025) mostró que el debate de red completa no siempre es óptimo. Las topologías de Sparse (estrella, anillo, centro y voz) pueden igualar la precisión a un menor costo de token. Cada debater ve solo un subconjunto de pares.

> "Mejorando el debate multi-agente con la topología de comunicación de Sparse" (arXiv:2406.11776, 2024-2025) muestra que el debate en todo el mundo no es siempre el mejor.

> El debate de múltiples agentes permite que varios agentes presenten diferentes puntos de vista sobre el mismo problema y el argumento para mejorar la calidad de la racionalización. Este método se desempeña mejor en tareas de racionalización complejas que un solo agente.

Las implicaciones:

- N=5, R=3 = 5 × 3 = 15 propuestas, cada una leyendo 4 pares = 60 opciones de crítica.
- Estrella N=5, R=3 (un centro + 4 bocinos) = 15 propuestas, bocinos sólo leen el centro = 12 operaciones de crítica.

### Cuando el debate ayuda

- **Factuality.**En las propuestas independientes, el control cruzado reduce las alucinaciones.
- **Rule-following.**Validez de movimiento de ajedrez  un modelo pierde una regla, otros la atrapan.
- **Open-ended reasoning.**Muchos marcos se limitan a la respuesta correcta.

### Cuando el debate duele

- **Latency-sensitive UX.**Las rondas en serie N × R es la latencia que tal vez no tengas.
- **Cost-sensitive scale.**N × R tokens por pregunta.
- **Simple factual lookups.**Una búsqueda es más barata que cinco debates.

### 2026 instancias prácticas

- **Anthropic orchestrator-workers**(Lección 12)  una variante del debate con un paso de síntesis.
- **LangGraph supervisor**(Lección 13)  Router central + agentes especializados pueden implementar el debate como un nodo.
- **OpenAI Agents SDK**(Lección 16)  Los agentes se entregan para la crítica iterativa.
- **Multi-agent evals** debate en pareja + evaluador-optimizador para la señal de evaluación.

### Cuando este patrón va mal

> ¿ Qué es esto ?**【困惑】**P: ¿Cuándo vale la pena usar el debate? ¿Cuándo vale la pena usar el retraso y el costo de N×R? Parece muy alto. A: Sólo se usa en el escenario de "un modelo equivocado a la vez cuesta mucho más que el costo del debate". Fórmula de juicio: costo del debate = N×R× costo de razonamiento único; pérdida esperada de un modelo equivocado a la vez =  errores de tasa ×  errores de tasa ×  errores de tasa ×  errores de tasa                                                                                                                                                                                                                                                                                                                                                                                                       

- **Convergence collapse.**Todos los agentes convergen en la primera respuesta equivocada, y se mitigan con las rondas de desacuerdo requeridas.
- **Hub failure.**En una topología estelar, un mal centro corrompe a todos.
- **Prompt homogenization.**Todos los agentes utilizan el mismo tipo de instrucciones, producen las mismas respuestas, utilizan diferentes instrucciones y/o modelos.

> **收敛崩溃。**Todos los agentes reciben la primera respuesta errónea.
> **中心故障。**En el medio de la estrela, un centro malo contamina a todos los habitantes.
> **提示同质化。**Todos los agentes utilizan la misma sugerencia; generan la misma respuesta.

## Construye y realiza.

> ️ **【易错点】**场景: desarrolladores con el mismo prompt 起起了5辩论者 实例期待"多样化观点" → 后果:5 个实例给出几乎相同的答案 (甚至相同的错误),辩论沦为N 倍成本的自我精炼,这叫"快速同化" → 修复:要么用不同模型 (GPT-4o + Claude + Gemini,异构带来真分歧),要么给每个辩论者不同角色 (你是怀疑论者"",你是乐观派""你是细节核查员"),要么至少随机化温度 (Temperatura):
```figure
debate-converge
```

## Construye el mismo

`code/main.py`Implementa el debate de la Sdlib:

- `Debater`clase (Mestre de Derecho escrito con derivación de opinión por debatedor).
- `FullMeshDebate`y `SparseDebate`Los corredores.
- Tres preguntas: una factual, una basada en reglas, una razonamiento.
- Metricas: respuesta convergente, rondas a convergencia, operaciones de crítica total.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Resultado: exactitud y coste por protocolo; coincidencias escasas en 2/3 de las preguntas a un coste menor.

> 输出: precisión y coste de cada acuerdo; raridad en 2/3 de los problemas para un coste más bajo para la conexión completa.

> El debate de múltiples agentes permite que varios agentes presenten diferentes puntos de vista sobre el mismo problema y el argumento para mejorar la calidad de la racionalización. Este método se desempeña mejor en tareas de racionalización complejas que un solo agente.

## Usalo con el marco de ejecución

- **Anthropic orchestrator-workers**Para debates simples de dos o tres trabajadores.
- **LangGraph**El Parlamento Europeo ha aprobado el informe de la Comisión en el marco del debate sobre el tema.
- **Custom**para investigaciones o garantías de corrección especializadas.

## Envíe el producto .

`outputs/skill-debate.md`El programa de trabajo de la Comisión de Investigación y Desarrollo de la Información sobre la información sobre la información y la información sobre la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información.

> `outputs/skill-debate.md` Construir un multi-agente que pueda ser configurado  N  R 和收 规则的多代理 辩

> El debate de múltiples agentes permite que varios agentes presenten diferentes puntos de vista sobre el mismo problema y el argumento para mejorar la calidad de la racionalización. Este método se desempeña mejor en tareas de racionalización complejas que un solo agente.

## Los ejercicios.

1. Implementar una regla de "desacordo forzado": en la primera ronda, cada debater debe presentar una propuesta distinta.
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Añadir una agregación ponderada por confianza: los debatedores regresan (respuesta, confianza); el agregador pesa por confianza. ¿Ayudan?
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. ¿Es la heterogeneidad que mejora la precisión?
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. Medir el costo de los tokens para la malla completa vs. escaso en sus 3 preguntas.
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. Lea el artículo de la Sociedad de Mentes.
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Debate | "Multi-agent critique" | N proposers, R rounds of cross-critique, converge |  |
| Full mesh | "Everyone reads everyone" | Every debater reads every peer each round |  |
| Sparse topology | "Limited peer view" | Debaters read only a subset of peers |  |
| Hub-and-spoke | "Star topology" | One central debater, N-1 spokes read only the hub |  |
| Convergence | "Agreement" | Debaters converge on a shared answer |  |
| Society of Minds | "Du et al. debate paper" | ICML 2024 multi-agent debate method |  |

## Más Leer más Leer más

- [Du et al., Society of Minds (arXiv:2305.14325)](https://arxiv.org/abs/2305.14325) debate canónico multi-agente
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Sparse Communication Topology (arXiv:2406.11776)](https://arxiv.org/abs/2406.11776) resultados topológicos escasos
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) los trabajadores orquesta­doros como variante de debate
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) contraparte de autocrítica de modelo único
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
