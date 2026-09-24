# ¿Por qué multi-agente?

> Un agente golpea una pared, el movimiento inteligente no es un agente más grande, sino más agentes.

> **【中文解读】**Este capítulo presenta por qué se necesita más agentes  sistemas  un agente                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

> **【拓展：why multi agent→具体应用】** Un agente en el tratamiento de tareas complejas se enfrenta a tres botellas:  1) 上下文溢出所有信息塞进一个窗口,重要被淹没;  2) 角色混乱 Un agente desempeña varios papeles que causan un conflicto de palabras;  3) 串行执行工具调用只能排队――多 Agent 通过分工协作解决这些问题――Antropic research indicates,多 Agent 系统在 BrowseComp 基准上多 Agent 升 90.2%,80% 方仅由代币使用解释量.

> ¿ Qué es esto ?**【前置】**学本节前Permanecer de dominio:Fase 14(Ingeniería de agentes) Todo, especialmente Fase 14·01(Fase 14·01(Curso de agentes) y Fase 14·28(Patanos de orquestación)。本节回答"什么时候用多 Agent"简单回答:单 Agent + 工具不够时。Antropic 经验法则:任务需要 > 50 工具调用、或 > 1 角色(如研究员 + 写手)、或并行能省时间,才考虑多 Agent。

> ¿ Qué es esto ?**【类比】**单 Agent vs 多 Agent = 全能管家 vs 专业团队──全能管家──单 Agent) puede hacer todo pero cada cosa no es精: mañana hacer comida、下午修车、晚上辅导作业,每样都半吊子──专业团队──多 Agent:厨师专做饭、机修工专修车、家教专辅导,每个人精一行──代价:协调成本(Agent 间通信) y complejidad aument简单任务单 用 Agent 更划算──

**Type:** Learn | **类型:** 学习
**Languages:** TypeScript | **语言:** TypeScript
**Prerequisites:** Phase 14 (Agent Engineering) | **前置知识:** Phase 14 (Agent 工程)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizaje

- Identificar el límite máximo de un agente único (desbordamiento de contexto, experiencia mixta, cuello de botella secuencial) y explicar cuándo dividir en múltiples agentes es el movimiento correcto
  China Translation: Identificar un agente único 上限(上下文溢出、专业能力混合、串行瓶),并解释何时分分多代理是正确的选择
- Compara patrones de orquestación (pipelina, ventilador paralelo, supervisor, jerárquico) y seleccione el correcto para una estructura de tarea dada
  China: comparación de la estructura de la tarea y la estructura de la tarea, y la selección de la estructura adecuada
- Diseñar un sistema multiagente con límites claros de rol, estado compartido y contrato de comunicación
  China 译文: diseñar un sistema multi-agente con un papel claro en el marco de la frontera, el estado compartido y el acuerdo de comunicación
- Analiza las diferencias entre la complejidad de varios agentes (latencia, costo, dificultad para deshacerse) y la simplicidad de un solo agente
  En inglés, el peso entre el análisis de múltiples agentes  complexidad 延迟、成本、调试难度) y el balance entre un agente 简单性

## El problema es la introducción del problema

Construiste un único agente en la Fase 14. Funciona. Puede leer archivos, ejecutar comandos, llamar a las API y razonar sobre los resultados. Luego lo apuntas a una base de código real: 200 archivos, tres idiomas, pruebas que dependen de la infraestructura y un requisito para investigar las API externas antes de escribir código.

> En la Fase 14 se construye un único agente. Funciona bien, puede leer documentos, ejecutar órdenes, utilizar API y hacer una reflexión sobre los resultados. Luego se dirige a una verdadera base de códigos: 200 documentos, tres idiomas, pruebas de dependencia de infraestructura, así como la necesidad de primero estudiar las necesidades de código de la API externa.

La brecha entre los agentes de demostración y los agentes de producción es la brecha entre "un archivo, un idioma, una herramienta" y "muchos archivos, muchos idiomas, muchas herramientas con dependencias".

> 演示 Agente y Producción Agente la diferencia entre "un documento, una lengua, un instrumento" y "muchos documentos, muchos lenguajes, muchos instrumentos dependientes" 演示有效因为任务适合――生产失败因为任务不适应――

El agente se ahoga. No porque el LLM sea tonto, sino porque la tarea excede lo que un bucle de agente puede manejar. La ventana de contexto se llena de contenido de archivo. El agente olvida lo que leyó hace 40 llamadas de herramienta. Trata de ser un investigador, un codificador y un revisor a la vez, y hace mal los tres.

> El agente se ha desmoronado. No es porque el LLM sea estúpido, sino porque la tarea va más allá del alcance de un solo agente.

Este es el techo de un solo agente.

> Es un agente único y limitado. Cada vez que una tarea requiere las siguientes condiciones, se encuentra:

El techo es estructural, no algorítmico. Un LLM mejor retrasa el techo pero no lo elimina. Una ventana de contexto de 1M-token se llena con la misma seguridad que una de 200k  sólo necesita más archivos.

> La límite superior es estructural, no algorítmica. Mejor LLM 延迟上限但不移除它──1M token 上下文窗口像200k 一样确定地填满只是需要更多文件──

- **More context than fits in one window**- leer 50 archivos se hace pasar de 200 mil tokens
  En inglés:**超出一个窗口容量的上下文** 读取 50 文件会超过 200k tokens
- **Different expertise at different stages**- la investigación requiere una motivación diferente a la generación de código
  En inglés:**不同阶段需要不同的专业知识** Los estudios necesitan generar diferentes sugerencias con el código
- **Work that can happen in parallel**- ¿Por qué leer tres archivos secuencialmente cuando puedes leerlos simultáneamente?
  En inglés:**可以并行执行的工作**  Pueden leer tres documentos al mismo tiempo, ¿por qué deben ordenarse?

## El concepto central.

### El techo de un solo agente

Un agente único es un bucle, una ventana de contexto, un sistema de instrucciones.

> Un agente único es un ciclo, una ventana de texto, un sistema de sugerencias.

```
┌─────────────────────────────────────────┐
│            SINGLE AGENT                 │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │         Context Window            │  │
│  │                                   │  │
│  │  research notes                   │  │
│  │  + code files                     │  │
│  │  + test output                    │  │
│  │  + review feedback                │  │
│  │  + API docs                       │  │
│  │  + ...                            │  │
│  │                                   │  │
│  │  ██████████████████████ FULL ███  │  │
│  └───────────────────────────────────┘  │
│                                         │
│  One system prompt tries to cover       │
│  research + coding + review + testing   │
│                                         │
│  Result: mediocre at everything         │
└─────────────────────────────────────────┘
```

El sistema único de instrucciones es la causa raíz. Tiene que dar instrucciones para la investigación, codificación, revisión y pruebas simultáneamente. Cada instrucción diluye las otras. El agente termina "ok" en todo, excelente en nada.

> 单系统提示是根本原因――它必须同时为研究,编码,审核和测试提供指令――每条指令稀释其他――Agent 最终在所有事上"还行",在任何事上都不优秀――

Tres cosas se rompen:

> Tres problemas conducirán al colapso:

1. **Context saturation**En la curva 30, el agente ha consumido 150 mil tokens de contenido de archivos, salidas de comandos y razonamiento previo.
   En inglés:**上下文饱和** 工具结果不断堆积──到第30轮时,Agent 已消耗了150k tokens文件内容、命令输出和先前推理──第5轮的关键细节丢失──

2. **Role confusion**- un mensaje de sistema que dice "es un investigador, codificador, revisor y probador" produce un agente que hace medio estudio, medio código y nunca termina la revisión.
   En inglés:**角色混乱** Un sistema de sugerencias que escribe "es usted un investigador, programador, revisor y examinador" generará un medio estudio, medio codificación, siempre un agente de revisión incompleta.

3. **Sequential bottleneck**- el agente lee el archivo A, luego el archivo B, luego el archivo C. Tres llamadas en serie de LLM.
   En inglés:**串行瓶颈** Agente 读取文件 A,然后文件 B,然后文件 C──三次串行 LLM 调用──三次串行工具执行──没有并行性──

El agente único es un generalista que se le pide que sea un especialista en cada paso.

> Un agente único es un agente que se requiere que en cada paso se convierta en un experto.

### La solución multiagente

Divide el trabajo. Dale a cada agente un trabajo, una ventana de contexto y una llamada de sistema sintonizada para ese trabajo:

> 拆分工作──Dá a cada agente una tarea、 una ventana de texto arriba abajo y un sistema de recomendaciones para la tarea:

Esta es la "separación de preocupaciones" aplicada a los agentes de LLM. El pedido de cada agente es más corto y más enfocado. La ventana de contexto de cada agente contiene solo lo que necesita. Cada agente puede ser probado y mejorado de forma independiente. El orquestrador maneja la composición.

> Se aplica a los "puntos de atención separados" del agente de LLM. Cada agente tiene un conjunto de pruebas y mejoras independientes.

```
┌──────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                          │
│                                                          │
│  "Build a REST API for user management"                  │
│                                                          │
│         ┌──────────┬──────────┬──────────┐               │
│         │          │          │          │               │
│         ▼          ▼          ▼          ▼               │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│   │RESEARCHER│ │  CODER   │ │ REVIEWER │ │  TESTER  │  │
│   │          │ │          │ │          │ │          │  │
│   │ Reads    │ │ Writes   │ │ Checks   │ │ Runs     │  │
│   │ docs,    │ │ code     │ │ code     │ │ tests,   │  │
│   │ finds    │ │ based on │ │ quality, │ │ reports  │  │
│   │ patterns │ │ research │ │ finds    │ │ results  │  │
│   │          │ │ + spec   │ │ bugs     │ │          │  │
│   └─────┬────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │
│         │           │            │             │         │
│         └───────────┴────────────┴─────────────┘         │
│                          │                               │
│                     Merge results                        │
└──────────────────────────────────────────────────────────┘
```

Cada agente tiene:
- Una solicitud de sistema enfocada ("Usted es un revisor de código. Su único trabajo es encontrar errores. ")
  China: un sistema de información centrado en el código.
- Su propia ventana de contexto (no contaminada por el trabajo de otros agentes)
  Traducción: su propio trabajo (en inglés)
- Un contrato de entrada/salida claro (recibe notas de investigación, código de salida)
  China: 清晰的输入/输出契约 (en inglés: 清晰的输入/输出契约)

El agente orquestrador sólo necesita entender la tarea de alto nivel y cómo delegar. No necesita saber cómo hacer cada subtarea. Cada agente especializado solo necesita saber su propio trabajo estrecho.

> 编排 应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对

### Sistemas reales que hacen esto

**Claude Code subagents**- cuando Claude Code genera un subagente con`Task`El padre mantiene su contexto limpio, el niño hace un trabajo enfocado y devuelve un resumen.

> **Claude Code 子 Agent** 当 Claude Código 使用 `Task`Cuando el agente de desarrollo, se crea un agente de desarrollo de alcance limitado.

El patrón es viral porque se compone: un subagente puede generar sus propios subagentes. Tres niveles de profundidad es común en tareas complejas de base de código; más allá de eso, el descomposición se vuelve dolorosa.

> Este modelo viral se propaga porque se puede combinar: Sub-Agencia puede generar su propio Sub-Agencia.

**Devin**- ejecuta un agente de planificación, un agente de codificación y un agente del navegador. El planificador divide el trabajo en pasos. El codificador escribe código. El navegador investiga la documentación. Cada uno tiene un contexto separado.

> **Devin** 运行一个规划代理一个编码代理 和一个浏览器代理――规划器将工作分解成步骤――编码器编写代码――浏览器研究文档―― cada uno tiene su propia 上下文――

La arquitectura de Devin es el patrón de supervisor de libros de texto: un planificador que posee el plan global, varios trabajadores especializados que ejecutan las rodajas.

> La arquitectura de Devin es el modelo de supervisor de la forma de los libros de texto: un planificador que tiene un plan integral, un especialista que ejecuta varios fragmentos de trabajo.

**Multi-agent coding teams (SWE-bench)**- los sistemas de mejor rendimiento en el banco SWE utilizan un investigador que lee la base de código, un planificador que diseña la corrección y un codificador que la implementa.

> **多 Agent 编码团队 (SWE-bench)** SWE-bench en el sistema de mejor rendimiento utilizando un investigador de la biblioteca de código, un planificador de diseño de la modificación del programa y un codificador de la implementación de la modificación.

El tablero de clasificación del banco SWE 2026 está dominado por sistemas multi-agentes. El patrón: un investigador con un amplio contexto para la comprensión de la base de código, un planificador con un prompt enfocado para el diseño de fijación, un codificador con requisitos estrictos de mecanografía para la implementación. Cada papel obtiene el prompt que necesita.

> 2026 SWE-bench  ranking by multiple Agent 系统主导──模式:带大上下文的研究员用于代码库理解、带焦点提示的规划器用于修复设计、带严格类型要求的编码器用于实现──每个角色获得它需要的提示──

**ChatGPT Deep Research**- genera múltiples agentes de búsqueda en paralelo, cada uno explorando un ángulo diferente, y luego sintetiza los resultados.

> **ChatGPT Deep Research** Y se produce varios agentes de búsqueda, cada uno explora diferentes ángulos, y luego se componen los resultados.

### El espectro

El multi-agente no es binario, es un espectro:

> Do agente no es de dos. Es una espectral:

El marco del espectro es importante porque la mayoría de los sistemas de producción no están en ninguno de los extremos. Claude Code utiliza subagentes (un nivel de profundidad). Devin utiliza un equipo pequeño.

> El marco de la gama de espectro es importante, ya que la mayoría de los sistemas de producción no están en un extremo.

```
SIMPLE ──────────────────────────────────────────── COMPLEX

 Single        Sub-         Pipeline      Team         Swarm
 Agent         agents

 ┌───┐       ┌───┐        ┌───┐───┐    ┌───┐───┐    ┌─┐┌─┐┌─┐
 │ A │       │ A │        │ A │ B │    │ A │ B │    │ ││ ││ │
 └───┘       └─┬─┘        └───┘─┬─┘    └─┬─┘─┬─┘    └┬┘└┬┘└┬┘
               │                │        │   │       ┌┴──┴──┴┐
             ┌─┴─┐          ┌───┘───┐    │   │       │shared │
             │ a │          │ C │ D │  ┌─┴───┴─┐    │ state │
             └───┘          └───┘───┘  │  msg   │    └───────┘
                                       │  bus   │
 1 loop      Parent +      Stage by    │       │    N peers,
 1 context   child tasks   stage       └───────┘    emergent
                                       Explicit      behavior
                                       roles
```

**Single agent**- Un bucle, un prompt.

> **单 Agent** Un ciclo, un consejo.  Adaptado a una simple tarea.

**Subagents**- un padre da a luz a los hijos para subtareas enfocadas el padre mantiene el plan los niños reportan esto es lo que hace Claude Code

> **子 Agent** Padre Agente 汇报结果── ése es el método de Claude Code──

**Pipeline**- agentes se ejecutan en secuencia. la salida del agente A se convierte en la entrada del agente B. Es bueno para flujos de trabajo en etapas: investigación -> código -> revisión -> prueba.

> **流水线** Agente 顺序运行──Agent A's输出成为 Agent B's输入──适合分阶段的工作流:研究 -> 编码 -> 审阅 -> 测试──

**Team**Los agentes funcionan en paralelo con un bus de mensajes compartidos cada uno tiene un papel un orquestrador coordina es bueno cuando se necesitan diferentes habilidades simultáneamente

> **团队** Agente 通过共享消息总线并行运行──每个人都有角色──编排器协调──适应需要同时使用不同技能的场景──

**Swarm**- muchos agentes idénticos o casi idénticos con estado compartido. sin orquestaje fijo. agentes recogen el trabajo de una cola. bueno para tareas paralelas de alto rendimiento.

> **群体**  许多相同或近似相同的代理共享状态――没有固定的编排器――Agent从队列中获取工作――适合高吞吐量并行任务――

### Los cuatro patrones multi-agentes

#### Modelo 1: oleoductos

```
Input ──▶ Agent A ──▶ Agent B ──▶ Agent C ──▶ Output
          (research)  (code)      (review)
```

Cada agente transforma los datos y los transmite, sencillo de razonar, el fracaso en una etapa bloquea el resto.

> Cada agente transfiere datos y los transmite al siguiente.

Usar cuando: cada etapa tiene una entrada / salida clara y las etapas son naturalmente secuenciales. La investigación → código → revisión → prueba es el ejemplo canónico. Evite cuando: las etapas pueden correr en paralelo o necesitan iteración entre ellas.

> Uso de escenario: cada etapa tiene una clara entrada/salida y la etapa se ejecuta en orden natural.

#### Modelo 2: Descanso / In-fan

```
                ┌──▶ Agent A ──┐
                │              │
Input ──▶ Split ├──▶ Agent B ──├──▶ Merge ──▶ Output
                │              │
                └──▶ Agent C ──┘
```

Dividir el trabajo en agentes paralelos, luego fusionar los resultados.

> Se asignará el trabajo a un agente que se ejecuta en línea, y luego se combinará los resultados.

Utilice cuando: la tarea se divide en piezas independientes (por ejemplo, busque 5 fuentes diferentes, resuma 10 documentos). Evite cuando: las subtareas dependen entre sí o la fusión requiere un razonamiento profundo.

> Uso de escenario: las tareas pueden ser claramente divididas en partes independientes (por ejemplo, buscar 5 diferentes fuentes, en general 10 partes del archivo)

#### Modelo 3: Orquesta-trabajador

```
                    ┌──────────┐
                    │  Orch.   │
                    └──┬───┬───┘
                  task │   │ task
                 ┌─────┘   └─────┐
                 ▼               ▼
           ┌──────────┐   ┌──────────┐
           │ Worker A │   │ Worker B │
           └──────────┘   └──────────┘
```

Un orquestrador inteligente decide qué hacer, delega a los trabajadores y sintetiza los resultados.

> El ordenador inteligente decide qué hacer, envía a la máquina, y genera resultados. El ordenador en sí mismo es un agente de herramientas de generación de la máquina.

Utilice cuando: la tarea es lo suficientemente compleja como para que decidir qué hacer sea un problema difícil.

> Uso de escenario: tareas suficientemente complejas, decidir qué hacer en sí mismo es un problema difícil.

#### Patrón 4: El grupo de compañeros

```
         ┌───┐ ◄──── msg ────▶ ┌───┐
         │ A │                  │ B │
         └─┬─┘                  └─┬─┘
           │                      │
      msg  │    ┌───────────┐     │ msg
           └───▶│  Shared   │◄────┘
                │  State    │
           ┌───▶│  / Queue  │◄────┐
           │    └───────────┘     │
      msg  │                      │ msg
         ┌─┴─┐                  ┌─┴─┐
         │ C │ ◄──── msg ────▶ │ D │
         └───┘                  └───┘
```

No hay orquestaje central, los agentes se comunican entre pares, las decisiones surgen de la interacción, más difícil de deshacer, pero se extiende a muchos agentes.

> 没有编排器中央. 代理之间点对点通信. 决策从交互中涌现. 更难调试. 更多的调试, pero puede extenderse a muchos agentes.

Utilice cuando: muchos agentes homogéneos que realizan un trabajo similar (descarga, clasificación) a escala.

> Uso de escenario: muchos agentes de calidad hacer en gran escala similares trabajos (en inglés)

### Cuando NO utilizar multi-agentes

Cada mensaje entre agentes es un punto de falla potencial. Desarreglar pasa de "leer una conversación" a " rastrear mensajes a través de cinco agentes".

> Cada mensaje entre agentes es un punto de fallo potencial.

**Stay single-agent when:**
- La tarea se ajusta a una ventana de contexto (bajo ~ 100k tokens de datos de trabajo)
  En inglés, "task fit a one up down" se puede decir en inglés "task fit a one up down" (totas de trabajo no superan los 100 mil tokens)
- No necesitas diferentes instrucciones del sistema para diferentes etapas
  Sin embargo, el sistema de la información no necesita una nueva información.
- La ejecución secuencial es lo suficientemente rápida.
  Sin embargo, el proceso de ejecución es muy rápido.
- La tarea es lo suficientemente simple como para que dividirla añade más gastos generales que valor
  Traducción:Tascas suficientemente simples, desglosar aumentó los gastos más que su valor

**The complexity cost:**
- Cada límite de agente es un paso de compresión perdida: el contexto completo del agente A se resume en un mensaje para el agente B
  Traducción: Cada agente 边界都是有损压缩步骤: El texto completo del agente A se resume en el mensaje del agente B
- La lógica de coordinación (quién hace qué, cuándo, en qué orden) es su propia fuente de errores
  Quien hace lo que hace, cuándo lo hace, según lo que ordena) en sí mismo es un error fuente
- Aumenta la latencia: N agentes significa N llamadas de LLM en serie mínimo, más si necesitan hablar de un lado a otro
  China 延迟增加:N 个代理 调用, si es necesario volver a hablar
- Multiplice de costos: cada agente quema tokens de forma independiente
  El costo de cada agente  independiente consumo token

Regla de oro: si una tarea requiere menos de 20 llamadas de herramientas y encaja en 100k tokens, manténla un agente único.

> 經驗法则: Si una tarea sólo necesita menos de 20 veces para utilizar herramientas, y es adecuada para 100k tokens, mantenga un solo agente.

## Construye y realiza.
```figure
swarm-messages
```

## Construye el mismo

### Paso 1: El agente único sobrecargado

Aquí hay un solo agente que intenta hacer todo. Tiene un enorme sistema de respuesta y una ventana de contexto que contiene investigación, código y reseñas:

> Este es un agente único que intenta hacer todo. Tiene una enorme oferta de sistemas y una ventana de análisis de código y revisión.

```typescript
type AgentResult = {
  content: string;
  tokensUsed: number;
  toolCalls: number;
};

async function singleAgentApproach(task: string): Promise<AgentResult> {
  const systemPrompt = `You are a full-stack developer. You must:
1. Research the requirements
2. Write the code
3. Review the code for bugs
4. Write tests
Do ALL of these in a single conversation.`;

  const contextWindow: string[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const research = await fakeLLMCall(systemPrompt, `Research: ${task}`);
  contextWindow.push(research.output);
  totalTokens += research.tokens;
  totalToolCalls += research.calls;

  const code = await fakeLLMCall(
    systemPrompt,
    `Given this research:\n${contextWindow.join("\n")}\n\nNow write code for: ${task}`
  );
  contextWindow.push(code.output);
  totalTokens += code.tokens;
  totalToolCalls += code.calls;

  const review = await fakeLLMCall(
    systemPrompt,
    `Given all previous context:\n${contextWindow.join("\n")}\n\nReview the code.`
  );
  contextWindow.push(review.output);
  totalTokens += review.tokens;
  totalToolCalls += review.calls;

  return {
    content: contextWindow.join("\n---\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

Problemas con este enfoque:
- La ventana de contexto crece con cada etapa.
  La ventana de arriba abajo de la página crece con cada etapa.
- El sistema de instrucción es genérico. No se puede ajustar para cada etapa.
  En inglés, el sistema de sugerencias es de uso general.
- Nada funciona en paralelo.
  No hay ninguna ejecución.

El bucle de un solo agente obliga al LLM a cambiar de contexto entre tareas cognitivas muy diferentes (investigación vs codificación vs revisión) en cada turno.

> 单代理 循环迫使 LLM Cada turno está en tareas de conocimiento muy diferentes 研究 vs 编码 vs 审阅) entre cambios sobre los siguientes.

### Paso 2: Agentes especializados

Ahora lo dividimos.

> Ahora lo desmantelaremos. Cada agente obtiene una misión.

```typescript
type SpecialistAgent = {
  name: string;
  systemPrompt: string;
  run: (input: string) => Promise<AgentResult>;
};

function createSpecialist(name: string, systemPrompt: string): SpecialistAgent {
  return {
    name,
    systemPrompt,
    run: async (input: string) => {
      const result = await fakeLLMCall(systemPrompt, input);
      return {
        content: result.output,
        tokensUsed: result.tokens,
        toolCalls: result.calls,
      };
    },
  };
}

const researcher = createSpecialist(
  "researcher",
  "You are a technical researcher. Read documentation, find patterns, and summarize findings. Output only the facts needed for implementation."
);

const coder = createSpecialist(
  "coder",
  "You are a senior TypeScript developer. Given requirements and research notes, write clean, tested code. Nothing else."
);

const reviewer = createSpecialist(
  "reviewer",
  "You are a code reviewer. Find bugs, security issues, and logic errors. Be specific. Cite line numbers."
);
```

Cada especialista tiene un mensaje enfocado, cada uno tiene una ventana de contexto limpia con sólo la entrada que necesita.

> Cada experto tiene una propuesta enfocada. Cada uno obtiene una ventana de texto arriba abajo limpia, que sólo contiene las entradas necesarias.

El informe del investigador está optimizado para leer y resumir. El informe del codificador está optimizado para escribir código limpio. El informe del revisor está optimizado para encontrar errores. Ningún informe único intenta hacer los tres.

> Los consejos de los investigadores para leer y optimizar el resumen. Los consejos de los editores para escribir código puro para optimizar. Los consejos de los revisores para detectar errores. No hay un solo consejo para intentar hacer estas tres cosas al mismo tiempo.

### Paso 3: Coordinar a través de mensajes

Envía a los especialistas con un mensaje explícito:

> 通过显式消息传递将专家连接起来:

```typescript
type AgentMessage = {
  from: string;
  to: string;
  content: string;
  timestamp: number;
};

async function multiAgentApproach(task: string): Promise<AgentResult> {
  const messages: AgentMessage[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const researchResult = await researcher.run(task);
  messages.push({
    from: "researcher",
    to: "coder",
    content: researchResult.content,
    timestamp: Date.now(),
  });
  totalTokens += researchResult.tokensUsed;
  totalToolCalls += researchResult.toolCalls;

  const coderInput = messages
    .filter((m) => m.to === "coder")
    .map((m) => `[From ${m.from}]: ${m.content}`)
    .join("\n");

  const codeResult = await coder.run(coderInput);
  messages.push({
    from: "coder",
    to: "reviewer",
    content: codeResult.content,
    timestamp: Date.now(),
  });
  totalTokens += codeResult.tokensUsed;
  totalToolCalls += codeResult.toolCalls;

  const reviewerInput = messages
    .filter((m) => m.to === "reviewer")
    .map((m) => `[From ${m.from}]: ${m.content}`)
    .join("\n");

  const reviewResult = await reviewer.run(reviewerInput);
  messages.push({
    from: "reviewer",
    to: "orchestrator",
    content: reviewResult.content,
    timestamp: Date.now(),
  });
  totalTokens += reviewResult.tokensUsed;
  totalToolCalls += reviewResult.toolCalls;

  return {
    content: messages.map((m) => `[${m.from} -> ${m.to}]: ${m.content}`).join("\n\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

Cada agente recibe sólo los mensajes dirigidos a él, sin contaminación de contexto, los 50 mil tokens de lectura de documentación del investigador nunca entran en el contexto del revisor.

> Cada agente sólo recibe sus propios mensajes. No hay contaminación en el archivo.

El objetivo principal es el aislamiento de la información. La ventana de contexto de cada agente está dedicada a su propia tarea. El presupuesto de 200k tokens de un agente no se desperdicia en el trabajo de otros agentes.

> Esta es la ventaja central: información aislada. Cada ventana de texto de cada agente se centra en sus propias tareas. Un agente de 200 mil tokens.

### Paso 4: Compare

```typescript
async function compare() {
  const task = "Build a rate limiter middleware for an Express.js API";

  console.log("=== Single Agent ===");
  const single = await singleAgentApproach(task);
  console.log(`Tokens: ${single.tokensUsed}`);
  console.log(`Tool calls: ${single.toolCalls}`);

  console.log("\n=== Multi-Agent ===");
  const multi = await multiAgentApproach(task);
  console.log(`Tokens: ${multi.tokensUsed}`);
  console.log(`Tool calls: ${multi.toolCalls}`);
}
```

La versión multi-agente utiliza más tokens totales (tres agentes, tres llamadas LLM separadas), pero el contexto de cada agente se mantiene limpio.

> Más agentes  versión utiliza más de un total de tokens (en inglés, "Tre Agent", en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en inglés, en français, en anglais, en anglais, en anglais, en anglais

El comercio es claro: gastar más tokens, obtener mejor rendimiento. Vale la pena cuando la tarea es difícil. No vale la pena para "resumir este párrafo".

> 权衡很清晰:花更多代币,获得更好的输出――任务难时值得――对"总结这一段"不值得――

## Usalo con el marco de ejecución

Esta lección produce una invitación reutilizable para decidir cuándo ir a multi-agente.`outputs/prompt-multi-agent-decision.md`¿ Qué ?

> Este curso ofrece una sugerencia replicable para decidir cuándo utilizar más agentes.`outputs/prompt-multi-agent-decision.md`¿Qué es eso?

El informe de respuesta presenta cuatro preguntas de diagnóstico: (1) ¿necesita la tarea más de 100 mil tokens de contexto de trabajo? (2) ¿necesita experiencia diferente en diferentes etapas? (3) ¿Existe trabajo paralelo? (4) ¿vale la pena la complejidad?

> La sugerencia hace cuatro preguntas de diagnóstico: 1) ¿Se necesita más de 100 mil tokens de trabajo? 2) ¿Se necesita un conocimiento especializado diferente en diferentes fases? 3) ¿Hay trabajo que se pueda realizar? 4) ¿La complejidad vale la pena?

## Los ejercicios.

1. Añadir un cuarto especialista: un agente "tester" que recibe código del codificador y revisa la retroalimentación del revisor, luego escribe pruebas
   China: Add Fourth Expert: a "Testamateur" Agente, recibe el código del codificador y el análisis del revisor, y luego redacta el test
2. Modificar la línea de tubería para que el revisor pueda enviar retroalimentación al codificador para un bucle de revisión (máximo 2 rondas)
   China: Modificar el flujo de agua, para que el revisor pueda enviar el reverso al codificador para realizar el ciclo de modificación (más de 2 radas)
3. Convierta la tubería secuencial en un ventilador: ejecuta el investigador y un agente "analista de requisitos" en paralelo, luego fusione sus salidas antes de pasar al codificador
   China:将顺序流水线转换为扇出:并行运行研究员和"需求分析师"agente, luego juntar sus salidas y reenviarlas al codificador

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Swarm / 群体 | "A hive mind of AI agents" / "AI Agent 的蜂巢思维" | A set of peer agents with shared state and no fixed leader. Behavior emerges from local interactions. / 一组具有共享状态且无固定领导者的对等 Agent。行为从局部交互中涌现。 |
| Orchestrator / 编排器 | "The boss agent" / "老板 Agent" | An agent whose tools include spawning and managing other agents. It plans and delegates but may not do the actual work. / 一个工具包括生成和管理其他 Agent 的 Agent。它规划和委派，但可能不做实际工作。 |
| Coordinator / 协调器 | "The traffic cop" / "交通警察" | A non-agent component (often just code, not an LLM) that routes messages between agents based on rules. / 一个非 Agent 组件（通常只是代码，不是 LLM），根据规则在 Agent 之间路由消息。 |
| Consensus / 共识 | "The agents agree" / "Agent 们达成一致" | A protocol where multiple agents must reach agreement before proceeding. Used when conflicting outputs need resolution. / 多个 Agent 在继续之前必须达成一致的协议。用于需要解决冲突输出的情况。 |
| Emergent behavior / 涌现行为 | "The agents figured it out themselves" / "Agent 自己想出来的" | System-level patterns that arise from agent interactions but were not explicitly programmed. Can be useful or harmful. / 从 Agent 交互中产生但未被明确编程的系统级模式。可能有用也可能有害。 |
| Fan-out / fan-in / 扇出/扇入 | "Map-reduce for agents" / "Agent 的 Map-reduce" | Splitting a task across parallel agents (fan-out), then combining their results (fan-in). / 将任务分配给并行 Agent（扇出），然后合并它们的结果（扇入）。 |
| Message passing / 消息传递 | "Agents talk to each other" / "Agent 之间互相交谈" | The communication mechanism between agents: structured data sent from one agent to another, replacing shared context windows. / Agent 之间的通信机制：从一个 Agent 发送到另一个 Agent 的结构化数据，替代共享上下文窗口。 |

## Más Leer más Leer más

- [The Landscape of Emerging AI Agent Architectures](https://arxiv.org/abs/2409.02977)- estudio de patrones de múltiples agentes
  China 翻译: 新兴 AI Agent 架构概览  多 Agent 模式综述
- [AutoGen: Enabling Next-Gen LLM Applications](https://arxiv.org/abs/2308.08155)- El marco de conversación multiagente de Microsoft
  AutoGen:赋能下一代 LLM 应用  微软的多代理对话框架
- [Claude Code subagents documentation](https://docs.anthropic.com/en/docs/claude-code)- cómo Claude Code delega con la tarea
  中文翻译:Claude Code 子 Agente 文档  Claude Code 如何使用任务委派
- [CrewAI documentation](https://docs.crewai.com/)- marco multiagente basado en el papel
  La organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de las organizaciones de la organización de las organizaciones de la organización de las organizaciones de la organización de las organizaciones de los grupos de los grupos de los grupos de los grupos de los grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos
