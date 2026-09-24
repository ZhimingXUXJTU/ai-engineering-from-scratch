# Plataformas de LLM administradas  Bedrock, Vertex AI, Azure OpenAI  平台 托管 OpenAI LLM

> Tres hiperescaladoras, tres estrategias distintas. AWS Bedrock es un mercado modelo  Claude, Llama, Titan, Estabilidad, Cohere detrás de una API. Azure OpenAI es una asociación exclusiva de OpenAI más unidades de rendimiento provistas (PTU) para capacidad dedicada. Vertex AI es Gemini primero con la mejor historia de largo contexto y multimodal. En 2026 el análisis artificial mide Azure OpenAI a ~ 50 ms mediana y Bedrock a ~ 75 ms en Llama 3.1 405B equivalentes  PTUs explican la brecha porque la capacidad dedicada supera la compartida a pedido. La regla de decisión no es "cuál es el más rápido" sino "cuál es el catálogo de modelos y la superficie de FinOps que coincide con mi producto". Esta lección te enseña a elegir con las compensaciones escritas, no con vibraciones.

> **【中文解读】**Este capítulo presenta la selección y comparación de las plataformas de servicios de gestión de LLM ofrecidas por OpenAI, Anthropic, Google, etc.

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 11 (LLM Engineering)全部你已经会使用OpenAI/Anthropic API 调模型;Fase 13 (Tools & Protocols) 理解MCP等协议。本节讲生产部署选哪个云不是技术问题,是商业+合规+技术综合决策。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cost-and-latency comparator) | **语言:** Python（标准库，成本-延迟比较器）
**Prerequisites:** Phase 11 (LLM Engineering), Phase 13 (Tools & Protocols) | **前置知识:** Phase 11（LLM 工程）, Phase 13（工具与协议）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizaje

- Nombre las tres estrategias de plataforma (mercado vs exclusivo vs Gemini-primero) y coincida cada una con un caso de uso del producto.

> ¿ Qué es esto ?**【类比】**三大云平台 LLM 服务 = 三种餐厅:(1) **AWS Bedrock**= 美食广场((Una API 调多家模型,Claude/Llama/Titan,灵活但延迟略高);(2) **Azure OpenAI**= 米其林餐厅(OpenAI 独家合作,PTU 专属容量,延迟最低 ~50ms,但贵且绑定OpenAI);(3) **Vertex AI**= Tema de la sala de comidas (Google Gemini 主打,长上下文和多模态最强,2M token 窗口) ――select哪哪个看你的菜谱(Use Claude 还是 GPT 还是 Gemini) 和预算──

> ️ **【易错点】**托管平台选型的 3 个坑: (1) **只看标价**Bedrock 上 Claude 比人类 直连贵 15-20% (云税), pero合规和统一计值钱;做 TCO (总拥有成本)而非单价比较 (单价比较)**忽略数据驻留** Los datos de los usuarios europeos deben permanecer en Europa, optar por Azure EU 区域 o Bedrock eu-central-1; la transmisión de datos transfronteriza es contraria al RGPD。(3) **没做厂商锁定评估**Con OpenAI PTU 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后想换Bedrock 后后后后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bedrock 后的Bed
  China                                                                                                                                                                                                                                                               
- Explica qué unidades de rendimiento proporcionadas (PTU) te compran en Azure OpenAI y por qué Bedrock a pedido suele leer ~ 25 ms más lento en la escala 405B.
  China Translation: explicación de lo que ha traído la unidad de volumen de producción de Azure OpenAI (PTU) y por qué la implementación de Bedrock en 405B a escala suele ser lenta en 25 ms.
- Diagrama la superficie de atribución FinOps para cada plataforma (Profiles de Inferencia de Aplicaciones Bedrock vs Profiles de Inferencia Vertex por equipo vs Áreas de alcance de Azure + Reservas de PTU).
  La aplicación de la información de la plataforma de trabajo de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la
- Escriba una política de "mínimo de dos proveedores" y explique por qué el bloqueo de un solo proveedor es el error caro en 2026.
  China:写下"双供应商最低" estrategia,并解释为什么单供应商锁定是2026年昂贵的错误――

## El problema es la introducción del problema

Usted eligió Claude 3.7 Sonnet para su producto. Ahora necesita para servirlo. Puede llamar a la API de Antropic directamente, o puede llamarlo a través de AWS Bedrock, o puede pasar a través de una puerta de entrada. La API directa es la más simple; Bedrock añade BAAs, puntos finales VPC, IAM y CloudWatch atribución. La puerta de entrada añade failover, facturación unificada y límites de tasas entre los proveedores.

> Usted ha elegido para su producto Claude 3.7 Sonnet. Ahora necesita implementarlo. Puede utilizar directamente la API Antropic, también puede utilizar a través de AWS Bedrock, o puede usar a través de la API Web.

La pregunta más profunda es el catálogo. Si necesitas a Claude y Llama y Gemini en el mismo producto, no puedes comprarlos todos desde un solo lugar a menos que ese lugar sea Bedrock más Vertex más Azure OpenAI simultáneamente.

> Más profundo problema es el catálogo de modelos. Si necesitas Claude, Llama y Gemini en el mismo producto, no puedes comprar todos los modelos en un solo lugar, a menos que utilices Bedrock + Vertex + Azure OpenAI simultáneamente.

Esta lección muestra las tres apuestas, la brecha de latencia, la brecha de FinOps y el riesgo de bloqueo.

> En esta clase se trazan tres puntos:

> **【中文解读】**选择 LLM 后,"在哪里部署" es una decisión de nivel de infraestructura.  Direct调用 API 最简单,但缺乏企业级控制; 通过云平台(Bedrock/Vertex/Azure)调用增加了合规、审计能力; 通过网关调用则获得多供应商容量和统计费.

> **【拓展：LLM 部署模式】**El modelo de implementación de servicios de LLM en el período 2024-2026 ha pasado desde la "API directa" → "Cloud Platform托管" → "AI 网关统一路由" de desarrollo. En el año 2025 los proyectos de conexión a la red de AI OpenRouter、Portkey、LiteLLM obtienen una gran adopción, el valor central es proporcionar una conexión única entre varios proveedores、 fallover automático y optimización de costes. En el caso de los servicios de la empresa, aproximadamente el 60% de los proyectos de implementación de sistemas de conexión a la red ya han sido adoptados.

## El concepto central.

> **【中文解读】**La estrategia de la plataforma de LLM de los fabricantes de tres grandes nube es muy diferente: AWS Bedrock es un "modelo集市", un aglomerado de varios proveedores; Azure OpenAI es un "sólo cooperativo", un "sólo cooperativo", un "modelo" de OpenAI; Vertex AI es un "gemini  prioritario", un punto de venta para superar las capacidades de la escritura y la multimedia.

> **【拓展：全球 LLM 云平台格局】**Además de tres grandes hiperescalade afuera, en el año 2026 hay más de lo que vale la pena de tener en cuenta: Cloudflare Workers AI(边缘推理) ✓ Juntos AI(Open Source Model推理平台, $0.18/M tokens para Llama 3.1 70B) ✓ Grroq(LPU 推理引擎,TTFT < 20ms) ✓ Cerebras(CS-3 wafer-scale 推理,2000+ tokens/s) ✓ En el país hay cientos de miles de ✓帆阿里百炼、火山方舟等, pero el catálogo de modelos no está conectado con la plataforma internacional

### Tres estrategias

**AWS Bedrock**La empresa de software de Bedrock está trabajando en la creación de un nuevo sistema de control de datos de la red de datos de la red de Internet.

> **AWS Bedrock** 模型集市──Claude(Antropico)、Llama(Meta)、Titan(AWS 自有)、Estabilidad(图像)、Cohere(嵌入)、Mistral, así como imágenes y嵌入子目录── una API、 una IAM 界面、 una CloudWatch 导出──Bedrock 注是客户想要可选择性而不是单一模型──

**Azure OpenAI** la asociación exclusiva. Obtiene GPT-4 / 4o / 5 / o serie, DALL·E, Whisper y ajuste fino de los modelos OpenAI en los centros de datos de Azure. No hay modelos no OpenAI en el catálogo "Azure OpenAI Service"  esos van a Azure AI Foundry (producto separado).

> **Azure OpenAI** 独家合作──你在Azure 数据中心获得 GPT-4/4o/5/o 系列、DALL·E、Whisper 和 OpenAI 模型微调──"Azure OpenAI Service" 目录中没有非 OpenAI 模型那些在Azure AI Foundry(独立产品) 中──Azure 注是OpenAI 保持前沿地位和客户想要对此关系的企业级控制──

**Vertex AI** Gemini primero, todo lo demás segundo. Gemini 1.5 / 2.0 / 2.5 Flash y Pro, más Model Garden (tercer).

> **Vertex AI** Gemini 优先,其他其次──Gemini 1.5/2.0/2.5 Flash 和 Pro,加上 Model Garden(第三方)──Vertex 的注是多模态长上下文1M代币的 Gemini 上下文是差异化因素──

### Diferencias de latencia en la escala

El análisis artificial tiene un índice de referencia continuo. En implementaciones equivalentes Llama 3.1 405B (compartidas bajo demanda), la latencia media de primer token de Azure OpenAI es de alrededor de 50 ms; Bedrock es de alrededor de 75 ms. La brecha no es un fallo de AWS  es una diferencia de modelo de capacidad. Azure vende PTUs (Unidades de Despliegue Provisionadas), que reservan la capacidad de GPU para su inquilino. El equivalente de Bedrock (Provisioned Throughput) existe, pero comienza alrededor de $21/hora por unidad, y la mayoría de los clientes se quedan en el uso compartido a pedido.

> Análisis Artificial 运行持续基准测试。在等效的Llama 3.1 405B 部署) 共享按量) 上,Azure OpenAI 中位首代币 延迟约50ms;Bedrock 约75ms。差距不是 AWS 问题而是容量模型差异──Azure 销售 PTU(预置吞吐量单位),为您租户预留 GPU 容量──Bedrock 等效功能存在但起价约$21/户小时/按量模式,大多数客户使用共享量模式──

La capacidad compartida a pedido compite con el tráfico de todos los demás clientes. La capacidad dedicada no. Si el TTFT de su producto es < 100 ms en P99, compra PTUs en Azure, compra Bedrock Provisioned Throughput o acepta la variación predeterminada.

> 按量共享容量与所有其他客户的流量竞争 GPU资源──专用容量不会──如果你的产品SLA是P99 TTFT < 100ms,你要么在Azure 购买PTU,要么购买Bedrock Provisioned Throughput,要么接受默认方差──

> **【中文解读】**延迟差距的本质是"容量模型"差异―― en la distribución de la masa compartida, tu solicitud compite con el tráfico de todos los demás clientes de recursos GPU; capacidad especial (PTU) 则预留独占 GPU――Azure PTU en 40-60% utilization rate puede ahorrar hasta 70% de costes, pero en el espacio todavía paga――Bedrock's masa model TTFT mide alrededor de 75ms,Azure PTU alrededor de 50ms,25ms diferencia en el alto espectro de interacción en el escenario de los usuarios.

### Economía del rendimiento de suministro

Azure PTUs: un bloque reservado de cálculo de inferencia. Hasta ~70% de ahorro frente a la demanda para cargas de trabajo predecibles. Coste fijo por hora independientemente del tráfico  usted paga por la reserva incluso cuando está inactivo. El equilibrio de ruptura es generalmente alrededor de 40-60% de utilización sostenida.

> Azure PTU: pre-reservación de cálculo de bloques. Para la carga de trabajo predecible, el coste fijo por hora, independientemente de cómo el tráfico, incluso el espacio, también debe ser pagado.

Capacidad de transmisión de la cama: $21-$50 por hora dependiendo del modelo y la región. matemática similar  equilibrio de ruptura es alrededor de la mitad de la utilización máxima.

> Bedrock Provisioned Throughput: 每小时 $21-$50, depende de los modelos y regiones. Un modelo económico similar tiene un punto de equilibrio de pérdida de aproximadamente la mitad de la tasa de utilización de valor máximo.

La capacidad de suministro de Vertex se vende por SKU Gemini; los precios varían según el modelo y la región y se publicitan menos públicamente.

> Vertex  Preposición de capacidad según Gemini SKU  Venta; precio en función del modelo y la región, información pública menor。

### Superficie de FinOps  el diferenciador real

**Bedrock Application Inference Profiles**Es la atribución más limpia del mercado.`team`¿ Qué ?`product`¿ Qué ?`feature`• redirige todas las invocaciones de modelos a través de él; CloudWatch rompe el costo por perfil sin procesamiento posterior.

> **Bedrock Application Inference Profiles**Es el programa de atribución de costes más claro del mercado.`team`¿Qué es esto?`product`¿Qué es esto?`feature` Marca los archivos de configuración; a través de ellos todos los modelos de la red; CloudWatch  no necesita procesamiento posterior, ya que se puede dividir los archivos de configuración según el costo.

**Vertex**La atribución es proyecto por equipo más etiquetas en todas partes. Modela cada equipo como un proyecto GCP, coloca etiquetas en cada recurso, y utiliza BigQuery Billing Export + DataStudio para los rollups. Más trabajo, pero BigQuery le da SQL arbitrario en los datos de costos.

> **Vertex**归因是项目-per-团队加无处不在标签――: Usted construirá cada equipo en un proyecto GCP, colocará un etiquetado en cada recurso, utilizando BigQuery Billing Export + DataStudio  realizar un total de tasas 工作量更大, pero BigQuery 允许 ejecutar cualquier SQL sobre los costos de los datos―:

**Azure**Las etiquetas se heredan de grupos de recursos, no de solicitudes, por lo que la atribución por solicitud requiere métricas personalizadas de Application Insights o una puerta de enlace que sella los encabezados.

> **Azure**Dependiendo de la suscripción/el grupo de recursos de la red de trabajo, PTU  pre-reservado como objeto de coste de primer nivel.

El patrón: Bedrock es nativo más limpio, Vertex es más flexible a través de BigQuery, Azure es más opaco a menos que usted instrumento.

> 总结:Bedrock 原生最清晰,Vertex 通过 BigQuery 最灵活,Azure 除非自行埋点否则最不透明──

> **【中文解读】**FinOps (en inglés: FinOps) es la infraestructura de LLM más subestimada. Los perfiles de Inferencia de Aplicaciones de Bedrock son los más precisos en la actualidad en términos de producción original y de costo de uso.

> **【拓展：LLM FinOps 实践】**企业 LLM  gasto en 2025 creció en promedio 300%  Flexera 2025 云状态报告) 常见 FinOps 策略包括:(1) 按代币 消耗设置团队预算告警;(2) 使用缓存层(Semantic Cache) reducir el recurso调调约 30-40%;(3) 模型路由简单任务用小模型、复杂任务用大模型,可节省50%+ 成本;(4) 批量API在非实时场景可降低50% 价格;;

### El bloqueo es el riesgo de 2026

El compromiso de un solo hiperescalado estaba bien cuando un modelo dominaba. En 2026 la frontera se mueve mensualmente  Claude 3.7 un trimestre, Gemini 2.5 el siguiente, GPT-5 el trimestre después.

> Cuando un modelo es dominante, solo un compromiso puede también ser realizado. En 2026 el modelo de vanguardia cada mes está cambiando. Una temporada es Claude 3.7, la siguiente temporada es Gemini 2.5, la siguiente es GPT-5.

Los equipos de trabajo del patrón adoptan: dos proveedores mínimos para cualquier llamada de LLM crítica al producto. Bedrock más Azure OpenAI es el par común  Claude de uno, GPT de otro, fallo entre ellos, la misma puerta de enlace. El aumento de costos es insignificante porque las rutas de la puerta de enlace son óptimas; el aumento de disponibilidad durante los apagones (como el incidente de Azure OpenAI de enero de 2025, el apagón de AWS us-east-1) es decisivo.

> Modelo de adopción de equipos de alta eficiencia: cualquier producto clave LLM 调用双供应商最低策略。Bedrock + Azure OpenAI es el conjunto más común uno proporciona Claude, otro proporciona GPT, a través del mismo enlace para realizar fallas de transferencia。 El aumento de costos puede ser ignorado, ya que la disponibilidad de la red de la ruta es mejor; durante el período de tiempo 机的可用性提升(como Azure OpenAI en enero de 2025 AWS us-east-1 机) es decisivo.

> **【中文解读】**El mayor riesgo de infraestructura del año 2026 es el bloqueo de proveedores. El modelo de vanguardia cada trimestre está cambiando. Q1 con Claude 3.7, Q2 con Gemini 2.5, Q3 con GPT-5. El bloqueo de una sola plataforma significa una capacidad de vanguardia superior a 2/3 de la misma. La mejor práctica es la estrategia de "doble proveedor mínimo": Bedrock + Azure OpenAI es el conjunto más común, a través de la red de conexión, el aumento de costos puede ser ignorado, pero la disponibilidad se mejora significativamente en el caso de fallas.

> **【拓展：云厂商宕机事件】**En enero de 2025, Azure OpenAI experimentó un fallo global de hasta varias horas, que afectó a todos los clientes empresariales de ChatGPT de Azure que dependen de un solo Azure. Ese mismo año, AWS también sufrió fallas graves en la región de este-1.

### Residencia de datos, BAAs y industrias reguladas

Bedrock: BAAs en la mayoría de las regiones; puntos finales de VPC; barandillas.
Azure OpenAI: HIPAA, SOC 2, ISO 27001; residencia de datos de la UE; el estándar regulado por la empresa.
Vertex: HIPAA, GDPR, residencia de datos por región; la pila de cumplimiento de Google Cloud.

> El programa de investigación de la Universidad de Madrid, en el que se desarrollaban las actividades de investigación y desarrollo, se desarrolló en el marco de la investigación de la investigación y desarrollo de la tecnología.
> Azure OpenAI:HIPAA, SOC 2, ISO 27001; datos de la UE;
> Vertex:HIPAA, GDPR, según los datos de la región; Google Cloud's compliance──

Las diferencias son en las políticas de retención de datos, cómo se manejan los registros y si el monitoreo de abuso lee el tráfico (opt-in por defecto en la mayoría; opt-out disponible para las empresas).

> Los datos de la empresa se pueden excluir de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión

### Números que debes recordar

- TTFT mediano de Azure OpenAI en equivalentes Llama 3.1 405B: ~ 50 ms (con PTU).
  En el modelo de Llama 3.1 405B 等效模型中位 TTFT:~50ms(utilizando PTU)
- Mediana de TTFT de cama bajo demanda: ~75 ms.
  El tiempo de la operación de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de la cámara de
- Capacidad de transmisión de la cama: $21-$50/hora por unidad.
  中文翻译:Bedrock Provisionado Desempleo: cada unidad $21-$50/小时──
- Reto de equilibrio de las PTU de Azure: ~ 40-60% de utilización sostenida.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- Ahorro de PTU frente a la demanda en alta utilización: hasta el 70%.
  China:PTU en alta tasa de utilización en comparación con el modo de consumo ahorro de hasta el 70%

## Usalo con el marco de ejecución
```figure
i4-platform-lanes
```

## Usalo

`code/main.py`comparar las tres plataformas en una carga de trabajo sintética  modela la economía de demanda frente a PTU, la variación de TTFT y la fidelidad de la atribución de costos. ejecutarlo para ver dónde las PTUs dan sus frutos y dónde la amplitud del modelo del mercado supera a una brecha de TTFT.

> `code/main.py`En la carga de trabajo de la composición comparar tres plataformas se construye en masa frente a PTU economía TTFT favor diferencias y costos atribuidos a la seguridad  运行

> **【中文解读】**实践部分通过模拟工作负载对三大平台的关键指标包括:TTFT(首代币延迟) 吞吐量、每百万代币 成本──通过调整利用率参数, se puede ver directamente PTU en qué nivel de carga bajo en comparación con la masa de cuentas más planea──

## Envíe el producto .

Esta lección produce`outputs/skill-managed-platform-picker.md`. Dado el perfil de la carga de trabajo (modelos necesarios, TTFT SLA, volumen diario, requisitos de cumplimiento), recomienda una plataforma primaria, una retroceso y un plan de instrumentación FinOps.

> 本课产 出  `outputs/skill-managed-platform-picker.md` proporcionar un modelo de configuración de carga de trabajo                                                                                                                                                                                                                                                                  

> **【拓展：生产环境平台选型 Checklist】**El proyecto de ley de gestión de la producción de productos y servicios de la Unión Europea (IPCC) se ha desarrollado para el desarrollo de la tecnología de gestión de los productos y servicios de la Unión Europea (IPCC), que se desarrolla en el marco de la aplicación de la ley de gestión de los productos y servicios de la Unión Europea (GDPR).

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿En qué uso sostenido Azure PTU supera a la demanda para un modelo de clase 70B?
   Traducción:运行`code/main.py` ¿En qué medida la PTU de Azure es mejor que el modelo de clase 70B bajo la tasa de utilización continua?
2. Su producto necesita Claude 3.7 Sonnet y GPT-4o. Diseñar un despliegue de dos proveedores que va a qué hiperescalador, qué puerta de entrada se encuentra delante, ¿cuál es la política de fallas?
   China: Tu producto necesita Claude 3.7 Sonnet 和 GPT-4o.
3. Un cliente de atención médica regulada requiere BAAs, residencia de datos de EE.UU. Este, y sub-100ms P99 TTFT. Elija una plataforma y justifique con tres características específicas.
   Un cliente de salud bajo control necesita BAAs, Estados Unidos-Oriente y P99 TTFT < 100ms.
4. Descubre que su factura de Bedrock ha aumentado 4 veces este mes sin cambios en el tráfico. ¿Cómo encontraría al culpable sin los perfiles de aplicación?
   Usted encontró que el volumen de la página web de Bedrock ha aumentado 4 veces, pero el tráfico no ha cambiado. ¿Cómo encontrar la razón? ¿Hay perfiles que necesitan mucho tiempo?
5. Lea las páginas de precios de Azure OpenAI y Bedrock. ¿Para una carga de trabajo Claude de 100M-token/mes, que es más barata  API Antropic directa, Bedrock a pedido o Bedrock Provisioned Throughput?
   Por ejemplo, el software de la plataforma de intercambio de datos (CAP) es un sistema de intercambio de datos (CAP) de datos (CAP) de datos (CAP).

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|----------|
| Bedrock | "AWS LLM service" | Model marketplace across Claude, Llama, Titan, Mistral, Cohere | AWS 的 LLM 模型集市平台 |
| Azure OpenAI | "Azure's ChatGPT" | Exclusive OpenAI models in Azure datacenters with enterprise controls | Azure 独家托管 OpenAI 模型的企业服务 |
| Vertex AI | "Google's LLM" | Gemini-first platform with Model Garden for third-party models | Google 的 Gemini 优先 AI 平台 |
| PTU | "dedicated capacity" | Provisioned Throughput Unit — reserved inference GPUs, priced per hour | 预置吞吐量单位——独占推理 GPU 容量 |
| Application Inference Profile | "Bedrock tagging" | Per-product cost/usage profile with tags, CloudWatch-native | Bedrock 按产品归因的推理配置文件 |
| Model Garden | "Vertex catalog" | Vertex AI's third-party model section, separate from Gemini | Vertex AI 第三方模型目录 |
| Two-provider minimum | "LLM redundancy" | Policy of running every critical LLM path across ≥2 hyperscalers | 双供应商最低策略——关键 LLM 调用跨 2+ 云商 |
| BAA | "HIPAA paperwork" | Business Associate Agreement; required for PHI; provided by all three | 业务关联协议——HIPAA 合规必需 |
| Abuse monitoring | "the log watcher" | Provider-side safety scan on prompts/outputs; opt-out in enterprise | 平台侧的 prompt/输出安全扫描 |

## Más Leer más Leer más

- [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) tarjeta de tasa autorizada y precios de rendimiento provistos.
- [Azure OpenAI Service Pricing](https://azure.microsoft.com/en-us/pricing/details/azure-openai/) Economía y tarjetas de interés de la PTU.
- [Vertex AI Generative AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) Tías Gemini y recargos de jardín modelo.
- [Artificial Analysis LLM Leaderboard](https://artificialanalysis.ai/) índices de referencia de latencia y rendimiento continuos entre los proveedores.
- [The AI Journal — AWS Bedrock vs Azure OpenAI CTO Guide 2026](https://theaijournal.co/2026/03/aws-bedrock-vs-azure-openai/) marco de decisión empresarial.
- [Finout — Bedrock vs Vertex vs Azure FinOps](https://www.finout.io/blog/bedrock-vs.-vertex-vs.-azure-cognitive-a-finops-comparison-for-ai-spend) Mecánica de atribución lado a lado.
