# Agentes multimodal y uso informático (Capstone) ✓

> El producto fronterizo 2026 es un agente multimodal que lee capturas de pantalla, hace clic en botones, navega por las interfaces web, llena formularios y completa flujos de trabajo de extremo a extremo. SeeClick y CogAgent (2024) demostraron que la primera era la de la conexión a tierra. Ferret-UI añadió móvil. ChartAgent introdujo el uso de herramientas visuales para los gráficos. VisualWebArena y AgentVista (2026) son los puntos de referencia de las persecuciones fronterizas  e incluso Gemini 3 Pro y Claude Opus 4.7 puntaje ~30% en las tareas difíciles de AgentVista. Esta piedra angular reúne todos los hilos de la Fase 12: percepción (VLM de alta resolución), razonamiento (LLM con uso de herramientas), conexión a tierra (salida de coordenadas), memoria de horizonte largo y evaluación.

> **【中文解读】**El producto de vanguardia de 2026 es capaz de leer recta, punto de pulsación, navegación web, relleno de formularios, de extremo a extremo de completar el flujo de trabajo. AgenteSeeClick y CogAgent demostraron que la interfaz gráfica de usuario se puede usar en dispositivos móviles, Interfaz gráfica de usuario se puede extender a dispositivos móviles, pero en la interfaz gráfica de usuario, incluso Gemini 3 Pro y Claude Opus 4.7 también tienen un porcentaje de aprobación de aproximadamente el 30% en la fase 12.

**Type:** Capstone
**Languages:** Python (stdlib, action schema + agent loop skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 12 · 09 (Qwen-VL JSON), Phase 14 (Agent Engineering)
**Time:** ~240 minutes

> ¿ Qué es esto ?**【前置】**學本節前請先掌握:Fase 12 全部(VLM 演进) 、Fase 14·01-10(Agencia 循环、工具调用) 、Fase 14·30+(工作台系列 实践) ⋅本节是Fase 12 的毕业课所有多模态 +Agencia 技术整合成一个能操作电脑的产品──
> ¿ Qué es esto ?**【类比】**Más información sobre el proceso de evaluación de la evaluación de los resultados de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de los resultados de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la
> ️ **【易错点】**让 Agent 直接执行动作不设人工审核 = 灾难(可能误转账、错删除) 修复:所有"破坏性动作" (→ "la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la

## Objetivos de aprendizaje

- Diseñar un bucle de agentes multimodal: percibir → razón → acción → observación → repetición.
  设计多模态 Agente 循环:感知 → 推理 → 行动 → 观察 → 重复。
- Construir un esquema de salida de tierra de la interfaz gráfica (coordenadas de clic, texto de tipo, desplazamiento, arrastre) el VLM puede emitir como JSON.
  构建 GUI 定位输出模式(点击坐标、输入文字、滚动、拖),VLM 以 JSON 格式输出──
- Comparar agentes de sólo capturas de pantalla vs agentes de árbol de accesibilidad vs agentes híbridos.
  En comparación con el agente de la escisión pura, el agente sin obstáculos y el agente mixto.
- Configurar una evaluación de referencia de agente multimodal en una pequeña rodaje de VisualWebArena.
  En VisualWebArena, se ha creado un grupo de diferentes modelos de agentes.

## El problema es definido .

> **【中文解读】**En el caso de los usuarios de un sitio web, los usuarios de un sitio web pueden utilizar un sistema de visualización de datos de usuario para realizar un proceso de visualización de datos de usuario.

Un flujo de trabajo en el sitio de reserva: "Encuentra un vuelo a Tokio para el 15 de abril, asiento en el pasillo bajo $800, reserva".

> Una orden de trabajo: "Help me find 4 月 15 日飞东京的航班,靠走道, $800 以下,预订──"

Un agente multimodal debe:

> Más información sobre el producto

1. Toma una captura de pantalla del navegador.
   En inglés, el lenguaje de la lengua se traduce en inglés como "en inglés".
2. Parsear la captura de pantalla + URL + objetivo en un plan.
   En inglés, traducción de la lengua inglesa:解析截图 + URL + 目标,生成计划──
3. Emite una acción estructurada: haga clic (en x,y), escriba "Tokyo" (en el elemento E), desplaza hacia abajo, seleccione (botón de radio).
   En el texto original, el texto se basa en el texto de la traducción de la palabra "Tokio" (en inglés: "Tokyo") y en el texto de la traducción de la palabra "Tokyo" (en inglés: "Tokyo") y en el texto de la traducción de la palabra "Tokyo" (en inglés: "Tokyo") y en el texto de la traducción de la palabra "Tokyo" (en inglés: "Tokyo") y en el texto de la traducción de la palabra "Tokyo" (en inglés: "Tokyo") y en el texto de la traducción de la palabra "Tokyo" (en inglés: "Tokyo") y en el texto de la palabra "Tokyo" (en inglés: "Tokyo") y en el texto de la palabra "Tokyo" (en inglés: "Tokyo").
4. Aplicar la acción en el navegador.
   En español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en español: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés: en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; ma más más más más más más más anglais; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; en inglés; anglais; anglais; anglais; anglais; anglais; anglais; anglais; anglais; anglais; ang
5. Observe el nuevo estado (próxima captura de pantalla).
   En el caso de los niños, el estado de salud es un problema.
6. Repita hasta que la tarea esté terminada.
   En español, "recomposición" significa "también" y "también" significa "también".

Cada paso es una llamada VLM multimodal. La salida VLM debe ser JSON parseable. Los errores se componen en cada paso, por lo que la recuperación es importante.

> Cada paso es una vez de varios modos de VLM 调用──VLM 输出必须是可解析的 JSON──错误在步骤间积累, por lo tanto, el mecanismo de recuperación es crucial──

## El concepto central.

> **【中文解读】**Agente de uso informático) permite que la IA opere directamente la interfaz de computadora: captura de contenido de pantalla, generación de ratones/borras de control.

> **【拓展：Computer Use 的前沿**El uso de la computadora de Antropic 让 Claude 直接操作桌面应用,完成网页浏览、表单填写等任务──OpenAI Operator 使用类似方法──关键技术挑战:精确定位: 准确点击按) 状态跟踪: 了解界面变化: 误恢复: 操作失败后重试: △


### GUI de tierra  el primitivo  GUI 定位 基础原语

La conexión a tierra de la interfaz gráfica es: dada una captura de pantalla y una instrucción de lenguaje natural, emitir la coordenada (x, y) para hacer clic (o otra acción).

> GUI 定位是:给定一张截图和自然语言指令,输出需要点击的 (x, y) 坐标(或其他动作)

> **【中文解读】**GUI 定位是:给定一张截图和自然语言指令,输出需要点击的 (x, y) 坐标(或其他动作) ――SeeClick es el primer resultado abierto a gran escala, CogAgent 增加了1120x1120高分辨率编码,Ferret-UI 聚焦移动端 UI──输出格式通常是JSON,`element_desc`字段帮助恢复当坐标在截图间漂移时,语义提示让系统重新定位──

SeeClick (arXiv:2401.10935) fue el primer resultado abierto a escala: ajustar a la perfección un VLM en datos de GUI sintéticos + reales, las coordenadas de salida como tokens de texto plano.

> SeeClick es el primer gran resultado abierto: en sintetizado+ real GUI datos en VLM, con símbolo de texto puro 输出坐标──有效──

CogAgent (arXiv:2312.08914) añadió codificación de alta resolución 1120x1120 para interfaces interactivas densas. puntaje: ~84% en la navegación web.

> CogAgent para la interfaz de usuario más compacta añadió 1120x1120 código de alta resolución.

Ferret-UI (arXiv:2404.05719) se centra en las UI móviles, se integra con los datos de accesibilidad de iOS.

> Ferret-UI 聚焦移动端 UI, integrado iOS 无障碍数据──

El formato de salida es generalmente JSON:

> 输出格式: generalmente es JSON:

```json
{"action": "click", "x": 384, "y": 220, "element_desc": "Search button"}
```

El `element_desc`ayuda a la recuperación: si las coordenadas se desplazan entre capturas de pantalla, la pista semántica permite que el sistema vuelva a aterrizar.

> `element_desc`帮助恢复: si el坐标在截图间漂移, se puede hacer un cambio de posición en el sistema.

### Planes de acción.

Un esquema de acción típico tiene 6-10 tipos de acción:

> El modelo típico de movimiento incluye 6-10 tipos de movimientos:

> **【中文解读】**El típico modo de movimiento incluye 6-10 especies de movimientos tipo:clic (click) (点击) (type) (输入) (scroll) (roll) (drag) (拖) (drag) (拖) (select) (select) (select) (select) (hover) (hover) (suspend) (navigate) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (see) (en) (en) (en) (en) (en) (en)))) (en)) (en)) (en)))) (en)) (en)) (en)))) (en)) (en)))) (en)) (en)))) (en)))) (en)))) (en)))) (en)))) (en)))) (en)))))))))) (en))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

- `click`(x, y)
  En inglés:`click`:点击 (x, y)
- `type`¿Qué es esto?
  En inglés:`type`:输入文本,可选位置──
- `scroll`: (dirección, cantidad)
  En inglés:`scroll`¡Más tiempo!
- `drag`(x0, y0, x1, y1)
  En inglés:`drag`Desde (x0, y0) 拖到 (x1, y1)
- `select`: (option_index)
  En inglés:`select`: seleccionar los proyectos:
- `hover`(x, y)
  En inglés:`hover`: susp susp (x, y)
- `navigate`¿Qué es esto ?
  En inglés:`navigate`Por ejemplo, en el caso de los viajeros,
- `wait`(ms)
  En inglés:`wait`Esperemos mil segundos.
- `done`: (éxito, explicación)
  En inglés:`done`:完成(成功/失败, explica)

El agente emite una acción por paso. El envase del navegador ejecuta y devuelve el nuevo estado.

> Agente cada paso de salida de un movimiento.

### Sólo capturas de pantalla vs árbol de accesibilidad .

> **【中文解读】**两种输入模式: Pure截图模式最通用但精度较低;无障碍树 (无障碍树) más fiable pero sólo disponible en datos estructurados; Mixed Mode simultáneamente utiliza ambos, Tree for atomic motion positioning,截图 for语义理解;; Production Agent 尽可能使用混合模式;;

Dos modos de entrada:

> 两种输入模式:

- Sólo capturas de pantalla: imagen completa, sin información estructural.
  En inglés, "Creo de la imagen" es el término completo de la imagen.
- Árbol de accesibilidad: información estructurada de accesibilidad DOM / iOS. mucho más confiable para la tierra; funciona donde el árbol está disponible.
  China:无障碍树: estructurada DOM / iOS 无障碍信息──定位更可靠;在有树数据时可用──
- Híbrido: ambos, con el árbol como base confiable para las acciones atómicas y la captura de pantalla para el contexto semántico.
  La lengua árabe se utiliza para la definición de la lengua árabe.

Los agentes de producción usan híbridos cuando es posible. La automatización del navegador (Selenium + accesibilidad) siempre tiene el árbol; las aplicaciones de escritorio a veces lo hacen.

> Productor de productos 尽可能使用混合模式──浏览器自动化(Selenium + 无障碍) Siempre hay árbol;

### Memoria de largo horizonte                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

Un flujo de trabajo de 20 pasos genera 20 capturas de pantalla. El contexto del VLM se llena rápidamente. Tres estrategias de compresión:

> 20 pasos de trabajo producen 20 张截图──VLM 上下文快快填满──三种压缩策略:

> **【中文解读】**20 pasos de trabajo generan 20 cintas, VLM 上下文很快填满了.

- En la cadena de resumen: después de cada 5 pasos, resumen lo que ha sucedido, deje caer viejas capturas de pantalla.
  En el contexto de la historia, el historiador de la historia de la historia de la historia de la historia, el historiador de la historia de la historia, el historiador de la historia, el historiador de la historia, el historiador de la historia, el historiador de la historia, el historiador de la historia, el historiador de la historia, el historiador de la historia, el historiador de la historia, el historiador de la historia, el historiador y el historiador de la historia de la historia, el historiador de la historia, el historiador y el historiador de la historia.
- Skip-frame: mantenga la primera, última y cada 3 captura de pantalla.
  La historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la China.
- Registro de herramientas: ejecutar acciones, mantener un registro de texto de lo que se hizo; no vuelva a mirar capturas de pantalla antiguas.
  El texto original de la obra original se traduce en inglés como "El libro de la historia".

La API de uso de computadoras de Claude utiliza el patrón de registro.

> El ordenador de Claude utiliza API utiliza el modelo de registro.

### Usar herramientas visuales Usar herramientas visuales

> **【中文解读】**ChartAgent  introducir herramientas de visualización调用:Agent puede sacar "cortar la región (100,200,300,400) y luego utilizar OCR" como herramienta de调用.

ChartAgent (arXiv:2510.04514) introduce el uso de herramientas visuales para la comprensión de gráficos: recorte, zoom, OCR, llamada de detección externa. El agente puede emitir "recorte a región (100, 200, 300, 400) y luego llamar a OCR" como llamada de herramienta. La herramienta devuelve texto; el VLM continúa el razonamiento.

> ChartAgent  introducir herramientas de visualización调用用于图表理解:剪剪,缩放,OCR、调用外部检测──Agent puede exportar "剪剪到区域 (100, 200, 300, 400) y luego调用 OCR" como herramienta调用──工具返回文本;VLM 继续推理──

Este patrón generaliza: la solicitud de marcas de conjunto, la anotación de regiones y las herramientas de detección externa se ajustan al mismo esquema de "salida una llamada de herramienta, recibe una respuesta estructurada".

> Este modelo se puede promover: conjunto de marcas de información, marcas de área y instrumentos de inspección externa están adaptados a la misma "herramienta de salida, de consulta, de recepción estructurada" modelo.

### Los puntos de referencia de 2026 .

> **【拓展：多模态 Agent 基准全景】**ScreenSpot-Pro 测试 GUI 定位(open模型 ~85%,前沿 ~90%);VisualWebArena 测试端到端网页任务(open模型 ~20%,Gemini 3 Pro ~27%);AgentVista es el 2026 el más difícil de base, que cubre 12 áreas de trabajo real, modelo de primera línea sólo 27-40%;WebArena/WebShop 已被前沿模型和──

- ScreenSpot Pro. GUI de tierra en ~ 1k capturas de pantalla web. Abierto SOTA Qwen2.5-VL-72B ~85%. Frontier ~90%.
  En el caso de los equipos de la red, el número de usuarios es de aproximadamente un 90% en el caso de los equipos de la red.
- VisualWebArena. tareas web de extremo a extremo (tienda, foro, anuncios clasificados). SOTA abierto ~ 20%. Gemini 3 Pro ~ 27%.
  La página web de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red
- El punto de referencia más difícil para 2026: flujos de trabajo realistas en 12 dominios.
  En el contexto de la actualidad, el modelo de trabajo en el sector de la industria es el más difícil de alcanzar.
- WebArena / WebShop. Referencias más antiguas; saturadas por frontera.
  El sitio web está en el centro de la historia de la historia de la industria.

### ¿Por qué es difícil todavía?

> **【中文解读】**Agente  rendimiento botella:1) 细粒度视觉定位("点击小 X"在移动分辨率下经常失败);2) 长期规划(10 步后 Agente 偏离目标);3) 错误恢复(点击失败时检测和恢复缺乏训练数据);4) 跨页面上下文(跳转标签页或长表单丢失状态) ――研究方向包括记忆架构、、式重规划多样式验证──

Cuellos de botella en el rendimiento de los agentes:

> Agente 性能瓶:

1. "Clique en la pequeña X" a menudo falla en la resolución móvil.
   En el caso de los pequeños grupos de la población, el número de grupos de población en el área de distribución de los grupos de población es de aproximadamente un millón de habitantes.
2. Después de 10 acciones, el agente se aleja del objetivo.
   En español, el nombre de la persona que se encuentra en el centro de la ciudad es el de la ciudad de Nueva York.
3. Recuperación de error. Cuando un clic falla (botón incorrecto), la detección + recuperación rara vez es un entrenamiento de datos.
   En el caso de los niños, el tiempo de trabajo es de 5 años.
4. Contexto de página cruzada. Saltando entre pestañas o formularios largos pierde estado.
   Traducción:跨页面上下文──跳转标签页或长表单丢失状态──

Direcciones de investigación: arquitecturas de memoria, replanamiento explícito, verificación multimodal (combinación de capturas de pantalla para el éxito de la acción).

> Estudios de la investigación y la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la ciencia de los casos de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la ciencia de los casos de la investigación de la investigación de la ciencia de los casos en el desarrollo de la investigación de la investigación de la ciencia de la ciencia de los casos de la ciencia de los casos de la ciencia de la ciencia de la ciencia de la ciencia de los casos de la ciencia de la ciencia de la ciencia de los casos de la ciencia de los casos de la ciencia de la ciencia de la ciencia de los casos de la ciencia de los casos de la ciencia de los casos de la ciencia de la ciencia de los casos de la ciencia de los casos de la ciencia de los casos de la ciencia de la ciencia de los casos de la ciencia de los casos de la ciencia de la ciencia de los casos de los casos de la ciencia de los casos de la ciencia de los casos de la ciencia de los casos de los casos de la ciencia de los casos de los casos de la ciencia de los casos de los casos de

### La piedra angular construye-lo.

> **【中文解读】**毕业项目任务: construir una computadora usando Agent, capaz de leer pre-order web 模拟页面的 HTML+截图,规划多步序列(搜索→选择→填表→提交),输出匹配动作模式的 JSON 动作, y evaluar en 10 固定任务──

La tarea final: construir un agente de uso de computadora que:

> 毕业项目任务:构建一个计算机使用 Agent, requerir:

1. Lea la captura de pantalla HTML + de una página falsa del sitio de reserva.
   En inglés, el texto de la página web es "Html + 截图".
2. Planea una secuencia de varios pasos: búsqueda → seleccionar → llenar el formulario → enviar.
   中文翻译:规划多步序列:搜索→选择→填表→提交──
3. Emite acciones JSON que coinciden con el esquema de acción.
   En inglés, el código de código de JSON 动作.
4. Evalúa en una rebanada fija de 10 tareas.
   En español: evaluar en 10 tareas fijas.

La lección proporciona código de andamio que es fácil de extender en un navegador real.

>  cursos proporcionan código de escritura, fácil de extender a un navegador real ⋅

## Usalo con el marco de ejecución
```figure
mm-agent-loop
```

## Usalo

`code/main.py`es el andamio de piedra angular:

- Descripción de esquema de acción JSON (10 acciones).
  En inglés, el lenguaje de la lengua japonesa se traduce en inglés como "JSON".
- Fake estado del navegador como dictado.
  En el caso de los niños, el estado de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela
- El esqueleto de bucle del agente: estado de recepción, emisión de acción, aplicación, bucle.
  En inglés, "Agent" se llama "Agent" o "Agent" se llama "Agent" o "Agent" se llama "Agent" o "Agent" se llama "Agent" o "Agent" se llama "Agent" o "Agent" se llama "Agent" o "Agent" se llama "Agent" o "Agent" se llama "Agent" o "Agent" se llama "Agent" o "Agent" o "Agent" se llama "Agent" o "Agent" o "Agent" se llama "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "Agent" o "O" o "Agent" o "O" o "O" o "Agent" o "O" o "O" o "O" o "O" o "O" o "O" o "O" o "O" o "O "O "O "O "O" o "O "O "O "O "O "O " "O "O "O " "O " "O " " "O " " " "O " " " o " o " o " o " o " o " o " " " " " o " o " " o " o " o " " " " o " o " " " " " o " " o " " o " o " " " " " o " o " " " o " " " " " " o " " " " " " " " " " " " o " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
- 10 mini-marcas de referencia de tareas (páginas sintéticas) para medir la tasa de éxito de extremo a extremo.
  En el caso de los proyectos de investigación, el proyecto de investigación de la Universidad de San Francisco (UFPA) se ha desarrollado en el ámbito de la investigación y la investigación.
- Cubo de recuperación de errores para cuando una acción falla.
  En español: 动作失败时的错误恢复子.

## Envíe el producto .

Esta lección produce`outputs/skill-multimodal-agent-designer.md`. Dado un producto de uso informático (dominio, conjunto de acciones, objetivo de evaluación), diseña el bucle completo de agente, la estrategia de memoria, el modo de aterrizaje y el puntaje esperado de referencia.

> 本课产 出  `outputs/skill-multimodal-agent-designer.md` Dedicar productos de uso informático (en el ámbito de la evaluación), diseñar un ciclo completo de agentes, estrategias de memoria, modelos de ubicación y porcentajes de base de datos previstos.

## Los ejercicios.

1. Extenda el esquema de acción con un `screenshot_region`¿Qué tareas son beneficiosas?
   扩展动作模式, añadir `screenshot_region`¿Qué tareas se beneficiarán?

2. Leer AgentVista (arXiv:2602.23166). Describa la categoría de tareas más difíciles y por qué los modelos fronterizos siguen fallando.
   阅读 AgentVista 论文── describir las categorías de tareas más difíciles y las causas de que el modelo de vanguardia sigue fracasando──

3. Compresión de memoria de largo horizonte: diseñar una cadena de resumen con ≤4 capturas de pantalla mantenidas en vivo, cualquier número registrado.
   长期记忆压缩: diseñar una cadena de resumen, mantener ≤4 张截图活跃, cantidad arbitraria registrada hasta日志。

4. Construir un gancho de recuperación de errores: en caso de falla de acción (botón no encontrado), ¿qué hace el agente después?
   构建错误恢复子:当动作失败 (按未找到) 时,Agent siguiente paso hacer qué?

5. Comparar Claude 4.7 con una captura de pantalla híbrida + árbol de accesibilidad Qwen2.5VL en 10 tareas web. ¿Cuál gana en qué tareas?
   En comparación con el modelo de Claude 4.7 en la imagen pura y el modelo mixto Qwen2.5 VL en 10 tareas de páginas web. ¿En qué clase de tareas ganó?

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|----------|
| GUI grounding | "Click coordinates" | Model outputs (x,y) for the target of an instruction on a screenshot | GUI 定位：模型输出截图上指令目标的 (x,y) 坐标 |
| Action schema | "Tool definitions" | JSON description of valid actions (click, type, scroll, drag) | 动作模式：有效动作的 JSON 描述 |
| Accessibility tree | "Structured DOM" | Machine-readable UI hierarchy from browser/iOS APIs | 无障碍树：来自浏览器/iOS API 的机器可读 UI 层级 |
| Hybrid agent | "Screenshot + tree" | Uses both image and structured info; more reliable than either alone | 混合 Agent：同时使用图像和结构化信息 |
| Visual tool use | "Zoom/crop/detect" | Agent calls external vision tools (OCR, detection) mid-plan | 视觉工具使用：Agent 在规划中调用外部视觉工具 |
| Summary-chain | "Memory compression" | Periodic text summaries replace long screenshot history | 摘要链：定期文本摘要替代长截图历史 |
| VisualWebArena | "E2E web bench" | 2024 benchmark for end-to-end web tasks | 端到端网页任务基准（2024） |
| AgentVista | "2026 hard bench" | 12-domain realistic workflows; even Gemini 3 Pro scores ~30% | 12 领域真实工作流基准，前沿模型仅约 30% |

## Más Leer más Leer más

- [Cheng et al. — SeeClick (arXiv:2401.10935)](https://arxiv.org/abs/2401.10935)
- [Hong et al. — CogAgent (arXiv:2312.08914)](https://arxiv.org/abs/2312.08914)
- [You et al. — Ferret-UI (arXiv:2404.05719)](https://arxiv.org/abs/2404.05719)
- [ChartAgent (arXiv:2510.04514)](https://arxiv.org/abs/2510.04514)
- [Koh et al. — VisualWebArena (arXiv:2401.13649)](https://arxiv.org/abs/2401.13649)
- [AgentVista (arXiv:2602.23166)](https://arxiv.org/abs/2602.23166)
