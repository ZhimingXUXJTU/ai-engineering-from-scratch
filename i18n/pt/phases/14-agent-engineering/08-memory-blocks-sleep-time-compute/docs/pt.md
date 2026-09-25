# Blocos de memória e tempo de sono (Letta)
# Blocos de memória e tempo de sono

> O modelo pode editar diretamente e um agente de tempo de sono que consolida a memória de forma assíncrona enquanto o agente primário está ocioso.

> **【中文解读】**MemGPT em 2024 tornou-se Letta. A evolução de 2026 acrescentou duas ideias: o modelo pode editar diretamente os blocos de memória de função dispersada, bem como o Agente de repouso do Agente principal 空時異步合并記憶.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT) | **前置知识:** Phase 14 · 07 (MemGPT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Nomear os três níveis de memória que Letta usa (núcleo, recall, arquivo) e o papel de cada um.
  O Letta utiliza três níveis de memória (core, recall, archive) e seu papel.
- Explique o padrão de bloqueio de memória: Bloco humano, bloco Persona e blocos definidos pelo usuário como objetos de primeira classe.
  中文翻译:解释记忆块模式:Human 块、Persona 块和用户自定义块作为一等类型化对象──
- Descreva o que é o cálculo do tempo de sono, por que fica fora do caminho crítico e por que pode executar um modelo mais forte do que o agente primário.
  O que é o cálculo do sono? Por que ele está fora do caminho-chave? Por que pode ser executado em relação ao agente principal?
- Implementar um ciclo de dois agentes scripted onde um agente primário serve respostas e um agente de tempo de sono consolida blocos entre viradas.
  Tradução do inglês para o inglês: implementing a scripting dual agent loop, main agent 提供响应,休眠 agent 在轮次间合并块──

## O problema é o problema da introdução

MemGPT (Lessão 07) resolveu o fluxo de controle de memória virtual.

> MemGPT ((第 7 课) resolveu o fluxo de controle de memória virtual. Surgiram três problemas de produção:

1. **Latency.**Cada operação de memória está no caminho crítico. se o agente tiver que poda, resumir ou reconciliar enquanto o usuário espera, a latência da cauda explode.
   Tradução:**延迟。**Cada operação de memória está em um caminho fundamental. Se o agente tiver que cortar o resumo ou coordinar o processo de espera do usuário, o final vai ser adiado.
2. **Memory rot.**Os escritos acumulam-se, os fatos contraditórios permanecem, a recuperação afoga-se em conteúdo obsoleto.
   Tradução:**记忆腐化。**写入积累――矛盾的事实保留――检索被过时内容淹没――
3. **Structure loss.**Um arquivo plano não pode expressar "o bloco humano está sempre no prompt; o bloco Persona está sempre no prompt; o bloco tarefa troca por sessão".
   Tradução:**结构丢失。**平的归档存储不能表达"Human 块始终在提示中;Persona 块始终在提示中;Task 块按会话交换――"

Letta (letta.com) é o nome da plataforma o projeto MemGPT original adotado em 2024  O padrão do papel mantém o nome MemGPT  e a reescritura de 2026 Letta V1 é um passo posterior e separado.

> Letta (Letta.com) é uma reescritura de 2026: o bloco de memória torna a estrutura expressiva; o cálculo de sono irá se juntar e se mover para um caminho fundamental.

> **【中文解读】**記憶塊 (memória blocos) e休眠計算 (休眠計算) são duas estratégias de otimização do MemGPT/Letta. 記憶塊 (memória blocos) são um segmento de texto fixo de grande dimensão, semelhante a uma página de memória, usado para controlar detalhadamente a proporção de informações nas janelas de texto.

> **【拓展：Letta 的演进】**Letta(original MemGPT) introduziu dois conceitos-chave no desenvolvimento de 2024-2025 de blocos de memória e de cálculo de repouso.

> - Não .**【前置】**必須先通過Fase 14·07 (MemGPT) 本節是它的直接延续──如果你不理解 MemGPT's"主上下文 vs 外部上下文"两层模型,那么 Letta's三层(core/recall/archival) 扩展会把你搞──

## O conceito central.

### Três níveis

| Tier | Scope | Where it lives | Written by |
|------|-------|----------------|------------|
| 层级 | 范围 | 存储位置 | 写入者 |
| Core | Always visible | Inside the main prompt | Agent tool call + sleep-time rewrites / Agent 工具调用 + 休眠重写 |
| Recall | Conversation history | Retrievable | Automatic turn logging / 自动轮次日志 |
| Archival | Arbitrary facts | Vector + KV + graph | Agent tool call + sleep-time ingest / Agent 工具调用 + 休眠摄取 |

O núcleo é o núcleo MemGPT. O memorando é o buffer de conversação com a sua cauda despejada. O arquivo é a loja externa. A divisão limpa a sobrecarga de dois níveis do MemGPT.

> O núcleo é o núcleo do MemGPT. O memorando é o diálogo do grupo de controle de dados. O arquivo é o arquivo externo.

### Blocos de memória

Um bloco é uma seção tipada, persistente e editável do nível principal.

> O bloco é a tipificação de camadas principais, a perpetuidade, a edição de áreas diferentes.

- **Human block** Factos sobre o utilizador (nome, função, preferências, objectivos).
  Tradução:**Human 块** Sobre os fatos do usuário (姓名,角色,偏好,目标)
- **Persona block** autoconceito do agente (identidade, tom, restrições).
  Tradução:**Persona 块**Agent's ego concept (conceptos de autor) 身份、语气、约束) 

Letta generaliza para blocos arbitrários definidos pelo usuário: a `Task`Bloque para o objectivo actual, um `Project`Bloco de dados baseados em código, a`Safety`Bloco para restrições duras.`id`- Não .`label`- Não .`value`- Não .`limit`(capítulo de caracteres), `description`(para que o modelo saiba quando editá-lo).

> Letta 泛化为任意用户定义块:用于当前目标的 `Task`块、用于代码库事实 `Project`块、 para usar de hard binding `Safety`Todos os blocos têm`id`- Não.`label`- Não.`value`- Não.`limit`(字符上限)`description`(让模型知道何时编辑它)

Os blocos são editáveis através da superfície da ferramenta:

> 块通过工具接口可编辑:

- `block_append(label, text)`
  Tradução:`block_append(label, text)`向块追加文本──
- `block_replace(label, old, new)`
  Tradução:`block_replace(label, old, new)`替换块中的文本──
- `block_read(label)`
  Tradução:`block_read(label)`读取块内容──
- `block_summarize(label)` condensa um bloco próximo do seu limite.
  Tradução:`block_summarize(label)` Compressão aproximada do limite de blocos

### Computação do tempo de sono

A adição Letta 2025: executar um segundo agente em segundo plano, fora do caminho crítico.`learned_context`em blocos compartilhados e consolidar ou invalidar os registos de arquivo.

> 2025 Letta's new addition function:                                                                                                                                                                                                                                                           `learned_context`写入共享块,并合并或使归档记录失效──

Propriedades que caem:

> 随之产生的特性:

- **No latency cost.**As respostas primárias não esperam por operações de memória.
  Tradução:**无延迟成本。**Não aguardo a memória.
- **Stronger model allowed.**O agente de tempo de sono pode ser um modelo mais caro e mais lento porque não é limitado pela latência.
  Tradução:**允许更强的模型。**O Agente de sono pode ser mais caro, um modelo mais lento, porque não é limitado a atrasos.
- **Natural consolidation window.**Dedup, resumir, invalidar fatos contraditórios quando o usuário não está esperando.
  Tradução:**天然的合并窗口。**Em um momento de não esperar, o usuário vai recorrer ao resumo, fazendo com que as contradições falhem.

A forma corresponde ao modo como os humanos trabalham: você faz a tarefa, dorme sobre ela, a memória a longo prazo se acalma durante a noite.

> - Não .**【类比】**Computação de tempo de sono 像夜晚的清洁工:白天你(主代理) ocupado em responder clientes, escritórios(主上下文)堆满今天的会议记录、文件、咖啡杯;晚晚清洁工(睡眠时间代理) 进来擦桌子、归档文件、把"明天要跟进的事"贴到便利贴上(写入人/任务块) ・・・ 第二天你来上班,看整洁待的桌面和清晰的办公清单──**关键**O cliente não está esperando.

> Esta forma de trabalho é de acordo com o modo humano: você faz tarefas, você dorme, longa-term memória em noite.

### Letta V1 e raciocínio nativo
### Raciocínio nativo

Letta V1 (`letta_v1_agent`, 2026) deprecia `send_message`/ batimento cardíaco e em linha`Thought:`Os responsáveis API (OpenAI) e as mensagens API com pensamento extendido (Antropic) emitem o raciocínio em um canal separado, passado por turnos (encriptado entre provedores na produção). O ciclo de controle ainda é ReAct. O rastro de pensamento é estrutural, não em forma de prompt.

> Letta V1`letta_v1_agent`,2026) abandonado`send_message`/ Heart jump e dentro `Thought:`A partir daí, o sistema de controle é um sistema de controle que é um sistema de controle de dados e de dados.

### Onde este padrão vai mal

> ️ **【易错点】**"静默漂移" é o bug mais perigoso da Letta 部署: agente do sono em backstage alterou o bloco de personalidade (por exemplo, "始终使用中文回复"改成"中英文混用"), mas o principal agente não sabe.**后果**O usuário encontra o agente  comportamento mutar mas não encontra nenhuma causa  porque o diário de diálogo só registra a saída do agente principal **一行修复**: Cada vez que você dorme  write in posterior version                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

- **Block bloat.**Infinito .`block_append`Envia um resumo de bloco antes da escrita que empurra sobre o limite.
  Tradução:**块膨胀。** infinito `block_append` Rapidamente alcançar o limite superior                                                                                                                                                                                                                                                          
- **Silent drift.**O agente do sono reescreve um bloco e o agente principal nunca percebe.
  Tradução:**静默漂移。**Agente de descanso Reescrever blocos mas o principal Agente de não notar.
- **Poisoned consolidation.**O agente do sono processa o conteúdo alcançável pelo atacante no núcleo.
  Tradução:**投毒合并。**O Agente de Hospedagem irá processar o conteúdo do atacante no núcleo.

> 🤔 **【困惑】**P: Agente de tempo de sono com modelos mais fortes não será mais caro? Por que é economizar dinheiro em vez de queimar dinheiro? A:**避开了关键路径的高价** Agente principal  deve usar streaming + alta prioridade, único preço é 2-3 vezes do lote.

## Construí-lo.
```figure
memory-blocks
```

## Construí-lo

`code/main.py`Implementos:

> `code/main.py`实现:

- `Block` identificação, etiqueta, valor, limite, descrição.
  Tradução:`Block`id、etiqueta、valor、limit、descrição。
- `BlockStore` CRUD + `near_limit(label)`- Ajudante.
  Tradução:`BlockStore`CRUD + `near_limit(label)`辅助方法──
- Dois agentes com guião`PrimaryAgent`serve um turno, `SleepTimeAgent`consolida-se entre os viros.
  Tradução do português:`PrimaryAgent`- Não.`SleepTimeAgent`Em rotina, em rotina.
- Um rastro que mostra uma conversa de três voltas com o Bloc escreve, mais um passe de sono que resume um bloco e invade um fato antiquado.
  Tradução do inglês para o inglês: demonstrar três rodadas de diálogo com blocos de escrita, mais blocos de compressão e fazer o passado falhar de facto de tratamento de sono.

- É o que é ?

> 运行:

```
python3 code/main.py
```

A transcrição mostra a divisão: as viradas primárias são rápidas e produzem escritos crus; o passe de sono compacta e limpa.

> 转录记录显示分工:主轮次快速产生原始写入;休眠处理压缩和清理──

## Use-o com o framework implementado.

- **Letta**(letta.com) para a implementação de referência.
  Tradução:**Letta**(letta.com) Referência: realização.
- **Claude Agent SDK skills**Como conhecimento em forma de bloco  uma habilidade é um bloco de instruções nomeado, versão, recuperável que o agente carrega à demanda.
  Tradução:**Claude Agent SDK skills**Como blocos de conhecimento, a habilidade é denominada, versão, versão, controle de blocos de instruções, Agente por carga.
- **Custom builds**Para equipes que querem o controle sobre o backend de armazenamento, use o contrato Letta API para poderem migrar mais tarde.
  Tradução:**自定义构建** Adaptado para querer controlar o armazenamento de fundos de armazenamento.

## Envia-o . Produto .

`outputs/skill-memory-blocks.md`gera um sistema de blocos em forma de Letta com ganchos de tempo de sono para qualquer tempo de execução, incluindo regras de segurança e cablagem de citação.

> `outputs/skill-memory-blocks.md`Para qualquer operação gerar Letta forma de blocos sistemas, com ação de segurança e de ligação de referência.

## Exercícios.

1. Adicionar um`block_summarize`ferramenta que substitui o valor de bloco por um resumo gerado por modelo quando `near_limit`Qual limiar de gatilho minimiza as chamadas de resumo e o desbordamento de blocos?
   Tradução: 添加`block_summarize`工具, em `near_limit`返回 true 时使用模型生成的摘要替换块值──哪个触发值最小化摘要调用和块溢出? 返回 true 时用模型生成的摘要替换块值── 触发值最小化摘要调用和块溢出? 返回 true 时用模型生成的摘要替换块值── 触发值最小化摘要调用和块溢出?
2. Implementar a dedução do tempo de sono sobre o arquivo: dois registros cujo texto tem > 90% de sobreposição simbólica colapsam para um.
   Tradução do inglês: In the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical storage of the logical pathway.
3. Blocos de versão. em cada registro de escrita o valor antigo e uma diferença. Expor `block_history(label)`Então os operadores podem fazer o depósito "por que o agente esqueceu X".
   Tradução do inglês em grego: 版本化块──每次写入记录旧值和差异──暴露 `block_history(label)`Deixe-me tentar, porque o agente esqueceu o X?
4. Tratem os agentes do sono como escritores não confiáveis, quando tocarem no bloco Persona ou Segurança, precise de uma revisão de segundo agente antes de se comprometer.
   Quando eles tocam Persona ou Segurança, antes de enviar, eles precisam de um segundo agente.
5. Portar o exemplo para usar a API Letta (`letta_v1_agent`Quais são as mudanças no esquema de blocos, e como o raciocínio nativo altera a forma do rastro?
   Chinese:将示例移植为使用Letta API (Letta API)`letta_v1_agent`O que é que o modelo de bloco tem mudado? Como o modelo de vida original pode mudar o seu trajeto?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Memory block | "Editable prompt section" / "可编辑提示分区" | Typed, persistent, LLM-editable segment of core memory / 类型化、持久化、LLM 可编辑的核心记忆段 |
| Human block | "User memory" / "用户记忆" | Facts about the user, pinned in core / 关于用户的事实，固定在 core 中 |
| Persona block | "Agent identity" / "Agent 身份" | Self-concept, tone, constraints, pinned in core / 自我概念、语气、约束，固定在 core 中 |
| Sleep-time compute | "Async memory work" / "异步记忆工作" | Second agent doing consolidation off the critical path / 第二个 Agent 在关键路径之外做合并 |
| Core / Recall / Archival | "Tiers" / "层级" | Three-layer memory split: always-visible / conversation / external / 三层记忆拆分：始终可见 / 对话 / 外部 |
| Block limit | "Cap" / "上限" | Character limit per block; forces summarization / 每个块的字符限制；强制摘要 |
| Native reasoning | "Thinking channel" / "思考通道" | Provider-level reasoning output, not prompt-level `Thought:` / 提供商级推理输出，非提示级 `Thought:` |
| Learned context | "Sleep output" / "休眠输出" | Facts the sleep-time agent writes into shared blocks / 休眠 Agent 写入共享块的事实 |

## Mais leitura 延伸阅读

- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) padrão de bloco
  中文翻译:Letta 记忆块博客块模式。
- [Letta, Sleep-time Compute blog](https://www.letta.com/blog/sleep-time-compute) Consolidação de sincronização
  Tradução do inglês:Letta 休眠计算博客异步合并──
- [Letta, Rearchitecting the Agent Loop](https://www.letta.com/blog/letta-v1-agent) Reescrever o raciocínio nativo
  Tradução do inglês: Letta 重建 Agent 循环博客原生推理重写。
- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) origem
  Tradução do português:MemGPT 论文起源──
