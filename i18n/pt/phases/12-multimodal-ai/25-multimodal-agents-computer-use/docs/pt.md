# Agentes multimodal e uso de computador (Capstone) 

> O produto 2026 frontier é um agente multimodal que lê capturas de tela, clique em botões, navega por interfaces web, preenche formulários e completa fluxos de trabalho de ponta a ponta. SeeClick e CogAgent (2024) provaram a primitiva de grounding de GUI. A interface de ferret adicionou móveis. O ChartAgent introduziu o uso de ferramentas visuais para gráficos. VisualWebArena e AgentVista (2026) são os referências que as perseguições de fronteira  e até mesmo Gemini 3 Pro e Claude Opus 4.7 pontuação ~30% nas tarefas difíceis de AgentVista. Esta pedra final reúne todos os fios da Fase 12: percepção (VLM de alta resolução), raciocínio (LLM com uso de ferramentas), aterramento (saída de coordenadas), memória de longo horizonte e avaliação.

> **【中文解读】**O produto da linha de frente de 2026 é capaz de ler gráficos, pontos de pressão, navegação, páginas web, preenchimento de formulários, de fim a fim de completar o fluxo de trabalho. AgenteSeeClick e CogAgent provaram a GUI  localização original disponível, Ferret-UI  expansão para o terminal móvel, ChartAgent  introdução de ferramentas visuais de uso. Mas em AgentVista  difícil tarefas, mesmo Gemini 3 Pro e Claude Opus 4.7 também cerca de 30% de taxa de aprovação.

**Type:** Capstone
**Languages:** Python (stdlib, action schema + agent loop skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 12 · 09 (Qwen-VL JSON), Phase 14 (Agent Engineering)
**Time:** ~240 minutes

> - Não .**【前置】**學本節前請先掌握:Fase 12 全部(VLM 演进) 、Fase 14·01-10(Agente 循环、工具调用) 、Fase 14·30+(工作台系列 Agent 实践) ⋅本节是Fase 12 的毕业课所有多模态 + Agent 技术整合成一个能操作电脑的产品──
> - Não .**【类比】**多模态 Agente = "AI 实习生"──看截图(感知) + 想"下一步该点哪里"(推理) + 输出点击点击坐标(行动) + 看新页面(观察) + 循环──普通 VLM = 看图说话(描述);Agenta VLM = 看图做事(执行动作)──困难在于:坐标精度(点错按) 长程规划(10步订票流程) 错误恢复(弹窗、广告、登录页)。
> ️ **【易错点】**让 Agent 直接执行动作不设人工审核 = 灾难(可能误转账、错删除) 修复:所有"破坏性动作" (→ "Bai-ba) 点击提交、确认、删除按) 必须人类审核或干-run 模式。A filosofia de design do uso de computadores antropicos é "proposta→人类批准→执行",对应 模式,15·15 fase proposta-then-commit 模式。

## Objetivos de aprendizagem

- Desenhar um ciclo de agentes multimodal: perceber → razão → agir → observar → repetir.
  设计多模态 Agente 循环:感知 → 推理 → 行动 → 观察 → 重复。
- Construir um esquema de saída de aterragem da GUI (coordenadas de clique, texto de tipo, rolamento, arrastar) o VLM pode emitir como JSON.
  构建 GUI 定位输出模式(点击坐标、输入文字、滚动、拖),VLM 以 JSON 格式输出──
- Compare agentes apenas para captura de tela versus agentes de árvore de acessibilidade versus agentes híbridos.
  Comparado com o Agente de Criação Pura, Agente sem Obstáculos e Agente Misto.
- Configurar uma avaliação de referência de agente multimodal em uma pequena faixa do VisualWebArena.
  Em VisualWebArena, um pequeno grupo de projetos foi criado para criar um agente de avaliação baseada em vários modelos.

## O problema é definido .

> **【中文解读】**Em um cenário de compra, por exemplo: Agente  precisa de cortar a página do navegador, resolver cortar o URL + plano de geração de objetivos, fazer uma operação estruturada, então o mecanismo de recuperação é essencial.

Um fluxo de trabalho no local de reserva: "Encontre-me um voo para Tóquio para 15 de abril, assento no corredor de menos de $800, reserva-o".

> Um pedido de trabalho: "Ajudá-me a encontrar o voo de 4 月 15 日飞东京,靠走道, $800 以下,预订──"

Um agente multimodal precisa:

> 多模态 Agente 需要:

1. Tome uma captura de tela do navegador.
   Tradução do inglês:截取浏览器屏幕截图──
2. Partilhe a captura de tela + URL + objetivo em um plano.
   中文翻译:解析截图 + URL + 目标,生成计划。
3. Emite uma ação estruturada: clique (em x,y), digite "Tokio" (em elemento E), deslize para baixo, selecione (botão de rádio).
   Tradução do inglês para japonês:                                                                                                                                                                                                                                                           
4. Aplicar a ação no navegador.
   Tradução do inglês:
5. Observe o novo estado (próximo captura de tela).
   No entanto, o que não é verdade é que o que não é verdade.
6. Repita até que a tarefa seja concluída.
   Tradução do inglês:重复直到任务完成──

Cada passo é uma chamada VLM multimodal. A saída VLM deve ser JSON parseável. Os erros compõem-se em todas as etapas, então a recuperação importa.

> Cada passo é uma vez de vários modos VLM 调用──VLM 输出必须是可解析的 JSON──错误在步骤间积累, portanto, o mecanismo de recuperação é essencial──

## O conceito central.

> **【中文解读】**A AI pode ser usada como um agente de uso de computador.

> **【拓展：Computer Use 的前沿**Utilização de computador antropico 让 Claude 直接操作桌面应用,完成网页浏览、表单填写等任务──OpenAI Operator 使用类似方法──关键技术挑战:精确定位──准确点击按) 状态跟踪──理解界面变化──误恢复──操作失败后重试──


### GUI de terra  o primitivo  GUI 定位 基础原语

A aterragem da interface gráfica é: dada uma captura de tela e uma instrução de linguagem natural, saia a coordenada (x, y) para clicar (ou outra ação).

> GUI 定位是:给定一张截图和自然语言指令,输出需要点击的 (x, y) 坐标(或其他动作)

> **【中文解读】**GUI 定位是:给定一张截图和自然语言指令,输出需要点击的 (x, y) 坐标(或其他动作) ――SeeClick é o primeiro grande resultado aberto, CogAgent 增加了1120x1120高分辨率编码,Ferret-UI 聚焦移动端 UI──输出格式通常是JSON,`element_desc`字段帮助恢复当坐标在截图间漂移时,语义提示让系统重新定位──

SeeClick (arXiv:2401.10935) foi o primeiro resultado aberto em escala: ajuste fino de um VLM em dados sintéticos + GUI real, coordenadas de saída como tokens de texto simples.

> SeeClick é o primeiro grande resultado aberto: em sintetizado + real GUI dados sobre o VLM, em puro texto token 输出坐标──有效──

CogAgent (arXiv:2312.08914) adicionou 1120x1120 codificação de alta resolução para interfaces de uso densas.

> CogAgent para a interface intensiva adicionou 1120x1120 código de alta resolução.

Ferret-UI (arXiv:2404.05719) concentra-se em UI móveis, integra-se com dados de acessibilidade iOS.

> Ferret-UI 聚焦移动端 UI, integrado iOS 无障碍数据──

O formato de saída é geralmente JSON:

> 输出格式通常是JSON:

```json
{"action": "click", "x": 384, "y": 220, "element_desc": "Search button"}
```

O `element_desc`ajuda a recuperação: se as coordenadas se deslocarem entre as capturas de tela, a sugestão semântica permite que o sistema re-terrestre.

> `element_desc`帮助恢复:如果坐标在截图间漂移,语义提示让系统重新定位──

### Esquemas de ação.

Um esquema de ação típico tem 6 a 10 tipos de ação:

> O modelo típico de movimento inclui 6 a 10 tipos de movimento:

> **【中文解读】**O modelo típico de movimento inclui 6-10 tipos de movimentos: clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique, clique,

- `click`(x, y)
  Tradução:`click`:点击 (x, y)
- `type`(texto, x?, y?)
  Tradução:`type`:输入文本,可选位置──
- `scroll`: (direcção, quantidade)
  Tradução:`scroll`A direção, a quantidade.
- `drag`(x0, y0, x1, y1)
  Tradução:`drag`: de (x0, y0) 拖到 (x1, y1)。
- `select`: (option_index)
  Tradução:`select`:选择选项。
- `hover`(x, y)
  Tradução:`hover`: suspenso (x, y)
- `navigate`- Não .
  Tradução:`navigate`- Não, não.
- `wait`(ms)
  Tradução:`wait`Esperem mil segundos.
- `done`(sucesso, explicação)
  Tradução:`done`:完成(成功/失败, explicar) 』

O agente emite uma ação por passo. O envelope do navegador executa e retorna o novo estado.

> Agente cada passo de saída de um movimento.

### Só para captura de tela vs. árvore de acessibilidade .

> **【中文解读】**两种输入模式: Pure截图模式最通用但精度较低;无障碍树 (无障碍树) 无障碍信息) 无障碍信息 (无障碍信息) 无障碍信息 (无障碍信息) 无障碍信息) 无障碍模式 (público) 无障碍信息 (无障碍信息) 无障碍信息 (无障碍信息) 无障碍信息 (无障碍信息) 无障碍信息 (无障碍信息) 无障碍信息 (无障碍信息) 无障碍信息 (无障碍信息) 无障碍信息 (无障碍信息) 无障碍模式 (无障碍信息) 无障碍模式 (无障碍信息) 无障碍信息) 无障碍模式 (无障碍信息) 无障碍信息 (无障碍信息) 无障碍信息) 无障碍模式 (无障碍信息) 无障碍模式 (无障碍模式) 无障碍模式 (无障碍模式) 无障碍模式 (无障碍模式) 无障碍模式 (incluindo o método de utilização simultânea, 截图 (incluindo o método de manipulação de átomos) 截图 (incluindo o método de manipulação de átomos) 截图 (incluindo o método de informação) 截图) 截图 (incluindo o método de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de informação de base)

Dois modos de entrada:

> 两种输入模式:

- Apenas imagem de tela: imagem completa, sem informações estruturais.
  Tradução do inglês: Pure截图:完整图像,无结构信息──最通用;适用于任何应用──
- Árvore de acessibilidade: informação estruturada de acessibilidade DOM / iOS. Muito mais confiável para a aterragem; funciona onde a árvore está disponível.
  Não há obstáculos em usar dados em um arco.
- Híbrido: ambos, com a árvore como base confiável para ações atômicas e a captura de tela para contexto semântico.
  中文翻译:混合:两者都用,树用于原子动作定位,截图用于语义理解。

Os agentes de produção usam híbridos quando possível. A automação do navegador (Selenium + acessibilidade) sempre tem a árvore; às vezes, os aplicativos de desktop.

> Produção Agente 尽可能使用混合模式──浏览器自动化(Selenium + 无障碍) Sempre há árvore; aplicação em desktop há──

### Memória de longo prazo. Memória de longo prazo.

Um fluxo de trabalho de 20 passos gera 20 capturas de tela. O contexto do VLM se enche rapidamente.

> 20 步工作流产生 20 张截图──VLM 上下文快快填满──三种压缩策略:

> **【中文解读】**20 步工作流产生 20 张截图,VLM 上下文很快填满了.

- Resumo-cadeia: depois de cada 5 passos, resumir o que aconteceu, soltar capturas de tela antigas.
  Chinese: 摘要链: cada 5 步总结 já acontecido, deixando o antigo截图.
- Skip-frame: mantenha a primeira, a última e cada 3a captura de tela.
  Tradução do português: 跳:保留首、尾和每第 3 张截图──
- Registo de ferramentas: executa ações, mantenha um registro de texto do que foi feito; não volte a olhar para capturas de tela antigas.
  Tradução do inglês para tradução do inglês para inglês: instrument记录日志:执行动作,保留文本日志;不重新查看旧截图──

A API de computador do Claude usa o padrão de registro, mais simples e confiável.

> O computador de Claude usa API Uso de padrão de registro.

### Usar ferramentas visuais Usar ferramentas visuais

> **【中文解读】**ChartAgent  introduzir ferramentas de visão调用:Agent pode sair "corte de área (100,200,300,400) e então usar OCR" como ferramenta de调用.

O ChartAgent (arXiv:2510.04514) introduz o uso de ferramentas visuais para a compreensão de gráficos: crop, zoom, OCR, chamada de detecção externa. O agente pode emitir "crop to region (100, 200, 300, 400) e depois chamar OCR" como uma chamada de ferramenta. A ferramenta retorna texto; o VLM continua a raciocínio.

> ChartAgent  introduzir ferramentas de visão调用用于图表理解:剪剪,缩放,OCR、调用外部检测──Agent pode sair "剪到区域 (100, 200, 300, 400) e então调用 OCR" como ferramenta调用──工具返回文本;VLM 继续推理──

Este padrão generaliza: a solicitação de conjunto de marcas, anotação de região e ferramentas de detecção externas se encaixam no mesmo esquema "saia uma chamada de ferramenta, receba uma resposta estruturada".

> Este modelo pode ser promovido: conjunto de marcas de indicação, marcas de área e ferramentas de exame externo são adaptados ao mesmo "output tool调用, reception structured response" modelo.

### Os índices de referência de 2026

> **【拓展：多模态 Agent 基准全景】**ScreenSpot-Pro 测试 GUI 定位(open模型 ~85%,前沿 ~90%);VisualWebArena 测试端到端网页任务(open模型 ~20%,Gemini 3 Pro ~27%);AgentVista é o 2026 mais difícil基准, cobrindo 12 áreas de trabalho real, modelo da frente apenas 27-40%;WebArena/WebShop 已被前沿模型和──

- ScreenSpot-Pro. GUI de aterragem em ~ 1k web screenshots. SOTA Qwen2.5-VL-72B ~ 85% Frontier ~ 90%.
  O que é o "Show" de uma versão de "Show" de "Show" de uma versão de "Show" de uma versão de "Show" de uma versão de "Show" de uma versão de "Show" de uma versão de "Show" de uma versão de "Show" de uma versão de "Show" de uma versão de "Show" de uma versão de "Show" de uma versão de "Show" de uma versão de "Show" de uma versão de "Show" de uma versão de "Show" de uma versão de "Show" de uma versão de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de "Show" de " " " " " " " " " " "Show" de " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
- VisualWebArena. tarefas web de ponta a ponta (loja, fórum, anúncios classificados). SOTA aberta ~ 20%. Gemini 3 Pro ~ 27%.
  O que é o "VisualWebArena?""Term to end" (em inglês)
- O modelo de referência mais difícil de 2026: fluxos de trabalho realistas em 12 domínios.
  Chinese: 中文翻译:AgentVista──2026 年最难基准──跨 12 领域真实工作流──前沿模型 27-40%;开放模型 10-20%──
- WebArena / WebShop. Referências mais antigas; saturadas por fronteira.
  中文翻译:WebArena / WebShop。旧基准; já foi previamente modelo和。

### Porque é que ainda é difícil?

> **【中文解读】**Agente  desempenho botelha:1) 细粒度视觉定位("点击小 X"在移动分辨率下经常失败);2) 长期规划(10 步后Agente 偏离目标);3) 错误恢复(点击失败时检测和恢复缺乏训练数据);4) 跨页面上下文(跳转标签页或长表单丢失状态) ――研究方向包括记忆架构、、式重规划多样形验证──

Gargalos de engarrafamento no desempenho do agente:

> Agente 性能瓶:

1. "Clique no pequeno X" falha frequentemente na resolução móvel.
   Chinese: 小粒度视觉定位── "点击小 X"在移动分辨率下经常失败──
2. Depois de 10 ações, o agente desvia-se do alvo.
   Tradução do inglês: 长期规划──10 个动作后
3. Recuperação de erro. Quando um clique falha (botão errado), detecção + recuperação raramente é treinado dados.
   Tradução do inglês: error recovery──点击失败时,检测+恢复缺乏训练数据──
4. Contexto de página cruzada. Salto entre as fichas ou formulários longos perde estado.
   Tradução do inglês:跨页面上下文──跳转标签页或长表单丢失状态──

Direcções de investigação: arquiteturas de memória, replanejamento explícito, verificação multimodal (combatimento de imagens de tela para o sucesso da ação).

> A partir de agora, o grupo de pesquisadores da Universidade de São Paulo (UCSB) vai realizar um estudo sobre a evolução da tecnologia e a evolução da tecnologia.

### A pedra angular construiu-o.

> **【中文解读】**毕业项目任务:构建一个计算机使用代理,能够读取预订网站模拟页面的HTML+截图,规划多步序列(搜索→选择→填表→提交),输出匹配动作模式的JSON动作,并对10固定任务进行评估──

A tarefa final: construir um agente de uso de computador que:

> 毕业项目任务:构建一个计算机使用 Agent,要求:

1. Leia a captura de tela HTML + de uma página falsa do site de reserva.
   Tradução do idioma: 截图──
2. Planeja uma sequência de vários passos: busca → selecionar → preencher formulário → enviar.
   中文翻译:规划多步序列:搜索→选择→填表→提交──
3. Emite ações JSON correspondentes ao esquema de ação.
   Tradução do inglês para o português:
4. Avalia em uma faixa fixa de 10 tarefas.
   Tradução do inglês:                                                                                                                                                                                                                                                            

A lição fornece código de andamio que é fácil de estender para um navegador real.

>  cursos fornecem código de escrita, fácil de expandir para o navegador real.

## Use-o com o framework implementado.
```figure
mm-agent-loop
```

## Usá-lo

`code/main.py`é o andaime de pedra:

- Definição JSON do esquema de ação (10 ações).
  中文翻译:动作模式 JSON 定义(10 种动作) 』
- O estado do navegador falso como ditado.
  No entanto, o que não é um problema é que o que está acontecendo.
- O esqueleto do agente: estado de recepção, emissão de ação, aplicação, ciclo.
  Tradução do inglês para o inglês:Agent 循环骨架:接收状态、输出动作、执行、循环。
- Mini-marca de referência de 10 tarefas (páginas sintéticas) para medir a taxa de sucesso de ponta a ponta.
  Tradução do inglês: 任务迷你基准 (título original)
- Anel de recuperação de erros para quando uma ação falha.
  Tradução do inglês para o inglês: 动作失败时的错误恢复子.

## Envia-o . Produto .

Esta lição produz`outputs/skill-multimodal-agent-designer.md`. Tendo em conta um produto de utilização informática (domínio, conjunto de ações, meta de avaliação), desenha o ciclo completo de agentes, a estratégia de memória, o modo de aterramento e a pontuação esperada de referência.

> 本课产 出 `outputs/skill-multimodal-agent-designer.md` fornecer produtos de uso de computadores (s) (s) (s), (s) (s) (s) (s), (s) (s) (s) (s), (s) (s) (s) (s), (s) (s) (s) (s) (s), (s) (s) (s) (s), (s) (s) (s) (s), (s) (s) (s) (s), (s) (s) (s) (s), (s) (s) (s), (s) (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (s), (e (s), (e (f) (f) (f) (f) (f) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (d) (

## Exercícios.

1. Extenda o esquema de ação com um `screenshot_region`ferramenta (crop + zoom). Que tarefas são de benefício?
   扩展动作模式, adição `screenshot_region`工具(裁剪+缩放) ◊ quais tarefas serão beneficiadas?

2. Leia AgentVista (arXiv:2602.23166). Descreva a categoria de tarefas mais difíceis e por que os modelos de fronteira ainda falham.
   阅读 AgentVista 论文──descrever as categorias de tarefas mais difíceis e as razões pelas quais o modelo de vanguarda ainda falha──

3. Compressão de memória de longo horizonte: desenhar uma cadeia de resumo com ≤4 capturas de tela mantidas em directo, qualquer número registado.
   长期记忆压缩: desenhar uma cadeia de resumo, manter ≤4 张截图活跃, número arbitrário registrado até日志。

4. Construir um gancho de recuperação de erros: em falha de ação (botão não encontrado), o que o agente faz a seguir?
   Quando o processo de construção é falhado, o agente faz o seguinte passo?

5. Compare Claude 4.7 com um screenshot híbrido + árvore de acessibilidade Qwen2.5 - VL em 10 tarefas da web. Qual vence em quais tarefas?
   Comparado com o modelo de Claude 4.7 em quadros simples e o modelo mixado Qwen2.5 VL em 10 missões de páginas web.

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|----------|
| GUI grounding | "Click coordinates" | Model outputs (x,y) for the target of an instruction on a screenshot | GUI 定位：模型输出截图上指令目标的 (x,y) 坐标 |
| Action schema | "Tool definitions" | JSON description of valid actions (click, type, scroll, drag) | 动作模式：有效动作的 JSON 描述 |
| Accessibility tree | "Structured DOM" | Machine-readable UI hierarchy from browser/iOS APIs | 无障碍树：来自浏览器/iOS API 的机器可读 UI 层级 |
| Hybrid agent | "Screenshot + tree" | Uses both image and structured info; more reliable than either alone | 混合 Agent：同时使用图像和结构化信息 |
| Visual tool use | "Zoom/crop/detect" | Agent calls external vision tools (OCR, detection) mid-plan | 视觉工具使用：Agent 在规划中调用外部视觉工具 |
| Summary-chain | "Memory compression" | Periodic text summaries replace long screenshot history | 摘要链：定期文本摘要替代长截图历史 |
| VisualWebArena | "E2E web bench" | 2024 benchmark for end-to-end web tasks | 端到端网页任务基准（2024） |
| AgentVista | "2026 hard bench" | 12-domain realistic workflows; even Gemini 3 Pro scores ~30% | 12 领域真实工作流基准，前沿模型仅约 30% |

## Mais leitura 延伸阅读

- [Cheng et al. — SeeClick (arXiv:2401.10935)](https://arxiv.org/abs/2401.10935)
- [Hong et al. — CogAgent (arXiv:2312.08914)](https://arxiv.org/abs/2312.08914)
- [You et al. — Ferret-UI (arXiv:2404.05719)](https://arxiv.org/abs/2404.05719)
- [ChartAgent (arXiv:2510.04514)](https://arxiv.org/abs/2510.04514)
- [Koh et al. — VisualWebArena (arXiv:2401.13649)](https://arxiv.org/abs/2401.13649)
- [AgentVista (arXiv:2602.23166)](https://arxiv.org/abs/2602.23166)
