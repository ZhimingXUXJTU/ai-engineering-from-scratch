# Comprensião de vídeo longo em contexto de milhões de tokens .

> Um vídeo 4K de 1 hora a 24 FPS, parcheado e incorporado, produz a ordem de 60 milhões de tokens. Um episódio de podcast de 2 horas transcrito é de 30.000 tokens. Um filme completo de Blu-ray, mesmo comprimido com agressão, é de centenas de milhares de tokens. O Gemini 1.5 do Google (março de 2024) abriu esta era com um contexto de 10 milhões de tokens, fazendo uma recall confiável de agulha em uma pilha de feno em vídeos de uma hora. LWM (Liu et al., fevereiro 2024) mostrou o caminho de escala da atenção do anel. O LongVILA e o Video- XL aumentaram ainda mais a ingestão. O VideoAgent trocou o contexto bruto por recuperação agente. Cada abordagem é uma troca diferente na composição, na recordação e na complexidade da engenharia. Esta lição lê-os lado a lado.

> **【中文解读】**1 小时 4K 视频可产生约6000.000 token,远超任何模型的上下文窗口──处理长视频有三条路径:(1) 暴力上下文(Gemini 1,5 000 000 token 上下文);(2) Ring Attention 跨设备分布式注意力;(3) Token 压缩(Video-XL 摘要);(4) Agent 检索(VideoAgent 将视频当数据库查询) ⋅ Cada caminho tem diferenças em quantidade de cálculo, taxa de convocação e complexidade de projeto.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, needle-in-haystack simulator + agentic-retrieval router) | **语言:** Python（标准库，大海捞针模拟器 + Agent 检索路由器）
**Prerequisites:** Phase 12 · 17 (video temporal tokens) | **前置知识:** Phase 12 · 17（视频时间 token）
**Time:** ~180 minutes | **时间:** ~180 分钟

> - Não .**【前置】**O que é que você está fazendo? Você está fazendo isso? Você está fazendo isso? Você está fazendo isso? Você está fazendo isso?
> - Não .**【类比】**长视频理解 = "看完整部电影后能回答细节"──三种策略:(1) Gemini 1.5 路线 = Colocar o filme inteiro em seu cérebro(10M token 上下文,硬件怪兽);(2) Video-XL 路线 = 看完写摘要+检索原始片段(token 压缩);(3) VideoAgent 路线 = 当数据库查,问题导向地拉取相关段(Agent 检索) ~~

## Objetivos de aprendizagem

- Calcule o conteúdo total de tokens visuais para vídeos de formato longo em diferentes FPS e pooling.
  Tradução do inglês para tradução do inglês: calcula diferença FPS 和池化配置下长视频的视觉代币 总数──
- Explique os três caminhos de escalagem: contexto bruto (Gemini 1.5), atenção ao anel (LWM), compressão de tokens (LongVILA / Video-XL).
  Tradução do inglês em japonês:解释三条扩展路径:暴力上下文
- Compare VLMs de vídeo de contexto bruto vs VLMs de vídeo de recuperação de agentes (VideoAgent) em precisão e latência.
  Comparar original on downstream VLM 和 Agente 检索视频 VLM(VideoAgent) em Precisação e Tarde em
- Desenhar um teste de agulha em um monte de feno para um vídeo de 30 minutos e medir a recall em um minuto específico.
  Tradução do inglês para Chinês:为30分钟视频设计大海捞针测试并测量特定分钟的召回率──

## O problema é o problema da introdução

Um único quadro de patches de tamanho Qwen2.5VL com 384 resoluções nativas é ~729 tokens. Em 3x3 pooling isso é 81 tokens por quadro. Um clip de 30 minutos em 1 FPS = 1800 quadros = 145.800 tokens. Feliz até 2025.

> Qwen2.5-VL Big小的补丁 在 384 原生分辨率下每约729 token──3x3 池化后每 81 token──30 分钟片段 1 FPS = 1800  = 145,800 token,2025年开放 VLM 可处理但紧张──2 FPS 下 291,600 token只有最大上文才能容纳──

Um filme de 2 horas em 1 FPS é de 583k tokens. Além da maioria dos modelos abertos de 2026; requer Gemini 2.5 Pro ou agrupamento mais agressivo.

> 2 小时电影 1 FPS é 583k token── ultrapassando a capacidade da maioria dos modelos abertos de 2026; precisa de Gemini 2.5 Pro ou mais ativada de acumulação──

Surgiram três caminhos de escala.

> A expansão é um processo de desenvolvimento.

## O conceito central.

> **【中文解读】**长视频理解(百万代币 级别) é uma das principais desafios da IA em vários modelos.

> **【拓展：Gemini 1.5 Pro 的百万 token 上下文**Gemini 1.5 Pro  suporta 1M token  entrada, pode ser processado cerca de 1 horas de vídeo ou 1000+ páginas de documentos.


### Caminho 1: contexto bruto (Gemini 1.5, Claude Opus)

Atira hardware para o problema, escala contexto para milhões de tokens, processar tudo em uma passagem para a frente.

> Us Hardware Violence Solutions. O texto será expandido para milhões de tokens, uma vez para o outro para a distribuição de todo o conteúdo.

O Gemini 1.5 Pro foi lançado com 1M tokens; Gemini 1.5 Ultra para 10M; Gemini 2.5 Pro em 2026 faz horas de vídeo de forma confiável.

> O Gemini 1.5 Pro em 1M token  lançado  Gemini 1.5 Ultra  expandido para 10M; Gemini 2.5 Pro em 2026 pode ser devidamente processado  video ⋅ artigo registrou 99,7% de grande escala de recomposição em torno de 9,5M token ⋅

Engenharia: uma implementação de atenção personalizada com hierarquia de memória (local + global + escassa) mais roteamento de especialistas em MoE para eficiência de longo contexto. Não publicado em detalhes completos. Não de código aberto.

> 工程实现: auto-definir mecanismo de atenção,带有内存层次(局部+全局+稀疏),加上 MoE 专家路由提升长上下文效率──未完整公开──非开源──

### Caminho 2: Atenção ao anel (LWM, LongVILA)

A atenção em anel distribui longas sequências entre dispositivos em um "anel" onde cada dispositivo mantém um pedaço.

> **【中文解读】**O Ring Attention distribuirá a longa sequência em vários dispositivos, cada dispositivo tem um bloco de sequência, através de comunicação circular calcular a atenção integral.

LWM (Liu et al., 2024) treinou um modelo de contexto de 1M-token desta forma.

> LWM(Liu 等人,2024) com este método treinado 1M token 上下文模型── treinamento calcular quantidade com o aumento linear do volume de dados, e não de segunda dimensão

LongVILA (arXiv:2408.10188) adaptou o padrão para VLMs. Vídeos de 1400 quadros em 192 tokens por quadro = contexto de 268k, treinados com atenção de anel em paralelo de 8 vias.

> LongVILA vai adaptar este modelo a VLM──1400 视频, por cada 192 tokens = 268k 上下文, através de 8 路并行环形注意力训练──

### Caminho 3: Compressão de tokens (Video-XL, LongVA)

Mais barato do que o contexto bruto: comprime agressivamente antes que o LLM veja a sequência.

> Bì violence上下文より便宜: em LLM 看到序列之前進行激進壓縮──

Video-XL (arXiv:2409.14485) usa um token de resumo visual: cada clip de quadros N produz um único token de "resumo" que atende ao N. Na inferência, o LLM vê um token de resumo por clip, reduzindo drasticamente o contexto.

> Video-XL Utilize Vídeo 片段生成一个"摘要"代号,对该 N 做注意――推理时 LLM Cada um dos vídeos só vê um tóquio de resumo, reduzindo significativamente a seguinte:

LongVA estende o contexto de LLM de 200 mil para 2 milhões com uma técnica de "transferência de contexto longo".

> LongVA utilizou a técnica de "长上下文迁移" para LLM 上下文 de 200k 扩展到2M── em longa

A compressão de tokens elimina o recall em marcas de tempo específicas para a escalabilidade. O modelo geralmente sabe o que aconteceu, mas às vezes perde os quadros exatos.

> O token  comprimação em sacrifício de tempo específico da taxa de retorno em troca de expansão.

### Caminho 4: Recuperação de Agentes (VideoAgent)

Não entregue o vídeo completo ao LLM. Em vez disso, trate o vídeo como um banco de dados e use um LLM para consultá-lo.

> Não coloque todo o vídeo em um LLM.

VideoAgent (arXiv:2403.10517):

> VideoAgente ((arXiv:2403.10517):

1. O LLM lê a pergunta.
   > LLM 读取问题──
2. O LLM pede uma ferramenta de recuperação de clips relevantes ("mostra-me segmentos com um gato").
   > LLM 调用检索工具获取相关片段("给我看有猫的片段")
3. A ferramenta retorna as marcas de tempo do clip.
   > 工具返回匹配的片段时间──
4. O LLM lê esses clips através de um VLM.
   > LLM 通過VLM 读取这些片段──
5. O Mestrado em Direito e Direito compõe a resposta ou faz perguntas de acompanhamento.
   > O Mestrado em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito.

Este é o padrão LLM-as-agente aplicado a vídeos longos. inferência mais barata (apenas clips relevantes codificados), engenharia mais difícil (qualidade de recuperação torna-se o gargalo de engarrafamento).

> É o que fazer para o LLM como agente 模式应用到长视频──推理更便宜──

### Indicadores de referência para agulhas em um estábulo de feno

O teste padrão de longo contexto: insira um marcador visual ou textual único em um ponto aleatório no vídeo, e, em seguida, faça uma consulta que exige a sua recordação.

> 标准长上下文测试: inserir um marcador único de vídeo ou texto em qualquer posição no vídeo, e então apresentar uma consulta necessária para lembrar esse marcador.

Metrícula: Recall@k em longo de vídeo e posição do marcador.

> Indicador:跨视频长度和标记位置的 Recall@k。

Os modelos Gemini 2.5 Pro pontua >99% de recall em vídeos de até 90 minutos. Os modelos 72B abertos (Qwen2.5-VL-72B, InternVL3-78B) pontua ~85-90% em 30 minutos e degradam para além de 60.

> Gemini 2.5 Pro em 90 minutos de vídeo sobre a taxa de convocação >99%──aberta 72B 模型(Qwen2.5-VL-72B、InternVL3-78B) em 30 minutos de volta em torno de 85-90%,60 minutos de volta em volta──

O VideoAgent pode combinar ou vencer modelos de contexto bruto em 2 horas ou mais porque a recuperação atinge a agulha se a ferramenta for boa.

> VideoAgent pode ser combinado ou superado no modelo original de vídeo de 2 horas ou mais, pois, desde que a ferramenta seja boa, a pesquisa pode atingir o objetivo.

### Que caminho escolher

Para um clip de 15 minutos com precisão de fronteira: aberto 72B + contexto nativo geralmente funciona.

> 15 分片段追求前沿准确率:开放 72B + 原生上下文通常可行──选 Qwen2.5-VL-72B──

Para conteúdo de 30 minutos a 1 hora: LongVILA ou Video-XL para aberta; Gemini 2.5 Pro para fechado.

> 30 minutos a 1 hora de conteúdo: aberta com LongVILA ou Video-XL; fechada com Gemini 2.5 Pro;;

Para conteúdo de mais de 2 horas: VideoAgent ou padrões de recuperação similares. Alternativamente, resuma em pedaços menores e alimenta resumos hierárquicos.

> 2 小时以上内容:VideoAgent ou similar search mode──或缩写为更小块并进入分层摘要──

### Modelo de produção 2026

Na prática, as canais de produção de vídeo longo são híbridas:

> Na prática, a produção de vídeos é um mix de:

1. Execute amostragem dinâmica de FPS + agressão em conjunto em todo o vídeo (obtenha uma representação global de 100k-token).
   O vídeo foi lançado em 17 de janeiro de 2015 e foi lançado em 18 de janeiro de 2015.
2. Passe para um VLM 72B para um resumo global.
   Tradução do inglês:传入 72B VLM 生成全局摘要.
3. Se o utilizador fizer perguntas detalhadas, execute a recuperação agencial usando o resumo como índice.
   Se o usuário perguntar detalhes, use resumo como índice de execução Agente 检索。

Isso combina contexto bruto para compreensão global e recuperação de detalhes locais.

> Isto combina a compreensão geral do contexto da violência e a capacidade de detalhes locais de investigação.

## Use-o com o framework implementado.
```figure
mm-video-token-budget
```

## Usá-lo

`code/main.py`- Não .

- Computa orçamentos de tokens para vídeos de 1 minuto a 3 horas em diferentes FPS + pooling.
  Chinese Translation:计算 1 分钟到 3 小时视频在不同 FPS + 池化下的代币 预算──
- Simula uma corrida de agulha em um monte de feno: injetar um marcador em um tempo aleatório, fazer uma pergunta, marcar a recordação.
  Chinese: 模拟大海捞针测试: 注入标记,提问,评分召回率──
- Inclui um simulador de roteador de recuperação de agentes que seleciona clips específicos para alimentar um VLM a jusante.
  Tradução do inglês para inglês:

Escreva a tabela de orçamento e sinta a diferença na escala.

> 运行预算表,感受规模差距──

## Envia-o . Produto .

Esta lição produz`outputs/skill-long-video-strategy-planner.md`. Dada a duração do vídeo e a complexidade da consulta, ele escolhe entre conteúdo bruto, compressão e recuperação agencial e calcula as expectativas de latência + qualidade.

> 本课产 出 `outputs/skill-long-video-strategy-planner.md` Dado o tempo e a complexidade da consulta, ele é selecionado entre violência e compressão, e calcula o atraso + expectativa de qualidade.

## Exercícios.

1. Uma palestra de 45 minutos a 1 FPS, 81 tokens por quadro. Tokens totais?

2. Desenhar um teste de agulha em um monte de feno: em que minuto você injeta o marcador, e qual é o formato exato da consulta?

3. Comparar conteúdo bruto Qwen2.5-VL-72B (contexto 80k) com VideoAgent (Claude 3.5 + recuperação) em um vídeo de 1 hora. Qual vence no recall? Qual vence na latência?

4. A escala de custo de memória da atenção de anel linearmente em comprimento de sequência e linearmente em contagem de dispositivos. Explique por que e o que falha se você deixar cair a fase de rotação de anel.

5. Leia Gemini 1.5 Secção 5 sobre agulha em uma pilha de feno. O que o jornal descobriu sobre a recall na fronteira de token 1M vs 10M?

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Brute context | "Just more tokens" 暴力上下文 | Scale LLM context to millions of tokens; process everything in one pass 将 LLM 上下文扩展到百万 token，一次前向传播处理全部内容 | |
| Ring attention | "LWM-style parallel" 环形注意力 | Distributed attention pattern where each device holds a chunk and rotates 分布式注意力模式，每个设备持有一块并在环中轮转 | |
| Token compression | "Summary tokens" 摘要 token | Reduce per-clip tokens via a learned compressor before the LLM LLM 前通过学习型压缩器减少每片段 token 数 | |
| Needle-in-haystack | "NIH test" 大海捞针测试 | Insert a unique marker at a random point, ask model to recall it at test time 在随机位置插入唯一标记，测试时要求模型回忆 | |
| Agentic retrieval | "LLM as query planner" Agent 检索 | LLM asks a retrieval tool for relevant clips, reads them via a VLM, composes answer LLM 调用检索工具获取相关片段，通过 VLM 阅读并生成回答 | |
| VideoAgent | "Retrieval pattern for video" 视频检索模式 | Canonical agentic-retrieval design: question -> tool -> clip -> answer 经典 Agent 检索设计：问题→工具→片段→回答 | |

## Mais leitura 延伸阅读

- [Gemini Team — Gemini 1.5 (arXiv:2403.05530)](https://arxiv.org/abs/2403.05530)
- [Liu et al. — LWM / RingAttention (arXiv:2402.08268)](https://arxiv.org/abs/2402.08268)
- [Xue et al. — LongVILA (arXiv:2408.10188)](https://arxiv.org/abs/2408.10188)
- [Shu et al. — Video-XL (arXiv:2409.14485)](https://arxiv.org/abs/2409.14485)
- [Wang et al. — VideoAgent (arXiv:2403.10517)](https://arxiv.org/abs/2403.10517)
