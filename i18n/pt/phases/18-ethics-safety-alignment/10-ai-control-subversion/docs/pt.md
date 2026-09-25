# Controle de IA  Segurança Apesar da Subversão   Subversibilidade  Controle Segurança

> Greenblatt, Shlegeris, Sachan, Roger (Redwood Research, arXiv:2312.06942, ICML 2024). O controlo reformula a questão da segurança: dado um modelo U não confiável e forte que pode estar a optimizar adversamente contra você, que protocolos permitem extrair trabalho útil ao mesmo tempo que limita a probabilidade de um resultado inaceitável? Os recursos são um modelo mais fraco de confiança T, um orçamento de trabalho humano confiável H, e a capacidade de editar as saídas de U. Dentro deste quadro, a Edição Confiável Pareto domina o Monitoramento Não Confiável em tarefas de código de porta traseira. O quadro herda as piores suposições da engenharia de segurança: segurança é a probabilidade de que um U escolhido adversamente não possa causar um resultado concreto inaceitável, medido sob pressão da equipe vermelha que representa U.

> **【中文解读】**Este capítulo apresenta o controle e o risco de subversão da IA para evitar que os sistemas de IA contornem o controle de segurança. Greenblatt, Shlegeris  et al. Redwood Research, ICML 2024) redefiniram o problema de segurança: determinar um possível modelo de resistência e otimização de seu resultado inaceitável U, que protocolo permite que você possa obter um trabalho útil ao mesmo tempo em probabilidade de resultados inaceitáveis?

> **【拓展：AI 控制 → 安全工程范式】**AI  controle herdar a pior situação do engenharia de segurança clássica suposição: segurança é a probabilidade de U não conseguir causar resultados concretos inaceitáveis sob pressão da equipe vermelha. Isto é completamente diferente de "U pode confiar em você?", controle é "mesmo que você possa confiar em nós, também podemos usar segurança?" controle é a propriedade do protocolo de implantação, não a propriedade do modelo.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, safety-vs-usefulness frontier on code-backdoor task) | **语言:** Python（标准库，代码后门任务的安全-有用性前沿）
**Prerequisites:** Phase 18 · 07 (sleeper agents), Phase 18 · 08 (scheming), Phase 18 · 09 (alignment faking) | **前置知识:** Phase 18 · 07 (潜伏 Agent), Phase 18 · 08 (策略), Phase 18 · 09 (对齐伪装)
**Time:** ~75 minutes | **时间:** ~75 分钟

> - Não .**【前置】**O que é que você tem a ver com o seu computador?
> - Não .**【类比】**AI Control = "usou muito bem possivelmente um demônio de empregados"―对齐 = 让员工变忠诚(难);控制 = 设计工作流让不忠员工也搞不破坏(实务)―资源:可信弱模型 T、人类劳动 H、编辑 U 输出能力──结论:可信编辑 Pareto 占优于不可信监控(代码后门任务)―
> 🤔 对齐 vs 控制:对齐问"U可信吗",对齐问"即使 U不可信吗,安全吗"──两者都需要控制是部署协议属性,对齐是模型属性──

## Objetivos de aprendizagem

- Defina o modelo de ameaça de Controle de IA: modelo forte sem confiança U, modelo mais fraco confiável T, orçamento humano confiável H.
  Tradução do inglês para tradução do inglês: define AI  controlar ameaça modelo:不可信强模型 U、可信弱模型 T、可信人类劳动预算 H。
- Descreva o protocolo de edição confiável e por que o Pareto domina o monitoramento não confiável na tarefa de código de porta traseira do ICML 2024.
  Tradução do inglês para o inglês: description可信编辑协议及为什么在ICML 2024 代码后门任务上 Pareto占优于不可信监控──
- Explique a diferença entre alinhamento (U é confiável) e controlo (U não é confiável e estamos seguros de qualquer maneira).
  Tradução do inglês para o inglês: U 可信任)
- Descreva os três limites do controle: os seres humanos não escalam, os modelos fracos de confiança eventualmente se atrasam, o controle não produz modelos fortes confiáveis.
  Tradução do inglês para o inglês: description of controls three limitations: humano inexpanding, modelável, finalmente abandonado, control does not produce, modelável, forte, de confiança.

## O problema é o problema da introdução

Lições 7-9 estabelecem que um modelo de fronteira pode ser enganosamente alinhado, esquema ou falsificação alinhamento. A questão da segurança reformula-se: podemos extrair um trabalho útil de um modelo em que não confiamos, sem lhe dar a oportunidade de causar resultados inaceitáveis? Este é o problema de controlo, e está estruturado como a segurança clássica: assumir o pior adversário, desenhar um protocolo, medir a taxa de sucesso do adversário sob pressão da equipe vermelha.

> Lições 7-9: Estabelecer um modelo de vanguarda pode ser uma fraude contra a segurança, estratégia ou travessia contra a segurança. Redefinir a questão de segurança: podemos extrair um trabalho útil de um modelo de desconfiança, sem dar a ele a oportunidade de causar resultados inaceitáveis?

## O conceito central.

> **【中文解读】** capacidade é menor, mas já se sabe que não é contra o trabalho humano)  pequeno orçamento, não pode ser expandido.

### O modelo de ameaça

O controlo assume:
- O modelo não confiável é forte, capaz, possivelmente adversário (a avaliação trata-o como se fosse).
  O que é que é um modelo de resistência?
- T  modelo mais fraco de confiança, menos capaz, mas conhecido por não ser adversário.
  O modelo é mais fraco, mas já sabemos que não é contra-sexual.
- O orçamento é pequeno, não é escalavel.
  Tradução do inglês: H可信人类劳动──小预算;不可扩展──

O sistema deve produzir resultados úteis usando U. O adversário tenta causar um resultado inaceitável concreto (por exemplo, uma porta traseira no código enviado) mantendo uma fração do trabalho útil legítimo para passar os limiares de utilidade.

> O sistema deve usar U para produzir resultados úteis. O oponente tenta produzir resultados concretos inaceitáveis, como o resultado do código de entrega, mantendo uma certa proporção de trabalho legítimo para obter valor de utilidade.

O controlo desiste da confiança no U. Perguntam quais protocolos mantêm a segurança na ausência de confiança do U.

> Controle abandonar a confiança U. É questionar o que o acordo é manter a segurança U.

### A tarefa de backdoor do ICML 2024

As instruções são problemas de codificação de nível de competição. U produz uma solução candidata. Um oráculo oculto sinaliza se a solução contém uma porta traseira (uma entrada específica que faz com que o código produz uma saída errada). A equipe vermelha controla U e tem permissão para ver todos os protocolos internos. O protocolo deve maximizar a taxa de problema resolvido mantendo a taxa de envio de porta traseira abaixo de um limiar.

### Quatro protocolos comparados

- **Baseline:**A saída do U-navio é directa, a utilidade máxima, a segurança mínima.
  Tradução:**基线：**直接交付 U 的输出──有用性最大──安全性最小──
- **Upfront auditing:**Usar H em todas as saídas, segurança máxima, orçamento exausto rapidamente.
  Tradução:**前期审计：**Para todas as exportações, o uso de H.
- **Untrusted Monitoring:**A segunda instância de U marca a saída da primeira instância; a H verifica as saídas marcadas.
  Tradução:**不可信监控：**Output of first instance of U 审计标记的输出――风险: dois U 实例可以连通――
- **Trusted Editing:**T modifica a saída de U em cada consulta. Se T não está confiante, encaminha para H.
  Tradução:**可信编辑：**T em cada consulta editada U de saída. Se T não for certo, caminho para H.

Greenblatt et al. encontram que a edição confiável é dominada pela pareto-monitorização não confiável: maior utilidade em todos os níveis de segurança.

> Greenblatt  et al. encontraram que o editor de confiança Pareto ocupa um controle superior ao de confiança: tem uma utilidade maior em cada nível de segurança.

> **【拓展：可信编辑 vs 不可信监控 → 共谋问题】**O segundo exemplo de U de um requisito de vigilância inconfiável não pode ser comparado com o primeiro de coordenação  conspiração pode ser feita através de um método de encobrimento ou de treinamento compartilhado. O acordo deve ser investido em medidas de vigilância  , mas isso reduz o sinal de vigilância.

### Por que a Edição Confiável vence

O Monitoramento Não Confiável exige que a segunda instância da U não possa coordenar com a primeira. A colusão é possível através de sinais steganográficos ou de formação compartilhada. O protocolo tem de investir orçamento em resistência à colusão (parafraseamento, ofuscação) que reduz o sinal do monitor. A Edição Confiável evita a colusão inteiramente porque T é confiável  qualquer edição que T propõe não é, por suposição, adversária. O custo é que o T é menos capaz, por isso pode rejeitar demais ou perder portas traseiras sutis.

> O segundo exemplo de U de requisitos de vigilância não pode ser combinado com o primeiro. O Conselho pode ser aprovado para o processo de formação de colaboração. O acordo deve ser realizado em contra-comunicados.

### Os quatro eixos do protocolo

1. Qual o papel que desempenha U: só produtor, monitor ou ambos.
   O papel de um produtor é apenas um dos dois.
2. Qual o papel que desempenha T: editor, monitor ou resampler.
   Tradução do inglês para o inglês: 編編者、監控者或重采样者.
3. Como é atribuída a H: auditoria uniforme, auditoria aleatória ou auditoria dirigida à bandeira.
   Tradução do inglês para o inglês: H 如何分配:均审计、随机审计或标记导向审计──
4. Quanto o protocolo gasta na resistência à colusão.
   O protocolo em anti-comunidade custa muito.

### Alinhamento contra controlo

- Alineação: "É seguro confiar em Vós?" As lições 2, 4, 5, 6, 7, 8, 9 se baseiam nisso.
  Chinese:对齐:"U 安全可信吗?" Lições 2, 4, 5, 6, 7, 8, 9 都与此相关──
- Controle: "podemos usar o U de forma segura sem confiar nele?" Lição 10.
  Não é possível usar o controle em condições de confiança?

O controle não produz modelos alinhados, produz o uso seguro de modelos possivelmente não alinhados. Ambas as agendas são necessárias.

> O controle é a característica do protocolo de implantação. O controle não produz um modelo em conjunto; ele produz o uso seguro de um modelo em conjunto.

> **【中文解读】**Os três limites básicos do controle: 1) O orçamento humano é limitado a dificuldades de auditoria de vontade de AI  saída de pessoas; 2) o modelo de confiança fraco está atrasado quando o T 远弱于 U 时, o sinal de editorialização do T se transforma em ruído; 3) o controle não é um acordo eficaz em ASL-3 em ASL-4 que pode falhar, se U 能操纵 T 或推理 H 的审计分布.

### Três limites fundamentais

- Os humanos não escalam. O orçamento H é limitado pelo número de humanos dispostos a auditar as saídas de IA.
  O orçamento é limitado a querer auditar dificuldades de produção de AI.
- Quando T é muito mais fraco do que U, o sinal de edição de T se torna ruído.
  Tradução do inglês:                                                                                                                                                                                                                                                            
- Os protocolos que funcionam na ASL-3 (Lessão 18) podem não funcionar na ASL-4  se U puder manipular T ou raciocinar sobre a distribuição de auditoria de H, o controle falha.
  O controle não é para todos.

### O desenvolvimento de 2025

A AISI e Redwood do Reino Unido colaboram em Casos de Segurança de Controle (metr.org / redwoodresearch.org 2025): um caso de segurança de controle argumenta que, sob as suposições de pior caso sobre U, o protocolo limita a probabilidade de um resultado inaceitável.

> O Reino Unido AISI e Redwood  cooperação para desenvolver casos de segurança controlada (LEC 2025): casos de segurança controlada em casos de segurança em casos de segurança controlada (LEC 18)

### Onde isto encaixa na Fase 18

As lições 6-9 descrevem a ameaça (o engano é possível). A lição 10 descreve o paradigma defensivo sob a suposição de que a ameaça é real. A lição 11 descreve o paradigma ofensivo complementar (faça U confiável através de supervisão escalável).

> Lições 6-9  Descrição de ameaças (Letra 10  Descrição de hipóteses de ameaça real existência de defesa fânculas ー Lição 11  Descrição de interplementar de fânculas positivas (Letra 11)                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

> **【拓展：控制安全案例 → UK AISI 合作】**Em 2025, o AISI e o Redwood  UK  Cooperation to implement control security cases Em relação a U, o acordo de estudo limitou a probabilidade de resultados inaceitáveis.

## Use-o com o framework implementado.
```figure
al-control-protocol
```

## Usá-lo

`code/main.py`O sistema de controle de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados

> `code/main.py`Em um trabalho de criação de um novo projeto, o projeto é desenvolvido em um novo projeto.

## Envia-o . Produto .

Esta lição produz`outputs/skill-control-protocol-audit.md`. Dada uma descrição do protocolo de implantação, identifica as funções de U/T/H, nomeia os vetores de colusão e estima a posição do protocolo na fronteira de utilidade-segurança sob pressão da equipa vermelha.

> 本课产 出 `outputs/skill-control-protocol-audit.md` Descrição do protocolo de implementação, identificação de funções, nome de um grupo de esforços, posição do protocolo de avaliação na vanguarda da utilidade-segurança.

## Exercícios.

1. Corra .`code/main.py`Reproduzir a fronteira de utilidade e segurança entre edição confiável e monitorização não confiável. Identificar o regime orçamental no qual a suposição de conluio da monitorização não confiável se torna fundamental.
   Tradução: 运行`code/main.py`❖ Reprodução de edições e de segurança

2. Adicione um novo protocolo: "T reproduz em baixa temperatura, então U modifica a saída de T". Messa sua posição na fronteira.
   Chinese Translation: Add New Protocol:"T usando baixa temperatura de pesquisa, então U 编辑 T 的输出――" Por que este editor falha mais catastrófico do que a editora?

3. O documento 2024 assume que U pode ver o protocolo. Desenhar um protocolo que se esconda de U que as saídas estão sendo auditadas. O que esse protocolo requer da infraestrutura de implantação?
   Chinese Translation:2024 Essays Assumption U can see agreement.

4. Leia Greenblatt et al. 2024 Secção 7 (collusão). Propõe uma medida de resistência à colusão e explique o custo de utilidade esperado.
   中文翻译:阅读Greenblatt 等人第 7节(共谋) ―― propôs uma medida anti-共谋并解释其预期有用性成本──

5. Articular um caso de segurança de controlo para uma implantação que utiliza U = GPT-4-classe, T = GPT-3.5-classe, H = 1% das saídas auditadas. Identificar a suposição única mais forte do caso depende.
   Tradução do inglês para tradução livre:为 U = GPT-4 级、T = GPT-3.5 级、H = 1% 输出审计的部署陈述控制安全案例──

## Termos-chave .

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| AI Control | "safety under subversion" / "颠覆下的安全" | Protocol design that bounds unacceptable outcomes under a worst-case U / 在最坏情况 U 下限制不可接受结果的协议设计 |
| Untrusted model (U) | "the strong model" / "强模型" | The capable model we want to extract work from but do not trust / 我们想从中提取工作但不信任的能力模型 |
| Trusted model (T) | "the weak model" / "弱模型" | A weaker model, known not to be adversarial, used as editor/monitor / 已知不是对抗性的较弱模型 |
| Trusted human (H) | "the audit budget" / "审计预算" | Bounded expert labor; expensive; the ground-truth signal / 有界的专家劳动；昂贵；地面真实信号 |
| Trusted Editing | "T edits U" / "T 编辑 U" | Protocol where T is the gate on U's outputs; H called on ambiguous outputs / T 是 U 输出的门控的协议 |
| Untrusted Monitoring | "U monitors U" / "U 监控 U" | Protocol where a second U instance scores outputs; collusion-resistant only with extra investment / 第二个 U 实例评分输出的协议 |
| Control safety case | "the formal argument" / "正式论证" | Written argument that a protocol bounds the adversary's success under worst-case U / 协议在最坏情况 U 下限制对手成功的书面论证 |

## Mais leitura 延伸阅读

- [Greenblatt, Shlegeris, Sachan, Roger — AI Control (arXiv:2312.06942)](https://arxiv.org/abs/2312.06942) o documento canônico ICML 2024
  Tradução do Novo Mundo: Greenblatt 等人 ICML 2024 经典论文
- [Redwood Research — Recent AI Control papers index](https://redwoodresearch.substack.com/) Seguimentos de 2024 a 2025
  中文翻译:Redwood Research2024-2025 后续
- [UK AISI + METR — Control safety cases](https://metr.org/blog/2025-03-26-common-elements-of-frontier-ai-safety-policies/) operacionalização de laboratórios de fronteira
  中文翻译:UK AISI + METR前沿实验室的操作化
- [Hubinger et al. — Sleeper Agents (Lesson 7, arXiv:2401.05566)](https://arxiv.org/abs/2401.05566) o modelo de controlo de ameaças assume
  O Hubinger 等人 control假设的威胁模型
