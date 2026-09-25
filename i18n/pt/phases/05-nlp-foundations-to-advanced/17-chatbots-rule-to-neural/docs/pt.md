# Chatbots  Regras baseadas em Neural para LLM Agentes   Chat chat 机器人  规则到神经网络到 LLM Agente

> Ela respondeu com padrões de correspondência. DialogFlow mapeou intenções. GPT respondeu a partir de pesos. Claude corre ferramentas e verifica. Cada era resolveu o pior fracasso do anterior.
> ELIZA Use Mode Matchback──DialogFlow 映射意图──GPT 从权重中回答──Claude 运行工具并验证──每时代解决了上一时代最严重失败──

> **【中文解读】**De ELIZA a Seq2Seq a Agente GPT.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 13 (Question Answering), Phase 5 · 14 (Information Retrieval) | **前置知识:** Phase 5 · 13（问答系统），Phase 5 · 14（信息检索与搜索）
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

Um usuário diz "Quero mudar meu voo". O sistema tem que descobrir o que eles querem, que informações faltam, como obtê-las e como concluir a ação.

> O usuário diz "Eu quero mudar o meu voo"". O sistema deve descobrir o que eles querem, o que falta de informação, como obter, como concluir a operação.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

A conversação é difícil para um sistema ML. A entrada é aberta. A saída tem que ser coerente em muitas viradas. O sistema pode precisar agir no mundo (mudar um voo, carregar um cartão). Cada passo errado é visível para o usuário.

> Para o sistema de controle de dados, a entrada é aberta. A saída deve ser mantida em várias rotas. O sistema pode precisar de uma ação contra o mundo.

As arquiteturas de chatbot têm ciclizado através de quatro paradigmas, cada um introduzido porque o anterior falhou de forma visível. Esta lição os acompanha em ordem.

> A estrutura de máquinas passou por quatro tipos, cada um por causa do fracasso do anterior muito evidente e introduzido.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

![Chatbot evolution: rule-based → retrieval → neural → agent](../assets/chatbot.svg)

### O meio século escrito, 1950-2001

O primeiro paradigma não durou cinco anos. Durou cinquenta. Saber seu arco importa porque cada sistema nele é a mesma máquina  entrada de correspondência, emitir uma resposta emlatada, atualizar um pequeno estado  e cinquenta anos de adição de regras a essa máquina nunca produziram o caso geral. Esse teto é por que paradigmas de dois a quatro existem.

**1950.**Turing evita "as máquinas podem pensar?" propondo uma substituição operacional: se um interrogador não pode distinguir a máquina de uma pessoa através de um teletipo, a questão filosófica é discutida. A conversa se torna o ponto de referência do campo antes que o campo tenha um nome.

**1956.**O nome chega a um workshop de verão em Dartmouth, onde se faz uma "inteligência artificial" na conjectura de que cada característica da inteligência "pode ser descrita com tanta precisão que uma máquina possa ser feita para simula-la".

**1966.**ELIZA envia o truque de reflexão que você constrói no Passo 1: regras de decomposição puxar fragmentos da entrada, regras de reensamblagem ecoá-los como perguntas. Cerca de 200 padrões total, estado zero, zero compreensão  e os usuários confiaram nele de qualquer maneira. Weizenbaum passou o resto de sua carreira alarmado com quão pouca maquinaria que levou.

**1972.**PARRY, construído em Stanford para modelar a paranóia, acrescenta a peça que a ELIZA não tinha: o estado interno. As variáveis numéricas para medo, raiva e desconfiança atualizam-se em cada virada e porta que o script dispara a seguir, por isso, entradas idênticas produzem respostas diferentes dependendo da conversa até agora. Num teste de transcrição cego, os psiquiatras distinguiram o PARRY dos pacientes humanos por acaso. É o antepassado direto do condicionamento de personalidade, um sistema de prompt implementado como três flutuantes. No mesmo ano, os dois bots foram apontados um para o outro através da ARPANET: um script de terapeuta entrevistando uma máquina de estado de paranoia, a primeira conversa bot-to-bot em uma rede.

**1995.**A Alice escalou a receita ELIZA com AIML, um dialeto XML para pares de padrões-template. Cerca de 40.000 categorias escritas à mão, três vencedores do Prêmio Loebner.

**2001.**O SmarterChild coloca a receita na frente de 30 milhões de usuários de mensagens instantâneas e adiciona buscas de fundo  tempo, ações, horários de filmes  entrelaçadas em modelos.

O paradigma acabou não porque alguém o refutou mas porque o custo de manutenção das máquinas de estado escritas à mão cresce linearmente com a cobertura enquanto as expectativas dos usuários crescem com o que viram na semana passada.

```figure
chatbot-lineage
```

**Rule-based (ELIZA, AIML, DialogFlow).**Os padrões de escrita manual correspondem às entradas do usuário e produzem respostas. Os classificadores de intenções encaminham-se para fluxos predefinidos. As máquinas de preenchimento de slot coletam informações necessárias. Funciona brilhantemente dentro do escopo estreito para o qual foi projetado. Falha imediatamente fora dele. Ainda navega em domínios críticos à segurança (autenticação bancária, reserva de companhias aéreas) onde a alucinação não é tolerada.

> **基于规则（ELIZA、AIML、DialogFlow）。**Manual de escrita Modelo de correspondência de usuário entrada e produção de resposta.

**Retrieval-based.**Um sistema de estilo FAQ. Encode cada par de (expresso, resposta). No tempo de execução, codifique a mensagem do usuário e recupere a resposta armazenada mais próxima. Pense no clássico recurso de "artigois semelhantes" da Zendesk.

> **基于检索。**FAQ 式系统──编码对对(话语、响应) ――运行时编码用户消息并检索近期存储响应──类似于Zendesk 经典"相似文章"功能──比规则更好处理释义──无生成,所以无幻觉──

**Neural (seq2seq).**Encoder-decoder treinado em registros de conversação. Gera respostas a partir do zero. Fluente, mas propenso a saídas genéricas ("não sei") e derivação factual. Nunca confiável sobre o tópico. A razão é que Google, Facebook e Microsoft tiveram chatbots decepcionantes em 2016-2019.

> **神经（seq2seq）。**O seu trabalho foi desenvolvido em uma área de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa de pesquisa em pesquisa em pesquisa de pesquisa em pesquisa de pesquisa de pesquisa em pesquisa em pesquisa em pesquisa

**LLM agents.**Um modelo de linguagem envolto em um loop que planeja, chama ferramentas e verifica resultados. Não é um chatbot com um prompt longo. Um loop de agente: planejar → chamar ferramenta → observar resultado → decidir o próximo passo. Retrieval-first grounding (RAG) impede que ele alucine. chamadas de ferramenta deixam que ele realmente faça as coisas. Esta é a arquitetura de 2026.

> **LLM Agent。**包装在循环中的语言模型,规划,调用工具并验证结果──不是带长提示的聊天机器人──一个代理 循环:规划 → 调用工具 → 观察结果 → decidir o próximo passo──检索优先定(RAG) prevenir iluminação──调用工具让它实际做事──这就是2026年架构──

Os quatro paradigmas não são substituições sequenciais. Um chatbot de produção 2026 percorre os quatro: baseado em regras para autenticação e ações destrutivas, recuperação para FAQ, geração neural para fraseamento natural, agente LLM para consultas abertas ambíguas.

> Este tipo de padrão não é substituído por ordem. Em 2026, os aparelhos de produção de chat são utilizados em quatro vias: baseados em regras para a verificação e operação destrutiva, pesquisa para a FAQ, gerenciamento de neurônios para a linguagem natural, LLM Agent para a consulta aberta de blurb.

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

### Passo 1: correspondência de padrões baseada em regras

```python
import re


class RulePattern:
    def __init__(self, pattern, response_template):
        self.regex = re.compile(pattern, re.IGNORECASE)
        self.template = response_template


PATTERNS = [
    RulePattern(r"my name is (\w+)", "Nice to meet you, {0}."),
    RulePattern(r"i (need|want) (.+)", "Why do you {0} {1}?"),
    RulePattern(r"i feel (.+)", "Why do you feel {0}?"),
    RulePattern(r"(.*)", "Tell me more about that."),
]


def rule_based_respond(user_input):
    for pattern in PATTERNS:
        m = pattern.regex.match(user_input.strip())
        if m:
            return pattern.template.format(*m.groups())
    return "I don't understand."
```

ELIZA em 20 linhas. O truque de reflexão ("Eu me sinto triste" → "Por que você se sente triste") é a demonstração canônica do psicoterapeuta de Weizenbaum de 1966.

> 20 行 ELIZA──反射技巧("Eu me sinto triste" → "Por que você se sente triste") é a apresentação clássica de Weizenbaum em 1966 do terapeuta psicológico.

### Passo 2: baseado em recuperação (FAQ)

Este trecho ilustrativo requer`pip install sentence-transformers`O corretor.`code/main.py`para esta lição usa uma semelhança de Jaccard stdlib em vez disso, então a lição funciona sem dependências externas.

> Este exemplo de código precisa de um .`pip install sentence-transformers`(会拉取火) │ 本课的可运行 `code/main.py`Utilize Jaccard de Standards Library para substituir a similaridade, assim o curso não precisa de dependência externa.

```python
from sentence_transformers import SentenceTransformer
import numpy as np


FAQ = [
    ("how do i reset my password", "Go to Settings > Security > Reset Password."),
    ("how do i cancel my order", "Go to Orders, find the order, click Cancel."),
    ("what is your return policy", "30-day returns on unused items, original packaging."),
]


encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
faq_questions = [q for q, _ in FAQ]
faq_embeddings = encoder.encode(faq_questions, normalize_embeddings=True)


def faq_respond(user_input, threshold=0.5):
    q_emb = encoder.encode([user_input], normalize_embeddings=True)[0]
    sims = faq_embeddings @ q_emb
    best = int(np.argmax(sims))
    if sims[best] < threshold:
        return None
    return FAQ[best][1]
```

A recusa baseada em limiares é a escolha chave de design.`None`E deixem o sistema escalar.

> Baseado em value rejeição é a escolha de design chave. Se o melhor correspondência não for suficientemente próximo, retorne.`None`让系统升级处理──

### Passo 3: geração neural (linha de base)

Use um pequeno codificador-decodificador com sintonia de instruções (FLAN-T5) ou um modelo de conversação com sintonia fina. Produção-inutile por si só em 2026 (contradição, deriva fora do tópico, absurdo factual), mas embarca dentro de sistemas híbridos para fraseamento natural. Os modelos de decodificação apenas no estilo DialoGPT precisam de separadores de viradas explícitos e de manuseio de EOS para produzir respostas coerentes; um modelo de texto FLAN-T5 funciona fora da caixa para um exemplo de ensino.

> Utilize pequeno instrução micro调编码器-解码器(FLAN-T5) ou micro调的对话模型──2026年单独使用不适合生产;;矛盾、跑题、事实错误), mas em sistemas mistos é usado em palavras-chave naturais──DiálogoGPT 风格的仅解码器模型需要显式轮次分隔符和EOS 处理才能产生连贯回复;FLAN-T5 text2text 流水线开箱即即即适合教学示例──

```python
from transformers import pipeline

chatbot = pipeline("text2text-generation", model="google/flan-t5-small")

response = chatbot("Respond politely to: Hi there!", max_new_tokens=40)
print(response[0]["generated_text"])
```

### Passo 4: Loop de agente LLM

Forma de produção de 2026:

> Formação de produção de 2026:

```python
def agent_loop(user_message, tools, llm, max_steps=5):
    history = [{"role": "user", "content": user_message}]
    for _ in range(max_steps):
        response = llm(history, tools=tools)
        tool_call = response.get("tool_call")
        if tool_call:
            tool_name = tool_call.get("name")
            args = tool_call.get("arguments")
            if not isinstance(tool_name, str) or tool_name not in tools:
                history.append({"role": "assistant", "tool_call": tool_call})
                history.append({"role": "tool", "name": str(tool_name), "content": f"error: unknown tool {tool_name!r}"})
                continue
            if not isinstance(args, dict):
                history.append({"role": "assistant", "tool_call": tool_call})
                history.append({"role": "tool", "name": tool_name, "content": f"error: arguments must be a dict, got {type(args).__name__}"})
                continue
            fn = tools[tool_name]
            result = fn(**args)
            history.append({"role": "assistant", "tool_call": tool_call})
            history.append({"role": "tool", "name": tool_name, "content": result})
        else:
            return response["content"]
    return "I could not complete the task in the step budget."
```

As ferramentas são funções chamáveis que o LLM pode invocar. O ciclo termina quando o LLM retorna uma resposta final em vez de uma chamada de ferramenta. O orçamento de passo evita loops infinitos em tarefas ambíguas.

> Três pontos essenciais: O instrumento é uma função de Mestrado em Ciências Humanas que pode ser utilizada.

A produção real adiciona: a primeira colocação em terra de recuperação (injectar documentos relevantes antes de cada chamada de LLM), barris (recusar ações destrutivas sem confirmação), observabilidade (logar cada passo) e avaliações (controlas automatizadas de que o comportamento do agente permanece em conformidade com as especificações).

> 实际生产还需要:检索优先定(每次 LLM 调用前注入相关文档) 护(未经确认拒绝破坏性操作) 可观测性(记录每步) 和评估(自动检查代理 行为保持规范) 

### Passo 5: encaminhamento híbrido

```python
def hybrid_chat(user_input):
    if is_destructive_action(user_input):
        return structured_flow(user_input)

    faq_answer = faq_respond(user_input, threshold=0.6)
    if faq_answer:
        return faq_answer

    return agent_loop(user_input, tools, llm)


def is_destructive_action(text):
    danger_words = ["delete", "cancel", "charge", "refund", "transfer"]
    return any(w in text.lower() for w in danger_words)
```

O padrão: regras deterministas para qualquer coisa destrutiva, recuperação para FAQs em lata, agentes LLM para tudo o mais.

> Modelo: para qualquer operação destrutiva, para qualquer tipo de consulta, para qualquer tipo de consulta, para qualquer tipo de consulta, para qualquer outra coisa, para qualquer tipo de operação prejudicial.

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

A pilha de 2026:

> Tecnologia de 2026:

| Use case / 使用场景 | Architecture / 架构 |
|---------|---------------|
| Booking, payment, authentication / 预订、支付、认证 | Rule-based state machines + slot filling / 基于规则的状态机 + 槽位填充 |
| Customer support FAQs / 客户支持 FAQ | Retrieval over curated answers / 对精选答案的检索 |
| Open-ended help chat / 开放式帮助聊天 | LLM agent with RAG + tool calls / 带 RAG + 工具调用的 LLM Agent |
| Internal tools / IDE assistants / 内部工具 / IDE 助手 | LLM agent with tool calls (search, read, write) / 带工具调用的 LLM Agent（搜索、读写） |
| Companion / character chatbots / 伴侣/角色聊天机器人 | Tuned LLM with persona system prompt, retrieval on knowledge / 微调 LLM 配角色系统提示和知识检索 |

Sempre use roteamento híbrido na produção. Nenhuma arquitetura única lida bem com cada solicitação. A camada de roteamento em si é tipicamente um pequeno classificador de intenções.

> Na produção, o uso de rotas mistas é sempre feito. Não há uma única estrutura capaz de lidar com cada tipo de pedido.

## Os modos de falha que ainda estão a ser enviados vão entrar no modelo de falha da produção.

- **Confident fabrication.**A redução: verificar os resultados, registar as chamadas de ferramentas, nunca deixar o LLM afirmar ter feito algo sem uma devolução bem-sucedida da ferramenta.
  **自信捏造。**O agente da LLM afirma ter concluído uma operação não concluída.
- **Prompt injection.**O usuário inserir texto que excede o sistema de solicitação. LLM01 classificado no OWASP Top 10 para LLM Aplicações 2025. Dois sabores: injeção direta (pesteado no chat) e injeção indireta (oculto em documentos, e-mails ou ferramentas de saída que o agente lê).
  **提示注入。**Utilizador inserir um sistema de orientação em texto. Em OWASP LLM  aplicação 2025 Top 10 中排 LLM01──两种形式:直接注入(粘贴到聊天中) 和间接注入(隐藏在文档、邮件或代理 读取的工具输出中)

  As taxas de ataque variam de acordo com o cenário. As taxas de sucesso medidas variam entre 0,5-8,5% em modelos de fronteira em referência geral de utilização de ferramentas e codificação. As configurações específicas de alto risco (ataques adaptativos contra agentes de codificação de IA, orquestração vulnerável) atingiram ~84%. Os CVEs de produção incluem EchoLeak (CVE-2025-32711, CVSS 9.3)  uma falha de exfiltração de dados com clicar zero no Microsoft 365 Copilot desencadeada por um e-mail controlado pelo atacante.
  ATAK SUCCESS RATE DE SCENASON De acordo com o cenário. Em uso de ferramentas gerais e código base, a medida do modelo de frente tem uma taxa de sucesso de cerca de 0,5-8,5%  Configuração de risco específico  Ataques de adaptação de um agente de código artificial  FRAGE CED) alcançou cerca de 84%  Produção de CVE incluindo EchoLeak  CVE-2025-32711, CVSS 9.3)  Zero-Click data breach vulnerability em Microsoft 365 Copilot, controlado pelo atacante 

  Mitigações: tratar a entrada do usuário como não confiável ao longo do loop; desinfeccionar antes das chamadas de ferramenta; isolar as saídas da ferramenta do prompt principal; usar o padrão Plan-Verificar-Executar (PVE) onde o agente planeja primeiro, depois verifica cada ação contra esse plano antes de executar (isso impede resultados da ferramenta de injetar novas ações não planejadas); exigir confirmação do usuário para ações destrutivas; aplicar menos privilégios aos escopo de ferramenta.
  缓解措施: durante todo o ciclo, o usuário será visto como incrível; o instrumento será usado para usar o usuário; o instrumento será separado do principal; o usuário será usado para executar o método de planejamento-verificação-execução (PVE); o agente será usado para planejar e executar o resultado de cada operação; o usuário será autorizado a executar o resultado de cada operação; o usuário será autorizado a executar o seu pedido de destruição; o usuário será autorizado a executar o seu pedido de execução.

  Não há uma quantidade de engenharia rápida que elimine completamente esse risco.
  Não importa o número de propostas, não é possível eliminar completamente esse risco.
- **Scope creep.**O agente sai da tarefa porque uma chamada de ferramenta retornou informações tangencialmente relacionadas. Mitigation: contratos de ferramentas estreitos; manter o sistema imediatamente focado; adicionar avaliações para taxa de fora da tarefa.
  **范围蔓延。**O agente porque ferramenta调用回复间接相关信息而跑题──缓解:缩小工具契约;保持系统提示聚焦;添加跑题率评估──
- **Infinite loops.**A redução do orçamento, a dedução da chamada, o juiz de LLM sobre "estamos a fazer progressos".
  **无限循环。**O agente continua a utilizar o mesmo instrumento.
- **Context window exhaustion.**As conversas longas empurram as primeiras voltas para fora do contexto.
  **上下文窗口耗尽。**长对话将最早轮次推出上下文──缓解: resumo de antigos轮次、 de acordo com a semelhança de pesquisa relativa às rotas históricas、 ou usar长上下文模型──

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

## Envia-o . Produto .

Salva como`outputs/skill-chatbot-architect.md`- Não .

> 保存为 `outputs/skill-chatbot-architect.md`- Não .

```markdown
---
name: chatbot-architect
description: Design a chatbot stack for a given use case.
version: 1.0.0
phase: 5
lesson: 17
tags: [nlp, agents, chatbot]
---

Given a product context (user need, compliance constraints, available tools, data volume), output:

1. Architecture. Rule-based, retrieval, neural, LLM agent, or hybrid (specify which paths go where).
2. LLM choice if applicable. Name the model family (Claude, GPT-4, Llama-3.1, Mixtral). Match to tool-use quality and cost.
3. Grounding strategy. RAG sources, retrieval method (see lesson 14), tool contracts.
4. Evaluation plan. Task success rate, tool-call correctness, off-task rate, hallucination rate on held-out dialogs.

Refuse to recommend a pure-LLM agent for any destructive action (payments, account deletion, data modification) without a structured confirmation flow. Refuse to skip the prompt-injection audit if the agent has write access to anything.
```

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 

## Exercícios.

1. **Easy.**Implementar a resposta baseada em regras acima com 10 padrões para um bot de encomenda de cafeteria.
   **简单。**Para café-florista, um único mecanismo de implementação da resposta baseada nas regras acima, 10 modus.
2. **Medium.**Construir uma FAQ híbrida + fallback LLM. 50 entradas de FAQ em lata para um produto SaaS, fallback LLM com recuperação no site do doc. Medir a taxa de recusa e precisão em 100 perguntas reais de suporte.
   **中等。**Construir FAQ misturada + LLM 回退──50 个 SaaS 产品的固定 FAQ 条目,LLM 回退带文档站检索──在100 个真实支持问题上测量拒绝率和准确率──
3. **Hard.**Implemente o ciclo de agente acima com três ferramentas (busca, leitura de dados do usuário, envio de e-mail). Execute uma avaliação com 50 cenários de teste, incluindo tentativas de injeção imediata.
   **困难。**Utilize três ferramentas (receitar, ler, obter dados do usuário, enviar e enviar e-mail) para realizar o ciclo de agência acima.

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Termos-chave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Intent（意图） | What the user wants / 用户想要什么 | Categorical label (book_flight, reset_password). Routed to a handler. / 分类标签（book_flight、reset_password）。路由到处理器。 |
| Slot（槽位） | A piece of info / 一条信息 | Parameter the bot needs (date, destination). Slot filling is the sequence of asks. / 机器人需要的参数（日期、目的地）。槽位填充是依次询问的过程。 |
| RAG（检索增强生成） | Retrieval plus generation / 检索加生成 | Retrieve relevant docs, then ground the LLM's response. / 检索相关文档，然后锚定 LLM 的响应。 |
| Tool call（工具调用） | Function invocation / 函数调用 | LLM emits a structured call with name + args. Runtime executes, returns result. / LLM 发出带名称和参数的结构化调用。运行时执行并返回结果。 |
| Agent loop（Agent 循环） | Plan, act, verify / 规划、执行、验证 | Controller that runs LLM calls interleaved with tool calls until task complete. / 运行 LLM 调用与工具调用交错直到任务完成的控制器。 |
| Prompt injection（提示注入） | User attacks prompt / 用户攻击提示 | Malicious input that tries to override the system prompt. / 试图覆盖系统提示的恶意输入。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.

## Mais leitura 延伸阅读

- [Weizenbaum (1966). ELIZA — A Computer Program For the Study of Natural Language Communication](https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf) o original papel de chatbot baseado em regras. / 原始基于规则的聊天机器人论文──
- [Thoppilan et al. (2022). LaMDA: Language Models for Dialog Applications](https://arxiv.org/abs/2201.08239) O artigo do Google sobre o chatbot neural, pouco antes de os agentes do LLM assumirem o cargo.
- [Yao et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) o papel que nomeou o padrão de ciclo do agente. / 命名 Agent 循环模式的论文──
- [Anthropic's guide on building effective agents](https://www.anthropic.com/research/building-effective-agents) 2024 orientação de produção que ainda é válida em 2026. / 2024 年生产指南,2026 年仍然有效。
- [Greshake et al. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) o papel de injecção rápida. / 提示注入论文──
- [OWASP Top 10 for LLM Applications 2025 — LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) o ranking que fez a injecção rápida a principal preocupação de segurança. / 使提示注入成为首要安全关注的排名──
- [AWS — Securing Amazon Bedrock Agents against Indirect Prompt Injections](https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agents-a-guide-to-safeguarding-against-indirect-prompt-injections/) Defensas práticas de camada de orquestração, incluindo fluxos de planejamento-verificação-execução e confirmação de usuários.
- [EchoLeak (CVE-2025-32711)](https://www.vectra.ai/topics/prompt-injection) o CVE canônico de exfiltração de dados com cero clique a partir de injeção de prompt indireta. caso de referência para o porquê de agentes de acesso de escrita precisarem de defesas de tempo de execução. / 间接提示注入的典型零点击数据泄露 CVE──写入权限 Agent 需要运行时防御的参考案例──
| Intent | What the user wants | Categorical label (book_flight, reset_password). Routed to a handler. |
| Slot | A piece of info | Parameter the bot needs (date, destination). Slot filling is the sequence of asks. |
| RAG | Retrieval plus generation | Retrieve relevant docs, then ground the LLM's response. |
| Tool call | Function invocation | LLM emits a structured call with name + args. Runtime executes, returns result. |
| Agent loop | Plan, act, verify | Controller that runs LLM calls interleaved with tool calls until task complete. |
| Prompt injection | User attacks prompt | Malicious input that tries to override the system prompt. |

## Mais leitura

- [Turing (1950). Computing Machinery and Intelligence](https://academic.oup.com/mind/article/LIX/236/433/986238) o artigo que fez da conversa o ponto de referência do campo.
- [Weizenbaum (1966). ELIZA — A Computer Program For the Study of Natural Language Communication](https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf) o papel original baseado em regras.
- [Colby, Weber, Hilf (1971). Artificial Paranoia](https://doi.org/10.1016/0004-3702(71)90002-6)  Arquitetura variável de afeto de PARRY, o primeiro chatbot com estado.
- [Thoppilan et al. (2022). LaMDA: Language Models for Dialog Applications](https://arxiv.org/abs/2201.08239)O artigo do Google sobre chatbot neural, pouco antes de os agentes do LLM assumirem o cargo.
- [Yao et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)O papel que nomeou o padrão do ciclo do agente.
- [Anthropic's guide on building effective agents](https://www.anthropic.com/research/building-effective-agents) Orientação de produção de 2024 que ainda se mantém em 2026.
- [Greshake et al. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) o papel de injecção rápida.
- [OWASP Top 10 for LLM Applications 2025 — LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) o ranking que fez da injecção rápida a principal preocupação de segurança.
- [AWS — Securing Amazon Bedrock Agents against Indirect Prompt Injections](https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agents-a-guide-to-safeguarding-against-indirect-prompt-injections/) Defesas práticas de camada de orquestração, incluindo fluxos de planeamento-verificação-execução e de confirmação do utilizador.
- [EchoLeak (CVE-2025-32711)](https://www.vectra.ai/topics/prompt-injection) o CVE canônico de exfiltração de dados com clicar zero da injecção indirecta de prompt.
