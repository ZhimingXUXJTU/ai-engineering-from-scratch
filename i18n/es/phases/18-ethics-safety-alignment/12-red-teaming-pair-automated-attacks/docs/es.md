# Red-Teaming: PAIR y ataques automáticos

> El gobierno de China ha adoptado una nueva política de control de la población de la región. PAIR  Rapid Automatic Iterative Refinement  es el jailbreak automático canónico de caja negra. Un LLM atacante con un sistema de red-team prompt propone iterativamente jailbreaks para un LLM objetivo, acumulando intentos y respuestas en su propio historial de chat como retroalimentación en contexto. PAIR suele tener éxito dentro de 20 consultas, órdenes de magnitud más eficientes que GCG (la búsqueda de gradientes a nivel de tokens de Zou et al.) y sin requerir acceso a caja blanca. PAIR es ahora una línea de base estándar en JailbreakBench (arXiv:2404.01318) y HarmBench, junto con GCG, AutoDAN, TAP y Prompt Adversarial Persuasive.

> **【中文解读】**Este capítulo presenta el método de evaluación de seguridad sistematizado de Red Team Testing, con ataques automatizados para descubrir la falla de un sistema AI.

> **【拓展：PAIR → GCG → 攻击家族谱系】**GCG(Zou 等人 2023) en la orden牌级梯度搜索对抗后,需要白盒访问,产生不可读字符串──PAIR 是黑盒的,产生自然语言攻击且可跨模型迁移──AutoDAN 使用进化搜索,TAP 引入分支剪枝,PAP 编码人类说服技术──JailbreakBench(100 有害行为) y HarmBench(510 行为) estándardized evaluation──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, mock PAIR loop against a toy target) | **语言:** Python（标准库，针对玩具目标的模拟 PAIR 循环）
**Prerequisites:** Phase 18 · 01 (instruction-following), Phase 14 (agent engineering) | **前置知识:** Phase 18 · 01 (指令遵循), Phase 14 (Agent 工程)
**Time:** ~75 minutes | **时间:** ~75 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 18·01、Fase 14──PAIR = 自动化黑盒越狱, atacar LLM 代生成越狱 prompt──
> ¿ Qué es esto ?**【类比】**PAIR = "AI automáticamente encuentra la falla"――手工红队 = 人写越狱(慢);PAIR = 攻击 LLM 看目标 LLM 反应,代改进(usualmente 20 查询内成功,比 GCG 快几个数量级)―JailbreakBench/HarmBench 标准基线。

## Objetivos de aprendizaje

- Describa el algoritmo PAIR: el sistema de ataque rápido, la refinamiento iterativo, la retroalimentación en contexto.

> 描述 PAIR 算法: ataqueador sistemas提示、代改进、上下文反──

- Explica por qué PAIR es estrictamente más eficiente que GCG cuando el objetivo es la caja negra.

> Explica por qué PAIR en el objetivo es más estricto que GCG.

- Nombre de otras cuatro líneas de base de ataque automatizado (GCG, AutoDAN, TAP, PAP) y indicar una característica distintiva de cada una.

> 列出其他四种自动化攻击基线 (GCG, AutoDAN,TAP,PAP) y sus características distintivas.

- Describa los protocolos de evaluación de JailbreakBench y HarmBench y qué significa "tipo de éxito de ataque" en cada uno.

> describir el acuerdo de evaluación de JailbreakBench y HarmBench y el significado de sus respectivas "tasas de éxito de ataque".

## El problema es el problema .

El red-teaming solía ser una actividad manual. Un pequeño número de expertos probadores construyeron las instrucciones adversarias y rastrearon las que funcionaron. Esto no se escala: la tasa de éxito del ataque necesita una muestra estadística, y el objetivo es un objetivo en movimiento con cada lanzamiento de un modelo. PAIR operacionaliza el red-teaming como un problema de optimización con un objetivo de caja negra.

> 红队测试过去是手动活动―― un pequeño grupo de expertos que realizan pruebas de resistencia y siguen las ventajas de las pruebas. Esto es inexplicable: la tasa de éxito de los ataques requiere estadísticas de muestras, y los objetivos de cada modelo son variables cuando se publican.

## El concepto.

> **【中文解读】**PAIR  algoritmo de proceso:输入目标 LLM T、评判 LLM J、攻击者 LLM A、目标字符串 G、预算 K(normalmente 20 查询)  ciclo k=1..K:A 根据目标和历史(提示,响应) 对发出新提示 p_k;提交 p_k 到 T 获得响应 r_k;J 评分;如果分数超过值则停止;否则增加到历史继续;;NeurIPS 2023 结果:对 GPT-3.5-turbo 和 Llama-2-7B-chat 攻击成功率 >50%,平均成功查询数在 10-20 范围内.

### Algorithm de la pareja

Las entradas:
- Objetivo LLM T (el modelo que estamos atacando).
- El juez LLM J (ponga si una respuesta es un jailbreak).
- El atacante LLM A (el optimista del equipo rojo).
- La cadena de objetivos G: "responde con [instrucción perjudicial]."
- Presupuesto K (generalmente 20 consultas).

> 输入: objetivo LLM T(我们攻击的模型) 评判 LLM J(评分响应是否越狱) 攻击者 LLM A(红队优化器) 目标字符串 G("用[有害指令]响应") 预算 K(通常20 查询) ⋅

Loop, para k en 1..K:
1. A se incita con el objetivo G y el historial de pares (prompto, respuesta) hasta ahora.
2. Una emite una nueva llamada p_k.
3. Envía p_k a T; recibe respuesta r_k.
4. J marca (p_k, r_k) en el gol.
5. Si el puntaje >= umbral, detenga el jailbreak encontrado.
6. Si no, añadir (p_k, r_k) a la historia de A; continuar.

> 循环 k=1..K:1. A 被提示目标 G 和历史(提示,响应) 对──2. A 发出新提示 p_k──3. 提交 p_k 到 T;接收响应 r_k──4. J 评分(p_k, r_k) ・・・5.

Resultado empírico (NeurIPS 2023): >50% de tasa de éxito de ataque contra GPT-3.5-turbo, Llama-2-7B-chat; consultas promedio de éxito en el rango de 10 a 20.

> 实证结果(NeurIPS 2023): para GPT-3.5-turbo、Llama-2-7B-chat  ataque tasa de éxito > 50%; número de preguntas de éxito promedio en el rango 10-20 ⋅

### Por qué PAIR es eficiente

GCG (Zou et al. 2023) busca los sufijos de tokens adversarios por gradiente; requiere acceso a modelos de caja blanca y produce sufijos ilegibles. PAIR es caja negra y produce ataques de lenguaje natural que se transfieren a través de modelos. La retroalimentación en contexto de PAIR permite que el atacante aprenda de cada rechazo; GCG no tiene equivalente (cada nueva actualización de tokens tiene que redescubrir el progreso anterior).

> GCG 通过梯度搜索对抗性令牌后;需要白盒访问且产生不可读后──PAIR es una caja negra que produce modelos de migración de ataques a la lengua natural──PAIR's 上下文反让攻击者从每次拒中学习; GCG 没有等价机制──

### Ataques automatizados relacionados

- **GCG (Zou et al. 2023, arXiv:2307.15043).**En el nivel de las fichas, se busca los sufijos adversarios.

> **GCG（Zou 等人 2023）。**Se puede mover en un círculo de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la

- **AutoDAN (Liu et al. 2023).**La búsqueda evolutiva de las instrucciones, guiada por un objetivo jerárquico.

> **AutoDAN（Liu 等人 2023）。**进化搜索提示, por la dirección de objetivos de la clasificación.

- **TAP (Mehrotra et al. 2024).**Árbol de ataques con poda  ramas múltiples despliegues de estilo PAIR.

> **TAP（Mehrotra 等人 2024）。**带剪枝的攻击树分支多个 PAIR式推出──

- **PAP (Zeng et al. 2024).**Las Prompts Adversarias Persuasivas codifican las técnicas de persuasión humana como plantillas de prompto.

> **PAP（Zeng 等人 2024）。**La tecnología de la persuasión humana se codifica como un modelo de la persuasión.

> **【拓展：ASR 指标 → 评估陷阱】** Rate de éxito de ataque ASR) debe ser reportado bajo un presupuesto de consulta fijo 90% ASR en 200 consultas y 85% ASR en 20 consultas es incomparable 评判身份也驱动报告 ASRGPT-4-turbo 评判和Llama Guard 评判对同一攻击可能给出不同分数──比较攻击需要匹配预算和指定评判──

### JailbreakBench y HarmBench

Ambas (2024) evaluaciones estandarizadas:

> 两者(2024) estándarizado evaluación:

- JailbreakBench (arXiv:2404.01318). 100 comportamientos dañinos en 10 categorías de políticas de OpenAI. tasa de éxito de ataque (ASR) como la métrica principal. Requiere un juez (GPT-4-turbo, Llama Guard o StrongREJECT).

> El banco de correos: 100 个有害行为,横跨 10 个 OpenAI 政策类别── ataque tasa de éxito(ASR) como indicador principal── necesita un juez──

- HarmBench (Mazeika et al. 2024). 510 comportamientos en 7 categorías, con pruebas de daño semántico y funcional. Compara 18 ataques contra 33 modelos.

> HarmBench:510 个行为,横跨 7 个类别,包含语义和功能性危害测试──比较 18 种攻击对 33 模型──

Los ataques de comparación requieren presupuestos iguales; un ASR del 90% en 200 consultas no es comparable al 85% de ASR en 20.

> Las RAS suelen presentarse bajo un presupuesto de consulta fijo.

> **【中文解读】**2026 años de implementación significado: cada laboratorio de vanguardia ahora está en la publicación anterior a la producción de modelos de funcionamiento PAIR y TAP。ASR 轨迹出现在模型卡(LECCIÓN 26) y casos de seguridad

### Razones por las que importa para las implementaciones de 2026

Cada laboratorio fronterizo ahora ejecuta PAIR y TAP contra modelos de producción antes de su lanzamiento.

> Cada laboratorio de vanguardia está en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad en la actualidad

### Donde esto encaja en la Fase 18

La lección 12 es la base del ataque automatizado. La lección 13 (Many-Shot Jailbreaking) es una explotación complementaria de longitud. La lección 14 (ASCII Art / Visual) es un ataque de codificación. La lección 15 (Injección de Prompt Indirect) es la superficie de ataque de producción de 2026. La lección 16 cubre las contrapartes de herramientas defensivas (Llama Guard, Garak, PyRIT).

> Lección 12 es la base de la automatización de ataques. Lección 13 es el uso de la longitud de la interacción. Lección 14 es el código de ataques. Lección 15 es la producción de ataques de 2026 años.

> **【拓展：TAP 和 PAP → 攻击进化】**TAP(Mehrotra 等人 2024) a través de la división de varios PAIR 式 lanzó并剪枝扩展 PAIR更高 ASR pero更多计算──PAP(Zeng 等人 2024) convertirá la tecnología de persuasión humana en código de sugerencias模板── atacar a la familia desde la búsqueda de la caja blanca de GCG hasta la búsqueda de la caja negra de PAIR, la búsqueda de árboles de TAP y la ingeniería social de la PAP.

## Usalo.
```figure
al-pair-loop
```

## Usalo

`code/main.py`El objetivo es un clasificador falso que rechaza las instrucciones "obvias" dañinas (filtro de palabras clave). El atacante es un refinador basado en reglas que intenta la paráfrase, el marco de juego de roles y la codificación. El juez marca la respuesta. Observas al atacante triunfar en ~5-15 iteraciones contra el filtro de palabras clave y fallar contra un filtro semántico.

> `code/main.py`Construir un ciclo de juego PAIR ⋅ objetivo es rechazar "evidente" sugerencias nocivas ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅    ⋅                                                                                                                                                       

## Envíalo .

Esta lección produce`outputs/skill-attack-audit.md`. Dado que el equipo rojo ha realizado un informe de evaluación, el comité de auditoría revisa: qué ataques se realizaron (PAIR, GCG, TAP, AutoDAN, PAP), con qué presupuesto cada uno, con qué juez, en qué comportamiento perjudicial se estableció (JailbreakBench, HarmBench, interno).

> 本课产 出  `outputs/skill-attack-audit.md` Determinar el informe de evaluación del equipo rojo, la auditoría: qué ataques se han ejecutado, el presupuesto de cada ataque, el juez utilizado, el conjunto de comportamientos nocivos.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`- Medir las medias de preguntas para el éxito de las tres estrategias integradas de atacantes.

2. Implementar una cuarta estrategia de ataque (por ejemplo, traducción a otro idioma, codificación base64).

3. En la Figura 5 (comparación PAIR vs GCG) se describen dos escenarios en los que se prefiere la GCG a pesar de la ventaja de eficiencia de PAIR.

4. JailbreakBench informa ASR contra un conjunto de objetivos fijos. Diseñe una métrica adicional que mide la diversidad de ataque (variación en las instrucciones exitosas). Explica por qué la diversidad es importante para la evaluación de la defensa.

5. TAP (Mehrotra 2024) extiende PAIR con ramificación + poda.`code/main.py`y describir el coste computacional frente a la tasa de éxito.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| PAIR | "automated jailbreak" | Prompt Automatic Iterative Refinement; attacker-LLM + judge-LLM loop |
| GCG | "gradient jailbreak" | White-box token-level gradient search for adversarial suffixes |
| Attack success rate (ASR) | "% jailbreaks at k queries" | Primary metric; must be reported with query budget and judge identity |
| Judge LLM | "the scorer" | LLM that grades whether a response satisfies the harmful goal |
| JailbreakBench | "the evaluation" | Standardized harmful-behaviour set with tagged categories |
| HarmBench | "the broader bench" | 510 behaviours, functional + semantic harm tests |
| TAP | "tree of attacks" | PAIR with branching + pruning; better ASR at higher compute |

## Más Leer más Leer más

- [Chao et al. — Jailbreaking Black Box LLMs in Twenty Queries (arXiv:2310.08419)](https://arxiv.org/abs/2310.08419) Papel de pareja, NeurIPS 2023
- [Zou et al. — Universal and Transferable Adversarial Attacks on Aligned LLMs (arXiv:2307.15043)](https://arxiv.org/abs/2307.15043) Papel de GCG
- [Chao et al. — JailbreakBench (arXiv:2404.01318)](https://arxiv.org/abs/2404.01318) Evaluación estandarizada
- [Mazeika et al. — HarmBench (ICML 2024)](https://arxiv.org/abs/2402.04249) evaluación más amplia
