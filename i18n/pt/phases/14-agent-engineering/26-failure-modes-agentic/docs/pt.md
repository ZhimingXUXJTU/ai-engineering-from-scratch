# Modos de falha: por que os agentes se quebram

> MASFT (Berkeley, 2025) cataloga 14 modos de falha multi-agente em 3 categorias. Taxonomy da Microsoft documenta como falhas existentes de IA se amplificam em configurações agenciais. Dados de campo da indústria convergem em cinco modos recorrentes: ações alucinadas, deslocamento de escopo, erros de cascata, perda de contexto, uso indevido de ferramentas.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 05 (Self-Refine and CRITIC), Phase 14 · 24 (Observability) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

> - Não .**【前置】**學本節前請先掌握:Fase 14·05(Auto-Refinação / CRITIC)  了解单 Agent 自我纠错的局限;Fase 14·24(Observabilidade)  本节假设你已经能使用OpenTelemetry 看完整的痕迹──本节教你**识别 trace 中的失败模式**, é a fase 14·29 ((Tempos de execução da produção)

> 🤔 **【困惑】**P: Por que o Agente  fracassou é mais difícil de encontrar do que o software tradicional  fracassou? A: Porque o Agente  fracassou é "software failure" 代码没崩、API 没返回错误, mas o Agente usa ferramentas erradas调用、错误参数、错误顺序"成功完成" 任务── Tradicional teste afirmações só podem ver API 返回码,看不到语义错误──

## Objetivos de aprendizagem

- Nomear as três categorias de falhas do MASFT e pelo menos quatro modos específicos em cada uma delas.
- Explique por que a falha agencial amplifica os modos de falha da IA existentes (bias, alucinações).
- Descreva os cinco modos recorrentes na indústria e as suas mitigações.
- Implementar um detector stdlib que marca agentes rastreados com rótulos de modo de falha.

## O problema é o problema da introdução

As equipes enviam agentes que trabalham em 90% das pistas. Os 10% de falhas não são ruído aleatório  eles caem em um pequeno número de categorias recorrentes. Uma vez que você pode nomeá-los, você pode monitorá-los e corrigir-los.

> O agente da equipe lançado trabalha normalmente em 90% do rastreamento. Os 10% dos falhos não são ruídos acidentais. Eles pertencem a algumas categorias repetidas. Uma vez que você consegue nomeá-los, você consegue monitorá-los e repará-los.


> **【中文解读】**O modelo de falha do agente 系统与普通软件不同: 1) 级联失败一个错误决策触发后续一系列错误; 2) 目标漂移Agenção em execução em longa cadeia desviada do objetivo original; 3) 过度自信Agenção em resultados errados constrói uma história de sucesso;.

> **{【拓展：2025-2026 年的 Agent 事故报告揭示了系统性失败模式。典型案例如下：(1) 编码 Ag...】}**O relatório de acidente de agente para 2025-2026 revela um modelo de falha sistêmica. Tipos de casos tais como: 1) o agente codificador modificou documentos irrelevantes que levaram ao colapso do sistema; 2) o agente de estudo em 15 passos começou a discutir problemas filosóficos; 3) o agente de cliente diz ao usuário o sucesso da operação, mas não foi executado na prática.

> - Não .**【类比】**5 grandes modelos de fracasso do agente como 5 tipos típicos de acidentes de carro:**幻觉动作**=看错导航开错路;(2) **范围蔓延**=Teria sido feito para a vizinha província;**级联错误**=小擦后慌乱撞墙;(4) **上下文丢失**= esqueci de onde saíste;**工具误用**=把油门当车.  每种失败有应对防御:导航验证,明确终点,紧急停车按,定期回顾,工具白名单, 

> ️ **【易错点】**Agente 失败排查的 3 个坑: ((1) **只看最终输出**Agente 自信说"完成",但中间步骤全错;务必看完整的痕迹,不仅看结尾() 的输出──(2) **不设失败预算**O mesmo erro连续重试 20 次烧光预算; us max_retries=3 + 失败计计器──(3) **没做意图验证**Agente decide" eliminar o arquivo X", mas X é /etc/passwd; 高危操作必须用户二次确认 + 路径白名单。

## O conceito central.

### MASFT (Berkeley, arXiv:2503.13657)

Taxonomia de falhas de sistemas de vários agentes. 14 modos de falha agrupados em 3 categorias.

> O modelo de sucesso do agente inclui: um erro de divulgação de vários tipos de manipulação (ou manipulação) 幻觉成功 (seja como o caso do agente) 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 (seja como o caso do agente)                                                                                                                                                                                                                                                                                                                                                 

A alegação central: as falhas são falhas fundamentais de design em sistemas multi-agentes, não limitações de LLM a serem corrigidas com melhores modelos base.

> 核心主张: fracassos é uma falha de design básica do sistema de vários agentes, não é possível através de um modelo de base melhor para corrigir o limite de LLM ◦

> O modelo de sucesso do agente inclui: um erro de divulgação de vários tipos de manipulação (ou manipulação) 幻觉成功 (seja como o caso do agente) 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 (seja como o caso do agente)                                                                                                                                                                                                                                                                                                                                                 

### Taxonomia da Microsoft do Modo de Falha em Sistemas de IA Agênticos

- Falhas existentes da IA (bias, alucinações, vazamento de dados) ampliam-se em configurações agentes.
- Novos fracassos surgem da autonomia: ação involuntária em escala, o uso indevido de ferramentas, a deriva da missão.
- O whitepaper é o registo de riscos dos produtos agentes.

### Caracterizando falhas na IA Agêntica (arXiv:2603.06847)

- Os fracasso surgem da orquestração, evolução do estado interno e interação ambiental.
- Não é só "mau código" ou "mau modelo de saída".

### Estudo de Alucinações de Agentes da LLM (arXiv:2509.18970)

Duas manifestações primárias:

1. **Instruction-following Deviation**O agente não segue o aviso do sistema.
2. **Long-range Contextual Misuse** O agente esquece ou aplica mal o contexto das curvas anteriores.

Erros de subintenção: omissão (passo perdido), redundancia (passo repetido), desordem (passo fora de ordem).

> O modelo de sucesso do agente inclui: um erro de divulgação de vários tipos de manipulação (ou manipulação) 幻觉成功 (seja como o caso do agente) 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 (seja como o caso do agente)                                                                                                                                                                                                                                                                                                                                                 

### Os cinco modos recorrentes do setor

As análises de campo de Arize, Galileo, NimbleBrain 2024-2026 convergem em:

> O modelo de sucesso do agente inclui: um erro de divulgação de vários tipos de manipulação (ou manipulação) 幻觉成功 (seja como o caso do agente) 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 (seja como o caso do agente)                                                                                                                                                                                                                                                                                                                                                 

1. **Hallucinated actions.**O agente invoca uma ferramenta que não existe ou fabrica argumentos.
2. **Scope creep.**O agente expande a tarefa além do pedido do usuário (cria relações públicas adicionais, envia e-mails adicionais).
3. **Cascading errors.**Uma chamada errada desencadeia efeitos a jusante. Uma alucinação fantasma SKU desencadeia quatro chamadas API  um incidente de vários sistemas.
4. **Context loss.**As tarefas de longo horizonte esquecem as restrições de turno precoce.
5. **Tool misuse.**Chama a ferramenta certa com argumentos errados, ou a ferramenta errada inteiramente.

Os agentes não conseguem distinguir "eu falhei" de "a tarefa é impossível" e muitas vezes alucinam uma mensagem de sucesso em 400 erros para fechar o ciclo.

> O agente não consegue distinguir entre "eu falhei" e "a missão não foi concluída", muitas vezes, em 400 erros, ele vê uma mensagem de sucesso e fecha o ciclo.

> O modelo de sucesso do agente inclui: um erro de divulgação de vários tipos de manipulação (ou manipulação) 幻觉成功 (seja como o caso do agente) 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 (seja como o caso do agente)                                                                                                                                                                                                                                                                                                                                                 

### Mitigation: portões em cada passo

Portais de verificação automáticas em cada etapa de uma cadeia de raciocínio, verificando a base de fatos em relação ao estado ambiental.

> O modelo de sucesso do agente inclui: um erro de divulgação de vários tipos de manipulação (ou manipulação) 幻觉成功 (seja como o caso do agente) 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 (seja como o caso do agente)                                                                                                                                                                                                                                                                                                                                                 

- Classificador de segurança por etapa (Lessão 21).
- Validação de argumentos de chamada de ferramenta (Lessão 06).
- Verificação cruzada do conteúdo recuperado com relação a fatos conhecidos (Lessão 05, CRÍTICA).
- Detectar alucinação de sucesso por re-probar estado (o arquivo foi realmente criado?).

### Onde o monitoramento de falhas vai mal

- **Tagging only crashes.**A maioria das falhas dos agentes produzem resultados válidos.
- **No baseline.**A detecção da deriva precisa de um último bom conhecido; sem ela não se pode dizer "este está a piorar".
- **Over-alerting.**Cada falha produz uma página, um cluster e um limite de taxa.

> **仅标记崩溃。**A maioria dos agentes não consegue produzir resultados eficazes.
> **没有基线。**O teste de mudança requer um estado de boa qualidade; sem ele, você não pode dizer "este está a ficar mau".
> **过度告警。**Cada falha produz uma página.

## Construí-lo e realizei-o.
```figure
failure-cascade
```

## Construí-lo

`code/main.py`Implementa um tagger de modo de falha stdlib:

> O modelo de sucesso do agente inclui: um erro de divulgação de vários tipos de manipulação (ou manipulação) 幻觉成功 (seja como o caso do agente) 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 (seja como o caso do agente)                                                                                                                                                                                                                                                                                                                                                 

- Um conjunto de dados sintéticos de rastreamento que abrange os cinco modos.
- Funções do detector por modo (patrões de assinatura em chamadas de ferramenta, saídas, ações repetidas).
- Um tagger que marca cada traço e relata a distribuição de modo.

- É o que é ?

```
python3 code/main.py
```

Resultado: rótulos por rastro + distribuição agregada, uma reprodução barata do que a superfície de aglomeração de rastro da Phoenix.

> 输出: cada etiqueta de rastreamento + 聚合分布,Fenix  rastreamento聚类所显示内容的廉价复现――

> O modelo de sucesso do agente inclui: um erro de divulgação de vários tipos de manipulação (ou manipulação) 幻觉成功 (seja como o caso do agente) 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 (seja como o caso do agente)                                                                                                                                                                                                                                                                                                                                                 

## Use-o com o framework implementado.

- **Phoenix**para o agrupamento de derivação da produção (Lessão 24).
- **Langfuse**para repetição de sessão + anotação.
- **Custom**para assinaturas específicas de domínio que a sua plataforma de observação não pode detectar.

## Envia-o . Produto .

`outputs/skill-failure-detector.md`gera detectores de modo de falha adaptados ao seu domínio, ligados a uma loja de rastreamento.

> `outputs/skill-failure-detector.md`Criado para o seu campo de teste de padrões de falha, conectado ao arquivo de rastreamento.

> O modelo de sucesso do agente inclui: um erro de divulgação de vários tipos de manipulação (ou manipulação) 幻觉成功 (seja como o caso do agente) 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环爆炸 (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 explosion (seja como o caso do agente), 循环 (seja como o caso do agente)                                                                                                                                                                                                                                                                                                                                                 

## Exercícios.

1. Adicione um detector para "alucinação de sucesso": o agente retorna sucesso, mas o estado-alvo permanece inalterado.
  Tradução do inglês para tradução do inglês:
2. Marque 100 traços reais de um produto que construiu. Qual modo domina?
  Tradução do inglês para tradução do inglês:
3. Implementar uma métrica de "rádio de cascata": dada uma falha no passo N, quantas etapas a jusante foram afectadas?
  Tradução do inglês para tradução do inglês:
4. Leia os 14 modos de falha do MASFT, escolha três que se aplicam ao seu produto, escreva detectores.
  Tradução do inglês para tradução do inglês:
5. Conectar um detector a um trabalho de CI: falhar na construção se >=5% das pistas marcar um modo.
  Tradução do inglês para tradução do inglês:

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| MASFT | "Multi-agent failure taxonomy" | Berkeley 14-mode categorization |  |
| Cascading error | "Ripple failure" | One early mistake propagates through N steps |  |
| Context loss | "Forgot the constraint" | Long-horizon turn drops early-turn facts |  |
| Tool misuse | "Wrong tool / wrong args" | Valid call, wrong invocation |  |
| Success hallucination | "Faked completion" | Agent claims success on a 400; state unchanged |  |
| Scope creep | "Overreach" | Agent does more than asked |  |
| Instruction-following deviation | "Disobedience" | Ignores system prompt or user constraint |  |
| Sub-intention errors | "Plan bugs" | Omission, redundancy, disorder in plan execution |  |

## Mais leitura 延伸阅读

- [Cemri et al., MASFT (arXiv:2503.13657)](https://arxiv.org/abs/2503.13657) 14 modos de falha, 3 categorias
  Tradução do português:
- [Microsoft, Taxonomy of Failure Mode in Agentic AI Systems](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)Registro de riscos
  Tradução do português:
- [Arize Phoenix](https://docs.arize.com/phoenix) Clustering de deriva na prática
  Tradução do português:
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) quando os padrões mais simples evitam completamente os modos
  Tradução do português:
