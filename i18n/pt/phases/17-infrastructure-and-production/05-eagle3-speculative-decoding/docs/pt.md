# A Descodagem Especulativa em Produção

> A descodificação especulativa combina um modelo de projeto rápido com o modelo alvo. O projecto propõe tokens K; o alvo verifica-se em um único prazo; tokens aceitos são gratuitos. Em 2026, o EAGLE-3 é a variante de nível de produção  ele treina um projeto de cabeça nos estados ocultos do modelo alvo em vez de em tokens brutos, empurrando a taxa de aceitação alfa para a faixa de 0,6-0,8 no bate-papo geral. A pergunta certa não é "quão rápido é o projeto", mas "o que é o alfa no meu tráfego?" Se o alfa cair abaixo de ~0.55, a descodificação especulativa é negativa líquida em alta concurência porque cada projeto rejeitado custa uma segunda passagem de destino para a frente. Esta lição ensina-te a medir o alfa primeiro e a virar a bandeira em segundo lugar.

> **【中文解读】**Este capítulo apresenta a técnica de avaliação de aceleração de dados.
**Type:** Learn
**Languages:** Python (stdlib, toy acceptance-rate simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 10 · 18 (Multi-Token Prediction)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy acceptance-rate simulator) | **语言:** Python（标准库，接受率模拟器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 18 (Multi-Token Prediction) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 10 · 18（多 Token 预测）

> - Não .**【前置】**學本节前请先掌握:Fase 17·04(vLLM) 、Fase 10·18(MTP 多 token 预测) 、Fase 10·25(投机解码原理) ⋅本节是生产版 EAGLE-3。
> - Não .**【类比】**EAGLE-3 = "翻译员打草稿"──草稿模型(草案) 快速猜 K 个代币,目标模型一次验证──猜对=免费,猜错=多一次验证开销──EAGLE-3 创新:用目标模型隐藏状态训练草案(而不是原始代币),接受率 α 提到 0.6-0.8──生产关键问题:α 在你的流量上多少?<0.55 时反而拖慢(拒绝的草案 浪费计算力)必须先测α 再开旗──
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizagem

- Nomear as três gerações de decodificação especulativa e explicar o que a EAGLE-3 muda da EAGLE-2 e de um modelo clássico de projeto.
  Tradução do inglês para o inglês:  中文翻译:说出推测解码的三代,并解释Eagle-3 相比Eagle-2 和经典草案 模型改变了什么──
- Defina a taxa de aceitação alfa, calcule a velocidade esperada a partir do alfa e K (longo de rascunho) e identifique o alfa de equilíbrio para a sua simultaneidade alvo.
  Tradução do inglês para o inglês: define rate of acceptance alpha, de alpha 和 K(draft 长度) calcular o esperado de aceleração,并确定目标并发下亏平衡 alpha──
- Explique por que a descodificação especulativa é opt-in (não padrão) no vLLM 2026 e por que ativá-la sem medir o alfa é um padrão anti-produção.
  Tradução do inglês para o inglês: Why not to measure alpha, why not to measure alpha, why not to start it is production counter mode.
- Escrever um plano de medição: qual referência, qual distribuição de prompt, qual ponto de concurência, qual métrica para entrar.
  Tradução do inglês para o inglês: write out measurement plan:哪个基准测试、哪个快点 分布、哪个并发点、哪个指标作为门控──

## O problema é o problema da introdução

> **【中文解读】**推理的解码阶段是内存带宽限定的每解码一个代币 需要读取约140 GB/s权重,GPU 计算几乎空──推测解码利用这个空: Usando um pequeno modelo barato gerar K 个候选代币, então deixar o modelo objetivo verificar todas as K 个个在一次前向传播中. △ Aceitação de taxa alfa é o único indicador importante低于0.55 时推测解码在高并发下反而有害.

> **【拓展：推测解码的产业应用】**O Google em 2025 vai lançar o seu código de busca em uma análise de IA, o que aumentou significativamente a velocidade de resposta em uma situação de perda de qualidade.`speculative_config`作为官方接口──在生产中,推测解码特别适合实时对话(TTFT 敏感) 和代码补全(延迟敏感)场景──但需要注意:高并发(256+) 当,decode batch 已经足够大,内存带宽的差距缩小,推测解码的收益降低──

O decodificador é limitado à memória. Em um H100 executando Llama 3.3 70B FP8, cada token decodificado lê ~ 140 GB / s de pesos e emite um token. O computador da GPU é quase ocioso durante o decodificação.

> 解码是内存限定的──在 H100 上运行 Llama 3.3 70B FP8 时, cada token 读取约140 GB/s de peso e输出一个 token──GPU 计算在解码期间几乎空瓶是HBM 带宽,而不是矩阵乘吞吐量──

A descodificação especulativa explora a lacuna. Gerencie tokens candidatos K com um modelo de projeto barato, em seguida, peça ao modelo alvo para verificar todos os K em uma única passagem para a frente. Cada token verificado é efetivamente livre (amortizado em um lote de K para a frente o alvo teria que fazer de qualquer maneira).

> 推测解码利用这个差距―― usando um projeto barato 模型生成 K 个候选标签,然后让目标模型在一次前向传播中验证所有 K 个――每个验证通过标签 实际上是免费的(分摊到目标模型应该做的 K 批前向中) ⋅

A abordagem clássica de modelo de projecto utiliza um modelo menor da mesma família (Llama 3.2 1B de elaboração para Llama 3.3 70B). Funciona, mas a taxa de aceitação é mediocre  a distribuição do modelo menor diverge do objetivo. A EAGLE, depois a EAGLE-2, depois a EAGLE-3 treinam uma cabeça de projeto leve diretamente nos estados internos do modelo alvo, de modo que a distribuição do projeto acompanha o alvo muito mais de perto. É por isso que o alfa passa de 0,4 com o modelo de projeto para 0,6-0,8 com o EAGLE-3.

> 经典的草案 模型方法使用同系列的更小模型(Llama 3.2 1B 为 Llama 3.3 70B 做草案) ―― é possível, mas a taxa de aceitação é plana更小模型的分布偏离目标──EAGLE、EAGLE-2、EAGLE-3 直接在目标模型的内部状态上训练轻量草案头,所以草案的分布更接近目标──这就是为什么从草案的0.4 升至EAGLE-3 的0.6-0.8──

A captura: A EAGLE-3 está a optar por participar no VLLM 2026. `speculative_config`As equipes que o desactivam sem medir o tráfego real, muitas vezes vêem a latência da cauda piorar, não melhorar.

> 关键点:EAGLE-3 em 2026 vLLM 中是选择进的──`speculative_config`必須明顯設定──無標志,就沒有加速──不測真流量 alfa 就開啟的團隊常見尾部延遲變差而不是改善──

## O conceito central.

### O que a descodificação especulativa realmente compra

> **【中文解读】**推测解码的加速比公式为 `S = (1 + K*alpha) / (1 + verify_overhead)` Para K=5, alfa=0,7, a aceleração teórica é de 4,1x. Mas a produção real normalmente alcança apenas 2-3x, pois o alfa raramente alcança 0,7 ou mais no fluxo real, e a produção de alta quantidade de lote aumenta.

Sem descodificação de especificações, o custo por token é um objetivo avançado. Com o descodificação de especificações no comprimento do projeto K e alfa de aceitação, os tokens esperados por token avançado é `1 + K * alpha`O acelerador é`(1 + K * alpha) / (1 + epsilon)`onde epsilon é o custo de verificação de cheque. para K=5, alfa=0,7: `(1 + 5*0.7) / (1 + 0.1) = 4.5 / 1.1 = 4.1x`Os números do mundo real agrupam-se em torno de 2-3 vezes porque o alfa raramente é tão alto no tráfego de produção e o epsilon cresce em grandes parcelas.

> 没有推测解码时,每 token 成本是一个目标前向传播──有推测解码时,草案 长度 K 和接受率 alpha 下,每次目标前向的预期代币 数为 `1 + K * alpha`◊ acelerar-se`(1 + K * alpha) / (1 + epsilon)`, dos quais o epsilon é um projeto + 验证开销── para K=5, alfa=0,7:`(1 + 5*0.7) / (1 + 0.1) = 4.5 / 1.1 = 4.1x` A concentração de dados real é de 2-3x, porque o alfa é muito pequeno no fluxo de produção, e o epsilon é muito grande no tamanho do lote.

### Porque é que o alfa é a única métrica que importa

Os tokens rejeitados não desaparecem  eles forçam um segundo alvo para a primeira token rejeitada. Em uma carga de trabalho onde o alfa cai para 0,4, pagas despesas gerais de projeto mais verificação mais re-roll. Em alta simultânea (digamos 256 simultâneos), o lote de decodificação já é grande o suficiente para que a diferença de largura de banda de memória entre "alvo sozinho" e "alvo com verificação" diminua. Abaixo do alfa 0,55 na maioria dos hardware de 2026, o código de especificações é negativo.

> Os tokens rejeitados não desaparecem, obrigando-os a realizar o segundo objetivo de propagação. Em uma carga de trabalho de 0,4 por alpha, você paga um projeto de expansão, verificação e reproduzção. Em alta e alta, o lote de resolução já é grande o suficiente, o limite de largura de memória entre o objetivo único e o objetivo de verificação é reduzido. Em 2026, na maioria dos hardware, o alfa é inferior a 0,55 por hora de avaliação.

O programa de treinamento de um projeto de trabalho em um grupo de dados de um grupo de trabalho, que é um grupo de treinamento de um grupo de trabalho, é um projeto de treinamento de um grupo de trabalho.

> Alpha 因工作负载而异. Em ShareGPT 风格的通用聊天天, com o treinamento ShareGPT  EAGLE-3 达到 0.6-0.8 . Em áreas específicas de tráfego 代码、医疗、法律) , com o treinamento de dados geral .

### GERAÇÕES de águia num olhar

> **【中文解读】**推测解码经历了三代演进:(1) Modelo clássico de esboço(同一系列的小模型,alpha 0.3-0.5)简单但接受率低;(2) EAGLE-1/2(在目标模型隐藏状态上训练草案头,alpha 0.5-0.7)更高接受率;(3) EAGLE-3(在多层隐藏状态上训练,alpha 0.6-0.8)2025-2026年生产级方案──关键区别是 EAGLE 直接在目标模型内部表示训练草案,而不是在原始代币上,因此分布更接近目标──

> **【拓展：推测解码 vs 其他加速技术】**LLM 推理加速技术对比:(1) 推测解码(EAGLE-3) 2-3x 加速, necessita de extra chefe de projeto;(2) 量化(INT8/FP8) 推理加速 1.5-2x, tem ligeira perda de qualidade;(3) 分块预填降低ITL Tail,但不直接提升吞吐;(4) 分分式预填/decode消除资源浪费,30-40% 成本节省;(5) 自研芯片(Groq/Cerebras) 5-10x 解码速度但单价更高──

- **Classic draft model**A infraestrutura é simples  dois modelos carregados, o projecto corre K para frente por alvo para frente.
  Tradução:**经典 draft 模型**A estrutura é simples, carregando dois modelos, um esboço para cada objetivo.
- **EAGLE-1 (2024)**A cabeça de projeto única treinada em estados ocultos do alvo (última camada).
  Tradução:**EAGLE-1 (2024)**O objetivo é alcançar o objetivo de um novo projeto de treinamento.
- **EAGLE-2 (2025)**A programação de projetos é mais complexa.
  Tradução:**EAGLE-2 (2025)**O projeto de desenvolvimento de um grupo de projetos de desenvolvimento de projetos de desenvolvimento de projetos de desenvolvimento de projetos de desenvolvimento de projetos de desenvolvimento de projetos de desenvolvimento de projetos de desenvolvimento de projetos de desenvolvimento de projetos de projetos de desenvolvimento de projetos de projetos de desenvolvimento de projetos de projetos de desenvolvimento de projetos de projetos de projetos de desenvolvimento de projetos de projetos de projetos de projetos de desenvolvimento de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projetos de projet
- **EAGLE-3 (2025-2026)**A formação de um chefe de projeto em várias camadas-alvo (não apenas a última), melhor alinhamento.
  Tradução:**EAGLE-3 (2025-2026)**O que é mais importante é que o programa de treinamento seja mais rápido e mais rápido.

### A receita de produção para 2026

> **【中文解读】**O processo de implementação da EAGLE-3 é de cinco etapas: 1) primeiro, com base no modelo de base, estabelecer TTFT/ITL/吞吐量基线; 2) ativar o projeto de EAGLE-3 配置; 3) monitorar a taxa de aceitação alfavLLM V1 通过`spec_decode_metrics.accepted_tokens_per_request`暴露此指标;(4) Se alfa < 0.55,禁用推测解码或训练领域特定草案头;(5) 在生产并发水平重新测试, confirmar P99 ITL 没有恶化──

1. Modelo de nave alvo simples. Messa TTFT de linha de base, ITL, rendimento na simultânea meta.
   Tradução do inglês para o inglês:                                                                                                                                                                                                                                                          
2. Ativar o projecto EAGLE-3 através do vLLM `speculative_config`Reexamine o índice de referência.
   Tradução do português:`speculative_config`Initial do projecto EAGLE-3
3. Taxa de aceitação de registos alfa. vLLM V1 informa isto como `spec_decode_metrics.accepted_tokens_per_request`Divida pelo comprimento do esboço solicitado para obter o alfa.
   Tradução do inglês:记录接受率 alpha──vLLM V1 通过 `spec_decode_metrics.accepted_tokens_per_request`報告──除以要求草案 长度得到 alpha──
4. Se o alfa < 0,55 na distribuição do tráfego de produção, desativar a descodificação das especificações ou criar um rascunho EAGLE-3 específico para o domínio.
   Se a distribuição de fluxo de produção em alfa < 0,55, é impossível fazer o projeto EAGLE-3 específico em um campo de treinamento.
5. Confirme que o P99 não piorou.
   Tradução do inglês: в производство并发下重新测试── confirmar P99 ITL 没有恶化──

### O problema da produção: cauda P99

O P99 pode piorar se você não sintonizar. Os projetos rejeitados desencadeiam uma sequência de duas passagens (draft + verifique-fail + re-rolo).

> 平均 ITL 随推测解码下降──如果不调优,P99可能恶化──被拒绝的草案 触发两次传递序列(草案 + 验证失败 + 重新生成)──在满批次下,这两次传递串行化──关注 P99 ITL,而不是 P50──

### Se o EAGLE-3 já estiver implantado

O Google implementou a descodificação especulativa em AI Overviews em 2025 (a mesma qualidade, resposta mais rápida).`speculative_config`como a interface documentada; a descodificação especulativa da GPU de N-gram em V1 é a variante compatível com preenchimento em pedaços. SGLang suporta EAGLE-3 como o caminho de projeto recomendado para cargas de trabalho pesadas de prefixos.

> O Google em 2025 vai lançar o código de desenvolvimento para AI Overviews.`speculative_config`Como interface documentada;N-gram GPU em V1 推测解码是与分块预填兼容的变体──SGLang 支持EAGLE-3 作为前密集工作负载的推草案路径──

### - Matemática de equilíbrio numa linha.

A aceleração prevista: `S(alpha, K) = (1 + K*alpha) / (1 + verify_overhead)`- Configuração .`S = 1`soluções para alfa: `alpha_breakeven = verify_overhead / K`. Para verify_overhead típico ~0,15 e K=5: `alpha_breakeven = 0.03`Mas essa é a matemática de decodificação crua. Na alta simultânea a verificação aumenta e o lote de decodificação já amortiza as leituras de memória em todas as sequências, então a efetiva equilíbrio alfa_breakeven sobe para ~0.45-0.55 na prática.

> 预期加速比:`S(alpha, K) = (1 + K*alpha) / (1 + verify_overhead)`。设 `S = 1`- Não .`alpha_breakeven = verify_overhead / K` Tipo de verificação ≈ 0,15,K=5:`alpha_breakeven = 0.03`, mas é o original de matemática. , em alta e alta evolução, a verificação de custos de venda aumentou, o número de unidades já foi lido em sequência entre as divisões, por isso, o nível de alfa_breakeven efetivo aumentou para cerca de 0,45-0,55.

### Quando não utilizar a descodificação especulativa

> **【拓展：推测解码的适用场景】**推测解码在以下场景有效:(1) 实时对话(TTFT < 200ms 要求) 2-3x 加速显著改善用户体验;(2) 代码补充(实时性要求高);(3) 低并发场景(< 50 concurrent) 内存带宽差距大,收益明显──在以下场景应避免:(1) 批量离线生成延迟不重要,使用平面目标;(2) 短输出< 50 tokens) 草案 开销和验证成本主导;(3) 专业领域无领域训练的草案) alpha 太;(4) vLLM v0.18.0 + 草案-model + 零碎-pre-model + 组合 不兼容──

> **【拓展：vLLM 推测解码配置】**VLLM V1 支持三种推测解码模式:(1) Draft model传统小模型作为草案,与零碎预填不兼容;(2) EAGLE在隐状态训练的草案头,推用于通用场景;(3) N-gram GPU基于提示 中 N-gram 查找的 GPU端草案,是唯一与零碎预填 兼容的模式──`speculative_config`必須明顯設定,vLLM默认不開任何推测解码──

- Geração offline de lote 1, onde a latência não importa.
  O método de produção de um produto é o método de produção de um produto.
- Os resultados são muito curtos (menos de 50 tokens).
  Tradução do inglês: very short of output ((50 tokens 以下) 』
- Domínios especializados sem um chefe de recrutamento treinado.
  Não há nenhum campo de treinamento de chefe de projeto.
- vLLM v0.18.0 + código de especificações do modelo de projeto + `--enable-chunked-prefill`Esta combinação não compila. A exceção documentada é o N-gram GPU especificação decodificação em V1.
  中文翻译:vLLM v0.18.0 + modelo de projeto 推测解码 + `--enable-chunked-prefill` Este conjunto não pode ser editado  Documentos exceção é N-gram GPU em V1.

## Use-o com o framework implementado.
```figure
mx-speculative-tree
```

## Usá-lo

`code/main.py`Simula um ciclo de decodificação com e sem decodificação especulativa em uma gama de valores alfa e comprimentos de esboço K. Imprime o break-even alfa, o speedup medido e o comportamento da cauda.

> `code/main.py`模拟有/无推测解码的解码循环,覆盖一系列 alpha 值和草案 长度 K――它印印亏平衡 alpha、测量加速比和尾部行为──在多个 (alpha, K) 组合上运行,精确看推测解码在哪里停止收益──

## Envia-o . Produto .

Esta lição produz`outputs/skill-eagle3-rollout.md`. Tendo em conta um modelo-alvo, uma descrição da distribuição de tráfego e um alvo de simultâneo, produz um plano de implantação EAGLE-3 em fases  linha de referência, permite a configuração, a medida alfa, o gate em alfa >= 0,55, ver P99 ITL.

> 本课产 出 `outputs/skill-eagle3-rollout.md` dado modelo de objetivo  distribuição de fluxo e desenvolvimento de objetivos, gerando por fase EAGLE-3  lançamento de plano 基准基线、 ativar a configuração  medir alfa ̇ ̇ ̇ ̇ ̇ = 0,55  como controle de entrada ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇  ̇ ̇ ̇  ̇ ̇ ̇  ̇ ̇     ̇          ̇      ̇      ̇                                                                        

## Exercícios.

1. Corra .`code/main.py`Em K=5, qual alfa você precisa para um 2x aceleração? para um 3x aceleração?
   Tradução: 运行`code/main.py`O que é que é o "verificar" sobre-carga?
2. Imagine que o tráfego de produção divide 70% de chat geral, 30% de código. Chat geral atinge alfa 0,7 com EAGLE-3 treinado no ShareGPT; código atinge alfa 0,4. O que é alfa misturado e o código de especificação é net-positivo?
   Chinese Language Translation:假设生产流量 70% 通用聊天,30% 代码──通用聊天 alfa 0.7,代码 alfa 0.4──混合 alfa 是多少,推测解码是否净正向?
3. Leia o VLLM `speculative_config`A documentação: nomear os três modos (modelo de projeto, EAGLE, N-gram) e qual é compatível com preenchimento em pedaços.
   Tradução do português:`speculative_config`文档──说出三种模式(projeto modelo、EAGLE、N-gram)及哪个与分块预填兼容──
4. Veja a baixa média do ITL de 25% depois de habilitar a EAGLE-3, mas o P99 ITL subiu 15%.
   O nível de TI em relação ao nível de TI é de 25% abaixo, mas o P99 ITL é de 15% acima.
5. Calcule o custo de memória da cabeça de projeto EAGLE-3 para Llama 3.3 70B. Como se compara a executar Llama 3.2 1B como um projeto clássico?
   Tradução do inglês para tradução do inglês: calcula Llama 3.3 70B de EAGLE-3

## Termos-chave .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| Speculative decoding | "draft plus verify" / "draft 加验证" | Propose K tokens with a cheap model, verify all K in one target forward / 用廉价模型提议 K 个 token，一次目标前向验证所有 K 个 |
| Acceptance rate alpha | "spec accept rate" / "推测接受率" | Fraction of draft tokens accepted by the target; the only metric that matters / 被 target 接受的 draft token 比例；唯一重要的指标 |
| Draft length K | "spec k" / "推测 K" | How many tokens the draft proposes per target forward; typical 4-8 / 每次 target 前向 draft 提议多少 token；通常 4-8 |
| Verify overhead epsilon | "spec overhead" / "推测开销" | Extra cost to verify-and-reroll vs a plain target forward; grows with batch / 验证+重新生成 vs 普通 target 前向的额外成本；随 batch 增长 |
| EAGLE-3 | "latest EAGLE" / "最新 EAGLE" | 2025-2026 variant; trains draft head on multiple target layers; alpha 0.6-0.8 / 2025-2026 变体；在多个 target 层上训练 draft head |
| `speculative_config` | "vLLM spec config" / "vLLM 推测配置" | The explicit opt-in in vLLM V1; no default means no acceleration / vLLM V1 中的显式 opt-in；无默认即无加速 |
| N-gram spec decode | "N-gram draft" / "N-gram draft" | GPU-side draft using N-gram lookups in the prompt; chunked-prefill-compatible / GPU 端使用 prompt 中 N-gram 查找的 draft；与分块预填充兼容 |
| Break-even alpha | "no-op alpha" / "无效果 alpha" | Alpha at which spec decode gives zero speedup; watch this at production concurrency / 推测解码零加速的 alpha；在生产并发下关注 |
| Rejected-draft two-pass | "reroll cost" / "重新生成成本" | Two target forwards when drafts reject; drives P99 tail / draft 被拒绝时的两次 target 前向；驱动 P99 尾部 |

## Mais leitura 延伸阅读

- [vLLM — Speculative Decoding docs](https://docs.vllm.ai/en/latest/features/spec_decode/) fonte autorizada em `speculative_config`e compatibilidade de preenchimento em pedaços no V1.
- [vLLM Speculative Config API](https://docs.vllm.ai/en/latest/api/vllm/config/speculative/) o conjunto exato de campos.
- [EAGLE paper (arXiv:2401.15077)](https://arxiv.org/abs/2401.15077) formulação original da cabeçalha de projecto da EAGLE.
- [EAGLE-2 paper (arXiv:2406.16858)](https://arxiv.org/abs/2406.16858) Esboços e árvores adaptáveis.
- [UC Berkeley EECS-2025-224](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-224.html) Sistema de Mestrado em Direito e Direito Executivo e decodificação especulativa.
- [BentoML — Speculative Decoding](https://bentoml.com/llm/inference-optimization/speculative-decoding) Lista de verificação da implantação da produção.
