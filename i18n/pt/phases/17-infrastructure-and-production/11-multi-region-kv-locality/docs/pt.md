# Multicorpo Regional LLM Servindo e KV Cache Localidade  多区域 局部性 服务 LLM KV

> O equilíbrio de carga de round-robin é ativamente prejudicial para a inferência LLM em cache. Uma solicitação que não aterrissa no nó que mantém seu prefixo paga preenchimento total  aproximadamente 800 ms em P50 em um prompt longo versus ~ 80 ms com um cache hit. Em 2026, o padrão de produção é um roteador consciente de cache (vLLM Router in Rust, llm-d router) que consome eventos de cache KV e rotas em prefixo-hash match. A pesquisa recente (GORGO) torna a latência de rede transregional um termo explícito no objetivo de roteamento. As ofertas comerciais de "infereção transregional" (infereção transregional Bedrock, gateways multi-cluster GKE) tratam a inferência como opaca  eles lidam com a disponibilidade, não com a TTFT. A JPMorgan e a Clínica Mayo fizeram um falha-over no leste em Novembro de 2024 em 22 minutos. A realidade do DR: 32% das falhas do LLM DR são porque as equipes fizeram backup de pesos, mas esqueceram arquivos de tokenizer ou configurações de quantização.

> **【中文解读】**Este capítulo apresenta o Cache de KV 局部性 跨区域部署 时的 KV 优化策略.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy prefix-cache-aware router simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving), Phase 17 · 06 (SGLang RadixAttention) | **前置知识:** Phase 17 · 04 (vLLM Serving), Phase 17 · 06 (SGLang RadixAttention)

> - Não .**【前置】**O programa de desenvolvimento de um novo sistema de gestão de dados deve ser desenvolvido com um sistema de gestão de dados.
> - Não .**【类比】**多区域 LLM = "连锁餐厅中央厨房"――Round-robin = 随机送单到分店(缓存命中率 0,每次重复做);Cache-aware router = 按前哈希送到已有缓存的分店(命中 80ms vs 未命中 800ms)──JPMorgan/Mayo Clinic 2024 灾备演练 22 分钟切换──失败教学:32% LLM DR 失败因为只备权重忘了代币器量或配置文件清单必须完整──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizagem

- Explique por que as rupturas de equilíbrio de carga em round-robin cacham a inferência e quantifique a penalidade TTFT.
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para o inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe, tradução do inglês para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe, tradução de tradução do árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe o árabe o árabe o árabe o árabe o árabe o árabe o árabe o árabe o árabe o árabe o árabe o árabe árabe o árabe o árabe é o árabe o árabe o árabe é o árabe o árabe o árabe é o árabe o árabe é o árabe o árabe o árabe é o árabe é o árabe o árabe é o árabe o árabe é o árabe é o árabe é o árabe o árabe é o árabe é o árabe é o árabe é o árabe é o árabe é o árabe é o árabe é o árabe é o árabe é o árabe é o árabe é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é
- Diagrama de um roteador consciente de cache: entradas (eventos de cache KV), algoritmo (paralelas de prefixo-hash), tie-breaker (utilização de GPU).
  Tradução do inglês para o inglês: drawings of cache storage (KV) 缓存事件 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法 (KV) 算法) 算法 (KV) 算法) 算法 (KV) 算法) 算法 (V) 算法) 算法 (V) 算法) 算法 (V) 算法) 算法)
- Nomear o driver de falha de 32% de DR para LLMs (arquivos de tokenizer / configurações de quantização faltantes) e indicar uma lista de verificação de DR de três arquivos.
  Chinese:                                                                                                                                                                                                                                                              
- Distinguir as ofertas comerciais transnacionais (Bedrock CRI, GKE Multi-Cluster Gateway) das rotas de veículos de transporte informático.
  中文翻译:区分商业跨区域产品(Bedrock CRI、GKE Multi-Cluster Gateway) com KV 感知路由──

## O problema é o problema da introdução

> **【中文解读】**Os três principais problemas do serviço de LLM são: 1) o equilíbrio de carga de dados de cache de dados da UE, causando a queda da taxa de cache de 70% para 8%; 2) o fracasso de DR DR de 32% da DR DR de LLM foi devido à equipe ter registrado o peso do seu documento, mas esquecido a configuração quantitativa; 3) o dados de dados da UE, o GDPR exige que os dados dos usuários não possam sair da UE, o roteador consciente de cache não pode previamente corresponder às solicitações dos usuários de Paris, que viajará para os EUA-este-1:

> **【拓展：多区域推理的产业实践】**As melhores práticas de implantação de LLM em vários países incluem: 1) Roteador de cache-consciente independente de cada região (vLLM Router / llm-d router), evitar o alto atraso de transferência de KV em toda a região (US-EU RTT 约75ms,US-APAC 约220ms); 2) GORGO Research will network delay as a como um objetivo de desenvolvimento de um programa de desenvolvimento de um sistema de trabalho que otimize o prefill_time + network_latency; 3) inferência transregional de Bedrock e GKE Multi-Cluster Gateway  processar disponibilidade, mas não processar TTFT Você ainda precisa aplicar um router de cache-consciente de camadas.

O seu serviço funciona em US-East-1, US-West-2, e EU-West-1. Você coloca um ALB na frente com round-robin. Prefixo cache taxa de hit na produção cai para 8%. TTFT P50 triplica.

> Seu serviço opera nos EUA-este-1、us-oeste-2 和 eu-oeste-1── você está na frente de ALB fazer rotina de consulta── a taxa de espera de produção anterior caiu para 8%──TTFT P50 翻了三倍──suo vLLM 日志显示每个请求都在支付完整预填充成本──

O round-robin é o ideal para serviços sem estado. A inferência LLM é estadual por design. O cache KV codifica tudo o que o modelo viu. Routing blind é rotear para o cache errado.

> 轮询负载均衡对无状态服务优优――LLM 推理自然是有状态KV 缓存编码了模型看到的一切内容――盲路由就是路由到错误的缓存――

Separadamente, sua equipe tem um plano DR. Você faz backup de pesos do modelo para S3 cross-região. Uma interrupção regional acontece; você tenta falhar; a réplica se recusa a iniciar. Você esqueceu tokenizer.json, a configuração de quantização e a configuração de escalação RoPE estavam em um balde separado que você não sincronizou.

> Por outro lado, sua equipe tem um plano de recuperação de catástrofe. Você vai colocar o modelo em seu peso transregional até S3 e falhas regionais ocorrerão. Você tentará falhas transmissíveis.

O serviço de LLM multi-regional é um problema de cache, um problema de roteamento e um problema de higiene DR  não um problema de equilíbrio de carga.

> O Mestrado em Direito em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em em em em Mestrado em Mestrado em em em em em em em em em em em em em em em em em em Mestrado em em em em em em em em em em em em em Mestrado em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em

## O conceito central.

### Roteamento consciente de cache

> **【中文解读】**Cache-aware 路由工作机制:请求到达后,路由器对前 (如前512 tokens) fazer哈希,查询每个副本" você tem este pré缓存?";;副本通过pub/sub 频道发布 KV Cache 事件(分配/淘汰块),路由器维护前哈希→副本的索引──匹配到则路由到该副本,未匹配则按GPU利用率选择──vLLM Router(Rust 实现,2026 production-stack) support O(1) 寻找,未匹配时回归至最小队列深度──

O roteador seleciona o replicador com a correspondência, fazendo com que o seu dispositivo seja usado para fazer a correção de dados.

> Por favor, leve um sugestão para chegar. Router para o pre (como 512 tokens) fazer hash; pergunta a cada edição "Você tem esse pre cache?"

**vLLM Router**(Rust, 2026 production stack): subscribe a `kv.cache.block_added`eventos, mantém um índice de réplica prefixo-hash →, rotas com O(1) busca.

> **vLLM Router**(Rust,2026 produção-pilha): 订阅 `kv.cache.block_added`事件,维护前哈希 → 副本索引,O(1) 查找路由──无匹配时回归最小队列深度──

**llm-d router**O mesmo padrão, Kubernetes nativo. Publica eventos através da API ControlPlane.

> **llm-d router**O mesmo modo, Kubernetes Origins.

**SGLang RadixAttention**(Fase 17 · 06) é o equivalente intra-replica.

> **SGLang RadixAttention**(Fase 17 · 06) é o equivalente do lado de fora.

### Números

> **【拓展：KV Cache 路由的性能数据】**Diferença de desempenho do KV de vários conjuntos de circuitos: 2K-token 提示在 Llama 3.3 70B FP8 H100 上,cache hit(同副本、前常驻) TTFT ~80ms;cache miss(冷预填) TTFT ~800ms10x 差距──如果路由器在副本间实现 60-80% 的前缓存命中率,可以在 N副本容量下近似单副本性能──区域间 RTT 也是关键因素:us-east-1  us-west-2 ~65ms、us-east-1  eu-west-1 ~75ms、us-east-1  东-1 ~220ms 跨区域路由只在远远的网络中延迟才才时.

TTFT P50 em um sinal de 2K, Llama 3.3 70B FP8, H100:
- Cachegueiro (sima réplica, prefixo residente): ~80 ms.
- Falha de cache (preenchimento a frio): ~ 800 ms.

Se o seu roteador atingir 60-80% do cache de prefixos em réplicas, você aproxima o desempenho de uma única réplica na capacidade de N-replica. Se atingir 10%, você aproxima a escalação ingênua.

> 2K-token 提示在 Llama 3.3 70B FP8 H100 上的 TTFT P50:缓存命中(同副本,前常驻) 约80ms;缓存未命中(冷预填充) 约800ms──10倍差距──

### Trans-região tem uma nova restrição  latência de rede

RTT interregional:
- US-East-1  US-West-2: ~65 ms.
- EUA-Leste-1  Eu-Oeste-1: ~75 ms.
- US-East-1  ap-southeast-1: ~ 220 ms.

Se o roteamento leva uma solicitação de us-east-1 para um prefixo quente em ap-southeast-1, o prefill guardado (800 → 80 ms) é envenenado por 440 ms viagem de ida e volta.`prefill_time + network_latency`A resposta é manter o roteamento regional, exceto em prefixos massivos de vários MB onde prefill domina.

> 区域间 RTT:us-east-1  us-west-2 约 65ms;us-east-1  eu-west-1 约 75ms;us-east-1  ap-southeast-1 约 220ms;;`prefill_time + network_latency`A resposta é geralmente manter a regionalização do caminho, a menos que a pré-reempenha seja predominante em um grande número de MB.

### A "infereção transregional" comercial não ajuda aqui

A inferência transregional AWS Bedrock encaminha automaticamente as solicitações para outras regiões durante a pressão de capacidade. Optimiza a disponibilidade, não o TTFT, e trata a inferência como opaca.

> AWS Bedrock 跨区域推理在容量压力下自动将请求路由到其他区域――它优化可用性而不是 TTFT,将推理视为不透明――GKE Multi-Cluster Gateway 也是如此服务级故障转移,不感知 KV 缓存――

Ainda precisa de um roteador de cache de camada de aplicativo mesmo quando usas estes. Eles lidam com o caso "us-east-1 está em chamas". Roteamento de cache-consciente lidam com o caso TTFT.

> Mesmo usando estes produtos, você ainda precisa de aplicar camadas de cache de sensorização de routers.

### DR higiene  o problema dos arquivos faltantes de 32%

> **【中文解读】**DR 卫生的三文件最低清单:(1) HF 模型仓库下的所有文件(权重 + 配置 + 分词器);(2) 引擎特定服务配置(vllm_config.yaml等);(3) 部署清单(K8s YAML、Dockerfile、依赖锁文件) ⋅加上:

> **【拓展：LLM 灾难恢复最佳实践】**A prática fundamental do LLM DR de 2026 é: 1) modelo de produção completa não é apenas um documento de peso, contém também tokenizer.json、quantize_config.json、RoPE 缩放配置、聊天模板; 2) transregional同步S3 replicação transregional Usado para modelo de armazenagem, garantir que todas as regiões tenham um副本完整; 3) automação DR 测试 usando Chaos Engineering; 4) RTO 目标企业级 LLM 服务通常要求 RTO < 30 分钟.

Estatisticas de 2026 citadas amplamente: 32% das falhas de LLM DR acontecem porque as equipes fizeram backup de pesos, mas esqueceram:

- `tokenizer.json`ou `tokenizer.model`
- Configurações de quantização (`quantize_config.json`, escalas AWQ, pontos zero GPTQ)
- Configurações específicas do modelo (escalagem RoPE, máscaras de atenção, modelos de bate-papo)
- Configuração do motor (`vllm_config.yaml`, padrões de amostragem, manifesto de adaptador LoRA)

> Estatísticas de 2026: 32% da MLL Catástrofe de recuperação falhou porque a equipe reservou o peso, mas esqueceu:

A correcção é um manifesto mínimo de DR de três arquivos:

1. Todos os arquivos sob o modelo HF repo (pesos + configurações + tokenizer).
2. Configuração de serviço específica do motor.
3. Manifesto de implantação (K8s YAML, Dockerfile, bloqueio de dependência).

> 修复方案是三文件最低 DR 清单:(1) HF 模型仓库下的所有文件(权重 + 配置 + 分词器);(2) 引擎特定服务配置;(3) 部署清单(K8s YAML、Dockerfile、依赖锁文件) ⋅

O exercício do JPMorgan US-East-1 recuperou 22 minutos em novembro de 2024 só porque o livro de jogo foi ensaiado.

> Além disso, cada trimestre de execução DR 演练――JPMorgan 2024 年 11 月 US-East-1 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演练 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 演 了 演 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了 了

### Residência de dados é ortogonal

O cliente PHI da UE não pode sair da UE. Se o seu roteador consciente do cache enviar uma solicitação de Paris para us-east-1 para uma correspondência de prefixo, você violou o GDPR independentemente do ganho TTFT. Partir roteadores por fronteira de residência antes de otimizar o cache.

> Se o seu caixe de percepção de roteiro enviar uma solicitação de origem para o leste dos EUA-1 para realizar uma correspondência, independentemente do que o TTFT possa beneficiar, você já infringiu o GDPR.

### Números que você deve lembrar

- Cache hit vs miss TTFT gap: ~ 10x (80 ms vs 800 ms em 2K prompt).
- RTT interregional EUA-UE: ~75 ms.
- Falha de DR: 32% falha em configurações de tokenizer/quantico.
- JPMorgan us-east-1 falha de nov. 2024: 22 minutos (30 minutos SLA).

## Use-o com o framework implementado.
```figure
cache-aware-router
```

## Usá-lo

`code/main.py`Simula três estratégias de roteamento (round-robin, cache-consciente regional, cache-consciente global) em uma carga de trabalho multi-região.

> `code/main.py`Em vários sectores, a Comissão tem como objetivo:

## Envia-o . Produto .

Esta lição produz`outputs/skill-multi-region-router.md`- Tendo em conta as regiões, as restrições de residência e a SLA, elabora um plano de rotação.

> 本课产 出 `outputs/skill-multi-region-router.md` Provisões de desenvolvimento e desenvolvimento de sistemas de gestão de infraestruturas.

## Exercícios.

1. Corra .`code/main.py`A que comprimento de rotação interregional supera a rotação local, dada a RTT de 75 ms?
   Tradução: 运行`code/main.py`❖ Dado 75ms RTT, em que ponto a longitud do caminho transversal é melhor do que o caminho local?
2. A taxa de acessos no cache cai de 70% para 12%. Diagnóstico de três possíveis causas e os observaveis que confirmam cada uma.
   Tradução do inglês: Your Casualty Life Rate (TRA) - 70% - 12%
3. Desenhar um manifesto DR para um modelo 70B AWQ-quantizado servido em vLLM com 5 adaptadores LoRA. Lista todos os arquivos e configuração.
   Para vLLM há 5 LoRA 适配器的70B AWQ 量化模型设计 DR 清单──列出每个文件和配置──
4.    O estudo foi publicado em 18 de janeiro de 2012 e foi publicado em 18 de janeiro de 2012 no periódico The New York Times.
   O que é o problema com o sistema de transferência de dados?
5. Uma solicitação de origem de Paris corresponde a um prefixo no EUA-Leste-1.
   Tradução do inglês para o português: a petição de um oriente de Paris em EUA-oeste-1 匹配到前──你路由它吗?写出策略──

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Cache-aware routing | "smart LB" | Route on prefix-hash match to KV-cache-holding replica |
| KV-cache events | "cache pub-sub" | Replicas publish block add/evict; router indexes |
| Prefix hash | "cache key" | Hash of first N tokens used as router lookup |
| GORGO | "cross-region routing research" | arXiv 2602.11688; network latency as explicit term |
| Cross-region inference | "Bedrock CRI" | AWS product; availability failover, not TTFT awareness |
| DR manifest | "the backup list" | Every file needed to restore — not just weights |
| Data residency | "GDPR boundary" | Legal constraint on which region sees user data |
| RTT | "round-trip time" | Network latency; 75 ms US-EU, 220 ms US-APAC |
| LLM-aware LB | "cache-hit LB" | Cache-aware router as a product category |

## Mais leitura 延伸阅读

- [BentoML — Multi-cloud and cross-region inference](https://bentoml.com/llm/infrastructure-and-operations/multi-cloud-and-cross-region-inference)
- [arXiv — GORGO (2602.11688)](https://arxiv.org/html/2602.11688v1) Reutilização de caché KV transnacional com prazo de latência da rede.
- [TianPan — Multi-Region LLM Serving Cache Locality](https://tianpan.co/blog/2026-04-17-multi-region-llm-serving-data-residency-routing)
- [AWS Bedrock Cross-Region Inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) Documentação de falha de disponibilidade.
- [vLLM Production Stack Router](https://github.com/vllm-project/production-stack) Fonte de roteador consciente de cache.
