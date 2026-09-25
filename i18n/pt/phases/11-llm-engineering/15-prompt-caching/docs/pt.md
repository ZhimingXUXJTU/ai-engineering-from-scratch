# Cachagem de contato e contato em cache.

> O seu sistema de memória é de 4.000 tokens. Seu contexto RAG é de 20.000 tokens. Você envia ambos com cada solicitação. Você também paga por ambos  toda vez. O cache rápido permite que o provedor mantenha esse prefixo quente do seu lado e lhe faça uma taxa de 10% da taxa normal em reutilização. Usado corretamente, reduz o custo de inferência em 5090% e a latência do primeiro token em 4085%.

> **【中文解读】**系统提示4000 token + RAG 上下文20000 token, por pedido deve ser pago. 提示缓存让供应商保留前,重用时只收取10%费用.

> **【拓展：提示缓存→RAG生产优化】**A resposta em cache do Antropic Prompte Caching e OpenAI é a técnica chave para reduzir os custos do sistema de produção RAG, especialmente com a sugestão de sistemas fixos e uma grande quantidade de pesquisas.

> - Não .**【前置】**O projeto de desenvolvimento de um sistema de gestão de dados e de dados é um dos principais objetivos da empresa.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 01 (Prompt Engineering), Phase 11 · 05 (Context Engineering), Phase 11 · 11 (Caching and Cost) | **前置知识:** Phase 11 · 01 (提示工程)、05 (上下文工程)、11 (缓存与成本)
**Time:** ~60 minutes | **时间:** ~60 分钟

## O problema é o problema da introdução

Um agente de codificação envia o mesmo aviso de 15 mil tokens para Claude em cada turno de uma conversa.$3/M input tokens is $Multiplica por 10.000 conversas diárias e a conta chega a US$ 9.000 por dia por texto que nunca muda.

> Um agente programador em cada conversa, em cada conversa, envia os mesmos 15.000 tokens para Claude.$3/M 输入 token，仅输入成本就是 $0,90 também não inclui as mensagens reais do usuário.

Não se pode reduzir o pedido sem prejudicar a qualidade. Não se pode evitar enviá-lo  o modelo precisa dele em cada turno.

> Não se pode reduzir a oferta sem prejudicar a qualidade. Não se pode evitar enviar a oferta. A única maneira de parar de pagar o preço total do fornecedor é pagar o preço total.

> - Não .**【类比】**Caching rápido 像"快递公司记住你的常用地址"第一次发货要详细说明"北京市朝阳区...",之后每次发货只需说"老地方",快递公司自动调出地址──技术上:供应商把前的KV缓存存在自己的服务器,下次请求来时直接复用,不需要重新计算注意的K/V矩阵──对用户透明你只需在API调用加个`cache_control`- Não.

> ️ **【易错点】**Cachagem rápida de 3 个坑:(1) **prefix 顺序敏感**cache 命中要求 prefix 完全相同(incluindo空格、换行), sistema prompt 末尾多一个空格就错过;务必把可变部分(user输入)放最后。(2) **cache TTL 5 分钟**Antropic 默认 5 分钟过期,没流量时 cache 失效; usou TTL prolongado(1 小时) 保住冷启动场景──(3) **没监控命中率** não saber o que é o resultado  não saber o que é o resultado `cache_creation_input_tokens`和 `cache_read_input_tokens`, registado até o painel de controlo.

Essa medida é o caching rápido. A Anthropic lançou em agosto de 2024 (com uma variante de 1 hora de TTL estendida em 2025), a OpenAI automatizou-a no final desse ano, o Google lançou o caching de contexto explícito ao lado do Gemini 1.5, e os três agora oferecem como um recurso de primeira classe em seus modelos de fronteira.

> Este método é sugerir o cache. Antropic lançou o cache em agosto de 2024 e lançou o cache em agosto de 2025.


> **【中文解读】**O valor do caching rápido depende do sistema de caching rápido (normalmente muito longo) e em todos os pedidos não muda.


## O conceito central.

> **【中文解读】**O Quick Caching utiliza as características do LLM 推理 Se vários pedidos compartilham o mesmo prompt anterior, pode-se cessar o KV-cache anterior 计算结果, evitar repetir o cálculo.

> **【拓展：Prompt Caching 的成本节省】**O caching rápido do Antropic irá repetir a entrada anterior, o custo reduzindo cerca de 90%;; funções semelhantes do OpenAI serão cachées para entrada  preço reduzido $0.50/M tokens（原价 $5)。 para sistemas de ponta de 5K tokens + 平均10次重复使用场景,月成本可降低约75%──


![Prompt caching: write once, read cheap](../assets/prompt-caching.svg)

**The mechanic.**Quando o prefixo de uma solicitação coincide com um de uma solicitação recente, o provedor serve o cache KV da execução anterior em vez de recodificar os tokens.

> **机制。**Quando a prévia da solicitação é combinada com a prévia da solicitação recente, o fornecedor fornece KV-cache, em vez de token recodificado, na operação anterior.

**Three provider flavors in 2026.**

| Provider | API style | Hit discount | Write premium | Default TTL | Min cacheable |
|---------|-----------|--------------|---------------|-------------|---------------|
| Anthropic | Explicit `cache_control` markers on content blocks | 90% off input | 25% surcharge | 5 min (extendable to 1 hour) | 1,024 tokens (Sonnet/Opus), 2,048 (Haiku) |
| OpenAI | Automatic prefix detection | 50% off input | none | Up to 1 hour (best-effort) | 1,024 tokens |
| Google (Gemini) | Explicit `CachedContent` API | Storage-billed; read at ~25% of normal | Storage fee per token·hour | User-set (default 1 hour) | 4,096 tokens (Flash), 32,768 (Pro) |

**The invariant.**Os três prefixos de cache apenas. Se qualquer token diferir entre as solicitações, tudo depois do primeiro token diferente é um erro. Coloque as partes * estáveis * no topo, as partes * variáveis * na parte inferior.

> **不变量。**Se houver qualquer token entre os pedidos, o primeiro é diferente, e depois tudo está na sequência.

### O layout de cache-friendly

```
[system prompt]          <-- cache this
[tool definitions]       <-- cache this
[few-shot examples]      <-- cache this
[retrieved documents]    <-- cache if reused, else don't
[conversation history]   <-- cache up to last turn
[current user message]   <-- never cache (different every time)
```

Viola a ordem  colocar a mensagem do usuário acima do prompt do sistema, interromper recuperações dinâmicas entre poucas fotos  e o cache nunca atinge.

>  Contrariamente ao ordenamento  colocará as mensagens do usuário sobre o sistema de sugestões, entre poucos exemplos entre entre entre os registros.

### O cálculo do equilíbrio

O prémio de escrita de 25% da Anthropic significa que um bloco em cache deve ser lido pelo menos duas vezes para economizar dinheiro líquido. 1 escrever + 1 ler média 0,675x custo por solicitação (salva 32%); 1 escrever + 10 ler média 0,205x (salva 80%). Regra de ouro: cache qualquer coisa que você espera reutilizar pelo menos 3 vezes dentro do TTL.

> O 25% do Antropic  write in premium significa que os blocos de cache devem ser lidos pelo menos duas vezes para poderem manter o dinheiro.

## Construí-lo e realizei-o.
```figure
prompt-cache-hit
```

## Construí-lo

### Passo 1: Cachagem de prompt antropópica com marcadores explícitos

```python
import anthropic

client = anthropic.Anthropic()

SYSTEM = [
    {
        "type": "text",
        "text": "You are a senior Python reviewer. Follow the rubric exactly.\n\n" + RUBRIC_15K_TOKENS,
        "cache_control": {"type": "ephemeral"},
    }
]

def review(code: str):
    return client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": code}],
    )
```

O `cache_control`O marcador diz à Anthropic para armazenar o bloco por 5 minutos. Reutilizar dentro dessa janela acerta; reutilizar após expirar e escreve novamente.

> `cache_control`标记告诉 Antropic 将该块存储 5 分钟.

**Response usage fields:**

```python
response = review(code_a)
response.usage
# InputTokensUsage(
#     input_tokens=120,
#     cache_creation_input_tokens=15023,   # paid at 1.25x
#     cache_read_input_tokens=0,
#     output_tokens=340,
# )

response_b = review(code_b)
response_b.usage
# cache_creation_input_tokens=0
# cache_read_input_tokens=15023           # paid at 0.1x
```

Verifique ambos os campos na CI  se `cache_read_input_tokens`mantém-se em zero em todas as solicitações, as tuas chaves de cache estão a drift.

> Em IC, verifique estes dois segmentos se`cache_read_input_tokens`Em várias vezes, mantém-se em zero, a sua chave de arquivo está flutuando.

### Passo 2: TTL prolongado por uma hora

Para os trabalhos de longa duração, o prazo de 5 minutos expirará entre os trabalhos.`ttl`- Não .

```python
{"type": "text", "text": RUBRIC, "cache_control": {"type": "ephemeral", "ttl": "1h"}}
```

O TTL de 1 hora custa o dobro da prima de escrita (50% em relação à linha de base em vez de 25%) mas retribui rapidamente em qualquer lote que reutilize o prefixo mais de 5 vezes.

> 1 小时 TTL é de 2 vezes mais elevado do que 50% do nível de base, não mais de 25%), mas é muito rápido em qualquer reutilização anterior a 5 vezes mais do que no tratamento em lote.

### Passo 3: Caché automático OpenAI

Qualquer prefixo acima de 1.024 tokens que corresponda a uma solicitação recente recebe automaticamente um desconto de 50%.

```python
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},   # long and stable
        {"role": "user", "content": user_msg},
    ],
)
resp.usage.prompt_tokens_details.cached_tokens  # the discounted portion
```

A mesma regra de layout amigável ao cache aplica-se. Duas coisas matam o cache da OpenAI que não matam o Anthropic: alterando o `user`campo (utilizado como componente de chave de cache) e ferramentas de reordenação.

> As regras de configuração são as mesmas. Duas coisas matam a cache de OpenAI e não matam a Anthropic.`user`字段和重新排序工具──

### Passo 4: Gemini cache de contexto explícito

O Gemini trata o cache como um objeto de primeira classe que você cria e nomeia:

```python
from google import genai
from google.genai import types

client = genai.Client()

cache = client.caches.create(
    model="gemini-3-pro",
    config=types.CreateCachedContentConfig(
        display_name="rubric-v3",
        system_instruction=RUBRIC,
        contents=[FEW_SHOT_EXAMPLES],
        ttl="3600s",
    ),
)

resp = client.models.generate_content(
    model="gemini-3-pro",
    contents=["Review this code:\n" + code],
    config=types.GenerateContentConfig(cached_content=cache.name),
)
```

O Gemini cobra armazenamento por token·hora durante o tempo que o cache vive e lê a ~25% da taxa de entrada normal. Esta é a forma certa quando você reutiliza o mesmo prompt gigante em várias sessões ao longo de dias.

> Gemini 按缓存存活期间每代币·小时收取存储费,读取费率约为正常输入的25%──当你在多次会议中跨天重复使用相同的大型提示时,这是正确的选择──

### Passo 5: medição da taxa de impacto na produção

Veja .`code/main.py`Para uma contabilidade simulada de três provedores que acompanha as contagens de escrita/leitura/malfatura e calcula o custo misturado por 1K solicitações.

> - Não .`code/main.py`获取模拟的三供应商会计师,跟踪写入/读取/未命中计数并计算每千请求的混合成本──按目标命中率门控部署多数生产 预热后应见 >80% 读取比例──

## Encurralagens que ainda se lançam em 2026

> A queda de 2026 continua a ocorrer:

- **Dynamic timestamps at the top.** `"Current time: 2026-04-22 15:30:02"`Cada pedido falha, move as marcas de tempo abaixo do ponto de ruptura do cache.
  **顶部的动态时间戳。**系统提示顶部放  sistema de informação`"Current time: 2026-04-22 15:30:02"`                                                                                                                                                                                                                                                              
- **Tool reordering.**Serialize as ferramentas em uma ordem estável  um reorganização entre as implementações quebra cada golpe.
  **工具重排序。**E estabilizar a ordem de ordem de ferramentas de ordenação de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens de ordens
- **Free-text near-duplicates.**"Você é útil". vs "Você é um assistente útil".  Uma diferença de 1 byte = total falta.
  **自由文本近似重复。**"Você é útil". vs "Você é um assistente útil".
- **Too-small blocks.**O Anthropic impõe um piso de 1.024 tokens (2.048 para Haiku).
  **过小的块。**Antropic 强制 1,024 token 下限(Haiku 为 2,048)。更小的块静默不缓存。
- **Blind cost dashboards.**Divide "tokens de entrada" em caché versus não caché.
  **盲目的成本仪表板。**Colocar o "token de entrada" em cache vs. não cache.

## Use-o com o framework implementado.

A pilha de armazenamento em cache de 2026:

> 2026 缓存技术:

| Situation | Pick |
|-----------|------|
| Agent with stable 10k+ system prompt, many turns | Anthropic `cache_control` with 5-min TTL |
| Batch job reusing a prefix for 30+ minutes | Anthropic with `ttl: "1h"` |
| Serverless endpoints on GPT-5, no custom infra | OpenAI automatic (just make your prefix stable and long) |
| Multi-day reuse of a giant code/doc corpus | Gemini explicit `CachedContent` |
| Cross-provider fallback | Keep the cacheable prefix layout identical across providers so any hit works |

| 场景 | 选择 |
|------|------|
| Agent 有稳定 10k+ 系统提示、多轮 | Anthropic `cache_control` 配 5 分钟 TTL |
| 批处理重用前缀 30+ 分钟 | Anthropic 配 `ttl: "1h"` |
| GPT-5 上的无服务器端点、无定制基建 | OpenAI 自动（让前缀稳定且够长） |
| 多天重用大型代码/文档语料 | Gemini 显式 `CachedContent` |
| 跨提供商回退 | 跨提供商保持可缓存前缀布局一致，任何命中都工作 |

Combinar com o caching semântico (Fase 11 · 11) para a camada de mensagem do usuário: manuais de caching de prompt *token-identical* reutilização, manuais de caching semântico *meaning-identical* reutilização.

> Compreensão de dados e informações sobre o uso de dados e informações sobre o usuário

## Envia-o . Produto .

Salvar`outputs/skill-prompt-caching-planner.md`- Não .

```markdown
---
name: prompt-caching-planner
description: Design a cache-friendly prompt layout and pick the right provider caching mode.
version: 1.0.0
phase: 11
lesson: 15
tags: [llm-engineering, caching, cost]
---

Given a prompt (system + tools + few-shot + retrieval + history + user) and a usage profile (requests per hour, TTL needed, provider), output:

1. Layout. Reordered sections with a single cache breakpoint marked; explain which sections are stable, which are volatile.
2. Provider mode. Anthropic cache_control, OpenAI automatic, or Gemini CachedContent. Justify from TTL and reuse pattern.
3. Break-even. Expected reads per write within TTL; net cost vs no-cache with math.
4. Verification plan. CI assertion that cache_read_input_tokens > 0 on the second identical request; dashboard split by cached vs uncached tokens.
5. Failure modes. List the three most likely reasons the cache will miss in this setup (dynamic timestamp, tool reorder, near-duplicate text) and how you will prevent each.

Refuse to ship a cache plan that places a dynamic field above the breakpoint. Refuse to enable 1h TTL without a reuse count that makes the 2x write premium pay back.
```

## Exercícios.

1. **Easy.**Faça uma conversa de 10 voltas com um sistema de 5.000 tokens contra o Claude.`cache_control`Relata a conta de entrada de cada token.
   取一个10轮对话和5000代币 系统提示,不使用和使用 `cache_control`分別运行, relatório输入 token 费用──
2. **Medium.**Escrever um arame de teste que, dada uma template de solicitação e um registro de solicitação, calcule a taxa de sucesso esperada e a economia de dólares por fornecedor (Anthropic 5m, Anthropic 1h, OpenAI automático, Gemini explícito).
    redação de ferramentas de teste, formulários de orientação e diários de solicitação, cálculo da taxa de sorteo e da economia de cada fornecedor
3. **Hard.**Construir um optimizador de layout: dado um prompt e uma lista de campos marcados `stable=True/False`, reescrever o prompt para colocar um único ponto de ruptura de cache na posição máxima de cache-friendly sem perder informações. Verificar em um endpoint real Antropic.
   构建布局优化器:重写提示将缓存断点放在最大缓存友好位置――

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Prompt caching | "Makes long prompts cheap" / "让长提示变便宜" | Reusing a provider-side KV-cache for matching prefixes; 50-90% discount on repeated input tokens. | 提示缓存：重用供应商端的 KV-cache，对重复输入 token 提供 50-90% 折扣 |
| `cache_control` | "The Anthropic marker" / "Anthropic 标记" | Content-block attribute that declares "everything up to here is cacheable"; `{"type": "ephemeral"}`. | cache_control：内容块属性，声明"到这里为止的内容可缓存" |
| Cache write | "Paying the premium" / "付溢价" | The first request that populates the cache; billed at ~1.25x input rate on Anthropic, free on OpenAI. | 缓存写入：第一次填充缓存的请求 |
| Cache read | "The discount" / "折扣" | Subsequent requests matching the prefix; billed at 10% (Anthropic), 50% (OpenAI), ~25% (Gemini). | 缓存读取：匹配前缀的后续请求 |
| TTL | "How long it lives" / "存活时间" | Seconds the cache stays warm; Anthropic 5m default (extendable 1h), OpenAI best-effort up to 1h, Gemini user-set. | TTL：缓存保持活跃的秒数 |
| Extended TTL | "1-hour Anthropic cache" / "1小时缓存" | `{"type": "ephemeral", "ttl": "1h"}`; 2x write premium but worth it for batch reuse. | 扩展 TTL：1 小时缓存，2 倍写入溢价 |
| Prefix match | "Why my cache missed" / "为什么缓存未命中" | Caches only hit when every token from the start up to the breakpoint is byte-identical. | 前缀匹配：缓存只在从开头到断点的每个 token 完全相同时才命中 |
| Context caching (Gemini) | "The explicit one" / "显式缓存" | Google's named, storage-billed cache object; best for multi-day reuse of large corpora. | 上下文缓存 (Gemini)：命名、按存储计费的缓存对象 |

## Mais leitura 延伸阅读

- [Anthropic — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)- Não .`cache_control`, 1h TTL, desdobrar as mesas.
  Antropic 提示缓存文档cache_control、1 小时 TTL、亏平衡表──
- [OpenAI — Prompt caching](https://platform.openai.com/docs/guides/prompt-caching) correspondência automática de prefixos.
  OpenAI 提示缓存文档自动前匹配──
- [Google — Context caching](https://ai.google.dev/gemini-api/docs/caching)- Não .`CachedContent`API e preços de armazenamento.
  Google 上下文缓存文档CachedContent API 和存储定价──
- [Anthropic engineering — Prompt caching for long-context workloads](https://www.anthropic.com/news/prompt-caching) post de lançamento original com números de latência.
  Antropic 工程博客长上下文工作负载的提示缓存,含延迟数据──
- Fase 11 · 05 (Engenharia de contexto)  onde cortar o prompt para que o cache possa aterrar.
  Seção 11 - 05 (construção)
- Fase 11 · 11 (Cachagem e Custos)  par de prompt caching com um cache semântico nas mensagens do usuário.
  Seção 11 阶段 · 11(缓存与成本)                                                                                                                                                                                                                                                        
- [Pope et al., "Efficiently Scaling Transformer Inference" (2022)](https://arxiv.org/abs/2211.05102) o modelo de memória KV-cache que solicita o cache expõe aos usuários; explica por que um prefixo em cache é ~ 10x mais barato para ler novamente do que para recomputar.
  Explicação de por que o cache é 10 vezes mais barato do que o KV-cache.
- [Agrawal et al., "SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills" (2023)](https://arxiv.org/abs/2308.16369) prefill é o ponto de urgência de cache atalhos; este artigo explica por que TTFT cai dramaticamente no cache hit enquanto TPOT não é afetado.
  Explicação de por que a TTFT em fase de caça foi muito baixa e a TPOT não foi afetada.
- [Leviathan et al., "Fast Inference from Transformers via Speculative Decoding" (2023)](https://arxiv.org/abs/2211.17192) o cache rápido fica ao lado da descodificação especulativa, da atenção flash e da MQA/GQA como alavancas que dobram a curva de custo de inferência; leia isto para os outros três.
  提示缓存与投机解码、Flash Attention 和 MQA/GQA 并列的推理成本曲线杆──
