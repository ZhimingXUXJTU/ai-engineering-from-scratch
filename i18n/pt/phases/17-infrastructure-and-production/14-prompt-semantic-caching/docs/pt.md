# Cachagem rápida e Cachagem semântica Economia

> **Pricing snapshot dated 2026-04.**As reivindicações numéricas abaixo refletem os cartões de taxas de fornecedores capturados na publicação desta lição; verifique contra os documentos vinculados antes de citarem-nos para baixo.

> **【中文解读】**Esta secção apresenta a resposta de sugestões de dados para reduzir os custos de cálculo.


> O caching ocorre em duas camadas. L2 (nível de fornecedor) prompt/prefix caching reutiliza atenção KV para prefixos repetidos  Os documentos de caching de prompt da Anthropic anunciam até 90% de redução de custos e 85% de redução de latência em longos pedidos; para Claude 3.5 Sonnet lecturas de cache são $0.30/M vs $3,00/M fresco com um TTL de 5 minutos e um prêmio de escrita de 2x para a opção TTL de 1 hora (docs.anthropic.com, 2026-04). O caching de prompt do OpenAI aplica-se automaticamente para os tokens de prompt ≥1024 e os preços de entrada em caché com aproximadamente um desconto de 90% versus fresco (platform.openai.com, 2026-04); a taxa de caché exata por modelo depende do cartão de taxa ao vivo. L1 (nivel de aplicação) cache semântico salta o LLM inteiramente em incorporar hites de semelhança. Produtor "95% de precisão" refere-se à correção, não à taxa de impacto  as taxas de impacto da produção relatadas variam de 10% (chat aberto) até 70% (FAQ estruturado); nenhum dos provedores publica uma linha de base oficial, por isso trate-as como telemetria comunitária em vez de garantias. As armadilhas de produção: a paralelalização mata o cache (N solicitações paralelas emitidas antes da primeira escrita no cache podem inflar o gasto várias vezes), e o conteúdo dinâmico dentro do prefixo impede que o cache atinja inteiramente. ProjectDiscovery relatou que a taxa de hits passou de 7% para 74% (2025-11) movendo texto dinâmico do prefixo cacheável.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy two-layer cache simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang RadixAttention) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang RadixAttention)
**Time:** ~60 minutes | **时间:** ~60 minutes
**Type:** Learn
**Languages:** Python (stdlib, toy two-layer cache simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 06 (SGLang RadixAttention)
**Time:** ~60 minutes

> - Não .**【前置】**学本节前请先掌握:Fase 17·04(vLLM)、Fase 17·06(RadixAttention)、Fase 11·04(Embutidos Usados para语义缓存)。
> - Não .**【类比】**缓存 = "翻历史聊天记录"──L2 提示缓存(Anthropic/OpenAI) = 服务商帮你存储(90% 成本降,85% 延迟降);L1 语义缓存 = 自己用嵌入 找相似问题直接返回──陷:并行请求会破坏缓存、前里塞动态内容(时间) = 永远命中不了──ProjectDiscovery 把动态文本挪出可存前后,命中 7%率→74%──
> ️ **【易错点】**厂商宣传 "95% 准确率" refere-se à correlação de corretão e não à probabilidade de surto.

## Objetivos de aprendizagem

- Distinguir o caching de prompts/prefixos L2 (reutilização de KV no fornecedor) do caching semântico L1 (bypass de LLM em prompts semelhantes).
  中文翻译:区分 L2提示/前缓存(提供商级 KV 复用) 和 L1语义缓存(相似提示跳过 LLM) 』
- Explica o Anthropic `cache_control`Marcação explícita e as duas opções TTL (5-min vs. 1 hora) com os seus multiplicadores de preço.
  Tradução do idioma:`cache_control`显式标记和两种 TTL 选项(5 分钟 vs 1 小时) e seu preço multiplicado
- Calcule as economias mensais esperadas, dada a taxa de acidente, a combinação de resposta/prompto e os preços dos tokens.
  Tradução do inglês para o inglês: given determinate fortune rate、提示/响应比例和代币价,计算预期月度节省。
- Nomear o padrão anti-paralelalização que infla contas por 5-10x e o padrão anti-conteúdo dinâmico que desmorona taxa de hits.
  Tradução do inglês: "Inflation of the balance sheet" (Inflação do balanço) - "Inflação do balanço" (Inflação do balanço) - "Inflação do balanço" (Inflação do balanço) - "Inflação do balanço" (Inflação do balanço) - "Inflação do balanço" (Inflação do balanço) - "Inflação do balanço" (Inflação do balanço) - "Inflação do balanço" (Inflação do balanço) - "Inflação do balanço" (Inflação do balanço) - "Inflação do balanço" (Inflação do balanço) - "Inflação do balanço" (Inflação do balanço) - "Inflação do balanço" (Inflação do balanço) - "Inflação do balanço" (Inflação do balanço) - "Inflação do balanço" (Inflação do balanço) - "Inflação do balanço" (Inflação) - "Inflação do balanço" (Inflação) - "Inflação do balanço" (Inflação) - "

## O problema é o problema da introdução

> **【中文解读】**提示缓存有两常见失败模式:(1) 并行化反模式Agent 发发出 10 个并行工具调用,所有请求在第一缓存写前达完成,完成前达,10 次写入、0 次读取,账单膨胀 5-10x;(2) 动态内容反模式系统提示中包含当前时间、请求 ID等动态内容,每个请求都唯一,缓存中率 0%──修复方法:将静态内容放缓存前,动态内容放缓边界后──

> **【拓展：提示缓存的经济价值】**提示缓存是 LLM 成本优化中最直接的杆──Antropic 缓存 仅阅读 仅阅读$0.30/M（Claude 3.5 Sonnet），比 fresh input $3.00/M 便宜 10x──OpenAI para ≥1024 tokens de sugestões de caixas automáticas, caixas de entrada são de cerca de 10% do preço da nova entrada──Em produção RAG 系统, a taxa média de caixas de sugestões de sistema compartilhado pode chegar a 60-80%, por mês poupar milhares de dólares──语义缓存(L1) em situações estruturadas FAQ 场景可达 40-70% de vida──

Você adiciona o cache de instruções ao seu serviço RAG. A conta permanece plana. Você mede a taxa de hits; é 7%. As instruções parecem estáticas, mas não são  o prompt do sistema inclui a data atual formatada para o minuto, um ID de solicitação e uma reordem de exemplo aleatório para a diversidade. Cada solicitação escreve uma nova entrada de cache, lê zero.

> **【中文解读】**
> 提示缓存分两层:L2(fourwer级) 重用重复前的 KV cacheAnthropic 声称缓存读取成本降低90%、延迟降低85%;L1(应用级)语义缓存存在嵌入相似度命中时直接跳过LLM。 mas dois反模式会毁掉缓存效果:(1) prompt 中的动态内容(时间、请求 ID) 阻止缓存命中;(2) 并行请求在第一缓存写入前全部到达,导致N 次取写入次读零――

Separadamente, seu agente executa dez chamadas paralelas de ferramentas por pergunta de usuário. Todas as dez chegam ao provedor antes de a primeira escrita em cache ser concluída. Dez escreve, zero lê. Sua conta é 5-10 vezes o que "com cache" deveria custar.

O caching é um protocolo, não uma bandeira.

## O conceito central.

### L2  Cachagem de antecedentes/prefixos do fornecedor

> **【中文解读】**L2 层(提供商级)提示缓存复用重复前的注意力 KV──Antropic 使用显式 `cache_control`标记,TTL 选项有 5 分钟(写入成本 1.25x) 和 1 小时(2x),读取成本仅为新鲜输入的1/10──OpenAI对 ≥1024 token提示自动缓存,无需标记──Google Gemini 通过显式 API 提供语境缓存──自部署方案使用vLLM prefix缓存或SGLang RadixAttention──

O provedor armazena o KV de atenção para um prefixo cacheável e o reutiliza no próximo pedido que corresponda ao prefixo.

**Anthropic (Claude 3.5 / 3.7 / 4 series)**: explícito `cache_control`TTL: 5 minutos (costas de escrita 1,25x base) ou 1 hora (costas de escrita 2x base).$0.30/M on Claude 3.5 Sonnet vs $3,00/M fresco  10 vezes mais barato (docs.anthropic.com, a partir de 2026-04). As tarifas diferem por modelo (Opus/Haiku publicado separadamente); sempre verifique a página de preços ao vivo.

**OpenAI**O sistema de cache automático para as instruções ≥1024 tokens (platform.openai.com, 2026-04). Não há bandeira explícita. A entrada em cache é aproximadamente 10 vezes mais barata do que a nova nas atuais cartões de taxa gpt-4o/gpt-5. Nem os documentos nem as notas de lançamento publicam uma linha de base oficial de taxa de sucesso; relatórios comunitários agrupam cerca de 3060% com um projeto de prompt cuidadoso. Monitor `usage.cached_tokens`Para medir o seu.

**Google (Gemini)**: conteúdo em cache através de API explícito; 1M-token conteúdo significa que o cache paga ainda mais.

**Self-hosted (vLLM, SGLang)**: Fase 17 · 06 abrange o mesmo padrão em seu próprio cálculo.

### L1  Caching semântico a nível de aplicativo

> **【中文解读】**L1 层(应用级)语义缓存在调用 LLM 之前,对提示做哈希和嵌入查找. 如果找到相似度超过值 (通常 0.95+) 的缓存请求,直接返回缓存响应.

Antes de ligar para o LLM, hash o prompt, embude-o e procure uma solicitação similar armazenada em cache (similaridade de cozinho acima do limiar, normalmente 0,95+).

Caso aberto: Redis Vector Similarity, GPTCache, Qdrant. Comércio: Portkey Cache, Helicone Cache.

As alegações de precisão do fornecedor se referem à frequência com que a resposta de cache retornada foi semanticamente apropriada, não à frequência com que você bate.

- Chat aberto: 10-15%.
- FAQ estruturada / apoio: 40-70%.
- Questões de código: 20-30% (variantes pequenas matam os hits).
- Agentes de voz que repetem as instruções: 50-80% (conjunto fixo de normalização de voz).

### O padrão anti-paralelalização

> **【拓展：并行化反模式的真实案例】**Equipe de direção:Agent em direção à Antropic Emitir 10 ferramentas de direção:Compartilhar com uma mesma ferramenta de 4K-token Sistema de sugestões  Antropic em direção a uma máquina de direção:Cache:Escrever em cerca de 300ms  Completar, mas solicitações 2-10 em uma mesma janela de milênio de segundo chegar, cada um vê o cache perdido  Resultado: 10 vezes escrever  Preço  0 vezes ler desconto  Rectificação: sequência: primeiro  Primeiro individual enviar pedido 1, etc. Cache  Reemplenar  Reemplenar  Aumentar 300ms  A primeira ferramenta  Modificar, mas economizar 5-10x  Contacto  Projeto  Desenvolvimento  Desenvolvimento  Desenvolvimento  Mudança  Mudança  Desenvolvimento  Desenvolvimento  Rate  Aumento de 7%  74%  Casos de 11 de novembro de 2025 

O seu agente faz 10 chamadas para ferramentas em paralelo. Todas as 10 têm o mesmo prompt do sistema de tokens 4K. As gravações do cache antropico são por pedido; a primeira gravação do cache completa cerca de 300 ms após o provedor ver o prompt. As solicitações de 2 a 10 chegam na mesma janela de milissegundos e cada uma vê o cache perdido. Você paga 10 prêmios de escrita, 0 descontos de leitura.

Correção: lote com sequencial-first  fazer pedido 1 sozinho, em seguida, disparar 2-10 uma vez que o caché de 1 tem povoado. Adiciona 300 ms para a primeira chamada de ferramenta; salva 5-10x a conta.

### O antipatrão de conteúdo dinâmico

O teu sistema de resposta parece:

```
You are a helpful assistant. The current time is 14:32:17.
User ID: abc123. Today is Tuesday...
```

Cada pedido é único, cada pedido é escrito, zero hits.

Correção: mover tudo realmente estático para o prefixo cacheable; adicionar conteúdo dinâmico após o limite do cache:

```
[cacheable]
You are a helpful assistant. [rules, examples, instructions]
[/cacheable]
[dynamic, not cached]
Current time: 14:32:17. User: abc123.
```

O ProjectDiscovery passou de 7% para 74% da taxa de cache desta forma e publicou a anatomia.

### Batch de pilha + cache para cargas de trabalho noturnas

As APIs de lote (Fase 17 · 15) oferecem 50% de desconto em turnaround de 24 horas. A entrada em cache no topo lhe dá ~ 10x acima disso. As cargas de trabalho de classificação, rotulagem e geração de relatórios durante a noite podem cair para ~ 10% do custo sincrônico-unchedded por empilhamento.

### Números que você deve lembrar

Os pontos de preços são capturados 2026-04 dos documentos dos fornecedores vinculados e são verificados a cada poucos meses antes de dependerem deles.

- Leitura em cache antropico: $0,30/M no Claude 3.5 Sonnet, aproximadamente 10 vezes mais barato do que a entrada fresca (docs.anthropic.com).
- Prêmio de escrita de cache antropópica: 1,25x (5-min TTL) ou 2x (1-hora TTL).
- O caché automático OpenAI: aplica-se a pedidos ≥ 1024 tokens; entrada em caché com preço de aproximadamente 10% da entrada nova em cartões de taxa corrente (platform.openai.com).
- Taxa de hits de cache semântico (relatado pela comunidade): ~ 10% aberto chat; até ~ 70% FAQ estruturada. Não uma linha de base documentada pelo fornecedor.
- ProjectDiscovery: 7% → 74% taxa de acidentes movendo dinâmica do prefixo (blog do projeto, 2025-11).
- Anti-patrão de paralelalização: relatórios típicos de inflação de contas 510x quando N solicitações paralelas perdem a primeira escrita cache.

## Use-o com o framework implementado.

> **【中文解读】**
> O melhor método de análise é de fazer um teste de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de um sistema de dados de dados de um sistema de dados de dados de um sistema de dados de dados de um sistema de dados de dados de um sistema de dados de dados de um sistema de dados de dados de dados de um sistema de dados de dados de dados de um sistema de dados de dados de dados de um sistema de dados de dados de dados de um sistema de dados de dados de dados de dados de um sistema de dados de dados de dados de dados de um sistema de dados de dados de dados de dados.`cache_control`标记静态前──实测案例:把动态内容移出缓存前,命中率从7% 跳到74%──对于RAG 系统,静态系统提示 + 检索到的文档属于缓存范围,用户问题不属于──

> **【拓展：提示缓存→成本优化】**提示缓存是 LLM 成本优化最直接的手段──Anthropic Claude 的缓存读取价格为 $0.30/M token，不到新鲜输入 $O sistema de armazenamento de dados pode reduzir a contabilidade mensal da API de centenas de milhares de dólares para centenas de milhares de dólares.
```figure
semantic-cache-hit
```

## Usá-lo

`code/main.py`Simula o cache L1 + L2 em cargas de trabalho mistas.

> `code/main.py`Simula o cache L1 + L2 em cargas de trabalho mistas.

> `code/main.py`Simula o cache L1 + L2 em cargas de trabalho mistas.

## Envia-o . Produto .

> **【拓展：缓存 + 批处理叠加优化】**缓存与批处理 API(Fase 17·15) 叠加效果:批处理 API 50% 折扣 + 缓存输入 ~10x 折扣 = 约10% 的同步未缓存成本──隔夜分类、标签和报告生成工作负载可通过叠加这些两种优化降至基准约10%──关键是将提示模板视为缓存键修复排序、移动内容态,这是最容易忽视但最有效的优化──

Esta lição produz`outputs/skill-cache-auditor.md`- Tendo em conta o modelo e o tráfego, verifica a cachéabilidade e recomenda a reestruturação.

> 本课产 出 `outputs/skill-cache-auditor.md`- Tendo em conta o modelo e o tráfego, verifica a cachéabilidade e recomenda a reestruturação.

## Exercícios.

1. Corra .`code/main.py`- O que é que a lei muda?
   Tradução: 运行`code/main.py`◊ trocar e fazer a rotina ◊ expandir a conta?
2. O seu sistema de solicitação tem uma data.
   Tradução do inglês para o inglês: Your system提示包含日期──将它移出──展示前后命中率数学──
3. Calcule o equilíbrio de 1 hora de TTL (2x escrever) vs 5 minutos de TTL (1.25x escrever) dada a taxa de chegada do pedido.
   O resultado foi o resultado de uma análise de custos de produção de uma empresa de investimento.
4. O cache semântico no limiar de 0,95 atinge 20%. No 0,85 atinge 50% mas você vê respostas armazenadas em cache incorretas. Escolha o limiar certo e justifique.
   Chinese Translation:语义缓存值 0.95 时命中率 20%──0.85 时命中率 50% Mas você vai ver幻觉──值设多少?
5. Você faz 10 subqueries paralelas por pergunta de usuário. Reescrever para a facilidade de cache sem adicionar latência de ponta a ponta.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| L2 prompt cache | "prefix cache" | Provider stores KV for repeated prefix |
| `cache_control` | "Anthropic cache marker" | Explicit attribute marking cacheable blocks |
| Cache write premium | "write tax" | Extra cost for first miss-to-cache (1.25x or 2x) |
| L1 semantic cache | "embedding cache" | App-level hash-and-embed before calling LLM |
| GPTCache | "LLM caching lib" | Popular OSS L1 cache library |
| Cache hit rate | "hits / total" | Fraction of requests served from cache |
| Parallelization anti-pattern | "the N-write trap" | N parallel requests miss cache N times |
| Dynamic content trap | "the time-in-prompt trap" | Dynamic bytes in prefix kill hit rate |
| RadixAttention | "intra-replica cache" | SGLang's prefix-cache implementation |

## Mais leitura 延伸阅读

- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) oficial `cache_control`semântica e TTL.
- [OpenAI Prompt Caching](https://platform.openai.com/docs/guides/prompt-caching) comportamento de cache automático e elegibilidade.
- [TianPan — Semantic Caching for LLMs Production](https://tianpan.co/blog/2026-04-10-semantic-caching-llm-production)
- [ProjectDiscovery — Cut LLM Costs 59% With Prompt Caching](https://projectdiscovery.io/blog/how-we-cut-llm-cost-with-prompt-caching)
- [DigitalOcean / Anthropic — Prompt Caching](https://www.digitalocean.com/blog/prompt-caching-with-digital-ocean)
