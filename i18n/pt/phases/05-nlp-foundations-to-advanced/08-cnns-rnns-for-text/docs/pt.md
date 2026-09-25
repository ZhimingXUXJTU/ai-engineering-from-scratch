# CNNs e RNNs para texto

> As convulsões aprendem n-gramas, as recorrências lembram-se, ambas são substituídas pela atenção, ambas ainda são importantes em hardware limitado.
> 卷积学习 n-gram。 ciclo responsável pela memória。 ambos foram substituídos pelo mecanismo de atenção。 mas ainda são importantes em hardware limitado。

> **【中文解读】**CNN 捕捉局部 n-gram 特征,RNN 处理长程依赖──Transformer 之前的主流架构──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 11 (PyTorch Intro), Phase 5 · 03 (Word Embeddings), Phase 4 · 02 (Convolutions from Scratch) | **前置知识:** Phase 3 · 11（PyTorch 入门），Phase 5 · 03（词嵌入），Phase 4 · 02（从零实现卷积）
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

O TF-IDF e o Word2Vec produziram vetores planos que ignoraram a ordem das palavras.`dog bites man`de`man bites dog`A ordem das palavras às vezes carrega o sinal.

> TF-IDF e Word2Vec                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     `dog bites man`和 `man bites dog`词序有时携带信号

Duas famílias de arquiteturas preencheram essa lacuna antes que os transformadores chegassem.

> Antes da aparição do Transformer, duas tribos de arquiteturas preencheram esse espaço em branco.

**Convolutional nets for text (TextCNN).**Aplique convulsões 1D sobre sequências de incorporações de palavras. Um filtro de largura 3 é um detector de trigramas aprendizagem: ele abrange três palavras e produz uma pontuação. Estacle diferentes largura (2, 3, 4, 5) para detectar padrões em várias escalas. Max-pool para uma representação de tamanho fixo. plano, paralelo, rápido.

> **文本卷积网络（TextCNN）。**Em palavras embutidas em sequências de aplicação de um volume de dimensão. O amplitude de 3 é um triângulo de teste de forma a ser aprendido.

**Recurrent nets (RNN, LSTM, GRU).**Processar tokens um a cada vez, mantendo um estado oculto que transporta informações para a frente. Sequenciais, portadores de memória, comprimentos de entrada flexíveis. Modelagem de sequência dominada de 2014 a 2017, então a atenção aconteceu.

> **循环网络（RNN、LSTM、GRU）。**个个处理代币,维护向前传递信息的隐藏状态――顺序、有记忆、灵活输入长度── de 2014 a 2017 anos, a série dominante foi construída, então apareceu o mecanismo de atenção──

Esta lição constrói ambos, e depois nomeia o fracasso que motivou a atenção.

> Esta aula construiu os dois, e depois apontou o fracasso do motor de atenção.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

**TextCNN**Os tokens são incorporados.`k`A convolução 1D desliza um filtro em sequência `k`-gramas de embebimentos, produzindo um mapa de características. A max-pooling global sobre esse mapa escolhe a ativação mais forte.

> **TextCNN**(Kim, 2014) ⋅ Token 被嵌入──宽度为 ⋅`k`O que é que é que é?`k`-gram 嵌上滑波器,产生特征图――对该特征图做全局最大池化选取最强激活――从多个波器宽度最大池化输出拼接――送进分类器头――

Por que funciona. Um filtro é um n-gram aprendizagem. Max-pooling é invariable de posição, por isso "não bom" dispara a mesma característica no início ou no meio de uma revisão. Três largura de filtro com 100 filtros cada dá-lhe 300 n-gram detetores aprendidos.

> Por que é eficaz? 波器是可学习的 n-gram──最大池化是位置不变的,所以"not good"在评论开头或中间触发相同特征──三波器宽度各 100 波器给你 300 个可学习的 n-gram 检测器── treinamento é paralelo; não há dependência de ordem──

**RNN.**A cada passo .`t`, o estado oculto .`h_t = f(W * x_t + U * h_{t-1} + b)`Compartilhar .`W`- Não .`U`- Não .`b`O estado oculto no tempo.`T`Para classificação, pool across `h_1 ... h_T`(máximo, médio ou último).

> **RNN。**Em cada passo de tempo.`t`, estado oculto`h_t = f(W * x_t + U * h_{t-1} + b)`- Não.`W`- Não.`U`- Não.`b`跨时间共享──时间 `T`O estado oculto é o resumo de toda a história anterior.`h_1 ... h_T`上池化(最大、平均值或最后) ⋅

Os RNNs comuns sofrem de gradientes desaparecendo.**LSTM**Adiciona portões que decidem o que esquecer, o que armazenar e o que produzir, estabilizando gradientes através de longas sequências.**GRU**simplifica o LSTM para dois portões; desempenha de forma semelhante com menos parâmetros.

> Normal RNN  existência de problemas de desaparecimento.**LSTM**Adicionar a decisão de esquecer o que, armazenar o que e o que sair, estabilizar a escala da sequência.**GRU**Simplificar o LSTM em duas portas; os parâmetros são menores, mas o efeito é semelhante.

**Bidirectional RNNs**executar um RNN para frente e outro para trás, concatenando estados ocultos. a representação de cada token vê o contexto esquerdo e direito. essencial para etiquetar tarefas.

> **双向 RNN**运行一个RNN向前、另一个向后,拼接隐藏状态──每个代币的表示看左右两侧的上下文──对标注任务必不可少──

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.
```figure
rnn-unroll
```

## Construí-lo

### Passo 1: TextCNN em PyTorch

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


class TextCNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, n_classes, filter_widths=(2, 3, 4), n_filters=64, dropout=0.3):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.convs = nn.ModuleList([
            nn.Conv1d(embed_dim, n_filters, kernel_size=k)
            for k in filter_widths
        ])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(n_filters * len(filter_widths), n_classes)

    def forward(self, token_ids):
        x = self.embed(token_ids).transpose(1, 2)
        pooled = []
        for conv in self.convs:
            c = F.relu(conv(x))
            p = F.max_pool1d(c, c.size(2)).squeeze(2)
            pooled.append(p)
        h = torch.cat(pooled, dim=1)
        return self.fc(self.dropout(h))
```

O `transpose(1, 2)`transformações`[batch, seq_len, embed_dim]`- Não .`[batch, embed_dim, seq_len]`Porque ...`nn.Conv1d`O resultado agregado é de tamanho fixo, independentemente da comprimento da entrada.

> `transpose(1, 2)`- Não .`[batch, seq_len, embed_dim]`Gravatura`[batch, embed_dim, seq_len]`Porque ...`nn.Conv1d`O eixo intermediário é visto como um caminho. A saída posterior à polarização é de grandeza fixa, independentemente da extensão da entrada.

### Passo 2: Classificador LSTM

```python
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_classes, bidirectional=True, dropout=0.3):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=bidirectional)
        factor = 2 if bidirectional else 1
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * factor, n_classes)

    def forward(self, token_ids):
        x = self.embed(token_ids)
        out, _ = self.lstm(x)
        pooled = out.max(dim=1).values
        return self.fc(self.dropout(pooled))
```

Para classificação, o max-pooling geralmente supera a tomada do último estado oculto porque a informação no final de uma longa sequência tende a dominar o último estado.

> Em sequências, faz a maior acumulação, em vez de a última acumulação de estado. Para a classificação, a maior acumulação é geralmente melhor do que a última acumulação oculta, pois a informação do fim da longa sequência tende a dominar o último estado.

### Passo 3: a demonstração do gradiente de desaparecimento (intuição)

Uma RNN simples sem gating não pode aprender dependências de longo alcance.`A`apareceu em qualquer lugar numa sequência.`A`Se o gradiente for inferior a 1, o gradiente desaparece, se for superior a 1, ele explode.

> Não tem controle de controle RNN não pode aprender a depender de longo prazo.`A`Se não aparecer em qualquer posição da sequência.`A`Na posição 1, a longitude do sequência é de 100, a gradiência da perda deve passar por 99 vezes o ciclo de multiplicação do peso. Se o peso for menor que 1, a gradiência desaparece. Se for maior que 1, a gradiência explode.

```python
def vanishing_gradient_sim(seq_len, recurrent_weight=0.9):
    import math
    return math.pow(recurrent_weight, seq_len)


# At weight=0.9 over 100 steps:
#   0.9 ^ 100 ≈ 2.7e-5
# The gradient from step 100 to step 1 is effectively zero.
```

Os LSTMs corrigem isto com um **cell state**O GRU é um sistema de treinamento que funciona através da rede com apenas interações adicionais (o gate esquece-o multiplicativamente, mas os gradientes ainda fluem ao longo da "autopista").

> LSTM  através de um**细胞状态** Correção do problema, este estado só através de aumento de interação através da rede  esquecimento de sua forma de multiplicar, mas a gradiência ainda está a circular ao longo da "autopista"  GrU com menos parâmetros fez coisas semelhantes  ambas permitem que você treine estabilização em 100+ sequências de passos 

### Passo 4: por que isso ainda não foi suficiente

Três problemas persistiam mesmo com os LSTMs.

> Mesmo que haja LSTM, três problemas persistem.

1. **Sequential bottleneck.**O treinamento de um RNN numa sequência de comprimento 1000 requer 1000 passos em série para frente/para trás.
   **顺序瓶颈。**Em longitude para 1000 de sequências de treinamento RNN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
2. **Fixed-size context vector in encoder-decoder setups.**O decodificador vê apenas o estado oculto final do codificador, comprimido sobre toda a entrada. As entradas longas perdem detalhes. A lição 09 abrange isso diretamente.
   **编码器-解码器中的固定大小上下文向量。**O descifrador só vê o estado oculto final do codificador, comprimindo toda a entrada.
3. **Distant-dependency accuracy ceiling.**Os LSTMs superam as RNNs comuns, mas ainda têm dificuldade em propagar informações específicas em mais de 200 passos.
   **远距离依赖准确率天花板。**LSTM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

A atenção resolveu os três, os transformadores reduziram completamente a recorrência, a lição 10 é o pivô.

> Atenção resolveu todos os três problemas. O transformador abandonou completamente o ciclo.

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

O PyTorch's `nn.LSTM`- Não .`nn.GRU`, e `nn.Conv1d`O código de formação é padrão.

> PyTorch `nn.LSTM`- Não.`nn.GRU`和 `nn.Conv1d`É o que estamos fazendo.

Embrace Face navios pre-entrenados embutidos que você conectar como a camada de entrada:

> Abraçando o rosto  provide pré-treinamento inserção como entrada inserção:

```python
from transformers import AutoModel

encoder = AutoModel.from_pretrained("bert-base-uncased")
for param in encoder.parameters():
    param.requires_grad = False


class BertCNN(nn.Module):
    def __init__(self, n_classes, filter_widths=(2, 3, 4), n_filters=64):
        super().__init__()
        self.encoder = encoder
        self.convs = nn.ModuleList([nn.Conv1d(768, n_filters, kernel_size=k) for k in filter_widths])
        self.fc = nn.Linear(n_filters * len(filter_widths), n_classes)

    def forward(self, input_ids, attention_mask):
        with torch.no_grad():
            out = self.encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        x = out.transpose(1, 2)
        pooled = [F.max_pool1d(F.relu(conv(x)), kernel_size=conv(x).size(2)).squeeze(2) for conv in self.convs]
        return self.fc(torch.cat(pooled, dim=1))
```

Lista de verificação de restrições de uso quando se adequar.

> 适用约束检查清单──

- **Edge / on-device inference.**TextCNN com GloVe embutidos é 10-100 vezes menor do que um transformador.
  **边缘/设备端推理。**带 GloVe 嵌入的 TextCNN 比变压器 小 10-100 倍――如果部署目标是手机,这就是你的技术──
- **Streaming / online classification.**RNN processa um token por vez; transformadores precisam da sequência completa. Para o texto recebido em tempo real, LSTMs ainda ganham.
  **流式/在线分类。**RNN Cada vez que processar um token; Transformer  precisa de um processo completo.
- **Tiny models for baselines.**Iteração rápida em uma nova tarefa.
  **用于基线的微型模型。**Em novas missões, rápido. Em CPU, 5 minutos de treinamento.
- **Sequence labeling with limited data.**BiLSTM-CRF (leção 06) ainda é uma arquitetura NER de nível de produção para frases com rótulos de 1k-10k.
  **数据有限的序列标注。**BiLSTM-CRF ((第 06 课) para 1k-10k 标注句子 ainda é produção de classe NER 架构──

O resto vai para um transformador.

> Tudo o resto com o Transformer.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

## Envia-o . Produto .

Salva como`outputs/prompt-text-encoder-picker.md`- Não .

> 保存为 `outputs/prompt-text-encoder-picker.md`- Não .

```markdown
---
name: text-encoder-picker
description: Pick a text encoder architecture for a given constraint set.
phase: 5
lesson: 08
---

Given constraints (task, data volume, latency budget, deploy target, compute budget), output:

1. Encoder architecture: TextCNN, BiLSTM, BiLSTM-CRF, transformer fine-tune, or "use a pretrained transformer as a frozen encoder + small head".
2. Embedding input: random init, GloVe / fastText frozen, or contextualized transformer embeddings.
3. Training recipe in 5 lines: optimizer, learning rate, batch size, epochs, regularization.
4. One monitoring signal. For RNN/CNN models: attention mechanism absence means they miss long-range deps; check per-length accuracy. For transformers: fine-tuning collapse if LR too high; check train loss.

Refuse to recommend fine-tuning a transformer when data is under ~500 labeled examples without showing that a TextCNN / BiLSTM baseline has plateaued. Flag edge deployment as needing architecture-before-everything.
```

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 

## Exercícios.

1. **Easy.**Treinar um TextCNN em um conjunto de dados de brinquedos de 3 classes (você invente os dados). Verifique se as largura dos filtros (2, 3, 4) superam uma única largura (3) em média F1.
   **简单。**Em um conjunto de dados de 3 tipos de brinquedos, a formação de texto (TextoCNN) é feita por você mesmo.
2. **Medium.**Implementar pool max, pool mean e pool de último estado para o classificador LSTM. Comparar em um pequeno conjunto de dados; documento que o pooling ganha e hipotetizar por quê.
   **中等。**Para LSTM, a classificação de sistemas de cálculo de valores e de dados é a melhor forma de obter o máximo de quantificação, a quantificação de valores e o valor de quantificação de dados.
3. **Hard.**Construa um tagger BiLSTM-CRF NER (combine a lição 06 e esta). Treine no CoNLL-2003. Compare com a linha de base CRF-solo da lição 06 e com um ajuste fino do BERT. Relate o tempo de treinamento, a memória e a F1.
   **困难。**Construir BiLSTM-CRF NER 标标标机(结合第 06 课和本课) ⋅ em CoNLL-2003 上训练──与第 06 课的纯CRF基线和BERT 微调比较──报告训练时间、内存和F1──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Termos-chave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| TextCNN | CNN for text / 文本 CNN | Stack of 1D convolutions over word embeddings with global max-pool. Kim (2014). / 在词嵌入上堆叠一维卷积加全局最大池化。Kim (2014)。 |
| RNN（循环神经网络） | Recurrent net / 循环网络 | Hidden state updated at each time step: `h_t = f(W x_t + U h_{t-1})`. / 每个时间步更新隐藏状态：`h_t = f(W x_t + U h_{t-1})`。 |
| LSTM | Gated RNN / 门控 RNN | Adds input / forget / output gates + a cell state. Trains stably through long sequences. / 添加输入/遗忘/输出门 + 细胞状态。在长序列上稳定训练。 |
| GRU | Simpler LSTM / 更简单的 LSTM | Two gates instead of three. Similar accuracy, fewer parameters. / 两个门代替三个。类似准确率，更少参数。 |
| Bidirectional（双向） | Both directions / 两个方向 | Forward + backward RNN concatenated. Every token sees both sides of its context. / 前向 + 后向 RNN 拼接。每个 token 看到其上下文两侧。 |
| Vanishing gradient（梯度消失） | Training signal dies / 训练信号消失 | Repeated multiplication by <1 weights in plain RNNs makes early-step gradients effectively zero. / 普通 RNN 中对小于 1 的权重反复乘法使早期步骤的梯度实际上为零。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.

## Mais leitura 延伸阅读

- [Kim, Y. (2014). Convolutional Neural Networks for Sentence Classification](https://arxiv.org/abs/1408.5882)O texto é legível.
- [Hochreiter, S. and Schmidhuber, J. (1997). Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf)O artigo LSTM é inesperadamente lúcido.
- [Olah, C. (2015). Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/) os diagramas que tornaram os LSTMs acessíveis a todos. /  Deixem os LSTMs para todos tornarem-se compreensíveis.
