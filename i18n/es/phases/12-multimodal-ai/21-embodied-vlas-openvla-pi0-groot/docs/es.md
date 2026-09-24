# VLAs incorporados: RT-2, OpenVLA, π0, GR00T 具身 VLA: visión-linguística-movimiento modelo y control de máquinas

> La primera vez que un modelo leyó una receta de un sitio web y la ejecutó en un robot de cocina fue RT-2 (Google DeepMind, julio 2023). RT-2 discretizó las acciones como tokens de texto, co-finó un VLM en datos web más datos de acción de robots, y demostró que el conocimiento del lenguaje de visión a escala web se transfiere al control robótico. OpenVLA (junio 2024) envió la referencia abierta 7B. La serie π0 de la Inteligencia Física (2024-2025) añadió expertos en acción de coincidencia de flujo. El GR00T N1 de NVIDIA (marzo 2025) entregó control de doble sistema (Sistema 1 / Sistema 2) para robots humanoides a escala. El VLA primitivo  visión-linguego-acción, un solo modelo que ve, lee y actúa  es el puente entre los modelos de comprensión de esta fase y los sistemas autónomos en la Fase 15.

> **【中文解读】**RT-2  Primera prueba de conocimiento de lenguaje visual de nivel de red se puede transferir al control de máquinas:将关节动作分散化为文本代币,与VLM 联合微调――OpenVLA es open source 7B 参考,π0 引入流匹配动作专家,GR00T N1 实现双系统(快思考/慢思考)

> **【拓展：Embodied VLA 到机器人产业】**El modelo de VLA está pasando de laboratorio hacia la industria: Tesla Optimus, Figura 01  1X Tecnologías  etcétera de máquinas están en desarrollo de sistemas de control basados en VLA. En el escenario industrial, VLA se puede utilizar en máquinas de almacenamiento de materiales, máquinas de montaje, etc. El reto central es la seguridad y la fiabilidad.

**Type:** Learn
**Languages:** Python (stdlib, action tokenizer + VLA inference skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 15 (Autonomous Systems, referenced)
**Time:** ~180 minutes

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·05(LLaVA VLM 基础) Fase 15·01(Agencia 循环) 控制理论基础(关节空间、末端执行器位姿) VLA = VLM 输出从文本变成机器人动作,是Fase 12到Fase 15(自主系统) 的桥梁──
> ¿ Qué es esto ?**【类比】**VLA = " darle a los robots un cerebro y un ojo "― Tradicional 机器人 = 程序员写死 if-else 规则(see红色就停下); VLA = 像人看图说话做事("把红杯放到桌上"→看杯→规划路径→控制关节执行)―RT-2 Colocar la movimiento despropiado en token = Colocar la movimiento en texto escrito en un prompt;π0 流匹配 = 输出连续动作而非离散 token, más preciso―

## Objetivos de aprendizaje

- Describa la tokenización de acciones: codificación discreta en bin (RT-2), tokens de acción eficientes FAST, acciones de coincidencia de flujo continua (π0).
  En el texto original, el nombre de la palabra "R" se encuentra en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de la palabra "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el nombre de "R" en el "R" en el "R" en el "R" en el "R" en el "R" en el "R" en el "R" en el "R" en el "R" en el "R" en el "R" en el "R" en el "R" en el "R" en el "R"
- Explicar por qué la coordinación de datos en la web + robots preserva la transferencia de conocimientos generales a tareas nuevas.
  China Translation: explica por qué en la red + de datos de los robots se puede mantener el conocimiento general de la capacidad de la migración a nuevas tareas.
- Comparar OpenVLA (abriendo 7B Llama+VLM), π0 (combinación de flujo) y GR00T N1 (sistema dual) en la misma tarea del robot.
  En español traducción: en el mismo ordenador en la misma misión comparar OpenVLA (OpenVLA) (en inglés)
- Nombre del conjunto de datos Open X-Embodiment y su papel como cuerpo de formación RT-X.
  En el contexto de la formación de la lengua, el lenguaje de la lengua se utiliza para la formación de la lengua.

## El problema es la introducción del problema

Un robot que hace tareas a partir de instrucciones de lenguaje natural ha sido un objetivo de investigación desde la década de 1970. La respuesta de 2020: un modelo de acción de lenguaje de visión (VLA). La misma arquitectura de VLM utilizada para VQA, pero la salida son acciones (tornos conjuntos, poses de efecto final, comandos discretos) en lugar de texto.

> Usando la instrucción de lenguaje natural para hacer que los robots hagan negocios desde 1970 es el objetivo de la investigación.

Desafíos específicos de las VLA:

> Desafíos especiales de VLA:

1. Los espacios de acción son continuos (ángulos conjuntos, fuerzas) y de alta dimensión (7 brazos DOF + agarre 3-DOF = 10 dimes a 30 Hz).
   El espacio es un espacio de la libertad.
2. Los datos de entrenamiento específicos de los robots son escasos. Open X-Embodiment tiene ~ 1M trayectorias; imagen de texto web es 5B +.
   China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
3. La frecuencia de control es importante. El circuito de control de 30 Hz significa un presupuesto de 33 ms por acción.
   Control Frequency es importante. 30Hz  control回路 significa cada movimiento 33ms  presupuesto.
4. Una acción incorrecta daña el hardware, los seres humanos o la propiedad.
   China 译文:安全性. 误会动作损坏硬件. 损害人员或财产.

## El concepto central.

> **【中文解读】**具體視覺-語言-動作模型 (VLA) 让机器人理解语言指令和視覺场景后执行物理动作──OpenVLA es la fuente abierta de VLA, pi0(Inteligencia Física) y NVIDIA Groot es el modelo representativo de la inteligencia física──VLA = 视觉编码器 + LLM + 动作解码器──

> **【拓展：具身智能的进展**OpenVLA-7B en Google Robot logra alrededor del 80% de la tasa de éxito de tareas. Pi0 utiliza flujo de coincidencia (flow matching) para generar trayectorias continuas de movimientos, más suaves que las tradicionales. NVIDIA Groot se dedica a los robots humanos. El reto central de la inteligencia es la escasez de datos.


### Tokenización de acciones (RT-2)

El truco de RT-2: representar cada objetivo conjunto como un token de texto cuantizado. Discrete el rango normalizado [-1, 1] en 256 contenedores, mapa cada contenedor a un ID de vocabulario. Una acción de 10 DOF se convierte en 10 tokens en cada paso de control.

> Las técnicas de RT-2:将每个关节目标表示为量化文本代币――将归结化的 [-1, 1] 范围离散化为 256 个单元, cada单元 映射到一个词汇 ID──10 自由度动作在每个控制步转变成 10 个单元──

Co-fine-tune un VLM PaLM-X en una mezcla:

> En datos mezclados en conjunto, el PaLM-X VLM:

- Parejas de imágenes web y texto (capcionado, VQA).
  La traducción de la página web es:
- Demonstraciones de robots, acción como tokens.
  En el caso de los ejemplos de la lengua inglesa, el nombre de la lengua se puede añadir a la lengua inglesa.

El modelo ve "recoger el cubo rojo" (lenguaje) → imagen (visión) → secuencia de acción de 10 tokens (objetivos conjuntos discretados). El entrenamiento previo a la web preserva la transferencia de conocimiento general: RT-2 puede seguir "moverse hacia el objeto en movimiento rápido" aunque "moverse rápido" no está en los datos de entrenamiento.

> 模型看"拿起红色方块" (en inglés) 图像 (en inglés) 视觉 (en inglés) 图像 (en inglés) 视觉 (en inglés) 图像 (en inglés) 视觉 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像) 图像 (en inglés) 图像 (en inglés) 图像 (en inglés) 图像) 图像 (en inglés) 图像 (en inglés) 图像 (en)) 图) 图) 图) 图) 图) 图) 图) 图 (en inglés) 图) 图) 图 (en inglés) 图) 图) 图 (en inglés) 图) 图 (en inglés) 图) 图 (en inglés) 网 (en inglés) 网 (en inglés)                                                                                                                        

Inferencia a 3-5 Hz en el papel RT-2, limitada por el decodificación autorregresista VLM.

> RT-2 论文中推理速度 3-5 Hz, limitado a VLM 自归解码──

### OpenVLA  la referencia abierta 7B

OpenVLA (Kim et al., junio 2024) es el equivalente RT-2 de peso abierto. 7B Llama backbone, DINOv2 + SigLIP doble codificador de visión, tokenización de acción en 256 contenedores.

> OpenVLA es un programa de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programación de programa de programa de programación de programa de programa de programación de programación de programación de programa de programación de programa de programa de programa de programación de programación de programa de programa de programa de programación de programa de programa de programa de programa de programa de programa de programa de programa de programa de programa de programa de

Entrenado en Open X-Embodiment (970k trayectorias en 22 robots).

> En el Open X-Embodiment 上训练(22 个机器人共 97万条轨迹) ・内置 LoRA 微调支持,适配新机器人──

Inferencia: 4-5 Hz en un A100 con cuantización. Lo suficientemente rápido para la manipulación lenta, no para el control de alta frecuencia.

> 推理:A100 上量化后 4-5 Hz──对慢速操作足够,不适合高频控制──

### FAST tokenizer  más rápido de decodificación de la acción

Pertsch et al. (2024) mostró que la tokenización discreta bin es ineficiente  la mayoría de las acciones se agrupan en una pequeña región de espacio bin. FAST (Tokenizer de secuencia de acción en dominio de frecuencia) comprime las secuencias de acción a través de DCT y cuantifica los coeficientes.

> Pertsch 等人(2024) indican que la dispersión binaria de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la actividad de la sociedad de la sociedad de la sociedad de la sociedad.

Una trayectoria de acción de 30 pasos se convierte en ~ 10 tokens FAST en lugar de 300 tokens discretos.

> 30 pasos de trayectoria se convirtieron en 10 tokens FAST, en lugar de 300 tokens separados de los binos.

### π0 y acciones de coincidencia de flujo

El π0 de la Inteligencia Física (Black et al., octubre 2024) reemplaza a los tokens de acción discretos con un experto en acción de coincidencia de flujo:

> Inteligencia física π0 Us流匹配动作专家替代离散动作代币:

- Un pequeño transformador de acción lee los estados ocultos del VLM y emite una secuencia de acción continua de 50 pasos a través de un flujo rectificado.
  Transformer 读取 VLM 隐藏状态, 通过正流输出连续的50 步动作序列──
- El tren de la cabeza de acción con pérdida de coincidencia de flujo; el VLM preentrenamiento permanece sin cambios.
  China 预训练不变── 动作头用流匹配损失训练; VLM 预训练不变──
- Inferencia: secuencia de acción completa emitida en ~5 pasos de denotación, control efectivo de 50 Hz.
  La serie de movimientos completos está en unos 5 pasos en el ruido de salida, igual efecto 50Hz 控制。

La fórmula de acción continua conserva la suavidad que la discretization destruye.

> π0  afirmación: en una amplia misión operativa derrotar OpenVLA y Octo.

> **【中文解读】**π0 Usando flujo para hacer un cambio de movimiento de desagregación: un pequeño movimiento Transformer 读取 VLM 隐藏状态, 通过正流输出连续的50 步动序列──推理时只需约5步去噪声,实现效率等效50Hz 控制频率──连续动作表达保留了离散会破坏的动作平滑性──

π0.5 y π0-FAST son mejoras incrementales. π0-FAST combina la tokenización de FAST con la coincidencia de flujo.

> π0.5 y π0-FAST es el aumento de la escalación.

### GR00T N1  Sistema dual para humanoides

El GR00T N1 de NVIDIA (marzo 2025) se construye para robots humanoides (> 30 DOF, cuerpo completo):

> GR00T N1 de NVIDIA para diseño de máquinas en forma humana:

- Sistema 2: una gran escena de lectura + instrucción de VLM, que produce subobjetivos de alto nivel a ~ 1 Hz.
  En el caso de los grandes VLM, el sistema de VLM es un sistema de VLM.
- Sistema 1: un pequeño transformador de cabeza de acción que produce comandos conjuntos de bajo nivel de 50-100 Hz condicionados a los subobjetivos.
  En inglés, el sistema de transformación de la cabeza de movimiento pequeño es el sistema de transformación de la cabeza de movimiento de la cabeza de la cabeza de la cabeza de la cabeza de la cabeza.

Los mapas divididos para el pensamiento rápido y lento de Kahneman: los planes del sistema 2, el sistema 1 actúa.

> Este tipo de separación se refleja en el pensamiento rápido de Carniman: sistema 2 规划, sistema 1 执行―― ventajas:

GR00T N1.7 (finales 2025) mejora la escalación de datos. GR00T sintoniza con datos sim-to-real de Omniverse.

> GR00T N1.7 ((2025 años de final) ha mejorado la expansión de datos.

### Cuadro de la X abierto

Los datos de la capacitación. RT-X (octubre 2023) reunió 22 conjuntos de datos que cubren 1M trayectorias en 22 robots. Open X-Embodiment es el corpus que todos utilizan:

> 训练数据──RT-X(2023 年 10 月) ha integrado 22 conjuntos de datos, que cubren 100 000 条轨迹 de 22 机器人──Open X-Embodiment es el lenguaje que todos utilizan:

- ALOHA / Puente V2 / Droid / RT-2 Cocina / Mesa de idiomas.
  El lenguaje de la mesa es el idioma de la cocina.
- Cada muestra: (estado del robot, visualización de la cámara, instrucción, secuencia de acción).
  En el caso de los sistemas de control de datos, el sistema de control de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de
- Higiene de entrenamiento: unificar el espacio de acción, normalizar los rangos articulares, cambiar el tamaño de las cámaras.
  La definición de la definición de un espacio de trabajo es la definición de un espacio de trabajo.

OpenVLA y π0 se entrenan en Open X-Embodiment. La brecha de dominio para cualquier robot específico se cierra mediante el ajuste fino de LoRA en 100-1000 demostraciones específicas de tareas.

> OpenVLA y π0 en Open X-Embodiment en el entrenamiento.

### Co-ajuste fino vs solo robot

La co-ajuste de la calidad mezcla datos de VQA web con trayectorias de robots. La relación importa: demasiado VQA y el modelo olvida las acciones; demasiado datos de robots y el modelo pierde el conocimiento general.

> 联合微调将网页 VQA 数据与机器人轨迹混合──比例很重要: VQA 太多模型忘记动作;机器人数据太多模型失去通用知识──

Ratio de RT-2: ~1:1. OpenVLA: ~0.5:1 web-to-robot. π0: similar. La relación precisa es un hiperparámetro para sintonizar por tamaño de conjunto de datos.

> La proporción de RT-2 es de aproximadamente 1:1──OpenVLA 约 0.5:1──π0 类似──精确比例是按数据集大小调节的超参数──

El entrenamiento solo para robots produce modelos específicos de tareas que fallan en las instrucciones fuera de distribución. La co-finación es la diferencia entre "recoger el cubo rojo (en demostración) " y "recoger el tercer objeto más grande desde la izquierda (fraseo novedoso). "

>                                                                                                                                                                                                                                                               

### Limitos de seguridad y acción

Cada VLA de producción se embarca con:

> Cada VLA de producción está equipado:

- Los límites de articulación dura (no pueden superar el par de especificación).
  En el caso de los grupos de la estructura, el sistema de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura.
- Limitos de velocidad (clicado blando).
  En inglés, el nombre de la línea de trabajo es "Castor".
- Limitaciones del espacio de trabajo (el factor final no puede salir de la mesa).
  El ejecutor de la oficina de trabajo no puede salir de la mesa.
- Aplicación de un sistema de gestión de la información.
  China: nueva misión de la labor de la gente.

Estos se sientan fuera del VLA como controles de capa de control. La salida del VLA es una sugerencia, no un comando.

> Estas están situadas fuera de VLA  controles de control .

## Usalo con el marco de ejecución
```figure
mm-action-tokens
```

## Usalo

`code/main.py`¿Qué es esto ?

- Implementa la tokenización y destokenización de acciones de 256 bin.
  Traducción: "Implementar 256 bin 动作分词化和反分词化"
- Esboza un tokenizador FAST basado en la cuantización DCT +.
  La traducción de la lengua inglesa es:
- Compara el número de tokens por paso de acción (discrete-bin, FAST, flujo continuo).
  En español, el nombre de la persona que se encuentra en el mapa es el nombre de la persona que se encuentra en el mapa.
- Imprime un resumen de la línea de RT-2 → OpenVLA → π0 → GR00T.
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión

## Envíe el producto .

Esta lección produce`outputs/skill-vla-action-format-picker.md`. Dado que se realiza una tarea de robot (manipulación, navegación, cuerpo humanoide completo), se escoge entre bin discreto + RT-2, FAST + OpenVLA, flujo de coincidencia + π0, o sistema dual + GR00T.

> 本课产 出  `outputs/skill-vla-action-format-picker.md`△ dado a los equipos de trabajo (操作、导航、人形全身), en el caso de los equipos de trabajo (Rt-2、FAST+OpenVLA、流匹配+π0 o dos sistemas+GR00T 之间选择──

## Los ejercicios.

1. Un brazo de 10 DOF a 30 Hz de velocidad de control. La tokenización de un bin discreto a 256 contenedores emite cuántos tokens por segundo? ¿Puede un VLM 7B mantenerse al día? 10 libertad de arma mecánica, 30 Hz de frecuencia de control, 256 frecuencia de dispersión de bin;; por segundo, ¿cuántos tokens se producen? 7B VLM 能跟上?

2. FAST tokenization comprime trayectorias de 30 pasos a ~10 tokens. ¿Qué pierde el usuario si la trayectoria tiene movimiento de alta frecuencia (por ejemplo, tambor)? FAST se va a 30 pasos de轨迹压缩为约10 tokens──如果轨迹包含高频运动(如击鼓),会丢失什么?

3. El flujo de la cabeza de coincidencia de π0 se denota en ~5 pasos. Comparar el rendimiento con el decodificación autorregresista de OpenVLA a 4-5 Hz.

4. El sistema 1 / sistema 2 de GR00T divide mapas a Kahneman. Proponga una división diferente (sistema 3?) que podría ayudar a caminar a bipedos. GR00T's sistema1/ sistema2 separándose de la teoría de la máquina. Propone un esquema separado diferente.

5. Lea la sección 4 de Open X-Embodiment sobre la curadoria de conjuntos de datos. Nombre de las tres reglas de curadoria que impiden la filtración de dominio.

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| VLA | "Vision-language-action" 视觉-语言-动作模型 | Model that takes image + instruction and outputs action commands 接受图像+指令并输出动作命令的模型 | |
| Action tokenization | "Discrete bins" 离散 bin 编码 | Quantize continuous joint targets into 256 bins per dim, each a vocab ID 将连续关节目标量化为每维 256 个 bin，每个 bin 对应一个词表 ID | |
| FAST tokenizer | "Frequency action tokens" 频域动作 token | DCT + quantize to compress 30-step trajectories to ~10 tokens 用 DCT + 量化将 30 步轨迹压缩为约 10 个 token | |
| Co-fine-tune | "Mix web + robot" 混合微调 | Train on web VQA data alongside robot demos to preserve general knowledge 在网络 VQA 数据和机器人演示上联合训练以保留通用知识 | |
| Flow-matching action head | "pi0 continuous output" 流匹配动作头 | Small transformer that outputs a 50-step action sequence via rectified flow 通过矫正流输出 50 步连续动作序列的小型 Transformer | |
| System 1 / System 2 | "Dual-system control" 双系统控制 | Large VLM plans slowly, small action head acts quickly; GR00T pattern 大 VLM 慢规划，小动作头快执行；GR00T 模式 | |
| Open X-Embodiment | "RT-X dataset" 开放具身数据集 | 1M-trajectory cross-robot dataset; the training corpus 100 万轨迹跨机器人数据集；标准训练语料 | |

## Más Leer más Leer más

- [Brohan et al. — RT-2 (arXiv:2307.15818)](https://arxiv.org/abs/2307.15818)
- [Kim et al. — OpenVLA (arXiv:2406.09246)](https://arxiv.org/abs/2406.09246)
- [Black et al. — π0 (arXiv:2410.24164)](https://arxiv.org/abs/2410.24164)
- [NVIDIA — GR00T N1 (arXiv:2503.14734)](https://arxiv.org/abs/2503.14734)
- [Open X-Embodiment Collab — RT-X (arXiv:2310.08864)](https://arxiv.org/abs/2310.08864)
