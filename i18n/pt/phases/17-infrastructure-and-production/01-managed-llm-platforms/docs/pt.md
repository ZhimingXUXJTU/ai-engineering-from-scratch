# Gestão de LLM Plataformas  Bedrock, Vertex AI, Azure OpenAI  平台 托管 OpenAI LLM

> Três hiperescaladores, três estratégias distintas. AWS Bedrock é um mercado modelo  Claude, Llama, Titan, Estabilidade, Cohere por trás de uma API. O Azure OpenAI é uma parceria exclusiva com o OpenAI, além de unidades de transferência de dados (PTUs) para capacidade dedicada. A IA Vertex é a primeira Gemini com a melhor história de longo contexto e multimodal. Em 2026, a Análise Artificial mede o Azure OpenAI em ~ 50 ms de mediana e o Bedrock em ~ 75 ms em equivalentes Llama 3.1 405B  PTUs explicam a lacuna porque a capacidade dedicada supera a capacidade compartilhada sob demanda. A regra da decisão não é "o que é mais rápido", mas "o que catálogo de modelos e a superfície FinOps coincide com o meu produto". Esta lição ensina a escolher com as compensações escritas, não com vibrações.

> **【中文解读】**Esta secção apresenta a seleção e comparação das plataformas de serviços de gestão de LLM oferecidas pela OpenAI, Anthropic, Google, etc.

> - Não .**【前置】**學本節前 請先掌握:Fase 11 (LLM Engineering) 全部你已經會使用OpenAI/Anthropic API 调模型;Fase 13 (Tools & Protocols) 理解 MCP等协议──本节讲生产部署选哪个云不是技术问题,是商业+合规+技术综合决策──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cost-and-latency comparator) | **语言:** Python（标准库，成本-延迟比较器）
**Prerequisites:** Phase 11 (LLM Engineering), Phase 13 (Tools & Protocols) | **前置知识:** Phase 11（LLM 工程）, Phase 13（工具与协议）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizagem

- Cite as três estratégias de plataforma (mercado vs exclusivo vs Gemini-first) e combina cada uma com um caso de uso do produto.

> - Não .**【类比】**三大云平台 LLM 服务 = 三种餐厅:(1) **AWS Bedrock**= 美食广场((一个API 调多家模型,Claude/Llama/Titan,灵活但延迟略高);(2) **Azure OpenAI**= 米其林餐厅(OpenAI 独家合作,PTU 专属容量,延迟最低 ~50ms,但贵且绑定OpenAI);(3) **Vertex AI**= Tema餐厅(Google Gemini 主打,长上下文和多模态最强,2M token 窗口)。select哪哪个看你的菜谱(Use Claude 还是 GPT 还是 Gemini)和预算──

> ️ **【易错点】**托管平台选型的 3 个坑: 1) **只看标价**Bedrock 上 Claude 比 Anthropic 直连贵 15-20% (云税),但合规和统一计值钱;做 TCO (总拥有成本)而非单价比较 (云税),但合规和统一计值钱;做 TCO (总拥有成本)而不是单价比较 (单价比较)**忽略数据驻留** Os dados dos utilizadores europeus devem permanecer na Europa, escolher Azure EU 区域 ou Bedrock eu-central-1; transfronteiras transferências de dados violam o RGPD。(3) **没做厂商锁定评估** Usar OpenAI PTU 后想换 Bedrock 后想换 Bedrock 后想换 Bedrock 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后后后后后后后后后后后后后后后后后换 后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后
  Chinese: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: : : : : : : :
- Explique o que as Unidades de Transmissão Provisória (PTUs) compram no Azure OpenAI e por que o Bedrock sob demanda normalmente lê cerca de 25 ms mais lentamente na escala 405B.
  Tradução do inglês para Chinês: Explique o que a unidade de pronúncia de pronúncia do Azure OpenAI (PTU) trouxe, e por que o Bedrock 按量部署在405B 规模下通常慢约25ms──
- Diagrama a superfície de atribuição FinOps para cada plataforma (profis de inferência de aplicativos Bedrock vs Vertex projeto por equipe vs escopo de Azure + reservas de PTU).
  O programa de desenvolvimento de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de para para para para para para para para para para para para para para para para para para para para para para para para os de assistê para os de assistê para os de assistê para os de assistê para os de assistê para os de assistê para os de assistê para os de assistê para os de assistê para
- Escreva uma política de "mínimo de dois fornecedores" e explique por que o bloqueio de um único fornecedor é o erro caro em 2026.
  Chinese:写下"双供应商最低" estratégia,并解释为什么单供应商锁定是2026年昂贵的错误――

## O problema é o problema da introdução

Você escolheu Claude 3.7 Sonnet para o seu produto. Agora você precisa servi-lo. Você pode ligar para a API Anthropic diretamente, ou você pode chamá-la através da AWS Bedrock, ou você pode passar por um gateway. A API direta é a mais simples; Bedrock adiciona BAAs, pontos finais VPC, IAM e atribuição CloudWatch. O gateway adiciona falhaover, faturamento unificado e limites de taxas entre provedores.

> Você escolheu o produto Claude 3.7 Sonnet. Agora precisa de implementá-lo. Você pode usar diretamente a API Anthropic, também pode usar a AWS Bedrock, ou através da API Web.

A questão mais profunda é o catálogo. Se você precisa de Claude e Llama e Gemini no mesmo produto, você não pode comprá-los todos de um só lugar a menos que esse lugar seja Bedrock mais Vertex mais Azure OpenAI simultaneamente. Os hiperescaladores não são intercâmbios.

> Mais profundo problema é o catálogo de modelos. Se você precisar de Claude, Llama e Gemini no mesmo produto, você não pode comprar todos os modelos em um único local, a menos que use simultaneamente Bedrock + Vertex + Azure OpenAI.

Esta lição mapeia as três apostas, a lacuna de latência, a lacuna de FinOps e o risco de bloqueio.

> Esta aula traçou três diferenças de atraso, de diferença de finalização e de risco de bloqueio.

> **【中文解读】**选择 LLM 后,"在哪里部署" é uma decisão de nível de infraestrutura. 直接调用API 最简单,但缺乏企业级控制; 通过云平台(Bedrock/Vertex/Azure)调用增加了合规、审计能力; 通过网关调用则获得多供应商容量和统计费.

> **【拓展：LLM 部署模式】**O modelo de implementação de serviços de LLM em 2024-2026 passou de "API direta" → "Cloud Platform托管" → "AI 网关统一路由" a evolução.

## O conceito central.

> **【中文解读】**A estratégia de plataforma de LLM de três grandes fabricantes de nuvem é claramente diferente: AWS Bedrock é um "model集市", agrupando vários fornecedores; Azure OpenAI é um "sólo cooperativo", especializado em modelos OpenAI; Vertex AI é um "gêmeo prioritário", para além de longo tempo.

> **【拓展：全球 LLM 云平台格局】**Além de três grandes hipercalores, em 2026 há mais: Cloudflare Workers AI (administração de margens) ✓ Juntos AI (administração de margens) ✓ Tôquinas de modelo aberto (tôquinas de código aberto) $0.18/M para Llama 3.1 70B) ✓ Grroq (tôquinas de código aberto) ✓ LPU ✓ Motores de cálculo, TFT < 20ms) ✓ Cerebras (tôquinas de escala de wafer) ✓ CS-3 ✓ Tôquinas de código aberto (tôquinas de código aberto) ✓ 2000+ tokens (s) ✓

### Três estratégias

**AWS Bedrock**O mercado. Claude (Anthropic), Llama (Meta), Titan (AWS primeira-parte), Estabilidade (imagem), Cohere (embeddings), Mistral, mais imagem e inserção de sub-catálogos. Uma API, uma superfície IAM, uma CloudWatch exportação.

> **AWS Bedrock** 模型集市──Claude(Antropic)、Llama(Meta)、Titan(AWS 自有)、Stability(图像)、Cohere(嵌入)、Mistral, bem como imagens e emplacamentos 図書目录──a API、a IAM 界面、a CloudWatch 导出──Bedrock 注是客户想要可选择性而不是单一模型──

**Azure OpenAI** a parceria exclusiva. Você recebe GPT-4 / 4o / 5 / o-série, DALL·E, Whisper e ajuste fino de modelos OpenAI nos datacenters Azure. Nenhum modelo não OpenAI no catálogo "Azure OpenAI Service"  aqueles vão para a Azure AI Foundry (produto separado). A aposta da Azure é que OpenAI continua a ser a fronteira e os clientes querem controles empresariais sobre esse relacionamento específico.

> **Azure OpenAI** 独家合作──你在Azure 数据中心获得 GPT-4/4o/5/o 系列、DALL·E、Whisper 和 OpenAI 模型微调──"Azure OpenAI Service" 目录中没有非 OpenAI 模型那些在Azure AI Foundry(独立产品) 中──Azure 注是OpenAI 保持前沿地位和客户想要对此关系的企业级控制──

**Vertex AI** Gemini primeiro, tudo o resto em segundo lugar. Gemini 1.5 / 2.0 / 2.5 Flash e Pro, além do Model Garden (terceiro).

> **Vertex AI** Gemini  priorit, outros 其次── Gemini 1.5/2.0/2.5 Flash 和 Pro,加上 Model Garden(第三方)──Vertex 的注是多模态长上下文1M token 的 Gemini 上下文是差异化因素──

### Diferença de latência na escala

A Análise Artificial apresenta valores de referência contínuos. Em implementações equivalentes Llama 3.1 405B (compartilhadas sob demanda), a latença média do primeiro token do Azure OpenAI é de cerca de 50 ms; Bedrock é de cerca de 75 ms. A diferença não é uma falha da AWS  é uma diferença de modelo de capacidade. O Azure vende PTUs (Provisioned Throughput Units), que reservam capacidade de GPU para o seu inquilino. O equivalente do Bedrock (Provisioned Throughput) existe, mas começa em torno de US$ 21/hora por unidade, e a maioria dos clientes permanece em compartilhamento sob demanda.

> Análise Artificial 运行持续基准测试。在等效的Llama 3.1 405B 部署) 共享按量) 上,Azure OpenAI 中位首代币 延迟约50ms;Bedrock 约75ms。差距不是AWS 问题而是容量模型差异──Azure 销售PTU(预置吞吐量单位),为您租户预留GPU 容量──Bedrock 等效功能存在但起价约$21/户小时/按量模式,大多数客户使用共享量模式──

Capacidade compartilhada sob demanda compete com o tráfego de todos os outros clientes. Capacidade dedicada não. Se o seu produto SLA é TTFT < 100 ms em P99, você compra PTUs no Azure, compra Bedrock Provisioned Throughput ou aceita a variância padrão.

> 按量共享容量与其他客户流量竞争 GPU资源──专用容量不会──如果你的产品 SLA是P99 TTFT < 100ms,你要么在Azure 购买PTU,要么购买Bedrock Provisioned Throughput,要么接受默认方差──

> **【中文解读】**延迟差距的本质是"容量模型"差异――共享按量部署中,你的请求与其他客户的流量竞争 GPU资源;专用容量(PTU) 则预留独占 GPU――Azure PTU在 40-60%利用率时可节省高达70% 成本,但空时仍然付费――Bedrock's mass model TTFT 中位数约75ms,Azure PTU约50ms,25ms差距在高频交互场景中被用户感知──

### Economia da produção de dados

Azure PTUs: um bloco reservado de computação de inferência. Até ~ 70% de poupança vs. sob demanda para cargas de trabalho previsíveis. Custos fixos por hora independentemente do tráfego  você paga pela reserva mesmo quando está ociosa. O equilíbrio de ruptura geralmente é de cerca de 40-60% de utilização sustentada.

> Azure PTU: pré-reserva de cálculo de blocos. Para a carga de trabalho previsível, a economia de carga por volume é de cerca de 70%.

Transmissão de Bedrock: $21-$50 por hora dependendo do modelo e região. Matemática similar  equilíbrio de ruptura é cerca de metade da utilização máxima. compromisso mensal requerido.

> Bedrock Provisioned Throughput: 每小时 $21-$50, depende do modelo e da região.

A capacidade de fornecimento da Vertex é vendida por SKU Gemini; os preços variam de acordo com o modelo e a região e são menos publicamente anunciados.

> Vertex  pré-imposição de capacidade por Gemini SKU  venda; preço em relação ao modelo e à região, public information is less。

### Superfície FinOps  o diferenciador real

**Bedrock Application Inference Profiles**As atribuições de um perfil são as mais limpas do mercado.`team`- Não .`product`- Não .`feature`· rotear todas as invocações de modelo através dele; CloudWatch quebra o custo por perfil sem pós-processamento. Adicionado 2025, ainda o mais granular nativo de hipercaler.

> **Bedrock Application Inference Profiles**É o mais claro esquema de atribuição de custos do mercado.`team`- Não.`product`- Não.`feature` Marque os arquivos de configuração; através dele todos os modelos são modificados; CloudWatch                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

**Vertex**A atribuição é projeto por equipe mais rótulos em todos os lugares. Você modela cada equipe como um projeto GCP, coloca rótulos em cada recurso, e usa BigQuery Billing Export + DataStudio para rolups. Mais trabalho, mas BigQuery dá-lhe SQL arbitrário sobre os dados de custo.

> **Vertex**归因是项目-per-team加无处不在标签―― Você vai construir cada equipe para um GCP 项目, colocar a etiqueta em cada recurso, usando BigQuery Billing Export + DataStudio 进行汇总――工作量更大, mas BigQuery 允许你对成本数据执行任意SQL――

**Azure**baseia-se em escopo de assinatura/grupo de recursos mais tags, com reservas de PTU como um objeto de custo de primeira classe. Tags são herdados de grupos de recursos, não de solicitações, por isso a atribuição por solicitação requer métricas personalizadas de Application Insights ou um gateway que marca cabeçalhos.

> **Azure**Dependendo da subscrição/Ressource Group Role Domain Add tags, PTU  reservado como um objeto de custo de primeira classe.

O padrão: Bedrock é o nativo mais limpo, Vertex é o mais flexível através do BigQuery, Azure é o mais opaco a menos que você use o instrumento.

> 总结:Bedrock 原生最清晰,Vertex 通过 BigQuery 最灵活,Azure 除非自行埋点否则最不透明──

> **【中文解读】**FinOps (WEB é a maior infraestrutura de LLM em baixo valor. Os perfis de Inferência de Aplicação de Bedrock são os mais precisos de atualidade para o gerador original de recursos.

> **【拓展：LLM FinOps 实践】**企业 LLM  spending in 2025 year grew average 300% (Flexera 2025 云状态报告)  Common FinOps 策略包括: 1) 按代币 消耗设置团队预算告警; 2) 使用缓存层(Semantic Cache) reduzir o recorrido de volta em volta em cerca de 30-40%; 3) 模型路由简单任务用小模型、复杂任务用大模型,可节省50%+ 成本; 4) 批量 API 在非实时场景可降低50% 价格;;

### O bloqueio é o risco de 2026

O compromisso de um único hiperescalado estava bem quando um modelo dominava. Em 2026 a fronteira se move mensalmente  Claude 3.7 no primeiro trimestre, Gemini 2.5 no próximo, GPT-5 no trimestre seguinte.

> Quando um modelo é dominado, um único cloud compromete-se também. Em 2026, o modelo de vanguarda é cada mês em mudança.

Os equipes de trabalho de padrão adotam: dois provedores mínimos para qualquer chamada de LLM crítica ao produto. Bedrock mais Azure OpenAI é o par comum  Claude de um, GPT do outro, falha-over entre eles, o mesmo gateway. O aumento de custos é insignificante porque as rotas do gateway são ótimas; o aumento da disponibilidade durante interrupções (como o incidente do Azure OpenAI de janeiro de 2025, a interrupção AWS us-east-1) é decisivo.

> Modelo de adoção da equipe de alta eficiência: qualquer produto chave LLM 调用双供应商最低策略。Bedrock + Azure OpenAI é a combinação mais comum um fornecer Claude, outro fornecer GPT, através do mesmo network connection para realizar falhas de transferência。 O aumento dos custos pode ser ignorado, porque o network connection é o melhor; a disponibilidade aumentada durante o período de 机期 (((como Azure OpenAI ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎  ︎ ︎ ︎  ︎ ︎  ︎  

> **【中文解读】**O maior risco de infraestrutura do ano 2026 é o bloqueio de fornecedores. O modelo de vanguarda está em mudança por trimestre. Q1 usando Claude 3.7, Q2 usando Gemini 2.5, Q3 usando GPT-5. O bloqueio de uma única plataforma significa capacidade de vanguarda de 2/3 da falha. A melhor prática é a estratégia "double supplier minimum": Bedrock + Azure OpenAI é o conjunto mais comum, através de uma rede de blocos, o aumento de custos pode ser ignorado, mas a disponibilidade aumenta significativamente em casos de falhas.

> **【拓展：云厂商宕机事件】**Em janeiro de 2025, o Azure OpenAI sofreu uma falha global de até horas, afetando todos os clientes empresariais de ChatGPT de Azure. No mesmo ano, a AWS us-east-1 também sofreu falhas graves. A estratégia de vários fornecedores provou seu valor em esses eventos: quando um sistema operacional, o conector de rede automaticamente trocará o tráfego para outro, realizando uma falha de percepção.

### Residência de dados, BAAs e indústrias regulamentadas

Bedrock: BAAs na maioria das regiões; pontos finais VPC; barris.
Azure OpenAI: HIPAA, SOC 2, ISO 27001; residência de dados da UE; padrão regulamentado pela empresa.
Vertex: HIPAA, GDPR, residência de dados por região; Google Cloud compliance stack.

> Bedrock: maioria regiões fornecem BAAs; VPC 端点;防护──常见金融科技默认选择──
> Azure OpenAI:HIPAA、SOC 2、ISO 27001; EU dados residentes;
> Vertex:HIPAA, GDPR, conforme dados regionais; Google Cloud's compliance──

As diferenças são nas políticas de retenção de dados, como os registos são manuseados e se o monitoramento de abuso lê o seu tráfego (opt-in por defeito na maioria; opt-out disponível para empresas).

> Os três países que estão em vias de entrar em contato com a legislação nacional são os Estados-Membros que estão em vias de entrar em contato com a legislação nacional.

### Números que você deve lembrar

- TTFT médio do Azure OpenAI em equivalentes Llama 3.1 405B: ~ 50 ms (com PTUs).
  中文翻译:Azure OpenAI 在 Llama 3.1 405B 等效模型上的中位 TTFT:~50ms(使用PTU) 』
- TTFT mediano de cama sob demanda: ~75 ms.
  O seu tempo de trabalho foi de aproximadamente 20 minutos.
- Transmissão de Bedrock: $21-$50/hora por unidade.
  中文翻译:Bedrock Provisioned Throughput:每单位 $21-$50/小时──
- Azure PTU-break-even: ~ 40-60% de utilização sustentada.
  中文翻译:Azure PTU 亏平衡点:~40-60% 持续利用率──
- Poupança de PTU vs. demanda em alta utilização: até 70%.
  Chinese Translation:PTU em alta utilização de tempo em relação ao modo de economia de volume de até 70%

## Use-o com o framework implementado.
```figure
i4-platform-lanes
```

## Usá-lo

`code/main.py`Comparar as três plataformas em uma carga de trabalho sintética  modela economia on-demand vs PTU, variância TTFT e fidelidade de atribuição de custos.

> `code/main.py`Em comparação com três plataformas em carga de trabalho de síntese, a construção de modelos em massa vs PTU economidade TTFT quadratação e custo atribuído à segurança 

> **【中文解读】**实践部分通过模拟工作负载对比三大平台──关键指标包括:TTFT(首代币延迟)、吞吐量、每百万代币 成本──通过调整利用率参数,可以直观看PTU在什么负载水平下比按量计费更划算──

## Envia-o . Produto .

Esta lição produz`outputs/skill-managed-platform-picker.md`. Tendo em conta o perfil da carga de trabalho (modelos necessários, TTFT SLA, volume diário, requisitos de conformidade), recomenda uma plataforma primária, um retorno e um plano de instrumentação FinOps.

> 本课产 出 `outputs/skill-managed-platform-picker.md` fornecer um modelo necessário, SLA TTFT, volume de utilização, requisitos de conformidade,

> **【拓展：生产环境平台选型 Checklist】**O processo de desenvolvimento de um sistema de gestão de dados (SLA) é um processo de desenvolvimento de dados e de dados, que permite a criação de um sistema de gestão de dados e de dados, que permite a criação de um sistema de gestão de dados e de dados.

## Exercícios.

1. Corra .`code/main.py`Em que utilização sustentada o Azure PTU supera a demanda para um modelo de classe 70B?
   Tradução: 运行`code/main.py` O PTU Azure em que nível de utilização contínua é superior ao modelo de classe 70B?
2. O seu produto precisa de Claude 3.7 Sonnet e GPT-4o. Desenhar uma implantação de dois fornecedores que vai para qual hiperescalador, qual gateway fica na frente, qual é a política de falhaover?
   Tradução do inglês para Chinês:Your product needs Claude 3.7 Sonnet 和 GPT-4o。designdouble supplier部署哪到哪个云商,前面放什么网关,故障转移策略是什么?
3. Um cliente de saúde regulado requer BAAs, residência de dados do leste dos EUA e sub-100ms P99 TTFT. Escolha uma plataforma e justifique com três características específicas.
   Um cliente de saúde regulado precisa de BAAs, EUA-Leste e P99 TTFT < 100ms.
4. Descobres que a tua conta da Bedrock aumentou 4 vezes neste mês sem mudanças de tráfego.
   Você encontrou que o volume de pesquisas em Bedrock aumentou 4 vezes, mas o volume não mudou.
5. Leia as páginas de preços do Azure OpenAI e Bedrock. Para uma carga de trabalho Claude de 100 milhões de tokens / mês, que é mais barato  API Antropic direta, Bedrock on-demand ou Bedrock Provisioned Throughput?
   Para 100M de tokens/mês de Claude 工作负载, qual é o mais barato 直接人类 API、Bedrock 按量还是Bedrock Provisioned Throughput?

## Termos-chave .

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

## Mais leitura 延伸阅读

- [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) cartão de taxa autorizada e preços de transferência fornecidos.
- [Azure OpenAI Service Pricing](https://azure.microsoft.com/en-us/pricing/details/azure-openai/) Economia da PTU e cartões de taxas.
- [Vertex AI Generative AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) Níveis Gemini e cobranças adicionais para o Model Garden.
- [Artificial Analysis LLM Leaderboard](https://artificialanalysis.ai/) Referências contínuas de latência e de rendimento entre os prestadores.
- [The AI Journal — AWS Bedrock vs Azure OpenAI CTO Guide 2026](https://theaijournal.co/2026/03/aws-bedrock-vs-azure-openai/) quadro de decisão empresarial.
- [Finout — Bedrock vs Vertex vs Azure FinOps](https://www.finout.io/blog/bedrock-vs.-vertex-vs.-azure-cognitive-a-finops-comparison-for-ai-spend) Mecânica de atribuição lado a lado.
