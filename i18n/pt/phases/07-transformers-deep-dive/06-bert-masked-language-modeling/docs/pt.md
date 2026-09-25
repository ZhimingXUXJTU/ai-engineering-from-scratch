# BERT  Modelagem de Língua Enmascarada ∙ BERT  掩码语言模型

> O GPT prevê a próxima palavra, o BERT prevê uma palavra que falta, uma frase de diferença e meia década de tudo em forma de inserção.

> **【中文解读】**BERT é um Transformador de Encoder-only, usando o treinamento de pré-conhecimento de massas.

**Type:** Hands-on | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 5 · 02 (Text Representation) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 5 · 02 (Text Representation)
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

Em 2018, cada tarefa de PNL  sentimento, NER, QA, entailment  treinou seu próprio modelo a partir do zero em seus próprios dados rotulados. Não havia um checkpoint pré-treinado "entender inglês" que você pudesse ajustar. ELMo (2018) mostrou que você poderia treinar embutimentos contextuais com um LSTM bidirecional; ajudou, mas não generalizou.

> Em 2018, cada tarefa de PNL  análise emocional  nome de corpo identificação  respostas  texto  contendo  todos necessários em seus próprios dados de marcação a partir de modelo de treinamento zero .

BERT (Devlin et al. 2018) perguntou: e se pegássemos num codificador transformador, treinássemos-o em cada frase na internet e forçássemos-o a prever palavras faltantes de contexto em ambos os lados?

> BERT(Devlin  et al., 2018) apresentou uma questão fundamental: se usar o Transformer 编码器, treinando todas as frases na Internet, forçá-lo a basear-se em dois lados de palavras que são ocultadas, como será?

O resultado: em 18 meses, o BERT e suas variantes (RoBERTa, ALBERT, ELECTRA) dominaram todas as listas de liderança de PNL existentes.

> O resultado é: em 18 meses, BERT e seus variantes (Robert, Albert, Electra) dominaram todas as listas de pesquisa de PNL. Até 2020, cada mecanismo de pesquisa no mundo tem um BERT.

Em 2026, os modelos com apenas codificadores ainda são a ferramenta certa para classificação, recuperação e extração estruturada. Eles funcionam 510x mais rápido por token do que os decodificadores e seus incorporados são a espinha dorsal de cada pilha de recuperação moderna.

> Até 2026, o modelo especial de codificador ainda é a escolha correta de classificação, pesquisa e estruturação. A velocidade de execução de cada token é de 5-10 vezes maior do que a de codificador rápido, sendo incorporado em cada sistema moderno de pesquisa.

> **【中文解读】**A revolução do BERT consiste no "pre-training+micro-modulação": em grande escala sem marcas, o pre-training é feito usando um modelo de linguagem masquerada (MLM), e depois reduzindo a quantidade de parâmetros em tarefas específicas.

## O conceito central.

![Masked language modeling: pick tokens, mask them, predict originals](../assets/bert-mlm.svg)

### O sinal de treinamento

Faça uma frase:`the quick brown fox jumps over the lazy dog`- Não .

> - Não .`the quick brown fox jumps over the lazy dog`- Não.

Mascarar 15% dos tokens aleatoriamente:

> Como se fosse 15% de token:

```
input:  the [MASK] brown fox jumps [MASK] the lazy dog
target: the quick brown fox jumps over the lazy dog
```

Treinar o modelo para prever os tokens originais em posições mascaradas.`[MASK]`Na posição 1 pode usar `brown fox jumps`É o que o GPT não pode fazer.

> 訓練模型在被掩藏位置预测 原始代币──因为编码器是双向的,预测位置是1 的 `[MASK]`Pode utilizar a posição 2 及后的`brown fox jumps`É o que o GPT não faz.

### As regras da máscara BERT

Dos 15% dos tokens selecionados para previsão:

> Em 15% dos tokens utilizados na previsão:

- 80% são substituídos por `[MASK]`- Não .
  Tradução do idioma: 80% 被替换为`[MASK]`- Não.
- 10% são substituídos por um token aleatório.
  Chinese:                                                                                                                                                                                                                                                              
- 10% permanecem inalterados.
  Chinese: 保持不变──

Porque não sempre ?`[MASK]`Porque ?`[MASK]`O modelo de aprendizagem é o modelo de aprendizagem que não aparece na hora da inferência.`[MASK]`A posição de 100% mascarada criaria uma mudança de distribuição entre o pré-treino e o ajuste fino.

> Porque não é sempre útil?`[MASK]`Porque ?`[MASK]`Não aparecerá nunca na hora de pensar. Se o modelo de treinamento estiver em posição de 100% de escuridão, espero ver.`[MASK]`, causando uma deslocação de distribuição entre o treinamento prévio e o pequeno.

> **【中文解读】**A teoria de que o token não apareça é que o modelo também veja o token normal e o token de substituição.

> **【拓展：BERT 在 RAG 系统中的角色】**现代 RAG(检索增强生成) no sistema,BERT 变体 ainda é o núcleo do estágio de检索. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型. 模型.           模型.                                                                                                                                                   

### Próximo Previsão de Sentença (NSP)  e por que foi retirado

O BERT original também foi treinado em NSP: dado duas frases A e B, prevê se B segue A. RoBERTa (2019) abolou e mostrou que o NSP prejudicou, não ajudou.

> O primeiro é o primeiro, que é o primeiro, que é o primeiro, que é o primeiro, que é o primeiro, que é o primeiro, que é o segundo.

### O que mudou em 2026: ModernBERT

O papel ModernBERT de 2024 reconstruiu o bloco com primitivos de 2026:

> O ModernBERT de 2024 reedificou o bloco de codificação com componentes modernos:

| Component | Original BERT (2018) | ModernBERT (2024) |
|-----------|----------------------|-------------------|
| 组件 | 原始 BERT (2018) | ModernBERT (2024) |
| Positional | Learned absolute | RoPE |
| 位置编码 | 学习式绝对位置 | RoPE |
| Activation | GELU | GeGLU |
| 激活函数 | GELU | GeGLU |
| Normalization | LayerNorm | Pre-norm RMSNorm |
| 归一化 | LayerNorm | 前归一化 RMSNorm |
| Attention | Full dense | Alternating local (128) + global |
| 注意力 | 全密集 | 交替局部 (128) + 全局 |
| Context length | 512 | 8192 |
| 上下文长度 | 512 | 8192 |
| Tokenizer | WordPiece | BPE |
| 分词器 | WordPiece | BPE |

E ao contrário da pilha de 2018, é Flash-Attention-native. Inferência é 23× mais rápida em comprimento de sequência 8K do que DeBERTa-v3 com melhores pontuações GLUE.

> Diferente da tecnologia de 2018, o ModernBERT originalmente suporta Flash Attention.

### Casos de uso que ainda escolhem um codificador em 2026

| Task | Why encoder beats decoder |
|------|---------------------------|
| 任务 | 为什么编码器优于解码器 |
| Retrieval / semantic search embeddings | Bidirectional context = better embedding quality per token |
| 检索/语义搜索嵌入 | 双向上下文 = 每个 token 更好的嵌入质量 |
| Classification (sentiment, intent, toxicity) | One forward pass; no generation overhead |
| 分类（情感、意图、毒性） | 一次前向传播；无生成开销 |
| NER / token labeling | Per-position output, natively bidirectional |
| NER/token 标注 | 逐位置输出，天然双向 |
| Zero-shot entailment (NLI) | Classifier head on top of encoder |
| 零样本蕴含 (NLI) | 编码器之上的分类器头 |
| Reranker for RAG | Cross-encoder scoring, 10x faster than LLM rerankers |
| RAG 重排序器 | 交叉编码器评分，比 LLM 重排序器快 10 倍 |

## Construí-lo e realizei-o.
```figure
transformer-residual
```

## Construí-lo

### Passo 1: Mastização da lógica

Veja .`code/main.py`- A função`create_mlm_batch`Retorna IDs de entrada (com máscaras aplicadas) e rótulos (apenas em posições mascaradas, -100 em outros lugares  Ignore PyTorch's index convention).

> 参见 `code/main.py`。 função `create_mlm_batch`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

```python
def create_mlm_batch(tokens, vocab_size, mask_prob=0.15, rng=None):
    input_ids = list(tokens)
    labels = [-100] * len(tokens)
    for i, t in enumerate(tokens):
        if rng.random() < mask_prob:
            labels[i] = t
            r = rng.random()
            if r < 0.8:
                input_ids[i] = MASK_ID
            elif r < 0.9:
                input_ids[i] = rng.randrange(vocab_size)
            # else: keep original
    return input_ids, labels
```

### Passo 2: executar previsão MLM em um corpus pequeno

Treinar um codificador de 2 camadas + MLM cabeça em um vocabulário de 20 palavras, 200 frases.

> Em 20 palavras de vocabulário e 200 sentenças, treinar um programador de 2 níveis + MLM ︎ não envolve a escala apenas fazer um exame de racionalidade da propagação anterior completo treinamento requer PyTorch

### Passo 3: comparação dos tipos de máscaras

Mostre como a regra de três direções mantém o modelo utilizável sem `[MASK]`A previsão de uma frase não mascarada e de uma frase mascarada devem produzir distribuições simbólicas razoáveis porque o modelo viu ambos os padrões no treinamento.

> Mostra regras de três caminhos como fazer um modelo em ausência`[MASK]`Em alguns casos, ainda é possível prever as frases não ocultas e as frases ocultas. Ambas devem gerar uma distribuição razoável, pois os modelos já foram encontrados no treinamento.

### Passo 4: Tópico de sintonia

Substitua a cabeça de MLM por uma cabeça de classificação num conjunto de dados de sentimento de brinquedo. Somente a cabeça entra; o codificador está congelado. Este é o padrão que todas as aplicações BERT seguem.

> Usar o tipo de cabeça substituindo o MLM, treinar em um conjunto de dados de emoções de brinquedos.

> **【拓展：BERT 微调的实践技巧】**As melhores práticas de BERT 微调 incluem: 1) Utilize menor de aprendizagem rate ((2e-5 até 5e-5) evitar prejudicar o prep training weight; 2) para usar token de classe de tarefas (CLS) como expressão de frase; 3) para NER etc. para token de tarefas, usar output de cada posição; 4) para resolver gradualmente (defreezing) pode ser promovido em pequenos dados.

## Use-o com o framework implementado.

```python
from transformers import AutoModel, AutoTokenizer

tok = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
model = AutoModel.from_pretrained("answerdotai/ModernBERT-base")

text = "Attention is all you need."
inputs = tok(text, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, N, 768)
```

**Embedding models are fine-tuned BERT.** `sentence-transformers`modelos como `all-MiniLM-L6-v2`O codificador é o mesmo, a perda mudou.

> **嵌入模型是微调后的 BERT。** `sentence-transformers`模型如 `all-MiniLM-L6-v2`Na essência é a mesma estrutura do programador em relação ao treinamento de perda.

**Cross-encoder rerankers are also fine-tuned BERT.**Classificação em pares em`[CLS] query [SEP] doc [SEP]`A atenção bidirecional entre consulta e doc é exatamente o que dá aos encodadores cruzados a vantagem de qualidade em relação aos bicodadores.

> **交叉编码器重排序器也是微调后的 BERT。**Em`[CLS] query [SEP] doc [SEP]`A atenção bidirecional entre consulta e arquivo é a razão pela qual a qualidade do redator de transferência é melhor do que a de redator duplo.

**When not to pick BERT in 2026.**Qualquer coisa gerativa. O codificador não tem nenhuma maneira sensata de produzir tokens autoregressivamente. Além disso: qualquer coisa abaixo de parâmetros 1B onde um pequeno decodificador pode igualar a qualidade com mais flexibilidade (Phi-3-Mini, Qwen2-1.5B).

> **2026 年何时不选 BERT。**任何生成式任务──编码器没有合理的方式进行自归代币 生成──此外, em 1B 参数以下的场景,小型解码器 ((如 Phi-3-Mini、Qwen2-1.5B) pode obter uma flexibilidade considerável com menores参数──

> **【拓展：ModernBERT 的现代化改进】**ModernBERT(2024) vai 2018 BERT arquitetura completa atualização:RoPE 替代学习式位置编码、GeGLU 替代 GELU、前归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归

## Envia-o . Produto .

Veja .`outputs/skill-bert-finetuner.md`. O âmbito de competência é ajustado a um BERT (selecção de espinha dorsal, especificação de cabeça, dados, avaliação, parada) para uma nova tarefa de classificação ou extracção.

> 参见 `outputs/skill-bert-finetuner.md` Esta habilidade é utilizada para novas categorias ou tarefas de planejamento de tarefas (BERT 微调方案) 

## Exercícios.

1. **Easy.**Corra .`code/main.py`Confirme que ~ 15% são selecionados, e daqueles ~ 80% se tornam `[MASK]`- Não .
   Tradução: 运行`code/main.py`, imprimir 10.000 tokens de distribuição escondida, confirmar cerca de 15% selecionados, dos quais cerca de 80% são transformados.`[MASK]`- Não.
2. **Medium.**Implementar mascaramento de palavras inteiras: se uma palavra é tokenizada em subpalavras, mascarar todas as subpalavras juntas ou nenhuma. Medir se isso melhora a precisão de MLM em um corpus de 500 frases.
   Tradução do inglês: implementar o termo masquerodo: se um termo é dividido em vários subpazes, quer seja todo masquerodo ou todo não masquerodo.
3. **Hard.**Treinar um pequeno BERT de 2 camadas, d=64, em 10.000 frases de um conjunto de dados públicos.`[CLS]`Comparar com uma linha de base apenas para decodificadores em parâmetros correspondentes.
   Tradução do inglês em japonês: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏: 藏语: 藏: 藏: 藏语: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏: 藏:   藏: 藏:    藏:  藏:     藏:                                                                                                                                         `[CLS]`Qual é melhor em relação ao código base de SST-2?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| MLM | "Masked language modeling" | Training signal: randomly replace 15% of tokens with `[MASK]`, predict the originals. |
| MLM | "掩码语言建模" | 训练信号：随机将 15% 的 token 替换为 `[MASK]`，预测原始 token。 |
| Bidirectional | "Looks both ways" | Encoder attention has no causal mask — every position sees every other position. |
| 双向 | "看两边" | 编码器注意力没有因果掩码——每个位置都能看到其他所有位置。 |
| `[CLS]` | "The pooler token" | A special token prepended to every sequence; its final embedding is used as the sentence-level representation. |
| `[CLS]` | "池化 token" | 一个特殊 token，添加到每个序列开头；其最终嵌入用作句子级表示。 |
| `[SEP]` | "Segment separator" | Separates paired sequences (e.g. query/doc, sentence A/B). |
| `[SEP]` | "片段分隔符" | 分隔成对序列（如查询/文档、句子 A/B）。 |
| NSP | "Next sentence prediction" | BERT's second pretraining task; shown to be useless in RoBERTa, dropped after 2019. |
| NSP | "下一句预测" | BERT 的第二个预训练任务；RoBERTa 证明其无用，2019 年后弃用。 |
| Fine-tuning | "Adapt to a task" | Keep the encoder mostly frozen; train a small head on top for the downstream task. |
| 微调 | "适应任务" | 保持编码器基本冻结；在顶部训练一个小头用于下游任务。 |
| Cross-encoder | "A reranker" | A BERT that takes both query and doc as input, outputs a relevance score. |
| 交叉编码器 | "重排序器" | 同时接收查询和文档作为输入的 BERT，输出相关性分数。 |
| ModernBERT | "2024 refresh" | Encoder rebuilt with RoPE, RMSNorm, GeGLU, alternating local/global attention, 8K context. |
| ModernBERT | "2024 刷新版" | 用 RoPE、RMSNorm、GeGLU、交替局部/全局注意力重建的编码器，8K 上下文。 |

## Mais leitura 延伸阅读

- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)- Papel original.
  O que é que é o "Bert"?
- [Liu et al. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692)Como treinar o BERT corretamente; mata o NSP.
  Tradução do inglês para tradução livre: cómo正确训练 BERT;证明了 NSP 无用──
- [Clark et al. (2020). ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators](https://arxiv.org/abs/2003.10555) a detecção de tokens substituídos supera o MLM em computação correspondente.
  Tradução do inglês para tradução do inglês: substituir token 检测在相同计算量下优于MLM。
- [Warner et al. (2024). Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder](https://arxiv.org/abs/2412.13663)- Papel ModernBERT.
  Tradução do português:ModernBERT
- [HuggingFace `modeling_bert.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/bert/modeling_bert.py) referência de codificador canônico.
  O que é que é o "HuggingFace BERT" (HuggingFace BERT)
