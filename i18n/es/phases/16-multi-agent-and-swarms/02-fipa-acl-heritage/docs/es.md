# El legado de las leyes de FIPA-ACL y habla.

> Antes de MCP, antes de A2A, había FIPA-ACL. En el año 2000 la Fundación IEEE para Agentes Físicos Inteligentes ratificó un lenguaje de comunicación de agentes con veinte performativos, dos lenguajes de contenido y un conjunto de protocolos de interacción  contrato net, suscripción/notificación, solicitud-cuando. Se desvaneció de la industria porque la carga general de ontología era demasiado pesada para la web, pero el revival de LLM de sistemas multiagentes está reimplementando silenciosamente las mismas ideas sin la semántica formal: los contratos JSON representan los performativos, el lenguaje natural representa las ontologías. Esta lección lee en serio la FIPA-ACL para que pueda ver qué decisiones del protocolo 2026 son reinvenciones, qué son novedades, y dónde la ola actual va a redescubrir los problemas que ya resolvieron los años 2000.

> **【中文解读】**Este curso habla sobre el protocolo de comunicación de sistemas y agentes de FIPA-ACL  herencia  más  historia y evolución moderna.

> **【拓展：FIPA ACL 遗产→具体应用】**FIPA ACL (Fundación para el lenguaje de comunicación de agentes físicos inteligentes) es un estándar de comunicación de los agentes de los años 1990-2000 年代多 系统的通信标准。 Aunque FIPA 组织已解散于2013年, pero su idea central 標準化的通信原语如INFORM、REQUEST、PROPOSE) todavía afecta al protocolo de agentes de los años 2026 协议 A2A 协议 puede ser considerado como el LLM 时代重生 FIPA ACL.

> ¿ Qué es esto ?**【前置】**Previo curso Previo curso Previo curso Previo dominio:Fase 16·01 ((¿qué hace falta más agente) Fase 13 ((MCP/ protocolo de instrumentos)  本课是历史课理解FIPA ACL 才能看懂 2026 协议(MCP/A2A/ACP) 是重新发明还是真创新──

> ¿ Qué es esto ?**【类比】**FIPA-ACL = "AI 界的拉丁语"── 2000 años de estándar,2026 años de acuerdo(MCP/A2A) en gran cantidad heredado su idea──区别:FIPA 用形式化本体(重)、现代协议用 JSON+自然语言(轻)──学历史的价值:避免重复覆FIPA 因为"本体太重"而死,现代协议要保持轻量──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 01 (Why Multi-Agent) | **前置知识:** Phase 16 · 01（为什么需要多 Agent）
**Time:** ~60 minutes | **时间:** 约 60 分钟

## # El problema # # El problema #

> **【中文解读】**El acuerdo de 2026 parece estar en plena implementación, el proceso de implementación de los nuevos protocolos de hace 20 años se encuentra en el proceso de adopción de un nuevo acuerdo.

El panorama del protocolo de agentes para 2026 está ocupado: MCP para herramientas, A2A para agentes, ACP para auditoría empresarial, ANP para confianza descentralizada, NLIP para contenido en lenguaje natural, además de CA-MCP y dos docenas de propuestas de investigación.

> El 2026 es un año de gran éxito en el ámbito del protocolo de agentes: el MCP se utiliza para herramientas, el A2A se utiliza para agentes, el ACP se utiliza para auditoría empresarial, el ANP se utiliza para descentralización de la confianza, el NLP se utiliza para el contenido de lenguaje natural, y el CA-MCP y más de veinte propuestas de investigación.

La lectura honesta es que la mayoría de ellos están redescubriendo un árbol de decisión muy específico de veinte años. La teoría del habla-acto de Austin (1962) y Searle (1969) nos dio "las declaraciones son acciones". KQML (1993) convirtió eso en un protocolo por cable. FIPA-ACL (ratificado en 2000) produjo la normalización de referencia: veinte performativos, lenguajes de contenido SL0/SL1, protocolos de interacción para la red de contratos y suscripción-notificación. JADE y JACK fueron las plataformas de referencia de Java. El esfuerzo se desvaneció alrededor de 2010 porque la carga de ontología era demasiado pesada y la web estaba ganando.

> La mayoría de ellas están redescubriendo un árbol de decisión muy específico de hace veinte años. La teoría del comportamiento de palabras de Austin (1962) y Searle (1969) nos dice que "la palabra es la acción" KQML (KQML) 1993 se convertirá en un acuerdo de línea (FIPA-ACL) (Ratificación 2000) generó una estandarización de referencia: veinte obras de comportamiento, lenguaje de contenido SL0/SL1 (Content Language SL0/SL1) para el contrato de red y el acuerdo de intercambio de suscripciones-informática (BIS). JADE y JACK es una plataforma de referencia de Java (Java).

Cuando miras a MCP's `tools/call`En el ciclo de vida de las tareas de A2A, o en el almacén de contexto compartido de CA-MCP, se observa una reaparición más suave y nativa de las decisiones de FIPA.

> Cuando usted revise MCP `tools/call`Cuando se guarda el archivo de misiones en el ciclo de vida de A2A o CA-MCP, se ve que FIPA es más flexible en la toma de decisiones, y que JSON es la base de la historia.

## Concepto de la esencia de la concepción

> **【中文解读】**Este es el primer libro de la serie de estudios de la Universidad de California en la que se trata de la investigación de la lengua inglesa.

### Acta de discusión, en un párrafo

> **【中文解读】**Una frase habla claro en la teoría de la base: algunas frases no están en la descripción del mundo, sino en el cambio del mundo. Searle las divide en cinco categorías; KQML Coloca este concepto de filosofía en un acuerdo de línea de software ejecutable; FIPA-ACL  finales de estandarización. Todos los protocolos de agentes modernos son la última generación de esta cadena.

Austin notó que algunas frases no describen el mundo, lo cambian. "Lo prometo". "Pido". "Declaro". Llamó a estas declaraciones performativas. Searle formalizó cinco categorías: asertivo, directivo, comisionado, expreso y declarativo. KQML (Finin et al., 1993) hizo que esto funcione para los agentes de software: un mensaje es un performativo (la acción) más contenido (de qué se trata la acción). FIPA-ACL limpió las lagunas de KQML y estandarizó alrededor de veinte performativos.

> Austin nota que algunas frases no describen el mundo ellos cambian el mundo―"mi compromiso―""mi petición―""mi anuncio―" él llama a estas palabras para construir conversaciones―Searle la formalizó en cinco categorías: aserción, orden, compromiso, expresión, anuncio, KQML 

### Los veinte performativos de la FIPA (lista parcial)

| Performative | Intent |
|---|---|
| `inform` | "I tell you P is true" |
| `request` | "I ask you to do X" |
| `query-if` | "Is P true?" |
| `query-ref` | "What is the value of X?" |
| `propose` | "I propose we do X" |
| `accept-proposal` | "I accept the proposal" |
| `reject-proposal` | "I reject the proposal" |
| `agree` | "I agree to do X" |
| `refuse` | "I refuse to do X" |
| `confirm` | "I confirm P is true" |
| `disconfirm` | "I deny P" |
| `not-understood` | "Your message did not parse" |
| `cancel` | "Cancel the ongoing X" |
| `cfp` | "Call for proposals on X" |
| `subscribe` | "Notify me when X changes" |
| `failure` | "I tried X and failed" |

La lista completa está en `fipa00037.pdf`El punto no es memorizarlo. El punto es que cada uno de estos corresponde a un protocolo primitivo que un LLM eventualmente re-agrega.

> 完整列表在 `fipa00037.pdf`(FIPA ACL 消息结构) 中── El enfoque no está en la memoria sino en que cada uno de los participantes se enfrenta a un acuerdo LLM 最终会重新添加的原语──

### Mensaje canónico FIPA-ACL

> **【中文解读】**Sólo hay siete cartas y una más.`content`¿Qué es eso?`conversation-id`Y `reply-with`Es la petición de respuesta a los cambios de la lengua original.

```
(inform
  :sender       agent1@platform
  :receiver     agent2@platform
  :content      "((price IBM 83))"
  :language     SL0
  :ontology     finance
  :protocol     fipa-request
  :conversation-id   conv-42
  :reply-with   msg-17
)
```

Se trata de siete campos que contienen el envase del protocolo; un campo (`content`El resto de campos son exactamente lo que reinventas cada vez que puestas retemplajes, threading y ontología en un protocolo JSON.

> 七个字段承载协议信封; una字段(`content`) Cargar carga efectiva. El resto de los segmentos es exactamente lo que volverás a probar cada vez.

### Las dos plataformas heredadas

**JADE**(Java Agent DEvelopment framework, 19992020s) fue el tiempo de ejecución más utilizado de conformidad con FIPA. Los agentes extendieron una clase base, intercambiaron mensajes ACL, se ejecutaron dentro de contenedores y se coordinaron utilizando "comportamientos".

> **JADE**(Java Agent 开发框架, 1999-2020 年代) es el FIPA 兼容运行时.                                                                                                                                                                                                                                                    

**JACK**(Software orientado a agentes, comercial) enfatizó el razonamiento BDI (Creencia-Deseo-Intención) en la parte superior de los mensajes FIPA.

> **JACK**(Software orientado a agentes, productos comerciales) enfatizó en la FIPA 消息之上 llevar a cabo BDI (confianza- deseo-intención)

Ambos disminuyeron una vez que la pila web comió casos de uso de múltiples agentes. MCP y A2A son los "contenedores" de tiempo de ejecución de 2026.

> Una vez que la tecnología web ha absorbido a muchos agentes, por ejemplo, ambos se han ido desmoronando.

### Por qué la FIPA se desvaneció

- **Ontology overhead.**La FIPA requirió una ontología compartida para analizar `content`El acuerdo sobre ontologías es un proceso de estándares de años.
  En inglés:**本体开销。**FIPA  necesita compartir este análisis `content` En el interior de la web se ha logrado un acuerdo que ha sido un proceso de estandarización de varios años.
- **Formal semantics nobody used.**SL (Lenguaje Semántico) dio condiciones de verdad rigurosas, pero la mayoría de los sistemas de producción utilizaban contenido de forma libre e ignoraba el formalismo.
  En inglés:**没人用的形式语义。**SL (语义语言) proporciona condiciones de verdadero valor estrictas, pero la mayoría de los sistemas de producción utilizan el contenido de forma libre y ignoran el formalismo.
- **Tooling lock-in.**JADE era solo para Java, JACK era comercial, y los equipos poliglotes se desplazaban alrededor de ambos.
  En inglés:**工具锁定。**JADE 仅支持Java;JACK 是商业的──多语言团队绕过了两者──
- **The internet won the stack.**REST, luego JSON-RPC, luego gRPC reemplazó el transporte de ACL.
  En inglés:**互联网赢得了技术栈。**REST, luego JSON-RPC, luego gRPC sustituyó la transmisión de ACL.

### El revival de la LLM es FIPA-lite

> **【中文解读】**¿ Cuál es el número de personas que se encuentran en el mercado ?`request`y MCP `tools/call`Y排放: 同一个信封(谁、对谁、意图、载荷、关联 id), diferentes语法──Liu 等 2025 综述明确给出谱系映射:MCP=工具使用语行为,A2A=Agent对等言语行为,ACP=审计轨迹言语行为,ANP=去中心化身份扩展──新规范都是JSON语法、更松语义的ACL 后代──

Comparar una FIPA `request`a un MCP `tools/call`¿Qué es esto ?

> El FIPA `request`Con el MCP`tools/call` hacer comparación:

```
(request                                {
  :sender  agent1                         "jsonrpc": "2.0",
  :receiver tool-server                   "method":  "tools/call",
  :content "(lookup stock IBM)"           "params":  {"name":"lookup_stock",
  :ontology finance                                   "arguments":{"symbol":"IBM"}},
  :conversation-id c42                    "id": 42
)                                        }
```

El mismo sobre, diferente sintaxis. Ambos llevan: quién, quién, intención, carga útil, correlación id. Ninguno es una revolución sobre el otro  son diferentes compromisos en el mismo diseño.

> La misma enciclopedia, diferentes idiomas. Ambas tienen un mismo diseño.

La encuesta de 2025 de Liu et al. ("Una encuesta de protocolos de interoperabilidad de agentes: MCP, ACP, A2A, ANP", arXiv:2505.02279) hace que este linaje sea explícito: MCP corresponde a actos de habla de uso de herramientas, A2A a actos de habla de agentes-peer, ACP a actos de habla de auditoria, ANP a extensiones de identidad descentralizada.

> Liu 等人 2025 综述("Agent 互操作性协议综述:MCP, ACP, A2A, ANP",arXiv:2505.02279) señala claramente este linaje:MCP a las herramientas de tratamiento de uso de palabras, A2A a los agentes de tratamiento de otros comportamientos de habla, ACP a las auditorías de trayectoria de habla, ANP a la expansión de la identidad de tratamiento descentralizado.

### El compromiso, declarado claramente

> **【中文解读】**权衡要明说:FIPA 给形式语义(可证明) 规范施事行为目录(no necesita discutir) 带正确性保证的交互协议模式;现代规范给 JSON 原生载荷、自然语言内容、Web 传输、能力发现──交换的就是"更松散的意图语义换更容易实现"──

**What FIPA gave you and modern specs drop:**

> **FIPA 给你的而现代规范丢弃的：**

- Semántica formal  puedes probar `inform`implica que el remitente cree el contenido.
  En inglés, "Formación de expresión" se puede demostrar.`inform`Significa que el enviador cree en el contenido.
- Un catálogo canónico de performativos  no tienes que volver a argumentar "deberíamos tener un `cancel`¿Qué es eso?
  No hay que volver a discutir.`cancel`¿Qué es esto?"
- Décadas de patrones de interacción-protocolo  contrato-red, suscripción-notificación, propuesta-acepción  con propiedades de corrección conocidas.
  China 訳: decennial 交互协议模式合同网、订阅-通知、提议-接受具有已知的正确性属性──

**What modern specs give you and FIPA did not:**

> **现代规范给你的而 FIPA 没有的：**

- Cargas útiles nativas de JSON compatibles con todas las herramientas modernas.
  Traducción:JSON original y válida carga.
- Contenido en lenguaje natural que los LLM puedan interpretar sin una ontología codificada a mano.
  El lenguaje natural puede ser interpretado sin el código manual.
- Transporte de la pila web (HTTP, SSE, WebSocket).
  En inglés, el nombre de la red de Internet es "Web" (en inglés: Web 技术传输) y el nombre de la red de Internet es "Web Socket").
- Descubrimiento de la capacidad a través de MCP en vivo `server/discover`y las tarjetas de agente A2A.
  Por el tiempo MCP`server/discover`Y tarjeta de agente A2A  realizar la capacidad de detección.

Se trata de una semántica de intención más flexible para una implementación más fácil.

> Más relajado de la intención de lograr una realización más fácil.

### Protocolos de interacción que valgan la pena llevar

> **【中文解读】**FIPA 约15 交互协议里,三个值搬进 LLM 多 Agent 系统:合同网:任务市场模式,应应阶段16·16 协商) 订阅/通知(每个事件总线) 请求-当(持久工作流引擎的延迟任务,应阶段16·22) 它们都能干净映射到现代消息队列、HTTP + 轮询或 SSE 流──

FIPA envió ~ 15 protocolos de interacción. Tres son dignos de llevar adelante en sistemas multi-agentes LLM:

> La FIPA ha publicado unos 15 acuerdos de intercambio. Tres de ellos deben prolongarse hasta el LLM en el sistema de múltiples agentes:

1. **Contract Net Protocol (CNP).**Cuestiones de gerente `cfp`(llamada a presentar propuestas); los licitadores responden con `propose`El director acepta/rechaza. Este es el patrón canónico del mercado de tareas (fase 16 · 16 de negociación).
   En inglés:**合同网协议 (CNP)。**管理者发布 `cfp`(征求提案);投标者用 `propose`响应;管理者接受/拒绝──这是典型任务市场模式(Fase 16 · 16 协商)──
2. **Subscribe/Notify.**El suscriptor envía `subscribe`El editor envía `inform`Esto es cada evento-bus en 2026.
   En inglés:**订阅/通知。**订阅者发送   suscriptores`subscribe`; editor en el tema cambio en el envío `inform`Es la línea de eventos de cada año de 2026.
3. **Request-When.**"Hacer X cuando la condición Y se mantiene". Acción retrasada con condiciones previas. El analógico 2026 es tareas diferidas en motores de flujo de trabajo duraderos (Fase 16 · 22 Escalado de producción).
   En inglés:**请求-当。**"Cuando se establezcan las condiciones Y  ejecutar X¬" con las condiciones de prepuestación de la demora de la acción ⋅2026 años de similar es la demora de la tarea en el motor de la duración del trabajo ⋅Fase 16 · 22

Cada uno de ellos hace un mapa limpio en las colas de mensajes modernas, encuestas HTTP + o streaming SSE.

> Cada uno puede ser claramente mapeado hasta la línea de noticias moderna, HTTP + 轮询 o SSE 流.

### ¿Qué se rompe cuando dejas de lado la ontología

> **【中文解读】**El precio de perder el cuerpo es**语义漂移**Dos agentes tienen conceptos muy diferentes para el mismo término "cliente", y el receptor se basa en un error de comprensión de la acción, mientras que el esquema verificador no se mantiene.`content`Siguen siendo más fáciles de usar.

Sin una ontología compartida, los agentes deducen el significado del contenido del lenguaje natural.**semantic drift**: dos agentes usan la misma palabra (`"customer"`En el caso de los conceptos sutilmente diferentes, el agente del receptor actúa sobre la interpretación errónea, ningún validador de esquema lo capta.

> 没有共享本体,Agent de contenido de lenguaje natural 推断含义──记录在案的2026年失败模式是**语义漂移**Dos agentes para el mismo palabra`"customer"`) hay conceptos muy diferentes, el receptor agente se basa en una acción de comprensión errónea, no hay un modelo de verificador que pueda captarlo.

Mitigations sin entrar en ontología completa:

> No utilizar completamente las medidas de alivio del cuerpo:

- Esquema JSON en `content` rechaza los errores estructurales en el cable.
  En español:`content`Utiliza JSON Schema en la transmisión de la capa rechazar errores estructurales
- Los artefactos de tipo (A2A)  rechazan la modalidad incorrecta.
  En inglés, el método de cálculo de la estructura de los componentes de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura.
- El performativo explícito en el sobre  hace que la intención sea inequívoca incluso cuando el contenido es lenguaje natural.
  El contenido de la obra es claro, aunque sea en lenguaje natural.

### Las especificaciones de 2026, mapeadas a la herencia del habla-acto

| Modern spec | FIPA analog | What it keeps | What it drops |
|---|---|---|---|
| MCP `tools/call` | `request` | explicit intent, correlation id | formal semantics, ontology |
| MCP `resources/read` | `query-ref` | explicit intent, correlation id | formal semantics |
| A2A Task lifecycle | contract-net + request-when | async lifecycle, state transitions | formal completeness guarantees |
| A2A streaming events | subscribe/notify | async push | typed-predicate subscription |
| CA-MCP shared context | blackboard (Hayes-Roth 1985) | multi-writer shared memory | logical consistency model |
| NLIP | natural-language content | LLM-native | schema |

Leyendo la tabla de arriba a abajo, el patrón es: mantener la estructura primitiva, dejar el formalismo, dejar que LLM se sobrepongan a la ambigüedad.

> Desde arriba hasta abajo, el modelo es: conservar la estructura original, abandonar el formalismo, hacer LLM 弥补模糊性.

> **【中文解读】**Una frase总结全表:2026 规范保留的是结构性原语(显式意图、关联 id、异步生命周期), se pierde el formalismo(形式语义、本体、逻辑一致性), se completa el diferencial con la capacidad de interpretación del LLM.

```figure
sw-contract-net
```

## Construye y realiza.

> **【中文解读】**Ejemplo Código es una biblioteca de normas FIPA-ACL  Traducidor:把五条 MCP/A2A 风格消息编码成 FIPA-ACL 再解码回来,并跑一个"un administrador + tres candidatos"玩具合同网协商──输出并排展示同一消息的2026 JSON 形态和FIPA-ACL 形态和一些协议原语在往返中存活,只有语法不同──

`code/main.py`Implementa un traductor FIPA-ACL de pure-stdlib. Encodifica y decodifica el envase ACL canónico y muestra cómo cada forma de mensaje MCP / A2A se reduce a los mismos siete campos.

> `code/main.py`实现 una pura biblioteca de normas FIPA-ACL 翻译器──它编解码标准ACL 信封,并展示每个MCP / A2A 消息形状如何简化为相同七段──演示内容:

- Enciende cinco mensajes de estilo MCP y A2A como FIPA-ACL.
  China 翻译:将将五个 MCP 风格和 A2A 风格的消息编码为FIPA-ACL。
- Decodifica FIPA-ACL de nuevo al equivalente moderno.
  El texto original de la ley de la ley de los Estados Unidos de América (FIPA-ACL) se traduce en la forma oficial de la ley de los Estados Unidos de América (FIPA-ACL) en el texto original de la ley de los Estados Unidos de América.
- Se ejecuta un contrato de juguete Negociación de red entre un gerente y tres licitadores utilizando `cfp`¿ Qué ?`propose`¿ Qué ?`accept-proposal`¿ Qué ?`reject-proposal`¿ Qué ?
  En inglés:`cfp`¿Qué es esto?`propose`¿Qué es esto?`accept-proposal`¿Qué es esto?`reject-proposal`Entre un administrador y tres candidatos se lleva a cabo una negociación de un contrato de juego.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

La salida es una pista lado a lado que muestra cada mensaje moderno tanto en su forma JSON 2026 como en su forma FIPA-ACL, luego una vuelta de una oferta de red de contrato. Los mismos protocolos primitivos sobreviven a la vuelta de viaje; solo la sintaxis difiere.

> 输出是一个并排追踪, muestra cada 条现代消息的 2026 JSON 形式和 FIPA-ACL 形式, luego es el contrato 网投标标的往返──

## Usalo con el marco de ejecución

`outputs/skill-fipa-mapper.md`La técnica de la información de base de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de`inform`¿Con la sintaxis JSON?"

> `outputs/skill-fipa-mapper.md`Es una habilidad, leer cualquier agente  protocolo 规范并生成 FIPA-ACL 映射.`inform`¿Qué es eso?

## Envíe el producto .

> **【中文解读】**No resucitar FIPA-ACL, llevarlo de vuelta a su lista de verificación:意图原语、关联 id、明顯内容语言、一等公民的交互协议、语义漂移预案── cualquier nuevo protocolo en producción, primero responder a estas cinco preguntas──

No traiga a FIPA-ACL de vuelta.

> No vuelvas a traer el FIPA-ACL.

- ¿Cuál es la intención primitiva (performativa) de cada mensaje?
  Traducción:El mensaje de la historia es que el mensaje es un mensaje.
- ¿Hay una identificación de correlación para la solicitud-respuesta y cancelación?
  ¿Hay algún tipo de ID de conexión para solicitar-respondiendo y cancelar?
- ¿Existe un lenguaje de contenido explícito (JSON-RPC, texto plano, artefacto de tipografía estructurado)?
  ¿Hay algún tipo de contenido en lenguaje de texto estructurado?
- ¿Son los protocolos de interacción de primera clase, o están re-implementando el contrato-net desde cero?
  El protocolo de intercambio es un acuerdo de igualdad de ciudadanos, ¿o estás empezando a re-realizar el contrato?
- ¿Qué sucede cuando dos agentes no están de acuerdo sobre el significado del contenido (drift semántico)?
  Cuando dos agentes tienen diferencias en el contenido ¿qué sucede cuando se transfiere el contenido?

Documenta estas cinco preguntas para cualquier nuevo protocolo antes de enviarlo a la producción.

> Antes de publicar cualquier nuevo protocolo hasta el medio de producción, registre estos cinco problemas.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Observar la codificación de ida y vuelta. Identificar qué performativo FIPA corresponde a `tools/call`¿ Qué ?`resources/read`, y la creación de tareas A2A.
   Traducción:运行`code/main.py` observar y volver a codificar  identificar qué comportamiento de la FIPA se debe aplicar `tools/call`¿Qué es esto?`resources/read`Y A2A 任务创建――
2. Extenda la demostración de la red de contratos con un `cancel`El ejecutivo puede retirar la tarea en medio de la oferta.`cancel`¿No resolverá eso por sí solo?
   En inglés:`cancel`施事行为扩展合同网演示, para que el administrador pueda retirar las tareas en el medio de la oferta.`cancel`¿Solvió una situación de fallas que no se resolvió por el solo intento de volver a resolver?
3. Leer la estructura de mensajes de la FIPA ACL (http://www.fipa.org/specs/fipa00037/) secciones 4.14.3. escoge una performativa no cubierta en esta lección y describa su análogo moderno JSON-RPC.
   La ley de la FIPA ACL 消息结构(http://www.fipa.org/specs/fipa00037/）第4.1-4.3 节──选择本课未涵盖的一个施事行为并描述其现代 JSON-RPC类比──
4. Lee Liu et al., arXiv:2505.02279. Para cada uno de los MCP, A2A, ACP, ANP, enumere las familias performativas FIPA que mantienen y dejan.
   Para cada uno de los MCP, A2A, ACP, ANP, lista sus reservas y desechas de FIPA 施事行为族──
5. Diseñar un esquema JSON mínimo para el `content`campo de una `request`¿Qué es lo que ese esquema te da que el lenguaje natural puro no, y cuánto cuesta?
   Por tu propio sistema .`request`施事行为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `content`字段设计一个最小的JSON-Schema. Este modelo te proporciona un lenguaje puro natural.

## Términos clave .

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| Speech act | "An utterance that does something" | Austin/Searle: utterances as actions. The theoretical parent of ACL. | 言语行为 |
| FIPA | "That old XML thing" | IEEE Foundation for Intelligent Physical Agents. Standardized ACL in 2000. | FIPA 基金会 |
| ACL | "Agent Communication Language" | FIPA's envelope format: performative + content + metadata. | Agent 通信语言 |
| Performative | "The verb" | The intent class of a message: `inform`, `request`, `propose`, `cfp`, etc. | 施事行为 |
| KQML | "FIPA's predecessor" | Knowledge Query and Manipulation Language (1993). Simpler, narrower. | KQML |
| Ontology | "Shared vocabulary" | A formal definition of the concepts the content language talks about. | 本体 |
| SL0 / SL1 | "FIPA content languages" | Semantic Language levels 0 and 1 — the formal content language family. | SL 内容语言 |
| Contract Net | "Task market" | Manager issues cfp; bidders propose; manager accepts. The canonical interaction protocol. | 合同网 |
| Interaction protocol | "Pattern of messages" | A sequence of performatives with known correctness: request-when, subscribe-notify, etc. | 交互协议 |

## Más Leer más Leer más

- [Liu et al. — A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP](https://arxiv.org/html/2505.02279v1) la encuesta canónica de 2025 que conecta las especificaciones modernas con el patrimonio de la FIPA
  China                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
- [FIPA ACL Message Structure Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/) el formato del envase 2000 ratificado
  Chino:FIPA ACL 消息结构规范2000年批准的信封格式
- [FIPA Communicative Act Library Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/) el catálogo completo de la interpretación
  Chino:FIPA 通信行为库规范完整的施事行为目录
- [MCP specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) el equivalente actual de uso de herramientas sin estado de `request`- ¿ Qué ?`query-ref`
  El programa de trabajo de la Comisión de Educación (MCP) 2026-07-28 规范`request`- ¿ Qué ?`query-ref`de la actualidad sin estado de herramientas uso igual efecto
- [A2A specification](https://a2a-protocol.org/latest/specification/) el equivalente moderno de agente-para-par de contrato-net y suscriptor-notificar
  En inglés: A2A 规范合同网和订阅通知的现代代理对等效
