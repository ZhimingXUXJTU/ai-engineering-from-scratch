# Sociedade da Mente e Multidíbio de Agentes .

> A premissa de Minsky de 1986  inteligência é uma sociedade de especialistas  é redescoberta a cada década. Em 2023 Du et al. transformou-a em um algoritmo concreto: múltiplas instâncias de LLM propõem respostas, lêem as respostas umas das outras, criticam e atualizam.**multiple agents**E ...**multiple rounds**A sociedade supera o monólogo de um único agente; a troca de várias rondas supera a votação de um só disparo.

> **【中文解读】**Esta secção apresenta o debate sobre o espírito social  Aplicação da teoria do espírito social de Marvin Minsky em vários agentes  sistemas 

> **【拓展：society of mind debate→具体应用】**Marvin Minsky 心智社会 (心智社会, 1986) propôs que o intelecto é o produto de muitas simples mentes colaborativas. Esta ideia é que, em 2026, o sistema de debate de vários agentes pode ser implementado em vários agentes.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (Primitive Model)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**学本节前请先掌握:Fase 16·04(原语模型)、Fase 13·01-03(CoT 推理)。Minsky 心智社会理论 + LLM 辩论算法。
> - Não .**【类比】**Do Agente 辩论 = "学术同行评审"──单 Agent = 一个作者写论文(易自但片面); Do Agente 辩论 = 多位审稿人 + 作者多轮回应,最终共识更稳健──Du et al. 2023 证明:多 Agent + 多轮独立贡献提升不是简单加法,是协同效应──3-5 个 Agent 最优(多多多了反而成一团)──

## Problema Introdução

A autoconsistência  amostra um modelo muitas vezes e tome a resposta da maioria  é a melhor raciocínio mais barata que você pode aproveitar. Funciona, mas satura rapidamente. Você pode dobrar suas amostras e não ver outro salto significativo.

> A autoconformidade é a melhor hipótese mais barata que você pode adicionar a um modelo. É eficaz, mas rapidamente.

A saturação vem de erros correlacionados: o mesmo modelo tende a falhar da mesma forma.

> 和来自相关错误: identico modelo tende a fracassar da mesma maneira.

O debate quebra a saturação. Em vez de N amostras independentes de um modelo, N agentes ler o raciocínio e revisão uns dos outros. A correlação entre amostras cai (eles não são mais i.i.d.), e o ponto de convergência é muitas vezes correto onde a votação i.i.d. foi com certeza errado.

> O debate rompeu 和── não obtendo N 个独立样本从一个模型中, mas deixando N 个代理阅读彼此的推理并修改──相应性下降了.

A decorreção é o mecanismo. Quando os agentes vêem o raciocínio de outros agentes, não podem deixar de interagir com ele  quer para defender a sua posição ou para atualizar-a.

> Quando o Agente vê a opinião de outro Agente, eles têm que participar ou defender sua posição, ou atualizar-la. Essa participação forçada não pode gerar qualquer número de informações independentes e distribuídas.

## Conceptos básicos

### O algoritmo Du et al. 2023

A partir de arXiv:2305.14325 (ICML 2024):

> De arXiv:2305.14325 (ICML 2024):

O algoritmo é intencionalmente simples: sem papéis especiais, sem juiz, sem moderador. Todo agente é simétrico. A única assimetria é a ordem de quem fala primeiro, e até mesmo isso desaparece em várias rodadas.

> 算法有意简单: não há papel especial, não há árbitro, não há apresentador.

1. Cada um dos agentes N produz uma resposta inicial à pergunta.
   Tradução do inglês:N 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 
2. Para a rodada r = 2..R: cada agente é mostrado as respostas da rodada r-1 dos outros agentes e perguntado "considerando estes, dê sua resposta atualizada".
   Para o segundo r = 2..R 轮: cada agente 看到其他代理 第 r-1 轮的答案并被问"考虑这些,给出你的更新答案――"
3. Após as rodadas R, a maioria vota as respostas finais.
   Depois da R 轮, a maioria dos votos foi feita para a resposta final.

Os testes em papel sobre MMLU, GSM8K, biografias, MATH e referências de factualidade.

> 论文在 MMLU、GSM8K、传记、MATH 和事实性基准上测试──辩论持续优于CoT 和自我反思──

A suíte de referência abrange tanto o raciocínio (MATH, GSM8K  problemas com respostas corretas verificáveis) quanto a factualidade (biografias  afirmações verificáveis contra a Wikipedia).

> 基准套件涵盖推理(MATH、GSM8K有可验证正确答案问题) 和事实性(传记可对照维基百科 检查的声明) ⋅ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain ⇒ Factuality gain                                                                         

### Dois botões independentes

Ablações do mesmo documento:

> Como se fosse um estudo de análise de um estudo de análise de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um estudo de um

- **Agent count alone**O Parlamento Europeu e o Conselho aprovaram o relatório de resolução.
  Tradução:**仅 Agent 数量**(1 ronde, maioria dos votos) Na maioria das tarefas, é melhor do que um único agente, mas vai atingir a plataforma.
- **Round count alone**(1 agente que vê o seu próprio raciocínio prévio) dificilmente ajuda a fraqueza conhecida da reflexão.
  Tradução:**仅轮数**(1 Agente vê-se a sua própria opinião anterior) quase não ajuda.
- **Both together**O intercâmbio entre agentes múltiplos impulsiona o ganho.
  Tradução:**两者结合** produziu uma grande melhoria

### Por que funciona

Dois mecanismos:

>  dois mecanismos:

Os dois mecanismos são compostos: a exposição a discordâncias fornece novas informações; erros descorrelados impedem que as novas informações sejam mediadas para a resposta errada.

>  dois mecanismos complexos: exposição a diferenças fornecendo novas informações;  correlação de erros prevenindo novas informações serem mediadas a respostas erradas

1. **Exposure to disagreement.**Quando um agente vê a cadeia de raciocínio de outro agente com uma conclusão diferente, ele tem que justificar ou atualizar. De qualquer forma, o contexto para o rondo r + 1 é mais rico do que o rondo r.
   Tradução:**暴露于分歧。**Quando um Agente vê outro Agente com diferentes conclusões, ele deve provar ou atualizar. De qualquer forma, a primeira ronda de R+1 tem um volume superior a a segunda.
2. **Correlated error reduction.**Em auto-consistência, todas as amostras vêm do mesmo modelo, então os erros correlacionam  você média em uma resposta confidentemente errada. Diferentes modelos ou sementes diferentes descorrelam. Diferentes *visões debatidas* descorrelam ainda mais.
   Tradução:**相关错误减少。**Em auto-concordância, todas as amostras provêm do mesmo modelo, portanto, errores relacionados  Você obtém uma resposta errada de confiança em média  Diferente modelo ou diferentes sementes para se relacionar Diferente * opinião de debate * Mais relacionar

### O debate é heterogêneo

A A-HMAD e os acompanhamentos relacionados utilizam *modelos base diferentes* para diferentes agentes.

> A-HMAD 和相关后续工作为不同 Agent 使用*不同的基础模型*──Llama + Claude + GPT 辩论减少单一文化崩(Lesson 26),因为一个模型族的相关错误不被其他模型族共享────

O argumento de erro-decorrelação é o mesmo por trás dos métodos de conjunto no ML clássico: modelos diversos falham de forma diferente, então a votação é mais confiável.

> 错误去相关论点与经典ML中集成方法背后的相同:多样化模型以不同方式失败, therefore voting is more reliable──问题是多样性昂贵──三份API 账单而不是一份) 且收益在 3-4模型族后快速和──

Desvantagem: um modelo fraco participando de um debate pode arrastar o consenso para a sua resposta errada (ver "Devemos estar indo LOCO?", arXiv:2311.17371).

> 缺点: um modelo fraco de debate participativo pode dar o consenso para arrastar para sua resposta errada.

Um modelo fraco (por exemplo, um parâmetro Llama 7B) pode superar um modelo forte (GPT-4) se o modelo forte atualiza-se de forma muito agressiva em relação às respostas erradas confiantes do modelo fraco. Calibre quais modelos participam.

> 异构辩论不是免费多样性──弱模型(如 7B 参数 Llama) 可以否决强模型(GPT-4), se强模型过激进地向弱模型的自信错答案更新──校准哪些模型参与──

### NLSOM  a extensão 129-agente

Zhuge et al. ("Mindstorms in Natural Language-Based Societies of Mind", arXiv:2305.17066) escalaram essa ideia para 129-sociedades membros.

> Zhuge 等人("Baseado em linguagem natural, o pensamento da sociedade",arXiv:2305.17066) vai expandir essa ideia para 129 membros da sociedade.

O resultado da escalagem é impressionante: após ~ 50 agentes, os papéis individuais começam a se especializar sem ser informados. Alguns se tornam "pesquisadores", "outros" críticos, "outros" sintetizadores.

>  O resultado da expansão é notável: depois de mais de 50 agentes, os papéis individuais começaram a se especializar em condições de não ser informados. Alguns se transformaram em "investigadores", outros "criticadores" e outros "completeiros".

### Modos de falha

- **Sycophancy cascade.**Todos os agentes se afastam para o agente que parece mais confiante. O debate desmorona com a voz mais alta.
  Tradução:**谄媚级联。**Todos Agente se submetem a parecer o Agente mais confiante.
- **Topic drift.**Os debates em muitas rodadas se desviam da pergunta original.
  Tradução:**主题漂移。**Douradas de debate de origem.
- **Compute blowup.**N agentes x R rodadas = N*R LLM chamadas, cada uma com um contexto que cresce. Um debate de 5 agentes, 5 rodadas é de 25 chamadas em contexto crescente.
  Tradução:**计算爆炸。**N 个代理 x R 轮 = N*R 次 LLM 调用, per次的上下文都在增长──5 个代理、5 轮的辩论是25 次调用,上下文不断增长──每一个问题的成本可能超过单次CoT 调用的10倍──

## Construí-lo e realizei-o.
```figure
multi-agent-debate
```

## Construí-lo

`code/main.py`O programa é um debate de 3 agentes x 3 rodadas sobre uma pergunta matemática onde cada agente começa com uma resposta diferente (possivelmente errada).

> `code/main.py`Em um problema matemático, executar 3 Apresentante x 3 Radas de debate, cada Apresentante começa a responder a uma diferença (possivelmente erro).

A demonstração mostra dois efeitos-chave:

> A apresentação mostrou dois efeitos-chave:

- Uma única rodada de troca move os agentes mais perto da resposta correta.
  Tradução do inglês: 单轮交流将 Agent 移向正确答案.
- As rondas extras anteriores à segunda ronda mostram retornos decrescentes (combatentes com o plato de Du et al).
  O número de rotas adicionais de mais de 2o turno mostra um aumento nos lucros ([[Plataforma dos outros]]).

- Correr .

```
python3 code/main.py
```

## Use-o com o framework implementado.

`outputs/skill-debate-configurator.md`Configura um debate para uma nova tarefa: número de agentes, número de rodadas, heterogeneidade (modelo igual versus misturado), atribuição de funções (simétrica versus oponente).

> `outputs/skill-debate-configurator.md`Por outro lado, a sua função é de fazer uma análise de dados e de fazer uma análise de dados.

## Envia-o . Produto .

Se você enviar debate:

> Se depender de um sistema de debate:

- **Cap rounds at 3.**Du et al. mostram que 3 rodadas capturam a maior parte do ganho.
  Tradução:**将轮数限制在 3。**Du 等人 demonstrou que as três rotas capturaram a maior parte dos benefícios.
- **Cap agents at 5.**Além do 5, o conteúdo e o custo dominam.
  Tradução:**将 Agent 限制在 5。**                                                                                                                                                                                                                                                              
- **Heterogeneous by default.**Pelo menos dois modelos base diferentes na piscina.
  Tradução:**默认异构。**Há pelo menos dois modelos base diferentes na piscina.
- **Adversarial slot.**Um agente fez com que discordasse, não importa.
  Tradução:**对抗角色。**Um agente é exposto a qualquer maneira que seja.
- **Log every round.**Os sistemas de debate que escondem rodadas intermediárias não podem ser depurados ou auditados.
  Tradução:**记录每轮。**O sistema de debate oculto no meio da fase não pode ser controlado nem auditado.

## Exercícios.

1. Corra .`code/main.py`, então, definir a contagem de rodadas para 5 e observar retornos decrescentes. em que rodada a convergência adicional para?
   Tradução: 运行`code/main.py`O número de rotas será definido como 5 e observe a redução dos lucros.
2. A Comissão propõe que a Comissão adopte um novo regulamento que, em conformidade com o artigo 107.o, n.o 1, do Tratado, estabeleça um regime de harmonização das legislações nacionais.
   Chinese Translation: Adicionar o quarto agente que tem um papel de resistência:总是与当前多数不同意.
3. Plot (impressão) o resultado do acordo por rodada (fracção de agentes na resposta da maioria).
   Chinese Language Translation: Drawing (印制) Per round 合致性分数 ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  () )  ()  ()  () )  ()  () )  ()  ()  ()  ()  () )  ()  ()  ()   ()                                                                                                       
4. Leia as ablações da Seção 4. Replica o resultado "apenas agentes" vs. "apenas rondas" vs. "ambos" usando este código.
   Tradução do inglês para tradução do inglês: read Du 等人第 4 节消融实验──使用此代码复现"仅代理"vs"仅轮数"vs"两者结合"的结果──
5. Leia "Devemos estar indo LOCO?" (arXiv:2311.17371) e enumere duas variantes de debate além do round-robin  por exemplo, liderado por juízes, cadeia de debate, adversária.
   Chinese: 阅读" Should we go towards MAD ?" (ArXiv: 2311.17371)并列出两种轮询之外的辩论变体例如,裁判主导、辩论链、对抗式──

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Society of Mind / 心智社会 | "Minsky's idea" / "Minsky 的想法" | Intelligence as interacting specialists; 1986 framing now operationalized via LLM debate. / 智能作为交互的专家；1986 年的框架现在通过 LLM 辩论实现。 |
| Multi-agent debate / 多 Agent 辩论 | "Agents argue" / "Agent 争论" | N agents propose, critique each other, revise over R rounds, majority-vote. / N 个 Agent 提议、批评彼此、在 R 轮中修改、多数投票。 |
| Consensus / 共识 | "They agree" / "他们一致" | Not epistemic truth — just fraction-on-majority-answer. Can be confidently wrong. / 不是认识论真理——只是多数答案上的比例。可能自信地犯错。 |
| Rounds / 轮次 | "Exchange steps" / "交换步骤" | One round = each agent reads the others and updates once. / 一轮 = 每个 Agent 阅读其他 Agent 并更新一次。 |
| Heterogeneous debate / 异构辩论 | "Mix model families" / "混合模型族" | Using different base models to decorrelate errors. / 使用不同的基础模型来去相关错误。 |
| Sycophancy cascade / 谄媚级联 | "Everyone agrees with the loud one" / "每个人都同意最大声的" | Debate failure where agents defer to the most confident agent regardless of correctness. / 辩论失败，Agent 不顾正确性屈从于最自信的 Agent。 |
| NLSOM | "129-agent society" / "129 Agent 社会" | Natural-language society of mind; Zhuge et al.'s scaled version. / 自然语言心智社会；Zhuge 等人的扩展版本。 |
| Correlated error / 相关错误 | "Same model, same bug" / "相同模型，相同 bug" | Why self-consistency saturates; debate across different views decorrelates. / 自我一致性为什么饱和；不同观点的辩论去相关。 |

## Mais leitura 延伸阅读

- [Du et al. — Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325) o papel de referência, ICML 2024
  中文翻译:Du 等人  通过多 Agent 辩论改进语言模型的事实性和推理  参考论文, ICML 2024
- [Zhuge et al. — Mindstorms in Natural Language-Based Societies of Mind](https://arxiv.org/abs/2305.17066) 129-agente NLSOM
  中文翻译:Zhuge 等人  基于自然语言的心智社会中的思维风暴  129 Agente NLSOM
- [Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs](https://arxiv.org/abs/2311.17371) Referências de debate
  Tradução do inglês para tradução do inglês: Should we go towards MAD?
- [Debate project page](https://composable-models.github.io/llm_debate/) Código, demonstrações e detalhes de ablação de Du et al.
  Tradução do inglês para o inglês:                                                                                                                                                                                                                                                          
