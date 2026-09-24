# Negociación y negociación Negociación 讨价还价

> Los agentes negocian recursos, precios, asignaciones de tareas y términos. El conjunto de puntos de referencia 2026 es claro: NegotiationArena (arXiv:2402.05863) muestra que los LLM pueden mejorar los beneficios ~20% a través de la manipulación de persona ("desesperación"); "Medición de las habilidades de negociación" (arXiv:2402.15813) muestra que el comprador es más difícil que el vendedor y la escala no ayuda  su **OG-Narrator**(generador de ofertas deterministas + narrador de LLM) empujó la tasa de transacciones del 26,67% al 88.88%; la Competencia de Negociación Autónoma a Gran escala (arXiv:2503.06416) llevó a cabo cerca de 180 mil negociaciones y encontró que**chain-of-thought-concealing**Bhattacharya et al. 2025 en Harvard Negotiation Project metrics clasificó a Llama-3 como más eficaz, Claude-3 agresivo, GPT-4 más justo. Esta lección implementa el Protocolo de Contratación Net (el antepasado de FIPA, Lección 02), conecta un comprador/vendedor de estilo LLM, ejecuta una descomposición de estilo OG-Narrador y mide cómo cambia la tasa de transacción con cada elección estructural.

> **【中文解读】**Este artículo presenta las estrategias de negociación en la distribución de recursos y tareas de los agentes.

> **【拓展：negotiation bargaining→具体应用】**协商和讨价还价 es el mecanismo central de distribución de recursos de múltiples agentes. Tres estrategias de negociación: 1) 合作型Agentos buscan la maximización de los intereses globales; 2) 竞争型Agentos buscan la maximización de sus propios intereses; 3) 混合型兼顾个人和整体. En la economía de los agentes, las negociaciones suelen realizarse mediante un acuerdo de propuesta-respuesta estructurado, similar al protocolo de red de contratos.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 02 (FIPA-ACL Heritage), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 02（FIPA-ACL 遗产），Phase 16 · 09（并行群体网络）

> ¿ Qué es esto ?**【前置】**Estudios de la FPIA en el ámbito de la formación profesional y de la formación profesional.
> ¿ Qué es esto ?**【类比】**Agente 协商 = "二手市场砍价"──LLM 通过 persona 操纵(装穷)能多 20%;隐藏推理过程的 Agent 赢对手看不到你的底线──OG-Narrator 把协商拆为"确定性提议生成"+"LLM 叙述",交易率 26%→89%──模型差异:Llama-3 最有效、Claude-3 强势、GPT-4公平 最选即选择风格──
**Time:** ~75 minutes | **时间:** ~75 分钟

## # El problema # # El problema #

Los dos agentes deben acordar un precio. Dejo a sí mismos con las instrucciones de lenguaje puro, las LLM 2024-2026 cierran acuerdos a tasas sorprendentemente bajas (~27% en las ofertas estrictamente parametrizadas en arXiv:2402.15813).

> 两个 agentes 需要就价格达成. 在纯语言提示下,2024-2026年 LLM 成交率惊地低. 在 arXiv:2402.15813 的紧密参数化议议价中约27%) 规模化不能解决: GPT-4 在议价结构上不比 GPT-3.5 好;它只是在议价*语言*上更好.

El problema principal es que los LLM confluyen dos trabajos: decidir la oferta y narrarla. OG-Narrator los separó: un generador de ofertas determinista calcula los movimientos numéricos; el LLM solo narra.

> El problema fundamental es que el LLM ha mezclado dos tareas: determinar la oferta y la oferta de narración.

Esto refleja un hallazgo clásico de múltiples agentes: descoplar el mecanismo de la capa de comunicación gana. El Protocolo de Red de Contratos (FIPA, 1996; Smith, 1980) es el mecanismo de referencia del mercado de tareas.

> Esto refleja un clásico mecanismo de múltiples agentes que se encuentra en el proceso de desarrollo de la tecnología de comunicación.

## Concepto de la esencia de la concepción

### En un párrafo, la red de contratos

El Protocolo Net de Contratos de Smith de 1980: un **manager**transmite a **call for proposals (cfp)**¿ Qué es ?**bidders**Responder con **propose**mensajes que contienen sus ofertas; el gerente elige un ganador y envía **accept-proposal**al ganador y **reject-proposal**El ganador realiza el trabajo.**refuse**La FIPA codificó esto como `fipa-contract-net`protocolo de interacción.

> El acuerdo de contrato de Smith 1980:**管理者**广播**提案请求（cfp）**El artículo 1**投标人**回复 contiene su oferta de**提案**消息; administrator选择获胜者并向获胜者发送**接受提案**, hacia los votantes**拒绝提案**△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △   △ △                                                                                                                                                              **拒绝**(投标人拒绝提案)  FIPA 将其编码为`fipa-contract-net`交互协议── también

### Por qué gana el narrador de OG

"Medición de las habilidades de negociación de los modelos de lenguaje" (arXiv:2402.15813) observó que:

> "Mejure Language Model of议价能力" (en inglés) observa:

- Los LLM suelen infringir las reglas de negociación (ofrecer a precios sin sentido, ignorar el ZOPA de la otra parte).
  La ley de precios de los productos de la industria de la producción de petróleo (LLM) viola frecuentemente las reglas de precios de los productos de la industria de la producción de petróleo (LLM) y de la industria de la producción de petróleo (LLM) (LLM) (LLM) 经常违反议价规则 (LLM) 
- Se anclan mal (aceptan malas ofertas iniciales; contraofertas en cantidades simbólicas en lugar de estratégicas).
  China: 定效差 (定效差)                                                                                                                                                                                                                                                         
- Los modelos más grandes hacen que el lenguaje sea más plausible con un error estratégico similar.
  China: sólo por la escala no se pueden resolver estos problemas.

La descomposición del narrador OG:

```
           ┌──────────────────┐        ┌──────────────────┐
  state  → │ offer generator  │ price → │  LLM narrator    │ → message
           │  (deterministic) │        │  (writes the     │
           │                  │        │   human-style    │
           └──────────────────┘        │   accompaniment) │
                                       └──────────────────┘
```

El generador de ofertas es una estrategia de negociación clásica: un modelo de negociación de Rubinstein, una estrategia de Zeuthen o un simple precio de venta por precio.

La tasa de negocio se eleva porque:
- Los precios se mantienen en la zona de negociación.
- Los anclajes son estratégicos, no emocionales.
- El LLM hace lo que es bueno: escribir.

> Por lo tanto, el precio de la compra se ha incrementado.
> - 价格保持在议价区间内──
> - 点是战略性的,而非情绪化的──
> - LLM hacer lo que es bueno: escribir.

### NegociaciónConclusiones de Arena

El estudio de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la ciencia de la ciencia de los ciencias de los ciencias de los ciencias de la ciencia de la ciencia de los Estados Unidos de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de los Estados Unidos de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de los Estados de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de los Estados de la ciencia de los Estados de la ciencia de la ciencia de los Estados de la ciencia de los Estados de la ciencia de la ciencia de la ciencia de la ciencia de la ciencia de la

> El proyecto de ley de la Unión Europea (UE) de 2004 sobre la protección de las personas con discapacidad (UE) y la protección de las personas con discapacidad (UE) de 2006 sobre la protección de las personas con discapacidad (UE) de 2006 sobre la protección de las personas con discapacidad (UE) (UE) de 2006 sobre la protección de las personas con discapacidad (UE) (UE) de 2006 sobre la protección de las personas con discapacidad (UE) (UE) de 2006 sobre la protección de las personas con discapacidad (UE) (UE) (UE) (UE) (UE) (UE) (UE) 2015: 2017: 2745, p.

- Las LLM pueden mejorar los pagos ~20% adoptando personas ("Estoy desesperado por vender esto para el viernes")  La manipulación de persona es una táctica real.
  El LLM puede aumentar los beneficios mediante la adopción de personas para aumentar los ingresos de aproximadamente un 20% ("I urgently need to sell this in this周五前")
- Los agentes justos/cooperativos son explotados por los adversarios; la defensa requiere una contraposición explícita.
  En la actualidad, el sistema de defensa de la población de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la Sudán.
- Los pares simétricos convergen en resultados inequitados en aproximadamente el 40% de los escenarios de referencia.
  En el contexto de la base de la situación, el 10% de los resultados obtenidos en el caso de la tasa de cambio se han reducido a un 40% en comparación con el de la tasa de cambio.

Esto no es "los LLM son malos negociadores". Es "los LLM negocian demasiado como los humanos, incluyendo las partes explotables".

> Esto no es "LLM es un mal negociador" sino "el modo de negociación de LLM es demasiado humano, incluida la parte que se puede utilizar".

### El ocultamiento de la cadena del pensamiento

La Gran Competencia de Negociación Autónoma (arXiv:2503.06416) realizó aproximadamente 180 mil negociaciones en muchas estrategias de LLM. Los ganadores ocultaron su razonamiento a sus contrapartes:

> En el concurso de consultas autónomas de gran escala ((arXiv:2503.06416) se han llevado a cabo aproximadamente 180.000 consultas en muchas estrategias de LLM.

- Si un agente imprime "Sólo voy a$75; my reservation price is $70" en un rascacielos visible al público, el oponente lo lee.
  Si el agente sólo me iba a salir$75；我的保留价是 $70" impreso en el libro de la escritura, para que pueda ser leído por la mano.
- Los ganadores computaban la estrategia en privado; el canal de salida contiene solo la oferta y la narración mínima requerida.
  La estrategia de cálculo de los ganadores; el canal de salida sólo contiene una oferta y una descripción mínima.

Este es un eco de 2026 de la teoría clásica del juego (Aumann 1976 sobre racionalidad e información): revelar su valoración privada costos de pago. LLM no intuyen esto y felizmente escriben sus reservas en rastros de razonamiento que se vuelven visibles para la contraparte.

> Este es el clásico blog de Aumann 1976  Sobre la razón y la información) en 2026 Reacción: revelar la pérdida de beneficios de la valoración privada. LLM no se dará cuenta de esto, pero está dispuesto a introducir los precios de retención en el rastro de la hipótesis, estos rasgos son visibles para los oponentes.

Ingeniería de toma: separar el contexto privado de la plancha de raspado del contexto público de los mensajes. No es opcional.

> 工程要点:将私人草稿本上下文与公开消息上下文分离── esto no es opcional──

### Bhattacharya et al. 2025  clasificaciones de modelos

En relación con las métricas del proyecto de negociación de Harvard (negociación en principio, respeto de la BATNA, reciprocidad de intereses):

> En el programa de Harvard, el objetivo de la organización es:

- **Llama-3**fue más eficaz en las negociaciones (taxa de transacción + pago).
  En inglés:**Llama-3**En el ámbito de la negociación, la tasa de conversión + 收益 (recaudación) es la más efectiva.
- **Claude-3**El Consejo de Ministros de la Unión Europea ha adoptado una decisión en el marco de la cual se ha adoptado un nuevo reglamento.
  En inglés:**Claude-3**Es el negociador más agresivo.
- **GPT-4**fue la más justa (la menor variación en la remuneración entre los emparejamientos).
  En inglés:**GPT-4**La diferencia de beneficios entre los diferentes tipos de compensación es mínima.

Este es un instantáneo de 2025. El punto no es qué modelo gana en abril de 2026  es que los diferentes modelos base tienen estilos de negociación persistentes.

> Este es un rápido resumen de 2025. El enfoque no es el modelo que ganará en el mes de abril de 2026, sino que el modelo de base diferente tendrá un estilo de negociación duradero.

### Alocamiento de tareas a través de contrato Net + LLM

El uso moderno de Contract Net para LLM multi-agente:

> 合同网在现代 LLM 多 Agent 中中重用:

1. El agente gerente descompone una tarea en unidades.
   En inglés, el agente administrador se divide en unidades.
2. Las emisiones `cfp`con descripción de tareas a los agentes de los trabajadores.
   Traducción:A los trabajadores y trabajadoras`cfp`¿Qué es eso?
3. Cada trabajador devuelve una oferta: `(price, eta, confidence)`donde el precio podría ser tokens, unidades de cálculo o dólares.
   Cada trabajador regresa a un precio:`(price, eta, confidence)`, el precio puede ser token ̇ calcular unidades o dólares ̇
4. El gerente elige los ganadores (un solo o múltiples, dependiendo de la tarea) y los premios.
   Traducción:Manejerador seleccionó a quien ganó (单个或多个,取决于任务)并授标──
5. Los trabajadores rechazados pueden presentar ofertas para otras tareas.
   En inglés, "también se puede contratar a un trabajador que no tiene trabajo".

Esto supera a 100 trabajadores porque la coordinación es transmisión y respuesta, no chat sincrónico.

> Esto puede ampliarse muy bien a más de 100 trabajadores, ya que coordinar es un modo de transmisión y respuesta, y no un modo de conversación simultánea.

### Negociación interactiva entre las partes interesadas de la MLL

El proyecto de ley de la Comisión de Infraestructuras y Desarrollo de la Información (NIIP)https://proceedings.neurips.cc/paper_files/paper/2024/file/984dd3db213db2d1454a163b65b84d08-Paper-Datasets_and_Benchmarks_Track.pdf) introduce juegos de puntaje multipartíficos con **secret scores**y **minimum-acceptance thresholds**. Cada parte interesada tiene servicios públicos privados; el LLM debe inferirlos a partir de mensajes. Esta es la generalización de la negociación de dos partidos a la formación de coaliciones de partidos N. Relevante para los mercados de tareas de producción con capacidades de trabajadores heterogéneas.

> NeurIPS 2024  se ha introducido en el mercado de la tecnología de**秘密分数**Y**最低接受阈值**La mayoría de los grupos de interés tienen un uso privado; el LLM debe deducirse de la información.

### La regla de narración contra mecanismo

En todos los puntos de referencia de las negociaciones 2024-2026, la regla de ingeniería consistente es:

> Deje que el LLM narre. No deje que el LLM compute la oferta.

> 让LLM 叙述──不要让LLM 计算报价──

Si la oferta necesita ser un número (precio, ETA, cantidad), generarla deterministicamente desde el estado de negociación y que el LLM produzca el marco.

> Si la oferta requiere un número de precios, se genera de forma determinada desde el estado de negociación, se produce un marco de LLM. Si la oferta requiere una estructura de propuestas, se descompone la tarea, se distribuye el papel, se elabora, pero se realiza en función del modelo y de la cantidad de envíos.

## Construye con movimiento.
```figure
a5-og-narrator
```

## Construye el mismo

`code/main.py`los instrumentos:

- `ContractNetManager`¿ Qué ?`ContractNetTask`¿ Qué ?`Bid` gerente + licitadores, transmisión de programas, recopilación de propuestas, adjudicación.
  En inglés:`ContractNetManager`¿Qué es esto?`ContractNetTask`¿Qué es esto?`Bid` 管理者 + 投标人,广播 cfp,收集提案,授标──
- `og_narrator_bargain(state, rng)` Comprador OG-Narrador: concesión determinista de estilo Zeuthen hacia el punto medio.
  En inglés:`og_narrator_bargain` OG-Narrador 买方:确定性 Zeuthen 风格向中间点让步──
- `seller_response(state, rng)` política determinista de contratiempos de venta (la verdad estructural de los dos estilos).
  En inglés:`seller_response` 确定性卖方还价策略 (en inglés)
- `naive_llm_bargain(state, rng)` simula una negociación de LLM: elige precios con alta variación, a menudo fuera de la ZOPA.
  En inglés:`naive_llm_bargain` 模拟全 LLM 议价者:以高方差选价,经常超出 ZOPA。
- Medición: tasa de negociación de más de 1000 ensayos con precios de reserva frescos muestrados por ensayo.
  En el caso de los experimentos, el precio de la prueba es de 1000 veces.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Resultado esperado: tasa de negocio de LLM ingenuo ~65-75%; tasa de negocio de OG-Narrador ~85-95%; la brecha de 15-25 puntos es la ventaja estructural de descomponer la generación de ofertas de la narración.

> 预期输出:朴素 LLM 成交率约65-75%;OG-Narrator 成交率约85-95%;15-25 个百分点的差距是将报价生成与叙述解的结构优势──加上一个三个投标者和一个任务的合同网任务市场分配示例──

## Usalo.

`outputs/skill-bargainer-designer.md`diseña un protocolo de negociación: quién genera ofertas (determinista o LLM), quién narra, cómo se separan los scratchpads privados de los mensajes públicos y cómo se monitorea la tasa de transacciones.

> `outputs/skill-bargainer-designer.md`设计一个议价协议:谁生成报价 (quién genera oferta) 确定性 (definitividad) o LLM (Mastería de la competencia) 谁叙述,谁叙述,谁草稿本如何与公开消息分离,以及如何监控成交率──

## Envíalo .

Lista de control de las negociaciones de producción:

- **Separate scratchpad.**El Estado privado nunca llega al contexto de la contraparte.
  En inglés:**分离草稿本。**El estado privado nunca llegará a la siguiente posición de los oponentes.
- **Deterministic offer generation.**Precios, cantidades, ETA: calcular, no pedir.
  En inglés:**确定性报价生成。**价格、数量、ETA: calcular, no hacer sugerencias
- **Validate all incoming offers**Rechazar las ofertas fuera de la zona de ZOPA en el límite del protocolo.
  En inglés:**验证所有传入报价**Según el modelo, la frontera del acuerdo rechazó la oferta de ZOPA.
- **Bound rounds.**3-5 disparos máximo; escala a mediador en punto muerto.
  En inglés:**限制轮次。**Última 3-5 rutas; muerte bloqueada cuando se eleva a la regla.
- **Measure deal rate and payoff variance**Una tasa de transacción en caída es un síntoma  a menudo una deriva rápida o un ataque de contraparte.
  En inglés:**持续测量成交率和收益方差。**La baja de la tasa de conversión es un síntoma, generalmente un movimiento de la señal o un ataque de la persona.
- **Log all rejected proposals**Para los administradores de la red de contratos, los licitadores perdedores deben entender por qué.
  En inglés:**记录所有被拒绝的提案**及确定性理由── para los administradores de contratos, los candidatos a la selección deben entender las razones──

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Confirme que OG-Narrador supera a Naive-LLM en precio de la oferta. ¿Por cuánto?
   Traducción:运行`code/main.py`¿Confirmar que el narrador de OG está mejor que un LLM simple en el nivel de rendimiento?
2. Implementación **persona-based payoff improvement**(arXiv:2402.05863)  el comprador adopta un personaje "desesperado de comprar esta semana" sólo en la narración, ofrece generador sin cambios. ¿Cambia la tasa de oferta o el pago?
   Traducción: ejecutar**基于人格的收益改进**(arXiv:2402.05863) ¿Acaso la tasa de cambio o los beneficios han cambiado?
3. Implementar la cadena de pensamiento **concealment**¿Qué sucede si accidentalmente se filtra (simula al cambiar los canales)?
   Traducción:Mejoramiento de la idea**隐藏**¿Qué ocurrirá si no se desprende el plan privado de un opositor?
4. Extenda el contrato neto a la subasta de N-bidor con precio de reserva. Cuando todas las ofertas superan la reserva, ¿cómo decide el gerente entre el precio más bajo y la más alta calidad? ¿Qué regla de entrega elige y por qué?
   Cuando todas las ofertas superan el precio de retención, ¿cómo el administrador puede elegir entre el precio mínimo y la calidad máxima? ¿Cuál es la regla de concesión que elijas, por qué?
5. Lea Bhattacharya et al. 2025 en Harvard Negotiation Project metrics. Implemente dos negociación con diferentes estilos (agresivos vs. justos).
   El proyecto de la Comisión de Asuntos Exteriores de la Unión Europea (UE) se ha desarrollado en el marco de la cooperación internacional entre la Unión Europea y la Unión Europea (UE) y el Reino Unido (UE) en el marco de la cooperación internacional entre la Unión Europea y la Unión Soviética (UE).

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Contract Net / 合同网 | "Task market" / "任务市场" | Smith 1980, FIPA 1996. cfp + propose + accept/reject. The canonical task-market. / Smith 1980, FIPA 1996。cfp + propose + accept/reject。规范的任务市场。 |
| ZOPA / 可能协议区 | "Zone of possible agreement" / "可能协议区域" | Overlap between buyer's max and seller's min. Offers outside it cannot close. / 买方最大值和卖方最小值的重叠。超出此范围的报价无法成交。 |
| BATNA / 最佳替代方案 | "Best alternative to a negotiated agreement" / "谈判协议的最佳替代方案" | Your fallback if this deal fails. Sets your reservation price. / 如果交易失败的后备方案。设定你的保留价。 |
| OG-Narrator / OG-叙述者 | "Offer generator + narrator" / "报价生成器 + 叙述者" | Decomposition: deterministic offer, LLM narration. / 分解：确定性报价，LLM 叙述。 |
| Zeuthen strategy / Zeuthen 策略 | "Risk-minimizing concession" / "风险最小化让步" | Classical offer-generator that concedes based on risk limits. / 基于风险限制让步的经典报价生成器。 |
| Rubinstein bargaining / Rubinstein 议价 | "Alternating-offer equilibrium" / "交替报价均衡" | Game-theoretic model for infinite-horizon bargaining with discounting. / 带折现的无限期议价博弈论模型。 |
| CoT concealment / CoT 隐藏 | "Hide your reasoning" / "隐藏推理" | Winners in arXiv:2503.06416 kept private scratchpads; public channel shows offer only. / arXiv:2503.06416 的获胜者保持私人草稿本；公开通道只显示报价。 |
| Persona manipulation / 人格操纵 | "Emotional posturing" / "情绪姿态" | arXiv:2402.05863: ~20% payoff gain from desperation/urgency personas. / arXiv:2402.05863：绝望/紧迫人格带来约 20% 的收益增益。 |

## Más Leer más Leer más

- [NegotiationArena](https://arxiv.org/abs/2402.05863) el índice de referencia; resultados de manipulación y explotación de personas
- [Measuring Bargaining Abilities of Language Models](https://arxiv.org/abs/2402.15813) OG-Narrator y el resultado de comprador-más duro que vendedor
- [Large-Scale Autonomous Negotiation Competition](https://arxiv.org/abs/2503.06416) ~ 180 mil negociaciones; la ocultación de la cadena de pensamiento gana
- [LLM-Stakeholders Interactive Negotiation (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/984dd3db213db2d1454a163b65b84d08-Paper-Datasets_and_Benchmarks_Track.pdf) Juegos multipartíticos con utilidades secretas
- [Smith 1980 — The Contract Net Protocol](https://ieeexplore.ieee.org/document/1675516) el mecanismo clásico, IEEE Transacciones en computadoras
