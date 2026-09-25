# T5, BART  Modelos de codificação-decodificação.

> Os codificadores entendem. Os decodificadores geram. Coloquem-nos de novo juntos e você obtém um modelo construído para tarefas de entrada → saída: traduzir, resumir, reescrever, transcriver.

> **【中文解读】**T5 Colocar todas as tarefas de PNL 统一为文本格式  BART Use去噪自编码训练──适用于翻译、摘要等序列转换任务──

**Type:** Study | **类型:** 学习
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

GPT-só decodificador e BERT-só encodificador cada tira abaixo da arquitetura de 2017 para um objetivo diferente.

> 解码器专用 GPT 和编码器专用 BERT, por sua vez, para diferentes objetivos, precisou a estrutura de 2017 .

- Tradução: Inglês → Francês.
  Tradução do inglês para inglês:
- Resumo: 5.000 tokens artigo → 200 tokens resumo.
  中文翻译:摘要: 5.000 tokens 文章 → 200 tokens 摘要。
- Reconhecimento de fala: tokens de áudio → tokens de texto.
  Tradução do inglês: 文本 token
- Extração estruturada: prosa → JSON.
  Tradução do inglês: JSON.

Para estes, o encoder-decoder faz o ajuste mais limpo. O encoder produz uma representação densa da fonte. O decodador gera a saída, atendendo a essa representação em cada passo. O treinamento é de deslocamento por um no lado da saída. A mesma perda que o GPT, apenas condicionada à saída do encoder.

> Para estas tarefas, o codificador-descodificador é a escolha mais adequada. O codificador gerou fontes de densidade de expressão.

Dois artigos definiram o livro de jogos moderno:

> 两篇论文 define o moderno padrão:

1. **T5**(Raffel et al. 2019). "Transformador de Transferência de Texto para Texto". Cada tarefa de NLP reformulada como texto-in, texto-out. Arquitetura única, vocabulário único, perda única. Pretrainado em previsão de tempo mascarado (espaços corruptos na entrada, decodificá-los na saída).
   Tradução:**T5**(Raffel 等人,2019) ――"文本到文本迁移 Transformer"― cada tarefa de PNL é redefinida como文本输入文本输出―单一架构、单一词表、单一损失― utilizando os os dados de um módulo de previsão para realizar um pre-treinamento (破坏输入中的片段,解码它们在输出中)―
2. **BART**(Lewis et al. 2019). "Transformador bidirecional e auto-regressivo. " Denoising autoencoder: corrupto input de várias maneiras (misture, mascarar, excluir, girar), peça ao decodificador para reconstruir o original.
   Tradução:**BART**(Lewis 等人,2019) ――"双向自归变压器"──去噪自编码器:用多种方式破坏输入(打乱、掩码、删除、旋转),要求解码器重建原始文本──

Em 2026, o formato de codificador-decodificador continua a existir onde a estrutura de entrada importa:

> Em 2026, o formato de codificador-descodificador continua a existir em cenários importantes da estrutura de entrada:

- Suspirar (discurso → texto).
  中文翻译:Susparar(语音 → 文本) 』
- A pilha de traduções do Google.
  Tradução do idioma: Google's Translation System.
- Alguns modelos de complementação / reparação de código que têm estruturas de contexto e edição distintas.
  Alguns têm claramente em baixo- edição estruturas de código complementar / modificar modelos.
- Flan-T5 e variantes para tarefas de raciocínio estruturado.
  Tradução do português:Flan-T5  e seus variações, para tarefas de cálculo estrutural.

Só o decodificador ganhou o destaque, mas o decodificador nunca desapareceu.

> O modelo de descifrador especial ganhou a pole-light, mas o codificador-descifrador nunca desapareceu.

> **【中文解读】**编码器-解码器架构在"输入→输出"结构化任务中仍然有优势──T5 将所有 NLP 任务统一为文本格式,BART 用去噪音自编码训练──虽然在纯文本生成领域被仅被 Decoder 取代,但在语音识别(Whisper) 翻译、摘要等任务中仍然是最佳选择──

## O conceito central.

![Encoder-decoder with cross-attention](../assets/encoder-decoder.svg)

### O loop para a frente

```
source tokens ─▶ encoder ─▶ (N_src, d_model)  ──┐
                                                 │
target tokens ─▶ decoder block                   │
                 ├─▶ masked self-attention       │
                 ├─▶ cross-attention ◀───────────┘
                 └─▶ FFN
                ↓
              next-token logits
```

O encoder é executado de forma autoregressiva, mas atende a cada passo a *a mesma* saída do encoder.

> O chave é que o codificador para cada entrada só executa uma vez. O descifrador para cada entrada é automaticamente executado, mas em cada passo todos os outros estão preocupados com o mesmo.

> **【中文解读】**交叉注意力是编码器-解码器架构的信息桥梁:Q 来源编码器,K/V 来源编码器输出;;编码器只运行一次(高效),解码器每步都通过交叉注意力访问编码器的完整输出;;

> **【拓展：Whisper 的编码器-解码器设计】**O modelo de reconhecimento de som de Whisper da OpenAI usa uma estrutura de codificação de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de um sistema de reconhecimento de som de reconhecimento de um sistema de reconhecimento de som de som de um sistema de reconhecimento de reconhecimento de som de um sistema de reconhecimento de reconhecimento de som de um sistema de reconhecimento de reconhecimento de som de reconhecimento de um sistema de reconhecimento de reconhecimento de reconhecimento de reconhecimento de um sistema de reconhecimento de reconhecimento de reconhecimento de um sistema de reconhecimento de reconhecimento de reconhecimento de reconhecimento de um sistema de reconhecimento de reconhecimento de reconhecimento de um sistema de reconhecimento de reconhecimento de reconhecimento de um sistema de reconhecimento de reconhecimento de reconhecimento de reconhecimento de reconhecimento de um sistema de reconhecimento de reconhecimento de reconhecimento de reconhecimento de um sistema de reconhecimento de reconhecimento de reconhecimento de reconhecimento de texto de texto de texto de texto de texto de texto de um sistema de texto de texto de texto de texto de texto de um sistema de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de texto de

### T5 Pre-treino  Corrupção de tempo

Escolha intervalos aleatórios da entrada (longoia média de 3 tokens, 15% total).`<extra_id_0>`- Não .`<extra_id_1>`, etc. O decodificador só sai os espaços corruptos com o seu prefixo sentinela:

> 随机选择输入中的片段(平均长度 3 个标志,总计 15%) ―― usando um único marcador de posto para substituir cada um dos segmentos:`<extra_id_0>`- Não.`<extra_id_1>`É só para fazer um vídeo de um episódio destruído e para o seu posto de comando.

```
source: The quick <extra_id_0> fox jumps <extra_id_1> dog
target: <extra_id_0> brown <extra_id_1> over the lazy
```

O sinal é mais barato do que prever toda a sequência.

> Em experimentos de dissipação do T5 论文, a concorrência é equivalente com a MLM (BERT) e a anterior LM (UniLM).

### BART pré-treino  denotação de ruído múltipla

O BART experimenta cinco funções sonoras:

> BART 尝试五种噪声函数:

1. Mascaragem de tokens.
   Tradução do português:Token 掩码.
2. - A eliminação de tokens.
   Tradução do português:Token 删除。
3. Infiltramento de texto (mascarar um espaço, inserir o decodificador o comprimento certo).
   Tradução do inglês: 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文本填充, 文码器插入正确长度, 解码器插入正确长度, 藏藏藏, 藏藏藏藏, 藏藏藏藏, 藏藏藏, 藏藏藏, 藏藏藏, 藏, 藏藏藏, 藏, 藏藏, 藏, 藏, 藏, 藏, 藏, 藏, 藏, 藏, 藏, 藏, 藏, 藏
4. Permutação de frases.
   Tradução do português:句子排列──
5. - A rotação de documentos.
   Tradução do português:文档旋转──

Combinando o enchimento de texto + permutação de frase produziram os melhores números a jusante. O decodificador sempre reconstitui o original. A saída do BART é a sequência completa, não apenas os intervalos corrompidos , portanto, o cálculo pré-treinamento é maior que T5.

> 组合文本填充 + 句子排列产生最佳下游效果──解码器总是重建原文本──BART's output is a complete sequence, not just a broken fragment

> **【中文解读】**T5 和 BART 预训策略不同:T5 间隔腐败只预测被破坏的片段(高效),BART 脱噪自编码重建整个序列(更彻底但更贵) ――选择取决于任务T5 更适合抽取任务,BART 更适合抽取任务──

### Inferência

A mesma geração autoregressiva que a GPT. Aplica-se amostragem gananciosa / feixe / top-p. Buscar feixe (largura 45) é padrão para tradução e resumo porque a distribuição de saída é mais estreita do que o chat.

> 推理与 GPT的自归生成相同──贪心/束搜索/top-p 采样都适用──束搜索(宽度 4-5) é uma estratégia padrão de tradução e resumo, pois a distribuição de output é menor do que o diálogo──

> **【拓展：Beam Search 在翻译中的重要性】**编码器-解码器模型在翻译和摘要任务中常用束搜索 (BAMS) 宽度 4-5),因为输出分布较窄. Beam search 维护多个候选序列,每步保留得分最高的几个继续扩展──相比贪心搜索,beam search 能找到更优的全局序列;相比随机采样,它更稳定──在对话生成中通常不需要束搜索,因为输出分布更广──

### Quando escolher cada variante em 2026

| Task | Encoder-decoder? | Why |
|------|------------------|-----|
| 任务 | 是否用编码器-解码器？ | 原因 |
| Translation | Yes, usually | Clear source sequence; fixed output distribution; beam search works |
| 翻译 | 通常是 | 明确的源序列；固定的输出分布；束搜索有效 |
| Speech-to-text | Yes (Whisper) | Input modality differs from output; encoder shapes audio features |
| 语音转文本 | 是（Whisper） | 输入模态与输出不同；编码器处理音频特征 |
| Chat / reasoning | No, decoder-only | No persistent "input" — the conversation is the sequence |
| 对话/推理 | 否，解码器专用 | 没有持久的"输入"——对话本身就是序列 |
| Code completion | Usually no | Decoder-only with long context wins; code models like Qwen 2.5 Coder are decoder-only |
| 代码补全 | 通常否 | 带长上下文的解码器专用胜出；Qwen 2.5 Coder 等代码模型是解码器专用 |
| Summarization | Either works | BART, PEGASUS beat earlier decoder-only baselines; modern decoder-only LLMs match them |
| 摘要 | 都可以 | BART、PEGASUS 超越早期解码器专用基线；现代解码器专用 LLM 能匹配它们 |
| Structured extraction | Either | T5 is clean because "text → text" absorbs any output format |
| 结构化提取 | 都可以 | T5 很干净，因为"文本 → 文本"可以吸收任何输出格式 |

A tendência desde ~2022: apenas o decodificador assume as tarefas que o encodificador-decodificador costumava possuir porque (a) os LLM apenas com decodificador sintonizados por instrução se generalizam para qualquer coisa através de solicitações, (b) uma arquitetura escala mais fácil do que duas, (c) a RLHF assume um decodificador.

> Desde 2022 tendências: o decodificador especial assumiu tarefas que o codificador-decodificador já possuía, pois (a) a instrução de decodificador especial LLM  através de sugestões pode ser generalizada para qualquer tarefa, (b) uma única estrutura é mais fácil de expandir do que duas, (c) RLHF 假设使用解码器──编码器-解码器在输入模态不同语音、图像) 或束搜索质量重要时仍然有用──

> **【拓展：T5 的 text-to-text 统一范式】**T5 核心理念是将所有 NLP 任务统一为"文本输入→文本输出"格式──翻译:"traduir Inglês para Francês: Hello → Bonjour";分类:"sentimento: Este filme é ótimo → positivo"──这种统一简化了架构和训练流程,也后来指示调和快速工程的思想源头──Flan-T5 更是通过指令微调大幅提升了零样本能力──

## Construí-lo e realizei-o.
```figure
encoder-decoder
```

## Construí-lo

Veja .`code/main.py`Implementamos a corrupção de tempo de estilo T5 para um corpus de brinquedos. A peça mais útil desta lição porque aparece em todas as receitas de pré-treino de codificadores-decodificadores desde então.

> 参见 `code/main.py` Nós realizamos o T5 风格的片段破坏 é a parte mais útil desta aula, pois aparece em cada programa de treinamento de programadores-descodificadores subsequentes.

### Passo 1: Corrupção de expansão

```python
def corrupt_spans(tokens, mask_rate=0.15, mean_span=3.0, rng=None):
    """Pick spans summing to ~mask_rate of tokens. Return (corrupted_input, target)."""
    n = len(tokens)
    n_mask = max(1, int(n * mask_rate))
    n_spans = max(1, int(round(n_mask / mean_span)))
    ...
```

O formato-alvo é a convenção T5: `<sent0> span0 <sent1> span1 ...`A entrada corrompida interliga tokens inalterados com os tokens sentinela em locais de intervalo.

> 目標格式遵循 T5 约定:`<sent0> span0 <sent1> span1 ...` Introdução do objeto destruído será um token inalterado com um token de posto de serviço 交替排列──

### Passo 2: Verificação de ida e volta

Considerando a entrada e o alvo corruptos, reconstruir a frase original. Se a sua corrupção é reversível, o pass forward é bem definido. Esta é uma verificação de sanidade  treinamento real nunca faz isso, mas o teste é barato e pega bugs de um por um em sua contabilidade de tempo.

> 给定被破坏的输入和目标,重建原始句子──如果破坏是可逆的,前向传播就是良定义的──这是一个合理性检查真实训练从不这样做,但测试成本低且能发现片段簿记中的差一错──

### Passo 3: Barulho BART

Cinco funções: `token_mask`- Não .`token_delete`- Não .`text_infill`- Não .`sentence_permute`- Não .`document_rotate`Compõem dois deles e mostrem o resultado.

> 五个函数:`token_mask`- Não.`token_delete`- Não.`text_infill`- Não.`sentence_permute`- Não.`document_rotate`◊ 组合其中两个并显示结果──

## Use-o com o framework implementado.

Referência em "CoggingFace":

> AbraçosFace 参考:

```python
from transformers import T5ForConditionalGeneration, T5Tokenizer
tok = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

inputs = tok("translate English to French: Attention is all you need.", return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=32)
print(tok.decode(out[0], skip_special_tokens=True))
```

O truque T5: o nome da tarefa entra no texto de entrada. O mesmo modelo lida com dezenas de tarefas porque cada tarefa é de texto-in, texto-out. Em 2026 este padrão foi generalizado por modelos de decodificador-só com sintonia de instruções, mas T5 codificou-o primeiro.

> T5 técnicas: nome de tarefa escrito em texto de entrada. O mesmo modelo pode processar dezenas de tarefas, pois cada tarefa é de entrada de texto-exportação de texto. Em 2026, este modelo foi ordenado para que o módulo de código de código de pequeno modo fosse generalizado, mas T5 foi o primeiro a regulamentá-lo.

## Envia-o . Produto .

Veja .`outputs/skill-seq2seq-picker.md`. A habilidade escolhe entre codificador-decodificador e decodificador apenas para uma nova tarefa dada estrutura de entrada-saída, latência e metas de qualidade.

> 参见 `outputs/skill-seq2seq-picker.md` Esta habilidade, de acordo com a estrutura de entrada-saída 、 atraso e objetivos de qualidade, é utilizada para escolher uma estrutura especial de codificadores-descódigos ou de descódigos para novas tarefas.

## Exercícios.

1. **Easy.**Corra .`code/main.py`, aplicar a corrupção de intervalos para uma frase de 30 tokens, verificar que a concatenagem dos tokens fonte não sentinel com os intervalos de destino decodificados reproduza o original.
   Tradução: 运行`code/main.py`, para um token de 30 palavras aplicadas, destruição, verificação será não-tropa fonte token e o código de código de código objetivo
2. **Medium.**Implementar o BART `text_infill`ruído: substituir os intervalos aleatórios por um único `<mask>`O decodificador deve inferir o comprimento de tempo correto mais conteúdo. Mostre um exemplo.
   Tradução do português: implementar BART `text_infill`噪声: Use singles `<mask>`Para que o código seja alterado, o dispositivo deve determinar a duração e o conteúdo do vídeo.
3. **Hard.**- A música é perfeita .`flan-t5-small`Em um pequeno corpus inglês → porco-latino (200 pares).`Llama-3.2-1B`sobre os mesmos dados com o mesmo cálculo.
   中文翻译:在小型英语 → Porco Latin 语料库(200对) 上微调 `flan-t5-small` 50 em restantes, em conjunto com as medidas BLEU, porcentagem.`Llama-3.2-1B`Comparado.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Encoder-decoder | "Seq2seq transformer" | Two stacks: bidirectional encoder for input, causal decoder with cross-attention for output. |
| 编码器-解码器 | "Seq2seq Transformer" | 两个堆栈：双向编码器处理输入，带交叉注意力的因果解码器生成输出。 |
| Cross-attention | "Where source talks to target" | Decoder's Q × encoder's K/V. The only place encoder information enters the decoder. |
| 交叉注意力 | "源与目标对话的地方" | 解码器的 Q × 编码器的 K/V。编码器信息进入解码器的唯一通道。 |
| Span corruption | "T5's pretraining trick" | Replace random spans with sentinel tokens; decoder outputs the spans. |
| 片段破坏 | "T5 的预训练技巧" | 用哨兵 token 替换随机片段；解码器输出这些片段。 |
| Denoising objective | "BART's game" | Apply a noise function to the input, train the decoder to reconstruct the clean sequence. |
| 去噪目标 | "BART 的游戏" | 对输入应用噪声函数，训练解码器重建干净序列。 |
| Sentinel token | "The `<extra_id_N>` placeholder" | Special tokens that tag corrupted spans in the source and re-tag them in the target. |
| 哨兵 token | "`<extra_id_N>` 占位符" | 在源端标记被破坏片段、在目标端重新标记的特殊 token。 |
| Flan | "Instruction-tuned T5" | T5 fine-tuned on >1,800 tasks; made encoder-decoder competitive at instruction-following. |
| Flan | "指令微调的 T5" | 在 1,800+ 任务上微调的 T5；使编码器-解码器在指令遵循方面具有竞争力。 |
| Beam search | "Decoding strategy" | Keep top-k partial sequences at each step; standard for translation/summarization. |
| 束搜索 | "解码策略" | 每步保留得分最高的 k 个部分序列；翻译/摘要的标准策略。 |
| Teacher forcing | "Training-time input" | During training, feed the true previous output token to the decoder, not the sampled one. |
| Teacher forcing | "训练时输入" | 训练时向解码器输入真实的上一个输出 token，而非采样的 token。 |

## Mais leitura 延伸阅读

- [Raffel et al. (2019). Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683)- T5.
  Tradução do português:T5
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.13461)- BART.
  Tradução do português:BART
- [Chung et al. (2022). Scaling Instruction-Finetuned Language Models](https://arxiv.org/abs/2210.11416)- Flan-T5.
  Tradução do português:Flan-T5
- [Radford et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) Whisper, o codificador-decodificador canônico de 2026.
  Chinese:Whisper 论文, 2026 典型编码器-解码器模型──
- [HuggingFace `modeling_t5.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/t5/modeling_t5.py) execução de referência.
  中文翻译:HuggingFace T5 参考实现。
