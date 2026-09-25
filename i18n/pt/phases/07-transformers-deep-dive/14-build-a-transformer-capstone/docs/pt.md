# Construir um Transformador a partir do zero  A Capstone  Desde zero construir Transformador                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

> Trinta lições, um modelo, sem atalhos.

> **【中文解读】**Integra todos os conhecimentos, desde zero realizando a estrutura completa do GPT.

**Type:** Hands-on | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 7 · 01 through 13. Don't skip. | **前置知识:** Phase 7 · 01 through 13. Don't skip.
**Time:** ~120 minutes | **时间:** ~120 分钟

## O problema é o problema da introdução

Já leu todos os artigos, implementou atenção, divisões de várias cabeças, codificações posicionais, blocos de codificação e decodificação, perdas de BERT e GPT, MoE, cache KV. Agora faça com que trabalhem juntos em uma tarefa real.

> Você já leu cada artigo. Você conseguiu a atenção, muitas divisões, codificação de localização, codificadores e codificadores blocos, BERT e GPT perda, MOE, KV, cache. Agora deixe-os trabalhar em conjunto em uma tarefa real.

A pedra angular: treinar um pequeno transformador de end-to-end apenas para um decodificador em uma tarefa de modelagem de linguagem de nível de personagens. Ele lê Shakespeare. Ele gera novo Shakespeare. É pequeno o suficiente para treinar em um laptop em menos de 10 minutos. É correto o suficiente que trocar um conjunto de dados maior e treinamento mais longo lhe dá um LM real.

> 毕业项目: 在字符级语言建模任务上端到端训练一个小型解码器专用变压器──它读取莎士比亚,生成新的莎士比亚──它足够小,可以在笔记本上完成10分钟内训练──它足够正确,换成更大的数据集和更长的训练时间就能得到真正的语言模型──

Este é o "nanoGPT" do curso. Não é original. O tutorial de 2023 de Karpathy é a implementação de referência que cada aluno escreve pelo menos uma vez. Levamos a forma e reformula-a em torno do que cobrimos.

> É o "nanoGPT" do curso. Não é o original. O "Karpathy 2023" é um programa de nanoGPT que todos os alunos escrevem pelo menos uma vez para realizar.

> **【中文解读】**Este programa de formação irá integrar todos os conhecimentos do curso: configuração de linguagem de código-fonte, localização de código-fonte, RMSNorm, atenção para as causas, SwiftGLU FFN, ligação de defeitos, treinamento de um Shakespeare produtor que pode ser concluído em 10 minutos no seu bloco de notas, embora pequeno, mas a estrutura é o mesmo que o GPT-4, aumentando o volume de dados e treinamento para obter um modelo de linguagem real.

> **【拓展：从 nanoGPT 到生产级 LLM】**O nanoGPT da Karpathy é o melhor ponto de partida para aprender o Transformer. A diferença fundamental entre nanoGPT e nível de produção do LLM é: tamanho de dados, de MB a TB, infraestrutura de treinamento, de GPUs simples a milhares de GPUs, treinamento distribuído, de dados e de modelos, de fluxo de água e de fluxo de água, bem como treinamento posterior, mas a estrutura central é a mesma.

## O conceito central.

![Transformer-from-scratch block diagram](../assets/capstone.svg)

A arquitetura, com notas:

> 架构,带注释:

```
input tokens (B, N)
   │
   ▼
token embedding + positional embedding  ◀── Lesson 04 (RoPE option)
   │
   ▼
┌──── block × L ────────────────────┐
│  RMSNorm                          │  ◀── Lesson 05
│  MultiHeadAttention (causal)      │  ◀── Lesson 03 + 07 (causal mask)
│  residual                         │
│  RMSNorm                          │
│  SwiGLU FFN                       │  ◀── Lesson 05
│  residual                         │
└────────────────────────────────── ┘
   │
   ▼
final RMSNorm
   │
   ▼
lm_head (tied to token embedding)
   │
   ▼
logits (B, N, V)
   │
   ▼
shift-by-one cross-entropy            ◀── Lesson 07
```

### O que enviamos

> Nós entregamos o conteúdo:

- `GPTConfig` um local para a configuração de todos os hiperparâmetros.
  Tradução:`GPTConfig` Um local de configuração de todos os superparâmetros.
- `MultiHeadAttention` Causal, batch, com caminho opcional de estilo Flash (PyTorch's `scaled_dot_product_attention`)).
  Tradução:`MultiHeadAttention` 因果的、批量,可选闪光 风格路径(PyTorch 的 `scaled_dot_product_attention`)。
- `SwiGLUFFN` FFN moderno.
  Tradução:`SwiGLUFFN` 现代 FFN。
- `Block` Atenção pré-norma, embalada residual + FFN.
  Tradução:`Block`                                                                                                                                                                                                                                                              
- `GPT` embutidos, blocos empilhados, cabeçalho LM, gerar().
  Tradução:`GPT` 嵌入、堆叠块、LM 头、generate()
- Localização com AdamW, cosino LR, corte de gradiente.
  Tradução do inglês para o português:带 AdamW、余弦学习率、梯度裁剪的训练循环──
- Tokenizer de nível Char sobre textos de Shakespeare.
  Tradução do inglês: Shakespeare 文本上的字符级分词器──

> **【中文解读】** completa GPT  implementação contém: configuração 多头因果注意力(可选 Flash Attention) ✓ SwiGLU FFN、前归归化残差块、 completa GPT 模型类型(嵌入 + 堆叠块 + LM 头 + 生成函数) ✓ AdamW + 余弦学习率 练习循环── 简洁的说法, utilizou learn式位置嵌入(而不是 RoPE) 没有实现 KV 缓存,但练习要求你添加这些──

### O que não enviamos

> Nós não entregamos conteúdo:

- RoPE  implementado conceitualmente na lição 04. Aqui usamos embutimentos posicionais aprendidos para simplicidade.
  Em seu livro, o professor de ciências da área de pesquisa, o professor de ciências da área de pesquisa, o professor de ciências da área de pesquisa, o professor de ciências da área de pesquisa, o professor de ciências da área de pesquisa, o professor de ciências da área de pesquisa e ciências da área de pesquisa, o professor de ciências da área de pesquisa, o professor de ciências da área de pesquisa, o professor de ciências da área de pesquisa, o professor de ciências da área de pesquisa, o professor de ciências da área de pesquisa e ciências da área de pesquisa, o professor de ciências da área de pesquisa, o professor de ciências da área de pesquisa, o professor de ciências da área de ciência e da área de pesquisa, o professor de ciência da área de ciência e da área de ciência, o professor de ciência da área de ciência e da área de ciência, o professor de ciência e do professor de ciência da área de ciência, o professor de ciência da área de ciência e da área de ciência, o professor de ciência e do professor de ciência, o professor de ciência e do professor de ciência da área de ciência, o professor de ciência, o professor de ciência e do professor de ciência, o professor de ciência e do professor de ciência, o professor de ciência, o professor de ciência e do professor de ciência, o professor de ciência, etc.
- O cache KV durante a geração  cada passo de geração recalcula a atenção sobre o prefixo completo. Mais lento, mas mais simples. Os exercícios pedem que você adicione um cache KV.
  Tradução do inglês para o inglês: KV 缓存  Cada passo de produção para o preâmbulo completo re-computação atenção.
- Atenção Flash  PyTorch 2.0+ auto-dispatches se as entradas coincidem; usamos `F.scaled_dot_product_attention`- Não .
  Tradução do inglês:Flash Attention  PyTorch 2.0+ 在输入匹配时自动分派;我们使用 `F.scaled_dot_product_attention`- Não.
- MoE  FFN único por bloco.
  Tradução do português: MoE  Cada bloco de FFN.

### Metricas de metas

Em um laptop Mac M2, um laptop de 4 camadas, 4 cabeças, d_model=128 GPT treinado para 2.000 passos em `tinyshakespeare.txt`- Não .

> Em Mac M2 笔记本上,4 层、4 头、d_model=128 de GPT em `tinyshakespeare.txt`上训练 2000 步:

- A perda de treino converge de ~ 4,2 (aleatório) para ~ 1,5 em cerca de 6 minutos.
  Tradução do inglês: training loss from about 4.2 (随机) in about 6 minutes in receipt to about 1.5 (trenagem perdida de cerca de 4,2 (随机) em cerca de 6 minutos em receção para cerca de 1,5 (trenagem perdida de cerca de 4,2 (随机) 随机)
- A produção amostrada parece em forma de Shakespeare: palavras arcaicas, interrupções de linha, nomes próprios como "ROMEO:" surgem.
  O que é que é o nome de um personagem?
- A perda de valor (a última 10% do texto não recebida) acompanha de perto a perda de formação; não há sobreajuste neste tamanho/orçamento.
  O resultado foi o resultado da avaliação de desempenho de um grupo de estudantes.

> **【拓展：从字符级到子词级 Tokenizer】**Este projeto usa símbolo de classe tokenizer (BPE) (ou seja, para o uso de um símbolo de classe BPE, GPT-4), para obter um equilíbrio entre o volume de palavras, a duração de sequências e a grafia de palavras, é o padrão moderno do LLM.

## Construí-lo e realizei-o.
```figure
n5-block-stack
```

## Construí-lo

Esta aula usa PyTorch.`torch`(Construção do CPU está bem).`code/main.py`O roteiro diz:

> 本课使用 PyTorch──安装 `torch`(CPU 版本即可)`code/main.py`❖ O que é esse livro:

- Descarga`tinyshakespeare.txt`se faltarem (ou se estiverem a ler uma cópia local).
  Tradução do português:`tinyshakespeare.txt`(或读取本地副本)
- Tokenizer de carros de nível byte.
  Tradução do inglês:
- Trem/val dividido em 90/10.
  Tradução do inglês: 90/10
- Loop de treinamento com bf16 autocast no hardware suportado.
  Tradução do inglês: Support Hardware on bf16
- A amostragem após o treino termina.
  Tradução do inglês: training completed后的采样.

### Passo 1: dados

```python
text = open("tinyshakespeare.txt").read()
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
encode = lambda s: [stoi[c] for c in s]
decode = lambda xs: "".join(itos[x] for x in xs)
```

65 caracteres únicos, pequeno vocabulário, cabe a um tamanho de 4 bytes, sem BPE, sem drama de tokenizer.

> 65 个唯一字符──微型词表──适配 4 字节 vocab_size──没有 BPE,没有分词器的麻烦──

### Passo 2: modelo

Veja .`code/main.py`O bloco é um livro de texto da lição 05  pré-norma, RMSNorm, SwiGLU, MHA causal.

> 参见 `code/main.py`◊ Este bloco é um dos livros do curso 05                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

### Passo 3: ciclo de treinamento

Obter um lote aleatório de janelas de tokens de comprimento 256, para frente, transmissão por entropia, para trás, passo AdamW, registro, repetição.

> 获取随机批量长度为 256 的标题窗口──前向传播──偏移一位的交叉──反向传播──AdamW 步进──记录──重复──

```python
for step in range(max_steps):
    x, y = get_batch("train")
    logits = model(x)
    loss = F.cross_entropy(logits.view(-1, vocab_size), y.view(-1))
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    opt.zero_grad()
```

### Passo 4: amostra

Dado um pedido, repetidamente encaminhado, amostra de logits top-p, anexe, e continuar.

> 给定一个提示,反复前向传播, de top-p logits 采样,追加,继续──500 个标志 后停止──

### Passo 5: ler a saída

Depois de 2.000 passos:

> 2000 步后:

```
ROMEO:
Away and mild will not thy friend, that thou shalt wit:
The chief that well shame and hath been his friends,
...
```

Não é Shakespeare, mas em forma de Shakespeare, uma vitória clara por 800 mil parâmetros e 6 minutos num laptop.

> Não é Shakespeare, mas como Shakespeare, cerca de 800 mil números no bloco de notas de 6 minutos.

## Use-o com o framework implementado.

Esta pedra-chave é uma arquitetura de referência.

> Este projeto é uma estrutura de referência.

1. **Swap the tokenizer.**Utilize BPE (por exemplo `tiktoken.get_encoding("cl100k_base")`O tamanho da vocab aumentou de 65 para 50 mil.
   Tradução:**替换分词器。**Utilize BPE`tiktoken.get_encoding("cl100k_base")`)──词表大小 65 跳到约50,000──模型容量需要相应扩展──
2. **Train on a bigger corpus.**Utilização`OpenWebText`ou `fineweb-edu`10B tokens em um único A100 leva cerca de 24 horas para um GPT de 125M-param.
   Tradução:**在更大的语料上训练。**Utilização `OpenWebText`Ou `fineweb-edu`(HuggingFace) ・・・在单张 A100 上用10B token 训练 125M 参数 GPT 约需24小时──
3. **Add RoPE + KV cache + Flash Attention.**Os exercícios abaixo vão guiá-lo através de cada um.
   Tradução:**添加 RoPE + KV 缓存 + Flash Attention。**O exercício abaixo irá guiá-lo a completar cada passo.

Isto acaba como um GPT de 125M que gera inglês fluente. Não é um modelo de fronteira. Mas o mesmo caminho de código  apenas maior  é o que Karpathy, EleutherAI e o Instituto Allen usam para treinar pontos de controle de pesquisa em 2026.

> Finalmente, obtemos um que possa gerar um fluido Inglês de 125M GPT. Não é um modelo de vanguarda. Mas o mesmo código de rotação é apenas maior.

> **【拓展：Karpathy 的 nanoGPT 与教育意义】**O nanoGPT de Andrej Karpathy ((2023) é um dos ensinamentos mais influentes da história da educação de IA. Ele provou um GPT completo e treinável que pode ser realizado com cerca de 300 layers de PyTorch. Este método de ensino "desde zero construção" faz com que você realmente entenda o papel de cada componente, em vez de transformar o transformador em uma caixa negra.

## Envia-o . Produto .

Veja .`outputs/skill-transformer-review.md`A habilidade revisa uma implementação transformadora a partir do zero para verificar a correcção em todas as 13 lições anteriores.

> 参见 `outputs/skill-transformer-review.md` Esta habilidade   revistar uma transformação de construção de zero                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

## Exercícios.

1. **Easy.**Corra .`code/main.py`Verifique se a perda de validação da fase final do modelo treinado é inferior a 2.0. Mudança `max_steps`De 2.000 a 5.000 , a perda de val continua a melhorar?
   Tradução: 运行`code/main.py` Verificar que o nível final do modelo de treinamento é inferior a 2,0 `max_steps`A perda de certificados de 2000 para 5000?
2. **Medium.**Substitua as inserções posicionais aprendidas com RoPE. Aplique a rotação para Q e K dentro `MultiHeadAttention`A perda de val é pelo menos tão baixa.
   Tradução do inglês: using RoPE 替换学习式位置嵌入──在 `MultiHeadAttention`O que é o problema é que o processo de produção de produtos não é um processo de produção de produtos não-produtivos.
3. **Medium.**Implementar um cache KV no loop de amostragem. Gerar 500 tokens com e sem cache. O relógio de parede deve melhorar em 520x em um laptop.
   Tradução do inglês: In the sampling cycle, KV 缓存──有缓存和无缓存── produz 500 tokens──笔记本应该有5-20 倍的实际时间改善──
4. **Hard.**Adicione uma segunda cabeça ao modelo que prevê o próximo token mais um (MTP  Multi-Token Prediction de DeepSeek-V3). Treinar em conjunto.
   Chinese: 添加第二个头预测 下一个代币MTP 来源: DeepSeek-V3 的多代币预测)
5. **Hard.**Substitua o único FFN por bloco por um MoE de 4 especialistas. Roteador + roteamento top-2. Veja como a perda de val muda em parâmetros ativos correspondentes.
   Chinese Translation:将每块的单个FFN 替换为4 专家 MoE──路由器 + top-2 路由──观察在匹配活跃参数下验证损失的变化──

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| nanoGPT | "Karpathy's tutorial repo" | Minimal decoder-only transformer training code, ~300 LOC; the canonical reference. |
| nanoGPT | "Karpathy 的教程仓库" | 最小解码器专用 Transformer 训练代码，约 300 行；经典参考。 |
| tinyshakespeare | "The standard toy corpus" | ~1.1 MB of text; every character-LM tutorial since 2015 uses it. |
| tinyshakespeare | "标准玩具语料库" | 约 1.1 MB 文本；自 2015 年以来每个字符级语言模型教程都用它。 |
| Tied embeddings | "Share input/output matrix" | LM head weight = transpose of token embedding matrix; saves parameters, improves quality. |
| 绑定嵌入 | "共享输入/输出矩阵" | LM 头权重 = token 嵌入矩阵的转置；节省参数，提高质量。 |
| bf16 autocast | "Training precision trick" | Run forward/back in bf16, keep optimizer state in fp32; standard since 2021. |
| bf16 自动混合精度 | "训练精度技巧" | 前向/反向用 bf16，优化器状态用 fp32；2021 年以来的标准。 |
| Gradient clipping | "Stops spikes" | Cap global grad norm at 1.0; prevents training blowups. |
| 梯度裁剪 | "阻止尖峰" | 将全局梯度范数限制在 1.0；防止训练爆炸。 |
| Cosine LR schedule | "The 2020+ default" | LR ramps up linearly (warmup) then decays cosine-shaped to 10% of peak. |
| 余弦学习率调度 | "2020+ 默认" | 学习率线性升温（warmup）然后余弦衰减到峰值的 10%。 |
| MFU | "Model FLOP Utilization" | Achieved FLOPs / theoretical peak; 40% dense, 30% MoE is strong in 2026. |
| MFU | "模型 FLOP 利用率" | 实际 FLOPs / 理论峰值；2026 年稠密 40%、MoE 30% 是好的。 |
| Val loss | "Held-out loss" | Cross-entropy on data the model never saw; overfit detector. |
| 验证损失 | "留出损失" | 模型从未见过的数据上的交叉熵；过拟合检测器。 |

## Mais leitura 延伸阅读

- [The Annotated Transformer (Harvard NLP)](https://nlp.seas.harvard.edu/annotated-transformer/) a aplicação clássica com anotações.
  Tradução do português: 哈佛 NLP 的注解版 Transformer,经典参考实现──
