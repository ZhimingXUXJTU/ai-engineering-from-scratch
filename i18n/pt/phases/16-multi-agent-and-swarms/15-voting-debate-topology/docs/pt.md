# Votar, auto-consistência e topologia do debate

> A mais barata agregação: amostra N agentes independentes, maioria-voto. Wang et al. 2022 autoconsistência fez isso com um modelo amostrado N vezes. Multi-agente amplia com **heterogeneous**Agentes para escapar da monocultura  diferentes modelos, diferentes indicações, diferentes temperaturas, diferentes contextos. Além da maioria dos votos, debate topologia questões: MultiAgentBench (arXiv:2503.01935, ACL 2025) avaliou a coordenação estrela / cadeia / árvore / gráfico e encontrou **graph best for research**O AgentVerse (ICLR 2024) documenta dois padrões emergentes  comportamentos voluntários e comportamentos de conformidade  e a conformidade é tanto uma característica (encontrando consenso) quanto um risco (pensamento em grupo, lição 24). Esta lição mapeia o espaço topológico, constrói cada variante e mede o imposto de coordenação.

> **【中文解读】**Esta secção apresenta a estrutura organizacional de votação e debate para tomar decisões através de vários agentes.

> **【拓展：voting debate topology→具体应用】**投票和辩論拓 形形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形  形 形    形 形     形 形   形      形      形                                                                                                              


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 14 (Consensus and BFT) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 14（共识与 BFT）

> - Não .**【前置】**O processo de decisão é um processo de decisão que se deve realizar com a participação de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de representantes de um grupo de grupos de representantes de um grupo de grupos de representantes de um grupo de grupos de representantes de um grupo de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos.
> - Não .**【类比】**投票拓 = "conferência de mesa de colocação"──星形 = 圆桌投票(独立);链形 = 接力修改(前面 Agente de saída 传给下一个);图形 = 圆桌讨论(多轮交互)──MultiAgentBench 结论:图形适合研究任务但有"协调税"──>4 个 Agente 性价比下降)──异质性是关键不同模型/温度/快速 防单一文化错误──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problema Introdução

O debate pode melhorar a precisão (Du et al., arXiv:2305.14325).

> O debate pode aumentar a precisão, mas também pode reduzir a precisão.

1. Quem fala com quem (topologia).
   Tradução do inglês:
2. Quantas rondas (Du 2023: ambas as rondas e agentes importam independentemente).
   Tradução do inglês: How many times (do 2023)
3. Se os agentes são heterogêneos (modelos base diferentes quebram a monocultura).
   O agente é um agente de uma cultura diferente.
4. Se há ou não uma voz adversária (steel-manning vs straw-manning).
   O que é que é o "resistente" de uma pessoa?

As equipes que "exercem 5 agentes e votam" em uma tarefa geralmente regressam contra um único agente. Os falhas não são aleatórios. Eles rastream topologia e heterogeneidade. Esta lição é o mapa topológico.

> O grupo vai "carregar 5 agentes e votar" duro adicionado à tarefa, de vez em quando o desempenho de um único agente é pior.

## Conceptos básicos

### Autoconsistência, linha de base de modelo único

Wang et al. 2022 ("A autoconsistência melhora a cadeia de raciocínio do pensamento") amostrou o mesmo modelo N vezes a temperatura > 0 e votou a maioria nas respostas do caminho de raciocínio. O resultado no GSM8K: ganhos substanciais com amostras N = 40 em uma única decodificação gananciosa.

> Wang 等人 2022 年 (("autoconsistência melhorando a ideia de pensar na teoria") em condições de temperatura > 0 para a mesma amostra de modelos N 次,并对推理路径答案进行多数投票――GSM8K 上的结果:N=40 次采样比单次贪心解码有显著提升――autoconsistência é um único agente 投票的多代理 前身――

Limites: autoconsistência usa um modelo base. erros são correlacionados pela construção. Se o modelo tem um viés sistemático, todas as amostras N compartilham.

> Limitação: auto-considência usando um modelo básico. O erro na construção é relacionado. Se o modelo tiver uma parcialidade sistêmica, todos os N 个样本都共享它.

### Voto multi-agente, extensão heterogênea

Substitua as amostras N por N * diferentes* agentes. Diferentes modelos base (Claude, GPT, Llama), diferentes instruções, acesso a ferramentas diferente. O benefício: erros não correlacionados. O custo: diferentes agentes custam diferentes quantidades; coordená-los adiciona custos gerais.

> N 个样本将换成 N 个*不同*的代理――不同的基础模型(Claude、GPT、Llama), diferentes提示, diferentes工具访问──好处:不相关的错误──代价:不同代理的成本不同;协调它们增加开销──

O nome canônico para o debate heterogêneo para 2026 é **A-HMAD** Debate heterogêneo multi-agente adversário. Não é universalmente adotado, mas os artigos usam o termo para "debate de modelos diferentes, o que reduz os erros correlacionados do colapso da monocultura".

> 2026 ano de diferença de debate**A-HMAD** À contra-abstinência de diversos tipos de debates 辩论──并非普遍采用,但论文使用这个词指"不同模型辩论,减少单一文化崩的相关错误"──

### As quatro topologias

```
star                chain               tree                graph

    ┌─A─┐           A─B─C─D         ┌──A──┐              A───B
    │   │                           │     │              │ × │
    B   C                           B     C              D───C
    │   │                          / \   / \
    D   E                         D   E F   G           (fully connected)
```

Uma linha, todas as outras falam apenas com a linha, equivalente a um supervisor sem canal de volta.
Chain: linear, cada agente vê a saída do anterior.
Árvore: hierárquica, utilizada pelos sistemas de agentes hierárquicos (Lessão 06).
Grafico: qualquer um a qualquer. Inclui clique totalmente conectado e DAGs arbitrários.

> Estrátil: um centro, todos os outros agentes apenas com o centro conversação.
> 链形:线性, cada Agente 看到前一个Agente 的输出──类似流水线──
> 树形:层次化,用于层次化 Agent 系统 (→ 6o curso)
> 图形: arbitrária até arbitrária──incluindo totalmente conectado do grupo e arbitrária DAG──

### O imposto de coordenação (MultiAgentBench)

MultiAgentBench (MARBLE, ACL 2025, arXiv:2503.01935) benchmarked estrela, cadeia, árvore, gráfico em um conjunto de tarefas incluindo pesquisa, codificação e planejamento. Resultados principais medidos:

> MultiAgentBench ((MARBLE,ACL 2025,arXiv:2503.01935) realizou um teste de base para a forma de estrelas, cadeia, árvore e gráfico em um conjunto de missões que inclui o estudo, codificação e planejamento:

- **Graph**A topologia vence as tarefas de investigação.
  Tradução:**图形**拓在研究任务上获胜;信息随意流动;Agentes podem se criticar mutuamente.
- **Star**O Hub filtra e consolida.
  Tradução:**星形**Em resposta rápida, a tarefa de facto é a de ganhar.
- **Chain**ganhos em oleodutos gradualmente (refinamento por etapas).
  Tradução:**链形**Em fase de desenvolvimento, a empresa está a ganhar.
- **Coordination tax**O valor do relógio de parede e do token crescem mais rápido do que a qualidade.
  Tradução:**协调税**Em um gráfico, aparecem cerca de 4 agentes.

O teto de 4 agentes é empírico, não fundamental. Reflete a capacidade de contexto de 2026 LLM: o contexto de cada agente se enche de resultados de pares, e o valor marginal de adição de agente N + 1 cai uma vez que todos podem ver todos.

> 4 O limite superior do agente é experiencial, não fundamental. Reflete a capacidade de produção de cada agente, quando todos conseguem ver cada um, o valor marginal do agente aumenta N+1.

### Estratégias de Debate Multidisponentes ("Deveríamos estar a ENFALAR?")

ArXiv:2311.17371 é a pesquisa de 2023 das estratégias MAD. Descoberta-chave replicada por outros: variantes MAD que são *estruturalmente semelhantes* à autoconsistência (ampliamento independente + agregação) muitas vezes apresentam um desempenho inferior à autoconsistência ao usar o mesmo orçamento.

> arXiv:2311.17371 é um resumo estratégico de MAD de 2023 ⋅ conclusão chave já foi repetida por outros: MAD variantes semelhantes à sua autoconformidade na estrutura ([[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

### AgenteVerse padrões emergentes

AgenteVerse (ICLR 2024, https://proceedings.iclr.cc/paper_files/paper/2024/file/578e65cdee35d00c708d4c64bce32971-Paper-Conference.pdf) documenta dois comportamentos que emergem do debate multi-agente, mesmo sem um desenho explícito:

- **Volunteer.**Um agente oferece ajuda ("Eu posso dar o próximo passo") sem ser solicitado. Útil: atribui trabalho ao agente mais capacitado para uma subtarefa.
  Tradução:**自愿者。**Agente 主动提供帮助 ((" posso fazer o próximo passo") 有用: vai distribuir o trabalho para o Agente com mais capacidade para as tarefas dos filhos
- **Conformity.**O agente ajusta a sua posição para corresponder a um crítico, mesmo quando o crítico está errado.
  Tradução:**从众。**Agente 调整立场以匹配批评者, mesmo que o crítico seja errado.

A conformidade é o motivo pelo qual o debate até acordo recompensa os intimidantes.

> De um lado, o "debatimento ao acordo" é o motivo pelo qual os políticos são incentivados a fazerem isso.

### Heterogeneidade: o botão real que move precisão

Um padrão 2024-2026 na literatura prática: trocar um dos seus agentes N por um modelo base diferente dá uma maior precisão do que aumentar N por 1.

> Um modelo da literatura prática de 2024-2026: substituir um de N 个代理 (N 个代理) em um modelo base diferente do que aumentar N + 1 个代理 (N + 1 个代理) 带来更大的准确率提升――直觉是单一文化 cada nova fonte de erro independente é mais valiosa do que extra,

Em um limite, a heterogeneidade supera a numerosidade. Três modelos diferentes superam cinco cópias de um modelo na maioria das tarefas que têm verdade de terra limpa.

> Em casos limitados, a diferença entre a construção e o número de respostas é maior. Na maioria das tarefas, três modelos diferentes são superiores a cinco duplicadas do mesmo modelo.

### Métodos de júri

O quadro Sibyl (citado na literatura Minsky-LLM) formaliza um "jurado"  um pequeno conjunto de agentes especializados que refinam respostas votando em cada etapa. Ao contrário do voto de maioria simples, um júri tem papéis: um agente interroga, um fornece contexto, um marca plausibilidade. Os métodos do júri são um ponto médio entre o voto simples (barato, propenso à monocultura) e o MAD completo (custo, propenso à conformidade).

> Sibyl framework (→ Links de Minsky-LLM) formalizou o "jurício" 一小组 especializado Agente 通过每阶段投票来改进答案──与简单多数投票不同, o júri tem papel: um Agente 交叉质询, um fornecer 上下文, um评分合理性── o método do júri é de simples votação (便宜,易单一文化) e um completo MAD (MAD) 昂贵,易从众) 

### Quando o voto com debate domina

- A questão tem verdade fundamental (fatos, matemática, comportamento de código).
  Chinese Language Translation: problema tem padrão de resposta ((factos, matemática, código de comportamento) ⋅ votação ⋅ receção ⋅ é significativo ⋅
- Os agentes podem aceder a diferentes fontes ou ferramentas (disponível a heterogeneidade).
  O agente pode acessar diferentes fontes ou ferramentas ([[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]).
- As rodadas são limitadas (2-3 típicas) e há um juiz ou verificador separado.
  Tradução em chinês:轮次有界 (normalmente 2-3 轮),有独立评委或验证器──
- O orçamento permite 3-5 agentes. Além de 5-7 em topologia gráfica, o imposto de coordenação domina.
  O orçamento permite 3-5 agentes.

### Quando a votação com debate dói

- A pergunta é de opinião, os agentes convergem para a resposta que parece mais confiante, não mais correta.
  Tradução do inglês para o inglês: question is opinion type of.
- Todos os agentes compartilham um modelo base.
  Chinese: 所有 Agent 共享基础模型──单一文化使共识无意义──
- As rodadas são ilimitadas, a conformidade ganha sempre.
  Tradução do inglês: 轮次无界──从众每次都赢──
- A tarefa é simples. Um agente único com autoconsistência em N=5 é mais barato e tão preciso.
  Tradução do inglês: task simple. Single Agent.

## Construí-lo.
```figure
sw-debate-topology
```

## Construí-lo

`code/main.py`Implementos:

- `run_star(agents, hub, question)` Pesquisas de cada trabalhador, agregados.
  Tradução:`run_star` Centro de consulta para cada trabalhador
- `run_chain(agents, question)` refinamento sequencial.
  Tradução:`run_chain` 顺序改进──
- `run_tree(root, children, question)` hierárquica com agregação profundidade-2.
  Tradução:`run_tree` 层次化,深度 2 聚合──
- `run_graph(agents, question, rounds)`- Debate total, rodadas limitadas.
  Tradução:`run_graph` Todo o debate, há uma rotina.
- Um dial de heterogeneidade scripted: cada agente tem um `error_bias`Indicando a sua erroneidade sistemática.
  Tradução do Novo Mundo: "Cada agente tem um".`error_bias`Indicar seu erro sistêmico.
- Um arame de medição que executa cada topologia em N=3, 5, 7 e relata (acurateza, total_tokens, wallclock_simulated).
  Tradução do inglês para tradução do inglês:                                                                                                                                                                                                                                                         

- Correr .

```
python3 code/main.py
```

Resultados esperados: uma tabela de topologia × N → (acurateza, tokens, latência). Grafico ganha em N=3-5 nas tarefas de estilo de pesquisa; estrela ganha nas tarefas de fatos rápidos; grafico em N=7 mostra o imposto de coordenação (latencia infla mais rápido do que precisão).

> 预期输出:拓 × N →(准确率,token,延迟)表格──图形在 N=3-5 的研究风格任务上获胜;星形在快速事实性任务上获胜;图形在 N=7 时显示协调税(延迟膨胀快于准确率)

## Usa-o. Usa-o.

`outputs/skill-topology-picker.md`é uma habilidade que lê uma descrição de tarefa e recomenda uma topologia (estrela / cadeia / árvore / gráfico), um N (número de agentes), um perfil de heterogeneidade (modelos básicos a utilizar) e um limite redondo.

> `outputs/skill-topology-picker.md`É uma habilidade, read取任务描述并推拓(星形/链形/树形/图形) 、N(Agenta 数量) 、异构配置(使用的基础模型) 和轮次上限──

## Envia-o .

Para qualquer conjunto:

- Começa com **self-consistency at N=5**O modelo base é o mais barato.
  Tradução do inglês: From a Strong Basis Model**N=5 自一致性**Começa... é um preço baixo.
- Avaliar para **heterogeneous voting at N=3**Se a precisão for importante, mede o delta.
  Se o índice de precisão é importante, eleva-se para **N=3 异构投票**◊ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈
- Apenas atualizar para **debate topology**se a tarefa tiver estrutura (investigação, múltiplas etapas) e se for possível realizar rodadas limitadas.
  Tradução do inglês para inglês: only in task has structure (), e há rotas disponíveis para a atualização.**辩论拓扑**- Não.
- Sempre registar o grupo de minorias. Quando uma minoria está persistentemente certa, você tem um sinal de diversidade.
  Quando a minoria continua correta, você tem sinais de diversidade.
- "Melhor precisão a 10 vezes o custo" é uma decisão empresarial.
  O "precision rate of 10 times cost" é uma decisão comercial.

## Exercícios.

1. Corra .`code/main.py`. Descrever a curva de coordenação-imposto para topologia do gráfico: precisão vs N, tokens vs N. Em que N a curva se inclui?
   Tradução: 运行`code/main.py`◊ desenhar um gráfico de um plano de curvatura de coordenação:
2. Implementar A-HMAD: três agentes com preconceitos deliberadamente diferentes. Como a linha de base de todos os mesmos preconceitos compara-se com A-HMAD no ataque de monocultura da lição 14?
   Tradução do inglês para tradução do inglês: implementar A-HMAD: três agentes com diferentes preconceitos intencionais.
3. Adicionar um papel de "juiz" à topologia do gráfico que não vota, apenas marca o consenso final.
   Tradução do inglês: In the diagramming area, do "comitê" é um papel, não votando apenas em um voto de consenso final.
4. Leia o artigo AgentVerse (ICLR 2024). Identifique qual é o comportamento emergente que a sua implementação mostra mais fortemente.
   Chinese: 阅读 AgentVerse 论文(ICLR 2024) ―― Identificar seu cumprimento mais intensamente demonstrar qual é o comportamento mais recente── Você pode através de sugestão mudar de comportamento?
5. Leia MultiAgentBench (arXiv:2503.01935) Seção 4 (experimentos topológicos). Reproduzir o resultado "grafo-ganha-investigação" em uma tarefa do papel usando o seu arnes.
   No entanto, o resultado do estudo foi muito mais rápido, com o resultado de um estudo de um estudo de um estudo de um estudo.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Self-consistency / 自一致性 | "Sample N times, vote" / "采样 N 次，投票" | Wang 2022. Single model, N temperature>0 samples, majority vote on reasoning paths. / Wang 2022。单模型，N 次 temperature>0 采样，推理路径多数投票。 |
| Heterogeneity / 异构性 | "Different models" / "不同模型" | Ensemble of different base models or prompt families. Breaks monoculture. / 不同基础模型或提示族的集成。打破单一文化。 |
| MAD / 多 Agent 辩论 | "Multi-agent debate" / "多 Agent 辩论" | Generic term for agents exchanging critiques over rounds. See Du 2023. / Agent 跨轮次交换批评的通用术语。见 Du 2023。 |
| A-HMAD / 对抗性异构 MAD | "Adversarial Heterogeneous MAD" / "对抗性异构 MAD" | MAD variant emphasizing different models + adversarial structure. / 强调不同模型 + 对抗结构的 MAD 变体。 |
| Topology / 拓扑 | "Who talks to whom" / "谁和谁对话" | Star, chain, tree, graph. Determines information flow. / 星形、链形、树形、图形。决定信息流。 |
| Coordination tax / 协调税 | "Diminishing returns" / "边际收益递减" | Above ~4 agents on graph, cost grows faster than quality. / 图形拓扑约 4 个 Agent 后，成本增长快于质量。 |
| Volunteer behavior / 自愿者行为 | "Unprompted help" / "主动帮助" | AgentVerse emergent pattern: an agent offers to take a step. / AgentVerse 涌现模式：Agent 主动提出执行步骤。 |
| Conformity behavior / 从众行为 | "Agreement under pressure" / "压力下的同意" | AgentVerse emergent pattern: an agent aligns with a critic. / AgentVerse 涌现模式：Agent 与批评者对齐。 |
| Jury / 陪审团 | "Small specialized panel" / "小型专业小组" | Sibyl-style ensemble with roles (examiner, context, scorer). / Sibyl 风格的带角色集成（质询者、上下文、评分者）。 |

## Mais leitura 延伸阅读

- [Wang et al. — Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171) Linha de base para um único modelo
- [Du et al. — Improving Factuality and Reasoning via Multiagent Debate](https://arxiv.org/abs/2305.14325) Os dois agentes e as rodadas são independentes
- [MultiAgentBench / MARBLE](https://arxiv.org/abs/2503.01935) índice de referência de topologia que mostra o gráfico melhor para a investigação, cadeia para os oleodutos
- [Should we be going MAD?](https://arxiv.org/abs/2311.17371) Pesquisa de estratégia MAD; constata que a MAD muitas vezes perde para a autoconsistência com orçamento igual
- [AgentVerse (ICLR 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/file/578e65cdee35d00c708d4c64bce32971-Paper-Conference.pdf) padrões emergentes de voluntariado e conformidade
- [MARBLE repo](https://github.com/ulab-uiuc/MARBLE) Implementação de referência
