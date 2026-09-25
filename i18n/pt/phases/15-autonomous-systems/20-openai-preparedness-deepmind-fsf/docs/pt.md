# OpenAI Preparação Framework e DeepMind Frontier Safety Framework .

> OpenAI Preparedness Framework v2 (abril de 2025) introduz categorias de pesquisa  Autonomia de longo alcance, Sandbagging, Replicação e Adaptação Autônoma, Minar salvaguardas  distintas das categorias rastreadas. As categorias rastreadas desencadeiam os relatórios de capacidades e os relatórios de salvaguardas revisados pelo grupo consultivo de segurança. O FSF v3 da DeepMind (septembro de 2025, com Níveis de Capacidade de rastreamento adicionados em 17 de abril de 2026) dobra a autonomia em domínios de P&D e Ciber (ML R&D autonomia nível 1 = automatizar completamente o pipeline de P&D da IA a custo competitivo versus ferramentas humanas + AI). O FSF v3 aborda explicitamente o alinhamento enganoso através de monitorização automatizada de uso indevido de raciocínio instrumental. A nota honesta: As categorias de pesquisa no PF v2 (incluindo Autonomia de longo alcance) não desencadeiam automaticamente mitigações; a linguagem de política é "potencial". A própria DeepMind diz que o monitoramento automatizado "não permanecerá suficiente a longo prazo" se o raciocínio instrumental forçar.

> **【中文解读】**Este capítulo apresenta os principais mecanismos de segurança de laboratórios de IA:


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-framework decision-table diff tool) | **语言:** Python（标准库，三框架决策表差异工具）
**Prerequisites:** Phase 15 · 19 (Anthropic RSP) | **前置知识:** Phase 15 · 19（Anthropic RSP）
**Time:** ~45 minutes | **时间:** ~45 分钟

> - Não .**【前置】**O estudo foi realizado em uma área de investigação de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa
> - Não .**【类比】**O sistema de segurança da empresa é um sistema de segurança de segurança de três aeronaves. O sistema de segurança de três aeronaves é um sistema de segurança de três aeronaves.
> 🤔 **【困惑】**P: Por que os RSP são voluntários? Porque não há lei obrigatória. A Lei da UE sobre IA é a primeira lei regional, mas apenas abrange a União Europeia.

## O problema é o problema da introdução

A lição 19 leu a política de escala da Anthropic de perto. Esta lição completa a imagem lendo OpenAI e DeepMind. Os três documentos são artefatos primos que abordam a mesma pergunta  quando um laboratório de fronteira deve pausar ou abrir um modelo  e convergem em um pequeno conjunto de categorias e divergem em lugares específicos que importam.

> No capítulo 19, foi lido detalhadamente a política de expansão da Antropic. Este curso foi lido através da política de OpenAI e DeepMind para completar o panorama.

A convergência: as três etiquetas autonomia de longo alcance como uma classe de capacidade que vale a pena rastrear. Todos os três reconhecem o comportamento enganoso como uma classe específica de risco. Todos os três têm um órgão interno de revisão. A divergência: a OpenAI divide as categorias em "Tracked" (mitigação obrigatória) e "Research" (sem desencadeamento automático). A DeepMind dobra a autonomia em dois domínios em vez de nomeá-la separadamente. Os nomes do laboratório são Tracked vs Research, ou Critical vs Moderate, ou Tier-1 vs Tier-2; a consequência operacional de qual balde uma capacidade vive é diferente entre os laboratórios.

> 收点:三者都将长程自主标记为值得跟踪的能力类别──三者都承认欺骗行为──对齐伪装、sandbagging) 是特定风险类别──三者都有内部审查机构──分歧点:OpenAI将分类为"Tracked"(强制缓解) 和"Research"(无自动触发)──DeepMind将自主性折叠成两个领域而不是单独命名──实验室命名Tracked vs Research、Critical vs Moderate、Tier-1 vs Tier-2;能力桶的运营后果在实验室间不同──

A mesma capacidade pode ser "mitigação obrigatória" na Anthropic, "monitorada mas não desencadeada" na OpenAI e " rastreada em um domínio específico" na DeepMind.

> A mesma capacidade em Antropic é "reforço forçado", em OpenAI é "monitoramento mas não toque", em DeepMind é "seguimento em um determinado campo"......

## O conceito central.

### O quadro de preparação da OpenAI v2 (abril de 2025)

Estrutura:

> 结构:

- **Tracked Categories**O relatório de medidas de salvaguarda (qualquer medidas de mitigação já em vigor) foi revisto pelo Grupo Consultivo de Segurança antes da implantação.
  Tradução:**Tracked Categories（跟踪类别）**O relatório de segurança da empresa foi publicado em 31 de janeiro de 2012 e foi publicado em 31 de janeiro de 2012 e foi publicado em 31 de janeiro de 2012 e publicado em 31 de janeiro de 2012 e publicado em 31 de janeiro de 2014.
- **Research Categories**A Comissão propõe que a Comissão adopte medidas de controlo de dados para a aplicação de medidas de controlo de dados e de controlo de dados, incluindo medidas de controlo de dados e de controlo de dados.
  Tradução:**Research Categories（研究类别）**O laboratório está a seguir, mas ainda não comprometeu-se a identificar a capacidade de modelagem de alívio.

A definição chave no v2: Categorias de pesquisa não desencadeiam automaticamente mitigações. A linguagem de política é mitigações "potenciais". Este é o delta específico para assistir: a localização de uma categoria em Tracked vs Research é a bisagra entre "permeado" e "observado".

> O quadro-chave do v2 é:Categorias de pesquisa Não automaticamente são provocadas por aceleradores.

### DeepMind Frontier Safety Framework v3 (september 2025; Tracked Capability Levels adicionados em 17 de abril de 2026)

Estrutura:

> 结构:

- **Critical Capability Levels (CCLs)**: limiares de capacidade em cinco domínios: Ciber, Bio, I&D do ML, CBRN, Autonomia (dobrado em I&D do ML e Ciber).
  Tradução:**Critical Capability Levels（CCL，关键能力等级）**A capacidade de desenvolvimento de máquinas e de desenvolvimento de máquinas (R&D)
- **Tracked Capability Levels**Exemplo concreto: ML R&D autonomia nível 1 = automatizar completamente o pipeline de R&D da IA a um custo competitivo versus ferramentas humanas + IA.
  Tradução:**Tracked Capability Levels（跟踪能力等级）**:2026  4 月 追加额外粒度──具体例:机器学习研发自主级 1 = 以与人类+AI 工具竞争的成本完全自动化AI 研发管道──
- **Deceptive alignment monitoring**: compromisso explícito com o controlo automatizado de abusos de raciocínio instrumental.
  Tradução:**欺骗对齐监控**• um compromisso claro de monitoramento automatizado da utilização abusiva de ferramentas.

A estruturação da autonomia difere da OpenAI. DeepMind não mantém "Autonomia" como um domínio de nível superior; é dobrada para os domínios onde a autonomia causaria danos (ML R&D e Cyber). O argumento é que a autonomia sem um domínio é capacidade sem risco; o contra-argumento é que a autonomia entre domínios é um meta-riesgo que o framework deve nomear.

> O DeepMind não vai reservar a "autonomia" para o domínio superior; ela é dobrada para o domínio onde a autonomia causará danos.

### O que os três convergem

- Grupo Consultivo de Segurança Interna (nomeado Anthropic SAG, OpenAI SAG, DeepMind comitê interno).
  中文翻译:内部安全咨询组 ((名为 ANTHROPIC SAG、OpenAI SAG、DeepMind 内部委员会) ――高能力模型部署前审查。
- Menção explícita de alinhamento enganoso / alinhamento fingido como uma classe de risco.
  Chinese:                                                                                                                                                                                                                                                              
- Artifactos permanentes em uma cadência declarada (Antropic: Roadmap de segurança fronteiriça, Relatório de riscos; OpenAI: Relatórios de Capacidades e Garantias; DeepMind: Ciclo de atualização do FSF).
  Tradução em inglês:                                                                                                                                                                                                                                                            
- Reconhecimento de que as defesas exclusivamente de monitorização têm um limite.
  Chinese:                                                                                                                                                                                                                                                              

### Onde divergem

- **Anthropic**: compromisso de pausa removido na v3.0; AI R&D-4 limiar é o nomeado próximo portal.
  Tradução:**Anthropic**:v3.0 移除暂停承诺;AI R&D-4 值是命名的下一个门控──
- **OpenAI**: Segurança versus pesquisa dividida; Categorias de pesquisa (incluindo autonomia de longo alcance) não se abrem automaticamente.
  Tradução:**OpenAI**:Tracked vs Research 分割;Categorias de pesquisa(incluindo长程自主)不自动门控──
- **DeepMind**A autonomia foi redobrada para outros domínios; os níveis de capacidade rastreados adicionam granularidade em abril de 2026.
  Tradução:**DeepMind**O desenvolvimento de um sistema de gestão de recursos humanos e de recursos humanos é um dos principais objetivos da União Europeia.

### Sandbagging: uma capacidade específica que complica os três

Sandbagging (um modelo estrategicamente com um desempenho inferior nas avaliações) está nas categorias de pesquisa da OpenAI. A RSP v3.0 da Anthropic aborda isso através da lacuna de avaliação-contexto (Lessão 1).

> Sandbagging (模型在评估中战略性表现不佳) (Research Categories of OpenAI) 中──Antropic RSP v3.0 通过评估上下文差距(第 1 课)处理──DeepMind 通过 FSF v3 的欺骗对齐监控处理──

Se um modelo não se baseia em avaliações, os limites de capacidade de cada quadro são subestimados. O quadro só funciona se a medição funciona. É por isso que a medição externa (Lessão 21, METR) e a avaliação adversária são necessárias, além da autoavaliação de laboratório.

> Se o modelo estiver em avaliação, a capacidade de cada quadro será subestimada. O quadro só será válido quando a medida for efetiva. É por isso que, além da avaliação do próprio laboratório, a avaliação externa (METR) e a avaliação de resistência são necessárias.

### A habilidade de leitura de políticas

- Localiza: todas as capacidades que lhe interessam devem ser encontradas na apólice.
  Tradução:**定位**A política não abrange todas as capacidades que você tem em conta.
- Classificar: é rastreado (acciona mitigação) ou pesquisa ( rastreado, mas não desencadeando)?
  Tradução:**分类**O que é que é o "Track" ou "Research"?
- Cadência: a política é atualizada em um calendário declarado ou apenas após eventos específicos?
  Tradução:**节奏**A política de declaração é actualizada ou só após um determinado evento?
- Independência: a revisão externa é obrigatória ou opcional? Parceiros antropóficos com a Apollo e o Instituto de Segurança de IA dos EUA; OpenAI com a METR; DeepMind com a SAG interna principalmente.
  Tradução:**独立性**A investigação externa é obrigatória ou opcional?Antropic e Apollo e American AI Security Institute cooperation;OpenAI e METR 合作;DeepMind principal e SAG interno:

## Use-o com o framework implementado.
```figure
a5-tracked-vs-research
```

## Usá-lo

`code/main.py`A tecnologia de informação é uma ferramenta de análise de dados que permite a análise de dados e de dados, que permite a análise de dados e de dados, e que permite a análise de dados e de dados.

> `code/main.py` a realização de uma pequena diferença de desempenho de decisão.  a determinação de uma capacidade:  autonomia  fraude para a organização  desenvolvimento de automação  reforço de rede, etc.  a elaboração de três políticas, respectivamente, sobre como classificá-las e quais as medidas de alívio que podem ser implementadas  a elaboração de três políticas.

## Envia-o . Produto .

`outputs/skill-cross-policy-diff.md`produz uma comparação entre políticas para uma capacidade específica, utilizando os três quadros como referência.

> `outputs/skill-cross-policy-diff.md`Para a definição de capacidade de gerar políticas, utilizar três quadros como referência.

## Exercícios.

1. Corra .`code/main.py`. Confirmar que a saída da ferramenta de diferença corresponde às políticas para pelo menos duas capacidades que você pode verificar com os documentos de origem.
   Tradução: 运行`code/main.py` Identificação de diferenças de ferramentas de saída correspondem a pelo menos duas capacidades de verificação de documentos de origem disponíveis.

2. Leia o OpenAI Preparedness Framework v2 em sua totalidade. Identifique cada categoria de pesquisa. Para cada uma, escreva uma frase sobre por que está em Pesquisa em vez de Tracked.
   中文翻译:完整阅读 OpenAI Preparedness Framework v2──识别每个研究类别──为每个写一句话说明为何在研究而非追踪──

3. Leia o DeepMind FSF v3 completo, além da atualização de Níveis de Capacidade de Aprilo de 2026. Identifique os critérios de avaliação específicos do nível 1 da autonomia de P&D do ML. Como você o mediria externamente?
   中文翻译:完整阅读 DeepMind FSF v3 加 2026 年 4 月 Capacidade de rastreamento Níveis 更新──识别机器学习研发自主等级 1 的具体评估标准──你会如何外部测量?

4. Sandbagging está na OpenAI's Research Categories. Desenhar uma avaliação que forçaria um modelo de sandbagging a revelar sua capacidade real.
   No entanto, o estudo foi concluído em uma análise de dados que mostrou que o desenvolvimento de um sistema de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados

5. Compare as três políticas em uma capacidade específica (a sua escolha). Nomear qual das políticas de classificação que você acha mais rigorosa e qual menos. Justificar com o texto fonte.
   Chinese Language Translation: Comparar três políticas em específico capacidades (你选) 类别.

## Termos-chave .

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| Preparedness Framework | "OpenAI's scaling policy" | PF v2 (April 2025); Tracked vs Research categories | OpenAI 准备度框架：PF v2，Tracked vs Research |
| Tracked Category | "Mandatory mitigation" | Triggers Capabilities + Safeguards Reports; SAG review | 跟踪类别：触发能力+防护报告，SAG 审查 |
| Research Category | "Monitored only" | Tracked but no automatic mitigation; includes Long-range Autonomy | 研究类别：跟踪但不自动缓解，含长程自主 |
| Frontier Safety Framework | "DeepMind's scaling policy" | FSF v3 (Sept 2025) + Tracked Capability Levels (Apr 2026) | DeepMind 前沿安全框架 |
| CCL | "Critical Capability Level" | DeepMind threshold per domain (Cyber, Bio, ML R&D, CBRN) | 关键能力等级：DeepMind 各领域阈值 |
| ML R&D autonomy level 1 | "R&D automation" | Fully automate AI R&D pipeline at competitive cost | 机器学习研发自主等级 1：完全自动化研发管道 |
| Sandbagging | "Strategic underperformance" | Model underperforms on evals; in OpenAI Research Categories | Sandbagging：模型战略性表现不佳 |
| Instrumental reasoning | "Means-ends reasoning" | Reasoning about how to achieve goals; target of DeepMind monitoring | 工具性推理：DeepMind 监控目标 |

## Mais leitura 延伸阅读

- [OpenAI — Updating our Preparedness Framework](https://openai.com/index/updating-our-preparedness-framework/)Anúncio v2.
  Tradução do português:
- [OpenAI — Preparedness Framework v2 PDF](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf) Documento completo.
  Tradução do português:
- [DeepMind — Strengthening our Frontier Safety Framework](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) Anúncio da FSF v3.
  Tradução do português:FSF v3 公告
- [DeepMind — Updating the Frontier Safety Framework (April 2026)](https://deepmind.google/blog/updating-the-frontier-safety-framework/) Adição de Níveis de Capacidade de rastreamento.
  中文翻译:Niveis de Capacidade rastreados 添加
- [Gemini 3 Pro FSF Report](https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_fsf_report.pdf) exemplo de relatório de risco em formato FSF.
  Tradução do inglês para inglês:
