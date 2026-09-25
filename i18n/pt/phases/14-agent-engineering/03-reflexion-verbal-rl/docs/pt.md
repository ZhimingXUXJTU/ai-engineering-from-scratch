# Refleção: Aprendizagem de reforço verbal

> A RL baseada em gradientes precisa de milhares de testes e um cluster de GPU para corrigir um modo de falha. Reflexion (Shinn et al., NeurIPS 2023) faz isso em linguagem natural: após cada teste falhado, o agente escreve uma reflexão, armazená-la em memória episódica e condiciona o próximo teste nessa memória. Este é o padrão por trás do cálculo do tempo de sono da Letta, das aprendizagens do Claude Code CLAUDE.md e da regra de aprendizagem pro-fluxo de trabalho.

> **【中文解读】**Baseada em gradientes de RL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

> **【拓展：Reflexion → Claude Code 的自我学习】**O mecanismo de Claude Code CLAUDE.md é, em essência, uma variação da Refleção.

> - Não .**【前置】**本节依赖:Phase 14·01(Agent Loop)你必须已经能够跑通一个 ReAct 循环,因为 Reflexion 的 Actor 内部就是一个 ReAct loop;以及Phase 14·02(ReWOO)理解"试验/轨迹"的概念──如果你分不清"一次试验"和"一个步骤",先回去补补 ReAct──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 02 (ReWOO) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 02 (ReWOO)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizagem

- Nome os três componentes da Refleção (Ator, Avalador, Auto-Reflector) e o papel da memória episódica.
  中文翻译:说出 Reflexion的三个组件 (Actor, Evaluator, Self-Reflector)以及情景记忆的作用.
- Implementar um loop de reflexão stdlib com avaliador binário, buffer de reflexão e novas tentativas de repetição.
  Tradução do inglês para tradução do inglês: Reflexion 循环, containing二元评估器、反思缓冲区和全新重试──
- Escolha entre fontes de feedback escalares, heurísticas e auto-avaliações para uma determinada tarefa.
  Tradução do inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para inglês para tradução do inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês
- Explique por que o reforço verbal detecta erros que a RL baseada em gradientes precisaria de milhares de testes para corrigir.
  Tradução do inglês para tradução do inglês: Explain why language solitude can capture RL based on gradient requires thousands of trials to correct errors.

## O problema é o problema da introdução

Um agente falha numa tarefa. Em RL padrão você executaria milhares de testes mais, calcular gradientes, atualizar pesos.

> Agente  falhou em uma missão  Em RL padrão, você precisa executar milhares de vezes mais de experimentos  calcular gradientes  atualizar o peso  caro  lento, e a maioria dos agentes de produção  não tem orçamento de treinamento para cada falha 

A reflexão (Shinn et al., arXiv:2303.11366) faz uma pergunta diferente: e se o agente pensasse apenas em por que falhou e tentasse novamente com esse pensamento em seu prompt?

> Reflexão ((Shinn 等人, arXiv:2303.11366) propõe uma questão diferente: se o Agente  apenas pensar em causas de fracasso, então, na próxima tentativa de sugestão, juntar-se a essa ideia?

O resultado: no ALFWorld, ele supera o ReAct e outras linhas de base não-finamente sintonizadas. No HotpotQA, ele melhora em relação ao ReAct. Na geração de código (HumanEval / MBPP) ele define o estado da arte na época. Tudo sem um único passo de gradiente.

> Resultado: no ALFWorld 上 it derrotou ReAct 和其他非微调基线── no HotpotQA 上 it surpassed ReAct── em código gerado ((HumanEval/MBPP) 上 it reached its best level── tudo isso sem necessidade de um passo de escala──

## O conceito central.

### Os três componentes

```
Actor         : generates a trajectory (ReAct-style loop)     # 执行器：生成行动轨迹
Evaluator     : scores the trajectory — binary, heuristic, or self-eval  # 评估器：评分
Self-Reflector: writes a natural-language reflection on the failure      # 自我反思器：写反思
```

Mais uma estrutura de dados:

```
Episodic memory: list of prior reflections, prepended to the next trial's prompt  # 情景记忆
```

Um teste é realizado pelo ator. O avaliador o marca. Se a pontuação for baixa, o auto-reflector produz uma reflexão ("Escolhi a ferramenta errada porque li mal a pergunta como perguntando sobre X quando estava perguntando sobre Y"). A reflexão entra na memória episódica.

> - Não .**【类比】**Refleção 像考试做错题后的"错题本"机制:你做错一道题(Actor 失败)→ 拿到对错信号(Evaluator 评分)→ 写下"我为什么错了"(Self-Reflector 写反思)→ 下次考前翻错题本(情景记忆前置到提示) ・・・ 下次重复同类题,错的概率就低了──关键是错题本(反思) 用自然语言写,不需要重训练模型权──

> Uma vez, um ator, um avaliador, um avaliador, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor, um autor ou um autor, um autor ou um autor, um autor ou um autor, um autor ou um autor, um autor ou um autor, um autor ou um autor, um autor ou um autor, um autor ou um autor, um autor ou um autor, um autor ou um autor ou um autor, ou um autor ou um autor ou um autor, ou um autor ou um autor ou um ou outro, ou um autor ou um ou outro, ou um autor ou um ou outro, ou um ou outro, ou um ou outro, ou um ou outro, ou um ou outro, ou um ou outro, ou um ou outro, ou um ou outro ou outro, ou um ou outro ou outro ou outro, ou um ou outro ou outro ou outro ou outro, ou um ou outro ou outro ou outro ou outro ou outro ou outro ou outro, ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou outro ou ou ou ou ou ou ou ou ou outro ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou ou

### Três tipos de avaliadores

1. **Scalar**- um sinal binário externo. ALFWorld é bem-sucedido ou falha. testes HumanEval passar ou falhar.
   Tradução:**标量** Exterior 2元信号──ALFWorld Sucesso ou fracasso──HumanEval 测试通过或不通过──最简单,信号最强──
2. **Heuristic** assinaturas de falha predefinidas. "Se o agente tiver produzido a mesma ação duas vezes seguidas, marque como bloqueado". "Se a trajetória exceder 50 passos, marque como ineficiente".
   Tradução:**启发式**预定义的失败签名──"Se o Agente 连续两次产生相同行动,标记为卡住──""Se o tráfego exceder 50 步,标记为低效──"
3. **Self-evaluated**O Mestrado em Direito e Direito do Trabalho (LLM) tem uma trajetória própria.
   Tradução:**自评估**LLM para seu próprio trajeto avaliação──在没有真价值时需要──信号较弱;与工具定验证第 5 课CRITIC)

O padrão 2026 é uma mistura: escalar quando disponível, auto-equivalente quando não, heurísticas como trilhas de segurança.

> ️ **【易错点】**Três tipos de avaliação são muito difíceis de fazer: em um trabalho de avaliação de forma rigorosa, como o de "não-padrão", o avaliador continua a gerar "sinal de fracasso".**后果**O que é que é que é?**一行修复**A primeira é a de "fail signal" (seja como é possível distinguir entre os bons e os maus), "区分不开就降级为自衡 + 代上限").

> A prática de 2026 é a utilização misturada: com padrão, com padrão, sem padrão, com padrão de segurança.

### Por que isso generaliza

A reflexão não é um novo algoritmo, mas sim um padrão com nome.

> A reflexão é, em vez de um novo algoritmo, não é como dizer um modelo de nomeamento.

- Computação de tempo de sono de Letta (Lessão 08): um agente separado reflete sobre conversas passadas e escreve para blocos de memória.
  Tradução do inglês para tradução do inglês: Letta's sleep-time computation (Letta's sleep-time computation)
- O Claude Code.`CLAUDE.md`/ padrão de "salvar memória": reflexões capturadas como aprendizagem, prependidas para futuras sessões.
  Tradução do português:`CLAUDE.md`/"preservar memória" mode:反思被捕获为学习经验,前置到未来会话──
- Pro-fluxo de trabalho `/learn-rule`comando: correções capturadas como regras explícitas.
  Tradução do português:`/learn-rule`命令:纠正被捕为显式规则──
- Os nós de reflexão do LangGraph: um nó que marca a saída e as rotas para refinar se necessário.
  Chinese:                                                                                                                                                                                                                                                              

Todos derivam da mesma percepção: a linguagem natural é um meio rico o suficiente para levar "o que aprendi do fracasso" entre corridas.

> Todas elas se originam da mesma percepção: a linguagem natural é um meio suficientemente rico para transmitir entre os processos "o que aprendi do fracasso".

> **【拓展：Reflexion → 生产环境的自我修复】** quase todos os meios de produção "auto-reparação" Agente utilizam Refleção 变体:Letta's sleep-time computation 异步反思、Claude Code's CLAUDE.md 存储学习经验、Langgraph's反思节点──核心洞察相同:自然语言足够承载"从失败中学到了什么"──

### Quando funciona e quando não funciona

A reflexão funciona quando:

> Reflecção em:

- Há um sinal de falha claro (falha de teste, erro de ferramenta, resposta errada).
  Chinese Language Translation: Cóxias de erro (testing failure, tool err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err err
- A classe de tarefas é reprodutiva (o mesmo tipo de pergunta pode ser repetida).
  O que é que é o problema?
- A reflexão tem espaço para melhorar a trajetória (orçamento de acção suficiente).
  O que é que é o melhor?

A reflexão não ajuda quando:

> Reflexão nas seguintes situações:

- O agente já tem sucesso na primeira tentativa.
  O agente 首次尝试即成功── é o primeiro a tentar o sucesso.
- A falha é externa (rede desligada, ferramenta quebrada)  a reflexão sobre "a rede estava desligada" não ajuda futuras operações.
  O que é que é o "desemprego" de um sistema de redes?
- O reflexo transforma-se em superstição, armazenando uma narrativa sobre uma corrida única.
  O que é que se passa com o "desemprego" de um homem?

2026 trampa: rotação da memória. Reflexões se acumulam; alguns são obsoletos ou errados; re-runs ficam mais lentos à medida que o buffer episódico cresce. Mitigation: compactação periódica (Lessão 06), TTL em reflexões, ou um agente de limpeza separado no tempo de sono (Letta).

> 🤔 **【困惑】**P: Refleção 真的能" é igual a "RL 吗?RL 改是模型权重,Reflection 改只快,机械完全不同── A: 不能等价──论文标题"Verbal RL"是修辞而非数学等价──Reflection 改只快,机械完全不同── A: 不能等价──论文标题"Verbal RL"是修辞而非数学等价──Refleção 优势是**样本效率极高**Com 3 a 5 vezes de reflexão, podemos reparar um modelo falhado, enquanto a RL precisa de milhares de vezes de renovação; o desvantagem é:**反思不会持久**Para o modelo de peso, cada nova sessão é pesada. Portanto, a reflexão é adequada para o "scenário de produção sem orçamento treinado", o "RL" é adequado para o "modo de formação offline dissolved".

> 2026                                                                                                                                                                                                                                                              

## Construí-lo e realizei-o.
```figure
react-trace
```

## Construí-lo

`code/main.py`O ator emite listas de candidatos; o avaliador verifica a soma; o autor-reflector escreve uma linha sobre o que correu mal. A reflexão entra na memória episódica para o próximo teste.

> `code/main.py`Em um brinquedo  em questão Refleção: gerar uma e para valor objetivo lista de 3 elementos.

Componentes:

> 组件:

- `Actor` uma política escrita que melhora quando vê reflexões.
  Tradução:`Actor` ver reflexo                                                                                                                                                                                                                                                             
- `Evaluator.binary()` Passar/falhar na quantia-alvo.
  Tradução:`Evaluator.binary()`                                                                                                                                                                                                                                                              
- `SelfReflector` gera um diagnóstico de falha de linha única.
  Tradução:`SelfReflector`生成一行失败诊断──
- `EpisodicMemory` uma lista limitada com semântica TTL.
  Tradução:`EpisodicMemory`带 TTL 语义的有界列表──

- É o que é ?

> 运行:

```
python3 code/main.py
```

O rastro mostra três ensaios. Ensaios 1 falha, um reflexo é armazenado, ensaios 2 vê o reflexo e melhora, mas ainda falha, ensaios 3 é bem sucedido. Compare com uma execução de linha de base (sem reflexo)  ele permanece preso na resposta de ensaios 1.

> 轨迹显示三次试验──试验1 失败,储反思,试验2 看到反思并改进但仍失败,试验3 成功──与基线运行(无反思)对比它停留在试验1的答案──

## Use-o com o framework implementado.

O LangGraph envia a reflexão como um padrão de nós.`/memory`O comando e o fluxo de trabalho pro `/learn-rule`Externalize o buffer episódico como um arquivo de marcação. O computador de tempo de sono de Letta executa o Auto-Reflector em tempo de inatividade para que o agente primário permaneça limitado à latência. O OpenAI Agents SDK não envia Reflexion diretamente; você o constrói com um Guardrail personalizado que rejeita trajetórias por pontuação e memória`Session`que sobrevive através de corridas.

> LangGraph vai refletir como um modelo de ponto de fornecimento.`/memory`命令和 pro-workflow `/learn-rule`O sistema de controle de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados`Session`Vamos construir-lhe.

## Envia-o . Produto .

`outputs/skill-reflexion-buffer.md`cria e mantém um buffer episódico com captura de reflexão, TTL e deduplicação. Dada uma classe de tarefas e uma falha, emite um reflexo que realmente ajuda o próximo teste (não um genérico "seja mais cuidadoso").

> `outputs/skill-reflexion-buffer.md` criar e manter um quadro de reflexão captura TTL 和去重的情景缓冲区

## Exercícios.

1. Passe de avaliador binário para avaliador escalar que retorna uma métrica de distância (quão longe do alvo).
   Tradução do inglês para tradução do inglês: will evaluator be changed from 2元切换 for return distance measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure measure
2. Adicione um TTL de 10 testes às reflexões.
   Tradução do inglês para tradução do inglês: Give reflection add 10 times experimental TTL.
3. Implementar avaliador heurístico: marque o ensaio como preso se a mesma ação se repetir. Como isso interage com o Auto-Reflector?
   Tradução do inglês para tradução do inglês: implement启发式评估器:重复相同行动时标记为卡住.
4. Exerce Reflexion com um Actor adversário que ignora os reflexos.
   O ator 运行 Reflexion──最少需要什么提示工程才能迫使 Actor notate反思?
5. Leia a secção 4 do artigo Reflexão sobre AlfWorld. Reproduzir a melhoria da taxa de sucesso de 130% conceptualmente: qual é a chave delta vs. vanilla ReAct?
   Tradução do original: Reflexion 论文 第4节关于AlfWorld的内容──概念上重现 130%成功率改进:相比原始ReAct的关键差别是什么?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Reflexion | "Self-correction" / "自我纠错" | Shinn et al. 2023 — Actor, Evaluator, Self-Reflector plus episodic memory / Shinn 等人 2023——Actor、Evaluator、Self-Reflector 加情景记忆 |
| Verbal reinforcement | "Learning without gradients" / "无梯度学习" | Natural-language reflection prepended to the next trial's prompt / 自然语言反思前置到下一次试验的提示 |
| Episodic memory | "Per-task reflections" / "按任务的反思" | Bounded buffer of prior reflections for one task class / 一个任务类别的先前反思有界缓冲区 |
| Scalar evaluator | "Binary success signal" / "二元成功信号" | Pass/fail or numeric score from ground truth / 来自真值的通过/失败或数值评分 |
| Heuristic evaluator | "Pattern-based detector" / "基于模式的检测器" | Predefined failure signatures (e.g. stuck-loop, too-many-steps) / 预定义的失败签名（如卡住循环、步数过多） |
| Self-evaluator | "LLM-as-judge on own trace" / "LLM 评价自身轨迹" | Lower-signal fallback when no ground truth — pair with tool-grounded verification / 无真值时的低信号后备——与工具锚定验证配合 |
| Memory rot | "Stale reflections" / "过时反思" | Episodic buffer fills with obsolete entries; fix with compaction/TTL / 情景缓冲区填满过时条目；用压缩/TTL 修复 |
| Sleep-time reflection | "Async self-reflection" / "异步自我反思" | Run Self-Reflector off the hot path so primary agent stays fast / 在非关键路径上运行 Self-Reflector 使主 Agent 保持快速 |

## Mais leitura 延伸阅读

- [Shinn et al., Reflexion: Language Agents with Verbal Reinforcement Learning (arXiv:2303.11366)](https://arxiv.org/abs/2303.11366) o papel canônico
  Tradução do Novo Mundo:Reflexão 经典论文语言 Agent 的语言强化学习──
- [Letta, Sleep-time Compute](https://www.letta.com/blog/sleep-time-compute) Reflexão de sincronia na produção
  Lettera  Sobre o ambiente de produção
- [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) Gestão do buffer episódico como parte do contexto
  Chinese:Anthropic  Sobre o Agente de IA 上下文工程的文章将情景缓冲区作为上下文的一部分管理──
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) padrão de nó de reflecção
  中文翻译:LangGraph 概览反思节点模式。
