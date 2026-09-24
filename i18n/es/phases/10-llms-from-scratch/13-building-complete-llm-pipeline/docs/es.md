# Construir un oleoducto completo de LLM Construir una gran línea de conducción

> Todo desde las lecciones 01 a 12 es una etapa de una tubería. Esta lección es el andamio que convierte esas etapas en una sola carrera de extremo a extremo: tokenizar, pre-trein, escala, SFT, alinear, evaluar, cuantizar, servir. No entrenarás a un modelo 70B en una computadora portátil. Producirás la capa de orquestación, el manifiesto, la puerta de evaluación y el plan de retroceso que un equipo fronterizo de 2026 utiliza para decidir qué se envíe. Esta es la piedra angular.

> **【中文解读】**Se trata de un programa de formación de la que se desarrollará una serie de cursos de formación y formación en el campo de la educación y la educación.

> **【拓展：端到端管线→生产实践】**La verdadera gran producción de modelos también incluye: datos version management, experimento seguimiento (W&B) modelos registrados, A/B 测试,回滚计划.

> ¿ Qué es esto ?**【前置】**Esta es la piedra angular de la Fase 10 (la primera fase es la fase 10), requiere que se complete la Fase 10·01-12 全部。本节不教新知识,教你如何把前12节串成一条可运行的管线──

> ¿ Qué es esto ?**【类比】**完整LLM 管线 = 造车流水线. 前面 12 课学了每个工位. 发动机,装底盘,喷漆),本节是工厂设计师把这些工位按顺序串起来,加上"质检门" (por el portal) "",返工通道" (por el rollo) "",生产计划表" (manifest) ⋅你不会亲手制作70B 模型, pero tú escribirás para que el equipo produzca en masa 70B 模型的"造车手册"―

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** All Phase 10 lessons 01-12
**Time:** ~120 minutes

## Objetivos de aprendizaje

- Componer las once lecciones anteriores (tokenizer, datos, pre-entrenamiento, escalado, SFT, RLHF, DPO, CAI, eval, cuantización, inferencia) en una única especificación de tubería reproducible
  Se puede combinar en una sola norma de la línea de tuberías que se pueda repetir.
- Definir el contrato de artefacto entre etapas: lo que consume cada etapa, lo que produce y cómo la siguiente etapa verifica la entrada
  定义阶段间产品契约: cada etapa consume qué, produce qué, siguiente etapa cómo verificar la entrada
- Construir un orquestrador que rastrear experimentos, hashes artefactos, y puertas de envío decisiones en los umbrales de evaluación
  Construir un ordenador, seguir experiencias ̇ hacer productos y evaluar valor  controlando la toma de decisiones
- Diseñar el plan de retroceso: qué artefactos son baratos para volver a usar, cuáles son caros y cuánto cuesta un puesto de control corrupto
  design roll plan: qué productos son baratos, cuáles son caros, cuáles son malos

## El problema es la introducción del problema

Las clases anteriores cada trabajo. Tokenizer entrenado. GPT pequeño pre-entrenado. Datos de SFT ensamblado. Modelo de recompensas entrenado. DPO ejecutado. Evalos medidos. Pesos cuantizados exportados. servidor de inferencia girado. Cada uno es una libreta. Cada uno tiene sus propias convenciones, sus propias vías de salida, su propia semilla.

>  Precedentes cursos cada uno puede trabajar  分词器训练了──迷你 GPT 预训练了── SFT 数据集组装了──奖励模型训练了── DPO 运行了──评估测量了──量化权重导出──推理服务器启动── cada uno es un cuaderno── cada uno tiene su propio destino, su propio camino de salida, su propia semilla──

Una carrera de entrenamiento fronterizo no es un cuaderno. Llama 3 405B tomó 30 millones de horas H100 en aproximadamente 54 días. DeepSeek-V3 usó alrededor de 2,8 millones de horas H800. Durante ese tiempo, un punto de control corrupto, una contaminación de datos, una regresión de evaluación puede costar a un equipo una semana de tiempo y un mes de presupuesto de GPU. La forma en que los equipos sobreviven a esto es a través de la higiene de la tubería: cada etapa tiene una entrada determinista, una salida determinista, un manifiesto, un hash y una puerta.

> La operación de entrenamiento de la primera línea no es un portátil. Llama 3 405B utilizó alrededor de 3000 millones de H100 小时, aproximadamente 54 天. DeepSeek-V3 utilizó alrededor de 280 millones de H800 小时. En este tiempo, un punto de control de deterioro, una contaminación de datos, una evaluación de regreso puede hacer que el equipo pierda una semana de tiempo de espera y un mes de presupuesto de GPU.

Esto es la piedra angular. No se ejecutará la tubería de extremo a extremo en una computadora portátil. Se escribirá el orquestrador que coordina las etapas, el manifiesto que describe la carrera, el verificador que se encarga de las decisiones de navegación, y el plan de repetición que permite a un tercero volver a ejecutar su trabajo desde un solo archivo. El código es pequeño; la disciplina es grande.

> Este es el curso de punta. Usted no estará en el portátil de la línea de ejecución de la línea de ejecución de la línea de ejecución de la línea de coordinación de los ordenadores de cada etapa. Usted escribirá una descripción de la lista de ejecución de la línea de ejecución.

El patrón se extiende desde 100M hasta 1T sin cambios. Los mismos cuatro componentes - manifiesto, orquestrador, puerta de evaluación, almacén de artefactos - ejecutan Llama 3 y también ejecutan su hobby GPT. La diferencia es el tamaño de los números dentro de la configuración de cada etapa, no la forma de la tubería.

## El concepto central.

> **【中文解读】**Este curso va a integrar todos los componentes de la LLM en un completo proceso de formación.

> **【拓展：完整管线的成本估算】** entrenar un modelo Llama 3 de la categoría 70B  costo de la línea de tubería completa: pre-entrenamiento aproximadamente 200-500 millones USD (GPU 时间), SFT aproximadamente 1-50.000 USD (Data tag), RLHF/DPO aproximadamente 5-10 millones USD (Preferencia de datos tag) ;; costo total del pre-entrenamiento fue de 95%+, pero la fase de preparación determinó la utilidad y seguridad del modelo ;;


### Las doce etapas

Cada lección de la Fase 10 es una etapa. Aquí está el gráfico completo de dependencia.

```mermaid
graph TD
    S1["01 Tokenizer vocab"] --> S2["02 Trained tokenizer"]
    S2 --> S3["03 Sharded dataset"]
    S3 --> S4["04 Base model checkpoint"]
    S4 --> S5["05 Scaled training recipe"]
    S5 --> S6["06 SFT checkpoint"]
    S6 --> S7["07 Reward model + PPO policy"]
    S6 --> S8["08 DPO policy"]
    S7 --> S9["09 CAI / GRPO refined policy"]
    S8 --> S9
    S9 --> S10["10 Eval report"]
    S9 --> S11["11 Quantized weights"]
    S11 --> S12["12 Inference server"]
    S10 --> GATE["Ship gate"]
    S12 --> GATE

    style S1 fill:#1a1a2e,stroke:#e94560,color:#fff
    style S4 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style S9 fill:#1a1a2e,stroke:#0f3460,color:#fff
    style GATE fill:#1a1a2e,stroke:#51cf66,color:#fff
```

Las etapas 07 y 08 pueden funcionar en paralelo. Todo lo demás es una dependencia dura. Un cambio en la etapa 02 (tokenizer) invalidará todos los artefactos en la corriente baja. Un cambio en la etapa 10 (eval) invalidará solo la decisión del barco.

> 阶段 07 和 08 可以并行运行──其他都是硬依赖──阶段 02(分词器) de cambios hace que todos los productos abajo se ejecuten──阶段 10(评估) de cambios sólo hace que las decisiones se ejecuten──

### El Manifiesto

Un manifiesto es un archivo único que describe una ejecución completamente lo suficiente como para reproducirla. Nada que el oleoducto produzca debe depender del estado que no está en el manifiesto. Los campos son aburridos y obligatorios.

```
pipeline_version: 1.2.3
seed: 42
git_commit: a1b2c3d4
stages:
  01_tokenizer:
    recipe: bpe_32k
    input_hash: sha256:...
    output_hash: sha256:...
    wall_clock_sec: 3600
    cost_usd: 12
```

El hash de salida de la etapa N es el hash de entrada de la etapa N+1. Cualquier desviación y la tubería se detiene. Así es como se detecta la corrupción de datos temprano. También es cómo un compañero de equipo en un continente diferente verifica que su repetición produjo el mismo artefacto que el tuyo.

En la práctica los equipos utilizan un pequeño esquema YAML más un verificador manifest que difiere de la ejecución exitosa anterior.

### Tipografía de artefactos

La salida de cada etapa es un artefacto tipado, no un manto de directorio, no un picillo, sino un tipo con nombre con un esquema conocido.

| Stage | Artifact Type | Key Fields |
|-------|--------------|-----------|
| 01-02 | Tokenizer | vocab.json, merges.txt, config.json, hash |
| 03 | Dataset | shards[], row count, token count, dedup stats |
| 04-05 | Checkpoint | weights.safetensors, config.json, optimizer state, step count |
| 06 | SFT Model | checkpoint + SFT recipe + data mix |
| 07 | Reward Model | RM checkpoint + preference data hash |
| 08-09 | Policy | checkpoint + reference hash + beta + KL budget consumed |
| 10 | Eval Report | benchmark scores + regression diffs + eval data hash |
| 11 | Quantized Model | quantized weights + calibration data + accuracy delta vs FP16 |
| 12 | Server Spec | endpoint + model hash + config + observability hooks |

La mecanografía evita el modo de falla más común: el uso de una salida de etapa 08 como entrada de etapa 06, el envío de un modelo entrenado por DPO a través del camino SFT.

### La puerta de Eval

El envío no es "la capacitación terminada". El envío es "la capacitación terminada y la puerta de evaluación pasada". La puerta se define antes de que comience la carrera.

```
gates:
  mmlu:      >= baseline + 0.5   # no regression
  humaneval: >= baseline + 1.0
  truthfulqa: >= baseline         # no drop
  safety_refusal_rate: <= 0.05
  kl_from_reference: <= 25.0
  cost_total_usd: <= 50000
```

Cada puerta es un umbral numérico. No hay puertas "parecen buenas". No hay firmas subjetivas. Si cada puerta pasa, el artefacto se marca embarcable. Si alguna puerta falla, la carrera se mantiene en espera de una supervisión explícita por un revisor nombrado, que se registra en el manifiesto.

La mayoría de los desastres se detectan en dos puertas: una puerta de regresión (el nuevo modelo debe ser al menos tan bueno como el anterior en referencia) detecta errores de formación.

### El Orquestrador

Un pequeño código que lee el manifiesto, despacha etapas, rastrea artefactos y detiene cualquier violación de contrato. Esto no es Airflow. Esto no es Kubeflow. Para la higiene de tuberías quieres algo aburrido que has escrito.

El trabajo del orquestrador es estrecho:

1. Resolva el día de la fiesta del manifiesto.
2. Para cada etapa, compruebe si la salida esperada ya existe en el hash correcto (salte si es así).
3. Conduce el escenario, captura el estorbo, mide el reloj de la pared y el costo.
4. Verifique el hash de salida contra el hash de entrada esperado de la etapa descendente.
5. En caso de fallo, escriba un manifiesto parcial con la etapa exacta de fallo y salga no cero.

Eso es 200 líneas de Python.`code/main.py`En esta lección, bajo el capó, el oleoducto real usa`torchrun`o `ray`para ejecutar etapas individuales en grupos, pero el orquestrador mismo funciona en una sola caja.

### El seguimiento de experimentos y el almacenamiento de artefactos

Dos sistemas externos anclan el oleoducto.

**Experiment tracker (wandb, neptune, mlflow).**El rastreador es donde vas cuando necesitas comparar la carrera A con la carrera B tres semanas después. Los equipos casi siempre usan un rastreador alojado para esto. Escribir tu propio tiempo pierde que debería ir al entrenamiento.

**Artifact store (S3, R2, GCS).**Almacenamiento de objetos inmutables para puntos de control, conjuntos de datos, tokenizers, informes de evaluación. los artefactos se dirigen por hash, no por nombre de archivo.`latest.pt`es una pistola de pie;`ckpt-7b-step-20000-sha256:abc123.safetensors`es un contrato.

El orquestrador escribe a ambos, el rastreador es para los humanos que miran mapas, la tienda de artefactos es para la siguiente etapa buscando entradas.

### Costo

Una carrera fronteriza tiene un número de dólar adjunto.

**Pre-run estimate.**A partir del manifiesto, calcular los FLOPs esperados (para la pre-entrenamiento: 6 x parámetros x tokens), las horas esperadas de GPU (FLOPs / rendimiento máximo / utilización), y el costo en dólares a la tasa de alquiler actual.

**In-run tracking.**El reloj de la pared y el costo están registrados en el manifiesto. Después de cada etapa, se verifica el presupuesto restante. Si una etapa se supera, la puerta de la siguiente etapa se evalúa con el nuevo presupuesto restante. No se descubre que se queda sin dinero cuando llama el VC.

El costo reportado de Llama 3 fue $61M. DeepSeek-V3 reported $5.6M para la carrera principal de preentrenamiento. La proporción es principalmente eficiencia de hardware más mezcla de expertos -- pero el costo específico es visible porque ambos equipos lo rastrearon por etapa, no por carrera.

### Reproducibilidad vs. Determinismo

Estos no son los mismos. *Reproducible* significa el mismo manifiesto más el mismo código más la misma infraestructura produce un punto de control con métricas posteriores equivalentes. *Deterministic* significa salida idéntica a bits.

La formación moderna en LLM es reproducible pero no determinista. El orden reducido del entrenamiento distribuido, el no-determinismo del núcleo de GPU (cuBLAS, flash-attn) y el redondeo de precisión mixta se combinan para producir flotadores que difieren en el nivel 1e-5 entre las carreras. Esto está bien para las métricas finales, que no se mueven. Es fatal si se trata de deshacerse de diferencias de nivel de bits. La cura es registrar el hash de entrada de cada etapa, el hash de salida y las métricas de título -- si coinciden, la carrera se "reproduce" incluso si los pesos no son bit-identicos.

```mermaid
graph LR
    M["Manifest v1.2.3"] --> O["Orchestrator"]
    O --> S["Stages 01 → 12"]
    S --> AS["Artifact Store\n(content-addressed)"]
    S --> ET["Experiment Tracker\n(metrics, curves)"]
    AS --> GATE["Eval Gate"]
    ET --> GATE
    GATE -->|pass| SHIP["Ship"]
    GATE -->|fail| ROLL["Rollback plan"]

    style M fill:#1a1a2e,stroke:#0f3460,color:#fff
    style GATE fill:#1a1a2e,stroke:#e94560,color:#fff
    style SHIP fill:#1a1a2e,stroke:#51cf66,color:#fff
    style ROLL fill:#1a1a2e,stroke:#c0392b,color:#fff
```

### Plan de retroceso

Antes de que comience la carrera, escriba lo que sucede en el fracaso de cada etapa.

- **Cheap to re-run**(horas): tokenizer, eval, cuantización, servidor de inferencias.
- **Medium**(días): SFT, DPO, CAI. Mantenga el modelo base; vuelva a ejecutar solo las etapas de alineación.
- **Expensive**El plan de retroceso aquí no es "re-run". Es "utilizar el último buen punto de control y volver a ejecutar las etapas más baratas de abajo con datos revisados".

Debido a que las dependencias de etapa se escriben y se hashan, el orquestrador puede calcular el conjunto de retroceso automáticamente: invalidar la etapa fallida más todos los descendientes. Un fracaso en la etapa 06 (SFT) invalidará 06, 07, 08, 09, 10, 11, 12.

### Recetas de producción observadas en 2026

La mayoría de los equipos fronterizos convergieron en el mismo esqueleto.

- Tokenizer: 128k BPE con fallback de byte. entrenado en una pequeña rebanada multilingüe equilibrada.
- Pre-entrenamiento: 10-20T tokens, principalmente web más código más sintético. Muon o AdamW optimizador. FSDP2 o DeepSpeed ZeRO-3.
- SFT: pares de instrucciones 500k-2M, humanos y sintéticos mezclados, con una reducción estricta en relación con el conjunto de eval.
- Alineación: DPO o CAI + GRPO. RLHF sólo cuando la señal de preferencia es demasiado multidimensional para DPO.
- Eval: MMLU-Pro, MATH, HumanEval+, GPQA, SWE-Bench Verified, LiveBench, más un conjunto privado que el público nunca ve.
- Cuantificación: GPTQ o AWQ de 4 bits para servir, evaluaciones de seguridad de 8 bits donde la precisión es importante.
- Servir: vLLM, TensorRT-LLM, o en casa. Batchamiento continuo. Descifrado especulativo.

Los números cambian cada seis meses.

```figure
beam-search
```

## Construye el mismo

> **【拓展：训练管线的工程挑战】** Completo LLM  entrenamiento de la línea de los desafíos de ingeniería incluyen: inspección de puntos de gestión                                                                                                                                                                                                                                                 


## Construye y realiza.

El código de la lección es un orquestrador y un controlador de manifiesto, no doce guiones de entrenamiento. Cada etapa se simula con un marcador de lugar que produce un artefacto de salida con la forma y el hash correctos.

> Este código de clase es un ordenador y un revisor de orden, no 12 guiones de entrenamiento. Cada etapa utiliza un modelo de posición, produce un producto de salida de forma correcta y de forma precisa.

El oleoducto en `main.py`Se puede usar un sistema de evaluación para mostrar cómo se ve una carrera realizada. cambiar cada sistema de clasificación por el guión de entrenamiento real de la lección correspondiente y tienes el esqueleto que usa una línea de frontera real.

> `main.py`El ejecutivo central de la tubería tiene 12 fases de ocupación, produce un listado, y prueba una evaluación fallida de los controles para mostrar lo que es el ejecutivo suspendido.

## Usalo con el marco de ejecución

El flujo de trabajo canónico tiene tres comandos.

> El trabajo estándar tiene tres órdenes.

- ¿ Qué ?`plan`La mayoría de los errores de tubería aparecen a tiempo, los umbrales faltantes de puertas, hashes obsoletos, sobrepasos presupuestarios.`plan`Es libre.`run`ahorra dinero capturando insectos en el lado barato.

> Cada vez que lo hace .`plan` La falta de control de los flujos de la línea en el plan se produce en el tiempo de ejecución.`plan`免费──运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `run`Precioso. En un lado, barato.

La producción de `gate`es cualquiera `SHIP`o `HOLD: <reason>`Una carrera realizada no es un fracaso; es un punto de decisión. Un revisor nombrado o anula (y se registra la anulación) o aprueba la retirada.

> `gate`de la salida es `SHIP`O `HOLD: <reason>` La ejecución suspendida no es un fracaso; es un punto de decisión.

## Envíe el producto .

Esta lección produce`outputs/skill-llm-pipeline-reviewer.md`. Le proporcione un manifiesto de la línea de tuberías y revisa todos los contratos: tipografía de etapas, cadena de hash, puertas, plan de retroceso, estimación de costes.

> 本课产 出  `outputs/skill-llm-pipeline-reviewer.md` Rechazará el listado de las líneas de tubería de su propuesta de entrada, revisará todos los contratos: tipo de fase, cadena de acceso, control de puertas, plan de desplazamiento, estimación de costes, rechazará la aprobación de la lista de la falta de evaluación de puertas de control, presupuesto ilimitado de KL o datos de evaluación y entrenamiento mixtos.

## Los ejercicios.

1. Extenda el orquestrador para que se ejecute en paralelo las etapas 07 y 08.`concurrent.futures`Confirmar el registro final del manifiesto de las salidas de ambas etapas y que el hash de entrada de la etapa 09 es una combinación determinista de ambas.
   China: 扩展编排器支持阶段 07 和 08 的并行执行──使用标准库 `concurrent.futures`模块── confirmar el registro final de las dos fases de salida, y la entrada de la etapa 09 哈希是两者的确定性组合──

2. Añadir una puerta de control de contaminación. Dado el hash del conjunto de datos eval y los fragmentos del conjunto de datos de entrenamiento, calcular la superposición (combinación exacta de cadenas o coincidencia de 13 gramos). La puerta falla si la superposición supera el 0,1%.
   China 翻译: 添加"污染检查"门控──给定评估数据集哈希和训练数据集分片,计算重叠(精确字符串匹配或13克匹配)──重叠超过0.1% 则门控失败──进入被污染的训练集并确认门控挂起运行──

3. Implemente un estimador de costos desde los primeros principios. Para la etapa 04 (pre-entrenamiento), estimar FLOPs como 6 x parámetros x tokens, asumir 40% MFU (utilización de FLOPs modelo) en H100 a 989 TFLOPs BF16, a $2.50/GPU-hora. Informar la estimación para un modelo 7B entrenado en tokens 2T. Comparar con los números publicados Llama 2.
   China Translation: From第一性原理实现成本估算器──对于阶段 04(预训), estimar FLOPs 为 6 x 参数 x token,假设 H100 上 40% MFU(模型算力利用率),989 TFLOPS BF16,$2.50/GPU-小时──报告 7B 模型在 2T token 上训练的估算──与已发表的 Llama 2 数据比较──

4. Construir un retroceso parcial. Simula un fallo en la etapa 09 (CAI), luego volver a ejecutar las etapas 09 a 12 dejando 01-08 almacenado en caché. El orquestrador debe detectar los artefactos almacenados en caché mediante hash y saltarlos. Medir el reloj de pared guardado en comparación con la re-ejecución completa.
   La estructura de los sistemas de ordenadores de la máquina de ordenadores de la máquina de ordenadores de la máquina de ordenadores de la máquina de ordenadores de la máquina de ordenadores de la máquina de ordenadores de la máquina de ordenadores de la máquina de ordenadores de la máquina de ordenadores de la máquina de ordenadores de la máquina de ordenadores de la máquina de ordenadores de la máquina de ordenadores de ordenadores de la máquina de ordenadores de ordenadores de la máquina de ordenadores de ordenadores de la máquina de ordenadores de ordenadores de la máquina de ordenadores de ordenadores de ordenadores de la máquina de ordenadores de ordenadores de ordenadores de la máquina de ordenadores de ordenadores de ordenadores de ordenadores de la máquina de ordenadores de ordenadores de ordenadores de ordenadores de ordenadores de la máquina de ordenadores de ordenadores de ordenadores de ordenadores de ordenadores de ordenadores de la máquina de ordenadores de ordenadores de ordenadores de ordenadores de ordenadores de la máquina de ordenadores de ordenadores de ordenadores de ordenadores de ordenadores de la máquina de ordenadores de ordenadores de ordenadores de ordenadores de ordenadores de la máquina de la máquina de ordenadores de ordenadores de ordenadores de ordenadores de ordenadores de ordenadores de ordenadores de la máquina de la máquina de la máquina de la máquina de la máquina de ordenadores de ordenadores de ordenadores de ordenadores de ordenadores de ordenadores de ordenadores de ordenadores de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los cuentas de los

5. Añadir observabilidad. Emite extensiones de OpenTelemetry para cada etapa, con atributos para parámetros, tokens vistos, pérdida y costo. Pipe las extensiones a un coleccionista local. El punto no son tablas de control; el punto es que la salud de cada etapa se puede rastrear a partir de un solo ID de rastro.
   China Translation: Add可观测性── para cada etapa de la transmisión de OpenTelemetry span,带参数、已见代币、损失和成本属性── será el período de la transmisión de los tubos a los locales de recogida──重点不是 el cuadro de instrumentos;重点是每阶段的健康可从单个追踪ID 追踪──

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Manifest | "The recipe file" | YAML or JSON describing pipeline version, seed, per-stage config, and gate thresholds — sufficient to replay a run | 清单文件，描述管线版本、种子和每阶段配置 |
| Content-addressed | "By hash not name" | Artifacts stored by SHA-256 of their contents, so you can never confuse version A with version B | 内容寻址，按 SHA-256 哈希存储产物 |
| Eval gate | "The ship criteria" | Numeric thresholds on benchmark metrics and safety scores that must pass before an artifact is marked shippable | 评估门控，基准和安全分数必须达标才能发布 |
| KL budget | "How far alignment drifted" | A cap on cumulative KL(policy || reference) across alignment stages, enforced as a gate | KL 预算，对齐阶段累计 KL 散度的上限 |
| MFU | "How much of the GPU you used" | Model FLOPs Utilization — achieved FLOPs divided by theoretical peak. 40% is typical at 70B scale, 55% at 7B | 模型算力利用率，实际 FLOPs / 理论峰值 |
| Rollback plan | "What we do when it breaks" | Pre-written set of actions per stage on failure: re-run, fall back, retrain with revised inputs | 回滚计划，每个阶段失败时的预设行动方案 |
| Orchestrator | "The conductor" | The process that reads the manifest, dispatches stages, verifies hashes, halts on any contract violation | 编排器，读取清单、调度阶段、验证哈希 |
| Artifact store | "Versioned S3 for weights" | Immutable content-addressed object store — single source of truth for checkpoints, datasets, eval reports | 产物存储，不可变的内容寻址对象存储 |
| Reproducible | "Same metrics on replay" | Different bit-level weights but equivalent downstream metrics — the realistic target for distributed LLM training | 可复现，重跑时指标等价（权重可能不同） |
| Cost gate | "You cannot exceed X" | Pre-run cost estimate plus in-run tracker — the pipeline refuses to start if the estimate exceeds budget | 成本门控，预估超预算则拒绝启动 |

## Más Leer más Leer más

- [Dubey et al., 2024 -- "The Llama 3 Herd of Models"](https://arxiv.org/abs/2407.21783)-- la descripción pública más detallada de una línea de transporte fronteriza, incluidos los datos, la formación, la alineación, la evaluación
- [DeepSeek-AI, 2024 -- "DeepSeek-V3 Technical Report"](https://arxiv.org/abs/2412.19437)-- la primera línea de producción de eficiencia en aproximadamente 1/10 del coste de la formación de la clase Llama 3
- [Kaplan et al., 2020 -- "Scaling Laws for Neural Language Models"](https://arxiv.org/abs/2001.08361)-- la relación de escalación original computación-datos-parámetros
- [Hoffmann et al., 2022 -- "Training Compute-Optimal Large Language Models (Chinchilla)"](https://arxiv.org/abs/2203.15556)-- la corrección a Kaplan que recalibró los presupuestos de datos modernos
- [PyTorch FSDP2 documentation](https://pytorch.org/docs/stable/fsdp.html)-- el primitivo de formación distribuida que sustituye a FSDP1 en PyTorch 2.4+
- [Weights & Biases LLM Reports](https://wandb.ai/site/llms)-- manifiestos reales y resultados de experimentación para carreras de LLM de código abierto, útiles como plantillas plagiátiles
