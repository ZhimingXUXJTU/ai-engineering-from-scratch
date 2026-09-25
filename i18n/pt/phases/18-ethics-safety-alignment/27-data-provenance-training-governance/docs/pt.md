# Data Provenance e Training-Data Governance.

> A Lei da UE sobre IA exige que as normas de exclusão de GPAI sejam legíveis por máquina até agosto de 2025 (via a exceção TDM da Diretiva da UE sobre Direitos de Autor). California AB 2013 (assinado 2024)  Transparência de dados de treinamento de IA gerativa exige que os desenvolvedores publiquem um resumo de conjuntos de dados com 12 campos obrigatórios. 2025 Alinhamento da DPA com base em interesse legítimo: DPC irlandês (21 de maio de 2025) aceita a formação de META em LLM sobre conteúdo público público de adultos da UE/EEE com garantias após a opinião do EDPB; Tribunal Regional Superior de Colônia (23 de maio de 2025) rejeita a injunção; DPA de Hamburgo diminui a urgência; ICO do Reino Unido (23 de setembro de 2025) emite uma resposta regulatória positiva às garantias de formação de IA do LinkedIn (transparência, opção simplificada, janelas de objeção estendidas) e continua a monitorar  não uma autorização formal. A ANPD brasileira (2 de julho de 2024) suspendeu o processamento da Meta por causa da insuficiente transparência da informação; a medida preventiva foi levantada em 30 de agosto de 2024 depois que a Meta apresentou um plano de conformidade. Problema de irreversão: os frameworks de consentimento de cookies são projetados para rastreamento reversível em tempo real; uma vez que os dados estão em pesos de modelo, a exclusão cirúrgica é impossível  nenhum direito prático de exclusão do GDPR para redes neurais treinadas. A janela de conformidade está na hora da recolha. Data Provenance Initiative (dataprovenance.org, Longpre, Mahari, Lee et al., "Consent in Crisis", julho 2024): auditoria em larga escala mostra um rápido declínio dos dados comuns da IA à medida que os editores adicionam restrições a robots.txt.

> **【中文解读】**Esta secção apresenta a origem e a gestão de treinamento de dados  garantir a legalidade e a traçabilidade dos dados de treinamento de IA  CALIFORNIA AB 2013  Requisitos gerados por desenvolvedores de IA  Publicar contém 12  Segmentos essenciais de dados  Resumo  EU AI Act  Requer que o GPAI realize o Reto de Registo de Máquinas de Leitura                                                                                                                                                                                                               

> **【拓展：合法利益趋同 → 2025 DPA 立场】**Em 2025, várias agências de proteção de dados em posição de interesse legal tendência: DPC irlandesa (DPC) 21 de maio de 2025) em Meta em primeira pessoa aberta UE/EEE Plano de treinamento de adultos em conteúdo LLM (LLC) (BAT) (BAT); Cologne High等地区法院驳回禁令; UK ICO (COL); 23 de setembro de 2025) em LinkedIn (Restore AI) 训练发发发积极监管应应――趋同原则: legitim interest can prove the reasonability of training on first person content available in public, no need for consent.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, 12-field California AB 2013 scaffolding generator) | **语言:** Python（标准库，12 字段 California AB 2013 脚手架生成器）
**Prerequisites:** Phase 18 · 24 (regulatory), Phase 18 · 26 (cards) | **前置知识:** Phase 18 · 24 (监管), Phase 18 · 26 (卡片)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**學本節前 請先掌握:Fase 18·24-26── DataTraceability + 訓練管理AI 訓練資料的合法性和可追溯性──
> - Não .**【类比】**O número de dados que são obtidos em um determinado número de dados é de um número de dados que são obtidos em um determinado número de dados.
> ️ Iniciativa de Provença de Dados 2024.7: AI 数据共享生态快速衰退,出版方加 robots.txt 限制──

## Objetivos de aprendizagem

- Descreva os 12 campos obrigatórios da California AB 2013 para a transparência de dados no treinamento de IA Gerativa.
- Estabelecer a posição do DPA sobre a formação de LLM de interesse legítimo em 2025 (DPC irlandês, ICO do Reino Unido, Hamburgo, Colônia).
- Descreva o problema da irreversão: por que o direito de exclusão do RGPD não tem equivalente prático para redes neurais treinadas.
- Estabelecer a conclusão "Consentimento em crise" da Iniciativa de Provença de Dados.

> 描述 California AB 2013 的 12 个必填字段──说明 2025 年 DPA 关于合法利益 LLM 训练的立场──描述不可逆性问题:为什么GDPR被遗忘权对训练神经网络没有实际等价──说明数据来源倡议的"Consent in Crisis"发现──

## O problema é o problema .

A governação de dados de formação é o montante de cada cartão modelo (Lessão 26) e obrigação regulatória (Lessão 24). Em 2024-2025, o cenário regulatório consolidado em três princípios: infraestrutura de exclusão, divulgação por conjunto de dados e adaptações de interesse legítimo para dados disponíveis ao público. Os provedores que não cumprem no momento da coleta não podem remediar o montante.

> O treinamento de gestão de dados é o primeiro passo de cada modelo de caráter e obrigação de supervisão. O cenário de supervisão de 2024-2025 é consolidado em três princípios: retirada da infraestrutura, divulgação de cada conjunto de dados e disposição legítima de interesses dos dados disponíveis ao público.

## O conceito .

> **【中文解读】**12 个必填字段:数据集来源/所有者;数据集如何促进 AI 系统预期目的;数据点数量;数据点类型描述;数据集是否包含受版权/商标/专利保护的数据;数据集是否包含个人信息;数据集是否包含聚消费者信息;清洁/处理/修改说明;数据集时间段; data collection date·是否第一次使用日期;数据集数据生成;第12 项合成数据) em relação a fevereiro de 2018, a lista de dados é nova.

### California AB 2013

A documentação deve ser publicada em ou antes de 1 de janeiro de 2026 para sistemas lançados em ou após 1 de janeiro de 2022. A Seção 3111 (a) exige que os desenvolvedores publiquem um resumo de alto nível dos conjuntos de dados utilizados na formação com 12 itens legais:
1. Fontes ou proprietários dos conjuntos de dados.
2. Descrição de como os conjuntos de dados promovem o propósito pretendido do sistema de IA.
3. Número de pontos de dados nos conjuntos de dados (intervalo geral aceitável; estimativas para conjuntos de dados dinâmicos).
4. Descrição dos tipos de pontos de dados (tipos de rótulos para conjuntos de dados rotulados; características gerais para os não rotulados).
5. Se os conjuntos de dados incluem quaisquer dados protegidos por direitos autorais, marcas ou patentes, ou se estão inteiramente no domínio público.
6. Se os conjuntos de dados foram adquiridos ou licenciados.
7. Se os conjuntos de dados incluem informações pessoais (de acordo com o código civil de Cal. §1798.140 ((v)).
8. Se os conjuntos de dados incluem informações agregadas dos consumidores (de acordo com o código civil de Cal. §1798.140 ((b)).
9. Limpeza, transformação ou outra modificação por parte do desenvolvedor, com o propósito previsto.
10. Período de tempo durante o qual os dados foram recolhidos, com aviso se a recolha estiver em curso.
11. Data em que os conjuntos de dados foram utilizados pela primeira vez durante o desenvolvimento.
12. Se o sistema utiliza ou utiliza continuamente a geração de dados sintéticos.

O item 12 (dados sintéticos) é novo em relação às fichas de dados de Gebru et al. 2018. O item 7 (informações pessoais) desencadeia obrigações da Lei de Direitos à Privacidade (CPRA). O estatuto isenta segurança/integritade, operação de aeronaves e sistemas de segurança nacional apenas federais (Seção 3111(b)).

### Lei da UE sobre IA (Lessão 24) e exclusão do TDM

A excepção à Directiva da UE sobre direitos de autor para a extração de textos e dados permite a formação sobre conteúdos disponíveis ao público, a menos que o titular dos direitos opte por não participar.

### 2025 Convergência do DPA em relação a interesses legítimos

O artigo 1.o, n.o 1, alínea a), do Regulamento (UE) n.o 1095/2013 do Parlamento Europeu e do Conselho, de 15 de dezembro de 2012, estabelece um regime de controlo da segurança pública e de segurança pública. O Tribunal Regional Superior de Colónia (23 de Maio de 2025) rejeita a injunção contra a Meta: a exclusão é suficiente. O DPA de Hamburgo elimina o procedimento de urgência para a coerência a nível da UE. O ICO do Reino Unido (23 de setembro de 2025) emitiu uma resposta regulatória positiva  não uma autorização formal  à retomada da formação de IA do LinkedIn com salvaguardas semelhantes e monitoramento contínuo.

Princípio convergente: o interesse legítimo pode justificar a formação sobre conteúdos de primeira parte disponíveis ao público com exclusão.

### ANPD brasileiro (junho de 2024)

Suspendeu o tratamento dos dados dos utilizadores brasileiros pela Meta para formação em IA por causa da insuficiente transparência da informação.

> **【中文解读】**Infelizmente, o sistema de controle de dados é um sistema de controle de dados que permite a análise de dados e de dados.

### O problema da irreversão

O consentimento de cookies foi projetado para rastreamento reversível em tempo real. Os dados de treinamento são diferentes: uma vez que os dados entram em pesos de modelo, a exclusão cirúrgica não é possível.

Remédios parciais:
- **Unlearning.**Removação aproximada, medida por MIA (Lessão 22).
- **Influence function-based localization.**Identificar os pesos mais influenciados pelos dados; atualizar seletivamente.
- **Fine-tune-suppression.**Treinar o modelo a recusar as saídas derivadas dos dados.

A janela de conformidade está na hora da recolha.

> **【拓展：数据来源倡议 → AI 公地萎缩】**A Data Provenance Initiative (www.dataprovenance.org) de "Consent in Crisis" (Consenso em Crise) (Julho de 2024) descobriu que os editores estão acelerando a adição de robots.txt 限制── open training DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公地 DATA公          

### Iniciativa de Provença de Dados

Dataprovenance.org. Longpre, Mahari, Lee e outros. "Consenso em Crise" (Julho 2024): auditoria em larga escala de dados comuns de treinamento de IA. Descobrir: os editores estão a adicionar restrições de robots.txt a uma taxa acelerada. O comércio aberto está a contrair-se rapidamente. 2023 -> 2024 viu cerca de 25% das principais fontes de formação adicionar alguma restrição. Implicação: a futura disponibilidade de dados de formação depende de novos paradigmas de aquisição (licenciamento, geração sintética, participação incentivada).

### Onde isto encaixa na Fase 18

A lição 26 é documentação a nível de modelo. A lição 27 é governança a nível de conjunto de dados. Juntos definem a camada de transparência. A lição 28 mapeia o ecossistema de pesquisa que trabalha nessas questões.

> Lição 26 é modelo de classe de documentos. Lição 27 é dados conjunto de classe de gestão. Eles definem em conjunto a transparência de nível. Lição 28 é mapear estes problemas.

> **【拓展：巴西 ANPD → 不同监管结果】**ANPD brasileiro (Junho de 2024) suspendeu a Meta devido à falta de transparência da informação  Treinamento de tratamento de IA de dados de usuários brasileiros  Diferente dos resultados do DPA da UE  AnPD  Prioridade para a transparência e não para o interesse ilegal  Permissão de prevenção  Prevenção para a eliminação de medidas após a apresentação do Plano de Conformidade do Meta  Agosto de 2024  Isto mostra que diferentes jurisdições podem chegar a conclusões claramente diferentes sobre a mesma prática tecnológica 

## Usa-o. Usa-o.
```figure
an-provenance-oneway
```

## Usá-lo

`code/main.py`gerar um esquadrão de resumo de um conjunto de dados de 12 campos, em conformidade com a California AB 2013. Você pode preencher os campos e observar quais desencadeiam obrigações de privacidade ou de seguimento de direitos autorais.

> `code/main.py`Para brinquedos, o conjunto de dados gerado em conformidade com o California AB 2013 12 字段数据集摘要脚手架── você pode preencher um parágrafo e observar quais são os seguintes requisitos de privacidade ou direitos autorais──

## Envia-o .

Esta lição produz`outputs/skill-provenance-check.md`. Tendo em conta um conjunto de dados utilizado na formação, verifica a cobertura de 12 campos do AB 2013, a conformidade com a infraestrutura de exclusão, o alinhamento do DPA e a avaliação do risco de irreversão.

> 本课产 出 `outputs/skill-provenance-check.md` Dataset of data used in determin training, inspection AB 2013 12 字段覆盖、退出基础设施合规、DPA 对齐和不可逆性风险评估──

## Exercícios.

1. Corra .`code/main.py`- Reproduzir um resumo de 12 campos para um conjunto de dados de brinquedos e identificar quais campos são subespecificados.

2. A Diretiva TDM da UE sobre direitos autorais é legível por máquina. Propõe um formato padrão para o sinal de exclusão e compare-o com robots.txt e C2PA "Sem treinamento em IA".

3. Leia o "Consentimento em Crise" da Iniciativa de Provença de Dados (julho de 2024). Descreva as três categorias de conteúdo que restringem mais rapidamente e argumenta uma consequência econômica.

4. A alinhamento do DPA de 2025 aceita um interesse legítimo em formação de conteúdo público.Construir um cenário em que um interesse legítimo não seria suficiente e identificar a base jurídica necessária para um prestador.

5. Esboçar um manifesto de origem de dados de formação que compreenda os campos AB 2013 e uma cadeia de origem assinada pela C2PA para cada conjunto de dados. Identificar uma barreira técnica e uma barreira legal.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| AB 2013 | "the California law" | Generative AI training-data transparency; 12 mandated fields |
| TDM exception | "text-and-data-mining" | EU Copyright Directive training-data exception with opt-out |
| Legitimate interest | "the EU basis" | GDPR Article 6 basis that may justify training on public content |
| Opt-out signal | "machine-readable no-train" | robots.txt, C2PA "No AI Training," TDM.Reservation |
| Irreversibility | "cannot un-train" | Data in model weights is not surgically removable |
| Unlearning | "approximate removal" | Post-training interventions to reduce model dependence on specific data |
| Consent in Crisis | "the DPI audit" | July 2024 finding of accelerating robots.txt restrictions |

## Mais leitura 延伸阅读

- [California AB 2013](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB2013) Lei de transparência dos dados sobre formação de IA
- [EU AI Act + GPAI Code of Practice (Lesson 24)](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) Capítulo do direito de autor
- [Longpre, Mahari, Lee et al. — Consent in Crisis (dataprovenance.org, July 2024)](https://www.dataprovenance.org/consent-in-crisis-paper) Auditoria do IPD
- [IAPP — EU Digital Omnibus GDPR amendments (2025)](https://iapp.org/news/a/eu-digital-omnibus-amendments-to-gdpr-to-facilitate-ai-training-miss-the-mark) contexto regulamentar
