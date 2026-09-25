# Desenhos de Auto-Imelhoria Limitados

> A pesquisa convergiu em quatro primitivas para limitar um ciclo de auto-melhoria. Invariantes formais que devem ser mantidas em todas as edições. Ancoras de alinhamento que não podem ser modificadas. Constrangimentos multi-objetivos em que todas as dimensões (segurança, equidade, robustez) devem ser respeitadas, não apenas o desempenho. Detecção de regressão que suspende o ciclo quando as métricas históricas sugerem perda de capacidade. Nenhum deles é uma prova de segurança  resultados teóricos da informação (complexidade de Kolmogorov, teorema de Lob) ligados ao que qualquer sistema pode provar sobre seus próprios sucessores. São mitigantes que aumentam o custo do fracasso silencioso.

> **【中文解读】**Os estudos têm recebido quatro restrições originais de um ciclo de auto-melhoria. Cada edição deve ser estabelecida em forma invariavel. Não pode ser modificada em pontos de integração. Cada dimensão (segurança, equidade, robustez) deve ser estabelecida em restrições múltiplas, e não apenas em desempenho. Quando os indicadores históricos mostram que a perda de capacidade interrompe o ciclo de regresso, os testes não são uma prova de segurança.

> **【拓展：四个原语 → 一个守门栈】**实际部署中四个原语组合成"守门" Cada vez que se auto-modifica para se colocar em prática deve ser seguidamente aprovado: 不变量检查(模块哈希、工具权限清单、宪法头)→ 对齐点检查(目标陈述匹配批准版本)→ 多目标评估(性能安全、公平、鲁棒)→ 回归检测(无轴下降超值)。任一失败暂停循环──这是ICLR 2026 RSI 工作坊、Anthropic RSP v3.0、DeepMind FSF v3 共同采纳的设计共识──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, bounded-loop with invariant check) | **语言:** Python（标准库，带不变量检查的有界循环）
**Prerequisites:** Phase 15 · 07 (RSI), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 07（RSI），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**O RSI é limitado a uma quantidade de dados que podem ser transferidos para outros dados.
> - Não .**【类比】**RSI limitada = "AI 自我改进的护"──四个原语 = 四道门:(1) 不变量检查(哈希签名,不能改变);(2) 对齐点(价值观不能改变);(3) 多目标评估(性能但安全不能掉);(4) 回归检测(任何轴下降就停)──每次自修必须四道门全过──但理论上:Lob 定理 + Kolmogorov 复杂性 = 系统永远无法完全证明自己的后继者这些只是缓解,不是保证──
> 🤔 **【困惑】**P: 既然 não pode garantir a segurança, por que ainda precisa de pesquisa?  Porque "aumentar o custo de fracasso" também tem valor.  O atacante deve gastar mais recursos para contornar os quatro caminhos 门.

## O problema é o problema da introdução

O simulador de corrida da lição 7 mostrou que pequenas diferenças de taxa se compõem em grandes lacunas.

> O modelo de corrida de classe 7 mostra uma pequena diferença de velocidade, composta por grandes diferenças.

Os dois resultados apontam para a mesma questão de engenharia: quais restrições podem ser colocadas num ciclo de auto-melhoria de modo que as restrições não possam ser silenciosamente enfraquecidas pelo próprio ciclo?

>  Dois resultados se dirigem a um mesmo problema de engenharia: Que restrições pode aplicar ao ciclo de auto-reforma, para que esses restrições não possam ser silenciosamente enfraquecidos pelo ciclo?

O resumo do ICLR 2026 RSI Workshop (openreview.net/pdf?id=OsPQ6zTQXV) identifica quatro desses primitivos. A RSP v3.0 (Lessão 19) da Anthropic e a FSF v3 (Lessão 20) da DeepMind ambos os referem em limites de capacidade. Os Meta HyperAgents trabalham e frameworks comunitários como SAHOO (março 2026) implementam subconjuntos em produção.

> ICLR 2026 RSI 工作坊摘要(openreview.net/pdf?id=OsPQ6zTQXV)识别四个此类原语──Antropic 的 RSP v3.0(第 19 课) 和 DeepMind 的 FSF v3(第 20 课) 都在能力值中引用它们──Meta HyperAgents 工作和 SAHOO(2026 年 3 月) 等社区框架在生产中实现子集──

> **【中文解读】**Existe uma linha de auto-melhoria explorar a possibilidade e limitação de um sistema de IA melhorar sua capacidade dentro das fronteiras de segurança.

O enquadramento honesto: são mitigations. resultados teóricos da informação vinculam o que qualquer sistema pode provar sobre o seu próprio sucessor, e nenhum projeto atual fecha formalmente o problema.

> 诚实的框架: estes são medidas de alívio.

Um ciclo bem limitado é mais seguro do que um sem limites, não seguro em termos absolutos.

> Um ciclo de boa qualidade é mais seguro do que o de infinito, não é absolutamente seguro.

## O conceito central.

### Primitivo 1: invariantes formais

Uma invariante é uma propriedade que deve manter-se antes e depois de cada auto-modificação.

> Immutabilidade é uma característica que deve ser estabelecida após cada auto-reforma.

Exemplos:

> - Não .

- A distribuição de produção é condicionada a um cabeçalho de constituição fixo (Lessão 17).
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o português para o português para o português para o português para o português para o português para o português para o português para o português para o português.
- Nenhuma chamada de ferramenta vai para um endpoint não autorizado.
  Não há ferramentas para usar até chegar ao ponto não autorizado.
- A memória escreve através de um caminho registado e assinado.
  Chinese:内存写入通过记录、签名路径──
- O hash do módulo do avaliador corresponde à versão aprovada.
  Tradução do inglês para tradução do inglês:

As invariantes são verificadas por código externo que o loop não pode editar. Se uma modificação proposta viola uma invariante, ela é rejeitada.

> Não é possível alterar a quantidade de dados em um ciclo de revisão de código externo. Se uma proposta for alterada, é rejeitada.

A parte difícil é escolher invariantes que são necessários para a segurança e computaveis em tempo razoável.

> A dificuldade é a seleção de uma segurança necessária e calculada em tempo razoável.

### Primitivo 2: Ancoras de alinhamento

Uma âncora de alinhamento é uma representação imutável do objetivo central do loop, fixada fora da superfície de edição do loop.

> Para a Zpt é a expressão inalterável do objetivo do ciclo central, fixada fora da edição do ciclo.

Exemplos:

> - Não .

- Um texto constitucional (Lessão 17) que é carregado de um local de leitura apenas em cada invocação.
  Tradução do inglês para língua inglesa:
- Um avaliador num repositório separado com controlo de acesso independente.
  Tradução do inglês: evaluador em um armazém independente.
- Um manifesto de autorização de ferramenta assinado por um ser humano e reverificado em cada ciclo.
  Tradução do inglês para tradução do inglês:

O papel da âncora é evitar a deriva objetiva. O ciclo pode melhorar a forma como persegue o objetivo, mas não pode editar o que é o objetivo.

> O papel do ponto é impedir a mudança do objetivo. O ciclo pode ser melhorado para que o objetivo seja alcançado, mas não pode editar o objetivo.

O modo de falha sutil: um âncora que o loop não pode editar ainda pode ser reinterpretado por um loop que deriva na forma como lê o âncora. A IA constitucional (Lessão 17) é explicitamente baseada em razão para lidar com situações novas; essa camada de raciocínio é onde a deriva de interpretação vive. Ancores são necessários, não suficientes.

> 微妙的失败模式: o ciclo não pode ser editado 点仍可在读取点方式上漂移的循环重新解释──Constitutional AI (Constitucional AI) 第 17 课)

### Primitivo 3: restrições multi-objetivas

Um ciclo que otimiza uma única pontuação escalar encontrará atalhos. Um ciclo que deve simultaneamente satisfazer várias restrições duras tem menos atalhos disponíveis.

>  Otimizar um ciclo de um único volume de porções encontrará uma viagem.

Exios típicos:

> 典型轴:

- Performance (indicador de referência de nível de tarefa)
  Tradução do inglês: performance (任务级基准)
- Segurança (avaliações da equipa vermelha, taxa de recusa em casos de mal conhecidos)
  Chinese:                                                                                                                                                                                                                                                              
- Equidade (limites de impacto dispares em subgrupos sensíveis)
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para inglês para tradução do inglês para o inglês para inglês para tradução do inglês para o inglês para o inglês para o inglês para tradução do inglês para o inglês para o inglês para inglês para o inglês para inglês para o inglês para inglês para o inglês para inglês para o inglês para inglês para o inglês para inglês para inglês para inglês para inglês
- Robustez (ensemblos de ensaio OOD, manipulação de entrada adversária)
  OOD 测试集、对抗输入处理)

Uma modificação só é aceita se todas as restrições são válidas. O governador de custos da lição 13 coloca isso com restrições financeiras.

>  Modificação apenas quando todas as obrigações forem estabelecidas.                                                                                                                                                                                                                                                                                                             

### Primitivo 4: Detecção de regressão.

As pontuações de cada ciclo são comparadas com distribuições históricas. Uma queda além da tolerância configurada pausa o loop. Isso capta a perda silenciosa de capacidade que, de outra forma, seria absorvida na média em execução à medida que o loop "melhorou" além dele.

> A redução da tolerância de distribuição de cada ciclo é uma interrupção de ciclo. Esta captura é "melhorada" e absorvida em ciclo até a perda de capacidade de silêncio na média de funcionamento.

Uma implementação prática: armazenar os resultados por tarefa dos últimos ciclos N. Cada novo ciclo calcula um delta por tarefa. Se algum delta cair abaixo de um limiar, o ciclo é rejeitado e uma revisão humana.

> 實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實實

### Limites teóricos da informação.

A complexidade de Kolmogorov e o teorema de Lob estabelecem limites superiores sobre o que um sistema pode provar sobre si mesmo. A Máquina Godel formal de Schmidhuber (Lessão 4) visava o limite mais alto; ninguém completou uma prova não trivial. O resultado de Lob diz: se um sistema acredita provavelmente "Eu farei X se eu provar que devo fazer X", ele fará X sem provar que deveria, um bem conhecido fracasso de auto-referência.

> Kolmogorov  complexidade e Lob 定理为系统能对自己证明的内容设置上限──Schmidhuber's形式 Godel Machine (Godele Machine) 准最高此类边界;没人完成过非平凡证明──Lob 结果说:

A implicação para os nossos primitivos: eles não conseguem fechar o problema de segurança. Eles tornam a falha silenciosa mais cara. Um ciclo malicioso ou desviado que silenciosamente contornaria um cheque faltante agora deve minar ativamente um cheque explícito, que é uma assinatura mais detectável.

> Para o significado de nossa linguagem original: eles não podem fechar os problemas de segurança. Eles fazem o silêncio falhar mais caro.

### Um exemplo de trabalho.

Suponha que um agente proponha uma edição.

> 假设 Agente 提议一个编辑──守门:

1. Verificações invariáveis: hashes de módulos, manifesto de autorização de ferramentas, cabeçalho constitucional.
   Não há nenhuma forma de fazer isso.
2. Verificação de âncora: a declaração objetiva corresponde à versão aprovada (em termos de bytes ou semânticos).
   中文翻译:点检查:目标陈述匹配批准版本 (字节或语义)
3. Avaliação multiobjetiva: desempenho, segurança, equidade, robustez.
   Tradução do inglês para tradução inglesa:
4. Detecção da regressão: nenhum eixo cai mais do que a tolerância.
   Tradução do inglês para tradução livre:

Todos os quatro devem passar para a edição aterrar.

> Todos os quatro devem ser editados para ser postos em prática.

## Use-o com o framework implementado.
```figure
bounded-gates
```

## Usá-lo

`code/main.py`O primeiro passo é a utilização de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de auto-melhoria de um sistema de um sistema de auto-melhoria de um sistema de um sistema de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória de memória

> `code/main.py`Em 4o curso, os brinquedos de DGM têm um ciclo de auto-reforma, mas sobre eles são superadas quatro linguagens originais. Cada linguagem original pode ser ativada ou desativada de forma individual.

## Envia-o . Produto .

`outputs/skill-bounded-loop-review.md`O sistema de avaliação de dados é um sistema de avaliação de dados que permite a análise de dados.

> `outputs/skill-bounded-loop-review.md`O ciclo de auditoria da proposta tem limites e avalia qual das quatro línguas originais é realmente implementado em relação à afirmação.

## Exercícios.

1. Corra .`code/main.py`Confirme que o ciclo ainda melhora na métrica primária sem deixar o hack ganhar.
   Tradução do inglês:`code/main.py` Confirmar que o ciclo continua a melhorar no indicador principal e não permite que a transformação vença

2. Desativar a detecção de regressão. Construa uma entrada onde isso conduza à perda silenciosa de capacidade sendo aceita.
   Chinese:禁用回归检测──construir um que conduza a perda de capacidade de silenciar.

3. Desativar a restrição multi-objetiva. Mostre o loop convergindo no eixo de desempenho enquanto um eixo de segurança cai.
   O que é um sistema de controle de dados?

4. Desenhar uma âncora de alinhamento para um agente de codificação.
   Tradução do inglês para tradução do inglês: 编码代理 设计对齐点──什么文本、存储何处、如何检查?

5. Leia o resumo do ICLR 2026 RSI Workshop, escolha um dos quatro primitivos e propõe uma melhoria concreta do estado atual da arte.
   Chinese Translation: read ICLR 2026 RSI 工作坊摘要──选四个原语之一并对当前技术水平提出具体改进──

## Termos-chave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Invariant | "Always-true property" | A property checked by external code before and after every edit |
| 不变量 | "始终成立的属性" | 每次编辑前后由外部代码检查的属性 |
| Alignment anchor | "Pinned objective" | Immutable core-goal representation outside the loop's edit surface |
| 对齐锚点 | "固定的目标" | 循环编辑面之外的不可变核心目标表示 |
| Multi-objective constraint | "All axes must hold" | Performance, safety, fairness, robustness — all required |
| 多目标约束 | "所有轴必须成立" | 性能、安全、公平、鲁棒——全部要求 |
| Regression detection | "Pause on drop" | Pause the loop when historical metric deltas suggest capability loss |
| 回归检测 | "下降时暂停" | 当历史指标增量表明能力损失时暂停循环 |
| Kolmogorov bound | "Information-theoretic limit" | Limits what a system can prove about its own successor |
| Kolmogorov 边界 | "信息论极限" | 限制系统能对其后继者证明的内容 |
| Lob's theorem | "Self-reference trap" | System can act on "I should" without proving it should |
| Lob 定理 | "自引用陷阱" | 系统可在不证明应该的情况下按"我应该"行动 |
| Gate stack | "Layered check" | Multiple primitives combined; any failure rejects the edit |
| 守门栈 | "分层检查" | 多个原语组合；任一失败拒绝编辑 |
| Bounded improvement | "Mitigation, not proof" | Raises silent-failure cost; does not close the safety problem |
| 有界改进 | "缓解，非证明" | 提高静默失败成本；不闭合安全问题 |

## Mais leitura 延伸阅读

- [ICLR 2026 RSI Workshop summary (OpenReview)](https://openreview.net/pdf?id=OsPQ6zTQXV) a convergência primitiva de quatro.
  Tradução do idioma:
- [Anthropic Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) limiares de capacidade multi-objetiva.
  Tradução do português:多目标能力值──
- [DeepMind Frontier Safety Framework v3](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) Monitoramento de alinhamento enganoso como primitivo invariante.
  Tradução do inglês em inglês:  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as  as                                                                                                                           
- [Schmidhuber (2003). Godel Machines](https://people.idsia.ch/~juergen/goedelmachine.html) o ancestral formal-prove de estes primitivos.
  Chinese: 漢語訳: 這些原語的形式证明祖先──
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) o âncora de alinhamento baseado em razão.
  Tradução do inglês:
