# SGLang e RadixAttenção para Prefixos Pesados Cargas de Trabalho
# Prefixo-Cache Servindo  RadixAttenção e KV Reutilização

> Trate o cache KV como um recurso reutilizável de primeira classe armazenado em uma árvore de radix e muda a programação com ele: em vez de FCFS (primeiro-chegado, primeiro servido) como agendas vLLM, um cronista consciente do cache priorizará solicitações com prefixos compartilhados mais longos  efetivamente uma profundidade-primeira travessia de radix para que os ramos quentes permaneçam residentes no HBM. O SGLang é o motor que construiu a ideia. No Llama 3.1 8B com as instruções de 1K parecidas com o ShareGPT, o SGLang chega a ~ 16.200 tok/s para ~ 12.500 do vLLM, uma vantagem de ~ 29%. Nas cargas de trabalho RAG de prefixo pesado, a vantagem atinge 6,4x. Nas cargas de trabalho em forma de clonagem de voz, a taxa de acessos no cache foi limpa em 86%. Implementado em mais de 400.000 GPUs em 2026 em xAI, LinkedIn, Cursor, Oracle, GCP, Azure, AWS. O problema é que o número 6.4x evapora quando o prefixo de ordem é inconsistente.

> **【中文解读】**Este capítulo apresenta o SGLang e RadixAttention  através de 
**Type:** Learn
**Languages:** Python (stdlib, toy radix-tree cache + cache-aware scheduler)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 14 (Agentic RAG)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy radix-tree cache + cache-aware scheduler) | **语言:** Python（标准库，radix tree 缓存 + 缓存感知调度器模拟）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 14 (Agentic RAG) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 14（Agentic RAG）

> - Não .**【前置】**学本节前请先掌握:Fase 17·04(vLLM) 、Fase 14(Agentic RAG) ・SGLang Usando árvore de radix 复用 KV cache比vLLM FCFS 更智能的调度。
> - Não .**【类比】**SGLang RadixAttention = "memória biblioteca"。vLLM = Cada vez mais re-visualizar o catálogo;SGLang = 热门前(sistema提示+RAG context)存 radix tree 复用。Llama 3.1 8B 在 ShareGPT 上比 vLLM 快 29%;RAG 工作负载快 6.4 倍;语音克隆场景缓存命中 86%──2026 部署在40万+ GPU(xAI、LinkedIn、Cursor)──关键:前必须稳定排序才有效──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Diagrama RadixAttenção: como os prefixos são armazenados em uma árvore radix e como os blocos KV são compartilhados entre sequências enraizadas no mesmo ramo.
  No entanto, o que é que o bloco de KV é compartilhado entre os outros?
- Explique a programação consciente do cache e por que o FCFS é errado para o tráfego pesado de prefixos.
  Tradução do inglês para tradução do inglês: Explain cache storage sensitivity调度 and why FCFS for pre密集流量 is erroneous.
- Calcule a aceleração esperada para uma carga de trabalho dada a taxa de acidente do prefixo-cache e a distribuição de comprimento imediata.
  Tradução do inglês para o inglês: given determination 缓存命中率和快速 长度分布,计算工作负载的预期加速──
- Nomear a disciplina de ordenação rápida que faz o número 6.4x real versus um lado positivo perdido.
  Chinese:                                                                                                                                                                                                                                                              

## O problema é o problema da introdução

> **【中文解读】**O serviço tradicional de sugestão irá fazer cada pedido imediatamente 视为不透明 Mesmo 5000 RAGs Petições de partilha do mesmo 2000 tokens 系统提示, vLLM também executará 5000 vezes prefill completo. RadixAttention 通过将 token 序列存储在radix tree 中解决这个问题: 新请求沿树匹配已有前,只需预填新增的后部分──挑战在调度FCFS(先来先服务) 破坏前局部性,需要缓存意识调度器优先服务共享前的请求──

> **【拓展：前缀共享在 Agent 场景的价值】**Agente 工作负载天然具有前共享特征:系统提示、工具方案、少数shot示例、对话历史跨请求重复──Cursor(AI 代码编辑器) em 2026 report its Agent 调用中系统提示 + 工具定义占据快速的80%,仅用户查询部分不同── após usar RadixAttention 后, estes parcerias 后只需计算一次,后续请求复用KV Cache,将推理成本降低60-80%──

O serviço clássico trata o prompt de cada solicitação como opaco. Mesmo quando 5.000 solicitações RAG começam com o mesmo prompt de sistema de 2.000 tokens mais o mesmo preâmbulo de recuperação, vLLM preenche o prefixo de 2.000 tokens 5.000 vezes.

> O serviço clássico irá preencher cada pedido de imediato, mesmo que 5.000 RAG pedidos sejam feitos com os mesmos 2.000 tokens.

A observação: as instruções em cargas de trabalho agencias e RAG compartilham quase sempre prefixos longos. Pronto de sistema, esquemas de ferramentas, exemplos de poucas fotos, cabeçalhos de recuperação, histórico de conversação  todas repetem-se em todas as solicitações. Se você armazenou o cache KV para esse prefixo uma vez e o reutilizou, você não o preencheria novamente.

> Observação: Agente e RAG  Pronto na carga de trabalho  quase sempre                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

A RadixAttention faz exatamente isso. Os tokens são indexados em uma árvore radix; cada nó possui blocos KV para a sequência de token em seu caminho da raiz. Uma nova solicitação percorre a árvore: qualquer nó cujo token corresponde reutiliza os blocos KV desse nó. O custo de preenchimento torna-se proporcional ao sufixo "novo", não o prompt completo.

> RadixAttention está fazendo isso. Token em árvore de radix. Indicação; cada nodo possui o KV blocos da sequência de tokens da rotação da raiz para a rotação. Novo pedido através do árvore: qualquer token 匹配的节点复用该节点的 KV块.

O desafio é agendar. Se duas solicitações compartilham um prefixo de 2.000 tokens e um terceiro compartilha apenas 200 tokens do mesmo prefixo, você quer servir as duas solicitações compartilhadas longamente juntas para que o prefixo longo permaneça no HBM. FCFS faz o oposto  ele serve quem chegou primeiro, potencialmente despejando o ramo quente antes que o próximo pedido de prefixo longo atinja.

> O desafio está na regulação. Se dois pedidos compartilhamos 2.000 tokens, o terceiro apenas compartilhamos 200 tokens, você quer servir simultaneamente dois pedidos compartilhados para manter o longo prazo no HBM.

## O conceito central.

### A árvore de radix como índice de KV

> **【中文解读】**Árvore de Radix (Radix tree) é a estrutura de dados central do SGLang. Cada ponto tem um token de alcance e de resposta a blocos de KV. Novos pedidos para entrar em tempo de correspondência: sistema de orientação de ponto de correspondência reutilizar 124 blocos de KV, documento de divisão de correspondência reutilizar 31 blocos, apenas para o novo problema distribuir 4-6 blocos. Por exemplo, 160 blocos de total, árvore de radix apenas precisa de 4 blocos de nova calculação.

Uma árvore de radix (trie compacto) armazena sequências de tokens. Cada nó possui um intervalo de tokens e os blocos KV calculados para esse intervalo.

> Árvore de Radix (紧前树) sequência de tokens de armazenamento. Cada um dos pontos tem um token.

```
root
 |- "You are a helpful assistant..."  (2,000 tokens, 124 KV blocks)
      |- "Context: <doc A>..."        (500 tokens, 31 blocks)
           |- "Question: Alice..."    (80 tokens, 5 blocks)
           |- "Question: Bob..."      (95 tokens, 6 blocks)
      |- "Context: <doc B>..."        (520 tokens, 33 blocks)
```

Um novo pedido vem com o sistema prompt + "Contexto: <doc A>" + "Question: Carol". O cronista executa: prefixo do sistema coincide (124 blocos reutilizados), doc-A branca coincide (31 blocos reutilizados), então atribui blocos novos apenas para "Question: Carol" (4 blocos). Prefill custo: 4 blocos de novos tokens. Sem a árvore: 160 blocos. ~40x economia em prefill.

> Uma nova solicitação com um sistema de sugestões + "Contexto: <doc A>" + "Question: Carol" 进入──调度器遍历:系统前匹配(复用124块),doc-A 分支匹配(复用31块),然后只为 "Question: Carol" 分配新块(4块)──预填成本:4块新代币──没有树:160块──预填节省约40倍──

### Programação de cache

> **【中文解读】**As duas estratégias-chave da modulação de percepção de cache: 1) a profundidade da prioridade da prioridade do serviço com o pedido de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de partilha de

Reutilização com a base de árvore Radix não tem sentido se o cache se desfechar.

> Se o cache continua a funcionar, o root tree 支持的复用毫无意义―― duas estratégias-chave:

1. **Depth-first dispatch**Quando escolher a próxima solicitação da fila, prefira solicitações enraizadas no mesmo ramo que o conjunto de execução atual. Isso mantém o ramo quente fixado.
   Tradução:**深度优先调度**◊ Quando escolher o próximo pedido da linha, priorizar a escolha com o pedido do grupo de execução e da cadeia.
2. **LRU at branch level, not block level**. Eliminar ramos inteiros (a partir das folhas mais curtas utilizadas) em vez de blocos individuais, para que a forma do cache coincida com a forma do radix.
   Tradução:**分支级 LRU**❖ eliminação de toda a secção (~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Um pedido de compartilhamento de 2.000 tokens fica atrás de um pedido de compartilhamento de 50, e depois a filial de 2.000 tokens é despejada para admitir a de 50.

> FCFS 违反两者──一共享2000代币请求排在共享50代币请求后面,然后2000代币分支被淘汰以接受50代币请求──

### Números de referência que você deve memorizar

- Llama 3.1 8B, H100, ShareGPT 1K: SGLang ~ 16.200 tok/s vs vLLM ~ 12.500 (~ 29% vantagem).
  Llama 3.1 8B,H100,ShareGPT 1K prompt:SGLang 约 16,200 tok/s vs vLLM 约 12,500(约 29% 优势)。
- RAG com prefixo pesado (seme sistema + mesmo documento, pergunta variada): até 6,4x no SGLang.
  O sistema de dados é o que é o sistema de dados.
- Cargas de trabalho de clonagem de voz: taxa de acessos de prefixos em cache de 86,4%.
  Tradução do inglês para tradução livre:
- Taxas de impacto da produção em todos os clientes da SGLang: 50-99% dependendo da disciplina imediata.
  Chinese:SGLang 客户的生产命中率:50-99%, depende do rápido 排序纪律──
- Deployado em 400.000+ GPUs em 2026.
  Chinese:                                                                                                                                                                                                                                                              

### O pedido te apanhou.

> **【中文解读】**6.4x aceleração dependendo da ordem de um modelo de sugestão.`[system, tools, context, history, question]`, às vezes construído .`[system, context, tools, history, question]`,radix tree  não pode encontrar o mesmo tipo de informação para o ser humano, para o árvore radix são duas séries diferentes.

> **【拓展：SGLang 在生产中的采用】**SGLang em 2026 já foi implantado em mais de 400.000 blocos de GPU, os usuários incluem xAI(Grok)、LinkedIn、Cursor、Oracle, bem como o serviço de administração do GCP/Azure/AWS。 o cenário de vantagem central é o de Agente e RAG 工作负载

O número 6.4x depende de um pedido consistente de modelo de pedido.`[system, tools, context, history, question]`em alguns pedidos e `[system, context, tools, history, question]`O que parece um prefixo compartilhado para um ser humano são duas sequências distintas para a árvore radíx.

> 6.4x Número depende de um prompt de acordo 模板排序── Se o seu cliente em certas solicitações construção `[system, tools, context, history, question]`, entre outros pedidos`[system, context, tools, history, question]`Para os seres humanos, a árvore é comum, para a árvore radix, são duas categorias diferentes.

Lever do engenheiro: seu modelo de pedido é uma chave de cache. Fique a ordem. Coloque tudo imutável (sistema, ferramentas, esquemas) em primeiro lugar. Coloque o contexto de recuperação em segundo lugar. Coloque a pergunta do usuário em último lugar. Não deixe conteúdo dinâmico no prefixo.

> 工程师的杆:你的提示 模板是缓存键──固定顺序──将所有不可变内容(系统、工具、schema) 放最前──检索上下文放中间──用户问题放最后──不要在可缓存前中交错动态内容──

Caso real da pesquisa: o movimento de conteúdo dinâmico para fora do prefixo cacheável levou uma implantação de 7% para 74% taxa de hits de cache em uma mudança.

> O caso real do estudo: o desenvolvimento de conteúdos em movimento para a fase de armazenamento, a taxa de armazenamento de armazenamento de uma vez em cada fase, aumentou de 7% para 74%.

### Onde a RadixAttention ganha e perde

> **【拓展：RadixAttention vs Prefix Caching 性能对比】**SGLang vs vLLM's anterior performance de cache comparado: em Llama 3.1 8B H100, SGLang  alcançou ~16,200 tok/s vs vLLM ~12,500 tok/s  29%                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

Ganhos:
- RAG (seme preâmbulo de recuperação, pergunta variada).
  Tradução do inglês para grego:RAG(相同检索前,不同问题)
- Agentes (mesmo esquema de ferramentas, consulta variada).
  中文翻译:Agent (Agent) 相同工具方案,不同查询) 
- Chat com o sistema de alargamento.
  Tradução do idioma:长系统提示的聊天──
- Cargas de trabalho de voz/visão com preámbulos repetidos.
  Tradução do inglês:重复前的语音/视觉工作负载──

Perdas (retorna à capacidade de transmissão a nível vLLM):
- Geração de um só momento com instruções únicas (completo de código, chat aberto sem instrução do sistema).
  Tradução do inglês para o inglês: independente prompt 的单次生成 ((代码补全、无系统提示的开放聊天) 』
- Instruções dinâmicas onde cada solicitação interliga conteúdo único no prefixo.
  Tradução do inglês para o inglês: Each request in a available cache before in交错独特内容的动态 prompt──

### Por que é um problema de cronograma, não apenas um problema de núcleo

Você pode implementar a reutilização de KV como um truque do kernel. A visão da SGLang é que a reutilização só paga se o cronógrafo mantém o ramo quente residente. Uma política ingênua de "reutilização se disponível" vai fazer o cache sob carga mista. O cronógrafo indexado por árvore radix é o que transforma o truque do kernel em uma vantagem de produção de 29%.

> Você pode implementar KV  duplo para técnicas de kernel. SGLang's insight is duplo only in the regulator to keep hot split branches constantly.

### Interação com o vLLM

Os dois sistemas não são concorrentes estritais.`--enable-prefix-caching`O espaço foi fechado, mas não desapareceu completamente. A pilha inteira do SGLang é radix-first; o vLLM o enxertou. Para cargas de trabalho dominadas pela reutilização de prefixos, o SGLang permanece o padrão. Para serviços de finalidade geral sem padrões de prefixos fortes, o vLLM permanece igual ou melhor.

> 两个系统不是严格竞争者──2026年 vLLM 添加了前缓存(`--enable-prefix-caching`O sistema de roteador de roteador de roteadores de roteadores de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros de roteiros

## Use-o com o framework implementado.
```figure
roofline
```

## Usá-lo

`code/main.py`Implementa um cache KV de brinquedo radix-tree mais um cronógrafo com duas políticas: FCFS e cache-consciente. Executa a mesma carga de trabalho através de ambos, relata taxa de acidente de prefixo-cache e delta de throughput.

> `code/main.py`实现一模拟基根树 KV 缓存加两个策略调度器:FCFS 和缓存感知──用两者运行相同工作负载,报告前缓存命中率和吞吐量差异──然后运行"乱序排序"工作负载展示 6.4x 崩──

## Envia-o . Produto .

> **【拓展：前缀缓存策略选择】**2026 ano 缓存有三个层次:(1) 应用级语义缓存(Phase 17·14) 在调用 LLM 前用嵌入相似度匹配历史响应,命中率 10-70%;(2) 服务端前缓存(SGLang RadixAttention / vLLM prefix caching) 重复使用 KV Cache,10x 延迟降低;(3) 跨节点缓存路由(Phase 17·11) 通过缓存-awaren router将请求路由由由到持有前的副本──三者可以叠加:语义缓存 →避免 LLM 调用 端端前缓存避免重复预填 → 跨节点路由避免请求配

Esta lição produz`outputs/skill-radix-scheduler-advisor.md`. Dada uma descrição da carga de trabalho (forma do modelo de solicitação, padrão de recuperação, número de inquilinos simultâneos), produz uma prescrição de solicitação de solicitação e uma indicação de saída para a adopção do SGLang.

> 本课产 出 `outputs/skill-radix-scheduler-advisor.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                                                                                         

## Exercícios.

1. Corra .`code/main.py`Comparar FCFS e cache-consciente na mesma carga de trabalho. Onde vem o delta de  pre-fill poupança, decodificação poupança ou atraso na fila?
   Tradução: 运行`code/main.py` Comparar o FCFS com o Cachem no mesmo trabalho.
2. Modificar a carga de trabalho para que as instruções de permuta aleatória `[system, tools, context]`- O que acontece com a taxa de impacto?
   Tradução do inglês: Modificar`[system, tools, context]`O que é que se passa na taxa de destino?
3. Calcule o custo do HBM de manter um sistema de 2.000 tokens como um ramo de radix no Llama 3.1 8B. Compare com o custo de um lote de 16 sequências sem reutilização de prefixos.
   Chinese Translation:计算在 Llama 3.1 8B 上保持 2,000 token 系统提示作为一个基因 分支常驻的HBM 成本──与无前复用16序列批次成本比较──
4. Leia o artigo SGLang RadixAttention. Explique em três frases por que o despejo de LRU em forma de árvore é melhor que o LRU em forma de bloco sob carga pesada de prefixo.
   中文翻译:阅读 SGLang RadixAttention 论文──用三句话解释为什么树形 LRU 淘汰在前密集负载下优于块形 LRU──
5. Um cliente relata apenas 8% de taxa de cache.
   Tradução do inglês para o inglês: Client report only 8% 缓存命中率──说出三个可能原因和每个诊断方法──

## Termos-chave .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| RadixAttention | "the SGLang thing" / "SGLang 的那个" | KV cache indexed as a radix tree so shared prefixes reuse blocks / KV 缓存以 radix tree 索引，共享前缀复用块 |
| Radix tree | "compact trie" / "紧凑前缀树" | Tree where each node owns a token range and its KV blocks / 每个节点拥有 token 范围和 KV 块的树 |
| Cache-aware scheduler | "hot-branch-first" / "热分支优先" | Scheduler that prefers requests sharing the resident branch / 优先服务共享常驻分支请求的调度器 |
| Prefix-cache hit rate | "how much of your prompt was free" / "prompt 多少是免费的" | Fraction of prompt tokens served from reused KV blocks / 从复用 KV 块服务的 prompt token 比例 |
| FCFS | "first-come first-served" / "先来先服务" | Default scheduling that breaks prefix locality / 破坏前缀局部性的默认调度 |
| Branch-level LRU | "evict the leaf" / "淘汰叶子" | Eviction policy matched to radix shape / 匹配 radix 形状的淘汰策略 |
| Prompt template ordering | "the cache key" / "缓存键" | The prompt's component order determines what the tree can share / prompt 组件顺序决定树能共享什么 |
| System prompt pinning | "resident prefix" / "常驻前缀" | Keep the immutable system portion pinned to avoid eviction thrash / 保持不可变系统部分固定避免淘汰抖动 |

## Mais leitura 延伸阅读

- [SGLang GitHub](https://github.com/sgl-project/sglang) fonte e documentos.
- [SGLang documentation](https://sgl-project.github.io/) RadixAttenção e detalhes de programação.
- [SGLang paper — Efficiently Programming Large Language Models (arXiv:2312.07104)](https://arxiv.org/abs/2312.07104) a referência do projecto.
- [LMSYS blog — SGLang with RadixAttention](https://www.lmsys.org/blog/2024-01-17-sglang/) Números de referência e raciocínio do agendador.
- [vLLM — Prefix Caching](https://docs.vllm.ai/en/latest/features/prefix_caching.html) A própria implementação radix-like do vLLM, para comparação.
