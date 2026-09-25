# AI Gateways  LiteLLM, Portkey, Kong AI Gateway, Bifrost 网关 LLM

> Um gateway fica entre os seus aplicativos e os provedores de modelos. As características principais são roteamento do provedor, retrocesso, retestes, limitação de taxa, referências secretas, observabilidade, guardrails. Divisão do mercado em 2026: **LiteLLM**é MIT OSS com mais de 100 provedores, compatível com OpenAI, mas quebra em torno de ~ 2000 RPS (8 GB de memória, falhas em cascata em benchmarks publicados); melhor para Python, <500 RPS, desenvolvimento / prototipagem. **Portkey**é posicionado no plano de controle (guardrails, redação de PII, detecção de jailbreak, trilhas de auditoria), foi Apache 2.0 de código aberto Março de 2026, 20-40 ms de latência overhead, $49/mo production tier. **Kong AI Gateway** built on Kong Gateway — Kong's own benchmark on same 12 CPUs: 228% faster than Portkey, 859% faster than LiteLLM; $Preço de 100/modelo/mês (máximo 5 no nível Plus); adequado para empresas se já estiver no Kong. **Bifrost**(Maxim AI)  Retemps automáticos com back-off configurável, fallback para Anthropic em OpenAI 429. **Cloudflare / Vercel AI Gateways** gerenciado, zero-ops, retry básico. Residência de dados impulsiona a decisão de auto-host; Portkey e Kong sentam no meio com OSS + opcional gerenciado.

> **【中文解读】**Este capítulo apresenta a IA 网关LLM Pedidos de rotação, equilíbrio de carga e segurança 网关


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy gateway-routing simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 16 (Model Routing) | **前置知识:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 16 (Model Routing)

> - Não .**【前置】**O processo de desenvolvimento de um sistema de gestão de dados é um processo de desenvolvimento de dados e de dados.
> - Não .**【类比】**AI Gateway = "AI 流量交警"。LiteLLM = 开源 MIT 100+ provedor, mas < 500 RPS 适合;Portkey = 控制面(PII 脱敏/越狱检测/审计) $49/月;Kong = 性能王(自家基准比 Portkey 快 228%、比 LiteLLM 快 859%),适合已使用的企业;Bifrost = 自动重试+按回退;Cloudflare/Vercel = 托管运维;;
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizagem

- Enumerar as seis características principais do gateway (routing, fallback, retries, limites de taxa, segredos, observabilidade, barris).
  Chinese Language Translation:列举六个核心网关功能 (→ "Restaurante" em chinês)
- Mapear quatro gateways 2026 (LiteLLM, Portkey, Kong AI, Bifrost) para escalar limites e casos de uso.
  Chinese:将四个 2026 年网关 (LiteLLM、Portkey、Kong AI、Bifrost) mapeamento até escala de escala.
- Cite o índice de referência Kong (228% contra Portkey, 859% contra LiteLLM) e explique por que é importante para > 500 RPS.
  Não é importante que o seu tempo seja de >500 RPS.
- Escolha auto-hosted versus gerenciado dada a residência de dados e orçamento de operações.
  Tradução do inglês para o inglês: given determined data residence and运维预算,选择自托管vs托管──

## O problema é o problema da introdução

> **【中文解读】**A AI 网关 está localizada entre aplicativos e fornecedores de modelos, o problema central de solução é a gestão de vários fornecedores. Os produtos simultaneamente utilizam o OpenAI, o Antropic e o autototável Llama, cada fornecedor tem diferentes SDKs, modelos errados, restrições de velocidade e programas de certificação.

> **【拓展：2026 年 AI 网关市场】**Os quatro principais jogadores do mercado de AI 网关:(1) LiteLLMMIT 开源,100+ provedores, mas em ~2000 RPS 时崩(8GB 内存);(2) Portkey2026 3月开源 Apache 2.0,控制面定位(guardrails、PII 脱敏、越狱检测、审计追踪),20-40ms 延迟开销;(3) Kong AI Gateway 基于成熟 API 网关产品,Kong 基准测试显示自己的Portkey 快 228%、比 LiteLLM 快 859%;(4) Cloudflare/Vercel AI Gateway 托管、零运维、边缘部署;;

O seu produto chama OpenAI, Anthropic e um Llama auto-hosted. Cada provedor tem um SDK diferente, modelo de erro, limite de taxa e esquema de auth. Você quer falha (se OpenAI 429, tente Anthropic), uma única loja de credenciais, observabilidade unificada e limites de taxa por inquilino.

Reinventando isso na camada de aplicativos, cada serviço é associado a cada provedor. Uma camada de gateway consolida-o em um processo com uma API (normalmente compatível com o OpenAI) que é divulgada aos provedores.

## O conceito central.

### Seis características principais

1. **Provider routing** OpenAI, Anthropic, Gemini, auto-hosted, etc. por trás de uma API.
2. **Fallback** em 429, 5xx, ou falha de qualidade, tente novamente em outro lugar.
3. **Retries**- O back-off exponencial, tentativas limitadas.
4. **Rate limits**- Por inquilino, por chave, por modelo.
5. **Secret references** extrair as credenciais do cofre no tempo de execução (nunca no aplicativo).
6. **Observability** ATRITUDOS OTEL + GenAI (Fase 17 · 13) + ATRITUÇÃO DE COSTOS.
7. **Guardrails** Reduzir PII, detectar jailbreak, filtros de tópicos permitidos.

### LiteLLM  MIT OSS, Python

- 100+ provedores, compatíveis com o OpenAI, configuração do roteador, retrocesso, observabilidade básica.
- Desfez cerca de 2000 RPS no ponto de referência de Kong; 8 GB de memória, falhas em cascata sob carga sustentada.
- Melhor ajuste: aplicativo Python, < 500 RPS, gateways de desenvolvimento/estagem, roteamento experimental.
- Custo: $0 para OSS; nível livre de nuvem existe.

### Portkey  posicionamento do plano de controlo

- Apache 2.0 OSS a partir de março de 2026.
- 20-40 ms por pedido de atraso.
- $49/mo para nível de produção com retenção + SLA.
- O melhor ajuste: indústrias regulamentadas que necessitam de barris de segurança + observabilidade agrupada.

### Kong AI Gateway  o jogo de escala

- Construído no Kong Gateway (produto de gateway API maduro, lua+OpenResty).
- O próprio índice de referência da Kong no equivalente a 12 CPUs: 228% mais rápido que o Portkey, 859% mais rápido que o LiteLLM.
- Preço: 100 dólares por modelo por mês, máximo 5 no nível Plus.
- Melhor ajuste: já em Kong; > 1000 RPS; disposto a licenciar.

### Bifrost (Maxim AI)

- Reintentos automáticos com back-off configurável.
- O Fallback para Anthropic no OpenAI 429 é uma receita canônica.
- Novos participantes, comerciais.

### Cloudflare AI Gateway / Vercel AI Gateway

- Re-ataque básico e observabilidade.
- Melhor ajuste: aplicativos JavaScript que servem Edge no Cloudflare/Vercel.
- Limitado em comparação com Kong/Portkey em barris e limites de taxa.

### Auto-hosted versus gerenciado

> **【中文解读】**O sistema de gestão de dados é um dos principais factores de decisão em relação ao sistema de gestão de dados. O sistema de gestão de dados é um sistema de gestão de dados.

> **【拓展：网关 + 可观测性 + 路由的组合】**Fase 17·13(可观测性) + 16(模型路由) + 19(网关) está na produção é da mesma camada.

Residência de dados é a função forçante. saúde e finanças auto-host padrão (LiteLLM ou Portkey OSS ou Kong). produtos de consumo gerenciados por padrão (Cloudflare AI Gateway) ou de nível médio (Portkey gerenciado). híbrido: auto-hosted para inquilino regulamentado, gerenciado para outros.

### Orçamento de latência

> **【拓展：AI 网关延迟预算分析】**AI 网关延迟直接影响TTFT,是选型的关键因素. ]]> 2026年各网关的延迟开销:(1) LiteLLM 5-15msPython 实现,简单但高并发下不稳定;(2) Portkey 20-40ms功能最全面但延迟最高;(3) Kong 3-8msGo + OpenResty,延迟最低且高并发稳定;(4) Cloudflare/Vercel 1-3ms边缘部署优势;;

- LiteLLM: 5-15 ms de carga normal.
- 20-40 ms em cima.
- 3 a 8 ms em cima.
- Cloudflare/Vercel: 1-3 ms de custo geral (vantagem de ponta).

A latência do gateway adiciona-se diretamente ao TTFT. Para TTFT P99 < 100 ms SLA, Kong ou Cloudflare. Para P99 < 500 ms, qualquer.

### Materia semântica de limite de taxa

O token-bucket simples funciona até uma escala moderada. Multi-tenant requer janela deslizante + allocação de explosão + tiering por tenente. LiteLLM navega token-bucket; Kong navega janela deslizante; Portkey navega em camadas.

### Gateway + observabilidade + roteamento compõe

Fase 17 · 13 (observabilidade) + 16 (routing modelo) + 19 (gateways) são a mesma camada na produção. Escolha uma ferramenta que cobre todas as três ou cableá-las cuidadosamente: a maioria das implementações de 2026 combina Helicone (observabilidade) ou Portkey (garda) com Kong (escala) para papéis divididos.

### Números que você deve lembrar

- LiteLLM: quebra em ~ 2000 RPS, memória de 8 GB.
- Portkey: 20-40 ms de custo; Apache 2.0 desde março de 2026.
- Kong: 228% mais rápido que Portkey, 859% mais rápido que LiteLLM.
- Preço Kong: 100 dólares por modelo por mês, 5 max no nível Plus.
- Cloudflare/Vercel: 1-3 ms de carga no limite.

## Use-o com o framework implementado.
```figure
mx-gateway-fallback
```

## Usá-lo

`code/main.py`Simula o roteamento de gateway com fallback em 3 provedores sob injeção 429/5xx. Relata latência, taxa de retiro e taxa de impacto de fallback.

> `code/main.py`Simula o roteamento de gateway com fallback em 3 provedores sob injeção 429/5xx. Relata latência, taxa de retiro e taxa de impacto de fallback.

> `code/main.py`Simula o roteamento de gateway com fallback em 3 provedores sob injeção 429/5xx. Relata latência, taxa de retiro e taxa de impacto de fallback.

## Envia-o . Produto .

Esta lição produz`outputs/skill-gateway-picker.md`Dada a escala, a postura das operações, a conformidade, o orçamento de latência, escolhe um portal.

> 本课产 出 `outputs/skill-gateway-picker.md`Dada a escala, a postura das operações, a conformidade, o orçamento de latência, escolhe um portal.

## Exercícios.

1. Corra .`code/main.py`Configurar fallback de OpenAI→Anthropic→auto-hosted. Qual é a taxa de impacto esperada com taxa de erro de fornecedor de 5%?
   Tradução: 运行`code/main.py`Configuração OpenAI -> Antropic -> Autotúbio de regresso. Qual é a condição de desenvolvimento mais razoável?
2. O seu SLA é TTFT P99 < 200 ms em uma linha de base de 300 ms. Quais gateways mantêm dentro do orçamento?
   Chinese Translation: Seu SLA está em 300ms 基线上的 TTFT P99 < 200ms── quais são as redes que estão dentro do orçamento?
3. Um cliente de saúde precisa de auto-hosting + redação de PII + auditoria.
   中文翻译:一个医疗保健客户需要自托管 + PII 脱敏 + 审计――选择 Portkey OSS 或 Kong――
4. Comparar LiteLLM vs Kong: a que limite máximo de RPS deve migrar uma equipa?
   Comparar LiteLLM vs Kong: equipe em que RPS acima limite deve mudar?
5. Desenhar uma política de limite de taxas para um SaaS multi-arrendatário: nível gratuito, nível de teste, nível pago. Token-bucket ou janela deslizante?

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Gateway | "API broker" | Process sitting between apps and providers |
| LiteLLM | "the MIT one" | Python OSS, 100+ providers, breaks at 2K RPS |
| Portkey | "guardrails gateway" | Control plane + observability, Apache 2.0 |
| Kong AI Gateway | "the scale one" | Built on Kong Gateway, benchmark leader |
| Bifrost | "Maxim's gateway" | Retries + Anthropic fallback recipe |
| Cloudflare AI Gateway | "edge managed" | Edge-deployed managed gateway, zero-ops |
| PII redaction | "data scrub" | Regex + NER mask before sending to model |
| Jailbreak detection | "prompt injection guard" | Classifier on user input |
| Audit trail | "regulated log" | Immutable record of every LLM call |
| Token-bucket | "simple rate limit" | Refill-based rate limiter |
| Sliding-window | "precise rate limit" | Time-windowed rate limiter; better fairness |

## Mais leitura 延伸阅读

- [Kong AI Gateway Benchmark](https://konghq.com/blog/engineering/ai-gateway-benchmark-kong-ai-gateway-portkey-litellm)
- [TrueFoundry — AI Gateways 2026 Comparison](https://www.truefoundry.com/blog/a-definitive-guide-to-ai-gateways-in-2026-competitive-landscape-comparison)
- [Techsy — Top LLM Gateway Tools 2026](https://techsy.io/en/blog/best-llm-gateway-tools)
- [LiteLLM GitHub](https://github.com/BerriAI/litellm)
- [Portkey GitHub](https://github.com/Portkey-AI/gateway)
- [Kong AI Gateway docs](https://docs.konghq.com/gateway/latest/ai-gateway/)
