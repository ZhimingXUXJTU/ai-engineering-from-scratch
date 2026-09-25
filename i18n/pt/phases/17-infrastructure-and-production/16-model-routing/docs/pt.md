# Modelo de roteamento como um custo-reduzimento primitivo

> Um corretor dinâmico avalia cada solicitação (tipo de tarefa, comprimento de token, semelhança de inserção, confiança) e envia consultas simples para um modelo barato, aumentando as complexas para um modelo de fronteira. Também chamado de cascata de modelos. Os estudos de caso de produção mostram uma redução de custos de 20-60% na iso-qualidade em todas as implementações dos EUA/Reino Unido/UE; uma melhoria de eficiência de roteamento de 30% em SaaS de grande volume transforma-se em economias anuais de seis dígitos. O contexto de 2026 é que os preços de inferência LLM caíram ~ 10x por ano  um token de classe GPT-4 foi de $20/M to ~$0,40/M, de finais de 2022 a 2026. A maior parte da queda é melhor servindo pilhas (fase 17 · 04-09), não hardware. O roteamento é como você converte essa queda de preço em margem sem regressão do produto. O modo de falha é a deriva do modelo barato: a rota empurra 40% para um modelo mais fraco, a qualidade cai de 3-5% nas tarefas de raciocínio, ninguém percebe por um quarto. Roteiras de portal por métricas de qualidade online, não apenas conjuntos de avaliação offline.

> **【中文解读】**Esta secção apresenta estratégias de otimização de custos de diferentes modelos de escolha de modelos de acordo com a complexidade das tarefas.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cascading router simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 19 (AI Gateways) | **前置知识:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 19 (AI Gateways)

> - Não .**【前置】**学本节前 請先掌握:Fase 17·01(托管平台) ‧Fase 17·19(AI Gateway) 』模型路由 = 动态 bróker 按任务复杂度选便宜或贵模型──
> - Não .**【类比】**模型路由 = "医院分诊"──简单感冒→社区医生(Haiku/Sonnet);疑难杂症→专家(Opus);急诊→主任(GPT-4)──20-60% 成本降,30% 路由效率改进=六位数年省──背景:LLM 价格 2022-2026 降10倍/年,多数降来自服务改进而非硬件路由把价格转转变成利──
> ️ **【易错点】**便宜模型漂移:40% 路由到弱模型→推理质量降低 3-5%→ 一季度没人发现──修复:用在线质量监控(不仅离线评估)守住底线──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizagem

- Explique o modelo em cascata: barato primeiro com verificação de confiança, escalada em baixa confiança.
  Tradução do inglês para tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: línguese: línguese: línguese: tradução livre: línguese: línguese
- Enumerar os quatro sinais de roteamento (classificação da tarefa, comprimento da tarefa, incorporação de semelhança com o conjunto de hard-known, autoconfiança a partir da primeira passagem).
  Chinese: 列举四种路由信号 (→ "quatro rotas de sinal")
- Calcular o custo combinado esperado na divisão de roteamento-alvo e na tolerância à perda de qualidade.
  Tradução do inglês para tradução do inglês: calculado objetivo, por meio de um método de cálculo,
- Nomear a métrica de monitoramento de deriva (gate de qualidade on-line) que pega o modelo barato.
  Tradução do inglês em inglês:                                                                                                                                                                                                                                                           

## O problema é o problema da introdução

> **【中文解读】**模型路由的核心洞察:70% de consulta é simples ("Paris já está a chegar?", reescrever esta frase"), pode ser tratado com um modelo de Haiku 级 com um custo perfeito de 3% . Apenas 30% . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 

> **【拓展：模型路由的产业案例】**2026 ano modelo route by in production típico resultado: 20-60% Custo reduzido(同质量下) ・ LLM 推理价格从2022年到2026年下降约10x/年(GPT-4 级从$20/M 降到 $0,40/M), a maior parte da redução provém da sugestão de otimização (Fase 17·04-09);; modelo de roteiro para que você capte esses benefícios na aplicação, em vez de esperar que todos os usuários se transferam para um modelo barato;;

O seu serviço custa US$ 80 mil por mês no GPT-5. As suas análises mostram que 70% das perguntas são simples: "qual é a hora em Paris?" "reformula essa frase". Um modelo de classe Haiku lida perfeitamente com 3% do custo. 30% precisa do raciocínio do GPT-5.

Se você encaminhar 70% para barato e 30% para caro, sua conta cai cerca de 65% na mesma qualidade do produto. Isto é encaminhamento. O truque é construir o corretor sem regressar a qualidade.

## O conceito central.

### Quatro sinais de encaminhamento

> **【中文解读】**O sistema de controle de dados é um sistema de controle de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de

1. **Task classification**Pode ser um classificador baseado em regras, um pequeno LLM (Haiku-classe a $ 0,25/M), ou incorporando semelhança com baldes rotulados.

2. **Prompt length**As instruções <500 tokens geralmente não precisam de fronteira para a coerência.

3. **Embedding similarity to known-hard set**Se a consulta estiver próxima (cosin > 0,88) de um balde conhecido de duração, escala directamente para a fronteira.

4. **Self-confidence from first-pass**Se os registos do modelo revelarem baixa confiança OR se ele recusa OR saiba a linguagem de cobertura, tente novamente na fronteira.

### Três padrões

> **【拓展：模型路由的三种模式】**模型路由的三种实现模式对比: 1) Pre-route前置分类器 (规则或小 LLM), aumentar 5-10ms 延迟,总体最快; 2) Cascade先发到廉价模型,低信度时升级到前沿模型,中位延迟约1.2x、升级时约2x,质量底线最好; 3) Ensemble route并行运行廉价和前沿模型,奖励模型选择最佳,最高质量但最高成本──在生产中推 Cascade 作为默认它提供质量,成本,延迟之间最佳平衡──

**Pre-route**(classificador de frente): ~ 5-10ms de latência adicionada; mais rápido em geral.

**Cascade**(mais barato primeiro, em baixa confiança): ~ 1,2x de latência média (excurso barato mais verificação), ~ 2x em escalada.

**Ensemble route**(exercício barato e fronteira em paralelo para uma amostra, escolha de modelo de recompensa): mais alta qualidade, maior custo; utilização apenas para A/B crítica.

### Implementação

As gateways de IA (fase 17 · 19) expõem o roteamento.`router`Configurar com fallback e roteamento de custos. Portkey tem guardas + roteamento. Kong AI Gateway tem roteamento baseado em plugins.

O código aberto: RouteLLM (LMSYS), Não Diamante (comercial), Prompt Mule.

### A curva de preços de 2026

| Model class | Late 2022 | 2026 | Change |
|-------------|-----------|------|--------|
| GPT-4-level quality | ~$20/M | ~$0.40/M | 50x cheaper |
| Frontier (GPT-5, Claude 4) | — | ~$3-10/M | new tier |

A maior parte da melhoria é a eficiência de serviço  as lições principais na Fase 17 · 04-09 transformadas em quedas de custos do lado do provedor. O roteamento permite capturar esses ganhos na camada de aplicativo em vez de esperar que todos os seus usuários migrem para o nível barato.

### A deriva é o risco real

> **【中文解读】**漂移是模型路由的真正风险──路由将将 40% 发送到廉价模型,6 个月后任务分布变化(用户更成熟、问题更长), mas as classificações do router ainda são baseadas em Q1 dados treinamento──质量下降没有投诉足够响亮,直到在竞争对手的基准测试中落败才知道──必须通过在线质量指标门控制路由:用户反自动LLM 评审;;5% 采样) 升级率、拒绝率──

> **【拓展：模型路由的实现方案】**2026 ano modelo de routes de implementação de opções:(1) AI 网关(Fase 17·19)LiteLLM de roteador configuração Portkey de guardas+routing Kong AI Gateway de plug-in 路由 、OpenRouter de recomendação API;(2) 开源RouteLLM(LMSYS) fornecer uma biblioteca de routes completa;(3) 商业Not Diamond 提供 SaaS 模型路由产品;;

A sua rota envia 40% para o modelo barato. Ao longo de seis meses, a distribuição de tarefas muda (os usuários ficam mais sofisticados, fazem perguntas mais longas). O roteador não percebe porque seu classificador foi treinado em dados do Q1. A qualidade cai silenciosamente. Ninguém se queixa suficientemente alto. Você descobre em um benchmark do concorrente que perdeu.

Roteiras de entrada por métricas de qualidade online:

- Os utilizadores colocam os dedos para cima/para baixo por rota.
- Jury de LLM automatizado numa amostra de retenção (5%) por rota.
- Taxa de escalada: se a cascata estiver a subir mais de 30%, o modelo barato está a ser super-routado.
- Taxa de recusa por rota.

### Números que você deve lembrar

- 2026 poupança de roteamento em iso-qualidade: estudos de caso de 20 a 60%.
- Descenso dos preços dos LLM 2022-2026: ~ 10x ao ano agregado.
- Nível GPT-4 2022 vs 2026: ~$20/M → ~$0,40/M.
- Impacto de latência em cascata: ~ 1,2x média, ~ 2x escalada (~ 10% do tráfego).

## Use-o com o framework implementado.
```figure
model-cascade-router
```

## Usá-lo

`code/main.py`Simula a pré-ruta, a cascata e o conjunto numa carga de trabalho mista.

> `code/main.py`Simula a pré-ruta, a cascata e o conjunto numa carga de trabalho mista.

> `code/main.py`Simula a pré-ruta, a cascata e o conjunto numa carga de trabalho mista.

## Envia-o . Produto .

Esta lição produz`outputs/skill-router-plan.md`- Tendo em conta a carga de trabalho e o orçamento de qualidade, escolhe um padrão de roteamento e sinais.

> 本课产 出 `outputs/skill-router-plan.md`- Tendo em conta a carga de trabalho e o orçamento de qualidade, escolhe um padrão de roteamento e sinais.

## Exercícios.

1. Corra .`code/main.py`Em que piso de precisão a cascata bate o pré-caminho?
   Tradução: 运行`code/main.py`O que é que a linha de ligação é melhor do que a linha de ligação?
2. A sua base de usuários é de 30% empresarial (questões complexas), 70% gratuito (simples).
   Tradução do inglês: 30% é empresa, 70% é livre.
3. Uma rota reduz a qualidade em 2% mas economiza 40%. É um navio?
   Chinese Language Translation: um caminho reduzir a qualidade de 2% Mas poupar 40%...
4. Implementar uma verificação de confiança usando logprobs de OpenAI / APIs antropóficas. Qual é o limiar que você começa com?
   中文翻译: usar OpenAI/Anthropic API de logprobs 实现置信度检查──什么值触发升级?
5. Ao longo de seis meses, a taxa de escalada sobe de 8% para 22%. Diagnóstico de três causas e a correção para cada uma.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Model routing | "cost broker" | Dynamic choice of model per request |
| Model cascade | "cheap-first escalate" | Run cheap, fall through to frontier on low confidence |
| Pre-route | "classify first" | Classifier up front; no re-run |
| Ensemble route | "parallel pick" | Run multiple, reward-model picks best |
| Escalation rate | "uprouted %" | Fraction of cascade requests that escalated |
| RouteLLM | "LMSYS router" | OSS router library |
| Not Diamond | "commercial router" | SaaS model-routing product |
| Drift | "cheap creep" | Distribution shift without router noticing |
| Online quality gate | "live check" | Automated LLM-judge sampling live traffic |

## Mais leitura 延伸阅读

- [AbhyashSuchi — Model Routing LLM 2026 Best Practices](https://abhyashsuchi.in/model-routing-llm-2026-best-practices/)
- [Lukas Brunner — Rise of Inference Optimization 2026](https://dev.to/lukas_brunner/the-rise-of-inference-optimization-the-real-llm-infra-trend-shaping-2026-4e4o)
- [RouteLLM paper / code](https://github.com/lm-sys/RouteLLM)
- [Not Diamond — model routing](https://www.notdiamond.ai/)
- [OpenRouter](https://openrouter.ai/) Porta de entrada multi-modelo com primitivos de roteamento.
