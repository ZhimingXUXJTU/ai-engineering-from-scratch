# CAIS, CAISI e Risco em escala social

> O Centro de Segurança de IA (CAIS, San Francisco, fundado em 2022 por Hendrycks e Zhang) publica o quadro de quatro riscos  uso malicioso, corridas de IA, riscos organizacionais, IAs desonestas  e a declaração de maio de 2023 sobre risco de extinção assinada por centenas de professores e líderes de empresas. 2026 lançamentos do CAIS: AI Dashboard para avaliação de modelo de fronteira, Índice de Trabalho Remoto (com AI de escala), Superintelligence Strategy Paper, AI Frontiers newsletter. Uma entidade distinta: Centro de NIST para Padrões e Inovações de IA (CAISI)  acordos voluntários dirigidos ao governo dos EUA e avaliações de capacidade não classificadas focadas em riscos de ciber, bio e armas químicas. O CAIS define o risco organizacional como um dos quatro riscos de nível superior: cultura da segurança, auditorias rigorosas, defesas de várias camadas e segurança da informação são fundamentais, mas rotineiramente negociados contra a velocidade de implantação. O SB-53 da Califórnia, se assinado, seria a primeira regulamentação de risco catastrófico a nível estadual dos EUA.

> **【中文解读】**Este capítulo apresenta a avaliação de riscos sociais do CAIS/CAISI AI 系统对社会潜在影响和风险分析


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-risk inventory and mitigation matcher) | **语言:** Python（标准库，四风险盘点与缓解匹配器）
**Prerequisites:** Phase 15 · 19 (RSP), Phase 15 · 20 (PF + FSF) | **前置知识:** Phase 15 · 19（RSP）、Phase 15 · 20（PF + FSF）
**Time:** ~45 minutes | **时间:** ~45 分钟

> - Não .**【前置】**O estudo foi realizado em um estudo de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa em pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa em pesquisa em pesquisa em pes
> - Não .**【类比】**CAIS = "AI 风险的智囊团" (民间研究,发言声明、推框架); CAISI = "AI 风险的政府办公室" (NIST 下属, coordão voluntário) (Brasil: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês: CAIS) (do inglês:
> 🤔 **【困惑】**Q: Estas organizações têm que fazer com engenharia de IA? Uso direto é conforme à regulamentação: se o seu produto envolver cenários de risco elevado (medicina, finanças, recrutamento), precisa consultar o CAIS framework para fazer uma avaliação de risco, pode precisar de cumprir a Lei da UE sobre IA, o SB-53 e outras regulamentações.

## O problema é o problema da introdução

As lições 19 e 20 cobriram políticas de escalação interna do laboratório. A lição 21 cobriu a avaliação independente de capacidade. Esta lição abrange a terceira perspectiva: a sociedade civil e as organizações governamentais que moldam a discussão pública e a linha de base regulatória para o risco de IA catastrófica.

> Os artigos 19 e 20 abrangem a política de expansão interna do laboratório. Os artigos 21 e 21 abrangem a avaliação de capacidade independente. Os artigos 21 e 21 abrangem o terceiro ponto de vista: formação de discussões públicas e de organizações governamentais e sociais.

CAIS é uma organização de pesquisa sem fins lucrativos que publica quadros para pensar sobre risco de IA e coordena declarações públicas. CAISI é um centro do governo dos EUA dentro do NIST que executa acordos voluntários com laboratórios e avaliações de capacidade não classificadas. Os nomes rimam; as missões não se sobrepõem. Um praticante deve saber ambos.

> 两个不同的实体很重要――CAIS é uma organização de investigação sem fins lucrativos que publica AI 风险思考框架并协调公开声明――CAISI é um centro do governo dos EUA no NIST, com laboratório de operação voluntário acordo e avaliação de capacidade não-secretária――名字押; tarefas não se sobrepõem―― os profissionais devem saber ambos――

O conteúdo prático: o quadro de quatro riscos do CAIS é a taxonomia de risco em escala social mais citada na literatura. A cultura de segurança e o risco organizacional são uma dessas quatro, e esta é a mais diretamente sob o controlo de um profissional. SB-53 (Califórnia) seria a primeira regulamentação de risco de catástrofe a nível estadual dos EUA se assinada; a estrutura da lei é importante porque a regulamentação a nível estadual historicamente levou a ação federal na política tecnológica dos EUA.

>  Praticado conteúdo:O quadro de quatro riscos do CAIS é o mais amplamente citado na literatura. O risco de escala social e organizacional é um dos mais diretamente controlados pelos profissionais.

## O conceito central.

### CAIS  Centro de Segurança da IA

- Fundada: 2022 em San Francisco, por Dan Hendrycks e colegas (o nome "Zhang" refere-se a um colaborador inicial, não um cofundador atual; veja o site do CAIS para a liderança atual).
  Chinese Translation:成立:2022年在旧金山,由 Dan Hendrycks 和同事创立("Zhang"指早期合作者,非当前联合创始人;当前领导见 CAIS 网站) 
- Estatuto: 501 ((c) ((3) organização sem fins lucrativos.
  No entanto, o que não é um problema é que o seu nome é "Cidade de Deus".
- Output notável de 2023: declaração sobre o risco de extinção, co-assinada por centenas de pesquisadores e CEOs. Estabeleceu: "A mitigação do risco de extinção da IA deve ser uma prioridade global ao lado de outros riscos em escala social, como pandemias e guerra nuclear".
  Chinese Translation:2023 显著产出:灭绝风险声明,数百研究员和CEO 联合签署――声明:"Reduzir o risco de extinção da IA em relação a outras doenças sociais, como a epidemia e a guerra nuclear, como uma prioridade global".""
- Resultados de 2026: Painel de análise de IA para avaliação de modelos de fronteira, Índice de Trabalho Remoto (junto com AI de escala), Papel de Estratégia de Superinteligência, boletim informativo da AI Frontiers.
  中文翻译:2026 产出:前沿模型评估 AI Dashboard、Remote Labor Index(vec Scale AI 联合)、Superintelligence Strategy Paper、AI Frontiers 简报。

### O quadro dos quatro riscos

Os quadros do CAIS agrupam o risco catastrófico da IA em quatro categorias de nível superior:

> O quadro do CAIS vai dividir a IA 风险 de catástrofes em quatro categorias principais:

1. **Malicious use**: um ator mau usa a IA para causar danos (sinteze de armas biológicas, desinformação, ciberataques).
   Tradução:**恶意使用**O que é que é o "Brasil" ?
2. **AI races**A pressão competitiva entre laboratórios, empresas ou nações empurra a implantação para além do ponto em que é segura.
   Tradução:**AI 竞赛**A pressão de concorrência entre empresas e países favorece a implementação de pontos de segurança.
3. **Organizational risks**A evolução da tecnologia de informação e de informação é uma das principais consequências da utilização de tecnologias de informação.
   Tradução:**组织风险**A Comissão Europeia (UE) adoptou um relatório sobre a situação dos laboratórios de investigação e de investigação.
4. **Rogue AIs**A IA é suficientemente capaz de perseguir objetivos que estão em conflito com o bem-estar humano.
   Tradução:**失控 AI**A inteligência artificial (AI) é capaz de alcançar os objetivos de conflito com o bem-estar humano.

Esta não é a única taxonomia; é a mais citada. As categorias não são mutuamente exclutivas  uma IA desonesta produzida por uma organização que negociou auditoria de velocidade em uma corrida é todas as quatro.

> Esta não é a única classificação; é a mais frequentemente citada.

### Onde o risco organizacional vive

Das quatro categorias, o risco organizacional é o mais accionavel para os profissionais. A cultura de segurança de um laboratório, o rigor de auditoria, a camada de defesa e a segurança da informação decidem se seus modelos de navios com os controles das lições 1018 estão realmente em vigor, ou se esses controles são itens da lista de verificação que ninguém verificou.

> Entre as quatro categorias, o risco organizacional é o mais operacional para os profissionais. A cultura de segurança laboratorial, a rigor de auditoria, a divisão de defesa e a segurança da informação determinam se o seu modelo é com o controle de classe 1018 em prática lançado, ou se esses controles são listados sem verificação humana.

As alavancas concretas de risco organizacional:

> 具体组织风险杆:

- **Safety culture**A Comissão considera que a Comissão deve ter em conta as necessidades do mercado interno e, em particular, a necessidade de uma avaliação adequada da situação dos trabalhadores.
  Tradução:**安全文化**A CAIS descobriu que este é um forte fator de previsão de outras taxas.
- **Rigorous audits**As auditorias internas produzem relatórios otimistas.
  Tradução:**严格审计**O auditório interno produz um relatório positivo.
- **Multi-layered defenses**: não é suficiente uma única camada (tema de execução da Fase 15).
  Tradução:**多层防御**Não há um nível suficiente.
- **Information security**A classificação de dados de avaliação, a classificação de dados de avaliação, a classificação de dados de avaliação, a classificação de dados de avaliação, a classificação de dados de avaliação, a classificação de dados de avaliação e a classificação de dados de avaliação, a classificação de dados de avaliação e de dados de avaliação, a classificação de dados de avaliação e de dados de avaliação, a classificação de dados de avaliação e de dados de avaliação, a classificação de dados de dados de avaliação e de dados de avaliação, a classificação de dados de dados de avaliação e de dados de avaliação, a classificação de dados de dados de avaliação e de dados de dados de avaliação, a classificação de dados de dados de avaliação e de dados de dados de dados de dados, a classificação de dados de dados de dados de dados, a classificação de dados de dados de dados e de dados de dados, a classificação de dados de dados de dados, a classificação de dados de dados de dados e de dados de dados de dados, a classificação de dados de dados de dados de dados, a classificação de dados de dados de dados de dados de dados e de dados de dados, a classificação de dados de dados de dados de dados de dados, a classificação de dados de dados de dados de dados de dados de dados, e de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados, e de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de
  Tradução:**信息安全**O modelo de direitos de vazamento, avaliação de vazamentos de dados, controle e prevenção de vazamentos técnicos, RAND SL-4 do capítulo 19, é um padrão específico.

### CAISI  Centro de Normas e Inovações da IA

- Opera dentro do NIST.
  Tradução do inglês:
- Executa acordos voluntários com laboratórios de fronteira.
  Tradução do inglês:
- Publica avaliações de capacidade não classificadas focadas em riscos de ciber, bio e armas químicas.
  Tradução do inglês para o inglês:
- Diferente do CAIS; os acrônimos colidem; verifique a URL (nist.gov) para confirmar qual você está lendo.
  中文翻译:与 CAIS 不同;首字母缩写冲突;检查URL(nist.gov)确认你在读哪个──

O papel da CAISI é o público, contraparte do governo para os trabalhos de laboratório privados da METR (Lessão 21). Os relatórios da CAISI não são classificados; os relatórios da METR são muitas vezes identificados pela NDA.

> O papel do CAISI é o METR Private Person Laboratory cooperation (§ 21 课) do METR Public 面向政府对应物――CAISI 报告非密;METR 报告通常 NDA 门控――读者从业者得到更完整的图景――

### California SB-53

O projeto de lei do Senado da Califórnia (20252026 sessão) aborda o risco catastrófico de modelos de fronteira.

> 加州参议院法案 (→ 2025) (→ 2026)

- Limitações específicas de capacidade que desencadeiam obrigações a nível estatal.
  Tradução do inglês para "Capacidade específica de um Estado"
- Proteção de denunciantes para funcionários do laboratório de IA.
  Chinese Translation:AI 实验室员工举报人保护.
- Requisitos para relatar incidentes em caso de falhas catastróficas.
  Chinese:                                                                                                                                                                                                                                                              

Se assinado, seria a primeira regulamentação de risco catastrófico a nível estadual dos EUA. Independentemente do status da assinatura, a estrutura da lei molda a forma como outras legislaturas estaduais abordam o problema. Os praticantes na Califórnia devem acompanhar o status da lei; os praticantes em outros lugares devem lê-la para entender como a regulamentação a nível estadual dos EUA provavelmente parecerá.

> Se assinado, será o primeiro regulador de riscos de catástrofe a nível estadual dos EUA. Independentemente do estado da assinatura, o quadro do projeto de lei moldará como os outros órgãos legislativos estaduais lidam com os problemas.

### O risco em escala social não é um problema de uma única camada

O tema em curso da Fase 15  defesa em profundidade  aplica-se também à camada social. Nenhuma organização, regulamentação ou quadro único fecha o risco catastrófico. O ecossistema funciona apenas quando:

> O tema de transição do capítulo 15 é a defesa profunda, que também se aplica ao nível social. Não existe uma única organização, lei ou quadro que possa encerrar o risco catastrófico.

- Políticas de escalagem de embarcações de laboratórios (Lessões 19, 20).
  No entanto, o governo não conseguiu manter a sua posição.
- Os avaliadores externos produzem medições (Lessão 21).
  Tradução do inglês para tradução livre:
- A sociedade civil acompanha e divulga (CAIS).
  Tradução do inglês para "Médio de Segurança e Propaganda"
- O Governo administra programas voluntários e regulamentação de base (CAISI, SB-53).
  Tradução do inglês para "Categoria de Execução de Serviços de Segurança e Segurança"
- Os praticantes construem controles de várias camadas (Lessões 1018).
  Tradução do português:从业者构建多层控件 (从业者构建多层控件)

Esta é a síntese final para a fase: cada lição anterior é uma camada numa pilha cuja integridade importa mais do que a força de qualquer camada.

> É o composto final da fase: cada aula anterior é uma camada da coleção, sua integridade é mais importante do que a intensidade de qualquer camada única.

## Use-o com o framework implementado.
```figure
a5-four-risks
```

## Usá-lo

`code/main.py`O sistema de avaliação de risco é um sistema de análise de risco que, em função da implementação proposta, marca a implementação em relação às quatro categorias de risco e retorna uma lista de verificação de mitigação.

> `code/main.py` implementar pequenas estratégias de risco.  Implementar a implementação de propostas, que refaz quatro categorias de risco e torna-se uma lista de medidas de redução.

## Envia-o . Produto .

`outputs/skill-societal-risk-review.md`Revisar uma posição de risco em escala social: qual das quatro categorias é abordada, quais são as medidas de mitigação, qual é a exposição ao risco organizacional.

> `outputs/skill-societal-risk-review.md`审查部署的社会规模风险姿态:触及四类中哪些?

## Exercícios.

1. Corra .`code/main.py`- Introdução de três implantações sintéticas em diferentes escalas.
   Tradução: 运行`code/main.py` Introdução de três unidades de produção de diferentes dimensões.

2. Leia o documento completo do CAIS sobre os quatro riscos, escolha uma categoria de risco e escreva dois parágrafos sobre o que acredita ser o desenvolvimento mais importante para 2026.
   Chinese: Full-read CAIS 四风险论文──select a风险类别, write two paragraphs about you think this category 2026 最重要发展──

3. Leia o projeto atual do SB-53 da Califórnia. Identifique uma disposição que acredite fortalecer a postura de risco catastrófico e uma que acredite enfraquecê-la.
   No entanto, o que não é verdade é que o governo não pode fazer isso.

4. Escolha uma implantação de IA de produção que conheça (a sua ou publicada). Ponha-a em relação aos sub-impulsos de risco organizacional: cultura de segurança, rigor de auditoria, defesas de várias camadas, segurança da informação. Qual é o mais fraco?
   Chinese Language Translation: Choose one you know of production AI deployment (): "Securidade cultural", "Audit rigoridade", "Multi-camada de defesa", "Segurança da informação", "Qual é o mais fraco?"

5. Esboçar uma versão 2028 do quadro de quatro riscos que reflita um ano de capacidade adicional e um ano de experiência adicional de implantação. O que você adicionaria, removeria ou reagruparia?
   O desenho reflete o quadro de quatro riscos de experiência de um ano de capacidade extra e um ano de experiência externa.

## Termos-chave .

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| CAIS | "Center for AI Safety" | Non-profit; four-risk framework; 2023 extinction statement | CAIS：非营利，四风险框架 |
| CAISI | "US government AI safety" | NIST Center; voluntary agreements; unclassified evals | CAISI：NIST 中心，自愿协议 |
| Four-risk framework | "CAIS's taxonomy" | malicious use, AI races, organizational risks, rogue AIs | 四风险框架：恶意使用/AI 竞赛/组织风险/失控 AI |
| Malicious use | "Bad actor uses AI" | Bioweapons, disinformation, cyberattacks | 恶意使用：生物武器、虚假信息、网络攻击 |
| AI races | "Competitive pressure" | Labs/companies/nations push deployment past safety | AI 竞赛：竞争压力推动部署越过安全 |
| Organizational risk | "Lab internal failure" | Safety culture, audit, defenses, infosec | 组织风险：安全文化、审计、防御、信息安全 |
| Rogue AI | "Misaligned agent" | Capable AI pursuing goals conflicting with human welfare | 失控 AI：追求冲突目标的强大 AI |
| California SB-53 | "State-level regulation" | 2025–2026 bill; first US state catastrophic-risk regulation if signed | 加州 SB-53：州级灾难性风险监管法案 |

## Mais leitura 延伸阅读

- [Center for AI Safety](https://safe.ai/) a instituição de acolhimento do quadro dos quatro riscos.
  Tradução do inglês para "Four Financial Institutions"
- [CAIS — AI Risks that Could Lead to Catastrophe](https://safe.ai/ai-risk) o papel de quatro riscos.
  Tradução do português:
- [CAIS — May 2023 statement on extinction risk](https://safe.ai/statement-on-ai-risk) breve declaração comum.
  Tradução do inglês:
- [NIST CAISI](https://www.nist.gov/caisi) Centro de inovação e padrões de IA dirigidos ao governo.
  Tradução do inglês para Chinês: Fação em direção ao governo
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) liga os compromissos de laboratório à estruturação em escala social.
  Chinese Translation: ligação a compromisso de nível laboratório com a estrutura de escala social
