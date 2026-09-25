# Sequência a Sequência Modelos .

> Dois RNNs fingindo ser tradutores, o gargalo de engarrafamento que atingiram é a razão pela qual existe atenção.
>  Dois RNN 假装是翻译器──它们遇到的瓶正是注意力机械存在的原因──

> **【中文解读】**O mecanismo de atenção é o de resolver o seu problema e foi inventado.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 08 (CNNs + RNNs for Text), Phase 3 · 11 (PyTorch Intro) | **前置知识:** Phase 5 · 08（CNN 和 RNN 文本处理），Phase 3 · 11（PyTorch 入门）
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

A classificação mapeia uma sequência de comprimento variável para um único rótulo. A tradução mapeia uma sequência de comprimento variável para outra sequência de comprimento variável. A entrada e saída vivem em diferentes vocabulários, possivelmente em idiomas diferentes, sem garantia de paridade de comprimento.

> 分类将变长序列映射为单标. 译文将变长序列映射为另一个变长序列.

A arquitetura seq2seq (Sutskever, Vinyals, Le, 2014) rompeu isso com uma receita deliberadamente simples. Dois RNNs. Um lê a frase fonte e produz um vetor de contexto de tamanho fixo. O outro lê esse vetor e gera o token da frase alvo por token. O mesmo código que você escreveu para a lição 08, colados de forma diferente.

> Seq2seq 架构(Sutskever, Vinyals, Le, 2014) resolveu este problema com um esquema de intenção simples.

Este é um problema que vale a pena estudar por duas razões: primeiro, o gargalhão de engarrafamento do contexto-vector é o fracasso mais pedagógico útil na PNL. Ele motiva tudo o que a atenção e os transformadores são bons em.

> Isto vale a pena aprender por duas razões. Primeiro, é o fracasso do maior valor pedagógico da PNL.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

**Encoder.**Um RNN que lê a frase fonte.**context vector** um resumo de tamanho fixo de toda a entrada.

> **编码器（Encoder）。**A RNN... o seu estado oculto final é:**上下文向量**  整条输入的固定大小摘要──据说不会丢失任何内容的源信息──

**Decoder.**Outro RNN iniciado a partir do vetor de contexto. Em cada etapa, ele toma o token gerado anteriormente como entrada e produz uma distribuição sobre o vocabulário alvo.`<EOS>`O token é produzido ou o máximo de comprimento é atingido.

> **解码器（Decoder）。**O outro RNN de inicialização do valor de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda de onda`<EOS>`- O que é o maior tamanho?

**Training:**Perda de entropia cruzada em cada passo do decodificador, somada sobre a sequência.

> **训练：**Cada passo de descifrador perde o intervalo, a procura e a perda na sequência.

**Teacher forcing.**Durante o treino, a entrada do decodificador em passo `t`é o símbolo de verdade no ponto de partida`t-1`O modelo não é um sistema de cálculo, mas um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, que é um sistema de cálculo, e que é um sistema de cálculo, é um sistema de cálculo, e que é um sistema de cálculo, é um sistema de cálculo, é um sistema de cálculo, e um sistema de cálculo, é um sistema de cálculo, que é um sistema de cálculo, e um sistema de cálculo, e um sistema de cálculo, é um sistema de cálculo, é um sistema de cálculo, que é um sistema de cálculo, e um sistema de cálculo, e um sistema de cálculo, por exemplo, é um sistema de cálculo, é um sistema de cálculo, é um sistema de cálculo, é um sistema de cálculo, é um sistema de cálculo, e um sistema de cálculo, e um sistema de cálculo, é um sistema de cálculo, e um sistema de cálculo, de cálculo, de cálculo, e um sistema de cálculo, de cálculo, e é um sistema de cálculo, de cálculo, e é um sistema de cálculo, de cálculo, e é um sistema de cálculo, por exemplo, é, é um sistema de cálculo, é um sistema de cálculo, é um sistema de cálculo, é um sistema de cálculo, e é, é um**exposure bias**- Não .

> **教师强制（Teacher Forcing）。**                                                                                                                                                                                                                                                              `t`O ingresso é localizado.`t-1`De* verdade* token, em vez de o descifrador próprio anterior uma previsão. Isto estabilizou treinamento; sem ele, os primeiros erros de classe, o modelo nunca aprenderá.**暴露偏差（Exposure Bias）**- Não.

**The bottleneck.**Tudo o que o codificador aprendeu sobre a fonte deve ser comprimido para esse vetor de contexto. Frases longas perdem detalhes. Palavras raras ficam borbulhadas. Reordem (chat noir vs. gato preto) deve ser memorizado, não calculado.

> **瓶颈。**Tudo o que o codificador aprendeu sobre a origem deve ser comprimido para o que ele escreveu.

Atenção (leção 10) corrige isso deixando o decodificador olhar para * cada * estado oculto do codificador, não apenas o último.

> Atenção(第 10 课) 通过让解码器查看* cada*编码器隐藏状态(不仅仅是最后一个) 来修复这个问题――这是全部的关键点――

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.
```figure
lstm-gates
```

## Construí-lo

### Passo 1: um codificador

```python
import torch
import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, src_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(src_vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)

    def forward(self, src):
        e = self.embed(src)
        outputs, hidden = self.gru(e)
        return outputs, hidden
```

`outputs`tem forma`[batch, seq_len, hidden_dim]` um estado oculto por posição de entrada. `hidden`tem forma`[1, batch, hidden_dim]`A lição 08 diz "pool over outputs for classification". Aqui mantemos o último estado oculto como o vector de contexto, e ignoramos as saídas por passo.

> `outputs`形状为 `[batch, seq_len, hidden_dim]` Cada entrada de posição é um estado oculto.`hidden`形状为 `[1, batch, hidden_dim]` Último passo.                                                                                                                                                                                                                                                                                                                                                                         

### Passo 2: um decodificador

```python
class Decoder(nn.Module):
    def __init__(self, tgt_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(tgt_vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, tgt_vocab_size)

    def forward(self, token, hidden):
        e = self.embed(token)
        out, hidden = self.gru(e, hidden)
        logits = self.fc(out)
        return logits, hidden
```

O decodificador é chamado um passo a tempo. Entrada: um lote de tokens individuais e o estado oculto atual. saída: logs de vocabulário para o próximo token e o estado oculto atualizado.

> 解码器每次调用一步──输入:一批单个代币 和当前隐藏状态──输出: 下一个代币的词表 logits 和更新后的隐藏状态──

### Passo 3: ciclo de formação com o professor forçando

```python
def train_batch(encoder, decoder, src, tgt, bos_id, optimizer, teacher_forcing_ratio=0.9):
    optimizer.zero_grad()
    _, hidden = encoder(src)
    batch_size, tgt_len = tgt.shape
    input_token = torch.full((batch_size, 1), bos_id, dtype=torch.long)
    loss = 0.0
    loss_fn = nn.CrossEntropyLoss(ignore_index=0)

    for t in range(tgt_len):
        logits, hidden = decoder(input_token, hidden)
        step_loss = loss_fn(logits.squeeze(1), tgt[:, t])
        loss += step_loss
        use_teacher = torch.rand(1).item() < teacher_forcing_ratio
        if use_teacher:
            input_token = tgt[:, t].unsqueeze(1)
        else:
            input_token = logits.argmax(dim=-1)

    loss.backward()
    optimizer.step()
    return loss.item() / tgt_len
```

Duas botões que valham a pena nomear.`ignore_index=0`Salta perdas em tokens de enchimento. `teacher_forcing_ratio`é a probabilidade de usar o token verdadeiro versus a previsão do modelo em cada etapa. Comece em 1.0 (forçando o professor completo) e aneal para baixo para ~0.5 sobre o treinamento para fechar a lacuna de viés de exposição.

> Duas características dignas de atenção:`ignore_index=0`- Não, não. - Não, não.`teacher_forcing_ratio`É a probabilidade de cada passo de usar um token real e de prever um modelo.

### Passo 4: Localização de inferências (avidas)

```python
@torch.no_grad()
def greedy_decode(encoder, decoder, src, bos_id, eos_id, max_len=50):
    _, hidden = encoder(src)
    batch_size = src.shape[0]
    input_token = torch.full((batch_size, 1), bos_id, dtype=torch.long)
    output_ids = []
    for _ in range(max_len):
        logits, hidden = decoder(input_token, hidden)
        next_token = logits.argmax(dim=-1)
        output_ids.append(next_token)
        input_token = next_token
        if (next_token == eos_id).all():
            break
    return torch.cat(output_ids, dim=1)
```

A codificação gananciosa escolhe o token de maior probabilidade em cada passo. Pode desviar-se: uma vez que você se compromete com um token, não pode desvincular-se. **Beam search**Mantém o topo...`k`Sequências parciais vivas e escolhe o mais alto escore completo no final.

> 贪心解码每步选择最高概率的代币――它可能走偏: uma vez que você submetido um token, é inábil retirar――**束搜索（Beam Search）**保持排名前 `k`de secções de sequência sobrevivem, na última seleção da secção máxima de sequência completa.

### Passo 5: o gargalo de engarrafamento, demonstrado

Treinar o modelo em uma tarefa de cópia de brinquedo: fonte `[a, b, c, d, e]`, alvo`[a, b, c, d, e]`Aumentar o comprimento da sequência, observar a precisão.

> Em jogo de replicação de tarefas`[a, b, c, d, e]`, objectivo `[a, b, c, d, e]`                                                                                                                                                                                                                                                              

```
seq_len=5   copy accuracy: 98%
seq_len=10  copy accuracy: 91%
seq_len=20  copy accuracy: 62%
seq_len=40  copy accuracy: 23%
```

Um único estado oculto GRU não pode memorizar sem perdas uma entrada de 40 tokens. A informação está lá em cada passo do codificador, mas o decodificador só vê o último estado.

> 单个GRU 隐藏状态无法无损记忆 40 代币的输入――信息存在于每个编码器步骤,但解码器只看到最后状态――注意力直接修复了这个问题――

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

PyTorch tem `nn.Transformer`E ...`nn.LSTM`- baseado em modelos de sequência.`transformers`Na biblioteca, os navios completos de modelos de codificadores-decodificadores (BART, T5, mBART, NLLB) são treinados em bilhões de tokens.

> - Tenho uma tocha .`nn.Transformer`E baseado em`nn.LSTM`模板──Hugging Face 的 `transformers`O banco fornece um modelo completo de codificadores-descodificadores em bilhões de tokens.

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tok = AutoTokenizer.from_pretrained("facebook/bart-base")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

src = tok("Translate this to French: Hello, how are you?", return_tensors="pt")
out = model.generate(**src, max_new_tokens=50, num_beams=4)
print(tok.decode(out[0], skip_special_tokens=True))
```

Os encodadores-decodadores modernos deixaram cair RNNs para transformadores. A forma de alto nível (encodador, decodador, gerar-token-by-token) é idêntica ao papel seq2seq de 2014. O mecanismo dentro de cada bloco é diferente.

> O moderno codificador-descodificador usal transformador substituiu RNN── alta estrutura( codificador、descodificador、 cada token (produzido) com o artigo seq2seq de 2014 完全相同──各块内部的机制不同──

### Quando ainda se pode procurar o seq2seq baseado em RNN

Quase nunca, para novos projectos.

> Para novos projectos, quase não há nenhuma exceção específica:

- Tradução de streaming onde você consome entrada um token por vez com memória limitada.
  流式翻译,逐代币 消耗输入,内存有界──
- Geração de texto no dispositivo onde o custo da memória do transformador é proibitivo.
  设备端文本生成,Transformer 内存成本过高──
- Entender o gargalho de encodeador-decodeador é o caminho mais rápido para entender por que os transformadores ganharam.
  O que é que é o Transformer?

### Preconceito de exposição e suas mitigações

- **Scheduled sampling.**Relação de força do professor durante o treinamento para que o modelo aprenda a recuperar dos seus próprios erros.
  **计划采样（Scheduled Sampling）。** Durante o treino, o professor de retorno de incêndio forçou a proporção, que o modelo de aprendizagem recupere de seus próprios erros
- **Minimum risk training.**Treinar em pontuação de nível de sentença BLEU em vez de nível de token entropia cruzada.
  **最小风险训练（Minimum Risk Training）。**Em termos de expressão, o nível azul é o número de divisões, e não o nível de transferência.
- **Reinforcement learning fine-tuning.**Recompense o gerador de sequências com uma métrica usada no moderno LLM RLHF.
  **强化学习微调。**Utilize indicação de premiação gerador de cadeia de graduação.

Os três ainda se aplicam à geração baseada em transformadores.

> Esta terceira ainda é aplicável para a geração baseada em Transformer.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

## Envia-o . Produto .

Salva como`outputs/prompt-seq2seq-design.md`- Não .

> 保存为 `outputs/prompt-seq2seq-design.md`- Não .

```markdown
---
name: seq2seq-design
description: Design a sequence-to-sequence pipeline for a given task.
phase: 5
lesson: 09
---

Given a task (translation, summarization, paraphrase, question rewrite), output:

1. Architecture. Pretrained transformer encoder-decoder (BART, T5, mBART, NLLB) is the default. RNN-based seq2seq only for specific constraints.
2. Starting checkpoint. Name it (`facebook/bart-base`, `google/flan-t5-base`, `facebook/nllb-200-distilled-600M`). Match the checkpoint to task and language coverage.
3. Decoding strategy. Greedy for deterministic output, beam search (width 4-5) for quality, sampling with temperature for diversity. One sentence justification.
4. One failure mode to verify before shipping. Exposure bias manifests as generation drift on longer outputs; sample 20 outputs at the 90th-percentile length and eyeball.

Refuse to recommend training a seq2seq from scratch for under a million parallel examples. Flag any pipeline that uses greedy decoding for user-facing content as fragile (greedy repeats and loops).
```

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 

## Exercícios.

1. **Easy.**Implementar a tarefa de cópia de brinquedo. Treinar um GRU seq2seq em pares de entrada e saída onde o alvo é igual à fonte. Medir a precisão em comprimentos 5, 10, 20. Reproduzir o gargalo de engarrafamento.
   **简单。**实现玩具复制任务──训练 GRU seq2seq 在目标等于源的输入输出对上──测量长度 5、10、20 的准确率──复现瓶──
2. **Medium.**Adicionar a decodificação de busca de feixe com largura de feixe 3. Medir o azul em um pequeno corpus paralelo contra a ganância.
   **中等。**添束宽度为 3 的束搜索解码──在小平行语料上测量对贪心的蓝色──记录束搜索在哪里胜出(normalmente são os últimos tokens)以及在哪里没有区别──
3. **Hard.**- A música é perfeita .`facebook/bart-base`Comparar a saída de feixe 4 do modelo de base com a do modelo base em entradas mantidas.
   **困难。**Em 10 mil para o conjunto de dados de`facebook/bart-base`◊ em deixar de entrar em conjunto com o modelo de menor modulação 4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Termos-chave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Encoder（编码器） | Input RNN / 输入 RNN | Reads source. Produces per-step hidden states and a final context vector. / 读取源。产生逐步隐藏状态和最终上下文向量。 |
| Decoder（解码器） | Output RNN / 输出 RNN | Initialized from context vector. Generates target tokens one at a time. / 从上下文向量初始化。逐个生成目标 token。 |
| Context vector（上下文向量） | The summary / 摘要 | Final encoder hidden state. Fixed size. The bottleneck attention solves. / 最终编码器隐藏状态。固定大小。注意力解决的瓶颈。 |
| Teacher forcing（教师强制） | Use true tokens / 使用真实 token | Feed the ground-truth previous token at training time. Stabilizes learning. / 训练时馈入真实的前一个 token。稳定学习。 |
| Exposure bias（暴露偏差） | Train/test gap / 训练/测试差距 | Model trained on true tokens never practiced recovering from its own mistakes. / 在真实 token 上训练的模型从未练习从自己的错误中恢复。 |
| Beam search（束搜索） | Better decoding / 更好的解码 | Keep top-k partial sequences alive at each step instead of committing greedily. / 每步保持排名前 k 的部分序列存活，而非贪心提交。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.

## Mais leitura 延伸阅读

- [Sutskever, Vinyals, Le (2014). Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215)O artigo original seq2seq. Quatro páginas.
- [Cho et al. (2014). Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078) introduziu o GRU e o enquadramento de codificador-decodificador. /  introduced GRU 和编码器-解码器框架──
- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) o papel de atenção. Leia imediatamente após esta aula. / 注意力论文──在本课后立即阅读──
- [PyTorch NLP from Scratch tutorial](https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html) construível seq2seq + código de atenção. / 可构建的 seq2seq + 注意力代码──
