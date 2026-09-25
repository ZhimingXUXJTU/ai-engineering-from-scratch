# Qwen-VL Família e Dinâmica-FPS Video  Qwen-VL  série com o movimento 率视频

> A família Qwen-VL  Qwen-VL (2023), Qwen2-VL (2024), Qwen2.5-VL (2025), Qwen3-VL (2025)  é a linhagem de modelos de linguagem de visão aberta mais influente em 2026. Cada geração fez uma única aposta arquitetônica decisiva que o resto do ecossistema aberto copiou em doze meses: resolução dinâmica nativa através de M-RoPE, amostragem dinâmica-FPS com alinhamento de tempo absoluto, atenção de janela no ViT e formatos de saída de agente estruturado. Por Qwen3-VL, a receita havia se estabilizado: um codificador 2D-RoPE-ViT com entradas nativas de relação de aspecto, um projetor MLP em uma grande base de linguagem Qwen3, e estágios de treinamento que enfatizava o OCR, o enraizamento e o comportamento do agente como alvos de primeira classe. Esta lição lê a família em ordem cronológica para que compreendas por que cada botão está onde está.

> **【中文解读】**Qwen-VL 系列 é a família de modelos de linguagem de 2026 mais influente. Cada geração fez uma decisão de estrutura chave, tomada pela comunidade de código aberto em 12 meses, em conformidade com: M-RoPE Origins

> **【拓展：Qwen-VL 的产业生态位】**Qwen-VL 系列 possui vantagens significativas no sentido de compreender o OCR e o vídeo.

**Type:** Learn  | **类型：学习**
**Languages:** Python (stdlib, M-RoPE encoder + dynamic-FPS sampler)  | **语言：Python（标准库，M-RoPE 编码器 + 动态帧率采样器）**
**Prerequisites:** Phase 12 · 06 (patch-n'-pack)  | **前置：阶段12第06课（补丁打包）**
**Time:** ~120 minutes  | **时长：约120分钟**

> - Não .**【前置】**學本节前请先掌握:Fase 12·06(patch-n'-pack 任意分辨率);Fase 7·04(RoPE 旋转位置编码,本节升级为 3D M-RoPE);Fase 14·04(Agent 工具调用,本节讲解 VLM 如何输出 JSON)
> - Não .**【类比】**Qwen-VL 系列 = "中文 VLM 旗舰"──和 LLaVA 系列的区别:LLaVA 主打英文 + 简单架构;Qwen-VL 主打中英双语 + 高分辨率 + 结构化输出──
> ️ **【易错点】**Qwen-VL 输出边界框坐标时混"绝对像素 vs相对比例"不同代次使用不同约定──Qwen2-VL 用绝对像素(0-1000 范围),Qwen2.5-VL 改用归一化比例(0-1)──修复:使用前查文档,按代次正确解析坐标──

## Objetivos de aprendizagem

- Calcule as rotativas de três eixos do M-RoPE (temporal, altura, largura) e explique por que são necessárias todas as três.
- Escolha uma estratégia de amostragem dinâmica de FPS para um vídeo e razone sobre a precisão de tokens por segundo versus detecção de eventos.
- Nomear as quatro atualizações geracionais Qwen-VL em ordem e o que cada uma habilitou.
- Arranjar um formato de saída do agente JSON de estilo Qwen2.5VL e analisar as chamadas de ferramentas estruturadas de uma resposta VLM.

## O problema é o contexto do problema .

O Qwen-VL foi enviado em agosto de 2023 como resposta direta ao LLaVA-1.5 e BLIP-2.

Resolução: LLaVA-1.5 funcionou em 336x336. Bom para fotos, inútil para uma fatura em chinês ou uma tela de tela de cálculo densa. A primeira inovação do Qwen-VL foi 448x448 e saída de caixa de limite terrestre, deixando o modelo apontar para as coisas.

Video: Video-LLaMA empilhou codificadores por quadro e os alimentou para o LLM. Funcionou para clips curtos, não para vídeos de vários minutos onde o eixo temporal é o sinal. A equipe Qwen queria um único codificador que entenda o tempo.

Output estruturado: LLaVA emite texto de forma livre. Um agente precisa de JSON. Qwen-VL treinado em formatos de saída JSON explícitos, incluindo coordenadas de caixa de limites como texto.

Cada geração Qwen-VL estende um destes três eixos.

> **【中文解读】**Qwen-VL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

## O conceito central.

### Qwen-VL (Agosto 2023)

A primeira geração: OpenCLIP ViT-bigG/14 como codificador (2.5B parâmetros), LLama-compatível Q-Former (1-passo com 256 consultas), base Qwen-7B. Contribuições:

- Resolução 448x448 (então SOTA para um VLM aberto).
- "O gato está em <box> 112, 204, (280, 344)</box>".
- Chinese + English Multilingual Training desde o início.

Os critérios de referência na época: competitivo com o GPT-4V em inglês, dominante no chinês.

> **【中文解读】**Qwen-VL primeira geração de ruptura:448x448 resolução(超越 LLaVA 的 336x336) 定位能力(输出边界框坐标)  中英双语──在中文基准上显著领先──

### Qwen2-VL (septembro 2024)  M-RoPE e resolução nativa  Qwen2-VL: M-RoPE com resolução de origem

Qwen2-VL substituiu a pilha de resolução fixa + Q-Former por um codificador ViT de resolução dinâmica nativo.

- Resolução dinâmica nativa / 原生动态分辨率. O ViT aceita qualquer HxW divisível por 28 (patch 14 com 2x fusão espacial). Uma imagem em 1120x672 (40x24 patches fusíveis) produz 960 tokens visuais.
- M-RoPE (Multimodal RoPE) / 多模态旋转位置编码. Cada token carrega uma posição 3D (t, h, w) em vez de 1D. Para imagens t = 0, para vídeo t = frame_index. RoPE gira vectores de consulta / chave por uma frequência por eixo. Não há tabela de inserção posicional.
- MLP projector / MLP 投影器. Deixe o Q-Former; use um MLP de 2 camadas nos tokens de parche combinados.
- Video com FPS dinâmico / 动态率视频. Vídeo amostrado em 1-2 FPS por padrão, mas o modelo aceita contagens arbitrárias de quadros.

Resultado: Qwen2-VL-7B equipara GPT-4o em vários benchmarks multimodal e superou-o em DocVQA (94.5 vs 88.4).

> **【中文解读】**A estrutura central do Qwen2-VL mudou: eliminando resolução fixa + Q-Former, substituindo a resolução de vida original ViT + M-RoPE + MLP  Projector. M-RoPE para cada token  atribui uma posição 3D ( tempo, altura, largura), fazendo com que a mesma posição codifique a capacidade de processar textos, imagens e vídeos.

### Qwen2.5VL (Fevereiro 2025)  FPS dinâmico + tempo absoluto  Qwen2.5VL: movimento 率 + 绝对时间

O grande passo da Qwen2.5VL foi o vídeo.

- Títulos de tempo absoluto / 绝对时间 token. Em vez de índices de posição (quadro 0, 1, 2...), use timestamps reais. "À 0:04, o gato salta". O modelo vê `<time>0.04</time>`Tokens intercalados com tokens de quadro.
- FPS dinâmico / 动态率. Amostra a 1 FPS para imagens lentas, 4+ FPS para a ação. O usuário ou treinador escolhe; M-RoPE se adapta.
- Atenção à janela em ViT / ViT  janela  atenção à janela. Atenção espacial é janela (local dentro de blocos) para a transmissão; atenção global a cada poucas camadas.
- Formatos de saída JSON explícito / 显式 JSON 输出格式.`{"tool": "click", "coords": [380, 220]}`Agente pronto para sair da caixa.
- MRoPE-v2 escala / MRoPE-v2 缩放. Escala de posições com o tamanho máximo de entrada para que um vídeo de 10 minutos não se esgotar da faixa de frequência.

Benchmarks: Qwen2.5-VL-72B supera o GPT-4o na maioria dos benchmarks de vídeo, combina com o Gemini 2.0 nos documentos e define o SOTA de modelo aberto para o grounding da GUI (ScreenSpot: 84% de precisão vs 38% para o GPT-4o).

> **【中文解读】**Qwen2.5VL's breakthrough lies in video understanding: absolutamente tempo token 让模型知道"第4秒猫跳了",动态率让模型在动作密集时自动提高采样率,窗口注意力提升 ViT 吞吐量──72B 版本在视频基准上超越GPT-4o,GUI 定位精度(ScreenSpot 84%)远超GPT-4o(38%)──

> **【拓展：结构化输出对 Agent 工程的意义】**Qwen2.5-VL estruturado JSON 输出使之能直接作为计算机使用代理 (Computer Use Agent) 的视觉感知模块. Em cenários financeiros, isso significa que VLM pode sair estruturado "点击坐标" ou "提取的字段", diretamente consumido pelo sistema de download, sem necessidade de expressão de expressão.

### Qwen3-VL (novembro 2025)

Qwen3-VL é uma atualização incremental que consolida em vez de reinventar: maior espinha dorsal do LLM (Qwen3-72B), dados de treinamento expandidos, melhorado OCR, raciocínio mais forte através do "modo de pensamento" Qwen3.

A linha de linhagem: até 2025, a arquitetura Qwen-VL tinha se estabilizado.

> **【中文解读】**Qwen3-VL é um aumento de escala e não uma reinvenção: maior LLM 骨干、更多训练数据、更好的OCR、更强的推理(Qwen3 "思考模式")。ViT 和 M-RoPE 保持不变── até 2025, a estrutura do Qwen-VL já está estabilizada, a versão posterior será principalmente aumentada através de expansão e otimização de dados──

### M-RoPE matematicamente.

O RoPE clássico gira uma consulta `q`de dimensão `d`por posição `m`utilizando coordenadas emparelhadas:

```
q_rot[2i]   = q[2i]   * cos(m * theta_i) - q[2i+1] * sin(m * theta_i)   # 经典 RoPE 旋转
q_rot[2i+1] = q[2i]   * sin(m * theta_i) + q[2i+1] * cos(m * theta_i)
theta_i     = 10000^(-2i/d)                                                 # 频率基
```

O M-RoPE divide o escuro escondido em três bandas.`d = 96`. Assinar 32 dims para temporário, 32 para altura, 32 para largura. Cada faixa gira por sua própria posição de eixo. Um parche em (t=5, h=10, w=20) obtém rotações `R_t(5)`- Não .`R_h(10)`- Não .`R_w(20)`Aplicada às suas três bandas.

Uso de tokens de texto `t = text_index, h = 0, w = 0`(ou uma escolha normalizada), mantendo a compatibilidade.`t = frame_time, h = row, w = col`. Uso de imagens únicas `t = 0`- Não .

A vantagem: uma codificação de posição lida com texto, imagem e vídeo sem código ramificado ou tabelas de posição diferentes.

> **【中文解读】**M-RoPE vai dividir a dimensão oculta em três frequências (tempo, altura, largura), cada frequência em função de seu próprio eixo de rotação.

### Dinâmica-FPS de amostragem lógica 动态 率采样逻辑

Dado um vídeo de duração `T`segundos e um orçamento de tokens-alvo `B`- Não .

1. Calcule o máximo de FPS que pode pagar: `fps_max = B / (T * tokens_per_frame)`Calcula a taxa máxima de renda.
2. Escolha um FPS alvo de `{1, 2, 4, 8}`que satisfaz .`fps <= fps_max`- De entre os candidatos.
3. Se o movimento for alto (heurística de fluxo óptico ou pedido explícito do usuário), escolha FPS mais alto. Se o movimento for baixo, escolha mais baixo.
4. Amostra uniformemente no FPS escolhido; insira `<time>t</time>`- Sim, sim. - Sim, sim.

Qwen2.5-VL treina essa lógica implicitamente; na inferência o utilizador controla através de `fps`Parâmetro: Uma sequência de ação de 60 segundos em 4 FPS com 81 tokens por quadro = 19440 tokens, gerenciável em um contexto de 32k.

> **【中文解读】**动态率的核心思想:根据视频时长、token 预算和运动量,自动选择最佳率──60秒动作场景在4FPS下产生19440 token,可在32k上下文中处理──

### Output de agente estruturado .

O treinamento de agentes da Qwen2.5VL visa explícitamente as chamadas de ferramentas estruturadas:

```
{
  "tool": "mouse_click",          # 工具名称
  "coords": [1024, 512],          # 点击坐标
  "button": "left",               # 鼠标按钮
  "modifier": null                # 修饰键
}
```

O parsing é determinista: JSON.parse sobre a saída do modelo. Comparar com o "clique em (1024, 512) " em forma livre, que exigia regex e manipulação de ambigüidade. A mudança é por que as pontuações ScreenSpot do Qwen2.5-VL saltaram de 55% para 84%.

> **【中文解读】** Struktural output permite que o VLM possa enviar diretamente ferramentas resolúveis de modo regular (como clicando em "坐标"), sem necessidade de expressão de regras.
```figure
mm-mrope-axes
```

## Usá-lo

## Use-o em prática.

`code/main.py`Implementos:

- M-RoPE computação de posição para uma sequência de mistura de texto, imagens e quadros de vídeo.
- Dinâmico-FPS amostragem: dado (durada, orçamento, movimento_nível), escolher FPS e emitir marcas de tempo de quadro.
- Um parsemador de saída de JSON Qwen2.5VL que lida com respostas de chamadas de ferramenta com campos de coordenadas.

## Envia-o .

Esta lição produz`outputs/skill-qwen-vl-pipeline-designer.md`. Dada uma tarefa de vídeo (monitorização, agente, reconhecimento de ação, acessibilidade), emite a configuração Qwen2.5VL (orçamento de quadro, estratégia FPS, bandeira de atenção à janela, modo de saída de agente) e uma estimativa de latência.

> **【中文解读】**O programa de ensino de ensino superior é um programa de ensino de ensino superior de ensino médio, com um objetivo de melhorar a qualidade de vida e melhorar a qualidade de vida dos estudantes.

## Exercícios.

1. Calcule as rotações M-RoPE para um parche em (t=3, h=5, w=7) com 48 escondidos (16 por banda, base theta 10000). Mostre os ângulos de rotação para os três primeiros pares em cada banda.
   | 计算 (t=3, h=5, w=7) 补丁的 M-RoPE 旋转，隐藏维度48（每频段16），基数10000。展示每频段前三对的旋转角度。

2. Uma câmera de segurança de 10 minutos em 1 FPS produz quantos quadros? Em 384 resolução com pool 3x, quantos tokens totais?
   | 10分钟安防摄像头录像在 1FPS 下产生多少帧？384分辨率+3x池化后多少 token？Qwen2.5-VL 默认 32k 上下文能处理吗？

3. Escolha FPS para um rally de tênis de 30 segundos versus uma demonstração de receita de 30 segundos versus uma gravação de agente de interface de 30 segundos.
   | 为 30 秒网球比赛、30 秒食谱演示、30 秒 UI 代理录像选择帧率。用动态帧率逻辑论证每个选择。

4. Qwen2.5VL deixa cair o Q-Former inteiramente. Por que um simples MLP funciona em 2025 mas não em 2023?
   | Qwen2.5-VL 完全去掉了 Q-Former。为什么 MLP 在 2025 年可行但 2023 年不行？（提示：数据规模和编码器质量。）

5. Parse três Qwen2.5-VL JSON ferramenta-chamadas de saída em Python dicts. O que falha para JSON malformado e que estratégia de recuperação recomendamos Qwen cookbook?
   | 将三个 Qwen2.5-VL JSON 工具调用输出解析为 Python 字典。畸形 JSON 会出什么问题？Qwen 食谱推荐的恢复策略是什么？

## Termos-chave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| M-RoPE | "Multimodal RoPE" | 3D rotary position embedding with temporal, height, and width bands in the hidden dim | 三维旋转位置编码，隐藏维度分时间、高度、宽度三个频段 | |
| Dynamic FPS | "Smart sampling" | Frame sampling rate chosen per video based on motion, duration, and token budget | 根据运动量、时长和 token 预算动态选择帧率 | |
| Absolute time token | "Timestamp token" | `<time>t</time>` interleaved in the sequence so the model sees actual seconds not frame index | 在序列中插入真实时间戳 token | |
| Window attention | "Local attention" | Spatial self-attention restricted to small windows for speed; global attention added periodically | 空间自注意力限制在小窗口内加速，周期性加入全局注意力 | |
| Structured agent output | "JSON mode" | Training data supervision teaching the VLM to emit parseable JSON with coords and tool names | 训练 VLM 输出可解析的 JSON（含坐标和工具名） | |
| min_pixels / max_pixels | "Resolution bounds" | Per-request Qwen2.5-VL controls bounding total pixel count and therefore token count | 按请求控制最小/最大像素数从而控制 token 数 | |
| Grounding | "Point-at-it" | Outputting bounding-box coordinates as text tokens; used since Qwen-VL v1 | 输出边界框坐标作为文本 token，从 Qwen-VL v1 开始支持 | |

## Mais leitura 延伸阅读

- [Bai et al. — Qwen-VL (arXiv:2308.12966)](https://arxiv.org/abs/2308.12966)Qwen-VL Primeira geração
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191)♬ Qwen2-VL M-RoPE
- [Qwen Team — Qwen2.5-VL Technical Report (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923) Qwen2.5VL 
- [Qwen Team — Qwen3-VL (arXiv:2511.21631)](https://arxiv.org/abs/2511.21631)Qwen3-VL aumento de potência
- [Zhu et al. — InternVL3 (arXiv:2504.10479)](https://arxiv.org/abs/2504.10479)O InterVL3
