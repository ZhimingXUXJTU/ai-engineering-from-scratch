# Modelos de Língua de Vídeo: Tokens Temporais e Grounding.

> O vídeo não é uma pilha de fotos. Um clip de 5 segundos tem ordem causal, verbos de ação e cronometragem de eventos que um modelo de imagem não pode representar. Video-LLaMA (Zhang et al., junho 2023) enviou o primeiro open video-LLM com a terração audiovisual. O VideoChat e o Video-LLaVA escalaram o padrão. Até 2025, o TMRoPE da Qwen2.5-VL encerrou a lacuna com os modelos proprietários de fronteira. Cada sistema resolveu tokens temporais de forma diferente  Q-former por clip, concat-pool por frame, TMRoPE por token. Esta lição lê os padrões, constrói um amostragem de quadro uniforme versus dinâmico e avalia as tarefas de aterragem temporal.

> **【中文解读】**视频不是一堆照片的堆积──5秒的短视频包含因果顺序、动作动词和事件时间信息,这是图像模型无法表示的──从 Video-LLaMA(2023) 到Qwen2.5-VL(2025),视频 VLM 核心突破在时间位置编码TMRoPE 让模型能够看到"4.2秒"而不是"第15"──

**Type:** Build
**Languages:** Python (stdlib, frame sampler + temporal-grounding evaluator)
**Prerequisites:** Phase 12 · 08 (LLaVA-OneVision)
**Time:** ~180 minutes

> - Não .**【前置】**O programa de estúdio é o primeiro e mais importante para a série de jogos de vídeo.
> - Não .**【类比】**视频 VLM 处理时间维度 = "看足球比赛回放"──均采样 = 每 10 秒截一(错过进球瞬间);事件驱动采样 = 进球时密集采样+其他时间稀疏(捕捉关键时刻);动态 FPS = 根据画面变化自动调度──TMRoPE 让模型能理解"4.2 秒发生进球"而不是"第15 ", é o produto de nível de vídeo entender o关键──

## Objetivos de aprendizagem

- Explique por que a codificação posicional temporal altera o desempenho do VLM de vídeo independentemente do codificador de visão.
  Tradução do inglês para tradução do inglês: VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  VLM  V
- Compare a amostragem uniforme, dinâmica-FPS e de quadros orientados por eventos em tokens-por-segundo versus precisão de aterragem.
  Chinese Language Translation: Comparar com a taxa de precisão de posições e números por segundo.
- Descreva Q-former-per-clip (Video-LLaMA) vs pooled-per-frame (Video-LLaVA) vs M-RoPE-per-token (Qwen2.5-VL) projetos.
  O que é que você tem a ver com o seu nome?
- Cite os quatro critérios de referência para o vídeo: VideoMME, TempCompass, EgoSchema, Video-MMMU.
  O que é que você tem a ver com o seu próprio nome?

## O problema é o problema da introdução

Um vídeo de 1 minuto a 30 FPS é de 1800 quadros. A 196 tokens visuais por quadro (ViT-B em 224), que é 352k tokens  maior do que qualquer contexto LLM da era de 2024.

> 1 minuto 30 FPS de vídeo tem 1800 ── em cada 196  vídeo token ((ViT-B em 224 resolução) calculado, com 352k de tokens  superou qualquer LLM de 2024 

> **【中文解读】**1 min 30FPS de vídeo tem 1800 , por ano 196  tokens de vídeo, total de 352k tokens muito além de 2024 LLM de cima e baixo janeiro。 três estratégias de compressão de cada tipo têm diferentes:

Existem três estratégias de redução:

> Três estratégias de compressão:

1. Quadros de submuestra (1-8 FPS dependendo do conteúdo).
   中文翻译:子采样(根据内容 1-8 FPS)。
2. Agrupar os tokens de patch de cada quadro de forma agressiva (3x3 ou 4x4 pool bilinear).
   Tradução do inglês para tradução do inglês:
3. Compressão através de um Q-former que toma um clip de 16 quadros e sai 64 tokens.
   Por meio de Q-former 压缩,将 16 片段映射为 64 个代币──

Cada troca é diferente. sub-sampling perde detalhes temporais. pooling perde detalhes espaciais. Q-former perde um pouco, mas economiza tokens.

> Cada tipo de peso é diferente. O tempo é perdido.

A codificação de posição temporal é o outro eixo: como o modelo sabe que o quadro 5 veio antes do quadro 6? As opções incluem RoPE temporal simples 1D (Video-LLaMA), incorporações temporais aprendidas (Video-LLaVA) e TMRoPE (Qwen2.5-VL, 3D completa).

> 时间位置编码是另一个维度:模型怎么知道第5 在第6 之前?选项包括简单的 1D 时间 RoPE(Video-LLaMA)、可学习时间嵌入(Video-LLaVA) 和TMRoPE(Qwen2.5-VL, completa 3D)。

## O conceito central.

> **【中文解读】**视频语言时序定位(Temporal Grounding) é preciso encontrar no vídeo com a descrição do tempo correspondente à descrição do vídeo.

> **【拓展：时序定位的应用场景】**时序定位在视频搜索、自动剪辑、体育分析、安防监控等场景有广泛应用──技术上分为时刻检索(定位单个片段) 和亮点检测(定位高光时刻)── atualmente, os melhores modelos alcançam cerca de 60% mIoU em Charades-STA dados coluna──


### Video-LLaMA: Q-former por clip + ramo de áudio

Video-LLaMA (2023) foi o primeiro vídeo-LLM aberto. Arquitetura:

> Video-LLaMA(2023) é a primeira aberta em vídeo LLM.

- Clip de 16 quadros a 2 FPS (de 8 segundos).
  中文翻译:16 片段,2 FPS(即8秒)
- Características de ViT por quadro -> Video Q-former que atende cruzando sobre todos os 16 quadros -> 32 consultas aprendidas -> LLM.
  Chinese Language Translation: 每 ViT 特征 → Video Q-former 对所有 16 做交叉注意力 → 32 个学习查询 → LLM。
- Ramo de áudio paralelo: forma de onda -> Encoder de áudio ImageBind -> Áudio Q-former -> 32 consultas -> LLM.
  中文翻译:并行音频分支:波形 → ImageBind 音频编码器 → Áudio Q-former → 32 个查询 → LLM。

Força: raciocínio conjunto audiovisual. Fraqueza: comprimento fixo do clip, sem fixação arbitrária de tempo.

> 优势:音视频联合推理――劣势: fixa片段长度, não pode fazer qualquer tempo

### VideoChat e Video-LLaVA

O VideoChat manteve a ideia de Video-LLaMA, mas deixou cair o áudio e simplificou. O Video-LLaVA (Lin et al., 2023) treinou um único codificador visual em ambas as imagens e quadros de vídeo ("alinhamento antes da projeção"), dando uma representação unificada. Ambos são o codificador CLIP congelado + MLP + LLM.

> VideoChat manteve a ideia de Video-LLaMA, mas eliminou o audio e simplificou-o.

Nenhum deles lida com vídeo longo.

> Não posso lidar com isso.

### Qwen2,5-VL e TMRoPE

Qwen2.5-VL introduziu TMRoPE  Temporal-Modality Rotary Position Embedding. Cada patch token carrega uma posição (t, h, w) onde t é o timestamp real (não o índice de quadro).

> Qwen2.5-VL  introduziu TMRoPE tempo-模态旋转位置编码── cada patch token 携带 (t, h, w) 位置, dentre eles t é o tempo real(非索引)──

Diferenças fundamentais do simples incorporamento temporal:

> Diferença fundamental entre o tempo simples e o tempo embutidos:

- O modelo vê "em 4,2 segundos" e não "no quadro 15".
  O modelo visto é "4,2 segundos" e não "15 "。
- Cada token visual gira independentemente por sua marca de tempo.
  Tradução do inglês para inglês:                                                                                                                                                                                                                                                           
- Compativel com FPS dinâmico. Se você amostrar a 2 FPS aqui e 4 FPS ali, o TMRoPE lida com o espaçamento desigual de forma nativa.
  Se algum lugar 2 FPS 采样、另一处 4 FPS 采样,TMRoPE 原生处理不均间隔──

O TMRoPE permite que "em que segundo o gato salta?" consultas. O modelo pode emitir "em 4,2 segundos".

> TMRoPE 支持"Cat in few seconds jumps?"

> **【中文解读】**TMRoPE é a inovação chave do Qwen2.5 - VL: cada token de visão porta (t, h, w) informações de localização, entre elas t é tempo real  e não  índice. Isso significa que o modelo vê "4,2 segundos" em vez de "15 ", e pode naturalmente processar o tempo de intervalo de tempo abaixo da taxa de diferença.

> **【拓展：TMRoPE 在金融视频分析中的应用】**A capacidade absoluta de posicionamento no tempo da TMRoPE é essencial para a cena financeira: quando o relatório financeiro é publicado em vídeo, pode-se determinar o lugar "o CEO quando fala sobre o crescimento de receita"; quando o monitoramento de transações é analisado em vídeo, pode-se marcar pontos de tempo de eventos extraordinários.

### Estratexias de amostragem de quadro

Uniforme: mostra N quadros uniformemente ao longo da duração.

> 均采样:在时长内均采样 N ──简单,但丢失运动峰值──

FPS dinâmico: amostra adaptativamente com base na intensidade de movimento. fluxo óptico ou diferenciação de quadro escolhe segmentos de alta moção para amostragem mais densa. Qwen2.5-VL traz sobre isso.

> 动态 FPS: De acordo com a intensidade do movimento auto-adaptada de amostragem.

Event-driven: executar um detector leve, amostrar mais onde a ação acontece.

> 事件驱动:运行轻量级检测器, 在动作发生处密集采样――VideoAgent 使用──

Quadro de teclado + contexto: amostra em limites de tomadas + alguns quadros adjacentes.

> 关键 + 上下文: 在镜头边界采样 + 少量相邻──用于电影内容──

> **【中文解读】**O que é o melhor método para o ano de 2026 é o FPS + 3x3 双线性池化──

### Reunião por quadro

A 1 FPS e 576 tokens por quadro, um clip de 5 minutos é de 172.800 tokens.

> 1 FPS ⋅ 576 tokens ⋅ 5 分钟片段 ⋅ 172.800 ⋅ tokens ⋅ Qwen2.5-VL-72B ⋅ 128k 上下文 可处理,但成本高──

3x3 bilinear pool reduz para 64 tokens por quadro -> 19.200 tokens por 5 minutos.

> 3x3 双线性池化降至每 64 tokens → 5 分钟 19,200 tokens── maioria das tarefas

Poem mais agressivamente (6x6 -> 16 tokens por quadro) para fluxos de trabalho de agentes onde o detalhe espacial importa menos.

> 更激进地池化(6x6 → 每 16 token) Adaptado para espaço细节不太重要

### Os quatro critérios de referência de vídeo

- VideoMME: compreensão completa do vídeo, curto + médio + longo.
  Tradução em inglês:VideoMME:综合视频理解,短+中+长。
- TempCompass: raciocínio temporal de graus finos, perguntas "antes" / "depois".
  Tradução do inglês para o português: TempCompass:细粒度时间推理, "之前"/"之后"问题──
- EgoSchema: vídeo em primeira pessoa de longo horizonte.
  O que é o "EgoSchema"?
- Video-MMMU: perguntas multimodal de vídeo multidisciplinares.
  O vídeo-MMMU:多模态多学科视频问题──

Uma avaliação completa de vídeo-VLM atinge os quatro. Eles enfatizam diferentes eixos  TempCompass é tudo sobre encomendar, EgoSchema é sobre 3 + minutos de raciocínio, VideoMME abrange durações.

> 完整的视频 VLM 评估需要覆盖全部四基准──它们测试不同维度TempCompass 关注时序,EgoSchema 关注 3分钟以上的推理,VideoMME 跨越不同时长──

### Formatos de saída de aterragem

Formatos de saída para aterragem temporal:

> 时序定位的输出格式:

- "O gato salta ao redor da marca de 4 segundos". Facil de analisar mas impreciso.
  Tradução do inglês: "Cat in 4 seconds or around jumping up".""
- JSON estruturado: `{"event": "jump", "start": 4.1, "end": 4.3}`O Qwen2.5VL treina isto.
  Tradução do português: JSON`{"event": "jump", "start": 4.1, "end": 4.3}`Qwen2.5VL                                                                                                                                                                                                                                                            
- Baseado em tokens: especial `<time>4.1</time>`Os tokens estão entrelaçados com a resposta.
  Tradução do português:`<time>4.1</time>`token 与答交错──Qwen2.5-VL 的内部格式──

O formato de saída JSON do Qwen2.5VL analisa diretamente.

> 基于 token 的格式在下游使用中最准确──Qwen2.5-VL 的 JSON 输出格式可直接解析──

### 2026 melhores práticas

Para VLMs de vídeo em 2026:

> 2026  Video VLM  ಅತ್ಯುತ್ತಮ практика:

- Encoder: SigLIP 2 com M-RoPE ou TMRoPE (Qwen2.5-VL).
  Tradução do português:编码器:带 M-RoPE 或 TMRoPE 的 SigLIP 2(Qwen2.5-VL) 』
- Amostragem de quadro: FPS dinâmico (1-4 dependendo do movimento) com tampa máxima do quadro.
  O número de pessoas que estão em situação de risco é de aproximadamente 1 a 4 anos.
- A combinação por quadro: 3x3 bilinear.
  Tradução do inglês:
- Saída: JSON estruturado com campos de tempo + evento.
  Tradução do inglês para tradução do inglês: JSON.
- Referências: VideoMME + TempCompass para geral; EgoSchema para longo horizonte.
  中文翻译:基准测试:通用用 VideoMME + TempCompass;长程用 EgoSchema。

## Use-o com o framework implementado.
```figure
video-temporal-patches
```

## Usá-lo

`code/main.py`inclui:

> `code/main.py`包含:

- Amplificadores de quadros de FPS uniformes e dinâmicos.
  Tradução do inglês:均和动态 FPS 采样器──
- Um avaliador de fixação temporal de brinquedos: dado um evento de "verdade básica" no tempo T e uma saída de modelo, pontuação de precisão com tolerância.
  Chinese Translation: a toying time sequence position evaluator: given given given time T's "real" events and model output, within the capacity difference range, em seu âmbito de competência.
- Uma comparação entre o Video-LLaMA (16 quadros, Q-former), o Video-LLaVA (8 quadros, MLP), o Qwen2.5-VL (FPS dinâmico + TMRoPE).
  O que é que você tem a ver com o seu vídeo?

## Envia-o . Produto .

Esta lição produz`outputs/skill-video-vlm-frame-planner.md`. Dada uma tarefa de vídeo (monitorização, reconhecimento de ação, fixação temporal, resumo), ele escolhe o amostragem de quadro, o factor de agregação, o formato de saída e o nível de precisão esperado.

> 本课产 出 `outputs/skill-video-vlm-frame-planner.md` dado um determinado vídeo tarefa ((monitoring]], movimentos de identificação, tempo de localização, resumo), ele seleciona o amostragem, o fator de produção, o formato de saída e a taxa de precisião de antecipação equação.

## Exercícios.

1. Para uma demonstração de 3 minutos de cozinha, escolha uniforme vs FPS dinâmico. Justifique com uma contagem de tokens.

2. TMRoPE adiciona o que especificamente uma tabela de inserção temporal simples não pode fazer? TMRoPE 具体添加了什么简单的时间嵌入表无法做到的功能?

3. Escreva um esquema JSON para o enraizamento temporal que um VLM possa aprender a emitir. Incluir casos de erro.

4. Leia a Seção 3 do Video-LLaVA sobre "Alignment Before Projection". Por que é melhor que treinar codificadores de imagem e vídeo separados?

5. Dada a tabela de classificação de VideoMME, qual é a diferença entre o modelo aberto superior e o modelo proprietário superior a partir de 2026? Quanto dessa diferença é atribuível à codificação temporal versus escala LLM base?

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Temporal grounding | "Time-localized answers" 时序定位 | VLM outputs a specific timestamp range for when an event happens VLM 输出事件发生的具体时间戳范围 | |
| TMRoPE | "Time-Multimodal RoPE" 时间-多模态旋转位置编码 | 3D rotary position with absolute timestamps, used by Qwen2.5-VL 带绝对时间戳的 3D 旋转位置编码 | |
| Dynamic FPS | "Motion-aware sampling" 运动感知采样 | Sample more frames in high-motion segments, fewer in static ones 高运动段密集采样，静态段稀疏采样 | |
| Frame pooling | "Spatial compress per frame" 逐帧空间压缩 | Reduce patches per frame with bilinear interpolation before the LLM LLM 前用双线性插值减少每帧 patch 数 | |
| Video Q-former | "Clip compressor" 片段压缩器 | Cross-attention bottleneck mapping N frames to K learned queries 将 N 帧映射为 K 个学习查询的交叉注意力瓶颈 | |
| VideoMME | "Video bench" 视频基准 | Comprehensive short/medium/long video benchmark, 2500+ samples 覆盖短/中/长视频的综合基准测试 | |

## Mais leitura 延伸阅读

- [Zhang et al. — Video-LLaMA (arXiv:2306.02858)](https://arxiv.org/abs/2306.02858)
- [Li et al. — VideoChat (arXiv:2305.06355)](https://arxiv.org/abs/2305.06355)
- [Lin et al. — Video-LLaVA (arXiv:2311.10122)](https://arxiv.org/abs/2311.10122)
- [Qwen Team — Qwen2.5-VL (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923)
- [Lin et al. — VILA-1.5 (arXiv:2312.07533)](https://arxiv.org/abs/2312.07533)
