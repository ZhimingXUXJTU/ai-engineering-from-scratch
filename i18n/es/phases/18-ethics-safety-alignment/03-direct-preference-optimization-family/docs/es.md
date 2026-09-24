# La familia de optimización de preferencias directas                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

> Rafaelov y otros. (2023) mostró que el óptimo de RLHF tiene una forma cerrada en términos de datos de preferencias, por lo que puede saltarse el modelo de recompensa explícito y optimizar la política directamente. Esa visión dio lugar a una familia  IPO, KTO, SimPO, ORPO, BPO  cada uno fijando un modo de falla de DPO. En 2026, los algoritmos de alineación directa envían más carreras fronterizas después del entrenamiento que PPO. Pero la curva de optimización excesiva de la Lección 2 sigue siendo aplicable: los DAA no escapan de Goodhart, simplemente se mueven donde muerde.

> **【中文解读】**Este episodio presenta el modelo de recompensas de la familia jugar directamente desde el RLHF  sustitución de la formación de datos de preferencias Rafailov  et al. 2023) prueba RLHF                                                                                                                                                                                                                                    

> **【拓展：DPO 家族 → 现代 AI 训练】**En 2026, se implementó un algoritmo de coordinación directo (DAA) en el PPO en más de los entrenamientos posteriores. Pero la curva de optimización excesivamente elevada de la Lección 2 sigue siendo aplicable.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, six-variant preference-loss comparator) | **语言:** Python（标准库，六种变体偏好损失比较器）
**Prerequisites:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (Reward hacking), Phase 10 · 08 (DPO basics) | **前置知识:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (奖励黑客), Phase 10 · 08 (DPO 基础)

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 18·01-02(InstructGPT+古德哈特) 、Fase 10·08(DPO 基础) ⋅DPO Familia = 绕过显式奖励模型直接从偏好数据训练──
> ¿ Qué es esto ?**【类比】**DPO = "eliminar el concurso de jueces"―RLHF = 训练裁判(奖励模型) + 训练选手优化裁判评分;DPO = 直接用比赛结果;;DPO = 直接用比赛结果;;偏好对) entrenamiento选手;;家族变体 IPO/KTO/SimPO/ORPO/BPO 都在修修 DPO 不同缺陷;;2026 DAA(直接对齐算法) 比 PPO 部署更多;;但古德特定法不变只是从"奖励模型过优化"挪到"参考策略比率过度优化"―
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Derivar el formulario cerrado de DPO del RLHF-with-KL óptimo.
  Traducción:De la RLHF de KL con el brazo de la mano.
- Indique el modo de falla de cada una de las correcciones de IPO, KTO, SimPO, ORPO y BPO en DPO.
  En el caso de los DPO, el sistema de pago de los fondos de inversión de los países en desarrollo es el de la empresa.
- Distinguir entre "la brecha implícita de recompensa" y "la fuerza de preferencia" y explicar por qué importa el mapeo de identidad de la OPI.
  China: "La diferencia de recompensa oculta" y "la intensidad preferente", explica por qué la evaluación de la inversión en bolsa es importante.
- Explica por qué Rafailov et al. (NeurIPS 2024) demuestra que los DAA se optimizan demasiado a pesar de no tener RM explícita.
  La versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de

## El problema es la introducción del problema

El objetivo del RLHF (lección 1):

> RLHF 目标(Leyón 1):

```
max_pi E_{x,y~pi} [ r(x, y) ] - beta * KL(pi || pi_ref)
```

tiene un óptimo conocido:

> Hay lo mejor que se sabe:

```
pi*(y|x) = (1/Z(x)) * pi_ref(y|x) * exp(r(x, y) / beta)
```

Así que la recompensa se define implícitamente por la relación entre la política óptima y la referencia:

> Por lo tanto, la proporción de recompensas por el mejor estrategia y la estrategia de referencia se define de forma oculta:

```
r(x, y) = beta * log(pi*(y|x) / pi_ref(y|x)) + beta * log Z(x)
```

Substituir esto en la probabilidad de preferencia Bradley-Terry y la función de partición `Z(x)`cancela porque depende sólo de`x`. Lo que queda es una pérdida en los parámetros de la política solamente  no se necesita un modelo de recompensa.

> Para poner esto en Bradley-Terry  de forma similar, la función de reparto `Z(x)`Porque sólo depende`x`Y抵消── lo que queda es la función de pérdida de los elementos de la pura estrategia no necesita un modelo de recompensa── esto es DPO──

La arrugas: la derivación asume que el óptimo es alcanzable, los datos de preferencias son en distribución y la política de referencia es el anclaje de modo verdadero. Ninguno de estos se mantiene exactamente.

>  El problema consiste en: introducir las hipótesis óptimas  preferencias en la distribución de datos  estrategia de referencia es real  punto  Estas hipótesis en la práctica no se establecen completamente  Cada miembro de la familia modifica diferentes hipótesis de violación 

## El concepto central.

> **【中文解读】**La recomendación de RPO:RLF 目标有已知最优解 pi*((DH y yx) = (1(x)) * pi_ref(y yx) * exp(r((x,y) /beta)  se indicará el premio para el número de parámetros de la mejor estrategia y la proporción de la estrategia de referencia, cede a Bradley-Terry 偏像然, la función de distribución Z(x) porque sólo depende de x y el descuento  restante es la función de pérdida de los parámetros de la estrategia pura, sin necesidad de un modelo de recompensa  pero la recomendación de hipótesis de la mejor estrategia de alcance  la distribución de datos preferencia  dentro de la estrategia de referencia es realmente  puntos  Estas hipótesis no están completamente validas en la práctica.

### DPO (Rafailov y otros, 2023)

```
L_DPO = -log sigmoid(
  beta * log(pi(y_w | x) / pi_ref(y_w | x))
  - beta * log(pi(y_l | x) / pi_ref(y_l | x))
)
```

¿Qué puede salir mal?

> ¿Qué puede ocurrir?

- La brecha implícita de recompensas `beta * (log(pi/pi_ref)_w - log(pi/pi_ref)_l)`Una pequeña preferencia puede producir una brecha arbitrariamente grande.
  China: Hid式奖励差距无限──小偏好可产生任意大的差距──
- El disco de pérdida selecciona y rechaza las pruebas de registro en direcciones opuestas. Puede empujar la prueba de registro absoluta elegida hacia abajo siempre que la rechazada caiga más rápido. Este es el fenómeno de la respuesta elegida degradada.
  China Translation: pérdida de la probabilidad de selección y rechazo de la probabilidad de la cantidad hacia la dirección opuesta. Si la probabilidad de la disminución de la negativa es más rápida, puede reducir la probabilidad de la elección de la cantidad absoluta.
- Las preferencias fuera de distribución (par raro raro vs par raro raro) producen recompensas implícitas arbitrarias.
  La distribución externa prefiere obtener un premio arbitrario.

> **【拓展：IPO → DPO 的边界控制】**IPO(Optimización de preferencias de identidad) sustituye el log-sigmoide por el mapa de恒等, la diferencia de preferencias se encuentra en 1/(2*beta) 封顶. Esto resuelve el problema central del DPO: los pequeños diferenciales de preferencias pueden generar una gran diferencia de recompensa oculta.

### El mercado de la inversión se ha convertido en un mercado de inversión.

La optimización de preferencias de identidad reemplaza el log-sigmoid con un mapeo de identidad en la probabilidad de preferencias. La pérdida se convierte en un error cuadrado en un objetivo limitado:

> El IPO utilizó el tipo de mapeo para reemplazar el log-sigmoide, la diferencia de preferencias fue de 1/(2*beta) 封顶── esto resolvió el problema central del DPO: la diferencia de preferencias de menor tamaño puede generar una diferencia de recompensa oculta de cualquier tamaño──

```
L_IPO = (log(pi(y_w | x) / pi_ref(y_w | x)) - log(pi(y_l | x) / pi_ref(y_l | x)) - 1/(2 beta))^2
```

El margen está limitado por `1/(2 beta)`La fuerza de preferencia y la brecha implícita de recompensa son proporcionales.

> 边界被                   `1/(2 beta)`封顶── preferencia de intensidad y la diferencia de recompensa oculta en la proporción correcta── no explotar──

> **【拓展：KTO → 无配对数据训练】**La innovación clave de la KTO (Kahneman-Tversky Optimization) es abandonar completamente la combinación de estructuras, solo se necesita un solo marcador para la salida de "ideal" o "no ideal". Esto amplió enormemente el alcance de los datos de entrenamiento disponibles.

### KTO (Ethayarajh et al., 2024)

La optimización Kahneman-Tversky elimina completamente la estructura pareja. Dado una salida única etiquetada y una señal binaria "deseable" o "indeseable", se asigna a una utilidad de teoría de prospectos:

> KTO  completamente abandonó la combinación de estructuras ⋅ dado un solo signo de salida y de dos "ideal" o "no ideal" señales, que se proyecta a la perspectiva teoría de la aplicación:

```
v(x, y) = sigma(beta * log(pi(y|x) / pi_ref(y|x)) - z_ref)
```

El beneficio: puede utilizar datos sin pareja, que es mucho más abundante.

> Para los beneficios y pérdidas, el uso de diferentes tipos de pérdidas es un beneficio: puede utilizar datos no comparados, esto es mucho más que comparados con datos ricos.

> **【中文解读】**SimPO removió la estrategia de referencia, sustituyendo la longitud unificación por la comparación de números, además de la gama de gama  estabilidad de entrenamiento. Esto resolvió directamente el modelo de fracaso de la longitud de la DPO  más largo y_w  constructivamente generar una mayor diferencia de probabilidad de números  ORPO  Más intensificado: añadir los proyectos de preferencia a los NLL de la SFT estándar                                                                                                                                                                                                             

### SimPO (Meng et al., 2024)

Optimización de preferencias sencillas alinea la señal de entrenamiento con la generación. Eliminar la política de referencia por completo y normalizar la probabilidad de registro por longitud:

> SimPO va a entrenar señales y generar para la totalidad.

```
L_SimPO = -log sigmoid(
  (beta / |y_w|) * log pi(y_w | x)
  - (beta / |y_l|) * log pi(y_l | x)
  - gamma
)
```

con un margen `gamma`La normalización de longitud elimina el incentivo para explotar el modo de falla de la longitud-bias del DPO (más largo `y_w`da una brecha mayor de registro-prob por construcción).

> Además de la frontera`gamma`稳定训练――长度归结消除了利用DPO 长度偏见失败模式的激励(更长的 长度归结消除了DPO 长度偏见失败模式的激励的使用`y_w`La estructuración produce una mayor diferencia de probabilidad de los números.

### ORPO (Hong et al., 2024)

Optimización de preferencias de probabilidades-ratio añade un término de preferencia a la probabilidad de registro negativo de SFT estándar:

> ORPO aumentará los prefijos a los estándares de SFT 负对数似然上:

```
L_ORPO = L_NLL(y_w) + lambda * L_OR
L_OR = -log sigmoid(log(odds(y_w) / odds(y_l)))
```

No hay política de referencia  el término SFT es el regulador. Entrenamiento en una sola etapa desde el modelo base al modelo alineado. No hay punto de control separado SFT.

> 无参考策略SFT 项就是正则化器──单阶段从基础模型训练到对齐模型──无需单独的SFT 检查点──

### BPO (envía ICLR 2026 OpenReview id=b97EwMUWu7)

Identifica el problema de respuestas elegidas degradadas: DPO conserva el ranking `y_w > y_l`Pero el log-prob absoluto de `y_w`BPO añade una corrección de línea única que penaliza los movimientos hacia abajo en la respuesta elegida.

> BPO 识别了"退化选择响应" problema:DPO 保持 `y_w > y_l`排序但 `y_w`La probabilidad absoluta de que el número de personas se reduzca puede disminuir.

> **【拓展：DAA 过度优化 → 通用防御】**Rafailov 等人(NeurIPS 2024) en varios conjuntos de datos y en el presupuesto de KL  entrenar DPO、IPO、SLiC 策略。 real recompensa con la curva de KL presentándose con la misma forma de adelantamiento y adelantamiento de Gao 等人。 recompensas ocultas de DAA durante el entrenamiento en la búsqueda de muestras de distribución, KL  正则化无法稳定这一点──通用修复更好的数据、集集集、早停对PPO和DPO家族同样适用──

### El resultado universal: los DAA siguen optimizando demasiado

Rafailov et al. "Leyes de escala para la sobreoptimización de modelos de recompensas en algoritmos de alineación directa" (NeurIPS 2024) entrenó políticas con DPO, IPO, SLiC en múltiples conjuntos de datos en los presupuestos de KL. Las curvas oro-recompensa-vs.KL tienen la misma forma Gao et al. Pico y colapso.

> Rafailov  et al. se entrenaron en varios conjuntos de datos y en el presupuesto de KL  DPO、IPO、SLiC  estrategia。 la verdadera recompensa se presenta con la misma curva de KL que Gao  et al. ‖ La forma de subsiguiente recompensa de DAA durante el entrenamiento se encuentra en la búsqueda de muestras distribuidas, KL no puede ser establecida en este punto―

Los DAA no escapan a Goodhart. Cambian la superficie donde se muerde de "modelo de recompensa sobre-optimizado" a "ratio de política de referencia sobre-optimizado".

> DAA no ha escapado de la antigua ley específica. Simplemente van a atacar la superficie de "otimizar excesivamente el modelo de recompensa" a "otimizar excesivamente la tasa de referencia de estrategia".

> **【中文解读】**El método de selección de 2026 años: hay un gran número de parámetros de preferencias datos → DPO(保守 beta) o SimPO((如有长度偏见); hay un poco de preferencias de 2元反 → KTO;想要单阶段管线 → ORPO;DPO 日志显示选择概率下降 → BPO; la intensidad de preferencias cambia mucho y DPO 和 → IPO;; cada laboratorio en todos los métodos se ejecuta de nuevo según las tareas seleccionar la mejor manera de razonamiento matemático y seguridad puede ser diferente.

### Elegir entre ellos (2026)

- Si tiene datos de preferencias en parejas grandes: DPO con beta conservadora, SimPO si es evidente el sesgo de longitud.
  China: tiene un gran número de preferencias en el sistema de datos de la información.
- Si tiene comentarios binarios sin pareja: KTO.
  China: Código de la Unión Europea (CIS)
- Si quieres un oleoducto de una sola etapa de un modelo base: ORPO.
  Querido desde el modelo básico de un solo paso de la línea de conducción → ORPO。
- Si ves registros degradados de registro elegidos en registros de DPO: BPO.
  En el caso de los países de la Unión Soviética, el porcentaje de ingresos por la producción de productos agrícolas en el país se ha reducido a un 50% en el período de transición.
- Si las preferencias varían mucho y el DPO es saturante: IPO.
  Prefijo intensidad variación grande y DPO 和 → IPO。

Cada laboratorio ejecuta los cinco en una batería y elige el ganador por tarea. No hay razón para que el óptimo sea el mismo para el razonamiento matemático y la seguridad.

> Cada laboratorio se ejecuta de manera completa en todos los métodos. No hay razón para pensar que el mejor método para la raciocínio matemática y la seguridad sea el mismo.

> **【拓展：DPO 家族实践 → 方法选择】**En 2026 cada laboratorio de vanguardia se ejecutó en todos los métodos. No hay razón para pensar que el método más eficaz de la raciocinio matemático y la seguridad es el mismo. En el conjunto de datos de los juguetes de variación de intensidad de preferencia, comparamos las seis pérdidas, dibujamos la tasa de victoria final de cada método, la probabilidad de selección de desvío y la distribución de premios oculta.

## Usalo con el marco de ejecución
```figure
dpo-margin
```

## Usalo

`code/main.py`comparar seis pérdidas (DPO, IPO, KTO, SimPO, ORPO, BPO) en un conjunto de datos de preferencias de juguete donde la fuerza de preferencia real varía por pareja. Cada pérdida se optimiza contra la misma muestra de 500 parejas con una pequeña política de softmax.

> `code/main.py`En el conjunto de datos de juguetes de variación de la intensidad de preferencia, comparar seis tipos de pérdidas (DPO,IPO,KTO,SimPO,ORPO,BPO) ⋅ cada tipo de pérdidas en el mismo 500 para la muestra con la optimización de la estrategia de softmax pequeño ⋅ dibujar la tasa de victoria final de cada método ⋅ seleccionar la probabilidad de desvío y la distribución de premios oculta ⋅

## Envíe el producto .

Esta lección produce`outputs/skill-preference-loss-selector.md`. Dadas las estadísticas de los conjuntos de datos (parados vs. sin par, variables vs. preferencias uniformes, distribución de longitud) y un objetivo (estadios individuales o FFT-then-preferencia), recomendamos una pérdida de preferencias e informamos del modo de falla contra el cual protege.

> 本课产 出  `outputs/skill-preference-loss-selector.md` Datos de datos de la estadística de los grupos de datos (parentesco vs no parentesco, variable vs mediano de la intensidad y la longitud de la distribución) y objetivos (por ejemplo, una sola etapa o una SFT-tras-prefixión), recomendando la pérdida de la preferencia y reportando el modelo de fracaso de su protección.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Informar la caída final de registro de prueba elegida para DPO y BPO. BPO debe mantener una probabilidad absoluta elegida más alta  verificar esto.
   Traducción:运行`code/main.py` Reporte de la probabilidad de descenso de la selección final de DPO y BPO.

2. Modificar los datos de preferencias para que todos los pares tengan la misma fuerza. ¿Cuál de los seis métodos es más robusto? ¿Cuál degrada? Explique la ventaja de la OPI aquí.
   Traducción: Modificar los datos de preferencia hace que todos los tipos de datos de preferencia sean comparados.

3. Haga que las respuestas rechazadas sean en promedio 2 veces más largas que las elegidas. Sin cambiar nada más, muestre la explotación de longitud del DPO numéricamente y la corrección del SimPO.
   En el caso de los datos de la información, el número de datos que se muestran en el DPO es de 2 veces.

4. Rafailov et al. (NeurIPS 2024) afirman que los DAA se optimizan demasiado. Reproduce una versión de un solo punto: la divergencia KL de gráfico elegida-menos-rechazada y observa la sobre-optimización en DPO en beta grande.
   La versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de

5. Lea el resumen del documento de BPO (OpenReview b97EwMUWu7).`code/main.py`¿ Qué ?
   En el caso de los BPO, el BPO se ha convertido en un grupo de personas que se han convertido en un grupo de personas.`code/main.py`En el medio de la realización de la confirmación.

## Términos clave .

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| DPO | "RLHF without a reward model" / "没有奖励模型的 RLHF" | Loss derived from the closed-form RLHF optimum; policy parameters only / 从闭式 RLHF 最优解推导的损失；仅策略参数 |
| Implicit reward | "the log-ratio" / "对数比率" | `beta * log(pi(y\|x) / pi_ref(y\|x))` — the DPO-implied reward / DPO 隐含的奖励 |
| IPO | "bounded DPO" / "有界 DPO" | Replaces log-sigmoid with identity; implicit reward gap capped by `1/(2 beta)` / 用恒等映射替换 log-sigmoid；隐式奖励差距被 `1/(2 beta)` 封顶 |
| KTO | "unpaired DPO" / "非配对 DPO" | Prospect-theory utility over single labels with loss aversion / 带损失厌恶的单标签前景理论效用 |
| SimPO | "reference-free DPO" / "无参考 DPO" | Length-normalized log-likelihood + margin; no reference policy / 长度归一化对数似然 + 边际；无参考策略 |
| ORPO | "one-stage DPO" / "单阶段 DPO" | NLL + odds-ratio preference term; trains from base model in one pass / NLL + 胜率比偏好项；单阶段从基础模型训练 |
| BPO | "chosen-preserving DPO" / "保留选择的 DPO" | DPO plus a penalty for decreasing the chosen response's absolute log-prob / DPO 加上降低选择响应绝对对数概率的惩罚 |
| Degraded Chosen | "chosen goes down" / "选择概率下降" | DPO decreases chosen log-prob so long as rejected falls faster / DPO 降低选择对数概率只要拒绝下降更快 |
| DAA | "direct alignment algorithm" / "直接对齐算法" | Any preference-loss method that skips an explicit RM / 任何跳过显式 RM 的偏好损失方法 |

## Más Leer más Leer más

- [Rafailov et al. — Direct Preference Optimization (NeurIPS 2023, arXiv:2305.18290)](https://arxiv.org/abs/2305.18290)
  La historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de los Estados Unidos
- [Azar et al. — A General Theoretical Paradigm to Understand Learning from Human Preferences (AISTATS 2024, arXiv:2310.12036)](https://arxiv.org/abs/2310.12036) OPI
  En inglés: Azar 等人 IPO 论文
- [Ethayarajh et al. — KTO: Model Alignment as Prospect Theoretic Optimization (arXiv:2402.01306)](https://arxiv.org/abs/2402.01306)
  El texto de la ley es el siguiente:
- [Meng, Xia, Chen — SimPO (NeurIPS 2024, arXiv:2405.14734)](https://arxiv.org/abs/2405.14734)
  Sinopsis: El libro de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de los Estados Unidos
- [Hong, Lee, Thorne — ORPO (EMNLP 2024, arXiv:2403.07691)](https://arxiv.org/abs/2403.07691)
  En inglés: Hong 等人 ORPO 论文
- [BPO — Behavior Preservation Optimization (ICLR 2026 OpenReview b97EwMUWu7)](https://openreview.net/forum?id=b97EwMUWu7)
  El comportamiento de BPO 保持优化
- [Rafailov et al. — Scaling Laws for RM Overoptimization in DAAs (NeurIPS 2024, arXiv:2406.02900)](https://arxiv.org/abs/2406.02900)
  La ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de los derechos de
