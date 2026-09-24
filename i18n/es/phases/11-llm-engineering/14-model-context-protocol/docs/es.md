# Modelo de Protocolo Contextual (MCP) 模型上下文协议

> MCP le da a un host de IA un protocolo para descubrir e invocar herramientas, recursos y instrucciones. La revisión 2026-07-28 hace que ese protocolo sea estatal: la capacidad y el contexto de la versión viajan con cada solicitud, no en un apretón de manos vinculado a la conexión.

> **【中文解读】**MCP  da a la AI un conjunto de protocolos unificados para encontrar y utilizar herramientas, recursos y sugerencias. Modelo de ideas.

> **【拓展：MCP→Phase 13 深入路线】**Este curso es el primer contacto sistémico de MCP: dar un modelo de protocolo y una realización mínima operable.

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:(1) Fase 11·09(Llamada de función) 理解工具调用基础;(2) Fase 11·03(Outputs estructurados) 理解 JSON Schema;(3) JSON-RPC 2.0 基本概念(请求/响应/通知)―旧版教程里 `initialize`握手和                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `Mcp-Session-Id`Se ha eliminado el discurso en la nueva normativa. Si has aprendido la versión anterior, primero borra estos recuerdos.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 03 (Structured Outputs) | **前置知识:** Phase 11 · 09（函数调用）、Phase 11 · 03（结构化输出）
**Time:** ~75 minutes | **时间:** 约 75 分钟

## Objetivos de aprendizaje

- Distinguir un host MCP, cliente, servidor, transporte y servidor primitivo.
  En el caso de los servicios de transporte, el servicio de transporte es el servicio de transporte.
- Construir una solicitud JSON-RPC con los metadatos requeridos por MCP 2026-07-28.
  Construir con MCP 2026-07-28 necesariamente para obtener datos de JSON-RPC
- Usar`server/discover`para inspeccionar versiones, identidad y capacidades.
  En inglés:`server/discover`探测服务器的版本、身份与能力── también se puede utilizar para la búsqueda de datos.
- Retorna los resultados de las herramientas, recursos y instrucciones.
  Traducción:Desde herramientas, recursos y sugerencias regresar con los resultados de los tipos de marcas y de las sugerencias de caché.
- Explica cómo el MCP sin estado moderno interactúa con los servidores de la era de apretones de manos.
  Traducción:MCP 如何与握手时代的旧服务器互操作.
- Elija el estado seguro, el transporte y los límites de aprobación para un servidor.
  China: 译文:为服务器选择安全的状态、传输与审批边界──

## El problema es la introducción del problema

Su aplicación necesita una consulta de base de datos, una operación de calendario y un lector de archivos. Sin un protocolo compartido, cada host de IA necesita descubrimiento personalizado, invocación, errores, transporte y pegamento de autorización para esas mismas capacidades.

> Su aplicación necesita consultas de base de datos, operaciones de calendario y lectura de documentos. Cuando no hay un acuerdo de intercambio, cada anfitrión de IA debe tener la misma capacidad de redactar un código de descubrimiento, manipulación, error, transmisión y autorización.

MCP reduce esa matriz de integración. Un servidor publica una superficie JSON-RPC estándar. Un cliente compatible puede descubrir la superficie, presentarla a un modelo o usuario, invocarla e interpretar el resultado sin un adaptador específico para el servidor.

> MCP comprimió esta matriz integrada. El servidor emitió una interfaz estándar JSON-RPC.

El MCP estándariza la comunicación. No decide a qué herramienta debe llamar el modelo, hacer que el contenido no confiable sea seguro o convertir una solicitud sin estado en un estado de aplicación duradero.

> Un límite clave fácilmente ignorado: el MCP sólo estándariza la comunicación. No decide qué herramienta debe utilizarse, no hará que el contenido de incrédulo sea seguro, ni convertirá las solicitudes sin estado en un estado de aplicación permanente. Estas decisiones siguen siendo propiedad de su anfitrión y servidor.

> ¿ Qué es esto ?**【类比】**MCP 像"电源插座国标"── cuando no hay un sello nacional, cada dispositivo eléctrico tiene un tipo de conexión, de vez en cuando el país debe comprar una conexión eléctrica; tiene un sello nacional, un sistema eléctrico. Pero el sello nacional no se preocupa por si se instala el soporte eléctrico o el uso de la seguridad eléctrica.

## El concepto central.

![MCP host, stateless request, and server primitives](../assets/mcp-architecture.svg)

### Los tres servidores primitivos.

1. **Tools**Cada herramienta tiene un nombre, descripción, entrada de esquema JSON y manipulador.
2. **Resources**se nombran, contenido dirigido a URI que un cliente puede leer.
3. **Prompts**son plantillas reutilizables que un host puede exponer a un usuario.

El host es la aplicación de IA. Un cliente MCP dentro de ese host habla a un servidor. El transporte lleva mensajes JSON-RPC entre ellos.

> Host es una aplicación de IA en sí misma; un cliente MCP dentro del host sólo conversa con un servidor; la transmisión de la capa entre ambos se traslada JSON-RPC 消息──注意"客户端: server = 1:1"需要多个服务器当就挂多个客户端──

### Las solicitudes de apatrida reemplazan el apretón de manos.

> **【中文解读】**Este es el mayor cambio en la nueva versión de la norma:`initialize`La mano en la mano,`notifications/initialized`Y el acuerdo de todos los miembros de la comunidad se ha movido.`params._meta`(协议版本、客户端能力、客户端身份)`_meta`、 falta de necesidad de llenar 字段或类型不对 → `-32602`; versión en formato legal pero servidor no apoya → `-32022`¿Qué es eso?

MCP 2026-07-28 se elimina `initialize`y `notifications/initialized`También elimina las sesiones a nivel de protocolo.`params._meta`¿Qué es esto ?

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "lesson-client",
        "version": "1.0.0"
      }
    }
  }
}
```

Se requiere la versión del protocolo y las capacidades del cliente.`_meta`, un campo requerido faltante, o un campo requerido con el tipo incorrecto se malforma y devuelve Parámetros inválidos (`-32602`). Una cadena de versiones bien formada que el servidor no admite devuelve `UnsupportedProtocolVersionError`(El artículo`-32022`Un servidor puede procesar una solicitud válida sin recuperar un registro de negociación previo.

Estatal no significa que una aplicación nunca pueda mantener el estado.`Mcp-Session-Id`Si un flujo de trabajo necesita continuidad, el servidor acuña un mango opaco y el cliente pasa ese mango como un argumento de herramienta ordinario en llamadas posteriores.

> "Sin estado" no es equivalente a que la aplicación no puede tener estado, sino que el estado no puede estar en MCP  conexión o `Mcp-Session-Id`后面──工作流需要连续性时,由服务器发发发一句不透明柄 (en inglés: workflow needs continuity) 后面──工作流需要连续性时,由服务器发发发发一句不透明句柄 (en inglés: workflow needs continuity), el cliente en el posterior uso lo considera como un instrumento ordinario.

> ️ **【易错点】**El código antiguo mantiene los datos de los clientes en el "objetos conectados" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto conectado" en el "objeto" en el "objeto de la "objeto" en el "objeto" en el "objeto" en el "objeto" en el "objeto" en el "objeto" en el "objeto" en el "objeto" en el "objeto" en el "objeto" en el "objeto" en el "objeto" en el "objeto" en el "objeto" en el "objeto" en el "objeto" en el "objeto de la "objeto" en el "objeto" en el "objeto de la "objeto" en el "objeto".`_meta`, la solicitud de la empresa se rechazó directamente. Cada solicitud debe reconstruirse.

### Descubrimiento y selección de versiones

> **【中文解读】** `server/discover`Es un método obligatorio de la nueva versión del servidor: devolver la versión compatible, capacidades y condición de servidor, y llevar`ttlMs`- ¿ Qué ?`cacheScope`缓存提示──双时代客户端在studio 上先用 `server/discover`探测: recibieron resultados descubiertos o identificables modernos errores`-32022`) se explica que el servidor moderno; encontrarse con errores irreconocibles o supertiempo sólo permite regresar a 2025-11-25 `initialize`El proceso 旧流程是兼容代码, no es moderno默认.

Cada servidor moderno implementa`server/discover`. El resultado anuncia las versiones, capacidades y identidad del servidor:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "complete",
    "supportedVersions": ["2026-07-28"],
    "capabilities": {
      "tools": {},
      "resources": {},
      "prompts": {}
    },
    "ttlMs": 3600000,
    "cacheScope": "public",
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "demo-server",
        "version": "1.0.0"
      }
    }
  }
}
```

Un cliente puede llamar a otro método directamente y manejar un error de versión, pero el descubrimiento hace que la visualización de la capacidad y la selección de la versión sean explícitas. Una versión no soportada devuelve `UnsupportedProtocolVersionError`con código `-32022`Sus datos contienen`supported`, una serie de revisiones del servidor, y `requested`, la revisión rechazada.

En el estudio, un cliente de doble era investiga con`server/discover`Un resultado de descubrimiento o un error moderno reconocido como`UnsupportedProtocolVersionError`Cualquier error o tiempo de espera que no sea reconocido como moderno permite regresar al 2025-11-25`initialize`El comportamiento heredado es código de compatibilidad, no el estándar moderno.

### Los resultados son explícitos.

> **【中文解读】**Cada resultado central está con él.`resultType`¿Qué es esto ?`complete`(操作完成) o `input_required`(necesita que el cliente vuelva y vuelva según el modelo MRTR; el servidor central sólo permite que el cliente vuelva y vuelva según el modelo MRTR)`tools/call`¿Qué es esto?`resources/read`¿Qué es esto?`prompts/get`里返回它) ∼ 旧式省略 `resultType`Los resultados deben estar en orden.`complete`处理──列表/读取结果还带 `ttlMs`Con`cacheScope` determinación de la orden + nueva información de la información que permite al cliente almacenar en caché, y aumentar la caché rápida

Cada núcleo de 2026-07-28 resultado tiene`resultType`¿Qué es esto ?

- `complete`significa que la operación ha terminado.
- `input_required`significa que el servidor necesita otra vuelta a través del patrón de solicitudes de viaje múltiple. los servidores centrales pueden devolverlo sólo desde `tools/call`¿ Qué ?`resources/read`, o`prompts/get`¿ Qué ?

Los clientes deben tratar un resultado heredado que omita `resultType`tan completo.

Los servidores deben incluir `io.modelcontextprotocol/serverInfo`en cada resultado `_meta`Esta identidad es auto-relatada y es para visualización, registro y depuración, no para decisiones de seguridad.

También se incluyen la lista y los resultados de lectura `ttlMs`y `cacheScope`- Un determinista .`tools/list`orden más un indicio de frescura permite a los clientes almacenar el descubrimiento en caché de forma segura y mejora la estabilidad de caché rápido. `cacheScope: public`Permiten almacenamiento en caché compartido; `private`La aplicación de la ley de la información en el mercado interior se limita a la reutilización en el contexto de la llamada.

### El formato de cable y el transporte.

> **【中文解读】**线格式仍然是JSON-RPC 2.0。现代 Streamable HTTP 只暴露一个接受 POST的端点,每条 JSON-RPC消息独立一个 POST;请求 POST的响应是一个 JSON对象或一条请求级 SSE流;通知 POST被接受时返回 HTTP 202 空响应体──2026-07-28 里没有独立 GET 流、没有 DELETE 会话端点、没有`Mcp-Session-Id`No hay.`Last-Event-ID`重放长期变更通知改用 `subscriptions/listen`POST(Respuesta para mantener abierto el SSE 流)

MCP utiliza JSON-RPC 2.0 en stdio o HTTP transmitible.

- Una solicitud tiene `jsonrpc`¿ Qué ?`id`¿ Qué ?`method`, y `params`¿ Qué ?
- Una respuesta tiene la coincidencia`id`y de cualquier otro`result`o `error`¿ Qué ?
- Una notificación no tiene `id`y no espera ninguna respuesta.

Un POST de solicitud recibe un objeto JSON o un flujo de eventos enviados por servidor con escala de solicitud que termina con la respuesta final. Una notificación aceptada POST recibe HTTP 202 sin cuerpo de respuesta; esta revisión central no define notificaciones de cliente a servidor sobre HTTP de transmisión.

No hay un flujo de MCP GET independiente, DELETE punto final de sesión, `Mcp-Session-Id`, o`Last-Event-ID`Las notificaciones de cambios de larga duración utilizan una`subscriptions/listen`POST cuya respuesta permanece abierta como un flujo de SSE.

### Entrada del cliente sin solicitudes iniciadas por el servidor .

> **【中文解读】**旧规范允许服务器反向发请求(`sampling/createMessage`¿Qué es esto?`roots/list`¿Qué es esto?`elicitation/create`);现行协议改用 MRTR(Múltiple Solicitudes de viaje de ida y vuelta):工具调用返回 `resultType: input_required`Y también`inputRequests`- ¿ Qué ?`requestState`, clientela recoger entrada después de uso**新的 JSON-RPC ID**重试原方法并携带 `inputResponses`, originalmente como reportaje`requestState` Roots/Sampling/Logging  todavía disponible pero abandonado  Nuevo implementar no volver a utilizar, prioridad con documentos/catálogos de referencia 、 recursos URI 和直连模型供应商──

Las revisiones anteriores permiten que un servidor envíe solicitudes como `sampling/createMessage`¿ Qué ?`roots/list`, o`elicitation/create`El protocolo actual utiliza solicitudes de viajes múltiples en lugar de una llamada de herramienta elegible, lectura de recursos o solicitud de devoluciones.`resultType: input_required`con al menos uno de los `inputRequests`o `requestState`. El cliente recoge cualquier entrada solicitada, vuelve a probar el método original con un nuevo ID JSON-RPC y el correspondiente `inputResponses`, y se hace eco de la exacta`requestState`Cuando se proporcionó uno.`inputRequests`Si estaban presentes, el retiro omite.`inputResponses`¿ Qué ?

Las raíces, muestras y registro siguen funcionando pero están desactualizadas, por lo que las nuevas implementaciones no deben adoptarlas.`inputRequests`, nunca como solicitudes independientes de servidor a cliente JSON-RPC. Prefiere parámetros de archivo o directorio explícitos, URIs de recursos, configuración de servidor e integración directa entre proveedor de modelos. Utilice stderr para el diagnóstico de estudio y OpenTelemetry para la telemetría de producción.

```figure
mcp-nxm-collapse
```

## Construye con movimiento.

> **【中文解读】**五步构建:(1) 注册服务器接口面(工具/资源/提示);(2) 给每个请求附加 `_meta`Se puede elegir el lugar de trabajo.`server/discover`¡ ¡ ¡ Qué tan grande !`tools/list`• 4) HTTP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `MCP-Protocol-Version`- ¿ Qué ?`Mcp-Method`- ¿ Qué ?`Mcp-Name`),头体不一致 → HTTP 400 + `-32020`• 5) Colocar las fronteras de seguridad fuera del estado del acuerdo per petición de identificación host local 绑定 + Origin 校验`destructiveHint`标记破坏性工具并要求主持人审批──

### Paso 1: Registre una superficie de servidor. Paso 1: Registre la interfaz del servidor.

El registro se mantiene sencillo a pesar de que el contrato de solicitud ha cambiado:

```python
server = MCPServer("demo-server")

@server.tool(
    "add",
    "Add two integers.",
    {
        "type": "object",
        "properties": {
            "a": {"type": "integer"},
            "b": {"type": "integer"}
        },
        "required": ["a", "b"]
    }
)
def add(a: int, b: int) -> dict:
    return {"sum": a + b}
```

La aplicación enviada en `code/main.py`También registra un recurso y un prompt. utiliza deliberadamente la biblioteca estándar para que pueda ver cada sobre en lugar de delegar el protocolo a un SDK.

### Paso 2: adjuntar metadatos a cada solicitud. Paso 2: dar a cada solicitud datos adicionales.

```python
def request(method, params=None):
    body_params = dict(params or {})
    body_params["_meta"] = {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientCapabilities": {},
        "io.modelcontextprotocol/clientInfo": {
            "name": "demo-client",
            "version": "1.0.0"
        }
    }
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": body_params
    }
```

No almacenes estos metadatos en caché solo en un objeto de conexión. El servidor los valida en cada solicitud.

### Paso 3: opcionalmente descubre antes de la lista.

Llamé`server/discover`, elige una versión compatible, luego llame `tools/list`- Un directo .`tools/list`También es válido si ya conoce la versión y puede manejarla `-32022`¿ Qué ?

La demostración devuelve listas de herramientas en orden de nombres y adjunta `ttlMs`¿ Qué ?`cacheScope`¿ Qué ?`resultType`Una llamada de herramienta devuelve un resultado completo, no caché porque su salida puede depender del estado actual.

### Paso 4: mapear la misma solicitud a HTTP.

Un control remoto .`tools/call`POST incluye encabezados que reflejan el cuerpo JSON-RPC:

```http
POST /mcp HTTP/1.1
Content-Type: application/json
Accept: application/json, text/event-stream
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: add
```

El `MCP-Protocol-Version`El encabezado debe coincidir con la versión en `_meta`- ¿ Qué ?`Mcp-Method`Se requiere en cada solicitud de JSON-RPC y debe coincidir `method`- ¿ Qué ?`Mcp-Name`sólo se requiere para `tools/call`¿ Qué ?`resources/read`, y `prompts/get`, donde debe coincidir con el nombre de la herramienta, URI de recurso o nombre de solicitud. Un encabezado requerido faltante o una incompatibilidad devuelve HTTP 400 con `HeaderMismatch`código `-32020`¿ Qué ?

### Paso 5: Aplicar la seguridad fuera del estado del protocolo .

- Valida la autorización y la audiencia en cada solicitud HTTP.
- Conectar los servidores locales a localhost y validar `Origin`en HTTP transmitible.
- Marque las herramientas mutantes con `destructiveHint: true`y requieren la aprobación del anfitrión.
- Pasar directorio y alcance de archivo explícitamente en lugar de depender de raíces obsoletas.
- Trate los recursos y la salida de herramientas como datos no confiables.
- Mantenga el stdout reservado para JSON-RPC bajo stdio; escriba diagnósticos a stderr.

## Usala para hacer pruebas .

Ejecutar la lección de su directorio:

```bash
python3 code/main.py
cd code
python3 -m unittest discover tests -v
```

La primera línea debe informar sobre el descubrimiento de `demo-server`en el protocolo `2026-07-28`- Entonces inspeccionar .`MCPClient.request`: se reconstruye `_meta`Eliminar los metadatos de una solicitud y observar que el servidor lo rechaza.

## Envíalo . Entregue productos .

`outputs/skill-mcp-server-designer.md`El portal de aceptación requiere un resultado de descubrimiento, una política de metadatos por solicitud, listas deterministas de caché, manejos de estado explícitos, encabezados de transporte, autorización y reglas de aprobación.

## Continúa con el MCP Deep Dive Continúa con el MCP Deep Dive

Esta lección te da el modelo de protocolo. la fase 13 convierte cuatro límites de producción en lecciones separadas de construcción y verificación:

1. [MCP Tool Contracts and Content](../../../13-tools-and-protocols/28-mcp-tool-contracts-and-content/docs/en.md)cubre esquemas de entrada cerrados, contenido estructurado, metadatos de enrutamiento, paginado opaco, autorización de finalización y la diferencia entre errores de protocolo y dominio de herramienta.
2. [MCP Reliability, Cancellation, and Flow Control](../../../13-tools-and-protocols/29-mcp-reliability-cancellation-and-flow-control/docs/en.md)cubre la cancelación de solicitudes, la cancelación de tareas duraderas, plazos, idempotencia, retropresión, amortiguamiento de proxy y comportamiento de reconexión.
3. [MCP Registry Supply Chain, Admission, Drift, and Rollback](../../../13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift/docs/en.md)cubre la prueba del espacio de nombres, la procedencia de los artefactos, los pines inmutables, la deriva en vivo, el estado del Registro, la evidencia de admisión y el retroceso.
4. [MCP Conformance Engineering](../../../13-tools-and-protocols/31-mcp-conformance-versioning-and-operations/docs/en.md)cubre transcripciones de cable dorado y negativo, épocas de versiones estrictas, diferenciales SDK, pruebas de proxy, redacción, puertas de salud y retroceso de liberación.

Los seguimos en el orden en que el servidor cruzará un límite de equipo o confianza. Juntos se mueven de el método funciona a el contrato permanece seguro y diagnosticable a través de la implementación.

## Los ejercicios.

1. Añadir un`subtract`herramienta y confirmación `tools/list`se mantiene ordenado alfabéticamente.
2. Eliminar la clave de versión del protocolo y verificar Parámetros inválidos (`-32602`Entonces envíe la versión bien formada pero sin soporte `2025-11-25`, verificar`-32022`, confirme`requested`se hace eco de esa revisión, y elegir entre `supported`¿ Qué ?
3. Añadir un servidor-minted `draftId`Explique por qué ese es el estado de aplicación en lugar de una sesión de protocolo.
4. Regreso .`input_required`Reutilice la llamada original con un nuevo ID, un `inputResponses`la entrada, y el exacto `requestState`en lugar de inventar una solicitud JSON-RPC de servidor a cliente.
5. Esbozar un cliente de estudio de doble época. Tratar un resultado o un error moderno reconocido como moderno, y permitir la retroceso a `initialize`Sólo por un error no reconocido o un tiempo de espera.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| MCP | "Tool protocol for LLMs" | JSON-RPC protocol for server discovery, tools, resources, prompts, and extensions |
| Host | "The AI app" | Owns the model and UI and mounts one or more MCP clients |
| Client | "The connector" | Speaks MCP to one server on behalf of a host |
| Stateless MCP | "No session" | Every request carries version and capabilities; no protocol state is keyed by a connection |
| `server/discover` | "Capability probe" | Required server method advertising versions, capabilities, and identity |
| `resultType` | "Result state" | Marks a result as `complete` or `input_required` |
| State handle | "Workflow id" | Server-minted application identifier passed as an ordinary argument |
| Streamable HTTP | "Remote transport" | One POST endpoint with JSON or request-scoped SSE responses |
| MRTR | "Ask and retry" | Input request embedded in a result, followed by a retry of the original operation |

## Más Leer más Leer más

- [MCP 2026-07-28 key changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- [MCP server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
- [MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [MCP Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
- [MCP deprecated features](https://modelcontextprotocol.io/specification/2026-07-28/deprecated)
